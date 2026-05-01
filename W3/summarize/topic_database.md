# Database — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** AWS Database Offerings, Amazon DynamoDB Getting Started, Amazon RDS Service Primer, AWS SimuLearn: Databases in Practice, AWS SimuLearn: First NoSQL Database

---

## 1. Tổng Quan Database Trên AWS

### Relational vs Non-Relational

| | Relational (SQL) | Non-Relational (NoSQL) |
|---|---|---|
| **Cấu trúc** | Tables, rows, columns — schema cố định | Flexible schema (JSON, key-value...) |
| **Query** | SQL | API calls (GetItem, Query, Scan...) |
| **Scale** | Vertical (scale up) | Horizontal (scale out) |
| **Dùng khi** | Complex queries, transactions, joins | High throughput, flexible data, scale lớn |
| **AWS service** | RDS, Aurora | DynamoDB |

---

## 2. Amazon RDS — Relational Database Service

### RDS là gì?
- **Managed relational database** — AWS lo: patching, backup, failover, scaling.
- Hỗ trợ: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora.
- Bạn vẫn quản lý: schema, queries, indexes, application logic.

### RDS Key Features

**Multi-AZ Deployment**
- AWS tự động tạo **standby replica** ở AZ khác.
- Synchronous replication — data luôn đồng bộ.
- Failover tự động khi primary fail (~1–2 phút).
- Dùng cho: **high availability**, không phải read scaling.

**Read Replicas**
- Asynchronous replication từ primary.
- Dùng để **scale read traffic** — app đọc từ replica, ghi vào primary.
- Có thể tạo ở Region khác (cross-region read replica).
- Có thể promote thành standalone database.

**Automated Backups**
- Backup tự động hàng ngày + transaction logs.
- Retention: 1–35 ngày.
- Point-in-time recovery — restore về bất kỳ thời điểm nào trong retention period.

### RDS vs EC2 Database
| | RDS | EC2 + Database |
|---|---|---|
| Patching | AWS lo | Bạn lo |
| Backup | Tự động | Tự setup |
| Failover | Tự động (Multi-AZ) | Tự setup |
| Flexibility | Giới hạn | Full control |
| Dùng khi | Standard workload | Custom config, unsupported engine |

---

## 3. Amazon Aurora

- **AWS-built** relational database — compatible với MySQL và PostgreSQL.
- **5x faster** hơn MySQL, **3x faster** hơn PostgreSQL.
- Storage tự động scale từ 10GB đến 128TB.
- **6 copies** của data trên 3 AZ — highly durable.
- **Aurora Serverless:** Tự động scale compute lên/xuống theo demand — trả theo ACU (Aurora Capacity Units).

---

## 4. Amazon DynamoDB

### DynamoDB là gì?
- **Fully managed NoSQL database** — key-value và document.
- Serverless — không cần provision server, tự động scale.
- Single-digit millisecond latency ở bất kỳ scale nào.
- Dùng cho: gaming, IoT, mobile, real-time apps, session management.

### Core Concepts

**Table, Item, Attribute**
```
Table = tập hợp Items (tương đương table trong SQL)
Item  = 1 record (tương đương row)
Attribute = field của item (tương đương column — nhưng flexible)
```

**Primary Key — Quan trọng nhất**
- **Partition Key (PK):** Xác định partition lưu data. Phải unique nếu dùng đơn.
- **Sort Key (SK):** Kết hợp với PK tạo composite key — cho phép nhiều items cùng PK.
- **Chọn PK tốt:** Cardinality cao, phân phối đều — tránh hot partition.

**Capacity Modes**
| Mode | Dùng khi | Pricing |
|------|---------|---------|
| **On-Demand** | Unpredictable traffic | Trả per request |
| **Provisioned** | Predictable traffic | Trả per RCU/WCU |

**RCU và WCU**
- **RCU (Read Capacity Unit):** 1 strongly consistent read của item ≤4KB/giây
- **WCU (Write Capacity Unit):** 1 write của item ≤1KB/giây

### Query vs Scan
| | Query | Scan |
|---|---|---|
| Dùng PK/SK | ✅ Bắt buộc | ❌ |
| Hiệu quả | ✅ Chỉ đọc data cần | ❌ Đọc toàn bộ table |
| Chi phí | Thấp | Cao (tốn nhiều RCU) |
| **Best practice** | Luôn dùng Query | Tránh Scan trên table lớn |

### Global Secondary Index (GSI)
- Cho phép query theo attribute khác ngoài PK/SK.
- Có partition key và sort key riêng.
- Asynchronous replication từ base table.
- Dùng khi cần query theo nhiều access patterns khác nhau.

### DynamoDB Streams
- Capture mọi thay đổi (insert/update/delete) trong table theo thứ tự.
- Dùng để trigger Lambda, replicate data, audit trail.

### DAX — DynamoDB Accelerator
- **In-memory cache** cho DynamoDB — giảm latency từ ms xuống microseconds.
- Fully managed, compatible với DynamoDB API.
- Dùng khi: read-heavy workload, cần microsecond latency.

---

## 5. Amazon ElastiCache

- **In-memory caching** — Redis hoặc Memcached.
- Giảm load cho database bằng cách cache kết quả query.
- **Redis:** Hỗ trợ data structures phức tạp, persistence, replication, pub/sub.
- **Memcached:** Đơn giản hơn, multi-threaded, không persistence.
- Đặt trong **private subnet** — không expose ra internet.

---

## 6. Chọn Database Đúng

| Nhu cầu | Service |
|---------|---------|
| Relational, complex queries, transactions | RDS (MySQL/PostgreSQL) |
| Relational, high performance, AWS-native | Aurora |
| NoSQL, high throughput, flexible schema | DynamoDB |
| In-memory cache, microsecond latency | ElastiCache / DAX |
| Data warehouse, analytics | Redshift |
| Graph database | Neptune |
| Time series | Timestream |

---

## Quick Reference

**Q: Multi-AZ và Read Replica khác gì nhau?**
A: Multi-AZ dùng cho high availability — standby replica sync, failover tự động khi primary fail. Read Replica dùng cho read scaling — async replication, app đọc từ replica để giảm tải primary. Multi-AZ không serve read traffic.

**Q: DynamoDB Query vs Scan?**
A: Query dùng PK/SK — chỉ đọc data cần, hiệu quả, chi phí thấp. Scan đọc toàn bộ table rồi filter — tốn RCU, chậm trên table lớn. Luôn thiết kế data model để dùng Query thay Scan.

**Q: Khi nào dùng RDS, khi nào dùng DynamoDB?**
A: RDS khi cần SQL, complex joins, transactions (e-commerce, ERP, financial). DynamoDB khi cần scale lớn, latency thấp, schema flexible, serverless (gaming, IoT, session store, real-time).

**Q: GSI trong DynamoDB dùng để làm gì?**
A: Cho phép query theo attribute khác ngoài primary key — giải quyết multiple access patterns. Ví dụ: table có PK=userId, nhưng cần query theo email → tạo GSI với PK=email.
