# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: **Journal #133361 (2026-08-28) của hệ thống Auto-fixbug LME** — Redmine description KHÔNG có section "Đánh giá ảnh hưởng" riêng. Nội dung dưới đây trích nguyên văn từ journal đó.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee ticket hiện tại: Ngọc Ánh |
| Commit / Pull Request | commit `ed88830f5c` (repo `sns-line`, 3 file) — không có link PR. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=36395 |
| Branch | `ai_fixbug_36395` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-28` |
| Auto-filled | `2026-09-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #133361 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn mục ■ 1 của Dev:

Màn đăng ký bản mới (register-v3) bỏ mất bước lấy đường dẫn trang trước (referer) làm nguồn giới thiệu mà bản cũ vẫn có, nên khi người dùng vào thẳng trang đăng ký (URL không kèm tham số `path_intro`, trình duyệt không có cookie) thì giá trị này rỗng ngay từ bước gửi mail xác thực. Ở bước tạo tài khoản, server lấy thẳng giá trị màn hình gửi lên rồi giải mã: giá trị null/rỗng biến thành chuỗi rỗng và được ghi vào cột `path_intro` của bảng người dùng. Ngoài ra server không dùng lại giá trị đã lưu sẵn ở bảng đăng ký tạm (lưu lúc gửi mail), nên nếu link trong mail thiếu tham số thì mất luôn nguồn giới thiệu đã biết.

## 2. Cách fix

> Nguyên văn mục ■ 2 của Dev (đây là mô tả của **vòng review thứ 2**):

Sửa theo AI review vòng 2: lệnh đếm lượt đăng ký theo đường dẫn giới thiệu (`countPathIntro`, `AuthController` dòng ~1067) vẫn nhận giá trị thô do FE gửi lên thay vì giá trị đã được xử lý. Vòng trước đã chuyển từ ghi đè lên request sang dùng biến cục bộ nhưng quên cập nhật lời gọi này, khiến số đếm lệch với chính giá trị vừa ghi vào bảng người dùng: đăng ký từ mobile thì đếm theo đường dẫn gốc trong khi bản ghi lưu đường dẫn bản mobile; còn đúng trường hợp ticket này sửa (link trong mail thiếu tham số, giá trị lấy từ bản ghi đăng ký tạm) thì đếm nhận rỗng nên số lượt không tăng, làm thống kê cho super admin bị hụt âm thầm. Nay truyền chính biến đã xử lý vào lệnh đếm, giữ nguyên rỗng khi đăng ký trực tiếp để không khớp nhầm bản ghi đường dẫn nào. Chỉ sửa đúng lỗi bắt buộc, không đụng cảnh báo.

**Tóm tắt hành vi mới (theo `requirements` REQ-001/REQ-002 trên Studio task #259):**

- Thứ tự ưu tiên xác định nguồn giới thiệu: **tham số URL → cookie `path_intro_lme` / `path_intro` → referer (trang trước) → giá trị đã lưu ở `user_temporary`**.
- Giá trị được URL-decode + trim trước khi lưu. Các giá trị suy biến (`''`, chỉ khoảng trắng, chuỗi quy ước `'1'`) coi như **không có nguồn**.
- Không xác định được nguồn nào → lưu **`APP_URL` của môi trường đang chạy** (không còn lưu chuỗi rỗng).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục ■ 3 của Dev, convert sang bảng.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AuthController::validateRegisterV2` — `app/Http/Controllers/AuthController.php` | Có sửa | Nơi ghi `users.path_intro` của luồng đăng ký đang chạy |
| 2 | `AuthController::resolvePathIntro` — `app/Http/Controllers/AuthController.php` | **Hàm mới** | Xác định nguồn giới thiệu theo thứ tự ưu tiên |
| 3 | `AuthController::sendMail` — `app/Http/Controllers/AuthController.php` | Có sửa | Lưu `path_intro` vào bảng đăng ký tạm ở bước gửi mail |
| 4 | `AuthController::registerUserV3` / `registerUserAff` — `app/Http/Controllers/AuthController.php` | Có sửa | Truyền `pathIntro` + `referer` ra view |
| 5 | `AuthController::redirectRegist` — `app/Http/Controllers/AuthController.php` | Có check | Mở form đăng ký từ link trong mail |
| 6 | `AuthController::countPathIntro` — `app/Http/Controllers/AuthController.php` | Dev ghi "giữ nguyên" (⚠️ xem ghi chú bên dưới) | Đếm lượt theo trang giới thiệu |
| 7 | `trackReferer` / `sendEmail` / `register` — `resources/views/auth/auth-v3/register-v3.blade.php` | Có sửa | Màn đăng ký đang dùng |
| 8 | `PaymentController::resolveRegistrationRoute` — `app/Http/Controllers/Admin/PaymentController.php` | Có check | Quy ước hiển thị 通常登録 khi `path_intro` rỗng hoặc bằng URL hệ thống |

⚠️ **Mâu thuẫn nội tại trong báo cáo Dev — Leader cần xác nhận với Dev trước khi giao TC:**
Mục 3 ghi `countPathIntro` "**giữ nguyên**" và mục 4.2 ghi `path_intro_data.count_user` "**không đổi** (vẫn đếm theo giá trị màn hình gửi lên như cũ)", nhưng mục 2 (cách fix) lại nói rõ **"Nay truyền chính biến đã xử lý vào lệnh đếm"** — tức **lời gọi `countPathIntro` ĐÃ bị đổi tham số**. Hai chỗ này ngược nhau → coi `path_intro_data.count_user` là **CÓ thay đổi hành vi** (đã ghi thành `D3` ở mục 4.2) và bắt buộc test số đếm, không tin dòng "không đổi".

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Mục ■ 4.1 của Dev chỉ liệt kê **file thay đổi**, không liệt kê function. Bảng dưới giữ nguyên 2 file Dev ghi (`F1`, `F2`) và bổ sung các function từ mục ■ 3 để dùng làm chiều coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | *(file thay đổi — Dev ghi ở 4.1)* | `app/Http/Controllers/AuthController.php` | Direct | 1 trong 2 file được sửa |
| F2 | *(file thay đổi — Dev ghi ở 4.1)* | `resources/views/auth/auth-v3/register-v3.blade.php` | Direct | 1 trong 2 file được sửa |
| F3 | `AuthController::resolvePathIntro` | `AuthController.php` | Direct (**hàm mới**) | Trung tâm của fix — thứ tự ưu tiên URL → cookie → referer → `user_temporary` |
| F4 | `AuthController::validateRegisterV2` | `AuthController.php` | Direct | Nơi ghi `users.path_intro` |
| F5 | `AuthController::sendMail` | `AuthController.php` | Direct | Ghi `path_intro` vào `user_temporary` ở bước gửi mail |
| F6 | `AuthController::registerUserV3` / `registerUserAff` | `AuthController.php` | Direct | Truyền `pathIntro` + `referer` ra view; `registerUserAff` = đăng ký qua link giới thiệu |
| F7 | `AuthController::redirectRegist` | `AuthController.php` | Indirect | Mở form đăng ký từ link mail (case link thiếu tham số) |
| F8 | `AuthController::countPathIntro` | `AuthController.php` | Direct (⚠️ Dev ghi "giữ nguyên" nhưng mục 2 nói đã đổi tham số truyền vào) | Đếm lượt theo trang giới thiệu |
| F9 | `trackReferer` / `sendEmail` / `register` (JS trong blade) | `register-v3.blade.php` | Direct | Màn đăng ký đang dùng |
| F10 | `PaymentController::resolveRegistrationRoute` | `Admin/PaymentController.php` | Indirect (không sửa) | Đọc `path_intro` để phân loại 通常登録 / referral |
| F11 | `UserController` — xoá tài khoản (giảm `count_user`) | `Admin/UserController.php` | Indirect (không sửa — suy từ REQ-005 Studio) | Bất đối xứng: tài khoản lưu `APP_URL` chưa từng được cộng nhưng vẫn có thể bị trừ |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục ■ 4.2 của Dev.

| # | Data (table.column) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `users.path_intro` | UPDATE (thay đổi giá trị ghi khi CREATE tài khoản) | Từ nay tài khoản đăng ký mới **luôn có giá trị** (không còn chuỗi rỗng); **tài khoản cũ đang rỗng vẫn giữ nguyên** |
| D2 | `user_temporary.path_intro` | CREATE / đọc lại | Được dùng lại làm **nguồn dự phòng**; Dev ghi "không thay đổi cách ghi" (nhưng REQ-003 Studio nói trước fix giá trị bị **bỏ qua âm thầm** ở bước gửi mail → Leader verify lại) |
| D3 | `path_intro_data.count_user` | UPDATE | Dev ghi "không đổi", nhưng mục 2 nói đã truyền biến đã xử lý vào `countPathIntro` → ⚠️ **coi là CÓ đổi**, phải test số đếm (cộng đúng / không cộng nhầm / mobile `sp.html` / khớp một phần) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục ■ 4.3 của Dev.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **User Registration** (ngoài glossary) — luồng đăng ký tài khoản LME mới | F1–F9, D1, D2 | **High** — ghi đúng đường dẫn giới thiệu thay vì chuỗi rỗng |
| T2 | **User / Account List (FS-003)** — cột đường dẫn giới thiệu trong danh sách quản trị | D1, F10 | **Medium** — hiển thị đúng nguồn |
| T3 | **Payment History (FS-009)** — cột phân loại nguồn đăng ký | D1, F10 | **Medium** — 通常登録 hay tên trang giới thiệu |
| T4 | **Affiliate Register** (ngoài glossary) — đăng ký qua link giới thiệu | F6 | **High** — dùng chung màn `register-v3` nên hưởng cùng thay đổi; phải giữ đúng quan hệ người giới thiệu |
| T5 | *(bổ sung từ REQ-005/REQ-010/REQ-011 của Studio — Dev không ghi ở 4.3)* Xoá tài khoản (thống kê `count_user`) · màn đăng ký đời cũ `/register` · các trạng thái lỗi token của `register-v3` | F8, F11, D3 | **Medium** — đánh dấu để Leader quyết có đưa vào phạm vi test không |

---

## 5. Recover data (mục ■ 5 của Dev — nguyên văn)

⚠ **CÓ** — Tài khoản đã đăng ký trước bản fix vẫn đang có `path_intro` rỗng. Có thể bù một phần: với các tài khoản này, đối chiếu email sang bảng đăng ký tạm (`user_temporary.path_intro`) — nơi còn giữ nguồn giới thiệu lúc gửi mail xác thực — để điền lại; trường hợp bảng tạm cũng rỗng thì coi là đăng ký trực tiếp (điền URL hệ thống) hoặc để nguyên vì phía hiển thị đã coi rỗng là 通常登録. **Cần human quyết định có chạy bù hay không, script bù chưa được viết trong ticket này.**
Phạm vi: `users.path_intro` của các tài khoản có `path_intro` rỗng/NULL (theo câu SQL trong ticket: `admin_id = 1`, `created_at` trong tháng 2026-05 trở về trước).

## 6. Verify của Dev (mục ■ 6 — nguyên văn)

- **Mức: `lint`** (⚠️ KHÔNG có unit/integration test, KHÔNG đối chiếu dữ liệu thật).
- Lệnh: `php -l app/Http/Controllers/AuthController.php` → No syntax errors detected; compile blade `register-v3` bằng Illuminate BladeCompiler rồi `php -l` → No syntax errors detected; chạy thử logic chọn nguồn giới thiệu với **6 trường hợp** (có tham số / chỉ có bản ghi tạm / rỗng cả hai / giá trị `'1'` / chuỗi toàn khoảng trắng / null) → mọi trường hợp đều ra giá trị khác rỗng.
- Bằng chứng: **MySQL dev (`host.docker.internal:3306`) không kết nối được trong container (Connection refused) nên không đối chiếu được dữ liệu thật**; kết luận dựa trên đọc code luồng đăng ký. So sánh 2 màn: `resources/views/auth/register_user_v2.blade.php` dòng 1442-1444 có nhánh lấy referer khi thiếu `path_intro`, còn `resources/views/auth/auth-v3/register-v3.blade.php` (màn đang dùng) không có. Quy ước hiển thị: `PaymentController::resolveRegistrationRoute` coi `path_intro` rỗng hoặc bằng `APP_URL` là đăng ký trực tiếp (通常登録).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] ⚠️ **Đã hỏi Dev về mâu thuẫn `countPathIntro` / `path_intro_data.count_user`** (mục 2 nói đổi, mục 3 + 4.2 nói giữ nguyên)
- [ ] ⚠️ **Đã chốt hướng xử lý dữ liệu cũ còn rỗng** (mục 5 — có chạy script bù hay không)
