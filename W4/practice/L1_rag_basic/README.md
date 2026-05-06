# L1 - RAG Basic: Single-Fact Retrieval

> **Prerequisites:** Hoàn thành 3 courses đầu (Amazon Bedrock Getting Started, Foundation Models, Integrating AI)

## Mục tiêu

Build một chatbot đơn giản có khả năng:
- Retrieve thông tin từ 1 document trong knowledge base
- Trả lời 10 câu hỏi L1 từ `questions/student/L1_questions.json`

## Kiến thức áp dụng

- **Bedrock Knowledge Base**: RAG pipeline (S3 → Vector Store → Retrieve API)
- **Bedrock Runtime**: Invoke model để generate answer
- **Embedding**: Text → Vector representation
- **Retrieval**: Cosine similarity search

---

## Ý nghĩa của L1

L1 là level đơn giản nhất trong bài practice W4 — mục tiêu là xây dựng một RAG chatbot cơ bản có thể trả lời câu hỏi từ **1 document duy nhất** trong knowledge base. "Single-fact retrieval" nghĩa là mỗi câu hỏi chỉ cần tìm thông tin từ 1 chỗ để trả lời.

Luồng hoạt động:
```
Câu hỏi → Tìm chunk liên quan trong KB → Đưa vào prompt → Claude trả lời
```

---

## Ý nghĩa từng file

```
L1_rag_basic/
├── bedrock_client.py    # Tầng giao tiếp với AWS
│                        # - retrieve(): gọi KB lấy chunks
│                        # - invoke_model(): gọi Claude generate answer
│
├── rag_pipeline.py      # Logic RAG chính
│                        # - retrieve() → construct_prompt() → generate()
│                        # Đây là "bộ não" của chatbot
│
├── chatbot.py           # Giao diện người dùng (CLI)
│                        # Chạy để chat trực tiếp: python chatbot.py
│
├── test_l1.py           # Tự động chấm điểm 10 câu hỏi L1
│                        # So sánh answer với expected trong questions JSON
│
├── requirements.txt     # Thư viện cần cài: boto3, python-dotenv
│
├── .env                 # Config thực tế (KB ID, region, model) - không commit lên git
│
└── .env.example         # Template mẫu cho .env
```

Mối quan hệ giữa các file:
```
test_l1.py
    └── gọi → rag_pipeline.py (RAGPipeline)
                  └── gọi → bedrock_client.py (BedrockClient)
                                  └── gọi → AWS Bedrock KB + Claude

chatbot.py
    └── gọi → rag_pipeline.py (cùng pipeline, chỉ khác interface)
```

`bedrock_client.py` là tầng thấp nhất — chỉ biết gọi AWS. `rag_pipeline.py` là tầng nghiệp vụ — biết cách kết hợp retrieve + generate. `test_l1.py` và `chatbot.py` là 2 cách dùng pipeline đó cho 2 mục đích khác nhau.

---

## Architecture Overview

```
User Question
    ↓
[1] Bedrock Retrieve API
    ↓ (returns relevant chunks)
[2] Prompt Construction (system + context + question)
    ↓
[3] Bedrock Invoke Model (Claude)
    ↓
Answer
```

---

## AWS Setup - Step by Step

### Step 1: Tạo S3 Bucket cho Knowledge Base

```bash
# Tạo bucket (thay YOUR_NAME bằng tên của bạn)
aws s3 mb s3://geekbrain-kb-YOUR_NAME --region us-east-1

# Upload 36 documents
aws s3 sync ../data_package/knowledge_base/ s3://geekbrain-kb-YOUR_NAME/docs/
```

**❓ Câu hỏi thực hành 1:** Sau khi upload xong, chạy lệnh `aws s3 ls s3://geekbrain-kb-YOUR_NAME/docs/ --recursive | wc -l`. Kết quả phải là bao nhiêu files? Tại sao?

---

### Step 2: Tạo Bedrock Knowledge Base

#### 2.1. Vào AWS Console → Amazon Bedrock → Knowledge bases → Create

#### 2.2. Knowledge base details:
- **Name**: `geekbrain-kb`
- **Description**: `GeekBrain internal documentation for AI chatbot`
- **IAM role**: Create and use a new service role

#### 2.3. Data source configuration:
- **Data source name**: `geekbrain-docs`
- **S3 URI**: `s3://geekbrain-kb-YOUR_NAME/docs/`

#### 2.4. Embeddings model:
- **Model**: `Titan Embeddings G1 - Text v1.2`
- **Dimensions**: 1024

**❓ Câu hỏi thực hành 2:** Tại sao chọn Titan Embeddings thay vì Cohere Embed? (Hint: xem pricing và performance trong course)

#### 2.5. Vector store:
- **Vector database**: Quick create a new vector store (OpenSearch Serverless)
- **Collection name**: `geekbrain-vectors`

#### 2.6. Chunking strategy:
- **Chunking strategy**: Default chunking
- **Max tokens**: 300
- **Overlap percentage**: 20%

**❓ Câu hỏi thực hành 3:** Với 36 documents, mỗi doc trung bình 500 words, chunking 300 tokens với 20% overlap sẽ tạo ra khoảng bao nhiêu chunks? (1 token ≈ 0.75 words)

#### 2.7. Sync data source
- Click **Sync** để ingest documents vào vector store
- Đợi ~5-10 phút cho quá trình hoàn tất

---

### Step 3: Test Bedrock KB trong Console

#### 3.1. Vào Knowledge base → Select your KB → Test

#### 3.2. Thử query:
```
What is the current API rate limit for PaymentGW?
```

**Expected result:** Phải retrieve được chunks từ `api_reference_v2.md` và trả lời `1000 requests per minute per merchant`

**❓ Câu hỏi thực hành 4:** Nếu kết quả trả về là `500 requests per minute`, điều gì đã xảy ra? (Hint: xem L1-01 grading notes)

---

### Step 4: Lấy Knowledge Base ID

```bash
# List all knowledge bases
aws bedrock-agent list-knowledge-bases --region us-east-1

# Lưu lại KNOWLEDGE_BASE_ID (dạng: XXXXXXXXXX)
```

Copy `knowledgeBaseId` vào file `.env` (sẽ tạo ở bước sau)

---

## Code Implementation

### File structure

```
L1_rag_basic/
├── README.md (file này)
├── .env.example
├── requirements.txt
├── bedrock_client.py      # Bedrock API wrapper
├── rag_pipeline.py        # RAG logic
├── chatbot.py             # Main chatbot interface
└── test_l1.py             # Test với 10 câu hỏi L1
```

---

### Setup Python Environment

```bash
cd L1_rag_basic/

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Testing

### Test với 10 câu hỏi L1

```bash
python test_l1.py
```

**Expected output:**
```
Testing L1 Questions...
[1/10] L1-01: What is the current API rate limit for PaymentGW?
✓ PASS - Answer: 1000 requests per minute per merchant
...
[10/10] L1-10: How often does GeekBrain rotate JWT signing keys?
✓ PASS - Answer: Every 30 days

Results: 10/10 passed
```

**❓ Câu hỏi thực hành 5:** Nếu câu L1-03 (PaymentGW outage root cause) fail, làm thế nào để debug? (Hint: check retrieved chunks)

---

## Interactive Testing

```bash
python chatbot.py
```

```
GeekBrain AI Chatbot (L1 - RAG Basic)
Type 'quit' to exit

You: What is GeekBrain's data retention policy for transaction logs?
Bot: GeekBrain's data retention policy for transaction logs is 7 years.

You: quit
```

---

## Debugging Tips

### 1. Check retrieved chunks

Thêm vào `rag_pipeline.py`:
```python
def retrieve_with_debug(self, query: str):
    response = self.retrieve(query)
    print(f"\n=== Retrieved {len(response['chunks'])} chunks ===")
    for i, chunk in enumerate(response['chunks']):
        print(f"\nChunk {i+1}:")
        print(f"Score: {chunk['score']}")
        print(f"Source: {chunk['source']}")
        print(f"Text: {chunk['text'][:200]}...")
    return response
```

### 2. Check prompt construction

Log prompt trước khi gọi Bedrock:
```python
print(f"\n=== Prompt ===\n{prompt}\n")
```

### 3. Common issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty chunks | KB chưa sync xong | Đợi sync hoàn tất |
| Wrong answer | Retrieved wrong doc | Improve query phrasing |
| Rate limit error | Quá nhiều requests | Add retry logic |

---

## Success Criteria

- ✅ 10/10 câu hỏi L1 pass
- ✅ Average response time < 3 seconds
- ✅ Retrieved chunks có score > 0.5
- ✅ Answer cite đúng source document

---

## Next Steps

Sau khi hoàn thành L1:
1. Học tiếp **Course 4-6** (MultiModal KB, S3 Vectors, SimuLearn Lab)
2. Move to **L2 - Multi-Source Reasoning**

**❓ Câu hỏi thực hành 6 (Bonus):** L1 chỉ retrieve từ 1 document. Nếu câu hỏi cần thông tin từ 2 documents (như L2-02), điều gì sẽ xảy ra với implementation hiện tại?
