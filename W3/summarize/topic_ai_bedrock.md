# AI & Amazon Bedrock — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** Amazon Bedrock Getting Started, Introduction to Amazon Bedrock: Foundation Models and AI Applications, Integrating AI into Your Apps with Amazon Bedrock, Building with MultiModal Knowledge Bases in AWS Bedrock, Build with S3 Vectors + Bedrock Knowledge Bases, Multi-Agent Collaboration with Amazon Bedrock Agents

---

## 1. Amazon Bedrock — Tổng Quan

### Bedrock là gì?
- **Fully managed service** để build generative AI applications.
- Cung cấp access vào **Foundation Models (FMs)** từ nhiều providers qua 1 API.
- Serverless — không cần quản lý infrastructure.
- Data của bạn **không được dùng để train model** của providers.

### Foundation Models có sẵn trên Bedrock
| Provider | Models |
|----------|--------|
| **Anthropic** | Claude 3 (Haiku, Sonnet, Opus) |
| **Amazon** | Titan Text, Titan Embeddings, Nova |
| **Meta** | Llama 3 |
| **Mistral** | Mistral, Mixtral |
| **Stability AI** | Stable Diffusion (image generation) |
| **Cohere** | Command, Embed |

### Cách chọn Model
| Nhu cầu | Model phù hợp |
|---------|--------------|
| Text generation, Q&A, summarization | Claude, Llama, Titan Text |
| Embedding (vector representation) | Titan Embeddings, Cohere Embed |
| Image generation | Stable Diffusion |
| Fast, cheap, simple tasks | Claude Haiku, Mistral |
| Complex reasoning | Claude Sonnet/Opus |

---

## 2. Bedrock API — Cách Tích Hợp

### InvokeModel API
Gọi trực tiếp model, nhận response đồng bộ:

```python
import boto3, json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Explain VPC in simple terms"}]
    })
)

result = json.loads(response['body'].read())
print(result['content'][0]['text'])
```

### Converse API (Recommended)
API thống nhất cho tất cả models — không cần biết format riêng của từng model:

```python
response = bedrock.converse(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    messages=[{"role": "user", "content": [{"text": "Hello"}]}]
)
```

---

## 3. RAG — Retrieval Augmented Generation

### Vấn đề của FM thuần túy
- FM chỉ biết data đến thời điểm training (knowledge cutoff).
- Không biết về data nội bộ của công ty.
- Có thể "hallucinate" — tạo ra thông tin sai.

### RAG giải quyết thế nào
Thay vì hỏi FM trực tiếp, RAG:
1. **Retrieve:** Tìm kiếm documents liên quan từ knowledge base
2. **Augment:** Thêm documents đó vào prompt
3. **Generate:** FM trả lời dựa trên context được cung cấp

```
User Question
      │
      ▼
[Embedding Model] → Vector → [Vector Store] → Similar Docs
                                                    │
      ┌─────────────────────────────────────────────┘
      ▼
[Prompt = Question + Retrieved Docs] → FM → Answer
```

### RAG Pipeline Components
| Component | Vai trò | AWS Service |
|-----------|---------|-------------|
| **Document Store** | Lưu raw documents | S3 |
| **Embedding Model** | Convert text → vectors | Titan Embeddings, Cohere Embed |
| **Vector Store** | Lưu và search vectors | OpenSearch Serverless, Aurora pgvector, S3 Vectors |
| **FM** | Generate answer từ context | Claude, Llama... |

---

## 4. Amazon Bedrock Knowledge Bases

### Knowledge Base là gì?
- **Managed RAG pipeline** — AWS lo toàn bộ: chunking, embedding, vector store, retrieval.
- Bạn chỉ cần: upload documents vào S3, tạo Knowledge Base, gọi API.

### Cách hoạt động
```
1. Ingest: S3 docs → Chunking → Embedding → Vector Store
2. Query:  User question → Embed → Search vectors → Retrieve chunks → FM → Answer
```

### Chunking Strategies
| Strategy | Dùng khi |
|----------|---------|
| **Fixed size** | Documents đồng nhất, đơn giản |
| **Semantic** | Documents phức tạp, cần context |
| **Hierarchical** | Documents có cấu trúc (headings, sections) |

### RetrieveAndGenerate API
```python
bedrock_agent = boto3.client('bedrock-agent-runtime')

response = bedrock_agent.retrieve_and_generate(
    input={'text': 'What is our refund policy?'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'KB_ID',
            'modelArn': 'arn:aws:bedrock:...:claude-3-haiku'
        }
    }
)
print(response['output']['text'])
```

### S3 Vectors (Mới)
- Native vector storage trong S3 — không cần OpenSearch hay Aurora.
- Đơn giản hơn, rẻ hơn cho use cases cơ bản.
- Dùng cho: Knowledge Base, semantic search.

---

## 5. Amazon Bedrock Agents

### Agent là gì?
- FM có khả năng **lập kế hoạch và thực hiện multi-step tasks** tự động.
- Không chỉ trả lời — còn có thể gọi APIs, query database, thực hiện actions.

### Anatomy của Bedrock Agent
```
Bedrock Agent
├── Foundation Model (FM)     ← "bộ não" — reasoning và planning
├── Instructions              ← system prompt, định nghĩa behavior
├── Action Groups             ← APIs agent có thể gọi (Lambda functions)
└── Knowledge Base            ← RAG — thông tin agent có thể tra cứu
```

### Action Groups
- Định nghĩa **actions** agent có thể thực hiện.
- Mỗi action = 1 Lambda function.
- Dùng **OpenAPI schema** để mô tả API spec cho agent.

```
User: "Book a flight from HAN to SGN tomorrow"
Agent:
  1. Understand intent (FM)
  2. Call searchFlights action (Lambda)
  3. Call bookFlight action (Lambda)
  4. Return confirmation (FM)
```

### Multi-Agent Collaboration
- **Supervisor Agent** điều phối nhiều **Sub-Agents** chuyên biệt.
- Mỗi sub-agent có expertise riêng (booking, payment, support...).
- Supervisor phân công task cho đúng sub-agent.

```
User Request → Supervisor Agent
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
    Booking      Payment    Support
    Agent        Agent      Agent
```

---

## 6. Model Customization

### Tại sao cần Customize?
- FM mặc định là general-purpose — không tối ưu cho domain cụ thể.
- Customization giúp model hiểu terminology, format, và behavior của bạn tốt hơn.

### Các kỹ thuật Customization

| Kỹ thuật | Mô tả | Dùng khi |
|----------|-------|---------|
| **Fine-tuning** | Train lại model với labeled data (input/output pairs) | Cần model học task cụ thể, có dataset sẵn |
| **Continued Pre-training** | Tiếp tục train với unlabeled domain data | Cần model hiểu domain knowledge (y tế, pháp lý...) |
| **Reinforcement Fine-tuning (RFT)** | Train dựa trên reward signal, không cần large labeled dataset | Có thể định nghĩa "good response" rõ ràng |
| **Custom Model Import** | Import model đã train từ nơi khác (SageMaker, HuggingFace...) | Đã có model riêng, muốn dùng qua Bedrock API |

### Fine-tuning Flow
```
Your labeled data (S3)
        │
        ▼
  Bedrock Fine-tuning Job
        │
        ▼
  Custom Model (provisioned throughput)
        │
        ▼
  Deploy & Invoke via Bedrock API
```

> **Lưu ý:** Fine-tuned models yêu cầu **Provisioned Throughput** — không dùng on-demand pricing như FM gốc.

---

## 7. Model Evaluation

### Mục đích
- So sánh nhiều FMs để chọn model phù hợp nhất cho use case.
- Đánh giá chất lượng response trước khi deploy production.

### Hai loại Evaluation

| Loại | Cách hoạt động | Metrics |
|------|---------------|---------|
| **Automatic Evaluation** | Dùng curated datasets + algorithms | Accuracy, Robustness, Toxicity, BERTScore |
| **Human Evaluation** | Người thật rate responses | Custom criteria do bạn định nghĩa |

### Khi nào dùng?
- Trước khi chọn FM cho production → dùng Automatic Evaluation để so sánh nhanh.
- Khi cần đánh giá chất lượng subjective (tone, helpfulness) → dùng Human Evaluation.
- Sau khi fine-tune → so sánh custom model vs base model.

---

## 8. Bedrock Guardrails

- **Content filtering** — block harmful content (hate speech, violence, PII...).
- **Topic denial** — ngăn model trả lời về topics không liên quan.
- **Grounding check** — verify response dựa trên source documents (giảm hallucination).
- Áp dụng cho cả input (user prompt) và output (model response).

---

## 9. Bedrock AgentCore *(2025 — Production-scale)*

### AgentCore là gì?
- Infrastructure layer để **deploy và operate agents ở production** một cách secure và scalable.
- Giải quyết các vấn đề thực tế khi đưa agent lên production: memory, security, observability...

### 7 Services của AgentCore

| Service | Vai trò |
|---------|---------|
| **Runtime** | Môi trường thực thi agent, tự động scale |
| **Gateway** | Quản lý kết nối tới external APIs và tools |
| **Memory** | Persistent memory — agent nhớ context qua nhiều sessions |
| **Identity** | Auth & authorization cho agent (IAM integration) |
| **Observability** | Logging, tracing, monitoring agent behavior |
| **Code Interpreter** | Agent có thể viết và chạy code trực tiếp |
| **Browser** | Agent có thể browse web để lấy thông tin |

### AgentCore vs Bedrock Agents

```
Bedrock Agents     → Build logic của agent (FM + Actions + KB)
AgentCore          → Infrastructure để run agent đó ở production
```

> Tương tự: Bedrock Agents = viết app, AgentCore = deploy app lên server.

---

## 10. Prompt Engineering Cơ Bản

### Cấu trúc prompt tốt
```
System: [Role và context của AI]
Human: [Task cụ thể]
       [Context/data cần thiết]
       [Format output mong muốn]
```

### Techniques
| Technique | Mô tả | Dùng khi |
|-----------|-------|---------|
| **Zero-shot** | Hỏi thẳng, không ví dụ | Task đơn giản |
| **Few-shot** | Cho vài ví dụ trước khi hỏi | Cần format cụ thể |
| **Chain of Thought** | Yêu cầu "think step by step" | Reasoning phức tạp |
| **RAG** | Cung cấp context từ documents | Cần thông tin cụ thể |

---

## Quick Reference

**Q: RAG là gì và tại sao cần?**
A: Retrieval Augmented Generation — kỹ thuật cung cấp context từ knowledge base vào prompt trước khi FM trả lời. Cần vì FM không biết data nội bộ của công ty và có knowledge cutoff. RAG giúp FM trả lời chính xác hơn dựa trên data thực tế.

**Q: Bedrock Knowledge Base khác RAG tự build thế nào?**
A: Knowledge Base là managed RAG — AWS lo chunking, embedding, vector store, retrieval. Tự build phải tự setup từng component. Knowledge Base đơn giản hơn, ít code hơn, nhưng ít flexible hơn.

**Q: Bedrock Agent dùng để làm gì?**
A: Cho phép FM thực hiện multi-step tasks tự động — không chỉ trả lời mà còn gọi APIs, query database qua Action Groups (Lambda). Anatomy: FM + Instructions + Action Groups + Knowledge Base.

**Q: Embedding là gì?**
A: Chuyển đổi text thành vector số (list of floats) — đại diện cho "ý nghĩa" của text trong không gian nhiều chiều. Texts có ý nghĩa tương tự sẽ có vectors gần nhau. Dùng trong RAG để tìm documents liên quan đến câu hỏi.

**Q: Fine-tuning khác RAG thế nào?**
A: RAG cung cấp context lúc runtime (không thay đổi model). Fine-tuning thay đổi weights của model — model "học" luôn vào bên trong. RAG linh hoạt hơn, dễ update data. Fine-tuning tốt hơn khi cần model học style, format, hoặc domain-specific behavior cố định.

**Q: Model Evaluation dùng để làm gì?**
A: So sánh và chọn FM phù hợp trước khi dùng. Có 2 loại: Automatic (dùng metrics như accuracy, toxicity) và Human (người thật rate). Dùng sau fine-tuning để verify custom model tốt hơn base model.

**Q: AgentCore là gì, khác Bedrock Agents thế nào?**
A: Bedrock Agents = build logic của agent (FM + Actions + Knowledge Base). AgentCore = infrastructure để deploy agent đó lên production với đầy đủ memory, security, observability, code interpreter, browser. Agents là "what", AgentCore là "how to run it at scale".
