# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (Auto-fixbug LME)` |
| Commit / Pull Request | `sns-line @ commit acf3036dde (nhánh gốc release_step_20260511, 1 file) — đã push` |
| Branch | `ai_fixbug_37932` |
| Ngày submit đánh giá | `2026-06-29` |
| Auto-filled | `2026-06-30 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ journal Redmine #37932 (AI LME Fix bug, 2026-06-29) -->

Trang đặt lịch sự kiện **1 ngày** mà `liff.line.me` redirect tới (route `event-booking/index` → `MobileEventBookingController@index` → blade `order/index`) chỉ có `og:title` và `og:description`, **THIẾU thẻ `og:image`**. Khi share URL lên Facebook/email, do không có ảnh OGP hợp lệ nên Facebook tự nhặt một ảnh trong HTML (hoặc bản cache) → hiển thị sai ảnh (ảnh American Express). Ảnh tiêu đề của sự kiện vốn có sẵn nhưng không được đưa lên thẻ meta OGP.

## 2. Cách fix

<!-- Nguyên văn từ journal Redmine #37932 -->

Thêm xử lý OGP cho crawler trong `MobileEventBookingController@index`: khi user-agent là crawler (`facebookexternalhit`, gồm bot preview của LINE) thì trả trang preview nhẹ (`preview_url`) với `og:title` (tên sự kiện), `og:description` (mô tả); **riêng `og:image` hiện để rỗng (`$image=''`)**. User thật vẫn vào trang đặt lịch bình thường.

> ⚠️ Lưu ý cho Leader/Tester: cách fix hiện **chỉ thêm `og:title` + `og:description`, `og:image` đang để RỖNG**. Nghĩa là ảnh sai (American Express) sẽ không còn bị nhặt, nhưng **chưa chắc hiển thị đúng ảnh tiêu đề của sự kiện** trên preview. Cần verify rõ expected: "không hiện ảnh sai" vs "hiện đúng ảnh tiêu đề".

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ journal: pipe-separated → convert sang bảng -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MobileEventBookingController::index` (`app/Http/Controllers/Basic/MobileEventBookingController.php`) | Thêm nhánh xử lý crawler UA → trả `preview_url` với meta OGP | File chính được fix |
| 2 | `order/index.blade.php` | (không sửa) — là view thiếu `og:image` | Xác định nơi thiếu thẻ OGP |
| 3 | `preview_url.blade.php` | (view OGP) | View được render cho crawler |
| 4 | `BookingEventController::getInfoEventBookingUrl` | (không sửa) | Pattern crawler UA tham chiếu |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MobileEventBookingController::index` | `app/Http/Controllers/Basic/MobileEventBookingController.php` | Direct | Thêm nhánh crawler → trả trang preview OGP; user thật giữ nguyên luồng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (Không có) | — | Chỉ thêm xử lý render meta OGP, **không đụng DB** (theo Dev) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đặt lịch sự kiện (イベント予約) — ảnh xem trước (OGP) khi chia sẻ URL đặt lịch sự kiện lên Facebook/LINE/email | F1 | Medium |
| T2 | Đặt lịch sự kiện — luồng user thật mở URL & booking bình thường (regression do thêm nhánh crawler) | F1 | Medium |

> Ghi chú: Dev report fix cho sự kiện **1 ngày** (`MobileEventBookingController`). Cần xác minh với Leader/Dev: sự kiện **nhiều ngày** (`BookingEventController`) có cùng vấn đề thiếu `og:image` không, hay đã có sẵn OGP (journal trả lời KH có nhắc cả 1 ngày lẫn nhiều ngày dùng `BEventDetail.image`).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
