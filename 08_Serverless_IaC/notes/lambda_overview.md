# AWS Lambda — Tổng Quan Kiến Thức

---

## 1. Serverless là gì?

Serverless là mô hình điện toán đám mây cho phép bạn **chạy code mà không cần quản lý server**. AWS xử lý toàn bộ hạ tầng bên dưới.

| Tác vụ | Traditional | Serverless |
|---|---|---|
| Cấu hình instance | ✅ | ❌ |
| Cập nhật OS | ✅ | ❌ |
| Cài application platform | ✅ | ❌ |
| Build & deploy app | ✅ | ✅ |
| Cấu hình auto scaling | ✅ | ❌ |
| Monitor & maintain app | ✅ | ✅ |

---

## 2. AWS Lambda là gì?

AWS Lambda là **compute service** cho phép chạy code theo sự kiện (event-driven), không cần provisioning hay quản lý server.

### Đặc điểm chính
- Chạy code khi có event xảy ra — không chạy thì không tốn tiền
- Tự động scale theo số lượng request
- Tích hợp sẵn monitoring & logging qua Amazon CloudWatch
- Hỗ trợ nhiều ngôn ngữ: **Node.js, Python, Java, Go, C#, Ruby, PowerShell**
- Billing theo **1-millisecond increments**

### Lambda function là gì?
Một Lambda function là một đoạn code nhỏ, **stateless**, tự chứa (self-contained). Mỗi function bao gồm:
- Code + dependencies
- Tên function
- Cấu hình tài nguyên (memory, timeout)

---

## 3. Event-Driven Architecture

Lambda hoạt động theo mô hình **Producer → Router → Consumer**.

```
[Event Producer]  →  [Event Router]  →  [Event Consumer / Lambda]
  (S3, API GW,        (EventBridge,        (Lambda function
   DynamoDB...)         SNS, SQS...)         xử lý event)
```

- **Producer**: tạo ra event (user upload file, đặt hàng, gửi request...)
- **Router**: lọc và chuyển event đến đúng consumer
- **Consumer**: Lambda nhận event và xử lý

---

## 4. Các Invocation Model (Cách gọi Lambda)

### 4.1 Synchronous (Đồng bộ)
- Lambda chạy và **chờ trả kết quả** ngay lập tức
- **Không có retry** tự động — phải tự xử lý trong code
- Dùng khi: **API Gateway, Cognito, CloudFormation, Alexa, Lex, CloudFront**

### 4.2 Asynchronous (Bất đồng bộ)
- Event được **đưa vào queue**, không cần chờ kết quả
- **Tự động retry 2 lần** khi thất bại
- Hỗ trợ **Destinations** để gửi kết quả thành công/thất bại đến service khác
- Dùng khi: **SNS, S3, EventBridge**

### 4.3 Polling (Thăm dò)
- Lambda **tự động poll** (theo dõi) các streaming/queue service
- Retry tùy thuộc vào cấu hình event source
- Dùng khi: **Kinesis, SQS, DynamoDB Streams**

| Model | Retry | Ví dụ |
|---|---|---|
| Synchronous | Không có | API Gateway |
| Asynchronous | 2 lần | S3, SNS |
| Polling | Tùy event source | SQS, Kinesis |

---

## 5. Execution Environment (Môi trường thực thi)

### Vòng đời
```
[INIT Phase]  →  [INVOKE Phase]  →  [SHUTDOWN Phase]
```

1. **Init**: Tạo môi trường, download code, khởi tạo extensions, runtime, và code ngoài handler
2. **Invoke**: Chạy handler function, sau đó sẵn sàng cho invocation tiếp theo
3. **Shutdown**: Khi không có invocation trong một thời gian, Lambda tắt môi trường

### Cold Start vs Warm Start

| | Cold Start | Warm Start |
|---|---|---|
| Khi nào xảy ra | Môi trường mới, function chưa chạy | Môi trường đã tồn tại |
| Thời gian | Chậm hơn (phải init) | Nhanh hơn |
| Chi phí | Billing bắt đầu sau khi runtime init xong | Chỉ tính thời gian chạy code |

### Giảm thiểu Cold Start
- Dùng **Provisioned Concurrency** — giữ môi trường luôn warm
- Lưu dependencies cục bộ
- Hạn chế re-initialization biến
- Tái sử dụng connections hiện có
- Dùng `/tmp` làm transient cache

---

## 6. Permissions (Phân quyền)

Lambda dùng **2 loại IAM policy**:

### 6.1 Execution Role
- Định nghĩa Lambda **được làm gì** với các service khác (VD: ghi vào DynamoDB)
- Bao gồm **IAM Policy** (actions được phép) + **Trust Policy** (cho phép Lambda AssumeRole)
- Nguyên tắc: **Least Privilege** — chỉ cấp quyền tối thiểu cần thiết

### 6.2 Resource-based Policy (Function Policy)
- Định nghĩa **ai được phép invoke** Lambda function
- Tự động tạo khi bạn thêm trigger từ console
- Dùng để cấp quyền cross-account

```
Resource Policy  →  "Ai được gọi Lambda?"   (VD: S3 được invoke function này)
Execution Role   →  "Lambda được làm gì?"    (VD: Lambda được ghi vào DynamoDB)
```

---

## 7. Authoring (Viết code Lambda)

### Handler Method
Entry point của Lambda function, nhận 2 tham số:
- **Event Object** *(bắt buộc)*: chứa dữ liệu từ event source (path, body, bucket name...)
- **Context Object** *(tùy chọn)*: metadata về execution (request ID, thời gian còn lại, log stream...)

```python
def lambda_handler(event, context):
    # event: thông tin từ trigger (VD: S3 bucket, API request)
    # context: thông tin về môi trường thực thi
    return {"statusCode": 200, "body": "Hello"}
```

### Design Best Practices
- **Tách business logic** ra khỏi handler — dễ test, dễ port
- **Modular functions** — mỗi function làm 1 việc (Single Responsibility)
- **Stateless** — không lưu state trong function, dùng DynamoDB/S3/ElastiCache
- **Chỉ include những gì cần** — giảm deployment package size → giảm cold start

### Coding Best Practices
- Dùng **logging** (ghi vào CloudWatch)
- Dùng **environment variables** cho config — không hardcode
- Dùng **AWS Secrets Manager / Parameter Store** cho sensitive data
- **Tránh recursive code** — có thể gây uncontrolled scaling
- Tái sử dụng execution context khi warm start

---

## 8. Cấu hình Lambda Function

### 8.1 Memory
- Tối đa **10 GB**
- CPU được cấp phát **tỉ lệ thuận** với memory
- Dùng **Lambda Power Tuning** để tìm cấu hình tối ưu (cost vs speed)

### 8.2 Timeout
- Tối đa **900 giây (15 phút)**
- Set timeout phù hợp — không nên để max nếu không cần
- Billing tính theo thời gian thực thi (1ms increments)

### 8.3 Concurrency (Đồng thời)
Số lượng invocations chạy **cùng một lúc**.

| Loại | Mô tả |
|---|---|
| **Unreserved** | Concurrency chung, tối thiểu 100 cho các function không có reservation |
| **Reserved** | Đảm bảo số lượng concurrent instances tối đa cho 1 function cụ thể |
| **Provisioned** | Khởi tạo sẵn môi trường — dùng khi cần low latency, high performance |

**Lý do set concurrency limit:**
- Kiểm soát chi phí
- Điều tiết tốc độ xử lý batch
- Match với downstream resource (VD: RDS không scale nhanh bằng Lambda)

---

## 9. Deployment

### 3 cách deploy Lambda
1. **Lambda Console Editor** — phù hợp cho function đơn giản, không có custom library
2. **Deployment Package** — `.zip` file hoặc **Container Image** (push lên ECR)
3. **Automation Tools** — AWS SAM + CodeBuild/CodeDeploy/CodePipeline

### AWS SAM (Serverless Application Model)
Framework open-source để build serverless app. SAM template (YAML) được transform thành CloudFormation template.

```yaml
# Ví dụ SAM template đơn giản
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello-world/
      Handler: app.lambdaHandler
      Runtime: nodejs16.x
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

### Versioning & Aliases
- **Version**: snapshot bất biến của function (`$LATEST` → publish → `v1`, `v2`...)
- **Alias**: pointer đến một version cụ thể (VD: `prod` → v2, `beta` → v3)
- **Traffic shifting**: alias có thể chia traffic giữa 2 versions (VD: 90% v1, 10% v2)

### AWS CodeDeploy Traffic Shifting
- **Canary**: shift traffic 2 lần
- **Linear**: shift dần đều theo % mỗi X phút
- **All-at-once**: chuyển toàn bộ traffic ngay lập tức

---

## 10. Monitoring & Troubleshooting

### Amazon CloudWatch Metrics
| Metric | Ý nghĩa |
|---|---|
| Invocations | Số lần function được gọi |
| Duration | Thời gian thực thi |
| Errors | Số lần lỗi |
| Throttles | Số lần bị từ chối do vượt concurrency limit |
| ConcurrentExecutions | Số instances đang chạy đồng thời |
| DeadLetterErrors | Số lần gửi vào DLQ thất bại |

### AWS X-Ray
- Visualize các component của application
- Phân tích **cold start vs warm start**
- Tìm bottleneck và lỗi trong luồng xử lý

### AWS CloudTrail
- Audit toàn bộ API calls
- Hỗ trợ rollback khi có deployment không mong muốn

### Dead-Letter Queue (DLQ)
- Lưu các invocation **thất bại** để xử lý thủ công sau
- Dùng cho **asynchronous** và **non-stream polling** events
- DLQ có thể là **SQS queue** hoặc **SNS topic**

---

## 11. AWS Serverless Platform — Tổng quan

| Category | Services |
|---|---|
| Compute | AWS Lambda, Lambda@Edge |
| Orchestration | AWS Step Functions |
| Storage | Amazon S3 |
| Data stores | Amazon DynamoDB |
| Event bus | Amazon EventBridge |
| Messaging | Amazon SNS, Amazon SQS |
| API Integration | Amazon API Gateway, AWS AppSync |
| Developer tools | AWS CDK, AWS SAM |

---

## 12. Nguyên tắc quyết định tách Lambda riêng

> **"Mỗi Lambda function nên làm đúng 1 việc — đặt tên được bằng `[động từ] + [danh từ]` là dấu hiệu tốt."**

| Câu hỏi | Nếu YES → Tách riêng |
|---|---|
| Trigger khác nhau? | S3 event vs API Gateway |
| Memory/timeout yêu cầu khác? | ML cần 3GB, gửi email chỉ cần 128MB |
| Có thể fail độc lập? | Lỗi email không nên ảnh hưởng payment |
| Tần suất gọi khác nhau nhiều? | 10,000 lần/ngày vs 5 lần/ngày |
| Team khác nhau maintain? | Ownership rõ ràng |
