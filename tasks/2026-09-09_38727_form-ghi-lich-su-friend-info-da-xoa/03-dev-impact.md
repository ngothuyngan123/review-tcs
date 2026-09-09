# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — QA assignee trên Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | repo `sns-line`, commit `235ae7ce92` (2 file) — chưa có link PR. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38727 |
| Branch | `ai_fixbug_38727` (nhánh gốc `release_step_20260623`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-26` (Journal #133033) |
| Auto-filled | `2026-09-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Ghi chú của `/new-task`** — điểm cần Leader soi khi verify:
> 1. Mục 4.1 trong báo cáo Redmine là **"File thay đổi"**, KHÔNG phải list function. Bảng F1/F2 dưới đây do `/new-task` suy ra từ mục 2 + mục 3, cần Dev xác nhận.
> 2. `recordFriendInfoHistory` là **hàm dùng chung** nhưng mục 3 chỉ kê **2 function** và **không có danh sách caller đầy đủ**. Dev chỉ nói chung chung "các luồng khác (đặt lịch/booking)". ⇒ Cần yêu cầu Dev bổ sung danh sách caller, nếu không đây là vùng bỏ lọt bug.
> 3. Mục 4.2 ghi `friend_information_value` "chỉ luồng form" — cần xác nhận các luồng khác gọi hàm ghi lịch sử có bị đổi hành vi ghi value không.

---

## 1. Nguyên nhân

Câu hỏi form gắn ghi câu trả lời vào một thông tin bạn bè tùy chỉnh. Khi thông tin bạn bè đó đã bị xóa, hàm lưu vẫn chèn giá trị và ghi lịch sử tham chiếu tới bản ghi đã mất, nên cột tên quản lý trong lịch sử bị trống.

## 2. Cách fix

Trong `FormAnswerService::storeFriendInfo`, nếu thông tin bạn bè tùy chỉnh (`id>0`) đã bị xóa (không còn setting) thì **bỏ qua chèn giá trị + ghi lịch sử**. Đồng thời **chặn tại gốc** trong helper `recordFriendInfoHistory`: `id>0` mà setting không tồn tại thì không ghi lịch sử mồ côi — nên các luồng khác (đặt lịch / booking) cũng không còn tạo lịch sử thiếu tên quản lý.

Fix độc lập branch riêng (parent `#26684` là ticket umbrella tổng hợp, không gộp).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerService::storeFriendInfo` — `app/Services/FormAnswer/FormAnswerService.php` | Thêm guard: `id>0` + setting không tồn tại ⇒ bỏ qua chèn value + ghi history | Điểm phát sinh trực tiếp lịch sử mồ côi từ luồng trả lời form |
| 2 | `recordFriendInfoHistory` — `app/Helpers/functions.php` | Thêm guard tại gốc: `id>0` mà setting không tồn tại ⇒ không ghi lịch sử | Hàm dùng chung — chặn tại gốc để mọi luồng gọi vào đều không sinh dòng mồ côi |

> ⚠️ Dev **KHÔNG kê danh sách caller** của `recordFriendInfoHistory` ngoài 2 dòng trên (chỉ nhắc "đặt lịch / booking" trong mục 2).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Báo cáo Redmine mục 4.1 chỉ liệt kê FILE thay đổi. Bảng dưới do /new-task map từ mục 2 + 3 — Dev cần xác nhận. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerService::storeFriendInfo` | `app/Services/FormAnswer/FormAnswerService.php` | Direct | Guard bỏ qua value + history khi setting đã xóa |
| F2 | `recordFriendInfoHistory` (helper dùng chung) | `app/Helpers/functions.php` | Direct | Guard tại gốc — **ảnh hưởng mọi luồng gọi vào**, không chỉ form |
| F3 | Các luồng gọi `recordFriendInfoHistory` (đặt lịch / booking, và các caller khác chưa được Dev kê) | `<chưa được Dev liệt kê>` | Indirect | ⚠️ Vùng regression chưa xác định hết — xem ghi chú ở đầu file |

**Nguyên văn mục 4.1 (File thay đổi):**
- `app/Services/FormAnswer/FormAnswerService.php`
- `app/Helpers/functions.php`

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_info_history` | CREATE (bị chặn) | Không còn phát sinh dòng mồ côi (setting đã xóa) với `friend_info_name` NULL. **Dòng mồ côi cũ giữ nguyên — không recover data.** |
| D2 | `friend_information_value` | CREATE (bị chặn) | Không còn chèn giá trị tham chiếu setting đã xóa — Dev ghi rõ **"chỉ luồng form"** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Information (FA-015)** | F1, F2, D1, D2 | High — không ghi giá trị/lịch sử khi thông tin bạn bè tùy chỉnh đã bị xóa |
| T2 | **Form Builder (FA-011)** | F1, D1, D2 | High — trả lời form ghi vào friend info bỏ qua trường đã xóa, form result vẫn phải hiển thị bình thường |
| T3 | Đặt lịch / booking (và các luồng khác gọi `recordFriendInfoHistory`) | F2 | Medium — Dev nhắc trong mục 2 nhưng **không kê tên function cụ thể** |

---

## 5. Recover data

✔ **Không cần recover data** — bản ghi `friend_info_history` mồ côi ghi trước bản fix vẫn còn trong DB (cột 管理名 trống).

## 6. Verify của Dev

| Mục | Nội dung |
|---|---|
| Mức verify | `lint` (⚠️ **không có unit test / integration test**) |
| Lệnh | `php -l FormAnswerService.php: OK` · `php -l functions.php: OK` · DB dev xác nhận có dòng `friend_info_history` mồ côi trước fix |
| Bằng chứng | orphan `friend_info_history` rows: `id=13 setting=1285 name=NULL`, `id=14 setting=1287 name=NULL` (setting đã xóa) |

## 7. Tự review của AI (nguyên văn)

```
Guard đặt đúng chỗ: chỉ bỏ qua khi id>0 và setting không tồn tại; field mặc định id<0 (-1..-10) vẫn ghi bình thường (địa chỉ -7..-10, tên/điện thoại/email/sinh nhật/tỉnh). Không đụng luồng lưu form_answer_result nên form result + chi tiết câu trả lời vẫn hiển thị.
 • Rủi ro / lưu ý khi test:
   - Không phát hiện được nếu có luồng nào cố ý ghi lịch sử cho id âm ngoài -1..-10 (đã kiểm: không có)
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (⚠️ **hiện đang THIẾU danh sách caller của hàm dùng chung `recordFriendInfoHistory`** — hỏi Dev)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
