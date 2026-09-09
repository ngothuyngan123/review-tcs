# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: journal Redmine #38294 ngày 2026-07-07 của user **AI LME Fix bug** (báo cáo Auto-fixbug LME). Redmine **không có** section "Đánh giá ảnh hưởng" trong description — nội dung dưới đây parse từ journal.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (Auto-fixbug)` — journal 2026-07-03 ghi `plan: dev Tùng`; assigned_to hiện tại = `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | `commit d9807bde4e` (repo `sns-line`, 1 file) — không có link PR trong Redmine |
| Branch | `ai_fixbug_38294` (nhánh gốc `release_step_20260623`) — đã push lên origin |
| Ngày submit đánh giá | `2026-07-07` |
| Auto-filled | `2026-07-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Query đếm số bạn của modal lọc (lọc theo tag + ngày kết bạn) ở màn gửi tin hàng loạt / danh sách hội thoại chạy quá 300s. Hai nguyên nhân: (1) điều kiện ngày dùng hàm DATE(followed_at) bọc quanh cột nên MySQL không dùng được index, phải quét và tính hàm cho từng dòng; (2) điều kiện tag 'có tag'(>0)/'không tag'(=0) dùng subquery tương quan COUNT chạy lại cho TỪNG dòng và đếm hết mọi bản ghi tag của mỗi bạn thay vì dừng ngay khi thấy 1 bản ghi.

## 2. Cách fix

Sửa builder query lọc bạn `Conversation::advanceFilter` + `advanceFilterPost` (sns-line): (1) bỏ `whereDate(followed_at)`, đổi sang so sánh khoảng datetime sargable (`>= 'ngày 00:00:00'`, `<= 'ngày 23:59:59'`) để MySQL dùng được index và bỏ tính hàm DATE() mỗi dòng — áp cho cả nhóm điều kiện AND lẫn OR (ngày cố định + theo số ngày); (2) đổi điều kiện tag 'có tag'(count>0)→`EXISTS` và 'không tag'(count=0)→`NOT EXISTS` để dừng sớm, giữ nguyên loại 'đủ tất cả tag'(=N)/'thiếu tag'(!=N). Ngữ nghĩa không đổi (đã đối chiếu số liệu trên dev DB). Các bộ lọc `qr_code`/`conversion` cùng kiểu subquery đếm **còn tồn** (ghi yokoten).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilter` (app/Conversation.php) | Có — rewrite điều kiện ngày sargable + tag EXISTS/NOT EXISTS | Builder query lọc bạn gây treo |
| 2 | `Conversation::advanceFilterPost` (app/Conversation.php) | Có — rewrite tương tự | Builder query lọc bạn (nhánh POST) gây treo |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Redmine mục 4.1 ghi ở dạng **File thay đổi**, không tách F1/F2 — dưới đây map từ mục 3 + 4.1.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilter` | `app/Conversation.php` | Direct | Rewrite điều kiện ngày (sargable) + tag EXISTS/NOT EXISTS, cả nhánh AND lẫn OR |
| F2 | `Conversation::advanceFilterPost` | `app/Conversation.php` | Direct | Rewrite tương tự F1 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_line_user.followed_at` | READ (điều kiện lọc) | Chỉ ĐỌC, không ghi. DATETIME giây (không microsecond) → `23:59:59` bao trọn ngày |
| D2 | `tag_line_user.tag_id` / `tag_line_user.line_user_id` | READ (subquery EXISTS) | Chỉ ĐỌC, không ghi |
| — | — | — | **Không cần recover/migrate data** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Filter / Segment (SC-003) | F1, F2, D1, D2 | `<Redmine không ghi mức risk>` — tối ưu query đếm bạn của bộ lọc tag + ngày kết bạn, kết quả không đổi |
| T2 | Broadcast (FA-008) | F2, D1, D2 | `<Redmine không ghi mức risk>` — màn gửi tin hàng loạt gọi `advanceFilterPost` để đếm/dựng danh sách người nhận theo bộ lọc |
| T3 | Friend List (FA-013) | F1, D1, D2 | `<Redmine không ghi mức risk>` — danh sách bạn bè / danh sách hội thoại lọc theo cùng builder |

---

## Ghi chú nguyên văn từ báo cáo AI Auto-fixbug

**5. Recover data** — ✔ Không cần recover data.

**6. Verify** — Mức: `runtime-data`.
- `php -l app/Conversation.php`: No syntax errors.
- Đối chiếu trên dev DB (bot 542): OLD `count>0`=18 == NEW `EXISTS`=18; OLD `=0`=19 == NEW `NOT EXISTS`=19; OLD date range=5 == NEW sargable range=5 → ngữ nghĩa giống hệt.
- EXPLAIN: cả 2 dạng ngày đều dùng index `bot_id`; dạng sargable bỏ được tính `DATE()` mỗi dòng và cho phép dùng index composite `(bot_id, followed_at)` nếu DBA thêm.

**Rủi ro / lưu ý khi test (AI tự review)**
- `followed_at` là DATETIME giây (không microsecond) nên `'23:59:59'` bao trọn ngày — đúng ngữ nghĩa `DATE() <=`; nếu sau này đổi cột sang `datetime(6)` cần rà lại biên cuối ngày.
- Giá trị ngày từ modal luôn dạng `'Y-m-d'` (date picker) nên nối `' 00:00:00'` / `' 23:59:59'` an toàn.
- Khuyến nghị DBA thêm index composite `(bot_id, followed_at)` trên `bot_line_user` để tận dụng tối đa rewrite sargable (**không nằm trong patch code này**).

**Link tham chiếu**
- Phiên xử lý AI: `https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=ba27fbb6-c403-404d-9b94-d33d39153d05`
- Dashboard fixbug: `https://dashboard.melonglobal.net/fixbug-lme/?id=38294`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
