# Database HA & Disaster Recovery — Projects Thực Hành

Danh sách các project có sẵn architecture diagram để học và kiểm nghiệm High Availability (HA) và Disaster Recovery (DR) cho database trên AWS.

---

## Khái niệm cốt lõi cần nắm trước

| Khái niệm | Giải thích |
|-----------|------------|
| **RTO** (Recovery Time Objective) | Thời gian tối đa chấp nhận được để khôi phục hệ thống sau sự cố |
| **RPO** (Recovery Point Objective) | Lượng dữ liệu tối đa có thể mất (tính theo thời gian) |
| **Multi-AZ** | Deploy DB ở nhiều Availability Zone trong 1 Region → HA |
| **Cross-Region** | Replicate DB sang Region khác → DR |
| **Failover** | Chuyển traffic từ primary sang standby khi primary fail |
| **Failback** | Đưa traffic trở lại primary sau khi primary phục hồi |

### 4 DR Strategies (từ rẻ → đắt, chậm → nhanh)

1. **Backup & Restore** — RPO: giờ, RTO: 24h+
2. **Pilot Light** — RPO: phút, RTO: 10 phút - vài giờ
3. **Warm Standby** — RPO: giây, RTO: phút
4. **Active-Active (Multi-Site)** — RPO: ~0, RTO: ~0

---

## 🏆 Projects Có Architecture Diagram + Code Deploy Được

### 1. Disaster Recovery on AWS Workshop

- **URL:** https://disaster-recovery.workshop.aws/
- **Architecture:** ✅ Diagram cho mỗi lab
- **Database labs:**
  - [Aurora Global Database](https://disaster-recovery.workshop.aws/en/labs/advanced/aurora-global-database.html) — cross-region replication + failover
  - [RDS Multi-AZ](https://disaster-recovery.workshop.aws/en/services/databases/rds.html) — in-region HA failover
  - [DynamoDB](https://disaster-recovery.workshop.aws/en/services/databases/dynamodb.html) — Point-in-time recovery, Global Tables
- **Học được:** Triển khai 4 DR strategies, monitor replication lag với CloudWatch, thực hành failover thật
- **Chi phí ước tính:** Thấp nếu tear down ngay sau lab

---

### 2. Guidance for Disaster Recovery Using Amazon Aurora

- **URL:** https://aws.amazon.com/solutions/guidance/disaster-recovery-using-amazon-aurora/
- **Architecture PDF:** https://d1.awsstatic.com/solutions/guidance/architecture-diagrams/disaster-recovery-using-amazon-aurora.pdf
- **GitHub:** https://github.com/aws-solutions-library-samples/guidance-for-disaster-recovery-using-amazon-aurora
- **Architecture:** ✅ Diagram chi tiết (Aurora Global Database cross-region)
- **Học được:**
  - Aurora Global Database replication mechanism
  - Cross-region failover automation
  - AWS Backup integration cho Aurora
  - So sánh các DR option cho Aurora (Global DB vs backup/restore vs snapshot copy)
- **Deploy:** CloudFormation templates có sẵn trong repo

---

### 3. Designing Resilient Applications with Amazon Aurora and RDS Proxy

- **URL:** https://aws.amazon.com/solutions/guidance/designing-resilient-applications-with-amazon-aurora-and-amazon-rds-proxy/
- **Docs:** https://docs.aws.amazon.com/solutions/designing-resilient-applications-with-amazon-aurora-and-amazon-rds-proxy/
- **Architecture:** ✅
- **Học được:**
  - Near-zero RPO pattern
  - RDS Proxy giảm failover downtime (connection pooling, pinning)
  - Persistent message queue (SQS) giữ data an toàn trong lúc failover
  - Lambda + Aurora + RDS Proxy integration
- **Deploy:** Code + template sẵn

---

### 4. Aurora PostgreSQL Fast Failover Demo

- **GitHub:** https://github.com/aws-samples/amazon-aurora-postgresql-fast-failover-demo
- **Architecture:** ✅ Diagram trong README
- **Học được:**
  - In-region HA: Aurora Multi-AZ automatic failover
  - Cross-region DR: Aurora Global Database failover
  - Lambda canary health check (scan mỗi 10 giây, trigger failover sau 30 giây fail liên tục)
  - Route53 DNS failover routing
  - RDS Proxy connection management during failover
- **Deploy:** CDK/CloudFormation
- **Đặc biệt hay:** Demo rõ ràng cách detect failure + automated response

---

### 5. Cross-Region DR Orchestrator Framework

- **GitHub:** https://github.com/aws-samples/aws-cross-region-dr-databases
- **Architecture:** ✅
- **Học được:**
  - Automated cross-region failover AND failback (cả 2 chiều)
  - Manifest-driven: cấu hình DR cho nhiều DB cùng lúc
  - Hỗ trợ nhiều engine: RDS, Aurora, DynamoDB Global Tables, ElastiCache
  - Step Functions orchestration
  - Single-click DR trigger
- **Deploy:** CloudFormation (primary: us-east-1, secondary: us-west-2)
- **Đặc biệt hay:** Framework tái sử dụng được, không chỉ demo 1 lần

---

### 6. Cross-Region Failover, Graceful Failback and Observability

- **GitHub:** https://github.com/aws-solutions-library-samples/guidance-for-crossregion-failover-and-graceful-failback-and-observability-on-aws
- **Architecture:** ✅
- **Học được:**
  - Full three-tier app: React frontend + Lambda API + Aurora Global DB
  - Graceful failback (không mất data khi chuyển về primary)
  - Observability during DR events (CloudWatch, dashboards)
  - End-to-end DR cho cả application stack, không chỉ database
- **Deploy:** Full stack deployable
- **Đặc biệt hay:** Thực tế nhất — DR cho toàn bộ app, không chỉ DB đơn lẻ

---

## 📚 Tài Liệu Đọc Hiểu Trước Khi Lab

| Tài liệu | URL | Ghi chú |
|-----------|-----|---------|
| DR Strategy for Databases on AWS | https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-database-disaster-recovery/welcome.html | Prescriptive Guidance chính thức, đọc đầu tiên |
| RDS Reference Architectures | https://github.com/aws-samples/aws-dbs-refarch-rdbms | Architecture patterns cho RDBMS trên AWS |
| AWS Blog: Purpose-built Database Recovery | https://aws.amazon.com/blogs/database/aws-purpose-built-database-recovery-a-guide-to-business-continuity-and-disaster-recovery-strategies/ | Blog tổng hợp DR cho tất cả DB engines |
| Automate DR for Relational Databases (PDF) | https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/automate-dr-solution-relational-database/automate-dr-solution-relational-database.pdf | Step Functions + Aurora automation |

---

## 🗺️ Lộ Trình Học Đề Xuất

```text
Bước 1: Đọc DR Strategy Prescriptive Guidance
         → Hiểu RTO/RPO, 4 DR tiers, cách chọn DB phù hợp
         │
Bước 2: DR on AWS Workshop — Lab Aurora Global Database
         → Deploy Aurora cross-region, test failover thủ công
         │
Bước 3: Aurora PostgreSQL Fast Failover Demo
         → Hiểu automated failover detection (Lambda canary + Route53)
         │
Bước 4: Cross-Region DR Orchestrator Framework
         → Automated failover/failback cho nhiều DB engines
         │
Bước 5: Cross-Region Failover + Observability (Full Stack)
         → DR cho toàn bộ three-tier app + monitoring
```

---

## ⚠️ Lưu Ý Chi Phí

- Aurora Global Database: tính phí cả 2 Region (primary + secondary)
- Cross-region data transfer có phí
- **Luôn tear down sau khi lab xong** — xóa CloudFormation stacks ở CẢ HAI Regions
- Dùng `aws cloudformation delete-stack` hoặc console để cleanup
- Kiểm tra RDS snapshots còn sót (snapshot cũng tốn phí storage)
