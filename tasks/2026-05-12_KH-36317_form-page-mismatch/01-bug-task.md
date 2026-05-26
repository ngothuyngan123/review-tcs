# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | KH #36317 |
| Ngày báo cáo | 2026-05-08 |
| Khách hàng / PM báo | (KH — 回答ID 28091) |
| Module / Màn hình | Form (LINE user trả lời form) → Google Spreadsheet sync + Form result |
| Priority | High (regression nghi vấn — sai data result phía KH) |
| Môi trường phát hiện | Production |

## Mô tả bug (nguyên văn từ khách hàng)

[08-05-2026][回答ID：28091][Form] Form ver3.0 終了報告: response trang nhánh sâu 3-levels bị reflect ngược lên start page (có thể regression).

Tóm tắt nội bộ (bằng VN): Friend trả lời form ở page 3 nhưng dữ liệu trả lời lại sync vào page 1 trên Google Spreadsheet (và/hoặc form result phía admin).

## Steps to reproduce

1. Admin tạo form ver3.0 có nhiều page (rẽ nhánh sâu ≥ 3 levels).
2. Friend (LINE user) trả lời form, có nhập câu trả lời ở page 3 (page nhánh sâu).
3. Friend submit form.
4. Admin mở Google Spread đã liên kết với form / mở form result trên admin web → kiểm tra dữ liệu của回答ID 28091.

## Expected result

- Câu trả lời page 3 được ghi nhận **đúng cột tương ứng page 3** trên Google Spread.
- Form result phía admin hiển thị câu trả lời đúng page.

## Actual result

- Câu trả lời của page 3 bị sync ngược lên page 1 trên Google Spread (sai cột / sai page).
- Phía dev: chưa tái hiện được khi reproduce nội bộ → chưa tìm được **root cause**.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response (回答ID 28091 trên production)

## Ghi chú thêm của Leader

- Bug có dấu hiệu **regression** (form ver3.0). Cần verify cả trên form rẽ nhánh thực sự (deep ≥3 levels).
- Dev chưa tìm được root cause → cách fix hiện tại là **workaround**: chặn submit + hiện message tiếng Nhật khi tổng số câu trả lời/page khác setting admin.
- Vì là workaround, TCs phải:
  1. Verify workaround chạy đúng (message hiện trong các trường hợp mismatch).
  2. Cố gắng tái hiện scenario gốc của KH để xác nhận workaround **che được** lỗi này (kể cả khi root cause chưa rõ).
  3. Verify data sau submit ở Google Spread **và** form result (đây mới là nơi KH thấy sai).
