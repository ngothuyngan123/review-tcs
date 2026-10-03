# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #39239 bởi `/new-task` (2026-09-26).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #39239 — [LME-Studio] Không cách ly dữ liệu đa tài khoản: sửa lịch lesson và xoá staff của bot thuộc tài khoản khác đều thành công |
| Module / Màn hình | Lesson / Calendar Booking (FA-019) — màn quản lý lịch lesson (`/basic/calendar-management`, hộp thoại sửa lịch) · Staff Management (FA-035) — màn quản lý nhân viên (`/admin/ajax/delete-staff-bot`) |

## Mô tả bug (bản dịch tiếng Việt)

*Bug từ LME Test Studio* — severity High
Task: #42
Test case: NEW-104

Bug API: 2 endpoint ghi dữ liệu không kiểm quyền sở hữu bot, nên tài khoản admin A sửa được lịch lesson và xoá được staff của bot thuộc tài khoản admin B.

## Steps to reproduce

1. Chuẩn bị 2 tài khoản admin khác nhau (A và B), mỗi tài khoản sở hữu 1 bot riêng.
2. Trên bot của tài khoản B: tạo 1 lịch lesson (calendar_management) và 3 staff (user_staff_bots).
3. Đăng nhập bằng tài khoản A và chọn bot của A.
4. Gọi POST /basic/calendar-management/{id lịch của bot B}/edit với tên lịch mới 'TC cross tenant'.
5. Gọi POST /admin/ajax/delete-staff-bot với id bản ghi staff thuộc bot của tài khoản B.
6. Truy vấn DB kiểm tra tên lịch của bot B và số staff của bot B.

## Expected result

- Yêu cầu phải bị từ chối vì tài khoản A không có quyền trên bot của tài khoản B; lịch của bot B giữ nguyên tên cũ và số staff của bot B không đổi.

## Actual result

- Cả hai thao tác đều thành công từ tài khoản A: endpoint sửa lịch trả HTTP 200 {"success":true} và tên lịch của bot B bị đổi từ 'seed lesson …' thành 'TC cross tenant'; endpoint xoá staff trả HTTP 200 {"status":true} và số staff của bot B giảm. Không có bước kiểm tra quyền sở hữu bot trong hai endpoint này.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- log shard chứa TC 6120 — https://redmine.watermelon.vn/attachments/download/28633/log%20shard%20ch%E1%BB%A9a%20TC%206120
- log shard chứa TC 6186 — https://redmine.watermelon.vn/attachments/download/28634/log%20shard%20ch%E1%BB%A9a%20TC%206186

## Ghi chú thêm của Leader

- Bug do **LME Test Studio** phát hiện (tác giả ticket: AI Auto test Lme), tracker **Bug API** — tái hiện bằng request dựng tay, UI không có đường chọn lịch/staff của bot khác.
- Điều kiện tiên quyết: **2 tài khoản admin độc lập** (A, B), mỗi tài khoản sở hữu 1 bot, không mời nhau; bot B có ≥ 1 lịch lesson + ≥ 3 staff.
- Fix do **AI auto-fixbug** trên branch `ai_fixbug_39239` (gốc `release_step_20260805`); Dev chỉ verify mức **lint**, **không tái hiện trên dev**.
- Phần xoá staff **trùng nội dung** với fix của ticket **#38960** (branch `ai_fixbug_38960`) — lưu ý khi gộp.
- Journal 2026-09-20: “Gom task fix bug → Refer #41143”. Ticket đã **Closed** (2026-09-22, đổi trạng thái hàng loạt từ Dashboard).
- Tần suất: 100% (lỗi logic thiếu kiểm quyền, không phải xác suất).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Endpoint 1 | POST `/basic/calendar-management/{id}/edit` (bảng `calendar_management`) |
| Endpoint 2 | POST `/admin/ajax/delete-staff-bot` (bảng `user_staff_bots`) |
| Ca lỗi gốc trên Studio | Task #42 — TC NEW-104 |
| Log | TC 6120, TC 6186 (xem attachment) |

## Journal / note từ Redmine (nguyên văn)

**Journal #133411 — AI LME Fix bug — 2026-08-28:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
(Nội dung mục 1 → 4 đã chép sang 03-dev-impact.md. Phần còn lại giữ nguyên văn dưới đây.)

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l trên 5 file đã sửa: No syntax errors detected (cả 5); git diff --stat origin/release_step_20260805...ai_fixbug_39239: đúng 5 file, 40 thêm / 5 xoá; grep toàn app: hàm dịch vụ sửa lịch chỉ có 1 nơi gọi (chính controller đã gắn cổng kiểm) nên thêm điều kiện bot không ảnh hưởng luồng khác; hàm kho dữ liệu cũ giữ nguyên cho luồng sắp xếp lịch
   Bằng chứng: routes/web.php: POST /calendar-management/{id}/edit khai báo TRƯỚC khối Route::middleware(['checkLessonCalendarInBot']) nên không được lớp kiểm quyền bọc; Trên release, hàm xoá nhân viên truy vấn UserStaffBot theo mỗi id rồi destroy — không có điều kiện bot nào; Hai hàm dùng lại đều có sẵn trên release: kiểm lịch-thuộc-bot ở tầng dịch vụ và hàm lấy danh sách bot được quản lý nhân viên trong tệp helper chung; Không tái hiện trực tiếp trên dev (cần 2 tài khoản quản trị + phiên đăng nhập, chỉ được phép đọc dữ liệu)

■ TỰ REVIEW (AI)
Fix bám đúng tiền lệ đã có trên release: cổng kiểm sở hữu đặt ở dòng đầu hàm, trả về trước khi ghi bất cứ thứ gì, và câu lệnh cập nhật lịch kèm luôn điều kiện bot theo quy tắc bảo mật của repo. Dạng phản hồi chọn theo cách giao diện xử lý: màn lịch chỉ đọc nhánh success nên trả HTTP 200 kèm cờ thất bại + thông báo tiếng Nhật (giao diện tự hiện cảnh báo), màn nhân viên không hiện thông báo ở nhánh lỗi nên trả 403 gọn như bản sửa cùng họ. Luồng hợp lệ không đổi: người dùng thao tác trên bot đang chọn luôn qua cổng.
 • Rủi ro / lưu ý khi test:
   - Phần xoá nhân viên trùng nội dung với branch ticket #38960 đang chờ review — khi gộp phải chọn một bản, tránh xung đột
   - Nếu tồn tại luồng hợp lệ nào gọi sửa lịch khi phiên đang ở bot khác (mở nhiều tab rồi đổi bot) thì nay sẽ bị chặn — đây là hành vi mong muốn theo yêu cầu ticket, nhưng cần lưu ý khi test
   - Còn 4 điểm ghi cùng kiểu chưa kiểm sở hữu (đã liệt kê ở quét ngang) — ngoài phạm vi ticket này

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39239 (nhánh gốc release_step_20260805, commit ab90476694, 5 file)  [đã push]
```

**Journal #137265 — AI LME CSS — 2026-09-20:**

```
Gom task fix bug -> Refer #41143
```
