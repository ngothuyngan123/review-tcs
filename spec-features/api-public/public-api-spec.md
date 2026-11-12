# FA-046 — Public API Phase 1 「API連携 / 外部連携」 — Contract Spec

> **Loại spec**: **Contract-first** (đặc tả hợp đồng do nhà cung cấp phát hành), **KHÁC** các file code-first trong feature này.
> **Nguồn**: tài liệu "Đặc tả chi tiết API Phase 1 liên kết ngoài của LME" — **bản 1.2.0 / 28-09-2026**, WSSJ phát hành cho công ty Missiona (đơn vị implement API). Bản HTML gốc: [docs/api_v1_1104.html](docs/api_v1_1104.html).
> **Thêm vào spec-features**: 2026-11-04 (human dán trực tiếp).
> **Phạm vi**: Public API `/v1/*` mà hệ thống ngoài gọi bằng API key — **đúng phần [web/api-spec.md §7](../admin/api-integration/web/api-spec.md) ghi là "KHÔNG nằm trong source đã clone"**. Đây là phần API do job Java implement (Phase 2 middleware), không phải màn quản trị key `/basic/api-integration` của FA-046 (spec code-first ở [admin/api-integration/](../admin/api-integration/)).
> **Mức tin cậy**: hợp đồng do nhà cung cấp chốt, **nhưng chưa đối chiếu được với code runtime** (code `/v1` chưa có trong source). Dùng làm **oracle expected cho TC**, vẫn phải verify thực tế khi test.

---

## 0. Quan hệ với spec code-first của FA-046

| Hạng mục | Khớp với FA-046 code-first? | Ghi chú |
|---|---|---|
| API key format `lme_live_sk_<32hex>` | ✅ Khớp | [api-spec.md §7](../admin/api-integration/web/api-spec.md) + migration #40041 ghi cùng format |
| Xác thực: `api_keys.key_lookup_hash` = HMAC-SHA256(key, `API_KEY_PEPPER`) | ✅ Khớp | Doc §2 mô tả đúng cơ chế tra key → bot + scope |
| `scope` full / read, kiểm `is_deleted` · `status` · `expires_at` (null = vĩnh viễn) | ✅ Khớp | Doc §2 |
| Idempotency-Key (bảng `api_idempotency_keys`) | ✅ Khớp | Migration `create_api_idempotency_keys_table` có sẵn; doc dùng cho `/do_action`, `/messages/push`, `/messages/template` |
| Route `/v1/*`, middleware `api_signature_auth`, job hết hạn key | ⚠️ **Chưa có code** | [api-spec.md §7](../admin/api-integration/web/api-spec.md) grep không thấy route/middleware/job → doc này là **nguồn duy nhất** cho các endpoint, chưa verify được bằng source |

➡️ **Khi review/write TC cho task Public API**: dùng file này làm chuẩn expected; những điểm "chưa có code" phải đánh dấu `Đã hỏi leader` / kiểm thực tế trên môi trường, không coi là spec đã khóa.

---

## 1. Mục đích & use case

Phase 1 định nghĩa trước các API để hệ thống bên ngoài đưa kết quả phán đoán quay lại LME: lấy danh sách/chi tiết friend, add/remove tag, cập nhật friend info, start/stop scenario, gửi message, lấy template và lấy conversation.

| Use case | Luồng | API chính | Key đối chiếu |
|---|---|---|---|
| **AI Bot tự động trả lời** | Tool AI phán đoán message của friend → gọi API LME | Gửi message, chi tiết friend, add/remove tag, start/stop scenario, cập nhật friend info | `lmessage_friend_id`, `line_friend_id` |
| **CRM/SFA** | CRM lấy danh sách friend → cập nhật tag/friend info/scenario/trạng thái chat | Danh sách + chi tiết friend, tag/scenario/field list, conversation, trạng thái chat | `lmessage_friend_id`, `line_friend_id` |
| **EC** | EC ghi nhận event (view/cart/checkout/purchase/ship/stock) → gọi API tiếp cận friend | Add/remove tag, cập nhật friend info, start/stop scenario, gửi message | `lmessage_friend_id`, `line_friend_id` |

---

## 2. Quy định chung

| Hạng mục | Quy định |
|---|---|
| **Base URL** | Staging `https://api-stg.lmes.jp` · Production `https://api.lmes.jp`. Mọi endpoint dưới prefix `/v1` (vd `https://api.lmes.jp/v1/friends`). |
| **Authentication** | Header `X-LME-API-KEY`. Key gốc `lme_live_sk_<32hex>` (#40041), cấp **theo bot**. Server tra `api_keys.key_lookup_hash` = HMAC-SHA256(key, `API_KEY_PEPPER`) → suy ra bot + quyền `scope` (full/read); kiểm `is_deleted`, `status`, `expires_at` (null = vĩnh viễn). |
| **Request format** | `Content-Type: application/json`. API lấy danh sách dùng **query**; API cập nhật dùng **JSON body**. |
| **Ngày giờ** | `YYYY-MM-DD`, `YYYY-MM-DDTHH:mm:ss+09:00`. Event/reservation/payment dùng **giờ Nhật (JST)** làm chuẩn. |
| **Paging** | `page`, `limit`. `limit` mặc định **100**, tối đa **500** record. |
| **Rate limit** | Đọc (GET): **300 request/phút** · Ghi (POST/PUT/DELETE): **60 request/phút**. Quota tính **theo bot**, cửa sổ cố định theo phút (fixed window, reset mỗi đầu phút). Mọi response `/v1` kèm header `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Vượt → **429 `rate_limited`** + header `Retry-After` (giây). Chỉ đếm request đã xác thực API key. |
| **Idempotency** | Header `Idempotency-Key` cho `/do_action`, `/messages/push`, `/messages/template` để chống chạy trùng. Giá trị do client tự đặt, tối đa **100 ký tự** (vượt → 400 `invalid_request`). |
| **Key đối chiếu friend** | `lmessage_friend_id` (ID nội bộ LME) hoặc `line_friend_id` (LINE Friend ID). |

### Response chung

```json
{
  "success": true,
  "request_id": "req_20260730_001",
  "data": {},
  "pagination": {"page": 1, "limit": 100, "total_items": 1240, "total_pages": 13, "has_next": true}
}
```

### Error chung

| HTTP | Code | Ý nghĩa | Ví dụ |
|---|---|---|---|
| 400 | `invalid_request` | Request sai format | JSON sai, thiếu field bắt buộc |
| 401 | `unauthorized` | Xác thực thất bại | Thiếu/sai API key, key hết hạn, key đã xoá |
| 403 | `forbidden` | Không có quyền trên target | Key bị disable, key `read` gọi API ghi, bot đã xoá |
| 404 | `not_found` | Target không tồn tại | Không thấy friend/tag/scenario/template/field/option/handling status — **hoặc resource thuộc bot khác** |
| 409 | `conflict` | Trùng/conflict khi cập nhật | Gửi lại cùng event ID |
| 422 | `validation_error` | Input không thỏa validation | Operation không hợp lệ với field type |
| 429 | `rate_limited` | Vượt giới hạn gọi | Vượt 300/phút (đọc) hoặc 60/phút (ghi) của bot — đợi theo `Retry-After` |

> ⚠️ **Lưu ý TC**: resource thuộc bot khác trả **404** (từ bản 1.1.0; trước đó 403/422). Key `read` gọi API ghi → **403**.

---

## 3. API index Phase 1

| Method | Path | Mục đích | Input chính |
|---|---|---|---|
| GET | `/friends` | Danh sách friend | `page`, `limit`, `line_names`, `tag_ids`, `emails`, `added_date_from/to` |
| GET | `/friends/detail` | Chi tiết friend | `lmessage_friend_id` |
| GET | `/tags` | Danh sách tag | `page`, `limit` |
| GET | `/friend-info-fields` | Danh sách friend info field | `page`, `limit` |
| GET | `/scenarios` | Danh sách scenario | `page`, `limit` |
| POST | `/messages/push` | Gửi text/media message | `friend_id`, `messages[]`, `messages[].type` |
| POST | `/messages/template` | Gửi template message | `friend_id`, `templates[]` |
| GET | `/templates` | Danh sách template | `page`, `limit` |
| GET | `/conversations` | Danh sách conversation | `page`, `limit`, `confirm_status`, `handling_status_ids`, `tag_ids`… |
| GET | `/conversations/detail` | 100 message gần nhất của 1 friend | `lmessage_friend_id` |
| GET | `/handling-statuses` | Danh sách trạng thái xử lý | — |
| POST | `/do_action` | Thực hiện hàng loạt action trên friend | `lmessage_friend_ids[]`, `actions[]`, `actions[].type` |

---

## 4. Chi tiết API Phase 1

### 4.1 `GET /friends` — Danh sách friend

Dùng khi CRM đồng bộ lần đầu hoặc cập nhật danh sách theo paging + filter cơ bản.

**Input** (tất cả ở query, đều không bắt buộc):

| Param | Type | Mô tả |
|---|---|---|
| `page` | integer | Số trang, mặc định 1 |
| `limit` | integer | Số record, mặc định 100, tối đa 500 |
| `line_names` | string \| CSV | Tìm gần đúng theo tên LINE hoặc tên quản lý (không phân biệt hoa thường). Nhiều giá trị → OR |
| `tag_ids` | integer \| CSV | Tag ID (từ `/tags`). Nhiều → OR (friend có ≥1 tag) |
| `emails` | string \| CSV | Email, khớp chính xác. Nhiều → OR |
| `added_date_from` | date | Ngày thêm bạn từ, `YYYY-MM-DD` |
| `added_date_to` | date | Ngày thêm bạn đến, `YYYY-MM-DD` |

> Filter khác loại kết hợp **AND**; nhiều giá trị trong cùng filter kết hợp **OR**.

**Output chính**: `data.total_items`, `data.total_pages`, `data.friend_detail[]` với mỗi item: `added_time` (date), `friendtype` (`old`/`new`), `line_friend_id`, `lmessage_friend_id` (integer), `line_name`, `system_name` (string|null), `email` (string|null), `phone` (string|null).

**Sample In**
```
GET /v1/friends?page=1&limit=100&line_names=Tanaka,Sato&tag_ids=101,102&added_date_from=2026-07-01&added_date_to=2026-07-30
```
**Sample Out**
```json
{
  "success": true,
  "request_id": "req_20260730_0001",
  "data": {
    "total_items": 250,
    "total_pages": 3,
    "friend_detail": [
      {"added_time": "2026-07-30", "friendtype": "new", "line_friend_id": "Uxxxxxxxx",
       "lmessage_friend_id": 12345, "line_name": "Tanaka", "system_name": "Tanaka CRM",
       "email": "customer@example.com", "phone": "09000000000"}
    ]
  }
}
```

### 4.2 `GET /friends/detail` — Chi tiết friend

Chỉ nhận `lmessage_friend_id` (**không** nhận LINE Friend ID/email/phone). 1 friend / request.

**Input**: `lmessage_friend_id` (query, integer, **Có**).

**Output**: `data.friend` gồm: `lmessage_friend_id`, `line_friend_id`, `line_name|null`, `system_name|null`, `email|null`, `phone|null`, `tags[]` (`{id, name}`), `friend_info[]` (`{id, type, name, value}`), `scenarios[]` (`{id, name, status}`).
- `friend_info[].type` ∈ `TEXT`/`POINT`/`DATE`/`SELECT`/`IMAGE`/`FILE`.
- `friend_info[].value`: POINT trả **number** (không parse được → null); DATE dạng `YYYY-MM-DD`; còn lại string. Field SELECT (kể cả built-in `-6`) **luôn trả value string (label)**, không trả option_id.
- `scenarios[].status` ∈ `following`/`completed`/`stopped`.

**Sample In**
```
GET /v1/friends/detail?lmessage_friend_id=12345
```
**Sample Out** (rút gọn)
```json
{
  "success": true, "request_id": "req_20260730_0003",
  "data": {"friend": {
    "lmessage_friend_id": 12345, "line_friend_id": "Uxxxxxxxx", "line_name": "Tanaka",
    "system_name": "Tanaka CRM", "email": "customer@example.com", "phone": "09000000000",
    "tags": [{"id": 101, "name": "cart_abandonment"}],
    "friend_info": [
      {"id": -3, "type": "TEXT", "name": "email", "value": "customer@example.com"},
      {"id": 5001, "type": "POINT", "name": "point", "value": 20}
    ],
    "scenarios": [{"id": 88, "name": "cart_abandonment_reminder", "status": "following"}]
  }}
}
```

### 4.3 `GET /tags` — Danh sách tag

**Input**: `page`, `limit` (query, không bắt buộc).
**Output**: `data.tags[]` (`{id, name, friend_count}`) + `pagination`.

**Sample In**: `GET /v1/tags?page=1&limit=100`

### 4.4 `GET /friend-info-fields` — Danh sách friend info field

Dùng resolve `field_id` trước khi cập nhật friend info qua `/do_action`.

**Input**: `page`, `limit`.
**Output**: `data.fields[]` (`{field_id, title, field_type, options[]|null}`) + `pagination`.
- `field_id`: built-in dùng **ID âm**, custom dùng **ID dương**.
- `field_type` ∈ `TEXT`/`POINT`/`DATE`/`SELECT`/`IMAGE`/`FILE`.
- `options[]`: chỉ có khi `field_type = SELECT`. Riêng built-in `field_id=-6` (都道府県名) trả **47 tỉnh cố định**.

**Built-in field (ID âm) — luôn ở đầu `page=1`, `group_id=0`:**

| field_id | Tên (JP) | field_type |
|---|---|---|
| -1 | システム表示名 (tên hệ thống/quản lý) | TEXT |
| -2 | 携帯電話 (SĐT) | TEXT |
| -3 | メールアドレス (email) | TEXT |
| -4 | 生年月日 (ngày sinh) | DATE |
| -6 | 都道府県名 (tỉnh/thành) | SELECT |
| -7 | 郵便番号 (mã bưu điện) | TEXT |
| -8 | 市区町村名 (quận/huyện/thành phố) | TEXT |
| -9 | 町名/番地 (địa chỉ/số nhà) | TEXT |
| -10 | 建物名・部屋番号 (tòa nhà/số phòng) | TEXT |

> ⚠️ Không có `field_id=-5` trong danh sách (cả doc API lẫn doc webhook đều bỏ -5).

**Field `-6` (都道府県名) — SELECT đặc biệt**: `option_id` = STT tỉnh 1-based (1=北海道 … 13=東京都 … 27=大阪府 … 47=沖縄県). Khi set qua `/do_action` gửi **`option_id`** (server resolve STT → tên tỉnh string rồi lưu; ngoài 1..47 → **404**; gửi `value` thay `option_id` → **422**). Khi đọc ra (`/friends/detail`) trả **tên tỉnh string** (label), không trả option_id.

Bảng 47 tỉnh (option_id → tên):
```
1 北海道  2 青森県  3 岩手県  4 宮城県  5 秋田県  6 山形県  7 福島県
8 茨城県  9 栃木県  10 群馬県  11 埼玉県  12 千葉県  13 東京都  14 神奈川県
15 新潟県  16 富山県  17 石川県  18 福井県  19 山梨県  20 長野県  21 岐阜県
22 静岡県  23 愛知県  24 三重県  25 滋賀県  26 京都府  27 大阪府  28 兵庫県
29 奈良県  30 和歌山県  31 鳥取県  32 島根県  33 岡山県  34 広島県  35 山口県
36 徳島県  37 香川県  38 愛媛県  39 高知県  40 福岡県  41 佐賀県  42 長崎県
43 熊本県  44 大分県  45 宮崎県  46 鹿児島県  47 沖縄県
```

### 4.5 `GET /scenarios` — Danh sách scenario

Dùng resolve `scenario_id` trước khi start/stop.
**Input**: `page`, `limit`.
**Output**: `data.scenarios[]` (`{scenario_id, name, followers_count, completed_count, dropped_count}`) + `pagination`.

### 4.6 `POST /messages/push` — Gửi message (text / media)

Thay thế `/messages/text` + `/messages/media`: mảng `messages[]` trộn text và media (`image`/`video`/`audio`), gửi theo thứ tự khai báo.

**Giới hạn**: tối đa **5** message object/request · text ≤ **5.000 ký tự**/object · URL media ≤ **2.000 ký tự**, HTTPS TLS 1.2+ · ảnh gốc JPEG/PNG ≤ **10 MB** · ảnh preview JPEG/PNG ≤ **1 MB** · video MP4 ≤ **200 MB** · audio MP3/M4A ≤ **200 MB**.

**Input (body)**:

| Param | Bắt buộc | Type | Mô tả |
|---|---|---|---|
| `friend_id` | Có | integer\|string | Friend ID nhận message |
| `id_type` | Không | string | `lmessage_friend_id` (mặc định) hoặc `line_friend_id` |
| `messages[]` | Có | array\<object\> | Trộn text + media, ≤ 5 object |
| `messages[].type` | Có | string | `text` / `image` / `video` / `audio` |
| `messages[].text` | Có điều kiện | string | Khi `type=text`, ≤ 5.000 ký tự |
| `messages[].url` | Có điều kiện | string | URL media khi `type=image/video/audio`, HTTPS TLS 1.2+, ≤ 2.000 ký tự |
| `messages[].preview_url` | Không | string | Ảnh preview cho image/video (JPEG/PNG ≤ 1 MB); bỏ trống → dùng URL gốc làm preview |
| `messages[].duration` | Có điều kiện | integer | Độ dài audio (ms); bắt buộc khi `type=audio` |
| `mark_confirmed` | Không | boolean | Đánh dấu chat đã xác nhận sau khi gửi |
| `Idempotency-Key` | Khuyến nghị | string (header) | Chống xử lý trùng khi retry |

**Output**: `success`, `request_id`.

**Sample In**
```
POST /v1/messages/push
Idempotency-Key: push-12345-20260730

{
  "friend_id": 12345, "id_type": "lmessage_friend_id",
  "messages": [
    {"type": "text", "text": "Cảm ơn bạn đã liên hệ..."},
    {"type": "image", "url": "https://example.com/guide.jpg", "preview_url": "https://example.com/guide_preview.jpg"},
    {"type": "video", "url": "https://example.com/intro.mp4", "preview_url": "https://example.com/intro_preview.jpg"},
    {"type": "audio", "url": "https://example.com/guide.mp3", "duration": 60000}
  ],
  "mark_confirmed": true
}
```

### 4.7 `POST /messages/template` — Gửi template message

Gửi tối đa **5** template/request theo `templates[]`.

**Input (body)**: `friend_id` (Có), `id_type` (Không, mặc định `lmessage_friend_id`), `templates[]` (Có, ≤ 5 item), `templates[].template_id` (Có, integer — từ `/templates`), `mark_confirmed` (Không), `Idempotency-Key` (header, khuyến nghị).
**Output**: `success`, `request_id`.

### 4.8 `GET /templates` — Danh sách template

Resolve `template_id` trước khi gửi template.
**Input**: `page`, `limit`.
**Output**: `data.templates[]` (`{template_id, name}`) + `pagination`.

### 4.9 `GET /conversations` — Danh sách conversation

Chat 1:1 của bot, sắp xếp **favorite lên đầu**, sau đó theo tin mới nhất.

**Input (query, không bắt buộc)**:

| Param | Type | Mô tả |
|---|---|---|
| `page`, `limit` | integer | Paging |
| `confirm_status` | integer | `0` = đã đọc (確認済み), `1` = chưa đọc (未確認) |
| `handling_status_ids` | integer \| CSV | Trạng thái xử lý, nhiều ID → OR (từ `/handling-statuses`) |
| `handling_status_names` | string \| CSV | Theo tên trạng thái xử lý, khớp chính xác (không phân biệt hoa thường); gộp OR với `handling_status_ids` |
| `line_names` | string \| CSV | Tên LINE hoặc tên quản lý, gần đúng; nhiều → OR |
| `tag_ids` | integer \| CSV | Tag ID (từ `/tags`), gộp với `tag_names` |
| `tag_names` | string \| CSV | Tên tag, khớp chính xác |
| `tag_mode` | string | `or` (mặc định, ≥1 tag) hoặc `and` (đủ tất cả tag) |
| `display_status` | string | `display` (mặc định), `hidden`, `all` |

> Filter khác loại → AND; nhiều giá trị trong 1 filter → OR (tag theo `tag_mode`). Tên tách bằng dấu phẩy — tên chứa dấu phẩy thì dùng filter theo ID.

**Output**: `data.conversations[]` với `lmessage_friend_id`, `line_friend_id`, `line_name`, `system_name|null`, `last_message`, `last_message_date` (datetime), `confirm_status` (`read`/`unread`), `handling_status` (`{id,name}`|null) + `pagination`.

### 4.10 `GET /conversations/detail` — 100 message gần nhất của 1 friend

**Giới hạn**: tối đa **100** message gần nhất. Phạm vi lịch sử theo contract bot: **free = 180 ngày**, **trả phí = 365 ngày (12 tháng)** gần nhất; cũ hơn không trả về.

**Input**: `lmessage_friend_id` (query, integer, Có).
**Output**: `data.lmessage_friend_id`, `data.messages[]`, `data.handling_status` (object|null), `data.display_status` (`display`/`hidden`), `data.block_status` (`blocked`/`block`/`normal`), `data.favorite` (`yes`/`no`).
- `messages[].sender` ∈ `friend` / `LINE_OA`.
- `messages[].message_type`: text, image, video, file, sticker, template, pdf, booking, scenario, event, broadcast, action…
- `messages[].data` chuẩn hoá theo type: text + media (image/video/audio/file) → **string**; template/scenario/event/broadcast/action → **array** `[{type, content}]`; pdf/booking/scenario-event → **object**. Field nội bộ (image_server, thumbnail_path, from…) đã loại.

### 4.11 `GET /handling-statuses` — Danh sách trạng thái xử lý

Lấy `status ID` để đồng bộ trạng thái xử lý chat với CRM; ID này dùng cho action `handling_status` của `/do_action`.
**Input**: không có param.
**Output**: `data[]` (`{id, name}`).

### 4.12 `POST /do_action` — Thực hiện hàng loạt action trên friend

Thay thế các API đơn lẻ: `/update-tag`, `/friend-info-field-update`, `/operate-scenarios`, `/change-handling-statuses`, `/change-block-statuses`, `/change-favorite-statuses`.

**Cách hoạt động**: gửi 1 mảng friend (`lmessage_friend_ids[]`) + 1 mảng action (`actions[]`). Mỗi action áp cho **tất cả** friend, chạy **tuần tự** theo thứ tự khai báo.

**Bảng phân loại action**:

| `type` | Mục đích | `action` hợp lệ | Param riêng |
|---|---|---|---|
| `tag` | Add/remove tag | `add`, `remove` | `tag_ids[]` |
| `friend_info` | Cập nhật friend info field | `set`, `clear`, `today`, `point_replace`, `point_plus`, `point_minus`, `point_clear` | `field_id`, `value`, `option_id` |
| `scenario` | Start/stop/tiếp tục scenario | `start`, `stop`, `resume` | `scenario_id`, `start_from` |
| `handling_status` | Đổi trạng thái xử lý chat | `attach`, `detach` | `handling_status_id` |
| `block` | Đổi block / hiển thị trong chat 1:1 | `block`, `unblock`, `show`, `hide` | — |
| `favorite` | Bật/tắt favorite | `add`, `remove` | — |
| `confirm_status` | Đổi đã đọc/chưa đọc (確認/未確認) của conversation — **khác** `handling_status` | `confirm`, `unconfirm` | — |

**Input (body)**:

| Param | Bắt buộc | Type | Áp dụng | Mô tả |
|---|---|---|---|---|
| `lmessage_friend_ids[]` | Có | array\<integer\> | Chung | Đề xuất **tối đa 100** friend/request |
| `actions[]` | Có | array\<object\> | Chung | Thực hiện tuần tự. Đề xuất **tối đa 10** action/request |
| `actions[].type` | Có | string | Chung | 1 trong 7 type ở bảng trên |
| `actions[].action` | Có | string | Chung | Giá trị hợp lệ theo từng `type` |
| `actions[].tag_ids[]` | Có điều kiện | array\<integer\> | tag | Tag ID cần add/remove (từ `/tags`) |
| `actions[].field_id` | Có điều kiện | integer | friend_info | Field ID (built-in âm, custom dương; từ `/friend-info-fields`) |
| `actions[].value` | Có điều kiện | string | friend_info | Khi `set`/`point_replace`/`point_plus`/`point_minus`. TEXT=text, DATE=`YYYY-MM-DD`, POINT=số, IMAGE/FILE=string (URL/path). **Không cần** khi `clear`/`today`/`point_clear` |
| `actions[].option_id` | Có điều kiện | integer | friend_info | Khi `set` field SELECT (từ `options[]`). Field `-6`: option_id = STT 1..47 (ngoài → 404; gửi `value` thay option_id → 422) |
| `actions[].scenario_id` | Có điều kiện | integer | scenario | Khi `start`/`resume`; **không cần** khi `stop` (từ `/scenarios`) |
| `actions[].start_from` | Có điều kiện | integer | scenario | Số ngày bắt đầu, **chỉ** khi `resume` (vd 3 = từ ngày thứ 3). `start` luôn chạy từ đầu |
| `actions[].handling_status_id` | Có điều kiện | integer | handling_status | Khi `attach`; **không cần** khi `detach` (từ `/handling-statuses`) |
| `Idempotency-Key` | Khuyến nghị | string (header) | Chung | Chống xử lý trùng khi retry |

**Output**: `success`, `request_id`.

**Sample In**
```
POST /v1/do_action
Idempotency-Key: do-action-20260730-001

{
  "lmessage_friend_ids": [12345, 12346],
  "actions": [
    {"type": "tag", "action": "add", "tag_ids": [101]},
    {"type": "friend_info", "action": "point_plus", "field_id": 5001, "value": "10"},
    {"type": "scenario", "action": "start", "scenario_id": 88},
    {"type": "handling_status", "action": "attach", "handling_status_id": 12},
    {"type": "block", "action": "hide"},
    {"type": "favorite", "action": "add"},
    {"type": "confirm_status", "action": "confirm"}
  ]
}
```

---

## 5. Lịch sử cập nhật (từ doc gốc)

| Bản | Ngày | Thay đổi chính |
|---|---|---|
| **1.2.0** | 28/09/2026 | Bổ sung đủ built-in field ID âm (-1..-4, -6..-10) ở `/friend-info-fields`; field `-6` (都道府県名) SELECT 47 tỉnh, `option_id` = STT 1-based; `/do_action` `friend_info.set` field `-6` nhận `option_id` (ngoài 1..47 → 404; gửi `value` → 422); đọc ra là tên tỉnh string |
| **1.1.0** | 21/09/2026 | Resource bot khác → 404 (trước 403/422); "compliant status" → "handling status"; đổi path `GET /conversations` (message gần nhất) → `GET /conversations/detail`, thêm `GET /conversations` (danh sách); `/do_action` thêm type `confirm_status`; bỏ tiền tố `filters.` ở query; thống nhất `line_name`/`system_name` |
| **1.0.0** | 10/09/2026 | Bản đầu tiên |

> Authentication signature, retry spec và data type cuối cùng "sẽ xác định ở spec chi tiết" (footer doc). Base URL + rate limit đã chốt ở §2.
