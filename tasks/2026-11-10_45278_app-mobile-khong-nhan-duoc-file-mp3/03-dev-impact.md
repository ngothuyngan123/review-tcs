# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thinh Nguyen` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-11-10` |
| Auto-filled | `2026-11-10 by /new-task` |

> ⚠️ Journal #153502 (Thinh Nguyen) KHÔNG viết theo đúng format 4 mục chuẩn (1. Nguyên nhân / 2. Cách fix / 3. Function caller đã check / 4.1-4.2-4.3) — Dev dùng format rút gọn riêng (`Nguyên nhân` · `Hướng sửa` · `File sửa` · `Đánh giá ảnh hưởng` · `Migration` · `Recover dữ liệu` · `Điểm cần test`). Nội dung dưới đây được **map 1:1 sang khung chuẩn**, không bịa thêm — Tester verify lại khi tick checkbox.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Check data API trả thì link file là đuôi dạng `.mpeg3`, không phải đuôi file chuẩn → trình phát audio trên app mobile không play được loại file này.

## 2. Cách fix

Copy file sang dạng đuôi đúng `.mp3` để play được trên trình phát mobile.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chỉ ghi "File sửa", không ghi riêng caller đã check — raw text, Tester verify lại khi hỏi Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `audio_player_screen.dart` | Thêm logic copy file sang đúng đuôi `.mp3` trước khi play | Trình phát audio app không nhận đuôi `.mpeg3` |
| 2 | `chat_item.dart` | Liên quan hiển thị/truyền link file audio trong item chat | File sửa Dev liệt kê cùng `audio_player_screen.dart` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Audio player (trình phát MP3 trên app mobile) | `audio_player_screen.dart` | Direct | Rủi ro thấp theo Dev — chỉ thêm logic copy file sang đúng đuôi `.mp3` |
| F2 | Chat item render (hiển thị item chat kèm audio) | `chat_item.dart` | Direct | Dev liệt kê cùng F1, chưa tách rõ thay đổi riêng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có | — | Dev xác nhận: "Migration / thay đổi dữ liệu: không có (đã kiểm diff)" |
| D2 | Không có | — | Dev xác nhận: "Recover dữ liệu: Không cần recover" |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 — xem/phát file audio (MP3) trên app mobile LME | F1, F2 | Low (theo Dev ghi "Rủi ro thấp") |

**Điểm cần test (Dev chỉ định)**: Phần view file audio có đuôi `.mpeg3` — tức các tin MP3 **đã nhận trước khi fix** (link cũ dạng `.mpeg3`), không chỉ tin mới gửi sau fix.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
