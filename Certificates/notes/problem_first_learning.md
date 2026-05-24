# Problem-First Learning — Phương pháp học AWS hiệu quả

## Tổng quan

**Problem-First Learning (PFL)** là phương pháp học bằng cách xuất phát từ một bài toán thực tế, sau đó tìm hiểu các dịch vụ/concept cần thiết để giải quyết bài toán đó — thay vì học từng dịch vụ một cách rời rạc rồi mới tìm cách áp dụng.

> **Nguyên tắc cốt lõi:** Não người không nhớ thông tin rời rạc. Não chỉ nhớ khi thông tin gắn với một vấn đề cần giải quyết, một quyết định cần đưa ra, hoặc một sai lầm đã mắc phải.

---

## Tại sao cách học truyền thống không hiệu quả

| Cách học truyền thống | Problem-First Learning |
|---|---|
| Học EC2 → học S3 → học RDS → ... | Đặt bài toán → tìm ra cần EC2, S3, RDS |
| Đọc docs từ đầu đến cuối | Đọc đúng phần cần để giải quyết vấn đề |
| Nhớ định nghĩa dịch vụ | Nhớ *khi nào dùng* và *tại sao chọn cái này thay vì cái kia* |
| Kiến thức rời rạc, dễ quên | Kiến thức gắn với context, khó quên hơn |
| Thực hành sau khi học lý thuyết | Lý thuyết và thực hành xen kẽ nhau |

---

## Cấu trúc một session học theo PFL

Mỗi session học nên đi theo 5 bước sau:

### Bước 1: Đặt bài toán (5-10 phút)
Bắt đầu bằng một tình huống thực tế, không phải định nghĩa.

**Ví dụ tốt:**
> "Tôi cần deploy một REST API cho mobile app, dự kiến 10,000 requests/ngày, cần scale tự động, và không muốn quản lý server."

**Ví dụ không tốt:**
> "Hôm nay tôi sẽ học Lambda."

Bài toán tốt cần có:
- Một **yêu cầu chức năng** (làm được gì)
- Một **ràng buộc** (scale, cost, availability, security...)
- Một **ngữ cảnh** (loại app, team size, budget...)

### Bước 2: Phân tích và đặt câu hỏi (10-15 phút)
Trước khi đọc bất kỳ tài liệu nào, tự hỏi:

- Bài toán này cần giải quyết vấn đề gì?
- Tôi đã biết gì có thể áp dụng?
- Tôi chưa biết gì? Cần tìm hiểu thêm gì?
- Có những lựa chọn nào? Trade-off của mỗi lựa chọn là gì?

Viết ra giấy hoặc file trước khi tra cứu. Đây là bước quan trọng nhất — nó kích hoạt tư duy chủ động thay vì tiếp thu thụ động.

### Bước 3: Nghiên cứu có định hướng (30-60 phút)
Chỉ đọc những gì cần để trả lời câu hỏi ở Bước 2. Không đọc toàn bộ docs của một dịch vụ.

Khi đọc, luôn giữ câu hỏi trong đầu:
- *"Cái này giải quyết vấn đề gì của tôi?"*
- *"Khi nào thì KHÔNG nên dùng cái này?"*
- *"Cái này khác gì với [alternative]?"*

### Bước 4: Thực hành — Build, Break, Fix (60-120 phút)
Đây là trọng tâm của PFL.

**Build:** Tự tay xây dựng solution cho bài toán. Không làm theo step-by-step tutorial — chỉ dùng docs khi bị kẹt.

**Break:** Sau khi build xong, cố tình phá vỡ nó:
- Xóa một security group → điều gì xảy ra?
- Thay đổi IAM policy → permission nào bị ảnh hưởng?
- Tắt một subnet → traffic đi đâu?
- Giảm memory Lambda xuống mức tối thiểu → latency thay đổi thế nào?

**Fix:** Debug và khôi phục. Quá trình này dạy bạn nhiều hơn bất kỳ tutorial nào.

### Bước 5: Feynman + Ghi chép có cấu trúc (15-20 phút)
Sau khi hoàn thành, đóng tất cả tài liệu lại và:

1. **Giải thích lại bài toán và solution** bằng lời của mình, như đang dạy người khác
2. **Ghi chép theo template PFL** (xem phần dưới)
3. **Đặt câu hỏi mở rộng** cho session tiếp theo

---

## Template ghi chép PFL

Mỗi bài học nên được ghi lại theo format này:

```markdown
## [Tên bài toán]

### Bài toán
[Mô tả tình huống thực tế]

### Câu hỏi ban đầu
- [Những gì tôi chưa biết trước khi bắt đầu]

### Solution
[Kiến trúc/approach đã chọn]

### Tại sao chọn cách này?
[So sánh với các lựa chọn khác, trade-off]

### Những gì tôi học được
- [Concept 1]: [Giải thích bằng lời của mình]
- [Concept 2]: [Giải thích bằng lời của mình]

### Khi nào dùng / Khi nào KHÔNG dùng
| Dùng khi | Không dùng khi |
|---|---|
| ... | ... |

### Điều bất ngờ / Sai lầm đã mắc
[Những gì không như kỳ vọng, lỗi gặp phải và cách fix]

### Câu hỏi mở rộng cho lần sau
- [Câu hỏi 1]
- [Câu hỏi 2]
```

---

## Cách AI đồng hành theo phương pháp PFL

Khi học một topic mới, bạn có thể yêu cầu AI hỗ trợ theo các mode sau:

### Mode 1: Tạo bài toán (Problem Generator)
Prompt mẫu:
> "Tôi vừa học xong [topic]. Hãy tạo cho tôi 3 bài toán thực tế theo phương pháp PFL, từ dễ đến khó, có ràng buộc rõ ràng để tôi phải suy nghĩ về trade-off."

### Mode 2: Socratic Guide (Không cho đáp án ngay)
Prompt mẫu:
> "Tôi đang giải bài toán [mô tả]. Tôi đang nghĩ đến [approach của tôi]. Đừng cho tôi đáp án — hãy hỏi tôi những câu hỏi để tôi tự tìm ra vấn đề."

### Mode 3: Review Solution
Prompt mẫu:
> "Đây là solution của tôi cho bài toán [mô tả]: [solution]. Hãy review theo góc độ: (1) correctness, (2) cost, (3) security, (4) scalability. Chỉ ra điểm yếu và gợi ý cải thiện."

### Mode 4: Break Scenario
Prompt mẫu:
> "Tôi đã build [architecture]. Hãy đưa ra 5 tình huống failure hoặc edge case để tôi thử phá vỡ và debug solution của mình."

### Mode 5: Feynman Check
Prompt mẫu:
> "Tôi sẽ giải thích [concept] bằng lời của mình. Hãy nghe và chỉ ra chỗ nào tôi hiểu sai hoặc thiếu: [giải thích của tôi]."

---

## Bộ bài toán mẫu theo level

### Level 1 — Foundation (tuần 1-2)
Phù hợp khi mới bắt đầu với một domain.

1. *"Deploy một static website có thể chịu được 1 triệu lượt truy cập/tháng với chi phí thấp nhất có thể."*
2. *"Lưu trữ file upload từ user (ảnh, video) sao cho an toàn và chỉ user đó mới xem được."*
3. *"Tạo một user cho developer mới, chỉ được phép đọc S3 bucket cụ thể, không được làm gì khác."*

### Level 2 — Integration (tuần 3-4)
Khi đã quen với từng dịch vụ, bắt đầu kết hợp.

1. *"Xây REST API không cần server, tự động scale, trả về data từ database. Budget: dưới $10/tháng cho 100k requests."*
2. *"Khi user upload file lên S3, tự động resize ảnh và lưu vào bucket khác. Không được dùng server thường trực."*
3. *"Deploy web app sao cho: dev team push code lên GitHub → tự động test → tự động deploy lên staging."*

### Level 3 — Production-like (tuần 5-8)
Gần với thực tế production.

1. *"Thiết kế architecture cho e-commerce app: 99.9% uptime, auto-scale khi flash sale, database không mất data khi AZ bị down."*
2. *"Migrate một monolith app đang chạy trên EC2 sang containerized architecture. Zero downtime trong quá trình migrate."*
3. *"Thiết kế hệ thống logging và alerting: biết ngay khi error rate tăng đột biến, có thể trace một request từ đầu đến cuối."*

### Level 4 — Trade-off Decisions (tháng 3+)
Không có đáp án đúng duy nhất — phải justify lựa chọn.

1. *"Khách hàng cần chạy batch job xử lý 10GB data mỗi đêm. So sánh: EC2 Spot, Lambda, Fargate, EMR. Chọn cái nào và tại sao?"*
2. *"Team đang tranh luận giữa RDS Multi-AZ và Aurora Serverless cho một SaaS app có traffic không đều. Phân tích và đưa ra recommendation."*
3. *"Công ty muốn giảm AWS bill 30% mà không ảnh hưởng performance. Audit architecture hiện tại và đề xuất."*

---

## Dấu hiệu bạn đang học đúng theo PFL

✅ Bạn có thể giải thích tại sao chọn dịch vụ A thay vì B trong một tình huống cụ thể  
✅ Khi gặp lỗi, bạn biết bắt đầu debug từ đâu  
✅ Bạn tự đặt được câu hỏi "Điều gì xảy ra nếu..." trước khi thử  
✅ Bạn nhớ kiến thức vì gắn với một lần bạn tự tay build hoặc fix  
✅ Bạn có thể vẽ lại architecture từ đầu mà không cần nhìn tài liệu  

## Dấu hiệu bạn đang học sai

❌ Đọc docs xong nhưng không biết dùng vào đâu  
❌ Làm theo tutorial step-by-step nhưng thay đổi một bước là không biết làm gì  
❌ Nhớ định nghĩa nhưng không nhớ khi nào nên dùng  
❌ Chưa bao giờ tự đặt bài toán, chỉ làm theo bài có sẵn  
❌ Không biết tại sao solution của mình lại tốn nhiều tiền  

---

## Lưu ý khi dùng tài liệu này với AI

Khi bắt đầu một session học mới, paste đoạn sau vào đầu cuộc trò chuyện:

```
Tôi đang học [topic] theo phương pháp Problem-First Learning.
Hãy đồng hành với tôi theo cách sau:
- Không cho đáp án ngay khi tôi chưa thử
- Hỏi tôi câu hỏi để kích thích tư duy thay vì giải thích thụ động
- Khi tôi đưa ra solution, hãy review theo góc độ: correctness, cost, security, scalability
- Tạo bài toán có ràng buộc rõ ràng để tôi phải suy nghĩ về trade-off
- Nhắc tôi làm bước Break sau khi Build xong

Topic hôm nay: [topic]
```
