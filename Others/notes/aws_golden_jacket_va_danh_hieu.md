# AWS Golden Jacket và Hệ thống danh hiệu AWS

> Tổng hợp ngày 2026-10-15. Danh mục chứng chỉ và chương trình của AWS thay đổi liên tục, nên luôn kiểm tra lại nguồn chính thức trước khi lên kế hoạch.

## 1. AWS Golden Jacket (áo vàng)

Golden Jacket là áo khoác màu vàng gold thêu chữ "AWS Certified", phần thưởng danh giá nhất của chương trình chứng chỉ AWS. Dưới 1% nhân viên AWS cũng sở hữu nó.

### Điều kiện: giữ TẤT CẢ chứng chỉ active cùng lúc

Yêu cầu là sở hữu toàn bộ chứng chỉ AWS đang generally available (GA) và tất cả còn hiệu lực đồng thời tại thời điểm cutoff của đợt xét. Không phải "thi đủ X cái trong Y tháng".

Tại ngày 2026-10-15, trang chính thức `aws.amazon.com/certification/exams/` hiển thị **13 chứng chỉ GA**:

| Cấp | Chứng chỉ |
|---|---|
| Foundational (2) | Cloud Practitioner, AI Practitioner |
| Associate (5) | Solutions Architect, Developer, CloudOps Engineer (tên mới của SysOps Administrator), Data Engineer, Machine Learning Engineer |
| Professional (2) | Solutions Architect Professional, DevOps Engineer Professional |
| Specialty (2) | Security, Advanced Networking |

Ghi chú về con số:
- Nhiều blog 2024-2025 ghi "12". Con số đã lên 13 sau khi AWS thêm AI Practitioner, Data Engineer, ML Engineer.
- Các Specialty cũ (Machine Learning, Database, Data Analytics, SAP on AWS) đã bị khai tử; Specialty hiện chỉ còn Security và Advanced Networking.
- **AI Business Strategist** đang chạy ở dạng Beta. Chứng chỉ Beta thường chưa tính vào yêu cầu Golden Jacket cho tới khi GA; khi GA thì bộ sẽ thành 14.
- Con số chuẩn nhất luôn là "toàn bộ chứng chỉ đang GA tại thời điểm cutoff", nên hãy đếm trực tiếp trên trang exams, bỏ qua các mục gắn nhãn Beta.

### Hiệu lực và mốc thời gian

- Mỗi chứng chỉ có hiệu lực **3 năm**. Phải hoàn tất cả bộ trong vòng ~3 năm kể từ chứng chỉ đầu tiên, nếu không cái đầu hết hạn trước khi xong cái cuối.
- Người đi nhanh thường mất vài tháng đến ~1 năm để thi hết.
- Golden Jacket không tự động gửi khi đủ bộ. AWS trao theo đợt, gắn với sự kiện **re:Invent hàng năm** (khoảng cuối tháng 11 đến đầu tháng 12 tại Las Vegas).

### Quy trình nhận áo (theo đợt gắn với re:Invent)

1. AWS mở form đăng ký Golden Jacket cho năm đó (ví dụ "re:Invent 2025 Golden Jacket Program"). Phải tự đăng ký, AWS không tự quét rồi gửi.
2. AWS kiểm tra tại thời điểm cutoff: tất cả chứng chỉ phải còn hiệu lực đồng thời trong suốt sự kiện. Một cái hết hạn trước ngày đó thì rớt khỏi đợt.
3. Nhận áo trực tiếp tại re:Invent hoặc ship sau đó (có người chờ thêm vài tháng).

Phân biệt: "đủ chứng chỉ còn hiệu lực" = eligible (điều kiện cần). "Cầm được áo" phụ thuộc chu kỳ chương trình, neo vào re:Invent cuối năm. Không thể pass cái cuối vào tháng 3 rồi mong tháng 4 có áo.

Một số năm AWS gắn thêm tiêu chí đóng góp cộng đồng / được ghi nhận trong hệ sinh thái. Phần này không ổn định qua các năm, nên đọc kỹ điều khoản form đăng ký của chính năm định tham gia.

### Đợt tiếp theo

- re:Invent 2025 (1-5/12/2025) đã qua.
- Đợt gần nhất: **AWS re:Invent 2026, ngày 30/11 - 4/12/2026, Las Vegas, NV**.
- Form đăng ký riêng của năm thường mở trước sự kiện vài tuần đến vài tháng. Theo dõi trang Training & Certification và email AWS Certified để bắt form khi mở.

## 2. Hệ thống danh hiệu / chương trình công nhận của AWS

AWS không có một bậc thang danh hiệu tuyến tính từ thấp lên cao. Có nhiều chương trình song song, mỗi cái mục đích khác nhau, có thể chồng lấn.

### 2.1. AWS Community Builder
- Chương trình nộp đơn (application-based), quy mô hàng nghìn người toàn cầu.
- Dành cho người đam mê kỹ thuật và thought leader đang lên, muốn chia sẻ kiến thức (blog, video, open source, nói chuyện).
- Nhiều category theo lĩnh vực (Serverless, Containers, Security, AI/ML, Data...).
- Nhiệm kỳ 1 năm, phải tái nộp đơn hằng năm.
- Thường là điểm khởi đầu, nhưng không bắt buộc phải qua đây mới thành Hero.

### 2.2. AWS Hero
- Mức cao hơn, chọn lọc hơn nhiều (toàn cầu chỉ vài trăm người).
- Không nộp đơn được. Do nhân viên Amazon đề cử, hội đồng xét duyệt theo quý.
- Xét theo đóng góp cộng đồng bền bỉ, không nhìn số chứng chỉ.
- Hai nhóm:
  - **Community Hero**: quảng bá toàn bộ AWS, xây dựng cộng đồng địa phương.
  - **Specialized Hero (Category Hero)**: chuyên sâu 1 lĩnh vực. Hiện có 6 loại: Container, Data, DevTools, AI, Security, Serverless.

### 2.3. AWS User Group Leader
- Người tổ chức, điều hành các AWS User Group / Community Day tại địa phương.
- Có **AWS User Group Leader Award** (trao tại re:Invent, có các hạng mục như Ownership...).

### 2.4. AWS Ambassador (thuộc APN - Partner Network)
- Dành cho nhân viên của các công ty đối tác AWS (APN Partner).
- Là chuyên gia có chứng chỉ, thúc đẩy năng lực AWS nội bộ công ty, tạo nội dung kỹ thuật public, hỗ trợ cộng đồng vùng.
- Ambassador có thể trở thành Hero; Hero chỉ là Ambassador nếu đang làm cho một AWS Partner đủ điều kiện.

### 2.5. AWS Golden Jacket
- Trao cho người giữ toàn bộ chứng chỉ active đồng thời, cộng đóng góp cộng đồng được ghi nhận.
- Công nhận gắn với chứng chỉ, khác bản chất với Hero / Community Builder (gắn với đóng góp cộng đồng).

### 2.6. Student Builder / Student Builder Groups
- Nhánh dành cho sinh viên, tương tự User Group nhưng cho môi trường đại học.

## 3. Phân biệt theo trục công nhận

| Trục | Chương trình | Cách vào | Nhiệm kỳ |
|---|---|---|---|
| Đóng góp cộng đồng | Community Builder | Nộp đơn | 1 năm, tái nộp hằng năm |
| Đóng góp cộng đồng | Hero | Được đề cử (không nộp đơn) | Xét duyệt theo quý |
| Cộng đồng địa phương | User Group Leader | Tổ chức / điều hành user group | Theo hoạt động |
| Đối tác (Partner) | Ambassador | Thuộc công ty APN Partner | Theo chương trình APN |
| Chứng chỉ | Golden Jacket | Đủ bộ chứng chỉ + đăng ký đợt | Theo đợt re:Invent hằng năm |
| Sinh viên | Student Builder | Môi trường đại học | Theo hoạt động |

Không có chuyện "Community Builder lên Hero lên Golden Jacket" như một bậc thang tuyến tính. Chúng là các danh hiệu độc lập, có thể chồng lấn: một người có thể đồng thời là Hero, từng là Community Builder, và có Golden Jacket.

## Nguồn

- [AWS Certification Exams](https://aws.amazon.com/certification/exams/) - nguồn sống để đếm số chứng chỉ GA
- [AWS re:Invent 2025 Golden Jacket Program](https://pages.awscloud.com/GLOBAL-event-T1-AWS-re-Invent-Golden-Jacket-2025-reg.html)
- [AWS re:Invent - plan / justify your trip](https://aws.amazon.com/events/reinvent/plan/justify-your-trip/)
- [AWS Builder Center - Community Builders](https://builder.aws.com/community/community-builders)
- Trang AWS Heroes chính thức
