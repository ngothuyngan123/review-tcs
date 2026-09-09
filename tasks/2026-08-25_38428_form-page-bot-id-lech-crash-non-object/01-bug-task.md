# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bởi `/new-task`. Tester phải verify rồi tick checkbox bên dưới trước khi chạy `/write-tc` hoặc `/review-tc`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38428 — [AI][Bug Exception] Trying to get property '..' of non-object/var/www/html/lme_shorten/sns-line/app/Services/FormAnswer/FormAnswer` |
| Redmine URL | https://redmine.watermelon.vn/issues/38428 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-07-02` |
| Khách hàng / PM báo | `ai-exception detect-bug` (ticket tự tạo bởi check-exception AI từ exception bắn lên Chatwork) |
| Module / Màn hình | `Biểu mẫu (Form Answer)` — màn chỉnh sửa form `/basic/form-answer/edit/{id}` (lưu form, `saveV3`) + màn trả lời biểu mẫu công khai `/form-answer/{unique_key}` (LIFF / LINE user) |
| Priority | `Medium` (Redmine priority = `Normal`; ⚠️ description ghi *Rủi ro: high*) |
| Môi trường phát hiện | `Production (s.lmes.jp)` |

### Thông tin Redmine bổ sung (không có trong template gốc)

| Trường | Giá trị |
|---|---|
| Tracker | `Bug tự detect` |
| Status | `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |
| Parent ticket | `#26684` |
| Attachments | Không có |
| Relations | Không có |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine (format textile). KHÔNG diễn giải lại. -->

```
*Ticket tự tạo bởi check-exception AI (từ exception bắn lên Chatwork).*

*Phân loại:* php_code_error — *Rủi ro:* high
*Số lần cảnh báo:* 36 — *Số user lỗi:* 0
*Room:* SNSLineException — *Server:* s.lmes.jp/
*Lần đầu:* 2026-07-01 21:13 UTC — *Lần cuối:* 2026-07-02 08:51 UTC

h3. Signature (đã chuẩn hóa)
<pre>Trying to get property '..' of non-object/var/www/html/lme_shorten/sns-line/app/Services/FormAnswer/FormAnswerService.#</pre>
h3. Exception mẫu (mới nhất)
<pre>Server: s.lmes.jp/
Trying to get property 'id' of non-object/var/www/html/lme_shorten/sns-line/app/Services/FormAnswer/FormAnswerService.php171</pre>
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguyên văn journal #132977 — Ngô Thúy Ngần, 2026-08-25T13:52:24Z. Description gốc KHÔNG có Section "Tái hiện bug". -->

Thao tác tái hiện:

1. Vào detail form của bot A => Mở 2 tab màn hình detail form này
2. Tại tab thứ nhất => Chọn sang bot B
3. Tại tab thứ 2 => Thao tác nhanh click button プレビュー để save form và mở ra màn preview form

## Expected result

- `<Redmine KHÔNG ghi Expected — tester fill>`

## Actual result

<!-- Nguyên văn phần "BUG:" của journal #132977. -->

- BUG: Màn preview bị hiển thị lỗi 404 và bắn exception chatwork: `Trying to get property 'id' of non-object/var/www/html/sns-line/app/Services/FormAnswer/FormAnswerService.php171`

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — **không phải attachment**, log exception nằm inline trong description Redmine (signature + exception mẫu). Redmine `attachments` = rỗng.

## Ghi chú thêm của Leader

<!-- Auto-fill từ /new-task — các điểm tester cần biết trước khi viết/review TC. -->

- **Ticket auto-detect**: tạo bởi AI check-exception từ exception Chatwork room `SNSLineException`, server `s.lmes.jp/`. Phân loại `php_code_error`, rủi ro `high`, **36 lần cảnh báo**, *Số user lỗi: 0*. Lần đầu 2026-07-01 21:13 UTC — lần cuối 2026-07-02 08:51 UTC.
- **Steps to reproduce KHÔNG có trong description gốc** — được QA (Ngô Thúy Ngần) bổ sung ở journal ngày 2026-08-25, tức **sau** khi Dev (AI auto-fixbug) submit đánh giá ảnh hưởng ngày 2026-07-02. Kiểm tra xem steps này có khớp root cause Dev mô tả trong [03-dev-impact.md](03-dev-impact.md) không.
- **Steps repro dùng 2 tab cùng lúc** (tab 1 đổi bot → tab 2 bấm プレビュー): đây là race giữa session bot và bot sở hữu form → thuộc nhóm quan điểm concurrency (`CONC-*`), không chỉ là luồng lưu form đơn lẻ.
- ⚠️ **Cần recover data**: Dev báo có form đã bị ghi đè `form_answer_page.bot_id` sai (dev: 6 dòng) — **không recover thì các form cũ vẫn lỗi khi mở dù đã deploy fix**. Xem mục 5 file [03-dev-impact.md](03-dev-impact.md). Số dòng lệch **trên production chưa được xác nhận**.
- ⚠️ Đường dẫn trong subject (`lme_shorten/sns-line/...`) và trong journal QA (`sns-line/...`) khác nhau — verify đúng 1 codebase hay 2 deploy path.
