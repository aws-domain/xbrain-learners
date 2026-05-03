# Task 1.4 — Cloud Economics

> **Exam weight:** Domain 1 = 24% of scored content

## Fixed Costs vs Variable Costs

| | Fixed Costs (On-premises) | Variable Costs (Cloud) |
|---|---|---|
| **Đặc điểm** | Trả trước, không đổi theo mức dùng | Trả theo mức dùng thực tế |
| **Ví dụ** | Mua server, thuê data center | AWS EC2 On-Demand, S3 storage |
| **Rủi ro** | Over-provision hoặc under-provision | Không có rủi ro capacity |
| **Linh hoạt** | Thấp | Cao |

---

## Chi phí On-Premises

Khi tự vận hành data center, tổ chức phải chịu:

- **Hardware** — Mua server, storage, networking equipment
- **Facilities** — Thuê/xây data center, điện, làm mát (cooling)
- **Staff** — Nhân viên vận hành, bảo trì, bảo mật
- **Software licenses** — OS, database, middleware
- **Maintenance** — Sửa chữa, nâng cấp phần cứng
- **Disaster recovery** — Backup site, redundant hardware

> Tất cả những chi phí này **biến mất hoặc giảm đáng kể** khi chuyển lên AWS.

---

## Licensing Strategies

### Bring Your Own License (BYOL)
- Mang license hiện có (ví dụ: Windows Server, SQL Server) lên AWS
- Phù hợp khi đã có license dài hạn
- Dùng với **Dedicated Hosts** để đáp ứng yêu cầu license

### Included Licenses
- License được tính vào giá AWS (ví dụ: Amazon RDS for SQL Server)
- Đơn giản hơn, không cần quản lý license riêng
- Phù hợp khi không có license sẵn hoặc muốn đơn giản hóa

---

## Rightsizing

**Rightsizing** = chọn đúng loại và kích thước tài nguyên AWS phù hợp với nhu cầu thực tế.

- Tránh over-provisioning (dùng instance quá lớn, lãng phí tiền)
- Tránh under-provisioning (dùng instance quá nhỏ, ảnh hưởng performance)
- Công cụ hỗ trợ: **AWS Trusted Advisor**, **AWS Compute Optimizer**

---

## Benefits of Automation

- **Giảm chi phí nhân công** — Tự động hóa các tác vụ lặp đi lặp lại
- **Giảm lỗi do con người** — Scripts và IaC nhất quán hơn thao tác thủ công
- **Scale nhanh hơn** — Auto Scaling phản ứng ngay lập tức với thay đổi tải
- **Ví dụ:** AWS CloudFormation, AWS Lambda, Auto Scaling Groups

---

## Economies of Scale

AWS tổng hợp nhu cầu của **hàng triệu khách hàng** → mua phần cứng với số lượng lớn → giá thành thấp hơn → chuyển lợi ích cho khách hàng qua việc **giảm giá liên tục**.

> AWS đã giảm giá hơn 100 lần kể từ khi ra mắt năm 2006.

---

## Total Cost of Ownership (TCO)

TCO = tổng chi phí thực sự khi so sánh on-premises vs cloud, bao gồm:
- Chi phí trực tiếp (hardware, software)
- Chi phí gián tiếp (staff, facilities, downtime)

**AWS Pricing Calculator** — công cụ ước tính chi phí AWS trước khi triển khai.

---

## Exam Tips

- Fixed cost = CapEx = on-premises; Variable cost = OpEx = cloud
- Rightsizing giúp tối ưu Cost Optimization pillar
- BYOL phù hợp với Dedicated Hosts
- Economies of scale = lý do AWS có thể giảm giá liên tục
