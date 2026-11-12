# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Redmine không gán assignee; journal đánh giá do "AI Reader AI Reader" đăng>` |
| Commit / Pull Request | `efbc04e51f` — tạo PR: https://bitbucket.org/snstool/sns-line/pull-requests/new?source=ai_fixbug_43827 |
| Branch | `ai_fixbug_43827` (đã push origin) |
| Ngày submit đánh giá | `2026-10-22` |
| Auto-filled | `2026-10-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Endpoint `POST /confirm_password` (`AuthController@confirmPassword`) xác định user cần đổi mật khẩu bằng field `id` lấy trực tiếp từ request, KHÔNG validate `reset_token`, không auth, không kiểm owner.
- Token chỉ được kiểm khi render trang GET (`resetPasswordV3`) rồi nhúng cả object user vào HTML; đến bước POST đổi mật khẩu thì bỏ qua token → chỉ tin `id`. Vì `id` là auto-increment (đoán/duyệt tuần tự được) nên bất kỳ ai cũng POST với `id` bất kỳ + mật khẩu hợp format là đổi được mật khẩu của tài khoản đó (chiếm tài khoản, không cần đăng nhập/email/token).

## 2. Cách fix

- Định danh user LẤY TỪ `reset_token` (`User::where('reset_token', $token)`), bỏ hẳn dùng `id` từ request.
- Thêm validate token: `required` + `exists:users,reset_token`; kiểm hết hạn 24h (`reset_token_expired`), đồng bộ với `resetPasswordV3`.
- Giữ nguyên: check độ mạnh mật khẩu, chặn mật khẩu đã dùng gần đây, revoke OAuth refresh token, set `reset_token = null` sau khi đổi (token dùng 1 lần).
- FE 2 trang reset gửi `token` thay cho `id` (`reset_token` sẵn có trong object user truyền ra view, không nằm trong `$hidden`).
- Thêm `logInfo` cho hành động đổi mật khẩu (không log giá trị token).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `reset_password_v2.blade.php` (Vue `confirmPassword()`) | Payload gửi `token` thay cho `id` | Caller của `route('confirmPassword')` / `/confirm_password` |
| 2 | `auth-v3/reset-password-v3.blade.php` (Vue `confirmPassword()`) | Payload gửi `token` thay cho `id` | Caller của `route('confirmPassword')` / `/confirm_password` |
| 3 | `AuthController@change` (`change_password`, luồng mobile) | Không đổi | Dùng endpoint khác, vốn đã validate token → KHÔNG ảnh hưởng (Dev khẳng định) |
| 4 | `public/js/my_page/index.js`, `public/js/admin/list_bot_enterprise.js` | Không đổi | Trùng chuỗi `confirmPassword` nhưng là tên biến/field hoặc endpoint khác, không gọi route này |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `confirmPassword()` — `POST /confirm_password` | `app/Http/Controllers/AuthController.php` | Direct | Core fix: đổi từ xác định user theo `id` → theo `reset_token`; thêm validate `required`+`exists:users,reset_token`+hết hạn 24h |
| F2 | `confirmPassword()` (Vue method) | `resources/views/auth/auth-v3/reset-password-v3.blade.php` | Direct | FE gửi `token` thay cho `id` trong payload POST |
| F3 | `confirmPassword()` (Vue method) | `resources/views/auth/reset_password_v2.blade.php` | Direct | FE gửi `token` thay cho `id` trong payload POST |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `users.password` | UPDATE | Field ghi giữ nguyên như trước fix — chỉ đổi ĐIỀU KIỆN xác định user (`id` → `reset_token`) |
| D2 | `users.reset_token` | UPDATE | Set `null` sau khi đổi mật khẩu (token dùng 1 lần); sau fix còn là field dùng để TÌM user (`where reset_token = $token`) thay cho `id` |
| D3 | `users.is_active` | UPDATE | Giữ nguyên hành vi như trước fix |
| D4 | `users.remember_token_reset_pass` | UPDATE | Giữ nguyên hành vi như trước fix |
| D5 | `oauth_refresh_tokens.is_revoked` | UPDATE | Revoke refresh token sau khi đổi mật khẩu — giữ nguyên hành vi như trước fix |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đặt lại mật khẩu qua link email — reset-password v2 | F1, F3, D1, D2, D4, D5 | High (fix bảo mật trực tiếp trên luồng chính) |
| T2 | Đặt lại mật khẩu qua link email — reset-password v3 | F1, F2, D1, D2, D4, D5 | High (fix bảo mật trực tiếp trên luồng chính) |
| T3 | Đăng nhập / phiên OAuth sau khi đổi mật khẩu (revoke refresh token) | F1, D5 | Medium — logic revoke giữ nguyên nhưng chỉ chạy nếu luồng đổi mật khẩu tới được bước này sau khi fix |
| T4 | Đổi mật khẩu qua app mobile (`change_password` → `AuthController@change`) | Mục 3 #3 | Low — Dev khẳng định dùng endpoint khác, không bị chạm; cần 1 TC regression xác nhận độc lập |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
