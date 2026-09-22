# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40997 — [AI][Performance] POST /basic/line_user/update chậm max 345s (5 lần/24h)` |
| Module / Màn hình | Friend List — thao tác **Xóa bạn bè** (`POST /basic/line_user/update` với `type=deleteLineUser`). Theo journal Dev: 4 lối vào — 友だち詳細 (SCR-FL-07), ブロックされた友だち xóa 1 + xóa hàng loạt (SCR-FL-05), và API app mobile `delete-friend`. Ảnh hưởng số liệu **Landing Page (FA-011)**. |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

**Endpoint:** `POST /basic/line_user/update`

**Mức:** high — xếp theo độ chậm: max 345s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 74

**Số lần chậm 24h:** 5 (kỳ trước 0, 1h qua 0) — xu hướng new

**Thời gian:** max 345s · p95 345s · trung bình 160.6s · median 65s

**Phân bố:** ≥15s SUPPERSLOW 4 · 10–15s VERYSLOW 0 · 5–10s SLOWLV1 1

**User bị ảnh hưởng:** 4 (tổng 4)

**Server:** step.lme.jp — **BotId:** 144726, 164017, 163876, 140177

**Lần đầu:** 2026-09-15 00:29 UTC — **Lần cuối:** 2026-09-15 06:29 UTC

**Lịch sử dài hạn:** tổng 5 lần chậm trong 1 ngày, đỉnh 5 lần/24h, chậm nhất 345s, từ 2026-09-15 00:29 UTC

### Vì sao ưu tiên này
- Độ chậm: p95 345s — treo gần như timeout (+45 điểm)
- Tần suất: 5 lần/24h (+6 điểm)
- User ảnh hưởng: 4 user bị chậm (+6 điểm)
- Độ mới: Xảy ra trong 6h qua (+9 điểm)
- Xu hướng: Mới xuất hiện (kỳ trước 0 lần, nay 5) (+8 điểm)

### URL mẫu
- `/basic/line_user/update`

### Các lần CHẬM NHẤT đã ghi nhận

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 345 | 2026-09-15 13:29 VN | SUPPERSLOW | 102490 | /basic/line_user/update |
| 329 | 2026-09-15 13:29 VN | SUPPERSLOW | 102490 | /basic/line_user/update |
| 65 | 2026-09-15 08:46 VN | SUPPERSLOW | 125028 | /basic/line_user/update |
| 59 | 2026-09-15 10:20 VN | SUPPERSLOW | 124924 | /basic/line_user/update |
| 5 | 2026-09-15 07:29 VN | SLOWLV1 | 106784 | /basic/line_user/update |

### Nguồn cảnh báo trong source
Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket do AI detect performance tự sinh từ log request chậm. -->

## Expected result

<!-- (trống — xem Ghi chú thêm của Leader) -->

## Actual result

<!-- (trống — xem Ghi chú thêm của Leader) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40997 không có attachment. Dữ liệu log request chậm đã được nhúng thẳng vào description (bảng "Các lần CHẬM NHẤT đã ghi nhận"). -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket do hệ thống AI detect performance tự sinh, không có steps/expected/actual do người báo. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** (2 câu gom thay 5 câu lặp + 3 index mới) + **regression** cả 4 luồng xóa bạn bè và số liệu Landing.

- **Môi trường phát hiện:** Production — server `step.lme.jp`.
- **Tần suất:** KHÔNG phải 100% — 5 lần chậm trong 24h, chỉ trên bot có lượng log trang đích lớn. Trên dữ liệu nhỏ (local/dev) thao tác vẫn nhanh → **không tái hiện được độ chậm ở local**.
- ⚠️ **RULE-08** — đây là bug **performance đo trên production**. Kết luận "đã hết chậm" **KHÔNG** được rút ra từ local/staging dữ liệu nhỏ. Studio hiện chỉ chạy 31/35 TC ở env `local`.
- **Điểm chậm tăng vọt khi chạy song song:** 59–65s khi xóa đơn lẻ → 329–345s khi 2 thao tác xóa chạy đồng thời (2 request cùng 1 phút của cùng 1 user 102490).
- **Cảnh báo từ chính Dev (journal):** không EXPLAIN được trên dữ liệu thật vì dev DB không kết nối được → **mức cải thiện thực tế chưa được đo**. 3 câu `ALTER TABLE ... ADD INDEX` chạy trên bảng log lớn → cần chạy ngoài giờ cao điểm / dùng `pt-online-schema-change`.
- **Migration chỉ kiểm chỉ mục theo TÊN** → nếu môi trường thật đã có chỉ mục tương đương nhưng khác tên, migration vẫn tạo thêm (dư thừa, không sai).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `144726`, `164017`, `163876`, `140177` |
| Friend | `<không ghi trong ticket — chỉ có user ID người thao tác>` |
| Đối tượng cấu hình | Landing page (trang đích) mà friend bị xóa từng bấm — bảng `detail_landing_click` · `time_action_landing` · `collect_open_landings` |
| User thực hiện thao tác | `102490` (2 request 345s + 329s), `125028` (65s), `124924` (59s), `106784` (5s) |
| Thời điểm lỗi | 2026-09-15 13:29 VN (2 request song song), 08:46 VN, 10:20 VN, 07:29 VN |
| Server | `step.lme.jp` (production) |
| Đối chứng | User `106784` cùng endpoint chỉ 5s (SLOWLV1) — bot ít log trang đích |

## Journal / note từ Redmine (nguyên văn)

**Journal #136862 — AI LME Fix bug — 2026-09-17:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Thao tác Xóa bạn bè (POST /basic/line_user/update với type=deleteLineUser) chạy cascade dọn khoảng 40 bảng; nút cổ chai nằm ở khối dọn số liệu trang đích. Ba bảng log trang đích dùng chung cho TOÀN hệ thống đều thiếu chỉ mục đúng với điều kiện đang lọc: bảng lượt bấm trang đích và bảng lượt hành động trang đích chỉ có chỉ mục theo mã trang đích trong khi câu lệnh lọc theo mã bot + mã bạn bè, còn bảng lượt mở trang đích không có chỉ mục nào ngoài khóa chính. Vì vậy mỗi lần xóa 1 bạn, máy chủ phải quét cạn các bảng log này nhiều lượt (2 câu tổng hợp + 1 câu xóa), cộng thêm 5 câu lặp lại cho MỖI trang đích mà bạn đó từng bấm (1 câu lấy mã thiết bị + 4 câu đếm). Chi phí gần như không phụ thuộc bot lớn hay nhỏ nên mọi bot đều chậm ở mức hàng chục giây (59s, 65s) và tăng vọt lên 329-345s khi hai thao tác xóa chạy song song cùng lúc, đúng như dữ liệu trong ticket (2 request cùng một phút của cùng một người dùng).

■ 2. CÁCH FIX
Sửa trên nhánh ai_small_40997 (sns-line, 5 file). (1) Thêm migration tạo 3 chỉ mục đúng với điều kiện lọc của khối dọn số liệu trang đích: bảng lượt bấm trang đích theo (mã bot, mã bạn bè, mã trang đích), bảng lượt hành động trang đích theo (mã bot, mã bạn bè), bảng lượt mở trang đích theo (mã bot, mã trang đích) — dùng prefix 64 ký tự cho cột mã bạn bè để không chạm giới hạn độ dài khóa, có kiểm tra chỉ mục đã tồn tại trước khi tạo nên chạy lại vẫn an toàn. (2) Gom 5 câu lệnh lặp cho mỗi trang đích (1 câu lấy mã thiết bị + 4 câu đếm) thành đúng 2 câu tổng hợp chạy một lần trước vòng lặp, qua 3 hàm dùng chung mới trong app/Helpers/functions.php; giữ nguyên phạm vi lọc, phạm vi xóa mềm và cách tính từng con số. Áp cho cả 4 luồng xóa bạn bè (xóa trên web, chặn-xóa, chặn-xóa hàng loạt, xóa trên app) theo đúng bài học #38390/#40708. (3) Thêm unit test cho hàm tra số liệu theo trang đích. Quét ngang: các chỗ khác dùng cùng bảng đều lọc theo mã trang đích (đã có chỉ mục) nên không thuộc phạm vi lỗi này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FriendlistController::updateLineUser case deleteLineUser (app/Http/Controllers/Basic/FriendlistController.php)
FriendlistController::deleteUserBlock (app/Http/Controllers/Basic/FriendlistController.php)
FriendlistController::deleteUserBlockAction (app/Http/Controllers/Basic/FriendlistController.php)
Api\FriendInformationController::deleteFriend (app/Http/Controllers/Api/FriendInformationController.php)
collectLandingClickStatsOfLineUsers (app/Helpers/functions.php)
collectLandingDeviceIdsOfLineUsers (app/Helpers/functions.php)
getLandingClickStat (app/Helpers/functions.php)
removeHistoryLineUser (app/Helpers/functions.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Helpers/functions.php
   - app/Http/Controllers/Basic/FriendlistController.php
   - app/Http/Controllers/Api/FriendInformationController.php
   - database/migrations/2026_09_15_103000_add_index_for_delete_friend_landing_cleanup.php
   - tests/Feature/LandingClickStatHelperTest.php
 • 4.2 Data ảnh hưởng:
   - detail_landing_click — thêm chỉ mục (bot_id, line_id(64), landing_id); KHÔNG đổi dữ liệu
   - time_action_landing — thêm chỉ mục (bot_id, line_id(64)); KHÔNG đổi dữ liệu
   - collect_open_landings — thêm chỉ mục (bot_id, landing_id); KHÔNG đổi dữ liệu
   - landing / landing_histories — số liệu trừ đi khi xóa bạn giữ nguyên công thức cũ, không thay đổi giá trị
 • 4.3 Tính năng liên quan:
   - Friend List / Friend Delete (outside glossary) — luồng xóa bạn bè trên web và app chạy nhanh hơn, logic dọn dữ liệu giữ nguyên
   - Landing Page (FA-011) — số liệu thống kê trang đích (lượt quét, lượt bấm, lượt kết bạn) vẫn bị trừ đúng như trước khi sửa
   - QR Code / Landing statistics (outside glossary) — chỉ hưởng lợi từ chỉ mục mới, không sửa code

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l 5 file đã sửa: No syntax errors detected; Boot Laravel (bootstrap/app.php + Console Kernel) rồi in toSql() của 2 câu tổng hợp mới: giữ nguyên điều kiện bot_id + line_id + phạm vi xóa mềm (deleted_at is null) như các câu COUNT cũ; In SQL của migration: ALTER TABLE ... ADD INDEX đúng 3 bảng, cột và prefix như thiết kế; class migration khớp tên file; vendor/bin/phpunit --filter LandingClickStatHelperTest: OK (5 tests, 5 assertions); git diff --stat release_step_20260827...ai_small_40997: đúng 5 file
   Bằng chứng: database/migrations/2020_06_15_182615_detail_landing_click.php: chỉ có index landing_id, không index line_id; database/migrations/2022_06_13_173633_create_time_action_landing_table.php: chỉ có index landing_id; database/migrations/2025_06_19_114922_create_collect_open_landings_table.php (+2 migration bổ sung cột): không tạo chỉ mục nào; MySQL dev (host.docker.internal:3306) không kết nối được trong lần chạy này nên không EXPLAIN được trên dữ liệu thật — kết luận dựa trên định nghĩa chỉ mục trong migration của chính repo; lesson #38390/#40708: cùng endpoint từng chậm vì quét bảng lớn; các nút cổ chai đã fix trước đó (url_shorten) đã có mặt trên release_step_20260827

■ TỰ REVIEW (AI)
Thay 5 câu truy vấn lặp theo từng trang đích bằng 2 câu tổng hợp chạy một lần, giữ nguyên bộ lọc (bot_id + line_id), phạm vi xóa mềm và cách tính từng con số; bổ sung chỉ mục cho 3 bảng log để các câu còn lại không quét cạn bảng. Không đổi logic nghiệp vụ, không đổi dữ liệu.
 • Rủi ro / lưu ý khi test:
   - 3 câu ALTER chạy trên bảng log lớn: MySQL 5.7 thêm secondary index theo ALGORITHM=INPLACE nên không chặn đọc/ghi, nhưng vẫn nên chạy ngoài giờ cao điểm hoặc bằng pt-online-schema-change (đã ghi chú trong migration)
   - Không EXPLAIN được trên dữ liệu thật vì dev DB không kết nối được; mức cải thiện thực tế cần đo lại sau khi lên môi trường có dữ liệu
   - Nếu môi trường thật đã có sẵn chỉ mục tương đương nhưng khác tên thì migration vẫn tạo thêm chỉ mục mới (chỉ kiểm theo tên) — dư thừa chứ không sai; DBA nên rà trước khi chạy

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40997 (nhánh gốc release_step_20260827, commit d958c99506, 5 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 14 phút 20 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=8d674aea-3195-4b3f-a45a-947a1a7a57ab
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40997
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
