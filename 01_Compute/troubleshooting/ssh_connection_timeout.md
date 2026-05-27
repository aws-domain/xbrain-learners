# Troubleshooting: SSH vào EC2 bị Time Out

## Triệu chứng
- Đã allow port 22 trong Security Group với source "My IP"
- Vẫn bị connection timeout khi SSH

---

## Nguyên nhân & Cách kiểm tra

### Lớp 1: Network — trước khi packet tới EC2

**NACL (Network ACL)** — hay bị bỏ qua nhất
- NACL là stateless → phải có rule cho cả **inbound port 22** VÀ **outbound ephemeral ports (1024-65535)**
- Nếu outbound bị block → connection bị drop sau khi handshake

**Route Table**
- Subnet của EC2 phải có route `0.0.0.0/0 → Internet Gateway`
- Thiếu route này → packet không biết đi đâu → timeout

**Internet Gateway**
- IGW đã được **attach vào VPC** chưa? Tạo IGW xong mà quên attach là lỗi rất thường gặp

---

### Lớp 2: EC2 Instance

**Public IP**
- EC2 có **Public IP hoặc Elastic IP** không? Không có public IP → không thể reach từ internet

**Subnet loại**
- EC2 đang ở **public subnet** hay **private subnet**? Private subnet không có route ra IGW → không SSH trực tiếp được

**Instance State**
- Instance đang thật sự ở trạng thái `running` chưa, hay đang `pending`/`stopping`?

---

### Lớp 3: Security Group

**"My IP" bị thay đổi** ⚠️ — nguyên nhân phổ biến nhất
- ISP cấp **dynamic IP** → IP thay đổi sau khi đã set rule → rule cũ không còn match
- Kiểm tra IP hiện tại rồi so với rule trong SG:
```bash
curl ifconfig.me
```

**Đúng SG nhưng sai instance**
- Instance có thể đang dùng SG khác, không phải SG bạn vừa sửa

---

### Lớp 4: Client Side

**Sai key pair** — thường gây `Permission denied` thay vì timeout
- Đảm bảo đúng file `.pem` và permission `400`:
```bash
chmod 400 key.pem
```

**Sai username**
| AMI | Username |
|---|---|
| Amazon Linux | `ec2-user` |
| Ubuntu | `ubuntu` |
| RHEL | `ec2-user` hoặc `root` |

---

## Debug nhanh

```bash
# 1. Kiểm tra IP hiện tại của bạn
curl ifconfig.me

# 2. Test port 22 có reachable không
nc -zv <EC2_PUBLIC_IP> 22

# 3. SSH với verbose để xem lỗi ở bước nào
ssh -vvv -i key.pem ec2-user@<EC2_PUBLIC_IP>
```

---

## Thứ tự ưu tiên kiểm tra

```
Route Table → IGW attached → Public IP → NACL → My IP còn đúng không → Key pair & Username
```
