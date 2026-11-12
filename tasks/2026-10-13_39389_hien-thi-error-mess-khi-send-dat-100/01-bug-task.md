# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39389 — Hiển thị error mess khi send messages đạt đến 100%` |
| Module / Màn hình | `Chat management — トークリスト (chat 1:1 web) + luồng gửi tin nền (一斉配信/step/chat/push) của web sns-line + job Java linect-service xử lý limit gửi tin (LOA limit tháng LINE OA chính thức + エルメ free plan 1.000 tin)` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Dịch sát nội dung gốc Redmine, giữ thuật ngữ JP -->

Tên gốc (JP): 通知設定修正（配信数が100％に達した時点で通知を送信する）— "Sửa cài đặt thông báo (gửi thông báo ngay tại thời điểm số lượng gửi tin đạt 100%)".

Thay vì hiển thị lỗi hoặc gửi thông báo ngay tại thời điểm lấy dữ liệu qua API, (yêu cầu) hiển thị error mess khi send messages đạt đến 100%.

Link Slack thảo luận: https://l-message.slack.com/archives/C094LL6901W/p1785321574307639?thread_ts=1772173998.602049&cid=C094LL6901W
Link task (Google Apps Script): https://script.google.com/macros/s/AKfycbx_hQyrSEc2kkEWM1qW7TfpUlLgvdZJeEYCO0CsDuV2wuY2uKr6x2QH59MiXZvO4ADg/exec?ticket=6cad6283-ed87-4692-b981-f1bfee0d3840&page=54cd5461-e8fe-4c01-8acd-d4757f208300

[Detail task java]
- Base branch: release-t09-2026
- Mốc 100% của LME và LINE: sửa lại để notify ngay khi đạt limit lúc send message (không chờ job quét)
- Khi bot bị limit số lượng send của hệ thống LME, hoặc khi call API phía LINE: cần check xem đã có thông báo limit chưa, nếu chưa có thì chỉ insert notify 1 lần.
- Tham khảo job hiện tại chạy hàng ngày: branch `release-recover-by-schedule`, class `ScanLimitMessageLoaJob`.
- Cần tối ưu:
  + Hạn chế việc phải check lại xem đã có notify chưa mỗi lần gửi message.
  + Tránh trùng lặp notify vì có nhiều job chạy (hoặc web đã insert).
- Yêu cầu gốc: đọc file plan mode `ai-plan_mode/task_39389.md` (nội bộ dev, không đính kèm Redmine).

> ⚠️ Đây là **Feature** (loại ticket = Feature trên Redmine), không phải bug tái hiện từ 1 ca lỗi cụ thể của khách. Không có section "Tái hiện bug" trong Redmine.

## Steps to reproduce

<!-- Không có — Feature request, không phải bug có ca lỗi tái hiện cụ thể. Xem "Dữ liệu định danh ca lỗi" bên dưới cho điều kiện dựng env test (bot chạm trần). -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachment Redmine (1): `task_39389.md` — https://redmine.melonglobal.net/attachments/download/31434/task_39389.md (nội dung task chi tiết gốc, chưa fetch nội dung file này — có thể cần đọc thêm nếu 03-dev-impact chưa đủ).

## Ghi chú thêm của Leader

⚠️ **Scope đã đổi hướng 2 lần trong quá trình implement — đọc kỹ trước khi giao TC:**

1. **17/09/2026** (Journal #136843, tài khoản "AI LME Fix bug"): bản fix đầu tiên — web sns-line **tự tạo record `mobile_notify`** ngay lúc gửi tin chạm trần (hàm `notifyReachDeliveryLimit100` / `insertNotifyReachLimit100`, 7 file PHP, branch `ai_small_39389`).
2. **23/09/2026** (Journal #137843, Do Van Tu — TuDV): **HUỶ HIỆU LỰC** bản 17/09. TA/BA chốt ngược lại: *"Phía web hoặc app khi send lỗi chỉ hiển thị alert message lỗi trên UI ngay tại thời điểm send lỗi. KHÔNG tạo record mobile_notify."* → phần notify thật chuyển hẳn sang **job Java (linect-service)**. Web chỉ còn 1 bug thật được vá: màn トークリスト báo "送信しました" giả khi chạm trần (branch `ai-feature-39389`, commit `892d8fe8bd`, file `TalkListController.php`).
   - Điểm còn mở BA/TA chưa chốt dứt điểm lúc đó: **F-01** (2 luồng send-test `/send-test-template` v2 và `/basic/send_for_tester` trả câu lỗi chung cho mọi gói LINE, lệch BR-C06) · **F-02** (màn マイページ gửi tin luôn báo thành công, không kiểm kết quả — đề nghị tách ticket riêng, **KHÔNG thuộc phạm vi #39389**) · **F-03** (`TemplateService::sendTestMessage` có return sớm làm chết đoạn map câu lỗi, chưa lộ ra vì FE chỉ gọi bản v3) · **F-04** (câu lỗi web vẫn đoán theo gói Elme ở `functions.php`/`MessageService::handleErrorMessage` — giữ nguyên theo QA-08/P-03).
3. **08/10/2026** (Journal #141074, Thanh Duy Nguyen — Dev chính thức phụ trách job Java): bản thiết kế **cuối cùng** cho job Java — xem chi tiết đầy đủ ở `03-dev-impact.md`. Đây là nội dung dùng làm input chính cho review/write TC.

**Kết luận phạm vi hiện tại (theo Studio `dev_impact` + `requirements`, task #350, round 1):**
- **Web (sns-line, branch `ai-feature-39389`)**: CHỈ sửa `TalkListController::ajaxTalkSendMessage` (トークリスト) để hiện đúng alert lỗi (không còn báo giả thành công), **KHÔNG tạo `mobile_notify`**. Các luồng gửi khác (chat-v3 `createMessageV2`, một斉配信, step, send-test, salon/lesson, API `ChatController::createMessage` cũ) giữ hành vi cũ — cần **regression test**, không phải code mới (REQ-001 → REQ-008).
- **Job Java (linect-service, branch `m_202610_notify-limit-100-percent_39389`)**: phần việc chính — `LimitMessageNotifyModel` mới, tạo `mobile_notify` type 15 (配信数アラート) cho user bật mốc 12 (LOA 100%) / 15 (エルメ 100%) ngay tại thời điểm gửi tin bị chặn, chống trùng 3 lớp (RAM cache + `bots.limit_notify_*_mark` UPDATE atomic + check exists DB), bỏ notify cũ type 7/8 (REQ-009 → REQ-012).

⚠️ **Rủi ro cần lưu ý khi test** (từ Journal #141074 + Studio `dev_impact`):
- Cảnh báo chỉ tới khách nếu khách đã bật `is_notify_send_error` + mốc 12/15 trong cấu hình thông báo.
- Thiếu DDL (`bots.limit_notify_loa_mark`, `bots.limit_notify_elme_mark`) trước khi deploy jar (cờ `ENABLE_NOTIFY_LIMIT_ON_SEND` mặc định bật) → KHÔNG notify được, báo lỗi ChatWork, nhưng gửi tin không bị chặn.
- Cờ `ENABLE_NOTIFY_LIMIT_ON_SEND` = 0 → tắt hẳn toàn bộ notify mới (dùng để rollback).
- Nội dung cảnh báo mốc LOA 100% chọn theo `limit_message_loa` hiện lưu (≤5000 → câu nâng gói, >5000 → câu mua thêm, NULL → nâng gói); tài khoản chưa có số liệu có thể lệch bậc gói.
- Phần notify cũ kiểu 500/1.000 tin (type 7/8) **bị bỏ hẳn** → hồi quy: mất cảnh báo sớm mốc 500 nếu có khách đang trông vào cảnh báo này.
- Chưa đồng bộ hoàn toàn với job ngày `ScanLimitMessageLoaJob` (dùng `app_user_id` khác) và nhánh web cũ (nội dung khác) → nguy cơ trùng notify trong tháng — Studio `dev_impact` tự đánh giá đây là rủi ro **chưa xử lý xong**, cần test kỹ.
- Môi trường chạy test tới nay: Studio báo 50 TCs, mới chạy ở `local` (8 runs, automated 76%), **chưa chạy `dev`/`staging`/`prd`** — RULE-08 (bill tiền/job/domain) áp dụng vì đây là flow liên quan hạn mức gửi tin + job nền, không thể kết luận chỉ từ local.
- Ticket vẫn ở trạng thái Redmine "Đang fix" (status cuối cùng cập nhật 2026-10-13), Studio ở stage `tc-ready`, review state = `leader` (đang chờ Leader review) — chưa Closed/Resolved.

## Journal / note từ Redmine (nguyên văn)

**Journal #131732 — Nguyen Ngoc Hai — 2026-08-21:**
```
https://dashboard.melonglobal.net/implement-task-small-lme/?id=39389
```
*(Bỏ qua — chỉ là link dashboard, không có giá trị điều tra. Giữ lại cho đủ trace.)*

**Journal #136843 — AI LME Fix bug — 2026-09-17:** *(⚠️ ĐÃ BỊ HUỶ HIỆU LỰC bởi Journal #137843 dưới — chỉ giữ lại để trace lịch sử, KHÔNG dùng làm căn cứ viết/review TC)*
```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
■ 1. NGUYÊN NHÂN: Cảnh báo chạm trần 100% trước đây chỉ do job chạy 1 lần/ngày (1h sáng) gọi API LINE lấy số tin đã gửi rồi so mốc — tại thời điểm khách gửi tin bị chặn, hệ thống chỉ ghi lỗi gửi tin, không notify, khách phải chờ gần 1 ngày mới biết hết hạn mức. Màn Cài đặt thông báo đã chuyển sang mốc % (50/80/100%) nhưng phần sinh thông báo vẫn dùng mã mốc theo số tin kiểu cũ → không khớp, cảnh báo 100% gần như không tới khách.
■ 2. CÁCH FIX: Web sns-line (nhánh ai_small_39389) thêm hàm dùng chung notifyReachDeliveryLimit100 / insertNotifyReachLimit100 bắn mobile_notify mốc 12 (LOA)/15 (エルメ) ngay lúc gửi tin bị chặn, gắn vào 9 điểm xử lý lỗi hạn mức, 7 file PHP (functions.php, MobileNotifyService.php, MessageService.php, SalesManagementV2Controller.php, SalesService.php, HandleBillStripe.php, HandleSendActionTrialV2.php). Chống trùng: 1 lần/mốc/tháng (đối chiếu mobile_notify) + cache 30 phút.
■ BRANCH/COMMIT: sns-line: ai_small_39389 (gốc release_step_20260827, commit 6991a77d80, 7 file) [đã push]
```

**Journal #137843 — Do Van Tu (TuDV) — 2026-09-23:** *(comment tự động do workflow AI implement sinh ra, qua API key TuDV)*
```
★ CẬP NHẬT PHẠM VI & TÌNH TRẠNG #39389
■ 0. XIN HUỶ HIỆU LỰC comment 17/09 (AI LME Fix bug): mô tả phương án web TỰ TẠO mobile_notify — ĐÃ LỖI THỜI.
Lý do: 21/09/2026 TA (Tư DV) chốt ngược lại: "Phía web hoặc app khi send lỗi chỉ hiển thị alert message lỗi trên UI ngay tại thời điểm send lỗi. KHÔNG tạo record mobile_notify." Chốt này đã áp vào spec: C-01 → NO_OP, C-06 → NO_OP (web/app chỉ còn regression test). Branch ai_small_39389 KHÔNG khớp phạm vi đang chốt — đề nghị chưa test/chưa merge theo nó. (Đã thử gỡ comment 17/09 qua API nhưng không đủ quyền "Edit notes" — nhờ người có quyền xoá giúp, trước mắt coi là VÔ HIỆU.)

■ 1. PHẠM VI ĐÚNG THEO SPEC HIỆN TẠI
- Web sns-line: KHÔNG thêm điểm tạo thông báo nào. Chỉ cần alert lỗi hiện đúng ngay lúc gửi chạm trần (Elme 1.000通 / hạn mức LINE thật) ⇒ phần việc chính là REGRESSION TEST.
- Job Java (linect-service) — toàn bộ phần việc hiệu lực còn lại: C-02 (SentMessageHelper.callSent + BotModel.notifyLineLimitReached), C-03 (BotModel.addSendCount đổi so sánh vượt ngưỡng before<N && after>=N, nhánh clamp >1000 vẫn phải thông báo, ghi setting_value 7/8), C-04 (chống trùng theo tháng + khoá ngắn).
- QA-13 (BA/khách xác nhận chốt TA) vẫn đang MỞ — nếu lật lại thì thiết kế cũ cho web còn ở Technical Spec §3.2, bật lại được.

■ 2. ĐÃ LÀM PHÍA WEB (branch ai-feature-39389)
Audit 13 luồng gửi web/app theo QA-03: 8 luồng vốn đã hiện đúng câu theo gói LINE thật (chat 1:1 web+app · send test template v3 · 一斉配信 v2+v3 · ステップ配信/remind · QR quick send · form quick send · event/salon/lesson v3).
Phát hiện 1 LỖI THẬT và đã vá: màn トークリスト (POST /ajax/talk-list-send-message) — khi chạm trần (Elme hoặc LINE) vẫn báo "送信しました" dù tin KHÔNG gửi được. Nguyên nhân: FE chỉ hiện alert khi response có a.status==0, nhưng BE trả ResponseData (result/error_message) hoặc raw JSON của LINE → không khớp; kèm 1 đường gọi isSucceeded() trên kiểu bool → HTTP 500.
Đã sửa: app/Http/Controllers/Basic/TalkListController.php — commit 892d8fe8bd (ai-feature-39389). Nhánh lỗi trả status=0 + câu JP đúng gói LINE thật (コミュニケーションプラン / ライトプラン 5,000通 / スタンダードプラン 30,000通); trần Elme giữ câu cũ "配信数上限に達しています。こちらから契約内容を確認してください。". KHÔNG tạo mobile_notify.
Verify: php -l sạch; harness 8 kịch bản × 2 phiên bản: TRƯỚC fix 7/8 lỗi (6 báo thành công giả + 1 fatal); SAU fix 8/8 đúng kỳ vọng. CHƯA test runtime với DB/LINE thật.

■ 3. ĐIỂM CẦN BA/TA CHỐT (cố ý CHƯA tự sửa)
- F-01: 2 luồng send-test (/send-test-template v2, /basic/send_for_tester) trả câu lỗi CHUNG cho mọi gói LINE, lệch BR-C06. Không tự đổi vì Technical Spec §3.2 ghi "không sửa thông điệp lỗi trả cho người gửi — chỉ regression test".
- F-02: màn マイページ (/basic/friendlist/my_page/send-message) luôn trả "送信しました。" không kiểm kết quả gửi → thành công giả. Ngoài danh sách QA-03 — đề nghị tách ticket riêng.
- F-03: TemplateService::sendTestMessage có return sớm làm chết đoạn map câu lỗi phía dưới (chưa lộ vì FE chỉ gọi bản v3).
- F-04: khiếm khuyết G-2 "đoán câu lỗi theo gói Elme" không chỉ ở job Java — web (functions.php, MessageService::handleErrorMessage) cũng đoán theo gói Elme. Giữ nguyên theo QA-08+P-03, chỉ đính chính mô tả.
```

**Journal #137965 — AI LME Fix bug — 2026-09-23:**
```
[Dashboard] Đổi trạng thái: Đã push → Đã đóng
Lý do: chuyển sang implement
```

**Journal #139969 — Thanh Duy Nguyen — 2026-10-04:**
```
- Khi bot bị limit số lượng send của hệ thống Lme, hoặc khi call api phía LINE. Cần check xem có thông báo limit chưa, nếu chưa có chỉ insert notify 1 lần.
- Tham khảo job hiện tại chạy hàng ngày: branch release-recover-by-schedule, class ScanLimitMessageLoaJob.
- Cần tối ưu: hạn chế check lại đã có notify chưa mỗi lần gửi message; tránh trùng lặp notify vì có nhiều job chạy (hoặc web đã insert).
=> Hãy đưa ra phương án phù hợp cho tôi
```

**Journal #141074 — Thanh Duy Nguyen — 2026-10-08:** *(nội dung đầy đủ — xem `03-dev-impact.md`)*
