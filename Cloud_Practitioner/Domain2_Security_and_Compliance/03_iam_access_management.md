# Task 2.3 — AWS Identity and Access Management (IAM)

> **Exam weight:** Domain 2 = 30% of scored content

## IAM Overview

**AWS IAM** cho phép quản lý **ai** (authentication) có thể làm **gì** (authorization) trên AWS resources.

- **Miễn phí** — không tính phí riêng cho IAM
- **Global service** — không gắn với Region cụ thể
- Áp dụng **Principle of Least Privilege** — chỉ cấp quyền tối thiểu cần thiết

---

## IAM Components

### Root User
- Tài khoản được tạo khi đăng ký AWS
- Có **toàn quyền** trên tất cả AWS services và resources
- **Không nên dùng cho công việc hàng ngày**
- Chỉ dùng cho các tác vụ đặc biệt:
  - Thay đổi account settings
  - Đóng AWS account
  - Thay đổi AWS Support plan
  - Restore IAM admin permissions

### IAM Users
- Đại diện cho **người hoặc ứng dụng** cụ thể
- Có username/password (console) hoặc access keys (programmatic)
- Mặc định không có quyền gì

### IAM Groups
- Tập hợp các IAM users
- Gán policies cho group → tất cả users trong group thừa hưởng
- Không thể lồng groups vào nhau
- Một user có thể thuộc nhiều groups

### IAM Roles
- Tập hợp permissions, **không gắn với user cụ thể**
- Được **assume** (đảm nhận) tạm thời bởi: users, services, applications
- Dùng cho: EC2 instance cần truy cập S3, cross-account access, federated users
- **Không có long-term credentials** (access keys)

### IAM Policies
- **JSON document** định nghĩa permissions
- Gắn vào users, groups, hoặc roles
- **Managed Policies** — AWS tạo sẵn hoặc customer tạo, có thể tái sử dụng
- **Inline Policies** — Gắn trực tiếp vào một entity, không tái sử dụng được

---

## Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

| Element | Mô tả |
|---------|-------|
| **Effect** | Allow hoặc Deny |
| **Action** | AWS API action (ví dụ: s3:GetObject) |
| **Resource** | ARN của resource áp dụng |
| **Condition** | Điều kiện tùy chọn |

> **Deny luôn thắng Allow** khi có conflict.

---

## Authentication Methods

### Multi-Factor Authentication (MFA)
- Thêm lớp bảo mật thứ hai ngoài password
- **Bắt buộc** cho root user (best practice)
- Loại: Virtual MFA (Google Authenticator), Hardware MFA, U2F Security Key

### Access Keys
- Dùng cho **programmatic access** (CLI, SDK, API)
- Gồm: Access Key ID + Secret Access Key
- **Không bao giờ** hardcode trong code
- Lưu trữ an toàn với **AWS Secrets Manager** hoặc **AWS Systems Manager Parameter Store**

### Password Policies
- Đặt yêu cầu độ phức tạp password cho IAM users
- Cấu hình: độ dài tối thiểu, ký tự đặc biệt, expiration, reuse prevention

---

## AWS IAM Identity Center (SSO)

- Trước đây gọi là **AWS Single Sign-On (SSO)**
- Quản lý access tập trung cho **nhiều AWS accounts** và applications
- Tích hợp với: Active Directory, Okta, Azure AD
- **Federated identity** — dùng identity provider bên ngoài

---

## Cross-Account Access

- Dùng **IAM Roles** để cho phép users từ account A truy cập resources ở account B
- Không cần tạo user mới ở account B
- Quy trình: Trust policy → Assume role → Temporary credentials

---

## AWS Secrets Manager

- Lưu trữ và rotate **secrets** (passwords, API keys, database credentials)
- Tự động rotate secrets theo lịch
- Tích hợp với RDS, Redshift, DocumentDB

---

## Exam Tips

- Root user = không dùng hàng ngày, bảo vệ bằng MFA
- IAM Roles = best practice cho EC2 truy cập AWS services (không dùng access keys)
- Deny > Allow trong policy evaluation
- IAM Identity Center = quản lý SSO cho nhiều accounts
- Principle of Least Privilege = chỉ cấp quyền tối thiểu cần thiết
- Access keys = programmatic access, không hardcode trong code
