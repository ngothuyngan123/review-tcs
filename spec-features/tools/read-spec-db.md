---
name: read-spec-db
description: "Đọc spec database cho backend/DBA — tables, columns, relationships, enums, field traceability"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc spec Database — dành cho Backend / DBA

## Mục đích
Đọc và trình bày database mapping: bảng chính/phụ, cột, relationships, enums, field traceability (UI → API → DB).

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Tên bảng, cột, constraint, index giữ nguyên tiếng Anh từ schema
- Mô tả cột bằng tiếng Việt

## Các bước thực hiện

### Bước 1: Resolve tính năng

*(Cùng logic với read-spec.md — Bước 1 & 2)*

1. Xác định SPEC_BASE_PATH
2. Resolve `{feature}` → `{portal}` + folder path
3. Nếu không tìm thấy → báo lỗi

### Bước 2: Đọc DB Mapping

Đọc file `{SPEC_BASE_PATH}/{portal}/{feature}/db/db-mapping.md`.

Nếu file không tồn tại → thông báo "DB mapping chưa có" + liệt kê files có sẵn.

### Bước 3: Bổ sung từ Feature Spec

Đọc `{SPEC_BASE_PATH}/{portal}/{feature}/feature-spec.md` (nếu tồn tại):
- **Mục "Database Tables"** (thường §3) — overview bảng chính/phụ
- **Mục "Field Traceability Matrix"** (thường §4) — UI field → API param → DB column
- **Mục "Bảng tham chiếu Enum / Status"** (thường §10 nếu có) — giá trị enum trong DB

### Bước 4: Trình bày thông tin database

#### A. Tổng quan bảng

Phân loại bảng thành 2 nhóm:

**Bảng chính (Primary)** — bảng trực tiếp đọc/ghi bởi tính năng:
| Bảng | Model | Vai trò | Đọc/Ghi | Confidence |
|------|-------|---------|---------|-----------|

**Bảng phụ (Secondary)** — FK, config, logs, chia sẻ:
| Bảng | Vai trò | Đọc/Ghi | Confidence |
|------|---------|---------|-----------|

#### B. Chi tiết từng bảng chính

Với mỗi bảng chính, trình bày:

1. **Tên bảng** + Model tương ứng
2. **Cột**:
   | Cột | Kiểu | Nullable | Default | Mô tả |
   |-----|------|---------|---------|-------|
3. **Primary Key**, **Foreign Keys**
4. **Indexes** (nếu biết)
5. **Relationships** với bảng khác:
   - Loại: 1-1, 1-N, N-N
   - FK column
   - Bảng liên quan
6. **Ghi chú**: Soft delete? Sharding? Partitioning?

#### C. Relationships Diagram

Vẽ sơ đồ quan hệ dạng text (hoặc Mermaid nếu feature-spec có):

```
tags (1) ──→ (N) tag_line_user ──→ (1) line_user
tags (N) ──→ (1) category
tags (1) ──→ (1) t_actions ──→ (N) t_actions_detail
```

#### D. Enum / Status Values

Trích xuất giá trị enum cho từng cột có kiểu enum hoặc status:

| Bảng.Cột | Giá trị DB | Hiển thị JP | Ý nghĩa VN |
|----------|-----------|------------|------------|

#### E. Field Traceability (UI → API → DB)

Nếu feature-spec có Field Traceability Matrix, trình bày:

| UI Label JP | API Param | DB Table.Column | Kiểu |
|------------|----------|----------------|------|
| 「タグ名」 | name | tags.name | varchar(50) |

#### F. Shared Tables

Bảng dùng chung giữa features:
| Bảng | Dùng bởi features | Cách phân biệt |
|------|-------------------|---------------|
| category | FA-012 (tags), FA-003 (auto-reply) | `kind=0` (tag folders), `kind=1` (reply folders) |
| t_actions | FA-012, FA-003, FA-001 | `action_type` phân biệt context |
| filters_v2 | FA-003, FA-002, FA-008 | `parent_type` + `parent_id` |

#### G. Confidence Notes

Đánh dấu thông tin DB theo mức tin cậy:
- **Cao**: Đọc từ DB schema (CREATE TABLE)
- **Trung bình**: Suy luận từ code (model relationships, query trong controller)
- **Thấp**: Phỏng đoán từ tên cột hoặc data mẫu

## Output format

```
## FA-XXX {Tên}「{Tên JP}」 — DB Spec

### Tổng quan
- Bảng chính: N bảng
- Bảng phụ: M bảng

### Bảng chính
| Bảng | Model | Vai trò | Đọc/Ghi |
...

### Bảng phụ
| Bảng | Vai trò | Đọc/Ghi |
...

---

### Chi tiết: tags
**Model**: Tags | **Vai trò**: Bảng chính lưu tag

| Cột | Kiểu | Nullable | Default | Mô tả |
|-----|------|---------|---------|-------|
| id | bigint unsigned | NO | auto | PK |
| bot_id | int | NO | | FK → bots.id |
| name | varchar(50) | NO | | Tên tag |
...

**Relationships**:
- tags (1) → (N) tag_line_user (FK: tag_id)
- tags (N) → (1) category (FK: category_id)

---

### Relationships Diagram
```
tags ──→ tag_line_user ──→ line_user
tags ──→ category
tags ──→ t_actions ──→ t_actions_detail
```

### Enum / Status
| Bảng.Cột | DB Value | JP Display | Ý nghĩa |
...

### Field Traceability
| UI Label | API Param | DB Column |
...

### Shared Tables
| Bảng | Dùng bởi | Phân biệt bằng |
...
```
