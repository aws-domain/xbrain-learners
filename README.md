# Cloud Learning Dashboard — XBrain AWS DevOps/CloudOps

Chào mừng bạn đến với **Không gian học tập và lưu trữ kiến thức Cloud** của chương trình *XBrain AWS DevOps/CloudOps Foundation Program*.

Repository này đã được tái cấu trúc hoàn toàn theo phương pháp **Topic/Domain kỹ thuật** chuẩn *best-practice*, giúp tăng cường hiệu quả tự học, tra cứu lâu dài và thực hành lập trình/trắc nghiệm trực quan.

---

## 🚀 ĐẶC BIỆT: Trải nghiệm Cloud Learning Portal (HTML)
Bạn có thể mở trực tiếp giao diện Dashboard tương tác bằng web cực kỳ đẹp mắt và trực quan để làm trắc nghiệm luyện thi, mở nhanh chatbot AI và tra cứu lộ trình:

👉 **Nhấp đúp chuột để mở file [index.html](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/index.html) trên trình duyệt của bạn!**

---

## 📂 Sơ đồ Cấu trúc Thư mục Mới

```text
.
├── index.html (Cloud Learning Portal - Dashboard tương tác siêu đẹp)
├── README.md (File chỉ dẫn này)
│
├── curriculum/ (Thư mục hành chính, lộ trình và tracking)
│   ├── course_tracking.md (File theo dõi các khóa học đã hoàn thành)
│   ├── pending_courses.md (Danh sách các khóa học sắp tới)
│   ├── syllabus_foundation_phase1.csv (Syllabus gốc của chương trình)
│   ├── mappings/ (Lịch trình học của từng tuần W1 - W6)
│   └── weeks/ (Tài liệu học tập chính thức theo từng tuần do ban tổ chức cung cấp)
│       ├── W2/ (Chứa learner_guide.en.md, project_announcement.en.md)
│       ├── W3/ (Chứa guides và QnA Prep W3_qna_ontap.vi.md)
│       └── ...
│
├── 01_Cloud_Foundations/
│   ├── Cloud_Practitioner/ (Tài liệu ôn thi chứng chỉ AWS Cloud Practitioner)
│   └── notes/ (problem_first_learning.md...)
│
├── 02_Compute/ (Ghi chú về EC2, ECS, EKS...)
├── 03_Storage/ (Ghi chú về S3, EBS, EFS...)
│
├── 04_Database/
│   ├── notes/ (dynamodb.md, rds_qna.md, neptune, elasticache...)
│   └── diagrams/ (rds-for-postgresSQL/)
│
├── 05_Networking/
│   ├── notes/ (vpc_with_multiple_subnets.md, api_gateway_vs_alb.md...)
│   ├── diagrams/ (Sơ đồ mạng)
│   ├── practice/ (Các workshop: conduit-aws-networking, networking-ws)
│   └── quizzes/ (Các bài thi trắc nghiệm HTML: basics_quiz, gateways_quiz...)
│
├── 06_Security_Identity/
│   └── notes/ (sensitive_data_detection_with_macie.md...)
│
├── 07_AI_ML/
│   ├── notes/ (Ghi chú Amazon Bedrock, RAG, Knowledge Base...)
│   ├── practice/ (Các lab L1-L5 của Bedrock, chat_ui.html, test_friend_api.py)
│   ├── mentoring/ (Các bài session học trực tuyến bằng HTML)
│   └── quizzes/ (bedrock_ai_quiz.html trắc nghiệm)
│
├── 08_Data_Engineering/
│   ├── notes/ (amazon_connect_data_streaming.md...)
│   └── practice/ (data_package/...)
│
├── 09_Serverless_IaC/
│   ├── notes/ (lambda_overview.md, event_driven_architecture.md, sam_vs_cfn.md...)
│   ├── diagrams/ (serverless-patterns/)
│   └── practice/ (serverless-workshop/, workshop-progress.md)
│
├── 10_Observability_Operations/ (Tài liệu sẽ học ở Tuần 6)
└── 11_Cost_Governance/ (Tài liệu tối ưu chi phí học ở Tuần 6)
```

---

## 🎯 Chi tiết các Topics học tập chính

| Thư mục | Chủ đề kỹ thuật | Nội dung nổi bật |
|---------|-----------------|------------------|
| [01_Cloud_Foundations](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/01_Cloud_Foundations) | Nền tảng Cloud & Ôn thi | Tài liệu ôn thi AWS CCP (Domain 1-4), phương pháp học Problem-First |
| [02_Compute](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/02_Compute) | Tính toán đám mây | So sánh EC2 vs ECS vs Fargate, Compute Services Overview |
| [03_Storage](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/03_Storage) | Lưu trữ dữ liệu | S3 storage classes, EBS volume types (gp3/io2), EFS Primer |
| [04_Database](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/04_Database) | Cơ sở dữ liệu | RDS Postgres & QnA, DynamoDB modeling, Neptune & Redis |
| [05_Networking](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/05_Networking) | Kiến trúc Mạng | VPC, Subnet, Route Table, Peering, Transit Gateway, Direct Connect |
| [06_Security_Identity](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/06_Security_Identity) | Bảo mật & Định danh | IAM least privilege, KMS key, WAF, sensitive data detection với Macie |
| [07_AI_ML](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/07_AI_ML) | Trí tuệ nhân tạo | Amazon Bedrock, RAG, Knowledge Base, lab L1-L5, chatbot UI tương tác |
| [08_Data_Engineering](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/08_Data_Engineering) | Kỹ thuật Dữ liệu | Kinesis Data Streams, Glue ETL, Athena, EMR, Connect Data streaming |
| [09_Serverless_IaC](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/09_Serverless_IaC) | Không máy chủ & IaC | AWS Lambda, CloudFormation, SAM, Serverless workshop thực tế |

---

## 📈 Lộ trình & Theo dõi Tiến độ (Curriculum & Tracking)

Vui lòng truy cập thư mục [curriculum](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/curriculum) để xem:
1. **[course_tracking.md](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/curriculum/course_tracking.md)**: Cập nhật các khóa học bạn đã hoàn thành (Hiển thị 23 khóa đã học).
2. **[pending_courses.md](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/curriculum/pending_courses.md)**: Danh sách 65 khóa học đang chờ phân bổ theo chủ đề để bạn chủ động chuẩn bị.
3. **[syllabus_foundation_phase1.csv](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/curriculum/syllabus_foundation_phase1.csv)**: Syllabus chính thức của Phase 1.
4. **[weeks/](file:///Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/curriculum/weeks)**: Thư mục chứa tài liệu học chi tiết theo từng tuần học (W1 đến W5 hiện tại). Mỗi tuần đều có đầy đủ **Learner Guide** và **Project Announcement** được dịch song ngữ Anh-Việt chuẩn chỉ.

Chúc bạn có những giờ học tập thật hiệu quả và chinh phục thành công chứng chỉ AWS DevOps/CloudOps! 🚀
