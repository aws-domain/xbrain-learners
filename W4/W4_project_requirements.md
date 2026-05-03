# Yêu cầu Project W4 — Build an AI That Actually Answers

> Deadline: **Thứ Sáu 08/05/2026** — post commit link `docs/W4_evidence.md` lên Slack trước slot trình bày
> Presentation: **Thứ Sáu 14:00–18:00** (~10-12 phút/nhóm)

---

## Fix W3 trước (bắt buộc trước khi thêm W4)

- [ ] Evidence Pack `docs/W3_evidence.md` đã commit và post link lên Slack chưa?
- [ ] Lambda execution role không có wildcard — đã verify chưa?
- [ ] S3 Gateway Endpoint đã có trên route table và diagram chưa?
- [ ] Data Access Pattern Log Part C (wrong-paradigm test) đã đủ chưa?
- [ ] CloudWatch Logs sau S3 trigger đã capture chưa?

---

## Bức tranh tổng thể

Bạn xây một AI system trả lời câu hỏi về **GeekBrain** — một fintech startup chạy 6 production services. Hệ thống phải trả lời được 4 cấp độ câu hỏi, mỗi cấp yêu cầu một capability mới.

**3 nguồn dữ liệu — phải hiểu rõ cái gì nằm ở đâu:**

| Nguồn | Chứa gì | Truy cập bằng cách nào |
|-------|---------|----------------------|
| Knowledge Base (36 markdown docs) | Thông tin công ty, team, policy, postmortem, architecture | RAG retrieval (vector search) |
| Database (4 CSV files đã seed) | Exact costs, incidents, SLA targets, daily metrics | SQL query qua tool function |
| Monitoring API (Python script chạy local) | Current live status, latency, error rate, request volume | HTTP call qua tool function |

> **Key insight:** Knowledge Base không có số tiền, không có daily metrics, không có live system state. Câu hỏi nào hỏi số liệu hoặc trạng thái hiện tại → chỉ tools mới trả lời được.

---

## 4 Levels (Cumulative — không được bỏ qua)

### L1 — Simple RAG (2.0 điểm)

**Yêu cầu:** Trả lời câu hỏi đơn giản từ 1 document, có cite source.

Checklist:
- [ ] Upload 36 markdown docs lên S3 bucket
- [ ] Tạo Bedrock Knowledge Base, chọn embedding model (Amazon Titan Embeddings v2), sync hoàn tất
- [ ] Gọi `Retrieve` API — verify trả về đúng chunks
- [ ] Kết nối với LLM (Claude Sonnet via Bedrock) với system prompt yêu cầu cite source document
- [ ] Pass condition: trả lời đúng + nêu tên source document

Test questions:
- "Who is the Team Platform lead?" → "Alex Chen" (from `team_platform.md`)
- "What is the deployment freeze window?" → "Friday 18:00 to Monday 08:00" (from `deployment_policy.md`)
- "What authentication method does PaymentGW use?" → "API key + HMAC-SHA256" (from `api_reference_v2.md`)

---

### L2 — Multi-Source Retrieval (3.0 điểm)

**Yêu cầu:** Tổng hợp từ nhiều documents, xử lý conflict giữa các documents.

Checklist:
- [ ] Tăng retrieval K lên 8–10 chunks
- [ ] Cập nhật system prompt: ưu tiên document mới hơn khi có conflict, giải thích discrepancy
- [ ] Pass condition: resolve đúng conflict rate limit (v1: 500 req/min vs v2: 1000 req/min → chọn v2)

Test questions:
- "What is PaymentGW's API rate limit?" → 1000 (v2), acknowledge v1 said 500
- "Can Team Commerce deploy a fix on Friday night for a P1 bug?" → tổng hợp `deployment_policy.md` + `incident_response_policy.md` + team info
- "What lessons were common across March 2026 incidents?" → tổng hợp 2 postmortems

---

### L3 — Tool-Augmented RAG (4.0 điểm)

**Yêu cầu:** Gọi external tools để lấy dữ liệu không có trong document. Đây là level quan trọng nhất.

Checklist:
- [ ] Seed database: `python seed_data.py` → verify `SELECT COUNT(*) FROM monthly_costs` = 36 rows
- [ ] Start monitoring API: `uvicorn monitoring_api:app --port 8000` → test tất cả endpoints
- [ ] Build Tool 1 — Database Query (SQL → rows)
- [ ] Build Tool 2 — Service Metrics (GET `/metrics/{service_name}` → JSON)
- [ ] Register tools với LLM (Bedrock Agents / framework / raw function calling)
- [ ] Pass condition: trả lời đúng số liệu từ DB/API — **không phải guess**

Tool descriptions phải rõ ràng:
```
Database Query: Execute read-only SQL. Contains monthly_costs, incidents,
sla_targets, daily_metrics. Use for HISTORICAL data.

Service Metrics: Get CURRENT live metrics (latency, error rate, requests/min).
Use for live/current data only.
```

Test questions:
- "What was PaymentGW's total infrastructure cost in Q1 2026?" → $16,500 (từ DB)
- "What is PaymentGW's current p99 latency?" → ~185ms (từ API)
- "Is NotificationSvc meeting its SLA targets?" → gọi cả 2 tools → latency 3200ms vs target 2000ms, error 2.1% vs target 1.0% → No

---

### L4 — Memory / Multi-Turn (1.0 điểm)

**Yêu cầu:** Conversation nhiều lượt, follow-up questions resolve được pronoun từ lượt trước.

Checklist:
- [ ] Implement memory strategy (buffer / window / query rewriting)
- [ ] Pass condition: 3–4 lượt conversation, "its", "that service", "their team" được resolve đúng

Test conversation:
- Turn 1: "Which service had the highest cost in March?" → PaymentGW ($7,500)
- Turn 2: "Why did its costs spike?" → resolve "its" = PaymentGW → retrieve postmortem
- Turn 3: "Which team is responsible?" → Team Platform, Alex Chen
- Turn 4: "The postmortem mentioned a review deadline. Is it overdue?" → so sánh với ngày hiện tại

Memory strategies:

| Strategy | Cách làm | Phù hợp khi |
|----------|----------|-------------|
| Buffer | Lưu tất cả, gửi tất cả | Demo ngắn (<10 turns) |
| Window | Lưu tất cả, gửi 5 turns gần nhất | Context có giới hạn |
| Query rewriting | Rewrite câu hỏi thành self-contained trước khi retrieve | Cần retrieval chính xác hơn |

---

## Tools cần implement

| Tool | Chức năng |
|------|-----------|
| Service Status | Current live status của 1 service |
| Service Metrics | Current performance metrics (latency, error rate, req/min) |
| List Services | Danh sách tất cả services |
| Incident History | Lịch sử incidents của 1 service |
| Team Info | Thông tin về 1 team |
| Compare Services | So sánh 1 metric giữa nhiều services |
| Database Query | Query structured data (costs, SLAs, daily metrics) |

---

## Bonus (tùy chọn — chỉ tính nếu L1–L3 đã hoàn chỉnh)

| Bonus | Credit | Yêu cầu |
|-------|--------|---------|
| **Bonus A — Observability Dashboard** | +0.5 | UI hiển thị pipeline internals: chunks retrieved, tool called, LLM input/output |
| **Bonus B — Agent Reasoning** | +0.5 | Multi-step investigation với structured output và visible reasoning steps |
| **Bonus C — KB Auto-Sync** | +0.5 | S3 event → Lambda → `StartIngestionJob` khi document thay đổi |

Maximum bonus: +1.0 (A hoặc B = +0.5, C = +0.5 riêng). Score tối đa: 11.0.

---

## Evidence Pack — `docs/W4_evidence.md` (20% điểm)

File markdown trong group repo. Slides thứ Sáu = lấy screenshots từ file này.

| Section | Nội dung |
|---------|----------|
| 1. Cover | Số nhóm, tên thành viên, LLM dùng, framework dùng, link repo |
| 2. Architecture Overview | Diagram hệ thống + component list + data flow + screenshot app đang chạy |
| 3. Decision Log | 3 quyết định key + ít nhất 1 thứ không work và đã xử lý thế nào |
| 4. Per-Level Evidence | Mỗi level: screenshot đáp án đúng + proof pipeline đã xử lý (log/dashboard) |
| 5. Reflection | Level khó nhất và lý do. Nếu có thêm 1 ngày sẽ làm gì khác |

**Proof yêu cầu cho từng level:**

- **L1:** Log showing Bedrock Retrieve call trả về chunks
- **L2:** Screenshot conflict resolution (rate limit → 1000, not 500)
- **L3:** Log showing tool được gọi và trả về real data — **đây là proof quan trọng nhất**
- **L4:** Screenshot 3–4 turn conversation với pronoun resolution

**Nếu dùng AgentCore:** Diagram phân biệt AgentCore manages gì vs bạn build gì + annotated trace logs cho 2 câu hỏi (1 RAG-only, 1 tool-augmented).

**Thang điểm Evidence Pack:**

| Nộp gì | Score tối đa |
|--------|-------------|
| Không có Evidence Pack | Cap 2/5 |
| Có screenshot nhưng không có logs/proof | Cap 3/5 |
| Screenshot + logs + notes + decision log | 4/5 |
| Đầy đủ, rõ ràng, có tổ chức | 5/5 |

> **Post commit link lên Slack trước slot trình bày. Không post = tự động cap evidence score ở 2.**

---

## Rubric W4

| Criterion | Weight |
|-----------|--------|
| L1 — Retrieval | 2.0 điểm |
| L2 — Multi-Source Retrieval | 3.0 điểm |
| L3 — Retrieval + Tools | 4.0 điểm |
| L4 — Memory | 1.0 điểm |
| **Total** | **10.0 điểm** |

**Presentation breakdown:**

| Component | Weight |
|-----------|--------|
| Live Demo (L1–L4) | 50% |
| Individual QnA | 30% |
| Architecture & Evidence Pack | 20% |

---

## Lịch build tối ưu

### Thứ Ba — Explore data (không code)
1. Đọc tất cả 36 documents trong `knowledge_base/` — note conflicts, note gaps
2. Start monitoring API: `uvicorn monitoring_api:app --port 8000` → hit mọi endpoint
3. Seed database: `python seed_data.py` → query verify data
4. Vẽ architecture trên giấy trước khi code

### Thứ Năm sáng — L1 (target: xong trước 12:00)
1. Upload docs lên S3
2. Tạo Bedrock KB, sync, verify
3. Test retrieval → kết nối LLM → verify 3 test questions

### Thứ Năm chiều — L2 → L3
- 13:00–15:00: Tăng K, cải thiện system prompt, test conflict resolution → L2 done
- 15:00–17:00: Build 2 tool functions, register với LLM, test first tool call → L3 started

### Thứ Sáu sáng — Polish + Evidence
- 08:00–10:00: Finalize L3, test all questions, add L4 nếu còn thời gian
- 10:00–12:00: Viết Evidence Pack, chụp screenshots, chuẩn bị slides

---

## Common Mistakes — Tránh những lỗi này

1. **Không đọc docs trước khi code** — sẽ build conflict resolution mà không biết docs nào conflict
2. **Nhảy thẳng vào L3 khi L1 chưa xong** — nếu retrieval broken thì tools vô nghĩa
3. **Không start monitoring API** — nhóm nào chỉ build document retrieval sẽ fail L3 hoàn toàn
4. **Tool description quá mơ hồ** — LLM đọc description để quyết định gọi tool nào
5. **Không test với số thực** — L3 chấm điểm dựa trên numerical accuracy
6. **Không chụp screenshot trong lúc build** — đừng để đến sáng thứ Sáu mới chụp
