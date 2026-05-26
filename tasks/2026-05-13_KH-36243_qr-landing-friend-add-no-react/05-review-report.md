# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | KH #36243 (回答ID 10810) |
| Reviewer (Leader) | _<điền>_ |
| Tester được review | _<chưa xác định — sheet không có cột Assignee fill>_ |
| Ngày review | 2026-05-13 |
| Version TCs | v1 (Google Sheet Improve 1.0 rows 3492-3548) |
| Vòng review | Round 1 |

> **Note đầu vào**:
> - **01-bug-task.md** auto-filled từ Redmine #36243 ngày 2026-05-13 nhưng **CHƯA TICK verify** → flag [BLOCKER] (xem §4.1).
> - **02-spec-reference.md**: Không có spec riêng → fallback `templates/LME-SYSTEM-SPEC.md`.
> - **03-dev-impact.md** auto-fill từ journal #118286 (Ngần). Nội dung dev mơ hồ — không trace được "check liff login" là logic gì → flag [BLOCKER] (xem §4.1).
> - **04-tc-list.md** convert từ Google Sheet nested checklist (rows 3492-3548) → 49 TCs. Nhiều TC có Expected inherit visual rỗng.
> - **Bug đặc thù**: root cause là **LINE-side bug** (Android 26.6.0/26.6.1 edge-to-edge support). LINE Developers đã announce (https://developers.line.biz/ja/news/2026/05/11/liff-outage/). LME fix là workaround → TC phải cover device matrix LINE Android version cụ thể.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có nhiều BLOCKER không thể approve. Cần fix trước khi review Round 2.

**Lý do**: (a) Dev impact 03 mơ hồ, không trace được logic fix → TC không verify được. (b) Bộ TC 49 cái cover rộng "QR landing flow" nhưng **thiếu chính xác bug context**: không TC nào test **LINE Android 26.6.0/26.6.1** (version specific gây bug), không TC nào tách riêng **QRCA** (1 trong 2 case KH gốc), expected hầu hết inherit rỗng. (c) Tester verify auto-fill Redmine chưa tick. (d) Bug fix LME chỉ là workaround cho LINE-side bug → cần test matrix LINE version để confirm fix work + không regress LINE iOS / LINE Android version cũ.

---

## 2. Tóm tắt cho member

Em đã viết bộ TC **rất chi tiết** cho QR landing (matrix friend new/old/unblock × device iOS/Android × source quét/click × position list/detail/LP — 40+ case) — đây là điểm tốt cho regression toàn feature. **Tuy nhiên thiếu chính xác bug context**: bug KH là **device-specific với LINE Android 26.6.0/26.6.1 edge-to-edge** nhưng không TC nào ghi rõ LINE version cần test, không có TC tách riêng case **QRCA** (1/2 case KH), và 35+ TC có Expected inherit rỗng do format sheet visual. Em cần (a) **làm rõ với dev** logic "check liff login" cụ thể là gì → mới viết được Expected đo lường được, (b) bổ sung 8 TC ở §5 (LINE version matrix, QRCA dedicated, iOS baseline regression, logic LIFF login check, OA profile page, CL18 load-before-deploy, device matrix, send action sau add friend), (c) fill đầy đủ Expected cho 35+ TC inherit rỗng, (d) tick "Tester verify auto-fill" sau khi đọc lại Redmine.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — Reproduce KH (Android tap btn 友だち追加 không phản hồi) | Fix | — | TC-01 (cover flow nhưng **không nêu LINE Android version specific**) | 1 | **RISK** |
| **F1** — `liff_callback.blade.php` (LIFF callback render) | Function | Direct | TC-07..46 (cover gián tiếp qua quét QR/click link kích hoạt callback) — **không có TC direct verify logic check LIFF login** | 40 (gián tiếp) | **RISK** |
| **T1** — Add friend qua **Landing QR Code** | Feature | High | TC-02..06 (Landing all) + TC-07..16 (Friend new) + TC-17..26 (Friend old chưa tồn tại) + TC-27..36 (Friend old đã tồn tại) + TC-37..46 (Friend unblock) | 45 | **OK** (rộng) — nhưng nhiều TC inherit rỗng |
| **T2** — Add friend qua **QR Code Action (QRCA)** | Feature | High | _Không có TC nào ghi "QRCA" specific_ — TC test "landing QR" chung, không tách QRCA dù KH report đúng case này | 0 dedicated | **GAP** |
| **T3** — Add friend qua **LINE OA profile page button** | Feature | Medium | _Không có TC nào cover_ — dev report loại scope, nhưng KH context có nhắc (journal #117779: "nút trên trang profile của LINE Official Account không phản hồi") | 0 | **GAP** |
| _Hidden_ — **LINE Android version matrix** (26.6.0/26.6.1 vs 15.13.1/15.15.1 vs 26.3.0+) | Behavior | High | _Không có TC nào nêu version specific_ — bug device-specific theo LINE version | 0 | **GAP** |
| _Hidden_ — **Logic check LIFF login** (cách fix dev đề xuất) | Function | Direct | _Không có TC direct verify_ — dev mô tả mơ hồ, member chưa viết TC tương ứng | 0 | **GAP** |
| _Hidden_ — **Send action sau add friend** (C.2 Send message) | Feature | Medium | TC-07/11/17/21/27/31/37/41 mention expected "send action sau add bot" nhưng **gián tiếp**, không TC dedicated | 0 dedicated | **RISK** |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-47 | "Landing new friend" | Header rỗng, sheet chỉ có title (column B), không có sub-content | Fill content (precondition + steps + expected) HOẶC xóa nếu trùng TC-07/17/27/37 |
| TC-48 | "Landing Copy" | Header rỗng, không rõ scope (copy landing? copy QR?) | Fill content HOẶC xóa |
| TC-49 | "Check account staff" | Header rỗng (giống pattern TC-07 ở task #36365) — có thể là CL1 staff permission | Convert thành TC CL1: "Staff không phân quyền không access modal landing QR" + "Staff có quyền tạo landing được" |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] BUG-1: Tester verify auto-fill Redmine CHƯA TICK** — `01-bug-task.md` auto-filled từ Redmine ngày 2026-05-13 nhưng checkbox "Tester verify auto-fill chính xác" còn rỗng. Theo quy tắc `/review-tc`: **review không có giá trị final** cho tới khi tester đọc lại Redmine 36243 (description + 5 journals + 3 attachments) và tick checkbox. **Fix**: Tester verify + tick.

- **[BLOCKER] DEV-1: Dev impact 03 mơ hồ, không trace được logic fix** — Journal #118286 ghi "check liff login của liff app khi mở trên Android" — không nêu (a) detect Android version thế nào, (b) check LIFF login state ra sao, (c) action gì khi check fail (re-login? thêm padding? move button?), (d) behavior change UI cụ thể. Member viết Expected không được vì không biết logic. **Fix**: Leader hỏi dev clarify 4 điểm trên, update 03-dev-impact.md trước khi member viết TC version 2.

- **[BLOCKER] GAP-1: LINE Android version matrix** — Root cause specific: LINE Android 26.6.0/26.6.1 (LINE iOS 15.13.1/15.15.1 KHÔNG reproduce — journal #117779). **TC hiện tại không TC nào nêu LINE version** → tester có thể test trên version sai → miss reproduce / miss verify fix. **Fix**: Bổ sung `TC-NEW-01` (LINE Android 26.6.0/26.6.1 reproduce bug **trước fix**) + `TC-NEW-02` (verify fix trên cùng version) + `TC-NEW-03` (regression LINE iOS không bị ảnh hưởng) ở §5.

- **[BLOCKER] GAP-2: QRCA specific case không có TC** — KH report đúng case này: "**1 case khi add qua QRCA**". Đây là 1/2 case gốc của bug. TC trong sheet chỉ test "QR landing" generic, không tách QRCA. **Fix**: Bổ sung `TC-NEW-04` ở §5 — QRCA specific flow (action sau khi add friend qua QR Code Action, không phải QR landing thường).

- **[BLOCKER] TC-01 Expected mơ hồ + không nêu LINE version** — Title "Tái hiện case KH" reproduce flow nhưng Expected chỉ "Click btn kết bạn phải phản hồi và add friend thành công (sau fix)". Không nói (a) LINE Android version nào test, (b) device hardware cụ thể (Pixel? Galaxy? versioncm Android OS?), (c) verify gì khi tap (chỉ tap có phản hồi? hay phải add friend được hoàn chỉnh? hay phải nhận message action sau đó?). **Fix**: Rewrite TC-01 chi tiết theo TC-NEW-01/02 ở §5.

- **[BLOCKER] GAP-3: Logic "check LIFF login" — không có TC direct verify** — Cách fix dev là "check liff login khi mở LIFF app trên Android". KHÔNG có TC nào test trực tiếp logic này: (a) khi nào trigger check, (b) behavior nếu chưa login (re-login UI?), (c) behavior nếu login fail. **Fix**: Bổ sung `TC-NEW-05` ở §5 (sau khi dev clarify logic).

### 4.2 Major (nên fix)

- **[MAJOR] TC-03/04/06/08-10/12-16/18-26/28-36/38-46 Expected inherit rỗng** — **35+ TC** (≈ 70%) có cột Expected ô rỗng do sheet visual inherit từ TC parent (TC-07, TC-11, TC-17, TC-21, TC-27, TC-31, TC-37, TC-41). Khi tester chạy theo file 04 (không xem sheet visual) → không biết expected gì → không reproducible. **Fix**: Member fill từng cell Expected (copy expected của parent) khi convert sang `04-tc-list.md` standalone — đặc biệt quan trọng vì sheet master sẽ là source of truth.

- **[MAJOR] GAP-4: LINE OA profile page button không cover** — Journal #117779 nhắc rõ "**nút trên trang profile của LINE Official Account không phản hồi thao tác nhấn**". Dev report loại scope (chỉ scope LIFF callback), nhưng nếu LME có button "Add friend" trên LINE OA profile được generate qua tool → có thể cùng vùng bị che. **Fix**: Verify với dev → nếu có liên quan → bổ sung `TC-NEW-06`.

- **[MAJOR] Mất cân đối Positive/Negative/Boundary/Regression** — Đếm 49 TC: **41 Positive / 5 Negative (landing off) / 0 Boundary / 1 Regression (TC-01) / 2 unknown (TC-47/48)**. Tỷ lệ chuẩn gợi ý 30/25/25/20. **Thiếu**: (a) Boundary device (LINE version edge: 26.5.x vs 26.6.0 vs 26.7.x — fix work cho version nào?), (b) Negative (mạng yếu khi tap, friend đã add rồi tap lại), (c) Regression đầy đủ cho T1 (test fix không break flow LINE iOS, version Android cũ). **Fix**: Bổ sung TC-NEW-03 (iOS regression) + TC-NEW-07 (Android version range boundary).

- **[MAJOR] TC-47, TC-48, TC-49 lạc chủ đề / rỗng** — Title-only, không có precondition/steps/expected (xem ORPHAN). **Fix**: Member fill nội dung HOẶC xóa.

- **[MAJOR] Compatibility (Non-function checklist LME §A.2)** — Bug LÀ device-specific (Android). **PHẢI test matrix device thật**: ít nhất Pixel (Google), Galaxy (Samsung), Xperia (Sony) với LINE Android version 26.6.0 + 26.6.1. **Hiện tại** không TC nào nêu device hardware. **Fix**: Bổ sung `TC-NEW-08` (device matrix).

- **[MAJOR] CL18 (load UI trước, submit sau)** — Standard release checklist LME: cần verify case "user mở landing QR trước khi deploy fix → fix deploy → user tap button → vẫn hoạt động không cần reload". **Fix**: Bổ sung `TC-NEW-09`.

- **[MAJOR] C.2 Send message — Send action sau add friend (gián tiếp)** — TC-07/11/17/21/27/31/37/41 expected có "send action thành công cho user" + "send msg, action ở `setting-add-friend` (hoặc -old/-unblock)" — đây là feature C.2 ở checklist LME. **Cover gián tiếp** nhưng không TC dedicated verify (a) action có replace friend info đúng không, (b) profile sender đúng không, (c) `last_message`/`last_time_message` update. **Fix**: Bổ sung `TC-NEW-10` (verify send action C.2 specific) HOẶC tách expected của TC-07 thành 2 TC.

- **[MAJOR] Precondition mơ hồ — không nêu LINE version + device hardware** — Toàn bộ TC chỉ ghi "device Android" hoặc "device iOS" — không nêu LINE app version, OS version (Android 12 vs 14 — Android 14 mới có edge-to-edge default), device model. **Fix**: Mỗi TC liên quan device phải có Precondition block đầy đủ.

- **[MAJOR] Format sheet không 10 cột chuẩn** — Sheet dùng nested checklist (Main / Sub1-4 / Expected) — không match template 10 cột (TC ID / Title / Type / Priority / Precondition / Steps / Expected / Output note / Assignee / Status). Tôi đã convert best-effort nhưng nhiều cell rỗng. **Fix**: Sau khi member fix các blocker, convert sheet sang format 10 cột standalone trước khi `/sync-tc` push master.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC ID rỗng** — Sheet không có cột TC ID, tôi tạm gán TC-01..49. Member fill TC ID chuẩn team (e.g. `TC-36243-01`) trước khi sync.

- **[MINOR] Assignee + Status rỗng toàn bộ** — Cột Assignee và Status pre-fill rỗng. Status có "Done step" ở vài row trong cột K (cột feature khác). Mơ hồ. **Fix**: Member fill Assignee tester thực tế + Status để rỗng trước test.

- **[MINOR] Title TC chứa keyword chung "quét QR landing"** — Phần lớn TC dùng cùng cụm — khó scan để map impact. **Fix**: Mỗi TC variant thêm sub-keyword phân biệt (vd "[Android-LINE26.6][Friend-new] Quét QR landing ở màn list").

- **[MINOR] Note column thiếu context** — Cột Output note chỉ có "Done step" ở vài TC, không note environment / device cụ thể đã test. **Fix**: Khi tester run, ghi rõ "Tested on Pixel 8a / LINE Android 26.6.1 / 2026-05-15".

- **[MINOR] DB verify `detail_landing_click` chưa nêu field check cụ thể** — Expected của TC-07/11/etc nói "check db: `detail_landing_click`" — nhưng không nêu field nào (record có `bot_id`/`line_user_id`/`landing_id`/`scanned_at`?) → tester không biết verify cái gì. **Fix**: Ghi rõ field + giá trị expected.

### 4.4 Nit (gợi ý)

- **[NIT]** Expected có thể tách block: (a) UI behavior Android, (b) UI behavior iOS, (c) DB state (`detail_landing_click` fields), (d) Send queue (action_id, profile_sender), (e) LINE user receive — giúp tester check từng layer.

- **[NIT]** Thêm matrix LINE Android version: baseline 15.13.1/15.15.1 (không bị) + 26.3.0..26.5.x (đoán bị do edge-to-edge) + 26.6.0 + 26.6.1 (confirm bị) + 26.7.0+ (sau fix LINE-side).

- **[NIT]** Có thể tham khảo approach của L Step (đối thủ đã fix — journal #117858) — hỏi PM xem có info technical không.

- **[NIT]** Thêm screenshot/video evidence trong Expected cho UI behavior — đặc biệt với edge case "button bị che" vs "button còn nguyên".

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Sau khi dev clarify logic fix, refine thêm.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | Reproduce bug **trước fix** trên LINE Android 26.6.0/26.6.1 | (1) Device Android (Pixel/Galaxy/Xperia) — OS Android 13+.<br>(2) LINE Android app **version 26.6.0** hoặc **26.6.1** (cài bản APK cũ nếu LINE đã auto-update).<br>(3) Bot LME có 1 QR landing active. URL repro: `https://go.lmes.jp/landing-qr/2002341759-JRn2awBD?uLand=7nUI4Q` (staging).<br>(4) Build LME **trước khi merge fix**. | 1) Mở URL QR landing bằng LINE app trên device Android<br>2) Quan sát màn LIFF mở<br>3) Tap button `友だち追加` (Add Friend) ở bottom<br>4) Quan sát phản hồi UI và bottom navigation bar | (a) Button `友だち追加` **KHÔNG phản hồi khi tap** (reproduce bug)<br>(b) Vị trí button bị **chồng / che bởi vùng navigation bar Android**<br>(c) DB `detail_landing_click` KHÔNG có record mới<br>(d) Bot KHÔNG add được friend mới | High | Regression (verify bug exists) | BUG, T1, T2 |
| **TC-NEW-02** | Verify fix LME **work** trên LINE Android 26.6.0/26.6.1 | Setup TC-NEW-01 nhưng dùng **build LME đã merge fix**. | 1) Mở URL QR landing bằng LINE app trên device Android (LINE 26.6.0/26.6.1)<br>2) Quan sát màn LIFF<br>3) Tap button `友だち追加`<br>4) Verify friend được add + DB record tạo + action send | (a) Button `友だち追加` **react ngay khi tap**<br>(b) Friend được add vào bot LINE OA<br>(c) DB `detail_landing_click` có record mới (`bot_id`, `line_user_id`, `landing_id`, `scanned_at`)<br>(d) Send action sau add friend thành công | High | Positive | BUG, F1, T1, T2 |
| **TC-NEW-03** | iOS baseline regression — fix không break LINE iOS | (1) Device iOS (iPhone 13+).<br>(2) LINE iOS app **version 15.13.1** hoặc **15.15.1** (version KH report không bị bug).<br>(3) Build LME đã merge fix. | 1) Mở URL QR landing bằng LINE app trên iOS<br>2) Tap button `友だち追加`<br>3) Verify friend add + action | (a) Hoạt động bình thường — button react, friend add success<br>(b) Behavior **không khác** so với version trước fix<br>(c) DB + action giống TC-NEW-02 | High | Regression | F1, T1 |
| **TC-NEW-04** | QRCA specific — Add friend qua **QR Code Action** | (1) Bot có **QR Code Action** (QRCA — không phải QR landing thường). 3 QRCA active (theo journal #117733 — KH `小川直美`).<br>(2) Device Android LINE 26.6.0/26.6.1. | 1) User scan QR Code Action (QRCA) bằng LINE app Android<br>2) Tap button `友だち追加`<br>3) Verify add friend + action QRCA trigger | (a) Button react ngay khi tap (sau fix)<br>(b) Friend add success<br>(c) Action của QRCA được trigger (send msg/action theo setting QRCA)<br>(d) DB ghi nhận đúng `qrca_id` (không phải `landing_id`) | High | Positive | T2, BUG |
| **TC-NEW-05** | Logic check LIFF login khi mở Android (verify fix code) | _<Pending dev clarify trong 03>_ — sau khi dev confirm logic, viết steps cụ thể:<br>VD: (1) Friend đã accept LIFF app trước đó, session expired.<br>(2) Mở LIFF từ Android. | 1) Mở LIFF callback URL bằng Android (LINE 26.6.x)<br>2) Quan sát check LIFF login state<br>3) Verify behavior khi check pass / fail | (a) Khi LIFF login valid → chuyển flow add friend bình thường<br>(b) Khi LIFF login invalid → trigger re-login (hoặc workaround theo logic dev confirm)<br>(c) Không có dòng `error_log` về LIFF state | High | Positive + Negative | F1 |
| **TC-NEW-06** | LINE OA profile page button (verify scope LME-side) | (1) Bot LINE OA có button add friend trên profile page (nếu tool LME có generate).<br>(2) Device Android LINE 26.6.0/26.6.1. | 1) Mở LINE OA profile page bằng LINE Android<br>2) Tap button `友だち追加` trên profile | (a) Nếu fix LME cover → button react<br>(b) Nếu LINE-side only (không scope LME) → flag dev confirm, không count fail | Medium | Boundary (scope check) | T3 |
| **TC-NEW-07** | Boundary — LINE Android version edge (26.5.x / 26.7.x) | (1) Device Android, LINE app **version 26.5.x** (trước range bug) hoặc **version 26.7.0+** (sau fix LINE-side, nếu có).<br>(2) Build LME đã merge fix. | 1) Mở URL QR landing<br>2) Tap button kết bạn<br>3) Verify behavior | (a) 26.5.x → button react bình thường (không reproduce bug — workaround fix LME không break)<br>(b) 26.7.0+ → button react (LINE đã fix edge-to-edge issue) | Medium | Boundary | F1, T1 |
| **TC-NEW-08** | Compatibility — Device matrix Android | (1) 3 device hardware: **Pixel 8a** (Google reference) + **Galaxy S24** (Samsung) + **Xperia 1 V** (Sony).<br>(2) Mỗi device cài LINE Android 26.6.0/26.6.1.<br>(3) Build LME đã merge fix. | 1) Lần lượt mỗi device: mở URL QR landing → tap btn kết bạn → verify add friend OK<br>2) So sánh behavior 3 device | (a) Tất cả 3 device đều: button react, friend add success<br>(b) Không device nào có UI artifact (button bị che) | Medium | Compatibility | T1, A.2 Compatibility |
| **TC-NEW-09** | CL18 — Load UI trước, deploy fix sau, submit | (1) Mở sẵn URL QR landing trên device Android (LINE 26.6.x) — **trước khi deploy fix**.<br>(2) Giữ tab mở, không reload.<br>(3) Deploy fix LME.<br>(4) User vẫn ở tab cũ. | 1) User tap button `友だち追加` (vẫn tab cũ, chưa reload)<br>2) Quan sát phản hồi | (a) Hoặc fix **work ngay không cần reload** (LIFF callback chạy backend mới)<br>(b) Hoặc **prompt user reload** (msg JP rõ ràng) — không silent fail | Medium | Boundary (CL18) | F1, T1, CL18 |
| **TC-NEW-10** | C.2 Send action sau add friend qua QR landing | (1) QR landing có setup action send msg sau add friend.<br>(2) Friend mới (chưa từng add bot). | 1) Friend quét QR landing → add friend success<br>2) Quan sát action send msg<br>3) Verify nội dung msg (replace friend info), profile sender, last_message update | (a) Msg action send đúng nội dung<br>(b) Friend info replace đúng (nếu có insert code)<br>(c) Profile sender đúng (bot, không lẫn account khác)<br>(d) `last_message` + `last_time_message` cập nhật<br>(e) Friend bị block bot trước đó → KHÔNG send | Medium | Functional | T1, C.2 Send message |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — QR Landing / LIFF callback flow
  - **Nội dung cần update**:
    1. Document **LINE Android version compatibility matrix**: version nào bị edge-to-edge issue, version nào không, fix LME apply cho range nào.
    2. Document **logic check LIFF login khi mở Android**: trigger condition, behavior khi state invalid, fallback flow.
    3. Reference **LINE Developers official news**: https://developers.line.biz/ja/news/2026/05/11/liff-outage/
  - **Người chịu trách nhiệm update**: Dev assignee (Ngần) + PM.
  - **Câu hỏi cần dev clarify** (impact direct lên TCs round 2):
    1. Logic "check liff login khi mở trên Android" cụ thể là gì? (Detect Android UA? Check session token? Trigger nào?)
    2. Behavior khi LIFF login check fail → re-login UI hay padding UI?
    3. Fix có cover **QRCA** flow không hay chỉ QR landing? (KH report 1 case qua QRCA)
    4. Có scope LINE OA profile page button không? (Hay chỉ là LINE-side bug, đợi LINE fix?)
    5. iOS có affect không (theo LINE thì không, nhưng cần regression test)?
    6. Android OS version nào ảnh hưởng (Android 13+? 14+ default edge-to-edge?)
    7. L Step (đối thủ) fix bằng cách gì → có info technical tham khảo?

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — FAIL: GAP-1 (LINE version), GAP-2 (QRCA), GAP-3 (logic LIFF login), GAP-4 (OA profile), RISK BUG/F1/T1
- [x] **B. Chất lượng từng TC** — FAIL: 35+ TC Expected inherit rỗng, Precondition thiếu LINE version, Title generic
- [x] **C. Chất lượng bộ TC** — FAIL: Ratio 41/5/0/3 (Positive/Negative/Boundary/Regression) — mất cân đối nặng
- [x] **D. Spec alignment** — Flag spec update (§6)
- [x] **E. Hành chính** — FAIL: TC ID rỗng, Assignee rỗng, Tester verify auto-fill chưa tick, format sheet không 10 cột
- [x] **F. Base checklist LME**:
  - [ ] **F.1 Checklist web** — chưa cover: A.2 Compatibility (device matrix Android), CL13 (Line Friend redirect kết bạn — partial cover), CL18 (load UI trước, submit sau deploy)
  - [ ] **F.2 Checklist job** — B.1 Job callback liên quan (LIFF callback) nhưng chưa explicit cover
  - [ ] **F.3 Các tính năng chung** — C.2 Send message gián tiếp qua expected TC-07/11/etc, chưa TC dedicated

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | 2026-05-13 |
| Tester | (đã đọc & hiểu feedback) | |
