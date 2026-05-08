# Google Apps Script Backend

## 1. Tạo Google Sheet

- Tạo một Google Sheet mới để nhận dữ liệu khảo sát
- Copy `Spreadsheet ID` từ URL:
  - `https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit`

## 2. Tạo Apps Script

- Vào [script.new](https://script.new)
- Tạo project mới
- Copy nội dung từ `Code.gs` vào file `Code.gs`
- Thay:

```javascript
const SPREADSHEET_ID = 'PUT_YOUR_SPREADSHEET_ID_HERE';
```

bằng Spreadsheet ID thật

## 3. Deploy Web App

- Chọn `Deploy` → `New deployment`
- Type: `Web app`
- Execute as: `Me`
- Who has access: `Anyone`

Sau khi deploy, copy URL dạng:

```text
https://script.google.com/macros/s/XXXXXXXXXXXX/exec
```

## 4. Dán URL vào form frontend

Mở file:

- `training/course-feedback/index.qmd`

Tìm:

```javascript
const SCRIPT_URL = "YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL";
```

và thay bằng URL `.../exec` vừa deploy.

## 5. Render lại site

```bash
quarto render
```

## Dữ liệu được lưu

Sheet `course_feedback` sẽ tự tạo header:

- `submitted_at`
- `course_slug`
- `course_name`
- `content_rating`
- `instructor_rating`
- `strengths`
- `improvements`
- `source_page`
- `user_agent`
