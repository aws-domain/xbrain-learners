# AWS SAM vs CloudFormation (CFN)

---

## 1. CloudFormation (CFN) là gì?

CloudFormation là dịch vụ **Infrastructure as Code (IaC)** của AWS. Bạn mô tả toàn bộ hạ tầng bằng file YAML/JSON, CFN sẽ tạo ra đúng những gì bạn mô tả trên AWS.

- Quản lý hạ tầng như code — có thể version control, review, rollback
- Tạo ra **Stack** — một tập hợp các AWS resources được quản lý như một đơn vị
- Hỗ trợ **toàn bộ** AWS services

### Ví dụ CFN thuần — tạo 1 Lambda + API Gateway

```yaml
Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-function
      Runtime: python3.11
      Handler: app.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: my-deployment-bucket
        S3Key: my-function.zip

  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  MyApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: my-api

  # ... thêm 50-100 dòng nữa để config API Gateway đầy đủ
```

Chỉ để tạo 1 Lambda + API Gateway đơn giản, CFN cần **100+ dòng**.

---

## 2. AWS SAM là gì?

SAM (Serverless Application Model) là **extension của CFN**, được thiết kế riêng cho serverless. SAM dùng cú pháp ngắn gọn hơn, rồi **tự động transform thành CFN template đầy đủ** trước khi deploy.

- Open-source framework
- Thêm dòng `Transform: AWS::Serverless-2016-10-31` để báo CFN đây là SAM template
- Tự động tạo IAM Role, config API Gateway, permissions — không cần viết tay

### Ví dụ SAM — cùng Lambda + API Gateway trên

```yaml
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 3
    MemorySize: 128

Resources:
  MyFunction:
    Type: AWS::Serverless::Function      # thay vì AWS::Lambda::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.11
      Events:
        Api:
          Type: Api
          Properties:
            Path: /users
            Method: get
```

SAM tự lo phần còn lại: tạo IAM Role, config API Gateway, mapping permissions.

---

## 3. So sánh SAM vs CFN

| | CloudFormation | SAM |
|---|---|---|
| Mục đích | Toàn bộ AWS infrastructure | Tập trung vào Serverless |
| Độ dài template | Dài, chi tiết | Ngắn gọn hơn nhiều |
| Resource type Lambda | `AWS::Lambda::Function` | `AWS::Serverless::Function` |
| Auto tạo IAM Role | ❌ Phải tự viết | ✅ Tự động |
| Auto config API Gateway | ❌ Phải tự viết | ✅ Tự động qua `Events` |
| Local testing | ❌ Không hỗ trợ | ✅ `sam local invoke` |
| Quan hệ | Nền tảng (engine) | Build trên CFN |

---

## 4. Quan hệ giữa SAM và CFN

SAM không thay thế CFN — SAM là **shorthand viết trên CFN**. Bạn viết ít hơn, SAM tự điền phần còn lại rồi đưa cho CFN xử lý.

```
Bạn viết SAM template (template.yaml)
        │
        │  sam deploy
        ▼
SAM transform → CFN template đầy đủ
        │
        ▼
CloudFormation deploy Stack lên AWS
```

> Giống như TypeScript vs JavaScript — bạn viết TypeScript (SAM), compiler chuyển thành JavaScript (CFN), rồi mới chạy thực sự.

---

## 5. SAM CLI — Các lệnh quan trọng

| Lệnh | Tác dụng |
|---|---|
| `sam init` | Khởi tạo project serverless mới |
| `sam build` | Build function, đóng gói dependencies |
| `sam local invoke` | Chạy Lambda function trên local (dùng Docker) |
| `sam local start-api` | Chạy API Gateway local để test |
| `sam validate` | Kiểm tra SAM template có hợp lệ không |
| `sam deploy --guided` | Deploy lên AWS, có hướng dẫn từng bước |
| `sam logs` | Xem CloudWatch logs của function |

---

## 6. Trong workshop thực hành

Khi bạn chạy `sam deploy`, thực ra đang xảy ra:

```
1. SAM đọc template.yaml
        ↓
2. Transform thành CFN template đầy đủ
        ↓
3. Upload code lên S3
        ↓
4. CFN tạo/cập nhật Stack trên AWS
```

**Tip**: Sau khi `sam build`, xem file `.aws-sam/build/template.yaml` để thấy CFN template đã được transform — hữu ích để hiểu SAM đang làm gì bên dưới.

---

## 7. Cấu trúc SAM template điển hình

```yaml
Transform: AWS::Serverless-2016-10-31

# Cấu hình mặc định cho tất cả functions
Globals:
  Function:
    Timeout: 3
    MemorySize: 128
    Runtime: python3.11

# Khai báo resources
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/           # thư mục chứa code
      Handler: app.handler    # file.function_name
      Environment:
        Variables:
          TABLE_NAME: !Ref MyTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /users
            Method: get

  MyTable:
    Type: AWS::Serverless::SimpleTable   # DynamoDB table đơn giản

# Outputs — hiển thị sau khi deploy xong
Outputs:
  ApiUrl:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/users"
  FunctionArn:
    Description: "Lambda Function ARN"
    Value: !GetAtt MyFunction.Arn
```

---

## 8. Khi nào dùng SAM, khi nào dùng CFN thuần?

| Tình huống | Dùng |
|---|---|
| Build serverless app (Lambda, API GW, DynamoDB) | **SAM** |
| Quản lý hạ tầng phức tạp (VPC, EC2, RDS, ECS...) | **CFN** |
| Cần local testing cho Lambda | **SAM** |
| CI/CD pipeline cho serverless | **SAM** |
| Kết hợp serverless + non-serverless resources | **SAM** (vẫn dùng được CFN syntax bên trong) |
