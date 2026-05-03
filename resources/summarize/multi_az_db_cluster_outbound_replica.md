# Multi-AZ DB Cluster — Outbound Read Replica

## Khái niệm

**Outbound Read Replica** là Read Replica được tạo ra **từ** một Multi-AZ DB Cluster, nằm **bên ngoài** cluster đó.

Cluster đóng vai trò **source** (nguồn), replica là **destination**.

```
Multi-AZ DB Cluster (writer) ──replication──► Read Replica (bên ngoài)
        [source]                                    [destination]
```

---

## Mục đích sử dụng

- **Cross-region DR**: đặt replica ở region khác, promote lên nếu region chính sập
- **Scale đọc thêm**: bổ sung ngoài 2 reader sẵn có trong cluster
- **Migration**: chuyển dữ liệu sang region hoặc account khác

---

## Inbound vs Outbound

| | Inbound Read Replica | Outbound Read Replica |
|---|---|---|
| Chiều replication | DB ngoài → Cluster | Cluster → DB ngoài |
| Mục đích chính | Migrate **vào** cluster | Migrate **ra** / DR / scale thêm |
| Source | DB instance cũ | Multi-AZ DB Cluster |
| Destination | Multi-AZ DB Cluster mới | Instance hoặc cluster khác |

---

## Chi tiết Multi-AZ DB Cluster

### Kiến trúc
- **1 writer + 2 reader**, mỗi instance 1 AZ
- Dùng **SSD NVMe local** (không qua EBS) → latency thấp hơn

### Replication
- Writer đẩy thay đổi sang 2 reader
- Cần **ít nhất 1 reader xác nhận** thì mới commit
- Đảm bảo dữ liệu không mất khi failover

### Failover
- Tự động chọn reader có log mới nhất
- Thời gian: thường **< 35 giây** (Multi-AZ Instance ~60 giây)
- Không cần replica bên ngoài — failover nội bộ giữa 3 instance trong cluster
- Sau failover, RDS **tự tạo instance mới** thay thế cái vừa chết → cluster luôn duy trì 1 writer + 2 reader

### Lợi thế
- Latency giao dịch **nhanh gấp 2x** so với Multi-AZ Instance
- 2 reader tự load balance, không cần proxy thêm
- Có thể gắn thêm **tối đa 15 Read Replica** bên ngoài cluster (outbound)
- Nâng cấp phiên bản nhỏ chỉ 35 giây (hoặc 1 giây nếu dùng RDS Proxy)

### Dùng khi
- Cần đọc nhiều
- Độ trễ thấp
- Luôn sẵn sàng (HA cao nhất)

---

## So sánh các loại triển khai RDS

| | Single-AZ Instance | Multi-AZ Instance | Multi-AZ DB Cluster |
|---|---|---|---|
| Số instance | 1 | 2 (1 primary + 1 standby) | 3 (1 writer + 2 reader) |
| Số AZ | 1 | 2 | 3 |
| Reader nhận traffic? | — | ❌ | ✅ |
| Replication | — | Sync (block-level) | Sync (transaction-level) |
| Failover | ❌ | ~1-2 phút | ~35 giây |
| Storage | EBS | EBS | SSD NVMe local |
| Latency | Baseline | Baseline | 2x nhanh hơn |
