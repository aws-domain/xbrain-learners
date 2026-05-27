# EC2 Placement Groups

## Vấn đề gốc rễ

Khi launch EC2 bình thường, AWS tự phân bổ instance lên phần cứng — bạn không kiểm soát được các instance có nằm gần hay xa nhau. Điều này gây ra 2 nhóm vấn đề đối lập:

- **Cần gần nhau**: Ứng dụng HPC/ML cần trao đổi dữ liệu liên tục → latency cao → chậm → tốn tiền
- **Cần xa nhau**: Ứng dụng critical có replica → nếu cùng rack → rack hỏng → tất cả sập
- **Cần cả hai ở scale lớn**: Distributed system (Kafka, Cassandra) → không thể dùng giải pháp đơn giản

---

## 3 Loại Placement Group

### 1. Cluster — "Gần nhau nhất có thể"
- Tất cả instance cùng **một rack, một AZ**
- Băng thông lên đến **10 Gbps** giữa các instance
- Rủi ro: rack hỏng → tất cả bị ảnh hưởng
- **Use case**: HPC, ML training, Big Data (Hadoop)

### 2. Spread — "Xa nhau nhất có thể"
- Mỗi instance trên **rack vật lý riêng biệt** (khác nguồn điện & mạng)
- Giới hạn: **tối đa 7 instance/AZ**
- Có thể trải qua nhiều AZ
- **Use case**: Primary/Secondary database, ứng dụng critical cần high availability

### 3. Partition — "Scale lớn, isolate theo nhóm"
- Chia thành nhiều **partition** (tối đa 7 partition/AZ), mỗi partition là tập rack riêng
- Không giới hạn số instance mỗi partition
- **Use case**: Kafka, Cassandra, HDFS — distributed system lớn cần fault isolation

---

## So sánh

| | Cluster | Spread | Partition |
|---|---|---|---|
| Mục tiêu | Low latency | High availability | Fault isolation at scale |
| Giới hạn instance | Không | 7/AZ | Không (7 partition/AZ) |
| Trải qua nhiều AZ | ❌ | ✅ | ✅ |
| Rủi ro phần cứng | Cao | Thấp nhất | Trung bình |

---

## Lợi ích thực sự

| Bạn muốn gì | Giải pháp |
|---|---|
| Giảm latency → tiết kiệm chi phí compute | Cluster |
| Đảm bảo SLA / uptime production | Spread |
| Scale lớn + kiểm soát fault domain | Partition |

---

## Lưu ý cho kỳ thi

- Placement Group **không tốn phí** thêm
- Không thể **merge** 2 placement group
- Instance có thể **move** vào group khi đang **stopped**
- Cluster group nên dùng cùng **instance type** để đạt bandwidth tối đa
