# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #34422 journal **#133049** (AI LME Fix bug, 2026-08-26). Journal #132275 (2026-08-21, nội dung chỉ `Feature #33909`) không có giá trị điều tra — bỏ qua.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME, không có dev người cụ thể đứng tên) |
| Commit / Pull Request | `e31f3f8fe2` (1 file) — không có link PR trong Redmine |
| Branch | `ai_fixbug_34422` (nhánh gốc `release_step_20260805`), repo `sns-line` — đã push |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-10-07 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=72e326f5-f8d5-4381-960f-2614eed18b7b |
| Mức verify của Dev | `lint` — `php -l` trên file view + biên dịch Blade (Illuminate BladeCompiler) rồi `php -l` bản compile + kiểm cú pháp/hành vi biểu thức Vue bằng `node new Function` (4 tổ hợp dữ liệu). **KHÔNG verify được trên dữ liệu dev** (MySQL `host.docker.internal:3306` từ chối kết nối tại thời điểm điều tra) — **CHƯA có verify trên UI thật**. |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn:

Màn danh sách hợp đồng vẽ 2 dòng cho cùng 1 hợp đồng: dòng gói chính và dòng phí theo số bạn bè, cả hai đều lấy phương thức thanh toán từ cùng một bản ghi hợp đồng. Nhưng ô Phương thức thanh toán của 2 dòng lại đọc theo 2 quy tắc khác nhau: dòng gói chính ưu tiên trường lưu phương thức cũ (phương thức đang thực sự có hiệu lực, vì đổi sang thẻ chỉ áp dụng từ kỳ thanh toán kế tiếp), còn dòng phí theo số bạn bè chỉ đọc phương thức mới nên hiện ngay thẻ. Do đó sau khi đổi từ chuyển khoản sang thẻ thành công, 2 dòng của cùng một hợp đồng hiển thị mâu thuẫn nhau. Ô này của dòng phí theo số bạn bè được viết lại thiếu nhánh phương thức cũ khi bảng bị tách làm 2 mẫu hiển thị.

## 2. Cách fix

> Nguyên văn:

Sửa ô Phương thức thanh toán của dòng phí theo số bạn bè trong màn danh sách hợp đồng (`resources/views/basic/bill/index.blade.php`) để dùng đúng thứ tự ưu tiên như dòng gói chính và như màn chi tiết hợp đồng: lấy phương thức cũ đang có hiệu lực trước, không có mới lấy phương thức hiện tại; 4 số cuối thẻ cũng lấy theo đúng phương thức đang hiển thị. Chỉ sửa hiển thị, không đụng logic thu tiền. Quét ngang thấy màn chi tiết phí theo số bạn bè cũng còn đọc phương thức mới nhưng nằm ngoài phạm vi ticket nên chỉ ghi nhận.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Ô Phương thức thanh toán dòng **gói chính** — `resources/views/basic/bill/index.blade.php:573-608` | Không sửa | Baseline đối chiếu — đã dùng đúng thứ tự ưu tiên phương thức cũ |
| 2 | Ô Phương thức thanh toán dòng **phí theo số bạn bè** — `resources/views/basic/bill/index.blade.php:847-871` | **Sửa** — thêm nhánh ưu tiên phương thức cũ + 4 số cuối thẻ theo phương thức đang hiển thị | Đây là nơi phát sinh bug |
| 3 | Ô Gói sử dụng dòng phí theo số bạn bè — `resources/views/basic/bill/index.blade.php:752-761` | Không sửa | Đối chiếu — đã dùng kỳ thanh toán cũ, chủ ý tương tự |
| 4 | `ListPageController::getDataContract` — `app/Http/Controllers/V2/Bill/ListPageController.php:300-440` | Không sửa | Dựng dòng phí theo số bạn bè bằng **clone** bản ghi hợp đồng → đã sẵn 2 trường phương thức cũ, không cần sửa backend |
| 5 | `PointSettingController::changeCard` — `app/Http/Controllers/PointSettingController.php:1273-1281` | Không sửa | Ghi phương thức cũ khi chưa thu tiền ngay |
| 6 | `PointSettingController::changePaymentMethod` — `app/Http/Controllers/PointSettingController.php:518-519` | Không sửa | Ghi phương thức cũ chiều ngược lại (card → transfer) |
| 7 | `AutoPaymentJobUnivapay` — `app/Console/Commands/AutoPaymentJobUnivapay.php:159,567,934` | Không sửa | Xoá phương thức cũ **sau khi** thu tiền thành công bằng phương thức mới |
| 8 | `HandleBillMaxFriend::handleCardBilling` / `handleTransferBilling` — `app/Console/Commands/HandleBillMaxFriend.php:64-95,318-330` | Không sửa | Đối chiếu phương thức dùng để **thu phí** theo số bạn bè — job này thu theo phương thức **MỚI** (xem mâu thuẫn ở mục rủi ro) |
| 9 | Màn chi tiết hợp đồng — `resources/views/basic/bill/detail.blade.php:188-191` | Không sửa | Nguồn đối chiếu quy ước hiển thị (phương thức cũ + ghi chú ngày hiệu lực) |
| 10 | `isContractWaitingTransferMaxFriend` — `public/_assets/modules/bill/js/index.js:816-818` | Không sửa | Điều kiện ẩn/hiện ô Phương thức thanh toán của dòng phí theo số bạn bè |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Hiển thị ô Phương thức thanh toán — dòng phí theo số bạn bè | `resources/views/basic/bill/index.blade.php` (3 dòng, khu vực ~847) | Direct | Đổi từ chỉ đọc `payment_method` sang ưu tiên `payment_method_old` rồi mới `payment_method`; 4 số cuối thẻ lấy theo phương thức đang hiển thị |

**File thay đổi (mục 4.1 nguyên văn của Dev):**
- `resources/views/basic/bill/index.blade.php`

### 4.2. List data bị update khi fix bug

<!-- Dev khẳng định không có data bị update — chỉ sửa hiển thị (view), không ghi/không đổi dữ liệu, không đụng backend/query/job/DB. -->

**Recover data**: ✔ Dev khẳng định **không cần recover data**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Contract Plan & Payment (FA-031)** — ô Phương thức thanh toán ở dòng phí theo số bạn bè trên màn danh sách hợp đồng hiển thị đúng phương thức đang có hiệu lực, đồng bộ với dòng gói chính và màn chi tiết hợp đồng | F1 | Medium — fix hiển thị thuần (không đụng DB/job/thu tiền), nhưng vùng chạm là cột enum nhiều tổ hợp trạng thái + 1 điểm **chưa chốt hướng nghiệp vụ** (xem rủi ro bên dưới) |

---

## Rủi ro / lưu ý khi test (nguyên văn Dev — "TỰ REVIEW (AI)")

- **Điểm cần người review chốt hướng**: khoản phí theo số bạn bè trên thực tế được **job thu theo phương thức MỚI** của hợp đồng (`HandleBillMaxFriend` lọc theo `bot_contracts.payment_method`), nên có cách hiểu **ngược lại** là dòng phí theo số bạn bè hiện thẻ mới mới đúng, còn dòng gói chính mới sai. Dev đã chọn hướng **đồng bộ về dòng gói chính** (hiển thị phương thức cũ) vì: (a) đó là hành vi chủ ý thêm từ 2026-01-14 (commit `f5b366217e`) và màn chi tiết hợp đồng cũng hiển thị như vậy kèm ghi chú ngày hiệu lực; (b) ô này chỉ hiện khi khoản phí max-friend đã thanh toán/đang lỗi, không phải khoản sắp thu. **Nếu PM muốn hướng ngược lại thì chỉ cần revert đúng 3 dòng đã sửa.**
- **Không tái hiện được trên môi trường dev** (MySQL từ chối kết nối) nên Dev chỉ verify bằng lint + biên dịch Blade + kiểm biểu thức Vue — **cần tester dựng lại kịch bản đổi phương thức khi hợp đồng còn hạn để xác nhận trên giao diện thật**.
- Không bump số version tài nguyên tĩnh theo rule (cấm bump version), nhưng thay đổi nằm ở file view (server render) nên không dính cache trình duyệt — chỉ cần tải lại trang.
- Quét ngang thấy **màn chi tiết hợp đồng, phần phí theo số bạn bè** cũng còn đọc phương thức mới (cùng kiểu bug) nhưng Dev xác định **ngoài phạm vi ticket 34422** — chỉ ghi nhận, không fix.

**Bằng chứng (mục 6. VERIFY của Dev):**
- Lịch sử git: nhánh hiển thị phương thức cũ được thêm ngày 2026-01-14 (commit `f5b366217e`) cho ô Phương thức thanh toán khi bảng còn 1 mẫu hiển thị; ngày 2026-02-08 commit `2aaddb1824` tách bảng thành 2 mẫu và ô của dòng phí theo số bạn bè bị viết lại chỉ còn 2 nhánh, mất nhánh phương thức cũ. Ticket được tạo 2026-02-11, ngay sau đó.
- Màn chi tiết hợp đồng (`detail.blade.php:188`) dùng đúng thứ tự ưu tiên phương thức cũ trước và có ghi chú ngày phương thức mới bắt đầu áp dụng — xác nhận đây là quy ước hiển thị chủ ý, không phải lỗi của dòng gói chính.
- Truy vấn dựng danh sách `select bot_contracts.*` nên dòng phí theo số bạn bè (clone bản ghi hợp đồng) đã có sẵn 2 trường phương thức cũ và 4 số cuối thẻ cũ, không cần sửa backend.
- Ô Phương thức thanh toán của dòng phí theo số bạn bè chỉ hiện khi khoản phí đó **KHÔNG** ở trạng thái chờ chuyển khoản, tức khoản đã thanh toán hoặc đang lỗi — nên hiển thị phương thức đang có hiệu lực là phù hợp.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Đã chốt hướng nghiệp vụ**: hiển thị theo phương thức CŨ (đồng bộ dòng gói chính) hay theo phương thức MỚI (đồng bộ với thực tế job `HandleBillMaxFriend` thu tiền)? — xem mâu thuẫn ở mục rủi ro.
- [ ] **Đã hỏi Dev**: màn chi tiết hợp đồng, phần phí theo số bạn bè (ngoài phạm vi ticket) — có cần raise ticket riêng không?
