# Task 4.1 — AWS Pricing Models

> **Exam weight:** Domain 4 = 12% of scored content

## AWS Pricing Fundamentals

AWS có 3 nguyên tắc pricing cơ bản:
1. **Pay for what you use** — không có upfront commitment (trừ Reserved)
2. **Pay less when you reserve** — cam kết dài hạn = giảm giá
3. **Pay less with more usage** — volume discounts (tiered pricing)

---

## Compute Purchasing Options

### On-Demand Instances
- Trả theo **giờ hoặc giây**, không cam kết
- Linh hoạt nhất, đắt nhất
- **Khi nào dùng:** Dev/test, unpredictable workloads, short-term needs

### Reserved Instances (RI)
- Cam kết **1 hoặc 3 năm** → tiết kiệm 40-75%
- **Payment options:**
  - All Upfront — trả hết trước, tiết kiệm nhiều nhất
  - Partial Upfront — trả một phần trước
  - No Upfront — không trả trước, tiết kiệm ít nhất
- **Types:**
  - **Standard RI** — không thay đổi được instance type, tiết kiệm nhiều nhất
  - **Convertible RI** — có thể đổi instance type, tiết kiệm ít hơn
- **Khi nào dùng:** Steady-state workloads, production databases, web servers

**RI trong AWS Organizations:**
- RI có thể được **shared** giữa các accounts trong Organization
- Nếu account mua RI không dùng hết, capacity tự động apply cho accounts khác
- Quản lý qua **management account**

### Spot Instances
- Dùng **unused EC2 capacity** của AWS
- Tiết kiệm **60-90%** so với On-Demand
- AWS có thể **terminate với 2 phút notice** khi cần capacity
- **Khi nào dùng:** Batch processing, data analysis, CI/CD, fault-tolerant workloads
- **Không dùng cho:** Databases, critical applications, stateful workloads

### AWS Savings Plans
- Cam kết **spend một lượng $/hour** trong 1-3 năm
- Linh hoạt hơn Reserved Instances
- **Types:**
  - **Compute Savings Plans** — áp dụng cho EC2, Lambda, Fargate (linh hoạt nhất)
  - **EC2 Instance Savings Plans** — chỉ EC2, tiết kiệm nhiều hơn
  - **SageMaker Savings Plans** — cho SageMaker

### Dedicated Hosts
- **Server vật lý riêng** dành cho bạn
- Kiểm soát instance placement
- **Dùng cho:** BYOL (Bring Your Own License) — Windows Server, SQL Server, Oracle
- Đắt nhất trong các options

### Dedicated Instances
- Instances chạy trên **hardware riêng** (không share với customers khác)
- Khác Dedicated Hosts: không kiểm soát được physical server
- **Dùng cho:** Compliance requirements, isolation

### Capacity Reservations
- **Reserve EC2 capacity** trong một AZ cụ thể
- Không có discount — trả On-Demand price
- Đảm bảo có capacity khi cần (ví dụ: disaster recovery)
- Kết hợp với Savings Plans hoặc RI để có discount

---

## Storage Pricing

### S3 Pricing Factors
- **Storage** — GB/month theo storage class
- **Requests** — GET, PUT, COPY, POST, LIST requests
- **Data transfer** — outbound data transfer (inbound miễn phí)
- **Management features** — S3 Inventory, Analytics, Object Tagging

### Data Transfer Costs
| Transfer | Cost |
|----------|------|
| **Inbound** (vào AWS) | Miễn phí |
| **Outbound** (ra internet) | Tính phí theo GB |
| **Between AZs** (cùng Region) | Tính phí nhỏ |
| **Between Regions** | Tính phí |
| **CloudFront → Internet** | Thấp hơn EC2 → Internet |

---

## Exam Tips

- Spot = rẻ nhất nhưng có thể bị terminate
- Reserved = tiết kiệm nhất cho steady-state (cam kết 1-3 năm)
- Dedicated Hosts = cần cho BYOL licensing
- Savings Plans = linh hoạt hơn RI, áp dụng cho nhiều services
- Data transfer vào AWS = miễn phí; ra internet = tính phí
- RI trong Organizations = shared across accounts tự động
