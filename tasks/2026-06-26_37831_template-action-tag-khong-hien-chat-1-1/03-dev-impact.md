# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **LƯU Ý QUAN TRỌNG — có 2 lần đánh giá ảnh hưởng KHÁC NHAU trong Redmine:**
> 1. **AI auto-fix sớm** (journal #122460, 2026-06-18, branch `ai_fixbug_37831`): root cause bug ① = `array_diff` so sánh capture template **1 chiều** + fix bug ② (escaping `@json`). Cover **cả ① và ②**.
> 2. **Human dev — bản mới nhất** (journal #123773, 2026-06-26, branch `m_202606_clear-cache-sourcemessage_37831`): root cause bug ① = **job cache source_message 30s**. Chỉ cover **bug ①**, KHÔNG đề cập bug ②.
>
> File này lấy **bản mới nhất (human dev #123773)** làm chính (mục 1–4 bên dưới). Bản AI auto-fix để ở phần **Phụ lục** cuối file (tham khảo, đặc biệt cho bug ②).
> ❗ **Tester/Leader cần xác nhận với Dev:** (a) fix đang test là bản nào (cache-clear hay symmetric-diff)? (b) bug ② (ký tự `&`) đã được fix & deploy trong release này chưa? — vì bản mới nhất không nhắc tới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương (báo cáo ảnh hưởng #123773); assigned_to: Kieu Son Tung |
| Commit / Pull Request | https://bitbucket.org/snstool/linect-service/commits/e5a7570fea76517cb6450e91855813f15715d5c0 |
| Branch | m_202606_clear-cache-sourcemessage_37831 |
| Ngày submit đánh giá | 2026-06-26 |
| Auto-filled | 2026-06-26 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn journal #123773 (Thanh Phương, 2026-06-26):

- Job cache source message của action, template, step_message 30s. Nếu KH thay đổi và gửi lại luôn trong 30s cache thì hiển thị trên chat 1:1 source cũ.

## 2. Cách fix

> Nguyên văn journal #123773:

- Web khi update action, template, step_message socket cho job để clear cache.
- Khi update template thì cần update cả action, step_message của bot đó, vì template có thể dùng trong action, step_message.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — journal #123773 mục 3 để trống. Hỏi Dev liệt kê caller đã check.>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Nguyên văn journal #123773 mục 4.1:

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | ActionSourceMessageCache | `<chưa rõ — Dev fill>` | Direct | Clear cache khi update action |
| F2 | ScenarioSourceMessageCache | `<chưa rõ — Dev fill>` | Direct | Clear cache khi update step_message |
| F3 | TemplateSourceMessageCache | `<chưa rõ — Dev fill>` | Direct | Clear cache khi update template (kéo theo action + step_message) |

### 4.2. List data bị update khi fix bug

> Nguyên văn journal #123773 mục 4.2: "Không có".

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có data bị migrate/update | — | Chỉ clear cache source_message (không đổi schema/data). Cache là vùng tạm. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn journal #123773 mục 4.3:

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Update rồi gửi lại template/action/step_message trong vòng 30s → chat 1:1 hiện đúng nội dung mới | F1, F2, F3 | High |
| T2 | Không update, gửi lại bình thường → vẫn hiển thị đúng (không regress) | F1, F2, F3 | Medium |
| T3 | Update **template** → clear cache lan cả cho action & step_message (do template dùng chung) | F3 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **hiện đang trống, cần Dev bổ sung**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Xác nhận fix đang deploy: cache-clear (#123773) hay symmetric-diff (#122460)?**
- [ ] **Xác nhận bug ② (ký tự `&` nửa chiều rộng) có nằm trong release này không.**

---

## Phụ lục — Đánh giá AI auto-fix sớm hơn (journal #122460, 2026-06-18) — THAM KHẢO

> Branch `ai_fixbug_37831` (gốc `release_step_20260511`, commit `aa34323953`, 4 file). Đây là root cause/fix do hệ thống AI auto-fix đề xuất **trước** đánh giá human #123773. Giữ lại vì là nguồn DUY NHẤT cover **bug ②**. KHÔNG chắc bản này có được merge/deploy hay không — cần Dev xác nhận.

**1. Nguyên nhân (AI):**
- Lỗi ①: khi lưu tin, code so sánh danh sách capture template để quyết định tạo `source_messages` mới hay dùng lại bản cũ, nhưng chỉ so MỘT CHIỀU `array_diff(cũ, mới)`. Khi danh sách mới có thêm capture (cũ ⊂ mới, vd cũ=[3157269], mới=[3157269,3691006]) thì `array_diff` trả `[]` → tưởng không đổi → dùng lại `source_messages` cũ thiếu capture mới → tin lưu trỏ tới nguồn cũ thiếu nội dung → màn chat 1:1 không hiển thị (dù LINE vẫn gửi tới điện thoại).
- Lỗi ②: màn chi tiết nhúng tên template vào biến JS bằng escape HTML (`{{ }}`) nên `&` bị đổi thành thực thể HTML và hiện nguyên văn.

**2. Cách fix (AI):**
- Lỗi ①: sửa `app/Services/MessageService.php` — đổi so sánh capture template từ 1 chiều sang ĐỐI XỨNG (`array_diff` cả 2 hướng) tại 5 chỗ (template đơn + broadcast/scenario/event/action).
- Lỗi ②: 3 màn quản lý template xuất tên template ra JS bằng `@json` thay vì `{{ }}`.

**3. Đã check function (AI):** `MessageService::createMessageTypeV2` (~802/826/848/870), `MessageService::handleCreateMessageTemplate` (~611), `ChatController::refreshMessage` (hiển thị), `TemplateV2Controller::createGroupTemplate`.

**4.1 File thay đổi (AI):**
- `app/Services/MessageService.php`
- `resources/views/basic/template_v2/add.blade.php`
- `resources/views/basic/template_v2/add-template.blade.php`
- `resources/views/basic/message_template/park-template/add.blade.php`

**4.2 Data (AI):** Không cần migrate. ⚠️ Vận hành: tin CŨ đã lưu trước fix vẫn trỏ `source_messages` thiếu capture → vẫn không hiện; fix chỉ áp dụng cho tin gửi MỚI sau deploy. Tên template từng bị lưu lặp `&amp;amp;` cần KH sửa lại 1 lần.

**4.3 Tính năng (AI):**
- Lưu & hiển thị tin nhắn template/action ở màn 1:1 chat quản trị — tin gửi qua action (thêm tag) hiện đúng.
- Quản lý Template — màn chi tiết hiển thị đúng ký tự `&` nửa chiều rộng.

**Rủi ro AI tự nêu:** tin cũ trước deploy không tự hiện lại; symmetric diff tạo `source_messages` mới nhiều hơn khi danh sách capture thực sự khác (đúng mục đích).
