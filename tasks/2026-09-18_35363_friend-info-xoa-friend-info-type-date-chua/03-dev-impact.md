# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #35363 (Journal #130711 — AI LME Fix bug — 2026-08-20). Tester verify rồi tick checkbox bên dưới.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (AI auto-fixbug) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `2a337fc303` (repo sns-line, 3 file) — không có link PR |
| Branch | `ai_fixbug_35363` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-20` |
| Auto-filled | `2026-09-18 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trường thông tin bạn bè kiểu ngày (年月日) khi được lưu sẽ sinh lịch nhắc: 1 bản ghi event_step (type=3, gắn friend_info_id) và các bản ghi event_step_time cho từng bạn để job gửi action đúng mốc ngày. Nhưng các luồng XÓA trường thông tin (xóa 1 mục, xóa nhiều mục, xóa cả nhóm) chỉ xóa giá trị, tùy chọn và cài đặt hiển thị, hoàn toàn không đụng tới event_step và event_step_time. Job gửi nhắc chỉ quét event_step_time theo trạng thái chưa gửi và tới giờ, không kiểm tra trường thông tin còn tồn tại hay không, nên vẫn tiếp tục gửi tin cho khách sau khi trường đã bị xóa.

## 2. Cách fix

Thêm hàm dùng chung deleteEventStepFriendInfo(friendInfoId, botId) trong app/Helpers/functions.php: lấy danh sách event_step type=3 theo friend_info_id + bot, xóa toàn bộ event_step_time của các bản ghi đó rồi xóa chính các event_step, có ghi log xóa. Gọi hàm này ở tất cả luồng xóa trường thông tin bạn bè: màn quản trị web (xóa 1 mục, xóa nhiều mục, xóa cả nhóm trong FriendInformationController) và API dùng cho app (xóa trường, xóa thư mục trong FriendInfoMobileController). Quét tương tự trên 2 repo: luồng xóa giá trị ngày của từng người bạn và luồng xóa bot đã dọn lịch nhắc sẵn nên không phải sửa.

**Tự review (AI):** Fix đúng root cause và tối thiểu: bổ sung đúng bước dọn còn thiếu ở luồng xóa, dùng lại cách dọn mà luồng lưu đã áp dụng sẵn (xóa event_step_time theo event_step_id rồi xóa event_step). Hàm mới tự chứa trên release, không sửa hàm dùng chung sẵn có nên không ảnh hưởng luồng lưu/sửa đang chạy. event_step type=3 gắn duy nhất với 1 friend_info_id nên xóa không đụng lịch của tính năng khác. So sánh friend_info_id bằng chuỗi khớp đúng kiểu cột varchar và không dính các trường mặc định d_1..d_6.

Rủi ro / lưu ý khi test:
- Chưa chạy được trên DB dev (stack dev tắt) nên chưa có bằng chứng số bản ghi bị xóa thực tế - cần QA verify lại theo các bước tái hiện
- Xóa cứng (hard delete) cả event_step_time đã gửi của trường bị xóa: mất lịch sử mốc gửi cũ của trường đó. Chấp nhận được vì trường thông tin không còn tồn tại và luồng lưu hiện tại cũng xóa cứng theo cách này; lịch sử gửi tin thật vẫn nằm ở bảng tin nhắn
- Dữ liệu tồn đọng cũ vẫn cần dọn thủ công (xem phần recover data)

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `deleteEventStepFriendInfo` — app/Helpers/functions.php:9098 | Hàm mới | Dọn event_step type=3 + event_step_time theo friend_info_id + bot |
| 2 | `settingEventTimeFriendInfo` — app/Helpers/functions.php:9124 | — | Tham chiếu cách dọn lịch theo từng bạn |
| 3 | `FriendInformationController::infoFriendAction` case `deleteItem` — FriendInformationController.php:630 | Gọi hàm mới | Xóa 1 mục |
| 4 | `FriendInformationController::infoFriendAction` case `deleteItems` — FriendInformationController.php:653 | Gọi hàm mới | Xóa nhiều mục |
| 5 | `FriendInformationController::infoFriendAction` case `deleteGroup` — FriendInformationController.php:583 | Gọi hàm mới | Xóa cả nhóm |
| 6 | `FriendInformationController::deleteDataFriendInfo` — FriendInformationController.php:874 | — | Chỉ xóa action_detail |
| 7 | `FriendInformationController::saveSettingInfoFriend` — FriendInformationController.php:1170-1300 | — | Luồng tạo/sửa sinh event_step + event_step_time |
| 8 | `FriendInfoMobileController::deleteFriendInfoField` — Api/Mobile/FriendInfoMobileController.php:784 | Gọi hàm mới | API app xóa trường |
| 9 | `FriendInfoMobileController::deleteFriendInfoFolder` — Api/Mobile/FriendInfoMobileController.php:957 | Gọi hàm mới | API app xóa thư mục |
| 10 | `HelperService` — app/Services/HelperService.php:762 | — | Xóa giá trị ngày của 1 bạn, đã gọi settingEventTimeFriendInfo null |
| 11 | `FlowDeleteBot` — app/Console/Commands/FlowDeleteBot.php:287 | — | Xóa bot đã dọn event_step + event_step_time |
| 12 | `NewEventRemindTask.startJobScan` (linect-service) | — | Job quét event_step_time chưa gửi, không kiểm tra trường thông tin còn tồn tại |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ liệt kê **file thay đổi** (không đánh F1/F2) — map theo file:

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `deleteEventStepFriendInfo` (hàm mới) | app/Helpers/functions.php | Direct | |
| F2 | `infoFriendAction` deleteItem / deleteItems / deleteGroup | app/Http/Controllers/Basic/FriendInformationController.php | Direct | |
| F3 | `deleteFriendInfoField` / `deleteFriendInfoFolder` | app/Http/Controllers/Api/Mobile/FriendInfoMobileController.php | Direct | API app mobile |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `event_step` | DELETE | Xóa các bản ghi type=3 có friend_info_id trỏ tới trường thông tin đang bị xóa (mỗi trường thông tin sở hữu riêng, không dùng chung) |
| D2 | `event_step_time` | DELETE | Xóa các bản ghi lịch gửi thuộc những event_step nói trên (gồm cả bản ghi chưa gửi status=0 lẫn đã gửi, vì trường thông tin không còn nữa) |
| — | `friend_information_setting`, `friend_information_value`, `action` | — | Không đụng tới — đã được luồng xóa cũ xử lý |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Information (FA-015) — xóa trường thông tin bạn bè nay dọn luôn lịch nhắc theo mốc ngày đã sinh | F1, F2, F3, D1, D2 | _(Dev không ghi mức)_ |
| T2 | Reminder Delivery (FA-022) — job gửi nhắc không còn bản ghi event_step_time mồ côi nên không gửi nhầm tin sau khi trường thông tin đã bị xóa | D1, D2 | _(Dev không ghi mức)_ |

### 5. Recover data (Dev ghi thêm)

⚠ CÓ — Fix chỉ chặn phát sinh mới. Dữ liệu tồn đọng từ các trường đã bị xóa TRƯỚC khi có fix vẫn nằm trong event_step/event_step_time và job vẫn gửi tin khi tới mốc. Cần chạy dọn 1 lần trên production: tìm event_step type=3 có friend_info_id không bắt đầu bằng `d_` và không còn tồn tại trong friend_information_setting, xóa event_step_time thuộc các bản ghi đó rồi xóa chính event_step. SELECT đếm trước để DEV/PM duyệt, backup 2 bảng trước khi xóa. Phạm vi: toàn hệ thống.

### 6. Verify (Dev)

Mức **lint** (`php -l` 3 file OK). Không có unit test, chưa kiểm chứng trên DB dev.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
