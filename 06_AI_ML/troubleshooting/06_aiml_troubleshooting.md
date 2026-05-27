# Topic 06: AI/ML Troubleshooting — Khắc Phục Sự Cố Bedrock API Throttling & RAG Knowledge Base

## 📌 Tổng quan cốt lõi (Core Concepts)
- **Bedrock API Quotas:** Amazon Bedrock áp dụng giới hạn nghiêm ngặt về số lượng API Requests per Minute (RPM) và Tokens per Minute (TPM) tùy thuộc vào Model ID được sử dụng.
- **RAG & Knowledge Base Performance:** Chất lượng câu trả lời của mô hình trong kiến trúc RAG (Retrieval-Augmented Generation) phụ thuộc trực tiếp vào phương pháp cắt nhỏ văn bản (Chunking Strategy) và độ tương thích của Embedding Model trong Vector Database.

---

## 📐 Sơ đồ Hoạt động & Kiến trúc (Architectural Flows)

### Sơ đồ luồng xử lý RAG & Điểm Nghẽn Chất Lượng Dữ Liệu
```
[Tài liệu thô: PDF/Word]
         │
         ▼
 1. Chunking Strategy? (Cắt nhỏ văn bản)
         ├── Default Chunking (300 tokens) ──► [Có thể làm mất ngữ cảnh giữa các trang]
         └── Semantic/Hierarchical Chunking ─► [Giữ nguyên cấu trúc luận điểm - Khuyên dùng]
         │
         ▼
 2. Embedding Model ? (Chuyển đổi sang vector)
         ├── Model A (Cohort/Titan) ───────► [Lưu vào Vector DB - OpenSearch Serverless]
         └── Yêu cầu: Embedding Model lúc truy vấn và lúc lưu trữ bắt buộc phải đồng nhất.
         │
         ▼
[User Query] ──► [KBS Retrieval] ──► [Prompt Context] ──► [Bedrock LLM] ──► [Response]
```

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

| Tiêu chí | Provisioned Throughput (Bedrock) | On-Demand (Bedrock) |
|---|---|---|
| **Cơ chế hoạt động** | Thuê riêng một lượng tài nguyên xử lý (Model Units) dành riêng cho doanh nghiệp của bạn. | Sử dụng chung hạ tầng chia sẻ (Shared resources), tính tiền theo lượng Token sử dụng. |
| **Tránh lỗi Throttling**| **Tuyệt đối** (Cam kết throughput ổn định, không bao giờ bị throttle). | **Dễ bị throttle** khi hệ thống có tải đột biến (Spike load). |
| **Giá cả** | Rất cao, phù hợp cho môi trường Production lớn, chạy 24/7. | Thấp, phù hợp cho môi trường Dev/Test hoặc ứng dụng có tải nhỏ. |

---

## 🛠️ DevOps Best Practices & Thực chiến

### 1. Bedrock API trả về lỗi `ThrottlingException`
*   **Nguyên nhân:** Lượng request đồng thời từ ứng dụng của bạn hoặc số lượng Token gửi đi vượt quá giới hạn **TPS (Transactions Per Second)** hoặc **TPM (Tokens Per Minute)** của tài khoản đối với model đó (ví dụ Claude 3 Opus/Sonnet).
*   **Cách kiểm tra bằng CloudWatch Metrics:**
    *   Theo dõi metric `InvocationThrottles` của Bedrock Service trong region đó.
*   **Giải pháp khắc phục và tối ưu hóa:**
    *   **Áp dụng cơ chế Exponential Backoff với Jitter (Phản xạ bắt buộc):** Trong mã nguồn ứng dụng Client, khi nhận mã lỗi `429 (Too Many Requests)` hoặc `ThrottlingException`, không được gửi lại request ngay lập tức mà phải đợi tăng dần theo lũy thừa kèm yếu tố ngẫu nhiên để tránh làm nghẽn thêm hệ thống.
        ```python
        import time
        import random
        
        def call_bedrock_with_retry(client, model_id, prompt):
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    response = client.invoke_model(modelId=model_id, body=prompt)
                    return response
                except client.exceptions.ThrottlingException:
                    if attempt == max_retries - 1:
                        raise
                    # Tính toán thời gian chờ lũy thừa với jitter
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
        ```
    *   **Sử dụng Bedrock Provisioned Throughput:** Dành cho môi trường Production để mua đứt băng thông (Model Units - MU).
    *   **Yêu cầu tăng Limit (Quota Increase):** Gửi Service Quota increase request trên AWS Console để nâng giới hạn RPM/TPM của Model.

### 2. Knowledge Base (RAG) không trả về kết quả đúng
*   **Nguyên nhân 1: Chunking Strategy sai (Lỗi phổ biến nhất):**
    *   Sử dụng mặc định **Default Chunking (300 tokens)** cắt ngang xương một bảng số liệu hoặc một đoạn phân tích kỹ thuật, làm đứt gãy ngữ cảnh của thông tin.
*   **Nguyên nhân 2: Khác biệt về Embedding Model:**
    *   Tài liệu được embed bằng model cũ (ví dụ Titan v1), nhưng ứng dụng RAG khi nhận câu hỏi của User lại dùng model mới (v2) để so sánh vector -> Khoảng cách vector bị lệch, dẫn đến tìm kiếm sai thông tin liên quan.
*   **Cách điều tra và tối ưu hóa chất lượng RAG:**
    *   *Kiểm tra độ chính xác bằng CLI (Retrieve API):*
        ```bash
        aws bedrock-agent-runtime retrieve \
          --knowledge-base-id KB01234567 \
          --retrieval-query "Làm cách nào để sửa lỗi SSH?"
        ```
        *(Xem các đoạn văn bản trả về trong list `retrievalResults` xem có chứa thông tin đúng không).*
    *   *Chiến lược sửa lỗi thực tế:*
        *   Chuyển sang **Hierarchical Chunking (Parent-Child)**: Cắt văn bản thành các chunk lớn (Parent) để giữ ngữ cảnh tổng quát, bên trong chứa các chunk nhỏ (Child) để tìm kiếm chính xác.
        *   Chuyển sang **Semantic Chunking**: Tự động phát hiện sự thay đổi chủ đề trong văn bản để cắt chunk thông minh thay vì cắt cứng theo số lượng ký tự.

---

## ⏱️ Khi nào nên chọn cái nào? (Decision Matrix)
- Chọn **Semantic Chunking** khi: Tài liệu có cấu trúc phức tạp, thay đổi luận điểm liên tục (ví dụ: Hợp đồng pháp lý, Báo cáo tài chính).
- Chọn **Fixed-size Chunking (với overlap)** khi: Tài liệu dạng phẳng, văn phong đồng nhất (ví dụ: Sách giáo khoa, Hướng dẫn sử dụng cơ bản).
- Chọn **Provisioned Throughput** khi: Ứng dụng AI yêu cầu độ trễ cực thấp (Low Latency) và cam kết chất lượng dịch vụ (SLA) nghiêm ngặt cho khách hàng doanh nghiệp.

---

## 📚 Nguồn Tham Khảo (References)
- *Tài liệu AWS chính thức:* 
  - [Quotas for Amazon Bedrock API operations](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html)
  - [Improve RAG performance using advanced chunking strategies in Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-chunking.html)
