# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; vòng review nằm ở tên file.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task #184** |
| Vì sao không dùng nguồn ưu tiên cao hơn | N.A. — đã lấy được TC ở nguồn 1 |
| Ticket · task_id · round · branch | `33222` · `#184` · round 1 · `ai_fixbug_33222` |
| Thời điểm fetch | `2026-09-04` |
| Tổng số TC review | **11** (Studio `totalMatched=11`, tất cả `status = draft`) |
| Snapshot đã ghi | **không ghi đè** — `04-tc-list.md` đã có header `<!-- source: MCP LME TEST STUDIO — task_id=184 ... 2026-09-03 -->` và nội dung khớp đúng bản fetch hôm nay (11 TC, `updated_at` 2026-09-03 09:07–09:08). Không có delta ở bảng TC → giữ nguyên file. |
| Đối chiếu chéo nguồn | **KHÔNG** — đã dừng ở nguồn 1 |
| Tester được review | AI pipeline (Studio job `549`) — 10 TC · `quyend@mcp` — 1 TC (`NEW-12`) |
| Vòng review | Round 1 · `reviewState = leader` · `reviewed = false` |
| **Nguồn spec đã dùng** | [spec-features/admin/salon-booking/feature-spec.md](../../spec-features/admin/salon-booking/feature-spec.md) (§2.3 tab コース・スタッフ, §2.6 flow LINE user, BR-10) + [db/db-mapping.md](../../spec-features/admin/salon-booking/db/db-mapping.md) (`calendar_salon_staff`) + [web/logic-spec.md](../../spec-features/admin/salon-booking/web/logic-spec.md) (cột `filter_id` / `filter_number` / `is_all_course` / `course_ids`). ⚠️ **Spec KHÔNG mô tả màn preview và KHÔNG mô tả filter bạn bè gắn cho staff/course** → xem `[MAJOR-14]` + §6. |

### Cảnh báo bắt buộc về chất lượng nguồn (mục 0.6)

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | 10/11 `pass` (90.9%), 1 chưa chạy. **Nhưng cả 10 pass đến từ run `#435` ngày 2026-08-24** — 11 ngày trước, và trước cả khi steps tái hiện được bổ sung (2026-09-03). Run hoàn tất **gần nhất** là `#821` (2026-09-03 13:24→13:33) = **`error`**, 0 kết quả. Run `#838` (2026-09-04 02:03) đang **`running`**. | `[MAJOR-1]` |
| 2 | TC `fail`/`error` · TC gắn ticket bug | 0 `fail`. `bug_tickets` rỗng ở cả 11 TC. TC chưa chạy: `NEW-12` (#15561) — đúng là TC regression `use_course=0` do reviewer thêm. **Ngoài ra**: run `#435` ghi `counts.pass = 12` nhưng chỉ còn **10** kết quả gắn được TC; dải id 12285–12295 khuyết `12290` (`NEW-6`) → **2 TC đã bị xóa khỏi task sau khi đã chạy pass**, không còn vết. | `[MAJOR-5]` |
| 3 | Môi trường đã chạy | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 11** (`envAuto`: local runs=3, còn lại runs=0). | `[BLOCKER-3]` RULE-08 / ENV-003 |
| 4 | Ai chạy | 10/10 kết quả có `source = ai`, `by = pipeline`. `task_get_report.manual.totals` = **toàn 0** → **không TC nào do QA người chạy**. `submittedWithoutMcp = false` (OK). | `[MAJOR-2]` |
| 5 | Tác giả TC | 10/11 `author = AI`, `provenance.source = ai`, `createdJobId = 549`. 1 TC `provenance.source = human` (`quyend@mcp`). = **90.9% do AI sinh**, `reviewState` chưa `done`. | `[MAJOR-3]` |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **2 mã / 3 lượt TC**: `TOOL-NEGCTRL-001` (`NEW-3`), `TOOL-KNOW-002` (`NEW-5`, `NEW-9`). → **không tính là cover** ở §3.6. | `[MAJOR-4]` |

**Bảng đối chiếu định danh** (dùng suốt report):

| Studio id | temp_id | TC No. (file 04) | Tóm tắt |
|---|---|---|---|
| 12285 | NEW-1 | `TC-FUNC001-01` | Preview: staff CÓ filter bạn bè vẫn hiện |
| 12286 | NEW-2 | `TC-FUNC001-02` | Preview: staff KHÔNG filter vẫn hiện (đối chứng) |
| 12287 | NEW-3 | `TC-TOOLNEGCTRL001-01` | Preview: staff không phụ trách khóa KHÔNG hiện |
| 12288 | NEW-4 | `TC-UI003-01` | Preview: khóa chưa gán staff → list trống |
| 12289 | NEW-5 | `TC-TOOLKNOW002-01` | Preview: lịch **tuần** có slot cho staff có filter |
| 12291 | NEW-7 | `TC-OUTPREVIEW001-01` | Preview: lịch **tháng** — đối chiếu với friend |
| 12292 | NEW-8 | `TC-FUNCSEQ001-01` | Preview: chuyển tháng → slot cập nhật |
| 12293 | NEW-9 | `TC-TOOLKNOW002-02` | Đối chiếu preview ⇔ friend (staff + slot tuần) |
| 12294 | NEW-10 | `TC-REGSHARED001-01` | Regression friend F-OK: staff hiện + có slot |
| 12295 | NEW-11 | `TC-FRIEND001-01` | Regression friend F-NG: staff bị ẩn |
| 15561 | NEW-12 | `TC-REGSHARED001-02` | Preview `use_course=0` — **chưa chạy** |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có 4 `[BLOCKER]`, cần fix và review lại

**Lý do ngắn gọn**: bộ TC bám khá sát 2 nhánh code đã sửa và có đối chứng âm/dương tốt, nhưng (a) hàm dùng chung `getListStaffCanBook` còn **3/5 call site chưa có TC nào** trong khi đây chính là rủi ro Dev tự nêu; (b) **100% TC chỉ chạy trên `local`**, chưa từng chạm staging/production; (c) steps tái hiện được bổ sung **sau** khi TC đã sinh mà chưa ai rà lại; (d) cách ly đa bot (`BR-18`) bị chính coverage report của Studio đánh dấu `level = none`.

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần khó nhất: có **đối chứng âm** (`NEW-11` friend không thỏa filter vẫn bị ẩn staff) và **đối chứng dương** (`NEW-2`, `NEW-10`) — đây đúng là thứ chặn được rủi ro lớn nhất của fix này là "nới lỏng nhầm luồng đặt lịch thật". `NEW-12` bổ sung nhánh `use_course=0` cũng rất đúng hướng.

Ba điểm phải xử lý trước khi merge: **(1)** fix sửa hàm dùng chung có 5 nơi gọi, TC mới chạm 2 — cần Dev đưa tên cụ thể của "2 job gán nhân viên" + `getTotalListTimeBookingQ` rồi test từng nơi; **(2)** toàn bộ kết quả pass đang là bản chụp ngày 24/08 trên `local`, còn lần chạy lại gần nhất thì **lỗi** — chưa được coi là "đã test xong"; **(3)** ticket này có **2 bug**, nhưng Bug 2 (staff không phụ trách khóa vẫn hiện) mới chỉ có đúng 1 TC và còn hở nhánh `is_all_course = 1`, staff bị tắt hiển thị, và bước chọn **khóa** ở preview.

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG-1** — preview không hiện lịch làm việc (staff có filter bạn bè) | Bug | NEW-1, NEW-5, NEW-7, NEW-9 | 4 | 4/4 pass (local, 24/08) | **RISK** — không TC nào dựng đúng dữ liệu gốc KH báo ("các ngày từ 19/12"); `NEW-9` tự ghi chú phải dùng đúng dataset gốc nhưng run thực tế chạy tháng 2026-08 |
| **BUG-2** — preview hiện staff không phụ trách khóa | Bug | NEW-3 | 1 | 1/1 pass | **RISK** — 1 TC duy nhất, mang mã `TOOL-NEGCTRL-001` (không phải quan điểm hợp lệ); hở `is_all_course=1`, `course_ids` rỗng, và bước chọn khóa |
| **F1** `getListStaffCanBook($isPreview)` | Function · Direct | NEW-5, NEW-7, NEW-11, NEW-12 | 4 | 3/4 (NEW-12 chưa chạy) | **RISK** |
| **F2** `getListStaffByCalendar` (AJAX) | Function · Direct | NEW-1, NEW-2, NEW-3, NEW-4, NEW-12 | 5 | 4/5 | **RISK** — thiếu `booking_page_display = 0`, `is_all_course = 1`, 指定なし |
| **F3** `getListTimeBooking` → lịch tuần | Function · Direct | NEW-5, NEW-9, NEW-10 | 3 | 3/3 | **RISK** — toàn Normal, không Abnormal/Boundary |
| **F4** `showTimeBookingMonth` → lịch tháng | Function · Direct | NEW-7, NEW-8 | 2 | 2/2 | **RISK** — **0 TC chạy nhánh `isPreview=false`** (friend thật) của chính hàm vừa sửa |
| **F5** `isValidFilter` | Function · Indirect | NEW-10, NEW-11 | 2 | 2/2 | **RISK** — chỉ local; chỉ 1 loại filter, không phân biệt type friend info |
| **F6** 4 call site khác: đặt lịch thật · **2 job gán nhân viên** · `getTotalListTimeBookingQ` | Function · Indirect | NEW-10, NEW-11 (chỉ nhánh "đặt lịch thật") | 2/5 nơi | 2/2 | **GAP** — 3/5 call site **0 TC** |
| **F7** `Conversation::advanceFilterPost` (**KHÔNG sửa**) | Function · Indirect | — | 0 | — | **GAP có chủ ý** — code không bị chạm ⇒ không có rủi ro hồi quy từ fix này, **không đề xuất TC**; nhưng là vấn đề phạm vi → §6 |
| **D** — data | Data | Dev ghi "Không có" | — | — | N/A — fix thuần read-path, không UPDATE/DELETE. Leader verify. |
| **T1** Preview trang đặt lịch salon | Feature | NEW-1…NEW-9, NEW-12 | 9 | 8/9 | **RISK** — thiếu bước chọn **khóa** ở preview, 指定なし, staff OFF |
| **T2** Luồng đặt lịch salon **thật của friend** (LIFF) | Feature | NEW-9, NEW-10, NEW-11 | 3 | 3/3 | **RISK** — thiếu **lịch tháng phía friend** (đúng vùng bug lịch sử `TC-SLN-443`); precondition toàn data sạch |
| **T3** 2 job gán nhân viên dùng chung `getListStaffCanBook` | Feature | — | 0 | — | **GAP** |

### ORPHAN TCs

**Không có.** Cả 11 TC đều trace được về code path đã sửa (kiểm theo AP-5). `NEW-2` tuy là case đối chứng "không đổi hành vi" nhưng hợp lệ — nó phân lập tác động của nhánh filter.

⚠️ Ngược lại có **2 TC biến mất**: run `#435` đếm `pass = 12`, hiện chỉ 10 kết quả gắn TC, khuyết Studio id `12290` (`NEW-6`). Đã pass rồi bị xóa khỏi task → không biết chúng cover gì. Xem `[MAJOR-5]`.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape 1 — "sửa hàm dùng chung"** (`getListStaffCanBook` thêm param `$isPreview`, mục 2 ghi rõ *"các chỗ chấm điều kiện lọc còn lại nằm ở luồng đặt lịch thật và job gán nhân viên"*).

| Câu hỏi adversarial | Trả lời từ bộ TC hiện tại | Kết luận |
|---|---|---|
| Có **danh sách nơi ảnh hưởng do DEV cung cấp** không? | Có mô tả ("4 call site khác: đặt lịch thật, 2 job gán nhân viên, `getTotalListTimeBookingQ`") nhưng **không có tên file / tên job** — chính điểm nghi vấn #3 của `03-dev-impact.md`. | **`[BLOCKER-1]`** |
| TC test **từng nơi** trong danh sách? | 2/5 (chỉ nhánh "đặt lịch thật" qua `NEW-10`/`NEW-11`). 2 job + `getTotalListTimeBookingQ` = **0 TC**. | **`[BLOCKER-1]`** |
| Chức năng **tương tự** (Salon ⇄ Lesson ⇄ Booking Event) đã rà? | Không TC nào. Cả 3 tính năng đều có màn preview và đều có cơ chế filter bạn bè. | `[MAJOR-8b]` |

**Fix shape 2 — "thêm cờ / thêm điều kiện"** (`$isPreview = false`; nhánh `if (!in_array($courseId, $courseIds)) continue`).

| Câu hỏi adversarial | Trả lời | Kết luận |
|---|---|---|
| Đủ 5 pattern biên? | Chỉ có `NEW-4` (khóa chưa gán staff). **Thiếu**: `is_all_course = 1` (staff nhận tất cả khóa — nhánh `in_array` phải bị bỏ qua), `course_ids` rỗng, staff `booking_page_display = 0`, 指定なし. | `[MAJOR-7]` |
| Test **server-side** (gọi thẳng API) hay chỉ qua UI? | 11/11 đi qua UI preview. **0 TC gọi thẳng** `GET /ajax/mobile/calendar-salon/get-list-staff-by-calendar` với `line_id='preview'` và `calendar_salon_id` của **bot khác**. | **`[BLOCKER-4]`** |
| Đủ luồng vào (create/edit/copy/CSV/API)? | N/A — fix là read-path. | × có lý do |

**Symptom-only KH report check** — `01-bug-task.md` mục "Mô tả bug" nguyên văn: *"Preview: đang ko hiển thị lịch lv các ngày từ 19/12 / Friend: hiển thị được lịch lv"*. **Không có error message / error code / log.** Dev tái hiện đúng 1 root cause (`!empty([null])` ⇒ `isValidFilter` luôn false). → **`[MAJOR-6]`**: cần cover ≥ 2 plausible root cause. Ứng viên hợp lý khác cùng cho ra "preview trống lịch mà friend thì có": **(a)** filter gắn ở **course** (`calendar_salon_course.filter_id` — cột này tồn tại theo `web/logic-spec.md:246`) chứ không phải ở staff; **(b)** 受付上限 / 予約の開始・締切 chặn khoảng ngày đó; **(c)** ca làm việc của tuần 19/12 không tồn tại. TC hiện tại chỉ cover root cause (staff filter).

**REG-SPEC-001 — spec đổi sau khi có TC**: steps tái hiện (journal #133918) được bổ sung **2026-09-03**; 10/11 TC sinh **2026-08-24 08:35**. Nghĩa là bộ TC được viết khi **chưa có** steps tái hiện — và chính steps mới này là nơi Bug 2 được mô tả tường minh lần đầu. Chưa có bằng chứng ai rà lại 11 TC theo spec mới. → **`[BLOCKER-2]`**.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| AP-1 Single-trigger generic-fix | Không | Fix không phải generic catch |
| **AP-2 Symptom-only KH report** | **Dính** | → `[MAJOR-6]` |
| **AP-3 Happy-path-only regression** | **Dính** | `T3` = 0 TC; `T2` có 3 TC nhưng precondition toàn data sạch (không có staff OFF / khóa rỗng / friend bị block) → `[MAJOR-15]` |
| **AP-4 Fix shape không verify được** | **Dính** | `03-dev-impact.md` ghi *"không có link PR trong Redmine"* → không đọc được diff để xác nhận fix shape thực tế → `[MAJOR-9]` |
| AP-5 Layer-downstream over-coverage | Không | 11/11 TC đều chạm code path đã sửa |
| AP-6 Mục 3 dev-impact trống | **Dính một phần** | Mục 3 có bảng 8 dòng nhưng **không phân biệt "đã SỬA" và "chỉ CHECK"** (file 03 tự ghi chú), và F6 không định danh được → gộp vào `[BLOCKER-1]` |

---

## 3.6 Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp? | TC cover (hợp lệ) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ luôn bắt buộc | NEW-1 (N), NEW-2 (N) | 2/2 | **RISK** — 2 TC đều `Normal`, thiếu Abnormal + Boundary → `[MAJOR] RULE-01` |
| `OUT-PREVIEW-001` | **Cao** | ◯ **BẮT BUỘC** — có chế độ preview | NEW-7 (N) | 1/1 | **RISK** — quan điểm Cao chỉ 1 TC `Normal` → `[MAJOR] RULE-01`. (NEW-9 làm đúng phần "so preview vs thật" nhưng mang mã `TOOL-KNOW-002` → không tính) |
| `REG-SHARED-001` | **Cao** | ◯ **BẮT BUỘC** — sửa hàm dùng chung | NEW-10 (N), NEW-12 (N, **chưa chạy**) | 1/2 | **GAP thực chất → `[BLOCKER-1]`** — thiếu danh sách nơi ảnh hưởng; 3/5 call site 0 TC; chưa rà Lesson/Event |
| `FRIEND-001` | **Cao** | ◯ **BẮT BUỘC** — friend info dùng làm **điều kiện lọc** | NEW-11 (A) | 1/1 | **RISK → `[MAJOR] RULE-01`** — chỉ 1 `Abnormal`; quan điểm đòi test theo **từng type** friend info (text/point/select/date/…), TC chỉ nói "filter" chung |
| `REG-SPEC-001` | **Cao** | ◯ **BẮT BUỘC** — steps tái hiện bổ sung 03/09 sau khi TC sinh 24/08 | — | — | **GAP → `[BLOCKER-2]`** |
| `ENV-003` | **Cao** | ◯ **BẮT BUỘC** — chạm job nền (2 job gán NV) + trang LIFF | — (11/11 chỉ `local`) | 0 ngoài local | **GAP → `[BLOCKER-3]`** |
| `PERM-003` | **Cao** | ◯ **BẮT BUỘC** — multi-bot; Studio coverage tự đánh `BR-18 … level=none, tcIds=[]` | — | — | **GAP → `[BLOCKER-4]`** |
| `UI-003` | TB → **Cao** (rủi ro false success) | ◯ màn danh sách + AJAX; preview trả list rỗng **trông giống** kết quả đúng | NEW-4 (B) | 1/1 | **RISK** — chỉ có trạng thái **rỗng**; thiếu loading / lỗi mạng → `[MAJOR]` |
| `FUNC-SEQ-001` | Trung bình | ◯ ≥2 thao tác trên cùng danh sách (đổi khóa → đổi staff → đổi tháng) | NEW-8 (N) | 1/1 | **RISK** — chỉ chuỗi "chuyển tháng"; thiếu đổi khóa → đổi staff → F5 |
| `CONC-003` | TB → **Cao** (nhiều request cùng màn) | ◯ chuyển nhanh tuần/tháng/đổi staff khi AJAX chưa trả | — | — | **GAP → `[MAJOR-17]`** — kho đã có `TC-SLN-465`, dùng lại (§5) |
| `LIST-001` | Trung bình | ◯ danh sách staff/course có filter | NEW-4 (một phần) | 1/1 | **RISK** |
| `DATA-DB-001` | Cao | **×** | — | — | Fix thuần **read-path**, 4.2 = "Không có" (Leader verify). Ghi lý do theo RULE-03. |
| `LIFF-ENTRY-001` | Cao | **×** | — | — | Fix **không chạm** URL/entry — chỉ đổi nội dung danh sách bên trong trang. Regression URL đã có `TC-SLN-495` ở kho. |
| `COMPAT-LEGACY-001` | Cao | **×** | — | — | Không version-up đối tượng nào |
| `DEPLOY-ASSET-001` | Cao | **×** | — | — | Chỉ sửa 2 file PHP, không sửa JS/CSS/asset |
| `MSG-*` · `PAY-*` · `DATA-COUNT-001` · `MEDIA-*` | — | **×** | — | — | Fix không gửi tin / không tính tiền / không thêm số đếm / không chạm media |

**Quan điểm ưu tiên Cao đang thiếu TC**: `REG-SPEC-001`, `ENV-003`, `PERM-003` (0 TC) · `REG-SHARED-001` (có TC nhưng không phủ 3/5 call site).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **`[BLOCKER-1]` FIX-SHAPE / `REG-SHARED-001` — GAP-1: hàm dùng chung chưa được rà đủ nơi gọi.** `getListStaffCanBook` có 5 call site; Dev chỉ mô tả 3 nơi còn lại bằng lời ("2 job gán nhân viên", "`getTotalListTimeBookingQ`") **không kèm tên file/tên job**, và **0 TC** chạm chúng. Đây đúng là rủi ro Dev tự viết ra: *"nếu một call site nào đó vô tình truyền true, filter bạn bè sẽ bị bỏ qua ở luồng đặt lịch thật"*. — **Fix**: yêu cầu Dev đưa danh sách chính xác (tên class::method + tên job + file), sau đó chạy `TC-REGSHARED001-03` và `TC-REGSHARED001-04` (§5). Kèm rà chức năng tương tự Lesson / Booking Event.
- **`[BLOCKER-2]` `REG-SPEC-001` — GAP-2: spec thay đổi sau khi TC đã sinh, chưa ai rà lại.** Steps tái hiện (journal #133918) bổ sung **2026-09-03**; 10/11 TC sinh **2026-08-24 08:35**. Bug 2 chỉ được mô tả tường minh trong steps mới, mà Bug 2 hiện chỉ có 1 TC. — **Fix**: rà **từng** TC trong 11 TC, gán 1 trong 4 trạng thái `[Giữ nguyên]` / `[Cần sửa]` / `[Cần thêm mới]` / `[Hết hiệu lực]` kèm lý do; case `[Hết hiệu lực]` đánh dấu, **không xóa**. Rà lại cả cột "Áp dụng?" của quan điểm — steps mới có thể kích hoạt quan điểm chưa chọn. Đây **không sinh TC mới**, là hành động rà soát.
- **`[BLOCKER-3]` `ENV-003` / RULE-08 — GAP-3: 100% TC chỉ chạy `local`.** Studio `envAuto`: `local` runs=3 · `dev` 0 · `staging` 0 · `prd` 0. Task chạm **job nền** (2 job gán nhân viên dùng chung hàm vừa sửa) và trang đặt lịch phát hành cho LINE user. KH báo bug trên môi trường thật, không phải local. Không được kết luận "đã test xong" từ local. — **Fix**: chạy `TC-ENV003-01` (§5) — tối thiểu bộ BUG-1 + BUG-2 + 2 TC regression friend trên **staging** và **production**.
- **`[BLOCKER-4]` `PERM-003` / BR-18 — GAP-4: cách ly đa bot ở endpoint preview chưa có TC nào.** Chính `task_get_report.coverage` của Studio đánh dấu `BR-18 "Multi-tenant isolation, mọi query filter bot_id — cần verify preview vẫn filter đúng bot_id"` với `tcIds: []`, `level: "none"`. Endpoint `get-list-staff-by-calendar` nhận `calendar_salon_id` từ request và ở chế độ preview **đã bỏ bớt một tầng lọc** → phải chứng minh tầng `bot_id` vẫn còn. — **Fix**: `TC-PERM003-01` (§5).

### 4.2 Major (nên fix)

- **`[MAJOR-1]` Kết quả `pass` hiện tại không còn hiệu lực.** 10 pass đều thuộc run `#435` (2026-08-24), trong khi run hoàn tất gần nhất `#821` (2026-09-03) = **`error`** và run `#838` (2026-09-04) đang chạy dở. — **Fix**: chờ `#838` xong hoặc chạy lại; nếu `#821` lỗi do hạ tầng thì ghi rõ nguyên nhân vào task, đừng để trạng thái "10/11 pass" đứng một mình.
- **`[MAJOR-2]` Không TC nào do QA người chạy.** `manual.totals` toàn 0; 10/10 kết quả `source = ai`, `by = pipeline`. Nhóm rủi ro cao nhất — `NEW-11` (friend không thỏa filter **phải** bị ẩn staff) — hiện chỉ có AI tự chạy tự chấm. — **Fix**: QA chạy tay tối thiểu `NEW-3`, `NEW-9`, `NEW-11` và đính evidence.
- **`[MAJOR-3]` 90.9% TC do AI sinh, chưa qua review.** `reviewState = leader`, `reviewed = false`, cả **11/11 TC `status = draft`**. — **Fix**: Leader chốt trạng thái TC trên Studio sau khi xử lý report này.
- **`[MAJOR-4]` 3 lượt TC dùng mã quan điểm nội bộ Studio.** `NEW-3` = `TOOL-NEGCTRL-001`, `NEW-5`/`NEW-9` = `TOOL-KNOW-002` — không có trong `framework/checklist-lme.md` nên **không tính là cover**. Hệ quả nặng nhất: **Bug 2 mất mã quan điểm map coverage** (chỉ `NEW-3` cover Bug 2). — **Fix**: `testcase_update` gán lại — `NEW-3` → `FUNC-001` (Abnormal), `NEW-5` → `OUT-PREVIEW-001`, `NEW-9` → `OUT-PREVIEW-001`. Kéo theo `TC No.` ở file 04 đổi tương ứng.
- **`[MAJOR-5]` 2 TC bị xóa khỏi task sau khi đã chạy pass.** Run `#435` ghi `counts.pass = 12`, hiện chỉ 10 kết quả gắn TC; khuyết Studio id `12290` (`NEW-6`). Không rõ 2 TC đó cover gì và vì sao bị xóa → có thể đã mất coverage mà matrix không phát hiện. — **Fix**: `testcase_get_history` / `task_get_history` để truy lại nội dung 2 TC bị xóa, xác nhận không mất chiều nào.
- **`[MAJOR-6]` `[AP-2]` SYMPTOM-ONLY: KH chỉ báo triệu chứng, TC chỉ cover 1 root cause.** Xem §3.5. — **Fix**: hỏi Dev về alternative root cause, trước mắt bổ sung `TC-FUNC001-03` (filter ở **course**, §5).
- **`[MAJOR-7]` Bug 2 thiếu biên `is_all_course = 1` và `course_ids` rỗng.** Theo `db/db-mapping.md:209`, `is_all_course = 1` nghĩa là "nhận **tất cả** khóa học". Nhánh mới `if (!in_array($courseId, $courseIds)) continue` phải **bị bỏ qua** với staff này, nếu không staff nhận-mọi-khóa sẽ **biến mất** khỏi preview — tức fix Bug 2 lại đẻ ra bug mới cùng lớp với Bug 1. **0 TC** cover. — **Fix**: `TC-FUNC001-05` (§5).
- **`[MAJOR-8]` Bước chọn khóa ở preview chưa có TC** (điểm nghi vấn #5 của `03-dev-impact.md` chưa được trả lời). `getListCourseByCalendar` cũng có nhánh "bỏ lọc khi `lineId='preview'`" và `calendar_salon_course` cũng có `booking_page_display` + `filter_id` (`web/logic-spec.md:246`) → **cùng lớp lỗi với Bug 2**, chỉ khác là ở bước trước. Nếu preview vẫn hiện course đã tắt/bị filter thì khiếu nại gốc "preview hiển thị khác với bên friend" **chưa được fix trọn**. — **Fix**: `TC-FUNC001-03` (§5).
- **`[MAJOR-8b]` Chưa rà chức năng tương tự.** `REG-SHARED-001` nêu đích danh cặp **Salon / Lesson / Booking Event**; cả 3 đều có preview và cơ chế filter bạn bè. 0 TC. — **Fix**: hỏi Dev 2 tính năng kia có cùng pattern `lineId='preview'` không; có thì mở ticket riêng (không nhét vào ticket này).
- **`[MAJOR-9]` `[AP-4]` Không có link PR** (`03-dev-impact.md`: *"không có link PR trong Redmine"*) → không thể đọc diff để xác nhận fix shape thực tế đúng như mô tả. — **Fix**: yêu cầu Dev cung cấp link PR / diff của commit `bcc9733e24`.
- **`[MAJOR-10]` Staff bị tắt hiển thị (`booking_page_display = 0`) ở preview chưa có TC.** Trước fix, preview *"bỏ qua toàn bộ việc lọc"*; fix mới chỉ khôi phục lọc **theo khóa**. Câu hỏi chưa ai trả lời: preview có còn hiện staff đã tắt không? Kho có `TC-SLN-432` chứng minh phía LINE user staff OFF **không** hiện → preview phải khớp. — **Fix**: `TC-FUNC001-04` (§5).
- **`[MAJOR-11]` 指定なし (không chỉ định nhân viên) ở preview chưa có TC.** Đây là đường **gộp slot của tất cả staff**; trước fix mọi staff có filter đều bị loại ⇒ slot 指定なし ở preview sai. Sau fix phải bằng hợp của các staff. Kho có `TC-SLN-257` cho phía LINE user. — **Fix**: `TC-OUTPREVIEW001-02` (§5).
- **`[MAJOR-12]` Lịch tháng phía friend thật chưa có TC** — `showTimeBookingMonth` là hàm **bị sửa** (F4), nhưng cả `NEW-10` lẫn `NEW-11` chỉ xem **lịch tuần**. Kho có sẵn bug lịch sử đúng vùng này: `TC-SLN-443` *"Bug: màn tháng không hiển thị khi có filter staff"* (Bug tự detect 9/2025). — **Fix**: dùng lại `TC-SLN-443` (§5).
- **`[MAJOR-13]` `FRIEND-001` RULE-01 + thiếu chiều type.** Chỉ 1 TC `Abnormal`; quan điểm yêu cầu chạy filter theo **từng type friend info** (text / point / select / date / …). — **Fix**: `TC-FRIEND001-02` (§5).
- **`[MAJOR-14]` Không có spec cho hành vi preview → không có chuẩn chấm Expected.** `spec-features/admin/salon-booking/` **không có một dòng nào** về màn preview, cũng không mô tả filter bạn bè gắn cho staff/course. Toàn bộ fix đứng trên giả định *"preview xem như bạn bè thỏa điều kiện"* mà AI **tự suy từ code hiện hữu** (nguyên văn mục 6 VERIFY). Kèm theo: **11/11 TC có `spec_status = null`** → không TC nào ghi "Trạng thái đánh giá spec". — **Fix**: chốt giả định với BA/Leader rồi ghi vào spec (§6); mỗi TC điền `spec_status`.
- **`[MAJOR-15]` `[AP-3]` Regression `T2`/`T3` chỉ chạy trên data sạch.** `T3` = 0 TC; `T2` = 3 TC, precondition đều là friend/staff/khóa ở trạng thái chuẩn. Không có TC nào chạy regression với edge state (staff OFF, khóa rỗng, friend bị block, ca làm việc trống).
- **`[MAJOR-16]` `NEW-1` có Expected không phân biệt được trước/sau fix.** Nguyên văn: *"NV-A PHẢI xuất hiện… **Trước fix NV-A vẫn hiện** nhưng do bỏ MỌI lọc; sau fix vẫn hiện đúng vì thuộc khóa K1."* → cùng một quan sát ("NV-A hiện") đúng cho **cả hai** phía của fix ⇒ TC này **không chứng minh được fix đã áp dụng**. — **Fix**: gộp điều kiện phân biệt vào Expected (VD: cùng lúc phải có 1 staff không phụ trách K1 **không** xuất hiện), hoặc tách phần đối chứng sang `NEW-3` và ghi rõ 2 TC phải chạy cặp.
- **`[MAJOR-17]` `CONC-003` — chuyển nhanh view khi AJAX chưa trả.** Preview gọi 3 endpoint rời (staff / tuần / tháng); đổi khóa → đổi staff → đổi tháng liên tục có thể render kết quả của request cũ. 0 TC. — **Fix**: dùng lại `TC-SLN-465` (§5).
- **`[MAJOR-18]` Evidence rỗng — RULE-02.** Cả 10 kết quả run `#435` đều có `artifacts: []`; `actual` chỉ là dòng text do runner tự sinh. `OUT-PREVIEW-001` yêu cầu **cặp screenshot preview vs thật**; `FRIEND-001` yêu cầu screenshot count/detail/LINE app. — **Fix**: đính screenshot cho tối thiểu `NEW-7`, `NEW-9`, `NEW-11`.
- **`[MAJOR-19]` SPEC-CONFLICT: hai loại filter mang nghĩa ngược nhau, chưa ai chốt preview theo bên nào.** Fix đặt nguyên tắc *"preview = coi như bạn bè **thỏa** điều kiện"*. Nhưng filter cấp calendar 「予約ページの非表示」 có **ngữ nghĩa đảo**: theo `TC-SLN-350` (kho FA-020), khách **THỎA MÃN** filter thì **bị chặn** trang đặt lịch. Áp cùng nguyên tắc ⇒ preview sẽ tự chặn chính nó. Không có TC nào và không có spec nào nói preview xử lý filter 「予約ページの非表示」 ra sao. — **Không tự chọn bên**; đẩy lên Dev/Leader → §6.
- **`[MAJOR-20]` 2 checkbox "Tester verify auto-fill chính xác" chưa tick** ở cả `01-bug-task.md` và `03-dev-impact.md`. Bảng `F1`–`F7` và `T2`/`T3` là do `/new-task` **suy ra**, chưa Dev/tester confirm → coverage matrix ở §3 đang đứng trên input chưa được xác nhận.

### 4.3 Minor (có thể fix sau)

- **`[MINOR-1]`** `TC No.` ở `04-tc-list.md` sinh từ mã quan điểm không hợp lệ: `TC-TOOLKNOW002-01`, `TC-TOOLKNOW002-02`, `TC-TOOLNEGCTRL001-01`. Sẽ tự hết khi xử lý `[MAJOR-4]`.
- **`[MINOR-2]`** `NEW-9` ghi chú *"ticket ghi hiện tượng từ 19/12; không thay bằng khoảng thời gian ngẫu nhiên"* nhưng run thực tế chạy tháng `2026-08` — TC tự mâu thuẫn với ghi chú của chính nó.
- **`[MINOR-3]`** `NEW-8` — `actual` của run ghi *"fixture ca làm đều nhau nên cả 2 tháng đều có slot"*, tức TC **không thực sự** kiểm được "slot đổi theo tháng". Precondition yêu cầu "ca làm khác nhau ở 2 tháng" nhưng fixture không đáp ứng → kết quả `pass` là giả.
- **`[MINOR-4]`** `exec_mode = auto` ở cả 11 TC nhưng nhiều TC bản chất là quan sát UI (`NEW-4` trạng thái rỗng, `NEW-7` so sánh 2 màn) — nên tách `manual` để QA chạy tay được.

### 4.4 Nit (gợi ý)

- **`[NIT-1]`** `Conversation::advanceFilterPost` (`!empty([null]) === true`) là root cause thật nhưng được **bypass ở tầng trên** thay vì sửa. Vì file đó **không bị chạm code**, các caller khác **không** phát sinh hồi quy từ fix này → **không đề xuất TC regression cho chúng**. Tuy vậy cùng một lỗi sẽ tái diễn ở bất kỳ luồng nào truyền `lineUserId` rỗng → §6.
- **`[NIT-2]`** `04-tc-list.md` dòng 1 vẫn là `<!-- sync-tcs: url=<chưa có Sheet TC human cho ticket này> ... -->` — nếu không định push sang Sheet thì bỏ dòng config cho gọn.
- **`[NIT-3]`** Theo RULE-11, các mục §4 của `checklist-lme.md` (FORM-01/CHAT-01/ADM-*/TPL-01) **không** được dùng để flag ở report này — đã tuân thủ, ghi lại để Leader khỏi hỏi.

---

## 4.5 TC trùng lặp nội dung

**Đã rà đủ 11/11 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Friend F-OK xem staff + slot tuần | `NEW-9` (`TC-TOOLKNOW002-02`) | **`NEW-10`** (`TC-REGSHARED001-01`) — **đề nghị GỘP, KHÔNG xóa** | `DUP-SUBSET` | Cùng `Normal`; cùng đối tượng+thao tác *"mở lịch salon bằng `line_id` = F-OK, chọn K1 + NV-A, xem danh sách staff và slot tuần"*; cùng tiền đề *"F-OK thỏa toàn bộ filter của NV-A"*. Bước 3–5 của `NEW-9` lặp lại nguyên vẹn toàn bộ `NEW-10`. | `[MINOR]` |

**Gate trước khi đề nghị xóa** — giả định xóa `NEW-10` rồi chạy lại §3 + §3.6: `REG-SHARED-001` (Cao) sẽ chỉ còn `NEW-12` — mà `NEW-12` **chưa chạy** ⇒ quan điểm ưu tiên Cao mất toàn bộ TC đã thực thi; `F5` chỉ còn `NEW-11` (`Abnormal`), mất chiều `Normal`. → **Mất cover ⇒ đổi từ "xóa" sang "gộp"**: giữ cả 2, nhưng cho `NEW-9` **dẫn chiếu kết quả của `NEW-10`** ở bước 3–5 thay vì dựng lại friend F-OK lần hai, và ghi rõ 2 TC chạy nối tiếp trong cùng session.

**Các cặp đã kiểm và KHÔNG phải trùng** (ghi lại để khỏi rà lại vòng sau):

- `NEW-5` vs `NEW-9` — cùng `TOOL-KNOW-002` / `Normal` / cùng xem slot tuần ở preview, **nhưng tiền đề khác**: `NEW-9` bắt buộc phải có friend `F-OK` thỏa filter, `NEW-5` không cần. `NEW-5` là bản tái hiện tối thiểu của BUG-1 (rẻ hơn nhiều để dựng) → giữ cả 2.
- `NEW-1` vs `NEW-12` — cùng "staff có filter vẫn hiện ở preview", nhưng `use_course = 1` vs `use_course = 0` ⇒ tiền đề khác nhánh code.
- `NEW-7` vs `NEW-9` — cùng "đối chiếu preview ⇔ friend", nhưng lịch **tháng** vs lịch **tuần** (2 hàm khác nhau: `showTimeBookingMonth` vs `getListTimeBooking`).

**`DUP-INFLATE`: không có.** Không cặp trùng nào đang làm một quan điểm *trông như* đủ 3 loại case, cũng không làm impact nào ở §3 *trông như* `OK` — các `RISK`/`GAP` ở §3 đến từ thiếu chiều thật, không phải do trùng che.

**`DUP-CONFLICT`: không có** giữa 11 TC với nhau. Có 1 conflict **giữa TC và kho** — xem `[MAJOR-19]` + §6.

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu `11` TC ở BƯỚC 0 + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (498 TC) — không TC đề xuất nào trùng.**
>
> Kho FA-020 đã có TC đúng vùng ảnh hưởng → **dùng lại, không viết mới**:
> - **GAP-9** → `TC-SLN-443` *"Bug: màn tháng không hiển thị khi có filter staff"* (Bug tự detect 9/2025) — chạy lại **sau** khi deploy fix #33222, phía **friend thật**, để chặn `[MAJOR-12]`. Chỉnh: thêm bước so với preview cùng tháng.
> - **GAP-12** → `TC-SLN-465` *"Chuyển nhanh giữa day / week / month khi API chưa trả"* — chạy trên **màn preview** (kho đang viết cho phía LINE user), để chặn `[MAJOR-17]`.
> - `TC-SLN-432` (staff OFF không hiện phía LINE user) và `TC-SLN-257` (setting 指定なし) — **không dùng lại nguyên văn được** vì kho viết cho phía LINE user, còn GAP nằm ở **preview** → dẫn chiếu làm oracle trong `TC-FUNC001-04` và `TC-OUTPREVIEW001-02` bên dưới.
> - `TC-SLN-495` đã cover regression LIFF URL → **không** viết thêm TC `LIFF-ENTRY-001`.
>
> **GAP-2 (`[BLOCKER-2]`) không sinh TC** — `REG-SPEC-001` là hành động **rà soát** 11 TC cũ, không phải case chạy được.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `TC-REGSHARED001-03` | UI | `REG-SHARED-001` | Job gán nhân viên tự động (スタッフ自動割り当て) | Normal | manual | product | Job gán nhân viên tự động vẫn loại đúng nhân viên không thỏa filter bạn bè sau fix | - Lịch salon「サロンA」bật スタッフ自動割り当て<br>- NV-A phụ trách khóa K1, **CÓ** gắn filter bạn bè (điều kiện: có tag T1)<br>- NV-B phụ trách K1, KHÔNG gắn filter<br>- Cả 2 có ca làm cùng khung giờ<br>- Friend F-NG **không** có tag T1; friend F-OK **có** tag T1<br>- **Đã lấy được từ Dev tên chính xác của 2 job gán nhân viên** (`[BLOCKER-1]`) | 1. Dùng friend F-NG mở link đặt lịch salon thật, chọn khóa K1.<br>2. Chọn 指定なし (để hệ thống tự gán) và đặt 1 booking ở khung giờ cả NV-A lẫn NV-B đều rảnh.<br>3. Đợi job gán nhân viên chạy xong.<br>4. Mở màn quản lý booking, xem nhân viên được gán cho booking đó.<br>5. Lặp lại bước 1–4 với friend F-OK. | F-NG: không tag T1 · F-OK: có tag T1 | - Booking của **F-NG** được gán cho **NV-B**, KHÔNG bao giờ gán NV-A (F-NG không thỏa filter của NV-A).<br>- Booking của **F-OK** có thể được gán NV-A hoặc NV-B.<br>- Hành vi giống hệt trước và sau khi deploy fix #33222 — job không truyền cờ preview nên không được nới lỏng filter. |  | Lấp GAP-1 / cover impact F1, F6, T3 · regression · Đánh giá spec: Spec không ghi (đã hỏi Dev — chờ tên job) · Evidence: ảnh màn booking detail hiện tên nhân viên được gán, cho cả 2 friend · RULE-08: job nền, production tách job độc lập |
| `TC-REGSHARED001-04` | UI | `REG-SHARED-001` | Đặt lịch salon — tổng slot khả dụng (`getTotalListTimeBookingQ`) | Normal | manual | product | Tổng số slot khả dụng phía friend không đổi trước/sau fix | - NV-A phụ trách K1 **CÓ** filter bạn bè; NV-B phụ trách K1 không filter; cả 2 có ca làm trong tháng M<br>- Friend F-OK thỏa filter NV-A; friend F-NG không thỏa<br>- **Đã có từ Dev tên hàm/màn dùng `getTotalListTimeBookingQ`** (`[BLOCKER-1]`) | 1. **Trước** khi deploy fix: dùng F-OK mở lịch salon, chọn K1, ghi lại số ngày có slot trong tháng M; lặp với F-NG.<br>2. Deploy fix #33222.<br>3. Lặp lại bước 1 với đúng 2 friend, đúng tháng M.<br>4. So sánh từng con số. | Tháng M cố định; đếm tay số ngày có ca làm của NV-A + NV-B | - Số ngày có slot của **F-OK** và của **F-NG** **giữ nguyên** trước và sau deploy.<br>- F-NG thấy số ngày ít hơn hoặc bằng F-OK (vì bị loại NV-A).<br>- Không phát sinh ngày có slot mới ở luồng friend thật. |  | Lấp GAP-1 / cover impact F1, F6 · regression · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: 2 cặp screenshot lịch tháng trước/sau deploy + bảng đếm tay · RULE-08 |
| `TC-PERM003-01` | API | `PERM-003` | Preview đặt lịch salon — endpoint danh sách nhân viên | Abnormal | auto | staging | Preview không trả nhân viên của bot khác khi đổi `calendar_salon_id` trên URL | - Tài khoản admin U1 chỉ là owner của **bot A**<br>- Bot A có lịch salon SA (`idA`) với nhân viên NV-A1<br>- Bot B (**U1 không có quyền**) có lịch salon SB (`idB`) với nhân viên NV-B1<br>- U1 đang đăng nhập và đang mở preview của SA | 1. Ở preview của SA, mở DevTools → Network, bắt request `GET /ajax/mobile/calendar-salon/get-list-staff-by-calendar`, ghi lại tham số.<br>2. Gửi lại đúng request đó nhưng **thay `calendar_salon_id` = `idB`** (giữ nguyên `line_id='preview'` và session của U1).<br>3. Quan sát response.<br>4. Lặp với endpoint lịch tuần `get-list-time-booking` và lịch tháng, cùng cách đổi id.<br>5. Tạo ở bot A và bot B mỗi bên 1 nhân viên **trùng tên** rồi lặp bước 2. | `calendar_salon_id` = `idB` (thuộc bot khác) | - Cả 3 endpoint **từ chối truy cập** (403 / redirect / danh sách rỗng), **KHÔNG** trả về NV-B1.<br>- Không nhân viên nào của bot B lọt vào response.<br>- Trường hợp trùng tên: response chỉ chứa nhân viên của bot A. |  | Lấp GAP-4 / cover impact F1, F2, F3, F4 · Đánh giá spec: Spec ghi rõ (BR-18 multi-tenant; `calendar_salon_staff.bot_id`) · Evidence: screenshot request/response của cả 3 endpoint · Chặn `[BLOCKER-4]` — Studio coverage đang ghi BR-18 `level=none` · Catalog MAP-PERM-03 |
| `TC-ENV003-01` | API | `ENV-003` | Preview + đặt lịch salon — đối chiếu môi trường | Normal | manual | Tất cả | Bộ case lõi #33222 cho cùng kết quả trên staging và production | - Đã dựng cùng bộ dữ liệu (NV-A có filter + NV-B không filter + khóa K1/K2 + friend F-OK/F-NG) trên **staging** và **production**<br>- Fix #33222 đã deploy ở cả 2 môi trường | 1. Trên **staging**: chạy lần lượt `NEW-1`, `NEW-3`, `NEW-5`, `NEW-7`, `NEW-11`; ghi kết quả từng case.<br>2. Trên **production**: chạy đúng 5 case đó với dữ liệu tương đương.<br>3. Lập bảng đối chiếu staging ⇔ production cho từng case.<br>4. Ghi lại **router id** của production ở mỗi lần gọi, chạy lại 5 case sao cho phủ **cả 2 server** loadbalance.<br>5. Kiểm 2 job gán nhân viên chạy đúng ở production (production tách job độc lập, khác dev/staging chạy gộp). | 5 case lõi × 2 môi trường × 2 router | - 5/5 case cho **cùng kết quả** ở staging và production.<br>- Kết quả không đổi giữa 2 router của production.<br>- Job gán nhân viên ở production cho kết quả như `TC-REGSHARED001-03`.<br>- Mọi khác biệt phát hiện được ghi thành ticket riêng. |  | Lấp GAP-3 / cover impact BUG-1, BUG-2, F1–F5, T1, T2, T3 · Đánh giá spec: Spec ghi rõ (RULE-08 + Catalog D: ENV-JOB, ENV-LB) · Evidence: bảng đối chiếu môi trường đã tick + screenshot/log lấy **trên production** · Chặn `[BLOCKER-3]` — hiện `envAuto` = local 3 run, dev/staging/prd 0 run |
| `TC-FUNC001-03` | UI | `FUNC-001` | Preview đặt lịch salon — bước chọn khóa (コース) | Abnormal | manual | staging | Preview không hiện khóa đã tắt hiển thị hoặc bị filter bạn bè chặn | - Lịch salon「サロンA」`use_course = 1`<br>- Khóa K1: bật hiển thị (`booking_page_display = 1`), không filter<br>- Khóa K2: **tắt** hiển thị (`booking_page_display = 0`)<br>- Khóa K4: bật hiển thị nhưng **CÓ** gắn filter bạn bè (điều kiện: có tag T1)<br>- Friend F-OK có tag T1; friend F-NG không có | 1. Từ màn quản lý lịch salon bấm nút xem trước → mở preview.<br>2. Quan sát danh sách khóa ở bước chọn khóa.<br>3. Mở cùng lịch salon bằng friend **F-OK**, quan sát danh sách khóa.<br>4. Mở bằng friend **F-NG**, quan sát danh sách khóa.<br>5. Lập bảng so 3 danh sách. | K1 (ON, không filter) · K2 (OFF) · K4 (ON, filter tag T1) | - **Preview**: hiện K1 và K4; **KHÔNG** hiện K2 (đã tắt hiển thị) — nhất quán với nguyên tắc fix ở bước chọn nhân viên (bỏ lọc bạn bè, **giữ** các lọc còn lại).<br>- **F-OK**: hiện K1 và K4.<br>- **F-NG**: hiện K1, **không** hiện K4.<br>- Preview khớp F-OK ở cả 3 khóa. |  | Lấp GAP-5 / cover impact BUG-2, T1 · **cũng là root cause thay thế cho `[MAJOR-6]`** (filter gắn ở course thay vì staff) · dẫn từ `TC-SLN-430` · Đánh giá spec: **Spec không ghi** — spec-features không mô tả preview, cần hỏi Dev/BA (§6) · Evidence: 3 screenshot danh sách khóa đặt cạnh nhau |
| `TC-FUNC001-04` | UI | `FUNC-001` | Preview đặt lịch salon — danh sách nhân viên phụ trách khóa | Abnormal | manual | staging | Preview không hiện nhân viên đã tắt hiển thị trên trang đặt lịch | - Lịch salon `use_course = 1`, khóa K1<br>- NV-A: phụ trách K1, `booking_page_display = 1`, có filter bạn bè<br>- NV-D: phụ trách K1, **`booking_page_display = 0`** (đã tắt bằng nút hiển thị trên trang booking)<br>- Cả NV-A và NV-D đều có ca làm trong tuần đang xem<br>- Friend F-OK thỏa filter của NV-A | 1. Mở preview đặt lịch salon, chọn khóa K1.<br>2. Quan sát danh sách nhân viên.<br>3. Chọn NV-A, xem lịch tuần và ghi lại các slot.<br>4. Mở cùng lịch salon bằng friend F-OK, chọn K1, quan sát danh sách nhân viên.<br>5. Bật lại hiển thị cho NV-D rồi lặp bước 1–2. | NV-D `booking_page_display = 0` | - Bước 2: **NV-D KHÔNG xuất hiện** ở preview (fix chỉ được bỏ lọc bạn bè, không được bỏ lọc hiển thị).<br>- Bước 4: NV-D cũng không xuất hiện với F-OK → preview khớp friend.<br>- Bước 5: sau khi bật lại, NV-D xuất hiện ở preview.<br>- Slot của NV-A ở bước 3 không chứa ca làm của NV-D. |  | Lấp GAP-6 / cover impact BUG-2, F2, T1 · dẫn từ `TC-SLN-432` (kho: staff OFF không hiện phía LINE user) · Đánh giá spec: Spec ghi rõ (BR-10 + `calendar_salon_staff.booking_page_display`) · Evidence: screenshot danh sách nhân viên ở preview và ở F-OK, trước/sau khi bật lại NV-D |
| `TC-FUNC001-05` | UI | `FUNC-001` | Preview đặt lịch salon — danh sách nhân viên phụ trách khóa | Boundary | manual | staging | Nhân viên nhận TẤT CẢ khóa (`is_all_course = 1`) hiển thị ở mọi khóa trong preview | - Lịch salon `use_course = 1`, có **3 khóa** K1, K2, K3<br>- NV-E: bật "nhận tất cả khóa học" (`is_all_course = 1`), **CÓ** gắn filter bạn bè, có ca làm<br>- NV-F: `is_all_course = 0`, `course_ids` chỉ chứa K2<br>- NV-G: `is_all_course = 0` và **`course_ids` rỗng** (chưa gán khóa nào)<br>- Friend F-OK thỏa filter của NV-E | 1. Mở preview, chọn khóa K1 → ghi danh sách nhân viên.<br>2. Chọn khóa K2 → ghi danh sách.<br>3. Chọn khóa K3 → ghi danh sách.<br>4. Chọn NV-E ở từng khóa, xem lịch tuần có slot không.<br>5. Mở bằng friend F-OK, lặp bước 1–3. | NV-E `is_all_course=1` · NV-F `course_ids=[K2]` · NV-G `course_ids=[]` | - **NV-E xuất hiện ở CẢ K1, K2, K3** — nhánh lọc theo khóa mới thêm phải được bỏ qua khi `is_all_course = 1`; nếu không NV-E biến mất và fix Bug 2 lại đẻ ra chính Bug 1.<br>- NV-F chỉ xuất hiện ở K2.<br>- NV-G **không** xuất hiện ở khóa nào.<br>- Bước 4: NV-E có slot ở cả 3 khóa.<br>- Bước 5: danh sách của F-OK khớp preview ở cả 3 khóa. |  | Lấp GAP-7 / cover impact BUG-2, F1, F2 · Đánh giá spec: Spec ghi rõ (`db/db-mapping.md:209` — `is_all_course` 1 = nhận tất cả khóa học) · Evidence: 3 screenshot danh sách nhân viên theo từng khóa, ở preview và ở F-OK · Biên nguy hiểm nhất của nhánh `in_array($courseId, $courseIds)` |
| `TC-OUTPREVIEW001-02` | UI | `OUT-PREVIEW-001` | Preview đặt lịch salon — 指定なし (không chỉ định nhân viên) | Normal | manual | staging | Slot của 指定なし ở preview bằng hợp slot của mọi nhân viên, gồm cả nhân viên có filter bạn bè | - Lịch salon `use_course = 1`, đã **bật** lựa chọn 指定なし<br>- Khóa K1 có đúng 2 nhân viên: NV-A (**CÓ** filter bạn bè, ca làm **thứ 2 + thứ 4**) và NV-B (không filter, ca làm **thứ 6**)<br>- Friend F-OK thỏa filter của NV-A | 1. Mở preview, chọn khóa K1, chọn 指定なし.<br>2. Xem lịch tuần và ghi lại **chính xác** các ngày/khung giờ có slot.<br>3. Quay lại, chọn riêng NV-A → ghi slot; chọn riêng NV-B → ghi slot.<br>4. Đối chiếu: slot của 指定なし có bằng hợp của (NV-A ∪ NV-B) không.<br>5. Mở bằng friend F-OK, chọn 指定なし, ghi slot và so với preview. | NV-A: T2 + T4 · NV-B: T6 → hợp = T2, T4, T6 (đếm tay) | - Slot 指定なし ở preview = **T2, T4, T6** (đủ hợp của 2 nhân viên), không thiếu ngày nào của NV-A.<br>- Bằng đúng slot 指定なし mà F-OK nhìn thấy.<br>- Trước fix NV-A bị loại nên 指定なし chỉ còn T6 — sau fix phải đủ 3 ngày. |  | Lấp GAP-8 / cover impact BUG-1, F1, F3, T1 · dẫn từ `TC-SLN-257` (kho: setting 指定なし phía LINE user) · Đánh giá spec: Spec không ghi (đã hỏi Dev — §6) · Evidence: cặp screenshot lịch tuần 指定なし ở preview và ở F-OK + bảng đếm tay 3 ngày |
| `TC-OUTPREVIEW001-03` | UI | `OUT-PREVIEW-001` | Preview đặt lịch salon — danh sách nhân viên phụ trách khóa | Boundary | manual | staging | Khóa mà TẤT CẢ nhân viên đều có filter bạn bè — preview hiện đủ, friend không thỏa thì rỗng | - Lịch salon `use_course = 1`, khóa K5<br>- **Toàn bộ** nhân viên phụ trách K5 (NV-H, NV-I) đều **CÓ** gắn filter bạn bè, đều có ca làm<br>- Friend F-NG **không thỏa** filter của cả NV-H lẫn NV-I<br>- Friend F-OK thỏa cả hai | 1. Mở preview, chọn khóa K5 → quan sát danh sách nhân viên và slot.<br>2. Mở bằng **F-NG**, chọn K5 → quan sát danh sách nhân viên và màn hình kết quả.<br>3. Mở bằng **F-OK**, chọn K5 → quan sát.<br>4. So 3 kết quả. | K5 có 2/2 nhân viên đều gắn filter | - **Preview**: hiện đủ NV-H + NV-I kèm slot (bỏ lọc bạn bè).<br>- **F-NG**: danh sách nhân viên **rỗng**, màn hiển thị trạng thái rỗng rõ ràng — KHÔNG trắng màn, KHÔNG loading vô hạn, KHÔNG báo "thành công".<br>- **F-OK**: khớp preview.<br>- Đây là trường hợp preview **cố ý khác** friend — phải xác nhận đúng chủ đích, không phải bug. |  | Lấp GAP-11 / cover impact BUG-1, T1, T2 · Đánh giá spec: **Spec không ghi** — chính là điểm cần chốt ở §6 (preview khác friend đến mức nào là chấp nhận được) · Evidence: 3 screenshot đặt cạnh nhau · Bổ sung chiều `Boundary` còn thiếu của `OUT-PREVIEW-001` (RULE-01) |
| `TC-FRIEND001-02` | UI | `FRIEND-001` | Preview + đặt lịch salon — filter bạn bè theo type friend info | Normal | manual | staging | Filter nhân viên hoạt động đúng với nhiều type friend info khác nhau | - Khóa K1 có 4 nhân viên, mỗi nhân viên gắn 1 filter dùng **1 type friend info khác nhau**: NV-J = `text`, NV-K = `select`, NV-L = `date` (ngày sinh), NV-M = `point` (số)<br>- Friend F-OK có giá trị **thỏa cả 4** filter<br>- Friend F-NG có giá trị **không thỏa cả 4** | 1. Mở preview, chọn K1 → ghi danh sách nhân viên.<br>2. Mở bằng **F-OK**, chọn K1 → ghi danh sách.<br>3. Mở bằng **F-NG**, chọn K1 → ghi danh sách.<br>4. Sửa giá trị friend info của F-NG cho **thỏa riêng filter của NV-L (date)**, mở lại → ghi danh sách.<br>5. **Xóa** giá trị friend info vừa sửa của F-NG, mở lại → ghi danh sách. | 4 type: text · select · date · point | - Bước 1 (preview): hiện **đủ 4** nhân viên (bỏ lọc bạn bè, không phân biệt type).<br>- Bước 2 (F-OK): hiện đủ 4.<br>- Bước 3 (F-NG): **rỗng**.<br>- Bước 4: chỉ hiện **NV-L**.<br>- Bước 5: trở lại **rỗng** — xóa giá trị phải có tác dụng ngay, không còn kết quả cũ. |  | Lấp GAP-10 / cover impact F5, T2 · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: bảng kết quả 5 bước + screenshot danh sách nhân viên từng bước · Bổ sung chiều `Normal` còn thiếu của `FRIEND-001` (RULE-01); Catalog `MAP-FI-*` |

---

## 6. Spec update needed

| # | Vấn đề | Hiện trạng | Cần ai chốt |
|---|---|---|---|
| 1 | **Giả định nền của cả fix chưa được ai xác nhận**: *"preview xem như bạn bè thỏa điều kiện lọc"*. | AI **tự suy từ code hiện hữu** (mục 6 VERIFY: *"`getListCourseByCalendar` và `getListStaffByCalendar` đã có sẵn nhánh bỏ qua lọc khi `lineId='preview'` → xác nhận ý đồ"*). `spec-features/admin/salon-booking/` **không có dòng nào** về preview. | **BA / Leader** — chốt rồi ghi vào `spec-features/admin/salon-booking/feature-spec.md` |
| 2 | **`[MAJOR-19]` Hai loại filter mang nghĩa ngược nhau.** Filter cấp **nhân viên** (`calendar_salon_staff.filter_id`): thỏa ⇒ **được thấy** nhân viên. Filter cấp **calendar**「予約ページの非表示」: theo `TC-SLN-350` của kho FA-020, khách **thỏa** ⇒ **bị chặn** trang. Nguyên tắc "preview coi như thỏa" áp lên loại thứ 2 sẽ khiến preview **tự chặn chính nó**. Không spec nào và không TC nào nói preview xử lý filter「予約ページの非表示」ra sao. | Chưa xác định. **Không tự chọn bên.** | **Dev + BA** — chốt hành vi đúng, rồi bổ sung TC tương ứng |
| 3 | **Preview được phép khác friend đến mức nào?** Fix cố ý làm preview **khác** friend không thỏa filter (preview thấy, friend không). Nhưng tiêu đề ticket lại là *"preview đang hiển thị khác với bên friend"*. Cần định nghĩa rõ: preview khớp friend **thỏa mọi điều kiện** — và mọi khác biệt ngoài phạm vi đó là bug. | `NEW-9` ngầm dùng định nghĩa này nhưng chưa được viết thành spec; `TC-OUTPREVIEW001-03` (§5) chạm đúng vùng xám này. | **BA / Leader** |
| 4 | **`[NIT-1]` Root cause `Conversation::advanceFilterPost` chưa được sửa.** `when(!empty($lineUserId))` với mảng `[null]` ⇒ `!empty([null]) === true` ⇒ `whereIn('line_user_id',[null])` không khớp gì ⇒ `isValidFilter` luôn `false`. Fix hiện tại **bypass ở tầng trên**. Vì file này không bị chạm code nên **không phát sinh hồi quy** từ ticket này — nhưng bất kỳ luồng nào khác truyền `lineUserId` rỗng sẽ dính lại đúng lỗi này. | Dev chọn không sửa (mục 3, bảng dòng 8). | **Dev** — quyết định sửa tận gốc ở ticket riêng, hay ghi nhận là nợ kỹ thuật |
| 5 | **Bug 2 có được coi là fix trọn không?** `03-dev-impact.md` điểm nghi vấn #5 hỏi: *"Bug 2 chỉ được xử lý ở `getListStaffByCalendar`. Màn ngày/giờ và bước `getListCourseByCalendar` có bị lệch tương tự không?"* — **chưa có ai trả lời**, và không TC nào chạm bước chọn khóa. | `TC-FUNC001-03` (§5) được thiết kế để trả lời. | **Dev** |
| 6 | **Không có link PR** (`[MAJOR-9]`) → không xác nhận được fix shape thực tế khớp mô tả. | `03-dev-impact.md`: *"không có link PR trong Redmine"*, commit `bcc9733e24`. | **Dev** |
