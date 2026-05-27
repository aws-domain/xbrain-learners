# Topic 03: Database Troubleshooting — Khắc Phục Sự Cố DynamoDB & RDS Connections

## 📌 Tổng quan cốt lõi (Core Concepts)
- **DynamoDB Throughput Limits:** DynamoDB hoạt động dựa trên cơ chế phân vùng dữ liệu (Partitions). Khi số lượng requests vượt quá giới hạn cấu hình (RCUs/WCUs), DynamoDB sẽ trả về lỗi nghẽn.
- **RDS Connection Limits:** Số lượng kết nối đồng thời tối đa của RDS được tính toán tự động dựa trên dung lượng RAM của Instance Class. Khi ứng dụng scale out quá nhanh, các kết nối DB bị cạn kiệt, dẫn đến sập ứng dụng Client.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ chẩn đoán DynamoDB Throttle (Hot Partition Scenario)
```
[DynamoDB Requests]
        │
        ├──► Case A: Uniform Access Pattern
        │       └── Request Rate > Provisioned RCUs/WCUs ──► [Kích hoạt DynamoDB Auto Scaling]
        │
        └──► Case B: Non-Uniform Access (Hot Partition)
                ├── Accessing same Partition Key? ────────► [Thiết kế lại Partition Key - Add Salt]
                └── Querying same Hot Item? ──────────────► [Đặt DynamoDB Accelerator - DAX ở trước]
```

### Sơ đồ giảm tải kết nối qua RDS Proxy (Database Connection Pooling)
```
[Scale Out: 100+ Lambda Instances]
         │ (Open 100+ Direct DB Connections - Crash DB)
         ▼
[RDS MySQL / PostgreSQL Database] (Resource Exhausted)

  ───► Giải pháp khắc phục với RDS Proxy ───►

[Scale Out: 100+ Lambda Instances]
         │
         ▼
    [RDS Proxy] (Connection Pooling & Reuse)
         │ (Maintains only 5-10 Active DB Connections)
         ▼
[RDS MySQL / PostgreSQL Database] (Healthy & Stable)
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | DynamoDB Provisioned Mode | DynamoDB On-Demand Mode |
|---|---|---|
| **Cơ chế tính phí** | Trả tiền theo dung lượng RCUs/WCUs đăng ký trước (dù có xài hết hay không). | Trả tiền chính xác theo số lượng Request thực tế phát sinh (Pay-per-request). |
| **Tốc độ đáp ứng tải** | Tải tăng đột biến quá nhanh sẽ bị throttle trước khi Auto Scaling kịp nâng giới hạn. | Đáp ứng tải tăng vọt ngay lập tức mà không cần cấu hình scale. |
| **Phù hợp nhất cho** | Hệ thống có lượng truy cập ổn định, dễ dự đoán traffic. | Hệ thống có tải đột biến không dự đoán trước (ví dụ: Flash Sale, Ticket Booking). |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. DynamoDB bị Throttle (Lỗi `ProvisionedThroughputExceededException`)
*   **Nguyên nhân 1: Quên bật Auto Scaling:** Lượng traffic tăng vượt quá giới hạn RCUs/WCUs tĩnh cấu hình cho bảng.
*   **Nguyên nhân 2: Hiện tượng Hot Partition (Cực kỳ nguy hiểm):**
    *   **Cơ chế:** DynamoDB chia nhỏ bảng thành nhiều partition vật lý dựa trên giá trị của **Partition Key**. Mỗi partition có giới hạn cứng là **1000 WCUs và 3000 RCUs**.
    *   Nếu ứng dụng của bạn liên tục đọc/ghi vào duy nhất một giá trị Partition Key (ví dụ: ID của một KOL trên mạng xã hội), partition chứa key đó sẽ bị nghẽn (Throttle), dù tổng dung lượng RCUs/WCUs của cả bảng vẫn còn dư rất nhiều.
*   **Cách kiểm tra và xử lý bằng CloudWatch Metrics:**
    *   *Kiểm tra metrics:* Quan sát `ReadThrottleEvents` và `WriteThrottleEvents` trong CloudWatch.
    *   *Xử lý bằng CLI:*
        *   Nâng cấp bảng sang chế độ **On-Demand** để tự động scale không giới hạn:
            ```bash
            aws dynamodb update-table \
              --table-name MyTable \
              --billing-mode PAY_PER_REQUEST
            ```
        *   Nếu bị Hot Partition: Thiết kế lại Partition Key (ví dụ: thay vì dùng `Date` làm partition key, hãy dùng `Date_RandomNumber` để phân phối đều dữ liệu ra các partition vật lý - Kỹ thuật **Write Sharding / Salting**).

### 2. RDS Database Connections bị cạn kiệt (Lỗi `Too many connections`)
*   **Nguyên nhân:** Ứng dụng Serverless (AWS Lambda) tự động scale out thành hàng trăm instances khi có tải. Mỗi Lambda instance khi khởi tạo sẽ mở một kết nối trực tiếp đến RDS và giữ kết nối đó. Điều này nhanh chóng vắt kiệt RAM của RDS và làm sập cơ sở dữ liệu.
*   **Cách kiểm tra bằng CLI:**
    *   *Kiểm tra metric trong CloudWatch:* Theo dõi metric `DatabaseConnections` của RDS.
    *   *Kiểm tra số kết nối tối đa cho phép của RDS class hiện tại (ví dụ MySQL):*
        ```sql
        SHOW VARIABLES LIKE 'max_connections';
        ```
*   **Giải pháp xử lý (DevOps Best Practices):**
    *   **Triển khai RDS Proxy:** Đặt một RDS Proxy đứng trước database. RDS Proxy sẽ đóng vai trò làm bộ đệm Connection Pool, gom hàng nghìn kết nối từ Lambda lại và chỉ duy trì một số lượng nhỏ kết nối ổn định tới RDS.
    *   *Tạo RDS Proxy bằng CLI:*
        ```bash
        aws rds create-db-proxy \
          --db-proxy-name my-rds-proxy \
          --engine-family MYSQL \
          --auth Description="RDS Credentials",AuthScheme=SECRETS_MANAGER,SecretArn="arn:aws:secretsmanager:..." \
          --role-arn arn:aws:iam::... \
          --vpc-subnet-ids subnet-123456 subnet-789012
        ```
    *   **Tối ưu hóa Code:** Đảm bảo giải phóng kết nối (close connection) trong mã nguồn Lambda sau khi kết thúc thực thi hoặc sử dụng các thư viện quản lý pool hiệu quả.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **DynamoDB Accelerator (DAX)** khi: Cần giảm độ trễ đọc của DynamoDB từ mili-giây xuống **micro-giây** cho các hot key (Read-heavy cache).
- Chọn **RDS Proxy** khi: Sử dụng database quan hệ (RDS MySQL, PostgreSQL) kết hợp với các dịch vụ **Serverless (Lambda)** có tính chất scale out đột ngột.
- Chọn **DynamoDB Auto Scaling** khi: Muốn tiết kiệm tiền và tải của hệ thống thay đổi từ từ, dễ dự đoán theo thời gian trong ngày.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Avoid partition throttling in Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
  - [Managing connections with Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
