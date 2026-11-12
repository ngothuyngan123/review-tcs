# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43827 — confirmPassword api không cần validate token cũng đổi được pass` |
| Module / Màn hình | Reset Password — đặt lại mật khẩu qua link email (reset-password v2 / v3) · API `POST /confirm_password` (`AuthController@confirmPassword`) |

## Mô tả bug (bản dịch tiếng Việt)

Endpoint `POST /confirm_password` (`AuthController@confirmPassword`) xác định user cần đổi mật khẩu bằng field `id` lấy trực tiếp từ request, KHÔNG validate `reset_token`, không auth, không kiểm owner.

Token chỉ được kiểm khi render trang GET (`resetPasswordV3`) rồi nhúng cả object user vào HTML; đến bước POST đổi mật khẩu thì bỏ qua token → chỉ tin `id`. Vì `id` là auto-increment (đoán/duyệt tuần tự được) nên bất kỳ ai cũng POST với `id` bất kỳ + mật khẩu hợp format là đổi được mật khẩu của tài khoản đó (chiếm tài khoản, không cần đăng nhập/email/token).

## Steps to reproduce

> ⚠️ Ticket không có section "Tái hiện bug" riêng (tracker "Bug tự detect" — AI tự phát hiện, không phải khách hàng báo). Steps dưới đây suy trực tiếp từ phần "Nguyên nhân" Dev mô tả trong Journal #146856, không bịa thêm.

1. Vào màn hình đặt lại mật khẩu (reset-password v2 hoặc v3) — hoặc gọi trực tiếp API, không cần có link email hợp lệ.
2. Gửi request `POST /confirm_password` với field `id` = id (auto-increment, đoán/duyệt được) của BẤT KỲ user khác, KHÔNG kèm `reset_token` hợp lệ tương ứng user đó, KHÔNG đăng nhập. Kèm `password` mới hợp format.
3. Server xác định user cần đổi mật khẩu bằng `id` lấy trực tiếp từ request — không validate token/owner.

## Expected result

- API phải từ chối (ví dụ `422`) khi không có `reset_token` hợp lệ khớp đúng user; KHÔNG được đổi mật khẩu chỉ dựa vào `id`.

## Actual result

- API đổi mật khẩu thành công cho user ứng với `id` bất kỳ trong request, không cần token hợp lệ / email / đăng nhập → chiếm được tài khoản của người khác (account takeover / IDOR).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #43827 không có attachment nào. -->

## Ghi chú thêm của Leader

- Tracker "Bug tự detect" — bug do AI phát hiện, không phải khách hàng báo lỗi. Ticket không ghi môi trường phát hiện cụ thể.
- Đây là lỗ hổng bảo mật nghiêm trọng (account takeover qua IDOR ở endpoint đổi mật khẩu) — cần test kỹ cả 2 luồng reset-password v2 và v3, và xác nhận luồng mobile (`change_password` → `AuthController@change`) KHÔNG dùng endpoint này nên không bị ảnh hưởng (theo khẳng định của Dev ở mục 3, file 03).

## Journal / note từ Redmine (nguyên văn)

**Journal #146856 — AI Reader AI Reader — 2026-10-22:**

```
Bug tự detect #43827: confirmPassword api không cần validate token cũng đổi được pass
1. Nguyên nhân
    - Endpoint POST /confirm_password (AuthController@confirmPassword) xác định user cần đổi mật khẩu bằng field `id` lấy trực tiếp từ request, KHÔNG validate `reset_token`, không auth, không kiểm owner.
    - Token chỉ được kiểm khi render trang GET (resetPasswordV3) rồi nhúng cả object user vào HTML; đến bước POST đổi mật khẩu thì bỏ qua token → chỉ tin `id`. Vì `id` là auto-increment (đoán/duyệt tuần tự được) nên bất kỳ ai cũng POST với `id` bất kỳ + mật khẩu hợp format là đổi được mật khẩu của tài khoản đó (chiếm tài khoản, không cần đăng nhập/email/token).
2. Cách fix
    - Định danh user LẤY TỪ `reset_token` (User::where('reset_token', $token)), bỏ hẳn dùng `id` từ request.
    - Thêm validate token: required + exists:users,reset_token; kiểm hết hạn 24h (reset_token_expired), đồng bộ với resetPasswordV3.
    - Giữ nguyên: check độ mạnh mật khẩu, chặn mật khẩu đã dùng gần đây, revoke OAuth refresh token, set reset_token = null sau khi đổi (token dùng 1 lần).
    - FE 2 trang reset gửi `token` thay cho `id` (reset_token sẵn có trong object user truyền ra view, không nằm trong $hidden).
    - Thêm logInfo cho hành động đổi mật khẩu (không log giá trị token).
3. Đã check và sửa các function sử dụng đến function/data vừa sửa
    - Grep toàn bộ caller của route('confirmPassword') / /confirm_password: chỉ 2 blade reset_password_v2 và reset-password-v3 gọi → đã sửa đồng thời (gửi token thay id).
    - Luồng mobile reset mật khẩu dùng endpoint khác (change_password → AuthController@change, vốn đã validate token) → KHÔNG ảnh hưởng.
    - 2 file JS khác trùng chuỗi confirmPassword (public/js/my_page/index.js, public/js/admin/list_bot_enterprise.js) chỉ là tên biến/field hoặc endpoint khác → không gọi route này.
4. Đánh giá ảnh hưởng
  4.1 List function liên quan
        - app/Http/Controllers/AuthController.php
            + confirmPassword()
        - resources/views/auth/auth-v3/reset-password-v3.blade.php
            + confirmPassword() (Vue method) — payload gửi token thay cho id
        - resources/views/auth/reset_password_v2.blade.php
            + confirmPassword() (Vue method) — payload gửi token thay cho id
  4.2 List những data bị update khi fix bug
        - Fix KHÔNG đổi danh sách field bị ghi, chỉ đổi ĐIỀU KIỆN xác định user (id → reset_token).
        - Các field endpoint ghi (giữ nguyên như trước): users.password, users.is_active, users.reset_token, users.remember_token_reset_pass; oauth_refresh_tokens.is_revoked.
  4.3 Tính năng có thể bị ảnh hưởng
        - Màn hình đặt lại mật khẩu qua link email (reset-password v2 và v3) → đặt mật khẩu mới.
        - Caller nào POST /confirm_password mà thiếu token sẽ bị 422 (đúng ý đồ bảo mật) — đã rà chỉ 2 blade web, luồng mobile không dùng endpoint này.

---
Branch / Commit
    - Branch: ai_fixbug_43827 (đã push origin)
    - Commit: efbc04e51f
    - Tạo PR: https://bitbucket.org/snstool/sns-line/pull-requests/new?source=ai_fixbug_43827
```
