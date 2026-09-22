# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41075 — [AI][Performance] POST /ajax/popup/init-data-detail-click chậm max 135s (2 lần/24h)` |
| Module / Màn hình | Popup (FA-018) — màn 「詳細データ」 (Chi tiết dữ liệu click) của popup, tab 「数値情報」; endpoint `POST /ajax/popup/init-data-detail-click` |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

**Endpoint**

```
POST /ajax/popup/init-data-detail-click
```

**Mức:** high — xếp theo độ chậm: max 135s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 68
**Số lần chậm 24h:** 2 (kỳ trước 0, 1h qua 2) — xu hướng new
**Thời gian:** max 135s · p95 135s · trung bình 84s · median 135s
**Phân bố:** ≥15s SUPPERSLOW 3 · 10–15s VERYSLOW 0 · 5–10s SLOWLV1 1
**User bị ảnh hưởng:** 2 (tổng 3)
**Server:** step.lme.jp — **BotId:** 179609, 160621, 46203
**Lần đầu:** 2026-09-14 02:31 UTC — **Lần cuối:** 2026-09-17 08:26 UTC
**Lịch sử dài hạn:** tổng 4 lần chậm trong 3 ngày, đỉnh 2 lần/24h, chậm nhất 135s, từ 2026-09-14 02:31 UTC

**Vì sao ưu tiên này**

- Độ chậm: p95 135s — treo gần như timeout (+45 điểm)
- Tần suất: 2 lần/24h (+2 điểm)
- User ảnh hưởng: 2 user bị chậm (+6 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Mới xuất hiện (kỳ trước 0 lần, nay 2) (+3 điểm)

**URL mẫu**

```
/ajax/popup/init-data-detail-click
```

**Các lần CHẬM NHẤT đã ghi nhận**

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 135 | 2026-09-17 15:26 VN | SUPPERSLOW | 42768 | /ajax/popup/init-data-detail-click |
| 33 | 2026-09-17 15:24 VN | SUPPERSLOW | 139689 | /ajax/popup/init-data-detail-click |
| 29 | 2026-09-14 09:31 VN | SUPPERSLOW | 139689 | /ajax/popup/init-data-detail-click |
| 7 | 2026-09-15 08:22 VN | SLOWLV1 | 86581 | /ajax/popup/init-data-detail-click |

**Nguồn cảnh báo trong source**

Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket do AI detect performance tự tạo từ log request chậm, không có steps của người dùng. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41075 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket do hệ thống AI detect performance tự tạo từ log request chậm, không có steps tái hiện của người dùng. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** (gom N+1 query · đếm bằng SQL · thêm index) + **regression số liệu hiển thị** (dữ liệu trả về phải giữ nguyên tuyệt đối).
- **Môi trường phát hiện**: production `step.lme.jp`.
- **Tần suất**: KHÔNG phải 100% — chỉ 4 lần chậm trong 3 ngày. Phụ thuộc khối lượng log của popup và độ dài khoảng ngày lọc (30–90 ngày ⇒ 60–180 lần quét toàn bảng nối tiếp).
- **Ngưỡng cảnh báo hệ thống**: >4s (middleware `NotifyChatworkRequestTimeSlow`), mốc SLOWLV1 ≥5s / VERYSLOW ≥10s / SUPPERSLOW ≥15s — dùng làm ngưỡng pass/fail cho TC đo thời gian.
- ⚠️ **RULE-08**: fix gồm migration thêm index trên 2 bảng nhật ký lớn (`detail_action_popup`, `detail_landing_click`). Kết luận về performance chỉ có giá trị trên môi trường có khối lượng dữ liệu tương đương production; local/staging không thay thế được.
- **Lưu ý vận hành từ Dev**: chạy migration vào giờ thấp điểm, theo dõi thời gian chạy + dung lượng đĩa. Migration đã viết idempotent.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Server | `step.lme.jp` (production) |
| bot_id | `179609`, `160621`, `46203` |
| User bị ảnh hưởng | `42768` (135s) · `139689` (33s và 29s) · `86581` (7s) |
| Đối tượng cấu hình | Popup — màn 「詳細データ」, tab 「数値情報」 (bảng thống kê theo ngày) |
| Thời điểm lỗi | `2026-09-17 15:26 VN` (chậm nhất, 135s); lần đầu `2026-09-14 09:31 VN` |
| Đối chứng | Cùng endpoint với khoảng ngày ngắn / popup ít log → phản hồi bình thường (≤7s) |

## Journal / note từ Redmine (nguyên văn)

**Journal #137307 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Endpoint phục vụ màn Chi tiết dữ liệu click của Popup. Tab thống kê theo ngày chạy vòng lặp TỪNG NGÀY trong khoảng lọc, mỗi ngày bắn 2 query riêng (N+1): đếm hiển thị/click và đếm bạn bè thêm mới; query đếm hiển thị/click còn tải TOÀN BỘ bản ghi ra PHP rồi đếm bằng vòng lặp thay vì đếm bằng SQL. Nặng nhất là 2 bảng nhật ký này chỉ có khoá chính, KHÔNG có index theo mã popup + thời gian, nên mỗi query là một lần quét toàn bảng nhật ký khổng lồ (bảng ghi 1 dòng cho mỗi lần popup hiển thị của mọi bot). Chọn khoảng 30-90 ngày tương đương 60-180 lần quét toàn bảng nối tiếp nhau, gây treo tới 135s.

■ 2. CÁCH FIX
Gom N+1 query trong PopupService::getDataActionPopup: thay vì gọi 2 query cho MỖI ngày, nay gọi 2 query tổng hợp GROUP BY ngày cho cả khoảng lọc rồi ghép kết quả theo từng ngày trong PHP (số query cố định = 2, không phụ thuộc số ngày). Thêm 2 hàm range mới trong PopupRepository (countDataActionPopupByTypeInRange, countDataAddFriendByPopupInRange) và sửa hàm đếm theo ngày cũ để đếm bằng COUNT/SUM trong SQL thay vì tải toàn bộ bản ghi ra PHP đếm bằng vòng lặp. Thêm migration tạo index (popup_id, created_at) cho 2 bảng nhật ký detail_action_popup và detail_landing_click (trước đó chỉ có khoá chính nên mọi truy vấn theo popup đều quét toàn bảng). Đã bỏ 1 dòng ghi log debug vô nghĩa trong vòng lặp ngày. Dữ liệu trả về giữ nguyên tuyệt đối — đã kiểm chứng bằng harness so sánh output bản cũ vs bản mới trên cùng dữ liệu, chỉ khác số lần gọi repository (10 lần còn 2 lần với khoảng 5 ngày). Quét ngang: mẫu vòng lặp truy vấn theo ngày còn ở Cross Analysis / Calendar / Admin User nhưng khác tính năng và khác bảng nên để ngoài scope.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
PopupAjaxController::initDataDetailClick (app/Http/Controllers/Ajax/PopupAjaxController.php:563)
PopupService::getDataActionPopup (app/Services/PopupService.php:471) — ĐÃ SỬA
PopupRepository::countDataActionPopupByType (app/Repositories/Eloquents/PopupRepository.php:87) — ĐÃ SỬA
PopupRepository::countDataActionPopupByTypeInRange (app/Repositories/Eloquents/PopupRepository.php:116) — MỚI
PopupRepository::countDataAddFriendByPopup (app/Repositories/Eloquents/PopupRepository.php:133)
PopupRepository::countDataAddFriendByPopupInRange (app/Repositories/Eloquents/PopupRepository.php:157) — MỚI
getBetweenDates (app/Helpers/functions.php:10018) — chỉ đọc, giữ nguyên
PopupController::detailDataClick (app/Http/Controllers/Basic/PopupController.php:86) — nguồn khoảng ngày mặc định
BotController (app/Http/Controllers/Admin/BotController.php:8008) và FlowDeleteBot (app/Console/Commands/FlowDeleteBot.php:481) — xoá theo popup_id, hưởng lợi từ index mới, không sửa

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Services/PopupService.php
   - app/Repositories/Eloquents/PopupRepository.php
   - database/migrations/2026_09_18_000001_add_index_popup_id_created_at_for_detail_log_tables.php
 • 4.2 Data ảnh hưởng:
   - detail_action_popup — CHỈ ĐỌC trong luồng sửa; migration THÊM index idx_dap_popup_id_created_at (popup_id, created_at). Không đổi cột/dữ liệu. Ảnh hưởng ghi: mỗi lần chèn bản ghi hiển thị/click popup phải cập nhật thêm 1 index (chi phí ghi tăng nhẹ, đổi lại bỏ được quét toàn bảng khi đọc).
   - detail_landing_click — CHỈ ĐỌC trong luồng sửa; migration THÊM index idx_dlc_popup_id_created_at (popup_id, created_at). Không đổi cột/dữ liệu. Ảnh hưởng ghi: tương tự, mỗi lần chèn bản ghi click/thêm bạn từ landing tốn thêm 1 index.
   - LƯU Ý VẬN HÀNH: 2 bảng này là nhật ký lớn, chạy migration thêm index nên làm vào giờ thấp điểm. MySQL 5.6+ thêm index kiểu INPLACE (online DDL) nên vẫn cho phép ghi trong lúc chạy, nhưng vẫn cần theo dõi thời gian và dung lượng đĩa cho index mới.
 • 4.3 Tính năng liên quan:
   - Popup (FA-018) — màn Chi tiết dữ liệu click của popup: bảng thống kê theo ngày (số hiển thị, số click, tỉ lệ click, số bạn thêm mới, tỉ lệ thêm bạn) nhanh hơn nhiều, số liệu giữ nguyên
   - QR Code Action / Landing (FA-017) — dùng chung bảng nhật ký click landing; chỉ nhận thêm 1 index, không đổi logic, truy vấn theo popup nhanh hơn
   - Popup Ads Setting (FS-006) — cùng nhóm cấu hình popup, không đụng logic, chỉ hưởng lợi gián tiếp từ index

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l app/Repositories/Eloquents/PopupRepository.php: No syntax errors detected; php -l app/Services/PopupService.php: No syntax errors detected; php -l database/migrations/2026_09_18_000001_add_index_popup_id_created_at_for_detail_log_tables.php: No syntax errors detected; Kiểm SQL sinh ra bằng Eloquent (toSql + bindings): 2 query range đúng cú pháp, tham số hoá đầy đủ, giữ nguyên điều kiện where của bản cũ và vẫn có ràng buộc soft-delete (deleted_at is null) của bảng click landing; Harness so sánh output bản CŨ vs bản MỚI của getDataActionPopup trên cùng tập dữ liệu giả lập (3 ca: khoảng 5 ngày có ngày trống, khoảng 1 ngày, khoảng start>end): JSON kết quả GIỐNG HỆT, chỉ khác số lần gọi repository 10 -> 2; Chưa chạy được EXPLAIN trên MySQL dev (host.docker.internal:3306 Connection refused) — kết luận thiếu index dựa trên migration tạo bảng (chỉ có increments('id')) và không có migration nào thêm index cho popup_id/created_at; Không viết PHPUnit: thay đổi thuộc nhóm truy vấn DB (repository), không phải logic thuần theo quy tắc B4c
   Bằng chứng: database/migrations/2022_07_12_133040_create_tbl_detail_action_popup.php chỉ tạo increments('id') + popup_id + browser + action + timestamps, KHÔNG có index nào cho popup_id/created_at; database/migrations/2020_06_15_182615_detail_landing_click.php chỉ index landing_id; migration 2025_06_13_164227 định thêm index post_code nhưng dòng đó bị comment; /workspace/share/db/db-refined/schema-annotated/tables/detail_action_popup.sql ghi rõ [SIZE] Unbounded — needs archival (bảng nhật ký không giới hạn); grep toàn repo: getBetweenDates chỉ có DUY NHẤT 1 nơi gọi là PopupService::getDataActionPopup

■ TỰ REVIEW (AI)
Tối ưu đúng điểm nghẽn và giữ nguyên tuyệt đối dữ liệu trả về: bỏ N+1 (2 query/ngày -> 2 query cho cả khoảng), đếm bằng SQL thay vì tải bản ghi ra PHP, thêm index (popup_id, created_at) cho 2 bảng nhật ký chưa có index. Đã chứng minh tương đương output bằng harness chạy song song bản cũ và bản mới trên cùng dữ liệu. Không refactor ngoài phạm vi endpoint.
 • Rủi ro / lưu ý khi test:
   - Migration thêm index trên 2 bảng nhật ký lớn — nên chạy giờ thấp điểm, theo dõi thời gian chạy và dung lượng đĩa; migration đã viết idempotent (kiểm tra index tồn tại trước khi thêm) nên chạy lại an toàn
   - Chi phí ghi tăng nhẹ ở 2 bảng nhật ký do phải cập nhật thêm index mỗi lần chèn
   - Phép gộp theo ngày dùng DATE(created_at) của MySQL trong khi bản cũ so sánh khoảng thời gian trong PHP — cả hai đều chạy trên cùng múi giờ phiên MySQL nên kết quả trùng khớp; điều kiện lọc khoảng vẫn để nguyên dạng so sánh khoảng nên index vẫn được dùng (không bọc hàm quanh cột trong điều kiện WHERE)
   - Chưa đo được thời gian thực tế trên môi trường có dữ liệu lớn vì MySQL dev trong container không kết nối được (Connection refused) — cần theo dõi lại số liệu giám sát sau khi release

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41075 (nhánh gốc release_step_20260827, commit ccffbeed6c, 3 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 9 phút 36 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=adbef931-0b88-471e-946f-84b2431f452b
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41075
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
