# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37188 — [Bill tiền tool] Số tiền bill trên univapay là 10780 nhưng trên tool mình ghi nhận là 116424` |
| Module / Màn hình | `Bill tiền tool — CRON thu tiền định kỳ Univapay (job:check_auto_payment_univapay) + callback hợp đồng lại (recontractV2) — Contract Plan & Payment (FA-031), Payment History (FS-009), Affiliate Payment Mgmt (FS-013)` |

## Mô tả bug (bản dịch tiếng Việt)

Check charge_id: 11f14f81-42e1-af7c-9b1d-5beb58f01eaf
Ngày bill: 2026-05-14 19:40
Email: mooochi010204@gmail.com

(Hiện tại anh Tư đã recover)

## Steps to reproduce

<!-- Redmine không ghi steps thao tác UI — đây là bug phía hệ thống (job + callback thanh toán Univapay), không phải thao tác tái hiện trên màn hình. Xem "Dữ liệu định danh ca lỗi" bên dưới + 03-dev-impact.md mục 1 (Nguyên nhân) để biết điều kiện phát sinh. -->

-

## Expected result

Số tiền ghi nhận trong lịch sử thanh toán (`payment_histories.amount`) khớp với số tiền THỰC THU trên Univapay cho giao dịch `charge_id: 11f14f81-42e1-af7c-9b1d-5beb58f01eaf` — tức khớp giá kỳ THÁNG `10780`.

## Actual result

Tool ghi nhận `116424` (= `10780 x 0.9 x 12`, đúng công thức giá kỳ NĂM `calculateSaleEnterprise`) cho một giao dịch thực tế đã thu theo kỳ THÁNG `10780` trên Univapay — lệch do callback thanh toán TÍNH LẠI số tiền từ trạng thái hợp đồng tại thời điểm callback chạy thay vì dùng số đã thu thật (xem 03-dev-impact.md mục 1).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue #37188 không có attachment (0). -->

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Production** — ca lỗi thật của khách (`mooochi010204@gmail.com`), đã được "anh Tư" recover tay bản ghi trong ticket này.
- ⚠️ Bug không tái hiện được qua thao tác UI — đây là lỗi logic tính tiền trong callback/job thanh toán định kỳ Univapay, root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng, xem `03-dev-impact.md`.
- Status Redmine hiện tại: **Fix done - Đợi test**.
- Dev KHÔNG kiểm chứng được bằng dữ liệu thật: MySQL dev `host.docker.internal:3306` Connection refused (dev stack đang tắt) — mức verify Dev đạt được chỉ là `php -l` (lint) + đối chiếu số học, **CHƯA chạy test thực tế trên bất kỳ env nào**.
- ⚠️ Có **RECOVER DATA** cần thiết cho các bản ghi `payment_histories` (và `payment_detail_aff` tương ứng) đã ghi sai số tiền TRONG QUÁ KHỨ trước fix — fix chỉ chặn phát sinh mới, KHÔNG tự sửa dữ liệu cũ — xem chi tiết ở `03-dev-impact.md` mục 5.
- Ticket gồm **2 nguyên nhân / 2 cách fix độc lập** trong cùng 1 journal: (1) thu tiền định kỳ (bill_job) — đúng ca báo lỗi trong ticket này; (2) hợp đồng lại (recontractV2) — case Dev tự bổ sung thêm ngày 2026-08-26, KHÔNG có trong mô tả gốc của ticket nhưng cùng nằm trong phạm vi branch fix `ai_fixbug_37188` — cần test cả 2.
- Dev tự ghi nhận: còn 3 handler callback khác cùng kiểu "tính lại tiền từ hợp đồng" nhưng NGOÀI phạm vi ticket này — chỉ ghi nhận, không fix (xem `03-dev-impact.md` mục 2).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra theo email khách trên production>` |
| Friend / Account | `mooochi010204@gmail.com` |
| Đối tượng cấu hình | `charge_id (Univapay): 11f14f81-42e1-af7c-9b1d-5beb58f01eaf` |
| Thời điểm lỗi | `2026/05/14 19:40` (ngày bill) |
| Đối chứng | `<chưa có case đối chứng cụ thể trong ticket — số học khớp chính xác công thức calculateSaleEnterprise(standard_year) = 116424, xem 03-dev-impact.md mục 6>` |

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #133178 (AI LME Fix bug — đánh giá ảnh hưởng đầy đủ, 2026-08-27) đã chuyển toàn bộ vào 03-dev-impact.md, không lặp lại nguyên văn ở đây. Đây cũng là journal note duy nhất của ticket (1 journal). -->
