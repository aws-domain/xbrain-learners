# Cloud Foundations & Architecture — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** AWS Cloud Practitioner Essentials, AWS Technical Essentials, AWS Solutions Architect - Fundamentals of Architecting on AWS

---

## 1. Cloud Computing Cơ Bản

### Cloud là gì?
- Cung cấp IT resources (compute, storage, database, networking...) qua internet theo mô hình **pay-as-you-go**.
- Không cần mua/quản lý hardware vật lý — AWS lo phần đó.

### 3 Mô hình triển khai
| Mô hình | Mô tả | Ví dụ |
|---------|-------|-------|
| **Cloud** | Toàn bộ trên cloud | Startup mới hoàn toàn trên AWS |
| **On-Premises** | Toàn bộ tại data center riêng | Ngân hàng, tổ chức tài chính |
| **Hybrid** | Kết hợp cloud + on-premises | Đang migrate, hoặc compliance yêu cầu |

### 3 Mô hình dịch vụ
| Model | AWS lo | Bạn lo | Ví dụ |
|-------|--------|--------|-------|
| **IaaS** | Hardware, network, virtualization | OS, runtime, app | EC2 |
| **PaaS** | Hardware + OS + runtime | App, data | Elastic Beanstalk |
| **SaaS** | Tất cả | Chỉ dùng | Gmail, Salesforce |

### Lợi ích chính của Cloud
- **Trade fixed expense for variable expense** — trả theo dùng, không mua trước
- **Economies of scale** — AWS mua hardware số lượng lớn → giá rẻ hơn
- **Stop guessing capacity** — scale up/down theo nhu cầu thực tế
- **Increase speed and agility** — deploy trong phút thay vì tuần
- **Go global in minutes** — AWS có Region trên toàn thế giới

---

## 2. AWS Global Infrastructure

### Regions
- Khu vực địa lý riêng biệt, chứa nhiều AZ.
- Mỗi Region **độc lập hoàn toàn** — data không tự động replicate sang Region khác.
- Chọn Region dựa trên: latency, compliance, pricing, service availability.

### Availability Zones (AZ)
- 1 hoặc nhiều data center vật lý trong 1 Region.
- Cách nhau đủ xa để tránh single point of failure, nhưng đủ gần để low-latency replication.
- **Best practice:** Deploy ở ít nhất 2 AZ để high availability.

### Edge Locations
- Điểm phân phối nội dung của **CloudFront** (CDN).
- Nhiều hơn số Region — đặt gần người dùng cuối để giảm latency.

---

## 3. AWS Well-Architected Framework — 6 Pillars

> Bị check mọi tuần — phải thuộc.

| Pillar | Mục tiêu | Ví dụ thực tế |
|--------|----------|---------------|
| **Operational Excellence** | Chạy và monitor hệ thống hiệu quả | CloudWatch, runbooks, IaC |
| **Security** | Bảo vệ data và hệ thống | IAM least privilege, encryption, MFA |
| **Reliability** | Hệ thống hoạt động đúng và recover được | Multi-AZ, backup, auto-scaling |
| **Performance Efficiency** | Dùng resource hiệu quả | Chọn đúng instance type, serverless |
| **Cost Optimization** | Tránh lãng phí | Reserved instances, right-sizing, S3 lifecycle |
| **Sustainability** | Giảm tác động môi trường | Tối ưu utilization, dùng managed services |

---

## 4. Kiến Trúc 3-Tier (Must-Know)

Pattern kiến trúc chuẩn cho web application:

```
Internet
    │
[Presentation Tier]  ← Load Balancer + Web Server (Public Subnet)
    │
[Application Tier]   ← App Server / Lambda (Private Subnet)
    │
[Data Tier]          ← RDS / DynamoDB (Isolated Subnet)
```

| Tier | Chứa gì | Subnet |
|------|---------|--------|
| Presentation | ALB, CloudFront, Static assets (S3) | Public |
| Application | EC2, Lambda, ECS | Private |
| Data | RDS, DynamoDB, ElastiCache | Isolated |

---

## 5. Shared Responsibility Model

> Câu hỏi hay gặp: "Ai chịu trách nhiệm về X?"

```
AWS chịu trách nhiệm:          Bạn chịu trách nhiệm:
- Physical hardware            - Data của bạn
- Network infrastructure       - IAM users & permissions
- Hypervisor                   - OS patching (EC2)
- Managed service security     - Application security
- Regions, AZs, Edge           - Encryption config
```

**Rule of thumb:**
- **"Security OF the cloud"** → AWS lo
- **"Security IN the cloud"** → Bạn lo

---

## 6. AWS Pricing Model

### 3 nguyên tắc pricing
1. **Pay for what you use** — theo giờ hoặc giây
2. **Pay less when you reserve** — Reserved Instances tiết kiệm 30–72%
3. **Pay less with more volume** — S3, data transfer giảm giá theo tier

### Các hình thức mua EC2
| Hình thức | Tiết kiệm | Dùng khi |
|-----------|-----------|----------|
| **On-Demand** | 0% | Dev/test, unpredictable workload |
| **Reserved (1–3 năm)** | 30–72% | Production, steady-state workload |
| **Savings Plans** | 30–66% | Flexible, commit theo $/giờ |
| **Spot** | 60–90% | Batch jobs, fault-tolerant workload |

---

## Quick Reference

**Q: Region và AZ khác gì nhau?**
A: Region là khu vực địa lý (ví dụ: ap-southeast-1 = Singapore). AZ là data center vật lý trong Region đó. 1 Region có ít nhất 3 AZ. Deploy ở nhiều AZ để high availability.

**Q: Well-Architected Framework có mấy pillar?**
A: 6 pillars — Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.

**Q: Shared Responsibility Model — AWS lo gì, mình lo gì?**
A: AWS lo "security OF the cloud" (hardware, network, hypervisor). Bạn lo "security IN the cloud" (data, IAM, OS patching, app security).

**Q: Kiến trúc 3-tier gồm những gì?**
A: Presentation tier (ALB, web server — public subnet), Application tier (EC2/Lambda — private subnet), Data tier (RDS/DynamoDB — isolated subnet).
