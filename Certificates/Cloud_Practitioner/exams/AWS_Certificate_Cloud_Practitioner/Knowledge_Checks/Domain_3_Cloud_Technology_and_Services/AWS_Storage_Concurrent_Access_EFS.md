# AWS Storage Services - Concurrent Access and File Operations

**Date**: 2026-05-11

## Câu hỏi

**English**: A data analytics company is running a proprietary batch analytics application on AWS and wants to use a storage service which would be accessed by hundreds of EC2 instances simultaneously to append data to existing files. As a Cloud Practitioner, which AWS service would you suggest for this use-case?

**Tiếng Việt**: Một data analytics company đang chạy batch analytics application trên AWS và muốn dùng storage service mà có thể được truy cập bởi hàng trăm EC2 instances đồng thời để append data vào existing files. Bạn suggest AWS service nào?

## Đáp án đúng ✅

**EFS (Elastic File System)**

**Tại sao?**

- ✅ **Concurrent access** - Hàng nghìn EC2 instances có thể access đồng thời
- ✅ **File system interface** - Hỗ trợ file operations (read, write, **append**)
- ✅ **Shared storage** - Multiple instances mount cùng 1 file system
- ✅ **NFS protocol** - Network File System

**Keywords trong câu hỏi**:

- "Hundreds of EC2 instances **simultaneously**" → Concurrent access
- "**Append data to existing files**" → File operations

## 4 AWS Storage Services

### 1. **EFS (Elastic File System)** ✅

**Type**: **File Storage** (NFS)

**Đặc điểm**:

- ✅ **Concurrent access** - Up to thousands of EC2 instances
- ✅ **Shared file system** - Multiple instances mount cùng lúc
- ✅ **File operations** - Read, write, **append**, modify
- ✅ **POSIX-compliant** - Standard file system semantics
- ✅ **Multi-AZ** - Data replicated across AZs
- ✅ **Elastic** - Auto scale storage capacity

**Use cases**:

- ✅ **Shared storage** cho multiple EC2 instances
- ✅ **Big data analytics** - Multiple workers access same data
- ✅ Content management systems
- ✅ Web serving
- ✅ Home directories

**Ví dụ**:

- 100 EC2 instances chạy analytics
- Tất cả mount cùng EFS file system
- Đồng thời append results vào shared log file
- **EFS handle concurrent writes** ✅

### 2. **EBS (Elastic Block Store)** ❌

**Type**: **Block Storage**

**Đặc điểm**:

- ❌ **Single instance only** - 1 EBS volume attach vào 1 EC2 instance
- ❌ **KHÔNG concurrent access** - Không thể attach vào nhiều instances đồng thời
- ✅ High performance
- ✅ Persistent storage
- ✅ Snapshots

**Tại sao KHÔNG phù hợp?**

- Câu hỏi cần "hundreds of EC2 instances simultaneously"
- EBS chỉ attach vào 1 instance → **KHÔNG đáp ứng**

**Use cases**:

- Boot volumes cho EC2
- Database storage (single instance)
- Application storage (single instance)

**Lưu ý**: EBS Multi-Attach (io1/io2) cho phép attach vào **max 16 instances** trong same AZ, nhưng vẫn không đủ cho "hundreds of instances"

### 3. **Instance Store** ❌

**Type**: **Ephemeral Block Storage**

**Đặc điểm**:

- ❌ **Single instance only** - Gắn vào 1 EC2 instance
- ❌ **KHÔNG concurrent access**
- ❌ **Ephemeral** - Data mất khi instance stop/terminate
- ✅ Very high performance (local disk)
- ✅ FREE (included với instance)

**Tại sao KHÔNG phù hợp?**

- Chỉ 1 instance access được
- Data không persistent
- Không thể share giữa instances

**Use cases**:

- Temporary cache
- Scratch data
- High-performance computing (single instance)

### 4. **S3 (Simple Storage Service)** ❌

**Type**: **Object Storage**

**Đặc điểm**:

- ✅ **Concurrent access** - Unlimited concurrent requests
- ❌ **KHÔNG hỗ trợ file append** - Object storage, không phải file system
- ❌ **KHÔNG có file system interface** - REST API only
- ✅ Highly scalable
- ✅ Durable (11 9's)

**Tại sao KHÔNG phù hợp?**

- S3 là **object storage**, không phải file storage
- **KHÔNG hỗ trợ append operations** - Phải upload lại toàn bộ object
- Không có POSIX file system semantics

**S3 operations**:

- PUT (upload/overwrite entire object)
- GET (download object)
- DELETE (delete object)
- **KHÔNG có APPEND** ❌

**Use cases**:

- Backup and archive
- Static website hosting
- Data lakes
- Media storage

## So sánh 4 Storage Services

| Feature               | EFS                | EBS                     | Instance Store | S3                    |
| --------------------- | ------------------ | ----------------------- | -------------- | --------------------- |
| **Type**              | File Storage       | Block Storage           | Block Storage  | Object Storage        |
| **Concurrent Access** | ✅ Thousands        | ❌ 1 instance            | ❌ 1 instance   | ✅ Unlimited           |
| **File Append**       | ✅ YES              | ✅ YES                   | ✅ YES          | ❌ **NO**              |
| **Shared Storage**    | ✅ YES              | ❌ NO                    | ❌ NO           | ✅ YES (but no append) |
| **Protocol**          | NFS                | Block device            | Block device   | REST API              |
| **Use Case**          | Shared file system | Single instance storage | Temp storage   | Object storage        |

## Key Point cho câu hỏi

**Requirements**:

1. ✅ **Concurrent access** by hundreds of EC2 instances
2. ✅ **Append data** to existing files

**Analysis**:

- EBS, Instance Store: ❌ Không concurrent access
- S3: ❌ Không hỗ trợ append operations
- **EFS**: ✅ Concurrent access + File append ✅

**Đáp án**: **EFS** ✅

## Ví dụ thực tế

**Scenario**: Batch analytics với 200 EC2 instances

### ❌ **Sai - Dùng EBS**

```text
EC2-1 → EBS Volume A (isolated)
EC2-2 → EBS Volume B (isolated)
EC2-3 → EBS Volume C (isolated)
...
```

- Mỗi instance có EBS riêng
- **KHÔNG share data** được
- Phải merge results sau → Phức tạp

### ✅ **Đúng - Dùng EFS**

```text
EC2-1 ↘
EC2-2 → EFS File System (shared)
EC2-3 ↗
...
EC2-200 ↗
```

- Tất cả instances mount cùng EFS
- **Concurrent append** vào shared files
- Real-time data sharing ✅

### ❌ **Sai - Dùng S3**

```text
EC2-1 → Download file → Process → Upload entire file
EC2-2 → Download file → Process → Upload entire file (overwrite)
```

- **KHÔNG thể append** - Phải upload lại toàn bộ
- Concurrent writes → Overwrite conflicts
- Không efficient

## Lưu ý cho bài thi

**Keywords nhận biết EFS**:

- "**Concurrent access**" / "**Simultaneously**"
- "**Multiple EC2 instances**"
- "**Shared file system**"
- "**Append to files**" / "**File operations**"
- "**NFS**"

→ Đáp án: **EFS** ✅
