# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kim Cúc` (người submit đánh giá ảnh hưởng — journal 2026-06-19) |
| Commit / Pull Request | `2f32444c376459de6cace24fba6933ee53fea951` |
| Branch | `m_202606_duplicate_line_user_37711` |
| Ngày submit đánh giá | `2026-06-19` |
| Auto-filled | `2026-06-19 by /new-task` |

> ⚠️ **2 bản fix song song trong Redmine** — file này lấy theo bản dev cuối cùng (Kim Cúc, fix phía JOB). Trước đó có bản AI auto-fixbug (branch `ai_fixbug_37711`, commit `a83fdce851`) fix phía WEB (QRCodeController::checkFriend + FormAnswerController::userOpenFormanswer). **Leader/Tester cần confirm với Dev branch nào được merge thực tế** trước khi viết/test TC — phạm vi impact của 2 bản KHÁC NHAU. Nội dung bản AI auto-fix lưu ở cuối file để tham chiếu.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [x] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Do tính năng form của web và callback follow của job chạy cùng thời điểm → tạo ra 2 bản ghi line_user trùng line_id. Hệ quả là 1 khách bị hiển thị thành 2 tài khoản, và cùng 1 ステップ配信 (scenario) chạy song song trên cả 2 bản ghi.

(Bổ sung từ phân tích root cause — journal Thanh Duy Nguyen 2026-06-19: "Do tính năng form của web và callback follow của job chạy cùng thời điểm nên tạo 2 bản ghi cùng line_id". Bảng line_user / bot_line_user KHÔNG có unique index → không có ràng buộc DB chặn trùng; cả 2 luồng cùng read→insert autocommit nên khi cửa sổ ghi chồng nhau thì cùng thấy "chưa tồn tại" rồi cùng tạo.)

## 2. Cách fix

Sau khi insert mới line_user, check lại theo line_id: nếu đã tồn tại bản ghi cùng line_id với id nhỏ hơn (tức luồng khác đã insert trước) thì xoá bản ghi vừa add và dùng lại bản ghi cũ. Áp dụng cho tất cả các điểm tạo mới line_user (follow bạn, nhắn tin lại, tạo group, thêm member group).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

Method mới `checkDuplicateLineUserAfterInsert` và repository method `findFirstByLineIdOrderByIdAsc` chỉ được gọi nội bộ trong `HandlePostbackTask` (4 điểm insert), không có caller cũ nào bị ảnh hưởng. Các luồng tạo line_user khác (`checkAddGroupFriend`, `checkAddGroup`, `checkAddOldFriend`, `doHandleFollowEvent`) giữ nguyên signature, chỉ chèn thêm bước dedup ngay sau save và trước khi dùng id để tạo dữ liệu phụ thuộc (conversation / bot_line_user / group_line_user).

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.checkDuplicateLineUserAfterInsert` | Method mới | Dedup line_user theo line_id sau insert |
| 2 | `LineUserRepository.findFirstByLineIdOrderByIdAsc` | Method mới | Tìm bản ghi line_user gốc (id nhỏ nhất) cùng line_id |
| 3 | `HandlePostbackTask.doHandleFollowEvent` | Chèn bước dedup sau save | Điểm tạo line_user khi follow |
| 4 | `HandlePostbackTask.checkAddOldFriend` | Chèn bước dedup sau save | Điểm tạo line_user khi bạn cũ nhắn tin lại |
| 5 | `HandlePostbackTask.checkAddGroupFriend` | Chèn bước dedup sau save | Điểm tạo line_user group |
| 6 | `HandlePostbackTask.checkAddGroup` | Chèn bước dedup sau save | Điểm tạo line_user khi thêm member group |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandlePostbackTask.checkDuplicateLineUserAfterInsert` (mới) | HandlePostbackTask | Direct | Method dedup mới |
| F2 | `LineUserRepository.findFirstByLineIdOrderByIdAsc` (mới) | LineUserRepository | Direct | Query gốc theo line_id |
| F3 | `HandlePostbackTask.doHandleFollowEvent` | HandlePostbackTask | Direct | Follow bạn |
| F4 | `HandlePostbackTask.checkAddOldFriend` | HandlePostbackTask | Direct | Bạn cũ nhắn tin lại |
| F5 | `HandlePostbackTask.checkAddGroupFriend` | HandlePostbackTask | Direct | Group friend |
| F6 | `HandlePostbackTask.checkAddGroup` | HandlePostbackTask | Direct | Thêm member group |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `line_user` | DELETE (runtime) | Khi phát hiện trùng, bản ghi line_user mới vừa insert sẽ bị xoá (`deleteById`), giữ lại bản ghi insert trước đó |
| D2 | Elasticsearch (sync line_user) | (không sync) | Bản trùng KHÔNG được sync lên Elasticsearch |
| D3 | Schema / migration / config | KHÔNG đổi | Không có thay đổi schema / migration / config |

> ⚠️ Dữ liệu trùng **CŨ** đã tồn tại trước fix vẫn cần DBA dọn/gộp riêng (needDataRecovery). Fix chỉ chặn trùng MỚI phát sinh.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Kết bạn / follow (doHandleFollowEvent) — add bạn mới + add lại bạn cũ, verify chỉ tạo 1 line_user | F3, D1 | High |
| T2 | Nhắn tin lại từ bạn cũ chưa có bot_line_user (checkAddOldFriend) — verify dùng đúng line_user gốc | F4, D1 | Medium |
| T3 | Group / member trong group (checkAddGroupFriend, checkAddGroup) — bot vào group + member gửi tin, verify line_user group/member không nhân đôi | F5, F6, D1 | Medium |
| T4 | ステップ配信 / Scenario (gửi tin theo bước) — case đang reproduce trùng tài khoản, verify sau fix mỗi khách chỉ 1 line_user nên scenario không chạy song song trên 2 bản ghi | F1, D1 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Đã confirm branch merge thực tế** (`m_202606_duplicate_line_user_37711` fix-job vs `ai_fixbug_37711` fix-web) — xem cảnh báo đầu file

---

## (Tham chiếu) Bản AI auto-fixbug — fix phía WEB (branch `ai_fixbug_37711`, commit `a83fdce851`)

> Lưu để Leader đối chiếu. KHÔNG dùng làm input chính nếu branch này không được merge.

**Nguyên nhân:** Đăng ký bạn bè (tạo line_user + bot_line_user + conversation) chạy ở NHIỀU điểm độc lập, không khóa chung, và 2 bảng line_user/bot_line_user KHÔNG có ràng buộc duy nhất. Khi user mở link form answer / calendar / booking (chưa là bạn hoặc đang block), web gọi `QRCodeController::checkFriend` — hàm này (A) TỰ TẠO bạn bè trực tiếp bên web (KHÔNG transaction, KHÔNG khóa) và (B) trả về URL LIFF add-friend; user bấm 'Thêm bạn' → LINE gửi follow callback thật → JOB `doHandleFollowEvent` TẠO bạn bè lần nữa. Cả hai bên đều read→insert autocommit; khi cửa sổ ghi chồng nhau → 2 tài khoản trùng + cùng một ステップ配信 chạy trên cả hai.

**Cách fix:** Áp guard chống tạo trùng (xóa bản web vừa tạo khi đã có bản id nhỏ hơn) + chặn gửi tin/chạy action khi trùng tại 2 điểm tạo bạn bè khi MỞ FORM/BOOKING bên web: (1) `QRCodeController::checkFriend`; (2) `FormAnswerController::userOpenFormanswer` (route `/ajax/open-formanswer`, cả 2 nhánh user mới và user đã có line_user). Mỗi điểm: dedup line_user/bot_line_user/conversation + cờ `isDuplicateFriend` để KHÔNG gửi lại tin add-old-friend / không chạy `sendAction(action_old_id)` / không cộng thống kê khi trùng. `CalendarSalonController::checkFriend` chỉ đọc (không tạo) → không cần.

**File thay đổi:** `app/Http/Controllers/Basic/QRCodeController.php`, `app/Http/Controllers/Basic/FormAnswerController.php`.

**Lưu ý test (theo AI):** Web-only — chỉ chặn khi WEB là bên tạo bản trùng (web insert sau job); nếu WEB thắng race thì bản trùng do JOB vẫn còn. Vẫn không có unique index ở DB. Dữ liệu trùng CŨ không được dọn bởi fix này.
