# Building a Tagging Strategy - 4 Bước Chi Tiết

**Chủ đề (Topic):** Cost Governance, Resource Governance, Tagging
**Nguồn:** AWS Cloud Operations module "Building a tagging strategy"
**Mục tiêu:** Giải thích chi tiết 4 bước và vai trò từng thành phần trên diagram AWS Organizations.

---

## 1. Cấu Trúc Diagram Chung

Cả 4 bước dùng chung một sơ đồ, mỗi bước làm nổi bật một phần (số 1/2/3/4):

- **AWS Organizations** (khung ngoài)
  - **Management account** - nơi tạo và attach Tag Policies + Service Control Policies (SCPs).
  - **Other OUs -> Member accounts** - các account thường.
  - **Infrastructure OU -> Operations account** - chứa Tagging dashboard + Remediation mechanism (AWS Systems Manager).
- **Tagging stakeholders** (bên trái) - finance, security, operations, software engineering đóng góp yêu cầu vào **Tagging strategy** (gồm tagging dictionary, tagging policy, tagging standards).

---

## 2. Step 1 - Define a Tagging Strategy

Quyết định tag nào **bắt buộc** (mandatory), lập tagging policy và tagging standards. Stakeholder khắp công ty cung cấp thông tin để cloud team chuẩn hóa.

- Đây là bước "giấy tờ", chưa đụng AWS.
- Trả lời câu hỏi: "Cần tag gì và theo quy tắc nào?"
- Output: **tagging dictionary** - input cho Step 2.

Ví dụ tag chuẩn: `CostCenter`, `Environment`, `Owner`, `Project`, `DataClassification`.

---

## 3. Step 2 - Create Tag Policies

Vào AWS Organizations (management account), tạo **Tag Policies** và **attach** vào các OU/account liên quan.

- Tag Policy định nghĩa key/value hợp lệ (ví dụ `Environment` chỉ nhận `prod|staging|dev`).
- Sinh **resource compliance report** để biết resource nào tag đúng/sai.
- Mặc định **chỉ báo cáo**, không tự chặn. Muốn chặn cứng thì dùng SCP (xem note enforcement).

Mục tiêu bước này: áp quy tắc tập trung + hiểu hiện trạng tagging trong môi trường.

---

## 4. Step 3 - Tag Resources With AWS Systems Manager

Gắn tag thật lên resource. Ba cách:

| Cách | Dùng khi |
|---|---|
| SSM Automation | Tự động gắn tag hàng loạt qua toàn môi trường |
| Resource Groups | Bulk tag nhiều resource cùng lúc |
| Tag Editor | Gắn tag thủ công qua console |

Đây là bước thi hành trên tài nguyên thật.

---

## 5. Step 4 - Create a Dashboard

Trong **Operations account**, dựng **Tagging dashboard** hiển thị metadata (tag) của resource, đồng thời đóng vai trò **remediation mechanism**.

- Phát hiện resource thiếu tag / sai tag.
- Kích SSM Automation tự sửa.
- Là vòng lặp giám sát + tự động khắc phục liên tục.

---

## 6. Summary

Tagging strategy là quá trình lặp và cải tiến: bắt đầu nhỏ với ưu tiên trước mắt, mở rộng schema dần theo nhu cầu.

---

## 7. Liên Quan Đến Kỳ Thi SOA-C03

| Nội dung tagging | Domain thi liên quan |
|---|---|
| Dashboard, cost allocation report | D1 Monitoring/Logging |
| SSM Automation + Resource Groups bulk tag | D3 Deployment/Provisioning/Automation |
| Tag Policy, SCP, Config compliance | D4 Security/Compliance |

Điểm dễ ra đề: phân biệt **Tag Policy** (báo cáo, thuộc Organizations) với **SCP** (chặn hành động), và **cost allocation tags** phải kích hoạt ở Billing console mới xuất hiện trong Cost Explorer.
