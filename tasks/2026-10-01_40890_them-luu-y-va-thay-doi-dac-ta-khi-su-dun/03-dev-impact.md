# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`) rồi parse section "Đánh giá ảnh hưởng", fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

⚠️ **INPUT KHÔNG CHUẨN**: Redmine #40890 **KHÔNG có section "Đánh giá ảnh hưởng phía dev"** theo format 4 mục chuẩn (ticket Feature, không phải Bug, chỉ có 1 journal "BÁO CÁO TIẾN ĐỘ AI DEV" dạng progress report — xem nguyên văn ở `01-bug-task.md`). Nội dung 4 mục dưới đây được tái dựng từ **MCP LME TEST STUDIO** — task #330 (`task_get_context` → field `dev_impact`, suy từ **diff thật** trên branch `ai-feature-40890`, không phải Dev tự viết tay) + journal Redmine. **Tester/Leader bắt buộc verify lại trước khi tick checkbox bên dưới**, đặc biệt mục 3 (caller đã check) vì AI dev chỉ ghi "checklist 11 mục" chứ không liệt kê danh sách caller cụ thể.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Assignee Redmine trống; journal báo cáo tiến độ do "Do Van Tu TuDV" đăng nhưng ghi rõ là comment tự động từ AI dev workflow, không phải người viết tay>` |
| Commit / Pull Request | `<chưa có link PR>` — commit `31bd44d4bc` trên branch `ai-feature-40890` (base `131bde0f22` → HEAD `f0fbccea6e`) |
| Branch | `ai-feature-40890` |
| Ngày submit đánh giá | 2026-09-25 (journal #138551) / Studio task #330 tạo lúc 2026-09-25 09:52:28 |
| Auto-filled | 2026-10-01 by /new-task (nguồn: MCP LME TEST STUDIO `task_get_context` dev_impact + spec_delta, task #330) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact). ⚠️ Redmine không có section này — verify dựa trên `dev_impact` của Studio thay thế, cần đối chiếu thêm với Dev nếu nghi ngờ.

---

## 1. Nguyên nhân

`<Không áp dụng — đây là Feature request (thêm lưu ý UI + khả năng đổi đặc tả bắt buộc nhập liệu), không phải bug fix nên không có "nguyên nhân lỗi".>`

Yêu cầu gốc: thêm banner lưu ý trong panel ③「編集」 của màn `お客様への質問項目` (cả 2 hệ レッスン予約 + サロン・面談予約), thông báo rằng khi bật chức năng thanh toán (決済連携), 2 mục mặc định 「お名前」「メールアドレス」 sẽ là bắt buộc phải trả lời vì cần liên kết với hệ thống thanh toán.

## 2. Cách fix

Theo `dev_impact` (Studio, suy từ diff thật trên branch):

- **FE-only**: sửa 3 file blade — tạo mới partial `payment_required_notice.blade.php` (banner dùng chung) + `@include` partial này vào `setting_form.blade.php` của cả 2 màn calendar (lesson) và calendar-salon (salon). Không chạm API/BE/DB/Job.
- Banner hiển thị **có điều kiện**: chỉ hiện khi item đang chọn ở panel ③ là 1 trong 2 item mặc định hệ thống tạo sẵn (nhận diện qua cờ "không cho xoá" `can_delete`, **không** theo nội dung câu hỏi hay loại câu hỏi) — ẩn khi chọn câu hỏi do admin tự thêm hoặc khi panel ③ đang trống.
- Nội dung banner là chuỗi tĩnh (hằng số), không phải biến động — không phát sinh bề mặt XSS mới.
- Diff thật (spec_delta.diffStat từ Studio):
  ```
  .../components/payment_required_notice.blade.php   | 26 ++++++++++++++++++++++
  .../setting_calendar_tab/setting_form.blade.php    |  2 ++
  .../setting_calendar_tab/setting_form.blade.php    |  2 ++
  3 files changed, 30 insertions(+)
  ```

⚠️ Chưa thấy đề cập thay đổi logic **validate bắt buộc nhập** (phần "仕様変更" / thay đổi đặc tả trong tên ticket) — cần hỏi lại Dev xem 2 field này vốn đã bắt buộc sẵn khi bật thanh toán hay cần thêm validate riêng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

⚠️ **Input thiếu** — AI dev report chỉ ghi "Checklist: 11 mục — pass 10 / manual 1" (journal #138551 mục 3), không liệt kê danh sách caller/function cụ thể đã check. Container dev không có DB/Redis nên Dev chỉ verify compile/lint + kiểm tĩnh, chưa chạy runtime thật.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `setting_form.blade.php` (レッスン予約 — calendar_management) | `@include` partial banner mới | Hiện banner trong panel ③「編集」 |
| 2 | `setting_form.blade.php` (サロン・面談予約 — calendar-salon) | `@include` partial banner mới | Hiện banner trong panel ③「編集」 — bản sao gần giống màn Lesson |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Partial banner lưu ý thanh toán (mới) | `resources/views/basic/calendar_management/tabs/setting_calendar_tab/components/payment_required_notice.blade.php` | Direct | File mới, dùng chung cho cả 2 hệ (quyết định AI tự chọn D-01, chưa được BA/TA confirm — xem `01-bug-task.md`) |
| F2 | Panel ③「編集」 màn `お客様への質問項目` — hệ レッスン予約 | `setting_form.blade.php` (calendar_management) | Direct | Include banner mới |
| F3 | Panel ③「編集」 màn `お客様への質問項目` — hệ サロン・面談予約 | `setting_form.blade.php` (calendar-salon) | Direct | Include banner mới |

### 4.2. List data bị update khi fix bug

`<Không có>` — theo `dev_impact` Studio: thay đổi chỉ ở 3 file blade (view layer), không chạm API/BE/DB/cache/migration.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | Không có data nào bị update (FE-only, banner tĩnh) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | FA-019 Đặt lịch bài học (`レッスン予約`) — tab `予約設定` › `お客様への質問項目` › panel ③「編集」 | F1, F2 | Medium — rủi ro banner xô lệch layout panel ③ (counter n/50, toggle 表示設定/回答設定, dropdown 友だち情報) hoặc rò rỉ sang item tự thêm nếu điều kiện hiển thị sai |
| T2 | FA-020 Đặt lịch salon (`サロン・面談予約`) — tab `予約設定` › `お客様への質問項目` › panel ③「編集」 | F1, F3 | Medium — cùng rủi ro như T1; thêm rủi ro "làm 1 hệ quên hệ kia" vì 2 màn là bản sao gần giống nhau |
| T3 | Màn xem trước (`プレビュー`) + màn đặt lịch phía khách (LINE user) của cả 2 hệ | F1 (banner phải KHÔNG rò ra ngoài) | Low — banner là lưu ý cho quản trị viên, không được hiện ở phía khách |

**Rủi ro hồi quy chính** (theo `dev_impact` Studio): (1) quên áp dụng cho 1 trong 2 hệ Lesson/Salon — giảm thiểu nhờ dùng chung 1 partial; (2) banner rò rỉ sang item admin tự thêm nếu điều kiện `v-if`/`can_delete` sai; (3) chèn markup xô lệch layout panel ③ (counter, toggle, dropdown).

**8 requirements đã chốt trên Studio (task #330)** — dùng làm checklist đối chiếu coverage ở `/review-tc`:

| Req | Tóm tắt | Risk |
|---|---|---|
| REQ-001 | Banner hiện trong panel ③ khi chọn item mặc định | High |
| REQ-002 | Nội dung banner đúng nguyên văn chuỗi JP đã chốt | High |
| REQ-003 | Banner KHÔNG hiện với item tự thêm / khi panel ③ trống | High |
| REQ-004 | Điều kiện hiển thị banner độc lập trạng thái 決済連携 | Medium |
| REQ-005 | Hình thức hiển thị đúng đặc tả thiết kế (màu, khoảng cách, bo góc) | Medium |
| REQ-006 | Banner chỉ-đọc, không tương tác | Medium |
| REQ-007 | Các phần tử sẵn có của panel ③ + màn xem trước không đổi | Medium |
| REQ-008 | Hoạt động đúng trên lịch cũ + tài khoản staff | Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ hiện đang **thiếu**, cần hỏi lại Dev
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — ⚠️ cần hỏi rõ phần "仕様変更" (thay đổi đặc tả bắt buộc nhập) đã code hay chưa
