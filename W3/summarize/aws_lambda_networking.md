# AWS Lambda Networking — Core Knowledge Summary

> **Mục tiêu:** Hiểu rõ Lambda chạy ở đâu, khi nào cần VPC, trade-offs, và pattern thiết kế đúng cho W3 project.

---

## 1. Lambda Execution Environment

Lambda **không luôn nằm trong VPC của bạn**. Có 2 chế độ:

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Cloud                            │
│                                                         │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │  AWS-Managed Network │    │   Your VPC           │  │
│  │  (Default Lambda)    │    │                      │  │
│  │                      │    │  ┌────────────────┐  │  │
│  │  ✅ Internet access  │    │  │ Private Subnet │  │  │
│  │  ✅ AWS public APIs  │    │  │   Lambda       │  │  │
│  │  ❌ Private VPC      │    │  │                │  │  │
│  │     resources        │    │  └────────────────┘  │  │
│  └──────────────────────┘    └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Lambda NGOÀI VPC (Default)

Khi tạo Lambda **không config VPC**, nó chạy trong AWS-managed network:

**Có thể làm:**
- Gọi internet (external APIs, third-party services)
- Gọi AWS services có public endpoint: S3, DynamoDB, SQS, SNS...
- Đơn giản, không cần cấu hình thêm

**Không thể làm:**
- Reach RDS trong private subnet
- Reach ElastiCache (Redis/Memcached)
- Reach EC2 trong private subnet
- Reach bất kỳ resource nào trong VPC của bạn

---

## 3. Lambda TRONG VPC

Khi config Lambda với VPC, nó được gắn ENI vào **private subnet** của bạn:

**Có thể làm:**
- Truy cập RDS, Aurora trong private/isolated subnet
- Truy cập ElastiCache
- Truy cập EC2 và private resources khác trong VPC

**Mất đi (mặc định):**
- ❌ Internet access — vì nằm trong private subnet, không có public IP

---

## 4. Khi Nào Đặt Lambda Vào VPC?

| Cần truy cập | Có cần VPC không? |
|---|---|
| RDS / Aurora trong private subnet | ✅ Bắt buộc |
| ElastiCache (Redis/Memcached) | ✅ Bắt buộc |
| EC2 trong private subnet | ✅ Bắt buộc |
| S3 (public endpoint) | ❌ Không cần |
| DynamoDB (public endpoint) | ❌ Không cần |
| External API (api.stripe.com...) | ❌ Không cần |
| SQS, SNS, Secrets Manager | ❌ Không cần (hoặc dùng Interface Endpoint) |

> **Nguyên tắc:** Chỉ đặt Lambda vào VPC khi thực sự cần reach private resources. Không cần thì để ngoài — đơn giản hơn, rẻ hơn.

---

## 5. Pattern Đúng Cho Lambda Trong VPC

Khi Lambda đã vào VPC, cần giải quyết bài toán connectivity:

```
Lambda (private subnet)
    │
    ├──→ RDS (isolated subnet)
    │       └── qua Security Group rule (Lambda SG → RDS SG)
    │
    ├──→ S3
    │       └── qua S3 Gateway Endpoint (miễn phí, không ra internet)
    │
    └──→ External API / Internet
            └── qua NAT Gateway (tốn phí)
```

### Chi phí cần tính
| Thành phần | Chi phí |
|---|---|
| NAT Gateway | ~$0.045/giờ + $0.045/GB data |
| S3 Gateway Endpoint | **Miễn phí** |
| Interface Endpoint (PrivateLink) | ~$0.01/giờ/AZ + data fee |

> **Tip tiết kiệm:** Dùng S3 Gateway Endpoint thay NAT Gateway cho traffic đến S3. Với workload đọc/ghi S3 nhiều, tiết kiệm được đáng kể.

---

## 6. Security Group Cho Lambda Trong VPC

Lambda trong VPC cần được gắn Security Group. Pattern chuẩn:

```
Lambda SG:
  Outbound: allow HTTPS (443) → 0.0.0.0/0  (để gọi internet qua NAT)
  Outbound: allow MySQL (3306) → RDS SG     (để connect RDS)

RDS SG:
  Inbound: allow MySQL (3306) → Lambda SG   (chỉ cho Lambda vào, không allow 0.0.0.0/0)
```

> **Quan trọng:** RDS SG inbound chỉ allow từ Lambda SG — không bao giờ allow `0.0.0.0/0`.

---

## 7. Key Takeaways

1. **Lambda mặc định ngoài VPC** → có internet, không có private resources.
2. **Lambda trong VPC** → có private resources, mất internet (cần NAT GW để lấy lại).
3. **Quyết định đặt vào VPC** dựa trên: có cần RDS/ElastiCache/private EC2 không?
4. **S3 Gateway Endpoint** giải quyết S3 access từ private subnet mà không cần NAT GW.
5. **SG rule** phải đúng chiều: Lambda SG outbound → RDS SG inbound (theo port cụ thể).

---

## Quick Reference — Câu hỏi hay gặp

**Q: Lambda trong VPC có chậm hơn không?**
A: Trước đây có (cold start chậm do tạo ENI). Từ 2020, AWS dùng Hyperplane ENI — Lambda trong VPC gần như không còn cold start penalty nữa.

**Q: Lambda cần subnet nào trong VPC?**
A: Private subnet. Không đặt Lambda vào public subnet — Lambda không cần public IP, và đặt vào public subnet cũng không tự có internet access.

**Q: Một Lambda có thể gắn nhiều subnet không?**
A: Có. Nên gắn vào **nhiều subnet ở nhiều AZ** để đảm bảo high availability. Lambda sẽ tự chọn subnet khi scale.

**Q: Lambda trong VPC có cần NAT Gateway không?**
A: Chỉ cần nếu Lambda phải gọi internet hoặc AWS services không có VPC Endpoint. Nếu chỉ cần S3 và DynamoDB → dùng Gateway Endpoint, không cần NAT GW.
