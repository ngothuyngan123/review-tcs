# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34227 — [Form] Item radio,khi edit xong sort label => nhấn save các lable bị nhảy thứ tự` |
| Redmine URL | https://redmine.watermelon.vn/issues/34227 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2026-02-06` |
| Khách hàng / PM báo | `Kim Cúc` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set category, không có custom field; subject có prefix `[Form]`) |
| Priority | `Medium` (Redmine priority = `Normal`) |
| Môi trường phát hiện | `<chưa rõ>` — description không ghi môi trường |

**Thông tin Redmine bổ sung (không nằm trong template, giữ để trace):**

| Trường | Giá trị |
|---|---|
| Tracker | `Bug tự detect` |
| Trạng thái hiện tại | `Fix done - Đợi test` |
| Assignee hiện tại | `Đoàn Thị Bích Hảo` |
| Project | `Lme` |
| Cập nhật lần cuối | `2026-08-25` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Mô tả:
1. Tạo item radio
2. Setting Chọn add tag
3. Tạo các lable radio
4. Edit lable sau đó sort lable => save thì thứ tự lable bị nhảy

Video: https://screenrec.com/share/wjPYmUSXdh
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Trích nguyên văn từ danh sách đánh số trong "Mô tả:" của Redmine. Redmine KHÔNG có heading "Tái hiện bug" riêng. -->

1. Tạo item radio
2. Setting Chọn add tag
3. Tạo các lable radio
4. Edit lable sau đó sort lable => save thì thứ tự lable bị nhảy

## Expected result

- `<Redmine không ghi rõ — tester fill>` — description chỉ mô tả hiện tượng sai, không phát biểu kết quả mong đợi.

## Actual result

- Nguyên văn (bước 4): "Edit lable sau đó sort lable => save thì thứ tự lable bị nhảy"

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video
- [ ] Có log / request-response

- Video: https://screenrec.com/share/wjPYmUSXdh (link trong description; Redmine **không** có file attachment nào)

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- ⚠️ Redmine **không có heading "Tái hiện bug"** riêng — phần Steps ở trên lấy từ danh sách đánh số trong "Mô tả:". Expected result không được phát biểu trong ticket.
- ⚠️ Bug được fix bởi **hệ thống Auto-fixbug LME** (journal 2026-08-25), không phải dev người. Chi tiết đánh giá ảnh hưởng ở `03-dev-impact.md`.
- ⚠️ Report của Dev nêu rõ: **không bump `config('sns-line.version')`** → trình duyệt có thể còn cache bản JS cũ, **phải hard reload (Ctrl+F5)** trước khi test.
- ⚠️ Report của Dev nêu rõ: **không kiểm chứng được bằng trình duyệt** (stack dev không chạy, MySQL connection refused) → toàn bộ verify thao tác kéo-thả phụ thuộc vào tester.
