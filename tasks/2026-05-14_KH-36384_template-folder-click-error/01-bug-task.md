# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `KH-36384` |
| Redmine URL | https://redmine.watermelon.vn/issues/36384 |
| Auto-filled | `2026-05-14 by /write-tc` (fetch qua MCP redmine) |
| Ngày báo cáo | `2026-05-12` |
| Khách hàng / PM báo | User: `myroom.activecampaign@gmail.com` — Bot: `景品ショップマイルーム` |
| Module / Màn hình | Template management — Template folder list (`/basic/template-v2/...`) |
| Priority | `Normal` (Redmine priority id=2) |
| Tracker | `Bug KH` |
| Category | `Template` |
| Parent issue | `#36192` |
| Status | `New` |
| Assignee | AI CSS (id=160) |
| Môi trường phát hiện | Production (theo flow KH thật) |

## Mô tả bug (nguyên văn từ khách hàng)

> Khách báo: trong màn template management, khi click vào template folder **「定期配信用」** (Folder dành cho định kỳ broadcast), hệ thống hiển thị **error**.
>
> Cần team kiểm tra error message cụ thể và root cause (xem attachment để biết error đang hiển thị).
>
> Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B32M8NSRK

### 原文 (JP)

```
テンプレートフォルダ「定期配信用」をクリックするとエラーが表示される。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + journals + attachment từ Redmine và xác nhận đầy đủ.

## Steps to reproduce

> Reproduction Ngô Thúy Ngần (QA) phát hiện — journal #118361 ngày 2026-05-14:

1. Vào màn hình **list template** → Click detail một group template.
2. Click detail một template con trong group template → URL có dạng `/basic/template-v2/add-template?template_group_id=13305886&template_child_id=13305944`. Thêm hậu tố `/?utm_source=line&utm_medium=social&utm_id=syanai20260515` đằng sau (phán đoán: khách add link template này trong LP nào đó).
3. Truy cập lại link ở bước 2 → click **Save** template con này.
4. Back ra màn list template → bị lỗi (cùng error với KH báo).

## Expected result

- Mở folder template `定期配信用` (hoặc bất kỳ folder template nào) hiển thị danh sách template con bình thường, không có error.

## Actual result

- Click folder template `定期配信用` → hệ thống hiển thị error.
- Root cause (dev đã phân tích): `template_child_id` bị parse từ string chứa `/?utm_source=...` → content của template group bị lưu sai (`13305887,13305944/?utm_source=line`).
- Template ID lỗi cụ thể (Kieu Son Tung — journal #117993):
  - `id: 13305886`
  - `data lỗi: 13305887,13305944/?utm_source=line`
  - Ngày tạo/update: `2025-12-10 09:44:00` → `2026-05-12 10:34:17`

## Ảnh / video / log đính kèm

- [x] Có screenshot — `SnapCrab_NoName_2026-5-12_12-6-13_No-00.png` (attachment id=25699, 81KB) — ảnh error KH gặp.
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

- Bug được Ngọc Ánh **recover data** ngày 2026-05-13 (journal #118251). KH có thể vào lại bình thường, dev đang điều tra root cause song song.
- Test Lead Ngần đã viết TC list trên Google Sheet master — **Row 574 ~ 629**:
  https://docs.google.com/spreadsheets/d/131XoTI-AM4S6OwKbwcFlMnNJr0jVtbmpcOnf1BkiScs/edit?gid=828838454#gid=828838454
- Bug parent `#36192` — cần xem context của parent task nếu liên quan refactor lớn hơn.
