# Topic 02: Storage Troubleshooting — Khắc Phục Sự Cố S3 & EBS

## 📌 Tổng quan cốt lõi (Core Concepts)
- **Amazon S3 Authorization:** Phân quyền S3 là sự kết hợp phức tạp giữa IAM Policies, Bucket Policies, Access Control Lists (ACLs) và Block Public Access settings.
- **EBS Performance:** Hiệu năng của EBS phụ thuộc vào IOPS, Throughput và cơ chế tích lũy credit (Burst Balance đối với thế hệ gp2).
- **S3 Cross-Region Replication (CRR):** Cơ chế tự động sao chép bất đồng bộ (asynchronous replication) các objects giữa các buckets ở các AWS Regions khác nhau. Yêu cầu bắt buộc phải bật S3 Versioning trên cả Source và Destination buckets.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ luồng đánh giá quyền truy cập S3 (S3 Access Evaluation Flow)
```
[S3 Request: Get/Put Object]
            │
            ▼
 1. Block Public Access enabled? ───(Yes)──► [Block Public ACLs / Policies]
            │ (No)
            ▼
 2. Explicit Deny in Bucket Policy? ─(Yes)─► [Access Denied]
            │ (No)
            ▼
 3. Allowed in IAM or Bucket Policy? ─(No)─► [Access Denied]
            │ (Yes)
            ▼
 4. Object encrypted with KMS Key? ──(Yes)─► [Check KMS Key Policy for kms:Decrypt / kms:GenerateDataKey]
            │ (No / Allowed)
            ▼
     [Access Granted]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | EBS gp2 | EBS gp3 |
|---|---|---|
| **Cơ chế IOPS** | Tỷ lệ thuận với dung lượng (3 IOPS per GB). Nhỏ hơn 1TB phải dùng Burst Balance để đạt tối đa 3000 IOPS. | Cung cấp sẵn **3000 IOPS miễn phí** ở mọi dung lượng. Có thể mua thêm IOPS độc lập không cần tăng dung lượng đĩa. |
| **Giá cả** | Đắt hơn gp3 khoảng 20%. | Tiết kiệm chi phí hơn gp2, khuyên dùng cho mọi hệ thống. |
| **Cạm bẫy hiệu năng** | Dễ bị cạn kiệt Burst Balance dẫn tới IOPS tụt về baseline (rất thấp). | Hoạt động ổn định, không lo cạn kiệt burst credits. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. S3 Access Denied khi Upload / Download
*   **Nguyên nhân 1: Block Public Access:** Đang cố gắng tạo một public bucket/object bằng ACL nhưng Block Public Access ở cấp độ Account hoặc Bucket đang được bật (bảo vệ mặc định của AWS).
*   **Nguyên nhân 2: Bucket Policy hoặc IAM Policy bị cấu hình sai:** Thiếu các action quan trọng như `s3:PutObject` (cho phép upload) hoặc `s3:GetObject` (cho phép download).
*   **Nguyên nhân 3: Thiếu quyền KMS:** Objects được mã hóa bằng KMS Key (SSE-KMS), nhưng IAM Role của Client không có quyền `kms:Decrypt` (khi tải) hoặc `kms:GenerateDataKey` (khi upload).
*   **Cách kiểm tra và sửa đổi bằng AWS CLI:**
    *   *Kiểm tra cấu hình Block Public Access của Bucket:*
        ```bash
        aws s3api get-public-access-block --bucket my-secure-bucket
        ```
    *   *Tải file test để kiểm tra chi tiết mã lỗi:*
        ```bash
        aws s3 cp s3://my-secure-bucket/test-file.txt ./ --debug
        ```
        *(Tìm từ khóa `AccessDenied` trong debug trace để xác định API call bị chặn).*

### 2. EBS Volume bị đầy hoặc I/O chậm (Nghẽn Hiệu Năng gp2)
*   **Hiện tượng:** Ứng dụng chạy chậm đột biến, Disk I/O Queue Depth tăng cao, kiểm tra thấy metric `BurstBalance` của ổ gp2 trong CloudWatch chạm mức 0%.
*   **Cách kiểm tra bằng CLI hệ thống (truy cập qua SSM Session Manager):**
    *   *Kiểm tra dung lượng đĩa:*
        ```bash
        df -h
        # Tìm phân vùng bị 100% dung lượng
        ```
    *   *Kiểm tra I/O trực tiếp:*
        ```bash
        iostat -xz 1 10
        # Nếu %util gần 100%, đĩa đang bị nghẽn I/O nặng
        ```
*   **Giải pháp xử lý (Không tốn downtime):**
    *   Đổi trực tiếp loại đĩa từ `gp2` sang `gp3` qua AWS CLI/Console để tăng baseline IOPS lên 3000 ngay lập tức và tiết kiệm chi phí:
        ```bash
        aws ec2 modify-volume \
          --volume-id vol-0123456789abcdef0 \
          --volume-type gp3 \
          --iops 3000
        ```
    *   Sau khi modify đĩa thành công, tiến hành resize file system trên OS (ví dụ với ext4):
        ```bash
        sudo resize2fs /dev/xvda1
        ```

### 3. S3 Data không đồng bộ giữa các Regions (Replication Failures)
*   **Nguyên nhân 1: Versioning chưa được bật:** S3 Replication bắt buộc phải có Versioning được kích hoạt trên **cả Source và Destination buckets**.
*   **Nguyên nhân 2: IAM Role của Replication thiếu quyền:** IAM Role đảm nhận việc copy không có quyền đọc ở Source Bucket hoặc ghi ở Destination Bucket.
*   **Nguyên nhân 3: Khác biệt về Key Encryption:** Nếu source bucket dùng KMS để mã hóa, IAM Replication Role phải có quyền truy cập KMS Key ở region gốc và đích.
*   **Cách kiểm tra trạng thái replication bằng CLI:**
    *   *Kiểm tra trạng thái replication của một object cụ thể:*
        ```bash
        aws s3api head-object \
          --bucket my-source-bucket \
          --key data.json
        ```
        *(Xem giá trị `"ReplicationStatus": "PENDING"`, `"COMPLETED"`, hoặc `"FAILED"`).*

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **EBS gp3** thay vì **gp2** cho: 100% các dự án mới nhằm tối ưu chi phí và tăng hiệu năng mặc định (3000 IOPS).
- Chọn **EBS io2 (Provisioned IOPS)** khi: Chạy các database tải cực lớn (như Oracle, SAP, SQL Server) yêu cầu IOPS > 16,000 và độ trễ dưới 1 mili-giây.
- Chọn **S3 Versioning** khi: Cần bảo vệ dữ liệu trước các thao tác xóa nhầm, tấn công ransomware, hoặc bắt buộc phải cấu hình Cross-Region Replication (CRR).

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Troubleshoot Access Denied errors from Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-access-denied.html)
  - [Migrate from gp2 to gp3 EBS volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/migrate-to-gp3.html)
