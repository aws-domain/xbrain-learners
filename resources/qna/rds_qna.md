# RDS & Database Architecture — Q&A

## CLOUD-BASED DATABASES

### Relational Databases

**Managed service nghĩa là gì trong thực tế?**

AWS RDS lo:
- OS patching, DB engine patching
- Backup tự động, point-in-time restore
- Failover (Multi-AZ), replication
- Hardware provisioning, storage scaling

Mày vẫn tự lo:
- Schema design, query optimization
- Index strategy
- Application-level connection handling
- Parameter Group tuning

---

**Khi nào chọn RDS vs tự cài PostgreSQL trên EC2?**

Chọn RDS khi: không muốn quản lý infra, cần HA/backup sẵn, team nhỏ.

Chọn EC2 khi: cần custom OS config, extension không được RDS hỗ trợ, hoặc cần kiểm soát hoàn toàn.

Trade-off: RDS tốn tiền hơn, ít linh hoạt hơn, nhưng giảm operational overhead đáng kể.

---

**db.t3.micro vs db.r6g.large?**

| | db.t3.micro | db.r6g.large |
|---|---|---|
| CPU | Burstable | Dedicated |
| RAM | ~1GB | ~16GB |
| Dùng cho | Dev/test, traffic thấp | Production, memory-intensive |

Chọn dựa trên: workload pattern (burst vs sustained), RAM requirement, và budget.

---

### Non-Relational Databases

**Khi nào không phù hợp với relational DB?**

- Schema thay đổi liên tục
- Cần scale horizontal cực lớn (hàng tỷ records)
- Data dạng key-value đơn giản, cần latency < 1ms
- Time-series data với write throughput cao

Ví dụ: session store, shopping cart, IoT sensor data, social media feed.

---

**DynamoDB hay RDS PostgreSQL cho user profile của app mobile?**

Hỏi lại trước khi quyết định:
1. Profile có structure cố định hay mỗi user có attributes khác nhau?
2. Read/write ratio là bao nhiêu?
3. Có cần query phức tạp (JOIN, filter nhiều field) không?
4. Scale dự kiến — bao nhiêu user?
5. Có cần ACID transaction không?
6. Latency requirement là bao nhiêu?

---

### Database Migration

**Blue/Green Deployment giải quyết gì?**

In-place upgrade: DB đang chạy bị downtime, không rollback được nhanh.

Blue/Green: tạo Green environment mới, test kỹ, rồi mới chuyển traffic. Rollback = chuyển traffic về Blue ngay lập tức.

---

**Traffic chuyển sang Green như thế nào? Rollback?**

- AWS RDS Blue/Green dùng DNS switchover — thay đổi endpoint trong vài giây
- Rollback: switchover ngược lại về Blue, Green vẫn còn nguyên cho đến khi xóa

---

**Graviton instance lợi ích và rủi ro?**

Lợi ích: giá rẻ hơn ~20%, performance tốt hơn cho memory-intensive workload.

Rủi ro: ARM architecture — một số extension hoặc custom binary có thể không tương thích. Cần test kỹ trước khi migrate production.

---

## DATABASE ARCHITECTURES

**Multi-AZ vs Read Replica?**

- **Multi-AZ** → HA, failover tự động. Standby không nhận traffic.
- **Read Replica** → scale đọc. Không tự failover.

---

**Khi primary fail trong Multi-AZ, điều gì xảy ra?**

RDS tự động promote standby lên primary, DNS endpoint được cập nhật. Thời gian: ~60 giây (Multi-AZ Instance), ~35 giây (Multi-AZ Cluster). App không cần đổi connection string.

---

**Parameter Group là gì? Có cần restart không?**

Parameter Group = tập hợp config của DB engine (ví dụ: `max_connections`, `shared_buffers`).

- **Dynamic parameter**: apply ngay, không cần restart.
- **Static parameter**: cần restart instance.

---

**RPO và RTO?**

- **RPO** (Recovery Point Objective): mất tối đa bao nhiêu data? → ảnh hưởng bởi backup frequency.
- **RTO** (Recovery Time Objective): mất tối đa bao lâu để restore? → ảnh hưởng bởi restore strategy.

Backup hàng ngày → RPO tối đa 24h. Multi-AZ → RTO ~60 giây.

---

**Scale compute vs scale storage?**

- **Scale compute** (đổi instance size): gây downtime (restart). Multi-AZ giảm downtime xuống còn vài giây.
- **Scale storage**: không gây downtime, nhưng không thể giảm storage sau khi tăng.

---

### RDS Proxy

**Tại sao Lambda + RDS trực tiếp là vấn đề?**

Lambda scale nhanh → mỗi invocation mở 1 connection mới → DB bị overwhelmed. RDS Proxy giải quyết bằng connection pooling: nhiều Lambda share chung pool, DB chỉ thấy số connection nhỏ hơn nhiều.

---

**Connection pooling hoạt động thế nào?**

Proxy duy trì sẵn N connections đến DB. 1000 Lambda invocations → tất cả đi qua proxy → proxy multiplexes xuống còn vài chục connections thực sự đến DB.

Không có pooling: 1000 Lambda = 1000 connections đồng thời → DB crash hoặc từ chối kết nối.

---

**Khi nào không cần RDS Proxy?**

- App server truyền thống (EC2, ECS) với số connection ổn định, có thể tự manage pool (HikariCP, pgBouncer).
- Workload không có connection spike.

---

## PURPOSE-BUILT DATABASES

**pgvector giải quyết bài toán gì?**

Lưu và query vector embeddings trực tiếp trong PostgreSQL. Dùng cho similarity search trong AI/RAG: tìm document gần nhất với query vector bằng cosine/L2 distance.

---

**Tại sao dùng Pinecone thay vì pgvector?**

Pinecone tốt hơn khi: vector dataset lớn, cần ANN tốc độ cao, không muốn quản lý index trên PostgreSQL.

pgvector tốt hơn khi: dataset vừa, muốn kết hợp vector search với relational query trong cùng 1 DB, giảm chi phí infra.

---

**Table partitioning giúp gì?**

Query chỉ scan partition liên quan thay vì toàn bộ table → nhanh hơn, maintenance dễ hơn (drop partition cũ thay vì DELETE).

Chọn partition key dựa trên: column hay được filter nhất trong WHERE clause (thường là `created_at`, `region`, `status`).

---

**TLE cho phép làm gì?**

Viết PostgreSQL extension bằng ngôn ngữ thông thường (Python, JS, Perl) thay vì C. Dùng khi cần custom function/logic mà built-in extension không có.

---

### Bookstore App Use Case

**IAM Database Authentication vs username/password?**

IAM Auth: token tạm thời (15 phút), không có password cố định trong code, audit qua CloudTrail.

Lợi ích: không có credential bị leak, rotation tự động, centralized access control qua IAM policy.

---

**Secrets Manager giải quyết gì?**

Hardcode credentials: lộ khi code bị leak, rotation thủ công, không audit được.

Secrets Manager: lưu tập trung, rotation tự động, app fetch lúc runtime, audit qua CloudTrail.

---

**Khi nào dùng Glue + Athena thay vì query trực tiếp RDS?**

- Query analytics/reporting nặng trên data lớn → không muốn ảnh hưởng production DB
- Data đã được export ra S3 (data lake)
- Ad-hoc query không cần real-time

---

## SECURITY

**Encryption at rest vs in transit — enable ở đâu?**

- **At rest**: bật lúc tạo RDS instance (KMS key), không thể bật sau khi đã tạo (phải snapshot + restore).
- **In transit**: enforce SSL/TLS qua Parameter Group (`rds.force_ssl=1`).

---

**Least privilege cho EC2 kết nối RDS?**

IAM role của EC2 chỉ có:
- `rds-db:connect` trên đúng DB instance và đúng DB user
- Không có quyền `rds:*` (quản lý infra)

Security Group: EC2 SG được allow vào RDS SG trên port 5432, không mở public.

---

## PERFORMANCE & MONITORING

**CloudWatch metric nào xem đầu tiên khi RDS chậm?**

1. `CPUUtilization`
2. `DatabaseConnections`
3. `ReadLatency` / `WriteLatency`
4. `FreeableMemory`
5. `ReadIOPS` / `WriteIOPS`

---

**VACUUM trong PostgreSQL là gì?**

PostgreSQL dùng MVCC — UPDATE/DELETE không xóa row cũ ngay mà để lại "dead tuples". VACUUM dọn dead tuples, cập nhật statistics cho query planner.

Thiếu VACUUM: table bloat, query planner dùng sai execution plan → query chậm dần. Nghiêm trọng hơn: transaction ID wraparound → DB shutdown.

---

## BIG PICTURE: E-commerce Order Management

**Architecture:**

```
App Servers (ECS)
      │
   RDS Proxy
      │
Multi-AZ DB Cluster (PostgreSQL)
  writer (AZ-1) → reader-1 (AZ-2), reader-2 (AZ-3)
      │
  Read Replica (cross-region, DR)
```

**Từng quyết định:**

| Quyết định | Lý do |
|---|---|
| Multi-AZ DB Cluster | Đơn hàng = critical data, cần HA + failover nhanh (~35s) + scale đọc |
| RDS Proxy | App server scale → tránh connection exhaustion |
| Read Replica cross-region | DR, nếu region chính sập có thể promote |
| Encryption at rest (KMS) | Dữ liệu thanh toán, compliance |
| SSL in transit | Bảo vệ data trên đường truyền |
| IAM Auth + Secrets Manager | Không hardcode credentials |
| Automated backup 7 ngày + PITR | RPO thấp, có thể restore về bất kỳ thời điểm nào |
| Parameter Group tuning | `max_connections`, `shared_buffers` phù hợp với instance size |
| Table partitioning trên `orders` by `created_at` | Orders table lớn theo thời gian, query thường filter theo ngày |
| CloudWatch alarms | Alert khi CPU > 80%, connections > 80% max, latency tăng |
