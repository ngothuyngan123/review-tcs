<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1257980776#gid=1257980776 | sheet=Task nhỏ + test fix bug kh | anchor=Main Function -->

# 04 — TC List (DELTA — do /write-tc sinh)

> ⚠️ **Đây là file DRAFT chứa CHỈ TC delta** (impact/checklist mà 13 TC cũ trong `04-tc-list.md` CHƯA cover). KHÔNG đè TC cũ.
> Member đọc lại từng TC → merge các TC delta phù hợp vào `04-tc-list.md` rồi mới `/sync-ai-tc`.
>
> **TC cũ là read-only** — /write-tc KHÔNG sửa, KHÔNG override. Delta đánh số tiếp TC017+ (sheet cũ tới TC016).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | `v1 (delta /write-tc 2026-06-25)` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1257980776#gid=1257980776 (tab "Task nhỏ + test fix bug kh") |

---

## TC List (delta)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC017 | [Salon – E2E booking] Regression: giữ 連携先 câu お名前 = システム表示名 → khách đặt lịch salon → システム表示名 cập nhật theo đáp án (case -1) | Regression | High | Form salon; câu お名前 連携先 = システム表示名 (mặc định -1); user LINE là bạn bè bot, システム表示名 hiện = "山田太郎" | 1.お客様への質問項目 form salon: giữ nguyên 連携先 câu お名前 = システム表示名<br>2.User LINE đặt lịch salon, nhập お名前 = "新しい名前"<br>3.Mở Chat 1:1 của user đó (hoặc My page) xem システム表示名 | システム表示名 của user đổi thành "新しい名前" (case -1 ghi đè như behavior cũ — salon không bị fix làm hỏng nhánh giữ システム表示名) | | | |
| TC018 | [Salon – お客様への質問項目] Regression: câu お名前 — dropdown TRÊN 「友だち情報に回答を記録」(loại liên kết) VẪN KHOÁ → liên kết vẫn bắt buộc (salon) | Regression | High | Form salon; câu 「お名前を入力してください」(必須, mặc định) | 1.Vào お客様への質問項目 form salon<br>2.Click câu お名前 ở ②項目<br>3.③編集: nhìn dropdown TRÊN 「友だち情報に回答を記録」(loại liên kết) → thử bỏ/đổi sang "không liên kết" | Dropdown 「友だち情報に回答を記録」vẫn disabled, KHÔNG bỏ được liên kết → câu họ tên vẫn bắt buộc liên kết. Chỉ dropdown DƯỚI 「回答を記録する友だち情報を選択してください」(đích liên kết) mới mở khoá | | | |
| TC019 | [Salon – お客様への質問項目] Boundary: câu 短文回答 tự thêm (can_delete=1) → dropdown 連携先 VẪN enabled (salon) | Boundary | Medium | Form salon; thêm 1 câu 短文回答 tự tạo (vd 「備考」, can_delete=1) | 1.Mục ①: click 短文回答 thêm câu mới (vd 「備考」)<br>2.Click câu vừa thêm ở ②項目<br>3.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 câu tự tạo enabled (can_delete=1 → đk khoá false) — như trước fix; điều kiện mới chỉ siết câu mặc định, không ảnh hưởng câu tự thêm | | | |
| TC020 | [Lesson – お客様への質問項目] Regression: 保存 câu hỏi + reload màn お客様への質問項目 → không lỗi blade / view cache (CL-Func-2) | Regression | Medium | Form lesson | 1.Vào お客様への質問項目 form lesson, chỉnh 1 câu hỏi (vd đổi 連携先 câu お名前) > 保存<br>2.Reload trang<br>3.Mở Console (F12) check lỗi JS / blade | 保存 OK, reload không lỗi: không blade error, không vỡ layout 2 dropdown 連携, giá trị vừa lưu hiển thị đúng. (Lưu ý clear view cache khi deploy — đối xứng TC014 cho lesson) | | | |
| TC021 | [Lesson – Friend info display] Đáp án câu お名前 lưu vào friend info tự chọn hiển thị đúng ở My page / Chat 1:1 right bar; システム表示名 giữ nguyên (C.3) | Positive | High | Friend info text 「学生氏名」 đã tạo; form lesson câu お名前 連携先 = 「学生氏名」; user LINE bạn bè bot, システム表示名 = "山田太郎" | 1.User LINE đặt lịch lesson, nhập お名前 = "テスト花子"<br>2.Admin web: mở My page của user → tab 基本情報, xem field 「学生氏名」<br>3.Mở Chat 1:1 của user → right bar friend info<br>4.Xem システム表示名 ở 2 nơi trên | Field 「学生氏名」 = "テスト花子" (đáp án mới) ở cả My page lẫn Chat 1:1 right bar; システム表示名 VẪN "山田太郎" (không bị ghi đè) — đúng nhu cầu KH quản lý tên học sinh ở システム表示名 | Quan sát qua UI (My page + right bar), không cần check DB | | |
| TC022 | [Lesson – お客様への質問項目] Boundary: click qua lại giữa câu 短文回答 / 単一選択 / 日時 trong cùng màn → trạng thái enable/disable dropdown 連携先 cập nhật đúng từng loại, không stale (TC-24 / CL-Func-3) | Boundary | Medium | Form lesson có đủ 3 loại câu mặc định: お名前 (短文回答), 1 câu 単一選択, 1 câu 日時 (đều can_delete=0) | 1.Click câu お名前 (短文回答) → xem dropdown 連携先<br>2.Click sang câu 単一選択 → xem dropdown 連携先<br>3.Click sang câu 日時 → xem dropdown 連携先<br>4.Click ngược lại câu お名前 | Dropdown 連携先: enabled khi đang ở câu 短文回答(お名前); disabled khi ở câu 単一選択 và 日時 (giữ behavior cũ). Trạng thái cập nhật ngay mỗi lần click, KHÔNG giữ trạng thái câu trước (không stale do component dùng chung) | Lặp tương tự form salon. CL-NonF-1: verify thêm trên Win+Mac × Chrome+Safari (đây là thay đổi hành vi JS/blade của dropdown dùng chung) | | |
| TC023 | [Lesson – お客様への質問項目] Negative/Edge: đổi 連携先 câu お名前 sang メールアドレス (id=-3) → 保存 → reload → dropdown câu đó bị KHOÁ lại | Negative | Low | Form lesson; câu お名前 連携先 đang mở khoá sau fix | 1.Click câu お名前, đổi dropdown 連携先 sang 「メールアドレス」(basic info id=-3)<br>2.保存<br>3.Reload, click lại câu お名前, xem dropdown 連携先 | Sau reload dropdown 連携先 câu お名前 bị disabled lại (vì giờ id==-3 trùng điều kiện khoá câu email). Hành vi vô hại nhưng cần ghi nhận: user khó tự đổi ngược lại từ メールアドレス sang friend info khác → xác nhận đây có phải behavior chấp nhận được không (hỏi Leader/Dev) | Edge Dev tự nêu trong file 03 — verify để khẳng định "không gây hại" | | |

### Chú thích

- **Type / Priority**: đã gán theo phân tích impact. Member chỉnh nếu cần.
- **Output note / Assignee / Status**: để trống — QA fill sau khi run.
- TC delta đánh số TC017+ để nối tiếp 13 TC cũ (sheet tới TC016, bỏ trống TC011/012/015).

### Environment (note)

Mặc định **Staging** (`staging.lme.jp`). TC E2E (TC017, TC021) cần user LINE là bạn bè bot. TC022 phần Compatibility (CL-NonF-1) cần thêm Mac/Safari.

---

## Member tự check trước khi submit

### Coverage check (delta)
- [x] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (chưa có file 02 — tham chiếu `templates/LME-SYSTEM-SPEC.md`, member bổ sung sau nếu cần)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] **Mỗi impact** F/D/T có ≥ 1 TC verify (kết hợp TC cũ + delta — xem mapping ở summary)
- [x] Có ≥ 1 TC verify trực tiếp bug fix (TC008 cũ + TC021 delta UI)
- [x] Có ≥ 1 TC regression cho mỗi tính năng T (lesson: TC009/TC020; salon: TC017)
- [x] Title TC chứa keyword giúp Leader map impact

### Base checklist LME (mục liên quan task này)

**§A Checklist web**:
- [x] A.1 — **CL-Func-24 / TC-24** (UI component dropdown — hành vi tap/đổi qua lại) → TC022
- [x] A.1 — **CL-Func-3** (chuyển câu/tab setting, data không stale) → TC022
- [x] A.1 — **CL-Func-2** (sau save/reload không lỗi) → TC020 (+ TC014 cũ salon)
- [x] A.2 — **Regression** (CL-NonF-11→6): data cũ + nhánh case -1 → TC013 cũ, TC009 cũ, TC017
- [x] A.2 — **Compatibility** (CL-NonF-1): UI dropdown đổi hành vi → note ở TC022 (Win/Mac × Chrome/Safari)
- [ ] A.2 — Security (CL-NonF-5→2): **không áp dụng** (không có màn/URL mới)

**§C Tính năng chung**:
- [x] **C.3 Friend info** — nơi update (Lesson/Salon booking) + nơi hiển thị (My page, Chat 1:1 right bar) → TC021
- [ ] **C.5 Google sheet** — sync システム表示名 sang spread: **không sinh TC riêng** (job sync KHÔNG bị chạm code; giá trị view_name/friend_information_value đã verify ở TC009/TC017/TC021 — downstream phản ánh nguyên trạng). Member smoke nếu Leader yêu cầu.

<!-- DELTA generated by /write-tc 2026-06-25 từ 01-bug-task.md + 03-dev-impact.md + 13 TC cũ (read-only). Không override TC cũ. -->
