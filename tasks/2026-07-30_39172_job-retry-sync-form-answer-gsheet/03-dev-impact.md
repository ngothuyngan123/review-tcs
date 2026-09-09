# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> Nguồn: description Redmine #39172 (mục 1–5), Dev cập nhật qua journal #127553 (2026-07-30).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` (assignee) |
| Commit / Pull Request | commit `8752ddccdf8375818d2e8a07754304abd1111089` (không có URL PR trong Redmine) |
| Branch | `m_202607_retry_form_update_id_39172` |
| Ngày submit đánh giá | `2026-07-30` |
| Auto-filled | `2026-07-30 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bản ghi `form_answer_result` **cũ** không có `result_error_google_id` (back-link). Job retry set status về `NEW` nhưng **không set lại `result_error_google_id`**, nên khi retry sync xong, success path (`HandleFormAnswerSyncGoogleSheetTask` dòng **839-840** check `result_error_google_id > 0`) **không đóng được** `ResultErrorGoogle` → **treo mãi ở `STATUS_RUNNING`** (job retry chỉ pick `STATUS_NEW` nên không bao giờ xử lý lại).

## 2. Cách fix

- Khi retry job reset status về `NEW` thì **set lại `result_error_google_id = resultErrorGoogle.id` trong cùng 1 UPDATE (atomic)**, thêm 2 query `updateStatusSyncAndErrorId` / `updateStatusDeleteAndErrorId`.
- **Persist `ResultErrorGoogle = RUNNING` TRƯỚC khi mở lại bản ghi**, tránh main task set `SUCCESS` xong bị ghi đè ngược thành `RUNNING`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerResultRepository.updateStatusSyncAndErrorId` | **Mới** | Query atomic set status NEW + result_error_google_id |
| 2 | `FormAnswerResultRepository.updateStatusDeleteAndErrorId` | **Mới** | Query atomic cho nhánh delete |
| 3 | `RetryErrorGoogleSheetTask.needRetryErrorGoogle` (private, chạy trong loop của task) | Gọi 2 method mới | Nơi duy nhất gọi 2 method mới |

> Dev ghi rõ: 2 method repository là **mới**, chỉ gọi từ `RetryErrorGoogleSheetTask.needRetryErrorGoogle`. **Không sửa** `updateStatusSync`/`updateStatusDelete` cũ nên **không ảnh hưởng caller khác. Scope local.**

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerResultRepository.updateStatusSyncAndErrorId` (mới) | FormAnswerResultRepository | Direct | Set NEW + result_error_google_id atomic (nhánh SYNC) |
| F2 | `FormAnswerResultRepository.updateStatusDeleteAndErrorId` (mới) | FormAnswerResultRepository | Direct | Set NEW + result_error_google_id atomic (nhánh DELETE) |
| F3 | `RetryErrorGoogleSheetTask.needRetryErrorGoogle` | RetryErrorGoogleSheetTask | Direct | Gọi F1/F2 + persist ResultErrorGoogle=RUNNING trước khi reset |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answer_result.result_error_google_id` | UPDATE (ghi thêm giá trị vào **cột sẵn có** khi retry) | Dev ghi "Không có" đổi schema/config/constant — chỉ ghi giá trị vào cột đã tồn tại |
| D2 | `ResultErrorGoogle.status` (RUNNING → SUCCESS) | UPDATE (chuyển trạng thái) | Suy từ mô tả — đây là trạng thái treo bug; TC phải verify chuyển đúng |

> Dev khẳng định 4.2 = "Không có" (không đổi schema). D1/D2 ở đây là **hành vi data** (ghi cột sẵn có + chuyển status) — tách ra để TC bám, **không phải** thay đổi cấu trúc.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Job retry SYNC form answer lên Google Sheet**: bản ghi cũ có `result_error_google_id = 0/null` bị lỗi sync → retry xong verify `ResultErrorGoogle` chuyển `RUNNING → SUCCESS` (không còn treo RUNNING) | F1, F3, D1, D2 | High (suy luận — root cause của ticket) |
| T2 | **Retry DELETE form answer**: `status_sync_deleted = WAIT_RETRY` → retry xong `ResultErrorGoogle` đóng đúng | F2, F3, D1, D2 | Medium (suy luận) |
| T3 | **Sync/retry đa luồng (race)**: verify không còn race treo RUNNING (`ResultErrorGoogle` set `RUNNING` **trước** khi reset bản ghi về `NEW`) | F3, D2 | High (suy luận — race/idempotency) |

> Dev **không ghi mức High/Medium/Low** — cột "Nguy cơ regression" là **suy luận** để định hướng review, tester/Leader xác nhận lại.

---

## 5. Commit / Branch (mục 5 của Redmine)

- **Commit**: `8752ddccdf8375818d2e8a07754304abd1111089`
- **Branch**: `m_202607_retry_form_update_id_39172`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
