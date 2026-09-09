# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **comment "★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST"** của user `AI LME Fix bug` trên Redmine #40151, ngày **2026-08-25 06:27:41Z** (journal #3).
> Nguyên văn đầy đủ ở **Phụ lục** cuối file. Phần 1–4 bên dưới là map vào cấu trúc template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — **không phải Dev người**. Assignee Redmine hiện tại: `Hạnh Nguyễn` |
| Commit / Pull Request | commit `a0dbc96ebe` (4 file) — **không có link PR GitHub/GitLab** trong Redmine. Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=70413417-c812-4f9e-8621-e797a65b684c · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40151 |
| Branch | `ai_small_40151` (repo **sns-line**, nhánh gốc `release_step_20260805`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-25` |
| Auto-filled | `2026-08-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn từ Redmine (mục ■ 1. NGUYÊN NHÂN):

Ticket **#39230** thêm chốt chặn ở phần khởi tạo của màn Sao chép dữ liệu, chặn **TOÀN BỘ** mọi lời gọi dữ liệu của màn này với tài khoản gói miễn phí (trả lỗi **403**). Trong khi đó quy định (và chính popup có sẵn trên màn) ghi rõ tài khoản miễn phí **VẪN được lấy mã sao chép** để làm tài khoản nguồn copy sang tài khoản trả phí.

Vì bị chặn hết nên với tài khoản miễn phí:
- ô mã sao chép **trống**,
- danh sách dữ liệu sẽ được sao chép **trống**,
- thông tin tài khoản đích **trống**,
- nút cấp lại mã cũng bị chặn nên bấm **không có tác dụng** (giao diện chỉ ghi log lỗi ngầm, **không báo gì** ra UI).

**→ Đây là REGRESSION do ticket #39230, không phải bug mới.** (`BUG`)

## 2. Cách fix

> Nguyên văn từ Redmine (mục ■ 2. CÁCH FIX):

1. **Thu hẹp chốt chặn gói miễn phí** ở màn Sao chép dữ liệu: thêm danh sách route bị chặn (`FREE_PLAN_DENIED_ROUTES` — bắt đầu sao chép, trang tiến trình, kiểm tra tiến trình) và **chỉ kiểm tra gói cho đúng các route đó**.
2. Các route **nạp dữ liệu màn**, **nạp lịch sử** và **cấp lại mã sao chép** được **cho qua** → tài khoản miễn phí thấy lại mã sao chép, danh sách dữ liệu sẽ được sao chép và thông tin tài khoản đích; đồng thời dùng được nút sao chép mã và nút cấp lại mã.
3. **Bổ sung cờ gói miễn phí do máy chủ tính** (`is_free_plan`, dùng đúng hàm `Bots::isFreePlan` dùng để chặn) trả về cho giao diện. Giao diện dùng cờ này để hiện popup cần nâng cấp và khoá ô nhập mã nguồn — **trước đây giao diện chỉ xét loại gói bằng `plan_type == 2` nên tài khoản miễn phí kiểu mới bị lọt**.
4. **Chặn thêm ở giao diện** khi bấm bắt đầu sao chép với tài khoản miễn phí để không bị lỗi im lặng.
5. **Quét ngang:** đây là màn **DUY NHẤT** chặn cả màn ở phần khởi tạo; các màn khác chặn theo từng thao tác nên không cần sửa.

> ⚠️ **Lưu ý cho Leader:** đây là fix **mở rộng quyền** (nới chốt chặn) + **thêm chốt chặn 2 tầng mới** (FE + BE). Rủi ro chính là **hở quyền** (free thực thi được copy) chứ không chỉ là "hiển thị lại được mã".

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn từ Redmine (mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN) — Dev liệt kê dạng plain list, đã convert sang bảng.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BackupController::__construct` — `app/Http/Controllers/Basic/BackupController.php` | **Sửa** — bỏ chặn toàn màn, chỉ chặn theo route trong `FREE_PLAN_DENIED_ROUTES` | Đây chính là nơi #39230 đặt chốt chặn quá rộng → root cause |
| 2 | `BackupController::FREE_PLAN_DENIED_ROUTES` — cùng file | **Thêm mới** (hằng số) | Danh sách 3 route thực thi vẫn phải chặn với gói miễn phí |
| 3 | `BackupController::createTransferCode` — cùng file | Check (route được **cho qua**) | Route cấp lại mã — phải dùng được với bot free |
| 4 | `BackupController::saveBackupHistory` — cùng file | Check (route vẫn **bị chặn**) | Route thực thi sao chép — free không được chạy |
| 5 | `BackupService::getBotData` — `app/Services/BackupService.php` | **Sửa** — gắn thêm `is_free_plan` vào data trả về FE | Cấp cờ gói cho FE dùng chung, tránh lệch chốt chặn |
| 6 | `BackupService::createTransferCode` — cùng file | Check | Luồng sinh mã sao chép mới |
| 7 | `Bots::isFreePlan` — `app/Bots.php` | Check (dùng lại, **không sửa**) | Hàm chuẩn nhận diện gói miễn phí (cả free cũ `plan_type=2` lẫn free mới `contract_type='free'`) |
| 8 | `BotRepository::findByIdWithColumn` — `app/Repositories/Eloquents/BotRepository.php` | Check | Đọc bản ghi bot (gồm `transfer_code`) |
| 9 | `BotRepository::updateTransferCode` — cùng file | Check | Ghi `transfer_code` khi cấp lại mã |
| 10 | `initBotData` — `public/js/admin/backup/backup.js` | **Sửa** — đọc `is_free_plan` từ server thay vì chỉ xét `plan == 2` | FE nhận diện đúng free kiểu mới |
| 11 | `startCreateCode` — cùng file | Check | Luồng bấm cấp lại mã ở FE |
| 12 | `startCopy` — cùng file | **Sửa** — thêm chặn FE khi bot free bấm khởi chạy sao chép | Tránh lỗi im lặng (silent 403) |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ **Lưu ý mapping:** Dev đánh số 4.1 = "File thay đổi", 4.2 = "Data ảnh hưởng", 4.3 = "Tính năng liên quan". Template repo quy định 4.1 = **function**, 4.2 = **data**, 4.3 = **feature**. Bảng 4.1 dưới đây được **suy ra từ mục 3 + danh sách 4 file thay đổi** của Dev.

### 4.1. List function bị ảnh hưởng

**4 file thay đổi (nguyên văn Dev):**
- `app/Http/Controllers/Basic/BackupController.php`
- `app/Services/BackupService.php`
- `public/js/admin/backup/backup.js`
- `resources/views/basic/backup/backup.blade.php`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BackupController::__construct` + hằng `FREE_PLAN_DENIED_ROUTES` | `app/Http/Controllers/Basic/BackupController.php` | **Direct** | Chốt chặn chuyển từ **chặn toàn màn** → **chặn theo tên route**. Rủi ro Dev tự nêu: chốt chặn dựa vào **TÊN route**, đổi tên route mà quên sửa hằng → **hở quyền** |
| F2 | Route `backup.get-bot-data` (nạp dữ liệu màn) | BackupController | **Direct** | Từ 403 → **cho qua** với bot free |
| F3 | Route `backup.get-backup-history` (nạp lịch sử) | BackupController | **Direct** | Từ 403 → **cho qua** với bot free |
| F4 | Route `backup.create-transfer-code` (cấp lại mã) | BackupController | **Direct** | Từ 403 → **cho qua**; đây là route **mutate** `bots.transfer_code` |
| F5 | Route `backup.save-backup-history` (bắt đầu sao chép) | BackupController | **Direct** | **Vẫn chặn 403** với free — phải verify không hở |
| F6 | Route trang tiến trình `backup.processing` | BackupController | **Direct** | **Vẫn chặn** với free. ⚠️ TC Studio ghi chú: chỉ 403 **khi gọi ajax**; **điều hướng URL trực tiếp không bị nhánh này chặn** |
| F7 | Route `backup.check-processing` (kiểm tra tiến trình) | BackupController | **Direct** | **Vẫn chặn 403** với free |
| F8 | `BackupService::getBotData` | `app/Services/BackupService.php` | **Direct** | Trả thêm `is_free_plan` cho FE |
| F9 | `Bots::isFreePlan` | `app/Bots.php` | **Indirect** (dùng lại, không sửa) | Nguồn sự thật nhận diện gói. Nếu hàm này sai → **cả FE lẫn BE sai đồng thời** |
| F10 | `initBotData` / `startCreateCode` / `startCopy` | `public/js/admin/backup/backup.js` | **Direct** | FE: nhận diện free bằng `is_free_plan` hoặc `plan == 2`; thêm deny modal ở `startCopy` |
| F11 | View màn Sao chép dữ liệu (2 chỗ khoá theo cờ mới) | `resources/views/basic/backup/backup.blade.php` | **Direct** | `:disabled` theo `isFreePlan` cho ô nhập mã nguồn + nút xác nhận mã |
| F12 | `BotRepository::findByIdWithColumn` / `updateTransferCode` | `app/Repositories/Eloquents/BotRepository.php` | **Indirect** | Không sửa, nhưng nằm trên đường cấp lại mã |

### 4.2. List data bị update khi fix bug

> Nguyên văn Dev (mục ■ 4.2): *"Không có — chỉ đổi luồng kiểm tra quyền và dữ liệu trả về cho giao diện, không thêm/sửa/xoá bản ghi nào. Mã sao chép (cột `transfer_code` của bảng `bots`) chỉ thay đổi khi người dùng chủ động bấm cấp lại mã, dùng lại đúng luồng có sẵn."*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.transfer_code` | **UPDATE** (chỉ khi user chủ động bấm 再発行) | Dev khẳng định "không có data impact", nhưng fix **mở quyền gọi `create-transfer-code` cho bot free** → **nhóm tài khoản có thể ghi vào cột này đã MỞ RỘNG**. Đây là data impact thật, cần TC verify |
| D2 | `backup_history` (bản ghi tiến trình sao chép) | **KHÔNG được CREATE** với bot free | Đối chứng âm: sau khi free bấm khởi chạy (bị chặn 2 tầng) → **không được sinh** bản ghi mới |
| D3 | Payload response `get-bot-data` → thêm field `is_free_plan` | (không phải DB) | Contract API đổi — FE phụ thuộc field này |

> ⚠️ **Leader lưu ý:** Dev ghi "Không có data impact" là **chưa chính xác hoàn toàn** — xem D1. Ngoài ra Dev **không kiểm chứng được trên MySQL dev** (cổng 3306 từ chối kết nối trong container), nên toàn bộ phần DB **chưa có bằng chứng thật**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Data Copy / Backup (FA-033)** — màn Sao chép dữ liệu với **bot gói miễn phí** | F1–F4, F8, F10, F11, D1 | **High** — tài khoản free xem và cấp lại được mã sao chép, thấy danh sách dữ liệu được sao chép + thông tin tài khoản đích; thao tác **thực thi sao chép vẫn phải bị chặn** |
| T2 | **Plan gating màn Sao chép dữ liệu** (outside glossary) | F1, F5–F9, F10, F11 | **High** — chốt chặn chuyển từ chặn toàn màn sang **chặn theo từng route thực thi**; FE + BE dùng chung cờ gói do máy chủ tính nên không lệch chốt chặn. **Rủi ro hở quyền nếu đổi tên route** |
| T3 | **Data Copy / Backup với bot gói CÓ PHÍ** (standard/pro) | F1, F5, F11 | **Medium** — regression: luồng nhập mã nguồn → xác minh → khởi chạy sao chép phải **không đổi** |
| T4 | **Nhận diện gói miễn phí kiểu mới** (`contract_type='free'`, `plan_type≠2`) | F9, F10 | **Medium** — fix **vá thêm một lỗ có sẵn**: free kiểu mới trước đây **không** bị khoá ô nhập mã nguồn ở FE. Cần TC riêng cho loại tài khoản này |
| T5 | **Trang tiến trình sao chép** (`/basic/backup/processing/{id}`) | F6 | **Low–Medium** — Dev nêu: bot đang chạy sao chép rồi bị **hạ xuống gói miễn phí giữa chừng** thì không xem được tiến trình. Dev khẳng định *"giống hệt trước khi fix, không phải hồi quy mới"*. ⚠️ Nhưng TC Studio ghi chú route này **chỉ 403 khi ajax**, điều hướng URL trực tiếp **không bị chặn** → cần verify |

---

## Mục 5 & 6 từ báo cáo Dev (không có trong template — giữ lại vì ảnh hưởng cách viết TC)

### 5. Recover data

✔ **Không cần recover data.**

### 6. Verify mà Dev đã chạy

**Mức: `unit-test`** — Dev **KHÔNG chạy test tay trên UI thật**. Nguyên văn các lệnh:

- `php -l` trên `BackupController.php`, `BackupService.php` → No syntax errors
- `node --check public/js/admin/backup/backup.js` → OK
- Biên dịch Blade rồi `php -l` bản biên dịch → No syntax errors; xác nhận có **đúng 2 chỗ khoá** theo cờ mới
- Khởi động Laravel đọc bảng route: **7 route** của màn phân giải đúng tên; **3 tên trong danh sách chặn đều tồn tại thật**
- **Mô phỏng khớp route 6 đường dẫn**: nạp dữ liệu màn / nạp lịch sử / cấp lại mã = **CHO QUA**; bắt đầu sao chép / trang tiến trình / kiểm tra tiến trình = **CHẶN** với gói miễn phí
- Kiểm tra chuyển JSON của bản ghi bot: cờ `is_free_plan` xuất hiện trong dữ liệu trả về cho FE

**Bằng chứng Dev viện dẫn:**

- Popup có sẵn trên màn ghi rõ quy định: gói miễn phí **không dùng được** sao chép dữ liệu, **CHỈ lấy được mã sao chép** (`backup.blade.php` dòng 352)
- Comment BA trên Redmine ngày 25-08-2026 yêu cầu fill lại: mã transfer + nút sao chép mã + chức năng đổi mã, danh sách chức năng backup, thông tin bot đích
- FE vốn đã có sẵn nhánh xử lý gói miễn phí → chứng tỏ ý định thiết kế là **cho vào màn**, không phải chặn cả màn
- ❌ **Không kiểm chứng được trên MySQL dev**: cổng 3306 của máy chủ phát triển **từ chối kết nối** trong container

### Rủi ro / lưu ý khi test — do chính Dev nêu

1. Nếu bot **chưa từng có** mã sao chép (`transfer_code` rỗng) thì ô mã **vẫn trống** cho tới khi bấm cấp lại mã — bấm là có mã ngay. Bot tạo qua luồng thêm bot đều được sinh mã sẵn nên khả năng này thấp; **không kiểm chứng được** vì không kết nối được MySQL dev.
2. Trang tiến trình sao chép **vẫn chặn** với tài khoản miễn phí: bot đang chạy sao chép rồi bị hạ xuống gói miễn phí giữa chừng thì không xem được tiến trình — Dev khẳng định **giống hệt trước khi fix**, không phải hồi quy mới.
3. Chốt chặn nay dựa vào **TÊN route**: nếu sau này đổi tên route trong tệp định tuyến mà quên sửa danh sách thì **chốt chặn hở**. Đã đặt tên hằng rõ ràng kèm chú thích và đã xác nhận 3 tên tồn tại thật khi khởi động Laravel.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ Dev ghi "không có data impact", xem lại **D1**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Phụ lục — nguyên văn comment Auto-fixbug trên Redmine #40151

> User `AI LME Fix bug` · 2026-08-25 06:27:41Z · journal #3
> Thay đổi kèm theo: `status` 1 → 9 (Fix done - Đợi test), `assigned_to` → 58, `Commit Date` → 2026-08-25

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Ticket #39230 thêm chốt chặn ở phần khởi tạo của màn Sao chép dữ liệu, chặn TOÀN BỘ mọi lời gọi dữ liệu của màn này với tài khoản gói miễn phí (trả lỗi 403). Trong khi đó quy định (và chính popup có sẵn trên màn) ghi rõ tài khoản miễn phí VẪN được lấy mã sao chép để làm tài khoản nguồn copy sang tài khoản trả phí. Vì bị chặn hết nên với tài khoản miễn phí: ô mã sao chép trống, danh sách dữ liệu sẽ được sao chép trống, thông tin tài khoản đích trống; nút cấp lại mã cũng bị chặn nên bấm không có tác dụng (giao diện chỉ ghi log lỗi ngầm, không báo gì).

■ 2. CÁCH FIX
Thu hẹp chốt chặn gói miễn phí ở màn Sao chép dữ liệu: thêm danh sách route bị chặn (bắt đầu sao chép, trang tiến trình, kiểm tra tiến trình) và chỉ kiểm tra gói cho đúng các route đó; các route nạp dữ liệu màn, nạp lịch sử và cấp lại mã sao chép được cho qua nên tài khoản miễn phí thấy lại mã sao chép, danh sách dữ liệu sẽ được sao chép và thông tin tài khoản đích, đồng thời dùng được nút sao chép mã và nút cấp lại mã. Bổ sung cờ gói miễn phí do máy chủ tính (bằng đúng hàm dùng để chặn) trả về cho giao diện, giao diện dùng cờ này để hiện popup cần nâng cấp và khoá ô nhập mã nguồn — trước đây giao diện chỉ xét loại gói bằng 2 nên tài khoản miễn phí kiểu mới bị lọt. Chặn thêm ở giao diện khi bấm bắt đầu sao chép với tài khoản miễn phí để không bị lỗi im lặng. Quét ngang: đây là màn DUY NHẤT chặn cả màn ở phần khởi tạo, các màn khác chặn theo từng thao tác nên không cần sửa.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BackupController::__construct (app/Http/Controllers/Basic/BackupController.php)
BackupController::FREE_PLAN_DENIED_ROUTES (app/Http/Controllers/Basic/BackupController.php)
BackupController::createTransferCode (app/Http/Controllers/Basic/BackupController.php)
BackupController::saveBackupHistory (app/Http/Controllers/Basic/BackupController.php)
BackupService::getBotData (app/Services/BackupService.php)
BackupService::createTransferCode (app/Services/BackupService.php)
Bots::isFreePlan (app/Bots.php)
BotRepository::findByIdWithColumn (app/Repositories/Eloquents/BotRepository.php)
BotRepository::updateTransferCode (app/Repositories/Eloquents/BotRepository.php)
initBotData (public/js/admin/backup/backup.js)
startCreateCode (public/js/admin/backup/backup.js)
startCopy (public/js/admin/backup/backup.js)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/BackupController.php
   - app/Services/BackupService.php
   - public/js/admin/backup/backup.js
   - resources/views/basic/backup/backup.blade.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đổi luồng kiểm tra quyền và dữ liệu trả về cho giao diện, không thêm/sửa/xoá bản ghi nào. Mã sao chép (cột transfer_code của bảng bots) chỉ thay đổi khi người dùng chủ động bấm cấp lại mã, dùng lại đúng luồng có sẵn.
 • 4.3 Tính năng liên quan:
   - Data Copy / Backup (FA-033) — tài khoản gói miễn phí xem và cấp lại được mã sao chép, thấy danh sách dữ liệu được sao chép và thông tin tài khoản đích; thao tác thực thi sao chép vẫn bị chặn như cũ
   - Plan gating cho màn Sao chép dữ liệu (outside glossary) — chốt chặn gói miễn phí chuyển từ chặn toàn màn sang chặn theo từng route thực thi; giao diện dùng chung cờ gói do máy chủ tính nên không lệch chốt chặn

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l app/Http/Controllers/Basic/BackupController.php: No syntax errors detected; php -l app/Services/BackupService.php: No syntax errors detected; node --check public/js/admin/backup/backup.js: OK; Biên dịch Blade rồi php -l bản biên dịch: No syntax errors detected; kiểm tra chú thích Blade đã bị gỡ khỏi output và có đúng 2 chỗ khoá theo cờ mới; Khởi động Laravel đọc bảng route: 7 route của màn phân giải đúng tên, 3 tên trong danh sách chặn đều tồn tại thật; Mô phỏng khớp route 6 đường dẫn: nạp dữ liệu màn / nạp lịch sử / cấp lại mã = CHO QUA; bắt đầu sao chép / trang tiến trình / kiểm tra tiến trình = CHẶN với gói miễn phí; Kiểm tra chuyển JSON của bản ghi bot: cờ gói miễn phí xuất hiện trong dữ liệu trả về cho giao diện
   Bằng chứng: Popup có sẵn trên màn đã ghi rõ quy định: gói miễn phí không dùng được sao chép dữ liệu, CHỈ lấy được mã sao chép (resources/views/basic/backup/backup.blade.php dòng 352); Bình luận của BA trên Redmine ngày 25-08-2026 yêu cầu fill lại: mã transfer + nút sao chép mã + chức năng đổi mã, danh sách chức năng backup, thông tin bot đích; Giao diện vốn đã có sẵn nhánh xử lý gói miễn phí (hiện popup cần nâng cấp, khoá ô nhập mã nguồn) — chứng tỏ ý định thiết kế là cho vào màn, không phải chặn cả màn; Không kiểm chứng được trên MySQL dev: cổng 3306 của máy chủ phát triển từ chối kết nối trong container

■ TỰ REVIEW (AI)
Fix bám đúng root cause (chốt chặn quá rộng do ticket trước) và giữ nguyên ràng buộc nghiệp vụ quan trọng: tài khoản miễn phí vẫn KHÔNG được làm tài khoản đích của thao tác sao chép. Phần mở quyền chỉ gồm 3 route đọc/cấp mã; 3 route thực thi vẫn chặn, đã mô phỏng khớp route để xác nhận. Việc trả cờ gói miễn phí từ máy chủ còn vá thêm một lỗ có sẵn: tài khoản miễn phí kiểu mới trước đây không bị khoá ô nhập mã nguồn ở giao diện.
 • Rủi ro / lưu ý khi test:
   - Nếu bot chưa từng có mã sao chép trong dữ liệu (cột transfer_code rỗng) thì ô mã vẫn trống cho tới khi người dùng bấm cấp lại mã — bấm là có mã ngay. Bot tạo qua luồng thêm bot đều được sinh mã sẵn nên khả năng này thấp; không kiểm chứng được vì không kết nối được MySQL dev.
   - Trang tiến trình sao chép vẫn chặn với tài khoản miễn phí: nếu một bot đang chạy sao chép rồi bị hạ xuống gói miễn phí giữa chừng thì không xem được tiến trình — hành vi này giống hệt trước khi fix, không phải hồi quy mới.
   - Chốt chặn nay dựa vào TÊN route: nếu sau này đổi tên route trong tệp định tuyến mà quên sửa danh sách thì chốt chặn hở. Đã đặt tên hằng rõ ràng kèm chú thích và đã xác nhận 3 tên tồn tại thật khi khởi động Laravel.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40151 (nhánh gốc release_step_20260805, commit a0dbc96ebe, 4 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 9 phút 28 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=70413417-c812-4f9e-8621-e797a65b684c
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40151
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
