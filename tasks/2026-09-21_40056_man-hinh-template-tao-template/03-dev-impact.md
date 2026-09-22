# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) — assignee Redmine: Đoàn Thị Bích Hảo |
| Commit / Pull Request | `aa7eb13d44` (vòng 1, 20 file) → `4c60a17f92` (vòng 2, 21 file) — repo **sns-line** |
| Branch | `ai_fixbug_40056` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | 2026-09-07 (journal #134899) · **2026-09-15** (journal #136618 — bản mới nhất) |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Redmine #40056 **không có section "Đánh giá ảnh hưởng" trong description** — toàn bộ nội dung dưới đây lấy nguyên văn từ **2 journal AI Auto-fixbug**. Mục 2 (Cách fix) của 2 journal **KHÁC NHAU** (vòng 1 vs vòng 2), đã giữ cả hai.
> ⚠️ Mục 4.1 của Dev là **danh sách FILE thay đổi**, không phải danh sách function — bảng F* dưới đây dựng từ mục 3 (function đã check) + mục 2, gắn file tương ứng.

---

## 1. Nguyên nhân

*(nguyên văn journal #134899 và #136618 — giống nhau ở cả 2 vòng)*

Các endpoint ajax của màn danh sách template và màn tạo template/nhóm template trả HTTP code sai ý nghĩa: lỗi nghiệp vụ (đang sao lưu dữ liệu nên không cho thao tác, không tìm thấy template, tên rỗng/quá dài, lưu thất bại, quá hạn sửa nội dung trước giờ gửi) và cả lỗi hệ thống trong khối catch đều trả 200 (nghĩa là thành công), màn hình phải tự đoán qua cờ status/success trong thân phản hồi nên hệ thống giám sát không thấy lỗi; ngược lại nhánh chặn khi đang sao lưu lại trả 500 (nghĩa là server sập) cho một lỗi nghiệp vụ bình thường. Ngoài ra hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc: thiếu tham số vẫn chạy truy vấn/ghi theo giá trị rỗng rồi báo thành công (xoá theo id null, ghi đè danh sách message con thành chuỗi rỗng), hoặc rơi vào lỗi hệ thống thật. Hai khối catch còn bắt nhầm lớp ngoại lệ (`Doctrine\DBAL\Driver\Exception` là interface mà `\Exception` không implement) nên chưa bao giờ chạy, và một khối lấy mã ngoại lệ PHP (thường bằng 0) làm HTTP code.

## 2. Cách fix

### 2a. Vòng 1 — journal #134899 (2026-09-07), commit `aa7eb13d44`

Refix theo AI review vòng 1 — sửa 2 lỗi bắt buộc:

1. Endpoint lấy danh sách message con của nhóm mẫu tin nhắn (`GET .../park-template/list-template/{id}`) nhận id qua **ĐƯỜNG DẪN**, trong khi hàm kiểm tra dùng chung chỉ đọc dữ liệu body/query nên rule bắt buộc luôn trượt ⇒ mọi request đều bị trả `422`, làm màn tạo/sửa nhóm mẫu tin nhắn không nạp được danh sách message con (**3 nơi gọi đều hỏng**). Đã nạp tham số đường dẫn vào dữ liệu kiểm tra trước khi validate; đã rà lại toàn bộ endpoint được thêm kiểm tra trong lần fix trước (**6 ở màn danh sách + 18 ở màn tạo**) đối chiếu với định nghĩa route: chỉ endpoint này lấy tham số từ đường dẫn, các endpoint còn lại đều nhận qua body/query nên không dính. Đã chạy thử bằng script với vendor thật của repo: trước sửa dữ liệu kiểm tra rỗng (fail), sau sửa nhận đúng giá trị (pass).
2. **Nút bật/tắt gửi giãn cách**: nhánh lỗi mới thêm khôi phục trạng thái bằng phép đảo giá trị, nên khi người dùng mở modal bấm lưu mà **KHÔNG đổi gì** và request thất bại thì màn hình lật ngược sai trạng thái so với máy chủ (và đổi kiểu chuỗi thành luận lý). Đã chụp lại giá trị đang hiển thị trước khi ghi đè và khôi phục đúng giá trị đó cho cả biến hiển thị lẫn biến trong modal.

### 2b. Vòng 2 — journal #136618 (2026-09-15), commit `4c60a17f92` ← **bản mới nhất**

Bổ sung theo yêu cầu human (sau khi đã push): **MỌI truy vấn của 2 màn trong phạm vi ticket phải ràng buộc theo bot đang đăng nhập** — trước đây nhiều endpoint nhận id từ client rồi đọc/ghi/xoá chỉ theo id, nên tài khoản bất kỳ dò id là chạm được dữ liệu bot khác.

- **Màn danh sách mẫu tin nhắn**: endpoint điều phối (xoá thư mục, xoá 1 mẫu, xoá nhiều mẫu — câu xoá hàng loạt nhận thẳng danh sách id từ client), xoá mẫu tin nhắn, lấy danh sách message con của nhóm, xoá message trong nhóm, nhân bản mẫu tin nhắn.
- **Màn tạo mẫu tin nhắn / nhóm**: lưu mẫu tin nhắn (đổi tên / đổi thư mục), sắp xếp message con, xoá nhiều message con, lấy danh sách URL chuyển hướng, lấy dữ liệu thẻ giới thiệu và vị trí, **tạo/cập nhật nhóm** (chỗ này nguy hiểm nhất: dữ liệu ghi có cả `bot_id` nên dò id là kéo hẳn nhóm của bot khác sang bot mình), xem trước message con.
- 2 bảng `tmp_introduction` / `tmp_location` **KHÔNG có cột `bot_id`** nên ràng buộc gián tiếp qua template cha đã lọc bot (soạn message mới vẫn cho id rỗng như cũ).
- 2 endpoint **copy panel** truyền `action_id` từ client: bảng `t_actions` **KHÔNG có cột `bot_id`** (quyền sở hữu ở `t_actions_detail.bot_id`) và hàm nhân bản action đang dùng chung **~110 nơi**, nên chặn tại nơi gọi bằng helper riêng trong controller (**action chưa có detail nào thì cho qua** để không chặn nhầm) thay vì sửa hàm chung.
- Đã xác minh **12/12 chỗ tạo template đều ghi `bot_id`** nên lọc theo bot không làm mất dữ liệu hợp lệ.
- **CỐ Ý không đụng 4 câu truy vấn ở nhánh di chuyển / sắp xếp mẫu tin nhắn** vì ticket **#40979** (triển khai ngang lọc `bot_id`) đang sửa đúng 4 dòng đó — tránh sửa trùng và xung đột khi merge.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

*(nguyên văn mục 3 của journal — giống nhau ở cả 2 vòng)*

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MessageTemplateController::ajaxInitTemplate` | `app/Http/Controllers/Basic/MessageTemplateController.php` | Endpoint điều phối màn danh sách — HTTP code + validate + lọc bot |
| 2 | `MessageTemplateController::getListTemplateSort` | nt. | Danh sách / sắp xếp mẫu tin nhắn |
| 3 | `MessageTemplateController::ajaxDelTemplate` | nt. | Xoá mẫu tin nhắn — trước đây xoá theo id `null` |
| 4 | `MessageTemplateController::copyTemplate` | nt. | Nhân bản mẫu tin nhắn — lọc bot |
| 5 | `MessageTemplateController::getListTemplateChild` | nt. | Lấy danh sách message con của nhóm |
| 6 | `MessageTemplateController::deleteTemplateInGroup` | nt. | Xoá message trong nhóm |
| 7 | `TemplateV2Controller::saveTemplate` | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Lưu mẫu tin nhắn (đổi tên / đổi thư mục) |
| 8 | `TemplateV2Controller::ajaxCreateGroup` | nt. | Tạo / cập nhật nhóm — **điểm nguy hiểm nhất** (ghi kèm `bot_id`) |
| 9 | `TemplateV2Controller::saveSortTemplateChild` | nt. | Sắp xếp message con — trước đây ghi đè danh sách thành chuỗi rỗng |
| 10 | `TemplateV2Controller::deleteMultipleTemplateChild` | nt. | Xoá nhiều message con |
| 11 | `TemplateV2Controller::updateDelayMessage` | nt. | Bật/tắt gửi giãn cách — sửa khôi phục trạng thái ở nhánh lỗi |
| 12 | `TemplateV2Controller::updateUserQuickReply` | nt. | Quick reply |
| 13 | `TemplateV2Controller::getDataPreviewTemplateChild` | nt. | Xem trước message con |
| 14 | `TemplateV2Controller::copyFile` / `cloneActionButton` | nt. | 2 endpoint copy panel — chặn `action_id` bot khác bằng helper tại nơi gọi |
| 15 | `TemplateV2Controller::ajaxGetListUrlRedirect` | nt. | Danh sách URL chuyển hướng |
| 16 | `TemplateV2Controller::ajaxMetadataUrl` / `ajaxMetadataUrlAll` | nt. | Metadata URL |
| 17 | `TemplateV2Controller::initDataButton` / `initDataMedia` / `getDataText` / `getDataStamp` / `getDataLocation` / `getDataIntroduction` | nt. | Nạp dữ liệu từng loại message con |
| 18 | `saveTemplate()` | `resources/views/basic/template_v2/add-template.blade.php` | Phía màn hình — bắt lỗi theo HTTP code mới |
| 19 | `showTemplateAjaxError()` | `public/js/template_v2/ajax-error.js` | **File JS mới** — hàm hiển thị lỗi dùng chung cho 21 nơi gọi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev ghi mục 4.1 dưới dạng **danh sách file thay đổi** (21 file ở vòng 2). Bảng dưới nhóm theo cụm chức năng để map coverage; danh sách file nguyên văn giữ ở cuối mục.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | 6 endpoint ajax màn **danh sách mẫu tin nhắn** (`ajaxInitTemplate`, `getListTemplateSort`, `ajaxDelTemplate`, `copyTemplate`, `getListTemplateChild`, `deleteTemplateInGroup`) | `app/Http/Controllers/Basic/MessageTemplateController.php` | Direct | HTTP code + validate required + lọc `bot_id` |
| F2 | 18 endpoint ajax màn **tạo mẫu tin nhắn / nhóm** (`saveTemplate`, `ajaxCreateGroup`, `saveSortTemplateChild`, `deleteMultipleTemplateChild`, `updateDelayMessage`, `updateUserQuickReply`, `getDataPreviewTemplateChild`, `ajaxGetListUrlRedirect`, `ajaxMetadataUrl(All)`, `initDataButton/initDataMedia/getDataText/getDataStamp/getDataLocation/getDataIntroduction`) | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Direct | nt. |
| F3 | `GET .../park-template/list-template/{id}` — nạp tham số **đường dẫn** vào dữ liệu validate | `TemplateV2Controller` / route | Direct | Trước refix: **mọi request trả 422**, 3 nơi gọi hỏng |
| F4 | `TemplateV2Controller::copyFile` / `cloneActionButton` — helper chặn `action_id` không thuộc bot | `TemplateV2Controller.php` | Direct | `t_actions` không có `bot_id`; hàm nhân bản action dùng chung **~110 nơi** — chỉ chặn tại nơi gọi |
| F5 | `showTemplateAjaxError()` — hàm hiển thị lỗi ajax dùng chung | `public/js/template_v2/ajax-error.js` (**file mới**) | Direct | **21/21 nơi gọi** đã đổi sang hàm này |
| F6 | Nút **bật/tắt gửi giãn cách** — khôi phục trạng thái ở nhánh lỗi | `public/js/template_v2/add_group.js` + modal | Direct | Bug vòng 1: lật ngược trạng thái khi không đổi gì mà request fail |
| F7 | Nhánh hiển thị lỗi tại **nơi gọi dùng chung** — broadcast / step message / preview / send-test | `public/js/broadcast/modal-preview-draff-delivered.js`, `public/js/step_message/modal-send-test-all.js`, `public/js/template_v2/messages/modal-preview-template-child.js`, `modal-preview-send-test.js` | Indirect | Chỉ đổi nhánh lỗi, không đổi hành vi khi thành công |
| F8 | JS soạn từng loại message con (text / media / stamp / location / introduction / button) | `public/js/template_v2/messages/*.js` | Indirect | Bắt lỗi theo HTTP code mới |
| F9 | JS màn danh sách + nhóm mẫu tin nhắn đời cũ | `public/js/msg_template/index.js`, `public/js/msg_template/add_group.js` | Direct | nt. |
| F10 | 4 blade màn danh sách / tạo message | `resources/views/basic/message_template/index.blade.php`, `resources/views/basic/template_v2/add.blade.php`, `components/create-message.blade.php`, `add-template.blade.php` | Direct | Nạp `ajax-error.js`, đổi nhánh bắt lỗi |

<details>
<summary>Danh sách 21 file thay đổi — nguyên văn mục 4.1 journal #136618</summary>

```
- app/Http/Controllers/Basic/MessageTemplateController.php
- app/Http/Controllers/Basic/TemplateV2Controller.php
- public/js/template_v2/ajax-error.js
- public/js/msg_template/index.js
- public/js/msg_template/add_group.js
- public/js/template_v2/add_group.js
- public/js/template_v2/messages/button.js
- public/js/template_v2/messages/media.js
- public/js/template_v2/messages/stamp.js
- public/js/template_v2/messages/location.js
- public/js/template_v2/messages/introduction.js
- public/js/template_v2/messages/text.js
- public/js/template_v2/messages/modal-preview-template-child.js
- public/js/template_v2/messages/modal-preview-send-test.js
- public/js/step_message/modal-send-test-all.js
- public/js/broadcast/modal-preview-draff-delivered.js
- resources/views/basic/message_template/index.blade.php
- resources/views/basic/template_v2/add.blade.php
- resources/views/basic/template_v2/components/create-message.blade.php
- resources/views/basic/template_v2/add-template.blade.php
```

</details>

### 4.2. List data bị update khi fix bug

*(nguyên văn mục 4.2 journal)*

> **Không có** — chỉ đổi mã trạng thái HTTP và thêm kiểm tra đầu vào, không đổi cấu trúc / ghi dữ liệu; ngược lại còn **chặn 2 đường ghi hỏng dữ liệu** (xoá theo id `null`, ghi đè danh sách message con của nhóm thành chuỗi rỗng).

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — (không đổi cấu trúc / không thêm ghi mới) | — | Dev khẳng định không có data impact |
| D2 | Đường ghi hỏng **bị chặn**: xoá mẫu tin nhắn theo id `null` | DELETE (nay bị chặn) | Verify: dữ liệu KHÔNG còn bị xoá nhầm khi thiếu tham số |
| D3 | Đường ghi hỏng **bị chặn**: ghi đè danh sách message con của nhóm thành chuỗi rỗng | UPDATE (nay bị chặn) | Verify: danh sách message con không bị làm rỗng khi thiếu tham số |
| D4 | Phạm vi `WHERE` của mọi truy vấn 2 màn nay có thêm ràng buộc **bot đang đăng nhập** | SELECT / UPDATE / DELETE | Rủi ro 2 chiều: **chặn thiếu** (còn đọc/ghi bot khác) hoặc **chặn thừa** (mất dữ liệu hợp lệ của chính bot mình) |
| D5 | `tmp_introduction` / `tmp_location` — **không có cột `bot_id`** | SELECT | Ràng buộc gián tiếp qua template cha; soạn message mới vẫn cho id rỗng |
| D6 | `t_actions` — **không có cột `bot_id`** (sở hữu ở `t_actions_detail.bot_id`) | SELECT | Chặn tại nơi gọi; **action chưa có detail nào thì cho qua** → là lỗ hổng có chủ ý, cần TC |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

*(nguyên văn mục 4.3 journal)*

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Message Template (FA-010 / SC-001)** — màn danh sách mẫu tin nhắn: thêm / đổi tên / xoá thư mục, xoá / sao chép / di chuyển / sắp xếp mẫu tin nhắn **nay báo đúng lý do khi thất bại** | F1, F5, F9, F10, D2, D4 | **High** |
| T2 | **Template Message / Message Editor (SC-001 / SC-005)** — màn tạo mẫu tin nhắn (soạn text / ảnh / video / stamp / vị trí / nút): lưu mẫu tin nhắn, tạo nhóm, sắp xếp và xoá message con, bật/tắt gửi giãn cách | F2, F3, F4, F6, F8, F10, D3, D4, D5, D6 | **High** |
| T3 | **Broadcast (FA-008)** — dùng chung màn soạn tin và popup gửi thử: **chỉ cập nhật nhánh hiển thị lỗi tại nơi gọi**, không đổi hành vi khi thành công | F7 | Medium |
| T4 | **Step Delivery / Scenario (FA-009)** — dùng chung màn soạn tin và popup xem trước / gửi thử: chỉ cập nhật nhánh hiển thị lỗi tại nơi gọi | F7 | Medium |
| T5 | **Reminder Delivery (FA-022)** — dùng chung màn soạn tin qua tham số loại thao tác event: chỉ cập nhật nhánh hiển thị lỗi tại nơi gọi | F7 | Medium |
| T6 | **Nhóm mẫu tin nhắn đời cũ (park-template)** — `GET .../park-template/list-template/{id}` | F3 | **High** — trước refix mọi request trả 422 |

### 4.4. BUG — root cause / cách fix (tag `BUG`)

| Tag | Nội dung |
|---|---|
| `BUG-1` | Lỗi nghiệp vụ + lỗi hệ thống trong `catch` đều trả `200` → giám sát không thấy lỗi, màn hình phải tự đoán qua cờ `status`/`success` trong body |
| `BUG-2` | Nhánh chặn khi **đang sao lưu dữ liệu** trả `500` cho một lỗi nghiệp vụ bình thường |
| `BUG-3` | Thiếu validate required → thiếu tham số vẫn chạy query/ghi theo giá trị rỗng rồi **báo thành công** |
| `BUG-4` | 2 khối `catch` bắt nhầm lớp ngoại lệ (`Doctrine\DBAL\Driver\Exception` là interface, `\Exception` không implement) → **chưa bao giờ chạy** |
| `BUG-5` | 1 khối lấy **mã ngoại lệ PHP** (thường `0`) làm HTTP code |
| `BUG-6` | Truy vấn không ràng buộc bot đang đăng nhập → **dò id chạm được dữ liệu bot khác** (cross-tenant) |
| `BUG-7` | (do fix vòng 1 gây ra, đã refix) Endpoint nhận id qua **đường dẫn** nhưng validate chỉ đọc body/query → mọi request trả `422` |
| `BUG-8` | (do fix vòng 1 gây ra, đã refix) Nút bật/tắt gửi giãn cách khôi phục trạng thái bằng **phép đảo** → lật ngược sai khi không đổi gì mà request fail |

---

## 5. Recover data

✔ Không cần recover data *(nguyên văn journal)*

## 6. Verify của Dev

| Trường | Giá trị |
|---|---|
| Mức | **`lint`** ⚠️ |
| Lệnh | `php -l` trên 2 file controller: No syntax errors detected; `node --check` trên 14 file JS đã sửa + file mới `ajax-error.js`: OK; biên dịch 4 file blade bằng Illuminate BladeCompiler rồi `php -l`: No syntax errors detected; chạy thử `Illuminate\Validation\Factory` với gói ngôn ngữ `ja` của dự án cho 10 tổ hợp rule: message hiển thị trọn tiếng Nhật (vd `フォルダを選択してください。` / `フォルダ名は20文字以内で入力してください。` / `メッセージ内容の形式が正しくありません。`); rà lại từng nơi gọi bằng script đối chiếu ngược URL của khối `$.ajax` chứa nhánh lỗi vừa sửa: **21/21 khớp đúng endpoint dự kiến** |
| Bằng chứng | `Doctrine\DBAL\Driver\Exception` trong vendor là interface extends `Throwable` → `\Exception` không implement, xác nhận 2 khối `catch` cũ không bao giờ chạy; middleware `ConvertEmptyStringsToNull` có trong `app/Http/Kernel.php` → chuỗi rỗng thành `null` nên rule `nullable` hoạt động đúng với các id màn hình cố ý gửi rỗng; đối chiếu 7 màn khác cùng gọi `/ajax/template-v2/get-data`: không màn nào gửi `template_id` nên rule `nullable` không ảnh hưởng; nút trang trước/trang sau của danh sách có `v-if` chặn nên `page` luôn ≥ 1, rule `min:1` an toàn; **chưa chạy được trên dev stack (không có phiên đăng nhập)** — verify dừng ở mức lint + compile + thử bộ validate |

⚠️ **Không có verify runtime nào** — mọi hành vi thật (HTTP code trả về, message tiếng Nhật hiển thị trên màn, lọc bot có đúng không) đều **chưa được chạy** trước khi chuyển test.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
