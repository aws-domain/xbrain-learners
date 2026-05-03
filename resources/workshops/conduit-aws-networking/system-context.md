# System Context — Conduit (RealWorld App)

> File này mô tả hệ thống Conduit như một "production system" thực tế.  
> Dùng lại được cho các workshop về: Security, Database, Serverless, CI/CD, Monitoring...

---

## Tổng quan hệ thống

**Tên hệ thống:** Conduit  
**Loại:** Web application — nền tảng blog (Medium.com clone)  
**Người dùng mục tiêu:** Cá nhân muốn viết và đọc bài viết kỹ thuật  
**Quy mô giả định:** Startup nhỏ, ~1,000 DAU (Daily Active Users)

---

## Tính năng chính

| Tính năng | Mô tả | HTTP Method |
|-----------|-------|-------------|
| Đăng ký / Đăng nhập | JWT-based authentication | POST /api/users, POST /api/users/login |
| Xem danh sách bài viết | Global feed + personal feed | GET /api/articles |
| Viết bài viết | CRUD bài viết với tags | POST/PUT/DELETE /api/articles |
| Comment | Thêm/xóa comment | POST/DELETE /api/articles/:slug/comments |
| Like bài viết | Favorite/unfavorite | POST/DELETE /api/articles/:slug/favorite |
| Follow người dùng | Follow/unfollow | POST/DELETE /api/profiles/:username/follow |
| Profile | Xem thông tin người dùng | GET /api/profiles/:username |

---

## Kiến trúc kỹ thuật

### Stack

```
Frontend (React)
    ↓ HTTP/HTTPS
Backend API (Node.js + Express)
    ↓ TCP/5432
Database (PostgreSQL)
```

### Component chi tiết

**Frontend — React**
- Single Page Application (SPA)
- Build ra static files (HTML, CSS, JS)
- Gọi Backend API qua HTTP
- Không có server-side rendering
- Port: 3000 (development), serve qua Nginx (production)

**Backend — Node.js + Express**
- REST API
- JWT authentication (stateless)
- ORM: Sequelize
- Port: 3001
- Endpoints: `/api/*`
- Cần kết nối ra internet để: gửi email (nếu có), gọi third-party API

**Database — PostgreSQL**
- Relational database
- Port: 5432
- Tables chính: users, articles, comments, tags, favorites, follows
- Không cần kết nối ra internet
- Cần backup định kỳ

---

## Traffic Flow

```
User (browser)
    │
    │ HTTPS (port 443) hoặc HTTP (port 80)
    ↓
[Load Balancer / Nginx]
    │
    │ HTTP (port 80)
    ↓
[Frontend — React static files]
    │
    │ API calls: /api/* (port 3001)
    ↓
[Backend — Node.js Express]
    │
    │ PostgreSQL (port 5432)
    ↓
[Database — PostgreSQL]
```

---

## Yêu cầu phi chức năng (Non-functional Requirements)

| Yêu cầu | Mức độ | Ghi chú |
|---------|--------|---------|
| Availability | 99.9% | Không cần 99.99% cho startup |
| Latency | < 500ms | API response time |
| Security | Medium | JWT auth, HTTPS, DB không expose ra internet |
| Scalability | Horizontal | Có thể scale backend khi cần |
| Backup | Daily | Database backup |
| Monitoring | Basic | Logs + basic metrics |

---

## Môi trường

| Môi trường | Mục đích | Ghi chú |
|------------|---------|---------|
| **Development** | Local development | Docker Compose |
| **Staging** | Test trước khi release | Giống production, scale nhỏ hơn |
| **Production** | Live system | Workshop này deploy production-like |

---

## Dependencies bên ngoài

| Dependency | Mục đích | Ghi chú |
|------------|---------|---------|
| npm registry | Install packages | Backend cần ra internet khi deploy |
| GitHub | Source code | Pull code khi setup |
| (Optional) SMTP | Gửi email | Không bắt buộc cho workshop |

---

## Mapping với AWS Services

| Component | AWS Service | Lý do |
|-----------|-------------|-------|
| Frontend static files | EC2 + Nginx | Free Tier, đơn giản |
| Backend API | EC2 | Free Tier, full control |
| Database | RDS PostgreSQL | Managed, automated backup |
| Load Balancing | ALB | Distribute traffic (Phase nâng cao) |
| Static file hosting | S3 + CloudFront | Alternative cho frontend |
| Secrets (DB password) | SSM Parameter Store | Không hardcode credentials |
| Logs | CloudWatch Logs | Centralized logging |
| Backup | S3 | Database backup files |

---

## Tái sử dụng cho các Workshop khác

File này có thể dùng làm context cho:

| Workshop | Phần liên quan |
|----------|---------------|
| **Security** | IAM roles cho EC2, KMS encrypt RDS, WAF cho ALB, Secrets Manager |
| **Database** | RDS Multi-AZ, Read Replica, Aurora migration, DynamoDB cho sessions |
| **Serverless** | Migrate backend sang Lambda + API Gateway |
| **CI/CD** | CodePipeline deploy tự động khi push code |
| **Monitoring** | CloudWatch dashboards, alarms, X-Ray tracing |
| **Cost Optimization** | Right-sizing, Reserved Instances, Spot cho non-critical |
| **High Availability** | Multi-AZ, Auto Scaling Group, ALB health checks |
