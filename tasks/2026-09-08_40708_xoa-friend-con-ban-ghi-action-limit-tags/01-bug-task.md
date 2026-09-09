# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40708 — Khi xóa friend chưa xóa bản ghi khỏi bảng action_limit_tags` |
| Module / Màn hình | Friend List (FA-013) — xóa friend trên tool · liên quan Tag Management (FA-012) — 「制限到達後のタグ追加時アクション」 (action khi tag đạt giới hạn) · Action Settings (SC-004) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine gốc đã viết bằng tiếng Việt — giữ nguyên văn, không dịch lại. -->

Tag A có setting action limit (giới hạn số người) gắn tag B khi đạt giới hạn. Friend thỏa mãn giới hạn thì được gắn tag B. Nhưng sau khi **xóa friend trên tool** rồi **kết bạn lại và gắn lại tag A**, friend **không được gắn tag B nữa**.

> **BUG:** Friend lúc này không được gắn tag B nữa.
>
> **=> Expect:** Khi tag A bị limit thì friend vẫn phải được gắn tag B.

## Steps to reproduce

1. Tag A có setting action limit gắn tag B khi đạt giới hạn limit.
2. Friend thỏa mãn giới hạn limit => Được gắn tag B.
3. Xóa friend trên tool => Kết bạn lại và gắn lại tag A.

## Expected result

- Khi tag A bị limit thì friend vẫn phải được gắn tag B.

## Actual result

- Friend lúc này không được gắn tag B nữa.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40708 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

- **Tracker Redmine = `Bug tự detect`** — bug do nội bộ tự phát hiện, KHÔNG phải khách hàng báo. Ticket không ghi môi trường phát hiện, không có ID ca lỗi thật, không có attachment.
- **Ticket không ghi tần suất lỗi.** Theo mô tả root cause (bản ghi cũ còn sót trong `action_limit_tags` chặn lần chạy action mới) thì lỗi mang tính **tất định 100%** khi đủ điều kiện: friend đã kích hoạt action → bị xóa → kết bạn lại → gắn lại tag đang đầy.
- **Điều kiện tiên quyết để dựng env test:** tag A bật 「人数制限」=「制限する」 và **đã đầy**; phần 「制限到達後のタグ追加時アクション」 có cấu hình hành động gắn tag B; chế độ chạy action 「1度のみアクション稼働」 (1 lần) là chế độ tái hiện được bug — chế độ 「何度でもアクション稼働」 (nhiều lần) không bị chặn nên không lộ bug.
- ⚠️ **Fix chạm 2 phần khác nhau, phải test tách bạch:**
  1. **Fix gốc** — thêm bước xóa `action_limit_tags` vào hàm dọn dữ liệu chung `removeHistoryLineUser`, ảnh hưởng **cả 4 đường xóa friend** (xóa 1 friend ở màn danh sách, xóa 1 friend đã chặn, xóa nhiều friend đã chặn, xóa friend từ app).
  2. **Command recover** `php artisan recover:actionLimitTagOrphan` — **XÓA VĨNH VIỄN** dữ liệu mồ côi tồn đọng, không có bước hoàn tác. Phải chạy `--dry-run` đếm trước + backup bảng trước khi chạy thật.
- ⚠️ **Điểm Dev tự nêu là chưa chốt (cần Leader/BA xác nhận trước khi đóng ticket):**
  - Command recover dọn **mọi** dòng mồ côi, kể cả mồ côi do **nguyên nhân khác** (vd bot bị xóa) — rộng hơn phạm vi bug gốc.
  - Friend chỉ **CHẶN / bỏ theo dõi**, hoặc bị **gỡ tag ở màn quản lý tag**, vẫn giữ bản ghi `action_limit_tags` → Dev ghi "chờ BA xác nhận".
- ⚠️ **Dev CHƯA chạy được trên dữ liệu thật** — MySQL dev `Connection refused` tại thời điểm implement, mới chỉ verify mức `php -l` + `php artisan list` + in SQL sinh ra. Toàn bộ hành vi trên data thật còn nguyên rủi ro, QA phải verify từ đầu.

## Journal / note từ Redmine (nguyên văn)

**Journal #135225 — AI LME Fix bug — 2026-09-08:**

Journal duy nhất của ticket là báo cáo **AI AUTO-FIXBUG** (đã fix xong, chuyển test). Toàn bộ 6 mục của báo cáo đã được chép sang [03-dev-impact.md](03-dev-impact.md) — không lặp lại ở đây để tránh 2 bản lệch nhau.

Trích riêng câu SQL người phụ trách đưa cho bước recover data (dữ liệu định danh phạm vi dọn):

```sql
DELETE alt FROM action_limit_tags alt
LEFT JOIN bot_line_user blu
  ON blu.line_user_id = alt.line_user_id
 AND blu.bot_id = alt.bot_id
WHERE blu.id IS NULL;
```

```
(nên chạy SELECT COUNT(*) cùng điều kiện để đếm trước, và chạy theo lô nếu số lượng lớn)
phạm vi: Toàn bộ dòng action_limit_tags không còn cặp (bot_id, line_user_id) trong bot_line_user
         — chỉ là dữ liệu ghi dấu, xóa không ảnh hưởng thẻ hay hành động đang chạy
```

Branch để QA checkout: `ai_small_40708` (sns-line, nhánh gốc `release_step_20260805`, commit `d5355ff361`, 2 file — đã push).
