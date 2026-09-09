# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36768 (journal #124403) bởi `/new-task`. **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs. Tester verify + tick checkbox trước khi chạy skill tiếp theo.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Nguyen Ngoc Hai` (assigned: Do Van Tu TuDV) |
| Commit / Pull Request | `commit 6f8195ee04` |
| Branch | `feature/premium-id-36768` |
| Ngày submit đánh giá | `2026-07-01` |
| Auto-filled | `2026-07-02 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine journal #124403 -->

Yêu cầu mới: bot LINE có thể có Premium ID (premiumId) bên cạnh Basic ID (line_id). Cần lấy premiumId từ LINE và hiển thị ưu tiên premiumId ở mọi nơi đang show "LINE ID" của bot (header, bill, admin, backup…), đồng thời cho phép tìm kiếm theo premium ID.

## 2. Cách fix

<!-- Nguyên văn từ Redmine journal #124403 -->

- Thêm cột `bots.premium_id` (varchar(100), nullable, after line_id) — migration `2026_06_16_120000_add_premium_id_to_bots_table`.
- Helper dùng chung `app/Helpers/functions.php`: `displayLineId($lineId, $premiumId)` — trả premiumId nếu có, ngược lại line_id.
- Model `Bots`: thêm accessor `display_line_id` (append vào `$appends`) dùng `displayLineId`.
- Job cron mới `update:premium_id` (`UpdatePremiumIdBots`) — daily 03:20: `chunkById(500)` các bot chưa xóa có `channel_access_token`, gọi `getLineInfoBot()` (LINE bot/info), **chỉ update `premium_id` khi LINE trả về premiumId** (tránh ghi đè rỗng khi API lỗi). Đăng ký trong `Kernel::$commands` + schedule.
- Ghi `premium_id` khi fetch bot info (chỉ khi `infoBot['premiumId']` không rỗng): `ChatController` (~1221), `Admin/BotController` (2 chỗ), `Admin/UserController`, và FE `layout_v2_header.js` set `botInfo.premium_id`.
- Đổi hiển thị sang premium-first tại các điểm show LINE ID: `header-content.blade.php` (field LINE ID + copy), `bill/index.blade.php` (6 chỗ), `Admin/AccountController` (display_line_id + select thêm cột), `Admin/UserController` list (`displayLineId`), `Basic/UserController`, `ScreenController` + `BackupService` (backup), các view `supper_admin/tab_info`, payment/bill khác.
- Tìm kiếm: `Admin/AccountController` và `Admin/UserController` bổ sung `orWhere('premium_id', 'like', ...)` ngoài line_id.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ Redmine journal #124403 mục 3 -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `select([... 'line_id' ...])` phục vụ hiển thị (AccountController, Basic/UserController, ScreenController, BackupService, dataBotContract) | Bổ sung cột `premium_id` vào select | Để accessor / `displayLineId` có dữ liệu premiumId |
| 2 | `generateUrlToChat($lineId)` | **Không đổi** — vẫn dùng line_id | Chủ đích: link `lin.ee/chat` phải theo basicId, không ảnh hưởng bởi premium_id |
| 3 | `getLineInfoBot()` | **Không sửa** — chỉ tái sử dụng | Helper có sẵn |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Parse từ journal #124403 mục 4.1 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `displayLineId($lineId, $premiumId)` (helper MỚI) | `app/Helpers/functions.php` | Direct | Trả premiumId nếu có, else line_id |
| F2 | `Bots::getDisplayLineIdAttribute()` (accessor MỚI) | Model `Bots` | Direct | Append `display_line_id` vào `$appends` |
| F3 | Command `UpdatePremiumIdBots` (`update:premium_id`, MỚI) | Command + `Kernel.php` | Direct | Daily 03:20, chunkById(500), gọi LINE bot/info |
| F4 | Ghi `premium_id` khi fetch bot info | `ChatController` (~1221), `Admin/BotController` (2 chỗ), `Admin/UserController` + FE `layout_v2_header.js` | Direct | Chỉ ghi khi `premiumId` không rỗng |
| F5 | Hiển thị + tìm kiếm premium-first | `Admin/AccountController` (search/list/select), `Admin/UserController` (search/list), `Basic/UserController` (select), `ScreenController`, `BackupService`, `Bots::dataBotContract` | Direct | +`orWhere('premium_id','like',...)` cho search |
| F6 | Blade hiển thị LINE ID | `header-content.blade.php`, `bill/*`, `payment_history/*`, `supper_admin/tab_info` | Direct | Đổi sang `display_line_id` / `displayLineId` |
| F7 | Đăng ký command + schedule | `Kernel.php` | Direct | `$commands` + `dailyAt('03:20')` |

### 4.2. List data bị update khi fix bug

<!-- Parse từ journal #124403 mục 4.2 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.premium_id` (cột mới, varchar(100) nullable, after line_id) | MIGRATE (thêm cột) | Migration `2026_06_16_120000_add_premium_id_to_bots_table` — cần `php artisan migrate` khi deploy |
| D2 | `bots.premium_id` (giá trị) | UPDATE | Ghi bởi (a) job daily `update:premium_id`, (b) luồng fetch bot info (tạo/cập nhật bot, mở chat). **Chỉ ghi khi LINE trả premiumId không rỗng** → không xóa/ghi đè rỗng |
| D3 | `bots.$appends` thêm `display_line_id` | (serialize) | Mọi lần serialize model `Bots` ra JSON kèm thêm field `display_line_id` (tăng nhẹ payload, accessor chạy mỗi lần) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Parse từ journal #124403 mục 4.3 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Hiển thị LINE ID bot ở header (popup QR / bot info — basic & admin, v2 & legacy) — hiển + copy | F1, F2, F6, D2 | High |
| T2 | Bill (請求): index (nhiều card: overdue/max friend), detail, detail-bill-fail, cancel, sort modal | F5, F6, D2 | High |
| T3 | Admin アカウント検索: bảng kết quả (tab user/bot) + chi tiết + copy + **search theo premiumId** | F5, D2 | High |
| T4 | Super admin: chi tiết bot, chi tiết user (tab info) | F5, F6, D2 | Medium |
| T5 | Trang chọn bot admin (pre_select_bot) + danh sách bot (index_v3) — cột LINE ID + search | F5, D2 | Medium |
| T6 | Backup: màn processing + chọn tài khoản đích (data copy) | F5, D2 | Medium |
| T7 | Flow add bot / change bot → `premium_id` lưu đúng | F4, D2 | High |
| T8 | Button 情報更新 (header) → LINE ID đổi sang premiumId ngay (không reload) | F4, D2 | High |
| T9 | Job daily 03:20 → cập nhật `premium_id` cho bot có premiumId; lỗi API từng bot bị bỏ qua (không dừng job); tải thêm lên LINE API + DB update theo chunk 500 | F3, F7, D2 | Medium |
| T10 | URL chat / add-friend (`generateUrlToChat`) — **KHÔNG đổi** (vẫn theo line_id) | mục 3 | Low (verify không regression) |
| T11 | premium_id stale/sai (job chưa chạy hoặc LINE đổi) → ID hiển thị/copy có thể lệch tới lần đồng bộ kế tiếp | D2 | Medium (edge case) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Nguồn: Redmine #36768 journal #122071 (tóm tắt thay đổi + danh sách màn tester) + journal #124403 (đánh giá ảnh hưởng chính thức). Fetched 2026-07-02. -->
