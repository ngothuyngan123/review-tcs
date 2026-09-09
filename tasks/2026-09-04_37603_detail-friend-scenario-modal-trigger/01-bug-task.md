# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37603 — [Detail friend] [Scenario] Modal trigger scenario: Start scenario khi mở item bill 1 lần nhưng trong modal đang hiện text tính năng là item chu kỳ 継続商品販売` |
| Redmine URL | https://redmine.watermelon.vn/issues/37603 |
| Auto-filled | `2026-09-04 by /new-task` |
| Ngày báo cáo | `2026-06-14` |
| Khách hàng / PM báo | Thanh Phương |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine `category` = null, không có custom field. Subject có prefix `[Detail friend]` `[Scenario]`) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `Staging` — theo journal #5 của Thanh Duy Nguyen: "Server staging" |

### Metadata Redmine bổ sung

| Trường | Giá trị |
|---|---|
| Tracker | Bug tự detect |
| Status | Fix done - Đợi test |
| Project | Lme |
| Assigned to | Ngô Thúy Ngần |
| Parent issue | #26684 (journal #4: `parent_id` 37544 → 26684) |
| Created / Updated | 2026-06-14T07:19:51Z / 2026-08-24T06:15:54Z |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Bot 562
Line user id 131204

=> Exp: hiện text item bill 1 lần 単品商品販売
```

### Data tái hiện bổ sung (nguyên văn journal #5 — Thanh Duy Nguyen, 2026-08-24T03:09:50Z)

```
Server staging
bot id 562
line user id 173397
action_lineuser.id = 79603 
2026-08-24 11:17:35

=> type_start_scenario trong action_lineuser đang lưu TYPE_ITEM_CYCLE_SHOW = 13001. Chuyển bug sang web check
```

### Journal có ý nghĩa test (nguyên văn)

| # | Người | Thời điểm | Nội dung |
|---|---|---|---|
| 3 | Thanh Phương | 2026-08-21T03:55:40Z | `Check vẫn bị lỗi` (status 9 → 1, reopen) |
| 4 | Thanh Phương | 2026-08-21T10:19:10Z | `Test #37544` (đổi tracker, đổi parent → 26684) |
| 5 | Thanh Duy Nguyen | 2026-08-24T03:09:50Z | Data tái hiện trên staging (xem khối trên) |
| 7, 8 | AI LME Fix bug | 2026-08-24T06:15:34Z / 06:15:54Z | Báo cáo AI Auto-fixbug (2 note **trùng nội dung**) → đã map sang `03-dev-impact.md` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống theo nguyên tắc không bịa. -->

1.
2.
3.

## Expected result

<!-- Redmine không có section riêng. Dòng gần nhất trong description: "=> Exp: hiện text item bill 1 lần 単品商品販売" — giữ nguyên ở phần "Mô tả bug". -->

-

## Actual result

<!-- Redmine không có section riêng. Ghi nhận gần nhất ở journal #5: action_lineuser.type_start_scenario lưu TYPE_ITEM_CYCLE_SHOW = 13001. -->

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `2026_06_14_16_17_14_Window.png` — https://redmine.watermelon.vn/attachments/download/26861/2026_06_14_16_17_14_Window.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Bổ sung (đều lấy nguyên văn từ Redmine, không suy diễn):
- Description **không có** 3 section chuẩn (Tái hiện bug / Đánh giá ảnh hưởng / Link TCs). Section "Đánh giá ảnh hưởng" nằm ở **journal #7 & #8** do bot `AI LME Fix bug` post (2 note trùng y hệt nhau) → file 03 lấy từ journal #8 (mới nhất).
- Bug này **đã từng được đóng rồi reopen**: journal #2 chuyển sang "Fix done" (2026-08-21), journal #3 Thanh Phương "Check vẫn bị lỗi" đưa về Open. Vòng fix hiện tại là lần thứ 2 → cần regression kỹ vòng fix trước.
- Redmine **KHÔNG có "Link TCs"** → file 04 lấy từ **MCP LME TEST STUDIO** task #196 (xem header file 04).
