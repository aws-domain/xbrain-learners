# PFL Problems — Domain 1: Cloud Concepts

> Tham khảo: `resources/learning-method/problem_first_learning.md`  
> Lý thuyết liên quan: `01_benefits_of_aws_cloud.md`, `02_well_architected_framework.md`, `03_cloud_migration_strategies.md`, `04_cloud_economics.md`  
> Đáp án: `_pfl_answers.md`

---

## Cách dùng file này

1. Chọn một bài toán bên dưới
2. **Không đọc lý thuyết trước** — thử phân tích bằng những gì bạn đã biết
3. Khi bị kẹt, mới mở file lý thuyết tương ứng
4. Sau khi có câu trả lời, mở `_pfl_answers.md` để kiểm tra

---

## Level 1 — Foundation

### Bài toán 1.1: Startup cần quyết định on-premises hay cloud

**Tình huống:**
Một startup 5 người đang xây dựng app mobile. CTO muốn mua server vật lý để tiết kiệm chi phí dài hạn. CEO lo ngại rủi ro. Bạn được mời tư vấn.

**Ràng buộc:**
- Budget ban đầu hạn chế
- Không có đội IT vận hành
- Không biết traffic sẽ như thế nào trong 6 tháng đầu

**Câu hỏi cần trả lời:**
- Lập luận nào ủng hộ cloud thay vì on-premises trong trường hợp này?
- Đâu là điểm yếu của lập luận đó?
- Nếu startup này có 500 nhân viên và traffic ổn định, câu trả lời có thay đổi không?

*Lý thuyết liên quan: `01_benefits_of_aws_cloud.md` — 6 Advantages, CapEx vs OpEx*

---

### Bài toán 1.2: Giải thích cloud cho sếp không biết kỹ thuật

**Tình huống:**
Sếp của bạn hỏi: *"Tại sao chúng ta phải trả tiền cho AWS mỗi tháng thay vì mua server một lần?"*

**Yêu cầu:**
Giải thích bằng ngôn ngữ kinh doanh (không dùng thuật ngữ kỹ thuật) trong 3 câu.

**Câu hỏi mở rộng:**
- Khi nào thì on-premises lại rẻ hơn cloud về dài hạn?
- "Economies of scale" của AWS có nghĩa gì với một công ty nhỏ?

*Lý thuyết liên quan: `01_benefits_of_aws_cloud.md` — Value Proposition, CapEx vs OpEx*

---

## Level 2 — Integration

### Bài toán 1.3: Đánh giá kiến trúc theo Well-Architected Framework

**Tình huống:**
Một team đã deploy web app như sau:
- 1 EC2 instance duy nhất chạy cả web server lẫn database
- Không có backup
- Tất cả traffic đi thẳng vào EC2, không có load balancer
- Dùng root account AWS để deploy

**Yêu cầu:**
Phân tích kiến trúc này theo từng pillar của Well-Architected Framework. Chỉ ra vi phạm cụ thể ở mỗi pillar.

**Ràng buộc:**
- Budget tối thiểu để cải thiện
- Không được downtime khi refactor

*Lý thuyết liên quan: `02_well_architected_framework.md`*

---

### Bài toán 1.4: Lên kế hoạch migration

**Tình huống:**
Công ty bạn đang chạy 3 hệ thống on-premises:
- **App A:** CRM cũ, code từ 2010, không ai dám sửa
- **App B:** Web app hiện đại, đang phát triển tích cực
- **App C:** File server nội bộ, 10TB data, ít người dùng

**Yêu cầu:**
Đề xuất migration strategy (6 Rs) cho từng app. Giải thích tại sao.

**Câu hỏi trade-off:**
- App A: Rehost vs Retire — khi nào nên chọn cái nào?
- App C: Rehost vs Repurchase (dùng S3/EFS) — chi phí và complexity khác nhau thế nào?

*Lý thuyết liên quan: `03_cloud_migration_strategies.md`*

---

## Level 3 — Trade-off Decisions

### Bài toán 1.5: Tính toán TCO để thuyết phục ban lãnh đạo

**Tình huống:**
Ban lãnh đạo yêu cầu bạn chứng minh bằng số liệu rằng chuyển sang AWS sẽ tiết kiệm chi phí. Hiện tại công ty đang chi:
- $50,000/năm cho phần cứng server
- $30,000/năm cho điện và làm mát data center
- $40,000/năm cho 2 nhân viên IT vận hành server
- $10,000/năm cho bảo hiểm và bảo trì

**Yêu cầu:**
- Liệt kê những chi phí nào sẽ biến mất khi lên cloud
- Liệt kê những chi phí mới nào sẽ xuất hiện
- Dùng AWS Pricing Calculator để ước tính chi phí AWS tương đương
- Kết luận: có nên migrate không?

**Câu hỏi khó:**
- Nếu AWS bill cao hơn on-premises, có vẫn nên migrate không? Tại sao?

*Lý thuyết liên quan: `04_cloud_economics.md`*

---

## Exam-style Questions

Trả lời **không nhìn tài liệu**, sau đó mở `_pfl_answers.md` để kiểm tra:

1. Một công ty muốn giảm chi phí vận hành data center và tăng tốc độ deploy. Đây là ví dụ của advantage nào trong 6 advantages của AWS cloud?

2. Theo Well-Architected Framework, pillar nào tập trung vào việc tránh lãng phí tài nguyên không cần thiết?

3. Một công ty muốn chuyển database Oracle lên cloud với ít thay đổi nhất có thể. Migration strategy nào phù hợp nhất?

4. AWS Pricing Calculator được dùng để làm gì?

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
