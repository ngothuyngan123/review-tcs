# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41090 — [18-09-2026] [30614] [Salon] Lỗi hiển thị không có lịch đặt khi đổi nhân viên có/không ca làm` |
| Module / Màn hình | Salon Booking (FA-020) — màn đặt lịch salon phía khách (LINE user), bước chọn nhân viên → bước chọn ngày giờ (lịch tháng) |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — câu hỏi của người dùng) — 管理番号 (số quản lý) 30614
担当 (phụ trách): 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1789694529561149?thread_ts=1789694529.561149&cid=C0BALS7S73L
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=30614

Số quản lý: 30614
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C2V3RHAJY
Địa chỉ: reset@reset-pilates.jp
Tên LOA: マシンピラティスReset苦楽園店
Phụ trách: 沖原
Công cụ: リンク (L Message)

Nội dung yêu cầu:
Trong đặt lịch Salon (サロン予約), sau khi chọn nhân viên không có ca làm (シフトが無いスタッフ) rồi chọn nhân viên có ca làm (シフトがあるスタッフ) thì hiển thị 「予約できる日程がありません」 (không có lịch có thể đặt).
Có vẻ xảy ra khi đang ưu tiên chế độ hiển thị theo tháng (月表示を優先).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" trong description — steps dưới đây lấy từ Journal #137022 (Kim Cúc). -->

1. Tạo Calendar salon public có tạo Staff.
2. Calendar có nhiều staff, tạo lịch làm việc cho Staff 2 (Staff 1 không có lịch làm việc trong tháng).
3. Setting hiển thị lịch làm việc theo tháng tại màn [システムワード変更 / 表示設定]: chọn 「月を先に表示」.
4. Mở link booking ở LINE user, chọn Staff 1 (không có lịch làm việc trong tháng).
5. Chọn sang Staff 2 (có lịch làm việc).

## Expected result

- Sau khi chọn Staff 2 (có ca làm), lịch tháng hiển thị lại với các ngày còn khung của Staff 2; thông báo 「予約できる日程がありません」 biến mất.

## Actual result

- Chọn sang Staff 2 có lịch làm việc nhưng vẫn bị hiển thị không có lịch: 「予約できる日程がありません」.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [x] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/30583/screenshot1.png
- https://redmine.watermelon.vn/attachments/download/30584/screenshot2.png
- Video (Journal #137001): https://drive.google.com/file/d/1fO2Ia2_rpPLvxHcpf4AA_UymlJ9J053e/view?usp=drive_link

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Production** (khách thật — LOA マシンピラティスReset苦楽園店).
- Điều kiện kích hoạt: lịch salon có **chọn nhân viên** + setting 「月を先に表示」 (ưu tiên hiển thị tháng). Chế độ 「週を先に表示」 không dính (theo Dev).
- Thứ tự thao tác quan trọng: **nhân viên KHÔNG có ca trước → nhân viên CÓ ca sau**.
- CS ban đầu (Journal #136969) không tái hiện được trên môi trường nội bộ; khách tạm mở 1 suất trống cho nhân viên SENA (người không có suất trống) như biện pháp tạm thời. Dev (AI auto-fixbug) cũng không tái hiện trên dev do thiếu dữ liệu lịch salon + ca nhân viên phù hợp. QA (Kim Cúc) đã tái hiện được — xem Steps.
- Bug xảy ra 100% khi đủ điều kiện (theo mô tả root cause: cờ "không có lịch trống" không được reset khi đổi nhân viên).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Khách hàng | マシンピラティスReset苦楽園店 — reset@reset-pilates.jp (管理No 30614) |
| Nhân viên không có ca (tại thời điểm báo) | SENA |
| bot_id / salon_id | `<Input thiếu — ticket không ghi>` |
| Thời điểm báo | 2026-09-18 (Slack) |
| Đối chứng | Chế độ 「週を先に表示」 không lỗi (theo Dev) |

## Journal / note từ Redmine (nguyên văn)

**Journal #136969 — AI bug detect Lme — 2026-09-18:**

```
Comment slack ngày 2026-09-18 09:58:49

沖原裕樹（エルメサポート）
Cảm ơn quý khách đã luôn ủng hộ.

Sau khi kiểm tra, hiện tại chúng tôi chưa xác nhận được vấn đề mà quý khách đã gửi có xảy ra trong môi trường của chúng tôi.

Quý khách có thể vui lòng xác nhận lại xem vấn đề hiện có còn xảy ra trong môi trường của quý khách không?

Nếu vấn đề vẫn đang xảy ra, để điều tra chi tiết hơn, chúng tôi có thể thêm bạn vào tài khoản của quý khách được không?

Rất mong quý khách vui lòng hỗ trợ.
```

**Journal #136970 — AI bug detect Lme — 2026-09-18:**

```
Comment slack ngày 2026-09-18 10:03:53

お客様
Cảm ơn quý khách đã luôn ủng hộ.
Cảm ơn đã xác nhận.
Hiện tại, như một biện pháp tạm thời, chúng tôi đã tạm mở 1 suất trống trong ca làm của nhân viên (SENA) - người không có suất trống.
Để xác nhận lại, chúng tôi có nên trả về môi trường đã đổi thành không có suất trống trong ca làm không?
Về việc kết bạn (friend), việc thêm bạn không có vấn đề gì.
Mong quý khách hỗ trợ.
```

**Journal #136971 — AI bug detect Lme — 2026-09-18:**

```
Comment slack ngày 2026-09-18 10:15:43

沖原裕樹（エルメサポート）
Cảm ơn quý khách đã liên hệ.

Không cần thực hiện thay đổi ca làm nữa.

Về vấn đề quý khách đã hỏi, hiện chúng tôi đang tiến hành xác nhận nên mong quý khách vui lòng đợi thêm một chút.
```

**Journal #137001 — Ngọc Ánh — 2026-09-18:**

```
https://drive.google.com/file/d/1fO2Ia2_rpPLvxHcpf4AA_UymlJ9J053e/view?usp=drive_link
```

**Journal #137022 — Kim Cúc — 2026-09-18:**

```
Tái hiện bug KH:
1. Tạo Calendar salon public có tạo Staff
2. Calendar có nhiều staff, tạo lịch làm việc cho Staff 2
3. Setting hiển thị lịch làm việc theo tháng tại màn [システムワード変更 / 表示設定]: chọn 月を先に表示
Hiện tượng: KHi mở link booking ở Line user, chọn Staff 1 đang k có lịch làm việc trong tháng, chọn sang Staff 2 có lịch làm việc nhưng cũng bị hiển thị không có lịch: 予約できる日程がありません
```
