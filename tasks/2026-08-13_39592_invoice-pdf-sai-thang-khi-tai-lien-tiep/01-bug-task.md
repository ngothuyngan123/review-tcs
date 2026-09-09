# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39592 — [12-08-2026][T11874][Bill tiền tool] Khách báo hóa đơn thanh toán tháng 6 bị phát hành nhầm sang tháng 7, yêu cầu khắc phục gấp và gửi lại hóa đơn đúng.` |
| Redmine URL | https://redmine.watermelon.vn/issues/39592 |
| Auto-filled | `2026-08-13 by /new-task` |
| Ngày báo cáo | `2026-08-12` |
| Khách hàng / PM báo | `AI bug detect Lme` (author Redmine) — KH cuối: `sb.info@toraiz.jp` / Bot 「シャドーイングバディ」 / 宛名 トライズ株式会社; nguồn OEM Slack 管理番号 TY-11874 |
| Module / Màn hình | `Bill tiền tool` (category Redmine) — màn 「決済履歴・領収書のダウンロード」 (`/basic/payment-history`), tab 個別発行 |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>`. KH thật báo qua OEM ⇒ tester confirm là Production (step.lme.jp) trước khi test |

> Trạng thái Redmine lúc fetch: **Fix done - Đợi test** · Assigned to: **Ngô Thúy Ngần** · Tracker: `Bug KH` · Project: `Lme` · Custom field `Commit Date` = `2026-08-13`.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: sb.info@toraiz.jp
Bot Name: シャドーイングバディ

Khi phát hành hóa đơn thanh toán tháng 6, hóa đơn lại được phát hành cho tháng 7.
Về lỗi này, tôi cũng từng hỏi cùng vấn đề này trước đây nên mong được khắc phục gấp và gửi lại hóa đơn tháng 6.

宛名：トライズ株式会社

Chức năng: Khác / Không biết (その他・分からない)
Thời điểm phản hồi: 2026/08/12 10:51:27

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11874

Nguồn: OEM đã tạo ticket trên Slack — 管理番号 TY-11874
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BP5UZR6FR
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1786500109580849
```

### 内容 từ Slack (OEM)

```
【操作方法に関するお問い合わせフォーム】
6月支払いの領収書を発行した際、7月分にて発行されます。
こちらのエラーにつきまして、以前にも同様の問い合わせをさせていただきましたので至急改善と、6月の領収書の送付のご対応をお願いいたします。

宛名：トライズ株式会社
```

### Bổ sung từ journal Redmine

- **2026-08-12 19:54** — 沖原裕樹 (OEM): *"Tôi nghĩ đây là vấn đề đã xảy ra từ trước, khi tải liên tiếp các hóa đơn, ngày của hóa đơn tải lần đầu bị áp dụng luôn cho cả các lần tải sau đó."* — kèm video Loom.
- **2026-08-13 02:39** — Ngọc Ánh: Link video: https://www.loom.com/share/c90606b4105d442fa3c604ae80103879

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguồn: journal Redmine 2026-08-13 08:50 của **Hạnh Nguyễn** (nguyên văn).

1. Vào màn payment-history, click vào tab 2026/07
2. Thực hiện click sang bên tab 個別発行, click vào checkbox của hóa đơn => Download
3. Thực hiện click sang tháng 2026/06
4. Click vào checkbox của hóa đơn => Download

## Expected result

- Hiển thị đúng data hóa đơn của tháng tương ứng.

## Actual result

- File pdf của tháng 6 đang hiển thị data của tháng 7.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video — https://www.loom.com/share/c90606b4105d442fa3c604ae80103879 (link ngoài, **không** phải attachment Redmine)
- [ ] Có log / request-response

> `issue.attachments` = rỗng — mọi bằng chứng đều là link ngoài (Loom / Slack / dashboard).

## Ghi chú thêm của Leader

- Bug **tái hiện được** — steps đã được QA (Hạnh Nguyễn) xác nhận trên Redmine, điều kiện bắt buộc là **KHÔNG reload trang** giữa 2 lần tải.
- KH khẳng định đây là **lỗi lặp lại** (đã từng hỏi cùng vấn đề trước đây) → cần kiểm tra tính năng có từng được fix rồi tái phát không (**RULE-09** — nhánh cũ/mới).
- Bug thuộc nhóm **bill tiền / hóa đơn gửi khách** → theo **RULE-08**, kết luận cuối phải có TC chạy ở `PRODUCTION`, không kết luận từ staging.
- Ngoài fix, KH còn yêu cầu **gửi lại hóa đơn tháng 6 đúng** — đây là action nghiệp vụ ngoài phạm vi test, cần confirm ai làm.
