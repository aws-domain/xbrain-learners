# Elastic IP và Prefix List

## Elastic IP

Bình thường khi start/stop một EC2 instance, **public IP thay đổi mỗi lần**. Elastic IP (EIP) là một public IP tĩnh mà bạn "sở hữu" — không đổi dù instance restart hay thay thế.

```
Không có EIP:
  EC2 start lần 1  →  public IP: 54.23.11.5
  EC2 stop/start   →  public IP: 18.67.44.2  ← đổi rồi

Có EIP:
  EC2 start lần 1  →  public IP: 52.10.0.1   (EIP)
  EC2 stop/start   →  public IP: 52.10.0.1   ← không đổi
```

### Tại sao cần?

- DNS trỏ vào IP cố định — nếu IP đổi thì domain hỏng
- Đối tác/khách hàng whitelist IP trong firewall của họ — IP đổi là bị chặn
- NAT Gateway bắt buộc phải dùng EIP

### Vòng đời của EIP

```
Allocate EIP  →  52.10.0.1 (bạn đang giữ IP này)
Associate     →  gắn vào EC2 instance hoặc NAT Gateway
Disassociate  →  tháo ra, IP vẫn thuộc về bạn
Release       →  trả lại cho AWS
```

### Billing

- **Miễn phí** khi đang gắn vào một running instance
- **Tính phí** nếu allocate mà không gắn vào đâu — vì bạn đang giữ IP mà không dùng

---

## Prefix List

Prefix List là một **danh sách các CIDR được đặt tên** — dùng để tái sử dụng thay vì lặp lại CIDR ở nhiều chỗ.

### Vấn đề nó giải quyết

Giả sử công ty có 5 văn phòng, mỗi văn phòng một dải IP, cần cho phép tất cả vào hệ thống:

```
Không có Prefix List — phải lặp lại ở mỗi Security Group:
  SG-WebServer:  allow 203.0.113.0/24, 198.51.100.0/24, 192.0.2.0/24 ...
  SG-Database:   allow 203.0.113.0/24, 198.51.100.0/24, 192.0.2.0/24 ...
  SG-AppServer:  allow 203.0.113.0/24, 198.51.100.0/24, 192.0.2.0/24 ...
  → Thêm văn phòng mới: phải vào từng SG sửa, dễ bỏ sót
```

```
Có Prefix List:
  Tạo "pl-company-offices" = [203.0.113.0/24, 198.51.100.0/24, 192.0.2.0/24]

  SG-WebServer:  allow pl-company-offices
  SG-Database:   allow pl-company-offices
  SG-AppServer:  allow pl-company-offices
  → Thêm văn phòng mới: chỉ sửa Prefix List một chỗ, tất cả SG tự cập nhật
```

### Hai loại Prefix List

| | Customer-managed | AWS-managed |
|---|---|---|
| Ai tạo | Bạn tự tạo | AWS tạo sẵn |
| Ví dụ | danh sách IP văn phòng | `com.amazonaws.us-east-1.s3` |
| Dùng ở đâu | SG, NACL, Route Table | Route Table (VPC Endpoint routing) |

AWS-managed Prefix List đặc biệt hữu ích khi route traffic đến S3 hoặc DynamoDB qua VPC Endpoint — thay vì phải biết hết dải IP của S3, chỉ cần reference prefix list của AWS.

---

## Mối liên hệ với CIDR

```
CIDR        →  ngôn ngữ nền tảng để biểu diễn dải IP
Elastic IP  →  giải quyết vấn đề IP động của resource
Prefix List →  giải quyết vấn đề quản lý nhiều CIDR lặp lại
```
