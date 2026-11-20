<!-- generated: /pick-maincase 2026-11-19 · pool: 04-tc-list.md (MCP LME TEST STUDIO — task_id=560, lượt B, lọc REQ-X-41718-*) + §7 05-review-report.md · phạm vi: chỉ #41718 (1/3 ticket của lượt B) -->
# 06 — Main cases · #41718 Packets out of order khi đọc `calendar_salon_line_booking`

> Sprint cha #45229 · nhóm T15 · lượt B. Folder cha (`2026-11-16_45229_sprint-fix-bug-bao-mat-hieu-nang-php-web`) chỉ có file 04 dạng INDEX, không có dòng TC → pool lấy từ folder lượt B này. Đặt tên file kèm `.41718` vì lượt B gồm 3 ticket (#41717 · #41529 · #41718).

## 0. Tóm tắt

| Mục | Giá trị |
|---|---|
| Loại task | Fix bug — exception production do AI phát hiện (2 mẫu SQL: xoá bạn bè đã chặn · lệnh `recover:payment_univapay_timeout`). ⚠️ Không có commit riêng, Dev chưa xác định nguyên nhân → main case = chứng minh không tái hiện + chặn regression ở luồng có code đổi trong sprint (`FriendlistController`, `block.js` / `user_block.js`, `config/queue.php`) |
| Bộ TC | 7 TC của #41718 (04-tc-list.md: 4 · §7 chưa trên tool: 3 · 04-tc-write chưa push: không áp dụng) |
| Main case | 5 TC (71% bộ TC #41718 · 29% của 17 TC lượt B) · Bắt buộc sau release: 1 |
| Slot chưa có main case | 1 (B5 — có điều kiện) |
| Input thiếu | Dev không viết đánh giá ảnh hưởng cho #41718 (03 lượt B ghép từ Studio) · nguyên nhân gốc chưa xác định (05 §1 G4) · Studio: chỉ đọc `requirements` (`REQ-X-41718`, `-01`, `-02`); không đọc `dev_impact` vì ở mức sprint 743 file và #41718 không có commit riêng |

Tỉ lệ 71% vượt mức gợi ý ~20% vì pool của 1 ticket chỉ có 7 TC; đã rà lại, mỗi case giữ một slot riêng, không case nào thuộc danh sách loại trừ.

## 1. Main cases (5)

| # | TC ID | Slot | Tên case | Surface | Môi trường chạy | Sau release | Tiêu chí đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 1 | TC-DATAREF001-01 (chưa trên tool) | B1a | Xoá từng người + hàng loạt ở ブロックされた友だち khi bạn bè có đơn salon: xoá đủ đơn, bot B không bị chạm, không lỗi DB | web | dev, local, prd, staging | Không — xoá dữ liệu bạn bè; prd do #5 kiểm | C1 `REQ-X-41718-01` · F5 · D1 · `user_block.js` đổi trong sprint · C2 `DATA-REF-001` / `DATA-DB-001` Cao · C3 loại chặn phổ biến (bạn bè tự chặn bot) · C4 DB + 予約管理 bot A / B | Exception mẫu 1 (`select … where line_user_id … and bot_id …`) · Có đối chứng F07 + bot B, phần NEW-697 còn thiếu · Expected xoá đơn salon khớp spec `friend-list/feature-spec.md` L278 |
| 2 | NEW-699 | B1b | Lệnh khôi phục đơn thanh toán quá hạn chạy 2 lượt với đơn salon chờ webhook: exit 0, không lỗi giao thức DB, đơn đối chứng không bị đụng | job | LOCAL · đề xuất: dev, local, staging (seed DB + chạy artisan tay); phần prd của RULE-08 do #5 kiểm | Không — seed DB, chạy lệnh tay | C1 `REQ-X-41718-02` · F6 · exception mẫu 2 · C2 `JOB-001` Cao (job + thanh toán) · C4 trạng thái đơn trong DB + log · Đạt 13/11 | ⚠️ `CONF-SPEC` C1 chưa chốt (`status_webhook` 3/4 không có trong spec) · Xem §4 |
| 3 | NEW-700 | B2 | Queue worker: DB đóng kết nối do `wait_timeout` giữa 2 job salon ⇒ job sau vẫn xử lý xong, đơn 2 huỷ đúng | job | LOCAL · đề xuất: dev, local, staging (đổi `wait_timeout` GLOBAL, ảnh hưởng server) | Không — đổi cấu hình MySQL global | C1 `REQ-X-41718-02` · F7 `config/queue.php` đổi trong sprint · giả thuyết nguyên nhân của Studio · C2 `ENV-001` Cao · C4 `failed_jobs` + trạng thái đơn | TC duy nhất kiểm giả thuyết kết nối bị đóng · Dev xác định nguyên nhân khác thì phải chọn lại slot này |
| 4 | NEW-697 | B4 | Xoá hàng loạt 30 bạn bè ở ブロックした友だち có đơn salon: xoá đủ dữ liệu, không 500 / lỗi giao thức DB | web | LOCAL · đề xuất: dev, local, staging (seed 30 bạn bè trong DB) | Không — seed DB + xoá dữ liệu | C1 `REQ-X-41718-01` · F5 · caller khác của `deleteUserBlockAction` (EP-15 dùng chung SCR-FRL-04/05/06) · `block.js` đổi trong sprint · C2 `DATA-REF-001` Cao · C4 DB 30 bạn bè + log · Đạt 13/11 | Xem §4 (thiếu bot khác) |
| 5 | TC-ENV003-02 (chưa trên tool) | B6 | 7 ngày sau release không còn `Packets out of order` ở 2 câu SQL đọc đơn salon; lệnh chạy đủ 288 lượt/ngày, 0 lượt lỗi DB | job, web | prd | Bắt buộc — exception chỉ thấy trên prd | C1 BUG #41718 cả 2 mẫu · C2 `ENV-003` Cao · C5 đúng hạ tầng `step.lme.jp` · bằng chứng duy nhất cho G4 tới khi Dev xác định nguyên nhân | `manual` vì chỉ chạy được trên production · Cần Dev lấy log lệnh ngày thứ 7 |

**TC trong pool không chọn (2):**
- NEW-698: kịch bản xoá từng người đã nằm trong #1, và tiền đề chặn sai màn (xem §4).
- TC-DATAREF001-02: Abnormal ghép 2 luồng (xoá bạn bè trong lúc đơn đang chờ webhook). Không có trong tập nhỏ nhất; chạy ở vòng regression đầy đủ.

## 2. Slot chưa có main case (1)

| # | Slot | Case cần có | Surface | Expected cốt lõi | Môi trường |
|---|---|---|---|---|---|
| 1 | B5 (có điều kiện) | Đối soát dữ liệu của ca lỗi production: Dev/DBA query trên `step.lme.jp` theo `line_user_id = 62856142` + `bot_id = 108684` (exception 2026-09-28 → 29) các bảng trong cascade `deleteUserBlock()`: `bot_line_user`, `conversation`, `tag_line_user`, `form_answer_result`, `calendar_salon_line_booking`, `friend_information_value`. Exception bắn ở bước đọc đơn salon (bước 9/11 của cascade, spec L278); spec L679 ghi "cần đảm bảo transaction" nhưng chưa xác nhận có transaction | web | Dữ liệu bạn bè đó ở bot 108684 hoặc đã xoá hết ở mọi bảng, hoặc còn nguyên ở mọi bảng. Không có trạng thái xoá dở (vd `bot_line_user` đã mất nhưng `calendar_salon_line_booking` còn). Nếu bị xoá dở thì Recover data và đối soát các ca khác cùng signature (RULE-04) | prd — chạy 1 lần trước release. Dev xác nhận cascade chạy trong 1 transaction thì bỏ slot |

## 3. Slot không áp dụng

| Slot | Lý do |
|---|---|
| B3 | Không có điểm sửa cho #41718 (không commit riêng). Lệnh `recover:payment_univapay_timeout` không đổi code (03 mục 3 #5) và đã được kiểm ở B1b |

## 4. TC cần sửa trước khi chạy

| TC ID | Vấn đề | Cần sửa |
|---|---|---|
| NEW-699 | (1) `status_webhook = 3 / 4` trong tiền đề trái spec `salon-booking/db/db-mapping.md` L105 (0/1/2), CONF-SPEC C1 chưa chốt. (2) Expected chỉ nói đơn đối chứng không bị đụng; chưa nói 5 đơn quá hạn phải đổi sang trạng thái gì sau lệnh, tức chỉ kiểm "hết lỗi". (3) Mã `JOB-002` không có trong checklist | Dev chốt giá trị `status_webhook` và quy tắc xử lý đơn quá hạn, rồi thêm expected trạng thái cuối của 5 đơn. Đổi mã thành `JOB-001` |
| NEW-697 | B4 kỳ vọng "dữ liệu bot khác không đổi" nhưng tiền đề không dựng dữ liệu của 30 bạn bè ở bot khác, nên B4 luôn Đạt (05 §5 I5) | Thêm vào tiền đề: 3/30 bạn bè cũng là bạn của bot test thứ 2, mỗi người 1 đơn salon ở bot đó. Đổi mã thành `DATA-REF-001` |
| NEW-700 | Tiền đề tạm đổi `QUEUE_CONNECTION=database`; chưa rõ prd dùng driver queue nào (`config/queue.php` đổi ở T21 #45230) | Dev xác nhận driver queue của prd; nếu khác `database` thì chạy NEW-700 trên đúng driver đó |
| NEW-698 (không chọn) | Tiền đề cho user chặn bot bằng app LINE (sẽ hiện ở ブロックされた友だち `/user-block`, `blocked_by = 0` — spec L339), nhưng bước 1 mở `/basic/friendlist/block` (ブロックした友だち = admin chặn) | Đổi bước 1 sang `/basic/friendlist/user-block`, hoặc đổi tiền đề thành admin chặn bạn bè |
