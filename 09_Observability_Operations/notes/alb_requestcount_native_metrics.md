# ALB RequestCount & Nguyên Tắc "Dùng Metric Có Sẵn, Đừng Tự Xây"
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation)
**Note liên quan:** `cloudwatch_cli_put_commands.md`, `cloudwatch_cross_region_aggregation.md`, `cloudwatch_getting_started.md`, lab `d1-04`

---

## 0. Tóm Tắt Một Dòng
Muốn đo **tổng request** qua một ALB theo thời gian: dùng thẳng metric **`RequestCount`** mà ALB tự đẩy lên CloudWatch (chỉnh time range + period, đọc graph). KHÔNG dùng Lambda/Logs Insights để tự đếm, KHÔNG đo ở từng EC2. Nguyên tắc: AWS đã có metric native thì đừng xây công cụ đếm.

---

## 1. Bài Toán Gốc (câu hỏi thi)
App chạy trên EC2 trong ASG sau ALB, hỏng khi tổng request/giây vượt 150. Cần tổng hợp dữ liệu request trong 3 tuần để tìm lúc nào vượt ngưỡng.

**Đáp án đúng:** dùng metric **`RequestCount` của ALB**, đặt time range = 3 tuần, period = 1 phút, phân tích graph tìm đỉnh traffic.

---

## 2. Vì Sao Đúng: Đo Ở ALB, Không Đo Từng EC2

ALB đứng **trước** toàn bộ ASG, mọi request đều đi qua nó. `RequestCount` của ALB đã là **tổng** của cả cụm, bất kể có bao nhiêu instance (ASG còn scale in/out liên tục, đếm ở từng instance rất rối).

```
       request --> [ ALB ] --> ASG (EC2-1, EC2-2, EC2-3...)
                     |
              RequestCount = TONG tat ca request (do 1 cho, dung luon)
```

ALB tự publish `RequestCount` lên CloudWatch, không cần cấu hình gì. Chỉ việc mở metric, chỉnh time range + period, đọc graph.

---

## 3. Chi Tiết Quan Trọng: RequestCount Là SUM, Không Phải Req/s (ý bổ sung)
Đề nói "150 **requests per second**" nhưng `RequestCount` là **tổng số request trong period** (statistic `Sum`), KHÔNG phải req/s trực tiếp.
- Period 1 phút + `Sum` = tổng request trong 60 giây.
- Muốn ra req/s: chia cho số giây của period, hoặc dùng period nhỏ hơn.

Chọn đáp án thi thì không ảnh hưởng, nhưng ở việc thật phải nhớ: `RequestCount` đếm **tổng**, không phải **tốc độ**.

---

## 4. Vì Sao 3 Đáp Án Kia Sai (bẫy thi)

| Đáp án sai | Lý do loại |
|---|---|
| **CloudWatch Logs Insights** tính sum request từ các EC2 | Logs Insights để **truy vấn log**, không phải đếm metric. ALB đã có metric sẵn, không cần moi từ log. Sai công cụ. |
| **CloudWatch Events rule + SNS** khi vượt ngưỡng | Events/SNS chỉ để **báo động lúc đang xảy ra**, không **tích lũy dữ liệu 3 tuần** để phân tích lại. Sai mục đích (alert vs analyze). |
| **Lambda** gom metric từ các EC2 rồi đẩy lên CloudWatch | Tự xây bộ đếm thủ công trong khi ALB **đã có `RequestCount` sẵn**. Thừa, tốn công, tốn tiền. |

**Điểm chung của bẫy:** bắt bạn **tự xây** thứ AWS đã cung cấp sẵn. Đáp án nghe "kỹ thuật" hơn nhưng phức tạp hóa vấn đề.

---

## 5. Từ Khóa Quyết Định Trong Đề
- "**compile / accumulate data over three weeks**" + "**identify**" -> phân tích lịch sử, cần **metric có sẵn đọc lại**, không phải alert -> loại Events/SNS.
- "**total requests**" qua ALB -> metric **`RequestCount` của ALB**, không đo từng EC2 -> loại Logs Insights/Lambda.

---

## 6. Mẹo Nhớ (exam pattern)
- Đo total request qua ALB -> **`RequestCount`**.
- AWS đã có metric native (CPUUtilization, RequestCount, NetworkIn...) -> **đừng** chọn đáp án Lambda/Logs tự xây.
- Phân biệt rõ: **alert** (CloudWatch Events + SNS, phản ứng lúc đang xảy ra) khác **analyze lịch sử** (đọc metric theo time range).

---

## 7. Câu Tự Kiểm Tra
Đề đổi thành "**tự động restart** service mỗi khi `RequestCount` vượt 150 trong 1 phút". Bạn còn chỉ cần đọc graph `RequestCount` nữa không, hay phải thêm thành phần nào?

<details>
<summary>Đáp án</summary>

Không còn chỉ đọc graph. Giờ là chuỗi phản ứng tự động: `RequestCount` -> **CloudWatch alarm** (ngưỡng > 150, period 1 phút) -> vì cần chạy **SSM Automation** để restart service nên alarm không gọi thẳng được, phải qua **EventBridge** (alarm đổi state -> EventBridge bắt -> chạy SSM Automation runbook). Đọc graph chỉ để phân tích lịch sử; tự động phản ứng cần alarm + EventBridge + Automation.
</details>

---

## Nguồn
- Nội dung câu hỏi thi (digitalcloud.training) và lab `d1-04` trong project.
- [Using Amazon CloudWatch metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)
