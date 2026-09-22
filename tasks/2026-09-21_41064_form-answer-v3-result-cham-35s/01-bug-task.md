# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41064 — [AI][Performance] POST /basic/form-answer/v3/result/{id} chậm max 35s (4 lần/24h)` |
| Module / Màn hình | Form Builder (FA-011) — màn **xem kết quả trả lời biểu mẫu bản v3** (endpoint `POST /basic/form-answer/v3/result/{id}`) |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

**Endpoint:** `POST /basic/form-answer/v3/result/{id}`

- **Mức:** high — xếp theo độ chậm: **max 35s** trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 62
- **Số lần chậm 24h:** 4 (kỳ trước 6, 1h qua 3) — xu hướng flat
- **Thời gian:** max 35s · p95 35s · trung bình 15.5s · median 10s
- **Phân bố:** ≥15s SUPPERSLOW 3 · 10–15s VERYSLOW 5 · 5–10s SLOWLV1 6
- **User bị ảnh hưởng:** 3 (tổng 12)
- **Server:** step.lme.jp — **BotId:** 122146, 185531, 126113, 3458, 112319, 22103, 203456, 67342, 27766, 154096
- **Lần đầu:** 2026-09-14 02:30 UTC — **Lần cuối:** 2026-09-17 06:06 UTC
- **Lịch sử dài hạn:** tổng 14 lần chậm trong 4 ngày, đỉnh 7 lần/24h, chậm nhất 35s, từ 2026-09-14 02:30 UTC

**Vì sao ưu tiên này**
- Độ chậm: p95 35s — cực chậm (+38 điểm)
- Tần suất: 4 lần/24h (+6 điểm)
- User ảnh hưởng: 3 user bị chậm (+6 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Tương đương 24h trước (+0 điểm)

**URL mẫu**
- `/basic/form-answer/v3/result/81128?page=1`
- `/basic/form-answer/v3/result/176252?page=1`
- `/basic/form-answer/v3/result/86320?page=1`
- `/basic/form-answer/v3/result/178808?page=1`
- `/basic/form-answer/v3/result/3404?page=1`

**Query param gặp:** `page`

**Các lần CHẬM NHẤT đã ghi nhận**

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 35 | 2026-09-17 13:06 VN | SUPPERSLOW | 16712 | /basic/form-answer/v3/result/12598?page=1 |
| 16 | 2026-09-16 10:53 VN | SUPPERSLOW | 133872 | /basic/form-answer/v3/result/176252?page=1 |
| 15 | 2026-09-16 09:18 VN | SUPPERSLOW | 162113 | /basic/form-answer/v3/result/208130?page=1 |
| 14 | 2026-09-15 08:44 VN | VERYSLOW | 89404 | /basic/form-answer/v3/result/86320?page=1 |
| 12 | 2026-09-14 14:26 VN | VERYSLOW | 70139 | /basic/form-answer/v3/result/176252?page=1 |
| 11 | 2026-09-16 07:18 VN | VERYSLOW | 152396 | /basic/form-answer/v3/result/72282?page=1 |
| 10 | 2026-09-17 13:05 VN | VERYSLOW | 115612 | /basic/form-answer/v3/result/122289?page=1 |
| 10 | 2026-09-17 12:58 VN | VERYSLOW | 16712 | /basic/form-answer/v3/result/12598?page=1 |
| 9 | 2026-09-14 09:30 VN | SLOWLV1 | 86399 | /basic/form-answer/v3/result/81128?page=1 |
| 8 | 2026-09-16 10:53 VN | SLOWLV1 | 133872 | /basic/form-answer/v3/result/176252?page=1 |
| 7 | 2026-09-17 09:07 VN | SLOWLV1 | 37585 | /basic/form-answer/v3/result/34812?page=1 |
| 6 | 2026-09-15 23:00 VN | SLOWLV1 | 3636 | /basic/form-answer/v3/result/3404?page=1 |
| 5 | 2026-09-16 06:32 VN | SLOWLV1 | 146403 | /basic/form-answer/v3/result/204623?page=1 |
| 5 | 2026-09-15 12:08 VN | SLOWLV1 | 36215 | /basic/form-answer/v3/result/178808?page=1 |

**Nguồn cảnh báo trong source**

Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket do AI detect performance tự tạo từ log request chậm. -->

## Expected result

<!-- (trống) -->

## Actual result

<!-- (trống) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41064 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket do AI detect performance tự sinh từ log request chậm, KHÔNG có section "Tái hiện bug" với Steps / Expected / Actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix + regression impact**.

- **Môi trường phát hiện:** production `step.lme.jp`.
- **Tần suất:** KHÔNG phải 100% — chỉ 4 lần chậm/24h trên toàn hệ thống. Độ chậm phụ thuộc **số lượt trả lời của biểu mẫu** (biểu mẫu càng nhiều lượt trả lời càng chậm) → muốn tái hiện phải dựng biểu mẫu có rất nhiều bản ghi `form_answer_result`.
- **Điều kiện tiên quyết dựng env:** biểu mẫu v3 có lượng lớn lượt trả lời; giao diện mặc định gửi `paginate = per_page` với `per_page` mặc định **100** và `order = created_at` (`public/js/form_answer/form_result_v3.js:110`).
- ⚠️ **Migration thêm chỉ mục** chạy trên `form_answer_result` — bảng log dùng chung toàn hệ thống → thời điểm chạy migration là rủi ro **vận hành**, không chỉ là rủi ro chức năng.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | 122146, 185531, 126113, 3458, 112319, 22103, 203456, 67342, 27766, 154096 |
| Friend | — (ticket chỉ ghi user admin bị chậm: 16712, 133872, 162113, 89404, 70139, 152396, 115612, 86399, 37585, 3636, 146403, 36215) |
| Đối tượng cấu hình | Biểu mẫu (form) ID: **12598** (ca chậm nhất 35s), 176252, 208130, 86320, 72282, 122289, 81128, 34812, 3404, 204623, 178808 |
| Thời điểm lỗi | 2026-09-17 13:06 VN (max 35s); khoảng ghi nhận 2026-09-14 → 2026-09-17 |
| Đối chứng | Biểu mẫu ít lượt trả lời — cùng màn, cùng endpoint, phản hồi nhanh |

## Journal / note từ Redmine (nguyên văn)

**Journal #137306 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn xem kết quả trả lời biểu mẫu nạp dữ liệu bằng một truy vấn phân trang rồi lặp qua TỪNG dòng để lấy thêm thông tin. Giao diện mặc định lấy 100 dòng mỗi trang nên mỗi lần mở màn, máy chủ bắn khoảng 200-300 truy vấn con: mỗi dòng một truy vấn lấy bạn bè theo khóa chính và một truy vấn lấy danh sách nhắc hẹn (kèm truy vấn lấy người xóa). Ngoài ra còn một truy vấn thừa lên bảng sự kiện (lọc theo cột không có chỉ mục, kết quả lấy ra nhưng không dùng ở đâu) chạy mỗi request. Phần lọc ngày dùng hàm cắt ngày trên cột thời gian tạo nên không dùng được chỉ mục; cộng với việc bảng kết quả trả lời là bảng log dùng chung toàn hệ thống và câu lệnh còn sắp xếp theo thời gian tạo, nên cả câu đếm tổng của phân trang lẫn câu lấy dữ liệu đều phải quét rồi sắp xếp toàn bộ số dòng của biểu mẫu đó. Biểu mẫu càng nhiều lượt trả lời thì request càng lâu, đúng như dữ liệu trong ticket (nhiều bot khác nhau, nhiều biểu mẫu khác nhau đều chậm từ 5s tới 35s).

■ 2. CÁCH FIX
Sửa màn xem kết quả trả lời biểu mẫu (sns-line, nhánh ai_small_41064, 2 file). (1) Bỏ vòng lặp bắn truy vấn theo từng dòng: gom thành 2 truy vấn theo lô cho cả trang — một truy vấn lấy bạn bè theo danh sách mã (chỉ 4 cột đang dùng) và một truy vấn lấy nhắc hẹn theo danh sách mã kết quả (giữ nguyên eager load người xóa và lấy cả bản ghi đã xóa mềm), rồi tra theo bảng ánh xạ trong vòng lặp; nhóm nhắc hẹn được đánh lại số thứ tự để dữ liệu trả về vẫn là mảng như cũ. (2) Xóa truy vấn thừa lên bảng sự kiện (lấy ra nhưng không dùng, lọc theo cột không có chỉ mục nên quét cạn bảng mỗi request). (3) Đổi lọc ngày từ hàm cắt ngày sang so sánh khoảng thời gian (từ 00:00:00 ngày bắt đầu tới 23:59:59 ngày kết thúc) để dùng được chỉ mục — có hàm đọc ngày chấp nhận cả ba định dạng giao diện gửi (dấu chấm, gạch ngang, gạch chéo), đọc không được thì quay về cách lọc cũ. (4) Giới hạn cột được phép sắp xếp theo danh sách trắng (trước đây lấy thẳng tên cột từ request). (5) Thêm migration tạo chỉ mục (mã biểu mẫu, thời điểm xóa mềm, thời gian tạo) cho bảng kết quả trả lời, có kiểm tra chỉ mục đã tồn tại nên chạy lại vẫn an toàn. (6) Bỏ đọc file khi giá trị câu trả lời dạng tệp rỗng. Quét ngang: màn kết quả biểu mẫu bản cũ trong cùng tệp còn nguyên kiểu lặp truy vấn và lọc ngày này nhưng là endpoint khác, ghi nhận chứ không sửa ngoài phạm vi ticket.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FormAnswerController::showFormResultV3 (app/Http/Controllers/Basic/FormAnswerController.php:4182)
FormAnswerController::parseFormResultFilterDate — hàm mới đọc ngày lọc (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::showFormResult — bản cũ, cùng pattern, KHÔNG sửa (app/Http/Controllers/Basic/FormAnswerController.php:4057)
is_image (app/Helpers/functions.php:9149)
FormAnswerItemRemind::userDeleted (app/FormAnswerItemRemind.php)
AddIndexFormCreatedToFormAnswerResultTable::up (database/migrations/2026_09_17_150000_add_index_form_created_to_form_answer_result_table.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FormAnswerController.php
   - database/migrations/2026_09_17_150000_add_index_form_created_to_form_answer_result_table.php
 • 4.2 Data ảnh hưởng:
   - form_answer_result — THÊM chỉ mục form_answer_result_form_deleted_created_index (form_id, deleted_at, created_at); không đổi dữ liệu, chỉ ALTER TABLE thêm chỉ mục phụ (nên chạy ngoài giờ cao điểm vì là bảng log lớn)
   - form_answer_item_remind — chỉ đọc, không đổi
   - line_user — chỉ đọc, không đổi
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) — màn xem kết quả trả lời biểu mẫu bản v3 nạp nhanh hơn; dữ liệu trả về giữ nguyên định dạng (tên/ảnh đại diện bạn bè, danh sách nhắc hẹn, điểm chẩn đoán, phân trang)
   - Friend Information (FA-015) — tên hiển thị và ảnh đại diện bạn bè trong danh sách kết quả nay lấy theo lô thay vì từng dòng (chỉ đọc 4 cột đang dùng)

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l cả 2 file đã sửa: No syntax errors detected; Boot Laravel (bootstrap/app.php + Console Kernel) trong worktree có vendor thật rồi in toSql câu truy vấn chính sau fix: giữ nguyên điều kiện form_id + phạm vi xóa mềm, phần lọc ngày đổi thành created_at >= '2026-07-01 00:00:00' và created_at <= '2026-09-17 23:59:59' (sargable), sắp xếp created_at desc, id desc; Gọi hàm đọc ngày mới qua Reflection: '2026.07.01' / '2026-07-01' / '2026/07/01' đều ra 2026-07-01 00:00:00 .. 23:59:59; chuỗi không hợp lệ trả null (rơi về cách lọc cũ); In SQL 2 truy vấn theo lô: whereIn mã bạn bè và whereIn mã kết quả (kèm withTrashed, order theo id); Kiểm JSON của nhóm nhắc hẹn sau groupBy + values: ra mảng [{...}] và [] khi không có dòng — giữ nguyên định dạng cũ cho giao diện; git diff --stat release_step_20260827...ai_small_41064: đúng 2 file (+164/-20)
   Bằng chứng: public/js/form_answer/form_result_v3.js:110 — giao diện gửi paginate = pagination.per_page với per_page mặc định 100, kèm order='created_at' nên vòng lặp chạy 100 lần mỗi request; database/migrations/2026_01_26_164427_create_form_answer_item_remind_table.php — bảng nhắc hẹn đã có chỉ mục form_result_id nên gom whereIn theo lô vẫn dùng được chỉ mục; database/migrations/2024_12_06_163107_add_form_answer_id_column_to_events_table.php — cột form_answer_id của bảng sự kiện KHÔNG có chỉ mục, nên truy vấn thừa đã xóa phải quét cạn bảng mỗi request; repo chỉ có 2 migration thêm chỉ mục cho form_answer_result (status_sync_sheet, status_sync_deleted) — không có chỉ mục nào phủ (form_id, created_at); MySQL dev (host.docker.internal:3306) và web dev (:8000) không kết nối được trong lần chạy này nên không EXPLAIN được trên dữ liệu thật — kết luận dựa trên định nghĩa chỉ mục trong migration của repo, giống cách đã làm ở #40997; resources/views/basic/form_answer/form_result_v3.blade.php — màn này không đọc trường type_file (giao diện tự nhận dạng theo đuôi tệp), nên phần đọc file chỉ giữ nguyên để không đổi dữ liệu trả về

■ TỰ REVIEW (AI)
Fix bám đúng nguyên nhân chậm (số lượng truy vấn theo dòng + truy vấn thừa + lọc ngày không dùng được chỉ mục) và giữ nguyên định dạng dữ liệu trả về nên giao diện không phải sửa. Rủi ro chính nằm ở câu ALTER thêm chỉ mục trên bảng log lớn, cần chạy ngoài giờ cao điểm.
 • Rủi ro / lưu ý khi test:
   - ALTER TABLE thêm chỉ mục trên form_answer_result là bảng log lớn — MySQL 5.7 thêm chỉ mục phụ không chặn đọc/ghi nhưng vẫn tốn thời gian và dung lượng; nên chạy ngoài giờ cao điểm hoặc bằng pt-online-schema-change (đã ghi chú trong migration)
   - Đổi lọc ngày sang so sánh khoảng thời gian: với chuỗi ngày hợp lệ kết quả giống hệt cách cũ; với chuỗi lạ mà thư viện thời gian vẫn đọc được theo nghĩa tương đối (ví dụ 'yesterday') thì phạm vi lọc sẽ khác cách cũ — giao diện chỉ gửi định dạng YYYY.MM.DD nên không ảnh hưởng thực tế
   - Giới hạn cột sắp xếp theo danh sách trắng: nếu sau này có nơi gọi truyền cột khác thì sẽ bị bỏ qua thay vì lỗi truy vấn — giao diện hiện chỉ gửi created_at

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41064 (nhánh gốc release_step_20260827, commit bed522fed1, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 12 phút 11 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=0baa38d7-97ca-43b4-9620-99c9c84628dd
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41064
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
