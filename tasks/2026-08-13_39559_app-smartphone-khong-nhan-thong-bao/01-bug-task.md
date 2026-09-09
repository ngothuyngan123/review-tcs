# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #39559 bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39559 — [11-08-2026][T11862][Notify Setting] Khách báo ứng dụng smartphone không nhận được thông báo từ khoảng 3-4/8 dù đã cài lại app và xóa cache, trong khi PC vẫn nhận bình thường.` |
| Redmine URL | https://redmine.watermelon.vn/issues/39559 |
| Auto-filled | `2026-08-13 by /new-task` |
| Ngày báo cáo | `2026-08-11` (Redmine `created_on` = 2026-08-11T03:54:08Z) |
| Khách hàng / PM báo | `AI bug detect Lme` (Redmine `author`) — end user thật: `rintaro@ssks.work`, bot `RIASTAR｜デリカD:5専門中古車店` (bot_id `170162`, theo journal của Ngọc Ánh) |
| Module / Màn hình | `Notify Setting` (Redmine `category`) — màn 通知設定 (Cài đặt thông báo) |
| Priority | `Medium` (Redmine `priority` = Normal → map Medium) |
| Môi trường phát hiện | `Production (step.lme.jp)` — **suy ra**, không ghi tường minh trong description: bug do khách thật báo qua form CS + journal QA ghi "Thao tác tái hiện bug trên **step**". ⚠️ Tester confirm lại |

### Trạng thái Redmine (thời điểm fetch)

| Trường | Giá trị |
|---|---|
| Status | `Fix done - Đợi test` |
| Tracker | `Bug KH` · Project `Lme` |
| Assigned to | `Ngô Thúy Ngần` |
| Commit Date (custom field) | `2026-08-13` |
| Updated on | `2026-08-13T11:21:51Z` |
| Journals | 6 (trong đó **3 báo cáo AI AUTO-FIXBUG** — xem cảnh báo ở `03-dev-impact.md`) |
| Attachments / Relations | **0 attachment · 0 relation** |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #39559. KHÔNG diễn giải lại. -->

```
User: rintaro@ssks.work
Bot Name: RIASTAR｜デリカD:5専門中古車店

Tôi gặp khó khăn vì không nhận được thông báo trên ứng dụng điện thoại thông minh.
Trên PC vẫn nhận được thông báo.
Tôi đã kiểm tra qua cài đặt thông báo trên điện thoại, cài lại ứng dụng, xóa toàn bộ dữ liệu ＆ bộ nhớ cache nhưng vẫn không được.
Có vẻ từ khoảng ngày 3 hoặc 4 tháng 8 thì thông báo không còn đến nữa.

Chức năng: Cài đặt thông báo (通知設定)
Thời điểm phản hồi: 2026/08/11 12:41:51

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11862

Nguồn: OEM đã tạo ticket trên Slack — 管理番号 TY-11862
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BQ6V3PXFA
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1786420325773479

---

h3. 内容 từ Slack (OEM)
<pre>
【操作方法に関するお問い合わせフォーム】
スマートフォンアプリで、通知が来なくて困っています。
PCには通知は来ます。
スマホ本体の通知設定等はひと通り確認し、再インストール、データ＆キャッシュ全削除も試しました。
8月3日か4日あたりから通知が来なくなったようです。
</pre>

<!-- TaskRef: cs_form:T11862 oem_slack -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> ⚠️ **Description Redmine KHÔNG có Section "Tái hiện bug".** Các bước dưới đây lấy **nguyên văn từ journal của QA `Đoàn Thị Bích Hảo`** (2026-08-13T09:17:59Z), không phải từ description. Giữ nguyên cả lỗi typo của nguồn.

```
Thao tác tái hiện bug trên step:
1. Đăng nahjap account trên ios + android
2. Bật on cho kênh app và chọn timing = realtime
3. Tạo sự kiện sinh thông báo (nhắn tin, chặn/gỡ chặn,...)
4. Quan sát hiển thị

=> Ió nhận được còn android không nhận được thông báo
```

Diễn giải để dựng env (tester confirm):

1. Đăng nhập cùng account trên **cả app iOS và app Android** (trên `step` = production).
2. Màn 通知設定: bật **kênh app điện thoại (スマートフォンアプリ)**, chọn tần suất nhận = **realtime**.
3. Tạo sự kiện sinh thông báo (nhắn tin từ friend LINE, chặn/gỡ chặn, ...).
4. Quan sát thông báo trên từng thiết bị.

## Expected result

- App điện thoại (cả iOS và Android) **nhận được thông báo đẩy** khi có sự kiện, giống như PC. (Theo mô tả KH: "Trên PC vẫn nhận được thông báo" → kênh app phải nhận tương đương.)

## Actual result

- **Từ khách hàng (description)**: app điện thoại **không nhận được thông báo** từ khoảng **03–04/08/2026**, dù đã kiểm tra cài đặt thông báo trên máy, cài lại app, xoá toàn bộ dữ liệu + cache. **PC vẫn nhận bình thường.**
- **Từ journal QA khi tái hiện trên `step`**: `=> Ió [iOS] nhận được còn android không nhận được thông báo`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #39559 có **0 attachment**. Bằng chứng nằm ở dạng **log/query trên production do Dev dẫn trong đánh giá ảnh hưởng** (xem `03-dev-impact.md` mục 1: bản ghi `user_firebase_token` id 237937 đổi chủ 8 lần trong 45 phút; 2.958/3.071 ca lỗi) và **dashboard ngoài**:
> - Dashboard CS: https://dashboard.melonglobal.net/css-analytics/?id=T11862
> - Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=39559

## Ghi chú thêm của Leader

- **Bug tái hiện được** — QA đã tái hiện trên `step` (journal 2026-08-13T09:17:59Z). Khác với case "không tái hiện được": ở đây có cả log production của Dev **và** thao tác tái hiện của QA.
- ⚠️ **Ticket này đã qua 3 vòng AI Auto-fixbug** (journal 2026-08-13 03:39 → 06:40 → 11:21). Vòng sau **rollback/ghi đè** cách fix của vòng trước. `03-dev-impact.md` chỉ lấy **journal mới nhất (11:21:51Z, commit `3233088f19`)** — 2 vòng trước đã bị superseded, xem §Lịch sử vòng fix trong file 03.
- ⚠️ **Bug có nguyên nhân kép, phần app KHÔNG được fix ở ticket này**:
  - Nguyên nhân 1 (~96% ca, 2.958/3.071): `device_id` trùng do app Android gửi **build ID của ROM** → fix ở phía web (ticket này).
  - Nguyên nhân 2 (19 máy, chủ yếu **iOS**): app **không bao giờ gọi API cập nhật token** → **nằm ở phía app, không sửa được ở web**. Đây là **phần còn lại của ticket** sau khi web đã đúng.
  - → Triệu chứng của chính khách `rintaro@ssks.work` thuộc nhóm nào **chưa được xác định trong ticket**. Journal QA lại ghi iOS nhận được / Android không nhận — **ngược chiều** với phân bố nguyên nhân 2 (nhóm không gọi API chủ yếu là iOS). **Cần hỏi Dev/QA trước khi kết luận đã đóng bug của khách.**
- ⚠️ **2 ticket liên quan sinh ra trong quá trình fix** (Dev dẫn trong journal, `relations` Redmine để trống nên không tự link được):
  - **#39635** — token mới bị xoá mất, bản còn lại giữ token cũ (đã fix ở vòng bổ sung; TC `NEW-6` trên Studio gắn ticket này).
  - **#39636** — API lấy token vẫn trả token + số badge chưa xem của **NGƯỜI KHÁC** (lỗi rò rỉ dữ liệu chéo tài khoản).
- ⚠️ **Rủi ro vận hành Dev tự nêu, cố ý KHÔNG fix**: lệnh `recover:user_firebase_token` (chạy tay) vẫn còn lỗi cùng họ — sau fix này sẽ **xoá bản ghi của người vừa đăng nhập**. Dev đề nghị PM/leader quyết: ngừng dùng hoặc mở ticket riêng.
- Bộ TC ở `04-tc-list.md` **KHÔNG do member viết** — fetch từ MCP LME TEST STUDIO (task 67, 45 TC do AI sinh, `aiResult=fail`, 3 TC fail chưa raise ticket). Đọc §Cảnh báo trong file 04 trước khi review.
