# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #39231 bởi `/new-task` (2026-09-19). File này **chỉ giữ thông tin cần để viết/review TC** — metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39231 — [LME-Studio] Endpoint chấp nhận lời mời staff lỗi 500 khi bot_role của lời mời không đọc được` |
| Module / Màn hình | Quản lý nhân viên (FA-035 Staff Management) — luồng chấp nhận lời mời staff: `POST /admin/ajax/accept-invite-staff` (modal 「アカウント権限の承認」 ở trang chủ admin). Liên quan: `POST /admin/ajax/generate-link-invite-staff`, giới hạn 10 staff gói Standard. |

## Mô tả bug (bản dịch tiếng Việt)

*Bug từ LME Test Studio* — severity Medium
Task: #42
Test case: NEW-165

## Steps to reproduce

1. Chuẩn bị bot gói Standard mới đang có 9 staff.
2. Tạo 2 lời mời staff còn hiệu lực qua `POST /admin/ajax/generate-link-invite-staff`.
3. Đăng nhập bằng một tài khoản khác và gọi `POST /admin/ajax/accept-invite-staff` với mã lời mời thứ nhất.

## Expected result

- Endpoint phải xử lý được lời mời hợp lệ (hoặc trả lỗi nghiệp vụ rõ ràng), và khi bot đã đạt 10 staff thì lời mời kế tiếp phải bị bỏ qua kèm thông báo giới hạn, số staff giữ nguyên 10.

## Actual result

- Endpoint trả lỗi `'array_column() expects parameter 1 to be array, null given'` thay vì xử lý lời mời — luồng chấp nhận lời mời không kiểm tra `bot_role` null trước khi dùng `array_column()`, nên không thể xác minh được hành vi chặn ở lời mời thứ hai khi bot đã đủ 10 staff.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- log shard chứa TC 6181 (16274 bytes) — https://redmine.watermelon.vn/attachments/download/28620/log%20shard%20ch%E1%BB%A9a%20TC%206181

## Ghi chú thêm của Leader

- Bug do **LME Test Studio** (AI auto test) phát hiện, gọi thẳng API — không phải khách hàng báo. Fix do **AI Auto-fixbug** thực hiện (2 lượt: commit `219b164db2` ngày 2026-08-26, tự review v1 bổ sung commit `4e658d206e` ngày 2026-09-19).
- Điều kiện tiên quyết: bot **gói Standard hợp đồng mới** đang có 9 staff; 2 lời mời staff còn hiệu lực; 1 tài khoản khác (người được mời) để chấp nhận.
- Theo Dev (journal 2): muốn kiểm chứng nhánh chặn giới hạn 10 staff thì phải đi **qua giao diện** (modal 「アカウント権限の承認」) — gọi thẳng API chỉ với mã lời mời (không kèm `bots`) sẽ luôn dừng ở thông báo nghiệp vụ mới.
- Dev chưa verify được trên môi trường dev (DB dev `Connection refused`) — kiểm chứng chỉ ở mức lint + chạy thử logic bằng PHP CLI.

## Journal / note từ Redmine (nguyên văn)

**Journal #133045 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Endpoint chấp nhận lời mời nhân viên dùng thẳng danh sách bot do phía giao diện gửi lên (tham số bots) mà không kiểm tra. Khi request không kèm danh sách này — gọi thẳng API chỉ với mã lời mời, hoặc lời mời không còn bot nào để duyệt (giao diện gửi mảng rỗng nên tham số bị lược bỏ) — giá trị nhận được là rỗng, hàm gom danh sách id nhận rỗng nên PHP báo lỗi và trả 500 thay vì thông báo nghiệp vụ. Vì chết ngay ở bước này nên phần kiểm tra giới hạn 10 nhân viên phía sau không bao giờ chạy tới. Cùng lỗi này còn nằm ở hai chỗ đọc dữ liệu phân quyền bot của lời mời: chuỗi JSON lưu trong bảng lời mời nếu không giải mã được sẽ trả rỗng rồi bị dùng thẳng.

■ 2. CÁCH FIX
Chuẩn hoá và kiểm tra danh sách bot trước khi xử lý lời mời: thêm hàm lọc bỏ phần tử không phải mảng hoặc thiếu khoá định danh, danh sách rỗng thì trả lỗi nghiệp vụ tiếng Nhật rõ ràng ngay sau bước kiểm hạn dùng của lời mời (không còn lỗi 500, cũng không xoá phiên làm việc của luồng mời). Hai chỗ đọc dữ liệu phân quyền bot của lời mời được fallback mảng rỗng khi không giải mã được, đúng như cách phần phát hành link mời đang làm. Quét ngang: mẫu lỗi này chỉ còn trong chính màn quản lý nhân viên, không có endpoint nào khác gom id từ dữ liệu client gửi lên theo cách này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
StaffManagementController::acceptInviteStaff (app/Http/Controllers/Admin/StaffManagementController.php) — điểm phát sinh 500, đã thêm chốt chặn
StaffManagementController::normalizeAcceptedBots (app/Http/Controllers/Admin/StaffManagementController.php) — hàm lọc mới
StaffManagementController::getDetailInviteStaffByCode (app/Http/Controllers/Admin/StaffManagementController.php) — nguồn sinh danh sách bot cho màn duyệt lời mời
StaffManagementController::markUserVisitedLinkInvite (app/Http/Controllers/Admin/StaffManagementController.php) — cũng đọc dữ liệu phân quyền bot của lời mời
StaffManagementController::generateLinkInviteStaff (app/Http/Controllers/Admin/StaffManagementController.php) — đã an toàn sẵn, dùng làm mẫu
StaffManagementController::getStandardBotsExceedingStaffLimit + rollbackStaffIfOverLimit (app/Http/Controllers/Admin/StaffManagementController.php) — luồng giới hạn 10 nhân viên, không sửa
modal-confirm-invite-staff.js (public/js/admin/employees/modal-confirm-invite-staff.js) — kiểm payload màn hình gửi lên có đủ khoá định danh

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/StaffManagementController.php
 • 4.2 Data ảnh hưởng:
   - Không có — không thêm/sửa cột hay bản ghi nào; các bản ghi user_staff_bots / invite_staffs vẫn ghi như cũ khi lời mời hợp lệ
 • 4.3 Tính năng liên quan:
   - Staff Management (FA-035) — chấp nhận lời mời nhân viên: trả thông báo nghiệp vụ thay vì lỗi 500 khi danh sách bot rỗng/không đọc được, nhờ đó luồng chặn giới hạn 10 nhân viên gói Standard chạy được đến cuối

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/StaffManagementController.php: No syntax errors detected; php -r tái hiện lỗi gốc: array_column(null,'id') trên PHP 7.4.33 bắn đúng warning 'array_column() expects parameter 1 to be array, null given' — khớp thông báo lỗi trong ticket; php -r chạy thử hàm lọc mới với 7 payload (null / mảng rỗng / chuỗi / phần tử vô hướng / payload thật của màn / thiếu khoá role_id / role_id rỗng): giữ đúng payload hợp lệ, loại hết payload hỏng, array_column sau đó không còn warning
   Bằng chứng: public/js/admin/employees/modal-confirm-invite-staff.js:59 — màn hình gửi {bots: self.bots, code}; self.bots lấy từ get-detail-invite-staff-by-code nên luôn có đủ id/role_id/user_id/user_invite_id/user_staff_id/invite_staff_id => chốt chặn mới không chặn nhầm luồng thật; khi self.bots rỗng jQuery lược bỏ tham số bots nên server nhận rỗng — đúng ca gây 500; db-refined/invite_staffs.sql: bot_role là TEXT chứa JSON (ghi chú '[TYPE] JSON-ish payload') => giải mã hỏng trả rỗng, cần fallback; Không kiểm chứng được trên DB dev: host.docker.internal:3306 từ chối kết nối (Connection refused) tại thời điểm chạy

■ TỰ REVIEW (AI)
Diff bám đúng nguyên nhân: chốt chặn đặt ngay tại điểm phát sinh 500, đặt SAU các bước kiểm lời mời (hết hạn / đã dùng) nên thứ tự thông báo cho người dùng không đổi, và đặt TRƯỚC lệnh xoá phiên làm việc để request hỏng không làm mất trạng thái luồng mời. Luồng hợp lệ giữ nguyên hành vi vì hàm lọc trả lại đúng các phần tử màn hình gửi lên. Nhờ hết 500, phần chặn giới hạn 10 nhân viên (đã có từ ticket trước) mới chạy tới và kiểm chứng được.
 • Rủi ro / lưu ý khi test:
   - Hàm lọc yêu cầu 5 khoá định danh khác rỗng: nếu một bot trong lời mời không xác định được chủ sở hữu thì bot đó bị loại khỏi lần duyệt (trước đây sẽ chạy tiếp rồi chết ở bước sau) — người dùng nhận thông báo nghiệp vụ thay vì 500, coi là hành vi mong muốn
   - Thông báo lỗi mới là chuỗi tiếng Nhật viết thẳng trong controller, giống cách các thông báo sẵn có trong hàm này (không dùng file ngôn ngữ)
   - Chưa chạy được trên môi trường dev (DB dev không kết nối được) nên phần kiểm chứng dựa trên đọc code + chạy thử logic bằng PHP CLI

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39231 (nhánh gốc release_step_20260805, commit 219b164db2, 1 file)  [đã push]
```

**Journal #137185 — AI LME Fix bug — 2026-09-19:**

> Bản đầy đủ (lượt tự review v1, commit `4e658d206e`) — nội dung mục 1–4 đã chép nguyên văn vào [03-dev-impact.md](03-dev-impact.md). Phần khác biệt so với journal #133045:

```
■ 2. CÁCH FIX (bổ sung)
[Tự review v1 — bổ sung commit 4e658d206e, CẦN PUSH LẠI] Chỉ kiểm hình dạng payload là chưa đủ: gửi một mã bot bất kỳ (đủ khoá) vẫn chạy tiếp tới bước đọc hợp đồng bot và trả lỗi 500 y như bug gốc, đồng thời ghi được quyền nhân viên cho bot/quyền không nằm trong lời mời. Nay danh sách bot được đối chiếu với chính dữ liệu phân quyền lưu trong lời mời: bot không có trong lời mời thì bỏ; quyền, chủ sở hữu bot, người nhận lời mời lấy lại từ bản ghi lời mời và phiên đăng nhập hiện tại thay vì tin dữ liệu client. Luồng bấm duyệt trên màn hình không đổi vì màn duyệt vốn dựng danh sách bot từ chính dữ liệu này. Quét ngang (sửa lại kết luận cũ): endpoint chấp nhận đổi chủ bot cũng nhận mảng từ client không kiểm tra, nhưng lỗi bị khối bắt ngoại lệ nuốt nên trả thất bại thay vì 500 — ngoài phạm vi ticket, đề xuất mở ticket riêng.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39231 (nhánh gốc release_step_20260805, commit 4e658d206e, 1 file)  [đã push]
```
