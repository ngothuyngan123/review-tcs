# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36585 — [20-05-2026][10965][Media (image,video...)] Hình ảnh từ friend 「石丸雅司」 gửi không xem được trên app` |
| Redmine URL | https://redmine.watermelon.vn/issues/36585 |
| Auto-filled | 2026-05-22 by /new-task |
| Ngày báo cáo | 2026-05-20 |
| Khách hàng / PM báo | AI CSS |
| Module / Màn hình | Media (image,video...) — Chat 1:1 hiển thị message trên mobile app |
| Priority | Medium |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: kaleidoschope.vintage@gmail.com
Bot Name: 【絶版玩具店】かれいどスコープ

Hình ảnh được gửi từ friend 「石丸雅司」 không hiển thị được trên app.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B4RQPL5R9

---

h3. 原文 (JP)
<pre>
友だち「石丸雅司」から送られた画像がアプリ上で見れない。
</pre>

<!-- TaskRef: user_report:Rec0B4RQPL5R9 -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ journal "Tái hiện bug" do Thanh Phương submit ngày 2026-05-21 -->

1. Tải ảnh trên trình duyệt về lưu dạng file
2. Vào app LINE nhấn vào gửi file → chọn ảnh vừa tải → nhấn gửi cho bot

## Expected result

<!-- Source không ghi rõ Expected trong Section "Tái hiện bug". Suy từ description: ảnh user gửi phải hiển thị được trên app chat 1:1. Tester verify trước khi viết TC. -->

-

## Actual result

- Màn hình chat 1:1 phía app hiển thị màn hình xám, không hiển thị được ảnh do user gửi

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments từ Redmine:
- [スマホで見た時.png](https://redmine.watermelon.vn/attachments/download/25914/%E3%82%B9%E3%83%9E%E3%83%9B%E3%81%A7%E8%A6%8B%E3%81%9F%E6%99%82.png) (147KB) — màn hình app khi gặp bug
- [SnapCrab_NoName_2026-5-20_11-10-20_No-00.png](https://redmine.watermelon.vn/attachments/download/25915/SnapCrab_NoName_2026-5-20_11-10-20_No-00.png) (237KB)

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Bug nằm ở **app side (mobile)** khi render message do **user (friend) gửi** lên bot. Test trên cả 2 OS (android + iOS) — TC sheet đã liệt kê yêu cầu này.
- API liên quan: `getListMessageByUserV4` ([app/Http/Controllers/Api/ChatController.php](#)) — message type "file" trả về object thay vì link, nên app không hiển thị.
- Section "Tái hiện bug" và "Đánh giá ảnh hưởng phía dev" nằm trong **journal note** (không phải description). Author: Thanh Phương, ngày: 2026-05-21.
- `assigned_to` Redmine = Kieu Son Tung, nhưng journal Section B do **Thanh Phương** viết — `03-dev-impact.md` ghi Dev phụ trách = Thanh Phương theo journal.
