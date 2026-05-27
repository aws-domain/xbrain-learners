# Topic 05: Security & Identity Troubleshooting — Khắc Phục Sự Cố IAM Instance Profile & S3 Public Exposure

## 📌 Tổng quan cốt lõi (Core Concepts)
- **IAM Instance Profiles:** Đóng vai trò là cầu nối (container) cho phép truyền IAM Role vào một Amazon EC2 Instance. Khi không có Instance Profile, EC2 không thể giả lập (assume) Role để nhận temporary security credentials.
- **Data Exposure Detection & Remediation:** Bảo vệ dữ liệu nhạy cảm là ưu tiên hàng đầu. Khi AWS Macie phát hiện dữ liệu nhạy cảm (PII, thẻ tín dụng) nằm trong public S3 buckets, ta cần xây dựng cơ chế tự động hóa ứng phó sự cố (Automated Incident Response) để cô lập ngay lập tức bucket đó.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ cơ chế gán Role cho EC2 thông qua Instance Profile
```
 [IAM Role: S3ReadOnly] ───(Gán vào)───► [IAM Instance Profile]
                                                 │
                                                 ▼ (Đính kèm vào)
                                        [EC2 Instance]
                                                 │
                                                 ▼ (Ứng dụng chạy trên EC2 gọi S3)
                                      [IMDSv2 - Metadata Service]
                                    http://169.254.169.254/latest/meta-data/
                                                 │
                                                 ▼ (Trả về Temporary Credentials)
                                           [Access Granted]
```

### Sơ đồ luồng tự động cô lập S3 khi Macie phát hiện dữ liệu nhạy cảm
```
[S3 Public Bucket] ──► [Amazon Macie Scan]
                             │
                             ▼ (Phát hiện dữ liệu nhạy cảm PII)
                    [Amazon EventBridge Event]
                             │
                             ▼ (Kích hoạt tự động)
                     [AWS Lambda Function]
                             │
                             ▼ (Thực thi khắc phục)
             [Sửa Bucket Policy thành Private / Enable Block Public Access]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | IAM Role cho EC2 (via Instance Profile) | IAM Role cho Lambda (Execution Role) |
|---|---|---|
| **Cơ chế gán** | Phải bọc trong **Instance Profile** trước khi gán cho EC2. | Gán trực tiếp vào hàm Lambda khi cấu hình. |
| **Cơ chế cấp quyền** | Cấp thông qua metadata service của instance (IMDSv2). | Cấp trực tiếp vào biến môi trường thực thi của Lambda container. |
| **Trường hợp sử dụng** | Ứng dụng chạy trên EC2 cần quyền truy cập AWS services. | Logic xử lý trong hàm Lambda cần quyền gọi AWS APIs. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. IAM Role không hoạt động trên EC2 (Lỗi thiếu Instance Profile)
*   **Hiện tượng:** Ứng dụng chạy trên EC2 khi gọi AWS SDK (ví dụ `aws s3 ls`) nhận lỗi `Unable to locate credentials`. Dù bạn đã tạo IAM Role đầy đủ quyền.
*   **Nguyên nhân:** Khi tạo IAM Role bằng CloudFormation/CLI/Terraform, bạn chỉ tạo ra Role chứ **chưa tạo Instance Profile** và bọc Role đó vào để gán cho EC2. Khi dùng AWS Console, AWS tự động tạo Instance Profile ngầm nên ta ít khi nhận ra.
*   **Cách kiểm tra và xử lý bằng CLI:**
    *   *Kiểm tra EC2 có được gán Instance Profile nào không:*
        ```bash
        aws ec2 describe-instances \
          --instance-ids i-0123456789abcdef0 \
          --query "Reservations[*].Instances[*].IamInstanceProfile"
        ```
    *   *Các bước tạo và gán Instance Profile bằng CLI:*
        ```bash
        # 1. Tạo Instance Profile
        aws iam create-instance-profile --instance-profile-name MyEC2Profile
        
        # 2. Add Role vào Instance Profile
        aws iam add-role-to-instance-profile \
          --instance-profile-name MyEC2Profile \
          --role-name MyS3AccessRole
          
        # 3. Gán Instance Profile cho EC2 Instance đang chạy
        aws ec2 associate-iam-instance-profile \
          --instance-id i-0123456789abcdef0 \
          --iam-instance-profile Name=MyEC2Profile
        ```
    *   *Kiểm tra credential từ bên trong EC2 qua SSM:*
        ```bash
        curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
        ```
        *(Đảm bảo IMDSv2 trả về tên Role chính xác).*

### 2. Macie phát hiện dữ liệu nhạy cảm trong S3 Public Bucket
*   **Tình huống:** Amazon Macie quét và phát hiện ra một S3 bucket cấu hình Public chứa các file nhạy cảm (ví dụ file khách hàng chứa số điện thoại, CMND). Hệ thống cần hành động ngay lập tức để giảm thiểu rủi ro (Data Leakage).
*   **Giải pháp ứng phó sự cố tự động (DevOps Automated Remediation):**
    1.  **Macie** tạo một Finding dưới dạng JSON gửi sang **Amazon EventBridge**.
    2.  **EventBridge Rule** bắt sự kiện (`Macie Finding`) và kích hoạt một hàm **AWS Lambda**.
    3.  **Hàm Lambda** lập tức thực thi tắt tính năng Public và tháo Bucket Policy nguy hại.
*   **Cách viết Policy/Lệnh Lambda khắc phục tự động (CLI/API):**
    *   *Lambda tắt Block Public Access hoàn toàn cho Bucket:*
        ```python
        import boto3
        s3 = boto3.client('s3')
        
        def lambda_handler(event, context):
            bucket_name = event['detail']['resourcesAffected']['s3Bucket']['name']
            
            # Thực thi chặn Public Access lập tức
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            print(f"Secured bucket {bucket_name} successfully.")
        ```

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **IMDSv2** thay vì **IMDSv1** cho: 100% các EC2 instance mới nhằm chống lại các cuộc tấn công SSRF (Server-Side Request Forgery) bằng cách bắt buộc sử dụng cơ chế token-based session.
- Chọn **Amazon Macie** khi: Cần quét tự động liên tục để phát hiện dữ liệu PII/tài chính nhạy cảm trong hàng ngàn S3 buckets trên quy mô lớn.
- Chọn **AWS Config Rules** khi: Cần giám sát trạng thái cấu hình tĩnh (ví dụ: phát hiện và tự động chặn bất kỳ bucket nào vừa bị chuyển sang Public một cách bất thường).

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Using IAM instance profiles to grant EC2 permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html)
  - [Automating remediation of Macie findings using EventBridge](https://docs.aws.amazon.com/macie/latest/user/findings-monitor-eventbridge.html)
