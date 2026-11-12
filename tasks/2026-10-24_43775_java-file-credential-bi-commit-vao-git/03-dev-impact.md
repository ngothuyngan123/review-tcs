# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket #43775 **không có section "Đánh giá ảnh hưởng" tách riêng** trong `description` (description chỉ là báo cáo audit ngắn: Tác động / Vị trí code / Cách sửa / Mức tin cậy). Toàn bộ nội dung 4 mục dưới đây được parse từ **3 journal Dev handoff** trên Redmine (`#146950` 22/10, `#147096` 22/10, `#147481` 23/10 — journal sau supersede journal trước) + field `dev_impact` / `requirements` từ MCP LME TEST STUDIO (task #506). Nội dung giữ nguyên văn khi trích dẫn, có đánh dấu nguồn từng đoạn.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (Redmine `Assignee` để trống; tác giả journal là `Dev Studio`) |
| Commit / Pull Request | `linect-service@8db0b92a19cf6eadabd39de401e7b00e8d61e5f7` (round 2, mới nhất — fix bug con #44011); round 1: `linect-service@c65fd8c358cd3a8f9a071c8e6cc92a6b975fcc14`. Không có link PR, chỉ có commit hash trong journal. |
| Branch | `ai_studio_fixbug_43775` (nhánh gốc `release-t09-2026` @ `be6ef546aedb`) |
| Ngày submit đánh giá | `2026-10-23` (journal #147481, round 2 — mới nhất) |
| Auto-filled | `2026-10-24 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại 3 journal Redmine (#146950/#147096/#147481) và xác nhận đầy đủ 4 mục dưới đây không sót impact.

---

## 1. Nguyên nhân

**Round 1 (journal #146950, #147096 — 22/10):**
> FirebaseMessagingModel viết thẳng JSON service account Firebase Admin (có private key) vào hằng `jsonCredentials`, và `init()` đọc key từ chuỗi này. File nằm trong git (từ 2024-08-29) nên ai đọc được repo đều có private key với toàn quyền trên project Firebase `snsline-lme`. Cùng file có hằng `FIREBASE_API_KEY` (server key FCM legacy), chỉ được 3 hàm không còn caller dùng tới.

**Round 2 — nguyên nhân bug con #44011 (journal #147481 — 23/10):**
> Ở bản đã giao (round 1), `FirebaseMessagingModel.init()` chỉ bắt `IOException` khi đọc file key. Khi file rỗng, chỉ có khoảng trắng hoặc là mảng JSON, thư viện Google ném `IllegalArgumentException` nên lỗi đi qua khối catch: không có log đường dẫn và không báo Chatwork. Job vẫn dừng và ghi `STOPPED` đúng như mong muốn, chỉ thiếu cảnh báo (bug #44011).

## 2. Cách fix

**Nội dung thay đổi (round 2 — bản cuối cùng, journal #147481):**
- Job (khởi động): key Firebase Admin đọc từ file ngoài repo; thêm khoá cấu hình `FIREBASE_CREDENTIALS_FILE`, mặc định `snsline-lme-firebase-adminsdk-jpi8r-1982b7d90a.json`, đường dẫn tương đối tính theo thư mục chạy job.
- Job (khởi động): file thiếu, rỗng, chỉ có khoảng trắng, JSON hỏng hoặc sai dạng ⇒ log đường dẫn tuyệt đối và báo Chatwork `[To:6395420]`, job dừng khởi động. **Vòng 2 bổ sung** các case rỗng, khoảng trắng và không phải object (#44011, commit `8db0b92a19cf`: `init()` bắt thêm `RuntimeException`).
- Xoá server key FCM legacy (`FIREBASE_API_KEY`) cùng 3 hàm gửi push cũ không còn nơi gọi (`sentNotify`/`sentUpdateBadge`/`sendNotifications` — tên cũ, đã bị thay bởi `sentNotifyv2`/`sentUpdateBadgeV2*`); chức năng đang chạy không đổi.
- `.gitignore` bỏ qua file `*firebase-adminsdk*.json`.

File đã sửa (java-job, round 2):
```
.gitignore                                         |   2 +
src/main/java/sns/line/ConfigFile.java             |   4 +
.../sns/line/models/FirebaseMessagingModel.java    | 142 ++-------------------
3 files changed, 20 insertions(+), 128 deletions(-)
```

⚠️ `task_get_context.spec_delta` ghi `diffAvailable=false` — `git diff` không chạy được trên môi trường Studio (`không tìm thấy ref "origin/release-t09-2026"`). Dev impact bên dưới lấy từ journal + field `dev_impact` tự kê của Studio, **không** từ diff thật.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Gộp từ journal (mục "Nội dung thay đổi" / "Ảnh hưởng") + field dev_impact của MCP Studio task #506. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AppMain.run` → `FirebaseMessagingModel.init()` | Đổi nguồn đọc key: hằng code → file ngoài repo; bắt thêm `RuntimeException` (round 2) | Khởi động job — `init()` chạy sau `JobControlTask.checkStart` |
| 2 | `sentNotifyv2`, `sentNotifyV2ByToken`, `sentUpdateBadgeV2`, `sentUpdateBadgeV2ByUser` | Không đổi logic, chỉ đổi nguồn credentials | Push app mobile dùng chung `init()` |
| 3 | `HandleMobileNotifyRealtimeTask`, `ActionLaterService`, `GroupActionLaterService`, `HandlePushMessageNotifyService`, `NotifyMaintainScannerTask`, `HandleCheckNumberOfMessagesSentCurrent` | Không đổi logic | Các job gọi push (realtime / theo lịch / nhắc bảo trì / cảnh báo số tin) dùng chung credentials |
| 4 | `HandleSubscribeTopic`, `TokenSubscribeTopicRecoveryTask`, `getListTopic` (qua `getAccessToken`) | Không đổi logic | Subscribe/unsubscribe topic dùng chung credentials |
| 5 | `sentNotify`, `sentUpdateBadge`, `sendNotifications` (hàm cũ) + hằng `FIREBASE_API_KEY` | **XOÁ** | Dev đã grep xác nhận không còn caller ngoài nội bộ (server key FCM legacy) |
| 6 | `ConfigFile` | **THÊM** khoá `FIREBASE_CREDENTIALS_FILE` | Đọc đường dẫn file key (mặc định / tương đối / tuyệt đối / rỗng) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FirebaseMessagingModel.init()` | `FirebaseMessagingModel.java` | Direct | Đổi nguồn đọc key từ hằng sang file; vòng 2 bắt thêm `RuntimeException` |
| F2 | `AppMain.run` / `JobControlTask.checkStart` | — | Indirect | `init()` chạy sau check-start; lỗi file ⇒ toàn bộ task của job không chạy, `job_status` → `STOPPED` qua shutdown hook có sẵn (logic giữ nguyên) |
| F3 | `sentNotifyv2`, `sentNotifyV2ByToken`, `sentUpdateBadgeV2`, `sentUpdateBadgeV2ByUser` | — | Indirect | Dùng chung credentials khởi tạo trong `init()` |
| F4 | `HandleMobileNotifyRealtimeTask`, `ActionLaterService`, `GroupActionLaterService`, `HandlePushMessageNotifyService`, `NotifyMaintainScannerTask`, `HandleCheckNumberOfMessagesSentCurrent` | — | Indirect | Push app mobile (tin mới, badge, giới hạn số tin, nhắc bảo trì) |
| F5 | `HandleSubscribeTopic`, `TokenSubscribeTopicRecoveryTask`, `getListTopic`/`getAccessToken` | — | Indirect | Subscribe/unsubscribe topic |
| F6 | `sentNotify`, `sentUpdateBadge`, `sendNotifications` + `FIREBASE_API_KEY` | `FirebaseMessagingModel.java` | Direct (DELETE) | Server key FCM legacy — đã grep xác nhận không còn caller |
| F7 | `ConfigFile` (khoá `FIREBASE_CREDENTIALS_FILE`) | `ConfigFile.java` | Direct | Mặc định / tương đối (theo thư mục chạy job) / tuyệt đối / rỗng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `.gitignore` | UPDATE | Bỏ qua mọi file `*firebase-adminsdk*.json` (gốc repo + thư mục con) |
| D2 | File JSON service account Firebase Admin **trên từng server job** (ngoài repo, vận hành — không phải DB) | CREATE (ops) | Tên mặc định `snsline-lme-firebase-adminsdk-jpi8r-1982b7d90a.json` cạnh jar, HOẶC khai báo `FIREBASE_CREDENTIALS_FILE` tuyệt đối trong `config.properties`; chmod 600 |
| D3 | `job_status` (DB, bảng điều khiển job) | UPDATE | Chuyển `STOPPED` khi `init()` lỗi — qua shutdown hook có sẵn, hành vi giữ nguyên so với trước fix |
| D4 | Log job + Chatwork `[To:6395420]` | CREATE (nội dung cảnh báo) | **Bắt buộc** chỉ chứa đường dẫn tuyệt đối tới file key, **KHÔNG** chứa nội dung key (REQ-005) |
| D5 | Mã nguồn — chuỗi `jsonCredentials` (JSON key viết thẳng) + hằng `FIREBASE_API_KEY` | DELETE (khỏi working tree) | Chưa xoá khỏi **lịch sử git** — việc rotate key + rewrite history là theo dõi riêng (ops), ngoài phạm vi code review |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Khởi động job nền `linect-service` (toàn bộ job, mọi server) | F1, F2, D3, D4 | **High** — 1 server job thiếu/sai file key ⇒ toàn bộ task của job đó không chạy, lặp lại mỗi chu kỳ crontab |
| T2 | Push thông báo app mobile qua Firebase (tin mới, badge, giới hạn số tin, nhắc bảo trì) | F3, F4 | **High** — lỗi khởi tạo credentials chặn toàn bộ push, không riêng 1 loại tin |
| T3 | Subscribe/Unsubscribe topic push app mobile | F5 | **Medium** — cùng credentials, chỉ lộ khi key lỗi |
| T4 | Bảo mật — log/Chatwork khi lỗi khởi động không được lộ nội dung key | D4, D5 | **High** — yêu cầu bắt buộc theo `REQ-005` (Studio), lỗi ở đây = lộ private key lần 2 ngay trong cơ chế cảnh báo |
| T5 | Vận hành deploy (ops đặt file key lên server trước khi deploy) | D2 | **High** — quy trình ngoài code, rủi ro job dừng toàn bộ nếu quên đặt file; không tự rollback |
| T6 | *(Ngoài phạm vi task, chỉ để Leader theo dõi)* Module callback (`release-callback-t09-2026`) + 4 file credential `php-web` vẫn dùng/chứa key viết thẳng y hệt, CHƯA sửa | Ghi nhận ở journal #147096/#147481 (follow-up) | **Medium** — chưa fix, nhưng Dev đã chốt không nằm trong scope #43775; Leader không nên kỳ vọng TC #43775 cover 2 phần này |

---

## Bug con phát sinh khi Studio test (task #506, round 2) — cần Leader quyết định

| Ticket | Trạng thái Dev đề xuất | Lý do |
|---|---|---|
| `#44009` | Reject (không do ticket này) | `makeJar` lỗi vì thiếu `converter-jackson`; lỗi có sẵn từ base (commit `56010ac65`, 2024-11-20), nhánh fix không đụng `build.gradle` |
| `#44010` | Reject + update expected của testcase Studio `32074` | `bots.count_app_notify` đã ngừng ghi có chủ ý từ `#38562` (badge chuyển sang tính theo user) — không phải lỗi |
| `#44011` | Đã fix (commit `8db0b92a19cf`) | `init()` thiếu bắt `RuntimeException` khi file key rỗng/khoảng trắng/mảng JSON |

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Quyết định scope: #44009 / #44010 reject theo đề xuất Dev? #44010 có cần cập nhật testcase `32074` không?
- [ ] Xác nhận phạm vi task CHỈ gồm `java-job`, KHÔNG gồm `php-web` (4 file) và module `callback` — để tránh review/viết TC vượt phạm vi
