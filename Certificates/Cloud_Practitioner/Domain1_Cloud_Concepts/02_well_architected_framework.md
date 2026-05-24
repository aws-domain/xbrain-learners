# Task 1.2 — AWS Well-Architected Framework

> **Exam weight:** Domain 1 = 24% of scored content

## Tổng quan

AWS Well-Architected Framework cung cấp các best practices để thiết kế và vận hành hệ thống trên AWS một cách đáng tin cậy, bảo mật, hiệu quả và tiết kiệm chi phí.

Framework gồm **6 pillars (trụ cột)**:

---

## 6 Pillars

### 1. Operational Excellence (Xuất sắc vận hành)
- Tập trung vào việc **chạy và giám sát hệ thống** để mang lại giá trị business
- Liên tục cải thiện quy trình và thủ tục
- Key practices: IaC, small reversible changes, anticipate failure, learn from failures
- AWS services: AWS CloudFormation, AWS Config, AWS CloudTrail, Amazon CloudWatch

### 2. Security (Bảo mật)
- Bảo vệ thông tin, hệ thống và tài sản
- Key practices: strong identity foundation, enable traceability, apply security at all layers, automate security best practices, protect data in transit and at rest
- AWS services: IAM, AWS Shield, AWS WAF, Amazon GuardDuty, AWS KMS

### 3. Reliability (Độ tin cậy)
- Đảm bảo hệ thống **thực hiện đúng chức năng** và phục hồi nhanh khi có sự cố
- Key practices: test recovery procedures, automatically recover from failure, scale horizontally, stop guessing capacity, manage change in automation
- AWS services: Amazon Route 53, Auto Scaling, Multi-AZ deployments, AWS Backup

### 4. Performance Efficiency (Hiệu quả hiệu suất)
- Sử dụng tài nguyên IT và cloud **hiệu quả nhất**
- Key practices: democratize advanced technologies, go global in minutes, use serverless architectures, experiment more often
- AWS services: Amazon EC2 (right instance types), AWS Lambda, Amazon CloudFront, Amazon ElastiCache

### 5. Cost Optimization (Tối ưu chi phí)
- Tránh chi phí không cần thiết, hiểu và kiểm soát chi tiêu
- Key practices: implement cloud financial management, adopt a consumption model, measure overall efficiency, stop spending money on undifferentiated heavy lifting, analyze and attribute expenditure
- AWS services: AWS Cost Explorer, AWS Budgets, Reserved Instances, Spot Instances, AWS Trusted Advisor

### 6. Sustainability (Bền vững)
- Giảm thiểu tác động môi trường của workloads trên cloud
- Key practices: understand your impact, establish sustainability goals, maximize utilization, use managed services, reduce downstream impact
- AWS services: AWS Customer Carbon Footprint Tool, right-sizing, serverless

---

## So sánh các Pillars

| Pillar | Câu hỏi cốt lõi |
|--------|----------------|
| Operational Excellence | Làm thế nào để vận hành hiệu quả? |
| Security | Làm thế nào để bảo vệ hệ thống? |
| Reliability | Làm thế nào để hệ thống luôn hoạt động? |
| Performance Efficiency | Làm thế nào để dùng tài nguyên hiệu quả? |
| Cost Optimization | Làm thế nào để tránh lãng phí? |
| Sustainability | Làm thế nào để giảm tác động môi trường? |

---

## AWS Well-Architected Tool

- Công cụ miễn phí trong AWS Console
- Giúp review workload theo từng pillar
- Cung cấp recommendations và best practices
- URL: AWS Console → Well-Architected Tool

---

## Exam Tips

- Biết tên và mục đích của **cả 6 pillars**
- Câu hỏi thường hỏi: "Which pillar does X belong to?"
- Security và Reliability hay bị nhầm lẫn — Security = bảo vệ, Reliability = phục hồi
- Sustainability là pillar mới nhất (thêm năm 2021)
