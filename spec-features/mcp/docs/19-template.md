# Template Tools

> **Thay đổi lớn (refactor 2026-09-16 — P3.4 tool consolidation):**
>
> - `create_park_template` / `update_park_template` / `get_park_template_detail` đã **đổi tên** thành
>   `create_group_template` / `update_group_template` / `get_group_template_detail` (cùng container type='group').
> - `create_template_folder` / `update_template_folder` đã được **gộp** vào tool generic
>   `create_folder(type=template)` / `update_folder(type=template)` — xem [28-folder.md](28-folder.md).
> - `bulk_move_templates` đã **bị xoá** — thay bằng param `folder_id` trên từng tool `update_<type>_template`
>   (move 1 template/1 call), hoặc `update_group_template(folder_id=...)` để move cả group.

## 1. list_templates

**Description:** Liệt kê và tìm kiếm tất cả template của bot, **group theo folder (category)**. Truyền `names[]` để tra
cứu tên → id (EXACT, không phân biệt hoa thường, trim whitespace); bỏ qua `names[]` để duyệt toàn bộ. `names` không
match sẽ trả trong `not_found_names`. Lưu ý: pagination áp dụng trên **số category group**, không phải số template.

**Tool:** `list_templates`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|---------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên template EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG match. |
| page | Integer | No | Số trang (default: 1) — phân trang theo category group |
| limit | Integer | No | Số category group mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|----------------------------------------------------------------|
| categories | Json Array | Array Object Category (template group theo folder) |
| pagination | Json Object | Thông tin phân trang (theo số category group) |
| not_found_names | Array of String | (Chỉ trả khi truyền `names` và có tên không match) |

**Sub Object Category:**
| Name | Type | Description |
|---------------|------------|-------------------------------------------------------------------|
| category_id | Long | ID folder (0 = chưa phân loại) |
| category_name | String | Tên folder; `"(Uncategorized)"` cho category_id=0 |
| templates | Json Array | Array Object Template thuộc folder này |

**Sub Object Template:**
| Name | Type | Description |
|-------------|---------|----------------------------------------------------------------------------------------|
| id | Long | ID của template |
| name | String | Tên template |
| type | String | Loại template (text/form/image/video/voice/location/group) |
| type_button | Integer | (Chỉ trả khi khác null — type form) 1=Standard, 2=Color, 3=Image, 4=QuickReply |
| content | String | (Chỉ trả khi khác null) Nội dung: text truncate 200 ký tự; group = CSV id template con |
| position | Integer | Thứ tự sắp xếp |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|---------|--------------------------------------------|
| currentPage | Integer | Trang hiện tại |
| limit | Integer | Số category group mỗi trang |
| total | Integer | Tổng số category group (không phải template) |

**Sample Output:**

```json
{
  "categories": [
    {
      "category_id": 0,
      "category_name": "(Uncategorized)",
      "templates": [
        {
          "id": 101,
          "name": "Welcome Message",
          "type": "text",
          "content": "Thank you for adding us as a friend!",
          "position": 10
        },
        {
          "id": 104,
          "name": "Multi-message Set",
          "type": "group",
          "content": "101,102,103",
          "position": 3
        }
      ]
    },
    {
      "category_id": 5,
      "category_name": "Campaign Templates",
      "templates": [
        {
          "id": 103,
          "name": "Product Menu",
          "type": "form",
          "type_button": 2,
          "position": 5
        }
      ]
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

**Notes:**

- `in_park = 1` (template con đã bind vào group): bị loại khỏi kết quả — dùng `get_group_template_detail` để xem con
- `category_id < 0` (template nội bộ broadcast/scenario/event): bị loại khỏi kết quả
- Template orphan (category_id > 0 nhưng folder đã xóa/không tồn tại): bị loại khỏi kết quả
- `content` của text template được truncate tối đa 200 ký tự, thêm "..." nếu vượt quá
- `content` của group template chứa danh sách id template con phân cách bởi dấu phẩy (vd: "101,102,103")

---

## 2. get_template_detail

**Description:** Trả về FULL content (untruncated) của 1 template theo id, kèm object `data` clone-ready theo type.
Dùng TRƯỚC tool update tương ứng (`update_text_template` / `update_image_template` / `update_location_template` /
`update_form_template`) để clone state hiện tại rồi sửa field cần đổi. Hỗ trợ cả **CHILD template** (đã bind trong
group, `in_park=1`) và template riêng của scenario step (category_id=-111). Với type `group` dùng
`get_group_template_detail` thay thế.

**Tool:** `get_template_detail`

**Input:**
| Name | Type | Required | Description |
|-------------|---------|----------|-------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| template_id | Long | Yes | ID của template (số nguyên dương)   |

**Output:**
| Name | Type | Description |
|-------------|-------------|-------------------------------------------------------------------------------------------|
| id | Long | ID template |
| name | String | Tên template |
| type | String | Loại (text/form/image/video/voice/location/group) |
| type_button | Integer | (Chỉ trả khi khác null — type form) 1=Standard, 2=Color, 3=Image, 4=QuickReply |
| category_id | Long | Folder id (null với child trong group) |
| position | Integer | Thứ tự sắp xếp |
| content | String | Raw content column (full, không truncate) |
| updated_at | String | Timestamp lần sửa cuối `"yyyy-MM-dd HH:mm:ss"` — truyền lại vào `expected_updated_at` khi update |
| data | Json Object | Payload clone-ready cho text/location/form/image/video/voice; null (bị omit) cho group |

Các field null bị omit khỏi response (JsonInclude NON_NULL).

**Object `data`** là envelope 18 key chuẩn của backend: `type`, `message_button`, `message_media`, `message_stamp`,
`message_location`, `message_text`, `message_introduction`, `template_group_id`, `template_child_id`, `tmp_name`,
`action_type`, `broadcastId`, `scheduleSendId`, `conversationId`, `content`, `address`, `latitude`, `longitude` —
slot `message_*` tương ứng type được fill, các slot khác là object rỗng.

**Sample Output:**

```json
{
  "id": 101,
  "name": "Welcome Message",
  "type": "text",
  "category_id": 0,
  "position": 10,
  "content": "Thank you for adding us as a friend!",
  "updated_at": "2026-09-17 10:30:00",
  "data": {
    "type": "text",
    "message_button": {},
    "message_media": {},
    "message_stamp": {},
    "message_location": {},
    "message_text": {
      "content": "Thank you for adding us as a friend!",
      "usePreviewUrl": true,
      "keepRawUrl": false,
      "numberActionUrlRedirect": 1,
      "urlSettings": []
    },
    "message_introduction": {},
    "template_group_id": "200",
    "template_child_id": "101",
    "tmp_name": "",
    "action_type": "template",
    "broadcastId": "",
    "scheduleSendId": "",
    "conversationId": "",
    "content": "",
    "address": "",
    "latitude": "",
    "longitude": ""
  }
}
```

**Notes:**

- `data.template_group_id`: id group cha (chuỗi rỗng nếu chưa bind) — dùng làm `group_template_id` khi gọi update
- `data.message_text.urlSettings[]`: đúng format `TextUrlSetting` — copy trực tiếp vào `urlSettings[]` của
  `update_text_template`
- AI clone `data`, mutate field cần sửa, gửi lại qua tool `update_<type>_template` tương ứng (FULL REPLACE)

---

## 3. create_text_template

**Description:** Tạo TEXT message template standalone mới trong một parent group. Bắt buộc có group cha — gọi
`create_group_template(child_template_ids=[])` trước để lấy `group_template_id`. Quy tắc "new-set": mỗi yêu cầu mới
của user thì tạo group mới; chỉ tái sử dụng group cũ khi user nói rõ muốn thêm vào group đã có. Trả về
`{template_id, success}`.

**Tool:** `create_text_template`

**Input:**
| Name | Type | Required | Description |
|-------------------|------------------|----------|------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| name | String | No | Tùy chọn — template con không cần tên (bỏ trống → name rỗng như web UI; tên hiển thị nằm ở group template). Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| group_template_id | Long | Yes | Parent group id. Gọi `create_group_template(child_template_ids=[])` trước để lấy id này |
| folder_id | Long | No | Folder id (≥0; 0 = uncategorized; default 0). Child trong group không mang folder riêng — folder thuộc group cha |
| usage | String | No | Mục đích sử dụng: chỉ chấp nhận `'template'` (default). `'scenario'`/`'autoreply'`/`'broadcast'` bị từ chối kèm pointer sang tool đúng |
| data | TextTemplateData | Yes | Typed data record (xem bên dưới) |

**TextTemplateData fields:**
| Name | Type | Required | Description |
|-------------------------|-------------------------|----------|--------------------------------------------------------------------------------------------------|
| content | String | Yes | Nội dung text (1–5000 chars). Hỗ trợ token cá nhân hoá ({name}, [FRIEND_INFO_<id>]...) + LIFF URL |
| usePreviewUrl | Boolean | No | true (default) = hiện URL preview card cho cả message; false = tắt preview |
| keepRawUrl | Boolean | No | false (default) = LME auto-shorten URL + track click; true = giữ URL gốc, không rút gọn |
| urlSettings | Array of TextUrlSetting | No | Cấu hình action/expiry/OGP theo từng URL trong content (1 entry / 1 URL) |
| urlActionMode | Integer | No | Chế độ kích hoạt action URL: 1 (default) = chỉ chạy 1 lần/bạn; 0 = chạy mỗi lần click |

**Sub Object TextUrlSetting:**
| Name | Type | Required | Description |
|-----------------|--------------------|----------|------------------------------------------------------------------------------------------------------|
| url | String | Yes | URL chính xác trong content mà setting này áp dụng |
| urlId | Long | No | CHỈ khi UPDATE — id record URL redirect từ get_template_detail. Create: bỏ qua hoặc 0 |
| actionId | Long | No | Id action chain (từ create_action) — tham chiếu trực tiếp, tương đương `actions=[{actionId}]` |
| outTimeActionId | Long | No | Id action chain cho hành động sau khi URL hết hạn — tương đương `outTimeActions=[{actionId}]` |
| actions | Array of ActionRef | No | Chain chạy khi user tap URL: đúng 1 entry `{actionId}`. Inline action definition bị từ chối. Update: bỏ cả actionId+actions = giữ chain cũ; `actions: []` = xoá chain |
| expiry | TextUrlExpiry | No | Cấu hình hết hạn URL (表示期限). Null = không hết hạn |
| outTimeActions | Array of ActionRef | No | Chain chạy sau khi URL hết hạn: đúng 1 entry `{actionId}`. Chỉ có tác dụng khi có expiry |
| ogp | TextUrlOgp | No | Override OGP preview card. Null = backend tự fetch OGP từ URL |
| usePreviewUrl | Boolean | No | Bật/tắt preview riêng cho URL này (khác với usePreviewUrl cấp message) |

**Sub Object ActionRef:**
| Name | Type | Required | Description |
|----------|------|----------|--------------------------------------------------------------------------------------------------|
| actionId | Long | Yes | Id action chain đã tạo bằng create_action. Attach BY REFERENCE — update_action sau này áp dụng luôn |

**Sub Object TextUrlExpiry:**
| Name | Type | Required | Description |
|-------------|------------------|----------|----------------------------------------------------------------------------------------------|
| mode | String | Yes | `specific_date` = hết hạn ngày cố định; `n_days` = hết hạn N ngày sau khi gửi |
| expiredDate | String | No | [specific_date] Ngày hết hạn `yyyy-MM-dd`. Bắt buộc khi mode=specific_date |
| expiredTime | String | No | [specific_date] Giờ hết hạn `HH:mm` (default "00:00") |
| days | Integer | No | [n_days] Số ngày sau khi gửi (≥0; 0 = hết hạn ngay ngày gửi). Bắt buộc khi mode=n_days |
| afterDayTime | String | No | [n_days] Giờ trigger hết hạn `HH:mm` (default "00:00") |
| onExpired | TextUrlOnExpired | No | Trang hiển thị sau hết hạn — BẮT BUỘC khi có expiry (backend chỉ lưu expiry khi field này có) |

**Sub Object TextUrlOnExpired:** (đúng 1 trong 2 field)
| Name | Type | Required | Description |
|-------------|--------|----------|--------------------------------------------------------|
| message | String | No | Text hiển thị khi URL hết hạn (≤5000 chars) |
| redirectUrl | String | No | URL redirect sau hết hạn (phải bắt đầu http/https) |

**Sub Object TextUrlOgp:**
| Name | Type | Required | Description |
|-------------|--------|----------|-------------------------------------------------------------------------------------|
| title | String | No | Tiêu đề preview (≤10 chars) |
| description | String | No | Mô tả preview (≤25 chars) |
| imageUrl | String | No | Ảnh preview — full https:// URL (update: copy từ get_template_detail; create: upload qua get_file_params) |

**Sample Input:**

```json
{
  "bot_id": "AbC123",
  "name": "Sale Notice",
  "group_template_id": 200,
  "data": {
    "content": "Sale lớn tại https://example.com/lp — chỉ đến 31/12!",
    "urlSettings": [
      {
        "url": "https://example.com/lp",
        "actions": [{ "actionId": 15 }],
        "expiry": {
          "mode": "specific_date",
          "expiredDate": "2026-12-31",
          "expiredTime": "23:59",
          "onExpired": { "message": "Chương trình đã kết thúc." }
        }
      }
    ]
  }
}
```

**Output:** bọc envelope linect: `{ "result": "ok", "data": { "template_id": <Long>, "success": true }, "error": null }` — `data.template_id` là ID template con mới tạo (dùng cho update_group_template / update_*_template).

---

## 4. update_text_template

**Description:** REPLACE toàn bộ state của TEXT template (không phải diff). Gọi `get_template_detail(template_id)`
ngay trước khi update để lấy data mới nhất (tránh ghi đè sửa đổi trên web), build full payload từ response đó rồi gọi
tool. Type immutable — chỉ dùng cho template type text. `folder_id` (optional) move template sang folder khác trong
cùng 1 call.

**Tool:** `update_text_template`

**Input:**
| Name | Type | Required | Description |
|---------------------|------------------|----------|---------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| template_id | Long | Yes | ID template cần cập nhật (child template) |
| group_template_id | Long | Yes | Parent group id (lấy từ `get_template_detail` → `data.template_group_id`). Không hỗ trợ move sang group khác |
| name | String | No | Tùy chọn — bỏ trống/omit = giữ tên hiện tại. Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| usage | String | No | Chỉ chấp nhận `'template'` (default); giá trị khác bị từ chối |
| folder_id | Long | No | Move template sang folder này sau khi update nội dung (0 = uncategorized; >0 = folder kind=2 phải tồn tại). Chỉ áp dụng cho row parent-level; child trong group KHÔNG move riêng được — dùng `update_group_template(folder_id=...)`. Bỏ qua = không đổi folder |
| data | TextTemplateData | Yes | Full replacement data (clone từ get_template_detail trước khi sửa) — cấu trúc xem mục 3 |
| expected_updated_at | String | No | Giá trị `updated_at` từ get_template_detail (vd `"2026-07-15 10:30:00"`). Nếu template đã bị sửa sau đó → lỗi STALE_DATA, gọi lại get_template_detail rồi retry |

**Output:**
| Name | Type | Description |
|--------------|-------------|-----------------------------------------------------------------------------------|
| result | String | `ok` khi thành công |
| data | Json Object | Kết quả update từ backend: `{ "status": true, "data": { "id": "<template_id>" }, "msg": "", "actionType": "template" }` |
| error | String | null khi thành công |
| currentState | Json Object | State mới nhất của template sau update (cùng shape response get_template_detail) — MCP tự fetch thêm để AI luôn có data mới |
| folder_move | Json Object | (Chỉ trả khi truyền `folder_id`) kết quả move folder — envelope `{ result, data, error }` của bulk-move |

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "status": true, "data": { "id": "101" }, "msg": "", "actionType": "template" },
  "error": null,
  "currentState": {
    "id": 101,
    "name": "Sale Notice",
    "type": "text",
    "category_id": 0,
    "position": 10,
    "content": "Sale lớn tại https://example.com/lp — chỉ đến 31/12!",
    "updated_at": "2026-09-17 11:00:00",
    "data": { "...": "envelope 18 key như get_template_detail" }
  }
}
```

**Notes:**

- Với `urlSettings[]` giữ nguyên URL cũ: nếu bỏ qua `urlId`/`actionId`/`outTimeActionId`, MCP tự khôi phục từ DB theo
  `url`. Nhưng nếu AI đã set field `actions` (kể cả `actions: []`) thì coi là chủ đích — `actions: []` = xoá action
- Move nội dung + folder thất bại nửa chừng: nội dung đã update nhưng move fail → lỗi kèm hướng dẫn retry với cùng
  data + folder_id

---

## 5. create_image_template

**Description:** Tạo IMAGE message template standalone. Hỗ trợ 3 chế độ tap zone: **Case 1** không tap (bỏ qua
`layoutId` + `tapZones`); **Case 2** layout dựng sẵn (`layoutId` 1–8 + `tapZones` theo thứ tự zone +
`imgWidth`/`imgHeight`); **Case 3** toạ độ thủ công (`tapZones` kèm x/y/width/height, không có `layoutId`). Upload ảnh
qua `get_file_params` trước — dùng `download_url` làm `imgPath`, `img_width`/`img_height` cho Case 2.

**Tool:** `create_image_template`

**Input:**
| Name | Type | Required | Description |
|-------------------|-------------------|----------|--------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| name | String | No | Tùy chọn — template con không cần tên (bỏ trống → name rỗng như web UI; tên hiển thị nằm ở group template). Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| group_template_id | Long | Yes | Parent group id |
| folder_id | Long | No | Folder id (≥0; 0 = uncategorized; default 0) |
| usage | String | No | Chỉ chấp nhận `'template'` (default); giá trị khác bị từ chối |
| data | ImageTemplateData | Yes | Typed data record (xem bên dưới) |

**ImageTemplateData fields:**
| Name | Type | Required | Description |
|---------------|-----------------------|----------|--------------------------------------------------------------------------------------------------------------|
| imgPath | String | Yes | download_url từ `get_file_params`. Dùng LME-hosted URL, không dùng URL ngoài |
| thumbnailPath | String | No | Thumbnail URL. Nếu bỏ qua, dùng lại imgPath làm thumbnail |
| altText | String | No | Preview text cho LINE PC / notification bar (tối đa 400 chars) |
| layoutId | Integer | No | Case 2 — layout dựng sẵn 1–8: 1=full (1 zone), 2=chia dọc (2), 3=chia ngang (2), 4=3 dải ngang (3), 5=lưới 2×2 (4), 6=1 trên rộng + 2 dưới (3), 7=1 nửa trên + 2 dải (3), 8=lưới 2×3 (6) |
| tapZones | Array of ImageTapZone | No | Case 2: 1 entry / zone theo thứ tự layout — SỐ ZONE PHẢI ĐÚNG với layoutId. Case 3: mỗi entry kèm x/y/width/height. Bỏ qua = Case 1 |
| imgWidth | Double | No | Case 2 bắt buộc — pixel width, lấy từ `img_width` của get_file_params |
| imgHeight | Double | No | Case 2 bắt buộc — pixel height, lấy từ `img_height` của get_file_params |

**Sub Object ImageTapZone:**
| Name | Type | Required | Description |
|---------------|--------------------|----------|----------------------------------------------------------------------------------------------------|
| x | Integer | No | Case 3 bắt buộc — toạ độ X (pixel). Case 2 bỏ qua |
| y | Integer | No | Case 3 bắt buộc — toạ độ Y (pixel) |
| width | Integer | No | Case 3 bắt buộc — chiều rộng zone (>0) |
| height | Integer | No | Case 3 bắt buộc — chiều cao zone (>0) |
| url | String | No | Mở URL khi tap (http/https; cấm link Google Play / App Store) |
| phone | String | No | Số điện thoại gọi khi tap (10–12 chữ số, không gạch ngang) |
| lineId | String | No | LINE ID để add friend (bắt đầu bằng @) |
| email | String | No | Địa chỉ email mở mail client |
| inputText | String | No | Text prefill vào ô chat (≤5000 chars) |
| openInBrowser | Boolean | No | true = mở URL bằng browser ngoài; false/bỏ qua = in-LINE browser. Chỉ khi có url |
| urlExpiry | UrlExpiry | No | Cấu hình hết hạn URL. Chỉ khi có url |
| actions | Array of ActionRef | No | LME action chain chạy server-side khi tap: đúng 1 entry `{actionId}` (từ create_action). Kết hợp được với friend action. Inline definition bị từ chối |
| urlScheme | UrlSchemeData | No | LINE URL scheme — EXCLUSIVE với tất cả field action khác |
| loaProfileId | String | No | LINE ID của OA khác để mở trang profile (bắt đầu bằng @) |
| lmePage | LmePageData | No | Mở trang LME đã cấu hình (FORM/PRODUCT/EVENT/CONVERSION/SALON/LESSON) |

Quy tắc kết hợp: tối đa MỘT friend action (url/phone/lineId/email/inputText/loaProfileId/lmePage); `actions` (LME
chain) kết hợp được với friend action; `urlScheme` exclusive với tất cả. Zone không set action nào = zone chết
(decorative).

**Sub Object UrlExpiry:** (khác TextUrlExpiry — dùng cho image tap zone + form button)
| Name | Type | Required | Description |
|----------------|---------|----------|---------------------------------------------------------------------------------------|
| mode | String | No | `SPECIFIC_DATE` = hết hạn ngày cố định; `N_DAYS` = N ngày sau khi gửi |
| date | String | No | Ngày hết hạn `YYYY-MM-DD`. Bắt buộc khi mode=SPECIFIC_DATE |
| days | Integer | No | Số ngày sau khi gửi (≥0). Bắt buộc khi mode=N_DAYS |
| time | String | No | Giờ hết hạn `HH:mm` (24h). Bắt buộc cho cả 2 mode |
| expiredUrl | String | No | URL redirect sau hết hạn — đúng 1 trong expiredUrl/expiredMessage |
| expiredMessage | String | No | Text hiển thị sau hết hạn — đúng 1 trong expiredUrl/expiredMessage |

**Sub Object UrlSchemeData:**
| Name | Type | Required | Description |
|------|--------|----------|------------------------------------------------------------------------------------------------------------------|
| type | String | Yes | `SHARE_OA` (share OA, data=@lineId), `SHARE_TEXT` (share text), `CAMERA`, `CAMERA_ROLL`, `LOCATION`, `CUSTOM` (data=http(s) URL) |
| data | String | No | Bắt buộc cho SHARE_OA/SHARE_TEXT/CUSTOM; bỏ trống cho CAMERA/CAMERA_ROLL/LOCATION |

**Sub Object LmePageData:**
| Name | Type | Required | Description |
|------|--------|----------|-----------------------------------------------------------------------------------------------------------|
| type | String | Yes | `FORM` \| `PRODUCT` \| `EVENT` \| `CONVERSION` \| `SALON` \| `LESSON` |
| id | Long | Yes | ID entity đích — resolve qua list_forms / list_products / list_events / list_conversions / list_salons / list_lesson_calendars |

**Sample Input:** (Case 2 — layout 2 zone chia dọc)

```json
{
  "bot_id": "AbC123",
  "name": "Campaign Banner",
  "group_template_id": 200,
  "data": {
    "imgPath": "https://lme.example.com/uploads/img_123.jpg",
    "layoutId": 2,
    "imgWidth": 1040,
    "imgHeight": 1040,
    "tapZones": [
      { "url": "https://example.com/left" },
      { "actions": [{ "actionId": 15 }] }
    ]
  }
}
```

**Output:** bọc envelope linect: `{ "result": "ok", "data": { "template_id": <Long>, "success": true }, "error": null }` — `data.template_id` là ID template con mới tạo (dùng cho update_group_template / update_*_template).

---

## 6. update_image_template

**Description:** REPLACE toàn bộ state của IMAGE template (không phải diff). Gọi `get_template_detail` ngay trước để
lấy data mới nhất. Hỗ trợ tap zone — cùng 3 Case như create. Type immutable — chỉ dùng cho image template.
`folder_id` (optional) move folder trong cùng 1 call.

**Tool:** `update_image_template`

**Input:**
| Name | Type | Required | Description |
|---------------------|-------------------|----------|--------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| template_id | Long | Yes | ID template cần cập nhật |
| group_template_id | Long | Yes | Parent group id (từ `data.template_group_id` của get_template_detail) |
| name | String | No | Tùy chọn — bỏ trống/omit = giữ tên hiện tại. Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| usage | String | No | Chỉ chấp nhận `'template'` (default) |
| folder_id | Long | No | Move sang folder này sau update (như mục 4) |
| data | ImageTemplateData | Yes | Full replacement data — cấu trúc xem mục 5 |
| expected_updated_at | String | No | `updated_at` từ get_template_detail — phát hiện sửa đồng thời (STALE_DATA) |

**Output:** như mục 4 — envelope `{ result, data: { status, data: { id }, msg, actionType }, error }` + `currentState` (+ `folder_move` khi truyền `folder_id`).

---

## 7. create_location_template

**Description:** Tạo LOCATION message template standalone (gửi vị trí bản đồ).

**Tool:** `create_location_template`

**Input:**
| Name | Type | Required | Description |
|-------------------|----------------------|----------|-------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| name | String | No | Tùy chọn — template con không cần tên (bỏ trống → name rỗng như web UI; tên hiển thị nằm ở group template). Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| group_template_id | Long | Yes | Parent group id |
| folder_id | Long | No | Folder id (≥0; 0 = uncategorized; default 0)    |
| usage | String | No | Chỉ chấp nhận `'template'` (default)            |
| data | LocationTemplateData | Yes | Typed data record (xem bên dưới)                |

**LocationTemplateData fields:**
| Name | Type | Required | Description |
|-----------|--------|----------|------------------------------------------------|
| title | String | Yes | Tiêu đề vị trí (1–90 chars, vd: '東京駅')      |
| address | String | Yes | Địa chỉ đầy đủ (1–90 chars)                    |
| latitude | String | Yes | Vĩ độ dạng numeric string (vd: "35.6812")      |
| longitude | String | Yes | Kinh độ dạng numeric string (vd: "139.7671")   |

**Output:** bọc envelope linect: `{ "result": "ok", "data": { "template_id": <Long>, "success": true }, "error": null }` — `data.template_id` là ID template con mới tạo (dùng cho update_group_template / update_*_template).

---

## 8. update_location_template

**Description:** REPLACE toàn bộ state của LOCATION template (không phải diff). Gọi `get_template_detail` ngay trước
để lấy data mới nhất. Type immutable. `folder_id` (optional) move folder trong cùng 1 call.

**Tool:** `update_location_template`

**Input:**
| Name | Type | Required | Description |
|---------------------|----------------------|----------|--------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| template_id | Long | Yes | ID template cần cập nhật |
| group_template_id | Long | Yes | Parent group id |
| name | String | No | Tùy chọn — bỏ trống/omit = giữ tên hiện tại. Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| usage | String | No | Chỉ chấp nhận `'template'` (default)                               |
| folder_id | Long | No | Move sang folder này sau update (như mục 4)                        |
| data | LocationTemplateData | Yes | Full replacement data — cấu trúc xem mục 7                         |
| expected_updated_at | String | No | `updated_at` từ get_template_detail (STALE_DATA check)             |

**Output:** như mục 4 — envelope `{ result, data: { status, data: { id }, msg, actionType }, error }` + `currentState` (+ `folder_move` khi truyền `folder_id`).

---

## 9. create_form_template

**Description:** Tạo FORM (carousel/card có button) template standalone. Hỗ trợ 5 subtype: `standard` (button trắng) /
`color` (button màu) / `image` (nền panel là ảnh, overlay text/button) / `quick_reply` (chip text trên bàn phím) /
`quick_reply_image` (chip ảnh). Panel/button dùng ảnh thì gọi `get_file_params` trước. MCP layer tự fill ~40 backend
key mỗi button.

**Tool:** `create_form_template`

**Input:**
| Name | Type | Required | Description |
|-------------------|------------------|----------|-------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| name | String | No | Tùy chọn — template con không cần tên (bỏ trống → name rỗng như web UI; tên hiển thị nằm ở group template). Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| group_template_id | Long | Yes | Parent group id |
| folder_id | Long | No | Folder id (≥0; 0 = uncategorized; default 0)    |
| usage | String | No | Chỉ chấp nhận `'template'` (default)            |
| data | FormTemplateData | Yes | Typed data record (xem bên dưới)                |

**FormTemplateData fields:**
| Name | Type | Required | Description |
|-----------------------|--------------------|----------|-----------------------------------------------------------------------------------------------------------------------|
| subtype | String | Yes | `standard` / `color` / `image` / `quick_reply` / `quick_reply_image` (map type_button 1/2/3/4/4) |
| pcNotificationOrTitle | String | No | quick_reply: BẮT BUỘC — header text trên chips (≤5000). standard: PC preview text (≤400). color/image: message title (≤400). quick_reply_image: không dùng |
| clickLimit | String | No | `unlimited` (default) / `once_total` / `once_per_panel` / `once_per_button`. Không áp dụng cho quick_reply* (bị ép về 0) |
| exceedClickMessage | String | No | Text gửi khi user tap vượt click limit (chỉ standard/color/image) |
| exceedActions | Array of ActionRef | No | Action chain khi vượt click limit: đúng 1 entry `{actionId}` (từ create_action). Chỉ standard/color/image |
| panels | Array of FormPanel | Yes | Danh sách carousel panel (1–10). Standard 1 panel = tối đa 4 button; 2+ panel = tối đa 3 button mỗi panel |

**Sub Object FormPanel:**
| Name | Type | Required | Description |
|------------------|---------------------|----------|--------------------------------------------------------------------------------------------------------------|
| title | String | No | Tiêu đề panel. Standard/Color: ≤40 chars. IMAGE (đảo thuật ngữ UI): user nói 'ラベル/label' → field này, ≤10 chars |
| text | String | No | Body text. Standard: ≤60 chars, BẮT BUỘC để render; Color: ≤60 optional. IMAGE: user nói 'タイトル/title' → field này, ≤10 chars |
| imgPath | String | No | Ảnh panel (download_url từ get_file_params). Standard/Color: optional (all-or-none giữa các panel). IMAGE + quick_reply_image: BẮT BUỘC |
| aspectRatio | String | No | Tỉ lệ ảnh cho image/quick_reply_image (vd '1/1', '0.75/1') — tính từ img_width/img_height của get_file_params |
| typeSize | String | No | [image/color] Kích thước render: 'large' (default) / 'middle' / 'small' |
| titleBold | Boolean | No | [color] In đậm title. Default false |
| textBold | Boolean | No | [color] In đậm body. Default false (standard luôn ép true) |
| titleColor | String | No | Màu hex title. IMAGE default '#FFFFFF'; Standard/Color default '#000000' |
| titleBackground | String | No | Màu nền title. IMAGE default '#08BF5A' (phải là hex, không được rỗng); Standard/Color default '' |
| textColor | String | No | Màu hex body. IMAGE default '#FFFFFF'; Standard/Color default '#000000' |
| textBackground | String | No | Màu nền body. IMAGE default '#5B5B5B'; Standard/Color default '' |
| numberRowDisplay | Integer | No | Số button mỗi hàng. Standard: luôn 1. Color: 1 hoặc 2. Image/quick_reply: 1. Default 1 |
| buttons | Array of FormButton | Yes | Button của panel (Standard: max 4 cho 1 panel / 3 mỗi panel khi 2+; Color: max 4) |

**Sub Object FormButton:**
| Name | Type | Required | Description |
|---------------|--------------------|----------|-------------------------------------------------------------------------------------------------------------|
| label | String | No | Nhãn button (1–20 chars). BẮT BUỘC cho standard/color/quick_reply/quick_reply_image (với QR chip = text gửi khi tap). IMAGE subtype bỏ qua (ảnh là click target) |
| url | String | No | Mở URL ngoài khi tap (post_back=1). Truyền URL nguyên bản — không tự thêm query param. Trang LME-hosted → dùng `lmePage` |
| phone | String | No | Số điện thoại (10–12 chữ số, không gạch) — chế độ gọi điện (post_back=2) |
| lineId | String | No | LINE ID add friend (bắt đầu @) (post_back=3). KHÔNG được là LINE ID của chính bot |
| email | String | No | Email mở mail client (post_back=4). KHÔNG hỗ trợ trên quick_reply/quick_reply_image |
| inputText | String | No | Text prefill vào ô chat (post_back=8) |
| openInBrowser | Boolean | No | true = mở URL browser ngoài; false/bỏ qua = in-LINE browser. Chỉ khi có url |
| urlExpiry | UrlExpiry | No | Cấu hình hết hạn URL (xem mục 5). Chỉ khi có url |
| actions | Array of ActionRef | No | LME action chain server-side: đúng 1 entry `{actionId}`. Kết hợp được với mọi friend action. Inline bị từ chối |
| urlScheme | UrlSchemeData | No | LINE URL scheme (xem mục 5) — EXCLUSIVE với tất cả field action khác |
| loaProfileId | String | No | LINE ID của OA khác để mở profile (post_back=9, bắt đầu @) |
| lmePage | LmePageData | No | Mở trang LME đã cấu hình (post_back=10, xem mục 5) |
| labelColor | String | No | [color] Màu chữ button hex. Default '#FFFFFF' |
| labelBackground | String | No | [color] Màu nền button hex. Default '#08BF5A' |

Quy tắc kết hợp giống ImageTapZone: tối đa MỘT friend action; `actions` kết hợp được; `urlScheme` exclusive với tất
cả. QR chip: chỉ cần `label` là đủ (LINE tự gửi label text khi tap).

**Sample Input:**

```json
{
  "bot_id": "AbC123",
  "name": "Product Menu",
  "group_template_id": 200,
  "data": {
    "subtype": "color",
    "pcNotificationOrTitle": "Chọn sản phẩm",
    "clickLimit": "once_total",
    "panels": [
      {
        "title": "Menu",
        "text": "Bạn muốn xem gì?",
        "buttons": [
          { "label": "Xem sản phẩm", "lmePage": { "type": "PRODUCT", "id": 12 } },
          { "label": "Trang chủ", "url": "https://example.com", "actions": [{ "actionId": 15 }] }
        ]
      }
    ]
  }
}
```

**Output:** bọc envelope linect: `{ "result": "ok", "data": { "template_id": <Long>, "success": true }, "error": null }` — `data.template_id` là ID template con mới tạo (dùng cho update_group_template / update_*_template).

**Validation đặc biệt:**

- quick_reply/quick_reply_image: chỉ 1 quick_reply child mỗi group (create bị từ chối nếu group đã có)
- Không được dùng LINE ID của chính bot làm `lineId` (add-friend button)

---

## 10. update_form_template

**Description:** REPLACE toàn bộ state của FORM template (không phải diff). Gọi `get_template_detail` ngay trước để
lấy data mới nhất. Type immutable và **type_button (subtype) immutable** — đổi kiểu button phải delete + create mới.
`folder_id` (optional) move folder trong cùng 1 call.

**Tool:** `update_form_template`

**Input:**
| Name | Type | Required | Description |
|---------------------|------------------|----------|--------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| template_id | Long | Yes | ID template cần cập nhật |
| group_template_id | Long | Yes | Parent group id |
| name | String | No | Tùy chọn — bỏ trống/omit = giữ tên hiện tại. Nếu truyền: 1–20 chars sau trim, không trùng tên template top-level (case-insensitive) |
| usage | String | No | Chỉ chấp nhận `'template'` (default)                               |
| folder_id | Long | No | Move sang folder này sau update (như mục 4)                        |
| data | FormTemplateData | Yes | Full replacement data (REPLACE-ALL) — cấu trúc xem mục 9           |
| expected_updated_at | String | No | `updated_at` từ get_template_detail (STALE_DATA check)             |

**Output:** như mục 4 — envelope `{ result, data: { status, data: { id }, msg, actionType }, error }` + `currentState` (+ `folder_move` khi truyền `folder_id`).

---

## 11. create_group_template

**Description:** Tạo Group template (type='group') — container cha gom nhiều template con thành 1 đơn vị delivery
(child id lưu dạng CSV trong `template.content`). Workflow parent-first: gọi với `child_template_ids=[]` để tạo shell
→ nhận `group_template_id` → tạo con bằng `create_<type>_template(group_template_id=<id đó>)` → bind bằng
`update_group_template`.

**Tool:** `create_group_template`

**Input:**
| Name | Type | Required | Description |
|--------------------|--------|----------|------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| name | String | Yes | Tên group template (1–20 chars, unique giữa các template top-level trong bot — template con (in_park=1) không tham gia check)                                                     |
| folder_id | Long | No | Folder id (≥0; 0 = uncategorized; default 0). Folder của cả group — con nằm trong group, không có folder riêng |
| child_template_ids | Long[] | Yes | Mảng id template con (ordered). Cho phép rỗng [] để tạo shell trước. No duplicates, tất cả phải tồn tại + thuộc bot + active + KHÔNG phải type=group (không nested) |

**Output:**

```json
{
  "result": "ok",
  "data": { "park_template_id": 200, "success": true },
  "error": null,
  "group_template_id": 200
}
```

- `group_template_id`: key MCP surface ở top-level (P3.4) — dùng giá trị này; `data.park_template_id`: key legacy backend vẫn trả — cùng giá trị

**Workflow tiêu chuẩn:**

1. Gọi `create_group_template(child_template_ids=[])` → lấy `group_template_id`
2. Gọi `create_<type>_template(group_template_id=<group_id>)` cho từng child
3. Gọi `update_group_template(child_template_ids=[id1, id2, ...])` để bind children

---

## 12. update_group_template

**Description:** Update Group template — đổi tên, move folder, hoặc thêm/bớt/sắp xếp lại children. Chỉ gửi field cần
đổi — field bỏ trống **giữ nguyên** giá trị hiện tại (endpoint ghi đè cả tên / folder / danh sách con nên MCP đọc lại
group rồi gửi đủ). `child_template_ids` khi gửi là FULL list (REPLACE-ALL: con không có trong list bị loại khỏi group;
`[]` = bỏ hết con). `folder_id=0` = về uncategorized. Không có field nào để đổi → lỗi `Nothing to update`. Dùng
`template_id` từ response của từng `create_<type>_template`, không đoán.

> Đổi 2026-09-25 (review H4): trước đây `name` / `child_template_ids` bắt buộc và bỏ trống `folder_id` = chuyển cả
> group về uncategorized. Khi giữ danh sách con, MCP gửi lại đúng các con đang có (chỉ bỏ id không còn bản ghi — giống
> `children` của `get_group_template_detail`).

**Tool:** `update_group_template`

**Input:**
| Name | Type | Required | Description |
|--------------------|--------|----------|------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| group_template_id | Long | Yes | ID group template (phải tồn tại + type='group' + thuộc bot + active)         |
| name | String | No | Tên group mới (1–20 chars, unique giữa các template top-level trong bot). Bỏ trống = giữ tên hiện tại |
| folder_id | Long | No | Bỏ trống = giữ folder; `0` = uncategorized; `>0` = folder template (kind=2) — move cả group (kèm children) |
| child_template_ids | Long[] | No | Bỏ trống = giữ danh sách con hiện tại. Khi gửi: FULL ordered list id con mới (REPLACE-ALL), thứ tự trong mảng = thứ tự mới, `[]` = bỏ hết con. Tất cả phải tồn tại + thuộc bot + active + không type=group |

**Output:**

```json
{
  "success": true,
  "group_template_id": 200,
  "park_template_id": 200
}
```

---

## 13. get_group_template_detail

**Description:** Trả về detail của Group template (type='group') kèm danh sách children đã enrich (name + type).
Parse CSV child id từ `template.content` và JOIN bảng template. Dùng trước `update_group_template` để clone state hiện
tại. Read-only.

**Tool:** `get_group_template_detail`

**Input:**
| Name | Type | Required | Description |
|-------------------|--------|----------|----------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| group_template_id | Long | Yes | ID group template (phải tồn tại + type='group' + thuộc bot + active) |

**Output:**
| Name | Type | Description |
|-------------------|------------|----------------------------------------------------------------|
| id | Long | ID group template |
| name | String | Tên group |
| type | String | Luôn `"group"` |
| category_id | Long | Folder id |
| position | Integer | Thứ tự sắp xếp |
| children | Json Array | Danh sách con theo thứ tự CSV |
| missing_child_ids | Long[] | (Chỉ trả khi CSV có id không còn tồn tại — đã xóa) |

**Sub Object Child:**
| Name | Type | Description |
|----------|---------|--------------------------|
| id | Long | ID template con |
| name | String | Tên template con |
| type | String | Loại template con |
| position | Integer | Thứ tự sắp xếp |

**Sample Output:**

```json
{
  "id": 200,
  "name": "Campaign Group",
  "type": "group",
  "category_id": 0,
  "position": 5,
  "children": [
    { "id": 101, "name": "Welcome Message", "type": "text", "position": 10 },
    { "id": 102, "name": "Campaign Banner", "type": "image", "position": 8 }
  ]
}
```

---

**Notes chung cho Template CRUD:**

- Template name: tối đa 20 chars, unique trong bot (case-insensitive)
- Types được hỗ trợ qua MCP: text, form, image, location (video/voice phải dùng web UI — tool đã bị disable)
- Mọi template standalone BẮT BUỘC có parent group (`group_template_id`) — tạo shell bằng
  `create_group_template(child_template_ids=[])` trước
- **BR-01 backup guard** — mọi write op bị chặn khi bot đang backup/restore (`backup_history.status IN (0,1)`)
- **Type immutability** — không thể đổi type khi update (phải delete + create mới); form còn thêm type_button
  immutable
- **Action reference**: mọi surface action (urlSettings, tapZones.actions, buttons.actions, exceedActions) chỉ nhận
  đúng 1 entry `{actionId}` tham chiếu chain từ `create_action` — inline action definition bị từ chối. MCP verify chain
  tồn tại (fetch-and-embed) trước khi build payload
- **Optimistic lock**: truyền `expected_updated_at` (từ get_template_detail) vào update tool để phát hiện sửa đồng
  thời trên web → lỗi STALE_DATA
- **Move folder**: 1 template → param `folder_id` trên update tool (chỉ row parent-level); cả group →
  `update_group_template(folder_id=...)`
- Group template: children = CSV trong `template.content`; không cho nested groups
- `[FRIEND_INFO_<id>]` token: chỉ chèn khi user yêu cầu; MCP validate id tồn tại trong bot
  (lỗi kèm gợi ý gọi `list_friend_info_fields`)
- `[remain to=YYYY-MM-DD]` token: date phải là tương lai so với hôm nay
- Folder CRUD: xem [28-folder.md](28-folder.md) (`create_folder` / `update_folder` với `type=template`)
