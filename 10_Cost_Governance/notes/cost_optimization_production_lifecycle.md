# Cost Optimization Trong Quy Trình Triển Khai Production

**Chủ đề (Topic):** Cost Governance, FinOps, Production Readiness  
**Mục tiêu:** Hiểu cost optimization bắt đầu từ công đoạn nào trong lifecycle triển khai hệ thống lên Production, dựa trên dữ liệu nào, và dashboard đóng vai trò gì.

---

## 1. Ý Chính

Cost Optimization không nên được hiểu là một hoạt động "sau khi deploy xong rồi mở dashboard xem chỗ nào đắt". Trong môi trường Production trưởng thành, cost optimization là một **non-functional requirement**, tương tự như Security, Reliability, Observability, Maintainability.

Nói cách khác:

> Mỗi quyết định kỹ thuật đều tạo ra một cost behavior.

Dashboard chỉ là một lớp visibility và feedback loop. Nó giúp team nhìn thấy chi phí, nhưng không tự tạo ra quyết định tối ưu. Quyết định tối ưu đến từ việc hiểu business outcome, workload pattern, architecture tradeoff, ownership, budget, và dữ liệu vận hành thật.

AWS Well-Architected Cost Optimization Pillar cũng đặt cost optimization vào toàn bộ quá trình **design, delivery, and maintenance** của workload, không chỉ riêng giai đoạn vận hành sau Production.

---

## 2. Cost Optimization Bắt Đầu Từ Đâu?

Cost optimization bắt đầu từ rất sớm: **requirement và architecture phase**.

Trước khi chọn EC2, Lambda, RDS, DynamoDB, EKS, NAT Gateway, CloudFront hay bất kỳ service nào, team cần trả lời:

- Hệ thống này phục vụ business outcome gì?
- Mức SLO/SLA cần đạt là bao nhiêu?
- Traffic pattern dự kiến ra sao?
- Workload là always-on, bursty, event-driven, batch, streaming hay request/response?
- Data access pattern là hot, warm, cold, archival hay analytical?
- Có cần multi-AZ, multi-region, DR, active-active hay chỉ backup/restore?
- Cost acceptable là bao nhiêu?
- Unit economics cần đo là gì?

Ví dụ về unit economics:

- cost per user
- cost per transaction
- cost per order
- cost per API request
- cost per GB processed
- cost per tenant
- cost per training job

Điểm quan trọng: cost optimization không phải là "giảm tiền càng nhiều càng tốt". Mục tiêu đúng là **đạt business value với mức cost hợp lý**. Một hệ thống rẻ nhưng không đạt SLA, không scale được, hoặc gây mất dữ liệu thì không phải tối ưu.

---

## 3. Production Lifecycle Nhìn Từ Góc Độ Cost

### 3.1 Requirement Phase

Đây là nơi xác định "cost có ý nghĩa gì" đối với workload.

Các câu hỏi chính:

- Business value của workload là gì?
- Cost target hoặc budget envelope là bao nhiêu?
- Cost được đo theo tổng bill hay theo unit business?
- Mức availability cần thiết là gì?
- Mức performance cần thiết là gì?
- Có workload nào cần tách riêng vì có cost profile khác nhau không?

Ví dụ:

- Một internal admin tool có thể không cần multi-region.
- Một payment system có thể chấp nhận cost cao hơn để đổi lấy reliability.
- Một batch analytics job có thể dùng Spot hoặc chạy theo schedule.
- Một public API có thể cần autoscaling, caching, rate limiting để kiểm soát cost theo request volume.

Kết quả mong muốn của phase này:

- Có cost objective rõ ràng.
- Có business metric để gắn với cost.
- Có budget hoặc cost guardrail sơ bộ.
- Có assumption về traffic và growth.

---

### 3.2 Architecture And Design Phase

Đây là phase có tác động lớn nhất đến chi phí dài hạn.

Một số quyết định architecture ảnh hưởng trực tiếp tới cost:

- compute model: EC2, ECS, EKS, Lambda, Fargate, Batch
- database model: RDS, Aurora, DynamoDB, DocumentDB, OpenSearch, Redshift
- storage model: S3 Standard, Intelligent-Tiering, Glacier, EBS, EFS
- network path: public internet, NAT Gateway, VPC Endpoint, Transit Gateway, CloudFront
- availability pattern: single-AZ, multi-AZ, multi-region
- scaling pattern: manual, scheduled scaling, target tracking, queue-based scaling, serverless
- data retention: logs, backups, snapshots, object lifecycle
- observability depth: metrics, logs, traces, profiling

Các câu hỏi cần đặt:

- Dịch vụ nào phù hợp với demand pattern?
- Có đang over-engineer HA/DR so với requirement không?
- Có traffic nào đi qua NAT Gateway không cần thiết không?
- Có thể dùng VPC Endpoint để giảm data transfer/NAT processing cost không?
- Có nên dùng CloudFront/cache để giảm origin load không?
- Database có cần provision lớn ngay từ đầu không?
- Có thể tách read/write, hot/cold data, synchronous/asynchronous flow không?

Ví dụ:

- Workload có traffic không đều có thể phù hợp với Lambda hoặc autoscaling.
- Workload chạy 24/7 với baseline ổn định có thể phù hợp với Savings Plans sau khi có dữ liệu usage.
- Batch workload linh hoạt thời gian có thể dùng Spot hoặc schedule ngoài giờ cao điểm.
- Data lake cần lifecycle policy để chuyển dữ liệu cũ sang storage class rẻ hơn.

Kết quả mong muốn của phase này:

- Có architecture decision record ghi rõ tradeoff cost/reliability/performance.
- Có high-level cost estimate.
- Có worst-case scaling estimate.
- Có strategy cho tagging, account, budget, observability, retention.

---

### 3.3 Build And IaC Phase

Ở phase này, cost optimization chuyển thành governance và guardrail trong code.

Các thực hành thường dùng:

- định nghĩa infrastructure bằng CloudFormation, Terraform, CDK hoặc SAM;
- bắt buộc tagging cho resource;
- tách account hoặc environment: dev, staging, prod, sandbox;
- đặt default capacity nhỏ và scale theo metric;
- tạo lifecycle policy cho storage/log/snapshot;
- dùng policy để giới hạn region, instance family, GPU instance, high-cost service;
- đặt quota hoặc service limit phù hợp;
- tự động cleanup resource tạm;
- tạo budget và alert theo account/team/project/environment.

Tagging/cost allocation rất quan trọng vì không có ownership thì dashboard chỉ trả lời được "tốn bao nhiêu", nhưng không trả lời được "ai chịu trách nhiệm" hoặc "business unit nào tạo ra spend".

Một bộ tag cơ bản có thể gồm:

- `Owner`
- `Team`
- `Project`
- `Application`
- `Environment`
- `CostCenter`
- `BusinessUnit`
- `ManagedBy`

Kết quả mong muốn của phase này:

- Resource sinh ra từ IaC có metadata đầy đủ.
- Có budget/alert hoặc ít nhất có rule để tạo budget theo environment.
- Có guardrail ngăn các cấu hình quá đắt hoặc sai vùng.
- Có policy cho log retention, backup retention, object lifecycle.

---

### 3.4 Pre-Production Review Phase

Trước khi đưa hệ thống lên Production, nên có một cost review tương tự security review hoặc operational readiness review.

Checklist nên hỏi:

- Estimated monthly cost cho expected load là bao nhiêu?
- Worst-case cost nếu autoscaling đạt max capacity là bao nhiêu?
- Cost impact của multi-AZ hoặc multi-region là gì?
- Cost impact của logging, metrics, tracing là gì?
- Log retention đã hợp lý chưa?
- Backup/snapshot retention đã hợp lý chưa?
- Có budget, forecast, anomaly alert chưa?
- Có dashboard theo service/account/tag chưa?
- Có owner nhận alert chưa?
- Có runbook nếu cost spike bất thường chưa?
- Có resource nào chỉ dùng trong migration/cutover nhưng quên cleanup không?

Những lỗi hay làm Production đắt ngầm:

- bật logging quá chi tiết nhưng retention quá dài;
- tạo NAT Gateway cho mọi private subnet mà không tính traffic pattern;
- để traffic lớn đi qua NAT thay vì VPC Endpoint hoặc thiết kế network khác;
- database overprovision từ đầu;
- bật multi-AZ/multi-region theo thói quen mà không gắn với RTO/RPO;
- metric cardinality quá cao;
- snapshot giữ mãi không có lifecycle;
- sandbox/dev resource không tự tắt;
- EBS volume, Elastic IP, Load Balancer, NAT Gateway bị bỏ quên.

Kết quả mong muốn của phase này:

- Có go/no-go cost readiness.
- Có expected cost baseline.
- Có anomaly threshold.
- Có dashboard và alert owner.
- Có cleanup plan cho tài nguyên tạm.

---

### 3.5 Production Operate Phase

Sau khi lên Production, dashboard và billing data bắt đầu có vai trò lớn.

Dashboard giúp trả lời:

- Tổng cost đang là bao nhiêu?
- Cost tăng ở service nào?
- Account/team/project/environment nào tạo spend?
- Region nào đang tiêu nhiều?
- Usage type nào gây spike?
- Resource nào là top cost driver?
- Cost hiện tại có lệch so với forecast không?
- Unit cost có tăng không?
- Optimization đã làm có tạo ra saving thật không?

Ở phase này, team không chỉ nhìn bill cuối tháng. Team cần quan sát cost như một operational signal.

Ví dụ:

- API request tăng 2 lần nhưng cost tăng 5 lần: có thể scaling hoặc caching có vấn đề.
- Cost tăng mạnh ở NAT Gateway: có thể traffic path sai hoặc thiếu VPC Endpoint.
- Cost tăng ở CloudWatch Logs: có thể log volume hoặc retention sai.
- Cost tăng ở S3: có thể object lifecycle hoặc data duplication chưa tốt.
- Cost tăng ở RDS: có thể instance size quá lớn, storage autoscaling tăng, backup retention dài.

Kết quả mong muốn của phase này:

- Có visibility theo owner và service.
- Có anomaly detection.
- Có forecast so với budget.
- Có backlog optimization dựa trên dữ liệu thật.
- Có cadence review định kỳ.

---

### 3.6 Post-Production Optimization Phase

Khi đã có dữ liệu usage thật, team mới có thể tối ưu chính xác hơn.

Các hướng tối ưu thường gặp:

- right-sizing EC2, RDS, Lambda memory, EBS volume;
- tắt hoặc xóa idle resources;
- tune autoscaling policy;
- chuyển storage class;
- giảm log volume hoặc giảm retention;
- tối ưu query để giảm scan data;
- dùng cache để giảm backend/database load;
- dùng queue/batch để làm mượt spike;
- mua Savings Plans hoặc Reserved Instances khi usage ổn định;
- dùng Spot cho workload phù hợp;
- loại bỏ architecture component không còn cần thiết;
- review lại HA/DR nếu requirement thay đổi.

Điểm cần nhớ: không nên mua commitment quá sớm khi chưa hiểu usage baseline. Savings Plans/Reserved Instances là tối ưu pricing model, không sửa được architecture sai hoặc resource overprovision nghiêm trọng.

Kết quả mong muốn của phase này:

- Cost giảm nhưng không phá SLO/SLA.
- Unit cost ổn định hoặc giảm khi scale.
- Optimization được đo bằng dữ liệu trước/sau.
- Các quyết định cost được đưa lại vào architecture và IaC.

---

## 4. Các Layer Trong Cost Optimization

Có thể nhìn cost optimization qua 7 layer:

| Layer | Mục đích | Dựa trên cái gì |
|---|---|---|
| Business layer | Biết cost có đáng không | revenue, margin, SLO, SLA, unit economics |
| Ownership layer | Biết ai chịu trách nhiệm | account, team, product, cost center, environment |
| Allocation layer | Gán cost đúng nơi | tags, account structure, cost categories |
| Architecture layer | Chọn thiết kế ít lãng phí | demand pattern, HA/DR, compute/data/network pattern |
| Guardrail layer | Ngăn spend sai từ sớm | budgets, policy, quota, IaC standards |
| Observability/dashboard layer | Nhìn thấy cost và usage | billing data, CUR/Data Exports, metrics, logs |
| Optimization loop layer | Biến insight thành hành động | backlog, review cadence, anomaly response, rightsizing |

Dashboard nằm ở **Observability/dashboard layer**, không phải toàn bộ cost optimization.

Nếu không có Business layer, dashboard chỉ là biểu đồ tiền.

Nếu không có Ownership layer, không ai chịu trách nhiệm.

Nếu không có Allocation layer, cost không được phân bổ đúng.

Nếu không có Architecture layer, team chỉ tối ưu phần ngọn.

Nếu không có Guardrail layer, lỗi cost vẫn lặp lại.

Nếu không có Optimization loop layer, insight không biến thành hành động.

---

## 5. Pattern Vận Hành Theo FinOps

FinOps Foundation mô tả vòng lặp phổ biến là:

1. **Inform**
2. **Optimize**
3. **Operate**

### Inform

Mục tiêu là tạo visibility và accountability.

Dữ liệu cần có:

- cost by account
- cost by service
- cost by region
- cost by tag
- cost by team/product/environment
- usage trend
- forecast
- anomaly
- unit cost

### Optimize

Mục tiêu là tìm và thực hiện cơ hội tối ưu.

Ví dụ:

- right-sizing
- idle resource cleanup
- storage lifecycle
- commitment discount
- architecture tuning
- autoscaling tuning
- data transfer optimization
- log/metric optimization

### Operate

Mục tiêu là biến cost management thành quy trình vận hành thường xuyên.

Ví dụ:

- cost review hàng tuần hoặc hàng tháng;
- owner phải phản hồi cost anomaly;
- optimization backlog được ưu tiên như engineering work;
- budget threshold có escalation;
- platform team cung cấp guardrail;
- product/engineering/finance cùng nhìn một bộ số liệu.

---

## 6. Dashboard Quản Lý Cost Nên Dựa Trên Cái Gì?

Dashboard tốt không nên chỉ hiển thị tổng bill. Nó nên được thiết kế từ câu hỏi vận hành.

### Nhóm câu hỏi về business

- Cost per user/request/order là bao nhiêu?
- Unit cost có giảm khi scale không?
- Product/team nào tạo ra cost và business value tương ứng là gì?
- Cost có vượt budget không?

### Nhóm câu hỏi về engineering

- Service nào là top cost driver?
- Resource nào đắt nhất?
- Usage type nào tăng bất thường?
- Region nào có cost lạ?
- Data transfer cost đến từ đâu?
- Log/metric/tracing cost có bất thường không?

### Nhóm câu hỏi về governance

- Resource nào thiếu tag?
- Cost nào chưa phân bổ được?
- Account nào vượt budget?
- Environment nào có resource chạy ngoài giờ?
- Có resource idle/orphaned không?

### Nhóm câu hỏi về optimization

- Recommendation nào có saving lớn nhất?
- Optimization nào đã thực hiện?
- Saving trước/sau là bao nhiêu?
- Có workload nào đủ ổn định để mua Savings Plans/Reserved Instances không?
- Có workload nào phù hợp Spot không?

---

## 7. Ví Dụ Flow Chuẩn Khi Deploy Production

Một flow thực tế có thể như sau:

1. Xác định business metric và cost target.
2. Ước lượng traffic, data volume, retention, availability.
3. Chọn architecture dựa trên workload pattern.
4. Ước lượng cost theo expected load và worst-case load.
5. Định nghĩa tagging, account boundary, budget, alert.
6. Viết IaC với default capacity hợp lý và lifecycle policy.
7. Review cost trước Production.
8. Deploy Production.
9. Theo dõi dashboard, anomaly, forecast, unit cost.
10. Sau khi có usage thật, right-size và tối ưu pricing model.
11. Đưa bài học quay lại architecture, IaC, guardrail và checklist.

---

## 8. Một Cách Nói Khi Phỏng Vấn

Có thể trả lời như sau:

> Cost optimization should start from the requirement and architecture phase, not after production. I would first define business value, expected demand, SLO/SLA, budget, and unit economics. During design, I evaluate compute, data, network, scaling, availability, and retention choices because those decisions create most of the long-term cost behavior. During build and IaC, I add tagging, account separation, budgets, guardrails, and lifecycle policies. Before production, I run a cost readiness review including expected cost, worst-case autoscaling cost, logging, backup, and data transfer impact. After production, dashboards based on billing and usage data provide visibility, anomaly detection, forecasting, and unit-cost tracking. Then the team uses that data to right-size, remove idle resources, tune scaling, optimize storage, and consider Savings Plans or Reserved Instances when usage is stable.

Phiên bản ngắn hơn:

> Dashboard is not the starting point of cost optimization. It is the feedback layer. Real cost optimization starts from requirements and architecture, then continues through IaC guardrails, production readiness checks, operational visibility, and continuous FinOps review.

---

## 9. Tài Liệu Tham Khảo

- [AWS Well-Architected Framework - Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [AWS Well-Architected - Cost Optimization Definition](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/definition.html)
- [AWS Well-Architected - Practice Cloud Financial Management](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/practice-cloud-financial-management.html)
- [AWS Well-Architected - Optimize Over Time](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/optimize-over-time.html)
- [AWS Tagging Best Practices - Cost Allocation Tags](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/cost-allocation-tags.html)
- [FinOps Foundation - Principles](https://www.finops.org/framework/principles/)
- [FinOps Foundation - Phases](https://www.finops.org/framework/phases/)
