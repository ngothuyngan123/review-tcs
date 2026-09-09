# 03 — Đánh giá ảnh hưởng từ Dev

> **Nguồn**: Redmine #38962 — journal `133115` (2026-08-26T10:51:31Z, user `AI LME Fix bug`), báo cáo **AI AUTO-FIXBUG**.
> Nội dung 4 mục bên dưới **paste nguyên văn** từ Redmine; bảng phía sau mỗi mục là phần Claude parse lại theo template (đánh tag F/D/T) để map coverage.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` (báo cáo tự động, không có dev người). Redmine assigned_to = `Ngô Thúy Ngần` (QA nhận test) |
| Commit / Pull Request | Repo `sns-line`, commit `4c2606f832` — **không có link PR** trong Redmine |
| Branch | `ai_fixbug_38962` (nhánh gốc `release_step_20260805`, **1 file**, 18 thêm / 3 bớt, đã push origin) |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-03 by /new-task` |

**Link phiên xử lý AI** (Dev cung cấp): https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=a309e720-f872-4d64-8d34-f30866927a65 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38962

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" từ Redmine journal 133115. -->

Endpoint trả thông số cho modal cảnh báo vượt giới hạn gửi đọc bản ghi tin gửi hàng loạt CHỈ theo mã do client gửi lên, không ràng buộc theo bot đang đăng nhập. Nhóm route ajax chỉ chạy kiểm tra đã đăng nhập, không có cổng phân quyền theo bot, nên tài khoản bất kỳ dò mã tin là lấy được số người nhận và danh sách mẫu tin của bot khác.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" từ Redmine journal 133115. -->

Chặn đầu hàm lấy thông số cảnh báo vượt giới hạn gửi: mã tin gửi phải là số dương; đọc bản ghi bằng MỘT truy vấn có ràng buộc bot đang đăng nhập (gộp 2 truy vấn cũ vốn chỉ lọc theo mã), trả 403 khi tin không thuộc bot hiện tại; truy vấn mẫu tin con cũng thêm ràng buộc bot. Luồng hợp lệ không đổi vì modal xác nhận chỉ mở với tin gửi đã lưu của chính bot đó, và phía giao diện đã có sẵn nhánh dự phòng khi API lỗi. Fix độc lập branch riêng (ticket cha #38803 là tracker Feature nên không gộp); base là release_step_20260805 — nội dung file giống hệt release_staging_20260704 mà ghi chú ticket nhắc tới. Quét ngang: còn nhiều chỗ cùng kiểu đọc/ghi tin gửi theo mã thô ở BroadcastV2Controller/BroadcastController/ChatController, chưa sửa vì ngoài phạm vi ticket.

**⚠️ Điểm cần hỏi lại Dev**:
1. "còn nhiều chỗ cùng kiểu đọc/ghi tin gửi theo mã thô ở BroadcastV2Controller / BroadcastController / ChatController" — Dev **không liệt kê tên function cụ thể**, cũng không nói có bao nhiêu chỗ. Đây là **cùng một lớp lỗ hổng IDOR** nhưng nằm ngoài phạm vi ticket ⇒ Leader cần yêu cầu Dev liệt kê để mở ticket riêng (xem `BUG-GAP-01` cuối file).
2. Fix gộp **2 nhánh từ chối** (mã không hợp lệ / mã ngoài bot) thành cùng **403**, trong khi spec sprint 36436 ghi **400** cho invalid input ⇒ **conflict contract chưa chốt** (xem `BUG-GAP-02`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" — Dev list dạng plain, Claude convert sang bảng template. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TemplateV2Controller::getBroadcastLimitAlert` — `app/Http/Controllers/Basic/TemplateV2Controller.php:1056` | **CÓ sửa** (file duy nhất bị đổi) | Thêm validate mã tin gửi phải là số dương; gộp 2 truy vấn đọc thành 1 truy vấn có ràng buộc `bot_id`; trả 403 khi ngoài phạm vi bot; truy vấn mẫu tin con cũng thêm ràng buộc bot |
| 2 | route `templateV2.getBroadcastLimitAlert` — `routes/web.php:2667` | Không sửa (đã check) | Nhóm ajax, middleware chỉ có `check_login` + `check_remember_token` ⇒ **không có cổng phân quyền theo bot** — đây là lý do lỗ hổng tồn tại |
| 3 | `openAlertMessage` — `public/js/broadcast/modal-preview-draff-delivered.js:586` | Không sửa (đã check) | JS gọi endpoint để mở modal cảnh báo |
| 4 | `getDataPreview` — `public/js/broadcast/modal-preview-draff-delivered.js:386` | Không sửa (đã check) | JS dựng dữ liệu hộp xem trước |
| 5 | `confirmSaveBroadcast` — `public/js/broadcast/add-broadcast.js:645` | Không sửa (đã check) | Nơi mở modal xem trước; chỉ mở khi đã có `broadcastEdit.broadcast_id` đã lưu |
| 6 | preview từ màn danh sách — `public/js/broadcast/index.js:1554` | Không sửa (đã check) | Đường vào thứ 2 của modal, từ dòng trong danh sách của bot hiện tại |
| 7 | `isTemplateOfBot` / `getBotIdInScope` — `app/Helpers/functions.php:397-425` | Không sửa (đã check) | Mẫu ràng buộc phạm vi bot **đã duyệt** — fix bám theo mẫu này |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục "■ 4.1 File thay đổi": chỉ 1 dòng "app/Http/Controllers/Basic/TemplateV2Controller.php". -->
<!-- ⚠️ Dev chỉ liệt kê FILE, không liệt kê function ⇒ bảng dưới do Claude suy ra từ mục 2 + mục 3; tester verify lại. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TemplateV2Controller::getBroadcastLimitAlert` | `app/Http/Controllers/Basic/TemplateV2Controller.php` | **Direct** | Hàm DUY NHẤT bị sửa code. 3 thay đổi: (a) validate `broadcast_id` là số dương; (b) 1 truy vấn có ràng buộc `bot_id` thay 2 truy vấn cũ; (c) trả **403** khi ngoài phạm vi bot |
| F2 | Truy vấn đếm **mẫu tin con** trong `getBroadcastLimitAlert` (nhánh mẫu tin nhóm) | cùng file | **Direct** | Thêm ràng buộc bot ⇒ **số đếm có thể GIẢM** nếu tin gửi trỏ tới mẫu tin của bot khác (dữ liệu bẩn) |
| F3 | route ajax `templateV2.getBroadcastLimitAlert` | `routes/web.php:2667` | Indirect | Không sửa; vẫn chỉ có `check_login` + `check_remember_token` ⇒ cổng 403 trong F1 là **lớp bảo vệ DUY NHẤT** |
| F4 | `openAlertMessage` — nhánh `.fail()` (`modal-preview-draff-delivered.js:600-611`) | `public/js/broadcast/modal-preview-draff-delivered.js` | Indirect | Không sửa; khi API trả 403 thì JS gọi tiếp `registerBroadcast()` ⇒ **403 không làm kẹt màn**. Đây là lý do Dev khẳng định "luồng hợp lệ không đổi" |
| F5 | `confirmSaveBroadcast` (`add-broadcast.js:645`) · preview từ danh sách (`index.js:1554`) | `public/js/broadcast/*` | Indirect | 2 đường vào modal; cả 2 đều chỉ truyền mã tin gửi **của chính bot hiện tại** ⇒ người dùng hợp lệ không rơi vào nhánh 403 |
| BUG | Root cause: đọc bản ghi `BroadCast` theo `id` do client gửi, **không** ràng buộc `bot_id`; nhóm route ajax không có cổng quyền theo bot | `TemplateV2Controller.php:1051` (theo description) / `:1056` (theo journal) | — | ⚠️ Description ghi dòng **1051**, journal ghi dòng **1056** — lệch 5 dòng, tester đối chiếu lại khi đọc code |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "■ 4.2 Data ảnh hưởng": "Không có — fix chỉ thêm điều kiện lọc khi đọc, không ghi/sửa dữ liệu". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `broadcast.bot_id` | **READ** (thêm điều kiện lọc) | Dev khẳng định **không CREATE/UPDATE/DELETE/MIGRATE**. Bằng chứng schema Dev nêu: `broadcast.sql:17 — bot_id int(11) NOT NULL` |
| D2 | `template.bot_id` | **READ** (thêm điều kiện lọc) | Ràng buộc bot cho truy vấn mẫu tin con. Bằng chứng: `template.sql:25 — bot_id int(11) NOT NULL` |
| D3 | `broadcast.filter_number` · `broadcast.template_ids` | **READ** | Chính 2 field bị lộ trước khi fix |

> ✅ **Không có data bị ghi/sửa** ⇒ mục 5 của Dev: "Không cần recover data".
> ⚠️ Nhưng **giá trị đọc ra có thể đổi** (D2): nếu tồn tại tin gửi trỏ tới mẫu tin của bot khác thì số 今回の配信合計 **giảm** so với trước fix. Đây là **thay đổi hành vi quan sát được**, cần TC audit dữ liệu.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "■ 4.3 Tính năng liên quan" từ Redmine journal 133115. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Broadcast (FA-008)** — modal cảnh báo vượt giới hạn gửi chỉ đọc được tin gửi thuộc bot đang đăng nhập, chặn dò mã tin của bot khác *(nguyên văn Dev)* | F1, F3, D1 | **High** — cổng 403 mới nằm ngay trước khối tính số liệu; viết sai ràng buộc bot là **chính chủ bot cũng bị chặn** |
| T2 | **Message Template (FA-010)** — đếm số mẫu tin trong tin gửi được giới hạn theo bot hiện tại *(nguyên văn Dev)* | F2, D2 | **Medium** — số đếm giảm khi dữ liệu lệch bot; cảnh báo hiện **nhẹ hơn thực tế**, không chặn thao tác |
| T3 | Luồng **đăng ký tin gửi hàng loạt** (「この内容で配信登録」) trên màn tạo/sửa + màn danh sách | F4, F5 | **Medium** — Claude suy thêm từ mục 3 + 6 của Dev (Dev không tách riêng ở 4.3). Nhánh `.fail()` của JS phải giữ nguyên hành vi đăng ký |

---

## 5. Recover data

<!-- Nguyên văn mục "■ 5. RECOVER DATA". -->

✔ **Không cần recover data**

---

## 6. Verify của Dev

<!-- Nguyên văn mục "■ 6. VERIFY". -->

**Mức**: `lint`

**Lệnh đã chạy**:
- `php -l app/Http/Controllers/Basic/TemplateV2Controller.php` → No syntax errors detected
- `git diff --stat origin/release_step_20260805...ai_fixbug_38962` → đúng 1 file, 18 thêm / 3 bớt
- **Không chạy PHPUnit** — lý do Dev nêu: fix nằm ở Controller, không thuộc `app/Services` | `app/Helpers`
- **Không compile Java** — ticket chỉ đụng repo web `sns-line`

**Bằng chứng Dev đưa ra**:
- Schema `/workspace/share/db/db-refined/schema-annotated/tables/broadcast.sql:17` — `bot_id int(11) NOT NULL`; `template.sql:25` — `bot_id int(11) NOT NULL` ⇒ ràng buộc `bot_id` không loại nhầm bản ghi hợp lệ
- Đối chiếu phía giao diện: modal xem trước chỉ mở khi đã có mã tin đã lưu (`add-broadcast.js:645` kiểm `broadcastEdit.broadcast_id`) hoặc từ dòng trong danh sách của bot hiện tại (`index.js:1554`) ⇒ người dùng hợp lệ không rơi vào nhánh 403
- Nhánh lỗi phía giao diện (`modal-preview-draff-delivered.js:600` fail) đã gọi tiếp `registerBroadcast()` nên 403 không làm kẹt màn, không hiện toast lỗi
- **MySQL dev không kết nối được (Connection refused)** nên không dump được dữ liệu thực; **kết luận dựa trên schema + đọc mã nguồn**

> ⚠️ **Mức verify chỉ là `lint`** — không có unit test, không có test chạy thật, không dump được DB. Toàn bộ kết luận "luồng hợp lệ không đổi" là **suy luận từ đọc code**, chưa có bằng chứng chạy. Đây là lý do bộ TC phải có TC **chạy thật trên browser** cho nhánh hợp lệ (không chỉ gọi endpoint rồi suy).

---

## 7. Tự review của AI + rủi ro khi test

<!-- Nguyên văn mục "■ TỰ REVIEW (AI)". -->

Fix bám đúng đề xuất của ticket: ràng buộc bot cho truy vấn tin gửi và mẫu tin con, trả 403 khi ngoài phạm vi. Gộp 2 truy vấn trùng nhau thành 1 là hệ quả tự nhiên của việc phải lấy bản ghi để kiểm quyền sở hữu, không phải dọn dẹp thừa. Công thức tính cảnh báo giữ nguyên 100%. Đây là một lớp lỗi hệ thống (nhóm route ajax không có cổng quyền theo bot) — đã ghi các chỗ cùng kiểu vào phần quét ngang, không sửa ngoài phạm vi ticket.

**Rủi ro / lưu ý khi test (nguyên văn Dev)**:
- Nếu tồn tại dữ liệu cũ có tin gửi mang `bot_id` lệch với bot của người tạo thì màn sẽ trả **403 thay vì hiện cảnh báo**; schema để `bot_id NOT NULL` và luồng tạo/sao chép đều gán `bot_id` nên rủi ro thấp
- Ràng buộc bot cho truy vấn mẫu tin con sẽ làm **số tin đếm được giảm** nếu tin gửi trỏ tới mẫu tin của bot khác (dữ liệu bẩn) — khi đó cảnh báo hiện **nhẹ hơn thực tế**, không chặn thao tác

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### ⚠️ Điểm nghi vấn Claude phát hiện — Leader hỏi Dev trước khi giao TC

| # | Vấn đề | Vì sao quan trọng |
|---|---|---|
| `BUG-GAP-01` | Dev nêu "còn nhiều chỗ cùng kiểu đọc/ghi tin gửi theo mã thô ở `BroadcastV2Controller` / `BroadcastController` / `ChatController`" nhưng **không liệt kê tên function nào**. | Cùng **một lớp lỗ hổng IDOR** vẫn còn mở sau khi ticket này đóng. Route ajax không có cổng quyền theo bot ⇒ mọi endpoint cùng nhóm đều có nguy cơ. Cần Dev liệt kê để mở ticket riêng. |
| `BUG-GAP-02` | **Conflict contract 400 vs 403**: fix gộp "mã không hợp lệ" + "mã ngoài bot" cùng trả **403**, trong khi spec sprint 36436 (`spec-dev-BE:64-67`) ghi **400** cho invalid input. | Studio đã đánh dấu 2 TC là `spec_status = needs-human-review` và **không khoá được status code**. Leader/PO phải chốt contract trước khi kết luận Đạt. |
| `BUG-GAP-03` | Mức verify của Dev chỉ là **`lint`**; **không dump được DB** (MySQL dev Connection refused) ⇒ khẳng định "ràng buộc bot_id không loại nhầm bản ghi hợp lệ" **chỉ dựa trên schema**, chưa kiểm dữ liệu thật. | Nếu môi trường thật có tin gửi / mẫu tin lệch `bot_id` (dữ liệu legacy) thì **chính chủ bot bị 403** hoặc **số đếm giảm sai**. Bắt buộc có TC audit dữ liệu trên môi trường gần thật. |
| `BUG-GAP-04` | Description ghi `TemplateV2Controller.php:1051`, journal ghi `:1056`. | Lệch 5 dòng — tester đối chiếu lại đúng vị trí code khi verify. |
| `BUG-GAP-05` | Dev **không nêu impact tới `ChatController`** ở mục 4.3 dù có nhắc ở phần quét ngang mục 2. | 4.3 chỉ liệt kê FA-008 + FA-010; nếu chat cũng đọc broadcast theo mã thô thì phạm vi regression rộng hơn Dev khai. |
