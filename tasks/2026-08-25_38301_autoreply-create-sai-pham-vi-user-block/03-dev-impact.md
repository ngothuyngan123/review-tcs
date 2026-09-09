# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee ticket: `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | repo `sns-line` · commit `f6ee800f86` (2 file) · đã push. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38301 |
| Branch | `ai_fixbug_38301` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-25` (journal Redmine `2026-08-25T08:01:01Z` — **bản chốt**) |
| Auto-filled | `2026-08-25 by /new-task` |

> ⚠️ **Có 3 vòng báo cáo Auto-fixbug trên Redmine #38301** — file này chép nguyên văn **vòng 3 (bản chốt)**:
>
> | Vòng | Journal | Branch / commit | Phạm vi |
> |---|---|---|---|
> | 1 | `2026-07-03T11:13:40Z` | `ai_fixbug_37707` · `960dd329f1` · 1 file | 1 dòng — chỉ `AutoReply::create` (web). **Commit mồ côi, chưa từng vào release** |
> | 2 | `2026-08-21T04:18:32Z` | `ai_fixbug_38301` · `d467fbb296` · 1 file | 2 dòng — `AutoReply::create` + mảng default `initDataDetailAutoReply` (chỉ web) |
> | 3 (**chốt**) | `2026-08-25T08:01:01Z` | `ai_fixbug_38301` · `f6ee800f86` · **2 file** | **4 dòng** — cùng 2 pattern áp cho **cả web lẫn mobile API** |
>
> **Kiểm chứng của Dev**: `git merge-base --is-ancestor 960dd329f1 origin/release_step_20260805` → **NO** (commit vòng 1 KHÔNG có trong release hiện hành); commit cha `a6783b7558` → YES ⇒ branch `ai_fixbug_37707` đã merge trước, commit fix thêm sau bị bỏ quên.
>
> ⚠️ **QA bắt buộc verify môi trường test đang chạy commit `f6ee800f86`** trước khi kết luận pass/fail. Vòng test trước (21/08) fail chỉ vì môi trường vẫn chạy code cũ.
>
> ⚠️ **Verify level = `lint` (chỉ `php -l`)** — **KHÔNG có unit test / integration test** nào cho fix này. Toàn bộ bảo chứng đúng-sai dồn về manual test.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN — báo cáo Auto-fixbug 2026-08-25 (vòng 3, bản chốt). -->

2 nguyên nhân:

**(1)** Fix lần trước (03/07) commit vào branch `ai_fixbug_37707` — nhưng `#37707` là ticket Feature umbrella `[MCP] Triển khai Nhóm tính năng cơ bản Phase 2`, KHÔNG phải task fix, và branch đó đã được merge TRƯỚC khi commit fix được thêm vào ⇒ commit `960dd329` chưa bao giờ vào release (kiểm chứng: `git merge-base --is-ancestor 960dd329 origin/release_step_20260805` = NO) ⇒ môi trường tester vẫn chạy code cũ, bug tái hiện y nguyên.

**(2)** Bản thân code còn thiếu 2 chỗ:

- nhánh tạo mới `AutoReply::create` trong `saveDataDetailAutoReply` không gán `is_apply_active_friend` (bản ghi lấy default cột = 1 = `有効友だち` dù chọn `ブロックした友だち`), VÀ
- `initDataDetailAutoReply` trả mảng mặc định (màn TẠO MỚI) thiếu hẳn key `is_apply_active_friend` — `create.js` gán đè `self.data_reply = a.data_reply` nên key biến mất khỏi model Vue ⇒ màn tạo không radio nào được chọn sẵn, và nếu user không bấm radio thì payload không có key ⇒ khi có fix (1), `AutoReply::create` nhận NULL vào cột NOT NULL ⇒ MySQL lỗi 1048, lưu auto reply thất bại.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX — báo cáo Auto-fixbug 2026-08-25 (vòng 3, bản chốt). -->

Fix trên branch ĐỘC LẬP `ai_fixbug_38301` tách từ release hiện hành `release_step_20260805` (không gộp vào `ai_fixbug_37707` nữa: `#37707` là Feature umbrella `[MCP]` và branch đó đã merge xong ⇒ commit fix 03/07 mồ côi, chưa từng lên release).

**4 dòng / 2 file, cùng 2 pattern:**

- **(A)** nhánh tạo mới `AutoReply::create` thiếu `is_apply_active_friend` (bản ghi lấy default cột = 1 `有効友だち` dù chọn `ブロックした友だち`) → thêm vào, mirror nhánh update ngay trên.
- **(B)** mảng `$auto_reply` mặc định của endpoint init form thiếu hẳn key `is_apply_active_friend` → thêm `is_apply_active_friend => 1` (khớp default cột DB) để màn TẠO MỚI luôn có key trong model: radio `有効友だち` preselect đúng và payload luôn gửi giá trị, tránh insert NULL vào cột NOT NULL (lỗi MySQL 1048).

Áp cho **CẢ 2 luồng**:

- **web** `ReplyController` (`saveDataDetailAutoReply` + `initDataDetailAutoReply`)
- **mobile API** `AutoreplyMobileController` (`saveAutoreply` + `initAutoreplyForm`, route `api.php:345-346` `/init-autoreply-form` + `/save-autoreply`)

— bản mobile là copy 1:1 của web nên dính y hệt 2 pattern.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN — convert list plain sang bảng, giữ nguyên chữ của Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ReplyController::saveDataDetailAutoReply` — nhánh create (`app/Http/Controllers/Basic/ReplyController.php`, dòng ~1027) | **CÓ SỬA** — thêm `is_apply_active_friend => $dataReply->is_apply_active_friend` vào `AutoReply::create` | Pattern (A) — mirror nhánh update ngay trên (dòng ~1017) |
| 2 | `ReplyController::initDataDetailAutoReply` — mảng `$auto_reply` mặc định (dòng ~839-850) | **CÓ SỬA** — thêm `is_apply_active_friend => 1` | Pattern (B) — màn TẠO MỚI luôn có key trong model Vue, preselect đúng, tránh insert NULL |
| 3 | `AutoreplyMobileController::saveAutoreply` — nhánh create (`app/Http/Controllers/Api/Mobile/AutoreplyMobileController.php`, dòng ~290) | **CÓ SỬA** | Pattern (A) cho luồng mobile — copy 1:1 của web nên dính y hệt |
| 4 | `AutoreplyMobileController::initAutoreplyForm` — mảng mặc định (dòng ~105-116) | **CÓ SỬA** | Pattern (B) cho luồng mobile |
| 5 | `public/js/reply/create.js` (`data_reply` default + `self.data_reply = a.data_reply`) | **KHÔNG SỬA** | `create.js:20` default `1` bị ghi đè bởi `self.data_reply = a.data_reply` — lý do khiến key biến mất khỏi model Vue |
| 6 | `resources/views/basic/reply/create_v2.blade.php` (radio `v-model is_apply_active_friend`, Vue 2.6.12) | **KHÔNG SỬA** | View gắn radio vào model — nguồn để xác định hành vi preselect |
| 7 | `AutoReplyRepository:146` | **KHÔNG SỬA** | Rà toàn bộ `AutoReply::create` — chỗ này **đã copy field** |
| 8 | `TemplateRepository:1919` (clone auto-reply sang bot mới) | **KHÔNG SỬA — NGOÀI SCOPE** | ⚠️ **CHƯA copy `is_apply_active_friend`** — Dev ghi nhận cần ticket riêng |
| 9 | `BotTutorialExpRepository:74` | **KHÔNG SỬA** | Data tutorial, không liên quan |
| 10 | migration `2023_01_05_160920` | **KHÔNG SỬA** | Xác nhận cột `is_apply_active_friend` = `tinyInteger NOT NULL default 1` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn "■ 4.1 File thay đổi" — Dev liệt kê theo FILE. Cột Function/Module map lại từ mục 3 (chữ của Dev). -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ReplyController::saveDataDetailAutoReply` (nhánh CREATE) — endpoint **EP-12** `POST /admin/ajax/save-data-detail-auto-reply` | `app/Http/Controllers/Basic/ReplyController.php` | **Direct** | Pattern (A) — ghi `is_apply_active_friend` từ payload thay vì để DB dùng default |
| F2 | `ReplyController::initDataDetailAutoReply` (mảng mặc định) — endpoint **EP-11** `POST /admin/ajax/init-data-detail-auto-reply` | `app/Http/Controllers/Basic/ReplyController.php` | **Direct** | Pattern (B) — trả `is_apply_active_friend = 1` khi tạo mới |
| F3 | `AutoreplyMobileController::saveAutoreply` (nhánh CREATE) — route `/save-autoreply` (`api.php:346`) | `app/Http/Controllers/Api/Mobile/AutoreplyMobileController.php` | **Direct** | Pattern (A) cho app mobile Elme |
| F4 | `AutoreplyMobileController::initAutoreplyForm` (mảng mặc định) — route `/init-autoreply-form` (`api.php:345`) | `app/Http/Controllers/Api/Mobile/AutoreplyMobileController.php` | **Direct** | Pattern (B) cho app mobile Elme |
| F5 | Nhánh **UPDATE** của `saveDataDetailAutoReply` (~L1017) / `saveAutoreply` (~L279) | (2 file trên) | **Indirect** | **Không đổi** trong diff — vốn đã ghi đúng. Là đối chứng regression |
| F6 | Nhánh `initDataDetailAutoReply` gán từ `$dataReply` (~L882) / mobile (~L147) — luồng **edit / copy** | (2 file trên) | **Indirect** | **Không đổi** — vốn đã trả `is_apply_active_friend` từ DB |
| F7 | `TemplateRepository:1919` — clone auto-reply sang bot mới | `app/Repositories/.../TemplateRepository.php` | **Indirect — NGOÀI SCOPE, CHƯA FIX** | ⚠️ Cùng pattern thiếu field, Dev không sửa. Nguy cơ bug còn tồn tại ở luồng clone bot |
| F8 | `public/js/reply/create.js` · `create_v2.blade.php` (Vue 2.6.12) | `public/js/reply/create.js`, `resources/views/basic/reply/create_v2.blade.php` | **Indirect** | Không sửa nhưng quyết định hành vi preselect radio phía FE |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn "■ 4.2 Data ảnh hưởng". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `auto_reply.is_apply_active_friend` | **CREATE** (INSERT bản ghi mới) | Bản ghi **TẠO MỚI** (cả web lẫn app mobile) trước fix bị lưu default `1` (`有効友だち`) dù chọn `ブロックした友だち`; từ sau fix lưu đúng lựa chọn. **Bản ghi cũ không tự sửa được.** Cột: `tinyInteger NOT NULL default 1` (migration `2023_01_05_160920`) |

> **Không có migration / không cần recover data** — Dev kết luận `✔ Không cần recover data`.
>
> ⚠️ Lưu ý kỹ thuật của Dev: `config/database.php` `strict = false` ⇒ INSERT 1 dòng với NULL vào cột NOT NULL **vẫn lỗi 1048** (không tự chuyển 0). Đây là lý do bắt buộc phải có fix (B) kèm fix (A).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn "■ 4.3 Tính năng liên quan". -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Auto Reply (FA-003)** — màn `自動応答（作成）/（編集）` trên **web**: lưu + preselect đúng phạm vi đối tượng `アクション稼働対象絞り込み` (`有効友だち` / `ブロックした友だち`) | F1, F2, D1 | **High** |
| T2 | **Auto Reply (FA-003)** — **API mobile app Elme** (`/init-autoreply-form`, `/save-autoreply`): cùng hành vi như web khi tạo auto reply từ app | F3, F4, D1 | **High** |

---

## 5. Recover data

`✔ Không cần recover data` (nguyên văn mục ■ 5 của Dev).

> ⚠️ Leader lưu ý: kết luận này **chỉ đúng cho code**, không xử lý **bản ghi lịch sử** đã lưu sai `is_apply_active_friend = 1`. Nếu có KH đã tạo auto reply nhắm `ブロックした友だち` trước fix ⇒ auto reply đó đang chạy sai đối tượng và **không tự sửa**. Cần confirm với PM có phải rà data không.

## 6. Verify (Dev đã chạy)

| Mục | Nội dung |
|---|---|
| Mức | **`lint`** (không có unit test / integration test) |
| Lệnh | `php -l app/Http/Controllers/Basic/ReplyController.php` → No syntax errors detected<br>`php -l app/Http/Controllers/Api/Mobile/AutoreplyMobileController.php` → No syntax errors detected |

**Bằng chứng Dev dán (nguyên văn, tách xuống bullet):**

- `git merge-base --is-ancestor 960dd329f1 origin/release_step_20260805` → **NO** (commit fix cũ KHÔNG có trong release hiện hành); commit cha `a6783b7558` → YES ⇒ branch `ai_fixbug_37707` đã merge trước, commit fix thêm sau bị bỏ quên.
- Trên `release_step_20260805`: nhánh create của `saveDataDetailAutoReply` (**1027**) và `saveAutoreply` mobile (**289**) đều **thiếu** `is_apply_active_friend`, trong khi nhánh update (**1017 / 279**) đã có.
- 2 mảng mặc định (`ReplyController` **839-850**, `AutoreplyMobileController` **105-116**) **không có key** `is_apply_active_friend`; nhánh gán từ `$dataReply` (**882 / 147**) thì có.
- `config/database.php` `strict = false` ⇒ INSERT 1 dòng với NULL vào cột NOT NULL vẫn lỗi 1048 (không tự chuyển 0).
- `grep AutoReply::create` toàn `app/`: đã rà **5 chỗ**, 2 chỗ luồng tạo auto reply đã fix; `TemplateRepository:1919` (clone bot) **ngoài scope**; `AutoReplyRepository:146` đã copy field; `BotTutorialExpRepository:74` không liên quan.
- Fix nằm trên worktree riêng `/tmp/wt38301` (branch `ai_fixbug_38301`) vì working copy `source/sns-line` đang có worker khác chạy ticket `#37963`.

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

4 dòng, 2 file, cùng 1 pattern lặp ở web + mobile. Mỗi cặp: (a) mirror đúng nhánh update trong CÙNG hàm; (b) default `1` khớp default cột DB (migration `2023_01_05_160920`). Không ảnh hưởng bản ghi cũ, không đổi luồng edit/copy (2 luồng này vốn trả `is_apply_active_friend` từ DB).

**Rủi ro / lưu ý khi test (Dev tự nêu):**

1. Branch cũ `ai_fixbug_37707` còn commit `960dd329` mồ côi — **không nên merge branch đó** (nội dung đã có ở branch mới).
2. **App mobile phía client** cần đọc key `is_apply_active_friend` từ `/init-autoreply-form` để preselect radio; nếu client hardcode default thì vẫn hiển thị đúng vì server trả `1`.
3. **Clone auto-reply sang bot mới** (`TemplateRepository:1919`) vẫn **chưa copy** `is_apply_active_friend` — ngoài scope ticket, cần ticket riêng.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader nên chất vấn Dev (do `/new-task` phát hiện khi parse)

1. **Verify chỉ ở mức `lint`** — không có test tự động nào bảo chứng cho fix đụng vào luồng lưu dữ liệu. Có nên yêu cầu unit test cho nhánh CREATE (cả web + mobile) không?
2. **`TemplateRepository:1919` (clone auto-reply sang bot mới) chưa fix** dù cùng pattern → bug vẫn còn ở luồng clone bot. Raise ticket riêng ngay hay gộp vào ticket này?
3. **Client app mobile** — fix chỉ ở server. Nếu client hardcode default thì hành vi preselect trên app **chưa được ai verify**. Ai test phần app thật?
4. **Bản ghi cũ lưu sai** — Dev nói không cần recover. Có cần query thống kê xem thực tế có bao nhiêu bản ghi bị ảnh hưởng không (RULE-04)?
5. **Fix (B) đổi hành vi màn tạo mới**: trước đây không radio nào được chọn sẵn, sau fix `有効友だち` preselect. Đây là **thay đổi UI người dùng nhìn thấy** — spec có ghi rõ default phải là `有効友だち` không, hay đang suy từ default cột DB?
