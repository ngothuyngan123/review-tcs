# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37109 — [05-06-2026][11134][Bill tiền tool] Ngày của Hủy hợp đồng cưỡng chế (強制解約) hiển thị khác nhau giữa từng trang` |
| Redmine URL | https://redmine.watermelon.vn/issues/37109 |
| Auto-filled | `2026-06-09 by /new-task` |
| Ngày báo cáo | `2026-06-05` |
| Khách hàng / PM báo | `AI LME CSS` |
| Module / Màn hình | `Bill tiền tool` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: info@musashikoyama-sc.jp
Bot Name: 女性の起業☆武蔵小山創業支援センター

Ngày của Hủy hợp đồng cưỡng chế (強制解約) đang hiển thị khác nhau giữa từng trang (page).

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B8ENPAMC2

---

h3. 原文 (JP)
<pre>
強制解約の日付がページごとに異なっている。
</pre>
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ Section "Tái hiện bug" (journal #120574 của Ngọc Ánh). Đây là điều kiện DATA của contract, không phải thao tác click. -->

1. Có Bot contract thỏa **một trong hai** nhóm điều kiện:
   - **Nhóm A (thẻ card):** `payment_method = 1 (card)` + `status = 1 (đang hợp đồng)` + `expired_date < now` & `now - expired_date < 7 ngày` + `status_payment = 2 (bill fail)` + `status_payment_fail != (0, 5)`
   - **Nhóm B (chuyển khoản):** `payment_method = 2 (transfer)` + `status = 1 (đang hợp đồng)` + `expired_date < now` & `now - expired_date < 7 ngày` + `status_payment = 5 (đợi chuyển khoản)`
2. Mở trang danh sách **契約情報・領収書** (bill/index) → xem ngày 強制解約 (banner cảnh báo 決済エラー và/hoặc cột 延滞中).
3. Mở trang chi tiết **契約詳細** (bill/detail) của cùng contract đó → xem ngày 強制解約.
4. So sánh ngày 強制解約 giữa 2 trang.

## Expected result

- Ngày Hủy hợp đồng cưỡng chế (強制解約) phải hiển thị **GIỐNG nhau** trên mọi trang (list và detail) cho cùng một contract. *(Suy ra từ tiêu đề bug; Section "Tái hiện bug" không nêu Expected riêng.)*

## Actual result

- Ngày cancel (強制解約) ở màn **list** và màn **detail** đang **khác nhau**.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/26361/SnapCrab_NoName_2026-6-5_8-17-39_No-00.png
- https://redmine.watermelon.vn/attachments/download/26362/SnapCrab_NoName_2026-6-5_8-17-49_No-00.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Bug là dạng **data-condition** (không tái hiện được bằng thao tác click thuần — cần contract ở đúng trạng thái dữ liệu nêu trên). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify cách fix (đồng nhất ngày giữa list ↔ detail theo `payment_method`) + regression.
