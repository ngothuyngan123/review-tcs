# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | KH #36202 |
| Ngày báo cáo | 2026-05-01 |
| Khách hàng / PM báo | `<member điền>` |
| Module / Màn hình | Quản lý Staff (admin) |
| Priority | High |
| Môi trường phát hiện | `<member xác nhận — mặc định Production (step.lme.jp)>` |

## Mô tả bug (nguyên văn từ khách hàng)

Bug KH #36202: [01-05-2026][Quản lý Staff] Mặc dù bot plan standard nhưng vẫn được tạo > 10 staff

## Steps to reproduce

1. Vào màn quản lý staff
2. Thao tác tạo account staff (qua invite link)
3. Lặp lại bước 2 đến khi tạo > 10 staff cho bot plan standard

## Expected result

- Bot **free**: KHÔNG được phép tạo staff
- Bot **standard**: được tạo tối đa **10 staff** (không bao gồm user chính)
- Bot **pro**: KHÔNG giới hạn tạo staff

## Actual result

- Bot plan standard vẫn cho phép tạo > 10 staff (vượt quá limit)

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

- Cần Dev xác nhận: con số chính xác (10) có hard-code không, hay đọc từ config plan? — ảnh hưởng cách viết TC.
- Cần làm rõ: "không bao gồm user chính" nghĩa là count = 10 staff + 1 user chính = 11 total user/bot, hay count khác?
