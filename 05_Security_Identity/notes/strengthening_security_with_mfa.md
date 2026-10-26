# Strengthening Security with MFA

> Nội dung đã đối chiếu với tài liệu chính thức AWS IAM User Guide (xem mục Nguồn ở cuối).

## MFA là gì

**MFA (Multi-Factor Authentication)** = xác thực nhiều yếu tố. Ngoài sign-in credentials (password), user phải cung cấp thêm **một yếu tố xác thực nữa** từ một cơ chế MFA được AWS hỗ trợ mới truy cập được.

Mục đích: dù password bị lộ, kẻ tấn công vẫn **không** vào được vì thiếu yếu tố thứ hai.

## Ba loại yếu tố xác thực

| Yếu tố | Tên gọi trong AWS docs | Ví dụ |
|--------|------------------------|-------|
| **Something you know** | Knowledge factor | password, PIN |
| **Something you have** | Possession factor | security key, điện thoại |
| **Something you are** | Inherence factor | vân tay, khuôn mặt (biometric) |

Password là yếu tố đầu tiên (knowledge factor). MFA = password **+** ít nhất một possession/inherence factor.

## Các loại MFA mà AWS hỗ trợ

AWS chính thức liệt kê **3 loại** MFA:

| Loại | Mô tả |
|------|-------|
| **Passkeys & security keys** (FIDO) | Dựa trên chuẩn FIDO + public key cryptography. Gồm **security key** (thiết bị vật lý như YubiKey) và **synced passkey** (qua credential manager của Google/Apple/Microsoft/1Password...). **Phishing-resistant**, mạnh nhất. |
| **Virtual authenticator applications** | App trên điện thoại sinh mã **TOTP** (vd Google Authenticator, Authy). Hỗ trợ nhiều token trên một thiết bị. |
| **Hardware TOTP tokens** | Thiết bị vật lý sinh mã OTP 6 chữ số theo thuật toán TOTP. |

> **AWS khuyến nghị:** ưu tiên **passkeys / security keys (FIDO)** vì chống được phishing, man-in-the-middle và replay attack — mạnh hơn các lựa chọn dựa trên TOTP. Virtual MFA chỉ nên dùng tạm trong lúc chờ mua/nhận hardware.

### FIDO là gì (ngắn gọn)

**FIDO (Fast IDentity Online)** = bộ chuẩn xác thực mở, dùng **public key cryptography** thay cho password. Cặp khoá: **private key nằm trong thiết bị, không bao giờ rời đi**; public key lưu ở dịch vụ (AWS). Credential gắn với đúng **domain** của dịch vụ → trang giả không ký được → đó là lý do FIDO **phishing-resistant**. "Passkey" là tên gọi của credential FIDO.

## Best practices cốt lõi

1. **MFA cho root user là bắt buộc.** AWS **enforce MFA cho root user của mọi loại account** (standalone, management, member). User phải đăng ký MFA **trong vòng 14 ngày** kể từ lần đăng nhập Console đầu tiên nếu chưa bật.
2. **Root MFA chỉ ảnh hưởng root credentials.** IAM user là identity riêng, có cấu hình MFA riêng → phải bật MFA riêng cho từng IAM user.
3. **Đăng ký được tối đa 8 MFA device** cho mỗi root/IAM user (loại nào cũng được), nhưng chỉ cần **1 device** để đăng nhập. Nhiều device giúp tránh mất quyền truy cập khi 1 cái hỏng/mất.
4. **Ưu tiên temporary credentials cho human user** — dùng **IAM Identity Center** (SSO, MFA-protected) hoặc federation thay vì IAM user dài hạn khi có thể.

## MFA cho delete trong S3 (2 cơ chế)

Xoá là hành động phá huỷ, khó hồi phục → thêm MFA làm "chốt chặn": dù credentials bị lộ vẫn không xoá được. S3 có **2 cơ chế khác nhau**:

| | **MFA Delete** | **MFA-protected API access** (policy) |
|---|---|---|
| Là gì | Tính năng gắn vào **S3 Versioning** | Điều kiện trong **IAM / bucket policy** |
| Bảo vệ | Xoá vĩnh viễn object **version** + đổi trạng thái versioning | Bất kỳ action nào (không riêng delete) |
| Ai dùng | **Chỉ root** bật được, gõ trực tiếp `serial + mã 6 số` vào request | Áp cho IAM user/role bất kỳ |
| Bật bằng | Chỉ CLI/API (không có trên Console) | Viết JSON policy bình thường |

Cơ chế thứ 2 dùng condition key **`aws:MultiFactorAuthPresent`** — kiểm tra **request có được xác thực qua MFA hay không** (không phải "user đã bật MFA chưa"):

```json
{
  "Effect": "Deny",
  "Action": "s3:DeleteObject",
  "Resource": "arn:aws:s3:::my-bucket/*",
  "Condition": {
    "BoolIfExists": { "aws:MultiFactorAuthPresent": "false" }
  }
}
```

- Đọc: **Deny** `s3:DeleteObject` **nếu** request không qua MFA → chỉ request có MFA mới xoá được.
- Dùng `BoolIfExists` để xử lý đúng khi key không tồn tại (vd long-term access key).
- Viết dạng **Deny** vì `Explicit Deny > Allow` → chắc ăn.

## Ghi nhớ nhanh

- MFA không thay thế password → nó là **lớp thứ hai** chồng lên.
- Root user **phải** có MFA (và có deadline 14 ngày).
- Yếu tố xác thực phải thuộc **2 loại khác nhau** (know / have / are) mới gọi là MFA.
- Phishing-resistant (FIDO passkey/security key) > TOTP (virtual app / hardware token).

## Nguồn

- [AWS Multi-factor authentication in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
- [Multi-factor authentication for AWS account root user](https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-mfa-for-root.html)
