<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297 | sheet=Test fix bug | anchor=Main Function -->

# 04 — TC List (fetched từ Redmine #38075 Link TCs)

> ⚠️ **TCs human read-only** — fetch từ Sheet, KHÔNG sửa Title/Expected dù bug fix đổi behavior.
> Redmine ghi `row 45~50`, nhưng block #38075 thực tế trong Sheet trải **row 45–52** (8 TC). Đã lấy đủ cả block — 2 TC quan trọng nhất (staff-permission, bot đã xóa) nằm ở row 51–52.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297 — tab "Test fix bug" |

---

## TC List

> Nguồn là Sheet phân cấp (Main Function / Sub1–Sub4 / Expect Result). Mỗi scenario lá = 1 TC. Giữ NGUYÊN nội dung & Expected từ Sheet.
> Cột **Type** suy luận nhẹ từ bản chất scenario (Positive/Negative/Boundary); cột **Priority** Sheet gốc không có → để trống. Cột **Status** = kết quả test human đã đánh dấu trong Sheet (cột "Bug Tester #38075").

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check user login — User chưa có bot nào | Positive | | User mới, chưa có bot nào | 1. Login account | Sau khi login hiển thị màn hình add bot `/admin/bot-add-v2` | staging | | OK |
| TC002 | Login — User đã có bot nhưng chưa có lịch sử select bot (`user_selected_bot` không có bản ghi) | Positive | | User đã có bot; bảng `user_selected_bot` KHÔNG có bản ghi | 1. Login account | Sau khi login hiển thị màn hình `/admin/pre-select-bot` để user chọn bot | staging | | OK |
| TC003 | Login (chưa có lịch sử select) — Access trực tiếp URL 1 menu bot | Negative | | User đã có bot; `user_selected_bot` không có bản ghi | 1. Access trực tiếp URL của 1 menu bot: `/basic/message-template` | `<Expected để trống trong Sheet gốc — Leader/member bổ sung>` | | | |
| TC004 | Login (chưa có lịch sử select) — Access trực tiếp URL 1 menu user | Negative | | User đã có bot; `user_selected_bot` không có bản ghi | 1. Access trực tiếp URL của 1 menu user: `/admin/my-page` | `<Expected để trống trong Sheet gốc — Leader/member bổ sung>` | | | |
| TC005 | Login — Đã có lịch sử select, select vào bot đang làm owner | Positive | | `user_selected_bot` đã có bản ghi; bot đang select là bot user làm owner | 1. Login account | Sau khi login hiển thị màn overview của bot được select | staging | | OK |
| TC006 | Login — select vào bot của user khác và đang được làm staff | Positive | | `user_selected_bot` trỏ tới bot của user khác; user đang là staff bot đó (có trong `user_staff_bot`) | 1. Login account | Sau khi login hiển thị màn overview của bot được select | staging | | OK |
| TC007 | Login — select vào bot của user khác và KHÔNG được làm staff (core fix #38075) | Negative | | `user_selected_bot` trỏ tới bot của user khác; user KHÔNG là staff (không có trong `user_staff_bot`) | 1. Login account | Sau khi login hiển thị màn hình `/admin/pre-select-bot` để user chọn bot | staging | | OK |
| TC008 | Login — select vào bot đã bị xóa / không tồn tại | Boundary | | `user_selected_bot` trỏ tới bot `is_deleted=1` hoặc không tồn tại trong db | 1. Login account | Sau khi login hiển thị màn hình `/admin/pre-select-bot` để user chọn bot | staging | | OK |

### Chú thích cột

- **Type**: Positive (happy path) / Negative (điều kiện sai → verify redirect) / Boundary (giá trị biên: bot đã xóa). Suy luận nhẹ để hỗ trợ review; KHÔNG có trong Sheet gốc.
- **Priority**: Sheet gốc không có → để trống.
- **Status**: human đã test = `OK` (cột "Bug Tester #38075" ghi "OK staging"). TC003/TC004 Sheet để trống Expected + Result.

### Environment (note)

Human test trên **Staging** (`staging.lme.jp`) — Sheet đánh dấu "OK staging".

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH) → TC007
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được (lưu ý TC003/TC004 thiếu Expected)
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng:

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§C Các tính năng chung** (chọn feature mà task chạm đến):
- [ ] C.7 Plan limits (nếu liên quan)

<!-- Source: fetched từ Redmine #38075 Link TCs, tab "Test fix bug" (gid 2004892297), block #38075 = row 45-52 (Redmine ghi "row 45~50") lúc 2026-06-25. Fetch qua service account (scripts/fetch_sheet.py) vì MCP google-sheets không kết nối được phiên này. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
