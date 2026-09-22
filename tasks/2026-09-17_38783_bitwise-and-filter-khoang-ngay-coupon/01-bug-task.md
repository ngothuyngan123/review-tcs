# 01 — Bug Task từ khách hàng

> Auto-filled `2026-09-17 by /new-task` từ Redmine #38783 (REST API). Metadata Redmine (ngày báo, người báo, priority, URL) tra thẳng trên ticket.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38783 — Dùng bitwise & thay vì logical && trong filter khoảng ngày (filter không chạy đúng) [C1]` |
| Module / Màn hình | Coupon Code Issue (FS-015) — màn quản lý mã coupon `/admin/coupon-management`, **tab 「使用済み」** (bộ lọc khoảng ngày theo 発行日 / 使用日). Hàm `ajaxCouponManagement` — `app/Http/Controllers/Admin/UserController.php:9468` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine đã viết bằng tiếng Việt — chép nguyên văn, không diễn giải lại. -->

- `app/Http/Controllers/Admin/UserController.php:9468`
- `ajaxCouponManagement` dùng điều kiện `$type_filter == 0 && $start_date & $end_date`. Toán tử `&` (bitwise) ưu tiên cao hơn `&&` nên thực chất là `$type_filter==0 && ($start_date & $end_date)` — bitwise-AND 2 chuỗi ngày (cast về 0) → filter khoảng ngày gần như không kích hoạt đúng. Lặp lại cho `$type_filter==1`. Còn để lại `// DB::rollback();` (dead code).
- **Đề xuất:** Đổi thành `$start_date && $end_date`; xoá comment `DB::rollback` thừa.

## Steps to reproduce

<!-- Redmine #38783 KHÔNG có Section "Tái hiện bug" — ticket là bug do AI tự detect qua đọc code, không phải khách hàng báo. -->

## Expected result

<!-- Trống — xem mục trên. -->

## Actual result

<!-- Trống — xem mục trên. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38783: attachments = 0. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket thuộc tracker **`Bug tự detect`** (AI đọc code phát hiện), không có Steps/Expected/Actual do khách hàng báo. Root cause đã được xác định ở tầng code (precedence toán tử PHP). TCs nên tập trung **verify cách fix + regression impact** của màn quản lý mã coupon.
- **Tần suất lỗi:** không phải lỗi xác suất. Với `$start_date` / `$end_date` là chuỗi ngày dạng `"2026-03-01"` thì `(string) & (string)` cho kết quả chuỗi bitwise, PHP ép về falsy/truthy không như ý định → điều kiện `.when()` kích hoạt sai. Cần Leader chốt **hành vi trước fix** (filter có chạy hay không, chạy sai thế nào) để viết expected đối chứng regression.
- **Môi trường phát hiện:** không ghi trong ticket (phát hiện qua đọc source, nhánh gốc `release_step_20260623`).
- **Account test:** cần **System Admin** để vào `/admin/coupon-management` (theo precondition TC trên Studio: role `-1`, đăng nhập qua `/login-v2`).
- **Status ticket hiện tại:** `Fix done - Đợi test` · Priority `High` · Assignee `Kim Cúc`.

## Journal / note từ Redmine (nguyên văn)

> Redmine #38783 có **2 journal** (#125998, #125999) — **nội dung trùng nhau hoàn toàn** (cùng báo cáo AI Auto-fixbug, cùng thời điểm 2026-07-14, cùng branch/commit). Chép 1 bản bên dưới.

**Journal #125998 — AI LME Fix bug — 2026-07-14:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Trong hàm ajaxCouponManagement (màn quản lý phát hành mã coupon), điều kiện lọc theo khoảng ngày dùng nhầm toán tử & (bitwise AND) thay vì && (logical AND). Vì & có độ ưu tiên cao hơn && nên PHP hiểu là $type_filter==0 && ($start_date & $end_date); hai chuỗi ngày bị ép về số nguyên rồi AND theo bit → kết quả sai, khiến bộ lọc khoảng ngày gần như không kích hoạt đúng. Lặp lại cho cả nhánh $type_filter==1. Ngoài ra còn sót dòng comment dead code // DB::rollback(); trong khối catch.

■ 2. CÁCH FIX
Đổi toán tử & (bitwise) thành && (logical) ở 2 điều kiện .when() lọc khoảng ngày trong ajaxCouponManagement (nhánh type_filter==0 lọc theo created_at và type_filter==1 lọc theo datetime_use), để điều kiện chỉ kích hoạt khi cả start_date và end_date đều có giá trị. Đồng thời xoá dòng comment dead code // DB::rollback(); trong khối catch của hàm này. Quét yokoten toàn app không thấy chỗ nào khác dùng cùng pattern & sai.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ajaxCouponManagement (app/Http/Controllers/Admin/UserController.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/UserController.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ sửa logic điều kiện query, không đổi schema/dữ liệu
 • 4.3 Tính năng liên quan:
   - Coupon Code Issue (FS-015) — sửa bộ lọc theo khoảng ngày trong màn quản lý/danh sách mã coupon để lọc đúng theo ngày tạo và ngày sử dụng

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/UserController.php: No syntax errors detected
   Bằng chứng: Precedence PHP: & cao hơn && nên $a && $b & $c == $a && ($b & $c); fix đổi thành $a && $b && $c như ý định ban đầu

■ TỰ REVIEW (AI)
Fix tối thiểu đúng root cause: đổi & → && ở 2 điều kiện lọc khoảng ngày + xoá dead code. Không ảnh hưởng logic khác trong hàm.
 • Rủi ro / lưu ý khi test:
   - Không có rủi ro đáng kể — chỉ sửa toán tử điều kiện, hành vi lọc trở về đúng thiết kế

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38783 (nhánh gốc release_step_20260623, commit 17792c55ff, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 2 phút 33 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=995da4bb-99eb-4758-b09c-cf6c4349da3f
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38783
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #125999 — AI LME Fix bug — 2026-07-14:** trùng hoàn toàn nội dung Journal #125998 (post lặp 2 lần).
