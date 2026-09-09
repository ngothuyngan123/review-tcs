# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38280` — [Lesson] Đặt giới hạn 1 khung/ngày nhưng 2 người bấm đăng ký cùng lúc thì cả hai đều đặt được |
| Reviewer (Leader) | `<Leader ký>` (draft sinh bởi `/review-tc`, 2026-07-13) |
| Tester được review | `Thanh Phương` |
| Ngày review | `2026-07-13` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |
| Input files | `01-bug-task.md` ✔ · `02-spec-reference.md` ✘ (không có) · `03-dev-impact.md` ✔ · `04-tc-list.md` ✔ (26 TC) |

> **Spec reference**: không có `02-spec-reference.md` → dùng `templates/LME-SYSTEM-SPEC.md` tổng (FA-019 Lesson / FA-020 Salon). Không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có BLOCKER, cần bổ sung TC và review lại

**Lý do ngắn gọn**: Bộ 26 TC chỉ soi **1 chiều duy nhất** của race condition (N user tự đặt, cùng khung, cùng lúc, verify bằng mắt trên UI). Toàn bộ **khe hở mà chính Dev tự thừa nhận** (ranh giới giây, không có lock, production 2 server), toàn bộ **tầng DB** (bản dư bị `DELETE` cứng, `total_booking` đếm lại, `WHERE` scope), toàn bộ **side-effect của việc xóa booking** (tin LINE xác nhận / remind / Google Calendar / **trừ tiền**), và **2/4 kịch bản bắt buộc của `CONC-001`** đều **không có TC nào**. Trạng thái `OK staging` hiện tại **chưa chứng minh được là TC đã thật sự trigger đúng code path arbiter**.

---

## 2. Tóm tắt cho member

Bộ TC có **cấu trúc rất tốt**: đã tách rõ 2 nhánh *không bill tiền* / *có bill tiền*, có bậc thang remain = ∞ / 2 / 1, có cả case tuần tự (A trước, B sau) làm đối chứng, và đã chủ động mở rộng sang **Salon** đúng theo scope fix của Dev — đây là phần nhiều bộ TC khác hay bỏ sót.

Vấn đề lớn nhất **không nằm ở số lượng TC mà ở độ sâu của Expected**. Cách fix của Dev là *"tạo booking trước → phát hiện trùng → **xóa** bản dư → đếm lại"*, nên rủi ro thật không phải "có chặn được không" (UI thấy được) mà là **"cái gì đã kịp xảy ra trước khi bản dư bị xóa"**: user thua đã kịp bị trừ tiền chưa, đã kịp nhận tin xác nhận chưa, `total_booking` sau khi đếm lại có đúng không, và **arbiter có xóa nhầm booking của lịch/bot khác không**. Không TC nào chạm tới các câu hỏi đó.

Việc cần làm ở round 2: bổ sung **16 TC** ở §5 (ưu tiên NEW-01 → NEW-08), điền cột **Type / Priority / Output note (evidence)**, và **chứng minh bằng log rằng 2 request thực sự tới cùng giây** — nếu 2 lần bấm tay lệch nhau vài trăm ms thì `checkCanBooking` cũ đã chặn rồi, TC pass mà **chưa hề đi qua code fix**.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — race check-then-act ở `order()` luồng free | Fix | — | TC004, TC005 (+ TC017, TC018 Salon) | 4 | **RISK** — có TC reproduce, nhưng (a) không chứng minh 2 request cùng giây, (b) chưa làm rõ giới hạn KH set là *per-slot* hay *per-ngày* (xem BLOCKER-1) |
| **F1** — `order()` Lesson free | Function | Direct | TC001–TC007 | 7 | **RISK** — chỉ verify UI, không verify DB / không có double-click / 2 tab |
| **F2** — `checkCanBooking()` | Function | Direct | TC003, TC006 | 2 | **OK** (đường tuần tự có đối chứng) |
| **F3** — `countTotalBookingStatus()` (đếm lại `total_booking`) | Function | Direct | — | 0 | **GAP** |
| **F4** — `checkValidSlot()` Lesson paid (không sửa) | Function | Indirect | TC008–TC013 | 6 | **RISK** — có regression UI, nhưng không đối chiếu gateway / không verify "user thua không bị trừ tiền" |
| **F5** — `acquireReceptionBookingLock()` / `releaseReceptionBookingLock()` | Function | Direct | — | 0 | **GAP** — và bản thân sự tồn tại của helper này đang mâu thuẫn trong report Dev |
| **F6** — `rejectDuplicateSalonBooking()` | Function | Direct | TC014–TC026 | 13 | **RISK** — không cover fail-safe (không xác định được giới hạn → bỏ qua), không cover giới hạn theo nhân viên/season |
| **D1** — `calendar_course_bookings` (CREATE + **DELETE** bản dư) | Data | — | — | 0 | **GAP** — không TC nào query DB; không TC kiểm `WHERE` scope |
| **D2** — `calendar_salon_line_booking` (CREATE + **DELETE**) | Data | — | — | 0 | **GAP** |
| **D3** — `calendar_course_receptions.total_booking` (UPDATE) | Data | — | — | 0 | **GAP** — số chỗ còn lại hiển thị cho LINE user lấy từ đây |
| **D4** — `calendar_salon_setting_limit_booking` (READ) | Data | — | TC014–TC026 (gián tiếp) | 0 trực tiếp | **RISK** |
| **T1** — Lesson / Calendar Booking (FA-019) free | Feature | High | TC001–TC007 | 7 | **RISK** |
| **T2** — Lesson (FA-019) luồng thanh toán | Feature | Medium | TC008–TC013 | 6 | **RISK** |
| **T3** — Salon Booking (FA-020) | Feature | High | TC014–TC026 | 13 | **RISK** |
| **(thiếu trong 4.3)** — Booking **Event** — chức năng tương tự, cùng pattern check-then-act | Feature | ? | — | 0 | **GAP** — `REG-SHARED-001` |
| **(thiếu trong 4.3)** — Luồng **admin duyệt request booking** / **ADMIN_BOOK** (status 2) | Feature | ? | TC007, TC020 (chỉ tạo request, không duyệt) | 0 | **GAP** |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề. TC001–003 / TC014–016 (slot không giới hạn, remain=2, 1 user đặt) là **đối chứng false-positive** cho arbiter — **giữ lại**, nhưng phải nâng Expected xuống tầng DB (xem NEW-16). | Giữ |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **Race-condition** (biến thể hiếm: *detect-then-delete* — tạo bản ghi trước rồi xóa bản dư, **KHÔNG dùng lock, KHÔNG dùng atomic conditional UPDATE**). Kèm shape phụ: **xóa dữ liệu** (`DELETE` booking) + **sửa hàm dùng chung** (áp cùng helper cho Lesson và Salon). |
| **Trigger space cần cover** (`CONC-001` — 4 kịch bản bắt buộc) | (1) **double-click 1 nút** · (2) **cùng user, 2 tab / 2 thiết bị** · (3) **2 user thao tác gần đồng thời trên cùng bản ghi** (gồm cả **admin duyệt** 2 request, **ADMIN_BOOK** vs user tự đặt) · (4) **batch/đa luồng cùng chạm 1 giới hạn dùng chung** |
| **Số trigger TCs hiện cover** | **1 / 4** — chỉ kịch bản (4) (2 user, 3 user tự đặt cùng khung). Kịch bản (1), (2), (3) = 0 TC. |
| **Trigger space riêng của cách fix này** (do Dev tự nêu ở mục "Rủi ro") | (a) **Race lệch qua ranh giới giây** → arbiter mù (arbiter so `created_at` ở độ phân giải **giây**) · (b) **Bản id nhỏ chưa commit** lúc bản id lớn query → cả 2 cùng sống · (c) **Production 2 app server (loadbalance)** → cửa sổ race rộng hơn staging · (d) Salon: **season limit không tra được → fail-safe bỏ qua** (tức là **vẫn over-book**, im lặng) |
| **Số TC cover 4 rủi ro tự-thừa-nhận này** | **0 / 4** |
| **KH report dạng** | **Có root cause khá cụ thể** (KH nói rõ "bấm hoàn toàn đồng thời", Dev tái hiện đúng check-then-act) → **không** dính AP-2 thuần. **NHƯNG**: KH viết `1日の受付枠を1枠に設定` = *"đặt số khung tiếp nhận **trong 1 ngày** là 1 khung"* — TCs lại test `Slot có số remain = 1` (**số chỗ trong 1 khung**). Hai khái niệm này **không đồng nhất** → xem BLOCKER-1. |
| **Alternative root causes cần verify** | (1) Giới hạn **theo NGÀY** (2 user đặt **2 khung giờ khác nhau** trong cùng ngày, cùng lúc) — arbiter chỉ so **cùng khung** nên **không bắt được**. (2) Race giữa **user tự đặt** và **ADMIN_BOOK** / **admin duyệt request** — arbiter chỉ nhận diện booking `APPROVE`. |
| **Anti-patterns dính** | **AP-4** (mục "Commit / Pull Request" chỉ có commit hash `41cc44c4ce`, **không có link PR/diff** → không verify được fix shape thật: còn `acquireReceptionBookingLock` hay không, Salon paid có arbiter hay không). **AP-3** (mỗi Tx đều chỉ có regression happy-path, không có edge state). |

> Trigger cover **1/4** (CONC-001) và **0/4** (rủi ro tự thừa nhận) → flag **[BLOCKER] FIX-SHAPE** ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-1 · `CONC-001` thiếu 2/4 kịch bản bắt buộc**: không có TC nào cho **double-click 1 nút** (kịch bản 1) và **cùng 1 LINE user mở 2 tab / 2 thiết bị đặt song song** (kịch bản 2). Đây là 2 đường race **dễ xảy ra hơn** ngoài đời so với "2 người lạ bấm trúng cùng mili-giây". — **Fix**: bổ sung **NEW-02, NEW-03**.

- **[BLOCKER] FIX-SHAPE — GAP-2 · Không TC nào test khe hở mà chính Dev đã cảnh báo**: report Dev ghi rõ *"created_at độ phân giải giây: race lệch qua **ranh giới giây** sẽ không bị arbiter bắt"* và *"không có lock nên còn khe race rất hẹp"*. Bộ TC **không có TC nào** cố tình bắn 2 request lệch nhau ~100ms nhưng rơi vào **2 giây khác nhau** (vd `10:00:00.95` và `10:00:01.05`) — đúng kịch bản KH gặp. — **Fix**: bổ sung **NEW-01**. Nếu kết quả vẫn over-book → đây là **known limitation phải được Leader/PM chấp nhận bằng văn bản**, không được đóng ticket im lặng.

- **[BLOCKER] GAP-3 · `DATA-DB-001` / RULE-07 — fix có `DELETE` cứng nhưng 0 TC verify DB**: arbiter **xóa bản ghi booking** (`calendar_course_bookings` / `calendar_salon_line_booking`) rồi **update lại** `total_booking`. Toàn bộ 26 TC dừng ở màn LINE user. Không TC nào: (a) đếm số bản ghi thật trong DB sau race; (b) verify `total_booking` sau khi `countTotalBookingStatus` đếm lại; (c) **kiểm `WHERE` scope** — tạo booking **trùng khung giờ, trùng giây ở 2 calendar / 2 bot khác nhau** để chứng minh arbiter **không xóa nhầm** booking hợp lệ của bên kia. Với 1 fix mà hành động chính là `DELETE`, đây là rủi ro **mất dữ liệu thật của khách**. — **Fix**: **NEW-04, NEW-05, NEW-16**.

- **[BLOCKER] GAP-4 · Side-effect của booking bị xóa — RULE-06 (output cuối chuỗi) + `STATE-001`**: bản dư được **tạo với status APPROVE** rồi mới bị xóa. Trong khoảng đó, luồng đặt lịch bình thường của LME có thể đã kịp: gửi **tin xác nhận trên LINE**, tạo **remind schedule**, ghi **Google Calendar**, cập nhật **friend info**, gán **tag / chạy action**. Nếu các side-effect này chạy trước arbiter → user thua nhận tin *"đặt lịch thành công"* nhưng **không có booking nào tồn tại** (dữ liệu nửa vời + KH khiếu nại lần 2). Expected của TC004/TC005 chỉ ghi *"user còn lại nhận thông báo hết chỗ"* — **không phủ nhận** việc user đó cũng nhận tin xác nhận. — **Fix**: **NEW-06** (verify user thua **KHÔNG** có: tin LINE xác nhận, mail, remind, event Google Calendar, tag/action).

- **[BLOCKER] GAP-5 · `PAY-STATE-001` — 2 user thanh toán đồng thời: ai bị trừ tiền?** Nhóm TC *"có setting bill tiền"* (TC008–TC013 Lesson, TC021–TC026 Salon) chỉ verify UI *"user còn lại nhận thông báo hết chỗ"*. **Không TC nào** đối chiếu **dashboard Stripe / UnivaPay** để chứng minh user thua **không bị charge** (hoặc được refund). Tiền = ưu tiên **Cao tuyệt đối**. Đặc biệt với Salon: mục 2 của Dev nói arbiter chạy **trước khi charge** trong `createOrderPayment`, nhưng mục "Rủi ro" lại nói Salon paid **chưa** có arbiter — **2 câu này không thể cùng đúng**. — **Fix**: **NEW-07, NEW-08** + bắt Dev chốt bằng văn bản.

- **[BLOCKER] GAP-6 · `REG-SHARED-001` — chưa có danh sách nơi ảnh hưởng từ Dev, và Booking **Event** bị bỏ trắng**: `checklist-lme.md` ghi thẳng *"cặp **Salon / Lesson / Booking Event** là điểm lặp lại"*. Dev đã tự mở rộng fix từ Lesson sang Salon (tức là **đã xác nhận pattern lặp**) nhưng **không nói gì về Booking Event** — và cũng chưa cung cấp danh sách nơi ảnh hưởng theo yêu cầu của quan điểm. Nếu Event booking cũng dùng check-then-act thì bug **vẫn còn nguyên** ở đó. — **Fix**: yêu cầu Dev rà `order()` của **Booking Event** (và mọi chỗ có giới hạn số lượng: item số lượng có hạn); bổ sung **NEW-12**.

- **[BLOCKER] GAP-7 · Race chuyển sang tầng admin — `ADMIN_BOOK` + duyệt request booking**: Dev ghi *"Nhận diện đồng thời **chỉ xét APPROVE**; đếm sức chứa giữ đủ 3 status (APPROVE + ADMIN_BOOK + REQUEST_CANCEL)"*. Suy ra: nếu bản ghi tạo cùng giây là **ADMIN_BOOK** (admin đặt hộ khách) chứ không phải APPROVE → **arbiter không kích hoạt** → vẫn over-book. Tương tự, TC007/TC020 dừng lại ở *"cả 2 tạo được request booking"* mà **không đi tiếp bước admin duyệt** — 2 request cùng được duyệt tại slot remain=1 thì vượt giới hạn y hệt bug gốc, chỉ dời sang tầng admin (duyệt được từ **cả web lẫn app admin** — `MAP-SEND-19`). — **Fix**: **NEW-09, NEW-10**.

- **[BLOCKER] BLOCKER-1 · Giới hạn KH set là *"1 khung/NGÀY"* hay *"1 chỗ/khung"*? — TCs và fix đang giả định vế sau**: KH viết `1日の受付枠を1枠に設定` (= *số khung tiếp nhận **trong 1 ngày** = 1*). Toàn bộ TC lại test theo trục `Slot có số remain = N` (số chỗ **trong 1 khung**), và arbiter của Dev **chỉ so booking cùng khung (same reception)**. Nếu giới hạn thật sự áp **theo NGÀY**, thì 2 user đặt **2 khung giờ khác nhau trong cùng ngày** vào cùng lúc sẽ **không bị arbiter bắt** → **bug chưa được fix**. `Input thiếu`: Redmine không có screenshot màn setting để phân định. — **Fix**: hỏi Dev/KH xác nhận ngữ nghĩa của setting (calendar_id: 10955); nếu là per-day → bổ sung **NEW-11** và **fix phải được làm lại**.

- **[BLOCKER] GAP-8 · Evidence hiện tại không chứng minh TC đã đi qua code fix**: 26/26 TC ghi `OK staging`, nhưng steps chỉ là *"2 user nhấn booking cùng lúc"* (2 người bấm tay). Nếu 2 request lệch nhau > vài trăm ms, `checkCanBooking` **cũ** đã chặn — TC **pass mà không hề chạm arbiter**, tức là "OK" giả. `CONC-001` yêu cầu evidence là **số lần xử lý thực tế đếm từ log/DB**, không phải ảnh chụp màn hình. — **Fix**: mọi TC race phải đính kèm **log 2 request kèm timestamp (ms)** chứng minh đã tới cùng giây, + query DB đếm bản ghi. Ghi vào cột **Output note** (RULE-02).

### 4.2 Major (nên fix)

- **[MAJOR] AP-4 · Không có link PR/diff**: mục "Commit / Pull Request" chỉ có hash `41cc44c4ce`. Không đọc được diff → **không thể verify** fix shape thật (còn named lock hay không; Salon paid có arbiter hay không). Yêu cầu Dev cung cấp link PR trước khi Leader duyệt coverage.

- **[MAJOR] `01-bug-task.md` auto-filled từ Redmine nhưng **checkbox "Tester verify auto-fill chính xác" CHƯA tick**. Review chỉ có giá trị sau khi tester xác nhận đã đọc lại Redmine (đặc biệt journal #123920 chứa steps và calendar_id).

- **[MAJOR] `03-dev-impact.md` auto-filled từ Redmine nhưng **checkbox verify CHƯA tick**, và bản thân report Dev **tự mâu thuẫn 2 chỗ** (Salon paid có/không arbiter; có/không named lock). F/D/T có thể sai → mọi kết luận coverage bên dưới đều treo theo.

- **[MAJOR] RULE-01 · Cột `Type` và `Priority` trống 26/26 TC**: không phân loại được Normal / Abnormal / Boundary → **không kiểm chứng được** quan điểm ưu tiên Cao (`CONC-001`, `DATA-DB-001`, `PAY-STATE-001`) có đủ 3 loại case hay không. Thực tế đọc nội dung thì **thiếu hẳn nhóm Boundary** (không có TC nào chạm biên: ranh giới giây, đúng ngưỡng limit ±1, remain=0).

- **[MAJOR] RULE-02 · Cột `Output note` (evidence) trống 26/26 TC**: `CONC-001` bắt buộc evidence = *số lần xử lý thực tế từ log/DB*; `PAY-STATE-001` bắt buộc screenshot **3 nơi** (admin / user / gateway). Không ghi → không được tick Đạt.

- **[MAJOR] RULE-08 / `ENV-003` · 26/26 TC kết luận từ **Staging***: task chạm **bill tiền** (nhóm TC có setting bill tiền) và production có **2 app server loadbalance** (Catalog D — `ENV-LB`) → cửa sổ race trên production **rộng hơn** staging (2 process, 2 kết nối DB, latency khác). RULE-08 ghi rõ: hạng mục **bill tiền / loadbalance không được kết luận từ staging**. — **Fix**: **NEW-14** (chạy lại kịch bản race trên production, lưu **router id** của từng request).

- **[MAJOR] AP-3 · Regression happy-path-only**: T1/T2/T3 mỗi cái chỉ có TC ở trạng thái sạch. Không có TC đặt lịch ở **edge state**: slot vừa có người **hủy** (`REQUEST_CANCEL` — status 5 **vẫn chiếm chỗ** theo Dev) rồi user khác đặt ngay; slot remain=0; calendar hết hạn/đã tắt. — **Fix**: **NEW-13**.

- **[MAJOR] GAP-9 · `DATA-COUNT-001` · Số chỗ còn lại hiển thị cho LINE user**: `total_booking` được **đếm lại** sau khi xóa bản dư. Không TC nào verify **con số "còn N chỗ"** trên trang booking (và màn admin `Today&NewBooking`) khớp với số booking thật sau race. Đây là quan điểm có **12 ticket Closed** trong lịch sử.

- **[MAJOR] GAP-10 · Salon fail-safe im lặng**: Dev ghi *"giới hạn theo **mùa (season)** không tra → khi không chắc thì **bỏ qua** (fail-safe, không xóa nhầm)"* — nghĩa là ở cấu hình season, arbiter **tắt** và bug **vẫn còn**. Không TC nào chạm cấu hình season, cũng không TC nào cover giới hạn **theo nhân viên** (`calendar_salon_setting_limit_booking`). — **Fix**: **NEW-15**.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC ID / cột chuẩn**: sheet gốc không có cột `Type` / `Priority` / `Output note` / `Assignee` — bộ TC không bám 10 cột chuẩn của team (`templates/04-tc-list.template.md`). Đề nghị bổ sung 4 cột này vào tab `Booking phía line user`.

- **[MINOR] Range TC trong Redmine lệch 1 dòng**: journal #125009 ghi `row 551~562` / `1397~1408` nhưng Sheet có **13 dòng** mỗi bên (551–563 / 1397–1409). Dòng cuối (*"remain=1, A đặt trước rồi B"* nhóm **có** bill tiền) nằm ngoài range đã báo. Cập nhật lại note trên Redmine để tránh sót khi bàn giao.

- **[MINOR] Steps chưa tái lập được**: *"2 user nhấn booking cùng lúc"* không phải steps thực thi được (RULE: steps phải tuần tự, rõ ràng). Cần ghi rõ **cách tạo đồng thời** (2 thiết bị + đếm 3-2-1, hay bắn 2 request song song bằng script/Postman runner) và **cách chứng minh** đã cùng giây.

- **[MINOR] TC007 / TC020 (request booking) Expected mơ hồ**: *"Cả 2 booking đều book success, trạng thái là request booking"* — cần ghi rõ đây là **hành vi đúng theo spec** (request chưa chiếm chỗ) hay chỉ là **hiện trạng quan sát được**. Nếu là spec thì phải nói tiếp: khi admin duyệt, chỗ được cấp cho ai.

### 4.4 Nit (gợi ý)

- **[NIT]** Lesson và Salon dùng **cùng một bộ 13 case** — tốt cho tính đối xứng, nhưng Salon có thêm trục **nhân viên / season / overlap giờ** mà Lesson không có. Nên tách bộ Salon riêng thay vì copy nguyên.
- **[NIT]** Nên thêm 1 TC "đặt lịch tuần tự bình thường nhưng **trong cùng 1 giây**" (2 user, slot remain=**2**, đặt cùng giây, cả 2 **phải** thành công) để chứng minh arbiter **không xóa nhầm** — hiện TC002/TC015 có ý này nhưng dừng ở UI, chưa xuống DB. Đã đưa vào **NEW-16**.
- **[NIT]** `01-bug-task.md`: nên đính screenshot màn setting `1日の受付枠` của KH (calendar_id 10955) vào Redmine — sẽ giải quyết dứt điểm BLOCKER-1.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round 2. **Ưu tiên NEW-01 → NEW-08** (chặn merge).
> Ký hiệu chung — **Cách tạo đồng thời chuẩn** dùng cho mọi TC race: chuẩn bị 2 (hoặc N) request đã điền sẵn form, bắn song song bằng **script / Postman Collection Runner / 2 thiết bị + trigger chung**; sau đó **lấy log server 2 request kèm timestamp mili-giây** để chứng minh đã tới **cùng giây** (nếu không cùng giây → TC **không hợp lệ**, chạy lại).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact + quan điểm | Evidence bắt buộc |
|---|---|---|---|---|---|---|---|---|
| **NEW-01** | Race **lệch qua ranh giới giây** — arbiter không bắt được (khe hở Dev tự thừa nhận) | Lesson, calendar **không** bill tiền, 1 khung còn **remain = 1**. 2 LINE user A/B đã kết bạn. | 1. Bắn request đặt của A tại `T = HH:MM:SS.950`.<br>2. Bắn request của B tại `T + 100ms` (= `HH:MM:SS+1.050`) → **2 giây khác nhau**.<br>3. Query DB đếm booking của khung đó. | Chỉ **1** booking `APPROVE` tồn tại; B nhận thông báo hết chỗ.<br>⚠️ Nếu **cả 2** tồn tại → **fix chưa đóng được bug**, escalate ngay cho Dev/Leader (không được đóng ticket). | Cao | Boundary | BUG, F1, D1 · `CONC-001`, `ENV-001` | Log 2 request kèm ms + query `SELECT id, created_at FROM calendar_course_bookings WHERE ...` |
| **NEW-02** | **Double-click** nút đặt lịch bởi **1 user** tại slot remain = 1 | Như NEW-01, chỉ 1 user A. | 1. A bấm nút "予約する" **2 lần liên tiếp trong < 300ms**.<br>2. Query DB. | Đúng **1** booking được tạo. Không tạo 2 bản rồi xóa 1 (kiểm `id` không bị nhảy 2 đơn vị nếu có thể). Không có tin xác nhận gửi 2 lần. | Cao | Boundary | BUG, F1, D1 · `CONC-001` kịch bản 1 | Query DB đếm booking + log số lần `order()` được gọi + LINE app (chỉ **1** tin xác nhận) |
| **NEW-03** | **Cùng 1 LINE user, 2 tab / 2 thiết bị** đặt song song cùng khung | Slot remain = 1. User A mở trang đặt lịch trên **2 tab** (hoặc điện thoại + PC). | 1. Bấm đặt trên cả 2 tab **đồng thời**.<br>2. Query DB. | Theo spec: 1 user chỉ được 1 chỗ/khung → đúng **1** booking; tab còn lại báo lỗi rõ ràng.<br>`Input thiếu`: nếu spec **cho phép** 1 user đặt nhiều chỗ → Expected phải sửa theo spec, **hỏi PM trước khi chạy**. | Cao | Boundary | BUG, F1 · `CONC-001` kịch bản 2, `SEC-ISO-001` | Screenshot 2 tab + query DB |
| **NEW-04** | Verify **3 tầng** sau race: DB + màn hình + output (RULE-07) | Slot remain = 1. 2 user A/B bắn đồng thời (cùng giây). | 1. Chạy race.<br>2. Query `calendar_course_bookings` đếm bản ghi khung đó.<br>3. Query `calendar_course_receptions.total_booking`.<br>4. Mở trang booking phía LINE user + màn admin `Today&NewBooking`. | (a) DB: đúng **1** booking chiếm chỗ; (b) `total_booking` = **1** (đếm lại đúng sau khi xóa bản dư, không bị lệch); (c) trang LINE hiện **"hết chỗ"**; (d) màn admin hiện **1** booking. **Cả 4 phải khớp.** | Cao | Normal | F3, D1, D3, T1 · `DATA-DB-001`, `DATA-COUNT-001`, RULE-07 | Ảnh query trước/sau (kèm câu query) + screenshot 2 màn |
| **NEW-05** | **`WHERE` scope** — arbiter KHÔNG được xóa nhầm booking của calendar / bot khác | 2 bot (hoặc 2 calendar / 2 course) **khác nhau**, mỗi bên có 1 khung **cùng ngày cùng giờ**, mỗi bên remain = 1. | 1. Bắn **đồng thời trong cùng 1 giây**: user A đặt ở **bot 1**, user B đặt ở **bot 2** (2 booking hợp lệ, khác khung).<br>2. Query DB cả 2 bot. | **Cả 2** booking đều tồn tại. Arbiter **không** xóa bên nào (điều kiện query phải đủ `bot_id` / `course_id` / `reception_id`). | Cao | Abnormal | D1, D2, F1, F6 · `DATA-DB-001`, `PERM-003` | Query DB **2 tài khoản** trước/sau (kèm câu query) |
| **NEW-06** | User **thua cuộc** không được nhận bất kỳ side-effect nào của booking đã bị xóa | Slot remain = 1. Calendar có bật: tin xác nhận LINE, remind, sync Google Calendar, action gắn tag. 2 user A/B. | 1. Chạy race → B là bản dư bị xóa.<br>2. Kiểm **LINE app của B** (iOS + Android).<br>3. Kiểm hộp thư của B.<br>4. Kiểm remind schedule trong DB/admin.<br>5. Kiểm Google Calendar.<br>6. Kiểm tag / friend info của B. | B **KHÔNG** nhận tin "đặt lịch thành công", **KHÔNG** có mail xác nhận, **KHÔNG** có remind đã lên lịch, **KHÔNG** có event trên Google Calendar, **KHÔNG** bị gắn tag/chạy action. B chỉ nhận **thông báo hết chỗ**. | Cao | Abnormal | D1, T1, T3 · RULE-06, `STATE-001`, `STATE-DEP-001`, `INTG-CAL-001` | Screenshot LINE app thật (iOS+Android) + hộp thư + query remind + ảnh Google Calendar |
| **NEW-07** | **Lesson có bill tiền** — 2 user thanh toán đồng thời tại slot remain = 1: user thua **không bị trừ tiền** | Lesson calendar **có** setting bill tiền (Stripe hoặc UnivaPay sandbox). Slot remain = 1. 2 user A/B, thẻ test hợp lệ. | 1. A và B cùng hoàn tất bước thanh toán **đồng thời**.<br>2. Đối chiếu **3 nơi**: admin LME / màn user / **dashboard gateway**. | Chỉ 1 booking + **1** giao dịch charge thành công. User thua: **không có charge** (hoặc có charge → **phải được refund tự động**, và trạng thái hiển thị đúng ở cả 3 nơi). **Tuyệt đối không** có case "mất tiền, không có chỗ". | Cao | Abnormal | F4, T2 · `PAY-STATE-001`, `PAY-ABANDON-001` | Screenshot **3 nơi** + log giao dịch gateway |
| **NEW-08** | **Salon có bill tiền** (`createOrderPayment`) — arbiter chạy **trước** charge? | Salon calendar **có** bill tiền. Slot/nhân viên còn 1 chỗ. 2 user A/B. | 1. Chạy race qua luồng `paymentStripe` / `paymentUnivapay`.<br>2. Đối chiếu 3 nơi như NEW-07.<br>3. Kiểm **thứ tự** trong log: arbiter reject **trước** hay **sau** lệnh charge. | User thua bị **reject trước khi charge** (không phát sinh giao dịch nào ở gateway).<br>⚠️ Report Dev **tự mâu thuẫn** về việc Salon paid đã có arbiter chưa → **bắt buộc chốt với Dev trước khi chạy TC này**. | Cao | Abnormal | F6, T3, D2 · `PAY-STATE-001` | Screenshot 3 nơi + **log thứ tự** arbiter vs charge |
| **NEW-09** | **Admin duyệt 2 request booking** tại slot remain = 1 (race dời sang tầng admin) | Calendar setting **request booking** (承認制). Slot remain = 1. 2 request đang chờ duyệt (từ TC007/TC020). | 1. Admin 1 (web) và Admin 2 (**app admin**) bấm **duyệt 2 request đồng thời**.<br>2. Query DB. | Chỉ **1** request được chuyển `APPROVE`; request còn lại bị chặn với thông báo hết chỗ (không được duyệt cả 2). | Cao | Boundary | T1, T3, D1 · `CONC-001` kịch bản 3, `MAP-SEND-19`, `SYNC-APP-001` | Query DB + screenshot web + app admin |
| **NEW-10** | **ADMIN_BOOK** vs user tự đặt **cùng giây** — arbiter chỉ nhận diện `APPROVE` | Slot remain = 1. | 1. Admin đặt hộ khách (tạo booking `ADMIN_BOOK`, status 2) **cùng giây** với lúc user A tự đặt (`APPROVE`).<br>2. Query DB đếm booking chiếm chỗ. | Tổng booking chiếm chỗ = **1** (không vượt giới hạn).<br>⚠️ Theo mô tả fix, arbiter **chỉ so bản `APPROVE` khác** → TC này nhiều khả năng **FAIL**. Nếu fail → escalate: arbiter phải xét cả `ADMIN_BOOK`. | Cao | Abnormal | F1, D1, D3 · `CONC-001` kịch bản 3 | Query DB (status 1/2/5) trước-sau |
| **NEW-11** | Giới hạn theo **NGÀY** (`1日の受付枠 = 1`) — 2 user đặt **2 khung giờ khác nhau cùng ngày**, đồng thời | Lesson calendar set **số khung tiếp nhận / ngày = 1** (đúng cấu hình KH, calendar_id 10955). Ngày X có ≥ 2 khung giờ trống. | 1. User A đặt khung **10:00**, user B đặt khung **14:00** — **bắn đồng thời cùng giây**.<br>2. Query DB đếm booking **theo ngày**. | Chỉ **1** booking trong ngày X.<br>⚠️ Arbiter chỉ so **cùng khung** → TC này nhiều khả năng **FAIL** → nếu fail, **bug gốc của KH chưa được fix** (xem BLOCKER-1). **Chạy TC này TRƯỚC khi báo KH đã fix xong.** | Cao | Boundary | BUG, F1, F2 · `CONC-001`, `FUNC-004` | Query DB theo ngày + screenshot màn setting của KH |
| **NEW-12** | **Regression — Booking Event**: chức năng tương tự có dính cùng pattern check-then-act không? | Booking Event có giới hạn số chỗ, còn **1 chỗ**. 2 user A/B. | 1. Bắn 2 request đặt event **đồng thời cùng giây**.<br>2. Query DB. | Chỉ **1** booking được tạo.<br>⚠️ Nếu **cả 2** thành công → Booking Event **cũng dính bug gốc**, chưa được fix → tạo ticket riêng. | Cao | Regression | `REG-SHARED-001` (cặp Lesson / Salon / Booking Event) | Query DB + danh sách nơi ảnh hưởng do **Dev cung cấp** |
| **NEW-13** | **Hủy + đặt mới đồng thời** tại slot đầy (`REQUEST_CANCEL` vẫn chiếm chỗ) | Slot đã đầy (remain = 0), có 1 booking của user A. | 1. A bấm **hủy** đúng lúc user B bấm **đặt** (đồng thời, cùng giây).<br>2. Query DB đếm booking chiếm chỗ (status 1, 2, 5). | Không over-book: hoặc B bị báo hết chỗ (nếu hủy chưa hoàn tất), hoặc B đặt được **sau khi** A hủy xong — **không bao giờ** ra 2 booking chiếm chỗ. `total_booking` khớp số thật. | Cao | Boundary | F3, D1, D3, T1 · `CONC-001`, `STATE-DEP-001` | Query DB status 1/2/5 trước-sau + log 2 request |
| **NEW-14** | Chạy lại kịch bản race **trên PRODUCTION** (2 app server loadbalance) — RULE-08 | Production (`step.lme.jp`), calendar test riêng, slot remain = 1. | 1. Bắn 2 request đồng thời, **ghi lại router id / server id** của từng request (đảm bảo rơi vào **2 server khác nhau**).<br>2. Query DB. | Chỉ **1** booking.<br>⚠️ Không có lock → 2 process trên 2 server có thể cùng query không thấy nhau. Nếu fail trên production dù pass trên staging → đúng cảnh báo `ENV-LB`. | Cao | Boundary | T1, T2, T3 · `ENV-003`, `ENV-001`, RULE-08 | Log **router id** của 2 request + query DB **trên production** |
| **NEW-15** | **Salon** — giới hạn theo **nhân viên** và case **season** (fail-safe im lặng) | Salon có `calendar_salon_setting_limit_booking` theo **nhân viên**; thêm 1 cấu hình có **giới hạn theo mùa (season)**. | 1. Case A: 2 user đặt **cùng nhân viên, cùng giờ**, đồng thời → query DB.<br>2. Case B: calendar có **season limit** → 2 user đặt đồng thời → query DB. | Case A: chỉ 1 booking.<br>Case B: theo Dev, arbiter **bỏ qua** khi không tra được giới hạn season → **dự kiến over-book**. Nếu đúng → đây là **known limitation**, phải ghi vào Redmine và báo KH, **không được đóng ticket im lặng**. | Cao | Abnormal | F6, D4, T3 · `CONC-001`, `PAY-LIMIT-001` | Query DB + ảnh cấu hình limit (nhân viên / season) |
| **NEW-16** | **Đối chứng false-positive**: N user đặt cùng giây tại slot còn **đủ chỗ** → arbiter KHÔNG được xóa ai | Slot remain = **3**. 3 user A/B/C. | 1. Bắn 3 request đặt **đồng thời cùng giây**.<br>2. Query DB đếm booking + `total_booking`. | **Cả 3** booking tồn tại (arbiter chỉ xóa khi **đã đủ giới hạn**). `total_booking` = 3. Không ai nhận nhầm thông báo "hết chỗ". | Cao | Normal | F1, F3, D1, D3 · `CONC-001`, `DATA-DB-001` | Query DB + screenshot 3 LINE app |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ spec / xác nhận với Dev + PM** (chặn round 2):
  1. **Ngữ nghĩa `1日の受付枠`** — giới hạn **số chỗ trong 1 khung** hay **số booking trong 1 ngày**? (BLOCKER-1 / NEW-11). Người chịu trách nhiệm: **Dev + CS xác nhận với KH**.
  2. **Request booking (承認制)**: request **chưa chiếm chỗ** là hành vi đúng spec? Khi admin duyệt vượt giới hạn thì xử lý ra sao? (NEW-09). Người chịu trách nhiệm: **PM**.
  3. **1 LINE user đặt được mấy chỗ trong 1 khung?** (NEW-03). Người chịu trách nhiệm: **PM**.
  4. **Known limitation cần ghi vào spec/Redmine nếu TC xác nhận**: (a) race lệch ranh giới giây; (b) Salon season limit fail-safe bỏ qua; (c) không có lock → khe race trên production 2 server. Người chịu trách nhiệm: **Dev + Leader**.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 RISK · A.2 RISK (F3/F5 GAP) · A.3 **FAIL** (D1/D2/D3 GAP — 0 TC verify DB) · A.4 RISK · A.5 OK (không orphan) · A.6 **FAIL** (fix-shape 1/4 trigger)
- [x] **B. Chất lượng từng TC** — B.1 **FAIL** (Steps "2 user nhấn cùng lúc" không tái lập được; Expected không đo lường được ở tầng DB) · B.2 OK · B.3 OK · B.4 OK
- [x] **C. Chất lượng bộ TC** — **FAIL**: 0 TC Boundary; Type/Priority trống; Lesson và Salon trùng lặp nguyên bộ
- [x] **D. Spec alignment** — **RISK**: không có `02-spec-reference.md`; 3 điểm spec chưa rõ (xem §6)
- [x] **E. Hành chính** — **RISK**: thiếu 4/10 cột chuẩn; range Redmine lệch 1 dòng; tester/version có ghi
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — mở **C** (MAP-PAY-01 luồng lesson/salon, MAP-PLAN-04/05 race tại ngưỡng, MAP-SEND-19 duyệt booking từ app, MAP-CANCEL) + **D/D2** (ENV-LB 2 server, ENV-JOB, JOB-03 callback trùng) — **member chưa mở catalog nào**
  - [x] F.3 RULE — **RULE-01 FAIL** · **RULE-02 FAIL** · RULE-03 N/A (không có bảng ×) · **RULE-06 FAIL** · **RULE-07 FAIL** · **RULE-08 FAIL** · RULE-09 N/A · RULE-12 RISK (chưa có danh sách vùng ảnh hưởng từ Dev)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `CONC-001` — 1 hành động chỉ xử lý 1 lần | **Cao** | ◯ — **quan điểm trung tâm** của task | TC004/005/017/018 (chỉ kịch bản 4) | **RISK → BLOCKER** — thiếu kịch bản 1, 2, 3; evidence không phải log/DB |
| `DATA-DB-001` — WHERE scope + xác minh tầng DB | **Cao** | ◯ — fix có **DELETE** + **UPDATE** | — | **GAP** → BLOCKER |
| `PAY-STATE-001` — nhất quán trạng thái 3 nơi | **Cao** | ◯ — nhánh "có setting bill tiền" (Lesson + Salon) | TC008–013, TC021–026 (chỉ UI) | **RISK → BLOCKER** — không đối chiếu gateway, không verify "không trừ tiền" |
| `REG-SHARED-001` — shared code / chức năng tương tự | **Cao** | ◯ — Dev đã tự nhân bản fix sang Salon | TC014–026 (Salon) | **RISK → BLOCKER** — thiếu **Booking Event**; chưa có danh sách vùng ảnh hưởng từ Dev |
| `ENV-003` / RULE-08 — khác biệt staging vs production | **Cao** | ◯ — bill tiền + **loadbalance 2 server** | — (26/26 chỉ staging) | **GAP** → MAJOR |
| `STATE-001` — quy trình nhiều bước bị gián đoạn | **Cao** | ◯ — tạo booking → (side-effect) → xóa bản dư | — | **GAP** → BLOCKER (NEW-06) |
| `STATE-DEP-001` — hành động phụ thuộc khi gốc đổi | **Cao** | ◯ — booking bị xóa nhưng remind/action đã lên lịch | — | **GAP** → BLOCKER (NEW-06) |
| `DATA-COUNT-001` — số đếm & tổng hợp | **Cao** | ◯ — `total_booking` được **đếm lại** | — | **GAP** → MAJOR |
| `OUT-TRUTH-001` — UI khớp trạng thái thật | **Cao** | ◯ — nguy cơ **false success** (báo đặt thành công rồi booking bị xóa) | TC004/005 (một nửa) | **RISK** → gộp vào NEW-06 |
| `ENV-001` — fail-safe khi sự cố hạ tầng | **Cao** | ◯ — "bước validate slot chạy qua nhiều server" (đúng nguyên văn trigger) | — | **GAP** → MAJOR (NEW-14) |
| `FUNC-004` — giới hạn trên/dưới | **Cao** | ◯ — giới hạn số chỗ / số khung / ngày | TC001–003 (remain ∞/2/1) | **RISK** — thiếu biên: remain = 0, limit±1, giới hạn **theo ngày** |
| `INTG-CAL-001` — đồng bộ 2 chiều Google Calendar | **Cao** | ◯ — booking bị xóa sau khi đã sync? | — | **GAP** → gộp NEW-06 |
| `DATA-001` — cập nhật phản ánh ở mọi màn | **Cao** | ◯ | TC004/005 (chỉ màn LINE user) | **RISK** — thiếu màn admin `Today&NewBooking`, app admin |
| `SYNC-APP-001` — web ⇔ app admin | Trung bình → **Cao** | ◯ — duyệt/từ chối booking lesson & salon có trên **app admin** (MAP-SEND-19) | — | **GAP** → MAJOR (NEW-09) |
| `PAY-LIMIT-001` — giới hạn theo gói | **Cao** | ◯ (một phần) — MAP-PLAN-04/05: 2 tab + double-click tại ngưỡng | — | **GAP** → gộp NEW-02/NEW-03 |
| `PERF-LARGE-001` | Trung bình | × — fix không đổi truy vấn danh sách | — | × (lý do: không chạm luồng list/export) |
| `MEDIA-*`, `LIFF-ENTRY-001`, `MSG-001` | Cao | × — fix nằm ở tầng server `order()`, không chạm media / entry link / filter gửi tin | — | × (ghi lý do — RULE-03) |
| `COMPAT-LEGACY-001` | Cao | × — không có version-up dữ liệu trong fix này | — | × (lý do: fix không đổi schema/format) |
| `DEPLOY-ASSET-001` | Cao | × — không sửa JS/CSS/asset (chỉ 2 file PHP controller) | — | × |

> **Tổng kết F.1**: 7 quan điểm **Cao** ở trạng thái **GAP** (`DATA-DB-001`, `STATE-001`, `STATE-DEP-001`, `DATA-COUNT-001`, `ENV-003`, `ENV-001`, `SYNC-APP-001`) + 4 quan điểm **Cao** ở trạng thái **RISK nặng** (`CONC-001`, `PAY-STATE-001`, `REG-SHARED-001`, `FUNC-004`).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
