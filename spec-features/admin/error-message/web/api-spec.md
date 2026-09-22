# API Spec — FA-028 「配信エラー」 (Lỗi phát hành / Error message)

- **Portal**: Admin (LINE OA)
- **Mã tính năng**: FA-028
- **Màn hình chính**: `GET /basic/error-list-v2` — title 「配信エラー」
- **Controller chính**: `app/Http/Controllers/Basic/MessageErrorController.php` (v2, đang dùng)
- **Controller legacy**: `app/Http/Controllers/Basic/ErrorListController.php` (v1, phần lớn đã bị vô hiệu hoá)
- **Nguồn phân tích**: `routes/web.php`, 2 controller trên, `public/js/error_list/index_v2.js`, `public/js/error_list/modal-detail-message.js`, `resources/views/basic/error_list/v2/*.blade.php`
- **Mức độ tin cậy tổng thể**: **Cao** (toàn bộ endpoint được đọc trực tiếp từ route + controller + JS gọi API)

---

## 1. Bảng tổng hợp endpoints

### 1.1. Nhóm v2 — đang được UI 「配信エラー」 sử dụng

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Xác thực |
|----|--------|-----|-------|-------------------|-----------|----------|
| EP-01 | `GET` | `/basic/error-list-v2` | Render màn hình chính 「配信エラー」 | `Basic\MessageErrorController@index` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Session Admin/Staff + bot đang chọn |
| EP-02 | `POST` | `/ajax/get-message-error` | Nạp danh sách bản ghi lỗi theo tab + nguồn (có phân trang) | `Basic\MessageErrorController@ajaxGetMessageError` | `check_login`, `check_remember_token` | Session + CSRF token |
| EP-03 | `GET` | `/ajax/get-detail-error-message` | Nạp dữ liệu modal 「エラーメッセージ詳細」 | `Basic\MessageErrorController@getDataPreviewMessage` | `check_login`, `check_remember_token` | Session |
| EP-04 | `POST` | `/ajax/save-setting-message-error` | Đăng ký gửi lại / gửi ngay / xoá **1 bản ghi** | `Basic\MessageErrorController@saveSettingErrorMessage` | `check_login`, `check_remember_token` | Session + CSRF |
| EP-05 | `POST` | `/ajax/save-setting-message-error-all` | Đăng ký gửi lại / gửi ngay / xoá **nhiều bản ghi** (hoặc toàn bộ theo bộ lọc) | `Basic\MessageErrorController@saveSettingErrorMessageAll` | `check_login`, `check_remember_token` | Session + CSRF |
| EP-06 | `POST` | `/ajax/delete-message-error` | Xoá bản ghi lỗi hoặc huỷ đăng ký gửi lại (hàng loạt) | `Basic\MessageErrorController@ajaxDeleteErrorMessage` | `check_login`, `check_remember_token` | Session + CSRF |
| EP-07 | `POST` | `/ajax/update/last-time-message-error` | Đánh dấu đã xem lỗi mới nhất (tắt badge thông báo) | `Basic\ErrorListController@updateLastTimeShowError` | `check_login`, `check_remember_token` | Session + CSRF |

Vị trí khai báo route (`routes/web.php`):

| ID | Dòng | Route name | Nhóm |
|----|------|-----------|------|
| EP-01 | `routes/web.php:887` | `errorListV2` | `Route::group(['prefix' => 'basic', 'middleware' => ['basic_access','https_protocol','is_expire','check_remember_token']])` tại `routes/web.php:882` |
| EP-02 | `routes/web.php:2520` | `ajaxGetMessageError` | `Route::group(['prefix' => 'ajax', 'middleware' => ['check_login','check_remember_token']])` tại `routes/web.php:2485` |
| EP-03 | `routes/web.php:2522` | `errorMessage.getDataPreviewMessage` | như trên |
| EP-04 | `routes/web.php:2524` | `errorMessage.saveSettingErrorMessage` | như trên |
| EP-05 | `routes/web.php:2526` | `errorMessage.saveSettingErrorMessageAll` | như trên |
| EP-06 | `routes/web.php:2518` | `ajaxDeleteErrorMessage` | như trên |
| EP-07 | `routes/web.php:3509` | `update.last.time.show.message.error` | như trên |

> **Lưu ý**: `MessageErrorController@getListHistorySend()` (`MessageErrorController.php:61`) **không có route riêng** — nó được `ajaxGetMessageError()` gọi nội bộ khi `error_tab == 'history_send'` (`MessageErrorController.php:167`). Mức độ tin cậy: **Cao**.

### 1.2. Nhóm legacy v1 — `ErrorListController` (giữ lại nhưng phần lớn không còn dùng ở màn hình v2)

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Ghi chú |
|----|--------|-----|-------|-------------------|-----------|---------|
| EP-08 | `GET` | `/basic/error-list` | Màn hình lỗi v1 — **luôn redirect sang `errorListV2`** | `Basic\ErrorListController@index` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | `routes/web.php:1016` (route name `errorList`, cùng nhóm `routes/web.php:882`). `ErrorListController.php:74` là `return redirect()->route('errorListV2');` → toàn bộ code phía dưới là **dead code** |
| EP-09 | `GET` | `/basic/error-list-setting/{id}` | Render/trả JSON chi tiết 1 message lỗi (v1) | `Basic\ErrorListController@renderViewSetting` | `check_login`, `check_remember_token` | `routes/web.php:2052` |
| EP-10 | `POST` | `/basic/update-error` | Xoá message + bản ghi lỗi (v1) | `Basic\ErrorListController@setting` | `check_login`, `check_remember_token` | `routes/web.php:2054` |
| EP-11 | `GET` | `/basic/update-error-checked` | Xoá hàng loạt message + bản ghi lỗi theo danh sách message id (v1) | `Basic\ErrorListController@settingMessages` | `check_login`, `check_remember_token` | `routes/web.php:2056` |
| EP-12 | `POST` | `/basic/send-message` | Gửi lại ngay 1 message qua LINE API (v1, đồng bộ) | `Basic\ErrorListController@sendMessage` | `check_login`, `check_remember_token` | `routes/web.php:2058` |
| EP-13 | `POST` | `/basic/resend-all` | Gửi lại ngay nhiều message qua LINE API (v1, đồng bộ) | `Basic\ErrorListController@resendAll` | `check_login`, `check_remember_token` | `routes/web.php:2060` |
| EP-14 | `POST` | `/basic/send-message-checked` | Đăng ký gửi lại theo lịch (v1) | `Basic\ErrorListController@sendMessageChecked` | `check_login`, `check_remember_token` | `routes/web.php:2062` |

> Nhóm EP-09…EP-14 nằm trong `Route::middleware(['check_login', 'check_remember_token'])->group(...)` khai báo tại `routes/web.php:1877` — nhóm này **không có prefix**, nên URL giữ nguyên `/basic/...`. Mức độ tin cậy: **Cao** (xác định bằng quét khớp dấu ngoặc trên `routes/web.php`).

---

## 2. Chi tiết từng endpoint

### EP-01 — `GET /basic/error-list-v2`

**Mô tả**: Trả về view `basic.error_list.v2.index` — khung màn hình 「配信エラー」. Toàn bộ dữ liệu bảng được nạp sau bằng AJAX (EP-02), controller chỉ đẩy sẵn bảng mã lỗi để tab 「エラー原因一覧」 render tĩnh.

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:52-60`

**Request params**: không có.

**Dữ liệu truyền vào view**

| Biến | Kiểu | Nguồn | Mô tả |
|------|------|-------|-------|
| `tableErrorCode` | array | `config('sns-line.table_error_code')` — `config/sns-line.php:1099-1132` | Bảng mã lỗi 001–007 + `other`, hiển thị ở tab 「エラー原因一覧」 |

**Lỗi có thể xảy ra**

| HTTP | Nguyên nhân | Xử lý |
|------|------------|-------|
| 302 | Chưa đăng nhập / hết hạn phiên (`check_remember_token`, `is_expire`) | Redirect trang đăng nhập |
| 302 | Không có quyền truy cập bot (`basic_access`) | Redirect |

> `$bot_id = getBotId();` tại `MessageErrorController.php:53` được gán nhưng **không sử dụng** — mức độ tin cậy: **Cao**.

---

### EP-02 — `POST /ajax/get-message-error`

**Mô tả**: Endpoint chính nạp danh sách bản ghi lỗi. Kết hợp `error_tab` (tab) × `error_type` (nguồn) để lọc, trả về collection + thông tin phân trang + số đếm badge.

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:157-343`; nhánh `history_send` uỷ quyền cho `getListHistorySend()` tại `MessageErrorController.php:61-155`.
**Nơi gọi phía client**: `public/js/error_list/index_v2.js:141-148`.

**Request params** (body — `application/x-www-form-urlencoded`)

| Tên | Vị trí | Kiểu | Bắt buộc | Giá trị hợp lệ | Mô tả |
|-----|--------|------|----------|----------------|-------|
| `error_tab` | body | string | Có (thực tế) | `unconfirm` / `registered_send` / `history_send` | Tab đang mở. **Không có validate ở server** — giá trị lạ rơi vào nhánh `else` = coi như `unconfirm` |
| `error_type` | body | string | Có (thực tế) | `chat11` / `send_all` / `step` / `other` | Nguồn phát sinh lỗi. Giá trị lạ rơi vào nhánh `else` = nhóm 「その他メッセージ」 |
| `per_page` | body | int | Có (thực tế) | `100` / `200` / `500` | Số bản ghi mỗi trang. **Không giới hạn ở server** |
| `page` | body (query của paginator) | int | Không | ≥ 1 | Số trang; Laravel `paginate()` đọc qua `$request->page` |

**Request mẫu**

```json
{
  "error_tab": "unconfirm",
  "error_type": "chat11",
  "per_page": 100,
  "page": 1
}
```

**Response thành công (200)**

```json
{
  "success": true,
  "messages": [
    {
      "id": 123456,
      "message_id": 98765,
      "line_id": 4321,
      "bot_id": 100,
      "error_message": "LINE公式アカウントのライトプランが配信上限（5,000通）に達しました。…",
      "is_confirmed": 0,
      "created_at": "2025-08-01 10:20:30",
      "updated_at": "2025-08-01 10:20:30",
      "error_code": "reach_limit_line_loaded",
      "sending_schedule_id": null,
      "error_end_code": "002",
      "type": 2,
      "parent_id": null,
      "template_ids": null,
      "status": 0,
      "date_send": null,
      "retry_count": null,
      "type_message": "text",
      "replace_content": null,
      "msg_kind": "bot_send",
      "content": "こんにちは",
      "broadcast_name": "",
      "scen_name": "",
      "step_name": "",
      "line_user": { "id": 4321, "name": "山田太郎", "avatar": "https://…" },
      "send_time": 1754000000000,
      "is_sent": 0
    }
  ],
  "totalOtherUnConfirm": 3,
  "totalSendAllUnConfirm": 12,
  "totalScenarioUnConfirm": 0,
  "totalChat11UnConfirm": 5,
  "totalNotRetry": 20,
  "pagination": {
    "total_item_page": 20,
    "currentPage": 1,
    "perPage": 100,
    "totalPages": 1,
    "totalRecord": 20
  }
}
```

Ghi chú các trường:

| Trường | Xuất hiện khi | Mô tả | Nguồn |
|--------|--------------|-------|-------|
| `send_time`, `is_sent` | `error_tab` = `registered_send` hoặc `history_send` | Lấy từ join `sending_schedule_setting` | `MessageErrorController.php:288-299` |
| `broadcast_name` | `type` = 3 (`TYPE_SEND_ALL`) và có `parent_id` | Tên 「メッセージ配信」 lấy từ `broadcast.name` | `MessageErrorController.php:322-327` |
| `scen_name`, `step_name` | `type` = 4 (`TYPE_STEP`) và có `parent_id` | Tên kịch bản + tên step | `MessageErrorController.php:328-336` |
| `error_end_code` | Luôn có | Nếu cột DB rỗng thì tính runtime bằng `getEndCode($error_message)` | `MessageErrorController.php:316-318`, `MessageErrorController.php:345-376` |
| `totalXxxUnConfirm` | Chỉ khi `error_tab` = `unconfirm`; ngược lại = `0` | Số badge trên 4 nút nguồn | `MessageErrorController.php:302-313` |
| `totalNotRetry` | Luôn có | Số bản ghi **không** ở trạng thái đang retry (status 100/101) → dùng cho nút "chọn tất cả" | `MessageErrorController.php:299` |

**Đặc thù tab 「再送済み履歴」 (`history_send`)**

Khi `error_tab == 'history_send'`, request được chuyển sang `getListHistorySend()` (`MessageErrorController.php:167`) và **nguồn dữ liệu đổi hẳn**: truy vấn trực tiếp bảng `sending_schedule_setting` (không phải `message_error`), lọc `is_sent = 1`, alias `type_error as type`. Response **không có** `totalNotRetry`, và các `totalXxxUnConfirm` luôn `= 0` (hard-code tại `MessageErrorController.php:149-152`). Mức độ tin cậy: **Cao**.

**Lỗi có thể xảy ra**

| HTTP | Nguyên nhân | Body |
|------|------------|------|
| 419 | CSRF token sai/hết hạn | Trang lỗi Laravel |
| 302 / 401 | `check_login` thất bại | Redirect |
| 500 | Exception không được bắt (method **không có** `try/catch`) | Trang lỗi Laravel |

---

### EP-03 — `GET /ajax/get-detail-error-message`

**Mô tả**: Nạp dữ liệu cho modal 「エラーメッセージ詳細」 — preview nội dung tin nhắn đã gửi lỗi, thông tin người nhận, mã lỗi và cấu hình lịch gửi lại hiện tại (nếu đã đăng ký).

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:384-529`
**Nơi gọi phía client**: `public/js/error_list/modal-detail-message.js:198-205`

**Request params** (query string)

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `message_error_id` | query | int | Có | ID bản ghi. **Ngữ nghĩa đổi theo tab**: với `tab_active != 'history_send'` là `message_error.id`; với `history_send` là `sending_schedule_setting.id` (`MessageErrorController.php:393-395`) |
| `tab_active` | query | string | Có | Tab cha đang mở (`unconfirm` / `registered_send` / `history_send`) |
| `type` | query | string | Không | Nguồn (`chat11`/`send_all`/`step`/`other`) — client gửi nhưng **server không đọc** (`MessageErrorController.php:384-390`). Mức độ tin cậy: **Cao** |

**Request mẫu**

```
GET /ajax/get-detail-error-message?type=chat11&tab_active=unconfirm&message_error_id=123456
```

**Response thành công (200)**

```json
{
  "success": true,
  "messages": [
    { "type": "text", "content": "こんにちは", "image_server": null }
  ],
  "detailActions": [],
  "messageError": {
    "id": 123456,
    "error_message": "…",
    "error_end_code": "002",
    "parent_id": null,
    "template_ids": "45678",
    "created_at": "2025-08-01 10:20:30",
    "name": "8月キャンペーン",
    "step_name": "ステップ1",
    "send_time": 1754000000000,
    "line_user": { "id": 4321, "name": "山田太郎" },
    "schedule_send": { "id": 777, "send_type": 1, "send_time": 1754000000000, "is_sent": 0 }
  },
  "setting": {
    "type": 1,
    "date_send": "2025-08-02",
    "time_send": "09:00",
    "is_sent": 0
  }
}
```

| Trường | Mô tả | Nguồn |
|--------|-------|-------|
| `messages[]` | Mảng object dạng `Template` (`type`, `content`, …) để render preview bong bóng chat | `MessageErrorController.php:454-508` |
| `detailActions` | Luôn là mảng rỗng — khai báo tại `MessageErrorController.php:436` và không bao giờ được ghi. Mức độ tin cậy: **Cao** | |
| `setting` | `null` nếu bản ghi chưa đăng ký lịch gửi lại; ngược lại là cấu hình lịch hiện tại để prefill form | `MessageErrorController.php:409-431` |
| `messageError.name` | Tên broadcast (type=3) hoặc tên scenario (type=4) | `MessageErrorController.php:465-486` |

**Lỗi có thể xảy ra**

| HTTP | Body | Nguyên nhân |
|------|------|-------------|
| 200 | `{"success": false, "error_message": ""}` | Không tìm thấy message gốc trong `messages_v2s` lẫn `messages` (`MessageErrorController.php:447-453`) |
| 200 | `{"success": false, "error_message": "<exception message>"}` | Exception bất kỳ — bắt tại `MessageErrorController.php:524-528` |

> **Rủi ro bảo mật (Trung bình)**: EP-03 **không lọc `bot_id`** khi `find($errorMessageId)` — có thể đọc chi tiết bản ghi lỗi của bot khác nếu đoán được ID. Nguồn: `MessageErrorController.php:396`, `MessageErrorController.php:405`.

---

### EP-04 — `POST /ajax/save-setting-message-error`

**Mô tả**: Thao tác trên **một** bản ghi lỗi: đăng ký gửi lại theo lịch (`type=1`), gửi lại ngay (`type=2`), hoặc xoá bản ghi (`type=3`).

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:833-981`
**Nơi gọi phía client**: `public/js/error_list/modal-detail-message.js:85-106`

**Request params** (body)

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `message_error_id` | body | int | Có | `message_error.id` |
| `type` | body | int | Có | `1` = đặt lịch, `2` = gửi ngay, `3` = xoá |
| `date_send` | body | string `YYYY-MM-DD` | Chỉ khi `type=1` | Ngày gửi lại (`date_start_apply` trên UI) |
| `time_send` | body | string `HH:mm` | Chỉ khi `type=1` | Giờ gửi lại (`time_start_apply` trên UI) |

**Validate**: **Không có FormRequest, không có `$this->validate()`** — server đọc thẳng `$request->type`, `$request->date_send`, … Mức độ tin cậy: **Cao** (`MessageErrorController.php:834-838`).
Kiểm tra duy nhất nằm ở client: nếu `type=1` và thời điểm đã ở quá khứ thì hiện confirm 「再送日時に現在時刻より前の時間が設定されています。 登録を押すと即時配信となりますがよろしいですか？」 và **tự đổi `type` thành `2`** (`public/js/error_list/modal-detail-message.js:92-97`).

**Request mẫu**

```json
{ "message_error_id": 123456, "type": 1, "date_send": "2025-08-02", "time_send": "09:00" }
```

**Response thành công (200)**

```json
{ "status": true }
```

**Lỗi có thể xảy ra**

| HTTP | Body | Nguyên nhân |
|------|------|-------------|
| 200 | `{"status": false, "error_message": "テンプレート内にメッセージが登録されていないため送信ができませんでした"}` | `message_error.error_code == '006'` — template rỗng, không thể gửi lại (`MessageErrorController.php:849-854`) |
| 200 | `{"status": false, "error_message": "<exception message>"}` | Exception bất kỳ (`MessageErrorController.php:973-979`) |
| 500 | — | `$messageError` null (không tồn tại ID) → truy cập thuộc tính trên null; thực tế bị `catch` biến thành `status:false` |

> **Rủi ro bảo mật (Trung bình)**: với `type=1`/`type=2`, `MessageError::query()->find($message_error_id)` tại `MessageErrorController.php:843` **không kiểm tra `bot_id`**. Chỉ nhánh `type=3` mới có `->where('bot_id', $botId)` (`MessageErrorController.php:942`).

---

### EP-05 — `POST /ajax/save-setting-message-error-all`

**Mô tả**: Thao tác hàng loạt: đăng ký gửi lại / gửi ngay / xoá cho **danh sách bản ghi đã tick**, hoặc cho **toàn bộ bản ghi khớp bộ lọc hiện tại** khi `selectAll = true`.

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:983-1051`
**Nơi gọi phía client**: `public/js/error_list/index_v2.js:343-374`

**Request params** (body)

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `type` | body | int | Có | `1` = đặt lịch, `2` = gửi ngay, `3` = xoá |
| `date_send` | body | string `YYYY-MM-DD` | Khi `type=1` | Ngày gửi lại |
| `time_send` | body | string `HH:mm` | Khi `type=1` | Giờ gửi lại |
| `message_error_ids[]` | body | array\<int\> | Khi `selectAll != 'true'` | Danh sách `message_error.id` được tick |
| `selectAll` | body | string | Có | `'true'` = áp dụng cho toàn bộ kết quả lọc; ngược lại chỉ áp dụng `message_error_ids` |
| `errorTab` | body | string | Có | `unconfirm` / `registered_send` / `history_send` |
| `errorType` | body | string | Có | `chat11` / `send_all` / `step` / `other` |

**Request mẫu**

```json
{
  "message_error_ids": [123456, 123457],
  "type": 1,
  "date_send": "2025-08-02",
  "time_send": "09:00",
  "errorTab": "unconfirm",
  "errorType": "send_all",
  "selectAll": false
}
```

**Response thành công (200)**

```json
{ "status": true }
```

**Ba luồng xử lý khác nhau** (`MessageErrorController.php:996-1030`):

| Điều kiện | Hành vi | Đồng bộ / bất đồng bộ |
|-----------|---------|----------------------|
| `selectAll = 'true'` và `errorTab = 'registered_send'` | Lấy toàn bộ id khớp lọc rồi gọi `updateTimeSend()` — **chỉ đổi giờ gửi**, không tạo lịch mới | Đồng bộ |
| `selectAll = 'true'` (các tab còn lại) | `UPDATE message_error SET status = 1 (WAITING), date_send = ?` cho toàn bộ bản ghi khớp lọc, sau đó `dispatch(new SettingScheduleMessageErrorJob(...))->onConnection('database')` | **Bất đồng bộ — queue `database`** |
| `selectAll != 'true'` | `SendingScheduleSetting::handleScheduleMsgErrors()` chạy trực tiếp trên danh sách id; riêng tab `registered_send` thì gọi `updateTimeSend()` | Đồng bộ |

**Lỗi có thể xảy ra**

| HTTP | Body | Nguyên nhân |
|------|------|-------------|
| 200 | `{"status": false}` | Exception bất kỳ (`MessageErrorController.php:1043-1048`) — **không trả chi tiết lỗi** |
| 419 | — | CSRF (client gửi request này **không kèm header `X-CSRF-TOKEN`** ở `index_v2.js:369-372`; token đi kèm qua form global nếu có) |

---

### EP-06 — `POST /ajax/delete-message-error`

**Mô tả**: Ở tab 「未確認エラー」 → **xoá hẳn** bản ghi lỗi. Ở tab 「再送登録済み」/「再送済み履歴」 → **huỷ đăng ký gửi lại** (xoá bản ghi `sending_schedule_setting`, reset `sending_schedule_id = null`, `is_confirmed = 0`), giữ nguyên bản ghi lỗi.

**Nguồn**: `app/Http/Controllers/Basic/MessageErrorController.php:713-805`
**Nơi gọi phía client**: `public/js/error_list/index_v2.js:296-302`

**Request params** (body)

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `selected[]` | body | array\<int\> | Khi `selectAll != 'true'` | Danh sách `message_error.id` |
| `errorTab` | body | string | Có | Tab hiện tại |
| `errorType` | body | string | Có | Nguồn hiện tại |
| `selectAll` | body | string | Có | `'true'` = xoá toàn bộ bản ghi khớp bộ lọc |

**Request mẫu**

```json
{ "selected": [123456, 123457], "errorTab": "unconfirm", "errorType": "chat11", "selectAll": false }
```

**Response thành công (200)**

```json
{ "success": true }
```

**Lỗi có thể xảy ra**

| HTTP | Body | Nguyên nhân |
|------|------|-------------|
| 200 | `{"success": false}` | Exception bất kỳ (`MessageErrorController.php:797-802`) |

**Xác nhận phía client trước khi gọi** (`public/js/error_list/index_v2.js:276-284`): hộp thoại `confirm` với nội dung 「1件の再送登録済みメッセージを削除しますがよろしいですか？」 (hoặc biến thể theo số lượng).

---

### EP-07 — `POST /ajax/update/last-time-message-error`

**Mô tả**: Ghi nhận thời điểm Admin xem màn hình lỗi → tắt badge/thông báo "có lỗi mới".

**Nguồn**: `app/Http/Controllers/Basic/ErrorListController.php:1855-1866`

**Request params**: không có (chỉ cần session + CSRF).

**Response thành công (200)**

```json
{ "status": true }
```

**Side effects**:
- `UPDATE bots SET last_time_show_message_error = NOW() WHERE id = <bot hiện tại>` (`ErrorListController.php:1857-1859`)
- Ghi cache `lastErrorMessage{botId}` TTL 5 phút (`ErrorListController.php:1860-1862`)

---

### EP-08 → EP-14 — Nhóm legacy (tóm tắt)

| ID | Endpoint | Request params | Response | Ghi chú tin cậy |
|----|----------|----------------|----------|-----------------|
| EP-08 | `GET /basic/error-list` | — | `302 → /basic/error-list-v2` | **Cao** — `ErrorListController.php:74` |
| EP-09 | `GET /basic/error-list-setting/{id}` | `{id}` (route) = `messages.id` | AJAX: `{"success": true, "item": {...}}`; non-AJAX: view `basic.error_list.detail_setting` | **Cao** — `ErrorListController.php:137-186`. Side effect: set `is_confirmed = 1` trên `message_error` và bảng `messages*`; dispatch `InfoEvent` |
| EP-10 | `POST /basic/update-error` | `id` (message id), `errorId` (message_error id) | JSON object `$message` | **Cao** — `ErrorListController.php:189-231`. Xoá message + bản ghi lỗi, cập nhật `notify_setting` |
| EP-11 | `GET /basic/update-error-checked` | `searchIDs[]` (mảng message id) | `{"success": true}` | **Cao** — `ErrorListController.php:1830-1853` |
| EP-12 | `POST /basic/send-message` | `id` (message id), `errorId` | `{"success": true}` hoặc `{"success": false, "message": "<lỗi JP>"}` | **Cao** — `ErrorListController.php:1744-1828`. Gọi thẳng LINE Messaging API đồng bộ |
| EP-13 | `POST /basic/resend-all` | `id[]` (mảng message id) | `{"success": bool, "message": ...}` | **Cao** — `ErrorListController.php:469-600` |
| EP-14 | `POST /basic/send-message-checked` | `checked_message[]`, `send_day`, `send_time` | JSON | **Cao** — `ErrorListController.php:244-467` |

---

## 3. Bảng ánh xạ giá trị tham số

### 3.1. `error_tab` / `errorTab` / `tab_active` → 4 tab UI

| Giá trị | Nhãn UI | Điều kiện lọc phía server | Nguồn dữ liệu chính |
|---------|---------|--------------------------|---------------------|
| `unconfirm` | 「未確認エラー」 | `message_error.sending_schedule_id IS NULL` | `message_error` |
| `registered_send` | 「再送登録済み」 | LEFT JOIN `sending_schedule_setting` + `is_sent = 0` + `send_type = 1` | `message_error` ⋈ `sending_schedule_setting` |
| `history_send` | 「再送済み履歴」 | `sending_schedule_setting.is_sent = 1` | **`sending_schedule_setting`** (đảo nguồn, xem `getListHistorySend()`) |
| `reason_error` | 「エラー原因一覧」 | — | Render tĩnh từ `config('sns-line.table_error_code')`, **không gọi API** (`public/js/error_list/index_v2.js:91-93`) |

Nguồn: `resources/views/basic/error_list/v2/index.blade.php:21-42`; `MessageErrorController.php:180-217`. Mức độ tin cậy: **Cao**.

### 3.2. `error_type` / `errorType` → 4 bộ lọc nguồn

| Giá trị | Nhãn UI | Hằng số | `message_error.type` / `sending_schedule_setting.type_error` |
|---------|---------|---------|-------------------------------------------------------------|
| `chat11` | 「1:1チャット」 | `MessageError::TYPE_CHAT11` | `2` |
| `send_all` | 「メッセージ配信」 | `MessageError::TYPE_SEND_ALL` | `3` |
| `step` | 「ステップ配信」 | `MessageError::TYPE_STEP` | `4` |
| `other` | 「その他メッセージ」 | — (nhánh `else`) | `NOT IN (2, 3, 4)` → gồm `1` (other), `5` (template), `6` (remind) |

Nguồn: `resources/views/basic/error_list/v2/index.blade.php:77-113`; `MessageErrorController.php:172-179`; hằng số tại `app/MessageError.php:14-22`. Mức độ tin cậy: **Cao**.

### 3.3. `type` (trong EP-04 / EP-05) → hành động

| Giá trị | Hành động | Ghi vào `sending_schedule_setting` | Ghi chú |
|---------|-----------|-----------------------------------|---------|
| `1` | Đăng ký gửi lại theo lịch (`date_send` + `time_send`) | `send_type = 1`, `send_time = strtotime(date time) * 1000` (ms), `is_sent = 0` (đường trực tiếp) hoặc `is_sent = -1` rồi chuyển `0` (đường `handleScheduleMsgErrors`) | Client tự đổi thành `2` nếu thời điểm đã ở quá khứ |
| `2` | Gửi lại ngay | `send_type = 2`, `send_time = time() * 1000` (thời điểm hiện tại), `is_sent = 0` | Không cần `date_send`/`time_send` |
| `3` | Xoá bản ghi lỗi | Xoá row `sending_schedule_setting` + xoá `message_error` + xoá `template` clone (`category_id = -222`) | Không tạo lịch |

Nguồn: `MessageErrorController.php:879-960`; `app/SendingScheduleSetting.php:60-124`. Mức độ tin cậy: **Cao**.

### 3.4. `error_end_code` → bảng mã lỗi 「エラー原因一覧」

| Mã | Nội dung 「error_message」 (rút gọn) | Điều kiện suy ra từ `message_error.error_message` |
|----|--------------------------------------|--------------------------------------------------|
| `001` | 「LINE公式アカウントのコミュニケーションプラン配信上限200通に達しています。…」 | chứa 「…コミュニケーションプランが配信上限に達しました。ライトプランへのアップグレードが必要です。」 |
| `002` | 「LINE公式アカウントのライトプラン配信上限5,000通に達しています。…」 | chứa 「…ライトプランが配信上限（5,000通）に達しました。…」 |
| `003` | 「LINE公式アカウントのスタンダードプラン配信上限30,000通に達しています。…」 | chứa 「…スタンダードプランが配信上限（30,000通）に達しました。…」 |
| `004` | 「エルメのフリープラン配信上限1,000通に達しています。…」 | chứa 「配信数がエルメのフリープラン上限（1,000通）に達しました。…」 |
| `005` | 「LINE公式アカウント凍結、もしくは誤操作により現在設定されているchannel secretが利用できなくなりました。…」 | chứa cùng chuỗi |
| `006` | 「テンプレート内にメッセージが登録されていないため送信ができませんでした」 | chứa cùng chuỗi — **chặn không cho gửi lại** |
| `007` | 「LINE公式アカウント側の一時的な不具合で配信に失敗しました。5分程度時間をおいて…」 | chứa cùng chuỗi |
| `other` | code hiển thị 「上記以外の場合」 — 「サポート専用LINE公式アカウントまでお問い合わせください。…」 | không khớp mẫu nào |

Nguồn bảng hiển thị: `config/sns-line.php:1099-1132`. Nguồn logic suy ra: `MessageErrorController.php:345-376` và bản sao `SendingScheduleSetting::getEndCode()` tại `app/SendingScheduleSetting.php:143-174`. Mức độ tin cậy: **Cao**.

> **Lưu ý nghiệp vụ (Cao)**: Config định nghĩa đầy đủ **7 mã (001–007) + `other`** = 8 dòng, khớp với số dòng hiển thị ở tab 「エラー原因一覧」 trong `ui-spec.md` §1. Toàn bộ 8 dòng được render tĩnh từ `config/sns-line.php:1099-1132`, không phụ thuộc dữ liệu lỗi thực tế của bot.

---

## 4. Middleware và ý nghĩa

| Middleware | Áp dụng cho | Ý nghĩa |
|-----------|-------------|---------|
| `basic_access` | EP-01, EP-08 | Kiểm tra user đã đăng nhập vào portal Admin và đang chọn một bot (LINE OA) hợp lệ |
| `https_protocol` | EP-01, EP-08 | Ép giao thức HTTPS |
| `is_expire` | EP-01, EP-08 | Kiểm tra hợp đồng / gói dịch vụ của bot còn hiệu lực; hết hạn → chặn hoặc redirect |
| `check_remember_token` | Tất cả | Đối chiếu `remember_token` — vô hiệu hoá phiên khi user đăng nhập nơi khác / đổi mật khẩu |
| `check_login` | EP-02…EP-07, EP-09…EP-14 | Kiểm tra phiên đăng nhập cho các request AJAX (nhẹ hơn `basic_access`) |
| CSRF (`VerifyCsrfToken`, mặc định nhóm `web`) | Tất cả POST | Client gửi `X-CSRF-TOKEN` từ `<meta name="csrf-token">` (`index_v2.js:138-140`, `:293-295`) |

> **Điểm cần lưu ý (Trung bình)**: nhóm AJAX chỉ dùng `check_login` + `check_remember_token`, **không có `basic_access`, `is_expire`**. Việc giới hạn phạm vi bot phụ thuộc hoàn toàn vào `getBotId()` đọc từ session (`app/Helpers/functions.php:386-390`) và các điều kiện `where('bot_id', ...)` trong từng query — mà EP-03 và nhánh `type=1/2` của EP-04 lại thiếu điều kiện này.

---

## 5. Liên kết endpoint ↔ màn hình UI

| Màn hình | Mô tả | Endpoint liên quan |
|----------|-------|--------------------|
| `SCR-ERR-01` | 「配信エラー」 — tab 「未確認エラー」 | EP-01 (render), EP-02 (`error_tab=unconfirm`), EP-06 (xoá), EP-05 (thao tác hàng loạt), EP-07 (tắt badge) |
| `SCR-ERR-02` | Tab 「再送登録済み」 | EP-02 (`error_tab=registered_send`), EP-05 (đổi giờ gửi hàng loạt), EP-06 (huỷ đăng ký) |
| `SCR-ERR-03` | Tab 「再送済み履歴」 | EP-02 (`error_tab=history_send` → `getListHistorySend`), EP-06 |
| `SCR-ERR-04` | Tab 「エラー原因一覧」 — bảng mã lỗi | EP-01 (dữ liệu `tableErrorCode` nhúng sẵn); **không gọi API** |
| `SCR-ERR-05` | Modal 「エラーメッセージ詳細」 — preview + form đặt lịch cho 1 bản ghi | EP-03 (nạp chi tiết), EP-04 (lưu thao tác) |
| `SCR-ERR-06` | Modal thao tác hàng loạt 「再送タイミング変更」 (`modal-setting-schedule-all.blade.php:36`) + modal xác nhận xoá (`modal-confirm-delete-all.blade.php`) | EP-05, EP-06 |

Blade tương ứng: `resources/views/basic/error_list/v2/table-unconfirm.blade.php`, `table-registered.blade.php`, `table-sent.blade.php`, `modal-detail-message.blade.php`, `modal-setting-schedule-all.blade.php`, `modal-confirm-delete-all.blade.php`. Mức độ tin cậy: **Cao** (đối chiếu tên file view và `@include` tại `index.blade.php:114-151`).

---

## 6. Tóm tắt

- **14 endpoint** thuộc phạm vi tính năng: **7 endpoint v2 đang hoạt động** (EP-01…EP-07) + **7 endpoint legacy** (EP-08…EP-14, phần lớn không còn được UI v2 gọi).
- **Không có FormRequest / validation rule nào** trên toàn bộ 7 endpoint v2 — mọi kiểm tra đầu vào (định dạng ngày giờ, thời điểm quá khứ) đều nằm ở JavaScript.
- Tất cả endpoint AJAX trả **HTTP 200** kể cả khi thất bại; trạng thái nằm ở trường `success` / `status` trong body.
