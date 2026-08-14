# Notion Daily Task Report — Google Apps Script

Google Apps Script tự động đọc Notion Database mỗi ngày, filter tasks, và gửi email báo cáo.

## Flow

```
Notion DB ──(API)──▶ Google Apps Script ──(GmailApp)──▶ Email báo cáo
                         │
                         └── Time trigger (mỗi sáng)
```

## Setup (5 phút)

### 1. Tạo Notion Integration & lấy API Key

1. Vào https://www.notion.so/my-integrations
2. Click **"New integration"**
3. Đặt tên (ví dụ: `Daily Report Script`)
4. Capabilities: chỉ cần **Read content** — bỏ tích Insert/Update/Delete
5. Copy **Internal Integration Secret** (bắt đầu bằng `ntn_...`)

### 2. Share Database cho Integration

1. Mở Notion Database bạn dùng để quản lý tasks
2. Click **⋮** (menu) → **Connections** → **Connect to** → chọn integration vừa tạo
3. Lấy **Database ID** từ URL:
   ```
   https://www.notion.so/your-workspace/DATABASE_ID?v=...
                                         ^^^^^^^^^^^
   ```
   Database ID là chuỗi 32 ký tự (có dấu `-` hoặc không) nằm trước `?v=`

### 3. Tạo Google Apps Script Project

1. Vào https://script.google.com → **New Project**
2. Xóa code mặc định, paste toàn bộ nội dung file `Code.gs`
3. Đổi tên project: `Notion Daily Report`

### 4. Cấu hình Script Properties (bảo mật API keys)

1. Trong Apps Script editor: **Project Settings** (icon bánh răng bên trái)
2. Kéo xuống phần **Script Properties** → **Add script property**
3. Thêm 3 properties:

| Property | Value |
|----------|-------|
| `NOTION_API_KEY` | `ntn_xxxxxxxxxxxxxxxx` (từ bước 1) |
| `NOTION_DATABASE_ID` | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (từ bước 2) |
| `EMAIL_TO` | Email bạn muốn nhận báo cáo |

### 5. Chỉnh Property Names cho khớp Notion DB

Mở `Code.gs`, tìm phần `CONFIG` và chỉnh các giá trị cho đúng tên property trong Notion DB của bạn:

```javascript
PROP_STATUS: 'Status',       // Tên cột Status trong DB
PROP_TITLE: 'Name',         // Tên cột Title (thường là "Name")
PROP_DUE_DATE: 'Due Date',  // Tên cột ngày deadline
PROP_PRIORITY: 'Priority',  // Tên cột priority (bỏ qua nếu không có)
PROP_TAGS: 'Tags',          // Tên cột tags/categories

STATUS_DONE: 'Done',              // Giá trị status = hoàn thành
STATUS_IN_PROGRESS: 'In Progress',
STATUS_NOT_STARTED: 'Not Started',
```

### 6. Test thủ công

1. Chọn function `testReport` từ dropdown
2. Click **▶ Run**
3. Lần đầu sẽ yêu cầu **Authorization** — cho phép hết
4. Kiểm tra email — nếu nhận được báo cáo là OK

### 7. Setup Trigger tự động

1. Trong Apps Script: click icon ⏰ **Triggers** (menu trái)
2. **+ Add Trigger**:
   - Function: `sendDailyReport`
   - Event source: **Time-driven**
   - Type: **Day timer**
   - Time: chọn khung giờ (ví dụ 7:00 - 8:00 sáng)
3. Save

Done! Mỗi sáng bạn sẽ nhận email báo cáo tự động.

## Notion DB Schema khuyến nghị

Nếu bạn đang tạo DB mới, đây là schema tối thiểu:

| Property | Type | Values |
|----------|------|--------|
| Name | Title | — |
| Status | Status | Not Started, In Progress, Done |
| Due Date | Date | — |
| Priority | Select | Urgent, High, Medium, Low |
| Tags | Multi-select | (tùy: Work, Learning, Personal...) |

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|------|-------------|-----|
| `401 Unauthorized` | API key sai hoặc hết hạn | Kiểm tra lại Script Properties |
| `404 Not Found` | Database ID sai hoặc chưa share cho integration | Share lại DB cho integration |
| `400 validation_error` | Tên property không khớp | Kiểm tra tên chính xác trong Notion (case-sensitive) |
| Không nhận email | `EMAIL_TO` chưa set hoặc sai | Check Script Properties |
| `Exceeded maximum execution time` | DB quá lớn (>10,000 tasks) | Thêm filter cụ thể hơn trong query |

## Tùy chỉnh

- **Đổi giờ gửi**: Edit trigger trong Triggers panel
- **Thêm filter**: Sửa object `filter` trong `sendDailyReport()` theo [Notion filter syntax](https://developers.notion.com/reference/post-database-query-filter)
- **Đổi format email**: Sửa function `buildEmailHtml()`
- **Gửi cho nhiều người**: Đổi `EMAIL_TO` thành comma-separated: `a@x.com,b@x.com`
