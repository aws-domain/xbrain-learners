# Instance Store vs EBS (và vì sao DiskReadOps luôn bằng 0)

## Vấn đề gốc rễ

EC2 có 2 loại storage với bản chất khác nhau hoàn toàn. Nếu không phân biệt được, bạn sẽ hiểu sai vì sao một số CloudWatch metric (`DiskReadOps`, `DiskWriteOps`...) **gần như luôn bằng 0** dù instance vẫn đọc/ghi đĩa liên tục.

---

## Instance Store Volume

**Instance store** là ổ đĩa (SSD/NVMe) **gắn vật lý trực tiếp vào máy chủ host** đang chạy instance.

- **Ephemeral (tạm thời)**: dữ liệu **mất sạch** khi instance **stop**, **terminate**, hoặc host **hỏng**. (Reboot thì còn, vì không đổi host.)
- **Tốc độ cực cao, latency cực thấp** vì gắn local vào host.
- Đánh đổi: không bền → chỉ dùng cho **cache, buffer, scratch data, dữ liệu tạm có thể tái tạo**.

---

## EBS (Elastic Block Store)

**EBS volume** là ổ đĩa **mạng (network-attached)**, nằm **tách rời khỏi host**, kết nối tới instance qua mạng nội bộ AWS. Giống ổ cứng gắn ngoài qua mạng.

- **Persistent (bền vững)**: dữ liệu **vẫn còn** khi stop instance; có thể **tháo ra gắn sang instance khác**, snapshot sang S3.
- Nhanh nhưng đi qua mạng (không local như instance store).
- Dùng cho **OS (root volume), database, dữ liệu cần giữ lâu dài**.

---

## So sánh

| | Instance Store | EBS |
|---|---|---|
| Vị trí | Gắn vật lý vào host | Ổ mạng, tách khỏi host |
| Dữ liệu khi stop/terminate | **Mất** | **Còn** |
| Bền vững | Tạm thời (ephemeral) | Bền (persistent) |
| Tốc độ | Rất nhanh (local) | Nhanh, qua mạng |
| Tháo/gắn lại instance khác | Không | Có |
| Dùng cho | Cache, scratch, temp | OS, database, dữ liệu cần giữ |

---

## "EBS-backed" nghĩa là gì

- **EBS-backed instance**: root volume (ổ chứa OS) nằm trên EBS. Đây là **mặc định và phổ biến nhất** (Amazon Linux 2023, hầu hết AMI hiện đại).
- **Instance store-backed instance**: root volume nằm trên instance store (kiểu cũ, hiếm gặp).

> Điểm mấu chốt: một EBS-backed instance **thường KHÔNG có instance store volume nào**, trừ khi chọn dòng instance có sẵn instance store (họ `i3`, `m5d`, `c5d`...). `t3.micro` **không có** instance store.

---

## Vì sao DiskReadOps gần như luôn bằng 0

Các metric `DiskReadOps`, `DiskWriteOps`, `DiskReadBytes`, `DiskWriteBytes` trong namespace **`AWS/EC2`** **chỉ đếm I/O của instance store volume**, KHÔNG đếm I/O của EBS.

Ghép lại:
1. Instance `t3.micro` (EBS-backed) **không có instance store volume**.
2. Các metric `Disk*` chỉ đo instance store.
3. Không có instance store → không có gì để đếm → giá trị **0** (hoặc metric không được báo cáo).

> Đây là lý do nó **luôn** bằng 0 bất kể đọc/ghi đĩa nhiều thế nào — vì mọi I/O thật đang diễn ra trên **EBS**, mà EBS không được các metric `Disk*` này đo.

### Muốn đo I/O thật của EBS
Dùng metric trong namespace **`AWS/EBS`**: `VolumeReadOps`, `VolumeWriteOps`, `VolumeReadBytes`, `VolumeWriteBytes`.

---

## Đối chiếu: vì sao các metric khác KHÔNG bằng 0

| Metric | Vì sao khác 0 |
|---|---|
| `NetworkIn` / `NetworkOut` | Đo byte qua network interface; luôn có traffic (SSH/SSM, update, phản hồi) |
| `CPUUtilization` | Kể cả idle, OS vẫn chạy tiến trình nền → dao động nhỏ, không cố định 0 |
| `DiskReadOps` (và nhóm `Disk*`) | Đo instance store, mà EBS-backed thường không có → **0** |

---

## Lưu ý cho kỳ thi

- `DiskReadOps/DiskWriteOps/DiskReadBytes/DiskWriteBytes` (namespace `AWS/EC2`) đo **instance store**, không đo EBS → thường 0 trên instance EBS-backed
- Đo I/O EBS phải dùng `Volume*` trong namespace `AWS/EBS`
- Instance store = ephemeral (mất khi stop/terminate), EBS = persistent
- Reboot KHÔNG mất dữ liệu instance store; stop/terminate thì mất
- Không có built-in metric cho RAM; cần CloudWatch agent
