# Tool inventory — docs MCP task #39446

> Sinh bởi `/review-mcp-docs` 2026-10-14 từ `docs/04-form-survey.md` (bản cập nhật 2026-10-14, `04-form-survey (2).md`). Ghi đè mỗi lần chạy.
> Cột Enum / Default / Min-Max trích **nguyên văn** từ cột Description của docs; ô trống = docs không ghi (nguyên liệu cho `DOC-MISS`, KHÔNG suy đoán).
> `items[X].` = param của thao tác `type=X`; `field[T].` = param riêng của `field_type=T`; `field.` = param chung mọi câu hỏi nhóm 1 + 2.

## `list_forms` — Danh sách form (đọc) · nguồn: docs/04-form-survey.md §1
Tính năng LME: FA-011 フォーム作成 (spec-features/admin/form-answer/) · Thao tác: đọc (list) · Lỗi docs ghi: không ghi mã lỗi / mã HTTP nào

| Param | Kiểu | Bắt buộc | Enum / format | Default | Min / Max | Ràng buộc / phụ thuộc | Nguồn docs |
|---|---|---|---|---|---|---|---|
| `bot_id` | String · ID | ✔ |  |  |  | Bot ID hash string lấy từ tool list_bots | §1 (L14) |
| `names` | Array of String | — |  |  |  | Mảng tên form EXACT (match trên field `name` HOẶC `title` — form khớp 1 trong 2 cột sẽ được trả; case-insensitive, trim). Multiple = OR. Partial KHÔNG match. | §1 (L15) |
| `page` | Integer | — |  |  |  | Số trang (default: 1) | §1 (L16) |
| `limit` | Integer | — |  |  |  | Số lượng record mỗi trang (default: 100, max: 100) | §1 (L17) |

## `get_form_detail` — Chi tiết form (đọc) · nguồn: docs/04-form-survey.md §2
Tính năng LME: FA-011 フォーム作成 (spec-features/admin/form-answer/) · Thao tác: đọc (get) · Lỗi docs ghi: không ghi mã lỗi / mã HTTP nào

| Param | Kiểu | Bắt buộc | Enum / format | Default | Min / Max | Ràng buộc / phụ thuộc | Nguồn docs |
|---|---|---|---|---|---|---|---|
| `form_ids` | String · ID | ✔ |  |  | tối đa 100. | Danh sách ID Form/Survey cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" | §2 (L100) |
| `bot_id` | String · ID | ✔ |  |  |  | Bot ID hash string lấy từ tool list_bots | §2 (L101) |

## `get_form_responses` — Câu trả lời của form (đọc) · nguồn: docs/04-form-survey.md §3
Tính năng LME: FA-011 フォーム作成 (spec-features/admin/form-answer/) · Thao tác: đọc (get) · Lỗi docs ghi: không ghi mã lỗi / mã HTTP nào

| Param | Kiểu | Bắt buộc | Enum / format | Default | Min / Max | Ràng buộc / phụ thuộc | Nguồn docs |
|---|---|---|---|---|---|---|---|
| `form_id` | Long · ID | ✔ |  |  |  | ID của Form/Survey | §3 (L253) |
| `bot_id` | String · ID | ✔ |  |  |  | Bot ID hash string lấy từ tool list_bots | §3 (L254) |
| `page` | Int | — |  |  |  | Số trang (default: 1) | §3 (L255) |
| `limit` | Int | — |  |  |  | Số lượng record mỗi trang (default: 100, max: 100) | §3 (L256) |

## `create_form_survey` — Tạo vỏ form · nguồn: docs/04-form-survey.md §4
Tính năng LME: FA-011 フォーム作成 (spec-features/admin/form-answer/) · Thao tác: tạo · Lỗi docs ghi: "Số form (gói free) ≤ 3 (server từ chối)" — không ghi mã HTTP

| Param | Kiểu | Bắt buộc | Enum / format | Default | Min / Max | Ràng buộc / phụ thuộc | Nguồn docs |
|---|---|---|---|---|---|---|---|
| `bot_id` | String · ID | ✔ |  |  |  | Bot ID hash string lấy từ tool list_bots | §4 (L363) |
| `name` | String | ✔ |  |  | tối đa 50 ký tự | 管理名 (tên quản lý nội bộ, tối đa 50 ký tự) — hiển thị trong danh sách form của admin, KHÔNG hiển thị cho người trả lời (入力内容はお客様に表示されません) | §4 (L364) |
| `title` | String | ✔ |  |  | tối đa 20 ký tự | フォーム名 (tên form, tối đa 20 ký tự) — hiển thị cho người trả lời trên public form (入力内容がお客様に表示されます) | §4 (L365) |
| `folder_id` | Long · ID | — |  |  |  | フォルダ — ID folder chứa form. Bỏ trống hoặc 0 = chưa phân loại (未分類, mặc định) | §4 (L366) |
| `form_type` | Integer | — | 1 / 2 |  |  | タイプ選択 — loại form, KHÔNG đổi được sau khi tạo (あとから変更はできません): `1` = シンプルタイプ (đơn giản, form 1 trang — mặc định), `2` = 分岐タイプ (phân nhánh, trang trả lời rẽ nhánh theo nội dung câu trả lời) | §4 (L367) |

## `update_form_survey` — Sửa form theo mảng items[] (12 thao tác) · nguồn: docs/04-form-survey.md §5
Tính năng LME: FA-011 フォーム作成 (spec-features/admin/form-answer/) · Thao tác: sửa (12 thao tác) · xoá field/page · Lỗi docs ghi: không ghi mã lỗi / mã HTTP nào

| Param | Kiểu | Bắt buộc | Enum / format | Default | Min / Max | Ràng buộc / phụ thuộc | Nguồn docs |
|---|---|---|---|---|---|---|---|
| `bot_id` | String · ID | ✔ |  |  |  | Bot ID hash string lấy từ tool list_bots | §5 (L419) |
| `form_id` | Long · ID | ✔ |  |  |  | ID Form/Survey (từ list_forms hoặc id trả về của create_form_survey) | §5 (L420) |
| `items` | Array of Item | ✔ |  |  |  | Danh sách item của form theo thứ tự hiển thị (xem Sub Object Item) | §5 (L421) |
| `items[].type` | String (enum) | ✔ | HEADER_IMAGE / ADD_FIELD / UPDATE_FIELD / REMOVE_FIELD / UPDATE_BUTTON / ADD_PAGE / REMOVE_PAGE / SET_NEXT_PAGE / UPDATE_DESIGN / UPDATE_MESSAGE_ACTION / UPDATE_DIAGNOSTIC / UPDATE_SETTINGS |  |  | Loại item: `HEADER_IMAGE` (ảnh tiêu đề) / `ADD_FIELD` (thêm field) / `UPDATE_FIELD` (sửa field) / `REMOVE_FIELD` (xóa field) / `UPDATE_BUTTON` (sửa nút submit) / `ADD_PAGE` (thêm page) / `REMOVE_PAGE` (xóa page) / `SET_NEXT_PAGE` (điều hướng trang tiếp — 次のページ | §5 Sub Object Item (L427) |
| `items[HEADER_IMAGE].type` | String | ✔ |  |  |  | Cố định `"HEADER_IMAGE"` | §5 HEADER_IMAGE (L438) |
| `items[HEADER_IMAGE].page_id` | Long · ID | — |  |  |  | ID page cần đặt ảnh (từ get_form_detail pages[].page_id). Bỏ trống = page đầu tiên | §5 HEADER_IMAGE (L439) |
| `items[HEADER_IMAGE].image_url` | String | ✔ |  |  |  | URL ảnh tiêu đề — dùng `download_url` trả về từ tool `get_file_params` (sau khi user upload ảnh qua MCP client) | §5 HEADER_IMAGE (L440) |
| `items[ADD_FIELD].type` | String | ✔ |  |  |  | Cố định `"ADD_FIELD"` | §5 ADD_FIELD (L469) |
| `items[ADD_FIELD].page_id` | Long · ID | — |  |  |  | ID page đích (từ `get_form_detail` pages[].page_id). Bỏ trống = page đầu tiên (スタートページ). Với form phân nhánh có nhiều page, chỉ định rõ page cần thêm | §5 ADD_FIELD (L470) |
| `items[ADD_FIELD].field` | Object | ✔ |  |  |  | Nội dung field (xem Sub Object Field) — KHÔNG có `field_id` | §5 ADD_FIELD (L471) |
| `items[UPDATE_FIELD].type` | String | ✔ |  |  |  | Cố định `"UPDATE_FIELD"` | §5 UPDATE_FIELD (L480) |
| `items[UPDATE_FIELD].field_id` | Long · ID | ✔ |  |  |  | ID field cần sửa (từ `get_form_detail` pages[].fields[].id) | §5 UPDATE_FIELD (L481) |
| `items[UPDATE_FIELD].field` | Object | ✔ |  |  |  | Trạng thái mới của field (xem Sub Object Field). `field_type` phải khớp loại hiện tại — không đổi được loại field | §5 UPDATE_FIELD (L482) |
| `items[REMOVE_FIELD].type` | String | ✔ |  |  |  | Cố định `"REMOVE_FIELD"` | §5 REMOVE_FIELD (L490) |
| `items[REMOVE_FIELD].field_id` | Long · ID | ✔ |  |  |  | ID field cần xóa (từ `get_form_detail` pages[].fields[].id) | §5 REMOVE_FIELD (L491) |
| `items[UPDATE_BUTTON].type` | String | ✔ |  |  |  | Cố định `"UPDATE_BUTTON"` | §5 UPDATE_BUTTON (L549) |
| `items[UPDATE_BUTTON].page_id` | Long · ID | — |  |  |  | ID page (từ get_form_detail pages[].page_id). Bỏ trống = page đầu tiên | §5 UPDATE_BUTTON (L550) |
| `items[UPDATE_BUTTON].button_name` | String | ✔ |  |  | tối đa 30 ký tự | ボタンテキスト — text hiển thị trên nút, tối đa 30 ký tự, bắt buộc. Default web: 回答する | §5 UPDATE_BUTTON (L551) |
| `items[UPDATE_BUTTON].pattern` | Integer | — | 1 / 2 | 1 |  | デザイン: `1` (パターン① — nút nền đầy, default) / `2` (パターン②) | §5 UPDATE_BUTTON (L552) |
| `items[UPDATE_BUTTON].text_color` | String | — |  | #5799DB |  | 文字色 `#RRGGBB` (default #5799DB) | §5 UPDATE_BUTTON (L553) |
| `items[UPDATE_BUTTON].bg_color` | String | — |  | #EDF4FB |  | 背景色 `#RRGGBB` (default #EDF4FB) | §5 UPDATE_BUTTON (L554) |
| `items[UPDATE_BUTTON].font_weight` | Integer | — | 600 / 300 | 600 |  | 文字の太さ: `600` (đậm, default) / `300` (mảnh) | §5 UPDATE_BUTTON (L555) |
| `items[UPDATE_BUTTON].shadow` | Boolean | — |  |  |  | シャドウ — đổ bóng nút. Default true | §5 UPDATE_BUTTON (L556) |
| `items[ADD_PAGE].type` | String | ✔ |  |  |  | Cố định `"ADD_PAGE"` | §5 ADD_PAGE (L571) |
| `items[ADD_PAGE].page_name` | String | ✔ |  |  | tối đa 10 ký tự | ページ名 — tên page, tối đa 10 ký tự | §5 ADD_PAGE (L572) |
| `items[REMOVE_PAGE].type` | String | ✔ |  |  |  | Cố định `"REMOVE_PAGE"` | §5 REMOVE_PAGE (L590) |
| `items[REMOVE_PAGE].page_id` | Long · ID | ✔ |  |  |  | ID page cần xóa (từ get_form_detail pages[].page_id) | §5 REMOVE_PAGE (L591) |
| `items[SET_NEXT_PAGE].type` | String | ✔ |  |  |  | Cố định `"SET_NEXT_PAGE"` | §5 SET_NEXT_PAGE (L611) |
| `items[SET_NEXT_PAGE].page_id` | Long · ID | — |  |  |  | ID page cần cấu hình. Bỏ trống = page đầu tiên | §5 SET_NEXT_PAGE (L612) |
| `items[SET_NEXT_PAGE].mode` | String (enum) | ✔ | END / PAGE / BRANCH | END |  | `END` = 回答完了ページ (kết thúc form, default của page mới) / `PAGE` = chuyển tới 1 page cố định / `BRANCH` = phân nhánh theo câu trả lời | §5 SET_NEXT_PAGE (L613) |
| `items[SET_NEXT_PAGE].next_page_id` | Long · ID | — |  |  |  | Bắt buộc khi mode=PAGE — ID page đích | §5 SET_NEXT_PAGE (L614) |
| `items[SET_NEXT_PAGE].field_id` | Long · ID | — |  |  |  | Bắt buộc khi mode=BRANCH — ID câu hỏi điều khiển phân nhánh trên page này. Chỉ nhận câu hỏi SELECT (単一選択, radio/dropdown) bắt buộc | §5 SET_NEXT_PAGE (L615) |
| `items[SET_NEXT_PAGE].branches` | Array | — |  |  |  | Bắt buộc khi mode=BRANCH — mảng `{option_label, next_page_id}`: mỗi lựa chọn của câu hỏi map tới 1 page đích. `next_page_id = 0` (hoặc null) = 回答完了ページ. Option không có trong mảng sẽ theo đích của phần tử đầu tiên | §5 SET_NEXT_PAGE (L616) |
| `items[UPDATE_DESIGN].type` | String | ✔ |  |  |  | Cố định `"UPDATE_DESIGN"` | §5 UPDATE_DESIGN (L647) |
| `items[UPDATE_DESIGN].header` | Object | — |  |  |  | Section ヘッダー・背景 (xem bảng dưới) | §5 UPDATE_DESIGN (L648) |
| `items[UPDATE_DESIGN].heading` | Object | — |  |  |  | Section 見出し — thiết kế mặc định cho item HEADING | §5 UPDATE_DESIGN (L649) |
| `items[UPDATE_DESIGN].divider` | Object | — |  |  |  | Section 区切り線 — thiết kế mặc định cho item DIVIDER | §5 UPDATE_DESIGN (L650) |
| `items[UPDATE_DESIGN].question` | Object | — |  |  |  | Section 質問項目 — chữ câu hỏi + 補足 | §5 UPDATE_DESIGN (L651) |
| `items[UPDATE_DESIGN].button` | Object | — |  |  |  | Section ボタン — thiết kế mặc định nút các page | §5 UPDATE_DESIGN (L652) |
| `items[UPDATE_DESIGN].css` | Object | — |  |  |  | Section CSS・JS設定 — CSS class + custom CSS/JS | §5 UPDATE_DESIGN (L653) |
| `items[UPDATE_DESIGN].header.image_url` | String | — |  |  | ≤10MB | 共通ヘッダー画像 — URL ảnh header chung (download_url từ get_file_params; web giới hạn ≤10MB). Page mới tạo sẽ lấy ảnh này làm mặc định; từng page có thể ghi đè bằng item `HEADER_IMAGE` | §5 header (L658) |
| `items[UPDATE_DESIGN].header.remove_image` | Boolean | — |  |  |  | true = xóa ảnh header chung hiện tại | §5 header (L659) |
| `items[UPDATE_DESIGN].header.bg_color` | String | — |  | #FFFFFF |  | フォーム背景 — màu nền form `#RRGGBB` (default #FFFFFF) | §5 header (L660) |
| `items[UPDATE_DESIGN].heading.pattern` | Integer | — | 1 / 2 / 3 | 1 |  | デザイン選択 `1`/`2`/`3` (default 1). Lưu ý: trên web chọn pattern sẽ tự đổi màu mặc định kèm theo — qua MCP hãy set màu tường minh | §5 heading (L665) |
| `items[UPDATE_DESIGN].heading.text_color` | String | — |  | #FFFFFF |  | 文字色 `#RRGGBB` (default #FFFFFF) | §5 heading (L666) |
| `items[UPDATE_DESIGN].heading.bg_color` | String | — |  | #5799DB |  | 背景色 (pattern 1) / 線色 (pattern 2,3) `#RRGGBB` (default #5799DB) | §5 heading (L667) |
| `items[UPDATE_DESIGN].heading.font_weight` | Integer | — | 600 / 300 | 600 |  | `600` (đậm, default) / `300` (mảnh) | §5 heading (L668) |
| `items[UPDATE_DESIGN].heading.font_size` | Integer | — | 24 / 20 / 16 | 24 |  | `24` (lớn, default của form mới) / `20` (vừa) / `16` (nhỏ) | §5 heading (L669) |
| `items[UPDATE_DESIGN].heading.text_align` | String | — | left / center / right | center |  | `left` / `center` (default) / `right` | §5 heading (L670) |
| `items[UPDATE_DESIGN].heading.apply_to_existing` | Boolean | — |  |  |  | 現在登録されているすべての見出しに、このデザインを適用（上書き）する — true = ghi đè thiết kế này lên tất cả item HEADING đang có trên form. Default false | §5 heading (L671) |
| `items[UPDATE_DESIGN].divider.pattern` | Integer | — | 1 / 2 / 3 | 1 |  | デザイン選択 `1` (nét liền) / `2` (nét đứt) / `3` (2 nét) (default 1) | §5 divider (L676) |
| `items[UPDATE_DESIGN].divider.color` | String | — |  | #5799DB |  | カラー設定 `#RRGGBB` (default #5799DB) | §5 divider (L677) |
| `items[UPDATE_DESIGN].divider.width` | Integer | — | 350 / 250 / 150 | 350 |  | 線の長さ: `350` (長い, default) / `250` (普通) / `150` (短い) | §5 divider (L678) |
| `items[UPDATE_DESIGN].divider.apply_to_existing` | Boolean | — |  |  |  | true = ghi đè thiết kế này lên tất cả item DIVIDER đang có. Default false | §5 divider (L679) |
| `items[UPDATE_DESIGN].question.text_color` | String | — |  | #222222 |  | Màu chữ câu hỏi `#RRGGBB` (default #222222) | §5 question (L684) |
| `items[UPDATE_DESIGN].question.font_weight` | Integer | — | 600 / 300 | 600 |  | `600` (default) / `300` | §5 question (L685) |
| `items[UPDATE_DESIGN].question.font_size` | Integer | — | 18 / 16 / 14 | 16 |  | `18` / `16` (default) / `14` | §5 question (L686) |
| `items[UPDATE_DESIGN].question.help_color` | String | — |  | #222222 |  | Màu chữ 補足 `#RRGGBB` (default #222222) | §5 question (L687) |
| `items[UPDATE_DESIGN].question.help_font_weight` | Integer | — | 600 / 300 | 300 |  | `600` / `300` (default) | §5 question (L688) |
| `items[UPDATE_DESIGN].question.help_font_size` | Integer | — | 16 / 14 / 12 | 14 |  | `16` / `14` (default) / `12` | §5 question (L689) |
| `items[UPDATE_DESIGN].button.pattern` | Integer | — | 1 / 2 | 1 |  | `1` (パターン①, default) / `2` (パターン②) | §5 button (L694) |
| `items[UPDATE_DESIGN].button.text_color` | String | — |  | #5799DB |  | 文字色 `#RRGGBB` (default #5799DB) | §5 button (L695) |
| `items[UPDATE_DESIGN].button.bg_color` | String | — |  | #EDF4FB |  | 背景色 `#RRGGBB` (default #EDF4FB) | §5 button (L696) |
| `items[UPDATE_DESIGN].button.font_weight` | Integer | — | 600 / 300 | 600 |  | `600` (default) / `300` | §5 button (L697) |
| `items[UPDATE_DESIGN].button.shadow` | Boolean | — |  |  |  | Đổ bóng. Default true | §5 button (L698) |
| `items[UPDATE_DESIGN].button.apply_to_existing` | Boolean | — |  |  |  | true = ghi đè thiết kế này lên nút của tất cả page hiện có (kể cả nút trang xác nhận). Default false | §5 button (L699) |
| `items[UPDATE_DESIGN].css.heading_class` | String | — |  |  |  | CSS class cho 見出し (title_class) | §5 css (L704) |
| `items[UPDATE_DESIGN].css.heading_sub_class` | String | — |  |  |  | CSS class cho phụ đề 見出し (subtitle_class) | §5 css (L705) |
| `items[UPDATE_DESIGN].css.question_class` | String | — |  |  |  | CSS class cho câu hỏi (question_class) | §5 css (L706) |
| `items[UPDATE_DESIGN].css.help_class` | String | — |  |  |  | CSS class cho 補足 (subquestion_class) | §5 css (L707) |
| `items[UPDATE_DESIGN].css.dropdown_class` | String | — |  |  |  | CSS class cho dropdown | §5 css (L708) |
| `items[UPDATE_DESIGN].css.radio_class` | String | — |  |  |  | CSS class cho radio | §5 css (L709) |
| `items[UPDATE_DESIGN].css.checkbox_class` | String | — |  |  |  | CSS class cho checkbox | §5 css (L710) |
| `items[UPDATE_DESIGN].css.divider_class` | String | — |  |  |  | CSS class cho 区切り線 (line_class) | §5 css (L711) |
| `items[UPDATE_DESIGN].css.button_class` | String | — |  |  |  | CSS class cho nút (button_class) | §5 css (L712) |
| `items[UPDATE_DESIGN].css.apply_to_existing` | Boolean | — |  |  |  | true = áp các class trên vào tất cả item đang có (class_overwrite). Default false | §5 css (L713) |
| `items[UPDATE_DESIGN].css.custom_css` | String | — |  |  |  | Custom CSS của form — áp vào public form | §5 css (L714) |
| `items[UPDATE_DESIGN].css.custom_js` | String | — |  |  |  | Custom JS của form — áp vào public form | §5 css (L715) |
| `items[UPDATE_MESSAGE_ACTION].type` | String | ✔ |  |  |  | Cố định `"UPDATE_MESSAGE_ACTION"` | §5 UPDATE_MESSAGE_ACTION (L736) |
| `items[UPDATE_MESSAGE_ACTION].reply_message` | String | — |  |  | tối đa 5000 ký tự | 回答完了時に送信するメッセージ — message gửi cho friend ngay sau khi submit, tối đa 5000 ký tự. Hỗ trợ token `{name}` (tên hiển thị của friend) | §5 UPDATE_MESSAGE_ACTION (L737) |
| `items[UPDATE_MESSAGE_ACTION].use_reply_message` | Boolean | — |  |  |  | Bật/tắt gửi message trên. Truyền reply_message mà bỏ trống field này = tự bật | §5 UPDATE_MESSAGE_ACTION (L738) |
| `items[UPDATE_MESSAGE_ACTION].send_qa_copy` | Boolean | — |  |  |  | 質問と回答のコピーメッセージを送る — gửi kèm bản copy toàn bộ câu hỏi + câu trả lời sau message trên. Default false | §5 UPDATE_MESSAGE_ACTION (L739) |
| `items[UPDATE_MESSAGE_ACTION].reply_frequency` | String | — | ONCE / EVERY_TIME |  |  | アクションの稼働回数 (khối hoàn thành): `ONCE` (1度のみ — chỉ chạy lần submit đầu) / `EVERY_TIME` (何度でも — chạy mọi lần) | §5 UPDATE_MESSAGE_ACTION (L740) |
| `items[UPDATE_MESSAGE_ACTION].reply_action_id` | Long · ID | — |  |  |  | 回答完了時アクション — ID action chain (từ create_action) chạy khi friend submit. Truyền `0` = gỡ action | §5 UPDATE_MESSAGE_ACTION (L741) |
| `items[UPDATE_MESSAGE_ACTION].open_frequency` | String | — | ONCE / EVERY_TIME |  |  | アクションの稼働回数 (khối mở form): `ONCE` / `EVERY_TIME` | §5 UPDATE_MESSAGE_ACTION (L742) |
| `items[UPDATE_MESSAGE_ACTION].open_action_id` | Long · ID | — |  |  |  | フォーム表示時アクション — ID action chain chạy khi friend mở form. Truyền `0` = gỡ action | §5 UPDATE_MESSAGE_ACTION (L743) |
| `items[UPDATE_MESSAGE_ACTION].reminders` | Array | — |  |  |  | リマインドメッセージ — cấu hình nhắc hẹn (xem bảng dưới). Step được lưu theo form (1 bộ step/form, không theo field) → mỗi phần tử REPLACE toàn bộ danh sách step của FORM. Chỉ gửi 1 phần tử — gửi nhiều phần tử thì phần tử sau ghi đè phần tử trước | §5 UPDATE_MESSAGE_ACTION (L744) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].field_id` | Long · ID | ✔ |  |  |  | ID field REMINDER trên form — chỉ dùng để xác nhận form có field REMINDER hợp lệ (step lưu theo form, không gắn riêng field này) | §5 Reminder (L749) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps` | Array | ✔ |  |  |  | Danh sách step nhắc — REPLACE toàn bộ step hiện có của form (step không gửi sẽ bị xóa) | §5 Reminder (L750) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].id` | Long · ID | — |  |  |  | ID step khi sửa (bỏ trống = tạo mới) | §5 Reminder Step (L755) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].timing_type` | String | ✔ | DAYS_BEFORE / HOURS_BEFORE |  |  | `DAYS_BEFORE` = 配信終了日の N日前 HH:mm に配信 / `HOURS_BEFORE` = 配信終了日の H時間M分前に配信 | §5 Reminder Step (L756) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].days_before` | Integer | — |  |  |  | Số ngày trước hạn (timing_type=DAYS_BEFORE) | §5 Reminder Step (L757) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].send_time` | String | — |  |  |  | Giờ gửi `HH:mm` (timing_type=DAYS_BEFORE) | §5 Reminder Step (L758) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].hours_before` | Integer | — |  |  | 0–23 | Số giờ trước hạn, 0–23 (timing_type=HOURS_BEFORE) | §5 Reminder Step (L759) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].minutes_before` | Integer | — |  |  | 0–59 | Số phút trước hạn, 0–59 (timing_type=HOURS_BEFORE). Tổng tối đa 23h59m | §5 Reminder Step (L760) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].message` | String | — |  |  | tối đa 5000 ký tự | Nội dung nhắc, tối đa 5000 ký tự | §5 Reminder Step (L761) |
| `items[UPDATE_MESSAGE_ACTION].reminders[].steps[].action_id` | Long · ID | — |  |  |  | Action chain chạy khi tới giờ nhắc. message hoặc action_id phải có ít nhất 1 | §5 Reminder Step (L762) |
| `items[UPDATE_DIAGNOSTIC].type` | String | ✔ |  |  |  | Cố định `"UPDATE_DIAGNOSTIC"` | §5 UPDATE_DIAGNOSTIC (L799) |
| `items[UPDATE_DIAGNOSTIC].enabled` | Boolean | — |  |  |  | Bật/tắt tính năng chẩn đoán. Không tắt được khi form còn field DIAGNOSTIC (web chặn) | §5 UPDATE_DIAGNOSTIC (L800) |
| `items[UPDATE_DIAGNOSTIC].point_field_id` | Long · ID | — |  |  |  | Friend info field loại POINT dùng lưu tổng điểm của friend (từ list_friend_info_fields) | §5 UPDATE_DIAGNOSTIC (L801) |
| `items[UPDATE_DIAGNOSTIC].point_ranges` | Array | — |  |  |  | Dải điểm → phản hồi. REPLACE toàn bộ — dải không gửi sẽ bị xóa | §5 UPDATE_DIAGNOSTIC (L802) |
| `items[UPDATE_DIAGNOSTIC].point_ranges[].id` | Long · ID | — |  |  |  | ID dải khi sửa (bỏ trống = tạo mới) | §5 Point Range (L807) |
| `items[UPDATE_DIAGNOSTIC].point_ranges[].from_point` | Integer | ✔ |  |  |  | Điểm bắt đầu (bao gồm). Ràng buộc `from_point <= to_point`, các dải không được chồng nhau | §5 Point Range (L808) |
| `items[UPDATE_DIAGNOSTIC].point_ranges[].to_point` | Integer | ✔ |  |  |  | Điểm kết thúc (bao gồm) | §5 Point Range (L809) |
| `items[UPDATE_DIAGNOSTIC].point_ranges[].message` | String | — |  |  | tối đa 5000 ký tự | Message gửi khi tổng điểm rơi vào dải, tối đa 5000 ký tự | §5 Point Range (L810) |
| `items[UPDATE_DIAGNOSTIC].point_ranges[].action_id` | Long · ID | — |  |  |  | Action chain chạy khi rơi vào dải. message hoặc action_id phải có ít nhất 1 | §5 Point Range (L811) |
| `items[UPDATE_SETTINGS].type` | String | ✔ |  |  |  | Cố định `"UPDATE_SETTINGS"` | §5 UPDATE_SETTINGS (L833) |
| `items[UPDATE_SETTINGS].line_display_name` | String | — |  |  | tối đa 20 ký tự | お客様に表示されるフォーム名 / フォーム名 — tên form hiển thị cho người trả lời trên màn hình talk LINE, tối đa 20 ký tự | §5 UPDATE_SETTINGS (L834) |
| `items[UPDATE_SETTINGS].system_name` | String | — |  |  | tối đa 50 ký tự | 管理名 — tên quản lý nội bộ của form, tối đa 50 ký tự | §5 UPDATE_SETTINGS (L835) |
| `items[UPDATE_SETTINGS].line_talk_title` | String | — |  |  | tối đa 20 ký tự | LINEトーク画面表示 → タイトル — tiêu đề link preview khi gửi URL form lên LINE talk, tối đa 20 ký tự | §5 UPDATE_SETTINGS (L836) |
| `items[UPDATE_SETTINGS].line_talk_description` | String | — |  |  | tối đa 50 ký tự | LINEトーク画面表示 → 説明 — mô tả link preview, tối đa 50 ký tự | §5 UPDATE_SETTINGS (L837) |
| `items[UPDATE_SETTINGS].reply_limit` | Object | — |  |  |  | 回答制限 — giới hạn số lần trả lời mỗi friend | §5 UPDATE_SETTINGS (L838) |
| `items[UPDATE_SETTINGS].total_limit` | Object | — |  |  |  | 回答数の上限 — giới hạn tổng số câu trả lời toàn form | §5 UPDATE_SETTINGS (L839) |
| `items[UPDATE_SETTINGS].not_public` | Object | — |  |  |  | 非公開時の表示 — hiển thị khi form ở trạng thái không công khai (非公開) | §5 UPDATE_SETTINGS (L840) |
| `items[UPDATE_SETTINGS].confirm_page` | Boolean | — |  |  |  | 回答確認ページ — true = hiện trang xác nhận trước khi submit | §5 UPDATE_SETTINGS (L841) |
| `items[UPDATE_SETTINGS].after_submit` | Object | — |  |  |  | 回答後ページ遷移設定 — trang sau khi submit | §5 UPDATE_SETTINGS (L842) |
| `items[UPDATE_SETTINGS].countdown` | Object | — |  |  |  | カウントダウンタイマー | §5 UPDATE_SETTINGS (L843) |
| `items[UPDATE_SETTINGS].show_duration` | Object | — |  |  |  | 回答時間表示 — đếm/hiển thị thời gian trả lời | §5 UPDATE_SETTINGS (L844) |
| `items[UPDATE_SETTINGS].reply_limit.enabled` | Boolean | ✔ |  |  |  | false = 何度でも (không giới hạn); true = giới hạn số lần | §5 reply_limit (L849) |
| `items[UPDATE_SETTINGS].reply_limit.max_per_friend` | Integer | — |  |  | (≥1) | Số lần trả lời tối đa mỗi friend (≥1) — bắt buộc khi enabled=true | §5 reply_limit (L850) |
| `items[UPDATE_SETTINGS].reply_limit.over_display` | String | — | TEXT / URL | TEXT |  | Khi chạm giới hạn: `TEXT` (hiện message, default) / `URL` (chuyển trang) | §5 reply_limit (L851) |
| `items[UPDATE_SETTINGS].reply_limit.message` | String | — |  |  | tối đa 50 ký tự | Message khi chạm giới hạn, tối đa 50 ký tự. Default: あなたがこのフォームに回答できる上限に達しました。 | §5 reply_limit (L852) |
| `items[UPDATE_SETTINGS].reply_limit.redirect_url` | String | — |  |  |  | URL chuyển tới khi over_display=URL | §5 reply_limit (L853) |
| `items[UPDATE_SETTINGS].total_limit.enabled` | Boolean | ✔ |  |  |  | true = giới hạn tổng số câu trả lời của cả form | §5 total_limit (L858) |
| `items[UPDATE_SETTINGS].total_limit.max_total` | Integer | — |  |  | (≥1) | Tổng số câu trả lời tối đa (≥1) — bắt buộc khi enabled=true | §5 total_limit (L859) |
| `items[UPDATE_SETTINGS].total_limit.over_display` | String | — | TEXT / URL | TEXT |  | `TEXT` (default) / `URL` | §5 total_limit (L860) |
| `items[UPDATE_SETTINGS].total_limit.message` | String | — |  |  | tối đa 50 ký tự | Message khi đủ số lượng, tối đa 50 ký tự | §5 total_limit (L861) |
| `items[UPDATE_SETTINGS].total_limit.redirect_url` | String | — |  |  |  | URL chuyển tới khi over_display=URL | §5 total_limit (L862) |
| `items[UPDATE_SETTINGS].not_public.display` | String | — | TEXT / URL | TEXT |  | `TEXT` (hiện message, default) / `URL` (chuyển trang) | §5 not_public (L867) |
| `items[UPDATE_SETTINGS].not_public.message` | String | — |  |  | tối đa 50 ký tự | Message khi form非公開, tối đa 50 ký tự. Default: このフォームは回答を受け付けていません。 | §5 not_public (L868) |
| `items[UPDATE_SETTINGS].not_public.redirect_url` | String | — |  |  |  | URL chuyển tới khi display=URL | §5 not_public (L869) |
| `items[UPDATE_SETTINGS].after_submit.mode` | String | ✔ | RETURN_TO_TALK / SHOW_PAGE / REDIRECT_URL | RETURN_TO_TALK |  | `RETURN_TO_TALK` = 回答後ページを表示せずにトーク画面に戻る (default của web) / `SHOW_PAGE` = hiện trang cảm ơn (kèm message) / `REDIRECT_URL` = chuyển tới URL chỉ định | §5 after_submit (L874) |
| `items[UPDATE_SETTINGS].after_submit.message` | String | — |  |  |  | Nội dung trang cảm ơn — dùng khi mode=SHOW_PAGE | §5 after_submit (L875) |
| `items[UPDATE_SETTINGS].after_submit.redirect_url` | String | — |  |  |  | URL đích — bắt buộc khi mode=REDIRECT_URL | §5 after_submit (L876) |
| `items[UPDATE_SETTINGS].countdown.enabled` | Boolean | ✔ | false / true |  |  | `false` = tắt; `true` = bật hạn hiển thị. Lưu ý: đổi cấu hình timer khiến friend phải xác nhận lại form | §5 countdown (L881) |
| `items[UPDATE_SETTINGS].countdown.show_timer` | Boolean | — | false / true | false |  | `false` (default) = chỉ đặt hạn (form tự khóa sau hạn, không hiện đồng hồ); `true` = hiện đồng hồ đếm ngược. Các field tạo kiểu timer bên dưới cần `show_timer=true` | §5 countdown (L882) |
| `items[UPDATE_SETTINGS].countdown.deadline_type` | String | — | DATE / DURATION / ONE_TIME | DATE |  | Loại hạn: `DATE` (default — mốc ngày/giờ cố định) / `DURATION` (theo khoảng thời gian từ lúc mở form) / `ONE_TIME` (chỉ hiện 1 lần, không timer) | §5 countdown (L883) |
| `items[UPDATE_SETTINGS].countdown.date` | String | — |  |  |  | [DATE] Ngày đích `YYYY-MM-DD` — bắt buộc khi enabled=true & deadline_type=DATE | §5 countdown (L884) |
| `items[UPDATE_SETTINGS].countdown.time` | String | — |  |  |  | [DATE] Giờ đích `HH:mm` | §5 countdown (L885) |
| `items[UPDATE_SETTINGS].countdown.duration_days` | Integer | — |  |  |  | [DURATION] Số ngày từ lúc mở form — bắt buộc khi deadline_type=DURATION | §5 countdown (L886) |
| `items[UPDATE_SETTINGS].countdown.duration_mode` | String | — | OFFSET / CLOCK |  |  | [DURATION] `OFFSET` (kết thúc sau N ngày + H giờ M phút — dùng duration_hours/minutes) / `CLOCK` (kết thúc tại giờ đồng hồ ngày cuối — dùng duration_end_time). Default OFFSET | §5 countdown (L887) |
| `items[UPDATE_SETTINGS].countdown.duration_hours` | Integer | — |  |  | 0–23 | [DURATION/OFFSET] Số giờ 0–23 cộng thêm | §5 countdown (L888) |
| `items[UPDATE_SETTINGS].countdown.duration_minutes` | Integer | — |  |  | 0–59 | [DURATION/OFFSET] Số phút 0–59 cộng thêm | §5 countdown (L889) |
| `items[UPDATE_SETTINGS].countdown.duration_end_time` | String | — |  |  |  | [DURATION/CLOCK] Giờ kết thúc `HH:mm` ở ngày cuối | §5 countdown (L890) |
| `items[UPDATE_SETTINGS].countdown.expired_message` | String | — |  |  |  | Message khi hết giờ | §5 countdown (L891) |
| `items[UPDATE_SETTINGS].countdown.expired_display` | String | — | TEXT / URL | TEXT |  | `TEXT` (default) / `URL` | §5 countdown (L892) |
| `items[UPDATE_SETTINGS].countdown.expired_url` | String | — |  |  |  | URL chuyển tới khi hết giờ (expired_display=URL) | §5 countdown (L893) |
| `items[UPDATE_SETTINGS].countdown.timer_label` | String | — |  |  |  | [show_timer=true] Nhãn timer (タイマー文言, vd 終了まであと). Dùng chung cột `title_timer` với `show_duration.display_text` — set cái này đè cái kia | §5 countdown (L894) |
| `items[UPDATE_SETTINGS].countdown.pin_top` | Boolean | — |  | true |  | [show_timer=true] `true` (default) = ghim timer ở đầu trang | §5 countdown (L895) |
| `items[UPDATE_SETTINGS].countdown.precision` | String | — | CENTISECOND / SECOND / MINUTE |  |  | [show_timer=true] Độ chính xác: `CENTISECOND` (0.01s) / `SECOND` / `MINUTE`. Default CENTISECOND | §5 countdown (L896) |
| `items[UPDATE_SETTINGS].countdown.text_color` | String | — |  |  |  | [show_timer=true] Màu chữ timer `#RRGGBB` | §5 countdown (L897) |
| `items[UPDATE_SETTINGS].countdown.bg_color` | String | — |  |  |  | [show_timer=true] Màu nền timer `#RRGGBB` | §5 countdown (L898) |
| `items[UPDATE_SETTINGS].show_duration.enabled` | Boolean | ✔ |  |  |  | Bật/tắt hiển thị thời gian trả lời cho người trả lời | §5 show_duration (L903) |
| `items[UPDATE_SETTINGS].show_duration.display_text` | String | — |  |  | tối đa 50 ký tự | Text hiển thị kèm, tối đa 50 ký tự — bắt buộc khi enabled=true. Dùng chung cột `title_timer` với `countdown.timer_label` — set cái này đè cái kia | §5 show_duration (L904) |
| `items[ADD_FIELD/UPDATE_FIELD].field.field_type` | String | ✔ |  |  |  | Loại field (enum ở trên) | §5 Field chung (L965) |
| `items[ADD_FIELD/UPDATE_FIELD].field.label` | String | ✔ |  |  | tối đa 50 ký tự | 質問文 — nội dung câu hỏi hiển thị, tối đa 50 ký tự, bắt buộc với mọi câu hỏi nhóm 1 + 2 (nhóm trang trí có quy định riêng — xem từng loại) | §5 Field chung (L966) |
| `items[ADD_FIELD/UPDATE_FIELD].field.help` | String | — |  |  | tối đa 200 ký tự | 補足 — text bổ trợ dưới câu hỏi, tối đa 200 ký tự | §5 Field chung (L967) |
| `items[ADD_FIELD/UPDATE_FIELD].field.placeholder` | String | — |  |  | tối đa 50 ký tự | Placeholder, tối đa 50 ký tự — chỉ TEXT/TEXTAREA/NAME/EMAIL/PHONE | §5 Field chung (L968) |
| `items[ADD_FIELD/UPDATE_FIELD].field.required` | Boolean | — |  |  |  | 必須/任意 — bắt buộc trả lời. Default `true` (giống web khi thêm mới) | §5 Field chung (L969) |
| `items[ADD_FIELD/UPDATE_FIELD].field.css_question_class` | String | — |  |  |  | CSSクラス指定・質問文 — CSS class áp cho phần 質問文 của field này (câu hỏi + HEADING) | §5 Field chung (L970) |
| `items[ADD_FIELD/UPDATE_FIELD].field.css_help_class` | String | — |  |  |  | CSSクラス指定・質問文補足 — CSS class áp cho phần 補足 của field này (câu hỏi + HEADING) | §5 Field chung (L971) |
| `items[ADD_FIELD/UPDATE_FIELD].field.css_options_class` | String | — |  |  |  | CSSクラス指定 slot thứ 3 theo loại: lựa chọn (SELECT/CHECKBOX/GENDER/DIAGNOSTIC), ô nhập địa chỉ (ADDRESS), hoặc đường kẻ (DIVIDER) | §5 Field chung (L972) |
| `items[ADD_FIELD/UPDATE_FIELD].field[TEXT/TEXTAREA].input_restriction` | String | — | email / tel / kana / numeric / date_format |  | 10–12 | 入力制限 — chỉ `TEXT` (TEXTAREA không có): `email` / `tel` / `kana` / `numeric` / `date_format`. Bỏ trống = không giới hạn. `tel` → validate 10–12 chữ số | §5 field TEXT/TEXTAREA (L979) |
| `items[ADD_FIELD/UPDATE_FIELD].field[TEXT/TEXTAREA].link_friend_info` | Boolean | — |  |  |  | 友だち情報に回答を記録 (tự tạo field mới) — true = tự tạo friend info field từ câu hỏi này. Default false | §5 field TEXT/TEXTAREA (L980) |
| `items[ADD_FIELD/UPDATE_FIELD].field[TEXT/TEXTAREA].friend_info_id` | Long · ID | — |  |  |  | Ghi vào friend info field có sẵn: -1 (tên hiển thị) / -2 (SĐT) / -3 (email) hoặc ID dương loại 記述 (từ list_friend_info_fields). Loại trừ lẫn nhau với link_friend_info | §5 field TEXT/TEXTAREA (L981) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DATE].default_date_type` | Integer | — | 1 / 2 / 0 | 1 |  | デフォルト日付: `1` = ngày hiện tại (default), `2` = ngày chỉ định (kèm default_date), `0` = để trống | §5 field DATE (L986) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DATE].default_date` | String | — |  |  |  | Ngày chỉ định `YYYY-MM-DD` — dùng khi default_date_type=2 | §5 field DATE (L987) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DATE].record_time` | Boolean | — |  |  |  | 時間の記録 — true = thu thêm giờ (HH:mm) ngoài ngày. Default false. Bật true thì tính năng lưu vào friend info bên dưới KHÔNG dùng được (web ẩn khối 友だち情報に回答を記録 — giá trị ngày+giờ không lưu vào field friend info loại ngày được) | §5 field DATE (L988) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DATE].link_friend_info` | Boolean | — |  |  |  | 友だち情報に回答を記録 (tự tạo field mới) — true = tự tạo 1 friend info field mới loại ngày-giờ từ câu hỏi này rồi lưu câu trả lời vào đó. Chỉ dùng khi record_time=false. Default false. Loại trừ lẫn nhau với friend_info_id | §5 field DATE (L989) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DATE].friend_info_id` | Long · ID | — |  |  |  | Lưu câu trả lời vào friend info field có sẵn. Chỉ dùng khi record_time=false. Giá trị hợp lệ (theo dropdown web): `-5` = field hệ thống 生年月日 (Ngày sinh) — lưu ý mã là -5, khác preset BIRTHDAY dùng -4; hoặc ID dương của field friend info loại ngày-giờ (日時タイプ) d | §5 field DATE (L990) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].display` | String | — | radio / dropdown | radio |  | 表示方法: `radio` (nút radio, default) / `dropdown` (danh sách thả xuống) | §5 field SELECT (L995) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].options` | Array | ✔ |  |  | tối đa 100 | Danh sách lựa chọn, tối đa 100, mỗi option `{label}` — label bắt buộc, không được trùng nhau | §5 field SELECT (L996) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].record_mode` | String | — | none / tags / friend_info | none |  | 回答情報の連携: `none` (default) / `tags` (mỗi option gắn với 1 tag theo label — tag chưa có sẽ tự tạo khi friend trả lời, không cần tạo trước) / `friend_info` (ghi vào friend info) | §5 field SELECT (L997) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].link_friend_info` |  | — |  |  |  | Khi record_mode=friend_info: tự tạo mới hoặc chọn field có sẵn — friend_info_id phải đúng kiểu (SELECT → field kiểu select hoặc text; sai kiểu, không tồn tại hoặc của bot khác → lỗi) | §5 field SELECT (L998) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].friend_info_id` |  · ID | — |  |  |  | Khi record_mode=friend_info: tự tạo mới hoặc chọn field có sẵn — friend_info_id phải đúng kiểu (SELECT → field kiểu select hoặc text; sai kiểu, không tồn tại hoặc của bot khác → lỗi) | §5 field SELECT (L998) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT].auto_add_other` | Boolean | — |  |  |  | その他自動追加 — tự thêm lựa chọn "その他" (nhập tự do). Chỉ khi record_mode=none. Default true trên web | §5 field SELECT (L999) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CHECKBOX].options` | Array | ✔ |  |  |  | Tối đa 100 option `{label}`, label bắt buộc, không trùng | §5 field CHECKBOX (L1004) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CHECKBOX].selection_limit` | Object | — |  |  |  | 選択数の制限 `{from, to}` — số lựa chọn tối thiểu/tối đa, ràng buộc `0 <= from < to` | §5 field CHECKBOX (L1005) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CHECKBOX].record_mode` | String | — | none / tags |  |  | Chỉ `none` / `tags`. KHÔNG hỗ trợ friend_info (nhiều lựa chọn không map được vào 1 field). Không có auto_add_other | §5 field CHECKBOX (L1006) |
| `items[ADD_FIELD/UPDATE_FIELD].field[FILE_UPLOAD].file_type` | Integer | — | 1 / 2 / 3 / 4 / 5 | 1 | ≤10MB · ≤200MB · ≤50MB | ファイルの指定: `1` = ảnh (≤10MB, default), `2` = video (≤200MB, .mov), `3` = âm thanh, `4` = PDF (≤50MB), `5` = không chỉ định | §5 field FILE_UPLOAD (L1011) |
| `items[ADD_FIELD/UPDATE_FIELD].field[FILE_UPLOAD].link_friend_info` |  | — |  |  |  | Chỉ khi file_type = 1 (ảnh) hoặc 4 (PDF) | §5 field FILE_UPLOAD (L1012) |
| `items[ADD_FIELD/UPDATE_FIELD].field[FILE_UPLOAD].friend_info_id` |  · ID | — |  |  |  | Chỉ khi file_type = 1 (ảnh) hoặc 4 (PDF) | §5 field FILE_UPLOAD (L1012) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].display` | String | — | radio / checkbox | radio |  | `radio` (đơn chọn, default) / `checkbox` (nhiều chọn) | §5 field DIAGNOSTIC (L1017) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].options` | Array | ✔ |  |  |  | Tối đa 100 option `{label, point}` — `point` (số nguyên, cho phép âm) là điểm cộng khi chọn, bắt buộc mỗi option | §5 field DIAGNOSTIC (L1018) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].link_friend_info` |  | — |  |  |  | Chỉ khi display=radio (field loại selection). Checkbox không link được | §5 field DIAGNOSTIC (L1019) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].friend_info_id` |  · ID | — |  |  |  | Chỉ khi display=radio (field loại selection). Checkbox không link được | §5 field DIAGNOSTIC (L1019) |
| `items[ADD_FIELD/UPDATE_FIELD].field[REMINDER].options` | Array | ✔ |  |  |  | Tối đa 100 option `{label, end_date, end_time}` — mỗi option là 1 mốc nhắc: label bắt buộc; `end_date` (YYYY-MM-DD, ≥ hôm nay) + `end_time` (HH:mm) = hạn đăng ký. Sau khi save không đổi được date/time của option | §5 field REMINDER (L1026) |
| `items[ADD_FIELD/UPDATE_FIELD].field[POLICY].label` | String | ✔ |  |  | tối đa 50 ký tự | 案内文 (tiêu đề hiển thị), tối đa 50 ký tự. Default web: ご利用規約 | §5 field POLICY (L1033) |
| `items[ADD_FIELD/UPDATE_FIELD].field[POLICY].terms` | String | ✔ |  |  | tối đa 20.000 ký tự | 規約 — nội dung điều khoản, tối đa 20.000 ký tự | §5 field POLICY (L1034) |
| `items[ADD_FIELD/UPDATE_FIELD].field[POLICY].checkbox_text` | String | ✔ |  |  | tối đa 50 ký tự | チェックボックスの案内文, tối đa 50 ký tự. Default web: 規約に同意します | §5 field POLICY (L1035) |
| `items[ADD_FIELD/UPDATE_FIELD].field[NAME].placeholder` |  |  |  |  | ≤50 | placeholder (≤50), input_restriction · Luôn ghi vào tên hiển thị hệ thống (-1) | §5 preset (L1044) |
| `items[ADD_FIELD/UPDATE_FIELD].field[NAME].input_restriction` |  |  |  |  | ≤50 | placeholder (≤50), input_restriction · Luôn ghi vào tên hiển thị hệ thống (-1) | §5 preset (L1044) |
| `items[ADD_FIELD/UPDATE_FIELD].field[EMAIL].placeholder` |  |  |  |  | ≤50 | placeholder (≤50) · Validate định dạng email; ghi vào -3 | §5 preset (L1045) |
| `items[ADD_FIELD/UPDATE_FIELD].field[PHONE].placeholder` |  |  |  |  | ≤50 · 10–12 | placeholder (≤50) · Validate 10–12 chữ số; ghi vào -2 | §5 preset (L1046) |
| `items[ADD_FIELD/UPDATE_FIELD].field[BIRTHDAY].default_date_type` |  |  |  |  |  | default_date_type / default_date · Như DATE nhưng chỉ ngày (không time); ghi vào -4 | §5 preset (L1047) |
| `items[ADD_FIELD/UPDATE_FIELD].field[BIRTHDAY].default_date` |  |  |  |  |  | default_date_type / default_date · Như DATE nhưng chỉ ngày (không time); ghi vào -4 | §5 preset (L1047) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders` |  |  |  |  |  | address_placeholders (object, optional) · 5 ô con: zip_code / province / district / township / building — chỉ sửa được placeholder từng ô; building luôn optional, 4 ô còn lại required theo `required` của field; ghi vào -11 | §5 preset (L1048) |
| `items[ADD_FIELD/UPDATE_FIELD].field[GENDER].display` |  |  |  |  |  | display (radio\ · dropdown), options (default 男性/女性) | §5 preset (L1049) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].label` | String | ✔ |  |  | tối đa 50 ký tự | Text tiêu đề, tối đa 50 ký tự | §5 field HEADING (L1058) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].sub_text` | String | — |  |  | tối đa 200 ký tự | Text phụ dưới tiêu đề, tối đa 200 ký tự | §5 field HEADING (L1059) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].pattern` | Integer | — | 1 / 2 / 3 | 1 |  | Kiểu thiết kế `1`/`2`/`3` (default 1) | §5 field HEADING (L1060) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].text_color` | String | — |  | #FFFFFF |  | Màu chữ `#RRGGBB` (default #FFFFFF) | §5 field HEADING (L1061) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].bg_color` | String | — |  | #RRGGBB |  | Màu nền (pattern 1) / màu kẻ (pattern 2,3) `#RRGGBB` (default theo 共通デザイン設定 — form mới: #5799DB) | §5 field HEADING (L1062) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].font_weight` | Integer | — | 600 / 300 | 600 |  | `600` (đậm, default) / `300` (mảnh) | §5 field HEADING (L1063) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].font_size` | Integer | — | 24 / 20 / 16 | 24 |  | `24` (lớn, default) / `20` (vừa) / `16` (nhỏ) | §5 field HEADING (L1064) |
| `items[ADD_FIELD/UPDATE_FIELD].field[HEADING].text_align` | String | — | left / center / right | center |  | `left` / `center` (default) / `right` | §5 field HEADING (L1065) |
| `items[ADD_FIELD/UPDATE_FIELD].field[TEXT_BLOCK].content` | String | ✔ |  |  |  | Nội dung text/HTML tự do (web dùng rich-text editor) — không giới hạn độ dài | §5 field TEXT_BLOCK (L1070) |
| `items[ADD_FIELD/UPDATE_FIELD].field[IMAGE].image_url` | String | ✔ |  |  | tối đa 2048 · ≤ 10MB · ≤10000 | URL ảnh — dùng `download_url` từ `get_file_params`. Web giới hạn png/jpg ≤ 10MB, ≤10000px (server tự resize về tối đa 2048px) | §5 field IMAGE (L1075) |
| `items[ADD_FIELD/UPDATE_FIELD].field[IMAGE].is_full_width` | Boolean | — |  |  |  | Hiển thị full chiều ngang màn hình. Default false | §5 field IMAGE (L1076) |
| `items[ADD_FIELD/UPDATE_FIELD].field[VIDEO].video_url` | String | ✔ |  |  |  | Chỉ nhận URL YouTube hoặc Vimeo (không nhận mã nhúng iframe) | §5 field VIDEO (L1081) |
| `items[ADD_FIELD/UPDATE_FIELD].field[VIDEO].is_full_width` | Boolean | — |  |  |  | Hiển thị full chiều ngang. Default false | §5 field VIDEO (L1082) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIVIDER].pattern` | Integer | — | 1 / 2 / 3 | 1 |  | Kiểu đường kẻ `1`/`2`/`3` (default 1) | §5 field DIVIDER (L1087) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIVIDER].color` | String | — |  | #RRGGBB |  | Màu `#RRGGBB` (default theo 共通デザイン設定 — form mới: #5799DB) | §5 field DIVIDER (L1088) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIVIDER].width` | Integer | — | 350 / 250 / 150 | 350 |  | Độ dài: `350` (dài, default) / `250` (vừa) / `150` (ngắn) | §5 field DIVIDER (L1089) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CUSTOM_HTML].label` | String | ✔ |  |  | tối đa 50 ký tự | Tiêu đề, tối đa 50 ký tự | §5 field CUSTOM_HTML (L1094) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CUSTOM_HTML].html` | String | ✔ |  |  |  | Mã HTML/CSS tự do — không giới hạn độ dài, render nguyên trạng trên public form | §5 field CUSTOM_HTML (L1095) |
| `items[SET_NEXT_PAGE].branches[].option_label` | String |  |  |  |  | Phải khớp label lựa chọn hiện tại của câu hỏi (server đối chiếu theo label) | §5 SET_NEXT_PAGE (mô tả inline) (L616) |
| `items[SET_NEXT_PAGE].branches[].next_page_id` | Long · ID |  |  |  |  | 0 hoặc null = 回答完了ページ. Option không có trong mảng theo đích phần tử đầu tiên | §5 SET_NEXT_PAGE (mô tả inline) (L616) |
| `items[ADD_FIELD/UPDATE_FIELD].field[SELECT/CHECKBOX/GENDER].options[].label` | String | ✔ |  |  | tối đa 100 | label bắt buộc, không được trùng nhau; tối đa 100 option | §5 field SELECT/CHECKBOX (inline) (L979) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].options[].label` | String | ✔ |  |  | tối đa 100 | label bắt buộc; tối đa 100 option | §5 field DIAGNOSTIC (inline) (L1001) |
| `items[ADD_FIELD/UPDATE_FIELD].field[DIAGNOSTIC].options[].point` | Integer | ✔ |  |  |  | số nguyên, cho phép âm, bắt buộc mỗi option | §5 field DIAGNOSTIC (inline) (L1001) |
| `items[ADD_FIELD/UPDATE_FIELD].field[REMINDER].options[].label` | String | ✔ |  |  | tối đa 100 | label bắt buộc; tối đa 100 option | §5 field REMINDER (inline) (L1009) |
| `items[ADD_FIELD/UPDATE_FIELD].field[REMINDER].options[].end_date` | String |  |  |  |  | YYYY-MM-DD, ≥ hôm nay. Sau khi save không đổi được | §5 field REMINDER (inline) (L1009) |
| `items[ADD_FIELD/UPDATE_FIELD].field[REMINDER].options[].end_time` | String |  |  |  |  | HH:mm. Sau khi save không đổi được | §5 field REMINDER (inline) (L1009) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CHECKBOX].selection_limit.from` | Integer |  |  |  |  | 0 <= from < to | §5 field CHECKBOX (inline) (L988) |
| `items[ADD_FIELD/UPDATE_FIELD].field[CHECKBOX].selection_limit.to` | Integer |  |  |  |  | 0 <= from < to | §5 field CHECKBOX (inline) (L988) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders.zip_code` | String |  |  |  |  | Chỉ sửa placeholder ô con; building luôn optional, 4 ô còn lại required theo required của field | §5 preset ADDRESS (inline) (L1031) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders.province` | String |  |  |  |  | Chỉ sửa placeholder ô con; building luôn optional, 4 ô còn lại required theo required của field | §5 preset ADDRESS (inline) (L1031) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders.district` | String |  |  |  |  | Chỉ sửa placeholder ô con; building luôn optional, 4 ô còn lại required theo required của field | §5 preset ADDRESS (inline) (L1031) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders.township` | String |  |  |  |  | Chỉ sửa placeholder ô con; building luôn optional, 4 ô còn lại required theo required của field | §5 preset ADDRESS (inline) (L1031) |
| `items[ADD_FIELD/UPDATE_FIELD].field[ADDRESS].address_placeholders.building` | String |  |  |  |  | Chỉ sửa placeholder ô con; building luôn optional, 4 ô còn lại required theo required của field | §5 preset ADDRESS (inline) (L1031) |

Tổng: 5 tool · 246 param · 32 param ID
