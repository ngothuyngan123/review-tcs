# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40599 — [07-09-2026][T12083][Notify Setting] Khách báo mọi thông báo trên app (không chỉ thông báo thêm bạn) đều nhận trùng lặp cùng nội dung 2 lần, nhờ kiểm tra nguyên nhân.` |
| Module / Màn hình | `Notify Setting — màn Cài đặt thông báo (通知設定) + màn hình thông báo/push trên Mobile App` |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

- User: `ayano0509abelia@gmail.com`
- Bot Name: `Ensemble Grazie`

> Cảm ơn quý công ty đã hỗ trợ. Tôi cũng đã cài đặt ứng dụng.
> Trong cài đặt thông báo (通知設定), không chỉ thông báo thêm bạn (友だち登録) mà **tất cả các thông báo đều nhận được cùng một nội dung 2 lần**.
> Tôi chỉ muốn nhận thông báo 1 lần thôi, không biết nguyên nhân là gì ạ.
> Ảnh chụp màn hình là cài đặt thông báo thêm bạn.
> Ngoài ra còn có màn hình thông báo trên ứng dụng. Mong quý công ty hỗ trợ.

- Chức năng: Cài đặt thông báo (通知設定)
- Thời điểm phản hồi: 2026/09/07 08:27:10
- Ticket Slack do OEM đăng — 管理番号 TY-12083
- Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12083

## Steps to reproduce

<!-- Nguồn: Journal #134945 — Đoàn Thị Bích Hảo — 2026-09-07 (tái hiện lại bug) -->

1. Thực hiện **thêm bot mới** (luồng Add New Account / kết nối bot).
2. Tại bước **hiển thị QR code để quét mã kết bạn** (Step 5/5 「接続チェック」) → bấm **back lại màn trước**.
3. Bấm **next tiếp** → hệ thống insert **duplicate 2 record** cho cùng 1 bot trong bảng `notify_setting`.
4. Thực hiện tạo sự kiện sinh thông báo: **kết bạn**, **gửi tin hàng loạt**, ... → notify bị duplicate.
5. Mở app (danh sách thông báo + push) → mỗi sự kiện hiện **2 dòng cùng nội dung**, badge cộng 2.

## Expected result

- Mỗi sự kiện sinh thông báo chỉ tạo **đúng 1 bản ghi thông báo** cho mỗi người nhận → app hiển thị **1 mục**, push **1 lần**, badge tăng **1**.
- Lặp lại bước 2 của luồng kết nối bot (back → next nhiều lần) **không** sinh thêm bản ghi `notify_setting` cho cùng cặp (bot, người dùng).

## Actual result

- Mọi loại thông báo đều hiển thị **2 lần cùng nội dung** trên app, push **2 lần**, badge **cộng 2**.
- Bảng `notify_setting` có **2 bản ghi cho cùng cặp (bot, người dùng)** — bot khách 218134, 2 bản ghi tạo lúc `2026-09-04 21:48:06` và `2026-09-04 21:49:19`.
- Bản ghi thừa là **"bản ghi ma"**: màn Cài đặt thông báo chỉ đọc/ghi bản ghi đầu tiên → khách **bỏ tick vẫn nhận thông báo** từ bản ghi kia (bản ghi thừa mặc định BẬT sẵn thông báo app, tick đủ 4 mục thêm bạn).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/30027/screenshot1.png — màn cài đặt thông báo thêm bạn (友だち登録)
- https://redmine.watermelon.vn/attachments/download/30028/screenshot2.jpg — màn hình thông báo trên app

## Ghi chú thêm của Leader

- ⚠️ **Tester KHÔNG tái hiện được trên acc tester (7/9)** — trên bot 215377 push chỉ 1 lần, trong app cũng chỉ 1 nội dung (cả acc staff lẫn admin). Bug **phụ thuộc dữ liệu**: chỉ xảy ra khi bảng `notify_setting` đã có cặp (bot, user) trùng. Muốn tái hiện phải đi đúng luồng **back → next ở bước QR kết bạn khi thêm bot mới** (Journal #134945), hoặc dựng sẵn dữ liệu trùng.
- **Bản vá code CHỈ chặn phát sinh mới** — dữ liệu trùng cũ + badge dư **không tự mất**. Khách vẫn thấy thông báo trùng cho tới khi vận hành dọn dữ liệu bằng tay.
- ⚠️ **THỨ TỰ DEPLOY bắt buộc**: dọn dữ liệu trùng TRƯỚC → rồi mới `php artisan migrate`. Chạy ngược thứ tự thì migration lỗi `Duplicate entry` cho khoá `notify_setting_bot_id_user_id_unique` và **chặn deploy**.
- Badge đã cộng dư nắn lại bằng `php artisan recover:mobileBadgeNotify`.
- Bug thuộc bug do **AI Auto-fixbug** xử lý (branch `ai_fixbug_40599`), có phần "Tự review (AI)" nêu sẵn rủi ro — xem file `03-dev-impact.md`.
- Env test: recover dữ liệu `notify_setting` **đã chạy trên staging và step** (Journal #134973).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `218134` (bot của KH — có 2 bản ghi trùng) · `215377` (bot tester dùng đối chứng, KHÔNG tái hiện được) |
| Friend | `line_user_id: 60433702` (trên bot tester 215377) |
| Đối tượng cấu hình | `notify_setting` — 2 bản ghi cùng cặp (bot 218134, user), tạo `2026-09-04 21:48:06` và `2026-09-04 21:49:19` |
| Tài khoản test | `user_id acc staff: 29` · `user_id acc admin: 152543` (trên bot 215377) |
| Thời điểm lỗi | `2026/09/07 08:27:10` (thời điểm khách phản hồi) |
| Đối chứng | Bot tester `215377` — push 1 lần, app hiển thị 1 nội dung (cả staff và admin) |

## Journal / note từ Redmine (nguyên văn)

**Journal #134681 — Đoàn Thị Bích Hảo — 2026-09-07:**

```
tester không tái hiện được (7/9)

hiện tại tester check trên acc tester thì push thông báo 1 lần, vào bên trong app cũng chỉ hiển thị 1 nội dung ạ (cả acc staff và admin)
bot_id: 215377
user_id acc staff: 29 (acc staff),  
user_id acc admin: 152543
line_user_id: 60433702

=> nhờ dev check tiếp
```

**Journal #134866 — Đoàn Thị Bích Hảo — 2026-09-07:**

```
bot_id KH: 218134
```

**Journal #134945 — Đoàn Thị Bích Hảo — 2026-09-07:**

```
tái hiện lại bug:

1. xảy ra với trường hợp add bot mới => tại bước hiển thị qr code để quét mã kết bạn => thực hiện back lại màn trước => sau đó next tiếp dẫn đến insert duplicate 2 record cho cùng 1 bot trong bảng notify setting
2. Thực hiện tạo sự kiện thông báo: kết bạn, gửi tin hàng loạt,... => sẽ bị duplicate notify
```

**Journal #134973 — Ngô Thúy Ngần — 2026-09-07:**

```
Chạy recover done bảng notify_setting trên staging và step:
DELETE ns
FROM notify_setting ns
JOIN (
    SELECT
        user_id,
        bot_id,
        MIN(id) AS keep_id
    FROM notify_setting
    GROUP BY user_id, bot_id
    HAVING COUNT(*) > 1
) dup
    ON ns.user_id = dup.user_id
   AND ns.bot_id = dup.bot_id
WHERE ns.id <> dup.keep_id;
```

<!-- Journal #134965 (AI LME Fix bug — báo cáo Auto-fixbug) đã được parse nguyên văn vào 03-dev-impact.md. -->
