# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41194 — [AI][Performance] DELETE /basic/calendar-salon/{id}/booking/delete chậm max 1534s (12 lần/24h)` |
| Module / Màn hình | Đặt lịch Salon (FA-020) — API xoá đặt lịch Salon `DELETE /basic/calendar-salon/{id}/booking/delete` (nút 「この予約を削除する」 → 「削除する」 trong modal chi tiết đặt lịch, tab 「予約カレンダー」). Feature Studio: `calendar-salon`. |

## Mô tả bug (bản dịch tiếng Việt)

Ticket **tự tạo bởi hệ thống check-performance AI** (từ report request chậm bắn lên Chatwork room 417532006), **không phải khách hàng báo trực tiếp**. Không có "Steps to reproduce" thủ công — đây là cảnh báo đo hiệu năng tổng hợp từ log request thật.

**Endpoint:** `DELETE /basic/calendar-salon/{id}/booking/delete`

- Mức: **high** — xếp theo độ chậm (max 101s trong kỳ; >30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 73.
- Số lần chậm 24h: **12** (kỳ trước 2, 1h qua 0) — xu hướng **tăng**.
- Thời gian: **max 1534s** · p95 101s · trung bình 88.42s · median 85s.
- Phân bố: ≥15s SUPPERSLOW **13** · 10–15s VERYSLOW **0** · 5–10s SLOWLV1 **14**.
- User bị ảnh hưởng: 1 (tổng 6).
- Server: `step.lme.jp` — BotId: `139254, 133095, 181700, 100683, 15111, 97320`.
- Lần đầu: 2026-09-14 02:13 UTC — Lần cuối: 2026-09-20 15:44 UTC.
- Lịch sử dài hạn: tổng 27 lần chậm trong 5 ngày, đỉnh 14 lần/24h, chậm nhất 1534s, từ 2026-09-14 02:13 UTC.

**Vì sao ưu tiên này:**
- Độ chậm: p95 101s — treo gần như timeout (+45 điểm).
- Tần suất: 12 lần/24h (+10 điểm).
- User ảnh hưởng: 1 user bị chậm (+3 điểm).
- Độ mới: xảy ra trong 24h qua (+5 điểm).
- Xu hướng: tăng 6× so với 24h trước (+10 điểm).
- Journal #138070 (2026-09-24, ai-exception detect-bug): nâng độ ưu tiên theo quy định 2.1 → **Immediate** (có request treo ≥300s → coi như endpoint chết, cần xử lý ngay).

**URL mẫu:** `/basic/calendar-salon/8571/booking/delete` · `/basic/calendar-salon/16294/booking/delete` · `/basic/calendar-salon/13090/booking/delete` · `/basic/calendar-salon/9043/booking/delete` · `/basic/calendar-salon/31209/booking/delete`.

**Các lần chậm nhất đã ghi nhận** (trích bảng gốc — xem đầy đủ trên Redmine):

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 1534 | 2026-09-20 08:52 | SUPPERSLOW | 54807 | /basic/calendar-salon/15294/booking/delete |
| 101 | 2026-09-20 22:43 | SUPPERSLOW | 73445 | /basic/calendar-salon/17244/booking/delete |
| 99 | 2026-09-20 22:44 | SUPPERSLOW | 73445 | /basic/calendar-salon/17244/booking/delete |
| 97 | 2026-09-20 21:06 | SUPPERSLOW | 73445 | /basic/calendar-salon/13791/booking/delete |
| 92 | 2026-09-20 22:24 | SUPPERSLOW | 73445 | /basic/calendar-salon/30951/booking/delete |
| 9 | 2026-09-18 09:06 | SLOWLV1 | 65782 | /basic/calendar-salon/7254/booking/delete |
| 8 | 2026-09-17 11:23 | SLOWLV1 | 117972 | /basic/calendar-salon/16294/booking/delete |

**Nguồn cảnh báo trong source:** Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

⚠️ Không có steps thủ công — ticket do AI check-performance phát hiện qua thống kê thời gian request thật, không phải khách hàng report theo flow UI cụ thể. Theo đánh giá của Dev (journal, xem `03-dev-impact.md`), độ chậm phụ thuộc **khối lượng dữ liệu của bot** (số thông báo chưa đọc tích luỹ trong `mobile_notify` + số user nhận badge của bot), không phải 1 thao tác đơn lẻ nào tái hiện được 100% trên data rỗng.

Dev đã đánh giá nguyên nhân qua 3 vòng điều tra (journal #137527 → #138070 → #138767) và sửa theo hướng: đẩy bước đếm lại badge thông báo (`recountAppBadgeNotify`) chạy nền qua hàng đợi `database`/`default` thay vì có thể chạy đồng bộ trong request khi `QUEUE_DRIVER=sync`. Xem chi tiết ở `03-dev-impact.md`.

## Expected result

- Request `DELETE /basic/calendar-salon/{id}/booking/delete` hoàn tất nhanh, không phụ thuộc số thông báo chưa đọc hay số user của bot (ngưỡng tham chiếu theo mức SLOWLV1 của hệ thống: **dưới 5 giây**).
- Việc đếm lại badge thông báo app luôn chạy **ngoài request** (qua hàng đợi), ở **mọi môi trường** kể cả khi `QUEUE_DRIVER=sync`.

## Actual result

- Request xoá đặt lịch Salon từng chậm tới **1534 giây** (tối đa), p95 **101 giây**, lặp lại **12 lần/24h** và có xu hướng tăng — gần như timeout, ảnh hưởng tới user thao tác trên bot có nhiều thông báo tích luỹ.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

Không có attachment trên Redmine #41194 (0 attachment) — log request chậm đã trích nguyên văn ở "Mô tả bug" phía trên (lấy từ description gốc, hệ thống check-performance AI tự log).

## Ghi chú thêm của Leader

- ⚠️ Ticket do **AI check-performance tự tạo** từ thống kê request chậm, không phải CS/khách hàng báo — không có bước tái hiện thủ công, không có screenshot/video.
- Môi trường phát hiện: **Production** (`step.lme.jp`).
- Ticket status hiện tại: `Fix done - Đợi test`. Dev đã fix **3 lần** trên cùng branch (xem `03-dev-impact.md` để hiểu rõ lần 1 đã bị gỡ ở lần 3):
  1. **Lần 1** (2026-09-22, journal #137527): thêm migration tạo chỉ mục `salon_booking_id` cho bảng `mobile_notify`.
  2. **Lần 2** (2026-09-26, journal #138767 mục 1): phát hiện thêm nguyên nhân thật — job đếm lại badge (`recountAppBadgeNotify`) là **chỗ DUY NHẤT trong repo dispatch job không ghim connection/queue**, nên ở môi trường `QUEUE_DRIVER=sync` toàn bộ vòng đếm chạy **đồng bộ trong request**. Fix: ghim `connection('database')->queue('default')` cho cả 30 chỗ gọi.
  3. **Lần 3** (2026-09-26, cùng journal): **XOÁ hẳn migration của lần 1** vì Dev cho rằng "DB thật đã có sẵn chỉ mục `salon_booking_id`" nên ALTER TABLE là thừa.
- 🔴 **CẢNH BÁO QUAN TRỌNG — phát hiện từ TC Studio, mâu thuẫn trực tiếp với giả định của Dev ở lần 3**: Redmine **#41979** (ticket mới, status `New`, severity Medium, tạo 2026-10-03 bởi AI Auto test LME từ TC Studio `NEW-12`/`NEW-5` của chính task #41194 này) ghi nhận: **`SHOW INDEX FROM mobile_notify` trên DB test KHÔNG có bất kỳ chỉ mục nào bắt đầu bằng `salon_booking_id`** — chỉ có `PRIMARY(id)` và `mobile_notify_badge_recount_index(bot_id, is_confirm, status, user_id)`; `EXPLAIN` câu xoá thông báo chọn `mobile_notify_badge_recount_index` (theo `bot_id`), **không phải chỉ mục theo `salon_booking_id`** — tái hiện lại 2 lần độc lập (run #2588, #2596), kiểm chứng thêm bằng `mysql` CLI trực tiếp. Nếu môi trường step/production **cũng thiếu** chỉ mục này giống DB test thì câu xoá thông báo trong luồng xoá đặt lịch **vẫn quét/khoá cả dải thông báo chưa đọc của bot như trước khi fix** — tức là **phần gốc rễ chậm nhất (so với lần 1) có thể CHƯA được giải quyết thật sự**, chỉ phần đếm badge (lần 2) là chắc chắn đã ra khỏi request. TC `NEW-12` (kiểm chỉ mục) đã **FAIL**, TC `NEW-5` (đo hiệu năng end-to-end) bị **BLOCK/skip** vì cùng nguyên nhân. **Cần Dev/DBA xác nhận lại trên step/production trước khi đóng ticket** — không chỉ tin theo lời khai "DB đã có sẵn" trong journal lần 3.
- Branch fix: `ai_small_41194` (gốc `release_step_20260827`, commit `81f4db9ab3` — trạng thái SAU lần 3, 3 file, 54 dòng thêm/1 dòng xoá). Toàn bộ nội dung "Đánh giá ảnh hưởng" đã chuyển sang `03-dev-impact.md`.
- Studio đã có task review-ready cho ticket này (task **#348**, feature `calendar-salon`, 17 TC do AI sinh: **13 Đạt / 1 Không đạt (NEW-12) / 3 chưa có kết luận (NEW-5, NEW-16, NEW-17)** — xem `04-tc-list.md`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `139254, 133095, 181700, 100683, 15111, 97320` |
| User bị ảnh hưởng (mẫu) | `54807` (case chậm nhất 1534s) · `73445` (6 lần SUPPERSLOW 80–101s) |
| Đối tượng cấu hình | Đặt lịch Salon (mẫu): `8571`, `16294`, `13090`, `9043`, `31209`, `15294`, `17244`, `13791`, `30951`, `7254` |
| Thời điểm lỗi | Chậm nhất: `2026-09-20 08:52 VN` (1534s); cụm chậm dày nhất: `2026-09-20 21:06–22:44 VN` (7 lần SUPPERSLOW của user 73445) |
| Đối chứng | Không có case chạy đúng (<5s) được ghi trong ticket để so sánh trực tiếp — chỉ có phân bố SLOWLV1 (5–10s, 14 lần) làm mốc thấp nhất đã cảnh báo |

## Journal / note từ Redmine (nguyên văn)

**Journal #137527 — AI LME Fix bug — 2026-09-22:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
(Lần 1 — đã bị GỠ ở lần 3, xem Journal #138767. Giữ nguyên văn để đối chiếu lịch sử.)
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi xoá một đặt lịch Salon, hệ thống chạy thêm câu xoá thông báo chưa đọc của đúng đặt lịch đó trên bảng nhật ký thông báo (mobile_notify). Bảng này không có chỉ mục nào chứa cột mã đặt lịch Salon, nên MySQL chỉ thu hẹp được tới dải thông báo chưa đọc của bot rồi phải mở và khoá từng dòng để lọc. Bảng nhật ký không dọn định kỳ và chứa cả thông báo tin nhắn, nên bot tích luỹ nhiều thông báo thì mỗi lần xoá quét hàng trăm nghìn dòng và tranh khoá với luồng ghi thông báo mới, kéo request lên hàng chục giây tới hàng phút.

■ 2. CÁCH FIX
Thêm migration 2026_09_21_110000 tạo chỉ mục mobile_notify_salon_booking_index trên cột mã đặt lịch Salon (salon_booking_id) của bảng nhật ký thông báo...

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41194 (nhánh gốc release_step_20260827, commit fbeded2efb, 2 file)  [đã push]
```

> (Đã rút gọn — nội dung đầy đủ ở `03-dev-impact.md` mục "Lịch sử 3 lần fix".)

**Journal #138070 — ai-exception detect-bug — 2026-09-24:**

```
check-performance: bổ sung độ ưu tiên theo quy định 2.1 → *Immediate*
* Mức endpoint "high" (chậm nhất trong kỳ 1534s) → High
* ⬆️ Nâng lên Urgent: Có request treo ≥ 60s — user gần như chắc chắn bỏ cuộc / timeout
* ⬆️ Nâng lên Immediate: Có request treo ≥ 300s — coi như endpoint chết, cần xử lý ngay
```

**Journal #138767 — AI LME Fix bug — 2026-09-26 (bản fix CUỐI CÙNG — lần 2 + lần 3):**

> Nội dung đầy đủ (dài) đã chép nguyên văn sang `03-dev-impact.md` — đây là nguồn chính cho coverage TC, không lặp lại ở đây để tránh trùng lặp. Tóm tắt: phát hiện thêm nguyên nhân ở hàm `recountAppBadgeNotify` (không ghim connection/queue) → ghim `database/default` cho 30 chỗ gọi; đồng thời **gỡ bỏ migration của lần 1** vì Dev cho rằng DB thật đã có sẵn chỉ mục `salon_booking_id` (⚠️ xem cảnh báo mâu thuẫn với Redmine #41979 ở mục "Ghi chú thêm của Leader" phía trên).
