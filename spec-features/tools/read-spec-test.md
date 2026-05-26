---
name: read-spec-test
description: "Đọc spec cho QA/tester — test scenarios, business rules, error cases, edge cases, assertions"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc spec cho Testing — dành cho QA / Tester

## Mục đích
Đọc và tổng hợp thông tin testable từ tất cả specs: test scenarios, business rules, validation rules, error cases, edge cases, và assertions.

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Text UI tiếng Nhật giữ nguyên trong 「」 — tester cần biết exact text để verify
- Error messages tiếng Nhật giữ nguyên

## Các bước thực hiện

### Bước 1: Resolve tính năng

*(Cùng logic với read-spec.md — Bước 1 & 2)*

1. Xác định SPEC_BASE_PATH
2. Resolve `{feature}` → `{portal}` + folder path
3. Nếu không tìm thấy → báo lỗi

### Bước 2: Đọc Feature Spec (nguồn chính)

Đọc `{SPEC_BASE_PATH}/{portal}/{feature}/feature-spec.md` — file tổng hợp là nguồn tốt nhất cho testing vì chứa end-to-end flows.

Trích xuất:
- §1: Actors + scope (in/out of scope)
- §2: Màn hình + Luồng end-to-end (happy paths)
- §5: Business Rules (BR-XX)
- §7: Cross-references (side effects ảnh hưởng features khác)
- §8: Gaps / Unknowns (cần exploratory testing)

### Bước 3: Đọc UI Spec (user flows + validation)

Đọc `{SPEC_BASE_PATH}/{portal}/{feature}/ui/ui-spec.md`:
- User Flows — step-by-step thao tác user
- Form Fields — validation rules (required, max length, format)
- Error messages hiển thị trên UI
- Pagination, filtering behavior

### Bước 4: Đọc API Spec (error responses)

Đọc `{SPEC_BASE_PATH}/{portal}/{feature}/web/api-spec.md`:
- Error responses per endpoint (HTTP code, điều kiện, message)
- Validation rules per param
- Edge cases (empty input, boundary values, concurrent access)

### Bước 5: Đọc Job Spec (nếu có)

Check `{SPEC_BASE_PATH}/{portal}/{feature}/job/job-spec.md`:
- Nếu tồn tại → trích xuất test scenarios cho background jobs
- Queue states, timing, failure/retry scenarios

### Bước 6: Tổng hợp và trình bày theo format testing

#### A. Scope & Actors

| Actor | Quyền | Test cần cover |
|-------|-------|---------------|
| Admin | Toàn quyền | Tất cả operations |
| Staff | Tuỳ role | Test quyền bị giới hạn, access denied cases |

**In scope**: {liệt kê}
**Out of scope**: {liệt kê — không test phần này}

#### B. Test Scenarios per Screen

Tổ chức theo màn hình, mỗi scenario gồm:

**Happy Path Scenarios:**
```
TC-01: {Tên test case}
Precondition: {Điều kiện ban đầu}
Steps:
  1. {Bước 1}
  2. {Bước 2}
Expected: {Kết quả mong đợi}
Verify: {Assertions cụ thể — text JP, DB change, API response}
```

**Validation / Error Scenarios:**
```
TC-XX: {Tên — VD: Tạo tag với tên trùng}
Precondition: Đã có tag tên "Tag A"
Steps:
  1. Mở form tạo tag mới
  2. Nhập tên "Tag A" (trùng)
  3. Click「保存」
Expected: Hiển thị lỗi「そのタグ名はすでに利用されています」
API Response: HTTP 500
```

**Edge Case Scenarios:**
```
TC-XX: {Tên — VD: Tạo tag khi đang backup}
Precondition: Hệ thống đang chạy data backup
Steps:
  1. Thử tạo/sửa/xoá tag
Expected: Lỗi「データコピー中は、データ不備を回避するために、編集不可能です。...」
```

#### C. Business Rules as Test Assertions

Chuyển đổi mỗi BR-XX thành assertion testable:

| BR | Mô tả | Test Assertion | Priority |
|----|-------|---------------|----------|
| BR-01 | Tên tag không được trùng | INSERT tag "X" → OK. INSERT tag "X" lần 2 → error | Cao |
| BR-02 | Không thao tác khi backup | Khi backup status IN (0,1) → mọi POST/DELETE → error 500 | Cao |

#### D. Cross-Feature Impact Tests

Từ feature-spec §7:
- Hành động trong feature này ảnh hưởng features nào?
- VD: Xoá tag → xoá tag_line_user → sync_elasticsearch → ảnh hưởng friend list filter

| Hành động | Ảnh hưởng | Feature bị ảnh hưởng | Cần verify |
|----------|----------|---------------------|-----------|

#### E. Background Job Tests (nếu có)

Nếu có job-spec:
- Job có được trigger đúng thời điểm?
- Queue state transitions đúng?
- Failure handling / retry hoạt động?
- Data consistency sau job complete?

#### F. Exploratory Testing Focus Areas

Từ feature-spec §8 (Gaps/Unknowns) và items có confidence **Thấp** hoặc **Trung bình**:

| Area | Lý do | Gợi ý test |
|------|-------|-----------|
| Staff permissions | Confidence Trung bình — chưa xác nhận rõ cơ chế | Test các role khác nhau, verify access control |
| Dual flow Legacy/V2 | Flow legacy có thể còn accessible | Test truy cập trực tiếp URL legacy |

#### G. Enum / Status Boundary Tests

Nếu có enum values:
| Cột | Giá trị hợp lệ | Test boundary |
|-----|---------------|--------------|
| `auto_reply.status` | 0 (tắt), 1 (bật) | Gửi giá trị 2, -1, null |

## Output format

```
## FA-XXX {Tên}「{Tên JP}」 — Test Spec

### Scope
**In scope**: ...
**Out of scope**: ...

### Actors
| Actor | Quyền | Test coverage |
...

---

### SCR-XXX-01: {Tên màn hình}

#### Happy Path
TC-01: Load danh sách thành công
...

TC-02: Tạo mới thành công
...

#### Validation / Errors
TC-05: Tên trùng → lỗi「...」
...

#### Edge Cases
TC-08: Thao tác khi đang backup
...

---

### Business Rules
| BR | Assertion | Priority |
...

### Cross-Feature Impact
| Hành động | Ảnh hưởng | Verify |
...

### Exploratory Testing
| Area | Lý do | Gợi ý |
...
```
