# Public IP vs Route: Vì sao ra được Internet — IGW và NAT Gateway hoạt động thế nào

## 📌 Tổng quan cốt lõi (Core Concepts)
*Một instance ra Internet được cần **cả hai** điều kiện: có **đường đi** (route) và có **địa chỉ public** để Internet trả lời về. Hai thứ này do hai cơ chế khác nhau quyết định.*
- **Route table** quyết định **đường đi**. Subnet có route `0.0.0.0/0 → IGW` thì gọi là *public subnet*. Chỉ có vậy: "public subnet" không tự cấp IP cho ai.
- **Public IPv4** quyết định instance có **địa chỉ để Internet trả lời về** hay không. Đây là cài đặt riêng: bật lúc launch (`Auto-assign public IP`), bật mặc định ở subnet (`Enable auto-assign public IPv4 address`), hoặc gắn **Elastic IP**.
- **Bên trong VPC, instance chỉ biết private IP.** Chạy `ip addr` chỉ thấy `10.x.x.x`. Public IP được map ở **IGW**, không nằm trên card mạng của instance.
- **IGW dịch địa chỉ 1-1:** mỗi instance cần một public IP riêng. Instance không có public IP thì IGW không có gì để dịch, gói tin bị bỏ dù route đúng.
- **NAT Gateway dịch nhiều-1:** nhiều instance private dùng chung **một** Elastic IP của NAT. NAT chỉ trả lời các kết nối do instance bên trong **chủ động mở ra** (outbound-only).

---

## 📐 Sơ đồ Hoạt động (Architectural Flows)

### 1. Instance trong public subnet (có public IP)

```
 EC2 web (private 10.20.1.10, public IP 54.1.2.3)
        │  gói tin: nguồn 10.20.1.10
        ▼
 Route table public: 0.0.0.0/0 → IGW
        ▼
 IGW: tra "10.20.1.10 ↔ 54.1.2.3" → đổi nguồn thành 54.1.2.3
        ▼
 Internet ──► trả lời về 54.1.2.3 ──► IGW đổi lại 10.20.1.10 ──► EC2
```

### 2. Instance trong private subnet (không có public IP, ra qua NAT)

```
 EC2 app (private 10.20.11.20, KHÔNG có public IP)
        │  Route table private: 0.0.0.0/0 → NAT GW
        ▼
 NAT GW (nằm ở PUBLIC subnet, có Elastic IP 3.4.5.6)
        │  đổi nguồn 10.20.11.20 → 3.4.5.6, ghi nhớ kết nối này
        │  Route table public: 0.0.0.0/0 → IGW
        ▼
 IGW ──► Internet (chỉ thấy 3.4.5.6)
        ▼
 Trả lời về 3.4.5.6 ──► NAT tra bảng ghi nhớ ──► chuyển về 10.20.11.20
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | EC2 trong **public** subnet | EC2 trong **private** subnet + NAT |
|---|---|---|
| Public IP nằm ở | Chính instance (auto-assign hoặc EIP) | NAT Gateway (Elastic IP) |
| Route `0.0.0.0/0` trỏ tới | Internet Gateway | NAT Gateway |
| Dịch địa chỉ | 1-1 tại IGW | Nhiều-1 tại NAT |
| Ra Internet (outbound) | ✅ | ✅ |
| Internet chủ động kết nối vào | ✅ nếu SG/NACL cho phép | ❌ |
| Dùng cho | Web server, bastion, NAT GW, ALB | App server, DB, cần tải bản vá |

### Subnet default VPC vs subnet tự tạo
| Tiêu chí | Default VPC | VPC/subnet tự tạo |
|---|---|---|
| Auto-assign public IPv4 | Bật sẵn | **Tắt** mặc định |
| Hệ quả | Launch EC2 là tự có public IP | Chỉ route tới IGW vẫn không đủ, phải bật auto-assign hoặc gắn EIP |

Bật auto-assign ở subnet chỉ là **mặc định cho tiện**. Có thể ghi đè từng instance lúc launch (`Network settings > Edit > Auto-assign public IP`).

---

## 🛠️ Checklist: instance trong public subnet vẫn không truy cập được từ Internet
1. Route table của subnet có `0.0.0.0/0 → igw-...` chưa?
2. Instance có **public IPv4 hoặc Elastic IP** chưa? *(lỗi hay gặp nhất khi tự tạo subnet)*
3. Security group có cho inbound đúng port từ nguồn đúng chưa?
4. NACL của subnet có cho cả inbound lẫn **ephemeral ports** (1024-65535) chiều trả về chưa?
5. Trong instance, dịch vụ có đang listen và firewall OS có mở port không?

## ⚠️ Những điểm hay ra đề / dễ nhầm
- "Public subnet" = **có route tới IGW**. Không liên quan trực tiếp tới việc instance có public IP.
- **NAT Gateway phải nằm trong public subnet** (cần route tới IGW và có EIP). Đặt NAT trong private subnet là sai.
- NAT Gateway **chỉ outbound**. Muốn nhận traffic từ Internet vào thì cần public IP hoặc ALB.
- IPv6 không có NAT: dùng **egress-only Internet Gateway** để cho outbound-only.
- Mỗi public IPv4 tính phí (khoảng 0.005 USD/giờ, kể cả khi đang gắn vào instance), nên terminate instance tạm và release EIP không dùng.
- Public IP auto-assign **đổi khi stop/start**; muốn cố định phải dùng Elastic IP (xem [elastic_ip_and_prefix_list.md](./elastic_ip_and_prefix_list.md)).

## 🔗 Liên quan
- Bảng IGW, NAT, Peering, VPN, TGW: [aws_networking_gateways.md](./aws_networking_gateways.md)
- Thiết kế VPC nhiều subnet: [vpc_with_multiple_subnets.md](./vpc_with_multiple_subnets.md)
- Nguồn thực hành: capstone `cap1-1` (Mạng VPC) trong `aws-certification/soa-co3/capstones/cap1-web-platform/ch1-vpc-network`
