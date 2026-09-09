# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` |
| Commit / Pull Request | `commit a9beeef869` (bản mới nhất, đã sửa regression #38473) |
| Branch | `ai_fixbug_38390` (nhánh gốc `release_step_20260623`, repo sns-line) |
| Ngày submit đánh giá | `2026-07-03` |
| Auto-filled | `2026-07-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ℹ️ Redmine #38390 có **2 báo cáo AI auto-fixbug**. File này lấy theo bản **mới nhất** (journal 124800, 2026-07-03 10:59) — bản này đã sửa **regression #38473** do lần fix trước gây ra. Bản cũ (journal 124754) chỉ giữ để tham chiếu.

---

## 1. Nguyên nhân

Xóa 1 bạn chậm ở đoạn xóa short-url: code lấy TẤT CẢ url id của bot rồi truyền vào `whereIn('url_id', [...])` — bot lớn có ~16.000 id nên câu DELETE phải mang & so khớp danh sách id khổng lồ (x2 cho `url_shorten` và `url_shorten_detail`) gây chậm, dù index đã đầy đủ. Đồng thời nạp toàn bảng form/sự kiện bằng `->get()` chỉ để lấy id cũng tốn RAM. Lỗi lặp ở **4 điểm** xóa/chặn bạn (3 web + 1 app/API).

## 2. Cách fix

Tối ưu query xóa friend ở 4 điểm (web `deleteLineUser` / `deleteUserBlock` / `deleteUserBlockAction` + app/API `FriendInformationController@deleteFriend`): thay `whereIn('url_id', mảng ~16.000 id)` bằng **SUBQUERY** lọc url theo bot (semi-join qua index); đổi nạp toàn bảng form/sự kiện `->get()` sang `pluck('id')`. ĐÃ BỎ timeout API LINE (theo yêu cầu human — giữ nguyên lời gọi LINE như gốc).

⚠ **SỬA REGRESSION #38473**: lần fix trước đổi nhầm `whereIn('line_user_id',$botLineId)->where()` ở `deleteUserBlockAction` làm **sót dọn link các friend không đứng đầu** khi chặn-xóa hàng loạt — `$botLineId` ở hàm này là MẢNG, nay khôi phục `whereIn` cho cả 3 câu (`UrlShorten` / `UrlShortenDetail` / `DetailUrlClick`). `deleteLineUser` & `deleteUserBlock` dùng scalar nên giữ `where`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Basic\FriendlistController::updateLineUser` (case `deleteLineUser`) — `app/Http/Controllers/Basic/FriendlistController.php` | Subquery url + pluck; giữ `where` (scalar) | Xóa 1 bạn (web, màn hidden) |
| 2 | `Basic\FriendlistController::deleteUserBlock` — `app/Http/Controllers/Basic/FriendlistController.php` | Subquery url + pluck; giữ `where` (scalar) | Xóa bạn đã block (web) |
| 3 | `Basic\FriendlistController::deleteUserBlockAction` — `app/Http/Controllers/Basic/FriendlistController.php` | Subquery url + pluck; khôi phục `whereIn` (mảng) cho UrlShorten/UrlShortenDetail/DetailUrlClick (fix regression #38473) | Chặn-xóa **hàng loạt** (web) |
| 4 | `Api\FriendInformationController::deleteFriend` (~dòng 945) — `app/Http/Controllers/Api/FriendInformationController.php` | Subquery url + pluck | Luồng xóa bạn trên **APP** |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FriendlistController::updateLineUser` (case `deleteLineUser`) | `Basic/FriendlistController.php` | Direct | Web — màn hidden, xóa 1 bạn |
| F2 | `FriendlistController::deleteUserBlock` | `Basic/FriendlistController.php` | Direct | Web — xóa bạn đã block |
| F3 | `FriendlistController::deleteUserBlockAction` | `Basic/FriendlistController.php` | Direct | Web — chặn-xóa hàng loạt (điểm có regression #38473) |
| F4 | `FriendInformationController::deleteFriend` | `Api/FriendInformationController.php` | Direct | APP/API — xóa bạn |

> Ghi chú Dev: Job `linect` KHÔNG dính (unfollow chỉ set `is_blocked`).

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (tập bản ghi bị xóa) `url_shorten`, `url_shorten_detail`, `DetailUrlClick`, `form_answer` / `form_answer_result` (deleted_at), `b_event_detail`, `scenario_lineuser_history` | DELETE / UPDATE (soft) | Dev khẳng định **tập bản ghi bị xóa GIỮ NGUYÊN** — chỉ đổi cách truy vấn. ⚠ NHƯNG regression #38473 cho thấy: câu query sai có thể **sót dọn link** friend không đứng đầu ở case chặn-xóa hàng loạt → cần verify đúng/đủ cascade. |

> Dev ghi 4.2 = "Không có (chỉ đổi cách truy vấn + timeout; tập bản ghi bị xóa giữ nguyên)". Bảng trên do QA suy từ ■2 + TC gốc để làm rõ phạm vi cascade cần verify — **không phải data mới bị đổi**, mà là data **được kỳ vọng xóa đúng** sau fix.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend List (FA-013) — Xóa/Chặn bạn trên **web** (màn hidden `/basic/friendlist/hidden`, user-block, block) | F1, F2, F3, D1 | Medium |
| T2 | Friend Information (FA-015) — Xóa bạn trên **APP** (`Api deleteFriend`) | F4, D1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> 🔎 Điểm cần chú ý khi review: fix là **generic query-optimization áp cho 4 điểm** — cần cover đủ 4 điểm (3 web + APP) + case **xóa 1 bạn** vs **xóa hàng loạt** (nơi phát sinh regression #38473). Xem [feedback_generic_fix_detection] & liên quan issue #38473.
