# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43242 — [16-10-2026] [32027] [Đăng ký user/Login] Cài xác thực 2 bước nhưng không nhận được mã khi đăng nhập` |
| Module / Màn hình | Đăng ký user / Login — 2段階認証 (xác thực 2 bước) gửi mã qua email khi đăng nhập; mail đặt lại mật khẩu (`/reset-password`). Mọi mail giao dịch qua `MailApiService::sendMailApi` tới 7 domain Microsoft |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — câu hỏi của user) — 管理番号 32027. 担当: 管理者.

- Quản lý No: 32027
- Địa chỉ: mirin3880@gmail.com
- Tên LOA: 999（すりーないん）
- Phụ trách: 管理者
- Công cụ: リンク

Nội dung hỏi:

> Cảm ơn anh/chị đã hỗ trợ.
> Tôi đã cài đặt 2段階認証 (xác thực 2 bước) nhưng 認証コード (mã xác thực) khi đăng nhập không được gửi đến nên không thể đăng nhập được, tôi nên làm thế nào?

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: Production (`step.lme.jp`).
- Email đăng ký thật của user là `mirin999@outlook.jp` (domain Microsoft), KHÔNG phải `mirin3880@gmail.com` khách nhập ở form liên hệ.
- Không chỉ mã 2 bước: mail đặt lại mật khẩu (`https://step.lme.jp/reset-password`) cũng không tới, không có trong thư rác → khách không nhận được **bất kỳ** mail nào.
- Phạm vi Dev xác định: 7 domain Microsoft `hotmail.com`, `hotmail.co.jp`, `outlook.com`, `outlook.jp`, `live.com`, `live.jp`, `msn.com`.
- Mail bị rớt **sau khi** mail API đã nhận → code vẫn coi là gửi thành công (không có log lỗi).
- Support đề nghị tạm TẮT 2段階認証 của user liên quan trong lúc điều tra.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Email đăng ký (account lỗi) | `mirin999@outlook.jp` |
| Email form liên hệ (không phải email đăng ký) | `mirin3880@gmail.com` |
| Tên LOA | 999（すりーないん） |
| Thời điểm lỗi | Khách báo 2026-10-14 → 2026-10-15 (prd) |
| Đối chứng | Domain ngoài Microsoft nhận mail bình thường; mã 2 bước admin (System Admin) không đổi |

## Journal / note từ Redmine (nguyên văn)

**Journal #144666 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-16 09:13:25

鈴木 隆宏
Địa chỉ đăng ký đúng là 「mirin999@outlook.jp」
Email đổi mật khẩu cũng không nhận được
Cũng không có trong hộp thư spam
```

**Journal #144670 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-14 21:33:26

鈴木 隆宏（エルメサポート）
Gửi anh/chị Miwa

Cảm ơn anh/chị đã luôn ủng hộ.
Đây là bộ phận hỗ trợ L Message.

Cảm ơn anh/chị đã kiểm tra.

Sau khi kiểm tra địa chỉ email 「mirin3880@gmail.com」 mà anh/chị đã nhập vào form liên hệ, chúng tôi không tìm thấy địa chỉ này trong số các địa chỉ đã đăng ký L Message.

Vì vậy, có khả năng email lúc đăng ký là một địa chỉ khác.

Phiền anh/chị kiểm tra địa chỉ email đã đăng ký tại trang dưới đây.

▼Kiểm tra email đăng ký tại đây
https://step.lme.jp/check-user

Xin cảm ơn.
```

**Journal #144671 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-14 21:39:07

お客様
Xin lỗi.
Địa chỉ email đăng ký là địa chỉ này.
mirin999@outlook.jp
Tôi cũng không nhận được email gửi đến địa chỉ này.
```

**Journal #144672 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-15 10:48:50

鈴木 隆宏（エルメサポート）
Cảm ơn anh/chị đã luôn ủng hộ.

Cảm ơn anh/chị đã kiểm tra.

https://step.lme.jp/reset-password
Phiền anh/chị kiểm tra xem có nhận được email đặt lại mật khẩu từ trang trên hay không.

※Anh/chị không cần thực sự đổi mật khẩu.

Chúng tôi muốn xác nhận xem chỉ có email xác thực 2 bước không đến, hay tất cả email do chúng tôi gửi đều không nhận được.

Xin lỗi vì đã làm phiền, mong anh/chị kiểm tra giúp.
```

**Journal #144673 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-15 11:26:58

お客様
Cảm ơn anh/chị đã luôn ủng hộ.
Tôi không nhận được email nào cả.
```

**Journal #144910 — AI bug detect Lme — 2026-10-16:**
```
Comment slack ngày 2026-10-16 18:42:10

WSSサポーター
Hiện chúng tôi vẫn đang tiếp tục điều tra vấn đề không nhận được email gửi đến địa chỉ @outlook.jp.
Xin lỗi vì làm phiền, nhờ anh/chị tạm thời TẮT xác thực hai bước của user liên quan được không ạ?
```

**Journal #144919 — Do Van Tu TuDV — 2026-10-16:**
```
=> sửa lại các mail ['hotmail.com', 'hotmail.co.jp', 'outlook.com', 'outlook.jp', 'live.com', 'live.jp', 'msn.com'];
=> sử dụng reSendMailCommon
```

**Journal #144921 — Dev Studio — 2026-10-16:**
```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Mọi mail giao dịch đi qua hàm chung `MailApiService::sendMailApi`; từ fix #36764 (release 2026-05-29) địa chỉ thuộc 7 domain Microsoft luôn bị ép gửi qua mail API ngoài (`sendMailApiChild`) và không có đường dự phòng. Mail gửi qua kênh API này tới hộp thư Microsoft hiện bị rớt sau khi API đã nhận, nên code vẫn coi là gửi thành công. Kết quả: user outlook.jp bật xác thực 2 bước không nhận được mã (`ActiveAccount::sendMailCodeVerify`) và cũng không nhận mail đặt lại mật khẩu.

Hướng sửa:
- D-1 Gửi mail tới 7 domain Microsoft qua SMTP Gmail, lỗi thì quay về API

Ảnh hưởng / rủi ro:
Chỉ đổi kênh gửi cho email thuộc 7 domain Microsoft, áp cho mọi mail đi qua sendMailApi (mã 2 bước user, đặt lại mật khẩu, đăng ký/kích hoạt, mã xác thực xoá/đổi email/Google Calendar, staff, thanh toán tự động); domain khác và mã 2 bước admin không đổi. Rủi ro là giới hạn gửi/ngày của Gmail SMTP — khi đó tự quay về API như hiện tại.
```
