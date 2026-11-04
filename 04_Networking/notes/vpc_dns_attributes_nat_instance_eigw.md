# VPC DNS attributes, NAT instance (source/dest check, blackhole) và Egress-only IGW

## 📌 Tổng quan cốt lõi (Core Concepts)
*Ba chủ đề nhỏ nhưng hay vào đề: hai tùy chọn DNS của VPC, vì sao NAT instance cần tắt source/destination check, và cách IPv6 đi ra Internet một chiều.*

### 1. DNS resolution và DNS hostnames (hai tùy chọn khác nhau)
- **DNS resolution** (`enableDnsSupport`): bật Amazon DNS resolver (địa chỉ `VPC + 2`, ví dụ `10.20.0.2`). Tắt thì instance **không tra được tên nào**.
- **DNS hostnames** (`enableDnsHostnames`): instance có public IP được cấp **tên DNS** dạng `ec2-54-1-2-3.compute-1.amazonaws.com`. Tắt thì instance vẫn có public IP nhưng **không có tên**.
- Muốn tên hoạt động thì phải bật **cả hai**, vì hostnames dựa trên resolution.
- Từ **trong VPC**, public DNS name phân giải ra **private IP** (traffic đi nội bộ). Từ **Internet**, nó phân giải ra public IP.
- Default VPC bật cả hai. VPC tạo bằng CLI/API có `enableDnsHostnames = false` mặc định.

### 2. NAT instance và Source/Destination check
- Mặc định EC2 bật **source/destination check**: chỉ nhận gói có đích là chính nó và chỉ gửi gói có nguồn là chính nó.
- NAT instance phải **chuyển tiếp gói của máy khác**, nên bắt buộc **tắt** kiểm tra này. Không tắt thì traffic từ private subnet bị timeout.
- NAT instance là một EC2 đơn lẻ: băng thông theo instance type, tự vá OS, tự lo HA. NAT Gateway là dịch vụ managed, tự mở rộng và dư thừa trong AZ.

### 3. Route blackhole
- Khi target của route (NAT instance/gateway, peering, ENI...) bị xóa, route **vẫn còn** trong route table với trạng thái **Blackhole**.
- Traffic đi vào route đó bị **bỏ âm thầm**, không có thông báo lỗi. Triệu chứng: private instance đột nhiên mất Internet.
- AWS **không tự sửa** route table. Phải sửa tay từng route table liên quan.

### 4. Egress-only Internet Gateway (IPv6)
- IPv6 không có địa chỉ private, nên **không cần NAT**. Vấn đề còn lại là cho **đi ra** nhưng **chặn kết nối từ ngoài vào**: đó là việc của egress-only IGW.
- Route: `::/0 → eigw-...`. Chỉ dùng cho IPv6.

---

## 📐 Sơ đồ Hoạt động (Architectural Flows)

### NAT instance với source/dest check
```
cap-tmp-app (10.20.11.20) ──► NAT instance (public subnet, public IP)
                               │  ip_forward=1 + MASQUERADE: đổi nguồn thành IP của NAT instance
                               │  Source/dest check ON  → từ chối chuyển tiếp (gói có đích không phải nó) → TIMEOUT
                               │  Source/dest check OFF → chuyển tiếp được
                               ▼
                             IGW ──► Internet (thấy IP của NAT instance)
```

### Blackhole
```
Route table private: 0.0.0.0/0 → i-xxxx (NAT instance)
   terminate i-xxxx
Route table private: 0.0.0.0/0 → i-xxxx   [Status: Blackhole]   gói tin vào là mất, không lỗi
   sửa: đổi Target về NAT Gateway còn sống
```

### Tên DNS của EC2
```
Hỏi ec2-54-1-2-3...amazonaws.com
   từ trong VPC  → 10.20.1.10 (private IP)
   từ Internet   → 54.1.2.3  (public IP)
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

### DNS attributes
| Tiêu chí | DNS resolution | DNS hostnames |
|---|---|---|
| Tên API | `enableDnsSupport` | `enableDnsHostnames` |
| Hình dung | Có danh bạ để tra | Được ghi tên vào danh bạ |
| Tắt thì | Không tra được tên nào | Có public IP nhưng không có public DNS name |
| Phụ thuộc | Độc lập | Cần resolution bật |

Cần **cả hai bật** cho: RDS public endpoint phân giải từ Internet, interface VPC endpoint dùng **private DNS**, Route 53 private hosted zone gắn vào VPC.

### NAT Gateway vs NAT instance vs Egress-only IGW
| Tiêu chí | NAT Gateway | NAT instance | Egress-only IGW |
|---|---|---|---|
| Dành cho | IPv4 | IPv4 | **IPv6** |
| Route | `0.0.0.0/0` | `0.0.0.0/0` | `::/0` |
| Managed | Có, tự mở rộng | Không, tự vá/HA | Có |
| Source/dest check | Không liên quan | **Phải tắt** | Không liên quan |
| Cho ra, chặn vào | ✅ | ✅ | ✅ |
| Đổi địa chỉ | Có (many-to-1) | Có (MASQUERADE) | Không |

---

## 🛠️ Cấu hình NAT instance trên Amazon Linux 2023

AMI NAT dựng sẵn `amzn-ami-vpc-nat` dựa trên Amazon Linux AMI 2018.03 đã hết hỗ trợ, nên tự cấu hình trên AL2023 (User data):

```bash
#!/bin/bash
dnf install -y iptables-services
systemctl enable --now iptables
echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/custom-ip-forwarding.conf
sysctl -p /etc/sysctl.d/custom-ip-forwarding.conf
IFACE=$(ip route | awk '/default/ {print $5; exit}')
iptables -t nat -A POSTROUTING -o "$IFACE" -j MASQUERADE
iptables -F FORWARD
service iptables save
```

Các bước còn lại: đặt ở **public subnet** có public IP, SG cho inbound từ dải VPC, **Actions > Networking > Change source/destination check > Stop**, rồi đổi `0.0.0.0/0` của route table private sang `Instance`.

## ⚠️ Những điểm hay ra đề / dễ nhầm
- "NAT instance không hoạt động" → **source/destination check chưa tắt**.
- "Instance có public IP nhưng không có public DNS name" → bật **DNS hostnames**.
- "Private instance đột nhiên mất Internet, route table hiển thị Blackhole" → target đã bị xóa, trỏ route sang NAT còn sống.
- "IPv6 chỉ cho outbound" → **egress-only IGW**. "IPv4 chỉ cho outbound" → NAT Gateway.
- NAT Gateway cần ở **public subnet**; NAT instance cũng vậy.
- Gộp nhiều NAT Gateway về một thì phải sửa route table của **từng** private subnet.

## 🔗 Liên quan
- Route và public IP, IGW vs NAT: [public_ip_vs_route_igw_nat_flow.md](./public_ip_vs_route_igw_nat_flow.md)
- Bảng IGW, NAT, Peering, VPN, TGW: [aws_networking_gateways.md](./aws_networking_gateways.md)
- NAT instance làm workaround Free Tier (workshop): [phase5-alternatives.md](../practice/conduit-aws-networking/phase5-alternatives.md)
- Nguồn thực hành: capstone `cap1-1` (Phần 2, 10, 11) trong `aws-certification/soa-co3/capstones/cap1-web-platform/ch1-vpc-network`
