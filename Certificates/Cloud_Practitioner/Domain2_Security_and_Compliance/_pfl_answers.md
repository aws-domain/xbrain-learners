---

---
# PFL Answers — Domain 2: Security and Compliance

> Chỉ mở file này sau khi đã tự trả lời xong trong `_pfl_problems.md`

***

## Bài toán 2.1: Ai chịu trách nhiệm khi bị hack?

**EC2 bị hack qua lỗ hổng OS chưa patch:**

- **AWS KHÔNG chịu trách nhiệm.** EC2 là IaaS — AWS chỉ chịu trách nhiệm về phần cứng, hypervisor, và network infrastructure.
- **OS patching trên EC2 là trách nhiệm của Customer.** Bạn chọn AMI, bạn phải patch OS.
- Đây là ví dụ điển hình nhất của Shared Responsibility Model trong exam.

**Nếu dùng RDS thay EC2:**

- Trách nhiệm thay đổi đáng kể. RDS là managed service → **AWS chịu trách nhiệm patch OS và database engine.**
- Customer vẫn chịu trách nhiệm: database settings, user access, data encryption, security groups.
- Nếu RDS bị hack qua lỗ hổng OS → AWS chịu trách nhiệm.
- Nếu RDS bị hack vì customer để password yếu → Customer chịu trách nhiệm.

**Hacker xâm nhập data center vật lý:**

- **AWS chịu trách nhiệm hoàn toàn.** Physical security của data center là "Security OF the cloud" — thuộc phần AWS.

**Quy tắc nhớ nhanh:**

- Dịch vụ càng "managed" → AWS càng chịu nhiều trách nhiệm hơn
- Data và access management → luôn là trách nhiệm của Customer

***

## Bài toán 2.2: Thiết lập IAM cho team mới

**IAM Structure đề xuất — dùng Groups:**

| Group                 | Members | Policy                                    |
| --------------------- | ------- | ----------------------------------------- |
| `developers`          | Alice   | AmazonS3FullAccess + AWSLambda_FullAccess |
| `dba`                 | Bob     | AmazonRDSFullAccess                       |
| `devops`              | Carol   | AmazonEC2FullAccess + AmazonVPCFullAccess |
| `readonly-monitoring` | Dave    | CloudWatchReadOnlyAccess                  |

**Tại sao dùng Groups:**

- Khi Dave thăng chức → chỉ cần remove khỏi `readonly-monitoring`, add vào `developers`. Không cần sửa policy.
- Dễ audit: nhìn vào group là biết ai có quyền gì.

**Custom policy hay Managed policy:**

- Với trường hợp này, AWS Managed Policies là đủ và đơn giản hơn.
- Custom policy cần thiết khi cần restrict xuống resource cụ thể (ví dụ: Alice chỉ được access S3 bucket `project-x`).

**MFA:**

- **Bắt buộc cho tất cả** — đây là security best practice.
- Đặc biệt quan trọng với Carol (DevOps, có quyền cao nhất).
- Root account phải có MFA trước tiên.

***

## Bài toán 2.3: Audit security của một account AWS

**Xếp hạng theo mức độ nghiêm trọng:**

| Thứ tự | Vấn đề                              | Lý do                                     | Cách fix                                             |
| ------ | ----------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| 🔴 1   | S3 bucket public chứa data nhạy cảm | Data đang bị lộ **ngay lúc này**          | Block public access ngay lập tức                     |
| 🔴 2   | SSH port 22 mở cho `0.0.0.0/0`      | Bất kỳ IP nào cũng có thể brute-force SSH | Restrict về IP cụ thể hoặc dùng SSM Session Manager  |
| 🟠 3   | Root account dùng hàng ngày         | Nếu bị compromise → mất toàn bộ account   | Tạo IAM admin user, stop dùng root, bật MFA cho root |
| 🟠 4   | IAM users không có MFA              | Credential bị lộ → account bị chiếm       | Enforce MFA policy                                   |
| 🟡 5   | Không có CloudTrail                 | Không thể audit, không biết ai đã làm gì  | Bật CloudTrail ngay (free tier có 1 trail miễn phí)  |

**Nếu chỉ fix 2 vấn đề ngay hôm nay:**

1. **S3 bucket public** — data đang bị lộ ngay lúc này, thiệt hại thực tế đang xảy ra.
2. **SSH port 22 mở** — attack vector đang active, có thể bị exploit bất cứ lúc nào.

Root account và MFA quan trọng nhưng là preventive measures — chưa có thiệt hại ngay lập tức.

***

## Bài toán 2.4: Thiết kế IAM cho ứng dụng

**IAM Policy cho Lambda (Principle of Least Privilege):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:region:account:secret:my-secret-*"
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"],
      "Resource": "arn:aws:dynamodb:region:account:table/my-specific-table"
    },
    {
      "Effect": "Allow",
      "Action": ["sqs:SendMessage"],
      "Resource": "arn:aws:sqs:region:account:my-queue"
    }
  ]
}
```

**Tại sao dùng IAM Role thay vì IAM User:**

- IAM User có long-term credentials (access key + secret) → nếu lộ key là nguy hiểm
- IAM Role cấp **temporary credentials** tự động rotate → an toàn hơn nhiều
- Best practice: **applications dùng Roles, humans dùng Users**

**Cross-account access:**

- Cần **Resource-based policy** trên resource ở account B (trust policy cho phép account A)
- Và **Identity-based policy** trên Role ở account A (cho phép assume role ở account B)

**Break scenarios:**

- Xóa DynamoDB permission → Lambda throw `AccessDeniedException`
- Permission `*` cho tất cả DynamoDB → vi phạm Least Privilege, Lambda có thể đọc/ghi/xóa bất kỳ table nào → security risk nghiêm trọng

***

## Bài toán 2.5: Compliance cho ứng dụng y tế

**AWS có HIPAA compliant không?**

- Câu trả lời **phức tạp hơn yes/no.**
- AWS cung cấp **HIPAA-eligible services** — infrastructure của AWS đáp ứng yêu cầu HIPAA.
- Nhưng **compliance là shared responsibility**: AWS compliant với phần của họ, bạn phải compliant với phần của bạn.
- Bạn cần ký **Business Associate Agreement (BAA)** với AWS trước khi xử lý PHI (Protected Health Information).

**Shared Responsibility khi có compliance:**

- AWS: Cung cấp compliant infrastructure, ký BAA, cung cấp audit reports
- Customer: Thiết kế application đúng cách, encrypt data, control access, train nhân viên, document policies

**AWS Artifact:**

- Portal để download **compliance reports và certifications** của AWS (SOC 2, ISO 27001, HIPAA, PCI DSS...)
- Dùng để chứng minh với khách hàng/auditor rằng AWS infrastructure đáp ứng yêu cầu compliance
- Cũng dùng để ký BAA với AWS

**HIPAA-eligible services:** EC2, S3, RDS, Lambda, DynamoDB, CloudTrail, CloudWatch (và nhiều hơn — kiểm tra danh sách chính thức của AWS)

***

## Bài toán 2.6: Phát hiện và phản ứng với security incident

**Các bước xử lý ngay lập tức (theo thứ tự):**

1. **Disable IAM user ngay lập tức** — deactivate access keys, không xóa (cần để forensics)
2. **Revoke active sessions** — attach policy deny hoặc set `aws:TokenIssueTime` condition
3. **Terminate EC2 instances** đang được tạo ở region lạ
4. **Block S3 data export** — review và restrict S3 bucket policies
5. **Snapshot evidence** — lưu lại logs trước khi bất kỳ thứ gì bị xóa
6. **Notify security team** và escalate

**Service phát hiện activity bất thường:**

- **Amazon GuardDuty** — threat detection service, dùng ML để phát hiện unusual API calls, unauthorized deployments, suspicious activity.

**Revoke active sessions:**

- Vào IAM → User → Security credentials → **Revoke active sessions**
- Hoặc attach inline policy deny tất cả actions với condition `aws:TokenIssueTime`

**Điều tra root cause:**

- **AWS CloudTrail** — ghi lại tất cả API calls với timestamp, IP, user agent.
- **Amazon Detective** — tự động phân tích CloudTrail, VPC Flow Logs, GuardDuty findings để visualize security incidents.

***

## Exam-style Questions — Đáp án

**Câu 1:** Ai chịu trách nhiệm patch OS trên Amazon RDS?

**AWS** chịu trách nhiệm patch OS trên RDS. RDS là managed service — AWS quản lý OS và database engine patching.

So sánh: Trên EC2, **Customer** phải tự patch OS.

***

**Câu 2:** Chỉ cho phép user đã bật MFA xóa S3 objects.

Dùng **IAM Policy với condition** `aws:MultiFactorAuthPresent`**:**

```json
{
  "Effect": "Deny",
  "Action": "s3:DeleteObject",
  "Resource": "*",
  "Condition": {
    "BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}
  }
}
```

***

**Câu 3:** IAM Role khác IAM User ở điểm nào quan trọng nhất?

**IAM Role sử dụng temporary credentials** (tự động expire và rotate), trong khi IAM User có long-term credentials (access key không tự expire).

- Role không có username/password — được **assumed** bởi entities
- Role phù hợp cho applications và AWS services
- User phù hợp cho con người cần đăng nhập

***

**Câu 4:** AWS service nào cung cấp báo cáo compliance?

**AWS Artifact** — cung cấp on-demand access đến AWS compliance reports (SOC, ISO, PCI, HIPAA...) và cho phép ký agreements như BAA.

Không nhầm với: AWS Config (track config changes), CloudTrail (log API calls), Security Hub (centralized findings).

***

**Câu 5:** Developer commit AWS access key lên GitHub. Bước đầu tiên?

**Deactivate (hoặc delete) access key ngay lập tức** — trước khi làm bất kỳ thứ gì khác.

Lý do: Bots tự động scan GitHub và có thể đã lấy key trong vài phút. Xóa key khỏi GitHub là không đủ.

Sau đó: Kiểm tra CloudTrail → tạo key mới → update application → review IAM permissions.
