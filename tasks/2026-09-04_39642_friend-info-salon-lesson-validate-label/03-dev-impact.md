# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39642 — journal `#129200` của **AI LME Fix bug** lúc `2026-08-18T08:08:28Z`
> (report tự động của hệ thống Auto-fixbug LME). Description của ticket KHÔNG chứa đánh giá ảnh hưởng.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | **AI LME Fix bug** (hệ thống Auto-fixbug LME) — không phải dev người. Assignee Redmine hiện tại: Kim Cúc |
| Commit / Pull Request | `<không có link PR>` — commit `2faaa0caaf` (theo journal Redmine, 4 file). ⚠️ Studio task #111 lại tham chiếu `COMMIT-6356ec93a4` — **2 mã commit khác nhau, cần Leader xác nhận bản nào đang nằm trên môi trường test** |
| Branch | `ai_fixbug_39642` (repo `sns-line`, nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-18` |
| Auto-filled | `2026-09-04 by /new-task` |

**Link theo dõi (từ journal):**
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39642
- Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=5ed59dca-4844-4249-b02d-3362e6cfe3a6
- Thời gian AI xử lý: 9 phút 40 giây

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" của journal Redmine -->

Màn tạo mục trả lời của Biểu mẫu đã có validate chặn nhập trùng tên hiển thị lựa chọn (fix gốc, thông báo 選択肢の表示名が重複しています), nhưng 3 màn tương tự chưa có: Quản lý thông tin bạn bè (loại Lựa chọn / Điểm), Đặt lịch salon và Đặt lịch bài học. Người dùng nhập 2 lựa chọn trùng nhau vẫn lưu được, gây nhầm lẫn cho khách khi trả lời và ghi sai dữ liệu vào thông tin bạn bè.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" của journal Redmine -->

Triển khai ngang validate chặn trùng lựa chọn sang 3 màn còn thiếu, dùng đúng thông báo ticket yêu cầu. (1) Quản lý thông tin bạn bè: thêm kiểm tra trùng giá trị các dòng lựa chọn/mốc điểm ngay trước khi lưu, chỉ áp cho loại Lựa chọn và Điểm, báo lỗi '選択肢が重複しています。異なる値を入力してください。'. (2) Salon và (3) Bài học: thêm kiểm tra trùng tên hiển thị lựa chọn vào đúng hàm lưu mục nhập đã có sẵn validate ô trống, chặn cả nhóm lựa chọn tự nhập và nhóm lựa chọn hiển thị khi liên kết thông tin bạn bè, báo lỗi '選択肢の表示名が重複しています。異なる値を入力してください。' và không gọi API lưu. Cả 3 chỗ đều bỏ qua ô đang trống (đã có validate bắt buộc nhập riêng) và so sánh sau khi trim. Bump version asset để trình duyệt nạp JS mới. Phần Biểu mẫu (Radio/Droplist/Checkbox/Remind/Chẩn đoán/Giới tính) đã có sẵn fix gốc — đã kiểm từng loại, không cần sửa thêm.

> ⚠️ **Mâu thuẫn cần Leader chốt**: câu "Bump version asset để trình duyệt nạp JS mới" ở đây **mâu thuẫn** với `REQ-014` trên Studio task #111, vốn ghi *"commit fix KHÔNG bump phiên bản asset (nhánh fix để 202608062210, base để 202608191616)"*. Đây là điểm rủi ro deploy — xem thêm TC `NEW-44` đang ở trạng thái `skip` trong file 04.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN", convert sang bảng template -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `hasDuplicateSettingActionValue` — `public/js/infor_friend/create.js` | **Thêm mới** | Hàm kiểm tra trùng giá trị dòng lựa chọn / mốc điểm |
| 2 | `saveInforFriend` — `public/js/infor_friend/create.js` | Chèn guard chặn trùng | Hàm lưu duy nhất của màn → phủ cả luồng tạo mới, sửa và copy |
| 3 | `hasDuplicateOptionTitle` — `public/js/calendar_salon/calendar_detail.js` | **Thêm mới** | Kiểm tra trùng tên hiển thị lựa chọn (Salon) |
| 4 | `showDuplicateOptionTitleAlert` — `public/js/calendar_salon/calendar_detail.js` | **Thêm mới** | Hiển thị thông báo lỗi (Salon) |
| 5 | `updateFormQuestion` — `public/js/calendar_salon/calendar_detail.js` | Chèn guard chặn trùng | Hàm lưu mục nhập duy nhất → phủ nhập tay `@blur`, kéo sắp xếp, đổi liên kết friend info |
| 6 | `hasDuplicateOptionTitle` — `public/js/calendar_management/calendar_detail.js` | **Thêm mới** | Kiểm tra trùng tên hiển thị lựa chọn (Lesson) |
| 7 | `showDuplicateOptionTitleAlert` — `public/js/calendar_management/calendar_detail.js` | **Thêm mới** | Hiển thị thông báo lỗi (Lesson) |
| 8 | `updateFormQuestion` — `public/js/calendar_management/calendar_detail.js` | Chèn guard chặn trùng | Như #5, cho màn Lesson |
| 9 | `hasDuplicateLabels` + `validateItemForm` — `public/js/form_answer/v3/setting_form_items.js` | **KHÔNG sửa** — chỉ đọc để đối chiếu | Fix **GỐC** đã có sẵn ở màn Biểu mẫu |

**Đã kiểm và loại trừ (theo mục TỰ REVIEW của AI):** các màn `friend_information` khác — `setting_add_friend`, `chat`, `qr_code`, `calendar_*` — chỉ **chọn** thông tin bạn bè, không tạo/sửa danh sách lựa chọn.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Redmine mục 4.1 gốc là "File thay đổi" (4 file). Bảng dưới ghép file + function từ mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveInforFriend` + `hasDuplicateSettingActionValue` | `public/js/infor_friend/create.js` | Direct | Chỉ áp cho loại 「選択肢」 và 「ポイント」 |
| F2 | `updateFormQuestion` + `hasDuplicateOptionTitle` + `showDuplicateOptionTitleAlert` | `public/js/calendar_salon/calendar_detail.js` | Direct | Chặn cả nhóm lựa chọn tự nhập lẫn nhóm 「表示される選択肢」 |
| F3 | `updateFormQuestion` + `hasDuplicateOptionTitle` + `showDuplicateOptionTitleAlert` | `public/js/calendar_management/calendar_detail.js` | Direct | Logic nhân bản từ F2 sang màn Lesson |
| F4 | Cấu hình version asset | `config/sns-line.php` | Direct | Bump version để browser nạp JS mới — ⚠️ Studio REQ-014 phản bác điểm này |
| F5 | `hasDuplicateLabels` + `validateItemForm` (fix gốc Biểu mẫu) | `public/js/form_answer/v3/setting_form_items.js` | Indirect (KHÔNG sửa code) | Vùng **regression** — chỉ verify không hỏng |

**Tổng diff (theo mục VERIFY của journal):** `git diff --stat release_step_20260805...ai_fixbug_39642` → **4 file, +78/−1**.

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2: "Không có — chỉ thêm validate phía giao diện, không đổi schema, không ghi/sửa dữ liệu đã lưu" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Dev khẳng định: chỉ thêm validate phía giao diện, **không đổi schema, không ghi/sửa dữ liệu đã lưu** |

> ⚠️ Hệ quả cho TC: **dữ liệu cũ đang trùng lựa chọn KHÔNG được migrate** → bản ghi cũ vẫn còn trùng trong DB, chỉ bị chặn khi lưu lại. Xem mục "Rủi ro khi test" bên dưới.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3, giữ nguyên mã FA-xxx do Dev ghi -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Information (FA-015)** — chặn lưu khi 2 dòng lựa chọn hoặc mốc điểm trùng nhau | F1 | High |
| T2 | **Salon Booking (FA-020)** — chặn lưu mục nhập khi trùng tên hiển thị lựa chọn (đơn/nhiều/dropdown) | F2 | High |
| T3 | **Lesson / Calendar Booking (FA-019)** — chặn lưu mục nhập khi trùng tên hiển thị lựa chọn (đơn/nhiều/dropdown) | F3 | High |
| T4 | **Form Builder (FA-011)** — fix gốc đã có, chỉ đối chiếu để triển khai nhất quán, **không sửa code** | F5 | Medium (regression thuần) |
| T5 | **Toàn bộ màn dùng asset JS** — nếu `config/sns-line.php` đổi version | F4 | Medium — browser cache / deploy |

---

## 5. Recover data (mục "■ 5. RECOVER DATA" của journal)

✔ **Không cần recover data.**

## 6. Verify của Dev (mục "■ 6. VERIFY" của journal)

- **Mức:** `lint` (KHÔNG có unit test / integration test)
- **Lệnh đã chạy:**
  - `php -l config/sns-line.php` → No syntax errors detected
  - `node --check public/js/infor_friend/create.js` → OK
  - `node --check public/js/calendar_salon/calendar_detail.js` → OK
  - `node --check public/js/calendar_management/calendar_detail.js` → OK
  - `git diff --stat release_step_20260805...ai_fixbug_39642` → 4 file, +78/−1 — đúng phạm vi
- **Bằng chứng Dev đưa ra:**
  - Fix gốc xác định tại `public/js/form_answer/v3/setting_form_items.js:2423` (`hasDuplicateLabels`) + `:2466` (alert trong `validateItemForm`), commit `e7a6a9d81a` / `1a82cf8735` "fix bug form".
  - Không cần check DB: thuần validate giao diện, không phụ thuộc dữ liệu runtime.
  - Đã đối chiếu **6 loại item của Biểu mẫu** ticket liệt kê: Radio + Droplist (`radio.blade.php`, `typeoption radio|select`) / Checkbox (`checkbox.blade.php`) / Giới tính (`gender.blade.php`) / Remind (`remind.blade.php`) đều bind `selectable.items[].label` ⇒ đã được fix gốc bao. Chẩn đoán (`diagnostic.blade.php`) bind `.value` nhưng `updateValueDiagnostic` (`setting_form_items.js:2832`) và `changeListFriendInforDiagnostic` (`:2199`) đều đồng bộ `label = value` ⇒ cũng đã được bao. **Kết luận: phần Biểu mẫu KHÔNG cần sửa.**
  - Salon/Lesson **không có loại item Droplist riêng**: Radio và Droplist là cùng `form_type SETTING_FORM_RADIO(3)`, khác nhau ở `display_method` `1=ラジオボタン` / `2=ドロップダウン` (`setting_form.blade.php:567-620` salon) ⇒ **một guard bao cả hai**.

## 7. Tự review của AI + rủi ro khi test (nguyên văn journal)

Đã áp dụng nhất quán cách sửa của fix gốc (so sánh danh sách sau khi trim, bỏ qua ô trống, chặn ngay trước khi lưu, thông báo tiếng Nhật đúng như ticket khai) sang cả 3 chỗ còn thiếu. Với Salon/Lesson, guard được đặt trong đúng hàm lưu duy nhất (`updateFormQuestion`) nên phủ mọi đường vào: nhập tay từng ô (`@blur`), kéo sắp xếp lại lựa chọn, và đổi liên kết thông tin bạn bè. Với Thông tin bạn bè, guard đặt trong `saveInforFriend` trước khi `validateAll` nên chặn được cả luồng tạo mới, sửa và copy (cùng một màn / một hàm lưu).

**Rủi ro / lưu ý khi test — Dev nêu 4 điểm (đây là input trực tiếp cho TC):**

1. **Dữ liệu cũ đang trùng lựa chọn**: khách mở lại màn Salon/Lesson và **chỉ click vào ô lựa chọn rồi click ra là đã dính alert**, phải sửa cho hết trùng mới lưu tiếp được. Đây là hệ quả tất yếu của yêu cầu và giống hệt hành vi validate ô trống đã có sẵn.
2. **Validate CHỈ ở phía giao diện**, giống fix gốc — **gọi API trực tiếp vẫn lưu được trùng**. Không thêm chặn phía server để giữ đúng phạm vi fix gốc; nếu muốn chặt hơn thì nên mở ticket riêng cho cả 4 màn (kể cả Biểu mẫu).
3. **Nhóm 「表示される選択肢」 khi liên kết thông tin bạn bè** đã có (`options_information_friend`) trước đây không có validate nào; **nay bị chặn trùng**. AI quyết định BAO vì đó cũng là tên hiển thị do người dùng tự nhập của cùng item Lựa chọn. Nếu PM muốn thu hẹp thì bỏ đúng 1 block `if`.
4. **Loại Điểm** của thông tin bạn bè so sánh **dạng chuỗi sau trim**, nên `'5'` và `'05'` vẫn coi là **khác nhau**. Ô nhập là `type=number` nên thực tế trình duyệt đã tự chuẩn hoá; không xử lý thêm để tránh phình fix.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Chốt mâu thuẫn bump asset version**: journal nói "đã bump", Studio `REQ-014` nói "KHÔNG bump" (xem mục 2)
- [ ] **Chốt commit nào đang trên môi trường test**: `2faaa0caaf` (Redmine) vs `6356ec93a4` (Studio)
