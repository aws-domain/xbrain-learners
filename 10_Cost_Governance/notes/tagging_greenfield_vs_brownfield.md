# Tagging Strategy - Greenfield vs Brownfield

**Chủ đề (Topic):** Resource Governance, Tagging, Cloud Operations
**Mục tiêu:** Cùng quy trình 4 bước áp dụng cho hạ tầng mới (greenfield) và hạ tầng đã có (brownfield), nhưng trọng tâm khác nhau.

---

## 1. Kết Luận Ngắn

Quy trình 4 bước dùng được cho **cả hai** trường hợp. Khác biệt nằm ở **trọng tâm và thứ tự ưu tiên** của từng bước.

---

## 2. Cùng 4 Bước, Khác Trọng Tâm

| Bước | Greenfield (hạ tầng mới) | Brownfield (hạ tầng đã có) |
|---|---|---|
| 1. Define | Giống nhau; lợi thế làm sạch từ đầu | Giống nhau, thêm việc khảo sát hiện trạng lộn xộn |
| 2. Tag policies | Bật sớm, có thể enforce/SCP ngay | Bật chế độ **báo cáo trước**, chưa dám chặn |
| 3. Tag resources | Gắn tag ngay lúc tạo qua IaC, ít cần bulk | Bước **nặng nhất**: bulk tag hàng nghìn resource cũ |
| 4. Dashboard + remediation | Chủ yếu để duy trì chống drift | Vừa dọn tồn đọng, vừa duy trì |

---

## 3. Greenfield - Nghiêng Về Prevent

Sức mạnh: nhét tag vào **IaC ngay từ đầu**, resource sinh ra đã đúng tag.

```hcl
# Terraform - tag gắn sẵn lúc provision
resource "aws_instance" "app" {
  tags = {
    CostCenter  = "CC-1024"
    Environment = "prod"
    Owner       = "team-payments"
  }
}
```

Cộng thêm **SCP chặn từ đầu** (deny tạo resource thiếu tag) -> gần như không bao giờ có resource sai tag. Bước 3 bulk tag gần như thừa. Đây là kịch bản lý tưởng.

Lớp chủ đạo: **SCP + IaC**.

---

## 4. Brownfield - Nghiêng Về Detect + Remediate

Thách thức: resource cũ đã chạy production, tag lộn xộn hoặc không có. Không thể chặn cứng ngay (SCP/enforce mạnh làm gãy vận hành hiện tại). Trình tự mềm:

1. Bật Tag Policy chế độ **báo cáo** -> hiểu hiện trạng ("understand how resources are tagged").
2. Bulk tag phần tồn đọng bằng SSM / Resource Groups / Tag Editor.
3. Đạt tuân thủ đủ cao rồi **mới siết** enforcement/SCP.

Lớp chủ đạo: **Config + SSM + Tag Policy report**.

---

## 5. Vì Sao Module Nghiêng Về Brownfield

Các từ khóa trong module - "generate resource compliance reports", "understand how resources are tagged", "remediation mechanism" - chỉ có nghĩa khi **đã có resource để đo và sửa**. Greenfield thuần thì phòng ngừa ngay từ IaC, ít cần đo compliance của cái đã tồn tại. Tài liệu ngầm định doanh nghiệp đã có sẵn nhiều account/resource cần đưa vào khuôn khổ - đúng thực tế đa số công ty áp tagging khi hạ tầng đã phình to.

---

## 6. Nguyên Tắc Chung

Câu Summary "start small, grow the schema as you need" đúng cho cả hai, nhưng **cực kỳ quan trọng với brownfield** vì không thể chuẩn hóa hết một phát mà không làm gãy vận hành.
