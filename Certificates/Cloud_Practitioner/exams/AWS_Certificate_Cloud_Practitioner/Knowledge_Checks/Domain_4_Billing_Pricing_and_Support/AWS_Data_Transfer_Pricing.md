# AWS Data Transfer Pricing

**Date**: 2026-05-11

## Câu hỏi

**English**: The DevOps team at an IT company is moving 500 GB of data from an EC2 instance to an S3 bucket in the same region. Which of the following scenario captures the correct charges for this data transfer?

**Tiếng Việt**: DevOps team đang move 500 GB data từ EC2 instance sang S3 bucket trong cùng region. Scenario nào mô tả đúng charges cho data transfer này?

## Đáp án đúng ✅

**The company would NOT be charged for this data transfer**

**Tại sao?**
- EC2 và S3 trong **same region**
- Data transfer **within same region** = **FREE** (không tính phí)
- Không tính phí inbound, không tính phí outbound

## 3 Fundamental Drivers of AWS Cost

1. **Compute** - EC2, Lambda, etc.
2. **Storage** - S3, EBS, etc.
3. **Outbound Data Transfer** - Data ra khỏi AWS

## AWS Data Transfer Pricing Rules

### ✅ **FREE (Không tính phí)**

1. **Inbound data transfer** (vào AWS)
   - Internet → AWS = FREE
   - Ví dụ: Upload file lên S3 = FREE

2. **Data transfer within same region**
   - EC2 → S3 (same region) = **FREE** ✅
   - EC2 → RDS (same region) = FREE
   - S3 → Lambda (same region) = FREE
   - **Between AWS services in same region** = FREE

3. **Data transfer between AZs (một số trường hợp)**
   - Một số services miễn phí cross-AZ

### 💰 **CHARGED (Tính phí)**

1. **Outbound data transfer** (ra khỏi AWS)
   - AWS → Internet = **CHARGED**
   - Ví dụ: User download file từ S3 = CHARGED

2. **Cross-region data transfer**
   - EC2 (us-east-1) → S3 (us-west-2) = **CHARGED**
   - Data transfer giữa các regions khác nhau = CHARGED

3. **Cross-AZ data transfer (một số trường hợp)**
   - EC2 (AZ-A) → EC2 (AZ-B) = CHARGED (trong cùng region)

## Phân tích câu hỏi

**Scenario**: EC2 → S3, **same region**, 500 GB

**Kiểm tra**:
- ✅ Same region? **YES**
- ✅ Between AWS services? **YES**
- → **FREE** (không tính phí)

**Kết luận**: **$0** charge

## Các đáp án SAI ❌

### ❌ **"Charged for outbound data transfer from EC2"**
**SAI vì**: Same region transfer = FREE, không tính outbound

### ❌ **"Charged for inbound data transfer into S3"**
**SAI vì**: Inbound transfer luôn FREE

### ❌ **"Charged for both outbound and inbound"**
**SAI vì**: Same region transfer = FREE

## So sánh Scenarios

| Scenario | Region | Charge? | Reason |
|----------|--------|---------|--------|
| EC2 → S3 (same region) | us-east-1 → us-east-1 | ✅ **FREE** | Same region |
| EC2 → S3 (cross-region) | us-east-1 → us-west-2 | 💰 **CHARGED** | Cross-region |
| Internet → S3 (upload) | Internet → us-east-1 | ✅ **FREE** | Inbound |
| S3 → Internet (download) | us-east-1 → Internet | 💰 **CHARGED** | Outbound |
| EC2 → RDS (same region) | us-east-1 → us-east-1 | ✅ **FREE** | Same region |
| EC2 (AZ-A) → EC2 (AZ-B) | Same region, diff AZ | 💰 **CHARGED** | Cross-AZ |

## Key Point

**Same Region Transfer = FREE**
- EC2 → S3 (same region) = **$0** ✅
- EC2 → RDS (same region) = **$0**
- Lambda → DynamoDB (same region) = **$0**

**Cross-Region Transfer = CHARGED**
- EC2 (us-east-1) → S3 (us-west-2) = **$$$**

**Outbound to Internet = CHARGED**
- S3 → Internet = **$$$**

**Inbound = ALWAYS FREE**
- Internet → AWS = **$0**

## Ví dụ thực tế

**Scenario 1**: Backup EC2 data to S3 (same region)
- 1 TB data transfer
- Same region: us-east-1
- **Cost**: $0 ✅

**Scenario 2**: Replicate S3 to another region
- 1 TB data transfer
- us-east-1 → eu-west-1
- **Cost**: ~$20 (cross-region transfer) 💰

**Scenario 3**: Users download files from S3
- 1 TB download
- S3 → Internet
- **Cost**: ~$90 (outbound to internet) 💰

## Lưu ý cho bài thi

**Keywords quan trọng**:
- **"Same region"** → **FREE** ✅
- **"Cross-region"** → **CHARGED** 💰
- **"Outbound to internet"** → **CHARGED** 💰
- **"Inbound"** → **FREE** ✅

**Câu hỏi có "same region"** → Đáp án: **NOT charged / FREE**
