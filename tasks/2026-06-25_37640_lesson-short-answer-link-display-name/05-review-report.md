# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37640 — [Lesson] câu trả lời ngắn bị ép liên kết vào システム表示名` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `Ngọc Ánh` (TC fetch từ sheet) |
| Ngày review | `2026-06-25` |
| Version TCs | `v1` (13 TC, TC001–TC016, sheet bỏ trống TC011/012/015) |
| Vòng review | `Round 1` |

> **Spec reference**: không có file `02-spec-reference.md` riêng — dùng `templates/LME-SYSTEM-SPEC.md` tổng + comment chốt trong `01-bug-task.md` (liên kết bắt buộc nhưng đích liên kết 連携先 tự chọn).
> **Phạm vi review**: file `04-tc-list.md` (13 TC). Folder cũng có `04-tc-list.draft.md` (7 TC delta TC017–023 do `/write-tc` sinh) — đã dùng làm cơ sở cho §5 đề xuất bổ sung.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover tốt nhánh **Lesson** + bug gốc, nhưng nhánh **Salon (T2, High risk)** bất đối xứng — thiếu E2E "giữ システム表示名 → view_name", boundary và "loại liên kết vẫn khoá". Thêm 2 gap checklist LME (C.3 Friend info chỉ verify qua DB; TC-24 dropdown dùng chung) + 2 file input auto-fill chưa được tester verify.

---

## 2. Tóm tắt cho member

Bộ TC rất chắc ở **nhánh Lesson** và bắt đúng tim bug (TC008: đổi 連携先 → lưu friend_information_value, KHÔNG ghi đè システム表示名) — title rõ, expected đo lường được, có cả regression câu mail/radio/datetime giữ nguyên. Cần bổ sung chủ yếu là **đối xứng cho Salon** (Salon đang thiếu vài TC mà Lesson đã có) và **verify qua UI thay vì DB** (mở My page / right bar xem friend info, đúng góc nhìn manual tester) + 1 TC hành vi dropdown dùng chung khi click qua lại giữa các loại câu. 7 TC bổ sung đã được draft sẵn ở `04-tc-list.draft.md`, merge vào là xong.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (câu họ tên ghi đè システム表示名 → mở khoá 連携先) | Fix | — | TC008, TC001, TC002 | 3 | **OK** |
| F1 — view setting form **lesson** (điều kiện khoá dropdown 連携先) | Function | Direct | TC001, TC003, TC005, TC006, TC007, TC016 | 6 | **OK** |
| F2 — view setting form **salon** (điều kiện khoá dropdown 連携先) | Function | Direct | TC002, TC004 | 2 | **RISK** — thiếu boundary `can_delete=1` + "loại liên kết vẫn khoá" cho salon |
| F3 — `CalendarController::updateFriendInfoValue` | Function | Indirect | TC008, TC009 | 2 | **OK** |
| F4 — `CalendarSalonController::updateFriendInfoValue` | Function | Indirect | TC010 | 1 | **RISK** — thiếu regression nhánh `case -1` (giữ システム表示名 → view_name) cho salon |
| F5 — `CalendarManagementController::getDataFriendInfo` (seed -1/-2/-3) | Function | Indirect | TC001, TC002, TC013 | 3 | **OK** |
| F6 — `CalendarSettingSendFormService` / `CalendarSalonSettingSendFormService` | Function | Indirect | TC013 | 1 | **OK** (regression data cũ) |
| D1 — `friend_information_value` (đáp án câu họ tên) | Data | CREATE/UPDATE | TC008, TC010 | 2 | **RISK** — chỉ verify qua DB; thiếu verify hiển thị ở nơi friend info (C.3) |
| D2 — `line_users.view_name` (システム表示名) | Data | UPDATE | TC008, TC009, TC010 | 3 | **RISK** — nhánh `case -1` (ghi đè view_name) chỉ test lesson (TC009), salon thiếu |
| T1 — レッスン予約 (setting form + booking) | Feature | High | TC001, TC003, TC005, TC006, TC007, TC008, TC009, TC013, TC016 | 9 | **OK** |
| T2 — サロン予約 (setting form + booking) | Feature | High | TC002, TC004, TC010, TC013, TC014 | 5 | **RISK** — thiếu E2E `case -1` + boundary tự thêm + "loại liên kết vẫn khoá" cho salon |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không phát hiện TC lạc chủ đề — cả 13 TC đều map vào BUG / F* / D* / T*. | Giữ nguyên |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Specific code-check / Validation** — đổi điều kiện khoá UI từ `can_delete=0` → `can_delete=0 && friend_information_id==-3`, chỉ khối câu text. KHÔNG phải generic catch-all / race / migration / soft-delete. |
| Trigger space cần cover | {loại câu: **text / 単一選択 / 日時**} × {`can_delete`: **0 / 1**} × {`連携先 id`: **-1 (システム表示名) / -3 (メール) / custom friend info**}. Nhánh quan trọng: (a) text+can_delete=0+id≠-3 → mở khoá; (b) text+id==-3 → khoá; (c) text+can_delete=1 → mở khoá; (d) radio/datetime → khoá giữ nguyên; (e) E2E lưu theo id: -1→view_name / default→friend_information_value. |
| Số trigger TCs hiện cover | **Lesson ~ đầy đủ** (a:TC001, b:TC003, c:TC016, d:TC006/007, e:TC008/009). **Salon thiếu** (b:TC004 ok, nhưng c/d/e-case-1 chưa có → ~2/5). |
| KH report dạng | **Có root cause cụ thể** — KH mô tả rõ hành vi (決済時 短文回答 ghi đè システム表示名), không phải symptom-only. |
| Alternative root causes cần verify | N/A (không symptom-only). |
| Anti-patterns dính | **AP-5 (nhẹ)** — TC008/009/010 dẫn verify bằng "Check DB" `friend_information_value` / `view_name` trong khi fix chỉ chạm FE (blade); nên quan sát qua UI (My page / right bar). KHÔNG dính AP-1 (không generic-fix), KHÔNG AP-2 (không symptom-only), KHÔNG AP-6 (mục 3 đã list 7 caller). |

> Kết luận fix-shape: **không có BLOCKER**. Core (Lesson) cover đủ trigger. Gap chính = **bất đối xứng Salon** (trigger c/d/e-case-1) → MAJOR, không phải BLOCKER vì Salon vẫn có happy-path E2E (TC010) + câu mail khoá (TC004).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có._

### 4.2 Major (nên fix)

- **[MAJOR] FILE-01**: `01-bug-task.md` auto-filled từ Redmine (`2026-06-25 by /new-task`) nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**, và 2 field còn placeholder (Module/Màn hình, Môi trường phát hiện) — review chỉ có giá trị sau khi tester đọc lại Redmine và xác nhận. → Tester verify + tick checkbox.
- **[MAJOR] FILE-03**: `03-dev-impact.md` auto-filled từ Redmine nhưng checkbox **chưa tick**. Nguồn là journal **AI AUTO-FIXBUG** (không phải Dev người viết) → F1–F6 / D1–D2 / T1–T2 có thể chưa chuẩn. → Tester/Dev verify F/D/T + tick checkbox trước khi finalize.
- **[MAJOR] FIX-SHAPE / GAP-1 (F4, D2, T2 — Salon `case -1`)**: Không có TC nào verify nhánh **Salon "giữ 連携先 = システム表示名 → đặt lịch → システム表示名 cập nhật theo đáp án"** (đối xứng TC009 của Lesson). Đây là nhánh `case -1` của `CalendarSalonController::updateFriendInfoValue` trên feature High-risk. → Thêm **TC017** (§5).
- **[MAJOR] F.3 — C.3 Friend info (verify qua UI)**: Bug bản chất là về *nơi lưu friend info*, nhưng TC008/TC010 chỉ verify bằng "Check DB", **không** verify ở các nơi hiển thị/update friend info mà checklist C.3 yêu cầu (My page → tab 基本情報, Chat 1:1 → right bar). → Thêm **TC021** verify qua UI (§5).
- **[MAJOR] F.1 — CL-Func-24 / TC-24 (dropdown dùng chung)**: Dropdown 連携先 là UI component dùng chung có default; checklist TC-24 cảnh báo "dropdown có default thì hành vi tap bị sót". 13 TC test trạng thái từng loại câu **riêng lẻ** (load mới) nhưng **không** test hành vi **click qua lại** giữa text/radio/datetime trong cùng màn (stale state). → Thêm **TC022** (§5).

### 4.3 Minor (có thể fix sau)

- **[MINOR] GAP-2 (F2, T2 — Salon boundary)**: Thiếu đối xứng Salon cho boundary "câu 短文回答 tự thêm `can_delete=1` → dropdown enabled" (TC016 chỉ làm Lesson). → **TC019** (§5).
- **[MINOR] GAP-3 (F2, T2 — Salon "loại liên kết vẫn khoá")**: Thiếu đối xứng Salon cho "dropdown 「友だち情報に回答を記録」 vẫn khoá → liên kết vẫn bắt buộc" (TC005 chỉ làm Lesson). → **TC018** (§5).
- **[MINOR] GAP-4 (CL-Func-2 — Lesson reload)**: TC014 (保存+reload không lỗi blade) chỉ làm Salon; Lesson thiếu. → **TC020** (§5).
- **[MINOR] CL-NonF-1 Compatibility**: Fix đổi hành vi enable/disable của dropdown (JS/blade) nhưng không TC nào note kiểm Win/Mac × Chrome/Safari. → thêm note compat vào TC dropdown (TC022) hoặc 1 dòng Output note.
- **[MINOR] AP-5 / góc nhìn manual tester**: TC008/TC009/TC010 dẫn expected bằng tên cột DB (`friend_information_value`, `line_users.view_name`). Nên diễn đạt theo quan sát UI (đáp án hiển thị ở field friend info; システム表示名 ở right bar/My page không đổi). Giữ TC nhưng đổi cách verify.

### 4.4 Nit (gợi ý)

- **[NIT] Edge `id==-3`**: Dev tự nêu (file 03) — đổi 連携先 câu họ tên sang メール rồi bị khoá lại. Nên có 1 TC ghi nhận để xác nhận "vô hại". → **TC023** (§5). Cần Leader/Dev confirm hành vi này chấp nhận được (user khó đổi ngược).
- **[NIT] Cột Type/Priority trống**: file 04 fetch từ sheet không có Type/Priority → không đánh giá được tỷ lệ Positive/Negative/Boundary/Regression của bộ TC. Member nên bổ sung khi merge.
- **[NIT] PR link**: file 03 chỉ có commit hash `d788a7da27` + branch `ai_fixbug_37640`, không có URL PR clickable — nếu cần review fix-shape sâu hơn thì xin link PR.

---

## 5. TCs đề xuất bổ sung

> Đã được `/write-tc` draft sẵn trong `04-tc-list.draft.md` (TC017–TC023). Member merge vào `04-tc-list.md` rồi `/sync-ai-tc` (hoặc `/sync-review-tc` để push trực tiếp từ §5 này).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC017 | Salon E2E: giữ 連携先 câu お名前 = システム表示名 → đặt lịch salon → システム表示名 cập nhật theo đáp án (case -1) | Form salon, câu お名前 連携先 = システム表示名 (-1); user LINE bạn bè bot, システム表示名 = "山田太郎" | 1.Giữ 連携先 câu お名前 = システム表示名<br>2.User đặt lịch salon nhập お名前 = "新しい名前"<br>3.Mở Chat 1:1 / My page xem システム表示名 | システム表示名 đổi thành "新しい名前" (nhánh case -1 salon hoạt động như behavior cũ) | High | Regression | F4, D2, T2 |
| TC018 | Salon: câu お名前 — dropdown 「友だち情報に回答を記録」(loại liên kết) VẪN khoá → liên kết vẫn bắt buộc | Form salon, câu お名前 (必須) | 1.Click câu お名前 ở ②項目<br>2.Nhìn dropdown TRÊN 「友だち情報に回答を記録」<br>3.Thử bỏ/đổi sang không liên kết | Dropdown loại liên kết vẫn disabled, không bỏ được → câu họ tên vẫn bắt buộc liên kết; chỉ dropdown đích liên kết (DƯỚI) mở khoá | High | Regression | F2, T2 |
| TC019 | Salon Boundary: câu 短文回答 tự thêm (can_delete=1) → dropdown 連携先 VẪN enabled | Form salon, thêm câu 短文回答 tự tạo (vd 「備考」, can_delete=1) | 1.Mục ①: thêm câu 短文回答 mới<br>2.Click câu vừa thêm ở ②項目<br>3.Nhìn dropdown 連携先 | Dropdown enabled (can_delete=1 → đk khoá false); điều kiện mới chỉ siết câu mặc định | Medium | Boundary | F2, T2 |
| TC020 | Lesson: 保存 câu hỏi + reload màn お客様への質問項目 → không lỗi blade / view cache | Form lesson | 1.Chỉnh 1 câu hỏi > 保存<br>2.Reload<br>3.Console (F12) check lỗi JS/blade | 保存 OK, reload không lỗi, không vỡ layout 2 dropdown, giá trị lưu hiển thị đúng | Medium | Regression | F1, T1, CL-Func-2 |
| TC021 | Lesson: đáp án câu お名前 lưu vào friend info tự chọn hiển thị đúng ở My page / Chat 1:1 right bar; システム表示名 giữ nguyên | Friend info text 「学生氏名」 đã tạo; form lesson câu お名前 連携先 = 「学生氏名」; user システム表示名 = "山田太郎" | 1.User đặt lịch lesson nhập お名前 = "テスト花子"<br>2.Admin: My page user → tab 基本情報 xem 「学生氏名」<br>3.Chat 1:1 → right bar friend info<br>4.Xem システム表示名 ở 2 nơi | 「学生氏名」 = "テスト花子" ở cả My page lẫn right bar; システム表示名 VẪN "山田太郎" (verify qua UI, không cần DB) | High | Positive | BUG, D1, T1, C.3 |
| TC022 | Lesson: click qua lại giữa câu 短文回答 / 単一選択 / 日時 → trạng thái enable/disable dropdown 連携先 cập nhật đúng, không stale | Form lesson có đủ 3 loại câu mặc định (can_delete=0) | 1.Click câu お名前 (text) → xem dropdown<br>2.Click 単一選択 → xem<br>3.Click 日時 → xem<br>4.Click ngược lại お名前 | Dropdown enabled khi ở câu text; disabled khi ở 単一選択/日時; cập nhật ngay mỗi lần click, không giữ trạng thái câu trước. Lặp salon; check thêm Win/Mac × Chrome/Safari | Medium | Boundary | F1, T1, TC-24, CL-NonF-1 |
| TC023 | Lesson Edge: đổi 連携先 câu お名前 sang メール (id=-3) → 保存 → reload → dropdown câu đó bị khoá lại | Form lesson, câu お名前 連携先 đang mở khoá sau fix | 1.Đổi dropdown 連携先 câu お名前 sang 「メールアドレス」(-3)<br>2.保存<br>3.Reload, click lại câu お名前 | Dropdown 連携先 bị disabled lại (trùng đk id==-3). Xác nhận với Leader/Dev: hành vi này chấp nhận được (user khó đổi ngược) | Low | Negative | F1 (edge) |

---

## 6. Spec update needed

- [x] Không cần update spec — fix đã theo đúng comment chốt của KH/PM trong Redmine (liên kết câu trả lời vẫn **bắt buộc**, nhưng **đích liên kết 連携先 tự chọn**).
- [ ] Cần update spec
- ℹ️ **Ngoài scope (ghi nhận, không phải spec update)**: KH hỏi ở comment cuối về **商品販売 (bán sản phẩm)** + **イベント予約 (đặt chỗ sự kiện)** — cùng pattern khoá 連携先 nhưng **không** nằm trong fix #37640 (blade riêng, không bị chạm code). Nếu PM muốn đối ứng → mở task riêng, không gộp vào bộ TC này.

---

## 7. Checklist đã chạy

- [x] A. Coverage — 11 impact, 9 OK / 5 RISK / 0 GAP
- [x] B. Chất lượng từng TC — title rõ, expected đo lường được; trừ cách verify dẫn bằng DB (AP-5)
- [x] C. Chất lượng bộ TC tổng thể — không trùng lặp, không orphan; thiếu cột Type/Priority để soi tỷ lệ
- [x] D. Spec alignment — không mâu thuẫn (khớp comment chốt KH)
- [x] E. Hành chính — TC ID chuẩn; file 04 đúng folder; "Tester viết TCs" để placeholder
- [x] F. Base checklist LME
  - [x] F.1 Web — A.1: **TC-24/CL-Func-24** (MAJOR), CL-Func-2 (MINOR, lesson reload); A.2: Regression OK, **Compatibility** (MINOR), Security N/A (không URL mới)
  - [x] F.2 Job — B.2 CLJ01 Google sync: **không bắt buộc TC riêng** (sync code không bị chạm; view_name/friend_information_value đã verify upstream). Ghi nhận, không flag.
  - [x] F.3 Tính năng chung — **C.3 Friend info** (MAJOR, thiếu verify nơi hiển thị/update); C.5 Google sheet (downstream không chạm — note, không flag)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
