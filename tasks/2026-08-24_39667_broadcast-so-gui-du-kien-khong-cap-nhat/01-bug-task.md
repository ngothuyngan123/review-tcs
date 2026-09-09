# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task https://redmine.watermelon.vn/issues/39667`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39667 — [17-08-2026] [TY-11914] [Broadcast] Số gửi dự kiến không cập nhật, điều kiện lọc bị reset khi đặt lịch mới` |
| Redmine URL | https://redmine.watermelon.vn/issues/39667 |
| Auto-filled | `2026-08-24 by /new-task` |
| Ngày báo cáo | `2026-08-17` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn: OEM tạo task trên Slack — ユーザー問い合わせ, 管理番号 **TY-11914**, 担当 **後藤**, LOA **日テレポシュレ　本店**, địa chỉ a_takahashi@interspace.inc) |
| Module / Màn hình | `Broadcast` (Redmine category id 68) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — description không ghi domain>`. Journal #130744 (Kim Cúc, 2026-08-20) tái hiện trên **account KH**, broadcast id `1600019`. |
| Tracker / Status | `Bug KH` / `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |
| Commit Date (custom field) | `2026-08-20` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine. KHÔNG diễn giải lại. -->

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-11914
担当: 後藤
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1786943081004169?thread_ts=1786943081.004169&cid=C0BALS7S73L

Số quản lý：TY-11914
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BRFH8RXUY
Địa chỉ：a_takahashi@interspace.inc
Tên LOA：日テレポシュレ　本店
Phụ trách：後藤
Công cụ：リンク
Nội dung liên hệ
【操作方法に関するお問い合わせフォーム】
Tôi đã đặt lịch gửi tin nhắn (message broadcast), nhưng số lượng gửi hiện đang hiển thị 20 người (dự kiến) và số lượng gửi chính thức không được cập nhật.
※Dù đã nhấn 「現時点での配信予定数を再計算」, số liệu vẫn không cập nhật từ 「2026.08.12 21:38 時点の配信予定数」.

Cách đặt lịch gửi là copy nguyên điều kiện lọc đã dùng để gửi trước đó rồi thiết lập.

Ngoài ra, khi thiết lập gửi tin nhắn mới, dù chỉ định điều kiện lọc và đăng ký, sau khi hoàn tất đặt lịch thì điều kiện lọc lại bị reset.

Xin lỗi vì đã làm phiền,
mong được xác nhận giúp.

---
### 原文 (JP)

```
管理No　：TY-11914
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BRFH8RXUY
アドレス ：a_takahashi@interspace.inc
LOA名　　：日テレポシュレ　本店
担当　　 ：後藤
ツール　 ：リンク
問い合わせ内容
【操作方法に関するお問い合わせフォーム】
メッセージ配信の配信予約を行いましたが、配信数が20人（予定）となっており、正式な配信数が更新されません。
※「現時点での配信予定数を再計算」をクリックしても、「2026.08.12 21:38 時点の配信予定数」から更新されません。

配信予約の方法は、過去に配信した絞り込み条件をそのままコピーし設定しております。

また、新規でメッセージ配信設定を行う際、絞り込み条件を指定して登録をしても、予約完了後絞り込み条件がリセットされてしまいます。

お手数おかけしますが、
ご確認、よろしくお願いいたします。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> ⚠️ Description Redmine **KHÔNG có** section "Tái hiện bug". Các bước dưới đây lấy nguyên văn từ **journal #130744** (Kim Cúc, 2026-08-20) — QA verify lại trước khi dùng làm chuẩn.

1. Vào broadcast id: `1600019` (account KH)
2. Broadcast đang có setting filter
3. Click vào filter

## Expected result

> Suy từ mô tả của khách hàng (description), không phải section "Expected" riêng.

- Bấm 「現時点での配信予定数を再計算」 → số gửi dự kiến **và** mốc thời gian được cập nhật theo điều kiện lọc hiện tại.
- Mở lại broadcast đang có điều kiện lọc → hiển thị **đúng** điều kiện lọc đã lưu.
- Thiết lập gửi tin mới có chỉ định điều kiện lọc → sau khi hoàn tất đặt lịch, điều kiện lọc **vẫn còn**, không bị reset.

## Actual result

> Từ description + journal #130744.

- Số gửi hiển thị `20人（予定）`, số gửi chính thức không được cập nhật.
- Bấm 「現時点での配信予定数を再計算」 không cập nhật, vẫn giữ mốc 「2026.08.12 21:38 時点の配信予定数」.
- Click vào filter thì **không hiển thị** filter đã lưu, chỉ hiển thị 20 friend.
- Response: `success: false`, msg: `SQLSTATE[HY000]: General error: 1390 Prepared sta...` (bị cắt trong journal).
- Thiết lập gửi tin mới: sau khi hoàn tất đặt lịch, điều kiện lọc bị reset.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [x] Có log / request-response (message lỗi SQL trong journal #130744)

- https://redmine.watermelon.vn/attachments/download/29062/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-08-17%20105421.png
- https://redmine.watermelon.vn/attachments/download/29063/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-08-17%20105523.png

## Ghi chú thêm của Leader

- ⚠️ Description Redmine **không có** section "Tái hiện bug" theo format chuẩn. Steps/Actual ở trên ghép từ description khách hàng + journal #130744 của QA. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`) — TCs nên tập trung verify cách fix + regression impact.
- **Điều kiện tái hiện then chốt**: bug chỉ nổ trên **account nhiều bạn bè** (lỗi `1390 Prepared statement contains too many placeholders`, giới hạn 65535 tham số). Dev ghi rõ đã gặp trên **bot 111533**. Env test có ít friend sẽ **không** tái hiện được → xem cảnh báo RULE-08 ở `04-tc-list.md`.
- Bug **ảnh hưởng nghiệp vụ KH**: khách hàng đã **dừng gửi tin định kỳ hàng tuần (週次配信)** vì không biết số lượng gửi (journal #129122).
- Khách hàng còn hối tiến độ ngày 2026-08-24 (journal #132462).
- Timeline journals: 6 comment Slack (2026-08-17) → báo cáo AI Auto-fixbug #130706 (2026-08-20) → QA tái hiện #130744 (2026-08-20) → KH hỏi tiến độ #132462 (2026-08-24).
