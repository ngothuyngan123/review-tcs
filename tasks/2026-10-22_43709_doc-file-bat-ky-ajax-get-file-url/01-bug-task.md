# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43709 — Đọc file bất kỳ trên server qua /ajax/get-file-url (lấy được .env)` |
| Module / Màn hình | Bug tự detect (security) — endpoint `POST /ajax/get-file-url` (`BasicController::getFileUrl()`), dùng chung bởi màn 回答結果 form v2/v3, danh sách friend theo 友だち情報, my page friend |

## Mô tả bug (bản dịch tiếng Việt)

Loại: File, upload & đọc file.

Tác động / cách khai thác: Gửi `link_url=/../.env` → nhận được nội dung file cấu hình: mật khẩu DB, APP_KEY, key Stripe/Univapay/LINE. Không cần đăng nhập, không có CSRF.

Vị trí code: `app/Http/Controllers/Basic/BasicController.php:2755` · route `POST /ajax/get-file-url` (`routes/web.php:4248`).

Cách sửa (đề xuất của người báo cáo): Bắt đăng nhập; dùng `realpath()` và chỉ cho đọc trong thư mục media; chặn `..` (nội dung Redmine bị cắt ở đây, phần fix chi tiết thực tế xem file `03-dev-impact.md`).

## Steps to reproduce

1. Không đăng nhập (không có session cookie hợp lệ) — route gốc nằm ngoài group middleware đăng nhập.
2. Gửi `POST /ajax/get-file-url` với tham số `link_url=/../.env` (path traversal ra ngoài thư mục media, trỏ tới file cấu hình gốc của ứng dụng).
3. Server không kiểm tra path trước khi `file_get_contents()`.

## Expected result

- Request không đăng nhập phải bị chặn (401), hoặc nếu đã đăng nhập thì path đi ra ngoài thư mục media phải bị từ chối (422) — không được trả về nội dung file ngoài thư mục media dưới bất kỳ dạng nào (kể cả base64).

## Actual result

- Server trả về HTTP 200 kèm nội dung file `.env` (dạng base64): mật khẩu DB, `APP_KEY`, key Stripe/Univapay/LINE. Không cần đăng nhập, không có CSRF token.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue #43709 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

⚠️ Đây là **bug tự detect (security/pentest)**, không phải báo cáo từ khách hàng — tracker "Bug tự detect", không có section "Tái hiện bug" riêng trong Redmine. Steps/Expected/Actual ở trên được suy từ mục "Tác động / cách khai thác" + nội dung đánh giá ảnh hưởng của Dev (xem file `03-dev-impact.md`), không phải nguyên văn một section riêng.

Route `/ajax/get-file-url` nằm ngoài middleware đăng nhập và nằm trong `$except` của `VerifyCsrfToken` → khai thác được từ bên ngoài, không cần tài khoản, không cần CSRF token.

Dev ghi rõ: **chưa test nhánh fallback lấy file từ server media (`URL_SERVER_MEDIA`)** trên local — cần test trên staging/production (xem T-impact tương ứng ở file 03).

## Dữ liệu định danh ca lỗi

<!-- Không có ca lỗi cụ thể (không gắn với 1 bot/friend nào) — đây là lỗi logic ở tầng endpoint, áp dụng cho mọi bot/mọi dữ liệu. -->

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #146589 (AI Reader AI Reader, 2026-10-22) chính là nội dung "Đánh giá ảnh hưởng phía dev" — đã chuyển nguyên văn vào file 03-dev-impact.md theo đúng 4 mục, không chép lại trùng ở đây. -->
