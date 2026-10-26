# Tag Enforcement - Tag Policy vs SCP vs Config + SSM

**Chủ đề (Topic):** Resource Governance, Security/Compliance, Tagging
**Mục tiêu:** Phân biệt 3 lớp công cụ enforce tagging, biết khi nào chặn (preventive), khi nào phát hiện + sửa (detective/reactive).

---

## 1. Vấn Đề

Tag Policy mặc định **chỉ scan và đánh dấu** resource sai tag, không tự chặn việc tạo resource và không tự sửa. Vậy muốn chặn cứng hoặc tự sửa thì dùng gì? Ba lớp công cụ chia vai rõ ràng.

---

## 2. Bảng So Sánh 3 Lớp

| Công cụ | Loại | Vai trò | Chặn được gì |
|---|---|---|---|
| Tag Policy (Organizations) | Detective / Governance | Đo compliance định dạng tag | Scan + đánh dấu; tùy chọn `enforced_for` chặn **tag operation** sai định dạng |
| SCP (Service Control Policy) | Preventive | Guardrail cấp Organizations | **Từ chối luôn** `RunInstances`/`CreateBucket`... nếu thiếu tag bắt buộc |
| AWS Config rule `required-tags` | Detective + auto-remediation | Phát hiện + tự sửa | Không chặn; phát hiện non-compliant rồi kích SSM sửa |

---

## 3. Tag Policy - Điểm Cần Chính Xác

- Mặc định: chỉ báo cáo compliance.
- Có cơ chế `enforced_for` (prevention) chặn **tag operation** (`TagResource`/`UntagResource`) không tuân thủ trên một số resource type.
- Nhưng: **KHÔNG chặn việc tạo resource** thiếu tag, và **không phủ hết mọi service**.

Kết luận: Tag Policy là governance/đo lường, không phải chốt chặn cứng cửa vào.

---

## 4. SCP - Chặn Cứng Cửa Vào

Đây mới là preventive thật sự. Ví dụ chặn tạo EC2 nếu thiếu tag `CostCenter`:

```json
{
  "Effect": "Deny",
  "Action": "ec2:RunInstances",
  "Resource": "arn:aws:ec2:*:*:instance/*",
  "Condition": {
    "Null": { "aws:RequestTag/CostCenter": "true" }
  }
}
```

Condition key thường dùng: `aws:RequestTag/<key>`, `aws:TagKeys`.

---

## 5. Config + SSM - Phát Hiện Rồi Tự Sửa

Set up một lần, chạy nền always-on. Luồng:

```
Ai đó tạo resource mới / sửa tag sai
  -> AWS Config ghi nhận configuration item
    -> Config Rule "required-tags" đánh giá -> NON_COMPLIANT
      -> Remediation action gọi SSM Automation document
        -> SSM runbook tự gắn/sửa tag cho đúng dictionary
          -> Config đánh giá lại -> COMPLIANT
```

Ba mảnh cấu hình:
1. AWS Config bật recorder cho resource type cần theo dõi.
2. Config Rule `required-tags` (managed rule) khai báo tag bắt buộc.
3. Remediation gắn vào rule, trỏ tới SSM Automation document.

Remediation có 2 chế độ:

| Chế độ | Hành vi |
|---|---|
| Automatic | Vi phạm là SSM chạy luôn, không cần người bấm |
| Manual | Config chỉ đánh dấu, người vận hành bấm "Remediate" mới chạy |

---

## 6. Điểm Then Chốt: Preventive vs Reactive

| | Preventive (SCP) | Reactive (Config + SSM) |
|---|---|---|
| Thời điểm | Chặn **trước khi** resource ra đời | Sửa **sau khi** resource đã tồn tại |
| Nếu vi phạm | Không tạo được | Tạo được, sai trong vài giây/phút rồi bị sửa |
| Khoảng hở | Không | Có - cửa sổ non-compliant giữa lúc tạo và lúc remediate |

Nếu tag dùng để phân quyền bảo mật (ABAC), khoảng hở của Config có thể nguy hiểm -> phải dùng SCP chặn từ đầu.

---

## 7. Lưu Ý Thực Tế Với Config + SSM

- Config đánh giá theo sự kiện thay đổi hoặc định kỳ -> có độ trễ, không phải mili-giây.
- Có resource type Config không hỗ trợ ghi nhận -> rule không chạm tới được.
- Remediation có thể fail (thiếu quyền IAM, throttling) -> cần retry.
- Chi phí: Config tính tiền theo số configuration item ghi nhận; bật recorder toàn org lớn có thể tốn.

---

## 8. Kiến Trúc Phòng Thủ 3 Lớp

1. **SCP** - chặn tạo resource thiếu tag bắt buộc (cửa vào).
2. **Tag Policy** - đo compliance định dạng tag toàn org (thước đo).
3. **Config + SSM** - bắt cái đã lọt qua và tự sửa (dọn dẹp).
