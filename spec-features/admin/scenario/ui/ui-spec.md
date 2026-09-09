# UI Spec — FA-009: Phát hành theo bước 「ステップ配信」

> Tạo từ source code (UI không truy cập được — subscription required)
> Nguồn: blade templates + controller + routes
> Mức độ tin cậy chung: **Cao** (phân tích trực tiếp từ blade templates)

---

## Tổng quan

「ステップ配信」 (Step Delivery / Phát hành theo bước) là tính năng cho phép Admin tạo các kịch bản gửi tin nhắn tự động đến bạn bè (LINE users) theo trình tự và thời gian định sẵn. Mỗi kịch bản (scenario) chứa nhiều bước (steps), mỗi bước có thời điểm gửi và nội dung tin nhắn riêng.

Hệ thống hỗ trợ hai phiên bản giao diện:
- **v1** (cũ): `scenario_index.blade.php` + `index.blade.php` — được dùng trực tiếp (controller trả về `scenario_index`)
- **v2** (mới): `index_v2.blade.php` + thư mục `v2/` — giao diện nâng cấp, được load từ `index_v2`

---

## Actors

- **Admin**: Toàn quyền tạo/sửa/xóa scenario và step messages
- **Staff**: Quyền tùy theo cấu hình role — không phân biệt trong blade templates (không có điều kiện phân quyền rõ ràng trong blade)

---

## Màn hình

### SCR-SCE-01: Danh sách Scenario 「ステップ配信（一覧）」

- **URL**: `/basic/scenario` (GET)
- **Controller**: `Basic\ScenarioController@index`
- **View**: `basic.scenario.scenario_index`
- **Mức độ tin cậy**: **Cao**

#### Layout tổng thể

Màn hình chia làm 2 cột ngang (`.body_separate`):
1. **Cột trái**: Danh sách folder (`.scenario_folder_list`)
2. **Cột phải**: Danh sách scenario trong folder đang chọn (`.scenario_item_list`)
3. **Thanh action dưới**: Nút bulk action + pagination

Tiêu đề trang: 「ステップ配信」
Mô tả trang: 「ステップ配信とは、友だちに対し事前に準備したメッセージを、設定した順番と間隔で自動的に配信する機能です。」

#### Panel Folder (cột trái)

- Nút 「フォルダ追加」: mở form tạo folder inline (input field 管理名, tối đa 15 ký tự + nút 決定/キャンセル)
- Nút 「並べ替え」: mở modal sắp xếp folder `#modalSortFolder`
- Folder mặc định: 「未分類」 hiển thị số lượng item trong ngoặc — `(@{{ count_default }})`
- Danh sách folder: hiển thị tên và số lượng — `@{{ category.name }} (@{{ category.count }})`
- Folder đang active có class `.active`
- Mỗi folder (trừ 未分類) có menu hành động (hiện khi click `...`):
  - 「名称変更」: đổi tên folder
  - 「フォルダ削除」: xóa folder (mở modal xác nhận)
- Toggle ẩn/hiện panel folder qua nút ở thanh action dưới

#### Toolbar trên danh sách Scenario

- Nút 「新規作成」 (xanh lá): mở modal `#modalCreateScen` tạo scenario mới
- Nút 「並べ替え」: mở modal `#sorter_modal_v1` sắp xếp scenario
- Hiển thị đếm khi có item được chọn: 「このフォルダ内の N 件が選択されています」
- Ô tìm kiếm: placeholder 「管理名を入力」, tìm kiếm khi Enter, có nút xóa nội dung tìm kiếm

#### Bảng danh sách Scenario

| Cột | Label JP | Mô tả |
|-----|----------|-------|
| Checkbox | — | Chọn nhiều item để bulk action |
| Tên | 管理名 | Tên quản lý của scenario, click vào để vào trang chi tiết |
| Đang đọc | 購読中の友だち | Số bạn bè đang theo dõi (N人) + nút 「表示」 xem danh sách |
| Chưa hoàn thành | 途中で終了した友だち | Số bạn bè đã dừng giữa chừng (N人) + nút 「表示」 |
| Đã đọc xong | 読了済の友だち | Số bạn bè đã hoàn thành (N人) + nút 「表示」 |
| Action | — | Menu 「...」 (horizontal dots) → コピー / 削除 |

Click vào tên scenario → redirect sang `redirectPageEdit(item.id)` — tức là trang step messages của scenario đó.

Click 「表示」 trên số lượng bạn bè → mở trang danh sách bạn bè theo trạng thái:
- 「表示」 trên 購読中 → `showFriendFollow(item)`
- 「表示」 trên 途中で終了した → `showFriendUnfinish(item)`
- 「表示」 trên 読了済 → `showFriendComplete(item)`

#### Thanh action dưới (`.scenario_body_action`)

- Nút toggle ẩn/hiện folder panel
- Nút 「一括フォルダ変更」: chuyển folder hàng loạt (cần chọn item, mở modal `#modalMoveFolder`)
- Nút 「一括削除」: xóa hàng loạt (cần chọn item, mở modal `#modalBulkDeletion`)
- Pagination: chuyển trang, chọn số item mỗi trang (10/20/50/100/page)

#### Modals trong SCR-SCE-01

**Modal tạo Scenario mới** (`#modalCreateScen`):
- Tiêu đề: 「ステップ配信 新規作成」
- Field 「管理名」: text input, tối đa 20 ký tự (`v-model="text_length"`, hiển thị đếm ký tự)
- Field 「フォルダ」: dropdown select, mặc định 「未分類」, liệt kê các folder đang có
- Checkbox 「フォルダ内の一番上に追加する」: thêm vào đầu danh sách (mặc định: thêm cuối)
- Ghi chú: 「※ 未選択の場合、フォルダの一番下に追加されます」
- Nút submit: 「メッセージの登録に進む」→ form POST redirect sang trang step messages

**Modal sắp xếp Folder** (`#modalSortFolder`):
- Tiêu đề: 「【 フォルダ並べ替え 】」
- Kéo thả hoặc dùng popup menu: 「一番上に移動」/ 「一番下に移動」
- Nút 「変更を保存」

**Modal tạo/sửa Folder** (`#modalCreateOrUpdateFolder`):
- Tiêu đề: 「フォルダ作成・編集」
- Field 「フォルダ名」: text input, tối đa 15 ký tự
- Nút 「変更を保存」

**Modal xác nhận xóa Folder** (`#modalConfirmDeleteFolder`):
- Tiêu đề: 「フォルダ削除」
- Nội dung: 「フォルダを削除した場合、フォルダ内のコンテンツもすべて削除されますがよろしいですか？」
- Nút: 「フォルダを削除」

**Modal sắp xếp Scenario** (`#sorter_modal_v1`):
- Tiêu đề: 「並べ替え」
- Kéo thả hoặc dùng popup menu: 「一番上に移動」/ 「一番下に移動」
- Nút 「変更を保存」

**Modal chuyển Folder hàng loạt** (`#modalMoveFolder`):
- Tiêu đề: 「【 一括フォルダ変更 】」
- Chọn folder đích: dropdown (「未分類」 + danh sách folder)
- Nút: 「登録」

**Modal xóa hàng loạt** (`#modalBulkDeletion`):
- Tiêu đề: 「一括削除」
- Hiển thị đối tượng đang chọn, cảnh báo xóa vĩnh viễn
- Nút: 「全て削除」 / 「キャンセル」

---

### SCR-SCE-02: Danh sách Step Message 「ステップ配信メッセージ」 (v1 — cũ)

- **URL**: `/step-message/list-message/{scenario}` (GET) — hoặc redirect sau khi tạo scenario
- **Controller**: `Basic\StepMessageController@listMessage`
- **View**: `basic.step_message.index`
- **Mức độ tin cậy**: **Cao** (đây là view v1, có thể đã thay bằng v2)

#### Layout

- Tiêu đề: `【{tên scenario}】ステップ配信メッセージ`
- Toolbar: Nút 「新規メッセージ登録」 (link → create) + Nút 「テンプレートから追加」 (mở modal custom)
- Bảng danh sách step messages

#### Bảng danh sách (v1)

| Cột | Label JP | Mô tả |
|-----|----------|-------|
| Checkbox | — | Chọn nhiều item |
| Thời điểm gửi | 配信日程 | `start_date` + `order_number`通目 |
| Nội dung | 本文 | Hiển thị tùy loại tin nhắn (text/image/stamp/question/form/location/introduction/video/voice/group) |
| Số người nhận | 到達人数 | Link sang `/scenario-users?scenarioId=X&stepId=Y` |
| Nút sửa/copy | — | 「編集」 (link /basic/step-message/edit/{id}) + 「コピー」 |
| Preview/Test | — | Nút 「プレビュー」 + Link 「テスト」 |
| Xóa | — | Link 「削除」 (đỏ) |

Loại nội dung tin nhắn hiển thị trong cột 本文:
- `text`: nội dung text, có thể kèm RichMenu badge
- `image`: 「【画像】」 + thumbnail
- `stamp`: 「【スタンプ】」 + ảnh sticker
- `question`: 「【質問】」 + nội dung
- `form`: 「カルーセル 【カルーセル】」 + text button
- `location`: 「【位置情報】」 + nội dung
- `introduction`: 「【紹介】」 + friend name + nội dung
- `video`: 「動画【動画】」
- `voice`: 「【音声】」
- `group`: 「メッセージパック」 + tên

RichMenu badge hiển thị khi `item.rich_menu_id` có giá trị:
- `rich_menu_id != -1`: tên rich menu + 「リッチメニュー」
- `rich_menu_id == -1`: 「リッチメニュー解除」

Bulk delete khi có item được chọn → 「チェックしたメッセージを 削除」

---

### SCR-SCE-03: Danh sách Step Message 「ステップ配信メッセージ」 (v2 — mới)

- **URL**: (redirect sau tạo scenario, hoặc từ click tên scenario ở SCR-SCE-01)
- **Controller**: `Basic\StepMessageController` (các action v2)
- **View**: `basic.step_message.index_v2`
- **Mức độ tin cậy**: **Cao**

#### Layout tổng thể

- Tiêu đề: `【{tên scenario}】ステップ配信メッセージ`
- Phần filter/배信対象 (section-filter) — chọn đối tượng nhận
- Thanh toolbar action (top-action-common) — thêm step, bulk preview, pagination
- Danh sách step items (item-step lặp lại)

#### Phần Đối tượng gửi (Filter — section-filter)

- Nhãn: 「選択中の配信対象」
- Mặc định: 「ステップ購読者全員」 (toàn bộ subscriber)
- Có thể thêm nhiều đối tượng lọc (Filter Manager):
  - Tên quản lý (任意)
  - Nút 「絞り込み条件 編集」 → mở modal chỉnh sửa điều kiện lọc
  - Nút 「配信対象削除」
  - Hiển thị preview các điều kiện lọc đang áp dụng
- Nút 「配信対象追加」 để thêm filter mới

#### Thanh toolbar (top-action-common)

- Nút 「配信タイミング」 (xanh): thêm bước mới (tối đa 100 bước/filter)
  - Khi đạt 100: 「1つの配信対象に登録できる配信タイミングは100までです。」
- Nút 「一括プレビュー」: xem preview toàn bộ steps
- Selector 「表示件数」: chọn số items/trang
- Pagination: hiển thị `N~M / total件`, nút prev/next
- Nút 「一括操作」: mở menu bulk operations (bên phải)

#### Item Step (item-step.blade.php)

Mỗi step hiển thị:

**Header (infor_input)**:
- Số thứ tự step: số index + 1
- Thời điểm gửi (click để sửa):
  - `delay_type == 1`: 「ステップ開始直後」
  - `delay_type == 0`: `N日後HH:MM`
  - `delay_type == 2`: `N時間M分後`
- Tên step (`.step-name`): `@{{ step.name }}`
- Quick test users: danh sách avatar user để gửi test nhanh
- Số người đã nhận: 「配信済 N人」 (link sang `/scenario-users?scenarioId=X&stepId=Y`)
- Nút 「≡」 mở action menu cho step

**Nội dung Step (message_and_action)**:

Phần thêm tin nhắn (`.step_add_message`):
- Nút 「+ メッセージ」: thêm tin nhắn mới (redirect sang `/basic/template-v2/add-template`)
- Nút 「+ テンプレート」: chọn từ template có sẵn (mở modal `#templateModal`)
- Bảng danh sách messages trong step:
  - Icon loại message (text/form/image/video/voice/stamp/location/introduction/group)
  - Preview nội dung message (text, hình ảnh, v.v.)
  - Nút preview/test (icon play)
  - Nút 「...」 → menu: 上に移動 / 下に移動 / 削除

Phần Action (`.step_add_action`):
- Toggle 「エルメアクション設定」: ẩn/hiện panel cài đặt action
- Khi đã có action: 「エルメアクション N件設定済」
- Nút 「アクション登録・編集」: mở modal cài đặt actions cho step

**Sau step cuối cùng**: Nút 「配信タイミング追加」 để thêm step mới (v1)

#### Modal chọn thời điểm gửi (`.modal-edit-step`)

- Tiêu đề: 「配信タイミング」
- 3 lựa chọn:
  - 「ステップ開始直後」 (delay_type = 1)
  - 「日時で指定」 (delay_type = 0): nhập số ngày + giờ (input số ngày `start_day` + input time `start_time`)
  - 「経過時間で指定」 (delay_type = 2): nhập thời gian (input time `start_time`, đơn vị phút)
- Ghi chú: 「ステップ開始時からの経過日数と時間で配信タイミングを指定します / （0日後はステップ開始当日を指します）」
- Nút 「決定」 (xanh) lưu

#### Modal chọn Template (`#templateModal`)

- Tiêu đề: 「テンプレート選択」
- Cột trái: danh sách folder (「未分類」 + folder theo danh sách)
- Cột phải: danh sách template trong folder đã chọn (radio button)
- Nút 「決定」 thêm template vào step
- Nút 「プレビュー」 xem trước template

#### Modal xem trước Template (`#templateDetail`)

- Tiêu đề: `[{tên template}] プレビュー`
- Hiển thị nội dung tùy loại: text, image, stamp, question, form (carousel), location, introduction, video, voice, group
- Nút 「戻る」 đóng

#### Modal sắp xếp Step (partial `modal_sort`)

- Sắp xếp thứ tự các messages trong step

#### Modal cài đặt Profile gửi (`#setProfileModal`)

- Tiêu đề: 「【送信スタッフ設定】」
- Tạo/chọn profile gửi (avatar + tên nhân viên)
- Ghi chú: 「友だちのトーク画面にはスタッフ名 from 'LINE公式アカウント名'という形で表示されます。」
- Danh sách profile đã tạo với radio chọn
- Nút 「保存」

#### Modal xác nhận thêm Template (`#confirmAddTemplate`)

- Hai lựa chọn:
  - 「テンプレートをそのまま利用する」: dùng nguyên template (khi template gốc thay đổi → tự động áp dụng)
  - 「テンプレートを引用して編集する」: sao chép để sửa riêng (template gốc thay đổi không ảnh hưởng)
- Nút 「テンプレート選択」 → tiếp tục chọn template

---

### SCR-SCE-04: Tạo/Chỉnh sửa Step Message 「配信メッセージ登録」

- **URL tạo mới**: `/basic/step-message/store/{scenario}` (POST) — form submit
- **URL chỉnh sửa**: `/basic/step-message/edit/{step_message}/{template_id}` (GET)
- **URL mới v2**: `/basic/template-v2/add-template?template_group_id={step_id}&action_type=scenario&scenario_id={scenario_id}`
- **Controller**: `Basic\StepMessageController@store` / `@update` / `@edit`
- **View**: `basic.step_message.create`
- **Mức độ tin cậy**: **Cao**

#### Layout

- Tiêu đề: 「配信メッセージ登録」
- Tối đa 3 bộ nội dung (Tab 1, Tab 2, Tab 3) — mỗi bộ là 1 message

#### Tab chọn loại nội dung

Khi tạo mới, hiển thị các tab (tùy bot_type):
- 「テキスト」 (text)
- 「質問・ボタン」 (form) — chỉ khi bot_type == 0
- 「メディア」 (image/voice/video)
- 「スタンプ」 (stamp) — chỉ khi bot_type == 0
- 「位置情報」 (location) — chỉ khi bot_type == 0
- 「紹介」 (introduction) — chỉ khi bot_type == 0

Khi chỉnh sửa, tab bị khóa (pointer-events: none) theo loại đang có.

Đặc biệt nếu type là `group` (メッセージパック): hiển thị tên template + link 「テンプレートを編集する」.

#### Form Text (tab テキスト)

- Textarea nội dung `text_content` (tối đa 5000 ký tự)
- Hỗ trợ `{name}` → tên người nhận
- Nút 「URL設定」: phát hiện URLs trong nội dung → cấu hình URL settings
- Công cụ: 「PDFアップロード」

**Cấu hình URL** (khi có URL trong message):
- Toggle 「表示期限設定を利用しない」
- Khi bật:
  - Chọn loại period: 「日時指定」 (ngày/giờ cụ thể) hoặc 「経過日数指定」 (số ngày sau gửi)
  - 「期限到来後設定」: 「リダイレクトURL設定」 hoặc 「テキストページ表示設定」
- Nút 「アクションを設定する」: cài đặt action khi click URL (tag/scenario/rich menu)
- Nút 「設定する」 lưu / 「閉じる」 hủy

#### Nút submit

- 「登録」 (xanh, lớn) — submit form

#### Fields ẩn quan trọng

- `scenario_step_id`, `step_message_id`
- `template_id`, `template_id_2`, `template_id_3`
- `tmp_type[]`, `tmp_content[]`, `tmp_is_shorten_url[]`
- `media_path[]`, `thumbnail_path[]`
- `botIdCurrent`
- Nhiều fields cho question/button/carousel/URL redirect config

---

### SCR-SCE-05: Cài đặt Scenario 「ステップ配信設定」

- **URL**: `/scenario-setting` (GET) / `/basic/scenario-setting` (POST)
- **Controller**: `Basic\ScenarioController@setting` / `@updateSetting`
- **View**: `basic.scenario.setting`
- **Mức độ tin cậy**: **Cao**

#### Layout

- Tiêu đề: 「ステップ配信設定」
- Mô tả: 「友だち登録時に開始するステップ・タグの設定」
- Chia 2 cột: 「新規友だち」 và 「システム導入前からの友だち・アカウントへのブロックを解除した友だち」

#### Mỗi cột cấu hình (dùng cho cả New và Old friends)

- **ステップ**: dropdown chọn scenario để tự động subscribe (hoặc 「購読しない」)
- **ステップを購読する場合**: Radio chọn cách bắt đầu:
  - 「最初から始める」 (từ đầu)
  - 「途中から始める」 (từ giữa): nhập số ngày + giờ
- **タグ** (任意): chọn tag để gán khi subscribe (phân theo category/folder)

Nút submit cuối form (không hiển thị trong đoạn code xem được — Suy luận từ source code)

---

### SCR-SCE-06: Danh sách Bạn bè theo Scenario

- **URL**: `/scenario-users?scenarioId={id}&stepId={id}` (GET)
- **Controller**: `Basic\ScenarioController@getListFriendByScenarioId`
- **Mức độ tin cậy**: **Trung bình** (chỉ thấy URL từ links trong blade, không có view file)

---

## User Flows

### Flow 1: Tạo Scenario mới

1. Từ SCR-SCE-01 click 「新規作成」 → mở modal `#modalCreateScen`
2. Nhập 「管理名」 (tối đa 20 ký tự) + chọn folder + tùy chọn vị trí thêm (đầu/cuối)
3. Click 「メッセージの登録に進む」 → POST `/basic/scenario/store-scenario/store` → redirect sang SCR-SCE-03 (v2) hoặc SCR-SCE-02 (v1)

### Flow 2: Quản lý Folder

1. Từ SCR-SCE-01, click 「フォルダ追加」 → hiện form inline → nhập tên → 「決定」
2. Click folder → lọc scenario trong folder
3. Hover folder active → hiện icon 「...」 → 「名称変更」 / 「フォルダ削除」

### Flow 3: Thêm Step mới vào Scenario

1. Từ SCR-SCE-03, click 「配信タイミング」
2. Modal cài đặt thời điểm → chọn loại: bắt đầu ngay / chỉ định ngày / chỉ định thời gian
3. Nhập thông số thời gian → click 「決定」 → POST `/scenario/save-scenario-step`

### Flow 4: Thêm tin nhắn vào Step

1. Từ SCR-SCE-03, trong 1 step, click 「+ メッセージ」
   - → redirect sang `/basic/template-v2/add-template` với params
2. Hoặc click 「+ テンプレート」 → modal xác nhận cách thêm → chọn template → click 「決定」

### Flow 5: Chỉnh sửa tin nhắn trong Step

1. Click vào message trong danh sách → icon loại hoặc vùng content
2. Redirect sang trang edit template (v2) hoặc trang edit v1

### Flow 6: Cài đặt Auto-subscribe khi thêm bạn bè

1. Từ menu navigation → 「ステップ配信設定」 (SCR-SCE-05)
2. Chọn scenario cho 「新規友だち」 và/hoặc 「システム導入前からの友だち」
3. Cấu hình cách bắt đầu + tag → submit

### Flow 7: Xem bạn bè theo trạng thái

1. Từ SCR-SCE-01, click nút 「表示」 trên cột số lượng bạn bè
2. Mở trang danh sách bạn bè theo trạng thái (purchasing/unfinished/completed)

---

## Điểm chưa rõ (không xác nhận được từ UI)

1. **Controller cho v2**: Không rõ action nào trong `StepMessageController` phục vụ `index_v2` — cần xem controller.
2. **URL danh sách v2**: URL cụ thể để truy cập trang step message v2 của 1 scenario.
3. **Validation rules**: Các validation chi tiết phía server cho form tạo scenario/step message (chỉ thấy client-side).
4. **Quyền Staff**: Blade không có `@can` / `@if($user->hasRole(...))` rõ ràng — không xác định được giới hạn quyền Staff.
5. **Modal xem bạn bè**: View cho SCR-SCE-06 không được tìm thấy trong các blade đã đọc.
6. **Setting Add Friend v2**: File `setting_add_friend_v2.blade.php` tồn tại nhưng chưa đọc — có thể là phiên bản mới của SCR-SCE-05.
7. **Tối đa tin nhắn per step**: Code hiện chỉ enforce tối đa 100 steps/filter, không thấy giới hạn số messages/step rõ ràng trong blade.
8. **RichMenu change per step**: v2 có cột 「リッチメニュー変更」 trong settings panel — select với danh sách rich menus + option 「取り消し」 (value -1).
