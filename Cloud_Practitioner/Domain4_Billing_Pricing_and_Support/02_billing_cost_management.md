# Task 4.2 — Billing, Budget, and Cost Management

> **Exam weight:** Domain 4 = 12% of scored content

## AWS Cost Management Tools

### AWS Cost Explorer
- **Visualize và analyze** chi phí và usage theo thời gian
- Xem trends, identify cost drivers
- **Rightsizing recommendations** — gợi ý instance types phù hợp hơn
- Forecast chi phí 12 tháng tới
- Miễn phí để sử dụng

### AWS Budgets
- **Đặt ngưỡng chi phí** và nhận alerts khi vượt
- Types:
  - **Cost Budget** — alert khi chi phí vượt threshold
  - **Usage Budget** — alert khi usage vượt threshold
  - **Reservation Budget** — track RI/Savings Plans utilization
  - **Savings Plans Budget** — track Savings Plans coverage
- Gửi notifications qua Email hoặc SNS
- Có thể trigger **automated actions** (ví dụ: stop EC2 instances)

### AWS Pricing Calculator
- **Ước tính chi phí** trước khi triển khai
- Không cần AWS account
- URL: calculator.aws
- Dùng cho: planning, budgeting, TCO analysis

### AWS Cost and Usage Report (CUR)
- **Báo cáo chi tiết nhất** về chi phí và usage
- Granularity: hourly, daily, monthly
- Lưu vào S3, có thể query bằng Athena
- Dùng cho: detailed billing analysis, chargeback

---

## AWS Organizations

### Tổng quan
- Quản lý **nhiều AWS accounts** tập trung
- **Management account** (root) quản lý member accounts
- Tổ chức accounts theo **Organizational Units (OUs)**

### Consolidated Billing
- **Một hóa đơn** cho tất cả accounts trong Organization
- **Volume discounts** — tổng usage của tất cả accounts được tính chung
- **RI và Savings Plans sharing** — tự động share giữa accounts
- Management account chịu trách nhiệm thanh toán

### Service Control Policies (SCPs)
- **Giới hạn permissions** cho accounts/OUs
- Không grant permissions — chỉ restrict
- Áp dụng cho tất cả users và roles trong account (kể cả root)

---

## Cost Allocation Tags

### Tổng quan
- **Labels** gắn vào AWS resources để track chi phí
- Ví dụ: `Environment: Production`, `Team: Backend`, `Project: WebApp`

### Types
- **AWS-generated tags** — tự động tạo bởi AWS (ví dụ: `aws:createdBy`)
- **User-defined tags** — bạn tự tạo

### Activation
- Tags phải được **activate** trong Billing console mới xuất hiện trong reports
- Sau khi activate, xuất hiện trong Cost Explorer và CUR

### Use Cases
- Phân bổ chi phí theo team, project, environment
- Chargeback/showback cho internal departments
- Identify resources không có tags (untagged resources)

---

## Billing Support

### AWS Billing Dashboard
- Xem current month charges
- Month-to-date spending
- Forecasted charges

### AWS Free Tier
- **12 tháng miễn phí** cho new accounts (một số services)
- **Always free** — một số services luôn miễn phí (Lambda 1M requests/month, DynamoDB 25GB...)
- **Trials** — short-term free trials cho specific services
- Theo dõi Free Tier usage trong Billing Dashboard

---

## Exam Tips

- Cost Explorer = analyze past costs, forecast future
- AWS Budgets = set alerts khi vượt budget
- Pricing Calculator = estimate costs trước khi dùng
- Organizations = manage multiple accounts, consolidated billing
- Cost allocation tags = track costs by team/project/environment
- Consolidated billing = volume discounts + single invoice
- CUR = most detailed billing report, stored in S3
