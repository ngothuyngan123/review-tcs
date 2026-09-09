# UI Spec — SC-004 Action Settings (Modal アクション)

**ID Component:** SC-004  
**Tên:** Action Settings  
**Phiên bản:** 2025-05-20  
**Độ tin cậy tổng thể:** Cao (đọc trực tiếp từ source Blade)

---

## 1. Tổng quan

### Mô tả
SC-004 là shared component modal 「アクション」 cho phép Admin/Staff cấu hình một hoặc nhiều hành động tự động được thực thi khi một sự kiện xảy ra (người dùng nhấn nút, gửi tin nhắn, đáp lại auto-reply, v.v.). Mỗi action có thể kèm theo bộ lọc 「絞込」 để chỉ áp dụng cho nhóm bạn bè thỏa điều kiện.

### Mục đích
- Cho phép cấu hình nhiều hành động (multi-action) được thực thi theo thứ tự
- Hỗ trợ đa dạng loại action: gửi tin nhắn, gán tag, điều khiển step, cập nhật thông tin bạn bè, v.v.
- Mỗi action có thể áp dụng bộ lọc riêng (filter per action)

### Actors
- **Admin** — toàn quyền cấu hình
- **Staff** — tùy quyền được phân công

### Các tính năng sử dụng SC-004
- FA-001 Chat 1:1 (chat-1on1)
- FA-003 Auto Reply (auto-reply)
- FA-004 Broadcast/Step Message
- FA-009 Scenario (step delivery)
- FA-010 Rich Menu (action per button)
- FA-012 URL Tracking (action khi click link)
- FA-013 Form Answer (action khi submit form)
- FA-014 Bookmark
- FA-015 Action Schedule

---

## 2. Variants

Component tồn tại ở **3 variants** tương ứng 3 file Blade:

| Variant | File | Tên Modal | Mô tả |
|---------|------|-----------|-------|
| **V1** | `modal_setting_action.blade.php` | 「友だち一括操作」 | Legacy — dùng cho bulk action từ Friend List. 4 tabs cố định. Không hỗ trợ multi-action. |
| **V2** | `modal_select_action.blade.php` | 「アクション」 | Full action modal — sidebar trái chứa action type buttons, panel phải chứa config. Hỗ trợ multi-action + filter per action. **Đây là version chính.** |
| **V3** | `modal_select_action_pro.blade.php` | 「アクション編集」 | Pro edit version — dùng để chỉnh sửa action đã tạo. Bố cục tương tự V2 nhưng có section 「設定されたアクション」ở trên cùng. |

---

## 3. Màn hình SCR-ACT-01 — Modal V2: 「アクション」

**File:** `modal_select_action.blade.php`  
**DOM ID:** `#settingActionUrlModal` (bên trong `#vue_modal_action`)  
**Class modal:** `modal-dialog modal-lg multiple-action`

### 3.1 Layout tổng thể

```
+--------------------------------------------+
|  [X] nút đóng (góc phải trên)              |
|  アクション (tiêu đề modal)                   |
+------------------+-------------------------+
| Sidebar trái     | Panel phải              |
| (action buttons) | (config từng action)    |
|                  |                         |
| [+ ステップ]      | [danh sách actions đã   |
| [+ テンプレート]  |  thêm — v-for]          |
| [+ テキスト]      |                         |
| [+ リマインド]    |                         |
| [+ タグ]          |                         |
| [+ リッチメニュー]|                         |
| [+ ブックマーク]  |                         |
| [+ 友だち情報]    |                         |
| [+ 対応ステータス]|                         |
| [+ ブロック]      |                         |
+------------------+-------------------------+
| [保存]                                      |
+--------------------------------------------+
```

Ngoài ra có khu vực riêng ở trên cùng (trước sidebar) dành cho **action_only** — các action type đặc biệt chỉ có một action duy nhất (form_answer, booking, product_page, conversion, text_other, keywords, phone, email, add_friend). Khu vực này hiển thị v-if theo `action_only.type`.

### 3.2 Sidebar trái — Action Type Buttons

Mỗi button có:
- Icon `<i class="fal fa-plus-circle">` + tên action type
- CSS class `btn-add-action`
- Class `active_item` khi được chọn (`:class="{active_item: action_active=='scenario'}"`)
- Sự kiện `@click="addItem('type_key', 'Tên JP')`

| Button | Tên JP | `type_key` | Điều kiện hiển thị |
|--------|--------|------------|-------------------|
| ステップ | ステップ | `scenario` | Ẩn khi `type_action == 'step_message'` |
| テンプレート | テンプレート | `template` | Ẩn khi `type_action == 'broadcast_v2'` hoặc `'step_message'` |
| テキスト | テキスト | `text` | Ẩn khi `type_action == 'broadcast_v2'` hoặc `'step_message'` |
| リマインド | リマインド | `remind` | Ẩn khi `type_action` thuộc `listActionNotShowRemind` |
| タグ | タグ | `tag` | Luôn hiển thị |
| リッチメニュー | リッチメニュー | `richmenu` | Ẩn khi `type_action == 'richmenu'` |
| ブックマーク | ブックマーク | `bookmark` | Ẩn khi `type_action == 'bookmark'` |
| 友だち情報 | 友だち情報 | `friend_info` | Luôn hiển thị |
| 対応ステータス | 対応ステータス | `compliant_status` | Luôn hiển thị |
| ブロック | ブロック・非表示 | `block` | Luôn hiển thị |

### 3.3 Panel phải — Danh sách Actions (v-for)

Mỗi action trong list `actions` hiển thị theo `v-for="(item,indexAction) in actions"`. Mỗi item có 2 trạng thái:

#### Trạng thái thu gọn (`!item.is_edit_content`)
```
+----------------------------------------------+
| [Label tóm tắt action]  [絞込 未設定/設定済] [🗑] |
+----------------------------------------------+
```
- Label được render bởi `@include('layout.modal_setting.no_bracket_label_action')` — hiển thị mô tả ngắn action (ví dụ: `タグ タグ名をつける`, `ステップ 購読停止`)
- Button 「絞込 未設定」/「絞込 設定済」: toggle class `checkActionFilter(indexAction)` để mở modal filter
- Icon xóa `far fa-trash-alt` để xóa action

#### Trạng thái mở rộng (`item.is_edit_content`)
Hiển thị form config chi tiết theo `item.type`. Chi tiết từng action type ở mục 3.4.

---

### 3.4 Chi tiết config từng Action Type

#### 3.4.1 ステップ (Scenario) — `type == 'scenario'`

**Tiêu đề panel:** 「ステップ」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 配信設定 | `<select>` v-model `item.data.action` | 1=「停止」, 2=「開始/再開」, 3=「途中から配信」 |
| ステップ選択 | Combo-box (expand/collapse) | Hiển thị khi `item.data.action != 1`. Left: folder list (未分類 + `item.groups`). Right: radio list `item.group_items` |
| メッセージ選択 | `<input type="number">` + text 「日目のメッセージから配信」 | Hiển thị khi `item.data.action == 3`. Field: `item.data.start_day` |

**Validation:** `step_id_{indexAction}` required (khi action != 1)

---

#### 3.4.2 テンプレート (Template) — `type == 'template'`

**Tiêu đề panel:** 「送信するテンプレート」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| Folder picker | Menu bên trái | 未分類 + `item.groups` (click `initDataTemplate`) |
| Template picker | Radio list bên phải | `item.group_items` — radio chọn 1 template |

**Validation:** `template_id_{indexAction}` required  
**Hidden input:** `:name="'template_id_' + indexAction"` v-model `item.data.id`

---

#### 3.4.3 テキスト (Text) — `type == 'text'`

**Tiêu đề panel:** 「送信するテキスト」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 自動情報挿入 | Label (không phải input) | Header cho dropdown merge tags |
| LINE名挿入 | Button | `@click="addName(indexAction)"` — chèn tên LINE |
| 友だち情報 (dropdown) | Dropdown multi-level | Có 3 nhóm: 基本情報 (system_name, phone, email, birthday), 国内住所 (zip_code, province, district, township, building), Custom fields (`[FRIEND_INFO_{hash_id}]`) |
| 商品決済 (dropdown) | Dropdown — hiển thị khi `type_action == 'bill_item_v2'` | Items: PRODUCT_NAME, PRODUCT_ORDER_DATE, PRODUCT_AMOUNT_ORDER, PRODUCT_QUANTITY_ORDER, PRODUCT_ORDER_ID, PRODUCT_CYCLE |
| 予約 (dropdown) | Dropdown — hiển thị khi `show_booking_calendar` | Items: BOOKING_CALENDAR_reservation_name, reservation_currency, date_time, course, slot, url_confirm |
| 予約情報 (dropdown) | Dropdown — hiển thị khi `type_action == 'booking_event_day'` hoặc `'booking_event_day_plan'` | Items: EVENT_DAY_NAME, EVENT_DAY_DATE_START, EVENT_DAY_TIME_START_TIME_END, EVENT_DAY_NUMBER_BOOK, EVENT_DAY_AMOUNT_BILL |
| Emoji picker | Icon smile `fal fa-smile-o` | Chèn emoji vào textarea |
| Textarea | `<textarea>` v-model `item.data.content` | Max 5,000 ký tự. Counter: `count_text_content{indexAction}/5,000` |

**Validation:** `text_content_add_{indexAction}` required, max 5000

---

#### 3.4.4 リマインド (Remind) — `type == 'remind'`

**Tiêu đề panel:** 「リマインド」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 配信設定 | `<select>` v-model `item.data.type` | 1=「リマインド配信を開始」, 0=「リマインド配信を停止」 |
| リマインド選択 | Combo-box expand/collapse | Left: folder list (未分類 + groups). Right: radio list `item.group_items` — v-model `item.data.event_id` |
| 配信終了日時 | Date + Time input | Hiển thị khi `item.data.type == 1`. Date: `item.data.event_date` (type=date). Time: `item.data.event_start_time` (type=time). Text suffix: 「に配信終了」 |

**Validation:** `remind_ids_{indexAction}` required, `remind_date_ids_{indexAction}` và `remind_time_ids_{indexAction}` required (khi type=1)

---

#### 3.4.5 タグ (Tag) — `type == 'tag'`

**Tiêu đề panel:** 「タグ」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| Nút タグ新規追加 | Button success | Mở sub-modal `#modalAddTagModalAction` để thêm tag mới |
| Folder picker | Menu bên trái | 未分類(`count_default_tag`) + `groups_tag` |
| Tag picker | Checkbox list bên phải | Multi-select (`item.data.ids`). Có nút 「以下を全選択」 (select all trong folder). Hiển thị tags đã chọn ở khu vực `item.list_tags` với nút X để bỏ chọn |
| タグ操作 | `<select>` v-model `item.data.action` | 1=「つける」, 2=「はずす」 |

**Validation:** `tag_ids_{indexAction}` required  
**Sub-modal thêm tag mới** `#modalAddTagModalAction`:
- Chọn folder: `objectTag.folder_id` (未分類 + groups_tag)
- Nhập tên tag: `objectTag.tag_name` (max 50 ký tự, counter hiển thị)
- Nút 「保存してアクションに設定に戻る」 → `saveAddTag()` → quay lại modal chính
- Nút 「戻る」 → `backModalACtionFromAddTag()`

---

#### 3.4.6 リッチメニュー (Rich Menu) — `type == 'richmenu'`

**Tiêu đề panel:** 「リッチメニュー」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 表示設定 | `<select>` v-model `item.data.action` | 1=「表示を停止」, 2=「表示する」 |
| リッチメニュー選択 | Combo-box expand/collapse | Hiển thị khi `item.data.action == 2`. Left: folder (未分類 + groups). Right: radio list `item.group_items` — `chooseAction($event, indexAction, 'richmenu', groupItem.name)` |

**Validation:** `rich_menu_{indexAction}` required (khi action == 2)

---

#### 3.4.7 ブックマーク (Bookmark) — `type == 'bookmark'`

**Tiêu đề panel:** 「ブックマーク」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| Bookmark action | Radio group | value=1: 「ブックマークする」, value=2: 「ブックマークを外す」 |

**v-model:** `item.data.action` (`bookmark_{indexAction}`)

---

#### 3.4.8 友だち情報 (Friend Info) — `type == 'friend_info'`

**Tiêu đề panel:** 「友だち情報」  
**Các trường:**

**Bước 1 — Chọn field:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 友だち情報選択 | Combo-box expand/collapse | Left: folder (未分類, 基本情報, 国内住所, custom groups). Right: radio list `friend_items`. v-model `item.data.id` — `chooseFriendInfo($event, indexAction, friendItem.id)` |

Title phụ bên phải tùy theo `item.data.type`:
- type=1: 「選択肢」
- type=2: 「記述」
- type=3: 「年月日」
- type=6: 「ポイント」

**Bước 2 — Chọn thao tác (`item.data.type` xác định options):**

| `item.data.type` | Field type | Options |
|-----------------|------------|---------|
| 1 (選択肢) | `<select>` | 1=「登録されている情報を削除」, 2=「登録済みの選択肢から情報を登録」 |
| 2 (記述) | `<select>` | 1=「登録されている情報を削除」, 2=「以下の情報を登録」 |
| 3 (年月日) | `<select>` | 1=「登録されている情報を削除」, 2=「指定の日付を登録」, 3=「当日日付を登録」 |
| 6 (ポイント) | `<select>` | 0=「登録されている情報を削除」, 1=「ポイントを登録（上書き）する」, 2=「ポイントをプラス（＋）する」, 3=「ポイントをマイナス（－）する」 |

**Bước 3 — Nhập giá trị (tùy type và action):**

| Điều kiện | UI |
|-----------|-----|
| type=1 AND action=2 | Radio list chọn 1 giá trị từ `setting_actions` hoặc `valueOption` |
| type=2 AND action=2 | Textarea `content_info_text_{indexAction}` |
| type=3 AND action=2 | Date picker `content_info_date_{indexAction}` |
| type=3 AND action=3 | Không cần nhập (当日日付) |
| type=6 AND action != 0 | Radio 「指定」/「ランダム」. Nếu ランダム: 2 inputs từ/đến (from, to). Nếu 指定: 1 input số `content_info_point_{indexAction}` |

**Validation:** `friend_info_{indexAction}` required

---

#### 3.4.9 対応ステータス (Compliant Status) — `type == 'compliant_status'`

**Tiêu đề panel:** 「対応ステータス」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| 対応ステータス設定 | `<select>` v-model `item.data.action` | 1=「ステータスをつける」, 2=「ステータスを外す」 |
| 対応ステータス選択 | `<select>` v-model `item.data.id` | Hiển thị khi action=1. Options từ `status_setting` (mảng {id, name_status}). `@change="chooseStatus($event,indexAction)"` |

**Validation:** `compliant_status_{indexAction}` required, `compliant_id_{indexAction}` required (khi action=1)

---

#### 3.4.10 ブロック (Block) — `type == 'block'`

**Tiêu đề panel:** 「ブロック・非表示」  
**Các trường:**

| Field | Type | Options/Logic |
|-------|------|---------------|
| Block action | Radio group | 1=「ブロックする」, 2=「ブロック解除」, 3=「表示」, 4=「非表示」 |

**v-model:** `item.data.action` (`action_open_type_{indexAction}`)

---

### 3.5 Filter Per Action (Bộ lọc từng action)

Mỗi action có button 「絞込」:
- Text khi chưa đặt: 「絞込 未設定」 (CSS class `without-filter`)
- Text khi đã đặt: 「絞込 設定済」 (CSS class `has-filter`)
- Class toggle: `checkActionFilter(indexAction)` — check xem action tại indexAction có filter chưa
- Sự kiện: `v-on:click.stop="openModalFilter(indexAction)"` — mở modal filter riêng (SC-005 Friend Filter, modal khác)

---

### 3.6 Action Only Zone — Các action type đặc biệt

Hiển thị ở phần trên cùng, trước sidebar. Chỉ xuất hiện khi `action_only` tồn tại và `action_only.type` match. Các type này không thể kết hợp với action khác (single action only):

| `action_only.type` | Tên hiển thị | Cấu hình |
|-------------------|--------------|----------|
| `form_answer` | 「フォーム作成」 | Select từ `form_answers` (id, name) |
| `booking` | 「イベント予約」 | Select từ `bookings` (id, title) |
| `product_page` | 「商品ページ」 | Select từ `products` (id, name) |
| `conversion` | 「CV登録ページ」 | Select từ `conversions` (id, name) |
| `text_other` | 「テキストを送信させる」 | Textarea, max 5000 ký tự |
| `keywords` | 「キーワードを送信させる」 | Select từ `keywords` (id, keyword) |
| `phone` | 「電話をかけさせる」 | Input number, validation `phone_number` |
| `email` | 「メールを送る」 | Input email, validation `email` |
| `add_friend` | 「紹介したいLINE公式アカウントの友だち追加ページが開く」 | Input text LINE ID (placeholder `@abc123`) |

Mỗi action_only có nút X (`@click="removeActionOther()"`) để xóa.

---

### 3.7 Nút hành động

Nằm ở `div.modal-bottom` cuối modal:

| Nút | Hiển thị khi | Sự kiện |
|-----|-------------|---------|
| 「保存」 | `type_action` không thuộc: button, image_map, video, formAnswer_setting_action, formAnswer_diagnostic_content, add_friend_new, và không phải preview-chat11 | `saveSettingAction()` |
| 「保存」 (button variant) | `type_action == 'button'` | `saveSettingActionButton()` |
| 「保存」 (image_map variant) | `type_action == 'image_map'` | `saveSettingActionImageMap()` |
| 「保存」 (video variant) | `type_action == 'video'` | `saveSettingActionVideo()` |
| 「保存」 (formAnswer variant) | `type_action == 'formAnswer_setting_action'` hoặc `'formAnswer_diagnostic_content'` | `saveSettingActionFormAnswer()` |
| 「保存」 (add_friend_new variant) | `type_action == 'add_friend_new'` | `saveSettingAction()` |

Nút đóng modal: `<button type="button" class="close" data-dismiss="modal">` (icon X góc phải)

**Hidden inputs** (context truyền vào từ trang gọi modal):
- `#action_idx`, `#plan_key`, `#plan_key_slot`, `#button_tab_id`, `#button_index`, `#tmp_number`, `#type_image_map`, `#type_calendar`, `#index_calendar`, `#type_bill_item`, `#type_add_friend`, `#type_add_action_tag`, `#type_action_qrcode`

---

## 4. Màn hình SCR-ACT-02 — Modal V1: 「友だち一括操作」(Legacy)

**File:** `modal_setting_action.blade.php`  
**DOM ID:** `#settingActionUrlModal`  
**Class modal:** `modal-dialog modal-lg`

### 4.1 Layout

```
+--------------------------------------------+
| 友だち一括操作 (tiêu đề)                     |
| [mô tả: 選択した友だちのステップ停止変更や...]  |
+--------------------------------------------+
| [テンプレート送信] [ステップ] [タグ] [リッチメニュー] |
+--------------------------------------------+
| [Nội dung tab tương ứng]                   |
+--------------------------------------------+
| [閉じる]  [この条件で決定する]               |
+--------------------------------------------+
```

### 4.2 4 Tabs

#### Tab 1: テンプレート送信 (`#menu1`, active mặc định)
- Left panel: Folder list template (未分類 + groups từ `groups`) — click `showGroup(id)`
- Right panel (`.choice_detail`):
  - Radio 「選択しない」(value=0) — `showTemplate()`
  - Radio list templates từ folder đã chọn (`items_default` hoặc `items['templates']`)
  - v-model `checked`

#### Tab 2: ステップ (`#menu2`)
- Select 「ステップを購読」: `#scenario_id`
  - Option 「変更しない」(value=-1)
  - Option 「購読中止・予約キャンセル」(value=0)
  - Options từ `$scenario` (PHP foreach)
- Radio 「（新規）最初から/（再開）読んだところから」(value=0, checked)
- Radio 「途中から始める」(value=1) + Input number `#start_day` (日目)
- Sử dụng jQuery datepicker/timepicker

#### Tab 3: タグ (`#menu3`)
- Left: Folder list tag (未分類 + `sortedCategories`) — click `showGroup(id, 'third')`
- Right (`.choice_detail`):
  - Radio 「タグを選択しない」(value=0)
  - Radio list tags từ folder đã chọn (`items_default` hoặc `tag_items`)
  - v-model `checked`

#### Tab 4: リッチメニュー (`#menu4`)
- Select `#rich_menu`, name=`select_rich_menu`
  - Option 「選択しない」(value=0)
  - Options từ `$richMenus` (PHP foreach)

### 4.3 Nút hành động
- 「閉じる」: `data-dismiss="modal"`, onclick=`cancelSettingAction()`
- 「この条件で決定する」: onclick=`saveSettingAction()`

---

## 5. Màn hình SCR-ACT-03 — Modal V3: 「アクション編集」(Pro)

**File:** `modal_select_action_pro.blade.php`  
**DOM ID:** `#settingActionUrlModal`  
**Tiêu đề:** 「アクション編集」

### 5.1 Sự khác biệt so với V2

- Có section 「設定されたアクション」ở trên cùng — tiêu đề kiểu `.title-setting`
- Hỗ trợ cả `action_only` (các type đặc biệt: form_answer, booking, product_page, conversion, text_other, keywords, phone, email, add_friend)
- Phần action list (`#list_action_common`): `float: right; width: calc(100% - 200px); height: 80vh`
- Phần scenario action dùng `$scenario` PHP foreach (không dùng Vue combo-box như V2)
- Phần template action dùng dropdown Bootstrap (không phải combo-box)
- Phần text action: chỉ có nút 「友だち名挿入」, không có merge tag dropdown phức tạp như V2
- Phần remind action: select flat (không có combo-box folder), options từ `list_remind`
- Phần tag action: checkbox list với folder nav bên trái (style cũ, không dùng `item.group_open_tag`)

### 5.2 Điểm giống V2
- Các action type giống nhau: scenario, template, text, remind, tag, richmenu, bookmark, friend_info, compliant_status, block
- `action_only` zone giống hệt V2
- Label tóm tắt dùng `@include('layout.modal_setting.label_action')` (có dấu ngoặc 【】)

---

## 6. User Flows

### 6.1 Happy path — Thêm 1 action

```
1. Trang cha trigger mở modal (set hidden inputs + call Vue data)
2. Modal mở → user thấy sidebar trái (action type buttons) + panel phải trống
3. User click button action type (ví dụ: [+ タグ])
   → item mới được thêm vào `actions` array
   → panel phải hiển thị form config action "タグ"
   → button sidebar highlight (class active_item)
4. User cấu hình action:
   - Chọn folder tag (bên trái)
   - Check các tag (bên phải)
   - Chọn タグ操作 (つける/はずす)
5. User click 「保存」
   → `saveSettingAction()` được gọi
   → data được serialize và lưu về trang cha
   → modal đóng
```

### 6.2 Multi-action flow

```
1. User click button type 1 → action 1 được thêm → configure
2. User click button type 2 → action 2 được thêm → configure
   (Cả 2 action hiển thị trong list, mỗi action có expand/collapse riêng)
3. User click vào label tóm tắt của action thu gọn → mở rộng để chỉnh sửa
4. User nhấn 「保存」 → lưu toàn bộ actions array
```

### 6.3 Filter flow

```
1. User đã thêm action
2. User click 「絞込 未設定」 button trên action đó
   → `openModalFilter(indexAction)` được gọi
   → Modal filter (SC-005) mở
3. User cấu hình filter conditions trong modal filter
4. Xác nhận → quay lại modal action
5. Button đổi thành 「絞込 設定済」 (class thay đổi)
```

### 6.4 Thêm tag mới inline

```
1. Trong action type "タグ", user click [タグ新規追加]
   → Sub-modal #modalAddTagModalAction mở (overlay)
2. User chọn folder + nhập tên tag (max 50 ký tự)
3. User click 「保存してアクションに設定に戻る」
   → `saveAddTag()` → tag mới được thêm, modal action quay lại
4. Tag mới xuất hiện trong list để chọn
```

---

## 7. Context Modes (tham số `type_action`)

Tham số `type_action` được set từ trang cha qua Vue data. Giá trị này quyết định action buttons nào hiển thị và nút 「保存」 nào được gọi:

| `type_action` | Mô tả ngữ cảnh | Action bị ẩn |
|--------------|----------------|-------------|
| `reply` | Auto-reply action | (không ẩn đặc biệt) |
| `broadcast_v2` | Broadcast v2 action | テンプレート, テキスト |
| `step_message` | Step message action | ステップ, テンプレート, テキスト |
| `richmenu` | Rich menu button action | リッチメニュー |
| `bookmark` | Bookmark action | ブックマーク |
| `booking_event_day` | Event booking day action | — (hiện thêm merge tag 予約情報) |
| `booking_event_day_plan` | Event booking day plan | — (hiện thêm merge tag 予約情報) |
| `bill_item_v2` | Bill/product action | — (hiện thêm merge tag 商品決済) |
| `button` | Template button action | — (nút 「保存」 dùng `saveSettingActionButton()`) |
| `image_map` | Image map area action | — (nút 「保存」 dùng `saveSettingActionImageMap()`) |
| `video` | Video action | — |
| `formAnswer_setting_action` | Form answer action | — |
| `formAnswer_diagnostic_content` | Form diagnostic content | — |
| `add_friend_new` | Add friend action | — |
| `preview-chat11` | 1:1 chat preview | — (nút 「保存」 bị disabled) |

---

## 8. Label Components

### `label_action.blade.php` — Label với dấu 【】
Dùng trong V3 (pro). Render dạng: `【タグ】 タグ名をつける`, `【ステップ】 シナリオ名`, v.v.

### `no_bracket_label_action.blade.php` — Label không có 【】
Dùng trong V2 (main). Render dạng: `タグ タグ名をつける`, `ステップ 購読停止・予約キャンセル`, v.v.

**Mapping label theo type:**

| `item.type` | Label title | Nội dung tóm tắt |
|-------------|-------------|-----------------|
| `tag` | 「タグ」 | `{tag names}を{つける/はずす}` |
| `scenario` | 「ステップ」 | `{scenario_name}` hoặc 「購読停止・予約キャンセル」 |
| `template` | 「テンプレート」 | `{template_name}` |
| `text` | 「テキスト」 | `{content | shortContent}` |
| `richmenu` | 「リッチメニュー」 | `{richmenu_name}表示` hoặc 「表示を停止」 |
| `remind` | 「リマインド」 | `{remind_name}` |
| `bookmark` | 「ブックマーク」 | 「ブックマークする」/「ブックマークを外す」 |
| `block` | 「ブロック・非表示」 | 「ブロックする」/「ブロック解除」/「表示」/「非表示」 |
| `compliant_status` | 「対応ステータス」 | `{name}をつける` hoặc 「ステータスを外す」 |
| `friend_info` | 「友だち情報」 | Tùy type và action (xem label_action.blade.php) |

---

## 9. Screenshots

- `screenshots/friendlist-bulk-action.png` — Màn hình Friend List với bulk action panel (V1 legacy context)

---

## 10. Điểm chưa rõ — Cần điều tra thêm

1. **Modal Filter (SC-005)** — `openModalFilter(indexAction)` mở modal nào? Chưa xác định file Blade tương ứng. Cần tìm file modal filter trong `modal_setting/`.
2. **`listActionNotShowRemind`** — Mảng các `type_action` không hiển thị button リマインド. Cần tìm trong JS file `/js/select_action.js`.
3. **`show_booking_calendar`** — Biến Vue quyết định hiển thị dropdown 予約 trong text action. Cần tìm logic khởi tạo trong JS.
4. **`saveSettingAction()` logic** — JS function serialize data `actions` array thế nào? Cần đọc `/js/select_action.js` để biết data format gửi về trang cha.
5. **`type_action` được set từ đâu** — Khi trang cha mở modal, set `type_action` qua mechanism nào (custom event? global var?). Cần trace trong từng tính năng sử dụng.
6. **Validation framework** — Dùng `vee-validate` (import từ `/js/form_answer/vee-validate.rc7.min.js`). Custom rule `phone_number` cần điều tra logic.
7. **`chooseStatus` function** — Khi chọn対応ステータス, `item.data.content` được set thế nào? Cần đọc JS.
8. **`chooseFriendInfo` function** — Khi chọn friend info field, `item.data.type` được set từ đâu (data của field từ server hay hardcode)?
9. **Limit số lượng actions** — Không thấy giới hạn max số actions trong Blade. Có thể có validate ở JS.
10. **`action_only` vs `actions`** — Hai state này có thể tồn tại đồng thời không, hay loại trừ nhau?
