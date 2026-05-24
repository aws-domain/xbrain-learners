# AWS Shield Advanced - Protected Resources

**Date**: 2026-05-11

## Câu hỏi

**English**: AWS Shield Advanced provides expanded DDoS attack protection for web applications running on which of the following resources? (Select two)

**Tiếng Việt**: AWS Shield Advanced cung cấp DDoS attack protection mở rộng cho web applications chạy trên resources nào? (Chọn 2)

## AWS Shield Overview

### **AWS Shield Standard**
- ✅ **Activated by default** cho tất cả AWS customers
- ✅ **FREE**
- ✅ Protection cho network layer (L3) và transport layer (L4)

### **AWS Shield Advanced**
- ✅ **Paid service** - Subscription required
- ✅ Protection cho L3, L4, **và application layer (L7)**
- ✅ **DRT (DDoS Response Team)** support
- ✅ Advanced real-time metrics và reports
- ✅ Intelligent DDoS attack detection

## Đáp án đúng ✅ (Chọn 2)

### 1. **Amazon Route 53**
- DNS service
- ✅ **Covered by Shield Advanced**

### 2. **AWS Global Accelerator**
- Network layer service
- ✅ **Covered by Shield Advanced**

## AWS Shield Advanced - Full Protected Resources List

1. ✅ **Amazon EC2**
2. ✅ **Elastic Load Balancing (ELB)**
3. ✅ **Amazon CloudFront**
4. ✅ **Amazon Route 53**
5. ✅ **AWS Global Accelerator**

## Các đáp án SAI ❌

### ❌ **Amazon API Gateway**
**Tại sao sai?**
- API Gateway dùng **AWS WAF** để monitor HTTP/HTTPS requests
- **KHÔNG covered** under Shield Advanced

### ❌ **AWS CloudFormation**
**Tại sao sai?**
- Infrastructure as Code service
- Provision resources tự động
- **KHÔNG covered** under Shield Advanced

### ❌ **AWS Elastic Beanstalk**
**Tại sao sai?**
- PaaS service để deploy web apps
- Chỉ covered under **Shield Standard** (default)
- **KHÔNG có** Shield Advanced coverage

## So sánh

| Service | Shield Standard | Shield Advanced |
|---------|----------------|-----------------|
| **EC2** | ✅ | ✅ |
| **ELB** | ✅ | ✅ |
| **CloudFront** | ✅ | ✅ |
| **Route 53** | ✅ | ✅ |
| **Global Accelerator** | ✅ | ✅ |
| **API Gateway** | ✅ | ❌ (use WAF) |
| **Elastic Beanstalk** | ✅ | ❌ |
| **CloudFormation** | ✅ | ❌ |

## Key Point

**Shield Advanced covers 5 services**:
1. EC2
2. ELB
3. CloudFront
4. Route 53 ✅
5. Global Accelerator ✅

**Nhớ**: API Gateway dùng WAF, không phải Shield Advanced
