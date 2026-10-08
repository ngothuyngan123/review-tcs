# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Auto-fixbug (hệ thống, báo cáo 2 lần tại Journal #137967 + #140116/#140117); Assignee ticket Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | **Lần 1** (#137967): `8600ec8ccd` (2 file) — **Lần 2** (#140116): `d01e9e391d` (1 file, gộp chung fix #42041) — không có link PR riêng, chỉ có commit hash + branch nêu trong journal |
| Branch | ⚠️ **2 branch KHÁC NHAU, KHÔNG merge vào nhau**: `sns-line: ai_small_41004` (nhánh gốc `release_step_20260827`, commit `8600ec8ccd`, lần 1) · `sns-line: ai_fixbug_41004` (nhánh gốc `release_step_20260827`, commit `d01e9e391d`, lần 2). Xem cảnh báo chi tiết ở `01-bug-task.md` mục "Ghi chú thêm của Leader". |
| Ngày submit đánh giá | 2026-09-23 (lần 1) · 2026-10-05 (lần 2) |
| Auto-filled | 2026-10-05 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (cả 2 lần fix) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact). **Đặc biệt xác nhận branch nào sẽ dùng để test** trước khi member viết TC.

---

## 1. Nguyên nhân

**Lần 1 (Journal #137967, fix ban đầu cho #41004):** Ở màn nhập thông tin thanh toán của tính năng bán sản phẩm, khi khách mở đường dẫn đổi thẻ/đổi đăng ký mà sản phẩm không còn tồn tại (đã bị xoá), phần xử lý thoát sớm chỉ gửi sang giao diện đúng hai dữ liệu là nội dung lỗi và danh sách loại thẻ, nhưng giao diện vẫn luôn kiểm tra thêm một cờ trạng thái đã đăng ký (`flagCycle`). Cờ này không được gửi nên trang báo lỗi hệ thống thay vì hiện thông báo tiếng Nhật thông thường. Lỗi có từ 2023, chỉ bắn khi khách bấm vào đường dẫn của sản phẩm đã bị xoá.

**Lần 2 (Journal #140116/#140117, relapse của #41004 + bug con #42041):** Màn đổi thẻ thanh toán của sản phẩm định kỳ (`SalesManagementV2Controller::orderChange`) có **nhánh trả về sớm KHÁC** khi không tìm thấy sản phẩm theo mã — nhánh này không được fix lần 1 cover tới. Nhánh vẫn hiển thị giao diện nhập thông tin thanh toán nhưng chỉ truyền 2 biến (danh sách thương hiệu thẻ + thông báo lỗi), vẫn thiếu `flagCycle`. Đây là **lỗi vá thiếu** (patch kế tiếp của 1 lỗi cũ hơn từ commit 2023-07-27 `32d1fb10e8d` — lần đó đã bổ sung biến danh sách thương hiệu thẻ nhưng bỏ sót `flagCycle`). Bug con **#42041** phát sinh cùng lúc rà soát: cùng màn đổi thẻ, khi sản phẩm bị chuyển sang **không công khai** (không phải xoá hẳn) và khách mở đường dẫn (không phải xem trước của admin) thì hệ thống vẫn hiện form đổi thẻ bình thường — thiếu kiểm tra `status_valid`.

## 2. Cách fix

**Lần 1:** Sửa 2 lớp cho màn nhập thông tin thanh toán: (1) nhánh thoát sớm khi sản phẩm không tồn tại/không công khai nay gửi thêm cờ `flagCycle` (giá trị mặc định 0 có sẵn trong hàm) sang giao diện; (2) giao diện lấy cờ đó theo kiểu có giá trị mặc định khi thiếu (`$flagCycle ?? 0`), nên luồng khác nếu quên gửi cũng chỉ hiện thông báo lỗi tiếng Nhật thay vì văng lỗi trắng trang.

**Lần 2 — (1) #41004:** Bổ sung biến `flagCycle` vào mảng biến truyền cho giao diện tại nhánh trả về sớm **của `orderChange`** khi sản phẩm không tồn tại — hết lỗi hệ thống, hiện đúng thông báo lỗi tiếng Nhật.
**Lần 2 — (2) #42041 (bug con, cùng commit `d01e9e391d`):** Thêm kiểm tra `status_valid != 1` trong nhánh không phải preview của `orderChange` → sản phẩm không công khai hiện thông báo lỗi thay vì vẫn hiện form đổi thẻ (giống hành vi màn đổi thẻ bản cũ); chế độ xem trước của admin giữ nguyên.

⚠️ **Dev tự ghi:** view `enter-payment-info.blade.php` dòng 156/162 vẫn dùng `flagCycle` **không bọc kiểm tra tồn tại** → nếu có nhánh early-return mới trong tương lai quên truyền biến, lỗi sẽ **tái diễn lần 3**. Dev không sửa tận gốc (ngoài phạm vi fix tối giản) — để Leader quyết định có yêu cầu bọc kiểm tra tồn tại trong view không.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SalesManagementV2Controller::orderChange` (SalesManagementV2Controller.php:1892-2035) | **Lần 1: không sửa** / **Lần 2: đã sửa (dòng ~1902)** | Nhánh trả về sớm khi sản phẩm không tồn tại — chỗ relapse thực sự nằm ở đây, lần 1 không chạm tới |
| 2 | `SalesManagementV2Controller::orderChange` — nhánh kiểm `status_valid` (dòng ~1922) | **Lần 2: đã sửa [#42041]** | Thêm điều kiện `status_valid != 1` cho nhánh không phải preview |
| 3 | `SalesManagementV2Controller::viewEnterPaymentInfo` (:2163-2283) | Không sửa | Đã truyền đủ `flagCycle` từ trước ở cả 2 lần kiểm tra |
| 4 | `SalesManagementV2Controller::viewEnterFriendInfo` (:2037) | Không sửa | Đã truyền đủ cờ |
| 5 | `SalesManagementV2Controller::confirmOrder` (:2318) | Không sửa | Đã truyền đủ cờ |
| 6 | `SalesManagementV2Controller::orderCancel` (:1799) | Không sửa | Nhánh trả sớm an toàn — giao diện bọc kiểm tra tồn tại đầy đủ (Dev xác nhận ở lần 2) |
| 7 | `SalesManagementController::orderIndex` (SalesManagementController.php:1569) | Không sửa | Đã truyền đủ cờ (bản cũ) |
| 8 | `enter-payment-info.blade.php` (dòng 156, 162) | **Lần 1: đã sửa** (`$flagCycle ?? 0`) | Chỗ PHP ném lỗi — vẫn **không bọc kiểm tra tồn tại** sau cả 2 lần fix, chỉ dựa vào controller luôn truyền đủ |
| 9 | `cancel.blade.php` / `detail.blade.php` / `order_detail.blade.php` | Không sửa | Dev rà soát — mọi biến đều đã bọc kiểm tra tồn tại |
| 10 | `SalesManagementController::orderChange` (bản cũ) + `viewEnterPaymentInfo` [#42041] | Không sửa | Mẫu đối chứng — màn bản cũ đã có cùng thông báo lỗi khi sản phẩm không công khai |
| 11 | `orderCancel` / `changeCardItem` / `changeCardUnivapay` [#42041] | **Không sửa — ghi yokoten** | Không kiểm `status_valid` — Dev chủ động để ngoài phạm vi, chỉ ghi chú theo dõi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SalesManagementV2Controller::orderChange` — nhánh sản phẩm không tồn tại | SalesManagementV2Controller.php | Direct (lần 2) | Relapse của #41004 — nhánh KHÁC với nhánh đã fix lần 1, chỉ nằm trên branch `ai_fixbug_41004` |
| F2 | `SalesManagementV2Controller::orderChange` — nhánh kiểm `status_valid` [#42041] | SalesManagementV2Controller.php | Direct (lần 2, bug con) | Chặn hiện form đổi thẻ khi sản phẩm không công khai (trừ preview admin) — cùng commit `d01e9e391d` |
| F3 | Nhánh thoát sớm (sản phẩm không tồn tại/không công khai) truyền `flagCycle` | SalesManagementV2Controller.php | Direct (lần 1) | Chỉ trên branch `ai_small_41004` — KHÔNG có trên `ai_fixbug_41004` |
| F4 | `enter-payment-info.blade.php` — đọc `flagCycle` có default | resources/views/basic/sales/v2/order/enter-payment-info.blade.php:156,162 | Direct (lần 1) | Chỉ trên branch `ai_small_41004`; nếu test trên `ai_fixbug_41004` thì KHÔNG có default này, chỉ hết lỗi nhờ F1/F2 luôn truyền đủ |
| F5 | `viewEnterPaymentInfo` / `viewEnterFriendInfo` / `confirmOrder` | SalesManagementV2Controller.php | Indirect | Đã truyền đủ cờ từ trước — dùng để đối chứng không bị ảnh hưởng |
| F6 | `orderCancel`, `SalesManagementController::orderIndex` | (tương ứng) | Indirect | Không sửa — giao diện/luồng đã an toàn, dùng đối chứng regression |
| F7 | `orderCancel` / `changeCardItem` / `changeCardUnivapay` [#42041] | (chưa rõ file cụ thể — Dev không ghi) | Không sửa (ghi yokoten) | KHÔNG kiểm `status_valid` — rủi ro tương tự #42041 có thể còn tồn tại ở đây, Dev chủ động để ngoài phạm vi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | Không có | Lần 1 + lần 2 (#41004): chỉ sửa luồng hiển thị/biến truyền view, không đụng dữ liệu/bảng |
| D2 | `s_items.status_valid` [#42041] | READ (chỉ đọc) | Dùng để quyết định hiện form đổi thẻ hay báo lỗi — không ghi/update |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Single Product / Sales (FA-026) — màn nhập thông tin thanh toán & đổi thẻ sản phẩm bán hàng định kỳ: trường hợp sản phẩm **không tồn tại** (đã xoá) | F1, F3, F4 | High — đây là tính năng chính ticket báo, đã fix 2 lần ở 2 nhánh code khác nhau trên 2 branch khác nhau |
| T2 | Single Product / Sales (FA-026) — màn đổi thẻ: trường hợp sản phẩm **không công khai** (bị ẩn, chưa xoá) [#42041] | F2, D2 | High — bug con mới phát hiện cùng lúc rà soát, thay đổi hành vi (trước: vẫn cho đổi thẻ, sau: báo lỗi) |
| T3 | Contract Plan & Payment (FA-031) — khách đang có hợp đồng sản phẩm đã bị ẩn | F2 | Medium — khách KHÔNG tự đổi thẻ qua đường dẫn được nữa khi sản phẩm ẩn (giống hành vi bản cũ). **PO chưa chốt** đây có phải hành vi mong muốn hay không — xem Ghi chú Leader |

### Lưu ý từ Dev (tự review — journal #140116/#140117)

- ⚠️ **2 branch fix KHÔNG merge vào nhau** — `ai_small_41004` (lần 1, có F3/F4) và `ai_fixbug_41004` (lần 2, có F1/F2). Mỗi branch chỉ có 1 trong 2 lần fix. Dev tự nhận: test trên branch sai sẽ KHÔNG thấy đủ cả 2 lần fix.
- ⚠️ **Test Studio hiện đang dựng test từ `ai_small_41004`** — branch này KHÔNG có commit #42041 và KHÔNG có fix relapse F1. Phải trỏ Test Studio sang `ai_fixbug_41004` để retest thấy đủ fix lần 2 + #42041.
- ⚠️ View `enter-payment-info.blade.php` vẫn dùng `flagCycle` không bọc kiểm tra tồn tại (ngoài nhánh đã fix lần 1) — rủi ro tái diễn lần 3 nếu có nhánh early-return mới trong tương lai quên truyền biến.
- ⚠️ #42041 — PO chưa chốt có nên chặn đổi thẻ khi sản phẩm ẩn (T3) hay không — cần xác nhận với PO trước khi chốt expected result cho TC liên quan T3.
- ⚠️ F7 (`orderCancel` / `changeCardItem` / `changeCardUnivapay`) được Dev ghi "yokoten" (ghi nhận để theo dõi) nhưng **chưa sửa** — có thể còn lỗi tương tự #42041 (thiếu kiểm `status_valid`) nhưng nằm ngoài phạm vi 2 lần fix này.
- Dev lần 2 **không tái hiện được qua web dev** (`host.docker.internal:8000` không truy cập được lúc verify) — chỉ verify bằng compile Blade + chạy thật phần view qua harness, KHÔNG phải test end-to-end trên môi trường thật.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — **đặc biệt đã hiểu rõ đây là 2 lần fix trên 2 nhánh code riêng biệt**
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót, đặc biệt F7 chưa sửa)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] **Đã xác nhận với Dev/Leader branch nào sẽ dùng để test** (`ai_small_41004` hay `ai_fixbug_41004` hay 1 branch gộp cả 2) — KHÔNG tự chọn
- [ ] **Đã xác nhận với PO** hành vi T3 (chặn đổi thẻ khi sản phẩm ẩn) có đúng mong muốn không
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
