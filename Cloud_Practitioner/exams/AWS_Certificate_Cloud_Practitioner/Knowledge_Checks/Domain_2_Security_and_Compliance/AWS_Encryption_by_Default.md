# AWS Services - Encryption by Default

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following AWS services has encryption enabled by default?

**Tiếng Việt**: AWS service nào có encryption enabled by default?

## Đáp án đúng ✅

**CloudTrail Logs**

**Tại sao?**

- CloudTrail logs được save vào S3 bucket
- **By default**, log files được encrypt bằng **SSE-S3** (Server-Side Encryption with S3-managed keys)
- **Không cần** user enable, tự động encrypt

**CloudTrail Overview**:

- Service cho governance, compliance, auditing
- Record AWS API calls và activities
- Save logs vào S3 bucket
- **Encryption by default** ✅

## Các đáp án SAI ❌

### ❌ **EFS (Elastic File System)**

**Tại sao sai?**

- Hỗ trợ encryption (at rest và in transit)
- Nhưng là **optional feature**
- **User phải enable** manually
- **NOT enabled by default**

### ❌ **EBS (Elastic Block Storage)**

**Tại sao sai?**

- Hỗ trợ encryption (at rest và in transit)
- Nhưng là **optional feature**
- **User phải enable** manually
- **NOT enabled by default**

### ❌ **Amazon S3**

**Tại sao sai?**

- Hỗ trợ default encryption cho bucket
- Nhưng là **additional feature**
- **User phải enable** manually
- **NOT enabled by default**

## So sánh Encryption

| Service             | Encryption Support      | Enabled by Default?      |
| ------------------- | ----------------------- | ------------------------ |
| **CloudTrail Logs** | ✅ SSE-S3                | ✅ **YES**                |
| **EFS**             | ✅ At rest + in transit  | ❌ Optional (user enable) |
| **EBS**             | ✅ At rest + in transit  | ❌ Optional (user enable) |
| **S3**              | ✅ SSE-S3, SSE-KMS, etc. | ❌ Optional (user enable) |

## Other Services with Encryption by Default

- **AWS Secrets Manager** - Encrypted by default
- **AWS Systems Manager Parameter Store (SecureString)** - Encrypted by default
- **Amazon Macie** - Findings encrypted by default
- **AWS CloudTrail Logs** ✅

## Key Point

**CloudTrail Logs = ONLY service trong list có encryption by default**

- CloudTrail → **Automatic encryption** (SSE-S3) ✅
- EFS, EBS, S3 → **Optional**, user phải enable

**Lưu ý**: Nhiều AWS services hỗ trợ encryption, nhưng **ít services enable by default**
