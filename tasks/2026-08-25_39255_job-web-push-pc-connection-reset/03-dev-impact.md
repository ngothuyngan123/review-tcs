# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` (người submit đánh giá) · assigned_to Redmine hiện tại = `Hạnh Nguyễn` |
| Commit / Pull Request | `fc43f54c86bed5e8520a1573bb638524deac8b4f` |
| Branch | `m_202607_webpushpc_connnection-reset_39255` |
| Ngày submit đánh giá | `2026-08-01` (journal #127804, 04:38 UTC) |
| Auto-filled | `2026-08-25 by /new-task` |

> Nguồn: Redmine #39255 — journal #127804 (Thanh Duy Nguyen, 2026-08-01T04:38:23Z). Description của issue chỉ chứa stack trace, đánh giá ảnh hưởng nằm ở note.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine journal #127804. -->

- Web push PC dùng `pushService.send()` (web-push 5.1.1) tạo mới `CloseableHttpAsyncClient` (IOReactor + TLS handshake, pool rỗng) cho TỪNG notification; 10 thread webpush bắn liên tục → FCM reset connection → `java.io.IOException: Connection reset by peer` (`WebPushNotificationService.java:49` → `PushService.send:64`).

## 2. Cách fix

<!-- Nguyên văn từ Redmine journal #127804. -->

- Thay tầng transport bằng 1 `CloseableHttpClient` dùng chung có connection pool: dùng `pushService.preparePost()` giữ nguyên encrypt ECDH + ký VAPID JWT, rồi execute qua client pool.
- Config pool: `maxTotal 100` / `perRoute 50`, connect+socket timeout, `validateAfterInactivity`, `evictIdle 30s`, retry 2 lần; đọc hết body (`EntityUtils.consume`) để trả connection về pool.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục 3 Redmine, chuyển sang bảng template. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `WebPushNotificationService.sendPushNotifyPC` | Giữ nguyên signature | Đổi nội bộ tầng transport, caller không phải sửa |
| 2 | `WebPushNotificationService.init` | Giữ nguyên signature (thêm khởi tạo httpClient dùng chung bên trong) | Caller `AppMain:201` không bị ảnh hưởng |
| 3 | `LineModel.webPushPc` (`LineModel.java:297`) | Không đổi | Caller duy nhất của `sendPushNotifyPC`, đã check — không bị ảnh hưởng |
| 4 | `AppMain:201` | Không đổi | Nơi gọi `init()`, đã check — không bị ảnh hưởng |

> Dev kết luận: **scope local trong `WebPushNotificationService`**.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục 4.1 Redmine. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `WebPushNotificationService.init` | `WebPushNotificationService.java` | Direct | Thêm khởi tạo `httpClient` dùng chung |
| F2 | `WebPushNotificationService.buildHttpClient` | `WebPushNotificationService.java` | Direct (function **mới**) | Tạo pool + retry + evict idle |
| F3 | `WebPushNotificationService.sendPushNotifyPC` | `WebPushNotificationService.java:49` | Direct | Đổi từ `pushService.send` sang `preparePost` + `httpClient.execute`, consume body |
| F4 | `LineModel.webPushPc` | `LineModel.java:297` | Indirect (caller — Dev khẳng định không đổi) | Đường gọi duy nhất tới F3 |
| F5 | `HandleWebpushTask.actionPushPc` / `.run` | `HandleWebpushTask.java:58 / :39` | Indirect (theo stack trace) | Entry point job 10 thread — Dev **không liệt kê** ở mục 4.1, tester lưu ý khi review coverage |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2 Redmine. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Chỉ thêm hằng số tuning pool/timeout/retry in-code. **Không** đụng `config.properties` / DB / schema. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 Redmine. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Web push notify PC** — bắn nhiều push liên tục (10 thread webpush) không còn lỗi Connection reset, `statusCode 201` = success | F1, F2, F3 | High |
| T2 | **Notify PC luồng `LineModel.webPushPc` / `HandleWebpushTask`** — verify retry khi FCM lỗi tạm thời và connection được trả về pool (không leak/treo) | F3, F4, F5 | High |
| T3 | **Regression VAPID** — `preparePost` thay `send` → verify browser (Chrome PC) vẫn nhận đúng push, key ký hợp lệ | F3 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Ghi chú của `/new-task` (không phải nội dung Dev)

- Redmine journal có thêm **mục 5** (Commit / Branch) ngoài 4 mục chuẩn → đã map vào bảng "Thông tin" ở đầu file.
- Dev **không nêu** hành vi xử lý subscription hỏng (unsubscribe / gone / invalid signature) trong mục 4.2, nhưng Studio task #46 có `REQ-005` khẳng định có ghi trạng thái "ngừng nhận" + lưu nội dung lỗi vào bản ghi đăng ký. → **mâu thuẫn tiềm tàng với "4.2 Không có data update"**, Leader cần hỏi lại Dev.
- Studio task #46 còn ghi nhận 3 điểm Dev chưa xác nhận (`REQ-006` phạm vi retry chỉ ở tầng kết nối · `REQ-008` retry có thể gây push trùng · `CONFLICT-01/02/03`) — xem `04-tc-list.md`.
