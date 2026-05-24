# AWS Cloud Characteristics - Agility vs Elasticity vs Scalability vs Reliability

**Date**: 2026-05-11

## Câu hỏi

**English**: A company wants to move to AWS cloud and release new features with quick iterations by utilizing relevant AWS services whenever required. Which of the following characteristics of AWS Cloud does it want to leverage?

**Tiếng Việt**: Một công ty muốn move lên AWS cloud và release features mới với quick iterations bằng cách sử dụng AWS services khi cần. Đặc điểm nào của AWS Cloud mà công ty muốn leverage?

## Đáp án đúng ✅

**Agility**

**Tại sao?**
- Keyword: **"quick iterations"**, **"release new features"**, **"whenever required"**
- Agility = Khả năng **rapidly develop, test, launch** applications
- **Instantly deploy** new applications (không cần đợi weeks/months)
- Quickly **innovate, experiment, iterate**

**Ví dụ**:
- On-premises: Cần hardware mới → Đợi 2 tháng mua server → Setup → Deploy
- AWS Cloud: Cần service mới → Click button → Deploy ngay lập tức ✅

## 4 Đặc điểm AWS Cloud

### 1. **Agility** ✅ (Đáp án đúng)

**Định nghĩa**: Khả năng **rapidly develop, test, launch** applications

**Đặc điểm**:
- Deploy new applications **instantly**
- Không cần đợi hardware provisioning
- Quickly **innovate, experiment, iterate**
- Access AWS services **whenever required**

**Use case**: 
- Startup cần test idea nhanh
- Release features với quick iterations
- Experiment với new technologies

**Ví dụ thực tế**:
- Cần database mới → Tạo RDS instance trong 5 phút
- Cần ML model → Dùng SageMaker ngay lập tức
- Cần serverless function → Deploy Lambda trong vài giây

### 2. **Elasticity**

**Định nghĩa**: Khả năng **acquire và release resources** theo nhu cầu

**Đặc điểm**:
- **Scale OUT** khi cần thêm resources
- **Scale IN** khi không cần nữa (release resources)
- **Automatic** scaling based on demand
- **Pay only** for what you use

**Use case**:
- Traffic tăng đột ngột → Auto scale thêm EC2
- Traffic giảm → Auto scale down, giảm chi phí

**Ví dụ thực tế**:
- Black Friday: Traffic tăng 10x → Auto scale từ 10 servers lên 100 servers
- Sau Black Friday: Traffic về bình thường → Scale down về 10 servers
- **Không lãng phí** tiền cho 90 servers không dùng

### 3. **Scalability**

**Định nghĩa**: Khả năng **grow hoặc shrink** để accommodate demand changes

**Đặc điểm**:
- **Vertical Scaling** (Scale UP/DOWN): Tăng/giảm size của resource (t2.micro → t2.large)
- **Horizontal Scaling** (Scale OUT/IN): Tăng/giảm số lượng resources (1 server → 10 servers)
- Measurement của system's ability to handle growth

**Use case**:
- App có 1000 users → Grow lên 1 triệu users
- Database nhỏ → Grow lên petabyte-scale

**Ví dụ thực tế**:
- Startup: 1 EC2 instance (1000 users)
- Sau 1 năm: 100 EC2 instances (1 triệu users)
- System có khả năng **scale** để handle growth

### 4. **Reliability**

**Định nghĩa**: Khả năng **recover from failures** và mitigate disruptions

**Đặc điểm**:
- System tự **recover** khi có infrastructure/service disruptions
- **Dynamically acquire** resources để meet demand
- **High availability** - System luôn hoạt động
- **Fault tolerance** - Chịu được lỗi

**Use case**:
- Server crash → Auto replace với server mới
- AZ failure → Failover sang AZ khác
- Data loss → Restore từ backup

**Ví dụ thực tế**:
- EC2 instance fail → Auto Scaling launch instance mới
- AZ us-east-1a down → Traffic route sang us-east-1b
- Database corrupt → Restore từ RDS snapshot

## So sánh 4 đặc điểm

| Characteristic | Focus | Keyword | Example |
|----------------|-------|---------|---------|
| **Agility** | Speed of innovation | Quick iterations, rapid deploy | Deploy new app in minutes ✅ |
| **Elasticity** | Resource flexibility | Acquire/release, auto scale | Scale 10→100→10 servers |
| **Scalability** | Growth capacity | Grow/shrink, handle demand | 1K users → 1M users |
| **Reliability** | Fault tolerance | Recover, high availability | Server crash → Auto replace |

## Key Point cho bài thi

**Nhận biết từ keywords**:

- **"Quick iterations"**, **"rapidly deploy"**, **"innovate fast"** → **Agility** ✅
- **"Auto scale"**, **"acquire/release resources"** → **Elasticity**
- **"Handle growth"**, **"accommodate demand increase"** → **Scalability**
- **"Recover from failure"**, **"high availability"** → **Reliability**

## Tóm tắt bằng ví dụ

**Scenario**: E-commerce website

- **Agility**: Deploy new payment feature trong 1 ngày (thay vì 2 tháng)
- **Elasticity**: Black Friday traffic tăng → Auto scale thêm servers → Sau đó scale down
- **Scalability**: Từ 10K users năm ngoái → 1M users năm nay, system vẫn handle được
- **Reliability**: 1 server crash → Auto replace, website vẫn chạy bình thường
