# W5 — Course Mapping & Learning Priority

> **Dates:** 11 May - 15 May | Advanced Concepts
> **Dựa trên:** Syllabus chính thức
> ⚠️ Chưa có project announcement chính thức — cập nhật khi có.

---

## 📋 Danh sách courses theo ngày

| Course | Ngày | Thời lượng |
|--------|------|-----------|
| Configuring and Deploying VPCs with Multiple Subnets | Mon | 1h |
| Introduction to Amazon Virtual Private Cloud (VPC) | Mon | 1h |
| AWS Network Connectivity Options | Mon | 2.30h |
| AWS Network – Monitoring and Troubleshooting | Mon | 1h |
| AWS SimuLearn: Connecting VPCs 🧪 | Mon | 1h |
| Introduction to Amazon API Gateway | Mon | 1h |
| Amazon Bedrock AgentCore Gateway Tutorial | Tue | 3h |
| Amazon Elastic File System (Amazon EFS) Primer | Tue | 0.30h |
| AWS SimuLearn: File Systems in the Cloud 🧪 | Tue | 1h |
| AWS Backup Getting Started | Tue | 1h |
| AWS File Storage Services Getting Started | Wed | 2h |
| Architecting Serverless Applications | Wed | 2h |
| Scaling Serverless Architectures | Wed | 1.30h |
| Serverless Analytics | Wed | 0.25h |

---

## 🔴 Ưu tiên cao nhất

| Course | Topic | Tại sao ưu tiên |
|--------|-------|-----------------|
| **AWS Network Connectivity Options** (2.30h) | Networking | VPN, Direct Connect, VPC Peering, TGW — QnA kinh điển |
| **Configuring and Deploying VPCs with Multiple Subnets** | Networking | Multi-subnet, cross-AZ routing — diagram W5 |
| **AWS SimuLearn: Connecting VPCs** 🧪 | Networking | Hands-on VPC peering — evidence |
| **Architecting Serverless Applications** (2h) | Serverless | Event-driven patterns, SQS/SNS fan-out, Step Functions |
| **Scaling Serverless Architectures** (1.30h) | Serverless | Concurrency limits, reserved vs provisioned concurrency |
| **Introduction to Amazon API Gateway** | API | Deep dive — authorizers, throttling, stages |

---

## 🟡 Ưu tiên trung bình

| Course | Topic | Ghi chú |
|--------|-------|---------|
| **Amazon Bedrock AgentCore Gateway Tutorial** (3h) | AI / Bedrock | AgentCore — advanced Bedrock topic |
| **AWS Network – Monitoring and Troubleshooting** | Networking | VPC Flow Logs, Reachability Analyzer |
| **Serverless Analytics** | Serverless / Data | Kết nối data pipeline với serverless |
| **Introduction to Amazon VPC** | Networking | Review/reinforce VPC concepts |

---

## 🟢 Ưu tiên thấp

| Course | Ghi chú |
|--------|---------|
| **Amazon EFS Primer** (0.30h) | File system — nhanh, đọc sau |
| **AWS SimuLearn: File Systems in the Cloud** 🧪 | Hands-on EFS |
| **AWS Backup Getting Started** | Backup strategy |
| **AWS File Storage Services Getting Started** (2h) | Overview storage services |

---

## 📊 W5 Mental Model

```
[VPC Multi-Subnet + Multi-AZ]
    │
[VPC Peering / Transit Gateway / Direct Connect]
    │
[API Gateway]  ←  Throttling, Auth, Stages
    │
[Lambda]  ←  Concurrency, Event-driven patterns
    │
[SQS / SNS / EventBridge / Step Functions]
```

**Câu hỏi QnA dự đoán W5:**
- VPC Peering vs Transit Gateway — khi nào dùng cái nào?
- VPN vs Direct Connect — trade-offs?
- API Gateway REST API vs HTTP API?
- Reserved concurrency vs Provisioned concurrency?
- SQS vs SNS vs EventBridge — khi nào dùng cái nào?
