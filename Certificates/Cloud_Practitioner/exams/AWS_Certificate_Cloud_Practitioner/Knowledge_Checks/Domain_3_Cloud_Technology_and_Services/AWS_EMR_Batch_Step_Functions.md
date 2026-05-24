# AWS Big Data and Batch Processing Services

**Date**: 2026-05-12

## Câu hỏi

**English**: Which AWS service can be used to provision resources to run big data workloads on Hadoop clusters?

**Tiếng Việt**: AWS service nào có thể được dùng để provision resources cho big data workloads trên Hadoop clusters?

## Đáp án đúng ✅

**Amazon EMR (Elastic MapReduce)**

**Tại sao?**
- ✅ **Big data platform** cho Hadoop clusters
- ✅ **Provision resources** để run big data workloads
- ✅ Support **Hadoop, Spark, Hive, HBase, Flink, Presto**
- ✅ Industry-leading cloud big data platform

**Keywords trong câu hỏi**:
- "**Big data workloads**" → EMR ✅
- "**Hadoop clusters**" → EMR ✅
- "**Provision resources**" → EMR provisions EC2 instances

## Amazon EMR (Elastic MapReduce)

**Chức năng**: Cloud **big data platform** for Hadoop

**Đặc điểm**:
- ✅ Process **vast amounts of data**
- ✅ **Open source tools**: Hadoop, Spark, Hive, HBase, Flink, Hudi, Presto
- ✅ **Provision resources** (EC2 instances) để run Hadoop clusters
- ✅ Managed service - AWS handles cluster setup

**Use cases**:
- ✅ **Big data processing** (Hadoop/Spark workloads)
- ✅ Data transformation (ETL)
- ✅ Log analysis
- ✅ Machine learning (Spark MLlib)
- ✅ Data warehousing

**How it works**:
1. Create EMR cluster
2. EMR provisions **EC2 instances** (master, core, task nodes)
3. Run Hadoop/Spark jobs
4. Process big data
5. Terminate cluster khi done

## Các đáp án SAI ❌

### ❌ **AWS Step Functions**

**Chức năng**: **Orchestrate workflows** (serverless)

**Đặc điểm**:
- Coordinate multiple AWS services
- Serverless workflows
- Stitch together Lambda, Glue, SageMaker
- **KHÔNG provision resources**

**Tại sao SAI?**
- Step Functions **orchestrates services**, không provision resources
- **KHÔNG run Hadoop clusters**
- Không phải big data platform

**Use case**: Workflow orchestration, NOT big data processing

**Exam Alert**: 
- **Step Functions**: Orchestrate workflows, NO resource provisioning
- **AWS Batch**: Provision resources cho batch jobs
- **EMR**: Provision resources cho Hadoop/big data

### ❌ **AWS Batch**

**Chức năng**: **Batch computing workloads**

**Đặc điểm**:
- Plan, schedule, execute **batch jobs**
- **Dynamically provisions** compute resources (EC2)
- Optimize job distribution
- CPU/memory optimized instances

**Tại sao SAI?**
- AWS Batch dùng cho **batch computing**, không phải **Hadoop clusters**
- Không phải big data platform
- Không support Hadoop/Spark

**Use case**: Batch processing, NOT Hadoop big data

**Exam Alert**:
- **AWS Batch**: Batch computing workloads (provisions resources)
- **EMR**: Big data workloads on Hadoop (provisions resources)

### ❌ **Amazon EC2**

**Chức năng**: **Virtual servers** (compute)

**Đặc điểm**:
- Provision virtual servers
- Resizable compute capacity
- IaaS service

**Tại sao SAI?**
- EC2 chỉ là **compute instances**, không phải big data platform
- **KHÔNG tự động** setup Hadoop clusters
- Phải manual configure Hadoop (phức tạp)

**Use case**: General compute, NOT managed Hadoop clusters

**Lưu ý**: EMR **uses EC2** internally, nhưng EMR là managed service cho Hadoop

## So sánh EMR vs Batch vs Step Functions

| Feature | EMR | AWS Batch | Step Functions |
|---------|-----|-----------|----------------|
| **Purpose** | Big data (Hadoop) | Batch computing | Workflow orchestration |
| **Provision Resources** | ✅ YES (EC2 for Hadoop) | ✅ YES (EC2 for batch) | ❌ NO (serverless) |
| **Hadoop Support** | ✅ YES | ❌ NO | ❌ NO |
| **Use Case** | Big data processing | Batch jobs | Orchestrate services |

## Exam Alert - Step Functions vs Batch

### **AWS Step Functions**
- **Orchestrates** AWS services
- **Serverless** - NO resource provisioning
- Coordinate Lambda, Glue, SageMaker
- **Use case**: Workflow automation

### **AWS Batch**
- **Provisions** compute resources (EC2)
- Plan, schedule, execute **batch jobs**
- Optimize resource allocation
- **Use case**: Batch computing workloads

### **Key Difference**
- **Step Functions**: Orchestrate (NO provisioning)
- **Batch**: Provision resources cho batch jobs
- **EMR**: Provision resources cho Hadoop/big data

## Use Cases Comparison

### **EMR** ✅
```
Scenario: Process 100TB log files với Hadoop
Solution: EMR
- Create Hadoop cluster
- EMR provisions EC2 instances
- Run Hadoop MapReduce jobs
- Process big data
```

### **AWS Batch** ❌
```
Scenario: Run nightly batch jobs (không phải Hadoop)
Solution: AWS Batch
- Submit batch jobs
- Batch provisions EC2 instances
- Execute jobs
- NOT for Hadoop
```

### **Step Functions** ❌
```
Scenario: Orchestrate ETL pipeline
Solution: Step Functions
- Trigger Lambda → Glue → SageMaker
- NO resource provisioning
- Workflow orchestration only
```

## Key Point

**"Big data workloads on Hadoop clusters"** → **Amazon EMR** ✅

**EMR = Managed Hadoop/Spark platform**
- Provisions EC2 instances
- Setup Hadoop clusters
- Run big data workloads

**KHÔNG phải**:
- Step Functions = Orchestration (NO provisioning)
- AWS Batch = Batch jobs (NOT Hadoop)
- EC2 = Compute (NOT managed Hadoop)

## Ví dụ thực tế

**Scenario**: Company cần process 50TB clickstream data với Hadoop

### ✅ **Đúng - Dùng EMR**
```
1. Create EMR cluster
   - Master node: 1x m5.xlarge
   - Core nodes: 10x m5.2xlarge
   - Task nodes: 20x m5.xlarge

2. EMR provisions EC2 instances
3. Setup Hadoop cluster automatically
4. Upload data to HDFS
5. Run Hadoop MapReduce jobs
6. Process 50TB data
7. Output results to S3
8. Terminate cluster

→ Managed Hadoop platform ✅
```

### ❌ **Sai - Dùng AWS Batch**
```
AWS Batch:
- Dùng cho batch jobs, NOT Hadoop
- Không support Hadoop/Spark
- Không phù hợp cho big data processing
```

### ❌ **Sai - Dùng Step Functions**
```
Step Functions:
- Chỉ orchestrate workflows
- KHÔNG provision resources
- KHÔNG run Hadoop
```

## Lưu ý cho bài thi

**Keywords nhận biết EMR**:
- "**Big data**" → EMR
- "**Hadoop**" → EMR
- "**Spark**" → EMR
- "**Provision resources for Hadoop**" → EMR

**Keywords nhận biết Batch**:
- "**Batch computing**" → AWS Batch
- "**Batch jobs**" → AWS Batch
- "**NOT Hadoop**" → AWS Batch

**Keywords nhận biết Step Functions**:
- "**Orchestrate**" → Step Functions
- "**Workflow**" → Step Functions
- "**NO provisioning**" → Step Functions

## Tóm tắt

**EMR**: Big data platform, provisions resources cho **Hadoop clusters** ✅
**Batch**: Batch computing, provisions resources cho **batch jobs**
**Step Functions**: Workflow orchestration, **NO provisioning**
