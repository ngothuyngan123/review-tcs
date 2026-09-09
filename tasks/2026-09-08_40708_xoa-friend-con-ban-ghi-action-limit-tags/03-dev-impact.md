# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #40708 — Journal #135225 "★ AI AUTO-FIXBUG" (2026-09-08), do hệ thống Auto-fixbug LME sinh tự động.
> ⚠️ Description của ticket KHÔNG có section "Đánh giá ảnh hưởng" — toàn bộ nội dung dưới đây parse từ journal.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` (journal #135225) — assignee Redmine: `Ngô Thúy Ngần` |
| Commit / Pull Request | `<chưa có PR>` — commit `d5355ff361`; dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40708 |
| Branch | `ai_small_40708` (repo `sns-line`, nhánh gốc `release_step_20260805`, 2 file, đã push) |
| Ngày submit đánh giá | `2026-09-08` |
| Auto-filled | `2026-09-08 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Luồng xóa bạn bè trên tool dọn hàng chục bảng dữ liệu liên quan nhưng bỏ sót bảng ghi dấu 'đã chạy hành động khi thẻ đạt giới hạn' (`action_limit_tags`). Bản ghi cũ của bạn bè vẫn còn nên khi bạn bè đó kết bạn lại và được gắn lại thẻ A (đang bị giới hạn), hệ thống thấy đã có dấu nên bỏ qua, không chạy hành động gắn thẻ B nữa. Bảng này dùng chung cho cả web và job nền nên cả 2 phía đều bị chặn.

## 2. Cách fix

**(1) Fix gốc:** bổ sung bước xóa bản ghi ghi dấu hành động giới hạn thẻ (bảng `action_limit_tags`, lọc theo bot + bạn bè) vào hàm dọn dữ liệu chung của luồng xóa bạn bè trong `app/Helpers/functions.php` (`removeHistoryLineUser`) — hàm này được gọi ở cuối **cả 4 đường xóa bạn bè** (xóa 1 bạn ở màn danh sách bạn bè, xóa 1 bạn đã chặn, xóa nhiều bạn đã chặn, xóa bạn từ app) nên mọi đường xóa đều dọn sạch, bạn bè kết bạn lại và gắn lại thẻ đang bị giới hạn sẽ được chạy hành động (gắn thẻ B) như lần đầu.

**(2) Bổ sung theo spec:** thêm command recover cho dữ liệu **ĐÃ lỗi trước fix** — `app/Console/Commands/RecoverActionLimitTagOrphan.php`, chạy `php artisan recover:actionLimitTagOrphan [--chunk=1000] [--dry-run]`, xóa mọi bản ghi `action_limit_tags` mồ côi (không còn dòng `bot_line_user` tương ứng theo `bot_id` + `line_user_id`) đúng như câu SQL người phụ trách đưa; chạy theo lô (tìm tối đa `<chunk>` id mồ côi rồi xóa theo khóa chính) thay vì 1 câu `DELETE ... JOIN` để không khóa dài bảng `bot_line_user` (~137MB), dừng/chạy lại được, idempotent; có `--dry-run` để đếm trước khi xóa, ghi log start/end + số bản ghi xóa mỗi lô theo chuẩn `logInfo`. Command tự đăng ký nhờ `Kernel::commands()` đã `load(__DIR__.'/Commands')` nên **KHÔNG** phải sửa `app/Console/Kernel.php`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `removeHistoryLineUser` — `app/Helpers/functions.php:11967` | **CÓ SỬA** — thêm bước xóa `action_limit_tags` | Hàm dọn dữ liệu chung cuối luồng xóa bạn bè, nơi đặt fix |
| 2 | `ActionLimitTag::handleLimitActionTag` — `app/ActionLimitTag.php:11` | Không sửa | Nơi đọc bản ghi ghi dấu và quyết định có chạy hành động giới hạn hay không |
| 3 | `HelperService::addTags` — `app/Services/HelperService.php:1016-1045` | Không sửa | Nhánh thẻ đạt giới hạn gọi `handleLimitActionTag` rồi `sendAction` |
| 4 | `FriendlistController::updateLineUser` case `deleteLineUser` — `app/Http/Controllers/Basic/FriendlistController.php:2471-2867` | Không sửa (hưởng fix) | Xóa bạn bè ở màn danh sách bạn bè |
| 5 | `FriendlistController::deleteUserBlock` — `app/Http/Controllers/Basic/FriendlistController.php:3635-4023` | Không sửa (hưởng fix) | Xóa 1 bạn bè đã chặn |
| 6 | `FriendlistController::deleteUserBlockAction` — `app/Http/Controllers/Basic/FriendlistController.php:4026-4133` | Không sửa (hưởng fix) | Xóa nhiều bạn bè đã chặn |
| 7 | `Api\FriendInformationController::deleteFriend` — `app/Http/Controllers/Api/FriendInformationController.php:946-1338` | Không sửa (hưởng fix) | Xóa bạn bè từ app |
| 8 | `Basic\TagController::deletedDataTag` — `app/Http/Controllers/Basic/TagController.php:1039` | Không sửa | Đã có sẵn xóa bản ghi ghi dấu khi xóa hẳn thẻ |
| 9 | `LineUserModel.checkLimitActionModeAddTag` — `linect-service src/main/java/sns/line/models/LineUserModel.java:2355` | Không sửa | Phía job đọc cùng bảng, hưởng lợi từ fix, không phải sửa |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev chỉ ghi **"File thay đổi"** (2 file) ở mục 4.1, KHÔNG ghi theo dạng function `F1/F2/...`.
> `F1`–`F2` = file Dev thực sự sửa (nguyên văn mục 4.1). `F3`–`F6` suy từ **mục 3 của chính Dev** (danh sách function đã check) — không phải impact tự bịa thêm.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `removeHistoryLineUser` — hàm dọn dữ liệu chung luồng xóa bạn bè | `app/Helpers/functions.php` | **Direct** | File thay đổi (mục 4.1 Dev). Nơi đặt fix gốc — dùng chung cho cả 4 đường xóa bạn bè |
| F2 | Command `recover:actionLimitTagOrphan` (**file mới**) | `app/Console/Commands/RecoverActionLimitTagOrphan.php` | **Direct** | File thay đổi (mục 4.1 Dev). Tự đăng ký qua `Kernel::commands()`, không sửa `Kernel.php` |
| F3 | `ActionLimitTag::handleLimitActionTag` | `app/ActionLimitTag.php:11` | Indirect | Từ mục 3 — đọc bản ghi ghi dấu, quyết định có chạy action giới hạn hay không. Là nơi bug biểu hiện |
| F4 | `HelperService::addTags` | `app/Services/HelperService.php:1016-1045` | Indirect | Từ mục 3 — nhánh tag đạt giới hạn gọi `handleLimitActionTag` rồi `sendAction` |
| F5 | 4 caller xóa bạn bè: `FriendlistController::updateLineUser` (case `deleteLineUser`), `::deleteUserBlock`, `::deleteUserBlockAction`, `Api\FriendInformationController::deleteFriend` | `Basic/FriendlistController.php`, `Api/FriendInformationController.php` | Indirect | Từ mục 3 — không sửa code nhưng **đều đi qua F1** nên hành vi đổi ở cả 4 đường |
| F6 | `LineUserModel.checkLimitActionModeAddTag` (job nền) | `linect-service .../LineUserModel.java:2355` | Indirect | Từ mục 3 — phía job đọc **cùng bảng**, hưởng lợi từ fix dù không sửa mã job |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `action_limit_tags` (lọc theo `bot_id` + `line_user_id`) | **DELETE** | Từ nay bị xóa cùng bạn bè ở luồng xóa bạn bè (cả 4 đường) |
| D2 | `action_limit_tags` — bản ghi **mồ côi** (không còn `bot_line_user` tương ứng) | **DELETE (VĨNH VIỄN)** | Command recover xóa dữ liệu tồn đọng trước fix. Chỉ xóa dấu vết 'đã chạy hành động', **KHÔNG** đụng thẻ/bạn bè/hành động; bản ghi của bạn bè còn tồn tại (kể cả đang bị chặn) **KHÔNG** bị ảnh hưởng. Khuyến nghị chạy `--dry-run` để đếm trước, và **backup bảng** trước khi chạy thật |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> ⚠️ Dev **KHÔNG ghi mức nguy cơ regression** (High/Medium/Low) cho bất kỳ tính năng nào — cột dưới để `<Dev không ghi>`, Leader tự chấm khi review.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend List (FA-013)** — xóa bạn bè dọn thêm dấu vết hành động giới hạn thẻ, không để lại dữ liệu rác chặn nghiệp vụ | F1, F5, D1 | `<Dev không ghi>` |
| T2 | **Tag Management (FA-012)** — hành động khi thẻ đạt giới hạn chạy lại đúng cho bạn bè xóa rồi kết bạn lại; command recover trả lại trạng thái đúng cho dữ liệu đã lỗi trước fix | F2, F3, F4, D1, D2 | `<Dev không ghi>` |
| T3 | **Action Settings (SC-004)** — hành động tự động (gắn thẻ khác) khi thẻ đạt giới hạn được kích hoạt lại đúng cho **cả web và job nền** | F3, F4, F6, D1 | `<Dev không ghi>` |

---

## 5. Recover data (nguyên văn Dev)

⚠️ **CÓ** — Bạn bè đã bị xóa **TRƯỚC** khi có fix vẫn còn dòng tồn đọng trong `action_limit_tags`, nên nếu họ kết bạn lại thì **vẫn dính lỗi cũ**. Nên dọn các dòng mồ côi (không còn bản ghi bạn bè tương ứng) bằng câu lệnh do người phụ trách chạy sau khi release:

```sql
DELETE alt FROM action_limit_tags alt
LEFT JOIN bot_line_user blu
  ON blu.line_user_id = alt.line_user_id
 AND blu.bot_id = alt.bot_id
WHERE blu.id IS NULL;
```

(nên chạy `SELECT COUNT(*)` cùng điều kiện để đếm trước, và chạy theo lô nếu số lượng lớn)

**Phạm vi:** Toàn bộ dòng `action_limit_tags` không còn cặp (`bot_id`, `line_user_id`) trong `bot_line_user` — chỉ là dữ liệu ghi dấu, xóa không ảnh hưởng thẻ hay hành động đang chạy.

## 6. Verify của Dev (nguyên văn)

**Mức:** `lint`

**Lệnh đã chạy:**
- `php -l app/Console/Commands/RecoverActionLimitTagOrphan.php` → No syntax errors detected
- Boot app thật trong worktree (vendor hardlink + `.env` + `composer dump-autoload`): `php artisan list` hiện `recover:actionLimitTagOrphan` ⇒ command tự đăng ký qua `Kernel::commands()` `load(__DIR__.'/Commands')`, không cần sửa Kernel
- In SQL sinh ra bởi query builder:
  ```sql
  select `alt`.`id` from `action_limit_tags` as `alt`
  left join `bot_line_user` as `blu`
    on `blu`.`line_user_id` = `alt`.`line_user_id` and `blu`.`bot_id` = `alt`.`bot_id`
  where `blu`.`id` is null and `alt`.`id` > ? order by `alt`.`id` asc limit 1000
  ```
  ⇒ khớp ĐÚNG điều kiện câu SQL trong spec bổ sung
- `git diff --name-only origin/release_step_20260805...ai_small_40708` → đúng 2 file (`functions.php` + command mới), không lẫn commit worker khác
- Làm trong worktree cô lập (`wt/40708-addspec` detach từ `3bb34f0f84`) rồi dời branch bằng CAS `git update-ref`; worktree đã gỡ, autoload cây chung đã dump lại nguyên trạng

**Bằng chứng:**
- Xác nhận ngữ nghĩa cột: `action_limit_tags.line_user_id` = `line_user.id` (**KHÔNG** phải `bot_line_user.id`) — `HelperService::addTags` truyền cùng biến `$line_user_id` cho `tagLineUser` và `ActionLimitTag`
- `ConversationReplicate.php:174` join `bot_line_user.line_user_id = tag_line_user.line_user_id` ⇒ join của câu SQL trong spec là **ĐÚNG** (db-refined ghi `line_user_id` → `bot_line_user.id` là **sai**)
- `BotLineUser` model **KHÔNG** dùng SoftDeletes và 4 luồng xóa bạn bè đều gọi `BotLineUser::where(...)->delete()` (xóa cứng) ⇒ điều kiện `blu.id IS NULL` nhận diện đúng bạn bè đã bị xóa, **không quét nhầm bạn bè chỉ bị chặn**
- ⚠️ **Không chạy được trên dữ liệu thật:** MySQL dev `host.docker.internal:3306` vẫn `Connection refused` tại thời điểm implement ⇒ **chưa đếm/xóa thử**; đề nghị chạy `--dry-run` trên staging trước khi chạy thật

## 7. Rủi ro / lưu ý khi test (Dev tự review — nguyên văn)

- Command **xóa dữ liệu vĩnh viễn**: nên backup bảng `action_limit_tags` + chạy `--dry-run` trước khi chạy thật trên production
- Bảng **không có index** trên (`bot_id`, `line_user_id`) nên mỗi lô quét theo khóa chính; bảng lớn thì nên chạy giờ thấp điểm và giảm `--chunk` nếu thấy nặng
- Dữ liệu mồ côi do **nguyên nhân KHÁC** (vd bot bị xóa) **cũng bị dọn** — đúng phạm vi câu SQL người phụ trách đưa
- Các rủi ro của fix gốc vẫn giữ nguyên: bạn bè chỉ **CHẶN/bỏ theo dõi** hoặc **gỡ thẻ ở màn quản lý thẻ** vẫn giữ dấu vết, **chờ BA xác nhận**

> Ghi chú của Dev: phần bổ sung chỉ THÊM 1 file command mới, không đụng logic đang chạy. Giữ đúng điều kiện xóa của câu SQL người phụ trách đưa, chỉ đổi cách thực thi sang chạy theo lô + xóa theo khóa chính để tránh khóa bảng lâu. Không thêm schedule tự chạy — đây là command recover một lần, human chủ động chạy.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
