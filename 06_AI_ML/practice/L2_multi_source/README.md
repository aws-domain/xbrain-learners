# L2 - Multi-Source Reasoning: Synthesize Across Documents

> **Prerequisites:** 
> - ✅ Hoàn thành L1
> - ✅ Học thêm Course 4-6 (MultiModal KB, S3 Vectors, SimuLearn Lab)

## Mục tiêu

Nâng cấp chatbot để:
- Synthesize thông tin từ nhiều documents
- Resolve conflicts giữa các versions (v1 vs v2)
- Cross-reference dependencies giữa services
- Trả lời 8 câu hỏi L2 từ `questions/student/L2_questions.json`

## Sự khác biệt giữa L1 và L2

| Aspect | L1 | L2 |
|--------|----|----|
| **Retrieval** | 1 document | 2-4 documents |
| **Reasoning** | Direct lookup | Synthesis + conflict resolution |
| **Prompt** | Simple context | Structured multi-doc context |
| **Example** | "What is X?" | "If X happens, what should Y do?" |

---

## Key Concepts

### 1. Multi-Document Retrieval

**L1 approach:**
```
Query: "What is PaymentGW's rate limit?"
→ Retrieve from api_reference_v2.md
→ Answer: "1000 rpm"
```

**L2 approach:**
```
Query: "What is PaymentGW's rate limit?"
→ Retrieve from:
  - api_reference_v2.md (1000 rpm, effective March 2025)
  - api_reference_v1_archived.md (500 rpm, archived)
→ Resolve conflict: v2 supersedes v1
→ Answer: "1000 rpm per v2. v1 had 500 rpm but is archived."
```

**❓ PRACTICE QUESTION 1:** 
Trong course "Build with S3 Vectors and Bedrock KB", bạn học về metadata filtering.
Làm thế nào để filter chỉ lấy documents không có tag "archived"?

---

### 2. Cross-Document Reasoning

**Example: L2-02**
```
Question: "If Team Commerce discovers a P1 bug at 21:00 Friday, can they deploy?"

Required documents:
1. deployment_policy.md → Freeze: Fri 18:00 - Mon 08:00
2. incident_response_policy.md → P1 overrides freeze
3. team_structure.md → VP Mark Sullivan approves

Answer: "Yes, with VP approval despite freeze"
```

**❓ PRACTICE QUESTION 2:**
Câu hỏi này cần 3 documents. Nếu chỉ retrieve 2 documents, answer sẽ thiếu gì?

---

### 3. Dependency Mapping

**Example: L2-03**
```
Question: "Which services depend on AuthSvc?"

Required documents:
1. service_architecture.md → Dependency graph
2. service_authsvc.md → AuthSvc description

Answer: "PaymentGW and OrderSvc depend on AuthSvc for token validation"
```

---

## Changes from L1

### 1. Increase max_chunks

```python
# L1
result = rag.answer(query, max_chunks=5)

# L2
result = rag.answer(query, max_chunks=10)  # More chunks for multi-doc
```

**❓ PRACTICE QUESTION 3:**
Tăng max_chunks từ 5 → 10 → 15.
- Response time thay đổi như thế nào?
- Answer quality improve không?
- Trade-off là gì?

---

### 2. Improve Prompt for Synthesis

**L1 prompt:**
```
Answer based on context. Be concise.
```

**L2 prompt:**
```
You must synthesize information across multiple documents.

When documents conflict:
1. Prefer newer versions over archived
2. State both versions and explain the conflict
3. Cite which document you're using

When cross-referencing:
1. Combine information from all relevant documents
2. Show the reasoning chain
3. Identify if information is missing
```

**❓ PRACTICE QUESTION 4:**
Thử viết prompt instruction để LLM:
- Luôn list ra tất cả documents được sử dụng
- Explain reasoning step-by-step
- Highlight conflicts nếu có

---

### 3. Add Metadata Filtering (Optional)

```python
# Filter out archived documents
retrievalConfiguration={
    'vectorSearchConfiguration': {
        'numberOfResults': 10,
        'filter': {
            'equals': {
                'key': 'status',
                'value': 'active'
            }
        }
    }
}
```

**❓ PRACTICE QUESTION 5:**
Để implement metadata filtering, bạn cần:
1. Add metadata vào documents khi upload S3
2. Configure KB để index metadata
3. Use filter trong retrieve call

Metadata nào hữu ích cho GeekBrain KB?
- version (v1, v2)
- status (active, archived)
- team (platform, commerce, data)
- type (policy, service, postmortem)

---

## Implementation Steps

### Step 1: Copy L1 code to L2

```bash
cd /Users/enma/Downloads/Coding/Cloud_Engineer/xbrain-learners-c/W4/practice/L2_multi_source/

# Copy base files from L1
cp ../L1_rag_basic/bedrock_client.py .
cp ../L1_rag_basic/requirements.txt .
cp ../L1_rag_basic/.env.example .
```

---

### Step 2: Enhance rag_pipeline.py

Key changes:
1. Increase default max_chunks to 10
2. Improve prompt for multi-doc synthesis
3. Add document grouping by source
4. Add conflict detection logic

---

### Step 3: Update test script

```bash
# Test with L2 questions
python test_l2.py
```

Expected: 6-8/8 questions pass (some L2 questions are hard!)

---

## Testing Strategy

### Test Categories

**Easy L2 (should pass):**
- L2-01: Version conflict (v1 vs v2)
- L2-03: Dependency mapping

**Medium L2:**
- L2-02: Policy synthesis (3 docs)
- L2-04: Cost optimization (2 docs)

**Hard L2:**
- L2-06: Onboarding synthesis (4 docs)
- L2-08: Escalation path (2 docs + reasoning)

**❓ PRACTICE QUESTION 6:**
Chạy test_l2.py và identify câu nào fail.
Với mỗi failed question:
1. Check retrieved chunks → đủ documents chưa?
2. Check prompt → có instruct synthesis không?
3. Check answer → thiếu phần nào?

---

## Debugging Multi-Source Issues

### Issue 1: Missing Documents

**Symptom:** Answer thiếu information từ 1 document

**Debug:**
```python
# In rag_pipeline.py, add:
print(f"Retrieved documents: {set([c['source'] for c in chunks])}")
```

**Fix:** Increase max_chunks hoặc improve query phrasing

---

### Issue 2: Conflict Not Resolved

**Symptom:** Answer mention cả v1 và v2 nhưng không nói cái nào đúng

**Debug:** Check prompt có instruct conflict resolution không?

**Fix:** Add explicit instruction:
```
When you see multiple versions (v1, v2), always prefer the latest non-archived version.
```

---

### Issue 3: No Synthesis

**Symptom:** Answer chỉ repeat information từ 1 doc, không combine

**Debug:** Check chunks có đủ từ tất cả required docs không?

**Fix:** 
1. Improve prompt: "You MUST combine information from ALL provided documents"
2. Add document labels: [Doc 1: policy.md], [Doc 2: team.md]

---

## Success Criteria

- ✅ 6-8/8 câu hỏi L2 pass
- ✅ Conflict resolution works (L2-01)
- ✅ Multi-doc synthesis works (L2-02, L2-06)
- ✅ Cross-reference works (L2-03, L2-08)
- ✅ Average response time < 5 seconds

---

## Common Pitfalls

1. **Too few chunks:** L2 needs 8-10 chunks minimum
2. **Weak prompt:** Must explicitly instruct synthesis
3. **No conflict handling:** LLM gets confused by contradictions
4. **Missing metadata:** Can't filter archived docs

**❓ PRACTICE QUESTION 7:**
So sánh L1 vs L2 implementation:
- Code complexity tăng bao nhiêu %?
- Response time tăng bao nhiêu?
- Accuracy improve bao nhiêu?
- Trade-off có đáng không?

---

## Next Steps

Sau khi hoàn thành L2:
1. Học **Course 7-8** (Agents + Tools)
2. Move to **L3 - Grounded Computation**

**❓ PRACTICE QUESTION 8 (Preview L3):**
L2 có thể trả lời: "What is PaymentGW's SLA target?" (từ docs)
L2 KHÔNG thể trả lời: "What is PaymentGW's current latency?" (cần live API)

Tại sao? Làm thế nào L3 sẽ giải quyết?
