# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) — assignee ticket: Ngô Thúy Ngần |
| Commit / Pull Request | commit `7409e8194e` (6 file) — chưa có link PR trên ticket |
| Branch | `ai_fixbug_40336` (nhánh gốc `release_step_20260827`) — đã push lên origin |
| Ngày submit đánh giá | 2026-09-14 (Journal #136323) |
| Auto-filled | `2026-09-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Ở màn quản lý chat, khi đổi trạng thái đã xác nhận thì server có tính lại số hội thoại chưa xác nhận và lưu vào bot, nhưng phản hồi trả về trình duyệt chỉ có cờ thành công, không kèm con số mới. Phía giao diện cũng chỉ tải lại danh sách tin, không đụng tới badge cạnh menu 1:1 chat. Badge này được máy chủ dựng sẵn một lần lúc tải trang và màn quản lý chat không có kết nối socket cập nhật (chỉ màn chat 1:1 mới có), nên con số cũ nằm nguyên cho tới khi người dùng tải lại trang.

## 2. Cách fix

Lần này (theo yêu cầu human): gộp logic cập nhật badge của hai màn thành MỘT nguồn duy nhất. Tách hàm ghi badge ra file dùng chung mới `public/js/layout/sidebar-badge.js` (nạp kèm thanh bên), màn chat 1:1 và màn quản lý chat đều gọi hàm này thay vì mỗi màn một bản chép. Bỏ bản sao trong `talk_list/index.js` và bỏ hàm cũ trong `chats/chat-v2.js` (4 chỗ gọi đổi tên theo), nhờ đó hết trùng tên hằng giữa hai file. Đồng thời bỏ format sẵn ở server: `countBadge` trả **số nguyên thuần** thay vì chuỗi rút gọn kiểu dấu cộng đứng trước, để việc hiển thị quá 99 do một mình hàm dùng chung lo — trước đây màn chat 1:1 hiện dấu cộng **đứng trước** còn thanh bên hiện dấu cộng **đứng sau**. Giữ nguyên phần sửa gốc của ticket (API đổi trạng thái trả thêm số hội thoại chưa xác nhận).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TalkListController::changeStatusMessage` — `app/Http/Controllers/Basic/TalkListController.php` | Response trả thêm số hội thoại chưa xác nhận | Fix gốc: client cần con số mới để ghi badge |
| 2 | `countBadge` — `app/Helpers/functions.php` | Đổi kiểu trả về: chuỗi rút gọn → số nguyên thuần | Dồn việc format (>99) về 1 hàm JS dùng chung |
| 3 | `totalUserConfirmMessage` — `app/Helpers/functions.php` | (Dev liệt kê ở mục "đã check") | Nguồn tính số hội thoại chưa xác nhận |
| 4 | `setChatMenuBadge` — `public/js/layout/sidebar-badge.js` | **File mới** — hàm ghi badge dùng chung | Gộp 2 bản logic badge thành 1 nguồn |
| 5 | `changStatus` — `public/js/talk_list/index.js` | Bỏ bản sao logic badge, gọi hàm dùng chung | Hết trùng tên hằng giữa 2 file |
| 6 | `setBadge` — `public/js/chats/chat-v2.js` | **Đã gỡ**, 4 chỗ gọi chuyển sang hàm dùng chung | Gộp logic; màn chat 1:1 bị chạm dù đang chạy ổn |
| 7 | sidebar badge markup + nạp script — `resources/views/layout/v2/basic/sidebar.blade.php` | Nạp `sidebar-badge.js` kèm thanh bên | Mọi màn có sidebar đều có hàm dùng chung |
| 8 | `ChatController::getBadge` — `app/Http/Controllers/ChatController.php` | Caller của `countBadge` (đã check) | Chịu ảnh hưởng khi `countBadge` đổi kiểu trả về |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev kê theo mục "4.1 File thay đổi" — tag F* do /new-task gán theo thứ tự Dev liệt kê. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TalkListController::changeStatusMessage` (API đổi trạng thái hội thoại) | `app/Http/Controllers/Basic/TalkListController.php` | Direct | Trả thêm số hội thoại chưa xác nhận trong response |
| F2 | `countBadge` (+ `totalUserConfirmMessage`) | `app/Helpers/functions.php` | Direct | Đổi kiểu trả về sang số nguyên; 2 nơi gọi: `ChatController:6246` (payload socket), `ChatController:7062` (`/ajax/get-badge`) |
| F3 | `setChatMenuBadge` — hàm ghi badge dùng chung | `public/js/layout/sidebar-badge.js` (**file mới**) | Direct | Một mình lo hiển thị khi số > 99 |
| F4 | Màn chat 1:1 — `setBadge` bị gỡ, 4 chỗ gọi đổi sang hàm dùng chung | `public/js/chats/chat-v2.js` | Direct | Màn đang chạy ổn nhưng bị chạm code |
| F5 | Màn talk list — `changStatus`, bỏ bản sao logic badge | `public/js/talk_list/index.js` | Direct | |
| F6 | Sidebar layout — markup badge + nạp script | `resources/views/layout/v2/basic/sidebar.blade.php` | Direct | Cả 2 màn dùng `layout.basic.main` nên đều nhận script |
| F7 | `ChatController::getBadge` | `app/Http/Controllers/ChatController.php` | Indirect | Caller của `countBadge`, nhận kiểu trả về mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Dev ghi: Không có** — không đổi cấu trúc hay dữ liệu bảng nào |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat / Talk Management (**FA-002**) — badge menu chat cập nhật ngay sau khi đổi trạng thái xác nhận, không phải tải lại trang | F1, F5, F3 | (Dev không ghi mức) |
| T2 | 1-on-1 Chat (**FA-001**) — màn chat 1:1 dùng chung hàm ghi badge; cách hiển thị khi vượt 99 nay khớp với lúc máy chủ dựng thanh bên | F4, F3, F2 | (Dev không ghi mức) |

---

## 5. Recover data (từ báo cáo Dev)

- Không cần recover data.

## 6. Verify của Dev (nguyên văn báo cáo)

- **Mức**: lint.
- **Lệnh**: `php -l app/Helpers/functions.php`: No syntax errors detected; `php -l app/Http/Controllers/Basic/TalkListController.php`: No syntax errors detected; `node --check public/js/layout/sidebar-badge.js | chats/chat-v2.js | talk_list/index.js`: OK cả 3; grep `CHAT_MENU_BADGE_SELECTOR`: chỉ còn 1 khai báo duy nhất ở file dùng chung; grep `setBadge` trong `public` + `resources`: không còn chỗ nào gọi hàm cũ; `git diff --stat origin/release_step_20260827...ai_fixbug_40336`: 6 file, 64 thêm / 31 bớt.
- **Bằng chứng**: `countBadge` chỉ có 2 nơi gọi (`ChatController:6246` gói vào payload socket, `ChatController:7062` cho `/ajax/get-badge`), cả hai đều chỉ để hiển thị badge — không blade nào render trực tiếp nên đổi kiểu trả về không lan ra chỗ khác; grep xác nhận không trang nào nạp cùng lúc `chats/chat-v2.js` và `talk_list/index.js`; cả hai màn đều dùng `layout.basic.main` nên đều có thanh bên và nhận được file dùng chung; sửa trên git worktree riêng (`/tmp/wt40336`) vì working copy `source/sns-line` đang có worker khác dùng.

## 7. Rủi ro / lưu ý khi test (Dev tự review — nguyên văn)

- Đụng vào màn chat 1:1 đang chạy ổn: **4 chỗ gọi đổi tên hàm**. Nếu file dùng chung không được nạp thì badge màn chat sẽ ngừng cập nhật — đã nạp ở thanh bên nên mọi màn có thanh bên đều có; cả hai màn liên quan đều dùng chung layout đó.
- `countBadge` đổi kiểu trả về từ chuỗi rút gọn sang số nguyên: chỉ 2 nơi gọi, cả hai đều đẩy thẳng cho phần hiển thị badge, không nơi nào so sánh hay ghi vào dữ liệu.
- Badge trong **danh sách menu yêu thích do Vue vẽ**: vẫn ghi thẳng DOM như hành vi sẵn có, **chưa đồng bộ vào dữ liệu của Vue** (giữ nguyên như cảnh báo vòng 1 của AI reviewer, không phát sinh mới).
- Ghi chú của AI: "Phạm vi mở rộng sang màn chat 1:1 và một helper dùng chung nên cần review lại."

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
