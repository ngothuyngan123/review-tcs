# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39231 bởi `/new-task` — nguồn: **Journal #137185 (2026-09-19, lượt tự review v1)** — bản mới nhất, thay thế Journal #133045 (2026-08-26). Description Redmine không có section "Đánh giá ảnh hưởng"; đánh giá nằm trong journal của AI Auto-fixbug.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (AI Auto-fixbug) — assignee Redmine: Kim Cúc |
| Commit / Pull Request | `sns-line` commit `4e658d206e` (lượt 2, tự review v1) · commit `219b164db2` (lượt 1) — `<chưa có link PR>` |
| Branch | `ai_fixbug_39231` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | 2026-09-19 (lượt 1: 2026-08-26) |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Endpoint chấp nhận lời mời nhân viên dùng thẳng danh sách bot do phía giao diện gửi lên (tham số bots) mà không kiểm tra. Khi request không kèm danh sách này — gọi thẳng API chỉ với mã lời mời, hoặc lời mời không còn bot nào để duyệt (giao diện gửi mảng rỗng nên tham số bị lược bỏ) — giá trị nhận được là rỗng, hàm gom danh sách id nhận rỗng nên PHP báo lỗi và trả 500 thay vì thông báo nghiệp vụ. Vì chết ngay ở bước này nên phần kiểm tra giới hạn 10 nhân viên phía sau không bao giờ chạy tới. Cùng lỗi này còn nằm ở hai chỗ đọc dữ liệu phân quyền bot của lời mời: chuỗi JSON lưu trong bảng lời mời nếu không giải mã được sẽ trả rỗng rồi bị dùng thẳng.

## 2. Cách fix

Chuẩn hoá và kiểm tra danh sách bot trước khi xử lý lời mời: thêm hàm lọc bỏ phần tử không phải mảng hoặc thiếu khoá định danh, danh sách rỗng thì trả lỗi nghiệp vụ tiếng Nhật rõ ràng ngay sau bước kiểm hạn dùng của lời mời (không còn lỗi 500, cũng không xoá phiên làm việc của luồng mời). Hai chỗ đọc dữ liệu phân quyền bot của lời mời được fallback mảng rỗng khi không giải mã được, đúng như cách phần phát hành link mời đang làm.

[Tự review v1 — bổ sung commit 4e658d206e, CẦN PUSH LẠI] Chỉ kiểm hình dạng payload là chưa đủ: gửi một mã bot bất kỳ (đủ khoá) vẫn chạy tiếp tới bước đọc hợp đồng bot và trả lỗi 500 y như bug gốc, đồng thời ghi được quyền nhân viên cho bot/quyền không nằm trong lời mời. Nay danh sách bot được đối chiếu với chính dữ liệu phân quyền lưu trong lời mời: bot không có trong lời mời thì bỏ; quyền, chủ sở hữu bot, người nhận lời mời lấy lại từ bản ghi lời mời và phiên đăng nhập hiện tại thay vì tin dữ liệu client. Luồng bấm duyệt trên màn hình không đổi vì màn duyệt vốn dựng danh sách bot từ chính dữ liệu này. Quét ngang (sửa lại kết luận cũ): endpoint chấp nhận đổi chủ bot cũng nhận mảng từ client không kiểm tra, nhưng lỗi bị khối bắt ngoại lệ nuốt nên trả thất bại thay vì 500 — ngoài phạm vi ticket, đề xuất mở ticket riêng.

**Rủi ro / lưu ý khi test (Dev tự review):**
- Hàm lọc yêu cầu 5 khoá định danh khác rỗng: nếu một bot trong lời mời không xác định được chủ sở hữu thì bot đó bị loại khỏi lần duyệt (trước đây sẽ chạy tiếp rồi chết ở bước sau) — người dùng nhận thông báo nghiệp vụ thay vì 500, coi là hành vi mong muốn.
- Thông báo lỗi mới là chuỗi tiếng Nhật viết thẳng trong controller, giống cách các thông báo sẵn có trong hàm này (không dùng file ngôn ngữ).
- Chưa chạy được trên môi trường dev (DB dev không kết nối được) nên phần kiểm chứng dựa trên đọc code + chạy thử logic bằng PHP CLI (mức verify: lint).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `StaffManagementController::acceptInviteStaff` (app/Http/Controllers/Admin/StaffManagementController.php) | Sửa — thêm chốt chặn + đối chiếu danh sách bot với lời mời (tự review v1) | Điểm phát sinh 500 |
| 2 | `StaffManagementController::normalizeAcceptedBots` (cùng file) | Mới — hàm lọc, nay nhận thêm bản ghi lời mời làm nguồn chân lý | Chuẩn hoá payload `bots` |
| 3 | `StaffManagementController::getDetailInviteStaffByCode` (cùng file) | Sửa — fallback mảng rỗng khi `bot_role` không giải mã được | Nguồn sinh danh sách bot cho màn duyệt lời mời; **DÙNG CHUNG** cho cả màn đổi chủ bot (modal-confirm-change-owner-bot.js) |
| 4 | `StaffManagementController::markUserVisitedLinkInvite` (cùng file) | Sửa — fallback mảng rỗng | Cũng đọc dữ liệu phân quyền bot của lời mời; **DÙNG CHUNG** cho cả màn đổi chủ bot |
| 5 | `StaffManagementController::generateLinkInviteStaff` (cùng file) | Không sửa | Đã an toàn sẵn, dùng làm mẫu (nguồn ghi dữ liệu phân quyền bot vào lời mời) |
| 6 | `StaffManagementController::acceptOwnerBot` (cùng file) | **KHÔNG sửa** | Endpoint anh em cùng nhận mảng bot từ client, lỗi bị khối bắt ngoại lệ nuốt; đề xuất ticket riêng |
| 7 | `StaffManagementController::getStandardBotsExceedingStaffLimit` + `rollbackStaffIfOverLimit` (cùng file) | Không sửa | Luồng giới hạn 10 nhân viên |
| 8 | `modal-confirm-invite-staff.js` (public/js/admin/employees/) | Không sửa | Kiểm payload màn hình gửi lên có đủ khoá định danh (`{bots: self.bots, code}` ở dòng 59) |
| 9 | `modal-confirm-change-owner-bot.js` (public/js/admin/employees/) | Không sửa | Consumer thứ 2 của 2 hàm đã sửa (#3, #4), thuộc phạm vi retest |

---

## 4. Đánh giá ảnh hưởng

> Dev ghi 4.1 dưới dạng **file thay đổi** (1 file). Bảng F dưới đây tách theo function đã liệt kê ở mục 3 để map coverage — không thêm function ngoài mục 3.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `acceptInviteStaff` — `POST /admin/ajax/accept-invite-staff` | app/Http/Controllers/Admin/StaffManagementController.php | Direct | Chốt chặn danh sách bot rỗng + đối chiếu với `bot_role` lời mời |
| F2 | `normalizeAcceptedBots` (mới) | cùng file | Direct | Lọc phần tử không phải mảng / thiếu 5 khoá định danh / bot không có trong lời mời |
| F3 | `getDetailInviteStaffByCode` — `get-detail-invite-staff-by-code` | cùng file | Direct | Fallback mảng rỗng; dùng chung với màn đổi chủ bot |
| F4 | `markUserVisitedLinkInvite` — `mark-user-visited-link-invite` | cùng file | Direct | Fallback mảng rỗng; dùng chung với màn đổi chủ bot |
| F5 | `getStandardBotsExceedingStaffLimit` + `rollbackStaffIfOverLimit` | cùng file | Indirect | Không sửa — nay mới chạy tới được |
| F6 | `acceptOwnerBot` | cùng file | Indirect (không sửa) | Cùng mẫu lỗi, ngoài phạm vi ticket |

### 4.2. List data bị update khi fix bug

Nguyên văn Dev: "Không thêm/sửa cột, không migration, không cần recover data"

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `invite_staffs.bot_role` | READ | Chỉ ĐỌC; sau tự review v1 trở thành nguồn chân lý cho bước chấp nhận lời mời thay vì dữ liệu client gửi lên |
| D2 | `user_staff_bots` | CREATE (không đổi schema) | Khi danh sách bot rỗng/không hợp lệ thì không ghi bản ghi nào; quyền và chủ sở hữu bot nay lấy từ lời mời nên payload giả mạo bị ép về giá trị đúng |
| D3 | `invite_staffs.is_confirmed` | UPDATE (không bật khi chốt chặn kích hoạt) | Hàm trả lỗi sớm nên cờ này KHÔNG được bật, link mời vẫn dùng lại được |
| D4 | Contract JSON endpoint chấp nhận lời mời | — | Thêm một ca trả về thông báo nghiệp vụ thay cho lỗi 500; màn hình đã có sẵn nhánh hiển thị thông báo nên không phải sửa giao diện |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev không ghi mức risk High/Medium/Low — ghi `[TRỰC TIẾP]` / `[GIÁN TIẾP]`; cột Nguy cơ giữ nguyên nhãn của Dev.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Quản lý nhân viên (FA-035) — chấp nhận lời mời nhân viên | F1, F2, D1, D2, D3, D4 | [TRỰC TIẾP] — hết lỗi 500 khi danh sách bot rỗng/không đọc được, trả thông báo nghiệp vụ; bot không nằm trong lời mời bị loại, quyền và chủ sở hữu lấy theo lời mời |
| T2 | Quản lý nhân viên (FA-035) — giới hạn 10 nhân viên gói Standard | F5 | [GIÁN TIẾP] — nhờ hết 500 nên nhánh chặn giới hạn mới chạy tới; lưu ý kiểm chứng qua giao diện vì gọi thẳng API chỉ với mã lời mời sẽ luôn dừng ở thông báo nghiệp vụ |
| T3 | Đổi chủ quản lý chính của bot (màn FA-035) | F3, F4, F6 | [GIÁN TIẾP] — dùng chung 2 hàm đã sửa (lấy chi tiết lời mời theo mã + đánh dấu đã mở link) nên thuộc phạm vi kiểm thử lại |

> ⚠️ **T3 — Leader xác nhận Dev đánh giá ảnh hưởng sai (2026-09-19), loại khỏi phạm vi test.** Kéo theo F6 `acceptOwnerBot` (luồng đổi owner) cũng ngoài phạm vi — theo dõi ở ticket riêng theo đề xuất của Dev. Nội dung bảng trên giữ nguyên văn Dev.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
