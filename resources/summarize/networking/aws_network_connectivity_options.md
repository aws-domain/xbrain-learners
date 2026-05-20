# AWS Network Connectivity Options

> Source: AWS Documentation — VPC User Guide, Transit Gateway Guide, Site-to-Site VPN Guide, AWS PrivateLink

---

## MODULE 1: Understanding Connectivity Concepts

### Tại sao cần nhiều connectivity options?

Không có một giải pháp nào phù hợp cho mọi tình huống. AWS cung cấp nhiều lựa chọn vì mỗi use case có yêu cầu khác nhau về:

| Tiêu chí | Ảnh hưởng đến lựa chọn |
|----------|------------------------|
| **Latency** | VPN qua internet vs Direct Connect vật lý |
| **Bandwidth** | VPN ~1.25 Gbps/tunnel vs Direct Connect 1–100 Gbps |
| **Security** | Traffic có đi qua internet không? |
| **Cost** | Setup cost vs ongoing cost |
| **Scale** | 2 VPC vs hàng trăm VPC |
| **Direction** | User → AWS (Client VPN) vs Site → AWS (Site-to-Site VPN) |

### Phân loại connectivity

```
Connectivity trong AWS:
  VPC ↔ VPC          → VPC Peering, Transit Gateway
  VPC ↔ AWS Services → VPC Endpoints, PrivateLink

Connectivity Hybrid (On-premises ↔ AWS):
  Network ↔ AWS      → Site-to-Site VPN, Direct Connect
  User ↔ AWS         → Client VPN
```

---

## MODULE 2: AWS Network Service Offerings

### 1. VPC Endpoints và AWS PrivateLink

VPC Endpoint cho phép traffic từ trong VPC đến AWS services đi qua **AWS internal network** — không ra internet.

#### 3 loại VPC Endpoint

| Loại | Dùng cho | Cơ chế | Chi phí |
|------|----------|--------|---------|
| **Gateway Endpoint** | S3, DynamoDB (chỉ 2 service) | Thêm entry vào Route Table | **Miễn phí** |
| **Interface Endpoint (PrivateLink)** | Hầu hết AWS services còn lại | Tạo ENI với private IP trong subnet | ~$0.01/giờ/AZ |
| **Gateway Load Balancer Endpoint** | Traffic inspection (firewall, IDS/IPS) | Tích hợp với GWLB | Có phí |

#### AWS PrivateLink — Cơ chế hoạt động

PrivateLink là công nghệ nền tảng của Interface Endpoint. Nó cho phép:
- **Consumer VPC** kết nối đến **Provider service** qua private IP
- Traffic không bao giờ rời khỏi AWS network
- Provider có thể là: AWS service, AWS Partner, hoặc service của chính bạn (cross-account)

```
Consumer VPC                    Provider
┌──────────────────┐           ┌──────────────────┐
│  EC2 / Lambda    │           │  Service (NLB)   │
│       ↓          │           │       ↑          │
│  Interface       │──private──│  Endpoint        │
│  Endpoint (ENI)  │  network  │  Service         │
└──────────────────┘           └──────────────────┘
```

**Khi nào dùng PrivateLink thay vì public endpoint:**
- Compliance yêu cầu traffic không ra internet
- Muốn expose service của mình cho account khác mà không cần VPC Peering
- Cần access S3 từ on-premises qua Direct Connect (dùng S3 Interface Endpoint)

---

### 2. VPC Peering

Kết nối **2 VPC** với nhau — traffic đi qua AWS private network, không qua internet.

**Đặc điểm quan trọng:**
- Có thể peering cùng account, khác account, hoặc khác Region
- **Không transitive:** A↔B, B↔C → A **không** tự động reach C
- CIDR của 2 VPC **không được overlap**
- Phải thêm route vào route table của cả 2 VPC sau khi tạo peering

```
VPC A ←→ VPC B ←→ VPC C
VPC A KHÔNG reach được VPC C (phải tạo peering A↔C riêng)
```

**Khi nào dùng:** 2–3 VPC, kết nối đơn giản, ít thay đổi. Nhiều VPC → dùng Transit Gateway.

---

### 3. AWS Direct Connect

Kết nối on-premises → AWS qua **đường dây vật lý riêng** — không qua internet.

**Thông số:**
- Bandwidth: 1 Gbps, 10 Gbps, 100 Gbps (hoặc sub-1G qua hosted connection)
- Latency thấp, ổn định — không bị ảnh hưởng bởi internet congestion
- Setup time: tuần đến tháng

**Resiliency levels:**
| SLA | Cách đạt được |
|-----|---------------|
| **99.99%** (Maximum) | Nhiều connections, nhiều on-premises locations, nhiều DX locations |
| **99.9%** (High) | 2 connections đến nhiều locations |
| **< 99.9%** | 1 connection duy nhất — single point of failure |

**Direct Connect Gateway:**
- Cho phép **1 Direct Connect connection** reach nhiều VPC ở nhiều Region
- Không cần tạo VGW riêng cho từng VPC

```
On-Premises → [DX Location] → [Direct Connect Gateway] → VPC-1 (us-east-1)
                                                        → VPC-2 (ap-southeast-1)
                                                        → VPC-3 (eu-west-1)
```

---

### 4. AWS Site-to-Site VPN và AWS Client VPN

#### Site-to-Site VPN — Network to AWS

Kết nối **toàn bộ on-premises network** → AWS qua internet (encrypted IPSec tunnel).

**Thành phần:**
- **Virtual Private Gateway (VGW):** AWS-side endpoint, gắn vào 1 VPC
- **Transit Gateway:** AWS-side endpoint, kết nối nhiều VPC (khuyến nghị cho multi-VPC)
- **Customer Gateway (CGW):** AWS resource đại diện cho thiết bị on-premises
- **Customer Gateway Device:** Thiết bị vật lý/software thực tế ở on-premises

**Mỗi VPN connection có 2 tunnels** — active/passive, đảm bảo HA.

**Bandwidth:**
- Standard: **1.25 Gbps** per tunnel
- Large Bandwidth Tunnel (chỉ với TGW): **5 Gbps** per tunnel
- ECMP với TGW: aggregate nhiều tunnels → tối đa **50 Gbps** (cần BGP dynamic routing)

**Accelerated VPN:**
- Dùng **AWS Global Accelerator** để route traffic qua AWS edge location gần nhất
- Tránh internet congestion, giảm latency
- Chỉ hỗ trợ khi attach vào Transit Gateway

#### Client VPN — User to AWS

Kết nối **từng user cá nhân** → AWS từ bất kỳ đâu qua OpenVPN client.

**Đặc điểm:**
- Managed service — AWS lo scale, HA tự động
- Authentication: Active Directory, federated (SAML), certificate-based
- Có thể attach vào VPC subnet hoặc Transit Gateway
- Granular access control theo AD group

**So sánh Site-to-Site VPN vs Client VPN:**

| | Site-to-Site VPN | Client VPN |
|---|---|---|
| Kết nối từ | Toàn bộ network/site | Từng user cá nhân |
| Use case | Office → AWS, DC → AWS | Remote worker → AWS |
| Protocol | IPSec | OpenVPN (TLS) |
| Endpoint AWS side | VGW hoặc TGW | Client VPN Endpoint |
| Scale | Per-site | Per-user |

---

### 5. AWS Transit Gateway

Hub trung tâm kết nối nhiều VPC và on-premises networks — thay thế VPC Peering mesh phức tạp.

**Vấn đề VPC Peering giải quyết không được:**
```
5 VPC cần full mesh = 10 peering connections
10 VPC = 45 connections
→ Không scale được, không transitive
```

**TGW giải quyết:**
```
VPC A ─┐
VPC B ─┤
VPC C ─┼─→ [Transit Gateway] ←─ VPN / Direct Connect → On-Premises
VPC D ─┤
VPC E ─┘
→ Chỉ cần 5 attachments, TGW lo routing
```

**Attachment types:**

| Loại | Dùng cho |
|------|----------|
| VPC attachment | Kết nối VPC vào TGW |
| VPN attachment | Site-to-Site VPN |
| Direct Connect Gateway attachment | Direct Connect |
| Connect attachment | SD-WAN / GRE tunnel (tối đa 20 Gbps/attachment) |
| Peering attachment | Kết nối 2 TGW với nhau (cross-region) |
| Client VPN attachment | Client VPN endpoint |

**TGW Route Tables — Association vs Propagation:**
- **Association:** Attachment dùng route table nào để lookup khi forward traffic (mỗi attachment chỉ associate với 1 route table)
- **Propagation:** Attachment tự động thêm routes của nó vào route table nào (1 attachment có thể propagate vào nhiều route tables)

**MTU:**
- VPC, Direct Connect, Connect, Peering: **8500 bytes**
- VPN: **1500 bytes**

**Best practices (từ AWS Docs):**
- Không cần nhiều TGW cho HA — TGW highly available by design
- Dùng **1 TGW per Region** cho disaster recovery
- Dùng BGP Site-to-Site VPN thay vì static routing
- Dùng unique ASN cho mỗi TGW khi có nhiều TGW
- Tạo subnet riêng `/28` cho TGW attachment trong mỗi VPC

---

## MODULE 3: Design Patterns

### Pattern 1: Simplifying Multi-VPC Routing

**Vấn đề:** Nhiều VPC cần communicate với nhau + on-premises.

**Giải pháp: Hub-and-Spoke với TGW**

```
                    ┌─────────────────────────────┐
                    │      Transit Gateway         │
                    │   (hub trung tâm)            │
                    └──┬──────┬──────┬──────┬──────┘
                       │      │      │      │
                    VPC-A  VPC-B  VPC-C  VPN/DX
                   (prod) (dev) (shared) (on-prem)
```

**Isolation với nhiều Route Tables:**

Khi không muốn tất cả VPC reach nhau (ví dụ: dev không được reach prod):

```
Route Table "prod":
  - Associate: VPC-prod attachment
  - Propagate from: VPC-shared, VPN

Route Table "dev":
  - Associate: VPC-dev attachment
  - Propagate from: VPC-shared (không có VPN, không có prod)
```

---

### Pattern 2: Resilient Hybrid Networks

**Mục tiêu:** Không có single point of failure trong kết nối on-premises ↔ AWS.

**Tier 1 — Maximum Resiliency (99.99% SLA):**
```
On-Premises Location 1 ──DX──→ DX Location A ─┐
On-Premises Location 2 ──DX──→ DX Location B ─┴→ Transit Gateway → VPCs
```
2 on-premises locations + 2 DX locations + 2 connections mỗi location.

**Tier 2 — High Resiliency (99.9% SLA):**
```
On-Premises ──DX──→ DX Location A ─┐
            ──DX──→ DX Location B ─┴→ Transit Gateway → VPCs
```
2 DX connections đến 2 locations khác nhau.

**Tier 3 — VPN as backup cho Direct Connect:**
```
Primary:  On-Premises ──Direct Connect──→ Transit Gateway
Backup:   On-Premises ──Site-to-Site VPN──→ Transit Gateway
```
BGP routing tự động failover sang VPN khi DX down. ECMP cho phép dùng cả 2 đồng thời.

**Anti-patterns cần tránh:**
- Chỉ dùng 1 VPN tunnel (single point of failure)
- Nhiều tunnels nhưng cùng kết thúc ở 1 AZ
- Chỉ dùng 1 ISP cho VPN connectivity
- Không dùng BGP dynamic routing

---

### Pattern 3: Regional High Availability

**Mục tiêu:** Workload trong 1 Region vẫn hoạt động khi 1 AZ fail.

```
Region
├── AZ-1: TGW subnet + workload subnet
├── AZ-2: TGW subnet + workload subnet
└── AZ-3: TGW subnet + workload subnet (optional, mission-critical)
```

**Best practice:**
- Mỗi VPC attachment vào TGW nên có subnet ở **ít nhất 2 AZ**
- TGW tự highly available — không cần deploy thêm
- Dùng subnet `/28` riêng cho TGW attachment (không dùng chung với workload)

---

### Pattern 4: AWS Transit Gateway Peering (Cross-Region)

Kết nối 2 TGW ở **khác Region** — traffic đi qua AWS backbone, không qua internet, tự động encrypted.

```
Region A                          Region B
[TGW-A] ←── TGW Peering ──→ [TGW-B]
  │                                │
VPC-A1, VPC-A2               VPC-B1, VPC-B2
On-Premises-A                On-Premises-B
```

**Lưu ý quan trọng:**
- Phải tạo **static routes** thủ công (không có route propagation qua TGW peering)
- CIDR của các VPC ở 2 Region không được overlap
- Dùng unique ASN cho mỗi TGW

---

## Tổng hợp — Khi nào dùng gì

### Connectivity trong AWS

| Nhu cầu | Giải pháp |
|---------|-----------|
| 2–3 VPC kết nối đơn giản | VPC Peering |
| Nhiều VPC, hub trung tâm | Transit Gateway |
| VPC → AWS services (không qua internet) | VPC Endpoint (Gateway hoặc Interface) |
| Expose service cho account khác | AWS PrivateLink (Interface Endpoint) |

### Connectivity Hybrid

| Nhu cầu | Giải pháp |
|---------|-----------|
| Nhanh, rẻ, bandwidth thấp | Site-to-Site VPN + VGW |
| Multi-VPC + VPN | Site-to-Site VPN + TGW |
| Production, latency thấp, bandwidth lớn | Direct Connect |
| 1 DX → nhiều VPC/Region | Direct Connect Gateway |
| Remote user → AWS | Client VPN |
| Tối đa resiliency | DX (primary) + VPN (backup) + BGP |
| Cross-region multi-site | TGW Peering |

### Decision Tree nhanh

```
Cần kết nối on-premises?
  ├── Từng user cá nhân → Client VPN
  └── Toàn bộ network/site
        ├── Cần latency thấp, bandwidth lớn → Direct Connect
        └── Cần nhanh, budget thấp → Site-to-Site VPN
              └── Kết nối nhiều VPC? → Attach vào TGW (không phải VGW)

Cần kết nối VPC với VPC?
  ├── 2–3 VPC đơn giản → VPC Peering
  └── Nhiều VPC → Transit Gateway

Cần VPC access AWS services?
  ├── S3 hoặc DynamoDB → Gateway Endpoint (miễn phí)
  └── Services khác → Interface Endpoint (PrivateLink)
```
