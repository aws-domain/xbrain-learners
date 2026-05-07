# W4 Practice Project - GeekBrain AI Chatbot

> **Build an AI That Actually Answers (RAG + Tools + Memory)**
> 
> Practice project tương tự 100% với W4 project requirements, nhưng được chia nhỏ theo từng level để học dần.

---

## 📋 Overview

Project này giúp bạn build một AI chatbot hoàn chỉnh với 5 levels tăng dần về độ phức tạp:

| Level | Name | Capabilities | Time Estimate |
|-------|------|--------------|---------------|
| **L1** | RAG Basic | Single-document retrieval | 4-6 hours |
| **L2** | Multi-Source | Synthesize across documents | 3-4 hours |
| **L3** | Tools | Live data from API/DB | 6-8 hours |
| **L4** | Memory | Multi-turn conversations | 4-5 hours |
| **L5** | Investigation | Goal-directed reasoning | 3-4 hours |
| **Total** | | Full-stack AI chatbot | **20-27 hours** |

---

## 🎯 Learning Path

### Week 4 Schedule

#### **Thứ Hai** (4-6 hours)
- ✅ Học Course 1-3 (Bedrock foundation) - 2h
- 🛠️ Build L1 - RAG Basic - 2-4h
- 📝 Test với 10 câu hỏi L1

**Checkpoint:** Chatbot có thể trả lời câu hỏi đơn giản từ 1 document

---

#### **Thứ Ba** (6-8 hours)
- ✅ Học Course 4-6 (KB + Lab) - 2-3h
- 🛠️ Build L2 - Multi-Source - 2-3h
- 📝 Test với 8 câu hỏi L2
- 📊 Explore data package (36 docs, API, DB) - 1-2h

**Checkpoint:** Chatbot có thể synthesize thông tin từ nhiều documents

---

#### **Thứ Tư** (8-10 hours)
- ✅ Học Course 7-8 (Agents + Tools) - 2h
- 🛠️ Build L3 - Tools Integration - 6-8h
  - Setup monitoring API
  - Seed database
  - Create Lambda functions
  - Configure Bedrock Agent
- 📝 Test với 10 câu hỏi L3

**Checkpoint:** Chatbot có thể gọi tools để lấy live data

---

#### **Thứ Năm** (6-8 hours)
- ✅ Học Course 9 (DynamoDB) - 1h
- 🛠️ Build L4 - Conversation Memory - 4-5h
  - Create DynamoDB tables
  - Implement session management
  - Add entity tracking
- 📝 Test với 6 conversation scripts
- 🛠️ Build L5 - Investigation - 2-3h
- 📝 Test với 5 investigation prompts

**Checkpoint:** Chatbot có thể handle multi-turn conversations và investigations

---

#### **Thứ Sáu** (2-4 hours)
- 🎨 Polish & optimize
- 📊 Run full test suite (L1-L5)
- 📝 Document learnings
- 🚀 (Optional) Deploy to production

---

## 📁 Project Structure

```
W4/practice/
├── L1_rag_basic/
│   ├── README.md                    # Setup guide + practice questions
│   ├── .env.example
│   ├── requirements.txt
│   ├── bedrock_client.py            # Bedrock API wrapper
│   ├── rag_pipeline.py              # RAG logic
│   ├── chatbot.py                   # Interactive CLI
│   └── test_l1.py                   # Automated tests
│
├── L2_multi_source/
│   ├── README.md
│   ├── rag_pipeline_l2.py           # Enhanced RAG with synthesis
│   └── test_l2.py
│
├── L3_tools/
│   ├── README.md
│   ├── lambda/
│   │   ├── tools_handler.py         # Lambda for tools
│   │   └── requirements.txt
│   ├── bedrock_agent_client.py      # Agent API wrapper
│   └── test_l3.py
│
├── L4_memory/
│   ├── README.md
│   ├── dynamodb_client.py           # Session & history storage
│   └── test_l4.py
│
└── L5_investigation/
    ├── README.md
    └── test_l5.py
```

---

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** với Bedrock access
2. **Python 3.11+**
3. **AWS CLI** configured
4. **Data package** (đã có trong W4/data_package/)

### Step 1: Start with L1

```bash
cd W4/practice/L1_rag_basic/

# Đọc README.md để hiểu concepts
cat README.md

# Setup AWS resources (S3, Bedrock KB)
# Follow instructions in README.md

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env với your AWS credentials

# Test
python test_l1.py
```

### Step 2: Progress through levels

Sau khi L1 pass, move to L2, L3, L4, L5 theo thứ tự.

---

## 📚 Practice Questions

Mỗi level có **practice questions** embedded trong code và README:

- **❓ PRACTICE QUESTION**: Câu hỏi để suy nghĩ trong lúc code
- Giúp hiểu sâu concepts, không chỉ copy-paste code
- Không có "đúng/sai" tuyệt đối - encourage critical thinking

**Example từ L1:**
```python
❓ PRACTICE QUESTION 1:
Sau khi upload xong, chạy lệnh `aws s3 ls s3://geekbrain-kb-YOUR_NAME/docs/ --recursive | wc -l`. 
Kết quả phải là bao nhiêu files? Tại sao?
```

**Mục đích:**
- Verify understanding
- Encourage exploration
- Build debugging skills

---

## ✅ Success Criteria

### L1 - RAG Basic
- [ ] 10/10 câu hỏi L1 pass
- [ ] Average response time < 3s
- [ ] Retrieved chunks có score > 0.5

### L2 - Multi-Source
- [ ] 6-8/8 câu hỏi L2 pass
- [ ] Conflict resolution works (v1 vs v2)
- [ ] Multi-doc synthesis works

### L3 - Tools
- [ ] 8-10/10 câu hỏi L3 pass
- [ ] Tools được gọi đúng lúc
- [ ] Tool results synthesized với KB

### L4 - Memory
- [ ] 5-6/6 conversation scripts pass
- [ ] Pronouns resolved correctly
- [ ] Context maintained across 4+ turns

### L5 - Investigation
- [ ] 4-5/5 investigations pass
- [ ] Multi-step reasoning demonstrated
- [ ] Comprehensive findings + recommendations

---

## 🐛 Debugging Guide

### Common Issues by Level

#### L1 Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| Empty chunks | KB chưa sync xong | Đợi sync hoàn tất |
| Wrong answer | Retrieved wrong doc | Improve query phrasing |
| Rate limit error | Quá nhiều requests | Add retry logic |

#### L2 Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| Missing documents | Too few chunks | Increase max_chunks to 10-12 |
| Conflict not resolved | Weak prompt | Add explicit conflict resolution rules |
| No synthesis | LLM không combine | Improve prompt instructions |

#### L3 Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| Tool not called | Agent instructions unclear | Improve agent instructions |
| Lambda timeout | Function too slow | Increase timeout to 30s |
| Tool returns error | API/DB not accessible | Check monitoring API running |

#### L4 Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| Pronoun not resolved | Entity tracking fail | Improve entity extraction |
| Context lost | History not loaded | Check DynamoDB queries |
| Wrong entity referenced | Salience tracking issue | Track most recent entity |

#### L5 Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| Incomplete investigation | Agent stops early | Improve agent instructions |
| Missing data sources | Not using tools/KB | Explicit instruction to use both |
| Shallow recommendations | Generic output | Prompt for specific actions |

---

## 📊 Testing Strategy

### Automated Tests

```bash
# Run all tests
cd W4/practice/

python L1_rag_basic/test_l1.py
python L2_multi_source/test_l2.py
python L3_tools/test_l3.py
python L4_memory/test_l4.py
python L5_investigation/test_l5.py
```

### Manual Testing

```bash
# Interactive chatbot
python L1_rag_basic/chatbot.py

# With debug mode
python L3_tools/test_l3.py --debug
```

### Test Results

Results saved to JSON files:
- `l1_test_results.json`
- `l2_test_results.json`
- `l3_test_results.json`
- `l4_test_results.json`
- `l5_test_results.json`

Analyze để identify patterns và improve.

---

## 💡 Tips for Success

### 1. Start Simple
- Don't skip L1 to jump to L3
- Each level builds on previous
- Master fundamentals first

### 2. Read Practice Questions
- Embedded trong code và README
- Encourage critical thinking
- No "right" answers - explore!

### 3. Debug Systematically
- Check dependencies first (API running? DB seeded?)
- Use debug mode (`--debug` flag)
- Read AWS CloudWatch logs

### 4. Test Incrementally
- Test after each change
- Don't write all code then test
- Faster feedback loop

### 5. Document Learnings
- What worked? What didn't?
- Interesting findings?
- Questions for trainer?

---

## 🎓 Learning Outcomes

Sau khi hoàn thành project này, bạn sẽ:

### Technical Skills
- ✅ Build RAG systems với Bedrock
- ✅ Implement function calling với Agents
- ✅ Design conversation memory với DynamoDB
- ✅ Orchestrate multi-step AI workflows
- ✅ Deploy serverless AI applications

### AWS Services Mastery
- ✅ Amazon Bedrock (KB, Agents, Models)
- ✅ AWS Lambda (tools execution)
- ✅ Amazon S3 (document storage)
- ✅ Amazon DynamoDB (session management)
- ✅ IAM (permissions management)

### AI/ML Concepts
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Vector embeddings & similarity search
- ✅ LLM prompt engineering
- ✅ Function calling & tool use
- ✅ Multi-agent systems

---

## 🚀 Next Steps

### After Completing L1-L5

1. **Compare với W4 Project Requirements**
   - Có đáp ứng đủ không?
   - Missing features gì?

2. **Optimize Performance**
   - Reduce response time
   - Improve accuracy
   - Lower costs

3. **Add Production Features**
   - Authentication
   - Rate limiting
   - Monitoring
   - Error handling

4. **Deploy**
   - API Gateway + Lambda
   - CloudFront CDN
   - Route 53 DNS

5. **Extend Capabilities**
   - Streaming responses
   - Multi-language support
   - Voice interface
   - Slack integration

---

## 📞 Support

### Stuck? Check:

1. **README.md** trong mỗi level folder
2. **Practice questions** trong code
3. **Debugging guide** (section trên)
4. **AWS Documentation** (use MCP AWS Docs nếu cần)

### Still stuck?

- Review course materials
- Check CloudWatch logs
- Test components individually
- Ask trainer during QnA sessions

---

## 🎉 Congratulations!

Khi bạn hoàn thành tất cả 5 levels, bạn đã build được một **production-ready AI chatbot** với:

- 📚 Knowledge base (36 documents)
- 🔧 Tools integration (API + Database)
- 💬 Conversation memory
- 🔍 Goal-directed investigation
- ⚡ Real-time responses

**Đây chính là project W4 requirements!** 🚀

---

## 📝 Final Checklist

- [ ] L1 completed (10/10 pass)
- [ ] L2 completed (6+/8 pass)
- [ ] L3 completed (8+/10 pass)
- [ ] L4 completed (5+/6 pass)
- [ ] L5 completed (4+/5 pass)
- [ ] All AWS resources created
- [ ] All tests passing
- [ ] Code documented
- [ ] Learnings documented
- [ ] Ready for W4 demo! 🎤

Good luck! 💪
