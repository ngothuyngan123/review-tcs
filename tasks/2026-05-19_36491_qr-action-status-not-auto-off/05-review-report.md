# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36491 — [QR Landing] QRコードアクション — đã set 終了時期 nhưng status không tự OFF |
| Reviewer (Leader) | `<điền sau khi Leader verify>` |
| Tester được review | `<chưa xác định — bộ TC fetched từ Sheet master "Improve 1.0" rows 3546-3562, có thể do Hạnh Nguyễn (Dev) chuẩn bị template trước cho QA>` |
| Ngày review | 2026-05-19 |
| Version TCs | v1 (fetched từ Sheet) |
| Vòng review | Round 1 (Claude draft) |

> Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng, không có spec riêng cho task này (file `02-spec-reference.md` không tồn tại trong folder).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có 2 [MAJOR] về **auto-fill tester chưa verify** + nhiều [MAJOR] về **adversarial gaps** (auto-OFF cron job, symptom-only KH report, PR link trống, bulk-folder context KH report, edge `limit_end_time = now`). Coverage mechanical của 5 impact (BUG/F1/D1/T1/T2) **đều OK** — vấn đề nằm ở **chiều sâu adversarial** chứ không phải bỏ sót impact.

**Lý do ngắn gọn**: Bộ TCs từ Sheet "Improve 1.0" cover khá đầy đủ cho 2 option (`終了日時を設定しない` + `終了日時を設定する`) với 8 TCs lifecycle giá trị `time_qr_off_status` (0/1/3) — đây là điểm rất tốt. Tuy nhiên còn 8 vấn đề MAJOR cần Tester xử lý: (1) tick checkbox verify auto-fill file 01 + 03, (2) confirm với Dev về cron auto-OFF job (T2) thiếu trong 4.1, (3) kiểm tra alternative root cause cho symptom-only KH report, (4) bổ sung TC bulk folder + double-click + boundary `limit_end_time = now` + staff permission + compatibility.

---

## 2. Tóm tắt cho member

Coverage matrix của bộ TCs tốt — verify đầy đủ giá trị `time_qr_off_status` (0/1/3) qua 8 TCs lifecycle ở option `終了日時を設定する` và 7 TCs regression ở option `終了日時を設定しない`. Tuy nhiên có vài điểm cần hoàn thiện trước khi merge: (a) tester tick 2 checkbox "Tester verify auto-fill chính xác" trong file 01 + 03 (hiện đang trống — auto-fill từ `/new-task` chưa được tester confirm); (b) bổ sung TC verify **cron job auto-OFF** đọc `time_qr_off_status` (T2 cần function này nhưng mục 4.1 không list); (c) cover thêm bulk context — KH report ảnh hưởng toàn folder 「菌活1日目」, hiện TCs chỉ verify 1 QR đơn lẻ; (d) thêm boundary `limit_end_time = now` đối xứng với 3551/3552 đã cover `limit_start_time = now`.

---

## 3. Coverage Matrix

> Sheet "Improve 1.0" rows 3546-3562 dùng schema outline (B–H cell trống = kế thừa row trên), không có cột "TC ID / Type / Priority" theo schema chuẩn 10-cột. Map ID theo row number để dễ trace.

| Impact | Loại | Priority Dev đánh giá | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause — toggle OFF/ON sau start_time, đến end_time vẫn không tự OFF) | Fix | — | **R3558** (Check đang ON ⇒ OFF ⇒ ON: `End_time < now ⇒ OFF; Time_qr_off_status = 0`), R3559 (QR=ON, lifecycle 3-bước verify `Time_qr_off_status = 1/3/0`), R3561 (bật ON lại trong tgian start–end, tới end_time ⇒ OFF) | 3 | **OK** — bug fix flow được verify trực tiếp |
| F1 — `QRCodeController@ajaxUpdateBasicQrs` | Function | Direct | R3548–R3562 (toàn bộ 15 TCs đều trigger qua route `PUT /update-basic/{qr}`) | 15 | **OK** |
| F-implicit — Job/Cron auto-OFF QR khi đến `limit_end_time` (**Dev KHÔNG list trong 4.1**) | Function | (suy luận High vì T2 cần) | R3550 (`tới giờ ⇒ bật OFF` → expected "Hiển thị QR = OFF luôn"), R3557 (verify `time_qr_off_status = 0`), R3559 step 3 (tới end_time), R3560, R3561 step 2 | 5 | **RISK** — TC verify *symptom* "tới giờ ⇒ QR = OFF" nhưng KHÔNG có TC chỉ rõ **cron job nào** đọc field này; Dev không list function này trong 4.1 |
| D1 — `landing_qrs.time_qr_off_status` (Dev ghi "k có" — nhưng field này thay đổi GIÁ TRỊ runtime sau fix, schema không đổi) | Data | — | R3555 (note 3 giá trị 0/1/3), R3557 (=0 khi user toggle OFF), R3558 (=3 khi ON in active range, =0 khi end_time qua), R3559 (=1 chưa tới start, =3 in range, =0 hết), R3560 (=0), R3561 (=3 → =0), R3562 (=0) | 7 | **OK** — verify đầy đủ 3 giá trị `time_qr_off_status` qua các state transition |
| D2 — `landing_qrs.limit_start_time` + `landing_qrs.limit_end_time` (Dev "k có") | Data | — | R3548, R3549, R3551, R3552 (`limit_start_time` set khi 終了日時を設定しない), R3555–R3562 (cả 2 fields khi 終了日時を設定する) | 12 | **OK** |
| T1 — Toggle ON/OFF QR Landing ở list page khi QR có cấu hình `use_limit_time` | Feature | High | R3555–R3562 (8 TCs với option 終了日時を設定する verify đủ state: QR=OFF chưa/tới giờ ON, QR=ON chưa/tới giờ OFF, ON⇒OFF, ON⇒OFF⇒ON, bật ON lại trong start-end, OFF⇒ON⇒OFF) | 8 | **OK** |
| T2 — Auto-OFF QR theo `limit_end_time` (sẽ hoạt động đúng sau fix) | Feature | High | R3558 (`End_time < now ⇒ OFF`), R3559 step 3 (`Tới end_time ⇒ QR = OFF`), R3561 step 2 (`Tới end_time ⇒ QR = OFF`) | 3 | **RISK** — chỉ verify hành vi end-to-end (tới giờ thì QR OFF), KHÔNG verify cụ thể cron job + retry + timezone JST/UTC + xử lý nhiều QR cùng tới end_time |

### Regression — Option `終了日時を設定しない` (case KHÔNG set end_time)

| Row | Verify | Status |
|---|---|---|
| R3548 | QR = OFF, chưa tới giờ user bật ON ⇒ tới giờ vẫn ON (không tự OFF) | OK |
| R3549 | QR = ON, chưa tới giờ user bật OFF ⇒ tới giờ vẫn ON | OK |
| R3550 | Tới giờ rồi user bật OFF ⇒ OFF luôn | OK |
| R3551 | Set time = today, time > now ⇒ QR = ON, `limit_start_time` set vào DB | OK |
| R3552 | Set time = today, **time = now** (boundary `limit_start_time = now`) ⇒ QR = ON | OK |
| R3553 | Trước date đã setting: list = ON ⇒ ON; list = OFF ⇒ OFF | OK |
| R3554 | Sau date đã setting: cả 2 case đều ON (continue ON-state) | OK |

> Regression sau fix giữ behavior cũ cho case **không có `limit_end_time`** — fix chỉ thêm branch khi `use_limit_time = true && limit_end_time != null`, không động vào branch `終了日時を設定しない`.

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| _(không có)_ | — | Tất cả 15 TCs đều map về F1 (vì cùng đi qua route `PUT /update-basic/{qr}`) và 1 trong { T1, T2 } | Giữ nguyên |

---

## 3.5 Fix-shape analysis (adversarial)

> Chi tiết: [../../framework/review-checklist.md](../../framework/review-checklist.md) §A.6 + [../../framework/anti-patterns.md](../../framework/anti-patterns.md).

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Specific code check** — fix thêm nhánh `if (limit_end_time <= now) → time_qr_off_status = 0 else → 1`, KHÔNG phải generic catch-all. (Branch logic 2-way) |
| Trigger space cần cover | (1) `use_limit_time = false` (regression); (2) `use_limit_time = true && limit_start_time > now` (chưa tới start); (3) `use_limit_time = true && limit_start_time <= now && limit_end_time = null` (option `終了日時を設定しない`); (4) `use_limit_time = true && limit_start_time <= now && limit_end_time > now` (đang active → `time_qr_off_status = 1`); (5) `use_limit_time = true && limit_start_time <= now && limit_end_time <= now` (hết hạn → `time_qr_off_status = 0`); (6) `limit_end_time = now` exact (boundary) |
| Số trigger TCs hiện cover | **5/6** — case (1) cover bởi R3548–R3554, case (2) cover bởi R3559 step 1, case (3) cover bởi R3555 "ON state continues", case (4) cover bởi R3557/R3558/R3559 step 2, case (5) cover bởi R3558/R3559 step 3/R3561 step 2. **MISS case (6) `limit_end_time = now`** — đối xứng với 3551/3552 đã cover `limit_start_time = now` nhưng KHÔNG có TC cho `limit_end_time = now`. |
| KH report dạng | **Symptom-only** — KH chỉ ghi "đã set 終了時期 nhưng status không tự OFF" + ảnh hưởng "tất cả items trong folder 「菌活1日目」". KHÔNG có error log / error code / DB state cụ thể. Dev (Hạnh Nguyễn) tái hiện qua 1 root cause specific (toggle OFF/ON sau start_time → reset flag) — nhưng KH có thể gặp root cause khác cùng symptom. |
| Alternative root causes cần verify | (a) **Cron auto-OFF job timezone**: job chạy theo UTC nhưng `limit_end_time` lưu JST → off muộn 9h; (b) **Cron job retry / dead-letter**: job fail âm thầm, KHÔNG có TC verify retry; (c) **Bulk folder case**: KH report cả folder 「菌活1日目」 bị — có thể cron limit số QR xử lý/lần, dồn nhiều QR end_time gần nhau gây timeout/skip; (d) **Legacy data**: QR cũ tạo trước khi có `use_limit_time` column (default null), `time_qr_off_status` đã có sẵn = 0 → check migration; (e) **`saveSettingQrOff` impact**: nếu user thay đổi setting time SAU khi đã đến start_time → liệu logic mới có conflict với `saveSettingQrOff` (mục 3 nói "logic này không đổi" — cần verify) |
| Anti-patterns dính | **AP-2** (Symptom-only KH report — flag MAJOR), **AP-4** (PR/Commit link trống — flag MAJOR). Không dính AP-1 (fix specific chứ không generic), không dính AP-6 (mục 3 đã list 2 callers). Có risk nhẹ AP-3 với T2 (chỉ 3 TC verify auto-OFF — đều happy-path "tới giờ ⇒ OFF", thiếu edge state) |

> Fix shape là specific branch logic 2-way → trigger space cover 5/6 đã khá tốt. Vấn đề chính là alternative root causes (cron timezone / retry / bulk) chưa được verify — chuyển sang §4.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

_(Không có BLOCKER thực sự — coverage mechanical đủ cho mọi impact Dev đã list. Tất cả vấn đề downgrade về MAJOR vì có TC verify symptom end-to-end ngay cả khi function ẩn (cron auto-OFF) không được list rõ.)_

### 4.2 Major (nên fix)

**Liên quan auto-fill tester chưa verify** (luôn flag khi `/new-task` chạy mà tester chưa tick checkbox):
- **[MAJOR] FILE-01 AUTO-FILL CHƯA VERIFY**: `01-bug-task.md` ghi `Auto-filled: 2026-05-19 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick — yêu cầu tester đọc lại description + journal #118642 Redmine #36491 và xác nhận đầy đủ (steps reproduce + attachments + custom field), rồi tick checkbox trước khi review có giá trị.
- **[MAJOR] FILE-03 AUTO-FILL CHƯA VERIFY**: `03-dev-impact.md` ghi `Auto-filled: 2026-05-19 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick — F/D/T có thể chưa đầy đủ hoặc mapping sai (xem các MAJOR FIX-SHAPE bên dưới đã list các điểm nghi vấn cụ thể).

**Liên quan fix-shape adversarial (Bước 3c)**:
- **[MAJOR] FIX-SHAPE: GAP-1 — Cron job auto-OFF không có trong mục 4.1**: Mục 4.3 list T2 = "Tính năng auto-OFF QR theo `limit_end_time` (sẽ hoạt động đúng sau fix)" nhưng mục 4.1 chỉ có F1 = `ajaxUpdateBasicQrs`. Function nào ĐỌC `time_qr_off_status` để OFF QR khi `limit_end_time` đến (cron / scheduled command / queue worker)? Yêu cầu Dev list function này vào 4.1 (vd: `Console\Commands\AutoOffQrCommand` hoặc `Jobs\QrAutoOffJob`) — Bộ TCs hiện chỉ verify *symptom* "tới end_time → QR = OFF" mà không verify cụ thể cron đọc đúng field, có timezone đúng, có retry khi fail.
- **[MAJOR] SYMPTOM-ONLY**: KH report symptom-only ("set 終了時期 nhưng status không OFF" + ảnh hưởng cả folder 「菌活1日目」), Dev tái hiện 1 root cause (toggle OFF/ON sau start_time). Cần Tester hỏi lại Dev xem có alternative root cause nào không — đặc biệt: (a) **cron job timezone bug**, (b) **cron job batch limit / retry**, (c) **legacy QR trước khi có cột `use_limit_time`**, (d) **bulk folder case** — KH dùng từ "tất cả items trong folder", có thể cron skip một số QR khi xử lý batch lớn.
- **[MAJOR] AP-4 PR/COMMIT LINK TRỐNG**: `03-dev-impact.md` mục "Commit / Pull Request" để `<chưa có>` → reviewer không thể verify fix thực tế trong code (`QRCodeController.php:1015-1023`) là specific branch 2-way hay disguised generic. Yêu cầu Dev cung cấp PR link.

**Liên quan input dev-impact**:
- **[MAJOR] FILE-03 MỤC 4.1 THIẾU FUNCTION CRON AUTO-OFF**: như đã nói ở GAP-1 trên — cron/job auto-OFF cần list vào 4.1. Sau khi Dev confirm function, có thể cần thêm TC verify function này cụ thể.
- **[MAJOR] FILE-03 MỤC 4.2 GHI "K CÓ" GÂY HIỂU NHẦM**: Dev ghi "k có" nhưng field `landing_qrs.time_qr_off_status` thay đổi **giá trị runtime** (0 vs 1 tùy `limit_end_time`) sau fix. TCs đã verify field này (R3555–R3562). Đề nghị Dev sửa mục 4.2: thêm `D1 = landing_qrs.time_qr_off_status` với thao tác `UPDATE` ghi chú "schema không đổi, giá trị set khác sau fix theo `limit_end_time` state".

**Liên quan boundary / coverage gap**:
- **[MAJOR] GAP-2 — Edge case `limit_end_time = now` exactly**: TCs cover `limit_start_time = now` (R3551 `time > now`, R3552 `time = now`) nhưng **không có TC đối xứng** cho `limit_end_time = now`. Fix logic `if (limit_end_time <= now) → time_qr_off_status = 0` — case `=` thuộc nhánh "đã hết hạn", cần TC verify chính xác giây/phút boundary.
- **[MAJOR] GAP-3 — Bulk folder context KH report**: KH report `đối tượng: tất cả items trong folder 「菌活1日目」` (multiple QR cùng folder bị). TCs hiện chỉ verify 1 QR đơn lẻ — không có TC test toàn folder nhiều QR cùng setting end_time đến cùng lúc (verify cron job xử lý batch không skip).
- **[MAJOR] GAP-4 — Row 3556 expected trống**: Action "Tới giờ => ON" (QR=OFF state, option `終了日時を設定する`) nhưng cột Expected H trống → không rõ TC này verify gì. Đề nghị member fill expected (predict: QR auto-ON ở `limit_start_time`, `Time_qr_off_status = 3`).

### 4.3 Minor (có thể fix sau)

- **[MINOR] SCHEMA OUTLINE thiếu TC ID / Type / Priority**: Sheet master "Improve 1.0" dùng outline schema, không có TC ID rõ ràng (chỉ dùng row number 3548-3562) → khó tracking pass/fail từng TC. Khi `/sync-tc` push lên Sheet master master, cột Status có dropdown nhưng các cột Type / Priority / TC ID trống — đề nghị member bổ sung khi sync.
- **[MINOR] CL1 STAFF ACCOUNT**: Chưa có TC test với account staff (không quyền QR Landing) — `framework/checklist-lme.md` §A.1 CL1 bắt buộc.
- **[MINOR] CL5 DOUBLE CLICK**: Chưa có TC test double click button toggle status nhanh — checklist LME CL5.
- **[MINOR] CL3 CHUYỂN TAB**: Nếu màn QR detail có nhiều tab setting (basic/schedule/action) → chưa cover case chuyển tab khi đang set schedule.
- **[MINOR] COMPATIBILITY (LME A.2 Non-function)**: Chưa có TC mention Win + Mac (Chrome + Safari) cho list page toggle.
- **[MINOR] SECURITY URL MỚI**: Nếu `/update-basic/{qr}` là route đã có sẵn không thay đổi → không bắt buộc security test mới. Nhưng có thể cover regression: staff không quyền QR / param `{qr_id}` của bot khác → expected 403.

### 4.4 Nit (gợi ý)

- **[NIT] TC ID FORMAT**: Đề xuất convention `TC-36491-XX` thay vì row number Sheet — dễ trace trong report.
- **[NIT] TIMEZONE**: Đề xuất ghi rõ TC chạy với timezone Asia/Tokyo (JST) — vì `limit_start_time` / `limit_end_time` lưu kiểu gì (UTC hay local) ảnh hưởng cron job đọc.
- **[NIT] R3556 + R3559 step 2**: Cả 2 đều có expected mơ hồ về timing — đề nghị tách atomic.
- **[NIT] R3553 vs R3554**: Hơi confusing với 2 case "list = ON / list = OFF" trong cùng 1 cell expected — đề nghị tách thành 2 TC riêng.

---

## 5. TCs đề xuất bổ sung

> **Perspective**: Manual tester thao tác trên UI. Steps mô tả thao tác user nhìn thấy / click / nhập trên màn hình (UI element JP gốc, có chú thích VN). Expected chủ yếu verify hiển thị + behavior trên UI. **DB check chỉ là verify bổ sung** ở cuối Expected, không phải driver chính.
>
> Tham chiếu màn hình (theo screenshot tester gửi):
> - **Màn list QR**: `QRコードアクション（流入経路分析）` — cột `稼働状況` có toggle ON/OFF từng dòng (đây là entry point thao tác bug fix — gọi `ajaxUpdateBasicQrs`)
> - **Màn detail QR > Tab `基本設定` > Sidebar `稼働ON・OFFの設定`**: section `スケジュール設定` có switch `利用しない / 利用する`, field `開始日時` (date + time picker), radio `終了日時を設定しない(ONの状態を継続する)` / `終了日時を設定する`, field `終了日時` (date + time picker khi chọn 設定する). Bấm `保存` (đây là entry point gọi `saveSettingQrOff`).
>
> Member copy vào `04-tc-list.md` ở round tiếp theo (sau khi confirm với Dev về cron auto-OFF + alternative root cause).

| TC ID gợi ý | Title | Precondition | Steps (UI) | Expected (UI + DB phụ trợ) | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-36491-NEW-01 | Replay bug KH — toggle thủ công OFF/ON sau khi đã đến 開始日時, đến 終了日時 phải auto-OFF | Account standard, đã có ít nhất 1 folder QR. Có thể thao tác qua admin web Chrome (staging). | 1. Mở màn list `QRコードアクション` → bấm `+新規作成` (hoặc chọn 1 QR có sẵn) → vào màn detail<br>2. Vào tab `基本設定` → sidebar `稼働ON・OFFの設定`<br>3. Tại section `スケジュール設定`: bấm switch `利用する`<br>4. Set `開始日時` = `<today>` + `<now + 2 min>`<br>5. Chọn radio `終了日時を設定する`<br>6. Set `終了日時` = `<today>` + `<now + 5 min>`<br>7. Bấm `保存` → quay lại màn list<br>8. Tại column `稼働状況` của QR vừa tạo: chờ đến `開始日時` (sau 2 min) → quan sát toggle<br>9. Khi toggle đã ON, **click thủ công** toggle xuống OFF<br>10. Click lại toggle để bật lên ON<br>11. Chờ đến `終了日時` (sau 5 min từ lúc setting) → quan sát toggle column `稼働状況` | - Sau bước 8: toggle hiển thị **ON** (xanh) tại `稼働状況` — schedule auto-ON đã chạy<br>- Sau bước 11: toggle hiển thị **OFF** (xám) tại `稼働状況` — schedule auto-OFF chạy đúng dù user đã toggle thủ công ở giữa (đây là điểm fix)<br>- (DB phụ trợ) `landing_qrs.time_qr_off_status = 0` sau bước 11 | High | Positive (bug fix verify) | BUG, F1, T1, T2 |
| TC-36491-NEW-02 | Boundary — set 終了日時 đúng = phút hiện tại, toggle thủ công OFF→ON xem có auto-OFF không (đối xứng R3552 cho 開始日時) | QR có `スケジュール設定 = 利用する`, `開始日時` = past 1h (đã qua). | 1. Mở màn detail QR (đã có `開始日時` qua, QR đang ON ở list page)<br>2. Vào `稼働ON・OFFの設定` → chọn radio `終了日時を設定する`<br>3. Set `終了日時` = `<today>` + `<phút hiện tại>` (đúng phút now, chấp nhận sai số ±30s)<br>4. Bấm `保存` ngay lập tức<br>5. Quay lại list page, **click toggle** tại column `稼働状況` để OFF → ON lại nhanh trong vòng 30s<br>6. Reload màn list | - Sau bước 6: toggle ở column `稼働状況` hiển thị **OFF** (đã hết hạn — `終了日時 <= now`)<br>- Nếu user cố click ON lại → sau vài giây / lần reload kế tiếp, toggle quay về OFF (vì cron auto-OFF nhận diện đã quá hạn)<br>- (DB phụ trợ) `time_qr_off_status = 0` | High | Boundary | F1, T2 |
| TC-36491-NEW-03 | Bulk folder — folder chứa nhiều QR cùng `終了日時`, replay flow KH cho từng QR rồi verify cả folder auto-OFF | Tạo folder mới "Test bulk 36491" (hoặc dùng folder hiện có ≥ 5 QR). Mỗi QR đã setting `スケジュール設定 = 利用する`, cùng `開始日時 = past 30 min`, cùng `終了日時 = now + 5 min`. | 1. Mở màn list, chọn sidebar folder "Test bulk 36491" → xác nhận hiển thị ≥ 5 QR<br>2. Tại column `稼働状況`, **lần lượt click toggle** OFF → ON cho từng QR (replay flow KH — KH report "tất cả items trong folder")<br>3. Chờ đến `終了日時` (5 min sau setting)<br>4. Reload màn list → quan sát column `稼働状況` của TẤT CẢ QR trong folder | Sau bước 4: **TẤT CẢ** QR trong folder hiển thị toggle **OFF** ở `稼働状況`, không có QR nào còn ON / skip.<br>(DB phụ trợ) `time_qr_off_status = 0` cho cả ≥ 5 QR | High | Regression (bulk — KH context) | T2, ↦ Symptom KH "tất cả items trong folder" |
| TC-36491-NEW-04 | Staff không quyền QR Landing không thao tác được toggle ở column 稼働状況 | Tạo staff account, không cấp quyền `QRコードアクション（流入経路分析）`. | 1. Logout admin chính → login staff không quyền<br>2. Mở menu → thử click vào `QRコードアクション` | Sau bước 2: hoặc menu KHÔNG hiển thị item `QRコードアクション`, hoặc click vào → màn báo `アクセス権限がありません` (hoặc redirect về dashboard). Không vào được màn list, không click được toggle. | Medium | Negative (permission) | Checklist LME §A.1 CL1 |
| TC-36491-NEW-05 | Double click toggle column 稼働状況 không gây loop / duplicate state | QR có `スケジュール設定 = 利用する`, `開始日時 = past`, `終了日時 = future` (đang trong khoảng active). Toggle hiện ON. | 1. Mở màn list QR<br>2. Tại column `稼働状況` của QR: **double click** thật nhanh (< 200ms) lên toggle<br>3. Quan sát trạng thái toggle hiển thị | Sau bước 2-3: toggle hiển thị 1 trạng thái duy nhất (ON hoặc OFF, không nhấp nháy / không loop). Reload màn list → trạng thái nhất quán. (Không có 2 entry log trùng trong DB hoặc network tab show chỉ 1 request thành công 200, request còn lại bị block/reject) | Medium | Boundary | Checklist LME §A.1 CL5 |
| TC-36491-NEW-06 | Multi-tab race — 2 tab cùng QR, mỗi tab toggle ngược hướng | QR có `スケジュール設定 = 利用する`, đang trong khoảng start-end active. Toggle hiện ON. | 1. Mở 2 tab Chrome, cùng URL màn list QR<br>2. Tab 1: click toggle để OFF tại column `稼働状況`<br>3. **Cùng lúc đó** (trong vòng 1s), Tab 2: click toggle để ON cùng QR đó<br>4. Reload cả 2 tab | Sau bước 4: cả 2 tab hiển thị **cùng 1 trạng thái** toggle (không tab nào hiển thị state khác). Không có inconsistent: tab A = ON, tab B = OFF. | Medium | Boundary | Checklist LME §A.1 CL3 (multi-tab) |
| TC-36491-NEW-07 | Regression saveSettingQrOff — user đổi 終了日時 qua màn detail KHÔNG ảnh hưởng auto-OFF | QR đang ở trạng thái: `スケジュール設定 = 利用する`, `開始日時 = past`, `終了日時 = now + 10 min`. Toggle ON ở list page. Đã click toggle OFF → ON (đang ở trạng thái "user toggle in active range"). | 1. Vào màn detail QR đó → `稼働ON・OFFの設定`<br>2. Tại section `スケジュール設定`: đổi `終了日時` thành `now + 30 min` (kéo dài thêm)<br>3. Bấm `保存`<br>4. Quay lại list page → quan sát toggle column `稼働状況`<br>5. Chờ đến `終了日時 mới (now + 30 min)` → quan sát toggle | Sau bước 4: toggle vẫn **ON** (chưa đến `終了日時` mới).<br>Sau bước 5: toggle chuyển **OFF** đúng tại `終了日時` mới (saveSettingQrOff không bị hỏng bởi fix `ajaxUpdateBasicQrs`).<br>(DB phụ trợ) `time_qr_off_status = 1` ngay sau save (logic cũ saveSettingQrOff), sau khi đến end_time mới → `= 0` | Medium | Regression | Mục 3 dev-impact (caller `saveSettingQrOff`) |
| TC-36491-NEW-08 | Timezone — set 終了日時 cuối ngày JST, verify auto-OFF tại thời điểm JST | Bot setting timezone Asia/Tokyo (JST). Account standard staging. | 1. Vào màn detail 1 QR → `稼働ON・OFFの設定`<br>2. Set `スケジュール設定 = 利用する`, `開始日時` = hôm nay 23:50 JST<br>3. Chọn `終了日時を設定する`, set `終了日時` = hôm nay 23:55 JST<br>4. Bấm `保存`<br>5. Tại list page chờ đến 23:50 JST → quan sát toggle column `稼働状況`<br>6. Khi toggle ON, click thủ công OFF → ON lại<br>7. Chờ đến 23:55 JST → quan sát toggle | Bước 5: toggle = ON tại đúng 23:50 JST (không phải UTC equivalent 14:50 JST).<br>Bước 7: toggle = OFF tại đúng 23:55 JST.<br>(DB phụ trợ) `limit_start_time` và `limit_end_time` lưu đúng định dạng theo convention LME (verify Dev confirm UTC hay JST trong DB) | High | Boundary (alt root cause timezone) | T2, ↦ Alt root cause (a) |
| TC-36491-NEW-09 | Compatibility — toggle column 稼働状況 trên Win + Mac, Chrome + Safari | Cùng 1 QR test, có `スケジュール設定 = 利用する`, `開始日時 = past`, `終了日時 = future`. | 1. **Win + Chrome**: mở màn list QR → click toggle ở column `稼働状況` từ ON → OFF → ON → quan sát hiển thị mỗi lần<br>2. **Mac + Safari**: login cùng account, mở list QR cùng folder → lặp lại bước 1 | Cả 2 OS/browser: animation toggle mượt, không lag; hiển thị state đúng giống nhau. Click 1 lần = 1 toggle (không double-fire trên Safari). | Low | Regression | Checklist LME §A.2 Compatibility |
| TC-36491-NEW-10 | QR không bật スケジュール設定 (利用しない) — toggle hoạt động bình thường, không bị fix mới ảnh hưởng | QR có `スケジュール設定 = 利用しない` (switch OFF). Không có `開始日時` / `終了日時` set. | 1. Mở màn list QR<br>2. Tại column `稼働状況` của QR: click toggle nhiều lần (OFF → ON → OFF → ON)<br>3. Mở màn detail QR → `稼働ON・OFFの設定`: confirm switch `スケジュール設定 = 利用しない`<br>4. Chờ 5-10 min để xác nhận không có behavior tự động | Bước 2: mỗi lần click toggle UI cập nhật state ngay tức thì, không có lag.<br>Bước 4: toggle giữ nguyên trạng thái user vừa set, KHÔNG bị auto-OFF (vì schedule = 利用しない). Behavior giống y hệt trước fix.<br>(DB phụ trợ) `time_qr_off_status = 0` luôn (không trigger nhánh fix mới vì `use_limit_time = false`) | Medium | Regression (legacy/disable schedule) | Mục 4.3 implicit, ↦ Alt root cause (d) legacy |
| TC-36491-NEW-11 | Verify radio `終了日時を設定しない(ONの状態を継続する)` — toggle thủ công OFF/ON, không tự auto-OFF dù qua nhiều giờ | QR có `スケジュール設定 = 利用する`, set `開始日時 = now - 30 min` (đã qua), radio chọn `終了日時を設定しない(ONの状態を継続する)`. Đã `保存`. | 1. Mở màn list, verify QR toggle ON (vì đã qua `開始日時`)<br>2. Click toggle để OFF → ON lại tại column `稼働状況`<br>3. Chờ 30 min – 1h → quan sát toggle | Sau bước 3: toggle **vẫn = ON** suốt thời gian (không có `終了日時` thì không bao giờ auto-OFF). Đây là verify regression branch "ON state continues" sau fix vẫn hoạt động đúng. | Medium | Regression | T1 (option `終了日時を設定しない` không bị regress) |
| TC-36491-NEW-12 | Reload màn list ngay khi cron auto-OFF chạy — toggle hiển thị đồng bộ | QR `スケジュール設定 = 利用する`, `開始日時 = past`, `終了日時 = now + 2 min`, toggle đang ON, đã có thao tác toggle thủ công OFF/ON (replay bug flow). | 1. Tại màn list, mở QR ở chế độ hiển thị toggle column `稼働状況`<br>2. Chờ đến `終了日時 ± 30s`<br>3. **Reload màn list NGAY** (F5) lúc cron có thể đang chạy<br>4. Quan sát toggle | Bước 4: trong vòng 1-2 reload (mỗi reload cách ~30s), toggle chuyển từ ON → OFF. Không có trạng thái UI khác (vd: loading mãi, hiển thị "ON" cứng dù DB đã update). | Medium | Boundary (UI sync) | Checklist LME §A.1 CL2 (reload sau update) |

---

## 6. Spec update needed

- [x] **Không cần update spec** — fix khôi phục đúng spec ban đầu (`limit_end_time` đến hạn thì QR phải OFF). Trước fix là bug, không phải spec change.
- [ ] Cần update spec

**Note**: Nếu Dev muốn formalize behavior `time_qr_off_status` 3 giá trị (0 / 1 / 3) — đề nghị tạo spec riêng cho `spec-features/admin/qr-landing/` (sub-repo) để future-proof. Hiện R3555 đã ghi note trong cell expected — không tệ nhưng nên có spec chính thức.

---

## 7. Checklist đã chạy

- [x] A. Coverage — pass với note RISK ở T2 (cron auto-OFF function)
- [x] B. Chất lượng từng TC — pass với MINOR (schema outline thiếu TC ID / Type / Priority)
- [x] C. Chất lượng bộ TC tổng thể — pass; tỷ lệ Positive : Negative : Boundary : Regression khó tính chính xác vì schema outline không gán Type, nhưng quan sát: chủ yếu Positive + Boundary (lifecycle state), thiếu Negative + ít Regression edge state
- [x] D. Spec alignment — pass; không có file 02-spec-reference.md riêng, dùng LME-SYSTEM-SPEC tổng làm fallback
- [x] E. Hành chính — sheet đã có nguồn rõ ràng (`Source: fetched từ Redmine #36491 Link TCs ... lúc 2026-05-19`)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — CL1 (staff), CL3 (multi-tab), CL5 (double click) chưa cover → đề xuất NEW-04, NEW-05, NEW-06; Compatibility chưa cover → NEW-09
  - [x] F.2 Checklist job — Task chạm cron auto-OFF, nhưng KHÔNG dính B.2 Job sync Java (Google sync). B.1 Job callback không applicable.
  - [x] F.3 Các tính năng chung — C.1–C.8 không có item nào dính trực tiếp với task này. C.7 Plan limits: QR Landing có plan limit không? — nếu có cần check số QR active concurrent theo plan.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<điền sau khi Leader verify>` | |
| Tester | (đã đọc & hiểu feedback) | |

---

## Phụ lục — Reverse matrix (TC → Impact)

| Row | Cover impact nào | Status |
|---|---|---|
| R3548 | F1 + T1 (regression option `終了日時を設定しない`) | OK |
| R3549 | F1 + T1 (regression) | OK |
| R3550 | F1 + T1 + verify auto-OFF behavior (cron implicit) | OK |
| R3551 | F1 + T1 + boundary `limit_start_time` | OK |
| R3552 | F1 + T1 + boundary `limit_start_time = now` | OK |
| R3553 | F1 + T1 (regression trước date) | OK |
| R3554 | F1 + T1 (regression sau date) | OK |
| R3555 | F1 + T1 + D1 (note 3 giá trị `time_qr_off_status`) | OK — TC documentation tốt |
| R3556 | F1 + T1 — **expected trống → flag MAJOR GAP-4** | RISK |
| R3557 | F1 + T1 + D1 (`time_qr_off_status = 0`) | OK |
| R3558 | **BUG** + F1 + T1 + T2 + D1 (lifecycle 3 → 0) — TC verify trực tiếp bug flow KH | OK |
| R3559 | **BUG** + F1 + T1 + T2 + D1 (lifecycle 1 → 3 → 0) | OK — TC strong |
| R3560 | F1 + T1 + D1 (`time_qr_off_status = 0`) | OK |
| R3561 | **BUG** + F1 + T1 + T2 + D1 (lifecycle 3 → 0) | OK |
| R3562 | F1 + T1 + D1 (toggle cycle OFF → ON → OFF) | OK |
