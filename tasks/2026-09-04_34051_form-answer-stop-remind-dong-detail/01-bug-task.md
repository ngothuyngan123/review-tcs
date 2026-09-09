# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34051 — [Detail form-answer] Sau khi nhấn stop remind thì màn hình bị hiển thị đóng detail form-result` |
| Redmine URL | https://redmine.watermelon.vn/issues/34051 |
| Auto-filled | `2026-09-04 by /new-task` |
| Ngày báo cáo | `2026-01-30` |
| Khách hàng / PM báo | `Thanh Phương` (author = assigned_to) |
| Module / Màn hình | `<chưa rõ — Redmine không set category/custom field>`. Suy từ subject: **Detail form-answer** — màn danh sách câu trả lời biểu mẫu **V3**, popup chi tiết, tab リマインド (nhắc lịch). Tester confirm lại. |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>`. Note: Dev ghi **không tái hiện được trên dev qua giao diện** (file 03, mục Verify). |

### Metadata Redmine bổ sung

| Trường | Giá trị |
|---|---|
| Tracker | `Bug tự detect` |
| Status | `Fix done - Đợi test` |
| Parent issue | `#26684` (trước 2026-08-21 là `#33350` — "[Form] Update design item remind") |
| Attachments / Relations | Không có |
| Journals | 3 (1 note nội dung = báo cáo AI Auto-fixbug 2026-08-21; 2 note còn lại chỉ đổi assignee/tracker/parent) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #34051. KHÔNG diễn giải lại. -->

```
Exp: Khi nhấn stop thì màn hình vẫn hiển thị được đang mở vào detail form-result, trạng thái đã stop remind
```

> ⚠️ Description Redmine **chỉ có đúng 1 dòng Expected**, không có section "Tái hiện bug" / Steps / Actual.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug"/Steps. Các bước dưới đây suy từ subject + mục 1 "Nguyên nhân" của Dev (file 03) — tester phải verify lại trước khi dùng. -->

1. Mở màn danh sách câu trả lời biểu mẫu bản **V3** (`/basic/form-answer/v3/result/{id}`).
2. Bấm vào 1 câu trả lời có nhắc lịch (remind) đang hoạt động → popup chi tiết mở.
3. Chuyển sang tab 「リマインド」.
4. Bấm nút dừng gửi 「配信停止」 → xác nhận ở hộp thoại.

## Expected result

<!-- Nguyên văn từ description Redmine. -->

- Khi nhấn stop thì màn hình **vẫn hiển thị được đang mở vào detail form-result**, trạng thái **đã stop remind**.

## Actual result

<!-- Redmine KHÔNG có mục Actual riêng — nội dung dưới đây lấy nguyên văn từ SUBJECT của ticket. -->

- Sau khi nhấn stop remind thì màn hình bị **đóng detail form-result** (người dùng bị văng khỏi màn chi tiết).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> `issue.attachments` rỗng — ticket **không có** file đính kèm nào.

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** + **regression impact**.

Bổ sung:

- Ticket này do **AI Auto-fixbug LME** xử lý (journal 2026-08-21), không phải Dev người. Toàn bộ nội dung file 03 là báo cáo tự động — Leader nên soi kỹ mục 3 (caller đã check) và mục 4.
- Dev **không tái hiện được trên dev qua giao diện** (thiếu tài khoản + biểu mẫu có mục nhắc lịch + câu trả lời thực tế); root cause xác định **bằng đọc mã**, verify chỉ ở mức `lint` (`node --check`). → Bằng chứng fix **chưa có evidence chạy thực tế**.
- Fix **chỉ sửa 1 file JS**, **KHÔNG bump số phiên bản tài nguyên tĩnh** (không đụng `config/sns-line.php`) → rủi ro **cache-busting** sau deploy: browser đã cache `form_result_v3.js` cũ có thể vẫn dùng bản còn bug.
- Bug đã tồn tại từ **2026-01-30**, fix **2026-08-21** — kiểm tra xem UI màn form-answer V3 có thay đổi trong ~7 tháng đó không (base fix = `release_step_20260805`).
