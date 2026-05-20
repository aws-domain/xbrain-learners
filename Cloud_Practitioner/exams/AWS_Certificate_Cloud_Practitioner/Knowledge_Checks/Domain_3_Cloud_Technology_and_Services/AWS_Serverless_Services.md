# AWS Serverless Services

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following represents a serverless stack on AWS Cloud?

**Tiếng Việt**: Đâu là serverless stack trên AWS Cloud?

## Đáp án đúng ✅

**Step Functions + DynamoDB + Lambda**

## AWS Serverless Services

### ✅ **Lambda**
- Run code without provisioning servers
- Pay per execution
- Fully managed compute

### ✅ **DynamoDB**
- NoSQL database
- Fully managed
- No server provisioning

### ✅ **Step Functions**
- Coordinate multiple AWS services into workflows
- Orchestrate Lambda, Glue, SageMaker
- Fully managed

### ✅ **Other Serverless Services**
- S3, API Gateway, SNS, SQS, EventBridge, Fargate, Aurora Serverless, Athena, Glue

## KHÔNG PHẢI Serverless ❌

### ❌ **EC2**
- Phải provision servers
- Quản lý underlying OS
- **NOT serverless**

### ❌ **EMR (Elastic MapReduce)**
- Big data platform (Hadoop, Spark)
- Provisions **EC2 instances** để chạy workload
- **NOT serverless**

## Key Point

**Serverless = No server provisioning/management**

- Lambda, DynamoDB, Step Functions = Serverless ✅
- EC2, EMR = NOT serverless (cần provision servers) ❌
