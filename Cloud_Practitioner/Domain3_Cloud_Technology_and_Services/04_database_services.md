# Task 3.4 — AWS Database Services

> **Exam weight:** Domain 3 = 34% of scored content

## EC2-Hosted vs AWS Managed Databases

| | EC2-Hosted | AWS Managed (RDS, DynamoDB...) |
|---|---|---|
| **Kiểm soát** | Toàn quyền | Hạn chế |
| **Quản lý** | Bạn tự lo tất cả | AWS lo OS, patching, backups |
| **Effort** | Cao | Thấp |
| **Khi nào dùng** | Cần custom config, unsupported DB | Hầu hết trường hợp |

---

## Relational Databases (SQL)

### Amazon RDS (Relational Database Service)
- **Managed relational database** service
- Hỗ trợ engines: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server
- AWS lo: OS patching, backups, Multi-AZ failover, read replicas
- **Multi-AZ** = high availability (synchronous replication, automatic failover)
- **Read Replicas** = scale read traffic (asynchronous replication)

### Amazon Aurora
- **AWS-built relational database** — compatible với MySQL và PostgreSQL
- **5x faster** than MySQL, **3x faster** than PostgreSQL
- Storage tự động scale từ 10GB đến 128TB
- **Aurora Serverless** — tự động scale capacity theo demand
- **Aurora Global Database** — replicate across Regions với < 1 second latency

---

## NoSQL Databases

### Amazon DynamoDB
- **Fully managed NoSQL** key-value và document database
- **Serverless** — không cần provision servers
- **Single-digit millisecond** performance at any scale
- Tự động scale throughput và storage
- **DynamoDB Streams** — capture changes for event-driven architectures
- **Global Tables** — multi-region, multi-active replication

**Khi nào dùng DynamoDB:**
- Cần scale cực lớn (millions of requests/second)
- Flexible schema
- Key-value hoặc document data model
- Gaming, IoT, mobile, real-time applications

---

## In-Memory Databases (Caching)

### Amazon ElastiCache
- **Managed in-memory caching** service
- Engines: **Redis** và **Memcached**
- Giảm latency bằng cách cache frequently accessed data
- Use cases: session management, leaderboards, real-time analytics

| | Redis | Memcached |
|---|---|---|
| **Data structures** | Strings, lists, sets, hashes... | Strings only |
| **Persistence** | Có | Không |
| **Replication** | Có | Không |
| **Multi-AZ** | Có | Không |

---

## Database Migration Tools

### AWS DMS (Database Migration Service)
- **Migrate databases** vào AWS với downtime tối thiểu
- Hỗ trợ: homogeneous (MySQL → MySQL) và heterogeneous (Oracle → Aurora)
- **Continuous replication** trong quá trình migration
- Source DB vẫn hoạt động trong khi migrate

### AWS SCT (Schema Conversion Tool)
- **Convert database schema** từ engine này sang engine khác
- Ví dụ: Oracle schema → PostgreSQL schema
- Dùng kết hợp với DMS cho heterogeneous migrations

---

## Chọn Database Phù Hợp

| Nhu cầu | Service |
|---------|---------|
| Relational, managed | Amazon RDS |
| Relational, high performance | Amazon Aurora |
| NoSQL, serverless, any scale | Amazon DynamoDB |
| In-memory caching | Amazon ElastiCache |
| Graph database | Amazon Neptune |
| Time-series | Amazon Timestream |
| Ledger | Amazon QLDB |
| Data warehouse | Amazon Redshift |

---

## Exam Tips

- RDS = managed relational DB; bạn không access OS
- Aurora = AWS-native, faster than RDS MySQL/PostgreSQL
- DynamoDB = NoSQL, serverless, millisecond latency
- ElastiCache = caching layer, giảm load cho database
- DMS = migrate database; SCT = convert schema
- Multi-AZ = high availability (không phải performance)
- Read Replicas = scale reads (không phải HA)
