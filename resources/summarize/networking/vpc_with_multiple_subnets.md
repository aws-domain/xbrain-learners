# Configuring and Deploying Amazon VPC with Multiple Subnets

> Source: AWS Documentation — Amazon VPC User Guide

---

## MODULE 1: Amazon VPC Deployment

### Virtual Private Cloud (VPC) là gì?

VPC là một mạng ảo **logically isolated** trong AWS Cloud — bạn toàn quyền kiểm soát không gian IP, subnets, routing, và security.

### Các thành phần cốt lõi khi deploy VPC

**1. CIDR Block**
- Khi tạo VPC, bạn chọn một IPv4 CIDR block (ví dụ: `10.0.0.0/16`)
- CIDR của các VPC khác nhau **không được overlap** nếu cần kết nối với nhau
- Hỗ trợ IPv4-only, IPv6-only, hoặc dual-stack

**2. Subnet**

Subnet là một dải IP con nằm trong VPC. Mỗi subnet phải nằm hoàn toàn trong **một Availability Zone** — không thể span nhiều AZ.

Có 4 loại subnet phân loại theo routing:

| Loại | Đặc điểm |
|------|----------|
| **Public subnet** | Có direct route đến Internet Gateway — resource có thể access internet |
| **Private subnet** | Không có route đến IGW — cần NAT device để ra internet |
| **VPN-only subnet** | Route qua Virtual Private Gateway (Site-to-Site VPN), không có IGW |
| **Isolated subnet** | Không có route ra ngoài VPC — chỉ giao tiếp nội bộ VPC |

> **Lưu ý:** AWS reserved 5 IP đầu tiên trong mỗi subnet (network address, VPC router, DNS, future use, broadcast) — không dùng được cho resource.

**3. Route Table**

Mỗi subnet phải được associate với một route table. Route table quyết định traffic đi đâu:

```
Route table cho Public Subnet:
  10.0.0.0/16  →  local          (traffic nội bộ VPC)
  0.0.0.0/0    →  igw-xxxxxxx    (traffic ra internet)

Route table cho Private Subnet:
  10.0.0.0/16  →  local
  0.0.0.0/0    →  nat-xxxxxxx    (ra internet qua NAT Gateway)
```

**4. Internet Gateway (IGW)**

- Attach vào VPC để cho phép traffic ra/vào internet
- Attach IGW vào VPC chưa đủ — subnet phải có route `0.0.0.0/0 → igw` mới là public subnet

**5. NAT Gateway**

- Đặt trong **public subnet**, dùng Elastic IP
- Cho phép resource trong **private subnet** initiate traffic ra internet, nhưng internet không thể initiate vào

---

## MODULE 2: Securing and Configuring High Availability

### IAM trong VPC Context

IAM kiểm soát **ai được làm gì** với VPC resources:
- Ai được tạo/xóa VPC, subnet, security group
- Ai được modify route table
- Best practice: dùng IAM roles thay vì IAM users cho EC2 instances

### Security Features — Defense in Depth

VPC có 2 lớp bảo mật chính hoạt động song song:

#### Security Groups (Instance level)

- Hoạt động ở **instance level** — gắn vào EC2, RDS, Lambda, v.v.
- Chỉ có **Allow rules** — không có Deny
- **Stateful**: nếu cho phép inbound traffic, response tự động được allow (không cần tạo outbound rule tương ứng)
- Evaluate **tất cả rules** trước khi quyết định

#### Network ACLs — NACLs (Subnet level)

- Hoạt động ở **subnet level** — áp dụng cho tất cả instances trong subnet
- Có cả **Allow và Deny rules**
- **Stateless**: phải explicitly allow cả inbound lẫn outbound (kể cả return traffic)
- Evaluate rules theo **thứ tự số tăng dần** — match rule đầu tiên thì dừng
- Mỗi subnet chỉ associate được với **1 NACL** tại một thời điểm

#### So sánh Security Group vs NACL

| Đặc điểm | Security Group | Network ACL |
|----------|---------------|-------------|
| Cấp độ | Instance | Subnet |
| Rule type | Allow only | Allow + Deny |
| Stateful/Stateless | **Stateful** | **Stateless** |
| Evaluate | Tất cả rules | Theo thứ tự số, dừng khi match |
| Return traffic | Tự động allowed | Phải explicitly allow |

> **AWS khuyến nghị:** Dùng Security Group là primary control. NACL là secondary — dùng để deny một subset traffic cụ thể hoặc làm subnet-level guardrail.

#### Các công cụ bảo mật bổ sung

| Công cụ | Tác dụng |
|---------|----------|
| **VPC Flow Logs** | Monitor IP traffic vào/ra VPC, subnet, hoặc network interface |
| **AWS Network Firewall** | Stateful firewall bảo vệ subnet khỏi network threats |
| **Amazon GuardDuty** | Threat detection — phân tích VPC Flow Logs để phát hiện anomaly |
| **Network Access Analyzer** | Phát hiện unintended network access vào resources |

### Adding High Availability

**Nguyên tắc cốt lõi:** Deploy resources trải đều trên **ít nhất 2 Availability Zones**.

```
Region
├── AZ-1
│   ├── Public Subnet  (10.0.1.0/24)  ← Web servers
│   └── Private Subnet (10.0.2.0/24)  ← DB servers
└── AZ-2
    ├── Public Subnet  (10.0.3.0/24)  ← Web servers (redundant)
    └── Private Subnet (10.0.4.0/24)  ← DB servers (redundant)
```

#### Bản chất của Availability Zone

AZ là **infrastructure vật lý do AWS xây sẵn** — bạn không tự tạo thêm được, chỉ chọn dùng AZ nào. Mỗi Region có **ít nhất 3 AZ**, nhiều Region có 4–6 AZ:

| Region | Số AZ |
|--------|-------|
| us-east-1 (N. Virginia) | 6 |
| us-west-2 (Oregon) | 4 |
| ap-southeast-1 (Singapore) | 3 |
| ap-northeast-1 (Tokyo) | 4 |
| eu-west-1 (Ireland) | 3 |

- Mỗi AZ có independent power, cooling, physical security
- Nếu một AZ fail, AZ còn lại tiếp tục phục vụ traffic
- **Production:** tối thiểu 2 AZ (không nhất thiết phải dùng hết tất cả AZ trong Region)
- **Dev/Test:** có thể dùng 1 AZ để tiết kiệm chi phí
- **Mission-critical:** 3 AZ trở lên

> **Lưu ý chi phí:** Data transfer giữa các AZ trong cùng Region tính phí (~$0.01/GB mỗi chiều). Càng nhiều AZ, traffic cross-AZ càng nhiều — phần lớn workload dùng 2–3 AZ là đủ.

---

## MODULE 3: Multi-Tier Architecture

### Production-Ready: 3-Tier VPC Architecture

Đây là pattern chuẩn cho production workload:

```
Internet
    ↓
[Internet Gateway]
    ↓
┌─────────────────────────────────────────┐
│  PUBLIC SUBNET (AZ-1 + AZ-2)           │
│  - Application Load Balancer            │
│  - NAT Gateway (+ Elastic IP)           │
└─────────────────────────────────────────┘
    ↓ (chỉ traffic từ ALB)
┌─────────────────────────────────────────┐
│  PRIVATE SUBNET - App Tier (AZ-1 + AZ-2)│
│  - EC2 Web/App Servers                  │
│  - Auto Scaling Group                   │
└─────────────────────────────────────────┘
    ↓ (chỉ traffic từ App tier)
┌─────────────────────────────────────────┐
│  PRIVATE SUBNET - DB Tier (AZ-1 + AZ-2) │
│  - RDS Multi-AZ / Aurora                │
│  - ElastiCache                          │
└─────────────────────────────────────────┘
```

### Security Group Chain trong Multi-Tier

Mỗi tier chỉ nhận traffic từ tier ngay trên nó — không expose trực tiếp ra internet:

```
ALB Security Group:
  Inbound:  0.0.0.0/0 → port 80, 443   (từ internet)
  Outbound: sg-webserver → port 80, 443

Web Server Security Group:
  Inbound:  sg-alb → port 80, 443       (chỉ từ ALB)
  Outbound: sg-database → port 3306     (đến DB)

Database Security Group:
  Inbound:  sg-webserver → port 3306    (chỉ từ Web servers)
  Outbound: 0.0.0.0/0 → port 443       (để pull updates)
```

### Route Table cho từng tier

```
Public Subnet Route Table:
  10.0.0.0/16  →  local
  0.0.0.0/0    →  igw-id          ← ra internet trực tiếp

Private Subnet Route Table:
  10.0.0.0/16  →  local
  0.0.0.0/0    →  nat-id          ← ra internet qua NAT
  s3-prefix    →  vpce-s3-id      ← đến S3 qua VPC Endpoint (không qua internet)
```

### VPC Endpoint cho S3

Database servers trong private subnet cần access S3 (backup, logs) mà không muốn traffic đi ra internet:

```
Private Subnet → VPC Gateway Endpoint → S3
                 (traffic ở trong AWS network, không qua internet)
```

---

## Tổng kết — Checklist Production VPC

| Hạng mục | Yêu cầu |
|----------|---------|
| AZ coverage | Tối thiểu 2 AZ |
| Subnet separation | Public (ALB/NAT) + Private App + Private DB |
| Internet access | IGW cho public, NAT Gateway cho private |
| Security | Security Group (primary) + NACL (secondary) |
| Monitoring | VPC Flow Logs bật |
| DB access | Chỉ từ App tier security group |
| AWS service access | VPC Endpoint thay vì qua internet |
| IAM | Least privilege cho mọi resource |
