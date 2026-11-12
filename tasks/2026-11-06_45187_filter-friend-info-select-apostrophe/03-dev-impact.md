# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Section "Đánh giá ảnh hưởng" KHÔNG nằm trong Description Redmine mà nằm ở **Journal #151339 — Dev Studio (Dev handoff) — 2026-11-05**. Nội dung dưới đây parse nguyên văn từ journal đó (+ bổ sung D-1/D-2/D-3 từ Journal #151323).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Văn Dũng Đinh (DungDV) |
| Commit / Pull Request | Không có link PR trong Redmine — commit `75f5c82380d31ee57c22af1f71fd2618d14c22f4` (gốc `release-t09-2026` @`a3ce3af2d76b`), service `java-job` (linect-service); cherry-pick riêng commit `75f5c8238` sang `release-callback-t09-2026` — do DungDV thực hiện sau |
| Branch | `ai_studio_fixbug_45187` |
| Ngày submit đánh giá | 2026-11-05 (Journal #151339, 14:07) |
| Auto-filled | 2026-11-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (ở đây là Journal #151323 + #151339) và xác nhận đầy đủ 4 mục.

---

## 1. Nguyên nhân

Trong `LineUserModel`, hai hàm dựng điều kiện lọc (AND: `buildWhereFilter`, OR: `buildWhereORFilter`) tạo mệnh đề `IN` cho friend info dạng select và cho tỉnh bằng cách ghép thẳng giá trị option vào SQL trong dấu nháy đơn. Option do khách tự nhập có dấu `'` (ví dụ `⑧Farmer's Chicken札幌山鼻店`) làm câu SQL sai cú pháp, MySQL báo `SQLGrammarException`. Các nhánh khác trong hai hàm này đã bind tham số qua `?`, chỉ 8 chỗ `IN` này ghép chuỗi (đồng thời là lỗ **SQL injection**).

Vị trí cụ thể (branch gốc `staging-t10-2026`, commit `0475e7081`):
- `buildWhereFilter` (AND): `friend_information_value.value IN` — line 1021, 1024; `line_user.province IN` / `NOT IN` — line 965, 967
- `buildWhereORFilter` (OR): `friend_information_value.value IN` — line 1846, 1849; `line_user.province IN` / `NOT IN` — line 1790, 1792

## 2. Cách fix

Theo Journal #151323 (Dev Studio · Hướng sửa):
- **D-1** Thêm helper `buildInPlaceholders` trong `LineUserModel`.
- **D-2** Thay 8 chỗ ghép chuỗi `IN` bằng placeholder đã bind (`?`, giá trị truyền qua `whereArgsStock` / `query.setParameter`).
- **D-3** Unit test không chạm DB cho mệnh đề `IN`.

Nội dung thay đổi thực tế (Journal #151339):
- Job FilterV2 (dùng chung cho broadcast, action, action schedule, kịch bản, nhắc lịch event, auto-reply/postback/rich menu, export CSV, cross analysis): điều kiện friend info dạng select (含む / 含まない) không còn crash khi option chứa dấu nháy đơn.
- Điều kiện tỉnh (province) thuộc / không thuộc: giá trị được bind tham số; "không thuộc" vẫn gồm người chưa có tỉnh.
- Log `#isValidFilterV2` / `#getListLineUserFromFilterV2` nay in `IN (?,?)` và các option nằm trong danh sách args sau `==>`.
- **Hành vi lỗi cũ GIỮ NGUYÊN — cố ý không đổi trong ticket này**: `isValidFilterV2` trả `true` khi query lỗi (tin/action vẫn chạy cho người không khớp filter); `getListLineUserFromFilterV2` trả list rỗng khi lỗi.
- **Các builder FilterV2 vẫn nối thẳng `infoSearch` (id setting), `point` và `lineId` vào SQL** — chưa gây lỗi, Dev đề nghị mở việc riêng để bind nốt (ngoài phạm vi fix này).

File đã sửa (service `java-job`):
```
src/main/java/sns/line/models/LineUserModel.java   |  26 ++--
.../models/LineUserModelFilterInClauseTest.java    | 139 +++++++++++++++++++++
2 files changed, 157 insertions(+), 8 deletions(-)
```

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `LineUserModel.isValidFilterV2` (kiểm từng user) | Không đổi logic, chỉ nhận kết quả bind đúng từ `buildWhereFilter`/`buildWhereORFilter` | Caller cho: action, step kịch bản, auto-reply, action postback, rich menu toggle, nhắc lịch event |
| 2 | `LineUserModel.getListLineUserFromFilterV2` (lấy danh sách) | Không đổi logic, chỉ nhận kết quả bind đúng | Caller cho: broadcast, action schedule, export CSV, cross analysis, `FilterService` |
| 3 | Filter trộn AND + OR có thêm điều kiện `= ?` / `LIKE ?` | Đã kiểm thứ tự tham số bằng unit test + harness AND+OR | Mọi điều kiện dùng chung một danh sách tham số (`whereArgsStock`) — lệch thứ tự sẽ sai toàn bộ filter, không chỉ phần IN |
| 4 | Module callback (dùng cùng file `LineUserModel.java`) | **CHƯA sửa trong lần deploy này** — chỉ sửa sau khi cherry-pick commit `75f5c8238` riêng sang `release-callback-t09-2026` | Nhánh job đi trước nhánh callback 37 commit, không merge cả nhánh để tránh kéo theo thay đổi khác |

> ⚠️ Dev **chưa verify runtime với DB thật** — chỉ kiểm bằng unit test (`LineUserModelFilterInClauseTest`, không chạm DB) + harness AND+OR. Đây là input QA cần tự verify bằng TC thật (không chỉ tin vào "rủi ro thấp" của Dev).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `LineUserModel.buildWhereFilter` (AND) | `LineUserModel.java` (line ~965, 967, 1021, 1024) | Direct | Build mệnh đề `IN`/`NOT IN` cho `friend_information_value.value` (select) + `line_user.province` |
| F2 | `LineUserModel.buildWhereORFilter` (OR) | `LineUserModel.java` (line ~1790, 1792, 1846, 1849) | Direct | Tương tự F1 nhưng cho nhánh OR |
| F3 | `LineUserModel.isValidFilterV2` | `LineUserModel.java` | Indirect (caller của F1/F2) | Kiểm từng user cho: action, step kịch bản, auto-reply, action postback, rich menu toggle, nhắc lịch event |
| F4 | `LineUserModel.getListLineUserFromFilterV2` | `LineUserModel.java` | Indirect (caller của F1/F2) | Lấy danh sách cho: broadcast, action schedule, export CSV, cross analysis, `FilterService` (Dev không nêu luồng nghiệp vụ của `FilterService`) |
| F5 | Helper `buildInPlaceholders` (mới) | `LineUserModel.java` | Direct (mới thêm) | Sinh placeholder `?,?,...` cho mệnh đề IN, dùng chung cho cả 8 vị trí F1+F2 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có — Dev xác nhận "Migration/thay đổi dữ liệu: không có (đã kiểm diff)" | — | Chỉ sửa code build SQL (bind tham số), không chạm schema/data, không migration |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 一斉配信 (Broadcast) — gửi tin theo filter friend info select / province | F4 | Low (theo Dev) — nhưng là luồng lấy-danh-sách, ảnh hưởng số lượng người nhận thật |
| T2 | アクション予約 (Action schedule) | F4 | Low |
| T3 | CSV管理 (Export CSV theo filter) | F4 | Low |
| T4 | クロス分析 (Cross analysis theo filter) | F4 | Low |
| T5 | Step kịch bản (Scenario step), 自動応答 (Auto-reply), Postback action, リッチメニュー toggle, イベント リマインド — kiểm filter cho 1 user | F3 | Low — nhưng chạy per-user, tần suất gọi cao hơn F4 |
| T6 | Filter trộn AND + OR nhiều điều kiện (select + province + text/date/point khác) | F1, F2 | **Medium** — rủi ro lệch thứ tự tham số khi nhiều điều kiện dùng chung 1 danh sách args (Dev tự nêu là rủi ro chính) |
| T7 | Điều kiện tỉnh (province) thuộc / không thuộc | F1, F2 | Low — "không thuộc" phải vẫn gồm người chưa có tỉnh (behavior giữ nguyên) |

**Ghi chú ngoài phạm vi (KHÔNG thuộc 4.1-4.3 của fix này nhưng liên quan)**:
- Module callback (dùng chung `LineUserModel.java`) **chưa được fix** tới khi cherry-pick riêng — nguy cơ: nếu callback chạy trước khi cherry-pick, bug gốc vẫn còn ở đó.
- Module web (`php-web`, `Conversation.php` ~line 781) có bug tương tự với dấu `"` — ticket riêng, không cover ở đây.
- Hành vi "trả `true`/list rỗng khi query lỗi" **giữ nguyên, cố ý không đổi** — không phải regression nhưng cần TC xác nhận hành vi này không đổi (để tránh hiểu nhầm là đã fix).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
