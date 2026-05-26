# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | KH #36317 (回答ID 28091) |
| Reviewer (Leader) | _<điền>_ |
| Tester được review | _<điền>_ |
| Ngày review | 2026-05-12 |
| Version TCs | v1 (sheet `Improve form 01/2025 Line user` rows 1550-1577) |
| Vòng review | Round 1 — **đã Leader chốt scope** |

> **Clarify từ Leader (2026-05-12)**: Bug ở **web layer** — web lưu sai `page_id` vào DB (status_sync=0). Job chỉ là consumer pass-through (đọc đúng theo `page_id` ở DB rồi sync lên Spread). Root fix nằm hoàn toàn ở web → **KHÔNG cần test logic sync Spread / job retry**. Scope review xoay quanh F1 (`storeRenderForm`) + F2 (`form_render_v3.js`) + T1/T2.

> **Input thiếu**: `02-spec-reference.md` không có → fallback tham chiếu `templates/LME-SYSTEM-SPEC.md` (Form ver3.0).

---

## 1. Verdict

- [ ] **APPROVED**
- [x] **APPROVED WITH CHANGES** — Approve sau khi member bổ sung 3 TC: **TC-NEW-01**, **TC-NEW-09**, **TC-NEW-20**. Không cần review lại round 2.
- [ ] ~~REJECTED~~

**Lý do**: Bộ TC v1 cover tốt workaround validate (msg JP cho 3 case: thừa/thiếu item, đổi vị trí item, thêm/xóa/đổi page). Sau khi Leader clarify scope, chỉ thiếu 3 case quan trọng: (1) reproduce sát case KH với form rẽ nhánh sâu 3-levels, (2) chuyển nhánh giữa chừng bằng back-button (kiểm tra ghost data), (3) flow user reload theo hướng dẫn message JP.

---

## 2. Tóm tắt cho member

Bộ TC em viết khá đầy đủ về phần **validate workaround** (14 TC negative + 6 TC happy + 6 TC verify data sau submit). Sau khi anh clarify với em — root fix ở web layer (lưu sai `page_id`), job sync chỉ là pass-through nên không cần test sync logic — chỉ cần em bổ sung **3 TC** nữa là duyệt: (1) `TC-NEW-01` reproduce sát case KH (form rẽ nhánh sâu 3-levels), (2) `TC-NEW-09` switch branch giữa chừng bằng back-button (verify ghost data), (3) `TC-NEW-20` flow user reload theo hướng dẫn msg JP. Chi tiết steps ở §5.

---

## 3. Coverage Matrix (đã re-scope theo Leader)

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — Reproduce case KH (form rẽ nhánh sâu, lưu sai `page_id`) | Fix | — | _(thiếu — sẽ cover bởi TC-NEW-01)_ | 0 → 1 | GAP → **OK sau khi bổ sung** |
| **F1** — `storeRenderForm` (server check) | Function | Direct | TC-01..03, 08..15, 20..22 (validate msg JP) + TC-06,07,18,19,25,26 (verify data sau lưu) | 20 | OK |
| **F2** — `form_render_v3.js` (frontend render) | Function | Direct | TC-04,05,16,17,23,24 (render form happy) + 14 TC msg ở trên | 20 | OK |
| **T1** — Trả lời form, số item/page user ≠ admin | Feature | High | TC-01..03, 08..15, 20..22 | 15 | OK |
| **T2** — Trả lời form happy path (regression) | Feature | High | TC-04,05,16,17,23,24 (1 page / nhiều page / basic) + TC-NEW-01,09,20 (rẽ nhánh deep + back + reload) | 6 → 9 | RISK → **OK sau khi bổ sung** |
| ~~T3 — Sync data → GG Spread~~ | ~~Feature~~ | — | **Out of scope** — job pass-through, không bị chạm code | — | N/A |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động |
|---|---|---|---|
| _(không có)_ | | | Mọi TC đều thuộc scope F1/F2/T1/T2. |

---

## 4. Issues phát hiện (đã re-scope)

### 4.1 Blocker → Đã downgrade hoặc giải quyết

- **[BLOCKER → GIẢI QUYẾT BẰNG TC-NEW-01]** Không có TC reproduce sát case KH (form rẽ nhánh sâu 3-levels). Workaround chỉ chặn submit khi mismatch số item, KHÔNG che được scenario gốc (số item = setting nhưng lưu nhầm `page_id`). → Bổ sung TC-NEW-01.
- ~~[BLOCKER] GAP-2 — Thiếu cover §C.5 Google Sheet~~ **Leader reject**: Job sync là pass-through, không chạm code → không cần test.
- **[BLOCKER → GIẢI QUYẾT BẰNG TC-NEW-09]** Form rẽ nhánh conditional (ver3.0) — TCs v1 chỉ phân loại "1 page" vs "nhiều page", không có TC test switch branch / back-button. Đây là context bug (回答ID 28091). → Bổ sung TC-NEW-09.

### 4.2 Major → Đã Leader cân nhắc, chốt skip (trừ TC-NEW-20)

- **[MAJOR → GIẢI QUYẾT BẰNG TC-NEW-20]** Sau khi msg JP hiển thị, user phải reload theo hướng dẫn → có TC verify reload load đúng setting admin mới không? → Bổ sung TC-NEW-20.
- ~~[MAJOR] CL18 (load-before-submit)~~ **Skip** — Leader: workaround chạy ở server, không phụ thuộc FE state khi load.
- ~~[MAJOR] Bypass server validate~~ **Skip** — out of scope của task.
- ~~[MAJOR] CL5 double-click~~ **Skip** — không phải nguyên nhân bug này.
- ~~[MAJOR] CLJ01 sync retry~~ **Skip** — Leader: sync logic không cần test.
- ~~[MAJOR] §C.2 action sau submit~~ **Skip** — không chạm.
- ~~[MAJOR] §C.3/§C.4 friend info/tag qua form~~ **Skip** — không chạm.
- ~~[MAJOR] TC-13/14/15 chiều happy (đổi page trước user mở)~~ **Skip** — Leader: case đã được cover ngầm bởi TC-04/05/16/17/23/24 (user trả lời form theo setting hiện tại, không có msg).
- ~~[MAJOR] CL12 boundary max~~ **Skip** — không phải scope task này.

### 4.3 Minor (member có thể fix khi push lên sheet, không block approve)

- **[MINOR] Format sheet thiếu cột TC ID + Priority**: Khi member push lên sheet review tab, đề xuất bổ sung 2 cột này để Leader/Dev dễ tracking trạng thái khi fix bug.
- **[MINOR] TC-02, 03, 09, 10, 12,...** inherit Sub4 ô trống. Khi tester khác test lại phải nhớ ngữ cảnh TC trên. Đề xuất ghi đầy đủ Sub4 mỗi TC.
- **[MINOR] Expected mơ hồ**: TC-04/05/16/17/23/24 ghi "user trả lời form thành công" — viết rõ "submit không lỗi, redirect/hiện màn thank-you, KHÔNG hiện msg JP".

### 4.4 Nit (gợi ý — optional)

- **[NIT]** Boundary item TC-04 (1-3) + TC-05 (3-6) chồng nhau ở mốc 3. Nếu có thời gian, tách: đúng 1 item / đúng 3 item / đúng 6 item.
- **[NIT]** TC-15 "page đầu ra giữa" — ghi rõ VD: "form 5 page, đổi page 1 thành page 3".
- **[NIT]** Test font JP `フォームの質問数が変更されました...` hiển thị đúng trên LINE app iOS/Android.

---

## 5. TCs đề xuất bổ sung (Leader đã chốt — 3 TC)

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | Reproduce KH #36317 — form rẽ nhánh sâu 3-levels, verify câu trả lời page 3 hiển thị đúng page 3 trên form result | Form ver3.0 có 3 page (page1 → page2 → page3, mỗi page 2-3 item); đã liên kết GG Spread; admin setting **không thay đổi** suốt test | 1) User (LINE friend) mở link form trên app LINE<br>2) Trả lời page1 → next<br>3) Trả lời page2 → next<br>4) Trả lời page3, nhập text dễ nhận biết "ANSWER_P3_TEST" → submit<br>5) Admin mở **form result** trên web<br>6) Admin mở **GG Spread** liên kết (chờ job sync xong) | (a) Form result phía admin: câu trả lời "ANSWER_P3_TEST" hiển thị **đúng ô item của page 3**, KHÔNG nhảy lên page1<br>(b) GG Spread: "ANSWER_P3_TEST" nằm ở **cột tương ứng item của page 3**, không sai cột<br>(c) Không hiện msg JP (vì setting không đổi) | High | Regression | BUG, F1, T2 |
| **TC-NEW-09** | Form rẽ nhánh conditional — switch branch giữa chừng bằng back-button, verify không có ghost data từ nhánh cũ | Form ver3.0 có conditional jump: page1 chọn "A" → page2A, chọn "B" → page2B | 1) User mở form, ở page1 chọn "A" → đến page2A<br>2) Trả lời 1 item ở page2A<br>3) Bấm **back-button** về page1<br>4) Đổi chọn sang "B" → đến page2B<br>5) Trả lời page2B → submit<br>6) Admin check form result + GG Spread | (a) Form result chỉ hiển thị câu trả lời của nhánh B<br>(b) GG Spread: cột nhánh A trống, cột nhánh B có data đúng<br>(c) KHÔNG có ghost data từ nhánh A bị giữ lại | High | Regression | F1, F2, T2 |
| **TC-NEW-20** | Flow reload theo hướng dẫn msg JP — sau khi nhận msg, user reload load fresh setting admin mới và submit thành công | User đang trả lời form, admin sửa setting (thêm/xóa item) → user submit → workaround chặn + hiện msg JP `フォームの質問数が変更されました...` | 1) Setup: user mở form, đang trả lời<br>2) Admin thêm 1 item vào page user đang trả lời, save<br>3) User submit → msg JP hiện<br>4) User reload page (F5 hoặc theo hướng dẫn msg)<br>5) Quan sát form sau reload<br>6) User trả lời lại đầy đủ theo setting mới → submit | (a) Sau reload: form load fresh, hiển thị item mới mà admin vừa thêm<br>(b) User trả lời + submit lần 2 thành công, KHÔNG còn msg JP<br>(c) Data của lần submit thành công lưu đúng vào form result + GG Spread | Medium | Functional | F1, F2, T2 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: Form ver3.0 — submit flow (`templates/LME-SYSTEM-SPEC.md` Form section)
  - **Nội dung cần update**: Bổ sung rule validate workaround: "Khi submit, server compare tổng câu trả lời/page vs số câu hỏi/page của setting hiện tại; nếu khác → trả error + message `フォームの質問数が変更されました。画面を再読み込みしてから再度ご回答ください`". Ghi rõ đây là **workaround** vì root cause của KH #36317 (web lưu sai `page_id`) chưa xác định.
  - **Người chịu trách nhiệm update**: Dev assignee + PM.

---

## 7. Checklist đã chạy

- [x] A. Coverage — pass sau bổ sung TC-NEW-01 (BUG), TC-NEW-09 (T2 conditional branch)
- [x] B. Chất lượng từng TC — MINOR: expected mơ hồ ở 6 TC happy
- [x] C. Chất lượng bộ TC — pass sau re-scope
- [x] D. Spec alignment — flag spec update workaround
- [x] E. Hành chính — partial (sheet thiếu cột TC ID + Priority — MINOR)
- [x] F. Base checklist LME — **đã re-scope theo Leader**:
  - [x] F.1 Checklist web — N/A các CL về sync/security/double-click (out of scope task)
  - [x] F.2 Checklist job — N/A (job pass-through, không chạm)
  - [x] F.3 Các tính năng chung — N/A §C.2/C.3/C.4/C.5 (web layer fix, không chạm các tính năng chung)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | 2026-05-12 |
| Tester | (đã đọc & hiểu feedback) | |
