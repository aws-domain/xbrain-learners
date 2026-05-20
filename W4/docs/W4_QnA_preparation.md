# W4 — Q&A Preparation (Individual QnA — 30% presentation score)

## Context

Project: Build an AI system (chatbot) using **n8n** as orchestration layer, connected to:
- **Qdrant Vector DB** (RAG với Hybrid Search) — 36 markdown docs về GeekBrain
- **PostgreSQL** — structured data (costs, incidents, SLA targets, daily metrics) + persistent memory
- **Monitoring API** (HTTP tools) — live service status (/services, /status, /metrics, /incidents)
- **Memory** — PostgreSQL-based persistent conversation history cho multi-turn

Architecture: n8n AI Agent → Claude Opus 4.6 (Bedrock) + RAG tool (Qdrant Hybrid Search via HTTP) + PostgreSQL tool + HTTP tools + Think tool

---

## Category 1: Architecture & Design Decisions

### Q: Tại sao chọn n8n thay vì Bedrock Agents hoặc LangChain?

**A:** n8n là low-code workflow automation platform, cho phép:
- Visual workflow design — dễ debug, dễ thấy data flow qua từng node
- Native AI Agent node hỗ trợ tool calling (RAG, HTTP, database, Think)
- Không cần viết code phức tạp cho orchestration logic
- Dễ thêm/bớt tools mà không cần deploy lại
- Webhook node cho phép expose API endpoint dễ dàng
- Có sẵn Loop, Aggregate, Limit nodes cho data pipeline

So sánh:
- **vs Bedrock Agents**: Bedrock Agents lock-in vào AWS ecosystem, ít flexible khi cần custom RAG pipeline (Hybrid Search). n8n cho phép wrap custom RAG API thành HTTP tool.
- **vs LangChain**: LangChain code-heavy, cần developer maintain. n8n visual giúp non-dev team members hiểu flow. Nhưng thực tế nhóm vẫn dùng LangChain cho phần RAG API backend.

Trade-off: Ít control hơn raw code, phụ thuộc vào n8n platform. Nhưng iteration speed nhanh hơn nhiều.

---

### Q: Giải thích architecture flow từ lúc user gửi câu hỏi đến lúc nhận response?

**A:** Có 2 luồng chính:

**Luồng 1 — Agent (Query time):**
1. User gửi message → Webhook node (POST) hoặc "When chat message received" trigger
2. AI Agent node nhận request + truy vấn PostgreSQL Memory lấy conversation history (theo sessionId)
3. Agent gửi toàn bộ context (history + câu hỏi mới) cho Claude Opus 4.6 (LLM via Bedrock)
4. LLM phân tích ý định → có thể gọi **Think tool** trước để reasoning step-by-step
5. LLM quyết định tool(s) cần gọi: RAG (HTTP call tới Qdrant API), PostgreSQL (SQL query), HTTP APIs (live metrics)
6. Tool(s) trả về kết quả → LLM tổng hợp tất cả outputs → sinh câu trả lời
7. Respond to Webhook → trả JSON về cho client
8. Cặp Q&A mới được auto-append vào PostgreSQL Memory

**Luồng 2 — Data Ingestion (Indexing time):**
1. Webhook1 trigger → Read files from disk → Loop Over Items
2. Mỗi file: Extract text → Augment metadata (service_name, version, doc_type) → Chunking (token: 1024, overlap: 200)
3. Vector Store Processor (embedding bge-m3) → Aggregate thành batch → Upsert vào Qdrant
4. Sau khi hết file: mv files sang archived → Respond to Webhook1 (200 OK)

---

### Q: Data nào nằm ở đâu? Tại sao phải chia ra?

**A:**

| Nguồn | Chứa gì | Tại sao không gộp | Cách truy cập |
|-------|---------|-------------------|---------------|
| Qdrant (RAG) | Company info, team, policy, postmortem, architecture | Unstructured text, cần semantic + keyword search | HTTP tool → Hybrid Search API |
| PostgreSQL | monthly_costs, incidents, sla_targets, daily_metrics | Structured data, cần exact numbers, SQL aggregation | PostgreSQL tool (executeQuery) |
| Monitoring API | Live status, current latency, error rate, CPU | Real-time data, thay đổi liên tục, cần API call | HTTP tools (/services, /status, /metrics, /incidents) |

**Key insight:** Mỗi loại data có retrieval pattern khác nhau:
- RAG: semantic similarity → approximate matching → top-K chunks
- SQL: exact match → deterministic results → aggregation (SUM, AVG, GROUP BY)
- API: point-in-time snapshot → always fresh

Knowledge Base KHÔNG có con số cụ thể (dollar, latency ms). Nếu hỏi số liệu → phải dùng SQL/API tool.

---

### Q: LLM quyết định gọi tool nào dựa trên cái gì?

**A:** Dựa trên **tool description** trong system prompt + **Think tool** cho complex reasoning. Mỗi tool có mô tả rõ ràng:
- **RAG** (HTTP tool): "Search knowledge base for company information, policies, team structure, architecture, postmortems"
- **PostgreSQL**: "Query historical data — monthly costs, incident records, SLA targets, daily metrics"
- **HTTP /metrics**: "Get CURRENT live metrics — latency, error rate, request volume"
- **HTTP /status**: "Get current service status"
- **Think**: "Reasoning step — phân tích logic trước khi gọi tool khác"

**Cơ chế Function Calling:**
1. LLM nhận message + tool definitions (name, description, parameters schema)
2. LLM output structured JSON: `{"tool": "rag", "input": "PaymentGW architecture"}`
3. n8n parse JSON → route tới đúng tool node → execute → return result
4. LLM nhận result → quyết định tiếp (gọi tool khác hoặc synthesize answer)

Nếu câu hỏi cần nhiều nguồn (ví dụ: "Is PaymentGW meeting SLA?"), LLM sẽ gọi tuần tự: HTTP /metrics → PostgreSQL (SLA targets) → so sánh → trả lời.

---

### Q: Memory hoạt động như thế nào trong hệ thống?

**A:** Dùng **PostgreSQL Persistent Memory** (KHÔNG phải buffer window RAM):

**Cơ chế:**
1. Mỗi request mang theo `sessionId` → n8n query PostgreSQL lấy ALL messages có cùng sessionId
2. Toàn bộ history được inject vào context window cho LLM
3. LLM nhận: system prompt + conversation history + câu hỏi mới → sinh response
4. Cặp Q&A mới tự động append vào PostgreSQL với sessionId đó

**Tại sao PostgreSQL thay vì Window Buffer Memory (RAM)?**
- Window Buffer dễ bị reset khi n8n workflow restart
- RAM overflow với long conversation + RAG chunks lớn
- PostgreSQL: persistent, survive restart, queryable, scalable
- Có thể query history cho analytics/debugging

**Cách resolve pronoun ("its cost", "that service"):**
- LLM đọc lại history → biết "its" = service được nhắc ở turn trước
- Không cần NLP riêng, LLM tự resolve từ conversation context

---

## Category 2: RAG & Retrieval (Deep Dive)

### Q: RAG (Retrieval-Augmented Generation) hoạt động thế nào? Giải thích từng bước.

**A:** RAG = kỹ thuật bổ sung knowledge cho LLM bằng cách retrieve relevant documents trước khi generate.

**Tại sao cần RAG?** LLM có knowledge cutoff, không biết internal docs, hay hallucinate khi hỏi specific facts. RAG cho LLM "đọc tài liệu" trước khi trả lời.

**Pipeline của nhóm:**

```
[36 MD docs] → Augment Metadata → Chunking(1024 tokens, 200 overlap)
    → Embedding(bge-m3) → Upsert vào Qdrant (dense + sparse vectors)

[User query] → Embedding(bge-m3) + BM-25 tokenize
    → Hybrid Search (semantic + keyword) in Qdrant
    → Top-K chunks + metadata → LLM → Answer
```

**Từng thành phần:**
1. **Chunking**: Chia document dài thành đoạn nhỏ vừa context window
2. **Embedding**: Convert text → vector (mảng số) encode meaning
3. **Vector DB**: Lưu trữ + tìm kiếm vectors theo similarity
4. **Retrieval**: Tìm chunks liên quan nhất với query
5. **Generation**: LLM dùng retrieved chunks làm context để trả lời

---

### Q: Embedding là gì? bge-m3 khác gì Amazon Titan Embeddings?

**A:** 

**Embedding** = quá trình chuyển text thành vector (mảng floating-point numbers) sao cho text có nghĩa tương tự → vectors gần nhau trong không gian đa chiều.

```
"PaymentGW has high latency" → [0.12, -0.45, 0.88, ..., 0.33]  (1024 dimensions)
"Payment service is slow"    → [0.11, -0.43, 0.87, ..., 0.31]  (gần nhau!)
"Team Platform lead is Alex" → [0.78, 0.22, -0.15, ..., 0.67]  (xa nhau!)
```

**bge-m3 (BAAI General Embedding - Multi-lingual, Multi-granularity, Multi-functionality):**
- Output cả **dense vector** (semantic meaning) VÀ **sparse vector** (keyword matching)
- Hỗ trợ multilingual (tiếng Việt OK)
- 1024 dimensions
- Hiểu context tốt hơn Titan với technical terms

**Tại sao chọn bge-m3 thay vì Amazon Titan Embeddings v2?**
- Titan: chỉ dense vector, khó match exact keywords (mã lỗi, tên service)
- bge-m3: dense + sparse → kết hợp được với BM-25 cho Hybrid Search
- bge-m3 hiểu technical jargon tốt hơn (IT docs, error codes, service names)
- Self-hosted → không bị rate limit, low latency

---

### Q: Chunking là gì? Tại sao chunk_size=1024, overlap=200?

**A:**

**Chunking** = chia document dài thành đoạn nhỏ hơn vì:
- LLM context window có giới hạn (không thể nhét cả 36 docs)
- Embedding model có max token limit
- Chunks nhỏ hơn → retrieval chính xác hơn (ít noise)

**Các chiến lược chunking:**
| Strategy | Cách chia | Khi nào dùng |
|----------|----------|--------------|
| Fixed-size | Cứ mỗi N tokens cắt 1 lần | Simple, predictable |
| Sentence-based | Cắt theo câu/paragraph | Giữ nguyên ý nghĩa câu |
| Semantic | Dùng AI detect topic boundary | Tốt nhất nhưng chậm + đắt |
| Recursive | Thử separator lớn → nhỏ dần | LangChain default |

**Nhóm dùng Token-based (1024 tokens, 200 overlap):**
- **1024 tokens** (~750 words): đủ lớn để chứa 1 section hoàn chỉnh của MD doc (ví dụ: 1 postmortem section, 1 service description)
- **200 overlap** (20%): đảm bảo context không bị cắt đứt giữa chừng
  - Ví dụ: nếu chunk 1 kết thúc giữa câu "The root cause was..." → overlap giúp chunk 2 cũng có câu này

**Overlap hoạt động:**
```
Chunk 1: [token 0 -------- token 1024]
Chunk 2:            [token 824 -------- token 1848]  ← 200 tokens trùng
Chunk 3:                       [token 1648 -------- token 2672]
```

**Trade-off chunk size:**
- Quá nhỏ (256): mất context, nhiều chunks → retrieval chậm
- Quá lớn (2048): nhiều noise trong mỗi chunk, retrieval kém precise
- 1024 là sweet spot cho technical documentation

---

### Q: Hybrid Search là gì? Tại sao không chỉ dùng semantic search?

**A:**

**Semantic Search (Dense Retrieval):**
- Query → embedding → cosine similarity với stored vectors
- Ưu: hiểu meaning ("expensive" matches "high cost")
- Nhược: miss exact keywords (error code "INC-005", service name "PaymentGW")

**Keyword Search (Sparse Retrieval / BM-25):**
- BM-25 = Best Matching 25, thuật toán ranking dựa trên term frequency
- Tokenize query → match exact tokens trong documents → score by TF-IDF
- Ưu: exact match (tên service, mã lỗi, version numbers)
- Nhược: không hiểu synonyms ("slow" ≠ "high latency")

**Hybrid Search = Dense + Sparse kết hợp:**
```
Score_final = α × Score_semantic + (1-α) × Score_BM25
```
- Lấy top-K từ CẢ HAI phương pháp → merge + re-rank
- Reciprocal Rank Fusion (RRF) hoặc weighted combination

**Tại sao nhóm cần Hybrid Search:**
- IT docs chứa rất nhiều exact terms: "INC-005", "PaymentGW", "p99 latency", "HMAC-SHA256"
- Pure semantic search hay miss exact matches
- Pure BM-25 miss semantic ("what caused the outage" ≠ "root cause analysis")
- Hybrid = best of both worlds

**Implementation:** bge-m3 output cả dense + sparse vectors → Qdrant native Hybrid Search → wrap thành HTTP API → n8n Agent gọi qua HTTP tool.

---

### Q: Vector Database (Qdrant) hoạt động thế nào?

**A:**

**Vector Database** = database chuyên lưu trữ và search vectors (high-dimensional arrays).

**Qdrant specifics:**
- Lưu mỗi chunk dưới dạng: `{id, dense_vector[1024], sparse_vector, payload/metadata}`
- Payload = metadata: `{service_name, version, doc_type, filename, timestamp}`
- Search = tìm K vectors gần nhất với query vector (Approximate Nearest Neighbor - ANN)
- Dùng HNSW index (Hierarchical Navigable Small World) cho fast ANN search

**So sánh vs OpenSearch Serverless (Bedrock KB default):**
| | Qdrant | OpenSearch Serverless |
|--|--------|---------------------|
| Hybrid Search | Native support | Cần config phức tạp |
| Payload Filtering | Built-in, fast | Có nhưng chậm hơn |
| Self-hosted | Yes (Docker) | AWS managed only |
| Cost | Free (self-hosted) | Pay per OCU (~$700/month min) |
| Sparse vectors | Native | Limited |

**Payload Filtering:**
Khi search, có thể filter theo metadata TRƯỚC KHI tính similarity:
```json
{
  "query": "rate limit configuration",
  "filter": {"doc_type": "api_reference", "version": "v2"}
}
```
→ Chỉ search trong docs version 2, loại bỏ archived docs ngay từ đầu.

---

### Q: K (top-K) bao nhiêu là đủ? Tại sao?

**A:** Dùng K = 8-10 (thay vì default 3-5) vì:
- L2 yêu cầu tổng hợp từ NHIỀU documents (ví dụ: conflict giữa api_v1 và api_v2)
- K thấp → có thể miss document quan trọng
- K quá cao (>15) → nhiều noise, tốn context window, LLM có thể confused
- Hybrid Search đã lọc bớt noise → K cao hơn vẫn OK

**Context window budget:**
- Claude Opus 4.6: 200K tokens context
- 10 chunks × 1024 tokens = ~10K tokens cho RAG context
- Còn ~190K cho system prompt + memory + LLM reasoning
- → Rất thoải mái, không lo overflow

---

### Q: Khi 2 documents conflict (ví dụ rate limit 500 vs 1000), system xử lý thế nào?

**A:** Hệ thống có **multi-layer conflict resolution:**

**Layer 1 — Payload Filtering (tại retrieval time):**
- Metadata gán lúc ingestion: version, timestamp, status (active/archived)
- Qdrant filter: ưu tiên docs có `status: "active"`, `version: "latest"`
- Loại bớt conflict ngay từ đầu

**Layer 2 — System Prompt Hierarchy of Truth:**
```
Live HTTP APIs (absolute truth for real-time) 
  > PostgreSQL (historical aggregates) 
    > RAG (policies, architecture, intended state)
```

**Layer 3 — LLM Conflict Resolution (trong prompt):**
- Kiểm tra metadata: document nào marked "ARCHIVED" / "superseded_by"
- Ưu tiên document mới hơn (v2 > v1)
- **Show Evolution**: trình bày cả old + new value
- **Highlight Discrepancy**: nếu policy nói X nhưng live data nói Y → flag rõ

**Layer 4 — Jitter Rule:**
- Live metrics có ±5% jitter (random fluctuation)
- Minor differences (5%) → KHÔNG flag as contradiction
- Major differences (>10%) → flag + investigate

**Ví dụ thực tế:**
- RAG trả về: api_v1 (rate limit 500) + api_v2 (rate limit 1000)
- LLM: phân tích filename + metadata → v2 là mới hơn → answer: **1000** + note "was 500 in v1 (archived)"

---

## Category 3: Tool Use & Agent Reasoning (L3)

### Q: Khi nào system gọi Database tool vs RAG tool vs HTTP tool?

**A:** Agent quyết định dựa trên **intent classification** từ tool descriptions:

| Intent | Tool | Ví dụ câu hỏi |
|--------|------|---------------|
| Qualitative info (who, what, why, how) | RAG (Qdrant) | "Who leads Team Platform?", "Root cause of INC-005?", "Deployment policy?" |
| Exact numbers, aggregation | PostgreSQL | "PaymentGW Q1 cost?", "How many incidents in March?", "Most expensive service?" |
| Real-time state | HTTP APIs | "Current latency?", "Is service healthy NOW?" |
| Complex reasoning before action | Think | "Should we scale up?" (cần analyze multiple data points) |

**Multi-tool scenarios (phổ biến nhất):**
- "Is PaymentGW meeting SLA?" → HTTP /metrics (actual) + PostgreSQL (SLA target) + so sánh
- "Why did cost spike?" → PostgreSQL (cost data) + RAG (architecture docs, incident history)
- "Current status vs policy?" → HTTP /status (actual) + RAG (expected from policy)

---

### Q: Think tool là gì? Tại sao cần nó?

**A:** Think tool = một "scratchpad" cho LLM reasoning trước khi gọi tools khác.

**Cơ chế:** LLM gọi Think tool → viết ra suy luận step-by-step → KHÔNG trả cho user → LLM đọc lại reasoning → quyết định tools tiếp theo.

**Ví dụ:**
```
User: "Is NotificationSvc meeting its SLA?"
Think: "I need to: (1) get current metrics from HTTP API, (2) get SLA targets from DB, (3) compare actual vs target. Let me start with HTTP /metrics/NotificationSvc"
→ Call HTTP tool → Call PostgreSQL → Compare → Answer
```

**Tại sao cần:** Với câu hỏi phức tạp cần multi-step reasoning, nếu không có Think, LLM hay:
- Gọi sai tool trước
- Bỏ qua bước cần thiết
- Trả lời non trước khi có đủ data

Think = "dừng lại suy nghĩ" trước khi hành động → accurate tool selection.

---

### Q: Database schema có gì?

**A:** 4 tables:

| Table | Columns | Rows | Dùng khi |
|-------|---------|------|----------|
| monthly_costs | service, month, compute_cost, storage_cost, network_cost, third_party_cost, total_cost | 36 (6 services x 6 months) | Hỏi chi phí |
| incidents | id, service, severity, date, duration_minutes, description | ~10 incidents | Hỏi sự cố lịch sử |
| sla_targets | service, metric, target_value | ~18 (6 services x 3 metrics) | Hỏi SLA targets |
| daily_metrics | service, date, latency_p99, error_rate, requests_per_min | ~540 (6 services x 90 days) | Hỏi trends, so sánh |

**LLM sinh SQL thế nào?** Tool description chứa schema info → LLM generate SQL → PostgreSQL tool execute → return results. Ví dụ:
```sql
SELECT service, SUM(total_cost) as q1_total
FROM monthly_costs 
WHERE month IN ('2026-01', '2026-02', '2026-03')
GROUP BY service ORDER BY q1_total DESC;
```

---

### Q: Monitoring API có những endpoints nào?

**A:**

| Endpoint | Trả về | Khi nào gọi |
|----------|--------|-------------|
| GET /services | Danh sách tất cả services | "What services exist?" |
| GET /status/{service} | Current status (healthy/degraded/down) | "Is X up?" |
| GET /metrics/{service} | Live latency, error rate, requests/min, CPU, memory | "Current performance of X?" |
| GET /incidents | Recent incidents list | "Any ongoing incidents?" |
| GET /incidents/{service} | Incidents của 1 service cụ thể | "Recent issues with X?" |

**Tại sao HTTP tools thay vì SQL trực tiếp cho monitoring data?**
- Ban đầu thử cấp SQL tool trực tiếp cho monitoring DB → Agent sinh query sai logic, timeout, tốn token
- HTTP API = pre-defined, safe, standardized JSON response
- Agent không thể chạy dangerous queries (DROP TABLE, etc.)
- Response format consistent → LLM parse dễ hơn

---

### Q: Nếu LLM gọi sai tool (ví dụ dùng RAG cho câu hỏi cần số liệu), chuyện gì xảy ra?

**A:** RAG sẽ trả về text nói "costs have been rising" nhưng KHÔNG có con số cụ thể.

**Possible outcomes:**
1. ❌ Hallucinate một con số (worst case)
2. ✅ Nhận ra thiếu data → gọi thêm database tool (self-correction)
3. ⚠️ Trả lời "I don't have exact numbers" (acceptable but suboptimal)

**Mitigation strategies nhóm áp dụng:**
- Tool description cực rõ ràng: "for EXACT NUMBERS, ALWAYS use database tool"
- Think tool: LLM suy nghĩ trước → chọn tool chính xác hơn
- System prompt: "NEVER guess numbers. If you need quantitative data, use PostgreSQL or HTTP tool"
- Prompt hierarchy: nếu LLM detect missing data từ tool A → PHẢI gọi tool B trước khi trả lời

---

### Q: Function Calling / Tool Calling hoạt động thế nào ở mức kỹ thuật?

**A:**

**Khái niệm:** LLM không thực sự "chạy code". Nó output structured text nói "tôi muốn gọi tool X với input Y" → orchestrator (n8n) parse → execute → return result.

**Flow chi tiết:**
```
1. System prompt chứa tool definitions:
   tools: [
     {name: "rag", description: "...", parameters: {query: string}},
     {name: "postgresql", description: "...", parameters: {sql: string}},
     {name: "http_metrics", description: "...", parameters: {service: string}}
   ]

2. LLM nhận user message → decide cần tool → output:
   {"tool_calls": [{"name": "postgresql", "arguments": {"sql": "SELECT ..."}}]}

3. n8n parse tool_call → route tới PostgreSQL node → execute SQL → get result

4. Result inject vào conversation: "Tool result: [{service: PaymentGW, total: 16500}]"

5. LLM nhận result → decide: đủ data → synthesize answer
                            → thiếu data → gọi thêm tool khác (loop)
```

**ReAct Pattern (Reasoning + Acting):**
Agent hoạt động theo loop: Thought → Action → Observation → Thought → ... → Final Answer
- **Thought**: LLM suy nghĩ cần gì (Think tool)
- **Action**: gọi tool
- **Observation**: nhận kết quả
- Lặp lại cho đến khi đủ info → Final Answer

---

## Category 4: Specific Technical Questions

### Q: Tại sao dùng Claude qua Bedrock thay vì gọi Anthropic API trực tiếp?

**A:**
- Bedrock managed service — không cần manage API keys riêng
- Tích hợp sẵn với AWS ecosystem (IAM, CloudWatch, VPC)
- Pricing pay-per-token, không cần commit
- Compliance: data không rời AWS region
- Native integration với n8n (có sẵn Bedrock Chat Model node)
- Không bị rate limit nghiêm ngặt như direct API

**Trade-off:** Bedrock version thường chậm hơn 1-2 model versions so với Anthropic direct. Nhưng cho enterprise use case, security + compliance > bleeding edge.

---

### Q: Chat UI kết nối với n8n bằng cách nào?

**A:**
- n8n expose một **Webhook endpoint** (POST)
- Chat UI gửi `{ chatInput: "question", sessionId: "unique_id" }` via fetch()
- sessionId dùng để n8n track conversation memory trong PostgreSQL
- n8n xử lý xong → Respond to Webhook node trả JSON về
- Chat UI parse response, hiển thị answer với simulated streaming (typewriter effect)

---

### Q: Pipeline Trace / Observability Dashboard hiển thị những gì?

**A:** Dashboard hiện toàn bộ pipeline internals (Bonus A):
1. **Retrieval step** — RAG search results, chunks retrieved
2. **Tool calls** — Tool nào được gọi + input gì + output
3. **LLM decision** — Agent thought process (tại sao chọn tool)
4. **Latency từng bước** — Thời gian mỗi step (embedding, retrieval, LLM, tools)
5. **Token count** — Tokens consumed per step

Giúp debug khi answer sai: xem retrieval có đúng không, tool có được gọi không, LLM reasoning có hợp lý không.

---

### Q: Streaming response hoạt động thế nào?

**A:** n8n trả full response 1 lần (không phải true streaming). Chat UI simulate streaming bằng:
- Nhận full text từ webhook response
- Hiển thị word-by-word với delay ~28ms/word (typewriter effect)
- Hiện blinking cursor trong lúc streaming
- Sau khi xong → render full markdown formatting

**True streaming vs Simulated:**
| | True Streaming (SSE) | Simulated (nhóm dùng) |
|--|---------------------|----------------------|
| Time to first token | ~500ms | Full response time (5-30s) |
| UX | Token hiện dần, feel real-time | User chờ lâu rồi thấy type nhanh |
| Complexity | Server-Sent Events, chunked response | Simple POST → full response |
| n8n support | Không native | Works perfectly |

---

## Category 5: Problem Solving & Edge Cases

### Q: Nếu n8n server không phản hồi thì sao?

**A:** Chat UI có:
- Timeout 3 phút (AbortController)
- Timer hiển thị thời gian chờ (0s, 1s, 2s...)
- Error message thân thiện nếu timeout hoặc network error
- User có thể gửi lại câu hỏi

---

### Q: Làm sao đảm bảo LLM không hallucinate số liệu?

**A:** Multi-layer anti-hallucination:

1. **System prompt constraint**: "NEVER guess numbers. If you need exact data, use the database or API tool."
2. **Data separation**: RAG chunks KHÔNG chứa số liệu cụ thể → LLM buộc phải gọi tool
3. **Tool description clarity**: mô tả rõ data nào ở đâu
4. **Citation requirement**: response phải cite source ("Based on database query..." / "According to live metrics...")
5. **Think tool**: reasoning trước khi answer → nhận ra cần data → gọi tool

**Hallucination xảy ra khi:** LLM "tự tin" trả lời dựa trên training data thay vì retrieved context. Giải pháp: force LLM luôn ground answer trên tool results.

---

### Q: Câu hỏi nào khó nhất cho system? Tại sao?

**A:** Câu hỏi multi-step reasoning cần nhiều tools + logic:

**Ví dụ 1:** "Is NotificationSvc meeting its SLA targets?"
1. Think: cần actual metrics + SLA targets + comparison
2. HTTP /metrics/NotificationSvc → current latency, error rate
3. PostgreSQL → SLA targets (latency < 200ms, error < 1%)
4. Compare: actual 250ms > target 200ms → BREACHING
5. Synthesize: "NotificationSvc is BREACHING latency SLA (250ms vs 200ms target)"

**Ví dụ 2:** L4 multi-turn: "Why did its costs spike?"
- Cần resolve "its" = service từ turn trước (pronoun resolution via memory)
- Cần PostgreSQL: cost trend over months
- Cần RAG: architecture changes, incidents that caused spike
- Multi-source synthesis

**Ví dụ 3:** Conflict resolution: "What's the rate limit?"
- RAG returns 2 docs (v1: 500, v2: 1000)
- Agent phải: check metadata → prioritize v2 → explain evolution

---

### Q: Nếu có thêm 1 tuần, sẽ cải thiện gì?

**A:**
- True streaming (server-sent events từ n8n) — giảm perceived latency
- Auto-sync KB khi documents thay đổi (file watcher → re-ingest → re-embed)
- Query caching (Redis) cho frequent questions → sub-second response
- Confidence scoring — LLM rate 1-5 confidence, flag low-confidence answers
- Feedback loop — user thumbs up/down → fine-tune prompts
- Re-ranking model (cross-encoder) sau retrieval, trước LLM → better precision
- Chunk summarization — mỗi chunk kèm 1-line summary để LLM scan nhanh hơn

---

## Category 6: AWS & Cloud Specifics

### Q: Qdrant đóng vai trò gì? So sánh với OpenSearch Serverless?

**A:** Qdrant là vector database chính cho RAG:
- Lưu trữ dense vectors (bge-m3, 1024 dims) + sparse vectors (BM-25) cho mỗi chunk
- Native Hybrid Search: dense + sparse trong 1 query
- Payload filtering: filter theo metadata trước khi search → fast + precise
- Self-hosted (Docker) → full control, no cost per query
- REST API → dễ integrate với n8n qua HTTP tool

**So với OpenSearch Serverless (Bedrock KB default):**
- OpenSearch: AWS managed, min ~$700/month, limited sparse vector support
- Qdrant: self-hosted free, native hybrid search, payload schema flexible
- Trade-off: Qdrant cần self-manage (Docker, backup), OpenSearch fully managed

---

### Q: Tại sao dùng PostgreSQL cho CẢ structured data VÀ memory?

**A:** PostgreSQL đóng 2 vai trò:

**Vai trò 1 — Structured data store:**
- Data có quan hệ: costs per service per month, SLA per service per metric
- Cần SQL aggregation: SUM, AVG, GROUP BY, JOIN
- LLM sinh SQL dễ hơn DynamoDB query expressions
- Ad-hoc queries: bất kỳ câu hỏi nào cũng generate được SQL

**Vai trò 2 — Persistent conversation memory:**
- Lưu `session_id` + `message` (chat history)
- Survive n8n restart (vs RAM buffer memory bị mất)
- Queryable: có thể analytics on conversations
- n8n có native PostgreSQL Chat Memory node

**Tại sao không DynamoDB?**
- DynamoDB single-table design phức tạp cho ad-hoc queries
- Không có SQL → LLM phải sinh DynamoDB expressions (harder, more error-prone)
- Trade-off: PostgreSQL cần manage instance, nhưng query flexibility quan trọng hơn

---

### Q: CloudFront dùng để làm gì trong project này?

**A:**
- Serve Chat UI (chat_ui.html) từ S3 qua CloudFront CDN
- Giảm latency cho user (edge locations)
- HTTPS by default
- Cache static assets
- Custom domain nếu cần

---

### Q: Security considerations?

**A:**
- n8n webhook endpoint: có thể thêm API key header để authenticate
- Bedrock: IAM role-based access, data stays in AWS region
- PostgreSQL: trong private subnet, chỉ n8n access được
- HTTP tools: trỏ tới internal IP (192.168.31.x) → không expose ra internet
- Agent không có quyền DROP/DELETE trên DB (HTTP tool = read-only interface)
- Chat UI: static hosting, không chứa credentials (webhook URL là public endpoint)
- CORS configured trên n8n cho phép Chat UI domain
- Qdrant: internal network only, không public access

---

## Category 7: AI/ML Deep Knowledge (Bonus Questions)

### Q: Cosine Similarity vs Euclidean Distance — khác gì? Khi nào dùng cái nào?

**A:**

**Cosine Similarity:** đo góc giữa 2 vectors (bỏ qua magnitude)
```
cos(A, B) = (A · B) / (|A| × |B|)
Range: [-1, 1], 1 = giống nhất
```
- Ưu: robust với vectors có length khác nhau
- Dùng khi: text embeddings (document dài vs ngắn vẫn so sánh fair)

**Euclidean Distance:** đo khoảng cách thực trong không gian
```
d(A, B) = √(Σ(ai - bi)²)
Range: [0, ∞], 0 = giống nhất
```
- Ưu: đơn giản, trực quan
- Dùng khi: vectors đã normalized (cùng magnitude)

**Nhóm dùng Cosine Similarity** vì bge-m3 embeddings normalized → cosine ≈ dot product, standard cho text search.

---

### Q: ANN (Approximate Nearest Neighbor) là gì? HNSW hoạt động thế nào?

**A:**

**Vấn đề:** Với 10,000 chunks, mỗi chunk 1024 dims → exact search phải so sánh query với TẤT CẢ vectors → O(n) rất chậm.

**ANN:** Trade accuracy lấy speed. Chấp nhận miss 5% relevant results để search nhanh hơn 100x.

**HNSW (Hierarchical Navigable Small World):**
- Xây dựng graph multi-layer: layer cao = sparse (few nodes), layer thấp = dense (all nodes)
- Search: bắt đầu từ layer cao → nhảy xuống layer thấp dần → "zoom in" vào vùng gần query
- Giống GPS: zoom từ world → country → city → street
- Complexity: O(log n) thay vì O(n)
- Qdrant dùng HNSW làm default index

---

### Q: Token là gì? Tokenization hoạt động thế nào?

**A:**

**Token** = đơn vị nhỏ nhất LLM xử lý. KHÔNG phải word, KHÔNG phải character.

**Tokenization:** text → chuỗi tokens (subword units)
```
"PaymentGateway" → ["Payment", "Gate", "way"]     (3 tokens)
"unhappiness"    → ["un", "happiness"]              (2 tokens)  
"Hello world"    → ["Hello", " world"]              (2 tokens, kể cả space)
```

**Tại sao quan trọng:**
- LLM context window tính bằng tokens (Claude: 200K tokens)
- Chunking cắt theo tokens (1024 tokens/chunk)
- Cost tính per token (input + output)
- 1 token ≈ 0.75 English words ≈ 4 characters

**BPE (Byte-Pair Encoding):** thuật toán tokenization phổ biến nhất
- Training: tìm cặp bytes xuất hiện nhiều nhất → merge thành 1 token → lặp lại
- Kết quả: common words = 1 token, rare words = nhiều tokens

---

### Q: Temperature, Top-P, Top-K trong LLM generation là gì?

**A:** Các tham số control "creativity" của LLM output:

**Temperature (0.0 - 1.0+):**
- Thấp (0.0-0.3): deterministic, factual, consistent → dùng cho RAG answer
- Cao (0.7-1.0): creative, diverse, unpredictable → dùng cho brainstorming
- Nhóm dùng: low temperature vì cần factual accuracy

**Top-K:** Chỉ chọn từ K tokens có probability cao nhất
- K=1: always chọn token likely nhất (= temperature 0)
- K=50: chọn random từ top 50 candidates

**Top-P (nucleus sampling):** Chọn từ smallest set of tokens có cumulative probability ≥ P
- P=0.9: chọn tokens cho đến khi tổng prob = 90%
- Dynamic: nếu 1 token chiếm 95% → chỉ chọn token đó

---

### Q: Prompt Engineering trong system prompt quan trọng thế nào?

**A:** System prompt là "bộ não" controlling toàn bộ Agent behavior:

**Nhóm implement trong system prompt:**
1. **Role definition**: "You are a GeekBrain infrastructure assistant..."
2. **Tool selection rules**: "For exact numbers → use PostgreSQL, for policies → use RAG"
3. **Conflict resolution hierarchy**: Live API > PostgreSQL > RAG
4. **Anti-hallucination**: "NEVER guess numbers"
5. **Show Evolution**: "Present both old and new data"
6. **Jitter Rule**: "±5% fluctuation is normal, don't flag"
7. **Citation requirement**: "Always cite data source"

**Tại sao prompt engineering > fine-tuning cho use case này:**
- Fine-tuning cần data + compute + time
- Prompt engineering: iterate ngay, zero cost, easy to A/B test
- RAG + tools đã cung cấp knowledge → prompt chỉ cần define behavior
- Claude Opus 4.6 instruction-following rất tốt → prompt enough

---

### Q: Data Ingestion Pipeline — Augment Metadata bước này làm gì?

**A:** Trước khi chunking, mỗi file được gán thêm metadata:

```json
{
  "service_name": "PaymentGW",       // Từ filename hoặc content analysis
  "doc_type": "postmortem",           // postmortem, api_reference, policy, team...
  "version": "v2",                    // Nếu có versioning
  "filename": "postmortem_INC005_paymentgw_mar.md",
  "timestamp": "2026-03-15",
  "status": "active"                  // active vs archived
}
```

**Tại sao cần augment TRƯỚC chunking?**
- Sau khi chunk, mỗi chunk mất context "nó thuộc doc nào"
- Metadata gán vào TỪNG chunk → khi retrieve, biết chunk từ đâu
- Enable payload filtering: "chỉ search trong postmortems" hoặc "chỉ version v2"
- Agent có thể: "tìm tất cả docs về PaymentGW" → filter service_name = "PaymentGW"

---

### Q: Giải thích Upsert — tại sao không chỉ Insert?

**A:**

**Insert:** thêm mới. Nếu document đã tồn tại → duplicate!
**Upsert:** Insert nếu chưa có, Update nếu đã có (based on ID).

**Tại sao cần Upsert cho RAG pipeline:**
- Docs thay đổi thường xuyên (policy update, new version)
- Re-run pipeline: nếu chỉ Insert → duplicate chunks trong Qdrant → search trả duplicate results
- Upsert: mỗi chunk có unique ID (hash of filename + chunk_index) → re-run = update in place
- Idempotent: chạy pipeline bao nhiêu lần cũng cho kết quả giống nhau

---

## Quick Reference — Key Facts

| Topic | Answer |
|-------|--------|
| PaymentGW rate limit | 1000 req/min (v2), was 500 (v1 archived) |
| Team Platform lead | Alex Chen |
| PaymentGW March incident | Circuit breaker stuck OPEN due to misconfigured health check |
| Deployment freeze | Friday 18:00 - Monday 08:00 |
| PaymentGW auth | API key + HMAC-SHA256 signature |
| NotificationSvc queue | Amazon SQS |
| AuthSvc language | Go |
| JWT rotation | Every 30 days |
| P1 escalation | On-call → Alex Chen (15min) → Mark Sullivan VP (30min) → James Wright CTO (1hr) |
| LLM model used | Claude Opus 4.6 (via Amazon Bedrock) |
| Embedding model | bge-m3 (dense + sparse vectors) |
| Keyword search | BM-25 (sparse retrieval) |
| Vector store | Qdrant (self-hosted, Docker) |
| Search method | Hybrid Search (semantic + keyword) |
| Chunk size | 1024 tokens, 200 overlap |
| Memory | PostgreSQL persistent (session-based) |
| Orchestration | n8n (low-code workflow) + LangChain (RAG backend) |
| Conflict resolution | Live API > PostgreSQL > RAG |
