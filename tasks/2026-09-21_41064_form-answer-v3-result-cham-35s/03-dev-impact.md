# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `bed522fed1` (repo `sns-line`) · Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41064 |
| Branch | `ai_small_41064` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-21 (Journal #137306) |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn xem kết quả trả lời biểu mẫu nạp dữ liệu bằng một truy vấn phân trang rồi **lặp qua TỪNG dòng** để lấy thêm thông tin. Giao diện mặc định lấy 100 dòng mỗi trang nên mỗi lần mở màn, máy chủ bắn khoảng **200-300 truy vấn con**: mỗi dòng một truy vấn lấy bạn bè theo khóa chính và một truy vấn lấy danh sách nhắc hẹn (kèm truy vấn lấy người xóa).

Ngoài ra còn một **truy vấn thừa lên bảng sự kiện** (lọc theo cột không có chỉ mục, kết quả lấy ra nhưng không dùng ở đâu) chạy mỗi request.

Phần **lọc ngày dùng hàm cắt ngày** trên cột thời gian tạo nên không dùng được chỉ mục; cộng với việc bảng kết quả trả lời là **bảng log dùng chung toàn hệ thống** và câu lệnh còn sắp xếp theo thời gian tạo, nên cả câu đếm tổng của phân trang lẫn câu lấy dữ liệu đều phải quét rồi sắp xếp toàn bộ số dòng của biểu mẫu đó.

Biểu mẫu càng nhiều lượt trả lời thì request càng lâu, đúng như dữ liệu trong ticket (nhiều bot khác nhau, nhiều biểu mẫu khác nhau đều chậm từ 5s tới 35s).

## 2. Cách fix

Sửa màn xem kết quả trả lời biểu mẫu (`sns-line`, nhánh `ai_small_41064`, **2 file**):

1. **Bỏ vòng lặp bắn truy vấn theo từng dòng** — gom thành **2 truy vấn theo lô** cho cả trang: một truy vấn lấy bạn bè theo danh sách mã (chỉ 4 cột đang dùng) và một truy vấn lấy nhắc hẹn theo danh sách mã kết quả (giữ nguyên eager load người xóa và lấy cả bản ghi đã xóa mềm), rồi tra theo bảng ánh xạ trong vòng lặp; nhóm nhắc hẹn được **đánh lại số thứ tự** để dữ liệu trả về vẫn là mảng như cũ.
2. **Xóa truy vấn thừa lên bảng sự kiện** (lấy ra nhưng không dùng, lọc theo cột không có chỉ mục nên quét cạn bảng mỗi request).
3. **Đổi lọc ngày** từ hàm cắt ngày sang **so sánh khoảng thời gian** (từ `00:00:00` ngày bắt đầu tới `23:59:59` ngày kết thúc) để dùng được chỉ mục — có hàm đọc ngày chấp nhận cả **ba định dạng** giao diện gửi (dấu chấm, gạch ngang, gạch chéo), đọc không được thì **quay về cách lọc cũ** (fallback).
4. **Giới hạn cột được phép sắp xếp theo danh sách trắng** (trước đây lấy thẳng tên cột từ request).
5. **Thêm migration tạo chỉ mục** `(form_id, deleted_at, created_at)` cho bảng kết quả trả lời, có kiểm tra chỉ mục đã tồn tại nên **chạy lại vẫn an toàn** (idempotent).
6. **Bỏ đọc file** khi giá trị câu trả lời dạng tệp rỗng.

> **Quét ngang (Dev ghi nhận, KHÔNG sửa):** màn kết quả biểu mẫu **bản cũ** trong cùng tệp còn nguyên kiểu lặp truy vấn và lọc ngày này nhưng là **endpoint khác** — ghi nhận chứ không sửa ngoài phạm vi ticket.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerController::showFormResultV3` — `app/Http/Controllers/Basic/FormAnswerController.php:4182` | **ĐÃ SỬA** — gom truy vấn theo lô, xóa truy vấn thừa, đổi lọc ngày, whitelist cột sắp xếp, bỏ đọc file rỗng | Là endpoint bị chậm trong ticket |
| 2 | `FormAnswerController::parseFormResultFilterDate` — `app/Http/Controllers/Basic/FormAnswerController.php` | **HÀM MỚI** — đọc ngày lọc, chấp nhận 3 định dạng (`.` `-` `/`), trả `null` khi không đọc được → fallback cách lọc cũ | Phục vụ đổi lọc ngày sang so sánh khoảng thời gian |
| 3 | `FormAnswerController::showFormResult` — `app/Http/Controllers/Basic/FormAnswerController.php:4057` | **KHÔNG SỬA** — bản cũ, cùng pattern (lặp truy vấn + lọc ngày bằng hàm cắt ngày), endpoint khác | Ngoài phạm vi ticket — chỉ ghi nhận |
| 4 | `is_image` — `app/Helpers/functions.php:9149` | Không sửa — chỉ check caller | Liên quan xử lý giá trị câu trả lời dạng tệp (mục fix số 6) |
| 5 | `FormAnswerItemRemind::userDeleted` — `app/FormAnswerItemRemind.php` | Không sửa — giữ nguyên eager load trong truy vấn theo lô | Quan hệ "người xóa" của nhắc hẹn phải giữ nguyên sau khi gom lô |
| 6 | `AddIndexFormCreatedToFormAnswerResultTable::up` — `database/migrations/2026_09_17_150000_add_index_form_created_to_form_answer_result_table.php` | **FILE MỚI** — tạo chỉ mục, có check tồn tại trước khi tạo | Cho phép truy vấn lọc/sắp xếp dùng được chỉ mục |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ liệt kê **file thay đổi** (2 file), không kê theo format `F1/F2/...`. Bảng dưới do `/new-task` suy từ mục 2 + 3 — **tester verify lại trước khi dùng làm coverage**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerController::showFormResultV3` (endpoint `POST /basic/form-answer/v3/result/{id}`) | `app/Http/Controllers/Basic/FormAnswerController.php:4182` | Direct | Toàn bộ 6 điểm fix nằm ở đây |
| F2 | `FormAnswerController::parseFormResultFilterDate` | `app/Http/Controllers/Basic/FormAnswerController.php` | Direct (hàm mới) | 3 định dạng ngày + fallback khi parse fail |
| F3 | Migration `AddIndexFormCreatedToFormAnswerResultTable` | `database/migrations/2026_09_17_150000_add_index_form_created_to_form_answer_result_table.php` | Direct (file mới) | Idempotent — chạy lại không lỗi; có `down()` rollback chỉ mục |
| F4 | `FormAnswerItemRemind::userDeleted` (quan hệ eager load) | `app/FormAnswerItemRemind.php` | Indirect | Không sửa code nhưng đổi cách gọi: từ per-row sang whereIn theo lô + `withTrashed` |
| F5 | `is_image` | `app/Helpers/functions.php:9149` | Indirect | Bị ảnh hưởng bởi mục fix "bỏ đọc file khi giá trị dạng tệp rỗng" |
| F6 | `FormAnswerController::showFormResult` (bản cũ) | `app/Http/Controllers/Basic/FormAnswerController.php:4057` | **KHÔNG sửa** | Cùng pattern, endpoint khác — Dev ghi nhận, để ngoài phạm vi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answer_result` — chỉ mục `form_answer_result_form_deleted_created_index` (`form_id`, `deleted_at`, `created_at`) | MIGRATE (ALTER TABLE thêm chỉ mục phụ) | **KHÔNG đổi dữ liệu**. Bảng log lớn dùng chung toàn hệ thống → nên chạy **ngoài giờ cao điểm** hoặc bằng `pt-online-schema-change` |
| D2 | `form_answer_item_remind` | READ only | Chỉ đọc, không đổi. Truy vấn theo lô dùng chỉ mục `form_result_id` sẵn có |
| D3 | `line_user` | READ only | Chỉ đọc, không đổi — nay lấy theo lô, chỉ 4 cột đang dùng |
| D4 | `events` (cột `form_answer_id`) | (BỎ truy vấn) | Truy vấn thừa đã bị xóa; cột `form_answer_id` KHÔNG có chỉ mục nên trước đây quét cạn bảng mỗi request |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — màn xem kết quả trả lời biểu mẫu bản **v3** | F1, F2, D1 | **High** — nạp nhanh hơn; dữ liệu trả về phải **giữ nguyên định dạng** (tên/ảnh đại diện bạn bè, danh sách nhắc hẹn, điểm chẩn đoán, phân trang) |
| T2 | **Friend Information (FA-015)** — tên hiển thị + ảnh đại diện bạn bè trong danh sách kết quả | F1, D3 | **Medium** — nay lấy theo lô thay vì từng dòng, chỉ đọc 4 cột đang dùng |

---

## Rủi ro / lưu ý khi test (Dev tự nêu)

- ⚠️ **ALTER TABLE thêm chỉ mục trên `form_answer_result`** là bảng log lớn — MySQL 5.7 thêm chỉ mục phụ không chặn đọc/ghi nhưng vẫn tốn thời gian và dung lượng; nên chạy ngoài giờ cao điểm hoặc bằng `pt-online-schema-change` (đã ghi chú trong migration).
- ⚠️ **Đổi lọc ngày sang so sánh khoảng thời gian**: với chuỗi ngày hợp lệ kết quả **giống hệt** cách cũ; với chuỗi lạ mà thư viện thời gian vẫn đọc được theo nghĩa **tương đối** (ví dụ `yesterday`) thì phạm vi lọc sẽ **khác cách cũ** — giao diện chỉ gửi định dạng `YYYY.MM.DD` nên Dev đánh giá không ảnh hưởng thực tế.
- ⚠️ **Whitelist cột sắp xếp**: nếu sau này có nơi gọi truyền cột khác thì sẽ bị **bỏ qua thay vì lỗi truy vấn** — giao diện hiện chỉ gửi `created_at`.

## Mức VERIFY của Dev

- **Mức: `lint`** (không phải test thật). `php -l` 2 file OK; boot Laravel in `toSql`; gọi hàm đọc ngày qua Reflection; in SQL 2 truy vấn theo lô; kiểm JSON nhóm nhắc hẹn; `git diff --stat` = đúng 2 file (+164/-20).
- ⚠️ **MySQL dev + web dev KHÔNG kết nối được** trong lần chạy này → **chưa EXPLAIN trên dữ liệu thật**, kết luận về chỉ mục chỉ dựa trên định nghĩa migration trong repo.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
