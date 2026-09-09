# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #38428 bởi `/new-task`. Nguồn: journal **#124657 — "AI LME Fix bug", 2026-07-02T11:20:18Z** (bản **mới nhất**, đầy đủ nhất).
>
> ⚠️ **Đánh giá do AI Auto-fixbug sinh, KHÔNG phải Dev người viết.** Ticket có **3 bản** báo cáo auto-fixbug (10:21 / 11:15 / 11:20 cùng ngày) — nội dung KHÁC nhau, xem mục "Cảnh báo input" bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — Redmine `assigned_to` hiện tại = `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | `sns-line` commit `aebc144d44` (1 file) — **không có link PR GitHub/GitLab**. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38428 |
| Branch | `ai_fixbug_38428` (nhánh gốc `release_step_20260623`) — đã push lên origin |
| Ngày submit đánh giá | `2026-07-02` (journal #124657, 11:20:18Z) |
| Auto-filled | `2026-08-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## ⚠️ Cảnh báo input (do `/new-task` phát hiện, KHÔNG phải nội dung Dev)

1. **3 bản đánh giá mâu thuẫn nhau về `FormAnswerService::renderFormAnswer`.**
   - Bản #124641 (10:21) — mục 2 ghi: *"Bỏ guard null ở renderForm (thừa sau khi fix gốc)"*, mục 3 ghi renderFormAnswer *"thêm guard"*.
   - Bản #124657 (11:20, dùng cho file này) — mục 3 ghi renderFormAnswer *"điểm crash gốc, **không sửa**"*.
   -> **Tester phải xác nhận với Dev**: `FormAnswerService.php:171` cuối cùng CÓ hay KHÔNG có guard null? Câu trả lời đổi hoàn toàn kết quả mong đợi của TC mở form có trang lệch `bot_id` (500 crash vs 404 / trang trống).
2. **Mục 4.1 của báo cáo AI là "File thay đổi", KHÔNG phải "List function bị ảnh hưởng"** như template. Bảng 4.1 bên dưới được `/new-task` dựng từ mục 3 + 4.1 — tester verify lại, đặc biệt các function chỉ được nhắc "không sửa".
3. **Bản #124641 có nhắc `FormAnswerController@8045/8094` (delete page lọc `getBotId`) — "hệ quả cùng gốc, không sửa"; bản #124657 ĐÃ BỎ dòng này.** Đây là caller còn tồn tại rủi ro nhưng không được cover ở bản mới nhất.
4. **Mức VERIFY của Dev chỉ là `lint`** (`php -l`) — không có unit test / integration test. Toàn bộ gánh nặng verify dồn sang QA.
5. **Data cũ KHÔNG tự sửa** — bắt buộc chạy query recover (mục 5). Số dòng lệch trên **production chưa được xác nhận** (dev: 6).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "1. NGUYEN NHAN" — journal #124657. -->

Khi lưu biểu mẫu (saveV3), lúc CẬP NHẬT trang của form, hệ thống gán bot_id của trang bằng bot đang mở của phiên hiện tại (getBotId) thay vì bot sở hữu form. Nếu phiên đang ở bot khác / không xác định được bot (getBotId=0), bot_id của trang bị ghi đè sang bot sai/0, lệch với bot của form. Khi người dùng hoặc bot preview LINE mở form, màn render lọc trang theo đúng bot sở hữu nên không tìm thấy trang (null), lấy id của trang null gây lỗi 'Trying to get property id of non-object' tại FormAnswerService dòng 171 (36 lần). Xác nhận DB: 6 form có trang page_number=1 nhưng bot_id=0 khác bot form.

## 2. Cách fix

<!-- Nguyên văn mục "2. CACH FIX" — journal #124657. -->

Sửa FormAnswerController::saveV3 (1 file), 2 phần: (1) CHẶN GỐC — bot_id/form_id là field định danh của trang, chỉ set khi TẠO trang mới; nhánh UPDATE không đưa vào payload nên update không thể ghi đè bot_id trang sang bot session. (2) CHẶN THAO TÁC SAI — đầu saveV3: nếu bot đang mở khác bot sở hữu form thì rollback + trả JSON lỗi có msg (HTTP 500) để FE (.fail) hiển thị thông báo, yêu cầu user tải lại trang rồi thao tác lại (không redirect vì đây là AJAX). Data cũ 6 form bot_id lệch cần chạy recover 1 lần (query ở mục recover).

> **Bản cũ #124641 (10:21) mô tả cách fix KHÁC** — nguyên văn để đối chiếu:
>
> Sửa FormAnswerController::saveV3: bot_id và form_id là field định danh của trang → CHỈ set khi TẠO trang mới; nhánh UPDATE không đưa 2 field này vào payload nên update không thể ghi đè bot_id sang bot session (getBotId) như trước, chặn tận gốc việc trang bị lệch bot làm renderForm crash non-object. Bỏ guard null ở renderForm (thừa sau khi fix gốc). Data cũ 6 form bot_id lệch cần chạy recover 1 lần.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "3. DA CHECK FUNCTION / DATA LIEN QUAN" — journal #124657. -->

```
FormAnswerController::saveV3 (app/Http/Controllers/Basic/FormAnswerController.php:1274-1400 — ĐÃ SỬA: chặn lưu chéo bot + chỉ set bot_id/form_id khi CREATE trang)
FormAnswerService::renderFormAnswer (app/Services/FormAnswer/FormAnswerService.php:171 — điểm crash gốc, không sửa)
setting_form_items.js (.done/.fail của save-v3 — dùng cơ chế alert msg sẵn có, không đụng)
```

Chuyển sang bảng template:

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerController::saveV3` — `app/Http/Controllers/Basic/FormAnswerController.php:1274-1400` | **ĐÃ SỬA** | Chặn lưu chéo bot + chỉ set `bot_id`/`form_id` khi CREATE trang |
| 2 | `FormAnswerService::renderFormAnswer` — `app/Services/FormAnswer/FormAnswerService.php:171` | **Không sửa** (theo bản #124657) — ⚠️ bản #124641 nói *"thêm guard"* / *"bỏ guard"*, mâu thuẫn | Điểm crash gốc |
| 3 | `setting_form_items.js` (`.done`/`.fail` của `save-v3`) | Không đụng | Dùng cơ chế alert `msg` sẵn có |
| 4 | ⚠️ `FormAnswerController::store` (dòng 811 — `new FormAnswerPage`) | Không đụng | *Chỉ ở bản #124641*: "chỉ dựng object hiển thị, không ghi DB" |
| 5 | ⚠️ `FormAnswerController@8045/8094` (delete page lọc `getBotId`) | Không sửa | *Chỉ ở bản #124641*: "hệ quả cùng gốc" — **bản mới nhất đã bỏ, rủi ro chưa được đánh giá lại** |

---

## 4. Đánh giá ảnh hưởng

<!-- Nguyên văn mục "4. DANH GIA ANH HUONG" — journal #124657. -->

```
• 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FormAnswerController.php
 • 4.2 Data ảnh hưởng:
   - form_answer_page.bot_id — khi UPDATE trang KHÔNG còn bị ghi đè sang bot session (getBotId); chặn phát sinh lệch mới
   - Dữ liệu cũ KHÔNG tự sửa: 6 form đang lệch bot_id (trang bot_id=0 != bot form) cần chạy recover 1 lần: UPDATE form_answer_page fp JOIN form_answer fa ON fp.form_id=fa.id SET fp.bot_id=fa.bot_id WHERE fp.bot_id<>fa.bot_id;
   - Không thêm/xoá cột, không đổi schema, không đụng bảng khác
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) — lưu biểu mẫu giữ đúng bot sở hữu của trang, tránh tạo trang mồ côi khiến màn trả lời biểu mẫu công khai crash non-object (FormAnswerService:171); thao tác nhầm ở bot khác thì báo lỗi rõ + KHÔNG lưu (tránh làm hỏng form)
```

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev chỉ ghi **file thay đổi** (`app/Http/Controllers/Basic/FormAnswerController.php`), không liệt kê function theo format `F1/F2`. Bảng dưới do `/new-task` dựng lại từ mục 3 + 4.1 — **tester verify với Dev**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerController::saveV3` (endpoint `POST /form-answer/save-v3/{id}`) | `app/Http/Controllers/Basic/FormAnswerController.php` | **Direct** | File DUY NHẤT được Dev khai là thay đổi. 2 thay đổi: (a) guard chặn `getBotId() != form.bot_id` -> rollback + JSON `{status:false,msg}` HTTP 500; (b) `bot_id`/`form_id` chỉ set khi CREATE trang |
| F2 | `FormAnswerService::renderFormAnswer` | `app/Services/FormAnswer/FormAnswerService.php:164-176` | Indirect | Điểm crash (dòng 171). Hết crash nhờ data đúng, **không phải nhờ sửa code** (theo bản #124657) |
| F3 | FE `setting_form_items.js` — handler `.done`/`.fail` của `save-v3` | `setting_form_items.js` | Indirect | Không sửa, nhưng **là nơi hiển thị alert lỗi mới** -> phải test hiển thị đúng message tiếng Nhật |
| F4 | ⚠️ `FormAnswerController@8045/8094` — xoá trang (lọc `getBotId`) | `app/Http/Controllers/Basic/FormAnswerController.php` | Indirect (chưa đánh giá) | *Chỉ xuất hiện ở bản #124641*: "hệ quả cùng gốc, không sửa" -> **trang lệch `bot_id` có thể không xoá/sửa được** |
| F5 | ⚠️ `FormAnswerController::store` (dòng 811) | `app/Http/Controllers/Basic/FormAnswerController.php` | Không ảnh hưởng (theo Dev) | *Chỉ ở bản #124641*: "chỉ dựng object hiển thị, không ghi DB" |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answer_page.bot_id` | **UPDATE (hành vi thay đổi)** | Khi UPDATE trang KHÔNG còn bị ghi đè sang bot session (`getBotId()`) — chặn phát sinh lệch mới. Khi CREATE vẫn set = `form_answer.bot_id` |
| D2 | `form_answer_page.form_id` | **UPDATE (hành vi thay đổi)** | Cùng cơ chế D1 — field định danh, chỉ set khi CREATE |
| D3 | `form_answer_page.bot_id` — **data cũ đã lệch** | **MIGRATE (recover thủ công 1 lần)** | ⚠️ KHÔNG tự sửa. Dev: 6 form lệch (`page.bot_id = 0 != form.bot_id`). **Production chưa đếm.** Query ở mục 5 |
| D4 | Schema | **Không đổi** | Dev khẳng định: không thêm/xoá cột, không đổi schema, không đụng bảng khác |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — lưu biểu mẫu, màn `/basic/form-answer/edit/{id}` | F1, D1, D2 | **High** — luồng lưu form của TẤT CẢ khách. Dev: "lưu form đúng bot hành vi KHÔNG đổi", nhưng thao tác chéo bot nay **báo lỗi + KHÔNG lưu** (hành vi MỚI với user) |
| T2 | **Màn trả lời biểu mẫu công khai** `/form-answer/{unique_key}` (LINE user / LIFF) | F2, D3 | **High** — nơi phát sinh 500. Form cũ chưa recover **vẫn lỗi** sau deploy |
| T3 | ⚠️ **Xoá / sửa trang của form** (`FormAnswerController@8045/8094`) | F4, D3 | **Medium (chưa được Dev đánh giá ở bản mới nhất)** — bản #124641: "hệ quả cùng gốc, không sửa" |
| T4 | ⚠️ **Preview form (nút プレビュー)** — luồng QA dùng để tái hiện bug | F1, F2 | **Medium** — steps repro ở [01-bug-task.md](01-bug-task.md) đi qua nút プレビュー (save + mở preview). Dev **KHÔNG nhắc luồng preview** ở bất kỳ bản nào |

> **Ghi chú `/new-task`**: Dev ghi nguyên văn mục 4.3 chỉ có **1 dòng** (Form Builder FA-011). T2/T3/T4 do `/new-task` suy từ mục 1/2/3 + steps repro của QA — **cần tester xác nhận**, không phải Dev khai.

---

## 5. Recover data (mục ngoài template — Dev bắt buộc)

<!-- Nguyên văn mục "5. RECOVER DATA" — journal #124657. -->

```
⚠ CÓ — 6 form đã bị ghi đè bot_id=0 trên trang cần khôi phục về bot của form (chạy sau khi duyệt): UPDATE form_answer_page fp JOIN form_answer fa ON fp.form_id=fa.id SET fp.bot_id=fa.bot_id WHERE fp.bot_id<>fa.bot_id; Query chẩn đoán (đếm/soi trước): SELECT fa.id form_id, fa.bot_id form_bot, fp.id page_id, fp.page_number, fp.bot_id page_bot FROM form_answer fa JOIN form_answer_page fp ON fp.form_id=fa.id WHERE fp.bot_id<>fa.bot_id; Không recover thì 6 form cũ vẫn lỗi khi mở. (phạm vi: form_answer_page.bot_id lệch form_answer.bot_id (dev: 6 dòng / 6 form))
```

## 6. Verify của Dev (mục ngoài template)

<!-- Nguyên văn mục "6. VERIFY" — journal #124657. -->

```
Mức: lint
   Lệnh: php -l FormAnswerController.php: No syntax errors; git push --dry-run: a030d94a8c..aebc144d44 fast-forward OK (đã xử lý non-fast-forward do amend)
   Bằng chứng: DB dev: 6 form có form_answer_page.bot_id=0 != form_answer.bot_id (page_number=1) — đúng cơ chế saveV3 ghi đè bot_id trang bằng getBotId → renderForm lọc bot_id không thấy trang → crash dòng 171
```

## Tự review của AI + rủi ro khi test (nguyên văn)

```
Rủi ro thấp, khu trú trong saveV3. Lưu form đúng bot (luồng bình thường) hành vi KHÔNG đổi — create vẫn set bot_id đúng, update không đụng bot_id. 2 lớp: chặn thao tác chéo bot (báo lỗi cho user refresh) + không ghi đè bot_id/form_id khi update (chặn tận gốc crash non-object).
 • Rủi ro / lưu ý khi test:
   - Cần chạy query recover cho 6 form đã lệch; không recover thì các form đó vẫn lỗi khi mở (đã hết crash phát sinh mới)
   - Cần test: (a) lưu form bình thường OK; (b) đang mở bot A lưu form bot B / mất session → hiện thông báo, không lưu; (c) sau recover mở lại 6 form cũ → hiển thị bình thường
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **và đã chốt bản nào đúng (#124641 vs #124657)**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **đặc biệt `@8045/8094` delete page, và luồng preview プレビュー**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] **Đã xác nhận số bản ghi lệch `bot_id` trên PRODUCTION** (dev = 6, prod chưa đếm)
- [ ] **Đã chốt thời điểm chạy query recover** so với thời điểm deploy fix
- [ ] Nếu có điểm nghi vấn -> đã hỏi lại Dev trước khi member viết TC
