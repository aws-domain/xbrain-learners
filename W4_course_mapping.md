# W4 — Course Mapping & Learning Priority

> Dựa trên XBRAIN_SYLLABUS_FOUNDATION.pdf và pattern từ W3_course_mapping.md
> Ngày hiện tại: Chủ nhật 26/04/2026 — W4 bắt đầu thứ Hai 27/04/2026

---

## 🔴 Ưu tiên cao nhất (trực tiếp ảnh hưởng điểm)

| Course | Syllabus Link | Thời lượng | Must-Have liên quan | Tại sao ưu tiên |
|--------|--------------|-----------|-------------------|-----------------|
| **Data Engineering on AWS: Foundations** | [Link](https://skillbuilder.aws/learn/6BP61KB1FJ/data-engineering-on-aws--foundations/KXCN4PJD9Y) | ~2h | MH1 — Data Pipeline | Nền tảng toàn bộ W4: Kinesis → Glue → S3 → Athena/Redshift pipeline. Không hiểu flow này → không làm được deliverable |
| **Amazon Kinesis Data Streams: Getting Started** | [Link](https://skillbuilder.aws/learn/KHG5GEQU5X/amazon-kinesis-data-streams--getting-started/DQDTPWKNDC) | ~1h | MH1 — Ingestion layer | Real-time ingestion, shard capacity, consumer types — bị hỏi thẳng trong QnA |
| **AWS Glue Getting Started** | [Link](https://skillbuilder.aws/learn/FJ1W4H4Y4J/aws-glue-getting-started/XTFXU583XT) | ~1h | MH1 — ETL layer | Crawler, Data Catalog, Job (Spark/Python Shell) — evidence section 3 |
| **Introduction to Amazon Athena** | [Link](https://skillbuilder.aws/learn/2VNY7PZH5D/introduction-to-amazon-athena/AZY6TC4HSY) | ~1h | MH1 — Query layer | Serverless SQL trên S3, partition pruning, cost per query — QnA kinh điển |
| **Amazon EMR Getting Started** | [Link](https://skillbuilder.aws/learn/8XT2XRPFE8/amazon-emr-getting-started/C71XRG5CZ5) | ~1h | MH1 — Batch processing | Spark on EMR vs Glue — khi nào dùng cái nào, câu hỏi phân biệt |
| **Architecting Serverless Applications** | [Link](https://skillbuilder.aws/learn/MRWENY7FSX/architecting-serverless-applications/QVFY2JHVEH) | ~1h | MH2 — Serverless tier | Event-driven patterns, SQS/SNS fan-out, Step Functions — bắt buộc cho diagram |
| **Scaling Serverless Architectures** | [Link](https://skillbuilder.aws/learn/Z5UZYF3RKH/scaling-serverless-architectures/A7FYXA9TNE) | ~1h | MH2 — Serverless tier | Concurrency limits, reserved concurrency, provisioned concurrency — QnA |
| **Serverless Analytics** | [Link](https://skillbuilder.aws/learn/93CCUDZ4MV/serverless-analytics/QM7UGZJU9Z) | ~1h | MH1 + MH2 | Kết nối data pipeline với serverless compute — evidence section 4 |

---

## 🟡 Ưu tiên trung bình (cần cho diagram + advanced networking)

| Course | Syllabus Link | Thời lượng | Must-Have liên quan | Ghi chú |
|--------|--------------|-----------|-------------------|---------|
| **Amazon Redshift Getting Started** | [Link](https://skillbuilder.aws/learn/U6RG471X6Z/amazon-redshift-getting-started/DXQWFPZ1TU) | ~1h | MH1 — Warehouse layer | Data warehouse vs data lake — câu hỏi phân biệt Redshift vs Athena |
| **Amazon OpenSearch Service Getting Started** | [Link](https://skillbuilder.aws/learn/AGNP6G31UQ/amazon-opensearch-service-getting-started/6WYZ571TJU) | ~1h | MH1 — Search/Analytics | Full-text search, log analytics — khi nào dùng OpenSearch vs Athena |
| **Amazon Aurora Getting Started** | [Link](https://skillbuilder.aws/learn/W95CCPKD1Y/amazon-aurora-getting-started/PT4AMCE9XC) | ~1h | MH3 — DB upgrade | Aurora Serverless v2, Global Database, fast failover — nếu W3 dùng RDS |
| **Configuring and Deploying VPCs with Multiple Subnets** | [Link](https://skillbuilder.aws/learn/4HWA8PME5S/configuring-and-deploying-vpcs-with-multiple-subnets/BTRCDVX2RU) | ~1h | MH4 — Advanced VPC | Multi-subnet VPC, cross-AZ routing — cần cho W4 multi-AZ diagram |
| **AWS Network Connectivity Options** | [Link](https://skillbuilder.aws/learn/WQJNBEZYDW/aws-network-connectivity-options/PZDF9Z7DN5) | ~1h | MH4 — VPC Peering | VPN, Direct Connect, VPC Peering, Transit Gateway — W5 preview |
| **AWS Network: Monitoring and Troubleshooting** | [Link](https://skillbuilder.aws/learn/G351ZT8UCX/aws-network--monitoring-and-troubleshooting/QRAFEARKRT) | ~1h | MH4 — Observability | VPC Flow Logs, Reachability Analyzer — evidence section 6 |
| **AWS SimuLearn: Connecting VPCs** | [Link](https://skillbuilder.aws/learn/46NC4HQFUY/aws-simulearn-connecting-vpcs/J7QJJRTCTG) | ~1h Lab | MH4 — VPC Peering lab | Hands-on VPC peering — evidence section 6 |
| **AWS SimuLearn: Autohealing and Scaling Applications** | [Link](https://skillbuilder.aws/learn/ND78HW21FD/aws-simulearn-autohealing-and-scaling-applications/1C6SZU2GKX) | ~1h Lab | MH2 — Auto Scaling | ASG + ALB + health checks — bắt buộc nếu W4 yêu cầu HA app tier |
| **AWS SimuLearn: Highly Available Web Applications** | [Link](https://skillbuilder.aws/learn/MSNJKZ17FF/aws-simulearn-highly-available-web-applications/7MVYAZPHY4) | ~1h Lab | MH2 — HA pattern | Multi-AZ ALB + ASG — evidence section 3 |

---

## 🟢 Ưu tiên thấp (bonus / W5 dùng nhiều hơn)

| Course | Syllabus Link | Ghi chú |
|--------|--------------|---------|
| **Amazon Connect Data Streaming Intermediate** | [Link](https://skillbuilder.aws/learn/K44CB4W9J7/amazon-connect-data-streaming-intermediate/CR15W873MX) | Niche — chỉ cần nếu app có contact center use case |
| **Data Modeling for Amazon Neptune** | [Link](https://skillbuilder.aws/learn/56HTB2HGDT/data-modeling-for-amazon-neptune/RYFX8U16NG) | Chỉ cần nếu W3 chọn Neptune |
| **Data Modeling for Amazon ElastiCache for Redis** | [Link](https://skillbuilder.aws/learn/2Y9Y39G1XF/data-modeling-for-amazon-elasticache-for-redis/Y4TTCMPPKV) | Bonus nếu thêm caching layer |
| **Amazon DynamoDB: Data Modeling Techniques** | [Link](https://skillbuilder.aws/learn/PBHFT7NDMR/amazon-dynamodb--data-modeling-techniques/7ESV38N5YX) | Deepdive nếu W3 chọn DynamoDB và muốn optimize |
| **Introduction to Amazon API Gateway** (version 2) | [Link](https://skillbuilder.aws/learn/87NHV2TSKV/introduction-to-amazon-api-gateway/3S1482KMEZ) | Covered sâu hơn ở W5 |
| **Amazon Bedrock AgentCore Gateway Tutorial** | [Link](https://skillbuilder.aws/learn/XGGBY7N7T1/amazon-bedrock-agentcore-gateway-tutorial/Q6M9C4BPG7) | W5+ — AgentCore là advanced topic |

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
- Lambda concurrency: reserved vs provisioned? (Reserved = cap; Provisioned = warm, no cold start)

---

## 🔧 Workshop / Practice Resources

### Data Engineering Pipeline
- **[AWS Data Engineering Workshop](https://catalog.workshops.aws/data-engineering/en-US)** — Kinesis → Glue → S3 → Athena end-to-end
- **[Amazon Kinesis Workshop](https://catalog.workshops.aws/kinesis/en-US)** — shard management, consumer types, enhanced fan-out
- **[AWS Glue Workshop](https://catalog.workshops.aws/glue/en-US)** — Crawler, Data Catalog, Glue Job với PySpark
- **[Amazon Athena Workshop](https://catalog.workshops.aws/athena/en-US)** — partition projection, CTAS, cost optimization

### Serverless & Event-Driven
- **[Serverless Patterns Workshop](https://catalog.workshops.aws/serverless-patterns/en-US)** — SQS/SNS fan-out, Step Functions, EventBridge
- **[AWS Step Functions Workshop](https://catalog.workshops.aws/step-functions/en-US)** — orchestration vs choreography, error handling
- **[Amazon EventBridge Workshop](https://catalog.workshops.aws/eventbridge/en-US)** — event bus, rules, targets

### Advanced Networking
- **[VPC Networking Workshop](https://catalog.workshops.aws/networking/en-US)** — VPC Peering, Transit Gateway, PrivateLink
- **[AWS Network Firewall Workshop](https://catalog.workshops.aws/network-firewall/en-US)** — stateful inspection, domain filtering

### Cost Optimization (nếu W4 có cost component)
- **[AWS Cost Optimization Workshop](https://catalog.workshops.aws/cost-optimization/en-US)** — Compute Optimizer, Savings Plans, S3 Intelligent-Tiering

---

## 📅 Thứ tự học tối ưu theo ngày

### Thứ Hai — Data Engineering Foundation
1. **Data Engineering on AWS: Foundations** (~2h) → hiểu toàn bộ pipeline trước
2. **Amazon Kinesis Data Streams: Getting Started** (~1h) → ingestion layer
3. **Serverless Analytics** (~1h) → kết nối pipeline với serverless

### Thứ Ba — ETL + Query Layer
1. **AWS Glue Getting Started** (~1h) → ETL, Crawler, Data Catalog
2. **Introduction to Amazon Athena** (~1h) → serverless SQL trên S3
3. **Amazon Redshift Getting Started** (~1h) → warehouse vs lake distinction
4. **Amazon EMR Getting Started** (~1h) → Glue vs EMR decision

### Thứ Tư — Serverless Architecture + Advanced Networking
1. **Architecting Serverless Applications** (~1h) → event-driven patterns
2. **Scaling Serverless Architectures** (~1h) → concurrency, cold starts
3. **AWS SimuLearn: Autohealing and Scaling** (~1h Lab) → ASG + ALB hands-on
4. **Configuring VPCs with Multiple Subnets** (~1h) → multi-AZ VPC
5. **AWS SimuLearn: Connecting VPCs** (~1h Lab) → VPC peering hands-on

### Thứ Năm — Review + Evidence Pack
- Consolidate diagram với data pipeline layer
- Hoàn thiện Evidence Pack sections 3-6
- Chạy lại các queries/demos để chuẩn bị Friday

---

## ⚠️ W3 Gaps cần fix trước khi thêm W4

Dựa trên pattern W2→W3, W4 sẽ check lại các W3 items:

- [ ] Evidence Pack `docs/W3_evidence.md` đã commit và post link lên Slack chưa?
- [ ] Lambda execution role không có wildcard — đã verify chưa?
- [ ] S3 Gateway Endpoint đã có trên route table và diagram chưa?
- [ ] Data Access Pattern Log Part C (wrong-paradigm test) đã đủ chưa?
- [ ] CloudWatch Logs sau S3 trigger đã capture chưa?

---

## 🗺️ Mapping với W4 Must-Haves (dự đoán)

Dựa trên progression W1→W2→W3, W4 nhiều khả năng sẽ yêu cầu:

| Must-Have (dự đoán) | Courses cần học | Evidence cần có |
|--------------------|----------------|----------------|
| **MH1: Data Pipeline** | Data Engineering Foundations + Kinesis + Glue + Athena | Glue Job run log + Athena query result |
| **MH2: Serverless Event-Driven** | Architecting Serverless + Scaling Serverless + SimuLearn HA | Step Functions execution + CloudWatch metrics |
| **MH3: HA / Auto Scaling** | SimuLearn Autohealing + Highly Available Web Apps | ASG activity log + ALB health check |
| **MH4: Advanced Networking** | VPC Multi-Subnet + Connecting VPCs + Network Monitoring | VPC Flow Logs + Peering connection screenshot |

> ⚠️ Cập nhật file này ngay khi có W4 project announcement chính thức từ trainer.
