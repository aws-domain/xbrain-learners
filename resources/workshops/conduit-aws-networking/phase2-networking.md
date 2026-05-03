# Phase 2 — Networking Foundation

> **Thời gian:** ~2 giờ  
> **Mục tiêu:** Tạo toàn bộ networking layer từ đầu — VPC, subnets, gateways, route tables, security groups  
> **Tool:** AWS Console + AWS CLI  
> **Region:** ap-southeast-1 (Singapore) — gần Việt Nam, Free Tier available

---

## Tại sao không dùng Default VPC?

AWS tạo sẵn một Default VPC trong mỗi Region. Bạn có thể dùng nó, nhưng workshop này **không dùng Default VPC** vì:

1. Default VPC có tất cả subnet là public — không phù hợp với production pattern
2. Bạn không học được cách thiết kế từ đầu
3. Trong thực tế, team sẽ tạo VPC riêng cho mỗi project/environment

---

## 2.1 Tạo VPC

### Qua Console

1. Vào **VPC Console** → **Your VPCs** → **Create VPC**
2. Chọn **VPC only** (không dùng "VPC and more" — ta muốn tự tạo từng thứ)
3. Điền:
   - Name tag: `conduit-vpc`
   - IPv4 CIDR: `10.0.0.0/16`
   - Tenancy: Default
4. Click **Create VPC**

### Qua CLI

```bash
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=conduit-vpc}]' \
  --region ap-southeast-1

# Lưu VPC ID vào biến
VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=conduit-vpc" \
  --query "Vpcs[0].VpcId" \
  --output text \
  --region ap-southeast-1)

echo "VPC ID: $VPC_ID"
```

**Tại sao /16?**
- 65,536 IP addresses — đủ cho mọi thứ trong workshop và mở rộng sau này
- Trong production: chọn CIDR không overlap với on-premises network

> **Lưu ý:** Sau khi tạo VPC, nó chưa có gì cả — không có subnet, không có internet access, không có gì. Bạn phải tự tạo từng thứ.

---

## 2.2 Tạo Subnets

Tạo 4 subnets theo plan từ Phase 1:

### Public Subnet (AZ-1a)

```bash
# Public Subnet
PUBLIC_SUBNET=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 \
  --availability-zone ap-southeast-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=conduit-public-1a}]' \
  --region ap-southeast-1 \
  --query "Subnet.SubnetId" \
  --output text)

echo "Public Subnet: $PUBLIC_SUBNET"
```

### Private Subnet (AZ-1a)

```bash
PRIVATE_SUBNET=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.2.0/24 \
  --availability-zone ap-southeast-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=conduit-private-1a}]' \
  --region ap-southeast-1 \
  --query "Subnet.SubnetId" \
  --output text)

echo "Private Subnet: $PRIVATE_SUBNET"
```

### Isolated Subnets (AZ-1a và AZ-1b — cho RDS)

```bash
ISOLATED_SUBNET_1A=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.3.0/24 \
  --availability-zone ap-southeast-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=conduit-isolated-1a}]' \
  --region ap-southeast-1 \
  --query "Subnet.SubnetId" \
  --output text)

ISOLATED_SUBNET_1B=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.4.0/24 \
  --availability-zone ap-southeast-1b \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=conduit-isolated-1b}]' \
  --region ap-southeast-1 \
  --query "Subnet.SubnetId" \
  --output text)

echo "Isolated 1a: $ISOLATED_SUBNET_1A"
echo "Isolated 1b: $ISOLATED_SUBNET_1B"
```

**Kiểm tra:** Vào Console → VPC → Subnets → filter theo VPC `conduit-vpc`. Bạn sẽ thấy 4 subnets.

> **Câu hỏi tự kiểm tra:** Lúc này, 4 subnets có gì khác nhau không? Tại sao chúng đều "giống nhau" dù tên khác nhau?

<details>
<summary>Trả lời</summary>

Chưa có gì khác nhau cả. Tất cả đều chỉ là dải IP. Sự khác biệt public/private/isolated được tạo ra bởi **Route Table** — subnet nào có route `0.0.0.0/0 → IGW` thì là public, không có thì là private/isolated.

</details>

---

## 2.3 Tạo Internet Gateway

```bash
# Tạo IGW
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=conduit-igw}]' \
  --region ap-southeast-1 \
  --query "InternetGateway.InternetGatewayId" \
  --output text)

# Attach vào VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id $IGW_ID \
  --vpc-id $VPC_ID \
  --region ap-southeast-1

echo "IGW: $IGW_ID attached to VPC: $VPC_ID"
```

**Lưu ý quan trọng:** Tạo IGW và attach vào VPC chưa đủ để có internet access. Subnet vẫn chưa phải public subnet — cần thêm route table.

---

## 2.4 Tạo Route Tables

### Route Table cho Public Subnet

```bash
# Tạo route table
PUBLIC_RT=$(aws ec2 create-route-table \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=conduit-public-rt}]' \
  --region ap-southeast-1 \
  --query "RouteTable.RouteTableId" \
  --output text)

# Thêm route ra internet
aws ec2 create-route \
  --route-table-id $PUBLIC_RT \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id $IGW_ID \
  --region ap-southeast-1

# Associate với public subnet
aws ec2 associate-route-table \
  --route-table-id $PUBLIC_RT \
  --subnet-id $PUBLIC_SUBNET \
  --region ap-southeast-1

echo "Public Route Table: $PUBLIC_RT"
```

**Sau bước này:** Public subnet đã có route `0.0.0.0/0 → IGW` → đây là public subnet thực sự.

### Route Table cho Private Subnet (tạm thời chưa có NAT)

```bash
PRIVATE_RT=$(aws ec2 create-route-table \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=conduit-private-rt}]' \
  --region ap-southeast-1 \
  --query "RouteTable.RouteTableId" \
  --output text)

aws ec2 associate-route-table \
  --route-table-id $PRIVATE_RT \
  --subnet-id $PRIVATE_SUBNET \
  --region ap-southeast-1
```

> **Lưu ý:** Private subnet chưa có route ra internet. Backend EC2 sẽ không ra được internet cho đến khi ta thêm NAT Gateway ở bước 2.5.

### Route Table cho Isolated Subnets

```bash
ISOLATED_RT=$(aws ec2 create-route-table \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=conduit-isolated-rt}]' \
  --region ap-southeast-1 \
  --query "RouteTable.RouteTableId" \
  --output text)

aws ec2 associate-route-table \
  --route-table-id $ISOLATED_RT \
  --subnet-id $ISOLATED_SUBNET_1A \
  --region ap-southeast-1

aws ec2 associate-route-table \
  --route-table-id $ISOLATED_RT \
  --subnet-id $ISOLATED_SUBNET_1B \
  --region ap-southeast-1
```

Isolated subnet chỉ có `local` route — không có route ra internet. RDS sẽ không bao giờ ra được internet.

---

## 2.5 Tạo NAT Gateway

NAT Gateway cần Elastic IP trước.

```bash
# Allocate Elastic IP
EIP_ALLOC=$(aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=conduit-nat-eip}]' \
  --region ap-southeast-1 \
  --query "AllocationId" \
  --output text)

echo "EIP Allocation ID: $EIP_ALLOC"

# Tạo NAT Gateway trong PUBLIC subnet
NAT_GW=$(aws ec2 create-nat-gateway \
  --subnet-id $PUBLIC_SUBNET \
  --allocation-id $EIP_ALLOC \
  --tag-specifications 'ResourceType=natgateway,Tags=[{Key=Name,Value=conduit-nat-gw}]' \
  --region ap-southeast-1 \
  --query "NatGateway.NatGatewayId" \
  --output text)

echo "NAT Gateway: $NAT_GW"
echo "Đợi NAT Gateway available (~1-2 phút)..."

# Đợi NAT GW available
aws ec2 wait nat-gateway-available \
  --nat-gateway-ids $NAT_GW \
  --region ap-southeast-1

echo "NAT Gateway ready!"
```

**Thêm route NAT vào Private Route Table:**

```bash
aws ec2 create-route \
  --route-table-id $PRIVATE_RT \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id $NAT_GW \
  --region ap-southeast-1
```

**Kiểm tra route tables:**

```bash
# Xem route table của private subnet
aws ec2 describe-route-tables \
  --route-table-ids $PRIVATE_RT \
  --query "RouteTables[0].Routes" \
  --output table \
  --region ap-southeast-1
```

Bạn sẽ thấy:
```
10.0.0.0/16 → local
0.0.0.0/0   → nat-xxxxxxxx
```

> ⚠️ **Nhắc nhở chi phí:** NAT Gateway tính phí từ lúc tạo. Nhớ xóa sau workshop.

---

## 2.6 Tạo Security Groups

Đây là phần quan trọng nhất — Security Group chain quyết định traffic flow.

### SG cho Frontend EC2

```bash
SG_FRONTEND=$(aws ec2 create-security-group \
  --group-name "conduit-sg-frontend" \
  --description "Security group for Conduit frontend" \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=conduit-sg-frontend}]' \
  --region ap-southeast-1 \
  --query "GroupId" \
  --output text)

# Allow HTTP từ internet
aws ec2 authorize-security-group-ingress \
  --group-id $SG_FRONTEND \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0 \
  --region ap-southeast-1

# Allow HTTPS từ internet (cho sau này)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_FRONTEND \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0 \
  --region ap-southeast-1

# Allow SSH từ IP của bạn (thay YOUR_IP bằng IP thực)
# Lấy IP: curl ifconfig.me
aws ec2 authorize-security-group-ingress \
  --group-id $SG_FRONTEND \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32 \
  --region ap-southeast-1

echo "Frontend SG: $SG_FRONTEND"
```

### SG cho Backend EC2

```bash
SG_BACKEND=$(aws ec2 create-security-group \
  --group-name "conduit-sg-backend" \
  --description "Security group for Conduit backend" \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=conduit-sg-backend}]' \
  --region ap-southeast-1 \
  --query "GroupId" \
  --output text)

# Allow port 3001 CHỈ từ Frontend SG
aws ec2 authorize-security-group-ingress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 3001 \
  --source-group $SG_FRONTEND \
  --region ap-southeast-1

# Allow SSH từ Frontend SG (để debug — Bastion Host pattern)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_BACKEND \
  --protocol tcp \
  --port 22 \
  --source-group $SG_FRONTEND \
  --region ap-southeast-1

echo "Backend SG: $SG_BACKEND"
```

**Tại sao Backend SG không allow từ `0.0.0.0/0`?**

Backend nằm trong private subnet — không có public IP. Nhưng ngay cả khi có, ta cũng không muốn expose port 3001 ra internet. Chỉ Frontend mới được gọi vào Backend.

### SG cho RDS

```bash
SG_DATABASE=$(aws ec2 create-security-group \
  --group-name "conduit-sg-database" \
  --description "Security group for Conduit database" \
  --vpc-id $VPC_ID \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=conduit-sg-database}]' \
  --region ap-southeast-1 \
  --query "GroupId" \
  --output text)

# Allow PostgreSQL CHỈ từ Backend SG
aws ec2 authorize-security-group-ingress \
  --group-id $SG_DATABASE \
  --protocol tcp \
  --port 5432 \
  --source-group $SG_BACKEND \
  --region ap-southeast-1

echo "Database SG: $SG_DATABASE"
```

**Verify Security Group chain:**

```bash
# Xem rules của Database SG
aws ec2 describe-security-groups \
  --group-ids $SG_DATABASE \
  --query "SecurityGroups[0].IpPermissions" \
  --output table \
  --region ap-southeast-1
```

---

## 2.7 Tạo S3 Gateway Endpoint (Optional nhưng nên làm)

Backend cần upload/download files từ S3 (ví dụ: avatar, attachments). Thay vì đi qua NAT Gateway (tốn phí), dùng S3 Gateway Endpoint (miễn phí).

```bash
# Tạo S3 Gateway Endpoint cho private subnet
aws ec2 create-vpc-endpoint \
  --vpc-id $VPC_ID \
  --service-name com.amazonaws.ap-southeast-1.s3 \
  --route-table-ids $PRIVATE_RT \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=conduit-s3-endpoint}]' \
  --region ap-southeast-1
```

Sau bước này, route table của private subnet sẽ có thêm entry:
```
pl-xxxxxxxx (S3) → vpce-xxxxxxxx
```

Traffic từ Backend đến S3 sẽ đi qua AWS internal network, không qua NAT Gateway.

---

## 2.8 Enable VPC Flow Logs

VPC Flow Logs giúp debug networking issues — bạn sẽ cần nó ở Phase 4.

```bash
# Tạo CloudWatch Log Group
aws logs create-log-group \
  --log-group-name /aws/vpc/conduit-flow-logs \
  --region ap-southeast-1

# Tạo IAM Role cho Flow Logs (qua Console dễ hơn)
# Console: VPC → Your VPCs → conduit-vpc → Flow logs tab → Create flow log
# Filter: All
# Destination: CloudWatch Logs
# Log group: /aws/vpc/conduit-flow-logs
```

---

## 2.9 Lưu lại tất cả IDs

Tạo file để lưu các IDs — cần dùng ở Phase 3:

```bash
cat > ~/conduit-ids.sh << EOF
export VPC_ID=$VPC_ID
export PUBLIC_SUBNET=$PUBLIC_SUBNET
export PRIVATE_SUBNET=$PRIVATE_SUBNET
export ISOLATED_SUBNET_1A=$ISOLATED_SUBNET_1A
export ISOLATED_SUBNET_1B=$ISOLATED_SUBNET_1B
export IGW_ID=$IGW_ID
export PUBLIC_RT=$PUBLIC_RT
export PRIVATE_RT=$PRIVATE_RT
export ISOLATED_RT=$ISOLATED_RT
export NAT_GW=$NAT_GW
export EIP_ALLOC=$EIP_ALLOC
export SG_FRONTEND=$SG_FRONTEND
export SG_BACKEND=$SG_BACKEND
export SG_DATABASE=$SG_DATABASE
EOF

echo "IDs saved to ~/conduit-ids.sh"
echo "Load with: source ~/conduit-ids.sh"
```

---

## 2.10 Checklist Phase 2

Verify từng thứ trước khi sang Phase 3:

```bash
# Load IDs
source ~/conduit-ids.sh

# Verify VPC
aws ec2 describe-vpcs --vpc-ids $VPC_ID \
  --query "Vpcs[0].{ID:VpcId,CIDR:CidrBlock,State:State}" \
  --output table --region ap-southeast-1

# Verify Subnets
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query "Subnets[*].{Name:Tags[?Key=='Name']|[0].Value,CIDR:CidrBlock,AZ:AvailabilityZone}" \
  --output table --region ap-southeast-1

# Verify Route Tables
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query "RouteTables[*].{Name:Tags[?Key=='Name']|[0].Value,Routes:Routes[*].DestinationCidrBlock}" \
  --output table --region ap-southeast-1

# Verify NAT Gateway
aws ec2 describe-nat-gateways \
  --filter "Name=vpc-id,Values=$VPC_ID" \
  --query "NatGateways[0].{ID:NatGatewayId,State:State,SubnetId:SubnetId}" \
  --output table --region ap-southeast-1

# Verify Security Groups
aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query "SecurityGroups[*].{Name:GroupName,ID:GroupId}" \
  --output table --region ap-southeast-1
```

**Checklist:**
- [ ] VPC `10.0.0.0/16` đã tạo
- [ ] 4 subnets đã tạo đúng CIDR và AZ
- [ ] IGW đã attach vào VPC
- [ ] Public subnet có route `0.0.0.0/0 → IGW`
- [ ] Private subnet có route `0.0.0.0/0 → NAT GW`
- [ ] Isolated subnet chỉ có `local` route
- [ ] NAT Gateway ở public subnet, state = available
- [ ] 3 Security Groups đã tạo với đúng rules
- [ ] S3 Gateway Endpoint đã tạo (optional)
- [ ] VPC Flow Logs đã enable

**Câu hỏi tự kiểm tra:**
1. Tại sao NAT Gateway phải đặt ở public subnet?
2. Nếu quên associate route table với subnet, điều gì xảy ra?
3. Sự khác biệt giữa `source-group` và `cidr` trong Security Group rule là gì?
4. Tại sao Backend SG allow SSH từ Frontend SG thay vì từ IP của bạn?
