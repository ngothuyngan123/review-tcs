# [SC-003] Friend Filter — 絞り込みモーダル

**Mã**: SC-003  
**Phiên bản spec**: 1.0  
**Ngày tạo**: 2026-05-14  
**Validation**: ĐẠT — 93% coverage  
**Confidence tổng thể**: Cao (xác nhận trực tiếp từ source code + database schema)

---

## 1. Tổng quan

### Mô tả

SC-003 là **modal popup lọc bạn bè** (LINE friends) dùng chung cho hàng chục tính năng trong hệ thống LME. Người dùng thiết lập một hoặc nhiều điều kiện lọc, hệ thống tính số bạn bè thỏa điều kiện và áp dụng kết quả cho tính năng đang sử dụng.

### Thông tin kỹ thuật

| Thuộc tính | Giá trị |
|-----------|---------|
| HTML ID | `#newFunnelModal` |
| Tên JP (V1) | 「絞り込み設定」 |
| Tên JP (V2) | 「絞り込み」 |
| Controller | `Basic\FilterController` (1101 dòng) |
| Model chính | `FilterV2` (1075 dòng) → bảng `filters_v2` |
| Engine lọc | `Conversation::advanceFilterPost()` |
| File V1 | `resources/views/basic/filter/modal_filter.blade.php` |
| File V2 | `resources/views/layout/modal_filter_v2.blade.php` (285KB) |

### Ai sử dụng

- **Admin** và **Staff** (với quyền phù hợp)
- Xuất hiện trong **61+ màn hình** khác nhau của hệ thống
- Áp dụng cho mọi tính năng cần chọn đối tượng bạn bè

### Hai phiên bản song song

| Phiên bản | Đặc điểm | Trạng thái |
|-----------|---------|-----------|
| **V1** (「絞り込み設定」) | Modal Bootstrap chuẩn; AND-only; 6 filter types; lưu vào bảng `filters` | Cũ — vẫn dùng cho Broadcast cũ và Friendlist |
| **V2** (「絞り込み」) | Full-screen 1100px; AND + OR logic; 11 filter types; lưu vào `filters_v2` | Mới — dùng cho hầu hết tính năng từ V2 trở đi |

---

## 2. Sử dụng bởi

| Nhóm tính năng | Context | Version | Variant/Ghi chú |
|----------------|---------|---------|-----------------|
| Broadcast (「メッセージ配信」) | Chọn đối tượng nhận tin nhắn hàng loạt | V1 và V2 | V1: broadcast variant (width 900px, có preview số người); V2: `broadcast`, `broadcast-v2` parent_type |
| Friendlist (「友だちリスト」) | Lọc hiển thị danh sách bạn bè | V1 và V2 | V1: friendlist variant (submit form); V2: standard |
| Step/Scenario (「ステップ」) | Chọn điều kiện trigger bước scenario | V2 | parent_type: `step_message` — KHÔNG tính filterNumber |
| Auto-reply (「自動応答」) | Giới hạn đối tượng nhận auto-reply | V2 | |
| Rich Menu (「リッチメニュー」) | Giới hạn đối tượng hiển thị rich menu | V2 | 2 parent_type đặc biệt: `setting_rich_menu`, `filter-rich-menu-toggle` |
| Form (「フォーム」) | Giới hạn đối tượng nhận form | V2 | |
| Tag (「タグ」) | Lọc theo tag | V2 | |
| Conversion (「コンバージョン」) | Lọc theo conversion | V2 | |
| Calendar/Booking (「予約管理」) | Giới hạn đối tượng đặt lịch | V2 | 5 parent_type calendar riêng biệt |
| Action Schedule | Lịch tự động theo bộ lọc | V2 | parent_type: `action_schedule` — không cần `parent_id` |
| Cross Analysis (「クロス分析」) | Phân tích chéo dùng filter V2 | V2 | Dùng `saveFilterCrossAnalysis` — luôn INSERT mới |
| CSV Management | Xuất CSV với filter | V2 | |
| Chat (「チャット」) | Lọc cuộc trò chuyện | V2 | |
| Events/Sales | Lọc đối tượng cho sự kiện, bán hàng | V2 | |
| Filter Manager | Lưu bộ lọc để tái sử dụng | V2 | KHÔNG tính filterNumber, KHÔNG trả `line_user_ids` |

---

## 3. UI Specification

### 3.1 V1 — Modal Filter Cơ bản (「絞り込み設定」)

#### Layout tổng thể

```
+------------------------------------------+
|  [×] 絞り込み設定                          |
+------------------------------------------+
| 「すべて満たす」必要がある条件 (and条件)      |
| ┌────────────────────────────────────┐   |
| │ 名前         │ [text input]        │   |
| │              │ □LINE登録名 □本名 □システム │
| ├──────────────┼────────────────────┤   |
| │ タグ         │ [multi-select]      │   |
| │              │ [dropdown option]   │   |
| ├──────────────┼────────────────────┤   |
| │ 友だち登録日  │ [日付選択] から [日付選択]│
| ├──────────────┼────────────────────┤   |
| │ ステップ     │ [scenario select]   │   |
| │              │ [condition select]  │   |
| ├──────────────┼────────────────────┤   |
| │ コンバージョン│ [multi-select]      │   |
| │              │ [dropdown option]   │   |
| ├──────────────┼────────────────────┤   |
| │ メッセージ確認│ □未確認 □確認済み    │   |
| │ 状況         │                    │   |
| └────────────────────────────────────┘   |
|        [この条件で決定]                    |
+------------------------------------------+
```

- Loại modal: Bootstrap, `modal-lg` (~900px)
- Logic: **Chỉ AND** — tất cả điều kiện phải thỏa mãn đồng thời
- Footer: nút 「この条件で決定」gọi `saveFilter()`

#### 6 Filter Types (V1)

##### Filter 1: 「名前」(Tên bạn bè)

| Thuộc tính | Giá trị |
|-----------|---------|
| Input type | Text input + checkboxes |
| Form field | `modal_name_filter` (text), `modal_name_filter_type[]` (checkbox array) |
| Help text | 「スペースで区切るといずれかにあてはまる友だちを絞り込めます」|
| Logic | Nhiều từ khóa cách nhau bằng dấu cách = OR giữa các từ |

**Checkbox options** (có thể chọn nhiều):

| Label | Value | DB column |
|-------|-------|-----------|
| LINE登録名 | 1 | `line_user.name` |
| 本名 | 2 | `line_user.real_name` |
| システム表示名 | 3 | `line_user.view_name` |

##### Filter 2: 「タグ」(Tag)

| Thuộc tính | Giá trị |
|-----------|---------|
| Input type | Multi-select (tag picker) + dropdown option |
| Form field | `modal_add_tag_ids` (hidden, comma-separated IDs), `modal_tag_filter_option` (select) |
| UI | Click vào input area → dropdown mở; trái: danh sách category; phải: tags trong category |

**Tag picker options** (`modal_tag_filter_option`):

| Label | Value |
|-------|-------|
| 選択したタグのいずれか1つ以上を含む人 | 0 |
| 選択したタグをすべて含む人 | 1 |
| 選択したタグを1つ以上含む人を除外 | 2 |
| 選択したタグを全て含む人を除外 | 3 |

##### Filter 3: 「友だち登録日」(Ngày đăng ký bạn bè)

| Thuộc tính | Giá trị |
|-----------|---------|
| Input type | Date range picker (2 inputs) |
| Form field | `modal_from_filter` (từ ngày), `modal_to_filter` (đến ngày) |
| Connector | 「から」(từ ... đến) |
| DB column | `bot_line_user.followed_at` |

##### Filter 4: 「ステップ」(Scenario/Step)

| Thuộc tính | Giá trị |
|-----------|---------|
| Form field | `modal_scenario_filter` (select scenario ID), `modal_scenario_filter_option` (select), `modal_scenario_start_day_filter` (number, khi option=2) |

**Condition options** (`modal_scenario_filter_option`):

| Label | Value |
|-------|-------|
| を購読中の人 | 0 |
| を現在購読していない人 | 1 |
| の？日目まで送信済みの人 | 2 |
| を読了した人 | 3 |
| を読了していない人 | 4 |

##### Filter 5: 「コンバージョン」(Conversion)

| Thuộc tính | Giá trị |
|-----------|---------|
| Input type | Multi-select (conversion picker) + dropdown option |
| Form field | `modal_add_conversion_ids` (hidden, comma-separated IDs), `modal_conversion_filter_option` (select) |

**Options**: Tương tự Tag (4 options OR/AND/OR NOT/AND NOT, value 0-3)

##### Filter 6: 「メッセージ確認状況」/ 「対応マーク」

**Trong base và broadcast** (`メッセージ確認状況`):

| Label | Value UI | `conversation.status_last_message` |
|-------|----------|------------------------------------|
| 未確認 | 0 | 0 |
| 確認済み | 1 | 1 |

Form field: `modal_mark_filter[]` (checkbox array)

> **Lưu ý quan trọng**: Values 2, 3, 5, 7, 8, 9 tồn tại trong code nhưng đã bị comment out (lịch sử). Values 4 và 6 bị skip hoàn toàn.

**Trong friendlist**: Dynamic từ Vue data `marks` (form field `status_search`)

#### Điểm khác biệt giữa V1 Contexts

| Context | Sự khác biệt |
|---------|-------------|
| **Base** (`basic/filter`) | Footer: 「この条件で決定」→ `saveFilter()` |
| **Broadcast** (`basic/broadcast`) | Width 900px cố định; thêm preview section với 「X人へ送信されます」màu đỏ; nút 「決定」 ở footer |
| **Friendlist** (`basic/friendlist/layout`) | Thêm hidden form fields; submit về route `friendlistHome`; 「対応マーク」thay cho 「メッセージ確認状況」|

#### Filter Control Widget (V1)

File: `resources/views/basic/filter/filter_control.blade.php`

Wrapper hiển thị ngoài trang:

```
反応対象者の絞り込み [任意]
[絞り込み設定]          ← nút mở modal #newFunnelModal
┌─────────────────────────────┐
│ 条件: {preview_content}    [設定解除]│
└─────────────────────────────┘
→ {X}人が対象              ← click để xem danh sách
```

- 「絞り込み設定」: `data-toggle="modal" data-target="#newFunnelModal"`
- 「設定解除」: `clearFilter()` — xóa toàn bộ filter
- 「X人が対象」: `showUserList()` — xem danh sách người thỏa điều kiện

---

### 3.2 V2 — Modal Filter Nâng cao (「絞り込み」)

#### Layout tổng thể

```
+================================================================+
|  [×]                    絞り込み                                |
|  ┌──────────────────────────────────────────────────────────┐  |
|  │ 「全て満たす」必要がある条件 (and条件)を追加   [TAB AND]   │  |
|  │ 「どれか1つ以上満たす」必要がある条件(or条件)を追加[TAB OR] │  |
|  └──────────────────────────────────────────────────────────┘  |
|  ┌─────────────┐  ┌──────────────────────────────────────────┐ |
|  │ LEFT PANEL  │  │ RIGHT AREA — Điều kiện đã thêm           │ |
|  │ (filter     │  │ 「全て満たす」条件 (AND):                   │ |
|  │  type list) │  │  [condition card] [condition card] ...   │ |
|  │             │  │                                          │ |
|  │             │  │ 「どれか1つ以上満たす」条件 (OR):           │ |
|  │             │  │  [condition card]                        │ |
|  └─────────────┘  └──────────────────────────────────────────┘ |
|                    [           保存           ]                 |
+================================================================+
```

**Kích thước**: Full-screen viewport; content area rộng 1100px (responsive: 95% nếu màn hình nhỏ hơn)  
**Màu sắc**: Nền `#F6F6F6`; nút active và「保存」màu `#08BF5A` (xanh lá)

#### Tab Bar AND/OR

| Tab | Label | Khi active |
|-----|-------|-----------|
| AND | 「全て満たす」必要がある条件 (and条件)を追加 | Nền `#08BF5A`, chữ trắng |
| OR | 「どれか1つ以上満たす」必要がある条件 (or条件)を追加 | Nền trắng |

Click tab xác định điều kiện mới sẽ vào nhóm AND hay OR.

#### Left Panel — Danh sách Filter Types (chế độ thông thường)

Mỗi loại là nút `[+ Label]` với icon `fa-plus-circle`. Click → thêm condition card vào right area.

| Nhãn nút JP | Filter type key | Vue method |
|-------------|----------------|-----------|
| タグ | `tag` | `addItem('tag')` |
| 友だち名 | `friend_name` | `addItem('friend_name')` |
| 友だち追加日 | `day_add_friend` | `addItem('day_add_friend')` |
| ステップ購読状況 | `scenario` | `addItem('scenario')` |
| QRコードアクション | `qr_code` | `addItem('qr_code')` |
| コンバージョン | `conversion` | `addItem('conversion')` |
| 確認状況 | `status_search` | `addItem('status_search')` |
| 友だち情報 | `friend_info` | `addItem('friend_info')` |
| 対応ステータス | `status_chat` | `addItem('status_chat')` |
| アフィリエイター | `affiliate` | `addItem('affiliate')` |
| 新規・既存 友だち | `bot_new_friend` | `addItem('bot_new_friend')` |

> **Chế độ calendar**: Chỉ hiển thị nút 「タグ」(áp dụng cho `type_parent_filter` liên quan đến calendar).  
> **Nút disabled**: `ステップ購読状況` và `確認状況` bị disable (class `no_click`) trong một số context, kiểm soát bởi `type_ignore` và `type_ignore_or`.

#### Condition Cards (Right Area)

Mỗi điều kiện đã thêm hiển thị dạng card (`.box-action`):
- **Header**: tên filter + preview text điều kiện đã chọn + nút xóa (trash icon)
- **Body**: form chi tiết (expand/collapse khi click header)

#### 11 Filter Types Chi tiết (V2)

##### タグ (tag)
- Folder-tree chọn category (trái) + checkbox-list chọn tags (phải)
- Hỗ trợ「以下を全選択」(check all trong nhóm)
- Condition dropdown: 4 options (OR/AND/OR NOT/AND NOT) — tương tự V1

##### 友だち名 (friend_name)
- Text input tìm kiếm keyword
- Checkboxes: LINE登録名, 本名, システム表示名

##### 友だち追加日 (day_add_friend)
- **Hai chế độ** (chọn qua `day_filter_type`):
  - Chế độ 0: Khoảng ngày tuyệt đối (date range picker từ-đến)
  - Chế độ 1: Tương đối — số ngày trước hôm nay (`duration_day_start` đến `duration_day_end`)

##### ステップ購読状況 (scenario)
- Single-select scenario (searchable)
- Condition dropdown (5 options — xem mục 3.1 Filter 4)
- Input số ngày khi chọn option 2

##### QRコードアクション (qr_code)
- Multi-select QR code (landing) list
- Condition dropdown: bất kỳ đã scan / tất cả đã scan / chưa scan bất kỳ / chưa scan tất cả

##### コンバージョン (conversion)
- Multi-select conversion list
- Condition dropdown: 4 options (OR/AND/OR NOT/AND NOT)

##### 確認状況 (status_search)
- Checkboxes trạng thái xác nhận tin nhắn (「メッセージ確認状況」)

##### 友だち情報 (friend_info)
- Chọn trường thông tin tùy chỉnh của bạn bè
- Toán tử so sánh tùy theo kiểu dữ liệu của trường (text: chứa/không chứa; số: lớn hơn/nhỏ hơn; ngày: trước/sau)
- Hỗ trợ cả trường mặc định hệ thống (ID âm) và trường tùy chỉnh của bot (ID dương)

##### 対応ステータス (status_chat)
- Multi-select trạng thái xử lý chat
- Filter type: lọc vào (0) hoặc loại trừ (1)

##### アフィリエイター (affiliate)
- Multi-select danh sách affiliater
- Filter type: lọc vào (0) hoặc loại trừ (1)

##### 新規・既存 友だち (bot_new_friend)
- Chọn: 新規友だち (bạn bè mới) hoặc 既存友だち (bạn bè cũ)
- DB: `conversation.is_old_friend` (0=mới, 1=cũ)

#### Footer V2

Nút「保存」(màu `#08BF5A`, width 250px, căn giữa) → gọi `closeModalFilterAction()` → gọi EP-03 save-filter-v2.

---

### 3.3 Interaction Flow

#### Flow V1 (Base)

1. User click「絞り込み設定」trên trang → modal `#newFunnelModal` mở
2. User thiết lập điều kiện (mọi điều kiện kết hợp AND)
3. **Broadcast variant**: click「この条件で決定」→ preview cập nhật (「X人へ送信されます」đỏ) → click「決定」để xác nhận
4. **Các variant khác**: click「この条件で決定」→ `saveFilter()` → modal đóng
5. Ngoài modal: `filter_control` hiển thị preview + số người (`X人が対象`)
6. Click「設定解除」→ `clearFilter()` → xóa toàn bộ filter

#### Flow V2 (Modern)

1. User click nút mở modal (tên nút tùy context)
2. Modal full-screen xuất hiện, load trạng thái đã lưu (gọi EP-04)
3. User chọn tab AND hoặc OR
4. User click nút filter type ở left panel → condition card xuất hiện ở right area
5. User click vào card header để expand, cấu hình chi tiết
6. Có thể thêm nhiều điều kiện (mỗi click = 1 card mới)
7. Xóa từng điều kiện bằng trash icon trên card
8. Click「保存」→ gọi EP-03 → lưu filter → modal đóng → hiển thị số bạn bè mới

#### State Transitions

| Trạng thái | Mô tả |
|-----------|-------|
| Trước khi mở modal | Filter preview hiển thị (hoặc「条件なし（全員）」nếu chưa set) |
| Trong modal (chưa confirm) | Thay đổi chưa có hiệu lực với entity cha |
| Sau confirm V1 (`saveFilter`) | Filter lưu vào session/state; preview cập nhật; count cập nhật |
| Sau confirm V2 (`保存`) | Filter lưu vào `filters_v2`; entity cha được update; modal đóng |
| Sau `clearFilter` | Filter xóa; preview reset về「条件なし（全員）」|

---

## 4. API Endpoints

| EP | Method | URL | Mô tả |
|----|--------|-----|-------|
| EP-01 | POST | `/ajax/filter/get-list-tags-and-conversions` | Load danh sách tag categories + tags + conversions cho modal |
| EP-02 | POST | `/ajax/filter/get-list-user` | Lấy bạn bè theo filter V1 (real-time, không lưu DB) |
| EP-03 | POST | `/ajax/filter/save-filter-v2` | Lưu filter V2 + tính số bạn bè + update entity cha |
| EP-04 | POST | `/ajax/init-data-filter` | Load trạng thái filter V2 đã lưu khi mở modal |
| EP-05 | POST | `/ajax/get-list-group-tag-filter` | Lazy load tags theo group (accordion) |
| EP-06 | POST | `/ajax/get-list-rich-menu` | Load danh sách rich menu (cho filter rich menu) |
| EP-07 | POST | `/ajax/get-list-form-answer-rich-menu` | Load form answers (cho rich menu filter) |
| EP-08 | POST | `/ajax/get-list-template-rich-menu` | Load templates (cho rich menu filter) |

### EP-03 — Chi tiết lưu filter V2 (endpoint quan trọng nhất)

**Request bắt buộc**: `parent_type` (string), `parent_id` (int, có thể null một số loại)  
**Request tùy chọn**: `item_search` (JSON AND conditions), `item_search_or` (JSON OR conditions)

**Response**:
```json
{
  "success": true,
  "number_filter": 150,
  "filter_date": "2024-01-15 10:30:00",
  "line_user_ids": [...],
  "array_filter_id": [1, 2, 3],
  "parentIdNew": 42
}
```

**Các lỗi đặc biệt cho Broadcast**:
- Đang delivering: `"配信処理中です。編集できません。"`
- Đã delivered: `"既に配信済のため変更できません。"`
- Trong 5 phút trước giờ gửi: `"配信予定日時5分前からは配信内容の編集はできません。"`

### EP-04 — Chi tiết load filter V2

**Request**: `parent_type`, `parent_id`, và tùy chọn `copy_id` (để copy filter từ bản khác)

**Response**: Mảng `item_search` (AND) + `item_search_or` (OR) đã được enrich thêm thông tin hiển thị (tag names, scenario names, v.v.) + `number_filter` + `line_user_ids`

**Ngoại lệ**: `step_message` và `filter_manager` không nhận `number_filter`. `broadcast` và `filter_manager` không nhận `line_user_ids`.

---

## 5. Data Model

### 5.1 Bảng chính: `filters_v2`

**Mục đích**: Lưu từng điều kiện filter V2. Mỗi record = 1 điều kiện (1 filter card trong modal).

```sql
CREATE TABLE `filters_v2` (
  `id`                    int(10) UNSIGNED NOT NULL,
  `bot_id`                int(11) DEFAULT NULL,          -- bot sở hữu
  `parent_type`           varchar(255) DEFAULT NULL,     -- loại entity cha
  `parent_id`             int(11) DEFAULT NULL,           -- ID entity cha
  `operator`              varchar(100) DEFAULT NULL,      -- 'and' hoặc 'or'
  `type`                  varchar(255) DEFAULT NULL,      -- loại filter
  `data`                  text,                           -- JSON chi tiết điều kiện
  `text_preview`          text,                           -- text tóm tắt hiển thị UI
  `created_at`            timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`            timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `rich_menu_item_id`     int(11) DEFAULT NULL,           -- chỉ filter-rich-menu-toggle
  `rich_menu_redirect_id` int(11) DEFAULT NULL            -- chỉ filter-rich-menu-toggle
);
```

**Data size**: 17.8MB  
**Confidence**: Cao (xác nhận trực tiếp từ source code + DB schema)

### 5.2 Bảng legacy: `filters` (V1)

Lưu filter V1 — 1 record = toàn bộ điều kiện của 1 entity. Gắn trực tiếp với `auto_reply_id`, `broadcast_id`, hoặc `sms_schedule_id`. **Data size**: 477KB.

### 5.3 Cấu trúc JSON trong `filters_v2.data` theo từng filter type

| `type` | Keys chính | Ghi chú |
|--------|-----------|---------|
| `tag` | `tags_search` (array IDs), `tag_option` (0-3) | |
| `day_add_friend` | `day_filter_type` (0/1), `modal_from_filter`+`modal_to_filter` hoặc `duration_day_start`+`duration_day_end` | 2 chế độ |
| `scenario` | `scenario_search` (ID), `scenario_condition` (0-4), `number_date` | |
| `conversion` | `conversion_search` (string comma-separated IDs), `conversion_option` (0-3) | IDs lưu dạng string |
| `qr_code` | `qrs_search` (array landing IDs), `qr_condition` (0-3) | |
| `qr_code_action` | `qrs_search` (array landing IDs), `qr_condition` (0) | |
| `friend_info` | `info_search` (field ID), `type_data`, `op_compare`, `keyword`/`value`/`point` | ID âm = trường mặc định |
| `status_chat` | `status_chat_search` (array IDs), `status_chat_filter_type` (0/1) | |
| `affiliate` | `affiliate_search` (array IDs), `affiliate_filter_type` (0/1) | |
| `bot_new_friend` | `check_box_value` (0=新規, 1=既存) | |

### 5.4 Các bảng data source cho filter options

| Bảng | Dùng cho filter | Kích thước |
|------|----------------|-----------|
| `line_user` | Tất cả filter (bảng người dùng LINE) | 139.1MB |
| `bot_line_user` | Tất cả filter (liên kết bot-user, ngày kết bạn, affiliater) | 137.2MB |
| `tags` | Filter tag | 245KB |
| `tag_line_user` | Pivot tag-user | 134KB |
| `category` | Nhóm tag | 509KB |
| `scenario` | Filter scenario | 300KB |
| `scenario_lineuser` | Trạng thái đăng ký scenario | 218KB |
| `conversion` | Filter conversion | 187KB |
| `conversion_result` | Lịch sử conversion | 3KB |
| `landing` | Filter QR code (bảng QR codes) | 607KB |
| `detail_landing_click` | Lịch sử scan QR | 253KB |
| `conversation` | Filter mark, status_chat, bot_new_friend | 68.8MB |
| `status_chat` | Danh sách trạng thái xử lý chat | 801KB |
| `friend_information_setting` | Định nghĩa trường thông tin bạn bè | 627KB |
| `friend_information_value` | Giá trị trường thông tin bạn bè | 134KB |
| `affiliaters` | Danh sách affiliater | 35KB |
| `filter_manager` | Filter đã đặt tên để tái sử dụng | 94KB |

---

## 6. Filter → DB Mapping Matrix

### V1 Filter

| Filter Type (JP) | Request Param | DB Table | Column | SQL Pattern | Confidence |
|-----------------|--------------|----------|--------|-------------|------------|
| 名前 (LINE登録名) | `name_filter` + type=1 | `line_user` | `name` | `LIKE '%keyword%'` | **Cao** |
| 名前 (本名) | `name_filter` + type=2 | `line_user` | `real_name` | `LIKE '%keyword%'` | **Cao** |
| 名前 (システム表示名) | `name_filter` + type=3 | `line_user` | `view_name` | `LIKE '%keyword%'` | **Cao** |
| タグ (OR) | `tag_filter` + option=0 | `tag_line_user` | `tag_id` | `JOIN WHERE tag_id IN (list)` | **Cao** |
| タグ (AND) | `tag_filter` + option=1 | `tag_line_user` | `tag_id` | `HAVING COUNT(DISTINCT tag_id) = N` | **Cao** |
| タグ (OR NOT / AND NOT) | option=2/3 | `tag_line_user` | `tag_id` | `NOT IN (subquery)` | **Cao** |
| 友だち登録日 (từ) | `from_date_filter` | `bot_line_user` | `followed_at` | `WHERE followed_at >= ?` | **Cao** |
| 友だち登録日 (đến) | `to_date_filter` | `bot_line_user` | `followed_at` | `WHERE followed_at <= ? (23:59:59)` | **Cao** |
| ステップ (đang đăng ký) | `scenario_filter` + option=0 | `scenario_lineuser` | `is_following` | `= 1, is_deleted = 0` | **Cao** |
| ステップ (không đăng ký) | option=1 | `scenario_lineuser` | `is_following` | `NOT IN (is_following=1)` | **Cao** |
| ステップ (đã đọc xong) | option=3 | `scenario_lineuser` | `is_following` | `= 2, is_deleted = 0` | **Cao** |
| コンバージョン | `conversion_filter` + option | `conversion_result` | `conversion_id` | Tương tự tag (4 options) | **Cao** |
| メッセージ確認状況 | `mark_filter` | `conversation` | `status_last_message` | `WHERE status_last_message IN (?)` | **Cao** |

> **Lưu ý**: `mark_filter` nhận giá trị `status_last_message` trực tiếp (0=未確認, 1=確認済み). Xem mục 9 (Gaps) về mâu thuẫn với API spec.

### V2 Filter

| Filter type key | DB Table chính | Column lọc | Confidence |
|----------------|---------------|-----------|------------|
| `tag` | `tag_line_user` | `tag_id` | **Cao** |
| `friend_name` | `line_user` | `name`/`real_name`/`view_name` | **Trung bình** (chưa xác nhận đầy đủ) |
| `day_add_friend` | `bot_line_user` | `followed_at` | **Cao** |
| `scenario` | `scenario_lineuser` | `is_following`, `start_datetime` | **Cao** |
| `qr_code` | `detail_landing_click` | `landing_id`, `action=2` | **Cao** |
| `qr_code_action` | `detail_landing_click` | `landing_id`, `is_action_web IN (1,2)` | **Cao** |
| `conversion` | `conversion_result` | `conversion_id` | **Cao** |
| `status_search` / `確認状況` | `conversation` | `status_last_message` | **Cao** |
| `friend_info` | `friend_information_value` | `friend_information_setting_id`, `value` | **Cao** |
| `status_chat` | `conversation` | `id_status` | **Cao** |
| `affiliate` | `bot_line_user` | `affiliater_id` | **Cao** |
| `bot_new_friend` | `conversation` | `is_old_friend` | **Cao** |
| `richmenu` | `bot_line_user` | `rich_menu_id` | **Trung bình** (xác nhận một phần) |

**Query chain chuẩn (V2)**:
```
bot_line_user (base)
  JOIN line_user ON line_user.id = bot_line_user.line_user_id
  WHERE bot_line_user.bot_id = ? AND bot_line_user.is_blocked = 0
  [+ conditional JOINs/subqueries tùy filter type]
```

---

## 7. Business Rules

### 7.1 Khi nào dùng V1 vs V2

- **Filter V1** (`/ajax/filter/get-list-user`): Filter đơn giản, **không lưu DB**, trả kết quả ngay. Chỉ hỗ trợ AND. Dùng cho Broadcast V1 và Friendlist cũ.
- **Filter V2** (`save-filter-v2` + `init-data-filter`): Filter phức tạp, **lưu trạng thái** vào `filters_v2`. Hỗ trợ AND + OR. Dùng cho hầu hết tính năng từ V2 trở đi (61+ files).

### 7.2 AND/OR Logic (V2)

```
Kết quả cuối = (AND điều kiện 1) VÀ (AND điều kiện 2) VÀ ...
               VÀ (OR điều kiện A HOẶC OR điều kiện B HOẶC ...)
```

- `operator='and'`: tất cả điều kiện AND phải thỏa mãn đồng thời
- `operator='or'`: ít nhất một điều kiện OR phải thỏa mãn
- Engine: `Conversation::advanceFilterPost($bot_id, $itemFilterAnd, $itemFilterOr, $keyword, ...)`

### 7.3 Broadcast Protection

Trước khi lưu filter cho broadcast, hệ thống kiểm tra:
- Status `delivering` (đang phát): **chặn hoàn toàn** — không thể sửa
- Status `delivered` (đã phát xong): **chặn hoàn toàn** — không thể sửa
- Trong vòng **5 phút trước giờ gửi** (và không phải draft): **chặn** — trả lỗi

### 7.4 Cascade Copy cho Broadcast Con

Khi lưu filter cho broadcast cha (`parent_type=broadcast`):
1. Lưu filter cho cha
2. Tìm tất cả broadcast có `parent_id = parentId` (các broadcast con)
3. Xóa filter cũ của chúng
4. Copy filter của cha sang mỗi broadcast con

### 7.5 Mark Filter — Enum Values

Filter 「メッセージ確認状況」dùng giá trị từ `conversation.status_last_message`:

| Giá trị | UI Label | CSS | Trạng thái |
|---------|----------|-----|----------|
| 0 | 未確認 | label-info (xanh) | Chưa xác nhận |
| 1 | 確認済み | label-default (xám) | Đã xác nhận |
| 2-9 | Các trạng thái cũ | — | **Đã comment out** — không hiển thị trên UI, chỉ còn trong code lịch sử |

> Values 4 và 6 bị skip hoàn toàn trong enum.

### 7.6 Friend Info Filter — ID Đặc biệt

Trường thông tin bạn bè (`friend_info`) sử dụng hệ thống ID phân cấp:

| ID range | Nguồn | Folder |
|----------|-------|--------|
| `id > 0` | `FriendInformationSetting` tùy chỉnh của bot | `group_id` thực |
| `-1 >= id > -7` | Config `sns-line.info_default_info` (trường mặc định) | root (`folder_id = -1`) |
| `id <= -7` hoặc `= 'd_6'` | Config `sns-line.info_default_info_address` (địa chỉ mặc định) | nhóm địa chỉ (`folder_id = -2`) |

### 7.7 parent_type Điều hướng Behavior

`parent_type` là tham số cốt lõi quyết định toàn bộ hành vi:

| parent_type | Tính filterNumber? | Trả line_user_ids? | Side effect |
|-------------|-------------------|-------------------|-------------|
| `broadcast`, `broadcast-v2` | Có | Không | Update `broadcasts.filter_number` + `filter_date`; copy sang broadcast con |
| `step_message` | **Không** | Có | — |
| `filter_manager` | **Không** | **Không** | — |
| `cross_analysis` | Có (isCountOnly=true) | Có | — |
| `action_schedule` | Có | Có | Không cần `parent_id` |
| `setting_rich_menu` | Có | Có | ParentID chuyển sang ID của `SettingDisplayRichMenuHistory` DRAFT |
| `filter-rich-menu-toggle` | Có | Có | Update `rich_menu_switch_items.filter_ids` (khi có `filter_action_type`) |
| `calendar-*` (5 types) | Có | Có | Update filter_id/filter_number trên entity calendar tương ứng |
| `filter_remind_form` | Có | Có | Update `event_steps.is_use_filter_remind` (0 hoặc 1) |

### 7.8 Copy/Clone Filter

- **Copy via `copy_id`**: `initDataFilter` nhận `copy_id` → load filter của bản gốc nhưng clear ID → khi save sẽ tạo bản mới
- **Clone via `FilterV2::cloneFilters()`**: Sao chép toàn bộ filter records sang parent mới (dùng khi duplicate entity)
- **Cascade broadcast**: Xem mục 7.4

### 7.9 day_add_friend — Hai Chế độ

Filter ngày kết bạn có hai chế độ chọn bằng `day_filter_type`:

| day_filter_type | Chế độ | Fields sử dụng |
|----------------|--------|---------------|
| 0 | Khoảng ngày tuyệt đối | `modal_from_filter`, `modal_to_filter` (date) |
| 1 | Tương đối — X ngày trước hôm nay | `duration_day_start`, `duration_day_end` (số ngày) |

Khi lưu: chỉ lưu fields của chế độ đang dùng, unset fields của chế độ kia.

### 7.10 setting_rich_menu — Parent ID Thay đổi

Khi `parent_type = 'setting_rich_menu'`:
1. Hệ thống tìm hoặc tạo `SettingDisplayRichMenuHistory` với `status = DRAFT`
2. **ParentID được đổi sang ID của history record** (không phải ID của rich menu gốc)
3. Trả về `parentIdNew` trong response để frontend cập nhật

---

## 8. Khác biệt giữa các Contexts

| Feature / Context | Version | Variant | Đặc điểm riêng |
|-------------------|---------|---------|----------------|
| Broadcast V1 | V1 | broadcast | Width 900px; preview số người (màu đỏ); nút「決定」riêng ở footer |
| Friendlist V1 | V1 | friendlist | Dynamic marks (「対応マーク」); submit form về `friendlistHome` |
| Broadcast V2 | V2 | standard | parent_type=`broadcast`/`broadcast-v2`; cascade copy sang con; broadcast protection |
| Step Message | V2 | standard | parent_type=`step_message`; KHÔNG tính filterNumber |
| Filter Manager | V2 | standard | KHÔNG tính filterNumber, KHÔNG trả `line_user_ids` |
| Cross Analysis | V2 | special | Dùng `saveFilterCrossAnalysis` — luôn INSERT mới, không update |
| Action Schedule | V2 | standard | Không cần `parent_id` |
| Rich Menu Setting | V2 | special | ParentID chuyển sang SettingDisplayRichMenuHistory ID |
| Rich Menu Toggle | V2 | special | Thêm điều kiện `rich_menu_redirect_id` + `rich_menu_item_id` |
| Calendar (5 loại) | V2 | calendar | Left panel chỉ có タグ; 5 parent_type khác nhau → update column khác nhau |

---

## 9. Gaps và Unknowns

Các vấn đề chưa xác nhận hoàn toàn, cần điều tra thêm khi cần:

### [Gap-01] Mâu thuẫn giá trị `mark_filter` (Trung bình)

- **Vấn đề**: API Spec EP-02 ghi `mark_filter=1` là "marked", `mark_filter=2` là "not_marked". DB Mapping xác nhận code thực tế dùng `whereIn('conversation.status_last_message', $markFilter)` với giá trị 0 và 1 (tương ứng UI checkbox values 未確認/確認済み).
- **Tác động**: Dev đọc API spec có thể truyền sai giá trị.
- **Hướng giải quyết**: Kiểm tra JS frontend trong `modal_filter.blade.php` để xác nhận giá trị thực tế gửi lên; sau đó sửa API Spec EP-02.

### [Gap-02] Tên bảng sai trong Logic Spec (Nhẹ)

- **Vấn đề**: Logic Spec dùng sai tên 5 bảng (số nhiều): `categories` → `category`, `scenarios` → `scenario`, `landings` → `landing`, `friend_information_settings` → `friend_information_setting`, `status_chats` → `status_chat`.
- **Tác động**: Dev đọc logic spec có thể query sai tên bảng.
- **Xác nhận đúng**: Xem DB Mapping sections 8-14.

### [Gap-03] `friend_name` V2 chưa xác nhận đầy đủ (Nhẹ)

- **Vấn đề**: Filter type `friend_name` trong V2 thấy reference trong code nhưng chưa xác nhận cấu trúc JSON `data` đầy đủ và cách xử lý trong `advanceFilterPost`.
- **Hướng giải quyết**: Tìm case `friend_name` trong `Conversation::advanceFilterPost()`.

### [Gap-04] `richmenu` filter type chưa xác nhận query (Nhẹ)

- **Vấn đề**: Filter type `richmenu` được detect trong `initDataFilter` nhưng không tìm thấy case xử lý trong switch statement của `advanceFilterPost`. Cách query thực tế chưa rõ.
- **Hướng giải quyết**: Tìm trong `Conversation.php` đoạn ngoài switch statement để xác nhận cách dùng `richmenuId`.

### [Gap-05] EP-09 (Broadcast store-broadcast) confidence thấp (Nhẹ)

- **Vấn đề**: Endpoint `/basic/message-send-all/store-broadcast` với `action=save_filter` chưa xác minh từ BroadcastController.
- **Hướng giải quyết**: Khi spec tính năng Broadcast Messaging, xác nhận endpoint này và cập nhật API Spec.

### [Gap-06] `marks` trong Friendlist variant (Nhẹ)

- **Vấn đề**: Vue data `marks` trong friendlist variant được định nghĩa từ đâu (server API hay hardcode JS)?
- **Hướng giải quyết**: Kiểm tra FriendlistController để xác nhận nguồn dữ liệu.

### [Gap-07] Màn hình chụp V1 chưa có (Tùy chọn)

- Chỉ có 1 screenshot V2 (`screenshots/filter-modal-v2.png`). Không có screenshot V1.
- Không ảnh hưởng đến tính chính xác của spec.

---

## 10. Chất lượng Spec

### Coverage

| Spec file | Coverage | Đánh giá |
|-----------|---------|---------|
| UI Spec | 95% | Đầy đủ, rõ ràng. Thiếu screenshot V1. |
| API Spec | 90% | 8/9 endpoints đầy đủ; mark_filter values cần xác nhận lại. |
| Logic Spec | 92% | Đầy đủ business rules; có 5 tên bảng sai (không ảnh hưởng logic). |
| DB Mapping | 95% | Xuất sắc; xác nhận trực tiếp từ source code; phát hiện nhiều sai lệch. |
| **Tổng thể** | **~93%** | Vượt ngưỡng 70% yêu cầu. |

### Độ tin cậy tổng thể

**Cao** — Phần lớn thông tin được xác nhận trực tiếp từ source code (`FilterController.php`, `FilterV2.php`, `Conversation.php`) và database schema. Các gaps đều đã được ghi nhận và phân loại.

### Các phát hiện quan trọng (từ DB Mapping)

Những điểm này đặc biệt quan trọng vì db-hint ban đầu dự đoán sai — **spec đã sửa đúng**:

1. `is_mark` **không tồn tại** trong DB — filter mark thực tế dùng `conversation.status_last_message`
2. `view_name` ở bảng `line_user` (không phải `bot_line_user`) — type=3 (システム表示名)
3. Tên bảng đều **số ít**: `scenario`, `conversion`, `landing`, `category`
4. `detail_landing_click` join qua `line_id` **string** (không phải integer FK)
5. `conversation.is_old_friend` cho filter `bot_new_friend` (0=新規, 1=既存)
6. `conversation.id_status` là FK → `status_chat.id` cho filter `status_chat`
7. `bot_line_user.affiliater_id` là FK → `affiliaters.id` cho filter `affiliate`
8. `filters_v2.data` là JSON text không normalize — lưu toàn bộ filter state

### Open Questions (cần PM/Dev làm rõ)

1. Giá trị thực tế của `mark_filter` param được truyền từ frontend: `0`/`1` hay giá trị khác? (Gap-01)
2. Định nghĩa `marks` trong friendlist: server trả về hay hardcode JS? (Gap-06)
3. Luồng lưu filter Broadcast V1 qua `store-broadcast` với `action=save_filter` hoạt động như thế nào? (Gap-05)

---

*Spec được tổng hợp từ: ui-spec.md, api-spec.md, logic-spec.md, db-mapping.md, validation-report.md. Xác nhận trực tiếp từ source code Laravel và MySQL schema.*
