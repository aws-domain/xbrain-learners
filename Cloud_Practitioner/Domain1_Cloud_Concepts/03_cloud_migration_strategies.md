# Task 1.3 — Cloud Migration Strategies

> **Exam weight:** Domain 1 = 24% of scored content

## AWS Cloud Adoption Framework (AWS CAF)

AWS CAF giúp tổ chức **lập kế hoạch và thực hiện migration** lên AWS một cách có hệ thống.

### 4 Business Outcomes của AWS CAF

| Outcome | Mô tả |
|---------|-------|
| **Reduced business risk** | Giảm rủi ro kinh doanh nhờ tính tin cậy và bảo mật cao hơn |
| **Improved ESG performance** | Cải thiện hiệu suất môi trường, xã hội và quản trị |
| **Increased revenue** | Tăng doanh thu nhờ đổi mới nhanh hơn |
| **Increased operational efficiency** | Tăng hiệu quả vận hành, giảm chi phí |

### 6 Perspectives của AWS CAF

AWS CAF tổ chức hướng dẫn theo **6 perspectives**:

**Business Perspectives:**
1. **Business** — Đảm bảo cloud investments gắn với business outcomes
2. **People** — Cầu nối giữa technology và business, quản lý thay đổi tổ chức
3. **Governance** — Tối đa hóa lợi ích cloud, giảm thiểu rủi ro

**Technical Perspectives:**
4. **Platform** — Xây dựng và vận hành cloud platform
5. **Security** — Đảm bảo workloads đáp ứng yêu cầu bảo mật
6. **Operations** — Vận hành cloud services theo mức độ thỏa thuận với business

---

## 7 R's Migration Strategies

| Strategy | Tên gọi | Mô tả |
|----------|---------|-------|
| **Retire** | Loại bỏ | Tắt các ứng dụng không còn cần thiết |
| **Retain** | Giữ lại | Giữ ứng dụng on-premises (chưa sẵn sàng migrate) |
| **Rehost** | Lift and Shift | Di chuyển nguyên xi sang AWS (ví dụ: EC2) |
| **Relocate** | Hypervisor-level lift | Di chuyển VMware workloads sang VMware Cloud on AWS |
| **Repurchase** | Drop and Shop | Chuyển sang SaaS (ví dụ: Salesforce, ServiceNow) |
| **Replatform** | Lift, Tinker, and Shift | Tối ưu nhỏ khi migrate (ví dụ: RDS thay vì tự quản lý DB) |
| **Refactor/Re-architect** | Tái kiến trúc | Viết lại ứng dụng để tận dụng cloud-native features |

> **Exam tip:** Rehost = nhanh nhất, ít thay đổi nhất. Refactor = tốn công nhất nhưng lợi ích cao nhất.

---

## Migration Tools

### AWS Snowball
- Thiết bị vật lý để **transfer lượng data lớn** vào AWS
- Dùng khi băng thông mạng không đủ hoặc quá tốn kém
- Variants: Snowball Edge (compute + storage), Snowmobile (exabyte-scale)

### Database Replication
- Sao chép database từ on-premises sang AWS liên tục
- Dùng **AWS Database Migration Service (AWS DMS)**
- Hỗ trợ homogeneous (Oracle → Oracle) và heterogeneous (Oracle → Aurora)

### AWS Application Migration Service (MGN)
- Tự động hóa rehost (lift-and-shift) cho servers
- Replicate servers liên tục, cutover với downtime tối thiểu

---

## Migration Phases

```
Assess → Mobilize → Migrate & Modernize
```

1. **Assess** — Đánh giá trạng thái hiện tại, xác định migration readiness
2. **Mobilize** — Lập kế hoạch chi tiết, build migration factory
3. **Migrate & Modernize** — Thực hiện migration, tối ưu hóa sau khi lên cloud

---

## Exam Tips

- AWS CAF = framework lập kế hoạch, không phải tool kỹ thuật
- Biết 6 perspectives của CAF và phân loại Business vs Technical
- Biết 7 R's và khi nào dùng cái nào
- Snowball dùng khi data quá lớn để transfer qua internet
