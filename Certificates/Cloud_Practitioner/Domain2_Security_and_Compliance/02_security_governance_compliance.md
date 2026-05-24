# Task 2.2 — Security, Governance, and Compliance

> **Exam weight:** Domain 2 = 30% of scored content

## AWS Compliance

### AWS Artifact
- **Cổng tự phục vụ** để truy cập compliance reports và agreements
- Cung cấp: SOC reports, PCI DSS, ISO certifications, HIPAA BAA...
- Miễn phí, truy cập qua AWS Console
- Dùng khi: cần chứng minh compliance với auditors

### Compliance Programs
AWS tuân thủ nhiều tiêu chuẩn quốc tế và ngành:
- **PCI DSS** — Thanh toán thẻ tín dụng
- **HIPAA** — Dữ liệu y tế (Mỹ)
- **SOC 1/2/3** — Kiểm soát nội bộ
- **ISO 27001** — Bảo mật thông tin
- **GDPR** — Bảo vệ dữ liệu (EU)

---

## Security Services

### Amazon Inspector
- **Tự động đánh giá bảo mật** cho EC2 instances và container images
- Phát hiện vulnerabilities trong OS và applications
- Tích hợp với AWS Security Hub

### AWS Security Hub
- **Trung tâm bảo mật tập trung** — aggregates findings từ nhiều services
- Tích hợp với: GuardDuty, Inspector, Macie, Firewall Manager
- Cung cấp security score và compliance checks

### Amazon GuardDuty
- **Threat detection service** — phát hiện mối đe dọa bằng ML
- Phân tích: VPC Flow Logs, CloudTrail, DNS logs
- Phát hiện: unauthorized access, cryptocurrency mining, data exfiltration
- Không cần cài agent, bật trong vài click

### AWS Shield
- **DDoS protection**
- **Shield Standard** — Miễn phí, tự động bảo vệ tất cả AWS customers
- **Shield Advanced** — Trả phí, bảo vệ nâng cao cho EC2, ELB, CloudFront, Route 53

---

## Encryption

### Encryption in Transit
- Bảo vệ data khi di chuyển qua network
- Sử dụng **TLS/SSL** (HTTPS)
- Ví dụ: HTTPS cho API calls, SSL cho database connections

### Encryption at Rest
- Bảo vệ data khi lưu trữ
- **AWS KMS (Key Management Service)** — quản lý encryption keys
- Hỗ trợ: S3, EBS, RDS, DynamoDB, Lambda environment variables

### AWS KMS
- Tạo và quản lý **Customer Master Keys (CMKs)**
- Tích hợp với hầu hết AWS services
- Hỗ trợ automatic key rotation

---

## Logging & Monitoring for Security

### AWS CloudTrail
- **Ghi lại tất cả API calls** trong AWS account
- Ai làm gì, khi nào, từ đâu
- Lưu logs vào S3
- Dùng cho: audit, compliance, security investigation

### Amazon CloudWatch
- **Monitoring và observability** cho AWS resources
- Metrics, logs, alarms, dashboards
- Dùng cho: performance monitoring, operational health

### AWS Config
- **Ghi lại configuration changes** của AWS resources
- Đánh giá compliance với rules
- Dùng cho: configuration audit, compliance reporting

### AWS Audit Manager
- **Tự động hóa evidence collection** cho audits
- Mapping controls với AWS usage
- Dùng cho: continuous compliance assessment

---

## Exam Tips

- AWS Artifact = nơi lấy compliance documents (không phải tool bảo mật)
- GuardDuty = threat detection (ML-based), không cần agent
- Inspector = vulnerability assessment cho EC2/containers
- CloudTrail = "ai làm gì" (API audit log)
- CloudWatch = "hệ thống đang như thế nào" (metrics/monitoring)
- Shield Standard = miễn phí, tự động; Shield Advanced = trả phí
