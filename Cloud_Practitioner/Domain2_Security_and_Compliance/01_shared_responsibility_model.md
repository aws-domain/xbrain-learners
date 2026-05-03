# Task 2.1 — AWS Shared Responsibility Model

> **Exam weight:** Domain 2 = 30% of scored content (trọng số cao nhất sau Domain 3)

## Tổng quan

AWS Shared Responsibility Model phân chia trách nhiệm bảo mật giữa **AWS** và **khách hàng**:

> **AWS** chịu trách nhiệm bảo mật **OF** the cloud  
> **Khách hàng** chịu trách nhiệm bảo mật **IN** the cloud

---

## AWS Responsibilities — "Security OF the Cloud"

AWS chịu trách nhiệm bảo vệ **cơ sở hạ tầng** chạy tất cả các dịch vụ:

- **Physical security** — Data centers, servers, networking hardware
- **Hardware** — Servers, storage, networking equipment
- **Hypervisor** — Virtualization layer
- **Managed services infrastructure** — Phần cứng và phần mềm nền tảng của các managed services (RDS, DynamoDB, Lambda...)
- **Global infrastructure** — Regions, Availability Zones, Edge Locations

---

## Customer Responsibilities — "Security IN the Cloud"

Khách hàng chịu trách nhiệm về **những gì họ đưa lên cloud**:

- **Data** — Mã hóa, phân loại, quản lý dữ liệu
- **Identity & Access Management** — IAM users, roles, policies
- **Operating System** — Patching, configuration (với EC2)
- **Network configuration** — Security groups, NACLs, VPC settings
- **Application** — Code, dependencies, vulnerabilities
- **Client-side encryption** — Mã hóa dữ liệu trước khi gửi lên AWS

---

## Trách nhiệm thay đổi theo loại dịch vụ

| Loại dịch vụ | AWS chịu trách nhiệm | Khách hàng chịu trách nhiệm |
|---|---|---|
| **IaaS** (EC2) | Hardware, hypervisor, network | OS, middleware, app, data |
| **PaaS** (Elastic Beanstalk, RDS) | Hardware, OS, platform | App, data, access management |
| **SaaS** (Amazon Chime, WorkMail) | Hầu hết mọi thứ | Data, user access |
| **Serverless** (Lambda) | Hardware, OS, runtime | Code, IAM, data |

### Ví dụ cụ thể:

**Amazon EC2:**
- AWS: Physical host, hypervisor, network infrastructure
- Customer: OS patching, security groups, application, data

**Amazon RDS:**
- AWS: Physical host, hypervisor, OS, database engine patching
- Customer: Database settings, user access, data encryption, security groups

**AWS Lambda:**
- AWS: Physical host, OS, runtime environment
- Customer: Function code, IAM permissions, environment variables

---

## Shared Responsibilities

Một số trách nhiệm được **chia sẻ** giữa AWS và khách hàng:

| Trách nhiệm | AWS | Khách hàng |
|---|---|---|
| **Patch management** | Patch infrastructure | Patch guest OS và apps |
| **Configuration management** | Configure infrastructure | Configure OS, DB, apps |
| **Awareness & training** | Train AWS employees | Train customer employees |

---

## Exam Tips

- Câu hỏi phổ biến: "Ai chịu trách nhiệm về X?"
- **OS patching trên EC2** = Customer (không phải AWS)
- **OS patching trên RDS** = AWS (managed service)
- **Data encryption** = luôn là trách nhiệm của Customer
- **Physical security của data center** = luôn là trách nhiệm của AWS
- Khi dịch vụ càng "managed" thì AWS càng chịu nhiều trách nhiệm hơn
