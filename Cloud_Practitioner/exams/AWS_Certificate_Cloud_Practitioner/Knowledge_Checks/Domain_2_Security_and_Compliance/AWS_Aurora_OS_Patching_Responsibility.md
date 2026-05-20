# AWS Aurora - OS Patching Responsibility

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following entities applies patches to the underlying OS for AWS Aurora?

**Tiếng Việt**: Ai chịu trách nhiệm apply patches cho underlying OS của AWS Aurora?

## Đáp án đúng ✅

**The AWS Product Team automatically**

**Tại sao?**
- Amazon Aurora là **fully managed** database service
- Managed by **Amazon RDS**
- AWS tự động handle:
  - Hardware provisioning
  - Database setup
  - **Patching** ← OS patches
  - Backups

**Customer KHÔNG cần** làm gì về OS patching

## Amazon Aurora Overview

**Fully managed relational database**:
- MySQL và PostgreSQL-compatible
- Built for the cloud
- RDS automates administration tasks
- **AWS Product Team** responsible for OS patches

## Các đáp án SAI ❌

### ❌ **AWS customer by using AWS Systems Manager**
**Tại sao sai?**
- Systems Manager chỉ dùng để patch **EC2 instances** hoặc **on-premises instances**
- **KHÔNG thể** patch underlying OS của Aurora
- Aurora là managed service, customer không access OS

### ❌ **AWS Support after receiving request**
**Tại sao sai?**
- AWS Support handle support tickets
- **KHÔNG responsible** for patching Aurora OS
- Patching là automatic, không cần request

### ❌ **AWS customer by SSHing on instances**
**Tại sao sai?**
- Customer **KHÔNG thể SSH** vào Aurora instances
- Aurora là fully managed, không có OS access
- Customer chỉ patch **EC2 instances** của mình

## Shared Responsibility Model

### **AWS Responsibility** (Managed Services)
- ✅ **Aurora** - AWS patches OS
- ✅ **RDS** - AWS patches OS
- ✅ **DynamoDB** - AWS patches OS
- ✅ **Lambda** - AWS patches OS

### **Customer Responsibility**
- ✅ **EC2** - Customer patches OS
- ✅ **On-premises** - Customer patches OS

## So sánh

| Service | OS Patching Responsibility |
|---------|---------------------------|
| **Aurora** | AWS Product Team ✅ |
| **RDS** | AWS Product Team |
| **EC2** | Customer |
| **On-premises** | Customer |

## Key Point

**Managed service = AWS patches OS**  
**Unmanaged service (EC2) = Customer patches OS**

- Aurora/RDS = Fully managed → **AWS patches** ✅
- EC2 = Customer managed → **Customer patches**

**Customer KHÔNG thể SSH** vào Aurora/RDS instances
