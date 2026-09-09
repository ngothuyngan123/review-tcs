# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39507 — [TY-11824] [Booking Event] Lỗi khi test thanh toán event đặt chỗ 11/5-6SASALABO合宿` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `AI` (LME TEST STUDIO job #319 — 12 TC) + `thanhntp` (6 TC, và là người chạy toàn bộ 18 TC) |
| Ngày review | `2026-08-18` |
| Version TCs | Studio `round 1` (task #64) |
| Vòng review | `Round 1` |

> **Input dùng để review**: `01-bug-task.md` · `03-dev-impact.md` · `04-tc-list.md`.
> **Input thiếu**: không có `02-spec-reference.md` → *Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng, không có spec riêng cho task này.*
> **Input thiếu**: TC fetch từ Studio **không có Evidence** (API `testcase_list` không trả về) và **không có `spec_status`** → 2 chiều này không review được từ file, phải hỏi `thanhntp`.

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bản fix là **generic error-message handler** trên luồng **bill tiền**, nhưng nhánh code đã sửa chỉ được verify hợp lệ với **1 loại lỗi duy nhất** (`CHARGE_AMOUNT_TOO_HIGH`) — TC chứng minh "message bám theo mã lỗi" bị `skip`, TC unknown-fallback chỉ chạy ở `local` do pipeline AI submit. Ngoài ra **không TC nào đối soát bản ghi phía cổng UnivaPay** để chứng minh giao dịch thất bại không phát sinh charge (`PAY-STATE-001` + `ENV-PAY` bắt buộc), và **17 TC tick `Đạt` với Evidence rỗng** (RULE-02 → kết quả chưa được nghiệm thu).

---

## 2. Tóm tắt cho member

Bộ TC này **thiết kế rất tốt về mặt cấu trúc**: có TC trục chính tái hiện đúng bug (`TC-OUTTRUTH001-01`), có đối chứng âm cho nhánh không bật webhook, có regression đủ 3 tính năng anh em theo đúng danh sách Dev cung cấp, và note kỹ thuật của từng TC ghi rõ ranh giới phạm vi (không kỳ vọng 66.000 yên thanh toán thành công ở môi trường thử) — đây là điểm nhiều bộ TC khác thiếu.

Vấn đề lớn nhất **không nằm ở việc thiếu TC mà ở việc thiếu bằng chứng**: fix dạng "gán message theo mã lỗi" đòi hỏi ≥ 4 loại lỗi khác nhau + 1 mã lỗi lạ (§3 phụ lục `checklist-lme.md`), nhưng trên nhánh đã sửa hiện chỉ có **1 loại lỗi được người chạy verify ở staging**; TC lỗi thứ hai (`TC-FUNC004-01`) bị `skip` không ghi lý do, và TC mã lỗi lạ (`TC-TOOLERRHYG001-01`) chạy ở `local` do AI submit. Cộng thêm Evidence rỗng 18/18 và 0 TC production cho task bill tiền, kết quả "17/18 Đạt" hiện chưa đủ căn cứ để đóng ticket.

Việc cần làm: (1) chạy lại `TC-FUNC004-01` + `TC-TOOLERRHYG001-01` trên staging kèm ảnh chụp hộp thoại; (2) bổ sung 13 TC ở §5 (chủ yếu là các loại lỗi cổng thanh toán còn thiếu + đối soát dashboard UnivaPay); (3) gán `Mã quan điểm liên kết` cho 6 TC tự viết để coverage map được.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — nhánh `isProcessWithWebhook = true` quên gán nội dung thông báo lỗi → hộp thoại trắng | Fix | — | `TC-OUTTRUTH001-01` | 1 | **RISK** — đúng 1 TC, và chỉ với 1 mã lỗi (`CHARGE_AMOUNT_TOO_HIGH`). Xem §3.5 |
| **F1** — `MobileEventBookingController::payment`, nhánh chờ webhook (dòng 1102-1109) | Function | **Direct** | `TC-OUTTRUTH001-01`, `TC-FUNC004-01` (skip), `TC-TOOLERRHYG001-01` (local/AI), `TC-FUNC001-01`, `TC-INTGHOOK002-01`, `TC-TOOLNEGCTRL001-01`, `TC-INTGHOOK001-01` | 7 | **RISK** — đủ Normal/Abnormal/Boundary nhưng **thiếu chiều loại lỗi** (chỉ 1/10 error type §3 được verify hợp lệ) |
| **F2** — response JSON của endpoint thanh toán (message khác rỗng, cấu trúc key không đổi) | Function | **Direct** | `TC-APICONTRACT001-01` | 1 | **RISK** — 1 TC duy nhất, chạy ở `local`, `last_exec.source = ai`. Chưa có bằng chứng người chạy |
| **F3** — `order-item.js: payment` render hộp thoại (dòng 788-800) | Function | Indirect | `TC-OUTTRUTH001-01`, `TC-TOOLERRHYG001-01`, `TC-INTGHOOK001-01` | 3 | **OK** — có cả nhánh alert thứ nhất (không kèm trạng thái webhook) và nhánh thứ hai (kèm webhook status) |
| **D1** — *Dev khai "Không có data bị update"* | Data | — | — | — | **N/A** — không cần TC (đã xác nhận với mục 4.2 file 03) |
| **D2** — bản ghi đặt chỗ tạm bị xoá + số chỗ đã dùng của khung giờ được tính lại (hành vi cũ, fix không chạm) | Data | — | `TC-STATE001-01`, `TC-OUTTRUTH001-01`, `TC-FUNC004-01` (skip) | 3 | **RISK** — verify được DB + màn hình, nhưng **không có TC kiểm `WHERE` scope trên 2 tài khoản / 2 user cùng khung giờ** (RULE-07 · `DATA-DB-001`) |
| **T1** — Event Booking (FA-021) | Feature | **High** | `TC-FUNC001-01`, `TC-INTGHOOK002-01`, `TC-STATE001-01`, `TC-OUTTRUTH001-01`, `TC-FUNC004-01`, `TC-TOOLNEGCTRL001-01`, `TC-INTGHOOK001-01`, `TC-TOOLERRHYG001-01`, `TC-APICONTRACT001-01` | 9 | **OK** — có full happy path end-to-end (`TC-FUNC001-01` đi tới tin LINE hoàn tất đặt chỗ) |
| **T2** — Mua sản phẩm · Đặt lịch khoá học · Đặt lịch salon (dùng chung bảng dịch mã lỗi) | Feature | Low | `TC-REGSHARED001-01`, `-02`, `-03` | 3 | **OK** — đúng 1 TC/nơi theo danh sách Dev cung cấp (RULE-12). Xem `[AP-3]` ở §4.2 |
| **T3** — `MobileEventBookingController::changeBooking` (Dev khai **chưa sửa**, "lỗi khác — yokoten") | Feature | ⚠️ chưa đánh giá | `TC-NOVP-01`, `TC-NOVP-02`, `TC-NOVP-03` | 3 | **OK về số lượng** — nhưng cần Leader xác nhận scope (xem §4.2) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| `TC-NOVP-04` | Bill tiền stripe success có số tiền < hạn mức | Cổng **Stripe** — bản fix chỉ chạm nhánh **UnivaPay**; không map về BUG/F/D/T nào trong `03-dev-impact.md` | **Giữ** — coverage sibling gateway hợp lý (`REG-SHARED-001`). Nhưng phải **gán mã quan điểm** + ghi ở `Ghi chú` là "ngoài scope fix, chạy như regression" |
| `TC-NOVP-05` | Bill tiền stripe success có số tiền = hạn mức | như trên | **Giữ** + gán mã quan điểm. Đây thực chất là case **Boundary** — phải điền `Loại case = Boundary` |
| `TC-NOVP-06` | Bill tiền stripe success có số tiền > hạn mức | như trên | **Giữ** + gán mã quan điểm + **sửa tiêu đề** (ghi "success" nhưng kết quả mong đợi là lỗi) |

> Không có TC nào cần **remove**. 3 TC Stripe là over-coverage nhẹ (`[AP-5]`) nhưng có giá trị đối chứng — chỉ cần gắn nhãn đúng.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Generic catch-all** — nguyên văn: *"khi tạo giao dịch UnivaPay thất bại thì **lấy thông báo lỗi đã dịch sẵn theo mã lỗi** rồi trả về cho màn hình, thay vì trả chuỗi rỗng"* + *"Thêm một dòng ghi log lỗi"*. Keyword khớp: `set error message` / `return error` / `fallback message`. Bảng ánh xạ `getMessageErrorUnivapay` có nhánh cuối trả **chính chuỗi lỗi gốc** khi mã lỗi không khớp ⇒ đúng dạng generic có fallback |
| **Trigger space cần cover** | §3 Phụ lục `checklist-lme.md` — **≥ 4 error type + 1 unknown fallback**: `card_declined` · `insufficient_funds` · `expired_card` · `three_ds_failed` · `amount_exceeded` ✅ · `amount_too_small` · `network timeout / API 5xx` · `unknown error code` · `duplicate transaction` · `account suspended` |
| **Số trigger TCs hiện cover** | **1 / 10 hợp lệ** (chỉ `amount_exceeded` — `TC-OUTTRUTH001-01`, staging, người chạy).<br>3/10 trên danh nghĩa: `amount_too_small` (`TC-FUNC004-01` — **`skip`, không kết quả**) · `unknown code` (`TC-TOOLERRHYG001-01` — **`local`, `source = ai`**).<br>⚠️ `CARD_PROCESSING_DISABLED` (`TC-INTGHOOK001-01`) **KHÔNG tính** — chạy ở nhánh webhook-báo-lỗi (dòng 1115-1140), **không phải nhánh đã sửa** (1102-1109).<br>⚠️ `card_declined` có test ở `TC-NOVP-03` nhưng trên màn **change booking** — cũng không phải nhánh đã sửa |
| **KH report dạng** | **Symptom-only** — nguyên văn KH: *「イベント予約でテスト決済をしようとするとエラーが表示される」* (chỉ nói "hiển thị lỗi", không có mã lỗi / message). Dev khoanh được root cause **từ log production 2026-08-06 17:04:20**, không phải từ mô tả của KH |
| **Alternative root causes cần verify** | (a) **Mã lỗi khác cùng nhánh** → cũng cho hộp thoại trắng (declined / expired / 3DS / timeout);<br>(b) **`changeBooking`** — Dev khai có "lỗi khác chưa sửa";<br>(c) **Cổng Stripe** — nhánh xử lý riêng, chưa được Dev đối chiếu;<br>(d) ⚠️ **Request không tới handler**: J#128666 ghi *"kiểm tra log ngày 8/7・8/8 **không tìm thấy log xử lý đặt lịch** tương ứng"* trong khi KH khẳng định vẫn lỗi — bản fix chỉ thêm log ở nhánh **có chạy tới**; nếu có failure mode không sinh log thì fix này không chạm tới |
| **Anti-patterns dính** | **AP-1** ✅ (single-trigger generic-fix) · **AP-2** ✅ (symptom-only KH report) · **AP-3** ⚠️ (regression T2 chỉ 1 TC/nơi, precondition không có edge state) · **AP-4** ⚠️ (không có link PR/diff để verify fix là generic hay `if (code === X)`) · **AP-5** ⚠️ nhẹ (3 TC Stripe ngoài code path) · **AP-6** ❌ không dính (mục 3 file 03 list đủ 9 caller) |

> Trigger space cover **1/10** < tổng ⇒ flag `[BLOCKER] FIX-SHAPE` ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / [AP-1] GAP-1 — nhánh đã sửa chỉ được verify với 1 loại lỗi**: fix là generic error-message handler ở `MobileEventBookingController::payment` (dòng 1102-1109), nhưng trên **chính nhánh đó** chỉ có `TC-OUTTRUTH001-01` (`CHARGE_AMOUNT_TOO_HIGH`) được người chạy verify ở staging. `TC-FUNC004-01` (`CHARGE_AMOUNT_TOO_LOW`) **`skip` không ghi lý do**; `TC-TOOLERRHYG001-01` (unknown code) chạy ở **`local` với `source = ai`**. Các TC còn lại (`TC-INTGHOOK001-01`, `TC-TOOLNEGCTRL001-01`, `TC-NOVP-03`) đều nằm ở **nhánh code khác**. — **Fix**: bổ sung 4 TC error type theo §3 phụ lục (`TC-PAYSTATE001-04` → `-07` ở §5) + **chạy lại** `TC-FUNC004-01` và `TC-TOOLERRHYG001-01` trên `STAGING` do người chạy, kèm ảnh chụp hộp thoại. Nếu môi trường sandbox không trigger được 1 mã lỗi nào → ghi rõ mã đó + lý do vào `Ghi chú`, **không để `skip` trống**.

- **[BLOCKER] GAP-2 — `PAY-STATE-001`: không TC nào đối soát bản ghi phía cổng UnivaPay**: `PAY-STATE-001` (**Cao**, trigger *"BẮT BUỘC với mọi chức năng có giao dịch tiền"*) yêu cầu sau **mỗi** kịch bản phải mở **3 nơi** — admin nội bộ / màn user / **dashboard cổng thanh toán** — đối chiếu tên gói + trạng thái + số tiền, và *"thất bại thì **không trừ tiền**"*. Catalog `ENV-PAY` cũng ghi rõ *"**Đối soát với bản ghi của cổng thanh toán** sau mỗi release chạm luồng tiền"*. **18/18 TC chỉ verify DB + màn hình**, không TC nào mở dashboard UnivaPay. Đây đúng là câu hỏi KH đã đặt ở J#129042 (*"dù là thanh toán test thì hạn mức UnivaPay vẫn bị trừ phải không?"*) và hiện **không có TC nào trả lời được**. — **Fix**: thêm `TC-PAYSTATE001-01/-02/-03` ở §5 (RULE-01: đủ Normal + Abnormal + Boundary), Evidence bắt buộc = screenshot 3 nơi + log giao dịch.

### 4.2 Major (nên fix)

- **[MAJOR] RULE-02 — 17 TC tick `Đạt` nhưng Evidence rỗng 18/18**: RULE-02 ghi *"chỉ tick Đạt khi đã đính kèm **đúng loại** bằng chứng"*, F.3 xếp vi phạm RULE vào nhóm *"kết quả test **không được nghiệm thu**"*. Với task bill tiền, TC trục chính là **so nguyên văn chuỗi tiếng Nhật trong hộp thoại** — không có ảnh thì không ai verify lại được. — **Fix**: yêu cầu `thanhntp` bổ sung ảnh chụp hộp thoại cho tối thiểu `TC-OUTTRUTH001-01`, `TC-FUNC004-01`, `TC-TOOLERRHYG001-01`, `TC-TOOLNEGCTRL001-01`, `TC-INTGHOOK001-01`; đồng thời ghi **loại evidence bắt buộc** vào cột `Ghi chú` của cả 18 TC.

- **[MAJOR] RULE-08 / `ENV-003` — task bill tiền nhưng 0/18 TC chạy PRODUCTION**: 16 TC `staging` + 2 TC `local`. `ENV-003` (**Cao**) ghi *"**Không được** đánh × với lý do 'staging đã pass'"*; Catalog `ENV-PAY` ghi *"Dev/staging: tài khoản test — Production: **tài khoản thật**. **Không thể tái hiện lỗi cổng thanh toán ở môi trường test**"*. Bug của KH phát sinh đúng ở production, do **hạn mức sử dụng của account UnivaPay thật** (J#129041) — điều kiện này **không tồn tại trên staging**. — **Fix**: thêm `TC-ENV003-01` (§5) — smoke production với plan giá nhỏ + thẻ bị từ chối, chỉ verify **nội dung hộp thoại** (không tạo giao dịch tiền lớn), kèm đối soát dashboard UnivaPay production.

- **[MAJOR] [AP-2] SYMPTOM-ONLY — KH chỉ mô tả "hiển thị lỗi", còn 1 dữ kiện chưa giải thích được**: J#128666 (WSSサポーター, 2026-08-10) ghi *"kiểm tra log ngày 8/7・8/8 **không tìm thấy log xử lý đặt lịch** tương ứng"*, trong khi KH khẳng định *"hôm nay test lại vẫn bị lỗi tương tự"* (J#128691, 8/11). Log Dev dùng làm bằng chứng là ngày **8/6**. Nếu tồn tại failure mode mà request **không tới** `payment()` thì bản fix (thêm log + message **bên trong** hàm đó) không chạm tới. — **Fix**: hỏi Dev xác nhận (1) log 8/7-8/8 của 2 friend `ハマサキテスト` / `テスト` thực sự trống hay chỉ không tìm đúng chỗ; (2) có alternative root cause nào cũng cho hộp thoại trắng không. Nếu không giải thích được → phải có TC cho luồng vào (LIFF init / session hết hạn / `uid` sai) trước khi đóng ticket.

- **[MAJOR] RULE-01 — 5 quan điểm ưu tiên Cao thiếu loại case, không TC nào ghi lý do**:
  - `FUNC-001` (Cao): chỉ **Normal** (`TC-FUNC001-01`) — thiếu Abnormal + Boundary
  - `OUT-TRUTH-001` (Cao): chỉ **Abnormal** (`TC-OUTTRUTH001-01`) — thiếu Normal + Boundary
  - `STATE-001` (Cao): chỉ **Normal** (`TC-STATE001-01`) — thiếu Abnormal + Boundary
  - `REG-SHARED-001` (Cao): 3 TC đều **Abnormal** — thiếu Normal + Boundary
  - `FUNC-004` (Cao): 1 TC **Abnormal** và đang `skip` — thiếu cả 3 chiều thực tế
  — **Fix**: hoặc bổ sung TC (xem §5), hoặc ghi lý do vào `Ghi chú` từng TC (VD *"quan điểm không có khái niệm biên ở nhánh này"*). Không được để trống.

- **[MAJOR] Toàn bộ 18 TC bỏ trống `Trạng thái đánh giá spec`**: Studio trả `spec_status = null` cho cả 18. Đây là cột chống *"tự suy diễn rồi cho Đạt"* — đặc biệt quan trọng ở `TC-TOOLERRHYG001-01`, nơi chính note Studio ghi *"**CẦN LEADER XÁC NHẬN** … nội dung tiếng Anh thô có thể chưa đạt yêu cầu trải nghiệm — người chạy **KHÔNG được tự kết luận đạt hay không đạt**"* — **nhưng TC này đang được tick `Đạt`**. — **Fix**: điền `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` cho cả 18 TC; riêng `TC-TOOLERRHYG001-01` phải là `Đã hỏi leader` + ghi rõ Leader nào duyệt, hoặc chuyển về `Chưa test`.

- **[MAJOR] GAP-3 — `DATA-DB-001` / RULE-07: không TC nào kiểm `WHERE` scope khi xoá booking tạm**: luồng thất bại có **DELETE** bản ghi đặt chỗ + **recalc** số chỗ đã dùng của khung giờ (`TC-STATE001-01`, `TC-OUTTRUTH001-01` đều chạm). RULE-07 yêu cầu *"tạo bản ghi trùng tên ở 2 tài khoản để kiểm chứng `WHERE`"*. Hiện chỉ test 1 user đặt 1 mình. Rủi ro cụ thể: user A thanh toán fail → recalc có trả nhầm chỗ của user B trong cùng khung giờ không. — **Fix**: thêm `TC-DATADB001-01` (§5). *Lưu ý: code DELETE/recalc **không bị fix chạm** nên xếp MAJOR chứ không BLOCKER; nhưng đây là TC rẻ và chặn được lỗi mất chỗ.*

- **[MAJOR] GAP-4 — `PAY-ABANDON-001` (Cao) không có TC nào**: trigger *"BẮT BUỘC với mọi luồng thanh toán / subscription"*; Catalog `MAP-PAY-01` liệt kê event booking phải test đủ *"thành công / thất bại rồi retry / **hủy giữa chừng** / thanh toán lại / **thanh toán trùng** / charge sau khi đã hủy"* và `MAP-PAY-02` *"callback về trễ — trạng thái phải đúng khi callback đến **sau khi user đã rời màn hình**"*. Hiện cover: thành công ✅, thất-bại-rồi-retry ✅ (`TC-STATE001-01`), thanh toán lại ✅ — **thiếu**: hủy giữa chừng, thanh toán trùng, callback tới sau khi user rời màn. — **Fix**: thêm `TC-PAYABANDON001-01`, `-02` (§5).

- **[MAJOR] GAP-5 — `CONC-001` / duplicate transaction: không TC nào double-click 「決済する」**: §3 phụ lục liệt kê `Duplicate transaction (cùng order_id submit 2 lần)` là error type bắt buộc; Catalog `MAP-PLAN-05` cũng nêu pattern double-click. Với luồng tiền, nhân đôi charge là rủi ro cao hơn hẳn hộp thoại trắng. — **Fix**: thêm `TC-CONC001-01` (§5), evidence = số bản ghi charge đếm trên dashboard UnivaPay.

- **[MAJOR] `TC-TOOLNEGCTRL001-01` tick `Đạt` nhưng gắn `bug_tickets = [39619]`**: TC đạt mà vẫn sinh ticket bug là mâu thuẫn — hoặc kết quả sai, hoặc ticket #39619 là bug phát hiện ngoài lề cần trace. Task-level `openBugs = 0` càng khó hiểu. — **Fix**: Leader mở #39619, xác nhận quan hệ với TC này; nếu là bug do TC phát hiện → `Kết quả thực thi` phải là `Không đạt`.

- **[MAJOR] 6 TC tự viết thiếu `Mã quan điểm liên kết` + `Loại case`** (`TC-NOVP-01` → `-06`): không map được coverage, không áp được RULE-01. 2 TC trong đó thực chất là **Boundary** ("= hạn mức") nhưng bỏ trống. — **Fix**: `thanhntp` gán mã quan điểm trên Studio (`testcase_update`) rồi fetch lại: gợi ý `TC-NOVP-01/02/03` → `REG-SHARED-001` (sibling `changeBooking`), `TC-NOVP-04/05/06` → `PAY-STATE-001` hoặc `FUNC-004`.

- **[MAJOR] Scope chưa chốt — 3 TC test `changeBooking` trong khi Dev khai luồng này CHƯA sửa**: file 03 mục 3 dòng 2 ghi *"`changeBooking` … cùng họ nhưng lỗi khác, **chưa sửa** (ghi ở mục yokoten)"*, và mục 4.3 **không** liệt kê `changeBooking`. `TC-NOVP-01/02/03` đang `Đạt` ở staging ⇒ hoặc luồng này vốn đã đúng (thì "lỗi khác" của Dev là lỗi gì?), hoặc TC chưa chạm đúng nhánh. — **Fix**: hỏi Dev "lỗi khác ở `changeBooking`" cụ thể là gì, có cần tách ticket riêng không; ghi kết luận vào `Ghi chú` 3 TC đó.

- **[MAJOR] [AP-3] Regression T2 chỉ có happy-path abnormal, không có edge state**: `TC-REGSHARED001-01/02/03` đều dùng precondition sạch (1 sản phẩm/khoá học/menu giá 66000, lịch còn chỗ). Không có TC chạy 3 nơi này ở trạng thái biên (hết chỗ, sản phẩm đã ngừng bán, tài khoản khác gói). — **Fix**: mức tối thiểu, thêm 1 biến thể edge cho nơi rủi ro nhất (mua sản phẩm), hoặc ghi rõ ở `Ghi chú` là đã cân nhắc và chấp nhận rủi ro.

- **[MAJOR] [AP-4] Không có link PR/diff để verify fix shape thực tế**: file 03 chỉ có commit hash `6944f7ccb1` + branch `ai_fixbug_39507`, **không có link PR/diff xem được**. Không đọc được diff thì không phân biệt được fix là **generic catch-all** hay **`if (errorCode === CHARGE_AMOUNT_TOO_HIGH)`** — mà 2 shape này cần 2 bộ TC khác nhau. — **Fix**: yêu cầu Dev cung cấp link diff (hoặc paste 2 dòng đã thêm) vào file 03 trước khi review round 2.

### 4.3 Minor (có thể fix sau)

- **[MINOR] `TC-NOVP-06` tiêu đề mâu thuẫn nội dung**: *"Bill tiền stripe **success** có số tiền > số tiền hạn mức"* nhưng `Kết quả mong đợi` là *"Hiển thị thông báo lỗi của stripe"*. — **Fix**: đổi thành *"Bill tiền Stripe **thất bại** khi số tiền > hạn mức: hiện message lỗi của Stripe, không hộp thoại trống"*.

- **[MINOR] `Môi trường test` của 2 TC ghi `LOCAL` — không thuộc enum canonical** (`STAGING` / `DEV` / `PRODUCTION`). — **Fix**: quy `local` về `DEV`, hoặc bổ sung `LOCAL` vào enum ở `templates/04-tc-list.template.md` nếu team thống nhất dùng.

- **[MINOR] 10/18 TC có `env_tag = local-only` nhưng lại được ghi nhận chạy ở `staging`** — tag và env thực tế mâu thuẫn, khó biết TC có chạy đúng điều kiện thiết kế không. — **Fix**: `thanhntp` xác nhận lại; nếu chạy staging được thì sửa `env_tag` trên Studio.

- **[MINOR] `TC-NOVP-01` → `-06` có `Điều kiện tiền đề` và `Các bước thực hiện` quá vắn tắt**: VD *"Mở màn change booking / Nhập test card hợp lệ / Confirm decision"* — thiếu bot nào, event nào, plan giá bao nhiêu, ai là LINE user. Người khác đọc không dựng lại được env (vi phạm B.1/B.4 `review-checklist.md`). — **Fix**: bổ sung precondition theo mẫu của các TC do AI viết.

- **[MINOR] `TC-NOVP-03` nêu tên hàm `paymentCreditCardItemV2Univapay` trong `Kết quả mong đợi`** — hàm này không xuất hiện ở bất kỳ mục nào của file 03. — **Fix**: xác nhận với Dev tên hàm đúng, hoặc bỏ chi tiết code khỏi expected (TC nên viết ở góc nhìn quan sát được trên màn hình).

- **[MINOR] `Loại case` toàn bộ bộ TC lệch tỷ lệ gợi ý**: Normal 3 / Abnormal 8 / Boundary 1 / trống 6. Với task xử lý lỗi thì nghiêng Abnormal là hợp lý, nhưng **Boundary chỉ 1 TC** cho một task mà bản chất là **ngưỡng số tiền** thì quá mỏng. — **Fix**: xem `TC-FUNC004-02` ở §5.

### 4.4 Nit (gợi ý)

- **[NIT] `INTG-HOOK-001` (Cao) mới cover 1/5 chiều**: có webhook-báo-lỗi (`TC-INTGHOOK001-01`) và webhook-không-tới (`TC-INTGHOOK002-01`), **chưa có** webhook trùng / trễ / sai thứ tự. Evidence chuẩn của quan điểm này là *"SỐ LẦN XỬ LÝ THỰC TẾ đếm từ log/DB"*. Không nâng MAJOR vì **code nhận webhook không bị fix chạm** — nhưng nếu team chạy regression release thì nên bổ sung.

- **[NIT] `TC-INTGHOOK001-01` và `TC-INTGHOOK002-01` phụ thuộc "cửa sổ chờ ~5 giây"** để mô phỏng — TC dạng này dễ flaky, 2 người chạy có thể ra 2 kết quả. Gợi ý ghi rõ cách mô phỏng đã dùng vào `Ghi chú` khi chạy.

- **[NIT] Có thể gộp `TC-REGSHARED001-01/02/03`** thành 1 TC 3 nhánh nếu muốn gọn — nhưng **khuyến nghị giữ nguyên 3 TC** vì tách theo đúng danh sách vùng ảnh hưởng Dev cung cấp (RULE-12), dễ trace khi 1 nơi fail.

- **[NIT] `test_viewpoint_selection` của task Studio = `null`** → không có bảng duyệt quan điểm để kiểm RULE-03 (mọi × phải có lý do). Gợi ý team điền bảng này trên Studio để `/review-tc` các round sau đối chiếu được.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. **13 TC** — ưu tiên chạy theo thứ tự: GAP-1/GAP-2 (Blocker) → GAP-3/4/5 → ENV.
> ⚠️ Toàn bộ TC dưới đây thao tác trên **trình duyệt thật** ở màn LIFF phía LINE user, bot bật **chế độ chờ webhook** (đúng điều kiện của nhánh code đã sửa) — trừ TC ghi rõ khác.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PAYSTATE001-01 | PAY-STATE-001 | Normal | payment(): thanh toán event thành công — khớp 3 nơi màn user / admin / dashboard UnivaPay | - Bot test cấu hình UnivaPay môi trường thử, **bật** chế độ chờ webhook<br>- Event đặt chỗ bật thu phí tự động, duyệt tự động, khung giờ còn chỗ<br>- Plan tên `一般の方` giá 10.000 yên<br>- Có quyền đăng nhập **dashboard UnivaPay** (môi trường thử) của merchant đang dùng<br>- LINE user test đã kết bạn, có link đặt chỗ kèm uid | 1. Ghi lại số chỗ đã dùng của khung giờ + thời điểm bắt đầu test.<br>2. Mở link đặt chỗ trên trình duyệt thật, chọn khung giờ, chọn plan `一般の方` 10.000 yên, số lượng 1, nhập đủ thông tin, bấm 「申し込む」.<br>3. Nhập thẻ thử hợp lệ, bấm 「決済する」.<br>4. Chụp màn kết quả phía LINE user.<br>5. Mở màn admin quản lý đặt chỗ của event → chụp dòng đặt chỗ vừa tạo.<br>6. Mở **dashboard UnivaPay** → tìm charge theo thời điểm ở bước 1 → chụp bản ghi. | Plan `一般の方` 10.000 yên, số lượng 1, thẻ thử hợp lệ UnivaPay | **3 nơi khớp nhau**: (1) màn LINE user hiện trang kết thúc, không hộp thoại lỗi; (2) màn admin hiện đúng 1 bản ghi đặt chỗ, trạng thái đã thanh toán, tên plan `一般の方`, số tiền `10,000`; (3) dashboard UnivaPay có **đúng 1 charge** `successful` số tiền `10000 JPY`, mã giao dịch **trùng** mã lưu ở bản ghi đặt chỗ. Số chỗ đã dùng tăng đúng 1. | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-2** (`PAY-STATE-001` — chưa TC nào đối soát dashboard cổng). Evidence bắt buộc: **screenshot 3 nơi** + log giao dịch (RULE-02). Cover BUG/F1/T1 ở chiều Normal (RULE-01) |
| TC-PAYSTATE001-02 | PAY-STATE-001 | Abnormal | payment(): thanh toán thất bại — dashboard UnivaPay KHÔNG phát sinh charge thành công, không trừ tiền | - Như `TC-PAYSTATE001-01`<br>- Plan để giá 66.000 yên (vượt hạn mức mỗi giao dịch của môi trường thử)<br>- Ghi lại số chỗ đã dùng + số charge hiện có trên dashboard trước khi test | 1. Ghi lại số chỗ đã dùng và **đếm số charge** đang có trên dashboard UnivaPay.<br>2. Mở link đặt chỗ, chọn plan 66.000 yên, nhập đủ thông tin, bấm 「申し込む」.<br>3. Nhập thẻ thử hợp lệ, bấm 「決済する」.<br>4. Chụp nguyên văn hộp thoại lỗi.<br>5. Mở màn admin quản lý đặt chỗ → xác nhận không còn bản ghi rác.<br>6. Mở dashboard UnivaPay → đếm lại charge, mở bản ghi phát sinh mới nhất. | Plan 66.000 yên, số lượng 1, thẻ thử hợp lệ | Hộp thoại hiện 「課金金額が課金最大額より超過しています。」 (khác rỗng). Màn admin **không còn** bản ghi đặt chỗ tạm; số chỗ đã dùng trở về giá trị ghi ở bước 1. Trên dashboard UnivaPay: **không có charge `successful` nào mới**; bản ghi mới (nếu có) ở trạng thái `failed`/`error` với lý do `CHARGE_AMOUNT_TOO_HIGH`, **số tiền không bị trừ**. | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-2**. Trả lời trực tiếp câu hỏi KH ở J#129042 (test payment có bị trừ hạn mức không). Evidence: screenshot 3 nơi + ảnh dashboard trước/sau |
| TC-PAYSTATE001-03 | PAY-STATE-001 | Boundary | payment(): thanh toán ĐÚNG ngưỡng hạn mức 50.000 yên — thành công, 3 nơi khớp | - Như `TC-PAYSTATE001-01`<br>- **Xác nhận trước** hạn mức mỗi giao dịch của môi trường thử UnivaPay bằng tài liệu chính thức (RULE-05), ghi số vào `Ghi chú`<br>- Plan để giá đúng bằng hạn mức đó (dự kiến 50.000 yên) | 1. Tra tài liệu UnivaPay lấy hạn mức mỗi giao dịch của môi trường thử, ghi lại nguồn.<br>2. Đặt giá plan **đúng bằng** hạn mức, lưu.<br>3. Mở link đặt chỗ, chọn plan, bấm 「申し込む」 → nhập thẻ thử hợp lệ → 「決済する」.<br>4. Chụp màn kết quả.<br>5. Đối chiếu màn admin + dashboard UnivaPay. | Plan = đúng hạn mức (dự kiến 50.000 yên), thẻ thử hợp lệ | Thanh toán **thành công** (biên là giá trị hợp lệ): không hộp thoại lỗi, bản ghi đặt chỗ trạng thái đã thanh toán, dashboard UnivaPay có charge `successful` đúng số tiền. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-2** + RULE-01 (chiều Boundary cho `PAY-STATE-001`). **Nguồn hạn mức phải ghi rõ** (FUNC-004 yêu cầu). Nếu tài liệu ghi khác 50.000 → sửa lại data và báo Leader |
| TC-PAYSTATE001-04 | PAY-STATE-001 | Abnormal | payment(): thẻ bị từ chối (card_declined) — hộp thoại hiện đúng lý do, không trắng | - Bot bật chế độ chờ webhook, UnivaPay môi trường thử<br>- Plan giá 10.000 yên (**dưới** hạn mức — để chắc chắn lỗi đến từ thẻ, không phải số tiền)<br>- Có **thẻ test bị từ chối** của UnivaPay sandbox (tra tài liệu chính thức — RULE-05) | 1. Đặt giá plan 10.000 yên, lưu.<br>2. Mở link đặt chỗ, chọn plan, nhập đủ thông tin, bấm 「申し込む」.<br>3. Nhập **thẻ test bị từ chối**, bấm 「決済する」.<br>4. Đọc và chụp nguyên văn hộp thoại.<br>5. Đóng hộp thoại → xác nhận nút 「決済する」 bấm lại được.<br>6. Kiểm bản ghi đặt chỗ + số chỗ đã dùng. | Plan 10.000 yên; thẻ test declined của UnivaPay sandbox; ghi lại **mã lỗi thực nhận** | Hộp thoại **có nội dung** (không trắng, không rỗng) và nội dung **khác** câu của lỗi vượt hạn mức — đúng câu ánh xạ với mã lỗi thẻ bị từ chối. Không silent fail, không tự quay về talklist. Bản ghi đặt chỗ tạm bị xoá, số chỗ được trả lại. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-1** (§3 phụ lục — `card_declined`). Evidence: ảnh hộp thoại + mã lỗi thực nhận ghi vào `Ghi chú`. Nếu sandbox không trigger được → ghi rõ lý do, **không để trống** |
| TC-PAYSTATE001-05 | PAY-STATE-001 | Abnormal | payment(): thẻ hết hạn (expired_card) — message khác hẳn 2 case trên | - Như `TC-PAYSTATE001-04`<br>- Có **thẻ test hết hạn** của UnivaPay sandbox | 1. Đặt giá plan 10.000 yên, lưu.<br>2. Mở link đặt chỗ, chọn plan, bấm 「申し込む」.<br>3. Nhập **thẻ test hết hạn**, bấm 「決済する」.<br>4. Chụp nguyên văn hộp thoại.<br>5. So sánh nội dung với hộp thoại của `TC-PAYSTATE001-02` và `-04`. | Plan 10.000 yên; thẻ test expired | Hộp thoại hiện 「カード有効期限が過ぎています。」 (hoặc câu tương ứng trong bảng ánh xạ), **khác** cả câu lỗi vượt hạn mức lẫn câu thẻ bị từ chối ⇒ chứng minh message bám theo mã lỗi thật chứ không phải câu cố định. Bản ghi tạm bị xoá, chỗ được trả lại. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-1** (§3 phụ lục — `expired_card`). Đây là TC thay thế hợp lệ nếu `TC-FUNC004-01` (amount_too_low) tiếp tục không trigger được |
| TC-PAYSTATE001-06 | PAY-STATE-001 | Abnormal | payment(): số dư không đủ (insufficient_funds) — hộp thoại có nội dung + có đường lùi | - Như `TC-PAYSTATE001-04`<br>- Có **thẻ test số dư không đủ** của UnivaPay sandbox | 1. Đặt giá plan 10.000 yên, lưu.<br>2. Mở link đặt chỗ, chọn plan, bấm 「申し込む」.<br>3. Nhập **thẻ test insufficient funds**, bấm 「決済する」.<br>4. Chụp hộp thoại, ghi mã lỗi thực nhận.<br>5. Đóng hộp thoại, bấm 「戻る」 → chọn lại plan → thanh toán bằng thẻ hợp lệ. | Plan 10.000 yên; thẻ test insufficient funds; lần 2 dùng thẻ hợp lệ | Lần 1: hộp thoại có nội dung đúng nguyên nhân, **có UX recovery** (đóng được, quay lại được, bấm lại được). Lần 2: đặt chỗ thành công. Cuối cùng user chỉ có **1** bản ghi đặt chỗ, số chỗ đã dùng chỉ tăng 1. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-1** (§3 phụ lục — `insufficient_funds`) + kết hợp verify lại `STATE-001` (retry sau lỗi) ở chiều lỗi khác lỗi số tiền |
| TC-PAYSTATE001-07 | PAY-STATE-001 | Abnormal | payment(): cổng thanh toán timeout / trả 5xx — không treo màn, không hộp thoại trắng | - Như `TC-PAYSTATE001-04`<br>- Có cách chặn/làm chậm request tới cổng UnivaPay từ môi trường test (chặn domain cổng ở tầng mạng, hoặc throttle tới mức timeout) — ghi rõ cách đã dùng | 1. Đặt giá plan 10.000 yên, lưu.<br>2. Bật cơ chế chặn/làm chậm request tới cổng UnivaPay.<br>3. Mở link đặt chỗ, chọn plan, bấm 「申し込む」 → nhập thẻ hợp lệ → 「決済する」.<br>4. Quan sát tối đa 60 giây: màn hình có treo spinner vô hạn không.<br>5. Chụp hộp thoại/thông báo cuối cùng.<br>6. Gỡ chặn, kiểm bản ghi đặt chỗ + số chỗ + dashboard UnivaPay. | Plan 10.000 yên; request tới cổng bị timeout / trả 5xx | Màn hình **không treo vô hạn**: có hộp thoại hoặc thông báo **có nội dung** trong thời gian hữu hạn. Không hộp thoại trắng. Bản ghi đặt chỗ **không bị treo lơ lửng** — hoặc bị xoá + trả chỗ, hoặc ở trạng thái chờ có thể đối soát. Dashboard UnivaPay không có charge `successful` mồ côi. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-1** (§3 phụ lục — `network timeout / API 5xx`). Đây là error type **không có mã lỗi trong bảng ánh xạ** ⇒ đồng thời verify nhánh fallback của fix. Evidence: video/ảnh màn hình + log ứng dụng |
| TC-FUNC004-02 | FUNC-004 | Boundary | payment(): 3 giá trị sát ngưỡng hạn mức UnivaPay — 49.999 / 50.000 / 50.001 yên | - Bot bật chế độ chờ webhook, UnivaPay môi trường thử<br>- Đã tra và ghi lại **nguồn** hạn mức mỗi giao dịch của môi trường thử (RULE-05)<br>- Khung giờ còn tối thiểu 3 chỗ<br>- Ghi lại số chỗ đã dùng ban đầu | 1. Đặt giá plan = **hạn mức − 1** (dự kiến 49.999), lưu → đặt chỗ + thanh toán bằng thẻ hợp lệ → ghi kết quả + chụp màn.<br>2. Đặt giá plan = **đúng hạn mức** (50.000), lưu → lặp lại → ghi kết quả.<br>3. Đặt giá plan = **hạn mức + 1** (50.001), lưu → lặp lại → **chụp nguyên văn hộp thoại**.<br>4. Sau cả 3 lần, đối chiếu số chỗ đã dùng với số lần thanh toán thành công. | 49.999 / 50.000 / 50.001 yên, mỗi lần số lượng 1, thẻ thử hợp lệ.<br>**Phép tính tay**: 2 lần thành công (bước 1, 2) + 1 lần thất bại (bước 3) ⇒ số chỗ đã dùng = ban đầu + 2 | Bước 1 và 2: thanh toán **thành công**, không hộp thoại lỗi. Bước 3: hộp thoại hiện 「課金金額が課金最大額より超過しています。」 (**có nội dung**), bản ghi tạm bị xoá. Số chỗ đã dùng cuối cùng = ban đầu **+ 2**, khớp phép tính tay. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **[MINOR] Boundary quá mỏng** + RULE-01 chiều Boundary. 5 pattern của FUNC-004 chỉ áp dụng được 3 (biên / biên±1) — pattern `0` và `chuỗi rỗng` không áp dụng vì giá plan do admin nhập, đã có validate riêng ⇒ ghi lý do này vào `Ghi chú` khi chạy. **Nguồn hạn mức bắt buộc ghi rõ** |
| TC-PAYABANDON001-01 | PAY-ABANDON-001 | Abnormal | payment(): đóng tab ngay sau khi bấm 「決済する」 — đơn không treo, chỗ không bị giữ vĩnh viễn | - Bot bật chế độ chờ webhook, UnivaPay môi trường thử<br>- Plan giá 10.000 yên, khung giờ còn chỗ<br>- Ghi lại số chỗ đã dùng ban đầu và thời điểm thao tác | 1. Ghi lại số chỗ đã dùng.<br>2. Mở link đặt chỗ, chọn plan, nhập đủ thông tin, bấm 「申し込む」.<br>3. Nhập thẻ hợp lệ, bấm 「決済する」 rồi **đóng tab ngay lập tức**, trước khi màn hình trả kết quả.<br>4. Chờ 10 phút.<br>5. Mở lại màn admin quản lý đặt chỗ + dashboard UnivaPay + kiểm số chỗ đã dùng của khung giờ. | Plan 10.000 yên; đóng tab trong vòng < 1 giây sau khi bấm 「決済する」 | Trạng thái cuối **nhất quán giữa 2 phía**: nếu dashboard UnivaPay có charge `successful` thì bản ghi đặt chỗ phải tồn tại ở trạng thái đã thanh toán; nếu không có charge thì bản ghi tạm phải bị xoá và **số chỗ được trả lại**. **Không được** để đơn treo vô thời hạn hoặc chỗ bị giữ mà không có ai đặt. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-4** (`PAY-ABANDON-001` — Cao, hiện 0 TC). Catalog `MAP-PAY-01` mục "hủy giữa chừng". Evidence: ảnh trạng thái đơn + ảnh dashboard + số chỗ trước/sau |
| TC-PAYABANDON001-02 | PAY-ABANDON-001 | Abnormal | payment(): webhook tới SAU khi user đã rời màn hình — trạng thái đơn vẫn đúng | - Như `TC-PAYABANDON001-01`<br>- Có cách giữ webhook lại và bắn về **sau** khi user đóng màn (ghi rõ cách mô phỏng đã dùng) | 1. Ghi lại số chỗ đã dùng.<br>2. Chặn đường nhận webhook.<br>3. Mở link đặt chỗ → chọn plan → 「申し込む」 → thẻ hợp lệ → 「決済する」.<br>4. Chờ qua cửa sổ chờ (~5 giây) cho màn chuyển sang trạng thái đang xử lý, rồi **đóng tab**.<br>5. Mở lại đường nhận webhook để phản hồi của cổng về muộn.<br>6. Sau 10 phút, kiểm màn admin + dashboard UnivaPay + số chỗ + tin nhắn LINE user nhận được. | Plan 10.000 yên; webhook trả về **sau** khi user rời màn hình | Đơn được cập nhật đúng theo nội dung webhook đến muộn: nếu webhook báo thành công → bản ghi chuyển sang đã thanh toán, số chỗ giữ nguyên đã trừ, LINE user **nhận được tin hoàn tất** (RULE-06); nếu webhook báo lỗi → bản ghi bị xoá và chỗ được trả lại. Không có trạng thái kẹt giữa. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-4** + Catalog `MAP-PAY-02` ("callback về trễ — trạng thái phải đúng khi callback đến sau khi user đã rời màn hình"). Evidence: log webhook + trạng thái đơn cuối + ảnh tin LINE |
| TC-CONC001-01 | CONC-001 | Abnormal | payment(): double-click 「決済する」 — chỉ phát sinh 1 charge trên dashboard UnivaPay | - Bot bật chế độ chờ webhook, UnivaPay môi trường thử<br>- Plan giá 10.000 yên, khung giờ còn ≥ 2 chỗ<br>- Ghi lại số chỗ đã dùng + số charge trên dashboard trước khi test | 1. Ghi lại số chỗ đã dùng và số charge hiện có trên dashboard UnivaPay.<br>2. Mở link đặt chỗ → chọn plan → nhập đủ thông tin → 「申し込む」.<br>3. Nhập thẻ hợp lệ, **bấm 「決済する」 2 lần liên tiếp thật nhanh** (< 500ms).<br>4. Chờ xử lý xong, chụp màn kết quả.<br>5. Đếm số bản ghi đặt chỗ của user, số chỗ đã dùng, và **số charge mới** trên dashboard UnivaPay. | Plan 10.000 yên; 2 lần click liên tiếp < 500ms.<br>**Phép tính tay**: 1 lần đặt hợp lệ ⇒ 1 bản ghi, chỗ +1, 1 charge | Chỉ có **đúng 1** bản ghi đặt chỗ; số chỗ đã dùng tăng **đúng 1** (không phải 2); dashboard UnivaPay chỉ phát sinh **đúng 1** charge — **không bị thu tiền 2 lần**. Màn hình không hiện 2 hộp thoại chồng nhau. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-5** (§3 phụ lục — `duplicate transaction`; Catalog `MAP-PLAN-05`). Evidence bắt buộc: **ảnh dashboard đếm số charge trước/sau**, không chấp nhận "đã thử, thấy bình thường" |
| TC-DATADB001-01 | DATA-DB-001 | Abnormal | payment(): user A thanh toán thất bại KHÔNG làm mất chỗ của user B trong cùng khung giờ | - Bot bật chế độ chờ webhook, UnivaPay môi trường thử<br>- **2 LINE user test** đã kết bạn: user A và user B, mỗi user có link đặt chỗ riêng<br>- Cùng 1 khung giờ, sức chứa 5 chỗ<br>- 2 plan: `一般の方` 66.000 yên (fail) và `一般の方(お試し)` 10.000 yên | 1. User B đặt chỗ + thanh toán **thành công** plan 10.000 yên → ghi lại số chỗ đã dùng (kỳ vọng +1) và mã bản ghi của B.<br>2. User A mở link đặt chỗ **cùng khung giờ**, chọn plan 66.000 yên, 「申し込む」 → thẻ hợp lệ → 「決済する」 → đóng hộp thoại lỗi.<br>3. Kiểm màn admin: danh sách đặt chỗ của khung giờ đó.<br>4. Kiểm số chỗ đã dùng và số chỗ còn trống hiển thị phía LINE user.<br>5. Mở lại màn đặt chỗ bằng user B xác nhận đơn của B vẫn còn. | User B: plan 10.000 yên (thành công). User A: plan 66.000 yên (thất bại).<br>**Phép tính tay**: chỉ B đặt thành công ⇒ số chỗ đã dùng = ban đầu **+1**, còn trống = 4 | Bản ghi đặt chỗ của **user B vẫn nguyên vẹn** (không bị xoá lây khi recalc); bản ghi tạm của user A bị xoá. Số chỗ đã dùng = ban đầu +1 (**không** bị trừ về 0, **không** bị +2). Số chỗ còn trống trên màn LINE user của cả A và B đều hiển thị 4. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-3** (RULE-07 / `DATA-DB-001` — kiểm `WHERE` scope khi DELETE + recalc). Cover **D2**. Evidence: ảnh danh sách đặt chỗ trước/sau + số chỗ ở cả 2 phía |
| TC-ENV003-01 | ENV-003 | Normal | payment() trên PRODUCTION: thanh toán thất bại hiện message có nội dung, đối soát dashboard UnivaPay thật | - **Môi trường PRODUCTION**, sau khi release nhánh `ai_fixbug_39507`<br>- Bot production của tài khoản test nội bộ (KHÔNG dùng tài khoản khách), cấu hình UnivaPay **thật**, bật chế độ chờ webhook<br>- Event đặt chỗ nội bộ, plan giá **nhỏ nhất hợp lệ** (VD 100 yên) để hạn chế phát sinh tiền thật<br>- Có quyền xem dashboard UnivaPay production + kế hoạch hoàn tiền nếu charge thành công<br>- Có **thẻ test/thẻ thật bị từ chối** để tạo lỗi mà không phát sinh tiền | 1. Ghi lại thời điểm và số charge hiện có trên dashboard UnivaPay production.<br>2. Mở link đặt chỗ production bằng LINE user test nội bộ, chọn plan giá nhỏ, 「申し込む」.<br>3. Nhập **thẻ bị từ chối**, bấm 「決済する」.<br>4. Chụp nguyên văn hộp thoại lỗi.<br>5. Kiểm bản ghi đặt chỗ + số chỗ trên production.<br>6. Mở dashboard UnivaPay production đối soát: không có charge `successful` mới.<br>7. Nếu phát sinh charge ngoài dự kiến → hoàn tiền ngay và ghi vào `Ghi chú`. | Plan giá nhỏ nhất hợp lệ (VD 100 yên); thẻ bị từ chối; môi trường **production** | Hộp thoại phía LINE user **có nội dung** (không trắng, không rỗng) — chứng minh bản vá hoạt động trên production, nơi bug gốc phát sinh. Bản ghi đặt chỗ tạm bị xoá, số chỗ được trả lại. Dashboard UnivaPay production **không phát sinh charge `successful`**. | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | Lấp **[MAJOR] RULE-08 / `ENV-003`** — task bill tiền hiện 0/18 TC production; Catalog `ENV-PAY` ghi *"không thể tái hiện lỗi cổng thanh toán ở môi trường test"*. ⚠️ **Bắt buộc Leader duyệt trước khi chạy** (tạo data trên production). Dùng plan giá nhỏ + thẻ bị từ chối để **không** phát sinh tiền thật. Evidence: ảnh hộp thoại + ảnh dashboard production trước/sau |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec — chi tiết:**
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — Event Booking (FA-021), phần thanh toán qua cổng.
  - **Nội dung cần update**:
    1. **Hành vi khi mã lỗi KHÔNG có trong bảng ánh xạ**: hiện hệ thống trả **nguyên văn chuỗi lỗi tiếng Anh** của thư viện gọi API. Note của `TC-TOOLERRHYG001-01` ghi rõ *"CẦN LEADER XÁC NHẬN … nội dung tiếng Anh thô có thể chưa đạt yêu cầu trải nghiệm"*, và §3 phụ lục `checklist-lme.md` yêu cầu *"frontend hiển thị **message business-friendly** (không phải raw API error)"* ⇒ **spec chưa định nghĩa**, cần chốt: chấp nhận chuỗi tiếng Anh, hay phải có câu fallback tiếng Nhật chung.
    2. **Hạn mức mỗi giao dịch của môi trường thử UnivaPay (~50.000 yên)** hiện không nằm ở spec nào — KH và cả support đều mất 6 ngày mới xác định được (J#128717 → J#129061). Nên ghi vào spec + màn hướng dẫn cho khách.
  - **Người chịu trách nhiệm update**: `<Leader phân công — PM hoặc Dev owner FA-021>`

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ (có `TC-OUTTRUTH001-01` tái hiện đúng) · A.2 ⚠️ RISK (F1 thiếu chiều loại lỗi, F2 chỉ 1 TC local) · A.3 ⚠️ RISK (thiếu `WHERE` scope) · A.4 ✅ · A.5 ⚠️ (3 ORPHAN Stripe, giữ lại có điều kiện) · **A.6 ❌ FAIL** (xem §3.5)
- [x] **B. Chất lượng từng TC** — B.1 ⚠️ (6 TC tự viết precondition/steps quá vắn tắt) · B.2 ✅ · B.3 ✅ · B.4 ⚠️ (`TC-NOVP-*` không nêu bot/event/plan cụ thể)
- [x] **C. Chất lượng bộ TC** — tỷ lệ Normal 3 / Abnormal 8 / Boundary 1 / trống 6: hợp lý cho task xử lý lỗi nhưng **Boundary quá mỏng** cho task bản chất là ngưỡng số tiền. Không có TC trùng lặp. Không có phân quyền / i18n / multi-device cần xét (màn LIFF single-role)
- [x] **D. Spec alignment** — không có `02-spec-reference.md`; phát hiện 2 điểm spec chưa định nghĩa → §6
- [x] **E. Hành chính** — TC No. đúng format `TC-<mã quan điểm>-<nn>` cho 12 TC AI; **6 TC không có mã quan điểm** nên phải đặt tạm `TC-NOVP-nn`. File lưu đúng folder. **Thiếu**: người viết/ngày submit của 6 TC tự viết không ghi trong file 04 ngoài metadata Studio
- [x] **F. Base quan điểm test LME**
  - [x] **F.1 Quan điểm (tầng 1)** — bảng dưới
  - [x] **F.2 Catalog (tầng 2)** — **A** ⚠️ (input số tiền plan: chỉ 3 giá trị rời rạc, chưa theo 5 pattern DI) · **B** ✅ (hộp thoại/alert — UIC) · **C** ❌ **FAIL** (khối `C.7 Bill tiền` `MAP-PAY-01` yêu cầu 6 kịch bản, mới cover 3; `MAP-PAY-02` callback trễ chưa cover) · **D/D2** ❌ **FAIL** (`ENV-PAY` — 0 TC production, không đối soát bản ghi cổng) · **E** N/A (không chạm media)
  - [x] **F.3 RULE quy trình** — RULE-01 ❌ (5 quan điểm Cao thiếu loại case) · RULE-02 ❌ (evidence rỗng 18/18) · RULE-03 ⚠️ (không có bảng duyệt quan điểm để kiểm) · RULE-05 ⚠️ (không TC nào ghi đã tra tài liệu UnivaPay để lấy hạn mức) · RULE-06 ✅ (`TC-FUNC001-01` đi tới tin LINE thật) · RULE-07 ⚠️ (đủ DB + màn hình, thiếu `WHERE` scope 2 tài khoản) · RULE-08 ❌ (0 TC production) · RULE-09 N/A (input không nêu đối tượng version-up) · RULE-12 ✅ (regression đúng danh sách Dev cung cấp)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` — Luồng chính hoàn tất đúng đặc tả | **Cao** | ◯ luôn bắt buộc | `TC-FUNC001-01` (Normal) | **RISK** — thiếu Abnormal + Boundary, không ghi lý do → RULE-01 |
| `FUNC-004` — Giới hạn trên/dưới | **Cao** | ◯ ngưỡng số tiền của cổng | `TC-FUNC004-01` (Abnormal, **`skip`**) | **RISK** — TC duy nhất không có kết quả; thiếu biên/biên±1 → thêm `TC-FUNC004-02` |
| `FUNC-003` — Nhập sai định dạng | Cao (field số tiền) | × | — | × — giá plan nhập ở màn admin, **ngoài code path bị sửa**. Lý do đã ghi (RULE-03) |
| `CONC-001` — Đồng thời / idempotency | **Cao** | ◯ double-click nút thanh toán, duplicate transaction | — | **GAP** → `[MAJOR]` §4.2, thêm `TC-CONC001-01` |
| `DATA-DB-001` — `WHERE` scope khi UPDATE/DELETE | **Cao** | ◯ luồng lỗi có DELETE booking + recalc chỗ | — | **GAP** → `[MAJOR]` §4.2 (không nâng BLOCKER vì code DELETE không bị fix chạm), thêm `TC-DATADB001-01` |
| `DATA-COUNT-001` — Số đếm / thống kê | **Cao** | ◯ số chỗ đã dùng của khung giờ | `TC-STATE001-01`, `TC-OUTTRUTH001-01` | **RISK** — có đối chiếu màn hình + DB nhưng chưa có phép tính tay trên bộ dữ liệu biết trước (đã bổ sung ở `TC-FUNC004-02`, `TC-DATADB001-01`) |
| `INTG-HOOK-001` — Webhook trễ/trùng/sai thứ tự | **Cao** | ◯ luồng nhận webhook UnivaPay | `TC-INTGHOOK001-01` (webhook báo lỗi) | **RISK** — mới 1/5 chiều; trùng/trễ/thứ tự chưa có. `[NIT]` §4.4 vì code nhận webhook không bị chạm; `TC-PAYABANDON001-02` cover chiều "tới muộn" |
| `INTG-HOOK-002` — Callback KHÔNG tới | Trung bình | ◯ | `TC-INTGHOOK002-01` | **OK** |
| `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | **Cao** | ◯ **trọng tâm của bug** | `TC-OUTTRUTH001-01` (Abnormal) | **RISK** — chỉ 1 loại case + 1 mã lỗi → RULE-01; bổ sung `TC-PAYSTATE001-01/-04/-05` |
| `PAY-STATE-001` — Nhất quán trạng thái 3 nơi | **Cao** | ◯ **BẮT BUỘC** — có giao dịch tiền | — (không TC nào mở dashboard cổng) | **GAP** → **`[BLOCKER]`** §4.1, thêm `TC-PAYSTATE001-01` → `-07` |
| `PAY-ABANDON-001` — Rời luồng thanh toán giữa chừng | **Cao** | ◯ **BẮT BUỘC** — mọi luồng thanh toán | — | **GAP** → `[MAJOR]` §4.2, thêm `TC-PAYABANDON001-01/-02` |
| `PAY-AMOUNT-001` — Độ chính xác số tiền | Cao | × | — | × — fix không đụng tính tiền (không pro-rate/thuế/giảm giá). Lý do đã ghi |
| `PAY-LIMIT-001` — Giới hạn theo gói | Cao | × | — | × — hạn mức ở đây là của **cổng UnivaPay**, không phải giới hạn gói LME. Lý do đã ghi |
| `PAY-BATCH-001` · `PAY-CONFIRM-001` · `PAY-PLAN-001` | Cao | × | — | × — không có batch tiền, không có luồng tạm→chính thức, không đổi gói trong task này |
| `STATE-001` — Quy trình nhiều bước bị gián đoạn | **Cao** | ◯ đặt chỗ → thu tiền → xác nhận | `TC-STATE001-01` (Normal) | **RISK** — thiếu Abnormal (ngắt giữa 2 bước) + Boundary → RULE-01; `TC-PAYABANDON001-01` lấp một phần |
| `STATE-CLEAN-001` · `STATE-DEP-001` | Cao | × | — | × — không có thao tác hủy hợp đồng / đổi giờ event trong scope fix |
| `REG-SHARED-001` — Shared code / logic | **Cao** | ◯ dùng chung `getMessageErrorUnivapay` + cơ chế chờ webhook | `TC-REGSHARED001-01/-02/-03` + (`TC-NOVP-01/-02/-03` sibling `changeBooking`) | **RISK** — đủ nơi theo danh sách Dev (RULE-12) nhưng 3 TC đều Abnormal, precondition không có edge state → RULE-01 + `[AP-3]` |
| `REG-RUN-001` — Job/dữ liệu chạy dở khi release | Cao | ◯ có booking pending chờ webhook lúc release | — | **GAP** nhưng **không flag** — fix 2 dòng không đổi cấu trúc dữ liệu pending; ghi nhận để đưa vào smoke release (RULE-12). Gợi ý `[NIT]` |
| `ENV-003` — Khác biệt dev/staging/production | **Cao** | ◯ **BẮT BUỘC** — chạm **thanh toán** | — (16 staging + 2 local, **0 production**) | **GAP** → `[MAJOR]` §4.2 (theo mapping RULE-08), thêm `TC-ENV003-01` |
| `SEC-*` — lộ thông tin nhạy cảm trong message/log | Cao | ◯ message lỗi trả từ cổng ra màn user | `TC-TOOLERRHYG001-01` (dialog + console), `TC-APICONTRACT001-01` (log) | **OK** — nhưng cả 2 chỉ chạy ở `local` do AI submit ⇒ cần chạy lại staging |
| `UI-*` — hiển thị hộp thoại, nút bấm lại được | Trung bình | ◯ | `TC-OUTTRUTH001-01`, `TC-TOOLERRHYG001-01` | **OK** |
| `COMPAT-LEGACY-001` (RULE-09) | Cao | × | — | × — input không nêu event booking/UnivaPay từng version-up. **Cần Dev confirm** trước khi chốt × |
| `DEPLOY-ASSET-001` | Trung bình | × | — | × — fix chỉ sửa PHP, `order-item.js` **không đổi** (file 03 mục 3) ⇒ không có asset mới cần cache-bust |
| `JOB-001` · `PERF-LARGE-001` · `MSG-*` · `BULK-*` · `MEDIA-*` · `PERM-*` · `LIFF-ENTRY-*` · `SYNC-APP-*` · `NOTI-MAIL-001` · `OUT-EXPORT-001` | — | × | — | × — fix không thêm/sửa job nền, không gửi tin hàng loạt, không chạm media/phân quyền/entry LIFF/mail/export |

> **Mã quan điểm Studio không có trong tầng 1** — `/review-tc` không map coverage được, đã quy đổi thủ công ở bảng trên:
> `TOOL-NEGCTRL-001` → gần nhất `REG-SHARED-001` · `TOOL-ERRHYG-001` → gần nhất `SEC-*` · `API-CONTRACT-001` → gần nhất `OUT-TRUTH-001` (tầng response).
> 6 TC `TC-NOVP-*` **không có mã quan điểm nào** → xem `[MAJOR]` §4.2.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
