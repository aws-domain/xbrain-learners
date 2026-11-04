# CloudWatch CLI: put-metric-data vs put-metric-alarm vs put-dashboard
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation)
**Note liên quan:** `cloudwatch_getting_started.md`, `unified_cloudwatch_agent_setup.md`, lab `d1-03`

---

## 0. Tóm Tắt Một Dòng
Ba lệnh đều có thật, cùng nằm trong `aws cloudwatch`, nhưng là **3 chặng khác nhau** của vòng đời quan sát: **`put-metric-data`** ghi số liệu LÊN, **`put-metric-alarm`** canh ngưỡng và REACT, **`put-dashboard`** vẽ biểu đồ để NGƯỜI nhìn.

> Đã xác minh bằng docs AWS CLI chính thức (CloudWatch reference, bản 2.39.1). Cả 3 lệnh đều tồn tại.

---

## 1. Mạch Liên Kết: 3 Lệnh Là 3 Chặng Của Một Dòng Chảy

```
put-metric-data        put-metric-alarm         put-dashboard
   (ghi so)      --->     (canh nguong)    +    (ve bieu do de xem)
      |                        |                       |
      v                        v                       v
  Metric trong          Vuot nguong ->          Dashboard hien thi
  CloudWatch            ban SNS/EC2 action       metric cho nguoi xem
```

Điểm chung: cả ba đều là động từ **`put`** = "tạo mới nếu chưa có, **ghi đè** nếu đã có" (idempotent).
Ví dụ `put-dashboard`: docs ghi rõ "nếu update thì **thay toàn bộ** nội dung cũ". `put-*` không nối thêm, nó thay. Đây là đặc tính thi hay hỏi.

**Analogy:** nghĩ về một phòng điều khiển nhà máy.
- `put-metric-data` = công nhân ghi số đo vào sổ (nhập liệu).
- `put-metric-alarm` = cái còi tự hú khi số vượt ngưỡng (phản ứng tự động).
- `put-dashboard` = tấm bảng điện tử treo tường để quản lý nhìn (hiển thị).

*Chỗ analogy gãy:* dashboard CloudWatch chỉ hiển thị, nó **không** tự hành động; còi (alarm) mới hành động.

---

## 2. Bảng Phân Biệt

| | `put-metric-data` | `put-metric-alarm` | `put-dashboard` |
|---|---|---|---|
| Làm gì | Publish số liệu vào một metric | Tạo/sửa alarm trên 1 metric (hoặc biểu thức math) | Tạo/sửa 1 dashboard |
| Tham số chính | `--namespace`, `--metric-data` (tên, value, dimensions) | `--alarm-name`, `--metric-name`, `--threshold`, `--comparison-operator`, `--alarm-actions` | `--dashboard-name`, `--dashboard-body` (JSON widget) |
| Kết quả | Metric xuất hiện trong CloudWatch (có thể mất tới **15 phút** để thấy trong `list-metrics`) | Alarm đổi state OK / ALARM / INSUFFICIENT_DATA, bắn action khi đổi state | Bảng biểu đồ để người xem nhìn |
| Phạm vi | Theo **Region** | Theo **Region** | **Global**, không theo Region (docs: "All dashboards in your account are global") |
| Vai trò | Nguồn dữ liệu (write) | Phản ứng tự động (react) | Hiển thị cho người (view) |

---

## 3. Giải Thích Từng Lệnh + Ví Dụ CLI

### 3.1. `put-metric-data` — đẩy số liệu lên
Dùng khi có một **custom metric** app tự tính (số đơn hàng, latency nội bộ) và muốn đưa vào CloudWatch.
Đây chính là cách custom metric ra đời. Liên hệ lab `d1-03`: CloudWatch agent nội bộ cũng gọi API này để đẩy mem/disk lên namespace `CWAgent`.

```bash
aws cloudwatch put-metric-data \
  --namespace "MyApp/Orders" \
  --metric-name OrdersPlaced \
  --value 5 \
  --region ap-southeast-1
```

Lưu ý:
- Namespace **không được bắt đầu bằng `AWS/`** (tiền tố này dành riêng cho metric AWS sinh).
- Metric mới có thể mất tới **15 phút** mới hiện trong `list-metrics`.
- Giới hạn: tối đa 1000 metric khác nhau / request, payload tối đa 1 MB.

### 3.2. `put-metric-alarm` — canh ngưỡng và tự phản ứng
Dùng khi muốn: metric vượt ngưỡng thì báo (SNS) hoặc hành động (stop/reboot/recover EC2, Auto Scaling).

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "HighCPU" \
  --namespace "AWS/EC2" \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:ap-southeast-1:111122223333:AlertTopic \
  --region ap-southeast-1
```

**Bẫy thi quan trọng:** alarm chỉ bắn được tới **SNS, EC2 action (stop/terminate/reboot/recover), Auto Scaling action, SSM OpsItem/Incident** qua `--alarm-actions`.
Alarm **KHÔNG** trỏ thẳng được tới **SSM Automation document** hay **Lambda** — phải đi vòng qua **EventBridge**. (Đây đúng là điểm gài trong câu hỏi EventBridge + SSM Automation đã học.)

### 3.3. `put-dashboard` — vẽ bảng để nhìn
Dùng khi muốn gom nhiều metric/biểu đồ vào một màn hình. Chỉ để **xem**, không tự phản ứng, không ghi số liệu.

```bash
aws cloudwatch put-dashboard \
  --dashboard-name "Prod-Overview" \
  --dashboard-body file://dashboard.json
```

`dashboard.json` là mảng widget JSON, ví dụ tối thiểu từ docs:
```json
{"widgets":[{"height":6,"width":6,"y":0,"x":0,"type":"metric","properties":{"view":"timeSeries","stacked":false,"metrics":[["Namespace","CPUUtilization","Environment","Prod","Type","App"]],"region":"us-east-1"}}]}
```
Nhớ: dashboard là **global**, không gắn Region như metric/alarm. Update sẽ **thay toàn bộ** nội dung cũ.

---

## 4. Phân Biệt Bằng Một Câu
- **data** = tôi GHI số.
- **alarm** = tôi CANH số và REACT.
- **dashboard** = tôi VẼ số để NGƯỜI nhìn.

---

## 5. Mẹo Phân Biệt Nhanh Khi Thi (keyword -> lệnh)

| Thấy keyword trong đề | Chọn |
|---|---|
| "publish / send custom metric" | `put-metric-data` |
| "notify / trigger action when threshold exceeded" | `put-metric-alarm` |
| "visualize / single pane of glass / view multiple metrics" | `put-dashboard` |

Bẫy kèm: alarm → SSM Automation phải qua **EventBridge**; alarm trực tiếp chỉ tới **SNS / EC2 action / Auto Scaling / OpsItem**.

---

## 6. Câu Tự Kiểm Tra
App của bạn tự đếm số lần login thất bại và bạn muốn: (1) đưa con số này vào CloudWatch, (2) gửi email khi nó vượt 100 lần trong 5 phút.
- Bước (1) gọi lệnh nào?
- Bước (2) gọi lệnh nào?
- Email được gửi qua service nào?

<details>
<summary>Đáp án</summary>

(1) `put-metric-data` để đẩy custom metric lên. (2) `put-metric-alarm` với `--threshold 100`, `--period 300`, `--evaluation-periods 1`. Email gửi qua **SNS topic** (đặt ARN topic vào `--alarm-actions`, subscribe email và confirm).
</details>

---

## Sources
- [AWS CLI put-metric-data](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-data.html)
- [AWS CLI put-metric-alarm](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-metric-alarm.html)
- [AWS CLI put-dashboard](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/put-dashboard.html)
