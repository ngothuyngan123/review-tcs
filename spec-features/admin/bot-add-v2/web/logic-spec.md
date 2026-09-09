# FA-042 — Logic Spec: Add Bot Router (bot-add-v2)

## Controllers & Actions

| Controller | File | Line | Action |
|-----------|------|------|--------|
| `BotController@botAddV2` | `app/Http/Controllers/Admin/BotController.php` | L.385–411 | Render trang wizard |
| `BotController@checkAuthBot` | cùng file | L.412–441 | Kiểm tra campaign sau khi tạo bot |
| `BotController@step2Validate` | cùng file | L.4435–4487 | Validate credentials với LINE API |
| `BotController@checkEnableWebhook` | cùng file | L.4973–4999 | Kiểm tra trạng thái webhook |
| `BotController@checkEnableWebhookModal` | cùng file | L.5000–5056 | Kiểm tra webhook từ modal, cập nhật is_connected |
| `BotController@step2Check` | cùng file | L.5058–5739 | Tạo bot đầy đủ (endpoint chính) |
| `BotController@step2CheckFriend` | cùng file | L.4489–5057 | Polling kiểm tra scan QR |
| `BotController@deleteBot` | cùng file | L.5741–5762 | Xóa bot tạm khi timeout |
| `BotController@step4ChooseFreePlan` | cùng file | L.5876–5935 | Chọn gói free plan |

---

## Models sử dụng

| Model | File | DB Table | Vai trò |
|-------|------|----------|---------|
| `Bots` | `app/Bots.php` | `bots` | Model chính — thông tin LINE OA bot |
| `BotSlots` | `app/BotSlots.php` | `bot_slots` | Quản lý slot bot theo hợp đồng |
| `BotContracts` | (tham chiếu từ controller) | `bot_contracts` | Hợp đồng gói dịch vụ |
| `NotifySetting` | `app/NotifySetting.php` | `notify_setting` | Cài đặt thông báo mặc định cho bot mới |
| `Landing` | `app/Landing.php` | `landing` | Landing page test cho QR scan |
| `BotLineUser` | `app/BotLineUser.php` | `bot_line_user` | Quan hệ bot ↔ LINE user |
| `BotUsers` | `app/BotUsers.php` | `user_bot` | User (admin/staff) được phép dùng bot |
| `LineUser` | (tham chiếu từ controller) | `line_user` | Người dùng LINE |
| `DetailLandingClick` | (tham chiếu từ controller) | `detail_landing_click` | Click/scan event từ QR landing |
| `BotsTutorial` | (tham chiếu từ controller) | (bảng tương ứng) | Trạng thái tutorial onboarding |
| `BotLifeCycle` | (tham chiếu từ controller) | (bảng tương ứng) | Vòng đời bot — log sự kiện |
| `PaymentDetailAff` | (tham chiếu từ controller) | (bảng tương ứng) | Chi tiết affiliate payment |
| `PaymentHistories` | (tham chiếu từ controller) | (bảng tương ứng) | Lịch sử thanh toán |
| `CampaignStatus` | (tham chiếu từ controller) | (bảng tương ứng) | Trạng thái campaign 7 ngày |
| `BotsProfiles` | (tham chiếu từ controller) | (bảng tương ứng) | Profile mặc định của bot |
| `SettingDisplayInfoFriendChat11` | (tham chiếu) | `setting_display_info_friend_chat_11` | Cài đặt hiển thị thông tin bạn bè (3 records mặc định) |
| `ActionInfoFriendDefault` | (tham chiếu) | `action_info_friend_default` | Thông tin hành động mặc định (5 records) |
| `StatusChat` | (tham chiếu) | `status_chat` | Trạng thái chat mặc định |
| `AddFriendSetting` | (tham chiếu) | `add_friend_settings` | Cài đặt thêm bạn mặc định |

**Confidence:** Cao (đọc trực tiếp từ source code)

---

## Flow Logic

### Luồng tổng thể (wizard 5 bước UI — roadStep)

```
roadStep 1: Hướng dẫn ban đầu
    └─ User đọc hướng dẫn → click "次へ進む"

roadStep 2: Hướng dẫn tạo LINE OA / Channel (không có API call)
    └─ User làm theo hướng dẫn → click "次へ進む"

roadStep 3: Nhập thông tin API (Channel ID, Secret, Client ID, Secret)
    └─ User nhập 4 fields → click "次へ進む"
       ├─ POST /admin/step2-check-validate {type: 'channel'} → validate Channel
       ├─ Nếu OK → POST /admin/step2-check-validate {type: 'client'} → validate Client
       └─ Nếu cả 2 OK → roadStep = 4

roadStep 4: Cài đặt Webhook trên LINE Developer Console
    └─ User bật webhook → click "次へ進む"
       ├─ POST /admin/check-enable-use-webhook {channel_access_token}
       ├─ Nếu webhook ON → POST /admin/step2-check (tạo bot thực sự)
       │   └─ Nếu OK → roadStep = 5, nhận urlQrCode + landingId + bot_new_id
       └─ Nếu webhook OFF → báo lỗi, yêu cầu bật lại

roadStep 5: Scan QR Code (test add friend)
    └─ Hiển thị QR code → polling mỗi 5 giây (timeout 180s)
       ├─ POST /admin/step2-check-friend {bot_id, landing_id, ...}
       ├─ Nếu success → currentStep = 4 (hoàn thành)
       └─ Nếu timeout (180s) → POST /admin/step2-delete-bot → currentStep = 5 (lỗi)

currentStep 4: Hoàn thành — hiển thị nút "エルメの設定に進む"
    └─ User click → POST /admin/check-auth-bot {bot_id}
       ├─ has_campaign = 1 → redirect /manual/tutorial?botId=<hash>
       └─ has_campaign = 0 → currentStep = 6 (未認証アカウント warning)
```

### Chi tiết flow EP-04: step2Check (tạo bot)

```
1. Validate input:
   - channel_id_new: required, unique (không có trong bots.is_deleted=0)
   - channel_secret_new: required
   - client_id_new: required
   - client_secret_new: required

2. LINE API: POST /v2/oauth/accessToken (Messaging API)
   → Lấy channel_access_token

3. validateTokenAddBot() → kiểm tra token hợp lệ

4. DB::beginTransaction()

5. INSERT bots (is_deleted=2 — trạng thái tạm):
   - admin_id, channel_id, channel_secret, channel_access_token
   - is_deleted = 2 (chưa kích hoạt, sẽ được set về 0 khi QR scan thành công)
   - expired_date = NOW()
   - flag_contract_new = 1
   - is_get_old_friend = 1
   - is_connected = 1
   - transfer_code, role_add_bot, user_add (thông tin user thêm bot)

6. INSERT notify_setting (values mặc định cho bot mới)

7. INSERT setting_display_info_friend_chat_11 (3 records):
   - LINE名 (LINE display name)
   - 友だち追加日時 (friend added date)
   - システム表示名 (system display name)

8. INSERT action_info_friend_default (5 records):
   - system_display, phone_number, email, birthday, province

9. INSERT status_chat (từ config sns-line)

10. INSERT add_friend_settings (cài đặt mặc định)

11. LINE API: PUT /v2/bot/channel/webhook/endpoint
    → Đặt webhook URL = {DOMAIN_ENDPOINT_WEBHOOK}/line/callback/add/{bot_id}
    → UPDATE bots: webhook_url, is_verify=1, expired_date_channel_access_token=NOW+28days

12. LINE API: GET /v2/bot/info
    → UPDATE bots: view_name, line_id, url_add_friend, bot_image

13. INSERT bots_profiles (profile mặc định)

14. INSERT user_bot (từ ids[] — danh sách user được phép dùng bot)

15. Nếu liff_callback_unique == null (bot mới hoàn toàn):
    a. LINE Login API: POST /v2/oauth/accessToken (client_id + client_secret)
       → Lấy tokenLineLogin
    b. LINE LIFF API: POST /liff/v1/apps (LIFF 1 — 流入アクション)
       → liffId → UPDATE bots: liff_app_id, liff_callback_unique, channel_id_line_login, channel_secret_line_login
    c. Tạo landing test trong bảng `landing` (action_type=2, code=random 6 ký tự)
    d. Generate QR code PNG (300x300) tại /images/{user_id}/{bot_id}/landing/
    e. LINE LIFF API: POST /liff/v1/apps (LIFF 2 — 各種フォーム, botPrompt=aggressive)
       → liffId2 → UPDATE bots: liff_app_id_booking, url_liff_app_callback

16. Kiểm tra campaign eligibility:
    - Nếu không có bot_slot_id và không có botIdChange:
      a. GET LINE API /v2/bot/followers/ids?limit=1000
      b. Tính has_campaign: bot.created_at + 7 ngày >= NOW ? 1 : 0
      c. UPDATE bots: has_campaign
      d. UPSERT campaign_status: expired_date_campaign = created_at + 7 ngày 23:59
    - Special case: channel_id == '2008763594' (hardcoded test account)
      → Set has_campaign theo logic tương tự nhưng không gọi LINE API

17. INSERT bots_tutorial (nếu chưa có) với 7 ngày expired

18. UPDATE bots: has_tutorial = 1

19. DB::commit()

20. Return: {success, bot_new_id, urlQrCode, landingId, type_bot_connect, bot_connect}
```

### Chi tiết flow EP-05: step2CheckFriend (polling)

```
1. Tìm DetailLandingClick.landing_id = landing_id → line_id
2. Tìm LineUser.line_id = line_id → line_user_id
3. Tìm bot_line_user WHERE bot_id = bot_id AND line_user_id = line_user_id AND is_blocked = 0

4. Nếu KHÔNG tìm thấy → return {success: false} (chưa scan)

5. Nếu TÌM THẤY:
   DB::beginTransaction()
   
   a. UPDATE bot_line_user: is_tester = 1
   b. Force delete landing, Landing::removeItemLanding()
   
   Nếu botIdChange (đổi bot):
     - Gửi tin nhắn LINE: "新規接続が完了しました！\nエルメの管理画面に戻って、次へ進んでください"
     - UPDATE bots: free_send_count++
     - updateMessageSendCount()
     - return {success: true, changeBot: true, botIdChange: X, bot_id_new: Y}
   
   Nếu KHÔNG có botIdChange (thêm bot mới):
     Case A — Có bot_slot_id (plan trả phí):
       - Tìm BotSlots → BotContracts
       - UPDATE bots: is_deleted=0, expired_date=contract.expired_date, plan_type=1
       - UPDATE bot_slots: bot_id = bot_id
       - Nếu contract_type != 'enterprise': UPDATE bot_contracts: bot_id = bot_id
       - INSERT BotLifeCycle: TYPE=START/CONNECT_WITH_PLAN
       - UPDATE payment_histories: bot_name (cho records null)
       - Xử lý affiliate (PaymentDetailAff, sendMailAddAffSuccess)
       - Firebase: subscribe topic cho bot_id
     
     Case B — Không có bot_slot_id (free plan):
       - Kiểm tra: admin đã có bot free (plan_type=2, is_deleted=0) không?
         → Nếu có → return lỗi "現在のプランは利用できない機能です"
       - UPDATE bots: plan_type=2, is_deleted=0, is_get_old_friend=1
       - UPDATE bots_tutorial: expired_date_tutorial = null
       - INSERT bot_contracts (contract_type='free', contract_bill_type='month')
       - INSERT bot_slots (admin_id, bot_id, bot_contract_id)
       - INSERT BotLifeCycle: TYPE=START/CONNECT_BOT_FREE
       - Xử lý affiliate (PaymentDetailAff, sendMailAddAffSuccess)
     
     DB::commit()
     return {success: true}
```

---

## Business Rules

### BR-01: Bot slot kết nối
- Nếu `bot_slot_id` truyền vào và slot đã có `bot_id` → redirect, không cho thêm bot vào slot đã dùng.
- **Confidence:** Cao

### BR-02: Unique channel_id
- `channel_id_new` phải unique — không được trùng với bất kỳ bot nào có `is_deleted=0`.
- Kiểm tra trong cả `step2Validate` và `step2Check`.
- **Confidence:** Cao

### BR-03: Bot tạm (is_deleted=2)
- Bot được INSERT với `is_deleted=2` ngay từ đầu.
- Chỉ được kích hoạt (`is_deleted=0`) sau khi tester scan QR thành công trong `step2CheckFriend`.
- Nếu timeout → `deleteBot()` xóa hoàn toàn bot và dữ liệu liên quan.
- **Confidence:** Cao

### BR-04: Free plan limit
- Admin chỉ được có **1 bot free plan** (`plan_type=2, is_deleted=0`).
- Rule áp dụng cho admin tạo sau ngày `2021-07-01`.
- Kiểm tra ở cả `step2Check` (L.5631–5639) và `step2CheckFriend` (L.4676–4684).
- **Confidence:** Cao

### BR-05: Campaign eligibility
- Bot được coi là đủ điều kiện campaign (`has_campaign=1`) nếu tạo trong vòng 7 ngày kể từ khi đăng ký.
- Xác định dựa trên `bots.created_at + 7 ngày` so với thời điểm kết nối bot.
- Dữ liệu lưu trong `campaign_status.expired_date_campaign`.
- **Confidence:** Cao

### BR-06: LIFF app tạo mới
- Chỉ tạo LIFF app khi `bot.liff_callback_unique == null` (bot hoàn toàn mới).
- Tạo 2 LIFF apps: 1 cho流入アクション, 1 cho各種フォーム.
- **Confidence:** Cao

### BR-07: Timeout QR scan
- Frontend polling tối đa 180 giây.
- Nếu timeout → `POST /admin/step2-delete-bot` để xóa bot tạm.
- **Confidence:** Trung bình (logic phía client trong `add_bot.js`)

### BR-08: Webhook URL format
- Webhook URL phải là: `{DOMAIN_ENDPOINT_WEBHOOK}/line/callback/add/{bot_id}`
- Nếu `DOMAIN_ENDPOINT_WEBHOOK` không set → dùng `url('line/callback/add/' . $bot_id)`.
- **Confidence:** Cao

### BR-09: Affiliate referrer
- Khi bot kết nối thành công, nếu admin có `user_introduce` hoặc `user_introduce_2` → tạo `PaymentDetailAff` record.
- Gửi email thông báo cho affiliate nếu `is_receive_notification=1`.
- **Confidence:** Cao

### BR-10: BotsTutorial record
- Tạo `BotsTutorial` record khi bot kết nối thành công (nếu chưa có).
- Expired sau 7 ngày.
- Sau khi scan QR: `expired_date_tutorial = null` (hủy tutorial timer cho free plan).
- **Confidence:** Trung bình

---

## External API Calls (LINE API)

| # | Method | URL | Mục đích | Gọi từ |
|---|--------|-----|---------|--------|
| 1 | POST | `https://api.line.me/v2/oauth/accessToken` | Lấy channel access token (Messaging API) | `step2Validate`, `step2Check` |
| 2 | PUT | `https://api.line.me/v2/bot/channel/webhook/endpoint` | Set webhook URL | `step2Validate` (tạm), `step2Check` (thật) |
| 3 | GET | `https://api.line.me/v2/bot/channel/webhook/endpoint` | Kiểm tra trạng thái webhook | `checkEnableWebhook`, `checkEnableWebhookModal`, `step2Check` |
| 4 | GET | `https://api.line.me/v2/bot/info` | Lấy thông tin bot (tên, LINE ID, avatar) | `step2Check` |
| 5 | POST | `https://api.line.me/v2/oauth/accessToken` | Lấy token LINE Login (client credentials) | `step2Check` |
| 6 | POST | `https://api.line.me/liff/v1/apps` | Tạo LIFF app (流入アクション) | `step2Check` |
| 7 | POST | `https://api.line.me/liff/v1/apps` | Tạo LIFF app (各種フォーム, botPrompt=aggressive) | `step2Check` |
| 8 | GET | `https://api.line.me/v2/bot/followers/ids?limit=1000` | Kiểm tra số bạn bè để xác định campaign | `step2Check` |

**Xử lý lỗi LINE API:**
- Tất cả calls đều được wrap trong `try/catch`.
- Lỗi LINE API → `DB::rollBack()` và trả về response JSON với `success=false`.
- Log lỗi vào Laravel log.

**Confidence:** Cao

---

## Authorization

### Middleware
- Tất cả endpoints đều yêu cầu: `check_login` + `check_remember_token`
- `check_login`: Kiểm tra session đăng nhập Laravel.
- `check_remember_token`: Kiểm tra remember token hợp lệ.

### Quyền sở hữu bot
- `deleteBot`: Chỉ xóa bot khi `bot.admin_id = Auth::id()` — ngăn xóa bot của admin khác.
- `step2Check`, `step2CheckFriend`: Lấy `userId` từ `Auth::id()` hoặc từ `bot.admin_id`.

### Không có RBAC (Role-Based Access Control) riêng
- Tính năng thêm bot dùng chung cho Admin.
- Không phân quyền theo staff role ở tầng controller.

**Confidence:** Cao

---

## Ghi chú kỹ thuật

### QR Code Generation
- Sử dụng thư viện PHP QR Code (package `Bacon\QrCode`): `Png` renderer + `Writer`.
- QR code thêm bạn: 200x200 px, encode URL `url_add_friend` từ LINE.
- QR code landing test: 300x300 px, encode URL `https://line.me/R/app/{liffId}?uLand={code}`.
- Lưu tại: `/images/{userId}/{botId}/landing/{timestamp}_{landingId}.png`.

### Default Records sau khi tạo bot
Khi bot được INSERT, 3 nhóm records mặc định được tạo ngay:
1. **`setting_display_info_friend_chat_11`** — 3 records: LINE名, 友だち追加日時, システム表示名
2. **`action_info_friend_default`** — 5 records: system_display, phone_number, email, birthday, province
3. **`status_chat`** — từ config `sns-line` (số lượng record theo config)

### Firebase Push Notification
- Khi bot được kết nối với plan trả phí → đăng ký Firebase topic cho `bot_id`.
- Dùng `UserFirebaseToken` để lấy tokens của user, sau đó `FirebaseService::subscribeTopic()`.

### Logging
- Mọi action đều gọi `addLogUserAction()` để log activity.
- Dùng `Log::info()`, `Log::debug()`, `Log::error()` xuyên suốt.
- Thông báo Chatwork khi có lỗi nghiêm trọng: `notifyChatwork()`.

**Confidence:** Cao
