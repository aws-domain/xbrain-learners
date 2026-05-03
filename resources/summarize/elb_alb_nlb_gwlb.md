# ELB, ALB, NLB, GWLB — Phân biệt các loại Load Balancer trên AWS

## ELB là gì?

**Elastic Load Balancing (ELB)** là tên của **dịch vụ** load balancing trên AWS. ALB không phải là thứ ngang hàng với ELB — ALB là một loại nằm trong ELB.

```
ELB (dịch vụ)
├── ALB  — Application Load Balancer
├── NLB  — Network Load Balancer
├── GWLB — Gateway Load Balancer
└── CLB  — Classic Load Balancer (legacy, không dùng nữa)
```

---

## So sánh 3 loại chính

| | ALB | NLB | GWLB |
|---|---|---|---|
| Layer | L7 (Application) | L4 (Transport) | L3/L4 |
| Protocol | HTTP, HTTPS, WebSocket | TCP, UDP, TLS | IP |
| Routing dựa trên | Path, host, header, method | IP + Port | — |
| Use case | Web app, microservices, API | Real-time, gaming, IoT | Virtual appliances (firewall, IDS) |
| Latency | ~ms | Cực thấp (~µs) | — |
| Static IP | ❌ (dùng DNS) | ✅ | ✅ |
| Preserve client IP | ❌ (cần X-Forwarded-For) | ✅ | ✅ |

---

## ALB — Application Load Balancer

ALB hiểu **nội dung của request** — đọc được HTTP headers, path, query string rồi mới quyết định route đi đâu.

```
ALB routing rules:
  /api/*         →  Target Group: API servers
  /images/*      →  Target Group: Static servers
  host: admin.*  →  Target Group: Admin servers
```

**Phù hợp cho:**
- Web application, REST API
- Microservices (mỗi service một target group)
- Container workload (ECS, EKS)
- Kết hợp với API Gateway (API Gateway lo auth/throttling, ALB lo load balancing)

---

## NLB — Network Load Balancer

NLB không đọc nội dung request — chỉ nhìn vào **IP và port**, route cực nhanh.

```
NLB routing:
  TCP port 3306  →  RDS cluster
  UDP port 53    →  DNS servers
```

**Phù hợp cho:**
- Database connections (MySQL, PostgreSQL)
- Real-time app cần latency cực thấp
- Cần **static IP** để whitelist ở firewall phía client
- Non-HTTP protocol (MQTT, gRPC, game server)

---

## GWLB — Gateway Load Balancer

Loại ít gặp nhất — dùng để route traffic **qua virtual network appliances** (firewall bên thứ 3, IDS/IPS) trước khi vào hệ thống.

```
Internet → GWLB → Palo Alto Firewall → ALB → App servers
```

**Phù hợp cho:**
- Tích hợp third-party firewall, IDS/IPS vào VPC
- Centralized security inspection cho nhiều VPC

---

## Khi nào chọn loại nào?

```
Web app / API / microservices?      → ALB
Low latency / non-HTTP / static IP? → NLB
Third-party firewall / IDS?         → GWLB
```

> Trong hầu hết các bài học AWS về VPC và web architecture, "load balancer" mặc định ám chỉ **ALB**.
