# Topic 07: Data Engineering Troubleshooting — Khắc Phục Sự Cố Kinesis Consumers Lag & Glue Job Failures

## 📌 Tổng quan cốt lõi (Core Concepts)
- **Kinesis Data Streams Capacity:** Stream được tạo thành từ một hoặc nhiều **Shards**, cung cấp băng thông đọc/ghi cố định (1MB/s hoặc 1000 records/s ghi; 2MB/s đọc). Khi lượng dữ liệu đẩy vào vượt quá số Shards hiện tại, consumer sẽ bị trễ (Lag) nghiêm trọng.
- **AWS Glue Execution Resources:** Glue là dịch vụ serverless ETL. Sức mạnh tính toán của Glue Job được đo bằng **DPU (Data Processing Units)**. Lỗi thiếu tài nguyên, phân quyền IAM sai hoặc logic code Spark không tối ưu là các nguyên nhân chính khiến Glue Job bị Fail.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ chẩn đoán nghẽn Kinesis Stream (Kinesis Bottleneck & Consumer Lag)
```
  [Data Producers] (IOT / App logs)
         │ (Ghi vượt quá 1MB/s per shard)
         ▼
[Kinesis Shards: Shard 1, Shard 2] ◄──► [DescribeStreamSummary CLI]
         │ (Đọc bị chậm do chạm giới hạn 2MB/s read)
         ├──────────────────────────┐
         ▼ (Standard Consumer A)     ▼ (Standard Consumer B)
  [Shared Read: 2MB/s Pool]   [Shared Read: 2MB/s Pool] (Bị cạnh tranh băng thông)
         │
         ▼ (Giải pháp khắc phục với Enhanced Fan-Out)
  [Consumer A: Dedicated 2MB/s Pipe via HTTP/2 Push] ──► Không bị cạnh tranh
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | Kinesis Standard Consumer | Kinesis Enhanced Fan-Out (EFO) |
|---|---|---|
| **Băng thông Đọc (Read Bandwidth)** | Chia sẻ chung **2MB/s per Shard** cho toàn bộ consumers của stream đó. | Cung cấp đường ống riêng **2MB/s per Shard** cho mỗi Consumer đăng ký. |
| **Cơ chế truyền tải** | Pull model (HTTP GET request - polling). | Push model (HTTP/2 Server Push - Active connection). |
| **Độ trễ (Latency)** | Khoảng 200ms - 1 giây. | Dưới **70ms** (Real-time). |
| **Chi phí** | Rất rẻ, chỉ tính phí Shard giờ. | Đắt hơn, tính thêm phí sử dụng EFO và dung lượng dữ liệu truyền qua. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. Kinesis Consumer bị Lag (Trễ xử lý dữ liệu)
*   **Nguyên nhân 1: Quá tải Shards (Write/Read Limit Exceeded):**
    *   **Cơ chế:** Nếu tốc độ đẩy dữ liệu lớn hơn dung lượng ghi của số shard hiện tại, Kinesis sẽ trả về lỗi `ProvisionedThroughputExceededException` về phía producer. Ngược lại, nếu quá nhiều consumer cùng đọc một shard, tốc độ đọc sẽ bị giảm dẫn đến trễ.
*   **Nguyên nhân 2: Consumer xử lý chậm (Application Bottleneck):**
    *   Mã nguồn của Consumer (ví dụ: Lambda, ứng dụng EC2) xử lý nghiệp vụ quá lâu đối với mỗi batch records nhận về.
*   **Cách kiểm tra và xử lý bằng CLI:**
    *   *Kiểm tra metric trong CloudWatch:* Theo dõi metric `GetRecords.IteratorAgeMilliseconds` (đo khoảng cách thời gian giữa record mới nhất và record đang được xử lý). Nếu metric này tăng vọt liên tục -> Consumer đang bị Lag rất nặng.
    *   *Tự động scale tăng số lượng Shard bằng CLI (Resharding):*
        ```bash
        aws kinesis update-shard-count \
          --stream-name MyDataStream \
          --target-shard-count 10 \
          --scaling-type UNIFORM_SCALING
        ```
    *   *Giải pháp tối ưu hóa:*
        *   Nếu có nhiều ứng dụng cùng đọc một Stream -> Đăng ký **Enhanced Fan-Out (EFO)** cho các consumer quan trọng để có băng thông riêng biệt 2MB/s.
        *   Tăng kích thước batch size (`MaxBatchingWindowInSeconds`) hoặc chạy xử lý song song trên consumer.

### 2. AWS Glue Job bị Fail
*   **Nguyên nhân 1: Thiếu quyền IAM (Lỗi phổ biến nhất khi tạo mới):**
    *   IAM Role gán cho Glue Job thiếu quyền ghi log vào CloudWatch (`logs:*`), hoặc thiếu quyền đọc/ghi dữ liệu vào S3 Bucket tương ứng.
*   **Nguyên nhân 2: Out of Memory (OOM) / Thiếu DPU:**
    *   Dữ liệu quá lớn, chạy các phép Join phức tạp trong Spark không được phân bổ đủ bộ nhớ đệm DPU.
*   **Cách kiểm tra và xử lý:**
    *   *Kiểm tra log của Glue Job trên CloudWatch Logs:*
        Vào Log Group `/aws-glue/jobs/error` hoặc `/aws-glue/jobs/output` để xem stack trace chi tiết của Java/Python Spark.
    *   *Khắc phục lỗi phân quyền bằng cách kiểm tra IAM Role:*
        Đảm bảo Role có chứa AWS Managed Policy `AWSGlueServiceRole` và có S3 Bucket Policy cho phép Glue truy cập.
    *   *Khắc phục lỗi OOM / Tăng DPU:*
        *   Tăng số lượng DPU hoặc đổi Worker Type từ `G.1X` lên `G.2X` (cung cấp gấp đôi bộ nhớ và dung lượng đĩa) để tăng sức mạnh xử lý song song của Spark Cluster:
            ```bash
            aws glue update-job \
              --job-name my-etl-job \
              --job-update "Role=arn:aws:iam::...,Command={Name=glueetl,ScriptLocation=s3://...},WorkerType=G.2X,NumberOfWorkers=10,GlueVersion=4.0"
            ```
        *   *Tối ưu code Spark:* Tránh sử dụng `.collect()` trong Spark vì nó sẽ gom toàn bộ dữ liệu từ các worker node về driver node duy nhất, dễ gây sập bộ nhớ (OOM).

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **Glue Worker Type G.2X** khi: Thực hiện các tác vụ ETL phức tạp, join nhiều bảng dữ liệu khổng lồ, hoặc chạy các script Deep Learning cần nhiều RAM/Disk.
- Chọn **Glue Worker Type G.1X** khi: Các tác vụ transform dữ liệu cơ bản, xử lý batch đều đặn và lượng dữ liệu trung bình.
- Chọn **Enhanced Fan-Out (EFO)** khi: Stream có từ 2 consumers trở lên và ứng dụng yêu cầu độ trễ xử lý dữ liệu dưới 100ms.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Troubleshoot Kinesis Data Streams consumer lag](https://docs.aws.amazon.com/streams/latest/dev/troubleshooting-consumers.html)
  - [Monitoring AWS Glue jobs using CloudWatch metrics](https://docs.aws.amazon.com/glue/latest/dg/monitor-profile-glue-metrics.html)
