# AWS DDoS Protection Services

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following AWS services can be used to prevent Distributed Denial-of-Service (DDoS) attack? (Select three)

**Tiếng Việt**: AWS services nào có thể được dùng để prevent Distributed Denial-of-Service (DDoS) attack? (Chọn 3)

## Đáp án đúng ✅ (Chọn 3)

### 1. **AWS Shield**

**Chức năng**: Managed **DDoS protection service**

**Đặc điểm**:
- ✅ **Always-on detection** - Tự động phát hiện DDoS
- ✅ **Automatic inline mitigations** - Tự động chặn attacks
- ✅ Minimize downtime và latency
- ✅ **No need to engage AWS Support** - Tự động protection

**2 tiers**:
- **Shield Standard**: FREE, automatic protection cho tất cả AWS customers
- **Shield Advanced**: Paid, enhanced protection + DRT support

**Use case**: Primary DDoS protection cho AWS resources ✅

### 2. **AWS WAF (Web Application Firewall)**

**Chức năng**: **Web access control** và filtering

**Đặc điểm**:
- ✅ **Web ACLs** - Filter và block requests
- ✅ **Rate-based rules** - Auto block IPs khi exceed threshold
- ✅ Block requests based on **request signatures**
- ✅ Protect against **application layer (Layer 7) attacks**

**DDoS Protection**:
- Rate limiting → Prevent volumetric attacks
- IP blocking → Block malicious actors
- Request filtering → Block attack patterns

**Use case**: Application layer DDoS protection ✅

### 3. **Amazon CloudFront with Route 53**

**Chức năng**: **Global edge network** for content delivery và DNS

**Đặc điểm**:
- ✅ **Distributed network** of edge locations worldwide
- ✅ **CloudFront**: CDN absorbs traffic at edge
- ✅ **Route 53**: DNS service với DDoS protection
- ✅ **Global Amazon network** - Distributed defense

**DDoS Protection**:
- Edge locations absorb attack traffic
- Distributed architecture → Hard to overwhelm
- Geographic distribution → Spread attack impact

**Use case**: Infrastructure layer DDoS protection ✅

## Các đáp án SAI ❌

### ❌ **AWS CloudHSM**

**Chức năng**: **Hardware Security Module** for encryption

**Đặc điểm**:
- Generate và manage encryption keys
- FIPS 140-2 Level 3 validated
- Hardware-based encryption

**Tại sao SAI?**
- CloudHSM dùng cho **encryption**, không phải DDoS protection
- **KHÔNG có** DDoS mitigation capabilities

**Use case**: Encryption compliance, NOT DDoS protection

### ❌ **AWS Trusted Advisor**

**Chức năng**: **Best practices recommendations** tool

**Đặc điểm**:
- Cost optimization
- Security recommendations
- Performance improvement
- Service limits monitoring

**Tại sao SAI?**
- Trusted Advisor là **advisory tool**, không phải protection service
- **KHÔNG prevent** DDoS attacks
- Chỉ provide recommendations

**Use case**: Best practices guidance, NOT DDoS protection

### ❌ **Amazon Inspector**

**Chức năng**: **Security assessment service**

**Đặc điểm**:
- Automated security assessments
- Find vulnerabilities
- Check compliance
- Application security scanning

**Tại sao SAI?**
- Inspector dùng để **assess security**, không phải prevent attacks
- **KHÔNG có** DDoS protection capabilities
- Chỉ identify vulnerabilities

**Use case**: Security assessment, NOT DDoS protection

## AWS DDoS Protection Strategy

### **Multi-Layer Defense**

```
Layer 7 (Application) → AWS WAF ✅
        ↓
Layer 4 (Transport) → AWS Shield ✅
        ↓
Layer 3 (Network) → AWS Shield ✅
        ↓
Infrastructure → CloudFront + Route 53 ✅
```

### **Complete DDoS Protection Stack**

1. **AWS Shield** (Standard/Advanced)
   - Network layer (L3) protection
   - Transport layer (L4) protection
   - Always-on detection

2. **AWS WAF**
   - Application layer (L7) protection
   - Rate limiting
   - Request filtering

3. **CloudFront + Route 53**
   - Edge network distribution
   - Traffic absorption
   - Geographic distribution

## So sánh DDoS Protection Services

| Service | Layer | Protection Type | Cost |
|---------|-------|----------------|------|
| **Shield Standard** | L3, L4 | Network/Transport | FREE ✅ |
| **Shield Advanced** | L3, L4, L7 | Enhanced + DRT | Paid |
| **WAF** | L7 | Application | Pay per rule |
| **CloudFront + Route 53** | Infrastructure | Edge distribution | Pay per usage |

## DDoS Attack Types và Protection

### **Volumetric Attacks** (Network Layer)
- **Attack**: Flood với massive traffic
- **Protection**: Shield + CloudFront (absorb at edge) ✅

### **Protocol Attacks** (Transport Layer)
- **Attack**: SYN flood, UDP flood
- **Protection**: Shield (automatic mitigation) ✅

### **Application Layer Attacks** (Layer 7)
- **Attack**: HTTP flood, Slowloris
- **Protection**: WAF (rate limiting, filtering) ✅

## Key Point

**3 AWS services cho DDoS protection**:
1. **AWS Shield** - Managed DDoS protection ✅
2. **AWS WAF** - Web application firewall ✅
3. **CloudFront + Route 53** - Edge network distribution ✅

**KHÔNG phải DDoS protection**:
- CloudHSM = Encryption
- Trusted Advisor = Advisory tool
- Inspector = Security assessment

## Ví dụ thực tế

**Scenario**: E-commerce website cần DDoS protection

### ✅ **Complete Protection Stack**

```
Users → Route 53 (DNS with DDoS protection)
     ↓
CloudFront (Edge locations absorb traffic)
     ↓
AWS WAF (Filter malicious requests, rate limiting)
     ↓
ALB (Application Load Balancer)
     ↓
EC2 instances (Protected by Shield Standard)
```

**Protection layers**:
1. **Route 53**: DNS DDoS protection
2. **CloudFront**: Absorb volumetric attacks at edge
3. **WAF**: Block application layer attacks
4. **Shield Standard**: Automatic L3/L4 protection

**Result**: Multi-layer defense against DDoS ✅

## Lưu ý cho bài thi

**Keywords nhận biết DDoS protection**:
- "**Prevent DDoS**" → Shield, WAF, CloudFront + Route 53
- "**Always-on detection**" → Shield
- "**Rate-based rules**" → WAF
- "**Edge locations**" → CloudFront + Route 53

**KHÔNG nhầm lẫn**:
- CloudHSM = Encryption (NOT DDoS)
- Trusted Advisor = Advisory (NOT DDoS)
- Inspector = Assessment (NOT DDoS)

## Tóm tắt

**3 services cho DDoS protection**:
1. **Shield**: Managed DDoS protection (L3, L4)
2. **WAF**: Application firewall (L7)
3. **CloudFront + Route 53**: Edge network distribution

**Best practice**: Combine tất cả 3 services cho comprehensive DDoS protection
