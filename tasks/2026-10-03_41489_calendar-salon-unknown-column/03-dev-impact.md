# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #139822** trên Redmine #41489 (tác giả "AI LME Fix bug", 2026-10-02), do hệ thống **Auto-fixbug LME** tự sinh — ticket này không có section "Đánh giá ảnh hưởng" nằm trong description như format thường gặp, mà nằm trong journal note (báo cáo fix). Nội dung dưới đây chép **nguyên văn** 4 mục từ journal đó.
> Bổ sung đối chiếu **diff thật** lấy từ MCP LME TEST STUDIO (`task_get_context` task #353, section `dev_impact` + `spec_delta`) ở cuối file — khớp với nội dung Dev tự khai.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `32484cfc25` trên nhánh `ai_fixbug_41489` (repo `sns-line`), đã push origin |
| Branch | `ai_fixbug_41489` (gốc `release_step_20260827`) |
| Ngày submit đánh giá | `2026-10-02` (Journal #139822) |
| Auto-filled | `2026-10-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #139822 trên Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

API lưu câu hỏi của form đặt lịch Salon nhận NGUYÊN payload trình duyệt gửi lên rồi ghi thẳng vào bảng, không lọc theo cột thật của bảng. Payload của màn này ngoài các trường thật còn kèm khoá phụ chỉ dùng để hiển thị (thông tin bạn bè được liên kết), nên câu lệnh cập nhật sinh ra một cột không tồn tại, MySQL trả lỗi 1054 và request chết 500. Hậu quả với khách: bấm lưu chỉnh sửa câu hỏi nhưng không lưu được, màn hình lại không hiện thông báo lỗi nào (mã JS chỉ ghi console) nên người dùng tưởng đã lưu.

## 2. Cách fix

Chặn ngay tại chỗ ghi DB của màn cài đặt form đặt lịch Salon: thêm danh sách cột được phép cập nhật (hằng `UPDATABLE_COLUMNS` trong model `CalendarSalonSettingSendForms`, 19 cột, cố ý loại `id`/`calendar_id`/`bot_id`) và lọc payload bằng danh sách này trước khi gọi repository update; khoá không phải cột bị bỏ qua kèm 1 dòng log để truy nguyên, và nếu sau khi lọc không còn cột hợp lệ thì bỏ qua luôn câu update (tránh update rỗng).

Quét ngang: chỗ y hệt ở form đặt lịch **Bài học** (`calendar_setting_send_forms`) có cùng lỗ hổng nhưng khác tính năng nên **chỉ ghi nhận, chưa sửa** trong ticket này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Basic\CalendarSalonController::updateSettingForm` (`app/Http/Controllers/Basic/CalendarSalonController.php:1121`) | Không đổi | Caller — đã check, chỉ gọi qua service |
| 2 | `CalendarSalonSettingSendFormService::updateSettingForm` (`app/Services/CalendarSalon/CalendarSalonSettingSendFormService.php:97`) | **Có** — thêm lọc `array_intersect_key` theo whitelist trước khi gọi repository update, log key bị loại, bỏ qua update nếu rỗng | Chỗ ghi DB nhận payload client — root cause |
| 3 | `CalendarSalonSettingSendFormsRepository::update` (`app/Repositories/Eloquents/CalendarSalonSettingSendFormsRepository.php:40`) | Không đổi | Nơi thực thi update cuối cùng |
| 4 | `CalendarSalonSettingSendFormsRepository::getSettingSendForm` — eager load quan hệ `friendInformationSetting` (cùng file:26) | Không đổi | Nguồn sinh khoá phụ `friend_information_setting` trong payload hiển thị |
| 5 | `CalendarSalonSettingSendForms::friendInformationSetting` (`app/CalendarSalonSettingSendForms.php`) | Không đổi | Relation liên quan |
| 6 | `updateFormQuestion` — hàm JS gửi payload (`public/js/calendar_salon/calendar_detail.js:2566`) | Không đổi | FE — nguồn payload, chưa sửa việc "nuốt" lỗi 500 phía JS |
| 7 | `CalendarSalonSettingSendFormService::sortSettingForm` / `createNewSettingForm` | Không đổi | Đã truyền cột tường minh, **không bị ảnh hưởng** |
| 8 | `CalendarSettingSendFormService::updateSettingForm` (`app/Services/CalendarManagement/CalendarSettingSendFormService.php:242`) | Không đổi | Bản sinh đôi của **Bài học (Lesson)** — **cùng lỗi, không sửa lần này** (ghi nhận, đề xuất tách ticket) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonSettingSendForms` model — thêm hằng `UPDATABLE_COLUMNS` (19 cột) | `app/CalendarSalonSettingSendForms.php` | Direct | Cố ý loại `id`/`calendar_id`/`bot_id`/`created_at`/`updated_at`/`deleted_at` |
| F2 | `CalendarSalonSettingSendFormService::updateSettingForm` | `app/Services/CalendarSalon/CalendarSalonSettingSendFormService.php` | Direct | Lọc payload bằng whitelist + log key bị loại + skip update khi rỗng |
| F3 | `CalendarSettingSendFormService::updateSettingForm` (Lesson — bản sinh đôi) | `app/Services/CalendarManagement/CalendarSettingSendFormService.php:242` | **Indirect — KHÔNG sửa** | Cùng lỗi nhưng Dev chủ đích để ngoài phạm vi ticket này |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_setting_send_forms` (toàn bộ request update) | Không đổi dữ liệu đã lưu | Chỉ lọc dữ liệu đầu vào trước khi ghi — Dev khẳng định **không có migration/data change**, record cũ không bị ảnh hưởng, không cần recover |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — màn cài đặt form nhận đặt lịch salon (tab 「予約設定」 > 「お客様への質問項目」) | F1, F2 | High — mọi field hợp lệ phải tiếp tục lưu đúng sau khi thêm whitelist (rủi ro lọc nhầm field hợp lệ) |
| T2 | Đặt lịch Lesson (`calendar_setting_send_forms`, bản sinh đôi) | F3 | Low — chưa sửa, nhưng cần smoke để chắc thay đổi ở Salon không ảnh hưởng Lesson |

---

## 5. Recover data (bổ sung — nguyên văn journal)

✔ Không cần recover data — không có migration/data change, chỉ lọc input trước khi ghi.

## 6. Verify của Dev (bổ sung — nguyên văn journal)

- **Mức:** lint
- **Lệnh:** `php -l app/CalendarSalonSettingSendForms.php` → No syntax errors; `php -l app/Services/CalendarSalon/CalendarSalonSettingSendFormService.php` → No syntax errors; `php -r` kiểm chứng `array_intersect_key` với đúng payload trong exception: giữ 7 cột thật, loại đúng `friend_information_setting`.
- **Bằng chứng:** cột thật của bảng lấy từ 2 nguồn khớp nhau (migration `2024_05_24_171347_create_table_calendar_salon_setting_form_send.php` + snapshot schema production) — cả 2 đều KHÔNG có cột `friend_information_setting`; trên `origin/release_step_20260827` không có migration thêm cột sau đó; chỉ có đúng 1 chỗ ghi bảng này bằng mảng từ client.
- ⚠️ **Chưa kiểm chứng được trên DB dev** (`host.docker.internal:3306` connection refused) — Dev mới verify tới mức lint + đối chiếu schema tĩnh, **chưa chạy runtime thật**. Leader/Tester cần tự chạy case thật (UI + API) để xác nhận hành vi runtime, không chỉ tin vào lint.

## Rủi ro Dev tự nêu (TỰ REVIEW AI — nguyên văn journal)

- Cột mới thêm vào bảng sau này phải nhớ bổ sung vào hằng `UPDATABLE_COLUMNS`, nếu không sẽ **bị lọc mất lặng lẽ** (đã để comment ngay tại hằng).
- Nếu có client nào đang cố ý gửi `calendar_id`/`bot_id` để đổi chủ bản ghi thì nay bị chặn — đây là **chủ đích** (không cho client đổi chủ sở hữu); Dev đã rà màn hình và khẳng định không có luồng nào làm vậy.

## Đối chiếu diff thật (MCP LME TEST STUDIO — `task_get_context` task #353)

> `diffAvailable = true`, `diffStrategy = stat` (chỉ có diffstat, không có full diff). Nội dung Studio **khớp** với Journal #139822 ở trên, bổ sung vài điểm:

- **Files đổi** (diffstat): `app/CalendarSalonSettingSendForms.php` (+28) · `app/Services/CalendarSalon/CalendarSalonSettingSendFormService.php` (+14/-1).
- **Luồng chạm:** `EP-A70` — `POST /basic/calendar-salon/{id}/update-setting-form` ← `updateFormQuestion` (tab 予約設定 > お客様への質問項目). **Mọi** thao tác sửa câu hỏi Salon đều đi qua chỗ này.
- **Rủi ro hồi quy chính (theo Studio):** field hợp lệ bị lọc mất — whitelist khớp đủ cột migration, nhưng cần test lưu **từng field** FE thực gửi: `question`, `sub_question`, `enable` ('true'/'false'), `required`, `rule_type`, `rule_validation_type`, `link_friend_information`, `friend_information_id`, `enable_load_friend_information`, `display_method`, `options*`, `date_form`, `date_beginning`, `recording_time`.
- Logic phía trên (tạo `FriendInformationSetting` khi `link=2`, sync `FriendInfoOptionSelects`/`FriendInformationValue`, `total_user_has_value`) **không đổi** nhưng chạy **trước** bước lọc mới ⇒ cần regression câu hỏi radio/text/date có liên kết friend info.
- **Không đổi:** `createNewSettingForm`, `sortSettingForm` (gọi repository trực tiếp, truyền cột tường minh), `deleteSettingForm`, luồng booking phía khách (friend/LINE app).
- **Còn mở (chưa xử lý trong ticket này):** `can_delete`/`order` vẫn client sửa được qua API (chưa whitelist) — Studio đánh dấu "ghi nhận chờ xác nhận" (xem `REQ-004` trong requirements); Lesson (`calendar-management`) cùng lỗi gốc nhưng chưa sửa; FE vẫn "nuốt" lỗi 500 (không hiện toast lỗi).
