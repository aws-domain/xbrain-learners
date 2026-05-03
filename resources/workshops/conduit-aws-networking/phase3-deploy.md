# Phase 3 — Deploy từng Layer

> **Thời gian:** ~2.5 giờ  
> **Mục tiêu:** Deploy RDS, Backend EC2, Frontend EC2 vào đúng subnet  
> **Prerequisite:** Phase 2 hoàn thành, `source ~/conduit-ids.sh`

---

## Tổng quan kiến trúc sẽ deploy

```
Internet
    │ HTTP :80
    ▼
[Frontend EC2 — Public Subnet 10.0.1.0/24]
  Nginx serve static files + proxy /api/ → Backend
    │ :3001 (private network)
    ▼
[Backend EC2 — Private Subnet 10.0.2.0/24]
  Node.js + Express + PM2
    │ :3306 (private network)
    ▼
[RDS MariaDB — Isolated Subnet 10.0.3.0/24 + 10.0.4.0/24]
```

**Lưu ý quan trọng về repo:**
Repo `TonyMckes/conduit-realworld-example-app` chứa cả `backend/` và `frontend/` trong cùng 1 repo. Cấu trúc:
```
conduit-realworld-example-app/
├── backend/        ← Node.js API (port 3001)
│   ├── index.js    ← entry point
│   ├── config/config.js  ← đọc PROD_DB_* từ env
│   └── ...
└── frontend/       ← React + Vite (build ra static files)
    └── src/services/  ← gọi API qua relative URL /api/*
```

---

## 3.1 Deploy RDS MariaDB

RDS vào isolated subnet — không có internet access.

### Tạo DB Subnet Group

RDS cần subnet group với ít nhất 2 AZ:

<details>
<summary>📟 CLI</summary>

```bash
aws rds create-db-subnet-group \
  --db-subnet-group-name conduit-db-subnet-group \
  --db-subnet-group-description "Subnet group for Conduit RDS" \
  --subnet-ids $ISOLATED_SUBNET_1A $ISOLATED_SUBNET_1B \
  --tags Key=Name,Value=conduit-db-subnet-group \
  --region ap-southeast-1
```

</details>

<details>
<summary>🖥️ Console</summary>

1. Vào **RDS Console** → **Subnet groups** → **Create DB subnet group**
2. Điền:
   - Name: `conduit-db-subnet-group`
   - Description: `Subnet group for Conduit RDS`
   - VPC: chọn `conduit-vpc`
3. Phần **Add subnets**:
   - AZ `ap-southeast-1a` → chọn subnet `10.0.3.0/24` (isolated-1a)
   - AZ `ap-southeast-1b` → chọn subnet `10.0.4.0/24` (isolated-1b)
4. Click **Create**

</details>

### Tạo RDS Instance

<details>
<summary>📟 CLI</summary>

```bash
aws rds create-db-instance \
  --db-instance-identifier conduit-mariadb \
  --db-instance-class db.t3.micro \
  --engine mariadb \
  --master-username conduit_admin \
  --master-user-password "YourPassword123!" \
  --db-subnet-group-name conduit-db-subnet-group \
  --vpc-security-group-ids $SG_DATABASE \
  --no-publicly-accessible \
  --allocated-storage 20 \
  --storage-type gp2 \
  --backup-retention-period 1 \
  --tags Key=Name,Value=conduit-mariadb \
  --region ap-southeast-1
```

</details>

<details>
<summary>🖥️ Console</summary>

1. Vào **RDS Console** → **Databases** → **Create database**
2. **Engine:** MariaDB
3. **Templates:** Free tier
4. **DB instance identifier:** `conduit-mariadb`
5. **Master username:** `conduit_admin`
6. **Master password:** đặt password, nhớ lưu lại
7. **DB instance class:** db.t3.micro
8. **Storage:** 20 GiB, gp2
9. **Connectivity:**
   - VPC: `conduit-vpc`
   - DB subnet group: `conduit-db-subnet-group`
   - Public access: **No** ← quan trọng
   - VPC security group: chọn `database-sg`, bỏ `default`
10. Click **Create database**

> ⚠️ Đợi ~5-10 phút cho đến khi Status chuyển sang **Available**.

**Lấy endpoint sau khi available:**
RDS Console → chọn instance → tab **Connectivity & security** → copy **Endpoint**

```bash
echo "export RDS_ENDPOINT=<endpoint-vừa-copy>" >> ~/conduit-ids.sh
source ~/conduit-ids.sh
```

</details>

### Tạo database bên trong RDS

> ⚠️ **Lưu ý quan trọng:** Tạo RDS instance **không** tự động tạo database bên trong. Phải tạo thủ công sau khi instance available.

Sau khi deploy Backend EC2 và SSH vào được, chạy:

```bash
mysql -h $RDS_ENDPOINT -u conduit_admin -p'YourPassword123!' \
  -e "CREATE DATABASE IF NOT EXISTS conduit;"

# Verify
mysql -h $RDS_ENDPOINT -u conduit_admin -p'YourPassword123!' \
  -e "SHOW DATABASES;"
```

---

## 3.2 Tạo Key Pair để SSH

<details>
<summary>📟 CLI</summary>

```bash
aws ec2 create-key-pair \
  --key-name conduit-key \
  --query "KeyMaterial" \
  --output text \
  --region ap-southeast-1 > ~/.ssh/conduit-key.pem

chmod 400 ~/.ssh/conduit-key.pem
```

</details>

<details>
<summary>🖥️ Console</summary>

1. Vào **EC2 Console** → **Key Pairs** → **Create key pair**
2. Name: `conduit-key`, format: `.pem`
3. File tự động download → di chuyển vào `.ssh`:

```bash
mkdir -p ~/.ssh
mv ~/Downloads/conduit-key.pem ~/.ssh/conduit-key.pem
chmod 400 ~/.ssh/conduit-key.pem
```

</details>

---

## 3.3 Deploy Backend EC2 (Private Subnet)

### User Data Script cho Backend

> **Tại sao cần User Data?** EC2 chạy script này tự động khi boot lần đầu — thay vì SSH vào và gõ từng lệnh thủ công.

Paste đoạn script này vào ô **User data** khi tạo EC2 trên Console:

```bash
#!/bin/bash
set -e

# Update system
yum update -y

# Install Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs git

# Install MariaDB client (để test connection)
yum install -y mariadb105

# Clone repo (chứa cả backend và frontend)
cd /home/ec2-user
git clone https://github.com/TonyMckes/conduit-realworld-example-app.git conduit-backend

# Install dependencies ở root (node_modules dùng chung)
cd conduit-backend
npm install

# Install thêm mysql2 — Sequelize dùng để kết nối MariaDB
# (package 'mariadb' không dùng được vì ESM incompatibility)
npm install mysql2

# Install PM2 để chạy app như service
npm install -g pm2

echo "Backend setup complete."
```

> **Lưu ý:** Script này chỉ cài dependencies. Cấu hình `.env` sẽ làm ở bước tiếp theo sau khi SSH vào.

### Launch Backend EC2

<details>
<summary>🖥️ Console</summary>

1. **EC2 Console** → **Launch instances**
2. **Name:** `conduit-backend`
3. **AMI:** Amazon Linux 2023 (Free tier eligible)
4. **Instance type:** t2.micro
5. **Key pair:** `conduit-key`
6. **Network settings** → Edit:
   - VPC: `conduit-vpc`
   - Subnet: `10.0.2.0/24` (private subnet)
   - Auto-assign public IP: **Disable**
   - Security group: `backend-sg`
7. **Advanced details** → **User data** → paste script trên
8. **Launch instance**

**Lưu Private IP:**
EC2 Console → instance `conduit-backend` → tab Details → copy **Private IPv4 address**

```bash
echo "export BACKEND_INSTANCE=<instance-id>" >> ~/conduit-ids.sh
echo "export BACKEND_PRIVATE_IP=<private-ip>" >> ~/conduit-ids.sh
source ~/conduit-ids.sh
```

</details>

### Cấu hình Backend — tạo file .env

SSH vào Frontend EC2 (Bastion), rồi từ đó SSH vào Backend:

```bash
# Từ máy local → Frontend
ssh -i ~/.ssh/conduit-key.pem ec2-user@$FRONTEND_PUBLIC_IP

# Copy key lên Frontend để dùng làm Bastion
scp -i ~/.ssh/conduit-key.pem ~/.ssh/conduit-key.pem \
  ec2-user@$FRONTEND_PUBLIC_IP:~/.ssh/

# Từ Frontend → Backend
ssh -i ~/.ssh/conduit-key.pem ec2-user@$BACKEND_PRIVATE_IP
```

Trên Backend EC2, tạo file `.env` trong đúng thư mục:

```bash
# QUAN TRỌNG: file .env phải nằm trong backend/, không phải root
cat > /home/ec2-user/conduit-backend/backend/.env << 'EOF'
NODE_ENV=production
PORT=3001
PROD_DB_USERNAME=conduit_admin
PROD_DB_PASSWORD=YourPassword123!
PROD_DB_NAME=conduit
PROD_DB_HOSTNAME=<RDS_ENDPOINT>
PROD_DB_DIALECT=mysql
JWT_SECRET=your-super-secret-jwt-key-change-this
EOF
```

> **Tại sao `PROD_DB_*` thay vì `DATABASE_URL`?**
> Repo này dùng Sequelize với `config/config.js` đọc từng biến riêng lẻ theo `NODE_ENV`. Không dùng connection string kiểu `DATABASE_URL`.

> **Tại sao `PROD_DB_DIALECT=mysql` thay vì `mariadb`?**
> Package `mariadb` mới dùng ES Module (ESM) không tương thích với `require()` của CommonJS. Package `mysql2` tương thích với MariaDB và không có vấn đề này.

> **Tại sao không có `PROD_DB_LOGGING`?**
> Sequelize expect `logging` là function hoặc boolean `false`. Khi đọc từ `.env`, tất cả đều là string — `"false"` không phải `false` → crash. Bỏ biến này để Sequelize dùng default.

### Start Backend

```bash
cd /home/ec2-user/conduit-backend/backend

# Start với PM2
pm2 start index.js --name conduit-backend

# Verify đang chạy
pm2 logs conduit-backend --lines 5 --out
# Phải thấy:
# Server running on http://localhost:3001
# Connection with production database has been established.

# Auto-start khi reboot
pm2 save
pm2 startup
# Copy và chạy lệnh sudo mà pm2 startup in ra
```

### Verify Backend hoạt động

```bash
curl http://localhost:3001/api/articles
# Phải trả về JSON (có thể là empty array lúc đầu)
```

---

## 3.4 Deploy Frontend EC2 (Public Subnet)

### User Data Script cho Frontend

> **Lưu ý về Vite:** Frontend dùng Vite (không phải Create React App). Build output là `dist/` thay vì `build/`. Vite yêu cầu **Node.js 20+**.

```bash
#!/bin/bash
set -e

# Update system
yum update -y

# Install Node.js 20 (Vite yêu cầu Node 20+, không dùng được Node 18)
curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
yum install -y nodejs git nginx

# Clone repo
cd /home/ec2-user
git clone https://github.com/TonyMckes/conduit-realworld-example-app.git conduit-app

# Fix permission (User Data chạy với root, cần chown về ec2-user)
chown -R ec2-user:ec2-user /home/ec2-user/conduit-app

# Install dependencies
cd conduit-app
npm install

# Build frontend
# QUAN TRỌNG: Frontend dùng relative URL (/api/*) nên KHÔNG cần VITE_API_URL
# Nginx sẽ proxy /api/ đến Backend
cd frontend
npm run build

# Copy build files to Nginx
cp -r dist/* /usr/share/nginx/html/

# Configure Nginx với proxy đến Backend
# QUAN TRỌNG: phải có location /api/ để proxy đến Backend
# Frontend gọi API qua relative URL → browser gọi http://<frontend-ip>/api/*
# → Nginx proxy đến Backend private IP
cat > /etc/nginx/conf.d/conduit.conf << 'NGINX'
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
        proxy_pass http://BACKEND_PRIVATE_IP:3001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX

# Thay BACKEND_PRIVATE_IP bằng IP thực
sed -i "s/BACKEND_PRIVATE_IP/<BACKEND_PRIVATE_IP>/" /etc/nginx/conf.d/conduit.conf

# Start Nginx
systemctl enable nginx
systemctl start nginx

echo "Frontend setup complete."
```

> **Thay `<BACKEND_PRIVATE_IP>`** bằng IP thực của Backend EC2 (ví dụ: `10.0.2.175`) trước khi paste vào User data.

### Launch Frontend EC2

<details>
<summary>🖥️ Console</summary>

1. **EC2 Console** → **Launch instances**
2. **Name:** `conduit-frontend`
3. **AMI:** Amazon Linux 2023 (Free tier eligible)
4. **Instance type:** t2.micro
5. **Key pair:** `conduit-key`
6. **Network settings** → Edit:
   - VPC: `conduit-vpc`
   - Subnet: `10.0.1.0/24` (public subnet)
   - Auto-assign public IP: **Enable** ← khác với Backend
   - Security group: `frontend-sg`
7. **Advanced details** → **User data** → paste script trên (đã thay Backend IP)
8. **Launch instance**

**Lưu Public IP:**
```bash
echo "export FRONTEND_INSTANCE=<instance-id>" >> ~/conduit-ids.sh
echo "export FRONTEND_PUBLIC_IP=<public-ip>" >> ~/conduit-ids.sh
source ~/conduit-ids.sh
```

</details>

### Verify Frontend hoạt động

Đợi ~5 phút cho User Data chạy xong, sau đó:

```bash
# Kiểm tra User Data đã chạy xong chưa
ssh -i ~/.ssh/conduit-key.pem ec2-user@$FRONTEND_PUBLIC_IP
sudo tail -5 /var/log/cloud-init-output.log
# Phải thấy: "Frontend setup complete."

# Kiểm tra Nginx
systemctl status nginx

# Kiểm tra Nginx config có proxy /api/ không
cat /etc/nginx/conf.d/conduit.conf
```

Mở browser: `http://<FRONTEND_PUBLIC_IP>` → thấy giao diện Conduit.

---

## 3.5 Troubleshooting thực tế

Các lỗi hay gặp khi deploy lần đầu:

### Lỗi: `Dialect needs to be explicitly supplied`
**Nguyên nhân:** File `.env` không được đọc hoặc biến `PROD_DB_DIALECT` chưa set.
**Fix:** Kiểm tra file `.env` nằm đúng trong `backend/` (không phải root repo), và có đủ các biến `PROD_DB_*`.

### Lỗi: `options.logging is not a function`
**Nguyên nhân:** `PROD_DB_LOGGING=false` trong `.env` là string `"false"`, không phải boolean.
**Fix:** Xóa dòng `PROD_DB_LOGGING` khỏi `.env`.

### Lỗi: `Please install mariadb package manually`
**Nguyên nhân:** Sequelize dialect `mariadb` cần package `mariadb` nhưng package này dùng ESM không tương thích.
**Fix:** Dùng `PROD_DB_DIALECT=mysql` và cài `npm install mysql2`.

### Lỗi: `Unknown database 'conduit'`
**Nguyên nhân:** RDS instance đã tạo nhưng database `conduit` bên trong chưa được tạo.
**Fix:**
```bash
mysql -h $RDS_ENDPOINT -u conduit_admin -p'YourPassword' \
  -e "CREATE DATABASE IF NOT EXISTS conduit;"
```

### Lỗi: Trang trắng, không có data
**Nguyên nhân:** Frontend dùng relative URL `/api/*` nhưng Nginx chưa có `location /api/` để proxy đến Backend.
**Fix:** Thêm proxy config vào Nginx:
```bash
sudo tee /etc/nginx/conf.d/conduit.conf << 'NGINX'
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
        proxy_pass http://<BACKEND_PRIVATE_IP>:3001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX
sudo nginx -t && sudo systemctl reload nginx
```

### Lỗi: `ERR_REQUIRE_ESM` với package mariadb
**Nguyên nhân:** Package `mariadb` mới dùng ES Module, không tương thích với CommonJS `require()`.
**Fix:** Dùng `mysql2` thay thế — tương thích với MariaDB và không có vấn đề ESM.

---

## 3.6 Setup Monitoring — CloudWatch

### CloudWatch Agent trên EC2

```bash
# Cài trên từng EC2
sudo yum install -y amazon-cloudwatch-agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

> CloudWatch Agent cần IAM role với policy `CloudWatchAgentServerPolicy`.

### CloudWatch Alarms

```bash
# CPU cao — Frontend
aws cloudwatch put-metric-alarm \
  --alarm-name "conduit-frontend-cpu-high" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value=$FRONTEND_INSTANCE \
  --region ap-southeast-1

# RDS Connections cao
aws cloudwatch put-metric-alarm \
  --alarm-name "conduit-rds-connections-high" \
  --metric-name DatabaseConnections \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=DBInstanceIdentifier,Value=conduit-mariadb \
  --region ap-southeast-1
```

---

## 3.7 Checklist Phase 3

- [ ] RDS MariaDB đang chạy trong isolated subnet, không có public IP
- [ ] Database `conduit` đã được tạo bên trong RDS
- [ ] Backend EC2 trong private subnet, không có public IP
- [ ] Backend kết nối được RDS — log thấy "Connection with production database has been established"
- [ ] PM2 đang chạy `conduit-backend` với status `online`
- [ ] Frontend EC2 trong public subnet, có public IP
- [ ] Nginx đang chạy với `location /api/` proxy đến Backend
- [ ] Website accessible từ browser qua Frontend public IP
- [ ] Có thể đăng ký tài khoản và đăng nhập

**Câu hỏi tự kiểm tra:**
1. Tại sao Backend không có public IP nhưng vẫn ra được internet (để pull npm packages)?
2. Tại sao Frontend dùng Nginx proxy thay vì gọi thẳng Backend IP từ browser?
3. Tại sao phải tạo database `conduit` thủ công sau khi tạo RDS?
4. Tại sao dùng `mysql2` thay vì `mariadb` package?
5. File `.env` phải đặt ở đâu và tại sao?
