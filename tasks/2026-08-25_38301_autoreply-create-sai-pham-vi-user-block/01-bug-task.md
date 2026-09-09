# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38301 — [Tạo auto reply] Lưu thông tin アクション稼働対象絞り込み(phạm vi người dùng không đúng) khi chọn đối tượng user block` |
| Redmine URL | https://redmine.watermelon.vn/issues/38301 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-06-29` |
| Khách hàng / PM báo | `Bùi Pháp` (author Redmine) — tracker = **`Bug Tester`** (bug do tester phát hiện, không phải KH báo) |
| Module / Màn hình | `<category Redmine trống — tester fill>` — từ prefix subject: **Tạo auto reply**; theo file 03 phạm vi là màn 自動応答（作成/編集） `create_v2` (SCR-AR-02) + API mobile `/init-autoreply-form`, `/save-autoreply` |
| Priority | `High` (Redmine priority = High) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` — description chỉ ghi `Bot oppo`. Tester confirm lại trước khi dựng TC |

### Trạng thái ticket tại thời điểm fetch

| Trường | Giá trị |
|---|---|
| Status | `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |
| Project / Tracker | `Lme` / `Bug Tester` |
| Commit Date (custom field) | `2026-08-25` |
| Ngày cập nhật cuối | `2026-08-25T08:01:01Z` |
| Relations | (không có) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn phần context ([Pre-condition]) của description Redmine #38301. KHÔNG diễn giải lại. Phần [Test steps] / [Actual result] / [Expected result] tách xuống các section bên dưới. -->

```
[Pre-condition]:
1. Bot oppo
2. Màn hình mặc định: Tạo auto reply
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguyên văn [Test steps] trong description Redmine #38301. -->

1. Chọn đối tượng user block `ブロックした友だち`
2. Điền các thông tin bắt buộc còn laijtreen màn hình
3. Bấm nút `[登録]`
4. Xem chi tiết bản ghi auto reply vừa tạo

> Ghi chú: bước 2 trong Redmine có lỗi gõ (`còn laijtreen` = "còn lại trên") — **giữ nguyên văn**, ý là "điền các thông tin bắt buộc còn lại trên màn hình".

## Expected result

<!-- Nguyên văn [Expected result]. -->

- 4. Hiển thị bản ghi auto reply với đối tượng user block (`ブロックした友だち`)

## Actual result

<!-- Nguyên văn [Actual result]. -->

- 4. Hiển thị bản ghi auto reply với đối tượng user hoạt động (`有効友だち`)

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

| # | File | URL |
|---|---|---|
| 1 | `Screenshot_1.png` | https://redmine.watermelon.vn/attachments/download/27643/Screenshot_1.png |
| 2 | `7.png` | https://redmine.watermelon.vn/attachments/download/29245/7.png (đính kèm ở journal `2026-08-21` của Bùi Pháp — "Vẫn không chọn option `ブロックした友だち` khi tạ autoreply") |

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ **Ticket này đã qua 3 vòng fix — vòng 1 KHÔNG bao giờ lên release, tester đã reopen 1 lần.** Đây là bối cảnh bắt buộc phải nắm trước khi review/viết TC:

| Vòng | Ngày (journal) | Nội dung | Kết cục |
|---|---|---|---|
| 1 | `2026-07-03` | Fix 1 dòng, commit `960dd329f1` **gộp vào branch `ai_fixbug_37707`** | ❌ `#37707` là ticket **Feature umbrella** `[MCP] Triển khai Nhóm tính năng cơ bản Phase 2`, branch đó **đã merge TRƯỚC** khi commit fix được thêm ⇒ commit **mồ côi, chưa từng vào release**. Môi trường tester vẫn chạy code cũ |
| — | `2026-08-21` | **Tester Bùi Pháp reopen**: "Vẫn không chọn option `ブロックした友だち` khi tạ autoreply" (kèm ảnh `7.png`) | Status `Fix done - Đợi test` → reopen |
| 2 | `2026-08-21` | Fix lại trên branch độc lập `ai_fixbug_38301` (gốc `release_step_20260805`), commit `d467fbb296`, **2 dòng / 1 file** (chỉ web) | Chuyển test |
| 3 (**bản chốt**) | `2026-08-25` | Mở rộng sang **luồng mobile API**, commit `f6ee800f86`, **4 dòng / 2 file** | Status hiện tại `Fix done - Đợi test` |

**Hệ quả cho việc test:**
1. **Bắt buộc verify môi trường test đang chạy đúng commit `f6ee800f86` (branch `ai_fixbug_38301`)** trước khi kết luận pass/fail — lần trước bug "tái hiện y nguyên" chỉ vì code fix chưa lên môi trường.
2. Branch cũ `ai_fixbug_37707` vẫn còn commit mồ côi `960dd329` — Dev khuyến cáo **không merge branch đó**.
3. Bug ảnh hưởng **cả web lẫn app mobile** (bản mobile là copy 1:1 của web) — TC phải cover cả 2 luồng.
4. Dev ghi nhận **ngoài scope, chưa fix**: clone auto-reply sang bot mới (`TemplateRepository:1919`) vẫn chưa copy `is_apply_active_friend` → cần ticket riêng. Leader cân nhắc raise.
5. **Bản ghi cũ tạo trước fix không tự sửa được** (đã lưu sai `is_apply_active_friend = 1`) — Dev kết luận "không cần recover data"; Leader confirm lại với PM nếu có KH đã tạo auto reply cho user block trước fix.
