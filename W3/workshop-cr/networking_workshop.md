# AWS Networking Workshop — Foundation to Intermediate

> **Mục tiêu:** Hands-on với đúng những kiến thức đã học — VPC 3-tier, Subnets, Route Tables, Gateways, Security Groups, NACLs, VPC Endpoints, Lambda trong VPC.
>
> **Thời gian ước tính:** 3–4 giờ (có thể chia nhiều buổi)
>
> **Chi phí ước tính:** ~$1–2 nếu làm xong trong 1 ngày và cleanup đúng cách (NAT Gateway là thứ tốn tiền nhất ~$0.045/giờ)
>
> **Region khuyến nghị:** `ap-southeast-1` (Singapore) — gần nhất, latency thấp

---

## Tổng quan các Lab

| Lab | Tên | Kiến thức thực hành | Level |
|-----|-----|---------------------|-------|
| Lab 1 | Tạo VPC 3-Tier từ đầu | VPC, Subnets, CIDR, IGW | Foundation |
| Lab 2 | Cấu hình Route Tables | Route Tables, NAT Gateway | Foundation |
| Lab 3 | Security Groups & NACLs | SG vs NACL, Stateful vs Stateless | Foundation |
| Lab 4 | Lambda trong VPC | Lambda + VPC, ENI, connectivity | Foundation |
| Lab 5 | S3 Gateway Endpoint | VPC Endpoint, Route Table | Foundation |
| Lab 6 | Kiểm tra toàn bộ flow | End-to-end verification | Intermediate |

---

## Lab 1 — Tạo VPC 3-Tier Từ Đầu

**Mục tiêu:** Hiểu CIDR, tạo VPC và 3 loại subnet, gắn Internet Gateway.

### Bước 1.1 — Tạo VPC

1. Vào **VPC Console** → **Your VPCs** → **Create VPC**
2. Chọn **VPC only** (không dùng VPC and more — tự làm từng bước để hiểu)
3. Điền:
   - Name: `workshop-vpc`
   - IPv4 CIDR: `10.0.0.0/16`
4. Click **Create VPC**

> **Checkpoint:** Tại sao dùng `/16`? → 65,536 địa chỉ, đủ để chia nhiều subnet con.

### Bước 1.2 — Tạo 3 Subnets

Tạo lần lượt 3 subnet trong VPC vừa tạo (**Subnets** → **Create subnet**):

| Subnet | Name | AZ | CIDR |
|--------|------|----|------|
| Public | `workshop-public-1a` | `ap-southeast-1a` | `10.0.1.0/24` |
| Private | `workshop-private-1a` | `ap-southeast-1a` | `10.0.2.0/24` |
| Isolated | `workshop-isolated-1a` | `ap-southeast-1a` | `10.0.3.0/24` |

> **Checkpoint:** Mỗi subnet `/24` có bao nhiêu IP dùng được? → 256 - 5 (AWS reserve) = **251 IP**.

### Bước 1.3 — Tạo và Gắn Internet Gateway

1. **Internet Gateways** → **Create internet gateway**
   - Name: `workshop-igw`
2. Sau khi tạo xong → **Actions** → **Attach to VPC** → chọn `workshop-vpc`

> **Checkpoint:** IGW ở trạng thái `detached` thì public subnet có ra internet được không? → **Không**.

---

## Lab 2 — Cấu Hình Route Tables

**Mục tiêu:** Hiểu route table quyết định traffic đi đâu, tạo NAT Gateway, phân biệt route table của 3 loại subnet.

### Bước 2.1 — Route Table cho Public Subnet

1. **Route Tables** → **Create route table**
   - Name: `workshop-rt-public`
   - VPC: `workshop-vpc`
2. Sau khi tạo → tab **Routes** → **Edit routes** → **Add route**:
   - Destination: `0.0.0.0/0`
   - Target: chọn **Internet Gateway** → `workshop-igw`
3. Tab **Subnet associations** → **Edit subnet associations** → chọn `workshop-public-1a`

> **Checkpoint:** Mở Route Table của public subnet ra — bạn thấy 2 routes: `10.0.0.0/16 → local` và `0.0.0.0/0 → igw-xxx`. Đây chính xác là pattern đã học.

### Bước 2.2 — Tạo NAT Gateway

1. **NAT Gateways** → **Create NAT gateway**
   - Name: `workshop-nat`
   - Subnet: **`workshop-public-1a`** ← quan trọng! NAT GW phải đặt ở public subnet
   - Connectivity type: **Public**
   - Click **Allocate Elastic IP** (tự động tạo)
2. Chờ status chuyển sang **Available** (~1–2 phút)

> **Checkpoint:** Tại sao NAT Gateway đặt ở public subnet? → Vì nó cần IGW để forward traffic ra internet.

### Bước 2.3 — Route Table cho Private Subnet

1. Tạo route table mới:
   - Name: `workshop-rt-private`
   - VPC: `workshop-vpc`
2. Add route:
   - Destination: `0.0.0.0/0`
   - Target: **NAT Gateway** → `workshop-nat`
3. Associate với `workshop-private-1a`

### Bước 2.4 — Route Table cho Isolated Subnet

1. Tạo route table mới:
   - Name: `workshop-rt-isolated`
   - VPC: `workshop-vpc`
2. **Không add thêm route nào** — chỉ giữ `10.0.0.0/16 → local`
3. Associate với `workshop-isolated-1a`

> **Checkpoint cuối Lab 2:** So sánh 3 route tables:
> - Public: `local` + `0.0.0.0/0 → IGW`
> - Private: `local` + `0.0.0.0/0 → NAT`
> - Isolated: chỉ `local`
>
> Đây chính xác là bảng so sánh đã học.

---

## Lab 3 — Security Groups & NACLs

**Mục tiêu:** Tạo SG cho từng tier, hiểu stateful vs stateless bằng cách thực hành với NACL.

### Bước 3.1 — Tạo Security Groups

Tạo 3 Security Groups (**Security Groups** → **Create security group**), tất cả trong `workshop-vpc`:

**SG 1 — Bastion Host SG** (`workshop-sg-bastion`):
- Inbound: SSH (22) từ **My IP** (không phải 0.0.0.0/0)
- Outbound: All traffic (default)

**SG 2 — App/Lambda SG** (`workshop-sg-app`):
- Inbound: SSH (22) từ **`workshop-sg-bastion`** (chọn Security Group làm source)
- Outbound: HTTPS (443) → `0.0.0.0/0`
- Outbound: MySQL/Aurora (3306) → `workshop-sg-db` *(tạo sau)*

**SG 3 — Database SG** (`workshop-sg-db`):
- Inbound: MySQL/Aurora (3306) từ **`workshop-sg-app`**
- Outbound: All traffic (default — RDS cần trả response)

> **Checkpoint:** SG của DB không có rule inbound từ `0.0.0.0/0`. Chỉ App SG mới được vào. Đây là pattern "least privilege".

### Bước 3.2 — Thực Hành NACL (Hiểu Stateless)

Mục tiêu: chứng minh NACL stateless bằng cách tạo rule inbound nhưng quên outbound.

1. **Network ACLs** → tìm NACL đang associate với `workshop-public-1a`
2. Tab **Inbound rules** → **Edit inbound rules**:
   - Rule 100: Allow, TCP, Port 443, Source `0.0.0.0/0`
3. Tab **Outbound rules** → **Edit outbound rules**:
   - Xóa rule Allow All (nếu có), chỉ để **Deny All**

> **Quan sát:** Nếu bạn deploy EC2 vào public subnet và thử HTTPS — request vào được (inbound allow) nhưng response không về được (outbound deny ephemeral ports). Đây chính là stateless.

4. Fix lại: thêm outbound rule:
   - Rule 100: Allow, TCP, Port **1024–65535** (ephemeral ports), Destination `0.0.0.0/0`

> **Checkpoint:** Sau khi thêm outbound ephemeral ports → traffic hoạt động bình thường. Đây là lý do NACL phức tạp hơn SG.

5. **Cleanup NACL**: restore về Allow All để không ảnh hưởng các lab sau.

---

## Lab 4 — Lambda Trong VPC

**Mục tiêu:** Deploy Lambda vào private subnet, quan sát ENI được tạo, test connectivity.

### Bước 4.1 — Tạo Lambda Function

1. **Lambda Console** → **Create function**
   - Name: `workshop-lambda-vpc`
   - Runtime: Python 3.12
   - Architecture: x86_64

2. Tab **Configuration** → **VPC** → **Edit**:
   - VPC: `workshop-vpc`
   - Subnets: `workshop-private-1a`
   - Security groups: `workshop-sg-app`

3. Click **Save** — chờ Lambda tạo ENI (~30–60 giây)

### Bước 4.2 — Quan Sát ENI Được Tạo

1. Vào **EC2 Console** → **Network Interfaces**
2. Filter theo VPC: `workshop-vpc`
3. Bạn sẽ thấy ENI mới với description chứa tên Lambda function

> **Checkpoint:** ENI này có private IP trong range `10.0.2.x` (private subnet CIDR). Đây là "card mạng ảo" Lambda dùng để communicate trong VPC.

### Bước 4.3 — Test: Lambda Có Ra Internet Không?

Paste code này vào Lambda function:

```python
import urllib.request
import json

def lambda_handler(event, context):
    try:
        # Test internet access
        response = urllib.request.urlopen('https://httpbin.org/ip', timeout=5)
        data = json.loads(response.read())
        return {
            'statusCode': 200,
            'body': f"Internet access: YES — IP: {data['origin']}"
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': f"Internet access: NO — Error: {str(e)}"
        }
```

**Test** → **Test** (tạo test event mặc định) → Chạy.

> **Kết quả mong đợi:** `Internet access: YES` — vì private subnet có route qua NAT Gateway.
>
> **Thử thêm:** Xóa route `0.0.0.0/0 → NAT` khỏi `workshop-rt-private` → chạy lại → kết quả sẽ là `NO`. Restore lại sau khi test.

---

## Lab 5 — S3 Gateway Endpoint

**Mục tiêu:** Cho Lambda trong private subnet truy cập S3 mà không cần NAT Gateway, quan sát route table thay đổi.

### Bước 5.1 — Tạo S3 Bucket Test

1. **S3 Console** → **Create bucket**
   - Name: `workshop-vpc-endpoint-test-[random]` (tên phải unique)
   - Region: `ap-southeast-1`
   - Block all public access: ✅ (giữ nguyên)

### Bước 5.2 — Tạo S3 Gateway Endpoint

1. **VPC Console** → **Endpoints** → **Create endpoint**
   - Service category: **AWS services**
   - Search: `s3` → chọn `com.amazonaws.ap-southeast-1.s3` loại **Gateway**
   - VPC: `workshop-vpc`
   - Route tables: chọn **`workshop-rt-private`** và **`workshop-rt-isolated`**
2. Click **Create endpoint**

### Bước 5.3 — Quan Sát Route Table Thay Đổi

1. Vào **Route Tables** → `workshop-rt-private` → tab **Routes**
2. Bạn sẽ thấy route mới được tự động thêm vào:

| Destination | Target |
|-------------|--------|
| `10.0.0.0/16` | local |
| `0.0.0.0/0` | nat-gateway-id |
| `pl-6ca54005` (S3) | vpce-xxxxxxxx |  ← **mới xuất hiện** |

> **Checkpoint:** Route này được thêm tự động — đây là cách Gateway Endpoint hoạt động, khác với Interface Endpoint (tạo ENI).

### Bước 5.4 — Test Lambda Đọc S3

Cập nhật Lambda IAM role để có quyền S3, sau đó test:

1. **Lambda** → `workshop-lambda-vpc` → tab **Configuration** → **Permissions**
2. Click vào Execution role → **Add permissions** → **Attach policies** → thêm `AmazonS3ReadOnlyAccess`

3. Update Lambda code:

```python
import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    try:
        # List buckets để test S3 connectivity
        response = s3.list_buckets()
        bucket_names = [b['Name'] for b in response['Buckets']]
        return {
            'statusCode': 200,
            'body': f"S3 access: YES — Buckets: {bucket_names}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"S3 access: NO — Error: {str(e)}"
        }
```

4. **Test** → chạy → kết quả phải là `S3 access: YES`

> **Thử thêm (Intermediate):** Xóa NAT Gateway route khỏi private subnet route table, giữ S3 Endpoint → Lambda vẫn access được S3 nhưng không ra internet được. Đây chứng minh S3 Endpoint không cần NAT GW.

---

## Lab 6 — End-to-End Verification

**Mục tiêu:** Kiểm tra toàn bộ flow đã build, đọc VPC Flow Logs để hiểu traffic.

### Bước 6.1 — Enable VPC Flow Logs

1. **VPC Console** → `workshop-vpc` → tab **Flow logs** → **Create flow log**
   - Filter: **All**
   - Destination: **CloudWatch Logs**
   - Log group: tạo mới `/vpc/workshop-flowlogs`
   - IAM role: tạo mới (AWS tự suggest)

### Bước 6.2 — Chạy Các Test Cases

Chạy Lambda với các test cases sau và ghi lại kết quả:

| Test | Mô tả | Kết quả mong đợi |
|------|-------|-----------------|
| TC1 | Lambda gọi `https://httpbin.org/ip` | ✅ Thành công (qua NAT GW) |
| TC2 | Lambda list S3 buckets | ✅ Thành công (qua S3 Endpoint) |
| TC3 | Xóa NAT route → gọi internet | ❌ Timeout |
| TC4 | Xóa NAT route → list S3 | ✅ Vẫn thành công (S3 Endpoint không cần NAT) |

### Bước 6.3 — Đọc Flow Logs

1. **CloudWatch** → **Log groups** → `/vpc/workshop-flowlogs`
2. Tìm log entries sau khi chạy Lambda
3. Format của flow log:

```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```

> **Quan sát:** Traffic đến S3 (prefix list) sẽ không đi qua NAT GW IP — nó đi thẳng qua VPC Endpoint. Traffic đến internet sẽ thấy NAT GW IP là intermediate hop.

---

## Cleanup — Quan Trọng!

**Xóa theo thứ tự này** để tránh lỗi dependency:

1. ❌ Lambda function `workshop-lambda-vpc`
2. ❌ VPC Endpoint (S3 Gateway)
3. ❌ NAT Gateway `workshop-nat` ← **xóa ngay để ngừng tính phí**
4. ❌ Release Elastic IP (sau khi NAT GW đã xóa)
5. ❌ S3 bucket test
6. ❌ Security Groups (3 cái)
7. ❌ Route Tables (3 cái custom — không xóa default)
8. ❌ Subnets (3 cái)
9. ❌ Internet Gateway (detach trước, rồi delete)
10. ❌ VPC `workshop-vpc`

> ⚠️ **NAT Gateway là thứ tốn tiền nhất** (~$0.045/giờ). Xóa ngay sau khi xong Lab 4 nếu không tiếp tục.

---

## Tổng Kết — Những Gì Đã Thực Hành

| Kiến thức đã học | Đã hands-on ở Lab |
|---|---|
| CIDR notation, subnet sizing | Lab 1 |
| 3 loại subnet (Public/Private/Isolated) | Lab 1, 2 |
| Internet Gateway | Lab 1, 2 |
| NAT Gateway — đặt ở public, phục vụ private | Lab 2 |
| Route Table của từng loại subnet | Lab 2 |
| Security Group — stateful, allow only, SG-to-SG rule | Lab 3 |
| NACL — stateless, ephemeral ports | Lab 3 |
| ENI — Lambda tạo ENI khi vào VPC | Lab 4 |
| Lambda trong VPC vs ngoài VPC | Lab 4 |
| S3 Gateway Endpoint — route table tự thêm | Lab 5 |
| S3 Endpoint không cần NAT GW | Lab 5, 6 |
| VPC Flow Logs — đọc traffic | Lab 6 |
