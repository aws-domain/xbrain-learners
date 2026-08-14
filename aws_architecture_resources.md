# Nguồn AWS Architecture Projects để Học và Thực Hành

Danh sách các nguồn chính thức từ AWS lưu trữ project kèm architecture diagram, giúp học hỏi và thực hành lại.

---

## 1. AWS Architecture Center

- **URL:** https://aws.amazon.com/architecture/
- **Nội dung:** Reference architectures cho từng use case (web app, data lake, ML pipeline, v.v.), Well-Architected Labs, architecture diagrams kèm giải thích chi tiết.
- **Phù hợp khi:** Muốn xem kiến trúc tổng quan cho một bài toán cụ thể.

## 2. AWS Solutions Library

- **URL:** https://aws.amazon.com/solutions/
- **Nội dung:** Các solution xây dựng sẵn với CloudFormation/CDK templates deploy được ngay, architecture diagram, implementation guide chi tiết, source code trên GitHub.
- **Phù hợp khi:** Muốn deploy ngay một giải pháp hoàn chỉnh và đọc code thực tế.

## 3. AWS Samples (GitHub)

- **URL:** https://github.com/aws-samples
- **Nội dung:** Hàng nghìn project mẫu với code thực tế, nhiều repo có architecture diagram trong README.
- **Phù hợp khi:** Muốn đọc source code chi tiết và fork về chỉnh sửa.

## 4. Serverless Land

- **URL:** https://serverlessland.com/patterns
- **Nội dung:** Chuyên về serverless patterns — mỗi pattern có diagram, SAM/CDK template, và giải thích cách hoạt động.
- **Phù hợp khi:** Học serverless, event-driven architecture, Lambda patterns.

## 5. AWS Workshop Studio

- **URL:** https://workshops.aws/
- **Nội dung:** Các workshop hands-on có hướng dẫn từng bước, architecture diagram, deploy thật trên account.
- **Phù hợp khi:** Muốn học theo kiểu step-by-step có hướng dẫn đầy đủ.

## 6. AWS Well-Architected Labs

- **URL:** https://wellarchitectedlabs.com/
- **Nội dung:** Labs thực hành theo 6 pillars của Well-Architected Framework (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability).
- **Phù hợp khi:** Muốn hiểu sâu best practices và áp dụng vào thiết kế hệ thống.

---

## Cách Sử Dụng Hiệu Quả (Problem-First)

1. **Chọn 1 project/solution** phù hợp domain đang học
2. **Đọc architecture diagram** → tự vẽ lại bằng draw.io để hiểu flow
3. **Deploy theo hướng dẫn** → ghi notes vào `workshop/` folder
4. **Break it** → troubleshoot → ghi lessons learned vào troubleshooting file
5. **Tear down** resources để tránh phát sinh chi phí

---

## Mapping Với Các Domain Trong Repo

| Domain | Nguồn ưu tiên |
|--------|---------------|
| Serverless & IaC | Serverless Land, AWS Solutions Library |
| Networking | AWS Architecture Center, Workshop Studio |
| Database | AWS Solutions Library, AWS Samples |
| Security & Identity | Well-Architected Labs (Security pillar) |
| AI/ML | AWS Samples, Workshop Studio |
| Observability & Operations | Well-Architected Labs (Operational Excellence) |
| Cost Governance | Well-Architected Labs (Cost Optimization) |
