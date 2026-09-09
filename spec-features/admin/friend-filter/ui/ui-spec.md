# UI Spec — Friend Filter Modal (SC-003)

**ID Component**: SC-003  
**Tên hiển thị**: 「絞り込み」/ 「絞り込み設定」  
**HTML ID**: `#newFunnelModal`  
**Loại**: Shared Component — Modal lọc bạn bè  
**Phiên bản**: V1 (cũ) và V2 (mới, hiện đại)

---

## 1. Tổng quan

Component này là **modal popup** dùng để lọc danh sách bạn bè (LINE friends) theo nhiều tiêu chí kết hợp. Người dùng thiết lập điều kiện lọc, xác nhận, và kết quả được áp dụng cho tính năng đang sử dụng (broadcast, friendlist, auto-reply targeting, step scenario, v.v.).

### Ai sử dụng
- **Admin** và **Staff** (với quyền phù hợp)
- Xuất hiện trong 61+ màn hình khác nhau của hệ thống

### Mục đích theo context
| Context | Mục đích |
|---------|----------|
| Broadcast (「メッセージ配信」) | Chọn đối tượng nhận tin nhắn hàng loạt |
| Friendlist (「友だちリスト」) | Lọc hiển thị danh sách bạn bè |
| Step/Scenario | Chọn điều kiện trigger bước ステップ |
| Auto-reply (「自動応答」) | Giới hạn đối tượng nhận auto-reply |
| Rich Menu, Form, Action, v.v. | Giới hạn đối tượng áp dụng |

---

## 2. Hai Variants Chính

### SCR-FF-01 — Filter V1 (Base/Classic)

**File nguồn chính**:
- `resources/views/basic/filter/modal_filter.blade.php` — base version
- `resources/views/basic/broadcast/modal_filter.blade.php` — broadcast variant (width 900px)
- `resources/views/basic/friendlist/layout/modal_filter.blade.php` — friendlist variant

**Đặc điểm nhận dạng**:
- Modal Bootstrap chuẩn, width `modal-lg` (khoảng 900px)
- Title: 「絞り込み設定」
- Body: bảng HTML (`table table-bordered`) với 6 hàng filter
- Header section: 「すべて満たす」必要がある条件 (and条件)
- Chỉ hỗ trợ AND conditions (không có OR)
- Footer: nút「この条件で決定」hoặc「決定」(gọi `saveFilter()`)

---

#### SCR-FF-01: Layout tổng thể (V1)

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
| │ ステップ     │ [scenario select]  │   |
| │              │ [condition select] │   |
| ├──────────────┼────────────────────┤   |
| │ コンバージョン│ [multi-select]      │   |
| │              │ [dropdown option]   │   |
| ├──────────────┼────────────────────┤   |
| │ メッセージ確認│ □未確認 □確認済み   │   |
| │ 状況         │                    │   |
| └────────────────────────────────────┘   |
|        [この条件で決定]                    |
+------------------------------------------+
```

---

#### SCR-FF-01: Chi tiết từng Filter Type (V1)

##### Filter 1: 「名前」(Tên bạn bè)

| Thuộc tính | Giá trị |
|-----------|---------|
| Loại input | Text input + checkboxes |
| Form field | `modal_name_filter` (text), `modal_name_filter_type[]` (checkbox array) |
| Placeholder | (trống) |
| Help text | 「スペースで区切るといずれかにあてはまる友だちを絞り込めます」|
| Loại tìm kiếm | Nhiều từ khóa cách nhau bằng dấu cách = OR giữa các từ |

**Checkbox options** (`modal_name_filter_type[]`):
| Label | Value |
|-------|-------|
| LINE登録名 | 1 |
| 本名 | 2 |
| システム表示名 | 3 |

Logic: tìm trong các trường được chọn (có thể chọn nhiều)

---

##### Filter 2: 「タグ」(Tag)

| Thuộc tính | Giá trị |
|-----------|---------|
| Loại input | Multi-select (tag picker) + dropdown option |
| Form field | `modal_add_tag_ids` (hidden, comma-separated IDs), `modal_tag_filter_option` (select) |
| UI | Input area có thể click để mở tag pool; hiển thị tag đã chọn dạng label |

**Tag picker UI**:
- Click vào input area để mở dropdown
- Bên trái: danh sách category (bao gồm「未分類」và các category có tên)
- Bên phải: danh sách tags trong category đã chọn
- Tags đã chọn hiển thị dưới dạng badge với nút X để xóa

**Dropdown option** (`modal_tag_filter_option`):
| Label | Value |
|-------|-------|
| 選択したタグのいずれか1つ以上を含む人 | 0 |
| 選択したタグをすべて含む人 | 1 |
| 選択したタグを1つ以上含む人を除外 | 2 |
| 選択したタグを全て含む人を除外 | 3 |

---

##### Filter 3: 「友だち登録日」(Ngày đăng ký bạn bè)

| Thuộc tính | Giá trị |
|-----------|---------|
| Loại input | Date range picker (2 inputs) |
| Form field | `modal_from_filter` (từ ngày), `modal_to_filter` (đến ngày) |
| Placeholder | 「日付選択」 |
| Format | Ngày (date picker) |
| Connector text | 「から」(từ ... đến) |
| Behavior | Nhấn Delete/Backspace để xóa ngày (`clearDateFilter`) |

Logic: lọc bạn bè đã đăng ký trong khoảng thời gian từ-đến (khoảng ngày, cả hai đầu tùy chọn)

---

##### Filter 4: 「ステップ」(Scenario/Step)

| Thuộc tính | Giá trị |
|-----------|---------|
| Loại input | Dropdown chọn scenario + dropdown chọn điều kiện + input số ngày |
| Form field | `modal_scenario_filter` (select scenario ID), `modal_scenario_filter_option` (select condition), `modal_scenario_start_day_filter` (number) |

**Scenario select**: danh sách từ server (`$scenario` variable), option đầu là「選択なし」(value = "")

**Condition dropdown** (`modal_scenario_filter_option`):
| Label | Value |
|-------|-------|
| を購読中の人 | 0 |
| を現在購読していない人 | 1 |
| の？日目まで送信済みの人 | 2 |
| を読了した人 | 3 |
| を読了していない人 | 4 |

**Input số ngày** (`modal_scenario_start_day_filter`): chỉ hiện khi option = 2 (「の？日目まで送信済みの人」), nhập số nguyên >= 0, suffix「日目」

---

##### Filter 5: 「コンバージョン」(Conversion)

| Thuộc tính | Giá trị |
|-----------|---------|
| Loại input | Multi-select (conversion picker) + dropdown option |
| Form field | `modal_add_conversion_ids` (hidden, comma-separated IDs), `modal_conversion_filter_option` (select) |
| Placeholder | 「コンバージョン名を入力」|
| UI | Tương tự tag picker; click để mở danh sách conversion |

**Dropdown option** (`modal_conversion_filter_option`):
| Label | Value |
|-------|-------|
| 選択したコンバージョンのいずれか1つ以上を含む人 | 0 |
| 選択したコンバージョンをすべて含む人 | 1 |
| 選択したコンバージョンを1つ以上含む人を除外 | 2 |
| 選択したコンバージョンを全て含む人を除外 | 3 |

---

##### Filter 6: 「メッセージ確認状況」/ 「対応マーク」(Trạng thái xử lý tin nhắn)

**Trong base và broadcast variant** (`メッセージ確認状況`):
| Label | Value | CSS class |
|-------|-------|-----------|
| 未確認 | 0 | `label-info` (màu xanh) |
| 確認済み | 1 | `label-default` (màu xám) |

Form field: `modal_mark_filter[]` (checkbox array)  
Help text: 「複数選択した場合、いずれかにあてはまる友だちを絞り込めます」

**Bị comment out (có trong code nhưng không hiển thị)**:
- value=2: 未返信（マガジンコメント）
- value=3: 未返信（重要度低）
- value=5: 要対応（質問）
- value=7: 要対応（トラブル）
- value=8: 要対応（クロージング）
- value=9: 要対応（クレーム）

**Trong friendlist variant** (`対応マーク`): dynamic từ Vue data `marks` (các mark được định nghĩa từ server), form field `status_search` (v-model array)

---

#### SCR-FF-01: Điểm khác biệt giữa các Context (V1)

| Context | Sự khác biệt |
|---------|-------------|
| **Base** (`basic/filter`) | Footer: nút「この条件で決定」gọi `saveFilter()` |
| **Broadcast** (`basic/broadcast`) | Width 900px cố định; thêm preview section bên trong modal (「この条件で決定」preview + 「X人へ送信されます」đỏ + nút「決定」ở footer); font 14px |
| **Friendlist** (`basic/friendlist/layout`) | Thêm hidden form fields (keyword, tags_search, status_search...) để submit về route `friendlistHome`; Filter tên dùng v-model trực tiếp thay vì `name` attribute; 対応マーク thay cho メッセージ確認状況 (dynamic marks); footer behavior khác theo route hiện tại |

---

#### SCR-FF-01: Filter Control Widget

File: `resources/views/basic/filter/filter_control.blade.php`

Đây là wrapper component bao quanh modal, hiển thị trên các trang có filter:

```
反応対象者の絞り込み [任意]
[絞り込み設定]          ← nút mở modal #newFunnelModal
┌─────────────────────────────┐
│ 条件: {preview_content}    [設定解除]│
└─────────────────────────────┘
→ {X}人が対象              ← click để xem danh sách
```

- Nút「絞り込み設定」: mở modal bằng `data-toggle="modal" data-target="#newFunnelModal"`
- Preview area: hiển thị preview điều kiện hiện tại từ server (`$filter['filter_preview_content']`) hoặc「条件なし（全員）」
- Nút「設定解除」: gọi `clearFilter()` để xóa filter
- Count「X人が対象」: click gọi `showUserList()` để xem danh sách người thỏa điều kiện

---

### SCR-FF-02 — Filter V2 (Modern/Full-screen)

**File nguồn**: `resources/views/layout/modal_filter_v2.blade.php` (285KB — rất lớn)  
**Được dùng bởi**: 61 files (xem danh sách tại mục 4)

**Đặc điểm nhận dạng**:
- Modal full-screen (100% width/height viewport) với content area rộng 1100px (responsive: 95% nếu màn hình < 1100px)
- Nền mờ `rgba(0,0,0,0.5)`, không có backdrop riêng
- Title: 「絞り込み」(ngắn hơn V1)
- Tab bar AND/OR ở trên
- Left panel: danh sách loại filter có thể thêm
- Right area: điều kiện đã thêm
- Footer: nút「保存」màu xanh lá (width 250px)
- Hỗ trợ cả AND và OR conditions
- Background màu `#F6F6F6`

---

#### SCR-FF-02: Layout tổng thể (V2)

```
+================================================================+
|  [×]                    絞り込み                                |
|  ┌──────────────────────────────────────────────────────────┐  |
|  │ 「全て満たす」必要がある条件 (and条件)を追加               │  |
|  │ 「どれか1つ以上満たす」必要がある条件 (or条件)を追加       │  |
|  └──────────────────────────────────────────────────────────┘  |
|  ┌─────────────┐  ┌──────────────────────────────────────────┐ |
|  │ [+ タグ]    │  │ 「全て満たす」必要がある条件 (and条件)    │ |
|  │ [+ 友だち名]│  │  [condition card 1]  [condition card 2] │ |
|  │ [+ 友だち追]│  │                                          │ |
|  │ 加日        │  │ 「どれか1つ以上満たす」必要がある条件     │ |
|  │ [+ ステップ]│  │ (or条件)                                  │ |
|  │ 購読状況    │  │  [condition card]                        │ |
|  │ [+ QRコード]│  └──────────────────────────────────────────┘ |
|  │ アクション  │                                                 |
|  │ [+ コンバー]│                                                 |
|  │ ジョン      │                                                 |
|  │ [+ 確認状況]│                                                 |
|  │ [+ 友だち情]│                                                 |
|  │ 報          │                                                 |
|  │ [+ 対応ステ]│                                                 |
|  │ ータス      │                                                 |
|  │ [+ アフィリ]│                                                 |
|  │ エイター    │                                                 |
|  │ [+ 新規・既]│                                                 |
|  │ 存 友だち   │                                                 |
|  └─────────────┘                                                |
|                    [      保存      ]                           |
+================================================================+
```

---

#### SCR-FF-02: Tab Bar AND/OR

Hai nút tab ở trên, màu xanh lá khi active:

| Tab | Label | Vue method |
|-----|-------|-----------|
| AND tab | 「全て満たす」必要がある条件 (and条件)を追加 | `switchAndOrTab('and')` |
| OR tab | 「どれか1つ以上満たす」必要がある条件 (or条件)を追加 | `switchAndOrTab('or')` |

- Tab hiện tại (`.current`): nền `#08BF5A` (xanh lá), chữ trắng
- Tab không active: nền trắng, hover xám nhạt

---

#### SCR-FF-02: Left Panel — Danh sách Filter Types

Mỗi loại filter là một nút (button `.btn-add-action`) với icon `fa-plus-circle`. Click để thêm điều kiện vào vùng bên phải (AND hoặc OR section tùy tab đang active).

**Danh sách đầy đủ (mode thông thường)**:
| Nhãn nút | Filter type key | Vue method |
|----------|----------------|-----------|
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

**Danh sách rút gọn (mode calendar context)**: chỉ có `タグ`  
(Áp dụng cho các `type_parent_filter` liên quan đến calendar: `calendar-course-setting-status-send-after-booking`, `calendar-salon-course-setting-status-send-after-booking`, `filter-calendar-salon-booking`, `calendar-setting-show-booking-form`, v.v.)

**Nút bị disabled** (class `no_click`, cursor `no-drop`): `ステップ購読状況` và `確認状況` trong một số context (controlled bởi `type_ignore` và `type_ignore_or` arrays)

**Nút được highlight** (`.selected`): nút loại filter đang được chọn/focus

---

#### SCR-FF-02: Right Area — Condition Cards

Vùng bên phải chia làm 2 sections:
1. **AND section** (`.tab-title` với label 「全て満たす」必要がある条件 (and条件))
2. **OR section** (nếu có OR conditions)

Mỗi điều kiện đã thêm hiển thị dạng **condition card** (`.box-action`):
- **Header card** (`.title-child`): click để expand/collapse
  - Tên loại filter (vd: 「タグ」)
  - Preview text của điều kiện đã chọn (vd: tên các tag)
  - Nút xóa `fa-trash-alt` bên phải (`.ic-close-filter`)
- **Body card** (`.box-action-body`): form chọn chi tiết (expand/collapse)

---

#### SCR-FF-02: Chi tiết Filter Types (V2)

**Filter タグ (tag)**:
- Left panel: folder-tree chọn category (trái), checkbox-list chọn tags (phải)
- Hỗ trợ「以下を全選択」(check all trong nhóm)
- Tags đã chọn hiển thị preview trong card header
- Condition dropdown tương tự V1 (4 options: いずれか, すべて, 除外いずれか, 除外すべて)

**Filter 友だち名 (friend_name)**:
- Text input tìm kiếm
- Checkboxes: LINE登録名, 本名, システム表示名

**Filter 友だち追加日 (day_add_friend)**:
- Date range picker (từ-đến, dạng date input)

**Filter ステップ購読状況 (scenario)**:
- Single-select scenario (searchable)
- Condition dropdown (購読中, 購読していない, N日目まで送信済み, 読了した, 読了していない)
- Input số ngày (khi cần)

**Filter QRコードアクション (qr_code)**:
- Multi-select QR code actions
- Hiển thị trong phần `#item_qr`

**Filter コンバージョン (conversion)**:
- Multi-select conversion list
- Condition dropdown tương tự V1

**Filter 確認状況 (status_search)**:
- Checkboxes trạng thái xác nhận tin nhắn

**Filter 友だち情報 (friend_info)**:
- Multi-select theo các trường thông tin tùy chỉnh của bạn bè

**Filter 対応ステータス (status_chat)**:
- Select trạng thái xử lý chat (response status)

**Filter アフィリエイター (affiliate)**:
- Multi-select affiliate list

**Filter 新規・既存 友だち (bot_new_friend)**:
- Radio/select: bạn bè mới hoặc bạn bè cũ

---

#### SCR-FF-02: Footer

Nút「保存」(màu `#08BF5A` — xanh lá, width 250px, box-shadow) ở dưới cùng modal, căn giữa.

---

## 3. Interaction Flow

### Flow V1 (Base)
1. User click nút「絞り込み設定」trên trang → modal `#newFunnelModal` mở
2. User thiết lập các điều kiện lọc (các filter độc lập, kết hợp AND)
3. Broadcast variant: user click「この条件で決定」→ preview section trong modal cập nhật (hiển thị preview + số người thỏa điều kiện「X人へ送信されます」) → user click「決定」để xác nhận
4. Các variant khác: user click「この条件で決定」→ `saveFilter()` được gọi → modal đóng
5. Ngoài modal: filter_control.blade.php hiển thị preview điều kiện + số người (`X人が対象`)
6. User có thể click「設定解除」để xóa toàn bộ filter

### Flow V2 (Modern)
1. User click nút mở modal (tên nút tùy context)
2. Modal full-screen xuất hiện
3. User chọn tab AND hoặc OR
4. User click nút loại filter ở left panel → condition card xuất hiện ở right area
5. User mở rộng card và cấu hình chi tiết
6. User có thể thêm nhiều điều kiện (mỗi lần click = thêm 1 card)
7. User click「保存」→ filter được lưu, modal đóng (gọi `closeModalFilterAction()`)
8. User có thể xóa từng điều kiện bằng nút trash icon trên card

### State trước/sau confirm
| Trạng thái | Mô tả |
|-----------|-------|
| Trước khi mở modal | Filter hiện tại hiển thị trong preview area (hoặc「条件なし（全員）」) |
| Trong modal (chưa confirm) | Thay đổi chưa có hiệu lực |
| Sau khi confirm (V1 saveFilter) | Filter được lưu vào state Vue/session; preview cập nhật; count cập nhật |
| Sau khi confirm (V2 保存) | Filter được serialize và gửi về server hoặc lưu state; modal đóng |
| Sau khi clearFilter | Filter xóa; preview reset về「条件なし（全員）」; count = 0 hoặc tổng số |

---

## 4. Danh sách Context Sử dụng

### V1 (basic/filter, basic/broadcast, basic/friendlist)
- Broadcast messaging (메시지 배포) — dùng broadcast variant
- Friendlist page — dùng friendlist variant
- Và các tính năng cũ khác dùng `@include('basic.filter.modal_filter')`

### V2 (layout/modal_filter_v2) — 61 files bao gồm:
| Nhóm tính năng | Files |
|----------------|-------|
| Broadcast | `broadcast/index_v2`, `broadcast/content_form`, `broadcast/v2/edit-broadcast` |
| Friendlist | `friendlist/index` |
| Step/Scenario | `step_message/index_v2`, `step_message/scenario_message`, `scenario/setting_add_friend_v2` |
| Auto-reply | `reply/create_v2` |
| Rich Menu | `rich_menu/v2/*` |
| QR Code | `qr_code/create`, `qr_code/v2/*` |
| Form | `form_answer/create_v2`, `form_answer/create_v3`, `form_answer/v3/edit` |
| Tag | `tag/index`, `tag/add_tag`, `tag/v2/*` |
| Conversion | `conversion/index`, `conversion/create` |
| Calendar/Booking | `calendar_management/*`, `calendar_salon/*`, `booking_manager/*`, `booking_event/*`, `booking_event_day/*` |
| Action Schedule | `action_schedules/*` |
| Cross Analysis | `cross_analysis/*` |
| CSV Management | `csv_management/create_download_file` |
| Chat | `chat/index`, `chats/chat_basic` |
| Setting Add Friend | `setting_add_friend/*` |
| Sales | `sales/add_item`, `sales/v2/add-single-item` |
| Events | `events/add_message` |
| Template | `message_template/add`, `template_v2/components/create-message` |
| Friend Info | `friend_information/create` |

---

## 5. Điểm chưa rõ / Cần xác nhận

1. **Vue data `marks`** (friendlist variant): định nghĩa marks động từ đâu? Server trả về qua API hay hardcode trong JS? Cần kiểm tra controller friendlist.
2. **`saveFilter()` logic** (V1): function này serialize data và lưu vào đâu? Session? Local state? Cần kiểm tra JS file tương ứng.
3. **V2 `保存` behavior**: function backend được gọi như thế nào khi save? Có AJAX request không?
4. **`type_parent_filter`**: biến này được truyền vào V2 như thế nào? Xác định context để ẩn/hiện filter types.
5. **`type_ignore` và `type_ignore_or`**: các giá trị mặc định là gì cho từng context?
6. **V2 OR conditions**: logic kết hợp AND và OR như thế nào khi query DB?
7. **「友だち情報」filter**: các field info được lấy từ đâu? Từ bảng custom fields?
8. **Count preview** (「X人が対象」trong V1): được tính realtime qua AJAX hay chỉ sau khi submit?

---

## 6. Screenshots

- `screenshots/filter-modal-v2.png` — Filter Modal V2 (friendlist context)
