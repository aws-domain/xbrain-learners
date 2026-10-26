# Developing a Tagging Strategy - Tổng Quan

**Chủ đề (Topic):** Cost Governance, Resource Governance, Tagging
**Nguồn:** AWS Cloud Operations module "Building a tagging strategy" (4 bước)
**Mục tiêu:** Hiểu vì sao cần tagging strategy và quy trình 4 bước triển khai ở quy mô AWS Organizations.

---

## 1. Tag Là Gì Và Vì Sao Quan Trọng

Tag là cặp **key-value** gán vào resource AWS (ví dụ `Environment = prod`). Bản thân tag không đổi hành vi resource, nhưng là **metadata** để lọc, báo cáo, phân quyền và phân bổ chi phí.

Tagging chạm nhiều mục tiêu vận hành:

| Mục tiêu | Tag phục vụ điều gì |
|---|---|
| Cost allocation | Chia hóa đơn AWS về đúng team/dự án (chargeback/showback) |
| Security / Compliance | Đánh dấu mức nhạy cảm dữ liệu, áp policy theo tag (ABAC) |
| Operations | Biết môi trường, owner, lịch bật/tắt |
| Automation | SSM/Resource Groups thao tác hàng loạt theo tag |

Không có tag chuẩn, mọi thứ ở trên đều làm thủ công và dễ sai.

---

## 2. Tại Sao Stakeholder Toàn Công Ty Phải Tham Gia

Cloud team biết hạ tầng, nhưng **không sở hữu ngữ nghĩa nghiệp vụ** của tag:

- Chỉ **Finance** biết mã cost center hợp lệ.
- Chỉ **Security** biết cách phân loại dữ liệu.
- Chỉ **Operations** biết ai on-call, resource được tắt lúc nào.
- Chỉ **Software engineering** biết resource thuộc app/version nào.

Nếu cloud team tự bịa tag, sẽ ra những key vô dụng cho báo cáo (`server-01`, `test-vm`). Vậy nên:

- **Stakeholder cung cấp:** cần tag gì và tại sao (nội dung nghiệp vụ).
- **Cloud team quyết định:** tag phải viết thế nào (chuẩn kỹ thuật).

Đây là **cross-functional governance**, không phải quyết định kỹ thuật đơn lẻ.

---

## 3. Vấn Đề "Chuẩn Hóa"

Không chuẩn hóa thì cùng một ý nghĩa bị viết nhiều kiểu, không thể lọc/báo cáo/áp policy:

```
Team A:  Environment = "Prod"
Team B:  env         = "production"
Team C:  ENV         = "PRD"
```

Cloud team ra **tagging dictionary** thống nhất: key phải là `Environment`, value chỉ được `prod|staging|dev`. Dictionary này là input cho Tag Policy ở bước sau.

---

## 4. Quy Trình 4 Bước (AWS Organizations)

| Bước | Tên | Bản chất | Công cụ |
|---|---|---|---|
| 1 | Define a tagging strategy | Nghĩ ra quy tắc: tag bắt buộc, policy, standards | Tagging dictionary (giấy tờ) |
| 2 | Create tag policies | Áp quy tắc xuống org, đo compliance | AWS Organizations Tag Policies |
| 3 | Tag resources | Gắn tag thật lên resource | SSM Automation, Resource Groups, Tag Editor |
| 4 | Create a dashboard | Giám sát + tự sửa (remediation) | Operations account + Config + SSM |

Mạch logic:

```
Define (quy tắc)
  -> Create tag policies (áp lên Organizations, đo compliance)
    -> Tag resources (gắn tag thật)
      -> Dashboard + Remediation (giám sát, tự sửa)
        -> lặp lại, mở rộng dần
```

---

## 5. Nguyên Tắc Cốt Lõi (Summary Của Module)

Tagging strategy là quá trình **lặp và cải tiến**. Bắt đầu nhỏ với ưu tiên trước mắt, mở rộng schema dần theo nhu cầu. Đừng cố hoàn hảo ngay từ đầu, và đừng siết enforcement quá sớm khiến vận hành tê liệt.

---

## 6. Tài Liệu Liên Quan Trong Repo

- `tagging_strategy_4_steps.md` - chi tiết từng bước và diagram AWS Organizations.
- `tagging_enforcement_tag_policy_scp_config.md` - phân biệt 3 lớp enforcement (Tag Policy / SCP / Config + SSM).
- `tagging_greenfield_vs_brownfield.md` - áp dụng cho hạ tầng mới vs hạ tầng đã có.
