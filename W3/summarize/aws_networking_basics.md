# AWS Networking Basics — Core Knowledge Summary

> **Mục tiêu W3:** Hiểu đủ để thiết kế VPC 3-tier, đặt đúng subnet, chọn đúng gateway, và trả lời QnA về SGs vs NACLs.

---

## 1. Networking Concepts Cần Nhớ

### IP Addressing
- **CIDR notation**: `10.0.0.0/16` → 65,536 địa chỉ IP. Con số sau `/` càng lớn, dải IP càng nhỏ.
- **Private IP ranges** (RFC 1918 — không route được trên internet):
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`
- AWS **reserve 5 IP đầu** trong mỗi subnet (không dùng được cho EC2/Lambda).

### ENI — Elastic Network Interface
- **ENI là gì:** "Card mạng ảo" trong AWS — điểm kết nối của một resource vào subnet.
- Mỗi ENI có: private IP (từ CIDR subnet), MAC address, và gắn với Security Group(s).
- **EC2** → có ENI → có IP trong subnet → communicate được trong VPC.
- **Lambda trong VPC** → AWS tạo ENI trong subnet → Lambda reach được private resources.
- **Interface Endpoint (PrivateLink)** → tạo ENI với private IP → traffic đến AWS service không ra internet.
- Khi gắn Security Group vào EC2, thực ra bạn đang gắn vào **ENI** của nó (tối đa 5 SG per ENI).

### OSI Model — Chỉ cần nhớ 2 layer quan trọng
| Layer | Tên | AWS liên quan |
|-------|-----|---------------|
| Layer 3 | Network | Route Tables, VPC, CIDR |
| Layer 4 | Transport | Security Groups (TCP/UDP/port) |

---

## 2. Amazon VPC — Virtual Private Cloud

**VPC là gì:** Mạng ảo riêng biệt, isolated hoàn toàn trong AWS cloud. Bạn kiểm soát toàn bộ: IP range, subnets, routing, security.

### Thành phần cốt lõi

```
VPC (10.0.0.0/16)
├── Public Subnet      → có route ra Internet Gateway (2 chiều)
├── Private Subnet     → có route nội bộ + route ra internet qua NAT GW
└── Isolated Subnet    → chỉ có local route (trong VPC), KHÔNG có route ra internet
```

> **Lưu ý quan trọng:** "Isolated" có nghĩa là isolated khỏi **internet**, không phải isolated khỏi VPC. Isolated Subnet vẫn communicate được với các subnet khác trong cùng VPC qua `local` route — RDS vẫn nhận query từ Lambda và trả response về, tất cả đi qua local route.

### VPC 3-Tier Architecture (Must-Have W3)

```
Internet
    │
[Internet Gateway]
    │
┌─────────────────────────────────┐
│  PUBLIC SUBNET (10.0.1.0/24)    │  ← Load Balancer, Bastion Host
│  Route: 0.0.0.0/0 → IGW        │
└─────────────────────────────────┘
    │
┌─────────────────────────────────┐
│  PRIVATE SUBNET (10.0.2.0/24)  │  ← EC2, Lambda, App Server
│  Route: 0.0.0.0/0 → NAT GW     │
└─────────────────────────────────┘
    │
┌─────────────────────────────────┐
│  ISOLATED SUBNET (10.0.3.0/24) │  ← RDS, DynamoDB (VPC Endpoint)
│  Route: local only              │
└─────────────────────────────────┘
```

---

## 3. Gateways — Phân biệt rõ

| Gateway | Dùng cho | Hướng traffic |
|---------|----------|---------------|
| **Internet Gateway (IGW)** | Public subnet → Internet | 2 chiều (inbound + outbound) |
| **NAT Gateway** | Private subnet → Internet (outbound only) | 1 chiều (chỉ outbound) |
| **S3 Gateway Endpoint** | Private subnet → S3 (không qua internet) | Internal AWS network |
| **VPC Peering** | Kết nối 2 VPC với nhau | Private, không qua internet |

> **Key insight:** NAT Gateway đặt ở **public subnet**, nhưng phục vụ **private subnet**. EC2 trong private subnet gửi traffic → NAT GW → IGW → Internet.

### VPC Endpoints — Bức tranh đầy đủ

VPC Endpoint là cơ chế chung cho phép traffic từ trong VPC đến AWS services đi qua **AWS internal network**, không ra internet. Có 3 loại:

| Loại | Dùng cho | Cơ chế | Chi phí |
|------|----------|--------|---------|
| **Gateway Endpoint** | S3, DynamoDB (chỉ 2 service này) | Thêm entry vào Route Table | **Miễn phí** |
| **Interface Endpoint (PrivateLink)** | Hầu hết AWS services còn lại (SQS, SNS, Secrets Manager, ECR, CloudWatch...) | Tạo ENI với private IP trong subnet | **Có phí** (~$0.01/giờ/AZ) |
| **Gateway Load Balancer Endpoint** | Traffic inspection (firewall, IDS/IPS) | Tích hợp với GWLB | Có phí |

### S3 Gateway Endpoint (Quan trọng cho W3)
- Là loại **Gateway Endpoint** — một trong 3 loại VPC Endpoint ở trên.
- Cho phép Lambda/EC2 trong **private subnet** truy cập S3 **mà không cần NAT Gateway**.
- Tiết kiệm chi phí + tăng security (traffic không ra internet).
- Cấu hình: thêm route vào **Route Table** của private subnet → `pl-xxxxxxxx` (prefix list của S3).

**So sánh S3 Gateway Endpoint vs S3 Interface Endpoint:**

| | S3 Gateway Endpoint | S3 Interface Endpoint |
|---|---|---|
| Chi phí | Miễn phí | Có phí |
| Cơ chế | Route table entry | ENI với private IP |
| Dùng qua VPN/Direct Connect | ❌ | ✅ |
| Khi nào dùng | 99% trường hợp trong AWS | Cần access S3 từ on-premises qua Direct Connect |

> **Rule of thumb:** Trong VPC thông thường → luôn dùng **Gateway Endpoint** cho S3 và DynamoDB. Chỉ dùng Interface Endpoint khi có yêu cầu đặc biệt (on-premises, cross-region PrivateLink).

---

## 4. Route Tables

- Mỗi subnet phải associate với 1 route table.
- Route table chứa các rules: "traffic đến đâu thì đi qua gateway nào".

### Destination vs Target
- **Destination:** Dải IP đích của packet — router nhìn vào IP đích để tìm rule khớp.
- **Target:** Gateway/interface mà packet sẽ được forward tới để đến đích đó.

Đọc route table như câu văn: *"Packet đi đến [Destination] → forward qua [Target]"*

### Longest Prefix Match — Rule ưu tiên
Khi nhiều rule cùng khớp, router chọn rule **cụ thể nhất** (prefix dài nhất):
```
Packet đến 10.0.2.5:
  khớp 10.0.0.0/16 (/16) và 0.0.0.0/0 (/0)
  → chọn /16 vì cụ thể hơn → đi qua local

Packet đến 8.8.8.8:
  chỉ khớp 0.0.0.0/0
  → đi qua NAT Gateway
```
> `0.0.0.0/0` luôn là rule cuối cùng — "catch-all", chỉ match khi không có rule nào cụ thể hơn.

### Prefix List
**Prefix List là gì:** Danh sách các IP ranges được đặt tên — thay vì viết từng IP range một, dùng 1 ID đại diện cho tất cả.

**Vấn đề nó giải quyết:** S3 không có 1 IP cố định — AWS vận hành S3 trên hàng trăm IP ranges và có thể thay đổi. Nếu tự viết vào route table phải hàng trăm dòng và tự update khi AWS thêm IP mới.

**AWS Managed Prefix List:** AWS tạo sẵn prefix list cho các service của họ:
- `pl-6fa54006` = tất cả IP ranges của S3 tại `ap-southeast-1`
- AWS tự maintain và update — bạn không cần làm gì

**Dùng ở đâu:**
- Route table: `pl-6fa54006 (S3) → vpce-xxxxxxxx`
- Security Group outbound: allow HTTPS đến `pl-6fa54006` thay vì `0.0.0.0/0`

**So sánh Route Table của 3 loại subnet:**

| | Public Subnet | Private Subnet | Isolated Subnet |
|---|---|---|---|
| Route local (trong VPC) | ✅ | ✅ | ✅ |
| Route ra Internet | ✅ (qua IGW) | ✅ (qua NAT GW) | ❌ |
| Có public IP | ✅ | ❌ | ❌ |
| Dùng cho | ALB, Bastion Host | Lambda, EC2, App Server | RDS, ElastiCache |

**Ví dụ Route Table — Isolated Subnet (DB tier):**

| Destination | Target |
|-------------|--------|
| `10.0.0.0/16` | local |
| *(không có gì thêm)* | — |

**Ví dụ Route Table — Private Subnet có S3 Endpoint:**

| Destination | Target |
|-------------|--------|
| `10.0.0.0/16` | local |
| `0.0.0.0/0` | nat-gateway-id |
| `pl-63a5400a` (S3) | vpce-xxxxxxxx |

---

## 5. Security Groups vs NACLs

> **Câu hỏi QnA hay gặp:** "Khi nào dùng NACL thay SG?"

| Tiêu chí | Security Group (SG) | Network ACL (NACL) |
|----------|--------------------|--------------------|
| **Áp dụng cho** | EC2 instance / ENI | Subnet (toàn bộ subnet) |
| **Stateful/Stateless** | **Stateful** ✅ | **Stateless** ❌ |
| **Rules** | Allow only | Allow + Deny |
| **Thứ tự rules** | Tất cả rules được evaluate | Evaluate theo số thứ tự (thấp → cao), dừng khi match |
| **Default** | Deny all inbound, Allow all outbound | Allow all |

### Inbound vs Outbound Rules
Nhìn từ góc độ của resource được gắn SG:
- **Inbound:** Traffic đi **vào** resource — ai được phép kết nối tới
- **Outbound:** Traffic đi **ra** từ resource — resource được phép gọi đi đâu

```
Nguồn bên ngoài
      │  ← Inbound rule kiểm soát chiều này
      ▼
 [EC2 / Lambda / RDS]
      │  → Outbound rule kiểm soát chiều này
      ▼
Đích bên ngoài
```

**Ví dụ thực tế:**
- RDS SG **inbound**: allow port 3306 từ Lambda SG → Lambda mới query được RDS
- Lambda SG **outbound**: allow port 443 → Lambda mới gọi được HTTPS ra ngoài

### Type trong Security Group Rule
Khi nhập port, AWS tự điền **Type** là tên giao thức phổ biến tương ứng — chỉ là label cho dễ đọc, không có gì magic.

| Type | Protocol | Port | Dùng cho |
|------|----------|------|----------|
| SSH | TCP | 22 | Remote vào Linux server |
| HTTP | TCP | 80 | Web không mã hóa |
| HTTPS | TCP | 443 | Web có mã hóa (TLS) |
| MySQL/Aurora | TCP | 3306 | Kết nối MySQL database |
| PostgreSQL | TCP | 5432 | Kết nối PostgreSQL database |
| DNS (UDP) | UDP | 53 | Phân giải tên miền |
| RDP | TCP | 3389 | Remote vào Windows server |
| All traffic | All | All | Không giới hạn |
| Custom TCP | TCP | (tự nhập) | Port không có tên chuẩn |

> **Quan trọng:** AWS chỉ dùng **Protocol + Port** để enforce rule. Type chỉ để người đọc hiểu nhanh hơn. Rule `Type: HTTPS, Port: 443` hoàn toàn giống `Type: Custom TCP, Port: 443`.

### Stateful vs Stateless — Giải thích đơn giản
- **SG (Stateful):** Bạn allow inbound port 443 → response traffic tự động được allow về. Không cần rule outbound riêng.
- **NACL (Stateless):** Bạn allow inbound port 443 → **phải tự thêm rule outbound** cho ephemeral ports (1024–65535) để response về được.

### Khi nào dùng NACL?
- Cần **block một IP cụ thể** (SG không có Deny rule).
- Cần bảo vệ ở **subnet level** (ví dụ: block toàn bộ subnet khỏi một IP range).
- Defense-in-depth: dùng cả 2 — NACL là lớp ngoài, SG là lớp trong.

---

## 6. AWS Networking Services Overview

| Service | Chức năng |
|---------|-----------|
| **Amazon VPC** | Mạng ảo riêng, nền tảng của mọi thứ |
| **Amazon Route 53** | DNS service, routing policies (latency, failover, weighted) |
| **Amazon CloudFront** | CDN — cache content gần user, giảm latency |
| **AWS Direct Connect** | Kết nối on-premises → AWS qua đường dây vật lý (không qua internet) |
| **AWS VPN** | Kết nối on-premises → AWS qua internet (encrypted tunnel) |
| **Elastic Load Balancing** | Phân phối traffic vào nhiều EC2/Lambda targets |
| **AWS Transit Gateway** | Hub kết nối nhiều VPC + on-premises (thay thế VPC Peering phức tạp) |

---

## 7. Key Takeaways cho W3 Project

1. **Lambda trong private subnet** → cần NAT Gateway để gọi API bên ngoài, hoặc S3 Gateway Endpoint để đọc/ghi S3.
2. **RDS/DynamoDB** → đặt trong isolated subnet, chỉ cho phép traffic từ app subnet qua Security Group.
3. **S3 Gateway Endpoint** phải xuất hiện trên diagram và trong route table — đây là gap từ W2 cần fix.
4. **SG rule cho Lambda → RDS:** inbound RDS SG chỉ allow từ Lambda SG (không allow `0.0.0.0/0`).
5. **Mỗi AZ** nên có public + private subnet riêng để đảm bảo high availability.

---

## Quick Reference — Câu hỏi hay gặp

**Q: Inbound và Outbound rule trong SG là gì?**
A: Nhìn từ góc độ resource được gắn SG — Inbound là traffic đi vào resource (ai được phép kết nối tới), Outbound là traffic đi ra từ resource (resource được phép gọi đi đâu). Ví dụ: RDS SG inbound allow port 3306 từ Lambda SG → Lambda mới query được RDS.

**Q: Type trong SG rule thay đổi theo port nghĩa là gì?**
A: Type chỉ là label tên giao thức phổ biến tương ứng với port — SSH=22, HTTPS=443, MySQL=3306... AWS chỉ dùng Protocol + Port để enforce rule, Type chỉ để người đọc hiểu nhanh. `Type: HTTPS, Port: 443` hoàn toàn giống `Type: Custom TCP, Port: 443`.

**Q: Destination và Target trong Route Table là gì?**
A: Destination là dải IP đích của packet — router dùng để tìm rule khớp. Target là gateway packet sẽ đi qua để đến đích đó. Đọc thành câu: "Packet đến [Destination] → forward qua [Target]". Khi nhiều rule khớp, rule có prefix dài nhất (cụ thể nhất) được ưu tiên — gọi là longest prefix match.

**Q: Prefix List là gì?**
A: Danh sách IP ranges được đặt tên, do AWS quản lý. Ví dụ `pl-6fa54006` đại diện cho tất cả IP ranges của S3 tại ap-southeast-1. Thay vì viết hàng trăm IP range vào route table, chỉ cần 1 entry với prefix list ID. AWS tự update khi IP thay đổi. Dùng được trong cả route table lẫn Security Group rules.

**Q: Isolated Subnet có communicate được trong VPC không?**
A: Có. "Isolated" chỉ có nghĩa là isolated khỏi internet — không có route ra NAT GW hay IGW. Nhưng vẫn có `local` route nên communicate được với các subnet khác trong cùng VPC. RDS trong isolated subnet vẫn nhận query từ Lambda và trả response về bình thường, tất cả đi qua local route.

**Q: Lambda có luôn nằm trong VPC không?**
A: Không. Mặc định Lambda chạy trong AWS-managed network (ngoài VPC của bạn) — có internet access, nhưng không reach được private resources. Chỉ đặt Lambda vào VPC khi cần truy cập RDS, ElastiCache, hoặc EC2 trong private subnet. Trade-off: Lambda trong VPC mất internet access mặc định, muốn ra internet phải có NAT Gateway.

**Q: Tại sao Lambda cần VPC?**
A: Để truy cập RDS trong private subnet. Mặc định Lambda chạy ngoài VPC, không thể reach private resources.

**Q: VPC Endpoint có mấy loại?**
A: 3 loại — Gateway Endpoint (S3, DynamoDB, miễn phí), Interface Endpoint/PrivateLink (hầu hết services còn lại, có phí), và Gateway Load Balancer Endpoint (traffic inspection). Trong W3 project, S3 Gateway Endpoint là loại cần dùng.

**Q: NAT Gateway vs Internet Gateway khác gì?**
A: IGW cho phép 2 chiều (cần public IP). NAT GW chỉ cho outbound từ private subnet (instance không cần public IP).

**Q: S3 Gateway Endpoint có tốn phí không?**
A: Không tốn phí. Ngược lại còn tiết kiệm chi phí NAT Gateway data processing.

**Q: ENI là gì?**
A: Elastic Network Interface — card mạng ảo trong AWS. Mỗi EC2, Lambda trong VPC, hay Interface Endpoint đều có ENI để kết nối vào subnet. Security Group thực ra gắn vào ENI, không phải trực tiếp vào instance — đó là lý do tối đa 5 SG per ENI.

**Q: Có thể có nhiều SG trên 1 instance không?**
A: Có, tối đa 5 SG per ENI. Rules được merge lại — allow từ bất kỳ SG nào là được phép.
