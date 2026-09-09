# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #33117 bằng `/new-task`. Nguồn: **journal #131644** (AI LME Fix bug, 2026-08-21T02:06:09Z) — báo cáo `★ AI AUTO-FIXBUG`.
>
> ⚠️ **Fix do AI Auto-fixbug thực hiện**, không phải human dev.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | `sns-line` commit `e982edc05e` (3 file). Không có link Github/Gitlab trong ticket. |
| Branch | `ai_fixbug_33117` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-21` (journal #131644) |
| Auto-filled | `2026-08-24 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=be83e382-86c8-4394-bd26-d6471c625286 |
| Dashboard fixbug | https://dashboard.melonglobal.net/fixbug-lme/?id=33117 |
| Thời gian AI xử lý | 10 phút 25 giây |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN, journal #131644 -->

Màn chat 1:1 khởi tạo **2 bộ chọn emoji** dùng chung một thư viện: một bộ cho **modal multi action**, một bộ cho **ô nhập tin chat**. Cả hai bộ đều gắn thêm handler đóng bảng emoji lên thẻ `body`, và bộ của ô chat **đăng ký sau nên chạy sau**.

Khi bấm icon emoji của action gửi text, bộ của modal mở bảng emoji xong thì **ngay trong cùng cú click đó** bộ của ô chat **xoá luôn bảng vừa mở**, nên người dùng thấy bấm mà không có gì hiện ra.

Kèm theo đó, nếu bảng có hiện thì **cả 2 bộ cùng xử lý việc chèn emoji**, dẫn tới emoji bị **chèn nhầm sang cả ô nhập tin chat**.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX, journal #131644 -->

Sửa **thư viện chọn emoji dùng chung** (`public/js/fgEmojiPicker.js`) để chạy đúng khi một trang khởi tạo nhiều bộ chọn emoji:

1. Khi mở bảng emoji thì **đánh dấu bảng đó thuộc bộ nào** và **do cú click nào mở ra**.
2. Handler đóng bảng **bỏ qua bảng vừa được mở bởi chính cú click đang xử lý** (không xoá nhầm bảng của bộ khác).
3. Handler chèn emoji **chỉ chạy ở đúng bộ đã mở bảng** nên không chèn nhầm sang ô nhập của bộ khác.

Đồng thời cho thẻ nạp file thư viện trong layout dùng **số version chung** thay vì version cố định cũ (**và nâng version**) để trình duyệt tải lại bản đã sửa.

**Quét ngang**: chỉ có **2 nơi** khởi tạo bộ chọn emoji (modal action và ô chat) nên **chỉ màn chat 1:1** dính lỗi này, các màn khác chỉ có 1 bộ nên hành vi không đổi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3, journal #131644 -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FgEmojiPicker.functions.removeEmojiPicker` | `public/js/fgEmojiPicker.js` | Handler đóng bảng — **chỗ gây lỗi**: xoá BẤT KỲ bảng emoji nào đang mở nếu click không nằm trong bảng, không phân biệt bảng đó của bộ nào |
| 2 | `FgEmojiPicker.functions.emitEmoji` | `public/js/fgEmojiPicker.js` | Handler chèn emoji — giới hạn chỉ chạy ở đúng bộ đã mở bảng |
| 3 | `FgEmojiPicker.functions.openEmojiSelector` | `public/js/fgEmojiPicker.js` | Đánh dấu chủ sở hữu bảng + cú click mở |
| 4 | `FgEmojiPicker.bindEvents` + `this.lib().on` | `public/js/fgEmojiPicker.js` | Đăng ký handler trên `body` |
| 5 | `emojiPicker = new FgEmojiPicker` trigger `.fa-smile-o` | `public/js/select_action.js` | Bộ chọn emoji của **modal action** — đăng ký **trước** |
| 6 | `emojiPickerChat = new FgEmojiPicker` trigger `#emojiBtn` | `public/js/chats/chat-v2.js` | Bộ chọn emoji của **ô chat** — đăng ký **sau**, chạy sau |
| 7 | `insertAtCursorAction` | `public/js/select_action.js` | Chèn emoji vào ô nội dung action |
| 8 | `openSettingAction` | `public/js/chats/chat-v2.js` | Mở modal action từ màn chat |
| 9 | modal multi action — action gửi text | `resources/views/layout/modal_setting/modal_select_action.blade.php` | Markup modal |
| 10 | layout nạp thư viện emoji | `resources/views/layout/basic/footer.blade.php` | ĐÃ SỬA — đổi sang version chung |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục ■ 4.1 File thay đổi, journal #131644 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Thư viện chọn emoji dùng chung `FgEmojiPicker` (thêm 2 điều kiện bảo vệ ở `removeEmojiPicker` / `emitEmoji` / `openEmojiSelector`) | `public/js/fgEmojiPicker.js` | **Direct** | ⚠️ **Thư viện DÙNG CHUNG cho mọi màn có emoji picker** |
| F2 | Layout nạp thư viện emoji — đổi từ version cố định cũ sang **version chung** | `resources/views/layout/basic/footer.blade.php` | Direct | Để trình duyệt tải lại bản đã sửa |
| F3 | Config version asset (**nâng version chung**) | `config/sns-line.php` | Direct | ⚠️ Làm trình duyệt **tải lại toàn bộ js/css một lần** sau khi release |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục ■ 4.2 Data ảnh hưởng, journal #131644 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Không có.** Fix thuần front-end JS + config version asset. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục ■ 4.3 Tính năng liên quan, journal #131644 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — modal cấu hình hành động mở từ màn chat: bảng emoji của action gửi text mở được, và emoji **không còn bị chèn nhầm** vào ô nhập tin chat | F1 | **High** (màn duy nhất tái hiện được bug) |
| T2 | **Action Settings (SC-004)** — modal multi action **dùng chung ở nhiều màn** (tự động trả lời, kịch bản, tag, form, đặt lịch, bán hàng...): nút emoji của action gửi text | F1 | **High** |
| T3 | **Auto Reply (FA-003)** — dùng chung modal multi action; **chỉ có 1 bộ chọn emoji nên hành vi không đổi**, đã rà để chắc không hồi quy | F1 | Medium (verify không đổi) |

---

## 5. Recover data

✔ **Không cần recover data.**

## 6. Verify (Dev đã làm)

**Mức: lint** ⚠️

- `node --check public/js/fgEmojiPicker.js`: OK
- `php -l config/sns-line.php`: No syntax errors detected
- `php -l resources/views/layout/basic/footer.blade.php`: No syntax errors detected
- `git diff --stat origin/release_step_20260805...ai_fixbug_33117`: đúng 3 file đã sửa

**Bằng chứng:** Đọc code chứng minh thứ tự chạy handler — `select_action.js` được nạp ở **dòng 68** của `resources/views/basic/chat/index.blade.php` (qua include `modal_select_action`), `chat-v2.js` nạp ở **dòng 185** cùng file ⇒ bộ chọn emoji của modal **đăng ký handler body trước**, bộ của ô chat **đăng ký sau và chạy sau** trong cùng cú click. `removeEmojiPicker` xoá BẤT KỲ bảng emoji nào đang mở nếu click không nằm trong bảng, **không phân biệt bảng đó của bộ nào** — đây là chỗ gây lỗi.

> ⚠️ **Trình duyệt/web dev KHÔNG truy cập được từ container** (`curl http://host.docker.internal:8000` trả về `000`) nên **không chạy tái hiện runtime được**; đã kiểm chứng bằng **đọc code + lint**.

## 7. Tự review (AI) — rủi ro / lưu ý khi test

> Nguyên văn mục ■ TỰ REVIEW (AI). **Đây là input quan trọng nhất để chấm coverage TCs.**

Fix nằm ở **thư viện chọn emoji dùng chung** nhưng chỉ **thêm 2 điều kiện bảo vệ**, và cả 2 điều kiện đều **vô hiệu khi trang chỉ có 1 bộ chọn emoji** (bảng luôn thuộc chính bộ đó, còn handler đóng của chính nó luôn chạy TRƯỚC handler mở nên không bao giờ gặp bảng vừa mở trong cùng cú click). Vì vậy các màn khác **giữ nguyên hành vi**, chỉ màn chat 1:1 được sửa. Có nâng số version tài nguyên vì đụng file trong `public/js`, đồng thời trỏ thẻ nạp thư viện emoji sang version chung do trước đó nó dùng version cố định cũ nên không tự cập nhật cho trình duyệt.

**Rủi ro / lưu ý khi test:**

- ⚠️ **Nâng version chung** làm trình duyệt **tải lại toàn bộ js/css một lần** sau khi release — chấp nhận được, đúng quy ước dự án.
- ⚠️ **Không chạy được kiểm thử runtime trong container** (web dev không truy cập được) nên **cần tester bấm lại theo các bước tái hiện**, đặc biệt kiểm tra **không hồi quy ở ô nhập tin chat**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader cần quyết trước khi test

1. **Fix ở thư viện dùng chung** (`fgEmojiPicker.js`) ⇒ mọi màn có emoji picker đều nằm trong bán kính regression, kể cả màn Dev khẳng định "hành vi không đổi". Rủi ro **đối xứng** với bug gốc: trước fix bảng **đóng quá sớm**, sau fix có thể **đóng quá muộn / không đóng được** ở màn chỉ có 1 picker.
2. **Dev chỉ verify mức lint** — không có bằng chứng runtime nào. Toàn bộ hành vi UI phải do tester bấm tay xác nhận, **không được kết luận pass bằng đọc source**.
3. **Nâng version asset chung** (`config/sns-line.php`) ⇒ ảnh hưởng deploy toàn hệ thống, không riêng emoji picker (`DEPLOY-*`, `DATA-CACHE-*`).
4. Mục 4.2 ghi "**Không có**" data ảnh hưởng — nhưng emoji nhập vào action **được lưu xuống DB** khi save bản ghi (tự động trả lời, kịch bản...). Cần xác nhận encoding emoji khi lưu/đọc lại không nằm ngoài phạm vi verify.
