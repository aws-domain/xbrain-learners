# Stateful vs Stateless — Initiate và Established Connections

---

## 1. Hai khái niệm cốt lõi

### Initiate connection

Là hành động **bắt đầu** một kết nối mới. Bên nào gửi packet đầu tiên thì bên đó đang initiate.

Trong TCP, packet đầu tiên mang cờ **SYN** — đây là tín hiệu "tôi muốn mở kết nối mới".

### Established connection

Là kết nối **đã được thiết lập xong** — cả 2 bên đã hoàn tất handshake, đang trao đổi data. Packet lúc này không phải "gõ cửa mới" mà là "tiếp tục cuộc trò chuyện đang có".

---

## 2. TCP Handshake — Hình dung rõ hơn

```
Client                         Server
  |                               |
  |------SYN (initiate)---------->|   Client bắt đầu kết nối
  |<-----SYN-ACK-----------------|   Server đồng ý
  |------ACK--------------------->|   Handshake hoàn tất
  |                               |
  |<======data (established)=====>|   Đây là established connection
  |<======data (established)=====>|
  |<======data (established)=====>|
```

Từ lúc ACK xong trở đi, mọi packet đi lại đều thuộc về **established connection** này.

---

## 3. Tại sao quan trọng trong AWS Networking?

Security Group và NACL xử lý established connection **hoàn toàn khác nhau** — đây là điểm phân biệt quan trọng nhất giữa 2 loại.

---

## 4. Security Group — Stateful

SG **nhớ trạng thái** của connection. Khi một packet được allow đi ra (outbound), SG tự động ghi nhớ "có một connection đang mở theo chiều này". Response packet về sau được tự động cho qua mà không cần rule riêng.

```
Lambda gọi HTTPS ra ngoài:

  SG outbound rule: allow TCP 443 -> 0.0.0.0/0

  Lambda ---[SYN port 443]-----------> api.stripe.com    PASS (khớp outbound rule)
  Lambda <--[SYN-ACK]---------------- api.stripe.com    PASS (SG nhận ra đây là
  Lambda ---[ACK]------------------->  api.stripe.com          response của connection
  Lambda <--[data]------------------- api.stripe.com          đã được allow)

  Không cần inbound rule nào thêm.
```

**Chỉ cần rule cho chiều initiate. Chiều response tự động được allow.**

---

## 5. NACL — Stateless

NACL **không nhớ gì**. Mỗi packet được evaluate độc lập — NACL không biết packet này là response của một connection đã có hay là connection mới hoàn toàn. Nó chỉ nhìn vào IP và port của packet đó.

```
Lambda gọi HTTPS ra ngoài:

  NACL outbound rule: allow TCP 443 -> 0.0.0.0/0

  Lambda ---[SYN port 443]-----------> api.stripe.com    PASS (khớp outbound rule)
  Lambda <--[SYN-ACK port 52341]----- api.stripe.com    NACL check inbound...
                                                          Không có rule cho port 52341
                                                          -> BLOCK

  Response bị chặn dù outbound đã allow.
```

**Phải tự thêm rule cho cả 2 chiều.**

---

## 6. Ephemeral Ports — Tại sao response dùng port lạ?

Khi client initiate một connection, OS tự chọn một **random port** ở phía client để nhận response về. Port này gọi là **ephemeral port** (cổng tạm thời), thường nằm trong dải **1024–65535**.

```
Lambda (ephemeral port: 52341)  ---port 443--->  api.stripe.com (port 443)
Lambda (ephemeral port: 52341)  <--port 52341--  api.stripe.com (port 443)
                                        ^
                                 Response về đây
```

Port 52341 là random — mỗi connection chọn một port khác nhau. NACL không biết trước port nào sẽ được dùng.

**Giải pháp cho NACL:** Thêm inbound rule allow toàn bộ dải ephemeral ports:

```
NACL Inbound Rule:
  Rule #: 100
  Type: Custom TCP
  Port range: 1024-65535
  Source: 0.0.0.0/0
  Action: ALLOW
```

Rule này cho phép tất cả response traffic về được — dù server dùng ephemeral port nào.

---

## 7. So sánh đầy đủ

| Tiêu chí | Security Group (Stateful) | NACL (Stateless) |
|----------|--------------------------|-----------------|
| Nhớ trạng thái connection | Có | Không |
| Response traffic | Tự động allow | Phải tự thêm rule |
| Cần rule cho chiều nào | Chỉ chiều initiate | Cả 2 chiều |
| Ephemeral ports | Không cần quan tâm | Phải allow 1024-65535 |
| Áp dụng cho | Instance / ENI | Toàn bộ subnet |

---

## 8. Ví dụ thực tế — Lambda kết nối RDS

```
Lambda (private subnet) --> RDS (isolated subnet)

Security Group approach (đơn giản hơn):
  Lambda SG outbound:  allow TCP 5432 -> RDS SG
  RDS SG inbound:      allow TCP 5432 -> Lambda SG
  (Không cần thêm gì — SG tự lo response)

NACL approach (nếu dùng thêm NACL):
  Private subnet NACL outbound:  allow TCP 5432 -> isolated subnet CIDR
  Private subnet NACL inbound:   allow TCP 1024-65535 -> isolated subnet CIDR
  Isolated subnet NACL inbound:  allow TCP 5432 -> private subnet CIDR
  Isolated subnet NACL outbound: allow TCP 1024-65535 -> private subnet CIDR
  (Phải thêm rule cho cả 2 subnet, cả 2 chiều)
```

---

## 9. Khi nào cần quan tâm đến điều này?

**Với Security Group:** Hầu như không cần nghĩ đến — chỉ cần rule cho chiều initiate là đủ.

**Với NACL:** Luôn nhớ thêm rule inbound `TCP 1024-65535` cho bất kỳ subnet nào có outbound traffic ra ngoài. Thiếu rule này là response về bị chặn, connection treo.

**Dấu hiệu nhận biết lỗi do thiếu ephemeral port rule trong NACL:**
- Connection timeout (không phải connection refused)
- Request đi ra được nhưng không nhận được response
- Ping không được nhưng SG đã allow ICMP

---

## Quick Reference

**Q: SG có cần inbound rule để nhận response không?**
A: Không. SG stateful — allow outbound là response tự về được.

**Q: NACL có cần rule cho response không?**
A: Có. NACL stateless — phải thêm inbound rule allow 1024-65535 để response về được.

**Q: Ephemeral port là gì?**
A: Port random phía client dùng để nhận response, nằm trong dải 1024-65535. OS tự chọn mỗi khi tạo connection mới.

**Q: Tại sao không chỉ dùng SG mà không dùng NACL?**
A: SG là primary control, đủ cho hầu hết use case. NACL thêm vào khi cần Deny rule (SG không có Deny), hoặc cần bảo vệ ở subnet level thay vì instance level.

**Q: Nếu NACL block nhưng SG allow thì traffic đi được không?**
A: Không. Traffic phải pass cả 2 lớp — NACL kiểm tra trước (subnet level), SG kiểm tra sau (instance level). Một trong 2 block là traffic bị chặn.
