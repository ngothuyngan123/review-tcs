# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee ticket: `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | repo `sns-line` · commit `d1437b55b1` (8 file) · đã push. Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38843 |
| Branch | `ai_small_38843` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-10` (journal Redmine 2026-08-10T06:46:27Z — bản chốt) |
| Auto-filled | `2026-08-11 by /new-task` |

> ⚠️ **Có 2 vòng báo cáo Auto-fixbug trên Redmine #38843 (cùng ngày 2026-08-10)**:
> - Vòng 1 — `03:16:54Z`, commit `43037e3645`, 8 file, **11 unit test**. Truy vấn hợp đồng chỉ lấy bản ghi `is_active = 1`.
> - Vòng 2 (**bản chốt**) — `06:46:27Z`, commit `d1437b55b1`, 8 file, **15 unit test**. Bổ sung theo spec mới: chặn cả `bot_contracts.status = 3` (hợp đồng đã huỷ) khi bản ghi **không còn `is_active`**; truy vấn bỏ lọc `is_active`, bỏ `groupBy` chọn ngẫu nhiên, xếp hợp đồng đang hiệu lực trước.
>
> **File này chép nguyên văn vòng 2 (bản chốt).** Nếu QA checkout branch mà truy vấn vẫn lọc `is_active = 1` ⇒ đang ở commit cũ, hỏi lại Dev.
>
> ⚠️ **Mâu thuẫn nội tại trong báo cáo vòng 2**: mục ■2 ghi *"đã thêm 4 ca kiểm thử cho nhánh status = 3 (tổng 15 ca, chạy PHPUnit pass)"* nhưng mục ■6 VERIFY vẫn ghi *"OK (11 tests, 14 assertions)"* (copy nguyên từ vòng 1) ⇒ **bằng chứng chạy test cho 4 ca mới CHƯA được dán lại**. Leader hỏi Dev xác nhận trước khi coi phần `status = 3` là đã có unit test bảo chứng.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN — báo cáo Auto-fixbug 2026-08-10 (vòng 2) -->

Toàn bộ API cho app mobile (nhóm route `api/mobile`) chỉ đi qua middleware xác thực đăng nhập, không hề kiểm tra hợp đồng của tài khoản; middleware chặn hết hạn chỉ được gắn cho nhóm route web `/basic`. Vì vậy tài khoản đã hết hợp đồng vẫn gọi được mọi API và dùng app bình thường. Ngoài ra API danh sách tài khoản chỉ trả cờ thanh toán thất bại, không trả trạng thái hết hợp đồng nên app cũng không có dữ liệu để hiện popup chặn.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX — báo cáo Auto-fixbug 2026-08-10 (vòng 2) -->

Bổ sung phía máy chủ (`sns-line`):

1. Dịch vụ **`ContractExpireService`** xác định tài khoản hết hợp đồng theo **cùng quy tắc với web** (hợp đồng huỷ, gói trả phí quá hạn quá 23 giờ hoặc chưa thanh toán, gói free quá hạn 1 năm), có truy vấn gom qua `BotRepository`.
2. Middleware **`MobileContractExpire`** gắn cho **toàn bộ nhóm route `api/mobile`** — nhận diện tài khoản gửi kèm request (`botId` / `bot_id` / `botIdCurrent`), nếu hết hợp đồng thì trả **HTTP 403 với mã lỗi `contract_expired`** và thông điệp tiếng Nhật đúng nội dung ticket, đồng thời **chừa các API đăng xuất / danh sách tài khoản / thông tin người dùng / thông báo bảo trì** để người dùng còn chọn tài khoản khác.
3. API danh sách tài khoản trả thêm cờ **`is_contract_expired`** cho từng tài khoản và chuỗi thông điệp popup.

**BỔ SUNG LẦN 2 (theo spec mới):** chặn cả trường hợp `bot_contracts.status = 3` (hợp đồng đã huỷ) mà bản ghi hợp đồng **không còn `is_active`** — trước đây truy vấn chỉ lấy hợp đồng `is_active = 1` nên tài khoản bị huỷ hợp đồng theo đường **huỷ hợp đồng mới chưa bill** (`is_active = 0`) không bị chặn. Truy vấn `BotRepository` nay trả về **mọi** hợp đồng gắn với bot (bỏ lọc `is_active`, bỏ `groupBy` chọn ngẫu nhiên, xếp hợp đồng đang hiệu lực trước); `ContractExpireService` gom theo bot rồi xét:

- hợp đồng hiện tại (`is_active = 1`) bị huỷ → **chặn**;
- không còn hợp đồng hiệu lực nào mà có hợp đồng đã huỷ → **cũng chặn**;
- các quy tắc ngày hết hạn / chưa thanh toán **giữ nguyên** và **chỉ đọc từ hợp đồng đang hiệu lực** để không chặn nhầm hợp đồng chờ chuyển khoản chưa bill.

Đã thêm 4 ca kiểm thử cho nhánh `status = 3` (tổng 15 ca, chạy PHPUnit pass).

**Quét ngang:** nhóm route mobile web cũ (middleware `mobile_access`) cũng thiếu kiểm tra tương tự nhưng **thuộc sản phẩm khác, chỉ ghi nhận không sửa**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN — convert list plain sang bảng, giữ nguyên chữ của Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MobileContractExpire::handle` (`app/Http/Middleware/MobileContractExpire.php`) | **MỚI** | Cổng kiểm tra hợp đồng cho toàn bộ nhóm route `api/mobile`; trả HTTP 403 + `contract_expired` |
| 2 | `MobileContractExpire::resolveBotId` (`app/Http/Middleware/MobileContractExpire.php`) | **MỚI** | Nhận diện tài khoản gửi kèm request qua `botId` / `bot_id` / `botIdCurrent` |
| 3 | `ContractExpireService::isExpired` (`app/Services/ContractExpireService.php`) | **MỚI** | Xác định 1 tài khoản hết hợp đồng |
| 4 | `ContractExpireService::getExpiredBotIds` (`app/Services/ContractExpireService.php`) | **MỚI** | Truy vấn gom nhiều bot (dùng cho API danh sách tài khoản) |
| 5 | `ContractExpireService::isExpiredState` (`app/Services/ContractExpireService.php`) | **MỚI** | Quy tắc xét trạng thái hết hợp đồng (huỷ / quá hạn / chưa thanh toán / free quá 1 năm) |
| 6 | `BotRepository::getContractStateByIds` (`app/Repositories/Eloquents/BotRepository.php`) | **CÓ SỬA (vòng 2)** — bỏ lọc `is_active`, bỏ `groupBy`, xếp hợp đồng đang hiệu lực trước | Trả về mọi hợp đồng gắn với bot để bắt được `status = 3` khi `is_active = 0` |
| 7 | `BookingCalendar::getBots` (`app/Http/Controllers/Api/BookingCalendar.php`) | **CÓ SỬA** | API danh sách tài khoản trả thêm cờ `is_contract_expired` + chuỗi thông điệp popup |
| 8 | `IsExpire::handle` (`app/Http/Middleware/IsExpire.php`) | **KHÔNG SỬA** | Tham chiếu quy tắc web — nguồn để đồng bộ quy tắc hết hạn |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn "■ 4.1 File thay đổi" — Dev liệt kê theo FILE. Cột Function/Module map lại từ mục 3 (chữ của Dev). -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ContractExpireService` (`isExpired` / `getExpiredBotIds` / `isExpiredState`) — quy tắc xác định hết hợp đồng | `app/Services/ContractExpireService.php` | Direct | File MỚI. Dùng lại đúng quy tắc web `IsExpire`, **có 2 khác biệt CÓ CHỦ ĐÍCH** — xem mục 5 |
| F2 | `MobileContractExpire` (`handle` / `resolveBotId`) — middleware chặn app mobile | `app/Http/Middleware/MobileContractExpire.php` | Direct | File MỚI. Trả **HTTP 403** + mã lỗi `contract_expired` + message JP. Có **danh sách API được chừa** (đăng xuất / danh sách tài khoản / thông tin người dùng / thông báo bảo trì) |
| F3 | `BotRepository::getContractStateByIds` — truy vấn trạng thái hợp đồng theo danh sách bot | `app/Repositories/Eloquents/BotRepository.php` | Direct | **Sửa ở vòng 2**: bỏ lọc `is_active`, bỏ `groupBy` (trước đây chọn ngẫu nhiên 1 hợp đồng), sắp xếp hợp đồng đang hiệu lực trước |
| F4 | Khai báo interface repository | `app/Contracts/Repositories/BotRepositoryInterface.php` | Direct | Thêm chữ ký `getContractStateByIds` |
| F5 | Đăng ký middleware | `app/Http/Kernel.php` | Direct | Đăng ký alias `MobileContractExpire` |
| F6 | Gắn middleware cho nhóm route `api/mobile` | `routes/api.php` | Direct | **Điểm rủi ro rộng nhất** — toàn bộ API app mobile đi qua cổng mới |
| F7 | `BookingCalendar::getBots` — API danh sách tài khoản của app | `app/Http/Controllers/Api/BookingCalendar.php` | Direct | Trả thêm `is_contract_expired` + chuỗi thông điệp popup. **API này nằm trong danh sách được CHỪA** (không bị 403) |
| F8 | Unit test quy tắc hết hợp đồng | `tests/Feature/ContractExpireServiceTest.php` | Direct | 15 ca (11 vòng 1 + 4 ca nhánh `status = 3`) |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn "■ 4.2 Data ảnh hưởng" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Chỉ **ĐỌC** `bots`, `bot_slots`, `bot_contracts`; **không ghi/sửa dữ liệu, không migration** |
| — | Recover data | — | ✔ Không cần recover data |

> Ghi chú thêm (từ mục Tự review của Dev — không phải data bị ghi, nhưng ảnh hưởng vận hành): **mỗi request API mobile có thêm 1 truy vấn nhỏ theo khoá chính `bots.id`** (join `bot_slots` / `bot_contracts`). Dev đề xuất có thể cache theo request nếu thấy tải cao.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn "■ 4.3 Tính năng liên quan" -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Contract Plan & Payment (FA-031)** — trạng thái hết hợp đồng của tài khoản trở thành **điều kiện chặn app mobile** | F1, F3, F6 | High |
| T2 | **Account Select (`account-select`)** — API danh sách tài khoản của app trả thêm cờ hết hợp đồng và thông điệp popup | F7 | High |
| T3 | **1-on-1 Chat (FA-001)** — mọi API chat của app đi qua middleware mới, bị chặn khi tài khoản hết hợp đồng | F2, F6 | High |
| T4 | **Mobile App API (outside glossary)** — toàn bộ nhóm route `api/mobile` (**bạn bè, đặt lịch, thông báo, form, tag, doanh số**) chịu chung cổng kiểm tra hợp đồng | F2, F6 | High |

---

## 5. Verify của Dev + Rủi ro tự nêu (nguyên văn — dùng để dựng TC)

### Mức verify: **unit-test** (KHÔNG có verify runtime với DB thật)

`php -l` cho 7 file PHP đã sửa: **No syntax errors detected**; `vendor/bin/phpunit --filter ContractExpireServiceTest`: **OK (11 tests, 14 assertions)**; Container resolve middleware + service qua bootstrap Laravel: **OK**; `php artisan route:list`: lỗi nền sẵn (`gCalendarController` thiếu file credential Google trong container), **không do fix**.

⚠️ **Bằng chứng còn thiếu (nguyên văn Dev nêu)**:

- **MySQL dev `host.docker.internal:3306` không kết nối được (Connection refused)** → **không kiểm chứng được dữ liệu hợp đồng thật**, quy tắc hết hạn lấy theo middleware web `IsExpire`.
- **App Flutter (`share/src/lme-fluter-app`) hiện chỉ xử lý `status_payment_fail` trong `open_modal_list_bot.dart`, CHƯA có popup hết hợp đồng → cần app bổ sung phần hiển thị.**
- Con số test trong mục VERIFY (`11 tests`) **chưa khớp** với mục Cách fix (`tổng 15 ca`) — xem cảnh báo đầu file.

### Tự review của Dev (nguyên văn)

Fix nằm **hoàn toàn ở lớp API mobile của `sns-line`**: thêm cổng kiểm tra hợp đồng (middleware) + cờ trạng thái trong API danh sách tài khoản, dùng lại đúng quy tắc hết hạn của web nên không tạo định nghĩa mới. **Thiết kế fail-open có chủ đích**: request không kèm mã tài khoản, ngày hết hạn rỗng, hoặc môi trường tắt thanh toán thì **không chặn**, tránh khoá nhầm khách đang trả phí.

### Rủi ro / lưu ý khi test (Dev tự nêu — nguyên văn)

- **Popup + nút chọn tài khoản khác phải do app Flutter implement** theo mã lỗi `contract_expired`; **bản app cũ sẽ chỉ thấy lỗi chung** khi gọi API.
- **Middleware áp cho toàn bộ nhóm `api/mobile`** — nếu quy tắc hết hạn quá rộng sẽ **chặn nhầm**; đã chừa các API đăng xuất / danh sách tài khoản / thông tin người dùng và **bỏ qua khi thiếu dữ liệu**.
- Giữ nguyên **cổng env `ENABLE_PAYPAL`** như web: **môi trường tắt cờ này sẽ KHÔNG chặn** (đồng bộ với hành vi web hiện tại).
- **Khác web có chủ đích**: (a) **ngày hết hạn NULL coi như CHƯA hết hạn**; (b) các trạng thái **gói tăng bạn bè (`max_friend_plan`) KHÔNG tính là hết hợp đồng** vì thông điệp popup nói về hợp đồng.
- Mỗi request API mobile có thêm **1 truy vấn nhỏ** theo khoá chính `bots.id` (join `bot_slots` / `bot_contracts`); có thể cache theo request nếu thấy tải cao.

### Quy tắc "hết hợp đồng" — tổng hợp để dựng TC boundary

<!-- Suy từ mục ■2 (nguyên văn Dev), gom lại cho dễ đọc. Tester đối chiếu lại code branch trước khi dùng. -->

| Điều kiện | Kết quả mong đợi |
|---|---|
| Hợp đồng hiện tại (`is_active = 1`) có `status = 3` (đã huỷ) | **CHẶN** |
| Không còn hợp đồng `is_active = 1` nào, nhưng có hợp đồng đã huỷ (`status = 3`, `is_active = 0`) | **CHẶN** (bổ sung vòng 2) |
| Gói trả phí quá hạn **> 23 giờ** | **CHẶN** |
| Gói trả phí **chưa thanh toán** | **CHẶN** |
| Gói free quá hạn **1 năm** | **CHẶN** |
| Ngày hết hạn **NULL** | **KHÔNG chặn** (khác web — có chủ đích) |
| Trạng thái gói tăng bạn bè `max_friend_plan` | **KHÔNG chặn** (khác web — có chủ đích) |
| Request **không kèm** `botId` / `bot_id` / `botIdCurrent` | **KHÔNG chặn** (fail-open) |
| Env `ENABLE_PAYPAL` tắt | **KHÔNG chặn** |
| Hợp đồng **chờ chuyển khoản chưa bill** | **KHÔNG chặn** (quy tắc ngày hết hạn/chưa thanh toán chỉ đọc từ hợp đồng đang hiệu lực) |
| API đăng xuất / danh sách tài khoản / thông tin người dùng / thông báo bảo trì | **KHÔNG chặn** (chừa để còn chọn tài khoản khác) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Riêng ticket này**: đã confirm với Dev/PM **bản app Flutter có kèm phần hiển thị popup `contract_expired` hay chưa** — nếu chưa, phần Expect trong file 01 (popup + button `別のアカウントを選択する`) **không test được**, chỉ verify được response HTTP 403 phía API
- [ ] **Riêng ticket này**: đã confirm **danh sách đầy đủ các API được CHỪA** (Dev chỉ mô tả bằng chữ, chưa liệt kê route cụ thể) — cần cho TC verify không chặn nhầm
- [ ] **Riêng ticket này**: đã confirm bằng chứng PHPUnit cho **4 ca test mới của nhánh `status = 3`** (mục VERIFY vẫn còn số cũ 11 tests)
