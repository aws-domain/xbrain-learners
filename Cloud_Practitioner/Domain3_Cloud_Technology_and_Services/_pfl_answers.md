# PFL Answers — Domain 3: Cloud Technology and Services

> Chỉ mở file này sau khi đã tự trả lời xong trong `_pfl_problems.md`

---

## Bài toán 3.1: Chọn compute service phù hợp

| Workload | Service | Lý do |
|---|---|---|
| A — Web app 24/7, cần control OS | **EC2** | Cần full control OS, install custom software. EC2 là IaaS, bạn quản lý từ OS trở lên. |
| B — Function ngắn, event-driven | **Lambda** | Serverless, chỉ chạy khi có event, tính phí theo millisecond. Không cần quản lý server. |
| C — Container, muốn quản lý cluster | **ECS hoặc EKS** | ECS nếu dùng AWS-native, EKS nếu cần Kubernetes. Cả hai cho phép quản lý cluster. |
| D — Container, không muốn quản lý infra | **Fargate** | Serverless containers — chỉ define CPU/memory, AWS lo phần còn lại. |

**Lambda vs EC2 Spot cho Workload B:**
- **Lambda tốt hơn khi:** Function chạy < 15 phút, event-driven, traffic không đều, không cần warm state
- **EC2 Spot tốt hơn khi:** Cần chạy lâu hơn 15 phút, cần nhiều memory/CPU hơn Lambda limit, batch processing lớn

---

## Bài toán 3.2: Chọn storage service phù hợp

| Data | Service | Lý do |
|---|---|---|
| A — Ảnh profile, public URL | **S3** | Object storage, scalable, có thể serve public URL trực tiếp hoặc qua CloudFront. |
| B — Database, ACID transactions | **RDS** | Managed relational database, hỗ trợ ACID transactions. |
| C — Log cũ, compliance 7 năm | **S3 Glacier** | Archive storage, chi phí cực thấp (~$0.004/GB/tháng), phù hợp cho data ít truy cập. |
| D — Shared file system, multi-EC2 | **EFS** | Elastic File System, có thể mount đồng thời từ nhiều EC2 instances. |
| E — OS disk của EC2 | **EBS** | Block storage, attach trực tiếp vào EC2 như ổ cứng. |

**Điểm dễ nhầm:**
- EBS vs EFS: EBS = 1 instance, EFS = nhiều instances đồng thời
- S3 vs S3 Glacier: S3 = truy cập thường xuyên, Glacier = archive ít truy cập

---

## Bài toán 3.3: Chọn database service phù hợp

| Use case | Service | Lý do |
|---|---|---|
| A — E-commerce, SQL, transactions | **RDS** | Relational database, hỗ trợ SQL và ACID transactions. |
| B — Session data, < 1ms, key-value | **ElastiCache** | In-memory cache (Redis/Memcached), latency microseconds. |
| C — Graph data, social network | **Neptune** | Graph database, được thiết kế cho relationship queries. |
| D — Analytics, hàng tỷ rows | **Redshift** | Data warehouse, columnar storage, tối ưu cho analytical queries (OLAP). |

**Lưu ý DynamoDB:**
- Cũng là đáp án tốt cho Use case B nếu câu hỏi không nhấn mạnh "< 1ms" hoặc "caching"
- Trong exam: "NoSQL", "key-value", "flexible schema" → DynamoDB. "caching", "session", "sub-millisecond" → ElastiCache.

---

## Bài toán 3.4: Thiết kế 3-tier web architecture

**Architecture đề xuất:**

```
Users (toàn cầu)
    ↓
CloudFront (CDN) ← S3 (static assets: ảnh, CSS, JS)
    ↓
Route 53 (DNS)
    ↓
Application Load Balancer (ALB)
    ↓
EC2 Auto Scaling Group (nhiều AZs)
    ↓
RDS Multi-AZ (Primary + Standby)
```

| Yêu cầu | Service | Lý do |
|---|---|---|
| Static assets load nhanh toàn cầu | **CloudFront** | CDN với 400+ edge locations, cache content gần user |
| Auto-scale khi flash sale | **EC2 Auto Scaling Group** | Tự động thêm/bớt EC2 instances dựa trên metrics |
| Database không mất data khi AZ down | **RDS Multi-AZ** | Synchronous replication sang standby ở AZ khác, automatic failover |
| Phân phối traffic đều | **ALB** | Layer 7 load balancer, health checks |

---

## Bài toán 3.5: Thiết kế serverless architecture

**Architecture:**

```
Client → API Gateway → Lambda → DynamoDB
```

- **API Gateway:** Managed API endpoint, handle routing, auth, rate limiting. Tính phí per request.
- **Lambda:** Chạy code khi có request, tự scale, tính phí per invocation + duration. Không trả tiền khi idle.
- **DynamoDB:** NoSQL, serverless, tự scale, tính phí per request (on-demand mode).

**Tại sao không dùng RDS:** RDS cần instance chạy 24/7 → tốn tiền ngay cả khi không có request.

**Break scenarios:**
- **Lambda timeout 15 phút:** Lambda có hard limit 15 phút. Nếu cần chạy lâu hơn → dùng Step Functions, ECS, hoặc chia nhỏ task.
- **DynamoDB throttle:** Lambda nhận `ProvisionedThroughputExceededException`. Cần retry với exponential backoff, hoặc chuyển DynamoDB sang on-demand capacity mode.

---

## Bài toán 3.6: Networking — Thiết kế VPC

**VPC Design:**

```
VPC (10.0.0.0/16)
├── Public Subnet — AZ-a: Web Server EC2, NAT Gateway
├── Public Subnet — AZ-b: Web Server EC2
├── Private Subnet — AZ-a: App Server EC2
├── Private Subnet — AZ-b: App Server EC2
└── Private Subnet — AZ-a: RDS (Primary + Standby)
```

**Public vs Private Subnet:**
- **Public:** Có route đến Internet Gateway → instances có thể nhận traffic từ internet
- **Private:** Không có route đến Internet Gateway → không accessible từ internet trực tiếp

**Internet Gateway vs NAT Gateway:**
- **Internet Gateway:** Traffic 2 chiều (internet ↔ VPC). Đặt ở public subnet.
- **NAT Gateway:** Private subnet kết nối ra internet (download updates) nhưng internet không kết nối vào được. Đặt ở public subnet.

**Security Group vs NACL:**

| | Security Group | NACL |
|---|---|---|
| Level | Instance level | Subnet level |
| Stateful/Stateless | **Stateful** (return traffic tự động allowed) | **Stateless** (phải define cả inbound và outbound) |
| Rules | Allow only | Allow và Deny |

**Security Groups cho bài toán này:**
- Web SG: Allow 80/443 from `0.0.0.0/0`
- App SG: Allow traffic from Web SG only
- DB SG: Allow 3306/5432 from App SG only

---

## Bài toán 3.7: Chọn EC2 purchasing option

| Workload | Option | Lý do | Tiết kiệm |
|---|---|---|---|
| Web server 24/7, ổn định | **Reserved Instance (1yr)** | Predictable, chạy liên tục → commit để tiết kiệm | ~40% |
| Batch processing, có thể interrupt | **Spot Instances** | Chịu được interrupt → tiết kiệm tối đa | ~70-90% |
| Dev/test, giờ hành chính | **On-Demand** | Không chạy 24/7, không đủ để commit Reserved | 0% (tắt ~60% thời gian) |
| Spike handling, unpredictable | **On-Demand** | Không biết khi nào cần, không thể commit | 0% |

**Savings Plans vs Reserved Instances:**
- **Reserved Instances:** Commit vào instance type cụ thể. Ít linh hoạt hơn.
- **Savings Plans:** Commit vào mức spend ($/hour), áp dụng cho EC2 + Lambda + Fargate. Linh hoạt hơn khi migrate workload.

---

## Bài toán 3.8: Deploy strategy

| Option | Tên kỹ thuật | AWS Service | Khi nào dùng |
|---|---|---|---|
| A — Tắt rồi deploy | **In-place / Recreate** | CodeDeploy (AllAtOnce) | Dev/test, khi downtime chấp nhận được |
| B — Deploy song song, chuyển traffic dần | **Blue/Green Deployment** | CodeDeploy, Elastic Beanstalk, ECS | Production, cần zero downtime, dễ rollback |
| C — Deploy cho % user trước | **Canary Deployment** | CodeDeploy (Canary), API Gateway | Khi muốn test với real traffic trước, giảm risk |

**Trong exam:** "zero downtime" → Blue/Green. "test với một phần user" → Canary. "đơn giản, có thể downtime" → In-place.

---

## Exam-style Questions — Đáp án

**Câu 1:** Batch job có thể bị interrupt — purchasing option nào tiết kiệm nhất?

**Spot Instances** — tiết kiệm tới 70-90% so với On-Demand. AWS có thể terminate với 2 phút notice, nhưng batch jobs thường có thể checkpoint và resume.

---

**Câu 2:** Dịch vụ nào phân phối static content toàn cầu với độ trễ thấp nhất?

**Amazon CloudFront** — CDN với 400+ edge locations. Cache content tại edge location gần user nhất.

---

**Câu 3:** Shared file system cho nhiều EC2 instances mount đồng thời?

**Amazon EFS (Elastic File System)** — NFS-based, mount đồng thời từ hàng nghìn EC2 instances, tự động scale.

Không phải EBS — EBS chỉ attach được vào 1 instance tại một thời điểm.

---

**Câu 4:** Sự khác biệt chính giữa Security Group và Network ACL?

| | Security Group | Network ACL |
|---|---|---|
| **Stateful/Stateless** | **Stateful** — return traffic tự động được phép | **Stateless** — phải define cả inbound và outbound |
| **Level** | Instance level | Subnet level |
| **Rules** | Allow only | Allow và Deny |

Điểm quan trọng nhất: **Security Group là stateful, NACL là stateless.**

---

**Câu 5:** Chạy container mà không cần quản lý EC2 instances?

**AWS Fargate** — serverless compute engine cho containers. Chỉ define CPU và memory, AWS lo phần còn lại.

---

**Câu 6:** Chạy code không cần provision server, chỉ tính phí khi đang chạy?

**AWS Lambda** — serverless compute, tính phí theo số lần invocation và duration (millisecond). Không tính phí khi idle.
