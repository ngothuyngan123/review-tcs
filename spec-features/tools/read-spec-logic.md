---
name: read-spec-logic
description: "Đọc spec business logic cho backend developer — controllers, models, services, business rules, background jobs"
arguments:
  - name: feature
    description: "Tên tính năng (kebab-case VD: tag-management) hoặc mã (VD: FA-012, FS-001)"
    required: true
---

# Đọc spec Business Logic — dành cho Backend Logic Developer

## Mục đích
Đọc và trình bày business logic: controller flows, models, services, business rules, side effects, và background jobs (nếu có).

## Quy ước ngôn ngữ
- Trình bày bằng **tiếng Việt có dấu**
- Text UI tiếng Nhật giữ nguyên trong 「」
- Tên controller, model, method, service, table, column giữ nguyên tiếng Anh

## Các bước thực hiện

### Bước 1: Resolve tính năng

*(Cùng logic với read-spec.md — Bước 1 & 2)*

1. Xác định SPEC_BASE_PATH
2. Resolve `{feature}` → `{portal}` + folder path
3. Nếu không tìm thấy → báo lỗi

### Bước 2: Đọc Logic Spec

Đọc file `{SPEC_BASE_PATH}/{portal}/{feature}/web/logic-spec.md`.

Nếu file không tồn tại → thông báo "Logic spec chưa có" + liệt kê files có sẵn.

### Bước 3: Đọc Job Spec (nếu có)

Check `{SPEC_BASE_PATH}/{portal}/{feature}/job/job-spec.md`:
- Nếu tồn tại → đọc và tích hợp vào output
- Nếu không → ghi chú "Tính năng này không có background jobs"

### Bước 4: Đọc Business Rules từ Feature Spec

Đọc `{SPEC_BASE_PATH}/{portal}/{feature}/feature-spec.md` — tìm mục "Business Rules" (thường §5) và "Cross-references" (thường §7).

### Bước 5: Trình bày thông tin logic

#### A. Controllers

Với mỗi controller liên quan:
- **File path** (VD: `app/Http/Controllers/Basic/TagController.php`)
- **Namespace**
- **Số dòng** (nếu biết)
- **Danh sách actions** (public methods) + mô tả 1 dòng
- **Dependencies**: Models, Services, Traits được import

#### B. Per-Action Logic Flow

Với mỗi action chính, trình bày step-by-step:

```
Action: TagController@ajaxCreateMultipleTags
1. Nhận request params: tags[], category_id
2. Validate: kiểm tra tên tag trùng (Tags::whereIn)
3. Lấy max position trong folder
4. Bulk insert tags (bot_id, name, category_id, position)
5. Cập nhật tutorial: BotsTutorial.status_tag = 1
6. Response: {message: "success", first_tag_id: ID}

Side effects:
- INSERT INTO tags (N records)
- UPDATE bots_tutorial SET status_tag = 1
```

Focus vào:
- Thứ tự các bước xử lý
- DB operations (SELECT, INSERT, UPDATE, DELETE)
- Điều kiện rẽ nhánh (if/else)
- Side effects (ghi vào bảng khác, gọi service, sync elasticsearch, etc.)
- Error handling (throw exception, return error response)

#### C. Models

Với mỗi model liên quan:
| Model | DB Table | Relationships | Traits | Ghi chú |
|-------|---------|---------------|--------|---------|

Liệt kê relationships:
- hasMany, belongsTo, hasOne, belongsToMany
- Tên method + model liên quan + FK

#### D. Services / Helpers

Nếu có services được sử dụng:
- Tên service/class
- Methods được gọi
- Mô tả chức năng (VD: gọi LINE API, sync Elasticsearch, gửi notification)

#### E. Business Rules

Trích xuất từ feature-spec.md §5:

| BR | Mô tả | Nơi enforce | Hậu quả vi phạm |
|----|-------|-------------|-----------------|
| BR-01 | Tên tag không được trùng trong cùng bot | `ajaxCreateMultipleTags` | Lỗi 500 「そのタグ名はすでに利用されています」 |
| BR-02 | Không thao tác khi đang backup | Tất cả actions ghi | Lỗi 500 「データコピー中は...」 |

#### F. Background Jobs (nếu có)

Nếu `job-spec.md` tồn tại, trình bày:
- **Job class**: Tên class, package
- **Trigger**: Khi nào job được kích hoạt
- **Queue**: Bảng queue, state machine, polling interval
- **Logic**: Step-by-step xử lý trong job
- **Retry / Error handling**: Cách xử lý lỗi, retry policy
- **Data flow**: Input → processing → output → DB changes

#### G. Shared Tables & Cross-Feature Impact

Từ feature-spec §7:
- Bảng nào được dùng chung với features khác
- Cách phân biệt dữ liệu (VD: `category.kind=0` cho tags, `kind=1` cho folders khác)
- Side effects ảnh hưởng đến features khác (VD: sync_elasticsearch, sendAction)

### Bước 6: Highlight Confidence Levels

Đánh dấu thông tin theo mức độ tin cậy:
- **Cao**: Đọc trực tiếp từ source code
- **Trung bình**: Suy luận, cần kiểm tra
- **Thấp**: Phỏng đoán, cần xác minh

## Output format

```
## FA-XXX {Tên}「{Tên JP}」 — Logic Spec cho Backend Dev

### Controllers
| Controller | File | Actions | Dòng |
|-----------|------|---------|------|
| Basic\TagController | app/Http/Controllers/Basic/TagController.php | 20+ | 1603 |
| Api\TagController | app/Http/Controllers/Api/TagController.php | 8 | 376 |

### Models
| Model | Table | Relationships |
|-------|-------|---------------|
| Tags | tags | belongsTo(Category), hasMany(TagLineUser), hasOne(TAction) |
...

---

### Logic Flows

#### TagController@ajaxCreateMultipleTags — Tạo nhiều tag
1. Nhận params: tags[], category_id
2. Validate tên tag trùng ...
...

Side effects: INSERT tags, UPDATE bots_tutorial

---

### Business Rules
| BR | Mô tả | Nơi enforce |
...

### Background Jobs
(Không có / Hoặc chi tiết jobs)

### Shared Tables
| Table | Dùng bởi | Cách phân biệt |
...
```
