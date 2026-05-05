# PFL Problems — Domain 4: Billing, Pricing, and Support

> Tham khảo: `resources/learning-method/problem_first_learning.md`  
> Lý thuyết liên quan: `01_pricing_models.md`, `02_billing_cost_management.md`, `03_technical_resources_and_support.md`  
> Đáp án: `_pfl_answers.md`

---

## Cách dùng file này

1. Chọn một bài toán bên dưới
2. **Không đọc lý thuyết trước** — thử phân tích bằng những gì bạn đã biết
3. Khi bị kẹt, mới mở file lý thuyết tương ứng
4. Sau khi có câu trả lời, mở `_pfl_answers.md` để kiểm tra

> Domain 4 chỉ chiếm 12% nhưng là "điểm dễ lấy". Tập trung vào: Support plans, pricing models, và cost optimization tools.

---

## Level 1 — Foundation

### Bài toán 4.1: Giải thích hóa đơn AWS cho sếp

**Tình huống:**
Tháng này AWS bill của công ty là $5,000 — cao hơn tháng trước $2,000. Sếp hỏi tại sao.

Bạn nhìn vào bill và thấy:
- EC2: $2,000 (tăng $500)
- RDS: $1,500 (không đổi)
- S3: $800 (tăng $300)
- Data Transfer: $700 (tăng $1,200 ← đây là nguyên nhân chính)

**Câu hỏi:**
- AWS tính phí Data Transfer như thế nào? (inbound vs outbound, same region vs cross-region vs internet)
- Làm thế nào để giảm chi phí Data Transfer?
- Dùng tool nào để phân tích chi phí theo từng dịch vụ?

*Lý thuyết liên quan: `01_pricing_models.md`, `02_billing_cost_management.md`*

---

### Bài toán 4.2: Chọn Support Plan phù hợp

**Tình huống:**
3 công ty với nhu cầu khác nhau:

- **Công ty A:** Startup 3 người, dùng AWS Free Tier, chưa có production workload
- **Công ty B:** SME 50 người, có production app, đôi khi gặp vấn đề kỹ thuật, cần response trong vài giờ
- **Công ty C:** Enterprise, AWS là core infrastructure, cần dedicated Technical Account Manager, response < 15 phút khi production down

**Yêu cầu:**
Chọn Support Plan phù hợp cho từng công ty: Basic, Developer, Business, Enterprise. Giải thích tại sao và so sánh chi phí.

**Câu hỏi:**
- Support Plan nào mới có access vào AWS Trusted Advisor đầy đủ?
- Support Plan nào mới có Technical Account Manager (TAM)?

*Lý thuyết liên quan: `03_technical_resources_and_support.md`*

---

## Level 2 — Integration

### Bài toán 4.3: Tối ưu chi phí cho một architecture

**Tình huống:**
Công ty đang chạy architecture sau và muốn giảm chi phí 30%:
- 10 EC2 On-Demand instances chạy 24/7 (đã dùng ổn định 1 năm)
- RDS Multi-AZ chạy 24/7
- S3 bucket chứa 50TB data, 80% không được truy cập trong 90 ngày
- CloudFront distribution cho static assets

**Yêu cầu:**
Đề xuất ít nhất 3 cách cụ thể để giảm chi phí. Ước tính % tiết kiệm cho mỗi cách.

**Câu hỏi:**
- EC2 On-Demand vs Reserved Instance: tiết kiệm được bao nhiêu %?
- S3 Lifecycle Policy làm được gì?
- AWS Cost Explorer dùng để làm gì?

*Lý thuyết liên quan: `01_pricing_models.md`, `02_billing_cost_management.md`*

---

### Bài toán 4.4: Quản lý chi phí cho nhiều team

**Tình huống:**
Công ty bạn có 3 team dùng chung một AWS account:
- Team Frontend, Team Backend, Team Data

Cuối tháng không ai biết team nào đang tốn bao nhiêu tiền. CFO yêu cầu phải có báo cáo chi phí theo từng team.

**Yêu cầu:**
Đề xuất cách tổ chức để track chi phí theo team. Có ít nhất 2 approach khác nhau.

**Câu hỏi:**
- AWS Tags dùng như thế nào để track cost?
- AWS Organizations và Consolidated Billing giải quyết vấn đề gì?
- Cost Allocation Tags là gì?

*Lý thuyết liên quan: `02_billing_cost_management.md`*

---

## Level 3 — Trade-off Decisions

### Bài toán 4.5: Reserved Instance vs Savings Plans

**Tình huống:**
Công ty bạn đang dùng:
- 5 EC2 instances `m5.large` ở `us-east-1`, chạy 24/7
- Dự kiến trong 1 năm tới sẽ migrate một số workload sang Fargate

**Câu hỏi:**
- Reserved Instance (EC2) vs Savings Plans — cái nào linh hoạt hơn?
- Nếu bạn biết sẽ migrate sang Fargate, nên chọn cái nào? Tại sao?
- Commitment 1 năm vs 3 năm — trade-off là gì?

*Lý thuyết liên quan: `01_pricing_models.md`*

---

### Bài toán 4.6: Khi nào cần nâng Support Plan?

**Tình huống:**
Công ty đang dùng Developer Support Plan ($29/tháng). Một ngày production app bị down lúc 3 giờ sáng. Bạn mở ticket với AWS nhưng response time là "next business day".

**Câu hỏi:**
- Business Support Plan có gì khác? Chi phí là bao nhiêu?
- Nếu production down, response time của Business vs Enterprise là bao nhiêu?
- Ngoài response time, Business Support còn có gì mà Developer không có?
- Khi nào thì chi phí nâng Support Plan là "worth it"?

*Lý thuyết liên quan: `03_technical_resources_and_support.md`*

---

## Exam-style Questions

Trả lời **không nhìn tài liệu**, sau đó mở `_pfl_answers.md` để kiểm tra:

1. Một công ty muốn nhận cảnh báo khi AWS bill vượt quá $500/tháng. Dịch vụ nào dùng để thiết lập điều này?

2. AWS Trusted Advisor cung cấp recommendations về những lĩnh vực nào?

3. Support Plan nào là rẻ nhất mà vẫn có 24/7 phone support?

4. Một công ty có nhiều AWS accounts muốn nhận một hóa đơn duy nhất. Tính năng nào của AWS Organizations giúp điều này?

5. AWS Free Tier có mấy loại? Kể tên và sự khác biệt.

6. Dịch vụ nào giúp visualize và phân tích chi phí AWS theo thời gian?

---

## Ghi chép của tôi

```markdown
### [Tên bài toán]
**Ngày:** 
**Thời gian:** 
**Solution của tôi:** 

**Điều tôi chưa biết trước khi làm:**

**Điều bất ngờ / sai lầm:**

**Câu hỏi mở rộng cho lần sau:**
```
