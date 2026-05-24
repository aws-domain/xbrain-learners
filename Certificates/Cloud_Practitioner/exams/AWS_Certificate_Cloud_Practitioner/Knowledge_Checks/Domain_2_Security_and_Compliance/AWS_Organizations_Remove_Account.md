# AWS Organizations - Remove Account

**Date**: 2026-05-11

## Yêu cầu để remove account khỏi AWS Organizations

Account phải có đủ thông tin để hoạt động **standalone**:

1. ✅ Chấp nhận **AWS Customer Agreement**
2. ✅ Chọn **support plan**
3. ✅ Cung cấp và xác minh **contact information**
4. ✅ Có **payment method** hợp lệ

## Không cần

- ❌ Raise support ticket với AWS Support
- ❌ Remove khỏi AWS Systems Manager
- ❌ Remove Service Control Policies (SCPs)

## Lưu ý

- Khi account rời Organization, **SCPs tự động không còn hiệu lực**
- Users/roles sẽ có **nhiều quyền hơn** (không còn bị SCPs hạn chế)
- Account phải **tự thanh toán** hóa đơn AWS
