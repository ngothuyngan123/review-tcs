# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) — Assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `cecb9eddff` (sns-line, nhánh `ai_small_42006`) — không có link PR, chỉ có branch/commit do auto-fixbug push thẳng |
| Branch | `ai_small_42006` (base: `release_step_20260930_v2`) |
| Ngày submit đánh giá | 2026-10-05 (Journal #140022) |
| Auto-filled | 2026-10-05 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Điều kiện "chưa quét QR / chưa kết bạn qua landing" (`qr_condition=2`, nhánh AND) của bộ lọc bạn bè dùng `NOT IN` trên subquery bảng click landing KHÔNG khử trùng (1 người có nhiều dòng click). Từ MySQL 8.0.17, `NOT IN` ở mức AND được đổi thành antijoin và optimizer chọn plan quét lặp bảng click rất lớn (~31 triệu dòng) ⇒ cùng câu đếm 7s trên 5.7 thành ~50s trên 8.0. Nhánh này do #39121 đổi từ subquery đếm tương quan sang IN/NOT IN.

## 2. Cách fix

Nhánh "chưa quét QR" (`qr_condition=2`, mức AND) của bộ lọc bạn bè: đổi subquery `NOT IN` trên bảng click landing thành bảng dẫn xuất `SELECT DISTINCT line_id` (alias `qr_clicked`) để MySQL buộc materialize danh sách người đã quét 1 lần rồi loại trừ — đúng câu tối ưu ticket đã đo; giữ nguyên điều kiện lọc (`landing_id`, `line_id is not null`, `action=2`). Sửa ở `Conversation::advanceFilterPost` và bản mirror `ConversationReplicate`; các nhánh IN / group-by giữ nguyên. Quét ngang: nhánh IN (`qr_condition=0`), `qr_code_action` chưa đổi (ngoài phạm vi, ghi yokoten).

**[Tự review v1]** Bổ sung nhánh OR `qr_condition=2` (Conversation + mirror): nhóm OR chỉ 1 điều kiện "chưa quét QR" được Laravel sinh SQL ở mức AND ⇒ dính cùng antijoin trên MySQL 8.0 — nay cũng `NOT IN` trên bảng dẫn xuất DISTINCT (mirror giữ đúng điều kiện cũ không lọc action).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilterPost` — case qr_code nhánh AND (`app/Conversation.php`) | Sửa — đổi NOT IN sang bảng dẫn xuất DISTINCT | Đúng câu trong slow log |
| 2 | `Conversation::advanceFilterPost` — case qr_code nhánh OR (`app/Conversation.php`) | Sửa (bổ sung ở tự review v1) | Nhóm OR 1 điều kiện = mức AND, cũng dính antijoin |
| 3 | `ConversationReplicate::advanceFilterPost` — case qr_code nhánh AND (`app/ConversationReplicate.php`, mirror) | Sửa — đồng bộ với file chính | Bản sao của bộ lọc, phải giữ đồng bộ |
| 4 | Caller: `BotLineUser` / `BotLineUserPackage` / `FilterV2` (+Replicate) gọi `Conversation::advanceFilterPost` | Không sửa — chỉ đọc lại kết quả | Kiểm tra caller không bị ảnh hưởng ngữ nghĩa |
| 5 | `LineUserModel` (linect-service) | Không sửa | Điều kiện QR vẫn là subquery đếm tương quan, khác pattern, không bị bug này |
| 6 | Toàn bộ caller `Conversation::advanceFilterPost` (~27 file): Filter/Friendlist/CrossAnalysis/Broadcast(V2)/TalkList/Chat/RichMenu controllers, Api ListFriend/Remind/Mobile Filter, Mobile Calendar(Salon), Helpers/functions (remind), HelperService, CalendarSalonLineBookingService, console HandleExportCsv(2)/HandelCrossAnalysis(Screen)/HandleUpdateLatestInformationCsv/recoverShowFilterBroadcast | Không sửa | Chỉ đổi hiệu năng, kết quả không đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilterPost` — case `qr_code`, nhánh AND, `qr_condition=2` | `app/Conversation.php:537` | Direct | Đúng câu trong slow log gốc |
| F2 | `Conversation::advanceFilterPost` — case `qr_code`, nhánh OR, `qr_condition=2` | `app/Conversation.php:1233` | Direct | Bổ sung ở tự review v1 — cùng chuỗi `$in_string` dòng 1225 |
| F3 | `ConversationReplicate::advanceFilterPost` — case `qr_code`, nhánh AND, `qr_condition=2` (mirror) | `app/ConversationReplicate.php:492, 1109` | Direct | Bên ngoài chỉ gọi `ConversationReplicate::query()`; không có caller thực tế theo rà soát mã nguồn (xem NEW-3 ở file 04) |
| F4 | `qr_condition=3` ("chưa quét đủ N mã") | `app/Conversation.php:539, 1235` | Indirect (không sửa) | Subquery có GROUP BY … HAVING nên KHÔNG bị đổi thành antijoin — Dev chỉ kiểm, không sửa |
| F5 | ~27 caller của `Conversation::advanceFilterPost` | Filter/Friendlist/CrossAnalysis/Broadcast(V2)/TalkList/Chat/RichMenu controllers, Api ListFriend/Remind/Mobile Filter, Mobile Calendar(Salon), Helpers/functions (remind), HelperService, CalendarSalonLineBookingService, console HandleExportCsv(2)/HandelCrossAnalysis(Screen)/HandleUpdateLatestInformationCsv/recoverShowFilterBroadcast | Indirect | Chỉ đổi hiệu năng, kết quả không đổi theo Dev — cần TC verify lại vì đây chính là layer chứa bug gốc |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `detail_landing_click` (bảng click QR/landing) | READ-ONLY | Dev khẳng định "Không có — chỉ đổi cách viết câu SELECT, không ghi dữ liệu". Subquery chỉ đọc, không ghi |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Filter / Segment (SC-003) — điều kiện QR "chưa quét" mức AND trong bộ lọc bạn bè/phân đoạn (đếm & danh sách bạn bè, FilterV2, BotLineUser) | F1, F2, F3 | Medium — Dev nói "kết quả không đổi" nhưng đây chính là layer chứa bug gốc + plan optimizer MySQL 8.0 không ổn định (ticket ghi nhận lượt trước 746 dòng, lượt sau 178 triệu dòng cùng điều kiện) → cần TC verify kết quả số đếm/danh sách không đổi, không chỉ verify cú pháp SQL |
| T2 | QR Code Action / Landing (FA-017) | D1 | Low — dữ liệu landing chỉ được đọc, không đổi |
| T3 | Gián tiếp (chỉ hiệu năng, kết quả không đổi theo Dev): gửi tin theo bộ lọc (broadcast/remind), xuất CSV bạn bè, phân tích chéo, rich menu theo bộ lọc, lọc hội thoại (トークリスト), bộ lọc trên app mobile, lịch đặt chỗ salon | F5 | Low/Medium — nhiều caller dùng chung builder nên 1 lỗi ở F1/F2/F3 sẽ lan ra tất cả; nên có ít nhất 1 TC smoke cho mỗi nhóm caller chính (không cần lặp toàn bộ ma trận ở từng caller) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
