# AWS Cloud Computing Types - IaaS, PaaS, SaaS

**Date**: 2026-05-12

## Câu hỏi

**English**: Which of the following AWS services comes under the Software as a Service (SaaS) Cloud Computing Type?

**Tiếng Việt**: AWS service nào thuộc Software as a Service (SaaS) Cloud Computing Type?

## Đáp án đúng ✅

**Amazon Rekognition**

**Tại sao?**
- ✅ **Complete product** run và managed by AWS
- ✅ **No infrastructure management** - Chỉ dùng software
- ✅ **No machine learning expertise required** - Ready-to-use
- ✅ Image và video analysis service

**Rekognition = SaaS**: Chỉ cần call API, không cần manage infrastructure hoặc platform

## 3 Types of Cloud Computing

### 1. **IaaS (Infrastructure as a Service)**

**Định nghĩa**: Basic building blocks cho cloud IT

**Đặc điểm**:
- ✅ Access to **networking, compute, storage**
- ✅ **Highest flexibility** và management control
- ✅ Manage OS, runtime, applications
- ❌ Phải manage infrastructure

**AWS Examples**:
- **Amazon EC2** ✅ - Virtual servers
- Amazon VPC - Networking
- Amazon EBS - Block storage
- Amazon S3 - Object storage (có thể coi là IaaS)

**Non-AWS Examples**: GCP Compute Engine, Azure VMs, Rackspace, Digital Ocean, Linode

**Use case**: Full control over infrastructure

### 2. **PaaS (Platform as a Service)**

**Định nghĩa**: Platform để deploy và manage applications

**Đặc điểm**:
- ✅ **No need to manage infrastructure** (hardware, OS)
- ✅ Focus on **deployment và management** của applications
- ✅ No resource procurement, capacity planning, patching
- ❌ Phải manage applications

**AWS Examples**:
- **AWS Elastic Beanstalk** ✅ - Deploy web apps
- AWS Lambda - Serverless compute (có thể coi là PaaS)
- Amazon RDS - Managed database

**Non-AWS Examples**: Heroku, Google App Engine, Windows Azure

**Use case**: Deploy applications without managing infrastructure

### 3. **SaaS (Software as a Service)**

**Định nghĩa**: Complete product run và managed by provider

**Đặc điểm**:
- ✅ **Complete product** - Ready to use
- ✅ **No infrastructure management**
- ✅ **No platform management**
- ✅ Only think about **how to use the software**

**AWS Examples**:
- **Amazon Rekognition** ✅ - Image/video analysis
- Amazon Chime - Video conferencing
- Amazon WorkDocs - Document collaboration
- Amazon WorkMail - Email service

**Non-AWS Examples**: Gmail, Dropbox, Zoom, Salesforce, Office 365

**Use case**: Use software without managing anything

## Amazon Rekognition (SaaS)

**Chức năng**: Image và video analysis service

**Đặc điểm**:
- ✅ Add image/video analysis to applications
- ✅ **No machine learning expertise required**
- ✅ Proven, scalable deep learning technology
- ✅ **Fully managed** - AWS handles everything

**Capabilities**:
- Identify objects, people, text, scenes, activities
- Detect inappropriate content
- Facial analysis và recognition
- Celebrity recognition

**Why SaaS?**
- Chỉ cần **call API** → Get results
- **No infrastructure** to manage
- **No ML models** to train
- **Complete product** ready to use

## Các đáp án SAI ❌

### ❌ **Amazon EC2**

**Type**: **IaaS** (Infrastructure as a Service)

**Tại sao SAI?**
- EC2 provides **virtual servers** (infrastructure)
- Phải manage OS, applications, patching
- **Highest level of control** = IaaS

**Use case**: Infrastructure layer, NOT SaaS

### ❌ **AWS Elastic Beanstalk**

**Type**: **PaaS** (Platform as a Service)

**Tại sao SAI?**
- Beanstalk là **platform** để deploy applications
- Upload code → Beanstalk handles deployment
- Không phải complete software product
- **Platform layer** = PaaS, NOT SaaS

**Use case**: Application deployment platform, NOT SaaS

### ❌ **Elastic Load Balancing (ELB)**

**Type**: **IaaS** (Infrastructure as a Service)

**Tại sao SAI?**
- ELB là **infrastructure component** (load balancer)
- Distribute traffic across targets
- Part of infrastructure layer
- **NOT a complete software product**

**Use case**: Infrastructure component, NOT SaaS

## So sánh IaaS vs PaaS vs SaaS

| Feature | IaaS | PaaS | SaaS |
|---------|------|------|------|
| **Control Level** | Highest | Medium | Lowest |
| **Manage Infrastructure** | ✅ YES | ❌ NO | ❌ NO |
| **Manage Platform** | ✅ YES | ✅ YES | ❌ NO |
| **Manage Application** | ✅ YES | ✅ YES | ❌ NO |
| **Use Software** | ✅ YES | ✅ YES | ✅ YES |
| **AWS Example** | EC2 | Elastic Beanstalk | Rekognition |
| **Flexibility** | Highest | Medium | Lowest |
| **Ease of Use** | Complex | Medium | Easiest |

## Responsibility Model

### **IaaS (EC2)**
```
You manage:
├── Applications
├── Data
├── Runtime
├── Middleware
└── OS

AWS manages:
├── Virtualization
├── Servers
├── Storage
└── Networking
```

### **PaaS (Elastic Beanstalk)**
```
You manage:
├── Applications
└── Data

AWS manages:
├── Runtime
├── Middleware
├── OS
├── Virtualization
├── Servers
├── Storage
└── Networking
```

### **SaaS (Rekognition)**
```
You manage:
└── Use the software (API calls)

AWS manages:
├── Applications
├── Data
├── Runtime
├── Middleware
├── OS
├── Virtualization
├── Servers
├── Storage
└── Networking
```

## Key Point

**SaaS = Complete product, no management needed**

- **Rekognition** = SaaS ✅ (complete ML service)
- **Elastic Beanstalk** = PaaS (deployment platform)
- **EC2** = IaaS (virtual servers)
- **ELB** = IaaS (infrastructure component)

## Ví dụ thực tế

### **IaaS - EC2**
```
Developer:
1. Launch EC2 instance
2. Install OS
3. Install web server
4. Deploy application
5. Configure security
6. Manage updates/patches

→ Full control, high complexity
```

### **PaaS - Elastic Beanstalk**
```
Developer:
1. Upload application code
2. Beanstalk handles deployment

→ Medium control, medium complexity
```

### **SaaS - Rekognition**
```
Developer:
1. Call Rekognition API
2. Get image analysis results

→ No control, easiest to use
```

## Lưu ý cho bài thi

**Nhận biết SaaS**:
- "**Complete product**"
- "**No management needed**"
- "**Ready to use**"
- "**No expertise required**"

**AWS SaaS examples**:
- Rekognition (ML/AI)
- Chime (video conferencing)
- WorkDocs (documents)
- WorkMail (email)

**KHÔNG phải SaaS**:
- EC2 = IaaS
- Elastic Beanstalk = PaaS
- ELB = IaaS
