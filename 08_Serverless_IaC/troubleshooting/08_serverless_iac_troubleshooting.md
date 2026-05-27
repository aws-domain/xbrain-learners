# Topic 08: Serverless & IaC Troubleshooting — Khắc Phục Sự Cố CloudFormation Rollback & SAM Deploy

## 📌 Tổng quan cốt lõi (Core Concepts)
- **CloudFormation Rollback Mechanism:** Khi CloudFormation gặp bất kỳ lỗi nào trong quá trình khởi tạo hoặc cập nhật tài nguyên (ví dụ: lỗi cú pháp, thiếu quyền, vượt quá limit), nó sẽ tự động hoàn trả (Rollback) toàn bộ hệ thống về trạng thái an toàn trước đó.
- **AWS SAM (Serverless Application Model):** Là phần mở rộng của CloudFormation chuyên dùng để deploy Serverless Applications. Quá trình deploy của SAM dựa trên việc đóng gói mã nguồn code Lambda, đẩy lên một S3 Staging Bucket, chuyển đổi template thành CloudFormation thuần để khởi tạo tài nguyên.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ luồng lỗi Rollback của CloudFormation (CloudFormation Deploy & Rollback Flow)
```
[User: Run cfn-deploy] ──► [CloudFormation Engine]
                                   │
                                   ├──► 1. Validate Template Syntax? ──(Fail)──► [Immediate Failure]
                                   │
                                   ├──► 2. Create In-Progress (Resource by Resource)
                                   │       ├── Dependency missing? ───(Yes)───► [Dependency Error]
                                   │       └── IAM Role missing privilege? ──► [AccessDenied Error]
                                   │
                                   ▼ (Nếu xảy ra bất kỳ lỗi nào ở Phase 2)
                        [ROLLBACK_IN_PROGRESS] (Hủy toàn bộ tài nguyên vừa tạo)
                                   │
                                   ▼ (Hoàn thành rollback)
                        [ROLLBACK_COMPLETE]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Trạng thái Lỗi CloudFormation | Ý nghĩa thực tế | Cách xử lý |
|---|---|---|
| **`ROLLBACK_COMPLETE`** | Quá trình deploy thất bại và hệ thống đã khôi phục lại trạng thái cũ an toàn thành công. | Tìm nguyên nhân gốc rễ trong tab `Events`, sửa template và tiến hành deploy lại. |
| **`UPDATE_ROLLBACK_FAILED`** | **Cực kỳ nguy hiểm**. Quá trình khôi phục thất bại vì tài nguyên gốc đã bị xóa hoặc thay đổi ngoài luồng (Configuration Drift). Stack bị khóa cứng. | Phải sử dụng tính năng `ContinueUpdateRollback` và chủ động chọn Skip các tài nguyên bị lỗi để hoàn thành khôi phục. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. CloudFormation Stack bị Rollback
*   **Nguyên nhân 1: Sai lệch thứ tự phụ thuộc (Dependency Ordering):**
    *   **Cơ chế:** Bạn khai báo khởi tạo EC2 Instance trước khi VPC hoặc Subnet chứa nó được tạo xong.
    *   *Cách khắc phục:* Sử dụng thuộc tính `DependsOn` để chỉ định tường minh quan hệ phụ thuộc hoặc dùng hàm `!Ref`, `!GetAtt` để CloudFormation tự tính toán đồ thị phụ thuộc.
*   **Nguyên nhân 2: IAM Deployer Role thiếu quyền:**
    *   Tài khoản thực hiện lệnh deploy (hoặc IAM Role do CloudFormation assume) không có đủ quyền để tạo tài nguyên khai báo trong template (ví dụ cố gắng tạo IAM Role nhưng thiếu quyền `iam:CreateRole`).
*   **Nguyên nhân 3: Chạm ngưỡng Resource Limits:**
    *   Tài khoản đã chạm mốc giới hạn tối đa (ví dụ: đã tạo đủ 5 VPC mặc định trong Region).
*   **Cách kiểm tra và sửa đổi bằng CLI:**
    *   *Tìm nguyên nhân lỗi gốc rễ (Root Cause) bằng CLI:*
        ```bash
        aws cloudformation describe-stack-events \
          --stack-name my-app-stack \
          --query "StackEvents[?ResourceStatus=='CREATE_FAILED'].{Resource:LogicalResourceId,Reason:ResourceStatusReason}"
        ```
        *(Luôn luôn kéo lên tìm dòng `CREATE_FAILED` đầu tiên, vì các dòng tiếp theo chỉ là hiệu ứng domino rollback).*

### 2. AWS SAM Deploy thất bại
*   **Nguyên nhân 1: S3 Staging Bucket chưa được tạo hoặc sai cấu hình:**
    *   SAM cần một S3 Bucket để upload các file zip chứa code Lambda (`sam package`). Nếu bucket này bị xóa, phân quyền sai, hoặc bạn chưa tạo trước khi chạy deploy tay, quá trình đóng gói sẽ thất bại.
*   **Nguyên nhân 2: Lỗi logic/cú pháp trong template SAM (`template.yaml`):**
    *   Nhầm lẫn giữa cú pháp của CloudFormation và các từ khóa đặc biệt của SAM (ví dụ: `AWS::Serverless::Function`).
*   **Cách kiểm tra và xử lý bằng CLI:**
    *   *Kiểm tra cú pháp cục bộ trước khi deploy (Chống lỗi cú pháp):*
        ```bash
        sam validate --template template.yaml
        ```
    *   *Chỉ định tường minh S3 Staging Bucket trong câu lệnh deploy:*
        ```bash
        sam deploy \
          --template-file template.yaml \
          --stack-name my-serverless-app \
          --s3-bucket my-sam-staging-bucket-unique-name \
          --capabilities CAPABILITY_IAM
        ```
    *   *Tối ưu hóa:* Luôn sử dụng lệnh `sam deploy --guided` ở lần chạy đầu tiên để SAM tự tạo S3 bucket quản lý cấu hình mặc định trong file `samconfig.toml`.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **AWS CDK (Cloud Development Kit)** khi: Muốn viết hạ tầng (IaC) bằng các ngôn ngữ lập trình mạnh mẽ (TypeScript, Python) có hỗ trợ nhắc mã (IntelliSense) và viết unit test cho hạ tầng.
- Chọn **AWS SAM** khi: Tập trung phát triển các ứng dụng Serverless thuần túy (Lambda, API Gateway, DynamoDB) vì SAM cung cấp môi trường giả lập chạy local cực tốt (`sam local start-api`).
- Chọn **CloudFormation (YAML/JSON)** khi: Xây dựng các hạ tầng mạng ảo Core (VPC, Subnet, Route Table) tĩnh, ít khi thay đổi.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Troubleshoot AWS CloudFormation stack deletion or creation failures](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html)
  - [Deploying serverless applications using AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-deploying-applications.html)
