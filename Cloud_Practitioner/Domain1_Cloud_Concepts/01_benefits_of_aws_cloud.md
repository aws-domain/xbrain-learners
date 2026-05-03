# Task 1.1 — Benefits of the AWS Cloud

> **Exam weight:** Domain 1 = 24% of scored content

## Value Proposition of the AWS Cloud

AWS Cloud mang lại giá trị thông qua việc loại bỏ chi phí đầu tư cơ sở hạ tầng ban đầu (CapEx) và chuyển sang mô hình chi phí vận hành (OpEx) — bạn chỉ trả tiền cho những gì bạn dùng.

---

## 6 Advantages of Cloud Computing (AWS)

| # | Advantage | Giải thích |
|---|-----------|-----------|
| 1 | **Trade fixed expense for variable expense** | Không cần mua server trước, trả theo mức dùng thực tế |
| 2 | **Benefit from massive economies of scale** | AWS tổng hợp nhu cầu của hàng triệu khách hàng → giá thấp hơn |
| 3 | **Stop guessing capacity** | Scale up/down theo nhu cầu thực, không lo over/under-provision |
| 4 | **Increase speed and agility** | Deploy trong vài phút thay vì vài tuần |
| 5 | **Stop spending money on data centers** | Tập trung vào business, không lo vận hành phần cứng |
| 6 | **Go global in minutes** | Deploy ứng dụng trên nhiều AWS Regions chỉ với vài click |

---

## Global Infrastructure Benefits

### Speed of Deployment
- Provision resources trong vài phút qua AWS Management Console, CLI, hoặc API
- Không cần chờ mua, ship, rack, và cài đặt phần cứng vật lý

### Global Reach
- AWS có **Regions** trên khắp thế giới (Americas, Europe, Asia Pacific, Middle East, Africa)
- Dễ dàng phục vụ người dùng ở nhiều quốc gia với độ trễ thấp

---

## High Availability, Elasticity, and Agility

### High Availability (Tính sẵn sàng cao)
- Thiết kế hệ thống chạy liên tục, giảm thiểu downtime
- Sử dụng nhiều **Availability Zones (AZs)** trong một Region
- Nếu một AZ gặp sự cố, traffic tự động chuyển sang AZ khác

### Elasticity (Tính co giãn)
- Tự động **scale out** (thêm tài nguyên) khi tải tăng
- Tự động **scale in** (giảm tài nguyên) khi tải giảm
- Ví dụ: Auto Scaling Groups cho EC2, DynamoDB on-demand capacity

### Agility (Tính linh hoạt)
- Rút ngắn thời gian từ ý tưởng đến triển khai
- Thử nghiệm nhanh, fail fast, iterate nhanh hơn
- Giảm chi phí và rủi ro khi thử nghiệm công nghệ mới

---

## Key Terms

| Term | Định nghĩa |
|------|-----------|
| **CapEx** | Capital Expenditure — chi phí đầu tư cố định (mua server) |
| **OpEx** | Operational Expenditure — chi phí vận hành biến đổi (thuê cloud) |
| **On-premises** | Hạ tầng tự quản lý tại chỗ |
| **Scalability** | Khả năng tăng/giảm tài nguyên theo nhu cầu |
| **Fault tolerance** | Hệ thống tiếp tục hoạt động dù có thành phần bị lỗi |
