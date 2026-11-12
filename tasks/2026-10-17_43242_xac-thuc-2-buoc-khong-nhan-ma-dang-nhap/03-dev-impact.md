# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Redmine #43242 **không có section "Đánh giá ảnh hưởng phía dev" đủ format 4 mục**. Nội dung dưới đây lấy nguyên văn từ Journal #144921 (Dev Studio — Nguyên nhân & hướng sửa) + Journal #144919 (TuDV). Mục 3 / 4 chỉ là danh sách Dev ghi dạng văn xuôi, đã tách thành bảng F/T để dễ map — **Dev chưa tự kê**, Tester/Leader verify hoặc yêu cầu Dev bổ sung.
>
> ⚠️ **Mâu thuẫn hướng fix**: Redmine (Journal #144921) ghi "SMTP Gmail **lỗi thì quay về API**", nhưng Studio task #462 (handoff 165, commit `d75fc83`) ghi bản cuối **KHÔNG fallback về API** khi Gmail lỗi. Cần Dev xác nhận.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu (TuDV) — theo Journal #144919 |
| Commit / Pull Request | `<chưa có>` (Studio ghi commit `d75fc83`) |
| Branch | `<chưa rõ>` (Studio: `ai_studio_fixbug_43242`) |
| Ngày submit đánh giá | 2026-10-16 |
| Auto-filled | 2026-10-17 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Mọi mail giao dịch đi qua hàm chung `MailApiService::sendMailApi`; từ fix #36764 (release 2026-05-29) địa chỉ thuộc 7 domain Microsoft luôn bị ép gửi qua mail API ngoài (`sendMailApiChild`) và không có đường dự phòng. Mail gửi qua kênh API này tới hộp thư Microsoft hiện bị rớt sau khi API đã nhận, nên code vẫn coi là gửi thành công. Kết quả: user outlook.jp bật xác thực 2 bước không nhận được mã (`ActiveAccount::sendMailCodeVerify`) và cũng không nhận mail đặt lại mật khẩu.

## 2. Cách fix

- D-1 Gửi mail tới 7 domain Microsoft qua SMTP Gmail, lỗi thì quay về API.
- (Journal #144919) sửa lại các mail `['hotmail.com', 'hotmail.co.jp', 'outlook.com', 'outlook.jp', 'live.com', 'live.jp', 'msn.com']` → sử dụng `reSendMailCommon`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chưa liệt kê caller dạng bảng — trích từ đoạn "Ảnh hưởng / rủi ro" của Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MailApiService::sendMailApi` | Email thuộc 7 domain Microsoft → gửi qua SMTP Gmail (`reSendMailCommon`), lỗi thì quay về API (`sendMailApiChild`) | Hàm chung mọi mail giao dịch |
| 2 | `ActiveAccount::sendMailCodeVerify` | (caller — Dev không ghi thay đổi) | Gửi mã 2 bước user |

---

## 4. Đánh giá ảnh hưởng

> Raw Dev: "Chỉ đổi kênh gửi cho email thuộc 7 domain Microsoft, áp cho mọi mail đi qua sendMailApi (mã 2 bước user, đặt lại mật khẩu, đăng ký/kích hoạt, mã xác thực xoá/đổi email/Google Calendar, staff, thanh toán tự động); domain khác và mã 2 bước admin không đổi. Rủi ro là giới hạn gửi/ngày của Gmail SMTP — khi đó tự quay về API như hiện tại."

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MailApiService::sendMailApi` — rẽ nhánh 7 domain Microsoft → SMTP Gmail | `<chưa rõ>` | Direct | Hàm dùng chung mọi mail giao dịch |
| F2 | `ActiveAccount::sendMailCodeVerify` — mã 2 bước user | `<chưa rõ>` | Indirect | Caller |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — Dev chưa cung cấp>` | | Dev không nêu thay đổi DB / config (cấu hình SMTP Gmail `RESEND_MAIL_*`?) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Mã xác thực 2 bước khi user đăng nhập | F1, F2 | `<Dev chưa ghi>` |
| T2 | Mail đặt lại mật khẩu | F1 | `<Dev chưa ghi>` |
| T3 | Mail đăng ký / kích hoạt tài khoản | F1 | `<Dev chưa ghi>` |
| T4 | Mã xác thực xoá / đổi email / Google Calendar | F1 | `<Dev chưa ghi>` |
| T5 | Mail staff | F1 | `<Dev chưa ghi>` |
| T6 | Mail thanh toán tự động | F1 | `<Dev chưa ghi>` |
| T7 | Domain ngoài 7 domain Microsoft — Dev nói không đổi | F1 | `<Dev chưa ghi>` |
| T8 | Mã 2 bước admin — Dev nói không đổi | F1 | `<Dev chưa ghi>` |
| T9 | Vượt giới hạn gửi/ngày của Gmail SMTP → quay về API | F1 | `<Dev chưa ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
