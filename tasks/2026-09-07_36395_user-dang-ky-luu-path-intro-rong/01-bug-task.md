# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36395 — [12-05-2026] Một số user khi đăng ký thì đang bị lưu path_intro = ''` |
| Module / Màn hình | Đăng ký tài khoản LME — màn `register-v3` (`resources/views/auth/auth-v3/register-v3.blade.php`) + `AuthController`; cột `users.path_intro` (đường dẫn / nguồn giới thiệu) |

## Mô tả bug (bản dịch tiếng Việt)

Nội dung ticket (nguyên văn — description Redmine vốn đã là tiếng Việt):

> Check xem tại sao lại lưu rỗng?
> Expect: Mọi user đăng ký phải có path_intro

Câu SQL khoanh vùng ca lỗi trong ticket:

```sql
SELECT * FROM `users`
WHERE admin_id = 1
  AND created_at LIKE '2026-05%'
  AND (path_intro IS NULL OR path_intro = '')
```

→ Một số tài khoản đăng ký trong tháng 2026-05 có `users.path_intro` rỗng (`''`) hoặc `NULL`, trong khi kỳ vọng là **mọi** user đăng ký đều phải có `path_intro`.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — bug được phát hiện bằng truy vấn SQL trên dữ liệu thật, không có kịch bản thao tác do người báo cung cấp. -->

*(trống — xem "Ghi chú thêm của Leader")*

## Expected result

- Mọi user đăng ký phải có `path_intro` (nguyên văn dòng `Expect:` trong ticket).

## Actual result

- Một số user khi đăng ký bị lưu `path_intro = ''` (theo tiêu đề ticket + kết quả câu SQL ở trên).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `path_intro.png` — https://redmine.watermelon.vn/attachments/download/25718/path_intro.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (không có Steps / Expected / Actual do người báo viết) — root cause đã được Dev (hệ thống Auto-fixbug LME) confirm qua đánh giá ảnh hưởng (file [03-dev-impact.md](03-dev-impact.md)). TCs nên tập trung verify **cách fix + regression impact**.
- **Trạng thái ticket**: `Fix done - Đợi test` · tracker `Bug tự detect` · assignee hiện tại: Ngọc Ánh (trước đó: Ngô Thúy Ngần).
- **Môi trường phát hiện**: dữ liệu thật (`admin_id = 1`, `created_at` tháng 2026-05) → phát hiện trên **production data**, không phải dev/staging.
- **Tần suất**: KHÔNG phải 100% — ticket ghi "một số user". Theo Dev, lỗi xảy ra khi người dùng **vào thẳng trang đăng ký** (URL không kèm tham số `path_intro`, trình duyệt không có cookie), hoặc khi **link trong mail xác thực thiếu tham số**.
- **Nhánh fix để checkout**: repo `sns-line`, branch `ai_fixbug_36395` (nhánh gốc `release_step_20260805`, commit `ed88830f5c`, 3 file) — đã push.
- ⚠️ **Dev chỉ verify ở mức `lint`** — MySQL dev không kết nối được trong container (Connection refused) nên **chưa đối chiếu dữ liệu thật**; kết luận dựa trên đọc code. → Test bắt buộc phải tự verify giá trị ghi xuống DB.
- ⚠️ **Còn tồn dư dữ liệu cũ**: tài khoản đăng ký **trước** bản fix vẫn giữ `path_intro` rỗng. Dev đề xuất bù từ `user_temporary.path_intro` theo email nhưng **script bù chưa được viết** — cần human quyết định. Test cần phân biệt rõ "dữ liệu cũ còn rỗng" (ngoài phạm vi fix) với "tài khoản mới vẫn rỗng" (fix hỏng).
- **Quy ước hiển thị liên quan**: `PaymentController::resolveRegistrationRoute` coi `path_intro` rỗng **hoặc bằng `APP_URL`** là đăng ký trực tiếp (通常登録 — đăng ký thông thường) → sau fix, giá trị "không có nguồn giới thiệu" được lưu là `APP_URL` chứ không phải chuỗi rỗng.
- **Dashboard fixbug**: https://dashboard.melonglobal.net/fixbug-lme/?id=36395

## Journal / note từ Redmine (nguyên văn)

**Journal #133361 — AI LME Fix bug — 2026-08-28:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn đăng ký bản mới (register-v3) bỏ mất bước lấy đường dẫn trang trước (referer) làm nguồn giới thiệu mà bản cũ vẫn có, nên khi người dùng vào thẳng trang đăng ký (URL không kèm tham số path_intro, trình duyệt không có cookie) thì giá trị này rỗng ngay từ bước gửi mail xác thực. Ở bước tạo tài khoản, server lấy thẳng giá trị màn hình gửi lên rồi giải mã: giá trị null/rỗng biến thành chuỗi rỗng và được ghi vào cột path_intro của bảng người dùng. Ngoài ra server không dùng lại giá trị đã lưu sẵn ở bảng đăng ký tạm (lưu lúc gửi mail), nên nếu link trong mail thiếu tham số thì mất luôn nguồn giới thiệu đã biết.

■ 2. CÁCH FIX
Sửa theo AI review vòng 2: lệnh đếm lượt đăng ký theo đường dẫn giới thiệu (countPathIntro, AuthController dòng ~1067) vẫn nhận giá trị thô do FE gửi lên thay vì giá trị đã được xử lý. Vòng trước đã chuyển từ ghi đè lên request sang dùng biến cục bộ nhưng quên cập nhật lời gọi này, khiến số đếm lệch với chính giá trị vừa ghi vào bảng người dùng: đăng ký từ mobile thì đếm theo đường dẫn gốc trong khi bản ghi lưu đường dẫn bản mobile; còn đúng trường hợp ticket này sửa (link trong mail thiếu tham số, giá trị lấy từ bản ghi đăng ký tạm) thì đếm nhận rỗng nên số lượt không tăng, làm thống kê cho super admin bị hụt âm thầm. Nay truyền chính biến đã xử lý vào lệnh đếm, giữ nguyên rỗng khi đăng ký trực tiếp để không khớp nhầm bản ghi đường dẫn nào. Chỉ sửa đúng lỗi bắt buộc, không đụng cảnh báo.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
AuthController::validateRegisterV2 (app/Http/Controllers/AuthController.php) — nơi ghi users.path_intro của luồng đăng ký đang chạy
AuthController::resolvePathIntro (app/Http/Controllers/AuthController.php) — hàm mới xác định nguồn giới thiệu
AuthController::sendMail (app/Http/Controllers/AuthController.php) — lưu path_intro vào bảng đăng ký tạm ở bước gửi mail
AuthController::registerUserV3 / registerUserAff (app/Http/Controllers/AuthController.php) — truyền pathIntro + referer ra view
AuthController::redirectRegist (app/Http/Controllers/AuthController.php) — mở form đăng ký từ link trong mail
AuthController::countPathIntro (app/Http/Controllers/AuthController.php) — đếm lượt theo trang giới thiệu (giữ nguyên)
trackReferer / sendEmail / register (resources/views/auth/auth-v3/register-v3.blade.php) — màn đăng ký đang dùng
PaymentController::resolveRegistrationRoute (app/Http/Controllers/Admin/PaymentController.php) — quy ước hiển thị 通常登録 khi rỗng hoặc bằng URL hệ thống

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/AuthController.php
   - resources/views/auth/auth-v3/register-v3.blade.php
 • 4.2 Data ảnh hưởng:
   - users.path_intro — từ nay tài khoản đăng ký mới luôn có giá trị (không còn chuỗi rỗng); tài khoản cũ đang rỗng vẫn giữ nguyên
   - user_temporary.path_intro — được dùng lại làm nguồn dự phòng, không thay đổi cách ghi
   - path_intro_data.count_user — không đổi (vẫn đếm theo giá trị màn hình gửi lên như cũ)
 • 4.3 Tính năng liên quan:
   - User Registration (outside glossary) — luồng đăng ký tài khoản LME mới: ghi đúng đường dẫn giới thiệu thay vì chuỗi rỗng
   - User / Account List (FS-003) — cột đường dẫn giới thiệu của tài khoản trong danh sách quản trị hiển thị đúng nguồn
   - Payment History (FS-009) — cột phân loại nguồn đăng ký trong lịch sử thanh toán (通常登録 hay tên trang giới thiệu)
   - Affiliate Register (outside glossary) — đăng ký qua link giới thiệu cũng đi chung màn register-v3 nên hưởng cùng thay đổi

■ 5. RECOVER DATA
   ⚠ CÓ — Tài khoản đã đăng ký trước bản fix vẫn đang có path_intro rỗng. Có thể bù một phần: với các tài khoản này, đối chiếu email sang bảng đăng ký tạm (user_temporary.path_intro) — nơi còn giữ nguồn giới thiệu lúc gửi mail xác thực — để điền lại; trường hợp bảng tạm cũng rỗng thì coi là đăng ký trực tiếp (điền URL hệ thống) hoặc để nguyên vì phía hiển thị đã coi rỗng là 通常登録. Cần human quyết định có chạy bù hay không, script bù chưa được viết trong ticket này. (phạm vi: users.path_intro của các tài khoản có path_intro rỗng/NULL (theo câu SQL trong ticket: admin_id = 1, created_at trong tháng 2026-05 trở về trước))

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/AuthController.php: No syntax errors detected; Compile blade register-v3 bằng Illuminate BladeCompiler rồi php -l: No syntax errors detected; Chạy thử logic chọn nguồn giới thiệu với 6 trường hợp (có tham số / chỉ có bản ghi tạm / rỗng cả hai / giá trị '1' / chuỗi toàn khoảng trắng / null): mọi trường hợp đều ra giá trị khác rỗng
   Bằng chứng: MySQL dev (host.docker.internal:3306) không kết nối được trong container (Connection refused) nên không đối chiếu được dữ liệu thật; kết luận dựa trên đọc code luồng đăng ký; So sánh 2 màn: resources/views/auth/register_user_v2.blade.php dòng 1442-1444 có nhánh lấy referer khi thiếu path_intro, còn resources/views/auth/auth-v3/register-v3.blade.php (màn đang dùng) không có; Quy ước hiển thị: PaymentController::resolveRegistrationRoute coi path_intro rỗng hoặc bằng APP_URL là đăng ký trực tiếp (通常登録)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_36395 (nhánh gốc release_step_20260805, commit ed88830f5c, 3 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 49 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=5cdac3ec-be35-450f-aec7-c42eba270314
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=36395
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
