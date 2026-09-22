# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #35932 — Journal #132627 (Thanh Duy Nguyen, 2026-08-24) "📊 Báo cáo đánh giá ảnh hưởng (AI tạo tự động)". Chi tiết điều tra: attachment `bug_35932_chat11_delay_friendinfo.md`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | Commit `7bc51be1cb5a6f01c469b9c5b5228049dcaaf788` (chưa có link PR) |
| Branch | `m_202608_chat11-delay-friend-info_35932` (base `release-t07-2026`) |
| Ngày submit đánh giá | 2026-08-24 |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- `DelayMessageService.java:143` truyền `req.templateIds` = id template CHA (group, vd 105649) trong khi `listMessageToSave` lại mang id template CON (105650, 105651) do `buildSourceMessageForTemplate` expand group.
- `SentMessageHelper.java:104` tìm `MessagesV2s` theo `templateIds.contains(templateId)` nên không khớp cái nào, `build()` nhận map throwaway (`new HashMap<>()`) => `replace_content` lưu rỗng => chat 1:1 render nguyên code `[FRIEND_INFO_xxx]` (tin gửi sang LINE vẫn đúng vì text đã replace lúc build).

## 2. Cách fix

- Trong `DelayMessageService` gom id template CON vào `templateListSend` khi duyệt `sourceMessagesList` và dùng list này làm `templateIds` của `RequestSentTemplateToUser`, thay cho `Collections.singletonList(item.getTemplateId())`.
- Cách này đưa luồng delay về đúng như luồng gửi ngay `ScheduleSendChatTask.sendNow` (:97-120) vốn không bị lỗi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

Thay đổi nằm gọn trong `DelayMessageService.startJobAddMessageToQueue`, không đổi signature nên không có caller nào phải sửa. Đã check 3 chỗ tiêu thụ `req.getTemplateIds()` / `parentTemplateId`:

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SentMessageHelper.sentMessage` (:81-150) | Không sửa | Match theo id template con → sau fix mới khớp đúng |
| 2 | `SentMessageHelper.updateQuoteToken` (:546) | Không sửa | Match theo id template con → sau fix mới khớp (trước fix `quote_token` luồng delay bị bỏ sót) |
| 3 | `SentMessageHelper.checkError` (:572) | Không sửa | Match theo id template con → sau fix mới khớp (trước fix `message_line_capture` luồng delay bị bỏ sót) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `DelayMessageService.startJobAddMessageToQueue` | `src/main/java/sns/line/helper/DelayMessageService.java:126-148` | Direct | Điểm sửa duy nhất |

### 4.2. List data bị update khi fix bug

Không có thay đổi DDL/config/constant. Chỉ khác dữ liệu ghi ra runtime:

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `messages_v2s.replace_content` | UPDATE (runtime ghi) | Message gửi qua luồng delay |
| D2 | `messages_v2s.quote_token` / `line_message_id` | UPDATE (runtime ghi) | Message gửi qua luồng delay |
| D3 | `message_line_capture` | CREATE (runtime ghi) | Bản ghi của message gửi qua luồng delay |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 đặt lịch gửi có bật delay/random message: test template group nhiều message có chứa friend info, check nội dung hiển thị đã thay giá trị (không còn `[FRIEND_INFO_xxx]`) và tin LINE nhận được vẫn đúng | F1, D1 | *(Dev không ghi mức)* |
| T2 | Chat 1:1 đặt lịch gửi KHÔNG bật delay (sendNow): test lại để chắc không đổi, luồng này không sửa | — | *(Dev không ghi mức)* |
| T3 | Random message tách message của template group (`SendRandomMessage` sinh từ `MessageBuilder:167`): test template đơn gửi qua delay vẫn gửi và hiển thị đúng | F1, D1 | *(Dev không ghi mức)* |
| T4 | Reply/quote và unsend ở chat 1:1 với message gửi qua delay: sau fix `quote_token` và `message_line_capture` mới được ghi, cần check màn chat hiển thị và thao tác quote hoạt động bình thường | F1, D2, D3 | *(Dev không ghi mức)* |
| T5 | Lưu ý regression: với template group có bật cờ `is_delay_sent_message`, luồng delay nay gửi hết message con trong 1 lần (giống sendNow) thay vì tự giãn thời gian từng message con — hành vi này trước đó sinh ra bản ghi message rỗng/trùng nên coi là sửa cho nhất quán | F1 | *(Dev không ghi mức)* — **thay đổi hành vi, cần Leader/PO xác nhận** |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
