# W4 — Courses cần học theo Topic trọng tâm

> W4 project: Build an AI That Actually Answers (RAG + Tools + Memory)
> Topic trọng tâm: **AI/Bedrock** — không phải Data Engineering như dự đoán ban đầu

---

## Tại sao không phải Data Engineering?

`W4_course_mapping.md` dự đoán W4 là Kinesis → Glue → Athena pipeline. Thực tế project yêu cầu:
- Bedrock Knowledge Bases (RAG)
- Bedrock Agents / function calling (Tools)
- Lambda làm glue giữa LLM và data
- DynamoDB cho conversation state (Memory)

Kinesis, Glue, Athena, EMR **không xuất hiện** trong project. Bỏ qua tuần này.

---

## Thứ tự học theo ngày

---

### Thứ Hai — AI/Bedrock Foundation (ưu tiên cao nhất)

Mục tiêu: hiểu đủ để bắt đầu build L1 vào thứ Năm.

| Thứ tự | Course | Thời lượng | Liên quan đến |
|--------|--------|-----------|--------------|
| 1 | Amazon Bedrock Getting Started | 1h | Nền tảng — cách gọi Bedrock API, các model có sẵn |
| 2 | Introduction to Amazon Bedrock: Foundation Models and AI Applications | 45min | LLM fundamentals — tokenization, embedding, context window — QnA sẽ hỏi |
| 3 | Integrating AI into Your Apps with Amazon Bedrock | 10min | Cách gọi Bedrock từ code — ngắn, đọc nhanh |
| 4 | Building with MultiModal Knowledge Bases in AWS Bedrock | 20min | Trực tiếp là L1 setup — Bedrock KB + S3 |
| 5 | Build with Amazon S3 Vectors and Amazon Bedrock Knowledge Bases | 1h | RAG pipeline: S3 → KB → Retrieve API — core của L1 và L2 |
| 6 | AWS SimuLearn: Explore the Amazon Bedrock Playgrounds | 1h (Lab) | Hands-on với Bedrock trước khi build — làm quen console |

**Tổng: ~4h15min**

---

### Thứ Ba — Agents + DynamoDB (sau khi đã explore data)

Thứ Ba là ngày explore data package (đọc 36 docs, start API, seed DB). Học song song buổi tối hoặc lúc rảnh.

| Thứ tự | Course | Thời lượng | Liên quan đến |
|--------|--------|-----------|--------------|
| 7 | Multi-Agent Collaboration with Amazon Bedrock Agents | 1h | L3 approach — Bedrock Agents quản lý tool routing |
| 8 | Amazon Bedrock AgentCore Tools Tutorial | 1h | Tool implementation với AgentCore — nếu nhóm chọn approach này |
| 9 | Introduction to Amazon DynamoDB (Lab) | 45min | L4 memory — DynamoDB lưu conversation state |

**Tổng: ~2h45min**

---

### Thứ Tư — ML Theory (chuẩn bị cho QnA thứ Năm sáng)

Thứ Năm 08:30–10:00 có session "GenAI in practice" — trainer sẽ hỏi về AI/ML theory.

| Thứ tự | Course | Thời lượng | Liên quan đến |
|--------|--------|-----------|--------------|
| 10 | Introduction to Machine Learning: Art of the Possible | 30min | Big picture ML — supervised/unsupervised/RL |
| 11 | Machine Learning Essentials for Business and Technical Decision Makers | 1h30min | Deep learning architectures, LLM, GenAI — QnA theory |
| 12 | Developing Machine Learning Solutions | 1h | Training, overfitting, evaluation — QnA individual |

**Tổng: ~3h**

> Machine Learning Exam Basics (2h) có thể bỏ qua — quá rộng, không trực tiếp giúp build project.

---

## Tóm tắt theo mức độ ưu tiên

### Bắt buộc (ảnh hưởng trực tiếp đến điểm)

| Course | Lý do |
|--------|-------|
| Amazon Bedrock Getting Started | Không biết Bedrock → không build được gì |
| Introduction to Amazon Bedrock: Foundation Models | QnA individual sẽ hỏi LLM works như thế nào |
| Build with Amazon S3 Vectors and Bedrock Knowledge Bases | Đây chính là L1 của project |
| AWS SimuLearn: Explore the Amazon Bedrock Playgrounds | Hands-on trước khi build — tránh mất thời gian debug console |
| Multi-Agent Collaboration with Amazon Bedrock Agents | L3 tool routing — 4 điểm |

### Nên học (hỗ trợ QnA và L3/L4)

| Course | Lý do |
|--------|-------|
| Building with MultiModal Knowledge Bases in AWS Bedrock | Bổ sung context cho Bedrock KB setup |
| Integrating AI into Your Apps with Amazon Bedrock | Ngắn, bổ sung cách gọi API |
| Amazon Bedrock AgentCore Tools Tutorial | Nếu nhóm chọn AgentCore approach cho L3 |
| Introduction to Amazon DynamoDB (Lab) | L4 memory storage |
| Machine Learning Essentials for Business and Technical Decision Makers | Theory cho QnA thứ Năm sáng |

### Bỏ qua tuần này

| Course | Lý do bỏ |
|--------|----------|
| Data Engineering on AWS - Foundations | Không liên quan đến W4 project |
| Amazon Kinesis Data Streams | Không liên quan |
| AWS Glue Getting Started | Không liên quan |
| Introduction to Amazon Athena | Không liên quan |
| Amazon EMR Getting Started | Không liên quan |
| Machine Learning Exam Basics (2h) | Quá rộng, không giúp build project |
| Amazon Redshift Getting Started | Không liên quan |
| Amazon OpenSearch Service Getting Started | OpenSearch là vector store backend của Bedrock KB — AWS tự quản lý, không cần học riêng |

---

## Tổng thời gian học

| Ngày | Thời lượng | Nội dung |
|------|-----------|---------|
| Thứ Hai | ~4h15min | Bedrock foundation + KB + Lab |
| Thứ Ba (tối) | ~2h45min | Agents + DynamoDB |
| Thứ Tư | ~3h | ML theory cho QnA |
| **Tổng** | **~10h** | |

---

## Câu hỏi QnA hay gặp — cần nắm trước thứ Năm

Dựa trên pattern W3, trainer sẽ hỏi individual về:

- **RAG là gì?** Retrieval-Augmented Generation — thay vì LLM dùng training data, retrieve relevant chunks từ knowledge base rồi đưa vào context
- **Embedding là gì?** Vector representation của text — text tương tự nhau có vector gần nhau trong không gian nhiều chiều
- **Vector search hoạt động thế nào?** Cosine similarity giữa query embedding và document embeddings → trả về top-K chunks gần nhất
- **Tại sao cần Tools?** Knowledge base không có số liệu thực tế (costs, live metrics) — LLM cần gọi external tools để lấy data chính xác
- **Context window là gì?** Giới hạn số tokens LLM có thể xử lý trong 1 lần — ảnh hưởng đến bao nhiêu chunks có thể đưa vào
- **Tại sao L4 cần memory?** Mỗi LLM call độc lập — không có memory thì "its costs" ở Turn 2 không biết "its" là service nào từ Turn 1
- **Bedrock KB dùng vector store nào?** OpenSearch Serverless — AWS tự tạo và quản lý khi setup KB
- **Conflict resolution trong L2 hoạt động thế nào?** Retrieve cả 2 versions → system prompt hướng dẫn LLM ưu tiên document mới hơn / không archived
