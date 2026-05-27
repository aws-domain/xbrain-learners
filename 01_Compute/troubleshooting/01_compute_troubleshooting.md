# Topic 01: Compute Troubleshooting — Khắc Phục Sự Cố EC2 & Auto Scaling Group (ASG)

## 📌 Tổng quan cốt lõi (Core Concepts)
- **SSH Connectivity:** Kết nối an toàn đến EC2 instance thông qua SSH (Port 22). Yêu cầu bắt buộc phải thông suốt ở cả 3 lớp: Mạng ảo (VPC), Hệ điều hành (OS/Firewall), và Xác thực (SSH Key Pair).
- **Auto Scaling Mechanisms:** Tự động điều chỉnh số lượng EC2 instances dựa trên nhu cầu thực tế. Sử dụng Dynamic Scaling Policies phối hợp với Cooldown Periods để tránh hiện tượng Thrashing (tạo/hủy liên tục).

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ chẩn đoán kết nối SSH (EC2 SSH Troubleshooting Flow)
```
[SSH Client Request]
       │
       ├──► 1. Network Layer (VPC Control Plane)
       │       ├── SG / NACL block port 22? ────► [Sửa Inbound Rule]
       │       └── Route Table missing IGW? ────► [Thêm route 0.0.0.0/0 trỏ tới IGW]
       │
       ├──► 2. Authentication Layer
       │       └── Incorrect Private Key? ──────► [Kiểm tra file .pem, chmod 400]
       │
       └──► 3. OS / Service Layer (Data Plane)
               ├── SSHD Service stopped? ───────► [Khởi động lại SSHD qua SSM]
               └── Authorized_keys wrong? ──────► [Sửa file keys qua SSM Session Manager]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | Launch Template | Launch Configuration (Legacy) |
|---|---|---|
| **Khả năng versioning** | **Có** (Hỗ trợ quản lý phiên bản) | **Không** (Muốn sửa phải tạo mới hoàn toàn) |
| **Hỗ trợ Spot & On-Demand**| Hỗ trợ cấu hình hỗn hợp (Mixed Instances Policy) | Chỉ cấu hình được 1 loại instance duy nhất |
| **Tính linh hoạt** | Rất cao, khuyên dùng bởi AWS | Đã bị AWS coi là Deprecated |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. EC2 không SSH được
*   **Nguyên nhân mạng:** 
    *   Security Group thiếu Inbound Rule cho Port 22 từ IP của bạn.
    *   NACL chặn port 22 hoặc chặn Ephemeral Ports phản hồi.
*   **Nguyên nhân xác thực (Key Pair):**
    *   Sử dụng sai Private Key (`.pem`) tương ứng với Public Key đã nạp vào instance khi khởi tạo.
    *   Quyền của file Private Key quá rộng (SSH sẽ từ chối kết nối).
*   **Cách kiểm tra và sửa đổi bằng CLI & SSM (Không dùng SSH):**
    *   *Sửa quyền Key file local:*
        ```bash
        chmod 400 my-ec2-key.pem
        ```
    *   *Dùng SSM Session Manager kết nối trực tiếp (Bypass SSH Port 22 & SG):*
        ```bash
        aws ssm start-session --target i-0123456789abcdef0
        ```
    *   *Kiểm tra dịch vụ SSHD trong EC2 (nếu dùng Linux):*
        ```bash
        sudo systemctl status sshd
        # Nếu service bị dừng, khởi động lại:
        sudo systemctl restart sshd
        ```

### 2. ASG không Scale Out dù CPU tăng cao
*   **Nguyên nhân 1: Cooldown Period quá lớn:**
    *   **Cơ chế:** Cooldown Period (mặc định 300s) là khoảng thời gian ASG "đóng băng", không thực hiện thêm hành động scale nào sau khi vừa thực hiện scale xong, để đợi metric ổn định. Nếu đặt quá lớn, ASG sẽ không scale kịp khi tải tăng đột biến liên tục.
*   **Nguyên nhân 2: Cấu hình Scaling Policy sai:**
    *   Sử dụng metric không đại diện cho bottleneck (ví dụ: nghẽn do RAM nhưng policy lại dựa trên CPU Utilization).
*   **Nguyên nhân 3: Chạm ngưỡng Service Quota / Account Limit:**
    *   Account đã đạt giới hạn tối đa số lượng EC2 vCPUs trong Region đó, hoặc ASG đã đạt `MaxSize`.
*   **Cách kiểm tra và xử lý:**
    *   *Kiểm tra lịch sử hoạt động của ASG bằng CLI:*
        ```bash
        aws autoscaling describe-scaling-activities \
          --auto-scaling-group-name my-asg-group
        ```
        *(Xem lỗi `Failed` do cạn quota vCPU hoặc đã chạm `MaxSize`).*
    *   *Khắc phục:*
        *   Tăng cấu hình `MaxSize` của ASG.
        *   Chuyển sang dùng **Target Tracking Scaling Policy** (ví dụ: Giữ CPU ổn định ở 70%) thay vì Simple Scaling Policy.
        *   Request tăng Service Quota cho EC2 instances nếu bị cạn kiệt tài nguyên ở mức Account.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **SSM Session Manager** thay vì **SSH truyền thống** khi: Cần bảo mật tối đa, không muốn mở port 22 ra ngoài internet và cần log lại toàn bộ lịch sử gõ lệnh của kỹ sư vào CloudWatch.
- Chọn **Target Tracking Scaling Policy** khi: Muốn hệ thống tự tính toán số lượng instance cần tăng/giảm để giữ metric đích ổn định (ví dụ: CPU = 60%).
- Chọn **Step Scaling Policy** khi: Cần scale cực nhanh dựa trên các bước nhảy tải cụ thể (ví dụ: CPU > 80% add thêm 5 instances, CPU > 90% add thêm 10 instances).

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Troubleshoot connecting to your EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html)
  - [Troubleshoot Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-troubleshoot-as-group-concepts.html)
