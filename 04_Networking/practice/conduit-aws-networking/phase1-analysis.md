# Phase 1 — Phân tích & Thiết kế

> **Thời gian:** ~2 giờ  
> **Mục tiêu:** Hiểu hệ thống, quyết định AWS architecture, estimate cost, vẽ diagram  
> **Tools:** AWS Pricing Calculator, AWS Console (Budgets setup)

---

## 1.1 Đọc hiểu hệ thống

Trước khi thiết kế bất cứ thứ gì trên AWS, bạn cần hiểu hệ thống đang chạy như thế nào.

Đọc file `system-context.md` và trả lời các câu hỏi sau (tự trả lời trước khi xem gợi ý):

**Câu hỏi 1:** Conduit có bao nhiêu component? Chúng giao tiếp với nhau qua port nào?

<details>
<summary>Gợi ý</summary>

3 component chính:
- Frontend (React) — port 3000
- Backend (Node.js) — port 3001
- Database (PostgreSQL) — port 5432

Frontend gọi Backend qua HTTP `/api/*`
Backend gọi Database qua TCP port 5432

</details>

**Câu hỏi 2:** Component nào cần kết nối ra internet? Component nào không cần?

<details>
<summary>Gợi ý</summary>

- **Frontend:** Cần — user browser kết nối vào
- **Backend:** Cần outbound — để pull npm packages khi setup, gọi third-party API
- **Database:** KHÔNG cần — chỉ cần giao tiếp với Backend trong nội bộ

→ Đây là cơ sở để quyết định subnet nào cho từng component.

</details>

**Câu hỏi 3:** Component nào là "sensitive" nhất cần bảo vệ kỹ nhất?

<details>
<summary>Gợi ý</summary>

Database — chứa toàn bộ dữ liệu người dùng. Không bao giờ expose ra internet.

</details>

---

## 1.2 Quyết định AWS Architecture

### Bước 1: Mapping component → AWS Service

Điền vào bảng này (tự điền trước khi xem đáp án):

| Component | AWS Service | Lý do |
|-----------|-------------|-------|
| Frontend (React static) | ? | ? |
| Backend (Node.js API) | ? | ? |
| Database (PostgreSQL) | ? | ? |
| Load Balancer | ? | ? |

<details>
<summary>Đáp án + Lý do chi tiết</summary>

| Component | AWS Service | Lý do |
|-----------|-------------|-------|
| Frontend | **EC2 t2.micro + Nginx** | Free Tier, serve static files đơn giản. Alternative: S3 + CloudFront (rẻ hơn nhưng phức tạp hơn cho workshop) |
| Backend | **EC2 t2.micro** | Free Tier, full control, Node.js chạy trực tiếp. Alternative: Elastic Beanstalk (managed nhưng ít học được) |
| Database | **RDS PostgreSQL db.t3.micro** | Managed service — AWS lo backup, patching OS, HA. Free Tier 750h/tháng |
| Load Balancer | **Bỏ qua trong Phase 1** | ALB tốn phí, không có Free Tier. Dùng trực tiếp EC2 IP cho workshop này |

**Tại sao không dùng ALB ngay?**
ALB tốn ~$0.008/giờ + $0.008/LCU. Với workshop học Networking, ta học được nhiều hơn khi tự cấu hình Security Group chain mà không có ALB ở giữa. ALB sẽ là phần nâng cao.

</details>

### Bước 2: Quyết định Subnet placement

Đây là quyết định quan trọng nhất trong Networking design.

**Nguyên tắc:** Đặt component vào subnet có mức độ access tối thiểu cần thiết.

| Component | Subnet type | Lý do |
|-----------|-------------|-------|
| Frontend EC2 | **Public subnet** | User cần truy cập trực tiếp từ internet |
| Backend EC2 | **Private subnet** | Chỉ Frontend mới cần gọi vào, không expose ra internet |
| RDS PostgreSQL | **Isolated subnet** | Chỉ Backend mới cần gọi vào, không cần internet |
| NAT Gateway | **Public subnet** | NAT GW phải đặt ở public subnet để forward traffic ra internet |

> **Well-Architected — Security Pillar:** "Apply security at all layers" — mỗi layer chỉ nhận traffic từ layer ngay trên nó.

### Bước 3: Quyết định CIDR

Thiết kế IP space cho VPC:

```
VPC: 10.0.0.0/16  (65,536 IPs — đủ dùng cho mọi thứ)

AZ-1a (ap-southeast-1a):
  Public Subnet:   10.0.1.0/24  (254 IPs — cho Frontend, NAT GW)
  Private Subnet:  10.0.2.0/24  (254 IPs — cho Backend)
  Isolated Subnet: 10.0.3.0/24  (254 IPs — cho RDS)

AZ-1b (ap-southeast-1b):  ← RDS cần ít nhất 2 AZ
  Isolated Subnet: 10.0.4.0/24  (254 IPs — RDS standby)
```

**Tại sao /24 cho mỗi subnet?**
- 254 IPs dùng được (AWS reserve 5)
- Đủ cho workshop, dễ nhớ
- Trong production: tính toán kỹ hơn dựa trên số lượng instance

**Tại sao cần AZ-1b cho RDS?**
RDS yêu cầu **DB Subnet Group** phải có subnet ở ít nhất 2 AZ — dù bạn chỉ deploy 1 instance.

---

## 1.3 Vẽ Architecture Diagram

### As-Is Diagram (Local)

```
┌─────────────────────────────────────────┐
│              Local Machine              │
│                                         │
│  ┌──────────┐    ┌──────────────────┐  │
│  │ Browser  │───►│ Frontend :3000   │  │
│  └──────────┘    │ (React dev)      │  │
│                  └────────┬─────────┘  │
│                           │ /api/*     │
│                  ┌────────▼─────────┐  │
│                  │ Backend :3001    │  │
│                  │ (Node.js)        │  │
│                  └────────┬─────────┘  │
│                           │ :5432      │
│                  ┌────────▼─────────┐  │
│                  │ PostgreSQL :5432 │  │
│                  └──────────────────┘  │
└─────────────────────────────────────────┘
```

### To-Be Diagram (AWS Target Architecture)

```
Internet
    │
    │ HTTP :80
    ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS Region: ap-southeast-1                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  VPC: 10.0.0.0/16                                   │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  Public Subnet: 10.0.1.0/24 (AZ-1a)         │  │   │
│  │  │                                              │  │   │
│  │  │  ┌─────────────────┐  ┌──────────────────┐  │  │   │
│  │  │  │  EC2 t2.micro   │  │  NAT Gateway     │  │  │   │
│  │  │  │  Frontend+Nginx │  │  + Elastic IP    │  │  │   │
│  │  │  │  :80            │  │                  │  │  │   │
│  │  │  └────────┬────────┘  └──────────────────┘  │  │   │
│  │  └───────────┼──────────────────────────────────┘  │   │
│  │              │ :3001 (API calls)                    │   │
│  │  ┌───────────▼──────────────────────────────────┐  │   │
│  │  │  Private Subnet: 10.0.2.0/24 (AZ-1a)        │  │   │
│  │  │                                              │  │   │
│  │  │  ┌─────────────────────────────────────┐    │  │   │
│  │  │  │  EC2 t2.micro                       │    │  │   │
│  │  │  │  Backend (Node.js) :3001            │    │  │   │
│  │  │  └────────────────────┬────────────────┘    │  │   │
│  │  └───────────────────────┼────────────────────-┘  │   │
│  │                          │ :5432                   │   │
│  │  ┌───────────────────────▼──────────────────────┐  │   │
│  │  │  Isolated Subnet: 10.0.3.0/24 (AZ-1a)       │  │   │
│  │  │  Isolated Subnet: 10.0.4.0/24 (AZ-1b)       │  │   │
│  │  │                                              │  │   │
│  │  │  ┌─────────────────────────────────────┐    │  │   │
│  │  │  │  RDS PostgreSQL db.t3.micro         │    │  │   │
│  │  │  │  :5432                              │    │  │   │
│  │  │  └─────────────────────────────────────┘    │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Security Group Chain

```
Internet
    │
    │ allow :80, :443 from 0.0.0.0/0
    ▼
[SG: sg-frontend]
    │
    │ allow :3001 from sg-frontend only
    ▼
[SG: sg-backend]
    │
    │ allow :5432 from sg-backend only
    ▼
[SG: sg-database]
```

---

## 1.5 Estimate Cost — AWS Pricing Calculator

Trong thực tế, **trước khi deploy bất cứ thứ gì**, engineer phải estimate cost và trình bày với team/manager. Đây là bước không thể bỏ qua.

### Pricing Calculator vs Workload Estimate — Dùng cái nào?

AWS có 2 tool estimate khác nhau, dễ nhầm:

| | **calculator.aws** | **Workload Estimate (Console)** |
|---|---|---|
| Truy cập | https://calculator.aws — **không cần đăng nhập** | AWS Console → Cost Explorer |
| Mục đích | Lên kế hoạch **trước khi deploy** | Phân tích workload **đang chạy** |
| Dữ liệu | Bạn tự nhập thủ công | Có thể pull từ usage thực tế |
| Free Tier | **Không tự apply** — luôn hiển thị giá On-Demand | **Không tự apply** — cũng hiển thị giá On-Demand |

> ⚠️ **Lưu ý quan trọng:** Cả 2 tool đều **không trừ Free Tier** vào kết quả hiển thị. Chúng luôn show giá On-Demand đầy đủ. Free Tier chỉ được apply tự động trên **bill thực tế** cuối tháng — bạn sẽ thấy dòng "Free Tier Discount" trong invoice.

Workshop này dùng **calculator.aws** vì không cần đăng nhập và phù hợp để estimate trước khi deploy.

### Dùng AWS Pricing Calculator

URL: **https://calculator.aws/pricing/2/home**

**Bước 1:** Vào https://calculator.aws → **Create estimate**

**Bước 2:** Thêm từng service — click **Add service**, search tên service:

**EC2 (x2 instances):**
- Search "EC2" → Configure
- Region: Asia Pacific (Singapore)
- Tenancy: Shared Instances
- OS: Linux
- Instance type: **t2.micro**
- Number of instances: **2**
- Usage amount: **730** Hrs/month (730h = 1 tháng chạy liên tục)
- EBS Storage: gp3, **8 GB** mỗi instance
- → Calculator hiển thị: ~**$21/tháng** (giá On-Demand đầy đủ)
- → Thực tế bạn trả: **$0** nếu còn trong Free Tier 12 tháng đầu

**RDS PostgreSQL:**
- Search "RDS" → Configure
- Region: Asia Pacific (Singapore)
- Usage type: `APS1-InstanceUsage:db.t3.micro`
- Operation: `CreateDBInstance:0002` (Single-AZ)
- Usage amount: **730** Hrs
- → Calculator hiển thị: ~**$19/tháng**
- → Thực tế bạn trả: **$0** nếu còn trong Free Tier

**NAT Gateway:**
- Search "NAT Gateway" → Configure
- Region: Asia Pacific (Singapore)
- Hours: **8** hours (1 ngày workshop)
- Data processed: **1** GB
- → Kết quả: ~**$0.36** ($0.045/h × 8h + $0.045/GB × 1GB)
- → **Không có Free Tier — đây là khoản duy nhất bạn thực sự trả**

**Tổng estimate hiển thị trên calculator: ~$40/tháng**
**Chi phí thực tế bạn trả cho 1 ngày workshop: ~$0.36–$1** (chỉ NAT Gateway)

> **Tại sao vẫn nên làm bước này dù biết Free Tier?** Vì trong thực tế bạn sẽ estimate cho hệ thống production không có Free Tier. Luyện thói quen estimate trước khi deploy là kỹ năng quan trọng.

> **Lưu ý Free Tier:** 750h/tháng áp dụng cho **tổng tất cả EC2 t2.micro cộng lại**. Chạy 2 instance cùng lúc = 1460h/tháng → vượt Free Tier sau ~15 ngày. Xem bill thực tế tại Console → Billing → Bills.

**Export estimate:** Pricing Calculator → **Share** → Copy link (lưu lại hoặc share với team)

---

## 1.6 Setup Cost Guard — AWS Budgets

**Làm ngay trước khi deploy bất cứ thứ gì.** Đây là bước đầu tiên mọi engineer nên làm khi bắt đầu dùng AWS account.

AWS Budgets cho phép set alert khi chi phí vượt ngưỡng — tránh "bill shock" cuối tháng.

### Setup Zero Spend Budget (Free Tier protection)

Vào **AWS Console → Billing → Budgets → Create budget**

**Cách nhanh nhất — dùng template:**
1. Chọn **Use a template (simplified)**
2. Chọn **Zero spend budget**
3. Email: nhập email của bạn
4. → AWS sẽ alert ngay khi có **bất kỳ charge nào** (kể cả $0.01)

**Cách thủ công (hiểu rõ hơn):**
1. Budget type: **Cost budget**
2. Budget amount: **$5** (ngưỡng an toàn cho workshop)
3. Alert threshold: **80%** ($4) → nhận email cảnh báo sớm
4. Alert threshold thứ 2: **100%** ($5) → alert khi đạt ngưỡng

```
Billing Console → Budgets → Create budget
  ├── Template: Zero spend budget    ← dùng cái này trước
  └── Custom: $5 budget với 80% alert ← thêm cái này để có buffer
```

> **Từ AWS Docs:** Free Tier usage alerts tự động notify qua email khi bạn vượt **85%** giới hạn Free Tier của từng service. Enable tại: Billing → Billing preferences → Free Tier usage alerts.

### Enable Free Tier Usage Alerts

```
AWS Console → Billing → Billing preferences
  → Free Tier usage alerts: ON
  → Email: [your email]
```

Sau khi enable, bạn sẽ nhận email khi:
- EC2 usage > 637.5 hours (85% của 750h)
- RDS usage > 637.5 hours (85% của 750h)

---

## 1.7 Mapping với Cloud Practitioner Knowledge

### Well-Architected Framework — Quyết định nào map vào pillar nào?

| Quyết định | Pillar | Lý do |
|------------|--------|-------|
| RDS thay vì PostgreSQL tự cài trên EC2 | **Reliability** | AWS lo backup, failover, patching |
| Database trong isolated subnet | **Security** | Minimize attack surface |
| NAT Gateway cho backend | **Reliability** | Backend cần ra internet để pull packages |
| Free Tier services | **Cost Optimization** | Không tốn tiền khi học |
| 2 AZ cho RDS subnet group | **Reliability** | Chuẩn bị cho Multi-AZ sau này |

### Shared Responsibility Model

| Thành phần | AWS chịu trách nhiệm | Bạn chịu trách nhiệm |
|------------|---------------------|---------------------|
| EC2 | Physical host, hypervisor | OS patching, SG config, app code |
| RDS | Physical host, OS, DB engine patching | DB config, user access, data |
| VPC/Subnet/SG | Network infrastructure | Cấu hình đúng rules |

### CapEx vs OpEx

Nếu deploy on-premises:
- Mua server: ~$2,000-5,000 (CapEx)
- Điện, cooling, maintenance: ~$200/tháng (OpEx)
- Setup time: 2-4 tuần

Trên AWS (workshop này):
- EC2 t2.micro: Free Tier (750h/tháng)
- RDS db.t3.micro: Free Tier (750h/tháng)
- NAT Gateway: ~$1-2 cho 1 ngày workshop
- Setup time: vài giờ

---

## 1.8 Checklist trước khi sang Phase 2

- [ ] Hiểu được 3 component của Conduit và cách chúng giao tiếp
- [ ] Biết tại sao mỗi component đặt ở subnet nào
- [ ] Hiểu CIDR plan: VPC /16, mỗi subnet /24
- [ ] Có thể vẽ lại To-Be diagram từ trí nhớ
- [ ] Hiểu Security Group chain: Internet → Frontend → Backend → Database
- [ ] **Đã tạo estimate trên Pricing Calculator**
- [ ] **Đã setup AWS Budgets ($5 alert)**
- [ ] **Đã enable Free Tier usage alerts**

**Câu hỏi tự kiểm tra:**
1. Tại sao Backend đặt ở private subnet thay vì public subnet?
2. Tại sao RDS cần subnet ở 2 AZ dù chỉ deploy 1 instance?
3. NAT Gateway đặt ở subnet nào? Tại sao?
4. Nếu không có NAT Gateway, Backend có thể làm gì và không thể làm gì?
5. Tại sao phải setup Budgets **trước** khi deploy, không phải sau?
