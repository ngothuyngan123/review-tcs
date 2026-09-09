# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #133412 — AI LME Fix bug — 2026-08-28** trên Redmine #39467 (báo cáo hệ thống Auto-fixbug LME). Mục 1 / 2 / 3 / 4 dưới đây chép **nguyên văn**; phần bảng có đánh dấu rõ dòng nào là suy trực tiếp từ mục 2 + 3 của Dev.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee hiện tại của ticket: `Ngọc Ánh` (QA) |
| Commit / Pull Request | `commit 29030c7d21` (repo `sns-line`) — **không có link PR**. Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=a5f60ebf-b399-4025-ae83-d54980ea6949 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=39467 |
| Branch | `ai_fixbug_39467` (nhánh gốc `release_step_20260805`, 1 file) — đã push |
| Ngày submit đánh giá | `2026-08-28` |
| Auto-filled | `2026-09-08 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn Cài đặt thông báo có hàm kiểm quyền màn hình (`userHasScreenAccess`) đặt trong controller cho 3 route lưu cài đặt nhận thông báo, nhưng 4 route ajax phần Chatwork (lưu URL phòng, lưu API token, đổi kiểu gửi, gửi thử) lại quên gọi. Các route ajax này chỉ nằm sau lớp kiểm đăng nhập, không bị lớp kiểm quyền theo màn chặn, nên nhân viên được mời vào bot mà role KHÔNG có màn Cài đặt thông báo vẫn gọi trực tiếp được và ghi cấu hình thành công (HTTP 200, giá trị kiểu gửi Chatwork đổi từ 0 sang 1).

## 2. Cách fix

Thêm bước kiểm quyền màn Cài đặt thông báo (`userHasScreenAccess('notifySetting')`) vào đầu 4 route ajax Chatwork trong `NotifySettingController`: lưu URL phòng Chatwork, lưu API token, đổi kiểu gửi thông báo Chatwork và gửi thử; không có quyền thì trả 403 kèm thông báo tiếng Nhật giống các route lưu cài đặt thông báo sẵn có, và thoát trước khi chạm DB hay gọi API Chatwork. Quét ngang trong cùng màn: các route đọc dữ liệu và đăng ký push của chính người dùng không nằm trong phạm vi ghi cấu hình nên giữ nguyên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn danh sách Dev kê (mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN"), đưa về bảng template — không thêm/bớt mục nào.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `NotifySettingController::ajaxSaveUrlChatWork` (`app/Http/Controllers/Basic/NotifySettingController.php`) | **CÓ sửa** — thêm guard `userHasScreenAccess('notifySetting')` | Route ajax ChatWork thiếu kiểm quyền — root cause |
| 2 | `NotifySettingController::ajaxSaveApiTokenChatWork` (cùng file) | **CÓ sửa** — thêm guard | Route ajax ChatWork thiếu kiểm quyền — root cause |
| 3 | `NotifySettingController::ajaxChangeTypeSendChatwork` (cùng file) | **CÓ sửa** — thêm guard | Route ajax ChatWork thiếu kiểm quyền — **route tái hiện bug gốc** |
| 4 | `NotifySettingController::ajaxTestSendChatwork` (cùng file) | **CÓ sửa** — thêm guard | Route ajax ChatWork thiếu kiểm quyền — chặn trước khi gọi ra api.chatwork.com |
| 5 | `NotifySettingController::saveNotifySettingReceive` / `saveNotifySettingReceivePage` / `saveNotifySettings` | Không sửa | Mẫu kiểm quyền sẵn có mà bản fix sao chép |
| 6 | `userHasScreenAccess` (`app/Helpers/functions.php:4789`) | Không sửa | Hàm kiểm quyền dùng lại: chủ bot luôn qua, nhân viên phải có route màn trong role hiện tại |
| 7 | `getRouterBotInvite` (`app/Helpers/functions.php`) | Không sửa | Nguồn danh sách route theo role của nhân viên |
| 8 | `BasicAccess` middleware (`app/Http/Middleware/BasicAccess.php`) | Không sửa | Lớp kiểm đăng nhập — không chặn theo màn |
| 9 | `routes/web.php` dòng 3937-3940 (4 route ajax Chatwork) | Không sửa | 4 route nằm ngoài nhóm middleware kiểm quyền theo màn |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Ở mục 4.1 Dev chỉ ghi **file thay đổi**, nguyên văn: `app/Http/Controllers/Basic/NotifySettingController.php`.
> Các dòng `F*` dưới đây suy **trực tiếp** từ mục 2 + mục 3 của Dev (các function Dev nêu đích danh), không thêm function nào ngoài danh sách Dev đã kê.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ajaxSaveUrlChatWork` — `POST /ajax/notify/save-url-chat-work` (EP-11) | `app/Http/Controllers/Basic/NotifySettingController.php` | Direct | Thêm guard, trả 403 trước khi chạm DB / gọi ChatWork |
| F2 | `ajaxSaveApiTokenChatWork` — `POST /ajax/notify/save-api-token-chat-work` (EP-12) | cùng file | Direct | Thêm guard |
| F3 | `ajaxChangeTypeSendChatwork` — `POST /ajax/notify/save-type_notify_send_chatwork` (EP-13) | cùng file | Direct | Thêm guard — **route tái hiện bug gốc** |
| F4 | `ajaxTestSendChatwork` — `POST /ajax/notify/test-send-chatwork` (EP-14) | cùng file | Direct | Thêm guard — chặn trước outbound `api.chatwork.com` |
| F5 | `saveNotifySettingReceive` / `saveNotifySettingReceivePage` / `saveNotifySettings` (EP-07/08/09) | cùng file | Indirect | Không sửa, nhưng **cùng file điều khiển** → vùng regression |
| F6 | `userHasScreenAccess` | `app/Helpers/functions.php:4789` | Indirect | Được gọi thêm ở 4 chỗ mới; bản thân hàm không đổi |
| F7 | Route đọc dữ liệu + đăng ký push của chính người dùng (EP-02, EP-16) trên cùng màn | cùng controller | Indirect | Dev **cố ý giữ nguyên** — không nằm trong phạm vi ghi cấu hình |

### 4.2. List data bị update khi fix bug

> Nguyên văn Dev: *"Không có — chỉ chặn ghi trái quyền, không sửa/không migrate dữ liệu cũ. Cấu hình đã bị nhân viên không có quyền ghi trước đó (nếu có) vẫn giữ nguyên, chủ bot tự chỉnh lại trên màn."*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *Không có* (nguyên văn Dev) | — | Fix không CREATE / UPDATE / DELETE / MIGRATE bất kỳ dữ liệu nào |
| D2 | `notify_setting` — cột `url_chat_work`, `api_token_chat_work`, `type_notify_send_chatwork` (theo cặp `bot_id` + `user_id`) | Không đổi bởi fix — chỉ **bị chặn ghi** khi thiếu quyền | Dữ liệu staff không quyền đã ghi **trước** khi fix vẫn còn nguyên, chủ bot tự chỉnh lại trên màn |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn Dev; cột "Nguy cơ regression" Dev **không ghi mức** — mức dưới đây là đề xuất của `/new-task`, **Leader verify lại**.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Notification Settings (FA-006)** — chặn nhân viên không được cấp quyền màn Cài đặt thông báo ghi cấu hình Chatwork và gửi tin thử | F1–F5 | High *(đề xuất — Dev không ghi mức)* |
| T2 | **Staff Management (FA-035)** — role của nhân viên nay có hiệu lực với cả nhóm route Chatwork của màn Cài đặt thông báo | F6 | Medium *(đề xuất — Dev không ghi mức)* |

---

## 5. Recover data (mục Dev thêm ngoài template)

- ✔ **Không cần recover data.**

## 6. Verify của Dev (mục Dev thêm ngoài template)

- **Mức**: `lint` — ⚠️ **KHÔNG chạy được kiểm chứng runtime**: MySQL dev `host.docker.internal:3306` Connection refused (stack dev đang tắt).
- **Lệnh đã chạy**: `php -l app/Http/Controllers/Basic/NotifySettingController.php` → No syntax errors detected; `git diff --stat origin/release_step_20260805...ai_fixbug_39467` → 1 file changed, 16 insertions(+).
- **Bằng chứng Dev dẫn**:
  - `routes/web.php:3937-3940` — 4 route ajax Chatwork nằm ngoài nhóm middleware kiểm quyền theo màn, chỉ có lớp kiểm đăng nhập.
  - `NotifySettingController.php:197 / 378 / 623` — 3 route lưu cài đặt thông báo đã có sẵn `userHasScreenAccess('notifySetting')`, khớp mô tả 403 của tester.
  - `app/Helpers/functions.php:4789` — `userHasScreenAccess`: chủ bot luôn qua, nhân viên phải có route màn trong danh sách role hiện tại.

## Tự review của AI (nguyên văn) — rủi ro / lưu ý khi test

- Fix tối giản, đúng root cause: bù lớp kiểm quyền còn thiếu ở 4 route ajax Chatwork, dùng đúng hàm và đúng thông điệp 403 mà 3 route lưu cài đặt thông báo cùng màn đang dùng. Guard đặt ngay sau `addLogUserAction` và trước mọi thao tác DB/API nên không ghi và không gọi Chatwork khi thiếu quyền. Chủ bot (`admin_id`) luôn qua guard nên luồng bình thường không đổi.
- ⚠️ Nhân viên đang mở màn mà bị thu hồi quyền sẽ thấy thao tác lưu Chatwork **im lặng không có thông báo** (JS hiện chỉ ẩn overlay ở nhánh fail) — hành vi này giống các route lưu cài đặt thông báo hiện có, **không sửa thêm phía FE** để giữ fix tối giản.
- ⚠️ Chưa chạy được kiểm chứng runtime vì MySQL/web dev đang tắt; đã lint PHP và đối chiếu mẫu kiểm quyền sẵn có.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
