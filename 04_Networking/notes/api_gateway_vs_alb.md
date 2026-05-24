# API Gateway vs ALB — Khi nào dùng cái nào?

## API Gateway là gì trong bức tranh Networking?

API Gateway không phải networking component thuần túy như VPC hay subnet — nó là **entry point** cho traffic vào hệ thống, nằm ở tầng application (L7).

```
Internet
    ↓
[API Gateway]          ← "cửa vào" — xử lý auth, routing, throttling
    ↓
[Lambda / EC2 / ECS]   ← backend xử lý
    ↓
[DynamoDB / RDS]       ← data layer
```

API Gateway đứng ở **edge** — nhận HTTP/HTTPS request từ client, route đến backend dựa trên path và method.

---

## Tại sao API Gateway liên quan đến Networking?

**1. Thay thế load balancer trong serverless pattern**

Thay vì dùng ALB để route traffic vào EC2, dùng API Gateway để route vào Lambda.

**2. VPC Integration qua VPC Link**

```
Internet → API Gateway → VPC Link → Private ALB → EC2 trong private subnet
```

Không có VPC Link, không thể reach resource trong private subnet từ API Gateway.

**3. Private API Gateway**

Có thể tạo API Gateway chỉ accessible từ trong VPC — không expose ra internet.

**4. Xử lý một số việc mà firewall/security group làm**
- Throttling (rate limiting)
- API key authentication
- IP whitelisting qua Resource Policy
- WAF integration

---

## So sánh API Gateway vs ALB

| | API Gateway | ALB |
|---|---|---|
| Layer | Application (L7) | Network (L3/L4) + Application |
| Quan tâm đến | HTTP method, path, headers | IP, port, protocol |
| Backend phù hợp | Lambda, HTTP endpoints | EC2, ECS, containers |
| Max payload | 10 MB | 1 GB |
| Timeout | 29 giây | 4000 giây |
| Billing | Per request | Theo giờ (dù không có traffic) |
| Latency overhead | ~10–50ms | ~1ms |
| API versioning | ✅ có sẵn | ❌ |
| API key + usage plans | ✅ có sẵn | ❌ |
| Request/response transform | ✅ | ❌ |
| Built-in throttling | ✅ | ❌ |
| WebSocket / gRPC hiệu năng cao | ⚠️ giới hạn | ✅ tốt hơn |

---

## Khi nào chọn API Gateway?

- **Backend là Lambda** — đây là use case rõ ràng nhất, API Gateway được thiết kế cho việc này
- **Cần API management**: versioning (`/v1`, `/v2`), API key, usage plans, mock responses
- **Cần auth tích hợp sâu**: Cognito Authorizer hoặc Lambda custom authorizer gắn trực tiếp
- **Traffic không đều, có thể về 0** — không trả tiền khi không có request

---

## Khi nào chọn ALB?

- **Backend là EC2, ECS, container** — ALB tối ưu cho long-running servers, giữ persistent connection, handle health check, drain connection khi deploy
- **Cần WebSocket hoặc gRPC thực sự** với high-throughput
- **Latency là ưu tiên số 1** — ALB chỉ thêm ~1ms overhead
- **Request size lớn** — ALB handle tới 1GB payload

---

## Pattern kết hợp cả hai

Nhiều hệ thống production dùng cả hai:

```
Internet
    ↓
API Gateway          ← xử lý auth, throttling, versioning
    ↓
ALB (qua VPC Link)   ← load balance vào ECS cluster
    ↓
ECS containers
```

API Gateway lo phần "API management", ALB lo phần "load balancing".

---

## Tóm tắt quyết định

```
Serverless / Lambda-based?
→ Dùng API Gateway

Container / EC2-based?
→ Dùng ALB

Cần API management (versioning, keys, throttle)?
→ Dùng API Gateway dù backend là gì

Cần performance tối đa, payload lớn, long connection?
→ Dùng ALB
```
