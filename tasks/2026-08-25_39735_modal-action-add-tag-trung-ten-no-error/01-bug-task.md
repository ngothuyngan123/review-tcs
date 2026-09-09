# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39735 — [Modal multi action] Add tag bị trùng name thì đang không hiển thị msg lỗi` |
| Redmine URL | https://redmine.watermelon.vn/issues/39735 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-08-19` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` (tracker: **Bug tự detect** — QA tự phát hiện, không phải khách báo) |
| Module / Màn hình | Chat 1:1 → Modal 「アクション設定」 (multi action) → popup 「タグ新規追加」. Redmine không set category; Studio gắn feature = `chat-1on1`. Modal này **dùng chung cho ~30 màn** (55 file blade include) theo đánh giá Dev. |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description không ghi môi trường. **Tester xác nhận** bug phát hiện trên Dev/Staging/Production nào. |

> Thông tin bổ sung từ Redmine: status hiện tại = **Fix done - Đợi test** (chuyển bởi AI LME Fix bug, 2026-08-19) · assigned_to = **Ngọc Ánh** (đổi từ Ngô Thúy Ngần ngày 2026-08-25) · project = Lme · start_date = 2026-08-19 · không có parent issue / relations.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Thao tác:
1. Vào màn chat 1:1 => Mở modal multi action => Chọn action tag
2. Click button add tag タグ新規追加
3. Nhập vào tên tag đã tồn tại trong bot
4. Click button save 保存してアクションに設定に戻る

Output: Khi click save thì API trả về lỗi nhưng GUI không hiển thị msg lỗi gì cả
Expect: GUI Hiển thị msg lỗi そのタグ名はすでに利用されています
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Vào màn chat 1:1 => Mở modal multi action => Chọn action tag
2. Click button add tag タグ新規追加
3. Nhập vào tên tag đã tồn tại trong bot
4. Click button save 保存してアクションに設定に戻る

## Expected result

- GUI hiển thị msg lỗi `そのタグ名はすでに利用されています`

## Actual result

- Khi click save thì API trả về lỗi nhưng GUI không hiển thị msg lỗi gì cả

## Ảnh / video / log đính kèm

- [x] Có screenshot — `add-tag-tu-modal-action.png` → https://redmine.watermelon.vn/attachments/download/29154/add-tag-tu-modal-action.png
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

Bổ sung:
- Bug **tái hiện được** (Redmine có đủ Thao tác / Output / Expect) → TC tái hiện là bắt buộc, không chỉ verify fix.
- File `03-dev-impact.md` lấy từ **journal AI Auto-fixbug** (#129281, 2026-08-19) — không phải Dev người viết. Tester cần đối chiếu lại mục 3 (caller) trước khi chốt coverage.
- Bộ TC hiện có (`04-tc-list.md`) **không lấy từ Sheet human** mà lấy từ **MCP LME TEST STUDIO task #173** — Redmine không có "Link TCs". 7/8 TC do AI sinh, toàn bộ chạy ở `env = local`.
