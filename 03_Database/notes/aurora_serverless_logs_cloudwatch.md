# Aurora Serverless (MySQL): Audit & Đẩy Log Sang CloudWatch Logs
**Chủ đề (Topic):** Database
**Dịch vụ (Service):** Amazon Aurora Serverless (MySQL-compatible), Amazon CloudWatch Logs
**Ngữ cảnh (Context):** Câu hỏi exam SAA/SOA (audit database activity cua Aurora Serverless)

---

## 0. Câu Hỏi Và Đáp Án

> E-commerce dùng Aurora Serverless (MySQL-compatible), muốn **audit database activity** bằng cách thu thập và đẩy log lên **CloudWatch Logs**. Cần cấu hình gì?

**Đáp án đúng:** Với MySQL-compatible, bật **slow query log, general log, hoặc audit log** để thấy hoạt động database (rồi publish sang CloudWatch).

---

## 1. Vì Sao Không Xem Log Trực Tiếp Trên RDS Console Được

Aurora Serverless (v1) nối tới một **proxy fleet** gồm các DB instance tự scale lên/xuống theo tải. Không có một DB instance cố định đứng yên để chứa file log.

Hệ quả:
- **Không** mở/tải log trực tiếp trên RDS Console như Aurora provisioned.
- Giải pháp: cấu hình Aurora **publish log sang CloudWatch Logs**, rồi xem và tải log ở CloudWatch.

```
Aurora Serverless (proxy fleet, scale tu dong)
   không có instance cố định để chứa file log
            │  (cấu hình publish)
            ▼
   CloudWatch Logs  ──►  xem / tải / query (Logs Insights)
```

---

## 2. Điểm Bẫy Quan Trọng: KHÔNG Tự Động, Phải Bật

Aurora Serverless **CÓ** đẩy log lên CloudWatch, nhưng **không mặc định**. Phải cấu hình trước. Đây là chỗ phân biệt 2 phương án nghe giống nhau:

| Phát biểu | Đúng/Sai |
| :--- | :--- |
| "Tích hợp sẵn CloudWatch, log tự gửi lên tự động" | **Sai** (sai ở chữ tự động/mặc định) |
| "Bật slow query / general / audit log rồi log mới lên CloudWatch" | **Đúng** |

---

## 3. Cách Bật (2 Bước)

### Bước 1: Sửa Custom DB Cluster Parameter Group
Với **Aurora Serverless v1**, bật log bằng cách set tham số trong **custom parameter group** (không dùng được màn hình "Log exports" như provisioned). Các tham số MySQL (xác thực từ docs):

| Tham số | Ý nghĩa |
| :--- | :--- |
| `slow_query_log` | `1` = bật slow query log. Mặc định `0`. |
| `long_query_time` | Ngưỡng giây để một query bị coi là chậm (0 tới 31536000). |
| `log_queries_not_using_indexes` | `1` = log query không dùng index vào slow query log. |
| `general_log` | `1` = bật general log (mọi câu lệnh client gửi tới). Mặc định `0`. |
| `server_audit_logging` | `1` = bật audit log. |
| `server_audit_events` | Danh sách sự kiện audit: `CONNECT`, `QUERY`, `QUERY_DCL`, `QUERY_DDL`, `QUERY_DML`, `TABLE`. |

### Bước 2: Publish Sang CloudWatch
- **Aurora Serverless v1**: sau khi bật tham số, log tự publish lên CloudWatch Logs.
- **Aurora Serverless v2 / provisioned**: giống RDS thường, chọn log types ở **Log exports** khi Modify cluster, hoặc dùng CLI:

```bash
aws rds modify-db-cluster \
  --db-cluster-identifier aurora-mysql-01 \
  --cloudwatch-logs-export-configuration '{"EnableLogTypes":["audit","error","general","slowquery"]}'
```

> [!IMPORTANT]
> Phân biệt v1 vs v2: **Serverless v1** bật log qua **cluster parameter group** (không có nút Log exports). **Serverless v2** hoạt động gần như provisioned, dùng `--cloudwatch-logs-export-configuration` / màn hình Log exports bình thường. Câu hỏi exam cổ điển thường nói về v1.

---

## 4. Ba Loại Log MySQL (nhớ để chọn đúng)

| Loại log | Ghi gì | Dùng để |
| :--- | :--- | :--- |
| **slow query log** | Query chạy chậm quá `long_query_time` | Tối ưu performance |
| **general log** | Mọi câu lệnh client gửi tới DB | Debug, xem app gửi gì |
| **audit log** (`server_audit_logging`) | Kết nối, truy cập, thao tác (CONNECT/QUERY/DDL/DML...) | **Audit / compliance** (đúng yêu cầu câu hỏi) |

---

## 5. Vì Sao Các Phương Án Khác Bị Loại

| Phương án sai | Lý do |
| :--- | :--- |
| Xem log trực tiếp trên RDS Console | Không có DB instance cố định chứa file log -> Console không cho mở trực tiếp. |
| Tích hợp sẵn, log tự gửi lên CloudWatch | Không mặc định. Phải bật log trong parameter group trước. |
| Không xem được, phải gọi AWS Support | Sai hoàn toàn. Tự cấu hình publish sang CloudWatch được. |

---

## 6. Memory Tip (exam)

> Aurora đẩy log lên CloudWatch Logs **không bao giờ mặc định**. Luôn: (1) bật loại log (parameter group với Serverless v1, hoặc Log exports với v2/provisioned), (2) log mới chảy vào CloudWatch.
> - Thấy đáp án nói log "tự động/sẵn sàng ngay" -> **bẫy**.
> - Serverless v1 không xem log trên RDS Console (proxy fleet, không instance cố định) -> xem ở **CloudWatch**.
> - MySQL nhớ bộ 3: **slow query / general / audit**. Yêu cầu **audit / compliance** -> chọn **audit log** (`server_audit_logging` + `server_audit_events`).

---

## Nguồn (Sources)
- [Managing Aurora Serverless DB clusters - Logging (tham so parameter group)](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-administration.html)
- [Publishing Amazon Aurora MySQL logs to Amazon CloudWatch Logs (CLI modify-db-cluster)](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.CloudWatch.html)
- [AWS re:Post - Enable and view Aurora Serverless logs](https://aws.amazon.com/premiumsupport/knowledge-center/aurora-serverless-logs-enable-view/)
