# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33107 — Bot A đang access được link của bot B` |
| Redmine URL | https://redmine.watermelon.vn/issues/33107 |
| Auto-filled | `2026-09-04 by /new-task` |
| Ngày báo cáo | `2025-12-12` |
| Khách hàng / PM báo | `Thanh Phương` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set Category; theo description: **Template V2 — tạo mẫu tin con** + **Item bán hàng**) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `Staging (staging.lme.jp)` |
| Tracker | `Bug tự detect` |
| Status hiện tại | `Fix done - Đợi test` (done_ratio 80%) |
| Assignee | `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine. KHÔNG diễn giải lại. -->

```
1. [Template] Bot A đang access được link tạo template con của bot B => Template sau khi tạo bị sai bot_id

Check link tạo template ở các màn template, step message, send all, remind đều lỗi
- https://staging.lme.jp/basic/template-v2/add-template?template_group_id=38512
- https://staging.lme.jp/basic/template-v2/add-template?template_group_id=10382&action_type=scenario&scenario_id=2550&is_new=1
- https://staging.lme.jp/basic/template-v2/add-template?template_group_id=-11&action_type=sendAll&broadcastId=5287
- https://staging.lme.jp/basic/template-v2/add-template?template_group_id=678&action_type=event&event_id=337&is_new=1

2. [Item] Bot A access được màn edit item của bot B và edit được thông tin item của bot B
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" / "再現手順" → để trống theo quy tắc /new-task. -->
<!-- Thông tin gần nhất với steps là 4 link ở phần "Mô tả bug" phía trên (nguyên văn). -->

1.
2.
3.

## Expected result

- `Bot A không cho phép access vào các link của bot B`
  > ⚠️ Nguyên văn dòng `Expect:` trong **bản description ĐẦU TIÊN** (Redmine journal #107057, Thanh Phương, 2025-12-12T08:44:39Z). Reporter đã sửa description ngay sau đó và **dòng Expect này bị xoá** khỏi description hiện tại. Giữ lại vì đây là expected duy nhất Reporter từng ghi.

## Actual result

<!-- Redmine không tách section Actual — nội dung actual nằm ngay trong "Mô tả bug". -->

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue **KHÔNG có attachment nào** (`attachments = []`).

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — không có section "Tái hiện bug", không có attachment, Steps/Actual để trống. Root cause đã được Dev (AI auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

**Điều kiện tiên quyết để test:**
- Cần **2 bot khác chủ sở hữu** (bot A và bot B) để dựng case cross-bot.
- 4 biến thể link ở description dùng id thật của staging (`template_group_id=38512 / 10382 / -11 / 678`) — id này có thể đã đổi, tester phải lấy id thật trên env test.
- Chú ý giá trị **quy ước `template_group_id=-11`** (biến thể sendAll): Dev nói guard **cố ý không chặn** id rỗng/âm để không hỏng luồng tạo mới.

**Timeline đáng chú ý:**
- 2025-12-12 — Reporter tạo ticket (staging).
- 2026-03-27 — Nguyen Ngoc Hai note `branch: fix-bug-27083` (⚠️ branch mang số ticket **27083**, không phải 33107 — cần hỏi lại Dev đây là fix khác hay ticket gộp).
- 2026-06-10 — đổi tracker sang `Bug tự detect`.
- 2026-08-27 — **AI auto-fixbug** báo fix xong, chuyển status `Fix done - Đợi test`, branch `ai_fixbug_33107`.
