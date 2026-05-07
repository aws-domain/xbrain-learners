# W4 Evidence Pack — Build an AI That Actually Answers

## Section 1 — Cover

| Item | Detail |
|------|--------|
| Nhom | G10 |
| Thanh vien | Nguyen Thi Men, Le Tran Tuan Khanh, Phan Duc Huy, Huynh Xuan Hau, Le Van Hai, Tran Manh Truong, Tran Quoc Hung, Le Viet Quoc Hung, Tran Manh Cuong, Nguyen Duc Hao |
| LLM | Claude Opus 4.6 via AWS Bedrock |
| Framework | n8n (AI Agent workflow) + Bedrock Knowledge Base + PostgreSQL + Monitoring API |
| Frontend | Custom Chat UI (HTML/JS) — deployed on S3 + CloudFront |
| Repo | `[TODO: paste repo link]` |
| Live Demo | `[TODO: paste CloudFront URL]` |

---

## Section 2 — Architecture Overview

### System Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              User (Browser)                                │
│                     CloudFront → S3 (chat_ui.html)                         │
└─────────────────────────────────┬──────────────────────────────────────────┘
                                  │ POST /webhook/.../chat
                                  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           n8n AI Agent Workflow                             │
│                                                                            │
│  Triggers: Webhook + Chat Message Received                                 │
│  Agent: AI Agent node (orchestration + tool routing)                       │
│  Model: AWS Bedrock Chat Model (Claude Opus 4.6)                           │
│  Memory: Window Buffer (session-based, multi-turn)                         │
└───┬──────────┬──────────┬──────────┬──────────┬──────────┬────────────────┘
    │          │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│  RAG  │ │Postgre│ │/services│ │/status │ │/metrics│ │/incidents│
│       │ │SQL    │ │        │ │        │ │        │ │          │
│Bedrock│ │Tool   │ │  API   │ │  API   │ │  API   │ │   API    │
│  KB   │ │       │ │        │ │        │ │        │ │          │
└───────┘ └───────┘ └────────┘ └────────┘ └────────┘ └──────────┘
```

### Component List

| Component | Chuc nang |
|-----------|-----------|
| **Chat UI** (S3 + CloudFront) | Frontend web — streaming chat, markdown render, conversation history, observability panel |
| **n8n Workflow** | Orchestration — nhan request, route den AI Agent, tra response streaming |
| **AI Agent** (n8n node) | Quyet dinh: dung KB, goi tool, hay ca hai. Xu ly multi-turn memory |
| **AWS Bedrock Chat Model** | Claude Opus 4.6 — sinh cau tra loi |
| **Bedrock Knowledge Base** | 36 markdown docs, Titan Embeddings v2, OpenSearch Serverless |
| **PostgreSQL Tool** | Query structured data: monthly_costs, incidents, sla_targets, daily_metrics |
| **Monitoring API Tools** | /services, /status/{svc}, /metrics/{svc}, /incidents, /incidents/{svc} |
| **Memory** (n8n node) | Window buffer — luu conversation history theo sessionId |

### Data Flow

1. User nhap cau hoi tren Chat UI (CloudFront)
2. UI gui POST request den n8n webhook (streaming NDJSON)
3. n8n AI Agent nhan message + session memory
4. Agent quyet dinh: retrieve tu KB, goi tool, hoac ca hai
5. Agent goi Bedrock Claude Opus 4.6 voi context (KB chunks + tool results)
6. Response stream ve UI — hien thi tung token real-time
7. Memory luu turn vao session cho follow-up

### Bedrock Knowledge Base Configuration

| Parameter | Value |
|-----------|-------|
| KB ID | `GFZGL1QMKH` |
| Embedding Model | Amazon Titan Embeddings v2 |
| Vector Store | OpenSearch Serverless |
| Chunking Strategy | Default (fixed-size, 300 tokens, 20% overlap) |
| Source | S3 bucket `geekbrain-kb-manh-uong` — 36 markdown documents |

### Deployment

| Component | Infrastructure |
|-----------|---------------|
| Chat UI | S3 + CloudFront (distribution `E38R5WH77O2NHT`) |
| n8n | Self-hosted at `n8n.duckq1linux.id.vn` |
| Bedrock KB | AWS managed (us-east-1) |
| PostgreSQL | Managed database |
| Monitoring API | Hosted API endpoints |

### Screenshot — System Running

> **ANH 1:** Screenshot Chat UI dang hoat dong
> - Truy cap CloudFront URL
> - Can thay: header (GeekBrain AI Assistant, Group 10, Claude Opus 4.6, Connected), sidebar conversations, chat area

`[DAN ANH 1 VAO DAY]`

> **ANH 2:** Screenshot n8n workflow
> - Can thay: Webhook trigger → AI Agent → Respond to Webhook
> - Cac tools: RAG, PostgreSQL, /services, /status, /metrics, /incidents

`[DAN ANH 2 VAO DAY]`

---

## Section 3 — Decision Log

### Decision 1: n8n AI Agent thay vi code Python thu cong

**Chon:** n8n workflow voi AI Agent node — orchestration visual, tool routing tu dong.

**Hoc duoc:** n8n xu ly tool routing, memory management, va streaming response out-of-the-box. Trade-off: it control hon raw code, nhung setup nhanh hon nhieu va de maintain. AI Agent node tu quyet dinh khi nao goi tool nao dua tren tool description — khong can code routing logic.

### Decision 2: Claude Opus 4.6 thay vi Haiku

**Chon:** Claude Opus 4.6 cho inference — model manh nhat.

**Hoc duoc:** Opus cho reasoning tot hon khi can multi-step (L3: quyet dinh goi tool nao, L4: resolve pronouns). Response time cham hon Haiku nhung streaming UI che duoc latency — user thay text chay lien tuc.

### Decision 3: S3 + CloudFront cho frontend thay vi local

**Chon:** Deploy Chat UI len S3 + CloudFront — public accessible.

**Hoc duoc:** Static HTML khong can server, chi phi gan nhu $0, ai cung truy cap duoc. OAC (Origin Access Control) dam bao S3 bucket khong can public — chi CloudFront moi doc duoc. Demo live chi can share URL.

### Decision 4: PostgreSQL thay vi SQLite

**Chon:** PostgreSQL (managed) thay vi SQLite local.

**Hoc duoc:** n8n co native PostgreSQL node — ket noi truc tiep, khong can code. Data persist va accessible tu bat ky dau. SQLite chi phu hop khi chay local.

### Dieu khong hoat dong

`[TODO: dien 1 thu da thu ma fail. Vi du:]`
`- Thu dung Webhook node truc tiep nhung Chat UI bi loi "problem executing workflow" vi AI Agent chi ket noi voi Chat trigger node → chuyen sang dung Chat trigger URL`
`- Hoac: RetrieveAndGenerate API khong cho control prompt → chuyen sang Retrieve + tu build prompt trong n8n`

---

## Section 4 — Per-Level Evidence

### L1 — Simple RAG (2.0 diem)

**Cach hoat dong:** User hoi cau hoi don gian → n8n AI Agent goi Bedrock KB (RAG tool) → retrieve chunks → Claude tra loi dua tren context.

**Test Results:**

| Question | Expected | Actual | Status |
|----------|----------|--------|--------|
| Who leads Team Platform? | Alex Chen | Alex Chen leads Team Platform... | PASS |
| What is PaymentGW's API rate limit? | 1000 req/min | 1,000 requests per minute per merchant API key | PASS |
| What authentication method does PaymentGW use? | API key + HMAC-SHA256 | HMAC-SHA256 signature with X-API-Key and X-Signature headers | PASS |
| What programming language is AuthSvc written in? | Go | Go | PASS |

**Proof — RAG retrieval:**

> **ANH 3:** Screenshot Chat UI hien thi cau tra loi L1
> - Hoi: "Who leads Team Platform and what services do they own?"
> - Can thay: answer dung (Alex Chen, PaymentGW, AuthSvc) + sources cited

`[DAN ANH 3 VAO DAY]`

---

### L2 — Multi-Source Retrieval (3.0 diem)

**Cach hoat dong:** Cau hoi yeu cau thong tin tu nhieu docs hoac resolve conflict giua docs → AI Agent retrieve nhieu chunks (K=10) → system prompt chi dan uu tien version moi nhat.

**Conflict Resolution Test:**

Question: "What is PaymentGW's API rate limit?"
- KB retrieve ca `api_reference_v1_archived.md` (500 rpm) va `api_reference_v2.md` (1000 rpm)
- **System answer:** 1000 req/min (v2 is current, v1 is archived)

**Multi-doc Synthesis Test:**

Question: "Can Team Commerce deploy a fix on Friday night for a P1 bug?"
- Tong hop: deployment_policy.md + incident_response_policy.md + team info
- **System answer:** Co the deploy voi P1 exception process + approval

**Proof:**

> **ANH 4:** Screenshot conflict resolution
> - Hoi: "What is PaymentGW's API rate limit?" hoac "What lessons were common across March 2026 incidents?"
> - Can thay: answer acknowledge conflict hoac tong hop tu nhieu source

`[DAN ANH 4 VAO DAY]`

---

### L3 — Tool-Augmented RAG (4.0 diem)

**Cach hoat dong:** Cau hoi yeu cau so lieu khong co trong docs → AI Agent quyet dinh goi tool (PostgreSQL cho historical data, Monitoring API cho live data) → tra ve so lieu chinh xac.

**Available Tools trong n8n:**

| Tool | Chuc nang | Data source |
|------|-----------|-------------|
| PostgreSQL | Query costs, incidents, SLA, daily metrics | Database |
| /services | List tat ca services | Monitoring API |
| /status/{svc} | Live status cua 1 service | Monitoring API |
| /metrics/{svc} | Current latency, error rate, req/min | Monitoring API |
| /incidents | Lich su incidents | Monitoring API |
| /incidents/{svc} | Incidents cua 1 service | Monitoring API |

**Database Query Tool Test:**

Question: "What was PaymentGW's total infrastructure cost in Q1 2026?"
- AI Agent goi PostgreSQL tool
- Query: `SELECT SUM(total_cost) FROM monthly_costs WHERE service='PaymentGW' AND month IN ('2026-01','2026-02','2026-03')`
- **System answer:** $16,500

**Service Metrics Tool Test:**

Question: "What is PaymentGW's current p99 latency?"
- AI Agent goi /metrics/PaymentGW
- **System answer:** ~185ms (from live API)

**Combined Tools Test:**

Question: "Is NotificationSvc meeting its SLA targets?"
- Tool 1: /metrics/NotificationSvc → current latency, error rate
- Tool 2: PostgreSQL → SLA targets
- **System answer:** No — vượt ngưỡng cả latency và error rate

**Proof — Tool invocation:**

> **ANH 5 (QUAN TRONG NHAT):** Screenshot Chat UI cho cau hoi L3
> - Hoi: "What was PaymentGW's total infrastructure cost in Q1 2026?"
> - Can thay: answer voi so lieu chinh xac ($16,500)
> - Neu co Observability panel: thay tool call trong Raw Response

`[DAN ANH 5 VAO DAY]`

> **ANH 6:** Screenshot n8n execution log cho L3 question
> - Vao n8n → Executions → chon execution cua cau hoi L3
> - Can thay: AI Agent → PostgreSQL tool call → result → final response
> - DAY LA PROOF QUAN TRONG NHAT — chung minh tool duoc goi that

`[DAN ANH 6 VAO DAY]`

---

### L4 — Memory / Multi-Turn (1.0 diem)

**Cach hoat dong:** n8n Memory node luu conversation history theo sessionId. Moi chat session trong UI co sessionId rieng → AI Agent nhan full history → resolve pronouns tu turn truoc.

**Memory Strategy:** Window Buffer (n8n built-in) — luu N turns gan nhat, gui kem moi request.

**Conversation Test:**

| Turn | Question | Answer | Pronoun Resolved |
|------|----------|--------|-----------------|
| 1 | Which service had the highest cost in March? | PaymentGW ($7,500) | — |
| 2 | Why did its costs spike? | Circuit breaker incident → cost spike | its → PaymentGW |
| 3 | Which team is responsible? | Team Platform, led by Alex Chen | (context: PaymentGW) |
| 4 | The postmortem mentioned a review deadline. Is it overdue? | April 15, 2026 — yes, overdue | the postmortem → INC005 |

**Proof:**

> **ANH 7:** Screenshot Chat UI — multi-turn conversation
> - Hoi 4 cau lien tiep trong 1 chat session
> - Can thay: AI resolve dung "its", "that service", "their team"
> - Sidebar hien thi conversation title

`[DAN ANH 7 VAO DAY]`

---

## Section 5 — Reflection

### Level kho nhat: L3 (Tool-Augmented RAG)

**Ly do:**
1. Tool description phai du ro de AI Agent chon dung tool — mo ho la goi nham
2. PostgreSQL schema phai khop voi cau hoi — AI Agent tu sinh SQL nen can table/column names ro rang
3. Monitoring API endpoints phai active — neu down thi AI hallucinate so lieu
4. So lieu phai chinh xac tuyet doi — sai 1 so la 0 diem

### Neu co them 1 ngay

Xay dung Observability Dashboard day du hon (Bonus A) — hien thi pipeline internals real-time trong Chat UI: chunks retrieved voi scores, tool calls voi params va results, LLM reasoning steps. Hien tai chi co Raw Response JSON — chua parse chi tiet.

---

## Bonus — Observability Panel (Bonus A, +0.5)

Chat UI co san panel "Pipeline Observability" (toggle button goc phai):
- **Timing:** Tong thoi gian response (ms)
- **Raw Response:** Full JSON response tu n8n — hien thi tool calls, outputs
- Streaming real-time — thay duoc khi nao AI dang "thinking" vs "responding"

> **ANH 8:** Screenshot Observability panel dang mo
> - Bam nut "Observability" → panel hien ra ben phai
> - Can thay: Timing + Raw Response JSON

`[DAN ANH 8 VAO DAY]`

---

## W3 Feedback — Da Address

| W3 Feedback | Da fix trong W4 |
|-------------|-----------------|
| Placeholder Bedrock KB chua dien (Embedding model, Vector store, Chunking strategy) | Section 2: Titan Embeddings v2, OpenSearch Serverless, fixed-size 300 tokens 20% overlap |
| Chua co evidence Secrets Manager / IAM DB auth | n8n credentials managed securely trong n8n credential store (encrypted at rest). DB connection string khong expose trong code. |
| IAM policy JSON chua co text | CloudFront OAC policy da configure — chi CloudFront moi access duoc S3. Bedrock access qua n8n AWS credentials voi scoped permissions: `bedrock:InvokeModel`, `bedrock:Retrieve` |
