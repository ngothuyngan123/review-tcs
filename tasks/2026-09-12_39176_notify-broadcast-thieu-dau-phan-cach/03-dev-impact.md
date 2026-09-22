# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Văn Dũng Đinh` (người submit đánh giá) — assignee Redmine: `Đoàn Thị Bích Hảo` |
| Commit / Pull Request | `c191091d` |
| Branch | `m_202608_broadcast-notify-thousand-separator_39176` (base: `release-t07-2026`) |
| Ngày submit đánh giá | `2026-08-26` (Journal #133006) |
| Auto-filled | `2026-09-12 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- `SentMessageService.java:66` build nội dung notify bằng `String.format("配信人数 %s人 ...")` — `%s` in số `int` thô nên số người nhận từ 4 chữ số trở lên hiển thị `"12345人"` thay vì `"12,345人"`.
- Cùng lỗi ở `ActionScheduleBotTask.java:126` (`"対象人数 %s人"`) — chung luồng notify `mobile_notify`, fix chung để QA test 1 lượt.

## 2. Cách fix

- Đổi format specifier `%s` → `%,d` ở cả 2 chỗ. **Không** thêm helper mới (`TextUtils.getMoneyValue` hiện chỉ có overload `Long`) để tránh conflict với branch #33332 chưa merge.

Snippet Dev ghi trong ticket:

```java
// 1. SentMessageService.java:66
String contentNotify = String.format("配信人数 %,d人  タイトル：%s", requestSentTemplateToUser.getSuccessSendCount().get(), broadcastTitle);

// 2. ActionScheduleBotTask.java:126
String contentNotify = String.format("%sが稼働しました（対象人数 %,d人）", title, sendCount);
```

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev kết luận: **không ảnh hưởng caller** — chỉ đổi format specifier của biến local `contentNotify`, không đổi signature hay behavior của method nào.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ActionLaterService.buildNotifyContent` | Không đổi | Dùng lại nguyên văn `notify_content_main`, không format lại |
| 2 | `HandlePushNotifyPc` | Không đổi | Dùng lại nguyên văn `notify_content_main`, không format lại |
| 3 | `HandlePushNotifyChatwork` | Không đổi | Dùng lại nguyên văn `notify_content_main`, không format lại |
| 4 | `HandleMobileNotifyRealtimeTask` | Không đổi | Dùng lại nguyên văn `notify_content_main`, không format lại |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SentMessageService.startService` | `SentMessageService.java:66` | Direct | Đổi `%s` → `%,d` cho `配信人数` (số gửi thành công của broadcast) |
| F2 | `ActionScheduleBotTask.run` | `ActionScheduleBotTask.java:126` | Direct | Đổi `%s` → `%,d` cho `対象人数` (số đối tượng của action schedule) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** (Dev ghi rõ) | — | Fix nằm ở tầng ghi chuỗi hiển thị, không migrate, không đổi giá trị số lưu trong DB |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Notify broadcast (メッセージ配信) — gửi broadcast tới tệp ≥ 1000 friend, check notify trên LME-Studio, app mobile, Chatwork hiển thị `"12,345人"` | F1 | Medium |
| T2 | Notify action schedule (アクションスケジュール実行) — chạy action schedule với tệp ≥ 1000 friend, check số `対象人数` có dấu phẩy | F2 | Medium |
| T3 | Case số nhỏ (< 1000) vẫn hiển thị bình thường, không dính dấu phẩy thừa | F1, F2 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
