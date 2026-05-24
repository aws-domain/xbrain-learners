# Yêu cầu Project W3 — The Database Backbone

> Deadline: **17:00 thứ Năm** (nộp diagram + Evidence Pack commit link lên Slack)
> Presentation: **thứ Sáu** (~10-12 phút)

---

## Fix W2 trước (bắt buộc trước khi thêm W3)

- [ ] Thêm nhãn encryption at rest cho tất cả storage còn thiếu (S3, EBS, RDS, DynamoDB)
- [ ] Tighten IAM policies — xóa wildcard, scope về specific ARN
- [ ] Thêm VPC Gateway Endpoint cho S3 vào route table của private subnet

---

## 4 Must-Haves

### 1. Database Layer

Chọn 1 engine phù hợp với data của app:

| Paradigm | Khi nào dùng | Engine |
|----------|-------------|--------|
| Relational | Có FK, JOIN, ACID transaction | RDS, Aurora, self-hosted Postgres/MySQL |
| Key-Value | Lookup by known key at scale, >1k writes/sec | DynamoDB |
| Document | Nested docs, flexible schema, aggregation | DocumentDB, self-hosted MongoDB |
| Graph | N-hop traversal, social graph, recommendations | Neptune |

Checklist cho mọi engine:
- [ ] Private subnet, encryption at rest, HA plan (Multi-AZ hoặc documented backup)
- [ ] Ít nhất 1 record được write + read thực sự (không chỉ tạo trên console)
- [ ] Demo 2 operations theo paradigm:
  - Relational: 1 JOIN query + 1 indexed lookup
  - Key-Value: 1 Query by PK + 1 GSI query (không dùng Scan)
  - Document: 1 aggregation pipeline + 1 indexed-field lookup
  - Graph: 1 traversal (N-hop) + 1 property/node lookup

**Data Access Pattern Log** (bắt buộc, tối đa 1 trang — thiếu thì MH1 không quá 3 điểm):
- **Part A**: 3 access patterns thực tế của app + tần suất ước tính
- **Part B**: Mỗi pattern → engine + paradigm + cơ chế cụ thể (index, PK, GSI...)
- **Part C**: "Wrong-paradigm test" — 1 pattern, 2-3 câu giải thích tại sao paradigm khác sẽ fail

### 2. AI/Bedrock Layer

- [ ] Tạo Bedrock Knowledge Base kết nối S3 bucket từ W2
- [ ] Ingest ít nhất 3 documents (sync status: Complete)
- [ ] Biết tên embedding model và vector store đã chọn
- [ ] Gọi Retrieve hoặc RetrieveAndGenerate từ **Lambda/CLI** — không phải Playground

### 3. Lambda Layer

- [ ] Ít nhất 1 Lambda function kết nối app tier với Bedrock hoặc database
- [ ] IAM execution role **không có wildcard** (`Action: "*"` hay `Resource: "*"`)
- [ ] Có trigger hoạt động: S3 event trigger hoặc API Gateway
- [ ] Output visible trong CloudWatch Logs

### 4. VPC & Networking

- [ ] Diagram có 3 tầng: public / private app / private DB
- [ ] S3 Gateway Endpoint được thêm vào route table và label trên diagram
- [ ] DB Security Group inbound rule reference **app-tier SG ID** (không phải CIDR)

---

## Evidence Pack — `docs/W3_evidence.md` (quan trọng nhất — 40% điểm)

File markdown tự viết trong group repo. Slides thứ Sáu = copy 8-12 screenshot từ file này ra.

| Section | Nội dung |
|---------|----------|
| 1. Cover | Tên nhóm, thành viên, engine + paradigm, link W2 evidence |
| 2. Data Access Pattern Log | Parts A, B, C |
| 3. Deployment Evidence | Screenshot + notes cho từng acceptance criterion |
| 4. Working Query Evidence | 2 operations theo paradigm, có kết quả thực tế |
| 5. Lambda + Bedrock Evidence | CloudWatch log + Bedrock API response từ Lambda/CLI |
| 6. VPC + Networking Evidence | Route table có S3 GW Endpoint + DB SG inbound rule |
| 7. Negative Security Test | Screenshot bị denied khi truy cập trái phép |
| 8. Bonus | (nếu có) |

**Thang điểm Criterion IV:**
- Không có Evidence Pack → cap 2
- Có screenshot nhưng không có notes → cap 3
- Đủ hết + notes meaningful → 4
- Thêm bonus scenario có measurement + reflection → 5

> ⚠️ **Post commit link lên trainer Slack trước 17:00 thứ Năm. Không post = tự động cap IV ở 2.**

---

## Bonus (tùy chọn, tối đa +0.5)

Chỉ tính nếu 4 must-haves + Evidence Pack đã hoàn chỉnh.

| Bonus | Credit |
|-------|--------|
| Partial CFN template pass `validate-template` | +0.25 |
| Ops drill: Failover, PITR, Read Replica Promotion... | +0.5 |
| Full CFN stack cho toàn bộ W3 infra | +0.5 |
| CI/CD pipeline deploy CFN | +0.5 |

---

## Rubric W3

| Criterion | Weight |
|-----------|--------|
| W2 Recap & Reflection | 10% |
| AWS Architecture | 20% |
| Individual QnA | 30% |
| **Deployment & Evidence** | **40%** |
A