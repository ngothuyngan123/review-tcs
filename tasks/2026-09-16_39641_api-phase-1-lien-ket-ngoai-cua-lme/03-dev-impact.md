# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #39641 KHÔNG có section "Đánh giá ảnh hưởng phía dev".**
> Description chỉ có ghi chú triển khai ngắn (branch base, nơi đặt controller, điều kiện check key) — **không có** 4 mục chuẩn (1. Nguyên nhân · 2. Cách fix · 3. Function caller đã check · 4.1/4.2/4.3 impact).
> `/review-tc` sẽ **không chạy được BƯỚC 2 chiều (a) `dev-impact`** với input này.
>
> **2 cách bổ sung — chọn 1:**
> 1. Yêu cầu Dev điền 4 mục chuẩn vào Redmine rồi chạy lại `/new-task 39641`.
> 2. Chấp nhận thay thế bằng **tab Thông tin của MCP LME TEST STUDIO** (`task_get_context(74, sections=["dev_impact","spec_delta"])`) — `/review-tc` BƯỚC 2 chiều (b) `diff code` vẫn chạy được từ nguồn này.
>
> ⚠️ Vì đây là ticket **Feature** (tính năng mới), không phải bug fix, nên mục 1 (Nguyên nhân) và mục 2 (Cách fix) vốn **không áp dụng** theo nghĩa thông thường — nhưng mục 3 và 4 (caller đã check + impact lên tính năng cũ) thì **vẫn bắt buộc** vì API mới có ghi dữ liệu thật vào friend / tag / scenario / message của hệ thống hiện hữu.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Văn Đức Nguyễn (assignee Redmine) |
| Commit / Pull Request | `<chưa có>` — không có link Git nào trong description/journals |
| Branch | `feature/docs-api` (Journal #130732). Branch base: `release-product` (description) |
| Ngày submit đánh giá | `<chưa có>` — không có journal nào chứa section "Đánh giá ảnh hưởng" |
| Auto-filled | `2026-09-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

⚠️ **Không tick được checkbox này** cho tới khi Dev bổ sung đánh giá ảnh hưởng — hiện Redmine không có gì để verify.

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp>`

*(Ticket Feature, không có root cause. Mục này N/A.)*

## 2. Cách fix

`<Input thiếu — Dev chưa cung cấp section "Đánh giá ảnh hưởng".>`

Chỉ có **ghi chú triển khai** nguyên văn trong description Redmine (KHÔNG phải mục "Cách fix" theo format chuẩn):

```
Branch base: release-product
Api viết trong package controller
update repositories: thêm package và config connect vào db chính để update
Nội dung chi tiết đọc ở file đính kèm: api-detail-spec-proposal_vi (7).html

======================================================
*** Tìm trong bảng access_key_api where theo secret_key, check nếu ko thỏa mãn 1 trong các điều kiện thì không được access api:
- role_access: Nếu read chỉ được access api read
- expired_date: >= now() hoặc NULL (không giới hạn)
- status: 1 (enable)
```

⚠️ Tên bảng/cột ở ghi chú này (`access_key_api`, `secret_key`, `role_access`, `expired_date`) **không khớp** schema trong spec đính kèm và trong TC trên Studio (`api_keys`, `key_lookup_hash`, `expires_at`, `is_deleted`, `status`). Cần Dev xác nhận schema thực tế.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — Dev chưa liệt kê caller đã check>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |
| 2 | | | |

⚠️ Đây là mục **rủi ro cao nhất** của ticket này: API `POST /v1/do_action` và `POST /v1/messages/*` ghi thẳng vào tag / friend info / scenario / point / chat 1:1 / trạng thái xử lý — tức là **dùng lại đường ghi của tính năng hiện hữu**. Không có danh sách caller thì không rà được regression lên màn quản trị tương ứng.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

`<Input thiếu — Dev chưa cung cấp>`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu>` | | Direct / Indirect | |
| F2 | | | | |
| F3 | | | | |

### 4.2. List data bị update khi fix bug

`<Input thiếu — Dev chưa cung cấp>`

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu>` | CREATE / UPDATE / DELETE / MIGRATE | |
| D2 | | | |
| D3 | | | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

`<Input thiếu — Dev chưa cung cấp>`

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu>` | | High / Medium / Low |
| T2 | | | |
| T3 | | | |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
