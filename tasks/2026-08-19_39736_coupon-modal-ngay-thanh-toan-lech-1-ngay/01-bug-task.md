# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39736 — Ngày thanh toán tiền theo trên modal coupon đang lệch 1 ngày so với ngày` |
| Redmine URL | https://redmine.watermelon.vn/issues/39736 |
| Auto-filled | `2026-08-19 by /new-task` |
| Ngày báo cáo | `2026-08-19` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set category; theo journal repro: màn Point setting → Detail hợp đồng → modal クーポンコードを入力する) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description không ghi env. Tracker = **Bug KH** (bug khách hàng báo) → nghi Production, tester confirm lại. |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Khi nhập mã, hệ thống hiển thị「2026/09/26に延長」。
Vì ngày thanh toán tiếp theo là 2026/08/27, nên chẳng phải chính xác phải là đến 2026/09/27 sao？
=> export ngày trên modal coupon phải = ngày thanh toán tiền theo

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: journal #129304 — Hạnh Nguyễn, 2026-08-19T04:33:53Z. Paste nguyên văn. -->

Thao tác tái hiện: Admin tạo 1 coupon A => Copy mã coupon A

1. User vào màn point setting
2. 2. Click vào detail hợp đồng đang active đã thanh toán
3. Click button クーポンコードを入力する tại detail hợp đồng
4. Nhập mã coupon A
5. Click 次へ
6. Quan sát ngày trên modal

## Expected result

- Ngày hiển thị trên modal coupon = **ngày thanh toán tiếp theo** (theo ví dụ khách: `2026/09/27`).
- Nguyên văn khách: 「export ngày trên modal coupon phải = ngày thanh toán tiền theo」

## Actual result

- Modal hiển thị 「2026/09/26に延長」 — sớm hơn đúng **1 ngày** so với ngày thanh toán tiếp theo.
- Nguyên văn journal #129304: 「Đang hiển thị `bot_contracts.expired_date_contract` +1 tháng」

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue #39736 **không có attachment nào**.

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Bug do **AI AUTO-FIXBUG** xử lý (journal #129280, 2026-08-19T04:13:13Z) — status Redmine đã chuyển `Fix done - Đợi test`, assignee `Ngô Thúy Ngần`.
- Branch fix: `ai_small_39736` (base `release_step_20260805`, commit `8ef593df85`, 3 file). Xem `03-dev-impact.md`.
- ⚠️ Dev ghi nhận **quét ngang ngoài phạm vi ticket**: màn **Cài đặt điểm (Point setting)** cũng hiển thị nhãn "ngày thanh toán tiếp theo" bằng ngày hết hạn thô → **cùng kiểu lệch 1 ngày, CHƯA fix**, cần ticket riêng. Leader cân nhắc có đưa vào scope test hay không.
- ⚠️ Dev tự đánh giá liên quan bug cũ **#39383** (tái dùng hàm có sẵn độ lệch) → cân nhắc TC regression.
- Điều kiện tiền đề để repro: cần hợp đồng **đang active + đã thanh toán**, và 1 **mã coupon** do Admin tạo.
