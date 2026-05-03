# Task 3.5 — AWS Network Services

> **Exam weight:** Domain 3 = 34% of scored content

## Amazon VPC (Virtual Private Cloud)

VPC là **mạng ảo riêng** của bạn trên AWS — isolated, logically separated từ các customers khác.

### VPC Components

#### Subnets
- **Phân chia VPC** thành các segments nhỏ hơn
- **Public Subnet** — có route đến Internet Gateway, accessible từ internet
- **Private Subnet** — không có route trực tiếp ra internet
- Mỗi subnet nằm trong **một AZ** cụ thể

#### Internet Gateway (IGW)
- Cho phép resources trong VPC **giao tiếp với internet**
- Attach vào VPC, sau đó thêm route trong route table
- Highly available và scalable tự động

#### NAT Gateway
- Cho phép **private subnet instances** truy cập internet (outbound only)
- Internet không thể initiate connection vào private instances
- Managed service, highly available trong AZ
- **NAT Instance** = EC2-based alternative (ít dùng hơn)

#### Route Tables
- Định nghĩa **traffic routing** trong VPC
- Mỗi subnet associate với một route table
- Default route: local traffic trong VPC

#### VPC Peering
- Kết nối **hai VPCs** với nhau (cùng hoặc khác account/Region)
- Traffic đi qua AWS private network
- Không transitive (A↔B, B↔C không có nghĩa A↔C)

---

## Security trong VPC

### Security Groups
- **Stateful firewall** ở cấp độ instance/ENI
- Chỉ có Allow rules (không có Deny)
- Inbound và outbound rules riêng biệt
- Stateful: nếu allow inbound, response tự động được allow outbound

### Network ACLs (NACLs)
- **Stateless firewall** ở cấp độ subnet
- Có cả Allow và Deny rules
- Rules được evaluate theo thứ tự số (thấp hơn = ưu tiên hơn)
- Stateless: phải explicitly allow cả inbound và outbound

| | Security Groups | NACLs |
|---|---|---|
| **Level** | Instance | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow + Deny |
| **Default** | Deny all inbound | Allow all |

### Amazon Inspector
- Scan EC2 instances và container images tìm **vulnerabilities**
- Kiểm tra: CVEs, network exposure, unintended access

---

## DNS — Amazon Route 53

- **Managed DNS service** của AWS
- Chức năng:
  - **Domain registration** — mua và quản lý domain names
  - **DNS routing** — translate domain names thành IP addresses
  - **Health checking** — monitor endpoints, route traffic away từ unhealthy endpoints

### Routing Policies
| Policy | Dùng cho |
|--------|---------|
| **Simple** | Single resource |
| **Weighted** | A/B testing, gradual traffic shift |
| **Latency** | Route đến Region có latency thấp nhất |
| **Failover** | Active-passive failover |
| **Geolocation** | Route dựa trên vị trí địa lý người dùng |
| **Multivalue Answer** | Multiple healthy resources |

---

## Network Connectivity Options

### AWS VPN (Virtual Private Network)
- **Encrypted connection** qua public internet
- **Site-to-Site VPN** — kết nối on-premises network với VPC
- **Client VPN** — kết nối individual users với AWS
- Setup nhanh, chi phí thấp
- Bandwidth phụ thuộc vào internet connection

### AWS Direct Connect
- **Dedicated private connection** từ on-premises đến AWS
- Không đi qua public internet
- Bandwidth: 1 Gbps đến 100 Gbps
- **Consistent network performance**, lower latency
- Phù hợp cho: large data transfers, compliance, hybrid architectures

| | AWS VPN | AWS Direct Connect |
|---|---|---|
| **Connection** | Qua internet (encrypted) | Dedicated private line |
| **Setup time** | Vài phút | Vài tuần/tháng |
| **Cost** | Thấp | Cao hơn |
| **Bandwidth** | Biến động | Consistent |
| **Use case** | Backup, quick setup | Production, large data |

---

## Exam Tips

- Public subnet = có IGW route; Private subnet = không có IGW route
- NAT Gateway = private instances ra internet (outbound only)
- Security Groups = stateful, instance level; NACLs = stateless, subnet level
- Route 53 = DNS + domain registration + health checks
- Direct Connect = dedicated line, consistent performance
- VPN = encrypted over internet, quick setup
