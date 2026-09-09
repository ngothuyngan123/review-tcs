# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> Nguồn: journal Redmine #127417 của **"AI LME Fix bug"** (2026-07-29 02:40) — báo cáo tự động hệ thống Auto-fixbug LME.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | repo **sns-line** @ commit `4c10d81570` (đã push). Không có URL PR trong Redmine. |
| Branch | `ai_small_39121` (nhánh gốc `release_step_20260623`) — 2 file thay đổi |
| Ngày submit đánh giá | `2026-07-29` |
| Auto-filled | `2026-07-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Câu SQL trong ticket do **bộ lọc bạn bè theo điều kiện QR/landing** sinh ra, dựng tại `Conversation::advanceFilterPost` (và bản dùng DB replica `ConversationReplicate`). Điều kiện QR được viết bằng **subquery ĐẾM CÓ THAM CHIẾU cột ngoài** (`line_user.line_id = detail_landing_click.line_id`) nên MySQL phải chạy lại subquery cho **TỪNG dòng bạn bè** của bot. Bảng `detail_landing_click` chỉ có index theo `landing_id`, **không có index theo `line_id`**, nên mỗi lần chạy lại phải quét toàn bộ lượt click của landing đó rồi mới so `line_id`. Độ phức tạp thành **(số bạn bè) × (số lượt click của landing)** nên bot lớn vượt 300 giây.

## 2. Cách fix

Viết lại điều kiện lọc QR/landing trong bộ lọc bạn bè: **bỏ subquery đếm có tham chiếu cột ngoài**, đổi sang **subquery ĐỘC LẬP** dạng `line_user.line_id IN / NOT IN (select line_id from detail_landing_click where landing_id in (...))` để MySQL dựng bảng tạm danh sách `line_id` **một lần** rồi tra, thay vì chạy lại phép đếm cho từng bạn bè.

Bốn lựa chọn của bộ lọc **giữ nguyên ý nghĩa**:
- **đã quét ít nhất 1 mã** → dùng `IN`
- **chưa quét mã nào** → dùng `NOT IN`
- **đã quét đủ tất cả mã** → dùng `IN` kèm `group by line_id having count(distinct landing_id) = số mã`
- **chưa quét đủ** → dùng `NOT IN` của cùng subquery đó

Áp cho **cả 6 chỗ**: `Conversation.php` và `ConversationReplicate.php`, nhánh `AND` lẫn nhánh `OR`, cả loại QR đăng ký bạn (`action=2`) lẫn loại QR thao tác trên web (`is_action_web`). Kèm **ép kiểu số nguyên** cho danh sách id landing trước khi ghép vào câu raw (chặn chèn SQL).

> Quét ngang thấy cùng kiểu subquery đếm còn ở điều kiện **kịch bản / chuyển đổi / thẻ** nhưng chúng đối chiếu theo cột số `line_user_id` và **ngoài phạm vi ticket** nên chưa sửa.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilterPost` — case `qr_code` + `qr_code_action` nhánh **AND** (`app/Conversation.php`) | Có (đổi cách dựng SQL) | Nơi sinh câu query lỗi |
| 2 | `Conversation::advanceFilterPost` — case `qr_code` + `qr_code_action` nhánh **OR** (`app/Conversation.php`) | Có | Nơi sinh câu query lỗi |
| 3 | `ConversationReplicate::advanceFilterPost` — case `qr_code` nhánh **AND** (`app/ConversationReplicate.php`) | Có | Bản replica (DB read) cùng logic |
| 4 | `ConversationReplicate::advanceFilterPost` — case `qr_code` nhánh **OR** (`app/ConversationReplicate.php`) | Có | Bản replica (DB read) cùng logic |
| 5 | `Conversation::advanceFilterPost` — khối join `line_user` theo `existFilterName` | Đã kiểm (không đổi) | `qr_code`/`qr_code_action` vẫn nằm trong danh sách bắt buộc join `line_user` → điều kiện mới vẫn hợp lệ |
| 6 | `FilterV2::getFilterUser` / `BotLineUser` / `BroadcastController` / `TalkListController` / `FilterController` / `ChatController` | Chỉ rà nơi gọi, **không sửa** | Xác nhận caller không phụ thuộc cấu trúc câu SQL cũ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilterPost` (case qr_code/qr_code_action, nhánh AND + OR) | `app/Conversation.php` | Direct | Đổi cách dựng subquery QR/landing |
| F2 | `ConversationReplicate::advanceFilterPost` (case qr_code, nhánh AND + OR) | `app/ConversationReplicate.php` | Direct | Bản replica đọc DB, cùng logic |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(Không có)* | — | Chỉ đổi câu truy vấn **đọc**, **không ghi/sửa** dữ liệu, **không đổi cấu trúc bảng**. Đọc từ `detail_landing_click` (action, landing_id, line_id) + `line_user`, `bot_line_user`. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Filter / Segment (SC-003)** — điều kiện lọc theo mã QR/landing | F1, F2 | High — đổi cách dựng SQL, kết quả lọc **phải** giữ nguyên |
| T2 | **Friend List (FA-013)** — màn danh sách bạn bè | F1 | Medium — dùng bộ lọc để đếm & liệt kê bạn |
| T3 | **QR Code Action / Landing (FA-017)** | F1, F2 | Medium — nguồn dữ liệu lượt quét/thao tác landing được đọc bởi điều kiện lọc |
| T4 | **Broadcast / Step message / Auto reply / Action schedule / Cross analysis** (ngoài glossary) | F1, F2 | Medium — dùng chung bộ lọc bạn bè qua `advanceFilterPost` → cùng hưởng cải thiện tốc độ **và cùng chịu rủi ro nếu lệch kết quả lọc** |

---

## 5. Thông tin bổ sung từ báo cáo Dev (không có trong template — GIỮ để scope TC)

### §5 Recover data
- ✔ **Không cần recover data** (chỉ đổi query đọc).

### §6 Verify (Dev đã làm)
- **Mức: lint.** `php -l app/Conversation.php` + `php -l app/ConversationReplicate.php`: No syntax errors.
- Render thử chuỗi SQL sinh ra: câu `IN`/`NOT IN` + `group by ... having` đúng cú pháp; id landing bị ép kiểu số (test chuỗi chèn SQL trả về `477033`).
- `git diff --stat release_step_20260623...ai_small_39121`: chỉ **2 file** đã sửa.
- Bằng chứng: migration gốc `2020_06_15_182615` của `detail_landing_click` chỉ index `landing_id`, **không có index `line_id`** → đúng triệu chứng quét lặp. `detail_landing_click.line_id` **NULL được** → đã thêm `line_id is not null` để `NOT IN` không bị NULL nuốt kết quả. `line_user.line_id` NOT NULL → vế ngoài an toàn.
- ⚠️ **CHƯA chạy được EXPLAIN / đo thời gian thật**: MySQL dev `host.docker.internal:3306` báo *Connection refused* trong container lúc xử lý.

### Rủi ro / lưu ý khi test (Dev tự review — QUAN TRỌNG cho TC)
1. Hiệu quả phụ thuộc việc MySQL **materialize** subquery `IN`/`NOT IN` (mặc định bật từ 5.6). Nếu **prod tắt materialization** → tốc độ có thể không cải thiện như kỳ vọng → **đo EXPLAIN sau deploy trên bot lớn**.
2. Chưa đo được thời gian thật → **QA/DBA chạy lại câu lọc trên bot của khách, so số bạn bè trước/sau** để chắc kết quả không lệch.
3. Khuyến nghị DBA (ngoài diff): thêm index tổ hợp `detail_landing_click(landing_id, line_id)` hoặc `(landing_id, action, line_id)` — bảng rất lớn, DBA chạy giờ thấp điểm, **không** đưa vào migration tự động.
4. Trường hợp **danh sách mã QR gửi lên rỗng** vẫn sinh câu `in ()` lỗi cú pháp **như code cũ** — giữ nguyên hành vi, không xử lý trong ticket này.
5. Nhánh **OR của bản replica** vốn không lọc cột `action` → giữ nguyên, không tự siết thêm.
6. Giữ nguyên `distinct` → trường hợp danh sách mã bị trùng cho kết quả như cũ.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
