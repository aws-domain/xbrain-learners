# CloudWatch Logs Insights (Phân Tích Log Tương Tác)
**Chủ đề (Topic):** Observability & Operations
**Dịch vụ (Service):** Amazon CloudWatch Logs
**Ngữ cảnh (Context):** Lab d1-02 (phân tích VPC Flow Log, gộp lỗi Lambda) + mẫu câu hỏi SOA-C03

---

## 0. Logs Insights Là Gì Và Giải Quyết Vấn Đề Gì

**CloudWatch Logs Insights** là dịch vụ query log **tương tác, fully managed**. Nó cho phép phân tích log đã nằm sẵn trong một hoặc nhiều **log group** mà **không cần export dữ liệu đi đâu, không cần dựng hạ tầng**. Dùng được cả trên CloudWatch Console lẫn AWS CLI/SDK.

Vấn đề nó giải quyết: khi log đã ở CloudWatch Logs và bạn cần đếm/nhóm/thống kê (ví dụ "đếm số lỗi theo loại", "top IP theo byte"), Logs Insights trả lời ngay bằng một câu query, không phải ETL ra S3 rồi mới phân tích.

> [!IMPORTANT]
> Logs Insights KHÁC Metric Filter. Metric filter chạy **lúc log được ingest**, biến dòng khớp thành metric time-series để vẽ chart và tạo alarm. Logs Insights chạy **theo yêu cầu (ad-hoc)** trên log đã lưu, để phân tích và điều tra. Cần alarm liên tục -> metric filter. Cần truy vấn/điều tra -> Logs Insights.

---

## 1. Lệnh `stats` Và Hàm Aggregation

`stats` là lệnh tính **aggregate** trên các log event khớp query (count, sum, avg, min, max, countDistinct...). Ghép với `by <field>` thì kết quả được **nhóm theo giá trị của field đó**.

Cú pháp gộp đếm theo field (xác thực từ docs):
```
stats count(*) by fieldName
```
Kết quả: tổng số record khớp, nhóm theo từng giá trị của `fieldName`.

### 1.1 `count(*)` vs `count(fieldName)`
| Dạng | Đếm cái gì |
| :--- | :--- |
| `count(*)` | Mọi event khớp query (kể cả event không có field đó) |
| `count(fieldName)` | Chỉ event mà `fieldName` **khác null** |

Gộp lỗi theo loại thường dùng `stats count(*) by errorType` (đếm tất cả event trong từng nhóm).

### 1.2 Các hàm hay dùng
- `count(*)`, `count(f)`: đếm.
- `sum(f)`, `avg(f)`, `min(f)`, `max(f)`: thống kê số.
- `countDistinct(f)`: đếm giá trị duy nhất (ví dụ số IP khác nhau).
- `bin(5m)`: gom theo khung thời gian 5 phút (vẽ time-series).

### 1.3 Nhiều `stats` trong một query
Dùng được nhiều lệnh `stats` nối tiếp để aggregate trên kết quả của aggregate trước. Giới hạn số lệnh `stats` tùy **log class** của log group.
```
FIELDS strlen(@message) AS message_length
| STATS sum(message_length)/1024/1024 AS logs_mb BY bin(5m)
| STATS max(logs_mb), min(logs_mb), avg(logs_mb)
```

---

## 2. Query Nhiều Log Group Cùng Lúc (điểm thi hay hỏi)

Đây là tính năng khiến Logs Insights thắng nhiều kịch bản: **một request query được NHIỀU log group một lần**. Trong Console, ở dropdown "Select log group(s)" chọn nhiều log group; qua API/CLI thì truyền danh sách log group (hoặc dùng lệnh `SOURCE` để chọn theo prefix tên).

> [!IMPORTANT]
> Giới hạn (xác thực từ docs API `StartQuery`): **tối đa 10 data source trong một query**. Query **timeout sau 60 phút**. Mặc định tối đa **100 concurrent Logs Insights query** mỗi region (dùng chung với scheduled query).

Với **cross-account observability**, một query trong monitoring account quét được log group ở cả các source account.

---

## 3. Kịch Bản Mẫu: Gộp Lỗi Của Nhiều Lambda Cho Compliance

Bối cảnh: mỗi Lambda function ghi log vào **log group riêng**. Compliance team cần đếm số lỗi **nhóm theo loại lỗi** (`errorType`), với **ít operational overhead nhất**. Log đã nằm sẵn trong CloudWatch Logs.

Giải pháp: chọn tất cả log group của các Lambda vào scope, lọc event lỗi, rồi gộp đếm:
```
fields @message
| filter @message like /ERROR/
| stats count(*) by errorType
```
Kết quả:

| errorType | count(*) |
| :--- | :--- |
| TimeoutError | 42 |
| ValidationError | 17 |
| ThrottlingError | 9 |

Không di chuyển dữ liệu, không thêm dịch vụ, không dựng hạ tầng.

---

## 4. Vì Sao Các Phương Án Khác Bị Loại (pattern loại trừ của đề)

Deciding keyword: **"least operational overhead"** + **"logs already reside in CloudWatch Logs"**.

| Phương án sai | Lý do bị loại |
| :--- | :--- |
| Export log ra **S3** rồi phân tích (Athena) | Log đã ở CloudWatch. Export là một bước di chuyển dữ liệu thừa, tốn công setup. |
| Tạo **metric filter / rule per-log-group** | Phải tạo và quản lý một rule cho từng Lambda. Số function tăng thì overhead tăng theo. |
| Instrument bằng **tracing service riêng** (X-Ray) | Phải sửa code từng function, thêm một dịch vụ nữa. Thừa khi chỉ cần đếm lỗi từ log có sẵn. |

Logs Insights thắng vì: no data movement, no additional service, no infra setup, và một query quét hết các log group.

---

## 5. Logs Insights So Với Công Cụ Khác (hay bị trộn trong đề)

| Công cụ | Ghi/phân tích cái gì | Hợp cho |
| :--- | :--- | :--- |
| **Logs Insights** | Query ad-hoc log đã lưu trong CloudWatch Logs, nhiều log group | Đếm/nhóm/thống kê, điều tra sự cố, phân tích VPC Flow Log |
| **Metric filter** | Biến dòng log khớp thành metric lúc ingest | Alarm liên tục, chart time-series |
| **CloudTrail** | Ghi API call tới AWS (ai gọi gì, khi nào) | Audit hành vi account, không phải phân tích nội dung log app |
| **CloudFront logs** | Request HTTP qua CDN | Phân tích traffic CDN, không phải toàn bộ log VPC |
| **Athena trên S3** | Query SQL trên log đã export ra S3 | Log đã ở S3 / cần giữ dài hạn rẻ. Thừa nếu log đang ở CloudWatch |

---

## 6. Ví Dụ Query Thực Tế (lab d1-02)

Top IP đích theo byte từ VPC Flow Log:
```
stats sum(bytes) as totalBytes by dstAddr
| sort totalBytes desc
| limit 3
```
`by dstAddr` gom theo IP đích, `sum(bytes)` cộng tổng byte, `sort desc | limit 3` lấy 3 đích hút nhiều byte nhất. Lưu ý: "top" đo **khối lượng byte**, không phải số request.

Top client IP từ WAF log:
```
stats count(*) as requestCount by httpRequest.clientIp
| sort requestCount desc
```

---

## 7. Memory Tip (SOA-C03)

> Thấy đề có đủ cụm: **"logs already in CloudWatch Logs" + "least operational overhead" + "aggregate / group by / count"** -> đáp án gần như luôn là **CloudWatch Logs Insights với `stats count(*) by <field>`**.
> - Loại ngay: export ra S3/Athena (di chuyển dữ liệu thừa), metric filter từng log group (overhead theo số function), X-Ray (phải instrument lại).
> - Chi tiết AWS hay dùng để loại phương án: Logs Insights **query nhiều log group một lần** (tối đa 10 data source), nên không cần tạo rule cho từng function.
> - Phân biệt nhanh: **điều tra/phân tích ad-hoc = Logs Insights**, **alarm liên tục = metric filter**, **audit API call = CloudTrail**.

---

## Nguồn (Sources)
- [Tutorial: Run a query with an aggregation function](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_AnalyzeLogData_AggregationQuery.html)
- [stats command (CloudWatch Logs Insights query syntax)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Stats.html)
- [Start-CWLQuery (StartQuery) - gioi han 10 data source, timeout 60 phut, 100 concurrent](https://docs.aws.amazon.com/powershell/v5/reference/items/Start-CWLQuery.html)
