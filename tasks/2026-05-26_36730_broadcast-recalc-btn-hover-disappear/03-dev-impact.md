# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36730 bởi `/new-task` ngày 2026-05-26. Section "Đánh giá ảnh hưởng" parse từ journal #119437 của Kim Cúc.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Kieu Son Tung (assigned_to Redmine) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | 2026-05-26 (journal #119437) |
| Auto-filled | 2026-05-26 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Style `top` của popover bị sai → khi user di cursor vào button 「現時点での配信予定数を再計算」 thì popover/button bị dịch chuyển ra khỏi vùng hover → biến mất, không click được.

## 2. Cách fix

- Sửa lại style (top) của popover trong `public/css/send_all.css`.

> ⚠️ Note: Dev viết "sửa lại style sop" trong Redmine — Leader verify đây là typo của "style top" (đúng theo mục 1).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev không liệt kê chi tiết caller. Chỉ note: "Đã check và sửa các function sử dụng đến function/data vừa sửa".

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `public/css/send_all.css` | Sửa style `top` của popover | Fix root cause — popover dịch chuyển sai khi hover |
| 2 | `<chưa rõ — Dev chưa list caller cụ thể>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | CSS popover hover ở màn list send all | `public/css/send_all.css` | Direct | Style file dùng chung cho cả màn list send all (tab 配信予約 + 下書き) |

### 4.2. List data bị update khi fix bug

> Dev confirm: "k có" (không có data nào bị update).

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | (không có) | — | Fix thuần CSS — không chạm DB / cache / config |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình list send all — tab `配信予約` (đợi send / đã đặt lịch) | F1 | Medium |
| T2 | Màn hình list send all — tab `下書き` (draft) | F1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — verify "style sop" = "style top"
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — Dev không list rõ caller)
- [ ] Mục 4.1 không thiếu function: chỉ 1 file CSS, có file khác dùng cùng class CSS không?
- [ ] Mục 4.2 không thiếu data (CSS-only fix nên D=k có là hợp lý)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case**: 配信予約 + 下書き đủ chưa, hay còn tab nào khác dùng popover này (tab gửi rồi 配信済み)?
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
