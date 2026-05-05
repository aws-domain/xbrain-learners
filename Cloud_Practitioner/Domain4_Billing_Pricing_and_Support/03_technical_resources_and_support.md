# Task 4.3 — Technical Resources and AWS Support

> **Exam weight:** Domain 4 = 12% of scored content

> ⚠️ **Lưu ý quan trọng cho kỳ thi CLF-C02:**  
> AWS đang trong quá trình thay đổi cấu trúc Support Plans (hiệu lực từ 1/1/2027):
> - **Developer Support** → bị discontinued, thay bằng **Business Support+**
> - **Business Support** → bị discontinued, thay bằng **Business Support+**
> - **Enterprise On-Ramp** → bị discontinued, tự động upgrade lên **Enterprise Support**
>
> Tuy nhiên, **đề thi CLF-C02 hiện tại vẫn hỏi về 4 plans cũ** (Basic, Developer, Business, Enterprise).  
> Học cả hai để an toàn.

---

## AWS Support Plans (4 plans — vẫn xuất hiện trong exam)

### Basic Support
- **Giá:** Miễn phí (tất cả AWS accounts)
- **Technical support:** Không có
- **Trusted Advisor:** 7 core checks (Security + Service Limits)
- **Bao gồm:** Documentation, whitepapers, AWS re:Post forums, Service Health Dashboard
- **Dùng cho:** Non-production, learning, experimentation

### Developer Support
- **Giá:** $29/tháng hoặc 3% monthly AWS charges (lấy cái cao hơn)
- **Technical support:** Email trong **business hours** (8AM–6PM theo timezone của account)
- **Contacts:** 1 primary contact, unlimited cases
- **Response time:**
  - General guidance: < 24 business hours
  - System impaired: < 12 business hours
- **Trusted Advisor:** 7 core checks
- **Dùng cho:** Development và testing environments

### Business Support
- **Giá:** $100/tháng hoặc % monthly charges (10% cho $0–$10K, giảm dần theo volume)
- **Technical support:** **24/7** phone, email, chat
- **Contacts:** Unlimited contacts, unlimited cases
- **Response time:**
  - General guidance: < 24 giờ
  - System impaired: < 12 giờ
  - Production system impaired: **< 4 giờ**
  - Production system down: **< 1 giờ**
- **Trusted Advisor:** Full access (tất cả checks)
- **AWS Health API:** ✅
- **Third-party software support:** ✅
- **Dùng cho:** Production workloads

### Enterprise On-Ramp Support
- **Giá:** $5,500/tháng hoặc 10% monthly charges
- **Technical support:** 24/7 phone, email, chat
- **Response time:**
  - Business-critical system down: **< 30 phút**
- **TAM:** Access to a **pool of TAMs** (không dedicated)
- **Concierge Support Team:** ✅
- **Dùng cho:** Production và business-critical workloads

### Enterprise Support
- **Giá:** $15,000/tháng (đang giảm xuống $5,000 theo thông báo mới)
- **Technical support:** 24/7 phone, email, chat
- **Response time:**
  - Business-critical system down: **< 15 phút**
- **TAM:** **Dedicated** Technical Account Manager
- **Concierge Support Team:** ✅
- **Infrastructure Event Management:** Included
- **Well-Architected Reviews:** Included
- **Dùng cho:** Mission-critical workloads, large enterprises

---

## So sánh Support Plans (bảng thi quan trọng)

| | Basic | Developer | Business | Enterprise |
|---|---|---|---|---|
| **Giá** | Free | $29/tháng | $100/tháng | $15,000/tháng |
| **24/7 support** | ❌ | ❌ (business hours) | ✅ | ✅ |
| **Phone support** | ❌ | ❌ | ✅ | ✅ |
| **Production down response** | N/A | N/A | **< 1 giờ** | **< 15 phút** |
| **Trusted Advisor** | 7 checks | 7 checks | Full | Full |
| **TAM** | ❌ | ❌ | ❌ | ✅ (dedicated) |
| **Health API** | ❌ | ❌ | ✅ | ✅ |

---

## AWS Trusted Advisor

### Tổng quan
- Công cụ **tự động kiểm tra** AWS environment và đưa ra recommendations
- Giống như "người cố vấn" kiểm tra best practices

### 5 Categories
1. **Cost Optimization** — Identify unused/underutilized resources, RI recommendations
2. **Performance** — Improve speed and responsiveness
3. **Security** — Close security gaps, enable security features
4. **Fault Tolerance** — Increase availability and redundancy
5. **Service Limits** — Check if approaching AWS service quotas

### Access Levels
- **Basic/Developer:** 7 core checks (chủ yếu Security và Service Limits)
- **Business/Enterprise:** Full access — 500+ checks across all 5 categories

---

## AWS Technical Account Manager (TAM)

- **Dedicated advisor** cho Enterprise customers
- Proactively monitor environment, identify issues trước khi xảy ra
- Hỗ trợ planning, architecture reviews, operational reviews
- Điểm liên hệ chính với AWS
- **Chỉ có ở Enterprise Support plan** (dedicated) — Enterprise On-Ramp có pool of TAMs

---

## Các Technical Resources khác

### AWS Knowledge Center
- **FAQ và how-to guides** cho các vấn đề phổ biến
- Miễn phí, không cần support plan

### AWS re:Post
- **Community Q&A platform** (thay thế AWS Forums cũ)
- Hỏi và trả lời từ AWS experts, employees, và community
- Miễn phí cho tất cả
- URL: repost.aws

### AWS IQ
- Kết nối customers với **AWS Certified third-party experts**
- Experts giúp implement solutions, migrate workloads
- Thanh toán qua AWS account

### AWS Managed Services (AMS)
- AWS **vận hành infrastructure** thay cho bạn
- Handles patching, monitoring, backup, incident management
- Dành cho enterprises muốn outsource cloud operations

### AWS Professional Services
- **AWS consultants** giúp implement cloud strategies
- Dành cho large-scale migrations và transformations

---

## AWS Marketplace

- **Digital catalog** với hàng nghìn third-party software
- Mua software và charges xuất hiện trên AWS bill
- Categories: Security, Networking, Storage, ML, DevOps...
- Vendors: Palo Alto, Splunk, Datadog, MongoDB...

---

## AWS Health Dashboard

### Service Health Dashboard
- Hiển thị **trạng thái của tất cả AWS services** theo region
- Public, không cần đăng nhập
- URL: health.aws.amazon.com

### Personal Health Dashboard (AWS Health)
- Hiển thị events **ảnh hưởng đến account của bạn** cụ thể
- Scheduled maintenance, service degradations, security notifications
- **Business/Enterprise:** Access qua AWS Health API

---

## AWS Artifact

- Portal để download **compliance reports và certifications** của AWS
- SOC 1/2/3, PCI DSS, ISO 27001, HIPAA BAA...
- Miễn phí, accessible qua AWS Console
- Dùng để chứng minh với auditors rằng AWS infrastructure đáp ứng compliance requirements

---

## Exam Tips

- Developer plan = email only, **business hours** — **không có 24/7**
- Business plan = **minimum** để có 24/7 phone support + production down < 1 giờ
- Enterprise = **dedicated TAM** + < 15 phút response
- Trusted Advisor full access = **Business plan trở lên**
- TAM dedicated = **chỉ Enterprise** (On-Ramp có pool, không dedicated)
- AWS Artifact = compliance reports — **không phải support tool**
- re:Post = community forum, miễn phí cho tất cả
- Personal Health Dashboard = events ảnh hưởng đến **account của bạn** cụ thể (khác Service Health Dashboard là global)
