# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43376 — [18-10-2026][T12446][Lesson] URL hủy lịch gửi tự động cho khách (đặt lịch lesson) hiển thị nhầm màn hình của người khác, tương đương rò rỉ thông tin cá nhân, cần điều tra gấp.` |
| Module / Màn hình | `Đặt lịch lesson (レッスン予約, FA-019) — màn LIFF phía khách: chi tiết lịch đặt (tab=detail) mở từ キャンセル用URL + thao tác huỷ lịch. Dev xác nhận Salon (サロン・面談予約, FA-020) có cùng lỗ hổng.` |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: matsuzaki.h@josanshes.com
Bot Name: @873udajn

Có khách liên hệ rằng URL hủy lịch (キャンセル用URL) được gửi tự động cho khách hiển thị thành màn hình của người khác. Việc này tương đương rò rỉ thông tin cá nhân nên nhờ điều tra gấp.

Khách hàng liên quan → RIKO／井上理子
Tên khách bị hiển thị URL nhầm → 柴田真奈/登川真奈

Tên friend: RIKO／井上理子、柴田真奈/登川真奈
Chức năng: Đặt lịch lesson (レッスン予約)
Thời điểm phản hồi: 2026/10/18 08:38:12

Nguồn: Tayori — task #12446 (操作方法に関するお問い合わせフォーム)

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug". Suy từ journal Dev Studio #144995 — Leader verify lại. -->

1. Friend 登川 (B) đặt lịch lesson → nhận tin xác nhận chứa キャンセル用URL dạng `https://liff.line.me/<liff_id>?calendar_id=<id>&tab=detail&booking_id=<booking của B>`.
2. Shop copy tin xác nhận của B, gửi lẻ cho friend RIKO (A).
3. A mở URL trên LINE của mình.

## Expected result

- A không xem được thông tin booking của B và không huỷ được booking của B.

## Actual result

- A thấy màn chi tiết booking của B (họ tên, kana, email) và huỷ được booking của B.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.melonglobal.net/attachments/download/35402/screenshot1.png
- https://redmine.melonglobal.net/attachments/download/35403/screenshot2.png

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine (không có section "Tái hiện bug") — root cause đã được Dev confirm qua journal #144995 (file 03). TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: Production (khách thật).
- Theo Dev: hệ thống gửi tin tự động **không sai** — URL của B tới tay A qua tin shop gửi lẻ (copy từ tin xác nhận của B). Lỗi gốc là API chi tiết / huỷ lịch chỉ tìm theo `booking_id`, không kiểm LINE user đang mở trang.
- Phạm vi fix gồm **cả Salon** (D-4, D-5).
- Rủi ro release: WebView còn giữ JS cũ → chính chủ booking bị báo không tìm thấy → release phải bump version JS.
- Liên quan kho: FA-019 `MT-38` / `MT-63`, `TC-LSN-434`, `TC-LSN-609` (spec S-01 / S-03).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `141275` (Bot Name `@873udajn`) |
| Friend | A = RIKO／井上理子 (người mở URL) · B = 柴田真奈/登川真奈 (chủ booking) · line_id `62800491` (journal không ghi rõ của A hay B) |
| Đối tượng cấu hình | Lesson calendar `3874` · booking `583631` |
| URL lỗi | `https://liff.line.me/2006833331-Mgm1qWg2?calendar_id=3874&tab=detail&booking_id=583631` |
| Thời điểm lỗi | `2026/10/18 08:38:12` (thời điểm phản hồi) |

## Journal / note từ Redmine (nguyên văn)

**Journal #144989 — Ngô Thúy Ngần — 2026-10-17:**
```
bot_id 141275
line_id 62800491
lesson_id 3874

link cancel: https://liff.line.me/2006833331-Mgm1qWg2?calendar_id=3874&tab=detail&booking_id=583631
```

**Journal #144995 — Dev Studio — 2026-10-18:** → chép nguyên văn ở [03-dev-impact.md](03-dev-impact.md).
