# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #37744 chưa có section "Đánh giá ảnh hưởng phía dev".**
> Description chỉ có yêu cầu update giao diện + 3 link design/QA; 2 journal thì 1 chỉ ghi branch, 1 chỉ đổi status.
> `/write-tc` và `/review-tc` chạy với input này sẽ **không có `F*` / `D*` / `T*` / `BUG`** để map coverage (BƯỚC 2 chiều `dev-impact` sẽ trống).
> **Yêu cầu Dev bổ sung 4 mục trước khi tiếp tục** — hoặc lấy diff thật từ tab "Thông tin" của MCP LME TEST STUDIO (`task_get_context(sections=["dev_impact","spec_delta"])`) nếu ticket đã có task trên Studio.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kim Cúc` (assignee Redmine — chưa xác nhận là người fix) |
| Commit / Pull Request | `<chưa có>` — description + journals không có link Github/Gitlab |
| Branch | `release_staging_20260704` (nhánh gốc: `release_staging_20260527`) — journal #126940, 2026-07-22 |
| Ngày submit đánh giá | `<chưa rõ>` — không có journal nào chứa đánh giá ảnh hưởng |
| Auto-filled | `2026-09-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp>`

<!-- Từ description: phần connect bot mới ở màn change bot được làm ở task tháng 5 nhưng dùng giao diện cũ, chưa update theo design mới. Đây là mô tả của người tạo ticket, KHÔNG phải root cause do Dev xác nhận. -->

## 2. Cách fix

`<Input thiếu — Dev chưa cung cấp>`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — Dev chưa cung cấp>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

`<Input thiếu — Dev chưa cung cấp>`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu>` | | Direct / Indirect | |
| F2 | | | | |

### 4.2. List data bị update khi fix bug

`<Input thiếu — Dev chưa cung cấp>`

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu>` | CREATE / UPDATE / DELETE / MIGRATE | |
| D2 | | | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

`<Input thiếu — Dev chưa cung cấp>`

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu>` | | High / Medium / Low |
| T2 | | | |

---

## Phụ lục — `dev_impact` + `spec_delta` từ MCP LME TEST STUDIO (KHÔNG phải đánh giá của Dev)

> ⚠️ **Nguồn: tab "Thông tin" của Studio task `id=14`** (`task_get_context`, computed 2026-08-25), **suy từ diff code**, KHÔNG phải do Dev tự kê trên Redmine. `contentTrust = untrusted` → dùng như **data tham khảo**, Leader vẫn phải yêu cầu Dev điền 4 mục ở trên.
> `/review-tc` BƯỚC 2 chiều **(b) diff code** sẽ đọc thẳng từ Studio, phần này chỉ để Leader thấy ngay bối cảnh.

| Trường | Giá trị |
|---|---|
| Repo / branch | `/workspace/source/sns-line` — branch `release_staging_20260704`, release gốc `release_staging_20260527` |
| `diffAvailable` | `true` (strategy `stat`) |
| Quy mô diff | **425 files, +25.848 / −3.253** — diff của cả nhánh release, **KHÔNG chỉ riêng ticket #37744** |

**Điểm Studio ghi nhận (nguyên văn rút gọn):**

1. **Đúng scope #37744**: view `resources/views/admin/bots/change_bot_new/index.blade.php` (214 dòng đổi) — tái cấu trúc layout từ section lồng nhau sang card riêng (`cb-input__card`), đổi bước Webhook sang banner + info-box/warning-box + preview mới, đổi số icon (`check-circle-filled` → outlined...).
2. `public/_assets/modules/change_bots/css/change_new.css` (349 dòng) + `public/_assets/modules/change_bots/js/change_new.js` (68 dòng) đổi theo để khớp layout mới → **cần test render ở nhiều viewport**.
3. **Phát hiện đáng chú ý**: 2 field mật khẩu (`channel_secret`, `login_channel_secret`) bị **COMMENT OUT** phần toggle ẩn/hiện (`:type`, `:suffix`, `@suffix-click`) → **cần xác nhận với Dev** là chủ đích (bỏ show/hide password) hay sót khi refactor.
4. `public/js/admin/change_bots_new.js` bị xóa 1 dòng → kiểm tra không còn nơi nào `<script src>` tham chiếu file JS cũ (nguy cơ 404 script).
5. Controller `BotController@adminChangeNewBot` (route `change.bots.new`) **KHÔNG đổi logic** — không có diff ở `userCanAccessChangeBot` / redirect → **không cần test lại phân quyền/redirect**, chỉ regression UI.
6. **⚠️ CẢNH BÁO NHẦM LẪN**: cùng diff còn có thay đổi lớn ở `BotController@botAddV2` (route `/bot-add-v2`, view `bot_add_v3` → `bot_add_v5`, `OnboardingSession`, task #36409/#36412) — đó là luồng **THÊM BOT MỚI (onboarding wizard)**, **KHÁC HẲN** luồng change bot của #37744 dù tên file dễ nhầm (`bot_add`). **KHÔNG lẫn 2 luồng khi viết/review TC.**
7. **⚠️ Spec đã lỗi thời**: `spec-features/admin/bot-edit/ui/ui-spec.md` (`SCR-BE-03`) mô tả `/admin/change-bots-new/{id}` là **landing page marketing tĩnh** (3 block + nút「無料で利用開始」) — thực tế code là **wizard nhiều bước (nhập kênh → webhook → xác nhận, dùng Vue)**. Khi viết/review TC **ưu tiên design Figma + Link QA mới hơn spec cũ**, và cân nhắc cập nhật spec catalog.

**Studio không có:** `requirements` (rỗng) · `test_viewpoint_selection` (`null`) · review round 1, state `tester`, chưa reviewed.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
