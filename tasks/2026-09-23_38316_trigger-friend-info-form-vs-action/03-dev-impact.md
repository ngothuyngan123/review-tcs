# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `c44615ec68` (repo `sns-line`); Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38316 |
| Branch | `ai_small_38316` (nhánh gốc `release_staging_20260810`), diff base `2c1d7fb` — 24 file, +302/-201 |
| Ngày submit đánh giá | 2026-08-21 (Journal #131949) |
| Auto-filled | `2026-09-23 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

*(nguyên văn Journal #131949 — mục 1)*

Màn lịch sử thêm thông tin bạn bè hiển thị trigger dựa trên mã trigger lưu cùng bản ghi lịch sử. Trước fix, giá trị do khách nhập ở phần câu hỏi của form/màn đặt lịch được ghi bằng CHÍNH mã trigger của hành động tương ứng (ví dụ mã 8001 = hành động lúc nhận đặt chỗ sự kiện), nên không phân biệt được với giá trị do hành động trong cấu hình đa hành động ghi vào. Thêm nữa, nhãn của 4 tính năng đặt lịch (lịch hẹn, sự kiện, lớp học, salon) dùng chuỗi giống hệt nhau nên không biết thuộc tính năng nào, và 5 màn còn gắn nhầm mã của tính năng khác (đặt lịch hẹn gắn mã sự kiện, lớp học gắn mã lịch hẹn/sự kiện). Riêng nhánh ghi thông tin bạn bè bên trong đa hành động thì không truyền mã trigger nên lịch sử luôn hiện là thủ công.

## 2. Cách fix

*(nguyên văn Journal #131949 — mục 2)*

Tách hẳn trigger 'khách nhập ở câu hỏi form' ra khỏi trigger 'hành động': thêm 6 mã trigger mới kèm nhãn có sẵn tiền tố tính năng (`[フォーム]`/`[カレンダー]`/`[イベント]`/`[サロン]`/`[レッスン]`/`[商品販売]` + `質問項目に入力する情報`) và gắn đúng mã này cho toàn bộ **203 điểm** lưu thông tin bạn bè từ biểu mẫu của 6 tính năng, đồng thời sửa **5 màn** đang gắn nhầm mã tính năng khác (đặt lịch hẹn, lớp học). Thêm tiền tố tên tính năng vào nhãn trigger của các hành động dùng chung chuỗi giống nhau (lịch hẹn/sự kiện/salon/lớp học/bán hàng đơn lẻ/bán hàng định kỳ). Truyền mã trigger của hành động đang chạy vào nhánh ghi thông tin bạn bè trong đa hành động để lịch sử hiện đúng tên hành động thay vì 'thủ công'. Quét ngang: cùng kiểu nhãn trigger còn ở **lịch sử thẻ** và **lịch sử menu phong phú** nhưng **không thuộc phạm vi phiếu này**.

**Bảng mã trigger (từ mục 6 VERIFY — script gọi thử `getTriggerAttribute`):**

| Mã mới (nguồn nhập 質問項目) | Nhãn | Mã hành động cũ từng bị dùng |
|---|---|---|
| `4003` | `[フォーム] 質問項目に入力する情報` | `4002` (trả lời form) |
| `7013` | `[カレンダー] 質問項目に入力する情報` | `8001` (nhầm mã event) |
| `8013` | `[イベント] 質問項目に入力する情報` | `8001` |
| `9010` | `[サロン] 質問項目に入力する情報` | `9001` |
| `11010` | `[レッスン] 質問項目に入力する情報` | `7001` (web) / `8001` (mobile) — nhầm mã |
| `12004` | `[商品販売] 質問項目に入力する情報` (dùng chung đơn lẻ + định kỳ) | `12002` / `13002` |

**Dải tiền tố `TRIGGER_FEATURE_PREFIXES`** (nhãn hành động): `7001-7012` → `[カレンダー]` · `8001-8012` → `[イベント]` · `9001-9009` → `[サロン]` · `11001-11009` → `[レッスン]` · `12001-12003` → `[単品商品販売]` · `13001-13007` → `[継続商品販売]`. Các mã `質問項目` đặt **ngoài** dải này (chủ đích) để không double-prefix.

**Không đổi**: `NULL`/rỗng/chuỗi lạ → `手動`; `15001` → `手動（tên nhân viên）`; `4001` (lịch sử menu phong phú) và `15001` là 2 chỗ duy nhất trong code so sánh `trigger_type_start`, đều không bị đụng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

*(nguyên văn Journal #131949 — mục 3)*

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendInformationHistory::getTriggerAttribute` — `app/Models/FriendInformationHistory.php` | Thêm nhãn 6 mã mới + gọi `triggerFeaturePrefix` | Tầng hiển thị nhãn Trigger |
| 2 | `FriendInformationHistory::triggerFeaturePrefix` — `app/Models/FriendInformationHistory.php` | **Hàm mới** — dựng tiền tố `[tính năng]` theo dải mã | Phân biệt 4 tính năng đặt lịch dùng chung chuỗi nhãn |
| 3 | `SourceMessage::ACTION_QUESTION_INPUT` — `app/SourceMessage.php` | Thêm 6 hằng số mã trigger mới (4003/7013/8013/9010/11010/12004) | Tách nguồn "khách nhập 質問項目" khỏi nguồn "hành động" |
| 4 | `sendAction` — nhánh `friend_info` — `app/Helpers/functions.php` | Truyền `$typeStartScenario` (tham số thứ 7) xuống `recordFriendInfoHistory` thay vì NULL | Bước ghi friend info trong multi action trước đây luôn hiện `手動` |
| 5 | `recordFriendInfoHistory` — `app/Helpers/functions.php` | Nhận mã trigger từ caller | Điểm ghi `friend_info_history` dùng chung của 203 call site |
| 6 | `FriendDetailFriendInfoService::transformHistoryRow` — `app/Services/FriendDetailFriendInfoService.php` | Đọc `trigger_name` để render cột Trigger | Caller của tầng hiển thị |
| 7 | `FormAnswerService::storeRenderForm` / `storeFriendInfo` — `app/Services/FormAnswer/FormAnswerService.php` | `4002` → `4003` | Nguồn nhập 質問項目 của form |
| 8 | `EventBookingService::handleOrderCallback` / `callbackChangeBooking` — `app/Services/EventBooking/EventBookingService.php` | `8001` → `8013` | Nguồn nhập 質問項目 của event (nhiều nhánh callback) |
| 9 | `CalendarCourseBookingService::create` / `updateFriendInfoValue` — `app/Services/CalendarManagement/CalendarCourseBookingService.php` | → `11010` | Nguồn nhập 質問項目 của lớp học |
| 10 | `CalendarSalonLineBookingService::createBooking` / `updateFriendInfoValue` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | `9001` → `9010` | Nguồn nhập 質問項目 của salon |
| 11 | `SalesService::handleOrderCallback` — `app/Services/Sales/SalesService.php` | `12002` → `12004` | Nguồn nhập 質問項目 của bán hàng |
| 12 | `BookingManagerController::ajaxStartBooking` — `app/Http/Controllers/Basic/BookingManagerController.php` | `8001` → `7013` | **Màn gắn nhầm mã** — đặt lịch hẹn từng gắn mã event |
| 13 | `CalendarManagementController::saveInfoFormBooking` — `app/Http/Controllers/Basic/CalendarManagementController.php` | `7001` → `11010` | **Màn gắn nhầm mã** — lớp học (web) từng gắn mã calendar |
| 14 | `Mobile/CalendarController::updateFriendInfoValue` — `app/Http/Controllers/Mobile/CalendarController.php` | `8001` → `11010` | **Màn gắn nhầm mã** — lớp học (mobile) từng gắn mã event |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

*24 file thay đổi (nguyên văn mục 4.1 — Dev kê theo file, không theo function).*

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Hằng số mã + nhãn trigger | `app/SourceMessage.php` | Direct | Thêm 6 hằng số mã `質問項目` mới |
| F2 | `getTriggerAttribute` · `triggerFeaturePrefix` | `app/Models/FriendInformationHistory.php` | Direct | **Tầng hiển thị dùng chung** — mọi nguồn ghi friend info đều đi qua |
| F3 | `sendAction` (nhánh friend_info) · `recordFriendInfoHistory` | `app/Helpers/functions.php` | Direct | **Hàm dùng chung** 203 call site |
| F4 | `FormAnswerService` | `app/Services/FormAnswer/FormAnswerService.php` | Direct | Form → `4003` |
| F5 | `EventBookingService` | `app/Services/EventBooking/EventBookingService.php` | Direct | Event → `8013`, nhiều nhánh callback |
| F6 | `CalendarCourseBookingService` | `app/Services/CalendarManagement/CalendarCourseBookingService.php` | Direct | Lớp học → `11010` |
| F7 | `CalendarSalonLineBookingService` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Direct | Salon → `9010` |
| F8 | `SalesService` | `app/Services/Sales/SalesService.php` | Direct | Bán hàng → `12004` |
| F9 | `FormAnswerController` | `app/Http/Controllers/Basic/FormAnswerController.php` | Direct | Surface web — form |
| F10 | `BookingEventController` | `app/Http/Controllers/Basic/BookingEventController.php` | Direct | Surface web — event |
| F11 | `BookingEventDayController` | `app/Http/Controllers/Basic/BookingEventDayController.php` | Direct | Surface web — event theo ngày |
| F12 | `MobileEventBookingController` | `app/Http/Controllers/Basic/MobileEventBookingController.php` | Direct | Surface mobile — event |
| F13 | `BookingManagerController` | `app/Http/Controllers/Basic/BookingManagerController.php` | Direct | **Sửa mã nhầm** `8001` → `7013` |
| F14 | `AppBookingCalendar` | `app/Http/Controllers/Basic/AppBookingCalendar.php` | Direct | Surface app — đặt lịch hẹn |
| F15 | `CalendarManagementController` | `app/Http/Controllers/Basic/CalendarManagementController.php` | Direct | **Sửa mã nhầm** `7001` → `11010` |
| F16 | `CalendarSalonController` (Basic) | `app/Http/Controllers/Basic/CalendarSalonController.php` | Direct | Surface web — salon |
| F17 | `SalesManagementV2Controller` | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | `12002`/`13002` → `12004` |
| F18 | `SalesStripePaymentController` | `app/Http/Controllers/Basic/SalesStripePaymentController.php` | Direct | Callback thanh toán Stripe |
| F19 | `Api/BookingEventController` | `app/Http/Controllers/Api/BookingEventController.php` | Direct | **Surface API** — event |
| F20 | `Api/BookingCalendar` | `app/Http/Controllers/Api/BookingCalendar.php` | Direct | **Surface API** — đặt lịch hẹn |
| F21 | `Api/CalendarLessonController` | `app/Http/Controllers/Api/CalendarLessonController.php` | Direct | **Surface API** — lớp học |
| F22 | `Api/CalendarSalonController` | `app/Http/Controllers/Api/CalendarSalonController.php` | Direct | **Surface API** — salon |
| F23 | `Mobile/CalendarController` | `app/Http/Controllers/Mobile/CalendarController.php` | Direct | **Sửa mã nhầm** `8001` → `11010` |
| F24 | `Mobile/CalendarSalonController` | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | **Surface mobile** — salon |

### 4.2. List data bị update khi fix bug

*(nguyên văn mục 4.2)*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_info_history.trigger_type_start` | CREATE (bản ghi mới) | Bản ghi **MỚI** dùng mã mới (`4003`/`7013`/`8013`/`9010`/`11010`/`12004`) cho nguồn nhập ở câu hỏi form; bản ghi **CŨ** giữ nguyên mã cũ nên vẫn hiện nhãn hành động (có thêm tiền tố tính năng). **Không sửa / không migrate dữ liệu cũ.** |
| D2 | `friend_info_history` (nhánh multi action) | CREATE (bản ghi mới) | Nhánh ghi thông tin bạn bè trong đa hành động nay lưu mã trigger của hành động thay vì `NULL` (chỉ áp cho bản ghi mới). |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

*(nguyên văn mục 4.3 — Dev không ghi mức High/Medium/Low; cột dưới là suy luận từ phạm vi thay đổi, Leader verify lại.)*

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Information (FA-015)** — màn lịch sử thêm thông tin bạn bè: nhãn cột Trigger phân biệt được nguồn nhập ở câu hỏi form vs hành động, và có tiền tố tên tính năng | F2, F6, D1, D2 | **High** — tầng hiển thị dùng chung mọi nguồn ghi |
| T2 | **Form Builder (FA-011)** — thông tin bạn bè lưu từ câu hỏi biểu mẫu nay gắn trigger riêng của biểu mẫu | F4, F9, D1 | Medium |
| T3 | **Lesson / Calendar Booking (FA-019)** — thông tin bạn bè lưu từ biểu mẫu đặt lịch lớp học và lịch hẹn: gắn trigger riêng, đồng thời sửa các màn trước đây gắn nhầm mã tính năng khác | F6, F13, F14, F15, F20, F21, F23, D1 | **High** — 3 màn sửa mã nhầm, 4 surface (web/app/api/mobile) |
| T4 | **Salon Booking (FA-020)** — thông tin bạn bè lưu từ biểu mẫu đặt lịch salon gắn trigger riêng | F7, F16, F22, F24, D1 | Medium |
| T5 | **Event Booking (FA-021)** — thông tin bạn bè lưu từ biểu mẫu đặt chỗ sự kiện gắn trigger riêng | F5, F10, F11, F12, F19, D1 | Medium — nhiều nhánh callback (approve/change/cancel) |
| T6 | **Single Product / Sales (FA-026)** — thông tin bạn bè lưu từ biểu mẫu mua hàng (đơn lẻ và định kỳ) gắn trigger riêng | F8, F17, F18, D1 | Medium — liên quan callback thanh toán |
| T7 | **Action Settings (SC-004)** — hành động ghi thông tin bạn bè nay lưu kèm mã trigger nên lịch sử hiện đúng tên hành động thay vì thủ công | F3, D2 | **High** — `sendAction` là hàm dùng chung của mọi đường gọi action |

---

## 5. Recover data

✔ Không cần recover data (nguyên văn mục 5).

## 6. Verify của Dev

| Mục | Nội dung |
|---|---|
| Mức | **`lint`** |
| Lệnh | `php -l` cho 24 file: No syntax errors (0 fail). Script gọi thử `getTriggerAttribute` với 20 mã trigger → nhãn đúng cho `8001`/`7001`/`9001`/`11001`/`12002`/`13002`/`4003`/`7013`/`8013`/`9010`/`11010`/`12004`; `NULL`/rỗng/chuỗi lạ → `手動`; `15001` → `手動（tên nhân viên）`. `git diff --stat 2c1d7fb...ai_small_38316`: 24 file, +302/-201. |
| ⚠️ Bằng chứng thiếu | **Không kết nối được MySQL dev** (`host.docker.internal:3306 Connection refused`) → không dump được phân bố `trigger_type_start` thực tế. Kết luận **chỉ dựa trên đọc mã nguồn** 203 điểm gọi `recordFriendInfoHistory`. |
| Đã xác nhận | Không có nhánh logic nào so sánh `trigger_type_start` với các mã bị đổi — chỉ 2 chỗ so sánh là `4001` (lịch sử menu phong phú) và `15001` (thủ công), đều không đụng. |

## 7. Rủi ro / lưu ý khi test (Dev nêu)

1. Bản ghi lịch sử **CŨ** vẫn mang mã hành động nên sẽ hiện nhãn hành động (có tiền tố) chứ không phải `質問項目に入力する情報` — cần nói rõ với tester khi test lại dữ liệu cũ.
2. Nhánh đa hành động nay ghi mã trigger theo tham số của hàm gửi hành động; một số nơi gọi truyền **chuỗi không phải số** (ví dụ `friendList`/`chat`) thì lịch sử vẫn hiện `手動` như trước, không hồi quy.
3. **Chưa kiểm chứng được trên DB dev** (không kết nối được), cần tester chạy lại kịch bản thật cho từng tính năng.

**Điểm AI tự nêu cần người duyệt xác nhận:**

1. Phiếu chỉ liệt kê **5 tính năng** cho mục 1 nhưng tính năng **đặt lịch hẹn** cũng lưu thông tin bạn bè từ biểu mẫu nên AI **tự bổ sung `[カレンダー]`** cho nhất quán → Leader xác nhận.
2. Các nhãn hành động vốn đã duy nhất (biểu mẫu, tự động trả lời, thẻ, menu phong phú...) **KHÔNG** thêm tiền tố để tránh lặp chữ.
3. Bán hàng đơn lẻ / định kỳ tách nhãn **hành động** thành `[単品商品販売]`/`[継続商品販売]` (vì nhãn 2 loại trùng nhau), riêng nhãn **nguồn nhập ở câu hỏi** dùng chung `[商品販売]` đúng như phiếu ghi.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
