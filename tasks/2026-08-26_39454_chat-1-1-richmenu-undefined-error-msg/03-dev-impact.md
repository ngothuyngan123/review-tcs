# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39454 — journal **#132591** ngày **2026-08-24 07:36:24Z**, tác giả **AI LME Fix bug** (báo cáo tự động của hệ thống Auto-fixbug LME).
> Toàn bộ mục 1 → 7 bên dưới là **nguyên văn** từ journal, chỉ tách bảng cho dễ đọc.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | **AI LME Fix bug** (Auto-fixbug LME) — assignee Redmine hiện tại: `Ngọc Ánh` |
| Commit / Pull Request | `<không có link PR>` — commit `b5b3faa25f` (repo `sns-line`) · Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39454 · Phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=7cde801f-65fe-4b3d-a3be-64cadc328784 |
| Branch | `ai_fixbug_39454` (nhánh gốc `release_step_20260805`, 1 file, **đã push** origin) |
| Ngày submit đánh giá | `2026-08-24` |
| Auto-filled | `2026-08-26 by /new-task` |
| Thời gian AI xử lý | 6 phút 46 giây |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi đặt/đổi rich menu cho một người bạn từ màn chat 1:1, máy chủ gọi API liên kết rich menu của LINE. Nếu rich menu đó đã bị xóa khỏi tài khoản LINE chính thức (thường do công cụ khác dùng song song xóa mất) hoặc chưa từng đăng ký được lên LINE nên mã bên LINE đang rỗng, lời gọi này ném lỗi và khối bắt lỗi chỉ trả về cờ thất bại **KHÔNG kèm nội dung thông báo**. Màn chat lại hiển thị thẳng trường thông báo đó lên popup nên khách chỉ thấy 「undefined」, không biết vì sao không đặt được rich menu.

## 2. Cách fix

Sửa chức năng đặt rich menu cho từng người bạn ở màn chat 1:1 (`ChatController::chatEditRichMenu`): thêm hai hằng thông báo tiếng Nhật; khi rich menu chưa/không còn mã đăng ký bên LINE thì **dừng sớm (early-return)** và trả về đúng thông báo yêu cầu trong ticket (rich menu đã bị xóa khỏi tài khoản LINE chính thức, có thể do công cụ khác, chỉnh sửa - lưu lại để tạo lại); ở nhánh bắt lỗi, thêm **một lần kiểm tra rich menu còn tồn tại trên LINE hay không** (chỉ chạy khi đã lỗi, không thêm lần gọi nào ở luồng bình thường) để phân biệt đúng trường hợp bị xóa với các lỗi khác, lỗi khác trả thông báo chung có nội dung. Nhờ vậy popup ở màn chat không còn hiện 「undefined」.

**Quét ngang (nguyên văn):** chức năng đặt rich menu **hàng loạt** ở màn danh sách bạn bè **nuốt lỗi theo kiểu khác (vẫn trả thành công)** — khác phạm vi, chỉ ghi nhận.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::chatEditRichMenu` — `app/Http/Controllers/ChatController.php` | **Đã sửa** — thêm 2 hằng message JP + 2 nhánh early-return + kiểm tra rich menu trên LINE ở nhánh lỗi | Đây là function gây bug 「undefined」 |
| 2 | `ChatController::isRichMenuDeletedOnLine` — `app/Http/Controllers/ChatController.php` | **Hàm mới** | Phân biệt "rich menu bị xóa trên LINE" (404) với lỗi khác |
| 3 | `handleSaveEditRichMenu` / `hideRichMenu` — `public/js/chats/chat-v2.js` | Không sửa — chỉ check | Nơi hiện popup `alert(response.msg)` → chính là chỗ hiển thị 「undefined」 |
| 4 | `Basic\ChatController::index` → view `basic.chat.index` — `app/Http/Controllers/Basic/ChatController.php` | Không sửa — chỉ check | Xác nhận `chat-v2.js` là bản đang chạy |
| 5 | `FriendlistController::saveRichMenu` — `app/Http/Controllers/Basic/FriendlistController.php` | **Không sửa** | Đặt rich menu **hàng loạt** ở màn danh sách bạn bè — Dev ghi "khác phạm vi, chỉ ghi nhận" |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Journal Redmine ghi mục 4.1 là **"File thay đổi"** (chỉ 1 dòng), không phải list function theo format `F1/F2`. Bảng dưới do `/new-task` chuẩn hoá từ mục 4.1 + mục 3 — **Leader/tester verify lại**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::chatEditRichMenu` (endpoint đổi/dừng rich menu ở chat 1:1) | `app/Http/Controllers/ChatController.php` | **Direct** | Nguyên văn 4.1: *"File thay đổi: app/Http/Controllers/ChatController.php"* — **1 file duy nhất, 56 insertions / 1 deletion** |
| F2 | `ChatController::isRichMenuDeletedOnLine` | `app/Http/Controllers/ChatController.php` | **Direct** (hàm mới) | Chỉ được gọi ở nhánh lỗi → thêm 1 lần gọi LINE API khi đã lỗi |
| F3 | `handleSaveEditRichMenu` / `hideRichMenu` (FE popup `alert(response.msg)`) | `public/js/chats/chat-v2.js` | **Indirect** — không sửa code | Consumer của response; là nơi 「undefined」 hiện ra |
| F4 | `FriendlistController::saveRichMenu` (đặt rich menu hàng loạt) | `app/Http/Controllers/Basic/FriendlistController.php` | **Không sửa — Dev khai ngoài phạm vi** | Dev ghi: *"nuốt lỗi theo kiểu khác (vẫn trả thành công)"* → ⚠️ đây là **lỗi cùng lớp chưa được fix**, Leader chốt có test/raise ticket riêng không |

### 4.2. List data bị update khi fix bug

**Nguyên văn mục 4.2:** *"Không có — chỉ đổi nội dung phản hồi lỗi. Hai nhánh dừng sớm mới thêm chỉ chặn trường hợp mã rich menu bên LINE rỗng, tức là trường hợp trước đây chắc chắn lỗi và cũng không ghi được gì, nên không bỏ sót lần ghi hợp lệ nào vào `bot_line_user.rich_menu_id` hay `rich_menu_history`."*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_line_user.rich_menu_id` | **KHÔNG thay đổi** (Dev khẳng định) | ⚠️ Cần **đối chứng âm**: ở nhánh lỗi mới, giá trị cũ của friend phải giữ nguyên |
| D2 | `rich_menu_history` (bản ghi lịch sử, `trigger_type_start=15001`) | **KHÔNG thay đổi** (Dev khẳng định) | ⚠️ Cần verify: nhánh early-return không sinh bản ghi history rác |
| D3 | `rich_menus.rich_menu_id` (varchar(100) DEFAULT NULL — mã bên LINE) | Chỉ **đọc** | Dev dẫn schema `/workspace/share/db/db-refined` làm bằng chứng nhánh early-return là có thật |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Rich Menu (FA-004)** — báo đúng lỗi khi rich menu đã bị xóa khỏi tài khoản LINE chính thức, kèm hướng dẫn tạo lại | F1, F2 | *(Dev không ghi mức risk — Leader chốt)* |
| T2 | **1-on-1 Chat (FA-001)** — bảng thông tin bên phải màn chat, thao tác đổi/dừng rich menu của người bạn đang chọn | F1, F3 | *(Dev không ghi mức risk — Leader chốt)* |

> ⚠️ Dev **không ghi cột "nguy cơ regression" High/Medium/Low** cho 4.3 — `Input thiếu`, Leader tự đánh giá.

---

## 5. Recover data

✔ **Không cần recover data** (nguyên văn Dev).

## 6. Verify (nguyên văn Dev)

- **Mức:** `lint`
- **Lệnh:** `php -l app/Http/Controllers/ChatController.php` → *No syntax errors detected*; `git diff --stat origin/release_step_20260805...ai_fixbug_39454` → **1 file, 56 insertions, 1 deletion — đúng phạm vi**
- **Bằng chứng:** Schema `/workspace/share/db/db-refined`: `rich_menus.rich_menu_id varchar(100) DEFAULT NULL` = mã bên LINE, có thể rỗng khi chưa đăng ký được — xác nhận nhánh dừng sớm là có thật.
- ⚠️ **KHÔNG tái hiện được trên dev:** MySQL `host.docker.internal:3306` Connection refused (stack dev không chạy), và **không được phép gọi API LINE từ container**.

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

**Tự review (AI):** Fix bám đúng yêu cầu ticket: thay popup 「undefined」 bằng đúng câu thông báo tiếng Nhật khách yêu cầu cho trường hợp rich menu không còn tồn tại trên tài khoản LINE chính thức. Phạm vi gói gọn trong một hàm của màn chat 1:1, không đổi luồng thành công, không đổi dữ liệu. **Điểm cần người review lưu ý:** cách phân biệt "rich menu bị xóa" là gọi thêm một lần kiểm tra rich menu trên LINE ở nhánh lỗi (mã 404 = đã bị xóa); nếu muốn tối giản hơn có thể bỏ bước kiểm tra và trả thẳng thông báo này cho mọi lỗi, nhưng như vậy lỗi mạng/token cũng sẽ bị báo nhầm là bị xóa.

**Rủi ro / lưu ý khi test:**
- Nhánh lỗi tốn thêm một lần gọi API LINE (chỉ khi đã lỗi, không ảnh hưởng luồng bình thường).
- Nếu LINE trả 404 vì lý do khác ngoài rich menu không tồn tại thì thông báo có thể chưa sát; đã giới hạn bằng cách hỏi thẳng đường dẫn rich menu thay vì dựa vào mã lỗi của lần gọi liên kết (đường dẫn đó có cả mã người dùng nên 404 dễ nhập nhằng).
- Thông báo là chuỗi tiếng Nhật đặt thẳng trong controller, theo đúng cách các thông báo rich menu sẵn có trong mã nguồn (chưa có tệp ngôn ngữ riêng cho nhóm này).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn `/new-task` ghi nhận (Leader chốt)

1. **`FriendlistController::saveRichMenu` (đặt rich menu hàng loạt) có cùng lớp lỗi nhưng KHÔNG được fix** — Dev tự khai "nuốt lỗi theo kiểu khác (vẫn trả thành công)", tức là màn danh sách bạn bè **báo thành công khi thực chất thất bại** (nặng hơn 「undefined」). Leader chốt: raise ticket riêng hay đưa vào phạm vi test lần này.
2. **Cơ chế phân biệt 404** — chính AI ghi rủi ro "LINE trả 404 vì lý do khác" chưa được kiểm chứng ở môi trường thật.
3. **Mức verify chỉ `lint`**, không tái hiện được ở dev → toàn bộ bằng chứng hành vi phụ thuộc vào QA test tay ở env có LINE thật.
4. **4.3 thiếu mức risk** — `Input thiếu`.
