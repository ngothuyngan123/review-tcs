# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #42335 KHÔNG có section "Đánh giá ảnh hưởng phía dev".** Ticket này là **re-test phạm vi do QA chủ động mở** (không phải Dev nộp đánh giá sau khi fix 1 bug cụ thể) — `Assignee: -`, không có commit/PR nào gắn trực tiếp trên Redmine.
>
> Theo **RULE-11** (chỉ ticket Closed/Resolved/Fix done/Released mới là bằng chứng hợp lệ), mục 1–4 dưới đây để trống đúng chuẩn template vì không có "Dev tự kê". Tuy nhiên, task Studio `#376` (link ticket 42335) đã có sẵn **`dev_impact`** suy từ **diff code thật** (branch `release_step_20260930_v2` so với `origin/release_step_20260930`, 93 file thay đổi) — nội dung này được tách riêng ở **Phụ lục** cuối file, dùng làm chiều **"diff code"** ở BƯỚC 2(b) của `/review-tc` (KHÔNG dùng làm chiều "dev-impact" ở BƯỚC 2(a), vì chưa qua Dev xác nhận tay).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Assignee trống trên Redmine>` |
| Commit / Pull Request | `<chưa có trên Redmine — xem diffStat ở Phụ lục>` |
| Branch | `release_step_20260930_v2` |
| Ngày submit đánh giá | `<không áp dụng — không có Dev assessment>` |
| Auto-filled | `2026-10-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

<!-- Không tick được cho ticket này — Redmine không có section "Đánh giá ảnh hưởng" để verify. -->

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp. Ticket #42335 không có section "Đánh giá ảnh hưởng phía dev" (đây là ticket re-test phạm vi, không phải 1 bug cụ thể). Xem Phụ lục cho dev_impact do AI tự suy từ diff (chưa Dev xác nhận tay).>`

## 2. Cách fix

`<Input thiếu — không áp dụng, ticket không mô tả 1 fix cụ thể mà là yêu cầu re-test toàn bộ tính năng sau nhiều fix đã lên branch.>`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — không có Dev assessment để tham chiếu.>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

`<Input thiếu theo nghĩa "Dev tự kê". Xem diffStat 93 file ở Phụ lục — đây là file AI tự đọc diff xác định, chưa qua Dev xác nhận.>`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | | | Direct / Indirect | `<Input thiếu>` |

### 4.2. List data bị update khi fix bug

`<Input thiếu — không có Dev assessment kê data bị update.>`

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | | CREATE / UPDATE / DELETE / MIGRATE | `<Input thiếu>` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

`<Input thiếu theo nghĩa "Dev tự kê". Dùng 13 mục phạm vi re-test ở 01-bug-task.md + dev_impact ở Phụ lục để xác định quan điểm test ở BƯỚC 3a, KHÔNG thay cho mục này.>`

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | | F1, D1 | High / Medium / Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — **N/A, không có Dev assessment**
- [ ] Mục 2 (cách fix) có thể trace về code — **N/A**
- [ ] Mục 3 đã check đủ caller — **N/A**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **N/A, dùng Phụ lục (dev_impact Studio) thay thế**
- [ ] Mục 4.2 không thiếu data — **N/A**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — Leader đối chiếu Phụ lục + 13 mục phạm vi ở `01-bug-task.md`
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — **cần Leader assign Dev trước, ticket hiện chưa có Assignee**

---

## Phụ lục — `dev_impact` từ MCP LME TEST STUDIO (diff thật, KHÔNG phải Dev assessment)

> Nguồn: `task_get_context(task_id=376, sections=["dev_impact","spec_delta"])` — task Studio `#376` link ticket 42335, branch `release_step_20260930_v2` vs `origin/release_step_20260930`, `diffAvailable=true`, `diffStrategy=stat` (93 file thay đổi, +4576/-676). Nội dung AI tự suy từ diff code thật, **KHÔNG** phải Dev tự kê — dùng làm chiều "diff code" ở BƯỚC 2(b) của `/review-tc`, KHÔNG dùng thay mục 4 ở trên.

### dev_impact (nguyên văn)

- Engine tính slot/đếm booking (`CalendarSalonLineBookingService`) sửa nhiều lần trong v2: gộp ca qua nửa đêm khi 合算をする (#42034 — biên ngày, biên tuần CN→T2, biên tháng), 合算をする không ẩn oan khung đầu ca (#41743/#41742), lịch 個人 không còn xoá đơn ở lần kiểm lại (#41822 đã revert về trạng thái cũ) → rủi ro cao cho mục 1 (limit 1.1/1.2) và mục 13 (đặt/hủy).
- Phân bổ staff tự động (job `CalendarSalonStaffAssignment`/`Admin` + cột `staff_assignment_status` mới): hủy booking khi job đang phân bổ, không gửi tin xác nhận khi đơn đã hủy (#40910) → rủi ro cho mục 2 (random/ưu tiên).
- Google Calendar: block giờ khi không có staff/ca ngắn (test `GoogleBlock*`), dọn event mồ côi (command `RecoverSalonDeleteOrphanGoogleEvent`), hàng đợi xoá event sau phân bổ → mục 12.
- Xoá course/lịch lesson chỉ xoá remind type=4, không xoá nhầm remind salon trùng `user_booking_id` (#42148) → mục 8 remind salon.
- Controller `Mobile\CalendarSalonController` và `Basic\CalendarManagementController` có thay đổi → luồng admin app mobile và màn quản lý lịch chung.
- [12/10] Xoá calendar salon (#41194/#42081): dọn thêm lịch sử + thông báo app của booking đã xoá mềm, nhưng course/menu/lịch sử thanh toán/mobile_notify nay bị xoá TRƯỚC transaction → rủi ro xoá dở khi lỗi giữa chừng hoặc 2 request xoá song song (trái chú thích #41304).
- [12/10] Xoá course/staff salon đếm lại badge thông báo app (#42080) → kiểm badge app mobile sau khi xoá course/staff có booking chưa đọc.
- [12/10] Danh sách booking (LIFF lịch sử, tab mới cập nhật, API app) thêm khoá phụ id khi sắp xếp (#41998) → thứ tự các booking trùng giờ/trùng thời điểm cập nhật cố định theo id tăng dần.
- [12/10] トップ画面設定/店舗・ビジネス情報 lưu được text rỗng, xoá ảnh, cut/paste TinyMCE (#42326) — ngoài 13 mục, chỉ tiền điều kiện.
- Helper dùng chung `StripePayment`/`UnivapayPayment` (salon gọi ở `CalendarSalonLineBookingService`) có sửa trong v2 (#42306…): trả thêm `error_code`/`decline_code` khi thẻ bị từ chối — thay đổi cộng thêm, rủi ro thấp nhưng cần 1 case thẻ bị từ chối khi thanh toán booking salon để xác nhận message lỗi vẫn hiển thị đúng.
- Thanh toán: commit v2 chủ yếu ở 継続商品/hợp đồng định kỳ (kể cả #42384 status_webhook UnivaPay cho bill item định kỳ), không thấy sửa trực tiếp luồng bill salon; vẫn retest Stripe/UnivaPay/現地決済 theo yêu cầu human.
- Spec BR-19..BR-28 (giới hạn 60 ngày/20 ca/50 menu/50 remind/10.000 ký tự) CHƯA có trong code v2 → không dùng làm expected.

### diffStat — 93 file thay đổi (+4576/-676), nhóm theo khu vực

| Khu vực | File chính |
|---|---|
| Service salon/lesson core | `CalendarSalonLineBookingService.php` (+544/-?, lớn nhất), `CalendarSalonGoogleCalendarService.php` (+212, mới), `CalendarManagementService.php`, `CalendarCourseService.php`, `CalendarSalonCourseService.php`, `CalendarSalonStaffService.php`, `CalendarCourseBookingService.php` |
| Controller | `Mobile\CalendarSalonController.php` (+460), `Basic\CalendarSalonController.php`, `Basic\CalendarManagementController.php`, `Api\CalendarSalonController.php`, `Api\CalendarLessonController.php` |
| Job / command | `Jobs\CalendarSalonStaffAssignment(Admin).php`, `Console\Commands\RecoverSalonDeleteOrphanGoogleEvent.php` (+234, mới) |
| Repository | `Eloquents\CalendarSalonLineBookingRepository.php`, `CalendarManagementRepository.php`, `BCSalonGoogleCalendarRepository.php` |
| Billing (không trực tiếp salon nhưng dùng chung) | `Helpers\StripePayment.php`, `Helpers\UnivapayPayment.php`, `Services\BillingService.php`, `Console\Commands\AutoPaymentJobUnivapay.php`, `Services\Sales\SalesService.php` (+411/-, lớn), `Basic\SalesManagementV2Controller.php` |
| Friendlist / filter (chạm qua badge, friend info) | `Basic\FriendlistController.php`, `Basic\FilterController.php`, `public/js/friendlist/modal_filter_v2.js` |
| Test tự viết kèm diff (feature tests) | `CalendarManagementEditFieldsTest`, `CalendarSalonCombinedBreakBeforeTest`, `CalendarSalonGoogleBlockNoStaffTest`, `CalendarSalonGoogleBlockShortShiftTest`, `CalendarSalonMergeShiftMidnightTest`, `CalendarSalonOrderRecheckStaffIdTest`, `CalendarSalonServiceEndShiftTest`, `CalendarSalonSlotBoundaryTest`, `CalendarSalonStaffConcurrentLimitTest`, `FriendDetailPaymentHistoryTest`, `RecountAppBadgeNotifyDispatchTest` |

> `diffStrategy=stat` → chỉ có tên file + số dòng, **không có nội dung diff**. `/review-tc` khi chạy trên folder này nên tự gọi lại `task_get_context` nếu cần xem diff chi tiết hơn, hoặc dùng nguyên văn `dev_impact` trên làm chiều "diff code".
