# AWS Scaling - Vertical vs Horizontal

**Date**: 2026-05-11

## Câu hỏi

**English**: Which of the following is an INCORRECT statement about Scaling, a design principle of Reliability pillar of the AWS Well-Architected Framework?

**Tiếng Việt**: Phát biểu nào SAI về Scaling, một design principle của Reliability pillar trong AWS Well-Architected Framework?

## Đáp án đúng (SAI) ✅

**"Fault tolerance is achieved by Vertical Scaling"** ← Phát biểu SAI

**Tại sao SAI?**
- Vertical scaling chạy trên **single instance/computer**
- **Single point of failure** - Instance fail → Toàn bộ system down
- **KHÔNG có fault tolerance**
- Fault tolerance chỉ có với **Horizontal Scaling** (multiple instances)

## Vertical Scaling (Scale UP/DOWN)

**Định nghĩa**: Tăng/giảm **power** của existing machine

**Cách thức**:
- Add more **CPU**
- Add more **RAM**
- Add more **Storage**
- Chạy trên **1 instance duy nhất**

**Đặc điểm**:
- ✅ Simple to implement
- ✅ No code changes needed
- ❌ **Single point of failure** - No fault tolerance
- ❌ Limited by hardware capacity
- ❌ Downtime khi upgrade

**Ví dụ**:
- t2.micro (1 vCPU, 1GB RAM) → t2.xlarge (4 vCPU, 16GB RAM)
- RDS db.t3.small → db.r5.4xlarge

**Use case**:
- Database (RDS, Aurora)
- Single-server applications
- Khi không thể distribute workload

## Horizontal Scaling (Scale OUT/IN)

**Định nghĩa**: Tăng/giảm **số lượng instances**

**Cách thức**:
- Add more **instances/computers**
- Distribute workload across multiple instances
- Load balancer phân phối traffic

**Đặc điểm**:
- ✅ **Fault tolerance** - Instance fail → Other instances handle workload
- ✅ **No single point of failure**
- ✅ **Unlimited scaling** (add more instances)
- ✅ **No downtime** khi scale
- ❌ Phức tạp hơn (cần load balancer, distributed architecture)

**Ví dụ**:
- 1 EC2 instance → 10 EC2 instances
- Auto Scaling Group: Scale from 2 → 20 instances
- Distributed systems (microservices)

**Use case**:
- Web applications
- Stateless applications
- Microservices architecture

## So sánh Vertical vs Horizontal Scaling

| Feature | Vertical Scaling | Horizontal Scaling |
|---------|------------------|-------------------|
| **Method** | Add CPU/RAM/Storage | Add more instances |
| **Instances** | 1 instance | Multiple instances |
| **Fault Tolerance** | ❌ **NO** (single point of failure) | ✅ **YES** (no single point of failure) |
| **Scaling Limit** | Limited by hardware | Unlimited (add more instances) |
| **Downtime** | Yes (khi upgrade) | No |
| **Complexity** | Simple | Complex (load balancer, distributed) |
| **Cost** | Expensive (bigger instance) | Cost-effective (many small instances) |

## Các phát biểu ĐÚNG ❌

### ✅ **"Vertical Scaling implies you scale by adding more power (CPU, RAM)"**
**ĐÚNG** - Vertical scaling = Add CPU/RAM/Storage vào existing machine

### ✅ **"Horizontal Scaling implies you scale by adding more instances"**
**ĐÚNG** - Horizontal scaling = Add more computers/instances

### ✅ **"Fault tolerance is achieved by Horizontal scaling"**
**ĐÚNG** - Horizontal scaling có multiple instances → No single point of failure → Fault tolerance

## Key Point

**Fault Tolerance**:
- ❌ **Vertical Scaling = NO fault tolerance** (single instance)
- ✅ **Horizontal Scaling = YES fault tolerance** (multiple instances)

**Nhớ**:
- Vertical = 1 instance = Single point of failure = **NO fault tolerance**
- Horizontal = Multiple instances = No single point of failure = **Fault tolerance** ✅

## AWS Well-Architected Framework - Reliability Pillar

**Design Principles**:
- Use **Horizontal Scaling** for fault tolerance
- Avoid single points of failure
- Distribute workload across multiple AZs
- Use Auto Scaling Groups

**Vertical Scaling** không đáp ứng Reliability pillar vì:
- Single point of failure
- No fault tolerance
- Downtime khi upgrade

## Ví dụ thực tế

**Scenario**: E-commerce website

**Vertical Scaling**:
- 1 EC2 t2.large instance
- Instance fail → **Website down** ❌
- No fault tolerance

**Horizontal Scaling**:
- 5 EC2 t2.small instances + Load Balancer
- 1 instance fail → 4 instances còn lại handle traffic ✅
- **Fault tolerance** achieved
