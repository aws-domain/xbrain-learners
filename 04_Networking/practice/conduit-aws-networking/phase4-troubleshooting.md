# Phase 4 — Lỗi có Chủ Đích & Debug

> **Thời gian:** ~1.5 giờ  
> **Mục tiêu:** Gặp và debug 8 lỗi Networking thực tế  
> **Level:** Bắt đầu Intermediate (có hướng dẫn), tăng dần lên Advanced (chỉ có triệu chứng)

---

## Cách sử dụng Phase này

Mỗi lỗi có 3 phần:
1. **Cách tạo lỗi** — bạn chủ động break hệ thống
2. **Triệu chứng** — những gì bạn thấy
3. **Debug guide** — từ Intermediate (có hướng dẫn) đến Advanced (tự tìm)

**Quy trình debug chuẩn:**
```
1. Xác định triệu chứng (error message là gì?)
2. Xác định layer bị lỗi (Network? SG? Route? App?)
3. Kiểm tra từ ngoài vào trong (Internet → SG → Route → App)
4. Fix và verify
```

---

## Lỗi #1 — Security Group sai: Frontend không reach được Backend

**Level: Intermediate**

### Tạo lỗi

```bash
# Xóa rule cho phép Frontend SG vào Backend SG
aws ec2 revoke-security-group-ingress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 3001 \
  --source-group $SG_FRONTEND \
  --region ap-southeast-1
```

### Triệu chứng

Mở browser → `http://<FRONTEND_IP>` → trang load nhưng không có bài viết, console lỗi:
```
Failed to fetch: http://<FRONTEND_IP>/api/articles
```

Hoặc từ Frontend EC2:
```bash
curl http://$BACKEND_PRIVATE_IP:3001/api/articles
# → curl: (7) Failed to connect to ... port 3001: Connection refused
# hoặc: Connection timed out
```

### Debug Guide

**Bước 1:** Xác định lỗi ở đâu — Network hay App?

```bash
# Từ Frontend EC2, test connectivity
nc -zv $BACKEND_PRIVATE_IP 3001
# → Connection refused hoặc timeout → Network issue, không phải App issue
```

**Bước 2:** Kiểm tra Security Group của Backend

```bash
aws ec2 describe-security-groups \
  --group-ids $SG_BACKEND \
  --query "SecurityGroups[0].IpPermissions" \
  --output table \
  --region ap-southeast-1
# → Không thấy rule nào cho port 3001 → đây là vấn đề
```

**Bước 3:** Fix

```bash
aws ec2 authorize-security-group-ingress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 3001 \
  --source-group $SG_FRONTEND \
  --region ap-southeast-1
```

**Bước 4:** Verify

```bash
nc -zv $BACKEND_PRIVATE_IP 3001
# → Connection to ... 3001 port [tcp/*] succeeded!
```

**Bài học:** Security Group là stateful — chỉ cần allow inbound, response tự động được allow. Nhưng nếu thiếu inbound rule, connection bị block hoàn toàn.

---

## Lỗi #2 — Route Table thiếu: Backend không ra được internet

**Level: Intermediate**

### Tạo lỗi

```bash
# Xóa route NAT khỏi private route table
aws ec2 delete-route \
  --route-table-id $PRIVATE_RT \
  --destination-cidr-block 0.0.0.0/0 \
  --region ap-southeast-1
```

### Triệu chứng

SSH vào Backend EC2, thử:
```bash
curl https://registry.npmjs.org
# → curl: (6) Could not resolve host: registry.npmjs.org
# hoặc: Connection timed out
```

### Debug Guide

**Bước 1:** Test internet connectivity

```bash
# Từ Backend EC2
ping 8.8.8.8  # → 100% packet loss
curl ifconfig.me  # → timeout
```

**Bước 2:** Kiểm tra route table

```bash
# Từ local machine
aws ec2 describe-route-tables \
  --route-table-ids $PRIVATE_RT \
  --query "RouteTables[0].Routes" \
  --output table \
  --region ap-southeast-1
# → Chỉ thấy local route, không có 0.0.0.0/0
```

**Bước 3:** Kiểm tra NAT Gateway còn available không

```bash
aws ec2 describe-nat-gateways \
  --filter "Name=vpc-id,Values=$VPC_ID" \
  --query "NatGateways[0].{ID:NatGatewayId,State:State}" \
  --output table \
  --region ap-southeast-1
```

**Bước 4:** Fix

```bash
aws ec2 create-route \
  --route-table-id $PRIVATE_RT \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id $NAT_GW \
  --region ap-southeast-1
```

**Bài học:** Route table quyết định traffic đi đâu. Thiếu route `0.0.0.0/0 → NAT GW` = private subnet bị isolated hoàn toàn khỏi internet.

---

## Lỗi #3 — NACL block traffic: Bí ẩn — SG đúng nhưng vẫn không connect được

**Level: Intermediate → Advanced**

### Tạo lỗi

```bash
# Tạo NACL mới và associate với private subnet
NACL_ID=$(aws ec2 create-network-acl \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=conduit-broken-nacl}]' \
  --region ap-southeast-1 \
  --query "NetworkAcl.NetworkAclId" \
  --output text)

# Thêm rule DENY tất cả inbound (rule 100 deny all)
aws ec2 create-network-acl-entry \
  --network-acl-id $NACL_ID \
  --rule-number 100 \
  --protocol -1 \
  --rule-action deny \
  --ingress \
  --cidr-block 0.0.0.0/0 \
  --region ap-southeast-1

# Associate với private subnet
aws ec2 replace-network-acl-association \
  --association-id $(aws ec2 describe-network-acls \
    --filters "Name=association.subnet-id,Values=$PRIVATE_SUBNET" \
    --query "NetworkAcls[0].Associations[0].NetworkAclAssociationId" \
    --output text --region ap-southeast-1) \
  --network-acl-id $NACL_ID \
  --region ap-southeast-1
```

### Triệu chứng

```bash
# Từ Frontend EC2
curl http://$BACKEND_PRIVATE_IP:3001/api/articles
# → Connection timed out (không phải Connection refused)
```

Security Group nhìn có vẻ đúng, nhưng vẫn timeout. Đây là lỗi khó debug nhất vì SG không phải vấn đề.

### Debug Guide (Advanced — tự thử trước)

**Gợi ý:** Có 2 lớp firewall trong AWS — SG và NACL. Nếu SG đúng mà vẫn timeout, hãy kiểm tra NACL.

<details>
<summary>Xem đáp án đầy đủ</summary>

**Bước 1:** Phân biệt "Connection refused" vs "Connection timed out"
- `Connection refused` = port đang listen nhưng SG block → SG issue
- `Connection timed out` = packet không đến được đích → có thể NACL, Route, hoặc instance down

**Bước 2:** Kiểm tra NACL của private subnet

```bash
aws ec2 describe-network-acls \
  --filters "Name=association.subnet-id,Values=$PRIVATE_SUBNET" \
  --query "NetworkAcls[0].{ID:NetworkAclId,Entries:Entries}" \
  --output table \
  --region ap-southeast-1
# → Thấy rule 100 DENY all → đây là vấn đề
```

**Bước 3:** Fix — restore về default NACL

```bash
# Lấy default NACL ID
DEFAULT_NACL=$(aws ec2 describe-network-acls \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=default,Values=true" \
  --query "NetworkAcls[0].NetworkAclId" \
  --output text --region ap-southeast-1)

# Associate lại với default NACL
aws ec2 replace-network-acl-association \
  --association-id $(aws ec2 describe-network-acls \
    --filters "Name=association.subnet-id,Values=$PRIVATE_SUBNET" \
    --query "NetworkAcls[0].Associations[0].NetworkAclAssociationId" \
    --output text --region ap-southeast-1) \
  --network-acl-id $DEFAULT_NACL \
  --region ap-southeast-1
```

</details>

**Bài học:** NACL là stateless và hoạt động ở subnet level — nó block traffic trước khi SG được evaluate. Khi SG đúng mà vẫn timeout, luôn kiểm tra NACL.

---

## Lỗi #4 — Subnet sai: Backend đặt nhầm vào public subnet

**Level: Advanced — chỉ có triệu chứng**

### Tạo lỗi

Launch một Backend EC2 mới vào **public subnet** thay vì private subnet (simulate lỗi thiết kế).

### Triệu chứng

- Backend có public IP
- Backend accessible trực tiếp từ internet (security risk)
- `curl http://<BACKEND_PUBLIC_IP>:3001/api/articles` → trả về data (không nên xảy ra)

### Câu hỏi debug

1. Làm thế nào để phát hiện Backend đang ở sai subnet?
2. Tại sao đây là security risk dù SG chỉ allow từ Frontend SG?
3. Cách fix mà không cần terminate instance?

<details>
<summary>Gợi ý và đáp án</summary>

**Phát hiện:**
```bash
aws ec2 describe-instances \
  --instance-ids $BACKEND_INSTANCE \
  --query "Reservations[0].Instances[0].{SubnetId:SubnetId,PublicIP:PublicIpAddress}" \
  --output table --region ap-southeast-1
# → SubnetId = public subnet ID → sai
```

**Tại sao là security risk:**
Dù SG chỉ allow từ Frontend SG, nhưng:
- Instance có public IP → có thể bị scan/probe
- Nếu SG bị misconfigure sau này, backend exposed
- Principle of least privilege: backend không cần public IP

**Fix:**
Không thể thay đổi subnet của running instance. Phải:
1. Stop instance
2. Create AMI từ instance
3. Launch instance mới từ AMI vào đúng private subnet
4. Terminate instance cũ

**Bài học:** Subnet placement là quyết định không thể thay đổi sau khi launch. Phải đúng ngay từ đầu.

</details>

---

## Lỗi #5 — Security Group outbound: Backend không gọi được RDS

**Level: Advanced**

### Tạo lỗi

```bash
# Xóa tất cả outbound rules của Backend SG
aws ec2 revoke-security-group-egress \
  --group-id $SG_BACKEND \
  --protocol -1 \
  --cidr 0.0.0.0/0 \
  --region ap-southeast-1
```

### Triệu chứng

Backend app crash với lỗi:
```
Error: connect ETIMEDOUT <RDS_IP>:5432
```

### Câu hỏi debug

SG là stateful — tại sao xóa outbound rule lại ảnh hưởng đến kết nối đến RDS?

<details>
<summary>Gợi ý</summary>

SG stateful có nghĩa là: nếu bạn **initiate** connection từ Backend đến RDS, response tự động được allow về.

Nhưng "stateful" chỉ áp dụng cho **established connections**. Để **initiate** connection ra ngoài (outbound), bạn vẫn cần outbound rule.

Mặc định SG có outbound rule `allow all` — khi bạn xóa nó, Backend không thể initiate connection đến RDS nữa.

**Fix:**
```bash
# Restore outbound rule — chỉ allow đến RDS SG port 5432
aws ec2 authorize-security-group-egress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 5432 \
  --source-group $SG_DATABASE \
  --region ap-southeast-1

# Và allow HTTPS ra internet (cho npm, third-party APIs)
aws ec2 authorize-security-group-egress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0 \
  --region ap-southeast-1
```

</details>

---

## Lỗi #6 — IGW detached: Frontend mất internet access

**Level: Advanced**

### Tạo lỗi

```bash
aws ec2 detach-internet-gateway \
  --internet-gateway-id $IGW_ID \
  --vpc-id $VPC_ID \
  --region ap-southeast-1
```

### Triệu chứng

- `http://<FRONTEND_IP>` → timeout từ browser
- SSH vào Frontend → không được
- Nhưng... Frontend IP vẫn hiển thị trong Console

### Câu hỏi debug

1. Tại sao Frontend IP vẫn tồn tại nhưng không accessible?
2. Làm thế nào để verify IGW là vấn đề?
3. Fix như thế nào?

<details>
<summary>Đáp án</summary>

**Tại sao IP vẫn tồn tại:**
Public IP được assign cho instance, không phải cho IGW. Nhưng để traffic từ internet đến instance, cần IGW làm "cửa vào" VPC.

**Verify:**
```bash
aws ec2 describe-internet-gateways \
  --internet-gateway-ids $IGW_ID \
  --query "InternetGateways[0].Attachments" \
  --output table --region ap-southeast-1
# → State: detached
```

**Fix:**
```bash
aws ec2 attach-internet-gateway \
  --internet-gateway-id $IGW_ID \
  --vpc-id $VPC_ID \
  --region ap-southeast-1
```

</details>

---

## Lỗi #7 — NACL stateless: Ephemeral ports bị block

**Level: Advanced**

### Tạo lỗi

Tạo NACL custom cho public subnet, chỉ allow inbound port 80 nhưng quên allow outbound ephemeral ports:

```bash
NACL_PUBLIC=$(aws ec2 create-network-acl \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=conduit-public-nacl}]' \
  --region ap-southeast-1 \
  --query "NetworkAcl.NetworkAclId" \
  --output text)

# Allow inbound HTTP
aws ec2 create-network-acl-entry \
  --network-acl-id $NACL_PUBLIC \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=80,To=80 \
  --rule-action allow \
  --ingress \
  --cidr-block 0.0.0.0/0 \
  --region ap-southeast-1

# Allow outbound HTTP/HTTPS (nhưng QUÊN ephemeral ports)
aws ec2 create-network-acl-entry \
  --network-acl-id $NACL_PUBLIC \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=80,To=80 \
  --rule-action allow \
  --egress \
  --cidr-block 0.0.0.0/0 \
  --region ap-southeast-1

# Associate với public subnet
# (lấy association ID và replace)
```

### Triệu chứng

Browser gửi request đến `http://<FRONTEND_IP>` → **không nhận được response** (timeout), dù Nginx đang chạy bình thường.

### Câu hỏi debug

Tại sao allow inbound port 80 nhưng response không về được?

<details>
<summary>Giải thích</summary>

NACL là **stateless** — không nhớ connection state.

Khi browser kết nối đến port 80:
1. Browser gửi SYN từ ephemeral port (ví dụ: 54321) đến port 80 → **NACL inbound allow** ✅
2. Nginx xử lý và gửi response từ port 80 về ephemeral port 54321 → **NACL outbound cần allow port 54321** ❌

Ephemeral ports range: **1024–65535**

**Fix:**
```bash
# Thêm outbound rule cho ephemeral ports
aws ec2 create-network-acl-entry \
  --network-acl-id $NACL_PUBLIC \
  --rule-number 200 \
  --protocol tcp \
  --port-range From=1024,To=65535 \
  --rule-action allow \
  --egress \
  --cidr-block 0.0.0.0/0 \
  --region ap-southeast-1
```

**Bài học:** Đây là lý do AWS khuyến nghị dùng Security Group (stateful) là primary control, NACL chỉ là secondary. NACL dễ gây lỗi vì phải nhớ allow cả 2 chiều.

</details>

---

## Lỗi #8 — VPC Flow Logs: Debug bằng logs

**Level: Advanced**

### Scenario

Bạn nhận được báo cáo: "Đôi khi API call bị fail, không rõ nguyên nhân". Không có error message rõ ràng.

### Sử dụng VPC Flow Logs để debug

```bash
# Query Flow Logs trong CloudWatch
aws logs filter-log-events \
  --log-group-name /aws/vpc/conduit-flow-logs \
  --filter-pattern "REJECT" \
  --start-time $(date -d '1 hour ago' +%s000) \
  --region ap-southeast-1 \
  --query "events[*].message" \
  --output text | head -20
```

**Format của Flow Log:**
```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```

**Ví dụ REJECT log:**
```
2 123456789 eni-xxx 203.0.113.5 10.0.2.10 54321 3001 6 1 40 1234567890 1234567900 REJECT OK
```

Đọc log này: IP `203.0.113.5` cố gắng kết nối đến `10.0.2.10:3001` → bị REJECT → có thể là SG hoặc NACL block.

### Câu hỏi

1. Làm thế nào để phân biệt REJECT do SG vs NACL từ Flow Logs?
2. Nếu thấy nhiều REJECT từ cùng 1 IP, điều đó có nghĩa gì?

<details>
<summary>Gợi ý</summary>

**SG vs NACL trong Flow Logs:**
- Flow Logs capture traffic **trước khi** SG evaluate
- Nếu thấy REJECT → có thể là SG hoặc NACL
- Để phân biệt: kiểm tra xem traffic có đến được ENI không (SG evaluate ở ENI level)

**Nhiều REJECT từ 1 IP:**
- Có thể là port scanning / brute force attack
- Nên thêm NACL rule DENY IP đó (SG không có Deny rule)

</details>

---

## Tổng kết Phase 4

| Lỗi | Root Cause | Triệu chứng đặc trưng |
|-----|-----------|----------------------|
| #1 SG inbound missing | Security Group | Connection refused |
| #2 Route table missing | Route Table | DNS resolve fail, timeout |
| #3 NACL deny all | Network ACL | Timeout dù SG đúng |
| #4 Wrong subnet | Architecture | Instance có public IP không mong muốn |
| #5 SG outbound missing | Security Group | ETIMEDOUT khi connect ra ngoài |
| #6 IGW detached | Internet Gateway | Public IP không accessible |
| #7 NACL ephemeral | NACL stateless | Request vào được nhưng response không về |
| #8 Flow Logs debug | Monitoring | Dùng logs để tìm REJECT patterns |

**Debug checklist khi gặp networking issue:**
```
1. Ping/curl để xác định timeout vs refused
2. Kiểm tra Security Group (inbound + outbound)
3. Kiểm tra Route Table (có route đúng không?)
4. Kiểm tra NACL (có rule deny không?)
5. Kiểm tra IGW/NAT GW còn available không
6. Xem VPC Flow Logs để tìm REJECT
```
