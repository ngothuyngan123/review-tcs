# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37507 — [10-06-2026][QR Code] Giá trị tham số động sid có truyền sang Callback URL của Parameter Export hay không` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền — file 04 chưa có tên tester>` |
| Ngày review | `2026-06-13` |
| Version TCs | `v1 (fetched từ Sheet Improve 1.0, LINE 2914~2977)` |
| Vòng review | `Round 1` |

> **Note spec reference**: Không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng (section QR Code / Landing / Parameter Export). Không có spec chi tiết riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover khá tốt phần biến thể giá trị param (special char / JP / emoji / space / 0), nhưng **bỏ lọt 2 trigger-path quan trọng**: (1) fix nằm ở `doHandleFollowEvent` (chỉ chạy khi **follow / kết bạn mới**) trong khi bug KH có thể xảy ra với **friend cũ quét QR** — không có TC verify path này; (2) 3 case Dev **tự đánh dấu "cần confirm"** (forward_param rỗng/null, param trùng sẵn trong URL, mix param-info) chưa có TC tương ứng — đặc biệt case param trùng đã có hẳn 1 commit "AI review bổ sung".

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần **input variant** của param tự nhập (ký tự đặc biệt, tiếng Nhật, emoji, dấu cách, số 0) và phân nhánh **có/không setting param info** — đây là phần dễ bỏ sót nhất và em đã cover. Tuy nhiên cần bổ sung gấp: (1) TC cho **friend cũ / đang là friend** quét QR (vì fix chỉ ở event follow của friend mới — phải confirm với Dev path này có được fix không); (2) 3 case Dev đánh dấu "cần confirm" (forward_param rỗng, param trùng `sid` đã có sẵn trong URL, mix param-info+custom). Ngoài ra nhiều dòng **Expected để trống** → reviewer/người chạy TC không đo được kết quả, cần điền Expected rõ cho từng nhánh.

---

## 3. Coverage Matrix

> File 04 là bảng **phân cấp** fetch từ Sheet (Sub2→Sub5 / Expect / Actual), không có cột TC ID / Type / Priority / Precondition → mapping dưới suy luận từ nội dung Sub-columns + Expected. "Sheet Row" = số dòng trong tab `Improve 1.0`.

| Impact | Loại | Priority | TCs map (Sheet Row) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause: URL không setting param info → `forward_param` chưa set) | Fix | — | 2940–2948 (CÓ SETTING PARAM NGOÀI / không setting ucid → custom param vào request bin) | 9 | **RISK** — cover case follow mới; thiếu case forward_param rỗng/null |
| F1 — `HandlePostbackTask.doHandleFollowEvent` (bổ sung forward_param vào URL) | Function | Direct | 2914–2937 (landing callback theo friend state), 2940–2948 | ~33 | **RISK** — chỉ verify path **follow (add new friend)**; **không có TC** verify path friend cũ/đang friend quét QR (xem BLOCKER-1) |
| D1 — (Dev ghi "Không có") | Data | — | N/A | — | N/A |
| T1 — Callback case URL **đã có** setting param info → chỉ replace param truyền vào | Feature | Medium | 2949–2957 (có setting 1 ucid + custom param), 2958–2974 (regression: có setting ucid → không add param thừa), 2975 | ~26 | **RISK** — thiếu case param trùng (URL có sẵn `sid` + forward_param cũng `sid`) |
| T2 — Callback case URL **không** setting → set hết forward_param/mail/friend_name/friend_type/line_id | Feature | High | 2940–2948, 2976 | 10 | **RISK** — chưa verify **đủ 5 param** (mail/friend_name/friend_type/line_id) tự set khi URL không setting gì; chỉ tập trung forward_param |

### ORPHAN / non-TC rows

| Sheet Row | Nội dung | Lý do | Hành động đề xuất |
|---|---|---|---|
| 2938 | Text "Đánh giá ảnh hưởng Dev" | Annotation, không phải TC | Giữ (context) — đã tách sang `03-dev-impact.md` |
| 2939 | Text "Tái hiện case KH" | Annotation, không phải TC | Giữ (context) — đã tách sang `01-bug-task.md` |

Không phát hiện TC lạc chủ đề (orphan thật) — toàn bộ TC đều thuộc scope BUG / F1 / T1 / T2.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **URL/param construction fix** ("Set bổ sung thêm `forward_param` nếu có") — gần nhất với *validate-input / add-field*, KHÔNG phải generic catch-all error handler. |
| Trigger space cần cover | (a) Friend state: **add new friend** / unblock / old friend / đang là friend; (b) Param-info config: **không setting gì** / setting 1 phần / setting đủ; (c) forward_param: **có giá trị** / **rỗng/null** / **trùng param đã có sẵn trong URL**; (d) Giá trị param: special char / JP / emoji / space / số 0 / text có dấu cách không đúng URL format. |
| Số trigger TCs hiện cover | Friend state: **1/4 verify đủ** (chỉ add new friend có Expected; old/đang friend Expected trống). Param-info: 3/3 nhánh có TC. forward_param: 1/3 (thiếu rỗng/null + trùng). Giá trị param: ~9/9 ✅ tốt. |
| KH report dạng | **Gần symptom-only** — KH mô tả hiện tượng "param tự nhập không vào request bin"; ban đầu còn nghi "Callback URL chưa implement nhận param" (a Thắng đánh giá khả năng thấp). Dev chốt 1 root cause (forward_param chưa set). |
| Alternative root causes cần verify | (1) Path **friend cũ quét QR** dùng code khác `doHandleFollowEvent` → có thể vẫn miss param dù đã fix; (2) Encoding param (base64/JP/emoji) bị drop ở tầng callback → đã có TC special-char nhưng nên verify trên callback thật. |
| Anti-patterns dính | **AP-2** (symptom-only, một phần), **AP-6** (mục 3 dev-impact trống). AP-1 không dính (fix không phải generic catch). |

> Trigger space cover **chưa đủ** ở chiều friend-state và forward_param edge → flag [BLOCKER]/[MAJOR] tại §4.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 — Trigger path "friend cũ quét QR" không được verify**: Fix nằm ở `HandlePostbackTask.doHandleFollowEvent` — event này **chỉ chạy khi friend FOLLOW (kết bạn mới)**. Bug KH thực tế (journal 11/6: friend truy cập QR Action 「メディア03」 lúc 2026-06-08 13:55) **có thể là friend đã kết bạn từ trước**. TCs có dòng "old friend / đang là friend" (2920–2925, 2932–2937, 2958–2974) nhưng **Expected để trống** và **không có dòng nào verify forward_param/custom param được forward cho friend cũ**. → **Đề xuất**: thêm TC verify friend cũ + đang friend quét QR với custom param → callback có nhận param không (xem TC-NEW-01). **Đồng thời hỏi Dev**: `doHandleFollowEvent` có cover path friend cũ không, hay cần fix thêm ở handler khác?

- **[BLOCKER] FIX-SHAPE / GAP-2 — Case param trùng (URL đã có sẵn `sid` + forward_param cũng `sid`) chưa có TC**: Đây là case Dev **tự đánh dấu cần confirm** ("AI bổ sung: Kiểm tra case đã có param sẵn trong url rồi thì bỏ qua param đó?") và đã có hẳn **1 commit riêng "AI review bổ sung"** (`61e86cb...`) để xử lý. Không có TC nào verify hành vi khi param bị trùng → nguy cơ callback URL bị **duplicate param** hoặc set sai giá trị. → **Đề xuất**: TC-NEW-02.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify — `01-bug-task.md`**: File auto-filled `2026-06-13 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Yêu cầu tester đọc lại detail Redmine #37507 (description + journals) và tick trước khi review có giá trị.

- **[MAJOR] AUTO-FILL chưa verify — `03-dev-impact.md`**: Tương tự, checkbox CHƯA tick. F1/T1/T2 có thể chưa đầy đủ/mapping sai — yêu cầu tester verify lại Section "Đánh giá ảnh hưởng" Redmine và tick.

- **[MAJOR] [AP-6] Mục 3 dev-impact trống (caller chưa list)**: Mục "Đã check và sửa các function sử dụng đến function/data vừa sửa" chỉ có heading, không list caller. → Yêu cầu Dev list các nơi build URL callback (follow event, postback, các friend-state path) để xác định có function khác cùng pattern bug cần fix/test không. Liên quan trực tiếp BLOCKER-1.

- **[MAJOR] SYMPTOM-ONLY (AP-2) — forward_param rỗng/null chưa verify**: Dev tự hỏi "Case forward_param rỗng hoặc null có cần set không?" — chưa chốt và chưa có TC. → Đề xuất TC-NEW-03 (URL không gắn custom param + không setting param info → callback không bị thêm `&` rỗng / forward_param thừa / lỗi).

- **[MAJOR] T2 — chưa verify đủ 5 param auto-set**: Dev ghi case URL không setting → "Set hết forward_param, mail, friend_name, friend_type, line_id". TCs (2940–2948, 2976) tập trung custom param + "add all param ucid mặc định" nhưng **không có Expected liệt kê đủ 5 param** (mail/friend_name/friend_type/line_id) thực sự xuất hiện trong callback. → Bổ sung Expected cụ thể, hoặc TC riêng verify đủ 5 param (xem TC-NEW-05).

- **[MAJOR] Expected result để trống ở nhiều dòng**: Rất nhiều dòng không có Expected (2920–2925, 2927–2939, 2959–2974, và các dòng biến thể param 2941–2948 / 2950–2957). Kể cả khi Expected "kế thừa" từ dòng cha theo convention Sheet, các nhánh friend-state (old/đang friend) **không có Expected ở bất kỳ dòng cha nào** → không đo được kết quả. → Điền Expected rõ ràng, đo lường được cho từng nhánh.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Thiếu cột chuẩn TC ID / Type / Priority / Precondition**: File 04 fetch từ Sheet phân cấp, không có 4 cột này → khó trace coverage & ưu tiên. Đề nghị khi đưa vào review chính thức, bổ sung tối thiểu Precondition (account, bot, landing đã setting tab パラメーターエクスポート + request bin URL) cho mỗi block.

- **[MINOR] Title/Sub generic ở vài dòng**: vd 2975 "check khi setting param[...]" — `[...]` không rõ param gì; Expected "Không replace được" cần nêu rõ param nào không replace và vì sao (đúng spec hay là bug).

### 4.4 Nit (gợi ý)

- **[NIT] CL13 (Line Friend access link)**: QR landing thuộc nhóm tính năng access link tool LME. Cân nhắc thêm TC mở landing qua **in-app LINE / trình duyệt ngoài / PC** để confirm forward_param truyền nhất quán giữa các kênh mở (xem TC-NEW-06). Không bắt buộc nếu fix không đụng tầng redirect kết bạn.

- **[NIT] Tách annotation khỏi vùng TC**: Dòng 2938/2939 là text đánh giá ảnh hưởng + tái hiện nằm lẫn trong dải TC — khi sync nên để ở ô ghi chú riêng, tránh bị đếm nhầm là TC.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Friend CŨ / đang là friend quét QR landing có custom param (URL không setting param info) → forward_param vào callback | Bot có QR landing `...&sid=<base64>&test=true`; tab パラメーターエクスポート setting URL request bin, KHÔNG setting `{forward_param}`/ucid; account test **đã là friend từ trước** | 1. Friend cũ quét QR (hoặc nhấn link) Action có gắn `sid`, `test` <br>2. Mở request bin xem callback | Callback nhận **đủ** custom param (`sid`, `test`) đúng giá trị — giống hệt case friend mới. Nếu KHÔNG nhận → fix `doHandleFollowEvent` chưa cover path friend cũ ⇒ báo Dev | High | Regression / BUG | F1, BUG (trigger path) |
| TC-NEW-02 | Param trùng: URL Action đã chứa sẵn `sid` + forward_param cũng có `sid` | Như trên; URL Action gắn sẵn `?sid=AAA`, forward_param config trả `sid=BBB` | 1. Friend quét QR <br>2. Xem callback URL ở request bin | Callback **không bị duplicate** `sid` (không ra `sid=AAA&sid=BBB`); giá trị cuối đúng theo spec đã chốt (ghi rõ AAA hay BBB) | High | Boundary / Negative | T1 (Dev Q2 + commit AI review) |
| TC-NEW-03 | forward_param rỗng/null + URL không setting param info | Tab パラメーターエクスポート setting URL request bin, không setting param nào; URL Action **không** gắn custom param | 1. Friend quét QR (không param tự nhập) <br>2. Xem callback | Callback không bị thêm `forward_param=` rỗng / `&` thừa / lỗi 4xx-5xx; chỉ chứa param ucid mặc định hợp lệ | Medium | Boundary | BUG, T2 (Dev Q1) |
| TC-NEW-04 | Reproduce đúng case KH (QR Action メディア03) | Tái hiện đúng setup KH journal 11/6 | 1. Tạo/QR Action giống メディア03 gắn param động `sid` <br>2. Friend quét lúc thực tế <br>3. Kiểm tra **URL thực tế** lúc truy cập (log `detail_landing_click` landing_id) + callback | URL thực tế có gắn `sid`; callback nhận `sid`. Khớp với DB `detail_landing_click` | High | Positive / BUG | BUG |
| TC-NEW-05 | Case URL không setting param info → callback set ĐỦ 5 param | Tab パラメーターエクスポート không setting `{...}` nào | 1. Friend (mới) quét QR <br>2. Xem callback | Callback chứa **đủ**: forward_param + `mail` + `friend_name` + `friend_type` + `line_id` (giá trị đúng từng cái) | High | Positive | T2 |
| TC-NEW-06 | Mở QR landing đa kênh → forward_param nhất quán | Landing như TC-NEW-01 | Mở/quét QR qua: in-app LINE / trình duyệt ngoài / PC | Cả 3 kênh: callback nhận custom param như nhau | Low | Compatibility | F1 / CL13 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — nhưng **cần chốt 2 business rule** Dev còn để ngỏ (đề nghị PM/Dev xác nhận, ghi lại vào spec QR/Parameter Export):
  - Khi `forward_param` rỗng/null: có set vào URL callback hay bỏ qua?
  - Khi param trùng (URL đã có sẵn `sid` + forward_param cũng `sid`): ưu tiên giá trị nào? (giá trị URL gốc hay forward_param?)
- [ ] Cần update spec — N/A

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG: RISK; A.2 F1: RISK (thiếu path friend cũ); A.3 D: N/A; A.4 T1/T2: RISK; A.5 không có orphan; A.6 fix-shape: 2 BLOCKER
- [x] B. Chất lượng từng TC — B.1 fail (Expected trống nhiều dòng); B.4 data sample tốt (param thật, JP/emoji)
- [x] C. Chất lượng bộ TC tổng thể — thiếu Type/Priority phân bổ; tốt phần input variant
- [x] D. Spec alignment — không mâu thuẫn spec; 2 rule cần chốt (xem §6)
- [x] E. Hành chính — file 04 đúng folder; **thiếu tên tester + version**; thiếu TC ID chuẩn
- [x] F. Base checklist LME
  - [x] F.1 Web — **CL6 Data input** (special/JP/emoji/space/0): ✅ cover tốt. **CL13 Line Friend access link**: liên quan, chưa cover đa kênh (NIT, TC-NEW-06). CL11/CL10 (CRUD đúng account / impact friend info): chưa verify rõ.
  - [x] F.2 Job — **B.1 Job callback**: task chạm callback (request bin) ✅ có verify nội dung callback; không có concern rate-limit/retry (không phải Google sync) → B.2 N/A.
  - [x] F.3 Các tính năng chung — **C.3 Friend info** (Job: QR landing set import param → update sau kết bạn): liên quan, các param `line_id/friend_name/mail/friend_type` có trong scope nhưng chưa verify đủ (xem MAJOR T2). C.5 Google sheet: N/A (callback là request bin, không phải spread). C.1/C.2/C.4/C.7/C.8: N/A.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
