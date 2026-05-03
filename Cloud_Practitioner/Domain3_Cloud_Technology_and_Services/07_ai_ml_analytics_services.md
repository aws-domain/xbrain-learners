# Task 3.7 — AI/ML and Analytics Services

> **Exam weight:** Domain 3 = 34% of scored content

## AI/ML Services

### Amazon SageMaker AI
- **End-to-end ML platform** — build, train, deploy ML models
- Managed Jupyter notebooks
- Dùng cho: data scientists và ML engineers
- Không cần quản lý infrastructure

### Amazon Rekognition
- **Computer vision** — phân tích images và videos
- Phát hiện: objects, faces, text, scenes, activities
- Use cases: content moderation, facial analysis, celebrity recognition

### Amazon Comprehend
- **Natural Language Processing (NLP)**
- Phân tích text: sentiment, entities, key phrases, language detection
- Use cases: customer feedback analysis, document classification

### Amazon Lex
- **Conversational AI** — build chatbots và voice interfaces
- Cùng technology với Amazon Alexa
- Tích hợp với Lambda, Connect, Kendra

### Amazon Polly
- **Text-to-Speech** — chuyển text thành giọng nói tự nhiên
- Hỗ trợ nhiều ngôn ngữ và giọng đọc

### Amazon Transcribe
- **Speech-to-Text** — chuyển audio thành text
- Hỗ trợ real-time và batch transcription

### Amazon Translate
- **Neural machine translation**
- Dịch text giữa nhiều ngôn ngữ

### Amazon Kendra
- **Intelligent enterprise search** powered by ML
- Tìm kiếm thông tin từ nhiều data sources
- Hiểu ngôn ngữ tự nhiên (không chỉ keyword search)

### Amazon Personalize
- **Real-time personalization và recommendations**
- Cùng technology với Amazon.com recommendations
- Không cần ML expertise

### Amazon Forecast
- **Time-series forecasting** sử dụng ML
- Dự báo: demand, inventory, financial metrics

### Amazon Textract
- **Extract text và data** từ documents (PDF, images)
- Nhận dạng forms, tables, handwriting

### Amazon Bedrock
- **Fully managed service** để build generative AI applications
- Truy cập foundation models từ AWS và third-parties (Anthropic, Meta, Mistral...)
- Không cần quản lý infrastructure

---

## Analytics Services

### Amazon Athena
- **Serverless SQL query** trực tiếp trên S3
- Không cần load data vào database
- Trả tiền theo lượng data scanned
- Dùng cho: ad-hoc queries, log analysis

### Amazon Kinesis
- **Real-time data streaming**
- **Kinesis Data Streams** — ingest và process streaming data
- **Kinesis Data Firehose** — load streaming data vào S3, Redshift, OpenSearch
- **Kinesis Data Analytics** — SQL queries trên streaming data
- Use cases: log analytics, IoT, clickstream analysis

### AWS Glue
- **Serverless ETL (Extract, Transform, Load)** service
- **Glue Data Catalog** — metadata repository cho data assets
- Tự động discover và catalog data
- Dùng cho: data preparation, data integration

### Amazon QuickSight
- **Business Intelligence (BI)** và data visualization
- Tạo interactive dashboards và reports
- Serverless, pay-per-session
- Tích hợp với: S3, RDS, Redshift, Athena...

### Amazon Redshift
- **Cloud data warehouse**
- Petabyte-scale analytics
- Columnar storage, massively parallel processing
- **Redshift Serverless** — không cần provision clusters

### Amazon OpenSearch Service
- **Search và analytics** engine (formerly Elasticsearch)
- Full-text search, log analytics, real-time monitoring

### AWS Data Exchange
- **Marketplace cho data** — subscribe và use third-party datasets
- Tích hợp với S3, Redshift, Athena

---

## Exam Tips

- SageMaker = build/train/deploy ML models (cho ML practitioners)
- Rekognition = image/video analysis
- Lex = chatbots (same tech as Alexa)
- Comprehend = NLP, text analysis
- Athena = SQL queries on S3, serverless
- Kinesis = real-time streaming data
- Glue = ETL, data catalog
- QuickSight = BI dashboards
- Redshift = data warehouse (not OLTP)
