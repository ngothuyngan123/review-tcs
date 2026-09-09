<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297#gid=2004892297 -->
# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
> Member copy file này (hoặc paste từ Excel/Google Sheet) vào folder review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc (nếu có) | `https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297#gid=2004892297` (tab "[AI] TCs_37743", row 23-32) |

---

## TC List

> Bảng TC dùng **10 cột chuẩn team**. Cột Status giữ nguyên giá trị fetch từ Sheet.
> Sheet gốc có cột Feature/Category (không có trong template 10 cột) → gộp vào cột **Output note** để không mất dữ liệu.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-AH-019 | setBotInvite (chọn bot thủ công) vẫn ghi history như cũ (CL-NF-02) | Positive | High | User có quyền bot X: Chọn bot trên header | 1. Staff accept invite bot A<br>2. Staff chuyển sang bot X trên header<br>3. Vào màn「アクセス履歴」bot X | - Record được ghi như logic cũ (path setBotInvite không bị phá vỡ)<br>-「最終ログイン」(last_time_login) của user được cập nhật (BR-012 giữ nguyên) | Feature: Access History \| Category: Regression | | OK Step |
| TC-AH-019b | setBotInvite (chọn bot thủ công) vẫn ghi history như cũ (CL-NF-02) | Positive | High | User có quyền bot X: Chọn bot trong màn list bot | 1. Staff accept invite bot A<br>2. Staff chuyển sang bot X trong màn hình list bot<br>3. Vào màn「アクセス履歴」bot X | - Record được ghi như logic cũ (path setBotInvite không bị phá vỡ)<br>-「最終ログイン」(last_time_login) của user được cập nhật (BR-012 giữ nguyên) | Feature: Access History \| Category: Regression | | OK Step |
| TC-AH-020 | Tương tác setBotInvite + access cùng ngày không tạo record trùng | Edge Case | High | Hôm nay user đã setBotInvite bot X (đã có 1 record). | 1. Sau khi setBotInvite (đã có record hôm nay), user access thêm các trang khác của bot X cùng ngày<br>2. Vào màn「アクセス履歴」bot X | - ⏳ Pending QA (Q1): Giả định path access thấy đã có record của ngày → KHÔNG ghi thêm (tổng vẫn 1 dòng cho hôm nay)<br>- Cần BA xác nhận record từ setBotInvite có tính vào dedup-ngày không | Feature: Access History \| Category: Regression | | OK Step |
| TC-AH-021 | Dữ liệu lịch sử cũ (trước update) vẫn hiển thị bình thường | Positive | High | Bot X có sẵn các record access tạo trước khi deploy bản update. | 1. Vào màn「アクセス履歴」bot X<br>2. Xem các record cũ | - Record cũ hiển thị đầy đủ, đúng format, không lỗi<br>- Không bị thay đổi/mất sau khi deploy logic mới | Feature: Access History \| Category: Regression | | OK Step |
| TC-AH-024 | Login mới chưa chọn bot → chọn bot A ghi history (giải tỏa Q4) | Positive | High | User login mới, chưa có bot context (chưa từng chọn / không giữ selected bot). | 1. Login mới vào hệ thống<br>2. Login thành công → hệ thống hiển thị màn chọn bot<br>3. Chọn bot A | - Lịch sử truy cập hôm nay được ghi vào màn「ログイン履歴」(アクセス履歴) của bot A<br>- DB user_access_bot: 1 dòng login-history (user, bot A, hôm nay)<br>- DB user_selected_bot: bot đã chọn = bot A | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |
| TC-AH-025 | Đăng nhập từ màn Admin owner, chưa chọn bot → chọn bot A | Positive | High | Vào qua màn đăng nhập Admin, chưa có bot context. | 1. Đăng nhập từ màn Admin<br>2. Login thành công → màn chọn bot<br>3. Chọn bot A | - Lịch sử hôm nay ghi cho bot A trong màn「ログイン履歴」<br>- DB user_access_bot: 1 dòng (user, bot A, hôm nay)<br>- user_selected_bot: bot đã chọn = bot A | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |
| TC-AH-026 | Đăng nhập từ màn Admin owner, đã chọn bot trước → vào overview | Positive | Medium | Vào qua màn Admin, user đã có bot A context từ trước. | 1. Đăng nhập từ màn Admin<br>2. Vào thẳng màn overview của bot A (đã chọn từ trước) | - Lịch sử hôm nay ghi cho bot A<br>- DB user_access_bot: 1 dòng (user, bot A, hôm nay)<br>- user_selected_bot: bot A | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |
| TC-AH-027 | Đổi bot qua HEADER select (A→B) ghi history bot B | Positive | High | User đang ở bot A, có quyền bot B. | 1. Click select bot ở header<br>2. Chọn sang bot B | - Lịch sử hôm nay ghi cho bot B trong「ログイン履歴」<br>- DB user_access_bot: 1 dòng (user, bot B, hôm nay)<br>- user_selected_bot: chuyển sang bot B | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |
| TC-AH-028 | Đổi bot liên tiếp B→C ghi đúng bot đích | Edge Case | Medium | User vừa chọn bot B (đã có history bot B hôm nay). | 1. Từ bot B, đổi tiếp sang bot C (qua header)<br>2. Vào màn「ログイン履歴」của bot C | - Lịch sử hôm nay ghi cho bot C (đúng bot đích)<br>- bot B vẫn giữ history riêng của nó<br>- DB user_access_bot: thêm 1 dòng (user, bot C, hôm nay)<br>- user_selected_bot: bot C | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |
| TC-AH-029 | Chọn bot ở màn admin/home (A→B) ghi history bot B | Positive | Medium | User ở màn admin/home. | 1. Ở màn admin/home, dùng select bot<br>2. Chọn sang bot B | - Lịch sử hôm nay ghi cho bot B<br>- DB user_access_bot: 1 dòng (user, bot B, hôm nay)<br>- user_selected_bot: bot B | Feature: Access History \| Category: Login & Bot-Selection Entry Points | | OK Step |

### Chú thích cột

- **Type**: giữ nguyên giá trị từ Sheet (`Positive` / `Edge Case` / ...).
- **Output note**: chứa `Feature` + `Category` từ Sheet gốc (2 cột này không có chỗ trong template 10 cột).
- **Assignee**: Sheet gốc không có cột Assignee → để trống.
- **Status**: giữ nguyên giá trị fetch từ Sheet (`OK Step` / `NG` / `Not test`).

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`).

---

## Member tự check trước khi submit

<member điền sau khi review>

<!-- Source: fetched từ Redmine #38003 Link TCs, range A23:J32 tab "[AI] TCs_37743" lúc 2026-06-22 11:00. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
<!-- ⚠️ Lưu ý: MCP google-sheets không expose sheetId nên KHÔNG map trực tiếp được gid=2004892297 → tên tab. Tab "[AI] TCs_37743" được suy luận vì rows 23-32 khớp đúng "Line 23 ~ 32" trong Redmine VÀ nội dung là TC màn lịch sử access bot (đúng màn của task #38003). Tester verify lại đúng tab trước khi review. -->
