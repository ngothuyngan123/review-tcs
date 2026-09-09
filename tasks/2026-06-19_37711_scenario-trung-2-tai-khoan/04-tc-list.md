<!-- sync-target: https://docs.google.com/spreadsheets/d/1E1ZaqHfbb0mxvLIwgu7WEixMJ3oj4AtX2phsSRAyY4M/edit?gid=491458913 -->
# 04 — TC List (do member viết)

> File gồm **2 phần** để Leader/`/review-tc` review nguyên bộ:
> - **Phần A — TC human (TC-H01→H42)**: import verbatim từ tab **"text fix bug Kh"** (row 80–121) của Sheet. **Read-only** — Expected & Status giữ NGUYÊN văn từ Sheet; Title/Steps/Type/Priority/Precondition do Claude suy ra từ cấu trúc cây để hợp format 10 cột (KHÔNG sửa nội dung nghiệp vụ human).
> - **Phần B — TC delta (TC-D01→D11)**: Claude bổ sung phần human chưa cover (ép race, dedup, edge block/đã-xóa, entry PC/external...).
>
> ⚠️ **Lưu ý format khi sync**: tab human gốc dùng cấu trúc cây merged-cell (≈7 cột), KHÁC layout 10 cột chuẩn. Nếu `/sync-tc` push phần B append xuống dưới row 121 → cần **căn cột thủ công**. Phần A ở đây chỉ là bản chuyển-thể để review, KHÔNG push đè lên row 80–121 gốc.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | `v1 (delta)` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1E1ZaqHfbb0mxvLIwgu7WEixMJ3oj4AtX2phsSRAyY4M/edit?gid=491458913 (tab "text fix bug Kh", row 80–121 = TC human) |

---

## TC List — Phần A: TC human (import verbatim từ Sheet, read-only)

> 42 TC từ tab "text fix bug Kh" row 80–121. Cột **Expected result** & **Status** giữ NGUYÊN văn Sheet. Nhóm theo entry-point. Chủ đề xuyên suốt: mỗi luồng tạo bạn → verify **chỉ 1 line_user, không duplicate**.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-H01 | [Job] Follow QR thường — add friend khi chưa tồn tại line_user | Positive | High | Bot staging; tài khoản LINE chưa là bạn; QR thường của bot | 1. Quét QR thường để kết bạn (chưa tồn tại line_user).<br>2. Vào Quản lý bạn bè kiểm tra. | - Kết bạn với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | OK |
| TC-H02 | [Job] Follow QR thường — friend old chưa tồn tại trên tool | Positive | High | User là bạn cũ nhưng chưa có line_user trên tool | 1. Friend old kết bạn lại với bot.<br>2. Kiểm tra friend list. | - Kết bạn lại với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | OK |
| TC-H03 | [Job] Follow QR thường — thêm friend vào group, nhắn tin trong group | Positive | High | Bot ở trong group; friend là member | 1. Thêm friend vào group.<br>2. Friend nhắn tin trong group.<br>3. Kiểm tra friend list. | - gửi tin nhắn thành công<br>- 1 line user chỉ tồn tại 1 line_user_group<br>- line user không bị duplicate | | | OK |
| TC-H04 | [Job] Follow QR thường — gửi scenario (send quick test) | Positive | Medium | User đã kết bạn; có scenario; gửi quick test | 1. Gửi scenario bằng send quick test.<br>2. Kiểm tra hiển thị + nơi nhận. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H05 | [Job] Follow QR thường — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step.<br>2. Kiểm tra lịch sử send. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H06 | [Job] Follow QR thường — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step.<br>2. Kiểm tra lịch sử + máy user. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H07 | [Job] Follow QR landing — add friend khi chưa tồn tại line_user | Positive | High | User chưa là bạn; QR landing của bot | 1. Kết bạn qua QR landing (chưa tồn tại line_user).<br>2. Kiểm tra friend list. | - Kết bạn với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H08 | [Job] QR landing — thêm friend vào group, nhắn tin group | Positive | Medium | Bot trong group; friend từ QR landing | 1. Thêm friend (QR landing) vào group.<br>2. Friend nhắn tin group. | - gửi tin nhắn thành công<br>- 1 line user chỉ tồn tại 1 line_user_group<br>- line user không bị duplicate | | | Not test |
| TC-H09 | [Job] QR landing — scenario send quick test | Positive | Medium | Friend QR landing; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H10 | [Job] QR landing — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step.<br>2. Kiểm tra lịch sử send. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H11 | [Job] QR landing — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H12 | [Job] Có scenario đang chạy — friend kết bạn mới | Positive | High | Scenario đang chạy; friend kết bạn mới | 1. Trong khi scenario đang chạy, friend kết bạn mới.<br>2. Kiểm tra friend list. | - Kết bạn với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H13 | [Job] Có scenario đang chạy — step sau khi friend thỏa mãn điều kiện | Regression | Medium | Scenario có điều kiện rẽ nhánh; friend vừa thỏa mãn | 1. Cho friend thỏa mãn điều kiện step.<br>2. Quan sát step kế tiếp. | _(human để trống Expected)_ ⚠️ chưa có expected — đối chiếu TC-D10 (verify không double-send, không 2 luồng step song song) | ⚠️ Human bỏ trống expected — member bổ sung | | Not test |
| TC-H14 | [Job] Đang là friend — gửi scenario send quick test | Positive | Medium | User đang là friend | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H15 | [Job] Đang là friend — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step.<br>2. Kiểm tra lịch sử send. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H16 | [Job] Verify không ảnh hưởng user khác (line_id A / line_id B) | Negative | High | 2 user line_id A và B | 1. Add friend cho A và B.<br>2. Xóa friend A.<br>3. Kiểm tra B. | - A được add friend đúng<br>- B hoạt động bình thường<br>- khi xóa friend => Không xóa nhầm dữ liệu của B | | | Not test |
| TC-H17 | [Web] Mở link form => add friend (follow add bot trước → hiển thị link form trả lời) | Positive | High | User chưa là bạn; có link form answer | 1. Mở link form (chưa là bạn) → follow add bot → hiển thị link form.<br>2. Kiểm tra friend list. | - add friend với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H18 | [Web] Mở link form — check trả lời form | Positive | Medium | Đã add friend qua link form | 1. Trả lời form.<br>2. Kiểm tra kết quả + friend list. | - Trả lời form thành công<br>- hiển thị 1 line user | | | Not test |
| TC-H19 | [Web] Link form — gửi scenario send quick test | Positive | Medium | Friend từ link form; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H20 | [Web] Link form — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H21 | [Web] Link form — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H22 | [Web] Mở link booking lesson => add friend (follow add bot trước → hiển thị link booking) | Positive | High | User chưa là bạn; có link booking lesson | 1. Mở link booking lesson (chưa là bạn) → follow add bot → hiển thị link booking. | - add friend với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H23 | [Web] Booking lesson — check booking lesson thành công | Positive | Medium | Đã add friend qua link booking lesson | 1. Book lesson.<br>2. Kiểm tra friend list. | - Booking lesson thành công<br>- hiển thị 1 line user | | | Not test |
| TC-H24 | [Web] Booking lesson — scenario send quick test | Positive | Medium | Friend từ booking lesson; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H25 | [Web] Booking lesson — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H26 | [Web] Booking lesson — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H27 | [Web] Mở link booking salon => add friend | Positive | High | User chưa là bạn; có link booking salon | 1. Mở link booking salon (chưa là bạn) → follow add bot → hiển thị link booking. | - add friend với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H28 | [Web] Booking salon — check booking salon thành công | Positive | Medium | Đã add friend qua link booking salon | 1. Book salon.<br>2. Kiểm tra friend list. | - Booking salon thành công<br>- hiển thị 1 line user | | | Not test |
| TC-H29 | [Web] Booking salon — scenario send quick test | Positive | Medium | Friend từ booking salon; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H30 | [Web] Booking salon — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H31 | [Web] Booking salon — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H32 | [Web] Mở link booking event => add friend | Positive | High | User chưa là bạn; có link booking event | 1. Mở link booking event (chưa là bạn) → follow add bot → hiển thị link booking. | - add friend với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H33 | [Web] Booking event — check booking event thành công | Positive | Medium | Đã add friend qua link booking event | 1. Book event.<br>2. Kiểm tra friend list. | - Booking event thành công<br>- hiển thị 1 line user | | | Not test |
| TC-H34 | [Web] Booking event — scenario send quick test | Positive | Medium | Friend từ booking event; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H35 | [Web] Booking event — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H36 | [Web] Booking event — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H37 | [Web] Mở link item => add friend | Positive | High | User chưa là bạn; có link item | 1. Mở link item (chưa là bạn) → follow add bot → hiển thị link.<br>2. Kiểm tra friend list. | - add friend với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |
| TC-H38 | [Web] Item — check mua item | Positive | Medium | Đã add friend qua link item | 1. Mua item.<br>2. Kiểm tra friend list. | - item thành công<br>- hiển thị 1 line user | | | Not test |
| TC-H39 | [Web] Item — scenario send quick test | Positive | Medium | Friend từ item; scenario | 1. Gửi scenario send quick test. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng | | | Not test |
| TC-H40 | [Web] Item — scenario send khi đến giờ gửi step | Positive | Medium | Scenario có step hẹn giờ | 1. Chờ đến giờ gửi step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user | | | Not test |
| TC-H41 | [Web] Item — scenario chạy nhiều step | Positive | Medium | Scenario nhiều step | 1. Cho scenario chạy qua nhiều step. | - chỉ hiển thị 1 line_user<br>- send cho 1 user tương ứng<br>- lịch sử send chỉ hiển thị 1 line_user<br>- Mỗi step chỉ gửi 1 lần<br>- Không gửi trùng message | | | Not test |
| TC-H42 | [Web] Có scenario đang chạy — friend kết bạn mới qua link form | Positive | High | Scenario đang chạy; friend kết bạn mới qua link form | 1. Trong khi scenario đang chạy, friend kết bạn mới qua link form.<br>2. Kiểm tra friend list. | - Kết bạn với bot thành công<br>- Tạo 1 line_user<br>- Không có duplicate line_user<br>- hiển thị ở GUI 1 line user | | | Not test |

## TC List — Phần B: TC delta (Claude bổ sung phần human chưa cover)

> Bug bản chất là **race condition**: web `checkFriend` (mở link form/booking) đua với job follow-callback (`doHandleFollowEvent`) cùng `line_id` → tạo 2 line_user trùng → 1 khách thành 2 account, scenario chạy song song. Fix = sau insert check lại theo line_id, giữ bản id nhỏ nhất, xóa bản vừa tạo (job side: `HandlePostbackTask`; hoặc web side: `QRCodeController::checkFriend` / `FormAnswerController` tùy branch merge).
>
> 42 TC human đã cover **happy-path "verify 1 line_user"** cho mọi entry-point (follow/qr/form/booking/item) + scenario step. Delta dưới đây bù: **ép race, dedup đúng (keep-min-id + cascade), double-click, không xóa nhầm user khác, edge block/đã-xóa, entry PC/external-browser, scenario không double-send**.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-D01 | **[BUG reproduce]** Race web `checkFriend` ⨯ job `doHandleFollowEvent` cùng line_id → chỉ 1 line_user (CL-Func-25) | Boundary | High | Bot staging có scenario gắn action kết bạn; 1 tài khoản LINE chưa là bạn của bot; có link form answer của bot. Ưu tiên env **Dev (form.watermeru.com)** để dễ ép timing race. | 1. Từ tài khoản LINE chưa kết bạn, mở link form answer của bot (web `checkFriend` tạo line_user + trả màn LIFF add-friend).<br>2. NGAY khi màn LIFF/form hiện, bấm "Thêm bạn" để LINE bắn follow callback (job tạo bạn lần 2).<br>3. Lặp 5–10 lần để tăng xác suất 2 luồng chồng cửa sổ ghi.<br>4. Vào Quản lý bạn bè, tìm user vừa thêm. | Màn Quản lý bạn bè chỉ hiển thị **1** tài khoản cho user (không 2 dòng trùng tên/ảnh). Chat 1:1 chỉ **1** hội thoại. Scenario kết bạn chỉ chạy trên 1 bản ghi (không có 2 luồng step song song). | | | |
| TC-D02 | Dedup giữ line_user **id nhỏ nhất**, gộp conversation/lịch sử chat về 1 account (CL-Func-10) | Boundary | High | Tái hiện được trùng như TC-D01 (hoặc dùng user đã trùng sẵn). | 1. Gây trùng line_user cho user X (theo TC-D01).<br>2. Mở Quản lý bạn bè → chat 1:1 với X.<br>3. Kiểm tra lịch sử hội thoại + tin add-friend + thông tin friend info. | Còn đúng **1** account (bản tạo trước được giữ lại). Hội thoại/tin nhắn KHÔNG bị tách 2 luồng, không mất tin add-friend. KHÔNG xuất hiện account "rỗng" mồ côi trong list/search. | | | |
| TC-D03 | Double-click "Thêm bạn" / mở link form liên tiếp KHÔNG tạo line_user trùng (CL-Func-5) | Negative | Medium | User chưa kết bạn với bot. | 1. Mở link form, bấm "Thêm bạn" 2 lần thật nhanh.<br>2. Hoặc mở lại link form 3–4 lần liên tiếp trước khi hoàn tất kết bạn.<br>3. Hoàn tất kết bạn → vào friend list. | Chỉ **1** line_user; account không nhân đôi; scenario/tin add-friend chỉ chạy & gửi **1 lần** (không gửi lặp). | | | |
| TC-D04 | 2 user khác line_id (A, B) cùng kết bạn/mở link đồng thời — dedup KHÔNG xóa nhầm account khác (CL-Func-11) | Negative | High | 2 tài khoản LINE A và B đều chưa là bạn của bot. | 1. Cho A và B cùng mở link form + "Thêm bạn" gần như đồng thời.<br>2. Vào friend list kiểm tra cả A và B.<br>3. Xóa friend A, kiểm tra lại B. | Có đúng **2** account (A và B), mỗi user 1 bản ghi; KHÔNG account nào bị xóa nhầm; scenario chạy độc lập đúng từng user. Xóa A KHÔNG ảnh hưởng dữ liệu/hội thoại của B. | | | |
| TC-D05 | Friend đang **block** bot → mở link/re-follow không sinh line_user trùng, không double scenario (C.2 friend block) | Negative | Medium | User đã từng kết bạn rồi **block** bot. | 1. User block bot.<br>2. User mở link form (web `checkFriend`) rồi unblock / re-follow.<br>3. Kiểm tra friend list + lịch sử gửi scenario. | Vẫn **1** account cho user, không tạo bản trùng. Trong lúc block: KHÔNG gửi message/scenario. Sau unblock: dùng đúng account cũ, scenario tiếp đúng tiến trình (không chạy lại từ đầu trên bản trùng). | | | |
| TC-D06 | Friend đã **xóa mềm** trên tool → re-add qua link không sinh line_user trùng (TC-12 đối tượng đã xóa) | Negative | Medium | User có line_user đã bị xóa (soft-delete) trên tool. | 1. Xóa friend X trên tool.<br>2. User X mở link form/booking → kết bạn lại.<br>3. Vào friend list + scenario list. | Tạo/khôi phục đúng **1** account cho X (không đồng thời tồn tại bản đã-xóa + bản mới gây trùng hiển thị). Scenario không chạy song song trên 2 bản. | | | |
| TC-D07 | `checkAddGroup`: thêm **member mới** vào group đúng lúc member gửi tin → group_line_user không nhân đôi (F6) | Regression | Medium | Bot đã ở trong 1 group; có member chưa từng tương tác. | 1. Thêm member mới vào group.<br>2. Member đó gửi tin trong group gần như cùng lúc.<br>3. Vào Quản lý bạn bè (group) kiểm tra member. | Member chỉ tạo **1** line_user / 1 line_user_group; không nhân đôi member trong group; tin nhắn group hiển thị đúng 1 nguồn. | | | |
| TC-D08 | Mở link form/booking từ **PC / trình duyệt ngoài** (open_external_browser) chưa kết bạn → 1 line_user (CL-Func-13) | Boundary | High | User chưa kết bạn; có link form/booking; thiết bị PC hoặc trình duyệt ngoài (không phải in-app LINE). | 1. Mở link form/booking trên **PC** (hoặc Safari/Chrome ngoài LINE) → web `checkFriend` (open_external_browser) tạo line_user + redirect màn kết bạn.<br>2. Thực hiện kết bạn (job follow callback).<br>3. Vào friend list. | Sau kết bạn chỉ **1** line_user cho user; redirect màn kết bạn đúng; không sinh tài khoản trùng dù entry qua external browser/PC. | | | |
| TC-D09 | Access link **Conversion / QR code** chưa là bạn → redirect kết bạn → 1 line_user (CL-Func-13) | Regression | Medium | User chưa kết bạn; có link conversion + QR code của bot. | 1. User mở link Conversion (chưa là bạn) → redirect kết bạn → hoàn tất.<br>2. Lặp với QR code.<br>3. Vào friend list. | Mỗi luồng tạo đúng **1** line_user; không trùng; action conversion/QR chạy đúng 1 lần. | | | |
| TC-D10 | Scenario step KHÔNG gửi trùng & không chạy song song sau khi hết trùng line_user (T4, C.2 duplicate) | Regression | High | User đã được dedup về 1 line_user; có scenario nhiều step gắn cho user. | 1. Cho scenario chạy qua nhiều step (send quick test + đến giờ gửi step).<br>2. Mở lịch sử gửi của user trong scenario + chat 1:1.<br>3. Đối chiếu số lần nhận thực tế trên máy LINE của user. | Mỗi step gửi **đúng 1 lần**; lịch sử gửi chỉ **1 dòng/step** cho user; KHÔNG có 2 luồng step song song; user nhận đúng số message (không trùng). _(Hoàn thiện expected cho case human để trống ở row 92.)_ | | | |
| TC-D11 | Friend **block** giữa lúc scenario đang chạy → KHÔNG send step tiếp (C.2 friend block) | Negative | Medium | User đang trong scenario nhiều step, còn step chưa gửi. | 1. Khi scenario đang chạy dở, user block bot.<br>2. Chờ tới giờ step kế tiếp.<br>3. Kiểm tra lịch sử gửi + máy user. | Step sau thời điểm block KHÔNG được gửi (không action + không remind); lịch sử không ghi gửi thành công cho step đó. | | | |

### Chú thích cột

- **Type**: `Positive` happy path · `Negative` input/điều kiện sai · `Boundary` biên/race/multi-tab · `Regression` tính năng cũ không hỏng.
- **Priority**: `High` block release · `Medium` có workaround · `Low` nice-to-have.
- **Output note** / **Assignee** / **Status**: để trống — QA fill sau khi run.

### Environment (note)

Mặc định **Staging** (`staging.lme.jp`). Các TC ép race (TC-D01, TC-D02, TC-D04) **khó tái hiện thủ công** → ưu tiên env **Dev (`form.watermeru.com`)** để dễ ép timing 2 luồng chồng nhau (hoặc nhờ Dev hỗ trợ tạo data trùng sẵn). Nếu không ép được race trên Staging, ghi rõ vào Output note thay vì kết luận "không reproduce = pass".

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (chưa có file 02 — tham chiếu `templates/LME-SYSTEM-SPEC.md`, member bổ sung sau)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] **Mỗi impact** 4.1/4.2/4.3 có ≥1 TC verify (delta + reuse TC human — xem map cuối)
- [x] Có ≥1 TC verify trực tiếp bug fix (TC-D01 reproduce flow race)
- [x] Có ≥1 TC regression cho mỗi tính năng 4.3 (T1→reuse row80 + TC-D08/D12; T2→row81; T3→TC-D07; T4→TC-D10)
- [x] Có ≥1 negative + boundary cho data D1 (TC-D01/D02/D03/D04)
- [x] Mọi TC delta có steps rõ + expected đo lường được (quan sát qua GUI friend list / chat / lịch sử gửi)
- [x] Title chứa keyword function/data/feature để Leader map impact

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mục **liên quan** task này:

**§A Checklist web**:
- [x] A.1 — **CL-Func-25** (concurrent/race → TC-D01/D03/D04) · **CL-Func-13** (access link tool, in-app/external/PC → TC-D08/D09 + human Nhóm2) · **CL-Func-11** (không xóa nhầm account → TC-D04) · **CL-Func-5** (double-click → TC-D03) · **CL-Func-10** (xóa data cascade → TC-D02) · **TC-12** (block/đã xóa → TC-D05/D06/D11)
- [x] A.2 — **Regression** bắt buộc (CL-NonF-6 data cũ chạy bình thường; **CL-NonF-9 job side** — fix nằm ở job callback `HandlePostbackTask`). Security: **N/A** (không có URL/màn mới, `checkFriend` là route cũ). Compatibility: chạm nhẹ qua CL-Func-13 (in-app/external/PC) → đã đưa vào TC-D08.

**§B Checklist job**:
- [x] B.1 Job callback — **áp dụng** (fix ở callback follow `doHandleFollowEvent`; sheet gốc chưa có item nhưng task chạm trực tiếp). Cover bởi TC-D01/D10.
- [ ] B.2 CLJ01 Job sync Java — N/A (không chạm Google sync).

**§C Các tính năng chung**:
- [ ] C.1 Bill tiền — N/A
- [x] C.2 Send message — Scenario là nguồn send #2 (job) + #11 (send test); "gửi duplicate không?" + "friend block → không send" → TC-D10/D11 + human scenario rows
- [ ] C.3 Friend info — chạm gián tiếp (friend info gộp về 1 account khi dedup); member verify thủ công nếu cần
- [ ] C.4 Tag — N/A
- [ ] C.5 Google sheet — N/A (form answer ghi spread không thuộc scope dedup)
- [ ] C.6 Google calendar — N/A
- [ ] C.7 Plan limits — N/A
- [ ] C.8 Sort — N/A

---

## Map coverage nội bộ (Claude track — Leader verify)

| Impact / Nguồn | Cover bởi |
|---|---|
| BUG (race reproduce) | **TC-D01** (delta) |
| D1 line_user dedup (giữ min-id, xóa bản trùng) | TC-D01, TC-D02, TC-D03, TC-D04 |
| D1 cascade conversation/bot_line_user/group | TC-D02 (CL-Func-10) |
| D2 ES không sync bản trùng | TC-D01/D02 (quan sát: search/list friend chỉ 1) |
| F3/T1 `doHandleFollowEvent` (follow mới + bạn cũ) | reuse human row 80 (OK), row 81; + TC-D08/D12-equiv |
| F4/T2 `checkAddOldFriend` | reuse human row 81 |
| F5/F6/T3 `checkAddGroupFriend` / `checkAddGroup` | reuse human row 82 + **TC-D07** (member add — delta) |
| F1 `checkDuplicateLineUserAfterInsert` (logic dedup) | TC-D01/D02/D03/D04 |
| T4 Scenario không chạy song song | **TC-D10**, TC-D11 + reuse human scenario rows |
| CL-Func-13 entry chưa là bạn (PC/external/conversion) | **TC-D08, TC-D09** (delta) + human Nhóm2 (form/booking/item) |
| CL-Func-11 không xóa nhầm user khác | **TC-D04** + reuse human row 95 |
