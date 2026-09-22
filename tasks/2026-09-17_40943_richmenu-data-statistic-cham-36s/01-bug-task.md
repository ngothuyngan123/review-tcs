# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40943 — [AI][Performance] GET /ajax/rich-menu/data-statistic/{id} chậm max 36s (7 lần/24h)` |
| Module / Màn hình | **Rich Menu (FA-004)** — màn **Thống kê lượt bấm rich menu** (bảng lượt bấm theo ngày × vùng, dòng tổng 合計, nút **tải CSV**), gọi `GET /ajax/rich-menu/data-statistic/{id}`. Studio đặt mã màn `SCR-RM-06` (タップ回数詳細). Màn thống kê **bản cũ** `Basic/UserController::ajaxInitDataDetail` có cùng pattern chậm nhưng **KHÔNG sửa** (ngoài phạm vi). |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

### Endpoint
`GET /ajax/rich-menu/data-statistic/{id}`

**Mức:** high — xếp theo độ chậm: max 36s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 70

**Số lần chậm 24h:** 7 (kỳ trước 0, 1h qua 2) — xu hướng new

**Thời gian:** max 36s · p95 36s · trung bình 10.14s · median 6s

**Phân bố:** ≥15s SUPPERSLOW 1 · 10–15s VERYSLOW 0 · 5–10s SLOWLV1 6

**User bị ảnh hưởng:** 3 (tổng 3)

**Server:** step.lme.jp — **BotId:** 102830, 28561, 167302

**Lần đầu:** 2026-09-14 02:29 UTC — **Lần cuối:** 2026-09-14 08:58 UTC

**Lịch sử dài hạn:** tổng 7 lần chậm trong 1 ngày, đỉnh 7 lần/24h, chậm nhất 36s, từ 2026-09-14 02:29 UTC

### Vì sao ưu tiên này
- Độ chậm: p95 36s — cực chậm (+38 điểm)
- Tần suất: 7 lần/24h (+6 điểm)
- User ảnh hưởng: 3 user bị chậm (+6 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Mới xuất hiện (kỳ trước 0 lần, nay 7) (+8 điểm)

### URL mẫu
- `/ajax/rich-menu/data-statistic/132647?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order=day&dir=DESC`
- `/ajax/rich-menu/data-statistic/132647?start_date=2026-09-01&end_date=2026-09-13&download_csv=0&page=1&per_page=100&order=day&dir=DESC`
- `/ajax/rich-menu/data-statistic/132648?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order=day&dir=DESC`
- `/ajax/rich-menu/data-statistic/132648?start_date=2026-09-07&end_date=2026-09-13&download_csv=0&page=1&per_page=100&order=day&dir=DESC`
- `/ajax/rich-menu/data-statistic/731325?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order=day&dir=DESC`

**Query param gặp:** dir, download_csv, end_date, order, page, per_page, start_date

### Các lần CHẬM NHẤT đã ghi nhận

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 36 | 2026-09-14 15:58 VN | SUPPERSLOW | 128116 | /ajax/rich-menu/data-statistic/709823?start_date=2025-10-23&end_date=2026-09-14&download_csv=1&page=1&per_page=100&order |
| 7 | 2026-09-14 09:29 VN | SLOWLV1 | 66811 | /ajax/rich-menu/data-statistic/132647?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order |
| 6 | 2026-09-14 14:02 VN | SLOWLV1 | 15878 | /ajax/rich-menu/data-statistic/731325?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order |
| 6 | 2026-09-14 09:30 VN | SLOWLV1 | 66811 | /ajax/rich-menu/data-statistic/132648?start_date=2026-09-08&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order |
| 6 | 2026-09-14 09:29 VN | SLOWLV1 | 66811 | /ajax/rich-menu/data-statistic/132647?start_date=2026-09-01&end_date=2026-09-13&download_csv=0&page=1&per_page=100&order |
| 5 | 2026-09-14 15:57 VN | SLOWLV1 | 128116 | /ajax/rich-menu/data-statistic/709823?start_date=2025-10-23&end_date=2026-09-14&download_csv=0&page=1&per_page=100&order |
| 5 | 2026-09-14 09:30 VN | SLOWLV1 | 66811 | /ajax/rich-menu/data-statistic/132648?start_date=2026-09-07&end_date=2026-09-13&download_csv=0&page=1&per_page=100&order |

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

<!-- Redmine #40943 không có attachment. Log request chậm đã nhúng thẳng trong description (bảng "Các lần CHẬM NHẤT đã ghi nhận"). -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket do hệ thống AI detect performance tự sinh, không có steps/expected/actual do người báo. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** (2 câu gom thay hàng nghìn câu đếm lặp + lọc ngày nửa mở + chỉ mục ghép mới) + **regression** số liệu màn thống kê (bảng, dòng tổng, phân trang, CSV).

- **Môi trường phát hiện:** Production — server `step.lme.jp`.
- **Tần suất:** KHÔNG phải 100% — 7 lần chậm/24h, chỉ trên rich menu có lịch sử bấm lớn và/hoặc khoảng ngày dài. Trên dữ liệu nhỏ (local/dev) màn vẫn nhanh → **không tái hiện được độ chậm ở local**.
- **Ca nặng nhất là tải CSV khoảng dài:** request 36s có `download_csv=1` + khoảng `2025-10-23 → 2026-09-14` (327 ngày). Khi tải CSV code bỏ `array_slice` phân trang → số câu đếm = 327 × số vùng. Cùng user 128116, cùng khoảng ngày nhưng `download_csv=0` chỉ 5s → **đối chứng rõ giữa xem bảng và tải CSV**.
- Các ca 5–7s: khoảng 7–13 ngày, `per_page=100` → vài chục câu đếm.
- ⚠️ **RULE-08** — đây là bug **performance đo trên production**. Kết luận "đã hết chậm" **KHÔNG** được rút ra từ local/staging dữ liệu nhỏ. Studio hiện chạy 34/34 TC ở env `local`.
- **Cảnh báo từ chính Dev (journal):** mức verify chỉ là `lint` — **chưa chạy EXPLAIN, chưa đo thời gian thực tế** vì dev DB `host.docker.internal:3306` connection refused. Dev đề nghị người review chạy EXPLAIN 2 câu mới trên môi trường có dữ liệu thật sau khi chạy migration.
- **Migration** thêm chỉ mục trên bảng nhật ký bấm cỡ lớn `detail_click_richmenu` → ALTER TABLE chạy lâu, tốn dung lượng tạm; chạy giờ thấp điểm và theo dõi đĩa.
- **Yokoten chưa sửa:** màn thống kê rich menu **bản cũ** `Basic/UserController::ajaxInitDataDetail` còn nguyên pattern chậm — khách dùng màn cũ vẫn có thể gặp lại triệu chứng.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `102830`, `28561`, `167302` (ticket không ghi bot nào ứng với user/rich menu nào) |
| Rich menu (`{id}` trên URL) | `709823` (ca 36s), `132647`, `132648`, `731325` |
| User thực hiện thao tác | `128116` (36s CSV + 5s xem bảng), `66811` (4 request 5–7s), `15878` (6s) |
| Thời điểm lỗi | 2026-09-14 15:58 VN (36s, `download_csv=1`, khoảng 2025-10-23 → 2026-09-14) · các ca còn lại 09:29–15:57 VN |
| Server | `step.lme.jp` (production) |
| Đối chứng | Rich menu `709823`, user `128116`, cùng khoảng ngày nhưng `download_csv=0` → 5s (15:57 VN) |

## Journal / note từ Redmine (nguyên văn)

**Journal #136535 — AI LME Fix bug — 2026-09-15:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn thống kê rich menu đếm lượt bấm bằng MỘT câu đếm riêng cho TỪNG ngày × TỪNG vùng bấm, cộng thêm một câu đếm tổng cho từng vùng. Khoảng ngày càng dài thì số câu lệnh càng nhiều — đặc biệt khi tải CSV, lúc này màn không phân trang nên lấy trọn khoảng (URL chậm nhất 36 giây có khoảng gần 11 tháng = 327 ngày), nhân với số vùng của rich menu thành hàng nghìn câu đếm cho một request. Mỗi câu lại lọc ngày bằng hàm DATE() bọc lên cột thời gian bấm nên MySQL không dùng được chỉ mục, phải mở và quét toàn bộ lịch sử bấm của vùng đó rồi mới lọc; bảng nhật ký bấm cũng chỉ có chỉ mục một cột (vùng bấm / rich menu), chưa có chỉ mục phù hợp cho bộ lọc bot + vùng + thời gian.

■ 2. CÁCH FIX
Viết lại phần đếm lượt bấm của màn thống kê rich menu: thay hàng nghìn câu đếm lặp (mỗi ngày × mỗi vùng, cộng mỗi vùng một câu tổng) bằng ĐÚNG 2 câu truy vấn tổng hợp — một câu gom theo (vùng, ngày) cho bảng chi tiết và một câu gom theo vùng cho dòng tổng — rồi ghép kết quả trong PHP theo đúng thứ tự vùng và ngày như cũ. Đồng thời đổi điều kiện lọc ngày từ DATE(time_click) sang so sánh khoảng thời gian nửa mở (>= đầu ngày bắt đầu, < đầu ngày sau ngày kết thúc) để MySQL dùng được chỉ mục, và thêm migration tạo chỉ mục ghép (bot_id, rich_item_id, time_click) cho bảng nhật ký bấm rich menu (migration idempotent, kiểm tra information_schema trước khi tạo/xoá). Số liệu trả về không đổi — đã kiểm tương đương cả ở biên đầu/cuối ngày, bản ghi ngoài kỳ, bản ghi của bot khác và bản ghi thời gian rỗng. Quét ngang: còn 1 chỗ TRÙNG y hệt pattern ở màn thống kê rich menu bản cũ (Basic/UserController::ajaxInitDataDetail) — CHƯA sửa vì ngoài phạm vi ticket, đã ghi trong mục yokoten.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
RichMenuService::calculateStatistic (app/Services/V2/RichMenuService.php:397) — điểm chậm chính, đã viết lại
RichMenuService::startOfDay / startOfNextDay (app/Services/V2/RichMenuService.php:496,504) — helper mốc ngày mới thêm
RichMenuController::dataStatistic (app/Http/Controllers/V2/RichMenuController.php:453) — endpoint bị báo chậm, chỉ gọi service, không đổi
StatisticRickMenuExport::array/headings (app/Exports/StatisticRickMenuExport.php) — bên tiêu thụ CSV, xác nhận hình dạng dữ liệu detailClick/countTotal giữ nguyên
UserController::ajaxInitDataDetail (app/Http/Controllers/Basic/UserController.php:1410) — bản cũ cùng pattern, KHÔNG sửa (ngoài phạm vi)
DetailClickRichmenuRepository (linect-service) — chỉ ghi, không có truy vấn đọc nào bị ảnh hưởng

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Services/V2/RichMenuService.php
   - database/migrations/2026_09_14_100000_add_statistic_index_to_detail_click_richmenu_table.php
 • 4.2 Data ảnh hưởng:
   - detail_click_richmenu — THÊM chỉ mục ghép detail_click_richmenu_statistic_index (bot_id, rich_item_id, time_click). Không sửa/xoá dữ liệu, chỉ thêm chỉ mục. Cần chạy migration khi release; bảng nhật ký này lớn nên ALTER TABLE sẽ tốn thời gian và dung lượng đĩa (MySQL 5.6+ thêm index là thao tác online, không khoá ghi), nên chạy vào khung giờ thấp điểm.
   - detail_click_richmenu — mỗi lần ghi log bấm (linect-service insert) sẽ tốn thêm chi phí cập nhật 1 chỉ mục; đổi lại đọc thống kê nhanh hơn nhiều lần.
 • 4.3 Tính năng liên quan:
   - Rich Menu (FA-004) — màn Thống kê rich menu (bảng lượt bấm theo ngày × vùng, dòng tổng, và tải CSV): số liệu giữ nguyên, chỉ đổi cách truy vấn cho nhanh

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Services/V2/RichMenuService.php: No syntax errors detected; php -l database/migrations/2026_09_14_100000_add_statistic_index_to_detail_click_richmenu_table.php: No syntax errors detected; Boot Laravel trong worktree (vendor copy thật + composer dump-autoload) rồi in toSql(): câu 1 = 'select `rich_item_id`, DATE(time_click) as day_click, COUNT(*) as total_click from `detail_click_richmenu` where `bot_id` = ? and `rich_item_id` in (?, ?, ?) and `time_click` >= ? and `time_click` < ? group by `rich_item_id`, DATE(time_click)'; câu 2 = cùng dạng, group by `rich_item_id`. Câu CŨ in ra 'date(`time_click`) = ?' — xác nhận đúng chỗ bọc hàm làm hỏng index; Kiểm 2 helper mốc ngày: startOfDay(2026-09-08)=2026-09-08 00:00:00; startOfNextDay(2026-09-14)=2026-09-15 00:00:00; Test tương đương ngữ nghĩa (PHP thuần, mô phỏng cả 2 vị từ trên cùng tập dữ liệu có bản ghi biên 00:00:00 và 23:59:59, bản ghi trước/sau kỳ, bản ghi bot khác, bản ghi time_click rỗng): detail OLD==NEW PASS, total OLD==NEW PASS; Xác nhận Laravel 5.5 Query\Builder::groupBy là variadic và columnize giữ nguyên Expression (vendor/laravel/framework .../Builder.php:1318)
   Bằng chứng: Chỉ mục hiện có của bảng (migration 2022_08_18_175625_create_detail_click_richmenu_table.php): chỉ rich_id và rich_item_id, mỗi cái 1 cột; KHÔNG có bot_id, KHÔNG có time_click — khớp với giả thuyết quét toàn bộ lịch sử của vùng; URL chậm nhất trong ticket có download_csv=1 và khoảng 2025-10-23..2026-09-14 (327 ngày); code bỏ qua array_slice khi download_csv=1 nên listDay giữ trọn 327 ngày → 327 × số vùng câu đếm, khớp mức 36 giây; Các URL 6-7 giây còn lại là khoảng 7-13 ngày, per_page=100 → vài chục câu đếm, khớp mức SLOWLV1; KHÔNG kiểm được trên MySQL thật: dev DB host.docker.internal:3306 connection refused, container chỉ có PDO driver mysql (không có pdo_sqlite) → chưa chạy EXPLAIN, chưa đo thời gian thực tế

■ TỰ REVIEW (AI)
Fix bám đúng root cause và tối thiểu: giữ nguyên toàn bộ hình dạng dữ liệu trả về (detailClick là mảng theo index ngày với khoá day + data theo đúng thứ tự vùng đã sort; countTotal là mảng theo đúng thứ tự vùng) nên màn hình, phân trang và lớp xuất CSV không phải sửa gì. Vẫn đếm SỐ DÒNG (COUNT(*)) chứ không đổi sang cộng cột count, đúng như hành vi cũ. Hai câu mới dùng khoảng datetime nửa mở, đã đối chiếu tương đương với whereDate ở cả 4 tình huống biên. Có bổ sung khởi tạo data = [] cho mỗi ngày (trước đây khi rich menu không có vùng nào thì khoá data không tồn tại) — an toàn hơn cho lớp xuất CSV và không đổi kết quả.
 • Rủi ro / lưu ý khi test:
   - Migration thêm chỉ mục trên bảng nhật ký click cỡ lớn: ALTER TABLE sẽ chạy lâu và tốn dung lượng tạm. Thêm index là thao tác online từ MySQL 5.6 (không chặn ghi) nhưng vẫn nên chạy vào giờ thấp điểm và theo dõi đĩa.
   - Thêm 1 chỉ mục làm mỗi lần ghi log bấm tốn thêm chút chi phí (bảng này ghi liên tục từ job linect). Đánh đổi chấp nhận được vì đường đọc đang chậm tới 36 giây.
   - Chưa đo được trên MySQL thật (dev DB đang tắt) nên chưa có EXPLAIN xác nhận optimizer chọn đúng chỉ mục mới. Đề nghị người review chạy EXPLAIN 2 câu trên môi trường có dữ liệu thật sau khi chạy migration.
   - Câu gom theo (vùng, ngày) trả về tối đa (số ngày × số vùng) dòng — với 1 năm và 20 vùng là khoảng 7.300 dòng, nhẹ; không có rủi ro bộ nhớ.
   - Endpoint bản cũ ajaxInitDataDetail vẫn còn nguyên pattern chậm (xem yokoten) — nếu khách dùng màn cũ thì vẫn có thể gặp lại triệu chứng.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40943 (nhánh gốc release_step_20260827, commit fe4d32fa54, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 9 phút
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=2b0d1cb4-bf11-4244-a6d8-6d5db8c7a48b
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40943
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
