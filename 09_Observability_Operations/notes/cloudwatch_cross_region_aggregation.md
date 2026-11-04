# Gộp Metric Cross-Region: Metric Math + Detailed Monitoring
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation)
**Note liên quan:** `cloudwatch_anomaly_detection_metric_math.md`, `cloudwatch_metrics_explorer.md`, `cloudwatch_getting_started.md`, lab `d1-04`

---

## 0. Tóm Tắt Một Dòng
Muốn **gộp (aggregate)** CPU của EC2 trải **nhiều Region/account** thành một con số: dùng **metric math** (viết math expression), và mọi instance phải bật **detailed monitoring** (chu kỳ 1 phút). KHÔNG có nút "Cross-Region" để aggregate; instance chỉ có basic monitoring bị loại khỏi phép gộp.

---

## 1. Bài Toán Gốc (câu hỏi thi, chọn 2)
Công ty có EC2 trải nhiều VPC ở nhiều Region. Cần gộp CPU của mọi Reserved instance, cách dễ nhất, chi phí thấp nhất.

**Đáp án đúng (2):**
- Tạo CloudWatch dashboard, add widget, chọn **Math expression** dưới Graph Metric để query và gộp CPU của mọi Region.
- **Enable detailed monitoring** cho mọi EC2 instance.

---

## 2. Gỡ Hiểu Lầm Chính: "Không Thấy Nút Cross-Region Đâu"

Phân biệt 2 việc hay bị lẫn:

```
Xem (graph) metric Region khac   -> CO (doi Region nguon cua widget / dropdown goc phai)
Gop (aggregate) nhieu Region     -> KHONG co nut san -> phai dung METRIC MATH
```

- **Cross-Region graphing** (xem metric của Region khác): có thật, đổi Region nguồn của widget là được.
- **Aggregate cross-Region** (cộng/trung bình nhiều Region thành 1 đường): KHÔNG có nút bấm sẵn. Phải viết metric math, ví dụ `AVG(METRICS())` hoặc `SUM(...)`.

Đáp án sai "select Cross-Region under Graph Metric" bịa ra một cái nút **không tồn tại**. Đây là lý do lúc setup trên Console không ai thấy "chỗ cross-Region": nó vốn không có.

---

## 3. Vì Sao Cần Detailed Monitoring

Để gộp metric qua nhiều account/Region, AWS yêu cầu instance bật **detailed monitoring**. Instance chỉ có **basic monitoring KHÔNG được tính vào** phép gộp.

| | Basic monitoring | Detailed monitoring |
|---|---|---|
| Chu kỳ | 5 phút | 1 phút |
| Chi phí | Miễn phí | Tính phí nhẹ |
| Được tính vào aggregate cross-Region | KHÔNG | CÓ |

**Liên hệ lab d1-04 Phần 1:** ô "Enable detailed CloudWatch monitoring" chính là cái này. Lab bật nó vì gộp cross-Region cần nó (và để alarm phản ứng nhanh theo chu kỳ 1 phút).

---

## 4. Vì Sao 3 Đáp Án Kia Sai (bẫy thi)

| Đáp án sai | Lý do loại |
|---|---|
| "Select **Cross-Region** under Graph Metric" | **Không tồn tại nút đó.** Cross-Region graphing có, nhưng aggregate phải qua metric math. Distractor dựng nút ảo. |
| **QuickSight** dashboard | QuickSight là công cụ BI (báo cáo kinh doanh), không dùng để monitor hạ tầng AWS. Sai công cụ, lại tốn thêm chi phí. |
| **Basic monitoring** | Basic (5 phút) không được tính vào aggregate cross-Region. Phải là detailed. |

---

## 5. Từ Khóa Quyết Định Trong Đề
- "**aggregate across multiple Regions**" + "**easiest / minimal cost**" -> **metric math** (không phải nút cross-Region, không phải QuickSight).
- "**aggregate across Regions**" ngầm yêu cầu -> **detailed monitoring** (basic bị loại khỏi phép gộp).

---

## 6. Mẹo Nhớ (exam pattern)
Gặp "gộp metric nhiều Region/account" -> nhớ **cặp đôi**: **metric math + detailed monitoring**. Thấy đáp án nói "nút Cross-Region để aggregate" là bẫy, vì aggregate luôn phải qua math expression.

---

## 7. Câu Tự Kiểm Tra
Một instance chỉ bật basic monitoring (5 phút), các instance còn lại bật detailed. Khi viết metric math gộp CPU cross-Region, instance basic đó có xuất hiện trong kết quả gộp không? Để nó xuất hiện phải đổi gì?

<details>
<summary>Đáp án</summary>

Không. Instance chỉ có basic monitoring bị loại khỏi phép aggregate cross-Region. Để nó được tính vào, phải **enable detailed monitoring** cho instance đó (đổi từ basic 5 phút sang detailed 1 phút).
</details>

---

## Nguồn
- Nội dung câu hỏi thi (tutorialsdojo) và lab `d1-04` trong project.
- Docs AWS chính thức (dẫn trong đáp án đề):
  - [Aggregating statistics / cross-account cross-Region](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GetSingleMetricAllDimensions.html)
  - [Using metric math](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html)
  - [CloudWatch cross-account cross-Region dashboards (launch)](https://aws.amazon.com/about-aws/whats-new/2019/11/amazon-cloudwatch-launches-cross-account-cross-region-dashboards/)
