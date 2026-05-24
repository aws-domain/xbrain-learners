# EBS vs EFS - Availability Zone Characteristics

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following statements are CORRECT regarding the Availability Zone (AZ) specific characteristics of EBS and EFS storage types?

**Tiếng Việt**: Phát biểu nào ĐÚNG về đặc điểm Availability Zone (AZ) của EBS và EFS storage?

## Đáp án đúng ✅

**"EBS volume can be attached to a single instance in the same Availability Zone whereas EFS file system can be mounted on instances across multiple Availability Zones"**

## EBS (Elastic Block Store)

**Block storage cho EC2**

**AZ Characteristics**:
- ✅ **Single AZ only** - EBS volume nằm trong 1 AZ
- ✅ **Attach to single instance** - Chỉ attach được vào 1 EC2 instance
- ✅ **Same AZ requirement** - Instance và EBS phải cùng AZ
- ✅ **Replicated within AZ** - Data replicated trong cùng AZ

**Ví dụ**:
- EBS volume ở `us-east-1a` → Chỉ attach được vào EC2 ở `us-east-1a`
- **KHÔNG thể** attach vào EC2 ở `us-east-1b`

## EFS (Elastic File System)

**Network file system (NFS)**

**AZ Characteristics**:
- ✅ **Multi-AZ** - Data stored across multiple AZs
- ✅ **Mount on multiple instances** - Nhiều EC2 instances cùng mount
- ✅ **Cross-AZ access** - Instances ở các AZ khác nhau đều mount được
- ✅ **Highly available** - Metadata và data across multiple AZs

**Ví dụ**:
- EFS file system → EC2 ở `us-east-1a`, `us-east-1b`, `us-east-1c` đều mount được
- **Shared storage** across AZs

## So sánh

| Feature | EBS | EFS |
|---------|-----|-----|
| **Availability Zone** | Single AZ | Multiple AZs |
| **Attach/Mount** | 1 instance only | Multiple instances |
| **Cross-AZ** | ❌ Same AZ required | ✅ Cross-AZ supported |
| **Storage Type** | Block storage | File storage (NFS) |
| **Use Case** | EC2 boot volume, database | Shared file storage |

## Key Point

**EBS = Single AZ + Single instance**  
**EFS = Multi-AZ + Multiple instances**

- EBS: 1 volume → 1 instance → Same AZ ✅
- EFS: 1 file system → Many instances → Cross-AZ ✅

## Lưu ý

- EBS có thể **snapshot** và restore sang AZ khác, nhưng volume gốc vẫn chỉ ở 1 AZ
- EFS tự động replicate data across multiple AZs để high availability
