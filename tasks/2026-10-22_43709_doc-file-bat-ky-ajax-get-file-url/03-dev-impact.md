# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Reader AI Reader` (dev handoff tự động — journal #146589; `issue.assigned_to` không có) |
| Commit / Pull Request | `<chưa có link PR>` — commit `e5ddae145f` (web) |
| Branch | `ai_fixbug_43709` (web, tạo từ `release_step_20260930_v2`) |
| Ngày submit đánh giá | `2026-10-22` (journal #146589) |
| Auto-filled | `2026-10-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Route `POST /ajax/get-file-url` nằm ngoài group đăng nhập (chỉ có middleware `NotifyChatworkRequestTimeSlow`), và `/ajax/*` nằm trong `$except` của `VerifyCsrfToken` → ai cũng gọi được, không cần login, không cần CSRF token.
- `BasicController::getFileUrl()` ghép thẳng `link_url` vào `public_path()` rồi `file_get_contents()`, không kiểm tra path → gửi `link_url=/../.env` là nhận được nội dung `.env` (mật khẩu DB, `APP_KEY`, key Stripe/Univapay/LINE) dạng base64.
- Nhánh fallback ghép `env('URL_SERVER_MEDIA') . link_url`: path chứa `../` được chuyển nguyên sang server media; nếu `URL_SERVER_MEDIA` rỗng thì thành đọc file theo đường dẫn tuyệt đối bất kỳ trên server.

## 2. Cách fix

- Route: thêm middleware `check_login`, `check_remember_token` (chưa đăng nhập → HTTP 401 JSON).
- Thêm `GetFileUrlRequest`: `link_url` bắt buộc, kiểu chuỗi, tối đa 2048 ký tự.
- Tách logic sang `MediaFileService::readMediaFile()`:
  - Chỉ nhận path tương đối dạng `/{FOLDER_MEDIA}media/...` (vd `/ext-media-step/media/pdf/...`); chặn segment `.` và `..` (cả dạng urlencode `%2e%2e`), ký tự `\`, NUL, URL đầy đủ/scheme (`https://`, `php://`).
  - File local: `realpath()` phải nằm trong đúng thư mục `{FOLDER_MEDIA}media` tương ứng.
  - Fallback sang server media chỉ chạy khi `URL_SERVER_MEDIA` là URL http(s); thêm timeout 15s.
- Response lỗi trả đúng HTTP status, msg tiếng Nhật: `422` path không hợp lệ, `404` không tìm thấy file, `502` server media lỗi. Ghi log khi từ chối request.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `public/js/form_answer/form_result.js` → `downloadFile()` (màn 回答結果 form v2) | Không | Đã check, không ảnh hưởng |
| 2 | `public/js/form_answer/form_result_v3.js` → `downloadFile()` (màn 回答結果 form v3) | Không | Đã check, không ảnh hưởng |
| 3 | `resources/views/basic/form_answer/detail_form_result.blade.php` → `downloadFile()` (chi tiết kết quả form) | Không | Đã check, không ảnh hưởng |
| 4 | `public/js/infor_friend/list_friend_info.js` → `downloadFile()` (màn danh sách friend theo 友だち情報) | Không | Đã check, không ảnh hưởng |
| 5 | `public/js/my_page/my_page.js` → `downloadFile()` (my page friend: mypage_v2) | Không | Đã check, không ảnh hưởng |
| 6 | `public/js/basic/friend-list/friend-info.js` → `downloadFile()` dùng `window.open`, không gọi endpoint này | Không | Không ảnh hưởng |

Ghi chú thêm của Dev (không thuộc dạng bảng caller nhưng quan trọng cho TC):
- Tất cả màn gọi endpoint đều là màn `/basic` đã đăng nhập nên vẫn qua được `check_login`.
- Đã check giá trị file lưu trong DB (`FormAnswerResult.data`, `friend_information_value.value`) đều dạng `/{FOLDER_MEDIA}media/...` → khớp điều kiện mới.
- Đã test local: chưa đăng nhập → 401; các payload `/../.env`, `media/../`, `%2e%2e`, `..\`, NUL, file ngoài media, `https://`, `php://` → 422; file hợp lệ trong media → tải được. **Chưa test nhánh lấy file từ server media (`URL_SERVER_MEDIA`) → cần test trên staging.**

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getFileUrl()` | `app/Http/Controllers/Basic/BasicController.php` | Direct | Hàm chính bị sửa — chuyển logic path/đọc file sang `MediaFileService` |
| F2 | route `POST /ajax/get-file-url` | `routes/web.php` | Direct | Thêm middleware `check_login`, `check_remember_token` |
| F3 | `MediaFileService::readMediaFile()` / `mediaFolderPrefix()` / `fetchFromMediaServer()` | `app/Services/MediaFileService.php` (file mới) | Direct | Tách logic validate path + đọc file local/fallback server media |
| F4 | `GetFileUrlRequest::rules()` / `failedValidation()` | `app/Http/Requests/GetFileUrlRequest.php` (file mới) | Direct | Validate input `link_url` (bắt buộc, string, ≤2048 ký tự) |

### 4.2. List data bị update khi fix bug

Không có — Dev ghi "k có" (chỉ thay đổi logic validate/middleware, không chạm DB/migration/cache).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Bản thân endpoint `/ajax/get-file-url` (bảo mật: chặn chưa đăng nhập + path traversal + đọc file ngoài media) | F1, F2, F3, F4 | High — mục tiêu chính của fix, phải verify đủ cả 2 lớp chặn (login + path) |
| T2 | Tải file đính kèm (PDF/ảnh) ở màn 回答結果 form v2, v3 và màn chi tiết kết quả form | F1, F3, F4 | Medium — happy path + hành vi lỗi đổi từ `200 success:false` sang `4xx/5xx thật`, FE cần xử lý đúng, không tải file rỗng |
| T3 | Tải file ở màn danh sách friend theo 友だち情報 | F1, F3, F4 | Medium |
| T4 | Tải file ở my page friend | F1, F3, F4 | Medium — Dev liệt kê nhưng cần xác nhận lại route/view thực tế còn render (xem GAP ở report) |
| T5 | Case dữ liệu cũ lưu URL tuyệt đối `https://...` (trước fix vốn đã không tải được) | F3, F4 | Low — không phải regression thật vì đã hỏng từ trước, nay chỉ đổi mã lỗi thành 422 |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
