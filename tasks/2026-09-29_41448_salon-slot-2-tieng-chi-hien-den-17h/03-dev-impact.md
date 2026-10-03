# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41448 — refresh 2026-10-02 theo **Journal #139595** (cập nhật tiến độ, 2026-10-01, commit `7087f665bd` — vá bug MỚI #41822/#41823) + **Journal #139716** (báo cáo đầy đủ lần 3, 2026-10-01, commit `a4c92a8626`). Bản trước (Journal #139287 commit `d199db2c03` · Journal #139421 commit `e8931817a2`) **đã lỗi thời** — đã merge vào `release_step_20260930`, nay là base cho vòng vá mới. Nội dung giữ nguyên văn, chỉ chia vào đúng mục template.
>
> ⚠️ **Vòng vá này sinh ra TỪ chính TC do Leader/reviewer đề xuất ở round 2** (`TC-FUNC004-11` — Calendar 個人 · Option 3 limit 2): TC fail trên staging + prd (3 lần, 3 tester) → log Redmine **#41822** (reject #41823 vì trùng) → Dev tìm ra lỗi đếm lượt đặt `staff_id=0` HAI LẦN ở calendar 個人 → vá commit `7087f665bd`. Xem §4 GAP review round 2 (G5).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) · Assignee Redmine: Đỗ Quyên |
| Commit / Pull Request | `sns-line` commit fix thuần cuối `e8931817a2` (Journal #139421) — trước đó `d199db2c03` (5 file). Studio `dev_impact`: tip `origin/ai_fixbug_41448` = `8fd8a99592` (merge `release_step_20260930`), diff sạch = `69eeb2a6be..e8931817a2`. Chưa có link PR |
| Branch | `ai_fixbug_41448` (nhánh gốc `release_step_20260827`) — đã push. ⚠ Branch còn chứa commit `daf6b323f2` của ticket #41741 (phiên khác) |
| Ngày submit đánh giá | 2026-09-29 (Journal #139287) · cập nhật 2026-09-30 (Journal #139421) |
| Auto-filled | 2026-09-29 by /new-task · refresh 2026-09-30 |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bộ tính khung giờ Salon chia khoảng đặt thành nhiều đoạn nhỏ, mỗi đoạn lại đòi nhân viên phải còn trong ca. Nhưng khoảng đặt gồm cả 片付け時間 (dọn dẹp) ở đuôi — phần này theo thiết kế đã chốt ở #40128 ĐƯỢC phép tràn qua giờ tan ca, chỉ giờ PHỤC VỤ mới bắt buộc nằm trong ca. Hai bước trong cùng một luồng đang dùng hai chuẩn khác nhau: getListStaffValidInRangeOpt3 (đã trừ phần nghỉ) công nhận nhân viên ca ngắn phục vụ được khung này, rồi vòng duyệt từng đoạn ngay sau đó lại tước suất của chính họ ở đoạn chỉ còn dọn dẹp. Khi nhân viên có ca dài hơn đang bận (booking của người đó cũng bị kéo dài thêm 片付け), tổng suất còn lại tụt xuống bằng số booking đang chiếm → hệ thống kết luận đã đầy và ẩn khung, dù thực tế vẫn còn người phục vụ được trọn buổi.

VÍ DỤ ĐÃ TÁI HIỆN (cal 1239, ngày 2026-09-26, khung 17:30): khoảng bị chiếm trải 17:30→20:29 (phục vụ tới 19:30 + 1h dọn dẹp). Tại đoạn 20:00–20:29 chỉ còn dọn dẹp: staff 622 (ca tới 20:00, người lẽ ra phục vụ) bị đánh 'ngoài ca' → trừ suất, sumSlotTmp 2−1=1; staff 621 (ca tới 20:30) còn ca nhưng đang bận → countBooking=1 → sumSlotTmp(1) <= countBooking(1) và count(staffFalse) 2 >= count(listStaffValidInRange) 2 → chặn khung.

Vị trí lỗi: `CalendarSalonLineBookingService::checkStaffFalse` dòng 1856 (và dòng 2239 trong `checkLimitNoStaff`) truyền mốc của ĐOẠN vào `checkRangeInWorkingTime` thay vì mốc cuối giờ phục vụ.

## 2. Cách fix

**Fix gốc của #41448 (lớp 片付け時間)** — Journal #139287:

Tính `$serviceEndTs` = mốc cuối dải slot − breakTimeAfterApplied; thêm helper `getRangeForWorkingCheck()` — đoạn đã sang phần 片付け VẪN được kiểm 'còn trong ca' nhưng kiểm tại MỐC CUỐI GIỜ PHỤC VỤ thay vì tại mốc của đoạn (KHÔNG bỏ hẳn phép kiểm, vì bỏ sẽ mất lớp chặn với nhân viên tan ca GIỮA một đoạn — case bẫy E21); dùng ở `checkStaffFalse` và `checkLimitNoStaff` (nhánh 指名なし). Cố ý KHÔNG vá `checkLimitHasStaff` (nhánh chỉ định NV không dính bug; đo 37.440 tổ hợp không đổi kết luận nào). ⚠ Branch còn chứa commit `daf6b323f2` của ticket #41741 (`filterStaffWorkingAtServiceEnd`) — của phiên khác, không thuộc ticket này. 3 commit fix các bug mới của #41706 (P3/P4/P6) ĐÃ ĐƯỢC GỠ khỏi branch này theo yêu cầu human 29/09 và giữ ở branch riêng `ai_fixbug_41706` (HEAD `7c04671199`) để dùng sau.

**Bổ sung 2026-09-29 — fix 7 ticket con QA (#41740–#41746) trên cùng branch** — Journal #139287:

- **#41742** nghỉ TRƯỚC được phép nằm trước giờ vào ca: `getStartAndEndBooking` trả thêm `breakTimeFirstApplied`; `getRangeForWorkingCheck` xét đoạn chuẩn bị tại mốc BẮT ĐẦU phục vụ; `getListStaffValidInRange` chỉ đòi ca phủ từ lúc bắt đầu phục vụ.
- **#41746** khung cuối ca không bị ẩn: `getListStaffValidInRange` nhận mốc phục vụ thật (trước suy từ `$endDatetime` đã +1 phút); `findLimitRangeSlotBooking` xét mốc cuối dải theo phút cuối bị chiếm; bỏ +1 phút ở 2 cổng chặn giờ tan ca; bỏ qua đoạn rộng 0 phút ở cuối dải; controller gộp ca cho cả chế độ 合算をする để một buổi có thể do nhiều NV thay phiên.
- **#41745** chống nới lỏng: `filterStaffWorkingAtServiceEnd` nay kiểm CẢ mốc bắt đầu phục vụ — người vào ca muộn không còn góp suất che mất người khác đang bận.
- **#41743** hai khách đặt đồng thời: thay chốt chặn cũ (so hạn mức cấu hình + cùng giây) bằng chạy lại chính `checkCanBooking` chỉ tính đơn có id nhỏ hơn → đơn sau tự huỷ, luôn còn đúng 1 đơn.
- **#41740 / #41744** đã đạt sẵn ở HEAD (do 3 commit cũ đã revert) — đo lại đủ 4 mốc biên.

Đo lường: 32.960 khung × (ca × lượt đã đặt × option × khoá × nghỉ) — lỗ hổng đặt trùng 161→0, chặn oan 1491→8. PHPUnit 17/17 xanh (5 test mới, 3 fail trên code cũ).

**Cập nhật 2026-09-30 — branch đi tiếp 4 commit (`d199db2c03` → `e8931817a2`)** — Journal #139421 (nguyên văn, bỏ dấu):

```
■ CAC BAN VA THEM SO VOI NOTE TRUOC (d199db2c03)
  1. Han muc moi nhan vien tinh theo SO LUOT DONG THOI, khong phai tong so luot trong khung.
     Truoc: NV han muc 2 co hai luot NOI TIEP (18:00-19:00 roi 19:00-20:00) bi coi nhu het
     suat du luc nao cung chi ban 1 -> khung bien mat. (commit c6adf066a8)
  2. Nhanh chi dinh nhan vien cung xet ca cua nhung nguoi khac tai MOC GIO PHUC VU
     thay vi moc tho cua tung doan (nhat quan voi 2 vong lap con lai). (commit 23492bfad5)
  3. Chong dat trung dong thoi: bat \Throwable thay vi chi \Exception — loi kieu \Error
     truoc day lam don 'ma' o lai chiem khung. (commit e8931817a2)
  4. Job phan bo nhan vien PHIA KHACH: bo phep cong du 1 phut vao moc tan ca, neu khong job
     se noi hon man hien thi dung 1 phut va co the gan nguoi cho buoi ket thuc sau gio tan ca.
  5. Chong dat trung dong thoi da phu CA LUONG CO THANH TOAN (Stripe / Univapay / tra sau),
     chay TRUOC buoc tru tien nen ban du bi huy khi chua tinh tien.
```

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn Dev (Journal #139287 mục 3). Cột "Thay đổi" đối chiếu với mục 4.1 của cùng journal + Journal #139421 — **danh sách mục 3 của Dev chưa cập nhật theo 4.1** (vd `checkLimitHasStaff` mục 3 ghi "KHÔNG sửa" nhưng 4.1 + #139421 ghi đã sửa).

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonLineBookingService::checkSlotBookingIsValidType0` | Sửa | Tính `$serviceEndTs` (+ `serviceStartTs`), truyền xuống `checkLimitNoStaff` |
| 2 | `CalendarSalonLineBookingService::getRangeForWorkingCheck` | MỚI | Chọn mốc thời điểm để kiểm 'còn trong ca' (cuối giờ phục vụ / đầu giờ phục vụ) |
| 3 | `CalendarSalonLineBookingService::checkStaffFalse` | Sửa (+ `$serviceEndTs`) | |
| 4 | `CalendarSalonLineBookingService::checkLimitNoStaff` | Sửa (+ `$serviceEndTs`) | Truyền tiếp xuống `checkStaffFalse` |
| 5 | `CalendarSalonLineBookingService::checkLimitHasStaff` | Mục 3 Dev ghi "KHÔNG sửa" · **4.1 + Journal #139421 ghi ĐÃ sửa** (commit `23492bfad5`) | Nhánh chỉ định NV xét ca người khác tại mốc giờ phục vụ |
| 6 | `CalendarSalonLineBookingService::checkRangeInWorkingTime` | Không sửa | |
| 7 | `CalendarSalonLineBookingService::getListStaffValidInRangeOpt3` / `getListStaffValidInRange` | Mục 3 ghi "nguồn nguyên tắc #40128" · 4.1 ghi `getListStaffValidInRange` ĐÃ sửa (#41742, #41746) | |
| 8 | `CalendarSalonLineBookingService::getStartAndEndBooking` | Sửa (trả thêm `breakTimeFirstApplied`) | |
| 9 | `CalendarSalonLineBookingService::isReachMaxBooking` | Sửa (4.1) | Entry point dùng chung 5 nơi gọi |
| 10 | `Mobile\CalendarSalonController::getListTimeBooking` / `order` / `showTimeBookingMonth` | Sửa (4.1: `checkCanBooking`, `rejectDuplicateSalonBooking`, `order`, gộp ca) | Caller |
| 11 | `Jobs\CalendarSalonStaffAssignment` + `CalendarSalonStaffAssignmentAdmin` | Sửa (+`breakTimeFirstApplied`; job phía khách bỏ +1 phút) | Caller (job phân bổ nhân viên) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `checkSlotBookingIsValidType0` — `serviceEndTs` + `serviceStartTs` | app/Services/CalendarSalon/CalendarSalonLineBookingService.php | Direct | Fix gốc + #41742 |
| F2 | `getRangeForWorkingCheck` (mới) | nt | Direct | Mốc kiểm 'còn trong ca' ở phần 片付け (sau) và phần chuẩn bị (trước) |
| F3 | `checkStaffFalse` · `checkLimitNoStaff` | nt | Direct | Nhánh 指名なし |
| F4 | `checkLimitHasStaff` | nt | Direct | Nhánh 指名 — xét ca người khác tại mốc giờ phục vụ (commit `23492bfad5`) |
| F5 | `filterStaffWorkingAtServiceEnd` (kiểm cả mốc bắt đầu, #41745) · `hasStaffCanTakeWholeRange` (≥ 1 NV nhận trọn khoảng — áp **cả option 上限を設定しない**) | nt | Direct | Chống mở oan |
| F6 | Hạn mức mỗi NV = số lượt **đồng thời** (`maxConcurrentBookings` / `isOverlapRange`, commit `c6adf066a8`) · suất còn phải > số đơn 指名なし chưa gán | nt | Direct | Studio `dev_impact` |
| F7 | `getListStaffValidInRange` · `findLimitRangeSlotBooking` · `getStartAndEndBooking` · `checkLimitShiftsNotCombined` · `isReachMaxBooking` · `getListBookingConfirm` | nt | Direct | #41746: mốc phục vụ thật, bỏ +1 phút, bỏ đoạn 0 phút |
| F8 | `Mobile\CalendarSalonController`: `checkCanBooking` (+`$maxBookingId`) · `rejectDuplicateSalonBooking` (viết lại, bắt `\Throwable`, phủ luồng thanh toán Stripe / Univapay / trả sau, chạy trước bước trừ tiền) · `order` (closure kiểm lại chỗ trống) · 3 chỗ gộp ca nay áp cho cả 合算をする · hằng số `MESSAGE_SLOT_FULL` | app/Http/Controllers/Mobile/CalendarSalonController.php (+95/−66 ở #139287; Studio: +233) | Direct | #41743 + Journal #139421 mục 3, 5 |
| F9 | `Jobs\CalendarSalonStaffAssignment` (+`breakTimeFirstApplied`, bỏ +1 phút mốc tan ca) · `CalendarSalonStaffAssignmentAdmin` (+`breakTimeFirstApplied`) | app/Jobs/ | Direct | Job phân bổ đánh giá cùng mốc với hiển thị |

> Nguyên văn Dev 4.1 (Journal #139287):
> - app/Services/CalendarSalon/CalendarSalonLineBookingService.php (+236/−22) — checkSlotBookingIsValidType0, getRangeForWorkingCheck, filterStaffWorkingAtServiceEnd, checkStaffFalse, checkLimitNoStaff, checkLimitHasStaff, checkLimitShiftsNotCombined, getListStaffValidInRange, findLimitRangeSlotBooking, getStartAndEndBooking, isReachMaxBooking, getListBookingConfirm
> - app/Http/Controllers/Mobile/CalendarSalonController.php (+95/−66) — checkCanBooking (+$maxBookingId), rejectDuplicateSalonBooking (viết lại), order (truyền closure kiểm lại chỗ trống), 3 chỗ gộp ca nay áp cho cả 合算をする, hằng số MESSAGE_SLOT_FULL
> - app/Jobs/CalendarSalonStaffAssignment.php (+2/−1) + app/Jobs/CalendarSalonStaffAssignmentAdmin.php (+2/−1) — truyền breakTimeFirstApplied để phân bổ NV đánh giá cùng mốc với hiển thị
> - tests/Feature/CalendarSalonSlotBoundaryTest.php (MỚI, 193 dòng) — 5 test biên đầu ca/cuối ca (3 test fail trên code trước khi vá)
>
> F4 / F5 (`hasStaffCanTakeWholeRange`) / F6 / F8 (`\Throwable`, luồng thanh toán) / F9 (bỏ +1 phút) bổ sung từ Journal #139421 + Studio `dev_impact` — Tester verify.

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có (theo Dev) | — | Nguyên văn: "Thuần logic tính toán in-memory, không thêm/bớt truy vấn, không đổi dữ liệu đã lưu". Không cần recover data. ⚠ Tester lưu ý: chống đặt trùng (#41743 + Journal #139421) có **huỷ / dọn đơn tạm** (đơn tạo sau bị xoá, đơn tạm luồng thẻ bị dọn) — Dev không kê vào 4.2 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn chọn khung giờ LIFF (getListTimeBooking) — Salon | F1–F7 | High |
| T2 | Lịch tháng LIFF (showTimeBookingMonth) | F7 | Medium |
| T3 | Đặt lịch (order) + chống đặt trùng đồng thời, **gồm luồng có thanh toán** Stripe / Univapay / trả sau | F8 | High |
| T4 | Job phân bổ nhân viên tự động phía khách (CalendarSalonStaffAssignment) | F9 | High |
| T5 | Job phân bổ nhân viên phía admin (CalendarSalonStaffAssignmentAdmin) | F9 | Medium |
| T6 | Option 「上限を設定しない」 (type 0) — **nay đổi hành vi** | F5, F6, F7 | High |
| T7 | Option 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をする」 — gộp ca, nhiều NV thay phiên phục vụ 1 buổi | F8 (gộp ca), F7 | High |
| T8 | Luồng khách chọn đích danh nhân viên (指名) — cả 3 option | F4 | High |
| T9 | Option 「上限を設定する」 — nghỉ TRƯỚC / NV vào ca muộn | F1, F2, F5 | High |

> Cột "Nguy cơ regression" do `/new-task` gán theo mô tả rủi ro của Dev — Dev không ghi mức. Studio `dev_impact`: "Phạm vi hồi quy CAO & RỘNG: cả 3 option 予約受付上限 (0/1/2) × cả 2 luồng (指名なし/指名)". Nguyên văn Dev 4.3 (Journal #139287, phần còn hiệu lực) + phạm vi retest (Journal #139421):

```
- ⚠ PHẠM VI (đã hiệu chỉnh bởi tự review v1): đổi hành vi khi type_limit_calendar = 1 (上限を設定する) VÀ khách chọn 指名なし VÀ trong ngày có nhân viên lệch giờ tan ca, VÀ (lịch có cấu hình 片付け時間 time_after > 0 HOẶC có nhân viên tan ca ĐÚNG mốc kết thúc giờ PHỤC VỤ của khung). Đo 55.296 tổ hợp: 182 ô đổi khi 片付け > 0, 6 ô đổi khi 片付け = 0. Các nhánh khác (type 0, type 2 cả 合算する/しない, luồng chỉ định nhân viên): 0 ô đổi.
- ⚠ SỬA LẠI KHAI BÁO CŨ (tự review v1): bản report trước ghi "lịch KHÔNG cấu hình 片付け時間 → kết quả y hệt release" là SAI. [...] ⇒ QA PHẢI RETEST CẢ LỊCH KHÔNG CẤU HÌNH 片付け時間.
- CASE ĐỔI (trước ẩn → nay hiện): khung mà giờ PHỤC VỤ vẫn nằm trọn trong ca của một nhân viên, chỉ phần 片付け tràn qua giờ tan ca của chính người đó, trong khi nhân viên ca dài hơn đang bận. Ví dụ cal 1239 ngày 26/09: khung 17:30 và 18:00 (và 17:00) từ ẩn → hiện.
- CASE KHÔNG ĐỔI — đã kiểm bằng case bẫy: nhân viên hết ca GIỮA giờ phục vụ vẫn bị chặn (E21); nhân viên có 2 ca rời và giờ phục vụ rơi vào khoảng nghỉ giữa 2 ca vẫn bị chặn (E24); mọi nhân viên đều bận vẫn bị chặn (R3); khung vượt quá ca vẫn bị chặn (18:30 của cal 1239).
- MÀN HÌNH / JOB dùng chung isReachMaxBooking nên nới đồng bộ, không lệch nhau: màn chọn khung giờ LIFF (getListTimeBooking), lịch tháng (showTimeBookingMonth), validate lúc bấm đặt (order), job phân bổ nhân viên tự động phía khách (CalendarSalonStaffAssignment) và phía admin (CalendarSalonStaffAssignmentAdmin).
- RỦI RO CẦN THEO DÕI: (1) các bot Salon đang dùng 上限を設定する + 片付け時間 + nhân viên lệch ca sẽ thấy lịch 'thoáng' hơn trước — nên báo trước cho OEM 31074; (2) job phân bổ nhận thêm booking ở khung mới mở, cần xác nhận gán đúng nhân viên còn ca (người ca ngắn), không gán người đang bận.
- ⚠ TỒN ĐỌNG NGOÀI PHẠM VI FIX (tự review v1, cần human quyết): khung mà khoảng bị chiếm kết thúc ĐÚNG giờ tan ca (gộp ca) KHÔNG BAO GIỜ được chào, ở mọi chế độ giới hạn và cả 指名あり/なし [...] Hướng vá này human đã chủ động REVERT ngày 2026-09-25 (commit c9897b7481) nên KHÔNG tự sửa lại.
- ★ CẬP NHẬT 2026-09-29 — PHẠM VI ĐÃ RỘNG HƠN sau khi fix 7 ticket con #41740–#41746. Khai báo cũ "type 0 và type 2 không đổi" nay KHÔNG CÒN ĐÚNG: bản vá mới chạm CẢ BA option. QA phải retest cả 3.
- • 上限を設定しない (type 0): khung có giờ phục vụ kết thúc ĐÚNG giờ tan ca trước đây bị ẩn, nay hiện (getListStaffValidInRange nhận mốc phục vụ thật thay vì mốc đã cộng +1 phút).
- • 上限を設定する (type 1): thêm quy tắc nghỉ TRƯỚC được nằm ngoài ca (#41742) và siết lại — nhân viên vào ca MUỘN hơn giờ bắt đầu phục vụ không còn được giữ khung (#41745).
- • スタッフ数の合計 + 合算をする (type 2, shift_combine 2): nay GỘP ca liền nhau nên một buổi có thể do nhiều nhân viên THAY PHIÊN phục vụ (#41746 TC20949: NV-A 10:00–11:00 rồi NV-B 11:00–12:00 → khung 10:00 hiện). Đây là thay đổi hành vi rõ rệt nhất, cần QA xác nhận đúng ý nghiệp vụ.
- • Luồng ĐẶT LỊCH (không chỉ hiển thị): hai khách gửi cùng khung gần như đồng thời thì người sau nhận 予約がいっぱいです。別の枠を予約してください。 và không tạo đơn thứ hai (#41743). Cần retest cả luồng có thanh toán.
- • ĐO LƯỜNG toàn cục: 32.960 khung [...] lỗ hổng đặt trùng 161 → 0, chặn oan 1491 → 8. So A/B với release: 1486 khung mở đúng, 161 khung siết đúng, 0 nới sai, 3 siết sai (ca khoá 121 phút, hướng an toàn).
- • CÒN TỒN (không sửa trong đợt này, đã có từ release): khung đặt SÁT NHAU (buổi kết thúc đúng lúc lượt sau bắt đầu) ở option 上限を設定しない vẫn bị chặn — có thể là buffer cố ý, chờ BA xác nhận.

[Journal #139421]
■ PHAM VI RETEST DA RONG HON BAN BAO TRUOC — xin doc ky
  Ban bao truoc noi thay doi chi cham option 「上限を設定する」. KHONG CON DUNG:
  cong kiem moi (hasStaffCanTakeWholeRange + cach dem han muc) ap cho CA option
  「上限を設定しない」 (type 0). Nen retest CA BA option gioi han, o ca hai luong
  指名なし va chi dinh nhan vien.
```

---

## 4.4. Vòng vá mới 2026-10-01 — bug MỚI phát hiện qua TC round 2 (ngoài phạm vi gốc #41448)

> Hai bug này **không nằm trong khai báo gốc #41448** — phát hiện qua chính TC đề xuất ở report round 2 (`TC-FUNC004-11`, `TC-FUNC004-10`). Giữ lại ở đây vì cùng branch `ai_fixbug_41448` và cùng tính năng khung trống Salon.

**Journal #139595 (nguyên văn, bỏ dấu, 2026-10-01, commit `7087f665bd`):**

```
■ Phan viec cu DA VAO RELEASE
  Cac ban va cho #41740-#41746 va phan han muc dem theo so luot DONG THOI da duoc
  release_step_20260930 hap thu (kiem bang merge-base: 4d50ccf473 / 3ca24a9028 /
  c6adf066a8 / e8931817a2 deu la ancestor cua release). Khong con cho merge.

■ Phan moi tren branch
  commit 7087f665bd — vá #41822 / #41823: lich kieu 個人 dem luot dat staff_id = 0 HAI LAN
  nen 上限を設定する = 2 chi nhan duoc 1 luot moi khung. Loi CO SAN tren release.

■ Trang thai cong review
  AI review doc lap vong 11: PASS (0 loi bat buoc, 5 canh bao de human xem).
  Canh bao dang luu y nhat: cung kieu loi dem hai lan CO THE con o checkLimitShiftsNotCombined
  (cau hinh スタッフ数の合計 + 合算しない) — chua do duoc vi chua co TC, se xu ly khi co yeu cau.
```

**Journal #139716 (báo cáo đầy đủ, 2026-10-01, commit `a4c92a8626`):**

### 1. Nguyên nhân (2 lỗi mới)

(1) **#41743** — hồi quy của chính bản vá chống đặt trùng: `order()` kiểm chỗ trống 2 lần (trước và ngay sau khi tạo đơn); giữa 2 lần, với lịch **個人** biến `$staffId` bị gán lại thành id nhân viên thật để lưu đơn, nên lần kiểm lại xét theo kiểu 'đã chỉ định nhân viên'. Lịch 個人 không có danh sách nhân viên chọn được nên kiểu xét này luôn báo hết chỗ → đơn vừa tạo bị xoá, kể cả khi khung còn trống (**lịch 個人 không đặt được lượt nào qua luồng không thanh toán**).

(2) **#41742** ở chế độ 合算をする (nhiều nhân viên thay phiên): từ bản vá #41746, ca được gộp nên khung đi vào bộ đếm theo từng đoạn, mà bộ đếm này chỉ coi người đang có ca tại đúng đoạn đó là có mặt. Phần nghỉ trước nằm trước giờ vào ca của người sẽ phục vụ nên họ bị bỏ qua; nếu người còn lại đang bận thì khung bắt đầu đúng giờ vào ca bị ẩn oan.

### 2. Cách fix

(1) #41743: `order()` chốt `$staffIdForCheck` ngay khi đọc request và dùng chung cho cả 2 lần kiểm chỗ trống — lần kiểm lại sau khi tạo đơn xét đúng kịch bản như lần đầu. Luồng thanh toán vốn không dính nên không đổi.
(2) #41742: `findLimitRangeSlotBooking` nhận thêm mốc bắt đầu phục vụ; ở các đoạn chỉ còn nghỉ trước, người có ca tại mốc bắt đầu phục vụ cũng được tính là có mặt (CỘNG thêm, không bớt ai so với trước). Chỉ truyền mốc này cho nhánh 合算をする + 指名なし; các nhánh khác giữ nguyên.
Thêm 2 file test (3/4 test fail trên code cũ). Quét ngang: phát hiện màn lịch THÁNG truyền ngược `is_before_day`/`is_case_next_day` vào `isReachMaxBooking` (có từ 2024, khác phạm vi — chỉ ghi nhận).

### 3. Đã check function / data liên quan

- `Mobile/CalendarSalonController::order` — 2 lần gọi `checkCanBooking` + closure `rejectDuplicateSalonBooking`
- `Mobile/CalendarSalonController::paymentStripe` / `paymentUnivapay` / `createOrderPayment` — closure kiểm lại dùng `$staffId` CHƯA gán lại → không dính
- `Mobile/CalendarSalonController::checkCanBooking` — `listStaffId` rỗng với lịch 個人
- `CalendarSalonLineBookingService::isReachMaxBooking` — truyền mốc bắt đầu phục vụ cho nhánh 合算をする
- `CalendarSalonLineBookingService::findLimitRangeSlotBooking` — thêm tham số `serviceStartTs` (mặc định null)
- `CalendarSalonLineBookingService::checkLimitShiftsCombined` — đọc dải hạn mức, không đổi
- 5 nơi gọi `isReachMaxBooking` (3 controller + 2 job) — job truyền id nhân viên thật nên không vào nhánh mới

### 4. Đánh giá ảnh hưởng

**4.1 File thay đổi** (vòng mới, diff vs `release_step_20260930`):
- `app/Http/Controllers/Mobile/CalendarSalonController.php`
- `app/Services/CalendarSalon/CalendarSalonLineBookingService.php`
- `tests/Feature/CalendarSalonCombinedBreakBeforeTest.php` (MỚI)
- `tests/Feature/CalendarSalonOrderRecheckStaffIdTest.php` (MỚI)

**4.2 Data ảnh hưởng**: Không có — không đổi schema, không thêm/bớt truy vấn.

**4.3 Tính năng liên quan**:
- Đặt lịch salon (FA-020) — **lịch 個人**: gửi đặt lịch (không thanh toán) đặt được lại bình thường; hạn mức vẫn chặn đúng (REQ-010).
- Đặt lịch salon (FA-020) — lịch nhiều NV chế độ スタッフ数の合計 + シフトの合算をする có cài nghỉ trước: khung bắt đầu đúng giờ vào ca hiện lại ở màn chọn khung TUẦN và THÁNG; chỉ MỞ thêm khung, không đóng khung nào (REQ-008, REQ-009).

**Studio `dev_impact` (computed 2026-10-02):**
> Vòng mới (a4c92a8626, base release_step_20260930, merge-base 8fd8a99592) chỉ đổi 2 file prod. order(): thêm `$staffIdForCheck` dùng cho cả 2 lần kiểm → lịch 個人 không còn bị xoá đơn vừa tạo; lịch nhiều NV giá trị không đổi nên chống đặt trùng giữ nguyên. **Rủi ro**: lần kiểm lại sau khi tạo đơn với lịch 個人 nay xét theo nhánh 指名なし — phải xác nhận hạn mức 1/2 vẫn chặn đúng và 2 khách đặt đồng thời lịch 個人 không ra 2 đơn. `findLimitRangeSlotBooking`: đoạn chỉ còn nghỉ trước tính thêm người có ca tại mốc bắt đầu phục vụ; chỉ áp cho 合計 + 合算をする + 指名なし. **Rủi ro mở oan**: khung đầu ca có thể mở dù người vào ca không phục vụ trọn khoảng (vd bận/Google block ngay đầu ca) — cần đối chứng âm. **Quan trọng cho release**: nếu `release_step_20260930` lên mà thiếu `a4c92a8626` thì lịch 個人 không đặt được lượt nào qua luồng không thanh toán.

### 5. Recover data

✔ Không cần recover data.

### 6. Verify (Dev)

- PHPUnit `--filter Salon`: 73/73 xanh (2 file test mới: 3/4 fail trên code cũ, pass sau vá).
- Harness độc lập (`verify/41448-children`): lịch 個人 hạn mức 2 → lượt 1,2 đặt được, lượt 3 khung TẮT (release: mọi lượt bị xoá); hạn mức 1 → 1 lượt; không giới hạn → đặt mãi được; 2 khách đồng thời lịch nhiều NV (#41743 gốc): vẫn chỉ 1 đơn.
- Ma trận 44 kịch bản của 9 ticket con: chỉ đúng 1 kịch bản đổi (#41742 合算をする 14:30 TẮT→BẬT), 0 hồi quy.
- Quét ngẫu nhiên 120 cấu hình 合算をする có nghỉ trước: 20 khung TẮT→BẬT, 0 BẬT→TẮT.

### Requirements mới trên Studio (REQ-008 / 009 / 010)

| Req | Tên | Risk |
|---|---|---|
| REQ-008 | 合算をする + 指名なし: khung bắt đầu đúng giờ vào ca không bị ẩn bởi thời gian chuẩn bị | High |
| REQ-009 | Nhánh KHÔNG nhận #41742 (合算をする + 指名, 合算しない + 指名なし) giữ đúng hành vi đầu ca | Medium |
| REQ-010 | Lịch 個人: lần kiểm lại sau khi tạo đơn giữ đúng số đơn theo suất còn lại | High |

### Branch / commit

- `sns-line`: `ai_fixbug_41448` (nhánh gốc `release_step_20260930`, commit `a4c92a8626`, 4 file) [đã push]

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
