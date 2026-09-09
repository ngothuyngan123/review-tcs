# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: journal #131894 của **AI LME Fix bug** trên Redmine #39040 (2026-08-21T03:43:45Z).
> Format gốc của Auto-fixbug (■1..■6) đã được map sang 4 mục của template — nội dung giữ **nguyên văn**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `5c33646743` (repo `sns-line`, 4 file) — `<không có link PR trong Redmine>` |
| Branch | `ai_fixbug_39040` (nhánh gốc `release_step_20260623`) — đã push |
| Ngày submit đánh giá | `2026-08-21` |
| Auto-filled | `2026-08-26 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=38ad3881-ec99-4f82-9792-95cf4c14748f |
| Dashboard fixbug | https://dashboard.melonglobal.net/fixbug-lme/?id=39040 |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn ■ 1. NGUYÊN NHÂN

Màn profile/cài đặt kết nối bot bản MỚI (/admin/setting-bot — màn mà sidebar hiện tại trỏ tới) đặt giới hạn ảnh đại diện là 10MB ở cả JS lẫn server, trong khi giới hạn đúng của ảnh bot là 2MB (màn cũ /admin/bot-edit vẫn chặn 2MB). Ảnh trên 2MB (dưới 10MB) qua hết mọi bước kiểm tra và được lưu NGAY khi vừa chọn file (màn này tự lưu ảnh liền), nên không hiện bất kỳ thông báo lỗi nào. Bản spec sprint của màn mới bỏ ngỏ mục giới hạn dung lượng nên khi code lấy nhầm mức 10MB của các màn khác. Lần chạy trước sửa nhầm màn cũ nên bug vẫn tái hiện.

## 2. Cách fix

> Nguyên văn ■ 2. CÁCH FIX

Hạ giới hạn ảnh đại diện bot ở màn Cài đặt kết nối bản mới từ 10MB xuống 2MB cho khớp giới hạn thật của ảnh bot: sửa cả phần kiểm tra phía JS khi chọn file (setting-bot.js) lẫn phía server khi lưu ảnh (SettingBotController@update), cùng đổi nội dung thông báo thành '2MB以下のをアップしてください。' đúng như yêu cầu ticket. Giữ lại phần chặn 2MB phía server ở màn cũ /admin/bot-edit (cùng trường ảnh bot, màn này vẫn còn được liên kết từ danh sách tài khoản, trước đây chỉ cảnh báo phía JS nhưng vẫn lưu ảnh quá cỡ khi bấm lưu). Yokoten: các màn thêm/đổi tài khoản (change_bot.js/change_new_bot.js/olioa.js + ChangeBotController@store) hoàn toàn không kiểm dung lượng nhưng khác phạm vi ticket.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN (Dev list dạng plain → convert sang bảng template)

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SettingBotController@update` — `app/Http/Controllers/Admin/SettingBotController.php` | Có — hạ limit 10MB → 2MB (server-side), đổi message thành `2MB以下のをアップしてください。` | Điểm lưu ảnh phía server của màn MỚI `/admin/setting-bot` — root cause |
| 2 | `onAvatarSelected` / `saveImageImmediately` — `public/js/admin/setting-bot/setting-bot.js` | Có — hạ limit 10MB → 2MB (client-side), đổi message | Kiểm tra phía JS khi chọn file; màn này **tự lưu ảnh ngay khi chọn** |
| 3 | `BotController@botChange` — `app/Http/Controllers/Admin/BotController.php` | Có — giữ/thêm chặn 2MB phía server ở màn CŨ `/admin/bot-edit` | Trước đây chỉ cảnh báo phía JS nhưng **vẫn lưu ảnh quá cỡ** khi bấm lưu |
| 4 | `readURL` — `public/js/admin/bot.js` | Có (đã chặn 2MB từ 2025-12) | Kiểm tra phía JS của màn cũ `/admin/bot-edit` |

> **Yokoten Dev tự nêu nhưng KHÔNG fix (khác phạm vi ticket)** — vùng rủi ro cần Leader cân nhắc:
> `change_bot.js` / `change_new_bot.js` / `olioa.js` + `ChangeBotController@store` (màn thêm / đổi tài khoản) — **hoàn toàn không kiểm dung lượng**.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Nguyên văn ■ 4.1 — Dev list theo **File thay đổi**; cột Function suy từ mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SettingBotController@update` | `app/Http/Controllers/Admin/SettingBotController.php` | Direct | Server-side validate ảnh đại diện bot, màn mới `/admin/setting-bot`. 10MB → 2MB + message mới |
| F2 | `onAvatarSelected` / `saveImageImmediately` | `public/js/admin/setting-bot/setting-bot.js` | Direct | Client-side validate khi chọn file; luồng **auto-save ảnh tức thì** |
| F3 | `BotController@botChange` | `app/Http/Controllers/Admin/BotController.php` | Direct | Server-side chặn 2MB màn cũ `/admin/bot-edit` (trước chỉ chặn JS) |
| F4 | `readURL` | `public/js/admin/bot.js` | Direct | Client-side validate màn cũ `/admin/bot-edit` |
| F5 | `ChangeBotController@store`, `change_bot.js`, `change_new_bot.js`, `olioa.js` | (không sửa) | Indirect — **ngoài phạm vi fix** | Dev xác nhận **không kiểm dung lượng**; đề nghị Leader quyết có test / raise ticket riêng |

**Diff stat Dev báo:** `git diff --stat release_step_20260623...ai_fixbug_39040` → **4 file, +12/-5**.

### 4.2. List data bị update khi fix bug

> Nguyên văn ■ 4.2: "Không có — chỉ thêm/siết bước kiểm tra đầu vào, không đổi cấu trúc hay dữ liệu đã lưu"

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Không có data bị update.** Fix chỉ siết bước validate đầu vào, không đổi cấu trúc DB, không migrate, không đụng dữ liệu ảnh đã lưu |

**■ 5. RECOVER DATA:** ✔ Không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn ■ 4.3

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **LOA Connection Settings (FA-038)** — chặn upload ảnh đại diện bot vượt 2MB + hiện thông báo lỗi, ở **cả màn cài đặt kết nối bản mới (`/admin/setting-bot`) lẫn màn cũ (`/admin/bot-edit`)** | F1, F2, F3, F4 | Medium — hành vi thay đổi có chủ đích (ảnh 2MB–10MB nay bị chặn) |
| T2 | Màn thêm / đổi tài khoản (`change_bot` / `change_new_bot` / `olioa`) | F5 | `<Dev không đánh giá — ngoài phạm vi>`; hiện **không có validate dung lượng** |

---

## Phần bổ sung từ báo cáo Auto-fixbug (không có trong template gốc)

### ■ 6. VERIFY (mức: **lint** — KHÔNG có test chạy thật)

| Loại | Kết quả Dev báo |
|---|---|
| `php -l app/Http/Controllers/Admin/SettingBotController.php` | No syntax errors |
| `node --check public/js/admin/setting-bot/setting-bot.js` | OK |
| `git diff --stat` | 4 file, +12/-5 |

**Bằng chứng Dev nêu:**
- Sidebar bản v2 (`resources/views/layout/v2/admin/sidebar.blade.php:175,182`) trỏ tới route `settingBot` = `/admin/setting-bot` → đây là màn profile bot đang dùng.
- `setting-bot.js` `onAvatarSelected` gọi `saveImageImmediately` ngay khi chọn file → khớp mô tả "chọn ảnh xong là upload thành công".
- Sprint spec **#34620** (`screens/unclear-points.md` **UP-07**) **bỏ ngỏ giới hạn dung lượng ảnh đại diện** → màn mới lấy nhầm mức 10MB.
- Màn cũ `bot.js` chặn 2MB từ 2025-12.
- ⚠️ **Không tái hiện được trên dev** (web `host.docker.internal:8000` không chạy, không có secret Redmine).

### ■ TỰ REVIEW (AI) — rủi ro / lưu ý khi test

- Ảnh đại diện bot **từ 2MB đến 10MB** trước đây lưu được thì nay bị chặn — đây chính là hành vi ticket yêu cầu, **cần PM xác nhận mức 2MB là chuẩn** (spec sprint #34620 bỏ ngỏ mục này; mức 2MB lấy theo màn cũ và theo mô tả của tester).
- Ảnh dưới 2MB không bị ảnh hưởng; luồng **xóa ảnh, đổi tên, đổi secret không đụng tới**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn Leader cần chốt trước khi giao TC

1. **Mức 2MB có phải spec chuẩn không?** — spec sprint #34620 UP-07 bỏ ngỏ; Dev lấy 2MB theo màn cũ + mô tả tester → cần PM / spec xác nhận.
2. **F5 (màn thêm / đổi tài khoản) không kiểm dung lượng** — Dev cố ý bỏ ngoài phạm vi. Leader quyết: test regression hay raise ticket riêng?
3. **Verify mức `lint` + không tái hiện được trên dev** → không có bằng chứng chạy thật từ phía Dev; TC phải verify end-to-end trên env có upload thật (RULE-08: không kết luận từ local).
