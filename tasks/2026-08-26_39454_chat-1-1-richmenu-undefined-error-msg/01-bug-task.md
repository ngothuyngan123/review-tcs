# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39454 — [Chat 1: 1][Rich menu] Khi add hiển thị rich menu từ màn chat 1:1, case rich menu không tồn tại, sửa lại error message` |
| Redmine URL | https://redmine.watermelon.vn/issues/39454 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-08-07` |
| Khách hàng / PM báo | `Ngọc Ánh` (author Redmine) |
| Module / Màn hình | `<Redmine category TRỐNG>` — suy từ subject: **Chat 1:1 × Rich menu** (panel 基本情報, ô Rich menu) — *tester xác nhận lại* |
| Priority | `Medium` (Redmine priority = **Low**; journal #130774 ngày 2026-08-20 do Hoang Xuan Thang đổi `Normal → Low` và tracker `19 → 14 (Bug tự detect)`) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` |
| Trạng thái Redmine | `Fix done - Đợi test` · tracker `Bug tự detect` · project `Lme` · assignee hiện tại `Ngọc Ánh` (đổi 2026-08-25 bởi Ngô Thúy Ngần) |
| Ticket liên quan | https://redmine.watermelon.vn/issues/39422 (Ticket refer, Dev ghi trong description) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #39454. KHÔNG diễn giải lại. -->

```
Hiện tượng: khi richmenu được tạo từ phía tool khác, không phải từ lme tool. Khi add hiển thị rich menu đó từ màn chat 1:1 thì đang hiển thị 「undefined」
Update: Hiển thị message:
LINE公式アカウントからリッチメニューが削除されました。併用している他のツールが影響している可能性があります。
該当のリッチメニューを編集・保存すると、再作成できます。

Ticket refer: https://redmine.watermelon.vn/issues/39422
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #39454 KHÔNG có section "Tái hiện bug" / "再現手順". Để trống theo nguyên tắc không bịa. -->

*(Redmine không cung cấp — xem "Ghi chú thêm của Leader" bên dưới)*

## Expected result

<!-- Redmine KHÔNG có section Expected riêng. Yêu cầu duy nhất suy từ dòng "Update: Hiển thị message" trong description. -->

- Popup ở màn chat 1:1 hiển thị đúng message tiếng Nhật:
  `LINE公式アカウントからリッチメニューが削除されました。併用している他のツールが影響している可能性があります。`
  `該当のリッチメニューを編集・保存すると、再作成できます。`

## Actual result

<!-- Redmine KHÔNG có section Actual riêng. Suy từ dòng "Hiện tượng" trong description. -->

- Popup hiển thị 「undefined」.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*(Redmine #39454: `attachments` = **rỗng**, không có file đính kèm nào.)*

## Ghi chú thêm của Leader

⚠️ **Bug không có section "Tái hiện bug" trong Redmine** (Steps / Expected / Actual không được ghi tách bạch) — root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

⚠️ **Điều kiện tái hiện cốt lõi** (suy từ description + mục 1 file 03): rich menu tồn tại trong DB LME nhưng **không còn / chưa từng có id phía LINE** — thường do rich menu bị xóa từ tool khác dùng song song với LME, hoặc do đăng ký lên LINE thất bại nên `rich_menus.rich_menu_id` rỗng.

⚠️ **Dev tự ghi trong §6 VERIFY: KHÔNG tái hiện được trên dev** (MySQL `host.docker.internal:3306` connection refused, và không được phép gọi API LINE từ container). Mức verify của Dev chỉ là **`lint`** — chưa có bằng chứng chạy thật.

⚠️ Ticket refer **#39422** — Leader kiểm tra xem có phải cùng cụm rich menu bị xóa từ tool ngoài hay không, để chốt phạm vi regression.
