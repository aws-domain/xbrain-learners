# Event-Driven Architecture (EDA) — Kiến trúc Hướng Sự Kiện

---

## 1. EDA là gì?

Event-Driven Architecture là kiến trúc trong đó các service **giao tiếp với nhau thông qua events** — thay vì gọi trực tiếp vào nhau.

- **Event** = một thay đổi trạng thái hoặc một cập nhật, được biểu diễn dưới dạng **JSON**
- Các service **không cần biết nhau** — chỉ cần biết event có hình dạng (shape) như thế nào
- Đây là nền tảng của **Serverless architecture**: linh hoạt, scalable, loosely coupled

---

## 2. Luồng hoạt động — Ví dụ GET /users

```
Client (browser/app)
    │
    │  GET /users  (HTTP request)
    ▼
API Gateway          ← đóng vai trò URL Router
    │
    │  Chuyển HTTP request → JSON event
    ▼
Lambda Function
    │
    │  Query data
    ▼
DynamoDB
    │
    │  Trả data về Lambda
    ▼
Lambda Function
    │
    │  Đóng gói → JSON response event
    ▼
API Gateway
    │
    │  Lấy phần "body" → gửi HTTP response
    ▼
Client nhận kết quả
```

---

## 3. API Gateway — URL Router là gì?

### Khái niệm URL Router

Trong bất kỳ web app nào, khi có nhiều URL khác nhau, cần có thứ gì đó quyết định:
> *"Request đến `/users` thì xử lý ở đâu? Đến `/admin/login` thì xử lý ở đâu?"*

Đó là nhiệm vụ của **URL Router**.

### So sánh Local vs AWS

| | Local (truyền thống) | AWS Serverless |
|---|---|---|
| Địa chỉ | `localhost:8080/admin/login` | `https://abc123.execute-api.amazonaws.com/admin/login` |
| URL Router | Express / Flask / Spring | **API Gateway** |
| Xử lý logic | Controller/hàm trong server | **Lambda function** |
| Server chạy liên tục? | ✅ Luôn bật | ❌ Chỉ chạy khi có request |

> **Kết luận**: `localhost:8080/admin/login` và `https://....amazonaws.com/admin/login` là **cùng một khái niệm** — một cái chạy trên máy bạn, một cái chạy trên cloud không cần server thường trực.

---

## 4. Event trông như thế nào?

Khi client gọi `POST /admin/login`, API Gateway **không gọi thẳng Lambda** — nó tạo ra một JSON event rồi mới gửi vào Lambda:

```json
{
  "httpMethod": "POST",
  "path": "/admin/login",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"username\": \"alice\", \"password\": \"secret123\"}"
}
```

Lambda nhận JSON này qua tham số `event` trong handler.

---

## 5. Code so sánh — Local vs Lambda

### Local với Express (Node.js)
```javascript
app.post("/admin/login", (req, res) => {
    const { username, password } = req.body
    // xử lý login...
    res.json({ token: "abc123" })
})
```

### AWS Lambda tương đương
```python
import json

def lambda_handler(event, context):
    body = json.loads(event["body"])
    username = body["username"]
    password = body["password"]

    # xử lý login...

    return {
        "statusCode": 200,
        "body": json.dumps({"token": "abc123"})
    }
```

Lambda **không trả response trực tiếp về client** — nó trả về một JSON event cho API Gateway. API Gateway mới là người gửi HTTP response về client.

---

## 6. Tại sao Lambda không gửi thẳng về client?

Vì Lambda **không biết client là ai**. Lambda chỉ có một nhiệm vụ:
> *"Nhận event → xử lý → trả về event."*

**API Gateway** mới là người giữ kết nối HTTP với client.

```
Lambda trả về:            API Gateway gửi về client:
{                         HTTP 200 OK
  "statusCode": 200,  →   Content-Type: application/json
  "body": "..."
}                         {"token": "abc123"}
```

---

## 7. Tóm tắt vai trò từng thành phần

| Thành phần | Vai trò | Tương đương local |
|---|---|---|
| **Client** | Gửi HTTP request | Browser / Postman |
| **API Gateway** | Nhận request, chuyển thành event, route đến Lambda | Express router / URL dispatcher |
| **Lambda** | Xử lý business logic | Controller / handler function |
| **DynamoDB / DB** | Lưu trữ dữ liệu | Database (MySQL, PostgreSQL...) |
| **Event (JSON)** | Ngôn ngữ giao tiếp giữa các service | req/res object trong Express |

---

## 8. Điểm khác biệt cốt lõi

> Trên local, server **luôn chạy** và lắng nghe request.
>
> Trên AWS, **không có server thường trực** — khi có request, AWS mới khởi động Lambda để xử lý, xong rồi tắt. Đây chính là bản chất của **Serverless**.
