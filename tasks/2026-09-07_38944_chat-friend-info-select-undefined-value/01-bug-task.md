# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38944 — ErrorException: Undefined property: stdClass::$value in /var/www/html/sns-line/app/Http/Controllers/ChatController.php:4471` |
| Module / Màn hình | `Chat 1:1 — cột phải tab 「友だち情報」 (thông tin bạn bè), lưu 1 mục thông tin bạn bè kiểu 「選択肢」 (lựa chọn) — hàm saveSettingDisplayInfoItem` |

## Mô tả bug (bản dịch tiếng Việt)

Ticket dạng **Bug tự detect** (tracker `Bug tự detect`) — nội dung Redmine **không phải mô tả của khách hàng** mà là **log production** do hệ thống tự bắt. Diễn giải nội dung log:

- Lúc `2026-07-21 08:19:39` trên **production**, hàm `saveSettingDisplayInfoItem` của `ChatController` bắt đầu chạy (`saveSettingDisplayInfoItem start`).
- Dữ liệu gửi lên (`$infos`) là **1 mục thông tin bạn bè kiểu 「選択肢」** (`type_data: 1`) tên 「🚫ロードマップ案内🚫」, có **4 lựa chọn và cả 4 đều gắn action** (`action_id` 23 / 34 / 45 / 56). Chuỗi này **chỉ có `valueOption`** (danh sách lựa chọn) — **KHÔNG có trường `value`** ở cấp trên cùng (giá trị đã chọn).
- `$lineId` = `21`.
- Ngay sau đó hệ thống ghi `saveSettingDisplayInfoItem error`, rồi báo lỗi `ErrorException: Undefined property: stdClass::$value` tại `ChatController.php:4471` — tức code đọc thẳng thuộc tính `value` của dữ liệu gửi lên mà không kiểm tra tồn tại.

Nguyên văn log trong Redmine (giữ nguyên, không dịch — là dữ liệu kỹ thuật; ký tự JP đã khôi phục từ mojibake của Redmine):

```
[2026-07-21 08:19:39] production.INFO: saveSettingDisplayInfoItem start
[2026-07-21 08:19:39] production.INFO: Log action: saveSettingDisplayInfoItem ChatController
[2026-07-21 08:19:39] production.DEBUG: $infos: {"id":1,"bot_id":1,"type":1,"id_setting":1,"line_id":null,"order":5,"title":"🚫ロードマップ案内🚫","created_at":"2026-06-29 09:33:30","updated_at":"2026-07-16 10:07:12","type_data":1,"valueOption":[{"action_id":"23","value":"📧ロードマップの案内をする（進行中の方向け）","id":23},{"action_id":"34","value":"📧ロードマップの案内をする（完成の方向け）","id":34},{"action_id":"45","value":"📧ロードマップの案内をする（解約の人向け）","id":45},{"action_id":"56","value":"📧新機能の案内をする（凍結バージョン）","id":56}]}
[2026-07-21 08:19:39] production.DEBUG: $lineId: 21
[2026-07-21 08:19:39] production.INFO: saveSettingDisplayInfoItem error
[2026-07-21 08:19:39] production.ERROR: ErrorException: Undefined property: stdClass::$value in /var/www/html/sns-line/app/Http/Controllers/ChatController.php:4471
Stack trace:
#0 /var/www/html/sns-line/app/Http/Controllers/ChatController.php(4471): Illuminate\Foundation\Bootstrap\HandleExceptions->handleError(8, 'Undefined prope...', '/var/www/html/s...', 4471, Array)
```

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Expected result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Actual result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log production nằm ngay trong description (ticket **không có file attachment** nào)

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket không có section "Tái hiện bug", Steps / Expected / Actual để trống. Root cause đã được Dev (hệ thống Auto-fixbug) confirm qua đánh giá ảnh hưởng (xem `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.
- **Môi trường phát hiện: PRODUCTION** — log ghi channel `production.*`. Ca lỗi là dữ liệu thật của khách, không phải data test.
- **Tần suất**: ticket chỉ ghi nhận **1 lần xảy ra** (2026-07-21 08:19:39), không nói tần suất. Không có bằng chứng lỗi xảy ra 100%.
- Điều kiện tiên quyết suy từ log: mục thông tin bạn bè phải là **kiểu 「選択肢」** (`type_data = 1`) và payload gửi lên **thiếu hẳn khóa `value`**. Payload trong log có cả `id` (dòng hiển thị) và `id_setting` khác rỗng → mục đã nằm sẵn trong danh sách hiển thị của khung chat.
- ⚠️ **Không rõ client nào sinh ra payload thiếu `value`** — Redmine không ghi. Cần xác nhận với Dev trước khi chốt bộ TC: nếu UI hiện tại luôn kèm `value` thì bug chỉ tái hiện được ở tầng endpoint, không tái hiện được từ trình duyệt.
- Cả 4 lựa chọn của mục trong ca lỗi **đều gắn action** → khi verify fix phải kiểm luôn hành vi kích hoạt / không kích hoạt action.
- Ticket trạng thái **`Fix done - Đợi test`**, assignee **Ngô Thúy Ngần**, người tạo **Kieu Son Tung**. Category `Chat 1:1`, project `Lme`. Không có issue relation nào.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `1` |
| Friend | `$lineId = 21` (log không ghi tên friend / line_user_id) |
| Đối tượng cấu hình | Mục thông tin bạn bè 「🚫ロードマップ案内🚫」 — `id` dòng hiển thị = `1`, `id_setting` = `1`, `type` = `1`, `type_data` = `1` (選択肢), `order` = `5`, tạo `2026-06-29 09:33:30`, sửa lần cuối `2026-07-16 10:07:12` |
| Lựa chọn của mục | 4 lựa chọn, **tất cả đều gắn action**: `action_id 23` 「📧ロードマップの案内をする（進行中の方向け）」 · `action_id 34` 「📧ロードマップの案内をする（完成の方向け）」 · `action_id 45` 「📧ロードマップの案内をする（解約の人向け）」 · `action_id 56` 「📧新機能の案内をする（凍結バージョン）」 |
| Thời điểm lỗi | `2026/07/21 08:19:39` (production) |
| Đối chứng | `<không có — ticket chỉ ghi 1 ca lỗi, không có case chạy đúng để so sánh>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #133032 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi lưu một mục thông tin bạn bè kiểu 'chọn' từ khung chat 1:1, dữ liệu gửi lên chỉ chứa danh sách lựa chọn mà không có trường giá trị đã chọn. Đoạn code lưu lại đọc thẳng thuộc tính 'giá trị' của dữ liệu này mà không kiểm tra tồn tại, nên khi thiếu trường đó PHP báo lỗi thuộc tính không xác định và toàn bộ thao tác lưu bị hỏng.

■ 2. CÁCH FIX
Sửa ChatController::saveSettingDisplayInfoItem (dòng 4471, sns-line): bọc isset() khi đọc thuộc tính giá trị của dữ liệu gửi lên trước khi so sánh, thay vì đọc trực tiếp. Khi dữ liệu không kèm trường giá trị (mục kiểu 'chọn' bỏ trống) thì coi như rỗng và đi vào nhánh xóa giá trị, không còn báo lỗi thuộc tính không xác định. Cùng khuôn mẫu đã dùng ở nhánh type==0 (dòng 4333) trong chính hàm này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ChatController::saveSettingDisplayInfoItem (app/Http/Controllers/ChatController.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/ChatController.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ thêm kiểm tra tồn tại thuộc tính, không đổi cấu trúc/dữ liệu bảng
 • 4.3 Tính năng liên quan:
   - Friend Information (FA-015) — lưu giá trị mục thông tin bạn bè kiểu 'chọn' từ khung chat 1:1 an toàn khi payload thiếu trường giá trị

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/ChatController.php: No syntax errors detected
   Bằng chứng: Log ticket cho thấy $infos chỉ có 'valueOption' (danh sách lựa chọn), không có trường 'value' top-level → $value->value undefined tại dòng 4471; dòng 4470 dùng !empty (null-safe) còn 4471 đọc trực tiếp

■ TỰ REVIEW (AI)
Fix tối thiểu 1 dòng: thêm isset() guard đọc thuộc tính giá trị, theo đúng khuôn mẫu đã có sẵn ở dòng 4333 cùng hàm. Không đổi luồng lưu/xóa, chỉ chặn crash khi payload thiếu trường value. Rủi ro thấp.
 • Rủi ro / lưu ý khi test:
   - Không: khi thiếu value thì valueNew='' đi vào nhánh xóa giá trị — đúng hành vi 'bỏ chọn = xóa'; dòng calendar 4474 chỉ chạy khi valueNew truthy nên không bị ảnh hưởng

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_38944 (nhánh gốc release_step_20260623, commit 0aa5427f22, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 6 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=7fa09b3c-af23-455d-baa7-ce3fa90f09d9
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38944
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #133174 — Kieu Son Tung — 2026-08-27:**

```
branch release: release_step_20260827
```
