# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #134965 — "AI LME Fix bug" — 2026-09-07 11:00** (báo cáo `★ AI AUTO-FIXBUG`). Redmine **không có** section "Đánh giá ảnh hưởng" trong description — toàn bộ nội dung dưới đây parse từ journal đó.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee hiện tại: Đoàn Thị Bích Hảo |
| Commit / Pull Request | `sns-line` commit `e9c4630691` (2 file) — [đã push] |
| Branch | `ai_fixbug_40599` (nhánh gốc `release_step_20260827`) |
| Ngày submit đánh giá | `2026-09-07` |
| Auto-filled | `2026-09-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #134965 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bảng cài đặt thông báo (`notify_setting`) của bot có **2 bản ghi cho CÙNG cặp (bot, người dùng)** — human đã tra DB xác nhận, 2 bản ghi tạo lúc `2026-09-04 21:48:06` và `21:49:19`.

Cả hai luồng sinh thông báo đều duyệt theo **TỪNG bản ghi cài đặt**:
- bên web (hàm chèn thông báo dùng chung `insertMobileNotify`),
- bên job callback (bản đã deploy tách thông báo theo từng người dùng — `ActionLaterService.checkAddNotify`)

=> mỗi sự kiện sinh **2 dòng thông báo cùng người nhận**, app lọc theo người dùng nên thấy cả 2 => mọi loại thông báo hiện trùng, đẩy push 2 lần, badge cộng 2.

**NGUỒN SINH BẢN GHI TRÙNG** (human xác nhận qua log, bot `218134`): bước kiểm tra bạn bè ở luồng kết nối bot trả về **không có bạn bè**, người dùng **CHẠY LẠI bước 2** của luồng kết nối bot; bước này **reuse lại bot tạm** nên dùng lại đúng mã bot cũ nhưng **vẫn tạo cài đặt thông báo vô điều kiện** => thêm bản ghi thứ 2.

Bản ghi thừa còn là **"bản ghi ma"**: màn Cài đặt thông báo chỉ **đọc/ghi bản ghi đầu tiên**, nên khách bỏ tick vẫn nhận thông báo từ bản ghi kia, và bản ghi thừa **mặc định BẬT sẵn** thông báo app với tick đủ 4 mục thêm bạn.

## 2. Cách fix

Sửa đúng điểm đã gây ra ca này: **bước 2 của luồng kết nối bot** tạo bản ghi cài đặt thông báo **vô điều kiện**, trong khi nhánh ngay trên nó dùng lại bot tạm nên giữ nguyên mã bot — chạy lại bước 2 là thêm bản ghi thứ 2 cùng cặp (bot, người dùng), khiến mọi thông báo bị nhân đôi. **Đổi thành chỉ tạo khi chưa có.**

Kèm **migration THÊM RÀNG BUỘC DUY NHẤT** trên cặp (bot, người dùng) để không tái diễn — migration **KHÔNG dọn dữ liệu**, vận hành dọn tay trước khi deploy.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `insertMobileNotify` — `app/Helpers/functions.php:6953, 7292-7293` | Không sửa | Vòng lặp theo từng bản ghi `notify_setting`, gán `user_id` mỗi dòng → dòng trùng sinh notify trùng |
| 2 | `ActionLaterService.checkAddNotify` — linect-service, `origin/release-callback-t07-2026` | Không sửa | Bản đã deploy duyệt `findAllByBotId`, mỗi bản ghi 1 dòng + 1 push |
| 3 | `BotController@createBot` — `app/Http/Controllers/Admin/BotController.php:5603` | **ĐÃ SỬA** — chỉ tạo khi chưa có | Điểm tạo `notify_setting` lúc tạo/kết nối bot — root cause |
| 4 | `StaffManagementController::createNotifyDefault` — `app/Http/Controllers/Admin/StaffManagementController.php:577` | Không sửa (theo quyết định human) | Điểm tạo khi nhân viên nhận lời mời |
| 5 | `NotifySettingController::getNotifySetting` — `app/Http/Controllers/Basic/NotifySettingController.php:100` | Không sửa | Tìm-rồi-tạo **không khoá** → còn khả năng race |
| 6 | `NotifySettingController::saveNotifySettings` — `app/Http/Controllers/Basic/NotifySettingController.php:343` | Không sửa | Nhánh tạo mới khi lưu cài đặt |
| 7 | `NotifySettingController::saveNotifySettingReceive` — `app/Http/Controllers/Basic/NotifySettingController.php:203` | Không sửa | Chỉ update bản ghi đầu tiên → bản ghi trùng thành "bản ghi ma" |
| 8 | `Api/NotifyController@getListFriend` — `app/Http/Controllers/Api/NotifyController.php:160` | Không sửa | Lọc `user_id` nên khớp cả 2 dòng trùng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguồn: mục "4.1 File thay đổi" của journal. Dev chỉ kê FILE thay đổi, không kê function-level. Cột function suy từ mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController@createBot` — bước 2 luồng thêm/kết nối bot | `app/Http/Controllers/Admin/BotController.php` | Direct | **Điểm sửa duy nhất về code.** Chuyển tạo `notify_setting` vô điều kiện → chỉ tạo khi chưa có |
| F2 | Migration thêm unique constraint | `database/migrations/2026_09_07_000000_dedupe_and_unique_notify_setting_bot_user.php` | Direct | Thêm `notify_setting_bot_id_user_id_unique` trên `(bot_id, user_id)`. KHÔNG dọn dữ liệu |
| F3 | `NotifySettingController::getNotifySetting` (`:100`) | `app/Http/Controllers/Basic/NotifySettingController.php` | Indirect | Tìm-rồi-tạo không khoá — sau khi có unique có thể **ném lỗi trùng khoá** nếu race |
| F4 | `NotifySettingController::saveNotifySettings` (`:343`) | `app/Http/Controllers/Basic/NotifySettingController.php` | Indirect | Nhánh tạo mới khi lưu cài đặt — cùng rủi ro trùng khoá |
| F5 | `StaffManagementController::createNotifyDefault` (`:577`) | `app/Http/Controllers/Admin/StaffManagementController.php` | Indirect | **Không sửa theo quyết định human** — sẽ báo lỗi trùng khoá nếu điều kiện tồn tại của nó trượt |
| F6 | `insertMobileNotify` (`:6953`, `:7292-7293`) | `app/Helpers/functions.php` | Indirect | Duyệt theo từng bản ghi → còn dữ liệu trùng thì vẫn nhân đôi notify |
| F7 | `ActionLaterService.checkAddNotify` | linect-service, `origin/release-callback-t07-2026` | Indirect | Job callback, cùng cơ chế duyệt theo bản ghi |
| F8 | `Api/NotifyController@getListFriend` (`:160`) | `app/Http/Controllers/Api/NotifyController.php` | Indirect | API app đọc list notify — lọc `user_id` nên khớp cả 2 dòng trùng |
| F9 | `php artisan recover:mobileBadgeNotify` | `app/Console/Commands/RecoverMobileBadgeNotify.php` | Indirect | Lệnh nắn lại badge đã cộng dư |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `notify_setting` — index `notify_setting_bot_id_user_id_unique` trên `(bot_id, user_id)` | MIGRATE | Dòng `user_id NULL` **không** bị ràng buộc. Migration **KHÔNG dọn dữ liệu** → phải dọn cặp trùng bằng tay TRƯỚC, nếu không migration lỗi `Duplicate entry` |
| D2 | `notify_setting` — xoá bản ghi trùng (giữ `MIN(id)`) | DELETE (thủ công, vận hành) | Đã chạy trên **staging và step** (Journal #134973). Chuyển liên kết Chatwork (`notification_room_url`, `api_token`) sang bản ghi giữ nếu bản ghi đó đang trống |
| D3 | `mobile_notify` — các dòng thông báo trùng đã sinh trước fix | KHÔNG tự xoá | Không tự mất sau fix |
| D4 | Badge thông báo app (đã cộng dư) | UPDATE (thủ công) | Chạy `php artisan recover:mobileBadgeNotify` nếu khách phàn nàn |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Add New Account (FA-032)** — bước 2 luồng thêm tài khoản / kết nối bot | F1 | High — chạy lại bước này không còn tạo thêm bản ghi cài đặt thông báo cho cùng bot |
| T2 | **Notification Settings (FA-006)** — màn Cài đặt thông báo (通知設定) | F3, F4, F7, D1 | High — mỗi cặp (bot, người dùng) chỉ còn đúng 1 bản ghi nên thông báo không bị nhân đôi |
| T3 | **Quản lý nhân viên (スタッフ管理)** — nhân viên nhận lời mời | F5, D1 | Medium — điểm tạo KHÔNG được sửa, có thể ném lỗi trùng khoá sau khi thêm unique |
| T4 | **Mobile App — push notification / danh sách thông báo / badge** | F6, F8, D3, D4 | Medium — dữ liệu trùng cũ + badge dư không tự mất |
| T5 | **Deploy / migration** | F2, D1, D2 | High — sai thứ tự (chưa dedup mà chạy migrate) → deploy dừng với lỗi `Duplicate entry` |

---

## 5. Recover data (mục 5 của journal — ngoài template)

⚠ **CÓ — BẮT BUỘC dọn dữ liệu TRƯỚC khi chạy migration**, do MySQL không tạo được ràng buộc duy nhất khi bảng còn cặp trùng.

Trình tự:
1. Rà cặp trùng: `SELECT bot_id, user_id, COUNT(*) FROM notify_setting WHERE user_id IS NOT NULL GROUP BY bot_id, user_id HAVING COUNT(*) > 1;`
2. Chuyển liên kết Chatwork (`notification_room_url`, `api_token`) sang bản ghi giữ nếu bản ghi đó đang trống.
3. Xoá bản ghi thừa, **GIỮ `id` nhỏ nhất** — vì đó là bản ghi màn Cài đặt thông báo đang đọc/ghi.
4. Chạy lại câu ở bước 1, phải trả về **rỗng** rồi mới `php artisan migrate`.

Chạy ngược thứ tự → deploy dừng với lỗi `Duplicate entry` cho khoá `notify_setting_bot_id_user_id_unique` (lỗi có in ra đúng cặp bot-user còn trùng).

Các dòng `mobile_notify` đã trùng và badge đã cộng dư trước đó **không tự sửa**; cần thì chạy `php artisan recover:mobileBadgeNotify`.

**Phạm vi**: Toàn bộ bot đang có bản ghi cài đặt thông báo trùng, **không riêng bot của khách**. Bot của khách (2 bản ghi tạo `2026-09-04 21:48:06` và `21:49:19`) sẽ CHỈ hết trùng **sau khi dọn dữ liệu** — bản vá code chỉ chặn phát sinh mới.

## 6. Verify (Dev tự verify — mục 6 của journal)

| Mục | Nội dung |
|---|---|
| Mức | `lint` |
| Lệnh | `php -l BotController.php` + migration → No syntax errors detected |
| Diff | `git diff --stat origin/release_step_20260827...ai_fixbug_40599` → **2 file, 53 dòng thêm, 2 dòng bớt** |
| ⚠️ Chưa verify | **CHƯA chạy được migration** — MySQL dev `Connection refused` |

## 7. Tự review của AI — rủi ro / lưu ý khi test (nguyên văn)

Scope chốt theo quyết định human: chỉ sửa điểm tạo đã được chứng minh bằng log của khách (bước 2 luồng kết nối bot) + migration thêm ràng buộc duy nhất. Phần dọn dữ liệu đã bỏ khỏi migration, chuyển thành việc vận hành chạy tay có kiểm soát (backup, duyệt SQL) trước khi deploy.

- **THỨ TỰ DEPLOY**: phải dọn dữ liệu trùng trước, nếu không migration sẽ lỗi `Duplicate entry` và chặn deploy.
- **Bản vá code chỉ chặn phát sinh mới** — khách vẫn thấy thông báo trùng cho tới khi dữ liệu được dọn.
- **Điểm tạo lúc nhân viên nhận lời mời (không sửa theo quyết định human)** sẽ báo lỗi trùng khoá nếu điều kiện tồn tại của nó trượt — kiểm trước bằng `SELECT COUNT(*) FROM notify_setting WHERE admin_id IS NULL`.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
