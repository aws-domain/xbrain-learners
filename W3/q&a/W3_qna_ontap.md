# W3 Ôn Tập — Câu Hỏi + Trả Lời + Hướng Dẫn Console

> Dựa trên Evidence Pack của Petty VMCS (Nhóm 10) và W3 Requirements

---

## PHẦN 1 — DATABASE LAYER (RDS MariaDB)

---

**Q1. Tại sao nhóm chọn RDS MariaDB thay vì DynamoDB cho Petty VMCS?**

**A:** Petty VMCS có data cần FK relationships rõ ràng: `lich_hens` → `khach_hangs`, `thu_cungs`, `dich_vus`, `nhan_viens`. Khi đặt lịch hẹn, cần ACID transaction để đảm bảo tất cả FK hợp lệ và rollback nếu fail. DynamoDB không enforce referential integrity ở tầng DB — code phải tự validate bằng N lần `GetItem` và rollback bằng `TransactWriteItems` (tối đa 25 items). RDS phù hợp hơn vì: có JOIN, có FK constraint, có ACID transaction native. Engine đang dùng: **MariaDB 11.8**.

---

**Q2. DB Subnet Group là gì? Tại sao cần span 2 AZ?**

**A:** DB Subnet Group là tập hợp các subnet mà RDS có thể đặt instance vào. Cần span ít nhất 2 AZ vì:
- Multi-AZ yêu cầu Primary ở AZ1 và Standby ở AZ2
- Nếu chỉ có 1 AZ, không thể enable Multi-AZ

📍 **Console:** `RDS → Subnet groups → petty-db-subnet-group`

---

**Q3. Multi-AZ khác Read Replica như thế nào?**

**A:**
| | Multi-AZ | Read Replica |
|--|----------|-------------|
| Mục đích | High Availability (failover tự động) | Read scaling |
| Sync | Synchronous (real-time) | Asynchronous |
| Nhận read traffic | ❌ Không | ✅ Có |
| Failover | Tự động ~60-120s | Phải promote tay |

Petty dùng Multi-AZ vì ưu tiên availability tự động, không cần read scaling.

📍 **Console:** `RDS → Databases → petty-db → Configuration tab` → xem "Multi-AZ"

---

**Q4. Encryption at rest trên RDS hoạt động như thế nào? Tại sao dùng AWS-managed key thay vì customer CMK?**

**A:** RDS dùng AES-256 để encrypt data trên EBS volume. Key được quản lý bởi AWS KMS.
- **AWS-managed key (`aws/rds`):** AWS tự rotate hàng năm, không tốn thêm chi phí, không cần quản lý
- **Customer CMK:** Tự kiểm soát rotation, cần khi có compliance mandate (HIPAA, PCI-DSS...)

Petty chọn AWS-managed vì không có compliance mandate, muốn giảm operational overhead.

📍 **Console:** `RDS → Databases → petty-db → Configuration tab` → xem "Storage encrypted"

---

**Q5. Automated Backup trên RDS là gì? PITR là gì?**

**A:**
- **Automated Backup:** RDS tự động backup daily snapshot + transaction logs
- **Retention period:** 7 ngày (Petty config) — có thể restore về bất kỳ thời điểm nào trong 7 ngày
- **PITR (Point-in-Time Recovery):** Restore DB về một timestamp cụ thể, không chỉ về snapshot

📍 **Console:** `RDS → Databases → petty-db → Maintenance & backups tab`

---

**Q6. Tại sao DB Security Group dùng SG reference thay vì CIDR?**

**A:** 
- **CIDR (`10.0.0.0/16`):** Cho phép tất cả resource trong VPC kết nối vào DB — quá rộng
- **SG reference (`sg-xxxxxxxx`):** Chỉ resource thuộc ECS Security Group mới vào được DB

Nếu sau này thêm EC2 instance trong cùng subnet, nó vẫn không vào được DB vì không thuộc ECS SG. Đây là principle of least privilege.

📍 **Console:** `EC2 → Security Groups → [DB SG] → Inbound rules tab`

---

**Q7. Chạy EXPLAIN trên MariaDB để làm gì? Kết quả cần thấy gì?**

**A:** `EXPLAIN` cho biết query optimizer sẽ dùng index nào để thực thi query.

```sql
EXPLAIN SELECT * FROM lich_hens WHERE trang_thai = 'pending';
```

Kết quả cần thấy:
- `key` = `lich_hens_trang_thai_index` (không phải NULL)
- `type` = `ref` hoặc `range` (không phải `ALL` = full scan)
- `rows` = số nhỏ (không phải toàn bộ bảng)

Nếu `key = NULL` → index không được dùng → query chậm khi bảng lớn.

---

**Q8. Làm sao kết nối vào RDS để chạy query? (RDS trong private subnet)**

**A:** 3 cách:
1. **ECS Exec:** `aws ecs execute-command --cluster [cluster] --task [task-id] --command "mysql -h [RDS_ENDPOINT] -u petty -p"`
2. **Bastion host:** EC2 trong public subnet, SSH vào rồi connect RDS
3. **AWS Systems Manager Session Manager:** Không cần mở port 22

📍 **Console ECS Exec:** `ECS → Clusters → [cluster] → Tasks → [task] → Connect`

---

## PHẦN 2 — LAMBDA LAYER

---

**Q9. Lambda execution role là gì? Khác resource-based policy như thế nào?**

**A:**
- **Execution role:** IAM role Lambda *assume* khi chạy — định nghĩa Lambda được làm gì với AWS services khác (write DynamoDB, call Bedrock...)
- **Resource-based policy (function policy):** Định nghĩa ai được *invoke* Lambda function (S3, API Gateway, EventBridge...)

Petty cần execution role có quyền gọi Bedrock và đọc S3, nhưng **không có wildcard**.

📍 **Console:** `Lambda → [function] → Configuration → Permissions`

---

**Q10. Tại sao Lambda execution role không được có `Action: "*"` hoặc `Resource: "*"`?**

**A:** Wildcard vi phạm principle of least privilege:
- `Action: "*"` → Lambda có thể làm bất cứ gì (xóa S3 bucket, tạo IAM user...)
- `Resource: "*"` → Lambda có thể tác động lên bất kỳ resource nào trong account

Nếu Lambda bị compromise, attacker có toàn quyền trên AWS account. Thay vào đó:
```json
{
  "Action": ["bedrock:InvokeModel"],
  "Resource": "arn:aws:bedrock:ap-southeast-1::foundation-model/amazon.titan-text-express-v1"
}
```

📍 **Console:** `IAM → Roles → [Lambda role] → Permissions tab → xem policy JSON`

---

**Q11. S3 event trigger cho Lambda hoạt động như thế nào?**

**A:** Khi object được upload lên S3 bucket, S3 gửi event notification đến Lambda. Lambda được invoke **asynchronously** — S3 không chờ Lambda xử lý xong.

Flow: `Upload file → S3 → Event notification → Lambda invoke → CloudWatch Logs`

📍 **Console config:** `Lambda → [function] → Configuration → Triggers → Add trigger → S3`
📍 **Console verify:** `Lambda → [function] → Configuration → Triggers` → thấy S3 trigger active

---

**Q12. CloudWatch Logs của Lambda có gì? Cần thấy gì để confirm function đã chạy?**

**A:** Mỗi lần Lambda invoke tạo một log stream. Trong log stream có:
- `START RequestId: xxx Version: $LATEST` — bắt đầu invoke
- Output của function (print/console.log)
- `END RequestId: xxx`
- `REPORT RequestId: xxx Duration: X ms Billed Duration: X ms Memory Size: X MB`

Cần thấy **timestamp** và **REPORT** để confirm function đã thực sự chạy.

📍 **Console:** `CloudWatch → Log groups → /aws/lambda/[function-name] → [log stream mới nhất]`

---

**Q13. Cold start là gì? Tại sao Init Duration xuất hiện ở lần đầu?**

**A:** Cold start xảy ra khi Lambda cần tạo execution environment mới:
- Download code
- Initialize runtime
- Chạy initialization code (ngoài handler)

`Init Duration` trong REPORT chỉ xuất hiện ở cold start. Warm start (invoke lại trong thời gian ngắn) không có Init Duration vì environment được reuse.

---

## PHẦN 3 — BEDROCK KNOWLEDGE BASE

---

**Q14. Bedrock Knowledge Base là gì? RAG là gì?**

**A:**
- **Knowledge Base:** Quản lý RAG pipeline — lấy documents từ S3, chunk, embed, lưu vào vector store
- **RAG (Retrieval-Augmented Generation):** Thay vì hỏi thẳng LLM, hệ thống tìm relevant chunks từ documents rồi đưa vào prompt → LLM trả lời dựa trên context thực tế

Flow: `Query → Embed query → Search vector store → Retrieve chunks → LLM synthesize → Response`

📍 **Console:** `Amazon Bedrock → Knowledge bases`

---

**Q15. Embedding model và vector store là gì? Petty dùng gì?**

**A:**
- **Embedding model:** Chuyển text thành vector số (ví dụ: "chó bị sốt" → [0.2, 0.8, -0.1, ...])
- **Vector store:** Database lưu vectors, hỗ trợ similarity search

Các lựa chọn:
| Embedding model | Vector store |
|----------------|-------------|
| Amazon Titan Embeddings G1 - Text | OpenSearch Serverless |
| Amazon Titan Embeddings V2 | Aurora PostgreSQL |
| Cohere Embed | S3 Vectors |

📍 **Console:** `Bedrock → Knowledge bases → [KB] → xem "Embedding model" và "Vector store"`

---

**Q16. Retrieve vs RetrieveAndGenerate khác nhau như thế nào?**

**A:**
- **Retrieve:** Trả về chunks text liên quan — không gọi LLM
- **RetrieveAndGenerate:** Retrieve chunks + gọi LLM để synthesize câu trả lời

Petty dùng `RetrieveAndGenerate` để chatbot trả lời tự nhiên về chăm sóc thú cưng.

---

**Q17. Tại sao phải gọi Bedrock từ Lambda/CLI, không phải Playground?**

**A:** Playground chỉ là UI để test — không phải production flow. Requirements yêu cầu chứng minh API call thực sự từ application:
- Lambda → chứng minh serverless integration
- CLI → chứng minh biết cách gọi API programmatically

Playground không có CloudWatch log, không có IAM role, không thể verify trong Evidence Pack.

---

## PHẦN 4 — VPC & NETWORKING

---

**Q18. 3-tier architecture trong VPC là gì? Mỗi tier có gì?**

**A:**
```
Internet
    ↓
[Public Subnet] — ALB, NAT Gateway, Bastion
    ↓
[Private App Subnet] — ECS Fargate tasks
    ↓
[Private DB Subnet] — RDS MariaDB
```

- **Public:** Có route đến Internet Gateway (0.0.0.0/0 → igw)
- **Private App:** Có route đến NAT Gateway (0.0.0.0/0 → nat)
- **Private DB:** Không có route ra internet (isolated)

📍 **Console:** `VPC → Subnets` → xem từng subnet và route table

---

**Q19. S3 Gateway Endpoint là gì? Tại sao cần thêm vào route table?**

**A:** S3 Gateway Endpoint cho phép traffic từ VPC đến S3 đi qua AWS backbone network thay vì internet.

**Không có endpoint:** ECS → NAT Gateway → Internet → S3 (tốn $0.045/GB NAT processing)
**Có endpoint:** ECS → S3 Gateway Endpoint → S3 (miễn phí, không qua internet)

Lợi ích:
- Giảm chi phí NAT
- Tăng security (traffic không ra internet)
- Latency thấp hơn

📍 **Console config:** `VPC → Endpoints → Create endpoint → Service: com.amazonaws.ap-southeast-1.s3 → Gateway`
📍 **Console verify:** `VPC → Route Tables → [private route table] → Routes tab` → thấy `pl-xxxxxxxx → vpce-xxxxxxxx`

---

**Q20. Khi nào dùng NACL thay vì Security Group?**

**A:**
| | Security Group | NACL |
|--|---------------|------|
| Stateful | ✅ (return traffic tự động allow) | ❌ (phải allow cả inbound + outbound) |
| Rules | Allow only | Allow + Deny |
| Áp dụng cho | Instance/ENI | Subnet |
| Thứ tự rule | Tất cả được evaluate | Theo số thứ tự (thấp trước) |

**Dùng NACL khi:**
- Cần **block** một IP cụ thể (SG không có Deny)
- Cần bảo vệ ở tầng subnet (không phải instance)
- Ví dụ: Block IP của attacker đang DDoS

---

## PHẦN 5 — NEGATIVE SECURITY TEST

---

**Q21. Negative security test là gì? Petty test cái gì?**

**A:** Chứng minh unauthorized access bị denied — không chỉ nói "đã config đúng" mà phải show bằng chứng bị block.

Petty có 2 cách test:

**Cách 1 — Kết nối RDS từ máy local:**
```bash
mysql -h [RDS_ENDPOINT] -u petty -p --connect-timeout=10
```
Expected: `ERROR 2003 (HY000): Can't connect to MySQL server on '[endpoint]' (110)`
Lý do: RDS không có public IP, DB SG không có inbound từ 0.0.0.0/0

**Cách 2 — Gọi API không có token:**
```bash
curl -X GET https://api.petty.vn/api/lich-hen-all
```
Expected: `{"message": "Unauthenticated."}` với HTTP 401
Lý do: Route có middleware `auth:sanctum`

📍 **Console verify:** `EC2 → Security Groups → [DB SG] → Inbound rules` → confirm không có rule từ 0.0.0.0/0

---

## PHẦN 6 — CÂU HỎI Q&A THƯỜNG GẶP

---

**Q22. Trainer hỏi: "Tại sao không dùng DynamoDB cho Petty?"**

**A:** Petty VMCS là hệ thống quản lý phòng khám với data có FK relationships chặt chẽ. Khi đặt lịch hẹn, cần đảm bảo `khach_hang_id`, `thu_cung_id`, `dich_vu_id` đều tồn tại — đây là referential integrity mà DynamoDB không enforce. Ngoài ra, query "lấy lịch hẹn của khách hàng X kèm thông tin thú cưng và dịch vụ" cần JOIN 4 bảng — DynamoDB không hỗ trợ JOIN native, phải làm N+1 queries hoặc denormalize data. RDS phù hợp hơn cho use case này.

---

**Q23. Trainer hỏi: "Multi-AZ Standby có nhận read traffic không?"**

**A:** Không. Multi-AZ Standby chỉ dùng để failover tự động — nó sync data từ Primary nhưng không serve read traffic. Nếu muốn scale read, cần tạo Read Replica riêng. Petty dùng Multi-AZ vì ưu tiên high availability (tự động failover ~60-120s), không phải read scaling.

---

**Q24. Trainer hỏi: "Lambda function của nhóm làm gì?"**

**A:** Lambda function kết nối app tier với Bedrock Knowledge Base. Khi user gửi câu hỏi về chăm sóc thú cưng, Lambda:
1. Nhận request (trigger từ API Gateway hoặc S3)
2. Gọi `bedrock-agent-runtime:RetrieveAndGenerate` với câu hỏi
3. Bedrock tìm relevant chunks từ Knowledge Base
4. LLM synthesize câu trả lời
5. Lambda trả về response

IAM execution role chỉ có `bedrock:RetrieveAndGenerate` trên KB ARN cụ thể — không có wildcard.

---

**Q25. Trainer hỏi: "S3 Gateway Endpoint khác NAT Gateway như thế nào?"**

**A:**
- **NAT Gateway:** Cho phép private subnet ra internet (tốn tiền, traffic qua internet)
- **S3 Gateway Endpoint:** Cho phép private subnet kết nối S3 qua AWS backbone (miễn phí, không qua internet)

Nếu không có S3 Gateway Endpoint, ECS task kéo .env file từ S3 sẽ đi qua NAT Gateway → tốn $0.045/GB. Với endpoint, traffic đi thẳng trong AWS network → miễn phí + secure hơn.

---

**Q26. Trainer hỏi: "Nếu Primary RDS fail, chuyện gì xảy ra?"**

**A:** Với Multi-AZ:
1. RDS detect Primary fail (thường trong vài giây)
2. Tự động promote Standby thành Primary mới
3. DNS endpoint (`petty-db.xxx.rds.amazonaws.com`) được update trỏ sang instance mới
4. App reconnect tự động (Laravel có connection retry)
5. Downtime: ~60-120 giây

App không cần thay đổi connection string vì DNS endpoint không đổi.

---

**Q27. Trainer hỏi: "Làm sao biết Lambda đã thực sự chạy, không chỉ deployed?"**

**A:** CloudWatch Logs. Mỗi lần Lambda invoke tạo log stream với:
- Timestamp của invocation
- `START RequestId` → `END RequestId` → `REPORT` với duration và memory

Nếu chỉ deployed nhưng chưa invoke, sẽ không có log stream nào. Evidence Pack section 5.1 có screenshot CloudWatch log với timestamp sau khi trigger.

---

## PHẦN 7 — CHECKLIST TRƯỚC KHI PRESENT

---

**Những thứ cần biết thuộc lòng:**

- [ ] Tên DB engine: **RDS MariaDB 11.8**
- [ ] DB identifier: **petty-db** (hoặc tên thực tế)
- [ ] Subnet group: **webapp-group10-rds-subnet-group**
- [ ] Tên embedding model Bedrock: _(điền sau khi setup)_
- [ ] Tên vector store: _(điền sau khi setup)_
- [ ] Tên Lambda function: _(điền sau khi setup)_
- [ ] Lambda trigger type: S3 event / API Gateway
- [ ] IAM role của Lambda: _(tên role, không có wildcard)_

**Những thứ cần demo được live:**

1. Mở RDS console → show petty-db → Multi-AZ: Yes, Encrypted: Yes
2. Mở Lambda console → show function → Triggers active → CloudWatch log
3. Chạy JOIN query trên DB → show rows thực tế ✅ (đã có ảnh trong Evidence Pack 4.1)
4. Gọi Bedrock API → show response ✅ (đã có ảnh trong Evidence Pack 5.2)
5. Thử kết nối RDS từ ngoài → show bị denied ✅ (đã có ảnh trong Evidence Pack 7)

**Sections đã có ảnh thực tế trong Evidence Pack:**
- ✅ 3.1–3.6: RDS config (private subnet, encryption, Multi-AZ, backup, subnet group, SG)
- ✅ 3.9: Bedrock KB sync complete
- ✅ 3.10: Route table S3 endpoint
- ✅ 4.1: JOIN query với kết quả thực tế
- ✅ 4.2: EXPLAIN confirm index được dùng
- ✅ 5.1: CloudWatch log Lambda
- ✅ 5.2: Bedrock API response
- ✅ 7: Negative security test (mysql connection refused)
- ✅ 8.1: CFN validate template
- ⏳ 3.7: Lambda execution role (no wildcard)
- ⏳ 3.8: Lambda trigger active

---

*File này được tạo để ôn tập cho W3 presentation — Nhóm 10, Petty VMCS*
