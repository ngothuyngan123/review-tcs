# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn**: Redmine #37845 **không có section "Đánh giá ảnh hưởng" trong description**. Toàn bộ nội dung dưới đây parse từ **Journal #133046 — "AI LME Fix bug" — 2026-08-26** (báo cáo tự động của hệ thống Auto-fixbug LME), không phải Dev người viết.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Auto-fixbug LME (AI)` — assignee ticket: Ngô Thúy Ngần |
| Commit / Pull Request | `commit 7fc394d0a1` (1 file changed, 29 insertions, 3 deletions) — không có link PR |
| Branch | `ai_fixbug_37845` (nhánh gốc `release_step_20260805`), repo `sns-line` — đã push |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-08 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #133046 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn lịch sử đăng nhập nhân viên (`/admin/access-histories`) nằm trong nhóm route **chỉ có middleware kiểm đăng nhập**, không đi qua cổng kiểm quyền tính năng.

- Màn này dựng danh sách tài khoản trong dropdown bằng hàm lấy **MỌI** tài khoản mà người dùng được mời làm nhân viên (không lọc theo quyền).
- Không kiểm tham số tài khoản (`bot_id`) truyền trên URL → nhân viên chưa được phân quyền vẫn mở được màn.
- Hai endpoint lấy lịch sử và xuất CSV cũng nhận thẳng id tài khoản từ request mà **không giới hạn phạm vi**; thậm chí **khi không truyền id thì trả về lịch sử của TẤT CẢ tài khoản**.

Bằng chứng Dev nêu:
- `routes/web.php:547` nằm trong group prefix `/admin` middleware `['admin_access','https_protocol','check_remember_token']` — **KHÔNG có `basic_access`** nên không qua cổng kiểm quyền tính năng.
- `public/js/admin/employees/access_histories.js`: `bot_id` lấy từ query string, không khớp danh sách thì **fallback `bots[0]`** — nên trước fix luôn hiện dữ liệu của 1 tài khoản nào đó.

## 2. Cách fix

1. Thêm **hàm dùng chung** lấy danh sách tài khoản được phép xem lịch sử đăng nhập = **tài khoản mình sở hữu + tài khoản được mời có quyền màn quản lý nhân viên** — cùng nguồn với dropdown của màn 「スタッフ管理」, thay cho hàm cũ lấy mọi tài khoản được mời.
2. Màn lịch sử đăng nhập **chuyển hướng về màn danh sách tài khoản kèm thông báo 「この権限は許可されていません。」** khi danh sách rỗng **hoặc** `bot_id` trên URL nằm ngoài phạm vi.
3. Hai endpoint lấy lịch sử và xuất CSV **bắt buộc có `bot_id`** và phải nằm trong phạm vi, ngược lại **trả 403**.
4. **Quét ngang**: 2 endpoint lấy danh sách nhân viên theo tài khoản của màn quản lý nhân viên **còn cùng lỗi thiếu kiểm phạm vi** — đã ghi lại **CHƯA SỬA** vì ngoài phạm vi ticket.

> ⚠️ Mức verify của Dev chỉ đạt **`lint`** (`php -l`: no syntax errors + `git diff --stat` đúng 1 file). **Không kiểm chứng được bằng dữ liệu runtime** — MySQL dev `host.docker.internal:3306` Connection refused.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `UserController::accessHistories` — `app/Http/Controllers/Admin/UserController.php` | **Đã sửa** — thêm guard redirect + thông báo khi danh sách rỗng / `bot_id` ngoài phạm vi | Điểm vào màn hình bị bypass |
| 2 | `UserController::getAccessHistories` — `app/Http/Controllers/Admin/UserController.php` | **Đã sửa** — bắt buộc `bot_id` + trong phạm vi, ngược lại 403 | Endpoint lấy lịch sử nhận thẳng id từ request |
| 3 | `UserController::exportCsvAccessHistory` — `app/Http/Controllers/Admin/UserController.php` | **Đã sửa** — bắt buộc `bot_id` + trong phạm vi, ngược lại 403 | Endpoint xuất CSV nhận thẳng id từ request |
| 4 | `UserController::getBotIdsCanViewAccessHistory` — `app/Http/Controllers/Admin/UserController.php` | **Hàm MỚI** — nguồn quyền dùng chung cho cả 3 điểm vào | Thay hàm cũ lấy mọi tài khoản được mời |
| 5 | `getListBotId` / `getListBotIdStaffManagement` — `app/Helpers/functions.php` | Không sửa — chuyển sang dùng `getListBotIdStaffManagement($adminId,'employeesManagement')` | Hàm cũ `getListBotId` không lọc theo quyền |
| 6 | `getRouteFromRoleAccess` / `getRouterBotInvite` / `checkBotHasPermission` — `app/Helpers/functions.php` | Không sửa — chỉ đọc | Chuỗi tính quyền phía dưới hàm mới |
| 7 | `StaffManagementController::getListBotOwnership` — `app/Http/Controllers/Admin/StaffManagementController.php` | Không sửa | Màn cha 「スタッフ管理」 — nguồn quyền tham chiếu để đồng bộ |
| 8 | `AdminAccess::handle` / `BasicAccess::handle` — `app/Http/Middleware/` | Không sửa | Cổng chặn quyền có sẵn — route này KHÔNG đi qua `basic_access` |
| 9 | `access_histories.js` — `mounted` / `loadItems` / `downloadCSV` — `public/js/admin/employees/access_histories.js` | Không sửa | FE lấy `bot_id` từ query string, fallback `bots[0]` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev **chỉ liệt kê FILE thay đổi** ở mục 4.1, không liệt kê function theo format `F1/F2/...`. Bảng dưới do `/new-task` map lại từ mục 3 — **tester verify lại trước khi dùng làm coverage**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `UserController::accessHistories` (màn hình `/admin/access-histories`) | `app/Http/Controllers/Admin/UserController.php` | Direct | Redirect + toast 「この権限は許可されていません。」 khi ngoài quyền |
| F2 | `UserController::getAccessHistories` (API `/admin/get-access-histories`) | `app/Http/Controllers/Admin/UserController.php` | Direct | Bắt buộc `bot_id` trong phạm vi, ngược lại **403** |
| F3 | `UserController::exportCsvAccessHistory` (API `/admin/export-csv-access-history`) | `app/Http/Controllers/Admin/UserController.php` | Direct | Bắt buộc `bot_id` trong phạm vi, ngược lại **403**, không sinh file |
| F4 | `UserController::getBotIdsCanViewAccessHistory` (**hàm mới, dùng chung 3 nơi**) | `app/Http/Controllers/Admin/UserController.php` | Direct | Nguồn quyền = bot sở hữu + bot được mời có quyền `employeesManagement` |
| F5 | `getListBotIdStaffManagement` | `app/Helpers/functions.php` | Indirect | Hàm dùng chung với màn cha 「スタッフ管理」 — **caller tăng thêm 1** |
| F6 | Dropdown 対象のアカウント trên màn lịch sử (`access_histories.js` `mounted`) | `public/js/admin/employees/access_histories.js` | Indirect | Nguồn dữ liệu dropdown đổi → danh sách bot thu hẹp |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `user_access_bot` | **SELECT only** | Dev khẳng định: chỉ chặn quyền đọc, **không đổi dữ liệu** |
| D2 | `user_staff_bots` | **SELECT only** | Chỉ đọc để tính phạm vi bot được phép |

> Dev ghi nguyên văn mục 4.2: *"Không có - chỉ chặn quyền đọc, không đổi dữ liệu (user_access_bot, user_staff_bots chỉ được SELECT)"*. **Không cần recover data.**

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Staff Management (FA-035)** — màn lịch sử đăng nhập nhân viên アカウントログイン履歴: dropdown chọn tài khoản, xem lịch sử, xuất CSV **nay giới hạn theo quyền** | F1, F2, F3, F4, F6 | **High** |
| T2 | Màn cha 「スタッフ管理」 (Quản lý nhân viên) — dùng chung nguồn quyền `getListBotIdStaffManagement` | F5 | Medium — Dev không sửa hàm này, nhưng caller tăng |

---

## Ghi chú bổ sung từ Dev (mục "Rủi ro / lưu ý khi test")

- Nếu hệ thống **chưa có bản ghi quyền tính năng cho màn quản lý nhân viên** thì **mọi nhân viên (kể cả phó quản lý)** sẽ không mở được màn lịch sử đăng nhập — Dev coi đây là đúng kỳ vọng ticket và đồng bộ với dropdown màn cha.
- **Endpoint lấy danh sách nhân viên theo tài khoản** mà màn này gọi **vẫn chưa kiểm phạm vi** (đã ghi ở quét ngang) — **vẫn còn lộ tên nhân viên nếu gọi thẳng**. Ngoài phạm vi ticket, chưa sửa.
- Hàm phân quyền dùng lại **không lọc trạng thái lời mời** (giữ nguyên hành vi màn cha) → nhân viên **được mời nhưng chưa chấp nhận (「招待中」)** vẫn tính là có quyền nếu role của họ được cấp quyền.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
