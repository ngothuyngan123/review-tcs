# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #37606 bởi `/new-task` ngày 2026-06-16. Tester verify lại description + steps rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37606 — [15-06-2026][回答ID：28530][Info friend] Click thông tin bạn bè (友だち情報) trong folder 「撮影予約情報」>「予約済みのプラン」 báo lỗi` |
| Redmine URL | https://redmine.watermelon.vn/issues/37606 |
| Auto-filled | `2026-06-16 by /new-task` |
| Ngày báo cáo | `2026-06-15` |
| Khách hàng / PM báo | `AI LME CSS` (回答ID：28530) |
| Module / Màn hình | `Info friend (友だち情報) — màn xem/sửa trường Lựa chọn` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `Production` — Bot ULUM 名東区フォトアトリエ (user info@ulumstudio.com) |

## Mô tả bug (nguyên văn từ khách hàng)

User: info@ulumstudio.com
Bot Name: ULUM 名東区フォトアトリエ

Thông tin bạn bè (友だち情報): folder 「撮影予約情報」 > 「予約済みのプラン」
Khi click vào thông tin bạn bè (友だち情報) thì xuất hiện lỗi.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0BAFKM05F0

---

h3. 原文 (JP)
<pre>
友だち情報：フォルダ「撮影予約情報」>「予約済みのプラン」
友だち情報をクリックするとエラーが出る
</pre>

<!-- TaskRef: user_report:Rec0BAFKM05F0 -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Đăng nhập bot `ULUM 名東区フォトアトリエ` (user info@ulumstudio.com).
2. Vào 友だち情報 (Thông tin bạn bè) → folder 「撮影予約情報」 > 「予約済みのプラン」.
3. Click vào trường thông tin bạn bè (trường kiểu Lựa chọn 「予約済みのプラン」).

## Expected result

- Màn hiển thị chi tiết trường thông tin bạn bè bình thường, không báo lỗi.

> Note: Redmine không ghi rõ Expected — đây là suy luận hiển nhiên, tester verify lại.

## Actual result

- Xuất hiện lỗi / alert ngay khi vào màn, màn không hiển thị được.
- Theo điều tra Dev (file 03): lỗi `Trying to get property 'details' of non-object`.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachment: https://redmine.watermelon.vn/attachments/download/26863/1781450415uustWJ.jpeg

## Ghi chú thêm của Leader

⚠️ Bug **không tái hiện được trong Dev DB** (Dev không có data bot ULUM) — root cause đã được Dev confirm qua truy vết code + đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** (guard đọc action mồ côi) + **regression impact** đường cascade xóa tag → Action.
