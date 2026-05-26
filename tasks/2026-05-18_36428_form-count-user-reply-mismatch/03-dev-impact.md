# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36428 (journal Kim Cúc, 2026-05-18) bởi `/new-task`. Tester verify lại 4 mục rồi tick checkbox.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Kim Cúc (submit eval) / Kieu Son Tung (assigned_to) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | 2026-05-18 |
| Auto-filled | 2026-05-18 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trong màn hình setting `各種設定` của form, logic khi save sẽ **lưu tất cả các trường** của bảng `form_answer` (trừ các trường của 4 tab đầu). Khi user trả lời form sẽ tăng `count_user_reply`, nhưng cùng lúc đó admin lại vào edit màn `各種設定` thì `count_user_reply` bị update về **data cũ** (data lúc admin mở màn settings, chưa có user mới submit).

## 2. Cách fix

Khi save setting `各種設定` thì **chỉ save những trường được setting** (không động đến `count_user_reply` và các trường runtime khác của form_answer).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev không liệt kê chi tiết caller. Chỉ confirm đã check trong scope mục 4.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `public/js/form_answer/component/other-settings.js` | Giới hạn payload save chỉ chứa fields thuộc tab `各種設定` | Tránh ghi đè `count_user_reply` và các runtime field khác |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Save setting `各種設定` (tab 5 form setting) | `public/js/form_answer/component/other-settings.js` | Direct | Function bị sửa logic save — chỉ gửi các trường được setting |

### 4.2. List data bị update khi fix bug

> Dev ghi: "k có" → không có data nào bị update trực tiếp.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answer.count_user_reply` | (gián tiếp — sau fix sẽ KHÔNG bị ghi đè khi save settings) | Đây là field chịu tác động chính của bug; sau fix nó được bảo toàn |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Save setting `各種設定` (tab 5) — check lại **từng trường 1** xem có update đc không | F1 | High — Dev cảnh báo cần verify từng trường trong tab 5 không bị mất setting sau fix |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — Dev chỉ list 1 file JS, có thể cần check thêm controller backend xử lý request save settings)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (Dev nói "k có" — Leader confirm với Dev: có cần list các runtime field khác của form_answer không bị ghi đè?)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
