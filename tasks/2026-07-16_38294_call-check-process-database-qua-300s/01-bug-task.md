# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38294 — [Lme][call] Check process database quá 300s` |
| Redmine URL | `https://redmine.watermelon.vn/issues/38294` |
| Auto-filled | `2026-07-16 by /new-task` |
| Ngày báo cáo | `2026-06-29` |
| Khách hàng / PM báo | `Pham Dinh Vinh` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không có category; theo file 03: modal lọc bạn ở màn Gửi tin hàng loạt / Danh sách hội thoại) |
| Priority | `High` |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi rõ; alert dạng `[call]` + branch fix gốc `release_step_20260623`) |

## Mô tả bug (nguyên văn từ khách hàng)

```
[Step](call)Check process database quá 300s
Req: SELECT COUNT(*)
FROM information_schema.processlist
WHERE TIME > 300 AND information_schema.processlist.db is not null AND command <> "Sleep" AND USER <> 'xtrabackup_lme' AND USER <> 'dump-analytics'
Expect: 0 - Result: 1

6/26 8:51 VNT
```

**Journal bổ sung (2026-07-03 — Pham Dinh Vinh)** — query thực tế gây treo:

```
Tư:
select count(*) as aggregate from bot_line_user where (((select count(tag_line_user.tag_id) from tag_line_user where tag_line_user.tag_id IN (...) and bot_line_user.line_user_id = tag_line_user.line_user_id) > 0 and date(bot_line_user.followed_at) >= '2025-11-18' and date(bot_line_user.followed_at) <= '2026-06-18'));
@sato_kevin  cái này do query modal filter. chỗ này sẽ sửa imporve lại
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Chạy câu query monitor trên DB (theo dõi process đang chạy):
   ```sql
   SELECT COUNT(*)
   FROM information_schema.processlist
   WHERE TIME > 300 AND information_schema.processlist.db is not null AND command <> "Sleep"
     AND USER <> 'xtrabackup_lme' AND USER <> 'dump-analytics'
   ```
2. Thời điểm phát hiện: 6/26 8:51 VNT.
3. Process bị treo là query đếm bạn của **modal lọc** (lọc theo tag + ngày kết bạn) — xem journal 2026-07-03.

## Expected result

- Kết quả query monitor = `0` (không có process nào chạy quá 300s).

## Actual result

- Kết quả query monitor = `1` (có 1 process chạy quá 300s — query `count(*) from bot_line_user` với subquery đếm tag + `date(followed_at)`).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — query SQL gây treo được paste trong journal Redmine (2026-07-03), không có file attachment.

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được qua thao tác UI trong Redmine (đây là alert monitor DB, không phải bug chức năng) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (rewrite query sargable + EXISTS/NOT EXISTS) + regression impact (kết quả lọc KHÔNG đổi trước/sau fix).
