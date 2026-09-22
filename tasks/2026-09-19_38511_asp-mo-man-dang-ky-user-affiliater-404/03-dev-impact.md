# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #38511 — **Journal #131962 (AI LME Fix bug, 2026-08-21)**. Description ticket không có section "Đánh giá ảnh hưởng"; nội dung lấy từ báo cáo AI auto-fixbug.
> ⚠️ Đánh giá do **AI auto-fixbug** viết, không phải Dev người. Mục VERIFY chỉ ở mức **lint** — chưa có bằng chứng chạy thật sau fix.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) · Assignee Redmine: Đỗ Quyên |
| Commit / Pull Request | commit `c31b07792a` (repo `sns-line`) — <chưa có link PR> |
| Branch | `ai_fixbug_38511` (gốc `release_step_20260805`) · release: `release_step_20260827` |
| Ngày submit đánh giá | 2026-08-21 |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn đăng ký affiliater (/affiliate/{ma}/regist) còn một bước kiểm tra thừa: chỉ chấp nhận chủ tài khoản thuộc loại tài khoản khách thường (role 0 hoặc 1). User owner chọn ở màn quản lý ASP là chủ sở hữu bot, có thể thuộc loại khác (quản trị nội bộ -1 hoặc nhân viên 2) nên trượt kiểm tra và bị chuyển sang trang 404. Màn đăng nhập, màn quên mật khẩu và API tạo tài khoản affiliater đều không giới hạn loại tài khoản, nên đây là guard cũ còn sót lại chứ không phải quy tắc nghiệp vụ.

## 2. Cách fix

Bỏ điều kiện lọc theo loại tài khoản (role 0/1) trong bước kiểm tra chủ tài khoản của màn đăng ký affiliater, chỉ còn kiểm tra tài khoản có tồn tại — mọi user owner chọn được ở màn quản lý ASP đều mở được màn đăng ký, đồng bộ với màn đăng nhập và API tạo tài khoản affiliater vốn không giới hạn loại tài khoản. Quét tương tự: không có chỗ nào khác dùng lại bước kiểm tra này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AffiliateController::regist` (app/Http/Controllers/Aff/AffiliateController.php) | Sửa — bỏ lọc role 0/1 | Màn đăng ký affiliater, nơi có bước kiểm tra gây 404 |
| 2 | `AffiliateController::createNewAff` (app/Http/Controllers/Aff/AffiliateController.php) | Không | API tạo affiliater, không giới hạn loại tài khoản |
| 3 | `AffiliaterController::getLoginV2` / `getResetPassV2` (app/Http/Controllers/Affiliate/AffiliaterController.php) | Không | Màn đăng nhập + quên mật khẩu, không giới hạn loại tài khoản |
| 4 | `AffiliateManagementController::index` (app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php) | Không | Màn quản lý ASP dựng danh sách user owner + URL hướng dẫn affiliater |
| 5 | `member_add.blade.php` (resources/views/admin/aff/member_add.blade.php) | Không | Màn đăng ký, tự hiện thông báo tạm dừng khi chủ tài khoản chưa bật đăng ký mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev ghi mục 4.1 dạng "File thay đổi": chỉ `app/Http/Controllers/Aff/AffiliateController.php`. Diff: 1 file, 2 thêm 3 bớt.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `AffiliateController::regist` — bước kiểm tra chủ tài khoản | app/Http/Controllers/Aff/AffiliateController.php | Direct | Bỏ điều kiện role 0/1, giữ kiểm tra tài khoản tồn tại |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Chỉ sửa điều kiện kiểm tra khi hiển thị màn, không đọc/ghi thêm dữ liệu. Không cần recover data. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Affiliate Register (affiliate-register) — màn đăng ký affiliater mở được cho mọi chủ tài khoản ASP thay vì chỉ tài khoản khách thường | F1 | <Dev không ghi> |
| T2 | ASP Management — URL hướng dẫn affiliater copy từ màn quản lý ASP dùng được với mọi user owner chọn trong danh sách | F1 | <Dev không ghi> |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
