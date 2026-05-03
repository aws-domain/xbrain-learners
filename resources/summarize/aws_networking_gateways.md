# AWS Networking Gateways — Core Knowledge Summary

> **Source:** AWS Course — "Understanding AWS Networking Gateways"
> **Mục tiêu:** Hiểu rõ các loại gateway trong AWS, khi nào dùng cái nào, và cách chúng kết nối với nhau.

---

## 1. Amazon VPC — Nền Tảng

### Subnets và Availability Zones
- Mỗi subnet nằm trong **1 AZ duy nhất** — không span nhiều AZ.
- Để high availability: tạo subnet ở **nhiều AZ**, mỗi AZ có public + private subnet riêng.
- Traffic giữa các subnet trong cùng VPC đi qua **local route** — không cần gateway.

**Bản chất AZ:** AZ là infrastructure vật lý do AWS xây sẵn — không tự tạo thêm được, chỉ chọn dùng. Mỗi Region có **ít nhất 3 AZ** (thường 3–6). "Tối thiểu 2 AZ" là lời khuyên về deployment, không phải giới hạn kỹ thuật. Data transfer cross-AZ tính phí (~$0.01/GB) nên thực tế phần lớn workload dùng 2–3 AZ.

### Route Tables — 2 loại traffic
| Traffic | Route cần có |
|---------|-------------|
| Internal VPC (giữa các subnet) | `10.0.0.0/16 → local` (tự động có) |
| Internet traffic | `0.0.0.0/0 → IGW hoặc NAT GW` (phải tự thêm) |

---

## 2. Internet Gateway (IGW)

- Cho phép traffic **2 chiều** giữa VPC và internet.
- Gắn vào **VPC** (không phải subnet) — 1 VPC chỉ có 1 IGW.
- Subnet có route `0.0.0.0/0 → IGW` = **public subnet**.
- Resource trong public subnet cần **public IP hoặc Elastic IP** để nhận inbound traffic từ internet.

### Ingress Routing
- Cho phép route **inbound traffic từ internet** đến một appliance (firewall, IDS) trước khi vào EC2.
- Cấu hình: thêm route vào **edge route table** của IGW — traffic đến IP cụ thể sẽ đi qua appliance trước.

---

## 3. Public vs Private Subnet

| | Public Subnet | Private Subnet |
|---|---|---|
| Route internet | `0.0.0.0/0 → IGW` | `0.0.0.0/0 → NAT GW` |
| Có public IP | ✅ | ❌ |
| Inbound từ internet | ✅ (nếu SG cho phép) | ❌ |
| Outbound ra internet | ✅ | ✅ (qua NAT GW) |

---

## 4. NAT Gateway

- Cho phép resource trong **private subnet** gọi ra internet — **outbound only**.
- Inbound từ internet không thể initiate connection vào private subnet qua NAT GW.
- **Đặt ở public subnet** — cần IGW để forward traffic ra internet.
- Có **Elastic IP** (public IP cố định).
- Managed service — AWS lo scale và availability.

```
Private Subnet → NAT GW (public subnet) → IGW → Internet
```

> **Chi phí:** ~$0.045/giờ + $0.045/GB data — xóa ngay khi không dùng.

---

## 5. VPC Peering

- Kết nối **2 VPC** với nhau — traffic đi qua AWS private network, không qua internet.
- Có thể peering giữa VPC trong cùng account, khác account, hoặc khác Region.
- **Không transitive:** A peer B, B peer C → A **không** tự động reach C.

```
VPC A ←→ VPC B ←→ VPC C
VPC A KHÔNG reach được VPC C trực tiếp
```

- Cần thêm route vào route table của cả 2 VPC sau khi tạo peering.
- **Khi nào dùng:** Số lượng VPC ít (2–3), kết nối đơn giản. Nhiều VPC → dùng Transit Gateway.

---

## 6. Hybrid Connectivity — Kết Nối On-Premises

### Virtual Private Gateway (VGW)
- Là **AWS-side endpoint** cho kết nối hybrid (VPN hoặc Direct Connect).
- Gắn vào **VPC** — 1 VPC chỉ có 1 VGW.
- Hỗ trợ **route propagation** — tự động thêm on-premises routes vào route table của VPC.

### AWS Site-to-Site VPN
- Kết nối on-premises → AWS qua **internet** (encrypted IPSec tunnel).
- Cần 2 thành phần:
  - **Virtual Private Gateway (VGW):** AWS side
  - **Customer Gateway (CGW):** On-premises side (router/firewall vật lý hoặc software)
- Tạo **2 tunnels** cho redundancy (active/passive).
- Bandwidth: tối đa ~1.25 Gbps per tunnel.

```
On-Premises                    AWS
[Customer Gateway] ←VPN→ [Virtual Private Gateway] → VPC
```

### Customer Gateway (CGW)
- Là **AWS resource** đại diện cho thiết bị on-premises của bạn.
- Chứa thông tin: public IP của thiết bị on-premises, BGP ASN (nếu dùng dynamic routing).
- Không phải thiết bị vật lý — chỉ là config trong AWS.

### AWS Direct Connect
- Kết nối on-premises → AWS qua **đường dây vật lý riêng** — không qua internet.
- Băng thông: 1 Gbps, 10 Gbps, 100 Gbps (hoặc sub-1G qua hosted connection).
- Latency thấp hơn, ổn định hơn VPN — nhưng tốn thời gian setup (tuần đến tháng).
- Cần **Direct Connect Gateway** để kết nối vào nhiều VPC hoặc nhiều Region.

```
On-Premises → [Direct Connect Location] → AWS backbone → VPC
```

### So sánh VPN vs Direct Connect

| | Site-to-Site VPN | Direct Connect |
|---|---|---|
| Đường truyền | Internet (encrypted) | Đường dây vật lý riêng |
| Setup time | Vài phút | Tuần đến tháng |
| Bandwidth | ~1.25 Gbps | 1–100 Gbps |
| Latency | Không ổn định | Thấp, ổn định |
| Chi phí | Thấp | Cao |
| Dùng khi | Cần nhanh, budget thấp | Production, data lớn, latency quan trọng |

### Direct Connect Gateway
- Cho phép **1 Direct Connect connection** kết nối vào **nhiều VPC** ở nhiều Region.
- Không cần tạo riêng Direct Connect cho từng VPC.

### Virtual Private Gateway: Ingress Routing
- Tương tự IGW ingress routing — route inbound traffic từ on-premises qua appliance trước khi vào VPC.

---

## 7. AWS Transit Gateway (TGW)

### Vấn đề trước khi có TGW
Với nhiều VPC + on-premises, VPC Peering tạo ra **mesh phức tạp**:
- 5 VPC cần 10 peering connections
- Không transitive → mỗi cặp VPC cần 1 peering riêng
- Khó quản lý, khó scale

### TGW giải quyết thế nào
TGW là **hub trung tâm** — tất cả VPC và on-premises kết nối vào TGW, TGW lo routing:

```
VPC A ─┐
VPC B ─┤
VPC C ─┼─→ [Transit Gateway] ←─ VPN / Direct Connect → On-Premises
VPC D ─┤
VPC E ─┘
```

### Key Concepts

**Attachments** — cách kết nối vào TGW:
| Attachment type | Dùng cho |
|---|---|
| VPC attachment | Kết nối VPC vào TGW |
| VPN attachment | Kết nối Site-to-Site VPN |
| Direct Connect Gateway attachment | Kết nối Direct Connect |
| TGW Connect attachment | SD-WAN / third-party appliances (GRE tunnel) |
| Peering attachment | Kết nối 2 TGW với nhau (cross-region) |

**Route Tables** — TGW có route table riêng:
- **Association:** Mỗi attachment associate với 1 TGW route table — quyết định attachment dùng route table nào để lookup.
- **Propagation:** Attachment tự động propagate routes của nó vào TGW route table.

**Default behavior:**
- Mặc định tất cả attachments associate với **default route table** và propagate vào đó → tất cả VPC reach được nhau.
- Có thể tạo nhiều route table để **isolate** một số VPC (ví dụ: VPC production không reach VPC dev).

### TGW và Direct Connect
- TGW attach vào **Direct Connect Gateway** → 1 Direct Connect connection reach được tất cả VPC qua TGW.
- Thay thế việc phải tạo VGW riêng cho từng VPC.

### Transit Gateway Peering
- Kết nối 2 TGW ở **khác Region** với nhau.
- Traffic đi qua AWS backbone — không qua internet.
- Phải tự thêm static routes (không có route propagation qua TGW peering).

### Path Selection — TGW ưu tiên route nào?
Khi có nhiều path đến cùng destination:
1. **Longest prefix match** — cụ thể nhất được ưu tiên
2. **Static routes** — ưu tiên hơn propagated routes
3. **VPC attachment** — ưu tiên hơn VPN
4. **Direct Connect** — ưu tiên hơn VPN (nếu cùng prefix)

---

## 8. AWS Outposts

- AWS rack đặt **tại data center của bạn** — chạy AWS infrastructure on-premises.
- Có thể dùng cùng networking constructs như AWS Region: VPC, subnet, SG, route table.
- **Local Gateway (LGW):** Gateway đặc biệt cho Outpost — cho phép traffic từ Outpost ra on-premises LAN.
- **LGW Components:**
  - **Uplinks:** Kết nối vật lý Outpost → on-premises network
  - **VLANs:** Phân tách traffic
  - **Local Gateway Route Table:** Route traffic từ Outpost ra LAN

---

## 9. Tổng Hợp — Khi Nào Dùng Gì

### Kết nối Internet
| Nhu cầu | Giải pháp |
|---------|-----------|
| Public subnet cần inbound + outbound internet | Internet Gateway |
| Private subnet chỉ cần outbound internet | NAT Gateway |

### Kết nối VPC với VPC
| Nhu cầu | Giải pháp |
|---------|-----------|
| 2–3 VPC, kết nối đơn giản | VPC Peering |
| Nhiều VPC, cần hub trung tâm | Transit Gateway |
| VPC khác Region | VPC Peering (cross-region) hoặc TGW Peering |

### Kết nối On-Premises với AWS
| Nhu cầu | Giải pháp |
|---------|-----------|
| Nhanh, rẻ, bandwidth thấp | Site-to-Site VPN + VGW |
| Production, latency thấp, bandwidth cao | Direct Connect |
| 1 connection → nhiều VPC | Direct Connect Gateway |
| Nhiều VPC + on-premises, hub trung tâm | Transit Gateway |

---

## 10. Summary: Route Tables theo Scenario

| Scenario | Route Table cần có |
|----------|-------------------|
| Public subnet | `0.0.0.0/0 → IGW` |
| Private subnet có internet | `0.0.0.0/0 → NAT GW` |
| Isolated subnet (DB) | Chỉ `local` |
| Private subnet có S3 Endpoint | `local` + `NAT GW` + `pl-xxx → vpce` |
| VPC Peering | `10.x.x.x/16 → pcx-xxx` (thêm vào cả 2 VPC) |
| On-premises qua VPN/DX | Route propagation từ VGW hoặc TGW |

---

## Quick Reference — Câu hỏi hay gặp

**Q: VPC Peering có transitive không?**
A: Không. A↔B, B↔C không có nghĩa A reach được C. Phải tạo peering A↔C riêng, hoặc dùng Transit Gateway.

**Q: Khác nhau giữa VGW và TGW?**
A: VGW gắn vào 1 VPC, chỉ phục vụ VPC đó. TGW là hub trung tâm, nhiều VPC và on-premises kết nối vào — phù hợp khi có nhiều VPC cần communicate với nhau và với on-premises.

**Q: Direct Connect Gateway dùng để làm gì?**
A: Cho phép 1 Direct Connect connection reach nhiều VPC ở nhiều Region, thay vì phải tạo VGW riêng cho từng VPC.

**Q: TGW route table Association vs Propagation khác gì?**
A: Association quyết định attachment dùng route table nào để lookup khi forward traffic. Propagation quyết định attachment tự động thêm routes của nó vào route table nào.

**Q: Khi nào dùng VPN, khi nào dùng Direct Connect?**
A: VPN khi cần nhanh, budget thấp, bandwidth không quan trọng. Direct Connect khi cần latency thấp ổn định, bandwidth lớn, production workload — nhưng setup lâu và tốn kém hơn.

**Q: TGW Connect attachment dùng cho gì?**
A: Kết nối SD-WAN appliances hoặc third-party network appliances vào TGW qua GRE tunnel — thường dùng trong enterprise networking với thiết bị của Cisco, Palo Alto...
