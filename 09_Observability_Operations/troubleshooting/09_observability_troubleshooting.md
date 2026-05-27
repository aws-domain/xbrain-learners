# Topic 09: Observability Troubleshooting — Khắc Phục Sự Cố CloudWatch Agent & Alarm

## 📌 Tổng quan cốt lõi (Core Concepts)
- **CloudWatch Custom Metrics:** EC2 theo mặc định không thu thập các thông số sâu của hệ điều hành như RAM, Disk Space. Bạn bắt buộc phải cài đặt **CloudWatch Agent** nội bộ để đẩy các thông số này lên dưới dạng Custom Metrics thông qua API `PutMetricData`.
- **CloudWatch Alarms Evaluation:** Quá trình kích hoạt Alarm phụ thuộc vào sự kết hợp giữa **Period** (Khoảng thời gian đo lường) và **Evaluation Periods** (Số chu kỳ liên tiếp vượt ngưỡng để chuyển trạng thái từ `OK` sang `ALARM`).

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ cơ chế hoạt động của CloudWatch Agent trên EC2
```
[EC2 OS: Linux/Windows] ◄──► [CloudWatch Agent Service]
         │ (Đọc file config: amazon-cloudwatch-agent.json)
         ├──────────────────────────┐
         ▼ (Thu thập RAM/Disk)       ▼ (Đọc file log hệ thống)
   [System Metrics API]       [Read File: /var/log/nginx/access.log]
         │                           │
         └─────────────┬─────────────┘
                       │ (API Call qua VPC Endpoint hoặc Internet)
                       ▼ (Yêu cầu IAM Role: CloudWatchAgentServerPolicy)
             [Amazon CloudWatch Service]
             ┌─────────┴─────────┐
             ▼                   ▼
       [Metric Groups]     [Log Groups]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | Standard Resolution (CloudWatch Metrics) | High Resolution (CloudWatch Metrics) |
|---|---|---|
| **Chu kỳ thu thập tối thiểu** | 1 phút (60 giây). | **1 giây** (Thường dùng cho hệ thống real-time nhạy cảm). |
| **Chi phí** | Giá tiêu chuẩn. | Đắt hơn do lượng điểm dữ liệu đẩy lên nhiều gấp 60 lần. |
| **Phù hợp nhất cho** | Giám sát tài nguyên chung (CPU, Disk IOPS cơ bản). | Giám sát các lỗi đột biến tức thời (Spike errors), giao dịch tài chính. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. CloudWatch Alarm không kích hoạt dù Metric đã vượt ngưỡng
*   **Nguyên nhân 1: Sai lệch cấu hình Evaluation Periods (Lỗi phổ biến nhất):**
    *   **Cơ chế:** Nếu bạn cấu hình: *Period = 5 phút*, *Evaluation Periods = 3*. Nghĩa là metric bắt buộc phải vượt ngưỡng liên tục trong vòng **15 phút** (3 chu kỳ của 5 phút). Nếu CPU chỉ vọt lên trong 10 phút rồi giảm xuống, Alarm sẽ không bao giờ kích hoạt.
*   **Nguyên nhân 2: Độ phân giải Metric quá thô (Metric Resolution vs Period):**
    *   Sử dụng Custom Metric được đẩy lên mỗi 5 phút một lần, nhưng Alarm lại cấu hình kiểm tra mỗi 1 phút. Sự bất đồng bộ về chu kỳ dữ liệu khiến Alarm rơi vào trạng thái `INSUFFICIENT_DATA` hoặc không đánh giá chính xác.
*   **Cách kiểm tra và xử lý bằng CLI:**
    *   *Kiểm tra trạng thái cấu hình của Alarm:*
        ```bash
        aws cloudwatch describe-alarms \
          --alarm-names "High-CPU-Alarm" \
          --query "MetricAlarms[*].{State:StateValue,Period:Period,EvalPeriods:EvaluationPeriods}"
        ```
    *   *Khắc phục:* Đảm bảo chu kỳ của Alarm (`Period`) khớp hoặc lớn hơn chu kỳ đẩy dữ liệu thực tế của Metric. Giảm `Evaluation Periods` xuống `1` nếu muốn kích hoạt cảnh báo lập tức ngay khi chạm ngưỡng.

### 2. CloudWatch Agent không đẩy được Custom Metrics (RAM/Disk)
*   **Nguyên nhân 1: Thiếu IAM Role (Lỗi kinh điển):**
    *   EC2 Instance chưa được gán IAM Role (qua Instance Profile) chứa AWS Managed Policy `CloudWatchAgentServerPolicy`, dẫn đến việc Agent bị từ chối khi gọi API `PutMetricData`.
*   **Nguyên nhân 2: Lỗi cấu hình Agent file JSON:**
    *   File cấu hình `amazon-cloudwatch-agent.json` bị sai định dạng hoặc đường dẫn file log khai báo không tồn tại.
*   **Cách kiểm tra và xử lý bằng CLI (Truy cập EC2 qua SSM):**
    *   *Kiểm tra file log của chính CloudWatch Agent để tìm lỗi:*
        ```bash
        tail -n 50 /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
        ```
        *(Tìm lỗi `AccessDenied` -> Do thiếu IAM Role. Tìm lỗi `JSON parsing error` -> Do cấu hình sai file json).*
    *   *Khởi động lại Agent sau khi sửa cấu hình:*
        ```bash
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
          -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
        ```

### 3. Log Group không nhận được dữ liệu (Logs empty)
*   **Nguyên nhân:** CloudWatch Agent hoạt động bằng cách "đuôi" (tail) file log trên đĩa. Nếu user chạy Agent không có quyền đọc file log đó (ví dụ file log của Nginx thuộc sở hữu của user `nginx:nginx` nhưng Agent chạy dưới quyền user `cwagent` bị hạn chế quyền đọc).
*   **Cách khắc phục:**
    *   Cấp quyền đọc (Read permissions) cho thư mục và file log để user của CloudWatch Agent có thể truy cập:
        ```bash
        sudo chmod +r /var/log/nginx/access.log
        ```

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **CloudWatch Logs Insights** khi: Cần truy vấn, lọc và phân tích hàng triệu dòng log thô cực nhanh bằng cú pháp giống SQL mà không cần cài đặt ELK Stack.
- Chọn **Standard Resolution (1 phút)** khi: Cần thiết lập cảnh báo cho các hạ tầng chung như EC2 Auto Scaling, RDS để tối ưu chi phí.
- Chọn **AWS CloudTrail** thay vì **CloudWatch Logs** khi: Cần giám sát "Ai đã thao tác gì trên tài nguyên hệ thống ở mức API" (Kiểm toán bảo mật).

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Troubleshoot the CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/troubleshoot-CloudWatch-Agent.html)
  - [Configuring CloudWatch Alarms for accuracy](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
