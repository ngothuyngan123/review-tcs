# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu (TuDV)` — phân tích root cause + quyết định recover (Journal #150184, #150208); Dev Studio (AI) viết dev-impact đầy đủ; Redmine assignee: `Kieu Son Tung` |
| Commit / Pull Request | `<không có link PR>` — commit liên quan: `89c279b5e5a` (06/05/2026 — đưa bug vào), `8e5ed2db273` (sửa sót nhánh khác nhưng chưa sửa nhánh này), base branch tại `d4333b125bb197f92b14a9e48a2a969b23759f2d` |
| Branch | `ai_studio_fixbug_44785` (nhánh gốc `release_step_20260930_v2@79380b16eeec`) |
| Ngày submit đánh giá | `2026-11-03` |
| Auto-filled | `2026-11-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trong `ChatMessages::changeScenario`, nhánh **đăng ký lại vào chính kịch bản đang chạy với số ngày N** tính đúng mốc bắt đầu `$start_datetime` (= 00:00 hôm sau, nếu bước giờ cố định của ngày N đã quá giờ tại thời điểm bấm) **nhưng lại lưu `start_datetime = Carbon::now()`** (lúc bấm) thay vì mốc đã tính.

Khi hệ thống lên lịch (`createOrUpdateScenarioStepTimeByStartScenario`), bước ngày N có giờ gửi đã qua (so với `start_datetime = lúc bấm`) nên bị đánh **status 5** (không tạo lịch) — bước này bị bỏ qua. Bước kế tiếp (N+x) bị tính từ "hôm nay" (dựa trên `start_datetime` sai) nên bị **sớm 1 ngày** so với kỳ vọng.

- Lỗi do commit `89c279b5e5a` (06/05/2026) đưa vào.
- Commit `8e5ed2db273` đã sửa sót tương tự ở **nhánh khác** (đổi sang kịch bản khác) nhưng **chưa sửa nhánh này** (đăng ký lại cùng kịch bản).
- Có từ `release_staging_20260527`.
- Nhánh không có `start_day`/`start_time` (chế độ `今すぐ配信する`) ở dòng 2570-2585 cần rà thêm để đối chiếu 2 nhánh cho kết quả nhất quán (ghi chú của TuDV, Journal #150184) — kết luận cuối: nhánh này **không đổi**.

## 2. Cách fix

**D-1**: Lưu đúng mốc bắt đầu `$start_datetime` **đã tính** (00:00 hôm sau nếu giờ bước ngày N đã qua) khi đăng ký lại vào **chính kịch bản đang chạy** với N日目 — dùng lại công thức đang có ở nhánh "đổi sang kịch bản khác" (tương tự `ChatMessages.php:2733`).

Kết quả sau fix:
- Thực hiện `手動変更` (từ 友だち詳細 mới / mypage cũ / panel phải màn chat) chọn lại chính kịch bản đang 配信中 với N日目, **sau** giờ bước ngày N: bước ngày N gửi **ngày mai** đúng giờ; `scenario_lineuser.start_datetime` = ngày mai 00:00:00 (trước đây = lúc bấm → bước N bị bỏ).
- `scenario_lineuser_history`: dòng mới ghi đúng mốc `start_datetime` nói trên.
- Thực hiện cùng thao tác **trước** giờ bước ngày N: không đổi — bước N gửi hôm nay đúng giờ, `start_datetime` = lúc bấm (hành vi cũ giữ nguyên).

**File đã sửa** (`php-web`):
| File | Thay đổi |
|---|---|
| `app/Helpers/ChatMessages.php` | 3 dòng (+/-) |
| `.../ChangeScenarioSameScenarioStartDayTest.php` | +91 dòng (test mới) |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatMessages::changeScenario` — nhánh đăng ký lại **cùng** kịch bản (có `start_day`/`start_time`) | Có — gán `start_datetime` bằng mốc đã tính thay vì `Carbon::now()` | Root cause của bug |
| 2 | `ChatMessages::changeScenario` — nhánh đổi sang **kịch bản khác** (`ChatMessages.php:2733`) | Không | Đã đúng từ trước, dùng làm công thức tham chiếu để fix nhánh 1 |
| 3 | `ChatMessages::changeScenario` — nhánh **không có** `start_day`/`start_time` (`今すぐ配信する`, dòng 2570-2585) | Không | Dev đã rà, kết luận code không đổi / không phụ thuộc `start_datetime` theo cách gây bug |
| 4 | `createOrUpdateScenarioStepTimeByStartScenario` | Không (nhưng **đầu vào** `start_datetime` của nó thay đổi do sửa #1) | Tính lịch `scenario_step_time` của bước N và các bước sau N dựa trên `start_datetime` — Dev yêu cầu kiểm tra 次回配信 + các bước sau |
| 5 | Bước kiểu `経過時間` (`H時間M分後`) | Không | Tính từ `updated_at`, không phụ thuộc `start_datetime` → không bị ảnh hưởng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatMessages::changeScenario` — nhánh đăng ký lại **cùng** kịch bản đang chạy, có `start_day`/`start_time` | `app/Helpers/ChatMessages.php` | Direct | Root cause fix — gán `start_datetime` đúng mốc đã tính |
| F2 | `createOrUpdateScenarioStepTimeByStartScenario` | `app/Helpers/ChatMessages.php` (liên quan) | Indirect | Nhận `start_datetime` mới từ F1 → lịch gửi bước N + các bước sau N (`次回配信`) có thể đổi |
| F3 | `ChatMessages::changeScenario` — nhánh đổi sang **kịch bản khác** | `app/Helpers/ChatMessages.php` | Indirect (regression — PHẢI giữ nguyên) | Dùng làm công thức tham chiếu nhưng code nhánh này không đổi |
| F4 | `ChatMessages::changeScenario` — nhánh `今すぐ配信する` | `app/Helpers/ChatMessages.php` | Indirect (regression — PHẢI giữ nguyên) | Code không đổi theo xác nhận Dev |
| F5 | Tính bước kiểu `経過時間` (`H時間M分後`) | `app/Helpers/ChatMessages.php` (liên quan) | Indirect (regression — PHẢI giữ nguyên) | Không phụ thuộc `start_datetime` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `scenario_lineuser.start_datetime` | UPDATE (logic ghi) | Sau fix: đăng ký lại cùng kịch bản từ N日目 sau giờ bước N → ghi = 00:00 ngày mai (trước đây = `Carbon::now()`) |
| D2 | `scenario_lineuser_history` | CREATE (dòng lịch sử mới) | Dòng mới phải khớp `start_datetime` đã lưu ở D1 |
| D3 | `scenario_step_time` (lịch gửi bước N + các bước sau) | UPDATE (gián tiếp, tính lại theo `start_datetime` mới) | Qua F2 — ảnh hưởng `次回配信` |
| D4 | Dữ liệu đã lệch lịch **trước khi fix** (case `中ジョー`) | **KHÔNG migrate / KHÔNG recover** | ⚠️ Quyết định của TuDV (03/11/2026): chỉ sửa code, không gửi bù, không chạy script recover dữ liệu cũ |

Migration: **Không có** (Dev đã kiểm diff, xác nhận không có migration/schema change).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Step配信 — 友だち詳細 (mới) tab 「配信」→ ステップ配信 → 「手動変更」, đăng ký lại chính kịch bản từ N日目 | F1, D1 | High — bug chính, user-visible (bước bị bỏ, lịch sớm 1 ngày) |
| T2 | Step配信 — mypage cũ, thao tác 手動変更 tương tự | F1, D1 | High — cùng nhánh code |
| T3 | Step配信 — panel phải màn chat 1:1チャット, thao tác 手動変更 tương tự | F1, D1 | High — cùng nhánh code |
| T4 | 友だちリスト — thao tác hàng loạt (一括アクション) 「途中から配信」 | F1 (cùng nhánh changeScenario truyền start_day) | Medium |
| T5 | Action / Tag khởi động lại Step配信 từ N日目 (truyền `start_day`) | F1 | Medium |
| T6 | API nội bộ `start-scenario-api` truyền `start_day` cho bạn bè đang ở chính kịch bản | F1 | Medium |
| T7 | Scenario legacy (`method=1`) đăng ký lại chính kịch bản từ N日目 | F1 (nếu dùng chung nhánh code — cần xác nhận) | Medium |
| T8 | Lịch gửi bước N + các bước sau N / `次回配信` (Job gửi ステップ配信) | F2, D3 | High — lệch dây chuyền nếu `start_datetime` sai |
| T9 | Bộ lọc 友だちリスト — 絞り込み 「ステップ経過日数」 | D1 (đếm theo `start_datetime` mới) | Medium |
| T10 | Đổi sang **kịch bản khác** từ N日目 (regression — kết quả PHẢI giữ nguyên so với trước fix) | F3 | Low (nhưng bắt buộc có TC regression) |
| T11 | `今すぐ配信する` trên chính kịch bản đang chạy (regression — PHẢI giữ nguyên) | F4 | Low (nhưng bắt buộc có TC regression) |
| T12 | Bước kiểu `経過時間` (`H時間M分後`, regression — PHẢI giữ nguyên) | F5 | Low (nhưng bắt buộc có TC regression) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ Xác nhận lại với Dev/PM quyết định **không recover** dữ liệu lệch lịch của `中ジョー` trước khi QA ký duyệt — đây là quyết định business, không phải kỹ thuật
