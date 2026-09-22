# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40896 — [LME-Studio] Job callback xử lý mỗi webhook 2 lần và luồng tải media không bao giờ chạy (MODE=NORMAL)` |
| Module / Màn hình | Job xử lý callback LINE (`linect-service` — `HandlePostbackTask`) + luồng download media (`startJobGetMediaEvent`). Ticket cha: `#40889 [JOB] Job xử lý callback + nhận callback request từ phía LINE support lưu và xử lý request đầy đủ` |

## Mô tả bug (bản dịch tiếng Việt)

Bug từ **LME Test Studio** — severity **High**.

- Task Studio: **#298**
- Test case phát hiện: **NEW-19**

Chạy service `linect-service` ở nhánh `m_202609_forward_webhook_40475_release-callback` (commit `f6104a35`) với config `MODE` mặc định (`NORMAL`), `ENABLE_POSTBACK=1`, `ENABLE_DOWNLOAD_MEDIA=1` thì job xử lý callback bị **chạy 2 vòng quét song song** trên cùng bảng `callback_event`, khiến mỗi webhook bị xử lý hai lần; đồng thời **vòng quét của luồng tải media không được khởi động lần nào** nên row callback có media nằm kẹt vĩnh viễn ở trạng thái 30 (chờ tải media).

Bằng chứng từ `jstack` trên tiến trình job: `HandlePostbackTask$1` (vòng quét callback_event) = **2 thread**, `HandlePostbackTask$2` (worker) = **203 thread**, `lambda$startJobGetMediaEvent` (vòng quét media) = **0 thread**.

## Steps to reproduce

1. Chạy service `linect-service` (nhánh `m_202609_forward_webhook_40475_release-callback`, commit `f6104a35`) với config `MODE` mặc định (`NORMAL`) và `ENABLE_POSTBACK=1`, `ENABLE_DOWNLOAD_MEDIA=1`
2. Gửi 1 webhook message tới `POST /line/callback/add/{bot_id}` của một bot có rule 自動応答 (auto-reply) khớp từ khoá
3. Đếm bản ghi `messages_v2s` của conversation và bản ghi `auto_reply_history` của (`line_user`, `auto_reply`) trước/sau
4. Tạo thêm 1 `callback_event` có event message `type=image` (trạng thái 0) và theo dõi status của row
5. Chạy `jstack` trên tiến trình job và đếm thread: `HandlePostbackTask$1` (vòng quét), `$2` (worker), `lambda$startJobGetMediaEvent` (vòng quét media) — quan sát được **2 / 203 / 0**
6. Các testcase cùng root cause này: `17594` (kết quả nghiệp vụ nhân đôi), `17593` (row media kẹt ở trạng thái 30), `17584` và `17585` (một callback tạo hai kết quả nghiệp vụ)

## Expected result

- Mỗi webhook được xử lý **đúng một lần**: một bản ghi lịch sử hội thoại, một lần trả lời tự động.
- Row có media đi qua trạng thái **30** rồi **được tải** và kết thúc ở trạng thái đã xử lý xong.

## Actual result

- Một webhook sinh ra **HAI** bản ghi lịch sử hội thoại và **HAI** bản ghi `auto_reply_history` → friend nhận tin trả lời tự động **2 lần**.
- Row callback có media **đứng mãi ở trạng thái 30** (chờ tải media), media **không bao giờ được tải**.
- `jstack`: **2** thread vòng quét `callback_event`, **203** thread worker, **0** thread vòng quét media.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- `thống kê thread của JVM.txt` (583 bytes) — https://redmine.watermelon.vn/attachments/download/30391/th%E1%BB%91ng%20k%C3%AA%20thread%20c%E1%BB%A7a%20JVM.txt
- `log job.log` (51191 bytes) — https://redmine.watermelon.vn/attachments/download/30392/log%20job.log

## Ghi chú thêm của Leader

- ⚠️ Bug do **AI Auto test Lme** raise từ LME Test Studio (task #298, TC `NEW-19`), **không phải** khách hàng/CS báo. Tracker = `Bug Tester`, status = `New`, chưa có journal điều tra nào từ Dev.
- ⚠️ **Redmine #40896 CHƯA có mục "Đánh giá ảnh hưởng phía dev"** → file `03-dev-impact.md` hiện đang dùng đánh giá của **ticket cha #40889** (cùng branch + commit). Đánh giá đó nói về việc đổi format cột `callback_event.request`, **KHÔNG** cover root cause "2 vòng quét + 0 thread media" của bug này. Phải yêu cầu Dev bổ sung đánh giá riêng cho #40896.
- **Điều kiện tiên quyết dựng env**: service `linect-service`, config `MODE=NORMAL` (mặc định), `ENABLE_POSTBACK=1`, `ENABLE_DOWNLOAD_MEDIA=1`; bot phải có rule 自動応答 khớp từ khoá; cần quyền chạy `jstack` trên tiến trình job.
- **Tần suất**: theo mô tả là lỗi cấu hình khởi động job (số thread sai ngay từ lúc start) → tái hiện **100%** khi chạy đúng MODE=NORMAL, không phải lỗi xác suất.
- **Môi trường phát hiện**: môi trường chạy job của Studio (TC `NEW-19` chạy ở `env = local`). ⚠️ **RULE-08** — bug thuộc nhóm **job nền + media**, kết luận từ local/staging là chưa đủ.
- Bug là **lỗi cấu hình/khởi tạo scheduler theo MODE**, không phải lỗi màn hình → TC phải quan sát được ở tầng hành vi (tin auto-reply nhận mấy lần, media hiển thị được chưa, row có thoát trạng thái chờ không), kèm bằng chứng đếm thread.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Service / nhánh | `linect-service` — `m_202609_forward_webhook_40475_release-callback`, commit `f6104a35` |
| Config gây lỗi | `MODE=NORMAL` (mặc định) · `ENABLE_POSTBACK=1` · `ENABLE_DOWNLOAD_MEDIA=1` |
| Endpoint | `POST /line/callback/add/{bot_id}` |
| Bot | Bot có rule 自動応答 khớp từ khoá — `<bot_id: chưa ghi trong ticket>` |
| Bảng quan sát | `callback_event` (status 0 → 30 → done) · `messages_v2s` · `auto_reply_history` |
| Thread quan sát (jstack) | `HandlePostbackTask$1` = 2 (kỳ vọng 1) · `HandlePostbackTask$2` = 203 · `lambda$startJobGetMediaEvent` = 0 (kỳ vọng ≥ 1) |
| TC Studio liên quan | `NEW-19` (fail, gắn ticket 40896) · `17594` · `17593` · `17584` · `17585` |
| Đối chứng | `<chưa có — ticket không ghi MODE nào chạy đúng>` |
