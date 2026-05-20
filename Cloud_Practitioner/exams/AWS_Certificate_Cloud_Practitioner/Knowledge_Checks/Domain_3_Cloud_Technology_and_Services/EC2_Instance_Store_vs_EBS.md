# EC2 Storage - Instance Store vs EBS

**Date**: 2026-05-11

## Instance Store

**Ephemeral (temporary) storage** gắn trực tiếp vào physical server

**Đặc điểm**:
- ✅ **Fastest I/O** - Very high IOPS, lowest latency
- ✅ **FREE** - Included với EC2 instance
- ❌ **Data mất** khi instance stop/terminate/fail
- ❌ **Không thể detach** hoặc attach sang instance khác

**Use cases**:
- ✅ Temporary data, cache, buffers
- ✅ High-performance computing (HPC)
- ✅ Big data processing (Hadoop, Spark)
- ✅ **Fault-tolerant workloads** ← App tự xử lý data loss

**KHÔNG dùng cho**:
- ❌ Database (cần persistent)
- ❌ Critical data (cần backup)
- ❌ App không fault-tolerant

## EBS (Elastic Block Store)

**Persistent storage** - Network-attached block storage

**Đặc điểm**:
- ✅ **Data persistent** - Không mất khi instance stop
- ✅ **Có thể detach/attach** sang instance khác
- ✅ **Snapshot/backup** được
- ❌ **Chậm hơn** Instance Store (network latency)
- ❌ **Tốn phí** storage + IOPS

**Use cases**:
- ✅ Database storage
- ✅ Critical data
- ✅ App cần persistent storage

## So sánh

| Feature | Instance Store | EBS |
|---------|----------------|-----|
| **Performance** | Fastest (millions IOPS) | Fast (lower than Instance Store) |
| **Cost** | FREE | Paid (storage + IOPS) |
| **Persistence** | Ephemeral (data mất) | Persistent (data giữ lại) |
| **Use case** | Fault-tolerant, temp data | Database, critical data |

## Key Point cho bài thi

**"Fault-tolerant" + "high-performance" + "cost-effective"** → **Instance Store**

- Fault-tolerant = App tự xử lý data loss → Không cần persistent
- High-performance = Cần I/O nhanh nhất → Instance Store thắng
- Cost-effective = Miễn phí → Instance Store thắng
