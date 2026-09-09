# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38843 — [App mobile] Bot hết hợp đồng nhưng vẫn đang sử dụng được app bình thường` |
| Redmine URL | https://redmine.watermelon.vn/issues/38843 |
| Auto-filled | `2026-08-11 by /new-task` |
| Ngày báo cáo | `2026-07-15` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` (author Redmine) — tracker = **`Bug tự detect`** (không phải khách báo) |
| Module / Màn hình | `<category Redmine trống>` — từ prefix subject: **App mobile (LME Flutter app)**; theo file 03 phạm vi là toàn bộ nhóm route `api/mobile` + màn chọn tài khoản (Account Select) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` — tester confirm lại trước khi dựng TC |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #38843. KHÔNG diễn giải lại. -->

```
Expect: Bot hết hợp đồng thì báo lỗi không cho dùng app. Hiển thị popup báo lỗi:
こちらのアカウントの契約は期限切れのため、アプリをご利用いただけません。
Web版の「契約情報」画面から契約を更新するか、別のアカウントを選択してください。

1 button trên popup: 別のアカウントを選択する
=> Click thì cho phép chọn bot khác
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #38843 KHÔNG có section "Tái hiện bug" / 再現手順 → để trống theo nguyên tắc không bịa. -->

1.
2.
3.

## Expected result

<!-- Nguyên văn phần "Expect:" trong description. -->

- Bot hết hợp đồng thì **báo lỗi không cho dùng app**, hiển thị popup báo lỗi với nội dung JP:
  ```
  こちらのアカウントの契約は期限切れのため、アプリをご利用いただけません。
  Web版の「契約情報」画面から契約を更新するか、別のアカウントを選択してください。
  ```
- Popup có **đúng 1 button**: `別のアカウントを選択する`
- Click button đó → **cho phép chọn bot khác**

## Actual result

<!-- Redmine không có section "Kết quả thực tế" riêng. Chỉ có phát biểu ở subject ticket — chép nguyên văn, KHÔNG suy diễn thêm. -->

- Theo subject ticket: `Bot hết hợp đồng nhưng vẫn đang sử dụng được app bình thường`

## Ảnh / video / log đính kèm

<!-- Redmine #38843: attachments = rỗng. -->

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — description chỉ ghi **Expect** (hành vi mong muốn), KHÔNG có bước tái hiện / kết quả thực tế chi tiết. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

Bối cảnh bổ sung (đọc từ Redmine, tester tự verify lại):

- **Trạng thái ticket**: `Fix done - Đợi test` · assignee `Ngô Thúy Ngần` · tracker `Bug tự detect` · project `Lme`.
- **Đây là ticket dạng SPEC-GAP hơn là bug tái hiện**: description viết ở dạng yêu cầu behavior mong muốn (popup + button + luồng chọn bot khác). Nội dung popup JP trong ticket là **nguồn chuẩn để đối chiếu chuỗi hiển thị** khi test.
- **Fix nằm HOÀN TOÀN ở server (repo `sns-line`)** — thêm middleware chặn + cờ `is_contract_expired` trong API danh sách tài khoản. Dev ghi rõ:
  > App Flutter (`share/src/lme-fluter-app`) hiện chỉ xử lý `status_payment_fail` trong `open_modal_list_bot.dart`, **chưa có popup hết hợp đồng → cần app bổ sung phần hiển thị**.

  ⇒ **Nếu chỉ deploy phần server, popup + button `別のアカウントを選択する` như ticket mô tả SẼ CHƯA CÓ** — app bản cũ chỉ thấy lỗi chung khi gọi API (HTTP 403 `contract_expired`). Leader cần confirm với Dev/PM: bản app Flutter đi kèm đã implement chưa, trước khi giao TCs verify phần popup.
- **Đã có 2 vòng fix của AI Auto-fixbug** (cùng ngày `2026-08-10`):
  - Vòng 1 — `03:16`, commit `43037e3645`, 11 unit test.
  - Vòng 2 (**bản chốt**) — `06:46`, commit `d1437b55b1`, bổ sung chặn `bot_contracts.status = 3` (hợp đồng đã huỷ) kể cả khi bản ghi `is_active = 0`, tổng 15 unit test.

  ⇒ File `03-dev-impact.md` chép **nguyên văn vòng 2**. Nếu QA checkout branch mà không thấy nhánh xử lý `status = 3` ⇒ đang ở commit cũ, hỏi lại Dev.
- **Dev CHƯA verify được với DB thật** (MySQL dev `host.docker.internal:3306` Connection refused) → quy tắc hết hạn lấy theo middleware web `IsExpire`, chưa đối chiếu dữ liệu hợp đồng thật. **QA phải verify end-to-end trên môi trường có dữ liệu hợp đồng thật.**
- **Đã có bộ TC trên LME TEST STUDIO** (task `#59`) — Redmine không có Link TCs human, TCs lấy từ Studio, xem `04-tc-list.md`. Đã chạy round 1: **42 pass / 3 fail / 1 error / 6 chưa chạy**, `aiResult = fail`, `reviewState = leader`. **2 bug con đã raise từ bộ TC này: `#39539`, `#39540`** — Leader cần đọc 2 ticket đó trước khi kết luận #38843.
- **Điều kiện tiên quyết để test**: cần account/bot ở các trạng thái hợp đồng khác nhau (đang hiệu lực · huỷ hợp đồng `status=3` có/không `is_active` · gói trả phí quá hạn > 23h · gói trả phí chưa thanh toán · gói free quá hạn 1 năm · ngày hết hạn NULL) + biến môi trường `ENABLE_PAYPAL` bật. Xem mục 5 file 03.
