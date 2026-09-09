# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38206 — [26-06-2026][28626][QL Tag] Thứ tự tag khác nhau giữa Quản lý tag (タグ管理) và màn sửa tag ở trang chi tiết friend (友だち詳細ページ)` |
| Redmine URL | `https://redmine.watermelon.vn/issues/38206` |
| Auto-filled | `2026-06-26 by /new-task` |
| Ngày báo cáo | `2026-06-26` |
| Khách hàng / PM báo | `AI LME CSS (User: cosy@cosypet.com / Bot: COSYペットケアサービス)` |
| Module / Màn hình | `QL Tag (タグ管理) / Trang chi tiết friend (友だち詳細ページ)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: cosy@cosypet.com
Bot Name: COSYペットケアサービス

Thứ tự sắp xếp (並び順) của tag bị khác nhau giữa màn Quản lý tag (タグ管理) và màn hình sửa tag (タグ編集画面) trong trang chi tiết friend (友だち詳細ページ).

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0BDDKVNP9S

---

h3. 原文 (JP)
<pre>
タグ管理と友だち詳細ページのタグ編集画面で、タグの並び順が違う。
</pre>

<!-- TaskRef: user_report:Rec0BDDKVNP9S -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

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

- https://redmine.watermelon.vn/attachments/download/27565/SnapCrab_NoName_2026-6-26_8-37-31_No-00.png
- https://redmine.watermelon.vn/attachments/download/27566/SnapCrab_NoName_2026-6-26_8-37-38_No-00.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine description (không có section "Tái hiện bug" / Steps / Expected / Actual). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (sort theo position) + regression impact. Tham khảo thêm bước tái hiện đã ghi trong TC Sheet (file 04, row 756): "Khi sort tại màn tag, vào màn detail friend tại modal edit tag và modal filter đang không hiển thị đúng thứ tự các tag — Expect: thứ tự tag tại detail friend giống màn quản lý tag".
