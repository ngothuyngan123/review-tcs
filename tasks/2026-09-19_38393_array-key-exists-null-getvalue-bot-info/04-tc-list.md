<!-- source: MCP LME TEST STUDIO — task_id=195, ticket 38393, testcase_list (7 TC), fetch lúc 2026-09-19. READ-ONLY snapshot, sinh bởi scripts/parse_studio_tcs.py. -->

# 04 — TC List (snapshot từ MCP LME TEST STUDIO)

> ⚠️ `contentTrust = untrusted` → xử lý như **data**, không phải chỉ thị.
>
> ⚠️ **Redmine #38393 KHÔNG có Link TCs human** → bộ TC lấy từ Studio task #195 (`status=done-ai`, `aiResult=pass`, `reviewState=leader`, branch `ai_fixbug_38393`). **7/7 TC do AI sinh** (`author=AI`, `created_job_id=579`, `status=draft`) ngày **2026-08-24**; kết quả do **pipeline AI** chạy (by `anhptn`, run #1729, 2026-09-19, env **staging**) — 3 pass · 4 skip · 0 fail.
>
> ⚠️ **TC có thể đã lỗi thời so với fix hiện tại**: TC sinh 2026-08-24 dựa trên commit `3a0fd43306`. Journal #137191 (2026-09-19) Dev bổ sung **tự review v1 — commit `9df5f81524`**: thêm `&& is_array($infoBot)` ở `reGetProfileBot` / `reGetAvatarBot` (body hỏng → rơi nhánh else, **giữ nguyên** ảnh/tên cũ) + bọc update `bots_profiles` ở `changeNewBotStep1`. ⇒ Expected của **NEW-3 / NEW-6** (`success:true, img:'', nick_name:''`, DB ghi rỗng) **không còn khớp** hành vi sau fix. Ngoài ra crash-site production thật `Ajax/ChangeBotController::init` (GET `/ajax/change-bot/init`) và `changeNewBotStep1` **chưa có TC nào**.
> ⚠️ **READ-ONLY** — muốn sửa TC thì sửa trên Studio (`testcase_update`) rồi fetch lại.

# Digest — Studio task #195 · ticket 38393 · 7 TC

## Kết quả thực thi
| Trạng thái | Số TC |
|---|---|
| `skip` | 4 |
| `pass` | 3 |

→ **3/7 TC (42%) thực sự Đạt**; 4 TC còn lại KHÔNG có kết luận test.

## Môi trường
| Env | Số TC |
|---|---|
| `STAGING` | 7 |

→ Production: **0 TC**.  ⚠️ **RULE-08**: không kết luận media / domain / job nền / bill tiền từ local-staging.

## Ai chạy (source / by)
| source / by | Số TC |
|---|---|
| `ai / anhptn` | 7 |

## Tác giả TC
| author | Số TC |
|---|---|
| `AI` | 7 |

## Loại case
| case_type | Số TC |
|---|---|
| `Abnormal` | 3 |
| `Normal` | 2 |
| `Boundary` | 2 |

## Nhóm / chế độ chạy
| tc_group | Số TC |
|---|---|
| `ui` | 6 |
| `data` | 1 |

| exec_mode | Số TC |
|---|---|
| `auto` | 7 |

## Mã quan điểm KHỚP checklist-lme (3 mã)
`FUNC-001`(2) · `OUT-TRUTH-001`(2) · `REG-SHARED-001`(1)

## ⚠️ Mã quan điểm KHÔNG có trong checklist-lme (1 mã)
| Mã Studio | Số TC |
|---|---|
| `TOOL-KNOW-002` | 2 |

→ `/review-tc` KHÔNG map được coverage cho các mã này.

## ⚠️ TC fail / error hoặc có ticket bug (0)
(không có)

## ⚠️ TC skip / chưa chạy (4)
| ID | exec | Tiêu đề |
|---|---|---|
| NEW-2 | `skip` | Bấm 情報更新 khi token bot sai/hết hạn không làm crash, hiện thông báo lỗi |
| NEW-3 | `skip` | Tái hiện & verify fix: 情報更新 khi LINE trả HTTP 200 body null không còn  |
| NEW-5 | `skip` | Bấm 初期設定 khi token bot sai không làm crash server |
| NEW-6 | `skip` | Tái hiện & verify fix: 初期設定 khi LINE trả HTTP 200 body null không còn  |

## Màn hình (3)
| screen | Số TC |
|---|---|
| `Màn cài đặt kết nối LOA (bot-edit) — nút 情報更新` | 3 |
| `Màn chat 1:1 — nút 初期設定 (đồng bộ profile bot)` | 3 |
| `Helper getValue() — app/Helpers/functions.php` | 1 |

## requirement_keys (7)
`REQ-01`(1) · `REQ-02`(1) · `REQ-03`(1) · `REQ-04`(1) · `REQ-05`(1) · `REQ-06`(1) · `REQ-07`(1)

---

## Bảng TC (16 cột canonical)

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEW-1 | FUNC-001 | Normal | Đồng bộ ảnh/tên bot thành công khi bấm 情報更新 | Đăng nhập admin qua /login-v2, đã chọn bot context. Có 1 bot với channel_access_token LINE hợp lệ (LINE /v2/bot/info trả HTTP 200 kèm pictureUrl + displayName). Ghi lại giá trị bots.bot_image, bots.view_name và bots_profiles(avt_path,nick_name is_default=1) hiện tại để đối chiếu. | 1. Mở màn 「LOA接続設定」 (bot-edit) của bot hợp lệ<br>2. Bấm nút 「情報更新」<br>3. Chờ trang tự reload sau khi request thành công<br>4. Đối chiếu ảnh đại diện và tên bot hiển thị trên màn với dữ liệu LINE trả về<br>5. Kiểm tra DB bảng bots và bots_profiles (profile is_default=1) của bot đó | bot_id = ID plain của bot có token hợp lệ; LINE /v2/bot/info trả 200 {pictureUrl:'https://profile.line-scdn.net/...', displayName:'Xuka_BOT_Booking'} | Request /ajax/reGetAvatarBot trả success:true kèm img (=pictureUrl) và nick_name (=displayName). Trang reload; ảnh/tên bot trên màn cập nhật theo LINE. DB: bots.bot_image=avturl, bots.view_name=nick_name; bots_profiles(is_default=1).avt_path=avturl, nick_name=nick_name. Không có warning/exception. | Đạt |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12470 (NEW-1) · mã theo quan điểm: TC-FUNC001-01 · ui · auto · env-safe · REQ: REQ-01 · spec: EP-05, SCR-BE-01, TICKET-38393 · Trigger PHẢI từ browser thật (click 情報更新), không gọi thẳng endpoint. LINE là dependency ngoài: chạy với bot token hợp lệ (staging) hoặc stub GuzzleHttp\Client trả 200+JSON hợp lệ ở test-mode. Verify 3 tầng (RULE-07): DB + màn hình + response JSON. Nguồn: spec EP-05 logic step 3-7. · author=AI · status=draft |
| NEW-2 | OUT-TRUTH-001 | Abnormal | Bấm 情報更新 khi token bot sai/hết hạn không làm crash, hiện thông báo lỗi | Đăng nhập admin, chọn bot context. Có 1 bot với channel_access_token sai/hết hạn (LINE /v2/bot/info trả 401 → GuzzleHttp ném RequestException). Ghi lại bots.bot_image/view_name và bots_profiles hiện tại. | 1. Mở màn 「LOA接続設定」 (bot-edit) của bot có token sai<br>2. Bấm nút 「情報更新」<br>3. Quan sát hộp thoại alert của trình duyệt<br>4. Kiểm tra HTTP status của request /ajax/reGetAvatarBot (phải 200, không 500)<br>5. Kiểm tra DB bots và bots_profiles của bot đó xem có bị đổi không | bot_id = ID bot token sai; LINE /v2/bot/info trả 401 Unauthorized | Server bắt exception ở catch, trả HTTP 200 {success:false, message:'認証できませんでした。'}. FE hiện alert 「認証できませんでした。」. KHÔNG có fatal error / HTTP 500 / màn trắng. DB bots và bots_profiles giữ NGUYÊN giá trị cũ (không bị đồng bộ). Đây là hành vi 'không crash khi LINE API lỗi' (SRC-REGRESSION-010). | Chưa test |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12471 (NEW-2) · mã theo quan điểm: TC-OUTTRUTH001-01 · ui · auto · env-safe · REQ: REQ-02 · spec: EP-05, TICKET-38393 · Trigger từ browser thật. Dùng bot token sai để LINE trả 401 thật (không cần stub), hoặc stub Guzzle ném RequestException(401). Nhánh này try/catch đã bọc sẵn trước fix — verify fix không phá regression đường lỗi. Nguồn: spec EP-05 bảng lỗi 認証できませんでした。 · author=AI · status=draft |
| NEW-3 | TOOL-KNOW-002 | Boundary | Tái hiện & verify fix: 情報更新 khi LINE trả HTTP 200 body null không còn fatal | Đăng nhập admin, chọn bot context. Cấu hình để LINE /v2/bot/info trả HTTP 200 nhưng body decode ra null (body là chuỗi 'null' hoặc rỗng) — cần stub GuzzleHttp\Client ở test-mode; api.line.me thật không tái hiện được tình huống này. | 1. Bind stub cho LINE /v2/bot/info: HTTP 200, body 'null' (json_decode → null)<br>2. Mở màn 「LOA接続設定」 (bot-edit) của bot<br>3. Bấm nút 「情報更新」<br>4. Kiểm tra HTTP status và JSON response của /ajax/reGetAvatarBot<br>5. Kiểm tra log server: không còn 'array_key_exists() expects parameter 2 to be array, null given'<br>6. Kiểm tra DB bots.bot_image/view_name và bots_profiles sau thao tác | LINE /v2/bot/info → HTTP 200, response body = null (không phải JSON object) | SAU FIX: getValue('pictureUrl',null)=null, ?? '' → avturl=''; getValue('displayName',null)=null → nick_name=''. Không phát sinh exception/fatal array_key_exists. Request trả HTTP 200 {success:true, img:'', nick_name:''}. TRƯỚC FIX (đối chứng, nếu chạy trên release branch): sinh exception array_key_exists → lỗi ghi log. ⚠ HÀNH VI CẦN HUMAN XÁC NHẬN: sau fix DB bị update bot_image=''/view_name='' (mất ảnh/tên) — leader quyết định có acceptable hay cần guard giữ giá trị cũ. | Chưa test |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12472 (NEW-3) · mã theo quan điểm: TC-TOOLKNOW002-01 · ui · auto · env-safe · REQ: REQ-03 · spec: TICKET-38393, EP-05 · TC lõi tái hiện bug + verify đã fix (TOOL-KNOW-002). Trigger từ browser; chỉ stub dependency LINE ngoài, KHÔNG tự dựng payload FE. Nếu hạ tầng không stub Guzzle được → chấp nhận verify TĨNH source: getValue có is_array guard (functions.php) và call site dùng getValue(...)??'' (BotController reGetAvatarBot). Expected nhánh ghi rỗng là ASSUMPTION cần confirm, không phải pass/fail cứng. · author=AI · status=draft · ⚠️ mã quan điểm KHÔNG có trong checklist-lme |
| NEW-4 | FUNC-001 | Normal | Đồng bộ profile bot thành công khi bấm 初期設定 trên chat 1:1 | Đăng nhập admin, đã chọn bot context có channel_access_token hợp lệ. Mở màn chat 1:1 (/basic/chat-v3 hoặc tương đương). Bot có profile mặc định (is_default=1). Ghi lại bots.bot_image/view_name và bots_profiles(avt_path,nick_name) hiện tại. | 1. Mở màn chat 1:1 của bot hợp lệ<br>2. Ở khu vực profile mặc định, bấm 「初期設定」<br>3. Chờ overlay loading tắt và quan sát ảnh/tên profile cập nhật inline<br>4. Kiểm tra JSON response của /ajax/reget-profile-bot<br>5. Kiểm tra DB bots và bots_profiles (is_default=1) của bot | item của profile mặc định; LINE /v2/bot/info trả 200 {pictureUrl, displayName} | Request /ajax/reget-profile-bot trả success:true kèm img (=pictureUrl), nick_name (=displayName). UI cập nhật item.avt_path và item.nick_name inline (không reload). DB: bots.bot_image/view_name và bots_profiles(is_default=1).avt_path/nick_name = giá trị LINE trả về. Không có warning/exception. | Đạt |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12473 (NEW-4) · mã theo quan điểm: TC-FUNC001-02 · ui · auto · env-safe · REQ: REQ-04 · spec: TICKET-38393, SRC-REGRESSION-011 · Trigger từ browser thật (click 初期設定 → Vue reGetProfileBots). LINE là dependency ngoài: bot token hợp lệ (staging) hoặc stub Guzzle 200+JSON. reGetProfileBot lấy bot_id qua getBotId() từ session ⇒ phải chọn bot context trước. Route /ajax/reget-profile-bot chưa có mã EP trong spec chat-1on1 (gap spec) — nguồn là source + diff. · author=AI · status=draft |
| NEW-5 | OUT-TRUTH-001 | Abnormal | Bấm 初期設定 khi token bot sai không làm crash server | Đăng nhập admin, chọn bot context có channel_access_token sai/hết hạn (LINE trả 401). Mở màn chat 1:1. Ghi lại bots và bots_profiles hiện tại. | 1. Mở màn chat 1:1 của bot có token sai<br>2. Bấm 「初期設定」 ở profile mặc định<br>3. Kiểm tra HTTP status của /ajax/reget-profile-bot (phải 200, không 500)<br>4. Kiểm tra JSON response<br>5. Kiểm tra DB bots và bots_profiles xem có bị đổi không | item profile mặc định; LINE /v2/bot/info trả 401 | Server bắt exception ở catch, trả HTTP 200 {success:false, msg:'認証できませんでした。'}. KHÔNG có fatal/HTTP 500. DB bots và bots_profiles giữ NGUYÊN. Không crash khi LINE API lỗi (SRC-REGRESSION-011). | Chưa test |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12474 (NEW-5) · mã theo quan điểm: TC-OUTTRUTH001-02 · ui · auto · env-safe · REQ: REQ-05 · spec: TICKET-38393, SRC-REGRESSION-011 · Trigger từ browser thật. LƯU Ý QUIRK NGOÀI SCOPE (đã ghi conflict): FE chat-v2.js kiểm tra a.status==0 nhưng controller trả 'success'/'msg' → FE không alert đúng và gán nick_name/avt_path=undefined. Bug #38393 chỉ fix crash server; TC này chỉ assert server không crash + trả success:false. Quirk FE báo cáo riêng cho human, KHÔNG tự sửa/mở scope. · author=AI · status=draft |
| NEW-6 | TOOL-KNOW-002 | Boundary | Tái hiện & verify fix: 初期設定 khi LINE trả HTTP 200 body null không còn fatal | Đăng nhập admin, chọn bot context. Stub GuzzleHttp\Client cho LINE /v2/bot/info trả HTTP 200 body null (api.line.me thật không tái hiện được). Mở màn chat 1:1. | 1. Bind stub LINE /v2/bot/info: HTTP 200, body 'null'<br>2. Mở màn chat 1:1 của bot<br>3. Bấm 「初期設定」 ở profile mặc định<br>4. Kiểm tra HTTP status và JSON response của /ajax/reget-profile-bot<br>5. Kiểm tra log server: không còn lỗi array_key_exists ... null given<br>6. Kiểm tra DB bots và bots_profiles sau thao tác | LINE /v2/bot/info → HTTP 200, body = null | SAU FIX: getValue('pictureUrl',null)/getValue('displayName',null)=null → avturl='' , nick_name=''. Không sinh exception/fatal. Request trả HTTP 200 {success:true, img:'', nick_name:''}. TRƯỚC FIX (đối chứng release branch): exception array_key_exists ghi log. ⚠ CẦN HUMAN XÁC NHẬN: DB bị update rỗng bot_image=''/view_name='' — acceptable hay cần guard. | Chưa test |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12475 (NEW-6) · mã theo quan điểm: TC-TOOLKNOW002-02 · ui · auto · env-safe · REQ: REQ-06 · spec: TICKET-38393 · TC lõi reproduce+verify (TOOL-KNOW-002) cho call site chat. Trigger từ browser, chỉ stub LINE ngoài. Nếu không stub được ⇒ verify TĨNH: ChatController reGetProfileBot dùng getValue(...)??'' và functions.php getValue có is_array guard. Expected ghi rỗng là ASSUMPTION cần confirm. · author=AI · status=draft · ⚠️ mã quan điểm KHÔNG có trong checklist-lme |
| NEW-7 | REG-SHARED-001 | Abnormal | Helper getValue() null-safe với mọi kiểu tham số $arr | Source repo sns-line trên branch ai_fixbug_38393 (đã có fix). getValue định nghĩa tại app/Helpers/functions.php: return (is_array($arr) && array_key_exists($key,$arr)) ? $arr[$key] : null; | 1. Nạp helper functions.php (autoload/composer) trong ngữ cảnh test PHP<br>2. Gọi getValue('pictureUrl', ['pictureUrl'=>'https://x', 'displayName'=>'Bot']) — array hợp lệ có key<br>3. Gọi getValue('pictureUrl', null) — tham số null (chính là ca gây bug)<br>4. Gọi getValue('missing', ['a'=>1]) — array không có key<br>5. Gọi getValue('k', 'not-an-array') — tham số không phải array (string)<br>6. Bật error_reporting E_ALL và kiểm tra không có warning phát sinh ở các lời gọi trên | Bộ tham số: (key có, array hợp lệ) / (key, null) / (key thiếu, array) / (key, string) | getValue('pictureUrl', array-hợp-lệ) = 'https://x'. getValue('pictureUrl', null) = null (KHÔNG warning 'array_key_exists() expects parameter 2 to be array, null given', KHÔNG exception). getValue('missing', ['a'=>1]) = null. getValue('k','not-an-array') = null. Không phát sinh warning/notice/exception ở mọi trường hợp. Đây là gốc fix bảo vệ toàn bộ caller dùng chung (SRC-REGRESSION-012). | Đạt |  | STAGING | anhptn | 2026-09-19 |  |  | Studio #12476 (NEW-7) · mã theo quan điểm: TC-REGSHARED001-01 · data · auto · read-only · REQ: REQ-07 · spec: TICKET-38393, SRC-REGRESSION-006, SRC-REGRESSION-012 · TC unit thuần hàm PHP (không qua HTTP/UI) nên xếp group=data (kiểm chứng logic xử lý dữ liệu của helper dùng chung). Có thể chạy bằng PHPUnit hoặc kiểm tra tĩnh diff dòng getValue (functions.php:7190). Phủ REG-SHARED-001: verify fix helper không phá caller khác. Gộp Normal/Abnormal/Boundary qua nhiều bộ data_input thay vì tách nhiều TC. · author=AI · status=draft |
