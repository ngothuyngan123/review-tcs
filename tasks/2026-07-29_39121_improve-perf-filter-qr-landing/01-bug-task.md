# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39121 — Improve performance khi thực hiện filter ở modal filter theo điều kiện qrlanidng` |
| Redmine URL | https://redmine.watermelon.vn/issues/39121 |
| Auto-filled | `2026-07-29 by /new-task` |
| Ngày báo cáo | `2026-07-28` |
| Khách hàng / PM báo | `Do Van Tu TuDV` (author Redmine) |
| Module / Màn hình | `Friend Filter — modal lọc bạn bè theo điều kiện QR/landing` (dùng chung: Friend list, Broadcast, Scenario, Auto reply, Action schedule, Cross analysis) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `Production` (suy từ "bot lớn của khách" + "cấu hình prod" trong đánh giá ảnh hưởng — tester xác nhận lại) |

> Tracker Redmine: **SpecImprove** · Status: **Fix done - Đợi test** · Assigned to: **Ngô Thúy Ngần** · Custom field "Commit Date": 2026-07-29.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```sql
select count(*) as aggregate from `bot_line_user` inner join `line_user` on `line_user`.`id` = `bot_line_user`.`line_user_id` where (((select count(distinct(detail_landing_click.landing_id)) from detail_landing_click where detail_landing_click.landing_id in (477033) and line_user.line_id = detail_landing_click.line_id and action=2) > 0))
```

query này dùng ở đâu. đang bị lỗi performance > 300s

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- ⚠️ Redmine KHÔNG có section "Tái hiện bug" chính thức. Các bước dưới đây suy từ subject + description + đánh giá ảnh hưởng (Dev) — tester xác nhận lại trước khi dùng. -->

1. Vào một bot có **số bạn bè lớn** và một landing/QR có **nhiều lượt quét** (`detail_landing_click`).
2. Mở modal filter bạn bè (màn Friend list / Broadcast / Scenario / Auto reply / Action schedule / Cross analysis).
3. Thêm điều kiện lọc theo **QR/landing** (option `選択したQRコードアクションを1つ以上含む友だち` hoặc `...を除く友だち`).
4. Thực thi filter → đo thời gian query `select count(*) ... detail_landing_click ...`.

## Expected result

- Filter hoàn tất trong thời gian hợp lý, không timeout (suy luận — Redmine không ghi ngưỡng cụ thể).

## Actual result

- Query lọc bị **performance > 300s** (theo mô tả khách hàng) trên bot lớn.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue **không có attachment**. Log duy nhất là câu SQL trong description.

## Ghi chú thêm của Leader

⚠️ **Bug không có bước tái hiện chính thức trong Redmine** (không có section "Tái hiện bug"; đây là bug performance). Root cause đã được Dev (hệ thống Auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). **TCs nên tập trung: (1) verify kết quả filter KHÔNG đổi trước/sau fix (regression đúng đắn logic IN/NOT IN), (2) đo cải thiện performance trên bot lớn, (3) rà đủ các màn dùng chung `advanceFilterPost`.**

- Fix chỉ đổi **cách dựng câu SQL đọc** (subquery đếm có tham chiếu cột ngoài → subquery độc lập `IN`/`NOT IN`), **không ghi/sửa data, không đổi UI** → trọng tâm test là **kết quả lọc giữ nguyên** + **tốc độ**.
- Dev chưa đo được thời gian thật (MySQL dev không kết nối được lúc fix) → **bắt buộc đo EXPLAIN / thời gian trên bot lớn ở môi trường thật** (xem §6 VERIFY + phần rủi ro trong file 03).
