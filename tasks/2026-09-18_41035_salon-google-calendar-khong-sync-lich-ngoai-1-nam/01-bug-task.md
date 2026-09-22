# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41035 bởi `/new-task` (2026-09-18). Metadata Redmine tra thẳng trên Redmine.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41035 — [16-09-2026][T12166][Salon] Khách báo Google Calendar đã có lịch hẹn nhưng màn hình đặt lịch Salon của Elme vẫn hiển thị trống, gây nguy cơ đặt lịch trùng.` |
| Module / Màn hình | Salon — サロン予約 (FA-020) · 予約設定 →「Googleカレンダー連携」· khung giờ trống ở màn đặt lịch phía khách (LIFF) và lưới quản lý admin |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: jun.syukyaku.address@gmail.com
Bot Name: 人気ヒーラー育成家＠齋藤　順

Cảm ơn quý công ty đã hỗ trợ.

Hiện tại tôi đang sử dụng tính năng 「サロン予約」(đặt lịch salon) của Elme, nhưng đã xảy ra tình trạng có vẻ là lỗi liên quan đến việc liên kết với Google Calendar, nên tôi liên hệ để nhờ kiểm tra giúp.

Mặc dù trên Google Calendar đã liên kết có những khung giờ đã có lịch hẹn, nhưng ở màn hình đặt lịch phía Elme lại hiển thị là còn trống và có thể đặt lịch được.

Nếu cứ như vậy thì có khả năng lịch hẹn sẽ bị trùng, nên tôi muốn khắc phục càng sớm càng tốt.

Không biết nguyên nhân khiến lịch hẹn trên Google Calendar không được phản ánh đúng vào khung đặt lịch phía Elme là gì, và có cài đặt nào cần kiểm tra/sửa lại hay không, quý công ty có thể hướng dẫn giúp tôi được không ạ?

Xin lỗi vì đã làm phiền, mong quý công ty kiểm tra gấp giúp tôi.
Xin cảm ơn quý công ty.

Chức năng: Đặt lịch buổi học (レッスン予約) — *ghi chú: form khách chọn nhầm, nội dung thực tế là サロン予約*
Thời điểm phản hồi: 2026/09/16 15:38:34

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12166
Nguồn: Tayori — task #12166 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/21e2e27146ddd7b56cb0d26e12ce2dcbc183fadc/

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [x] Có log / request-response (SQL + payload event Google ở Journal #136749)

- https://redmine.watermelon.vn/attachments/download/30539/screenshot1.png
- https://redmine.watermelon.vn/attachments/download/30540/screenshot2.png

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: Production (khách thật, bot 82253).
- Điều kiện tái hiện suy từ journal: salon liên kết Google Calendar (chọn マイカレンダー) từ **2025-09-05**; lần liên kết đầu chỉ kéo event trong cửa sổ 1 năm (2025-09-05 → 2026-09-05). Event (đặc biệt là buổi của **lịch lặp**) rơi sau mốc đó mà không bị sửa trên Google → không bao giờ về Elme → slot hiển thị trống.
- Đánh giá ảnh hưởng (file 03) do **AI Reader** viết trên Redmine, chỉ verify mức **lint** — CHƯA chạy migration, CHƯA test với dữ liệu thật của khách.
- Kho TCs FA-020 (`kho-tcs/fa020-...md`) hiện **không có TC** nào cover giới hạn cửa sổ 1 năm của lần liên kết đầu; TC-SLN-470 ghi mốc lọc "tương lai > 2 năm" theo spec — lệch với cửa sổ 1 năm Dev nêu.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `82253` (人気ヒーラー育成家＠齋藤　順) |
| Đối tượng cấu hình | calendar salon `calendar_id = 17841` · `staff_id = 27698` |
| Event Google lỗi | `7v154eb3rln4traa10rv7u4r23_20260919T090000Z` — 2026-09-19 18:00–22:00 (Asia/Tokyo), status `confirmed`, created 2025-09-05, **không có dòng** trong `calendar_salon_booking_by_google` |
| Thời điểm lỗi | Khách báo 2026/09/16 15:38:34 |
| Đối chứng | Event nằm trong cửa sổ 2025-09-05 → 2026-09-05 thì đã được sync (theo phân tích Dev) |

## Journal / note từ Redmine (nguyên văn)

**Journal #136749 — Ngọc Ánh — 2026-09-16:**

```
calendar_id:17841
bot_id: 82253
staff_id = 27698

SELECT * FROM `calendar_salon_booking_by_google` WHERE `calendar_salon_id` = 17841 AND `staff_id` = 27698 AND event_id_google_calendar LIKE  '7v154eb3rln4traa10rv7u4r23_20260919T090000Z'

{
            "id": "7v154eb3rln4traa10rv7u4r23_20260919T090000Z",
            "start": "{\"date\":null,\"dateTime\":\"2026-09-19T18:00:00+09:00\",\"timeZone\":\"Asia\\/Tokyo\"}",
            "end": "{\"date\":null,\"dateTime\":\"2026-09-19T22:00:00+09:00\",\"timeZone\":\"Asia\\/Tokyo\"}",
            "status": "confirmed",
            "created_at": "2025-09-05T12:22:43.000Z",
            "updated_at": "2025-09-05T12:23:01.339Z"
        },
```

**Journal #137014 — AI bug detect Lme — 2026-09-18:**

```
Đã Add DB CS + thread OEM đã lên Slack → xác nhận Bug.
Đổi tracker "Bug KH cần xử lý nội bộ" → "Bug KH".
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C2Q2TKUUW
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1789701701432469
```

<!-- Journal #137013 (AI Reader — đánh giá ảnh hưởng) chuyển sang 03-dev-impact.md. -->
