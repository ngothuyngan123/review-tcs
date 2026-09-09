# FA-042 — API Spec: Add Bot Router (bot-add-v2)

## Tổng quan endpoints

| # | Method | URL | Controller@Method | Mô tả | Middleware |
|---|--------|-----|-------------------|-------|-----------|
| EP-01 | GET | `/admin/bot-add-v2` | `BotController@botAddV2` | Trang thêm bot mới (wizard) | check_login, check_remember_token |
| EP-02 | POST | `/admin/step2-check-validate` | `BotController@step2Validate` | Validate channel/client credentials với LINE API | check_login, check_remember_token |
| EP-03 | POST | `/admin/check-enable-use-webhook` | `BotController@checkEnableWebhook` | Kiểm tra trạng thái webhook LINE | check_login, check_remember_token |
| EP-04 | POST | `/admin/step2-check` | `BotController@step2Check` | Tạo bot mới, tạo LIFF app, generate QR code | check_login, check_remember_token |
| EP-05 | POST | `/admin/step2-check-friend` | `BotController@step2CheckFriend` | Polling kiểm tra bạn bè đã scan QR | check_login, check_remember_token |
| EP-06 | POST | `/admin/step2-delete-bot` | `BotController@deleteBot` | Xóa bot tạm khi timeout QR scan | check_login, check_remember_token |
| EP-07 | POST | `/admin/check-auth-bot` | `BotController@checkAuthBot` | Kiểm tra bot có campaign hay không | check_login, check_remember_token |
| EP-08 | POST | `/admin/step4-choose-free-plan` | `BotController@step4ChooseFreePlan` | Chọn gói free plan cho bot mới | check_login, check_remember_token |
| EP-09 | POST | `/ajax/check-enable-use-webhook-modal` | `BotController@checkEnableWebhookModal` | Kiểm tra webhook và cập nhật is_connected (modal) | check_login, check_remember_token |

> Nguồn: `src/web/sns-line/routes/web.php` L.184–185, L.1746–1761, L.2230  
> Controller: `src/web/sns-line/app/Http/Controllers/Admin/BotController.php`

---

## Chi tiết endpoints

### EP-01: GET /admin/bot-add-v2

**Mô tả:** Render trang wizard thêm bot mới (v2 flow). Kiểm tra điều kiện bot slot trước khi hiển thị.

**Controller:** `BotController@botAddV2` — L.385–411

**Query Parameters (optional):**

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `bot_slot_id` | integer | ID slot bot (enterprise flow) |
| `type` | integer | Loại kết nối (1 = trả phí slot, 2 = enterprise) |
| `type_change` | string | Flag thay đổi bot |

**Logic:**
1. Kiểm tra `bot_slot_id` (nếu có): Tìm `BotSlots` theo id.
2. Nếu `bot_slot_id` tồn tại và slot đã có `bot_id` → redirect về `adminIndex` (slot đã được kết nối).
3. Truyền vào view: `hash_id`, `bot_slot_id`, `type`, `typeChange`, `username`.

**Response:** Render view `admin.bots.bot_add_v3` (`bot_add_v3.blade.php`).

**Confidence:** Cao

---

### EP-02: POST /admin/step2-check-validate

**Mô tả:** Validate channel ID + channel secret (hoặc client ID + client secret) với LINE API. Được gọi 2 lần: lần 1 với `type=channel`, lần 2 với `type=client`.

**Controller:** `BotController@step2Validate` — L.4435–4487

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `channel_id` | string | Có | LINE Messaging API Channel ID |
| `channel_secret` | string | Có | LINE Messaging API Channel Secret |
| `type` | string | Có | `'channel'` hoặc `'client'` |

**Logic khi `type = 'channel'`:**
1. Kiểm tra `channel_id` không trùng với bot đang active (`is_deleted = 0`) trong DB.
2. POST LINE API `https://api.line.me/v2/oauth/accessToken` để lấy `access_token`.
3. Gọi `validateTokenAddBot()` để validate token hợp lệ.
4. PUT LINE API `https://api.line.me/v2/bot/channel/webhook/endpoint` để set webhook tạm (chuẩn bị).

**Logic khi `type = 'client'`:**
1. Chỉ POST LINE API để lấy access token (không set webhook).
2. Validate token.

**Response thành công:**
```json
{
  "success": true,
  "channel_access_token": "<token>"
}
```

**Response lỗi:**
```json
{
  "success": false,
  "msg": "<thông báo lỗi tiếng Nhật>"
}
```

**Confidence:** Cao

---

### EP-03: POST /admin/check-enable-use-webhook

**Mô tả:** Kiểm tra trạng thái webhook của LINE OA có đang bật (active) hay không.

**Controller:** `BotController@checkEnableWebhook` — L.4973–4999

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `channel_access_token` | string | Có | Channel Access Token của LINE OA |

**Logic:**
1. GET LINE API `https://api.line.me/v2/bot/channel/webhook/endpoint` với `Authorization: Bearer <token>`.
2. Nếu `response.active === false` → trả về lỗi.
3. Nếu `active === true` hoặc không có field active → trả về thành công.

**Response thành công:**
```json
{
  "success": true
}
```

**Response lỗi:**
```json
{
  "success": false,
  "flagError": 1,
  "back_step": 4,
  "msg": "Webhookをオンにして下さい。 既にオンの場合は、一度オフにしてから再度オンに変更して下さい。"
}
```

**Confidence:** Cao

---

### EP-04: POST /admin/step2-check

**Mô tả:** Endpoint chính tạo bot — tạo toàn bộ dữ liệu liên quan, đăng ký LIFF app, set webhook, generate QR code test, tạo landing page test.

**Controller:** `BotController@step2Check` — L.5058–5739

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `channel_id_new` | string | Có | LINE Messaging API Channel ID |
| `channel_secret_new` | string | Có | LINE Messaging API Channel Secret |
| `client_id_new` | string | Có | LINE Login Channel ID |
| `client_secret_new` | string | Có | LINE Login Channel Secret |
| `bot_slot_id` | integer | Không | ID slot bot (enterprise/paid plan) |
| `type` | integer | Không | Loại kết nối (1 hoặc 2) |
| `ids[]` | array | Không | Danh sách user IDs được phép dùng bot |

**Logic (tóm tắt — xem Logic Spec để chi tiết):**
1. Validate 4 fields, kiểm tra `channel_id_new` unique.
2. Lấy access token từ LINE API.
3. `DB::beginTransaction()`.
4. INSERT `bots` với `is_deleted=2` (trạng thái tạm — chưa kích hoạt).
5. INSERT các bảng mặc định: `notify_setting`, `setting_display_info_friend_chat_11` (3 records), `action_info_friend_default` (5 records), `status_chat`, `add_friend_settings`.
6. PUT LINE API webhook URL = `{domain}/line/callback/add/{bot_id}`.
7. GET LINE API `/v2/bot/info` → update `view_name`, `line_id`, `url_add_friend`, `bot_image`.
8. INSERT `bots_profiles` (profile mặc định).
9. INSERT `user_bot` (từ `ids[]`).
10. POST LINE Login API `https://api.line.me/liff/v1/apps` (2 lần) → tạo 2 LIFF apps:
    - LIFF app cho "流入アクション" (liff_app_id)
    - LIFF app cho "各種フォーム" với `botPrompt: aggressive` (liff_app_id_booking)
11. Generate QR code PNG (`/qr_image/qr_add_friend_bot_{bot_id}.png`).
12. Tạo landing page test trong bảng `landing`.
13. Cập nhật `BotSlots` nếu có `bot_slot_id`.
14. Kiểm tra campaign eligibility (GET `/v2/bot/followers/ids`), set `has_campaign`.
15. Tạo `BotsTutorial` record.
16. `DB::commit()`.

**Response thành công:**
```json
{
  "success": true,
  "bot_new_id": 123,
  "urlQrCode": "https://..../landing/xxx.png",
  "landingId": 456,
  "type_bot_connect": 0,
  "bot_connect": { /* Bots model */ }
}
```

**Response lỗi:**
```json
{
  "success": false,
  "flagError": 1,
  "msg": "<thông báo lỗi>",
  "back_step": 3
}
```

**Lưu ý:** `back_step` cho biết bước nào bị lỗi (3 = API form, 4 = Webhook).

**Confidence:** Cao

---

### EP-05: POST /admin/step2-check-friend

**Mô tả:** Polling endpoint — kiểm tra xem người dùng LINE đã scan QR code test và add friend bot chưa. Được gọi mỗi 5 giây trong tối đa 180 giây.

**Controller:** `BotController@step2CheckFriend` — L.4489–5057

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `bot_id` | integer | Có | ID bot đang tạo |
| `bot_slot_id` | integer | Không | ID slot bot |
| `type` | integer | Không | Loại kết nối |
| `botIdChange` | integer | Không | ID bot cũ (khi đổi bot) |
| `landing_id` | integer | Có | ID landing test đã tạo ở EP-04 |

**Logic:**
1. Tìm `DetailLandingClick` theo `landing_id` → lấy `line_id`.
2. Tìm `LineUser` theo `line_id`.
3. Kiểm tra `bot_line_user` có record với `bot_id` + `line_user_id` + `is_blocked=0`.
4. **Nếu chưa scan:** Response `{success: false}` — frontend tiếp tục polling.
5. **Nếu đã scan + có `botIdChange`:** (trường hợp đổi bot)
   - Gửi tin nhắn xác nhận LINE cho user.
   - Update `bot_line_user.is_tester = 1`.
   - Xóa landing test.
   - Response `{success: true, changeBot: true, botIdChange: X, bot_id_new: Y}`.
6. **Nếu đã scan + không có `botIdChange`:** (trường hợp thêm bot mới)
   - Update `bot_line_user.is_tester = 1`.
   - Xóa landing test.
   - **Nếu có `bot_slot_id`:** Kích hoạt bot với plan từ `BotContracts`, update `bot_slots.bot_id`, tạo `BotLifeCycle`, xử lý affiliate.
   - **Nếu không có `bot_slot_id`:** Kích hoạt bot với `plan_type=2` (free), tạo `BotContracts` + `BotSlots` mới.
   - Response `{success: true}`.

**Response thành công (scan xong — bot mới):**
```json
{
  "success": true
}
```

**Response thành công (đổi bot):**
```json
{
  "success": true,
  "changeBot": true,
  "botIdChange": 100,
  "bot_id_new": 123
}
```

**Response chưa scan:**
```json
{
  "success": false
}
```

**Response lỗi:**
```json
{
  "success": false,
  "msg": "現在のプランは利用できない機能です。アップグレードが必要になります。"
}
```

**Confidence:** Cao

---

### EP-06: POST /admin/step2-delete-bot

**Mô tả:** Xóa bot tạm (is_deleted=2) khi quá thời gian timeout QR scan (180 giây). Dọn dẹp toàn bộ dữ liệu liên quan.

**Controller:** `BotController@deleteBot` — L.5741–5762

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `bot_id` | integer | Có | ID bot cần xóa |

**Logic:**
1. Tìm bot với điều kiện: `id = bot_id` AND `admin_id = Auth::id()` AND `is_deleted = 2`.
2. Nếu tìm thấy:
   - Hard delete `bots` record.
   - Force delete `landing` records (+ `Landing::removeItemLanding()`).
   - Delete `setting_display_info_friend_chat_11`.
   - Delete `action_info_friend_default`.
   - Delete `status_chat`.
   - Delete `add_friend_settings`.
   - Delete `bots_profiles`.
   - Update `bot_slots.bot_id = null` (nếu có).
3. Luôn trả về success (kể cả khi không tìm thấy bot).

**Response:**
```json
{
  "success": true,
  "msg": ""
}
```

**Confidence:** Cao

---

### EP-07: POST /admin/check-auth-bot

**Mô tả:** Kiểm tra bot đã được kết nối với campaign 7 ngày hay chưa, quyết định bước tiếp theo sau khi hoàn tất QR test.

**Controller:** `BotController@checkAuthBot` — L.412–441

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `bot_id` | integer | Có | ID bot vừa tạo |

**Logic:**
1. Tìm `Bots` theo `bot_id`.
2. Kiểm tra `bot->has_campaign == 1`.
3. Nếu có campaign → `success = true` (redirect tutorial).
4. Nếu không → `success = false` (hiển thị warning 未認証アカウント).

**Response có campaign:**
```json
{
  "success": true,
  "bot_name": "Tên bot LINE"
}
```

**Response không có campaign:**
```json
{
  "success": false,
  "bot_name": "Tên bot LINE"
}
```

**Hành động phía client:**
- `success = true` → redirect `/manual/tutorial?botId=<hash_bot_id>`
- `success = false` → hiển thị step 6 (未認証アカウント warning)

**Confidence:** Cao

---

### EP-08: POST /admin/step4-choose-free-plan

**Mô tả:** Cập nhật plan type cho bot mới (dùng trong trường hợp chọn free plan sau khi đã có plan trả phí, hoặc downgrade).

**Controller:** `BotController@step4ChooseFreePlan` — L.5876–5935

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `planType` | integer | Có | Loại plan (2 = free) |
| `bot_new_id` | integer | Có | ID bot mới |

**Logic:**
1. Tìm bot theo `bot_new_id`.
2. Nếu `bot.plan_type == 1` và `planType == 2` (chuyển từ trả phí → free):
   - Tính `expired_date_free_plan`.
   - Update `bots`: `plan_type=2`, xóa `strip_card_id`, `is_deleted=0`.
3. Nếu có affiliate referrer (`user_introduce`) → tạo `PaymentDetailAff` record.

**Response:**
```json
{
  "success": true
}
```

**Confidence:** Trung bình (ít dùng trong flow chính)

---

### EP-09: POST /ajax/check-enable-use-webhook-modal

**Mô tả:** Kiểm tra webhook từ modal (khác EP-03 ở chỗ dùng `bot_id` thay vì `channel_access_token`, và cập nhật `bots.is_connected`).

**Controller:** `BotController@checkEnableWebhookModal` — L.5000–5056

**Request Body:**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `bot_id` | integer | Có | ID bot cần kiểm tra |

**Logic:**
1. Tìm `Bots` theo `bot_id`, lấy `channel_access_token`.
2. GET LINE API `https://api.line.me/v2/bot/channel/webhook/endpoint`.
3. Nếu `active === false` → update `bots.is_connected = 3`, trả về lỗi.
4. Nếu webhook URL không khớp với URL LME → update `is_connected = 2`, trả về lỗi kèm `webhook_url` đúng.
5. Nếu OK → update `is_connected = 1`, trả về success.

**Response thành công:**
```json
{
  "success": true,
  "bot_hash": "<hashid>"
}
```

**Response lỗi:**
```json
{
  "success": false,
  "flagError": 1,
  "bot_hash": "<hashid>",
  "msg": "Webhookをオンにして下さい。...",
  "webhook_url": "https://..."
}
```

**Confidence:** Cao
