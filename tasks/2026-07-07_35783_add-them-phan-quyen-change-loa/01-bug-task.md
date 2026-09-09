# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #35783 — Add thêm phân quyền Change LOA |
| Redmine URL | https://redmine.watermelon.vn/issues/35783 |
| Auto-filled | 2026-07-07 by /new-task |
| Ngày báo cáo | 2026-04-10 |
| Khách hàng / PM báo | Ngọc Ánh |
| Module / Màn hình | `<chưa rõ — tester fill>` (liên quan màn hình 権限設定 / phân quyền staff) |
| Priority | Medium |
| Môi trường phát hiện | `<chưa rõ>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

> Ticket tracker: **SpecImprove** (yêu cầu chỉnh spec, không phải bug tái hiện).

```
Add thêm phân quyền LINE公式アカウント入れ替え phía dưới データコピー
Default: 主管理者
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Không có Section "Tái hiện bug" trong Redmine (ticket SpecImprove). -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine #35783):
- Screenshot_62.png — https://redmine.watermelon.vn/attachments/download/25103/Screenshot_62.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine (ticket **SpecImprove**, không phải bug) — root cause / spec change đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** + **regression impact** của phân quyền.

**Journal làm rõ spec (đọc kèm để không hiểu sai description):**
- **2026-06-26 — Ngọc Ánh:** "26/6: bỏ chọn mục 「LINE公式アカウント入れ替え」 (Thay đổi LINE Official Account). (Mặc định, chúng tôi muốn chỉ 主管理者 (quản trị viên chính) mới có thể thực hiện thao tác LOA入れ替え (thay đổi LOA))."

⚠️ **LƯU Ý MÂU THUẪN**: Description gốc ghi "Add thêm phân quyền ...", nhưng update 26/6 (Ngọc Ánh) + đánh giá ảnh hưởng của Dev (file 03) cho thấy spec cuối là **XÓA quyền LINE公式アカウント入れ替え (LOA入れ替え) khỏi danh sách phân quyền staff — chỉ owner 主管理者 mới được đổi LOA**. Verify lại với PM nếu còn nghi ngờ trước khi viết/review TC.
