# L4 - Conversation Memory: Multi-Turn Continuity

> **Prerequisites:** 
> - ✅ Hoàn thành L1 + L2 + L3
> - ✅ Học Course 9 (Introduction to DynamoDB)

## Mục tiêu

Nâng cấp chatbot để:
- Nhớ conversation history
- Resolve pronouns và references ("it", "its", "that service")
- Maintain context across multiple turns
- Trả lời 6 conversation scripts từ `questions/student/L4_conversation_scripts.json`

## Sự khác biệt giữa L3 và L4

| Aspect | L3 | L4 |
|--------|----|----|
| **Memory** | Stateless (mỗi query độc lập) | Stateful (nhớ conversation) |
| **Pronouns** | Cannot resolve | Can resolve |
| **Example** | Single-turn Q&A | Multi-turn dialogue |

---

## The Problem L4 Solves

**L3 conversation (FAILS):**
```
Turn 1:
User: "Which service had the highest cost in March 2026?"
Bot: "PaymentGW at $7,500"

Turn 2:
User: "What is its current latency?"
Bot: ❌ "What service are you asking about?"
       (Agent doesn't know "its" = PaymentGW)
```

**L4 conversation (WORKS):**
```
Turn 1:
User: "Which service had the highest cost in March 2026?"
Bot: "PaymentGW at $7,500"
[Store: conversation_state = {mentioned_service: "PaymentGW"}]

Turn 2:
User: "What is its current latency?"
[Retrieve: mentioned_service = "PaymentGW"]
[Resolve: "its" → "PaymentGW"]
Bot: ✓ "PaymentGW's current p99 latency is approximately 185ms"
```

**❓ PRACTICE QUESTION 1:**
Trong course "Introduction to DynamoDB", bạn học về use cases.
Tại sao DynamoDB phù hợp cho conversation memory?
- Fast read/write?
- Schema flexibility?
- Scalability?
So sánh với RDS PostgreSQL.

---

## Key Concepts

### 1. Session Management

**Session = 1 conversation**

```python
session = {
    'session_id': 'uuid-1234',
    'user_id': 'user-abc',
    'created_at': '2026-05-06T10:00:00Z',
    'last_updated': '2026-05-06T10:05:00Z',
    'turn_count': 3
}
```

**❓ PRACTICE QUESTION 2:**
Session nên expire sau bao lâu?
- 30 minutes (như web session)?
- 24 hours (như chat app)?
- Never (keep forever)?
Trade-offs?

---

### 2. Conversation History

**Store each turn:**
```python
turn = {
    'session_id': 'uuid-1234',
    'turn_number': 2,
    'timestamp': '2026-05-06T10:02:00Z',
    'user_message': 'What is its current latency?',
    'bot_response': 'PaymentGW current p99 latency is 185ms',
    'entities_mentioned': ['PaymentGW'],
    'tools_called': ['get_service_metrics']
}
```

**❓ PRACTICE QUESTION 3:**
Nên store bao nhiêu turns?
- Last 5 turns?
- Last 10 turns?
- All turns?

Context window của Claude 3 Sonnet là 200K tokens.
Với mỗi turn ~500 tokens, có thể fit bao nhiêu turns?

---

### 3. Entity Tracking

**Track entities mentioned in conversation:**
```python
entities = {
    'services': ['PaymentGW', 'AuthSvc'],
    'teams': ['Team Platform'],
    'people': ['Alex Chen'],
    'dates': ['March 2026'],
    'incidents': ['INC-005']
}
```

**❓ PRACTICE QUESTION 4:**
Làm thế nào để extract entities từ conversation?
- Regex patterns?
- NER (Named Entity Recognition)?
- LLM-based extraction?

---

## DynamoDB Schema Design

### Table 1: Sessions

```
Table: geekbrain_sessions
Partition Key: session_id (String)

Attributes:
- session_id: String (PK)
- user_id: String
- created_at: String (ISO timestamp)
- last_updated: String
- turn_count: Number
- status: String (active, expired)
- ttl: Number (Unix timestamp for auto-deletion)
```

**❓ PRACTICE QUESTION 5:**
DynamoDB TTL (Time To Live) tự động xóa expired items.
Set TTL = created_at + 24 hours.
Tại sao cần TTL? Điều gì xảy ra nếu không có?

---

### Table 2: Conversation History

```
Table: geekbrain_conversations
Partition Key: session_id (String)
Sort Key: turn_number (Number)

Attributes:
- session_id: String (PK)
- turn_number: Number (SK)
- timestamp: String
- user_message: String
- bot_response: String
- entities_mentioned: List<String>
- tools_called: List<String>
- metadata: Map
```

**❓ PRACTICE QUESTION 6:**
Tại sao dùng composite key (session_id + turn_number)?
Benefit của sort key là gì?
Hint: Query patterns - "Get last 5 turns of session X"

---

## AWS Setup - Step by Step

### Step 1: Create DynamoDB Tables

```bash
# Create Sessions table
aws dynamodb create-table \
  --table-name geekbrain_sessions \
  --attribute-definitions \
    AttributeName=session_id,AttributeType=S \
  --key-schema \
    AttributeName=session_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Enable TTL
aws dynamodb update-time-to-live \
  --table-name geekbrain_sessions \
  --time-to-live-specification "Enabled=true, AttributeName=ttl"

# Create Conversations table
aws dynamodb create-table \
  --table-name geekbrain_conversations \
  --attribute-definitions \
    AttributeName=session_id,AttributeType=S \
    AttributeName=turn_number,AttributeType=N \
  --key-schema \
    AttributeName=session_id,KeyType=HASH \
    AttributeName=turn_number,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

---

### Step 2: Update Lambda IAM Role

```bash
# Create policy for DynamoDB access
cat > dynamodb-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/geekbrain_sessions",
        "arn:aws:dynamodb:us-east-1:*:table/geekbrain_conversations"
      ]
    }
  ]
}
EOF

# Attach to Lambda role
aws iam put-role-policy \
  --role-name GeekBrainToolsLambdaRole \
  --policy-name DynamoDBAccess \
  --policy-document file://dynamodb-policy.json
```

---

### Step 3: Update Bedrock Agent Configuration

**Agent instructions (add memory context):**
```
You are GeekBrain AI Assistant with conversation memory.

MEMORY USAGE:
- You have access to conversation history
- When user says "it", "its", "that service", refer to entities mentioned earlier
- Maintain context across multiple turns
- If unclear, ask for clarification rather than guessing

EXAMPLE:
Turn 1: "Which service had highest cost in March?"
You: "PaymentGW at $7,500"

Turn 2: "What is its current latency?"
You: [Understand "its" = PaymentGW from Turn 1]
You: "PaymentGW's current p99 latency is approximately 185ms"
```

**❓ PRACTICE QUESTION 7:**
Agent instructions có đủ để handle memory không?
Hay cần implement memory logic trong code?
Hint: Bedrock Agent có built-in session management.

---

## Implementation

### File structure

```
L4_memory/
├── README.md (file này)
├── dynamodb_client.py         # DynamoDB operations
├── memory_manager.py          # Session & history management
├── agent_with_memory.py       # Agent + Memory integration
├── chatbot_l4.py              # Interactive chatbot
└── test_l4.py                 # Test với 6 conversation scripts
```

---

## Testing Strategy

### L4 Conversation Scripts

**Script structure:**
```json
{
  "id": "L4-01",
  "title": "Cost Investigation",
  "turns": [
    {
      "turn": 1,
      "user": "Which service had highest cost in March?",
      "expected_answer": "PaymentGW at $7,500",
      "requires": "tool (DB query)"
    },
    {
      "turn": 2,
      "user": "Why did its costs spike that month?",
      "expected_answer": "March 5 P1 outage...",
      "requires": "memory + retrieval"
    }
  ]
}
```

**❓ PRACTICE QUESTION 8:**
Turn 2 requires "memory + retrieval".
Breakdown steps:
1. Retrieve conversation history
2. Identify "its" refers to PaymentGW
3. Retrieve postmortem from KB
4. Synthesize answer

Nếu step nào fail, toàn bộ conversation fail.

---

## Success Criteria

- ✅ 5-6/6 conversation scripts pass
- ✅ Pronouns resolved correctly
- ✅ Context maintained across 4+ turns
- ✅ Session management works
- ✅ Average response time < 10 seconds

---

## Common Issues

### Issue 1: Pronoun Not Resolved

**Symptom:** Turn 2 asks "What service?" instead of using context

**Debug:**
```python
# Check conversation history
history = memory.get_history(session_id)
print(f"Last turn entities: {history[-1]['entities_mentioned']}")
```

**Fix:** Improve entity extraction in Turn 1

---

### Issue 2: Wrong Entity Referenced

**Symptom:** "its" resolved to wrong service

**Example:**
```
Turn 1: "PaymentGW had 3 incidents. AuthSvc had 1."
Turn 2: "What is its current latency?"
Bot: ❌ "AuthSvc latency is..." (should be PaymentGW)
```

**Fix:** Track entity salience (most recently mentioned = most salient)

---

### Issue 3: Context Window Overflow

**Symptom:** After 20+ turns, agent becomes slow or errors

**Fix:** Implement sliding window (keep last 10 turns only)

---

## Next Steps

Sau khi hoàn thành L4:
1. Move to **L5 - Goal-Directed Investigation**

**❓ PRACTICE QUESTION 9 (Preview L5):**
L4 có thể handle multi-turn conversations.
L4 KHÔNG thể handle open-ended investigations:

```
User: "Assess whether PaymentGW is reliable and recommend improvements"

L4 approach: ❌ Single query → single answer
L5 approach: ✓ Multi-step investigation:
  1. Check current status (tool)
  2. Query incident history (tool)
  3. Read postmortems (KB)
  4. Check SLA compliance (tool + KB)
  5. Synthesize findings
  6. Generate recommendations
```

Tại sao L4 không đủ? L5 cần gì thêm?
