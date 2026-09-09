# Logic Spec — FA-009: Phát hành theo bước (ステップ配信)

## Controllers

### Basic\ScenarioController
**File**: `app/Http/Controllers/Basic/ScenarioController.php`
**Mức độ tin cậy**: **Cao**

#### Use (Models & Classes quan trọng)
- `App\Scenario`, `App\StepMessage`, `App\StepMessageHistory`
- `App\ScenarioLineuser`, `App\ScenarioStepTime`
- `App\AddFriendSetting`, `App\Bots`, `App\BackupHistory`
- `App\Category`, `App\FilterManager`, `App\FilterV2`
- `App\Actions`, `App\ActionDetail`
- `App\Template`, `App\TemplateMappingTable`
- `App\RichMenus`, `App\Events`, `App\Tags`, `App\Tag`
- `App\Http\Requests\OwnerGetScenario`, `App\Http\Requests\StoreScenario`

#### Methods

**`index()`** (line 67)
- Lấy tất cả `Scenario` theo `bot_id`.
- Đọc cookie `folder_scenario` (JSON: `{bot_id => folderId}`) để xác định folder active.
- Kiểm tra `Category` có tồn tại theo `folderId`; nếu không hợp lệ (category không thuộc bot, hoặc null) → reset `folderId = 0`, cập nhật lại cookie (TTL 14400 phút, path `/basic/scenario`).
- **View**: `basic.scenario.scenario_index`

**`create()`** (line 93)
- Phần lớn code bị comment — hàm rỗng về chức năng thực tế.
- **Mức độ tin cậy**: **Thấp** (có thể không còn dùng).

**`store(Request $request)`** (line 116)
- Kiểm tra `BackupHistory` (status 0 hoặc 1) → chặn nếu đang backup/transfer.
- Kiểm tra `botIdCurrent` khớp session hiện tại.
- Validate `name`: required, max:20. Lỗi: `「ステップ名を入力して下さい。」`
- Tính `position`: nếu có `flag_position` → `min(position) - 1` (thêm đầu); ngược lại → `max(position) + 1` (thêm cuối).
- Insert vào `scenario` (table) với: `bot_id`, `name`, `method=0`, `group_id`, `after_scenario_id_1`, `position`, `update_timestamp`.
- Đọc và cập nhật lại cookie `folder_scenario`.
- Trả về JSON: `{success, folderId, scenarioId}`.

**`getListFriendByScenarioId(Request $request)`** (line 299)
- Ba chế độ hiển thị user:
  - `type=1`: Theo `scenarioId + stepId` → đếm qua `StepMessageHistory` (status=2, distinct line_user_id)
  - `type=0`: Theo `scenarioId` + `userCount` ('start'/'stop') → `Scenario::getListFriendUsers()` phân trang (limit=100)
  - `type=3`: Theo `senderID` → `Scenario::getListFriendUsersBySenderId()` phân trang (limit=250)
- **View**: `basic.scenario.list_friend_user`

**`edit(OwnerGetScenario $request)`** (line 363)
- Auth: `OwnerGetScenario` xác nhận `bot_id` ownership.
- Load scenario, AddFriendSetting (quan hệ new/old scenario), Events.
- Phần lớn return view bị comment — hàm rỗng.

**`update(Request $request)`** (line 410)
- Kiểm tra backup/botId cross-check.
- Validate `name_edit`: required. Lỗi: `「ステップ名を入力して下さい。」`
- Update `scenario`: `name`, `after_scenario_id_1`, `group_id`, `delay_type_1=0`, `after_start_day_1=null`, `after_start_time_1=null`, `from_1=null`, `to_1=null`.
- Trả về JSON: `{success, folderId}`.

**`destroy(OwnerGetScenario $request)`** (line 475)
- Auth: `OwnerGetScenario`.
- Gọi `deletedDataScenario($scenarioId)`.
- Trả về JSON: `{redirect_uri, folderId}`.

**`deletedDataScenario($scenarioId)`** (line 2433) — private helper
- **Cascade xoá** (Mức độ tin cậy: **Cao**):
  1. Lấy tất cả `step_message` của scenario → lấy IDs
  2. Xoá `scenario_step_time` theo step IDs (`whereIn step_mesage_id`)
  3. Xoá toàn bộ `step_message` của scenario
  4. Xoá bản ghi `scenario`
  5. Xoá `scenario_lineuser` theo `scenario_id + bot_id`
  6. Xoá `step_message_history` theo `scenario_id + bot_id`
  7. Xoá `filter_v2` có `type='scenario'` và `data` JSON chứa `scenario_id` (kiểm tra `data['scenario_search']`)
  8. Xoá `action_detail` có `type='scenario'` và `data['id'] == scenarioId` và `action` là 2 hoặc 3

**`setting()`** (line 504)
- Load scenarios, AddFriendSetting, Categories (kind=0).
- Return view bị comment. Hiện không dùng.

**`updateSetting(Request $request)`** (line 521)
- Cập nhật `add_friend_setting`: `new_scenario_id`, `old_scenario_id`, `new_delay_type`, `old_delay_type`, `new_tag_id`, `old_tag_id`, `new_start_day/time`, `old_start_day/time`, `new_category_id`, `old_category_id`.
- Logic tính start_day/time: nếu `delay_type == 0` → null; nếu rỗng → 0 và `"00:00:00"`.
- Redirect về `route('scenario.index')`.

**`scenarioCheckDelete(Request $request)`** (line 579)
- Đếm `StepMessage` theo `scenario_id`. Luôn trả về `{result: true}` (không chặn).

**`ajaxGetListScenario(Request $request)`** (line 591)
- Xử lý nhiều `action`:
  - `sortItem`: Update `position` cho từng scenario theo thứ tự IDs
  - `sortFolder`: Update `position` cho từng Category theo thứ tự
  - `deleteItems`: Gọi `deletedDataScenario()` cho mỗi ID
  - `moveItem`: Update `group_id` và `position` cho nhiều scenario sang folder khác
  - `deleteFolderSelected`: Xoá `category` theo IDs
- Sau đó load lại: danh sách folders (join scenario, count), danh sách scenarios theo folder hiện tại

**`copyScenario(OwnerGetScenario $request)`** (line 789)
- Auth: `OwnerGetScenario`.
- Tạo Scenario mới với `name = "{tên cũ}のコピー"`, copy các trường từ scenario gốc.
- Copy `FilterManager` (type='scenario') + `FilterV2` liên kết.
- Với mỗi `StepMessage`:
  - Clone templates nếu `category_id >= 0` → giữ nguyên ID; `category_id < 0` → clone thành `-111`
  - Clone `Action` + `ActionDetail` (và FilterV2 theo action detail nếu `has_filters=1`)
  - Clone `FilterManager` mapping
  - Tạo `StepMessage` mới qua `StepMessage::createStepMessage()`
  - Tạo `TemplateMappingTable` entries

**`showPark(Request $request)`** (line 971)
- Load template pack theo `park_id`, `scenario_id`.
- Lấy templates default (Category) và categories có templates.
- **View**: `basic.scenario.park-template.show`

**`createScenarioStep(Request $request)`** (line 2190)
- Tạo hoặc cập nhật một `step_message` với thông tin timing.
- **delay_type**:
  - `0`: ngày cụ thể (`start_day` + `start_time` dạng `H:i:00`)
  - `1`: gửi ngay (send_now) — `start_day=null`, `start_time=null`
  - `2`: delay theo phút:giây (`start_time` dạng `mm:ss:00`)
- Kiểm tra trùng step (cùng `delay_type + start_day + start_time + filter_manager_id`) → báo lỗi `「設定した時間に配信するメッセージが既に存在しています。」`
- Sau khi tạo/update: reorder `order_number` cho tất cả steps của scenario (theo `start_day asc, start_time asc, id asc`)

**`deleteScenarioStep(Request $request)`** (line 2346)
- Xoá `step_message` theo `id`.
- Xoá templates `category_id=-111` của step.
- Xoá `step_message_history` theo `step_id + scenario_id`.
- Xoá `scenario_step_time` (status=0) của step.
- Với mỗi user đang follow scenario:
  - Tìm `lastStep` trong `scenario_step_time` còn pending (status=0, order by `send_time desc`)
  - Nếu còn step → update `is_last_step`: step cũ=0, step cuối=1
  - Nếu không còn step → cập nhật `scenario_lineuser.is_following = 2` (dừng)
- Gọi `countScenario($scenarioId)` để cập nhật counter.
- Xoá `template_mapping_table` cho step.

**`saveSortStepMessage(Request $request)`** (line 2413)
- Update `step_message.template_ids` (chuỗi IDs mới đã sort).

**`settingMessage(Request $request)`** (line 1072)
- Load thông tin để render form tạo tin nhắn add-friend.
- **View**: `basic.scenario.setting_message`

**`editSettingMessage(Request $request)`** (line 1119)
- Load template đã lưu trong `add_friend_setting.sent_templates_new_friend` hoặc `sent_templates_old_friend` (JSON).
- **View**: `basic.scenario.setting_message` (action='edit')

**`updateSettingMessage(Request $request)`** (line 1259)
- Xử lý tạo/update đến 3 templates (flagMsgSetting: 1/2/3).
- Nếu template đã tồn tại: `handlerUpdateTemplate()` (cập nhật); nếu không: `handlerCreateTemplate()` (tạo mới).
- Lưu JSON `{template_id, template_id_2, template_id_3}` vào `add_friend_setting`.
- Nếu `typeSetting='old'`: cũng set `action_add_old_friend = config('sns-line.action_setting_add_old_friend.private_setting')`

**`updateSettingAddFriend(Request $request)`** (line 1015)
- Cập nhật `add_friend_setting.action_new_id` và `action_old_id`.
- Logic null-handling phức tạp: nếu field đang có giá trị (kể cả 0) và request không gửi → giữ 0; nếu chưa có → giữ null.

---

### Basic\StepMessageController
**File**: `app/Http/Controllers/Basic/StepMessageController.php`
**Mức độ tin cậy**: **Cao**
**Dependency injection**: `StepMessageService`

#### Methods

**`listMessage(OwnerGetScenario $request)`** (line 83)
- Kiểm tra ownership scenario.
- Load: categories (kind=template), richMenus (status_rich=1, join category), scenarioFilter, conversion, statusObject.
- **View**: `basic.step_message.index_v2`

**`scenarioMessage(OwnerGetScenario $request)`** (line 118)
- Kiểm tra ownership scenario.
- Load thông tin next scenario (`categoryOfScenNext`, `next_scen_name`).
- Kiểm tra alert: `SettingAlert::checkExistsKey('add_step')`, `checkExistsKey('add_message')`.
- **View**: `basic.step_message.scenario_message`

**`markCloseAlert(Request $request)`** (line 170)
- Insert `setting_alert` với `user_id = Auth::id()` và `key`.

**`create(OwnerGetScenario $request)`** (line 216)
- Hỗ trợ action `clone_template`: clone template type='group' và gắn ID mới vào `step_message.template_ids`, sau đó redirect về listMessage.
- Load: richMenus, scenarios, tags, categories, stickers, stickerPackage, groups_template, items_template, items_template_default.
- Nếu có `clone_id`: load stepMessage gốc để clone data.
- Nếu có `template_id`: load template, extract `group_question_one/two`, load `group_buttons`.
- Load `categoryFriendIfo` với `FriendInformationSetting`, `friendInfoDefault`.
- **View**: `basic.step_message.create`

**`store(OwnerGetScenario $request)`** (line 749)
- Kiểm tra backup, botId cross-check.
- Kiểm tra `action_image_map` hợp lệ (x, y, width, height phải là số, không âm, width/height >= 1).
- Load `StepMessage` hiện có → lấy `template_ids` cũ.
- Với mỗi `tmp_type[key]`: gọi `handlerCreateTemplate($request, $key, $cloneTemplate)` → nhận `$template_id`.
- Append `$template_id` vào `$templateListId`.
- Nếu **tester mode** (`is_tester` có và khác `'undefined'`): gửi thử qua `ChatHelper::tester()`, sau đó xoá template. Không lưu vào `template_ids`.
- Nếu **lưu thực sự**: Update `step_message.template_ids` = join các IDs.

**`handlerCreateTemplate($request, $key, $cloneTemplate)`** (line 403) — private
- Tạo record trong `template` với `category_id = -111`.
- Hỗ trợ các loại: `text/stamp`, `group`, `voice`, `video`, `image`, `form`, `question`, `location`, `introduction`.
- Với `text`: gọi `detectUrlInMessageTextV2()` để phát hiện URL; lưu `url_redirect` nếu có.
- Với `image`: upload qua API (`uploadMediaFileApi`), tạo thumbnail qua API; nếu `tmp_setting_image_map=1` → tạo image map.
- Với `video`: upload video, upload thumbnail, upload lên Dropbox.
- Với `form`: tạo `tmp_button` và `buttons` cho từng panel.
- **Ghi chú**: `image_server` được lưu để xác định CDN server chứa media.

**`edit(Request $request)`** (line 856)
- Load `StepMessage`, `ownScenario`, template (up đến 3 cái: `template_id`, `template_id_2`, `template_id_3`).
- Load categories, stickers, richMenus, tags, FriendInformationSetting.
- **View**: `basic.step_message.create` (action='edit')

**`update(Request $request)`** (line 993)
- Update template hiện có (`tmp_update`).
- Hỗ trợ các loại tương tự `store`.
- Với `image + image_map`: kiểm tra xem đã có `ImageMap` chưa → update hoặc create.
- Nếu không còn image map: xoá `image_map_items`, `action_detail`, `actions`, `filter_v2` liên quan.
- Với `text`: cập nhật url detect, url redirect.
- Nếu **tester mode**: gọi `sendTestStepMessage()`, không save template.
- Nếu **lưu thực sự**: `$tmp_update->save()`.

**`deleteStepMessage(Request $request)`** (line 1585)
- Kiểm tra backup.
- Tìm `template_id` trong `step_message.template_ids`, xoá khỏi mảng.
- Xoá template (nếu `category_id=-111` và type không phải form/group/image).
- Update `step_message.template_ids` (sau khi bỏ).
- Xoá `template_mapping_table` tương ứng.

**`createStepMessageByTemplate(Request $request)`** (line 1643)
- Thêm template từ thư viện vào step (không tạo mới template).
- Logic thêm vào cuối, nhưng nếu template cuối là quick-reply button → insert trước nó.

**`cloneStepMessageByTemplate(Request $request)`** (line 1941)
- Clone template (type bất kỳ, `category=-111`) vào step.
- Logic tương tự `createStepMessageByTemplate` về vị trí chèn.

**`ajaxGetListStepMessageV2(Request $request)`** (line 1445)
- Nếu scenario chưa có step nào → tạo một step mặc định (`delay_type=1`).
- Load tất cả steps, order by `start_day asc, start_time asc, id asc`.
- Với mỗi step: load `profile_bot` (BotsProfiles), tính `start_time_format`, load `step_message` templates (kể cả group content).
- Trả về JSON: `{status, scenarioStep}`.

**`getListStepMessageV3(Request $request)`** (line 2267)
- Filter theo `filter_manager_id` (null → không có filter; có → có filter).
- `simplePaginate` theo `per_page`.
- Kiểm tra xem có step `delay_type=1` (send_now) và/hoặc `delay_type=0` (datetime) không.

**`saveSettingRichmenu(Request $request)`** (line 1811)
- Update `step_message.rich_menu_id`.

**`deleteProfilesBots(Request $request)`** (line 1863)
- Xoá `bots_profiles` theo `id`.
- Cập nhật `step_message.profile_id = null` nếu step đang dùng profile đó.
- Cập nhật tất cả step_message đang dùng profile đó về `null`.

**`saveFilterTag(Request $request)`** (line 1914)
- Cập nhật `step_message.tag_filter_method`, `delivery_tag`, `skip_tag`:
  - method=0: không filter (delivery_tag=null, skip_tag=null)
  - method=1: chỉ gửi người có tag (delivery_tag=tag_ids, skip_tag=null)
  - method=2: bỏ qua người có tag (skip_tag=tag_ids, delivery_tag=null)

**`saveCommonStepMessage(Request $request)`** (line 2051)
- type='filter': Gọi `saveFilter()` để tạo/update `FilterManager` (type='scenario').
- Cập nhật `filter_v2` liên kết.

**`deleteFilterManager(Request $request)`** (line 2109)
- Xoá `filter_v2` và `filter_manager`.
- Xoá các step_message có `filter_manager_id` = filterId.
- Xoá `scenario_step_time` (status=0) theo step IDs.
- Với mỗi user follow scenario: cập nhật is_last_step hoặc is_following=2.
- Gọi `countScenario($scenarioId)`.

**`templateChildStep(Request $request)`** (line 3440)
- Load template parent, parse `content` (CSV IDs).
- Load từng template con với relationships.
- Với form type: load `tmp_button`, tính `aspectRatio`.
- **View**: `basic.step_message.v2.list-template-child`

**`saveDataScenario(Request $request)`** (line 3558)
- Update `scenario`: `name`, `group_id`, `after_scenario_id_1`.

**`previewScenarioMessage(OwnerGetScenario $request)`** (line 3578)
- Tương tự `scenarioMessage` nhưng không load conversion/status bổ sung.
- **View**: `basic.step_message.preview_scenario_message`

**`ajaxGetProfileOfBots(Request $request)`** (line 1715)
- Lấy danh sách BotsProfiles: Admin profiles (is_default desc, position asc, id desc) + Staff profiles (is_default=0).
- Nếu `profile_id` được chỉ định → xác nhận profile đang chọn.
- Nếu không tìm thấy profile default → tạo mới `bots_profiles` với `is_default=1`.

**`ajaxSendStepMessageTest(Request $request)`** (line 1266)
- Gửi test cho nhiều step + nhiều line user.
- Tạo messages qua `ChatMessages::getTemplate()` và `createMultipleMessage()`.
- Sau khi gửi thành công: increment `bots.free_send_count`, update `summary_message_send`.
- Gọi `sendAction($actionId, ...)` nếu step có action.

---

## Models

### Scenario (`App\Scenario`)
**File**: `app/Scenario.php`
**Table**: `scenario`
**Mức độ tin cậy**: **Cao**

#### Relationships
| Relationship | Type | Target | FK |
|---|---|---|---|
| `next_scenario1` | belongsTo | Scenario | `after_scenario_id_1` |
| `next_scenario2` | belongsTo | Scenario | `after_scenario_id_2` |
| `next_scenario3` | belongsTo | Scenario | `after_scenario_id_3` |
| `next_scenario4` | belongsTo | Scenario | `after_scenario_id_4` |
| `next_scenario5` | belongsTo | Scenario | `after_scenario_id_5` |
| `scenario_lineusers` | hasMany | ScenarioLineuser | — |
| `scenario_lineusers_reading` | hasMany | ScenarioLineuser | where is_following=1 |
| `scenario_lineusers_ended` | hasMany | ScenarioLineuser | where is_following=0 hoặc 2 |
| `step_messages` | hasMany | StepMessage | — |
| `last_step_message` | hasOne | StepMessage | order by start_day/time/order_number/id DESC |

#### Key Static Methods
- `getScenarioToChange($bot_id, $line_id)` — lấy tất cả scenario kèm trạng thái đăng ký của 1 LINE user
- `getListScenario($botId, $folderId, $keyword)` — danh sách có paginate, with next_scenario1..5
- `getListFriendUsersByStepId($scenarioId, $stepid, $botId)` — đếm user đã nhận step (qua `step_message_history` status=2)
- `getArrayFriendUsersByStepId(...)` — lấy LINE users đã nhận step

#### Trường quan trọng (suy luận từ code)
| Trường | Mô tả |
|--------|-------|
| `bot_id` | ID bot/OA chủ sở hữu |
| `name` | Tên scenario |
| `status` | Trạng thái (0/1) |
| `method` | Phương thức (luôn =0 khi tạo) |
| `group_id` | ID folder (Category, kind=0) |
| `after_scenario_id_1` | Scenario tiếp theo sau khi kết thúc |
| `position` | Thứ tự sắp xếp |
| `count_follow` | Số user đang follow (cache counter) |
| `count_stop` | Số user đã dừng (cache counter) |
| `update_timestamp` | Unix timestamp lần cập nhật cuối |
| `delay_type_1` | Loại delay cho next scenario (luôn =0 khi update) |

---

### StepMessage (`App\StepMessage`)
**File**: `app/StepMessage.php`
**Table**: `step_message`
**Mức độ tin cậy**: **Cao**

#### Relationships
| Relationship | Type | Target | FK |
|---|---|---|---|
| `scenario` | belongsTo | Scenario | — |
| `template` | belongsTo | Template | — |
| `template2` | hasOne | Template | `template_id_2` |
| `template3` | hasOne | Template | `template_id_3` |
| `rich_menus` | hasOne | RichMenus | `rich_menu_id` |
| `profile` | belongsTo | BotsProfiles | `profile_id` |
| `detailActions` | hasMany | ActionDetail | `action_id` → `action_id` |

#### Trường quan trọng
| Trường | Mô tả |
|--------|-------|
| `scenario_id` | FK → scenario |
| `template_id` | Template chính (cũ, ít dùng) |
| `template_id_2`, `template_id_3` | Template bổ sung (cũ) |
| `template_ids` | Danh sách template IDs dạng CSV (mới, chủ yếu dùng) |
| `delay_type` | 0=theo ngày, 1=gửi ngay, 2=delay phút:giây |
| `start_day` | Số ngày sau khi đăng ký (delay_type=0) |
| `start_time` | Giờ gửi (delay_type=0: `H:i:s`; delay_type=2: `mm:ss:00`) |
| `order_number` | Thứ tự step trong scenario |
| `name` | Tên step |
| `tag_filter_method` | 0=không filter, 1=chỉ gửi người có tag, 2=bỏ qua người có tag |
| `delivery_tag` | CSV tag IDs — điều kiện gửi |
| `skip_tag` | CSV tag IDs — điều kiện bỏ qua |
| `is_stopped_after` | Dừng sau khi gửi |
| `is_deleted` | Soft delete flag |
| `rich_menu_id` | Rich menu đính kèm |
| `action_id` | ID action thực thi sau khi gửi |
| `filter_manager_id` | FK → filter_manager (filter phân nhánh) |
| `profile_id` | FK → bots_profiles (profile gửi) |
| `update_timestamp` | Unix timestamp |

#### Static Method
`createStepMessage($data)`:
- Kiểm tra trùng theo `(order_number, scenario_id, start_day, start_time)`.
- Nếu trùng: tăng `order_number` cho các step sau lên 1.
- Nếu không trùng nhưng `order_number` vượt tổng → đặt lại.

---

### ScenarioLineuser (`App\ScenarioLineuser`)
**File**: `app/ScenarioLineuser.php`
**Table**: `scenario_lineuser`
**Mức độ tin cậy**: **Cao**

#### Relationship
- `line_user`: hasMany LineUser (FK ngược: `line_user_id`)

#### Trường quan trọng
| Trường | Mô tả |
|--------|-------|
| `bot_id` | ID bot |
| `scenario_id` | FK → scenario |
| `line_user_id` | FK → line_user |
| `is_following` | 1=đang follow, 0=chưa, 2=đã dừng |
| `start_day` | Ngày bắt đầu |
| `start_time` | Giờ bắt đầu |
| `start_datetime` | Datetime bắt đầu |
| `sent_start_day`, `sent_start_time` | Ngày/giờ đã thực sự gửi bắt đầu |
| `is_deleted` | Soft delete flag |

---

### ScenarioStepTime (`App\ScenarioStepTime`)
**File**: `app/ScenarioStepTime.php`
**Table**: `scenario_step_time`
**Mức độ tin cậy**: **Cao**

#### Relationship
- `stepMessage`: hasOne StepMessage (`step_mesage_id` → `id`) — **Lưu ý lỗi typo: `step_mesage_id` thay vì `step_message_id`**

#### Trường quan trọng
| Trường | Mô tả |
|--------|-------|
| `user_id` | LINE user ID |
| `step_mesage_id` | FK → step_message (typo nhưng là tên thực trong DB) |
| `send_time` | Thời điểm dự kiến gửi (datetime) |
| `bot_id` | ID bot |
| `status` | 0=chờ gửi, khác 0=đã gửi/xử lý |
| `is_last_step` | 1=đây là step cuối cùng pending của user |

#### Static Methods
- `updateScenarioStepTimeRetry($data, $where, $retries=0)`: update với retry tối đa 3 lần
- `getScenarioStepTimeIsSame($scenarioStepTime)`: tìm record trùng theo `(user_id, bot_id, send_time, status=0)`

---

## Services

### StepMessageService (`App\Services\StepMessageService`)
**File**: `app/Services/StepMessageService.php`
**Mức độ tin cậy**: **Cao**

#### Dependencies (Repositories)
- `ConversationRepositoryInterface`
- `TemplateRepositoryInterface`
- `MessageService`
- `BotRepositoryInterface`
- `TemplateService`
- `LineUserRepositoryInterface`
- `StepMessageRepositoryInterface`

#### Method `sendTestStepMessageV3($request)`
- Gửi test step message theo kiến trúc mới (v3).
- Lấy `stepMessages` qua repository, với mỗi cặp (lineUser, stepMessage):
  - Lấy profile_send (profile_id của step hoặc default profile của bot)
  - Build message object: `msg_kind`, `profile_send`, `type`, `scenarioId`, `stepMessageId`, `stepNumber`, `filterId`, `versionId`, `name`, `timeSendType`, `beforeDay`, `timeSend`
  - Merge templates qua `TemplateService::mergeListTemplate()`
  - Gửi qua `MessageService::createMessageTypeV2()` với `isTester=true`

---

## Form Requests

### OwnerGetScenario
**File**: `app/Http/Requests/OwnerGetScenario.php`
**Mức độ tin cậy**: **Cao**

- `authorize()`: Kiểm tra `scenario.bot_id == getBotId()`. Nếu không khớp → redirect `/basic/scenario`.
- `rules()`: Không có validation rules.

---

## Validation Rules (tổng hợp)

| Endpoint | Field | Rule | Thông báo lỗi |
|----------|-------|------|---------------|
| store scenario | `name` | required, max:20 | 「ステップ名を入力して下さい。」 |
| update scenario | `name_edit` | required | 「ステップ名を入力して下さい。」 |
| store step message | `action_image_map[*].x/y` | >= 0, numeric | エリアN: 領域設定が間違っています。 |
| store step message | `action_image_map[*].width/height` | >= 1, numeric | (cùng message) |
| ownership check | scenario `bot_id` | == getBotId() | Redirect về /basic/scenario |
| bot cross-check | `botIdCurrent` | == getBotId() | 「別のアカウントに切り替えたので、要求を処理できません。」 |
| backup check | BackupHistory status | không có record status 0/1 | MESSAGE_NOTIFY_BACKUP constant |

---

## Business Rules

### BR-01: Quản lý folder (cookie-based)
- **Mức độ tin cậy**: **Cao** (line 71-82, ScenarioController@index)
- Folder active được lưu trong cookie `folder_scenario` (JSON: `{bot_id: folderId}`), TTL 14400 phút.
- Nếu `folderId` không hợp lệ (null, hoặc Category không tồn tại) → reset về `0` (tất cả scenario).

### BR-02: Thứ tự step (order_number)
- **Mức độ tin cậy**: **Cao** (ScenarioController@createScenarioStep, line 2306)
- Sau mỗi lần tạo/update step → reorder toàn bộ steps theo `(start_day asc, start_time asc, id asc)`.
- `StepMessage::createStepMessage()` kiểm tra trùng order_number và auto-increment.

### BR-03: Loại thời gian gửi (delay_type)
- **Mức độ tin cậy**: **Cao** (line 2207-2226)
- `delay_type=0`: theo ngày (start_day = N ngày, start_time = `H:i:00`)
- `delay_type=1`: gửi ngay sau khi đăng ký (send_now)
- `delay_type=2`: delay tính theo phút:giây (start_time = `mm:ss:00`)
- Không cho phép 2 steps trùng cùng `(delay_type, start_day, start_time, filter_manager_id)`.

### BR-04: Template category_id = -111
- **Mức độ tin cậy**: **Cao** (nhiều nơi)
- Templates được tạo cho step message luôn có `category_id = -111` (internal/private, không xuất hiện trong thư viện).
- Khi xoá step → xoá các template có `category_id=-111` thuộc step đó.

### BR-05: template_ids (CSV)
- **Mức độ tin cậy**: **Cao**
- `step_message.template_ids` lưu danh sách template IDs dạng CSV (phân cách bởi dấu phẩy).
- Một step có thể có nhiều template (tối đa 5 messages per batch khi gửi qua LINE API).
- Template loại 'group' chứa nhiều template con trong `template.content` (cũng dạng CSV).

### BR-06: Kiểm soát filter phân nhánh
- **Mức độ tin cậy**: **Cao**
- Một scenario có thể có nhiều `filter_manager` (phân nhánh điều kiện).
- Mỗi nhánh có danh sách step riêng (`step_message.filter_manager_id`).
- Khi xoá `filter_manager` → cascade xoá toàn bộ steps và pending send queue của nhánh đó.

### BR-07: Profile gửi tin
- **Mức độ tin cậy**: **Cao** (line 1791-1808)
- Mỗi step có thể được cấu hình gửi từ một profile bot cụ thể (`step_message.profile_id`).
- Profile `is_default=1` → không lưu vào `profile_id` (để null), dùng profile mặc định của bot.

### BR-08: Cascade xoá scenario
- **Mức độ tin cậy**: **Cao** (deletedDataScenario, line 2433)
- Xoá scenario → xoá toàn bộ: scenario_step_time, step_message, scenario, scenario_lineuser, step_message_history, và cleanup filter_v2 + action_detail liên quan.

### BR-09: Backup lock
- **Mức độ tin cậy**: **Cao** (nhiều nơi)
- Khi bot đang trong quá trình backup/transfer (`BackupHistory` có record status 0 hoặc 1 theo `transfer_code`) → chặn toàn bộ thao tác ghi (create/update/delete scenario, step_message).

### BR-10: Cập nhật counter scenario
- **Mức độ tin cậy**: **Cao**
- Hàm `countScenario($scenarioId)` được gọi sau các thao tác ảnh hưởng đến danh sách users.
- `count_follow` = số user `is_following=1`, `count_stop` = số user `is_following=2`.

---

## Events / Queue Jobs

> **QUAN TRỌNG cho job-analyzer**

### Bảng `scenario_step_time` — Queue gửi tin
- **Mức độ tin cậy**: **Cao**
- Khi xoá step (`deleteScenarioStep`): `ScenarioStepTime::where('step_mesage_id', $id)->where('status', 0)->delete()` — xoá các bản ghi pending.
- Khi xoá filter manager: tương tự.
- **Suy luận**: Bảng `scenario_step_time` là **queue/schedule table** cho Spring Boot job. Mỗi record = một lần gửi tin đã lên lịch cho một user cụ thể.
- Spring Boot job đọc `scenario_step_time` (status=0), gửi tin, cập nhật status.
- Trường `is_last_step` được dùng để xác định step cuối → Spring Boot có thể trigger chuyển scenario.

### Bảng `step_message_history` — Lịch sử gửi
- **Mức độ tin cậy**: **Cao**
- Khi xoá scenario/step: xoá `step_message_history` liên quan.
- `status=2` = đã gửi thành công (dùng để đếm user đã nhận step).

### Trigger khi đăng ký scenario (AddFriendSetting)
- **Mức độ tin cậy**: **Trung bình** (suy luận từ `AddFriendSetting` model và logic updateSetting)
- `add_friend_setting` lưu: `new_scenario_id`, `old_scenario_id`, `new_delay_type`, `old_delay_type`, `new_start_day`, `new_start_time`, `old_start_day`, `old_start_time`.
- Khi user thêm bot → Spring Boot job đọc `add_friend_setting` để xác định scenario cần đăng ký và thời điểm bắt đầu.

### updateMessageSendCount (trong ajaxSendStepMessageTest)
- Gọi `updateMessageSendCount($botId, date, 3, count)` — loại 3 = step message.
- **Mức độ tin cậy**: **Cao**

---

## Authorization

### Middleware
- Tất cả routes dưới `/basic` sử dụng middleware: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`.
- `basic_access`: kiểm tra quyền truy cập portal Admin/Staff.
- `is_expire`: kiểm tra tài khoản chưa hết hạn.
- `check_remember_token`: xác thực session/token.

### Form Request Authorization
- `OwnerGetScenario`: kiểm tra `scenario.bot_id == getBotId()` → đảm bảo chỉ chủ bot mới truy cập được scenario.
- Các method không dùng Form Request (`store`, `update`, `ajaxGetListScenario`...): thực hiện kiểm tra `botIdCurrent == getBotId()` trong code.

### Bot Cross-check
- Nhiều endpoints yêu cầu client gửi `botIdCurrent` trong request body.
- Nếu không khớp với session → trả về lỗi `「別のアカウントに切り替えたので、要求を処理できません。」`.
- **Mục đích**: ngăn race condition khi user mở nhiều tab với các bot khác nhau.
