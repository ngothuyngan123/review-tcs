# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40380 — Salon booking khi access vào màn hình booking đang chậm và bị tốn tài nguyên serve` |
| Redmine URL | https://redmine.watermelon.vn/issues/40380 |
| Auto-filled | `2026-08-30 by /new-task` |
| Ngày báo cáo | `2026-08-29` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine `category` = trống, không có custom field Module/Screen) |
| Priority | `High` (Redmine priority = High) |
| Môi trường phát hiện | `<chưa rõ>` — description không nêu env phát hiện. Chỉ ghi `branch production: release_step_20260827` |

**Thông tin Redmine bổ sung** (không nằm trong template chuẩn nhưng cần cho reviewer):

| Trường | Giá trị |
|---|---|
| Project | Lme |
| Tracker | **`Bug tự detect`** — ticket do hệ thống/AI tự phát hiện, không phải khách hàng báo |
| Status | `Fix done - Đợi test` |
| Assigned to | Do Van Tu TuDV |
| Journals / notes | **0** (không có comment nào) |
| Attachments | **0** |
| Relations | **0** |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description từ Redmine #40380. KHÔNG diễn giải lại. -->

```

1. Nguyên nhân: Tầng 1 — N+1 thật sự. CalendarSalonLineBookingService.php:2559 gọi getListBookingByGoogleConfirm trong foreach ($listTimeNew as $item). $listTimeNew2 là danh sách ca làm việc = staff × ngày × ca → 30 staff × 7 ngày ≈ 210 query. Khác với getListBookingByDate ở ngay trên (đã có array_key_exists($dateBook, ...) memo hoá theo ngày) — nhánh Google không hề memo hoá.

Tầng 2 — nhân 5. handleShowListBooking:4293 có for ($i = 0; $i <= 3; $i++) gọi getListTimeBooking tối đa 4 lần, cộng 1 lần fallback ở :4363 → ~1000 query / 1 request khi tuần hiện tại trống lịch.

Tầng 3 — mỗi query đều full table scan. Bảng chỉ có PK id — không index nào. Thêm nữa whereDate('date', ...) (:49-50) bọc cột trong DATE() → kể cả có index cũng không dùng được, mà cột date vốn đã là kiểu DATE nên DATE() hoàn toàn thừa.

2. Cách fix: Fix 1 — Prefetch 1 query, group theo ngày (giết N+1)


branch code: ai_fixbug_40378 
branch production: release_step_20260827
```

> ⚠️ Toàn bộ description là **đánh giá kỹ thuật của Dev** (mục 1 Nguyên nhân + mục 2 Cách fix) — đã copy sang `03-dev-impact.md`. **Không có phần mô tả triệu chứng từ phía người dùng**, không có Section "Tái hiện bug", không có Section "Link TCs".

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #40380 KHÔNG có Section "Tái hiện bug" → để trống, tester/Leader bổ sung. -->

1.
2.
3.

## Expected result

<!-- Không có trong Redmine. -->

-

## Actual result

<!-- Không có trong Redmine. -->

-

## Ảnh / video / log đính kèm

<!-- issue.attachments rỗng (0 file). -->

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Ghi chú thêm khi auto-fill:

- Tracker là **`Bug tự detect`** — ticket không đến từ khách hàng, mà từ rà soát source. Vì vậy không có "Steps to reproduce" theo góc nhìn người dùng; triệu chứng người dùng thấy được là **màn chọn ngày giờ đặt lịch salon load chậm**.
- ⚠️ **Branch code là `ai_fixbug_40378` nhưng ticket này là `#40380`** — lệch số ticket. Cần hỏi Dev xem branch có đúng của ticket này không, hay 1 branch fix chung nhiều ticket.
- Module/Màn hình chưa có trong Redmine. **Tham chiếu ngoài Redmine** (MCP LME TEST STUDIO task #268): `feature = calendar-salon`, các màn liên quan là *LIFF đặt lịch salon — chọn ngày giờ (tab 週 / 月)* và *job tự gán nhân viên*. Tester xác nhận lại trước khi ghi cứng vào ô Module.
- Spec tham chiếu: [spec-features/admin/salon-booking/](../../spec-features/admin/salon-booking/).
