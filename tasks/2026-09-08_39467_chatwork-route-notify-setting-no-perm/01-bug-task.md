# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39467 — [LME-Studio] Các route ChatWork của màn 通知設定 không kiểm quyền — staff không có quyền vẫn ghi được cấu hình` |
| Module / Màn hình | `通知設定 (Cài đặt thông báo) — FA-006` · màn con `通知設定 ChatWork連携` (liên kết ChatWork) và 4 route ajax ChatWork của màn này |

## Mô tả bug (bản dịch tiếng Việt)

Bug do **LME Test Studio** tự phát hiện — severity **High**.
Nguồn trong Studio: `Task: #15` · `Test case: NEW-65`.
(⚠️ Task Studio đang gắn với ticket này hiện là **task #265**, temp_id các TC là `NEW-1..NEW-22` — số `#15` / `NEW-65` trong mô tả là đánh số của lần chạy phát hiện bug, không khớp task hiện hành. Xem file `04-tc-list.md`.)

Nội dung bug: nhân viên (staff) được mời vào bot nhưng role **KHÔNG** chứa màn 通知設定 vẫn ghi được cấu hình ChatWork của màn này, vì nhóm route ajax ChatWork không kiểm quyền màn hình như các route lưu cài đặt thông báo khác trong cùng màn.

## Steps to reproduce

1. Tạo staff được mời vào bot với role **KHÔNG** chứa màn 通知設定 (route `notifySetting`)
2. Đăng nhập bằng staff đó và chọn bot
3. Gọi `POST /basic/notify-setting-receive` → quan sát 403 (đúng)
4. Gọi `POST /ajax/notify/save-type_notify_send_chatwork` với `type_notify_send_chatwork` khác giá trị hiện tại
5. Đọc lại cột `type_notify_send_chatwork` của `notify_setting` (`bot_id`, `user_id`) đó

## Expected result

- Mọi endpoint đổi cấu hình thông báo (kể cả nhóm ChatWork) đều phải **từ chối** khi tài khoản không có quyền màn 通知設定.

## Actual result

- Route ChatWork `/ajax/notify/save-type_notify_send_chatwork` **chấp nhận** lệnh ghi từ staff không có quyền màn 通知設定 (HTTP **200**) và đã lưu `type_notify_send_chatwork` từ **0 → 1**.
- Xác minh độc lập bằng test script: các route lưu của màn 通知設定 **CÓ** gọi `userHasScreenAccess('notifySetting')` (`saveNotifySettingReceive`, `saveNotifySettingReceivePage`, `saveNotifySettings`), nhưng các route ajax ChatWork thì **KHÔNG** (`ajaxSaveUrlChatWork`, `ajaxSaveApiTokenChatWork`, `ajaxChangeTypeSendChatwork`, `ajaxTestSendChatwork`) — và lệnh ghi từ staff không có quyền đã được lưu lại.
- Tái hiện ở **run #207** (vòng 1, môi trường **local**).

Log lời gọi (nguyên văn từ ticket):

```json
[{"url":"/basic/notify-setting-receive","status":403,"body":"{\"success\":false,\"message\":\"この権限は許可されていません。\"}"},
 {"url":"/basic/notify-setting-receive-page","status":403,"body":"{\"success\":false,\"message\":\"この権限は許可されていません。\"}"},
 {"url":"/ajax/notify/save-api-token-chat-work","status":200,"body":"{\"success\":false,\"msg\":\"ChatworkAPIトークンが正しくありません。入力内容をご確認ください。\"}"},
 {"url":"/ajax/notify/save-type_notify_send_chatwork","status":200,"body":"{\"success\":true,\"type_notify_send_chatwork\":\"1\"}"}]
```

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/28863/tc-772-permission.log
- https://redmine.watermelon.vn/attachments/download/28864/tc-772-permission.log

## Ghi chú thêm của Leader

- **Môi trường phát hiện**: `local` — tái hiện ở run #207 của LME Test Studio. **Chưa có bằng chứng trên staging / production.**
- **Tần suất**: lỗi xảy ra 100% khi đúng điều kiện (staff không có màn 通知設定 trong role, gọi route ajax ChatWork).
- **Điều kiện tiên quyết dựng env**: 1 bot test · 1 tài khoản chủ bot (admin_id) · 1 tài khoản staff đã nhận lời mời vào bot đó · 1 nhóm quyền (role) **không tick** màn 通知設定. Với các case gửi thử / lưu URL–token: cần **phòng ChatWork + API token thật của QA** và môi trường ra được Internet tới `api.chatwork.com`.
- **Trạng thái ticket**: `Fix done - Đợi test`. Branch fix `ai_fixbug_39467` (gốc `release_step_20260805`, commit `29030c7d21`, 1 file) đã push.
- ⚠️ **Dev chưa chạy được kiểm chứng runtime** (MySQL dev `host.docker.internal:3306` refused) — chỉ mới `php -l`. Test thực tế của QA là lần verify runtime đầu tiên.
- ⚠️ Dev tự nêu rủi ro: staff đang mở màn mà bị thu hồi quyền sẽ thấy thao tác lưu ChatWork **im lặng, không có thông báo lỗi** (JS chỉ ẩn overlay ở nhánh fail) — hành vi này Dev **cố ý không sửa** để giữ fix tối giản.
- Ticket **không có** dữ liệu định danh ca lỗi cụ thể (bot_id / user_id / thời điểm) → bỏ section "Dữ liệu định danh ca lỗi".
- Journal duy nhất có nội dung điều tra là **Journal #133412 — AI LME Fix bug — 2026-08-28** (báo cáo Auto-fixbug). Nội dung đã chép **nguyên văn** vào `03-dev-impact.md`, không lặp lại ở đây.
