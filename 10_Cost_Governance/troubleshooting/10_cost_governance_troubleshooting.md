# Topic 10: Cost Governance Troubleshooting — Kiểm Soát Chi Phí & Tài Nguyên Mồ Côi (Orphaned Resources)

## 📌 Tổng quan cốt lõi (Core Concepts)
- **Cost Allocation Tags:** Thẻ tag đính kèm tài nguyên AWS để phân loại hóa đơn (ví dụ theo `Project`, `Environment`). Thẻ này bắt buộc phải được kích hoạt thủ công trong Billing Console thì mới bắt đầu xuất hiện trong Cost Explorer.
- **Orphaned Resources:** Là các tài nguyên "mồ côi" không còn được liên kết với máy chủ đang hoạt động nhưng vẫn âm thầm tích lũy chi phí hàng giờ (ví dụ: EBS Volumes chưa mount, Elastic IPs bị bỏ quên).
- **Cost Anomalies & Security Threats:** Hóa đơn tăng đột biến bất thường thường là dấu hiệu của việc rò rỉ bảo mật (ví dụ: Hacker chiếm quyền AWS Account để đào coin bằng hàng loạt EC2 GPU công suất lớn).

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ luồng phát hiện và tự động dọn dẹp tài nguyên mồ côi (Orphaned Resources Cleanup)
```
  [AWS Resources Inventory]
              │
              ▼
    [AWS Config Rules Scan]
              ├──────────────────────────┐
              ▼ (Phát hiện Volume Unused)  ▼ (Phát hiện EIP Unattached)
    [volume-unused-check]        [eip-attached]
              │                          │
              └─────────────┬────────────┘
                            │ (Tạo non-compliant event)
                            ▼
                [Amazon EventBridge Rule]
                            │
                            ▼ (Trigger Lambda)
                  [AWS Lambda Cleanup]
                            │
                            ├──► Xóa Volume mồ côi (Tạo Snapshot dự phòng trước)
                            └── Giải phóng Elastic IP về Pool của AWS
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tài nguyên Mồ Côi | Cơ chế tính phí khi "mồ côi" | Cách phòng chống |
|---|---|---|
| **EBS Volume (Unattached)** | Tính phí nguyên vẹn theo GB/tháng tương tự như lúc đang chạy. | Sử dụng AWS Config Rule `volume-unused-check` để phát hiện. |
| **Elastic IP (Unattached)** | **Bị tính phí phạt theo giờ** nếu không được gán vào EC2 instance nào đang chạy (AWS phạt để thu hồi tài nguyên IP quý hiếm). | Sử dụng AWS Config Rule `eip-attached` để tự động giải phóng. |
| **NAT Gateway (Idle)** | Tính phí theo giờ giữ cổng tĩnh (dù có truyền nhận byte nào hay không). | Tự động tắt NAT Gateway ngoài giờ làm việc ở môi trường Dev/Test. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. Hóa đơn tăng đột biến (Phát hiện Crypto-Mining)
*   **Hiện tượng:** Hóa đơn AWS tăng vọt từ $100/tháng lên $10,000/tháng chỉ trong vài ngày.
*   **Nguyên nhân:** Khóa AWS Access Key bị rò rỉ lên GitHub công cộng. Hacker sử dụng API để tự động khởi chạy hàng chục EC2 GPU dòng lớn (như `g4dn.metal`) ở các Region xa lạ (như `us-east-2`, `eu-west-1`) để chạy tool đào coin.
*   **Cách kiểm tra và xử lý khẩn cấp:**
    1.  **Kiểm tra AWS GuardDuty:**
        *   GuardDuty sẽ phát hiện và gắn nhãn các cảnh báo dạng: `CryptoCurrency:EC2/BitcoinTool.B!gdn` (phát hiện hành vi đào coin dựa trên kết nối mạng).
    2.  **Sử dụng AWS Cost Anomaly Detection:**
        *   Thiết lập cảnh báo tự động gửi email/Slack ngay khi chi phí thực tế vượt ngưỡng dự báo hàng ngày.
    3.  **Quy trình cô lập và xử lý sự cố (Incident Response Playbook):**
        *   *Thu hồi Access Key bị lộ lập tức:*
            ```bash
            aws iam update-access-key \
              --access-key-id AKIAIOSFODNN7EXAMPLE \
              --status Inactive \
              --user-name compromise-user
            ```
        *   *Tìm và xóa toàn bộ instances đào coin ở mọi region:*
            ```bash
            # Quét tìm các instance đang chạy có công suất lớn
            aws ec2 describe-instances \
              --region us-east-2 \
              --filters "Name=instance-state-name,Values=running" \
              --query "Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType}"
            ```

### 2. Tài nguyên mồ côi âm thầm tích lũy chi phí (Orphaned Resources)
*   **Nguyên nhân:** Khi kỹ sư xóa EC2 Instance nhưng quên tích chọn "Delete EBS Volume on Termination", hoặc xóa EC2 nhưng giữ lại Elastic IP (EIP) dự phòng.
*   **Cách tìm kiếm tài nguyên mồ côi bằng CLI:**
    *   *Liệt kê các EBS Volumes ở trạng thái không sử dụng (available):*
        ```bash
        aws ec2 describe-volumes \
          --filters "Name=status,Values=available" \
          --query "Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType}"
        ```
    *   *Liệt kê các Elastic IP không được gán vào đâu:*
        ```bash
        aws ec2 describe-addresses \
          --query "Addresses[?AssociationId==null].{IP:PublicIp,AllocationId:AllocationId}"
        ```
    *   *Xóa dọn dẹp bằng CLI (Sau khi đã sao lưu dữ liệu):*
        ```bash
        aws ec2 delete-volume --volume-id vol-0123456789abcdef0
        aws ec2 release-address --allocation-id eipalloc-0123456789abcdef0
        ```

### 3. Tag không xuất hiện trong Cost Explorer (Cost Allocation Tags)
*   **Hiện tượng:** Bạn đã gắn tag `Project = MyNewApp` cho toàn bộ tài nguyên, nhưng khi vào Cost Explorer để lọc chi phí theo dự án thì không thấy bộ lọc `Project` hiển thị.
*   **Nguyên nhân:** Mặc định các tags tự tạo không được dùng làm bộ lọc chi phí. Bạn bắt buộc phải **Kích hoạt (Activate)** tag đó trong Billing Console.
*   **Cách khắc phục:**
    *   Truy cập **AWS Billing Console** -> **Cost Allocation Tags**.
    *   Tìm kiếm tag tên là `Project`.
    *   Tích chọn và ấn **Activate**. 
    *   *Lưu ý quan trọng:* Sẽ mất từ **24 đến 48 giờ** để AWS cập nhật dữ liệu hóa đơn phân tích theo tag mới.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **AWS Budgets** khi: Cần thiết lập cảnh báo tĩnh ngăn chặn chi phí vượt mức ngân sách định sẵn (ví dụ: Ngăn ngân sách tháng vượt quá $500).
- Chọn **AWS Cost Anomaly Detection** khi: Cần máy học (Machine Learning) tự động học hành vi chi tiêu và phát hiện các biến động bất thường không thể dự đoán trước.
- Chọn **AWS Config** khi: Cần thực thi các tiêu chuẩn tuân thủ hạ tầng nghiêm ngặt (Compliance), đảm bảo mọi tài nguyên không đạt chuẩn bị tự động phát hiện và dọn dẹp.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Activating user-defined cost allocation tags](https://docs.aws.amazon.com/billing/latest/userguide/activate-tags.html)
  - [Identifying unused resources using AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/volume-unused-check.html)
