# Task 3.6 — AWS Storage Services

> **Exam weight:** Domain 3 = 34% of scored content

## Amazon S3 (Simple Storage Service)

### Tổng quan
- **Object storage** — lưu trữ files dưới dạng objects
- Unlimited storage, objects up to **5TB**
- **99.999999999% (11 nines)** durability
- Globally unique bucket names
- Truy cập qua HTTP/HTTPS

### S3 Storage Classes

| Storage Class | Use Case | Availability | Cost |
|---|---|---|---|
| **S3 Standard** | Frequently accessed data | 99.99% | Cao nhất |
| **S3 Intelligent-Tiering** | Unknown/changing access patterns | 99.9% | Tự động tối ưu |
| **S3 Standard-IA** | Infrequently accessed, rapid retrieval | 99.9% | Thấp hơn Standard |
| **S3 One Zone-IA** | Infrequent access, single AZ | 99.5% | Thấp hơn Standard-IA |
| **S3 Glacier Instant Retrieval** | Archive, millisecond retrieval | 99.9% | Rất thấp |
| **S3 Glacier Flexible Retrieval** | Archive, minutes to hours retrieval | 99.99% | Rất thấp |
| **S3 Glacier Deep Archive** | Long-term archive, 12h retrieval | 99.99% | Thấp nhất |

### S3 Lifecycle Policies
- Tự động **chuyển objects** giữa storage classes theo thời gian
- Ví dụ: Standard → Standard-IA sau 30 ngày → Glacier sau 90 ngày → Delete sau 365 ngày
- Tiết kiệm chi phí tự động

### S3 Use Cases
- Static website hosting
- Backup và archive
- Data lake
- Media storage và distribution
- Software delivery

---

## Block Storage

### Amazon EBS (Elastic Block Store)
- **Block storage** gắn vào EC2 instances
- Giống như ổ cứng ảo
- **Persist** sau khi EC2 instance bị terminate (nếu cấu hình đúng)
- Chỉ attach vào **một EC2 instance** tại một thời điểm (trừ Multi-Attach)
- Nằm trong **một AZ** cụ thể

**EBS Volume Types:**
| Type | Dùng cho |
|------|---------|
| **gp3/gp2** (General Purpose SSD) | Boot volumes, general workloads |
| **io2/io1** (Provisioned IOPS SSD) | Databases, high I/O |
| **st1** (Throughput Optimized HDD) | Big data, data warehouses |
| **sc1** (Cold HDD) | Infrequently accessed data |

### Instance Store
- **Temporary block storage** gắn trực tiếp vào host
- **Ephemeral** — data mất khi instance stop/terminate
- Rất nhanh (physically attached)
- Dùng cho: cache, temporary data, scratch space

---

## File Storage

### Amazon EFS (Elastic File System)
- **Managed NFS file system** cho Linux
- **Shared access** — nhiều EC2 instances cùng mount
- Tự động scale, không cần provision capacity
- **Multi-AZ** — accessible từ nhiều AZs
- Dùng cho: shared file storage, content management, home directories

### Amazon FSx
- **Managed file systems** cho specific workloads:
  - **FSx for Windows File Server** — SMB protocol, Windows workloads
  - **FSx for Lustre** — High-performance computing, ML, analytics
  - **FSx for NetApp ONTAP** — Enterprise NAS
  - **FSx for OpenZFS** — ZFS-based workloads

---

## Storage Gateway

### AWS Storage Gateway
- **Hybrid storage** — kết nối on-premises với AWS storage
- Cached file systems — frequently accessed data on-premises, rest in S3
- Types:
  - **S3 File Gateway** — NFS/SMB access to S3
  - **Volume Gateway** — iSCSI block storage backed by S3
  - **Tape Gateway** — Virtual tape library backed by S3/Glacier

---

## AWS Backup

- **Centralized backup service** cho nhiều AWS services
- Backup: EC2, EBS, RDS, DynamoDB, EFS, FSx, Storage Gateway
- Tạo backup policies, schedules, retention rules
- Cross-region và cross-account backup

---

## So sánh Storage Types

| | S3 | EBS | EFS | Instance Store |
|---|---|---|---|---|
| **Type** | Object | Block | File | Block |
| **Access** | HTTP/API | Single EC2 | Multiple EC2 | Single EC2 |
| **Persistence** | Permanent | Permanent | Permanent | Ephemeral |
| **Scale** | Unlimited | Up to 64TB | Unlimited | Fixed |
| **Multi-AZ** | Yes | No | Yes | No |

---

## Exam Tips

- S3 = object storage, unlimited, 11 nines durability
- EBS = block storage, single EC2, single AZ
- EFS = file storage, multiple EC2, multi-AZ (Linux only)
- Instance Store = temporary, fastest, lost on stop/terminate
- S3 Glacier = archive, cheapest, slow retrieval
- Lifecycle policies = tự động chuyển storage class để tiết kiệm
- AWS Backup = centralized backup management
