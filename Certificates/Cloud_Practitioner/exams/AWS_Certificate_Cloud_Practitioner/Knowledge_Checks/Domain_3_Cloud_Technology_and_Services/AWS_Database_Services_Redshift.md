# AWS Database Services

**Date**: 2026-05-11

## Redshift ✅

**AWS Database Service** - Fully-managed **data warehouse**

**Đặc điểm**:
- Petabyte-scale cloud data warehouse
- Dùng cho **large scale data storage and analysis**
- OLAP (Online Analytical Processing)
- Columnar storage

## Các dịch vụ KHÔNG PHẢI Database

### ❌ **Glue**
- **ETL service** (Extract, Transform, Load)
- Dùng để prepare và load data cho analytics
- KHÔNG phải database

### ❌ **Storage Gateway**
- **Hybrid cloud storage service**
- Kết nối on-premises với AWS Cloud
- KHÔNG phải database

### ❌ **Database Migration Service (DMS)**
- **Migration service**
- Dùng để migrate databases
- KHÔNG phải database, chỉ là tool để migrate

## AWS Database Services (Full list)

- **RDS** - Relational databases (MySQL, PostgreSQL, Oracle, SQL Server, MariaDB)
- **Aurora** - AWS proprietary relational database
- **DynamoDB** - NoSQL database
- **Redshift** - Data warehouse ✅
- **ElastiCache** - In-memory cache (Redis, Memcached)
- **Neptune** - Graph database
- **DocumentDB** - Document database (MongoDB-compatible)
- **Keyspaces** - Cassandra-compatible database
- **Timestream** - Time series database

## Key Point

**Redshift = Data warehouse = Database service** ✅

Glue, Storage Gateway, DMS = **KHÔNG phải database**
