# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40171 — Tối ưu performance query count filter friend` |
| Redmine URL | https://redmine.watermelon.vn/issues/40171 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-08-25` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `<chưa rõ — Redmine không set category; theo file 03 mục 4.3: Friend Filter / Segment (SC-003)>` |
| Priority | `High` (Redmine priority = High) |
| Môi trường phát hiện | `<chưa rõ — description chỉ có câu SQL, không ghi môi trường>` |

**Metadata khác từ Redmine:**

| Trường | Giá trị |
|---|---|
| Project | Lme |
| Tracker | **Improve nội bộ** (KHÔNG phải Bug) |
| Status | Fix done - Đợi test |
| Assigned to | Ngô Thúy Ngần |
| Created / Updated | 2026-08-25T10:14:55Z / 2026-08-26T10:26:33Z |
| Attachments / Relations | 0 / 0 |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```sql
select count(*) as aggregate from `bot_line_user` where `bot_line_user`.`bot_id` = 97640 and `bot_line_user`.`is_blocked` = 0 and ((`bot_line_user`.`line_user_id` in (select `line_id` from `conversation` where `bot_id` = 97640 and (`status_last_message` in ('0') or `id_status` in ('0'))) and `bot_line_user`.`line_user_id` in (select `line_id` from `conversation` where `bot_id` = 97640 and `id_status` in (1454902, 1454916))))
```

> Toàn bộ description Redmine chỉ gồm câu SQL trên — không có mô tả hiện tượng, không có số liệu thời gian chạy trước/sau.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống, tester bổ sung nếu dựng được env. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #40171 KHÔNG có attachment nào.

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Bổ sung 3 điểm Leader cần lưu ý (lấy nguyên văn/trích từ Redmine, KHÔNG suy diễn):

1. **Tracker = "Improve nội bộ"**, không phải Bug — đây là ticket **tối ưu performance**, không có hiện tượng lỗi chức năng. Tiêu chí "đạt" chủ yếu là: (a) **kết quả lọc / số đếm KHÔNG đổi** so với trước fix, (b) thời gian chạy giảm. Dev khẳng định "Điều kiện lọc và kết quả trả về giữ nguyên".
2. **Dev CHƯA đo được trước/sau bằng EXPLAIN** — nguyên văn mục 6 (file 03): *"CHƯA EXPLAIN được trên môi trường dev: MySQL host.docker.internal:3306 và web :8000 đều Connection refused trong lúc xử lý — cần dev/QA chạy EXPLAIN để đo trước/sau"*. Mức verify của Dev mới là **unit-test** (khoá hình dạng SQL), chưa có bằng chứng chạy thật trên DB.
3. **Báo cáo Dev có mâu thuẫn nội bộ giữa mục 2 và mục 6/TỰ REVIEW** về cách fix cuối cùng (`CAST(line_id AS SIGNED)` hay `conversation.tb_line_user_id`) — xem cảnh báo chi tiết ở đầu file [03-dev-impact.md](03-dev-impact.md). **Phải chốt với Dev trước khi viết/review TC**, vì 2 cách này có rủi ro khác nhau (`tb_line_user_id` cho phép NULL → nguy cơ lọc THIẾU bạn bè).
4. Bot dùng trong câu SQL: `bot_id = 97640`; điều kiện lọc gồm `status_last_message`, `id_status` (`1454902`, `1454916`) — dữ liệu tham chiếu để dựng case tương đương.
