# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38552` — [Form] Form 六甲お子様アンケートフォーム (ペット有) có 13 件 câu trả lời nhưng spreadsheet chỉ hiển thị 4 件 |
| Reviewer (Leader) | `<Leader ký tên>` |
| Tester được review | `<chưa điền trong 04-tc-list.md>` |
| Ngày review | `2026-07-11` |
| Version TCs | `v1` (fetch từ Sheet "Sync google", rows 439–465, 27 TCs) |
| Vòng review | `Round 1` |

> **Spec reference**: không có `02-spec-reference.md` → dùng [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) tổng, không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần bổ sung TC và review lại

**Lý do ngắn gọn**: Bộ 27 TC cover rất tốt **chiều "không lệch cột"** (form 1-page/multi-page × header cũ/mới, retry, duplicate), nhưng **không có TC nào verify đúng triệu chứng KH báo — thiếu dòng dữ liệu** (13 件 → 4 件), và **không có TC nào chạy trên sheet ở đúng trạng thái lỗi của KH** (cột A trống giữa vùng data) — vốn chính là precondition mà Dev nêu ở mục 1 "Nguyên nhân". Hai gap này để lọt rủi ro **mất dữ liệu production** sau khi deploy fix.

---

## 2. Tóm tắt cho member

Bộ TC làm **rất chắc phần ma trận biến thể**: 4 tổ hợp form 1-page/multi-page × header cũ/mới (TC10–TC13) đúng như Dev yêu cầu, nhóm retry (TC18–TC21) và nhóm nhận diện header/Result ID (TC14–TC17) đều đủ — đây là phần thường bị bỏ sót và em đã cover.

Điểm cần bổ sung nằm ở **chỗ khác với hướng em đang test**: cả 27 TC đều verify "dòng mới **không lệch cột**", nhưng KH thực tế báo là **spreadsheet thiếu dòng** (13 bản ghi trả lời chỉ thấy 4). Không TC nào đối chiếu **số dòng trên sheet = số form result trong admin**, và không TC nào có precondition là **sheet đang ở trạng thái lỗi** (cột A trống ở giữa data — chính điều kiện Dev mô tả trong mục 1). Vì fix neo append vào `A1`, chạy trên sheet đang lệch có khả năng **ghi đè lên dòng cũ** → cần verify trước khi release, kể cả khi team đã chốt "lỗi KH".

Ngoài ra: TC09 có expected mâu thuẫn với chính note của nó (xem §4.2), TC22 (concurrent) đang `Not test`, TC27 chưa viết xong.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — append lệch cột khi sheet có ô cột A trống (`rangeDefine = null`) | Fix | — | TC02, TC06, TC07 | 3 | **RISK** — TC06/TC07 để trống ô ở **câu hỏi mới thêm** (cột giữa/cuối), KHÔNG có TC nào có **cột A trống** — đúng precondition mục 1 |
| **BUG-symptom** — spreadsheet thiếu bản ghi (13 件 → 4 件) | Fix | — | — | **0** | **GAP** — không TC nào đối chiếu số dòng sheet ↔ số form result |
| **F1** — `HandleFormAnswerSyncGoogleSheetTask.handle()` nhánh append sheet **không rỗng** (`appendRowData` dòng 429, `rangeDefine="A1"`) | Function | Direct | TC02, TC03, TC04, TC05, TC06, TC07, TC08, TC09, TC10–TC13, TC19, TC23, TC24, TC25 | 16 | **RISK** — nhiều TC nhưng precondition đều là sheet **sạch/hợp lệ**; thiếu chiều "sheet ở trạng thái lỗi" và thiếu negative "ghi đè data cũ" |
| **F1-đối chiếu** — nhánh sheet **rỗng** (dòng 389, `rangeDefine="A1"` từ trước, không sửa) | Function | Indirect (regression) | TC01, TC14, TC15, TC20 | 4 | **OK** |
| **D — data impact** | Data | — | — | — | **N/A** — Dev ghi rõ 4.2 trống (không đụng SQL/config/schema/constant) |
| **T1** — Đồng bộ câu trả lời form lên Google Sheet (case insert vào sheet đã có dữ liệu) | Feature | `<Dev không ghi mức risk>` | TC01–TC25 | 25 | **RISK** — happy-path-heavy (AP-3), thiếu edge state; CLJ01 (rate limit) chưa cover |

### Chiều bị thiếu (chi tiết)

| Chiều | Có TC? | Ghi chú |
|---|---|---|
| Positive (append từ cột A) | ✅ | TC01–TC13, TC23–TC25 |
| Regression (sheet rỗng / nhận diện header) | ✅ | TC14–TC17 |
| Retry / job sync | ✅ | TC18–TC21 |
| Boundary — **sheet đang ở trạng thái lỗi (cột A trống)** | ❌ | **GAP** |
| Negative — **ghi đè / mất dòng dữ liệu cũ** | ❌ | **GAP** |
| Count matching — **số dòng sheet = số form result** | ❌ | **GAP** |
| Concurrency | ⚠️ | TC22 tồn tại nhưng `Not test` |
| CLJ01 — rate limit + request lớn liên tục | ❌ | **GAP** (TC23 test data lớn, không test tần suất) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC26 | Check sync **xóa** form-result không bị ảnh hưởng | Fix không chạm flow delete (chỉ đổi 1 tham số ở nhánh append) | **Giữ** — hợp lệ như regression smoke của T1. Nhưng phải bổ sung Precondition + Steps (đang trống). |
| TC27 | Check sync form cũ (`using_old_version = 1`) | Không map được — TC **chưa viết xong** (trống Precondition/Steps/Expected/Status) | **Fix**: viết đủ nội dung, hoặc remove nếu không thuộc scope #38552 |

> Không có TC nào lạc chủ đề nghiêm trọng. Nhóm TC14–TC17 (Result ID ở A1/B1/C1) không nằm trong code Dev sửa nhưng là **regression hợp lệ** cho logic nhận diện sheet → giữ.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **Khác — API parameter / write-anchor change**. Không phải generic catch, không phải validation, không phải race-condition. Bản chất: đổi `rangeDefine` từ `null` → `"A1"` để thay đổi **cách Google Sheets API `values.append` tự dò "table"** và quyết định ô bắt đầu ghi. |
| **Trigger space cần cover** | Fix này không có "error trigger". Trigger space thực sự = **các trạng thái sheet mà Google phải dò table trên đó**: (1) sheet sạch, mọi dòng đầy cột A; (2) sheet có ô **giữa vùng data** ở cột **không phải A** trống; (3) sheet có ô **cột A** trống ở dòng cuối; (4) sheet có ô **cột A** trống **ở giữa** vùng data (= trạng thái sheet KH); (5) sheet có **dòng trống hoàn toàn** xen giữa data; (6) sheet đã bị **lệch cột từ trước** (data nằm từ cột B/C trở đi). |
| **Số trigger TCs hiện cover** | **2/6** — chỉ (1) và (2). Các trạng thái (3)(4)(5)(6) — tức đúng trạng thái sheet gây bug ở production — **không TC nào có precondition đó**. |
| **KH report dạng** | **Symptom-only** — KH chỉ nói "13 件 回答 nhưng spreadsheet chỉ 4 件", không có error code / log / message. |
| **Alternative root causes cần verify** | (a) Append ghi **đè** lên dòng cũ → mất bản ghi (đây là cách duy nhất giải thích được "thiếu 9 件" — lệch cột thuần túy KHÔNG làm mất dòng, chỉ làm xấu hiển thị). (b) Sync **fail + retry fail** → bản ghi không bao giờ lên sheet. (c) Form nhiều page → data ở **tab khác**, KH chỉ nhìn 1 tab (tham chiếu bug #34991 cùng sheet). (d) Chèn/xóa câu hỏi giữa form → data mới không map header (xem note TC09). |
| **Anti-patterns dính** | **AP-2** (symptom-only KH report) — dính. **AP-3** (happy-path-only regression) — dính. AP-1/AP-4/AP-6 — không dính (fix không phải generic-catch; có commit hash; mục 3 có nội dung). AP-5 — borderline ở TC26, đã note. |

### ⚠️ Điểm mấu chốt của review này

**Triệu chứng KH ≠ triệu chứng TCs đang verify.**

- Bản JP: 「回答が **13件** あるにも関わらずスプレッドシートには **4件** しか表示されていません」 — `件` là đơn vị đếm **bản ghi trả lời**, không phải câu hỏi. Nghĩa đúng: form có **13 bản ghi trả lời**, spreadsheet chỉ có **4 dòng** → **thiếu 9 dòng**.
- Bản dịch VN trong Redmine ("13 câu trả lời … chỉ hiển thị 4 câu") gây hiểu nhầm sang "thiếu cột".
- Toàn bộ 27 TC verify **"dòng mới không lệch cột"**. **Không TC nào verify "không thiếu dòng"**.
- Lệch cột **một mình không làm mất dòng**. Muốn 13 → 4 thì phải có **ghi đè** (append tính sai vị trí và đè lên dòng đã có) hoặc **sync thất bại**. Fix `rangeDefine = "A1"` neo append vào cột A — khi Google dò table từ A1 mà cột A có ô trống ở giữa, table có thể bị coi là kết thúc sớm → **dòng mới ghi đè lên dòng phía dưới**. Đây chính là rủi ro Dev/PM đã lường trước trong journal 2026-07-09 ("nếu có trường hợp lệch cột do KH sửa dẫn đến cột A ko có dữ liệu **có thể bị ghi đè lên** thì lỗi KH").

→ Dù team đã chốt **"ghi đè trong trường hợp đó = lỗi KH"** (chấp nhận về mặt nghiệp vụ), QA vẫn **bắt buộc phải có TC verify hành vi này** để: (1) biết chính xác fix có làm mất data hay không khi chạy trên sheet đang lỗi của KH; (2) có căn cứ trả lời KH; (3) quyết định có cần thông báo KH sửa sheet trước khi deploy không. Đây là lý do verdict REJECTED, không phải vì bộ TC kém.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-01 — Không TC nào chạy trên sheet ở đúng trạng thái lỗi (cột A trống giữa vùng data).**
  Mục 1 `03-dev-impact.md` nêu rõ điều kiện gây bug: *"trên sheet bị lệch cột (**cột A không có dữ liệu** do KH sửa) thì dòng mới ghi lệch sang phải"*. Nhưng steps tái hiện của Dev (và TC06/TC07 bám theo) lại để trống ô ở **câu hỏi mới thêm** — tức cột giữa/cuối, KHÔNG phải cột A. Cột A (Result ID / LINE ユーザーID) luôn có giá trị trong các TC hiện tại. → Bộ TC **chưa từng đặt hệ thống vào đúng điều kiện root cause**.
  **Fix**: bổ sung **TC-NEW-01, TC-NEW-02** (§5).

- **[BLOCKER] SYMPTOM-ONLY / GAP-02 — Không TC nào verify "không thiếu dòng" (count matching).**
  Triệu chứng KH là **13 件 → 4 件** (thiếu 9 bản ghi), nhưng 27/27 TC chỉ verify vị trí cột. Không TC nào đối chiếu **số dòng data trên spreadsheet = số form result ở màn admin**. Nếu fix vẫn để lọt case ghi đè → deploy xong KH vẫn mất data và bug tái phát với đúng triệu chứng cũ.
  **Fix**: bổ sung **TC-NEW-03** (§5). Đồng thời thêm bước "đếm và đối chiếu số dòng" vào Expected của TC02, TC03, TC04, TC06, TC07.
  _(Đây cũng chính là mục **TC-23** của checklist LME §A.1+: "test đối chiếu hiển thị màn hình ↔ output (CSV/spreadsheet/preview) phải khớp".)_

- **[BLOCKER] GAP-03 — Không TC nào verify hành vi ghi đè / mất dữ liệu khi append `A1` trên sheet đã bị lệch từ trước.**
  Đây là **trạng thái sheet thật của KH ngay lúc deploy** (WSSサポーター mới "khôi phục tạm" ngày 2026-07-08). Rủi ro mất dữ liệu production. Team đã chốt "lỗi KH" về mặt trách nhiệm, nhưng **hành vi phải được đo trước khi release**.
  **Fix**: bổ sung **TC-NEW-04** (§5). Kết quả TC này quyết định có cần gửi hướng dẫn KH sửa sheet trước deploy hay không.

### 4.2 Major (nên fix)

- **[MAJOR] TC09 — Expected mâu thuẫn với chính Output note, và mâu thuẫn có thể là root cause thật của bug KH.**
  Expected ghi *"Dữ liệu map đúng với header"*, nhưng note ghi ngược lại: *"Data sync mới sẽ fill lần lượt các cột theo thứ tự trong form result **chứ không map theo header** → khi nào sync lại toàn bộ sheet thì mới map lại theo header"*. Status vẫn `OK`.
  → Nếu behavior thực tế là "fill theo thứ tự, không map header", thì **KH chèn/sửa câu hỏi giữa form là đủ để data lệch so với header** — độc lập với fix `rangeDefine`. Đây là **alternative root cause (d)** ở §3.5.
  **Fix**: (1) viết lại Expected TC09 đúng behavior đã confirm; (2) **hỏi Dev**: fix `rangeDefine="A1"` có xử lý được case này không, hay cần fix riêng? (3) nếu là behavior by-design → ghi vào §6 Spec update.

- **[MAJOR] AP-2 — KH report symptom-only, TCs chỉ cover 1 root cause.**
  Cần confirm với Dev về 4 alternative root cause ở §3.5 (ghi đè / sync fail / data ở tab khác của form multi-page / không map header). Tối thiểu cover **≥ 2** trong bộ TC. TC-NEW-03 + TC-NEW-05 (§5) giải quyết (a) và (b).

- **[MAJOR] Caller scope chưa được confirm — Salon / Lesson / QR code có dùng chung pattern append không?**
  Mục 3 `03-dev-impact.md` viết: *"appendRowData có **2 chỗ gọi** trong `HandleFormAnswerSyncGoogleSheetTask.handle()`"* — câu này mơ hồ: 2 call site **trong file đó**, hay 2 call site **trong toàn bộ codebase**? Checklist LME §C.5 nêu **4 tính năng** liên kết Google spread: **Form / Salon / Lesson / QR code**. Nếu Salon/Lesson/QR cũng append qua helper cùng pattern (`rangeDefine = null`) → **cùng dính bug, cùng cần fix**.
  **Fix**: hỏi Dev câu hỏi trên **trước khi merge**. Nếu dùng chung → mở rộng scope fix + thêm regression TC cho Salon/Lesson/QR sync. Nếu không dùng chung → ghi rõ vào mục 3 để đóng nghi vấn.
  _(Không tự đề xuất TC test Salon/Lesson ở §5 vì chưa xác nhận code có bị chạm — tránh over-coverage AP-5.)_

- **[MAJOR] TC22 (concurrent submit) đang `Not test`.**
  Fix neo mọi request append vào cùng anchor `A1`. Hai job append đồng thời trên cùng sheet là kịch bản **trực tiếp liên quan đến vị trí ghi** — không thể để `Not test`. Checklist LME **CL-Func-25** (multi-thread không khóa) + **TC-12** (kịch bản hệ bất thường) đều yêu cầu.
  **Fix**: chạy TC22, thêm Expected đo lường được (mỗi user đúng 1 dòng, **tổng số dòng = tổng số submit**, không đè nhau).

- **[MAJOR] TC27 chưa hoàn chỉnh** — "Check sync form cũ (`using_old_version = 1`)" trống Precondition / Steps / Expected / Status.
  **Fix**: viết đủ, hoặc remove khỏi scope #38552 nếu không liên quan.

- **[MAJOR] F.2 / CLJ01 chưa cover — rate limit + retry với request lớn và liên tục.**
  Task chạm **job sync Java Google Sheet** → CLJ01 bắt buộc: *"tạo TCs với dữ liệu request lớn và liên tục để kiểm tra việc retry của job"*. TC23 test **sheet nhiều dòng** (data lớn) nhưng không test **tần suất request lớn**. TC18–TC21 test retry nhưng bằng cách **giả lập lỗi**, không phải bằng rate limit thật. Checklist §A.1+ **TC-10** cũng yêu cầu verify retry + backoff **KHÔNG MẤT DỮ LIỆU** khi vượt rate limit.
  **Fix**: bổ sung **TC-NEW-05** (§5).

- **[MAJOR] Expected của phần lớn TC không đo lường được** (vi phạm review-checklist §B.1).
  Ví dụ: TC08 *"Không phát sinh lệch cột"*, TC12 *"Dữ liệu đúng vị trí"*, TC05 *"Dữ liệu hiển thị đúng theo từng cột"*. Với bug về **vị trí ghi**, Expected phải chỉ đích danh ô: *"dòng mới bắt đầu tại **cột A**; A{n} = Result ID; câu trả lời Q3 nằm đúng cột header Q3; **tổng số dòng data = N**"*.
  **Fix**: rewrite Expected của TC02–TC13 theo mẫu trên.

- **[MAJOR] File 01 auto-filled từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick.**
  Review chỉ có giá trị khi tester đã đọc lại detail Redmine và xác nhận. **Đặc biệt quan trọng ở task này** vì bản dịch VN của description ("13 câu trả lời") **sai lệch nghĩa** so với bản JP gốc (「13件」= 13 bản ghi) — xem §3.5.
  **Fix**: tester đọc lại Redmine #38552 (cả 原文 JP), tick checkbox.

- **[MAJOR] File 03 auto-filled từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick.**
  F/D/T có thể chưa đầy đủ hoặc mapping sai. Cụ thể mục 4.3 Dev **không ghi mức risk regression** cho T1.
  **Fix**: tester đọc lại journal đánh giá ảnh hưởng, tick checkbox, hỏi Dev bổ sung risk level.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Toàn bộ TC trống cột `Type` và `Priority`** (sheet gốc không có 2 cột này). Leader không đánh giá được tỷ lệ Positive/Negative/Boundary/Regression (review-checklist §C). → Đề nghị bổ sung khi đưa vào file 04.
- **[MINOR] TC26 trống Precondition + Steps**, chỉ có Expected. Không chạy lại được bởi người khác.
- **[MINOR] `04-tc-list.md` trống "Tester viết TCs" và "Ngày submit"** (review-checklist §E — hành chính).
- **[MINOR] TC05 và TC08 trùng lặp một phần** — cả hai đều là "submit đầy đủ dữ liệu → không lệch cột". Đề nghị gộp hoặc phân hóa rõ (TC05 = đa dạng **loại câu hỏi**; TC08 = đa dạng **số lần submit**).
- **[MINOR] Steps của TC02/TC03/TC04/TC08 quá ngắn** ("Submit thêm một câu trả lời mới.") — không nói rõ sheet đang ở trạng thái nào, submit bao nhiêu lần. Người khác chạy lại sẽ ra kết quả khác.

### 4.4 Nit (gợi ý)

- **[NIT] Checklist LME §C.5** còn 2 mục chưa cover, cân nhắc thêm nếu có thời gian: **tiêu đề cột spread có xuống dòng**; **tên file/sheet chứa ký tự đặc biệt**. TC24 đã cover Unicode/emoji trong **giá trị cell** — nhưng chưa cover **newline trong cell** (có thể ảnh hưởng cách Google dò table).
- **[NIT] CL-Func-18** — case "load UI trước, submit sau khi release": để sẵn màn form phía LINE user trước deploy → submit sau deploy → verify vẫn ghi google spread đúng từ cột A.
- **[NIT] Không có PR link**, chỉ có commit hash `14ce35a`. Có hash là đủ trace, nhưng PR link giúp Leader verify fix shape nhanh hơn (AP-4).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Tất cả đều thao tác từ góc nhìn **manual tester** (quan sát trên spreadsheet + màn admin), không cần query DB.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | Sync khi sheet có ô **cột A trống ở dòng cuối** — verify dòng mới vẫn ghi từ cột A | Form đã liên kết Google Sheet, sheet có ≥ 3 dòng data. Mở sheet, **xóa thủ công giá trị ô cột A của dòng data cuối cùng** (giữ nguyên các cột còn lại) | 1. Mở sheet, xóa giá trị ô A của dòng data cuối.<br>2. LINE user submit 1 câu trả lời mới.<br>3. Chờ job sync xong, mở lại sheet. | Dòng mới được ghi vào **dòng ngay dưới dòng cuối cùng đang có data**, bắt đầu tại **cột A** (A chứa Result ID). **Không đè** lên dòng có ô A trống. Dòng có ô A trống vẫn giữ nguyên các giá trị cột B trở đi. Tổng số dòng data tăng đúng **+1**. | High | Boundary | **BUG**, F1, T1 |
| **TC-NEW-02** | Sync khi sheet có ô **cột A trống ở GIỮA vùng data** — verify không ghi đè dòng phía dưới | Sheet có ≥ 5 dòng data. Xóa thủ công giá trị ô cột A của **dòng data thứ 3** (giữa vùng data). Ghi lại (screenshot) toàn bộ nội dung sheet trước khi submit | 1. Chuẩn bị sheet như precondition, chụp màn hình sheet.<br>2. LINE user submit 1 câu trả lời mới.<br>3. Chờ job sync xong, mở lại sheet, so sánh với screenshot. | Dòng mới ghi vào **cuối vùng data**, bắt đầu từ cột A. **Toàn bộ 5 dòng cũ giữ nguyên**, không dòng nào bị ghi đè/mất. Tổng số dòng +1.<br>⚠️ **Nếu dòng mới ghi đè lên dòng 4/5** → đây là hành vi mà PM đã chốt "chấp nhận, lỗi KH" (journal 2026-07-09) → **KHÔNG raise bug, nhưng phải ghi rõ kết quả quan sát vào Output note** để Leader quyết định có cần thông báo KH sửa sheet trước deploy không. | High | Boundary / Negative | **BUG**, F1, T1 |
| **TC-NEW-03** | Đối chiếu **số bản ghi**: số dòng trên spreadsheet = số form result ở màn admin (verify đúng triệu chứng KH 13 件 → 4 件) | Form mới, đã liên kết Google Sheet | 1. Cho LINE user submit **13 lần** (dùng nhiều LINE user hoặc 1 user submit nhiều lần theo setting form), xen kẽ: 2 lần submit → edit form thêm câu hỏi → 3 lần submit (có bỏ trống câu mới) → edit form lần nữa → submit tiếp cho đủ 13.<br>2. Vào màn admin **Quản lý form → form result**, đếm số bản ghi.<br>3. Mở spreadsheet, đếm số dòng data (không tính header). | Số dòng data trên spreadsheet = **13** = số bản ghi ở màn admin. **Không thiếu dòng nào**. Mỗi dòng có Result ID ở cột A, khớp 1-1 với Result ID trên màn admin. | High | Positive / Regression | **BUG-symptom**, F1, T1 |
| **TC-NEW-04** | Sync trên sheet **đã bị lệch cột từ trước** (mô phỏng sheet KH tại thời điểm deploy) | Sheet có ≥ 5 dòng data trong đó **≥ 2 dòng bị lệch sang phải** (data bắt đầu từ cột B/C, cột A trống) — mô phỏng đúng sheet KH trước khi được khôi phục. Chụp màn hình sheet trước khi test | 1. Chuẩn bị sheet lệch như precondition, chụp màn hình.<br>2. LINE user submit 1 câu trả lời mới.<br>3. Chờ job sync xong, mở sheet, so sánh với screenshot.<br>4. Submit thêm 2 lần nữa, kiểm tra lại. | Ghi nhận chính xác (bằng screenshot trước/sau): dòng mới ghi ở **vị trí nào**, có **đè lên dòng lệch nào** không, tổng số dòng data trước/sau. Dòng mới phải bắt đầu từ **cột A**.<br>⚠️ TC này **không có expected pass/fail cứng** — mục tiêu là **đo hành vi trên sheet trạng thái lỗi thật** để Leader/PM quyết định: có cần yêu cầu KH sửa sheet (điền lại cột A) **trước khi deploy** hay không. Kết quả bắt buộc ghi vào Output note. | High | Negative / Boundary | **BUG**, F1, T1 |
| **TC-NEW-05** | Job sync — request lớn và **liên tục** (rate limit + retry, không mất dữ liệu) — CLJ01 | Form đã liên kết Google Sheet, sheet đã có data | 1. Cho **nhiều LINE user submit liên tục trong thời gian ngắn** (vd 30–50 submit trong vài phút, đủ để chạm rate limit Google Sheets API).<br>2. Theo dõi job sync (log/màn quản lý job) xem có request nào bị lỗi rate limit và được **retry** không.<br>3. Sau khi job chạy hết, mở spreadsheet đếm số dòng. | Mọi submit đều lên sheet: **số dòng data = tổng số submit**, **không mất dòng**, **không duplicate**. Request bị rate limit được **retry thành công** (có backoff). Mọi dòng (kể cả dòng ghi bởi retry) đều bắt đầu từ **cột A**, không lệch. | High | Boundary | F1, T1, **CLJ01** |
| **TC-NEW-06** | Chèn câu hỏi vào **giữa** form → verify data mới map đúng/sai so với header (làm rõ mâu thuẫn TC09) | Form đã có ≥ 3 câu hỏi và ≥ 2 bản ghi trên sheet | 1. Edit form, **chèn 1 câu hỏi mới vào giữa** (vd giữa Q1 và Q2).<br>2. LINE user submit 1 câu trả lời mới (điền đủ).<br>3. Mở sheet, đối chiếu **từng ô** của dòng mới với **tiêu đề cột (header)**. | Ghi rõ hành vi quan sát được: câu trả lời có nằm **đúng cột theo header** không, hay **fill tuần tự theo thứ tự trong form result** (như Output note TC09 mô tả).<br>→ Kết quả dùng để **confirm với Dev** đây là by-design hay là bug thứ 2 (xem §4.2 và §6). | High | Boundary | **BUG (alt root cause)**, F1, T1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ spec / behavior** — chi tiết:
  - **Section**: Form answer → đồng bộ Google Sheet (mapping câu trả lời ↔ cột header).
  - **Nội dung cần làm rõ**: Output note của **TC09** khẳng định *"Data sync mới sẽ fill lần lượt các cột theo thứ tự trong form result **chứ không map theo header**; khi nào sync lại toàn bộ sheet thì mới map lại theo header"* — trong khi Expected của chính TC09 lại ghi *"Dữ liệu map đúng với header"*. Hai câu này **loại trừ nhau**.
    → Nếu behavior thật là "fill tuần tự, không map header" thì **mọi lần KH chèn/xóa/sắp xếp lại câu hỏi giữa form đều làm data lệch so với header** — và đây là một **nguồn gây triệu chứng "hiển thị sai/thiếu" độc lập với fix `rangeDefine`**. Cần Dev + BA xác nhận đây là by-design hay là bug thứ 2 chưa được ghi nhận, rồi ghi vào spec.
  - **Người chịu trách nhiệm**: Dev (Thanh Phương / Kieu Son Tung) xác nhận behavior → BA/Leader cập nhật spec Form.

### Câu hỏi bắt buộc gửi Dev trước khi merge

1. `appendRowData` được gọi ở **2 chỗ trong file `HandleFormAnswerSyncGoogleSheetTask`**, hay **2 chỗ trong toàn bộ codebase**? Các job sync Google Sheet của **Salon / Lesson / QR code** có dùng chung helper append với `rangeDefine = null` không? (§4.2)
2. Với `rangeDefine = "A1"`, khi cột A có ô trống **ở giữa** vùng data, Google `values.append` sẽ ghi **sau dòng cuối cùng** hay **đè vào dòng trống đầu tiên**? (Quyết định expected của TC-NEW-02 / TC-NEW-04.)
3. Sheet của KH (`1cEv-riz...`) hiện đã được "khôi phục tạm". Sau khi deploy fix, **9 bản ghi bị thiếu** của KH có tự động lên sheet không, hay cần chạy **sync lại toàn bộ**? (Triệu chứng gốc là **thiếu 9 件**, fix chỉ ngăn lỗi mới phát sinh — chưa có kế hoạch phục hồi data cũ.)
4. Mục 4.3 chưa ghi **mức risk regression** cho T1 — High/Medium/Low?

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — 3 GAP (§4.1), 2 RISK trong matrix
- [x] **B. Chất lượng từng TC** — fail B.1 (Expected không đo lường được), fail B.3 với TC26/TC27 (thiếu steps)
- [x] **C. Chất lượng bộ TC tổng thể** — không đánh giá được tỷ lệ Type/Priority (2 cột trống); phát hiện trùng lặp nhẹ TC05/TC08
- [x] **D. Spec alignment** — phát hiện mâu thuẫn TC09 → §6
- [x] **E. Hành chính** — thiếu tên tester + ngày submit
- [x] **F. Base checklist LME**
  - [x] **F.1 Checklist web** — liên quan: **CL-Func-18** (load UI trước/submit sau release) ❌ chưa cover; **CL-Func-25** (multi-thread/thao tác liên tục) ⚠️ TC22 `Not test`; **TC-05** (format hiển thị spreadsheet) ⚠️ một phần; **TC-10** (API ngoài + rate limit + retry không mất data) ❌ chưa cover; **TC-12** (kịch bản hệ bất thường) ⚠️ một phần (TC18–TC21); **TC-23** (đối chiếu màn hình ↔ output spreadsheet) ❌ **chưa cover — đây là GAP-02**. A.2 Non-function: không có URL/màn hình mới → N/A.
  - [x] **F.2 Checklist job** — **B.2 / CLJ01 (Sync Google rate limit + retry)**: ❌ **chưa cover** phần rate limit + request lớn liên tục → [MAJOR] §4.2, đề xuất TC-NEW-05.
  - [x] **F.3 Các tính năng chung** — **C.5 Google sheet**: ✅ job retry (TC18–TC21) và ✅ **2 loại header form cũ/mới** (TC10–TC13) — cover tốt. ❌ chưa cấp quyền / mất quyền (chấp nhận được: fix không chạm auth). ❌ tiêu đề cột xuống dòng, ❌ tên file ký tự đặc biệt → [NIT]. ⚠️ **4 tính năng liên kết spread (Form/Salon/Lesson/QR)** — mới cover Form; Salon/Lesson/QR **phụ thuộc câu trả lời của Dev** (§4.2). C.1–C.4, C.6–C.8: không liên quan task này.

> **Member đã tick gì trong `04-tc-list.md`?** — Phần "Base checklist LME" trong file 04 **chưa tick mục nào** (file được fetch từ Sheet, member chưa điền). Không có case "tick nhưng chưa cover" → không flag MAJOR ở điểm này, nhưng đề nghị member điền phần này ở round 2.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Draft sinh bởi /review-tc ngày 2026-07-11. Input: 01-bug-task.md + 03-dev-impact.md + 04-tc-list.md (27 TCs, fetch từ Sheet "Sync google" rows 439-465). Không có 02-spec-reference.md → dùng LME-SYSTEM-SPEC tổng. Leader verify trước khi gửi member. -->
