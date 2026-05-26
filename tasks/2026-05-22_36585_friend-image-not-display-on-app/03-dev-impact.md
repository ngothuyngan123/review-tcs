# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương (journal author Section B); Redmine `assigned_to` = Kieu Son Tung |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | 2026-05-21 |
| Auto-filled | 2026-05-22 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ journal #118901 (Thanh Phương, 2026-05-21) -->

- User gửi message type file, nhưng api trả về định dạng object nên app k hiển thị được

## 2. Cách fix

<!-- Nguyên văn từ journal #118901 -->

- Thêm case type message = video vì đang bị thiếu
- Kiểm tra file nếu là dạng ảnh hoặc video thì set content = link

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chỉ ghi câu generic "Đã check và sửa các function sử dụng đến function/data vừa sửa" mà không liệt kê chi tiết. Input thiếu — Tester cần hỏi lại Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chỉ ghi generic, chưa list caller>` | | |

> ⚠️ **Input thiếu**: Mục 3 trong journal chỉ là heading "Đã check và sửa các function sử dụng đến function/data vừa sửa" mà không có nội dung danh sách caller. Cần verify với Dev để bổ sung trước khi /write-tc và /review-tc.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn từ journal mục 4.1 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getListMessageByUserV4` | `app/Http/Controllers/Api/ChatController.php` | Direct | API list message cho chat 1:1 — nơi fix case type=file/image/video |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn từ journal mục 4.2: "k có" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | (Dev report: không có data update) | — | Chỉ sửa logic transform response, không động vào DB |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn từ journal mục 4.3 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Hiển thị ảnh, video, audio, pdf, file trên chat 1:1 ở app | F1 | High — đây là chính nơi fix, mọi loại media phải verify |
| T2 | Các chỗ khác trên app có hiển thị message (Dev tự ghi note "check thêm còn chỗ nào hiển thị message trên app nữa k") | F1 | Medium — Dev chưa list cụ thể, tester cần survey UI app để liệt kê |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **⚠️ Hiện tại Mục 3 bị bỏ trống, cần Dev list caller cụ thể**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — **T2 quá mơ hồ, cần Dev cụ thể hóa**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Ghi chú bổ sung từ /new-task

- Fix mục 2 dạng **generic dispatch** (thêm case type=video + check file → set content=link). Theo memory `feedback_generic_fix_detection`: cần verify ≥ 3 trigger (image / video / audio / pdf / file) + ≥ 1 unknown/edge type fallback. TCs hiện có (file 04) đã cover ảnh, video, audio, pdf, file — nhưng cần verify thêm: type unknown / message dạng cũ trước fix / corrupt link.
- Mục 4.3 dòng 2 ("check thêm còn chỗ nào hiển thị message trên app nữa k") — Dev đẩy responsibility sang QA. Cần Leader chốt: app có những màn nào hiển thị message (chat 1:1, chat reply, history, push notification preview?) để cover regression.
