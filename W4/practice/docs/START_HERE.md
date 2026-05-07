# 🚀 START HERE - W4 Practice Project

> **Welcome!** Đây là điểm bắt đầu cho W4 Practice Project của bạn.

---

## 📖 Đọc Files Theo Thứ Tự Này

### 1️⃣ **PROJECT_SUMMARY.md** (ĐỌC ĐẦU TIÊN)
```bash
cat PROJECT_SUMMARY.md
```
**Nội dung:** Overview toàn bộ project, statistics, what was created

**Thời gian đọc:** 5 phút

---

### 2️⃣ **README.md** (ĐỌC THỨ HAI)
```bash
cat README.md
```
**Nội dung:** 
- Learning path chi tiết
- Week 4 schedule
- Project structure
- Success criteria
- Tips for success

**Thời gian đọc:** 10 phút

---

### 3️⃣ **QUICKSTART.md** (REFERENCE)
```bash
cat QUICKSTART.md
```
**Nội dung:**
- Quick commands
- Prerequisites checklist
- Common errors & fixes
- Progress tracking

**Thời gian đọc:** 5 phút (keep open for reference)

---

### 4️⃣ **L1_rag_basic/README.md** (BẮT ĐẦU CODING)
```bash
cd L1_rag_basic/
cat README.md
```
**Nội dung:**
- L1 concepts
- AWS setup step-by-step
- Code implementation
- Testing

**Thời gian:** 4-6 hours (setup + coding + testing)

---

## ⚡ Quick Start (TL;DR)

Nếu bạn muốn bắt đầu ngay:

```bash
# 1. Đọc overview
cd W4/practice/
cat PROJECT_SUMMARY.md

# 2. Bắt đầu L1
cd L1_rag_basic/
cat README.md

# 3. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure AWS
cp .env.example .env
# Edit .env với your AWS credentials

# 5. Follow README.md để setup AWS resources
# (S3 bucket, Bedrock KB, etc.)

# 6. Test
python test_l1.py
```

---

## 📅 Timeline

### Hôm Nay (Thứ Ba, May 6)
- ✅ Project đã được tạo
- 📚 Bạn sẽ học Course 1-3 (2h)
- 🛠️ Bạn sẽ build L1 (4-6h)

### Ngày Mai (Thứ Tư, May 7)
- 📚 Học Course 4-6 (2-3h)
- 🛠️ Build L2 (3-4h)
- 📊 Explore data package

### Thứ Năm (May 8)
- 📚 Học Course 7-8 (2h)
- 🛠️ Build L3 (6-8h)

### Thứ Sáu (May 9)
- 📚 Học Course 9 (1h)
- 🛠️ Build L4 + L5 (7-9h)

### Thứ Bảy (May 10)
- 🎨 Polish & demo prep

---

## 🎯 Your Mission

Build một **AI chatbot** với 5 capabilities:

1. **L1:** Answer questions từ documents (RAG)
2. **L2:** Synthesize info từ nhiều documents
3. **L3:** Call tools để lấy live data
4. **L4:** Remember conversation history
5. **L5:** Conduct multi-step investigations

**End Goal:** Full-stack AI chatbot giống W4 project requirements

---

## 📚 Files Overview

```
practice/
├── START_HERE.md           ← BẠN ĐANG Ở ĐÂY
├── PROJECT_SUMMARY.md      ← Đọc đầu tiên
├── README.md               ← Đọc thứ hai
├── QUICKSTART.md           ← Reference
│
├── L1_rag_basic/           ← Bắt đầu coding ở đây
│   ├── README.md           ← Setup guide
│   ├── bedrock_client.py
│   ├── rag_pipeline.py
│   ├── chatbot.py
│   └── test_l1.py
│
├── L2_multi_source/        ← Sau khi L1 xong
├── L3_tools/               ← Sau khi L2 xong
├── L4_memory/              ← Sau khi L3 xong
└── L5_investigation/       ← Sau khi L4 xong
```

---

## ✅ Pre-Flight Checklist

Trước khi bắt đầu, check:

- [ ] Đã có AWS account với Bedrock access
- [ ] AWS CLI đã configured (`aws configure`)
- [ ] Python 3.11+ installed
- [ ] Đã đọc PROJECT_SUMMARY.md
- [ ] Đã đọc README.md
- [ ] Sẵn sàng học Course 1-3
- [ ] Có 4-6 hours để build L1 hôm nay

---

## 🎓 Learning Approach

### Recommended Flow

```
1. Đọc theory (README.md)
   ↓
2. Học courses (AWS Skill Builder)
   ↓
3. Setup AWS resources (follow guide)
   ↓
4. Code implementation (use templates)
   ↓
5. Test (automated tests)
   ↓
6. Debug if needed
   ↓
7. Move to next level
```

### Key Principles

- **Start simple:** L1 trước, đừng skip
- **Read practice questions:** Embedded trong code
- **Test incrementally:** Sau mỗi function
- **Debug systematically:** Check dependencies first
- **Document learnings:** Ghi lại insights

---

## 💡 Pro Tips

### 1. Keep QUICKSTART.md Open
```bash
# Open in another terminal
cat QUICKSTART.md
```
Có quick commands và troubleshooting.

### 2. Use Debug Mode
```bash
python test_l1.py --debug
```
Shows detailed execution steps.

### 3. Save Your .env
```bash
# After L1 setup
cp L1_rag_basic/.env ~/geekbrain-env-backup
```
Reuse cho L2, L3, L4, L5.

### 4. Check AWS Console
- Bedrock → Knowledge bases
- Lambda → Functions
- DynamoDB → Tables
- CloudWatch → Logs

### 5. Take Breaks
- L1: 4-6 hours → take breaks every 1-2h
- L3: 6-8 hours → longest level, pace yourself

---

## 🆘 If You Get Stuck

### Step 1: Check README
Mỗi level có detailed README với:
- Concepts explanation
- AWS setup steps
- Common issues table
- Debug commands

### Step 2: Read Practice Questions
Embedded trong code, có hints.

### Step 3: Review Courses
Go back to course materials.

### Step 4: Check AWS Docs
Use MCP AWS Docs nếu cần.

### Step 5: Ask Trainer
During QnA sessions.

---

## 🎯 Success Metrics

### Today's Goal (L1)
- [ ] Học xong Course 1-3
- [ ] Setup AWS resources (S3, Bedrock KB)
- [ ] Code implementation done
- [ ] 9-10/10 test questions pass
- [ ] Understand RAG concepts

### This Week's Goal (L1-L5)
- [ ] All 5 levels completed
- [ ] All tests passing (>80% pass rate)
- [ ] Understand all concepts
- [ ] Ready for W4 demo

---

## 🚀 Ready to Start?

### Next Steps:

1. **Đọc PROJECT_SUMMARY.md** (5 min)
   ```bash
   cat PROJECT_SUMMARY.md
   ```

2. **Đọc README.md** (10 min)
   ```bash
   cat README.md
   ```

3. **Bắt đầu L1** (4-6 hours)
   ```bash
   cd L1_rag_basic/
   cat README.md
   ```

---

## 📞 Quick Links

- **Main guide:** [README.md](./README.md)
- **Quick reference:** [QUICKSTART.md](./QUICKSTART.md)
- **Project summary:** [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
- **Study plan:** [../W4_study_plan.md](../W4_study_plan.md)
- **Data package:** [../data_package/README.md](../data_package/README.md)

---

## 🎉 Let's Go!

Bạn đã có:
- ✅ Complete project structure
- ✅ Code templates cho 5 levels
- ✅ 50+ practice questions
- ✅ Detailed guides
- ✅ Test scripts
- ✅ AWS setup instructions

**Everything you need to succeed!**

Bây giờ:
1. Đọc PROJECT_SUMMARY.md
2. Đọc README.md
3. Bắt đầu L1

**Good luck! Bạn sẽ làm được! 💪🚀**

---

**Created:** 2026-05-06
**Status:** ✅ Ready
**Your journey starts here!** 👇

```bash
cat PROJECT_SUMMARY.md
```
