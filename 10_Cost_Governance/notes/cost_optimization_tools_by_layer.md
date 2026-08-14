# Cost Optimization Tools Theo Layer Và Lifecycle

**Chủ đề (Topic):** Cost Governance, FinOps Tooling  
**Mục tiêu:** Tóm tắt các công cụ giúp hiện thực hóa cost optimization trong từng công đoạn triển khai Production.

---

## 1. Ý Chính

Cost optimization không chỉ là mở dashboard sau khi deploy. Tooling nên được đặt theo đúng lifecycle:

- **Trước khi build:** estimate cost và kiểm tra tradeoff kiến trúc.
- **Khi build/IaC:** ép tagging, policy, budget, quota, lifecycle.
- **Khi chạy Production:** quan sát cost, phát hiện anomaly, tìm saving opportunity.
- **Sau khi có usage thật:** right-size, cleanup, optimize pricing model.

---

## 2. Map Theo Lifecycle

| Công đoạn | Mục tiêu | Công cụ phù hợp |
|---|---|---|
| Requirement | Xác định budget, cost target, unit economics | AWS Pricing Calculator, spreadsheet model, FinOps unit economics |
| Architecture design | Chọn kiến trúc hợp lý về cost/reliability/performance | AWS Well-Architected Tool, AWS Pricing Calculator, Architecture Decision Record |
| IaC / Build | Chuẩn hóa resource, tagging, policy, lifecycle | Terraform, CloudFormation, CDK, AWS Config, SCP, Service Quotas, cfn-guard, Checkov, tfsec |
| Pre-production review | Kiểm tra expected cost và worst-case cost | AWS Pricing Calculator, Infracost, Well-Architected Review, load test metrics |
| Production visibility | Nhìn cost theo account/service/tag/resource | Cost Explorer, CUR/Data Exports, Athena, QuickSight, CUDOS/CID |
| Alerting | Phát hiện vượt budget hoặc spike bất thường | AWS Budgets, Cost Anomaly Detection, CloudWatch, SNS, Slack/Jira integration |
| Optimization | Tìm và ưu tiên saving opportunity | Cost Optimization Hub, Compute Optimizer, Trusted Advisor, Cost Explorer recommendations |
| Continuous FinOps | Biến insight thành hành động định kỳ | CUDOS/CID, Jira/backlog, showback/chargeback, monthly cost review |

---

## 3. Map Theo Layer

| Layer | Tool chính | Vai trò |
|---|---|---|
| Business layer | AWS Pricing Calculator, unit economics model | Ước lượng cost theo business metric như cost/user, cost/request |
| Ownership layer | AWS Organizations, Control Tower, account structure | Tách cost theo team, product, environment |
| Allocation layer | Cost Allocation Tags, Cost Categories, Billing Conductor | Gán chi phí đúng owner/cost center |
| Architecture layer | Well-Architected Tool, Pricing Calculator | Đánh giá tradeoff cost/reliability/performance |
| Guardrail layer | SCP, IAM, AWS Config, Service Quotas, IaC policy scanning | Ngăn tạo resource đắt, sai region, thiếu tag |
| Dashboard layer | Cost Explorer, CUR/Data Exports, Athena, QuickSight, CUDOS/CID | Trực quan hóa cost/usage/resource-level detail |
| Optimization loop | Cost Optimization Hub, Compute Optimizer, Trusted Advisor | Gom recommendation, right-size, cleanup, commitment planning |

---

## 4. Tool Nào Dùng Để Làm Gì?

### AWS Pricing Calculator

Dùng trước khi deploy để estimate chi phí dự kiến cho kiến trúc.

Phù hợp cho:

- architecture estimate;
- pre-production review;
- so sánh option thiết kế.

### AWS Well-Architected Tool

Dùng để review workload theo các pillar, đặc biệt là **Cost Optimization Pillar**.

Phù hợp cho:

- architecture review;
- production readiness;
- periodic workload review.

### Cost Allocation Tags / Cost Categories

Dùng để biết chi phí thuộc về team, project, product, environment hoặc cost center nào.

Không có tagging/allocation tốt thì dashboard chỉ cho biết "tốn bao nhiêu", nhưng khó biết "ai chịu trách nhiệm".

### AWS Budgets

Dùng để đặt ngưỡng budget và cảnh báo khi actual hoặc forecasted cost vượt ngưỡng.

Ví dụ:

- budget theo account;
- budget theo project tag;
- budget theo environment;
- alert ở 50%, 80%, 100%.

### Cost Anomaly Detection

Dùng để phát hiện cost spike bất thường.

Ví dụ:

- NAT Gateway tăng đột biến;
- CloudWatch Logs tăng mạnh;
- S3 request/data transfer bất thường;
- EC2/RDS usage tăng ngoài pattern cũ.

### Cost Explorer

Dùng để phân tích nhanh cost theo service, account, region, tag, usage type.

Phù hợp cho investigation hằng ngày hoặc hằng tuần.

### CUR / Data Exports + Athena

Dùng cho phân tích sâu, resource-level, custom query, chargeback/showback và unit cost calculation.

### CUDOS / Cloud Intelligence Dashboards

Dùng làm dashboard FinOps trực quan trên QuickSight, thường dựa trên CUR/Data Exports.

Phù hợp cho:

- cost visibility;
- resource-level analysis;
- leadership reporting;
- optimization review.

### Cost Optimization Hub

Dùng để gom và ưu tiên saving recommendations trên nhiều account/region.

Phù hợp khi cần biết:

- nên tối ưu cái gì trước;
- saving opportunity nào lớn nhất;
- account/region nào có nhiều waste.

### Compute Optimizer

Dùng để right-size dựa trên usage thật.

Thường áp dụng cho:

- EC2;
- Auto Scaling group;
- EBS;
- Lambda;
- RDS.

### Infracost

Dùng trong CI/CD để estimate cost change từ Terraform plan ngay trong pull request.

Phù hợp cho:

- pre-merge cost review;
- kiểm soát thay đổi hạ tầng trước khi deploy.

---

## 5. Pattern CI/CD Gợi Ý

Một flow thực tế có thể là:

1. Developer mở PR thay đổi IaC.
2. CI kiểm tra tagging, region, instance type, policy.
3. CI estimate cost change.
4. Reviewer thấy thay đổi này tăng/giảm khoảng bao nhiêu mỗi tháng.
5. Deploy Production.
6. Cost được đưa vào Cost Explorer/CUR/CUDOS.
7. Budgets và Cost Anomaly Detection gửi alert nếu lệch.
8. Cost Optimization Hub/Compute Optimizer tạo recommendation.
9. Team đưa recommendation vào engineering backlog.
10. Dashboard đo saving thật sau khi tối ưu.

---

## 6. Câu Nhớ Nhanh

- **Pricing Calculator:** estimate trước khi xây.
- **IaC + policy:** đặt guardrail khi xây.
- **Tags/Cost Categories:** phân bổ trách nhiệm khi chạy.
- **Cost Explorer/CUR/CUDOS:** nhìn thấy cost khi vận hành.
- **Budgets/Anomaly Detection:** cảnh báo khi lệch.
- **Compute Optimizer/Cost Optimization Hub:** tìm cơ hội tối ưu.
- **FinOps cadence:** biến dashboard thành hành động.

