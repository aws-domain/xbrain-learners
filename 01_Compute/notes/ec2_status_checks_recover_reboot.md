# EC2 Status Checks + Auto Recovery / Auto Reboot

## Vấn đề gốc rễ

EC2 instance có thể hỏng vì 2 lý do hoàn toàn khác nhau, và mỗi loại cần một cách xử lý khác nhau:

- **Hỏng do AWS / phần cứng vật lý bên dưới** → bạn không sửa được từ bên trong instance
- **Hỏng do hệ điều hành / cấu hình bên trong instance** → chuyển sang máy khác cũng vô ích

Nếu dùng sai hành động để xử lý sai loại lỗi → instance không hồi phục, hoặc hai cơ chế tự động giẫm chân nhau.

---

## 2 loại Status Check

EC2 tự chạy 2 nhóm status check, phản ánh 2 tầng sự cố:

### StatusCheckFailed_System — hỏng phía AWS / phần cứng
- Máy chủ vật lý (host) chết, mất điện, mất mạng ở host, lỗi hệ thống của AWS
- **Không phải lỗi của bạn**, không sửa được từ trong instance
- Cách chữa đúng: **Recover** (dời sang host mới)

### StatusCheckFailed_Instance — hỏng phía OS / cấu hình trong instance
- OS treo, hết RAM, filesystem lỗi, cấu hình mạng sai, kernel panic
- Là vấn đề **bên trong máy của bạn**
- Cách chữa đúng: **Reboot** (khởi động lại OS) hoặc tự vào sửa

> `StatusCheckFailed` (tổng) = fail khi _System HOẶC _Instance fail (bao gồm cả hai).

---

## Recover hoạt động như thế nào

**Recover** = AWS di chuyển instance sang **một host vật lý mới (khỏe)** rồi khởi động lại trên đó. Đây là **cùng một instance**, không phải tạo máy mới.

### Vì sao Recover chỉ dùng với _System, không dùng với _Instance
- Lỗi **System** (phần cứng chết) → dời sang host mới là đúng thuốc → giải quyết được
- Lỗi **Instance** (OS của bạn hỏng) → dù dời sang host mới vẫn mang theo root volume hỏng → OS vẫn hỏng y như cũ → recover vô ích

> Ẩn dụ: Recover sửa được "nhà hỏng" (chuyển sang nhà mới), không sửa được "người trong nhà bệnh" (OS lỗi).

### Instance sau recover giữ nguyên những gì
Vì là cùng instance dời host (không tạo mới), nên giữ nguyên:
- **Instance ID**
- **Private IP** (thuộc ENI, ENI đi theo instance)
- **Elastic IP**
- Metadata và EBS volume đang gắn

> Hệ quả thực tế: các hệ thống khác trỏ tới instance qua IP/ID vẫn chạy bình thường sau recover, không cần cấu hình lại. Khác hẳn Auto Scaling thay instance mới (ID và IP đổi hết).

---

## Vì sao đặt Recover 2 period và Reboot 3 period

Khi có **cả hai alarm** cùng theo dõi một instance:
- Alarm **Recover** (gắn `StatusCheckFailed_System`): dời sang host mới
- Alarm **Reboot** (gắn `StatusCheckFailed_Instance`): khởi động lại OS

"Period" = số chu kỳ đánh giá liên tiếp phải fail thì alarm mới kích hoạt.

Khi host vật lý chết, thường **cả hai** check (_System và _Instance) fail cùng lúc. Nếu hai alarm đặt **cùng ngưỡng thời gian** → cùng kích hoạt → reboot và recover **xung đột (race condition)**, kết quả không đoán trước được.

Giải pháp: cho **Recover kích hoạt sớm hơn** Reboot.

| Alarm | Period | Kích hoạt sau |
|---|---|---|
| Recover | 2 | 2 phút lỗi |
| Reboot | 3 | 3 phút lỗi |

- Nếu là lỗi phần cứng thật → Recover ra tay trước (2 phút), dời instance sang host khỏe → check pass lại trước khi Reboot (3 phút) kịp kích hoạt → không xung đột
- Reboot chỉ thực sự kích hoạt khi lỗi kéo dài mà Recover không xử lý được

> Ý tưởng: ưu tiên Recover trước, Reboot là lớp dự phòng sau; chênh lệch thời gian giúp hai hành động không chạy đè lên nhau.

---

## Tóm tắt nhanh

| Loại lỗi | Status check | Hành động đúng | Lý do |
|---|---|---|---|
| Phần cứng / host AWS chết | `StatusCheckFailed_System` | Recover | Dời sang host khỏe |
| OS / cấu hình trong máy hỏng | `StatusCheckFailed_Instance` | Reboot | Khởi động lại OS |

---

## Lưu ý cho kỳ thi

- Recover **chỉ** đi với `StatusCheckFailed_System`, không dùng cho `_Instance`
- Instance sau recover **giữ nguyên** Instance ID, Private IP, Elastic IP, EBS volume
- Đặt Recover 2 period, Reboot 3 period để tránh tranh chấp khi dùng cả hai
- `StatusCheckFailed` (tổng) báo fail khi bất kỳ check con nào fail
