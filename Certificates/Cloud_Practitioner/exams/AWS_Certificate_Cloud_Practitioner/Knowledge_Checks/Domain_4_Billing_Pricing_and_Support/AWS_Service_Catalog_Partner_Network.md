# AWS Services for Solution Building and Consulting

**Date**: 2026-05-11

## Câu hỏi

**English**: An organization is planning to move its infrastructure from the on-premises datacenter to AWS Cloud. As a Cloud Practitioner, which options would you recommend so that the organization can identify the right AWS services to build solutions on AWS Cloud (Select two)?

**Tiếng Việt**: Một organization đang plan move infrastructure từ on-premises datacenter lên AWS Cloud. Bạn recommend options nào để organization có thể identify đúng AWS services để build solutions trên AWS Cloud? (Chọn 2)

## Đáp án đúng ✅ (Chọn 2)

### 1. **AWS Service Catalog**

**Chức năng**: Create và manage **catalogs of approved IT services**

**Đặc điểm**:
- ✅ Catalog các IT services được **approved for use on AWS**
- ✅ Include: VM images, servers, software, databases, multi-tier architectures
- ✅ **Standardize** services cho organization
- ✅ Governance và compliance

**Use case**:
- Organization muốn **standardize** AWS services
- Create catalog các solutions đã approved
- Users chọn từ pre-approved services
- **Identify right services** để build solutions ✅

**Ví dụ**:
- IT team tạo catalog: "Approved Web Application Stack"
- Include: EC2 (t3.medium), RDS (MySQL), ALB, S3
- Developers chọn từ catalog → Deploy standardized solution

### 2. **AWS Partner Network (APN)**

**Chức năng**: Global partner program với **consulting businesses**

**Đặc điểm**:
- ✅ Technology và **consulting partners**
- ✅ Help **identify right AWS services**
- ✅ Build solutions và services cho customers
- ✅ Expert guidance

**Use case**:
- Organization cần **expert help** để identify services
- Partners có experience với AWS solutions
- Consulting để design architecture
- **Identify right services** cho use-case ✅

**Ví dụ**:
- Organization muốn migrate e-commerce platform
- APN partner consult: EC2, RDS, ElastiCache, CloudFront, S3
- Partner help design và implement solution

## Các đáp án SAI ❌

### ❌ **AWS Organizations**

**Chức năng**: **Centrally manage multiple AWS accounts**

**Đặc điểm**:
- Centrally manage billing
- Control access, compliance, security
- Share resources across accounts
- Consolidated billing

**Tại sao SAI?**
- Organizations dùng để **manage accounts**, không phải identify services
- Không help với solution design
- Không provide consulting hoặc service recommendations

**Use case**: Multi-account management, NOT solution building

### ❌ **Amazon CloudWatch**

**Chức năng**: **Monitoring and observability service**

**Đặc điểm**:
- Monitor applications
- Performance metrics
- Logs và events
- Alarms và alerts

**Tại sao SAI?**
- CloudWatch dùng để **monitor resources**, không phải identify services
- Không help với solution design
- Không provide service recommendations

**Use case**: Resource monitoring, NOT solution building

**Nhớ**: "Resource performance monitoring, events, alerts" → CloudWatch

### ❌ **AWS CloudTrail**

**Chức năng**: **Governance, compliance, auditing service**

**Đặc điểm**:
- Log AWS API calls
- Account activity tracking
- Compliance auditing
- Security analysis

**Tại sao SAI?**
- CloudTrail dùng để **audit activity**, không phải identify services
- Không help với solution design
- Không provide service recommendations

**Use case**: Account auditing, NOT solution building

**Nhớ**: "Account-specific activity and audit" → CloudTrail

## So sánh Services

| Service | Purpose | Help Identify Services? |
|---------|---------|------------------------|
| **Service Catalog** | Catalog approved IT services | ✅ **YES** - Standardized solutions |
| **Partner Network (APN)** | Consulting partners | ✅ **YES** - Expert guidance |
| **Organizations** | Multi-account management | ❌ NO - Account management |
| **CloudWatch** | Monitoring | ❌ NO - Performance monitoring |
| **CloudTrail** | Auditing | ❌ NO - Activity logging |

## Key Point

**"Identify right AWS services to build solutions"** → Cần **guidance/consulting**:
- **Service Catalog**: Pre-approved service catalog ✅
- **Partner Network**: Expert consulting ✅

**KHÔNG phải**:
- Organizations: Account management
- CloudWatch: Monitoring
- CloudTrail: Auditing

## Ví dụ thực tế

**Scenario**: Company migrate on-premises to AWS

### ✅ **Đúng - Dùng Service Catalog**
```
IT Team tạo catalog:
├── Web Application Stack
│   ├── EC2 (t3.medium)
│   ├── RDS (MySQL)
│   └── ALB
├── Data Analytics Stack
│   ├── EMR
│   ├── S3
│   └── Redshift
└── Machine Learning Stack
    ├── SageMaker
    └── S3
```
- Developers chọn từ approved stacks
- **Identify right services** cho use-case ✅

### ✅ **Đúng - Dùng APN Partner**
```
Company → APN Consulting Partner
Partner assess requirements:
- E-commerce platform
- High availability needed
- Global users

Partner recommend:
- EC2 Auto Scaling
- RDS Multi-AZ
- CloudFront
- Route 53
- S3
```
- Expert help **identify right services** ✅

### ❌ **Sai - Dùng CloudWatch**
```
Company: "Help us identify services for migration"
CloudWatch: "I monitor resources, not recommend them"
```
- CloudWatch không provide service recommendations ❌

## Lưu ý cho bài thi

**Keywords nhận biết**:
- "**Identify right AWS services**" → Service Catalog / APN
- "**Build solutions**" → Service Catalog / APN
- "**Consulting**" / "**Guidance**" → APN
- "**Approved services**" / "**Catalog**" → Service Catalog

**KHÔNG nhầm lẫn**:
- Organizations = Account management
- CloudWatch = Monitoring
- CloudTrail = Auditing
