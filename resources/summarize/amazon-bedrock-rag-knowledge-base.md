# Amazon Bedrock — RAG và Knowledge Base: Kiến Thức Thực Hành

## 1. RAG Pipeline Tổng Quan

RAG (Retrieval-Augmented Generation) là pattern kết hợp **tìm kiếm** và **sinh văn bản**:

```
User Question
    ↓
[1] Embed query → vector
    ↓
[2] Cosine similarity search trong Vector Store
    ↓ (trả về top-K chunks liên quan)
[3] Construct prompt: system + context + question
    ↓
[4] Invoke LLM (Claude) → generate answer
    ↓
Answer
```

**Tại sao cần RAG thay vì hỏi LLM trực tiếp?**
- LLM chỉ biết thông tin đến training cutoff — không biết dữ liệu nội bộ/mới
- RAG inject dữ liệu thực tế vào prompt → giảm hallucination
- Không cần fine-tune model khi dữ liệu thay đổi

---

## 2. Kiến Trúc Knowledge Base trên Bedrock

### Luồng Ingestion (lúc setup)

```
S3 Bucket (markdown/PDF/txt)
    ↓ Sync
[Bedrock KB] Chunking → Embedding model → Vector Store (OpenSearch)
                                              ↑
                                    224 documents = 224 chunks
```

### Luồng Query (lúc runtime)

```
Query text → Embedding model → vector → Cosine similarity search
                                              ↓
                                    Top-K chunks + score
```

---

## 3. Chunking Strategy

### Cách tính số chunks

```
Số chunks = ceil((doc_length - chunk_size) / step) + 1

Trong đó:
  step = chunk_size × (1 - overlap_percent)
```

**Ví dụ thực tế:**
- 36 documents, mỗi doc ~1100 words
- Chunk size: 300 tokens, Overlap: 20%
- 1 token ≈ 0.75 words → 1100 words ≈ 1467 tokens/doc
- step = 300 × 0.8 = 240 tokens
- chunks/doc = ceil((1467 - 300) / 240) + 1 ≈ 6 chunks
- Tổng: 36 × 6 ≈ **216 chunks** (thực tế ra 224)

### Tại sao cần overlap?
- Thông tin quan trọng có thể nằm ở ranh giới giữa 2 chunks
- Overlap 20% đảm bảo context không bị cắt đứt

### Các strategy có sẵn trong Bedrock
| Strategy | Mô tả | Dùng khi |
|----------|-------|---------|
| Default chunking | Tự động theo token count | Văn bản thông thường |
| Fixed-size chunking | Cố định số tokens | Cần kiểm soát kích thước |
| No chunking | 1 document = 1 chunk | Document ngắn, cần toàn bộ context |
| Hierarchical chunking | Chunk lớn chứa chunk nhỏ | Document có cấu trúc rõ ràng |
| Semantic chunking | Chia theo ý nghĩa | Cần ngữ nghĩa chính xác |

---

## 4. Embedding Models

Embedding model chuyển text → vector số học để tính similarity.

### So sánh Titan vs Cohere

| | Titan Embeddings G1 v1.2 | Cohere Embed |
|--|--------------------------|-------------|
| **Giá** | $0.00002/1K tokens | $0.00010/1K tokens |
| **Dimensions** | 1024 | 1024 |
| **Ngôn ngữ** | English | 100+ ngôn ngữ |
| **Tích hợp AWS** | Native, IAM tự động | Third-party |
| **Dùng khi** | English, tiết kiệm chi phí | Multilingual, precision cao |

**Lưu ý quan trọng:** Embedding model không thể thay đổi sau khi tạo KB — phải tạo lại KB nếu muốn đổi model.

---

## 5. Vector Store Options

| Vector Store | Đặc điểm | Dùng khi |
|-------------|----------|---------|
| **OpenSearch Serverless** | Hybrid search (vector + keyword), mặc định | Hầu hết use cases, lab/demo |
| **Amazon S3 Vectors** | Lưu trữ lớn, chi phí thấp | Dataset lớn, ít query |
| **Aurora PostgreSQL** | Kết hợp SQL + vector search | Cần join với relational data |
| **Neptune Analytics** | Graph-based RAG | Dữ liệu dạng knowledge graph |

**OpenSearch Serverless** là lựa chọn mặc định và phù hợp nhất cho hầu hết trường hợp.

---

## 6. Hai Bedrock Clients và Tại Sao Khác Nhau

```python
import boto3

# Client 1: cho Knowledge Base operations
bedrock_agent_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
# Dùng cho: retrieve(), retrieve_and_generate()

# Client 2: cho model invocation
bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='us-east-1')
# Dùng cho: invoke_model(), converse()
```

**Tại sao tách riêng?**
- `bedrock-agent-runtime`: Quản lý KB, Agent, memory — stateful operations
- `bedrock-runtime`: Gọi model trực tiếp — stateless, low-level

---

## 7. Retrieve API

### Gọi Retrieve API

```python
response = bedrock_agent_client.retrieve(
    knowledgeBaseId='XXXXXXXXXX',
    retrievalQuery={'text': 'What is PaymentGW rate limit?'},
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5  # Top-K chunks trả về
        }
    }
)

# Parse kết quả
for result in response['retrievalResults']:
    print(result['content']['text'])      # Nội dung chunk
    print(result['score'])                # Cosine similarity score (0-1)
    print(result['location']['s3Location']['uri'])  # Source file
```

### Score có nghĩa gì?
- Score = cosine similarity giữa query vector và chunk vector
- Range: 0 (không liên quan) → 1 (giống hệt)
- Score > 0.5: retrieval tốt
- Score < 0.3: có thể lấy sai document

### numberOfResults ảnh hưởng gì?
- Tăng K → nhiều context hơn → answer đầy đủ hơn nhưng chậm hơn, tốn tokens hơn
- Giảm K → nhanh hơn nhưng có thể thiếu thông tin
- L1: K=5 đủ (single-fact)
- L2: K=8-10 (multi-source synthesis)

---

## 8. RetrieveAndGenerate vs Retrieve + InvokeModel

### Cách 1: RetrieveAndGenerate (built-in)

```python
response = bedrock_agent_client.retrieve_and_generate(
    input={'text': query},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb_id,
            'modelArn': f'arn:aws:bedrock:us-east-1::foundation-model/{model_id}'
        }
    }
)
answer = response['output']['text']
```

**Ưu điểm:** Đơn giản, ít code  
**Nhược điểm:** Ít control, không tùy chỉnh được prompt

### Cách 2: Retrieve rồi InvokeModel (manual)

```python
# Step 1: Retrieve
chunks = bedrock_agent_client.retrieve(...)

# Step 2: Construct prompt
context = "\n".join([c['content']['text'] for c in chunks['retrievalResults']])
prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"

# Step 3: Generate
response = bedrock_runtime_client.invoke_model(
    modelId=model_id,
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    })
)
```

**Ưu điểm:** Toàn quyền control prompt, dễ debug  
**Nhược điểm:** Nhiều code hơn

---

## 9. Inference Profiles — Tại Sao Cần `us.` Prefix

### Model cũ (legacy): gọi trực tiếp

```python
model_id = "anthropic.claude-3-haiku-20240307-v1:0"  # ← Direct model ID
```

### Model mới (Claude 3.5+, Claude 4.x): bắt buộc dùng Inference Profile

```python
model_id = "us.anthropic.claude-haiku-4-5-20251001-v1:0"  # ← us. prefix
#           ↑
#   Cross-region Inference Profile
```

**Tại sao AWS bắt buộc?**
- Inference Profile tự động route request sang region có capacity
- Đảm bảo availability cao hơn
- Prefix `us.` = US cross-region profile (us-east-1, us-west-2)

### Naming Convention

```
anthropic.claude-[version]-[date]-v[n]:0    ← Legacy model ID
us.anthropic.claude-[version]-[date]-v[n]:0 ← Inference Profile (cần cho model mới)
```

---

## 10. Các Lỗi Thường Gặp và Cách Fix

### Lỗi 1: Access Denied khi tạo folder S3

```
Insufficient permission to create folder
```

**Fix:** Thêm `s3:PutObject` vào IAM policy cho bucket

---

### Lỗi 2: Model Legacy/Deprecated

```
Access denied. This Model is marked by provider as Legacy
and you have not been actively using the model in the last 30 days.
```

**Fix:** Đổi sang model mới hơn trong `.env`

---

### Lỗi 3: Inference Profile Required

```
Invocation of model ID xxx with on-demand throughput isn't supported.
Retry your request with the ID or ARN of an inference profile.
```

**Fix:** Thêm prefix `us.` vào model ID

---

### Lỗi 4: temperature và top_p conflict

```
temperature and top_p cannot both be specified for this model.
```

**Fix:** Bỏ `top_p` khỏi request body, chỉ giữ `temperature`

---

### Lỗi 5: KB chưa sync xong

Triệu chứng: retrieve trả về 0 chunks

**Fix:** Vào Bedrock Console → Knowledge Base → Data source → Sync status phải là `Ready`

---

## 11. Prompt Engineering cho RAG

### System Prompt tốt cho RAG

```python
system = """You are a helpful AI assistant. Answer questions based ONLY on the provided context.

Rules:
1. Answer with a single short sentence or phrase - no markdown, no bullet points
2. Do NOT cite sources or add explanations
3. If the answer is NOT in the context, say "I don't have that information"
4. Be precise with numbers, dates, and technical details
5. Prefer CURRENT/active documents over ARCHIVED ones"""
```

### Xử lý conflict giữa documents (L2)

Khi KB retrieve cả `api_reference_v1_archived.md` và `api_reference_v2.md`:

```python
system = """...
5. Prefer CURRENT/active documents over ARCHIVED ones
6. When documents conflict, use the one with the latest date or status=CURRENT
7. Acknowledge the discrepancy if asked"""
```

### Context format tốt

```python
context_parts = []
for i, chunk in enumerate(chunks, 1):
    source = chunk['source'].split('/')[-1]
    context_parts.append(f"[Document {i}: {source}]\n{chunk['text']}")

context = "\n\n".join(context_parts)
```

---

## 12. Đánh Giá RAG Output (Testing)

### Keyword-based (đơn giản, dùng trong lab)

```python
def check_answer(expected, actual):
    expected_norm = expected.lower().replace(",", "").strip()
    actual_norm = actual.lower().replace(",", "").strip()

    # Containment check
    if expected_norm in actual_norm or actual_norm in expected_norm:
        return True

    # Key numbers must match
    import re
    exp_nums = set(re.findall(r"\d+", expected_norm))
    act_nums = set(re.findall(r"\d+", actual_norm))
    if exp_nums and not exp_nums.issubset(act_nums):
        return False

    # Keyword match >= 70%
    skip = {"the","a","an","is","in","on","at","to","for","of","and","or"}
    words = [w.strip(".,!?") for w in expected_norm.split()
             if len(w) > 1 and w not in skip]
    if not words:
        return True
    return sum(1 for w in words if w in actual_norm) / len(words) >= 0.7
```

### Các phương pháp evaluation khác

| Phương pháp | Mô tả | Khi nào dùng |
|-------------|-------|-------------|
| Exact match | So sánh chính xác | Số liệu, ngày tháng |
| Keyword matching | Check từ khóa quan trọng | Factual Q&A |
| Semantic similarity | Embedding cosine similarity | Câu trả lời diễn giải |
| LLM-as-judge | Dùng Claude để đánh giá | Production, cần accuracy cao |

---

## 13. Kiểm Tra Số Chunks trong OpenSearch

Sau khi sync KB, xem số chunks thực tế:

**Cách 1: AWS Console**
> OpenSearch Serverless → Collections → [collection] → Indexes → **Document count**

Document count = số chunks (mỗi document = 1 chunk + 1 vector)

**Cách 2: AWS CLI**

```bash
# Xem sync job statistics
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id YOUR_KB_ID \
  --data-source-id YOUR_DS_ID \
  --region us-east-1
```

Output có `statistics.numberOfDocumentsScanned` (số files) và Document count trong OpenSearch (số chunks).

---

## 14. Tóm Tắt Các Điểm Quan Trọng

1. **RAG = Retrieve + Generate** — không phải model trả lời từ training data
2. **224 chunks từ 36 files** — mỗi file được chia nhỏ theo chunking strategy
3. **Score > 0.5** = retrieval tốt; Score < 0.3 = có thể sai document
4. **Titan Embeddings** rẻ hơn 5x Cohere — dùng cho English-only
5. **`bedrock-agent-runtime`** cho KB, **`bedrock-runtime`** cho model — hai client riêng biệt
6. **Model mới cần `us.` prefix** — Inference Profile bắt buộc từ Claude 3.5+
7. **Không dùng `temperature` + `top_p` cùng lúc** trên model mới
8. **numberOfResults** ảnh hưởng trực tiếp đến quality và speed của RAG
