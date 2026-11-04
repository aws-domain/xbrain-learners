# CloudWatch Anomaly Detection vs Metric Math
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation)
**Note liên quan:** `cloudwatch_getting_started.md`, `cloudwatch_metrics_explorer.md`, `cloudwatch_cli_put_commands.md`, lab `d1-04`

---

## 0. Tóm Tắt Một Dòng
**Anomaly detection** = CloudWatch tự học nhịp bình thường của metric rồi kêu khi giá trị chui ra ngoài "vùng kỳ vọng" (band). **Metric math** = phép tính trên nhiều metric để tạo một đường mới (tỉ lệ, trung bình, tổng). Một cái **phát hiện bất thường**, một cái **tính toán/gộp số**.

---

## 1. Anomaly Detection

**Bài toán gốc:** alarm thường bắt đặt ngưỡng cứng ("CPU > 80% thì kêu"). Nhưng tải lên xuống theo giờ: ban ngày CPU 70% là bình thường, 3h sáng mà 70% lại bất thường. Ngưỡng cứng không phân biệt được: đặt thấp thì kêu nhầm ban ngày, đặt cao thì bỏ sót ban đêm.

**Cách hoạt động:** CloudWatch nhìn lịch sử metric, học nhịp lặp theo giờ/ngày, vẽ một **band** (dải kỳ vọng). Trong band = bình thường (không kêu). Ngoài band = bất thường (kêu).

```
CPU %
 80 |                      . <- diem nay NGOAI band -> ALARM
    |         ___________
 60 |       /  vung ky    \___        <- band (vung ky vong)
    |   ___/   vong (binh thuong) \___
 40 | /                               \
    +----------------------------------------> thoi gian
      0h    6h    12h    18h    24h
```

**Analogy:** như huyết áp. Bác sĩ không dùng một con số cứng cho mọi người; họ biết "lúc nghỉ của bạn thường 110-130", đo ra 170 thì báo động dù 170 với người khác có khi bình thường. Band là "khoảng bình thường của riêng metric này".

*Chỗ analogy gãy:* huyết áp con người ít đổi theo giờ, còn band CloudWatch tự uốn theo chu kỳ ngày/đêm, nên cùng một giá trị lúc này bình thường, lúc khác lại bất thường.

**Tham số chính:** `Anomaly detection threshold` = số lần độ lệch chuẩn (standard deviation). Số càng lớn, band càng rộng, càng ít kêu. Lab d1-04 để `2`.

**Khi nào dùng / không dùng:**

| Dùng anomaly detection | Dùng static threshold (ngưỡng cứng) |
|---|---|
| Tải lên xuống theo giờ/mùa, khó đặt một con số | Giới hạn rõ ràng, bất biến |
| "Bất thường so với chính nó" | "Vượt một mốc tuyệt đối" |
| CPU theo lưu lượng người dùng | Disk > 90%, phải báo bất kể giờ nào |

---

## 2. Metric Math

**Bài toán gốc:** một metric đơn lẻ nhiều khi không đủ. Có `Errors` và `Invocations` nhưng cái cần là **tỉ lệ lỗi**. Có CPU của 5 instance nhưng muốn xem **CPU trung bình cả cụm**. Metric math tính ra con số thực sự quan tâm.

**Cách hoạt động:** gán tên cho từng metric (`m1`, `m2`...) rồi viết biểu thức. CloudWatch tính ra một chuỗi thời gian mới, vẽ lên graph hoặc đặt alarm trên nó.

```
m1 = Errors        (vi du: 5)
m2 = Invocations   (vi du: 200)

Bieu thuc:  (m1 / m2) * 100  =  2.5   -> error rate 2.5%
```

**Vài hàm hay dùng:**
- `m1/m2*100` -> tính tỉ lệ (error rate, hit rate).
- `AVG(METRICS())` -> trung bình mọi metric đang có (gộp CPU nhiều instance).
- `SUM([m1,m2])` -> cộng gộp (tổng request nhiều target).

**Analogy:** như bảng tính Excel. Mỗi metric là một cột số liệu thô; metric math là ô công thức `=B2/C2*100` tạo cột mới "tỉ lệ". Bạn không nhập tay cột mới, nó tự tính từ cột gốc.

*Chỗ analogy gãy:* Excel tính trên ô tĩnh, còn metric math tính liên tục theo thời gian thực, mỗi điểm thời gian một kết quả.

**Khi nào dùng:** cần tỉ lệ (lỗi/tổng), gộp nhiều metric (nhiều instance/Region), đặt alarm trên con số tổng hợp thay vì từng metric lẻ. Gộp cross-Region cần bật detailed monitoring ở các instance.

---

## 3. So Sánh Nhanh

| | Anomaly detection | Metric math |
|---|---|---|
| Làm gì | Phát hiện giá trị bất thường | Tính toán / gộp metric |
| Đầu ra | Band + alarm khi ra ngoài band | Một metric mới (đường mới) |
| Trả lời câu hỏi | "Cái này có lạ không?" | "Con số tổng hợp là bao nhiêu?" |
| Ví dụ | CPU vọt bất thường lúc 3h sáng | Error rate = lỗi/tổng * 100 |

---

## 4. Mẹo Nhớ (exam)
- Đề nói "ngưỡng khó đặt vì tải thay đổi theo thời gian" / "phát hiện bất thường" -> **anomaly detection**.
- Đề nói "tính error rate", "gộp CPU nhiều instance/Region", "tỉ lệ phần trăm" -> **metric math**.

---

## 5. Câu Tự Kiểm Tra
Bạn có một API, lượng truy cập ban ngày cao, ban đêm gần như 0. Bạn muốn: (1) báo khi số lỗi so với tổng request vượt 5%, (2) báo khi lưu lượng truy cập "lạ" so với nhịp thường ngày. Mỗi yêu cầu dùng anomaly detection hay metric math, và vì sao?

<details>
<summary>Đáp án</summary>

(1) **Metric math**: viết biểu thức `errors/requests*100` rồi đặt alarm static > 5 trên đường mới đó. Đây là một tỉ lệ cố định, ngưỡng rõ ràng.

(2) **Anomaly detection**: lưu lượng lên xuống mạnh theo giờ (ngày cao, đêm ~0), không có một ngưỡng cứng nào hợp lý. Để CloudWatch học nhịp thường ngày và kêu khi ra ngoài band.
</details>

---

## Nguồn
- Nội dung lab `d1-04` trong project (`README.md`, Phần 4 bước 7-8).
- Kiến thức nền về CloudWatch anomaly detection và metric math (hành vi ổn định).
