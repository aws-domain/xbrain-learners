# AWS Hardware Security Module (HSM) Services

**Date**: 2026-05-11

## Câu hỏi

**English**: Due to regulatory and compliance reasons, an organization is supposed to use a hardware device for any data encryption operations in the cloud. Which AWS service can be used to meet this compliance requirement?

**Tiếng Việt**: Do regulatory và compliance reasons, một organization phải sử dụng hardware device cho bất kỳ data encryption operations nào trong cloud. AWS service nào có thể đáp ứng compliance requirement này?

## Đáp án đúng ✅

**AWS CloudHSM**

**Tại sao?**
- ✅ **Hardware Security Module (HSM)** - Physical hardware device
- ✅ **FIPS 140-2 Level 3 validated** - Highest security standard
- ✅ Generate và manage **encryption keys** trên hardware
- ✅ Fully-managed service

**Keywords trong câu hỏi**:
- "**Hardware device**" → CloudHSM (physical HSM)
- "**Data encryption operations**" → Encryption keys management
- "**Regulatory and compliance**" → FIPS 140-2 Level 3

## AWS CloudHSM

**Chức năng**: Cloud-based **Hardware Security Module**

**Đặc điểm**:
- ✅ **Physical hardware device** cho encryption
- ✅ **FIPS 140-2 Level 3 validated** HSMs
- ✅ Generate và use encryption keys trên AWS Cloud
- ✅ **Full control** over encryption keys
- ✅ Fully-managed: Hardware provisioning, patching, HA, backups

**Use cases**:
- ✅ **Regulatory compliance** (FIPS 140-2 Level 3 required)
- ✅ Contractual requirements cho hardware-based encryption
- ✅ High-security applications
- ✅ Database encryption (Oracle TDE, SQL Server TDE)
- ✅ SSL/TLS certificate management

**FIPS 140-2 Levels**:
- Level 1: Software-based (lowest security)
- Level 2: Software + tamper-evident
- **Level 3: Hardware-based + tamper-resistant** ← CloudHSM ✅
- Level 4: Highest (physical protection)

## Các đáp án SAI ❌

### ❌ **AWS KMS (Key Management Service)**

**Chức năng**: Managed service để create và manage **cryptographic keys**

**Đặc điểm**:
- Create và manage encryption keys
- Control key usage across AWS services
- **FIPS 140-2 validated** (nhưng **NOT Level 3**)
- **Shared tenancy** - AWS manages hardware

**Tại sao SAI?**
- KMS **KHÔNG phải hardware device** mà customer control
- KMS uses HSMs nhưng **shared** với other customers
- **KHÔNG đáp ứng** requirement "use a hardware device"
- KMS = Software-based key management

**Use case**: General encryption key management, NOT hardware-based compliance

### ❌ **AWS Secrets Manager**

**Chức năng**: Manage **secrets** (passwords, API keys, credentials)

**Đặc điểm**:
- Store và retrieve secrets
- Automatic rotation của credentials
- Database credentials, API keys management
- **NOT a Hardware Security Module**

**Tại sao SAI?**
- Secrets Manager quản lý **secrets**, không phải encryption operations
- **KHÔNG phải HSM**
- Không đáp ứng hardware device requirement

**Use case**: Secret management, NOT encryption hardware

### ❌ **AWS Trusted Advisor**

**Chức năng**: **Best practices recommendations**

**Đặc điểm**:
- Cost optimization recommendations
- Security best practices
- Performance improvement
- Service limits monitoring
- **NOT related to encryption**

**Tại sao SAI?**
- Trusted Advisor là **advisory tool**, không phải encryption service
- Không liên quan đến HSM hoặc encryption operations

**Use case**: AWS best practices guidance, NOT encryption

## So sánh CloudHSM vs KMS

| Feature | CloudHSM | KMS |
|---------|----------|-----|
| **Type** | Hardware Security Module | Managed key service |
| **FIPS 140-2** | **Level 3** ✅ | Level 2 |
| **Hardware Control** | **Dedicated hardware** ✅ | Shared hardware |
| **Tenancy** | **Single-tenant** | Multi-tenant |
| **Key Control** | **Customer managed** | AWS managed |
| **Compliance** | **High (hardware-based)** ✅ | Standard |
| **Use Case** | Regulatory compliance | General encryption |
| **Cost** | Higher (dedicated hardware) | Lower (shared) |

## Key Point

**"Hardware device for encryption"** → **CloudHSM** ✅

**CloudHSM vs KMS**:
- **CloudHSM**: Physical hardware, FIPS 140-2 **Level 3**, dedicated ✅
- **KMS**: Software-based, FIPS 140-2 Level 2, shared

**Regulatory compliance requiring hardware** → **CloudHSM**

## Ví dụ thực tế

**Scenario 1**: Bank cần FIPS 140-2 Level 3 compliance
```
Requirement: Hardware-based encryption
Solution: AWS CloudHSM ✅
- Dedicated HSM hardware
- FIPS 140-2 Level 3 validated
- Full control over keys
```

**Scenario 2**: Startup cần encrypt S3 data
```
Requirement: Simple encryption key management
Solution: AWS KMS ✅
- Managed service
- Cost-effective
- No hardware requirement
```

**Scenario 3**: Company cần store database passwords
```
Requirement: Secret management
Solution: AWS Secrets Manager ✅
- Automatic rotation
- Secure storage
- NOT encryption hardware
```

## Lưu ý cho bài thi

**Keywords nhận biết CloudHSM**:
- "**Hardware device**"
- "**FIPS 140-2 Level 3**"
- "**Regulatory compliance**"
- "**Dedicated HSM**"
- "**Hardware-based encryption**"

→ Đáp án: **AWS CloudHSM** ✅

**KHÔNG nhầm lẫn**:
- KMS = Software-based key management (NOT hardware device)
- Secrets Manager = Secret storage (NOT encryption hardware)
- Trusted Advisor = Best practices tool (NOT encryption)
