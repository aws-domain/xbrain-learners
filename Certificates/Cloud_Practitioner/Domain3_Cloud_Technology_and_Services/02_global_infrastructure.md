# Task 3.2 — AWS Global Infrastructure

> **Exam weight:** Domain 3 = 34% of scored content

## AWS Global Infrastructure Components

### Regions
- **Khu vực địa lý** chứa nhiều data centers
- Mỗi Region hoàn toàn **độc lập** với các Region khác
- Hiện có **30+ Regions** trên toàn thế giới
- Ví dụ: us-east-1 (N. Virginia), ap-southeast-1 (Singapore), eu-west-1 (Ireland)

**Cách chọn Region:**
- **Compliance** — Dữ liệu phải ở trong quốc gia/khu vực cụ thể
- **Latency** — Chọn Region gần người dùng nhất
- **Service availability** — Không phải service nào cũng có ở mọi Region
- **Pricing** — Giá có thể khác nhau giữa các Regions

### Availability Zones (AZs)
- Mỗi Region có **2-6 AZs** (thường là 3)
- Mỗi AZ là **một hoặc nhiều data centers** riêng biệt
- AZs trong cùng Region kết nối với nhau qua **high-speed private network**
- AZs **không chia sẻ single points of failure** (điện, cooling, network riêng biệt)
- Ví dụ: us-east-1a, us-east-1b, us-east-1c

**Tại sao dùng nhiều AZs?**
- **High availability** — Nếu một AZ down, AZ khác vẫn chạy
- **Fault tolerance** — Không có single point of failure
- **Disaster recovery** — Dữ liệu được replicate giữa AZs

### Edge Locations
- **Điểm phân phối nội dung** gần người dùng cuối
- Nhiều hơn Regions (400+ edge locations)
- Dùng bởi: **Amazon CloudFront** (CDN), **AWS Route 53** (DNS)
- Giảm latency bằng cách cache content gần người dùng

---

## High Availability với Multiple AZs

```
Region: us-east-1
├── AZ: us-east-1a  ← EC2 instance + RDS Primary
├── AZ: us-east-1b  ← EC2 instance + RDS Standby
└── AZ: us-east-1c  ← EC2 instance
         ↑
    Load Balancer phân phối traffic
```

- **Multi-AZ deployment** = best practice cho production
- Nếu us-east-1a down → traffic tự động chuyển sang us-east-1b và 1c
- RDS Multi-AZ: automatic failover trong vài phút

---

## Multiple Regions Use Cases

| Use Case | Giải thích |
|----------|-----------|
| **Disaster Recovery** | Nếu toàn bộ Region down, Region khác tiếp tục phục vụ |
| **Business Continuity** | Đảm bảo business không bị gián đoạn |
| **Low Latency** | Phục vụ người dùng ở nhiều châu lục |
| **Data Sovereignty** | Dữ liệu phải ở trong biên giới quốc gia cụ thể |

---

## Edge Locations và CloudFront

**Amazon CloudFront** là CDN (Content Delivery Network) của AWS:
- Cache static content (images, videos, HTML) tại edge locations
- Người dùng nhận content từ edge location gần nhất
- Giảm latency đáng kể cho global users
- Tích hợp với S3, EC2, ALB, Lambda@Edge

---

## AWS Local Zones
- Mở rộng AWS infrastructure đến **thành phố lớn** không có Region
- Giảm latency cho ứng dụng cần < 10ms
- Ví dụ: Los Angeles, Boston, Houston

## AWS Wavelength
- Đưa AWS compute đến **mạng 5G** của telecom providers
- Ultra-low latency cho mobile applications

## AWS Outposts
- Đưa **AWS infrastructure vào data center của bạn**
- Chạy AWS services on-premises
- Dùng cho: compliance, latency, data residency requirements

---

## Exam Tips

- Region = địa lý; AZ = data center(s) trong Region; Edge Location = cache point
- AZs không share single points of failure
- Multi-AZ = high availability; Multi-Region = disaster recovery
- CloudFront dùng Edge Locations, không phải AZs
- Số lượng: Edge Locations > AZs > Regions
