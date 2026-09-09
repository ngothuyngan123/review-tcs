# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39255 — [JOB] Web push notification PC bị lỗi java.io.IOException: Connection reset by peer` |
| Redmine URL | https://redmine.watermelon.vn/issues/39255 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-08-01` |
| Khách hàng / PM báo | `Thanh Duy Nguyen` (tracker: **Bug tự detect** — phát hiện từ log, không phải khách báo) |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set category; theo log: job `HandleWebpushTask` / Web push notification PC. Studio gắn feature = `notify-setting`) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description không ghi env. Log có `botId 202606 pushId 633376` + timestamp `2026-08-01 10:46:06`; **tester xác nhận log này lấy từ Production hay môi trường nào** |

> Thông tin bổ sung từ Redmine: status hiện tại = **Closed** (chuyển bởi Hoang Xuan Thang, 2026-08-21) · assigned_to = **Hạnh Nguyễn** · parent issue = **#33291** · project = Lme · start_date = 2026-08-01.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Detail lỗi: 
2026-08-01 10:46:06 ERROR WebPushNotificationService:64 - #sendPushNotifyPC Exception: botId 202606 pushId 633376
java.util.concurrent.ExecutionException: java.io.IOException: Connection reset by peer
	at org.apache.http.concurrent.BasicFuture.getResult(BasicFuture.java:71)
	at org.apache.http.concurrent.BasicFuture.get(BasicFuture.java:84)
	at org.apache.http.impl.nio.client.FutureWrapper.get(FutureWrapper.java:70)
	at nl.martijndwars.webpush.PushService.send(PushService.java:64)
	at sns.line.helper.WebPushNotificationService.sendPushNotifyPC(WebPushNotificationService.java:49)
	at sns.line.models.line.LineModel.webPushPc(LineModel.java:297)
	at sns.line.threads.notify.HandleWebpushTask.actionPushPc(HandleWebpushTask.java:58)
	at sns.line.threads.notify.HandleWebpushTask.run(HandleWebpushTask.java:39)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:750)
Caused by: java.io.IOException: Connection reset by peer
	at sun.nio.ch.FileDispatcherImpl.read0(Native Method)
	at sun.nio.ch.SocketDispatcher.read(SocketDispatcher.java:39)
	at sun.nio.ch.IOUtil.readIntoNativeBuffer(IOUtil.java:223)
	at sun.nio.ch.IOUtil.read(IOUtil.java:197)
	at sun.nio.ch.SocketChannelImpl.read(SocketChannelImpl.java:379)
	at org.apache.http.nio.reactor.ssl.SSLIOSession.receiveEncryptedData(SSLIOSession.java:460)
	at org.apache.http.nio.reactor.ssl.SSLIOSession.isAppInputReady(SSLIOSession.java:522)
	at org.apache.http.impl.nio.reactor.AbstractIODispatch.inputReady(AbstractIODispatch.java:120)
	at org.apache.http.impl.nio.reactor.BaseIOReactor.readable(BaseIOReactor.java:162)
	at org.apache.http.impl.nio.reactor.AbstractIOReactor.processEvent(AbstractIOReactor.java:337)
	at org.apache.http.impl.nio.reactor.AbstractIOReactor.processEvents(AbstractIOReactor.java:315)
	at org.apache.http.impl.nio.reactor.AbstractIOReactor.execute(AbstractIOReactor.java:276)
	at org.apache.http.impl.nio.reactor.BaseIOReactor.execute(BaseIOReactor.java:104)
	at org.apache.http.impl.nio.reactor.AbstractMultiworkerIOReactor$Worker.run(AbstractMultiworkerIOReactor.java:591)
	... 1 more
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống, không suy diễn. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — stack trace `java.io.IOException: Connection reset by peer` nằm nguyên văn trong description (không có file attachment trên Redmine)

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Bổ sung:
- Đây là **bug tự detect từ log job**, không có kịch bản người dùng thao tác → điều kiện tái hiện là **bắn nhiều web push PC đồng thời qua 10 thread**, không phải một luồng UI.
- Bộ TC hiện có (file `04-tc-list.md`) **không lấy từ Sheet human mà lấy từ MCP LME TEST STUDIO task #46** (Redmine không có "Link TCs"). 25/29 TC do AI sinh.
