# AWS Topic Ranking — Thực Tế Đi Làm

Ranking các topic theo mức độ xuất hiện thực tế trong mỗi dự án, từ cao xuống thấp.

---

## 🏆 Ranking

**1. 06_Security_Identity (IAM)**
Không có exception. Mọi resource, mọi service, mọi deploy đều cần IAM Role/Policy. Đây là thứ bạn config đầu tiên và sửa nhiều nhất.

**2. 05_Networking (VPC)**
Mọi hệ thống production đều có VPC, Subnet, SG. Lỗi mạng là loại lỗi phổ biến nhất và mất thời gian debug nhất.

**3. 09_Serverless_IaC (CloudFormation/SAM/Lambda)**
Không ai deploy tay lên production. IaC là bắt buộc. Lambda xuất hiện ở hầu hết mọi kiến trúc hiện đại.

**4. 02_Compute (EC2/ECS/Fargate)**
Ứng dụng phải chạy ở đâu đó. Dù là container hay VM, topic này luôn có mặt.

**5. 03_Storage (S3)**
S3 xuất hiện ở mọi nơi — log, artifact, backup, static file, data lake. Gần như không có project nào không dùng S3.

**6. 04_Database (RDS/DynamoDB)**
Hầu hết ứng dụng cần DB. Nhưng sau khi setup xong thì ít đụng hơn 5 topic trên.

**7. 10_Observability (CloudWatch/X-Ray)**
Khi hệ thống lên production, monitoring là bắt buộc. Nhưng thường setup một lần rồi chỉ xem khi có sự cố.

**8. 08_Data_Engineering (Kinesis/Glue)**
Chỉ xuất hiện nếu project có yêu cầu xử lý data pipeline. Không phải mọi project đều cần.

**9. 11_Cost_Governance**
Quan trọng nhưng thường là việc của Tech Lead/Architect, không phải engineer hàng ngày.

**10. 07_AI_ML (Bedrock)**
Đang nổi nhưng vẫn là use case đặc thù, không phải core infrastructure của mọi project.

---

## 💡 Takeaway

> Top 3 đầu tiên (IAM + Networking + IaC) chiếm khoảng **70% thời gian** của một Cloud/DevOps engineer trong công việc hàng ngày.
