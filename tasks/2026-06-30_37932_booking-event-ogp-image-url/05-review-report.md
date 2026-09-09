# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37932 — [Booking Event] OGP画像 của URL đặt lịch sự kiện (イベント予約URL)` |
| Reviewer (Leader) | `<Test Leader>` |
| Tester được review | `Thanh Phương` (assigned: Ngô Thúy Ngần) |
| Ngày review | `2026-06-30` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (không có `02-spec-reference.md` riêng cho task này) + checklist-lme §C (Booking Event không có sheet C riêng → base §A function + §D UI).
> **Nguồn file 04**: TCs fetch từ Redmine Link TCs (Google Sheet "Task nhỏ + fix bug KH", row 202~214) — không phải `/write-tc` sinh.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần fix và review lại.

**Lý do ngắn gọn**: Cách fix để `og:image = RỖNG` (không phải set ảnh tiêu đề làm OGP), nhưng **không TC nào tái hiện đúng kịch bản gốc** (event có ảnh nhúng trong nội dung → FB nhặt nhầm) cũng như **không verify ảnh OGP cuối cùng hiển thị gì**. Expected của TC001 quá mơ hồ ("không hiện ảnh American Express") trong khi rủi ro FB fallback scrape HTML khi `og:image` rỗng chưa được loại trừ. Thêm: 2 file input auto-fill chưa được tester verify.

---

## 2. Tóm tắt cho member

Bộ TC bao quát **kênh chia sẻ** rất tốt (Facebook / LINE / Email / Messenger) và có nghĩ tới biến thể nội dung (title dài, description dài, ký tự Nhật, emoji) — đây là điểm mạnh. Tuy nhiên bộ TC đang **test triệu chứng chứ chưa test đúng root cause**: bug gốc là event có **ảnh nhúng trong HTML/nội dung** bị FB nhặt làm OGP, nhưng không TC nào dựng lại event như vậy, và Expected mới chỉ ghi "không hiện ảnh American Express" mà chưa khẳng định **ảnh OGP cuối cùng là gì** (rỗng? hay ảnh tiêu đề?). Cần (1) tái hiện đúng kịch bản embedded-image, (2) chốt expected ảnh OGP với Dev/CSS, (3) phân biệt event **1 ngày vs nhiều ngày**, và (4) thêm TC cho **FB cache** (Sharing Debugger). Yêu cầu tester tick 2 checkbox verify auto-fill trước khi review có giá trị pháp lý.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — event share hiển thị ảnh sai (thiếu/empty og:image) | Fix | — | TC001, TC002, TC003, TC004 | 4 | **RISK** — chỉ test "không ra ảnh sai" trên event thường; chưa dựng event có ảnh nhúng (đúng root cause); expected mơ hồ |
| F1 — `MobileEventBookingController::index` (nhánh crawler UA) | Function | Direct | TC001–TC008, TC011, TC013 (nhánh crawler) · TC009, TC010, TC012 (nhánh user thật) | 13 | **RISK** — cover cả 2 nhánh nhưng không TC nào verify **UA detection** chọn đúng nhánh (crawler vs real user) |
| D1 — (không có data) | Data | — | N/A | — | N/A (Dev xác nhận không đụng DB) |
| T1 — OGP preview khi share URL đặt lịch sự kiện | Feature | Medium | TC001–TC008, TC011, TC013 | 11 | **RISK** — thiếu verify ảnh OGP đúng + thiếu phân biệt event 1 ngày / nhiều ngày |
| T2 — Luồng user thật mở URL & booking (regression nhánh crawler) | Feature | Medium | TC009, TC010, TC012 | 3 | **OK** — có TC user mở url + booking + refresh |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề — toàn bộ 13 TC đều thuộc scope BUG / F1 / T1 / T2 | Giữ nguyên |

> Lưu ý mơ hồ (KHÔNG tự đoán): nhiều TC có cột **Expected để trống** (TC002, TC004, TC006, TC007, TC008, TC012) — chỉ suy được mục đích từ Title. Đề nghị member điền Expected đo lường được (xem §4.2).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Conditional branch addition** — thêm nhánh `if (crawler UA)` → render meta OGP nhẹ (`preview_url`) với `og:title` + `og:description`, **`og:image = '' (RỖNG)`**. Không phải generic catch / validation / race / migration. |
| Trigger space cần cover | (1) Crawler UA của từng kênh: **facebookexternalhit** (FB), **LINE bot preview**, **Messenger**, **email client crawler**, (X/Twitterbot nếu trong scope). (2) Loại event: **1 ngày** (`MobileEventBookingController` — được fix) vs **nhiều ngày** (`BookingEventController` — KHÔNG đụng). (3) Trạng thái ảnh: event **có ảnh nhúng trong nội dung** / **có ảnh tiêu đề** / **không có ảnh** / **FB đã cache ảnh cũ**. |
| Số trigger TCs hiện cover | **Kênh: 4/4** (TC001-004) · **Loại event: 0/2** (không phân biệt 1 ngày/nhiều ngày) · **Trạng thái ảnh: 0/4** (không TC nào dựng event có ảnh nhúng / không ảnh tiêu đề / cache) · **UA detection: 0** (không verify chọn đúng nhánh) |
| KH report dạng | **Symptom-only** — KH chỉ thấy "hiển thị ảnh American Express khi share", không nêu root cause. Dev tái hiện 1 root cause (thiếu og:image → FB nhặt ảnh HTML). |
| Alternative root causes cần verify | (1) **FB cache** giữ ảnh scrape cũ (Dev tự nhận trong "Rủi ro khi test"). (2) **`og:image` rỗng vẫn để FB fallback nhặt ảnh trong body HTML** → ảnh AmEx (nằm trong nội dung email/content) có thể VẪN xuất hiện. (3) Ảnh nhúng nằm ở nội dung event chứ không phải header. |
| Anti-patterns dính | **AP-2** (symptom-only, alt root cause chưa cover), **AP-4** (không có PR diff link → không verify được UA matching & og:image thực sự rỗng), **AP-3** (regression T1/T2 thiên happy-path) |

> ⚠️ **Điểm adversarial quan trọng nhất**: `og:image=''` chỉ **bỏ thẻ ảnh**, KHÔNG cung cấp ảnh hợp lệ để override. Khi không có `og:image` hợp lệ, Facebook thường **fallback scrape ảnh trong HTML body** → đúng cơ chế gây bug ban đầu (ảnh AmEx trong nội dung). Nếu trang `preview_url` vẫn render nội dung event có ảnh → bug có thể **chưa được fix triệt để**. → flag [BLOCKER] FIX-SHAPE trong §4.1, bắt buộc 1 TC dựng event có ảnh nhúng trong nội dung.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-1**: Không TC nào **tái hiện đúng root cause** — event có **ảnh nhúng trong nội dung/mô tả** (như ảnh AmEx của KH). Fix để `og:image=''` (rỗng) chỉ bỏ thẻ ảnh, không chắc chặn được FB fallback scrape ảnh HTML body → bug có thể chưa fix triệt để. **Fix**: thêm TC-NEW-01 (dựng event mô tả chứa ảnh, share FB, verify preview KHÔNG nhặt ảnh nhúng).
- **[BLOCKER] GAP-2 — Expected mismatch**: TC001 Expected = "không hiện ảnh American Express" + "đúng title/description" nhưng **KHÔNG verify ảnh OGP cuối cùng hiển thị gì**. CSS đã trả lời KH rằng **ảnh tiêu đề (ヘッダー画像) sẽ là ảnh OGP**, trong khi Dev để `og:image` RỖNG (không ảnh). Đây là **mâu thuẫn behavior** giữa cam kết với KH và cách fix. **Fix**: chốt expected với Dev/CSS (preview "không ảnh" hay "ảnh tiêu đề") → cập nhật Expected TC001 + thêm TC-NEW-02. Xem §6 Spec update.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify — file 01**: `01-bug-task.md` auto-filled `2026-06-30 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Review chỉ có giá trị sau khi tester đọc lại detail Redmine #37932 và tick. **Fix**: tester verify + tick.
- **[MAJOR] AUTO-FILL chưa verify — file 03**: `03-dev-impact.md` auto-filled `2026-06-30 by /new-task`, checkbox **CHƯA tick** → F/D/T có thể chưa đầy đủ hoặc mapping sai. **Fix**: tester verify + tick trước khi chốt coverage.
- **[MAJOR] FIX-SHAPE — GAP-3 (event 1 ngày vs nhiều ngày)**: Fix chỉ đụng `MobileEventBookingController` (event **1 ngày**); event **nhiều ngày** (`BookingEventController::getInfoEventBookingUrl`) dùng controller khác và theo ghi chú kỹ thuật đã có sẵn `BEventDetail.image` làm OGP. TCs **không phân biệt loại event** → coverage mơ hồ + bỏ lọt khả năng 2 loại hành vi khác nhau. **Fix**: TC-NEW-03 (share event nhiều ngày, đối chiếu OGP với event 1 ngày).
- **[MAJOR] SYMPTOM-ONLY (AP-2) — FB cache**: Dev tự ghi rủi ro "FB cache ảnh cũ → cần Sharing Debugger để refresh". Không TC nào cover. KH có thể vẫn thấy ảnh AmEx do cache dù fix đúng. **Fix**: TC-NEW-05 (dùng FB Sharing Debugger scrape lại URL đã share trước fix → verify ảnh cập nhật).
- **[MAJOR] GAP-4 — UA detection branch**: Fix thêm nhánh `if(crawler UA)`. Không TC nào verify **nhánh chọn đúng**: user thật (browser UA) phải vào trang booking đầy đủ, crawler (`facebookexternalhit`) phải nhận `preview_url`. TC009/010 chỉ verify user mở được — chưa khẳng định user thật KHÔNG nhận trang preview rỗng. **Fix**: TC-NEW-06.
- **[MAJOR] AP-4 — thiếu PR diff link**: Mục "Commit / Pull Request" chỉ có branch `ai_fixbug_37932` + commit hash, **không có URL PR/diff** để review verify (UA match logic, og:image có thực sự rỗng, preview_url render gì). **Fix**: yêu cầu Dev cung cấp link diff hoặc Leader checkout branch verify code trước khi chốt.
- **[MAJOR] GAP-5 — event không có ảnh tiêu đề / event disable**: TC001 có precondition note "Check case event **disable** bill tiền" nhưng không có TC độc lập. Thiếu boundary: event **chưa set ảnh tiêu đề**, event **disable / đã kết thúc / private** → OGP hiển thị gì, có lỗi/lộ thông tin không. **Fix**: TC-NEW-04 + TC-NEW-07.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Expected để trống**: TC002, TC004, TC006, TC007, TC008, TC012 cột Expected trống — chỉ suy mục đích từ Title. Đề nghị điền Expected đo lường được (vd TC002: "Preview trong LINE talk/timeline hiển thị đúng title+description, không ảnh sai").
- **[MINOR] Thiếu cột Type/Priority**: Toàn bộ 13 TC trống Type & Priority (do fetch từ sheet). Đề nghị gán để cân đối Positive/Negative/Boundary/Regression (hiện gần như 100% positive).
- **[MINOR] Compatibility (CL-NonF-1 / TC-14)**: TC009 "các môi trường khác nhau" mơ hồ — nên ghi rõ ma trận: LINE app iOS / Android / PC, FB app vs web. OGP preview phụ thuộc nền tảng render.

### 4.4 Nit (gợi ý)

- **[NIT] TC-25 (LINE/FB spec ảnh OGP)**: Nếu chốt hiển thị ảnh tiêu đề làm OGP → thêm TC verify ảnh đúng kích thước/format khuyến nghị FB/LINE (vd 1200×630), tránh ảnh bị crop xấu.
- **[NIT] TC011 "share nhiều event liên tiếp"**: gợi ý ghi rõ verify mỗi URL ra đúng OGP **của chính event đó** (không cache lẫn giữa các event) — chạm AP cache.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Test trên **Staging** trừ khi ghi khác. Lưu ý FB cache → dùng **Sharing Debugger** (developers.facebook.com/tools/debug) để force re-scrape.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Share URL event 1 ngày có **ảnh nhúng trong nội dung** → preview không nhặt ảnh nhúng | Có event booking **1 ngày**; phần mô tả/nội dung event có **chèn 1 ảnh bất kỳ** (mô phỏng ảnh AmEx); chưa từng share URL này (chưa cache) | 1. Lấy URL đặt lịch event (liff.line.me/...). 2. Dán URL vào FB Sharing Debugger → Scrape. 3. Share URL lên Facebook & Email | Preview **KHÔNG** lấy ảnh nhúng trong nội dung làm OGP. Title/description đúng tên event. (Nếu spec yêu cầu ảnh tiêu đề → hiện ảnh tiêu đề; nếu spec "không ảnh" → không ảnh) | High | Negative | BUG, F1 |
| TC-NEW-02 | Verify ảnh OGP cuối cùng của event 1 ngày = đúng theo spec đã chốt | Event 1 ngày **đã set ảnh tiêu đề (ヘッダー画像)** | 1. Share URL lên FB/LINE/Email. 2. Quan sát ảnh trong preview | Theo expected đã chốt với Dev/CSS: **(A)** hiện đúng ảnh tiêu đề, HOẶC **(B)** không hiện ảnh nào (xác nhận `og:image` rỗng là chủ đích). KHÔNG để mơ hồ | High | Positive | BUG, T1 |
| TC-NEW-03 | Đối chiếu OGP: event **nhiều ngày** vs **1 ngày** | Có 1 event **nhiều ngày** (`BookingEventController`) + 1 event **1 ngày**, cùng set ảnh tiêu đề | 1. Share URL của cả 2 lên FB. 2. So sánh ảnh/title/description preview | Cả 2 loại hiển thị OGP **nhất quán** theo spec. Nếu khác nhau → ghi rõ và xác nhận với Dev là chủ đích | High | Regression | T1 |
| TC-NEW-04 | Share URL event **chưa set ảnh tiêu đề** | Event 1 ngày **không có** ảnh tiêu đề | 1. Share URL lên FB/LINE | Preview không lỗi; ảnh OGP = rỗng/placeholder theo spec; không nhặt ảnh rác từ HTML | Medium | Boundary | BUG, T1 |
| TC-NEW-05 | FB cache — re-scrape URL đã share trước fix | URL event đã từng share & FB đang cache ảnh AmEx (trước fix) | 1. Mở FB Sharing Debugger với URL đó. 2. Bấm "Scrape Again". 3. Share lại | Sau re-scrape, ảnh cập nhật theo fix mới, **không còn ảnh AmEx cũ**. Ghi chú: KH cần re-share/đợi cache | Medium | Regression | BUG (cache) |
| TC-NEW-06 | UA detection — user thật vs crawler nhận đúng trang | Event 1 ngày bất kỳ | 1. Mở URL bằng **trình duyệt thật / LINE app** (user). 2. Mở URL bằng UA `facebookexternalhit` (crawler, vd qua Debugger/curl) | User thật → vào **trang đặt lịch đầy đủ** (booking được). Crawler → nhận **preview_url** (trang meta OGP nhẹ), không phải trang booking | High | Negative | F1 |
| TC-NEW-07 | Share URL event **disable / đã kết thúc / private** | Event 1 ngày ở trạng thái disable hoặc đã hết hạn | 1. Share URL lên FB. 2. Mở URL bằng crawler & user | Preview không lỗi, không lộ thông tin ngoài ý muốn; user mở thấy đúng trạng thái (đã kết thúc/không khả dụng) | Medium | Negative | F1, T1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ spec/expected** — chi tiết:
  - **Section**: Booking Event — OGP của URL đặt lịch sự kiện (イベント予約URL).
  - **Nội dung cần làm rõ**: Có **mâu thuẫn** giữa câu trả lời CSS gửi KH ("ảnh OGP = ảnh tiêu đề ヘッダー画像, đổi header để đổi OGP") và cách fix thực tế của Dev (`og:image = '' RỖNG` cho event 1 ngày). Cần chốt: **ảnh OGP của event 1 ngày là ảnh tiêu đề hay không có ảnh?** Và có đồng bộ với event nhiều ngày (đang dùng `BEventDetail.image`) không? Quyết định này ảnh hưởng trực tiếp Expected của TC001 / TC-NEW-02 / TC-NEW-03.
  - **Người chịu trách nhiệm**: Dev (`AI LME Fix bug` owner) + CSS (người đã trả lời KH) + Test Leader xác nhận trước khi member viết lại Expected.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 (BUG: RISK), A.2 (F1: RISK), A.3 (N/A no data), A.4 (T1 RISK, T2 OK), A.5 (no orphan), A.6 fix-shape (xem §3.5)
- [x] B. Chất lượng từng TC — B.1 nhiều Expected trống (MINOR), B.2 atomic OK, B.3 độc lập OK, B.4 realistic OK
- [x] C. Chất lượng bộ TC — tỷ lệ lệch (gần 100% positive, thiếu negative/boundary), thiếu Priority
- [x] D. Spec alignment — phát hiện mâu thuẫn (xem §6)
- [x] E. Hành chính — TC ID đánh số tự động (sheet gốc trống), version v1 OK
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — liên quan: CL-Func-21 (format JP, TC007/008 cover OK), CL-Func-22 (upload ảnh tiêu đề — marginal), A.2 Compatibility (TC-14 cross-platform — RISK, MINOR §4.3), TC-25 (spec ảnh OGP — NIT)
  - [x] F.2 Checklist job — không chạm job/callback/google sync → N/A
  - [x] F.3 Các tính năng chung — Booking Event không có sheet C riêng; C.2 Send message KHÔNG liên quan (đây là render meta OGP, không gửi message). Không chạm Bill/Friend info/Tag/Sort.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
