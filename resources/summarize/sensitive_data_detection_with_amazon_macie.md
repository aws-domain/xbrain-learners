# Sensitive Data Detection with Amazon Macie - Core Knowledge Summary

## Tổng quan Amazon Macie

Amazon Macie là dịch vụ **data security** sử dụng machine learning và pattern matching để:
- **Phát hiện** sensitive data trong Amazon S3
- **Giám sát** security posture của S3 buckets
- **Tự động hóa** discovery, logging, và reporting
- **Bảo vệ** dữ liệu khỏi các rủi ro bảo mật

```
┌──────────────────────────────────────────────────────┐
│                   Amazon Macie                        │
├──────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │ S3 Bucket       │    │ Detection Engine        │  │
│  │ Inventory &     │    │ • Managed Identifiers   │  │
│  │ Monitoring      │    │ • Custom Identifiers    │  │
│  └────────┬────────┘    │ • ML + Pattern Match    │  │
│           │             └───────────┬─────────────┘  │
│           ↓                         ↓                │
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │ Policy Findings │    │ Sensitive Data Findings │  │
│  └────────┬────────┘    └───────────┬─────────────┘  │
│           └──────────┬──────────────┘                │
│                      ↓                               │
│  ┌───────────────────────────────────────────────┐   │
│  │ EventBridge │ Security Hub │ S3 (results)     │   │
│  └───────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## 1. Phương thức phát hiện Sensitive Data

### 1.1 Automated Sensitive Data Discovery

**Đặc điểm:**
- Chạy liên tục, đánh giá S3 bucket inventory **hàng ngày**
- Dùng **sampling techniques** để chọn representative objects
- Cung cấp **broad visibility** (tổng quan rộng) về nơi sensitive data có thể tồn tại
- Tạo **heat map** trực quan trên console
- Tính **sensitivity score** cho mỗi bucket

**Cách hoạt động:**
1. Macie đánh giá S3 bucket inventory
2. Dùng sampling để chọn representative S3 objects
3. Retrieve và analyze objects đã chọn
4. Tạo findings + cập nhật statistics/scores

**Cấu hình:**
- Mặc định: quét tất cả S3 general purpose buckets
- Có thể exclude specific buckets
- Admin có thể enable/disable cho từng member account
- Có thể chọn managed/custom data identifiers cụ thể

### 1.2 Sensitive Data Discovery Jobs

**Đặc điểm:**
- Phân tích **sâu hơn và targeted** hơn automated discovery
- Bạn kiểm soát hoàn toàn scope (buckets, objects, schedule)
- Chạy **on-demand** (1 lần) hoặc **recurring** (daily/weekly/monthly)

**Các bước tạo Job:**
1. **Choose S3 buckets** — Select cụ thể hoặc define criteria
2. **Define schedule & scope** — One-time hoặc recurring, refine bằng object properties
3. **Select managed data identifiers** — Chọn built-in identifiers
4. **Select custom data identifiers** — Thêm regex patterns tùy chỉnh
5. **Select allow lists** — Exclude text/patterns không cần report
6. **Enter general settings** — Name, description, tags
7. **Review and create**

**Scope refinement options:**
- Object tags
- Key name prefixes
- Last modified date
- File size
- Storage class

### So sánh 2 phương thức

| | Automated Discovery | Discovery Jobs |
|---|---|---|
| **Scope** | Broad (toàn bộ data estate) | Targeted (buckets cụ thể) |
| **Depth** | Sampling | Full hoặc sampling depth tùy chọn |
| **Schedule** | Liên tục (daily) | On-demand hoặc recurring |
| **Use case** | Monitoring tổng quan, detect trends | Deep investigation, compliance audit |
| **Control** | Ít cấu hình | Nhiều options tùy chỉnh |

---

## 2. Data Identifiers

### 2.1 Managed Data Identifiers (Built-in)

Macie cung cấp sẵn các identifiers dùng **ML + pattern matching** để detect:

#### Credentials
| Data Type | Ví dụ |
|-----------|-------|
| AWS Secret Access Key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| Google Cloud API Key | API keys |
| HTTP Basic Auth Header | Base64 encoded credentials |
| JSON Web Token (JWT) | Token strings |
| OpenSSH Private Key | `-----BEGIN OPENSSH PRIVATE KEY-----` |
| PGP Private Key | PGP key blocks |
| PKCS Private Key | PKCS formatted keys |
| PuTTY Private Key | PuTTY key files |
| Stripe API Key | `sk_live_...` |

#### Financial Information
| Data Type | Ví dụ |
|-----------|-------|
| Credit Card Number | Visa, Mastercard, Amex, etc. |
| Bank Account Number | IBAN, routing numbers |
| Credit Card Expiration | MM/YY |
| Credit Card Verification Code | CVV/CVC |

#### Personal Health Information (PHI)
| Data Type | Ví dụ |
|-----------|-------|
| DEA Registration Number | Drug Enforcement Agency |
| Health Insurance Claim Number | HICN |
| National Drug Code (NDC) | Drug identifiers |
| National Provider Identifier (NPI) | Healthcare provider IDs |
| Unique Device Identifier (UDI) | Medical device IDs |

#### Personally Identifiable Information (PII)
| Data Type | Ví dụ |
|-----------|-------|
| Birth Date | Dates of birth |
| Driver's License | License numbers (multi-country) |
| Full Name | Personal names |
| Mailing Address | Physical addresses |
| National ID Number | SSN, SIN, NINO, etc. |
| Passport Number | Passport numbers (multi-country) |
| Phone Number | Phone numbers (multi-country) |
| Social Security Number (SSN) | US SSN format |
| Taxpayer ID | Tax identification numbers |
| GPS Coordinates | Latitude/longitude pairs |
| Vehicle Identification Number | VIN |

**Keyword requirements:** Nhiều managed identifiers yêu cầu keyword gần kề để tăng accuracy (ví dụ: "SSN", "social security" gần số 9 chữ số).

### 2.2 Custom Data Identifiers

Cho phép detect dữ liệu đặc thù cho tổ chức (employee IDs, internal codes, proprietary data).

#### Thành phần cấu hình:

| Component | Mô tả | Giới hạn |
|-----------|--------|----------|
| **Regex** (required) | Pattern text cần match | Max 512 characters |
| **Keywords** (optional) | Words phải xuất hiện gần text match | Max 50 keywords, mỗi keyword 3-90 chars |
| **Maximum match distance** | Khoảng cách tối đa giữa keyword và text match | 1-300 characters (default: 50) |
| **Ignore words** (optional) | Words để exclude khỏi results | Max 10 words, mỗi word 4-90 chars |
| **Severity settings** (optional) | Custom severity dựa trên occurrence count | Low/Medium/High |

#### Cách Keywords hoạt động theo file type:

| File Type | Keyword Logic |
|-----------|--------------|
| **Structured columnar** (CSV, Excel, TSV) | Keyword trong tên column/field, hoặc trước text trong cùng cell |
| **Structured record** (JSON, Parquet, Avro) | Keyword trong element path name, hoặc trước text trong cùng field |
| **Unstructured** (PDF, Word, email, text) | Keyword trước text within max match distance |

#### Ví dụ Custom Data Identifier:

```
Name: Employee ID Detector
Regex: EMP-[0-9]{6}
Keywords: ["employee", "emp id", "staff number"]
Max match distance: 50
Ignore words: ["EXAMPLE", "TEST"]
```

**Lưu ý quan trọng:** Custom data identifiers **KHÔNG thể chỉnh sửa** sau khi tạo (immutable) — để đảm bảo audit trail nhất quán.

#### Regex hỗ trợ (PCRE subset):

**Hỗ trợ:** Character classes, quantifiers, alternation, anchors, case-insensitive `(?i)`

**KHÔNG hỗ trợ:** Backreferences, capturing groups, look-ahead/behind, recursive patterns, global flags

### 2.3 Allow Lists (Exceptions)

Định nghĩa text/patterns mà Macie sẽ **bỏ qua** khi phát hiện sensitive data.

#### 2 loại Allow Lists:

| Type | Mô tả | Use Case |
|------|--------|----------|
| **Predefined text** | Danh sách exact text cụ thể | Tên công khai, số phone công ty, test data |
| **Regular expression** | Regex pattern để ignore | Email domain công ty, phone format nội bộ |

**Ví dụ:**
- Allow list text: `["John Smith", "+84-28-1234-5678", "test@example.com"]`
- Allow list regex: `[a-z]+@mycompany\.com` (ignore tất cả email nội bộ)

**Nguyên tắc:** Nếu text match cả managed/custom identifier VÀ allow list → Macie **KHÔNG** report.

---

## 3. Findings (Kết quả phát hiện)

### 3.1 Hai loại Findings

#### Policy Findings
Phát hiện khi **security/privacy settings** của S3 bucket bị thay đổi:

| Finding Type | Mô tả | Severity |
|-------------|--------|----------|
| `Policy:IAMUser/S3BlockPublicAccessDisabled` | Block public access bị tắt | **High** |
| `Policy:IAMUser/S3BucketPublic` | Bucket cho phép anonymous/public access | **High** |
| `Policy:IAMUser/S3BucketSharedExternally` | Bucket shared với external account | **High** |
| `Policy:IAMUser/S3BucketReplicatedExternally` | Replication tới external account | **High** |
| `Policy:IAMUser/S3BucketSharedWithCloudFront` | Bucket shared qua CloudFront OAI/OAC | **Medium** |
| `Policy:IAMUser/S3BucketEncryptionDisabled` | Default encryption reset về SSE-S3 | **Low** |

**Đặc điểm Policy Findings:**
- Chỉ generate khi thay đổi xảy ra **SAU** khi enable Macie
- Subsequent occurrences → update existing finding (increment count)
- Lưu trữ **90 ngày**

#### Sensitive Data Findings
Phát hiện khi detect **sensitive data** trong S3 objects:

| Finding Type | Mô tả |
|-------------|--------|
| `SensitiveData:S3Object/Credentials` | Credentials (keys, tokens, certificates) |
| `SensitiveData:S3Object/Financial` | Financial info (credit cards, bank accounts) |
| `SensitiveData:S3Object/Personal` | PII + PHI (SSN, passport, medical IDs) |
| `SensitiveData:S3Object/CustomIdentifier` | Match custom data identifier criteria |
| `SensitiveData:S3Object/Multiple` | Nhiều categories trong cùng object |

**Đặc điểm Sensitive Data Findings:**
- Mỗi occurrence → **new finding** (không update existing)
- Lưu trữ **90 ngày**
- Bao gồm location info (vị trí chính xác của sensitive data trong object)

### 3.2 Severity Scoring

| Score | Level | Ý nghĩa |
|-------|-------|---------|
| 1 | **Low** | Rủi ro thấp |
| 2 | **Medium** | Rủi ro trung bình |
| 3 | **High** | Rủi ro cao, cần xử lý ngay |

#### Severity cho Sensitive Data Findings:

| Data Category | 1 occurrence | 2-99 occurrences | 100+ occurrences |
|--------------|-------------|-----------------|-----------------|
| **Credentials** | High | High | High |
| **Financial** | Varies by type | Medium → High | High |
| **Personal (PII/PHI)** | Varies by type | Medium → High | High |
| **Custom Identifier** | Medium (default) | Medium (configurable) | Medium (configurable) |

**Credentials luôn HIGH** vì dù chỉ 1 leaked credential cũng nguy hiểm.

### 3.3 Discovery Results

Ngoài Findings, Macie tạo **Sensitive Data Discovery Results** — logs chi tiết về quá trình analysis:
- Tạo cho **MỌI** object được analyze (kể cả không tìm thấy sensitive data)
- Lưu trong S3 bucket bạn configure
- Có thể query bằng Amazon Athena
- Dùng cho audit, compliance investigations

---

## 4. Tích hợp và Monitoring

### Integration Points

| Service | Chức năng |
|---------|----------|
| **Amazon EventBridge** | Publish findings as events → trigger Lambda, SNS, etc. |
| **AWS Security Hub** | Aggregate findings, check compliance standards |
| **Amazon S3** | Store discovery results (encrypted) |
| **Amazon Athena** | Query discovery results |
| **AWS Organizations** | Multi-account management |
| **CloudWatch Logs** | Monitor job execution |

### Multi-Account Management

- Tích hợp với **AWS Organizations** hoặc **invitation-based**
- Macie **administrator** có thể:
  - Review S3 bucket info cho member accounts
  - Review findings cho member accounts
  - Run discovery jobs trên member buckets
  - Enable/disable Macie cho member accounts
  - Configure automated discovery cho organization

---

## 5. Supported Object Types

### Storage Classes hỗ trợ:
- S3 Standard
- S3 Intelligent-Tiering
- S3 Standard-IA
- S3 One Zone-IA
- S3 Glacier Instant Retrieval (reduced)

### File Formats hỗ trợ:
- **Documents:** PDF, Word, Excel
- **Structured data:** CSV, TSV, JSON, JSON Lines, Parquet, Avro
- **Archives:** ZIP, GZIP, TAR
- **Email:** EML, MIME
- **Text:** Plain text, source code
- **Images:** Không trực tiếp (chỉ text-based content)

### Encryption hỗ trợ:
- SSE-S3 (Amazon S3 managed keys)
- SSE-KMS (AWS KMS managed keys — cần grant access)
- SSE-C: **KHÔNG hỗ trợ**

---

## 6. Best Practices

1. **Enable automated discovery** trước → overview data estate, rồi dùng jobs cho deep dive
2. **Configure discovery results repository** (S3 bucket) trước khi tạo jobs
3. **Dùng allow lists** để giảm false positives (test data, public info)
4. **Custom identifiers** cho proprietary data (employee IDs, internal codes)
5. **Integrate với EventBridge** → automated remediation workflows
6. **Publish to Security Hub** → centralized security view
7. **Review sensitivity scores** regularly để prioritize remediation
8. **Set up multi-account** nếu dùng AWS Organizations
9. **Test custom identifiers** trước khi deploy (dùng TestCustomDataIdentifier API)
10. **Dùng recommended managed identifiers** cho discovery jobs (Macie cung cấp recommended set)

---

## 7. Pricing Model

| Component | Tính phí theo |
|-----------|--------------|
| S3 bucket inventory & monitoring | Per bucket/month |
| Automated sensitive data discovery | Per GB analyzed |
| Sensitive data discovery jobs | Per GB analyzed |
| Free tier (30 ngày đầu) | Inventory & monitoring miễn phí |

**Tip:** Dùng job cost forecasting trước khi chạy large jobs.

---

## Quick Reference: Khi nào dùng gì

| Tình huống | Giải pháp |
|-----------|----------|
| Muốn biết tổng quan sensitive data trong toàn bộ S3 | Automated Discovery |
| Audit compliance cho specific buckets | Discovery Job (one-time) |
| Monitor ongoing cho critical buckets | Discovery Job (recurring) |
| Detect proprietary data format | Custom Data Identifier |
| Giảm false positives | Allow Lists |
| Automated response khi detect sensitive data | EventBridge → Lambda |
| Centralized security view | Security Hub integration |

---

*Sources: [Amazon Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/), [Macie API Reference](https://docs.aws.amazon.com/macie/latest/APIReference/)*
