# W3 — Course Mapping & Learning Priority

## ✅ Đã hoàn thành (removed from priority list)
- AWS Database Offerings, Amazon DynamoDB Getting Started, Amazon RDS Service Primer, AWS SimuLearn: Databases in Practice, AWS SimuLearn: First NoSQL Database, AWS Lambda Foundations, AWS Networking Basics, Subnets, Gateways, and Route Tables Explained, **Understanding AWS Networking Gateways**, **Differences Between Security Groups and NACLs**, **AWS SimuLearn: Networking Concepts**

## 🔴 Ưu tiên cao nhất (trực tiếp ảnh hưởng điểm)

| Course | Must-Have liên quan | Tại sao ưu tiên |
|--------|-------------------|-----------------|
| **Introduction to AWS Lambda** (1h Lab, Wed) | Must-have 3 — CloudWatch evidence | CloudWatch log sau S3 trigger — evidence section 5 |

## 🟡 Ưu tiên trung bình (cần cho diagram + VPC)

| Course | Must-Have liên quan | Ghi chú |
|--------|-------------------|---------|
| **Build with S3 Vectors + Bedrock KB** (1h, Mon) | Must-have 2 — Bedrock layer | RAG pipeline, embedding model, vector store |
| **Multi-Agent Collaboration Bedrock** (1h, Mon) | Must-have 2 — Bedrock layer | Anatomy của Bedrock Agent (FM + Instructions + Action Groups + KB) |

## 🟢 Ưu tiên thấp (bonus / W5 dùng nhiều hơn)

| Course | Ghi chú |
|--------|---------|
| **Getting Started with AWS CloudFormation** (1h, Wed) | Bonus +0.25 nếu có `validate-template` output |
| **Introduction to Amazon API Gateway** (6 phút, Tue) | Covered sâu hơn ở W5 |
| **AWS SimuLearn: Bedrock Playgrounds** (1h, Mon) | Chỉ để hiểu concept, không dùng Playground cho deliverable |

---

## Workshop / Practice Resources

### Database
- **[Amazon DynamoDB Labs](https://amazon-dynamodb-labs.com/)** — partition key design, GSI, Query vs Scan, DAX
- **[Amazon RDS Workshop](https://catalog.workshops.aws/rds-on-aws/en-US)** — Multi-AZ, Read Replica, failover drill

### Bedrock + RAG
- **[Amazon Bedrock Workshop](https://catalog.workshops.aws/amazon-bedrock/en-US)** — Knowledge Base, RAG pipeline, Agents với Action Groups
- **[Building with Amazon Bedrock](https://catalog.workshops.aws/building-with-amazon-bedrock/en-US)** — RetrieveAndGenerate API từ Lambda

### Lambda + VPC
- **[Lambda Powertools Workshop](https://catalog.workshops.aws/powertools/en-US)** — IAM least-privilege, CloudWatch structured logging
- **[VPC Networking Workshop](https://catalog.workshops.aws/networking/en-US)** — 3-tier VPC, S3 Gateway Endpoint, SGs vs NACLs

### CloudFormation (Bonus)
- **[CloudFormation Workshop](https://catalog.workshops.aws/cfn101/en-US)** — template structure, intrinsic functions, change sets

---

## Thứ tự học tối ưu (thứ Tư — hôm nay)

1. **Networking Concepts lab** → add S3 GW Endpoint ngay vào route table
2. **SGs vs NACLs** (6 phút) → thuộc luôn để trả lời QnA
3. **Lambda Foundations + Lab** → làm Evidence Pack section 5
4. **CloudFormation** (nếu còn thời gian) → bonus +0.25
