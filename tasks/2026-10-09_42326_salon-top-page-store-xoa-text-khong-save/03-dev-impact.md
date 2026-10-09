# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine qua `/new-task 42326`. Description Redmine **không có** section "Đánh giá ảnh hưởng" — nội dung lấy từ Journal #141125 + #141358 (v1) và #142199 + #142201 (v2) do "Dev Studio" ghi, đối chiếu thêm `dev_impact` của MCP LME TEST STUDIO task #379.
> ⚠️ `dev_impact` Studio viết theo **v1** (chỉ テキスト) và còn ghi `image_calendar` là "ngoài scope" — **v2 trên Redmine đã sửa cả `image_calendar`**. File này lấy Redmine v2 làm chuẩn.
> **Tester verify rồi tick checkbox dưới đây.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Nguyen Ha Vi (assignee Redmine; journal ký "Dev Studio") |
| Commit / Pull Request | v1 `1982d6b3fe12cdb06acf6376e7b04d31788ea891` · v2 `f5217491201dda62494b1ffd9c4c05b29194167f` (không có PR URL — workflow AI Studio) |
| Branch | `ai_studio_fixbug_42326` (repo `sns-line`, base `release_step_20260930_v2` @`657ba962f25d`) |
| Ngày submit đánh giá | v1: 2026-10-08 · v2: 2026-10-09 |
| Auto-filled | 2026-10-09 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #141358 + #142201 (Dev handoff v1 + v2) và xác nhận đầy đủ 4 mục dưới đây.

---

## 1. Nguyên nhân

**テキスト (v1 — Journal #141125 / #141358):** Khi ô テキスト (TinyMCE) bị xoá hết, màn hình gửi `description_top` / `description` là chuỗi rỗng; middleware toàn cục `ConvertEmptyStringsToNull` đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, hai cột này chỉ được đưa vào UPDATE khi `isset(...)` đúng, mà `isset(null)` = false, nên cột bị bỏ qua và text cũ giữ nguyên. Server vẫn trả success nên UI hiện toast 「編集が保存されました」.

**Ảnh 店舗 (v2 — Journal #142199 / #142201):** Khi bấm 削除 ảnh ở 店舗・ビジネス情報, màn hình gửi `image_calendar` rỗng; middleware `ConvertEmptyStringsToNull` của Laravel đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, cột `image_calendar` chỉ được ghi khi `isset(...)` đúng, mà `isset(null)` = false, nên ảnh cũ không bị xoá. Server trả bản ghi còn ảnh cũ, JS gán lại vào màn nên ảnh hiện lại ngay. Ô テキスト (đã sửa ở D-1) bị đúng cơ chế này.

## 2. Cách fix

> `D-1` / `D-2` dưới đây là **mã hướng sửa của Dev**, KHÁC tag data `D1` / `D2` / `D3` ở mục 4.2.

- **D-1** Ghi cả giá trị rỗng cho テキスト ở hàm lưu thông tin lịch Salon (vòng 1).
- **D-2** Lưu được việc xoá ảnh ở 店舗・ビジネス情報 (vòng 2).
- Endpoint lưu thông tin Salon (`POST /ajax/calendar-salon/save/info`, module web): các khoá `image_calendar`, `description`, `description_top` **có gửi lên (kể cả rỗng) thì ghi, không gửi thì giữ nguyên**.

Nội dung thay đổi (Dev handoff v2):
- 予約画面 → トップ画面設定: xoá hết テキスト → 保存 → reload: ô trống; プレビュー và trang top phía khách không còn text cũ (og:description quay về tên LINE).
- 予約画面 → 店舗・ビジネス情報: xoá hết テキスト → 保存 → reload: ô trống; プレビュー và khối 店舗情報 phía khách không còn text cũ.
- 予約画面 → 店舗・ビジネス情報: bấm 削除 ảnh → 保存: ngay sau lưu và sau reload hiện ảnh mặc định + 「設定されていません」; プレビュー và trang khách không còn ảnh.

File đã sửa (php-web, diff v2 cộng dồn):
```
app/Http/Controllers/Basic/CalendarSalonController.php | 10 +++++++---
1 file changed, 7 insertions(+), 3 deletions(-)
```

Migration / thay đổi dữ liệu: **không có** (Dev đã kiểm diff). Recover dữ liệu: **không cần** — bug chỉ làm thao tác xoá không có hiệu lực, giá trị cũ còn nguyên; người dùng xoá lại sau khi bản sửa lên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonController@saveCalendarInfo` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | Có — 3 điều kiện ghi `description_top` / `description` / `image_calendar`: khoá có gửi (kể cả rỗng) → ghi | Root cause fix D-1 + D-2 |
| 2 | 2 màn トップ画面設定 + 店舗・ビジネス情報 (dùng chung 1 request lưu; Studio: mixin `calendarDetailInfo`) | Không | Mỗi lần 保存 ghi cả テキスト 2 màn + ảnh 店舗 theo state đang có trên màn (nạp từ DB khi mở) → cần test chéo |
| 3 | Nhánh tải ảnh (変更/アップロード) ở 店舗・ビジネス情報 và ảnh trang top | Không | Nằm cùng hàm → smoke |
| 4 | Trang đặt lịch phía khách (LIFF) Salon — khối top page, ảnh + テキスト 店舗情報 | Không | Đọc từ các cột này, Dev: mọi nơi đọc đã xử lý NULL |
| 5 | og:description khi share link trang top | Không | Lấy テキスト top, không có thì tên LINE |
| 6 | プレビュー của 2 màn | Không | Đọc lại record sau lưu |
| 7 | API mobile Salon `Mobile/CalendarSalonController` (đọc `description_top`, đã `!empty`) | Không | Smoke |
| 8 | Lesson `CalendarManagementController` | Không chạm | Dev xác nhận (Studio: Lesson vốn ghi thẳng, không có lỗi tương tự) |

---

## 4. Đánh giá ảnh hưởng

> Dev đánh giá tổng: **Rủi ro thấp** — "Chỉ 3 điều kiện ghi trong 1 hàm, các cột đều cho phép NULL, mọi nơi đọc đã xử lý NULL, có harness và kiểm chứng ngược ở 2 mốc; **chưa verify runtime**." Dev **không** tách mức rủi ro cho từng F/D/T — cột "Mức độ" / "Nguy cơ regression" bên dưới do `/new-task` suy từ ghi chú Dev + Studio, **Tester/Leader cần verify**.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonController@saveCalendarInfo` — `POST /ajax/calendar-salon/save/info` | `app/Http/Controllers/Basic/CalendarSalonController.php` | Direct | 3 điều kiện ghi `description_top` / `description` / `image_calendar`; khoá có gửi (kể cả rỗng) → ghi, không gửi → giữ nguyên |
| F2 | Gói lưu dùng chung 2 màn トップ画面設定 + 店舗・ビジネス情報 (mixin `calendarDetailInfo`, TinyMCE) | JS màn 予約画面 Salon (Studio dẫn `setting-policy.js:202-226`) | Indirect | Mỗi lần 保存 ghi cả 2 cột テキスト + ảnh 店舗 theo state hiện tại. Studio: TinyMCE chỉ sync state qua keyup/change, nạp lại chỉ `setContent` khi có giá trị ⇒ rủi ro lưu màn A xoá mất dữ liệu màn B |
| F3 | Nhánh upload / đổi ảnh (変更/アップロード) — ảnh 店舗 + ảnh trang top | Cùng hàm F1 | Indirect | Code nhánh tải ảnh không đổi — smoke |
| F4 | Trang đặt lịch phía khách LIFF Salon — top_page (`description_top` khi `show_top_page`), 基本情報 (`description`, ảnh 店舗), og:description (fallback `line_name`) | Studio dẫn `bookings/top_page.blade.php`, `bookings/layouts/main.blade.php:10` | Indirect | Kiểm khi NULL và khi có text / ảnh |
| F5 | プレビュー admin (`previewTop` / `preview`) 2 màn | — | Indirect | Đọc lại record sau lưu |
| F6 | API mobile Salon `Mobile/CalendarSalonController` | — | Indirect | Đọc `description_top` (đã `!empty`) — smoke |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `description_top` (テキスト トップ画面設定 — bảng lịch Salon, Dev không ghi tên bảng) | UPDATE (hành vi ghi) | Giờ ghi NULL khi khoá gửi rỗng; cột nullable |
| D2 | `description` (テキスト 店舗・ビジネス情報) | UPDATE (hành vi ghi) | Như D1 |
| D3 | `image_calendar` (ảnh 店舗・ビジネス情報) | UPDATE (hành vi ghi) — **v2** | Bấm 削除 → 保存 giờ ghi NULL; màn hiện ảnh mặc định + 「設定されていません」 |

> Không migration. Record cũ (lưu trước fix) không tự sửa — xoá lại sau release (Studio REQ-008: record cũ xoá テキスト được sau fix).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 予約画面 → トップ画面設定 (Salon): xoá hết テキスト → 保存 → reload | F1, D1 | High — bug chính |
| T2 | 予約画面 → 店舗・ビジネス情報 (Salon): xoá hết テキスト + 削除 ảnh → 保存 → reload | F1, D2, D3 | High — bug chính (テキスト) + fix v2 (ảnh) |
| T3 | Lưu chéo giữa 2 màn dùng chung request — thao tác ở màn này không làm mất テキスト / ảnh màn kia | F1, F2, D1, D2, D3 | High — Dev + Studio đều nhấn mạnh "test chéo" (rủi ro mất dữ liệu) |
| T4 | Upload / 変更 ảnh 店舗 + xoá ảnh trang top ở トップ画面設定 (hồi quy) | F3, D3 | Medium — cùng hàm, Dev yêu cầu smoke |
| T5 | Trang đặt lịch phía khách LIFF Salon (top page, khối 店舗情報, ảnh) + og:description khi share link | F4, D1, D2, D3 | Medium |
| T6 | プレビュー 2 màn | F5 | Low |
| T7 | Validate 店舗名 khi bật trang top (「店舗名を入力してください。」) + トップ画面を表示しない với テキスト trống | F1 | Low — Dev liệt kê ở điểm cần test |
| T8 | App quản trị di động Salon (`description_top` làm mô tả) | F6 | Low — smoke |
| T9 | Lesson トップ画面設定 | Không chạm | Low — smoke (Studio REQ-010) |

### Điểm nghi vấn cần hỏi Dev / Leader

- **テキスト chỉ gồm khoảng trắng / xuống dòng**: Journal #141358 + #142201 ghi "sau lưu coi như trống"; Studio `dev_impact` ghi "code không trim ⇒ có thể lưu `<p>&nbsp;</p>`, không phải NULL"; Studio REQ-009 để expected "chờ human chốt". → Cần chốt expected trước khi viết/duyệt TC.
- Journal #142201 dẫn **#42605** ở điểm test xoá ảnh — chưa rõ quan hệ với #42326 (ticket con / ticket riêng cho `image_calendar`?).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
