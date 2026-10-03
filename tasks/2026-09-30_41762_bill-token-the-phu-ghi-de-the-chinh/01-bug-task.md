# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41762 — [30-09-2026] [TY-12269] [Bill tiền tool] Hỏi lý do thanh toán dùng thẻ phụ thay vì thẻ chính` |
| Module / Màn hình | `Bill tiền tool — Chi tiết hợp đồng (đăng ký/đổi thẻ phụ) + CRON thu tiền định kỳ (job:check_auto_payment_univapay) — Contract Plan & Payment (FA-031), Payment System Integration (FA-034)` |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12269
担当 (phụ trách): 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790734786584059?thread_ts=1790734786.584059&cid=C0BALS7S73L
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12269

管理No：TY-12269
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C51NS7CPR
Địa chỉ: lme@compass-bodymake.co.jp
Tên LOA: 対人支援コーチングプログラム『CORE』
Phụ trách: 沖原
Tool: リンク

Nội dung yêu cầu:
Hiện tại thẻ tín dụng đang đăng ký trên LME là:
・Thẻ thanh toán chính 4 số cuối「2019」
・Thẻ thanh toán phụ 4 số cuối「5190」
nhưng vào ngày 20/9, giao dịch thanh toán đã được thực hiện bằng「5190」.
Tại sao thẻ「2019」lại không được dùng để thanh toán?

## Steps to reproduce

<!-- Nguồn: Journal #139407 — Kim Cúc — 2026-09-30 (mục "Tái hiện bug KH:") -->

1. Card chính (univa_transaction_token) bị lỗi
2. Bot_contract có add thêm card phụ
3. Expired_date đã hết hạn (nhưng chưa quá 7 ngày)
4. Job bill hàng ngày bill tiền

## Expected result

<!-- Redmine không ghi expected result tường minh. Suy từ mô tả UI đăng ký thẻ phụ (メインカードの決済が失敗した場合に自動的にサブカードで決済を行います) — xem 03-dev-impact.md mục 1/2 — nhưng đây là diễn giải của Dev, KHÔNG phải trích dẫn khách/QA. -->

-

## Actual result

Trong bảng `payment_histories`, trường `last_four_card` của lần job bill thanh toán bị lấy theo card phụ từ lần thanh toán mới, thay vì thẻ chính — token thẻ định kỳ trên hợp đồng đã bị ghi đè bằng token thẻ phụ nên từ kỳ sau mọi lần thu tiền đều trừ thẻ phụ, thẻ chính (hiển thị 2019) không bao giờ được thử lại. (Journal #139407 + Journal #139403)

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/31183/SnapCrab_NoName_2026-9-30_11-19-1_No-00.png
- https://redmine.watermelon.vn/attachments/download/31184/SnapCrab_NoName_2026-9-30_11-19-9_No-00.png

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Production** (khách hàng thật, `lme@compass-bodymake.co.jp` — 対人支援コーチングプログラム『CORE』). Đây là bug về logic thu tiền định kỳ (webhook Univapay + job nền), không phải bug UI đơn thuần.
- Bug KHÔNG tái hiện qua thao tác UI đơn lẻ — cần dựng chuỗi trạng thái hợp đồng (thẻ chính lỗi → có thẻ phụ → quá hạn 1-7 ngày → chạy job bill hàng ngày) mới quan sát được hiện tượng.
- Dev không verify được bằng dữ liệu thật: MySQL dev `host.docker.internal:3306` connection refused; hợp đồng của khách nằm ở DB production. Mức verify Dev đạt được chỉ là `php -l` (lint) + đối chiếu code — **CHƯA chạy test thực tế trên bất kỳ env nào**.
- ⚠️ Có **RECOVER DATA** cần thiết cho các hợp đồng cũ đã bị ghi đè token trước khi có fix (token thẻ chính cũ KHÔNG phục hồi được từ DB) — xem chi tiết ở `03-dev-impact.md`.
- Dev tự đính chính (tự review v2) rằng 1 trong 3 lối vào ban đầu nêu ra (tái ký hợp đồng chọn thẻ phụ) **không** gây được hiện tượng của ticket này — chỉ 2 lối vào thật: webhook `bill_job` và đăng ký/đổi thẻ phụ lúc hợp đồng quá hạn.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra theo email khách trên production>` |
| Friend / Account | `lme@compass-bodymake.co.jp — 対人支援コーチングプログラム『CORE』` |
| Đối tượng cấu hình | Thẻ thanh toán chính 4 số cuối `2019`, thẻ thanh toán phụ 4 số cuối `5190` |
| Thời điểm lỗi | `2026/09/20` (giao dịch bị trừ bằng thẻ phụ 5190 thay vì thẻ chính 2019) |
| Đối chứng | `<chưa có case đối chứng cụ thể trong ticket>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #139407 — Kim Cúc — 2026-09-30:**

```
Tái hiện bug KH:
1. Card chính univa_transaction_token bị lỗi
2. Bot_contract có add thêm card phụ
3. Expired_date đã hết hạn( nhưng chưa quá 7 ngày)
4. Job bill hàng ngày bill tiền

Hiện tượng: trong bảng payment_histories trường last_four_card job bill thanh toán bị lấy theo card phụ từ lần thanh toán mới
```

<!-- Journal #139403 (AI LME Fix bug — đánh giá ảnh hưởng đầy đủ) đã chuyển toàn bộ vào 03-dev-impact.md, không lặp lại nguyên văn ở đây. -->
