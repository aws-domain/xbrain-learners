# W6 — Course Mapping & Learning Priority

> **Dates:** 18 May - 22 May | Advanced Concepts
> **Dựa trên:** Syllabus cập nhật 7-May-2026

---

## 📋 Danh sách courses theo ngày

### Thứ Hai (Mon)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| AWS SimuLearn: Auto-Healing and Scaling Applications 🧪 | 1h | Lab |
| AWS SimuLearn: Highly Available Web Applications 🧪 | 1h | Lab |
| Amazon Simple Storage Service (Amazon S3) Cost Optimization | 1h | Digital Course |
| Deep Dive: Amazon Elastic Block Store (Amazon EBS) Cost Optimization | 0.30h | Digital Course |
| AWS SimuLearn: Cloud Economics 🧪 | 1h | Lab |
| Deep Dive: Amazon Elastic Block Store (Amazon EBS) Performance Optimization | 1h | Digital Course |

### Thứ Ba (Tue)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| Auditing Your Security with AWS Trusted Advisor 🧪 | 1h | Lab |
| Getting Started with AWS Systems Manager 🧪 | 1h | Lab |
| Amazon CloudWatch Getting Started | 1h | Digital Course |
| Optimize Your Cloud Governance: Balance Security and Cost | 3h | Digital Course |
| AWS Cloud Financial Management for Builders | 1.50h | Digital Course |

### Thứ Tư (Wed)

| Course | Thời lượng | Loại |
|--------|-----------|------|
| AWS Security Best Practices: Monitoring and Alerting | 2h | Digital Course |
| AWS SimuLearn: Core Security Concepts 🧪 | 1h | Lab |
| Performing a Basic Audit of your AWS Environment 🧪 | 1h | Lab |
| Introduction to AWS Key Management Service 🧪 | 1h | Lab |
| Build with AWS Config: Enabling Security Controls and Incident Response | 1.50h | Digital Course |

---

## 🔴 Ưu tiên cao nhất

| Course | Topic | Tại sao ưu tiên |
|--------|-------|-----------------|
| **AWS SimuLearn: Auto-Healing and Scaling Applications** 🧪 | Compute / HA | ASG + ALB + health checks — evidence |
| **AWS SimuLearn: Highly Available Web Applications** 🧪 | Compute / HA | Multi-AZ ALB + ASG — diagram |
| **Amazon CloudWatch Getting Started** | Observability | Metrics, Logs, Alarms — monitoring evidence |
| **AWS Security Best Practices: Monitoring and Alerting** (2h) | Security | CloudWatch + CloudTrail + GuardDuty integration |
| **Introduction to AWS Key Management Service** 🧪 | Security | KMS key types, key policies, envelope encryption |
| **Optimize Your Cloud Governance: Balance Security and Cost** (3h) | Governance | Security vs cost trade-offs — capstone-relevant |
| **Build with AWS Config: Enabling Security Controls and Incident Response** (1.50h) | Security/Compliance | Config rules, auto-remediation — evidence |

---

## 🟡 Ưu tiên trung bình

| Course | Topic | Ghi chú |
|--------|-------|---------|
| **Auditing Your Security with AWS Trusted Advisor** 🧪 | Security / Cost | Best practice checks, security findings |
| **Getting Started with AWS Systems Manager** 🧪 | Operations | Patch management, SSM Agent, Run Command |
| **AWS Cloud Financial Management for Builders** (1.50h) | Cost / FinOps | Cost allocation, tagging strategy, Savings Plans |
| **Performing a Basic Audit of your AWS Environment** 🧪 | Security / Compliance | IAM Access Analyzer, Config, Trusted Advisor |
| **AWS SimuLearn: Core Security Concepts** 🧪 | Security | Hands-on security |
| **AWS SimuLearn: Cloud Economics** 🧪 | Cost | Cost optimization hands-on |
| **Amazon S3 Cost Optimization** | Cost / Storage | S3 storage classes, lifecycle policies |

---

## 🟢 Ưu tiên thấp

| Course | Ghi chú |
|--------|---------|
| **Deep Dive: EBS Cost Optimization** (0.30h) | Nhanh — đọc sau |
| **Deep Dive: EBS Performance Optimization** (1h) | gp3/io2 performance tuning |

---

## 📊 W6 Mental Model

```
[Auto Scaling Group + ALB]    ← High Availability
    │
[CloudWatch]                  ← Metrics, Logs, Alarms
[CloudTrail]                  ← API audit
[AWS Config]                  ← Compliance rules, auto-remediation
    │
[KMS]                         ← Encryption key management
[Trusted Advisor]             ← Security + cost best practices
[Systems Manager]             ← Operational management
    │
[Cloud Financial Management]  ← FinOps, cost allocation
[S3/EBS Optimization]         ← Storage cost + performance
```

**Câu hỏi QnA dự đoán W6:**
- CloudWatch vs CloudTrail — monitoring vs auditing?
- KMS CMK vs AWS Managed Key — khi nào dùng cái nào?
- Auto Scaling target tracking vs step scaling?
- S3 encryption options — SSE-S3 vs SSE-KMS vs SSE-C?
- AWS Config vs Trusted Advisor — khi nào dùng cái nào?
- Systems Manager vs direct SSH — trade-offs?
- Reserved Instances vs Savings Plans vs Spot?
