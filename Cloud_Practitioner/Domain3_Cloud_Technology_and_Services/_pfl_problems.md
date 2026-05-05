# PFL Problems — Domain 3: Cloud Technology and Services

> Tham khảo: `resources/learning-method/problem_first_learning.md`  
> Lý thuyết liên quan: `01_deploying_and_operating.md` đến `08_other_services.md`  
> Đáp án: `_pfl_answers.md`

---

## Cách dùng file này

1. Chọn một bài toán bên dưới
2. **Không đọc lý thuyết trước** — thử phân tích bằng những gì bạn đã biết
3. Khi bị kẹt, mới mở file lý thuyết tương ứng
4. Sau khi có câu trả lời, mở `_pfl_answers.md` để kiểm tra

> Domain 3 chiếm 34% exam — nhiều nhất. Tập trung vào việc hiểu **khi nào dùng dịch vụ nào** thay vì nhớ tính năng của từng dịch vụ.

---

## Level 1 — Foundation (Chọn đúng dịch vụ)

### Bài toán 3.1: Chọn compute service phù hợp

**Tình huống:**
Bạn có 4 workload khác nhau cần deploy:

- **Workload A:** Web app chạy 24/7, cần kiểm soát OS, cài custom software
- **Workload B:** Function xử lý ảnh khi user upload, chạy < 5 giây, không thường xuyên
- **Workload C:** Containerized microservices, team muốn quản lý cluster
- **Workload D:** Containerized app, team không muốn quản lý infrastructure gì cả

**Yêu cầu:**
Chọn compute service phù hợp nhất cho từng workload: EC2, Lambda, ECS/EKS, hay Fargate? Giải thích tại sao.

**Câu hỏi trade-off:**
- Workload B: Lambda vs EC2 Spot — khi nào Lambda tốt hơn? Khi nào EC2 Spot tốt hơn?

*Lý thuyết liên quan: `03_compute_services.md`*

---

### Bài toán 3.2: Chọn storage service phù hợp

**Tình huống:**
Bạn cần lưu trữ các loại data sau:

- **Data A:** Ảnh profile của 1 triệu user, cần truy cập nhanh, public URL
- **Data B:** Database của ứng dụng, cần ACID transactions
- **Data C:** Log files cũ (> 1 năm), hiếm khi truy cập, cần giữ 7 năm vì compliance
- **Data D:** Shared file system, nhiều EC2 instances cùng đọc/ghi đồng thời
- **Data E:** OS disk của EC2 instance

**Yêu cầu:**
Chọn storage service phù hợp: S3, EBS, EFS, S3 Glacier, RDS. Giải thích tại sao.

*Lý thuyết liên quan: `06_storage_services.md`*

---

### Bài toán 3.3: Chọn database service phù hợp

**Tình huống:**
4 use case database:

- **Use case A:** E-commerce app, cần transactions, structured data, SQL queries
- **Use case B:** User session data, cần đọc/ghi cực nhanh (< 1ms), key-value
- **Use case C:** Social network, data dạng graph (ai follow ai, ai bạn bè với ai)
- **Use case D:** Analytics, query trên hàng tỷ rows, không cần real-time

**Yêu cầu:**
Chọn database phù hợp: RDS, DynamoDB, ElastiCache, Neptune, Redshift. Giải thích tại sao.

*Lý thuyết liên quan: `04_database_services.md`*

---

## Level 2 — Integration (Kết hợp nhiều dịch vụ)

### Bài toán 3.4: Thiết kế 3-tier web architecture

**Tình huống:**
Bạn cần deploy một web app e-commerce với yêu cầu:
- Chịu được 10,000 concurrent users
- Tự động scale khi traffic tăng đột biến (flash sale)
- Database không mất data nếu một AZ bị down
- Static assets (ảnh, CSS, JS) load nhanh cho user toàn cầu

**Yêu cầu:**
Vẽ (hoặc mô tả) architecture sử dụng các dịch vụ AWS. Phải bao gồm:
- Tầng presentation (web/CDN)
- Tầng application (compute)
- Tầng data (database/storage)

**Câu hỏi:**
- Dịch vụ nào giúp static assets load nhanh toàn cầu?
- Dịch vụ nào giúp auto-scale EC2?
- Dịch vụ nào giúp database survive khi AZ bị down?

*Lý thuyết liên quan: `02_global_infrastructure.md`, `03_compute_services.md`, `04_database_services.md`, `05_network_services.md`*

---

### Bài toán 3.5: Thiết kế serverless architecture

**Tình huống:**
Startup muốn xây REST API với yêu cầu:
- Không muốn quản lý server
- Budget rất hạn chế (trả theo request, không trả khi idle)
- Cần lưu data có structure
- Dự kiến traffic: 0 đến 10,000 requests/ngày, không đều

**Yêu cầu:**
Thiết kế serverless architecture. Giải thích từng component.

**Break scenario:**
- Nếu Lambda function timeout sau 15 phút, có vấn đề gì?
- Nếu DynamoDB bị throttle, Lambda sẽ xử lý thế nào?

*Lý thuyết liên quan: `03_compute_services.md` (Lambda), `04_database_services.md` (DynamoDB), `05_network_services.md` (API Gateway)*

---

### Bài toán 3.6: Networking — Thiết kế VPC

**Tình huống:**
Bạn cần thiết kế network cho một 3-tier app:
- Web servers: cần accessible từ internet
- App servers: chỉ nhận traffic từ web servers
- Database: không được accessible từ internet, chỉ từ app servers

**Yêu cầu:**
Thiết kế VPC với subnets, security groups, và routing phù hợp.

**Câu hỏi:**
- Public subnet khác private subnet ở điểm nào?
- Internet Gateway vs NAT Gateway — dùng cái nào ở đâu?
- Security Group vs NACL — khi nào dùng cái nào?

*Lý thuyết liên quan: `05_network_services.md`*

---

## Level 3 — Trade-off Decisions

### Bài toán 3.7: Chọn EC2 purchasing option

**Tình huống:**
Công ty bạn có các workload sau:
- **Web server:** Chạy 24/7, traffic ổn định, đã dùng 2 năm
- **Batch processing:** Chạy mỗi đêm 4 tiếng, có thể bị interrupt
- **Dev/test environment:** Chỉ dùng giờ hành chính, tắt cuối tuần
- **Spike handling:** Thêm capacity khi có event đặc biệt, không thể predict

**Yêu cầu:**
Chọn purchasing option phù hợp cho từng workload: On-Demand, Reserved (1yr/3yr), Spot, Savings Plans.

*Lý thuyết liên quan: `03_compute_services.md`*

---

### Bài toán 3.8: Deploy strategy — Chọn cách deploy

**Tình huống:**
Team bạn cần deploy version mới của app. Có 3 lựa chọn:
- **Option A:** Tắt app cũ, deploy app mới (downtime ~10 phút)
- **Option B:** Deploy song song, chuyển traffic dần dần
- **Option C:** Deploy cho 5% user trước, nếu ổn mới rollout toàn bộ

**Câu hỏi:**
- Tên kỹ thuật của từng option là gì?
- AWS service nào hỗ trợ từng option?
- Khi nào nên dùng option nào?

*Lý thuyết liên quan: `01_deploying_and_operating.md`*

---

## Exam-style Questions

Trả lời **không nhìn tài liệu**, sau đó mở `_pfl_answers.md` để kiểm tra:

1. Một công ty cần chạy batch job có thể bị interrupt. EC2 purchasing option nào tiết kiệm nhất?

2. Dịch vụ nào giúp phân phối static content đến user toàn cầu với độ trễ thấp nhất?

3. Một ứng dụng cần shared file system mà nhiều EC2 instances có thể mount đồng thời. Dịch vụ nào phù hợp?

4. Sự khác biệt chính giữa Security Group và Network ACL là gì?

5. Một công ty muốn chạy container mà không cần quản lý EC2 instances. Dịch vụ nào phù hợp?

6. AWS service nào cho phép chạy code mà không cần provision server, và chỉ tính phí khi code đang chạy?

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
