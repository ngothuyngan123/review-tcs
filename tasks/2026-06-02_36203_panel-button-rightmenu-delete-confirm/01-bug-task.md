# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36203 — [01-05-2026][Khác] Panel/Button — 2 yêu cầu fix UX (panel right-side menu bị che; delete cần modal confirm)` |
| Redmine URL | `https://redmine.watermelon.vn/issues/36203` |
| Auto-filled | `2026-06-02 by /new-task` |
| Ngày báo cáo | `2026-05-04` |
| Khách hàng / PM báo | `AI CSS` |
| Module / Màn hình | `Khác — Panel/Button (パネル・ボタン), màn hình add/edit template button` |
| Priority | `Medium` |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: 
Bot Name: 

2 yêu cầu fix UX cho `パネル・ボタン` (Panel/Button):

**①** Menu của panel ở bên phải hiện tại không xem được nếu không scroll/dịch panel sang trái. Đề xuất: hiển thị luôn được mà không cần thao tác dịch panel — có sửa được không?

**②** Hành động delete đang chỉ cần 1 click là thực hiện ngay. Đề xuất: thêm modal confirm trước khi delete để tránh xoá nhầm — phương án này thấy thế nào?

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DV32EMRS?record_id=Rec0B0KNVQWH5

---

### 原文 (JP)
```
「パネル・ボタン」の修正要望（2点）

[補足]
①
右端にあるパネルのメニューについて、パネルを左にズラさないと確認できません。パネルをズラす操作がなくても表示された方が良いかと思いますが、修正は可能でしょうか？

②
削除がワンクリックが行えてしまいます。モーダル表示で削除操作の確認をした方が良いかと思いますがいかがでしょうか？
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: journal "Tái hiện case KH" của Kim Cúc (2026-05-23). -->

**Case 1 — Menu panel bên phải bị che:**
1. Tạo template button type 1, 2 hoặc 3
2. Trong template button tạo 5 panel
3. Ở panel 5 kéo scroll về; ở panel 4 click/hover vào icon 3 chấm → không hiển thị menu (sort, xóa panel)

**Case 2 — Delete không có confirm:**
1. Vào màn add/edit template button có panel
2. Click delete panel → panel bị xóa ngay (modal chưa confirm xóa)

## Expected result

- ① Menu (icon 3 chấm) của panel bên phải hiển thị được mà **không cần** scroll/dịch panel sang trái.
- ② Khi click delete panel → hiện **modal confirm** trước khi xóa.

## Actual result

- ① Menu panel bên phải bị che, phải scroll/dịch panel sang trái mới xem/thao tác được.
- ② Delete chỉ cần 1 click là xóa ngay, không có modal confirm → nguy cơ xóa nhầm.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->
- Đây là ticket tracker **SpecImprove** (cải tiến UX), không phải bug runtime. TCs nên tập trung verify 2 cải tiến: (①) menu panel right-side hiển thị không cần dịch panel; (②) modal confirm khi delete panel.
