# 05 — Review Report (draft cho Leader verify)

## Thông tin

| Trường | Giá trị |
|---|---|
| Task | `tasks/2026-08-26_40128_salon-dat-lich-ngoai-khung-gio-ca/` |
| Ticket | Redmine #40128 — `[24-08-2026][29927][Salon] Khách báo hệ thống cho phép gửi yêu cầu đặt lịch ngoài khung giờ ca làm việc dù chỉ thiết lập ca đến 20h30.` |
| Feature | FA-020 Salon Booking (`calendar-salon` / サロン・面談予約) |
| Branch fix | `ai_fixbug_40128` (gốc `release_step_20260805`), commit `3d50f0a332`, 4 file |
| Reviewer | `/review-tc` (draft) — Leader verify trước khi trả member |
| Ngày review | 2026-08-26 |
| Vòng review | round 1 (Studio `reviewState = leader`, `reviewed = false`, `review_list_comments` = rỗng → chưa có vòng review nào trước) |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#213` |
| Cách lấy | `task_list(ticket_id=40128)` → `testcase_list(task_id=213, limit=100)` → `task_get_context(sections=[requirements, test_viewpoint_selection, review])` → `task_get_report(213)` → `review_list_comments(213)` |
| Thời điểm fetch | 2026-08-26 (re-verify `task_list` ngay trước khi review — state không đổi) |
| **Tổng TC lấy về** | **25** |
| Nguồn 2 (Sheet human) | **KHÔNG dùng** — nguồn 1 đã có TC nên dừng theo thứ tự ưu tiên |
| Nguồn 3 (file 04) | **KHÔNG dùng làm nguồn** — nguồn 1 đã có TC |
| Đối chiếu chéo | **KHÔNG** — đã dừng ở nguồn đầu tiên có TC theo đúng quy tắc |

**Về file snapshot:** không tạo thêm `04-tc-list.studio.md`. Lý do: `04-tc-list.md` trong folder **chính là snapshot Studio** — được `/new-task` sinh trong cùng session này từ **cùng `task_id=213`, cùng lần fetch** (header file mang `<!-- source: MCP LME TEST STUDIO — task_id=213, ticket 40128, testcase_list (25 TC) -->`), không phải TC do member repo viết. Tạo file `.studio.md` thứ hai chỉ nhân đôi cùng một bảng. `task_list` đã được gọi lại trước khi review và **state không đổi** (25 TC · 14 pass · 0 fail · 1 other · 10 untested · round 1).

**Task Studio khác cùng ticket:** không có. `task_list(ticket_id=40128, include_archived=true)` → `totalMatched = 1`.

### 0.6 — Cảnh báo chất lượng nguồn

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass` **14/25 = 56%** · `skip` 1 · chưa chạy 10. Chỉ 14 TC có kết luận test. | **[MAJOR]** (`pass` < 80%) |
| 2 | **TC fail / error / gắn ticket bug** | `fail` 0 · `error` 0 · `bugs.total = 0` · không TC nào gắn `bug_tickets`. Không có TC fail chưa raise ticket. | OK |
| 3 | **Môi trường đã chạy** | **1 run duy nhất `#527`, `env = local`**. `envAuto`: dev 0 run · staging 0 run · prd 0 run. Task chạm **2 job nền** (`CalendarSalonStaffAssignment`, `CalendarSalonStaffAssignmentAdmin`). | **[MAJOR] RULE-08 / ENV-003** |
| 4 | **Ai chạy** | 100% `last_exec.source = ai`, `by = pipeline`. **0 TC do QA người chạy.** `submittedWithoutMcp = false`. Nhóm rủi ro cao (job nền, submit LIFF, 予約管理) đều chỉ do AI tự chạy. | **[MAJOR]** |
| 5 | **Tác giả TC** | **15/25 = 60% do AI sinh** (`provenance.source = ai`, `created_job_id = 658`); 10/25 do người thật viết (`cucdtk`, `provenance.source = human` — `toolWritten.mcp` chỉ là **kênh ghi**). Toàn bộ `status = draft`, `reviewState = leader`, `reviewed = false`. | **[MAJOR]** (≥50% AI sinh + `reviewState` chưa `done`) |
| 6 | **Mã quan điểm ngoài `checklist-lme.md`** | **6/25 TC (24%)** dùng mã không có ở tầng 1: `TOOL-KNOW-002` (1) · `TOOL-VAL2-001` (1) · `TOOL-OLDREC-001` (1) · `JOB-002` (3 — checklist chỉ có `JOB-001`). **Không tính là cover** ở BƯỚC 2/3b. Đáng chú ý: **TC tái hiện bug gốc nằm trong nhóm này**. | **[MAJOR]** |
| + | **Evidence** | `artifacts: []` ở **cả 15 kết quả run**; cột `Evidence thực tế` rỗng ở **25/25 TC**. 14 TC "Đạt" **không có bằng chứng đính kèm**, chỉ có text `actual` do runner tự thuật. | **[MAJOR] RULE-02** |
| + | **Trạng thái đánh giá spec** | `spec_status = null` ở **25/25 TC**. Không TC nào khai `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. | **[MAJOR]** |

---

## 1. Verdict

### 🔴 REJECTED

Có **5 `[BLOCKER]`**. Bộ TC bám khá sát diff code (đủ 5 điểm gọi Dev liệt kê, có đối chứng dương/âm, có case biên `breakTimeAfterApplied = 0`), nhưng **cấu hình đúng của bug khách hàng lại chưa được chạy lần nào**, và 2 TC regression "bất biến" đang **báo Đạt dù bước xác minh cốt lõi của chính TC đó không được thực hiện**.

---

## 2. Tóm tắt cho member

**Điểm tốt:** bộ TC bám sát diff — phủ đủ 5 điểm gọi Dev liệt kê (LIFF list, `checkCanBooking`, 2 job auto-assign, service core), có đối chứng dương (khung hợp lệ vẫn BẬT), đối chứng âm (gán thủ công vẫn cho vượt ca, chế độ trần N / gộp ca bất biến), và bắt đúng biên quan trọng nhất của fix (`breakTimeAfterApplied = 0` — kết thúc phục vụ trùng cuối ca vẫn BẬT). 10 TC do `cucdtk` bổ sung đã lấp đúng những trục AI bỏ sót (partial break = 30', trần 2 không gộp ca, 1 staff, semantic 「1予約=1staff」).

**Phải fix trước khi nghiệm thu:** (1) **cấu hình thật của bug KH — trần 2 + không gộp ca — chỉ có duy nhất TC-REGSHARED001-07 và TC đó chưa chạy lần nào**; (2) 2 TC "bất biến" (TC-REGSHARED001-03/-04) ghi Đạt nhưng `actual` tự khai **không diff được nhánh release**, tức bước 3 của chính TC không chạy — đây là *false pass*, nguy hiểm hơn chưa test; (3) toàn bộ 25 TC chỉ chạy ở `env = local` trong khi task chạm **job nền** → vi phạm RULE-08; (4) **lưới tuần/tháng LIFF** — Dev nêu rõ fix áp cho đường này nhưng 0 TC chạm, mà kho đã có **bug KH #33013** đúng shape "xem theo tuần thấy đặt được nhưng thực tế không"; (5) chức năng **空き枠通知 (danh sách chờ)** gửi tin cho *tất cả* người đang chờ khi slot mở lại — fix thay đổi chính điều kiện "slot có trống không" nhưng Dev không liệt kê và 0 TC cover.

---

## 3. Coverage Matrix

> `Exec` = số TC `pass` / tổng TC cover impact đó (nguồn Studio). **Có TC ≠ đã test.**

| Impact | Loại | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — trừ nhầm nguyên số phút nghỉ sau khỏi mốc cuối ca ⇒ NV hết ca giữa chừng vẫn được tính là phủ trọn khung | Root cause | TC-TOOLKNOW002-01, TC-REGSHARED001-06, **TC-REGSHARED001-07**, TC-FUNCDATE001-05, TC-FUNCDATE001-06 | 5 | **3/5** | **RISK** — cấu hình đúng của bug KH (trần 2 + không gộp ca) chỉ có TC-REGSHARED001-07, **chưa chạy**. TC đã chạy dùng trần 0. |
| **F1** — `CalendarSalonLineBookingService`: `getStartAndEndBooking`, `getListStaffValidInRange`, `checkLimitShiftsNotCombined`, `checkSlotBookingIsValid(Type0)`, `getSumSlot`, `checkStaffFalse`, `isReachMaxBooking` | Function (Direct) | 22/25 TC đi qua chuỗi này | 22 | 13/22 | **RISK** — chỉ 1 giá trị `time_before` (=0), 1 đơn vị slot (30'), 1 kiểu ca (trong ngày), 1 nguồn "bận" (booking LME) |
| **F2a** — `Mobile\CalendarSalonController::getListTimeBooking` | Function (Direct) | TC-TOOLKNOW002-01, TC-REGSHARED001-06 (actual xác nhận gọi đúng `get-list-time-booking`), TC-REGSHARED001-07 | 3 | 2/3 | RISK |
| **F2b** — `Mobile\CalendarSalonController::handleShowListBooking` (**danh sách khung theo tuần / tháng trên LIFF**) | Function (Direct) | *(không TC nào)* | **0** | 0/0 | **🔴 GAP** |
| **F2c** — `Mobile\CalendarSalonController::checkCanBooking` (validate lúc bấm đặt) | Function (Direct) | TC-TOOLVAL2001-01, TC-FUNC001-04 | 2 | 2/2 | **RISK** — chỉ `approve_type=2`; `approve_type=1` (自動承認) chưa có TC |
| **F3** — `Jobs\CalendarSalonStaffAssignment` | Function (Direct) | TC-JOB002-01, TC-JOB002-02 | 2 | 2/2 | **RISK** — chỉ `env=local` (RULE-08); không xác định chạy ở option `スタッフ自動割り当て` nào trong 3 option |
| **F4** — `Jobs\CalendarSalonStaffAssignmentAdmin` | Function (Direct) | TC-JOB002-03 | 1 | 1/1 | **RISK** — như F3 |
| **F5** — `getListStaffValidInRangeOpt3` (trần N cố định — Dev khẳng định bất biến) | Function (bất biến) | TC-REGSHARED001-03 | 1 | 1/1 | **RISK** — pass nhưng `actual` tự khai **không diff được nhánh release**; bước 3 của TC không thực hiện |
| **F6** — `checkLimitShiftsCombined` (gộp ca — Dev khẳng định bất biến) | Function (bất biến) | TC-REGSHARED001-04 | 1 | 1/1 | **RISK** — như F5 |
| **D1** — Dev khai "không có data impact"; cần chứng minh booking cũ không bị đụng | Data | TC-TOOLOLDREC001-01 | 1 | 1/1 | **RISK** — pass nhưng chỉ verify **DB**; bước 1 của TC (quan sát trên màn 予約管理) không thực hiện được → thiếu tầng màn hình (RULE-07) |
| **T1** — Salon Booking (FA-020): khung trống LIFF · validate lúc đặt · tự gán NV | Feature | 23 TC | 23 | 13/23 | **RISK** — thiếu: lưới tuần/tháng · 指名あり · ca qua nửa đêm · block time Google · nghỉ TRƯỚC · staff OFF · đơn vị slot ≠ 30' |
| **T2** — Booking Management (予約管理) | Feature | TC-REGSHARED001-02 (**skip**), TC-TOOLOLDREC001-01 (chỉ DB) | 2 | 0/2 | **🔴 GAP thực tế** — **0 TC thực sự quan sát được trên màn 予約管理**; cả 2 TC đều không dựng được session admin |
| **NEW** — 空き枠通知受け取り設定 (danh sách chờ · 受付再開時 gửi cho TẤT CẢ người chờ) + 受付上限の通知 (`is_notify_full_slot`) | Feature (Dev **không liệt kê**) | *(không TC nào)* | **0** | 0/0 | **🔴 GAP** |

### ORPHAN TCs

**Không có.** Cả 25/25 TC đều map được về `BUG` / `F*` / `D1` / `T*`. TC-REGSHARED001-02 (gán thủ công) tuy nằm **ngoài** 4 file thay đổi nhưng là **đối chứng âm có chủ đích** cho T2 — hợp lệ, không tính orphan.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện được từ `03-dev-impact.md` mục 2:** `"sửa hàm dùng chung"` (chuỗi `isReachMaxBooking` → `checkSlotBookingIsValid` → `getListStaffValidInRange`, **đổi tên tham số, bỏ fallback**, áp cho 5 điểm gọi) + `"validate input"` phụ (điều kiện hợp lệ của slot).

| Fix shape | Câu hỏi adversarial | Trả lời từ bộ TC hiện tại | Kết luận |
|---|---|---|---|
| **sửa hàm dùng chung** (REG-SHARED-001, **Cao**) | Có danh sách nơi ảnh hưởng do Dev cung cấp? | ✅ **Có** — Dev liệt kê 5 điểm gọi + khai đã grep `5/5 điểm gọi isReachMaxBooking` và `getStartAndEndBooking không có nơi gọi nào khác`. Đây là điểm mạnh của ticket này. | Pass |
| **sửa hàm dùng chung** | TC test **từng nơi** trong danh sách? | ❌ **4/5**. `getListTimeBooking` ✅ · `checkCanBooking` ✅ · 2 job ✅ · **`handleShowListBooking` (lưới tuần/tháng) ✗ — 0 TC**. | **[BLOCKER]** |
| **sửa hàm dùng chung** | Chức năng **tương tự** (Salon ⇄ Lesson ⇄ Booking Event) đã rà? | ❌ Không có TC nào, và `03-dev-impact.md` **không nêu** đã kiểm tra Lesson Booking / Event Booking có logic khung-giờ-trống tương tự hay không. Repo có `spec-features/admin/lesson-booking/` và `.../event-booking/`. | **[MAJOR]** |
| **validate input** (FUNC-002/003/004) | Có test **server-side** (không chỉ FE)? | ✅ TC-TOOLVAL2001-01 verify BE guard `create-order` trả `予約がいっぱいです。別の枠を予約してください。` và DB = 0 đơn. Tốt. | Pass |
| **validate input** | Đủ pattern biên? | ⚠️ Có 3 giá trị `breakTimeAfterApplied` (0 / 30 / 60) — **tốt**. Nhưng chỉ **1 giá trị `time_before` (= 0)**, **1 đơn vị slot (30')**, **course toàn bội số của 30'** (30/60/120). Kho có bug #31160 「course có 所要時間 lẻ → lịch hiển thị sai」và TC-SLN-433 「đơn vị nhận booking (13 mức)」. | **[MAJOR]** |
| **validate input** | Đủ luồng vào? | ❌ Chỉ LIFF không-chỉ-định-NV + `approve_type=2`. Thiếu: **指名あり** (`calendar_staff_type=2`, spec §2.6) · `approve_type=1` · admin thêm booking thủ công. | **[BLOCKER]** (指名あり) |
| *(phụ)* **job nền** (JOB-001, **Cao**) | Job verify ở env thật? Output cuối chuỗi? | ❌ Cả 3 TC job chỉ chạy `env=local`, dừng ở `staff_id` trong DB. Không đi tới remind (`event_step_time`) / Google Calendar sync — kho TC-SLN-272/273 cho thấy đổi staff kéo theo 2 hệ quả này. | **[MAJOR] RULE-06 + RULE-08** |

### Symptom-only KH report check

KH **không** report symptom-only — mô tả rất cụ thể (ca đến 20:30 nhưng nhận được yêu cầu đặt lúc 19:00, kèm data ngày 9/4). **Nhưng có tình huống nặng hơn:** ticket này từng có **2 root cause cạnh tranh**:
- **Giả thuyết 1 (support, journal #132656)**: slot ngoài ca là do admin **đổi nhân viên phụ trách thủ công** (MARIN→Yayoi lúc 8/24 15:31) — gán thủ công vốn không bị chặn theo ca.
- **KH bác bỏ (journal #132659)**: *"Vào khoảng 15時 hôm nay đã có yêu cầu đặt lịch từ 9/4 19時 vào nên sau khi phê duyệt tôi đã đổi phụ trách. **Không phải là yêu cầu đặt lịch phát sinh sau khi đổi phụ trách.**"*

Dev đi theo giả thuyết 2. **TC duy nhất kiểm chứng giả thuyết 1 vẫn còn đúng sau fix — TC-REGSHARED001-02 — đang `skip`.** Nghĩa là nhánh mà support từng khẳng định là nguyên nhân **chưa được xác nhận lần nào sau fix**.

→ **[MAJOR] ALT-ROOT-CAUSE**: xem §4.2.

### Anti-pattern

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | ✗ | Fix là tham số cụ thể, không phải generic catch. Có 3 giá trị `breakTimeAfterApplied` (0/30/60). |
| **AP-2** Symptom-only KH report | ✗ (biến thể) | KH report cụ thể, nhưng có **root cause thay thế bị bỏ dở** — xem trên. |
| **AP-3** Happy-path-only regression | ✅ **DÍNH** | TC-REGSHARED001-03 / -04 là 2 TC regression "bất biến" **quan trọng nhất**, và cả 2 đều **không thực hiện được bước đối chiếu 2 nhánh** mà vẫn ghi `pass`. Regression chỉ còn là suy luận code-path, không phải quan sát. → §4.1 |
| **AP-4** Specific code-check disguised as generic catch | ✗ | — |
| **AP-5** Layer-downstream over-coverage | ✗ | Bộ TC không đẻ TC thừa ở layer không bị chạm. TC-REGSHARED001-02 là đối chứng âm có chủ đích, hợp lệ. |
| **AP-6** Mục 3 dev-impact trống | ✗ | Mục 3 đầy đủ, có cả grep audit 5/5 caller. **Điểm mạnh của ticket.** |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi nghiệm thu)

**[BLOCKER] EXEC-01 — Cấu hình đúng của bug KH chưa được chạy lần nào.**
Bug xảy ra ở chế độ 「1つの予約を1人のスタッフのみで対応する（シフトの合算をしない）」 + trần = *tổng nhân viên tiếp nhận được* (Dev mục 1: *"chế độ trần = tổng nhân viên tiếp nhận được"* → `typeLimitCalendar = 2`, không gộp ca). TC duy nhất phủ đúng chế độ này là **TC-REGSHARED001-07** (Studio #13483) — `last_exec = null`, **chưa chạy lần nào**. TC đã chạy pass (TC-REGSHARED001-06) dùng `typeLimitCalendar = 0`, còn TC-TOOLKNOW002-01 không khai `typeLimitCalendar`.
→ **Fix:** chạy TC-REGSHARED001-07 trước tiên, trên staging với đúng cấu hình repro của Kim Cúc (file 01 mục Steps). Chưa chạy TC này thì **chưa có bằng chứng nào cho thấy bug KH đã hết**.

**[BLOCKER] EXEC-02 — TC-REGSHARED001-03 và TC-REGSHARED001-04 ghi `Đạt` dù bước xác minh cốt lõi không được thực hiện (false pass).**
Cả 2 TC có bước 3 là *"Đối chiếu với kết quả cùng dữ liệu trên nhánh `release_step_20260805` (trước fix)"*. `actual` của run #527 ghi nguyên văn: *"chỉ 1 worktree (branch fix) nên **không diff trực tiếp nhánh release**; bất biến suy ra từ code path không đổi + runtime coherent"*. Tức oracle của TC (so 2 nhánh) **không tồn tại**, nhưng TC vẫn `pass`. Đây là *false pass* — nguy hiểm hơn `Chưa test` vì che mất GAP.
→ **Fix:** đổi 2 TC này về `Không đạt` / `Chưa test` trên Studio, dựng 2 worktree (nhánh fix + nhánh release) rồi chạy lại **thật sự đối chiếu**. Nếu không dựng được 2 nhánh, phải đổi steps sang oracle khác (VD: bảng đối chiếu do Dev cung cấp + verify runtime từng khung) và ghi rõ đây là oracle thay thế.

**[BLOCKER] GAP-01 — `handleShowListBooking` (lưới tuần / tháng LIFF): 0 TC.**
Dev mục 2 khai fix *"Áp cho cả 5 điểm gọi: **danh sách khung theo tuần/tháng trên LIFF**, kiểm tra lại lúc bấm đặt, 2 job tự gán nhân viên"*. 25/25 TC chỉ thao tác *"chọn ngày X"* — không TC nào phân biệt lưới **tuần** / **tháng**, cũng không TC nào đối chiếu lưới LIFF với lưới admin. Kho FA-020 đã ghi nhận **bug KH #33013** (`TC-SLN-442`, viewpoint OUT-TRUTH-001) đúng shape này: *"xem theo tuần thấy ngày đặt được nhưng thực tế không"*, expected *"Lưới tuần, lưới tháng và lưới admin nhất quán với nhau"*.
→ **Fix:** bổ sung TC-REGSHARED001-08 (§5). Quan điểm `REG-SHARED-001` (**Cao**) yêu cầu test **từng nơi** trong danh sách Dev cung cấp — hiện mới 4/5.

**[BLOCKER] GAP-02 — Nhánh khách CHỌN nhân viên (指名あり): 0 TC.**
25/25 TC đều ở chế độ *"không chỉ định nhân viên"*. `spec-features/admin/salon-booking/feature-spec.md` §2.6 xác nhận LIFF có bước *"Trang chọn nhân viên (nếu `calendar_staff_type=2`)"*, và kho có `TC-SLN-440` 「Giờ bắt đầu hiển thị lấy theo staff được chọn」 + `TC-SLN-268` 「Đặt lịch CÓ chọn staff cụ thể → giữ nguyên, không random」. Fix đổi **signature** của `getListStaffValidInRange` (*"đổi hẳn tên tham số... dùng trực tiếp (không fallback)"*) và đi qua `getListTimeBooking` — cùng endpoint phục vụ cả 2 chế độ. Sau fix, slot sát cuối ca của staff **được chỉ định** cũng sẽ tắt đi; không TC nào chứng minh nhánh này đúng hay không hỏng.
→ **Fix:** bổ sung TC-REGSHARED001-09 + TC-REGSHARED001-10 (§5). **Hỏi Dev xác nhận** nhánh 指名あり có đi qua `getListStaffValidInRange` không — nếu KHÔNG thì phải ghi rõ vào mục 3 dev-impact và đóng lại như đối chứng âm.

**[BLOCKER] GAP-03 — 空き枠通知受け取り設定 (danh sách chờ) + 受付上限の通知: 0 TC, Dev không liệt kê.**
`spec-features/.../feature-spec.md` §2.4.5 có 「受付上限の通知」→ `calendar_salon.is_notify_full_slot`, `message_notify_full_slot`, bảng `calendar_salon_setting_notify_full_history`. Kho FA-020 nhóm 34 có `TC-SLN-339` (**MSG-001**, **Cao**): 「Action gửi khi có slot trống (受付再開時) — **gửi cho TẤT CẢ người đang chờ**」.
Fix thay đổi **chính điều kiện quyết định một khung là trống hay đầy**. Hai rủi ro cụ thể:
1. Nếu đường quyết định "slot mở lại" **dùng chung** chuỗi `isReachMaxBooking` → sau deploy, tập khách được gửi 受付再開 đổi mà Dev không lường (Dev không liệt kê đường này ở mục 3).
2. Nếu **không dùng chung** → LIFF hiển thị khung TẮT nhưng khách trong danh sách chờ vẫn nhận tin 「có slot trống」 → **gửi tin sai trạng thái thật** (OUT-TRUTH-001).
`MSG-001` là quan điểm **Cao**, trigger khớp (thay đổi điều kiện lọc người nhận), **0 TC cover** → theo quy tắc BƯỚC 3b = `[BLOCKER]`.
→ **Fix:** bổ sung TC-MSG001-01/-02/-03 (§5) **và** yêu cầu Dev bổ sung mục 3 dev-impact: đường 受付再開通知 / `is_notify_full_slot` có đi qua chuỗi vừa sửa không.

### 4.2 Major (nên fix)

**[MAJOR] EXEC-03 — RULE-08 / ENV-003: toàn bộ 25 TC chỉ chạy `env = local`.**
`envAuto` Studio: local 1 run · dev 0 · staging 0 · **prd 0**. Task chạm **job nền** (2 job auto-assign) → RULE-08 cấm kết luận từ local/staging cho hạng mục job. 24/25 TC gắn `env_tag = local-only`.
→ **Fix:** tối thiểu chạy lại trên **staging** toàn bộ nhóm BUG + F3/F4 (job). Nhóm job cần thêm 1 lượt smoke **production** sau deploy theo RULE-08.

**[MAJOR] EXEC-04 — 10/25 TC chưa chạy lần nào, và đúng 10 TC đó là 10 TC do người thật bổ sung.**
Pipeline chạy xong lúc `03:00:34`; `cucdtk` thêm TC lúc `03:34` và `05:23` → chưa có run nào sau đó. Nhóm chưa chạy chứa những trục quan trọng nhất mà AI bỏ sót: `TC-REGSHARED001-07` (trần 2 — cấu hình bug thật), `TC-FUNCDATE001-06` (giá trị `breakTimeAfterApplied` partial = 30, **giá trị partial duy nhất**), `TC-REGSHARED001-01` (lịch 1 staff), 4 TC semantic 「1予約=1staff」.
→ **Fix:** trigger run mới trên Studio cho 10 TC này trước khi kết luận.

**[MAJOR] EXEC-05 — RULE-02: 14 TC `Đạt` nhưng 0 evidence.**
`artifacts: []` ở toàn bộ 15 kết quả; `Evidence thực tế` rỗng ở 25/25 TC. Chỉ có text `actual` do chính runner tự thuật lại. RULE-02: *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng... Không chấp nhận 'đã xem, OK'"*.
→ **Fix:** với TC UI (LIFF slot) — screenshot lưới slot; TC API — response JSON; TC job — log job + query DB. Mỗi TC ghi **loại evidence bắt buộc** vào `Ghi chú`.

**[MAJOR] EXEC-06 — Kết quả Đạt của nhóm rủi ro cao chỉ do AI pipeline tự chạy.**
100% `last_exec.source = ai`, `by = pipeline`, 0 TC do QA người chạy. Nhóm rủi ro cao (job nền, submit LIFF thật, màn 予約管理) cần người xác nhận.
→ **Fix:** QA chạy tay tối thiểu: TC-TOOLKNOW002-01, TC-REGSHARED001-07, TC-TOOLVAL2001-01, 3 TC job.

**[MAJOR] EXEC-07 — 60% TC do AI sinh, `reviewState` chưa `done`, toàn bộ `status = draft`.**
→ **Fix:** Leader duyệt trên Studio và chuyển `reviewState` sau khi xử lý report này.

**[MAJOR] VIEW-01 — 6/25 TC dùng mã quan điểm không có trong `framework/checklist-lme.md`.**
`TOOL-KNOW-002`, `TOOL-VAL2-001`, `TOOL-OLDREC-001` (mã nội bộ Studio, họ `TOOL-*`), `JOB-002` (checklist chỉ có `JOB-001`). Các TC này **không được tính là cover** ở bảng quan điểm §7 F.1 — trong đó có **TC tái hiện bug gốc** (TC-TOOLKNOW002-01).
→ **Fix:** map lại trên Studio: `TOOL-KNOW-002` → `FUNC-001` hoặc `REG-SHARED-001`; `TOOL-VAL2-001` → `CONC-002` / `FUNC-001`; `TOOL-OLDREC-001` → `COMPAT-LEGACY-001` hoặc `DATA-MIG-001`; `JOB-002` → `JOB-001`. Hoặc Leader bổ sung 4 mã này vào `checklist-lme.md` theo RULE-10.

**[MAJOR] VIEW-02 — RULE-01: cả 4 quan điểm hợp lệ đều thiếu loại case, không TC nào ghi lý do.**

| Quan điểm | Ưu tiên | Normal | Abnormal | Boundary | Thiếu |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | 4 | **0** | **0** | Abnormal + Boundary |
| `FUNC-DATE-001` | Cao | **0** | 2 | 4 | Normal |
| `STATE-DEP-001` | Cao | 1 | 1 | **0** | Boundary |
| `REG-SHARED-001` | Cao | 4 | 3 | **0** | Boundary |

Không TC nào ghi lý do ở `Ghi chú` → vi phạm RULE-01.
→ **Fix:** bổ sung theo §5, hoặc ghi lý do miễn trừ vào `Ghi chú` trên Studio.

**[MAJOR] VIEW-03 — 25/25 TC không có `Trạng thái đánh giá spec`.**
`spec_status = null` toàn bộ. Đặc biệt nghiêm trọng vì **spec THỰC SỰ không định nghĩa hành vi này**: `spec-features/admin/salon-booking/feature-spec.md` §9.3 (dòng 1143) tự khai *"Điểm chưa capture được UI: ... 前後の空き時間"* và (dòng 1144) *"Calendar grid chi tiết (week/month view, slot display)"*; §2.4.3 chỉ liệt kê 4 field `time_before` / `time_after` / `time_before_google` / `time_after_google` **không có công thức tính slot**. Kho FA-020 còn đang treo conflict **MT-24** về đúng công thức này (xem §6).
→ **Fix:** mọi TC nhóm BUG phải ghi `Spec không ghi` + nêu rõ **đã hỏi ai chốt hành vi**. Dev đã ghi trong mục 6 là *"Quy tắc human chốt: kết thúc course trùng giờ hết ca thì KHÔNG cộng thời gian nghỉ sau"* — **phải đưa quy tắc này vào file 02 / spec**, không để nằm trong journal Redmine.

**[MAJOR] ALT-ROOT-CAUSE — TC duy nhất kiểm chứng root cause thay thế đang `skip`.**
TC-REGSHARED001-02 (gán nhân viên thủ công vẫn cho vượt ca) là đối chứng âm cho giả thuyết mà support từng khẳng định (journal #132656) và KH bác bỏ (journal #132659). Run #527: *"KHÔNG dựng được session admin BỀN trong sandbox... màn 予約管理 không thao tác được ⇒ skip"*. Runner có ghi chú code-review: *"`saveStaffAssignment` (service:4682) KHÔNG thêm guard `checkCanBooking` ⇒ ngoài scope fix"* — nhưng đó là **đọc code, không phải test**.
→ **Fix:** QA chạy tay TC này trên staging bằng session admin thật. Đây cũng là **TC duy nhất chạm màn 予約管理** ở tầng thao tác (T2 hiện `GAP` thực tế).

**[MAJOR] TC-TOOLOLDREC001-01 — pass nhưng thiếu tầng màn hình (RULE-07).**
Steps bước 1 yêu cầu *"vào 予約管理 mở lịch salon và ngày X"*, nhưng `actual` chỉ verify DB (`tồn tại=true, deleted_at=null, status=1, staff_id=3315`) — cùng lý do session admin như trên. RULE-07 yêu cầu khớp **3 tầng**: DB + màn hình + output.
→ **Fix:** verify lại trên staging, chụp màn 予約管理.

**[MAJOR] RULE-06 — 3 TC job dừng ở `staff_id` trong DB, không đi tới output cuối chuỗi.**
Khi job **không gán được** nhân viên (`staff_id = 0`), booking ở trạng thái không có người phụ trách. Kho FA-020 cho thấy đổi/gán staff kéo theo 2 hệ quả: `TC-SLN-272` (đồng bộ lại Google Calendar theo trạng thái booking) và `TC-SLN-273` (tính lại remind trong `event_step_time`). Spec §7.1.2 xác nhận `NewEventRemindTask` thay token `{staff_name}` → `staffName` hoặc `"指名なし"`.
→ **Fix:** bổ sung TC-JOB001-02 (§5) — verify tin remind + Google Calendar sync khi `staff_id = 0`.

**[MAJOR] GAP-04 — Nguồn "bận" thứ hai (block time Google Calendar): 0 TC.**
Cả 25 TC chỉ tạo trạng thái bận bằng **booking LME**. Kho FA-020: `TC-SLN-284` 「Block time từ Google **KHÔNG** được tính vào limit (nhưng **chặn slot**)」, `TC-SLN-288` (bug #26908), `TC-SLN-294` 「Event sync từ Google được xử lý y hệt booking LME về vùng nghỉ」. `INTG-CAL-001` là quan điểm **Cao**.
→ **Fix:** bổ sung TC-INTGCAL001-01 (§5).

**[MAJOR] GAP-05 — Ca qua nửa đêm (ca qua ngày / biên 00:00): 0 TC.**
Fix hoàn toàn là phép so *"kết thúc phục vụ ≤ cuối ca"*. Kho FA-020 có **cả một nhóm 17 TC** cho 「Ca làm việc — qua ngày & biên 00:00」 (nhóm 18), trong đó `TC-SLN-211` 「Ca qua ngày + thời gian nghỉ trước/sau: slot phía LINE user bị cắt đúng」, `TC-SLN-197` 「Nhập giờ kết thúc 24:00 và 00:00 cho ra cùng 1 ca」, và bug KH **#38519**. Với ca 22:00–01:00, "cuối ca" nằm ở ngày hôm sau → phép so mốc dễ sai.
→ **Fix:** bổ sung TC-FUNCDATE001-07 (§5). *Leader cân nhắc nâng lên `[BLOCKER]` nếu có khách hàng đang dùng ca qua ngày trên production.*

**[MAJOR] GAP-06 — Nghỉ TRƯỚC (`time_before`) không có TC nào; giá trị luôn = 0.**
Spec §2.4.3 xác nhận `calendar_salon_setting_time_free` có **4 field**: `time_before`, `time_after`, `time_before_google`, `time_after_google`. Fix chỉ chạm `breakTimeAfter`, nhưng hàm bị sửa (`getStartAndEndBooking`) là hàm **dựng khoảng bị chiếm**, tức tính cả nghỉ trước. Cùng lỗi "bị cắt ở biên ca" có thể tồn tại đối xứng ở **đầu ca**. Kho `TC-SLN-293` có ma trận 4 cấu hình nghỉ trước/sau; kho `TC-SLN-291` verify 4 field lưu độc lập.
→ **Fix:** bổ sung TC-FUNCDATE001-09 (§5) + **hỏi Dev** xem nghỉ trước có cùng khiếm khuyết không (§6).

**[MAJOR] GAP-07 — Staff OFF / staff ẩn (非表示) không có TC.**
`getListStaffValidInRange` phải loại staff OFF khỏi tập hợp lệ. Kho: `TC-SLN-287` 「Staff OFF vẫn hiển thị ở lưới admin nhưng KHÔNG tính vào limit」, `TC-SLN-286` B3 「staff OFF không tính」, B4 「staff không có ca không tính」. Spec BR-10 「Ẩn nhân viên khỏi trang booking」.
→ **Fix:** bổ sung TC-REGSHARED001-11 (§5).

**[MAJOR] GAP-08 — Chỉ 1 đơn vị slot (30') và course toàn bội số của 30'.**
Kho `TC-SLN-433` 「Khung giờ hiển thị theo đơn vị nhận booking (**13 mức**)」; `TC-SLN-441` bug **#31160** 「chọn course có 所要時間 lẻ → lịch hiển thị sai」. Phép so "kết thúc phục vụ vs cuối ca" nhạy với việc mốc có rơi đúng biên slot hay không.
→ **Fix:** bổ sung TC-FUNCDATE001-08 (§5).

**[MAJOR] GAP-09 — `approve_type = 1` (自動承認) không có TC.**
Spec §2.4.1: `approve_type` (1=自動, 2=Admin手動, 3=禁止キャンセル). TC-FUNC001-04 chỉ test `approve_type=2`. Với `approve_type=1`, booking tạo thẳng `status=1` qua cùng `checkCanBooking`.
→ **Fix:** bổ sung TC-REGSHARED001-12 (§5).

**[MAJOR] GAP-10 — スタッフ自動割り当て có 3 option, TC không khai chạy option nào.**
Kho `TC-SLN-260`: option 1 「利用しない」 · option 2 「random tự do」 · option 3 「theo thứ tự ưu tiên」. Tập ứng viên bị fix thu hẹp lại → với option 3, **kết quả chọn theo thứ tự ưu tiên đổi**. Kho còn có bug **#30555** (`TC-SLN-271`) 「staff KHÔNG có ca vẫn nhận booking khi random」 — đúng vùng regression.
→ **Fix:** bổ sung TC-JOB001-01 (§5) + dùng lại `TC-SLN-271`.

**[MAJOR] GAP-11 — DEPLOY-LIVE-001: LIFF mở trước deploy, submit sau deploy.**
TC-TOOLVAL2001-01 test "**dữ liệu** đổi giữa lúc load và submit" — tốt, nhưng **không** test "**code** đổi giữa lúc load và submit". Fix đổi điều kiện hợp lệ của slot; release không bật maintain. Kho: `TC-SLN-488` (DEPLOY-LIVE-001).
→ **Fix:** bổ sung TC-DEPLOYLIVE001-01 (§5), hoặc dùng lại `TC-SLN-488`.

**[MAJOR] GAP-12 — Chức năng tương tự (Lesson Booking / Event Booking) chưa được rà.**
`REG-SHARED-001` nêu rõ: *"cặp Salon / Lesson / Booking Event là điểm lặp lại"*. `03-dev-impact.md` mục 3 và 4.3 **không nhắc** đến 2 tính năng này. Repo có `spec-features/admin/lesson-booking/` và `spec-features/admin/event-booking/`, kho có `fa019-datlichbaihoc` và `fa021-eventbooking`.
→ **Fix:** **hỏi Dev**: Lesson Booking / Event Booking có hàm tính khung-giờ-trống + nghỉ sau tương tự không, và có cùng khiếm khuyết không. Nếu có → phải mở ticket riêng.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC-REGSHARED001-06 — tiêu đề/`screen` ghi sai endpoint.** Tiêu đề và cột `screen` ghi `API get-detail-list-calendar (EP-B05)`, nhưng `actual` của run ghi rõ: *"EP `get-list-time-booking` (Mobile `getListTimeBooking`, **ĐÚNG điểm fix** — `get-detail-list-calendar` admin **KHÔNG** tính khung trống)"*. 5 TC nhóm `api` đều mang nhãn `screen` sai này. → Sửa `screen` trên Studio thành `get-list-time-booking`.
- **[MINOR] RULE-02 — không TC nào ghi *loại* evidence bắt buộc ở `Ghi chú`.** (Gắn với EXEC-05.)
- **[MINOR] `client_ref` không đồng nhất.** 10 TC human có `client_ref` (`task213.*`), 15 TC AI đều `null`.
- **[MINOR] `priority` rỗng ở 15 TC AI**, trong khi 10 TC human đều `High`.

### 4.4 Nit (gợi ý)

- **[NIT]** Studio đặt tên ref `BR-07` cho 「Thời gian đệm (free time)」, còn `spec-features/admin/salon-booking/feature-spec.md` dùng `BR-07` cho 「Xóa calendar — quy trình 2 bước xác thực qua email」. **Hai hệ đánh số BR khác nhau** — dễ nhầm khi trace. Gợi ý Studio prefix lại (VD `SALON-BR-07`).
- **[NIT]** `task_get_report` báo coverage `0/16 covered · 15 partial · 1 none`; ref **`BR-07` (Thời gian đệm / free time) = 0 TC** dù đây đúng là business rule bị fix sửa cách áp dụng. Sau khi bổ sung TC ở §5 nên gắn `spec_ids` để ref này lên `partial`.
- **[NIT]** Spec §7.1.4 `MonitorCalendarBookingTask` phát hiện overlap booking LME ⇄ block time Google **có tính cả `time_before`/`time_after`**. Job này (Spring Boot) không nằm trong 4 file sửa nên giữ nguyên ngữ nghĩa cũ. Không phải rủi ro trực tiếp, nhưng nếu về sau nghỉ-sau đổi ngữ nghĩa ở tầng PHP mà tầng Java không đổi theo thì 2 bên lệch nhau — ghi lại để theo dõi.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 25 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `điều kiện tiền đề tương đương` → `kết quả mong đợi`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| **N1** — oracle chung: *"tồn tại ≥ 1 nhân viên vừa rảnh vừa phủ trọn thời gian phục vụ ⇒ khung BẬT"* | **TC-STATEDEP001-01** (bao trùm nhất: staff kia vừa bận vừa không đủ ca) + **TC-FUNC001-01** (bản duy nhất đã chạy `pass`) | **TC-FUNC001-03** → **GỘP** vào TC-STATEDEP001-01 (bổ sung nhánh "staff kia RẢNH nhưng không đủ ca" vào `Dữ liệu test`) | **DUP-INFLATE** | Loại case `Normal` · cùng thao tác (LIFF, khoá 120', không chỉ định NV, quan sát khung 19:00) · tiền đề chỉ khác ở tình trạng staff còn lại · expected đều = "BẬT vì có 1 staff phủ trọn" | **[MAJOR]** |
| **N2** — oracle chung: *"kết thúc phục vụ trùng đúng giờ hết ca ⇒ vẫn BẬT, nghỉ sau được tràn qua"* | **TC-FUNCDATE001-05** (đã chạy `pass`) | **TC-FUNCDATE001-03** → **GIỮ NGUYÊN, không xóa** | DUP-SUBSET (có lý do) | Cùng `FUNC-DATE-001` · cùng `Boundary` · cùng oracle | **[MINOR]** — chỉ ghi nhận |

**Giải thích N1 (vì sao là `DUP-INFLATE` chứ không phải `[MINOR]`):** 3 TC cùng một oracle làm `FUNC-001` **trông như có 4 TC**, che mất việc quan điểm này **thiếu hoàn toàn Abnormal và Boundary** (xem VIEW-02). Sau khi gộp, `FUNC-001` thực chất chỉ còn 2 ý định test riêng biệt.

**Gate check trước khi đề nghị xóa (bắt buộc):**
- Giả định xóa **TC-FUNC001-03** → chạy lại BƯỚC 2 + 3b: impact `F1`/`T1` vẫn còn 21 TC cover; quan điểm `FUNC-001` vẫn còn TC-FUNC001-01/-02/-04. **Không mất cover** → nhưng nhánh *"staff RẢNH mà không đủ ca không được tính"* là ý định riêng ⇒ **đổi từ "xóa" sang "GỘP"**, đưa nhánh này vào `Dữ liệu test` của TC-STATEDEP001-01.
- Giả định xóa **TC-FUNCDATE001-03** → mất trục *"độ dài course 30' "*, là trục duy nhất chống việc fix bị hardcode theo dữ liệu 120' của ticket (đúng như `note` của chính TC). ⇒ **KHÔNG xóa.**
- **Không TC nào bị đề nghị xóa hẳn.** Không có `DUP-EXACT`, không có `DUP-CONFLICT` giữa 25 TC.

**Các cặp đã kiểm tra và kết luận KHÔNG trùng:**
- TC-REGSHARED001-06 (`typeLimitCalendar=0`) vs TC-REGSHARED001-07 (`typeLimitCalendar=2`) vs TC-TOOLKNOW002-01 (LIFF) — cùng data, cùng oracle "19:00 ĐÓNG" nhưng **khác trục `typeLimitCalendar`** và **khác tầng quan sát** (API vs UI). Đúng chủ trương tách trục.
- TC-JOB002-02 vs TC-JOB002-03 — cùng tiền đề, cùng oracle `staff_id = 0`, nhưng **2 job class khác nhau**; `REG-SHARED-001` yêu cầu test từng caller. Giữ cả 2.
- TC-FUNCDATE001-01 vs TC-FUNCDATE001-02 — cùng "không được cộng ca 2 staff", nhưng khác cấu hình biên (A/B liền kề tại 19:00 vs tại 19:30) và khác khung quan sát (18:00 vs 19:00). Giữ cả 2.

**⚠️ Không tự xóa TC.** TC Studio là read-only — human quyết định rồi thao tác `testcase_update` / `testcase_delete` trên Studio.

---

## 5. TCs đề xuất bổ sung

### 5a — Đối chiếu kho TCs (bắt buộc, đã thực hiện)

- **File kho:** [kho-tcs/fa020-datlichsalon-サロン・面談予約.md](../../kho-tcs/fa020-datlichsalon-サロン・面談予約.md) — **498 TC**, 54 nhóm chức năng. Đọc có chọn lọc bằng `grep`/`awk` theo nhóm liên quan (không đọc cả file).
- **Vùng regression xác định được từ kho** (nhóm chạm cùng `F*`/`T*`): nhóm 24 `スタッフ自動割り当て` (17 TC) · nhóm 25 `受付上限 — 店舗・スタッフ` (14 TC) · nhóm 26 `前後の空き時間` (4 TC) · nhóm 18 `Ca làm việc — qua ngày & biên 00:00` (17 TC) · nhóm 34 `空き枠通知受け取り設定` (4 TC) · nhóm 46 `LINE user — chọn slot` (11 TC) · nhóm 54 `Dữ liệu cũ & hồi quy` (13 TC).
- **Conflict expected:** ✅ **KHÔNG có conflict** giữa TC đề xuất và kho. Ngược lại, kho **xác nhận hướng fix là đúng**: `TC-SLN-292` (Boundary) 「Slot đầu ngày và cuối ngày **KHÔNG bị trừ thời gian nghỉ**」, expected *"slot cuối cùng = giờ kết thúc − thời gian course, KHÔNG trừ thêm thời gian nghỉ"* — khớp với nguyên tắc `breakTimeAfterApplied = 0` của fix và với quy tắc human chốt ở `03-dev-impact.md` mục 6.
- **Conflict CÒN TREO trong kho:** `MT-24` (mức THẤP, ⏳ CHỜ QUYẾT ĐỊNH) — 「Slot cuối ngày: event Google có bị trừ thời gian nghỉ **trước**, booking LME thì không?」 → đẩy vào §6.
- **TC kho dùng lại được (KHÔNG viết mới):**

| GAP | Dùng lại TC kho | Cần chỉnh gì cho bug này |
|---|---|---|
| GAP-10 (auto-assign bỏ staff không đủ ca) | `TC-SLN-271` — Bug #30555 「staff KHÔNG có ca vẫn nhận booking khi random」 | Đổi tiền đề từ "staff KHÔNG có ca" → "staff **hết ca giữa chừng**" + lịch có nghỉ sau 60' |
| GAP-11 (release live) | `TC-SLN-488` — DEPLOY-LIVE-001 「UI load TRƯỚC release, submit SAU release」 | Chốt slot dùng để test = khung **sát cuối ca** (khung sẽ đổi trạng thái do fix) |
| GAP-04 (block time Google) | `TC-SLN-284` / `TC-SLN-288` | Thêm điều kiện "khung vượt cuối ca của staff còn lại" |
| GAP-07 (staff OFF) | `TC-SLN-287` / `TC-SLN-286` (nhánh B3, B4) | Thêm lịch có nghỉ sau + khung sát cuối ca |

### 5b — Xác nhận chống trùng

> **Đã đối chiếu 25 TC ở BƯỚC 0 + [kho-tcs/fa020-datlichsalon-サロン・面談予約.md](../../kho-tcs/fa020-datlichsalon-サロン・面談予約.md) (498 TC) — không TC đề xuất nào trùng.**
> Riêng 4 GAP ở bảng trên đã chuyển sang **dùng lại TC kho**, không viết mới. `TC No.` bên dưới đã kiểm tra không đụng 25 `TC No.` đang có trong `04-tc-list.md`.

### 5b-bis — Đã sync lên MCP LME TEST STUDIO (2026-08-26)

**15/15 TC ở §5c đã được `testcase_create` vào Studio task `#213`** (`status = draft`, `client_ref` idempotent → chạy lại không nhân bản). **KHÔNG đụng 25 TC cũ** — không sửa, không xóa, không gộp.

| TC No. (report) | Studio `id` | `temp_id` | `client_ref` |
|---|---|---|---|
| TC-REGSHARED001-08 | 14165 | NEW-26 | `task213.review.week-month-grid` |
| TC-REGSHARED001-09 | 14166 | NEW-27 | `task213.review.designated-staff-off` |
| TC-REGSHARED001-10 | 14167 | NEW-28 | `task213.review.designated-staff-boundary` |
| TC-REGSHARED001-11 | 14168 | NEW-29 | `task213.review.hidden-staff-excluded` |
| TC-REGSHARED001-12 | 14169 | NEW-30 | `task213.review.approve-type-auto` |
| TC-FUNCDATE001-07 | 14170 | NEW-31 | `task213.review.overnight-shift` |
| TC-FUNCDATE001-08 | 14171 | NEW-32 | `task213.review.slot-unit-15-course-90` |
| TC-FUNCDATE001-09 | 14172 | NEW-33 | `task213.review.break-before` |
| TC-MSG001-01 | 14223 | NEW-34 | `task213.review.waitlist-no-false-notify` |
| TC-MSG001-02 | 14224 | NEW-35 | `task213.review.waitlist-real-reopen` |
| TC-MSG001-03 | 14225 | NEW-36 | `task213.review.waitlist-boundary-slot` |
| TC-INTGCAL001-01 | 14226 | NEW-37 | `task213.review.google-blocktime-busy` |
| TC-JOB001-01 | 14227 | NEW-38 | `task213.review.autoassign-priority-option` |
| TC-JOB001-02 | 14228 | NEW-39 | `task213.review.no-staff-remind-output` |
| TC-DEPLOYLIVE001-01 | 14229 | NEW-40 | `task213.review.deploy-live-submit` |

**State Studio sau sync:** `exec.total` 25 → **40** · `pass` 14 (không đổi) · `fail` 0 · `other` 1 · `untested` 10 → **25** · `toolWritten.mcp` 10 → 25.

> ⚠️ 15 TC này ghi qua kênh MCP nên `provenance.source = human`, actor = tài khoản đang dùng MCP. Mỗi TC có prefix `[REVIEW round 1 — <severity> <GAP-id>]` ở `note` để phân biệt với 25 TC gốc.
>
> ⚠️ **`untested` tăng lên 25/40 là đúng dự kiến** — đây là TC đề xuất, chưa chạy. Không được đọc con số này như bộ TC xấu đi.
>
> 4 GAP còn lại (GAP-04 phần block-time, GAP-07, GAP-10, GAP-11) đã ghi rõ trong `note` là **dùng lại TC kho** `TC-SLN-284/288`, `TC-SLN-287`, `TC-SLN-271`, `TC-SLN-488` — không tạo TC Studio trùng.

### 5c — Bảng TC bổ sung (16 cột canonical)

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-08 | REG-SHARED-001 | Abnormal | handleShowListBooking: lưới TUẦN và lưới THÁNG trên LIFF phải tắt khung 19:00 giống lưới ngày | - Lịch salon chế độ 「1つの予約を1人のスタッフのみで対応する（シフトの合算をしない）」, trần = 「上限をその時間に受付可能なスタッフ数の合計にする」<br>- 前後の空き時間: nghỉ sau 60 phút<br>- Ngày X: staff A ca 12:00–20:30, staff B ca 14:30–21:00; B đã có 1 booking 17:30–21:00<br>- Khoá học 120 phút, khách KHÔNG chỉ định nhân viên<br>- Đã deploy nhánh `ai_fixbug_40128` | 1. Mở LIFF đặt lịch, chọn khoá 120 phút, để 「指名なし」<br>2. Ở màn chọn ngày giờ, chuyển sang chế độ xem theo **TUẦN**, tới tuần chứa ngày X → chụp trạng thái khung 19:00<br>3. Chuyển sang chế độ xem theo **THÁNG**, tới tháng chứa ngày X → mở ngày X, chụp trạng thái khung 19:00<br>4. Chuyển về chế độ xem theo **NGÀY** cho ngày X → chụp trạng thái khung 19:00<br>5. Đăng nhập admin, mở 予約管理 → lưới ngày X → đối chiếu khung 19:00<br>6. Từ mỗi lưới ở B2/B3, thử bấm chọn khung 19:00 | Ngày X; khoá 120 phút; khung xét = 19:00 | - Cả 3 lưới LIFF (tuần / tháng / ngày) đều hiển thị khung 19:00 **TẮT**, không bấm chọn được<br>- Lưới admin 予約管理 nhất quán: không còn nhận đặt ở 19:00<br>- Không lưới nào hiển thị 19:00 BẬT rồi mới báo lỗi ở bước sau<br>- Các khung ≤ 18:30 vẫn BẬT ở cả 3 lưới | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-01** (impact F2b `handleShowListBooking` — Dev khai fix áp cho "danh sách khung theo tuần/tháng" nhưng 0 TC). Regression. Dẫn từ kho `TC-SLN-442` (bug KH #33013 「xem theo tuần thấy ngày đặt được nhưng thực tế không」) và `TC-SLN-435/436/437`. **Evidence bắt buộc**: screenshot 3 lưới LIFF + lưới admin cùng ngày X. Spec chưa ghi (feature-spec §9.3 khai chưa capture week/month view) → hỏi Leader chốt. |
| TC-REGSHARED001-09 | REG-SHARED-001 | Abnormal | 指名あり: khách chọn đúng nhân viên hết ca giữa chừng thì khung vượt ca phải TẮT | - Lịch salon `calendar_staff_type = 2` (LIFF **có** bước chọn nhân viên)<br>- Cùng cấu hình bug: không gộp ca, nghỉ sau 60 phút, khoá 120 phút<br>- Ngày X: staff A ca 12:00–20:30 và đang RẢNH; staff B ca 14:30–21:00<br>- Đã deploy nhánh fix | 1. Mở LIFF đặt lịch, chọn khoá 120 phút<br>2. Ở bước chọn nhân viên, chọn **đích danh staff A**<br>3. Chọn ngày X<br>4. Quan sát khung bắt đầu 19:00<br>5. Nếu khung 19:00 vẫn bấm được → điền form và bấm gửi yêu cầu đặt lịch, quan sát thông báo và kiểm tra đơn có được tạo không | Ngày X; 指名 = staff A; khoá 120 phút; khung xét = 19:00 | - Khung 19:00 hiển thị **TẮT** vì phục vụ 19:00–21:00 vượt cuối ca A (20:30), dù A đang rảnh<br>- Nếu bấm được: hệ thống chặn ở bước submit, không tạo bản ghi booking khung 19:00<br>- Khung 18:30 (kết thúc đúng 20:30) vẫn BẬT và đặt được | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-02** (impact F1/F2a/T1 — 25/25 TC hiện tại đều 「指名なし」). Dẫn từ kho `TC-SLN-440`, `TC-SLN-268`; spec §2.6 (bước chọn nhân viên khi `calendar_staff_type=2`). **Evidence**: screenshot LIFF sau khi chọn staff A + response `get-list-time-booking`. ⚠️ Cần Dev xác nhận nhánh 指名あり có đi qua `getListStaffValidInRange` không. |
| TC-REGSHARED001-10 | REG-SHARED-001 | Boundary | 指名あり: kết thúc phục vụ trùng đúng giờ hết ca của nhân viên được chỉ định thì vẫn BẬT | - Như TC-REGSHARED001-09<br>- Staff A ca 12:00–20:30, đang rảnh cả ngày X<br>- Nghỉ sau 60 phút (được phép tràn qua cuối ca) | 1. Mở LIFF, chọn khoá 120 phút<br>2. Chọn đích danh staff A<br>3. Chọn ngày X<br>4. Quan sát khung 18:30<br>5. Đặt thử khung 18:30: điền form, bấm gửi yêu cầu đặt lịch<br>6. Kiểm tra đơn vừa tạo trên màn 予約管理 | Ngày X; 指名 = staff A; khoá 120 phút; khung xét = 18:30 (phục vụ 18:30–20:30 = đúng cuối ca A) | - Khung 18:30 **BẬT** và đặt được<br>- Đơn tạo thành công, nhân viên phụ trách = A, thời gian 18:30–20:30<br>- Fix không siết nhầm khung biên ở nhánh 指名あり | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-02 + RULE-01 (bổ sung `Boundary` cho REG-SHARED-001 — hiện 0 Boundary/7 TC)**. Cặp đối chứng dương của TC-REGSHARED001-09. **Evidence**: screenshot LIFF + bản ghi booking trên 予約管理. |
| TC-REGSHARED001-11 | REG-SHARED-001 | Normal | Nhân viên đang ẩn khỏi trang đặt lịch (非表示) không được tính vào tập nhân viên hợp lệ | - Cùng cấu hình bug (không gộp ca, nghỉ sau 60 phút, khoá 120 phút, 指名なし)<br>- Ngày X: staff A ca 12:00–20:30; staff C ca 14:30–21:00 và **đang RẢNH** nhưng bị đặt **ẩn khỏi trang booking**<br>- Không có staff nào khác | 1. Vào tab 「コース・スタッフ」 xác nhận staff C đang ở trạng thái ẩn khỏi trang đặt lịch<br>2. Mở LIFF đặt lịch, chọn khoá 120 phút, 指名なし<br>3. Chọn ngày X<br>4. Quan sát khung 19:00<br>5. Bỏ ẩn staff C, reload LIFF, quan sát lại khung 19:00 | Ngày X; staff C rảnh nhưng bị ẩn; khung xét = 19:00 | - B4: khung 19:00 **TẮT** — staff C bị ẩn không được đếm là nhân viên khả dụng, dù ca của C phủ trọn 19:00–21:00<br>- B5: sau khi bỏ ẩn C, khung 19:00 chuyển **BẬT**<br>- Trạng thái ẩn/hiện của staff phải làm đổi trạng thái khung tương ứng | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-07** (impact F1 `getListStaffValidInRange`). Dẫn từ kho `TC-SLN-287`, `TC-SLN-286` (nhánh B3/B4); spec BR-10 「Ẩn nhân viên khỏi trang booking」. **Evidence**: screenshot cài đặt staff + 2 lần screenshot lưới slot trước/sau. |
| TC-REGSHARED001-12 | REG-SHARED-001 | Normal | approve_type=1 (自動承認): khung hợp lệ tạo booking xác nhận ngay, khung vượt ca vẫn bị chặn | - Cùng cấu hình bug nhưng đặt 「各種設定 → 予約の確認方法」 = **自動** (`approve_type = 1`)<br>- Ngày X: A ca 12:00–20:30, B ca 14:30–21:00, B bận 17:30–21:00<br>- Khoá 120 phút, 指名なし | 1. Mở LIFF, chọn khoá 120 phút, 指名なし, chọn ngày X<br>2. Chọn khung **18:30** (hợp lệ) → điền form → gửi<br>3. Quan sát tin nhắn LINE khách nhận được và trạng thái đơn trên 予約管理<br>4. Quay lại LIFF, quan sát khung **19:00**<br>5. Nếu bấm được 19:00 → gửi và quan sát kết quả | Ngày X; `approve_type = 1`; khung 18:30 và 19:00 | - B2/B3: đơn 18:30 tạo ở trạng thái **đã xác nhận** (không phải chờ duyệt); khách nhận tin xác nhận đặt lịch trên **LINE app thật**<br>- B4: khung 19:00 **TẮT**<br>- B5: nếu ép gửi → bị chặn, không tạo đơn 19:00 | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-09** (impact F2c `checkCanBooking` — hiện chỉ có `approve_type=2`). Spec §2.4.1 `approve_type` (1=自動, 2=Admin手動, 3=禁止キャンセル). **RULE-06**: verify tin nhắn trên **LINE app thật**, không dừng ở màn admin. **Evidence**: screenshot LINE app + bản ghi trên 予約管理. |
| TC-FUNCDATE001-07 | FUNC-DATE-001 | Boundary | Ca qua nửa đêm: khung vượt giờ hết ca rạng sáng phải TẮT, khung kết thúc đúng cuối ca vẫn BẬT | - Lịch salon không gộp ca, nghỉ sau 60 phút, khoá 120 phút, 指名なし<br>- Ngày X: staff A có ca **qua ngày 22:00–01:00** (kết thúc 01:00 ngày X+1); staff B ca 18:00–23:00 và đã có booking 21:00–23:00<br>- Không có staff nào khác | 1. Mở LIFF, chọn khoá 120 phút, 指名なし, chọn ngày X<br>2. Quan sát khung **23:00** (phục vụ 23:00–01:00 = đúng cuối ca A)<br>3. Quan sát khung **00:00** (phục vụ 00:00–02:00, vượt cuối ca A 01:00)<br>4. Đặt thử khung ở B2 và kiểm tra đơn trên 予約管理 (đơn thuộc ngày nào)<br>5. Lặp lại quan sát ở lưới **tuần** và lưới **tháng** | Ca A 22:00–01:00 (qua ngày); khoá 120 phút; khung xét = 23:00 và 00:00 | - Khung **23:00 BẬT** — kết thúc phục vụ 01:00 trùng đúng cuối ca A, nghỉ sau được phép tràn qua<br>- Khung **00:00 TẮT** — phục vụ tới 02:00 vượt cuối ca A<br>- Đơn đặt ở 23:00 hiển thị đúng ở cả ngày X và ngày X+1 theo quy ước ca qua ngày, không sinh đơn ảo<br>- Lưới tuần/tháng nhất quán với lưới ngày | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-05** (impact F1 — phép so "kết thúc phục vụ ≤ cuối ca" khi cuối ca nằm sang ngày hôm sau). Dẫn từ kho nhóm 18 (17 TC): `TC-SLN-211`, `TC-SLN-197`, `TC-SLN-202`, `TC-SLN-203`, bug KH #38519. **Evidence**: screenshot lưới slot + bản ghi booking (ngày sở hữu). ⚠️ Leader cân nhắc nâng BLOCKER nếu production có KH dùng ca qua ngày. |
| TC-FUNCDATE001-08 | FUNC-DATE-001 | Boundary | Đơn vị nhận booking 15 phút + course 90 phút: mốc kết thúc phục vụ không rơi đúng biên slot 30 phút | - Lịch salon không gộp ca, nghỉ sau 60 phút, 指名なし<br>- Đặt 「予約受付単位」 = **15 phút** (khác mặc định 30 phút)<br>- Course dài **90 phút**<br>- Ngày X: staff A ca 12:00–20:30 và đang rảnh; không có staff khác | 1. Mở LIFF, chọn khoá **90 phút**, 指名なし, chọn ngày X<br>2. Quan sát khung **19:00** (phục vụ 19:00–20:30 = đúng cuối ca A)<br>3. Quan sát khung **19:15** (phục vụ 19:15–20:45, vượt cuối ca A)<br>4. Đặt thử khung ở B2, kiểm tra giờ đơn trên 予約管理<br>5. Đổi 予約受付単位 sang 10 phút, reload, quan sát lại khung 19:00 và 19:20 | 予約受付単位 = 15 phút; course = 90 phút; ca A đến 20:30 | - Khung **19:00 BẬT** (kết thúc đúng 20:30)<br>- Khung **19:15 TẮT** (kết thúc 20:45 > 20:30)<br>- Giờ đơn đã tạo = 19:00–20:30, khớp giữa LIFF, 予約管理 và DB<br>- Sau khi đổi đơn vị sang 10 phút, ranh giới BẬT/TẮT vẫn tính theo mốc kết thúc phục vụ thật, không lệch | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-08** (impact F1 — chống fix bị hardcode theo đơn vị 30' / course bội số 30'). Dẫn từ kho `TC-SLN-433` (13 mức đơn vị nhận booking), `TC-SLN-441` (bug #31160 「course 所要時間 lẻ → lịch hiển thị sai」). **Evidence**: screenshot lưới slot ở 2 mức đơn vị + bản ghi booking. |
| TC-FUNCDATE001-09 | FUNC-DATE-001 | Normal | Lịch có cài nghỉ TRƯỚC (前の空き時間): hành vi khung đầu ca không bị fix làm đổi | - Lịch salon không gộp ca, 指名なし, khoá 120 phút<br>- 前後の空き時間: **nghỉ trước = 60 phút, nghỉ sau = 0**<br>- Ngày X: staff A ca 12:00–20:30, đang rảnh<br>- Ghi lại kết quả trên nhánh `release_step_20260805` (trước fix) làm mốc so sánh | 1. Trên nhánh **trước fix**, mở LIFF, chọn khoá 120 phút, ngày X → ghi lại trạng thái toàn bộ khung, đặc biệt khung đầu ca 12:00 và khung cuối 18:30<br>2. Chuyển sang nhánh **fix**, lặp lại y hệt<br>3. Đối chiếu từng khung giữa 2 nhánh<br>4. Lặp lại với cấu hình nghỉ trước 60 + nghỉ sau 60 | Nghỉ trước = 60 phút; nghỉ sau = 0 rồi 60; ca A 12:00–20:30; khoá 120 phút | - Với nghỉ sau = 0: trạng thái **mọi khung GIỐNG HỆT** giữa 2 nhánh (fix chỉ chạm nghỉ sau)<br>- Khung đầu ca 12:00 vẫn BẬT — nghỉ TRƯỚC không được trừ vào giờ mở ca<br>- Với nghỉ trước 60 + nghỉ sau 60: chỉ các khung sát **cuối ca** đổi trạng thái; khung đầu ca không đổi | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-06** (impact F1 `getStartAndEndBooking` — hàm dựng khoảng bị chiếm, tính cả nghỉ trước; hiện 25/25 TC đều `time_before = 0`). Dẫn từ kho `TC-SLN-291`, `TC-SLN-292`, `TC-SLN-293`. ⚠️ Liên quan conflict **MT-24** đang treo trong kho — xem §6. **Evidence**: bảng đối chiếu trạng thái từng khung trên 2 nhánh + screenshot. |
| TC-MSG001-01 | MSG-001 | Abnormal | 空き枠通知: khung chuyển sang TẮT do fix KHÔNG được gửi tin 「受付再開」 cho khách đang chờ | - Lịch salon cùng cấu hình bug (không gộp ca, nghỉ sau 60 phút, khoá 120 phút)<br>- Đã BẬT 「空き枠通知受け取り設定」 (danh sách chờ)<br>- 3 khách F1/F2/F3 đang ở trạng thái chờ thông báo cho khung 19:00 ngày X<br>- Ngày X: A ca 12:00–20:30, B ca 14:30–21:00; B đang bận 17:30–21:00<br>- Chuẩn bị 3 máy LINE thật (hoặc 3 tài khoản LINE) để nhận tin | 1. Xác nhận trước deploy: khung 19:00 đang BẬT, 3 khách đang ở danh sách chờ<br>2. Deploy nhánh `ai_fixbug_40128`<br>3. Chờ qua ít nhất 1 chu kỳ job gửi thông báo danh sách chờ<br>4. Kiểm tra hộp thoại LINE của F1, F2, F3<br>5. Mở LIFF bằng tài khoản F1 → quan sát khung 19:00<br>6. Kiểm tra bảng lịch sử thông báo và trạng thái chờ của F1/F2/F3 | 3 khách chờ khung 19:00; khoá 120 phút; ngày X | - **Không** khách nào trong F1/F2/F3 nhận tin 「受付再開」 cho khung 19:00, vì sau fix khung này ĐÓNG<br>- LIFF của F1 hiển thị khung 19:00 **TẮT** — trạng thái tin nhắn và trạng thái LIFF **nhất quán**<br>- 3 khách vẫn giữ nguyên trạng thái đang chờ, không bị hủy khỏi danh sách chờ<br>- Không phát sinh dòng lịch sử thông báo sai cho khung 19:00 | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp GAP-03** (impact NEW — Dev **không liệt kê** đường 空き枠通知 ở mục 3/4). Dẫn từ kho `TC-SLN-339` (MSG-001 「gửi cho TẤT CẢ người đang chờ」), `TC-SLN-337`, `TC-SLN-340`; spec §2.4.5 `is_notify_full_slot` / `message_notify_full_slot`. **RULE-06**: verify nhận tin trên **LINE app thật**. **RULE-08**: gửi tin ra ngoài → phải xác nhận ở PRODUCTION sau deploy. **Evidence**: screenshot 3 hộp thoại LINE + lịch sử thông báo. |
| TC-MSG001-02 | MSG-001 | Normal | 空き枠通知: khi khung THẬT SỰ mở lại thì vẫn gửi đúng và đủ cho tất cả khách đang chờ | - Như TC-MSG001-01, đã deploy nhánh fix<br>- Khung 19:00 ngày X đang ĐÓNG; F1/F2/F3 đang chờ thông báo khung này | 1. Admin hủy booking 17:30–21:00 của staff B (B trở lại rảnh, ca B phủ trọn 19:00–21:00)<br>2. Chờ qua 1 chu kỳ job gửi thông báo danh sách chờ<br>3. Kiểm tra hộp thoại LINE của F1, F2, F3<br>4. Mở LIFF bằng F1 → quan sát và đặt thử khung 19:00<br>5. Kiểm tra lịch sử thông báo | Hủy booking của B; khung 19:00; 3 khách đang chờ | - **Cả 3 khách** F1/F2/F3 đều nhận tin 「受付再開」 trên LINE app thật, nội dung đúng `message_notify_full_slot` đã cài<br>- LIFF của F1 hiển thị khung 19:00 **BẬT** và đặt được<br>- Ai đặt trước thì được; sau khi đầy thì các khách còn lại không đặt được nữa<br>- Lịch sử thông báo ghi đủ 3 bản ghi | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp GAP-03** — đối chứng dương (fix không chặn nhầm luồng thông báo hợp lệ). Dẫn từ kho `TC-SLN-339` (nhánh B1/B3). **RULE-06** + **RULE-08** như TC trên. **Evidence**: screenshot 3 hộp thoại LINE + lịch sử thông báo + bản ghi booking. |
| TC-MSG001-03 | MSG-001 | Boundary | 空き枠通知 tại khung biên: khung kết thúc phục vụ trùng đúng cuối ca vẫn được coi là còn trống | - Như TC-MSG001-01, đã deploy nhánh fix<br>- Ngày X: staff A ca 12:00–20:30, đang rảnh<br>- Khách F1 đang chờ thông báo cho khung **18:30** (phục vụ 18:30–20:30 = đúng cuối ca A)<br>- Trước đó khung 18:30 vừa bị 1 booking chiếm, nay booking đó bị hủy | 1. Xác nhận F1 đang ở danh sách chờ khung 18:30<br>2. Hủy booking đang chiếm khung 18:30<br>3. Chờ qua 1 chu kỳ job gửi thông báo<br>4. Kiểm tra hộp thoại LINE của F1<br>5. Mở LIFF bằng F1 → quan sát khung 18:30 | Khung 18:30 (kết thúc đúng cuối ca A 20:30); nghỉ sau 60 phút | - F1 **nhận** tin 「受付再開」 cho khung 18:30<br>- LIFF hiển thị khung 18:30 **BẬT** — khớp với nội dung tin nhắn<br>- Fix không làm khung biên bị coi nhầm là đã đầy nên bỏ sót thông báo | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp GAP-03 + RULE-01 (bổ sung `Boundary` cho MSG-001)**. Biên `breakTimeAfterApplied = 0` ở tầng thông báo. **RULE-06** + **RULE-08**. **Evidence**: screenshot hộp thoại LINE của F1 + screenshot lưới slot. |
| TC-INTGCAL001-01 | INTG-CAL-001 | Abnormal | Nhân viên bận do block time đồng bộ từ Google Calendar: khung vượt cuối ca vẫn phải TẮT | - Lịch salon cùng cấu hình bug (không gộp ca, nghỉ sau 60 phút, khoá 120 phút, 指名なし)<br>- Ngày X: staff A ca 12:00–20:30, rảnh; staff B ca 14:30–21:00<br>- Staff B **đã liên kết Google Calendar**; trên Google Calendar của B có event 17:30–21:00 ngày X (KHÔNG phải booking LME)<br>- Đã chờ job đồng bộ Google đưa event thành block time trong LME | 1. Xác nhận trên 予約管理 rằng block time 17:30–21:00 của B đã đồng bộ về từ Google<br>2. Mở LIFF đặt lịch, chọn khoá 120 phút, 指名なし, chọn ngày X<br>3. Quan sát khung **19:00**<br>4. Quan sát khung **18:30**<br>5. Xóa event trên Google Calendar của B, chờ đồng bộ, quan sát lại khung 19:00 | Block time Google của B 17:30–21:00; ngày X; khoá 120 phút | - B3: khung 19:00 **TẮT** — B bận do block time Google, A hết ca 20:30 ⇒ không ai phủ trọn 19:00–21:00. Kết quả **giống hệt** trường hợp B bận do booking LME<br>- B4: khung 18:30 **BẬT** (kết thúc đúng cuối ca A)<br>- B5: sau khi xóa event Google và đồng bộ lại, khung 19:00 chuyển **BẬT** | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-04** (impact F1/T1 — nguồn "bận" thứ hai chưa có TC nào). Dẫn từ kho `TC-SLN-284` 「Block time Google KHÔNG tính vào limit nhưng CHẶN slot」, `TC-SLN-288` (bug #26908), `TC-SLN-294`. **Evidence**: screenshot Google Calendar của B + screenshot 予約管理 + screenshot lưới slot LIFF 2 lần. |
| TC-JOB001-01 | JOB-001 | Abnormal | Job tự gán ở option 「thứ tự ưu tiên」: bỏ qua nhân viên ưu tiên cao nhưng hết ca giữa chừng, chọn người kế tiếp đủ ca | - Lịch salon không gộp ca, nghỉ sau 60 phút, khoá 120 phút<br>- Đặt 「スタッフ自動割り当て」 = **option 3 (theo thứ tự ưu tiên)**, thứ tự: A → B → C<br>- Ngày X: A ca 12:00–20:30 (rảnh) · B ca 14:30–21:00 (rảnh) · C ca 14:30–21:00 (rảnh)<br>- Đã có 1 booking 19:00–21:00 tạo với 指名なし, chưa gán nhân viên | 1. Xác nhận thứ tự ưu tiên đang là A → B → C trên màn cài đặt<br>2. Kích hoạt job `CalendarSalonStaffAssignment` cho booking khung 19:00<br>3. Kiểm tra nhân viên được gán trên màn 予約管理 và trong DB<br>4. Đổi thứ tự ưu tiên thành C → A → B, tạo booking 19:00 mới, chạy lại job<br>5. Kiểm tra log job xem có lỗi/exception không | Option auto-assign = 3 (ưu tiên A→B→C); booking 19:00–21:00 | - B3: job **bỏ qua A** (ca đến 20:30, không phủ hết 21:00) và gán **B** — người đầu tiên trong thứ tự ưu tiên còn đủ ca<br>- B5 (thứ tự C→A→B): job gán **C**<br>- Job chạy thành công, không exception; log ghi rõ nhân viên được chọn<br>- Không booking nào bị gán cho nhân viên hết ca giữa chừng | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp GAP-10** (impact F3 — 3 TC job hiện có không khai chạy ở option auto-assign nào). Dẫn từ kho `TC-SLN-260` (3 option), `TC-SLN-265` (option 3), `TC-SLN-271` (bug #30555). **RULE-08**: job nền → phải xác nhận ở PRODUCTION sau deploy. **Evidence**: log job (thấy nhân viên được chọn) + query DB `staff_id` + screenshot 予約管理. |
| TC-JOB001-02 | JOB-001 | Normal | Sau khi job KHÔNG gán được nhân viên: tin remind và đồng bộ Google Calendar vẫn xử lý đúng | - Cùng cấu hình bug; đã bật remind trước giờ đặt lịch<br>- Ngày X: A ca 12:00–20:30, B ca 14:30–21:00 và bận 17:30–21:00<br>- Có 1 booking 19:00–21:00 (đơn cũ tạo trước fix, 指名なし) → sau fix job không tìm được nhân viên đủ ca<br>- Có máy LINE thật của khách đặt đơn này | 1. Kích hoạt job auto-assign cho booking 19:00 → xác nhận không gán được nhân viên<br>2. Kiểm tra bản ghi remind trong hàng đợi gửi tin của booking này<br>3. Chờ đến thời điểm gửi remind<br>4. Kiểm tra tin nhắn khách nhận trên **LINE app thật** — đặc biệt phần tên nhân viên<br>5. Kiểm tra Google Calendar của các nhân viên xem có event rác/sai không<br>6. Kiểm tra màn 予約管理 hiển thị đơn này thế nào | booking 19:00–21:00 không có nhân viên phụ trách | - Remind vẫn được gửi đúng giờ, **không lỗi job**<br>- Tin nhắn trên LINE hiển thị tên nhân viên là 「指名なし」 (hoặc giá trị mặc định theo cài đặt), **không để trống, không hiện `null`/`0`**<br>- Không tạo event Google Calendar cho nhân viên nào<br>- 予約管理 hiển thị đơn ở trạng thái chưa có người phụ trách, admin gán tay được | Chưa test | | **PRODUCTION** | | | | Spec không ghi | **Lấp MAJOR RULE-06** (3 TC job hiện dừng ở `staff_id` trong DB). Dẫn từ kho `TC-SLN-272` (đổi staff → sync Google), `TC-SLN-273` (đổi staff → tính lại remind); spec §7.1.2 (token `{staff_name}` → `staffName` hoặc 「指名なし」). **RULE-06** + **RULE-08**. **Evidence**: screenshot tin nhắn trên LINE app + log job remind + screenshot Google Calendar. |
| TC-DEPLOYLIVE001-01 | DEPLOY-LIVE-001 | Abnormal | Màn LIFF mở TRƯỚC deploy, bấm gửi SAU deploy: khung nay đã đóng phải bị chặn rõ ràng | - Cùng cấu hình bug; **chưa** deploy nhánh fix (đang chạy `release_step_20260805`)<br>- Ngày X: A ca 12:00–20:30, B ca 14:30–21:00 và bận 17:30–21:00 (khung 19:00 đang BẬT do bug)<br>- Release **không** bật maintain | 1. Trước deploy: mở LIFF, chọn khoá 120 phút, 指名なし, chọn ngày X và khung **19:00**, đi tới màn xác nhận. **Giữ nguyên màn hình, không reload**<br>2. Deploy nhánh `ai_fixbug_40128` lên môi trường đang test<br>3. Quay lại đúng tab LIFF đang mở, điền đủ thông tin và bấm gửi yêu cầu đặt lịch<br>4. Quan sát thông báo hiển thị cho khách<br>5. Kiểm tra DB/màn 予約管理 xem có đơn 19:00 nào được tạo không<br>6. Kiểm tra log server xem có exception 500 không | Khung 19:00; client tải trước deploy, submit sau deploy | - Hệ thống **chặn** tạo đơn, hiển thị thông báo dễ hiểu cho khách (VD 「予約がいっぱいです。別の枠を予約してください。」)<br>- **Không** tạo bản ghi booking 19:00, **không** lưu nửa vời (không có đơn thiếu trường)<br>- **Không** có exception 500 trong log<br>- Khách reload thì thấy khung 19:00 đã TẮT | Chưa test | | STAGING | | | | Spec không ghi | **Lấp GAP-11** (khác TC-TOOLVAL2001-01: TC đó test **dữ liệu** đổi giữa chừng, TC này test **code** đổi giữa chừng — client cũ gọi server mới). Dẫn từ kho `TC-SLN-488` (DEPLOY-LIVE-001). **Evidence**: screenshot màn LIFF cũ trước deploy + screenshot thông báo sau submit + log request + query DB. |

---

## 6. Spec update needed

| # | Vấn đề | Nguồn | Cần ai chốt |
|---|---|---|---|
| **S1** | **Không có spec cho công thức tính khung giờ trống khi có 前後の空き時間.** `spec-features/admin/salon-booking/feature-spec.md` §2.4.3 chỉ liệt kê 4 field (`time_before`, `time_after`, `time_before_google`, `time_after_google`) **không có công thức**; §9.3 tự khai chưa capture được UI 「前後の空き時間」 và 「Calendar grid chi tiết (week/month view, slot display)」. Không có chuẩn để đánh giá Expected của toàn bộ nhóm TC BUG. | feature-spec §2.4.3, §9.3 (dòng 1143–1144) | **Leader + Dev** |
| **S2** | **Quy tắc quyết định đang nằm trong journal Redmine, không nằm trong spec.** `03-dev-impact.md` mục 6 ghi: *"Quy tắc human chốt: kết thúc course trùng giờ hết ca thì KHÔNG cộng thời gian nghỉ sau → `breakTimeAfterApplied = 0`"*. Đây là **business rule mới**, hiện chỉ tồn tại trong 1 comment auto-fixbug. | `03-dev-impact.md` mục 6 | **Leader** — đưa vào `spec-features/admin/salon-booking/feature-spec.md` §2.4.3 dưới dạng BR mới |
| **S3** | **Conflict CÒN TREO trong kho: `MT-24`** (mức THẤP, ⏳ CHỜ QUYẾT ĐỊNH) — 「Slot cuối ngày: event Google có bị trừ thời gian nghỉ **trước**, booking LME thì không?」. Nguồn TC gốc mâu thuẫn: r1297 (booking LME) 「slot cuối = time end cửa hàng − time course」 vs r1305 (event Google) 「slot cuối = time end cửa hàng − time course **− time nghỉ trước**」. Fix #40128 vừa chốt nguyên tắc cho nghỉ **SAU**, nên đây là lúc chốt luôn nghỉ **TRƯỚC** cho nhất quán. | kho-tcs FA-020, MT-24 | **Leader + Dev** |
| **S4** | **Nghỉ TRƯỚC có cùng khiếm khuyết không?** `getStartAndEndBooking` là hàm dựng khoảng bị chiếm, tính cả nghỉ trước. Lỗi gốc là "phần nghỉ bị cắt ở biên ca nhưng vẫn bị trừ khỏi mốc so sánh". Cần Dev xác nhận nhánh nghỉ trước ở **đầu ca** có bị đối xứng hay không. | `03-dev-impact.md` mục 1–2 | **Dev** |
| **S5** | **Đường 空き枠通知 / 受付上限の通知 có đi qua chuỗi vừa sửa không?** Mục 3 và 4.3 của dev-impact **không nhắc** đến `is_notify_full_slot` / danh sách chờ, dù fix thay đổi chính điều kiện "khung còn trống hay đã đầy". | feature-spec §2.4.5; kho `TC-SLN-339` | **Dev** — bổ sung vào mục 3 dev-impact |
| **S6** | **Nhánh 指名あり (`calendar_staff_type = 2`) có đi qua `getListStaffValidInRange` không?** Nếu **có** → phải có TC (§5). Nếu **không** → ghi rõ vào mục 3 dev-impact như đối chứng âm, để vòng review sau không raise lại. | feature-spec §2.6 | **Dev** |
| **S7** | **Lesson Booking / Event Booking có logic khung-giờ-trống + nghỉ sau tương tự không?** `REG-SHARED-001` nêu rõ cặp Salon / Lesson / Booking Event là điểm lặp lại. Dev-impact không nhắc. | `framework/checklist-lme.md` REG-SHARED-001; `spec-features/admin/lesson-booking/`, `.../event-booking/` | **Dev** — nếu có, mở ticket riêng |
| **S8** | **Trùng mã `BR-07` giữa 2 hệ thống.** Studio dùng `BR-07` = 「Thời gian đệm (free time)」; feature-spec dùng `BR-07` = 「Xóa calendar — quy trình 2 bước xác thực qua email」. | `task_get_report(213)` vs feature-spec §5 | **Leader** — [NIT], thống nhất namespace |

---

## 7. Checklist đã chạy

| Mục | Nội dung | Kết quả |
|---|---|---|
| **A.1** | Bug root cause có TC verify | ⚠️ **Fail một phần** — có TC (TC-TOOLKNOW002-01) và đã pass, nhưng **cấu hình đúng của bug KH (trần 2 + không gộp ca) chưa chạy lần nào** (EXEC-01) |
| **A.2** | Function impact (4.1) đủ TC | ❌ **Fail** — 5/6 function nhóm; `handleShowListBooking` (lưới tuần/tháng) 0 TC (GAP-01) |
| **A.3** | Data impact (4.2) đủ TC | ⚠️ Pass yếu — Dev khai không có data impact; TC-TOOLOLDREC001-01 verify booking cũ nhưng thiếu tầng màn hình (RULE-07) |
| **A.4** | Feature impact (4.3) đủ TC | ❌ **Fail** — T2 (予約管理) 0 TC thực sự quan sát được; thiếu hẳn nhánh 空き枠通知 mà Dev không liệt kê |
| **A.5** | Gap & orphan detection | ✅ Pass — 0 orphan; 12 GAP đã liệt kê ở §4 |
| **A.6** | Fix-shape adversarial check | ❌ **Fail** — shape "sửa hàm dùng chung": có danh sách Dev cung cấp (tốt) nhưng mới test 4/5 nơi; thiếu rà chức năng tương tự (Lesson/Event) |
| **B.1** | TC rõ ràng | ✅ Pass — precondition/steps/expected viết tốt, có số liệu cụ thể; ⚠️ 5 TC nhóm `api` ghi sai tên endpoint ở `screen` |
| **B.2** | TC atomic | ✅ Pass |
| **B.3** | TC độc lập | ✅ Pass |
| **B.4** | TC realistic | ✅ Pass — dùng đúng shape data của bug KH |
| **C** | Chất lượng bộ TC tổng thể | ⚠️ **Fail một phần** — RULE-01 vi phạm ở cả 4 quan điểm hợp lệ (VIEW-02); 1 nhóm DUP-INFLATE che GAP (§4.5 N1) |
| **D** | Spec alignment | ❌ **Fail** — 25/25 TC không có `Trạng thái đánh giá spec`, trong khi spec **thực sự không định nghĩa** hành vi này (S1/S2) |
| **E** | Hành chính | ❌ **Fail** — 0 evidence (RULE-02); checkbox "Tester verify auto-fill chính xác" **chưa tick** ở cả `01-bug-task.md` và `03-dev-impact.md` |
| **F** | Base quan điểm test LME | ❌ **Fail** — xem F.1 |

> **[MAJOR] INPUT-01 — Auto-fill chưa được tester verify.** Cả `01-bug-task.md` và `03-dev-impact.md` đều có `Auto-filled: 2026-08-26 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. F/D/T có thể thiếu hoặc map sai → coverage matrix ở §3 dựa trên input chưa được người xác nhận. Yêu cầu tester đọc lại Redmine #40128 (description + journal #132918 + #133038) và tick trước khi report này có giá trị nghiệm thu.

### F.1 — Bảng quan điểm đối chiếu

> `Exec` = số TC `pass` / tổng TC cover. TC mang mã Studio lạ (`TOOL-*`, `JOB-002`) **không được tính là cover** theo mục 0.6 #6.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ luồng chính đặt lịch | TC-FUNC001-01/-02/-03/-04 | 3/4 | ⚠️ **[MAJOR] RULE-01** — 4/4 đều `Normal`, thiếu Abnormal + Boundary, không ghi lý do. Thêm nữa 3/4 trùng oracle (§4.5 N1) |
| `FUNC-DATE-001` | Cao | ◯ toàn bộ fix là phép so mốc thời gian | TC-FUNCDATE001-01→-06 | 2/6 | ⚠️ **[MAJOR]** — thiếu `Normal` (RULE-01); thiếu ca qua nửa đêm (GAP-05), đơn vị slot ≠ 30' (GAP-08), nghỉ trước (GAP-06) |
| `STATE-DEP-001` | Cao | ◯ trạng thái khung phụ thuộc ca + booking | TC-STATEDEP001-01/-02 | 0/2 | ⚠️ **[MAJOR]** — cả 2 TC **chưa chạy**; thiếu `Boundary` (RULE-01) |
| `REG-SHARED-001` | Cao | ◯ **BẮT BUỘC** — sửa hàm dùng chung, đổi signature | TC-REGSHARED001-01→-07 | 4/7 | ❌ **[BLOCKER]** — thiếu `handleShowListBooking` (GAP-01), 指名あり (GAP-02); 2 TC "bất biến" false pass (EXEC-02); thiếu `Boundary` (RULE-01); chưa rà Lesson/Event (GAP-12) |
| `MSG-001` | Cao | ◯ fix đổi điều kiện quyết định ai nhận tin 「受付再開」 | *(không TC nào)* | 0/0 | ❌ **[BLOCKER] GAP-03** |
| `JOB-001` | Cao | ◯ **BẮT BUỘC** — fix chạm 2 job nền | *(3 TC mang mã lạ `JOB-002` → không tính cover)* | — | ⚠️ **[MAJOR]** — coi như chưa cover cho tới khi map lại mã (VIEW-01); ngoài ra thiếu 3 option auto-assign (GAP-10) và output cuối chuỗi (RULE-06) |
| `INTG-CAL-001` | Cao | ◯ block time Google là nguồn "bận" thứ hai của cùng phép tính | *(không TC nào)* | 0/0 | ⚠️ **[MAJOR] GAP-04** |
| `ENV-003` ★ | Cao | ◯ **BẮT BUỘC** — job nền, khác biệt local/staging/prd | *(không TC nào ở staging/prd)* | 0/0 | ⚠️ **[MAJOR] RULE-08** (EXEC-03) |
| `DEPLOY-LIVE-001` ★ | Cao | ◯ release không maintain, đổi điều kiện hợp lệ của slot | *(không TC nào)* | 0/0 | ⚠️ **[MAJOR] GAP-11** |
| `OUT-TRUTH-001` | Cao | ◯ UI slot phải khớp trạng thái thật (lưới tuần vs ngày vs admin) | *(không TC nào)* | 0/0 | ⚠️ **[MAJOR]** — gộp vào GAP-01 |
| `COMPAT-LEGACY-001` ★ | Cao | ◯ đơn cũ tạo trước fix chạy song song | *(TC-TOOLOLDREC001-01 mang mã lạ → không tính cover)* | — | ⚠️ **[MAJOR]** — map lại mã `TOOL-OLDREC-001` → `COMPAT-LEGACY-001` (VIEW-01) |
| `CONC-001` | Cao | ◯ 2 khách cùng đặt khung cuối cùng | *(không TC nào)* | 0/0 | ⚠️ **[MAJOR]** — dùng lại kho `TC-SLN-460` (bug KH #38280). Fix thu hẹp tập slot hợp lệ ⇒ tranh chấp khung cuối tăng |
| `DATA-COUNT-001` | Cao | ◯ trần chỗ = phép đếm (`isReachMaxBooking`) | TC-REGSHARED001-03/-04/-05 (gián tiếp) | 3/3 | ⚠️ RISK — chưa có TC nào **đếm tay** số khung khả dụng rồi đối chiếu số hiển thị. Dùng lại kho `TC-SLN-279`→`TC-SLN-286` |
| `REG-RUN-001` | Cao | ◯ job auto-assign / remind đang chạy dở khi release | *(không TC nào)* | 0/0 | ⚠️ **[MAJOR]** — dùng lại kho `TC-SLN-494` |
| `FUNC-002` / `FUNC-003` | Cao / TB | × | — | — | × — fix không chạm form nhập liệu. Lý do: không có trường input mới |
| `PAY-*` | Cao | × | — | — | × — fix không chạm thanh toán (`is_use_payment` không nằm trong 4 file sửa) |
| `MEDIA-*` | Cao | × | — | — | × — fix không chạm upload/media |
| `SEC-*` / `PERM-*` | Cao | × | — | — | × — fix không đổi phân quyền; không có endpoint mới |
| `DATA-MIG-001` | Cao | × | — | — | × — Dev khai không migrate, không đổi schema (mục 4.2 = "Không có"), mục 5 = "Không cần recover data" |
| `DEPLOY-ASSET-001` ★ | Cao | × | — | — | × — 4 file sửa đều là PHP backend, không chạm JS/CSS/asset |

**Tổng kết quan điểm:** 14 quan điểm ◯ · **2 chưa cover hoàn toàn** (`MSG-001`, `INTG-CAL-001`) + 3 chỉ cover bởi mã lạ (`JOB-001`, `COMPAT-LEGACY-001`, và `TOOL-KNOW-002` của TC bug gốc) · 4 quan điểm ◯ khác chưa có TC nào (`ENV-003`, `DEPLOY-LIVE-001`, `OUT-TRUTH-001`, `CONC-001`, `REG-RUN-001`) · **RULE-01 vi phạm ở 4/4 quan điểm hợp lệ**.

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Trạng thái |
|---|---|---|---|
| Reviewer (draft) | `/review-tc` | 2026-08-26 | 🔴 REJECTED — 5 BLOCKER |
| Test Leader verify | | | ⬜ chưa |
| Member nhận feedback | `cucdtk` | | ⬜ chưa |

### Thứ tự xử lý đề nghị

1. **Chạy 10 TC chưa chạy** — ưu tiên tuyệt đối `TC-REGSHARED001-07` (cấu hình bug thật) và `TC-FUNCDATE001-06` (partial break = 30).
2. **Đổi TC-REGSHARED001-03 / -04 về `Chưa test`** trên Studio, dựng 2 nhánh rồi chạy lại thật (EXEC-02).
3. **Hỏi Dev 4 câu** ở §6: S4 (nghỉ trước), S5 (空き枠通知), S6 (指名あり), S7 (Lesson/Event) — 3 trong 4 câu này quyết định 2 BLOCKER.
4. **Chạy lại toàn bộ trên staging** + nhóm job smoke production (RULE-08).
5. Bổ sung 15 TC ở §5 + dùng lại 4 TC kho.
6. Map lại 6 mã quan điểm lạ (VIEW-01), bổ sung `Trạng thái đánh giá spec` (VIEW-03), đính evidence (EXEC-05).
7. Gộp TC-FUNC001-03 vào TC-STATEDEP001-01 (§4.5 N1) + bổ sung loại case còn thiếu (RULE-01).
