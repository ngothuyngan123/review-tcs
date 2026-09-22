# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (Auto-fixbug LME) — assignee ticket: Ngô Thúy Ngần |
| Commit / Pull Request | `commit 7828ead2e1` — sns-line, 1 file changed, 5 insertions(+), 2 deletions(-) · Phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=eac2682f-e89c-473a-8cce-eb948fd0f922 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40607 |
| Branch | `ai_fixbug_40607` (base `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-10` (Journal #135742) · Commit Date (custom field) = `2026-09-10` |
| Auto-filled | `2026-09-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **CẢNH BÁO PHẠM VI (do chính Dev nêu ở phần TỰ REVIEW):** bản sửa này **KHÔNG liên quan tới 3 hiện tượng mà phiếu gốc mô tả** (nút bốc thăm không chạy action, template không hiển thị, action không chạy sau khi cộng điểm). Sau khi gỡ phần webhook, phiếu **KHÔNG còn bản sửa nào cho triệu chứng gốc**. Cần human quyết định phiếu chốt theo hướng nào trước khi test.

---

## 1. Nguyên nhân

Ở màn quản lý thông tin bạn bè, khi xoá giá trị thủ công thì dòng lịch sử được ghi mà **KHÔNG kèm người thao tác**: hai chỗ ghi lịch sử trong hàm xoá bỏ trống cả `id người thao tác` lẫn `mã nguồn thao tác thủ công`. Hàm ghi lịch sử dùng chung chỉ tra tên khi có **ĐỦ hai giá trị này**, nên cột tên bị để trống và màn lịch sử chỉ hiện chữ thủ công trơn (hoặc hiện là tự động).

Tên người thao tác được **chụp lại (snapshot) ngay lúc ghi**, lúc đọc không tra lại bảng người dùng nữa, nên hàng đã ghi thiếu thì **không hiển thị lại được**.

Các màn khác (chi tiết bạn bè, chat 1:1, ứng dụng di động) đều truyền đủ nên vẫn hiện tên — đây là **thiếu sót riêng của điểm xoá này**.

## 2. Cách fix

Sửa màn quản lý thông tin bạn bè: khi xoá giá trị thủ công, truyền thêm `id người đang đăng nhập` và `mã nguồn thao tác thủ công` vào **hai chỗ ghi lịch sử** (xoá theo từng mục và xoá hàng loạt), để dòng lịch sử hiển thị đúng tên người thao tác.

Chỉ sửa đúng hai lời gọi đó, **không đổi hành vi xoá**, không đụng khâu hiển thị. Loại thao tác vẫn tự suy ra là "xoá" vì giá trị mới để trống.

Theo yêu cầu của dev trong phiên chat, **phần sửa điểm nhận webhook LINE đã được GỠ** khỏi nhánh này (nhánh dựng lại từ nhánh phát hành, chỉ còn một commit).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendInformationController::deleteFriendInfo` — `app/Http/Controllers/Basic/FriendInformationController.php` | **ĐÃ SỬA** — 2 chỗ ghi lịch sử | Điểm gây bug: bỏ trống id người thao tác + mã nguồn thủ công |
| 2 | `recordFriendInfoHistory` — `app/Helpers/functions.php` | Không sửa | Hàm ghi dùng chung, chỉ tra tên khi **đủ** id người thao tác và mã nguồn thủ công |
| 3 | `FriendInformationHistory::getTriggerAttribute` — `app/Models/FriendInformationHistory.php` | Không sửa | Chỉ hai mã nguồn thủ công mới in kèm tên, còn lại rơi vào nhánh mặc định |
| 4 | `FriendDetailFriendInfoService::transformHistoryRow` — `app/Services/FriendDetailFriendInfoService.php` | Không sửa | Quy tắc hiển thị cột người thao tác |
| 5 | `FriendDetailFriendInfoRepository::findHistoriesForUser` / `findAllHistoriesForSetting` | Không sửa | Truy vấn đọc lịch sử, **đã bỏ nối bảng người dùng** ⇒ tên chỉ đến từ cột lưu lúc ghi |
| 6 | `FriendlistController::ajaxSaveFriendInfoField` + `FriendDetailFriendInfoService::recordFieldChange` | Không sửa | Đối chiếu — truyền đủ |
| 7 | `ChatController::saveSettingDisplayInfoItem` | Không sửa | Đối chiếu — nhánh xoá truyền đủ |
| 8 | `Api\FriendInformationController::saveCustomInfo` | Không sửa | Đối chiếu (API mobile) — truyền đủ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ liệt kê "4.1 File thay đổi" — mục F1 là file duy nhất Dev kê. F2/F3 suy từ mục 3 (hàm dùng chung / hiển thị), Leader verify lại với Dev. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FriendInformationController::deleteFriendInfo` (xoá từng mục + xoá hàng loạt 一括削除) | `app/Http/Controllers/Basic/FriendInformationController.php` | Direct | **File DUY NHẤT thay đổi** (Dev kê ở mục 4.1) |
| F2 | `recordFriendInfoHistory` | `app/Helpers/functions.php` | Indirect | Hàm ghi lịch sử **dùng chung** — nay nhận thêm 2 tham số từ F1. Không sửa nhưng mọi caller đều đi qua đây ⇒ vùng regression |
| F3 | `FriendInformationHistory::getTriggerAttribute` + `FriendDetailFriendInfoService::transformHistoryRow` | Models / Services | Indirect | Khâu hiển thị cột người thao tác — không sửa, nhưng output đổi vì input đổi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_info_history.trigger_type_start` / `trigger_from_id` / `trigger_from_name` | CREATE (ghi mới) | Từ nay **được điền** khi xoá giá trị thủ công ở màn quản lý thông tin bạn bè |
| D2 | Các dòng `friend_info_history` ghi **TRƯỚC** bản sửa | KHÔNG migrate | ⚠️ Vẫn để trống và **KHÔNG bù được**: tên là snapshot lúc ghi, lúc đọc không tra lại bảng người dùng, cột id người thao tác cũng trống nên không có nguồn để suy ra |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Information (FA-015)** — lịch sử thay đổi thông tin bạn bè hiển thị đúng tên người thao tác khi xoá giá trị thủ công | F1, D1 | Medium (Dev kê — mục 4.3 chỉ có duy nhất tính năng này) |

---

## 5. Recover data

- ✔ **Không cần recover data** (Dev khẳng định). Nhưng lưu ý D2: data lịch sử cũ **vĩnh viễn trống tên**, không có phương án bù.

## 6. Verify của Dev

| Mục | Nội dung |
|---|---|
| **Mức** | `lint` (KHÔNG có unit test / integration test / manual test với DB) |
| **Lệnh** | `php -l app/Http/Controllers/Basic/FriendInformationController.php` → No syntax errors detected<br>`git diff --stat origin/release_step_20260827...ai_fixbug_40607` → 1 file changed, 5 insertions(+), 2 deletions(-) — xác nhận chỉ còn duy nhất file này<br>Kiểm tra lại điểm nhận webhook trên nhánh: đã trở về nguyên trạng như nhánh phát hành<br>Không sửa file `.java` nên không cần compile `linect-service` |
| **Bằng chứng** | Hàm ghi lịch sử dùng chung chỉ tra tên khi có **ĐỦ** mã nguồn thao tác thủ công VÀ id người thao tác; hai lời gọi trong hàm xoá bỏ trống cả hai nên tên luôn rỗng<br>Đối chiếu chéo: màn chi tiết bạn bè, chat 1:1 (kể cả nhánh xoá) và API di động đều truyền đủ và hiển thị đúng tên ⇒ khẳng định đây là thiếu sót riêng của điểm xoá này, không phải lỗi ở khâu hiển thị<br>Truy vấn đọc lịch sử đã bỏ phần nối sang bảng người dùng ⇒ tên chỉ có thể đến từ cột đã lưu lúc ghi<br>⚠️ **Không truy cập được dữ liệu thật của khách; máy chủ phát triển nội bộ cũng không kết nối được (MySQL từ chối kết nối) nên CHƯA dump được dòng lịch sử để đối chiếu** |

---

## Rủi ro / lưu ý khi test (Dev tự nêu ở phần TỰ REVIEW — AI)

1. ⚠️ Phiếu gốc nói về **action không chạy trong tính năng bốc thăm**, nhưng nhánh hiện chỉ còn bản sửa lịch sử thao tác — **cần human quyết định phiếu này chốt theo hướng nào** trước khi push và ghi ngược Redmine, vì nội dung ghi ngược sẽ không khớp mô tả phiếu.
2. ⚠️ Phân tích điểm nhận **webhook LINE** (bỏ sót sự kiện thứ 3 trở đi và lưu ngược thứ tự) **vẫn còn nguyên trên nhánh phát hành** và đã được báo lại **sáu lần** ở các phiếu trước mà chưa lần nào được push — gỡ khỏi nhánh này **không có nghĩa là đã xử lý**.
3. ⚠️ Các dòng lịch sử cũ vẫn **trống tên vĩnh viễn**, người dùng có thể hiểu nhầm là bản sửa không ăn — phải nói rõ khi bàn giao cho tester (test trên data **mới tạo sau deploy**).
4. ⚠️ **Ba lỗi khác trong cùng hàm xoá vẫn CÒN**, không nằm trong bản fix này:
   - Không ghi lịch sử cho **6 field mặc định**
   - **Bộ đếm sai** khi xoá hàng loạt (一括削除)
   - **Bản di động không ghi lịch sử**

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] **Đã chốt phạm vi ticket**: test scope fix thực tế (lịch sử friend info) hay yêu cầu Dev bổ sung fix cho 3 triệu chứng gốc
- [ ] **Đã chốt xử lý 3 lỗi còn lại trong cùng hàm xoá** (đưa vào scope hay tách ticket)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
