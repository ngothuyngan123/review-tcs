<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1257980776#gid=1257980776 | sheet=Task nhỏ + test fix bug kh | anchor=Main Function -->

# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
> Member copy file này (hoặc paste từ Excel/Google Sheet) vào folder review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `Ngọc Ánh` |
| Ngày submit | `2026-06-23` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1257980776#gid=1257980776 (tab "Task nhỏ + test fix bug kh", row 866~886) |

---

## TC List

> TCs fetch từ Redmine #37640 Link TCs — **read-only**, KHÔNG sửa title/expected dù fix đổi behavior. Cột Type/Priority sheet gốc không có → để trống. Các dòng "change 連携先 = ..." (merged-cell trong sheet) đã gộp vào Precondition của TC cha. Status giữ nguyên giá trị sheet.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | [Lesson – お客様への質問項目] Câu 「お名前を入力してください」(短文回答): dropdown 連携先「回答を記録する友だち情報を選択してください」MỞ KHOÁ | | | Form lesson; câu お名前 mặc định (必須), 連携先 = 基本情報(システム表示名).<br>Lặp với 連携先 = 基本情報_mail / 基本情報_số điện thoại / 国内住所 / type tự tạo | 1.Vào 予約画面>お客様への質問項目 form lesson<br>2.②項目: click câu 「お名前を入力してください」<br>3.③編集: nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 (đang = システム表示名) enabled, mở chọn được friend info khác. Trước fix: xám/disabled<br>Update đúng trường data đã chọn | | | OK |
| TC002 | [Salon – お客様への質問項目] Câu 「お名前を入力してください」(短文回答): dropdown 連携先 MỞ KHOÁ (salon) | | | Form salon; câu お名前 mặc định (必須), 連携先 = システム表示名.<br>Lặp với 連携先 = 基本情報_mail / 基本情報_số điện thoại / 国内住所 / type tự tạo | 1.Vào 予約画面>お客様への質問項目 form salon<br>2.Click câu 「お名前を入力してください」ở ②項目<br>3.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 (đang = システム表示名) enabled, mở chọn được friend info khác. Trước fix: xám/disabled<br>Update đúng trường data đã chọn | | | OK |
| TC003 | [Lesson – お客様への質問項目] Regression: câu 「メールアドレスを入力…」(連携先=メールアドレス, id=-3) dropdown 連携先 VẪN KHOÁ | | | Form lesson; câu メール mặc định (必須), 連携先 = メールアドレス | 1.Vào お客様への質問項目 form lesson<br>2.Click câu 「メールアドレスを入力…」ở ②項目<br>3.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 vẫn disabled (xám), giữ = メールアドレス, không đổi được (đúng đk id==-3) | | | OK |
| TC004 | [Salon – お客様への質問項目] Regression: câu 「メールアドレスを入力…」(id=-3) dropdown 連携先 VẪN KHOÁ (salon) | | | Form salon; câu メール mặc định (必須), 連携先 = メールアドレス | 1.Vào お客様への質問項目 form salon<br>2.Click câu メールアドレス<br>3.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 vẫn disabled | | | OK |
| TC005 | [Lesson – お客様への質問項目] Regression: câu お名前, dropdown 「友だち情報に回答を記録」(loại liên kết) VẪN KHOÁ → vẫn bắt buộc liên kết | | | Form lesson; câu 「お名前を入力してください」(必須) | 1.Click câu お名前 ở ②項目<br>2.③編集: nhìn dropdown TRÊN 「友だち情報に回答を記録」(すでに作成済みの友だち情報に回答を記録)<br>3.Thử đổi/bỏ | Dropdown 「友だち情報に回答を記録」vẫn disabled, không bỏ liên kết được. Chỉ dropdown DƯỚI 「回答を記録する友だち情報を選択してください」mới mở khoá | | | OK |
| TC006 | [Lesson – お客様への質問項目] Regression: câu 単一選択 — dropdown 連携先 GIỮ NGUYÊN behavior cũ (khoá theo can_delete=0) | | | Form lesson có câu mặc định loại 単一選択 (can_delete=0) nếu có | 1.Click 1 câu loại 単一選択 ở ②項目<br>2.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 câu 単一選択 giữ behavior cũ (khoá khi can_delete=0), không bị fix khối 短文回答 làm đổi | | | OK |
| TC007 | [Lesson – お客様への質問項目] Regression: câu 日時 (datetime) — dropdown 連携先 GIỮ NGUYÊN | | | Form lesson có câu loại 日時 (can_delete=0) nếu có | 1.Click 1 câu loại 日時 ở ②項目<br>2.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 câu 日時 giữ behavior cũ (khoá theo !can_delete) | | | OK |
| TC008 | [Lesson – E2E booking] Đổi 連携先 câu お名前 từ システム表示名 → friend info tự tạo → khách đặt lịch → lưu friend_information_value, KHÔNG ghi đè view_name | | | Friend info 記述/短文 「学生氏名」 sẵn; user LINE bạn bè bot, view_name(システム表示名)="山田太郎" | 1.お客様への質問項目 form lesson: câu お名前 → dropdown 「回答を記録する友だち情報を選択してください」đổi sang 「学生氏名」 >保存<br>2.Reload xác nhận 連携先=「学生氏名」<br>3.User LINE đặt lịch nhập お名前="テスト花子"<br>4.Check DB | friend_information_value(「学生氏名」)="テスト花子"; line_users.view_name VẪN "山田太郎" (không ghi đè) — đúng mục tiêu #37640 | | | OK |
| TC009 | [Lesson – E2E booking] Regression: giữ 連携先 câu お名前 = システム表示名 → đặt lịch → view_name update (case -1) | | | Form lesson câu お名前 連携先=システム表示名(-1); user view_name cũ="山田太郎" | 1.Giữ 連携先 câu お名前 = システム表示名<br>2.User LINE đặt lịch lesson nhập お名前="新しい名前"<br>3.Check view_name | line_users.view_name="新しい名前" (case -1 → view_name, behavior cũ giữ nguyên) | | | OK |
| TC010 | [Salon – E2E booking] Đổi 連携先 câu お名前 → friend info → khách đặt lịch → lưu friend_information_value, không ghi đè view_name (salon) | | | Friend info 「学生氏名」 sẵn; user view_name="山田太郎" | 1.お客様への質問項目 form salon: câu お名前 → dropdown 「回答を記録する友だち情報を選択してください」đổi sang 「学生氏名」 >保存<br>2.User đặt lịch salon nhập お名前="サロン花子"<br>3.Check DB | friend_information_value="サロン花子"; view_name VẪN "山田太郎" | | | OK |
| TC013 | [Lesson+Salon – Data cũ] Boundary: form lưu TRƯỚC fix → sau fix load お客様への質問項目 hiển thị đúng 連携先, không reset | | | Có form lesson+salon đã lưu câu お名前 (連携先=システム表示名) trước deploy fix | 1.Sau deploy, vào お客様への質問項目 form lesson (data cũ)<br>2.Click câu お名前, xem 連携先 + trạng thái enable<br>3.Lặp salon | 連携先 câu お名前 vẫn=システム表示名 (không reset/null); dropdown enabled nhưng giá trị đang chọn không đổi; save lại không đổi data | | | OK |
| TC014 | [Salon – お客様への質問項目] Regression: 保存 câu hỏi + reload màn お客様への質問項目 → không lỗi blade/view cache | | | Form salon | 1.Vào お客様への質問項目 form salon, chỉnh 1 câu hỏi >保存<br>2.Reload<br>3.Mở Console check lỗi JS/blade | 保存 OK, reload không lỗi (không blade error, không vỡ layout 2 dropdown 連携). Lưu ý clear view cache khi deploy | | | OK |
| TC016 | [Lesson – お客様への質問項目] Boundary: câu 短文回答 tự thêm (can_delete=1, vd câu liên kết 携帯電話 như 「test」) → dropdown 連携先 VẪN enabled | | | Form lesson, thêm 1 câu 短文回答 tự tạo (can_delete=1) — vd câu liên kết 携帯電話 như câu 「test」 trong UI | 1.Mục ①: click 短文回答 thêm câu mới (vd 「備考」)<br>2.Click câu vừa thêm ở ②項目<br>3.Nhìn dropdown 「回答を記録する友だち情報を選択してください」 | Dropdown 連携先 câu tự tạo enabled (can_delete=1 → đk khoá false), như trước fix; đk mới chỉ siết câu mặc định | | | OK |

### Chú thích cột

- **Type**: `Positive` / `Negative` / `Boundary` / `Regression` (sheet gốc không tách cột Type — Leader/member tự gán khi review).
- **Priority**: `High` / `Medium` / `Low` (sheet gốc không có — để trống).
- **Output note** / **Assignee** / **Status**: Status giữ nguyên từ sheet (`OK`). Output note / Assignee để trống.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). TC E2E booking (TC008~TC010) cần user LINE là bạn bè bot + check DB → ưu tiên Staging/Dev.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

<!-- Source: fetched từ Redmine #37640 Link TCs, range A866:J886 tab "Task nhỏ + test fix bug kh" lúc 2026-06-25. KHÔNG sửa TCs này nếu chưa confirm với Leader. Sheet gốc có gap TC011/TC012/TC015 (đã bị xoá/gộp trong sheet) — giữ nguyên đánh số. -->
