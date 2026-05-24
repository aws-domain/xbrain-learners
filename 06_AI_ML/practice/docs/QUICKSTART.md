# W4 Practice Project - Quick Reference

> **One-page guide** để navigate toàn bộ practice project

---

## 🗺️ Navigation

| Level | Folder | README | Test | Status |
|-------|--------|--------|------|--------|
| **L1** | [L1_rag_basic/](./L1_rag_basic/) | [Guide](./L1_rag_basic/README.md) | `test_l1.py` | ⬜ Not started |
| **L2** | [L2_multi_source/](./L2_multi_source/) | [Guide](./L2_multi_source/README.md) | `test_l2.py` | ⬜ Not started |
| **L3** | [L3_tools/](./L3_tools/) | [Guide](./L3_tools/README.md) | `test_l3.py` | ⬜ Not started |
| **L4** | [L4_memory/](./L4_memory/) | [Guide](./L4_memory/README.md) | `test_l4.py` | ⬜ Not started |
| **L5** | [L5_investigation/](./L5_investigation/) | [Guide](./L5_investigation/README.md) | `test_l5.py` | ⬜ Not started |

**Update status khi hoàn thành:** ⬜ → 🟡 In Progress → ✅ Completed

---

## ⚡ Quick Commands

### L1 - RAG Basic
```bash
cd L1_rag_basic/
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
python test_l1.py
```

### L2 - Multi-Source
```bash
cd L2_multi_source/
cp ../L1_rag_basic/.env .
python test_l2.py
```

### L3 - Tools
```bash
# Start monitoring API first
cd ../data_package/scripts/
uv sync
uv run uvicorn monitoring_api:app --reload --port 8000 &

# Seed database
uv run python seed_data.py --db-type sqlite --sqlite-path geekbrain.db

# Test L3
cd ../../practice/L3_tools/
python test_l3.py
```

### L4 - Memory
```bash
cd L4_memory/
python test_l4.py
```

### L5 - Investigation
```bash
cd L5_investigation/
python test_l5.py
```

---

## 📋 Prerequisites Checklist

### Before Starting L1
- [ ] AWS account với Bedrock access
- [ ] AWS CLI configured (`aws configure`)
- [ ] Python 3.11+ installed
- [ ] Học xong Course 1-3 (Bedrock foundation)

### Before Starting L2
- [ ] L1 completed (10/10 pass)
- [ ] Học xong Course 4-6 (KB + Lab)

### Before Starting L3
- [ ] L1 + L2 completed
- [ ] Học xong Course 7-8 (Agents + Tools)
- [ ] Monitoring API running
- [ ] Database seeded

### Before Starting L4
- [ ] L1 + L2 + L3 completed
- [ ] Học xong Course 9 (DynamoDB)
- [ ] DynamoDB tables created

### Before Starting L5
- [ ] L1 + L2 + L3 + L4 completed
- [ ] All AWS services running

---

## 🎯 Success Metrics

| Level | Pass Rate Target | Avg Response Time | Key Metric |
|-------|------------------|-------------------|------------|
| L1 | 90-100% (9-10/10) | < 3s | Retrieval accuracy |
| L2 | 75-100% (6-8/8) | < 5s | Synthesis quality |
| L3 | 80-100% (8-10/10) | < 8s | Tool usage |
| L4 | 83-100% (5-6/6) | < 10s | Context retention |
| L5 | 80-100% (4-5/5) | < 30s | Investigation depth |

---

## 🔧 AWS Resources Needed

### L1 Resources
- ✅ S3 bucket: `geekbrain-kb-YOUR_NAME`
- ✅ Bedrock Knowledge Base: `geekbrain-kb`
- ✅ OpenSearch Serverless collection: `geekbrain-vectors`

### L3 Additional Resources
- ✅ Lambda function: `geekbrain-tools`
- ✅ IAM role: `GeekBrainToolsLambdaRole`
- ✅ Bedrock Agent: `geekbrain-agent`

### L4 Additional Resources
- ✅ DynamoDB table: `geekbrain_sessions`
- ✅ DynamoDB table: `geekbrain_conversations`

---

## 💰 Cost Estimate

### Development/Testing (1 week)
| Service | Usage | Cost |
|---------|-------|------|
| Bedrock KB | 36 docs, ~100 queries | ~$2 |
| Bedrock Model | ~500 invocations | ~$5 |
| Lambda | ~1000 invocations | ~$0.20 |
| DynamoDB | ~500 reads/writes | ~$0.50 |
| S3 | 36 docs storage | ~$0.01 |
| OpenSearch Serverless | 1 collection, 7 days | ~$20 |
| **Total** | | **~$28** |

### Production (1000 users/day)
- Bedrock: ~$150/month
- Lambda: ~$10/month
- DynamoDB: ~$25/month
- OpenSearch: ~$90/month
- **Total: ~$275/month**

---

## 🐛 Common Errors & Fixes

### Error: "KNOWLEDGE_BASE_ID not found"
```bash
# Fix: Set in .env
echo "KNOWLEDGE_BASE_ID=your_kb_id_here" >> .env
```

### Error: "Connection refused localhost:8000"
```bash
# Fix: Start monitoring API
cd ../data_package/scripts/
uv run uvicorn monitoring_api:app --reload --port 8000
```

### Error: "Table geekbrain_sessions does not exist"
```bash
# Fix: Create DynamoDB tables
aws dynamodb create-table \
  --table-name geekbrain_sessions \
  --attribute-definitions AttributeName=session_id,AttributeType=S \
  --key-schema AttributeName=session_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### Error: "Lambda timeout after 3 seconds"
```bash
# Fix: Increase timeout
aws lambda update-function-configuration \
  --function-name geekbrain-tools \
  --timeout 30
```

---

## 📊 Progress Tracking

### Week 4 Daily Goals

**Thứ Hai (May 6)**
- [ ] Course 1-3 completed
- [ ] L1 setup done
- [ ] L1 tests passing

**Thứ Ba (May 7)**
- [ ] Course 4-6 completed
- [ ] L2 tests passing
- [ ] Data package explored

**Thứ Tư (May 8)**
- [ ] Course 7-8 completed
- [ ] L3 setup done (Lambda, Agent)
- [ ] L3 tests passing

**Thứ Năm (May 9)**
- [ ] Course 9 completed
- [ ] L4 tests passing
- [ ] L5 tests passing

**Thứ Sáu (May 10)**
- [ ] All levels completed
- [ ] Full test suite passing
- [ ] Ready for demo

---

## 📚 Related Files

### Study Materials
- [W4_study_plan.md](../W4_study_plan.md) - Course schedule
- [W4_course_mapping.md](../W4_course_mapping.md) - Course details

### Data Package
- [data_package/README.md](../data_package/README.md) - Data overview
- [data_package/knowledge_base/](../data_package/knowledge_base/) - 36 documents
- [data_package/scripts/](../data_package/scripts/) - API & DB scripts

### Test Questions
- [questions/student/L1_questions.json](../questions/student/L1_questions.json)
- [questions/student/L2_questions.json](../questions/student/L2_questions.json)
- [questions/student/L3_questions.json](../questions/student/L3_questions.json)
- [questions/student/L4_conversation_scripts.json](../questions/student/L4_conversation_scripts.json)
- [questions/student/L5_investigation_prompts.json](../questions/student/L5_investigation_prompts.json)

---

## 🎓 Learning Resources

### AWS Documentation
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)

### Course Materials
- AWS Skill Builder - Amazon Bedrock courses
- Course completion certificates

---

## 💡 Pro Tips

1. **Save your .env file**
   ```bash
   # Backup after L1 setup
   cp L1_rag_basic/.env ~/geekbrain-env-backup
   ```

2. **Use debug mode when stuck**
   ```bash
   python test_l3.py --debug
   ```

3. **Check AWS Console regularly**
   - Bedrock → Knowledge bases
   - Lambda → Functions
   - DynamoDB → Tables
   - CloudWatch → Logs

4. **Test incrementally**
   - Don't write all code then test
   - Test after each function
   - Faster feedback loop

5. **Document your learnings**
   - What worked?
   - What didn't?
   - Interesting findings?

---

## 🚨 Emergency Contacts

### Stuck on Setup?
1. Check README.md in level folder
2. Check practice questions in code
3. Review course materials
4. Ask trainer during QnA

### AWS Issues?
1. Check CloudWatch logs
2. Verify IAM permissions
3. Check service quotas
4. Review AWS documentation

---

## ✅ Final Checklist

Before demo day:
- [ ] All 5 levels completed
- [ ] All tests passing
- [ ] AWS resources cleaned up (if needed)
- [ ] Code documented
- [ ] Learnings documented
- [ ] Demo script prepared
- [ ] Questions for trainer prepared

---

**Last Updated:** 2026-05-06

**Good luck with your practice! 🚀**
