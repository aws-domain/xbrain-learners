# PFL Answers — Domain 1: Cloud Concepts

> Chỉ mở file này sau khi đã tự trả lời xong trong `_pfl_problems.md`

---

## Bài toán 1.1: Startup cần quyết định on-premises hay cloud

**Lập luận ủng hộ cloud:**
- **Trade CapEx for OpEx:** Không cần bỏ tiền mua server trước khi biết app có thành công không. Startup có thể dùng tiền đó cho product development.
- **Stop guessing capacity:** Không biết traffic → không thể mua đúng lượng server. Cloud cho phép scale up/down theo nhu cầu thực tế.
- **No IT team needed:** AWS quản lý phần cứng, startup tập trung vào code.
- **Go global in minutes:** Nếu app thành công và cần mở rộng ra thị trường mới, cloud làm được ngay.

**Điểm yếu của lập luận:**
- Cloud có thể đắt hơn on-premises về dài hạn nếu workload ổn định và predictable.
- Chi phí data transfer và egress có thể bất ngờ cao.
- Vendor lock-in — phụ thuộc vào AWS.

**Nếu 500 nhân viên, traffic ổn định:**
- Câu trả lời thay đổi một phần. Với workload ổn định và predictable, Reserved Instances hoặc thậm chí on-premises có thể rẻ hơn.
- Tuy nhiên, vẫn cần cân nhắc: chi phí vận hành IT team, chi phí hardware refresh mỗi 3-5 năm, và tính linh hoạt khi cần scale đột ngột.
- **Kết luận:** Hybrid cloud thường là lựa chọn của enterprise — on-premises cho baseline workload, cloud cho spikes.

---

## Bài toán 1.2: Giải thích cloud cho sếp không biết kỹ thuật

**Giải thích cho sếp (3 câu):**
> "Mua server giống như mua xe tải để giao hàng — bạn phải trả tiền ngay cả khi xe đang đỗ trong garage. Thuê AWS giống như dùng dịch vụ giao hàng — bạn chỉ trả khi thực sự cần. Ngoài ra, khi business tăng trưởng, bạn không cần mua thêm xe — chỉ cần đặt thêm chuyến."

**Khi nào on-premises rẻ hơn:**
- Workload chạy 24/7, ổn định, predictable trong nhiều năm
- Công ty đã có đội IT vận hành sẵn
- Yêu cầu compliance đặc biệt (một số ngành tài chính, quốc phòng)
- Thường là sau 3-5 năm với workload không thay đổi

**Economies of scale với công ty nhỏ:**
- AWS tổng hợp nhu cầu của hàng triệu khách hàng → mua phần cứng với giá cực rẻ → chuyển lợi ích đó cho khách hàng qua giá thấp hơn.
- Công ty nhỏ được hưởng giá của "enterprise" mà không cần mua với số lượng lớn.
- AWS liên tục giảm giá theo thời gian (đã giảm giá hơn 100 lần kể từ 2006).

---

## Bài toán 1.3: Đánh giá kiến trúc theo Well-Architected Framework

**Phân tích theo 6 pillars:**

| Pillar | Vi phạm | Cách fix (budget thấp) |
|---|---|---|
| **Operational Excellence** | Dùng root account, không có monitoring | Tạo IAM user, bật CloudWatch basic metrics |
| **Security** | Root account không có MFA, không rõ security group | Bật MFA root, review security group rules |
| **Reliability** | 1 EC2 = single point of failure, không backup | Bật automated backup RDS, snapshot EC2 định kỳ |
| **Performance Efficiency** | Web + DB trên cùng 1 instance tranh nhau resource | Tách DB ra RDS (có thể dùng RDS Free Tier) |
| **Cost Optimization** | Không monitor usage, có thể over-provisioned | Bật Cost Explorer, xem right-sizing recommendations |
| **Sustainability** | Over-provisioned = lãng phí energy | Right-size instance theo actual usage |

**Cải thiện không downtime:**
1. Tạo RDS instance mới → migrate data → update connection string → test → cutover
2. Đặt ALB trước EC2 (không cần downtime)
3. Tạo IAM user, stop dùng root account

---

## Bài toán 1.4: Lên kế hoạch migration

**App A — CRM cũ (Rehost hoặc Retire):**
- **Rehost (Lift & Shift):** Chuyển nguyên xi lên EC2. Nhanh, ít rủi ro, không cần sửa code. Phù hợp nếu app vẫn đang được dùng.
- **Retire:** Nếu ít người dùng và có thể thay thế bằng SaaS CRM (Salesforce, HubSpot) → Repurchase. Nếu không ai dùng → Retire.
- **Chọn Rehost khi:** App vẫn cần thiết nhưng không có người sửa code.
- **Chọn Retire khi:** Có thể thay thế bằng giải pháp tốt hơn hoặc không còn cần thiết.

**App B — Web app hiện đại (Replatform hoặc Refactor):**
- **Replatform:** Chuyển lên Elastic Beanstalk hoặc ECS với ít thay đổi code. Tận dụng managed services.
- **Refactor:** Nếu team muốn tận dụng cloud-native features (auto-scaling, serverless). Tốn thời gian hơn nhưng lợi ích dài hạn cao hơn.
- **Phù hợp nhất:** Replatform trước, Refactor dần dần.

**App C — File server (Rehost hoặc Repurchase):**
- **Rehost:** Chuyển lên EC2 + EFS. Giữ nguyên cách dùng, ít thay đổi cho user.
- **Repurchase (S3):** Rẻ hơn nhiều về storage cost, nhưng user phải thay đổi cách truy cập (không mount như network drive nữa).
- **Trade-off:** S3 rẻ hơn ~80% so với EFS cho cold data, nhưng cần thay đổi workflow của user.

---

## Bài toán 1.5: Tính toán TCO để thuyết phục ban lãnh đạo

**Chi phí biến mất khi lên cloud:**
- Phần cứng server ($50,000) → AWS quản lý
- Điện và làm mát ($30,000) → AWS chịu
- Bảo hiểm và bảo trì phần cứng ($10,000) → không còn
- **Một phần** chi phí nhân sự IT ($40,000) → 2 người IT có thể chuyển sang làm cloud operations

**Chi phí mới xuất hiện:**
- AWS monthly bill (EC2, RDS, S3, networking...)
- Training/certification cho team
- Có thể cần thêm người có kỹ năng cloud
- Data transfer costs (đặc biệt egress)

**Tổng on-premises hiện tại:** $130,000/năm

**Nếu AWS bill cao hơn on-premises — vẫn nên migrate vì:**
- **Agility:** Deploy nhanh hơn → time-to-market ngắn hơn → doanh thu tiềm năng cao hơn
- **Scalability:** Không bị giới hạn bởi phần cứng đã mua
- **Risk reduction:** Không lo hardware failure, disaster recovery dễ hơn
- **Hidden costs:** On-premises thường bị undercount (thời gian IT xử lý sự cố, opportunity cost...)

**Tool cần dùng:** AWS TCO Calculator và AWS Pricing Calculator

---

## Exam-style Questions — Đáp án

**Câu 1:** Một công ty muốn giảm chi phí vận hành data center và tăng tốc độ deploy.

Có thể là **2 advantages**:
- **"Stop spending money on data centers"** — giảm chi phí vận hành data center
- **"Increase speed and agility"** — tăng tốc độ deploy

Đọc kỹ câu hỏi để xác định họ hỏi về advantage nào.

---

**Câu 2:** Pillar nào tập trung vào việc tránh lãng phí tài nguyên không cần thiết?

**Cost Optimization** — tập trung vào việc tránh chi phí không cần thiết, right-sizing resources, và chỉ trả tiền cho những gì thực sự cần.

Lưu ý: **Sustainability** cũng liên quan đến tránh lãng phí nhưng theo góc độ môi trường. Câu hỏi về "chi phí" → Cost Optimization. Câu hỏi về "môi trường/carbon footprint" → Sustainability.

---

**Câu 3:** Migration strategy nào phù hợp khi muốn ít thay đổi nhất?

**Rehost (Lift & Shift)** — chuyển nguyên xi database Oracle lên EC2 mà không thay đổi gì.

Hoặc **Replatform** nếu họ sẵn sàng chuyển sang RDS for Oracle (managed service, ít thay đổi code nhưng AWS quản lý OS và patching).

Không phải **Refactor/Re-architect** vì đó đòi hỏi thay đổi nhiều.

---

**Câu 4:** AWS Pricing Calculator được dùng để làm gì?

Dùng để **ước tính chi phí AWS trước khi deploy** — nhập các dịch vụ và cấu hình dự kiến, tool tính ra monthly/annual cost estimate.

Phân biệt với:
- **AWS Cost Explorer:** Phân tích chi phí **đã phát sinh** (historical data)
- **AWS Budgets:** Đặt ngưỡng cảnh báo cho chi phí **đang chạy**
- **AWS TCO Calculator:** So sánh chi phí on-premises vs cloud
