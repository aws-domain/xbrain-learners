# CloudWatch Agent Trong Auto Scaling Group: Agent Đến Từ Đâu?
**Chủ đề (Topic):** Observability & Operations
**Domain liên quan:** SOA-C02 Domain 1 (Monitoring, Logging, and Remediation) + liên quan Compute (ASG)
**Note liên quan:** `unified_cloudwatch_agent_setup.md`, `cloudwatch_cli_put_commands.md`, lab `d1-03`

---

## 0. Tóm Tắt Một Dòng
Trong một **Auto Scaling Group (ASG)**, instance có CloudWatch agent hay không là do **AMI** quyết định (hoặc do user data / SSM tự cài), **không phải** do một "công tắc agent" của ASG. ASG chỉ nhân bản y nguyên AMI bạn chỉ định.

---

## 1. Bài Toán Gốc (câu hỏi thi)
Một ASG của team A có agent, ASG của team B không có. Engineer **chưa tự cài tay** trên cả hai. Vì sao lệch?

**Root cause đúng:** AMI của team A đã được **bake sẵn** CloudWatch agent trong image, nên mọi instance sinh ra đều tự có. Team B dùng **stock Amazon Linux AMI** (AMI trần) nên instance không có agent, phải tự cài (AWS khuyến nghị cài qua `yum`).

Nguyên tắc nền đã học: **AWS không tự cài CloudWatch agent.** Agent chỉ có mặt qua 2 đường:
1. Tự cài sau khi instance chạy (yum / SSM / user data).
2. Đã cài sẵn và lưu vào AMI từ trước (**baked AMI**).

---

## 2. Cơ Chế: AMI Quyết Định, ASG Chỉ Nhân Bản

```
AMI-A (da bake CloudWatch agent) ---> ASG nhan ban ---> Instance co agent  OK
AMI-B (stock Amazon Linux, tran)  ---> ASG nhan ban ---> Instance KHONG co agent (phai tu cai)
```

**Analogy:** AMI như khuôn đúc bánh. Khuôn có sẵn hạt nho thì mọi chiếc bánh đúc ra đều có nho; khuôn trơn thì bánh trơn. ASG là máy đúc hàng loạt, nó đổ đúng cái khuôn bạn đưa, không tự rắc thêm nho.

*Chỗ analogy gãy:* vẫn có thể "rắc nho sau khi ra lò" bằng user data / SSM cài agent lúc instance boot. Nhưng nếu không làm gì thêm, bánh giống hệt khuôn.

---

## 3. Vì Sao 3 Đáp Án Kia Sai (bẫy thi)

| Đáp án sai | Lý do loại |
|---|---|
| Có một **flag** trong lúc cấu hình ASG để nạp agent, dev lỡ tích vào 1 ASG | **Không tồn tại flag đó.** ASG / launch template không có ô "cài CloudWatch agent". Distractor bịa. |
| InstanceType không khớp architecture của image -> ASG tạo lỗi, **bỏ qua** agent | Sai logic. ASG hoặc **tạo thành công** hoặc **fail hoàn toàn**, không có chuyện tạo nửa vời rồi skip riêng agent. |
| Architecture không tương thích AMI -> **một số AWS service không được cài** | Nếu lệch architecture, ASG **không spin up được instance** và báo lỗi tương thích ngay, chứ không chạy được mà thiếu service. |

**Điểm chung của bẫy:** cả 3 dựng ra một cơ chế "cài nửa vời" hoặc "có công tắc agent" — AWS không có hành vi đó.

---

## 4. Từ Khóa Quyết Định Trong Đề
- "has **not manually installed**" + một nhóm vẫn có agent -> agent phải đến từ **AMI**.
- Nguyên tắc ngầm: ASG **tạo thành công hoặc fail hoàn toàn** -> loại mọi đáp án nói "skip service từng phần".

---

## 5. Thực Tế Nên Làm Thế Nào (ý bổ sung, không phải nội dung đề gốc)
Đời thực ít ai bake agent vào AMI thủ công vì sửa config phải rebuild AMI. Cách phổ biến để mọi instance trong ASG (kể cả instance scale-out mới) đều có agent:

- **User data** trong launch template: script cài agent lúc boot.
  ```bash
  #!/bin/bash
  yum install -y amazon-cloudwatch-agent
  /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config -m ec2 -s -c ssm:AmazonCloudWatch-td-agent-config
  ```
- **SSM State Manager association**: tự cài và giữ agent trên mọi instance, kể cả instance mới sinh. Đây là pattern **"least operational overhead"** (giống cách rải config cho fleet đa Region trong lab `d1-03`).

---

## 6. Mẹo Nhớ
Gặp câu "sao instance trong ASG có / không có agent" -> nghĩ ngay tới **AMI** (và user data). **ASG chỉ nhân bản, không tự cài gì.**

---

## 7. Câu Tự Kiểm Tra
Bạn muốn **mọi** instance mới do ASG scale-out đều có CloudWatch agent, mà **không** phải rebuild AMI mỗi lần đổi config. Dùng cơ chế nào trong launch template, và vì sao tiện hơn bake vào AMI?

<details>
<summary>Đáp án</summary>

Dùng **user data** (script cài agent + fetch-config từ Parameter Store lúc boot), hoặc tốt hơn là **SSM State Manager association**. Tiện hơn bake AMI vì: sửa config chỉ cần đổi parameter / document, không phải tạo lại AMI; áp tự động lên cả instance mới scale-out; thao tác vận hành thấp nhất.
</details>

---

## Nguồn
- Kiến thức nền về quan hệ AMI - ASG - agent (ổn định, không cần tra docs).
- Tham chiếu câu hỏi: [EC2 Auto Scaling FAQs](https://aws.amazon.com/ec2/autoscaling/faqs/)
