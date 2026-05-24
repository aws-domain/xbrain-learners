# PFL Problems — Domain 2: Security and Compliance

> Tham khảo: `resources/learning-method/problem_first_learning.md`  
> Lý thuyết liên quan: `01_shared_responsibility_model.md`, `02_security_governance_compliance.md`, `03_iam_access_management.md`, `04_security_components_resources.md`  
> Đáp án: `_pfl_answers.md`

---

## Cách dùng file này

1. Chọn một bài toán bên dưới
2. **Không đọc lý thuyết trước** — thử phân tích bằng những gì bạn đã biết
3. Khi bị kẹt, mới mở file lý thuyết tương ứng
4. Sau khi có câu trả lời, mở `_pfl_answers.md` để kiểm tra

---

## Level 1 — Foundation

### Bài toán 2.1: Ai chịu trách nhiệm khi bị hack?

**Tình huống:**
Công ty bạn đang chạy web app trên EC2. Một ngày, hacker xâm nhập vào server thông qua lỗ hổng trong OS chưa được patch. Dữ liệu khách hàng bị lộ.

**Câu hỏi:**
- AWS có chịu trách nhiệm về sự cố này không? Tại sao?
- Nếu thay EC2 bằng RDS (managed database), trách nhiệm có thay đổi không?
- Nếu hacker xâm nhập vào data center vật lý của AWS, ai chịu trách nhiệm?

*Lý thuyết liên quan: `01_shared_responsibility_model.md`*

---

### Bài toán 2.2: Thiết lập IAM cho team mới

**Tình huống:**
Bạn vừa onboard một team 4 người:
- **Alice** — Developer, cần đọc/ghi S3 và deploy Lambda
- **Bob** — DBA, chỉ cần truy cập RDS
- **Carol** — DevOps, cần full access EC2 và VPC
- **Dave** — Intern, chỉ được xem CloudWatch logs, không được thay đổi gì

**Yêu cầu:**
Thiết kế IAM structure cho team này. Quyết định:
- Dùng Users, Groups, hay Roles?
- Tạo custom policy hay dùng AWS managed policy?
- Có cần MFA không? Cho ai?

**Ràng buộc:**
- Principle of least privilege phải được áp dụng
- Nếu Dave được thăng chức thành Developer, việc cập nhật permission phải đơn giản nhất có thể

*Lý thuyết liên quan: `03_iam_access_management.md`*

---

## Level 2 — Integration

### Bài toán 2.3: Audit security của một account AWS

**Tình huống:**
Bạn được giao nhiệm vụ audit security của một AWS account đang có vấn đề. Bạn phát hiện:
- Root account đang được dùng hàng ngày
- Có 3 IAM user không có MFA
- Một S3 bucket chứa data nhạy cảm đang ở chế độ public
- Security group của EC2 đang mở port 22 (SSH) cho `0.0.0.0/0`
- Không có CloudTrail logging

**Yêu cầu:**
Xếp hạng các vấn đề theo mức độ nghiêm trọng và đề xuất cách fix từng cái.

**Câu hỏi trade-off:**
- Nếu chỉ có thể fix 2 vấn đề ngay hôm nay, bạn chọn 2 cái nào? Tại sao?

*Lý thuyết liên quan: `03_iam_access_management.md`, `04_security_components_resources.md`*

---

### Bài toán 2.4: Thiết kế IAM cho ứng dụng (không phải người dùng)

**Tình huống:**
Bạn có một Lambda function cần:
- Đọc secrets từ AWS Secrets Manager
- Ghi logs vào CloudWatch
- Đọc/ghi vào một DynamoDB table cụ thể
- Gửi message vào SQS queue

**Yêu cầu:**
- Tạo IAM policy cho Lambda function này
- Tại sao dùng IAM Role thay vì IAM User cho Lambda?
- Nếu Lambda cần access resource ở account AWS khác, cần thêm gì?

**Break scenario:**
- Xóa permission DynamoDB → Lambda báo lỗi gì?
- Thêm permission `*` cho tất cả DynamoDB → có vấn đề gì về security?

*Lý thuyết liên quan: `03_iam_access_management.md`*

---

## Level 3 — Trade-off Decisions

### Bài toán 2.5: Compliance cho ứng dụng y tế

**Tình huống:**
Công ty bạn đang xây dựng app quản lý hồ sơ bệnh nhân. Khách hàng yêu cầu tuân thủ HIPAA.

**Câu hỏi:**
- AWS có "HIPAA compliant" không? Câu trả lời có phức tạp hơn yes/no không?
- Shared Responsibility Model thay đổi thế nào khi có yêu cầu compliance?
- AWS Artifact dùng để làm gì trong trường hợp này?
- Những dịch vụ AWS nào được HIPAA eligible?

*Lý thuyết liên quan: `02_security_governance_compliance.md`*

---

### Bài toán 2.6: Phát hiện và phản ứng với security incident

**Tình huống:**
Lúc 2 giờ sáng, bạn nhận được alert: có activity bất thường từ một IAM user — đang tạo EC2 instances ở region bạn chưa từng dùng, và đang cố gắng export data từ S3.

**Yêu cầu:**
Liệt kê các bước bạn sẽ làm ngay lập tức, theo thứ tự ưu tiên.

**Câu hỏi:**
- AWS service nào đã phát hiện activity bất thường này?
- Làm thế nào để revoke tất cả active sessions của IAM user đó ngay lập tức?
- Sau khi xử lý xong, dùng service nào để điều tra root cause?

*Lý thuyết liên quan: `04_security_components_resources.md` — GuardDuty, CloudTrail, IAM*

---

## Exam-style Questions

Trả lời **không nhìn tài liệu**, sau đó mở `_pfl_answers.md` để kiểm tra:

1. Theo Shared Responsibility Model, ai chịu trách nhiệm patch OS trên Amazon RDS?

2. Một công ty muốn đảm bảo chỉ những người dùng đã bật MFA mới được phép xóa S3 objects. Cách nào để thực hiện điều này?

3. IAM Role khác IAM User ở điểm nào quan trọng nhất?

4. AWS service nào cung cấp báo cáo compliance và chứng chỉ bảo mật của AWS?

5. Một developer vô tình commit AWS access key lên GitHub public repo. Bước đầu tiên cần làm ngay là gì?

---

## Ghi chép của tôi

```markdown
### [Tên bài toán]
**Ngày:** 
**Thời gian:** 
**Solution của tôi:** 

**Điều tôi chưa biết trước khi làm:**

**Điều bất ngờ / sai lầm:**

**Câu hỏi mở rộng cho lần sau:**
```
