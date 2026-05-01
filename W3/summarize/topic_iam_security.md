# IAM & Security — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** AWS Identity and Access Management - Architecture and Terminology, Introduction to AWS IAM (Lab), AWS Security Fundamentals Second Edition

---

## 1. IAM — Identity and Access Management

### IAM là gì?
- Service quản lý **ai** (authentication) được làm **gì** (authorization) với AWS resources.
- Global service — không gắn với Region cụ thể.
- **Free** — không tính phí riêng cho IAM.

### Các thành phần IAM

**Users** — đại diện cho người hoặc application cụ thể
- Có credentials riêng (password, access key)
- Mặc định không có quyền gì — phải gán policy

**Groups** — tập hợp Users
- Gán policy vào Group → tất cả User trong Group được thừa hưởng
- User có thể thuộc nhiều Group

**Roles** — identity tạm thời, không gắn với người cụ thể
- EC2, Lambda, ECS... assume Role để có quyền
- Cross-account access
- Không có long-term credentials — dùng temporary security tokens (STS)

**Policies** — document JSON định nghĩa permissions
- Gắn vào User, Group, hoặc Role
- **Effect:** Allow hoặc Deny
- **Action:** Hành động được phép (s3:GetObject, ec2:StartInstances...)
- **Resource:** ARN của resource áp dụng

### Nguyên tắc Least Privilege
> Chỉ cấp đúng quyền cần thiết, không hơn.

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```
Không cấp `s3:*` nếu chỉ cần đọc/ghi — tránh accidental delete.

### IAM Policy Evaluation
Khi có nhiều policy, AWS evaluate theo thứ tự:
1. **Explicit Deny** → luôn thắng, dù có Allow ở đâu
2. **Explicit Allow** → được phép
3. **Implicit Deny** → mặc định deny nếu không có Allow

---

## 2. Authentication vs Authorization

| | Authentication | Authorization |
|---|---|---|
| **Câu hỏi** | Bạn là ai? | Bạn được làm gì? |
| **AWS mechanism** | Username/password, Access Key, MFA | IAM Policy |
| **Ví dụ** | Login vào AWS Console | Có quyền tạo EC2 không? |

---

## 3. MFA — Multi-Factor Authentication

- Thêm lớp bảo vệ ngoài password.
- **Bắt buộc** cho root account và IAM users có quyền cao.
- Loại: Virtual MFA (Google Authenticator), Hardware MFA, U2F Security Key.

---

## 4. AWS Security Services

### KMS — Key Management Service
- Tạo và quản lý **encryption keys**.
- Tích hợp với hầu hết AWS services: S3, RDS, EBS, Lambda...
- **CMK (Customer Managed Key):** Bạn tạo và quản lý key
- **AWS Managed Key:** AWS tạo và quản lý thay bạn
- Mọi thao tác với key đều được **audit qua CloudTrail**

### CloudTrail
- **Ghi lại mọi API call** trong AWS account — ai làm gì, lúc nào, từ đâu.
- Dùng cho: security audit, compliance, troubleshooting.
- Log lưu vào S3, có thể query bằng Athena.
- **Bật mặc định** cho management events (90 ngày). Muốn lưu lâu hơn → tạo Trail.

### GuardDuty
- **Threat detection service** — tự động phát hiện suspicious activity.
- Phân tích: VPC Flow Logs, CloudTrail, DNS logs.
- Ví dụ phát hiện: EC2 communicate với known malicious IP, unusual API calls, crypto mining.
- Không cần cài agent — enable là chạy.

### AWS WAF — Web Application Firewall
- Bảo vệ web application khỏi common attacks: SQL injection, XSS, DDoS layer 7.
- Gắn vào: CloudFront, ALB, API Gateway.
- Tạo **rules** để allow/block/count requests dựa trên IP, header, body...

### AWS Shield
- Bảo vệ khỏi **DDoS attacks**.
- **Shield Standard:** Miễn phí, tự động bảo vệ tất cả AWS resources.
- **Shield Advanced:** Trả phí, bảo vệ nâng cao, 24/7 DDoS Response Team, cost protection.

### AWS Inspector
- **Vulnerability scanning** cho EC2 instances và container images.
- Tự động scan khi có CVE mới.
- Tích hợp với ECR để scan container images trước khi deploy.

---

## 5. Encryption

### Encryption at Rest
- Data được mã hóa khi lưu trữ.
- S3: SSE-S3, SSE-KMS, SSE-C
- EBS: encrypt volume khi tạo
- RDS: encrypt database khi tạo

### Encryption in Transit
- Data được mã hóa khi truyền qua network.
- HTTPS/TLS cho web traffic
- SSL/TLS cho database connections

---

## 6. Root Account vs IAM User

| | Root Account | IAM User |
|---|---|---|
| Quyền | Toàn bộ, không giới hạn | Chỉ những gì policy cho phép |
| Dùng cho | Setup ban đầu, billing | Công việc hàng ngày |
| Best practice | Bật MFA, không dùng hàng ngày | Tạo IAM user riêng cho mỗi người |

> **Rule:** Không bao giờ dùng root account cho daily tasks. Tạo IAM admin user thay thế.

---

## Quick Reference

**Q: IAM Role khác IAM User thế nào?**
A: User gắn với người/application cụ thể, có long-term credentials. Role là identity tạm thời — EC2/Lambda assume role để có quyền, dùng temporary tokens (STS), không có password hay access key cố định.

**Q: Explicit Deny và Implicit Deny khác gì?**
A: Explicit Deny là có policy viết rõ "Deny action X" — luôn thắng mọi Allow. Implicit Deny là không có policy nào Allow → mặc định bị deny. Explicit Deny nguy hiểm hơn vì không thể override bằng Allow.

**Q: CloudTrail vs CloudWatch khác gì?**
A: CloudTrail ghi lại API calls (ai làm gì với AWS resources). CloudWatch monitor metrics và logs của application/infrastructure (CPU, memory, Lambda duration...).

**Q: WAF bảo vệ ở layer nào?**
A: Layer 7 (Application layer) — bảo vệ khỏi SQL injection, XSS, bad bots. Shield bảo vệ ở layer 3/4 (Network/Transport) — chống DDoS volumetric attacks.
