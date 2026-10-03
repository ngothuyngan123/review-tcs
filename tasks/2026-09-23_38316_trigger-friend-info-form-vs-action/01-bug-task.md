# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38316 — [Trigger lưu friend info] Phân biệt trigger lúc nhập info form và trigger lúc setting trong multi action` |
| Module / Màn hình | Friend Information (FA-015) — màn **lịch sử thêm thông tin bạn bè** (`友だち情報追加履歴`), cột **Trigger**. Nguồn ghi: 質問項目 của form/đặt lịch (フォーム · カレンダー · イベント · サロン · レッスン · 商品販売) + bước ghi friend info trong **multi action** (アクション) |

## Mô tả bug (bản dịch tiếng Việt)

Yêu cầu tách nhãn Trigger ở màn lịch sử thêm thông tin bạn bè thành 2 loại rõ ràng:

**1. Trigger lúc save friend info khi nhập thông tin form:**

- `[フォーム] 質問項目に入力する情報`: Thông tin lúc nhập form của tính năng form
- `[イベント] 質問項目に入力する情報`: Thông tin lúc nhập form của tính năng event booking
- `[レッスン] 質問項目に入力する情報`: Thông tin lúc nhập form của tính năng lesson
- `[サロン] 質問項目に入力する情報`: Thông tin lúc nhập form của tính năng salon
- `[商品販売] 質問項目に入力する情報`: Thông tin lúc nhập form của tính năng item

**2. Trigger lúc setting friend info trong multi action** ⇒ Thêm tiền tố đằng trước mỗi tính năng. Ví dụ tính năng event:

- `[イベント]予約受付時アクション`: Action lúc nhận booking approve ngay
- `[イベント]予約リクエスト受付時アクション`: Action lúc nhận request booking
- `[イベント]予約リクエスト承認時アクション`: Action lúc approve request booking
- `[イベント]予約リクエスト否認時アクション`: Action lúc từ chối request booking
- `[イベント]予約キャンセル時アクション`: Action lúc cancel booking
- `[イベント]キャンセルリクエスト受付時アクション`: Action lúc nhận request cancel booking
- `[イベント]キャンセルリクエスト承認時アクション`: Action lúc approve request cancel
- `[イベント]キャンセルリクエスト否認時アクション`: Action lúc từ chối request cancel
- `[イベント]予約変更時アクション`: Action lúc change booking (event)
- `[イベント]予約変更リクエスト受付時アクション`: Action lúc nhận request change (event)
- `[イベント]予約変更リクエスト承認時アクション`: Action lúc approve request change (event)
- `[イベント]予約変更リクエスト否認時アクション`: Action lúc từ chối request change (event)

## Steps to reproduce

<!-- Redmine KHÔNG có Section "Tái hiện bug" — ticket viết dưới dạng yêu cầu đổi nhãn Trigger, không có kịch bản tái hiện. -->

## Expected result

<!-- Không có trong Redmine — suy được từ mô tả: xem danh sách nhãn ở mục 1 + 2 phía trên. -->

## Actual result

<!-- Không có trong Redmine. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38316 KHÔNG có attachment. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** (ticket `Bug tự detect`, không có Section "Tái hiện bug", không attachment) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** + **regression impact**.

- **Môi trường**: Redmine không ghi môi trường phát hiện. Branch fix `ai_small_38316` (gốc `release_staging_20260810`).
- **Điều kiện tiên quyết dựng env**: bot có ít nhất 1 trường friend info; cấu hình được 6 tính năng có 質問項目 map vào friend info (form · đặt lịch hẹn カレンダー · sự kiện イベント · salon サロン · lớp học レッスン · bán hàng 商品販売 đơn lẻ + định kỳ); cấu hình được multi action có bước `友だち情報を追加/更新`.
- ⚠️ **Dữ liệu CŨ không migrate** — bản ghi lịch sử ghi trước fix vẫn mang mã hành động cũ nên hiển thị nhãn hành động (có thêm tiền tố), KHÔNG chuyển thành `質問項目に入力する情報`. Phải nói rõ với tester khi test lại data cũ.
- ⚠️ **Dev chưa verify được trên DB** — báo cáo AI ghi "Không kết nối được MySQL dev (host.docker.internal:3306 Connection refused)", kết luận chỉ dựa trên đọc mã nguồn 203 điểm gọi `recordFriendInfoHistory`. Verify chỉ ở mức `php -l` + script gọi thử `getTriggerAttribute`. **Chưa có bằng chứng chạy thật ở tầng DB/UI.**
- ⚠️ **Phạm vi AI tự nới so với ticket**: ticket chỉ liệt kê 5 tính năng ở mục 1, AI bổ sung thêm `[カレンダー]` (đặt lịch hẹn) → cần Leader xác nhận nhãn này đúng ý khách.
- ⚠️ **Bán hàng**: nhãn nguồn nhập 質問項目 dùng chung `[商品販売]` cho cả đơn lẻ và định kỳ (đúng ticket), nhưng nhãn **hành động** tách thành `[単品商品販売]` / `[継続商品販売]`.
- **Quét ngang chưa làm**: cùng kiểu nhãn trigger còn ở **lịch sử thẻ (tag)** và **lịch sử menu phong phú (rich menu)** — Dev ghi "không thuộc phạm vi phiếu này".

## Journal / note từ Redmine (nguyên văn)

**Journal #131949 — AI LME Fix bug — 2026-08-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn lịch sử thêm thông tin bạn bè hiển thị trigger dựa trên mã trigger lưu cùng bản ghi lịch sử. Trước fix, giá trị do khách nhập ở phần câu hỏi của form/màn đặt lịch được ghi bằng CHÍNH mã trigger của hành động tương ứng (ví dụ mã 8001 = hành động lúc nhận đặt chỗ sự kiện), nên không phân biệt được với giá trị do hành động trong cấu hình đa hành động ghi vào. Thêm nữa, nhãn của 4 tính năng đặt lịch (lịch hẹn, sự kiện, lớp học, salon) dùng chuỗi giống hệt nhau nên không biết thuộc tính năng nào, và 5 màn còn gắn nhầm mã của tính năng khác (đặt lịch hẹn gắn mã sự kiện, lớp học gắn mã lịch hẹn/sự kiện). Riêng nhánh ghi thông tin bạn bè bên trong đa hành động thì không truyền mã trigger nên lịch sử luôn hiện là thủ công.

■ 2. CÁCH FIX
Tách hẳn trigger 'khách nhập ở câu hỏi form' ra khỏi trigger 'hành động': thêm 6 mã trigger mới kèm nhãn có sẵn tiền tố tính năng ([フォーム]/[カレンダー]/[イベント]/[サロン]/[レッスン]/[商品販売] + 質問項目に入力する情報) và gắn đúng mã này cho toàn bộ 203 điểm lưu thông tin bạn bè từ biểu mẫu của 6 tính năng, đồng thời sửa 5 màn đang gắn nhầm mã tính năng khác (đặt lịch hẹn, lớp học). Thêm tiền tố tên tính năng vào nhãn trigger của các hành động dùng chung chuỗi giống nhau (lịch hẹn/sự kiện/salon/lớp học/bán hàng đơn lẻ/bán hàng định kỳ). Truyền mã trigger của hành động đang chạy vào nhánh ghi thông tin bạn bè trong đa hành động để lịch sử hiện đúng tên hành động thay vì 'thủ công'. Quét ngang: cùng kiểu nhãn trigger còn ở lịch sử thẻ và lịch sử menu phong phú nhưng không thuộc phạm vi phiếu này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FriendInformationHistory::getTriggerAttribute (app/Models/FriendInformationHistory.php)
FriendInformationHistory::triggerFeaturePrefix (app/Models/FriendInformationHistory.php)
SourceMessage::ACTION_QUESTION_INPUT (app/SourceMessage.php)
sendAction - nhánh friend_info (app/Helpers/functions.php)
recordFriendInfoHistory (app/Helpers/functions.php)
FriendDetailFriendInfoService::transformHistoryRow (app/Services/FriendDetailFriendInfoService.php)
FormAnswerService::storeRenderForm / storeFriendInfo (app/Services/FormAnswer/FormAnswerService.php)
EventBookingService::handleOrderCallback / callbackChangeBooking (app/Services/EventBooking/EventBookingService.php)
CalendarCourseBookingService::create / updateFriendInfoValue (app/Services/CalendarManagement/CalendarCourseBookingService.php)
CalendarSalonLineBookingService::createBooking / updateFriendInfoValue (app/Services/CalendarSalon/CalendarSalonLineBookingService.php)
SalesService::handleOrderCallback (app/Services/Sales/SalesService.php)
BookingManagerController::ajaxStartBooking (app/Http/Controllers/Basic/BookingManagerController.php)
CalendarManagementController::saveInfoFormBooking (app/Http/Controllers/Basic/CalendarManagementController.php)
Mobile/CalendarController::updateFriendInfoValue (app/Http/Controllers/Mobile/CalendarController.php)

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l cho cả 24 file đã sửa: No syntax errors (0 fail); Script thử nhanh gọi FriendInformationHistory::getTriggerAttribute với 20 mã trigger: 8001 -> [イベント]予約受付時アクション, 7001 -> [カレンダー]予約受付時アクション, 9001 -> [サロン]予約受付時アクション, 11001 -> [レッスン]予約受付時アクション, 12002 -> [単品商品販売]申し込み完了時アクション, 13002 -> [継続商品販売]申し込み完了時アクション, 4003 -> [フォーム] 質問項目に入力する情報, 7013/8013/9010/11010/12004 -> đúng nhãn từng tính năng; NULL/rỗng/chuỗi lạ -> 手動 (không đổi); 15001 -> 手動（tên nhân viên）(không đổi); git diff --stat 2c1d7fb...ai_small_38316: 24 file, +302/-201; kiểm tra diff không có dòng nào ngoài lệnh recordFriendInfoHistory bị đổi mã
   Bằng chứng: Không kết nối được MySQL dev (host.docker.internal:3306 Connection refused) nên không dump được phân bố trigger_type_start thực tế; kết luận dựa trên đọc mã nguồn toàn bộ 203 điểm gọi recordFriendInfoHistory.; Xác nhận không có nhánh logic nào so sánh trigger_type_start với các mã bị đổi: chỉ có 2 chỗ so sánh là 4001 (lịch sử menu phong phú) và 15001 (thủ công), đều không đụng.

■ TỰ REVIEW (AI)
Fix đúng root cause: tách mã trigger theo nguồn + theo tính năng thay vì vá chỗ hiển thị. Toàn bộ thay đổi ở điểm gọi chỉ là đổi tham số mã trigger (đã kiểm diff không đụng dòng nào khác), phần logic mới gom trong 2 file (hằng số nhãn + hàm dựng nhãn). Điểm cần người duyệt xác nhận: (1) phiếu chỉ liệt kê 5 tính năng cho mục 1 nhưng tính năng đặt lịch hẹn cũng lưu thông tin bạn bè từ biểu mẫu nên đã bổ sung [カレンダー] cho nhất quán; (2) các nhãn hành động vốn đã duy nhất (biểu mẫu, tự động trả lời, thẻ, menu phong phú...) KHÔNG thêm tiền tố để tránh lặp chữ; (3) bán hàng đơn lẻ và định kỳ được tách thành [単品商品販売]/[継続商品販売] vì nhãn hành động của 2 loại trùng nhau, riêng nhãn nguồn nhập ở câu hỏi dùng chung [商品販売] đúng như phiếu ghi.
 • Rủi ro / lưu ý khi test:
   - Bản ghi lịch sử CŨ vẫn mang mã hành động nên sẽ hiện nhãn hành động (có tiền tố) chứ không phải 質問項目に入力する情報 — cần nói rõ với tester khi test lại dữ liệu cũ.
   - Nhánh đa hành động nay ghi mã trigger theo tham số của hàm gửi hành động; một số nơi gọi truyền chuỗi không phải số (ví dụ friendList/chat) thì lịch sử vẫn hiện 手動 như trước, không hồi quy.
   - Chưa kiểm chứng được trên DB dev (không kết nối được), cần tester chạy lại kịch bản thật cho từng tính năng.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38316 (nhánh gốc release_staging_20260810, commit c44615ec68, 24 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 14 phút 2 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=f465ccf5-f0fa-475e-971b-f67e498c7457
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38316
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
