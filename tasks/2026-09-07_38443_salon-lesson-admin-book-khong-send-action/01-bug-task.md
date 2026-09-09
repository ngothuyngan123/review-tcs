# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38443 — [Salon/Lesson] Admin book có gán friend info value nhưng không send action của friend info cho user, lịch sử detail friend hiện 設定なし` |
| Module / Màn hình | Salon Booking (FA-020) + Lesson/Calendar Booking (FA-019) — modal 「予約追加」 (admin đặt lịch hộ) trên 「予約カレンダー」; Friend Information (FA-015) — tab 「友だち情報」 của màn 「友だち詳細」 (bảng lịch sử, cột 「追加時アクション」) |

## Mô tả bug (bản dịch tiếng Việt)

Khi **admin đặt lịch hộ khách** (book thay khách) trên lịch **salon** và lịch **lesson**, form đặt lịch có gán giá trị 友だち情報 (friend info) cho khách, nhưng hệ thống **không send action của friend info cho user**. Đồng thời ở màn 「友だち詳細」, **lịch sử của friend info hiển thị 「設定なし」** (chưa thiết lập) thay vì liên kết 「プレビュー」 (xem trước action).

> ⚠️ **Ghi chú nguồn**: phần description trên Redmine #38443 **chỉ có mục `Exp:`** (kết quả mong đợi). Nội dung mô tả hiện tượng ở trên lấy từ **tiêu đề ticket** — Redmine không có đoạn mô tả bug riêng.

## Steps to reproduce

*(Redmine #38443 **KHÔNG có** section "Tái hiện bug" / 再現手順 → để trống, không suy diễn. Dựng lại luồng tái hiện từ mục 1 "Nguyên nhân" ở [03-dev-impact.md](03-dev-impact.md).)*

## Expected result

- Send được action của friend info cho user
- Detail friend: Lịch sử của friend info hiển thị được preview action 「プレビュー」

## Actual result

*(Suy từ tiêu đề ticket — Redmine không có mục "Kết quả thực tế" riêng.)*

- Admin book có gán friend info value nhưng **không send action** của friend info cho user
- Lịch sử friend info ở màn detail friend hiển thị **「設定なし」**

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*(Redmine #38443 không có attachment nào.)*

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (không có section "Tái hiện bug", Steps/Actual để trống) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (xem [03-dev-impact.md](03-dev-impact.md)). TCs nên tập trung verify **cách fix + regression impact**.
- **Trạng thái ticket**: `Fix done - Đợi test` · Tracker `Bug tự detect` · Ticket do hệ thống **Auto-fixbug LME (AI)** fix, không phải Dev người viết.
- ⚠️ **Fix CHƯA chạy được trên môi trường thật** — Dev(AI) ghi rõ: "Chưa chạy được trên môi trường thật (DB dev không kết nối được), mới dừng ở mức đọc code và lint". Verify mới ở mức `php -l` + `git diff --stat`. → **QA là người verify hành vi thật đầu tiên.**
- ⚠️ **2 thay đổi hành vi thấy được** Dev(AI) tự nêu, cần chốt với PO/BA trước khi chấm Đạt/Không đạt:
  1. Tuỳ chọn 「予約時アクションの実行」 (Thực hiện / Không thực hiện) trên form đặt lịch hộ **chỉ chi phối action của lượt đặt**; fix **cố ý KHÔNG** gắn action friend info vào tuỳ chọn này. Nếu nghiệp vụ muốn 「実行しない」 chặn cả action friend info thì phải bọc thêm điều kiện.
  2. Với chế độ 「何度でも稼働」 (chạy mọi lần), **mỗi lần admin đặt lịch hộ và đổi giá trị đều gửi action cho khách** — đúng thiết kế tính năng nhưng là hành vi mới so với hiện tại.
- ⚠️ **Quét ngang còn 4 chỗ khác cùng thiếu đoạn kích hoạt action** (sửa thông tin biểu mẫu của lượt đặt đã có, và 2 luồng đặt lịch từ app) — Dev(AI) ghi nhận nhưng **ngoài phạm vi ticket**, KHÔNG fix lần này.
- Môi trường phát hiện: Redmine không ghi rõ.

## Journal / note từ Redmine (nguyên văn)

**Journal #131657 — AI LME Fix bug — 2026-08-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi admin tự đặt lịch hộ khách (salon và bài học), hệ thống chỉ lưu giá trị thông tin bạn bè và ghi dòng lịch sử, nhưng bỏ hẳn bước kích hoạt action đã gắn với lựa chọn của thông tin bạn bè đó. Vì action không chạy nên khách không nhận được nội dung, đồng thời dòng lịch sử không được gắn liên kết tới action nên cột xem trước ở màn chi tiết bạn bè hiển thị Chưa thiết lập. Luồng khách tự đặt lịch vẫn chạy đúng vì có sẵn đoạn kích hoạt action này.

■ 2. CÁCH FIX
Bổ sung vào 2 luồng admin đặt lịch hộ (salon và bài học) đoạn kích hoạt action gắn với lựa chọn của thông tin bạn bè, giống hệt luồng khách tự đặt lịch: đọc cấu hình action của mục thông tin, so khớp giá trị vừa lưu, tôn trọng chế độ chỉ chạy lần đầu, và truyền id dòng lịch sử vừa ghi vào lệnh chạy action để màn chi tiết bạn bè hiện được liên kết xem trước thay vì Chưa thiết lập. Quét ngang thấy 4 chỗ khác cùng thiếu đoạn này (sửa thông tin biểu mẫu của lượt đặt đã có, và 2 luồng đặt lịch từ app) nhưng nằm ngoài phạm vi ticket nên chỉ ghi nhận.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
CalendarSalonLineBookingService::createBooking (app/Services/CalendarSalon/CalendarSalonLineBookingService.php)
CalendarSalonLineBookingService::updateFriendInfoValue - luồng khách tự đặt, dùng làm mẫu đối chiếu (app/Services/CalendarSalon/CalendarSalonLineBookingService.php)
CalendarCourseBookingService::create (app/Services/CalendarManagement/CalendarCourseBookingService.php)
recordFriendInfoHistory (app/Helpers/functions.php)
sendAction (app/Helpers/functions.php)
getTableHistory - map mã 6004 sang bảng lịch sử thông tin bạn bè (app/Helpers/functions.php)
FriendDetailFriendInfoService::triggerFriendInfoAction - bản trung tâm ở màn chi tiết bạn bè (app/Services/FriendDetailFriendInfoService.php)
cell-actions_preview - chỗ render Xem trước / Chưa thiết lập (resources/views/basic/friend_detail/tabs/friend_info.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Services/CalendarSalon/CalendarSalonLineBookingService.php
   - app/Services/CalendarManagement/CalendarCourseBookingService.php
 • 4.2 Data ảnh hưởng:
   - action_lineuser — thêm bản ghi action chờ chạy khi admin đặt lịch hộ có gán thông tin bạn bè (trước đây không sinh)
   - friend_information_history.action_multi_capture_id — từ nay được gắn cho dòng lịch sử sinh từ admin đặt lịch hộ; dữ liệu cũ vẫn để trống
   - Không cần khôi phục dữ liệu cũ
 • 4.3 Tính năng liên quan:
   - Salon Booking (FA-020) — admin đặt lịch hộ nay chạy action của thông tin bạn bè
   - Lesson / Calendar Booking (FA-019) — admin đặt lịch hộ nay chạy action của thông tin bạn bè
   - Friend Information (FA-015) — lịch sử thông tin bạn bè hiện được liên kết xem trước action thay vì Chưa thiết lập

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Services/CalendarSalon/CalendarSalonLineBookingService.php: No syntax errors detected; php -l app/Services/CalendarManagement/CalendarCourseBookingService.php: No syntax errors detected; git diff --stat release_step_20260805...ai_fixbug_38443: đúng 2 file, 41 dòng thêm
   Bằng chứng: Đối chiếu code: luồng khách tự đặt lịch salon (updateFriendInfoValue, cùng file, quanh dòng 5525-5545) CÓ đoạn đọc cấu hình action rồi chạy action mã 6004 kèm id lịch sử; luồng admin đặt lịch hộ hoàn toàn không có đoạn này; getTableHistory trong app/Helpers/functions.php: mã 6004 map sang bảng lịch sử thông tin bạn bè, đây chính là đường ghi liên kết xem trước; resources/views/basic/friend_detail/tabs/friend_info.blade.php dòng 204-206: có liên kết thì hiện Xem trước, không có thì hiện Chưa thiết lập — khớp đúng triệu chứng ticket; Không kiểm chứng được trên DB dev: MySQL host.docker.internal:3306 từ chối kết nối tại thời điểm điều tra

■ TỰ REVIEW (AI)
Fix bám đúng mẫu đã có sẵn trong chính luồng khách tự đặt lịch salon (cùng file), không tạo hàm dùng chung mới nên không ảnh hưởng luồng nào khác. Chỉ thêm code vào đúng nhánh mục thông tin bạn bè kiểu lựa chọn; các nhánh tên, điện thoại, email, ngày sinh, tỉnh thành, địa chỉ không đổi. Khai báo id lịch sử ngay trong nhánh nên không bị rò giá trị sang vòng lặp sau.
 • Rủi ro / lưu ý khi test:
   - Tuỳ chọn Thực hiện / Không thực hiện trên form đặt lịch hộ có nhãn là hành động khi đặt lịch (chỉ chi phối action của lượt đặt), nên fix cố ý KHÔNG gắn action thông tin bạn bè vào tuỳ chọn này — giống mọi luồng khác đang ghi thông tin bạn bè. Nếu nghiệp vụ muốn tuỳ chọn đó chặn cả action thông tin bạn bè thì cần chốt lại và bọc thêm điều kiện.
   - Với chế độ chạy mọi lần, mỗi lần admin đặt lịch hộ và đổi giá trị sẽ gửi action cho khách — đúng thiết kế của tính năng nhưng là thay đổi hành vi thấy được so với hiện tại.
   - Chưa chạy được trên môi trường thật (DB dev không kết nối được), mới dừng ở mức đọc code và lint.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_38443 (nhánh gốc release_step_20260805, commit 4e6b59e1e4, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 19 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=d96a6d64-f288-40ce-96fa-ed3ba1451b2c
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38443
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
