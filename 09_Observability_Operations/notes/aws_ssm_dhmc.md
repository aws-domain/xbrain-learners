# Systems Manager DHMC (Default Host Management Configuration) — Tự động hóa quản lý EC2 Node

## 📌 Tổng quan cốt lõi (Core Concepts)
*Giải thích súc tích về tính năng quản trị tự động cấp tài khoản của AWS Systems Manager (SSM).*
- **DHMC (Default Host Management Configuration):** Tính năng của AWS Systems Manager cho phép tự động cấu hình và quản lý Amazon EC2 instances thành các *Managed Nodes* mà không cần đính kèm IAM Instance Profile thủ công cho từng instance.
- **SSM Agent:** Phần mềm chạy ngầm trên EC2 để giao tiếp với Systems Manager Service. Cần phiên bản tối thiểu `3.2.582.0` (hoặc tối thiểu `3.2.532.0`) để hỗ trợ DHMC.
- **IMDSv2 (Instance Metadata Service Version 2):** Dịch vụ metadata cục bộ trên EC2 sử dụng cơ chế token-oriented session bảo mật. DHMC **bắt buộc** phải sử dụng IMDSv2.
- **Default IAM Role (`AWSSystemsManagerDefaultEC2InstanceManagementRole`):** IAM Role được tạo tự động hoặc thủ công để đính kèm policy `AmazonSSMManagedEC2InstanceDefaultPolicy`, cấp các quyền tối thiểu cho toàn bộ EC2 kết nối với SSM.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### 1. Luồng phân giải thông tin xác thực (Credential Resolution & Fallback Flow)
*Sơ đồ dưới đây mô tả cách SSM Agent trên EC2 quyết định sử dụng quyền hạn từ IAM Instance Profile truyền thống hay Fallback về DHMC.*

```
                  ┌──────────────────────────────┐
                  │      EC2 Launch / Start      │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
               ┌──────────────────────────────────┐
               │    SSM Agent checks credentials  │
               └──────────────┬───────────────────┘
                              │
             Is IAM Instance Profile attached?
              /                            \
            YES                            NO
            /                                \
  ┌──────────────────────┐         ┌──────────────────────────────┐
  │ Use attached Role    │         │ Fallback to DHMC             │
  │ (Must have SSM perms)│         │ (Checks IMDSv2 & DHMC status)│
  └──────────┬───────────┘         └──────────────┬───────────────┘
             │                                    │
             │                               Does DHMC Role exist?
             │                                /                \
             │                              YES                 NO
             │                              /                    \
             ▼                             ▼                      ▼
  ┌──────────────────────┐     ┌───────────────────────┐   ┌───────────────────────┐
  │   SSM Managed Node   │     │   SSM Managed Node    │   │  Unmanaged Instance   │
  │      (Success)       │     │  (Automatic via DHMC) │   │ (Error / Not showing) │
  └──────────────────────┘     └───────────────────────┘   └───────────────────────┘
```

### 2. Luồng kết nối mạng trong VPC Private Subnet (Network Connectivity Flow)
*Khi EC2 nằm ở subnet cô lập (Private Subnet), SSM Agent sử dụng DHMC credentials để giao tiếp an toàn thông qua PrivateLink (VPC Endpoints).*

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ VPC (Private Subnet)                                                         │
│                                                                              │
│   ┌──────────────┐         VPC Endpoints (PrivateLink)                       │
│   │ EC2 Instance │ ──────► ┌─────────────────────────────────────────────┐   │
│   │              │         │ ssm.<region>.amazonaws.com                  │   │
│   │ (SSM Agent   │         │ ssmmessages.<region>.amazonaws.com          │   │
│   │  uses DHMC)  │         │ ec2messages.<region>.amazonaws.com          │   │
│   └──────────────┘         └──────────────────────┬──────────────────────┘   │
└───────────────────────────────────────────────────┼──────────────────────────┘
                                                    │ (AWS Internal Network)
                                                    ▼
                                      ┌───────────────────────────┐
                                      │    AWS Systems Manager    │
                                      │     (Fleet Manager)       │
                                      └───────────────────────────┘
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | Traditional IAM Instance Profile | DHMC (Default Host Management) |
|---|---|---|
| **Phạm vi áp dụng (Scope)** | Từng instance đơn lẻ (Per-instance basis). | Cấp tài khoản và Region (Account & Region-wide). |
| **Độ phức tạp cấu hình** | Cao (Phải gán role vào Launch Template/CI-CD pipeline). | Thấp (Chỉ cần kích hoạt 1 lần duy nhất cho mỗi Region). |
| **Yêu cầu Agent & IMDS** | Mọi phiên bản SSM Agent; Hỗ trợ cả IMDSv1 & IMDSv2. | SSM Agent >= `3.2.582.0`; Chỉ hỗ trợ IMDSv2. |
| **Quy tắc đè cấu hình (Override)** | Đè hoàn toàn lên DHMC nếu được gắn vào EC2. | Bị đè (Bypass) bởi bất kỳ IAM Instance Profile nào gắn sẵn. |
| **Bảo mật và Quyền hạn** | Có thể gán thêm nhiều policy truy cập S3, RDS, DynamoDB... | Chỉ giới hạn trong các quyền vận hành cơ bản của SSM. |
| **Trường hợp sử dụng** | EC2 chuyên biệt cần truy cập các tài nguyên AWS khác. | Quản lý quy mô lớn (Fleet-wide) để Patching, Session Manager. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. Tự động hóa triển khai hạ tầng (Infrastructure as Code & CLI)
> [!IMPORTANT]
> Tuyệt đối tránh kích hoạt DHMC thủ công bằng tay (Click-ops) trên Console. Hãy sử dụng AWS CLI để tự động hóa cấu hình đồng nhất giữa các tài khoản và Region.

#### Bước A: Khởi tạo IAM Role phục vụ DHMC (`AWSSystemsManagerDefaultEC2InstanceManagementRole`)
Tạo file cấu hình Trust Relationship (`trust-policy.json`):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ssm.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

Chạy CLI để khởi tạo role và gán AWS Managed Policy chuyên dụng:
```bash
# Tạo IAM Role
aws iam create-role \
  --role-name AWSSystemsManagerDefaultEC2InstanceManagementRole \
  --path /service-role/ \
  --assume-role-policy-document file://trust-policy.json

# Đính kèm AWS Managed Policy chuyên dùng cho DHMC
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedEC2InstanceDefaultPolicy \
  --role-name AWSSystemsManagerDefaultEC2InstanceManagementRole
```

#### Bước B: Kích hoạt tính năng DHMC tại AWS Region chỉ định
```bash
aws ssm update-service-setting \
  --setting-id arn:aws:ssm:<REGION>:<ACCOUNT_ID>:servicesetting/ssm/managed-instance/default-ec2-instance-management-role \
  --setting-value service-role/AWSSystemsManagerDefaultEC2InstanceManagementRole
```

#### Bước C: Truy vấn kiểm tra cấu hình dịch vụ
```bash
aws ssm get-service-setting \
  --setting-id arn:aws:ssm:<REGION>:<ACCOUNT_ID>:servicesetting/ssm/managed-instance/default-ec2-instance-management-role
```

### 2. Tăng cường Bảo mật (Security & Least Privilege)
- **Áp dụng SCPs (Service Control Policies):** Ngăn chặn các IAM User hoặc Sub-accounts tắt tính năng DHMC bằng cách deny quyền `ssm:ResetServiceSetting` và `ssm:UpdateServiceSetting` đối với tài nguyên dịch vụ DHMC.
- **Bắt buộc Enforce IMDSv2:** Sử dụng AWS Config rules hoặc IAM policies để kiểm soát và chặn việc khởi tạo EC2 dùng IMDSv1.

### 3. Tối ưu hóa chi phí (Cost Optimization)
- Bản thân tính năng DHMC được AWS cung cấp hoàn toàn **miễn phí**.
- Sử dụng DHMC giúp tự động hóa quá trình vá lỗi (Patching) thông qua Patch Manager, giảm thiểu chi phí nhân sự vận hành hệ thống hạ tầng quy mô lớn lên tới hàng ngàn EC2 instances.

### 4. Giới hạn kỹ thuật cần nhớ (Important Limits)
- **Thư mục Credential Cục bộ:** DHMC lưu thông tin xác thực tại `/var/lib/amazon/ssm` (Linux) hoặc `C:\ProgramData\Amazon` (Windows). **Tuyệt đối không xóa** hoặc can thiệp thủ công vào các thư mục này, nếu không EC2 sẽ mất kết nối hoàn toàn với SSM.
- **Tính năng khu vực (Regional):** DHMC hoạt động theo từng Region riêng lẻ. Bạn phải kích hoạt DHMC trên từng Region có EC2 hoạt động.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)

- **Chọn DHMC khi:**
  - Bạn quản trị hệ thống hạ tầng phân tán lớn (Fleet-wide management), muốn tự động bật tính năng Session Manager (không dùng SSH key) và Patching cho mọi EC2 mới tạo mà không cần phải thay đổi mã nguồn Terraform của EC2 Launch Templates.
  - Các EC2 instances của bạn đóng vai trò Web/App Server thuần túy và không cần quyền hạn truy cập tài nguyên AWS khác.

- **Chọn Traditional IAM Instance Profile khi:**
  - EC2 instance của bạn cần tương tác trực tiếp với các tài nguyên AWS như đọc/ghi S3 Bucket, gửi tin nhắn vào SQS, đọc ghi DynamoDB table, v.v.
  - Instance của bạn buộc phải sử dụng phần mềm cũ chỉ tương thích với IMDSv1 hoặc phiên bản SSM Agent thấp hơn bản `3.2.532.0`.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [AWS Systems Manager - Managing EC2 instances automatically with DHMC](https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-default-host-management-configuration.html)
  - [AWS Systems Manager Quick Setup - DHMC for an organization](https://docs.aws.amazon.com/systems-manager/latest/userguide/quick-setup-default-host-management-configuration.html)
