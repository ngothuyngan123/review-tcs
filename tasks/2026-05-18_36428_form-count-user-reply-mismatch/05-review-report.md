# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36428 — Form `初回アンケート` hiển thị `0人` nhưng `表示` có data |
| Reviewer (Leader) | Claude (draft) — Leader verify lại |
| Tester được review | (sheet team — file 04 fetch từ Sheet master) |
| Ngày review | 2026-05-18 |
| Version TCs | v1 (fetched từ Sheet "Improve form 01/2025" range A313:J339) |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC base tốt cho happy path "save tab 5 sau khi user đã submit" nhưng (a) thiếu test **đúng race condition** (admin mở tab 5 → user submit → admin save) — đây là root cause chính; (b) 2 row TC bỏ trống (form copy, account staff); (c) thiếu verify từng trường setting tab 5 lưu đúng giá trị sau fix (Dev đã cảnh báo); (d) auto-fill của file 01 + 03 từ Redmine **CHƯA được tester verify** (checkbox chưa tick).

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần **regression matrix theo từng tab setting** (tab 1, 2, 4 + tab 5 màn 1-4) và có check DB `form_answer.count_user_reply` ở expected — đúng hướng. Tuy nhiên TC hiện chỉ test **flow tuần tự** (user submit xong rồi admin mới save), trong khi root cause của bug là **race condition timing** (admin đã mở tab 5 trước khi user submit, save sau khi user submit). Ngoài ra cần điền nội dung cho 2 row đang để trống (form copy, account staff), liệt kê rõ các trường setting tab 5 và verify mỗi trường lưu đúng giá trị sau fix.

---

## 3. Coverage Matrix

> Note: File 04 fetch từ Sheet master tab "Improve form 01/2025" theo schema outline lồng nhau (KHÔNG phải 10-cột chuẩn). Khi suy luận coverage, dùng Function/Item (col C) + Detail (col D) + Precondition (col E) + Step (col F/G) + Expected (col H) làm input cho mapping.
> Reference Spec: KHÔNG có `02-spec-reference.md` → fallback LME-SYSTEM-SPEC tổng (Form section). Cần ghi chú rõ trong report.

| Impact | Loại | Priority | TCs map (theo row trong sheet) | # TC | Status |
|---|---|---|---|---|---|
| BUG — count_user_reply bị reset khi save 各種設定 | Fix | — | Row 315 (user đã submit + admin save tab 5 màn 1, expect DB count đúng), 317, 319, 321 | 4 | RISK (xem 4.1 BLOCKER-1: thiếu race condition timing) |
| F1 — Save setting `各種設定` (`public/js/form_answer/component/other-settings.js`) | Function | Direct | Row 315-321 (tab 5 màn 1-4 save) + Row 316, 318, 320 ("setting thêm => save") | 7 | RISK (thiếu boundary + thiếu enumerate trường — xem 4.2 MAJOR-2) |
| D1 — `form_answer.count_user_reply` | Data | — | Row 315 (expected check DB) | 1 | RISK (chỉ 1 expected, thiếu boundary: count=0, count cao, sau xóa reply) |
| T1 — Save setting `各種設定` tab 5 (Dev cảnh báo High risk: check từng trường) | Feature | High | Row 315-321, Row 322-332 (tab 1/2/4 regression) | ~15 | RISK (xem 4.2 MAJOR-2) |
| (Regression) — Save setting **các tab khác** (tab 1, 2, 4) | Regression | — | Row 322 (tab 1), 324/326/328 (tab 2 màn 1-3), 330/332 (tab 4 màn 1-2) | 6 | RISK — **thiếu tab 3** (xem 4.2 MAJOR-1) |
| (Regression) — User trả lời form từ các môi trường khác nhau | Regression | — | Row 333 (in app iOS/Android), 334 (ngoài app), 335 (qua button) | 3 | RISK — expected "có count số user" quá generic, không check DB / màn list (xem 4.2 MAJOR-3) |
| (Regression) — Form rẽ nhánh | Regression | — | Row 336 (đổi vị trí page), 337 (add/xóa page) | 2 | RISK — expected "có count số user" quá generic |
| (Regression) — Form copy | Regression | — | Row 338 (rỗng) | 0 | **GAP — heading có nhưng không có precondition/step/expected** |
| (Regression) — Account staff | Regression | — | Row 339 (rỗng) | 0 | **GAP — heading có nhưng không có precondition/step/expected** |

### ORPHAN TCs

| TC ID / Row | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC nào hoàn toàn lạc scope. Tất cả map được vào BUG / F1 / D1 / T1 / Regression | Giữ nguyên |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] BUG (Row 315-321)**: TC hiện chỉ test flow tuần tự "user submit form → sau đó admin save tab 5". **KHÔNG** test đúng race condition root cause: "admin đã **mở** tab 5 → user submit → admin nhấn **save**" (đây là sequence Dev mô tả: admin có data cũ ở client, save thì ghi đè data backend đã update). — **Fix**: thêm TC race-condition trong mục §5 (TC-NEW-01).
- **[BLOCKER] GAP-1 (Row 338, Form copy)**: TC để trống — chỉ có heading "Check form copy" mà không có precondition / step / expected. Nếu form copy không test → khi copy 1 form đã có user trả lời, count_user_reply của bản copy có sai không? Có thể là vector regression mới. — **Fix**: điền chi tiết TC trong mục §5 (TC-NEW-02).
- **[BLOCKER] GAP-2 (Row 339, Account staff)**: TC để trống — chỉ có heading "check account staff". CL1 LME checklist yêu cầu test cả staff được/không được phân quyền. Vì task chạm save settings → staff có quyền save không? Staff không quyền có bypass được không? — **Fix**: điền chi tiết TC trong mục §5 (TC-NEW-03).

### 4.2 Major (nên fix)

- **[MAJOR] MAJOR-1 (regression tab 3)**: TC regression cho save tab 1, 2, 4 đầy đủ nhưng **không có tab 3**. Dev impact mục 4.3 nói "check lại từng trường 1" — nghĩa là mọi tab phải được verify. — **Fix**: thêm TC save tab 3 màn 1, 2, ... (tuỳ form spec) tương tự row 324-332.
- **[MAJOR] MAJOR-2 (verify từng trường tab 5 lưu đúng giá trị sau fix)**: Dev cảnh báo "check lại từng trường 1 xem có update đc k" trong mục 4.3. Fix thay đổi logic save từ "ghi đè tất cả trường" → "chỉ ghi trường được setting". Rủi ro regression: **một số trường được setting BỊ MẤT** vì fix gửi thiếu trường. TC hiện chỉ check "save success" + count đúng, KHÔNG enumerate từng trường setting trong tab 5 và verify giá trị mỗi trường sau save. — **Fix**: liệt kê các trường setting trong tab 5 (từ spec / xem trực tiếp UI) → mỗi trường có 1 TC: setup value mới → save → check DB field tương ứng có lưu đúng giá trị mới.
- **[MAJOR] MAJOR-3 (expected "có count số user" quá generic)**: Row 333-337 expected chỉ ghi "có count số user" — không nói **số lượng cụ thể**, không nói **check ở đâu** (màn list / DB / chat 1:1), không có acceptance criteria đo lường được. — **Fix**: cụ thể hoá expected — vd "Sau khi user submit từ ngoài app LINE, màn list form hiển thị '1人' (chứ không phải '0人'), DB `form_answer.count_user_reply = 1`".
- **[MAJOR] MAJOR-4 (auto-fill 01 + 03 chưa verify)**: 2 file `01-bug-task.md` và `03-dev-impact.md` đều auto-filled từ Redmine bởi `/new-task` (2026-05-18) NHƯNG checkbox "Tester verify auto-fill chính xác" **CHƯA tick** ở cả 2 file. F/D/T mapping có thể chưa đầy đủ hoặc mapping sai. Đặc biệt: Dev list mục 4.2 = "k có data update" nhưng Leader (Claude) suy luận thêm D1 `form_answer.count_user_reply` — Dev cần confirm có còn data nào khác bị ảnh hưởng không. — **Fix**: tester đọc lại Redmine #36428 (cả description gốc + journal Ngọc Ánh 17/5 + journal Kim Cúc 18/5) → tick checkbox verify ở cả 01 và 03 → flag thêm F/D/T nếu thấy thiếu (đặc biệt: framing của Ngọc Ánh — "form hiển thị text giới hạn dù user chưa trả lời" — có thể là hệ quả khác của cùng bug count_user_reply bị reset → cần TC riêng).
- **[MAJOR] MAJOR-5 (thiếu boundary cho D1)**:
  - count_user_reply = 0 (form mới tạo, chưa user nào submit) → admin mở tab 5 save → count vẫn 0
  - count_user_reply ở mức cao (>1000) → admin save → count không bị reset
  - User submit → user **delete reply** (nếu spec cho phép) → admin save → count đúng
  - **Fix**: thêm 3 TC boundary tương ứng.
- **[MAJOR] MAJOR-6 (LME CL5 — double click save)**: Bug fix động đến logic save settings. Nếu admin double-click button save trong tab 5 → có ghi đè count 2 lần không? Có duplicate request không? — **Fix**: thêm TC double click button save tab 5.
- **[MAJOR] MAJOR-7 (LME CL2 — reload sau save)**: Sau khi save tab 5 → reload màn list form → check count vẫn đúng, không bị lệch state giữa client-server. — **Fix**: thêm TC reload sau save.
- **[MAJOR] MAJOR-8 (LME CL3 — chuyển tab)**: Bug fix thay đổi logic save tab 5 — có ảnh hưởng khi user mở nhiều tab cùng lúc và chuyển qua lại không? — **Fix**: thêm TC mở tab 5 → chưa save → chuyển sang tab khác → quay lại tab 5 → save → check data tab 5 không bị reset, count không bị ảnh hưởng.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Row 315-321 expected có typo**: "màn list hiên thị" → "hiển thị"; "reselt câu trả lời" → "result câu trả lời".
- **[MINOR] File 04 không có TC ID + Type + Priority + Assignee + Status**: schema sheet master không khớp 10-cột chuẩn. Khi sync ngược về Sheet thì OK, nhưng khi review thì khó trace TC nào đã/chưa run. — **Fix**: thống nhất với team nếu cần normalize schema, hoặc giữ nguyên và bỏ qua note này.
- **[MINOR] Row 316/318/320 "Có thực hiện setting thêm => save"**: precondition + expected không nói rõ "setting gì". 1 tester có thể chỉ thay đổi 1 field, tester khác thay đổi 10 fields → kết quả khác nhau. — **Fix**: enumerate cụ thể từng setting thay đổi (overlap với MAJOR-2).
- **[MINOR] Tab 5 màn 4 (Row 321) không có companion "setting thêm => save"** như màn 1/2/3 — bất đối xứng. — **Fix**: thêm row "Có thực hiện setting thêm => save" cho tab 5 màn 4.

### 4.4 Nit (gợi ý)

- **[NIT]** Khi sync ngược về Sheet master, cân nhắc bổ sung cột "Bug ref" để row 315 trở đi có link Redmine #36428 → dễ trace sau này.
- **[NIT]** Note Ngọc Ánh 17/5 (form hiển thị text giới hạn dù chưa trả lời) có thể là **biểu hiện thứ 2** của cùng bug count_user_reply bị reset (nếu form check "đã trả lời rồi" dựa trên 1 field khác cũng bị reset cùng). Đáng thêm 1 TC cụ thể: form có setting "giới hạn 1 lần trả lời" → user chưa trả lời → admin save tab 5 → user mở form → expect form **không** hiển thị text giới hạn, user vẫn trả lời được.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` (hoặc sheet master tab "Improve form 01/2025") ở round tiếp theo. Map to Impact ghi rõ để Leader trace.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Race condition: admin mở tab 5 → user submit → admin save → count không bị reset | (1) Form `初回アンケート` đang public, đã có 0 reply. (2) Admin đăng nhập web → mở màn detail form → click vào tab `各種設定` (tab 5) — KHÔNG save vội. (3) 1 user LINE chuẩn bị sẵn ở app LINE, đã click vào link form. | (a) User LINE submit form (browser confirm submit thành công). (b) Admin (browser khác đã mở tab 5) kiểm tra count ở màn list = 1人. (c) Admin quay lại tab `各種設定` → nhấn `保存` (KHÔNG đổi setting nào). | - Save tab 5 thành công (msg success).<br>- Màn list form vẫn hiển thị `1人` (KHÔNG về 0).<br>- DB: `form_answer.count_user_reply = 1`.<br>- Hiển thị data câu trả lời của user trong `表示`. | High | Positive (race condition) | BUG, F1, D1, T1 |
| TC-NEW-02 | Form copy: copy form đã có reply → count của form gốc và form copy đúng → save tab 5 form copy không reset count form gốc | (1) Form A đang public, đã có 3 user reply (count = 3). (2) Form A đã được copy thành form B (mới, chưa public). | (a) Mở form B → tab `各種設定` → save (không đổi setting). (b) Kiểm tra count cả 2 form. | - Form A: count = 3 (giữ nguyên).<br>- Form B: count = 0 (form mới, copy không kế thừa count).<br>- DB: `form_answer.count_user_reply` của form A = 3, form B = 0. | High | Regression | T1 |
| TC-NEW-03 | Account staff có quyền form: save tab 5 không bị reset count | (1) Bot có 1 staff được phân quyền `Form` (read + write). (2) Form đã có 2 user reply (count = 2). | (a) Staff login → mở form → tab 5 → save không đổi setting. | - Save thành công.<br>- Count vẫn = 2.<br>- DB không bị reset. | High | Positive (permission) | T1, LME CL1 |
| TC-NEW-04 | Account staff KHÔNG có quyền form: không thao tác được tab 5 | (1) Bot có 1 staff KHÔNG được phân quyền `Form`. | (a) Staff login → cố access URL form detail → kiểm tra hiển thị / redirect. | - Hiển thị "Không có quyền" hoặc redirect về dashboard.<br>- KHÔNG thấy nút save tab 5.<br>- Direct URL không bypass được. | High | Negative (permission) | T1, LME CL1, LME A.2 Security |
| TC-NEW-05 | Verify từng trường setting trong tab 5 lưu đúng sau fix | (1) Form đã có reply, count = 1. (2) Đã enumerate được X trường setting trong tab 5 (Dev/Tester confirm list trường). | Với mỗi trường setting i: (a) Đổi giá trị trường i sang giá trị mới (khác default). (b) Save tab 5. (c) Reload màn → kiểm tra giá trị trường i. (d) Verify count vẫn = 1. | - Mỗi trường setting lưu đúng giá trị mới sau save.<br>- Không trường nào bị mất giá trị (do fix gửi thiếu field).<br>- Count_user_reply không thay đổi sau save. | High | Boundary (enumerate) | F1, T1 |
| TC-NEW-06 | Save tab 3 (regression — đang thiếu) | (1) Form đã có reply, count = 1. (2) Admin mở form detail → tab 3. | (a) Save tab 3 màn 1 (không đổi setting). (b) Save tab 3 màn 1 (có đổi setting). (c) Lặp cho từng màn của tab 3 nếu có nhiều màn. | - Save thành công.<br>- Count_user_reply vẫn = 1.<br>- Settings của tab 3 lưu đúng. | High | Regression | T1 |
| TC-NEW-07 | Boundary: count = 0 → save tab 5 → count không bị set sai (vd −1 / null) | (1) Form mới tạo, chưa user nào reply. count = 0. | (a) Admin mở tab 5 → save (không đổi setting). | - Count vẫn = 0 (không bị set thành null / negative / random).<br>- DB: `form_answer.count_user_reply = 0`. | Medium | Boundary | D1 |
| TC-NEW-08 | Boundary: count cao (≥ 100) → save tab 5 → count giữ nguyên | (1) Form đã có ≥ 100 reply (seed test data). | (a) Admin mở tab 5 → save. (b) 1 user submit thêm. (c) Admin save lại tab 5. | - Sau (a): count = 100. Sau (b): 101. Sau (c): 101 (không bị reset về 100). | Medium | Boundary | D1 |
| TC-NEW-09 | LME CL5 — Double click button save tab 5 | (1) Form có 1 reply, count = 1. | (a) Admin mở tab 5 → double-click button `保存` rất nhanh. | - Chỉ 1 request save được gửi (check Network tab).<br>- Hoặc 2 request đều thành công không gây inconsistency.<br>- Count vẫn = 1, không bị duplicate ghi đè. | Medium | Boundary (UI) | F1, LME CL5 |
| TC-NEW-10 | LME CL2 — Reload sau save tab 5 | (1) Form có 2 reply, count = 2. | (a) Admin save tab 5. (b) F5 reload page. (c) Mở lại tab 5. | - Sau reload: tất cả setting tab 5 hiển thị giá trị vừa save.<br>- Count_user_reply hiển thị 2 ở màn list.<br>- DB: count = 2. | Medium | Regression | F1, LME CL2 |
| TC-NEW-11 | LME CL3 — Chuyển tab 5 ↔ tab khác chưa save | (1) Form có 1 reply, count = 1. | (a) Mở tab 5 → đổi giá trị 1 setting (chưa save). (b) Chuyển sang tab 1. (c) Quay lại tab 5 → check giá trị. (d) Save. | - Bước (c): tab 5 nhớ giá trị đã đổi ở (a) (hoặc revert về saved value — tuỳ spec). Behavior nhất quán.<br>- Sau (d): count vẫn = 1, setting save đúng. | Low | Regression | F1, LME CL3 |
| TC-NEW-12 | Verify framing Ngọc Ánh — Setting "giới hạn 1 lần trả lời" không bị stuck "đã trả lời" sau save tab 5 | (1) Form có setting "giới hạn 1 lần trả lời/user". (2) 1 user LINE chưa từng reply form này. | (a) Admin mở tab 5 → save (không đổi setting). (b) User mở link form từ LINE. | - User vẫn vào được form và submit được (KHÔNG bị hiển thị "Bạn đã trả lời rồi").<br>- Sau submit: count = 1.<br>- Nếu user submit lần 2 → bị reject đúng theo spec. | High | Negative (verify Ngọc Ánh framing) | BUG, T1 |
| TC-NEW-13 | LME C.5 Google sheet sync — save tab 5 không gây mismatch giữa count và sheet rows | (1) Form đã liên kết Google Sheet. (2) Có 2 reply đã sync sang sheet (sheet có 2 data rows). | (a) Admin save tab 5. (b) 1 user submit thêm → expect sync sang sheet (3 rows). (c) Admin save tab 5 lại. | - DB count = 3 sau bước (b).<br>- Sheet có 3 data rows.<br>- Sau (c): DB count vẫn = 3, sheet vẫn 3 rows, không trigger job re-sync sai. | Medium | Regression | T1, LME C.5 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — bug fix chỉ thu hẹp scope save (chỉ save trường được setting thay vì save tất cả), không thay đổi behavior end-user nên KHÔNG cần sửa LME-SYSTEM-SPEC.
- [ ] Cần update spec — chi tiết:
  - Section:
  - Nội dung cần update:
  - Người chịu trách nhiệm update:

**Note Spec reference**: Folder review KHÔNG có `02-spec-reference.md` → fallback tham chiếu `templates/LME-SYSTEM-SPEC.md` (Form section). Khuyến nghị thêm `02-spec-reference.md` ghi rõ list trường thực tế trong tab `各種設定` để TC-NEW-05 có input enumeration chính xác.

---

## 7. Checklist đã chạy

- [x] A. Coverage — phát hiện 2 GAP (Row 338, 339) + 1 missing tab (tab 3)
- [x] B. Chất lượng từng TC — phát hiện expected generic (Row 333-337), bất đối xứng (Row 321 thiếu companion), không có Type/Priority/Assignee (note Minor)
- [x] C. Chất lượng bộ TC tổng thể — phát hiện thiếu boundary + thiếu negative permission + thiếu race condition
- [x] D. Spec alignment — không có spec mâu thuẫn; note fallback LME-SYSTEM-SPEC
- [x] E. Hành chính — file 04 KHÔNG có TC ID/Tester/Version (sheet master schema khác template) — Minor
- [x] F. Base checklist LME — đối chiếu sau:
  - [x] F.1 Checklist web:
    - **CL1 (account staff)**: Row 339 rỗng → **GAP** (BLOCKER-3 đã flag, TC-NEW-03 + TC-NEW-04 đề xuất)
    - **CL2 (reload sau save)**: chưa có TC → MAJOR-7, TC-NEW-10
    - **CL3 (chuyển tab setting)**: chưa có TC → MAJOR-8, TC-NEW-11
    - **CL5 (double click)**: chưa có TC → MAJOR-6, TC-NEW-09
    - **CL7 (plan limits)**: form có giới hạn plan — task không trực tiếp chạm scope plan limit của save settings, có thể skip
    - **CL10 (update/delete data ảnh hưởng)**: covered gián tiếp qua tab 1/2/4 regression
    - **CL11 (CRUD đúng bản ghi)**: covered gián tiếp (test trên form A, không ảnh hưởng form khác — nên thêm explicit TC nếu có thời gian)
    - A.2 Non-function:
      - URLs đo lường: không liên quan
      - Regression: tab 1/2/4 covered; **tab 3 thiếu** → MAJOR-1, TC-NEW-06
      - Security: không có URL mới → skip
      - Compatibility (Win+Mac, iOS+Android): Row 333 chỉ user-side iOS/Android — chưa có admin Win+Mac → có thể bổ sung TC nhẹ
  - [x] F.2 Checklist job:
    - **B.1 Job callback**: không liên quan
    - **B.2 Job sync Java (CLJ01 — Google sync)**: form có Google sheet sync → bug fix có thể ảnh hưởng → TC-NEW-13 đề xuất
  - [x] F.3 Các tính năng chung:
    - **C.5 Google sheet**: form có liên kết Google Sheet → TC-NEW-13
    - Các mục khác (C.1-C.4, C.6-C.8): không liên quan trực tiếp với scope task này

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
