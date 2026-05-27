# Topic 04: Networking Troubleshooting — Khắc Phục Sự Cố VPC Peering

## 📌 Tổng quan cốt lõi (Core Concepts)
- **VPC Peering:** Kết nối mạng giữa hai VPC, cho phép truyền thông suốt qua các dải IP Private (IPv4 hoặc IPv6) như thể chúng nằm chung một mạng.
- **Routing & Security Policies:** VPC Peering không có tính chất bắc cầu (non-transitive). Để kết nối hoạt động, bắt buộc phải cập nhật bảng định tuyến (Route Table) ở cả hai đầu VPC và điều chỉnh Security Groups để chấp nhận CIDR của nhau.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ truyền thông VPC Peering (VPC Peering Architecture & Routing)
```
[VPC-A: CIDR 10.1.0.0/16]                     [VPC-B: CIDR 10.2.0.0/16]
 ┌──────────────────────┐                      ┌──────────────────────┐
 │ [EC2 Instance A]     │                      │ [EC2 Instance B]     │
 │ Private IP: 10.1.1.5 │                      │ Private IP: 10.2.1.8 │
 └──────────┬───────────┘                      └──────────┬───────────┘
            │                                             │
            ▼                                             ▼
  [Route Table VPC-A]                           [Route Table VPC-B]
  Destination: 10.2.0.0/16                      Destination: 10.1.0.0/16
  Target: pcx-012345678                          Target: pcx-012345678
            │                                             │
            └──────────────► [VPC Peering Connection] ◄────┘
                              ID: pcx-012345678
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | VPC Peering | AWS Transit Gateway (TGW) |
|---|---|---|
| **Độ phức tạp mở rộng** | Rất cao khi có nhiều VPC (Nối lưới chéo - Mesh network). | Rất thấp, hoạt động như một Cloud Hub trung tâm (Hub-and-Spoke). |
| **Tính chất bắc cầu** | **Không** (VPC A peering B, B peering C -> A không thể ping C). | **Có** (Các VPC kết nối vào TGW có thể truyền thông qua lại dễ dàng). |
| **Chi phí** | Không mất phí khởi tạo, chỉ tính phí truyền tải dữ liệu (Data Transfer). | Mất phí thuê cổng hàng giờ (Hourly attachment fee) + phí xử lý data. |
| **Trường hợp sử dụng** | Kết nối một vài VPC đơn giản (dưới 5-10 VPC). | Kết nối hàng chục/hàng trăm VPC trong kiến trúc Enterprise lớn. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. VPC Peering không thông (Lỗi mất kết nối giữa 2 VPC)
*   **Nguyên nhân 1: Quên cấu hình Route Table (Lỗi phổ biến nhất):**
    *   **Cơ chế:** Việc thiết lập VPC Peering thành công ở trạng thái `Active` mới chỉ là tạo ra "đường dây vật lý ảo". Bạn bắt buộc phải cấu hình "chỉ đường" cho các gói tin.
    *   *Ở VPC-A:* Route Table của subnet chứa EC2-A phải có route trỏ CIDR của VPC-B (`10.2.0.0/16`) tới target là VPC Peering Connection ID (`pcx-xxxx`).
    *   *Ở VPC-B:* Ngược lại, Route Table của subnet chứa EC2-B phải có route trỏ CIDR của VPC-A (`10.1.0.0/16`) tới target là `pcx-xxxx`.
*   **Nguyên nhân 2: Trùng lặp dải IP (Overlapping CIDR Blocks):**
    *   Nếu VPC-A và VPC-B có chung dải IP (ví dụ cả hai đều dùng `10.0.0.0/16`), AWS sẽ **từ chối** tạo kết nối VPC Peering.
*   **Nguyên nhân 3: Security Group chưa cho phép CIDR đối phương:**
    *   Security Group của EC2-B phải mở cổng cho phép Inbound traffic từ dải IP Private của VPC-A (`10.1.0.0/16`), chứ không thể refer trực tiếp ID của Security Group bên VPC-A (chỉ dùng được trong cùng 1 VPC, trừ khi sử dụng tính năng Security Group Referencing đặc biệt nhưng yêu cầu cấu hình cẩn thận).

*   **Cách kiểm tra và debug bằng CLI:**
    *   *Kiểm tra trạng thái VPC Peering:*
        ```bash
        aws ec2 describe-vpc-peering-connections \
          --vpc-peering-connection-ids pcx-0123456789abcdef0
        ```
        *(Đảm bảo `"Status": {"Code": "active"}`).*
    *   *Kiểm tra Route Table từ CLI:*
        ```bash
        aws ec2 describe-route-tables \
          --filters "Name=vpc-id,Values=vpc-0123456789abcdef0"
        ```
        *(Đảm bảo có dòng trỏ tới `pcx-xxxx`).*
    *   *Sử dụng lệnh `traceroute` từ EC2-A để xem gói tin bị dừng ở đâu:*
        ```bash
        traceroute 10.2.1.8
        ```

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **VPC Peering** khi: Cần kết nối 2 VPC trong cùng một region (hoặc khác region) với chi phí tối ưu nhất và băng thông không giới hạn.
- Chọn **Transit Gateway** khi: Cần xây dựng kiến trúc Hub-and-Spoke lớn kết nối VPCs nội bộ với mạng On-Premises (qua VPN hoặc Direct Connect).
- Chọn **VPC Endpoints (PrivateLink)** khi: Chỉ muốn cho phép VPC-A truy cập vào một **dịch vụ cụ thể** nằm ở VPC-B chứ không muốn mở thông toàn bộ mạng lưới giữa 2 VPC.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [VPC Peering limitations and routing configuration](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-routing.html)
  - [Troubleshoot VPC Peering connections](https://docs.aws.amazon.com/vpc/latest/peering/troubleshoot-peering.html)
