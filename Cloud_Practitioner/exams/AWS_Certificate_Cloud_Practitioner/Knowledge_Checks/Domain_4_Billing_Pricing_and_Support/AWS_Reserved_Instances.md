# AWS Reserved Instances/Capacity

**Date**: 2026-05-11

## Khái niệm

**Reserved = Đặt trước** tài nguyên cho **1 hoặc 3 năm** → **Giảm giá** so với On-Demand (lên đến 75%)

## Dịch vụ HỖ TRỢ Reservations ✅

1. **EC2 Reserved Instances** - Đặt trước EC2 instances
2. **DynamoDB Reserved Capacity** - Đặt trước read/write throughput
3. **ElastiCache Reserved Nodes** - Đặt trước cache nodes (Redis/Memcached)
4. **RDS Reserved Instances** - Đặt trước database instances (Aurora, MySQL, MariaDB, PostgreSQL, Oracle, SQL Server)
5. **Redshift Reserved Nodes** - Đặt trước data warehouse nodes

## Dịch vụ KHÔNG HỖ TRỢ Reservations ❌

- **Lambda** - Serverless, trả theo compute time
- **S3** - Object storage, trả theo dung lượng
- **DocumentDB** - Managed document database

## 3 loại thanh toán

- **No Upfront** - Không trả trước, trả hàng tháng
- **Partial Upfront** - Trả trước 1 phần, còn lại trả hàng tháng
- **All Upfront** - Trả trước toàn bộ (giảm giá nhiều nhất)

## Khi nào dùng Reserved?

✅ Workload ổn định, chạy 24/7  
✅ Biết trước nhu cầu 1-3 năm  
✅ Muốn tiết kiệm chi phí  

❌ Workload thay đổi nhiều → Dùng On-Demand/Spot
