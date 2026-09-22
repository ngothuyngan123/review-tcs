# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: **AI Auto-fixbug LME** (Journal #125990 Redmine #38785), KHÔNG phải Dev người viết. Mục 4.1 chỉ liệt kê **file thay đổi**, không liệt kê function-level impact; mục 3 không có bảng caller đầy đủ. Leader cần đối chiếu diff thật (branch `ai_small_38785`, commit `48877bb5b3`) trước khi chốt coverage.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Auto-fixbug LME (assignee ticket: Kim Cúc) |
| Commit / Pull Request | commit `48877bb5b3` (repo `sns-line`) — `<chưa có link PR>` |
| Branch | `ai_small_38785` (nhánh gốc `release_step_20260623`, 1 file) — đã push origin |
| Ngày submit đánh giá | 2026-07-14 |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hai API áp/kiểm coupon (`checkCouponCode`, `applyCouponCode`) chỉ nằm sau đăng nhập nhưng đọc thẳng mã coupon + id hợp đồng bot + id bot từ request rồi gia hạn hạn hợp đồng, không kiểm coupon/hợp đồng/bot có thuộc người đang đăng nhập không. Bất kỳ user nào cũng có thể dùng 1 coupon chưa dùng để gia hạn hợp đồng trả phí của bot người khác (IDOR).

## 2. Cách fix

`checkCouponCode` + `applyCouponCode`: thay truy vấn hợp đồng thô (`BotContracts::where id`) bằng `Bots::dataBotContract(botContractId, getListBotIdStaffManagement(userId, pointSettings), userId)` — hàm chuẩn dự án tự lọc quyền (chỉ trả hợp đồng khi bot thuộc quyền staff của user **HOẶC** `bot_contracts.admin_id = user`), trả `null` → coupon không hợp lệ, không gia hạn. `botId` vẫn lấy từ request như cũ. Coupon giữ nguyên lookup theo `coupon_code`. Bỏ 1 truy vấn hợp đồng bị lặp.

> ⚠️ **CONFLICT cần Leader xác minh trên diff thật:** câu *"botId vẫn lấy từ request như cũ"* mâu thuẫn với TC `NEW-8` / `NEW-12` trên LME TEST STUDIO (ghi *"BE bỏ qua `botId` request, lấy từ `$botContract->bot_id` qua `bot_slots`"*, dẫn diff `-$botId=$request->botId`). Hai hướng này cho **expected khác nhau** ở nhóm TC giả mạo `botId`.

**Verify của AI:** mức `lint` — `php -l UserController.php: No syntax errors`. Bằng chứng: `Bots::dataBotContract` lọc `bots.id IN listBotAccept` OR `bot_contracts.admin_id == user`; dùng nhất quán ở `PointSettingController` / `ListPageController` / `BotEnterPriseController` cho thao tác billing.

**Recover data:** ✔ Không cần recover data.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- AI chỉ liệt kê 3 function dạng plain list, không có bảng caller + không nêu thay đổi/lý do từng function. Convert sang bảng template, cột "Thay đổi" điền theo mục 2. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `checkCouponCode` — `app/Http/Controllers/Admin/UserController.php` (~L9560) | Thay `BotContracts::where('id', $botContractId)` bằng `Bots::dataBotContract(...)` | Chặn IDOR ở bước preview; không có quyền → trả coupon không hợp lệ |
| 2 | `applyCouponCode` — `app/Http/Controllers/Admin/UserController.php` (~L9606) | Thay truy vấn hợp đồng thô bằng `Bots::dataBotContract(...)`; bỏ 1 truy vấn hợp đồng bị lặp | Chặn IDOR ở bước ghi; chỉ gia hạn khi hợp đồng thuộc quyền user |
| 3 | `Bots::dataBotContract` — `app/Bots.php` (~L120-132) | **Không sửa** — chỉ được gọi thêm ở 2 function trên | Hàm chuẩn dự án cho thao tác billing, đã dùng ở `PointSettingController` / `ListPageController` / `BotEnterPriseController` |

> ⚠️ **Input thiếu:** AI **không liệt kê danh sách caller** của `getListBotIdStaffManagement` hay của `Bots::dataBotContract` để chứng minh không sót nơi bị ảnh hưởng. Đây là **hàm dùng chung** → theo quy ước repo, phải có danh sách caller trước khi kết luận không regression.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- AI chỉ ghi "File thay đổi: UserController.php". Bảng dưới suy từ mục 2 + 3, giữ nguyên phạm vi AI nêu. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `checkCouponCode` — endpoint `POST /ajax/check-coupon-code` | `app/Http/Controllers/Admin/UserController.php` | Direct | Bước **preview** ngày gia hạn, không ghi DB |
| F2 | `applyCouponCode` — endpoint `POST /ajax/apply-coupon-code` | `app/Http/Controllers/Admin/UserController.php` | Direct | Bước **ghi thật**: đốt coupon + gia hạn hợp đồng + gia hạn bot |
| F3 | `Bots::dataBotContract` | `app/Bots.php` | Indirect (không sửa, thêm caller) | Inner join `bot_slots` → hợp đồng thiếu `bot_slots` bị trả `null` |
| F4 | `getListBotIdStaffManagement($userId, 'pointSettings')` | `<chưa rõ file — AI không nêu>` | Indirect (không sửa, thêm caller) | Quyết định nhánh quyền staff |

### 4.2. List data bị update khi fix bug

> AI khẳng định: **"Không có (chỉ đổi cách lấy/kiểm quyền hợp đồng)"** — không có migration, không đổi schema.
> Bảng dưới liệt kê **data mà 2 API này ghi/đọc ở runtime** — không phải data bị fix thay đổi, nhưng là data phải đối chứng khi test (đặc biệt **đối chứng âm**: phải KHÔNG đổi khi IDOR bị chặn).

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D0 | — | **Không có data bị fix thay đổi** | Theo mục 4.2 của AI |
| D1 | `coupon_management.is_used` / `.user_id` / `.bot_contract_id` / `.datetime_use` / `.bot_name` | UPDATE (runtime) | Đối chứng âm: quyền fail → `is_used` phải VẪN = 0 (coupon không bị đốt) |
| D2 | `bot_contracts.expired_date_contract` | UPDATE (runtime) | Đối chứng âm: hợp đồng nạn nhân không đổi |
| D3 | `bots.expired_date` | UPDATE (runtime) | Đối chứng âm: bot nạn nhân / bot giả mạo `botId` không đổi |
| D4 | `bot_life_cycles` (bản ghi apply coupon) | CREATE (runtime) | Không tạo bản ghi khi quyền fail |
| D5 | `bot_slots` | READ (điều kiện join) | Hợp đồng thiếu `bot_slots` → `dataBotContract` trả `null` → **có thể chặn nhầm chủ hợp đồng hợp lệ** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Coupon Code Issue (FS-015)** — chỉ chủ / staff-có-quyền của hợp đồng mới áp/kiểm được coupon | F1, F2, D1 | High |
| T2 | **Contract Plan & Payment (FA-031)** — gia hạn hợp đồng chỉ khi hợp đồng thuộc quyền người đăng nhập | F2, D2, D3 | High |
| T3 | Màn chi tiết hợp đồng (契約情報 `/detail-contract/{id}`) — modal nhập mã coupon (`detail.js:203, 239`) | F1, F2 | Medium (đường đi UI của T1/T2) |
| T4 | Luồng **staff có quyền `pointSettings`** áp coupon cho bot được phân quyền | F3, F4 | Medium — nhánh `listBotAccept` của `dataBotContract`, dễ chặn nhầm |
| T5 | Hợp đồng **không có `bot_slots`** (dữ liệu cũ / edge) | F3, D5 | Medium — **rủi ro do chính fix**: chủ hợp đồng hợp lệ có thể bị chặn (REQ-006 trên Studio) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — ⚠️ **đang có CONFLICT về `botId`**, phải đọc diff `48877bb5b3` để chốt
- [ ] Mục 3 đã check đủ caller — ⚠️ **AI KHÔNG cung cấp danh sách caller** của `dataBotContract` / `getListBotIdStaffManagement`
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ AI chỉ ghi file, bảng F1-F4 do `/new-task` suy ra
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
