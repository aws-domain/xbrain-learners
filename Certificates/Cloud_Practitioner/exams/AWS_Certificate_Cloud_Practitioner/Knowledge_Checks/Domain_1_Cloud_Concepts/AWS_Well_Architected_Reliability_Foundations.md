# AWS Well-Architected Framework - Reliability Pillar Foundations

**Date**: 2026-05-12

## Câu hỏi

**English**: Which of the following AWS services are part of the AWS Foundation services for the Reliability pillar of the Well-Architected Framework in AWS Cloud? (Select two)

**Tiếng Việt**: AWS services nào là part của AWS Foundation services cho Reliability pillar của Well-Architected Framework trong AWS Cloud? (Chọn 2)

## Đáp án đúng ✅ (Chọn 2)

### 1. **AWS Trusted Advisor**

**Chức năng**: Real-time guidance cho AWS best practices

**Đặc điểm**:
- ✅ Cost optimization
- ✅ Security
- ✅ **Fault tolerance** ← Reliability
- ✅ Service limits
- ✅ Performance improvement

**Why Foundation for Reliability?**
- Provides recommendations cho reliability best practices
- Monitor service limits (prevent outages)
- Fault tolerance checks

### 2. **AWS IAM (Identity and Access Management)**

**Chức năng**: Manage access to AWS services securely

**Đặc điểm**:
- ✅ Create và manage users/groups
- ✅ Permissions management
- ✅ **Security best practices** ← Foundation
- ✅ Grant unique security credentials

**Why Foundation for Reliability?**
- Security foundation cho reliable systems
- Control access to resources
- Prevent unauthorized changes

## AWS Well-Architected Framework - Reliability Pillar

### **Foundations (Foundational Requirements)**

**4 Foundation Services**:
1. ✅ **AWS IAM** - Identity and access management
2. ✅ **Amazon VPC** - Network isolation
3. ✅ **AWS Trusted Advisor** - Best practices guidance
4. ✅ **AWS Shield** - DDoS protection

**Tại sao là Foundations?**
- Must be in place **BEFORE** architecting systems
- Influence reliability của entire system
- Foundational requirements cho reliable architecture

## Các đáp án SAI ❌

### ❌ **AWS CloudTrail**

**Chức năng**: **Governance, compliance, auditing**

**Đặc điểm**:
- Log AWS API calls
- Account activity tracking
- Compliance auditing
- Event history

**Tại sao SAI?**
- CloudTrail dùng cho **auditing**, không phải foundation
- **NOT part of Reliability pillar foundations**

**Use case**: Account-specific activity and audit

**Nhớ**: "Account-specific activity and audit" → CloudTrail

### ❌ **AWS CloudFormation**

**Chức năng**: **Infrastructure as Code (IaC)**

**Đặc điểm**:
- Model và provision resources
- Automated infrastructure deployment
- Template-based provisioning

**Tại sao SAI?**
- CloudFormation dùng cho **IaC**, không phải foundation
- **NOT part of Reliability pillar foundations**

**Use case**: Infrastructure as code

**Nhớ**: "Infrastructure as code" → CloudFormation

### ❌ **Amazon CloudWatch**

**Chức năng**: **Monitoring and observability**

**Đặc điểm**:
- Monitor applications
- Performance metrics
- Events và alerts
- Resource monitoring

**Tại sao SAI?**
- CloudWatch dùng cho **monitoring**, không phải foundation
- Excellent cho **Resilient systems** nhưng NOT foundation
- **NOT part of Reliability pillar foundations**

**Use case**: Resource performance monitoring, events, alerts

**Nhớ**: "Resource performance monitoring, events, alerts" → CloudWatch

## AWS Well-Architected Framework - 6 Pillars

### 1. **Operational Excellence**
- Run và monitor systems
- Continuous improvement

### 2. **Security**
- Protect information và systems
- IAM, encryption, detective controls

### 3. **Reliability** ← Câu hỏi này
- **Foundations**: IAM, VPC, Trusted Advisor, Shield ✅
- Recover from failures
- Meet demand
- Mitigate disruptions

### 4. **Performance Efficiency**
- Use resources efficiently
- Maintain efficiency as demand changes

### 5. **Cost Optimization**
- Avoid unnecessary costs
- Optimize spending

### 6. **Sustainability**
- Minimize environmental impact
- Energy efficiency

## Reliability Pillar - Design Principles

1. **Automatically recover from failure**
2. **Test recovery procedures**
3. **Scale horizontally**
4. **Stop guessing capacity**
5. **Manage change through automation**

**Foundations support these principles** ✅

## So sánh Foundation vs Monitoring Services

| Service | Type | Reliability Pillar Role |
|---------|------|------------------------|
| **IAM** | Foundation | ✅ Foundation service |
| **VPC** | Foundation | ✅ Foundation service |
| **Trusted Advisor** | Foundation | ✅ Foundation service |
| **Shield** | Foundation | ✅ Foundation service |
| **CloudWatch** | Monitoring | Resilient systems (NOT foundation) |
| **CloudTrail** | Auditing | Governance (NOT foundation) |
| **CloudFormation** | IaC | Automation (NOT foundation) |

## Key Point

**Reliability Pillar Foundations (4 services)**:
1. **AWS IAM** ✅
2. **Amazon VPC** ✅
3. **AWS Trusted Advisor** ✅
4. **AWS Shield** ✅

**KHÔNG phải Foundations**:
- CloudWatch = Monitoring (resilient systems)
- CloudTrail = Auditing
- CloudFormation = IaC

## Exam Alert - "Think X, think Y"

**Nhớ các patterns**:
- "**Account-specific activity and audit**" → **CloudTrail**
- "**Infrastructure as code**" → **CloudFormation**
- "**Resource performance monitoring, events, alerts**" → **CloudWatch**
- "**Best practices guidance**" → **Trusted Advisor**
- "**Reliability pillar foundations**" → **IAM, VPC, Trusted Advisor, Shield**

## Ví dụ thực tế

**Scenario**: Build reliable application on AWS

### **Step 1: Foundations** (BEFORE architecting)
```
1. AWS IAM ✅
   - Setup users, roles, permissions
   - Security foundation

2. Amazon VPC ✅
   - Network isolation
   - Subnets, security groups

3. AWS Trusted Advisor ✅
   - Check best practices
   - Monitor service limits

4. AWS Shield ✅
   - DDoS protection
   - Security foundation
```

### **Step 2: Build Application**
```
- Use EC2, RDS, S3, etc.
- Implement reliability design principles
```

### **Step 3: Monitor & Audit**
```
- CloudWatch: Monitor performance
- CloudTrail: Audit activities
- CloudFormation: IaC for consistency
```

**Foundations must be in place FIRST** ✅

## Lưu ý cho bài thi

**Keywords nhận biết Reliability Foundations**:
- "**Foundation services**" → IAM, VPC, Trusted Advisor, Shield
- "**Reliability pillar**" → Check foundations
- "**Before architecting**" → Foundations

**4 Foundation Services (nhớ)**:
1. IAM (security)
2. VPC (network)
3. Trusted Advisor (best practices)
4. Shield (DDoS protection)

**KHÔNG nhầm lẫn**:
- CloudWatch = Monitoring (NOT foundation)
- CloudTrail = Auditing (NOT foundation)
- CloudFormation = IaC (NOT foundation)

## Tóm tắt

**Reliability Pillar Foundations**:
- **IAM** + **Trusted Advisor** ✅ (trong câu hỏi)
- VPC + Shield (cũng là foundations)

**Must be in place BEFORE architecting systems**

**CloudWatch, CloudTrail, CloudFormation** = Important nhưng **NOT foundations**
