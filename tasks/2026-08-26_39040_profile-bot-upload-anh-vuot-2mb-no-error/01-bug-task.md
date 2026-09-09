# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39040 — [Upload image][Profile bot] Không hiển thị thông báo lỗi khi OA thực hiện upload ảnh cho bot vượt dung lượng tối đa` |
| Redmine URL | https://redmine.watermelon.vn/issues/39040 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-07-24` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set Category; từ subject: `[Upload image][Profile bot]`) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description không ghi env. Ghi chú: journal Dev nêu "Không tái hiện được trên dev (web host.docker.internal:8000 không chạy)" |
| Trạng thái Redmine | `Fix done - Đợi test` (cập nhật 2026-08-25) |
| Assignee hiện tại | `Đoàn Thị Bích Hảo` |
| Commit Date (custom field) | `2026-08-21` |

## Mô tả bug (nguyên văn từ khách hàng)

```
Pre-Conditions:
- Limit ảnh cho bot là 2MB

Steps:
1. Đi đến màn profile của bot
2. Thực hiện upload ảnh cho bot
3. Chọn ảnh > 2MB
4. Quan sát hiển thị

Actuals:
4. Upload ảnh thành công

Expected:
4. Không upload ảnh được, hiển thị thông báo lỗi "2MB以下のをアップしてください。"

evidence: https://screenrec.com/share/wuzsYQgdkq
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

**Pre-Conditions:**
- Limit ảnh cho bot là 2MB

**Steps:**
1. Đi đến màn profile của bot
2. Thực hiện upload ảnh cho bot
3. Chọn ảnh > 2MB
4. Quan sát hiển thị

## Expected result

- 4. Không upload ảnh được, hiển thị thông báo lỗi `2MB以下のをアップしてください。`

## Actual result

- 4. Upload ảnh thành công

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video — link ngoài trong description (Redmine `attachments` rỗng): https://screenrec.com/share/wuzsYQgdkq
- [ ] Có log / request-response

## Ghi chú thêm của Leader

- ⚠️ Bug được fix bởi **AI Auto-fixbug LME** (journal 2026-08-21). Chi tiết đánh giá ảnh hưởng ở [03-dev-impact.md](03-dev-impact.md).
- ⚠️ Dev ghi rõ **không tái hiện được trên dev** khi fix — TCs phải verify được cả JS (client) lẫn server-side, và verify trên môi trường có upload thật.
- ⚠️ Dev nêu **lần chạy trước sửa nhầm màn cũ** (`/admin/bot-edit`) nên bug vẫn tái hiện — lần này sửa màn mới `/admin/setting-bot`. Cần test **cả 2 màn**.
- ⚠️ Rủi ro Dev tự nêu: ảnh 2MB–10MB trước đây lưu được thì nay bị chặn; **spec sprint #34620 (UP-07) bỏ ngỏ mục giới hạn dung lượng** → mức 2MB cần PM xác nhận.
- Không có Section "Link TCs" trong Redmine → TCs lấy từ MCP LME TEST STUDIO (xem [04-tc-list.md](04-tc-list.md)).
