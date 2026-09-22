# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `521f738f02` (5 file) — Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=96a90258-45fa-475e-a778-f917b259fa28 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40806 |
| Branch | `ai_fixbug_40806` (repo `sns-line`, nhánh gốc `release_step_20260827`, đã rebase lên tip `be4cbf0930`) — **đã push** |
| Ngày submit đánh giá | 2026-09-14 (Journal #136321) — Commit Date custom field: 2026-09-14 |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trang đăng ký sự kiện trên LIFF gồm nhiều bước nằm CÙNG một trang, đổi bước bằng `v-show` nên trình duyệt không tự cuộn lại. Việc cuộn lên đầu mỗi lần đổi bước làm bằng cách gán anchor `#top` — nhưng **từ lần đổi bước thứ 2 trở đi hash đã trùng nên lệnh này KHÔNG còn tác dụng**.

Hậu quả: bấm nút chuyển sang màn xác nhận thì nội dung đổi nhưng vị trí cuộn vẫn ở đáy form, khách không thấy dòng 「まだ予約は完了していません」 lẫn nút đăng ký thật ở phía trên nên tưởng đã xong. Bấm nút quay lại thì trình duyệt khôi phục vị trí cuộn về đầu trang, màn xác nhận mới lộ ra, khách bấm nút đăng ký và lúc đó đơn mới thực sự được ghi — **đúng cả 3 chi tiết khách kể**.

Log production xác nhận: 12GB app log không có lỗi server nào, và request đăng ký của các khách bị ảnh hưởng **CHƯA BAO GIỜ tới server** (access log 3 ngày, 0 request đăng ký từ IP của họ) — tức không có dữ liệu nào bị mất, họ chưa hoàn tất bước cuối.

**Cùng nhóm lỗi âm thầm**: hàm chuyển bước có thể ném lỗi ở đoạn đọc giá trị field tên/email (sự kiện không bật 2 field này thì trả về rỗng) và Vue nuốt lỗi vào console, nên lệnh cuộn đặt ở CUỐI hàm cũng mất luôn.

## 2. Cách fix

1. **Bỏ cơ chế cuộn bằng anchor**: thêm hàm cuộn lên đầu chạy trong `nextTick` của Vue rồi thay **toàn bộ 15 chỗ gán `#top`** (6 trong file JS, 9 trong nút bấm của giao diện).
2. Trong hàm chuyển sang màn xác nhận (`confirmOrder`): đưa lệnh cuộn lên **NGAY sau khi đổi bước** (trước mọi câu lệnh có thể ném lỗi); đọc field tên/email theo kiểu an toàn (guard `objName`/`objEmail`) để không còn ném lỗi khi sự kiện không bật 2 field đó; **bỏ câu cảnh báo chọn ngày giờ đặt sai chỗ ở cuối hàm**.
3. **Sửa 2 chỗ báo lỗi câm**: (a) chưa tích đồng ý điều khoản thì cuộn tới dòng báo đỏ; (b) nhánh thất bại khi lấy thông tin friend (`getFriendInfo.fail`) bật lại nút + báo lỗi thay vì để nút xám vĩnh viễn.
4. **Thêm beacon lỗi JS phía khách**: bắt `window.onerror`, promise bị bỏ rơi và Vue `errorHandler` rồi POST về endpoint mới; server ghi log và báo Chatwork phòng `100533944` (chặn lặp 10 phút cho cùng một lỗi, giới hạn 5 báo mỗi lượt vào trang, gọi Chatwork có timeout + thử lại cho lỗi tạm thời).

> **ĐÃ GỠ theo yêu cầu human**: toàn bộ fix lượt trước (chốt chặn không báo thành công khi không tạo được bản ghi + đổi cờ kết quả khi sự kiện không tồn tại ở `payment`/`changeBooking` + đổi nhánh báo lỗi của giao diện) — giả thuyết đó đã bị log production bác bỏ nên không thuộc phạm vi ticket.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `confirmOrder` — `public/js/booking_event_day/order-item.js` | Đưa lệnh cuộn lên ngay sau khi đổi bước; guard `objName`/`objEmail`; xóa khối cảnh báo 「予約日時を選択してください。」 thừa ở cuối hàm | Hàm chuyển sang màn xác nhận — điểm phát sinh bug gốc |
| 2 | `scrollToTop` — `order-item.js` | **Hàm mới** — cuộn lên đầu trong `nextTick` của Vue | Thay cơ chế anchor `#top` |
| 3 | `validateFriend` — `order-item.js` | Chưa tick 利用規約 → cuộn tới dòng báo đỏ | Sửa lỗi báo câm |
| 4 | `getFriendInfo` — `order-item.js` | Nhánh `.fail` bật lại nút + hiện thông báo lỗi | Sửa nút xám vĩnh viễn |
| 5 | `changePageBooking` / `changePageCancel` / `loadFormPayment` — `order-item.js` | Thay gán `#top` → gọi `scrollToTop()` | Caller dùng chung cơ chế cuộn (luồng đổi lịch / hủy / thanh toán) |
| 6 | `Vue.config.errorHandler` — `order-item.js` | Bắt lỗi Vue → gửi beacon | Trước đó Vue nuốt lỗi vào console |
| 7 | `MobileEventBookingController::reportJsError` — `app/Http/Controllers/Basic/MobileEventBookingController.php` | **Endpoint mới** — nhận báo lỗi JS, ghi log, gọi Chatwork | Thu thập bằng chứng trực tiếp cho lần sau |
| 8 | `notifyChatworkJsError` — `app/Helpers/functions.php` | **Helper mới** — gửi Chatwork phòng `100533944`, timeout 5s, retry 3 | Kênh cảnh báo lỗi JS |
| 9 | `reportBookingEventJsError` + **9 nút `@click`** — `resources/views/basic/booking_event_day/order/index.blade.php` | Thay 9 chỗ gán `#top` → `scrollToTop()`; thêm hàm gửi beacon (MAX_REPORT=5, dedup) | 9/15 điểm đổi bước nằm trong blade |
| 10 | `routes/web.php` | Thêm route `POST /ajax/booking-event/report-js-error` (miễn CSRF) | Đăng ký endpoint mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev không kê theo format F1/F2 — bảng dưới đây map từ mục 4.1 "File thay đổi" + mục 3 của Dev. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `scrollToTop()` + 15 điểm gọi (6 JS + 9 blade) | `public/js/booking_event_day/order-item.js`, `resources/views/basic/booking_event_day/order/index.blade.php` | Direct | **Hàm dùng chung** — blast radius phủ cả luồng đặt mới, đổi lịch, hủy, thanh toán, lịch sử, điều khoản |
| F2 | `confirmOrder()` | `order-item.js` | Direct | Thứ tự lệnh đổi + guard name/email + xóa alert thừa |
| F3 | `validateFriend()` | `order-item.js` | Direct | Cuộn tới lỗi khi chưa tick 利用規約 |
| F4 | `getFriendInfo()` nhánh fail | `order-item.js` | Direct | Bật lại nút + thông báo lỗi |
| F5 | `changePageBooking()` / `changePageCancel()` / `loadFormPayment()` | `order-item.js` | Direct | Đổi từ anchor sang `scrollToTop()` |
| F6 | `Vue.config.errorHandler` | `order-item.js` | Direct | Bắt lỗi Vue → beacon |
| F7 | `MobileEventBookingController::reportJsError` | `app/Http/Controllers/Basic/MobileEventBookingController.php` | Direct (mới) | Endpoint mới, miễn CSRF |
| F8 | `notifyChatworkJsError()` | `app/Helpers/functions.php` | Direct (mới) | Gọi Chatwork đồng bộ trong request |
| F9 | Route `POST /ajax/booking-event/report-js-error` | `routes/web.php` | Direct (mới) | |
| F10 | **Hành vi nút Back của LINE** (system Back) | — (hệ quả của F1) | Indirect | **ĐỔI HÀNH VI**: URL không còn `#top` → Back của LINE **thoát LIFF** thay vì cuộn trang |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Dev ghi rõ: không thêm/sửa bảng nào |
| D2 | App log (file log) | CREATE | Endpoint `reportJsError` ghi log lỗi JS |
| D3 | Chatwork phòng `100533944` | CREATE (gửi tin ngoài) | Thông báo lỗi JS — throttle 10 phút/cùng lỗi, max 5 báo/lượt vào trang |

> **RECOVER DATA**: ✔ Không cần recover data (Dev xác nhận không có đơn hỏng/mồ côi).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Event Booking (FA-021)** — trang đăng ký sự kiện trên LIFF: cuộn lên đầu đúng ở mọi lần đổi bước, báo lỗi rõ thay vì im lặng, có beacon lỗi JS về Chatwork | F1, F2, F3, F4, F6 | **High** — Dev tự kê |
| T2 | Luồng **đổi lịch đặt chỗ** (予約内容変更) trên LIFF | F1, F5 | **High** — dùng chung `scrollToTop()`, Dev yêu cầu "test lại đủ 8 bước" |
| T3 | Luồng **hủy đặt chỗ** (キャンセル) trên LIFF | F1, F5 | **High** — dùng chung `scrollToTop()` |
| T4 | Luồng **thanh toán** event booking (`loadFormPayment`, màn thẻ, 特定商取引法に基づく表記) | F1, F5 | **High** — dùng chung `scrollToTop()`, Dev nêu rõ "cả luồng đổi lịch và luồng thanh toán" |
| T5 | Màn **lịch sử đặt chỗ / chi tiết 開催情報** trên LIFF | F1 | Medium — nằm trong 15 điểm scroll |
| T6 | **Điều hướng LIFF ↔ LINE** (nút Back hệ thống) | F10 | **High** — đổi hành vi, cần báo QA + có thể ảnh hưởng UX toàn trang |
| T7 | Endpoint báo lỗi JS + kênh Chatwork | F7, F8, F9, D2, D3 | Medium — tự cô lập trong try/catch, nhưng gọi Chatwork **đồng bộ** trong request |

---

## Rủi ro / lưu ý khi test (Dev tự nêu — mục TỰ REVIEW)

- ⚠️ **ĐỔI HÀNH VI cần báo QA**: sau fix URL không còn thêm `#top` nữa, nên bấm **nút quay lại của LINE sẽ THOÁT LIFF** thay vì chỉ cuộn trang như trước.
- ⚠️ Thay đổi cuộn trang áp cho **TẤT CẢ 15 điểm đổi bước** (cả luồng đổi lịch và luồng thanh toán) → phải test lại **đủ 8 bước**, trên **cả iOS và Android LINE**.
- ⚠️ **Chưa tái hiện được bug gốc trên thiết bị thật**, mức verify dừng ở lint + compile blade. Plan ghi rõ root cause là **giả thuyết khớp nhất với toàn bộ dữ kiện chứ chưa phải bằng chứng trực tiếp** — beacon lỗi JS chính là để lần sau có bằng chứng trực tiếp.
- ⚠️ Beacon **gọi Chatwork đồng bộ trong request**. Đã chặn lặp 10 phút + giới hạn 5 báo/lượt vào trang + timeout 5s; nếu backendapi chậm thì endpoint `report-js-error` chậm theo (không ảnh hưởng luồng đăng ký vì là request nền riêng).
- ⚠️ **LƯU Ý VẬN HÀNH**: trong lúc làm, `origin/release_step_20260827` đã tiến **102 commit** (`03f1f11fa9` → `be4cbf0930`) do tiến trình khác fetch trên working copy dùng chung. Branch đã được dựng lại trên tip mới nên diff sạch, nhưng nếu release lại tiến tiếp trước khi push thì nên đối chiếu lại.

## Mức VERIFY của Dev

| Mục | Giá trị |
|---|---|
| Mức | **lint** (không có unit test / integration test) |
| Lệnh đã chạy | Rebase (cherry-pick) lên `origin/release_step_20260827` = `be4cbf0930` — auto-merge sạch, không conflict; `php -l` MobileEventBookingController.php / functions.php / routes/web.php: No syntax errors; `node --check` order-item.js: OK; `BladeCompiler::compileString(index.blade.php)` + `php -l`: compiled ok |
| Grep xác nhận | Còn **0** chỗ gán `window.location.href = '#top'`; `scrollToTop()` xuất hiện **9 lần trong blade + 7 lần trong JS** (6 điểm gọi + 1 khai báo); fix lượt trước đã gỡ sạch (không còn `MESSAGE_BOOKING_NOT_CREATED`, không còn chốt chặn, không còn `$result = 'error'` thêm vào payment/changeBooking) |
| Bằng chứng log | App log 08/09 (12GB): payment event booking error = 0, TokenMismatch = 0; 6/6 đơn có thật đều tạo thành công và gửi action `21212607`; yukinko (`line_user_id 21771991`) mở form 08/09 09:26:07 nhưng **không có POST `/ajax/booking-event/payment`** nào; access log 3 ngày cũng 0 request payment từ IP của 2 u_code lỗi ⇒ request đăng ký chưa bao giờ rời khỏi trình duyệt; `u_code 3Ak3B03J7r` thành công cũng từng vào form 05/09 mà không submit được, tới 09/09 mất **5 phút 06 giây** sau khi form render mới bấm được nút; `b_slot 529452` `number_people = null`, `date_deadline = 2026-09-09 23:59`, `type_times_booking = 1` ⇒ loại trừ hết chỗ / quá hạn / chặn trùng |
| Chưa làm được | **CHƯA tái hiện được trên thiết bị thật**: container không có iPhone/LINE; dev DB `host.docker.internal:3306` Connection refused |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
