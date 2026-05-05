# PFL Answers — Domain 4: Billing, Pricing, and Support

> Chỉ mở file này sau khi đã tự trả lời xong trong `_pfl_problems.md`

---

## Bài toán 4.1: Giải thích hóa đơn AWS cho sếp

**AWS Data Transfer pricing:**

| Loại transfer | Chi phí |
|---|---|
| **Inbound** (internet → AWS) | **Miễn phí** |
| **Outbound** (AWS → internet) | Tính phí (~$0.09/GB đầu tiên, giảm dần theo volume) |
| **Same Region, same AZ** | Miễn phí (giữa các services) |
| **Same Region, khác AZ** | Tính phí (~$0.01/GB mỗi chiều) |
| **Cross-Region** | Tính phí (~$0.02/GB) |
| **CloudFront → internet** | Rẻ hơn EC2 → internet |

**Cách giảm Data Transfer cost:**
1. Đặt resources cùng AZ (EC2 và RDS cùng AZ)
2. Dùng CloudFront để serve content thay vì trực tiếp từ EC2/S3
3. Dùng VPC Endpoints để traffic không đi qua internet
4. Compress data trước khi transfer

**Tool phân tích chi phí:**
- **AWS Cost Explorer** — visualize chi phí theo service, region, tag, theo thời gian
- **AWS Cost and Usage Report (CUR)** — raw data chi tiết nhất, dùng với Athena để query

---

## Bài toán 4.2: Chọn Support Plan phù hợp

| Công ty | Support Plan | Lý do |
|---|---|---|
| A — Startup, Free Tier, no production | **Basic** | Miễn phí, đủ cho non-production. Có access AWS docs, forums, Trusted Advisor (7 checks cơ bản). |
| B — SME, production, cần response vài giờ | **Business** | 24/7 phone/chat support, response < 1 giờ cho production down. |
| C — Enterprise, cần TAM, < 15 phút | **Enterprise** | Dedicated TAM, response < 15 phút cho business-critical down. |

**So sánh Support Plans:**

| | Basic | Developer | Business | Enterprise |
|---|---|---|---|---|
| **Giá** | Free | $29/tháng | $100/tháng hoặc 10% bill | $15,000/tháng |
| **24/7 support** | ❌ | ❌ (business hours) | ✅ | ✅ |
| **Phone support** | ❌ | ❌ | ✅ | ✅ |
| **Response (production down)** | N/A | Next business day | < 1 giờ | < 15 phút |
| **TAM** | ❌ | ❌ | ❌ | ✅ |
| **Trusted Advisor (full)** | ❌ (7 checks) | ❌ (7 checks) | ✅ | ✅ |

**Lưu ý exam:** Developer plan chỉ có business hours support, không có 24/7. Nhiều người nhầm.

---

## Bài toán 4.3: Tối ưu chi phí cho một architecture

**3 cách giảm chi phí:**

**1. Chuyển EC2 sang Reserved Instances (~40% tiết kiệm)**
- 10 instances chạy 24/7, ổn định 1 năm → đủ điều kiện commit
- 1-year Reserved Instance: ~40% so với On-Demand
- 3-year Reserved Instance: ~60%

**2. S3 Lifecycle Policy (~46-83% tiết kiệm cho 80% data)**
- 80% data không truy cập trong 90 ngày → chuyển sang S3-IA hoặc Glacier
- S3 Standard: ~$0.023/GB/tháng
- S3 Standard-IA: ~$0.0125/GB/tháng (tiết kiệm ~46%)
- S3 Glacier: ~$0.004/GB/tháng (tiết kiệm ~83%)

**3. RDS Reserved Instance (~40% tiết kiệm)**
- RDS Multi-AZ chạy 24/7, ổn định → commit Reserved

**Bonus — Right-sizing:**
- Dùng **AWS Compute Optimizer** để xem có instance nào over-provisioned không

**Tool cần dùng:**
- **AWS Cost Explorer** → xem spending patterns
- **AWS Trusted Advisor** → cost optimization recommendations
- **AWS Compute Optimizer** → right-sizing recommendations

---

## Bài toán 4.4: Quản lý chi phí cho nhiều team

**Approach 1: AWS Tags + Cost Allocation Tags**
- Tag tất cả resources với key `Team` và value `Frontend`/`Backend`/`Data`
- Activate Cost Allocation Tags trong Billing console
- Dùng Cost Explorer để filter/group by tag
- **Ưu điểm:** Đơn giản, không cần thay đổi account structure
- **Nhược điểm:** Phụ thuộc vào việc team có tag đúng không, không enforce được

**Approach 2: AWS Organizations với separate accounts**
- Tạo separate AWS account cho mỗi team
- Dùng AWS Organizations để quản lý tập trung
- Consolidated Billing → 1 hóa đơn duy nhất nhưng breakdown theo account
- **Ưu điểm:** Isolation tốt hơn, security boundary rõ ràng
- **Nhược điểm:** Phức tạp hơn, cần quản lý nhiều accounts

**Recommendation:**
- Short-term: Tags (nhanh, ít effort)
- Long-term: Separate accounts (best practice cho enterprise)

**AWS Organizations + Consolidated Billing:**
- Quản lý nhiều accounts từ một management account
- Một hóa đơn duy nhất cho tất cả accounts
- Volume discounts được tổng hợp

---

## Bài toán 4.5: Reserved Instance vs Savings Plans

| | Reserved Instance | Savings Plans |
|---|---|---|
| **Commit vào** | Instance type cụ thể (m5.large, us-east-1) | Mức spend ($/hour) |
| **Áp dụng cho** | EC2 cụ thể | EC2 + Lambda + Fargate |
| **Linh hoạt** | Thấp hơn | Cao hơn |
| **Tiết kiệm** | Tương đương | Tương đương |

**Nếu biết sẽ migrate sang Fargate:**
- Chọn **Compute Savings Plans** — áp dụng cho cả EC2 lẫn Fargate
- Reserved Instance chỉ áp dụng cho EC2 → nếu migrate sang Fargate, discount bị mất

**1 năm vs 3 năm:**

| | 1 năm | 3 năm |
|---|---|---|
| **Tiết kiệm** | ~40% | ~60% |
| **Risk** | Thấp hơn | Cao hơn |
| **Flexibility** | Cao hơn | Thấp hơn |

Nếu không chắc về tương lai → 1 năm. Workload rất ổn định → 3 năm.

---

## Bài toán 4.6: Khi nào cần nâng Support Plan?

**Developer vs Business Support:**

| | Developer | Business |
|---|---|---|
| **Giá** | $29/tháng | $100/tháng hoặc 10% AWS bill |
| **Hours** | Business hours | 24/7 |
| **Phone support** | ❌ | ✅ |
| **Production down response** | Next business day | **< 1 giờ** |
| **Trusted Advisor** | 7 checks | Full |
| **AWS Health API** | ❌ | ✅ |

**Business vs Enterprise response time:**
- Business: < 1 giờ (production down), < 4 giờ (production impaired)
- Enterprise: **< 15 phút** (business-critical down), < 1 giờ (production down)

**Khi nào nâng Support Plan là "worth it":**
- **Công thức:** Cost of downtime per hour > Cost of support plan per month → nâng plan.
- Ví dụ: E-commerce app revenue $10,000/ngày → $417/giờ. Business Support $100/tháng là rất worth it.

---

## Exam-style Questions — Đáp án

**Câu 1:** Nhận cảnh báo khi AWS bill vượt $500/tháng?

**AWS Budgets** — đặt budget và nhận alert (email/SNS) khi chi phí thực tế hoặc dự báo vượt ngưỡng.

Phân biệt: AWS Budgets (proactive alert) vs AWS Cost Explorer (phân tích historical data).

---

**Câu 2:** AWS Trusted Advisor cung cấp recommendations về những lĩnh vực nào?

**5 lĩnh vực:**
1. **Cost Optimization** — Identify unused/underutilized resources
2. **Performance** — Improve speed and responsiveness
3. **Security** — Close security gaps
4. **Fault Tolerance** — Increase availability and redundancy
5. **Service Limits** — Check if approaching AWS service limits

Basic/Developer: 7 checks cơ bản. Business/Enterprise: Full access.

---

**Câu 3:** Support Plan rẻ nhất có 24/7 phone support?

**Business Support** ($100/tháng) — plan thấp nhất có 24/7 phone và chat support.

Developer plan chỉ có email support trong business hours.

---

**Câu 4:** Nhiều AWS accounts muốn nhận một hóa đơn duy nhất?

**Consolidated Billing** — tính năng của AWS Organizations, tổng hợp tất cả charges từ member accounts vào một hóa đơn của management account.

Lợi ích thêm: Volume discounts được tổng hợp.

---

**Câu 5:** AWS Free Tier có mấy loại?

**3 loại:**

1. **Always Free** — Không expire, luôn miễn phí trong giới hạn nhất định
   - Ví dụ: Lambda 1 triệu requests/tháng, DynamoDB 25GB storage

2. **12 Months Free** — Miễn phí 12 tháng kể từ ngày tạo account
   - Ví dụ: EC2 t2.micro 750 giờ/tháng, S3 5GB, RDS 750 giờ/tháng

3. **Trials** — Short-term free trial cho một số services
   - Ví dụ: Amazon SageMaker 2 tháng

---

**Câu 6:** Dịch vụ nào visualize và phân tích chi phí AWS theo thời gian?

**AWS Cost Explorer** — interactive graphs để visualize chi phí và usage theo thời gian, filter theo service/region/tag, và forecast chi phí tương lai.

Phân biệt với AWS Budgets (đặt alert) và AWS Pricing Calculator (ước tính trước khi deploy).
