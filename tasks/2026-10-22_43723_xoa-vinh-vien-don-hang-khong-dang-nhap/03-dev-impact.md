# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (dev handoff tự động — journal #146588/#146628/#146867/#147158; `issue.assigned_to` không có) |
| Commit / Pull Request | `<chưa có link PR>` — commit cuối `71a1069fdbc99d94f7389b8568cca1a9ba8c3d0e` (web, vòng chốt) |
| Branch | `ai_studio_fixbug_43723` (nhánh gốc `release_step_20260930_v2` @`4ae243379f82`) |
| Ngày submit đánh giá | `2026-10-22` (4 journal cùng ngày: 10:33 → 14:17 → 17:15) |
| Auto-filled | `2026-10-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

⚠️ **Dùng vòng cuối (journal #147158, 17:15) làm nội dung chính thức** cho 4 mục dưới đây — đây là bản đã gộp đủ các lớp bảo vệ sau 3 vòng vá trước (xem tóm tắt diễn biến ở `01-bug-task.md` → "Ghi chú thêm của Leader"). TC KHÔNG được viết theo hành vi của V1/V2 (đã lỗi thời).

---

## 1. Nguyên nhân

Bản giao v2 (V1/V2 ở các journal trước) chỉ dùng mã PaymentIntent (`charge_id`) làm bằng chứng chủ đơn. Endpoint xoá không gắn request với trình duyệt đã tạo đơn, nên **ai biết đúng id + đúng mã `charge_id` là xoá được, không cần cookie hay token của chính người mua** — đây là lỗ hổng cốt lõi còn sót lại sau 2 vòng vá trước.

Ngoài ra còn 3 lỗi phụ của cùng hàm (phát hiện khi rà lại ở vòng chốt):
- Hai lệnh xoá đơn và xoá hợp đồng (đơn định kỳ) không nằm trong một transaction → có thể xoá dở 1 trong 2 khi lỗi DB giữa 2 lệnh.
- Khi lỗi, nhánh `catch` ghi nguyên message của `QueryException` (có câu SQL kèm giá trị, bao gồm mã PaymentIntent) vào log và tin Chatwork.
- Middleware `TrimStrings` toàn app cắt khoảng trắng mọi tham số trước khi vào controller, trong khi controller so khớp `charge_id` nguyên văn → đúng mã nhưng dính khoảng trắng đầu/cuối vẫn xoá được (bug con `#3753`/`#43948`, Dev kết luận **không phải lỗi phân quyền** vì vẫn đòi đúng mã, nhưng vẫn sửa để nhất quán 400/403).

## 2. Cách fix

- **Màn xác nhận mua sản phẩm** (Stripe, `confirm-order`): response của bước tạo `payment-intent` trả thêm `deleteToken`; khi 3DS thất bại, JS gửi kèm `cycleId`, `orderId`, `charge_id`, `delete_token` khi yêu cầu xoá đơn tạm. Giao diện không đổi.
- **API `POST /ajax/items/delete-order-confirm-fail`**: bắt buộc `delete_token` đúng của `orderId` **trong session trình duyệt đã tạo đơn** (dùng 1 lần, sống 30 phút). Không cookie, không token, token sai, token của đơn khác, hết hạn hoặc dùng lại ⇒ **403** 「このデータを操作する権限がありません。」 và **không đụng DB**.
- Cùng API: token đúng nhưng mã PaymentIntent/`cycleId` sai hoặc đơn đã chốt ⇒ **403**; `orderId`/`cycleId` sai định dạng (kể cả có khoảng trắng) ⇒ **400**; lỗi hệ thống ⇒ **500**.
- Cùng API, đơn định kỳ: lệnh xoá đơn hàng và xoá hợp đồng chạy trong **một transaction** — một trong hai không xoá được (0 dòng hoặc lỗi DB) thì **giữ nguyên cả hai**.
- Cùng API, lỗi 500: log và tin Chatwork **chỉ** chứa id đơn, id hợp đồng và thông báo lỗi gốc rút gọn — **không còn** câu SQL, mã PaymentIntent hay token.
- Middleware `TrimStrings`: loại trừ riêng path `ajax/items/delete-order-confirm-fail` (mọi endpoint khác vẫn cắt khoảng trắng như cũ).

**10 bug con QA/automation phát hiện ở vòng trước, đã fix ở vòng chốt** (commit `71a1069fdbc9`, một phần chung commit `982f55d3dfe6` của V1):
| Bug | Nội dung | Kết luận |
|---|---|---|
| `#43948` | `TrimStrings` không cắt khoảng trắng cho endpoint này: `orderId=" 3528"` ⇒ 400, `charge_id=" C7 "` ⇒ 403, đơn còn nguyên. Endpoint khác vẫn cắt. | Đã sửa |
| `#43949` | Rule dự án cấm nhánh fix bug tự bump `sns-line.version` | **Không đổi code** — đội release tự bump khi phát hành |
| `#43950` | Log/Chatwork lỗi DB dùng message gốc (bỏ câu SQL), che mã PaymentIntent, cắt 200 ký tự | Đã sửa |
| `#43952` | Xoá cần thêm `delete_token` dùng 1 lần, gắn session trình duyệt đã tạo đơn | Đã sửa |
| `#43955` | Xoá đơn + hợp đồng trong 1 transaction; lỗi DB khi xoá hợp đồng ⇒ 500, cả hai còn nguyên | Đã sửa |
| `#43956` | Đơn 1 lần: không cookie/token ⇒ 403; cookie đúng + `delete_token` đúng ⇒ 200 | Đã sửa |
| `#43957` | Đơn định kỳ: không cookie/token ⇒ 403 (đơn + hợp đồng còn); token đúng ⇒ 200 xoá cả hai trong 1 transaction | Đã sửa |
| `#43958` | Biết mã PaymentIntent người khác nhưng không có session/token của họ ⇒ 403; token đúng mà mã sai/rỗng/khác hoa thường/mảng/khoảng trắng ⇒ 403 | Đã sửa |
| `#43959` | Thiếu token ⇒ 403 ở tầng xác thực; token đúng mà `cycleId` không khớp hợp đồng ⇒ 403 | Đã sửa |
| `#43960` / `#43961` | Màn xác nhận gửi thêm `delete_token` từ response payment-intent; cần hard-reload để nạp JS mới; JS cũ (không token) ⇒ 403, đơn tạm còn tới khi job dọn | Đã sửa |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Bước tạo đơn tạm `payment-intent` (Sales) | Có — response thêm field `deleteToken` | Nguồn phát token cho bước xoá |
| 2 | `deleteOrderPaymentError()` (xoá đơn khi Stripe lỗi ngay lúc tạo payment-intent) | Không | Dev đã check, không đi qua endpoint/token mới, giữ hành vi cũ |
| 3 | Job `recover:payment_univapay_timeout` (dọn đơn tạm treo ~15-20 phút) | Không | Không đổi code, vẫn là nơi dọn đơn tạm JS cũ/token hết hạn không xoá được |
| 4 | Các endpoint khác nhận `charge_id` có khoảng trắng (màn hoàn tiền admin, đăng nhập…) dùng chung middleware `TrimStrings` | Không | Dev đã check, chỉ loại trừ đúng 1 path `ajax/items/delete-order-confirm-fail`, các endpoint khác vẫn cắt khoảng trắng như cũ |
| 5 | `notifyChatworkException` (helper dùng chung gửi cảnh báo Chatwork) | Không (ghi nhận follow-up riêng) | Dev lưu ý Guzzle không có timeout (mặc định chờ vô hạn) — nếu Chatwork bị treo thì request chờ theo; Dev xếp vào ticket khác, không thuộc phạm vi #43723 |
| 6 | Trial `amount=0` (SetupIntent) và thanh toán UnivaPay | Không | Không đi qua endpoint/token mới, hành vi giữ nguyên |
| 7 | 3 endpoint `delete-*-confirm-fail` còn lại (Lesson, Salon, Event) | **Không** — ngoài phạm vi nhánh này | Phụ thuộc nhánh riêng (`#42413` Event; chọn 1 trong `#42436`/`#43402` cho Salon/Lesson) — vẫn còn lỗ hổng gốc tới khi các nhánh đó release |

Ghi chú thêm của Dev (quan trọng cho TC):
- `tests/Feature/SalesDeleteOrderConfirmFailTest.php` (626 dòng, phủ ma trận đủ các trường hợp) + `tests/Unit/TrimStringsExceptPathTest.php` (71 dòng, mới) — Dev đã chạy pass trên base.
- `tests/Feature/ContractExpireServiceTest.php` (test có sẵn, không liên quan) gây PHP fatal làm dừng cả bộ PHPUnit (thiếu method mới của `BotRepositoryInterface`) — Dev ghi nhận cần sửa ở ticket riêng, **không chặn** việc merge nhánh này.
- Migration / thay đổi dữ liệu: **không có** (Dev đã kiểm diff).
- Recover dữ liệu: **không cần** — nhánh task chưa phát hành; dữ liệu bị xoá trong các lượt QA là dữ liệu test local; lỗ hổng gốc trên production được đánh giá ở vòng V1 (xoá cứng không để lại dấu vết DB, chưa có báo cáo mất đơn thật) — Recover data không áp dụng cho task này.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Hàm xoá đơn tạm theo `charge_id` + `delete_token` (đơn 1 lần) | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | Thêm bắt buộc `delete_token`, trả 403/400/500 theo đúng điều kiện |
| F2 | Hàm xoá đơn + hợp đồng tạm trong transaction (đơn định kỳ) | `app/CycleOrderHistory.php` | Direct | Gộp 2 lệnh xoá order + cycle order vào 1 transaction |
| F3 | Route `POST /ajax/items/delete-order-confirm-fail` | `routes/web.php` (không đổi route, đổi controller) | Indirect | Vẫn public (không login, miễn CSRF) — bảo vệ chuyển hẳn sang `delete_token` |
| F4 | Bước tạo `payment-intent` — phát `deleteToken` | `SalesManagementV2Controller.php` (hàm tạo payment-intent) | Direct | Response thêm field mới; lưu token vào session (`salesPendingOrderDeleteTokens`) |
| F5 | `confirm-order.js` (JS màn xác nhận mua) | `public/js/sales/v2/confirm-order.js` | Direct | Gửi thêm `cycleId`, `orderId`, `charge_id`, `delete_token` khi 3DS thất bại |
| F6 | Middleware `TrimStrings` — danh sách loại trừ | `app/Http/Middleware/TrimStrings.php` | Direct | Thêm đúng 1 path ngoại lệ `ajax/items/delete-order-confirm-fail` |
| F7 | Log + `notifyChatworkException` ở nhánh lỗi 500 của hàm xoá | `SalesManagementV2Controller.php` | Direct | Rút gọn message, che mã PaymentIntent/SQL trước khi ghi log/Chatwork |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_order_history` (đơn 1 lần, `status_webhook=3` pending) | DELETE (có điều kiện) | Chỉ xoá khi `delete_token` + `charge_id` khớp đúng đơn, đơn chưa chốt |
| D2 | `s_cycle_order_history` (hợp đồng định kỳ tạm) | DELETE (có điều kiện, cùng transaction với D1 khi là đơn định kỳ) | Không xoá lẻ 1 trong 2 |
| D3 | Session trình duyệt — key mới `salesPendingOrderDeleteTokens` (cạnh `stripeCustomerV2`) | CREATE | Lưu token theo từng đơn, dùng 1 lần, hết hạn sau 30 phút; nhiều tab mua nhiều sản phẩm = nhiều token |
| D4 | Log app (dòng lỗi `deletePaymentOrderConfirmFail error`) | UPDATE (nội dung message) | Đã bỏ câu SQL, che mã PaymentIntent, cắt 200 ký tự |
| D5 | Tin nhắn room Chatwork lỗi của team | CREATE (khi lỗi 500) | Chỉ còn id đơn, id hợp đồng, message rút gọn — không còn mã PaymentIntent/SQL/token |

Migration / thay đổi dữ liệu: **không có** (Dev đã kiểm diff).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Endpoint `POST /ajax/items/delete-order-confirm-fail` (bảo mật: xoá đơn tạm Sales theo đúng chủ đơn) | F1, F2, F3, F6, F7 | **High** — mục tiêu chính của fix, phải verify đủ ma trận 200/400/403/500 + transaction + log/Chatwork che mã |
| T2 | Màn xác nhận mua sản phẩm Stripe (1 lần + định kỳ, 3DS thất bại/thành công/không cần 3DS) | F4, F5 | **High** — JS cũ (chưa hard-reload) vẫn phải nhận 403 an toàn, JS mới phải gửi đủ token |
| T3 | Tồn kho sản phẩm (đơn tạm sót do JS cũ/token hết hạn/lỗi 500 không xoá được) | D1, D2 | **Medium** — chiếm tồn kho tới khi job dọn (~15-20 phút), hàng định kỳ có thể chặn mua lại |
| T4 | Job `recover:payment_univapay_timeout` (dọn đơn tạm sót) | D1, D2 (không đổi code job) | **Low** — không đổi code nhưng là lưới an toàn cuối cho mọi case 403/500 |
| T5 | Các endpoint khác dùng chung middleware `TrimStrings` (form/API nhận tham số có khoảng trắng — hoàn tiền admin, đăng nhập…) | F6 | **Medium** — regression risk nếu loại trừ path sai phạm vi; phải verify các endpoint khác vẫn cắt khoảng trắng như cũ |
| T6 | Room Chatwork báo lỗi team | D5, F7 | **Low** — chỉ đổi nội dung tin, không đổi luồng |
| T7 | Trial `amount=0` (SetupIntent), thanh toán UnivaPay | Không chạm (xác nhận ở mục 3) | **Low** — cần 1 TC regression xác nhận hành vi không đổi |
| T8 | **[Ngoài phạm vi nhánh #43723]** 3 endpoint `delete-*-confirm-fail` còn lại — Lesson (`Mobile/CalendarController.php`), Salon (`Mobile/CalendarSalonController.php`), Event (`MobileEventBookingController.php`) | Dev xác nhận chưa sửa, phụ thuộc nhánh khác | **High (tồn đọng)** — vẫn còn lỗ hổng gốc giống Sales trước fix; không viết TC verify-fix ở task này, chỉ flag GAP/risk tồn đọng chờ leader chọn nhánh (`#42413`, `#42436`/`#43402`) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Riêng task này**: đã quyết định phạm vi test cho T8 (3 endpoint Lesson/Salon/Event ngoài phạm vi nhánh) — chỉ theo dõi GAP hay mở task review riêng khi nhánh `#42413`/`#42436`/`#43402` release
