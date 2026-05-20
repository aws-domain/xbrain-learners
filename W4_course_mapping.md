# W4 — Course Mapping & Learning Priority

> W4: 4 May - 8 May | Advanced Concepts
> Dựa trên syllabus cập nhật 7-May-2026

---

## 📋 Danh sách courses theo ngày

### Thứ Hai (Mon)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Amazon OpenSearch Service Getting Started | 1h | Digital Course |
| Amazon DynamoDB - Data Modeling Techniques | 1h | Digital Course |
| Introduction to Amazon DynamoDB 🧪 | 0.45h | Lab |
| Amazon Bedrock AgentCore Getting Started | 1h | Digital Course |
| Amazon Bedrock AgentCore Tools Tutorial | 1.30h | Digital Course |
| Data Engineering on AWS - Foundations | 4h | Digital Course |

### Thứ Ba (Tue)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Responsible Artificial Intelligence Practices | 1h | Digital Course |
| Amazon EMR Getting Started | 1h | Digital Course |
| AWS Glue Getting Started | 1h | Digital Course |
| Introduction to Amazon Athena | 1h | Digital Course |
| Amazon Redshift Getting Started | 1h | Digital Course |
| Amazon Aurora Getting Started | 1h | Digital Course |
| Amazon Kinesis Data Streams - Getting Started | 1h | Digital Course |
| Data Modeling for Amazon Neptune | 1h | Digital Course |

### Thứ Tư (Wed)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Data Modeling for Amazon ElastiCache for Redis | 1h | Digital Course |
| Amazon Connect Data Streaming Intermediate | 1h | Digital Course |
| Sensitive Data Detection with Amazon Macie | 1h | Digital Course |
| Introduction to Machine Learning: Art of the Possible | 0.30h | Digital Course |
| Machine Learning Essentials for Business and Technical Decision Makers | 1.30h | Digital Course |
| Machine Learning Exam Basics | 2h | Digital Course |
| Developing Machine Learning Solutions | 1h | Digital Course |

---

## 🔴 Ưu tiên cao nhất (trực tiếp ảnh hưởng điểm)

| Course | Thời lượng | Tại sao ưu tiên |
|--------|-----------|-----------------|
| **Data Engineering on AWS - Foundations** | 4h | Nền tảng toàn bộ W4: Kinesis → Glue → S3 → Athena/Redshift pipeline |
| **Amazon Kinesis Data Streams - Getting Started** | 1h | Real-time ingestion, shard capacity, consumer types — bị hỏi thẳng trong QnA |
| **AWS Glue Getting Started** | 1h | Crawler, Data Catalog, Job (Spark/Python Shell) — evidence section 3 |
| **Introduction to Amazon Athena** | 1h | Serverless SQL trên S3, partition pruning, cost per query — QnA kinh điển |
| **Amazon EMR Getting Started** | 1h | Spark on EMR vs Glue — khi nào dùng cái nào, câu hỏi phân biệt |
| **Amazon Bedrock AgentCore Getting Started** | 1h | AgentCore foundation — cần cho AI agent pipeline |
| **Amazon Bedrock AgentCore Tools Tutorial** | 1.30h | Hands-on AgentCore tools — action groups, orchestration |

---

## 🟡 Ưu tiên trung bình (cần cho diagram + DB layer)

| Course | Thời lượng | Ghi chú |
|--------|-----------|---------|
| **Amazon Redshift Getting Started** | 1h | Data warehouse vs data lake — câu hỏi phân biệt Redshift vs Athena |
| **Amazon OpenSearch Service Getting Started** | 1h | Full-text search, log analytics — khi nào dùng OpenSearch vs Athena |
| **Amazon Aurora Getting Started** | 1h | Aurora Serverless v2, Global Database, fast failover |
| **Amazon DynamoDB - Data Modeling Techniques** | 1h | Partition key design, GSI, single-table design |
| **Introduction to Amazon DynamoDB** 🧪 | 0.45h | Hands-on DynamoDB — CRUD operations |
| **Responsible Artificial Intelligence Practices** | 1h | AI ethics, governance — cần cho Bedrock projects |
| **Sensitive Data Detection with Amazon Macie** | 1h | Data security, PII detection — compliance |
| **Introduction to Machine Learning: Art of the Possible** | 0.30h | ML use cases overview |
| **Machine Learning Essentials for Business and Technical Decision Makers** | 1.30h | ML strategy và decision framework |

---

## 🟢 Ưu tiên thấp (bonus / niche use case)

| Course | Ghi chú |
|--------|---------|
| **Data Modeling for Amazon Neptune** | Chỉ cần nếu dùng graph database |
| **Data Modeling for Amazon ElastiCache for Redis** | Bonus nếu thêm caching layer |
| **Amazon Connect Data Streaming Intermediate** | Niche — chỉ cần nếu app có contact center use case |
| **Machine Learning Exam Basics** (2h) | Exam prep — học sau nếu thi ML cert |
| **Developing Machine Learning Solutions** | Advanced ML — không cần cho W4 deliverable |

---

## 📊 Data Pipeline Architecture — W4 Mental Model

```
[Sources]          [Ingestion]        [Processing]      [Storage]         [Query/Serve]
App Events    →   Kinesis Data    →   AWS Glue      →   S3 Data Lake  →   Athena (ad-hoc)
DB Changes        Streams             (ETL/ELT)         (Parquet/ORC)     Redshift (BI)
S3 Uploads    →   (real-time)     →   EMR Spark     →   Redshift      →   OpenSearch
                                      (batch)           (warehouse)       (full-text)
                                  →   Lambda        →   DynamoDB      →   App API
                                      (serverless)      (operational)
```

**Câu hỏi QnA kinh điển W4:**
- Kinesis vs SQS: khi nào dùng cái nào? (Kinesis = ordered, replay, analytics; SQS = decoupling, at-least-once)
- Glue vs EMR: khi nào dùng cái nào? (Glue = managed, serverless ETL; EMR = custom Spark, cost-sensitive large jobs)
- Athena vs Redshift: khi nào dùng cái nào? (Athena = ad-hoc, pay-per-query, no infra; Redshift = BI, complex joins, sustained workloads)
- OpenSearch vs Athena: khi nào dùng cái nào? (OpenSearch = full-text search, real-time; Athena = structured SQL, batch)
- AgentCore vs raw Bedrock API: khi nào dùng cái nào?

---

## 🔧 Workshop / Practice Resources

### Data Engineering Pipeline
- **[AWS Data Engineering Workshop](https://catalog.workshops.aws/data-engineering/en-US)** — Kinesis → Glue → S3 → Athena end-to-end
- **[Amazon Kinesis Workshop](https://catalog.workshops.aws/kinesis/en-US)** — shard management, consumer types, enhanced fan-out
- **[AWS Glue Workshop](https://catalog.workshops.aws/glue/en-US)** — Crawler, Data Catalog, Glue Job với PySpark
- **[Amazon Athena Workshop](https://catalog.workshops.aws/athena/en-US)** — partition projection, CTAS, cost optimization

### Database
- **[Amazon DynamoDB Labs](https://amazon-dynamodb-labs.com/)** — partition key design, GSI, Query vs Scan, DAX

### AI / ML / Bedrock
- **[Amazon Bedrock Workshop](https://catalog.workshops.aws/amazon-bedrock/en-US)** — AgentCore, Knowledge Base, RAG pipeline

---

## 📅 Thứ tự học tối ưu theo ngày

### Thứ Hai — Data Engineering + DB + AgentCore
1. **Data Engineering on AWS - Foundations** (4h) → hiểu toàn bộ pipeline trước
2. **Amazon DynamoDB - Data Modeling Techniques** (1h) → single-table design
3. **Introduction to Amazon DynamoDB** Lab (0.45h) → hands-on
4. **Amazon OpenSearch Service Getting Started** (1h) → search/analytics layer
5. **Amazon Bedrock AgentCore Getting Started** (1h) → AgentCore concepts
6. **Amazon Bedrock AgentCore Tools Tutorial** (1.30h) → hands-on tools

### Thứ Ba — ETL + Query + Analytics
1. **Amazon Kinesis Data Streams - Getting Started** (1h) → ingestion layer
2. **AWS Glue Getting Started** (1h) → ETL, Crawler, Data Catalog
3. **Introduction to Amazon Athena** (1h) → serverless SQL trên S3
4. **Amazon EMR Getting Started** (1h) → Glue vs EMR decision
5. **Amazon Redshift Getting Started** (1h) → warehouse vs lake
6. **Amazon Aurora Getting Started** (1h) → relational DB upgrade path
7. **Data Modeling for Amazon Neptune** (1h) → graph DB concepts
8. **Responsible Artificial Intelligence Practices** (1h) → AI governance

### Thứ Tư — ML + Data Security
1. **Introduction to Machine Learning: Art of the Possible** (0.30h) → ML overview
2. **Machine Learning Essentials** (1.30h) → ML strategy
3. **Machine Learning Exam Basics** (2h) → exam prep
4. **Developing Machine Learning Solutions** (1h) → hands-on ML
5. **Sensitive Data Detection with Amazon Macie** (1h) → data security
6. **Data Modeling for Amazon ElastiCache for Redis** (1h) → caching patterns
7. **Amazon Connect Data Streaming Intermediate** (1h) → streaming niche
