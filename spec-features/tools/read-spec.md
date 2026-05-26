---
name: read-spec
description: "Đọc tổng quan spec của 1 tính năng LME — entry point cho mọi vai trò"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc tổng quan spec tính năng LME

## Mục đích
Đọc và trình bày tổng quan spec của 1 tính năng LME. Đây là entry point — sau khi đọc, gợi ý skill chuyên sâu theo vai trò.

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Text UI tiếng Nhật giữ nguyên trong 「」
- Tên file, ID, tên bảng/cột/class/method giữ nguyên tiếng Anh

## Các bước thực hiện

### Bước 1: Xác định SPEC_BASE_PATH

Tìm thư mục chứa specs theo thứ tự:
1. Nếu CLAUDE.md của project có khai báo `SPEC_BASE_PATH` → dùng giá trị đó
2. Nếu skill nằm trong `features/tools/` → SPEC_BASE_PATH = `features/` (thư mục cha của `tools/`)
3. Tìm file `admin/index.md` trong các thư mục cha gần nhất

### Bước 2: Resolve tên tính năng → folder path

**Nếu argument là mã FA-XXX hoặc FS-XXX:**
1. FA-XXX → Grep `{SPEC_BASE_PATH}/admin/index.md` tìm dòng chứa `FA-XXX`
2. FS-XXX → Grep `{SPEC_BASE_PATH}/system-admin/index.md` tìm dòng chứa `FS-XXX`
3. Từ dòng match → extract tên tính năng (cột "Tên tính năng") và xác định folder (kebab-case)
4. Xác định portal = `admin` hoặc `system-admin`

**Nếu argument là tên kebab-case:**
1. Check `{SPEC_BASE_PATH}/admin/{feature}/` tồn tại → portal = admin
2. Fallback: check `{SPEC_BASE_PATH}/system-admin/{feature}/` → portal = system-admin
3. Nếu không tìm thấy → thông báo lỗi, liệt kê danh sách features có sẵn từ index.md

**Kết quả**: Xác định được `{portal}` và `{feature}` → đường dẫn = `{SPEC_BASE_PATH}/{portal}/{feature}/`

### Bước 3: Kiểm tra trạng thái hoàn thành

Kiểm tra sự tồn tại của các files trong `{SPEC_BASE_PATH}/{portal}/{feature}/`:

| File | Bắt buộc? | Ý nghĩa |
|------|----------|---------|
| `feature-spec.md` | Có | Spec tổng hợp — nếu có nghĩa là feature đã hoàn thành |
| `ui/ui-spec.md` | Có | Spec giao diện |
| `web/api-spec.md` | Có | Spec API |
| `web/logic-spec.md` | Có | Spec business logic |
| `job/job-spec.md` | Không | Spec background jobs (chỉ khi feature có jobs) |
| `db/db-mapping.md` | Có | Mapping database |

Báo cáo files có/không cho user.

### Bước 4: Đọc và trình bày tổng quan

**Nếu `feature-spec.md` tồn tại** (feature đã hoàn thành):

Đọc `feature-spec.md` và trích xuất:

1. **Thông tin cơ bản**: Mã, tên VN, tên JP, portal, URL patterns, controllers chính, DB tables chính
2. **Actors**: Bảng actors + vai trò + quyền
3. **Phạm vi (Scope)**: Bao gồm / Không bao gồm
4. **Ghi chú kiến trúc**: Dual flow Legacy/V2 nếu có, hoặc các điểm đặc biệt
5. **Danh sách màn hình**: SCR-XXX + tên + URL + mô tả 1 dòng
6. **Danh sách business rules**: BR-XXX + mô tả 1 dòng (nếu có section riêng)
7. **Cross-references**: Shared components (SC-XXX), features liên quan
8. **Gaps / Unknowns**: Điểm chưa rõ, confidence thấp

**Nếu `feature-spec.md` KHÔNG tồn tại** (feature chưa hoàn thành):
- Báo cáo files nào đã có
- Nếu có `ui/ui-spec.md` → đọc phần Tổng quan từ đó
- Gợi ý: "Feature này chưa hoàn thành spec. Các phần đã có: [list]. Bạn có thể đọc từng phần bằng skill tương ứng."

### Bước 5: Gợi ý skill tiếp theo

Trình bày bảng gợi ý:

```
📋 Đọc tiếp theo vai trò:
• Frontend dev  → /read-spec-ui {feature}
• Backend API   → /read-spec-api {feature}
• Backend Logic → /read-spec-logic {feature}
• Database      → /read-spec-db {feature}
• QA / Tester   → /read-spec-test {feature}
```

## Output mẫu

```
## FA-012 Quản lý thẻ「タグ管理」

**Portal**: Admin | **URL**: /basic/tag | **Trạng thái**: HOÀN THÀNH

### Mô tả
Quản lý thẻ (tag) gán cho bạn bè LINE. Tạo, sửa, xoá, phân folder, cấu hình action tự động.

### Actors
| Actor | Vai trò | Quyền |
|-------|---------|-------|
| Admin | Quản lý toàn bộ tag | Toàn quyền |
| Staff | Truy cập theo role | Tuỳ role do Admin cấu hình |

### Màn hình (5)
| Mã | Tên | URL |
|----|-----|-----|
| SCR-TAG-01 | Danh sách tag | /basic/tag |
| SCR-TAG-02 | Modal tạo tag | /basic/tag (modal) |
| ...

### Specs có sẵn
✅ feature-spec.md | ✅ ui-spec | ✅ api-spec | ✅ logic-spec | ❌ job-spec | ✅ db-mapping

### Cross-references
- Shared components: SC-001, SC-002, SC-004
- Features liên quan: FA-001 (Chat), FA-013 (Friend List)

📋 Đọc tiếp: /read-spec-ui, /read-spec-api, /read-spec-logic, /read-spec-db, /read-spec-test
```
