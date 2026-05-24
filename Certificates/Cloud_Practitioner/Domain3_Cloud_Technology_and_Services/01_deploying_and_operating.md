# Task 3.1 — Methods of Deploying and Operating in AWS

> **Exam weight:** Domain 3 = 34% of scored content (trọng số cao nhất)

## Ways to Access AWS Services

### 1. AWS Management Console
- **Giao diện web** trực quan
- Phù hợp cho: học tập, quản lý thủ công, monitoring
- Truy cập: console.aws.amazon.com

### 2. AWS CLI (Command Line Interface)
- **Programmatic access** qua terminal
- Phù hợp cho: automation scripts, batch operations
- Cài đặt: `pip install awscli` hoặc download installer
- Cần: Access Key ID + Secret Access Key

```bash
aws s3 ls                          # List S3 buckets
aws ec2 describe-instances         # List EC2 instances
aws lambda invoke --function-name MyFunc output.json
```

### 3. AWS SDKs (Software Development Kits)
- Tích hợp AWS vào **application code**
- Hỗ trợ: Python (boto3), JavaScript, Java, Go, .NET, Ruby, PHP...
- Dùng cho: ứng dụng cần tương tác với AWS services

### 4. Infrastructure as Code (IaC)
- Định nghĩa infrastructure bằng **code/templates**
- Reproducible, version-controlled, automated
- AWS tools: **AWS CloudFormation**, **AWS CDK**
- Third-party: Terraform, Pulumi

---

## Infrastructure as Code (IaC)

### AWS CloudFormation
- Dùng **YAML hoặc JSON templates** để định nghĩa AWS resources
- Tạo **Stacks** — tập hợp resources được quản lý cùng nhau
- Rollback tự động nếu deployment thất bại
- Miễn phí (chỉ trả cho resources được tạo)

### AWS CDK (Cloud Development Kit)
- Viết infrastructure bằng **ngôn ngữ lập trình** (Python, TypeScript, Java...)
- Compile thành CloudFormation templates
- Phù hợp cho developers quen với code hơn YAML

### AWS Elastic Beanstalk
- **PaaS** — deploy applications mà không cần quản lý infrastructure
- Upload code → Beanstalk tự lo: EC2, Load Balancer, Auto Scaling, RDS
- Hỗ trợ: Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker

---

## Deployment Models

### Cloud Deployment
- Toàn bộ infrastructure trên AWS
- Tận dụng đầy đủ cloud benefits
- Ví dụ: startup mới hoàn toàn trên AWS

### Hybrid Deployment
- Kết hợp **on-premises + cloud**
- Dùng khi: có legacy systems, compliance requirements, gradual migration
- AWS tools: AWS Direct Connect, AWS VPN, AWS Outposts

### On-Premises Deployment
- Toàn bộ trên data center của tổ chức
- Dùng AWS tools để quản lý (ví dụ: VMware Cloud on AWS)
- Ít phổ biến hơn trong context AWS

---

## One-Time vs Repeatable Operations

| | One-Time | Repeatable |
|---|---|---|
| **Khi nào dùng** | Tác vụ đặc biệt, không lặp lại | Deployment, provisioning thường xuyên |
| **Phương pháp** | Console, manual CLI | IaC, scripts, CI/CD pipelines |
| **Ví dụ** | Tạo account, setup ban đầu | Deploy new version, scale resources |

---

## Exam Tips

- Console = dễ dùng nhưng không scalable
- CLI/SDK = programmatic, phù hợp automation
- IaC (CloudFormation) = best practice cho production
- Elastic Beanstalk = PaaS, developer không cần biết infrastructure
- Hybrid = on-premises + cloud kết hợp
