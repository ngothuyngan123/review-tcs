# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38312 — Khi lưu lịch sử thay đổi friend info chưa lưu được action preview` |
| Redmine URL | https://redmine.watermelon.vn/issues/38312 |
| Auto-filled | `2026-07-02 by /new-task` |
| Ngày báo cáo | `2026-06-29` |
| Khách hàng / PM báo | `Do Van Tu TuDV` (author) — repro + report ảnh hưởng do `Thanh Phương` bổ sung trong journal |
| Module / Màn hình | `<chưa rõ — Redmine không set category>` (suy từ mô tả: Detail friend → Lịch sử thay đổi friend info; nguồn phát sinh: Event booking / Admin booking) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi>` (TCs trong Sheet test trên Staging `staging.lme.jp`) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

> ⚠️ Redmine description **trống**. Toàn bộ nội dung tái hiện bug + đánh giá ảnh hưởng nằm trong **journal (comment)** của Thanh Phương ngày 2026-06-29. Paste nguyên văn bên dưới.

**Tái hiện Bug:**
- Event có setting form nhập có liên kết friend info select + value của info có setting action
- Admin thực hiện booking cho user => user được gán friend info và send action
- Bug: Màn lịch ử friend info ở detail friend cột action đang hiện text không có action 設定なし

**Branch code (journal riêng của Do Van Tu TuDV):** `bugs/fix_bug_friend_info_20260629`

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Tạo/dùng Event có setting form nhập, có liên kết friend info dạng **select**, và trong **value** của info select có **setting action**.
2. Admin thực hiện **booking cho user** (màn Admin booking).
3. User được gán friend info tương ứng và send action.
4. Mở **Detail friend** → màn **Lịch sử thay đổi friend info** → xem cột **action**.

## Expected result

- Cột action của lịch sử friend info hiển thị 「プレビュー」 (preview) → click vào hiện được **preview action** đã setting.

## Actual result

- Cột action hiển thị text 「設定なし」 (không có action) — preview action **không được lưu**.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine attachments rỗng. -->

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug **không có Steps/Expected/Actual tách sẵn trong Redmine** — các mục trên được suy ra từ đoạn "Tái hiện Bug" trong journal. Tester nên đọc lại journal gốc để xác nhận trước khi review/viết TC.
