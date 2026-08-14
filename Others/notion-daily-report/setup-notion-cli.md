# Notion CLI + Task Database Setup

## 1. Cài Notion CLI

```bash
curl -fsSL https://ntn.dev | bash
```

Verify:
```bash
ntn --version
```

## 2. Login

```bash
ntn login
```

Browser mở → Authorize → Done. Credentials lưu trong keychain.

Kiểm tra:
```bash
ntn api v1/users/me
```

## 3. Lấy Parent Page ID

Tạo 1 page trống trong Notion (ví dụ tên "Task Management"), mở nó trên web.

URL sẽ dạng:
```
https://www.notion.so/Task-Management-abc123def456...
                                     ^^^^^^^^^^^^^^^
```

Copy phần ID (32 ký tự sau cùng, bỏ dấu `-`). Đó là `PAGE_ID`.

## 4. Tạo Task Database

```bash
ntn api v1/databases < Others/notion-daily-report/create-task-db.json
```

**Trước khi chạy**: mở file `create-task-db.json` và thay `YOUR_PAGE_ID` bằng Page ID thật.

Output trả về JSON — copy giá trị `"id"` → đó là **Database ID** của bạn.

## 5. Test tạo task

```bash
ntn api v1/pages \
  parent[database_id]=YOUR_DB_ID \
  properties[Name][title][0][text][content]="Test task từ CLI" \
  properties[Status][status][name]="Not Started" \
  properties[Priority][select][name]=Medium \
  'properties[Due Date][date][start]'=2026-08-13 \
  properties[Tags][multi_select][0][name]=Learning
```

Mở Notion → check database → task mới xuất hiện.

## 6. Kết nối Google Apps Script

Vào Google Apps Script project → Project Settings → Script Properties:

| Property | Value |
|----------|-------|
| `NOTION_API_KEY` | Lấy từ https://www.notion.so/my-integrations (tạo integration, copy secret) |
| `NOTION_DATABASE_ID` | Database ID từ bước 4 |
| `EMAIL_TO` | Email nhận báo cáo |

**Lưu ý**: `ntn login` dùng OAuth (user token), còn Google Apps Script cần **Integration token** (bắt đầu bằng `ntn_...`). Đây là 2 auth khác nhau:
- CLI (`ntn`): login bằng browser OAuth → dùng trực tiếp
- Apps Script: cần tạo Internal Integration tại https://www.notion.so/my-integrations → share DB cho integration

## 7. Share Database cho Integration

1. Mở database "Tasks" trong Notion
2. Click `⋮` → Connections → Connect to → chọn integration bạn vừa tạo
3. Confirm

Xong! Apps Script giờ có quyền đọc database.

## Tóm tắt flow

```
ntn api v1/pages ... ──▶ Notion Task DB ◀── Google Apps Script (đọc mỗi sáng)
                              │                        │
                              │                        └──▶ 📧 Email báo cáo
                              │
                         Notion UI (Board/Calendar view)
```
