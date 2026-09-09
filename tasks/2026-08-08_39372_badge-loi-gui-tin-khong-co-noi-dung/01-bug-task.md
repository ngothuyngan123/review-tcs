# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39372 — [05-08-2026] [TY-11730] [Error message] Badge lỗi gửi tin hiển thị dù không có nội dung lỗi` |
| Redmine URL | https://redmine.watermelon.vn/issues/39372 |
| Auto-filled | `2026-08-08 by /new-task` |
| Ngày báo cáo | `2026-08-05` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn gốc: OEM tạo task trên Slack — ユーザー問い合わせ, 管理番号 TY-11730, 担当 沖原) |
| Module / Màn hình | `Error message` (category Redmine) — cụ thể: badge menu 送信エラー trên sidebar + màn chat 1:1 |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>`. KH báo qua OEM/Tayori trên tài khoản thật (LOA `@196kuwhr`) ⇒ nhiều khả năng **Production (step.lme.jp)**. Tester confirm lại. |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #39372. KHÔNG diễn giải lại. -->

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-11730
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1785889118139889?thread_ts=1785889118.139889&cid=C0BALS7S73L

Số quản lý　：TY-11730
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BMLUD3T8F
Địa chỉ email ：roppongi.t.l.o@gmail.com
Tên LOA　　：@196kuwhr
Phụ trách　　 ：沖原
Công cụ　 ：リンク
Nội dung yêu cầu
Khi bạn bè gửi tin nhắn, badge thông báo lỗi gửi tin sẽ hiển thị.
Tuy nhiên khi kiểm tra lỗi gửi tin thì không thấy nội dung lỗi.
※Khi kiểm tra hành vi bằng cách add friend từ tài khoản của khách hàng, vui lòng cho biết trước tên tài khoản.

---
### 原文 (JP)

```
管理No　：TY-11730
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BMLUD3T8F
アドレス ：roppongi.t.l.o@gmail.com
LOA名　　：@196kuwhr
担当　　 ：沖原
ツール　 ：リンク
問い合わせ内容
友だちからメッセージが送信されると配信エラーの通知バッジが表示される。
しかし配信エラーを確認してもエラーメッセージがない。
※ユーザーのアカウントで友だち追加をして挙動の確認をする際には、あらかじめアカウント名を教えてください。
```

---
### Khách trao đổi thêm sau khi gửi yêu cầu (4 tin — nguồn Tayori)

1. (08月04日 09:38) Về việc chậm trễ tốc độ tải, hiện tại toàn bộ phía chúng tôi đã được cải thiện. Xin cảm ơn.

Từ trước khi xảy ra sự cố trên nền tảng LINE, dù tin nhắn đã gửi thành công nhưng vẫn bị phân vào mục tin nhắn lỗi.
Tin nhắn thực tế vẫn được gửi bình thường.

2. (08月04日 10:01) Xin lỗi vì cách diễn đạt trước đó gây khó hiểu.
Thực tế không có nội dung lỗi nào, nhưng chỉ riêng badge thông báo hiển thị như trong ảnh chụp màn hình đính kèm, và số lượng lỗi tăng theo tỷ lệ với số tin nhắn chưa đọc.

3. (08月04日 10:12) Nếu quý khách chia sẻ trước tên tài khoản v.v. thì không có vấn đề gì.
Xin lỗi vì đã làm phiền, mong quý khách hỗ trợ.

4. (08月04日 15:15) Đã rõ.
Mong quý khách tiếp tục hỗ trợ.

### 原文 (JP) — お客様からの追加連絡

```
1. 読み込み速度の遅延について、弊所全体で現在では改善しております。ありがとうございます。

LINEプラットフォームで障害が発生する前から、送信ができているにもかかわらず、エラーメッセージに振り分けれられてしまいます。
きちんとメッセージの送信はできています。

2. こちらの表現がわかりにくく申し訳ございません。
実際にはエラーメッセージはありませんが、通知のバッジだけは添付のスクリーンショットのように表示されており、未読メッセージに比例してエラーメッセージの数字も増えていきます。

3. 事前にアカウント名などをご共有いただければ問題ございません。
お手数をおかけしますがよろしくお願いいたします。

4. かしこまりました。
何卒よろしくお願いいたします。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #39372 KHÔNG có section "Tái hiện bug" / 再現手順 → để trống theo nguyên tắc không bịa. -->

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

- https://redmine.watermelon.vn/attachments/download/28751/SnapCrab_NoName_2026-8-5_9-15-9_No-00.png (KH gửi kèm — ảnh badge 送信エラー hiển thị số)

## Ghi chú thêm của Leader

⚠️ **Bug không có bước tái hiện chính thức trong Redmine** — description chỉ có mô tả hiện tượng từ KH, không có section "Tái hiện bug". Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

Bối cảnh bổ sung (đọc từ Redmine, tester tự verify lại):

- **Trạng thái ticket**: `Fix done - Đợi test` · assignee `Ngô Thúy Ngần` · Commit Date `2026-08-06`.
- **Hiện tượng KH mô tả (2 dấu hiệu quan trọng để dựng TC)**:
  1. Badge 送信エラー **tăng theo số tin nhắn CHƯA ĐỌC** khi bạn bè gửi tin — không phải tăng theo lỗi gửi tin thật.
  2. Mở màn 送信エラー ra thì **danh sách trống**, không có nội dung lỗi nào.
- **Theo báo cáo Dev (file 03)**: điều kiện xuất hiện là **đang ở màn chat 1:1** (sidebar v2 render chung trang với JS chat) và **có tin nhắn bạn bè gửi tới qua socket**. Đây là điều kiện tái hiện do Dev suy ra từ code, **không phải KH cung cấp** — cần tester verify thực tế.
- **Dev CHƯA chạy được kiểm chứng trên trình duyệt thật** (DB dev `host.docker.internal:3306` Connection refused) → kết luận thuần đối chiếu code. **QA phải verify end-to-end trên môi trường thật.**
- **Yêu cầu riêng từ KH**: khi test bằng cách add friend vào tài khoản của KH thì **phải báo trước tên tài khoản** cho KH.
- Đã có 2 vòng fix của AI Auto-fixbug (2026-08-06 và 2026-08-07). **Bản chốt là vòng 2026-08-07** (branch `ai_fixbug_39372`, commit `4a2c301858`, 4 file) — xem file 03.
