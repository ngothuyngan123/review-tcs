# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio (dev-studio@api — ghi nhận tự động qua Redmine journal; assignee issue để trống, chưa có Dev người xác nhận trực tiếp)` |
| Commit / Pull Request | `<chưa có — chỉ có branch, chưa thấy link PR trong Redmine>` |
| Branch | `ai_studio_fixbug_44046 (nhánh gốc release_step_20260930_v2 @3351f2aaa78d, commit ef35b6f6878846c9d353c4e59c617bb6e715b8cd, repo sns-line)` |
| Ngày submit đánh giá | `2026-10-23` (journal #147445; có bản sơ bộ ngày 2026-10-22 ở journal #147315) |
| Auto-filled | `2026-10-23 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Ghi chú auto-fill: Redmine #44046 **không có section "Đánh giá ảnh hưởng" theo format chuẩn 4 mục** — nội dung dưới đây được suy ra/mapping từ 2 journal note của Dev Studio (nguyên văn ở file `01-bug-task.md`). Cần Leader đọc lại journal gốc trước khi tick checkbox trên.

---

## 1. Nguyên nhân

`ChatController::ajaxDownloadFileChat11` chỉ kiểm `link_url` là chuỗi. Sau đó nó ghép thẳng vào `public_path()` (hoặc lấy phần path của URL rồi ghép vào `public_path()`) và đọc bằng `file_get_contents`, nên `/../.env` hay `http://x/../.env` trả về nội dung .env. Với URL đầy đủ, server tải đúng URL client gửi mà không giới hạn host, nên gọi được tới host nội bộ hoặc metadata (SSRF). Route nằm trong `/ajax` (chỉ yêu cầu đăng nhập, miễn CSRF), nên mọi tài khoản đăng nhập đều khai thác được.

→ 2 lỗ hổng gộp trong cùng 1 BUG: **(a) Path traversal / arbitrary file read** (đọc file ngoài ý muốn qua `../`, `php://`, `file://`, NUL byte…) và **(b) SSRF** (server gọi tới host do client chỉ định trong `link_url` dạng URL đầy đủ).

## 2. Cách fix

- **D-1**: Thêm `MediaFileService::readChatDownloadFile` — chỉ cho đọc file trong **thư mục media allowlist** (`CHAT_DOWNLOAD_FOLDERS`) hoặc tải từ **media server** / **Dropbox** (host khớp `DROPBOX_HOSTS` / `*.dropboxusercontent.com`).
- **D-2**: `ajaxDownloadFileChat11` gọi service mới; **path xấu trả 422** 「ファイルのパスが正しくありません。」, giữ nguyên **502/500** 「ダウンロードに失敗しました。」 cho file không tồn tại / media server lỗi như cũ.
- Chi tiết hành vi mới:
  - Path chứa `..`, `\`, NUL, `php://`, `file://`… (kể cả lồng trong URL host) → từ chối 422, không lộ nội dung.
  - URL đầy đủ có host lạ/nội bộ → server **không** gọi tới host đó nữa; chỉ lấy phần path, đọc theo local allowlist hoặc media server. Riêng Dropbox (host khớp allowlist) vẫn tải thẳng.
  - `link_url` dài quá 2048 ký tự → lỗi validate 422.
  - `type=audio` → cắt phần `?query` trước khi xử lý path.
  - Symlink trong thư mục allowlist trỏ ra ngoài (qua `realpath`) → 422.
  - File không tồn tại / media server lỗi → giữ như cũ, 502.
- File đã sửa (repo `sns-line`, nhánh `ai_studio_fixbug_44046`):
  - `app/Http/Controllers/ChatController.php` (85 dòng, rút gọn — chuyển logic sang service)
  - `app/Services/MediaFileService.php` (136 dòng mới — toàn bộ logic allowlist/SSRF-guard/Dropbox/media-server fallback)
- Migration / thay đổi dữ liệu: **Không có** (Dev xác nhận qua diff).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::ajaxDownloadFileChat11` (gọi từ `chat-v2.js downLoadFile`) | Gọi `MediaFileService::readChatDownloadFile` mới thay cho đọc file trực tiếp | Entry point của lỗ hổng — nơi chính được sửa |
| 2 | Header nút 「ダウンロード」 QR (`layout_v2_header.js`) | Trước gửi URL tuyệt đối ảnh QR → nay đi theo path `qr_image` | Dùng chung endpoint `/ajax/download-file-chat11` |
| 3 | Cài đặt thêm bạn 「新規友だち用」 / bỏ chặn 「ブロック解除友だち用」 (`setting-add-friend-new.js`) | QR dạng `URL_SERVER_MEDIA + FOLDER_MEDIA + qr_image` | Dùng chung endpoint |
| 4 | QR code v2 — danh sách QR + modal URL, tab 「QRコード表示」 (`qr_code/v2/index.js`, `mixins/qr_display_tab.js`) | Ảnh landing `FOLDER_MEDIA images` | Dùng chung endpoint |
| 5 | `/ajax/get-file-url` (`BasicController::getFileUrl` — form answer, friend info) | Dùng chung `MediaFileService`; helper kiểm path (`hasUnsafeSegment`) được **tách riêng** nhưng Dev khẳng định hành vi giữ nguyên | Regression risk — đổi helper dùng chung, cần verify không chặn nhầm case hợp lệ cũ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::ajaxDownloadFileChat11` (`POST /ajax/download-file-chat11`) | `app/Http/Controllers/ChatController.php` | Direct | Entry point lỗ hổng; sửa để gọi service mới, path xấu trả 422 |
| F2 | `MediaFileService::readChatDownloadFile` (mới) | `app/Services/MediaFileService.php` | Direct | Toàn bộ logic mới: allowlist thư mục, chống SSRF, Dropbox, fallback media server |
| F3 | `MediaFileService::hasUnsafeSegment` / `isDropboxHost` / `fetchFromDropbox` / `fetchFromMediaServer` (helper nội bộ) | `app/Services/MediaFileService.php` | Direct | Helper hỗ trợ F2; `hasUnsafeSegment` dùng chung với F4 |
| F4 | `BasicController::getFileUrl` (`/ajax/get-file-url`) | `app/Http/Controllers/BasicController.php` | Indirect | Dùng chung helper `hasUnsafeSegment` sau khi tách ra khỏi logic cũ — Dev khẳng định hành vi giữ nguyên, cần test regression (liên quan `TICKET-43709`, đối chiếu bug cũ 3721 — double-encode `%252e%252e`) |

### 4.2. List data bị update khi fix bug

**Không có** — Dev xác nhận qua diff: không có migration, không tạo/sửa/xoá bảng DB, field, cache hay config nào. Endpoint chỉ **đọc** file, không ghi dữ liệu.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 — nút tải ảnh/video/audio/file trong khung hội thoại (bao gồm tin có URL tuyệt đối dữ liệu cũ) + preview mẫu tin (kể cả video Dropbox) | F1, F2, F3 | High — chứa chính lỗ hổng, đổi toàn bộ logic đọc file; dữ liệu cũ (URL domain khác) có thể đổi hành vi từ tải được → 502 |
| T2 | Header 「友だち追加情報」 — nút tải QR | F1, F2 | Medium |
| T3 | Cài đặt thêm bạn mới 「新規友だち用」 / Cài đặt bỏ chặn 「ブロック解除友だち用」 — nút tải QR | F1, F2 | Medium |
| T4 | QR code v2 — danh sách QR + modal URL, tab 「QRコード表示」 — nút tải QR | F1, F2 | Medium |
| T5 | `/ajax/get-file-url` — tải file đính kèm form answer, friend info | F4 | Medium — regression do tách chung helper validate path |
| T6 | **(Security — không phải feature end-user)** Chặn path traversal (`../`, `php://`, `file://`, NUL, symlink ra ngoài) + chặn SSRF (host nội bộ/metadata/host lạ) qua endpoint `/ajax/download-file-chat11` | F1, F2, F3 | High — mục tiêu chính của fix; đây là nhóm TC quan trọng nhất (abnormal/security), không phải "feature" thông thường nhưng phải có coverage riêng ở §1/§2 report |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
