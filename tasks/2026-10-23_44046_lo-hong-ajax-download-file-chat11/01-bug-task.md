# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44046 — Tìm thấy lỗ hổng router /ajax/download-file-chat11 này lấy được env hoặc các file nhạy cảm khác` |
| Module / Màn hình | `Chat 1:1 (feature chat-1on1) — endpoint POST /ajax/download-file-chat11 (ChatController::ajaxDownloadFileChat11 + MediaFileService), dùng chung cho: nút tải tệp trong khung chat, nút tải QR ở header 「友だち追加情報」, cài đặt thêm bạn/bỏ chặn, QR code v2 (list + tab hiển thị)` |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ **Input thiếu**: Redmine issue #44046 **không có nội dung `description`** (trống) và **không có section "Tái hiện bug"**. Tracker = **"Bug tự detect"** → đây là lỗ hổng security do hệ thống/Dev tự rà soát phát hiện, không phải báo cáo tái hiện từ end-user/khách hàng. Toàn bộ nội dung điều tra nằm ở 2 journal note của Dev (chép nguyên văn ở section cuối file này).

Tóm tắt ngắn (dịch từ journal, không phải mô tả gốc của ticket):

`ChatController::ajaxDownloadFileChat11` chỉ kiểm `link_url` là chuỗi, rồi ghép thẳng vào `public_path()` (hoặc ghép phần path của URL vào `public_path()`) và đọc bằng `file_get_contents` — nên path traversal (`/../.env`, `http://x/../.env`) đọc được nội dung `.env`. Với URL đầy đủ, server gọi đúng URL client gửi mà không giới hạn host → SSRF (gọi được host nội bộ / metadata). Route nằm trong `/ajax` (chỉ yêu cầu đăng nhập, miễn CSRF) → **mọi tài khoản đăng nhập đều khai thác được**.

## Steps to reproduce

1. _(trống — Redmine không có section Tái hiện bug)_

## Expected result

- _(trống)_

## Actual result

- _(trống)_

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

_(issue.attachments = 0 — không có attachment)_

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine theo nghĩa thông thường** — đây là lỗ hổng security (path traversal + SSRF) do Dev tự rà soát code phát hiện (tracker "Bug tự detect"), root cause + hướng fix đã được Dev confirm đầy đủ qua 2 journal (file 03). TCs nên tập trung verify **cách fix chặn đúng payload độc hại** + **regression 5 luồng tải file/QR hợp pháp** + **regression `/ajax/get-file-url`**.
- Lỗ hổng được Dev xác nhận tồn tại từ **2024-10-21** đến nay (tức khoảng **2 năm**) và chỉ cần 1 tài khoản đăng nhập là khai thác được — mức độ rủi ro security rất cao, phạm vi production.
- **Việc Operations cần quyết định (NGOÀI phạm vi viết/review TC của task này — chỉ ghi nhận cho Leader theo dõi, không tạo TC)**:
  - Rà soát log truy cập xem lỗ hổng đã bị khai thác chưa (log hiện không ghi `link_url`/body POST).
  - Xoay vòng secret trong `.env` production (`APP_KEY`, mật khẩu DB, key LINE/Stripe/Univapay).
- **2 lỗ hổng cùng lớp lỗi — Dev đề nghị mở ticket riêng (KHÔNG thuộc phạm vi test của #44046)**:
  - `ImageRichmenuController::getCreateDownload` (`GET /rich-image/get-create-download`) — `response()->download(public_path() . fileName)`, cùng lớp lỗi đọc file tuỳ ý.
  - `BasicController::checkFileExist` (`/ajax/check-file-exist`, **không cần đăng nhập**) — cho dò file tồn tại + gửi HEAD tới `URL_SERVER_MEDIA + link_url`.
- Dev note thêm 1 điểm cần xem xét: file CSV lịch sử truy cập admin lưu ở `public/msg_template/access-histories-bot` với tên theo timestamp — ai đoán được tên thì tải được qua HTTP (không phải scope sửa của #44046, Dev chỉ ghi nhận).
- Recover dữ liệu: **không cần** — endpoint chỉ đọc, không ghi/làm hỏng dữ liệu (Dev đã xác nhận qua diff, không có migration).
- Môi trường đã có TCs chạy: **STAGING** (38/38 TC). Chưa chạy trên **production** → theo RULE-08 không thể kết luận domain/media-server behavior (vd nhánh "file chỉ có trên domain web khác media server sẽ không tải được") từ staging — Dev cũng tự note cần kiểm trên staging/production riêng.
- Nhánh dữ liệu cũ cần chú ý khi review: tin chat cũ lưu `content` là **URL tuyệt đối trên domain web khác** (vd `sns.`/`booking.`) — sau fix, server **bỏ host** trong URL, chỉ lấy path → nếu file chỉ tồn tại ở domain đó (không có ở local allowlist/media server) thì sẽ đổi hành vi từ "tải được" → "502 lỗi" (COMPAT-LEGACY-001, Studio case NEW-26).

## Journal / note từ Redmine (nguyên văn)

**Journal #147315 — Dev Studio — 2026-10-22:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
`ChatController::ajaxDownloadFileChat11` chỉ kiểm `link_url` là chuỗi. Sau đó nó ghép thẳng vào `public_path()` (hoặc lấy phần path của URL rồi ghép vào `public_path()`) và đọc bằng `file_get_contents`, nên `/../.env` hay `http://x/../.env` trả về nội dung .env. Với URL đầy đủ, server tải đúng URL client gửi mà không giới hạn host, nên gọi được tới host nội bộ hoặc metadata (SSRF). Route nằm trong `/ajax` (chỉ yêu cầu đăng nhập, miễn CSRF), nên mọi tài khoản đăng nhập đều khai thác được.

Hướng sửa:
- D-1 Thêm MediaFileService::readChatDownloadFile chỉ cho đọc file trong thư mục media hoặc tải từ media server/Dropbox
- D-2 ajaxDownloadFileChat11 gọi service mới, path xấu trả 422, giữ 502/500 như cũ

Ảnh hưởng / rủi ro:
Chỉ endpoint POST /ajax/download-file-chat11 đổi hành vi, ảnh hưởng nút tải ở chat 1:1, header QR, cài đặt thêm bạn/bỏ chặn và QR landing. URL đầy đủ không phải Dropbox giờ lấy file theo path ở local hoặc media server thay vì gọi host trong URL, nên cần test trên staging với dữ liệu thật.
```

**Journal #147445 — Dev Studio — 2026-10-23:**

```
Dev handoff — 23/10 10:02 · nhánh ai_studio_fixbug_44046

Nguyên nhân:
`ChatController::ajaxDownloadFileChat11` chỉ kiểm `link_url` là chuỗi. Sau đó nó ghép thẳng vào `public_path()` (hoặc lấy phần path của URL rồi ghép vào `public_path()`) và đọc bằng `file_get_contents`, nên `/../.env` hay `http://x/../.env` trả về nội dung .env. Với URL đầy đủ, server tải đúng URL client gửi mà không giới hạn host, nên gọi được tới host nội bộ hoặc metadata (SSRF). Route nằm trong `/ajax` (chỉ yêu cầu đăng nhập, miễn CSRF), nên mọi tài khoản đăng nhập đều khai thác được.

Nội dung thay đổi:
- Chat 1:1 (tải ảnh, video, audio, file): server chỉ đọc file trong thư mục media. Path chứa .., \, NUL, php://, file://… bị từ chối 422 với câu 「ファイルのパスが正しくありません。」
- Cùng endpoint: URL đầy đủ có host lạ hoặc nội bộ không còn được server gọi tới; file lấy theo path ở local hoặc media server. Chỉ link Dropbox được tải thẳng (vẫn trả tên file)
- link_url dài quá 2048 ký tự ⇒ lỗi validate 422
- File không tồn tại hoặc media server lỗi: giữ như cũ, trả 502 「ダウンロードに失敗しました。」

File đã sửa (php-web):
  app/Http/Controllers/ChatController.php |  85 ++++----------------
  app/Services/MediaFileService.php       | 136 +++++++++++++++++++++++++++++++-
  2 files changed, 149 insertions(+), 72 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ một endpoint đọc file đổi hành vi, không ghi dữ liệu và không đổi FE. Rủi ro chính: file chỉ có trên domain web khác media server sẽ không tải được.
- Chat 1:1 (chat-v2.js downLoadFile): ảnh, video, audio có query, file JSON filePath, ảnh/video trong preview mẫu tin — cùng endpoint đổi logic
- Header nút ダウンロード QR (layout_v2_header.js): gửi URL tuyệt đối của ảnh QR, nay đi theo path qr_image
- Cài đặt thêm bạn / bỏ chặn (setting-add-friend-new.js): QR dạng URL_SERVER_MEDIA + FOLDER_MEDIA + qr_image
- Màn QR code v2 và tab hiển thị QR (qr_code/v2/index.js, mixins/qr_display_tab.js): ảnh landing FOLDER_MEDIA images
- /ajax/get-file-url (form answer, friend info): dùng chung MediaFileService; helper kiểm path được tách ra nhưng hành vi giữ nguyên

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Endpoint chỉ đọc, không ghi hay làm hỏng dữ liệu nào. Không xác định được lỗ hổng đã bị khai thác hay chưa, vì log không ghi link_url và body POST không có trong access log; việc rà soát và xoay vòng secret là quyết định vận hành, đã ghi ở follow_ups.

Việc cần người làm thêm (ngoài phạm vi task):
- Vận hành: lỗ hổng tồn tại từ 21/10/2024 và chỉ cần một tài khoản đăng nhập là khai thác được. Cần quyết định rà log và xoay vòng secret trong .env (APP_KEY, mật khẩu DB, key LINE/Stripe/Univapay).
- Ticket riêng: ImageRichmenuController::getCreateDownload (GET /rich-image/get-create-download) trả response()->download(public_path() . fileName), cùng lớp lỗi đọc file tuỳ ý.
- Ticket riêng: BasicController::checkFileExist (/ajax/check-file-exist, không cần đăng nhập) cho phép dò file tồn tại và gửi HEAD tới URL_SERVER_MEDIA + link_url.
- Xem xét: file CSV lịch sử truy cập admin lưu ở public/msg_template/access-histories-bot với tên theo timestamp, ai đoán được tên là tải qua HTTP được.
- Vận hành: rà log/xem endpoint đã bị khai thác chưa và cân nhắc xoay vòng secret trong .env (log cũ không ghi link_url).
- Tạo ticket riêng cho cùng lớp lỗi: ImageRichmenuController::getCreateDownload (download public_path().fileName) và BasicController::checkFileExist (/ajax/check-file-exist, không cần đăng nhập).
- Trên staging: kiểm tải file có URL đầy đủ trên domain web khác server media (nay lấy theo path ở local/URL_SERVER_MEDIA); nếu môi trường nào chỉ lưu file ở domain khác thì sẽ báo 502.
- Rà log / quyết định xoay vòng secret trong .env của production, vì lỗ hổng tồn tại từ 2024-10 và không xác định được đã bị khai thác hay chưa
- Mở ticket riêng cho cùng lớp lỗi ở ImageRichmenuController::getCreateDownload và BasicController::checkFileExist (đã nêu trong thiết kế)

Điểm cần test:
- Các payload sau trả 422 và không lộ nội dung file: /../.env, /msg_template/../../.env, %2e%2e, ..\, NUL, php://filter/..., file:///etc/passwd, http/../.env, http://x/../.env
- http://127.0.0.1/..., http://169.254.169.254/..., http://evil/?dropbox: server không gọi tới host đó
- Symlink trong msg_template trỏ ra ngoài thì trả 422
- Chat 1:1: tải được ảnh, video, audio (link có query), file PDF/xlsx, cả nội dung dạng URL đầy đủ lẫn path tương đối
- Tải QR được ở header, cài đặt thêm bạn/bỏ chặn và QR landing
- Video Dropbox trong preview mẫu tin ở chat tải được, đúng tên file
- File không tồn tại thì báo 「ダウンロードに失敗しました。」 (502)
- /ajax/get-file-url (form answer, friend info) vẫn tải như trước
- Chặn: POST /ajax/download-file-chat11 với link_url=/../.env, /msg_template/../../.env, /msg_template/%2e%2e/%2e%2e/.env, http://x/../.env, file:///etc/passwd, php://filter/... ⇒ 422 「ファイルのパスが正しくありません。」, không có nội dung .env
- link_url=http://169.254.169.254/latest/meta-data/ hoặc http://127.0.0.1/... ⇒ server không gọi host đó (502 hoặc lỗi theo path ở media server)
- Chat 1:1: tải ảnh, video, audio (link có ?query), file PDF/xlsx — cả tin có URL đầy đủ lẫn path tương đối
- Chat 1:1: tải ảnh/file có URL đầy đủ trên domain web khác domain đang chạy (vd tin cũ của sns./booking.) ⇒ vẫn tải được nếu file có ở local hoặc media server
- Preview mẫu tin trong chat: tải ảnh/video, video Dropbox (dl.dropboxusercontent.com) tải được và đúng tên file
- QR: nút ダウンロード ở header, cài đặt thêm bạn / bỏ chặn, màn QR code v2 và tab hiển thị QR ⇒ tải được PNG
- File không tồn tại ⇒ 502 và alert 「ダウンロードに失敗しました。」
- /ajax/get-file-url (file đính kèm form answer, friend info) vẫn tải như trước

Branch: ai_studio_fixbug_44046
- sns-line: ai_studio_fixbug_44046 (nhánh gốc release_step_20260930_v2 @3351f2aaa78d, commit ef35b6f6878846c9d353c4e59c617bb6e715b8cd)
```
