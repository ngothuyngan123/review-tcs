# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36585 — `[20-05-2026][10965][Media (image,video...)] Hình ảnh từ friend 「石丸雅司」 gửi không xem được trên app` |
| Reviewer (Leader) | `<Leader fill>` |
| Tester được review | `<member fill — file 04 chưa ghi>` (TCs source: fetched từ Sheet `Content message` tab, row 252–272) |
| Ngày review | 2026-05-22 |
| Version TCs | v1 (auto-fetched từ Redmine Link TCs) |
| Vòng review | Round 1 |

> Note: file 02 (spec-reference) không có trong folder. Dùng [LME-SYSTEM-SPEC tổng](../../templates/LME-SYSTEM-SPEC.md) làm reference; không có spec riêng cho "Chat 1:1 message display trên mobile app" — chỉ có note trong sheet TC gốc trỏ Figma `mobile-chat-11`.

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TCs hiện tại cover được 4 trigger biết-trước (image / video / audio / pdf-docx) nhưng **thiếu TC fallback cho type CHƯA BIẾT** trong khi mục 2 dev-impact là fix dạng **add-case dispatch** (generic-like) → dính AP-1. Ngoài ra: file 01/03 chưa được tester verify auto-fill (checkbox unticked), mục 3 dev-impact trống, mục Commit/PR trống, mọi TC trống cột Steps/Precondition/Type/Priority — không chạy được.

---

## 2. Tóm tắt cho member

Bộ 19 TC bạn cung cấp đã cover khá đầy đủ ma trận **media type × (gửi mới / gửi dạng file / nhiều mess liên tiếp / message cũ)** — đây là điểm tốt: dimension matrix thinking đúng. Tuy nhiên trước khi merge cần fix 3 nhóm: (1) **bổ sung TC fallback** cho message type CHƯA BIẾT (vì fix là add-case dispatch, không phải hardcoded list) + alternative root cause (link hỏng / file lớn / filename JP chars); (2) **điền đủ Steps / Precondition / Type / Priority** cho mọi TC — hiện đang trống nên không chạy được; (3) **verify lại auto-fill** từ Redmine (tick 2 checkbox trong file 01 + 03), hỏi Dev list caller cho mục 3 và list cụ thể các màn khác hiển thị message trên app cho impact T2.

---

## 3. Coverage Matrix

> Xem cách dùng trong [../../framework/coverage-matrix.md](../../framework/coverage-matrix.md). Mapping suy luận từ Title / Sub-function của TC.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause: API trả object cho message type file → app hiển thị xám) | Fix | — | TC002 (gửi ảnh dạng image file — đúng flow KH `石丸雅司` đính kèm) | 1 | OK |
| F1 — `getListMessageByUserV4` (ChatController.php) | Function | Direct | TC001-TC018 (mọi TC đều đi qua API list message cho chat 1:1 trên app) | 18 | **RISK** (thiếu negative: type chưa biết, content_type mismatch, link hỏng) |
| D — (Dev: "k có" — chỉ sửa transform response) | Data | — | N/A | 0 | OK |
| T1 — Hiển thị ảnh / video / audio / pdf / file trên chat 1:1 ở app | Feature | High | TC001-TC005 (ảnh), TC006-TC010 (video), TC011-TC015 (audio), TC016-TC017 (pdf/docx), TC018 (other types do bot send), TC019 (cross-OS) | 19 | **RISK** (chưa cover: filename JP/special chars; message do user gửi vs do bot gửi; case friend block) |
| T2 — "Các chỗ khác hiển thị message trên app" (Dev tự note: "check thêm còn chỗ nào hiển thị message trên app nữa k") | Feature | Medium | — | 0 | **GAP** (T2 mơ hồ, cần Dev cụ thể hóa list màn: push notification preview / chat reply screen / message history / multi-friend list...) |

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC019 | Check trên cả 2 loại máy android và ios | Không phải 1 TC độc lập mà là **scope/precondition cho tất cả TC khác**. Hiện viết generic không nói chạy TC nào trên 2 OS → tester sẽ skip hoặc chỉ smoke 1 lần | **Rename** thành matrix: thêm cột "Device" trong precondition của TC001-TC018, hoặc duplicate TC quan trọng (TC002, TC006, TC011) chạy 1 lần Android + 1 lần iOS |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Validation / Add-case dispatch** (generic-like). Cụ thể: (a) "Thêm case type message = video vì đang bị thiếu" — switch/case theo `type`; (b) "Kiểm tra file nếu là dạng ảnh hoặc video thì set content = link" — conditional dispatch theo file kind. Đây là pattern dễ dính AP-1: code mới có thể là `switch (type) { case 'image': ... case 'video': ... default: object }` → mọi type không thuộc list vẫn fail. |
| Trigger space cần cover | LINE message types chính: `text / image / video / audio / file / sticker / location / button (template) / flex / postback`. Plus file content variants: `image` (jpg/png/heic/webp) / `video` (mp4/mov) / `audio` (m4a/mp3) / `document` (pdf/docx/xlsx) / `archive` (zip/rar) / `unknown MIME`. Plus mismatch case: file extension ≠ content_type. |
| Số trigger TCs hiện cover | **4 trigger biết-trước / nhiều hơn**: image (TC001-005), video (TC006-010), audio (TC011-015), pdf-docx (TC016-017). **Cover other-types từ bot** chỉ qua TC018 (sticker/location/button do bot send) nhưng KHÔNG cover other-types do **user** gửi. **0 TC cho unknown/fallback type** (vd: nếu LINE update thêm message type mới). |
| KH report dạng | **Symptom-only**. File 01 "Mô tả bug": "Hình ảnh được gửi từ friend 「石丸雅司」 không hiển thị được trên app." + Actual: "Màn hình chat 1:1 phía app hiển thị màn hình xám" → KH chỉ thấy hiện tượng (màn xám), không nêu error code / log. Dev đoán root cause = "api trả object thay vì link". |
| Alternative root causes cần verify | (1) Link CDN expired (LINE host timeout); (2) File quá lớn → app timeout; (3) Filename chứa JP/special chars (KH report `石丸雅司`) → URL encode lỗi; (4) Mismatch `content_type` vs file extension; (5) App permission storage / network; (6) Network slow trên mobile data; (7) Message với type LINE mới (vd: voice message ≠ audio). |
| Anti-patterns dính | **AP-1** (single-trigger generic-fix — thiếu unknown trigger fallback), **AP-2** (symptom-only KH report — chưa cover alt root cause), **AP-4** (Commit/PR trống — không verify được code thực sự là generic dispatch hay specific check), **AP-6** (mục 3 dev-impact chỉ có heading, không list caller). |

> Trigger space cover **4 / ~7-10** → flag [BLOCKER] FIX-SHAPE trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — `GAP-1`**: Fix mục 2 dạng add-case dispatch (`switch type` / conditional set content) nhưng **không có TC nào trigger với message type CHƯA BIẾT**. Per memory `feedback_generic_fix_detection`: generic-fix cần ≥ 3 trigger + ≥ 1 unknown fallback. Hiện cover 4 known triggers (image / video / audio / file) — đủ phần ≥ 3 — nhưng **thiếu unknown fallback**. → Bổ sung TC-NEW-01 (xem §5) — verify case message type lạ (vd: type mới LINE chưa support / message từ bot khác platform / corrupt type field) thì app hiển thị thế nào (fallback graceful vs crash).
- **[BLOCKER] AP-1 — `GAP-2`**: Cùng nguyên nhân trên — bổ sung **TC trigger với `content_type` mismatch file extension** (vd: file `.jpg` nhưng `content_type=application/octet-stream`, hoặc upload `.mp3` rename thành `.png`). Nếu fix là `if file is image OR video → set content = link` thì điều kiện check "is image" dựa vào gì? Extension hay MIME? Nếu MIME-only và file bị mismatch → vẫn dính bug cũ. → TC-NEW-02.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL UNVERIFIED — `file 01-bug-task.md`**: "Auto-filled: 2026-05-22 by /new-task" có giá trị nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick. Bug task auto-filled từ Redmine có thể sót journal / attachment / custom field quan trọng. → Yêu cầu tester đọc lại Redmine #36585 (đặc biệt 2 attachments: `スマホで見た時.png`, `SnapCrab_NoName_2026-5-20_11-10-20_No-00.png`) và tick checkbox trước khi review có giá trị.
- **[MAJOR] AUTO-FILL UNVERIFIED — `file 03-dev-impact.md`**: Tương tự, checkbox chưa tick. Dev impact auto-fill có nguy cơ F/D/T sót hoặc mapping sai (đặc biệt mục 3 đang trống, mục 4.3 dòng 2 "check thêm chỗ nào hiển thị message" mơ hồ). → Tester verify lại + hỏi Dev bổ sung mục 3 (caller list) và cụ thể hóa T2.
- **[MAJOR] SYMPTOM-ONLY (AP-2) — `GAP-3`**: KH chỉ ghi "không hiển thị được" (symptom). Dev tái hiện root cause = API trả object cho type=file. Cần TC cho ≥ 2 plausible alt root causes — đặc biệt **filename JP chars** (KH bug name là `石丸雅司`, có thể URL encode lỗi gây fail riêng cho friend có JP name) và **link CDN expired** (test reload message cũ sau khi link LINE expired). → TC-NEW-03, TC-NEW-04.
- **[MAJOR] AP-4 — `GAP-4`**: Mục "Commit / Pull Request" trong file 03 trống. Không verify được fix thực sự là generic dispatch hay specific code-check chỉ list 2 types `image | video`. → Yêu cầu Dev cung cấp PR link để Leader đọc diff.
- **[MAJOR] AP-6 — `GAP-5`**: Mục 3 file 03 "Đã check và sửa các function sử dụng đến function/data vừa sửa" chỉ có heading, không có function nào được list. Có nguy cơ caller khác cùng pattern bug (vd: API list message cho chat group, chat broadcast, message history export). → Yêu cầu Dev list caller cụ thể.
- **[MAJOR] TC FORMAT — mọi TC (TC001-TC019)**: Cột **Steps / Precondition / Type / Priority / Assignee / Status** trống. TC không có Steps → không chạy được. TC không có Precondition → tester không biết setup gì (cần bot account + friend account đã add, đã có message cũ pre-seed cho TC "message cũ" series). → Member điền đủ trước khi review tiếp.
- **[MAJOR] T2 KHÔNG CỤ THỂ — `GAP-6`**: Mục 4.3 dòng 2 ("check thêm còn chỗ nào hiển thị message trên app nữa k") là TODO Dev đẩy cho QA. Trên LINE-app side có ít nhất: chat 1:1 main / chat 1:1 reply screen / message history (scroll up) / notification preview / multi-friend list preview. → TC-NEW-05 bổ sung regression cho 1-2 màn chính, hoặc Leader chốt với Dev bỏ qua T2 nếu không thuộc scope fix.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC019 generic**: "Check trên cả 2 loại máy android và ios " viết dạng matrix, không phải TC độc lập. → Rename thành "(Compat) TC002 + TC006 + TC011 chạy song song trên Android + iOS" hoặc move sang Precondition.
- **[MINOR] TC số nhiều "nhiều ảnh/video/audio liên tiếp"** (TC003, TC008, TC013): không quantify "nhiều" — 2, 5, 10, 50? → Cụ thể hóa số: "≥ 5 ảnh gửi cách nhau < 2s".
- **[MINOR] TC004/TC005 và TC009/TC010 "message cũ"**: không define "cũ" là bao lâu (trước fix? trước migration? sau N giờ?). → Định nghĩa "cũ" = "tin nhắn user gửi trước thời điểm deploy fix".

### 4.4 Nit (gợi ý)

- **[NIT]** TC title nên có prefix `[App]` hoặc `[Chat 1:1]` để khi sort theo title trong Sheet master không lẫn với TCs của các tab khác.
- **[NIT]** "TC001 Check user gửi message ảnh" → nên đổi thành "TC001 [App][Chat 1:1] User gửi ảnh dạng image (not file) → app hiển thị được preview" để Leader scan title đủ hiểu.
- **[NIT]** TC018 "message type text, sticker, location, button, media do bot send cho user" — list 5 type trong 1 TC = 1 TC verify 5 thứ. Có thể tách 5 TC riêng (nhưng minor vì các type này không nằm trong scope fix).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | [Chat 1:1][App] Unknown message type fallback — verify app không crash khi nhận message với type chưa support | Bot + friend account đã add. Dev (hoặc backend simulation) inject message với `type` không nằm trong list known (vd: type="future_type_v6", "voice", "video_call_record" — tùy LINE roadmap). | 1. Friend → bot gửi 1 message dạng known (text) — verify hiển thị OK. 2. Dev/backend simulate inject 1 message với `type` lạ vào response của `getListMessageByUserV4`. 3. User mở chat 1:1 → reload list message. | App hiển thị **fallback graceful** cho message type lạ — không crash, không màn xám toàn screen. Có thể hiển thị placeholder "Message này không hỗ trợ trên phiên bản app hiện tại" hoặc bỏ qua message đó nhưng các message khác vẫn hiển thị bình thường. | High | Boundary / Negative | F1, BUG fallback |
| TC-NEW-02 | [Chat 1:1][App] Mismatch content_type vs file extension — verify fix dùng MIME hay extension | Bot + friend. Friend upload file `.jpg` nhưng MIME header = `application/octet-stream`; và 1 file `.mp3` đổi tên thành `.png`. | 1. Friend → bot gửi file `.jpg` với MIME `application/octet-stream`. 2. Friend → bot gửi file `audio.png` (thực ra là mp3 rename). 3. User mở chat 1:1. | App **không** hiển thị màn xám (bug cũ). Behavior cụ thể: hoặc hiển thị image preview nếu Dev dùng extension; hoặc hiển thị download link nếu Dev dùng MIME (Leader verify với Dev xem là behavior nào đúng spec). | High | Negative / Boundary | F1, BUG variant |
| TC-NEW-03 | [Chat 1:1][App] Filename JP / special chars — verify URL encode khi friend có tên JP gửi file | Friend account có display name JP (vd: "石丸雅司"), gửi file có filename JP (vd: "スマホで見た時.png"). | 1. Friend "石丸雅司" upload file "スマホで見た時.png" gửi cho bot. 2. User mở chat 1:1 trên app. | Ảnh hiển thị bình thường (KH bug name là `石丸雅司` — verify chính xác case KH). Filename JP không gây URL encode error. | High | Positive / Regression | F1, BUG (exact KH case) |
| TC-NEW-04 | [Chat 1:1][App] Link CDN expired — verify behavior khi xem message cũ link đã hết hạn | Friend gửi ảnh từ N tháng trước (link LINE CDN có thể đã expire). | 1. Scroll lên message cũ trong chat 1:1. 2. Tap vào ảnh để xem full. | Có hành vi **rõ ràng**: hoặc reload từ LINE API (set content = link mới); hoặc hiển thị placeholder "Ảnh này không còn khả dụng" — KHÔNG hiển thị màn xám / crash. | Medium | Negative / Boundary | F1, alt root cause |
| TC-NEW-05 | [App] Message preview ở push notification — verify type=file của user vẫn hiển thị thumbnail / icon | Bot + friend, app cài notification on. | 1. Friend → bot gửi 1 ảnh dạng image file. 2. User chưa mở app → check push notification trên lock screen. 3. Mở notification → vào chat 1:1. | Push notification hiển thị thumbnail hoặc icon "📷 Image" thay vì empty. Chat 1:1 hiển thị ảnh bình thường khi mở. (T2 — chỗ khác hiển thị message). | Medium | Regression | T2 |
| TC-NEW-06 | [Chat 1:1][App] File size boundary — verify ảnh siêu lớn vẫn hiển thị | Friend account có khả năng upload ảnh ≥ 10MB. | 1. Friend upload ảnh 10MB và 20MB. 2. User mở chat 1:1. | Cả 2 ảnh hiển thị được (có thể có loading state). Không màn xám. Verify cả Android + iOS vì giới hạn memory khác nhau. | Medium | Boundary | F1, alt root cause |
| TC-NEW-07 | [Chat 1:1][App] Friend block — verify message cũ từ friend đã block | User block friend → check message cũ. | 1. Friend gửi 1 ảnh dạng image file. 2. User mở chat → ảnh hiển thị. 3. User block friend. 4. User mở lại chat. | Verify behavior theo C.2 LME checklist (friend block). Message cũ hiển thị bình thường hay bị mask? (Leader confirm với spec.) | Low | Regression | C.2 LME |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec
- [ ] Cần update spec — chi tiết: (N/A — bug là behavior bug, không phải spec mismatch. Spec chuẩn ở Figma `mobile-chat-11` không nói "user gửi file dạng image phải hiển thị xám".)

> Note: Spec gốc cho chat 1:1 trên mobile app KHÔNG nằm trong [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) (spec chính phục vụ admin web). Nguồn truth duy nhất cho mobile app là Figma + sheet `TCsLine_Mobile_Chat 1:1`. Leader nên đề xuất với PM tạo `02-spec-reference.md` riêng cho 38 màn mobile app trước các task chat 1:1 sau.

---

## 7. Checklist đã chạy

- [x] A. Coverage — **partial pass**: A.1 (BUG cover qua TC002), A.2 F1 (RISK — thiếu negative), A.3 N/A, A.4 T1 (RISK — thiếu i18n/edge), A.4 T2 (GAP), A.5 (1 orphan: TC019), A.6 fail (xem §3.5)
- [x] B. Chất lượng từng TC — **fail**: B.1 (Steps/Precondition trống), B.2 OK, B.3 OK, B.4 (TC003/008/013 không quantify "nhiều")
- [x] C. Chất lượng bộ TC — **partial**: 0% negative/boundary, 100% positive-ish. Type column trống không phân loại được tỷ lệ chính xác.
- [x] D. Spec alignment — không có file 02, dùng LME-SYSTEM-SPEC fallback, không phát hiện mâu thuẫn.
- [x] E. Hành chính — TC IDs OK (TC001-TC019). File 04 trong đúng folder. Tester ký tên TRỐNG.
- [x] F. Base checklist LME (kiểm tra member đã tuân [checklist-lme.md](../../framework/checklist-lme.md) chưa)
  - F.1 Checklist web — **N/A** (bug ở app side, không phải web)
  - F.2 Checklist job — **N/A** (không chạm callback / Google sync)
  - F.3 Các tính năng chung:
    - C.2 Send message (4 app cases): **partial** — TC cover happy path nhưng thiếu **case message error** và **case friend block**. → TC-NEW-07 (block). Leader chốt có cần case message error (timeout, retry) không.
    - C.3-C.8: N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

## Phụ lục — Trace mapping TC → Impact (suy luận)

| TC | Title (rút gọn) | Map BUG | Map F1 | Map T1 | Map T2 | Note |
|---|---|---|---|---|---|---|
| TC001 | Ảnh — gửi image (not file) | (close) | ✓ | ✓ | | Positive — type=image known |
| TC002 | Ảnh — gửi image file | ✓ EXACT | ✓ | ✓ | | **Bug repro** đúng flow KH |
| TC003 | Ảnh — nhiều liên tiếp | | ✓ | ✓ | | Boundary multi-message |
| TC004 | Ảnh cũ dạng image | | ✓ | ✓ | | Regression message cũ |
| TC005 | Ảnh cũ dạng image file | | ✓ | ✓ | | Regression + repro cũ |
| TC006-010 | Video (5 variant) | | ✓ | ✓ | | Tương tự ảnh |
| TC011-015 | Audio (5 variant) | | ✓ | ✓ | | Tương tự ảnh |
| TC016 | File pdf/docx mới | | ✓ | ✓ | | Verify file không bị nhầm thành image |
| TC017 | File pdf/docx cũ | | ✓ | ✓ | | Regression file cũ |
| TC018 | Bot send other types | | ✓ | ✓ | | Regression types không trong scope fix |
| TC019 | Android + iOS | | | | | Orphan / matrix scope |
