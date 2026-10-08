# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) — Assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `5bc4e1e617` (sns-line, nhánh `ai_small_41442`) — không có link PR, chỉ có branch/commit do auto-fixbug push thẳng |
| Branch | `ai_small_41442` (base: `release_step_20260827`) |
| Ngày submit đánh giá | 2026-09-25 (Journal #138332) |
| Auto-filled | 2026-10-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bảng lỗi phát hành (`message_error`) là bảng log dùng chung của toàn hệ thống nhưng chỉ có chỉ mục theo cột `bot_id` nên mọi truy vấn của màn này đều phải đọc lần lượt toàn bộ số dòng của bot. Hai truy vấn chạy ở **CUỐI MỌI lần xoá** (đếm lại tổng lỗi chưa xác nhận để cập nhật số thông báo, và tìm lỗi chưa xác nhận mới nhất của bot) vì thế chậm kể cả khi người dùng chỉ xoá một dòng — riêng câu tìm lỗi mới nhất còn có thể bị chọn cách chạy quét ngược khoá chính, nên khi bot vừa bị xoá sạch lỗi thì phải quét ngược gần như cả bảng mới biết là không còn kết quả. Ngoài ra nhánh bấm "chọn tất cả" nạp toàn bộ bản ghi lỗi của bot thành đối tượng, kèm nối thừa bảng tin nhắn, nạp kèm quan hệ người dùng LINE và sắp xếp, chỉ để lấy ra danh sách id; với hai tab đã đặt lịch gửi lại thì mỗi bản ghi còn chạy riêng ba câu lệnh nên số truy vấn tăng tuyến tính theo số lỗi được chọn.

**(Vòng 3 — bổ sung sau khi Journal #138290 gắn thêm endpoint `/ajax/get-message-error`):** phần LẤY DANH SÁCH lỗi trước đây mỗi lần mở/đổi tab tốn hàng trăm câu lệnh — tab "chưa xác nhận" chạy 5 câu đếm riêng mỗi câu quét lại toàn bộ khối lỗi của bot; phần dựng nội dung hiển thị cho từng dòng tự chạy 3-8 câu lệnh/dòng (tra bảng tin nhắn mới/cũ/tách theo năm, ảnh chụp mẫu, tên chiến dịch/kịch bản) mà màn mặc định 100 dòng/trang nên 1 lần mở trang bắn ra vài trăm câu lệnh; tab "đã đặt lịch" không lọc sẵn theo điều kiện đã có lịch gửi nên quét cả khối lỗi chưa đặt lịch (chiếm gần hết bảng).

## 2. Cách fix

**Vòng 1** (release trước, giữ nguyên ở lần note này): sửa hàm xoá lỗi phát hành để nhánh "chọn tất cả" lấy danh sách id bằng `pluck` thay vì nạp toàn bộ đối tượng kèm quan hệ người dùng LINE, bỏ nối thừa bảng tin nhắn và bỏ sắp xếp (không ảnh hưởng kết quả); ép kiểu danh sách id nhận từ client về mảng; gom ba câu lệnh/dòng của 2 tab đã đặt lịch gửi lại thành truy vấn hàng loạt theo lô 1000; xoá hàng loạt cũng chia lô 1000; thêm chỉ mục `(bot_id, is_confirmed, id)` cho 2 truy vấn chạy ở cuối mọi thao tác xoá.

**Vòng 2** (giữ nguyên): bổ sung chỉ mục thứ hai `(bot_id, sending_schedule_id, type, status)` cho bảng `message_error` để câu lấy danh sách id khi bấm "chọn tất cả" chạy hoàn toàn trên chỉ mục, không còn phải đọc từng dòng dữ liệu của bot.

**Vòng 3** (lần fix này — theo spec bổ sung sau Journal #138290): tối ưu phần LẤY DANH SÁCH (`/ajax/get-message-error`). Ba việc, KHÔNG thêm chỉ mục mới (2 chỉ mục vòng 1-2 đã phủ đúng phần đầu điều kiện lọc):
1. Tab "chưa xác nhận": 5 câu đếm riêng (4 ô đếm theo loại + tổng số dòng không ở trạng thái gửi lại, cùng bộ điều kiện) → gộp thành **MỘT câu đếm nhóm theo loại** rồi tách số trong PHP — còn đúng 1 lượt quét, các con số trả về giữ nguyên.
2. Phần dựng nội dung hiển thị từng dòng (nội dung tin nhắn, ảnh chụp mẫu, tên chiến dịch/kịch bản) → mọi tra cứu được **nạp trước theo lô** rồi mới gán vào từng dòng (thay vì 3-8 câu/dòng) — một trang 100 dòng chỉ còn khoảng chục câu lệnh, giá trị gán giữ nguyên. Tab lịch sử gửi cũng bỏ được 1 câu lệnh/dòng theo cách tương tự.
3. Tab "đã đặt lịch": bổ sung điều kiện chỉ lấy dòng **ĐÃ có lịch gửi** — điều kiện cũ đã loại sẵn dòng chưa đặt lịch nên kết quả không đổi, nhưng truy vấn chỉ đọc phần nhỏ của chỉ mục thay vì cả khối lỗi chưa đặt lịch.

**[Tự review v1 — Vòng 3]** Bổ sung nhánh OR không áp dụng ở ticket này (khác ticket #42006) — ghi chú để tránh nhầm: phần tự-review của Vòng 3 xác nhận bảo toàn hành vi theo 3 hướng (câu đếm gộp giữ nguyên từng điều kiện lọc cũ; vòng dựng nội dung giữ nguyên thứ tự/nhánh rẽ cũ kể cả 2 chi tiết tinh tế — bảng tin nhắn tách theo năm lấy theo năm của DÒNG LỖI, và đổi pdf→text nằm SAU khối xử lý tin dạng text; điều kiện tab đã đặt lịch không đổi tập kết quả). **Cố ý KHÔNG làm**: (i) thêm chỉ mục thứ 3 để bỏ bước sắp xếp — chưa EXPLAIN được trên dữ liệu thật; (ii) tự dựng lại object phân trang; (iii) gom thêm các tra cứu ngoài phạm vi endpoint.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MessageErrorController::ajaxDeleteErrorMessage` (`app/Http/Controllers/Basic/MessageErrorController.php:720`) | Sửa — Vòng 1: pluck id, bỏ nối/sắp xếp thừa, batch 1000 | Nhánh "chọn tất cả" + xoá hàng loạt chậm |
| 2 | `MessageErrorController::removeSendingScheduleOfMessageErrors` (`:811`) | Sửa — Vòng 1: gom 3 câu/dòng → batch 1000 | 2 tab đã đặt lịch gửi lại |
| 3 | `recountTotalMsgErrorNotifySetting` (`app/Helpers/functions.php:4681`) | Không sửa logic, hưởng lợi từ chỉ mục mới | Chạy ở cuối mọi lần xoá — 1 trong 2 câu chậm gốc |
| 4 | `lastErrorMessage` (`app/Helpers/functions.php:4430`) | Không sửa logic, hưởng lợi từ chỉ mục mới | Tìm lỗi chưa xác nhận mới nhất — câu chậm gốc còn lại, cũng được gọi từ header admin (cache 5p) |
| 5 | `MessageError` model + hằng `STATUS_RETRY_WAIT`/`STATUS_RETRY_SENDING`/`TYPE_*` (`app/MessageError.php`) | Không sửa | Tham chiếu hằng, không đổi |
| 6 | `SendingScheduleSetting` model (`app/SendingScheduleSetting.php`) | Không sửa | Không có xoá mềm/observer — xoá batch an toàn |
| 7 | `callApiDeleteMessage` / `select_all_page` (`public/js/error_list/index_v2.js:289`) | Không sửa | Xác nhận: tick "chọn tất cả" = chọn TOÀN BỘ bản ghi của bot, không chỉ trang hiện tại |
| 8 | `table-unconfirm.blade.php` + `table-registered.blade.php` (ô chọn tất cả bind `select_all_page`) | Không sửa | Nguồn phát sinh request nạp toàn bộ bản ghi |
| 9 | Migration `AddPerformanceIndexesToMessageErrorTable` (`database/migrations/2026_09_24_100000_add_performance_indexes_to_message_error_table.php`) | Sửa — thêm 2 chỉ mục (Vòng 1 + Vòng 2 cùng 1 file, chưa release nên đổi tên an toàn) | Chỉ mục `(bot_id, is_confirmed, id)` + `(bot_id, sending_schedule_id, type, status)` |
| 10 | `MessageErrorController::ajaxGetMessageError` (`:164`) — Vòng 3 | Sửa — gộp câu đếm + nạp trước theo lô | Endpoint `/ajax/get-message-error`, đúng endpoint ticket gắn thêm |
| 11 | `MessageErrorController::getListHistorySend` (`:61`) — Vòng 3 | Sửa — bỏ 1 câu lệnh/dòng | Tab lịch sử gửi, đi qua cùng endpoint (`ajaxGetMessageError` chuyển tiếp sang hàm này) |
| 12 | `countUnConfirmErrorByType` / `errorTypeKey` / `errorTypeKeyOfType` (mới) — Vòng 3 | Thêm mới | Thay 5 câu đếm cũ bằng 1 câu đếm nhóm theo loại |
| 13 | `attachContentToMessageErrors` / `fetchByIds` / `parseTemplateIds` / `firstTemplateOf` / `firstCaptureTemplateId` / `messageModelOfYear` (mới) — Vòng 3 | Thêm mới | Nạp trước theo lô nội dung tin/mẫu/chiến dịch/kịch bản cho từng trang |
| 14 | `getEndCode` + `checkIsJson` (thuần PHP, không truy vấn) — Vòng 3 | Không sửa | Không chạm DB |
| 15 | `PaginationResource` (`app/Http/Resources/PaginationResource.php`) | Không sửa | Khoá phân trang FE dùng — Dev cố ý không tự dựng lại |
| 16 | `public/js/error_list/index_v2.js:141 initDataError` | Không sửa | Nơi gọi endpoint, xác nhận `per_page` mặc định 100 — lý giải vì sao 1 trang bắn hàng trăm câu lệnh trước fix |
| 17 | `MessagesV2` / `Messages` / `Messages2020..2025` / `Template` / `SourceMessage` / `CaptureTemplate` / `BroadCast` / `StepMessage` | Không sửa, chỉ đọc (nạp theo lô) | Không có global scope, không đổi bảng/kết nối |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MessageErrorController::ajaxDeleteErrorMessage` — endpoint `/ajax/delete-message-error` | `app/Http/Controllers/Basic/MessageErrorController.php:720` | Direct | Endpoint gốc ticket (max 93s). Vòng 1: pluck id, bỏ nối/sắp xếp thừa, batch 1000 |
| F2 | `MessageErrorController::removeSendingScheduleOfMessageErrors` | `:811` | Direct | Vòng 1: gom 3 câu/dòng của 2 tab đã đặt lịch → batch 1000 |
| F3 | `recountTotalMsgErrorNotifySetting` | `app/Helpers/functions.php:4681` | Indirect | Hưởng lợi từ chỉ mục mới `(bot_id, is_confirmed, id)` — chạy ở cuối mọi lần xoá |
| F4 | `lastErrorMessage` | `app/Helpers/functions.php:4430` | Indirect | Hưởng lợi từ chỉ mục mới — còn được gọi từ header admin mọi trang (cache 5 phút), ORDER BY id DESC LIMIT 1 có rủi ro quét ngược khoá chính dù có index (Dev tự nêu ở mục 6) |
| F5 | `MessageErrorController::ajaxGetMessageError` — endpoint `/ajax/get-message-error` | `:164` | Direct | Vòng 3 — endpoint gắn thêm qua Journal #138290. Gộp 5 câu đếm → 1 câu nhóm theo loại |
| F6 | `MessageErrorController::getListHistorySend` (tab Lịch sử gửi) | `:61` | Direct | Vòng 3 — đi qua cùng `ajaxGetMessageError`, bỏ 1 câu lệnh tra mẫu tin/dòng |
| F7 | `countUnConfirmErrorByType` / `errorTypeKey` / `errorTypeKeyOfType` (mới) | `MessageErrorController.php` | Direct (mới) | Vòng 3 — thay 5 câu đếm cũ |
| F8 | `attachContentToMessageErrors` / `fetchByIds` / `parseTemplateIds` / `firstTemplateOf` / `firstCaptureTemplateId` / `messageModelOfYear` (mới) | `MessageErrorController.php` | Direct (mới) | Vòng 3 — nạp trước theo lô nội dung hiển thị từng dòng (tab Đã đặt lịch cũng dùng) |
| F9 | Tab "Đã đặt lịch" (chưa gửi) — điều kiện lọc bổ sung trong `ajaxGetMessageError` | `MessageErrorController.php:164` | Direct | Vòng 3 — thêm điều kiện chỉ lấy dòng ĐÃ có lịch gửi, Dev khẳng định không đổi kết quả |
| F10 | Admin Header / Notification Badge (ngoài glossary — gọi `lastErrorMessage`) | `layout/basic/header.blade.php:978`, `layout/admin_v2/header.blade.php:884` | Indirect | Cache 5 phút — mọi trang quản trị đều gọi, nhẹ đi theo F4, nội dung hiển thị không đổi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `message_error` — thêm chỉ mục `(bot_id, is_confirmed, id)` | MIGRATE (thêm index) | Không đổi cột/dữ liệu, chỉ chỉ mục. Chi phí ghi thêm nhỏ khi phát sinh lỗi mới |
| D2 | `message_error` — thêm chỉ mục `(bot_id, sending_schedule_id, type, status)` | MIGRATE (thêm index) | Idem — Vòng 2 |
| D3 | `message_error` — hàng bị xoá khi xoá lỗi phát hành | DELETE (theo lô 1000) | Dev khẳng định tập bản ghi bị xoá KHÔNG đổi, chỉ chia lô |
| D4 | `sending_schedule_setting` — hàng bị xoá khi gỡ lịch gửi lại | DELETE (batch) | Không có xoá mềm/observer → xoá batch tương đương xoá từng đối tượng. 2 quy tắc tinh tế giữ nguyên: chỉ gỡ lịch gửi còn tồn tại; nhiều lỗi cùng trỏ 1 lịch thì chỉ lỗi đầu được gỡ |
| D5 | `notify_setting` — 3 cột tổng số lỗi | UPDATE | Không đổi cách tính, chỉ câu đếm đầu vào chạy nhanh hơn |
| D6 | Vòng 3 (`/ajax/get-message-error`) | READ-ONLY | Dev khẳng định không đụng dữ liệu — chỉ đổi cách LẤY dữ liệu, không thêm/bớt cột/index/bản ghi. Các con số trả về (4 ô đếm theo loại, tổng dòng không ở trạng thái gửi lại, tổng bản ghi + số trang) tính từ cùng bộ điều kiện cũ → giá trị không đổi |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Delivery Error List (FA-028) — xoá lỗi (1 dòng / nhiều dòng / chọn tất cả) ở cả 3 tab | F1, F2, D1-D4 | Medium — tập dữ liệu bị xoá + số đếm hiển thị Dev khẳng định không đổi, nhưng đây chính là code path chứa bug gốc + chưa EXPLAIN được trên dữ liệu thật → cần TC verify cả đúng-kết-quả và thời gian |
| T2 | Delivery Error List (FA-028) — các thao tác khác cùng màn (xác nhận lỗi, đặt lịch gửi lại, job đặt lịch chạy nền) | F3, D5 | Low — chỉ dùng chung hàm đếm, không đổi logic riêng |
| T3 | Admin Header / Notification Badge (ngoài glossary) | F4, F10 | Low — chỉ hiệu năng, nội dung hiển thị không đổi theo Dev; nhưng chạy trên MỌI trang quản trị nên 1 sai sót ở F4 sẽ lan rộng |
| T4 | Delivery Error List (FA-028) — xem danh sách (mở màn / đổi tab / đổi loại lỗi / chuyển trang) | F5, F7, F8, D6 | Medium — đây là phần Vòng 3 mới sửa (endpoint gắn thêm sau), nội dung dòng + số đếm Dev khẳng định giữ nguyên nhưng refactor sâu (gộp câu đếm, nạp trước theo lô) → cần TC verify từng loại nội dung hiển thị (tin nhắn các bảng/năm khác nhau, ảnh chụp mẫu, tên chiến dịch/kịch bản, mã lỗi kết thúc) không lệch |
| T5 | Delivery Error List (FA-028) — tab Lịch sử gửi (đã gửi) | F6 | Low/Medium — cùng endpoint Vòng 3, bớt 1 câu lệnh/dòng |
| T6 | Delivery Error List (FA-028) — tab Đã đặt lịch (chưa gửi) | F9 | Medium — thêm điều kiện lọc mới (dù Dev khẳng định không đổi kết quả) → nên có TC boundary cho dòng vừa có/vừa không có lịch gửi để xác nhận không bị loại sai |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
