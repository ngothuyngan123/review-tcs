# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39668 — [17-08-2026] [TY-11918] [Item] Trùng ID thanh toán trên trang lịch sử/biên lai (UnivaPay)` |
| Module / Màn hình | `支払履歴 — Lịch sử thanh toán・領収書 (/basic/payment-history)` · `契約情報・領収書 (/basic/point-settings)` · webhook `UnivaPay 決済コールバック (POST /univapay/get-callback-webhook)` — feature `point` |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — hỏi đáp từ người dùng) — 管理番号 (số quản lý) TY-11918
担当 (phụ trách): 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1786959932454549

Số quản lý　：TY-11918
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BQSGG7G1J
Địa chỉ ：zukeran_choku@tohogas.co.jp
Tên LOA　　：東邦ガスのよる給食
Phụ trách　 ：沖原
Công cụ　 ：リンク (link)

**Nội dung yêu cầu**

Trên trang lịch sử thanh toán・biên lai (決済履歴・領収書ページ) đang hiển thị 2 lần cùng một ID thanh toán (課金ID).

Trên UnivaPay chỉ hiển thị một, nhưng để chắc chắn, quý vị có thể kiểm tra giúp xem có phát sinh thanh toán trùng lặp (重複決済) hay không không?

## Steps to reproduce

<!-- Redmine KHÔNG có Section "Tái hiện bug" — khách hàng chỉ báo hiện tượng, không có bước tái hiện. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `SnapCrab_NoName_2026-8-20_14-4-11_No-00.png` (71830 bytes) — https://redmine.watermelon.vn/attachments/download/29209/SnapCrab_NoName_2026-8-20_14-4-11_No-00.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (không có Section "Tái hiện bug") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** + **regression impact**.
- **Môi trường phát hiện: Production** — ticket phát sinh từ tài khoản khách hàng thật (LOA 東邦ガスのよる給食), đối chiếu với cổng thanh toán UnivaPay thật.
- **Không phải trừ tiền 2 lần** — trên cổng UnivaPay chỉ có 1 giao dịch thật; hiện tượng là **2 dòng cùng 課金ID trên màn lịch sử**. TC không được viết theo hướng "khách bị charge 2 lần".
- **Tần suất**: không phải 100% — chỉ xảy ra khi cổng UnivaPay **gửi lại** cùng sự kiện `charge_finished` (cổng tự gửi lại khi LME xử lý lâu / không phản hồi kịp). Luồng gia hạn tự động dễ dính nhất vì còn gửi mail + cập nhật rich menu + ghi vòng đời hợp đồng.
- ⚠️ **BẮT BUỘC khi test/deploy**: phải chạy **migration `2026_08_18_000000`** tạo bảng `univapay_webhook_processed`. Chưa chạy migration → webhook ném lỗi "bảng không tồn tại" (rơi vào catch, trả 200 failed).
- ⚠️ **Dữ liệu trùng CŨ vẫn còn** — fix chỉ chặn phát sinh mới. Màn lịch sử của khách TY-11918 vẫn hiện 2 dòng cho tới khi human dọn thủ công. Không dùng dữ liệu cũ để kết luận fix hỏng.
- Dev **chưa chạy thử trên môi trường thật** (không kết nối được MySQL dev) — mới chỉ `php -l`. Toàn bộ verify thực tế đẩy sang QA.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| 管理番号 (số quản lý) | `TY-11918` |
| Tên LOA | `東邦ガスのよる給食` |
| Địa chỉ (tài khoản) | `zukeran_choku@tohogas.co.jp` |
| bot_id | `<Redmine không ghi — tra theo LOA/email khi dựng env>` |
| Đối tượng cấu hình | Bản ghi `payment_histories` trùng `univa_charge_id` (2 bản ghi cha `parent_month=1` cùng mã giao dịch) |
| Gói / hợp đồng | Gói **Standard**, đăng ký ngày **2026/08/08** (journal #130703) |
| Thời điểm lỗi | Khách báo `2026-08-17` (thanh toán gói ngày `2026/08/08`) |
| Đối chứng | Giao dịch chỉ nhận webhook 1 lần → chỉ 1 dòng trên màn; hợp đồng năm có 13 bản ghi (1 cha + 12 con chia tháng) nhưng **chỉ hiện 1 dòng** — đây KHÔNG phải ca lỗi |

## Journal / note từ Redmine (nguyên văn)

**Journal #129911 — AI bug detect Lme — 2026-08-19:**

```
Comment slack ngày 2026-08-19 19:06:12

WSSサポーター
Do UnivaPay gửi thông báo về cùng một giao dịch thanh toán 2 lần, nên không phải là phát sinh thanh toán trùng lặp, mà hệ thống đã tự động thực hiện xử lý xóa dữ liệu trùng lặp.
Hiện tại hiển thị trùng lặp cũng đã được khắc phục.
```

**Journal #130703 — AI bug detect Lme — 2026-08-20:**

```
Comment slack ngày 2026-08-20 14:16:04

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã luôn ủng hộ.

Sau khi kiểm tra, tài khoản 「東邦ガスのよる給食」 đã đăng ký gói Standard vào ngày 2026/08/08.

Theo điều khoản sử dụng của L Message, việc hoàn tiền phí sử dụng chỉ được hỗ trợ nếu quý khách liên hệ trong vòng 48 giờ kể từ khi đăng ký hợp đồng.

Lần này, do đã quá 48 giờ kể từ khi đăng ký hợp đồng, nên rất tiếc trường hợp này không thuộc đối tượng được hoàn tiền.

Chúng tôi thành thật xin lỗi vì không thể đáp ứng được mong muốn của quý khách, mong quý khách thông cảm.

Xin cảm ơn quý khách.
```

> ⚠️ Journal #129911 nói "hệ thống đã tự động thực hiện xử lý xóa dữ liệu trùng lặp" — **mâu thuẫn** với mục 5 RECOVER DATA của Dev (file 03) khẳng định dữ liệu trùng cũ **vẫn còn**, phải dọn thủ công. Cần Leader xác nhận với CS/Dev trước khi viết TC verify dữ liệu cũ.
