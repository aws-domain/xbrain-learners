# Serverless & IaC — Core Knowledge Summary

> **Scope:** W1 + W2 + W3 — Kiến thức tổng quát, chưa bao gồm W4–W7
> **Covers:** AWS Lambda Foundations, Introduction to AWS Lambda (Lab), Getting Started with AWS CloudFormation, Introduction to Amazon API Gateway

---

## 1. AWS Lambda

### Lambda là gì?
- **Serverless compute** — chạy code mà không cần quản lý server.
- AWS lo: provisioning, scaling, patching, availability.
- Bạn chỉ lo: code và configuration.
- **Event-driven** — Lambda chạy khi có event trigger, không chạy liên tục.

### Cách Lambda hoạt động
```
Event Source → [Trigger] → Lambda Function → [Output]
(S3, API GW,    (invoke)   (code chạy)       (response,
 DynamoDB,                                    side effects)
 SQS, SNS...)
```

### Lambda Key Concepts

**Handler** — entry point của function:
```python
def lambda_handler(event, context):
    # event: data từ trigger
    # context: runtime info (timeout còn lại, request ID...)
    return {"statusCode": 200, "body": "Hello"}
```

**Execution Role** — IAM Role Lambda assume để có quyền gọi AWS services:
- Cần `AWSLambdaBasicExecutionRole` để write CloudWatch Logs
- Cần `AWSLambdaVPCAccessExecutionRole` nếu Lambda trong VPC
- Thêm permissions tùy theo service Lambda cần gọi (S3, DynamoDB...)

**Timeout** — tối đa 15 phút (900 giây). Default 3 giây — tăng lên nếu cần.

**Memory** — 128MB đến 10,240MB. CPU tỉ lệ thuận với memory.

**Environment Variables** — lưu config, không hardcode trong code:
```python
import os
TABLE_NAME = os.environ['TABLE_NAME']
```

### Lambda Triggers Phổ Biến
| Trigger | Use case |
|---------|---------|
| **API Gateway** | REST API, HTTP endpoint |
| **S3** | Xử lý file khi upload (resize image, parse CSV) |
| **DynamoDB Streams** | React khi data thay đổi |
| **SQS** | Process messages từ queue |
| **SNS** | Nhận notifications |
| **EventBridge** | Scheduled tasks (cron), event routing |
| **CloudFront** | Lambda@Edge — xử lý request gần user |

### Lambda Pricing
- **Pay per request:** $0.20 per 1M requests
- **Pay per duration:** $0.0000166667 per GB-second
- **Free tier:** 1M requests + 400,000 GB-seconds/tháng

### Cold Start vs Warm Start
- **Cold start:** Lambda chưa có execution environment sẵn → phải init (~100ms–1s tùy runtime)
- **Warm start:** Execution environment còn tồn tại → chạy ngay, không có init time
- **Giảm cold start:** Provisioned Concurrency, giữ function warm, dùng runtime nhẹ (Python, Node.js)

### Lambda Concurrency
- **Concurrency** = số Lambda instances chạy đồng thời
- **Reserved Concurrency:** Giới hạn tối đa concurrency của 1 function — tránh throttle account
- **Provisioned Concurrency:** Pre-warm instances sẵn — loại bỏ cold start

---

## 2. Amazon API Gateway

### API Gateway là gì?
- **Managed service** để tạo, publish, maintain, monitor REST/HTTP/WebSocket APIs.
- Thường đứng trước Lambda — nhận HTTP request, invoke Lambda, trả response.

### Luồng cơ bản
```
Client → API Gateway → Lambda → DynamoDB/RDS/S3
                    ↑
              (auth, throttle,
               transform request)
```

### API Types
| Type | Dùng cho |
|------|---------|
| **REST API** | Full-featured, nhiều config options |
| **HTTP API** | Đơn giản hơn, rẻ hơn, low-latency |
| **WebSocket API** | Real-time, bidirectional (chat, gaming) |

### Key Features
- **Authentication:** IAM, Cognito, Lambda Authorizer
- **Throttling:** Giới hạn requests/giây để bảo vệ backend
- **Caching:** Cache response để giảm Lambda invocations
- **Stages:** dev, staging, prod — deploy API lên nhiều stage

---

## 3. AWS CloudFormation

### CloudFormation là gì?
- **Infrastructure as Code (IaC)** — định nghĩa AWS resources bằng YAML/JSON template.
- Deploy, update, delete resources theo template — **reproducible và consistent**.
- **Stack:** Tập hợp resources được tạo từ 1 template.

### Template Structure
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'My stack description'

Parameters:          # Input values khi deploy
  EnvironmentName:
    Type: String
    Default: dev

Resources:           # Bắt buộc — định nghĩa resources
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${EnvironmentName}-my-bucket'

Outputs:             # Export values để dùng ở stack khác
  BucketName:
    Value: !Ref MyBucket
```

### Intrinsic Functions Hay Dùng
| Function | Dùng để |
|----------|---------|
| `!Ref` | Reference resource hoặc parameter |
| `!Sub` | String substitution với variables |
| `!GetAtt` | Lấy attribute của resource |
| `!Join` | Nối strings |
| `!If` | Conditional logic |
| `!ImportValue` | Import output từ stack khác |

### CloudFormation vs Terraform
| | CloudFormation | Terraform |
|---|---|---|
| Provider | AWS only | Multi-cloud |
| Language | YAML/JSON | HCL |
| State management | AWS lo | Tự quản lý state file |
| Rollback | Tự động | Manual |
| Dùng khi | AWS-only, muốn native integration | Multi-cloud, team đã quen Terraform |

### Change Sets
- Preview thay đổi trước khi apply — xem resource nào sẽ được tạo/update/xóa.
- Best practice: luôn review change set trước khi execute trên production.

---

## 4. Serverless Architecture Pattern

Pattern phổ biến cho web API:

```
Client
  │
  ▼
API Gateway (HTTP endpoint)
  │
  ▼
Lambda (business logic)
  │
  ├──→ DynamoDB (data store)
  ├──→ S3 (file storage)
  └──→ SQS/SNS (async messaging)
```

**Ưu điểm:**
- Không quản lý server
- Auto-scale tự động
- Pay per use — không tốn tiền khi không có traffic
- High availability built-in

**Nhược điểm:**
- Cold start latency
- Timeout tối đa 15 phút — không phù hợp long-running tasks
- Debugging phức tạp hơn
- Vendor lock-in

---

## Quick Reference

**Q: Lambda Execution Role là gì?**
A: IAM Role mà Lambda assume khi chạy — cho phép Lambda gọi các AWS services khác. Cần ít nhất `AWSLambdaBasicExecutionRole` để write logs. Nếu Lambda trong VPC cần thêm `AWSLambdaVPCAccessExecutionRole` để tạo ENI.

**Q: Cold start là gì và cách giảm?**
A: Cold start xảy ra khi Lambda chưa có execution environment sẵn — phải init runtime trước khi chạy code (~100ms–1s). Giảm bằng: Provisioned Concurrency (pre-warm), dùng runtime nhẹ (Python/Node.js thay Java), giảm package size.

**Q: CloudFormation Stack là gì?**
A: Tập hợp AWS resources được tạo và quản lý cùng nhau từ 1 template. Xóa stack → xóa tất cả resources trong stack. Update stack → CloudFormation tính toán diff và chỉ update những gì thay đổi.

**Q: API Gateway HTTP API vs REST API?**
A: HTTP API đơn giản hơn, rẻ hơn (~70%), latency thấp hơn — dùng cho hầu hết use cases. REST API có nhiều tính năng hơn (caching, request validation, usage plans) — dùng khi cần những tính năng đó.
