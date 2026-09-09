# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39255 — [JOB] Web push notification PC bị lỗi java.io.IOException: Connection reset by peer` |
| Reviewer (Leader) | `<điền tên>` |
| Tester được review | Viết TC: **AI** (25/29) + **hanhntb** (4/29) · Chạy TC: **hanhntb** (29/29) |
| Ngày review | `2026-08-25` |
| Version TCs | Studio round 1 · `status = draft` toàn bộ 29 TC |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #46** (nguồn 1 — mặc định) |
| Ticket · task_id · round · branch | `39255` · `#46` · round `1` · `m_202607_webpushpc_connnection-reset_39255` |
| Thời điểm fetch | `2026-08-25` |
| Tổng số TC review | **29** |
| File 04 trong repo vs Studio | **Khớp** (29 vs 29) — `04-tc-list.md` được sinh từ chính lần fetch này bằng `scripts/parse_studio_tcs.py`. Không có STALE-INPUT. |
| Trạng thái Studio | `status = done-ai` · `aiResult = pass` · `reviewState = tester` · `reviewed = false` · `openBugs = 0` · `submittedWithoutMcp = false` |
| Comment vòng review trước | `review_list_comments(task_id=46)` → **rỗng** (chưa có vòng review nào) |

**Cảnh báo bắt buộc từ metadata Studio**

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **20/29 pass (69%)** · 9 `skip` · 0 `fail` · 0 `error` | **[MAJOR]** — dưới ngưỡng 80% |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có TC nào fail/error**; `bug_tickets` rỗng ở cả 29 TC | OK |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | `last_exec.env = prd` ở **cả 29 TC**, nhưng **mâu thuẫn với nội dung TC**: 19/29 khai `env_tag = local-only`, và precondition của 20 TC ghi rõ dùng **máy chủ giả lập (stub)**. TC duy nhất bắn vào **FCM thật** (NEW-11) đang `skip`. | **[BLOCKER]** — xem §4.1 B-1 |
| 4 | Ai chạy (`last_exec.source` / `by`) | 29/29 `source = manual`, `by = hanhntb` — **QA người chạy**, không phải AI pipeline tự chạy | OK (điểm tốt) |
| 5 | Tác giả TC (`author` / `provenance.source`) | **25/29 (86%) do AI sinh** (`provenance.source = ai`), 4/29 do `hanhntb` viết. `reviewState = tester`, `reviewed = false` | **[MAJOR]** — ≥50% AI sinh mà chưa qua review người |
| 6 | Mã quan điểm Studio KHÔNG có trong `checklist-lme.md` | **3 mã / 13 lượt TC**: `TOOL-ERRHYG-001` (7 TC) · `TOOL-NEGCTRL-001` (2 TC) · **trống** (4 TC: NEW-26/27/28/29) | **[MAJOR]** — 45% bộ TC không map được vào lưới quan điểm LME |

> ⚠️ Nội dung Studio có `contentTrust = untrusted` → đã xử lý như **data**. TC Studio là **read-only**: mọi đề xuất sửa ở report này phải thực hiện qua `testcase_update` trên Studio, không sửa trong repo.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần xử lý và review lại

**Lý do ngắn gọn**: Bộ TC được thiết kế tốt và bám sát diff ở mức hiếm thấy (techNote trích đúng hằng số, đúng `nonRetriableClasses`, đúng dòng code), nhưng **toàn bộ 20 TC Đạt đều chạy với máy chủ giả lập** — TC duy nhất tái kiểm lỗi gốc trên endpoint FCM thật (NEW-11) bị `skip`. Đồng thời **3 TC tự ghi "cần Dev/PO quyết định, chưa chốt expected" nhưng vẫn bị đánh Đạt**, trong đó NEW-18 đã đo và tái hiện được **rủi ro mới do chính bản fix sinh ra** (admin nhận thông báo trùng). Ticket đã Closed 2026-08-21 với 3 xung đột spec chưa chốt.

---

## 2. Tóm tắt cho member

Bộ TC này chất lượng cao hơn mặt bằng chung rõ rệt: 5 nhánh lỗi của cơ chế retry được tách bạch đúng (đứt kết nối / 503 / timeout đọc / DNS / chạm trần pool), có **đối chứng âm** (NEW-19, NEW-22) — thứ rất ít bộ TC nào làm, và NEW-10 đo đúng chỉ số quyết định là *số kết nối TCP thực mở* chứ không chỉ đếm request thành công.

Điểm phải fix nằm ở khâu **kết luận**, không phải khâu thiết kế: (1) TC lõi NEW-11 — bắn thật vào FCM — bị bỏ chạy, nên chưa có bằng chứng nào chứng minh lỗi gốc của ticket đã hết; (2) ba TC mang cờ `CONFLICT-01/02/03` tự viết rõ "không tự đánh Đạt/Không đạt, cần Dev/PO quyết định" nhưng đã bị đánh Đạt và đóng ticket; (3) 20 TC Đạt mà cột `Evidence thực tế` trống hoàn toàn — vi phạm RULE-02, kết quả chưa được nghiệm thu. Xử lý 3 điểm này là bộ TC đủ tiêu chuẩn approve.

---

## 3. Coverage Matrix

> Cột `Exec` = số TC **thực sự `pass`** / tổng TC map. TC `skip` **không** được tính là đã test.

| Impact | Loại | Priority | TCs map | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — tạo mới `CloseableHttpAsyncClient` mỗi push → FCM reset connection khi 10 thread bắn liên tục | Fix | — | NEW-11 (skip) · NEW-10 · NEW-12 | 3 | **2/3** | **RISK** — TC duy nhất chạm FCM thật đang `skip`; 2 TC pass đều dùng stub (chính techNote NEW-10 thừa nhận "chạy với stub nên KHÔNG tái hiện được reset thật của FCM") |
| **F1** — `WebPushNotificationService.init` | Function | Direct | NEW-1 (skip) · NEW-2 (skip) · NEW-7 (skip) · NEW-17 | 4 | **1/4** | **RISK** — 3/4 là kiểm tra tĩnh bị đánh `skip` |
| **F2** — `WebPushNotificationService.buildHttpClient` (mới) | Function | Direct | NEW-2 (skip) · NEW-8 (skip) · NEW-12 · NEW-20 | 4 | **2/4** | **OK** — có Normal (NEW-12) + Boundary (NEW-20) đã chạy |
| **F3** — `WebPushNotificationService.sendPushNotifyPC` | Function | Direct | NEW-3 (skip) · NEW-4 (skip) · NEW-9 · NEW-10 · NEW-13 · NEW-14 · NEW-15 · NEW-16 · NEW-18 | 9 | **7/9** | **OK** — phủ đủ Normal / Abnormal / Boundary |
| **F4** — `LineModel.webPushPc` (caller) | Function | Indirect | NEW-16 · NEW-21 · NEW-22 · NEW-23 · NEW-25 | 5 | **5/5** | **OK** |
| **F5** — `HandleWebpushTask.actionPushPc` / `.run` | Function | Indirect (Dev **không liệt kê** ở 4.1) | NEW-9 · NEW-10 · NEW-19 | 3 | **3/3** | **OK** — nhưng impact này thiếu trong file 03, xem §4.2 M-7 |
| **D — Dev khai "Không có data bị update"** | Data | — | NEW-21 · NEW-22 · NEW-23 | 3 | **3/3** | **RISK** — TC chứng minh **có** update `push_subscriptions.status` + `message_error` → mâu thuẫn mục 4.2 file 03, xem §4.2 M-6 |
| **T1** — Web push notify PC: bắn nhiều liên tục (10 thread) không còn Connection reset, statusCode 201 | Feature | High | NEW-10 · NEW-11 (skip) · NEW-20 | 3 | **2/3** | **RISK** — chỉ verify được trên stub |
| **T2** — Notify PC luồng `webPushPc` / `HandleWebpushTask`: retry khi FCM lỗi tạm thời + connection trả về pool, không leak/treo | Feature | High | NEW-4 (skip) · NEW-12 · NEW-13 · NEW-14 · NEW-15 · NEW-16 · NEW-18 · NEW-20 | 8 | **7/8** | **OK** |
| **T3** — Regression VAPID: `preparePost` thay `send`, browser Chrome PC vẫn nhận đúng push, key ký hợp lệ | Feature | High | NEW-3 (skip) · NEW-24 · NEW-25 · NEW-26 · NEW-28 | 5 | **4/5** | **OK** — NEW-24/25 chạy trên Chrome thật với khoá VAPID thật (thoả RULE-06 output cuối chuỗi) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| NEW-27 (`TC-NOVP-03`) | Tắt rồi bật lại 「Thông báo PC」 trên hệ thống | Test luồng **đăng ký / huỷ đăng ký subscription ở tầng UI + service worker** — tầng này **không bị chạm** bởi commit `fc43f54c` (diff chỉ 1 file `WebPushNotificationService.java`). AP-5 layer-downstream over-coverage. | **Giữ lại**, re-label là `regression` ở `Ghi chú`, **không tính** vào coverage của bản fix |
| NEW-29 (`TC-NOVP-04`) | Block quyền Notification của Chrome rồi cấp lại quyền | Như trên — kiểm hành vi cấp quyền của Chrome, không đi qua code path đã sửa | **Giữ lại**, re-label `regression` |

> NEW-26 (2 PC / 2 Chrome profile) và NEW-28 (1 thiết bị mất quyền không kéo theo thiết bị còn lại) **KHÔNG phải orphan** — cả hai đi thẳng qua vòng lặp nhiều `push_subscriptions` dùng chung 1 pool, đúng vùng code đã sửa. Đây là 2 TC người viết có giá trị nhất trong nhóm 4 TC của `hanhntb`.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | Kết hợp 3 shape: (a) **"sửa hàm dùng chung"** (`WebPushNotificationService` — REG-SHARED-001); (b) **"performance / optimize"** (thay client-per-request bằng connection pool); (c) **"concurrent"** (10 thread dùng chung 1 pool). **KHÔNG** phải generic catch-all — retry dựa trên `DefaultHttpRequestRetryHandler` với danh sách `nonRetriableClasses` **đóng và đọc được**, nên áp nhánh *specific code check* của review-checklist §A.6. |
| **Trigger space cần cover** | 8 nhánh thất bại của tầng transport: (1) đứt kết nối tầng IO · (2) HTTP 5xx · (3) timeout đọc 15s · (4) DNS không phân giải · (5) chạm trần `perRoute` → chờ pool 5s · (6) **lỗi bắt tay TLS/SSL** · (7) **HTTP 429 rate limit từ FCM** · (8) **mã lỗi chưa biết trước** |
| **Số trigger TCs hiện cover** | **5/8** — (1) NEW-13 ✅ · (2) NEW-14 ✅ · (3) NEW-15 ✅ · (4) NEW-16 ✅ · (5) NEW-20 ✅ · **(6)(7)(8) thiếu** |
| **KH report dạng** | **Có root cause cụ thể** — description Redmine chứa stack trace đầy đủ (`WebPushNotificationService.java:49` → `PushService.send:64`), exception class rõ ràng. **AP-2 KHÔNG dính**, không cần cover root cause thay thế. |
| **Alternative root causes cần verify** | N/A |
| **Anti-patterns dính** | **AP-5** (nhẹ — NEW-27 / NEW-29, xem ORPHAN). **AP-1 không dính** (5 trigger > ngưỡng 3). **AP-2 không dính** (có root cause). **AP-3 không dính** (T1/T2/T3 đều có Abnormal + Boundary). **AP-4 không dính** — tuy mục "Commit / Pull Request" chỉ có hash `fc43f54c` không có link PR, nhưng techNote của 12 TC trích **đúng tên hằng số, đúng số dòng, đúng bytecode của `web-push-5.1.1.jar`** → fix shape đã thực sự được đọc, không phải suy đoán. **AP-6 không dính** (mục 3 file 03 có liệt kê 2 caller). |

**Câu hỏi adversarial còn treo** (TCs hiện tại không trả lời được):

1. `MAX_CONNECTION_PER_ROUTE = 50` áp cho **mỗi route**. FCM trả về nhiều endpoint host khác nhau (`fcm.googleapis.com`, `*.push.services.mozilla.com`, `*.notify.windows.com`). Với `MAX_CONNECTION_TOTAL = 100` và nhiều route đồng thời, **trần tổng 100 có bị chạm trước trần route không**? NEW-20 chỉ test **1 route duy nhất**.
2. Cơ chế retry 2 lần nhân với 10 thread → **tối đa 30 request đồng thời** tới FCM khi mạng chập chờn. Có vượt rate limit của FCM không? **Không TC nào tra spec FCM chính thức** (vi phạm RULE-05).
3. Fix bắt buộc **restart job** để `init()` chạy lại. `notification_pc` đang xử lý dở lúc restart thì sao? Không TC nào chạm (REG-RUN-001).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge / trước khi coi ticket là đã verify)

- **[BLOCKER] B-1 · NEW-11 (`TC-ENV003-01`) `skip` — lỗi gốc của ticket chưa từng được tái kiểm trên endpoint thật.**
  Đây là TC **duy nhất** bắn vào FCM thật; 20 TC Đạt còn lại đều trỏ vào máy chủ giả lập. techNote của NEW-10 tự thừa nhận: *"chạy với stub nên KHÔNG tái hiện được reset thật của FCM — phần đó do TC 'Gửi dồn dập tới địa chỉ nhận FCM thật' đảm nhiệm"*. Stub không tái hiện được TLS handshake + hành vi ngắt kết nối của hạ tầng Google, tức là **cơ chế gây ra chính lỗi `Connection reset by peer`** chưa được đụng tới. Bản thân expected của NEW-11 cũng đã cảnh báo đúng điều này. Vi phạm **RULE-08** + **ENV-003** (job nền + domain bên thứ 3 không được kết luận từ local/staging).
  → **Chạy NEW-11 trên môi trường có endpoint FCM thật**, kèm đối chứng bản chưa fix theo đúng expected đã viết. Nếu bản chưa fix cũng không tái hiện được lỗi thì **ghi rõ "chưa tái hiện được lỗi gốc"** vào kết quả, không được đóng ticket bằng lần chạy sạch trên stub.

- **[BLOCKER] B-2 · NEW-18 (`TC-CONC001-03`) bị đánh Đạt trong khi chính TC cấm tự kết luận — rủi ro MỚI do bản fix sinh ra chưa có ai quyết định.**
  Bản fix bật `DefaultHttpRequestRetryHandler(RETRY_COUNT, true)` — tham số thứ hai `requestSentRetryEnabled = true` cho phép gửi lại **cả request POST đã đi**. TC đã đo và **tái hiện được**: máy chủ nhận **trọn vẹn 2 request** cho cùng 1 thông báo → admin có thể thấy **2 thông báo giống hệt nhau**. Expected của TC ghi nguyên văn: *"⚠ ĐÂY LÀ ĐIỂM CẦN DEV/PO QUYẾT ĐỊNH, không tự đánh Đạt/Không đạt"*. Vậy mà `last_exec.status = pass` và ticket đã Closed 2026-08-21. Ticket #39255 **không hề nhắc** tới rủi ro này (note Studio: *"CONFLICT-02 — rủi ro MỚI do bản fix sinh ra, ticket không nhắc"*).
  → Đưa `REQ-008` ra cho **Dev + PO quyết định**: chấp nhận đánh đổi (thà trùng hơn mất) → đổi expected thành "Đạt kèm ghi chú, có bản ghi quyết định"; không chấp nhận → yêu cầu Dev đổi `requestSentRetryEnabled = false` và test lại. **Không được để trạng thái Đạt như hiện tại.**

- **[BLOCKER] B-3 · GAP `REG-RUN-001` (Cao): không TC nào verify `notification_pc` đang xử lý dở khi restart job để deploy bản fix.**
  Bản fix nằm trong `init()` — bắt buộc **restart job** mới có hiệu lực. Trigger của REG-RUN-001 là *"BẮT BUỘC với mọi release khi hệ thống có job/dữ liệu đang chạy dở"*. Job web push chạy 10 thread liên tục; lúc restart chắc chắn có bản ghi đang ở trạng thái xử lý dở. Không TC nào trả lời: bản ghi đó bị **treo vĩnh viễn ở trạng thái đang xử lý**, bị **gửi lại từ đầu** (admin nhận trùng — cộng hưởng với B-2), hay được xử lý đúng một lần.
  → Bổ sung `TC-REGRUN001-01/02/03` ở §5.

### 4.2 Major (nên fix)

- **[MAJOR] M-1 · 3 TC mang cờ `CONFLICT` được đánh Đạt mà `Trạng thái đánh giá spec` để trống ở cả 29 TC.**
  `spec_status = null` **toàn bộ 29 TC**. Trong khi đó NEW-14 note *"CONFLICT-01 — chưa chốt expected"*, NEW-15 note *"CONFLICT-03"*, NEW-18 note *"CONFLICT-02"*. Đây đúng là kịch bản mà cột này sinh ra để chặn: **tự suy diễn expected rồi cho Đạt**. Cụ thể NEW-14: FCM trả 503 (lỗi tạm thời) **không được retry** — hệ quả nghiệp vụ là thông báo mất luôn, không có lần thử lại nào; TC ghi Đạt vì "đúng như code đang làm", chứ chưa ai xác nhận đó là **kỳ vọng của ticket**.
  → Điền `spec_status` cho cả 29 TC (`Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`). Riêng NEW-14/15/18 phải là `Đã hỏi leader` kèm tên người chốt, hoặc trả về `Chưa test` cho tới khi có quyết định.

- **[MAJOR] M-2 · RULE-02: 20 TC đánh Đạt nhưng `Evidence thực tế` trống 29/29.**
  RULE-02 quy định *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng"*. Các TC này đều đòi bằng chứng đo được — số kết nối TCP thực mở (NEW-10), số request nhận trọn vẹn (NEW-18), thời gian thoát ~15s (NEW-15), trạng thái bản ghi đăng ký trước/sau (NEW-21/22) — nhưng **không TC nào lưu lại**. Theo §1 checklist-lme, vi phạm RULE → **kết quả test không được nghiệm thu**, dù quan điểm đã tick đủ.
  → Đính kèm log job + số liệu đo cho ít nhất nhóm TC quyết định: NEW-10, NEW-12, NEW-13, NEW-15, NEW-18, NEW-20, NEW-21.

- **[MAJOR] M-3 · 8 TC "(Kiểm tra kỹ thuật)" bị đánh `skip` dù techNote đã chứa kết luận đầy đủ.**
  NEW-1/2/3/4/5/6/7/8 là TC đọc code tĩnh, và techNote của chúng **đã có kết quả thật**: tên hằng số + giá trị (`MAX_CONNECTION_TOTAL=100`, `SOCKET_TIMEOUT=15000`, `EVICT_IDLE_SECOND=30`…), xác minh `preparePost` tồn tại trong bytecode `web-push-5.1.1.jar`, liệt kê đúng 2 caller `AppMain.java:201` + `LineModel.java:297`, đối chiếu commit `fc43f54c` = 1 file / 73 insertions / 14 deletions. Việc verify **đã làm rồi**, chỉ là kết quả không được ghi nhận — nên hệ thống đang báo 69% pass thay vì con số thật.
  → Đổi 8 TC này sang `Đạt` kèm evidence là link diff / số dòng, **hoặc** nếu thực sự chưa ai đọc lại diff thì giữ `skip` và nói rõ. Không để trạng thái nhập nhằng như hiện tại.

- **[MAJOR] M-4 · GAP `JOB-001` điểm (1) + RULE-05: không TC nào tra spec FCM/Web Push chính thức về rate limit.**
  JOB-001 yêu cầu *"tra tài liệu chính thức MỚI NHẤT của bên thứ 3 để lấy rate limit hiện hành"* rồi *"tạo dữ liệu request lớn và liên tục vượt ngưỡng"*. Sau fix, 10 thread × retry 2 lần = **tối đa 30 request đồng thời** tới FCM — cao hơn hẳn trước fix (mỗi request 1 client, tự giới hạn bởi TLS handshake). Không TC nào cover **HTTP 429** hay hành vi khi vượt quota.
  → Bổ sung `TC-JOB001-02/03` ở §5.

- **[MAJOR] M-5 · GAP trigger (6)(7)(8) của fix shape: lỗi bắt tay TLS · HTTP 429 · mã lỗi chưa biết.**
  5/8 nhánh thất bại đã cover, còn 3 nhánh trống. Đáng chú ý nhất là **lỗi bắt tay TLS** — đây chính là tầng mà lỗi gốc phát sinh (`SSLIOSession.receiveEncryptedData` trong stack trace) và là nhánh stub **không mô phỏng được**.
  → Cover trong `TC-ENV003-02/03` ở §5.

- **[MAJOR] M-6 · Mục 4.2 file `03-dev-impact.md` sai: Dev khai "Không có data bị update", nhưng TC chứng minh ngược lại.**
  NEW-21 / NEW-22 / NEW-23 (đều Đạt) verify `push_subscriptions.status` bị chuyển sang ngừng nhận và `message_error` được ghi nội dung lỗi — khớp `REQ-005` của Studio. Đây là **UPDATE có điều kiện `WHERE`**, tức là `DATA-DB-001` phải ◯ chứ không phải "không có data". Hệ quả: coverage matrix xây từ file 03 sẽ **không có dòng `D1`** nào, dễ bỏ lọt.
  → Yêu cầu Dev bổ sung `D1 — push_subscriptions.status / message_error · UPDATE` vào mục 4.2. *(May mắn là TC đã cover sẵn, kể cả kiểm `WHERE` 2 tài khoản qua NEW-22 — đây là điểm cộng của bộ TC.)*

- **[MAJOR] M-7 · Mục 4.1 file 03 thiếu `HandleWebpushTask` — entry point 10 thread.**
  Stack trace trong ticket đi qua `HandleWebpushTask.run:39` → `.actionPushPc:58`, và `numberThread = 10` được khai ở `HandleWebpushManager` (techNote NEW-8). Con số 10 thread là **tiền đề của cả bài toán pool** (`10 ≤ 50 ≤ 100`), nhưng Dev không liệt kê ở 4.1 nên không ai bị buộc phải kiểm khi con số này thay đổi.
  → Bổ sung `F5 — HandleWebpushTask` vào 4.1 và ghi rõ ràng buộc `numberThread ≤ MAX_CONNECTION_PER_ROUTE`.

- **[MAJOR] M-8 · RULE-01: 4 quan điểm ưu tiên Cao thiếu loại case, không TC nào ghi lý do.**

  | Quan điểm | Loại case hiện có | Thiếu | Ghi lý do? |
  |---|---|---|---|
  | `FUNC-001` (Cao) | Normal ×3 | Abnormal, Boundary | Không |
  | `JOB-001` (Cao) | Abnormal ×1 | Normal, Boundary | Không |
  | `MSG-004` (Cao) | Normal ×2 | Abnormal, Boundary | Không |
  | `DATA-DB-001` (Cao) | Abnormal ×1 | Normal, Boundary | Không |

  → Bổ sung TC hoặc ghi lý do miễn trừ vào `Ghi chú` (RULE-01 cho phép miễn nếu quan điểm không có khái niệm biên — nhưng **phải viết ra**).

- **[MAJOR] M-9 · 13/29 TC (45%) không map được vào lưới quan điểm LME.**
  `TOOL-ERRHYG-001` (7 TC) và `TOOL-NEGCTRL-001` (2 TC) là **mã nội bộ Studio**, không có trong `framework/checklist-lme.md`; 4 TC của `hanhntb` (NEW-26/27/28/29) **bỏ trống** cột mã quan điểm. Theo quy tắc review, các TC này không được tính là cover quan điểm nào → coverage theo lưới LME bị hụt 45% dù nội dung TC thực chất có giá trị.
  → Map lại sang mã có sẵn, gợi ý: `TOOL-ERRHYG-001` → `JOB-001` hoặc `ENV-001` (fail-safe khi lỗi hạ tầng); `TOOL-NEGCTRL-001` → `REG-SHARED-001` (đối chứng nhánh không bị chạm); NEW-26/28 → `CONC-001`; NEW-27/29 → `STATE-001`. Nếu team muốn giữ mã `TOOL-*` thì phải bổ sung vào `checklist-lme.md` theo **RULE-10**.

- **[MAJOR] M-10 · GAP `SEC-002` (Cao): fix làm tăng lượng nội dung ghi log nhưng không TC nào quét log tìm thông tin nhạy cảm.**
  Sau fix, nhánh lỗi đọc và **ghi toàn bộ response body** (`IOUtils.readLines(entity)` — techNote NEW-21), và log có `endpoint` của subscription. Endpoint FCM **chứa registration token** của trình duyệt. NEW-17 mới chỉ cover một phần rất hẹp (*"log lỗi không được in ra khoá bí mật VAPID"*). SEC-002 yêu cầu quét đủ danh mục: token, email, LINE user ID, API secret.
  → Bổ sung `TC-SEC002-01` ở §5.

- **[MAJOR] M-11 · GAP `PERF-LARGE-001`: quy mô test không lấy từ số liệu khách hàng lớn nhất thực tế.**
  Test dùng 200 thông báo / 100 lần gửi đồng thời — con số **tự chọn**, không TC nào ghi *"nguồn của giới hạn"* như FUNC-004 yêu cầu. Không ai biết một lượt job trên production thực sự xử lý bao nhiêu bản ghi `notification_pc`. Nếu thực tế là hàng chục nghìn, hành vi của pool ở quy mô đó chưa được biết.
  → Tra số liệu production rồi bổ sung `TC-PERFLARGE001-01` ở §5.

- **[MAJOR] M-12 · RULE-04: chưa có thống kê phạm vi ảnh hưởng của lỗi trước khi đóng ticket.**
  Đây là bug **tự detect từ log production** — nghĩa là đã có thông báo thật bị mất. RULE-04 yêu cầu *"trước khi đóng ticket phải có query/thống kê toàn hệ thống xác nhận phạm vi ảnh hưởng"*. Không có số liệu bao nhiêu `notification_pc` bị fail vì lỗi này, thuộc bao nhiêu bot, và có cần gửi bù hay không. Ticket đã Closed 2026-08-21.
  → Yêu cầu Dev/QA thống kê số bản ghi bị ảnh hưởng trong khoảng lỗi và chốt có gửi bù hay không.

- **[MAJOR] M-13 · `01-bug-task.md` và `03-dev-impact.md` chưa tick "Tester verify auto-fill chính xác".**
  Cả 2 file mang `Auto-filled: 2026-08-25 by /new-task` và checkbox verify vẫn trống. F/D/T trong file 03 có thể thiếu hoặc map sai — và thực tế **đã sai 2 chỗ** (M-6, M-7).
  → Tester đọc lại Redmine #39255 (đặc biệt journal #127804) rồi tick, trước khi coi coverage matrix ở §3 là có hiệu lực.

- **[MAJOR] M-14 · `REG-SHARED-001` (Cao): cả 2 TC đều `skip`, và chưa rà brand khác.**
  Dev **có** cung cấp danh sách nơi ảnh hưởng (mục 3 file 03 — 2 caller), đây là điểm tốt. Nhưng NEW-3 và NEW-6 — 2 TC verify danh sách đó — đều `skip`. Ngoài ra REG-SHARED-001 yêu cầu rà theo **brand (Lme / Lwaka / Saruwaka / Lgram)**: cần xác nhận `WebPushNotificationService` có được deploy chung cho các brand khác không, hay chỉ project job của Lme.
  → Chạy NEW-3 / NEW-6 (xem M-3) + trả lời câu hỏi brand.

### 4.3 Minor (có thể fix sau)

- **[MINOR] m-1 ·** `Mã quan điểm liên kết` trống ở NEW-26/27/28/29 → 4 TC nhận `TC No.` dạng `TC-NOVP-0x`, không đúng quy ước `TC-<mã quan điểm bỏ gạch>-<nn>`. Sửa cùng M-9.
- **[MINOR] m-2 ·** Không TC nào ghi **loại evidence bắt buộc** ở cột `Ghi chú` (RULE-02 phần khai báo). Hiện `Ghi chú` chỉ có trace Studio + techNote.
- **[MINOR] m-3 ·** `CONC-001` chỉ cover kịch bản 4 (batch đa luồng chạm giới hạn chung). Ba kịch bản còn lại (double-click, 2 tab cùng user, 2 user sửa 1 bản ghi) **không áp dụng** cho job nền không có UI — nhưng RULE-03 yêu cầu **ghi lý do khi bỏ**, hiện không TC nào ghi.
- **[MINOR] m-4 ·** NEW-27 steps bước 1 lỗi chính tả: `"ửi một notification"` → `"Gửi một notification"`.
- **[MINOR] m-5 ·** Tỷ lệ loại case 14 Normal / 10 Abnormal / 5 Boundary = **48 / 34 / 17**, Boundary thấp hơn khuyến nghị (40/35/25) — hợp lý với bản chất task nhưng nên bổ sung Boundary theo M-8.
- **[MINOR] m-6 ·** Nhãn `last_exec.env = prd` ở cả 29 TC **mâu thuẫn** với `env_tag = local-only` của 19 TC và với precondition ghi rõ dùng stub. Nhãn môi trường đang sai → mọi báo cáo tổng hợp theo env của Studio sẽ sai theo. Sửa qua `testcase_update` / `result_submit`.

### 4.4 Nit (gợi ý)

- **[NIT] n-1 ·** NEW-20 chỉ ép 100 lần gửi đồng thời về **1 route**. Đáng thêm biến thể **nhiều route** (FCM + Mozilla + Windows push) để chạm trần `MAX_CONNECTION_TOTAL = 100` thay vì trần `perRoute = 50` — hai trần này hỏng theo hai kiểu khác nhau.
- **[NIT] n-2 ·** Mục "Commit / Pull Request" file 03 chỉ có hash `fc43f54c...`, không có link PR. Có link thì Leader vòng sau đọc diff nhanh hơn (dù lần này techNote đã bù đắp tốt).
- **[NIT] n-3 ·** `DATA-AUDIT-001`: việc job tự chuyển `push_subscriptions` sang ngừng nhận hiện chỉ ghi log job, không có bản ghi lịch sử thao tác admin nhìn thấy được. Mức rủi ro thấp (không phải PII nhạy cảm), nêu để Leader cân nhắc.
- **[NIT] n-4 ·** Theo **RULE-10**, bug này lọt ra production → nên sinh 1 dòng quan điểm/catalog mới. Gợi ý: bổ sung vào Catalog D2 dòng *"job gọi API bên thứ 3 qua HTTPS — bắt buộc dùng client có connection pool dùng chung, không tạo client mới mỗi request"*.

---

## 5. TCs đề xuất bổ sung

> Copy thẳng vào Studio (`testcase_create`) hoặc `04-tc-list.md` ở round tiếp theo. `TC No.` đã tránh trùng với 29 TC hiện có.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENV003-02 | ENV-003 | Abnormal | Mất mạng giữa lúc job đang bắn hàng loạt tới FCM thật — bắt tay TLS lỗi, job không chết | Job bản đã fix chạy trên môi trường bắn được tới FCM thật, khoá VAPID thật. Có ≥ 2 đăng ký nhận thông báo PC THẬT tạo từ Chrome trên PC. | 1. Tạo 200 bản ghi thông báo PC ở trạng thái chờ xử lý<br>2. Chạy job<br>3. Khi log cho thấy job đã gửi được khoảng 50 bản ghi, ngắt kết nối mạng ra ngoài của máy chạy job trong 30 giây<br>4. Nối mạng trở lại, để job chạy hết<br>5. Rà toàn bộ log job và đếm số bản ghi ở từng trạng thái cuối | 200 thông báo PC. Ngắt mạng 30 giây tại thời điểm đã xử lý ~50/200. | Trong lúc mất mạng, log ghi lỗi bắt tay TLS / không phân giải được tên miền một cách rõ ràng, **không có luồng nào chết và không có luồng nào ngủ 60 giây**. Sau khi có mạng lại, job **tự gửi tiếp** các bản ghi còn lại và toàn bộ 200 bản ghi kết thúc ở trạng thái đã xử lý hoặc trạng thái lỗi có ghi lý do — **tổng số bản ghi vào = số thành công + số lỗi**, không bản ghi nào biến mất hoặc kẹt ở trạng thái đang xử lý. Không có kết nối chết nào còn nằm trong pool khiến đợt gửi sau lỗi theo. | Chưa test |  | PRD |  |  |  |  | Lấp **M-5** (trigger 6 — lỗi bắt tay TLS, nhánh stub không mô phỏng được) + hỗ trợ **B-1**. Cover `ENV-003` / `JOB-001` điểm (4). Evidence bắt buộc: **log job trọn vẹn cả 3 giai đoạn** + bảng đếm số bản ghi vào/ra. |
| TC-ENV003-03 | ENV-003 | Boundary | Đăng ký thật của 3 nhà cung cấp push khác nhau cùng lúc — chạm trần tổng 100 kết nối chứ không phải trần 50 mỗi route | Job bản đã fix. Có đăng ký nhận thông báo PC thật từ **3 trình duyệt khác nhau**: Chrome (endpoint FCM của Google), Firefox (endpoint Mozilla), Edge (endpoint Windows). | 1. Bật nhận thông báo PC trên cả 3 trình duyệt cho cùng 1 admin<br>2. Tạo lượng thông báo PC đủ để phát sinh khoảng 120 lần gửi đồng thời trải đều trên 3 nhà cung cấp<br>3. Chạy job<br>4. Theo dõi tổng số kết nối đồng thời job mở ra (dùng lệnh xem kết nối mạng của tiến trình job)<br>5. Chờ xử lý xong và rà log | ~120 lần gửi đồng thời chia cho 3 route. Mốc đối chiếu: 50 mỗi route, **100 tổng**. | Tổng số kết nối đồng thời của tiến trình job **không vượt quá 100**, và số kết nối tới **từng** route không vượt quá 50. Phần vượt trần tổng phải **xếp hàng chờ** rồi được gửi, không lỗi ngay. Nếu lần gửi nào chờ lấy kết nối quá 5 giây thì phải kết thúc bằng lỗi **có ghi log rõ ràng**, không đứng im. Cuối cùng mọi thông báo đều được gửi trên cả 3 trình duyệt. | Chưa test |  | PRD |  |  |  |  | Lấp **n-1** + phần Boundary còn thiếu của `ENV-003`. NEW-20 mới chỉ chạm trần `perRoute` trên 1 route giả lập. |
| TC-REGRUN001-01 | REG-RUN-001 | Normal | Restart job để deploy bản fix trong lúc đang có thông báo xử lý dở — không mất, không kẹt | Job bản **chưa fix** đang chạy và đang xử lý một lô thông báo PC. Đã chuẩn bị sẵn bản fix để deploy. | 1. Tạo 300 bản ghi thông báo PC ở trạng thái chờ xử lý<br>2. Chạy job bản chưa fix, chờ tới khi log cho thấy đã xử lý khoảng 100 bản ghi<br>3. Ghi lại số bản ghi ở từng trạng thái tại thời điểm này<br>4. Dừng job và khởi động lại bằng bản đã fix<br>5. Để job chạy hết, sau đó đếm lại số bản ghi ở từng trạng thái | 300 thông báo PC, restart tại mốc ~100 bản ghi đã xử lý. | Sau khi restart, job **tiếp tục xử lý phần còn lại** và toàn bộ 300 bản ghi kết thúc ở trạng thái đã xử lý. **Không bản ghi nào kẹt vĩnh viễn ở trạng thái đang xử lý**, không bản ghi nào bị bỏ qua. Trình duyệt của admin nhận **đúng 300 thông báo, không nhận trùng** bản ghi nào thuộc lô đang xử lý dở lúc restart. | Chưa test |  | PRD |  |  |  |  | Lấp **B-3** (GAP `REG-RUN-001`, ưu tiên Cao). Evidence: bảng đếm số bản ghi từng trạng thái tại 3 mốc (trước restart / ngay sau restart / kết thúc) + số thông báo đếm được trên trình duyệt. |
| TC-REGRUN001-02 | REG-RUN-001 | Abnormal | Kill job đột ngột đúng lúc một lần gửi đang chờ phản hồi từ FCM | Job bản đã fix đang chạy, có đăng ký nhận thông báo PC thật. | 1. Tạo 50 bản ghi thông báo PC<br>2. Chạy job<br>3. Khi log cho thấy đang có lần gửi chờ phản hồi, kill tiến trình job **không cho dừng êm**<br>4. Kiểm tra trạng thái các bản ghi thông báo PC<br>5. Khởi động lại job và để chạy hết<br>6. Đếm số thông báo admin thực nhận trên trình duyệt | 50 thông báo PC, kill tiến trình giữa lúc đang chờ phản hồi. | Bản ghi đang gửi dở **không bị kẹt vĩnh viễn** ở trạng thái đang xử lý — hoặc quay về trạng thái chờ xử lý để lần chạy sau nhặt lại, hoặc kết thúc ở trạng thái lỗi có ghi lý do. Sau khi khởi động lại, toàn bộ 50 bản ghi đều kết thúc. Nếu bản ghi đang gửi dở được gửi lại thì admin có thể nhận trùng **đúng 1 thông báo đó** — ghi rõ số lượng thực tế vào kết quả để Dev/PO đối chiếu với quyết định ở REQ-008. | Chưa test |  | PRD |  |  |  |  | Lấp **B-3** + nối với **B-2** (cùng chạm rủi ro nhận trùng). |
| TC-REGRUN001-03 | REG-RUN-001 | Boundary | Restart job đúng thời điểm hàng đợi rỗng và đúng thời điểm hàng đợi đầy nhất | Job bản đã fix. | 1. Restart job khi **không có** bản ghi thông báo PC nào chờ xử lý, quan sát log khởi động<br>2. Tạo lượng thông báo PC lớn nhất mà production từng ghi nhận trong 1 lượt job<br>3. Restart job ngay khi job **vừa bắt đầu** nhặt lô này<br>4. Để chạy hết và đếm lại | Lô rỗng (0 bản ghi) và lô bằng đỉnh thực tế của production (lấy số từ M-11). | Với lô rỗng: job khởi động sạch, khởi tạo kết nối dùng chung thành công, **không ném lỗi**, không mở kết nối thừa. Với lô đỉnh: sau restart toàn bộ bản ghi vẫn được xử lý hết, thời gian hoàn tất không tăng bất thường, không bản ghi nào kẹt. | Chưa test |  | PRD |  |  |  |  | Lấp **B-3** phần Boundary (RULE-01 — `REG-RUN-001` ưu tiên Cao cần đủ 3 loại case). |
| TC-JOB001-02 | JOB-001 | Abnormal | FCM trả mã 429 vượt giới hạn tần suất — job không dừng, ghi log rõ và không mất bản ghi | Job bản đã fix. Đăng ký nhận thông báo PC trỏ tới máy chủ giả lập được cấu hình trả **HTTP 429** kèm header giới hạn tần suất cho 30 yêu cầu đầu, sau đó trả 201. | 1. Tra tài liệu chính thức mới nhất của FCM / Web Push để lấy giới hạn tần suất hiện hành, ghi lại nguồn và ngày tra<br>2. Tạo 100 bản ghi thông báo PC<br>3. Chạy job<br>4. Đếm số yêu cầu máy chủ giả lập nhận được và rà log job<br>5. Kiểm tra trạng thái cuối của 100 bản ghi | 100 thông báo PC. Máy chủ giả lập: 30 yêu cầu đầu trả 429, phần còn lại trả 201. | Job **không dừng** khi gặp 429. Log ghi rõ mã 429 cho từng lần gặp. **Số bản ghi vào (100) = số gửi thành công + số kết thúc ở trạng thái lỗi** — không bản ghi nào biến mất. Ghi rõ vào kết quả hành vi thực tế: có lùi tần suất (backoff) hay không, có thử lại hay không — **và đối chiếu với giới hạn chính thức tra được ở bước 1** để kết luận cấu hình hiện tại có an toàn ở quy mô production hay không. | Chưa test |  | STAGING |  |  |  | Spec không ghi | Lấp **M-4** (`JOB-001` điểm 1 + **RULE-05**) và **M-5** trigger (7). `Trạng thái đánh giá spec` phải hỏi Dev/Leader chốt trước khi kết luận Đạt. |
| TC-JOB001-03 | JOB-001 | Normal | Một lượt job xử lý trọn vẹn: số bản ghi vào bằng số ra, có cả bản ghi lỗi lẫn thành công | Job bản đã fix. Có 4 đăng ký nhận thông báo PC: 2 hợp lệ, 1 trả 410 đã huỷ đăng ký, 1 trỏ tên miền không tồn tại. | 1. Ghi lại số bản ghi thông báo PC ở trạng thái chờ xử lý trước khi chạy<br>2. Chạy job một lượt trọn vẹn<br>3. Chờ job báo kết thúc lượt<br>4. Đếm số bản ghi ở từng trạng thái cuối và đối chiếu với số ban đầu<br>5. Rà log job từ đầu tới cuối lượt | 40 thông báo PC trải trên 4 đăng ký nói trên. | **Số bản ghi vào = số đã xử lý thành công + số kết thúc ở trạng thái lỗi + số bị bỏ qua có lý do**, khớp tuyệt đối, không có bản ghi nào còn ở trạng thái chờ hoặc đang xử lý. Log ghi đủ dòng kết thúc lượt. Đăng ký trả 410 bị chuyển sang ngừng nhận, 2 đăng ký hợp lệ nhận đủ thông báo. | Chưa test |  | STAGING |  |  |  |  | Lấp phần **Normal** còn thiếu của `JOB-001` (**M-8**). Cover `JOB-001` điểm (4) — đối chiếu số vào/ra. |
| TC-SEC002-01 | SEC-002 | Abnormal | Log job khi gửi lỗi không được chứa địa chỉ nhận đầy đủ, khoá xác thực hay khoá bí mật VAPID | Job bản đã fix, đã bật ghi log ở mức chi tiết nhất. Có đăng ký nhận thông báo PC trỏ máy chủ giả lập trả 400 kèm **nội dung phản hồi dài có chứa chuỗi giống token**. | 1. Tạo 5 bản ghi thông báo PC<br>2. Chạy job để phát sinh cả nhánh gửi thành công lẫn nhánh lỗi<br>3. Mở toàn bộ file log của lượt chạy<br>4. Tìm trong log các chuỗi: địa chỉ nhận đầy đủ, khoá công khai, khoá xác thực của đăng ký, khoá bí mật VAPID, email admin<br>5. Kiểm tra thêm màn hình lỗi và console của trình duyệt admin | 5 thông báo PC. Máy chủ giả lập trả 400 kèm nội dung phản hồi dài chứa chuỗi dạng token. | Log **không chứa** khoá bí mật VAPID, không chứa khoá xác thực của đăng ký, và **không in địa chỉ nhận ở dạng đầy đủ** (nếu cần trace thì phải che bớt, vì địa chỉ nhận chứa mã định danh trình duyệt). Nội dung phản hồi lỗi được ghi log phải **giới hạn độ dài**, không đổ nguyên khối dữ liệu bên thứ ba trả về. Màn lỗi và console trình duyệt admin không lộ thông tin nào trong danh mục trên. | Chưa test |  | STAGING |  |  |  |  | Lấp **M-10** (GAP `SEC-002`, Cao). Rủi ro tăng sau fix vì nhánh lỗi giờ đọc và ghi log **toàn bộ** nội dung phản hồi. Evidence: kết quả tìm kiếm trên file log (dán lệnh + kết quả rỗng). |
| TC-PERFLARGE001-01 | PERF-LARGE-001 | Boundary | Chạy job với lượng thông báo bằng đỉnh thực tế của khách hàng lớn nhất | Job bản đã fix. **Đã tra và ghi lại** số bản ghi thông báo PC lớn nhất mà một lượt job từng xử lý trên production, kèm nguồn số liệu. | 1. Tra số liệu production: một lượt job web push PC xử lý nhiều nhất bao nhiêu bản ghi, cho bao nhiêu bot và bao nhiêu đăng ký — ghi rõ nguồn và ngày tra<br>2. Tạo test data **bằng hoặc lớn hơn** con số đó<br>3. Ghi lại thời điểm bắt đầu, chạy job<br>4. Đo thời gian tới khi job báo kết thúc lượt<br>5. Đếm số bản ghi ở từng trạng thái và rà log tìm lỗi kết nối | Lượng bản ghi = đỉnh production (điền số thật ở bước 1, **không tự chọn con số tròn**). | Job xử lý hết trong thời gian chấp nhận được và **ghi rõ con số đo được** để làm mốc so sánh cho các lần sau. Không xuất hiện lỗi `Connection reset by peer`, không lỗi hết thời gian chờ lấy kết nối từ pool, không luồng nào treo. Số bản ghi vào = số ra. **Ghi rõ nguồn của con số quy mô** vào kết quả theo yêu cầu của `FUNC-004`. | Chưa test |  | PRD |  |  |  |  | Lấp **M-11**. Quy mô hiện tại (200 bản ghi) là con số tự chọn, chưa có căn cứ từ production. |
| TC-CONC001-05 | CONC-001 | Abnormal | Thông báo trùng khi thử lại — quan sát trên trình duyệt thật, không chỉ đếm request | Job bản đã fix. Có đăng ký nhận thông báo PC **thật** từ Chrome trên PC. Có cách chủ động làm đứt kết nối sau khi yêu cầu đã gửi đi (ví dụ chặn gói tin chiều về ở tầng mạng). | 1. Mở Chrome đã bật nhận thông báo PC, giữ màn hình quan sát được<br>2. Tạo **đúng 1** bản ghi thông báo PC có tiêu đề dễ nhận biết<br>3. Chạy job, đồng thời chặn gói tin chiều về ngay sau khi yêu cầu đã được gửi đi<br>4. Bỏ chặn để lần thử lại đi được<br>5. **Đếm số thông báo thực sự hiện lên trên Chrome**<br>6. Lặp lại 5 lần để xem tỷ lệ xuất hiện | 1 thông báo PC mỗi lần, lặp 5 lần. Tiêu đề có đánh số lần để phân biệt. | Ghi nhận **con số thật**: trong 5 lần, bao nhiêu lần Chrome hiện **2 thông báo giống hệt nhau**. Đây là dữ liệu để Dev/PO chốt REQ-008. **Không tự đánh Đạt/Không đạt** — điền kết quả và chuyển cho người quyết định. Nếu quyết định là không chấp nhận trùng thì TC này thành Không đạt và Dev phải đổi cấu hình thử lại. | Chưa test |  | PRD |  |  |  | Đã hỏi leader | Lấp **B-2**. NEW-18 mới đếm request ở phía máy chủ giả lập, **chưa ai quan sát trình duyệt thật** — mà đó mới là thứ admin nhìn thấy (RULE-06 output cuối chuỗi). |
| TC-FUNC001-04 | FUNC-001 | Abnormal | Luồng chính khi bot vừa hết hạn giữa lúc job đang xử lý lô của bot đó | Job bản đã fix. Có 1 bot **còn hạn** với 1 đăng ký nhận thông báo PC hợp lệ và 20 bản ghi thông báo PC chờ xử lý. | 1. Chạy job, chờ tới khi log cho thấy đã xử lý khoảng 10/20 bản ghi<br>2. Trong lúc job đang chạy, chuyển bot sang trạng thái hết hạn quá 7 ngày<br>3. Để job chạy hết lô<br>4. Kiểm tra trạng thái cuối của 20 bản ghi và rà log<br>5. Đếm số thông báo admin thực nhận trên Chrome | 20 thông báo PC. Đổi trạng thái bot tại mốc ~10 bản ghi đã xử lý. | Hệ thống xử lý **nhất quán**: các bản ghi sau thời điểm bot hết hạn phải chuyển sang trạng thái bỏ qua do bot hết hạn kèm log lý do, **không** được gửi đi. Không bản ghi nào kẹt ở trạng thái đang xử lý. Số thông báo admin nhận trên Chrome khớp đúng số bản ghi được gửi trước thời điểm đổi trạng thái. Kết nối đang mở không bị rò rỉ khi nhánh bỏ qua được kích hoạt giữa chừng. | Chưa test |  | STAGING |  |  |  |  | Lấp **M-8** (`FUNC-001` Cao, thiếu Abnormal). Nối tiếp NEW-19 nhưng ở tình huống đổi trạng thái **giữa chừng** thay vì đã hết hạn từ đầu. |
| TC-FUNC001-05 | FUNC-001 | Boundary | Nội dung thông báo dài nhất và ngắn nhất mà hệ thống cho phép, gửi qua kết nối dùng chung | Job bản đã fix. Có đăng ký nhận thông báo PC thật từ Chrome trên PC. Đã xác nhận **nguồn của giới hạn** độ dài tiêu đề và nội dung thông báo (spec nội bộ hay giới hạn kích thước gói tin của Web Push). | 1. Ghi lại nguồn giới hạn độ dài đã tra được<br>2. Tạo lần lượt 5 bản ghi thông báo PC: đúng biên, biên trừ 1, biên cộng 1, tiêu đề rỗng, nội dung rỗng<br>3. Chạy job<br>4. Quan sát từng thông báo hiện trên Chrome<br>5. Rà log job cho từng lần gửi | 5 bản ghi theo 5 mẫu biên. Nội dung dùng tiếng Nhật 「新しい友だちが登録されました」 lặp lại cho đủ độ dài, có kèm ①②㈱ và emoji 🎉. | Với biên và biên trừ 1: Chrome hiện thông báo đầy đủ, **không mất ký tự tiếng Nhật, không lỗi font, không hiện ô vuông**. Với biên cộng 1: hệ thống xử lý **có chủ đích** — hoặc cắt bớt kèm log, hoặc từ chối gửi kèm log lý do, **không được ném lỗi làm chết luồng** và không được để bản ghi kẹt. Tiêu đề/nội dung rỗng: xử lý nhất quán, không ném lỗi. **Ghi rõ nguồn của giới hạn** vào kết quả. | Chưa test |  | PRD |  |  |  |  | Lấp **M-8** (`FUNC-001` Cao, thiếu Boundary) + `FUNC-004` 5 pattern biên. Kết nối dùng chung mang gói tin lớn hơn là điểm chưa ai thử. |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 điểm, tất cả đều xuất phát từ cờ `CONFLICT` của Studio:

**6.1 — `REQ-006` / `CONFLICT-01` · Phạm vi cơ chế thử lại**
- Section: `FA-006 job-spec` mục 3.5 (web push PC) — hoặc bổ sung mới nếu chưa có.
- Nội dung cần update: ghi rõ **thử lại 2 lần CHỈ áp dụng cho lỗi đứt kết nối ở tầng mạng**. Khi FCM trả mã lỗi HTTP (500/503) hoặc quá thời gian đọc 15 giây thì **không thử lại**, kết thúc ngay và ghi log. Hệ quả nghiệp vụ phải được viết ra: **FCM lỗi tạm thời = thông báo mất luôn, không có lần thử lại nào**.
- Người chịu trách nhiệm: Dev (`Thanh Duy Nguyen`) xác nhận đúng ý đồ → PM/PO duyệt.

**6.2 — `REQ-008` / `CONFLICT-02` · Chấp nhận thông báo trùng hay không** *(gắn với BLOCKER B-2)*
- Section: như trên.
- Nội dung cần update: chốt `requestSentRetryEnabled = true` là **đánh đổi có chủ đích** (thà trùng còn hơn mất) hay là **thiếu sót**. Nếu chấp nhận, spec phải ghi rõ "admin có thể nhận thông báo trùng khi mạng chập chờn" để CS không coi đó là bug mới.
- Người chịu trách nhiệm: **PO quyết định**, Dev thực thi.

**6.3 — `CONFLICT-03` · Mốc thời gian chờ đọc 15 giây**
- Section: như trên.
- Nội dung cần update: ghi mốc 15 giây là **giới hạn mới do bản fix đưa vào** (trước fix không có giới hạn tương đương, luồng có thể treo rất lâu). Cần ghi cả 8 hằng số tuning vào spec thay vì chỉ nằm trong code — hiện chỉ tồn tại dưới dạng hằng số viết thẳng trong `WebPushNotificationService.java`.
- Người chịu trách nhiệm: Dev + Leader.

> Ngoài ra: **RULE-10** — bug này lọt production, nên bổ sung 1 dòng vào `framework/catalog-lme.md` khối D2 (xem NIT n-4).

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ⚠️ (BUG có TC nhưng TC quyết định `skip`) · A.2 ✅ · A.3 ⚠️ (mục 4.2 file 03 sai) · A.4 ✅ · A.5 ⚠️ (2 ORPHAN) · A.6 ✅
- [x] **B. Chất lượng từng TC** — B.1 ✅ (precondition + expected rất cụ thể, có số đo) · B.2 ✅ · B.3 ✅ · B.4 ✅ (data dùng chuỗi tiếng Nhật thật, không dùng `test`/`abc`)
- [x] **C. Chất lượng bộ TC** — tỷ lệ loại case 48/34/17, Boundary thấp (m-5); không có TC trùng lặp; phân bố quan điểm lệch về nhóm `TOOL-*` (M-9)
- [x] **D. Spec alignment** — ❌ 3 xung đột chưa chốt, xem §6
- [x] **E. Hành chính** — ⚠️ `TC-NOVP-0x` sai format (m-1); `spec_status` trống 29/29 (M-1); `Evidence thực tế` trống 29/29 (M-2)
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** không áp dụng (job nền, không có ô nhập) · **B** không áp dụng · **C** không áp dụng (không thuộc 21 đường gửi tin LINE) · **D/D2** ❌ **vi phạm RULE-08**, xem B-1 · **E** không áp dụng
  - [x] F.3 RULE quy trình — RULE-01 ❌ (M-8) · RULE-02 ❌ (M-2) · RULE-03 ⚠️ (m-3) · RULE-04 ❌ (M-12) · RULE-05 ❌ (M-4) · RULE-06 ✅ (NEW-24/25/26/28 quan sát Chrome thật) · RULE-07 ⚠️ (verify DB + log ✅ qua NEW-21/22, **WHERE 2 tài khoản ✅** qua NEW-22 — nhưng thiếu tầng màn hình admin) · RULE-08 ❌ (B-1) · RULE-09 ✅ **không áp dụng** (`web-push 5.1.1` giữ nguyên, không version-up) · RULE-10 ⚠️ (n-4) · RULE-12 ⚠️ (M-14)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` — Luồng chính hoàn tất đúng đặc tả | Cao | ◯ luôn bắt buộc | NEW-1 · NEW-2 · NEW-9 | 1/3 | **RISK** — chỉ có Normal, thiếu Abnormal + Boundary (M-8) |
| `FUNC-004` — Giới hạn trên/dưới | Cao | ◯ có giới hạn số kết nối / thời gian chờ | NEW-8 | 0/1 | **RISK** — TC duy nhất `skip`; chưa ghi **nguồn của giới hạn** |
| `CONC-001` — Một hành động chỉ xử lý 1 lần | Cao | ◯ batch đa luồng chạm giới hạn dùng chung | NEW-10 · NEW-12 · NEW-18 · NEW-20 | 4/4 | **OK** về loại case (đủ N/A/B). ⚠️ Kịch bản 1-3 bỏ không ghi lý do (m-3); NEW-18 kết luận sai (B-2) |
| `DATA-DB-001` — WHERE scope + khóa mồ côi | Cao | ◯ có UPDATE `push_subscriptions` | NEW-21 · NEW-22 | 2/2 | **RISK** — chỉ Abnormal (M-8). **Điểm cộng**: NEW-22 kiểm đúng `WHERE` trên 2 tài khoản khác nhau như RULE-07 đòi hỏi |
| `DATA-MIG-001` — Migration dữ liệu cũ | Cao | ◯ (để chứng minh **không có** thay đổi lược đồ) | NEW-5 | 0/1 | **RISK** — `skip`, dù techNote đã có kết luận (M-3) |
| `JOB-001` — Job nền / batch gọi API ngoài | Cao | ◯ **BẮT BUỘC** — job nền gọi FCM theo lô | NEW-13 | 1/1 | **RISK** — chỉ Abnormal; **thiếu hẳn điểm (1) rate limit** (M-4) và điểm (4) đối chiếu số vào/ra |
| `ENV-003` — Khác biệt dev / staging / production | Cao | ◯ **BẮT BUỘC** — job nền + domain bên thứ 3 | NEW-11 | **0/1** | **GAP thực tế** → **[BLOCKER] B-1**. TC duy nhất `skip`, 20 TC Đạt đều dùng stub |
| `REG-SHARED-001` — Shared code / logic | Cao | ◯ sửa service dùng chung | NEW-3 · NEW-6 | **0/2** | **GAP thực tế** → **[MAJOR] M-14**. Dev **có** cung cấp danh sách caller (điểm cộng), nhưng chưa ai verify + chưa rà brand |
| `REG-RUN-001` — Job đang chạy dở khi release | Cao | ◯ **BẮT BUỘC** — fix nằm trong `init()`, phải restart job | — | **0/0** | **GAP** → **[BLOCKER] B-3** |
| `MSG-004` — Preview khớp nội dung nhận thật | Cao | ◯ (adapt: output cuối là thông báo Chrome PC) | NEW-24 · NEW-25 | 2/2 | **RISK** — chỉ Normal (M-8). **Điểm cộng**: chạy trên Chrome thật với khoá VAPID thật, thoả RULE-06 |
| `SEC-002` — Không lộ token / credential | Cao | ◯ fix làm tăng lượng log; endpoint chứa mã định danh trình duyệt | NEW-17 (một phần) | 1/1 | **RISK** → **[MAJOR] M-10**. Chỉ cover khoá bí mật VAPID lúc khởi động, không quét endpoint / nội dung phản hồi |
| `PERF-LARGE-001` — Dữ liệu lớn theo ngưỡng THỰC TẾ | Trung bình → Cao (job) | ◯ tính năng cải thiện hiệu năng | NEW-10 · NEW-20 | 2/2 | **RISK** → **[MAJOR] M-11**. Quy mô 200/100 là con số tự chọn, không có nguồn từ production |
| `ENV-001` — Fail-safe khi sự cố hạ tầng | Cao | ◯ (một phần — đứt kết nối giữa chừng) | NEW-13 · NEW-16 | 2/2 | **OK** |
| `STATE-CLEAN-001` — Dọn dẹp khi hủy / hạ gói | Cao | ◯ (một phần — bot hết hạn quá 7 ngày) | NEW-19 | 1/1 | **OK** — đối chứng âm, xác nhận bản fix không làm đổi nhánh này |
| `DATA-AUDIT-001` — Audit log / Lịch sử thao tác | Cao | △ (đăng ký thông báo không phải PII nhạy cảm cao) | — | 0/0 | **[NIT] n-3** — Leader cân nhắc, không flag |
| `COMPAT-LEGACY-001` / RULE-09 | Cao | ✗ **không áp dụng** | — | — | `web-push 5.1.1` giữ nguyên phiên bản, chỉ thay tầng thực thi. Không có nhánh cũ/mới song song |
| `DEPLOY-ASSET-001` · `DEPLOY-LIVE-001` | Cao | ✗ **không áp dụng** | — | — | Job nền, không có JS/CSS/asset và không có client cũ gọi server mới |
| `MSG-001` · `MSG-003` · `MSG-005` · `BULK-001` · `LIFF-ENTRY-001` · `MEDIA-*` · `FRIEND-001` · `LIST-001` | Cao/TB | ✗ **không áp dụng** | — | — | Không thuộc luồng gửi tin LINE, không có bộ lọc, không chạm media / friend info / danh sách |
| **Mã Studio không thuộc `checklist-lme.md`** | — | — | `TOOL-ERRHYG-001` ×7 · `TOOL-NEGCTRL-001` ×2 · trống ×4 | 9 pass / 4 skip | **KHÔNG tính là cover** → **[MAJOR] M-9**. Nội dung TC có giá trị, chỉ là không map được vào lưới quan điểm |

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Nguồn: MCP LME TEST STUDIO task #46 (ticket 39255), fetch 2026-08-25. Draft do /review-tc sinh — Leader verify trước khi gửi member. -->
