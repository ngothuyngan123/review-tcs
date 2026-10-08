# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41489 — [AI][Bug Exception] SQLSTATE: Column not found: # Unknown column '..' in '..' (SQL:../var/www/html/sns-line/vendor/laravel/framewo` |
| Module / Màn hình | Đặt lịch Salon (FA-020, 「サロン・面談予約」) — tab 「予約設定」 mục 「予約時のお客様への質問項目」 (màn cài đặt câu hỏi của form nhận đặt lịch Salon), API `update-setting-form`. Feature Studio: `calendar-salon`. |

## Mô tả bug (bản dịch tiếng Việt)

Ticket được **tự tạo bởi hệ thống check-exception AI** (từ exception bắn lên Chatwork), **không phải khách hàng báo trực tiếp**.

- Phân loại: uncategorized — Rủi ro: low
- Độ ưu tiên: Low (người review chọn)
- Số lần cảnh báo: 2 — Số user lỗi: 0
- Room: SNSLineException — Server: step.lme.jp/
- Lần đầu: 2026-09-24 11:25 UTC — Lần cuối: 2026-09-24 11:25 UTC (chỉ xảy ra 1 lần trong khung thời gian ghi nhận)

**Signature (đã chuẩn hóa):**
```
SQLSTATE: Column not found: # Unknown column '..' in '..' (SQL:../var/www/html/sns-line/vendor/laravel/framework/src/Illuminate/Database/Connection.#
```

**Exception mẫu (mới nhất):**
```
Server: step.lme.jp/
User: flw-g.sugiya@titan.ocn.ne.jp (178313)
BotId: 219803
SQLSTATE[42S22]: Column not found: 1054 Unknown column 'friend_information_setting' in 'field list'
(SQL: update `calendar_salon_setting_send_forms` set `question` = 「肝臓病」の診断を受けている, `required` = 1,
`form_type` = 3, `display_method` = 1, `link_friend_information` = 3, `friend_information_id` = 341813,
`friend_information_setting` = 「肝臓病」の診断を受けている,
`options_information_friend` = [{"title":"はい","value":"はい","id":"568397"},{"title":"いいえ","value":"いいえ","id":"568398"}], ...)
```

## Steps to reproduce

⚠️ Không có steps thủ công — bug do AI phát hiện qua giám sát exception (Chatwork), không phải khách hàng report theo flow UI. Theo đánh giá của Dev (journal, xem `03-dev-impact.md`): API lưu câu hỏi của form đặt lịch Salon nhận **nguyên payload trình duyệt gửi lên** rồi ghi thẳng vào bảng mà không lọc theo cột thật, nên khi payload có khoá phụ chỉ dùng để hiển thị (`friend_information_setting` — thông tin bạn bè liên kết), câu lệnh update sinh ra cột không tồn tại → MySQL lỗi 1054 → request chết 500.

Dev đã tái hiện lại bằng cách gửi đúng payload của exception tới endpoint (xem TC Studio `NEW-10` ở `04-tc-list.md`).

## Expected result

- Lưu chỉnh sửa câu hỏi của form đặt lịch Salon thành công (không lỗi 500) dù payload có kèm field không thuộc cột thật của bảng.
- Nếu có lỗi, màn hình phải hiển thị thông báo lỗi rõ ràng cho người dùng (không được "nuốt" lỗi).

## Actual result

- Request lưu câu hỏi trả **HTTP 500** (`SQLSTATE[42S22]: 1054 Unknown column 'friend_information_setting' in 'field list'`).
- Màn hình **không hiển thị thông báo lỗi nào** (JS cũ chỉ ghi `console`) → người dùng bấm lưu nhưng không lưu được, lại tưởng là đã lưu thành công.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment trên Redmine (0 attachment). Log exception đầy đủ đã trích ở "Mô tả bug" phía trên (lấy từ description gốc).

## Ghi chú thêm của Leader

- ⚠️ Bug do **AI check-exception tự tạo ticket** từ Chatwork, không phải CS/khách hàng báo — không có bước tái hiện thủ công, không có screenshot/video. Root cause + cách fix đã được Dev xác nhận đầy đủ qua đánh giá ảnh hưởng ở `03-dev-impact.md` (lấy từ journal #139822, do hệ thống Auto-fixbug LME tạo).
- Tần suất: chỉ ghi nhận 2 lần cảnh báo, 1 lần xảy ra (2026-09-24 11:25 UTC), 0 user bị ảnh hưởng theo thống kê hệ thống — nhưng theo phân tích root cause thì **mọi** lần sửa câu hỏi có liên kết friend info kiểu "đã có sẵn" (`link_friend_information = 3`) đều có khả năng gặp lỗi này, không phải lỗi xác suất thấp.
- Môi trường phát hiện: **Production** (`step.lme.jp`).
- Ticket status hiện tại: `Fix done - Đợi test`. Branch fix: `ai_fixbug_41489` (gốc `release_step_20260827`, commit `32484cfc25`) — xem chi tiết commit/branch ở `03-dev-impact.md`.
- Toàn bộ nội dung "Đánh giá ảnh hưởng" (nguyên nhân / cách fix / caller / impact) đã được chuyển nguyên văn sang `03-dev-impact.md` — không lặp lại ở đây để tránh trùng lặp.
- Studio đã có task review-ready cho ticket này (task #353, feature `calendar-salon`, 16 TC do AI sinh, đã chạy pass 16/16 — xem `04-tc-list.md`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `219803` |
| Friend | `flw-g.sugiya@titan.ocn.ne.jp` — friend ID `178313` |
| Đối tượng cấu hình | Câu hỏi form đặt lịch Salon — `friend_information_id = 341813`, `link_friend_information = 3` (liên kết friend info đã có sẵn), `form_type = 3` (単一選択), 2 lựa chọn `はい` (option id `568397`) / `いいえ` (option id `568398`) |
| Thời điểm lỗi | `2026-09-24 11:25 UTC` |
| Đối chứng | Không có — chưa ghi nhận case chạy đúng để so sánh trong ticket |
