# Serverless Patterns Workshop - Q&A

> **Workshop:** https://catalog.workshops.aws/workshops/76bc5278-3f38-46e8-b306-f0bfda551f5a/en-US  
> **Khóa học:** AWS Lambda Foundations (W3_Data/AWS_Lambda_Foundations)  
> Trả lời từng câu hỏi bên dưới. Sau khi bạn trả lời, mình sẽ phản hồi đúng/sai và giải thích thêm.

---

## Module 1 - Intro to Serverless

> 📚 *Mapping: Introduction to Serverless + How AWS Lambda Works*

**Q1.** Trong workshop, DynamoDB table được tạo với tên gì, và partition key là gì (tên + kiểu dữ liệu)?

**Q2.** Khi tạo Lambda function đầu tiên (`first-function`), runtime nào được chọn?

**Q3.** Trong function mặc định của Lambda, hai tham số của `lambda_handler` là gì? Mỗi tham số chứa loại thông tin gì?

**Q4.** Trong Function Logs sau khi test, có 3 dòng log chính: START, END, REPORT. `Init Duration` trong REPORT có nghĩa là gì? Tại sao nó chỉ xuất hiện ở lần chạy đầu tiên?

**Q5.** Khi Lambda function `m1-add-sample-data` được test lần đầu (chưa có permission), kết quả là gì? Tại sao?

**Q6.** Để Lambda function có thể đọc/ghi DynamoDB, bạn cần thêm policy gì vào Execution Role? Tại sao trong production không nên dùng policy này — và nguyên tắc nào nên áp dụng thay thế?

**Q7.** Trong code Python của `m1-add-sample-data`, thư viện `boto3` dùng để làm gì? `uuid.uuid4().hex` được dùng để tạo ra giá trị gì, và tại sao DynamoDB không dùng auto-increment như SQL?

**Q8.** Sau khi clean up Module 1, bạn cần xóa resources ở những service nào (kể đủ 4)?

---

## Module 2 - Synchronous Invocation

> 📚 *Mapping: How AWS Lambda Works → Synchronous invocation*

**Q9.** Synchronous invocation trong Lambda nghĩa là gì? Khi nào thì caller nhận được response? Nếu function lỗi, có built-in retry không?

**Q10.** API Gateway kết hợp với Lambda theo mô hình synchronous. Điều gì xảy ra nếu Lambda function vượt quá timeout? Timeout tối đa của Lambda là bao nhiêu?

**Q11.** Kể đủ 6 AWS service invoke Lambda theo kiểu **synchronous** (theo khóa học Lambda Foundations).

---

## Module 3 - Synchronous + Idempotence

> 📚 *Mapping: Authoring AWS Lambda Functions → Design best practices*

**Q12.** Idempotence là gì? Cho ví dụ về một operation **idempotent** và một operation **không idempotent** trong context của API.

**Q13.** Tại sao idempotence quan trọng trong serverless architecture, đặc biệt khi có retry logic? Liên hệ với error behavior của từng invocation model.

**Q14.** Một cách phổ biến để implement idempotency trong Lambda + DynamoDB là gì? (Gợi ý: liên quan đến `_id` trong workshop)

---

## Module 4 - Asynchronous Invocation

> 📚 *Mapping: How AWS Lambda Works → Asynchronous invocation + Destinations*

**Q15.** Asynchronous invocation khác synchronous như thế nào? Caller có chờ response không? Có bao nhiêu lần retry built-in?

**Q16.** Khi Lambda được invoke asynchronously, event được đưa vào đâu trước khi Lambda xử lý?

**Q17.** **Destinations** trong async invocation là gì? Bạn có thể cấu hình destination cho trường hợp nào? Điều này khác Dead Letter Queue (DLQ) như thế nào?

**Q18.** Kể đủ 3 AWS service invoke Lambda theo kiểu **asynchronous** (theo khóa học Lambda Foundations).

---

## Module 5 - Polling (Event Source Mapping)

> 📚 *Mapping: How AWS Lambda Works → Polling invocation + Event Source Mapping*

**Q19.** Polling invocation (Event Source Mapping) là gì? Lambda tự poll hay AWS poll thay cho Lambda? Retry behavior của model này như thế nào?

**Q20.** Kể đủ 6 AWS service mà Lambda có thể đọc events thông qua **Event Source Mapping** (theo khóa học Lambda Foundations).

**Q21.** Trong SQS + Lambda integration, `batch size` có nghĩa là gì? Điều gì xảy ra nếu Lambda function fail khi xử lý một batch?

---

## Module 6 - Streaming Data

> 📚 *Mapping: How AWS Lambda Works → Polling invocation (Kinesis, DynamoDB Streams)*

**Q22.** Khi dùng Lambda với Kinesis Data Streams, Lambda xử lý records theo thứ tự nào trong một shard? Tại sao điều này quan trọng?

**Q23.** `bisect_on_function_error` trong Lambda event source mapping với Kinesis có tác dụng gì? Nó giải quyết vấn đề gì?

**Q24.** Sự khác biệt chính giữa Kinesis Data Streams và SQS khi dùng làm trigger cho Lambda là gì? (Gợi ý: ordering, retention, consumer model)

---

## Tổng hợp - Lambda Configuration & Best Practices

> 📚 *Mapping: Configuring Your Lambda Functions + Authoring + Monitoring*

**Q25.** Lambda Execution Environment có 3 phase trong lifecycle. Kể tên và mô tả ngắn từng phase. Phase nào gây ra "cold start"?

**Q26.** Lambda có 3 loại concurrency. Kể tên và giải thích sự khác nhau giữa **Unreserved**, **Reserved**, và **Provisioned** concurrency.

**Q27.** Lambda tính phí dựa trên những yếu tố nào? Nếu bạn allocate 10 GB memory nhưng function chỉ dùng 2 GB, bạn bị charge bao nhiêu?

**Q28.** Kể 5 best practices khi **viết code** cho Lambda function (theo khóa học Lambda Foundations).

**Q29.** AWS SAM là gì? Nó liên quan đến CloudFormation như thế nào? Kể 3 lợi ích của AWS SAM so với viết CloudFormation template thuần.

**Q30.** Để monitor Lambda function, bạn có thể dùng những tool nào? Mỗi tool phù hợp với use case gì? (Kể ít nhất 3 tool)

---

## Bonus - Serverless Architecture Thinking

> 📚 *Mapping: Introduction to Serverless → Event-driven architectures*

**Q31.** Trong event-driven architecture, 3 thành phần chính là gì? Mô tả vai trò của từng thành phần.

**Q32.** Lambda function nên được thiết kế **stateless** — điều này có nghĩa là gì? Nếu cần lưu state, bạn có thể dùng những service nào và khi nào dùng cái nào?

**Q33.** Serverless có nghĩa là "không có server" không? Giải thích sự khác biệt thực sự giữa serverless và traditional server-based, dựa trên bảng so sánh trong khóa học.

**Q34.** Trong workshop này, kiến trúc tổng thể gồm những thành phần nào? Mô tả flow từ client đến database (theo diagram trong workshop).
