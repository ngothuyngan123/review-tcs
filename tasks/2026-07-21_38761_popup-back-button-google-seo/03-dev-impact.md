# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu TuDV (assigned) — nhánh B sửa code (AI implement) |
| Commit / Pull Request | `<chưa có>` |
| Branch | ai_small_38761 |
| Ngày submit đánh giá | 2026-07-21 |
| Auto-filled | 2026-07-21 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine journal (mục 1). -->

Ghi chú nội bộ: Tính năng Popup nhúng (FA-018) có 3 kiểu hiển thị định nghĩa ở `PopupService::getListViewConfig` (`app/Services/PopupService.php:148-152`). Template JS `public/js/embedded-popup/default_setting.js`: CHỈ kiểu `close_page` mới dùng `history.pushState` + `addEventListener('popstate')` (dòng 199-246) để bắt nút Back và bật popup — đúng pattern back-button hijack mà Google hạ đánh giá.…

## 2. Cách fix

<!-- Nguyên văn từ Redmine journal (mục 2). -->

Support #38761 (nhánh B - sửa code) theo các spec bổ sung của human: bỏ can thiệp nút Back theo chính sách Google (từ 15/06/2026) + thêm chú thích ở màn thiết lập popup.

1) Popup nhúng (`public/js/embedded-popup/default_setting.js`): kiểu `close_page` trước đây dùng `history.pushState` + `addEventListener('popstate')` để bắt nút Back → bật popup. Đã BỎ `pushState` + listener `popstate`. GIỮ tín hiệu rời trang hợp lệ `visibilitychange` (đổi tab) + `blur` (mất focus). Bỏ luôn `history.pushState` dư trong `popupInsertAdjacentHTML`.

2) Lịch Salon (`public/js/calendar_salon/index.js`): bỏ khối bẫy nút Back cuối file (`history.pushState` + `popstate` re-push).…

3) Chú thích ở màn thiết lập: class `text__msg__blockview` có sẵn (đồng bộ style với ghi chú `※ ` ngay trên). Bọc select+span trong div `flex-column` để text nằm dưới select. Không đụng logic hiển thị/booking khác.

→ 3 file (2 JS + 1 blade), thay đổi thuần frontend/view.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ Redmine journal (mục 3 "Đã check function/data"). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `PopupService::getListViewConfig` — `app/Services/PopupService.php:148-152` | Không đổi (check) | Định nghĩa 3 kiểu hiển thị popup |
| 2 | `PopupController::getContentSetting` | Không đổi (check) | Sinh JS từ template |
| 3 | `public/js/embedded-popup/default_setting.js:199-246` (khối `close_page`) | Sửa — bỏ `history.pushState` + `popstate` | Khối bắt nút Back; giữ `visibilitychange` + `blur` |
| 4 | `public/js/embedded-popup/default_setting.js:247-270` (`after_open_page`: `setTimeout`; `location`: scroll) | Không đổi (check) | 2 kiểu này không dùng back-button hijack |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Từ Redmine journal mục 4 — 📄 Files. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Template JS popup nhúng (kiểu `close_page`) | `public/js/embedded-popup/default_setting.js` | Direct | Bỏ `pushState`+`popstate`; bỏ `pushState` dư trong `popupInsertAdjacentHTML` |
| F2 | Lịch Salon (calendar_salon) | `public/js/calendar_salon/index.js` | Direct | Bỏ khối `pushState`+`popstate` cuối file |
| F3 | Blade màn thiết lập Popup — note chú thích | `<blade màn cài đặt Popup>` | Direct | Thêm note `text__msg__blockview` dưới select (chỉ khi `close_page`) |

### 4.2. List data bị update khi fix bug

<!-- Từ Redmine journal mục 4 — 🗃 Data: — (không có). -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | — | — | Không có data bị update. Fix thuần frontend/view; note JS sinh từ template lúc render. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Từ Redmine journal mục 4 — ⚙️ Tính năng. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | FA-018 Popup nhúng — kiểu `close_page` | F1 | High — trên MOBILE không còn bật popup khi bấm nút Back (mất kênh exit-intent chính trên mobile). Trên DESKTOP vẫn bật khi đổi tab (`visibilitychange`) hoặc cửa sổ mất focus (`blur`). |
| T2 | FA-018 Popup nhúng — kiểu `after_open_page` / `location` | F1 | Low — KHÔNG bị ảnh hưởng (không dùng back-button hijack); cần regression xác nhận không đổi. |
| T3 | Lịch Salon (calendar_salon, màn quản trị shop) | F2 | Medium — trước đây chặn nút Back của trình duyệt; nay bấm Back điều hướng bình thường. Không còn chặn thoát trang khi đang thao tác (cảnh báo mất dữ liệu chưa lưu = UI riêng, ngoài phạm vi ticket). |
| T4 | Màn thiết lập Popup (note chú thích) | F3 | Low — thêm note hiển thị dưới select khi chọn `close_page`; coexist với ghi chú `※` cũ. |

---

## 5. Recover data

✔️ Không cần.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Nguồn: Redmine #38761 journal "Đánh giá ảnh hưởng" của Ngô Thúy Ngần @ 2026-07-21T02:42:25Z. Branch ai_small_38761. Dòng kết thúc bằng "…" giữ nguyên như bản gốc Redmine (có thể bị Redmine cắt) — Dev/Leader verify lại nếu cần full text. -->
