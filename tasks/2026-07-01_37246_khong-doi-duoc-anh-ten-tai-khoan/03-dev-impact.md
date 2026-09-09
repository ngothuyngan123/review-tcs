# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` |
| Commit / Pull Request | `commit d2060d35b0` (repo sns-line, 1 file) |
| Branch | `ai_fixbug_37246` (nhánh gốc `release_step_20260511`) |
| Ngày submit đánh giá | `2026-06-23` |
| Auto-filled | `2026-07-01 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi đổi ảnh/tên tài khoản từ trang cài đặt hiển thị tài khoản LINE, backend **LUÔN** gọi lại LINE để xác thực Channel Secret của Messaging API — kể cả khi người dùng không đổi secret. Nếu secret đang lưu bị trống hoặc đã cũ/không còn hợp lệ thì lần xác thực này thất bại và chặn thao tác, hiện thông báo thông tin nhập sai, dù người dùng chỉ đổi ảnh/tên.

## 2. Cách fix

Chỉ xác thực lại token khi Channel Secret **thực sự thay đổi** (so với giá trị đang lưu), giống cách phần đăng nhập LINE đã làm. Khi chỉ đổi ảnh/tên (không đụng secret) thì bỏ qua bước xác thực này nên lưu được bình thường. Đồng thời không còn ghi đè secret bằng giá trị rỗng khi người dùng không đổi secret.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SettingBotController@update` — khối Messaging Channel Secret | Đã thêm guard `secretChanged` | Chỉ re-validate token khi secret thật sự đổi |
| 2 | `SettingBotController@getData` | FE nhận `channel_secret` thật (không mask) | Để so sánh `secretChanged` chính xác |
| 3 | `public/js/admin/setting-bot/setting-bot.js` | 3 luồng lưu (đổi ảnh / đổi tên / nút Lưu) đều gửi lại secret cũ khi không đổi | Đảm bảo BE so sánh đúng, không nhầm "đã đổi" |
| 4 | `validateTokenAddBot` (functions.php) | Không sửa — trả 0 khi token rỗng/không hợp lệ | Đúng là nguồn thông báo lỗi |
| 5 | Khối LINE Login (trong cùng hàm) | Không sửa — đã guard sẵn | Dùng làm chuẩn đối chiếu cho fix |
| 6 | `BotController` (luồng thêm bot, cùng message) | **KHÔNG đụng** | Re-validate ở đó là đúng nghiệp vụ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SettingBotController@update` (khối Messaging Channel Secret) | `app/Http/Controllers/Admin/SettingBotController.php` | Direct | Thêm guard `secretChanged`; file DUY NHẤT thay đổi |
| F2 | `SettingBotController@getData` | `app/Http/Controllers/Admin/SettingBotController.php` | Direct | Trả secret thật (không mask) để so sánh |
| F3 | `public/js/admin/setting-bot/setting-bot.js` (3 luồng lưu) | (JS) | Direct | Gửi lại secret cũ khi không đổi |
| F4 | `validateTokenAddBot` (functions.php) | `functions.php` | Indirect | Nguồn sinh message lỗi; behavior giữ nguyên |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `channel_secret` (Channel Secret của bot) | (bảo toàn) | Fix đảm bảo KHÔNG ghi đè `channel_secret` bằng giá trị rỗng khi user không đổi secret. **Không** thay đổi schema/migration. |

> Dev ghi: "4.2 Data ảnh hưởng: Không có — chỉ đổi luồng điều kiện, không thay đổi schema/dữ liệu." D1 ở trên là data cần **verify không bị hư hại** (không phải data bị migrate), tách ra để làm rõ risk.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Cài đặt hiển thị tài khoản LINE (「LINE公式アカウント表示設定」) — đổi ảnh/tên | F1, F2, F3 | Medium — đổi ảnh/tên hoạt động bình thường, hết báo lỗi sai khi không đổi secret |
| T2 | Đổi Messaging API Channel Secret | F1, F4 | Medium — vẫn xác thực lại token đúng như cũ khi secret thật sự thay đổi |
| T3 | An toàn dữ liệu Channel Secret | D1 | Medium — không còn ghi đè `channel_secret` bằng rỗng khi user không đổi secret |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Nguồn: Redmine #37246 journal id 123212 (AI AUTO-FIXBUG report), created_on 2026-06-23. -->
