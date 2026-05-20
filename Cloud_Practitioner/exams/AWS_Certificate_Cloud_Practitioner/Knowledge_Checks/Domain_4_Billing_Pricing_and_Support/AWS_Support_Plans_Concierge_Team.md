# AWS Support Plans - Concierge Support Team

**Date**: 2026-05-12

## Câu hỏi

**English**: A multi-national company wants to migrate its IT infrastructure to AWS Cloud and is looking for a concierge support team as well as a response time of around an hour in case the systems go down. As a Cloud Practitioner, which of the following support plans would you recommend to the company?

**Tiếng Việt**: Một multi-national company muốn migrate IT infrastructure lên AWS Cloud và đang tìm concierge support team cũng như response time khoảng 1 giờ khi systems go down. Bạn recommend support plan nào?

## Đáp án đúng ✅

**Enterprise**

**Tại sao?**
- ✅ **Concierge Support Team** - ONLY available trong Enterprise plan
- ✅ **Response time < 1 hour** cho production system outage
- ✅ **Response time < 15 minutes** cho business-critical systems
- ✅ Technical Account Manager (TAM)

**Keywords trong câu hỏi**:
- "**Concierge support team**" → ONLY Enterprise ✅
- "**Response time around an hour**" → Enterprise (< 1 hour for production)

## AWS Support Plans Overview

### ❌ **Basic** (FREE)

**Features**:
- 24x7 customer service
- Documentation, whitepapers, forums
- 7 core Trusted Advisor checks
- AWS Personal Health Dashboard
- ❌ **NO Concierge Support Team**
- ❌ **NO technical support**

**Response time**: N/A (no technical support)

### ❌ **Developer** ($29+/month)

**Features**:
- Email support (business hours only)
- General architectural guidance
- 7 core Trusted Advisor checks
- ❌ **NO Concierge Support Team**

**Response time**:
- General guidance: < 24 hours
- System impaired: < 12 hours

### ❌ **Business** ($100+/month)

**Features**:
- 24x7 phone, email, chat support
- Contextual architectural guidance
- Full Trusted Advisor checks
- Infrastructure Event Management (additional fee)
- ❌ **NO Concierge Support Team**

**Response time**:
- General guidance: < 24 hours
- System impaired: < 12 hours
- Production system impaired: < 4 hours
- Production system down: **< 1 hour** ✅

### ✅ **Enterprise** ($15,000+/month)

**Features**:
- 24x7 phone, email, chat support
- ✅ **Concierge Support Team** ← ONLY Enterprise
- ✅ **Technical Account Manager (TAM)**
- Contextual architectural guidance
- Full Trusted Advisor checks
- Infrastructure Event Management (included)
- Proactive/preventative programs

**Response time**:
- General guidance: < 24 hours
- System impaired: < 12 hours
- Production system impaired: < 4 hours
- Production system down: **< 1 hour** ✅
- Business-critical system down: **< 15 minutes** ✅

## Concierge Support Team

**Chức năng**: AWS **billing and account experts**

**Đặc điểm**:
- ✅ Specialize in **enterprise accounts**
- ✅ Assist with **billing and account inquiries**
- ✅ Quick và efficient support
- ✅ **ONLY available in Enterprise plan**

**Use case**:
- Complex billing questions
- Account management
- Enterprise-level support

## Response Time Comparison

| Support Plan | Production System Down | Business-Critical Down |
|--------------|------------------------|------------------------|
| **Basic** | N/A | N/A |
| **Developer** | N/A | N/A |
| **Business** | **< 1 hour** ✅ | N/A |
| **Enterprise** | **< 1 hour** ✅ | **< 15 minutes** ✅ |

## Các đáp án SAI ❌

### ❌ **Developer**

**Tại sao SAI?**
- ❌ **NO Concierge Support Team**
- ❌ Email support only (business hours)
- ❌ Response time: < 12 hours (system impaired)
- ❌ Không đáp ứng "response time around an hour"

### ❌ **Business**

**Tại sao SAI?**
- ❌ **NO Concierge Support Team** ← Key requirement
- ✅ Response time < 1 hour (production down) - Đáp ứng
- Nhưng **thiếu Concierge Support Team** → Không đủ

**Lưu ý**: Business có response time < 1 hour, nhưng **KHÔNG có Concierge Support Team**

### ❌ **Individual**

**Tại sao SAI?**
- **Made-up option** (không tồn tại)
- Distractor

## Key Point

**Concierge Support Team = ONLY Enterprise** ✅

**Câu hỏi có "Concierge Support Team"** → Đáp án: **Enterprise**

**Response time comparison**:
- Business: < 1 hour (production down) ✅ BUT NO Concierge
- Enterprise: < 1 hour (production down) ✅ AND Concierge ✅

## So sánh Business vs Enterprise

| Feature | Business | Enterprise |
|---------|----------|------------|
| **Concierge Support Team** | ❌ NO | ✅ **YES** |
| **TAM** | ❌ NO | ✅ YES |
| **Response (Production down)** | < 1 hour | < 1 hour |
| **Response (Business-critical)** | N/A | < 15 minutes |
| **IEM** | Additional fee | Included |
| **Price** | $100+/month | $15,000+/month |

## Exam Alert - Support Plans Comparison

### **Developer**
- Email support (business hours)
- General architectural guidance
- Response: < 12 hours (system impaired)

### **Business**
- 24x7 phone/email/chat
- Contextual architectural guidance
- Response: < 1 hour (production down)
- **NO Concierge, NO TAM**

### **Enterprise**
- 24x7 phone/email/chat
- **Concierge Support Team** ✅
- **Technical Account Manager (TAM)** ✅
- Response: < 15 minutes (business-critical)
- Response: < 1 hour (production down)

## Ví dụ thực tế

**Scenario**: Multi-national company requirements

**Requirements**:
1. ✅ Concierge support team
2. ✅ Response time ~1 hour (production down)

**Analysis**:
- Developer: ❌ No concierge, slow response
- Business: ❌ No concierge (có response < 1 hour nhưng thiếu concierge)
- **Enterprise**: ✅ Concierge + Response < 1 hour ✅

**Recommendation**: **Enterprise** ✅

## Lưu ý cho bài thi

**Keywords nhận biết Enterprise**:
- "**Concierge Support Team**" → ONLY Enterprise ✅
- "**Technical Account Manager (TAM)**" → ONLY Enterprise
- "**< 15 minutes response**" → ONLY Enterprise
- "**Business-critical systems**" → ONLY Enterprise

**Nếu câu hỏi có "Concierge"** → Đáp án chắc chắn: **Enterprise**

**KHÔNG nhầm lẫn**:
- Business có response < 1 hour nhưng **NO Concierge**
- Enterprise có **BOTH** Concierge và response < 1 hour
