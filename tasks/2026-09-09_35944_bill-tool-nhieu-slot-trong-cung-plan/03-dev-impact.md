# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #35944 — Journal #133416 (AI AUTO-FIXBUG, 2026-08-28). Nội dung 4 mục bên dưới chép nguyên văn từ journal, không diễn giải lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (auto-fixbug) — assignee ticket: Ngọc Ánh |
| Commit / Pull Request | `<chưa có link PR>` — repo `sns-line`, commit `c3b7019dcd` (1 file), nhánh gốc `origin/release_step_20260805` |
| Branch | `ai_fixbug_35944` (đã push) |
| Ngày submit đánh giá | `2026-08-28` |
| Auto-filled | `2026-09-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bộ đếm slot trống của mỗi gói chỉ tính hợp đồng đã kích hoạt. Hợp đồng mua bằng chuyển khoản chỉ được kích hoạt khi cổng thanh toán báo đã nhận tiền, nên slot vừa đặt mua còn đang chờ chuyển khoản không bị đếm. Vì vậy khách đặt liên tiếp nhiều bill cùng một gói đều lọt qua kiểm tra, và khi các khoản đó vào tiền thì mỗi hợp đồng sinh ra một slot trống, dẫn tới nhiều slot trống của cùng một gói.

## 2. Cách fix

Sửa 2 truy vấn đếm slot chưa gắn tài khoản của màn mua gói (trang Thêm tài khoản mới và API kiểm tra trước khi mua) để tính cả hợp đồng thanh toán bằng chuyển khoản chưa thu được tiền là đang giữ chỗ, thay vì chỉ đếm hợp đồng đã kích hoạt. Gom điều kiện dùng chung vào hàm `applyUnconnectedSlotCondition` trong cùng controller. Quét ngang 4 truy vấn tương tự ở `UserController`: đều là danh sách slot dùng được ngay nên giữ nguyên.

**Bằng chứng Dev nêu ở mục VERIFY (nguyên văn):**
> `BotController::paymentBotSlotV2` tạo hợp đồng chuyển khoản với `is_active = inactive`, sau khi tạo charge mới set `status = 1` và `status_payment = 0`; `univapayCallback` khi nhận được tiền (`type_bill = 3`) mới set `is_active = 1` và `status_payment = 1` — đó là lúc slot trống trở nên hữu hình với bộ đếm cũ.

**Điều kiện mới (theo phần TỰ REVIEW của Dev):** `payment_method = chuyển khoản` **và** `status_payment` khác đã thu / lỗi thu → chỉ **THÊM** tập hợp đồng chuyển khoản chưa thu tiền vào bộ đếm, không loại bỏ trường hợp nào đang được đếm.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotV2Controller::index` — `app/Http/Controllers/Admin/BotV2Controller.php` | **SỬA** — dùng điều kiện đếm mới | Call site 1: trang Thêm tài khoản mới (màn chọn gói) |
| 2 | `BotV2Controller::getSlotUnconnectBot` — `app/Http/Controllers/Admin/BotV2Controller.php` | **SỬA** — dùng điều kiện đếm mới | Call site 2: API kiểm tra trước khi mua |
| 3 | `BotV2Controller::applyUnconnectedSlotCondition` — `app/Http/Controllers/Admin/BotV2Controller.php` | **THÊM MỚI** | Gom điều kiện dùng chung cho 2 call site trên |
| 4 | `BotController::paymentBotSlotV2` — `app/Http/Controllers/Admin/BotController.php` | Đọc, **không sửa** | Nơi tạo hợp đồng chuyển khoản (`is_active = inactive`, `status = 1`, `status_payment = 0`) |
| 5 | `BotController::univapayCallback` — `app/Http/Controllers/Admin/BotController.php` | Đọc, **không sửa** | Nơi tiền vào (`type_bill = 3`) set `is_active = 1`, `status_payment = 1` |
| 6 | `ListPageController::cancelTransfer` — `app/Http/Controllers/V2/Bill/ListPageController.php` | Đọc, **không sửa** | Hủy bill chuyển khoản — xóa hẳn bản ghi (không xóa mềm) |
| 7 | `isContractWaitingTransfer` — `public/_assets/modules/bill/js/index.js` | Đối chiếu | Cách màn danh sách hợp đồng xác định "đang chờ chuyển khoản" |
| 8 | `getListUserMaster` / `showModalTypeContractNewStep` — `public/js/admin/bill_tool/index.js` | Đọc, **không sửa** | JS màn bill tool |
| 9 | `UserController::initDataListBot` / `botsForUser` / `checkOnePlan` — `app/Http/Controllers/Admin/UserController.php` | Quét ngang, **giữ nguyên** | 4 truy vấn tương tự nhưng là danh sách slot **dùng được ngay** → khác phạm vi |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Dev ghi mục 4.1 dưới dạng **"File thay đổi"** (1 file), không liệt kê theo F1/F2. Bảng dưới là ánh xạ sang quy ước tag của repo, dựa trên chính mục 2 + mục 3 của Dev — không thêm function nào ngoài danh sách Dev đã nêu.
>
> **Nguyên văn 4.1 của Dev:** `app/Http/Controllers/Admin/BotV2Controller.php`

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotV2Controller::index` (trang chọn gói `/admin/bot-add`) | `app/Http/Controllers/Admin/BotV2Controller.php` | Direct | Truy vấn đếm slot chưa gắn — đã sửa |
| F2 | `BotV2Controller::getSlotUnconnectBot` (API kiểm tra trước khi mua) | `app/Http/Controllers/Admin/BotV2Controller.php` | Direct | Truy vấn đếm slot chưa gắn — đã sửa |
| F3 | `BotV2Controller::applyUnconnectedSlotCondition` | `app/Http/Controllers/Admin/BotV2Controller.php` | Direct | Hàm dùng chung **mới thêm** — 2 caller là F1 + F2 |
| F4 | `BotController::paymentBotSlotV2` | `app/Http/Controllers/Admin/BotController.php` | Indirect | Không sửa; là nguồn sinh hợp đồng chuyển khoản mà F1/F2 nay đếm |
| F5 | `BotController::univapayCallback` | `app/Http/Controllers/Admin/BotController.php` | Indirect | Không sửa; đổi trạng thái làm hợp đồng rời khỏi tập "chờ chuyển khoản" |
| F6 | `ListPageController::cancelTransfer` | `app/Http/Controllers/V2/Bill/ListPageController.php` | Indirect | Không sửa; hủy bill → giải phóng chỗ giữ |
| F7 | `UserController::initDataListBot` / `botsForUser` / `checkOnePlan` | `app/Http/Controllers/Admin/UserController.php` | Indirect | **Cố ý KHÔNG sửa** — Dev đánh giá khác phạm vi (danh sách slot dùng được ngay) |

### 4.2. List data bị update khi fix bug

> **Nguyên văn 4.2 của Dev:** Không có - fix chỉ đọc dữ liệu, không ghi/sửa bảng nào

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có)* | — | Dev khẳng định fix chỉ **đọc** dữ liệu, không ghi/sửa bảng nào; không cần recover data (mục 5 journal) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Add New Account (FA-032)** — chặn mua thêm slot trống khi đã có bill chuyển khoản cùng gói đang chờ thanh toán | F1, F2, F3 | *(Dev không ghi mức)* |
| T2 | **Contract Plan & Payment (FA-031)** — hợp đồng chờ chuyển khoản nay được tính là đang giữ chỗ slot | F4, F5, F6 | *(Dev không ghi mức)* |

---

## Rủi ro Dev tự nêu (nguyên văn mục TỰ REVIEW)

1. Khách đặt bill chuyển khoản rồi **không thanh toán và không bấm hủy** sẽ bị chặn mua thêm slot cùng gói cho tới khi hủy bill hoặc hợp đồng quá hạn — đúng theo spec mỗi gói chỉ 1 slot trống, màn hóa đơn có sẵn nút hủy chuyển khoản.
2. Kiểm tra **không khóa hàng** nên 2 tab bấm mua **ĐỒNG THỜI** vẫn có thể lọt — hạn chế sẵn có của mọi giới hạn theo gói, không phải kịch bản của ticket (mua liên tiếp).
3. Hợp đồng chuyển khoản bị hủy **bị xóa hẳn khỏi bảng** (không phải xóa mềm) và hợp đồng đã hủy có `status = 3` nên không chặn nhầm.

## Mức verify của Dev

| Mục | Giá trị |
|---|---|
| Mức | **lint** (chỉ `php -l`) |
| Lệnh | `php -l app/Http/Controllers/Admin/BotV2Controller.php`: No syntax errors detected; `git diff --stat origin/release_step_20260805...ai_fixbug_35944`: 1 file, 35 insertions, 14 deletions |
| ⚠️ Hạn chế | **Không tái hiện được trên dev** — MySQL `host.docker.internal:3306` báo Connection refused nên không dump được dữ liệu hợp đồng chờ chuyển khoản. **Không có bằng chứng chạy thực tế từ phía Dev.** |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
