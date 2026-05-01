# Compute & Storage — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** AWS Compute Services Overview, Getting Started with AWS Storage, Amazon S3 Essentials, Amazon EBS Primer, AWS SimuLearn: Computing Solutions

---

## 1. EC2 — Elastic Compute Cloud

### EC2 là gì?
- Virtual machine (server ảo) chạy trên AWS infrastructure.
- Bạn chọn: OS, CPU, RAM, storage, network — full control.

### Instance Types
| Family | Tối ưu cho | Ví dụ |
|--------|-----------|-------|
| **General Purpose** | Balanced CPU/RAM | t3, m6i |
| **Compute Optimized** | CPU-intensive (batch, HPC) | c6i |
| **Memory Optimized** | RAM-intensive (database, cache) | r6i, x2i |
| **Storage Optimized** | High I/O (data warehouse) | i3, d3 |
| **Accelerated Computing** | GPU (ML, video) | p4, g5 |

### EC2 Pricing
| Hình thức | Tiết kiệm | Dùng khi |
|-----------|-----------|----------|
| **On-Demand** | 0% | Dev/test, unpredictable |
| **Reserved (1–3 năm)** | 30–72% | Production steady-state |
| **Savings Plans** | 30–66% | Flexible commitment |
| **Spot** | 60–90% | Batch, fault-tolerant |
| **Dedicated Host** | — | Compliance, licensing |

### Auto Scaling
- Tự động thêm/bớt EC2 instances dựa trên demand.
- **Scale out:** Thêm instance khi tải tăng
- **Scale in:** Bớt instance khi tải giảm
- Kết hợp với **Load Balancer** để phân phối traffic

---

## 2. Elastic Load Balancing (ELB)

| Loại | Dùng cho | Layer |
|------|---------|-------|
| **Application Load Balancer (ALB)** | HTTP/HTTPS, path-based routing | Layer 7 |
| **Network Load Balancer (NLB)** | TCP/UDP, ultra-low latency | Layer 4 |
| **Gateway Load Balancer (GWLB)** | Third-party appliances (firewall) | Layer 3 |

---

## 3. Amazon S3 — Simple Storage Service

### S3 là gì?
- **Object storage** — lưu trữ file dưới dạng objects trong buckets.
- Không phải file system — không có folder thật sự (chỉ là prefix trong key name).
- Durability: **99.999999999% (11 nines)** — data được replicate tự động.

### S3 Storage Classes
| Class | Dùng cho | Chi phí |
|-------|---------|---------|
| **S3 Standard** | Frequently accessed data | Cao nhất |
| **S3 Intelligent-Tiering** | Unknown access pattern | Tự động chuyển tier |
| **S3 Standard-IA** | Infrequently accessed, cần nhanh | Thấp hơn Standard |
| **S3 One Zone-IA** | IA, chấp nhận mất 1 AZ | Thấp hơn Standard-IA |
| **S3 Glacier Instant** | Archive, cần trong ms | Rất thấp |
| **S3 Glacier Flexible** | Archive, chấp nhận 1–12h | Rất thấp |
| **S3 Glacier Deep Archive** | Long-term archive, 12–48h | Thấp nhất |

### S3 Key Concepts
- **Bucket:** Container chứa objects — tên phải globally unique.
- **Object:** File + metadata. Key = đường dẫn đầy đủ (ví dụ: `images/2024/photo.jpg`).
- **Versioning:** Giữ nhiều version của cùng 1 object — bảo vệ khỏi accidental delete.
- **Lifecycle Policy:** Tự động chuyển objects sang storage class rẻ hơn hoặc xóa sau X ngày.
- **Presigned URL:** URL tạm thời cho phép access object mà không cần AWS credentials.

### S3 Security
- **Block Public Access:** Bật mặc định — ngăn bucket bị public accidental.
- **Bucket Policy:** JSON policy gắn vào bucket — control ai được access.
- **ACL:** Legacy, ít dùng — dùng Bucket Policy thay thế.
- **Encryption:** SSE-S3 (AWS managed), SSE-KMS (KMS key), SSE-C (customer key).

### S3 Use Cases
- Static website hosting
- Data lake / analytics
- Backup và archive
- Media storage (images, videos)
- Lambda deployment packages

---

## 4. Amazon EBS — Elastic Block Store

### EBS là gì?
- **Block storage** gắn vào EC2 instance — như ổ cứng của server.
- Persist độc lập với EC2 — xóa EC2 không mất data EBS (nếu không chọn delete on termination).
- Chỉ gắn vào **1 EC2 trong cùng AZ** (trừ io1/io2 Multi-Attach).

### EBS Volume Types
| Type | Dùng cho | IOPS | Throughput |
|------|---------|------|-----------|
| **gp3** (General Purpose SSD) | Boot volumes, general workload | 3,000–16,000 | 125–1,000 MB/s |
| **gp2** (General Purpose SSD) | Legacy, gp3 tốt hơn | 100–16,000 | — |
| **io2 Block Express** | Mission-critical DB, high IOPS | 256,000 | 4,000 MB/s |
| **io1** | High-performance DB | 64,000 | 1,000 MB/s |
| **st1** (Throughput HDD) | Big data, log processing | 500 | 500 MB/s |
| **sc1** (Cold HDD) | Infrequently accessed | 250 | 250 MB/s |

> **Hay bị hỏi:** gp3 vs io2 — gp3 cho general workload, io2 cho database cần IOPS cao và consistent latency.

### EBS Snapshots
- Backup EBS volume vào S3 (incremental).
- Dùng để: tạo volume mới, copy sang AZ/Region khác, tạo AMI.

---

## 5. Amazon EFS — Elastic File System

- **Shared file system** — nhiều EC2 instances mount cùng lúc (khác EBS chỉ 1 instance).
- Tự động scale — không cần provision size trước.
- Dùng cho: shared content, home directories, CMS.
- Chỉ dùng với **Linux** (NFS protocol).

---

## 6. So Sánh Storage Types

| | S3 | EBS | EFS |
|---|---|---|---|
| Type | Object | Block | File |
| Access | HTTP/HTTPS | Gắn vào EC2 | Mount NFS |
| Multi-instance | ✅ | ❌ (trừ io2 Multi-Attach) | ✅ |
| Use case | Files, backup, static web | OS, database | Shared filesystem |
| Pricing | Per GB stored | Per GB provisioned | Per GB used |

---

## Quick Reference

**Q: S3 và EBS khác gì nhau?**
A: S3 là object storage — lưu file qua HTTP, nhiều service access được, dùng cho backup/media/data lake. EBS là block storage — gắn vào EC2 như ổ cứng, chỉ 1 EC2 dùng được (cùng AZ), dùng cho OS và database.

**Q: gp3 vs io2 — khi nào dùng cái nào?**
A: gp3 cho general workload (boot volume, web server, dev). io2 cho database production cần IOPS cao (>16,000) và consistent low latency — như Oracle, SQL Server, SAP HANA.

**Q: S3 Versioning dùng để làm gì?**
A: Giữ nhiều version của cùng 1 object — bảo vệ khỏi accidental delete hoặc overwrite. Khi xóa object có versioning, AWS thêm "delete marker" thay vì xóa thật — có thể restore lại.

**Q: EBS Snapshot là gì?**
A: Backup incremental của EBS volume, lưu vào S3. Dùng để tạo volume mới, copy sang AZ/Region khác, hoặc tạo AMI từ instance đang chạy.
