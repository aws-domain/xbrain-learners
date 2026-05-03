# Task 3.3 — AWS Compute Services

> **Exam weight:** Domain 3 = 34% of scored content

## Amazon EC2 (Elastic Compute Cloud)

### Instance Types
Được tối ưu cho các workload khác nhau:

| Family | Tối ưu cho | Ví dụ use case |
|--------|-----------|----------------|
| **General Purpose** (t3, m5) | Balanced CPU/memory | Web servers, small databases |
| **Compute Optimized** (c5, c6g) | High CPU | Batch processing, gaming, ML inference |
| **Memory Optimized** (r5, x1) | High RAM | In-memory databases, real-time analytics |
| **Storage Optimized** (i3, d2) | High I/O | Data warehousing, distributed file systems |
| **Accelerated Computing** (p3, g4) | GPU | ML training, video rendering |

### EC2 Purchasing Options

| Option | Mô tả | Tiết kiệm | Khi nào dùng |
|--------|-------|-----------|--------------|
| **On-Demand** | Trả theo giờ/giây, không cam kết | 0% | Dev/test, unpredictable workloads |
| **Reserved Instances** | Cam kết 1-3 năm | 40-75% | Steady-state workloads |
| **Spot Instances** | Dùng capacity dư của AWS | 60-90% | Fault-tolerant, flexible workloads |
| **Savings Plans** | Cam kết spend ($/hour) 1-3 năm | 40-66% | Flexible alternative to Reserved |
| **Dedicated Hosts** | Server vật lý riêng | Varies | License compliance (BYOL) |
| **Dedicated Instances** | Instance trên hardware riêng | Varies | Compliance, isolation |
| **Capacity Reservations** | Reserve capacity trong AZ | 0% | Đảm bảo có capacity khi cần |

### Auto Scaling
- Tự động **thêm/bớt EC2 instances** dựa trên demand
- **Scale out** = thêm instances khi tải tăng
- **Scale in** = bớt instances khi tải giảm
- Đảm bảo **elasticity** và **cost optimization**

### Load Balancers
| Type | Dùng cho |
|------|---------|
| **Application Load Balancer (ALB)** | HTTP/HTTPS, Layer 7, path-based routing |
| **Network Load Balancer (NLB)** | TCP/UDP, Layer 4, ultra-low latency |
| **Gateway Load Balancer (GWLB)** | Third-party virtual appliances |
| **Classic Load Balancer** | Legacy, không khuyến nghị dùng mới |

---

## Container Services

### Amazon ECS (Elastic Container Service)
- **Managed container orchestration** cho Docker containers
- Chạy containers trên EC2 instances hoặc Fargate
- Tích hợp sâu với AWS ecosystem (IAM, VPC, ALB...)

### Amazon EKS (Elastic Kubernetes Service)
- **Managed Kubernetes** trên AWS
- Dùng khi team đã quen với Kubernetes
- Hỗ trợ EC2 và Fargate

### AWS Fargate
- **Serverless compute cho containers**
- Không cần quản lý EC2 instances
- Dùng với ECS hoặc EKS
- Trả tiền theo vCPU và memory được dùng

---

## Serverless Compute

### AWS Lambda
- Chạy **code mà không cần quản lý servers**
- Trigger bởi events: API Gateway, S3, DynamoDB, SQS, SNS...
- Hỗ trợ: Python, Node.js, Java, Go, Ruby, .NET
- **Tính phí theo số lần gọi và thời gian chạy**
- Timeout tối đa: 15 phút
- Tự động scale từ 0 đến hàng nghìn concurrent executions

---

## Chọn Compute Service Phù Hợp

```
Cần kiểm soát OS/hardware?
├── Có → EC2
└── Không → Cần chạy containers?
    ├── Có → Cần quản lý cluster?
    │   ├── Có → ECS/EKS trên EC2
    │   └── Không → Fargate
    └── Không → Lambda (event-driven, short-running)
```

---

## Exam Tips

- Spot Instances = rẻ nhất nhưng có thể bị terminate bất cứ lúc nào
- Reserved Instances = tiết kiệm nhất cho steady-state workloads
- Dedicated Hosts = cần cho BYOL licensing
- Lambda = serverless, event-driven, không quản lý server
- Fargate = serverless containers (không quản lý EC2)
- Auto Scaling = elasticity; Load Balancer = distribute traffic
