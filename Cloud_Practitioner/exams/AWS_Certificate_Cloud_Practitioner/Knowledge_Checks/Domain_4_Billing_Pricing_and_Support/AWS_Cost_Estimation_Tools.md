# AWS Cost Estimation Tools

**Date**: 2026-05-11

## Câu hỏi

**English**: A startup wants to set up its IT infrastructure on AWS Cloud. The CTO would like to get an estimate of the monthly AWS bill based on the AWS services that the startup wants to use. As a Cloud Practitioner, which AWS service would you suggest for this use-case?

**Tiếng Việt**: Một startup muốn setup IT infrastructure trên AWS Cloud. CTO muốn ước tính hóa đơn AWS hàng tháng dựa trên các AWS services mà startup muốn dùng. Bạn sẽ suggest dịch vụ AWS nào?

## Đáp án đúng ✅

**AWS Simple Monthly Calculator** (hoặc **AWS Pricing Calculator** - phiên bản mới)

**Tại sao?**
- Ước tính chi phí **TRƯỚC KHI** dùng AWS services
- Input: List các AWS services muốn dùng
- Output: **Estimate monthly AWS bill**
- Dùng cho **planning/budgeting** trước khi deploy

## Các tools KHÔNG ĐÚNG ❌

### ❌ **AWS TCO Calculator (Total Cost of Ownership)**
**Tại sao sai?**
- Dùng để **so sánh** chi phí on-premises vs AWS
- Input: On-premises infrastructure config
- Output: Cost comparison (on-prem vs AWS)
- **KHÔNG ước tính** monthly bill based on AWS services list

**Use case**: Chứng minh cho management rằng migrate lên AWS rẻ hơn on-prem

### ❌ **AWS Cost Explorer**
**Tại sao sai?**
- Visualize **historical costs** (chi phí đã phát sinh)
- Xem chi phí **quá khứ** (up to 12 months)
- **KHÔNG ước tính** future costs cho services chưa dùng

**Use case**: Phân tích chi phí đã dùng, tìm cost trends

### ❌ **AWS Budgets**
**Tại sao sai?**
- Set **budget alerts** khi chi phí vượt ngưỡng
- Track actual spending vs budget
- **KHÔNG ước tính** monthly bill trước khi dùng

**Use case**: Cảnh báo khi chi phí vượt budget đã set

## So sánh 4 tools

| Tool | Use Case | Timing |
|------|----------|--------|
| **Simple Monthly Calculator** | Ước tính bill cho services muốn dùng | **BEFORE** using AWS ✅ |
| **TCO Calculator** | So sánh on-prem vs AWS | BEFORE migration |
| **Cost Explorer** | Phân tích chi phí đã phát sinh | **AFTER** using AWS |
| **Budgets** | Set alerts cho chi phí | **DURING** using AWS |

## Key Point

**"Estimate monthly bill based on AWS services list"** → **Simple Monthly Calculator**

- **BEFORE** dùng AWS → Simple Monthly Calculator ✅
- **AFTER** dùng AWS → Cost Explorer
- Set alerts → Budgets
- Compare on-prem vs AWS → TCO Calculator

## Lưu ý

**AWS Simple Monthly Calculator** đã được thay thế bởi **AWS Pricing Calculator** (phiên bản mới hơn), nhưng chức năng giống nhau.
