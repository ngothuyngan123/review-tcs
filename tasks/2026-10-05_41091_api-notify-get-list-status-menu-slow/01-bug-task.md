# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41091 — [AI][Performance] POST /api/mobile/notify/get-list-status-menu-notify chậm max 43s (18 lần/24h)` |
| Module / Màn hình | `Notification Settings (FA-006) — API trạng thái menu thông báo của app Elme (mobile). Ticket có gắn thêm 1 endpoint liên quan: POST /api/mobile/notify/get-order-history (xem Ghi chú thêm của Leader).` |

## Mô tả bug (bản dịch tiếng Việt)

Ticket tự tạo bởi check-performance AI (từ report request chậm bắn lên Chatwork room 417532006).

### Endpoint
```
POST /api/mobile/notify/get-list-status-menu-notify
```
**Mức:** high — xếp theo độ chậm: max 43s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 70
**Số lần chậm 24h:** 18 (kỳ trước 13, 1h qua 2) — xu hướng flat
**Thời gian:** max 43s · p95 43s · trung bình 12.06s · median 9s
**Phân bố:** ≥15s SUPPERSLOW 12 · 10–15s VERYSLOW 7 · 5–10s SLOWLV1 27
**User bị ảnh hưởng:** 6 (tổng 15)
**Server:** step.lme.jp — **BotId:** —
**Lần đầu:** 2026-09-14 02:21 UTC — **Lần cuối:** 2026-09-18 01:07 UTC
**Lịch sử dài hạn:** tổng 46 lần chậm trong 5 ngày, đỉnh 21 lần/24h, chậm nhất 43s, từ 2026-09-14 02:21 UTC

### Vì sao ưu tiên này
- Độ chậm: p95 43s — cực chậm (+38 điểm)
- Tần suất: 18 lần/24h (+10 điểm)
- User ảnh hưởng: 6 user bị chậm (+10 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Tương đương 24h trước (+0 điểm)

### URL mẫu
```
/api/mobile/notify/get-list-status-menu-notify
```

### Các lần CHẬM NHẤT đã ghi nhận

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 43 | 2026-09-18 04:43 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 25 | 2026-09-18 04:43 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 22 | 2026-09-16 09:20 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 20 | 2026-09-14 22:15 VN | SUPPERSLOW | 73445 | /api/mobile/notify/get-list-status-menu-notify |
| 18 | 2026-09-17 06:32 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 17 | 2026-09-18 04:40 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 16 | 2026-09-18 07:23 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 16 | 2026-09-17 16:07 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 16 | 2026-09-15 05:10 VN | SUPPERSLOW | 123699 | /api/mobile/notify/get-list-status-menu-notify |
| 16 | 2026-09-14 22:15 VN | SUPPERSLOW | 73445 | /api/mobile/notify/get-list-status-menu-notify |
| 16 | 2026-09-14 09:21 VN | SUPPERSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 15 | 2026-09-16 08:43 VN | SUPPERSLOW | 140945 | /api/mobile/notify/get-list-status-menu-notify |
| 14 | 2026-09-17 13:24 VN | VERYSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 14 | 2026-09-16 10:05 VN | VERYSLOW | 56172 | /api/mobile/notify/get-list-status-menu-notify |
| 13 | 2026-09-15 04:23 VN | VERYSLOW | 15103 | /api/mobile/notify/get-list-status-menu-notify |

### Nguồn cảnh báo trong source
Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Không có — ticket tự tạo bởi hệ thống AI check-performance từ dữ liệu monitoring, không phải báo lỗi theo kịch bản tái hiện tay. -->

## Expected result

- Response time của `POST /api/mobile/notify/get-list-status-menu-notify` ở mức bình thường (không rơi vào SLOWLV1/VERYSLOW/SUPPERSLOW), kể cả khi bot tích luỹ nhiều thông báo chưa đọc.

## Actual result

- Request chậm max 43s, p95 43s, trung bình 12.06s khi bot có nhiều thông báo chưa đọc (xem bảng "Các lần CHẬM NHẤT đã ghi nhận" ở trên).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Không có attachment — issue.attachments rỗng (0). -->

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được theo kịch bản tay trong Redmine — đây là ticket **tự tạo bởi AI check-performance** (monitoring response time), không phải user report hành vi sai. Root cause + cách fix đã được Dev confirm qua đánh giá ảnh hưởng ở file `03-dev-impact.md` (Journal #137336, Fix done). TCs nên tập trung **verify performance sau fix** (response time giảm, không regression giá trị trả về) + **regression impact** trên các mục đếm thông báo liên quan.
- Status Redmine hiện tại: **Fix done - Đợi test**. Priority: Urgent (được AI nâng từ High lên Urgent do dồn dập ≥20 lần chậm/24h — Journal #138067).
- Branch fix (để QA checkout): `sns-line: ai_small_41091` (gốc `release_step_20260827`, commit `9b45dfda09`, 2 file) — đã push.
- ⚠️ **Lưu ý quan trọng về phạm vi**: Journal #138315 (2026-09-25, SAU journal fix #137336 ngày 2026-09-21) gắn thêm 1 endpoint **CÙNG VẤN ĐỀ** vào ticket này: `POST /api/mobile/notify/get-order-history` (ưu tiên tự tính Low, max 20s, p95 12s, 54 lần chậm/11 ngày). Vì endpoint này được gắn vào **sau** khi Dev đã báo fix done, cách fix ở file 03 (chỉ đề cập `getListStatusMenuNotify` + `countUnconfirmNotifyByType` + `getNumberNotifyUnconfirmForEachType`) **chưa rõ có cover `get-order-history` hay không** → cần hỏi lại Dev / kiểm tra branch trước khi coi đây là đã fix xong cho cả 2 endpoint.
- Dev **không verify được bằng EXPLAIN / dữ liệu thật** — MySQL dev (host.docker.internal:3306) từ chối kết nối lúc Dev check. Verify chỉ ở mức lint + sinh SQL + đối chiếu điều kiện lọc. Hiệu quả thực tế (giảm response time) **cần đo lại trên môi trường có dữ liệu thật** (dev/staging có DB, hoặc theo dõi production sau deploy).
- Rủi ro deploy: migration thêm chỉ mục mới (`AddIndexMenuStatusToMobileNotifyTable`) trên bảng `mobile_notify` (bảng lớn, không dọn định kỳ) → khóa bảng một lần khi chạy, **phải chạy giờ thấp điểm**. Index mới cũng tăng chi phí ghi khi insert thông báo (Dev đánh giá chấp nhận được).
- Liên quan ticket #41026 (cùng bảng `mobile_notify`, cùng nhóm API đếm thông báo) — đã ghi nhận trước vấn đề thiếu cột `type` trong index; migration của #41091 có kiểm tra index đã tồn tại chưa nên không xung đột nếu #41026 lên release trước.
- Server phát hiện: step.lme.jp (môi trường theo dõi performance thực tế — không phải dev/staging).

## Dữ liệu định danh ca lỗi

<!-- Ticket performance, không có 1 ca lỗi behavior cụ thể — liệt kê thông tin để dựng env đo performance. Xem đầy đủ các lần chậm ở bảng "Các lần CHẬM NHẤT đã ghi nhận" phía trên. -->

| Mục | Giá trị |
|---|---|
| bot_id | `<không có trong báo cáo AI detect — cần tra theo user_id lúc test>` |
| Friend / user bị ảnh hưởng | `Nhiều user, lặp lại nhiều nhất: 56172; còn: 73445, 123699, 140945, 15103 (tổng 6 user chịu ảnh hưởng trong kỳ 24h, 15 user trong lịch sử dài hạn 5 ngày)` |
| Đối tượng cấu hình | `Bảng mobile_notify (nhật ký thông báo) — bot có nhiều thông báo chưa đọc (unconfirm)` |
| Thời điểm lỗi | `Chậm nhất: 2026-09-18 04:43 VN (43s). Lịch sử: 46 lần chậm/5 ngày từ 2026-09-14 02:21 UTC, đỉnh 21 lần/24h.` |
| Đối chứng | `<không có — ticket tự tạo bởi AI check-performance, chưa có case đối chứng chạy đúng cụ thể>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #137336 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
API lấy trạng thái menu thông báo của app chạy 14 câu đếm riêng lẻ trên bảng nhật ký thông báo (một trong các bảng lớn nhất hệ thống, không dọn định kỳ). Chỉ mục duy nhất dùng được cho nhóm truy vấn này gồm bot - đã đọc - trạng thái gửi - người dùng, KHÔNG có cột loại thông báo, nên mỗi câu đếm phải mở lần lượt từng dòng chưa đọc của bot rồi mới lọc được đúng loại. Một request vì vậy phải đọc lượng dòng gấp 14 lần số thông báo chưa đọc của bot; bot tích luỹ nhiều thông báo chưa đọc thì thời gian phản hồi lên tới hàng chục giây (ghi nhận tối đa 43 giây).

■ 2. CÁCH FIX
Gộp 12 câu đếm thông báo chưa đọc chỉ lọc theo loại thành MỘT câu đếm gộp theo loại (thêm hàm dùng riêng countUnconfirmNotifyByType trong controller thông báo của app), giữ nguyên 2 câu đếm riêng cho loại biểu mẫu (lọc thêm mã sản phẩm) và tiếp thị liên kết (lọc thêm nhóm sự kiện) để không đổi điều kiện cũ — số câu truy vấn mỗi request giảm từ 14 xuống 3, kết quả từng mục menu và tổng badge giữ nguyên. Thêm migration tạo chỉ mục phủ (bot, loại, trạng thái gửi, đã đọc, người dùng) cho bảng thông báo để câu đếm chạy trọn trên chỉ mục thay vì mở từng dòng dữ liệu; migration có kiểm tra chỉ mục đã tồn tại nên chạy lại được và không xung đột nếu nhánh ticket #41026 (chỉ mục 4 cột là tiền tố) lên release trước. Quét ngang: API đếm thông báo chưa đọc theo từng loại còn lại cũng theo mẫu này nhưng nhẹ hơn và đã được chỉ mục mới phục vụ, ghi nhận lại chứ không sửa ngoài phạm vi ticket.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
NotifyController::getListStatusMenuNotify (app/Http/Controllers/Api/NotifyController.php:1133)
NotifyController::countUnconfirmNotifyByType (app/Http/Controllers/Api/NotifyController.php:1091 - hàm mới)
NotifyController::getNumberNotifyUnconfirmForEachType (app/Http/Controllers/Api/NotifyController.php:62 - cùng mẫu, không sửa)
setAppBadgeNotifyCount (app/Helpers/functions.php:4522)
AddIndexMenuStatusToMobileNotifyTable (database/migrations/2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Api/NotifyController.php
   - database/migrations/2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php
 • 4.2 Data ảnh hưởng:
   - mobile_notify — chỉ ĐỌC (đếm), không ghi; thêm 1 chỉ mục mới (bot_id, type, status, is_confirm, user_id): bảng lớn nên chạy migration vào giờ thấp điểm, tăng dung lượng chỉ mục và thêm chi phí ghi nhỏ khi insert thông báo
   - mobile_badge_noitfy — giữ nguyên hành vi: vẫn ghi lại tổng badge của user+bot sau khi đếm (giá trị tính ra không đổi)
   - Không cần recover dữ liệu
 • 4.3 Tính năng liên quan:
   - Notification Settings (FA-006) — API trạng thái menu thông báo của app Elme: giảm số câu đếm và thêm chỉ mục, giá trị highlight từng mục giữ nguyên
   - System Notifications (FS-014) — mục thông báo hệ thống nằm trong cùng câu đếm gộp, giá trị giữ nguyên
   - App badge thông báo (outside glossary) — tổng badge ghi vào bảng badge theo user+bot vẫn tính đúng như trước

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Api/NotifyController.php: No syntax errors detected; php -l database/migrations/2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php: No syntax errors detected; Boot Laravel (Console Kernel) trong worktree + in toSql: câu gộp sinh đúng SQL MySQL 'select `mobile_notify`.`type`, COUNT(*) as total ... where bot_id=? and (user_id is null or user_id=?) and is_confirm=? and status=? and type in (12 mã) group by `mobile_notify`.`type`' — cùng bộ điều kiện với câu đếm cũ, hợp lệ với ONLY_FULL_GROUP_BY; Kiểm tra guard danh sách loại rỗng qua Reflection: trả về mảng rỗng, không chạy query; Đối chiếu danh sách 12 mã loại gộp [2,12,10,11,15,6,8,9,4,13,14,17] với 12 câu đếm cũ: khớp 1-1, không trùng mã, không sót mã (loại 3 biểu mẫu và 16 tiếp thị liên kết vẫn đếm riêng)
   Bằng chứng: MySQL dev (host.docker.internal:3306) đang từ chối kết nối nên KHÔNG chạy được EXPLAIN / tái hiện dữ liệu thật — mọi verify làm ở mức lint + sinh SQL + đối chiếu điều kiện; Chỉ mục hiện có trên bảng thông báo (theo migration của nhánh release): chỉ có mobile_notify_badge_recount_index (bot_id, is_confirm, status, user_id) — không có cột type, đúng như phân tích nguyên nhân; Bài học #41026 (cùng bảng, cùng nhóm API) đã ghi nhận chính xác vấn đề thiếu cột type trong chỉ mục

■ TỰ REVIEW (AI)
Fix đúng gốc: giảm số lần quét bảng nhật ký thông báo trong 1 request (14 → 3 câu) và thêm chỉ mục phủ để câu đếm chạy trọn trên chỉ mục. Điều kiện lọc từng loại giữ nguyên 1-1 với code cũ nên giá trị highlight menu và tổng badge không đổi. Rủi ro chính nằm ở khâu deploy migration trên bảng lớn.
 • Rủi ro / lưu ý khi test:
   - Tạo chỉ mục trên bảng nhật ký lớn khoá bảng một lần khi chạy migration → phải chạy giờ thấp điểm
   - Thêm chỉ mục làm tăng chi phí ghi khi insert thông báo mới (chấp nhận được để đổi lấy API đọc nhanh)
   - Không chạy được EXPLAIN vì MySQL dev đang tắt; hiệu quả thực tế cần đo lại trên môi trường có dữ liệu

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41091 (nhánh gốc release_step_20260827, commit 9b45dfda09, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 11 phút 19 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=60234819-c3f6-416f-a71d-b70d1e608bb4
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41091
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #138315 — ai-exception detect-bug — 2026-09-25:**

```
🔗 Gắn thêm 1 endpoint CÙNG VẤN ĐỀ vào ticket này
check-performance AI — người dùng gắn từ dashboard lúc 2026-09-25 09:07 VN: endpoint dưới đây cùng vấn đề / cùng chức năng với ticket này, xin xử lý (improve) chung trong cùng ticket.

### Endpoint
POST /api/mobile/notify/get-order-history

Độ ưu tiên: Low — căn cứ:
- Mức endpoint "low" (chậm nhất trong kỳ 12s) → Low
Mức: low — xếp theo độ chậm: max 12s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 43
Số lần chậm 24h: 5 (kỳ trước 5, 1h qua 0) — xu hướng flat
Thời gian: max 20s · p95 12s · trung bình 7.4s · median 6s
Phân bố: ≥15s SUPPERSLOW 2 · 10–15s VERYSLOW 3 · 5–10s SLOWLV1 49
User bị ảnh hưởng: 2 (tổng 16)
Server: step.lme.jp — BotId: —
Lần đầu: 2026-09-14 07:39 UTC — Lần cuối: 2026-09-24 23:36 UTC
Lịch sử dài hạn: tổng 54 lần chậm trong 11 ngày, đỉnh 9 lần/24h, chậm nhất 20s, từ 2026-09-14 07:39 UTC

URL mẫu: /api/mobile/notify/get-order-history?page=1 (query param gặp: page)

Các lần CHẬM NHẤT đã ghi nhận:
| Giây | Thời điểm (VN) | Mức | User |
|---|---|---|---|
| 20 | 2026-09-18 05:58 VN | SUPPERSLOW | 51180 |
| 15 | 2026-09-22 00:17 VN | SUPPERSLOW | 10260 |
| 12 | 2026-09-24 13:07 VN | VERYSLOW | 9997 |
| 10 | 2026-09-18 13:40 VN | VERYSLOW | 61303 |
| 10 | 2026-09-16 22:20 VN | VERYSLOW | 9997 |

Lưu ý ưu tiên: endpoint này tự tính ra ưu tiên Low, trong khi ticket đang để Urgent — cân nhắc chỉnh lại độ ưu tiên của ticket cho khớp phần nặng nhất.

Các endpoint đang gắn chung ticket này:
- POST /api/mobile/notify/get-list-status-menu-notify
```
