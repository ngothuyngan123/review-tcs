<!-- sync-target: https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=10976066 -->
# 04 — Test Cases (fetched từ Redmine Link TCs)

> **Source**: Fetched từ Google Sheet tab `[AI]TCs_UI` (gid=10976066) lúc 2026-05-15, theo Redmine #36437 chỉ định Line 132~133, 163~165.
> **TCs READ-ONLY** — KHÔNG sửa expected/title của TCs cũ này dù bug fix đổi behavior. Đây là baseline để Leader đánh giá coverage.
> **Lưu ý format sheet**: Sheet `[AI]TCs_UI` dùng cấu trúc phân cấp (parent row có Feature/Category, child row inherit từ parent → các cell phía trên có thể trống). Đọc kèm context của parent row khi review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester | `<member điền sau khi review>` |
| Ngày viết | `<member điền>` |
| Version | `<member điền>` |
| Link Sheet gốc | https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=10976066 |

## TC List

| TC ID | Feature | Category | Scenario | Type | Priority | Precondition | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|---|---|---|
| (row 132) | | | Check khi log out -> log in lại | không bật xác thực 2 lớp | | | | Hiển thị màn list chưa select bot<br>admin/pre-select-bot | OK |
| (row 133) | | | | bật xác thực 2 lớp | | | | | OK |
| (row 163) | | | | | | Nếu đang sử dụng gói pro | | Hover hiển thị tooltip プロプランのため、これ以上のアップグレードはできません | OK |
| (row 164) | | | | | | Nếu đang dùng gói free/standard | | Cho phép upgrade plan | OK |
| (row 165) | | | Check khi log out -> log in lại | không bật xác thực 2 lớp | | | | Hiển thị admin/home user đã chọn | OK |

## ⚠️ Cảnh báo dành cho Leader / Reviewer

1. **Row 132 và row 165 có Scenario giống nhau** ("Check khi log out -> log in lại") + **cùng "không bật xác thực 2 lớp"** nhưng **Expected khác nhau**:
   - Row 132 → "Hiển thị màn list chưa select bot admin/pre-select-bot" (chưa chọn bot)
   - Row 165 → "Hiển thị admin/home user đã chọn" (đã chọn bot)
   - Khả năng cao là 2 case kiểm tra 2 context khác nhau (trước/sau khi đã chọn bot). Leader verify lại với QA viết sheet.

2. **Row 133 (Expected trống)** — case "bật xác thực 2 lớp + chưa chọn bot" hiện không có expected. **Đây có thể là gap của bộ TC gốc** vì:
   - Bug #36437 chính là về flow "bật 2 lớp + đã chọn bot trước" → cần thêm 1 TC verify case "2 lớp + đã chọn bot" trả về admin/home đúng bot.
   - Hiện row 133 chỉ test "2 lớp + chưa chọn bot" — không cover bug.

3. **Row 163, 164** liên quan `BTN アップグレード` (upgrade plan button), **không trực tiếp liên quan login/2FA**. Có thể là regression smoke test trên admin/home (post-login). Leader xem có cần giữ trong scope review không.

## Member tự check

- [ ] Coverage check: TCs trên có cover được bug #36437 (logout/login với 2FA + đã chọn bot trước) chưa?
- [ ] Base checklist LME: cần verify sau khi đọc framework/checklist-lme.md.

<!-- Source: fetched từ Redmine #36437 Link TCs, tab "[AI]TCs_UI" gid=10976066, rows 132-133 và 163-165 (theo Dev chỉ định "Line 132~133, 163~165"). Fetch time: 2026-05-15. -->
