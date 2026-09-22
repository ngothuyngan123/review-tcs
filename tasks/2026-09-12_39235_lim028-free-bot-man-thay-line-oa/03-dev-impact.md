# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME)` — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `commit 3057ac6942` (repo `sns-line`) — không có link PR trong ticket |
| Branch | `ai_fixbug_39235` (nhánh gốc `release_step_20260805`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-27` (Journal #133261) |
| Auto-filled | `2026-09-12 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN của Journal #133261. -->

Màn thay LINE OA (`/admin/change-bots-new`) chỉ kiểm tra quyền truy cập theo tài khoản, **KHÔNG kiểm tra gói cước và cửa sổ campaign**. Quy tắc bot gói miễn phí chỉ được thay LINE OA trong 1 tháng kể từ ngày tạo bot mới chỉ được cài ở màn kế bên (thay tài khoản phụ) và ở phía giao diện, nên bot Free cũ lẫn Free mới đã hết campaign vẫn mở được màn hình này bằng URL trực tiếp.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX của Journal #133261. -->

Bổ sung chốt chặn theo gói ở phía máy chủ cho màn thay LINE OA (hàm dựng màn `/admin/change-bots-new`): bot gói miễn phí đã quá 1 tháng kể từ ngày tạo bot thì không vào được màn hình mà chuyển sang trang thông báo cần nâng cấp gói — dùng đúng trang chặn và đúng quy tắc campaign mà màn thay tài khoản phụ đang áp dụng.

**Điểm khác**: nhận diện gói miễn phí bằng hàm dùng chung của model bot (`Bots::isFreePlan()`) nên phủ cả Free cũ (`plan_type = 2`) lẫn Free mới (loại hợp đồng `'free'`), trong khi guard cũ chỉ xét Free cũ.

**Quét ngang**: các điểm còn lại trong luồng thay LINE OA (khởi tạo dữ liệu màn, thực thi đổi LOA) vẫn nhận diện gói miễn phí chỉ bằng `plan_type = 2` — **đã ghi nhận, không sửa ngoài phạm vi ticket**.

**Quy tắc campaign lấy nguyên từ `BotController::adminChangeBotSub` (#39230)**: `free && now >= created_at + 1 tháng (cuối ngày)` → chặn.

**Phạm vi diff**: `git diff --stat release_step_20260805...ai_fixbug_39235` = **1 file, +10 dòng**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN, convert sang bảng. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::adminChangeNewBot` — `app/Http/Controllers/Admin/BotController.php` | **Đã thêm guard** | Điểm fix chính — hàm dựng màn thay LINE OA, trước đó không có guard gói/campaign |
| 2 | `BotController::adminChangeBotSub` — `app/Http/Controllers/Admin/BotController.php` | Không sửa | Guard mẫu đã có từ #39230 — nguồn copy quy tắc campaign |
| 3 | `BotController::userCanAccessChangeBot` — `app/Http/Controllers/Admin/BotController.php` | Giữ nguyên | Guard quyền truy cập, đứng trước guard gói |
| 4 | `BotController::checkAuthBot` — `app/Http/Controllers/Admin/BotController.php` | Không sửa | Chỉ kiểm cột `has_campaign`, không chặn được truy cập màn |
| 5 | `ChangeBotController::init` — `app/Http/Controllers/Ajax/ChangeBotController.php` | **Không sửa (điểm hở)** | Dữ liệu `is_free_plan` / `has_campaign` cho màn — vẫn nhận diện Free bằng `plan_type = 2` |
| 6 | `ChangeBotController::botCanChangeBot` + `execute` — `app/Http/Controllers/Ajax/ChangeBotController.php` | **Không sửa (điểm hở)** | Guard phía API đổi LOA — vẫn nhận diện Free bằng `plan_type = 2` |
| 7 | `Bots::isFreePlan` — `app/Bots.php` | Không sửa (được gọi lại) | Nhận diện gói miễn phí dùng chung; đang dùng ở `ChatController` / `ActionScheduleController` / `BackupController` |
| 8 | `change_new.js` `selectMethod` / `fetchPageData` — `public/_assets/modules/change_bots/js/change_new.js` | Không sửa | Chặn phía giao diện (lớp cũ, không đủ) |
| 9 | `admin/bots/change_bot_plan_blocked.blade.php` | Không sửa (được dùng lại) | Trang thông báo chặn theo gói |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ ghi "4.1 File thay đổi: app/Http/Controllers/Admin/BotController.php". Bảng dưới derive từ mục 3 + mục 2. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController::adminChangeNewBot` (màn `GET /admin/change-bots-new/{id}`) | `app/Http/Controllers/Admin/BotController.php` | **Direct** | Điểm sửa duy nhất — thêm guard gói + cửa sổ campaign, đặt **sau** guard quyền truy cập |
| F2 | `Bots::isFreePlan` | `app/Bots.php` | Indirect (caller mới) | Không sửa, nhưng nay có thêm 1 caller. Nhận diện Free = `plan_type == 2` **hoặc** `bot_contracts.contract_type == 'free'` |
| F3 | Trang chặn `change_bot_plan_blocked.blade.php` | `resources/views/admin/bots/` | Indirect (dùng lại) | Nay được render thêm từ màn thay LINE OA, không chỉ từ màn thay tài khoản phụ |
| F4 | `BotController::userCanAccessChangeBot` | `app/Http/Controllers/Admin/BotController.php` | Indirect (thứ tự guard) | Không sửa, nhưng thứ tự 2 lớp chặn quyết định: bot sai/không thuộc account → `/basic/overview`; Free hết campaign → trang chặn gói |
| F5 | `ChangeBotController::init` / `botCanChangeBot` / `execute` | `app/Http/Controllers/Ajax/ChangeBotController.php` | **KHÔNG sửa — điểm hở còn lại** | Vẫn chỉ nhận diện Free bằng `plan_type = 2` → bot Free **mới** hết campaign về lý thuyết vẫn gọi thẳng API đổi LOA được. Dev đề nghị tách ticket riêng |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2 của Dev. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(Không có)* | — | Dev ghi: "Không có — chỉ thêm điều kiện chặn khi dựng màn hình, **không đọc/ghi thay đổi dữ liệu**" |

**Data chỉ ĐỌC (không đổi), là biến quyết định của guard** — tester cần dựng đúng:

| # | Data đọc | Vai trò |
|---|---|---|
| — | `bots.plan_type` | `= 2` → Free cũ |
| — | `bot_contracts.contract_type` | `= 'free'` → Free mới (join qua bản ghi slot) |
| — | `bots.created_at` | Mốc cửa sổ campaign = `created_at + 1 tháng`, tính **hết ngày** (23:59:59) |
| — | `bots.has_campaign` | Cột cũ dùng ở `checkAuthBot`, **không** phải điều kiện của guard mới |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 của Dev + risk derive. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **LOA Connection Settings (FA-038)** — màn thay LINE OA (LOA入れ替え) nay chặn bot gói miễn phí đã hết campaign 1 tháng | F1, F2 | **High** |
| T2 | **Add New Account (FA-032)** — người dùng bị chặn được đưa về trang thêm/chọn tài khoản (dùng lại trang chặn sẵn có) | F3 | Medium |
| T3 | Màn thay tài khoản phụ (`/admin/change-bot-sub/{id}`) | F4 (cùng file, cùng quy tắc campaign) | Low — Dev tuyên bố không đụng, cần TC chứng minh |
| T4 | Luồng API đổi LINE OA (`ChangeBotController`) | F5 | Medium — **điểm hở đã biết, ngoài phạm vi ticket** |

---

## 5. Recover data

✔ **Không cần recover data** (Dev xác nhận).

## 6. Mức verify của Dev

| Mục | Giá trị |
|---|---|
| Mức | **lint** (không có unit test, không chạy dữ liệu thật) |
| Lệnh | `php -l app/Http/Controllers/Admin/BotController.php` → No syntax errors detected; `git diff --stat release_step_20260805...ai_fixbug_39235` → 1 file, +10 dòng |
| ⚠️ Hạn chế | MySQL dev (`host.docker.internal:3306`) **không kết nối được** trong phiên AI fix (Connection refused) → **không tái hiện được bằng dữ liệu thật**, chỉ kiểm chứng bằng đọc mã nguồn |

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

1. ⚠️ **Conflict expected**: ticket ghi *"chuyển hướng về trang chủ admin"*; bản fix trả **trang chặn HTTP 200** (「スタンダードプラン以上のご契約でご利用できます」) rồi đưa sang `/admin/bot-add`. Nếu PM muốn đúng chữ "về trang chủ admin" thì đổi 1 dòng thành `redirect('/basic/overview')`.
2. **Trường hợp hiếm**: bot miễn phí đang chạy dở tiến trình đổi LOA mà campaign hết hạn đúng lúc đó sẽ **không mở lại được màn theo dõi tiến độ** (cửa sổ vài phút). Dev chưa nới điều kiện này.
3. **Điểm hở API**: guard phía API đổi LOA vẫn nhận diện Free hẹp hơn (chỉ Free cũ) → bot Free mới hết campaign về lý thuyết vẫn gọi thẳng API được. Dev đề nghị tách ticket riêng.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Đã chốt conflict expected** (trang chặn `/admin/bot-add` vs redirect `/basic/overview`) với PM
