# Task 3.8 — Other In-Scope AWS Services

> **Exam weight:** Domain 3 = 34% of scored content

## Application Integration Services

### Amazon EventBridge
- **Serverless event bus** — kết nối applications với events
- Route events từ AWS services, SaaS apps, custom apps
- Dùng cho: event-driven architectures, microservices decoupling

### Amazon SNS (Simple Notification Service)
- **Pub/Sub messaging** — publish messages đến nhiều subscribers
- Protocols: HTTP/HTTPS, Email, SMS, SQS, Lambda
- **Fan-out pattern** — một message đến nhiều endpoints
- Dùng cho: notifications, alerts, mobile push

### Amazon SQS (Simple Queue Service)
- **Managed message queue** — decouple components
- **Standard Queue** — at-least-once delivery, best-effort ordering
- **FIFO Queue** — exactly-once processing, strict ordering
- Dùng cho: decoupling microservices, async processing

**SNS vs SQS:**
| | SNS | SQS |
|---|---|---|
| **Pattern** | Push (Pub/Sub) | Pull (Queue) |
| **Consumers** | Multiple simultaneously | One consumer per message |
| **Persistence** | Không | Có (up to 14 days) |
| **Use case** | Notifications, fan-out | Task queues, decoupling |

---

## Business Application Services

### Amazon Connect
- **Cloud contact center** service
- Omnichannel: voice, chat
- Tích hợp với AI/ML (Lex, Comprehend)
- Pay-per-minute pricing

### Amazon SES (Simple Email Service)
- **Managed email service**
- Gửi transactional, marketing, bulk emails
- High deliverability, cost-effective
- Dùng cho: order confirmations, password resets, newsletters

---

## Developer Tools

### AWS CodeBuild
- **Managed build service** — compile code, run tests, produce artifacts
- Không cần quản lý build servers
- Pay-per-minute

### AWS CodePipeline
- **CI/CD pipeline** automation
- Orchestrate: source → build → test → deploy
- Tích hợp với CodeBuild, CodeDeploy, GitHub, Jenkins

### AWS CodeDeploy
- **Automated deployment** đến EC2, Lambda, ECS, on-premises
- Rolling deployments, blue/green deployments

### AWS X-Ray
- **Distributed tracing** — debug và analyze microservices
- Visualize request flow qua các services
- Identify bottlenecks và errors

### AWS CodeCommit *(deprecated)*
- Managed Git repositories (AWS đã ngừng nhận customers mới)

---

## End-User Computing

### Amazon AppStream 2.0
- **Stream desktop applications** đến browsers
- Không cần cài app trên máy người dùng
- Dùng cho: enterprise apps, education

### Amazon WorkSpaces
- **Managed virtual desktops** (VDI)
- Windows hoặc Linux desktops trên cloud
- Dùng cho: remote work, BYOD, secure access

### Amazon WorkSpaces Secure Browser
- **Managed browser** cho secure web access
- Không cần VPN
- Dùng cho: contractors, third-party access

---

## Frontend Web and Mobile Services

### AWS Amplify
- **Full-stack development platform** cho web và mobile apps
- Hosting, authentication, APIs, storage
- Tích hợp với React, Vue, Angular, iOS, Android

### AWS AppSync
- **Managed GraphQL API** service
- Real-time data sync
- Tích hợp với DynamoDB, Lambda, RDS

---

## IoT Services

### AWS IoT Core
- **Connect và manage IoT devices** at scale
- Secure, bi-directional communication
- Tích hợp với Lambda, S3, DynamoDB, CloudWatch
- Hỗ trợ MQTT, HTTPS protocols

---

## Exam Tips

- SNS = push notifications, fan-out; SQS = queue, decoupling
- EventBridge = event-driven architecture, routing events
- CodePipeline = CI/CD orchestration; CodeBuild = build/test
- X-Ray = distributed tracing cho microservices
- Amplify = full-stack web/mobile development
- WorkSpaces = virtual desktops; AppStream = stream applications
- IoT Core = connect IoT devices to AWS
