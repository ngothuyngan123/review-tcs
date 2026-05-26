# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<member điền>` |
| Commit / Pull Request | `<member điền>` |
| Branch | `<member điền>` |
| Ngày submit đánh giá | 2026-05-07 |

---

## 1. Nguyên nhân

Bot standard chưa có logic giới hạn số lượng staff khi tạo invite link và khi staff accept invite.

## 2. Cách fix

- **FE (`invite_staft.js`)**: Tạo link invite sẽ chỉ post lên những bot **được tick chọn**, không post all như trước.
- **BE (`StaffManagementController.php`)**:
  - Bỏ logic check selected của list bot post lên từ FE.
  - Thêm logic check max staff của bot: nếu là bot standard và `plan_type = 1` và đã đạt max → dừng lại và hiển thị message lỗi.
- **BE (accept invite)**: Khi staff accept link invite thì check max staff của bot. Nếu là bot standard và `plan_type = 1` và đã đạt max → bỏ qua bot đó (accept xong vẫn thành công cho các bot còn lại) và hiển thị message lỗi cho bot bị skip.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `generateLinkInviteStaff` (StaffManagementController.php) | Add logic check max staff per bot | Block tạo invite khi đã max |
| 2 | `acceptInviteStaff` (StaffManagementController.php) | Add logic check max staff per bot khi accept | Block accept khi đã max |
| 3 | `public/js/admin/employees/invite_staft.js` | Chỉ post lên bot tick chọn | Đảm bảo BE check đúng tập bot user mong muốn |
| 4 | `app/UserStaffBot.php` | (data class — đã verify) | Là model count staff per bot |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `generateLinkInviteStaff` | `app/Http/Controllers/Admin/StaffManagementController.php` | Direct | Add check max staff theo plan_type |
| F2 | `acceptInviteStaff` | `app/Http/Controllers/Admin/StaffManagementController.php` | Direct | Add check max staff khi accept |
| F3 | `invite_staft.js` | `public/js/admin/employees/invite_staft.js` | Direct | Đổi behaviour — chỉ post selected bot |
| F4 | `UserStaffBot` model | `app/UserStaffBot.php` | Indirect | Dùng để count staff per bot |

### 4.2. List data bị update khi fix bug

| # | Data | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Đây là fix logic kiểm tra, không thay đổi schema / data. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn generate invite link (admin) | F1, F3 | High |
| T2 | Màn accept bot của staff | F2 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller
- [ ] Mục 4.1 không thiếu function
- [ ] Mục 4.2 — Dev xác nhận thật sự không có data update? (audit log staff invite có ghi không?)
- [ ] Mục 4.3 cover được cả happy path lẫn edge case
- [ ] **Cần làm rõ với Dev**:
  - Số max chính xác = 10? Hard-code hay đọc từ plan config?
  - "Không bao gồm user chính" — UserStaffBot có count user chính không?
  - Khi accept invite cho nhiều bot 1 lúc, bot nào full thì skip — UI hiển thị message thế nào (per-bot hay 1 message tổng)?
