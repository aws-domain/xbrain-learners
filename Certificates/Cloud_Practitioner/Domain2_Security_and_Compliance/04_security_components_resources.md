# Task 2.4 — Security Components and Resources

> **Exam weight:** Domain 2 = 30% of scored content

## Network Security Services

### AWS WAF (Web Application Firewall)
- Bảo vệ web applications khỏi **common web exploits**
- Lọc HTTP/HTTPS requests dựa trên rules
- Bảo vệ khỏi: SQL injection, XSS, bad bots
- Triển khai trên: CloudFront, ALB, API Gateway, AppSync

### AWS Firewall Manager
- **Quản lý tập trung** các firewall rules trên nhiều accounts và resources
- Tự động áp dụng WAF rules, Shield Advanced, Security Groups
- Dùng với AWS Organizations

### Amazon GuardDuty
- **Intelligent threat detection** sử dụng ML
- Phân tích: VPC Flow Logs, CloudTrail Events, DNS Logs
- Phát hiện: compromised instances, reconnaissance, data exfiltration
- Không cần cài agent, không ảnh hưởng performance

### AWS Shield
| | Shield Standard | Shield Advanced |
|---|---|---|
| **Giá** | Miễn phí | ~$3,000/tháng |
| **Bảo vệ** | Layer 3/4 DDoS | Layer 3/4/7 DDoS |
| **Resources** | Tất cả | EC2, ELB, CloudFront, Route 53, Global Accelerator |
| **Support** | Không | 24/7 DDoS Response Team |
| **Cost protection** | Không | Có (refund nếu scale do DDoS) |

---

## Data Protection Services

### Amazon Macie
- Dùng **ML để phát hiện sensitive data** trong S3
- Tự động phân loại: PII, financial data, credentials
- Cảnh báo khi data được expose không đúng cách

### AWS KMS (Key Management Service)
- Tạo và quản lý **cryptographic keys**
- Tích hợp với hầu hết AWS services
- **Customer Managed Keys (CMK)** — bạn kiểm soát hoàn toàn
- **AWS Managed Keys** — AWS quản lý thay bạn
- Hỗ trợ automatic key rotation (hàng năm)

### AWS Certificate Manager (ACM)
- Provision, manage, deploy **SSL/TLS certificates**
- Miễn phí cho certificates dùng với AWS services
- Auto-renewal

---

## Security Information Resources

### AWS Knowledge Center
- FAQ và hướng dẫn giải quyết vấn đề phổ biến
- URL: aws.amazon.com/premiumsupport/knowledge-center

### AWS Security Center
- Tổng hợp thông tin bảo mật, best practices, whitepapers
- URL: aws.amazon.com/security

### AWS Security Blog
- Cập nhật về security features, best practices, case studies
- URL: aws.amazon.com/blogs/security

---

## AWS Trusted Advisor

- **Công cụ tư vấn** kiểm tra AWS environment theo 5 categories:
  1. **Cost Optimization** — Tìm resources lãng phí
  2. **Performance** — Cải thiện hiệu suất
  3. **Security** — Phát hiện security gaps
  4. **Fault Tolerance** — Tăng độ tin cậy
  5. **Service Limits** — Kiểm tra giới hạn service

- **Free checks** — Có sẵn cho tất cả accounts
- **Full checks** — Cần Business hoặc Enterprise Support plan

### Security checks của Trusted Advisor:
- S3 bucket permissions (public access)
- Security groups với unrestricted access
- IAM use (root account usage, MFA)
- EBS public snapshots
- RDS public snapshots

---

## AWS Marketplace Security Products

- Marketplace cung cấp **third-party security solutions**
- Categories: Firewalls, IDS/IPS, Endpoint protection, SIEM
- Ví dụ: Palo Alto, Fortinet, Trend Micro, Splunk
- Billing tích hợp vào AWS bill

---

## Exam Tips

- WAF = bảo vệ web app (Layer 7); Shield = bảo vệ DDoS (Layer 3/4)
- GuardDuty = threat detection, không cần agent
- Macie = tìm sensitive data trong S3
- Trusted Advisor security checks miễn phí cho tất cả accounts
- AWS Marketplace = mua third-party security tools, billing qua AWS
- KMS = quản lý encryption keys, tích hợp với hầu hết services
