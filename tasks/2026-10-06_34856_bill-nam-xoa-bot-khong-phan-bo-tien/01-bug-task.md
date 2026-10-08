# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34856 — [Bill tool] Hợp đồng bill năm đã bill tiền nhưng khi xóa bot contract thì mình lại không phân bổ nữa` |
| Module / Màn hình | `Bill tool — job phân bổ hiển thị doanh thu bill năm theo tháng (UpdateFlagDisplayBillYearAffByMonthly), liên quan luồng xóa bot contract (BotController::botDelete) & hoàn tiền (RefundController::rollbackPlan)` |

## Mô tả bug (bản dịch tiếng Việt)

Hợp đồng bill năm (gói 1 năm/2 năm) khi thu tiền đã sinh sẵn các dòng phân bổ (`payment_histories` / `payment_detail_aff`) theo từng tháng để job hằng ngày bật cờ hiển thị doanh thu đúng kỳ hạn. Khi bot bị xóa (hủy kết nối), bản ghi hợp đồng (`bot_contracts`) bị xóa cứng khỏi database → job phân bổ hằng ngày tra không ra hợp đồng nên **bỏ qua luôn các dòng phân bổ còn lại của năm đã thu tiền**, dẫn đến doanh thu/hoa hồng affiliate của các tháng còn lại trong năm không được ghi nhận dù khách đã trả tiền.

Case cụ thể được báo cáo:
- `univapay_charge_id: 11f0fc04-5c60-5348-96b8-0f046efa0d4e`
- Expect: Xóa bot (contract) vẫn phải tiếp tục phân bổ các dòng doanh thu còn lại của năm đã thu tiền.

## Steps to reproduce

<!-- Redmine không ghi Steps/Expected/Actual theo format chuẩn — xem ghi chú Leader bên dưới. -->

## Expected result

- Xóa bot contract (hoặc hợp đồng bị xóa cứng do hoàn tiền) **không được chặn** việc job hằng ngày bật cờ phân bổ (`flag_display`) cho các dòng `payment_histories` / `payment_detail_aff` của năm đã thu tiền khi tới hạn tháng.

## Actual result

- Hợp đồng bị xóa cứng (do xóa bot hoặc do đổi slot/nâng gói/hoàn tiền) → job `UpdateFlagDisplayBillYearAffByMonthly` tra không ra hợp đồng → bỏ qua các dòng phân bổ còn lại → doanh thu/hoa hồng affiliate của các tháng sau trong năm **vĩnh viễn không được phân bổ**, dù khách đã trả tiền trước đó (case `univapay_charge_id` nêu trên).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue không có attachment (0). -->

## Ghi chú thêm của Leader

- ⚠️ Bug **không có Steps/Expected/Actual theo format chuẩn** trong Redmine — mô tả gốc chỉ nêu 1 ca kiểm tra cụ thể qua `univapay_charge_id` + kỳ vọng ("xóa bot vẫn phải phân bổ"). Root cause + cách fix đã được Dev confirm đầy đủ qua đánh giá ảnh hưởng ở `03-dev-impact.md` (journal AI Auto-fixbug #133415) → TCs nên tập trung verify cách fix (job phân bổ vẫn chạy đúng khi hợp đồng đã bị xóa cứng) + regression (hợp đồng còn tồn tại vẫn giữ logic cũ, dòng không gắn hợp đồng vẫn bị bỏ qua).
- Status Redmine hiện tại: **Fix done - Đợi test**.
- ⚠️ Dev tự ghi trong journal #133415: môi trường dev không kết nối được DB (`host.docker.internal:3306` connection refused) nên **chưa đếm được số dòng phân bổ "mồ côi" thực tế** ngoài test bằng reflection (5 case giả lập) — QA nên tự verify lại bằng dữ liệu thật trên DB test/staging, không chỉ tin kết quả reflection của Dev.
- ⚠️ Rủi ro vận hành Dev tự nêu: sau khi release, **lần chạy job đầu tiên sẽ bật hàng loạt** các dòng phân bổ tồn đọng của các tháng đã qua → doanh thu & hoa hồng affiliate của các tháng cũ trong báo cáo sẽ **tăng đột ngột**. Đây là đúng mong đợi của ticket (tiền đã thu nhưng chưa phân bổ), nhưng cần TC verify số liệu tăng đúng — không tăng sai/thiếu/thừa.
- ⚠️ Hợp đồng bị xóa do **hoàn tiền** (`RefundController::rollbackPlan`) cũng sẽ được job phân bổ tiếp theo logic mới — Dev note các report hiện tại đều lọc `status_refund` nên không tính sai doanh thu, nhưng đây là điểm cần có TC regression riêng (case hoàn tiền không bị phân bổ nhầm doanh thu đã hoàn).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| univapay_charge_id | `11f0fc04-5c60-5348-96b8-0f046efa0d4e` |
| bot_id | `<chưa rõ — tra theo univapay_charge_id trên DB>` |
| Friend | `<không áp dụng — bug ở tầng job/billing, không gắn 1 friend cụ thể>` |
| Đối tượng cấu hình | `Hợp đồng bill năm (bot_contracts) đã bị xóa cứng do xóa bot / đổi slot / nâng gói / hoàn tiền` |
| Thời điểm lỗi | `<chưa rõ — Redmine không ghi mốc thời gian cụ thể>` |
| Đối chứng | `<chưa có — chưa thấy case hợp đồng còn tồn tại chạy đúng để đối chứng trong Redmine>` |

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #129928 chỉ quote lại nguyên văn description gốc (không có nội dung điều tra mới) → không chép lại. Journal #133415 (AI Auto-fixbug — nguyên nhân/cách fix/đánh giá ảnh hưởng) đã chuyển vào 03-dev-impact.md. -->
