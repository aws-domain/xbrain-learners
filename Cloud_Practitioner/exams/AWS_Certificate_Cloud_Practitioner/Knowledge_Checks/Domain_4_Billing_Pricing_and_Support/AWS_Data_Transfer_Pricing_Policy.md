# AWS Data Transfer Pricing Policy

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following statement is correct regarding the AWS pricing policy for data transfer charges?

**Tiếng Việt**: Phát biểu nào ĐÚNG về AWS pricing policy cho data transfer charges?

## Đáp án đúng ✅

**Only outbound data transfer is charged**

**Tại sao?**
- AWS chỉ charge **outbound data transfer** (data ra khỏi AWS)
- **Inbound data transfer** = FREE
- **Data transfer within same region** = FREE

## 3 Fundamental Drivers of AWS Cost

1. **Compute** - EC2, Lambda, etc.
2. **Storage** - S3, EBS, etc.
3. **Outbound Data Transfer** - Data leaving AWS

## AWS Data Transfer Pricing Rules

### ✅ **FREE (Không tính phí)**

1. **Inbound data transfer** (INTO AWS)
   - Internet → AWS = **FREE** ✅
   - Upload data lên AWS = FREE
   - Ví dụ: Upload files lên S3 = FREE

2. **Data transfer within same region**
   - EC2 → S3 (same region) = **FREE** ✅
   - EC2 → RDS (same region) = FREE
   - Lambda → DynamoDB (same region) = FREE
   - **Between AWS services in same region** = FREE

3. **Data transfer between services in same AZ (using private IP)**
   - EC2 → EC2 (same AZ, private IP) = FREE

### 💰 **CHARGED (Tính phí)**

1. **Outbound data transfer** (OUT of AWS)
   - AWS → Internet = **CHARGED** 💰
   - Ví dụ: Users download files từ S3 = CHARGED
   - EC2 → Users = CHARGED

2. **Cross-region data transfer**
   - EC2 (us-east-1) → S3 (us-west-2) = CHARGED
   - Data transfer giữa regions = CHARGED

3. **Cross-AZ data transfer (một số trường hợp)**
   - EC2 (AZ-A) → EC2 (AZ-B) = CHARGED

## Các phát biểu SAI ❌

### ❌ **"Only inbound data transfer is charged"**
**SAI vì**: Inbound data transfer **LUÔN FREE**, không bao giờ charged

### ❌ **"Both inbound and outbound data transfer are charged"**
**SAI vì**: 
- Inbound = **FREE** ✅
- Outbound = **CHARGED** 💰
- Không phải cả 2 đều charged

### ❌ **"Data transfer between AWS services within same region is charged"**
**SAI vì**: Data transfer within same region = **FREE**, không charged

## So sánh Data Transfer Scenarios

| Scenario | Direction | Charged? | Reason |
|----------|-----------|----------|--------|
| Upload to S3 | Internet → AWS | ✅ **FREE** | Inbound |
| Download from S3 | AWS → Internet | 💰 **CHARGED** | Outbound |
| EC2 → S3 (same region) | Within AWS | ✅ **FREE** | Same region |
| EC2 → S3 (cross-region) | Within AWS | 💰 **CHARGED** | Cross-region |
| EC2 → RDS (same region) | Within AWS | ✅ **FREE** | Same region |
| EC2 (AZ-A) → EC2 (AZ-B) | Within region | 💰 **CHARGED** | Cross-AZ |

## Key Point

**AWS Data Transfer Pricing**:
- **Inbound** (INTO AWS) = **FREE** ✅
- **Outbound** (OUT of AWS) = **CHARGED** 💰
- **Within same region** = **FREE** ✅
- **Cross-region** = **CHARGED** 💰

**Chỉ có OUTBOUND data transfer bị charge** ✅

## Ví dụ thực tế

### Scenario 1: Upload backup to S3
```
On-premises → Internet → S3
Direction: Inbound
Cost: $0 (FREE) ✅
```

### Scenario 2: Users download videos from S3
```
S3 → Internet → Users
Direction: Outbound
Cost: ~$0.09/GB (CHARGED) 💰
```

### Scenario 3: EC2 process data and store in S3 (same region)
```
EC2 (us-east-1) → S3 (us-east-1)
Direction: Within same region
Cost: $0 (FREE) ✅
```

### Scenario 4: Replicate S3 to another region
```
S3 (us-east-1) → S3 (eu-west-1)
Direction: Cross-region
Cost: ~$0.02/GB (CHARGED) 💰
```

## Outbound Data Transfer Pricing (Example)

**Pricing tiers** (approximate, varies by region):
- First 10 TB/month: $0.09/GB
- Next 40 TB/month: $0.085/GB
- Next 100 TB/month: $0.07/GB
- Over 150 TB/month: $0.05/GB

**Ví dụ**: 
- 100 GB outbound data transfer = ~$9
- 1 TB outbound data transfer = ~$90

## Lưu ý cho bài thi

**Keywords nhận biết**:
- **"Inbound"** → **FREE** ✅
- **"Outbound"** → **CHARGED** 💰
- **"Same region"** → **FREE** ✅
- **"Cross-region"** → **CHARGED** 💰

**Câu hỏi về data transfer pricing**:
→ Đáp án: **"Only outbound data transfer is charged"** ✅

## Tóm tắt

**3 Fundamental Drivers of AWS Cost**:
1. Compute
2. Storage
3. **Outbound Data Transfer** ← Only this is charged for data transfer

**Data Transfer Rules**:
- IN = FREE ✅
- OUT = CHARGED 💰
- Same region = FREE ✅
- Cross-region = CHARGED 💰
