# W6 — Course Mapping & Learning Priority

> **Dates:** 18 May - 22 May | Advanced Concepts
> **Dựa trên:** Syllabus chính thức
> ⚠️ Chưa có project announcement chính thức — cập nhật khi có.

---

## � Danh sách courses theo ngày

| Course | Ngày | Thời lượng |
|--------|------|-----------|
| AWS SimuLearn: Auto-Healing and Scaling Applications 🧪 | Mon | 1h |
| AWS SimuLearn: Highly Available Web Applications 🧪 | Mon | 1h |
| Amazon Simple Storage Service (Amazon S3) Cost Optimization | Mon | 1h |
| Deep Dive: Amazon Elastic Block Store (Amazon EBS) Cost Optimization | Mon | 0.30h |
| AWS SimuLearn: Cloud Economics 🧪 | Mon | 1h |
| AWS Storage Gateway Deep Dive: Volume Gateway | Mon | 1.15h |
| AWS Storage Gateway Deep Dive: Amazon S3 File Gateway | Tue | 1h |
| AWS Backup Primer | Tue | 1.10h |
| Amazon CloudWatch Getting Started | Tue | 1h |
| AWS Organizations Getting Started | Tue | 1h |
| Securing and Protecting Your Data in Amazon Simple Storage Service | Tue | 1.40h |
| Protecting Your Instance with Security Groups | Tue | 1h |
| AWS Security Best Practices: Monitoring and Alerting | Wed | 2h |
| Introduction to the AWS Cloud Adoption Framework (CAF) | Wed | 1h |
| AWS SimuLearn: Core Security Concepts 🧪 | Wed | 1h |
| Performing a Basic Audit of your AWS Environment | Wed | 1h |
| Introduction to AWS Key Management Service | Wed | 1h |
| AWS SimuLearn: Design Modern Data Architectures with Agentic AI 🧪 | Wed | 1h |

---

## 🔴 Ưu tiên cao nhất

| Course | Topic | Tại sao ưu tiên |
|--------|-------|-----------------|
| **AWS SimuLearn: Auto-Healing and Scaling Applications** 🧪 | Compute / HA | ASG + ALB + health checks — evidence |
| **AWS SimuLearn: Highly Available Web Applications** 🧪 | Compute / HA | Multi-AZ ALB + ASG — diagram |
| **Amazon CloudWatch Getting Started** | Observability | Metrics, Logs, Alarms — monitoring evidence |
| **AWS Security Best Practices: Monitoring and Alerting** (2h) | Security | CloudWatch + CloudTrail + GuardDuty integration |
| **Introduction to AWS Key Management Service** | Security | KMS key types, key policies, envelope encryption |
| **Protecting Your Instance with Security Groups** | Security / Networking | SG deep dive — review trước QnA |

---

## 🟡 Ưu tiên trung bình

| Course | Topic | Ghi chú |
|--------|-------|---------|
| **Securing and Protecting Your Data in Amazon S3** (1.40h) | Security / Storage | S3 encryption, bucket policies, access points |
| **Performing a Basic Audit of your AWS Environment** | Security / Compliance | IAM Access Analyzer, Config, Trusted Advisor |
| **AWS SimuLearn: Core Security Concepts** 🧪 | Security | Hands-on security |
| **AWS SimuLearn: Cloud Economics** 🧪 | Cost | Cost optimization hands-on |
| **AWS SimuLearn: Design Modern Data Architectures with Agentic AI** 🧪 | AI / Data | Agentic AI + data architecture |
| **Amazon S3 Cost Optimization** | Cost / Storage | S3 storage classes, lifecycle policies |
| **AWS Organizations Getting Started** | Governance | Multi-account management |

---

## 🟢 Ưu tiên thấp

| Course | Ghi chú |
|--------|---------|
| **AWS Storage Gateway Deep Dive: Volume Gateway** | Hybrid storage — niche |
| **AWS Storage Gateway Deep Dive: S3 File Gateway** | Hybrid storage — niche |
| **AWS Backup Primer** | Backup strategy |
| **Introduction to AWS Cloud Adoption Framework (CAF)** | Framework overview |
| **Deep Dive: EBS Cost Optimization** (0.30h) | Nhanh — đọc sau |

---

## 📊 W6 Mental Model

```
[Auto Scaling Group + ALB]    ← High Availability
    │
[CloudWatch]                  ← Metrics, Logs, Alarms
[CloudTrail]                  ← API audit
[GuardDuty]                   ← Threat detection
    │
[KMS]                         ← Encryption key management
[S3 Security]                 ← Bucket policies, encryption
[Security Groups]             ← Instance-level firewall
    │
[AWS Organizations]           ← Multi-account governance
[Cloud Adoption Framework]    ← Migration strategy
```

**Câu hỏi QnA dự đoán W6:**
- CloudWatch vs CloudTrail — monitoring vs auditing?
- KMS CMK vs AWS Managed Key — khi nào dùng cái nào?
- Auto Scaling target tracking vs step scaling?
- S3 encryption options — SSE-S3 vs SSE-KMS vs SSE-C?
- AWS Organizations — OU, SCP là gì?
- CAF 6 perspectives là gì?
