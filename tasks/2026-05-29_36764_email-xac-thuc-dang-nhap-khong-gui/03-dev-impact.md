# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-05-29` (journal #119634) |
| Auto-filled | `2026-05-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguồn: journal #119634 (Kim Cúc), nguyên văn -->

- Email xác thực (認証メール) gửi qua hàm chung `MailApiService::sendMailApi`. Trước fix, khi `TYPE_SEND_MAIL=default` mail luôn đi theo đường SMTP mặc định (`sendMailDefault`).
- Với các địa chỉ thuộc nhóm Microsoft (hotmail/outlook/live/msn — KH dùng `naomi_m0629@hotmail.com`), mail gửi qua SMTP mặc định thường bị Microsoft chặn/loại bỏ âm thầm nên user không nhận được mail mã xác thực, dù các mail thông thường khác vẫn tới.

## 2. Cách fix

- Thêm hàm `isHotmailAddress($email)` kiểm tra domain email có thuộc nhóm Microsoft hay không (`hotmail.com`, `hotmail.co.jp`, `outlook.com`, `outlook.jp`, `live.com`, `live.jp`, `msn.com`).
- Trong `sendMailApi`, nếu email thuộc nhóm này → ép gửi qua API (`sendMailApiChild`, `mail2026.watermeru.com`) thay vì SMTP mặc định; các domain còn lại vẫn giữ luồng cũ theo `TYPE_SEND_MAIL`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguồn: journal #119634, mục 3 -->

> `MailApiService::sendMailApi` là điểm vào chung cho toàn bộ mail giao dịch, đã rà soát các nơi gọi. Thay đổi chỉ rẽ nhánh chọn kênh gửi (SMTP vs API) theo domain, không đổi nội dung/tham số mail → các nơi gọi dưới đây **không cần sửa**, chỉ được lợi (mail tới hộp thư Microsoft đáng tin cậy hơn).

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | SendAuthCode (mail mã xác thực) | Không | Đúng tính năng lỗi — caller chính |
| 2 | ResetPassword | Không | Đi qua `sendMailApi` |
| 3 | ActiveAccount | Không | Đi qua `sendMailApi` |
| 4 | AuthController | Không | Đi qua `sendMailApi` |
| 5 | SendMailUpdateAccountNumber | Không | Đi qua `sendMailApi` |
| 6 | AutoPaymentJob | Không | Đi qua `sendMailApi` |
| 7 | AutoPaymentJobUnivapay | Không | Đi qua `sendMailApi` |
| 8 | StaffAccessController | Không | Đi qua `sendMailApi` |
| 9 | BotController | Không | Đi qua `sendMailApi` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguồn: journal #119634, mục 4.1 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `sendMailApi` (thêm nhánh kiểm tra domain Microsoft) | `app/Mail/MailApiService.php` | Direct | Điểm rẽ nhánh SMTP vs API theo domain |
| F2 | `isHotmailAddress` (hàm mới) | `app/Mail/MailApiService.php` | Direct | Kiểm tra domain Microsoft |

### 4.2. List data bị update khi fix bug

<!-- Nguồn: journal #119634, mục 4.2 — "k có" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | (Dev báo: **không có** data bị update) | — | Fix chỉ rẽ nhánh kênh gửi, không chạm DB |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguồn: journal #119634, mục 4.3 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Gửi mail mã xác thực khi đăng nhập / xác thực 2 bước (認証メール) | F1, F2 | High |
| T2 | Mail kích hoạt / đăng ký tài khoản (ActiveAccount) | F1 | Medium |
| T3 | Mail đặt lại mật khẩu (ResetPassword) | F1 | Medium |
| T4 | Mail thông báo thanh toán tự động (AutoPaymentJob, AutoPaymentJobUnivapay) | F1 | Medium |
| T5 | Các mail giao dịch khác đi qua MailApiService (cập nhật số tài khoản, cấp quyền staff, BotController) | F1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ Lưu ý cho Leader: fix dạng "domain Microsoft → ép API". TCs cần cover NHIỀU domain trong nhóm (hotmail.com, hotmail.co.jp, outlook.com, outlook.jp, live.com, live.jp, msn.com) + ÍT NHẤT 1 domain ngoài nhóm (gmail/yahoo) để verify luồng cũ không đổi. Tham chiếu memory: generic-fix detection. -->
