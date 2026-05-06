# L3 - Grounded Computation: Tools Integration

> **Prerequisites:** 
> - ✅ Hoàn thành L1 + L2
> - ✅ Học Course 7-8 (Multi-Agent Collaboration, AgentCore Tools)

## Mục tiêu

Nâng cấp chatbot để:
- Gọi external tools (monitoring API, database)
- Trả lời câu hỏi cần live data (không có trong docs)
- Implement function calling với Bedrock Agents
- Trả lời 10 câu hỏi L3 từ `questions/student/L3_questions.json`

## Sự khác biệt giữa L2 và L3

| Aspect | L2 | L3 |
|--------|----|----|
| **Data source** | Knowledge Base only | KB + Tools (API, DB) |
| **Questions** | "What is the policy?" | "What is the current value?" |
| **Example** | "What is SLA target?" | "What is current latency?" |
| **Complexity** | Retrieval + Synthesis | Retrieval + Tool calling + Synthesis |

---

## Key Concepts

### 1. Why Tools?

**L2 can answer:**
```
Q: What is PaymentGW's SLA target for p99 latency?
A: 200ms (from sla_policy.md)
```

**L2 CANNOT answer:**
```
Q: What is PaymentGW's current p99 latency?
A: ❌ Not in knowledge base - this is live data!
```

**L3 with tools:**
```
Q: What is PaymentGW's current p99 latency?
→ Call tool: get_service_metrics("PaymentGW")
→ Tool returns: {"latency_p99_ms": 185}
A: ✓ Approximately 185ms
```

**❓ PRACTICE QUESTION 1:**
Trong course "Multi-Agent Collaboration", bạn học về khi nào cần tools.
List 5 loại câu hỏi mà L2 không trả lời được nhưng L3 có thể.

---

### 2. Tool Types for GeekBrain

#### Tool 1: Service Metrics (Live API)
```python
def get_service_metrics(service_name: str) -> dict:
    """
    Get current metrics from monitoring API.
    
    Returns:
    - latency_p99_ms
    - error_rate_percent
    - requests_per_minute
    - cpu_percent
    - memory_percent
    - uptime_percent
    """
```

**Example questions:**
- "What is PaymentGW's current latency?"
- "Is NotificationSvc meeting its SLA?"
- "Which service has highest CPU usage?"

---

#### Tool 2: Database Query (Historical Data)
```python
def query_costs(service: str = None, month: str = None) -> list:
    """Query monthly costs from database."""

def query_incidents(service: str = None, severity: str = None) -> list:
    """Query incident history."""

def query_sla_targets(service: str) -> dict:
    """Query SLA targets."""

def query_daily_metrics(service: str, start_date: str, end_date: str) -> list:
    """Query historical metrics."""
```

**Example questions:**
- "What was PaymentGW's cost in March 2026?"
- "How many P1 incidents in Q1?"
- "Compare current latency to Q1 average"

---

### 3. Function Calling with Bedrock

**Two approaches:**

#### Approach A: Bedrock Agents (Recommended)
- AWS manages tool routing
- Declarative tool definitions
- Built-in retry logic

#### Approach B: Manual Function Calling
- You handle tool routing
- More control but more code
- Need to parse LLM output

**❓ PRACTICE QUESTION 2:**
Trong course "AgentCore Tools", bạn học về 2 approaches.
So sánh ưu/nhược điểm của mỗi cách.
Với GeekBrain project, nên chọn cách nào? Tại sao?

---

## Architecture

```
User: "What is PaymentGW's current latency?"
    ↓
[1] Bedrock Agent receives question
    ↓
[2] Agent decides: Need tool "get_service_metrics"
    ↓
[3] Lambda function executes tool
    ↓
[4] Tool returns: {"latency_p99_ms": 185}
    ↓
[5] Agent generates answer: "Approximately 185ms"
    ↓
User receives answer
```

---

## AWS Setup - Step by Step

### Step 1: Setup Monitoring API

```bash
cd ../data_package/scripts/

# Install dependencies
uv sync

# Start API
uv run uvicorn monitoring_api:app --reload --port 8000
```

**Test API:**
```bash
curl http://localhost:8000/services
curl http://localhost:8000/metrics/PaymentGW
```

**❓ PRACTICE QUESTION 3:**
Gọi API endpoint `/metrics/PaymentGW` nhiều lần.
Giá trị có thay đổi không? Tại sao?
(Hint: xem monitoring_api.py - có jitter logic)

---

### Step 2: Setup Database

```bash
cd ../data_package/scripts/

# Seed SQLite database
uv run python seed_data.py --db-type sqlite --sqlite-path geekbrain.db

# Verify data
sqlite3 geekbrain.db "SELECT COUNT(*) FROM monthly_costs;"
# Should return: 36

sqlite3 geekbrain.db "SELECT COUNT(*) FROM incidents;"
# Should return: 8
```

**❓ PRACTICE QUESTION 4:**
Query database để trả lời:
1. Service nào có total cost cao nhất trong Q1 2026?
2. Có bao nhiêu P1 incidents?
3. Service nào có nhiều incidents nhất?

---

### Step 3: Create Lambda Functions for Tools

#### 3.1. Create Lambda execution role

```bash
# Create IAM role
aws iam create-role \
  --role-name GeekBrainToolsLambdaRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach basic execution policy
aws iam attach-role-policy \
  --role-name GeekBrainToolsLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

---

#### 3.2. Package and deploy Lambda

```bash
cd L3_tools/lambda/

# Package dependencies
pip install -r requirements.txt -t package/
cp tools_handler.py package/
cd package/
zip -r ../tools_lambda.zip .
cd ..

# Create Lambda function
aws lambda create-function \
  --function-name geekbrain-tools \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/GeekBrainToolsLambdaRole \
  --handler tools_handler.lambda_handler \
  --zip-file fileb://tools_lambda.zip \
  --timeout 30 \
  --environment Variables="{
    MONITORING_API_URL=http://YOUR_EC2_IP:8000,
    DB_PATH=/tmp/geekbrain.db
  }"
```

**❓ PRACTICE QUESTION 5:**
Lambda function cần access monitoring API (localhost:8000).
Nhưng Lambda không thể gọi localhost!
Giải pháp:
1. Deploy API lên EC2/ECS và dùng public URL
2. Dùng API Gateway + Lambda
3. Mock data trong Lambda (for practice)

Bạn chọn cách nào? Tại sao?

---

### Step 4: Create Bedrock Agent

#### 4.1. Create Agent

```bash
# Via AWS Console: Bedrock → Agents → Create Agent

# Agent details:
Name: geekbrain-agent
Description: GeekBrain AI with tools access
Model: Claude 3 Sonnet
Instructions: |
  You are GeekBrain AI Assistant with access to live monitoring data and historical records.
  
  Use tools when:
  - User asks about CURRENT metrics (latency, CPU, errors)
  - User asks about COSTS or INCIDENTS (historical data)
  - User asks to COMPARE current vs historical
  
  Use knowledge base when:
  - User asks about policies, architecture, teams
  - User asks about HOW things work
  
  Always combine tool results with knowledge base context for complete answers.
```

---

#### 4.2. Add Action Group (Tools)

```yaml
Action Group Name: monitoring-tools

Lambda Function: geekbrain-tools

API Schema: (OpenAPI format)
openapi: 3.0.0
info:
  title: GeekBrain Monitoring Tools
  version: 1.0.0
paths:
  /metrics/{service_name}:
    get:
      operationId: get_service_metrics
      description: Get current metrics for a service
      parameters:
        - name: service_name
          in: path
          required: true
          schema:
            type: string
            enum: [PaymentGW, AuthSvc, OrderSvc, NotificationSvc, FraudDetector, ReportingSvc]
  /costs:
    get:
      operationId: query_costs
      description: Query monthly costs
      parameters:
        - name: service
          in: query
          schema:
            type: string
        - name: month
          in: query
          schema:
            type: string
  /incidents:
    get:
      operationId: query_incidents
      description: Query incident history
      parameters:
        - name: service
          in: query
          schema:
            type: string
        - name: severity
          in: query
          schema:
            type: string
```

**❓ PRACTICE QUESTION 6:**
Trong course "AgentCore Tools", bạn học về OpenAPI schema.
Tại sao cần define schema chi tiết?
Nếu thiếu `enum` cho service_name, điều gì xảy ra?

---

#### 4.3. Associate Knowledge Base

```
Knowledge Base: geekbrain-kb (from L1)
Instructions: Use KB for policy/architecture questions
```

---

#### 4.4. Prepare Agent

Click **Prepare** → Wait ~2 minutes

---

### Step 5: Test Agent in Console

Test queries:
```
1. "What is PaymentGW's current p99 latency?"
   → Should call get_service_metrics tool

2. "What was PaymentGW's cost in March 2026?"
   → Should call query_costs tool

3. "Is PaymentGW meeting its SLA?"
   → Should call BOTH get_service_metrics AND query_sla_targets
```

**❓ PRACTICE QUESTION 7:**
Test câu 3 và observe agent behavior:
- Agent gọi bao nhiêu tools?
- Thứ tự gọi như thế nào?
- Agent có synthesize kết quả từ cả 2 tools không?

---

## Code Implementation

### File structure

```
L3_tools/
├── README.md (file này)
├── lambda/
│   ├── tools_handler.py       # Lambda function
│   ├── requirements.txt
│   └── tools_lambda.zip
├── bedrock_agent_client.py    # Agent API wrapper
├── tools_pipeline.py          # RAG + Tools pipeline
├── chatbot_l3.py              # Interactive chatbot
└── test_l3.py                 # Test với 10 câu L3
```

---

## Testing

```bash
python test_l3.py
```

**Expected results:**
- L3-01 to L3-03: Direct tool calls (should pass)
- L3-04 to L3-06: Tool + KB synthesis (harder)
- L3-07 to L3-10: Multi-tool queries (hardest)

**❓ PRACTICE QUESTION 8:**
Nếu L3-04 fail ("Is PaymentGW's error rate within SLA?"):
1. Check: Agent có gọi get_service_metrics không?
2. Check: Agent có gọi query_sla_targets không?
3. Check: Agent có compare 2 values không?

Debug bằng cách enable agent trace logging.

---

## Success Criteria

- ✅ 8-10/10 câu hỏi L3 pass
- ✅ Tools được gọi đúng lúc
- ✅ Tool results được synthesize với KB context
- ✅ Multi-tool queries work
- ✅ Average response time < 8 seconds

---

## Common Issues

### Issue 1: Lambda timeout
**Symptom:** Tool call fails after 3 seconds

**Fix:** Increase Lambda timeout to 30s

---

### Issue 2: Agent không gọi tool
**Symptom:** Agent trả lời "I don't have that information" thay vì gọi tool

**Fix:** Improve agent instructions:
```
When user asks about CURRENT or LIVE data, you MUST use tools.
Never say "I don't have that information" if a tool can provide it.
```

---

### Issue 3: Tool returns error
**Symptom:** Lambda returns 500 error

**Debug:**
```bash
aws lambda invoke \
  --function-name geekbrain-tools \
  --payload '{"service_name": "PaymentGW"}' \
  response.json

cat response.json
```

---

## Next Steps

Sau khi hoàn thành L3:
1. Học **Course 9** (DynamoDB)
2. Move to **L4 - Conversation Memory**

**❓ PRACTICE QUESTION 9 (Preview L4):**
L3 có thể trả lời: "What is PaymentGW's current latency?"
L3 KHÔNG thể trả lời conversation này:

```
Turn 1: "Which service had highest cost in March?"
Bot: "PaymentGW at $7,500"

Turn 2: "What is its current latency?"
Bot: ❌ "What service are you asking about?"
```

Tại sao? Làm thế nào L4 sẽ giải quyết?
