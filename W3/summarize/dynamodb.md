# DynamoDB

## 1. Mục đích

DynamoDB là **serverless, fully managed NoSQL database** trên AWS.

### So sánh với RDS

| | RDS | DynamoDB |
|---|---|---|
| Model | Managed (PaaS) | Serverless |
| Server | EC2 instance chạy ngầm | Không có server |
| Scale | Manual resize hoặc Auto Scaling | Tự động hoàn toàn |
| Idle cost | Trả tiền 24/7 | On-demand: không request = không tốn tiền |
| Connections | Giới hạn theo instance size | Không giới hạn |

> RDS vẫn được AWS managed một phần (OS patching, engine updates), nhưng vẫn phải chọn instance type, manage connections, scale manually — đó là điểm khác biệt cốt lõi với DynamoDB.

---

## 2. Vấn đề DynamoDB giải quyết

**Flexible schema:**
- Mỗi item có thể có attributes khác nhau hoàn toàn
- Không cần khai báo schema trước
- Thêm attribute mới → chỉ cần ghi item mới, zero downtime

**So với MySQL trong production:**
- Phải định nghĩa tất cả columns từ đầu
- Thêm column mới → `ALTER TABLE` có thể lock toàn bộ table hàng giờ với hàng triệu rows → downtime thực sự

---

## 3. Lợi ích

### TTL (Time To Live)
- Tự động xóa expired items — không cần viết cron job hay Lambda cleanup
- Benefit: **cost + operational simplicity** (không phải performance)
- TTL attribute phải là kiểu `Number`, giá trị là Unix timestamp
- TTL deletion có thể **trễ đến 48 giờ** — eventual deletion, không phải exact deletion
- Không nên để business logic rely hoàn toàn vào TTL → app phải tự check khi đọc:

```python
if item.get("ttl", 0) < int(time.time()):
    return None  # Treat as expired
```

**TTL values:**
```python
import time
from datetime import datetime

ttl_value = int(time.time()) + 86400  # expire sau 24h
print(f"TTL value: {ttl_value}")
print(f"Expires at: {datetime.fromtimestamp(ttl_value)}")
```

**Lưu ý production:**
- TTL được set tự động trong application code lúc ghi data
- Items không có TTL attribute → không bị xóa
- Items cũ không có TTL → chạy script một lần để update, hoặc để tồn tại

---

## 4. Pricing

| | On-Demand | Provisioned |
|---|---|---|
| Cách tính tiền | Theo từng request | Theo RCU/WCU đặt trước |
| Traffic pattern | Unpredictable, burst | Stable, dự đoán được |
| Scale | Tự động | Manual hoặc Auto Scaling |
| Cost | Cao hơn khi traffic ổn định | Rẻ hơn khi traffic ổn định |
| Free tier | Không cover | 25 RCU + 25 WCU vĩnh viễn |

- Session data (traffic unpredictable, burst cao giờ cao điểm) → **On-demand**
- Traffic ổn định, biết trước → **Provisioned** để tiết kiệm chi phí

### Chi tiết Capacity Units
- **RCU:** 1 strongly consistent read 4KB/s, hoặc 2 eventually consistent reads 4KB/s
- **WCU:** 1 write 1KB/s
- Có thể switch giữa 2 mode, nhưng chỉ **2 lần/ngày**
- On-Demand đắt hơn ~6-7x per request so với Provisioned nếu traffic ổn định

---

## Bonus — Unix Timestamp

- Là số giây tính từ **January 1, 1970 00:00:00 UTC** đến một thời điểm
- Thay đổi mỗi giây
- Dùng **AWS CloudShell** để chạy Python nhanh khi đang làm việc trên AWS Console
