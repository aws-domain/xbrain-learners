# Phase 5 — Workarounds & Alternatives

> **Thời gian:** ~30 phút  
> **Mục tiêu:** Hiểu trade-off của từng quyết định — có thể làm khác không? Tại sao?

---

## 5.1 NAT Gateway → NAT Instance (Free Tier workaround)

### Vấn đề

NAT Gateway tốn ~$0.045/giờ — không có Free Tier. Với workshop dài ngày, chi phí tích lũy.

### Workaround: NAT Instance

NAT Instance là EC2 t2.micro chạy NAT software — **nằm trong Free Tier**.

```bash
# Tìm NAT Instance AMI (AWS cung cấp sẵn)
NAT_AMI=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=amzn-ami-vpc-nat*" \
  --query "sort_by(Images, &CreationDate)[-1].ImageId" \
  --output text \
  --region ap-southeast-1)

# Launch NAT Instance trong public subnet
NAT_INSTANCE=$(aws ec2 run-instances \
  --image-id $NAT_AMI \
  --instance-type t2.micro \
  --key-name conduit-key \
  --subnet-id $PUBLIC_SUBNET \
  --security-group-ids $SG_FRONTEND \
  --associate-public-ip-address \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=conduit-nat-instance}]' \
  --region ap-southeast-1 \
  --query "Instances[0].InstanceId" \
  --output text)

# QUAN TRỌNG: Disable source/destination check
aws ec2 modify-instance-attribute \
  --instance-id $NAT_INSTANCE \
  --no-source-dest-check \
  --region ap-southeast-1

# Update private route table để dùng NAT Instance thay NAT Gateway
aws ec2 replace-route \
  --route-table-id $PRIVATE_RT \
  --destination-cidr-block 0.0.0.0/0 \
  --instance-id $NAT_INSTANCE \
  --region ap-southeast-1
```

### Trade-off Analysis

| | NAT Gateway | NAT Instance |
|---|---|---|
| **Chi phí** | ~$0.045/giờ + data | Free Tier (t2.micro) |
| **Availability** | Highly available (AWS managed) | Single point of failure |
| **Bandwidth** | Tự động scale | Giới hạn bởi instance type |
| **Maintenance** | AWS lo | Bạn phải patch OS |
| **Setup** | 1 lệnh | Nhiều bước, dễ sai |
| **Dùng cho** | Production | Dev/Test, học tập |

**Kết luận:** NAT Instance phù hợp cho workshop/learning. Production luôn dùng NAT Gateway.

---

## 5.2 RDS → PostgreSQL trên EC2 (Đơn giản hơn nhưng mất gì?)

### Workaround

Thay vì RDS, cài PostgreSQL trực tiếp trên Backend EC2:

```bash
# Trên Backend EC2
sudo yum install -y postgresql15-server
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Tạo database
sudo -u postgres psql -c "CREATE USER conduit_admin WITH PASSWORD 'ChangeMe123!';"
sudo -u postgres psql -c "CREATE DATABASE conduit OWNER conduit_admin;"
```

### Trade-off Analysis

| | RDS PostgreSQL | PostgreSQL trên EC2 |
|---|---|---|
| **Backup** | Automated, point-in-time | Tự setup cron job |
| **Patching** | AWS lo | Bạn phải tự patch |
| **Failover** | Multi-AZ tự động | Không có |
| **Monitoring** | CloudWatch tích hợp | Tự setup |
| **Chi phí** | db.t3.micro Free Tier | Dùng chung EC2 Free Tier |
| **Networking** | Isolated subnet riêng | Cùng subnet với Backend |
| **Shared Responsibility** | AWS lo OS/DB engine | Bạn lo tất cả |

**Kết luận:** PostgreSQL trên EC2 đơn giản hơn nhưng mất toàn bộ managed service benefits. Trong workshop này, RDS tốt hơn vì học được Shared Responsibility Model thực tế.

---

## 5.3 Bastion Host → AWS Systems Manager Session Manager

### Vấn đề với Bastion Host

- Cần mở port 22 (SSH) — attack surface
- Cần quản lý SSH keys
- Nếu Bastion Host down → không SSH được vào private instances

### Workaround: SSM Session Manager

SSM Session Manager cho phép SSH vào EC2 **không cần port 22**, không cần public IP, không cần SSH key.

```bash
# Cài SSM Agent trên Backend EC2 (Amazon Linux 2023 đã có sẵn)
# Chỉ cần IAM role đúng

# Tạo IAM role cho EC2
aws iam create-role \
  --role-name conduit-ec2-ssm-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name conduit-ec2-ssm-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

# Attach role vào Backend EC2
aws ec2 associate-iam-instance-profile \
  --instance-id $BACKEND_INSTANCE \
  --iam-instance-profile Name=conduit-ec2-ssm-role \
  --region ap-southeast-1

# SSH vào Backend qua SSM (không cần port 22!)
aws ssm start-session \
  --target $BACKEND_INSTANCE \
  --region ap-southeast-1
```

### Trade-off Analysis

| | Bastion Host | SSM Session Manager |
|---|---|---|
| **Port 22** | Cần mở | Không cần |
| **SSH Key** | Cần quản lý | Không cần |
| **Audit** | Khó | CloudTrail log tất cả sessions |
| **Setup** | Đơn giản | Cần IAM role |
| **Chi phí** | EC2 instance | Miễn phí |
| **Availability** | Phụ thuộc Bastion EC2 | AWS managed |

**Kết luận:** SSM Session Manager là best practice hiện đại. Bastion Host vẫn dùng khi cần port forwarding phức tạp.

---

## 5.4 Public IP → Elastic IP (Khi nào cần?)

### Vấn đề

Frontend EC2 có public IP, nhưng IP này thay đổi mỗi lần stop/start instance.

### Workaround: Elastic IP

```bash
# Allocate Elastic IP cho Frontend
FRONTEND_EIP=$(aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=conduit-frontend-eip}]' \
  --region ap-southeast-1 \
  --query "AllocationId" \
  --output text)

# Associate với Frontend instance
aws ec2 associate-address \
  --instance-id $FRONTEND_INSTANCE \
  --allocation-id $FRONTEND_EIP \
  --region ap-southeast-1

FRONTEND_EIP_ADDRESS=$(aws ec2 describe-addresses \
  --allocation-ids $FRONTEND_EIP \
  --query "Addresses[0].PublicIp" \
  --output text \
  --region ap-southeast-1)

echo "Frontend Elastic IP: $FRONTEND_EIP_ADDRESS"
```

### Khi nào cần Elastic IP?

- Khi cần IP cố định để DNS trỏ vào
- Khi đối tác whitelist IP của bạn
- Khi dùng NAT Gateway (bắt buộc)

**Lưu ý:** Elastic IP miễn phí khi gắn vào running instance. Tính phí khi không gắn vào đâu.

---

## 5.5 Single AZ → Multi-AZ (Khi nào upgrade?)

### Hiện tại (Workshop)

```
AZ-1a: Frontend + Backend + RDS primary
AZ-1b: RDS subnet (dự phòng, chưa dùng)
```

### Production Pattern

```
AZ-1a: Frontend EC2 + Backend EC2 + RDS primary
AZ-1b: Frontend EC2 + Backend EC2 + RDS standby
       ↑ ALB distribute traffic giữa 2 AZ
```

### Upgrade path

1. **Bước 1:** Enable RDS Multi-AZ (1 click trong Console)
2. **Bước 2:** Launch Backend EC2 thứ 2 trong AZ-1b
3. **Bước 3:** Tạo ALB distribute traffic giữa 2 Backend
4. **Bước 4:** Launch Frontend EC2 thứ 2 trong AZ-1b
5. **Bước 5:** Tạo ALB cho Frontend

**Chi phí tăng thêm:**
- RDS Multi-AZ: ~2x chi phí RDS
- ALB: ~$0.008/giờ + LCU
- EC2 thứ 2: hết Free Tier

**Kết luận:** Multi-AZ là production requirement, nhưng tốn tiền. Workshop dùng Single AZ để tiết kiệm, hiểu concept là đủ.

---

## 5.6 Trusted Advisor — Kiểm tra sau khi deploy

Sau khi hệ thống chạy ổn định, dùng **AWS Trusted Advisor** để review xem có misconfiguration nào không.

> **Từ AWS Docs:** Trusted Advisor inspects your AWS environment và đưa ra recommendations về cost savings, security, performance, fault tolerance, và service limits.

**Lưu ý về Free Tier:** Basic Support plan (miễn phí) chỉ có access vào:
- **Security checks** (một số)
- **Service Limits checks** (tất cả)

Các checks quan trọng nhất với Free Tier:

### Security checks (available với Basic plan)

```
AWS Console → Trusted Advisor → Security
```

| Check | Ý nghĩa với Conduit |
|-------|---------------------|
| **Security Groups — Specific Ports Unrestricted** | Phát hiện SG nào đang allow `0.0.0.0/0` vào port nhạy cảm (22, 3389, 3306...) |
| **Amazon S3 Bucket Permissions** | S3 bucket nào đang public |
| **IAM Use** | Có đang dùng root account không |
| **MFA on Root Account** | Root account có bật MFA chưa |

**Chạy check và xem kết quả:**

```
Trusted Advisor → Security → Security Groups - Specific Ports Unrestricted
→ Nếu thấy WARNING: SG của bạn đang allow port 22 từ 0.0.0.0/0
→ Fix: Đổi thành IP cụ thể của bạn (YOUR_IP/32)
```

### Service Limits checks

```
Trusted Advisor → Service Limits
→ Xem EC2 On-Demand Instance Limit
→ Xem VPC Elastic IP Address Limit
```

Quan trọng khi scale — biết giới hạn trước khi hit limit trong production.

---

## 5.7 Cost Explorer — Xem chi phí thực tế

Sau khi workshop chạy vài giờ, vào **Cost Explorer** để xem chi phí thực tế so với estimate.

```
AWS Console → Billing → Cost Explorer → Launch Cost Explorer
```

**Xem chi phí theo service:**
```
Cost Explorer → Service filter
→ Chọn: EC2, RDS, NAT Gateway, VPC
→ Time range: Last 7 days
→ Group by: Service
```

**So sánh với estimate:**

| Service | Estimate | Thực tế | Chênh lệch |
|---------|----------|---------|------------|
| EC2 | $0 (Free Tier) | ? | ? |
| RDS | $0 (Free Tier) | ? | ? |
| NAT Gateway | ~$0.36/ngày | ? | ? |
| Data Transfer | ~$0.09 | ? | ? |

**Nếu thấy charge bất ngờ:**
1. Xem Cost Explorer → filter theo service có charge
2. Drill down vào Usage Type để xem chi tiết
3. Kiểm tra xem có resource nào đang chạy mà bạn không biết không

> **Tip:** Cost Explorer có độ trễ ~24 giờ — charge hôm nay sẽ hiện vào ngày mai.

---

## 5.8 Cleanup — Xóa tất cả sau Workshop

⚠️ **Quan trọng:** Xóa theo đúng thứ tự để tránh dependency errors.

```bash
source ~/conduit-ids.sh

# 1. Terminate EC2 instances
aws ec2 terminate-instances \
  --instance-ids $FRONTEND_INSTANCE $BACKEND_INSTANCE \
  --region ap-southeast-1

aws ec2 wait instance-terminated \
  --instance-ids $FRONTEND_INSTANCE $BACKEND_INSTANCE \
  --region ap-southeast-1

# 2. Delete RDS (no final snapshot để tiết kiệm)
aws rds delete-db-instance \
  --db-instance-identifier conduit-postgres \
  --skip-final-snapshot \
  --region ap-southeast-1

# 3. Delete NAT Gateway (tốn tiền nhất)
aws ec2 delete-nat-gateway \
  --nat-gateway-id $NAT_GW \
  --region ap-southeast-1

# Đợi NAT GW deleted
aws ec2 wait nat-gateway-deleted \
  --nat-gateway-ids $NAT_GW \
  --region ap-southeast-1 2>/dev/null || sleep 60

# 4. Release Elastic IP
aws ec2 release-address \
  --allocation-id $EIP_ALLOC \
  --region ap-southeast-1

# 5. Delete Security Groups
aws ec2 delete-security-group --group-id $SG_DATABASE --region ap-southeast-1
aws ec2 delete-security-group --group-id $SG_BACKEND --region ap-southeast-1
aws ec2 delete-security-group --group-id $SG_FRONTEND --region ap-southeast-1

# 6. Delete Subnets
aws ec2 delete-subnet --subnet-id $PUBLIC_SUBNET --region ap-southeast-1
aws ec2 delete-subnet --subnet-id $PRIVATE_SUBNET --region ap-southeast-1
aws ec2 delete-subnet --subnet-id $ISOLATED_SUBNET_1A --region ap-southeast-1
aws ec2 delete-subnet --subnet-id $ISOLATED_SUBNET_1B --region ap-southeast-1

# 7. Detach và delete IGW
aws ec2 detach-internet-gateway \
  --internet-gateway-id $IGW_ID \
  --vpc-id $VPC_ID \
  --region ap-southeast-1

aws ec2 delete-internet-gateway \
  --internet-gateway-id $IGW_ID \
  --region ap-southeast-1

# 8. Delete Route Tables
aws ec2 delete-route-table --route-table-id $PUBLIC_RT --region ap-southeast-1
aws ec2 delete-route-table --route-table-id $PRIVATE_RT --region ap-southeast-1
aws ec2 delete-route-table --route-table-id $ISOLATED_RT --region ap-southeast-1

# 9. Delete VPC
aws ec2 delete-vpc --vpc-id $VPC_ID --region ap-southeast-1

# 10. Delete Key Pair
aws ec2 delete-key-pair --key-name conduit-key --region ap-southeast-1
rm ~/.ssh/conduit-key.pem

echo "Cleanup complete!"
```

---

## Tổng kết Workshop

### Kiến thức đã thực hành

| Concept | Thực hành ở đâu |
|---------|----------------|
| VPC design | Phase 2 — tạo từ đầu |
| Public/Private/Isolated subnet | Phase 2 + Phase 3 |
| Internet Gateway | Phase 2 |
| NAT Gateway | Phase 2 + Phase 5 (NAT Instance alternative) |
| Route Table | Phase 2 + Lỗi #2 |
| Security Group chain | Phase 2 + Lỗi #1, #5 |
| Network ACL | Lỗi #3, #7 |
| Elastic IP | Phase 2 (NAT GW) + Phase 5 |
| Bastion Host | Phase 3 + Phase 5 (SSM alternative) |
| VPC Flow Logs | Phase 2 + Lỗi #8 |
| S3 Gateway Endpoint | Phase 2 |
| Multi-AZ concept | Phase 1 + Phase 5 |

### Next Steps

Workshop này tạo ra nền tảng để học tiếp:
- **Security Workshop:** IAM roles cho EC2, KMS encrypt RDS, WAF
- **Database Workshop:** RDS Multi-AZ, Read Replica, Aurora
- **Serverless Workshop:** Migrate Backend sang Lambda + API Gateway
- **CI/CD Workshop:** CodePipeline auto-deploy khi push code
- **Monitoring Workshop:** CloudWatch dashboards, alarms, X-Ray
