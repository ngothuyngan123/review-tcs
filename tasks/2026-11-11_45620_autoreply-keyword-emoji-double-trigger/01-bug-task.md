# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45620 — [09-11-2026][32908][Auto reply] Khách báo auto-reply theo keyword (にじ/ハート) bị kích hoạt 2 cái cùng lúc dù tin nhắn của friend không chứa keyword; chỉ xảy ra khi đặt 部分一致・何度でも.` |
| Module / Màn hình | Tự động trả lời (自動応答 / Auto reply) — matching theo keyword kiểu 部分一致 (contains) |

## Mô tả bug (bản dịch tiếng Việt)

OEM ĐÃ TẠO TICKET SLACK

User: linx200202@gmail.com
Bot Name: LINXいとみ（おりん）

Đang xảy ra hiện tượng ngay sau khi friend gửi một câu không phải keyword thì 2 auto-reply theo keyword bị thực thi. Khi xem chi tiết trigger gửi thì hiện auto-reply (phản ứng với keyword đã thiết lập) nhưng trong câu được gửi không thấy keyword đó.

Keyword là:
- にじ
- ハート

và 2 tin tự động được gửi cùng lúc.

Khi đặt 部分一致 (khớp từng phần) ・ 何度でも (không giới hạn số lần) thì xảy ra, còn khi đặt 完全一致 (khớp hoàn toàn) ・ 一度のみ (chỉ 1 lần) thì không tái phát.

Có khoảng 5 vụ gửi tự động tương tự, tất cả đều chứa các từ như ありがとうございます (cảm ơn). Sau đó đôi khi kèm emoji như mặt cười hoặc emoji cúi đầu.

Tên friend liên quan: ふるたん, 槙石亜季, みゆき⭐︎

Chức năng: Tự động trả lời (自動応答)
Thời điểm phản hồi: 2026/11/09 12:56:00

Ảnh (link do KH/OEM đính kèm trong description, khác với 2 attachment Redmine ở mục dưới):
- https://go.lmes.jp/msg_template/media/images/3/218/form/1794196573ZPVzHs.png
- https://go.lmes.jp/msg_template/media/images/3/218/form/1794196580xFwyxF.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=32908
Nguồn: Google Sheet dòng 7, 回答ID 32908

## Steps to reproduce

> Redmine description không có heading "Tái hiện bug" chuẩn — steps dưới đây lấy từ **Journal #153579 (Ngô Thúy Ngần, 2026-11-10)**, là người đã tái hiện thành công trên tool:

1. Tạo và bật 2 auto reply:
   - Keyword: `🫶`, kiểu so khớp: 部分一致 (khớp từng phần), action trả lời set "Đã nhận keyword trái tim"
   - Keyword: `🌈`, kiểu so khớp: 部分一致 (khớp từng phần), action trả lời set "Đã nhận keyword cầu vồng"
2. Dùng tài khoản friend gửi tin nhắn sau vào bot (KHÔNG chứa `🫶` hoặc `🌈`):
   ```
   ありがとうございます😊
   しかし！今年からweb申請に変わったので、あっているのかわからないまま恐る恐る進めています😭
   ```

## Expected result

- Không auto-reply nào được kích hoạt, vì tin nhắn không chứa `🫶` hoặc `🌈`.

## Actual result

- Cả 2 auto-reply (`🫶` và `🌈`) cùng kích hoạt dù tin nhắn không chứa keyword nào trong 2 keyword đó.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.melonglobal.net/attachments/download/39744/screenshot1.png
- screenshot2.png — https://redmine.melonglobal.net/attachments/download/39745/screenshot2.png

## Ghi chú thêm của Leader

- Bug **không phải xác suất ngẫu nhiên** — tái hiện 100% khi: keyword là emoji 4-byte (UTF-8) + kiểu so khớp 部分一致. Kiểu 完全一致・一度のみ KHÔNG bị ảnh hưởng.
- Bug phát sinh từ khi **DB lên MySQL 8.0.46 (20/10/2026)** — code matching keyword không đổi từ 12/2023, lỗi là do hành vi `LOCATE()` + collation thay đổi giữa MySQL 5.7 → 8.0, KHÔNG phải do code mới.
- ⚠️ Dev ghi rõ: **Dev (MySQL 5.7) KHÔNG tái hiện được lỗi** — môi trường test bắt buộc phải dùng **MySQL 8 (staging / prd)**. Local test tool dùng MySQL nào cần verify trước khi tin tưởng kết quả `pass` trên env `local`.
- Phạm vi: mọi bot có auto-reply keyword kiểu 部分一致 với keyword là **emoji 4-byte** (🫶 🌈 💕 😊 …) — không giới hạn riêng 2 bot/keyword trong báo cáo KH.
- Nhánh 完全一致 (so khớp theo `utf8mb4_bin`, giữ nguyên) — Dev khẳng định chưa ghi nhận lỗi, nhưng chưa có TC verify riêng nhánh này sau fix.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `191487` (theo Journal #153599); bot gốc báo lỗi của KH chưa thấy ghi số — xem Journal #153245 cho keyword liên quan |
| Friend | ふるたん — line_user_id `U3c4c8377b3806c0bf1fc1d5c34b2db38` (line user id nội bộ `66774651`); 槙石亜季 — line_user_id `Uc146a312b58b54abf5136268c631065c` (line user id nội bộ `65657671`) |
| Đối tượng cấu hình | Auto-reply keyword `にじ` — reply_id=`3390540`; Auto-reply keyword `ハート` — reply_id=`3373337` |
| Thời điểm lỗi | 2026/11/09 12:56:00 (KH báo); case đối chứng Dev test: 2026-10-29 19:21:19 |
| Đối chứng | Journal #153579: case tái hiện trên tool bằng keyword `🫶`/`🌈` kiểu 部分一致 — cùng bản chất lỗi (emoji 4-byte + utf8mb4_unicode_ci) |

## Journal / note từ Redmine (nguyên văn)

**Journal #153245 — Ngọc Ánh — 2026-11-09:**

```
Key word:
にじ: reply_id=3390540
ハート: reply_id=3373337
line user id: 66774651 (ふるたん)
line user id: 65657671 (槙石亜季)
```

**Journal #153370 — Thanh Duy Nguyen — 2026-11-09:**

```
line user id: 66774651 (ふるたん) U3c4c8377b3806c0bf1fc1d5c34b2db38
line user id: 65657671 (槙石亜季) Uc146a312b58b54abf5136268c631065c
2026-10-29 19:21:19
```

**Journal #153579 — Ngô Thúy Ngần — 2026-11-10:**

```
Tái hiện lỗi:
1. Tạo và bật 2 auto reply:
+ Keyword: 🫶, kiểu so khớp: 部分一致, action trả lời set "Đã nhận keyword trái tim"
+ Keyword: 🌈, kiểu so khớp: 部分一致, action trả lời set "Đã nhận keyword cầu vồng"

2. Dùng tài khoản friend gửi tin nhắn sau vào bot:
ありがとうございます😊
しかし！今年からweb申請に変わったので、あっているのかわからないまま恐る恐る進めています😭


BUG: Cả hai auto-reply cùng kích hoạt.
=> Expect: Không kích hoạt auto-reply nào vì tin nhắn không chứa 🫶 hoặc 🌈.
```

**Journal #153599 — Thanh Duy Nguyen — 2026-11-10 (Kết luận nguyên nhân và cách fix — xem đầy đủ ở `03-dev-impact.md`):**

```
Môi trường test phải dùng MySQL 8 (staging). Dev (5.7) không tái hiện được lỗi.
```

> Nội dung đầy đủ của Journal #153599 / #153630 / #153670 (nguyên nhân, cách fix, bằng chứng, phạm vi ảnh hưởng) đã được chuyển vào `03-dev-impact.md` — không lặp lại ở đây.
