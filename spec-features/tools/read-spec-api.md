---
name: read-spec-api
description: "Đọc spec API cho backend developer — endpoints, params, responses, validation, errors"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc spec API — dành cho Backend API Developer

## Mục đích
Đọc và trình bày thông tin API endpoints: HTTP method, URI, request params, response format, validation rules, error responses, middleware.

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Text UI tiếng Nhật giữ nguyên trong 「」
- Tên controller, method, route, param giữ nguyên tiếng Anh

## Các bước thực hiện

### Bước 1: Resolve tính năng

*(Cùng logic với read-spec.md — Bước 1 & 2)*

1. Xác định SPEC_BASE_PATH
2. Resolve `{feature}` → `{portal}` + folder path
3. Nếu không tìm thấy → báo lỗi

### Bước 2: Đọc API Spec

Đọc file `{SPEC_BASE_PATH}/{portal}/{feature}/web/api-spec.md`.

Nếu file không tồn tại → thông báo "API spec chưa có cho tính năng này" + liệt kê files có sẵn.

### Bước 3: Trình bày thông tin API

#### A. Bảng tổng hợp Endpoints

Trích xuất bảng tổng hợp (thường ở đầu file):

| EP | Method | URI | Controller@Action | Middleware | Mô tả |
|----|--------|-----|-------------------|-----------|-------|

#### B. Chi tiết từng Endpoint

Với mỗi endpoint, trích xuất:

1. **Thông tin cơ bản**: EP-XX, Method, URI, Controller@Action, Middleware
2. **Liên kết UI**: Gọi từ màn hình nào (SCR-XXX), khi user thực hiện action gì
3. **Request Parameters**:
   | Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
   |-------|--------|------|----------|-------|-----------|
4. **Request mẫu** (JSON nếu có)
5. **Response mẫu** (JSON — thành công)
6. **Response lỗi**: HTTP code, điều kiện, response body / thông báo JP
7. **Lưu ý đặc biệt**: Rate limit, file upload, pagination, etc.

#### C. Thông tin bổ sung

- **Middleware chung**: Authentication, authorization model, CSRF
- **Dual-flow** (nếu có): Liệt kê endpoints Legacy vs V2, ghi chú flow nào đang active
- **Endpoints chia sẻ**: Nếu có endpoints thuộc controller/feature khác (VD: FilterController dùng chung cho nhiều features)

### Bước 4: Highlight patterns quan trọng

Tìm và highlight:
- Endpoints dùng AJAX (thường prefix `/ajax/`)
- Endpoints có file upload
- Endpoints có pagination (offset/limit hoặc page)
- Endpoints có validation phức tạp (multiple rules)
- Endpoints modify nhiều bảng DB (side effects)

## Output format

```
## FA-XXX {Tên}「{Tên JP}」 — API Spec cho Backend Dev

### Tổng hợp Endpoints ({N} endpoints)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-01 | GET | /basic/xxx | XxxController@index | Trang danh sách |
| EP-02 | POST | /ajax/v2/xxx/create | XxxController@ajaxCreate | Tạo mới (AJAX) |
...

### Middleware
- Auth: {mô tả}
- CSRF: {có/không}
- Khác: {throttle, etc.}

---

### EP-01: GET /basic/xxx
**Controller**: `Namespace\XxxController@index`
**Middleware**: auth, verified
**Liên kết UI**: SCR-XXX-01 — load trang danh sách
**Mô tả**: {Mô tả chức năng}

#### Request
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
...

#### Response (thành công)
```json
{...}
```

#### Errors
| HTTP | Điều kiện | Thông báo |
...

---

### EP-02: POST /ajax/v2/xxx/create
...
```
