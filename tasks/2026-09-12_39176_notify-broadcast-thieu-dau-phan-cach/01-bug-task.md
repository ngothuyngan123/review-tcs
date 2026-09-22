# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39176 — [LME-Studio] Số người nhận trong thông báo broadcast không có dấu phân cách hàng nghìn` |
| Module / Màn hình | `Broadcast (メッセージ配信) — notify hoàn tất gửi tin hàng loạt` + `Action Schedule (アクションスケジュール実行) — notify khi lịch hẹn hành động chạy` |

## Mô tả bug (bản dịch tiếng Việt)

*Bug từ LME Test Studio* — severity Medium.
Task: #11 · Test case: NEW-477.

Nội dung thông báo (notify) sinh ra sau khi gửi tin hàng loạt dùng `String.format` với `%s` thuần cho biến số nguyên (số người nhận), nên số từ 4 chữ số trở lên bị hiển thị liền không có dấu phân cách hàng nghìn. Kỳ vọng hiển thị có dấu phẩy phân cách (tương tự cách `TextUtils.getMoneyValue` định dạng số tiền).

base branch: `release-t07-2026`

Nội dung sửa Dev ghi ngay trong ticket:

```
sửa:
1. SentMessageService.java:66
	+ String contentNotify = String.format("配信人数 %,d人  タイトル：%s", requestSentTemplateToUser.getSuccessSendCount().get(), broadcastTitle);
2. ActionScheduleBotTask.java:126
	+ String contentNotify = String.format("%sが稼働しました（対象人数 %,d人）", title, sendCount);
```

## Steps to reproduce

1. Gửi broadcast tới số lượng lớn friend (vd 12345 người).
2. Broadcast hoàn tất, xem nội dung notify tại `SentMessageService.java:70`.

## Expected result

- Hiển thị có dấu phân cách hàng nghìn: `12,345人` (tương tự cách `TextUtils.getMoneyValue` định dạng số tiền).

## Actual result

- `String.format` dùng `%s` thuần cho số `int` → hiển thị `12345人`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #39176: attachments = 0 (không có file đính kèm). -->

## Ghi chú thêm của Leader

- Bug **tự detect bởi LME Test Studio** (author ticket = `AI Auto test Lme`), không phải khách hàng báo → severity Medium, lỗi hiển thị, không chặn luồng gửi tin.
- Lỗi **100% tái hiện** với mọi số ≥ 1.000 (không phải lỗi xác suất) — do format specifier sai, không phụ thuộc dữ liệu.
- Trạng thái Redmine hiện tại: **Fix done - Đợi test**; base branch `release-t07-2026`.
- Fix chạm **2 đường notify** (broadcast + action schedule) → phải test cả 2, không chỉ broadcast như tiêu đề ticket.
- Con số trong notify đi qua nhiều kênh tiêu thụ (chuông LME-Studio, app mobile, Chatwork, web push PC) → cần verify chuỗi lan nguyên văn ở từng kênh.
- ⚠️ Notify là **job nền** — theo RULE-08 không kết luận được từ local/staging; bộ TC Studio hiện mới chạy toàn bộ ở `env = local`.

## Journal / note từ Redmine (nguyên văn)

**Journal #133006 — Văn Dũng Đinh — 2026-08-26:**

```
Bug tự detect #39176 [LME-Studio] Số người nhận trong thông báo broadcast không có dấu phân cách hàng nghìn

1. Nguyên nhân
   - SentMessageService.java:66 build nội dung notify bằng String.format("配信人数 %s人 ...") — %s in số int thô nên số người nhận từ 4 chữ số trở lên hiển thị "12345人" thay vì "12,345人".
   - Cùng lỗi ở ActionScheduleBotTask.java:126 ("対象人数 %s人") — chung luồng notify mobile_notify, fix chung để QA test 1 lượt.

2. Cách fix
   - Đổi format specifier %s -> %,d ở cả 2 chỗ. Không thêm helper mới (TextUtils.getMoneyValue hiện chỉ có overload Long) để tránh conflict với branch #33332 chưa merge.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
   - Không ảnh hưởng caller: chỉ đổi format specifier của biến local contentNotify, không đổi signature hay behavior của method nào.
   - Đã check 4 nơi tiêu thụ chuỗi này (ActionLaterService.buildNotifyContent, HandlePushNotifyPc, HandlePushNotifyChatwork, HandleMobileNotifyRealtimeTask) — đều dùng lại nguyên văn notify_content_main, không format lại.

4. Đánh giá ảnh hưởng
        4.1 List function
            - SentMessageService.startService
            - ActionScheduleBotTask.run
        4.2 List những data bị update khi fix bug
            - Không có.
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Notify broadcast (メッセージ配信): gửi broadcast tới tệp >= 1000 friend, check notify trên LME-Studio, app mobile, Chatwork hiển thị "12,345人".
            - Notify action schedule (アクションスケジュール実行): chạy action schedule với tệp >= 1000 friend, check số 対象人数 có dấu phẩy.
            - Check lại case số nhỏ (< 1000) vẫn hiển thị bình thường, không dính dấu phẩy thừa.

5. Commit / Branch
        5.1 Commit hoặc pull request
            - c191091d
        5.2 Branch hiện tại của task
            - m_202608_broadcast-notify-thousand-separator_39176
```
