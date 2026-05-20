# W5 — Course Mapping & Learning Priority

> **Dates:** 11 May - 15 May | Advanced Concepts
> **Dựa trên:** Syllabus cập nhật 7-May-2026

---

## 📋 Danh sách courses theo ngày

### Thứ Hai (Mon)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Configuring and Deploying VPCs with Multiple Subnets | 1h | Digital Course |
| Introduction to Amazon Virtual Private Cloud (VPC) 🧪 | 1h | Lab |
| AWS Network Connectivity Options | 2.30h | Digital Course |
| AWS SimuLearn: Connecting VPCs 🧪 | 1h | Lab |
| AWS Network – Monitoring and Troubleshooting | 1h | Digital Course |
| AWS Network Firewall Getting Started | 1h | Digital Course |

### Thứ Ba (Tue)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| AWS File Storage Services Getting Started | 2h | Digital Course |
| Amazon Elastic File System (Amazon EFS) Primer | 0.30h | Digital Course |
| AWS SimuLearn: File Systems in the Cloud 🧪 | 1h | Lab |
| AWS Backup Getting Started | 1h | Digital Course |

### Thứ Tư (Wed)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Introduction to Amazon API Gateway 🧪 | 1h | Lab |
| Architecting Serverless Applications | 2h | Digital Course |
| Scaling Serverless Architectures | 1.30h | Digital Course |
| Serverless Analytics | 0.25h | Digital Course |

---

## 🔴 Ưu tiên cao nhất

| Course | Topic | Tại sao ưu tiên |
|--------|-------|-----------------|
| **AWS Network Connectivity Options** (2.30h) | Networking | VPN, Direct Connect, VPC Peering, TGW — QnA kinh điển |
| **Configuring and Deploying VPCs with Multiple Subnets** | Networking | Multi-subnet, cross-AZ routing — diagram W5 |
| **AWS SimuLearn: Connecting VPCs** 🧪 | Networking | Hands-on VPC peering — evidence |
| **Architecting Serverless Applications** (2h) | Serverless | Event-driven patterns, SQS/SNS fan-out, Step Functions |
| **Scaling Serverless Architectures** (1.30h) | Serverless | Concurrency limits, reserved vs provisioned concurrency |
| **Introduction to Amazon API Gateway** 🧪 | API | Hands-on Lab — authorizers, throttling, stages |
| **AWS Network Firewall Getting Started** | Security/Networking | Stateful inspection, domain filtering — network security layer |

---

## 🟡 Ưu tiên trung bình

| Course | Topic | Ghi chú |
|--------|-------|---------|
| **AWS Network – Monitoring and Troubleshooting** | Networking | VPC Flow Logs, Reachability Analyzer |
| **Introduction to Amazon VPC** 🧪 | Networking | Hands-on VPC — review/reinforce |
| **Serverless Analytics** (0.25h) | Serverless / Data | Kết nối data pipeline với serverless |
| **AWS File Storage Services Getting Started** (2h) | Storage | EFS, FSx, overview storage services |

---

## 🟢 Ưu tiên thấp

| Course | Ghi chú |
|--------|---------|
| **Amazon EFS Primer** (0.30h) | File system — nhanh, đọc sau |
| **AWS SimuLearn: File Systems in the Cloud** 🧪 | Hands-on EFS |
| **AWS Backup Getting Started** | Backup strategy |

---

## 📊 W5 Mental Model

```
[VPC Multi-Subnet + Multi-AZ]
    │
[VPC Peering / Transit Gateway / Direct Connect]
    │
[Network Firewall]  ←  Stateful inspection, domain filtering
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
- AWS Network Firewall vs Security Groups vs NACLs — layers?
