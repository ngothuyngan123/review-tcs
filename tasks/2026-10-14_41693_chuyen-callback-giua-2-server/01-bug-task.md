# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41693 — [job][lme]chuyển callback giữa 2 server chỉ bằng domain mà không cần ssh vào để thao tác chuyển mode` |
| Module / Màn hình | Action Settings — job `ActionService` / `SentMessageService` (queue gửi tin nhắn cho action từ bảng `action_line_user`) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nguyên văn description Redmine, dịch sát sang tiếng Việt. Ticket này là Feature (hạ tầng job gửi tin), không phải bug tái hiện trên UI. -->

1. Chuyển callback giữa 2 server chỉ bằng domain mà không cần ssh vào để thao tác chuyển mode.
`cb.lmes.jp`.
callback `.197`: chính.
contabo: backup callback → đã có cơ chế chạy callback mode main.
- Chưa tách job action-line-user:
  + Giải pháp: chuyển job này sang 1 trong các job chung, sửa code dùng queue send message riêng.

**Plan:** tuần này
- Release step 29/09
- Dev 30/09 - 1/10, test: 1-5/10

**Base branch:** `release-t09-2026`
- `RequestSentQueue` thêm 1 queue mới để phục vụ riêng cho job `ActionService`
- Job `ActionService`: khi gửi tin nhắn thì push vào Queue riêng
- `SentMessageService` thêm 1 logic xử lý item trong queue có MAX số luồng default = 20, số luồng này cho load từ config

## Steps to reproduce

<!-- Không có — ticket là Feature (tách queue gửi tin cho job ActionService), không phải bug tái hiện được trên UI. Root cause/cách fix xem file 03. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41693 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ Ticket **loại Feature** (tách queue gửi tin nhắn của job `ActionService` ra khỏi queue `NORMAL` dùng chung với callback/postback/scenario/broadcast), không phải bug end-user tái hiện được trên UI — không có section "Tái hiện bug" trong Redmine. Root cause/cách fix (nguyên văn journal Dev 2026-10-05) nằm ở `03-dev-impact.md`.

Branch dev: `m_202610_action-service-send-queue_41693` (khác base branch `release-t09-2026` ghi trong description — Dev đã tạo branch riêng cho task, xem commit trong journal).

## Journal / note từ Redmine (nguyên văn)

**Journal #140239 — Thanh Duy Nguyen — 2026-10-05:**

```
📊 Báo cáo đánh giá ảnh hưởng (AI tạo tự động):

Commit: 17a1ff385dd79ddf22abec559ae3ab3c1b78da2f

Feature #41693 [job][lme]chuyển callback giữa 2 server chỉ bằng domain mà không cần ssh vào để thao tác chuyển mode

1. Mục đích
   - Tách luồng gửi tin nhắn của job ActionService (action_line_user) ra queue send message riêng để có thể chuyển job này sang job chung mà không chiếm queue NORMAL của callback.

2. Cách thực hiện
   - RequestSentQueue thêm actionServiceRequestQueue; ActionModel.doAction(ActionLineUser) gắn cờ SEND_BY_ACTION_SERVICE_QUEUE (kế thừa cho action con tag/friend info) để push vào queue riêng.
   - SentMessageService thêm pool riêng xử lý queue này, số luồng load từ config MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD (default 20); retry 429 quay lại đúng queue gốc, tracking queue treo > 1 phút.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
   - ActionModel.doAction(ActionLineUser) chỉ có 1 caller là ActionService.doActions; các caller khác của ActionModel.doAction (postback, scenario, ActionScheduleBotTask...) không có cờ nên vẫn push queue NORMAL như cũ.

4. Đánh giá ảnh hưởng
        4.1 List function
            - ActionModel.doAction, ActionModel.isSendByActionServiceQueue, ActionModel.buildSubActionMapOption
            - RequestSentQueue.pushRequestToActionServiceQueue, getRequestFromActionServiceQueue, checkInTimeRetryRequest
            - SentMessageService.startService, startSendMessageThreads, startTrackingQueue
            - AppMain.logAllMessageRequestSendTrappedInQueue
        4.2 List những data bị update khi fix bug
            - Config mới (tuỳ chọn) MAX_SENT_MESSAGE_ACTION_SERVICE_THREAD trong config.properties, mặc định 20; không đổi DB.
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Action từ bảng action_line_user (job ActionService, vd 友だちリスト アクション, admin action): check tin nhắn gửi đúng, log "#pushRequestToActionServiceQueue".
            - Action con gắn tag / friend info chạy trong action trên: check tin nhắn cũng đi queue ACTION_SERVICE.
            - Gửi tin nhắn callback/postback/scenario/broadcast: check vẫn đi queue NORMAL, không đổi hành vi.
            - Retry khi LINE trả 429 cho tin nhắn action: check retry đẩy lại đúng queue ACTION_SERVICE.
            - Shutdown job: log size queue ACTION_SERVICE còn tồn.

5. Commit / Branch
        5.1 Commit hoặc pull request
            - (cùng commit với báo cáo này trên branch m_202610_action-service-send-queue_41693)
        5.2 Branch hiện tại của task
            - m_202610_action-service-send-queue_41693
```
