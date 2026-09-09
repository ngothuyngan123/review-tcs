# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39742 — journal `129308` ngày **2026-08-19T04:40:29Z**, user `AI LME Fix bug`
> (báo cáo tự động của hệ thống **Auto-fixbug LME**). Description của ticket KHÔNG chứa đánh giá ảnh hưởng.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (Auto-fixbug LME) — assignee hiện tại: `Thanh Phương` |
| Commit / Pull Request | `<không có link PR>` — commit `afe26df872` trên nhánh `ai_fixbug_39742` (7 file, đã push). Nhánh nguồn của cách sửa: `origin/improve-action-open-link` (2 commit `53757f6688` + `9c728a9b1d`) |
| Branch | `ai_fixbug_39742` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-19` |
| Auto-filled | `2026-09-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục 1 của journal 129308. -->

Action cấu hình ở mục "khi mở page" bị gửi lại mỗi lần trang được mở lại (tải lại trang, quay lại trang), vì server không có cách nào biết action đã gửi rồi. Nhánh tham chiếu `improve-action-open-link` đã xử lý theo hướng thêm tham số vào URL sau khi gửi action xong, nhưng nhánh đó chưa bao giờ được đưa lên nhánh release đang dùng nên cả 2 chỗ trên release vẫn còn lỗi.

## 2. Cách fix

<!-- Nguyên văn mục 2 của journal 129308. -->

Sửa theo AI review vòng 1 (1 lỗi bắt buộc): trước đó khi biểu mẫu đã đạt giới hạn tổng số câu trả lời (`false_limit_reply`) hoặc chính người dùng đã trả lời đủ số lần cho phép (`false_reply_kind`), server trả về sớm mà **KHÔNG** kèm cờ báo đã gửi action, nên giao diện không ghi được tham số vào URL — action khi mở page vẫn bị gửi lại mỗi lần tải lại trang (rất hay gặp: mở lại link biểu mẫu từ lịch sử chat LINE). Đã bổ sung cờ `hasAction` / `sendActionSuccess` vào cả 2 phản hồi trả về sớm này, giống phản hồi thành công. Đồng thời chuyển khối ghi tham số vào URL ở giao diện lên **TRƯỚC** phần xử lý các nhánh, vì đúng 2 nhánh giới hạn này có thể chuyển hướng sang URL khác — ghi trước để chắc chắn tham số được lưu vào trang hiện tại. **Không đụng phần bán hàng (bill tiền)** vì trang đó không có nhánh trả về sớm tương tự.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Chuyển list plain của mục 3 journal 129308 sang bảng template. Cột "Thay đổi"/"Lý do" giữ nguyên chữ Dev ghi. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerController::userOpenFormanswer` — `app/Http/Controllers/Basic/FormAnswerController.php` | Có sửa | Bổ sung cờ `hasAction`/`sendActionSuccess` vào 2 nhánh trả về sớm (`false_limit_reply`, `false_reply_kind`) |
| 2 | `FormAnswerService::renderFormAnswer` — `app/Services/FormAnswer/FormAnswerService.php` | Có sửa | Nằm trong luồng render form v3 |
| 3 | `openFormanswer` — `public/js/form_answer/form_render_v3.js` | Có sửa | Chuyển khối ghi param vào URL lên TRƯỚC phần xử lý các nhánh |
| 4 | form_render v3 blade — `resources/views/basic/form_answer/v3/form_render.blade.php` | Có sửa | Khai báo biến JS |
| 5 | `SalesManagementV2Controller::orderDetail` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Có sửa | Áp cùng cách fix cho màn bill tiền bản mới |
| 6 | order detail v2 blade — `resources/views/basic/sales/v2/order/detail.blade.php` | Có sửa | Khai báo biến JS + ghi param vào URL |
| 7 | `sendAction` / `sendActionOrderItem` — `app/Helpers/functions.php` | **Chỉ ĐỌC, không sửa** | Hàm dùng chung gửi action — Dev chủ động không đụng |
| 8 | `SalesManagementController::orderDetail` (bản cũ `is_product_new=0`) | **Đã rà, KHÔNG sửa** | Đã redirect sang bản v2 cho sản phẩm mới |
| 9 | `form_render.js` + `form_render.blade` (biểu mẫu bản cũ) | **Đã rà, KHÔNG sửa** | Màn cũ, không gửi tham số nên hành vi giữ nguyên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- ⚠️ Mục 4.1 trong journal Dev ghi là "File thay đổi" (7 file), KHÔNG phải list function.
     Bảng dưới ghép 7 file đó với function tương ứng Dev đã nêu ở mục 3.
     Cột "Mức độ ảnh hưởng" suy từ chính chữ Dev viết (sửa = Direct, chỉ đọc/đã rà = Indirect). -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerController::userOpenFormanswer` | `app/Http/Controllers/Basic/FormAnswerController.php` | Direct | Thêm cờ vào 2 nhánh trả về sớm |
| F2 | `SalesManagementV2Controller::orderDetail` | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | Màn bill tiền bản mới |
| F3 | `FormAnswerService::renderFormAnswer` | `app/Services/FormAnswer/FormAnswerService.php` | Direct | |
| F4 | (config version asset) | `config/sns-line.php` | Direct | Dev liệt kê trong 7 file thay đổi nhưng **KHÔNG giải thích ở mục 2 và 3** — nghi là bump version asset JS/CSS. ⚠️ Điểm cần hỏi Dev |
| F5 | `openFormanswer` (JS) | `public/js/form_answer/form_render_v3.js` | Direct | Đổi thứ tự ghi param vào URL |
| F6 | form_render v3 blade | `resources/views/basic/form_answer/v3/form_render.blade.php` | Direct | Khai báo biến JS |
| F7 | order detail v2 blade | `resources/views/basic/sales/v2/order/detail.blade.php` | Direct | Khai báo biến JS + ghi param vào URL |
| F8 | `sendAction` / `sendActionOrderItem` | `app/Helpers/functions.php` | Indirect | Chỉ đọc, không sửa — nhưng là hàm **dùng chung** cho nhiều nhánh action khác |
| F9 | `SalesManagementController::orderDetail` (v1) | — | Indirect | Đã rà, không sửa |
| F10 | `form_render.js` + `form_render.blade` (form bản cũ) | — | Indirect | Đã rà, không sửa |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2 journal 129308. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `user_open_formanswer.count_click` | UPDATE | **Vẫn tăng mỗi lần mở trang như cũ (không đổi)** — chỉ việc GỬI action là bị bỏ qua khi đã gửi rồi |
| D2 | `bot_line_user_item.count_action_view_page` | UPDATE | **Chỉ còn tăng khi action thật sự được gửi** → số đếm sẽ không bị cộng lặp khi khách tải lại trang. ⚠️ Đây là **thay đổi hành vi số liệu**, không chỉ là fix bug |
| D3 | `action_lineuser` | CREATE (giảm) | Giảm số bản ghi action trùng lặp sinh ra do tải lại trang |

**Recover data:** Dev ghi rõ ✔ **Không cần recover data cũ**.

⚠️ Lưu ý cho Leader: D2 nghĩa là **số liệu thống kê lượt xem trang sau fix sẽ THẤP HƠN trước fix** với cùng lượng truy cập. Dev không nêu việc này có cần thông báo cho khách/PM hay không.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 journal 129308. Cột "Nguy cơ regression" Dev KHÔNG ghi mức. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — action khi mở biểu mẫu chỉ gửi 1 lần, không gửi lại khi tải lại trang | F1, F3, F5, F6, D1, D3 | `<Dev không ghi mức>` |
| T2 | **Single Product / Sales (FA-026)** — action khi hiển thị trang chi tiết sản phẩm không gửi lại khi tải lại trang; số đếm lượt xem trang cũng không bị cộng lặp | F2, F7, D2 | `<Dev không ghi mức>` |
| T3 | **Action Settings (SC-004)** — cơ chế gửi hành động tự động gắn với 2 màn trên | F8, D3 | `<Dev không ghi mức>` |

---

## Phụ lục — mục 5 & 6 nguyên văn từ journal 129308

> Template 03 chỉ có 4 mục; journal của Auto-fixbug có thêm mục 5 (recover data) và 6 (verify).
> Giữ lại nguyên văn vì mục 6 là **bằng chứng phạm vi fix** mà Leader cần thẩm định.

**■ 5. RECOVER DATA** — ✔ Không cần recover data

**■ 6. VERIFY**

- **Mức: `lint`** (⚠️ **không phải test chức năng**)
- **Lệnh:** `php -l` trên 4 file PHP đã sửa: No syntax errors detected; Biên dịch Blade rồi `php -l` cho 2 file blade đã sửa: No syntax errors detected; `node --check public/js/form_answer/form_render_v3.js`: OK; `git diff --stat release_step_20260805...ai_fixbug_39742`: đúng 7 file, không kéo commit lạ
- **Bằng chứng:**
  - Nhánh tham chiếu `origin/improve-action-open-link` (2 commit `53757f6688` + `9c728a9b1d`) là nguồn của cách sửa; đã đối chiếu từng chỗ với code hiện tại trên release
  - Đã xác nhận cách sửa **CHƯA có trên release**: `git grep sendActionSuccess origin/release_step_20260805` = 0 kết quả
  - **Tra schema DB: chỉ có đúng 2 cột action khi mở page là `form_answer.action_open_id` và `s_items.action_show_page_id`** ⇒ phạm vi triển khai ngang đúng bằng 2 chỗ trong tiêu đề ticket
  - Đã kiểm 2 điểm gọi `openFormanswer` loại trừ nhau (`mounted` khi có `line_user_id` vs `liff.init` khi `!line_user_id`) ⇒ 1 lần gọi mỗi lần tải trang
  - ⚠️ **KHÔNG chạy được truy vấn DB dev để đếm dữ liệu thật**: MySQL `host.docker.internal:3306` báo Connection refused (dev stack đang tắt)

**■ Dashboard fixbug:** `https://dashboard.melonglobal.net/fixbug-lme/?id=39742`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn đã phát hiện khi auto-fill (Leader cần hỏi Dev)

1. **`config/sns-line.php`** nằm trong 7 file thay đổi nhưng **không được giải thích ở mục 2 lẫn mục 3** → hỏi Dev đây có phải bump version asset không, và ảnh hưởng cache phía user ra sao.
2. **Phạm vi "triển khai ngang" chốt bằng schema DB** (2 cột action) — cần thẩm định: cơ chế "action khi mở page" có chỗ nào **không** dựa vào 2 cột đó không (vd. LIFF entry, richmenu, scenario).
3. **Mâu thuẫn bề mặt trong chính journal**: mục 2 nói *"Không đụng phần bán hàng (bill tiền)"* nhưng mục 3 + 4.1 lại liệt kê `SalesManagementV2Controller::orderDetail` và blade order detail v2 là **có sửa**. Thực chất nhiều khả năng: bill tiền vẫn được port cách fix chính, chỉ là không có 2 nhánh early-return để vá thêm. Cần Dev xác nhận lại cách diễn đạt.
4. **D2 làm số liệu `count_action_view_page` giảm so với trước fix** → có cần thông báo PM/khách không?
5. Mức verify của Dev chỉ là **lint**, chưa chạy test chức năng, và **không query được DB** → mọi khẳng định về số bản ghi action đều **chưa có bằng chứng runtime từ phía Dev**.
