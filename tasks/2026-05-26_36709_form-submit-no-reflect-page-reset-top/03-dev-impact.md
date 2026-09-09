# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36709 (journal #119442 — Thanh Phương, 2026-05-26) by `/new-task` lúc 2026-05-26.
> Tester verify rồi tick checkbox "Tester verify auto-fill chính xác" bên dưới.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương (journal author Section "Đánh giá ảnh hưởng"). Redmine assigned_to = Kieu Son Tung — tester confirm với Leader nếu khác. |
| Commit / Pull Request | `<chưa có — Redmine custom field "Commit Date" rỗng, journal chưa kèm PR>` |
| Branch | `<chưa rõ — Dev chưa ghi>` |
| Ngày submit đánh giá | 2026-05-26 (journal #119442 created_on) |
| Auto-filled | 2026-05-26 by `/new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bug xảy ra do sự kết hợp của 2 lỗi ở cả Backend và Frontend.

- **B1**: User thêm page mới — BE chỉ thiếu thông tin `next_page_setting` của previous page (page hiện tại trước khi thêm page mới).
- **B2**: User xóa page mới vừa thêm — chưa update lại loại `next_page_type` của previous page về `END_FORM`.
- **B3**: User reload màn hình và nhấn Save form (lỗi FE):
  + Sau reload, có 1 logic FE đang set `next_page_setting` là **chính page hiện tại** (self-reference).
  + User nhấn Save form → giao diện gửi state hỏng (self-reference) xuống database.

**Hệ quả:**
- Database có 1 page cuối nhưng `next_page_setting` trỏ về chính nó.
- Khi user submit form, hệ thống thấy "có page tiếp theo" và "page tiếp theo chính là page hiện tại" → render lại đúng page đang đứng → biểu hiện ra là submit xong reset về top, không hiển thị kết quả.

=> Đây là lý do form 「1Mアンケート」 của T CLINIC submit không reflect kết quả.

## 2. Cách fix

- **Fix BE** — `FormAnswerService::addPage` (`app/Services/FormAnswer/FormAnswerService.php`):
  + Khi thêm page mới, ghi đầy đủ thông tin vào database — vừa đánh dấu "có page tiếp theo" (`next_page_type = RIGHT_PAGE = 1`), vừa ghi rõ id của page tiếp theo (`next_page_setting = {pageId: newPageId}`) cho previous page.

- **Fix FE** — `titlePageRight()` (`public/js/form_answer/v3/setting_form_items.js`):
  + Thêm guard `page.next_page_setting && ...` — tránh crash khi `next_page_setting=null`.
  + Bỏ wrap về index 0 khi page hiện tại là page cuối — return label rỗng (`'選択してください'`) thay vì self-reference.
  + Bỏ dòng mutate state `page.next_page_setting = {...}` — hàm render label không được sửa data.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chỉ ghi heading mục 3 mà không liệt kê chi tiết — chỉ note "Đã check và sửa". -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerService::addPage()` — `app/Services/FormAnswer/FormAnswerService.php` | Ghi đầy đủ `next_page_type` + `next_page_setting` cho previous page khi thêm page mới | Tránh để DB ở trạng thái thiếu thông tin (B1 root cause). |
| 2 | `titlePageRight()` — `public/js/form_answer/v3/setting_form_items.js` | Guard null, bỏ self-reference, bỏ mutate state | Tránh render gây self-reference (B3 root cause). |

> **Input thiếu**: Dev không ghi rõ đã check những caller nào khác của `addPage`/`titlePageRight` hoặc các function liên quan như `removePage`, `checkingNextPage` (được mention ở mục 4.3). Tester nên hỏi lại Dev xem có cần bổ sung không (Leader checklist mục 3).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerService::addPage()` | `app/Services/FormAnswer/FormAnswerService.php` | Direct | Sửa logic ghi DB khi thêm page mới (root fix BE). |
| F2 | `titlePageRight()` | `public/js/form_answer/v3/setting_form_items.js` | Direct | Sửa render label "Page tiếp theo" (root fix FE — guard null, bỏ self-reference, bỏ mutate). |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answer_pages.next_page_type` | UPDATE (qua flow addPage) | `3 (END_FORM)` → `1 (RIGHT_PAGE)` khi `addPage` có previous page (behavior như cũ, không đổi). |
| D2 | `form_answer_pages.next_page_setting` | UPDATE (qua flow addPage) | `null` → `{"pageId": <newPageId>}` khi `addPage` có previous page (**điểm thay đổi mới**). |

> Không có table/column nào khác bị ảnh hưởng. Không có schema migration.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Thêm page mới (Form rẽ nhánh)** — previous page giờ được lưu `next_page_setting={pageId:newId}` ngay từ BE. Test: thêm page → reload → flow hiển thị đúng tên page tiếp theo. | F1, D1, D2 | High |
| T2 | **Xóa page (Form rẽ nhánh)** — cleanup ở `removePage` giờ chạy đúng → khi xóa page cuối, page trước tự reset về `END_FORM`. Test: thêm page → xóa page mới → page trước phải về `type=3, setting=null`. | F1 (chained), D1, D2 | High |
| T3 | **Save form sau khi thêm/xóa page** — DB nhất quán ngay sau mỗi thao tác + FE không còn tạo self-reference trong render → save form không thể persist data hỏng. | F1, F2, D1, D2 | High |
| T4 | **Hiển thị label "Page tiếp theo"** trên màn setting — với page cuối có `type=1` (data lịch sử corrupt), label giờ hiển thị `'選択してください'` thay vì wrap về page đầu. UX nhất quán hơn, không thay đổi data ngầm. | F2 | Medium |
| T5 | **Form submit (public render)** — với data nhất quán, `checkingNextPage` trả response đúng → submit hiển thị kết quả, không reset top. | F1, F2, D1, D2 | High |
| T6 | **分岐 (branching, `next_page_type = 2`)** — không bị ảnh hưởng, fix chỉ chạm path `type=1 (RIGHT_PAGE)`. | (no impact) | Low (regression check) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — đặc biệt `removePage`, `checkingNextPage`)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — kiểm tra xem có nên add `removePage` / `checkingNextPage` không
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — fix chỉ chạm `form_answer_pages`, không có migration
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng (edge: page cuối với data corrupt từ trước, form đa page nested, branching type=2)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
