# Môi Trường Phát Triển & VPC Peering — Core Knowledge Summary

---

## 1. Các Môi Trường Trong Một Hệ Thống

Hầu hết công ty chạy cùng 1 codebase trên **nhiều môi trường riêng biệt**:

| Môi trường | Dùng cho | Đặc điểm |
|---|---|---|
| **Production** | Khách hàng thật đang dùng | Data thật, tiền thật, không được phép lỗi |
| **Staging** | Test trước khi release | Bản copy gần giống production, dùng để verify |
| **Development** | Dev đang code feature mới | Thường xuyên thay đổi, hay bị lỗi — không ảnh hưởng ai |

> **Tại sao phải tách?** Nếu dev lỡ tay chạy câu query xóa nhầm data mà tất cả chung 1 môi trường → data khách hàng thật bị mất. Tách ra thì chỉ mất data test, production không bị ảnh hưởng.

---

## 2. Các Môi Trường Chạy Ở Đâu?

Không có quy tắc cứng — tùy budget, quy mô, và giai đoạn phát triển của công ty.

### Phổ biến nhất hiện nay — Tất cả trên Cloud
```
Production  → AWS VPC
Staging     → AWS VPC
Development → AWS VPC hoặc máy local của dev
```
Công ty startup, công ty đã migrate lên cloud hoàn toàn. Chi phí thấp hơn tự dựng server, scale dễ hơn.

### Kiểu cũ — On-Premises
```
Production  → Server vật lý tại data center
Staging     → On-premises hoặc Cloud
Development → Máy local của dev
```
Nhiều công ty lớn, ngân hàng, tổ chức tài chính vẫn giữ production on-premises vì compliance, quy định pháp lý, hoặc đã đầu tư infrastructure từ trước.

### Đang chuyển đổi — Hybrid (Migration)
```
Production  → On-premises (chưa migrate xong)
Staging     → AWS (đã lên cloud trước)
Development → AWS hoặc local
```
Đây là lý do **Direct Connect và VPN** quan trọng — staging trên AWS cần giao tiếp với production còn on-premises trong giai đoạn chuyển đổi.

### Dev Environment
Dev thường **không cần chạy trên cloud** — chạy trên máy local hoặc Docker là đủ. Chỉ cần môi trường dev trên cloud khi test tính năng liên quan đến AWS infrastructure (VPC, RDS, Lambda...).

---

## 3. Tại Sao Cần VPC Peering?

Mỗi môi trường thường nằm trong **VPC riêng biệt** để isolation. VPC Peering cần thiết khi các VPC đó cần **giao tiếp có kiểm soát** với nhau.

### Các use case phổ biến

**1. Tách môi trường nhưng vẫn cần giao tiếp**
- Staging cần copy một phần data thật từ production để test cho sát thực tế
- Staging cần đọc reference data từ production (danh mục sản phẩm, config...)
- Pipeline CI/CD cần deploy vào cả staging lẫn production

> Nếu staging hoàn toàn độc lập, không cần lấy gì từ production → không cần peering.

**2. Tách theo team hoặc service (Microservices)**
```
VPC Team Payment  ←peering→  VPC Team Order
```
Mỗi team quản lý VPC riêng, có network boundary riêng. Nhưng các service vẫn cần gọi nhau — peering cho phép giao tiếp mà không cần ra internet.

**3. Multi-account architecture**
```
Account: Security Tools VPC  ←peering→  Account: Production VPC
```
Công ty lớn dùng nhiều AWS account riêng biệt. Security team cần monitor Production account — peering cho phép làm điều đó mà traffic không ra internet.

**4. Shared Services**
```
VPC Shared Services (Active Directory, DNS, Monitoring)
        ↕ peering
VPC App 1,  VPC App 2,  VPC App 3
```
Thay vì mỗi VPC tự chạy AD/DNS riêng, tạo 1 VPC chứa shared services, các VPC khác peer vào dùng chung — tiết kiệm chi phí.

**5. Acquisition / Merger**
Công ty A mua công ty B — mỗi bên đã có VPC riêng. Peering cho phép kết nối 2 hệ thống nhanh chóng mà không cần redesign toàn bộ network.

---

## 4. Tại Sao Không Gộp Vào 1 VPC Luôn?

Vì **isolation là mục đích có chủ đích**:
- **Blast radius:** Nếu 1 VPC bị compromise, không ảnh hưởng VPC kia
- **Phân quyền:** Rõ ràng theo team/account, dễ audit
- **Compliance:** Một số regulation yêu cầu tách biệt môi trường (ngân hàng, y tế...)

VPC Peering cho phép **giao tiếp có kiểm soát** — chỉ những gì được route và SG cho phép mới đi qua được.

---

## 5. Giới Hạn Của VPC Peering

- **Không transitive:** A↔B, B↔C → A không reach được C
- Số lượng VPC tăng → số peering connections tăng theo cấp số nhân (5 VPC = 10 connections)
- Khó quản lý khi scale lớn → dùng **Transit Gateway** thay thế

---

## Quick Reference

**Q: Staging và Production khác gì nhau?**
A: Production là môi trường khách hàng thật đang dùng — data thật, không được lỗi. Staging là bản copy gần giống production để team test trước khi release — lỗi ở đây không ảnh hưởng khách hàng.

**Q: Dev environment có cần chạy trên AWS không?**
A: Không nhất thiết. Dev thường chạy local hoặc Docker là đủ. Chỉ cần lên AWS khi test tính năng liên quan đến AWS infrastructure cụ thể.

**Q: Khi nào cần VPC Peering giữa Production và Staging?**
A: Khi staging cần lấy data hoặc gọi service từ production — ví dụ copy data thật để test, đọc reference data, hoặc CI/CD pipeline cần access cả 2. Nếu staging hoàn toàn độc lập thì không cần.

**Q: Tại sao không để tất cả trong 1 VPC cho đơn giản?**
A: Isolation có chủ đích — giới hạn blast radius khi có sự cố, phân quyền rõ ràng theo team/account, và đáp ứng compliance requirements.
