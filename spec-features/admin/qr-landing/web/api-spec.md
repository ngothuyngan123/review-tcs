# FA-017 — QR Code Action 「QRコードアクション」 — API Spec

> **Nguồn phân tích**: Laravel 5 / PHP 7.2 — `src/web/sns-line/`
> **Controller chính**: `App\Http\Controllers\Basic\QRCodeController` — `sns-line/app/Http/Controllers/Basic/QRCodeController.php` (3.966 dòng)
> **Bảng chính**: `landing`
> **Trạng thái**: ui-spec.md CHƯA có tại thời điểm phân tích → phần "Liên kết endpoint ↔ màn hình UI" dùng **tên view blade** làm cầu nối, **chờ đối chiếu ui-spec**.
> **Lưu ý**: Trong hệ thống tồn tại song song 2 thế hệ màn hình — **v1** (`basic.qr_code.create` / `basic.qr_code.index`) và **v2** (`basic.qr_code.v2.*`). UI đang chạy là **v2**; các endpoint v1 vẫn sống trong routes (xem cột "Ghi chú" và mục 5).

---

## 1. Bảng tổng hợp endpoints

### 1.1. Nhóm Admin / Staff (có xác thực)

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Xác thực |
|----|--------|-----|-------|-------------------|------------|----------|
| EP-01 | GET | `/basic/landing` | Màn hình danh sách QR Code Action | `QRCodeController@index` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session Laravel + CSRF |
| EP-02 | GET | `/ajax/v2/landing` | Lấy danh sách QR (phân trang, lọc, sắp xếp) | `QRCodeController@ajaxGetListQrs` | `check_login`, `check_remember_token` | Session (CSRF miễn — `/ajax/*`) |
| EP-03 | DELETE | `/ajax/v2/landing` | Xoá mềm nhiều QR | `QRCodeController@ajaxDeleteQrs` | `check_login`, `check_remember_token` | Session |
| EP-04 | POST | `/ajax/v2/landing/move-category` | Di chuyển nhiều QR sang thư mục khác | `QRCodeController@ajaxMoveCategory` | `check_login`, `check_remember_token` | Session |
| EP-05 | POST | `/ajax/v2/landing/sort-qrs` | (Rỗng — method không có thân hàm) | `QRCodeController@ajaxSortQrs` | `check_login`, `check_remember_token` | Session |
| EP-06 | PUT | `/ajax/v2/landing/update-basic/{qr}` | Cập nhật thông tin cơ bản QR (tên, thư mục, bật/tắt, action id) | `QRCodeController@ajaxUpdateBasicQrs` | `check_login`, `check_remember_token` | Session |
| EP-07 | GET | `/ajax/v2/landing/qr-removed` | Danh sách QR đã xoá (thùng rác) | `QRCodeController@ajaxGetQrsRemoved` | `check_login`, `check_remember_token` | Session |
| EP-08 | POST | `/ajax/v2/landing/restore/{id}` | Khôi phục QR đã xoá | `QRCodeController@restoreQr` | `check_login`, `check_remember_token` | Session |
| EP-09 | POST | `/ajax/v2/landing/{qr}/setting-detail` | Lưu cài đặt「アクション設定」(tab chi tiết) | `QRCodeController@settingDetail` | `check_login`, `check_remember_token` | Session |
| EP-10 | POST | `/ajax/v2/landing/{qr}/setting-introduce` | Lưu cài đặt trang/tin nhắn giới thiệu bạn bè | `QRCodeController@settingIntroduce` | `check_login`, `check_remember_token` | Session |
| EP-11 | POST | `/ajax/v2/landing/{qr}/setting-limit` | Lưu cài đặt giới hạn thời gian hiệu lực | `QRCodeController@settingLimit` | `check_login`, `check_remember_token` | Session |
| EP-12 | POST | `/ajax/v2/landing/update-connect-asp/{qr}` | Đặt QR này là QR liên kết ASP (affiliate) | `QRCodeController@updateConnectAsp` | `check_login`, `check_remember_token` | Session |
| EP-13 | POST | `/ajax/v2/landing/get-preview-action/{id}` | Lấy dữ liệu preview tin nhắn khi quét QR | `QRCodeController@ajaxGetPreviewAction` | `check_login`, `check_remember_token` | Session |
| EP-14 | POST | `/ajax/v2/landing/get-preview-intro-action/{id}` | Lấy dữ liệu preview action giới thiệu | `QRCodeController@ajaxGetPreviewActionIntro` | `check_login`, `check_remember_token` | Session |
| EP-15 | POST | `/ajax/v2/landing/quick-send-qr` | Gửi thử link QR cho tài khoản test | `QRCodeController@quickSendQr` | `check_login`, `check_remember_token` | Session |
| EP-16 | POST | `/ajax/v2/landing/get-init-detail-landing` | Dữ liệu thống kê chi tiết QR (tab1/tab2/tab3) + xuất CSV | `QRCodeController@ajaxInitDataDetailV2` | `check_login`, `check_remember_token` | Session |
| EP-17 | GET | `/ajax/v2/landing/category` | Danh sách thư mục QR | `QRCodeController@ajaxGetCategories` | `check_login`, `check_remember_token` | Session |
| EP-18 | POST | `/ajax/v2/landing/category/create` | Tạo (hoặc đổi tên) thư mục QR | `QRCodeController@ajaxCreateCategory` | `check_login`, `check_remember_token` | Session |
| EP-19 | PUT | `/ajax/v2/landing/category/update/{category}` | Đổi tên thư mục QR | `QRCodeController@ajaxUpdateCategory` | `check_login`, `check_remember_token` | Session |
| EP-20 | DELETE | `/ajax/v2/landing/category/{id}` | Xoá thư mục QR (kèm QR bên trong) | `QRCodeController@ajaxDeleteCategory` | `check_login`, `check_remember_token` | Session |
| EP-21 | POST | `/ajax/v2/landing/category/sort-category` | Sắp xếp thứ tự thư mục | `QRCodeController@ajaxSortCategory` | `check_login`, `check_remember_token` | Session |
| EP-22 | POST | `/ajax/v2/landing/getSettingAction` | Lấy chi tiết 3 action gắn với QR (chính / giới thiệu / hết hạn) | `QRCodeController@getSettingAction` | `check_login`, `check_remember_token` | Session |
| EP-23 | POST | `/ajax/v2/landing/edit/{id}/setting-option` | Lưu tuỳ chọn thiết kế QR (logo, màu, kiểu) — multipart | `QRCodeController@saveSettingOption` | `check_login`, `check_remember_token` | Session |
| EP-24 | GET | `/ajax/v2/landing/data` | Lấy dữ liệu 1 landing theo `id` hoặc `uLand` | `QRCodeController@getLandingData` | `check_login`, `check_remember_token` | Session |
| EP-25 | POST | `/ajax/v2/landing/edit/{id}/qr-off` | Lưu cài đặt「QRコードOFF」+ lịch bật/tắt theo thời gian | `QRCodeController@saveSettingQrOff` | `check_login`, `check_remember_token` | Session |
| EP-26 | POST | `/ajax/v2/landing/edit/{id}/external-setting` | Lưu cài đặt liên kết trang ngoài (HTML tag, callback, URL) | `QRCodeController@saveExternalSetting` | `check_login`, `check_remember_token` | Session |
| EP-27 | POST | `/ajax/v2/landing/edit/{id}/parameters` | Lưu mapping tham số `cid1..cid5` → trường thông tin bạn bè | `QRCodeController@saveExternalParameters` | `check_login`, `check_remember_token` | Session |
| EP-28 | GET | `/ajax/v2/landing/edit/{id}/parameters` | Lấy mapping tham số `cid1..cid5` | `QRCodeController@getExternalParameters` | `check_login`, `check_remember_token` | Session |
| EP-29 | GET | `/ajax/v2/landing/{id}/poster-connect-qr-code` | Lấy danh sách「広告名」(bước 1 LP Poster) | `QRCodeController@getPosterConnectQrCode` | `check_login`, `check_remember_token` | Session |
| EP-30 | POST | `/ajax/v2/landing/{id}/poster-connect-qr-code` | Lưu danh sách「広告名」(bước 1 LP Poster) | `QRCodeController@storePosterConnectQrCode` | `check_login`, `check_remember_token` | Session |
| EP-31 | GET | `/ajax/v2/landing/{id}/landing-url-qr-code` | Lấy danh sách LP + URL (bước 2 LP Poster) | `QRCodeController@getLandingPosterConnectQrCode` | `check_login`, `check_remember_token` | Session |
| EP-32 | POST | `/ajax/v2/landing/{id}/landing-url-qr-code` | Lưu danh sách LP + URL (bước 2 LP Poster) | `QRCodeController@storeLandingPosterConnectQrCode` | `check_login`, `check_remember_token` | Session |
| EP-33 | GET | `/ajax/v2/landing/{id}/landing-page-connect-qr-code` | Sinh ma trận URL đo lường (bước 4 LP Poster) | `QRCodeController@getLandingQrStep4Data` | `check_login`, `check_remember_token` | Session |
| EP-34 | GET | `/ajax/v2/landing/{id}/hash-id` | Lấy `liff_app_id`, domain, `uLand` để dựng URL QR (bước 3) | `QRCodeController@getHashId` | `check_login`, `check_remember_token` | Session |
| EP-35 | GET | `/ajax/v2/landing/{id}/landing-url-filter` | Danh sách LP-poster-url dùng làm bộ lọc màn thống kê | `QRCodeController@getLandingUrlFilter` | `check_login`, `check_remember_token` | Session |
| EP-36 | POST | `/ajax/v2/landing/setting_intro/steps_modal` | Ẩn vĩnh viễn modal hướng dẫn (per-user) | `QRCodeController@hideSettingIntroStepsModal` | `check_login`, `check_remember_token` | Session |
| EP-37 | GET | `/ajax/v2/landing/{id}/collect-statistic` | Số liệu tổng hợp lượt quét / kết bạn / action | `QRCodeController@collectStatistic` | `check_login`, `check_remember_token` | Session |
| EP-38 | GET | `/ajax/v2/landing/{id}/collect-friend` | Danh sách bạn bè theo loại (mới / unblock / đã là bạn / ẩn) | `QRCodeController@collectFriend` | `check_login`, `check_remember_token` | Session |
| EP-39 | GET | `/ajax/v2/landing/{id}/detail-click-day` | Chi tiết lượt quét theo 1 ngày cụ thể | `QRCodeController@detailClickDay` | `check_login`, `check_remember_token` | Session |
| EP-40 | POST | `/ajax/get-list-group-landing` | (v1) Danh sách thư mục + QR, kiêm CRUD thư mục theo `action` | `QRCodeController@ajaxGetListLanding` | `check_login`, `check_remember_token` | Session |
| EP-41 | POST | `/ajax/get-init-detail-landing` | (v1) Thống kê chi tiết QR bản cũ | `QRCodeController@ajaxInitDataDetail` | `check_login`, `check_remember_token` | Session |
| EP-42 | POST | `/ajax/get-sort-landing` | Lưu thứ tự sắp xếp QR | `QRCodeController@sortQRCode` | `check_login`, `check_remember_token` | Session |
| EP-43 | POST | `/ajax/init-data-sort-landing` | ⚠ Route trỏ tới `QRCodeController@initDataSort` — **method KHÔNG tồn tại** trong controller | `QRCodeController@initDataSort` | `check_login`, `check_remember_token` | Session |
| EP-44 | POST | `/ajax/landing/init-data-action` | Lấy chi tiết action + action giới thiệu để render modal | `QRCodeController@ajaxInitSettingAction` | `check_login`, `check_remember_token` | Session |
| EP-45 | POST | `/ajax/landing/save-preview-intro` | Lưu nhanh tiêu đề/nội dung trang giới thiệu từ màn preview | `QRCodeController@savePreviewIntro` | `check_login`, `check_remember_token` | Session |
| EP-46 | GET | `/basic/landing/v2/edit/{id}` | Màn hình chỉnh sửa QR (v2) | `QRCodeController@editLandingV2` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-47 | GET | `/basic/landing/v2/edit/{id}/poster` | Màn hình LP Poster (4 bước) | `QRCodeController@editLandingPoster` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-48 | GET | `/basic/landing/v2/preview-message-scan-qr/{id}` | Màn preview tin nhắn khi quét QR | `QRCodeController@previewMessageScanQr` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-49 | GET | `/basic/landing/show/{id}` | Màn hình thống kê chi tiết 1 QR | `QRCodeController@showFriendClick` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-50 | POST | `/basic/create-landing-v2` | Tạo QR mới hoặc sao chép QR (v2) | `QRCodeController@saveLandingV2` | `LogRequestMultipart`, `https_protocol`, `is_expire`, `check_remember_token` | Session **+ CSRF bắt buộc** |
| EP-51 | GET | `/basic/landing-qr/link-google` | Màn hình liên kết Google Spreadsheet | `QRCodeController@linkGoogle` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-52 | GET | `/basic/landing-qr/redirect-google-sheet` | Callback OAuth Google (redirect URI) | `QRCodeController@redirectUriGoogleSheet` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-53 | GET | `/basic/landing-qr/cancel-google-sheet/{id}` | Huỷ liên kết Google Spreadsheet | `QRCodeController@cancelGoogleSheet` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-54 | GET | `/basic/landing-qr/removed` | Màn hình thùng rác QR | `QRCodeController@qrsRemoved` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-55 | GET | `/basic/create-landing` | (v1 — legacy) Màn tạo QR bản cũ | `QRCodeController@store` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-56 | GET | `/basic/landing/edit/{id}` | (v1 — legacy) Màn sửa QR bản cũ | `QRCodeController@editLanding` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-57 | GET | `/basic/landing/copy/{id}` | (v1 — legacy) Màn sao chép QR bản cũ | `QRCodeController@copyLanding` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session |
| EP-58 | POST | `/basic/create-landing` | (v1 — legacy) Lưu QR mới bản cũ | `QRCodeController@saveLanding` | `LogRequestMultipart`, `https_protocol`, `is_expire`, `check_remember_token` | Session **+ CSRF** |
| EP-59 | POST | `/basic/landing/edit/{id}` | (v1 — legacy) Lưu chỉnh sửa QR bản cũ | `QRCodeController@saveEditLanding` | `LogRequestMultipart`, `https_protocol`, `is_expire`, `check_remember_token` | Session **+ CSRF** |
| EP-60 | POST | `/basic/landing/delete` | (v1 — legacy) Xoá nhiều QR | `QRCodeController@delete` | `LogRequestMultipart`, `https_protocol`, `is_expire`, `check_remember_token` | Session **+ CSRF** |
| EP-61 | GET | `/basic/landings/grouped-by-folder` | Danh sách thư mục + QR dùng chung (picker cho tính năng khác) | `Basic\LandingController@ajaxGroupedByFolder` | `check_login`, `check_remember_token` | Session |
| EP-62 | GET | `/basic/landing/set-cookie` | Ghi nhớ thư mục đang mở vào cookie | `Basic\BasicController@folderSetCookie` | — | Session |

### 1.2. Nhóm Public / LINE User (không middleware xác thực)

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Xác thực |
|----|--------|-----|-------|-------------------|------------|----------|
| EP-63 | GET | `/landing-qr/{liffId}` | Trang LIFF hiển thị QR / redirect vào LINE (đích của link QR) | `QRCodeController@qrLanding` | `NotifyChatworkRequestTimeSlow` | **Không** |
| EP-64 | POST | `/ajax/v2/landing/{id}/count-scan-qr-code` | Ghi nhận 1 lượt mở/quét QR | `QRCodeController@countScan` | `NotifyChatworkRequestTimeSlow` | **Không** (CSRF miễn — `/ajax/*`) |
| EP-65 | GET | `/landing/page-intro/{id}/{u_code}` | Trang giới thiệu bạn bè cho LINE User | `QRCodeController@pageIntro` | `NotifyChatworkRequestTimeSlow` | **Không** (định danh bằng `u_code`) |
| EP-66 | GET | `/landing/preview-page-intro/{type}/{id}` | Preview trang giới thiệu (dùng trong iframe màn admin) | `QRCodeController@previewPageIntro` | `NotifyChatworkRequestTimeSlow` | **Không** |
| EP-67 | GET | `/open-mobile/{type}/{id}` | Trang trung gian mở LIFF trên mobile | `QRCodeController@openMobile` | `NotifyChatworkRequestTimeSlow` | **Không** |
| EP-68 | GET | `/open-external-browser/{type}/{id}` | Trang trung gian mở trình duyệt ngoài | `QRCodeController@openExternalBrowser` | `NotifyChatworkRequestTimeSlow` | **Không** |
| EP-69 | POST | `/ajax/open-mobile/check-friend` | Kiểm tra/khởi tạo quan hệ bạn bè, trả URL đích | `QRCodeController@checkFriend` | `NotifyChatworkRequestTimeSlow` | **Không** (CSRF miễn) |

> **Cảnh báo bảo mật (Mức độ tin cậy: Cao)** — EP-64, EP-65, EP-69 hoàn toàn public, không CSRF, không rate-limit trong code, và nhận `bot_id` / `line_id` trực tiếp từ body. EP-69 có khả năng **tạo mới** `line_user`, `bot_line_user`, `conversation` và gửi tin nhắn. Xem chi tiết ở logic-spec.

---

## 2. Chi tiết từng endpoint

### EP-01 — GET `/basic/landing`
- **Mục đích**: Render màn hình danh sách QR Code Action 「QRコードアクション」.
- **Request params**: không có (đọc `bot_id` từ session qua `getBotId()`; đọc cookie `folder_landing`).
- **Response thành công**: render view `basic.qr_code.v2.index` với `getInfoBot`, `flagNewFreePlan`, `folderCookie`, `qrCodeNumber`, `scenario`, `conversion`, `richMenus`, `liff_id`.
- **Lỗi**:

  | HTTP | Mô tả |
  |---|---|
  | 302 → `adminIndex` | Bot không tồn tại hoặc `is_deleted = 1` |
  | 302 → `pointSettings` / `maintain` | Do middleware `is_expire` |
- **Nguồn**: `sns-line/app/Http/Controllers/Basic/QRCodeController.php:111-150`; route `sns-line/routes/web.php:977`

---

### EP-02 — GET `/ajax/v2/landing`
- **Mục đích**: Lấy danh sách QR của bot hiện tại, hỗ trợ lọc theo thư mục / từ khoá / đối tượng action, sắp xếp và phân trang.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Validation |
  |---|---|---|---|---|
  | `category_id` | query | int | Không | `0` ⇒ khớp `category_id IN (0, NULL)` |
  | `keyword` | query | string | Không | Tìm `name LIKE %keyword%`; khi có `keyword` thì bỏ qua lọc `category_id` |
  | `type` | query | string | Không | `sort_item` ⇒ chỉ trả `id`, `name` |
  | `action_with_friend` | query | int | Không | `0` ⇒ lấy cả `1` (NEW_FRIEND) và `2` (ALL_FRIEND) |
  | `limit` | query | int | Không | Mặc định `15` |
  | `unlimit` | query | bool | Không | `1` ⇒ trả toàn bộ, không phân trang |
  | `orders` | query | array | Không | `[{column, dir}]`; whitelist `column`: `category_id, created_at, position, name, updated_at, action_id, action_with_friend, status` |
  | `page` | query | int | Không | Chuẩn Laravel paginator |
- **Request mẫu**:
  ```
  GET /ajax/v2/landing?category_id=0&keyword=&limit=15&page=1&orders[0][column]=position&orders[0][dir]=ASC
  ```
- **Response thành công**:
  ```json
  {
    "status": true,
    "data": { "current_page": 1, "data": [ { "id": 1, "name": "...", "code": "ab12cd",
      "new_link_qr_code": "https://.../landing-qr/{liff_app_id}?uLand=ab12cd",
      "path_landing": "https://media.../landing/xxx.png",
      "action": { "details": [] } } ], "total": 20, "last_page": 2, "per_page": 15 },
    "landingConnectAsp": { "id": 0, "name": "設定しない" },
    "qrCodeNumber": 20,
    "contractType": "free"
  }
  ```
- **Lỗi**: không bắt exception riêng — lỗi PHP ⇒ 500 JSON của Laravel.
- **Nguồn**: `QRCodeController.php:891-973`; route `routes/web.php:2833`; client `sns-line/public/js/qr_code/v2/index.js:287`

---

### EP-03 — DELETE `/ajax/v2/landing`
- **Mục đích**: Xoá mềm (soft delete) nhiều QR cùng lúc.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Validation |
  |---|---|---|---|---|
  | `ids` | body | array\<int\> | Có (thực tế) | Không validate; chỉ chạy khi `!empty($ids) && is_array($ids)` |
- **Request mẫu**: `{ "ids": [12, 13, 14] }`
- **Response thành công**: `{ "message": "success" }` (HTTP 200) — **luôn trả success kể cả khi `ids` rỗng/sai kiểu**.
- **Side effect**: set `deleted_at = now()`, `operator_id = Auth::id()` trên `landing`; **xoá mềm** các bản ghi `detail_landing_click` tương ứng.
- **Nguồn**: `QRCodeController.php:975-998`; route `routes/web.php:2834`

---

### EP-04 — POST `/ajax/v2/landing/move-category`
- **Request params**: `ids` (array\<int\>, bắt buộc), `folder_move_id` (int|null, bắt buộc có key).
- **Response**: `{ "message": "success" }`
- **⚠ Lưu ý bảo mật (Cao)**: câu update **không lọc `bot_id`** — `Landing::whereIn('id', $ids)->update(['category_id' => $cat])` (`QRCodeController.php:1000-1011`). Có thể sửa QR của bot khác nếu biết id.
- **Nguồn**: `QRCodeController.php:1000-1011`; route `routes/web.php:2835`; client `index.js:398`

---

### EP-06 — PUT `/ajax/v2/landing/update-basic/{qr}`
- **Mục đích**: Cập nhật nhanh các trường cơ bản của QR; dùng cho toggle bật/tắt ở danh sách và lưu tên/thư mục ở màn edit.
- **Request params** (whitelist bằng `$request->only`):

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `qr` | path | int | Có | Route model binding → `Landing` |
  | `status` | body | int (0/1) | Không | `0` = 非公開, `1` = 公開 |
  | `name` | body | string | Không | Client kiểm ≤ 50 ký tự; **server không validate** |
  | `category_id` | body | int | Không | |
  | `action_id` | body | int | Không | |
  | `user_introduction_action_id` | body | int | Không | |
  | `action_limit_id` | body | int | Không | |
- **Response thành công**: `{ "message": "success" }`
- **Lỗi**:

  | HTTP | Mô tả |
  |---|---|
  | 404 | `Qr not found!` — `$qr->bot_id != getBotId()` |
  | 404 | Route model binding không tìm thấy id |
- **Logic phụ**: khi payload **chỉ** có `status`, hệ thống tính lại `time_qr_off_status` theo `use_limit_time`, `limit_start_time`, `limit_end_time` (xem logic-spec BR-08).
- **Nguồn**: `QRCodeController.php:1013-1052`; route `routes/web.php:2837`; client `index.js:729`, `edit.js:113`, `mixins/header_landing.js:42`

---

### EP-07 — GET `/ajax/v2/landing/qr-removed`
- **Request params**: `order` (string — tên cột), `dir` (`asc`/`desc`), `limit` (int, mặc định 15).
- **⚠**: `order` **không có whitelist** → truyền thẳng vào `orderBy()` (`QRCodeController.php:1322-1324`). Rủi ro SQL injection ở tên cột (Mức độ tin cậy: Trung bình — Laravel có wrap identifier nhưng không kiểm tồn tại cột).
- **Response**: `{ "message": "success", "data": {paginator} }` — mỗi item kèm quan hệ `operator:id,username`.
- **Nguồn**: `QRCodeController.php:1314-1332`; route `routes/web.php:2838`; client `public/js/qr_code/v2/qrs_removed.js:32`

---

### EP-08 — POST `/ajax/v2/landing/restore/{id}`
- **Mục đích**: Khôi phục QR từ thùng rác.
- **Request params**: `id` (path, int, bắt buộc).
- **Response thành công**: `{ "message": "success" }`
- **Lỗi**:

  | HTTP | Body | Mô tả |
  |---|---|---|
  | 500 | `{"status": false, "message": "現在のプランは利用できない機能です。アップグレードが必要になります。"}` | Gói free đã đủ 3 QR |
  | 404 | `Qr not found!` | Không có QR (kể cả trashed) thuộc bot |
  | 500 | `{"status": false, "message": PlanLimitGuard::PLAN_MESSAGE}` | Kiểm lại sau restore vẫn vượt hạn mức ⇒ **xoá lại QR vừa khôi phục** |
- **Side effect**: khôi phục `landing`, khôi phục `detail_landing_click`, và **bỏ cờ `is_deleted` của thư mục cha** nếu thư mục đang bị xoá.
- **Nguồn**: `QRCodeController.php:1334-1384`; route `routes/web.php:2839`

---

### EP-09 — POST `/ajax/v2/landing/{qr}/setting-detail`
- **Mục đích**: Lưu cài đặt hành động chính khi user quét QR.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `qr` | path | int | Có | Route model binding |
  | `action_id` | body | int | Không | ID action gắn vào QR |
  | `action_type` | body | int (1/2) | Không | 1 = chạy 1 lần, 2 = chạy nhiều lần |
  | `use_msg_new_friend` | body | int (0/1) | Không | Gửi tin nhắn cho bạn mới |
  | `use_msg_old_friend` | body | int (0/1) | Không | Gửi tin nhắn cho bạn cũ |
  | `use_msg_unblock` | body | int (0/1) | Không | Gửi tin nhắn khi unblock |
  | `interval_action` | body | int (0/1/2) | Không | 0 = không giới hạn, 2 = có khoảng cách thời gian |
  | `time_interval_action` | body | float | Không | Chỉ dùng khi `interval_action == 2` |
  | `general_message` | body | string | Không | Nội dung tin nhắn chung — **không nằm trong `$request->only`**, xử lý riêng qua bảng `template` |
- **Response**: `{ "message": "success" }`
- **Side effect trên `template`**: `general_message == ''` ⇒ xoá template và set `template_general_id = null`; có nội dung + đã có template ⇒ update `content` + `update_timestamp`; chưa có template ⇒ tạo mới với `category_id = -111222`, `type = 'text'`, `position = 0`.
- **⚠**: **không kiểm `$qr->bot_id == getBotId()`** (Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:1405-1441`; route `routes/web.php:2840`; client `mixins/setting_detail.js:60`

---

### EP-10 — POST `/ajax/v2/landing/{qr}/setting-introduce`
- **Request params**: `intro_page_title`, `intro_page_content` (HTML từ TinyMCE), `user_introduction_action_id` (int), `use_user_intro_action_message` (0/1), `intro_message` (string ≤ 500), và `user_intro_action_message` (string — xử lý riêng qua bảng `template`, gắn vào `template_intro_id`).
- **Response**: `{ "message": "success" }`
- **⚠**: không kiểm `bot_id`; không validate độ dài server-side (client dùng vee-validate).
- **Nguồn**: `QRCodeController.php:1443-1488`; route `routes/web.php:2841`; client `mixins/setting_introduce.js:85`

---

### EP-11 — POST `/ajax/v2/landing/{qr}/setting-limit`
- **Request params** (`$request->only`): `use_limit_time` (0/1), `limit_start_time` (`Y-MM-DD HH:mm`), `limit_end_time`, `use_qr_page_over_time` (0/1), `use_action_limit` (0/1), `action_limit_id` (int), `use_limit_end_time` (0/1).
- **Response**: `{ "message": "success" }`
- **⚠**: không kiểm `bot_id`; không validate `limit_end_time > limit_start_time` ở server (chỉ có ở client `mixins/setting_limit.js:83-91`); **không cập nhật `time_qr_off_status`** (khác với EP-25).
- **Nguồn**: `QRCodeController.php:1490-1507`; route `routes/web.php:2842`; client `mixins/setting_limit.js:67`

---

### EP-12 — POST `/ajax/v2/landing/update-connect-asp/{qr}`
- **Mục đích**: Chỉ định QR duy nhất được dùng cho luồng affiliate (ASP).
- **Request params**: `qr` (path, route model binding). Không có body.
- **Logic**: trong transaction — reset `connect_aff = 0` cho **toàn bộ** QR của bot, rồi set `connect_aff = 1` cho QR đích.
- **Response**: `{ "message": "success" }`; lỗi ⇒ HTTP 500 (`HttpException`).
- **Nguồn**: `QRCodeController.php:1386-1403`; route `routes/web.php:2843`; client `index.js:716`

---

### EP-13 — POST `/ajax/v2/landing/get-preview-action/{id}`
- **Mục đích**: Trả nội dung preview tin nhắn/action sẽ gửi khi user quét QR, dựa trên `add_friend_setting` của bot.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `id` | path | int | Có | Landing id |
  | `mode` | body | int | Không | 1 = bạn mới, 2 = bạn cũ, 3 = unblock, 4 = bỏ qua add-friend-setting |
  | `preview_tab` | body | int | Không | `2` ⇒ trả chi tiết action; khác ⇒ trả template text |
- **Response**: `{ "message": "success", "data": [ ...Template|ActionDetail... ] }`
- **Lỗi**: 404 `Qr not found!` khi landing không tồn tại. **Không kiểm `bot_id`**.
- **Nguồn**: `QRCodeController.php:1517-1555`; route `routes/web.php:2844`

---

### EP-14 — POST `/ajax/v2/landing/get-preview-intro-action/{id}`
- **Request params**: `id` (path, int).
- **Response**: `{ "message": "success", "data": [ ...Template... ] }` — nội dung `user_introduction_action_id` được diễn giải thành danh sách message (text + template, có xử lý template kiểu `group`).
- **Lỗi**: 404 `Qr not found!`.
- **Nguồn**: `QRCodeController.php:1557-1565` (+ `handlePreviewMessageFromAction` `:1575-1641`); route `routes/web.php:2845`

---

### EP-15 — POST `/ajax/v2/landing/quick-send-qr`
- **Mục đích**: Gửi link QR qua LINE tới các tài khoản test đã cấu hình.
- **Request params**: `landing_id` (int, bắt buộc), `lineIds` (array\<string\>, bắt buộc).
- **Response thành công**: `{ "success": true, "msg": <config sns-line.alert_success_send_for_tester> }`
- **Lỗi**:

  | Trường hợp | Body |
  |---|---|
  | Chưa cấu hình tài khoản test | `{"success": false, "msg": "テストアカウントが設定されていません"}` |
  | Gửi thất bại | Kết quả của `returnResponseSendMessageV2(...)` với `config('sns-line.send_fail_msg_screen_chat')` |
- **Side effect**: tạo `messages_v2`, tăng `bots.free_send_count`, cập nhật số tin gửi trong ngày (`updateMessageSendCount`).
- **Nguồn**: `QRCodeController.php:1160-1226`; route `routes/web.php:2846`; client `index.js:828`

---

### EP-16 — POST `/ajax/v2/landing/get-init-detail-landing`
- **Mục đích**: Endpoint chính của màn thống kê chi tiết 1 QR. Phục vụ 3 tab và cả xuất CSV.
- **Request params** (gửi dạng `FormData`):

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `id` | body | int | Có | Landing id |
  | `start_date` | body | date | Không | Mặc định = đầu tháng hiện tại |
  | `end_date` | body | date | Không | Mặc định = hôm nay; nếu `< start_date` ⇒ ép `= start_date` |
  | `tab` | body | string | Không | `tab1` (theo ngày — mặc định), `tab2` (theo bạn bè), `tab3` (theo LP/poster URL) |
  | `keyword` | body | string | Không | tab2: tìm `line_user.name`/`view_name`; tab3: tìm `landing_name`/`poster_name` |
  | `type` | body | string | Không | `download-csv` ⇒ trả file CSV Shift_JIS |
  | `page` / `per_page` | body | int | Không | Phân trang |
  | `order` / `dir` | body | string | Không | tab1 whitelist `date`; tab2 whitelist `time_click, is_old_friend, action`; tab3 whitelist `collect_open_landings.date_scan` |
  | `get_all` | body | 0/1 | Không | `1` ⇒ bỏ lọc khoảng ngày (tab2) |
  | `type_count` | body | int | Không | `1` = đếm distinct theo `line_id`/`device`; `2` = đếm tất cả dòng |
  | `landing_url_ids` | body | string | Không | CSV id của `landing_page_poster_url` để lọc |
  | `is_detail_day` | body | 0/1 | Không | tab2: `1` ⇒ không loại các dòng `is_old_friend = 0 AND action = 1` |
- **Response thành công (JSON)**:
  ```json
  {
    "success": true, "name": "QR名", "details": [...],
    "total_friend": 0, "total_action": 0, "total_block": 0,
    "total_friend_new": 0, "total_friend_click": 0, "total_friend_new_click": 0,
    "total_new_friend_tab2": 0, "total_old_friend": 0, "total_unblock": 0,
    "pagination": {"total":0,"from":0,"to":0,"last_page":1,"per_page":10,"current_page":1},
    "firstAdd": []
  }
  ```
- **Response CSV** (`type = download-csv`): HTTP 200, `Content-Type: text/csv; charset=Shift_JIS`, `Content-Disposition: attachment; filename="export.csv"`. Exporter theo tab: `DetailLandingClickExport` (tab1) / `LandingListFriendExport` (tab2) / `LandingPageUrlExport` (tab3).
- **Lỗi**: nếu `id` không tồn tại ⇒ `$landing` null ⇒ lỗi PHP truy cập `->name` (HTTP 500). **Không kiểm `bot_id` của landing** (chỉ lọc `bot_id` ở các bảng thống kê).
- **Nguồn**: `QRCodeController.php:1849-2288`; route `routes/web.php:2847`; client `public/js/qr_code/v2/detail.js:145,347`, `index.js:765`

---

### EP-17 — GET `/ajax/v2/landing/category`
- **Request params**: `keyword` (string), `action_with_friend` (int).
- **Response**: `{ "message": "success", "data": { "categories": [...], "count_default": 5 } }` — `count_default` = số QR không thuộc thư mục nào (`category_id` null hoặc 0).
- **Nguồn**: `QRCodeController.php:1059-1083`; route `routes/web.php:2849`

---

### EP-18 — POST `/ajax/v2/landing/category/create`
- **Request params**: `id` (int|null — nếu có và thư mục còn sống ⇒ **đổi tên**), `name` (string, bắt buộc thực tế).
- **Response**: `{ "message": "success", "item": {Category} }`
- **Logic**: khi tạo mới ⇒ `kind = 10` (kind landing), `position = max(position) + 1` trong phạm vi bot.
- **⚠**: khi đổi tên theo `id`, **không lọc `bot_id`** (`QRCodeController.php:1088-1091`).
- **Nguồn**: `QRCodeController.php:1085-1108`; route `routes/web.php:2850`

---

### EP-19 — PUT `/ajax/v2/landing/category/update/{category}`
- **Request params**: `category` (path, int), `name` (body, string).
- **Response**: `{ "message": "success" }`
- **Lỗi**: nếu category không thuộc bot ⇒ `$category` null ⇒ lỗi PHP tại `$category->id` (HTTP 500).
- **Nguồn**: `QRCodeController.php:1110-1125`; route `routes/web.php:2851`

---

### EP-20 — DELETE `/ajax/v2/landing/category/{id}`
- **Request params**: `id` (path, int).
- **Side effect (phá huỷ dữ liệu)**: set `category.is_deleted = 1`; **xoá mềm toàn bộ `landing` trong thư mục**; xoá mềm `detail_landing_click` của các landing đó.
- **Response**: `{ "message": "success" }`
- **⚠ Bug tiềm ẩn (Cao)**: biến `$landingIds` chỉ được gán trong nhánh `if ($group_id > 0)` nhưng lại được dùng ở `Log::info` bên ngoài ⇒ khi `group_id <= 0` sẽ ném `Undefined variable` (`QRCodeController.php:1127-1147`).
- **Nguồn**: `QRCodeController.php:1127-1147`; route `routes/web.php:2852`

---

### EP-21 — POST `/ajax/v2/landing/category/sort-category`
- **Request params**: `sort_ids` (string — danh sách id ngăn cách bởi dấu phẩy, đã **đảo ngược** phía client).
- **Logic**: gán `position = index + 1` theo thứ tự trong chuỗi. **Không lọc `bot_id`**.
- **Response**: `{ "message": "success" }`
- **Nguồn**: `QRCodeController.php:1149-1158`; route `routes/web.php:2853`; client `index.js:517`

---

### EP-22 — POST `/ajax/v2/landing/getSettingAction`
- **Request params**: `landingId` (body, int, bắt buộc).
- **Response**:
  ```json
  { "success": true, "data": { "...landing fields...",
      "detail_actions": [...], "detail_intro_actions": [...], "detail_limit_actions": [...] } }
  ```
  Mỗi `ActionDetail` được bổ sung `data` (đã decode qua `Actions::initDataAction`), `has_filters` (tính lại từ `FilterV2::initDataFilter`), `list_tags` (khi `type == 'tag'`), `is_edit_content = false`.
- **Lỗi**: 404 `Qrcode not found` — **có** kiểm `bot_id` ở đây.
- **Nguồn**: `QRCodeController.php:3462-3475` (+ `getActionDetailByActionId` `:3476-3502`); route `routes/web.php:2855`; client `mixins/setting_basic.js:184`

---

### EP-23 — POST `/ajax/v2/landing/edit/{id}/setting-option`
- **Mục đích**: Lưu tuỳ chọn thiết kế mã QR (logo giữa QR, kiểu, màu, chữ kèm theo).
- **Request**: `multipart/form-data`.

  | Tên | Vị trí | Kiểu | Bắt buộc | Validation (server) |
  |---|---|---|---|---|
  | `id` | path | int | Có | |
  | `setting_logo` | body | int | **Có** | `required|in:1,2,3` |
  | `type_design_qr` | body | int | **Có** | `required|in:1,2,3,4` |
  | `color_qr` | body | string | Không | `nullable|regex:/^#(?:[0-9a-fA-F]{3}){1,2}$/` |
  | `text_design_qr` | body | string (HTML) | Không | `nullable` |
  | `path_logo` | body | file | Không | Khi có file: `image|mimes:jpeg,png,jpg,gif,svg|max:10240` (10 MB) |
- **Response**: `{ "success": true }` (HTTP 200)
- **Lỗi**:

  | HTTP | Mô tả |
  |---|---|
  | 422 | Vi phạm validation (Laravel trả `errors`) |
  | 404 | `Bot not found` |
  | 404 | `Bot is free plan` — `bots.plan_type == 2` **không được dùng tính năng này** |
  | 404 | `Landing not found` (có kiểm `bot_id`) |
- **Side effect**: upload file vào `{FOLDER_MEDIA}media/images/{admin_id}/{bot_id}/landing/`, resize về tối đa 2048 px (bỏ qua SVG); `setting_logo != 3` ⇒ `path_logo = null`.
- **Nguồn**: `QRCodeController.php:3504-3585`; route `routes/web.php:2857`; client `mixins/setting_option.js:169`

---

### EP-24 — GET `/ajax/v2/landing/data`
- **Request params**: `id` (query, int) **hoặc** `uLand` (query, string — mã `landing.code`). Nếu cả hai cùng có, `id` được ưu tiên (ghi đè).
- **Response thành công**:
  ```json
  { "success": true, "data": { "landing": { "...", "path_landing": "https://...", 
      "new_link_qr_code": "https://.../landing-qr/{liff}?uLand=xxx", "link_qr_code": "..." },
      "bot_plan": 1, "hashBotId": "..." } }
  ```
- **Lỗi**: `{"success": false}` HTTP 404 khi không tìm thấy landing của bot; `HttpException 404 Bot not found` khi bot không tồn tại.
- **Nguồn**: `QRCodeController.php:3587-3615`; route `routes/web.php:2858`; client `mixins/setting_option.js:41`, `mixins/setting_qr_off.js:53`, `mixins/setting_external_link.js:80`

---

### EP-25 — POST `/ajax/v2/landing/edit/{id}/qr-off`
- **Mục đích**: Lưu cấu hình hiển thị khi QR ở trạng thái OFF + lịch bật/tắt tự động theo thời gian.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `id` | path | int | Có | |
  | `type_display_off` | body | int | Không | `0` = chạy action, `1` = hiển thị text, `2` = redirect URL |
  | `data_display_off` | body | string | Không | Nội dung text hoặc URL, tuỳ `type_display_off` |
  | `use_limit_time` | body | 0/1 | Không | Bật lịch giới hạn |
  | `use_limit_end_time` | body | 0/1 | Không | Có đặt thời điểm kết thúc hay không |
  | `limit_start_time` | body | `YYYY-MM-DD HH:mm:ss` | Không | |
  | `limit_end_time` | body | `YYYY-MM-DD HH:mm:ss` | Không | |
  | `use_action_limit` | body | 0/1 | Không | |
  | `action_limit_id` | body | int | Không | **Client có gửi nhưng server KHÔNG lưu** trường này ở đây (chỉ lưu qua EP-11 / EP-06) |
- **Response**: `{ "success": true }`
- **Lỗi**: 404 `Landing not found` (có kiểm `bot_id`).
- **Side effect**: khi 1 trong `limit_start_time` / `limit_end_time` / `use_limit_end_time` / `use_limit_time` đổi ⇒ `time_qr_off_status = 1` (đưa vào hàng đợi cho cron `landing:qr-off:schedule`). `type_display_off = 1` ⇒ `is_use_url_over_time = 0`, `text_over_time = data_display_off`, `url_over_time = null`; `= 2` ⇒ ngược lại.
- **Nguồn**: `QRCodeController.php:3617-3675`; route `routes/web.php:2859`; client `mixins/setting_qr_off.js:113`

---

### EP-26 — POST `/ajax/v2/landing/edit/{id}/external-setting`
- **Request params**: `is_on_param` (0/1), `is_on_html` (0/1), `is_on_callback` (0/1), `head_content` (HTML), `body_content` (HTML), `url_connect_qrcode_outside` (URL).
- **Validation**: chỉ `url_connect_qrcode_outside` được validate (`nullable|url`) và chỉ khi có giá trị.
- **Response thành công**: `{ "success": true }`
- **Lỗi**:

  | HTTP | Body | Mô tả |
  |---|---|---|
  | 404 | `Landing answer not found` | Landing không thuộc bot |
  | **410** | `{"success": false, "message": "有効なURLではありません。"}` | URL không hợp lệ (dùng mã 410 thay vì 422) |
- **Lưu ý**: 3 trường `head_content`, `body_content`, `url_connect_qrcode_outside` **luôn bị reset về null** rồi mới gán lại nếu request có giá trị ⇒ gửi thiếu trường = xoá dữ liệu cũ.
- **Nguồn**: `QRCodeController.php:3677-3733`; route `routes/web.php:2860`; client `mixins/setting_external_link.js:120`

---

### EP-27 — POST `/ajax/v2/landing/edit/{id}/parameters`
- **Request params**: `is_on_param` (0/1), `cid1`…`cid5` (int|null — id của `friend_information_setting`).
- **Logic**: luôn `updateOrCreate` đủ 5 bản ghi `landing_parameter` với `param_code = cid1..cid5`.
- **Response**: `{ "success": true }`
- **⚠**: câu update `landing.is_on_param` **không lọc `bot_id`** (`QRCodeController.php:3743-3747`).
- **Nguồn**: `QRCodeController.php:3735-3764`; route `routes/web.php:2861`; client `mixins/setting_external_link.js:171`

---

### EP-28 — GET `/ajax/v2/landing/edit/{id}/parameters`
- **Request params**: `id` (path, int).
- **Response**: `{ "data": [ { "id":1, "bot_id":..., "landing_id":..., "param_code":"cid1", "friend_information_id": -1, "friend_information_setting": {...} } ] }`
- **Lưu ý**: với `friend_information_id < 0` (trường mặc định hệ thống — cấu hình `sns-line.info_default_info_cross` / `info_default_info_address`), bản ghi bị **push 2 lần** vào mảng kết quả (`QRCodeController.php:3805-3813`) ⇒ khả năng trùng lặp hiển thị (Mức độ tin cậy: Cao — đọc trực tiếp từ code).
- **Nguồn**: `QRCodeController.php:3766-3816`; route `routes/web.php:2862`

---

### EP-29 / EP-30 — GET·POST `/ajax/v2/landing/{id}/poster-connect-qr-code` (LP Poster bước 1)
- **GET**: trả `{ "data": [ {"id":1, "poster_name":"広告A"} ] }`.
- **POST** (`Content-Type: application/json`):
  ```json
  { "poster_names": [ {"id": 1, "name": "広告A", "error": null}, {"id": null, "name": "広告B"} ] }
  ```

  | Tên | Vị trí | Kiểu | Bắt buộc | Validation |
  |---|---|---|---|---|
  | `poster_names` | body | array | **Có** | `required|array` |
  | `poster_names[].id` | body | int|null | — | `null` ⇒ tạo mới |
  | `poster_names[].name` | body | string | — | Chỉ validate ở client (bắt buộc, không trùng) |
- **Response**: `{ "success": true }`
- **Lỗi**: HTTP **403** `{"message": "再度ログインを行ってください。"}` khi bot ở gói free (`plan_type == 2`); 422 khi thiếu `poster_names`.
- **Side effect**: các `poster_connect_qrcode` cũ không xuất hiện trong payload sẽ bị **xoá cứng**, kèm xoá các `landing_page_poster_url` liên quan.
- **Nguồn**: `QRCodeController.php:3846-3877`; `Services/Landing/Poster/PosterSettingService.php:167-199`; routes `routes/web.php:2864-2865`; client `mixins/lp_poster/step1.js:13,52`

---

### EP-31 / EP-32 — GET·POST `/ajax/v2/landing/{id}/landing-url-qr-code` (LP Poster bước 2)
- **GET**: `{ "data": [ {"id":1, "landing_name":"LP-A", "landing_url":"https://..."} ] }`
- **POST** (JSON): `{ "landing_connect_qr": [ {"id":1, "landing_name":"LP-A", "landing_url":"https://..."} ] }` — validate `required|array`.
- **Response**: `{ "success": true }`; 403 khi gói free.
- **Side effect**: sau khi lưu, gọi `saveLandingPagePosterUrl()` để sinh **tích Descartes** `poster × landing_page` thành các bản ghi `landing_page_poster_url` với `code = Hashids::encode("{botId}{landingId}{posterId}{landingPageId}")`.
- **Nguồn**: `QRCodeController.php:3879-3910`; `PosterSettingService.php:18-90`; routes `routes/web.php:2866-2867`

---

### EP-33 — GET `/ajax/v2/landing/{id}/landing-page-connect-qr-code` (LP Poster bước 4)
- **Response**:
  ```json
  { "data": [ { "poster_name": "広告A",
      "landing_connected": [ {"landing_name":"LP-A",
        "landing_url":"https://lp.example.com/?uland=ab12cd&postcode=XyZ"} ] } ],
    "plan_type": 1 }
  ```
- **Lưu ý**: bot gói free (`plan_type == 2`) ⇒ `{"data": [], "plan_type": 2}`; bot không tồn tại ⇒ 404 `Bot not found`.
- **Nguồn**: `QRCodeController.php:3912-3930`; `PosterSettingService.php:112-146`; route `routes/web.php:2868`

---

### EP-34 — GET `/ajax/v2/landing/{id}/hash-id`
- **Response**: `{ "hashBotId": "<liff_app_id>", "lpPosterUrlDomain": "<env URL_OUTSIDE_STEP>", "uLand": "<landing.code>" }`
- **⚠**: `Landing::find($landingId)` **không lọc `bot_id`** ⇒ có thể đọc `code` QR của bot khác (`QRCodeController.php:3932-3943`).
- **Nguồn**: `QRCodeController.php:3932-3943`; route `routes/web.php:2869`

---

### EP-35 — GET `/ajax/v2/landing/{id}/landing-url-filter`
- **Response**: `{ "message": "success", "data": [ { "id":1, "code":"XyZ", "landing_page": {"id":1,"landing_name":"LP-A"}, "connect_qr_code": {"id":1,"poster_name":"広告A"} } ] }`
- Có lọc `bot_id`.
- **Nguồn**: `QRCodeController.php:2290-2298`; route `routes/web.php:2870`; client `detail.js:96`

---

### EP-36 — POST `/ajax/v2/landing/setting_intro/steps_modal`
- **Mục đích**: đánh dấu người dùng đã tắt modal hướng dẫn — set `users.hide_action_intro_modal = now()`.
- **Request params**: không có.
- **Response**: HTTP **204** No Content (body `null`). Mọi exception đều bị nuốt.
- **Nguồn**: `QRCodeController.php:3954-3965`; route `routes/web.php:2871`; client `public/js/qr_code/v2/setting_intro_steps.js:23`

---

### EP-37 — GET `/ajax/v2/landing/{id}/collect-statistic`
- **Request params**: `start_date`, `end_date` (date — phải có **cả hai** mới áp lọc), `type_count` (1 = distinct theo `line_id`/`device`, khác = đếm tất cả).
- **Response**:
  ```json
  { "message": "success", "data": {
      "total": 0, "total_click_pc": 0, "total_scan_pc": 0, "total_scan_mobile": 0,
      "total_new_friend": 0, "total_action_new_friend": 0,
      "total_un_block": 0, "total_action_un_block": 0,
      "total_action_user_not_show": 0, "total_action_friend_exist": 0 } }
  ```
- **Nguồn**: `QRCodeController.php:2332-2398`; route `routes/web.php:2872`; client `detail.js:401`

---

### EP-38 — GET `/ajax/v2/landing/{id}/collect-friend`
- **Request params**: `start_date`, `end_date`, `type` (1 = NOT_SHOW, 2 = UN_BLOCK, 3 = FRIEND, 4 = NEW_FRIEND), `type_count` (1 = gộp theo `line_id`), `page`, `per_page` (mặc định 10), `order[column]` (whitelist chỉ `time_click`), `order[dir]`.
- **Response**: `{ "message": "success", "data": {paginator}, "count_action": 0, "pagination": {...} }` — mỗi item có `lineUser` (kèm `conversation`) và cờ `is_blocked` được tính lại theo lần kết bạn đầu tiên.
- **Nguồn**: `QRCodeController.php:2400-2488`; route `routes/web.php:2873`; client `detail.js:424`

---

### EP-39 — GET `/ajax/v2/landing/{id}/detail-click-day`
- **Request params**: `day` (date, bắt buộc), `per_page` (mặc định 10), `page`, `type_count` (1 = distinct theo `device`), `order` + `dir` (**không whitelist** — truyền thẳng vào `orderBy`).
- **Response**: `{ "message": "success", "data": { "data": [...], "pagination": {...} } }`. Mỗi phần tử là bản ghi `collect_open_landings` được "làm phẳng" cùng dữ liệu `detail_landing_click` tương ứng (`flag_is_click`, `line_id`, `time_click`, `action`, `is_old_friend`, `is_action_web`, `post_code`, `is_landing_off`, `line_user`, `is_blocked`…).
- **Lỗi**: `HttpException` khi landing không tồn tại (lưu ý: gọi `new HttpException('...')` với tham số string ⇒ status code không chuẩn — Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:2533-2671`; route `routes/web.php:2874`; client `detail.js:479`

---

### EP-40 — POST `/ajax/get-list-group-landing` (v1)
- **Mục đích**: Endpoint đa năng bản cũ — vừa lấy danh sách vừa thực hiện CRUD thư mục/QR theo tham số `action`.
- **Request params**:

  | Tên | Vị trí | Kiểu | Ghi chú |
  |---|---|---|---|
  | `action` | body | string | `addAndEditGroup` / `deleteGroup` / `renameGroup` / `deleteLanding` / `sortFolder` / `moveFolder` |
  | `id`, `group_id`, `group_name`, `land_id`, `sort_ids`, `sort_position`, `item_ids`, `folder_move` | body | mixed | Tuỳ `action` |
  | `perPage` | body | int | Có ⇒ trả kèm `totalPage` |
- **Response**: `{ "status": true, "groups": [...], "landings": [...], "items": [], "group_open": 0, "items_default": [...], "count_default": 0, "qrCodeNumber": 0, "totalPage": 1 }`
- **Lỗi**: bắt exception → `{"status": false, "message": "..."}` với **HTTP 200**.
- **⚠**: `action = deleteGroup` / `deleteLanding` là thao tác **xoá thật** qua một POST không phân biệt method (Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:739-889`; route `routes/web.php:2831`

---

### EP-41 — POST `/ajax/get-init-detail-landing` (v1)
- **Request params**: `id`, `start_date`, `end_date`, `tab` (`tab1`/`tab2`), `only_new_friend` (`"true"`/`"false"`), `only_old_friend`.
- **Response**: `{ "success": true, "data_tab1": [...], "data_tab2": [...], "total_friend_new": 0, "total_friend_old": 0 }`
- **Nguồn**: `QRCodeController.php:1732-1847`; route `routes/web.php:2877`; view v1 `resources/views/basic/qr_code/show_friend_click.blade.php:250`

---

### EP-42 — POST `/ajax/get-sort-landing`
- **Request params**: `sort_ids` (string CSV các landing id).
- **Logic**: gán `position = index + 1`; giữ nguyên `updated_at` cũ (tránh làm "nhảy" sắp xếp theo thời gian cập nhật).
- **Response**: `{ "success": true }`
- **Nguồn**: `QRCodeController.php:2708-2720`; route `routes/web.php:2879`; client `index.js:822` (khối `sortedQrs`)

---

### EP-43 — POST `/ajax/init-data-sort-landing` ⚠ ROUTE HỎNG
- Route khai báo `Basic\QRCodeController@initDataSort` (`routes/web.php:2881`) nhưng **method `initDataSort` không tồn tại** trong `QRCodeController`. Gọi endpoint này sẽ ném `BadMethodCallException` ⇒ HTTP 500.
- **Mức độ tin cậy**: Cao (đã liệt kê toàn bộ method của controller và không tìm thấy).

---

### EP-44 — POST `/ajax/landing/init-data-action`
- **Request params**: `action_id` (int), `intro_action_id` (int).
- **Response**: `{ "success": true, "actionDetail": [...], "actionDetailIntro": [...] }` — mỗi item đã lọc bỏ action "mồ côi" (tham chiếu tag/template/scenario đã xoá — issue #38695) và tính lại `has_filters` (issue #38700).
- **Nguồn**: `QRCodeController.php:2673-2706`; route `routes/web.php:3349`

---

### EP-45 — POST `/ajax/landing/save-preview-intro`
- **Request params**: `id` (landing id), `type` (`page` | `message`), `title_page`, `content_page` (khi `type = page`), `intro_message` (khi `type = message`).
- **Response**: `{ "success": true }` — **luôn success** kể cả khi landing không tồn tại.
- **⚠**: **không lọc `bot_id`** (`QRCodeController.php:3442`).
- **Nguồn**: `QRCodeController.php:3439-3460`; route `routes/web.php:3351`

---

### EP-46 — GET `/basic/landing/v2/edit/{id}`
- **Response**: render `basic.qr_code.v2.edit` với `id`, `landingRecord` (đã bổ sung `general_message`, `user_intro_action_message`, `path_landing` full URL, `new_link_qr_code`, `link_qr_code`), `richMenus`, `scenario`, `hideActionIntroModal`.
- **Lỗi**: 302 → `/basic/landing` khi landing không thuộc bot; 302 → route `404` khi có exception.
- **Nguồn**: `QRCodeController.php:602-635`; route `routes/web.php:982`

---

### EP-47 — GET `/basic/landing/v2/edit/{id}/poster`
- **Response**: render `basic.qr_code.v2.lp_poster` với `landingId`, `landing`.
- **Lỗi**: 302 → `/basic/landing` khi bot ở gói free (`plan_type == 2`) hoặc landing không thuộc bot.
- **Nguồn**: `QRCodeController.php:3818-3844`; route `routes/web.php:984`

---

### EP-48 — GET `/basic/landing/v2/preview-message-scan-qr/{id}`
- **Response**: render `basic.qr_code.v2.preview_message_scan_qr` với `landing`.
- **Lỗi**: 302 → route `404` khi không tìm thấy landing. **Không lọc `bot_id`**.
- **Nguồn**: `QRCodeController.php:1509-1515`; route `routes/web.php:983`

---

### EP-49 — GET `/basic/landing/show/{id}`
- **Response**: render `basic.qr_code.v2.show_friend_click` với `landing`, `name`, `startDate` (đầu tháng), `endDate` (hôm nay), `landingCreatedAt`, `googleSheetId`.
- **Lỗi**: 302 → `/basic/landing` khi landing không thuộc bot (**có** kiểm `bot_id`).
- **Nguồn**: `QRCodeController.php:1716-1730`; route `routes/web.php:988`

---

### EP-50 — POST `/basic/create-landing-v2`
- **Mục đích**: Tạo QR mới (chế độ thường) hoặc sao chép QR có sẵn (chế độ `copy`).
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `newQrs` | body | object | Chế độ tạo mới | Toàn bộ trường sẽ được merge vào bản ghi `landing`. Client chỉ gửi `newQrs.name` |
  | `newQrs.name` | body | string | Có (client) | Client: bắt buộc, ≤ 50 ký tự. **Server không validate** |
  | `mode` | body | string | Chế độ copy | `copy` |
  | `id` | body | int | Chế độ copy | ID QR nguồn |
  | `X-CSRF-TOKEN` | header | string | **Có** | Route KHÔNG nằm trong `/ajax/*` |
- **Request mẫu (tạo mới)**: `{ "newQrs": { "name": "キャンペーンQR" } }`
- **Request mẫu (sao chép)**: `{ "id": 42, "mode": "copy" }`
- **Response thành công**: `{ "status": true, "id": 123 }` — client redirect tới `/basic/landing/v2/edit/{id}`.
- **Lỗi**:

  | HTTP | Body | Mô tả |
  |---|---|---|
  | 500 | `{"status": false, "message": "Bot does not exist"}` | Bot không tồn tại |
  | 500 | `{"status": false, "message": "現在のプランは利用できない機能です。アップグレードが必要になります。"}` | Gói free đã đủ 3 QR (kiểm trước insert) |
  | 500 | `{"status": false, "message": PlanLimitGuard::PLAN_MESSAGE}` | Đếm lại sau insert vẫn vượt ⇒ **xoá QR vừa tạo** |
  | 500 | `{"status": false, "message": "<exception message>"}` | Exception khác |
- **⚠ Nghiêm trọng (Mức độ tin cậy: Cao)**: `$settings = array_merge($settings, $newQrs)` rồi `DB::table('landing')->insertGetId($settings)` — **mass assignment không giới hạn**. Client có thể gửi bất kỳ cột nào của bảng `landing` (kể cả `bot_id`, `connect_aff`, `total_user_click`…). Cột không tồn tại ⇒ SQL error → 500.
- **⚠**: chế độ `copy` chỉ `where('id', $request->input('id'))` — **không lọc `bot_id`** ⇒ có thể sao chép QR của bot khác (`QRCodeController.php:245-247`).
- **Nguồn**: `QRCodeController.php:196-420`; route `routes/web.php:840`; client `index.js:437` (tạo) và `index.js:790` (copy)

---

### EP-51 — GET `/basic/landing-qr/link-google`
- **Response**: render `basic.qr_code.v2.link_google` với `landingConnectGoogle`, `google_sheet_auth_url`.
- **Side effect**: nếu bot chưa có bản ghi `landing_connect_google` ⇒ tự tạo mới với `status = DONE (2)`.
- **Nguồn**: `QRCodeController.php:1228-1246`; route `routes/web.php:1278`

---

### EP-52 — GET `/basic/landing-qr/redirect-google-sheet`
- **Request params** (do Google gửi về): `code` (authorization code), `scope` (string), `state` (= `bot_id`), `error` (khi user từ chối).
- **Response**: redirect về `landing.linkGoogle` kèm session `message`.
- **Lỗi**:

  | Trường hợp | Kết quả |
  |---|---|
  | Có `error` | 302 → `landingIndex` |
  | Thiếu scope `.../auth/spreadsheets` | 302 → `landing.linkGoogle` + message 「Google スプレッドシートのアクセス権限をチェックしてください」 |
  | `state` không phải bot hợp lệ | 302 → route `404` |
  | `Google_Exception` | 302 → `landing.linkGoogle` |
- **Side effect**: lưu `google_access_token`, `google_account_name`, `google_account_avatar`, `connect_time`, `status = WAITING (0)`.
- **⚠**: `state` (= `bot_id`) đến từ query string, **không đối chiếu với bot đang đăng nhập** (Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:1248-1284`; route `routes/web.php:1279`

---

### EP-53 — GET `/basic/landing-qr/cancel-google-sheet/{id}`
- **Request params**: `id` (path — id bản ghi `landing_connect_google`).
- **Response**: 302 `redirect()->back()`.
- **Lỗi/chặn**: nếu `status ∈ {PROCESSING(1), ERROR(3), WAITING(0)}` ⇒ redirect back kèm message 「スプレッドシートを作成しているため、接続を解除できません。３〜5分少し待ってから操作してください。」
- **Side effect**: xoá token + thông tin tài khoản Google; set `landing.google_sheet_id = null` cho **toàn bộ** landing của bot (kể cả bản đã xoá mềm).
- **⚠**: `$id` **không đối chiếu `bot_id`** ⇒ có thể huỷ liên kết Google của bot khác (`QRCodeController.php:1288-1289`).
- **Nguồn**: `QRCodeController.php:1286-1307`; route `routes/web.php:1280`

---

### EP-54 — GET `/basic/landing-qr/removed`
- **Response**: render `basic.qr_code.v2.qrs_removed` (không truyền biến; dữ liệu nạp qua EP-07).
- **Nguồn**: `QRCodeController.php:1309-1312`; route `routes/web.php:1281`

---

### EP-55…EP-60 — Nhóm endpoint v1 (legacy)

| ID | Endpoint | Ghi chú |
|---|---|---|
| EP-55 | GET `/basic/create-landing` → view `basic.qr_code.create` | Sinh sẵn `codeLanding` random 6 ký tự (`str_random(6)`, có kiểm trùng trong phạm vi bot) — `QRCodeController.php:152-178` |
| EP-56 | GET `/basic/landing/edit/{id}` → view `basic.qr_code.create` | Có kiểm `bot_id` — `QRCodeController.php:572-600` |
| EP-57 | GET `/basic/landing/copy/{id}` → view `basic.qr_code.create` | Clone action qua `MessageTemplateController@cloneMutilpleAction` — `QRCodeController.php:687-737` |
| EP-58 | POST `/basic/create-landing` | Params: `name`, `codeLanding`, `connect_aff`, `action_type`, `action_id`, `action_friend`, `action_qrcode_normal`, `url_connect_qrcode_outside`, `category_id`, `head_content`, `body_content`, `bill_type`, `interval_action`, `time_interval_action`, `intro_action_id`, `title_page_intro`, `content_page_intro`, `message_intro`, `actionLanding`. Response: `{"status": true}` / `{"status": false}` (500) — `QRCodeController.php:447-566` |
| EP-59 | POST `/basic/landing/edit/{id}` | **Validation server**: `name` → `required|max:255`, message lỗi 「QRコードアクション名は必須です。」. Response: 302 → `landingIndex`; lỗi ⇒ 302 → route `404`. **Update không lọc `bot_id`** (`:1610` ≈ `QRCodeController.php:657`) — `QRCodeController.php:637-685` |
| EP-60 | POST `/basic/landing/delete` | Params: `id` (array). Xoá mềm landing + xoá `detail_landing_click`. **Không lọc `bot_id`**. Response: `{"status": true}` HTTP 200 — `QRCodeController.php:1698-1714` |

> Route v1 tại `routes/web.php:839, 842, 844, 979, 981, 986`. Màn hình v1 (`basic.qr_code.create`) **không còn entry point từ UI v2**, nhưng route vẫn sống (comment trong code `QRCodeController.php:449-451` xác nhận điều này và là lý do đã bổ sung chốt chặn `PlanLimitGuard` cho `saveLanding`).

---

### EP-63 — GET `/landing-qr/{liffId}` — **PUBLIC**
- **Mục đích**: Đích đến của link/QR code. Render trang LIFF hiển thị QR (trên PC) hoặc tự động redirect vào ứng dụng LINE (trên mobile).
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `liffId` | path | string | Có | `bots.liff_app_id` — **thực tế không dùng để tra cứu**, chỉ để LINE nhận diện |
  | `uLand` | query | string | Có (thực tế) | `landing.code` — khoá tra cứu thật |
  | `device` | query | string | Không | `pc` ⇒ ép coi như quét từ PC |
  | `postcode` | query | string | Không | `landing_page_poster_url.code` — dùng để quy về nguồn quảng cáo |
- **Response thành công**: render `basic.qr_code.qr_landing` với `landing`, `device`, `postCode`.
- **Response đặc biệt khi QR OFF**:

  | Điều kiện | Kết quả |
  |---|---|
  | `status = 0` và `type_display_off = 2` | `redirect()->away($landing->data_display_off)` |
  | `status = 0` và `type_display_off = 1` | Trả về **HTML thô** `<p style="...">{data_display_off}</p>` (mặc định 「現在、友だち追加は受け付けていません。」) |
- **Lỗi**:

  | HTTP | Mô tả |
  |---|---|
  | 302 → `404` | `uLand` không khớp landing nào; hoặc bot không tồn tại (kèm thông báo Chatwork) |
  | 302 → `410` | Bot trả phí đã hết hạn > 7 ngày, hoặc `bot_contracts.status = 3` |
- **⚠**: `data_display_off` được echo trực tiếp không escape ⇒ nguy cơ **XSS** (Mức độ tin cậy: Cao — `QRCodeController.php:1687`).
- **Nguồn**: `QRCodeController.php:1643-1696`; route `routes/web.php:823`; view `resources/views/basic/qr_code/qr_landing.blade.php`

---

### EP-64 — POST `/ajax/v2/landing/{id}/count-scan-qr-code` — **PUBLIC**
- **Mục đích**: Ghi nhận một lượt mở trang QR (click trên PC / scan trên mobile).
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `id` | path | int | Có | Landing id |
  | `type` | body | int | Không | `1` = PC, `2` = MOBILE. Mặc định `1` |
  | `bot_id` | body | int | Không | Nhận từ client **nhưng không dùng** — controller lấy `landing->bot_id` |
  | `device` | body | string | Không | `pc` ⇒ tính là scan |
  | `device_id` | body | string | Không | Sinh ở client, lưu vào cookie `device_scan_landing` (TTL 365 ngày) |
  | `post_code` | body | string | Không | `landing_page_poster_url.code` |
- **Request mẫu**:
  ```
  POST /ajax/v2/landing/42/count-scan-qr-code
  type=2&bot_id=7&device=&device_id=k3jf9x1712345678901&post_code=XyZ
  ```
- **Response thành công**: `{ "message": "success" }`
- **Lỗi**: `HttpException('Landing not found')` khi id sai (tham số truyền vào là string ⇒ status code không chuẩn).
- **Side effect**: tạo bản ghi `collect_open_landings` (`bot_id`, `landing_id`, `ip`, `type`, `is_scan`, `date_scan = Ymd`, `device`, `post_code`); khi `type = MOBILE` hoặc `device = pc` ⇒ tăng `landing.total_user_click`.
- **⚠**: public, không CSRF, không rate limit ⇒ có thể **bơm số liệu thống kê** tuỳ ý (Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:2300-2330`; route `routes/web.php:4068`; client `resources/views/basic/qr_code/qr_landing.blade.php:100`

---

### EP-65 — GET `/landing/page-intro/{id}/{u_code}` — **PUBLIC**
- **Mục đích**: Trang「友だち紹介」cho LINE User đã là bạn — hiển thị nội dung giới thiệu và nút chia sẻ link kèm mã người giới thiệu.
- **Request params**: `id` (path — **thực tế là `landing.code`**, không phải id số), `u_code` (path — `bot_line_user.u_code`).
- **Response**: render `basic.qr_code.page_intro` với `lineUser`, `data` (landing), `messageEncoding`, `uCode`, `url_link_landing`, `botName`.
- **Logic dựng link chia sẻ**: ưu tiên `bots.domain_url_shorten`, kế đến `env('URL_OUTSIDE_STEP')`, cuối cùng `landing.link_qr_code`; kèm query `&u_code_intro={u_code}` để quy công người giới thiệu.
- **Lỗi**: không có nhánh lỗi — `u_code` sai ⇒ vẫn render view với `data = null`.
- **Nguồn**: `QRCodeController.php:3391-3424`; route `routes/web.php:831`

---

### EP-66 — GET `/landing/preview-page-intro/{type}/{id}` — **PUBLIC**
- **Request params**: `type` (path — `page` | `message`), `id` (path — landing id).
- **Response**: render `basic.qr_code.v2.preview_page_intro` với `type_preview`, `data`.
- **⚠**: public + **không lọc `bot_id`** ⇒ có thể xem nội dung trang giới thiệu của bất kỳ landing nào nếu biết id (Mức độ tin cậy: Cao).
- **Nguồn**: `QRCodeController.php:3426-3437`; route `routes/web.php:829`

---

### EP-67 / EP-68 — GET `/open-mobile/{type}/{id}` · `/open-external-browser/{type}/{id}` — **PUBLIC**
- **Mục đích**: Trang trung gian điều hướng LINE User vào LIFF app (mobile) hoặc trình duyệt ngoài.
- **Request params**: `type` (path — `booking_calendar`, `product-detail`, `product-change`, `product-cancel`, `booking_event`, `form_answer`, `calendar`, `calendar-salon` — `calendar` và `calendar-salon` **chỉ có ở `openMobile`**), `id` (path), `aff_id`, `lp_id`, `aff_setting_id` (query, tuỳ chọn).
- **Response**: render `basic.qr_code.open_mobile` / `basic.qr_code.open_external_browser` với `bot`, `id`, `type`, `aff_id`, `lp_id`, `aff_setting_id`.
- **Ghi chú**: hai endpoint này **dùng chung cho nhiều tính năng khác** (đặt lịch, form, sản phẩm), không riêng QR Code Action → ứng viên shared component.
- **Nguồn**: `QRCodeController.php:2722-2768` và `:2770-2808`; routes `routes/web.php:825, 827`

---

### EP-69 — POST `/ajax/open-mobile/check-friend` — **PUBLIC**
- **Mục đích**: Kiểm tra LINE User đã là bạn của bot chưa; nếu chưa/đã block thì gọi LINE API lấy profile, **tạo/khôi phục** quan hệ bạn bè, rồi trả URL đích tương ứng với `type`.
- **Request params**:

  | Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
  |---|---|---|---|---|
  | `line_id` | body | string | Có | LINE user id |
  | `bot_id` | body | int | Có | |
  | `id` | body | mixed | Có | ID/unique_key của đối tượng theo `type` |
  | `type` | body | string | Có | Như EP-67 |
  | `aff_id`, `lp_id`, `aff_setting_id` | body | int | Không | Tham số affiliate |
  | `tab`, `booking_id` | body | mixed | Không | Chỉ dùng cho `calendar` / `calendar-salon` |
- **Response thành công**: `{ "status": true, "url": "<url đích>", "is_friend": true|false }`
- **Response thất bại**: `{ "status": false, "url": "<bot.url_add_friend | route 404>", "is_friend": false }`
- **Side effect (rất nặng)**: có thể tạo `line_user`, `bot_line_user` (sinh `u_code` 10 ký tự duy nhất), `conversation`, `messages_v2` (kind `ADD_OLD_FRIEND`), `bot_friend_statistic`, `line_user_add_friend_history`, `aff_result`; gửi tin nhắn qua `TemplateService@sendMessageAction`; chạy action kết bạn qua `sendAction(...)`; push notify qua `MobileNotifyService@insertNotifyOldFriend`.
- **⚠ Nghiêm trọng (Cao)**: endpoint public, không CSRF, nhận `line_id` + `bot_id` trực tiếp ⇒ người ngoài có thể ép hệ thống tạo/khôi phục quan hệ bạn bè và kích hoạt gửi tin nhắn.
- **Nguồn**: `QRCodeController.php:2810-3389`; route `routes/web.php:833`

---

## 3. Middleware áp dụng

| Middleware | Class | Vai trò |
|---|---|---|
| `basic_access` | `App\Http\Middleware\BasicAccess` — `sns-line/app/Http/Middleware/BasicAccess.php` | Chốt phân quyền chính của portal Admin/Staff. Yêu cầu `Auth::check()` và `role ∈ {-1, 0, 1, 2}`. Nếu user là **Staff được mời** (`bots.admin_id !== Auth::id()` hoặc session `is_bot_invite`), lấy whitelist route theo `bot_role_access` + `access_feature` qua `getRouterBotInvite()`; route hiện tại không nằm trong whitelist ⇒ redirect `adminIndex` kèm lỗi 「この権限は許可されていません。」. Route `landingIndex` được seed trong bảng `access_feature` với tên 「流入アクション」 (`sns-line/database/seeds/AccessFeatureSeeder.php:15-46`) |
| `https_protocol` | `App\Http\Middleware\HttpsProtocol` | Ép chuyển hướng sang HTTPS |
| `is_expire` | `App\Http\Middleware\IsExpire` — `sns-line/app/Http/Middleware/IsExpire.php` | Chặn khi hệ thống bảo trì (`env MAINTAIN_SERVE`) → route `maintain`; chặn khi bot hết hạn hợp đồng / hết hạn gói free → route `pointSettings`; bot không tồn tại → `/admin/home` |
| `check_remember_token` | `App\Http\Middleware\CheckRememberToken` — `sns-line/app/Http/Middleware/CheckRememberToken.php` | So `session('remember_token')` với `users.remember_token_reset_pass`; lệch ⇒ logout. Với AJAX trả **HTTP 200** kèm `{status:false, message:"ログイン情報が変更されましたので、再度ログインしてください。"}` (không phải 401) |
| `check_login` | `App\Http\Middleware\CheckLogin` | Áp cho toàn bộ nhóm `/ajax/*` (`routes/web.php:2485`) — yêu cầu đã đăng nhập |
| `LogRequestMultipart` | `App\Http\Middleware\LogRequestMultipart` | Ghi log request multipart; bọc nhóm route `/basic/create-landing*`, `/basic/landing/edit/*`, `/basic/landing/delete` (`routes/web.php:836`) |
| `NotifyChatworkRequestTimeSlow` | `App\Http\Middleware\NotifyChatworkRequestTimeSlow` | Bọc gần như toàn bộ `web.php` từ dòng 81 — cảnh báo Chatwork khi request chậm. **Không phải middleware xác thực** |
| CSRF | `App\Http\Middleware\VerifyCsrfToken` — `sns-line/app/Http/Middleware/VerifyCsrfToken.php:14-53` | Toàn bộ URL khớp `'/ajax/*'` được **miễn CSRF**. Các endpoint dưới prefix `/basic/` (EP-50, EP-58, EP-59, EP-60) **bắt buộc** header `X-CSRF-TOKEN` |

### Ma trận middleware theo nhóm route

| Nhóm route | Khai báo | Middleware |
|---|---|---|
| Trang Admin `/basic/...` | `routes/web.php:882` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` |
| POST form v1/v2 `/basic/create-landing*`, `/basic/landing/edit/*`, `/basic/landing/delete` | `routes/web.php:836-837` | `LogRequestMultipart`, `https_protocol`, `is_expire`, `check_remember_token` (**thiếu `basic_access`** ⇒ Staff bị chặn ở màn hình nhưng không bị chặn ở endpoint lưu — Mức độ tin cậy: Cao) |
| AJAX `/ajax/...` | `routes/web.php:2485` | `check_login`, `check_remember_token` |
| Public | `routes/web.php:81` (bọc ngoài) | Chỉ `NotifyChatworkRequestTimeSlow` |

---

## 4. Liên kết endpoint ↔ màn hình UI

> ui-spec.md chưa có → dùng **tên view blade + file JS** làm cầu nối. **Chờ đối chiếu ui-spec** để gán mã `SCR-QRL-xx`.

| View blade | File JS điều khiển | Endpoint sử dụng |
|---|---|---|
| `basic.qr_code.v2.index` (danh sách QR) | `public/js/qr_code/v2/index.js` | EP-01 (render), EP-02, EP-03, EP-04, EP-06, EP-12, EP-16 (tải CSV), EP-17, EP-18, EP-19, EP-20, EP-21, EP-42, EP-50, EP-62 |
| `basic.qr_code.v2.edit` (chỉnh sửa QR — nhiều tab) | `public/js/qr_code/v2/edit.js` + `mixins/*` | EP-06, EP-09, EP-10, EP-11, EP-13, EP-14, EP-17, EP-22, EP-23, EP-24, EP-25, EP-26, EP-27, EP-28, EP-33, EP-44, EP-46 (render) |
| `basic.qr_code.v2.lp_poster` (LP Poster 4 bước) | `mixins/lp_poster/step1..step4.js` | EP-29, EP-30, EP-31, EP-32, EP-33, EP-34, EP-47 (render) |
| `basic.qr_code.v2.show_friend_click` (thống kê chi tiết) | `public/js/qr_code/v2/detail.js` | EP-16, EP-35, EP-37, EP-38, EP-39, EP-49 (render) |
| `basic.qr_code.v2.qrs_removed` (thùng rác) | `public/js/qr_code/v2/qrs_removed.js` | EP-07, EP-08, EP-54 (render) |
| `basic.qr_code.v2.link_google` (liên kết Google Sheet) | — | EP-51 (render), EP-52, EP-53 |
| `basic.qr_code.v2.preview_message_scan_qr` | `public/js/qr_code/v2/preview_message_scan_qr.js` | EP-13, EP-48 (render) |
| `basic.qr_code.v2.preview_page_intro` | — | EP-45, EP-66 (render) |
| `basic.qr_code.qr_landing` (**LINE User** — trang QR) | inline + `public/js/qr_code/qr_landing.js` | EP-63 (render), EP-64 |
| `basic.qr_code.page_intro` (**LINE User** — trang giới thiệu) | — | EP-65 (render) |
| `basic.qr_code.open_mobile` / `open_external_browser` (**LINE User**) | — | EP-67, EP-68 (render), EP-69 |
| `basic.qr_code.create` / `basic.qr_code.index` / `basic.qr_code.show_friend_click` (**v1 legacy**) | — | EP-40, EP-41, EP-55, EP-56, EP-57, EP-58, EP-59, EP-60 |
| Sidebar (mọi màn hình Admin) | `resources/views/layout/basic/sidebar.blade.php:409-411` | Mục menu 「QRコードアクション」 → `landingIndex` |

---

## 5. Ghi chú tổng hợp

1. **Tổng số endpoint**: 69 — **62 endpoint Admin/Staff** (EP-01…EP-62) và **7 endpoint Public/LINE User** (EP-63…EP-69).
2. **v1 vs v2**: 12 endpoint thuộc thế hệ v1 (EP-40, EP-41, EP-55…EP-60 và view `basic.qr_code.create`), vẫn hoạt động nhưng không có entry point từ UI hiện tại.
3. **1 route hỏng**: EP-43 (`/ajax/init-data-sort-landing` → `initDataSort` không tồn tại).
4. **1 route rỗng**: EP-05 (`ajaxSortQrs` là method rỗng, trả `null` ⇒ HTTP 200 body rỗng).
5. **Chuẩn response không thống nhất**: 4 dạng cùng tồn tại — `{message: "success"}`, `{success: true}`, `{status: true}`, và HTTP 204. Mã lỗi cũng không chuẩn (dùng 500 cho lỗi nghiệp vụ, 410 cho URL sai, 404 cho lỗi gói cước).
6. **Kiểm quyền sở hữu `bot_id` không đồng nhất** — xem bảng chi tiết trong `logic-spec.md` mục "Authorization".
