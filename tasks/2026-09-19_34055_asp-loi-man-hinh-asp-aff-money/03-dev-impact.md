# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #34055 bằng `/new-task`. Nguồn: **description** (đánh giá của Dev, fix gốc bằng PR 9507) + **Journal #133252** (AI auto-fixbug fix lại vì PR 9507 không có trên release). Phần lấy từ journal AI được ghi rõ `(AI journal)`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — description không ghi tên Dev. Fix lại bởi **AI LME Fix bug** (journal #133252). Assignee hiện tại trên Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | PR gốc: https://bitbucket.org/snstool/sns-line/pull-requests/9507/diff (⚠️ theo AI journal: **không có trên release**) · Fix lại: commit `2f2a40d022` |
| Branch | `ai_fixbug_34055` (gốc `release_step_20260805`) · branch release: `release_step_20260827` (journal #137187, 2026-09-19) |
| Ngày submit đánh giá | 2026-01-30 (description) · 2026-08-27 (AI journal #133252) |
| Auto-filled | `2026-09-19 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

**Description (Dev):**
- Trong logic có 1 query get list allbot nhiều record dẫn đến việc bùng RAM tạm thời, request bị kill

**(AI journal):** Màn hình tiền thưởng ASP (tab tình trạng chốt hợp đồng) nạp TOÀN BỘ danh sách bot của tài khoản quản trị vào bộ nhớ cùng lúc để dựng ô chọn bot. Tài khoản có rất nhiều bot làm bộ nhớ tăng đột biến, request vượt giới hạn RAM của PHP nên bị kill giữa chừng và màn hình báo lỗi. Vòng lặp còn ghi 2 dòng log gỡ lỗi cho MỖI bot, khuếch đại thêm tải ghi đĩa theo số bot.

## 2. Cách fix

**Description (Dev):**
- Fix dùng chuck để lấy ra từng block record

**(AI journal):** Sửa hàm dựng danh sách bot của màn tiền thưởng ASP: thay vì lấy hết bot một lần rồi lặp, nay duyệt theo từng khối 200 bản ghi (chunk) nên bộ nhớ dùng tại một thời điểm không tăng theo tổng số bot; thêm sắp xếp theo id để việc chia khối ổn định. Bỏ 2 dòng log gỡ lỗi in ra cho mỗi bot trong vòng lặp (log thừa từ lần sửa cũ, ghi theo số bot). Điều kiện lọc bot (hợp đồng pro/enterprise_pro/bot cũ/bot dùng thử) và dữ liệu trả về cho ô chọn bot giữ NGUYÊN. Quét ngang thấy 1 chỗ y hệt ở affBotDetailV2 cùng file — CHƯA sửa vì ngoài phạm vi ticket, đã ghi ở mục yokoten để human quyết định.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Description (Dev): mục 3 **để trống**. Bảng dưới lấy từ AI journal #133252.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ajaxAffMoneyV2` — app/Http/Controllers/Affiliate/AffiliaterController.php | Sửa (chunk 200 + `orderBy('id')` + bỏ 2 `Log::info`) | Hàm được sửa |
| 2 | `affMoneyV2` — app/Http/Controllers/Affiliate/AffiliaterController.php | Không | Chỉ trả view, không đụng |
| 3 | `money_v2.js`: `list_option = response.listBot` — public/js/affiliater/money_v2.js | Không | Nơi tiêu thụ danh sách bot, dữ liệu trả về không đổi |
| 4 | `affBotDetailV2` — app/Http/Controllers/Affiliate/AffiliaterController.php | **Không sửa** | Có pattern y hệt — ngoài scope ticket (yokoten, human quyết định) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ajaxAffMoneyV2` | app/Http/Controllers/Affiliate/AffiliaterController.php | Direct | Dev ghi ở description. Hàm duy nhất bị sửa |
| F2 | `money_v2.js` — dựng option ô chọn bot từ `response.listBot` | public/js/affiliater/money_v2.js | Indirect | (AI journal) consumer của F1, không sửa |
| F3 | `affBotDetailV2` | app/Http/Controllers/Affiliate/AffiliaterController.php | Indirect (chưa fix) | (AI journal) cùng pattern lấy toàn bộ bot → vẫn còn nguy cơ OOM |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Description để trống mục 4.2; AI journal: "chỉ đọc, không ghi/sửa dữ liệu", không cần recover data. Log máy chủ bớt 2 dòng/bot (bỏ `Log::info`) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình ASP aff tab 成約状況 — ô chọn bot (chỉ cần check show list bot đầy đủ chỗ select bot) | F1, F2 | `<Dev không ghi>` |
| T2 | Affiliate Reward Program (FA-027) — màn tiền thưởng cộng tác viên ASP, tab tình trạng chốt hợp đồng: ô chọn bot **và bảng số liệu thưởng** | F1 | `<Dev không ghi>` (AI journal) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
  - ⚠️ Cần chốt: bản lên release `release_step_20260827` là PR 9507 hay nhánh `ai_fixbug_34055`?
  - ⚠️ `affBotDetailV2` (yokoten) có fix trong ticket này không?
