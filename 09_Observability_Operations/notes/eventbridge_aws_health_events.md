# EventBridge + AWS Health Events — Phản ứng tự động với sự kiện sức khỏe tài khoản

## 📌 Tổng quan cốt lõi (Core Concepts)
*Dùng Amazon EventBridge để phát hiện thay đổi trạng thái của AWS Health event, rồi tự động thông báo hoặc xử lý thay vì ngồi canh dashboard.*
- **AWS Health (trước đây gọi là Personal Health Dashboard):** Cung cấp thông tin cá nhân hóa về sự cố dịch vụ, bảo trì theo lịch và thông báo ảnh hưởng trực tiếp tới tài nguyên trong tài khoản của bạn.
- **EventBridge rule:** Khi một Health event khớp với event pattern bạn khai báo, EventBridge gọi một hoặc nhiều **target**.
- **Cấu trúc event:** `source` = `aws.health`, `detail-type` = `AWS Health Event`. Có thể lọc thêm theo `detail.service`, `detail.eventTypeCategory` (`issue`, `accountNotification`, `scheduledChange`, `investigation`).
- **Tùy loại event**, bạn có thể: gửi thông báo, lưu lại thông tin event, thực hiện hành động khắc phục, kích hoạt event khác.

---

## 📐 Sơ đồ Hoạt động (Architectural Flow)

```
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────────────┐
│  AWS Health  │ ─► │ EventBridge (default │ ─► │ Rule: event pattern      │
│  event       │    │ event bus)           │    │ source = aws.health      │
└──────────────┘    └──────────────────────┘    └────────────┬─────────────┘
                                                             │ match
            ┌──────────────┬──────────────┬─────────────┬────┴──────────┐
            ▼              ▼              ▼             ▼               ▼
      ┌──────────┐   ┌──────────┐   ┌──────────┐  ┌───────────┐  ┌──────────────┐
      │  Lambda  │   │ Kinesis  │   │   SQS    │  │ Built-in  │  │  SNS topic   │
      │ function │   │ stream   │   │  queue   │  │ (CW alarm │  │ (email/SMS)  │
      └──────────┘   └──────────┘   └──────────┘  │  actions) │  └──────────────┘
                                                  └───────────┘
```

---

## 🎯 Các loại Target dùng trong workflow AWS Health

| Target | Dùng để làm gì |
|---|---|
| **AWS Lambda function** | Xử lý tùy biến: định dạng lại nội dung, đẩy sang Slack, tự động khắc phục. |
| **Kinesis streams** | Đưa event vào luồng dữ liệu để phân tích/lưu trữ. |
| **Amazon SQS queue** | Đệm event để consumer xử lý sau, tách rời hệ thống. |
| **Built-in targets (CloudWatch alarm actions)** | Kích hoạt hành động có sẵn của CloudWatch alarm. |
| **Amazon SNS topic** | Gửi thông báo email/SMS tới nhiều người nhận. |

## 🧩 Use case điển hình
- **Thông báo lên Slack:** Health event → EventBridge rule → **Lambda** → Slack channel webhook.
- **Email/SMS tùy biến:** Health event → EventBridge → **Lambda** (soạn nội dung) → **SNS** → text hoặc SMS.

---

## 🔐 Quyền truy cập của Target: Resource-based Policy vs IAM Role
Khi rule được kích hoạt, **tất cả target gắn với rule đều được gọi**. "Gọi" nghĩa là: invoke Lambda function, publish lên SNS topic, chuyển event vào Kinesis stream. Để gọi API trên tài nguyên của bạn, EventBridge cần được cấp quyền phù hợp.

| Target | Cơ chế cấp quyền |
|---|---|
| **AWS Lambda** | **Resource-based policy** (gắn trên function) |
| **Amazon SNS** | **Resource-based policy** (gắn trên topic) |
| **Amazon SQS** | **Resource-based policy** (gắn trên queue) |
| **Amazon CloudWatch Logs** | **Resource-based policy** (gắn trên log group) |
| **Kinesis streams** | **IAM role** (gắn với target của rule) |

- **IAM role của rule không có tác dụng với Lambda.** Với Lambda, bạn phải cấp resource-based policy cho principal `events.amazonaws.com`, ví dụ bằng `lambda:AddPermission`.
- IAM role cho rule chỉ dùng cho event liên quan đến **Kinesis streams** (trong phạm vi bài này).
- Tạo rule trên Console thì EventBridge thường tự thêm policy; tạo bằng CLI/IaC thì phải tự thêm.

---

## ⚠️ Lưu ý khi cấu hình (Gotchas)
- **Health event của dịch vụ global** (như IAM, Route 53, CloudFront) được phát tại **us-east-1**. Hãy tạo rule ở Region đó, và SNS topic target cũng phải cùng Region với rule.
- Tạo rule bằng CLI/IaC mà quên `lambda:AddPermission` thì rule không gọi được Lambda (xem mục quyền ở trên).
- **Gắn DLQ (SQS) cho target** để không mất event khi giao thất bại. DLQ chỉ bắt lỗi giao event của EventBridge, không bắt lỗi code bên trong Lambda.
- **Input transformer** giúp rút gọn JSON thô của Health event thành thông điệp dễ đọc trước khi gửi SNS.

## 🧠 Mẹo nhớ cho đề thi (SOA-C03)
- "Nhận thông báo khi AWS báo sự cố/bảo trì ảnh hưởng tài nguyên của tôi" → **AWS Health + EventBridge**.
- "Gửi cảnh báo Health lên Slack" → EventBridge → **Lambda** → Slack.
- "Gửi email/SMS" → target **SNS**, không phải SES.

## 🔗 Liên quan
- Lab thực hành EventBridge rule, input transformer, DLQ: `aws-certification/soa-co3/labs/domain-1-monitoring-performance/d1-05-eventbridge-rules-event-patterns-targets-dlq-input`
- Tổng quan EventBridge trong hệ sinh thái giám sát: [cloudwatch_getting_started.md](./cloudwatch_getting_started.md)
