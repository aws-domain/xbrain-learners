# AWS Hybrid Storage Services

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following is a hybrid storage service that allows on-premises applications to access data on AWS Cloud?

**Tiếng Việt**: Dịch vụ nào là hybrid storage service cho phép on-premises applications truy cập data trên AWS Cloud?

## Đáp án đúng ✅

**AWS Storage Gateway**

**Tại sao?**
- **Hybrid cloud storage service**
- Kết nối on-premises environments với AWS Cloud
- On-premises apps có thể truy cập AWS storage
- Cache data locally cho low-latency access

**3 loại Storage Gateway**:
1. **Tape Gateway** - Backup tapes lên cloud
2. **File Gateway** - File shares backed by S3
3. **Volume Gateway** - Block storage volumes backed by S3

**Use cases**:
- Moving tape backups to cloud
- Cloud-backed file shares
- Low latency access to AWS data
- Migration, archiving, disaster recovery

## Các dịch vụ KHÔNG ĐÚNG ❌

### ❌ **AWS Direct Connect**
**Tại sao sai?**
- **Connectivity service** (kết nối mạng)
- Tạo dedicated private connection từ on-prem đến VPC
- **KHÔNG phải storage service**
- Mất ít nhất 1 tháng để setup

**Use case**: Kết nối mạng private, không qua internet

### ❌ **AWS Snowball**
**Tại sao sai?**
- **Data transport solution** (vận chuyển data vật lý)
- Di chuyển terabytes/petabytes data vào/ra AWS
- Physical device để transport
- **KHÔNG cho phép** on-prem apps truy cập AWS storage real-time

**Use case**: Migrate large data một lần, không phải hybrid access

### ❌ **Amazon EBS**
**Tại sao sai?**
- **Block storage cho EC2 instances**
- Chỉ dùng với EC2 trong AWS
- **KHÔNG thể** attach vào on-premises applications

**Use case**: Storage cho EC2, không phải hybrid

## So sánh

| Service | Type | Use Case |
|---------|------|----------|
| **Storage Gateway** | Hybrid storage | On-prem apps access AWS storage ✅ |
| **Direct Connect** | Network connectivity | Private connection to AWS |
| **Snowball** | Data transport | One-time large data migration |
| **EBS** | Block storage | EC2 instance storage only |

## Key Point

**"Hybrid storage" + "on-premises apps access AWS Cloud"** → **Storage Gateway**

- Storage Gateway = Bridge giữa on-prem và AWS storage ✅
- Direct Connect = Network connection (không phải storage)
- Snowball = Physical transport (không phải real-time access)
- EBS = EC2 only (không phải hybrid)
