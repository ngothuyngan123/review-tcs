# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40948 — [AI][Performance] POST /ajax/init-data-filter chậm max 52s (12 lần/24h)` |
| Module / Màn hình | Friend Filter (SC-003) — modal lọc bạn bè dùng chung `絞込み条件モーダル`, endpoint `POST /ajax/init-data-filter`. Các màn gọi tới: CSV管理 (FA-014) · クロス分析 phân tích chéo (FA-024) · チャット管理 CSV出力 · 一斉配信 (FA-008) · 自動応答 Auto Reply (FA-003) · Action Schedule (FA-016) · リッチメニュー (FA-004) · 3 màn lịch gửi sau đặt chỗ (カレンダー / カレンダーサロン コース / カレンダーサロン スタッフ) |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

**Endpoint:** `POST /ajax/init-data-filter`

- **Mức:** high — xếp theo độ chậm: max 52s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 74
- **Số lần chậm 24h:** 12 (kỳ trước 0, 1h qua 5) — xu hướng new
- **Thời gian:** max 52s · p95 52s · trung bình 19.08s · median 11s
- **Phân bố:** ≥15s SUPPERSLOW 4 · 10–15s VERYSLOW 3 · 5–10s SLOWLV1 5
- **User bị ảnh hưởng:** 4 (tổng 4)
- **Server:** step.lme.jp — **BotId:** 107152, 196392, 41734, 109213
- **Lần đầu:** 2026-09-14 02:04 UTC — **Lần cuối:** 2026-09-14 08:52 UTC
- **Lịch sử dài hạn:** tổng 12 lần chậm trong 1 ngày, đỉnh 12 lần/24h, chậm nhất 52s, từ 2026-09-14 02:04 UTC

**Vì sao ưu tiên này**

- Độ chậm: p95 52s — cực chậm (+38 điểm)
- Tần suất: 12 lần/24h (+10 điểm)
- User ảnh hưởng: 4 user bị chậm (+6 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Mới xuất hiện (kỳ trước 0 lần, nay 12) (+8 điểm)

**URL mẫu:** `/ajax/init-data-filter`

**Các lần CHẬM NHẤT đã ghi nhận**

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 52 | 2026-09-14 09:07 VN | SUPPERSLOW | 73506 | /ajax/init-data-filter |
| 45 | 2026-09-14 09:04 VN | SUPPERSLOW | 73506 | /ajax/init-data-filter |
| 44 | 2026-09-14 09:05 VN | SUPPERSLOW | 73506 | /ajax/init-data-filter |
| 15 | 2026-09-14 15:52 VN | SUPPERSLOW | 145285 | /ajax/init-data-filter |
| 13 | 2026-09-14 15:41 VN | VERYSLOW | 145285 | /ajax/init-data-filter |
| 11 | 2026-09-14 15:28 VN | VERYSLOW | 145285 | /ajax/init-data-filter |
| 11 | 2026-09-14 09:25 VN | VERYSLOW | 145285 | /ajax/init-data-filter |
| 9 | 2026-09-14 15:48 VN | SLOWLV1 | 75014 | /ajax/init-data-filter |
| 8 | 2026-09-14 15:41 VN | SLOWLV1 | 145285 | /ajax/init-data-filter |
| 8 | 2026-09-14 14:00 VN | SLOWLV1 | 125936 | /ajax/init-data-filter |
| 7 | 2026-09-14 09:56 VN | SLOWLV1 | 125936 | /ajax/init-data-filter |
| 6 | 2026-09-14 14:00 VN | SLOWLV1 | 125936 | /ajax/init-data-filter |

**Nguồn cảnh báo trong source**

Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket do AI detect performance tự sinh từ log request chậm. -->

## Expected result

<!-- (trống — Redmine không ghi) -->

## Actual result

<!-- (trống — dữ liệu đo nằm ở bảng "Các lần CHẬM NHẤT đã ghi nhận" phía trên) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40948 KHÔNG có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (Steps / Expected / Actual trống) — ticket do hệ thống AI detect performance tự sinh từ log request chậm. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** (câu lọc chạy 1 lần thay vì 2) + **regression** các màn gọi modal lọc bạn bè.
- **Không phải lỗi 100%** — chỉ phát sinh với **bot nhiều bạn bè** + **bộ lọc rỗng** (quét toàn bộ bạn bè). Bot ít friend không tái hiện được độ chậm.
- **Môi trường phát hiện: production `step.lme.jp`.** Đo lại thời gian phản hồi phải làm trên môi trường có dữ liệu lớn — ⚠️ **RULE-08**: không kết luận hiệu năng từ local/dev. Dev ghi rõ **chưa đo được thời gian thực tế** (MySQL dev không kết nối được).
- Nhánh fix chép **nguyên văn** hàm `countFilterResult` + hằng danh sách màn từ **ticket #40986** (đang chờ review, cùng file `FilterController.php`) → rủi ro **xung đột merge** nếu #40986 bị sửa nội dung trong lúc review.
- Sau fix: các màn **ngoài danh sách trắng** nhận `line_user_ids` **rỗng** → đây là vùng regression chính cần cover.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `107152`, `196392`, `41734`, `109213` (bot bị ghi nhận chậm) |
| User bị ảnh hưởng | `73506` (52s / 45s / 44s) · `145285` · `75014` · `125936` |
| Đối tượng cấu hình | Modal lọc bạn bè dùng chung — **bộ lọc rỗng** (quét toàn bộ bạn bè) trên bot nhiều friend |
| Thời điểm lỗi | 2026-09-14 02:04 UTC → 2026-09-14 08:52 UTC (chậm nhất 2026-09-14 09:07 VN — 52s) |
| Đối chứng | Bot ít bạn bè / bộ lọc có điều kiện hẹp → request nhanh bình thường |

## Journal / note từ Redmine (nguyên văn)

**Journal #137322 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Endpoint /ajax/init-data-filter chạy câu truy vấn lọc bạn bè (rất nặng) HAI lần cho mỗi request: một lần đếm số người, một lần nữa lấy toàn bộ danh sách ID bạn bè rồi dựng thành đối tượng và đóng gói ra JSON. Danh sách ID đó lại được trả cho gần như mọi màn hình gọi tới, trong khi chỉ màn tạo file CSV và phân tích chéo mới thực sự đọc nó. Bot nhiều bạn bè và bộ lọc rỗng (quét toàn bộ bạn bè) thì chi phí gấp đôi này kéo request lên hàng chục giây.

■ 2. CÁCH FIX
Trong FilterController::initDataFilter, thay 3 cặp lệnh đếm-rồi-lấy-toàn-bộ-ID bằng hàm dùng chung countFilterResult: chạy câu lọc đúng MỘT lần, chỉ lấy danh sách ID cho 5 loại màn thực sự đọc nó (tạo file CSV, phân tích chéo, 3 màn cấu hình gửi tin sau khi đặt lịch), còn lại chỉ đếm. Hàm countFilterResult và hằng danh sách màn lấy nguyên từ ticket #40986 (đang chờ review) để hai nhánh gộp lại không đụng nhau. Quét ngang: cùng mẫu lỗi còn ở saveFilterV2 (đã xử lý ở #40986) và ở API lọc phía mobile (ngoài phạm vi).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FilterController::initDataFilter (app/Http/Controllers/Basic/FilterController.php)
FilterController::countFilterResult (app/Http/Controllers/Basic/FilterController.php)
FilterController::saveFilterV2 (app/Http/Controllers/Basic/FilterController.php)
FilterController::countAllFriend (app/Http/Controllers/Basic/FilterController.php)
Conversation::advanceFilterPost (app/Conversation.php)
initDataFilter (public/js/friendlist/modal_filter_v2.js)
initDataFilter (public/js/talk_list/modal_filter_message.js)
getDataFilter (public/js/schedules/plan.js)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FilterController.php
 • 4.2 Data ảnh hưởng:
   - Không có — thay đổi chỉ ở tầng đọc dữ liệu, không ghi/sửa bảng nào
 • 4.3 Tính năng liên quan:
   - Friend Filter (SC-003) — modal lọc bạn bè dùng chung: nạp lại điều kiện lọc và đếm số người nay chỉ chạy truy vấn 1 lần
   - CSV Management (FA-014) — màn tạo file CSV vẫn nhận đủ danh sách ID bạn bè như cũ
   - Cross Analysis (FA-024) — màn phân tích chéo vẫn nhận đủ danh sách ID bạn bè như cũ
   - Auto Reply (FA-003) — chỉ dùng số người lọc được, nay không còn nhận mảng ID thừa
   - Action Schedule (FA-016) — chỉ dùng số người lọc được, nay không còn nhận mảng ID thừa
   - Rich Menu (FA-004) — màn cấu hình hiển thị rich menu chỉ dùng số người lọc được
   - Broadcast (FA-008) — không đổi (trước nay vẫn không nhận mảng ID)

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/FilterController.php: No syntax errors detected; Harness Laravel thật (boot bootstrap/app.php + vendor): câu SQL của cách cũ select('bot_line_user.line_user_id')->get() và cách mới pluck() GIỐNG NHAU (builder có columns = NULL nên pluck áp đúng cột); Harness: stripTableForPluck('bot_line_user.line_user_id') = 'line_user_id' nên mảng trả ra [['line_user_id'=>id],...] trùng khớp định dạng cũ, giao diện không phải sửa; Harness: BotLineUser không có mutator/cast/date cho cột này nên pluck bỏ qua bước dựng model Eloquent; Harness: builder do advanceFilterPost trả về có groups=NULL, distinct=false, limit=NULL (cả khi bộ lọc rỗng lẫn khi có điều kiện AND/OR) nên count(*) bằng đúng số dòng lấy về — suy số lượng từ mảng ID là tương đương; Chưa chạy được unit test / kiểm chứng trên dữ liệu thật: MySQL dev không kết nối được (Connection refused)
   Bằng chứng: Chỉ 2 chỗ trong giao diện đọc response.line_user_ids của endpoint này: public/js/friendlist/modal_filter_v2.js (csv_create_download_file, cross_analysis) và public/js/talk_list/modal_filter_message.js (cùng 2 loại) — cả 2 đều nằm trong danh sách trắng; Các màn lịch (calendar-*-setting-status-send-after-booking) đọc line_user_ids từ response của save-filter-v2 chứ không phải endpoint này, nhưng vẫn giữ trong danh sách trắng cho an toàn; public/js/schedules/plan.js lưu cả response nhưng chỉ đọc number_filter

■ TỰ REVIEW (AI)
Thay 3 chỗ chạy trùng truy vấn trong initDataFilter bằng hàm dùng chung countFilterResult. Kết quả trả về giữ nguyên cho mọi màn thực sự đọc dữ liệu: number_filter không đổi (đã kiểm builder không có groupBy/distinct/limit nên count(*) bằng số dòng), line_user_ids giữ nguyên định dạng cho 5 loại màn trong danh sách trắng và rỗng cho các màn vốn không đọc tới.
 • Rủi ro / lưu ý khi test:
   - Hàm countFilterResult và hằng danh sách màn được chép NGUYÊN VĂN từ nhánh #40986 (cùng file, chưa merge vào release). Nếu cả hai nhánh cùng lên thì git gộp sạch vì phần thêm giống hệt nhau, nhưng nếu #40986 bị sửa nội dung trong lúc review thì sẽ xung đột ở khối này — người duyệt cần biết để gộp thủ công.
   - Các màn không nằm trong danh sách trắng nay nhận line_user_ids rỗng. Đã rà toàn bộ public/js và resources/views, không nơi nào đọc trường này ngoài 2 màn CSV và phân tích chéo; nếu sau này có màn mới cần, phải thêm loại màn đó vào hằng danh sách trắng.
   - Chưa đo được thời gian thực tế vì MySQL dev không kết nối được — mức cải thiện suy từ việc giảm từ 2 lượt chạy truy vấn nặng xuống 1 và bỏ hẳn việc tải toàn bộ ID cho phần lớn màn.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40948 (nhánh gốc release_step_20260827, commit 62edff4a8e, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 8 phút 14 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=bcf4ab39-0dfd-49e6-b2cc-f66436a7b603
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40948
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
