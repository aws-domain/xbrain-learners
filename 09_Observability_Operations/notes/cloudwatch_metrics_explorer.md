# CloudWatch Metrics Explorer: Dashboard Tự Cập Nhật Theo Tag
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation)
**Note liên quan:** `cloudwatch_getting_started.md`, `cloudwatch_agent_in_asg.md`, `cloudwatch_cli_put_commands.md`, lab `d1-04`

---

## 0. Tóm Tắt Một Dòng
**Metrics Explorer** là một loại widget CloudWatch dashboard lọc tài nguyên **động theo tag**, không ghim cứng từng resource ID. Lọc theo tag `aws:autoscaling:groupName` thì mọi instance của ASG (kể cả instance mới scale-out) tự vào widget, không cần Lambda hay EventBridge.

---

## 1. Bài Toán Gốc
Bạn có ASG co giãn số instance liên tục. Muốn một dashboard CPU luôn hiển thị **đủ mọi instance hiện có**, kể cả con mới sinh ra, mà không phải vào sửa widget mỗi lần scale.

Widget thường ghim cứng Instance ID: scale ra con mới -> widget KHÔNG tự thấy -> phải sửa tay. Metrics Explorer giải quyết đúng chỗ này.

---

## 2. Cơ Chế: Lọc Động Theo Tag

```
ASG td-asg  --(tu gan tag)-->  moi instance:  aws:autoscaling:groupName = td-asg
                                                      |
Widget Explorer loc: CPUUtilization, From = aws:autoscaling:groupName = td-asg
                                                      |
                                   quet moi instance co tag do
                                                      v
        +--------------+--------------+-------------------------+
     instance-1     instance-2     instance-3 (moi scale ra)
     (co tu dau)    (co tu dau)    -> tu vao widget, khong sua gi
```

**Analogy:** Explorer như danh sách lớp ghi theo điều kiện "mọi học sinh đeo huy hiệu lớp 10A", thay vì ghi cứng tên từng bạn. Ai mới vào lớp đeo huy hiệu là tự có tên; ai chuyển đi là tự mất tên. Không ai sửa danh sách tay.

*Chỗ analogy gãy:* widget không "biết" đó là ASG. Nó chỉ biết lọc theo tag `aws:autoscaling:groupName = td-asg`. ASG tình cờ tự dán cái tag (huy hiệu) đó lên mọi instance nó đẻ ra, nên kết quả trông như "widget theo ASG". Tag này do ASG tự gắn, bạn không tạo tay.

---

## 3. Explorer vs Widget Thường

| Tiêu chí | Widget thường (Line/Number...) | Metrics Explorer |
|---|---|---|
| Chọn resource kiểu gì | Ghim cứng từng Instance ID | Lọc động theo tag |
| ASG scale ra instance mới | KHÔNG tự hiện, phải sửa tay | TỰ hiện |
| Cần Lambda/EventBridge để tự cập nhật | Có thể phải viết thêm | Không cần |
| Set bao nhiêu lần | Mỗi lần scale lại sửa | Set 1 lần, xong |

---

## 4. Các Bước Tạo (Console, lab d1-04)

1. `CloudWatch > Dashboards > Create dashboard`, tên `td-perf-dash`.
2. `Add widget` > chọn **Explorer**.
3. Màn "What type of Explorer widget do you want?": chọn **Empty Explorer widget** (KHÔNG chọn Pre-filled). Bấm **Next**.
   - Pre-filled dùng template dựng sẵn như "EC2 Instances by type" — lọc theo **loại instance**, không theo tag ASG, nên không khớp mục tiêu lab. Phải sửa lại sau.
   - Empty cho màn trống để tự set tag -> khớp bước lab, nhanh và sạch hơn.
4. Màn cấu hình (sau Next):
   - **Metrics:** thêm `CPUUtilization`.
   - **From** (tag filter): chọn `aws:autoscaling:groupName`, giá trị `td-asg`.
5. Add to dashboard.

**Bẫy giao diện:** ô set điều kiện lọc (From / tag filter) KHÔNG nằm ở màn chọn kiểu widget. Nó ở **màn sau khi bấm Next**. Dễ tưởng lầm là "sao không thấy chỗ set tag".

---

## 5. Lưu Ý Thực Tế
- Tag `aws:autoscaling:groupName` do ASG tự gắn — gõ tag này ở ô From là Console gợi ý ra giá trị `td-asg`.
- Instance vừa `InService` có thể cần vài phút để metric `CPUUtilization` đổ về thì widget mới có đường kẻ. Tag khớp ngay, nhưng dữ liệu metric cần thời gian.
- Metrics Explorer lọc được theo bất kỳ tag nào, không riêng tag ASG. Dùng custom tag (ví dụ `Environment = prod`) để gom nhóm resource tùy ý.

---

## 6. Mẹo Nhớ (exam)
Đề nói "dashboard tự thêm instance mới khi ASG scale, **ít thao tác nhất**, không dùng Lambda/EventBridge" -> chọn **CloudWatch Metrics Explorer lọc theo tag `aws:autoscaling:groupName`**. Thấy "ghim theo Instance ID" là đáp án sai cho yêu cầu auto-update.

---

## 7. Câu Tự Kiểm Tra
Bạn tạo widget Explorer lọc theo `aws:autoscaling:groupName = td-asg`, rồi ASG scale từ 1 lên 3 instance. Bạn có phải sửa widget để thêm 2 instance mới không? Nếu bạn đã lỡ ghim cứng từng Instance ID vào một widget thường thì câu trả lời có đổi không?

<details>
<summary>Đáp án</summary>

Không phải sửa. Widget Explorer lọc động theo tag, 2 instance mới mang tag `aws:autoscaling:groupName = td-asg` nên tự vào widget. Với widget thường ghim cứng Instance ID thì câu trả lời đổi: 2 instance mới KHÔNG tự hiện, bạn phải vào sửa widget thêm ID của chúng tay.
</details>

---

## Nguồn
- Nội dung lab `d1-04` trong project (`README.md`, Phần 2 bước 3-4).
- Kiến thức nền về CloudWatch Metrics Explorer và tag filter (hành vi ổn định).
