# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Hạnh Nguyễn` |
| Commit / Pull Request | `https://bitbucket.org/snstool/sns-line/pull-requests/10229/diff` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-04` |
| Auto-filled | `2026-06-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Màn Quản lý popup (`/basic/popup-manager`) chưa có cơ chế ghi nhớ folder đang chọn (khác với các màn QR/template/tag... đã dùng cookie `folder_xxx`).
- Khi user đang đứng trong 1 folder rồi tạo item → trang reload lại từ đầu, `group_open` luôn về 0 → bị nhảy về folder default thay vì giữ folder vừa thao tác.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Thêm cơ chế ghi nhớ folder đang chọn cho màn popup bằng cookie `folder_popup` (lưu theo từng bot), đồng bộ với pattern các màn khác:
- JS: khi đổi folder (`showGroup`) gọi ajax lưu cookie `folder_popup`; khi load trang (`created`) đọc lại `folder_cookie` để set `group_open` → giữ đúng folder sau reload/tạo item.
- BE: thêm route `popupSetCookie`, thêm case popup trong hàm dùng chung `folderSetCookie`; `PopupController@index` đọc cookie, kiểm tra folder còn tồn tại (đúng bot, đúng kind, chưa xóa) — nếu folder không hợp lệ thì reset về 0, rồi truyền `folderCookie` ra view.
- Clear cookie `folder_popup` khi logout / đổi user để tránh lẫn dữ liệu giữa các tài khoản.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `folderSetCookie` (BasicController) | Chỉ THÊM case `popup`, không sửa case cũ | Hàm dùng chung switch-case cho nhiều màn (template, reply, tag, cross, conversion, landing, schedule...). Thêm case popup → các màn khác không ảnh hưởng. |
| 2 | `showGroup` / `created` (popup/index.js) | Thêm logic đọc/lưu cookie | Chỉ thuộc Vue instance màn popup, không dùng nơi khác. |
| 3 | `loginUserById` (Admin) + `logout` (AuthController) | Thêm 1 dòng clear cookie `folder_popup` | Cùng nhóm clear các cookie folder sẵn có → không ảnh hưởng luồng logout. |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | route `popupSetCookie` (`/basic/popup/set-cookie`) | `routes/web.php` | Direct | Thêm route mới |
| F2 | `folderSetCookie()` — thêm case `popup` (set cookie `folder_popup`, path `/popup-manager`) | `app/Http/Controllers/Basic/BasicController.php` | Direct | Hàm dùng chung — chỉ thêm case, không sửa case cũ |
| F3 | `index()` — đọc/validate cookie `folder_popup`, reset nếu folder không tồn tại, truyền `folderCookie` ra view | `app/Http/Controllers/Basic/PopupController.php` | Direct | |
| F4 | `created()` — đọc `folder_cookie` set `group_open` khi load trang | `public/js/popup/index.js` | Direct | |
| F5 | `showGroup()` — ajax lưu cookie `folder_popup` khi đổi folder | `public/js/popup/index.js` | Direct | |
| F6 | thêm biến `folder_cookie` và route `set_cookie` (`popupSetCookie`) cho JS | `resources/views/basic/popup/index.blade.php` | Direct | |
| F7 | `loginUserById()` — clear cookie `folder_popup` khi đổi/đăng nhập user khác | `app/Http/Controllers/Admin/UserController.php` | Indirect | |
| F8 | `logout()` — clear cookie `folder_popup` khi logout | `app/Http/Controllers/AuthController.php` | Indirect | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Cookie `folder_popup` (lưu folder đang chọn ở màn Popup theo từng bot) | CREATE / UPDATE / DELETE | Không có thay đổi cột DB. Tạo khi đổi folder, clear khi logout/đổi user |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn Quản lý popup (`/basic/popup-manager`): chuyển folder, tạo/sửa item — giữ đúng folder đang chọn sau reload | F1, F2, F3, F4, F5, F6, D1 | Medium |
| T2 | Luồng logout / đăng nhập bằng user khác (clear cookie `folder_popup`) | F7, F8, D1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ x] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [x ] Mục 2 (cách fix) có thể trace về code
- [ x] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ x] Mục 4.1 không thiếu function (so với mục 3)
- [ x] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ x] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ x] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
