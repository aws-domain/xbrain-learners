# Advanced Access Control with Attributes and Tags (ABAC)

> Nội dung đã đối chiếu với AWS IAM User Guide (xem Nguồn ở cuối).

## ABAC là gì

**ABAC (Attribute-Based Access Control)** = chiến lược phân quyền dựa trên **thuộc tính (attributes)**. Trong AWS, attributes chính là **tags**.

Ý tưởng cốt lõi: viết **một policy duy nhất** cho phép hành động **khi tag của principal khớp tag của resource**. Không cần liệt kê từng resource cụ thể.

Ví dụ: 3 role có tag `access-project` = `Heart` / `Star` / `Lightning`. Một policy duy nhất: "cho truy cập khi `tag của role` == `tag của resource`" → mỗi người chỉ đụng được resource cùng project.

## ABAC vs RBAC

| | **RBAC** (truyền thống) | **ABAC** (dựa trên tag) |
|---|---|---|
| Phân quyền theo | Job function → mỗi function một policy, liệt kê resource cụ thể | Tag khớp nhau giữa principal và resource |
| Thêm resource mới | **Phải sửa policy** để cho phép truy cập | **Không cần sửa policy** — chỉ cần gắn đúng tag |
| Số lượng policy | Nhiều (mỗi job một policy) | Ít (một/vài policy dùng chung) |
| Khi team/person đổi việc | Gán policy/role khác | Chỉ đổi tag / đổi role, policy giữ nguyên |

**Lợi ích chính của ABAC:** scale theo tăng trưởng (thêm resource/project không phải sửa policy), ít policy hơn, quyền granular, và dùng được **attribute từ corporate directory** (IdP SAML/OIDC truyền **session tags** vào IAM khi federate).

## Cơ chế: tag condition keys

Policy dùng **`Condition`** để so khớp tag của principal với tag của resource:

| Condition key | Nghĩa |
|---------------|-------|
| `aws:PrincipalTag/<key>` | Tag gắn trên **principal** (user/role đang gọi) |
| `aws:ResourceTag/<key>` (hoặc `iam:ResourceTag/...`) | Tag gắn trên **resource** đích |
| `aws:RequestTag/<key>` | Tag **được gửi kèm** trong request (lúc tạo/gắn tag) |

**Ví dụ policy ABAC** — cho assume role khi tag project/team/cost-center của user khớp tag của role:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": "arn:aws:iam::111122223333:role/access-*",
    "Condition": {
      "StringEquals": {
        "iam:ResourceTag/access-project": "${aws:PrincipalTag/access-project}",
        "iam:ResourceTag/access-team":    "${aws:PrincipalTag/access-team}",
        "iam:ResourceTag/cost-center":    "${aws:PrincipalTag/cost-center}"
      }
    }
  }]
}
```

`${aws:PrincipalTag/...}` là **biến** — lấy giá trị tag của chính người gọi rồi so với tag resource. Nhờ vậy **một policy** phục vụ được mọi project.

## Ghi nhớ nhanh

- ABAC = phân quyền bằng **tag khớp tag**; attributes trong AWS = tags.
- Ưu điểm lớn nhất so với RBAC: **thêm resource/project không phải sửa policy**.
- Bộ key hay dùng: `aws:PrincipalTag`, `aws:ResourceTag`, `aws:RequestTag`.
- Federation + ABAC: IdP truyền **session tags** → IAM áp vào principal → phân quyền theo thuộc tính nhân viên.
- Dùng cú pháp biến `${aws:PrincipalTag/key}` để so khớp động trong `Condition`.

## Nguồn

- [Define permissions based on attributes with ABAC authorization](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
