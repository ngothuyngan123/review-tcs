# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38200 — [26-06-2026][TY-11377][Booking Event] Đặt chỗ event hiển thị "đã đặt" phía user dù admin chưa duyệt (リクエスト制)` |
| Redmine URL | https://redmine.watermelon.vn/issues/38200 |
| Auto-filled | 2026-06-26 by /new-task |
| Ngày báo cáo | 2026-06-26 |
| Khách hàng / PM báo | AI LME CSS |
| Module / Màn hình | Booking Event |
| Priority | Medium |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Bot: PAPAMAMACARS湘南平塚店, User: oteline26@shchiba.uk) |

## Mô tả bug (nguyên văn từ khách hàng)

User: oteline26@shchiba.uk
Bot Name: PAPAMAMACARS湘南平塚店

【Form hỏi về cách thao tác (操作方法に関するお問い合わせフォーム)】
Cảm ơn team đã luôn hỗ trợ.

Có một điểm muốn xác nhận về hoạt động của hệ thống đặt chỗ (予約システム) nên tôi liên hệ.

Đặt chỗ event (イベント予約) (tên quản lý: 東京アウトドアショー_相談予約)
Khi kiểm tra cài đặt hệ thống, hiện tại đang để ở chế độ 「リクエスト制」 (chế độ yêu cầu — cần duyệt) chứ không phải 「自動承認」 (tự động duyệt).

Ngoài ra, khi thực tế đặt thử nhiều lượt để kiểm tra hoạt động, tôi xác nhận đặt chỗ được xử lý theo luồng 「リクエスト」 (yêu cầu) → 「管理者による承認」 (admin duyệt).

Tuy nhiên, hiện tại với một số đặt chỗ, dù phía admin chưa thực hiện xử lý duyệt nhưng phía màn hình người dùng (user) lại hiển thị là đã đặt chỗ (予約済み).

Về spec đúng ra:
・Ở trạng thái chưa duyệt thì có hiển thị là đã đặt chỗ không?
・Hay có khả năng đang phát sinh lỗi (不具合) trên hệ thống?

Nhờ team kiểm tra giúp các điểm trên ạ.

Ngoài ra, về khách ひろよ: trước đây có hiển thị trong danh sách đặt chỗ, nhưng hiện tại không hiển thị ở cả danh sách đặt chỗ lẫn danh sách hủy.

Nhờ team kiểm tra giúp luôn xem dữ liệu đặt chỗ đang ở trạng thái như thế nào ạ.

Xin lỗi đã làm phiền, mong team kiểm tra giúp.

Ảnh chụp màn hình ①
Tình trạng đặt chỗ của khách ひろよ

Ảnh chụp màn hình ②
Người được hiển thị là đã đặt trên màn hình đặt chỗ dù chưa được duyệt

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BDC121U2D

---

### 原文 (JP)
```
【操作方法に関するお問い合わせフォーム】
お世話になっております。

予約システムの動作について確認したい点があり、ご連絡いたしました。

イベント予約（管理名：東京アウトドアショー_相談予約）
システム設定を確認したところ、現在は「自動承認」ではなく「リクエスト制」の設定となっております。

また、実際に複数件の予約を行い動作確認をしたところ、予約は「リクエスト」→「管理者による承認」という流れで処理されることを確認しております。

しかしながら、現在一部の予約については、管理者側で承認処理が行われていない状態であるにもかかわらず、利用者側の画面では予約済みとして表示されている状況が確認できております。

本来の仕様として、
・未承認の状態でも予約済みと表示されるのか
・システム上の不具合が発生している可能性があるのか

上記についてご確認いただけますでしょうか。

また、ひろよ様につきましては、以前は予約一覧に表示されていたのですが、現在は予約一覧にもキャンセル一覧にも表示されていない状況です。

予約データがどのような状態になっているのか、あわせてご確認いただけますでしょうか。

お手数をおかけいたしますが、ご確認のほどよろしくお願いいたします。

スクリーンショット ①
ひろよさんの予約状況

スクリーンショット②
承認されていないにもかかわらず予約画面では予約となっている方
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Section "Tái hiện bug" KHÔNG có trong Redmine — xem Ghi chú thêm của Leader để biết chi tiết 2 lỗi do QA (Ngọc Ánh) ghi nhận. -->

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

Screenshots (Redmine attachments):
- ① https://redmine.watermelon.vn/attachments/download/27570/snapcrab_noname_2026-6-26_9-12-0_no-00.png — Tình trạng đặt chỗ của khách ひろよ
- ② https://redmine.watermelon.vn/attachments/download/27571/snapcrab_noname_2026-6-26_9-15-17_no-00.png — Người hiển thị "đã đặt" dù chưa duyệt

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (không có section "Tái hiện bug" — chỉ là form hỏi của khách). Root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

**Chi tiết 2 lỗi QA (Ngọc Ánh) ghi nhận — journal #123732:**

【Lỗi ①】 Đối với bạn bè đã đặt lịch, KHÔNG hiển thị trong danh sách đặt lịch.
- Tên bạn bè bị ảnh hưởng: ひろよ
- Tên quản lý đặt lịch sự kiện: 東京アウトドアショー_相談予約
- Thời gian đặt lịch: 27/06/2026 (Thứ Bảy) 12:00 - 14:00
- Thời gian phê duyệt yêu cầu đặt lịch: 12/06 23:13

【Lỗi ②】 Đối với bạn bè đã đặt lịch, action khi phê duyệt yêu cầu đặt lịch KHÔNG được gửi đi.
- Tên bạn bè bị ảnh hưởng: 梶山 貴規
- Tên quản lý đặt lịch sự kiện: 東京アウトドアショー_相談予約
- Thời gian đặt lịch: 27/06/2026 (Thứ Bảy) 10:00 - 12:00
- Thời gian gửi yêu cầu đặt lịch: 25/06 18:58
