# AWS Well-Architected Framework - Security Pillar Traceability

**Date**: 2026-05-12

## Câu hỏi

**English**: Which design principle of the AWS Well-Architected Framework can answer the question- "Who did what"?

**Tiếng Việt**: Design principle nào của AWS Well-Architected Framework có thể trả lời câu hỏi "Who did what"?

## Đáp án đúng ✅

**Security**

**Tại sao?**
- ✅ "**Who did what**" = **Traceability** of actions
- ✅ Traceability là part của **Security design principle**
- ✅ Track which user performed what action
- ✅ Audit và accountability

**Keywords trong câu hỏi**:
- "**Who did what**" → Traceability → **Security** ✅

## AWS Well-Architected Framework - 6 Pillars

### 1. **Operational Excellence**

**Focus**: Run và monitor systems để deliver business value

**Design Principles**:
- Perform operations as code
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Anticipate failure
- Learn from operational failures

**KHÔNG answer "Who did what"** ❌

### 2. **Security** ✅

**Focus**: Protect information và systems

**Design Principles**:
- Implement strong identity foundation
- Enable **traceability** ← "Who did what" ✅
- Apply security at all layers
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data
- Prepare for security events

**Enable Traceability**:
- ✅ Log và monitor all actions
- ✅ Track **who** did **what**, **when**, **where**
- ✅ Audit trails
- ✅ Accountability

**AWS Services**:
- **AWS CloudTrail** - Log API calls ("who did what")
- **Amazon CloudWatch** - Monitor và alert
- **AWS Config** - Track resource changes
- **VPC Flow Logs** - Network traffic logs

### 3. **Reliability**

**Focus**: Recover from failures, meet demand

**Design Principles**:
- Automatically recover from failure
- Test recovery procedures
- Scale horizontally
- Stop guessing capacity
- Manage change through automation

**KHÔNG answer "Who did what"** ❌

### 4. **Performance Efficiency**

**Focus**: Use resources efficiently

**Design Principles**:
- Democratize advanced technologies
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy

**KHÔNG answer "Who did what"** ❌

### 5. **Cost Optimization**

**Focus**: Avoid unnecessary costs

**Design Principles**:
- Implement cloud financial management
- Adopt consumption model
- Measure overall efficiency
- Stop spending on undifferentiated heavy lifting
- Analyze and attribute expenditure

**KHÔNG answer "Who did what"** ❌

### 6. **Sustainability**

**Focus**: Minimize environmental impact

**Design Principles**:
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt new hardware/software
- Use managed services
- Reduce downstream impact

**KHÔNG answer "Who did what"** ❌

## "Who Did What" = Traceability

### **Traceability Components**

**Who**: User/role identity
**Did**: Action performed
**What**: Resource affected
**When**: Timestamp
**Where**: Location/IP address
**Why**: Context (optional)

### **AWS Services for Traceability**

1. **AWS CloudTrail** ✅
   - Log all API calls
   - Track user actions
   - "Who did what" audit trail

2. **AWS Config**
   - Track resource configuration changes
   - Who changed what configuration

3. **Amazon CloudWatch Logs**
   - Application logs
   - System logs

4. **VPC Flow Logs**
   - Network traffic logs
   - Who accessed what

## Các đáp án SAI ❌

### ❌ **Reliability**

**Focus**: Recover from failures, availability

**Design Principles**:
- Recover from disruptions
- Dynamically acquire resources
- Keep systems available
- Plan for failure

**Tại sao SAI?**
- Reliability về **availability và recovery**
- **KHÔNG về traceability** của user actions

### ❌ **Operational Excellence**

**Focus**: Run và monitor systems

**Design Principles**:
- Monitor systems
- Proactively take actions
- Deliver business value

**Tại sao SAI?**
- Operational Excellence về **operations và monitoring**
- **KHÔNG về traceability** của user actions

### ❌ **Performance Efficiency**

**Focus**: Use resources efficiently

**Design Principles**:
- Efficient resource usage
- Maintain efficiency as demand changes

**Tại sao SAI?**
- Performance Efficiency về **resource efficiency**
- **KHÔNG về traceability** của user actions

## So sánh Pillars

| Pillar | Focus | Answer "Who did what"? |
|--------|-------|------------------------|
| **Security** | Protect data/systems | ✅ **YES** (Traceability) |
| **Operational Excellence** | Run/monitor systems | ❌ NO |
| **Reliability** | Recover from failures | ❌ NO |
| **Performance Efficiency** | Resource efficiency | ❌ NO |
| **Cost Optimization** | Avoid unnecessary costs | ❌ NO |
| **Sustainability** | Environmental impact | ❌ NO |

## Key Point

**"Who did what" = Traceability = Security pillar** ✅

**Security design principle**: **Enable traceability**
- Log all actions
- Monitor user activities
- Audit trails
- Accountability

## Ví dụ thực tế

### **Scenario**: Security incident investigation

**Question**: "Who deleted the production database?"

**Answer using Security pillar (Traceability)**:
```
1. Check AWS CloudTrail logs
   - API call: DeleteDBInstance
   - User: john.doe@company.com
   - Timestamp: 2026-05-12 10:30:00 UTC
   - IP: 203.0.113.45
   - Region: us-east-1

2. Result: "John Doe deleted production database at 10:30 AM"

→ "Who did what" answered ✅
```

**Without Security pillar (No traceability)**:
```
- No logs
- Cannot determine who deleted database
- No accountability
- Cannot investigate

→ "Who did what" CANNOT be answered ❌
```

## AWS Services for "Who Did What"

### **CloudTrail** (Primary)
```
Event example:
{
  "eventName": "DeleteBucket",
  "userIdentity": {
    "userName": "alice"  ← WHO
  },
  "eventTime": "2026-05-12T10:30:00Z",  ← WHEN
  "requestParameters": {
    "bucketName": "my-bucket"  ← WHAT
  },
  "sourceIPAddress": "203.0.113.45"  ← WHERE
}

→ Complete "Who did what" information ✅
```

### **AWS Config**
```
Configuration change:
- Resource: EC2 instance i-1234567890
- Changed by: bob@company.com  ← WHO
- Change: Security group modified  ← WHAT
- Timestamp: 2026-05-12T11:00:00Z  ← WHEN

→ Track configuration changes ✅
```

## Lưu ý cho bài thi

**Keywords nhận biết Security pillar**:
- "**Who did what**" → Security (Traceability) ✅
- "**Audit trail**" → Security
- "**Track user actions**" → Security
- "**Accountability**" → Security

**KHÔNG nhầm lẫn**:
- Operational Excellence = Run/monitor (NOT traceability)
- Reliability = Availability/recovery (NOT traceability)
- Performance Efficiency = Resource efficiency (NOT traceability)

## Tóm tắt

**"Who did what" = Security pillar** ✅

**Security design principle**: **Enable traceability**
- AWS CloudTrail logs all API calls
- Track user actions
- Audit và accountability
- Answer "Who did what, when, where"

**Other pillars KHÔNG answer "Who did what"**
