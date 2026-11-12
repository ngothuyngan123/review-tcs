# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` (job Java linect-service) · `Do Van Tu (TuDV)` (web sns-line, AI workflow, đã đóng 23/09) |
| Commit / Pull Request | Job Java: `7ce65dc`, `0a0f3b4`, `3464917`, `c8c8831`, `00d1741`, `902796f`, `18308c8`. Web: `892d8fe8bd` (fix thật duy nhất — `TalkListController.php`). |
| Branch | Job Java: `m_202610_notify-limit-100-percent_39389` (base: xem Redmine, không ghi rõ base cụ thể trong journal). Web: `ai-feature-39389` (Studio base `release_step_20260827`). |
| Ngày submit đánh giá | `2026-10-08` (Journal #141074 — bản cuối cùng, thay thế 2 bản trước 17/09 và 23/09) |
| Auto-filled | `2026-10-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

> ⚠️ **Input thiếu / lưu ý nguồn**: Redmine issue #39389 là **Feature**, không có section "Tái hiện bug" / "Đánh giá ảnh hưởng" chuẩn 4 mục (1.Nguyên nhân/2.Cách fix/3.Caller/4.Impact) trong **Description**. Nội dung dưới đây lấy từ **Journal #141074** (2026-10-08, Thanh Duy Nguyen) — là bản thiết kế có cấu trúc gần nhất với format chuẩn (1.Mục đích ~ Nguyên nhân/bối cảnh · 2.Cách thực hiện ~ Cách fix · 3.Caller · 4.1/4.2/4.3 Impact · 5.Commit/Branch), và **khớp 100%** với `dev_impact` + `spec_delta` đọc từ MCP LME TEST STUDIO (`task_id=350`, `computedAt=2026-10-08`). Đây là bản **thay thế** 2 bản trước (17/09 đã bị huỷ hiệu lực bởi 23/09; 23/09 mô tả scope + 1 bug web đã vá — vẫn còn giá trị, xem file `01-bug-task.md` phần Ghi chú Leader).
>
> Phần việc **web** (1 bug thật đã vá ở `TalkListController.php`, commit `892d8fe8bd`) lấy từ Journal #137843 (23/09) — không có trong #141074 vì #141074 chỉ nói về job Java.

## 1. Nguyên nhân (= Mục đích, theo Journal #141074)

Mốc 100% limit tin của LINE OA chính thức (LOA — gọi API LINE) và エルメ free plan (1.000 tin/tháng) phải **notify ngay lúc gửi message chạm/bị chặn limit**, không chờ job quét hằng ngày (`ScanLimitMessageLoaJob`, branch `release-recover-by-schedule`, chạy 1h sáng). Mỗi bot chỉ nhận **1 notify / mốc / tháng** dù nhiều jar / thread / web cùng phát hiện việc chạm trần cùng lúc (tránh trùng lặp notify khi nhiều nơi cùng insert).

Bối cảnh bổ sung (từ bản 17/09, vẫn đúng về root cause gốc): trước đây cảnh báo 100% chỉ do job 1 lần/ngày gọi API LINE lấy số tin đã gửi trong tháng rồi so mốc — khách phải chờ gần 1 ngày mới biết đã hết hạn mức. Màn Cài đặt thông báo đã chuyển sang mốc % (50/80/100%) nhưng phần sinh thông báo cũ dùng mã mốc theo số tin kiểu cũ (500/1.000, type 7/8) → không khớp cấu hình khách, cảnh báo 100% gần như không tới khách.

## 2. Cách fix (= Cách thực hiện, theo Journal #141074)

- Thêm **`LimitMessageNotifyModel`** (mới) — chống trùng **3 lớp**:
  1. Cache RAM theo JVM (key LOA kèm `channel_id`, retry sau 10 phút khi chưa có kết quả).
  2. UPDATE atomic cột `bots.limit_notify_loa_mark` / `bots.limit_notify_elme_mark` (giá trị `yyyyMM*1000+%`, chỉ tăng).
  3. Check `exists` trong `mobile_notify` theo bot + user + type + content trong tháng.
- Tạo `mobile_notify` **type 15** (+ `notification_pc`) cho user bật `is_notify_send_error` + mốc thông báo chứa **12** (LOA) hoặc **15** (エルメ). (Type 15 = 配信数アラート cho cả 2 loại trần; 12/15 là mã mốc trong 通知設定, không phải type.)
- Hook vào nhánh `REACH_LIMIT_FREE_PLAN`, `REACH_LIMIT_LINE` và khi `free_send_count` đạt 1.000 (chạy đồng bộ trong `SentMessageHelper`, dùng chung cho 一斉配信/step/chat/push).
- Cờ `ENABLE_NOTIFY_LIMIT_ON_SEND` (**mặc định bật**) để rollback nhanh nếu có sự cố.
- **Bỏ** notify cũ kiểu 500/1.000 tin (type 7/8 — không còn tồn tại).
- Change-bot sang OA khác → reset mark LOA (`resetLoaMarkForChangeBot`).

**Web (riêng, từ Journal #137843 23/09 — đã đóng, KHÔNG thuộc commit của #141074):** `TalkListController::ajaxTalkSendMessage` (トークリスト) sửa để trả đúng `status=0` + câu lỗi JP theo gói LINE thật khi chạm trần (Elme hoặc LINE), thay vì báo giả "送信しました". **KHÔNG tạo `mobile_notify`** ở web — đúng chốt TA 21/09 "web/app chỉ hiển thị alert trên UI, không tạo record".

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotModel.notifyReachFreeSendCount` | Giữ signature, bỏ notify 500/1.000 | 2 caller: `SentMessageHelper.sentMessage`, `BotModel.addSendCount` |
| 2 | `BotModel.notifyReachLimit100` | Gắn `LimitMessageNotifyModel` | 4 call site: `callSentPushMessage`, `callSent` (x2), `notifyReachFreeSendCount` |
| 3 | `ChangeBotJob.step1Recreate` | Gọi `resetLoaMarkForChangeBot`, catch mọi lỗi | 1 caller — đảm bảo OA mới sau change-bot vẫn báo lại được |
| 4 | `NotifyTypeConstants` (type 7/8) | Xoá — không còn caller | Notify cũ 500/1.000 đã bỏ |
| 5 | `TalkListController::ajaxTalkSendMessage` (web) | Đổi hợp đồng response lỗi (status=0/msg) | Vá bug báo giả thành công khi chạm trần (commit riêng 23/09, không nằm trong #141074) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `LimitMessageNotifyModel` (mới) | `src/main/java/sns/line/models/LimitMessageNotifyModel.java` | Direct | Chống trùng 3 lớp (RAM / mark atomic / exists DB) |
| F2 | `SentMessageHelper.callSentPushMessage`, `SentMessageHelper.callSent` | linect-service | Direct | Hook notify khi reach limit, dùng chung cho mọi luồng gửi nền (一斉配信/step/chat/push) |
| F3 | `BotModel.notifyReachFreeSendCount` | linect-service | Direct | Bỏ nhánh notify 500/1.000 cũ |
| F4 | `ChangeBotJob.step1Recreate` | linect-service | Direct | Reset mark LOA khi đổi OA |
| F5 | `BotRepository` (claim/release/reset mark, `findLimitMessageLoaById`) | linect-service | Direct | Hỗ trợ UPDATE atomic cột mark |
| F6 | `MobileNotifyRepository.existsByBotIdAndUserIdAndTypeAndNotifyContentAndNotifyTimeBetween` | linect-service | Direct | Lớp chống trùng thứ 3 (check exists) |
| F7 | `ConfigFile.ENABLE_NOTIFY_LIMIT_ON_SEND`, `NotifySetting.LIMIT_MESSAGE_*` (10-15), `NotifyTypeConstants` | linect-service | Direct | Cờ rollback + hằng mốc mới, xoá hằng cũ 7/8 |
| F8 | `TalkListController::ajaxTalkSendMessage` | `app/Http/Controllers/Basic/TalkListController.php` (web sns-line) | Direct | Fix riêng 23/09 — đổi response lỗi, KHÔNG liên quan commit job Java |
| F9 | 7 luồng gửi web/app khác (chat-v3 `createMessageV2`, 一斉配信 v2/v3, step/remind, QR/form quick send, event/salon/lesson v3, API `ChatController::createMessage` cũ) | web sns-line | Indirect — KHÔNG sửa code | Regression — đã audit 23/09, giữ hành vi cũ đúng theo gói LINE thật |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.limit_notify_loa_mark`, `bots.limit_notify_elme_mark` (cột mới) | MIGRATE (DDL `ai_docs/39389_alter_bots_limit_notify_mark.sql`) | **BẮT BUỘC chạy TRƯỚC khi deploy jar** — cờ mặc định bật, thiếu DDL ⇒ không notify được |
| D2 | `mobile_notify` | CREATE | type 15 (= 配信数アラート `DELIVERY_COUNT_ALERT`, dùng cho cả 2 loại trần) — chỉ tạo cho user có mốc 12 (LOA 100%) / 15 (エルメ 100%) trong 通知設定; tối đa 1 bản ghi/mốc/tháng/bot |
| D3 | `notification_pc` | CREATE | Tạo sau `mobile_notify`, cho kênh PC realtime |
| D4 | `notify_setting` | READ only | Check user có bật mốc 12/15 + `is_notify_send_error` |
| D5 | `bots` (hạn mức tháng, loại gói, `limit_message_loa`) | READ only | Chọn nội dung cảnh báo (nâng gói nếu ≤5000 hoặc NULL / mua thêm nếu >5000) |
| D6 | `mobile_notify` type 7/8 (notify cũ 500/1.000) | (ngừng tạo mới — dữ liệu cũ không xoá) | Hồi quy: mất cảnh báo sớm mốc 500 nếu có khách đang trông vào cảnh báo này |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Gửi message bot free khi `free_send_count` 999→1000 và khi đã chạm 1000 (job nền, mọi luồng: 一斉配信/step/chat/push) | F1,F2,F3,D2,D3 | High — notify phải đúng 1 lần, gửi tiếp/broadcast/nhiều jar không tạo thêm; tắt `is_notify_send_error` thì không notify |
| T2 | Gửi message khi LINE OA chạm limit tháng (monthly limit, LOA) | F1,F2,D2,D5 | High — nội dung đúng theo hạn mức (≤5000 nâng gói / >5000 mua thêm); Chatwork chưa liên kết room → `status_chat_work=1` |
| T3 | App Notification Settings (FA-055) — user bật mốc 12/15 sau khi bot đã chạm limit | F1,D2,D4 | Medium — lần gửi bị chặn sau ≥10 phút phải có notify; sang tháng mới notify lại |
| T4 | Change-bot sang OA khác | F4,D1 | Medium — OA mới vẫn nhận notify mốc 12 trong tháng; notify cũ type 7/8 không còn bắn |
| T5 | トークリスト (chat 1:1 web) — alert lỗi khi gửi chạm trần | F8 | High — REQ-001/002/003/004 (Studio): phải hiện đúng alert theo loại trần (Elme/LINE/lỗi khác), giữ nguyên luồng thành công |
| T6 | Các luồng gửi web/app khác (REQ-007 regression C-06) | F9 | Medium — đã audit, không sửa code, chỉ cần regression test giữ hành vi cũ |
| T7 | 「エラー一覧」 (ghi log lỗi gửi tin) | — | Low (REQ-008) — không đổi, chỉ regression |
| T8 | Deploy / vận hành: thiếu DDL D1 trước khi bật cờ `ENABLE_NOTIFY_LIMIT_ON_SEND` | D1,F7 | High (vận hành) — thiếu cột mark ⇒ không notify, báo lỗi ChatWork, nhưng **không** chặn gửi tin (an toàn luồng chính) |

> **Rủi ro chưa xử lý xong** (tự đánh giá của Dev qua Studio `dev_impact`, KHÔNG có trong journal gốc — Leader cần lưu ý khi review): job mới **chưa đồng bộ hoàn toàn** với job ngày `ScanLimitMessageLoaJob` (dùng `app_user_id` khác) và nhánh web cũ (nội dung khác) → **nguy cơ trùng notify trong cùng tháng**. Đây là GAP cần có TC riêng kiểm tra (xem §1/§7 report).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
