# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Hệ thống **Auto-fixbug LME** (AI) — journal `#132539` by `AI LME Fix bug`. Assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `44884f971e` (repo `sns-line`) — không có link PR trong ticket |
| Branch | `ai_fixbug_38871` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | 2026-08-24 |
| Auto-filled | `2026-09-08 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi xóa tag, hàm dọn dữ liệu của màn quản lý tag quét mọi bộ lọc tag của bot bằng `LIKE` rồi **giả định danh sách tag trong bộ lọc luôn là mảng id sạch**. Chỉ cần 1 bản ghi bộ lọc bất kỳ trong bot lưu khác dạng (id đơn lẻ, thiếu trường, hoặc dạng đối tượng `{id,name}` kiểu cũ) là vòng lặp văng lỗi, bị khối bắt lỗi bao ngoài nuốt và **dừng dọn toàn bộ các bộ lọc còn lại** — nên bộ lọc của broadcast vẫn giữ tag đã xóa kèm `text_preview` cũ.

Mọi nơi **ĐỌC** bộ lọc trong hệ thống đều đã ép kiểu mảng cho trường này, **riêng chỗ dọn lúc xóa thì không**.

## 2. Cách fix

Làm chắc bước dọn bộ lọc khi xóa tag trong `TagController::deletedDataTag` (fix **ĐỘC LẬP** branch `ai_fixbug_38871`, parent Redmine `#26684` là ticket umbrella nên không gộp branch):

1. Mỗi bộ lọc được xử lý trong **khối bắt lỗi riêng** → 1 bản ghi dữ liệu lệch dạng không còn chặn việc dọn các bộ lọc còn lại (và không chặn luôn phần dọn action + gỡ tag khỏi bạn bè phía sau).
2. **Chuẩn hóa** danh sách tag của bộ lọc về mảng id trước khi so khớp (chấp nhận id đơn lẻ hoặc phần tử dạng `{id,name}` của dữ liệu cũ).
3. **Chỉ sửa/xóa bộ lọc THỰC SỰ chứa tag vừa xóa** — bản ghi chỉ khớp do trùng chuỗi con giữ nguyên (trước đây bị ghi đè `text_preview`, thậm chí bị xóa nhầm khi thiếu trường `tags_search`).

Bộ lọc hết tag **vẫn bị xóa** và `text_preview` **vẫn được dựng lại** theo tag còn lại như cũ.

> **Yokoten**: bản sao y hệt ở API app (`TagMobileController`) **chưa sửa** — ghi nhận, không thuộc phạm vi ticket web này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TagController::deletedDataTag` — `app/Http/Controllers/Basic/TagController.php` | **CÓ SỬA** (chỗ fix chính) | Hàm dọn dữ liệu khi xóa tag |
| 2 | `TagController::ajaxDeleteTags` — `app/Http/Controllers/Basic/TagController.php` | Không sửa | Xóa tag từ màn quản lý tag v2, gọi `deletedDataTag` |
| 3 | `TagController::deleteTag` / `manageTag` case `deleteTag`\|`deleteGroup` — `app/Http/Controllers/Basic/TagController.php` | Không sửa | Các đường xóa tag còn lại, cùng gọi `deletedDataTag` |
| 4 | `FilterV2::saveFilter` — `app/FilterV2.php` | Không sửa | Nơi ghi bộ lọc tag, xác nhận cột `type='tag'` và `bot_id` |
| 5 | `FilterV2::initDataFilter` — `app/FilterV2.php` | Không sửa | Nơi đọc bộ lọc cho modal, xác nhận đều ép kiểu `(array) tags_search` |
| 6 | `BroadcastV2Controller::saveBroadcast` / `getDataFilter` — `app/Http/Controllers/Basic/BroadcastV2Controller.php` | Không sửa | Vòng đời bộ lọc của broadcast (`parent_type='broadcast'`) |
| 7 | `TagMobileController::deletedDataTag` — `app/Http/Controllers/Api/Mobile/TagMobileController.php` | **CHỈ RÀ, KHÔNG SỬA** ⚠️ | Bản sao cùng pattern — yokoten còn treo |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev **chỉ kê "File thay đổi"** (1 file) ở mục 4.1, KHÔNG kê theo function. Bảng dưới do `/new-task` suy từ mục 2 + mục 3 để gắn tag `F*` — **tester verify lại**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TagController::deletedDataTag` | `app/Http/Controllers/Basic/TagController.php` | Direct | Chỗ sửa duy nhất. 3 thay đổi: try/catch từng filter · chuẩn hóa `tags_search` · chỉ ghi khi thực sự chứa tag |
| F2 | `TagController::ajaxDeleteTags` (bulk delete) | `app/Http/Controllers/Basic/TagController.php` | Indirect | Entry point gọi F1 |
| F3 | `TagController::deleteTag` / `manageTag` case `deleteTag`\|`deleteGroup` | `app/Http/Controllers/Basic/TagController.php` | Indirect | Entry point gọi F1 (path đơn + xóa nhóm cascade) |
| F4 | Nhánh dọn `ActionDetail` + `tag_line_user` + `ActionLimitTag` (phía sau vòng lặp filter trong F1) | `app/Http/Controllers/Basic/TagController.php` | Indirect | Trước fix bị abort giữa chừng; nay luôn chạy tới nơi |
| F5 | `TagMobileController::deletedDataTag` | `app/Http/Controllers/Api/Mobile/TagMobileController.php` | **Không đổi — vẫn còn bug** ⚠️ | Yokoten chưa làm; xóa tag qua app mobile vẫn theo hành vi cũ |

**File thay đổi (nguyên văn mục 4.1 của Dev):**
- `app/Http/Controllers/Basic/TagController.php`

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `filters_v2.data` / `filters_v2.text_preview` — dòng lọc `type='tag'` của bot | UPDATE / DELETE | Nay được gỡ id tag vừa xóa (hoặc xóa cả dòng khi không còn tag) đúng như kỳ vọng ticket |
| D2 | `filters_v2` — bản ghi **chỉ khớp `LIKE` do trùng chuỗi con** | **KHÔNG còn bị chạm** (trước đây bị UPDATE/DELETE nhầm) | Giảm rủi ro mất dữ liệu so với trước — **thay đổi hành vi có chủ ý** |
| D3 | `tag_line_user` + `actions` / `action_detail` (+ `ActionLimitTag`) | DELETE / UPDATE | Phần dọn phía sau vòng lặp bộ lọc nay luôn chạy tới nơi, không bị dừng giữa chừng do 1 bộ lọc lỗi |
| D4 | Log ứng dụng — `Log::error` kèm `filter_id` cho mỗi filter dọn lỗi | CREATE (mới) | Lỗi không còn bị nuốt âm thầm; dùng để chẩn đoán nếu KH vẫn lỗi |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Tag Management (FA-012)** — xóa tag dọn sạch tham chiếu trong bộ lọc, bền với dữ liệu bộ lọc lệch dạng | F1, F2, F3, D1, D3 | High |
| T2 | **Friend Filter / Segment (SC-003)** — bộ lọc bạn bè theo tag được cập nhật/xóa đúng khi tag bị xóa | F1, D1 | High |
| T3 | **Broadcast (FA-008)** — bộ lọc đối tượng của tin gửi hàng loạt không còn giữ tag đã xóa (triệu chứng báo trong ticket) | F1, D1 | High |
| T4 | **Step Delivery / Scenario (FA-009)**, **Auto Reply (FA-003)** — bộ lọc tag dùng chung bảng `filters_v2` nên cũng được dọn đúng | F1, D1 | Medium |
| T5 | **Xóa tag qua API app mobile** (`TagMobileController`) — **KHÔNG được fix**, giữ nguyên hành vi lỗi cũ | F5 | Medium (yokoten treo) |
| T6 | Các `parent_type` còn lại của `filters_v2`: `modal_action` / `action_schedule` / `filter_manager` | F1, D1 | Medium |

---

## 5. Recover data (Dev tự nêu — không có trong template gốc)

⚠️ **CÓ.** Fix chỉ đúng cho các lần xóa tag **TỪ NAY**. Các bộ lọc đã bị bỏ sót trước đó (gồm chính broadcast trong ticket) vẫn còn id tag không tồn tại + `text_preview` cũ trong `filters_v2`; tag đã bị xóa nên **không còn sự kiện nào kích hoạt dọn lại**.

Cần 1 script dọn 1 lần: rà `filters_v2 type='tag'`, bỏ id không còn trong bảng `tags`, dựng lại `text_preview`, xóa dòng nếu rỗng.
**Phạm vi**: `filters_v2 (type='tag')` của các bot có tag đã xóa — mọi `parent_type`: `broadcast` / `step_message` / `auto_reply` / `modal_action` / `action_schedule` / `filter_manager`.

→ **Chờ human quyết định vì nằm ngoài phạm vi ticket.** Tester **phải dùng data mới tạo** khi verify, không dùng lại data cũ của ticket.

## 6. Verify của Dev (mức đạt được)

| Mục | Nội dung |
|---|---|
| Mức verify | **lint** (không chạy runtime) |
| Lệnh | `php -l app/.../TagController.php` → No syntax errors. Script PHP tách riêng test logic chuẩn hóa `tags_search` **6 dạng** (mảng id / 1 tag / id đơn lẻ / dạng `{id,name}` cũ / thiếu trường / chỉ trùng chuỗi con): **ALL PASS**. `git diff --stat release_step_20260805...ai_fixbug_38871`: 1 file, 48+/29- |
| ⚠️ Giới hạn | **KHÔNG kiểm chứng được bằng data runtime** — MySQL `host.docker.internal:3306` *Connection refused*, web `:8000` không phản hồi |
| Bằng chứng root cause | 10 chỗ ĐỌC bộ lọc đều ép kiểu `(array) tags_search`: `FilterV2:907,1139` · `FilterController:344,587` · `CrossAnalysisController:1100,1353` · `ActionScheduleController:1665` · `FriendlistController:4554` · `FilterV2Replicate:566,772` ⇒ dữ liệu trường này thực tế **có dạng khác mảng**. Ngay trong cùng hàm `deletedDataTag`, nhánh dọn action đã chủ động ép kiểu `((array)$data['ids'])` ⇒ pattern lệch dạng là có thật |

## 7. Rủi ro Dev tự nêu khi test

- Chưa tái hiện được trên dev (DB/web dev down) → root cause dựa vào phân tích code. **Nếu môi trường KH có nguyên nhân khác** (vd bộ lọc lưu `bot_id` khác) thì fix này chưa đủ — cần log lỗi `deletedDataTag filter_id ... error` mới thêm để chẩn đoán tiếp.
- Dữ liệu cũ đã bỏ sót **không tự dọn** (xem mục 5).
- Bản ghi chỉ khớp `LIKE` nay được **giữ nguyên** thay vì bị ghi đè `text_preview` — chủ ý (tránh mất dữ liệu), nhưng **là thay đổi hành vi so với code cũ**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
