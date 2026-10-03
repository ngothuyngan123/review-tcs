# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41195 — [AI][Performance] POST /ajax/v2/landing/get-init-detail-landing chậm max 398s (11 lần/24h)` |
| Module / Màn hình | QR Code Action / Landing (FA-017) — màn 「QRコードアクション（詳細データ）」 Chi tiết dữ liệu QR/Trang đích (endpoint `POST /ajax/v2/landing/get-init-detail-landing`, 3 tab: 数値情報 / 友だち一覧 / LP連携 + xuất CSV). Liên đới: Popup (FA-018) — tab2 màn Chi tiết lượt bấm popup (`PopupAjaxController::initDataDetailClick`, cùng pattern lỗi collation). |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

**Endpoint:** `POST /ajax/v2/landing/get-init-detail-landing`

- **Mức:** high — xếp theo độ chậm: max 105s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 77
- **Số lần chậm 24h:** 11 (kỳ trước 10, 1h qua 1) — xu hướng flat
- **Thời gian:** max 398s · p95 105s · trung bình 16.91s · median 8s
- **Phân bố:** ≥15s SUPPERSLOW 14 · 10–15s VERYSLOW 6 · 5–10s SLOWLV1 19
- **User bị ảnh hưởng:** 5 (tổng 12)
- **Server:** step.lme.jp — **BotId:** 30529, 59487, 115369, 198829, 2677, 70639, 71588, 9514, 15111, 153361
- **Lần đầu:** 2026-09-14 13:12 UTC — **Lần cuối:** 2026-09-21 08:34 UTC
- **Lịch sử dài hạn:** tổng 39 lần chậm trong 7 ngày, đỉnh 13 lần/24h, chậm nhất 398s, từ 2026-09-14 13:12 UTC

**Vì sao ưu tiên này**

- Độ chậm: p95 105s — treo gần như timeout (+45 điểm)
- Tần suất: 11 lần/24h (+10 điểm)
- User ảnh hưởng: 5 user bị chậm (+10 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Tương đương 24h trước (+0 điểm)

**URL mẫu:** `/ajax/v2/landing/get-init-detail-landing`

**Các lần CHẬM NHẤT đã ghi nhận**

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 398 | 2026-09-20 12:17 VN | SUPPERSLOW | 114949 | /ajax/v2/landing/get-init-detail-landing |
| 121 | 2026-09-20 08:35 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 109 | 2026-09-20 09:27 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 105 | 2026-09-21 00:22 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 105 | 2026-09-20 08:21 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 97 | 2026-09-20 08:29 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 89 | 2026-09-20 08:27 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 82 | 2026-09-20 08:22 VN | SUPPERSLOW | 175998 | /ajax/v2/landing/get-init-detail-landing |
| 57 | 2026-09-20 15:47 VN | SUPPERSLOW | 165836 | /ajax/v2/landing/get-init-detail-landing |
| 50 | 2026-09-20 15:47 VN | SUPPERSLOW | 165836 | /ajax/v2/landing/get-init-detail-landing |
| 28 | 2026-09-18 05:47 VN | SUPPERSLOW | 23036 | /ajax/v2/landing/get-init-detail-landing |
| 28 | 2026-09-14 20:12 VN | SUPPERSLOW | 23036 | /ajax/v2/landing/get-init-detail-landing |
| 27 | 2026-09-16 14:54 VN | SUPPERSLOW | 10000 | /ajax/v2/landing/get-init-detail-landing |
| 18 | 2026-09-16 14:54 VN | SUPPERSLOW | 10000 | /ajax/v2/landing/get-init-detail-landing |
| 12 | 2026-09-21 15:34 VN | VERYSLOW | 10000 | /ajax/v2/landing/get-init-detail-landing |

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

<!-- Redmine #41195 KHÔNG có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (Steps / Expected / Actual trống) — ticket do hệ thống AI detect performance tự sinh từ log request chậm. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** (chỉ mục + rewrite query) + **regression** 3 tab của màn Chi tiết dữ liệu QR/Landing.
- **Không phải lỗi cố định 100%** — chỉ phát sinh với **trang đích (landing) có lượng click lớn** (quét toàn bảng log `detail_landing_click` dùng chung toàn hệ thống). Trang đích ít click không tái hiện được độ chậm.
- **Môi trường phát hiện: production `step.lme.jp`.** ⚠️ **RULE-08**: không kết luận hiệu năng từ local/staging — Dev nhiều lần ghi **chưa chạy được EXPLAIN trên DB dev** (MySQL `host.docker.internal:3306` connection refused từ container).
- ⚠️ **Ticket đã qua NHIỀU vòng auto-fixbug** (6 journal fix, 2026-09-21 → 2026-09-28) — vòng đầu thêm 3 migration index, các vòng sau lần lượt: bỏ bớt index (đã có sẵn trên production), rewrite query (`NOT EXISTS` thay derived table), thêm rồi **tinh chỉnh lại** cách xử lý lệch collation `line_id` (utf8mb4 vs utf8) giữa `detail_landing_click` và `line_user`, và áp dụng case tương tự sang `PopupAjaxController` (FA-018). **File `03-dev-impact.md` chỉ chép Journal MỚI NHẤT (#138926, 2026-09-28)** — là bản tổng hợp/cuối cùng, đã bao gồm và ghi đè các vòng trước; các vòng trước để lại trong Journal note bên dưới để đối chiếu lịch sử.
- ⚠️ **Còn 1 subtask liên quan chưa xử lý xong tại thời điểm fetch**: ticket **#41667** (tester đo lại 352.3s → 0.2s cho ô 「ブロック」) đã được xử lý ở vòng fix cuối (#138926) nhưng **Studio task #333 vẫn còn TC fail/error/chưa chạy liên quan tới #41667** (xem cảnh báo ở mục "Nguồn TC" trong `04-tc-list.md`) — cần re-run trước khi kết luận Pass.
- Dev nhiều lần lưu ý: kết quả tối ưu **phụ thuộc production THỰC SỰ có sẵn** các chỉ mục `detail_landing_click(landing_id, time_click)`, `detail_landing_click(bot_id, line_id, landing_id)`, `line_user(line_id)` và đúng collation `utf8_unicode_ci` cho `line_user.line_id` — Dev không tự thêm migration cho các bảng lớn (log ~206k+ dòng / `line_user` ~26 triệu dòng), đề nghị DBA `SHOW INDEX` / `SHOW FULL COLUMNS` xác nhận trước release.

## Journal / note từ Redmine (nguyên văn)

**Journal #137424 — AI LME Fix bug — 2026-09-21 (vòng fix 1 — SUPERSEDED, xem #138926 để có bản mới nhất):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
■ 1. NGUYÊN NHÂN: Ba nút nghẽn — (1) tab Trang đích ghép bảng lượt mở với bảng nhật ký click qua collect_id không có chỉ mục, ghép nặng chạy 3 lần/request; (2) thống kê ngày hôm nay bọc DATE() nên không dùng được chỉ mục, chạy ở MỌI lần mở màn; (3) tab danh sách bạn bè ghép mốc thêm bạn bằng 2 vòng lặp lồng nhau (số dòng × số bạn) → CSV treo lâu.
■ 2. CÁCH FIX (vòng 1): (1) Thêm migration 3 chỉ mục: detail_landing_click(collect_id), detail_landing_click(landing_id, time_click), landing_page_poster_url(code). (2) Đổi DATE(time_click)=hôm nay sang khoảng nửa mở [00:00:00, 00:00:00 ngày mai). (3) Thay 2 vòng lặp lồng nhau bằng bảng tra theo line_id. Verify: harness so sánh thuật toán cũ/mới trên 300 bộ dữ liệu + 9 mốc biên, khớp 100%. Branch: ai_small_41195 (gốc release_step_20260827), commit a65732db21, 2 file.
```

**Journal #138071 — ai-exception detect-bug — 2026-09-24:**

```
check-performance: bổ sung độ ưu tiên theo quy định 2.1 → Immediate
* Mức endpoint "high" (chậm nhất trong kỳ 398s) → High
* ⬆️ Nâng lên Urgent: Có request treo ≥ 60s
* ⬆️ Nâng lên Immediate: Có request treo ≥ 300s
```

**Journal #138766 — AI LME Fix bug — 2026-09-26 (vòng fix 2 — SUPERSEDED):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
[SPEC BỔ SUNG] Migration KHÔNG tạo detail_landing_click(collect_id) và landing_page_poster_url(code) nữa vì DB thật đã có sẵn chỉ mục (hasIndex chỉ dò theo TÊN nên không phát hiện được chỉ mục sẵn có mang tên khác). Câu đếm totalBlock (tab2): QUAY LẠI correlated NOT EXISTS đúng đoạn code human chỉ định, bỏ derived table pre-aggregate mà #32481 đã thay vào (derived table buộc GROUP BY toàn bộ click action=2 của cả bot, rất nặng). Branch: ai_small_41195, commit 8068076166.
```

**Journal #138769 — AI LME Fix bug — 2026-09-26 (vòng fix 3 — SUPERSEDED):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
[SPEC BỔ SUNG] Gỡ nút nghẽn LỆCH COLLATION ở phép ghép detail_landing_click.line_id (utf8mb4_unicode_ci) = line_user.line_id (utf8_unicode_ci): MySQL phải nâng vế utf8 (cột CÓ chỉ mục) lên utf8mb4 cho TỪNG dòng ⇒ chỉ mục line_user.line_id vô hiệu. Sửa: hạ vế detail_landing_click.line_id về utf8 bằng hằng DetailLandingClick::JOIN_LINE_ID_UTF8 = "CONVERT(detail_landing_click.line_id USING utf8) COLLATE utf8_unicode_ci", dùng ở 3 chỗ ghép line_user. CẦN DEV/DBA XÁC NHẬN line_user.line_id có chỉ mục + đúng collation utf8_unicode_ci trên production. Branch: ai_small_41195, commit 5783fd952d, 3 file.
```

**Journal #138784 — AI LME Fix bug — 2026-09-26 (vòng fix 4 — SUPERSEDED):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
[SPEC BỔ SUNG] XOÁ HẲN migration 2026_09_21_100000 theo xác nhận human: chỉ mục cuối cùng còn lại (landing_id, time_click) DB thật ĐÃ CÓ SẴN ⇒ migration chỉ còn nguy cơ TẠO TRÙNG chỉ mục. Sau bước này branch KHÔNG còn thay đổi schema nào — diff gộp chỉ còn 2 file PHP. Branch: ai_small_41195, commit 3ec0049f52, 2 file.
```

**Journal #138821 — AI LME Fix bug — 2026-09-26 (vòng fix 5 — SUPERSEDED):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
[SPEC BỔ SUNG] Áp fix collation sang CÁC CASE TƯƠNG TỰ theo 4 vị trí human liệt kê: SỬA app/Http/Controllers/Ajax/PopupAjaxController.php:643 (initDataDetailClick, tab2 màn Chi tiết lượt bấm Popup FA-018) dùng lại hằng JOIN_LINE_ID_UTF8; KHÔNG SỬA (cố ý) QrActionHistoryRepository.php:25 và NotifyController.php:190 vì ở đó detail_landing_click là bảng ĐƯỢC TRA (không phải bảng lái) nên bọc CONVERT sẽ làm HỎNG chỉ mục đang dùng. Grep toàn repo xác nhận đúng 5 vị trí ghép detail_landing_click ↔ line_user, không sót. Branch: ai_small_41195, commit e942090680, 3 file.
```

**Journal #138926 — AI LME Fix bug — 2026-09-28 (vòng fix 6 — BẢN MỚI NHẤT, xem chi tiết đầy đủ ở `03-dev-impact.md`):**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
[Bổ sung #41667 — nguyên nhân tab 友だち一覧 vẫn 352.3s sau bản tối ưu vòng 5] Vòng fix 2026-09-26 áp CONVERT(...USING utf8) COLLATE utf8_unicode_ci cho MỌI chỗ ghép detail_landing_click ↔ line_user, kể cả câu đếm số bạn bị chặn (totalBlock). Ở câu đếm đó, điều kiện lọc conversation.is_blocked=1 mới là điều kiện chọn lọc nhất nên MySQL lái từ conversation → line_user (theo khóa chính) rồi TRA detail_landing_click theo line_id; bọc CONVERT lên chính cột được tra làm chỉ mục detail_landing_click_bot_line_landing_index (bot_id, line_id(64), landing_id) vô hiệu ⇒ bảng log về type=ALL 206.859 dòng (Using join buffer), quét lại cho từng bạn bị chặn.
[SPEC BỔ SUNG 2026-09-28 — subtask #41667] Câu đếm 「ブロック」: BỎ CONVERT khỏi điều kiện ghép line_user CỦA CHÍNH câu đếm này, quay lại so thẳng detail_landing_click.line_id = line_user.line_id (giữ nguyên NOT EXISTS). Tester đo: 352.3s → 0.2s, EXPLAIN type=ALL → type=ref, kết quả giữ nguyên 545. Nhánh CÓ từ khóa vẫn kế thừa CONVERT từ $queryDetail (cần cho câu danh sách) nên thêm điều kiện so thẳng TƯƠNG ĐƯƠNG ở WHERE để mở thêm đường bám chỉ mục. Docblock hằng JOIN_LINE_ID_UTF8 bổ sung luật dùng theo CHIỀU (chỉ CONVERT khi detail_landing_click là bảng lái). Branch: ai_small_41195 (gốc release_step_20260827), commit 32138de948, 3 file. [đã push]
```
