# Task 4.3 — AWS Technical Resources and Support Options

> **Exam weight:** Domain 4 = 12% of scored content

## AWS Support Plans

| | Basic | Developer | Business | Enterprise On-Ramp | Enterprise |
|---|---|---|---|---|---|
| **Giá** | Miễn phí | $29/month | $100/month | $5,500/month | $15,000/month |
| **Technical support** | Không | Business hours | 24/7 | 24/7 | 24/7 |
| **Response time (critical)** | N/A | N/A | < 1 hour | < 30 min | < 15 min |
| **Trusted Advisor** | 7 checks | 7 checks | Full | Full | Full |
| **TAM** | Không | Không | Không | Pool of TAMs | Dedicated TAM |
| **Concierge** | Không | Không | Không | Không | Có |

### Basic Support
- Miễn phí cho tất cả AWS accounts
- Truy cập: documentation, whitepapers, AWS re:Post
- AWS Trusted Advisor: 7 core checks
- AWS Health Dashboard

### Developer Support
- Phù hợp cho: development và testing
- Email support trong business hours
- 1 primary contact

### Business Support
- Phù hợp cho: production workloads
- 24/7 phone, email, chat support
- Full Trusted Advisor checks
- AWS Support API
- Third-party software support

### Enterprise On-Ramp Support
- Phù hợp cho: business-critical workloads
- Pool of Technical Account Managers (TAMs)
- Concierge Support Team
- Infrastructure Event Management (một lần/năm)

### Enterprise Support
- Phù hợp cho: mission-critical workloads
- **Dedicated Technical Account Manager (TAM)**
- Concierge Support Team
- Infrastructure Event Management (không giới hạn)
- Well-Architected Reviews
- Operations Reviews

---

## AWS Technical Resources

### AWS Documentation
- docs.aws.amazon.com
- User guides, API references, developer guides
- Luôn cập nhật, chính xác nhất

### AWS Whitepapers
- In-depth technical papers về AWS services và best practices
- Topics: security, architecture, cost optimization...
- aws.amazon.com/whitepapers

### AWS Knowledge Center
- FAQ và hướng dẫn giải quyết vấn đề phổ biến
- aws.amazon.com/premiumsupport/knowledge-center

### AWS re:Post
- **Community Q&A platform** (thay thế AWS Forums)
- Hỏi đáp với AWS experts và community
- repost.aws

### AWS Prescriptive Guidance
- **Step-by-step guidance** cho specific use cases
- Migration patterns, modernization strategies
- aws.amazon.com/prescriptive-guidance

### AWS Blogs
- aws.amazon.com/blogs
- Announcements, tutorials, case studies

---

## AWS Trusted Advisor

5 categories:
1. **Cost Optimization** — Idle resources, underutilized instances
2. **Performance** — High utilization, CloudFront optimization
3. **Security** — Open ports, MFA on root, public S3 buckets
4. **Fault Tolerance** — Multi-AZ, backups, Route 53 health checks
5. **Service Limits** — Approaching service quotas

**Free checks (Basic/Developer):** 7 core security và service limit checks  
**Full checks (Business/Enterprise):** 100+ checks across all categories

---

## AWS Health Dashboard

### Service Health Dashboard
- Status của tất cả AWS services theo Region
- Lịch sử incidents
- URL: health.aws.amazon.com

### AWS Health (Personal Health Dashboard)
- **Personalized view** về events ảnh hưởng đến **account của bạn**
- Proactive notifications về scheduled maintenance
- Tích hợp với EventBridge để automate responses
- AWS Health API — programmatic access

---

## AWS Partner Network (APN)

### Independent Software Vendors (ISVs)
- Công ty phát triển **software products** chạy trên AWS
- Ví dụ: Datadog, Splunk, HashiCorp

### System Integrators (SIs)
- Công ty **tư vấn và triển khai** AWS solutions
- Ví dụ: Accenture, Deloitte, Wipro

### AWS Marketplace
- **Digital catalog** với hàng nghìn software listings
- Mua, deploy, manage third-party software
- Billing tích hợp vào AWS bill
- Categories: Security, Networking, Storage, ML, DevOps...
- **Benefits:** Simplified procurement, flexible pricing, quick deployment

### Partner Benefits
- Partner training và certification
- Partner events và summits
- Volume discounts
- Co-selling với AWS

---

## AWS Professional Services

- AWS team của **consultants** giúp achieve business outcomes
- Work alongside customer teams
- Dùng cho: large migrations, complex architectures

### AWS Solutions Architects
- **Technical experts** giúp design AWS solutions
- Available qua AWS Support (Business/Enterprise)
- Không tính phí riêng (included trong support plan)

---

## AWS Trust and Safety Team

- Report **abuse của AWS resources**
- Ví dụ: spam, phishing, malware, DDoS attacks từ AWS IPs
- Contact: aws.amazon.com/forms/report-abuse

---

## Exam Tips

- Basic = miễn phí; Developer = email only; Business = 24/7 phone
- TAM = chỉ có Enterprise On-Ramp và Enterprise
- Trusted Advisor full checks = cần Business hoặc Enterprise
- AWS Health = personalized alerts cho account của bạn
- AWS Marketplace = mua third-party software, billing qua AWS
- re:Post = community forum (thay thế AWS Forums)
- Trust and Safety = report abuse, không phải security incidents
