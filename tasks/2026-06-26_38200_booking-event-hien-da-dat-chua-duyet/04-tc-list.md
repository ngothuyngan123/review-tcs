<!-- sync-target: https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763 -->
<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763 | sheet=Improve 2026.05 | anchor=Main Function -->

# 04 — TC List (do AI viết — DRAFT cho member verify)

> ⚠️ **DRAFT**: Member phải đọc lại từng TC, chỉnh data/precondition cho khớp env test thật, rồi mới submit cho Leader.
> Bộ TC này là **delta** — chỉ cover phần fix #38200 (`saveAction` crash khi admin duyệt booking event có field friend-info) chưa được TC cũ "Improve 2026.05" (row 463-532) cover. TC cũ về hiển thị status 1-7 + modal 操作履歴 giữ nguyên (read-only, không bị fix chạm).
> **TC001–TC011**: bộ gốc do `/write-tc` sinh. **TC012–TC018**: bổ sung từ review report (§5) sau khi đối chiếu 2 sheet feature đầy đủ "Event booking 1.0/2.0" (gồm Bug #32366 approve-request-change). Xem `05-review-report.md` để biết lý do từng TC.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | v1 |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763 (tab "Improve 2026.05", row 463-532 — TC cũ tham chiếu) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | saveAction approve booking event có field SĐT(電話番号): không crash, gửi action (repro Lỗi ②) | Positive | High | - Event booking chế độ 「リクエスト制」(cần admin duyệt).<br>- Form đặt chỗ có cấu hình thu **電話番号 (SĐT)**.<br>- 1 LINE friend đã kết bạn bot, đã gửi request booking (status 来店リクエスト).<br>- Booking có gắn action (vd template/message khi duyệt). | 1. Admin web → màn quản lý đặt chỗ event → mở booking đang ở 来店リクエスト.<br>2. Nhấn 承認 (duyệt).<br>3. Quan sát màn admin sau khi nhấn.<br>4. Mở LINE của friend kiểm tra tin nhắn. | - Màn admin KHÔNG hiện màn lỗi / 500 (trước fix văng `Undefined variable: lineUserForHistory`).<br>- Booking chuyển sang **来店予定**.<br>- Friend **nhận được** action/notification trên LINE (trước fix không nhận do crash sau khi đổi status). | | | |
| TC002 | saveAction approve booking event có field Tuổi(年齢): không crash | Positive | High | Như TC001 nhưng form thu **年齢 (Tuổi)** thay vì SĐT. | 1. Admin mở booking 来店リクエスト có field 年齢.<br>2. Nhấn 承認. | - Không màn lỗi.<br>- Status → 来店予定.<br>- Action gửi tới friend. | | | |
| TC003 | saveAction approve booking event có field Tỉnh(都道府県): không crash | Positive | High | Như TC001 nhưng form thu **都道府県 (Tỉnh/thành)** thay vì SĐT. | 1. Admin mở booking 来店リクエスト có field 都道府県.<br>2. Nhấn 承認. | - Không màn lỗi.<br>- Status → 来店予定.<br>- Action gửi tới friend. | | | |
| TC004 | saveAction approve booking event KHÔNG có field friend-info: fix không phá nhánh non-trigger | Regression | High | Event booking リクエスト制, form đặt chỗ **không** thu field friend-info nào (chỉ field thường). Friend đã gửi request booking. | 1. Admin mở booking 来店リクエスト.<br>2. Nhấn 承認. | - Approve thành công, status → 来店予定, action gửi tới friend — hành vi không đổi so với trước fix (nhánh không đi qua case -2/-4/-6). | | | |
| TC005 | saveAction approve booking có nhiều field friend-info (SĐT+Tuổi+Tỉnh): lịch sử friend info ghi đúng, không trùng | Boundary | Medium | Form đặt chỗ thu **cả 3** field 電話番号 + 年齢 + 都道府県. Friend gửi request booking với đủ 3 giá trị. | 1. Admin nhấn 承認 booking.<br>2. Vào detail friend → tab 基本情報 / lịch sử cập nhật friend info.<br>3. Đếm số bản ghi lịch sử cho mỗi field. | - Không crash.<br>- 3 field SĐT/Tuổi/Tỉnh đều được lưu đúng giá trị friend nhập.<br>- Mỗi field chỉ ghi **1 bản ghi lịch sử / 1 lần duyệt** (verify yokoten: dev cảnh báo có thể ghi TRÙNG ở case -2/-4/-6 do bad-merge). | Map yokoten "ghi lịch sử trùng". Nếu thấy trùng → NG, báo Leader. | | |
| TC006 | saveAction approve booking khi friend đã hủy kết bạn (lineUser null): xử lý null không crash | Boundary | Medium | Friend gửi request booking event (có field friend-info) → sau đó **block/hủy kết bạn** bot trước khi admin duyệt. | 1. Admin mở booking 来店リクエスト của friend đã hủy kết bạn.<br>2. Nhấn 承認. | - Không crash (`$lineUserForHistory` = null vẫn xử lý được, không văng exception).<br>- Status cập nhật nhất quán; nếu friend đã block thì KHÔNG gửi message (theo C.2 friend block). | Dev env (`form.watermeru.com`) nếu khó dựng trên Staging. | | |
| TC007 | Event booking リクエスト制 end-to-end: chưa duyệt KHÔNG hiện 予約済み, duyệt mới đổi (repro bug chính KH) | Regression | High | Event booking chế độ リクエスト制, form có field friend-info. 1 LINE friend chưa booking. | 1. Friend mở màn đặt chỗ event → gửi yêu cầu đặt (リクエスト).<br>2. **Trước khi** admin duyệt: friend mở lại màn trạng thái đặt chỗ của mình.<br>3. Admin web duyệt (承認) booking.<br>4. Friend mở lại màn trạng thái. | - Bước 2: phía user hiển thị **来店リクエスト** (đang chờ duyệt), **KHÔNG** hiển thị 予約済み/来店予定 (đây là triệu chứng bug gốc KH report).<br>- Bước 4: sau khi admin duyệt mới chuyển **来店予定**.<br>- Status DB chuyển 3 → 1 đúng thời điểm duyệt, không nhảy sớm. | | | |
| TC008 | saveAction: thao tác admin lỗi giữa chừng không để status "đã đặt" mồ côi (transaction yokoten) | Negative | Medium | Booking event có field friend-info. Mô phỏng lỗi ở bước lưu form_info / gửi notification SAU khi đổi status (vd ngắt mạng / inject lỗi ở Dev). | 1. Admin nhấn 承認 booking.<br>2. Gây lỗi ở bước sau khi status đã đổi (Dev: inject exception; hoặc ngắt API gửi message).<br>3. Quan sát status booking phía user + phía admin. | - Status booking **không** bị đổi sang đã đặt nếu thao tác duyệt chưa hoàn tất (lý tưởng: rollback) — HOẶC nếu đã đổi thì action vẫn được gửi.<br>- KHÔNG tái hiện tình trạng "user thấy 予約済み nhưng admin chưa duyệt xong / action không gửi". | Dev env. Verify yokoten "transaction bị comment trong saveAction" — nếu vẫn mồ côi status → báo Leader (nằm ngoài scope code fix nhưng cần ghi nhận). | | |
| TC009 | saveAction deny/cancel booking event có field friend-info: không crash, status đúng | Regression | High | Booking event có field friend-info đang ở 来店リクエスト / 変更リクエスト / キャンセルリクエスト. | 1. Admin mở booking → nhấn 否認 (deny) một request booking.<br>2. Lặp lại với thao tác cancel booking (admin nhấn キャンセル).<br>3. Quan sát status + slot. | - Không crash ở mọi thao tác admin qua saveAction.<br>- Deny → status **否認済**; slot bị 否認 **KHÔNG** bị tính chiếm chỗ (checklist TC-13).<br>- Cancel → status キャンセル. | | | |
| TC010 | Booking event sau approve hiển thị đúng trong danh sách đặt chỗ + modal 操作履歴 (regression Lỗi ①) | Regression | Medium | Booking event có field friend-info vừa được admin 承認 thành công (sau fix). | 1. Admin → màn danh sách đặt chỗ event → tìm booking vừa duyệt.<br>2. Mở modal 操作履歴 của booking.<br>3. Kiểm tra danh sách đặt chỗ và danh sách hủy. | - Booking hiển thị trong **danh sách đặt chỗ** (không biến mất khỏi cả list đặt lẫn list hủy như Lỗi ①).<br>- Modal 操作履歴 ghi mục **予約リクエスト 承認** với người thao tác = tên admin. | ⚠️ Booking cũ đã hỏng status do crash trước fix là dữ liệu lịch sử — ngoài scope code (dev xác nhận), admin rà thủ công. TC này chỉ verify booking duyệt SAU fix. | | |
| TC011 | recordFriendInfoHistory: friend info cập nhật + hiển thị đúng ở Chat 1:1 / My page sau approve (C.3) | Regression | Medium | Booking event thu field SĐT/Tuổi/Tỉnh, friend nhập giá trị khi đặt, admin vừa 承認. | 1. Sau khi approve, mở detail friend → Chat 1:1 right bar.<br>2. Mở My page → tab 基本情報.<br>3. Đối chiếu giá trị friend info với giá trị friend đã nhập khi booking. | - Giá trị SĐT/Tuổi/Tỉnh hiển thị đúng ở cả Chat 1:1 right bar và My page 基本情報.<br>- Giá trị khớp với input của friend khi đặt chỗ (logic recordFriendInfoHistory chạy trọn vẹn sau fix). | | | |
| TC012 | saveAction approve booking event **CÓ BILL** (course set tiền) + field friend-info: không crash, status + payment + action nhất quán | Positive | High | Event booking リクエスト制, course có setting số tiền (vd ¥100), form thu field SĐT. Friend đã request booking + đã nhập thẻ. | 1. Admin mở booking 来店リクエスト có bill.<br>2. Nhấn 承認.<br>3. Quan sát màn admin + 決済ステータス + LINE friend. | Không crash. Status → 来店予定; 決済ステータス → 決済成功 (¥100); action gửi tới friend. Không có tình trạng status đổi nhưng bill/action lỗi giữa chừng. | Map C.1 Bill tiền. Đối chiếu sheet "Event booking 1.0". | | |
| TC013 | Verify hiển thị booking theo status ở list đặt chỗ vs list hủy (điều tra Lỗi ① ひろよ) | Regression | High | Tạo booking với từng status 1/2/3/4/5/6/7 (và status bất thường nếu reproduce được). | 1. Với mỗi status, mở màn quản lý đặt chỗ event.<br>2. Kiểm tra booking xuất hiện ở list đặt / list hủy / không list nào. | Mỗi status hiển thị đúng list theo spec (sheet "Improve 2026.05"). Xác định status nào khiến booking biến mất khỏi CẢ 2 list. | ⚠️ Confirm với Dev: status nào gây Lỗi ①, có cần fix riêng không. | | |
| TC014 | Double-click 承認 booking event: không double-approve / không ghi lịch sử trùng | Boundary | Medium | Booking event 来店リクエスト có field friend-info. | 1. Admin double-click nhanh nút 承認.<br>2. Kiểm tra status + modal 操作履歴 + lịch sử friend info. | Chỉ 1 lần approve có hiệu lực; status → 来店予定; modal 操作履歴 chỉ ghi 1 mục 予約リクエスト 承認; không ghi trùng friend info. | Liên quan transaction yokoten + CL-Func-5 double-click. | | |
| TC015 | saveAction approve booking khi friend để **trống** field friend-info: recordFriendInfoHistory xử lý empty | Boundary | Low | Form thu SĐT nhưng không bắt buộc; friend request booking **bỏ trống** SĐT. | 1. Admin nhấn 承認.<br>2. Kiểm tra detail friend → friend info SĐT. | Không crash; friend info SĐT không bị ghi giá trị rỗng sai (hoặc ghi theo spec); status → 来店予定. | | | |
| TC016 | saveAction approve **REQUEST CHANGE** (status=6) booking có field friend-info: không crash + message replace đúng ngày giờ (regression Bug #32366) | Regression | High | Event booking リクエスト制 (change phải đợi approve), form thu field SĐT/Tuổi/Tỉnh. User đã có booking approve, sau đó gửi request change (đổi slot + đổi friend-info) → tồn tại 2 bản ghi status=6. | 1. Admin mở detail **booking gốc** → nhấn 承認 (approve request change).<br>2. Lặp lại: mở **booking mới** → approve.<br>3. Quan sát màn admin + message gửi cho user. | Không crash `$lineUserForHistory`. Booking gốc bị xóa, booking mới status→1. Message replace đầy đủ event_name + ngày/giờ slot + số lượng + số tiền (theo booking mới) — KHÔNG để trống ngày giờ. | Regression Bug #32366 (sendActionBookingV1). Đối chiếu sheet "Event booking 2.0". | | |
| TC017 | saveAction approve booking có field friend-info: bản ghi remind `user_event` được tạo (không mất do crash) | Regression | Medium | Event booking リクエスト制 có field friend-info, có setting remind. Friend đã request booking (status 3, **chưa** có user_event). | 1. Admin nhấn 承認.<br>2. Kiểm tra remind / nhắc lịch event của friend (hoặc chờ tới giờ remind). | Sau approve thành công → thêm 1 bản ghi user_event cho friend. Trước fix crash giữa chừng làm remind không được tạo. | Đối chiếu sheet "Event booking 1.0". | | |
| TC018 | saveAction approve booking có field friend-info: count 参加予定/承認待ち/remain cập nhật đúng | Regression | Medium | Event booking リクエスト制, slot có max số người, có field friend-info. Friend gửi request booking → count đang ở 承認待ち. | 1. Ghi nhận count 参加予定 / 承認待ち / remain trước approve.<br>2. Admin nhấn 承認.<br>3. Đối chiếu count sau approve. | Sau approve: booking chuyển **承認待ち → 参加予定**, remain giảm 1. Trước fix crash làm count đứng sai (đúng triệu chứng 参加予定 KH có thể quan sát). | Đối chiếu sheet "Event booking 2.0". | | |

### Chú thích cột

- **Type**: `Positive` happy path đúng fix / `Negative` input-điều kiện sai, verify xử lý lỗi / `Boundary` biên (null, multi-field, race) / `Regression` verify tính năng cũ không hỏng.
- **Priority**: `High` block release / `Medium` có workaround / `Low` nice-to-have.
- **Output note** / **Assignee** / **Status**: để trống — QA fill sau khi run.

### Environment (note)

Mặc định **Staging** (`staging.lme.jp`). TC006 + TC008 cần **Dev** (`form.watermeru.com`) để inject lỗi / dựng case lineUser null (đã ghi ở Output note).

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (chưa có file 02 — tham chiếu `templates/LME-SYSTEM-SPEC.md` FA-021 Event Booking; member bổ sung sau nếu cần)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify (F1 → TC001-006/008/009; D1 → TC007/008/009; T1 → TC004/007/009/010/011)
- [x] Có **ít nhất 1 TC** verify trực tiếp bug fix (TC001 repro Lỗi ②; TC007 repro triệu chứng chính KH)
- [x] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3 (T1 Event Booking → TC004/007/009/010/011)
- [x] Có **ít nhất 1 negative + 1 boundary** cho data quan trọng D1 b_user_booking.status (Negative TC008; Boundary TC005/006)
- [x] Mọi TC đều có steps rõ ràng, expected đo lường được
- [x] Title TC chứa **keyword** (saveAction / b_user_booking / recordFriendInfoHistory / Event booking) để Leader map impact

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mục liên quan task này:

**§A Checklist web**:
- [x] A.1 Function — TC-12 (kịch bản bỏ giữa chừng → TC008), TC-13 (trạng thái hợp lệ, 否認 không tính slot → TC009), CL-Func-2 (reload sau save không lỗi — member verify thủ công)
- [x] A.2 Non-function: Regression (CL-NonF-11/6) — TC004/007/009/010/011. Security/Compatibility: **không áp dụng** (fix không thêm URL/màn mới, không đổi UI).

**§C Các tính năng chung**:
- [x] C.2 Send message — nguồn job #10 "action ở booking event" (action gửi khi approve) → TC001/007
- [x] C.3 Friend info — update qua "Event booking → user trả lời form" + hiển thị Chat 1:1 / My page → TC011 (+ không ghi trùng TC005)
- [x] C.1 Bill tiền — approve booking-có-bill đi qua saveAction → **TC012** (bill + field friend-info, verify 決済成功 + amount + action). Đối chiếu sheet "Event booking 1.0".
- [ ] C.8 Sort — không liên quan fix.

<!-- Coverage track nội bộ (KHÔNG sync lên sheet):
BUG (Undefined var lineUserForHistory) → TC001, TC007
F1 saveAction Direct → Positive TC001/002/003/012, Negative TC008, Boundary TC005/006/014/015, Regression TC004/009/016/017/018
D1 b_user_booking.status → verify TC007/012, Boundary TC005/006/014, Negative TC008, Regression TC009/010/013/018
T1 Event Booking FA-021 High → Regression e2e TC007, + TC004/009/010/011/012/016/017/018
Yokoten: ghi lịch sử trùng → TC005/014; transaction comment → TC008/014
Customer symptom Lỗi ① (booking biến mất khỏi list) → TC010 + TC013 (điều tra status, confirm Dev)
Customer symptom Lỗi ② (action không gửi khi approve) → TC001/007
Scope mở rộng (đối chiếu sheet 1.0/2.0): C.1 bill → TC012; approve request CHANGE (Bug #32366) → TC016; remind user_event → TC017; count slot/plan → TC018
-->
