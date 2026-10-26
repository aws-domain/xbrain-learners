# Configuring IAM Identity Center for Federated Access

> Nội dung đã đối chiếu với AWS IAM Identity Center User Guide (xem Nguồn ở cuối).

## IAM Identity Center là gì

**AWS IAM Identity Center** (tên cũ: **AWS Single Sign-On**, đổi tên 26/07/2022) là giải pháp kết nối **workforce user** (nhân viên) tới:

- **AWS accounts** (nhiều account cùng lúc), và/hoặc
- **AWS managed applications**.

Thay vì tạo IAM user riêng cho từng người, bạn kết nối identity provider sẵn có → user đăng nhập **một lần**, truy cập mọi thứ được gán. Đây chính là hiện thực của **federated access**.

> **Lưu ý:** IAM Identity Center là **regional** (phải bật ở một region), khác với IAM cổ điển (global).

## Giá trị cốt lõi: "One point of federation"

Bạn **federate một lần duy nhất** — chỉ quản một certificate khi dùng IdP SAML 2.0 — rồi dùng chung cho nhiều account và nhiều app. Giảm công quản lý, giảm sai sót so với cấu hình federation rải rác.

## 3 khái niệm phải nắm

| Khái niệm | Là gì |
|-----------|-------|
| **Identity source** | Nơi lưu & xác thực user. 3 lựa chọn: **(1)** Identity Center directory (tạo user trực tiếp), **(2)** External IdP qua **SAML 2.0** (Okta, Azure AD, ...), **(3)** Active Directory. |
| **Permission set** | "Khuôn quyền" cho một job function (vd Admin, ReadOnly). Khi gán, Identity Center **tự tạo IAM role + policy tương ứng trong mỗi account**. |
| **Account assignment** | Gán **user/group** + **permission set** vào **account** cụ thể → quyết định ai vào account nào với quyền gì. |

## Luồng hoạt động (rút gọn)

1. Chọn **identity source** (directory nội bộ hoặc IdP ngoài).
2. Tạo **permission set** theo job function.
3. **Account assignment**: gán (user/group × permission set × account).
4. User đăng nhập **AWS access portal** (web portal) → thấy danh sách account/app được phép → bấm vào là truy cập (credentials tạm qua role, tự hết hạn).

## 2 loại instance

| Instance | Khi nào dùng |
|----------|--------------|
| **Organization instance** | **Best practice.** Deploy ở management account của AWS Organizations; là loại **duy nhất** quản được truy cập AWS accounts. Dùng cho production. |
| **Account instance** | Chỉ để hỗ trợ triển khai **cô lập** một vài AWS managed application. Không quản được multi-account. |

## Ghi nhớ nhanh

- IAM Identity Center = **federate một lần, truy cập nhiều account/app** (SSO cho workforce).
- Bộ ba: **identity source** (ai) → **permission set** (quyền gì) → **account assignment** (ở account nào).
- Permission set → Identity Center tự sinh **IAM role** trong từng account; user nhận **credentials tạm**, không có long-term key.
- Production → dùng **organization instance**.
- Identity Center là **regional**.

## Nguồn

- [What is IAM Identity Center?](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
