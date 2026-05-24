# AWS Acceptable Use Policy

**Date**: 2026-05-11

## Câu hỏi

**English**: Which policy describes prohibited uses of the web services offered by Amazon Web Services?

**Tiếng Việt**: Policy nào mô tả prohibited uses (cách sử dụng bị cấm) của web services do Amazon Web Services cung cấp?

## Đáp án đúng ✅

**AWS Acceptable Use Policy (AUP)**

**Tại sao?**
- ✅ Describes **prohibited uses** của AWS services
- ✅ Official policy tại https://aws.amazon.com/aup/
- ✅ Updated by AWS khi cần thiết
- ✅ Applies to AWS services và AWS website

## AWS Acceptable Use Policy (AUP)

**Chức năng**: Mô tả **prohibited uses** của AWS services

**Nội dung chính**:

### ❌ **Prohibited Activities**

1. **Illegal Activities**
   - Illegal content
   - Child sexual abuse material
   - Violate laws or regulations

2. **Security Violations**
   - Unauthorized access
   - Network attacks (DDoS, port scanning)
   - Malware distribution
   - Phishing

3. **Abusive Behavior**
   - Spam emails
   - Harassment
   - Fraudulent activities

4. **Intellectual Property Violations**
   - Copyright infringement
   - Trademark violations
   - Piracy

5. **Other Prohibited Uses**
   - Cryptocurrency mining (without permission)
   - High-risk activities without proper controls

**URL**: https://aws.amazon.com/aup/

**Enforcement**:
- AWS có quyền suspend/terminate accounts vi phạm
- Report violations đến AWS Abuse Team

## Các đáp án SAI ❌

### ❌ **AWS Trusted Advisor**

**Chức năng**: **Best practices recommendations** tool

**Đặc điểm**:
- Cost optimization
- Security recommendations
- Fault tolerance
- Performance improvement
- Service limits monitoring

**Tại sao SAI?**
- Trusted Advisor là **advisory tool**, không phải policy
- **KHÔNG mô tả** prohibited uses
- Chỉ provide recommendations

**Use case**: AWS best practices guidance, NOT policy enforcement

### ❌ **AWS Fair Use Policy**

**Tại sao SAI?**
- **Made-up option** (không tồn tại)
- Distractor

### ❌ **AWS Applicable Use Policy**

**Tại sao SAI?**
- **Made-up option** (không tồn tại)
- Distractor
- Tên gần giống "Acceptable Use Policy" để gây nhầm lẫn

## AWS Policies Overview

| Policy | Purpose |
|--------|---------|
| **Acceptable Use Policy (AUP)** | Prohibited uses của AWS services ✅ |
| **Customer Agreement** | Terms of service |
| **Service Level Agreement (SLA)** | Service availability guarantees |
| **Privacy Policy** | Data privacy và protection |
| **Data Processing Addendum (DPA)** | GDPR compliance |

## Key Point

**"Prohibited uses of AWS services"** → **AWS Acceptable Use Policy** ✅

**Nhớ tên chính xác**: **"Acceptable"** Use Policy (NOT "Applicable" or "Fair")

## Ví dụ Prohibited Uses

### ❌ **Scenario 1**: Spam emails
```
Company dùng SES để gửi spam emails
→ Vi phạm Acceptable Use Policy
→ AWS có thể suspend account
```

### ❌ **Scenario 2**: DDoS attacks
```
EC2 instances thực hiện DDoS attacks
→ Vi phạm Acceptable Use Policy
→ Report to AWS Abuse Team
```

### ❌ **Scenario 3**: Illegal content
```
S3 bucket host illegal content
→ Vi phạm Acceptable Use Policy
→ AWS terminate resources
```

### ✅ **Scenario 4**: Legitimate use
```
Company dùng EC2 cho web application
→ Tuân thủ Acceptable Use Policy
→ No issues
```

## Liên quan: AWS Abuse Team

**Khi phát hiện vi phạm AUP**:
- Report to **AWS Abuse Team**
- Email: abuse@amazonaws.com
- AWS investigate và take action

**Violations include**:
- Spam
- Port scanning
- DDoS attacks
- Intrusion attempts
- Malware distribution
- Prohibited content

## Lưu ý cho bài thi

**Keywords nhận biết**:
- "**Prohibited uses**" → Acceptable Use Policy ✅
- "**Acceptable Use Policy**" → Official policy
- "**Fair Use Policy**" → Made-up (distractor) ❌
- "**Applicable Use Policy**" → Made-up (distractor) ❌

**Tên chính xác**: **AWS Acceptable Use Policy (AUP)**

**URL**: https://aws.amazon.com/aup/

## Tóm tắt

**AWS Acceptable Use Policy**:
- Describes **prohibited uses** của AWS services
- Official policy document
- Enforced by AWS
- Violations → Account suspension/termination

**KHÔNG nhầm lẫn**:
- Trusted Advisor = Best practices tool (NOT policy)
- Fair Use Policy = Made-up (không tồn tại)
- Applicable Use Policy = Made-up (không tồn tại)
