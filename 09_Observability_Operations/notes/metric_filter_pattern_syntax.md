# Cú Pháp Filter Pattern Trong Metric Filter (Metric Filter Pattern Syntax)
**Chủ đề (Topic):** Observability & Operations
**Dịch vụ (Service):** Amazon CloudWatch Logs
**Ngữ cảnh (Context):** Lab d1-02, màn hình "Create metric filter" -> "Define pattern"

---

## 0. Metric Filter Là Gì Và Khác Gì Logs Insights

**Metric filter** quét log event khi chúng được đẩy vào CloudWatch Logs, khớp theo pattern bạn định nghĩa, rồi **cộng một giá trị số vào một CloudWatch metric mỗi khi tìm thấy dòng khớp**. Ví dụ: đếm số lần xuất hiện từ `ERROR`, hoặc đếm số HTTP 503.

> [!IMPORTANT]
> Metric filter KHÁC với CloudWatch Logs Insights. Logs Insights là ngôn ngữ truy vấn để phân tích log có sẵn. Metric filter chạy **tại thời điểm log được ingest** và biến dòng khớp thành một metric time-series để vẽ chart và tạo alarm. Cùng một filter pattern syntax này cũng dùng cho subscription filters, filter log events và Live Tail.

Filter pattern phân biệt chữ hoa chữ thường (**case sensitive**). Một log group tạo metric filter được tối đa **5 filter pattern chứa regex**.

---

## 1. Bốn Dạng Match (ứng với dropdown gợi ý trên Console)

Màn hình "Create filter pattern" gợi ý sẵn các mẫu. Chúng rơi vào 4 nhóm:

| Nhóm trên Console | Dạng log | Cú pháp bao ngoài |
| :--- | :--- | :--- |
| Match log events that contain a term | Log phi cấu trúc (text thô) | Không bao, viết thẳng term |
| Match log events with 400 level HTTP response | Log phân tách bằng khoảng trắng (access log) | Dấu ngoặc vuông `[ ... ]` |
| Match JSON log events | Log dạng JSON | Dấu ngoặc nhọn `{ ... }` |
| (regex, lồng vào 3 dạng trên) | Mọi dạng | Dấu phần trăm `% ... %` |

---

## 2. Dạng 1: Match Term Trong Log Phi Cấu Trúc (Unstructured)

Dùng khi log là text thô, không có cấu trúc field rõ ràng. Viết thẳng term, không bao ngoặc.

| Mục tiêu | Pattern | Ghi chú |
| :--- | :--- | :--- |
| Chứa 1 term | `ERROR` | Khớp mọi dòng có chữ `ERROR` |
| Chứa NHIỀU term (AND) | `ERROR ARGUMENTS` | Phải có **cả hai** từ mới khớp |
| Term tùy chọn (OR) | `?ERROR ?ARGUMENTS` | Dấu `?` đặt trước mỗi term = khớp term này **hoặc** term kia |
| Cụm từ chính xác | `"INTERNAL SERVER ERROR"` | Bao `" "` để khớp đúng nguyên cụm |
| Include và exclude | `ERROR -ARGUMENTS` | Có `ERROR` nhưng KHÔNG có `ARGUMENTS` (dấu `-` để loại) |
| Khớp tất cả | `" "` | Hai dấu nháy kép ôm một khoảng trắng = match mọi dòng |

> [!NOTE]
> Cụm từ hoặc term chứa ký tự không phải chữ/số phải bao trong dấu nháy kép `" "`.
> Dấu `?` KHÔNG kết hợp được với include/exclude. Nếu trộn `?` với pattern khác, mọi term có `?` bị bỏ qua.

---

## 3. Dạng 2: Match Trong Log Phân Tách Bằng Khoảng Trắng (Space-Delimited)

Đây là dạng dùng cho NGINX/Apache **access log**. Bao toàn bộ trong `[ ]`, liệt kê tên field theo đúng thứ tự, phân tách bằng dấu phẩy.

### 3.1 Cách field được tách
CloudWatch tách log theo khoảng trắng, NHƯNG:
- Phần trong `[...]` (ví dụ timestamp) được coi là **một field**.
- Phần trong `"..."` (ví dụ request line) được coi là **một field**.

Với dòng NGINX combined log:
```
192.168.1.10 - - [27/Oct/2026:11:00:00 +0700] "GET /api HTTP/1.1" 503 1234 "ref" "agent"
```

| Vị trí | Giá trị | Tên gán trong pattern |
| :--- | :--- | :--- |
| 1 | `192.168.1.10` | `ip` |
| 2 | `-` | `identity` |
| 3 | `-` | `user` |
| 4 | `[27/Oct/2026:11:00:00 +0700]` | `timestamp` |
| 5 | `"GET /api HTTP/1.1"` | `request` |
| 6 | `503` | `status_code` |
| 7 | `1234` | `bytes` |

Tên field đặt tùy ý, chỉ **vị trí** mới quan trọng.

### 3.2 Các điều kiện trên field
| Mục tiêu | Pattern |
| :--- | :--- |
| Bắt đúng HTTP 503 | `[ip, identity, user, timestamp, request, status_code=503, bytes]` |
| Bắt cả dải 5xx (wildcard) | `[ip, identity, user, timestamp, request, status_code=5*, bytes]` |
| Bắt cả dải 4xx (wildcard) | `[host, logName, user, timestamp, request, statusCode=4*, size]` |
| So sánh số | `[..., bytes>1000]` dùng được `=`, `!=`, `<`, `>`, `<=`, `>=` |
| Kết hợp AND/OR | `[w1=val1 && w2=val2]` hoặc `[w1=val1 || w2=val2]` |

---

## 4. Dạng 3: Match Trong Log JSON

Dùng khi log là JSON (ví dụ app log có cấu trúc). Bao toàn bộ trong `{ }`.

### 4.1 Cú pháp
```
{ PropertySelector Operator Value }
```
- **Property selector**: bắt đầu bằng `$.` rồi tới đường dẫn khóa. Ví dụ `$.statusCode`, `$.user.id`. Mảng dùng chỉ số 0-based trong `[]`, ví dụ `$.items[0]`.
- **Operator**: chuỗi dùng `=`, `!=`; số dùng `=`, `!=`, `<`, `>`, `<=`, `>=`.
- **Value**: chuỗi bao `" "`, có thể dùng `*` làm wildcard; hoặc số.

### 4.2 Ví dụ
| Mục tiêu | Pattern |
| :--- | :--- |
| Khớp chuỗi | `{ $.eventType = "UpdateTrail" }` |
| Khớp errorCode | `{ $.errorCode = "AccessDenied" }` |
| So sánh số | `{ $.latency > 1000 }` |
| Wildcard chuỗi | `{ $.requestURL = "https://*" }` |
| Kết hợp AND | `{ ($.a = "x") && ($.b > 5) }` |
| Kết hợp OR | `{ ($.a = "x") || ($.b = "y") }` |

> [!NOTE]
> Chỉ dùng được tối đa **1 wildcard selector** trong một property selector.

---

## 5. Dạng 4: Regex `% ... %` (lồng vào mọi dạng trên)

Regex không phải một dạng riêng, mà là công cụ bọc trong `% %`, nhúng được vào term thường, vào field của space-delimited, và vào value của JSON.

### 5.1 Ví dụ nhúng regex
| Ngữ cảnh | Pattern |
| :--- | :--- |
| Term phi cấu trúc | `%AUTHORIZED%` (khớp cả UNAUTHORIZED vì chứa chuỗi này) |
| Space-delimited, bắt 4xx | `[uuid, level, timestamp, statusCode=%4[0-9]{2}%]` |
| JSON value | `{ $.statusCode = %4[0-9]{2}% }` |

### 5.2 Giải mã `%4[0-9]{2}%`
| Phần | Nghĩa |
| :--- | :--- |
| `4` | Ký tự đầu đúng là số `4` |
| `[0-9]` | Một chữ số bất kỳ từ 0 đến 9 |
| `{2}` | Lặp cái ngay trước (`[0-9]`) đúng 2 lần |

Ghép lại: `4` + đúng 2 chữ số = `400` tới `499`. Bắt cả dải 4xx, giống `4*` nhưng CHẶT hơn (ép đúng 3 ký tự số).

### 5.3 Toán tử regex được hỗ trợ
| Toán tử | Nghĩa | Ví dụ |
| :--- | :--- | :--- |
| `^` | Neo đầu chuỗi | `%^[hc]at%` khớp "hat", "cat" ở đầu |
| `$` | Neo cuối chuỗi | `%[hc]at$%` khớp "hat", "cat" ở cuối |
| `?` | 0 hoặc 1 lần | `%colou?r%` khớp "color" và "colour" |
| `[]` | Lớp ký tự | `%[a-z]%` một chữ thường bất kỳ |
| `{m,n}` | Lặp từ m tới n lần | `%a{3,5}%` khớp "aaa".."aaaaa" |
| `\|` | HOẶC (OR) | `%gray\|grey%` khớp "gray" hoặc "grey" |
| `\` | Escape, lấy nghĩa đen | `%10\.10\.0\.1%` khớp đúng IP 10.10.0.1 |
| `*` | 0 hoặc nhiều lần | `%ab*c%` khớp "ac", "abc", "abbbc" |
| `+` | 1 hoặc nhiều lần | `%ab+c%` khớp "abc", "abbc", KHÔNG khớp "ac" |
| `.` | Một ký tự bất kỳ | `%.at%` khớp "hat", "cat", "4at" |
| `\d` `\D` | Số / không phải số | `%\d%` = `%[0-9]%` |
| `\s` `\S` | Khoảng trắng / không phải | tab, space, newline |
| `\w` `\W` | Chữ-số-gạch dưới / không | `%\w%` = `%[a-zA-Z_0-9]%` |
| `\xhh` | Ký tự ASCII theo hex | `%\x3A%` khớp `:` |

> [!WARNING]
> Dấu ngoặc tròn `(` `)` KHÔNG được hỗ trợ trong regex của filter pattern, không tạo được subpattern. Ký tự đa byte (multi-byte) không hỗ trợ.
> Khi khớp IP, PHẢI escape dấu `.` thành `\.`, nếu không `%10.10.0.1%` có thể khớp nhầm "10010,051" vì `.` khớp ký tự bất kỳ.

### 5.4 Giới hạn regex (quota)
- Tối đa **5 filter pattern chứa regex** cho mỗi log group (khi tạo metric filter hoặc subscription filter).
- Tối đa **2 regex trong một filter pattern** khi dùng với delimited hoặc JSON.

---

## 6. Wildcard `*` Vs Regex `% %` (dễ nhầm)

| | Wildcard `*` | Regex `% %` |
| :--- | :--- | :--- |
| Viết | `statusCode=4*` | `statusCode=%4[0-9]{2}%` |
| Nghĩa | Bắt đầu bằng 4, theo sau là bất kỳ gì | `4` + đúng 2 chữ số |
| Độ chặt | Lỏng (khớp cả `4`, `4abc`) | Chặt (đúng 3 ký tự số) |
| Khi nào dùng | Điều kiện đơn giản | Điều kiện phức tạp |

Bảng mục tiêu theo HTTP status:

| Mục tiêu | Pattern cho field status |
| :--- | :--- |
| Đúng 503 | `status_code=503` |
| Cả 5xx | `status_code=5*` hoặc `status_code=%5[0-9]{2}%` |
| Chỉ 500,502,503,504 | `status_code=%50[0-4]%` |
| 4xx và 5xx | `status_code=%[45][0-9]{2}%` |

Dòng cuối là chỗ regex thắng hẳn: `[45]` nghĩa là ký tự đầu là 4 hoặc 5, không wildcard nào viết gọn được.

---

## 7. Chốt Lại Cho Lab d1-02 (bắt HTTP 503)

Filter pattern cần gõ ở Step 1 (Define pattern):
```
[ip, identity, user, timestamp, request, status_code=503, bytes]
```

Step 2 (Assign metric) nên đặt:
- **Metric namespace**: ví dụ `TD/NGINX`
- **Metric name**: ví dụ `Http503Count`
- **Metric value**: `1` (mỗi dòng khớp đếm 1)
- **Default value**: `0` (để metric luôn có điểm 0 khi không có 503, tránh alarm rơi vào `INSUFFICIENT_DATA`)

> **Memory tip (SOA-C03):** nhớ 3 ký hiệu bao ngoài để nhận dạng nhanh dạng match:
> - Không bao = term trong log phi cấu trúc.
> - `[ ]` = space-delimited (access log).
> - `{ }` = JSON.
> - `% %` = regex (lồng vào 3 dạng trên).

---

## Nguồn (Sources)
- [Filter pattern syntax for metric filters, subscription filters, filter log events, and Live Tail](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html)
- [Filter pattern syntax for metric filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html)
