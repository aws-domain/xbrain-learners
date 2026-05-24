# Workshop: Deploy Conduit (RealWorld App) lên AWS — Networking Focus

> **Level:** Intermediate → Advanced  
> **Trọng tâm:** AWS Networking (VPC, Subnet, SG, NACL, Route Table, NAT Gateway, VPC Endpoint)  
> **Thời gian ước tính:** 6–8 giờ  
> **AWS Account:** Free Tier compatible  
> **Tool:** AWS Console + AWS CLI

---

## Giới thiệu hệ thống — Conduit (RealWorld App)

**Conduit** là một Medium.com clone — nền tảng blog đầy đủ tính năng:
- Đăng ký / đăng nhập (JWT auth)
- Viết, sửa, xóa bài viết
- Comment, like bài viết
- Follow người dùng khác
- Feed cá nhân hóa

**Tại sao chọn Conduit?**
- Đủ phức tạp để tạo ngữ cảnh thực tế (frontend + backend + database)
- Đơn giản đủ để deploy trong 1 ngày
- Có thể tái sử dụng cho các workshop khác (Security, Database, Serverless, CI/CD...)
- Cộng đồng lớn, tài liệu rõ ràng

**Stack kỹ thuật:**
- **Frontend:** React (static files)
- **Backend:** Node.js + Express.js (REST API)
- **Database:** PostgreSQL

**Repo:**
- Backend: https://github.com/TonyMckes/conduit-realworld-example-app
- Frontend: https://github.com/gothinkster/react-redux-realworld-example-app

---

## Cấu trúc Workshop — Real Project Flow

```
Phase 1 — Phân tích, Thiết kế & Cost Estimate   (~2 giờ)
  ├── Đọc hiểu hệ thống
  ├── Quyết định AWS service + lý do
  ├── Vẽ As-Is và To-Be diagram
  ├── AWS Pricing Calculator — estimate trước khi deploy
  └── AWS Budgets + Free Tier alerts — setup ngay

Phase 2 — Networking Foundation                  (~2 giờ)
  └── VPC, Subnets, IGW, NAT GW, SG, Route Tables, Flow Logs

Phase 3 — Deploy từng layer + Monitoring         (~3 giờ)
  ├── Deploy RDS → Backend EC2 → Frontend EC2
  ├── CloudWatch Agent + Alarms + Dashboard
  └── CloudWatch Logs (Nginx, App, VPC Flow Logs)

Phase 4 — Lỗi có chủ đích & Debug               (~1.5 giờ)
  └── 8 lỗi Networking, tăng dần Intermediate → Advanced

Phase 5 — Alternatives, Review & Cleanup         (~1 giờ)
  ├── NAT Instance, SSM Session Manager, Elastic IP
  ├── Trusted Advisor — security review sau deploy
  ├── Cost Explorer — so sánh estimate vs thực tế
  └── Cleanup script
```

---

## Files trong Workshop

| File | Nội dung |
|------|----------|
| `phase1-analysis.md` | Phân tích hệ thống, chọn AWS service, vẽ diagram |
| `phase2-networking.md` | Tạo VPC, subnet, SG, route table từ đầu |
| `phase3-deploy.md` | Deploy RDS, EC2 backend, EC2 frontend |
| `phase4-troubleshooting.md` | 8 lỗi Networking có chủ đích + debug guide |
| `phase5-alternatives.md` | Workarounds và trade-off analysis |
| `system-context.md` | File ngữ cảnh hệ thống — dùng lại cho các workshop sau |
| `diagrams/` | Architecture diagrams (as-is và to-be) |

---

## Prerequisites

Trước khi bắt đầu, cần có:
- [ ] AWS account (Free Tier)
- [ ] AWS CLI đã cài và configured (`aws configure`)
- [ ] Git đã cài
- [ ] Node.js 18+ đã cài (để chạy local test)
- [ ] Đã đọc qua các file summarize về Networking

**Verify AWS CLI:**
```bash
aws sts get-caller-identity
```

---

## Kiến thức sẽ được thực hành

### Networking (trọng tâm)
- ✅ VPC design từ đầu (không dùng default VPC)
- ✅ Public / Private / Isolated subnet
- ✅ Internet Gateway + NAT Gateway
- ✅ Route Table configuration
- ✅ Security Group chain (ALB → EC2 → RDS)
- ✅ Network ACL (stateless firewall)
- ✅ VPC Endpoint (S3 Gateway)
- ✅ Elastic IP
- ✅ Bastion Host pattern
- ✅ VPC Flow Logs + CloudWatch Logs Insights

### Observability & Operations
- ✅ CloudWatch Agent (memory, disk metrics)
- ✅ CloudWatch Alarms (CPU, RDS connections, NAT data)
- ✅ CloudWatch Dashboard
- ✅ CloudWatch Logs (Nginx, App logs tập trung)
- ✅ VPC Flow Logs queries (debug networking)

### Cost Management
- ✅ AWS Pricing Calculator (estimate trước deploy)
- ✅ AWS Budgets (alert khi vượt ngưỡng)
- ✅ Free Tier usage alerts
- ✅ Cost Explorer (so sánh estimate vs thực tế)
- ✅ Trusted Advisor (security + service limits review)

### Cloud Practitioner Mapping
- ✅ Well-Architected Framework (Reliability, Security, Cost)
- ✅ Shared Responsibility Model
- ✅ CapEx vs OpEx
- ✅ Free Tier awareness
- ✅ Pricing: On-Demand vs Reserved

---

## Lưu ý Free Tier

Các service dùng trong workshop và giới hạn Free Tier:

| Service | Free Tier | Lưu ý |
|---------|-----------|-------|
| EC2 t2.micro | 750 giờ/tháng | Dùng 2 instance = 375 giờ mỗi cái |
| RDS db.t3.micro | 750 giờ/tháng | Chỉ 1 instance |
| NAT Gateway | **KHÔNG có Free Tier** | ~$0.045/giờ — xóa ngay sau workshop |
| VPC, Subnet, SG | Miễn phí | Không tính phí |
| S3 | 5GB miễn phí | Dùng ít |
| EIP | Miễn phí khi gắn vào running instance | Xóa khi không dùng |

> ⚠️ **NAT Gateway là thứ duy nhất tốn tiền đáng kể.** Ước tính ~$1-2 nếu làm workshop trong 1 ngày. Nhớ xóa sau khi xong.
