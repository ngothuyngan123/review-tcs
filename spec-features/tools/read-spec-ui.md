---
name: read-spec-ui
description: "Đọc spec UI cho frontend developer — màn hình, form fields, user flows, shared components"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc spec UI — dành cho Frontend Developer

## Mục đích
Đọc và trình bày thông tin UI/UX cho frontend developer: màn hình, layout, form fields, bảng dữ liệu, user flows, và shared components.

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Text UI tiếng Nhật giữ nguyên trong 「」 — frontend dev cần biết chính xác text hiển thị
- Tên file, ID, class/method giữ nguyên tiếng Anh

## Các bước thực hiện

### Bước 1: Resolve tính năng

*(Cùng logic với read-spec.md — Bước 1 & 2)*

1. Xác định SPEC_BASE_PATH
2. Resolve `{feature}` → `{portal}` + folder path
3. Nếu không tìm thấy → báo lỗi

### Bước 2: Đọc UI Spec

Đọc file `{SPEC_BASE_PATH}/{portal}/{feature}/ui/ui-spec.md`.

Nếu file không tồn tại → thông báo "UI spec chưa có cho tính năng này" + liệt kê files có sẵn.

### Bước 3: Bổ sung từ Feature Spec

Đọc thêm từ `{SPEC_BASE_PATH}/{portal}/{feature}/feature-spec.md` (nếu tồn tại):
- **Mục "Các màn hình + Luồng xử lý end-to-end"** (thường là §2) — chứa luồng tích hợp UI + backend
- **Mục "Bảng tham chiếu Enum / Status"** (thường là §10 nếu có) — giá trị enum cho dropdowns, badges, radio buttons

### Bước 4: Kiểm tra Shared Components

Quét nội dung ui-spec.md và feature-spec.md tìm tham chiếu `SC-XXX`:
1. Nếu tìm thấy → đọc `{SPEC_BASE_PATH}/shared/registry.md` để lấy tên + mô tả component
2. Check `{SPEC_BASE_PATH}/shared/{component-name}/shared-spec.md` tồn tại không
3. Nếu shared spec tồn tại → đọc và tóm tắt phần liên quan

### Bước 5: Trình bày theo format frontend-friendly

Trình bày **theo từng màn hình (screen)**, mỗi screen bao gồm:

#### A. Thông tin màn hình
- Mã SCR-XXX, tên VN, tên JP
- URL pattern
- Layout tổng thể (mô tả vùng: sidebar, header, content, modal overlay...)

#### B. Form Fields (nếu có)
Bảng:
| # | Label JP | Loại input | Bắt buộc? | Mặc định | Validation | Ghi chú |
|---|---------|-----------|----------|---------|-----------|---------|

#### C. Bảng dữ liệu (nếu có)
Bảng:
| # | Header JP | Kiểu dữ liệu | Sortable? | Ghi chú |
|---|----------|-------------|----------|---------|

#### D. Actions / Buttons
Bảng:
| Element | Text JP | Loại | Hành vi | Xác nhận? |
|---------|---------|------|---------|----------|

#### E. User Flows
Liệt kê từng luồng người dùng liên quan đến màn hình:
- Mô tả step-by-step từ **góc nhìn user** (không đi sâu vào backend)
- VD: "User click「新規作成」→ modal hiện → nhập tên → click「保存」→ danh sách reload"

### Bước 6: Tổng hợp Enum/Status Values

Nếu feature-spec có bảng enum → trích xuất:

| Giá trị hiển thị JP | Màu badge | Ý nghĩa | Giá trị DB (nếu biết) |
|---------------------|----------|---------|----------------------|

### Bước 7: Tổng hợp Shared Components

Liệt kê shared components đã phát hiện:

| Mã SC | Tên | Vị trí sử dụng | Có shared spec? |
|-------|-----|----------------|-----------------|

Nếu shared spec có → tóm tắt: component có những gì, cách tích hợp.

## Output format

```
## FA-XXX {Tên}「{Tên JP}」 — UI Spec cho Frontend Dev

### Tổng quan
- Portal: Admin | URL: /basic/xxx
- Tổng số màn hình: N
- Shared components: SC-001, SC-004

---

### SCR-XXX-01: {Tên màn hình}「{Tên JP}」
**URL**: /basic/xxx
**Layout**: {Mô tả layout}

#### Form Fields
| # | Label JP | Loại input | Bắt buộc? | Mặc định | Validation | Ghi chú |
...

#### Bảng dữ liệu
| # | Header JP | Kiểu dữ liệu | Sortable? | Ghi chú |
...

#### Actions
| Element | Text JP | Loại | Hành vi |
...

#### User Flows
1. **Load trang**: User truy cập URL → trang hiển thị danh sách...
2. **Tạo mới**: User click「新規作成」→ modal hiện → ...
3. **Xoá**: User chọn checkbox → click「一括削除」→ confirm → ...

---

### SCR-XXX-02: ...
(cùng format)

---

### Enum / Status Values
| Giá trị JP | Màu | Ý nghĩa |
...

### Shared Components
| SC | Tên | Vị trí | Shared spec? |
...
```
