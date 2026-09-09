# 05 — Review Report

> Draft do `/review-tc` sinh ngày **2026-09-04** — Leader verify trước khi trả member.

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#221` |
| Ticket | Redmine `#38535` (suy từ tên folder) |
| Thời điểm fetch | `2026-09-04` (`testcase_list(task_id=221, limit=100)`) |
| Tổng TC lấy về | **23 TC** |
| Snapshot đã ghi | `04-tc-list.md` — **refresh** (bản cũ có header `<!-- source: MCP LME TEST STUDIO — task_id=221 ... fetch lúc 2026-09-03 -->`, là snapshot do tool sinh nên ghi đè theo 0.2b) |
| Nguồn 2 (Sheet human) | **Không dùng** — đã dừng ở nguồn 1 |
| Nguồn 3 (file 04) | **Không dùng** — đã dừng ở nguồn 1 |
| Đối chiếu chéo nguồn | **KHÔNG** — dừng ở nguồn đầu tiên có TC theo quy tắc BƯỚC 0 |
| **Nguồn spec đã dùng** | `spec-features/admin/notify-setting/` — [feature-spec.md §5 Business Rules (BR-01…BR-15)](../../spec-features/admin/notify-setting/feature-spec.md), [feature-spec.md §2 Luồng 5 — Cài đặt liên kết ChatWork](../../spec-features/admin/notify-setting/feature-spec.md), [web/logic-spec.md `ajaxSaveUrlChatWork()`](../../spec-features/admin/notify-setting/web/logic-spec.md), [web/api-spec.md EP-11](../../spec-features/admin/notify-setting/web/api-spec.md), [db/db-mapping.md `notify_setting` / `mobile_notify`](../../spec-features/admin/notify-setting/db/db-mapping.md), [job/job-spec.md §ChatWork job loop](../../spec-features/admin/notify-setting/job/job-spec.md). **Không** cần tới lme.jp/manual. |

### Metadata task Studio

| Trường | Giá trị |
|---|---|
| `status` / `pipelineStage` | `done-ai` |
| `aiResult` | **`fail`** |
| `reviewState` / `reviewed` | `leader` / **`false`** |
| `round` | 1 |
| `branch` | `ai_fixbug_38535` |
| `exec` | total 23 · **pass 17** · **fail 1** · other 1 · **untested 4** |
| `toolWritten` | 23 tổng — tool 22 · mcp 1 · **human 0** (rate 95.7%) |
| `submittedWithoutMcp` | `false` |
| `ranAt` / `runBy` | `2026-09-03 14:39:11` / `haodtb` (runs = 2, env `local`) |

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn

| # | Nội dung | Đánh giá |
|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass` = **17/23 = 73,9%** → **`[MAJOR]`** (< 80%). 6 TC còn lại KHÔNG có kết luận test: 4 chưa chạy + 1 `skip` + 1 `fail`. |
| 2 | **TC `fail` / gắn ticket bug** | `NEW-3` — `fail`, đã raise ticket **#40476** → không rơi vào mức `[BLOCKER]` "fail chưa raise ticket". Nhưng phải chốt trạng thái #40476 trước khi đóng #38535. |
| 3 | **Môi trường đã chạy** | 19 TC đã chạy **100% ở `env = local`**. Staging **0** · Production **0**. Task chạm **job nền** → **`[MAJOR]` RULE-08 / ENV-003**. Bug gốc được KH báo trên **Staging** (subject `[Stagging]`, journal 2026-07-09 "e verify trên stg đang thấy vẫn bị"). |
| 4 | **Ai chạy** | `last_exec.source = ai`, `by = haodtb` → toàn bộ 19 kết quả `pass` do **AI pipeline tự chạy**, không phải QA người chạy tay. Nhóm rủi ro cao (liên kết lần đầu, dọn hàng chờ) chỉ có kết quả Đạt do AI → **`[MAJOR]`**. |
| 5 | **Tác giả TC** | 22/23 `author = AI`, 1/23 `haodtb@mcp`, **0 TC do member người viết**. `reviewState = leader`, `reviewed = false` → **`[MAJOR]`** (≥ 50% TC do AI sinh mà review chưa `done`). |
| 6 | **Mã quan điểm không có trong `checklist-lme.md`** | **5 mã / 9 TC** — xem bảng dưới. Các TC này **KHÔNG được tính là cover** ở BƯỚC 2/3.6. |

**Mã quan điểm Studio không tồn tại trong `framework/checklist-lme.md`** (đã grep đối chiếu 80 mã):

| Mã Studio | Số TC | TC |
|---|---|---|
| `TOOL-NEGCTRL-001` | 4 | NEW-14, NEW-22, NEW-24, NEW-29 |
| `TOOL-KNOW-002` | 2 | NEW-6, NEW-7 |
| `API-CONTRACT-001` | 1 | NEW-1 |
| `TOOL-ERRHYG-001` | 1 | NEW-2 |
| `JOB-002` | 1 | NEW-27 |

> ⚠️ Hệ quả nặng nhất: **NEW-6 · NEW-7 · NEW-27** — 3 TC quan trọng nhất của ticket (tái hiện bug ở nhánh update, nhánh create, và tầng job) đều mang mã **không có trong framework** → coverage của `FUNC-001` / `JOB-001` không map được về quan điểm chuẩn. Đây là vấn đề nhãn, không phải vấn đề nội dung TC — nội dung 3 TC này viết tốt.

---

## 1. Verdict

# ❌ REJECTED

**5 `[BLOCKER]`** — bộ TC hiện tại **chưa chứng minh được bug đã hết**. Toàn bộ 17 kết quả Đạt dừng ở **tầng dữ liệu trên máy local**; không một lần chạy nào mở phòng Chatwork thật để xác nhận triệu chứng mà khách hàng báo đã biến mất. 4/5 TC nhóm `job` — chính là nhóm quan sát triệu chứng đó — chưa chạy.

---

## 2. Tóm tắt cho member

Bộ TC **thiết kế rất tốt về mặt nội dung**: có đủ cặp oracle đối xứng (cái phải MẤT / cái phải CÒN), tách đúng 2 nhánh `update` vs `create` — đúng nhánh làm bug bị re-open ngày 20/08, và có 3 đối chứng âm chắc tay ở tầng dữ liệu (bot khác, kênh App/PC, bản ghi đã gửi sẵn). Phần thiết kế này giữ nguyên, không cần sửa.

Vấn đề nằm ở **chỗ dừng lại**: bug của khách là *"Chatwork nhận hàng loạt thông báo cũ"*, nhưng mọi TC đã chạy chỉ kiểm tới cột trạng thái trong DB rồi dừng — chưa TC nào đã chạy mở phòng Chatwork ra nhìn. Đúng 5 TC làm việc đó (`NEW-27`, `NEW-28`, `NEW-29`, `NEW-33`, `NEW-31`) thì 4 chưa chạy và 1 `skip`. Cộng thêm 3 vùng Dev đã **tự khai là rủi ro** — admin + nhân viên cùng bot dọn chéo hàng chờ, và 2 luồng yokoten chưa sửa — hiện **không có TC nào**.

**Phải làm trước khi review lại**: chạy 5 TC nhóm `job` trên **staging** (không phải local), bổ sung TC cho 3 vùng rủi ro Dev đã khai, và chốt ticket #40476 (`NEW-3` đang fail).

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — job gửi bù thông báo phát sinh trước khi liên kết | Root cause | NEW-6 (nhánh update) · NEW-7 (nhánh create) · **NEW-27** (tầng job — oracle thật) | 3 | 2/3 pass · NEW-27 **chưa chạy** | **RISK** |
| **F1** `ajaxSaveUrlChatWork` | Direct | NEW-1, NEW-2, NEW-3, NEW-4, NEW-5, NEW-6, NEW-7, NEW-8, NEW-13, NEW-14, NEW-15, NEW-16, NEW-17 | 13 | 12/13 pass · NEW-3 **fail** (#40476) | **RISK** |
| **F2** `skipChatworkNotifyBeforeLink` (hàm mới) | Direct | NEW-6, NEW-7, NEW-8, NEW-13, NEW-14, NEW-4, NEW-21, NEW-22, NEW-24, NEW-31, NEW-33 | 11 | 9/11 pass · NEW-31 skip · NEW-33 chưa chạy | **RISK** |
| **F3** `saveNotifySettingReceive` / `saveNotifySettings` (yokoten chưa sửa) | Indirect | *(không TC nào)* | **0** | — | **GAP** |
| **F4** `HandlePushNotifyChatwork` (job linect-service **+ bản artisan cũ**) | Indirect | NEW-27, NEW-28, NEW-29, NEW-33, NEW-31 | 5 | **0/5** — 4 chưa chạy + 1 skip | **RISK** |
| **F5** `insertMobileNotify` (producer hàng chờ) | Indirect | NEW-9, NEW-28 | 2 | 1/2 pass · NEW-28 chưa chạy | **RISK** |
| **F6** `RecoverNotifySettingCloneStaff` (yokoten chưa sửa) | Indirect | *(không TC nào)* | **0** | — | **GAP** |
| **D1** `mobile_notify.status_chat_work` UPDATE | Data | NEW-6, NEW-7, NEW-8, NEW-21, NEW-22, NEW-24, NEW-9 | 7 | 7/7 pass | **OK** |
| **D2** `notify_setting.last_notify_chat_work_time` UPDATE | Data | NEW-6, NEW-1, NEW-23 (phải đặt lại) · NEW-13, NEW-14, NEW-4 (phải KHÔNG đặt lại) | 6 | 6/6 pass | **OK** |
| **D2b** `notify_setting.next_notify_chat_work_time` — **cổng vào của job** (`job-spec.md` dòng 273) | Data | *(không TC nào)* | **0** | — | **GAP** |
| **D3** `notify_setting.chat_work_total_msg_error` UPDATE | Data | NEW-1, NEW-23 (tầng dữ liệu) · NEW-29 (tầng job) | 3 | 2/3 pass · NEW-29 **chưa chạy** | **RISK** |
| **T1** Notification Settings (FA-006) | Feature | Toàn bộ nhóm `ui` (9 TC) | 9 | 9/9 pass | **RISK** (xem F3 — luồng bật/tắt công tắc cùng màn không có TC) |
| **T2** Delivery Error List (FA-028) | Feature | NEW-29 (tầng job) · NEW-23, NEW-1 (tầng dữ liệu) | 3 | 2/3 pass · TC duy nhất quan sát được cảnh báo **chưa chạy** | **RISK** |

**Tổng**: `OK` 2 · `RISK` 8 · `GAP` 3.

### ORPHAN TCs

**Không có.** Cả 23 TC đều trace được về `BUG` / `F*` / `D*` / `T*`.

> Ghi chú về **AP-5** (over-coverage tầng downstream): 5 TC nhóm `job` test `HandlePushNotifyChatwork` — code **không bị chạm** bởi bản vá. Theo thông lệ đây là dấu hiệu AP-5, nhưng **ở ticket này KHÔNG phải**: job chính là **kênh output** nơi triệu chứng khách hàng biểu hiện (KH nhìn thấy tin trong phòng Chatwork, không nhìn thấy cột DB). Theo **RULE-06**, verify tại job là **bắt buộc**, không phải thừa. Giữ nguyên 5 TC này.

---

## 3.5 Fix-shape analysis (adversarial)

Mục 2 `03-dev-impact.md`: *"…đánh dấu 'đã gửi' cho toàn bộ thông báo còn tồn đọng của bot, đồng thời đặt lại mốc thời gian gửi Chatwork và ngưỡng đếm lỗi phát hành… Đánh dấu theo `bot_id` đúng như cách job đọc/đánh dấu hàng chờ. **Yokoten: 2 chỗ cùng họ chưa sửa**…"*

| Fix shape khớp | Câu hỏi adversarial | TCs trả lời được? | Kết luận |
|---|---|---|---|
| **"sửa hàm dùng chung / mẫu xử lý tồn đọng"** (`REG-SHARED-001`) | Có danh sách nơi ảnh hưởng do Dev cung cấp? Có TC test **từng nơi** trong danh sách? | Danh sách **CÓ** (Dev tự khai 2 nơi: bật lại công tắc Chatwork · `RecoverNotifySettingCloneStaff`). TC cho 2 nơi đó: **0**. | **`[BLOCKER]`** |
| **"fix race condition / concurrent"** (`CONC-001`) | Đủ **4 kịch bản**? Evidence có đếm số lần xử lý thực tế? | (1) double-click ✓ NEW-13 · (2) 2 tab/2 thiết bị cùng user ✗ · (3) **2 user khác nhau cùng thao tác** ✗ ← *đúng rủi ro Dev tự khai* · (4) batch đa luồng ~NEW-31 nhưng `skip`. | **`[BLOCKER]`** |
| **"gửi tin / đối tượng nhận"** (`MSG-004`, RULE-06) | Nhận tin **THẬT** ở output cuối hay chỉ nhìn cột trạng thái / số đếm? | 17/17 TC pass đều dừng ở tầng dữ liệu. TC mở phòng Chatwork thật = NEW-27 / NEW-28 → **cả hai chưa chạy**. | **`[BLOCKER]`** |
| **"job nền + gọi API bên thứ 3 theo lô"** (`JOB-001`, `ENV-003`) | Số bản ghi **vào = xử lý thành công + hàng đợi lỗi**, không bản ghi nào biến mất? Rate limit Chatwork (429)? Chạy production? | Không TC nào lập sổ cân bằng vào/ra. Không TC nào chạm 429 (`job-spec.md` bước viii). 0 TC chạy staging/production. | **`[BLOCKER]`** (JOB-001 chưa cover) + **`[MAJOR]`** ENV-003 |
| **"số đếm / ngưỡng"** (`DATA-COUNT-001`) | Đối chiếu nhiều nguồn + phép tính tay? | NEW-23 có phép tính tay 3 bot (0 / 3 / 3) — **tốt**. Nhưng không đối chiếu với **màn Delivery Error List (T2)** mà người dùng thật sự nhìn. | **`[MAJOR]`** |
| **"đổi trạng thái hàng loạt"** (`DATA-AUDIT-001`) | Có audit log ai/khi nào/cũ→mới? | `mobile_notify` không nằm trong nhóm dữ liệu nhạy cảm (khách hàng / thanh toán / phân quyền / tag) → trigger không khớp. | × không áp dụng |

### Symptom-only KH report check

**KHÔNG dính AP-2.** File 01 có Actual/Expected cụ thể + evidence (`prnt.sc`, `screenrec.com`), Dev truy được root cause kèm dòng code.

**Nhưng có tín hiệu mạnh hơn — bug đã bị RE-OPEN 2 lần:**

| Lần | Ngày | Kết quả |
|---|---|---|
| Fix 1 | 2026-07-09 | Re-open cùng ngày — "verify trên stg đang thấy vẫn bị" |
| Fix 2 | 2026-07-30 | Re-open 2026-08-20 — "vẫn bị đối với **trường hợp đầu tiên**" |
| Fix 3 | 2026-08-26 | Đang review (bản này) |

→ Hai giả thuyết root cause trước đều **đúng một phần và bỏ sót nhánh**. Nhánh bỏ sót lần 2 (`create`) nay đã có `NEW-7`. Câu hỏi adversarial còn lại: **nhánh thứ ba bị bỏ sót là gì?** — ứng viên rõ ràng nhất chính là **2 luồng yokoten Dev tự khai chưa sửa** (F3, F6), hiện **0 TC**. Đây là lý do `REG-SHARED-001` được nâng lên `[BLOCKER]` chứ không phải `[MAJOR]`.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| AP-1 Single-trigger generic-fix | ✗ | Fix không phải generic catch-all. |
| AP-2 Symptom-only KH report | ✗ | KH có Actual/Expected + evidence cụ thể. |
| **AP-3 Happy-path-only regression** | **✓** | `T2` (FA-028) chỉ có 1 TC quan sát được (`NEW-29`) và TC đó **chưa chạy**; không có TC chạy T2 ở trạng thái biên (đã có lỗi tích lũy sẵn + vừa liên kết). |
| AP-4 Specific code-check disguised as generic catch | **✓ (một phần)** | Mục "Commit / Pull Request" **không có link PR** — chỉ có commit hash `5fa27b7ca8` + link dashboard nội bộ. Không review được diff thật để xác nhận điều kiện `isFirstLink`. |
| AP-5 Layer-downstream over-coverage | ✗ | Xem ghi chú ở §3 — job là output channel, không phải downstream layer bị over-test. |
| AP-6 Mục 3 dev-impact trống | ✗ (biến thể nhẹ) | Mục 3 có đủ 7 dòng. Nhưng **§4.1 gốc của Dev chỉ ghi tên FILE, không list function** — bảng F1–F6 là do `/new-task` map lại từ §3, chưa được Dev xác nhận. |

---

## 3.6 Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | NEW-6, NEW-7, NEW-8 *(mã Studio `TOOL-KNOW-002`/`PERM-001`)* | 3/3 pass | ⚠️ Cover về nội dung, nhưng 2/3 TC mang mã ngoài framework |
| `FUNC-002` | Cao | ◯ có form nhập liệu (ô URL phòng chat) | NEW-15 (5 biến thể sai) · NEW-6 (Normal) | 2/2 pass | ⚠️ Thiếu **Boundary** → RULE-01 |
| `FUNC-003` | TB **→ Cao** (field là URL) | ◯ | NEW-15, NEW-17 (Abnormal) · NEW-6 (Normal) | 3/3 pass | ⚠️ **Thiếu Boundary**, không ghi lý do → `[MAJOR]` RULE-01 |
| `FUNC-UNIQ-001` | TB | ◯ chặn trùng phòng chat trong cùng bot | NEW-16 (UI), NEW-5 (API) | 2/2 pass | ✅ OK |
| `CONC-001` | Cao | ◯ **BẮT BUỘC** — nút thực thi + nhiều người cùng sửa | NEW-13, NEW-4 (Normal/Abnormal) · NEW-31, NEW-33 (Boundary) | 2/4 pass · **NEW-31 skip · NEW-33 chưa chạy** | ❌ **Thiếu kịch bản (2) và (3)** của CONC-001 → `[BLOCKER]` |
| `DATA-DB-001` ★ | Cao | ◯ **BẮT BUỘC** — có UPDATE | NEW-21 (2 bot), NEW-22 (2 cột kênh), NEW-24 (lọc theo trạng thái) | 3/3 pass | ⚠️ Có `WHERE` scope theo **2 bot** ✓ nhưng **thiếu 2 staff cùng 1 bot** → RISK |
| `PERM-001` | Cao | ◯ admin vs nhân viên | NEW-8 | 1/1 pass | ⚠️ Chỉ nhánh create của nhân viên; không có tương tác admin ↔ nhân viên |
| `PERM-002` | Cao | ◯ thao tác nhạy cảm (cập nhật hàng loạt) | NEW-3 | **fail** (#40476) | ❌ Chưa kết luận được |
| `MSG-002` | Cao | ◯ gửi tin theo lịch | NEW-9 | 1/1 pass | ⚠️ Chỉ tầng hàng chờ |
| `MSG-004` | Cao | ◯ **BẮT BUỘC** — output user cuối nhìn thấy | NEW-28 | **chưa chạy** | ❌ TC duy nhất chưa chạy → `[BLOCKER]` RULE-06 |
| `STATE-DEP-001` | Cao | ◯ ngưỡng lỗi phụ thuộc trạng thái | NEW-23 | 1/1 pass | ✅ OK |
| `JOB-001` ★ | Cao | ◯ **BẮT BUỘC** — gọi API bên thứ 3 theo lô | *(chỉ NEW-27 mang mã `JOB-002` — **không có trong framework** → không tính cover)* | — | ❌ **Chưa cover** → `[BLOCKER]` |
| `ENV-003` ★ | Cao | ◯ **BẮT BUỘC** — job nền | 0 TC chạy staging/production | 19/19 chạy `local` | ❌ `[MAJOR]` RULE-08 |
| `REG-SHARED-001` | Cao | ◯ **BẮT BUỘC** — Dev đã cung cấp danh sách yokoten | *(không TC)* | — | ❌ `[BLOCKER]` |
| `REG-RUN-001` | Cao | ◯ job đang chạy dở khi release | NEW-31 (một phần) | **skip** | ❌ `[MAJOR]` |
| `COMPAT-LEGACY-001` ★ | Cao | ◯ tồn tại **2 phiên bản job** (linect-service + artisan cũ, F4) | *(không TC nào phân biệt phiên bản job)* | — | ❌ `[MAJOR]` RULE-09 |
| `SEC-002` | Cao | ◯ xử lý API token Chatwork | NEW-15, NEW-17, NEW-2 (expected có ràng buộc "không lộ token") | 3/3 pass | ⚠️ Chưa quét **server log** / console → `[NIT]` |
| `DATA-MIG-001` | Cao | ✗ không đổi cấu trúc dữ liệu | — | — | × không áp dụng |
| `INTG-HOOK-001/002` | Cao/TB | ✗ Chatwork gọi đi, không nhận webhook | — | — | × không áp dụng |
| `DATA-AUDIT-001` | Cao | ✗ `mobile_notify` không thuộc nhóm dữ liệu nhạy cảm | — | — | × không áp dụng |
| `MEDIA-*` / `PAY-*` / `LIFF-*` | — | ✗ | — | — | × không áp dụng |

**Quan điểm ưu tiên Cao chưa cover**: `JOB-001` · `REG-SHARED-001` · `MSG-004` (có TC nhưng chưa chạy) · `CONC-001` (thiếu 2/4 kịch bản) · `REG-RUN-001` · `COMPAT-LEGACY-001` · `ENV-003`.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] RULE-06 / MSG-004` — Không một kết quả Đạt nào từng mở phòng Chatwork thật**
Bug KH báo là *"Chatwork gửi hàng loạt thông báo của sự kiện trước khi liên kết"*. 17/17 TC `pass` đều dừng ở oracle tầng dữ liệu (`mobile_notify.status_chat_work` = 1). Hai TC quan sát phòng Chatwork thật — `NEW-27` (không nhận tin cũ) và `NEW-28` (vẫn nhận tin mới) — **đều chưa chạy**. Đánh dấu bản ghi "đã gửi" trong DB **không chứng minh** phòng chat không nhận tin: job có thể đã đọc hàng chờ trước khi lệnh dọn hoàn tất (đúng rủi ro `NEW-31` mô tả).
→ **Fix**: chạy `NEW-27` + `NEW-28` trên **staging**, đính kèm ảnh chụp phòng Chatwork trước/sau + log job. Không chấp nhận kết quả suy từ cột DB.

**`[BLOCKER] FIX-SHAPE: REG-SHARED-001` — Dev đã đưa danh sách yokoten, TCs bỏ trắng cả 2**
Mục 2 `03-dev-impact.md` ghi rõ: *"Yokoten: 2 chỗ cùng họ chưa sửa (bật lại công tắc thông báo Chatwork và lệnh recover khôi phục URL phòng chat cho admin)"* → tương ứng **F3** (`saveNotifySettingReceive`/`saveNotifySettings`) và **F6** (`RecoverNotifySettingCloneStaff`). Cả hai đều **0 TC**. Studio cũng đã khai `REQ-012` cho luồng bật lại công tắc nhưng không sinh TC nào.
Đáng lo hơn: `feature-spec.md` **BR-04** cho biết luồng bật lại công tắc **đã có sẵn** cơ chế mark-done tương tự (`saveNotifySettingReceive` dòng 196-201) — tức là hai luồng chạy **hai đoạn code khác nhau cho cùng một mục đích**, và chỉ một trong hai vừa được vá. Bug này đã re-open 2 lần vì bỏ sót nhánh; đây là ứng viên nhánh thứ ba.
→ **Fix**: bổ sung `TC-REGSHARED001-01` và `-02` (§5). Đồng thời hỏi Dev: BR-04 có thật sự đang chạy đúng ở nhánh create của luồng công tắc không?

**`[BLOCKER] FIX-SHAPE: CONC-001` — Thiếu 2/4 kịch bản bắt buộc, trong đó có đúng kịch bản Dev tự khai là rủi ro**
`CONC-001` yêu cầu 4 kịch bản. Hiện có (1) double-click = `NEW-13` và (4) batch = `NEW-31` (`skip`). **Thiếu (2)** cùng user trên 2 tab/2 thiết bị và **thiếu (3) 2 user khác nhau thao tác gần đồng thời**.
Kịch bản (3) chính là rủi ro **Dev tự nêu** ở §TỰ REVIEW: *"nếu bot có nhiều người (admin + nhân viên) cùng liên kết Chatwork, người liên kết sau sẽ dọn luôn hàng chờ chưa gửi của người trước"*. Studio đã khai thành `REQ-009` với chỉ dẫn *"cần ghi nhận hành vi thực tế và chuyển cho PO xác nhận"* — nhưng **không TC nào được sinh cho `REQ-009`**.
→ **Fix**: `TC-CONC001-01/-02/-03` (§5). Kết quả phải đưa PO chốt, không tự kết luận Đạt/Không đạt.

**`[BLOCKER] JOB-001` — Quan điểm Cao bắt buộc, hoàn toàn chưa cover**
Task chạm job nền gọi **Chatwork API v2 theo lô** (`job-spec.md`: gom toàn bộ pending thành 1 message rồi POST). `JOB-001` là **BẮT BUỘC**. TC duy nhất chạm tầng job mang mã `JOB-002` — **không tồn tại trong `checklist-lme.md`** → theo mục 0.6 #6 không được tính là cover.
Nội dung `JOB-001` chưa ai kiểm: (a) **số bản ghi vào = xử lý thành công + hàng đợi lỗi, không bản ghi nào biến mất** — bản vá cố tình đánh dấu "đã gửi" cho bản ghi **chưa từng được gửi**, đây đúng là tình huống bản ghi "biến mất" cần có sổ cân bằng; (b) rate limit 429 (`job-spec.md` bước viii `sleep 1 giây`) với hàng chờ lớn; (c) lỗi 403 → job mark done + bỏ qua (bước vii) → sau khi liên kết bằng token sai, thông báo mới cũng mất im lặng.
→ **Fix**: `TC-JOB001-01/-02` (§5). Đổi nhãn `NEW-27` từ `JOB-002` sang `JOB-001` trên Studio.

**`[BLOCKER] NEW-7` — TC bảo vệ kịch bản re-open có tiền đề tự hỏng, chạy tự động trên local, không có evidence**
`NEW-7` là TC **trọng tâm chống tái re-open** (nhánh `create` — đúng "trường hợp đầu tiên" bị re-open 2026-08-20). Chính note của TC cảnh báo: *"màn 「通知設定」 có hành vi tự tạo bản ghi mặc định khi mở, nên đi qua màn đó sẽ làm hỏng tiền điều kiện và biến TC này thành trùng với TC nhánh đã có bản ghi"* — khớp với **BR-02 Auto-create settings** trong spec.
Nghĩa là: nếu tiền đề bị hỏng, `NEW-7` **vẫn `pass`** nhưng thực chất chỉ chạy lại `NEW-6`, và nhánh từng làm bug re-open **không được test** — mà không ai biết. TC này chạy `exec_mode = auto` bởi AI pipeline trên `local`, cột `Evidence thực tế` rỗng.
→ **Fix**: chạy lại `NEW-7` **thủ công**, bắt buộc đính kèm bằng chứng **trước khi lưu** rằng không tồn tại bản ghi `notify_setting` cho cặp bot+user, và bằng chứng **sau khi lưu** rằng bản ghi được **tạo mới** (không phải update). Không có 2 bằng chứng này thì không được tick Đạt.

### 4.2 Major (nên fix)

**`[MAJOR]` Kết quả thực thi 73,9% < 80%** — 6/23 TC không có kết luận test (4 chưa chạy, 1 skip, 1 fail). Coverage ở §3 chỉ là *trên giấy* cho các impact tương ứng.

**`[MAJOR] RULE-08 / ENV-003` — 100% kết quả đến từ `env = local`** — Staging 0, Production 0. Task chạm **job nền** → `ENV-003` cấm kết luận từ local/staging, và bug gốc được KH báo trên **Staging**. Đặc biệt vô lý: 4 TC nhóm job khai `env_scope = dev|staging` nhưng chưa chạy ở đâu cả, còn `NEW-31` khai `env_scope = local` cho một TC race cần job thật.
→ Tối thiểu chạy lại toàn bộ 5 TC job + `NEW-6`/`NEW-7` trên **staging**.

**`[MAJOR]` 17 kết quả Đạt đều do **AI pipeline** tự chạy** (`last_exec.source = ai`) — không có lượt QA người chạy tay nào. Nhóm rủi ro cao (liên kết lần đầu, dọn hàng chờ) cần ít nhất 1 lượt người chạy + evidence.

**`[MAJOR]` 22/23 TC do AI sinh, 0 TC do member viết, `reviewed = false`** — bộ TC chưa qua vòng người duyệt nào trước khi tới Leader.

**`[MAJOR] NEW-3` đang `fail` với ticket #40476** — `PERM-002` (quan điểm Cao) chưa có kết luận. Phải chốt #40476 trước khi đóng #38535; nếu #40476 xác nhận endpoint gọi được không cần phiên đăng nhập thì lệnh dọn hàng chờ hàng loạt có thể bị kích hoạt từ ngoài — nghiêm trọng hơn bug gốc.

**`[MAJOR] RULE-01 / FUNC-003` — thiếu loại case Boundary** — `FUNC-003` được nâng lên **Cao** vì field là URL. Hiện có Normal (`NEW-6`) + Abnormal (`NEW-15`, `NEW-17`) nhưng **không có Boundary**, và không ghi lý do. Thiếu: URL độ dài biên, `rid` cực lớn / bằng 0 / âm, URL có khoảng trắng đầu-cuối (chỉ được nhắc thoáng ở `NEW-16`), URL sub-domain hợp lệ của chatwork.com.

**`[MAJOR] COMPAT-LEGACY-001 / RULE-09` — 2 phiên bản job cùng tồn tại, không TC nào phân biệt** — `03-dev-impact.md` F4 ghi rõ job có **2 bản**: `HandlePushNotifyChatwork` ở `linect-service` **và bản artisan cũ** ở `app/Console/Commands` ("cùng logic"). Không TC nào xác định môi trường test đang chạy bản nào. Nếu staging chạy bản artisan cũ còn production chạy linect-service (hoặc ngược lại), kết quả test không chuyển được sang môi trường kia.
→ Hỏi Dev: môi trường nào chạy bản nào? Bản artisan cũ còn được bật không?

**`[MAJOR] REG-RUN-001` — không có TC cho job đang chạy dở lúc deploy** — `NEW-31` chạm một phần nhưng đang `skip`. Kịch bản thật: deploy bản vá trong lúc hàng chờ đang có bản ghi và job đang giữa chu kỳ quét.

**`[MAJOR] GAP D2b` — `next_notify_chat_work_time` không được bản vá đặt lại và không TC nào kiểm** — `job-spec.md` dòng 273 cho thấy **cổng vào** của job là `next_notify_chat_work_time IS NULL OR <= now()`, còn `last_notify_chat_work_time` chỉ dùng ở bước (c) để tính `timeSchedule`. Bản vá (D2/D3) chỉ chạm `last_notify_chat_work_time` + `chat_work_total_msg_error`. Không TC nào ghi nhận `next_notify_chat_work_time` sau khi liên kết.

**`[MAJOR] REQ-013 chưa có TC — và bộ TC hiện tại về mặt cấu trúc KHÔNG THỂ phát hiện** — Studio khai `REQ-013`: *"đặt lại mốc gửi có thể làm thông báo hợp lệ đầu tiên sau khi liên kết bị lùi thêm đúng một chu kỳ tần suất"*. **Toàn bộ** TC nhóm job đều ghim tần suất `「リアルタイム」`; với realtime, `interval = 0` nên độ trễ luôn bằng 0 và **không bao giờ quan sát được**. Muốn thấy được phải test với tần suất theo lịch (15 phút / 1 giờ).

**`[MAJOR] AP-3` — `T2` (FA-028 Delivery Error List) chỉ có 1 TC quan sát được và TC đó chưa chạy** — `NEW-29`. Không có TC nào mở **màn Delivery Error List** để đối chiếu con số người dùng thật sự nhìn thấy với `chat_work_total_msg_error` đã chụp.

**`[MAJOR] AP-4` — không có link PR** — `03-dev-impact.md` chỉ có commit hash `5fa27b7ca8` + link dashboard nội bộ, không có link Github/Gitlab. Không review được diff để xác nhận điều kiện `isFirstLink` là `empty(notification_room_url)` như TC giả định.

**`[MAJOR]` Checkbox "Tester verify auto-fill chính xác" **chưa tick** ở cả `01-bug-task.md` và `03-dev-impact.md`** — cả hai file `Auto-filled: 2026-09-03 by /new-task`. Riêng `§4.1` đáng ngờ: báo cáo Dev **chỉ ghi tên file**, bảng F1–F6 do `/new-task` map từ §3 chứ không phải Dev viết. Review coverage dựa trên bảng chưa ai xác nhận.

**`[MAJOR] DATA-DB-001` — thiếu vế "2 staff cùng 1 bot"** — `NEW-21` đã kiểm `WHERE` scope trên **2 bot** (tốt), nhưng `DATA-DB-001` yêu cầu tạo bản ghi trùng ở **2 tài khoản (2 bot, 2 staff)**. Vế 2 staff trùng đúng với `REQ-009` chưa có TC.

**`[MAJOR] NEW-14` — `Kết quả mong đợi` chứa ràng buộc mà `Các bước thực hiện` không kiểm được** — Expected của `NEW-14` kết thúc bằng: *"Sau khi đổi URL, 4 thông báo này vẫn phải được gửi vào phòng chat B."* Nhưng 6 bước của TC dừng ở *"Đối chiếu lại trạng thái 4 thông báo, mốc gửi ChatWork gần nhất và ngưỡng đếm lỗi gửi tin"* — **không có bước nào mở phòng chat B**, cũng không có bước chờ job. Vế cuối của expected chưa từng được kiểm, nhưng TC vẫn được tick `pass`.
→ **Fix**: hoặc bổ sung 2 bước (chờ job chạy 2 chu kỳ → mở phòng B đối chiếu 4 tin), hoặc cắt vế đó khỏi expected và chuyển sang TC nhóm job. Rà lại các TC còn lại theo cùng tiêu chí: expected chỉ được chứa thứ steps kiểm được.

> Đã rà máy toàn bộ 23 TC: **không một TC `pass` nào** có bước mở phòng Chatwork hoặc đọc nhật ký job. 4 TC có bước đó (`NEW-27`, `NEW-28`, `NEW-29`, `NEW-31`) đều chưa chạy hoặc `skip`. Đây là bằng chứng máy cho `[BLOCKER] RULE-06` ở §4.1.

### 4.3 Minor (có thể fix sau)

**`[MINOR]` 5 mã quan điểm ngoài framework** (`TOOL-NEGCTRL-001`, `TOOL-KNOW-002`, `API-CONTRACT-001`, `TOOL-ERRHYG-001`, `JOB-002`) — 9/23 TC. Đề nghị map lại: `TOOL-KNOW-002`→`FUNC-001`, `TOOL-NEGCTRL-001`→`DATA-DB-001`, `API-CONTRACT-001`→`FUNC-001`, `TOOL-ERRHYG-001`→`SEC-002`, `JOB-002`→`JOB-001`.

**`[MINOR]` `TC No.` không theo format repo** — Studio dùng `temp_id` dạng `NEW-6`, `NEW-27`; chuẩn repo là `TC-<mã quan điểm bỏ gạch>-<nn>`. Không chặn review, nhưng khiến map coverage phải làm tay.

**`[MINOR]` Cột `Evidence thực tế` rỗng ở toàn bộ 23 TC** — `testcase_list` không trả về trường này. Với 17 TC đã `pass`, RULE-02 yêu cầu evidence đúng loại. Cần lấy từ `task_get_report` hoặc yêu cầu người chạy bổ sung.

**`[MINOR]` `Trạng thái đánh giá spec` (`spec_status`) null ở toàn bộ 23 TC** — không TC nào khai `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Với 2 xung đột spec ở §6, đây là chỗ đáng lẽ phải được đánh dấu.

**`[MINOR]` `NEW-31` khai `env_scope = local`** — TC race cần job thật chạy; khai local mâu thuẫn với `ENV-003`. Nên đổi sang `staging`.

### 4.4 Nit (gợi ý)

**`[NIT] SEC-002`** — expected của `NEW-15`/`NEW-17`/`NEW-2` có ràng buộc "không lộ token", tốt. Bổ sung bước quét **server log** + console DevTools cho đủ `Kiểm tra` của SEC-002. Ghi chú: spec `logic-spec.md` đã đánh dấu **EP-12 trả `api_token` trong response** là rủi ro bảo mật sẵn có — ngoài phạm vi ticket này, nhưng đáng mở ticket riêng.

**`[NIT]`** `NEW-17` có note rất tốt về bẫy phân loại (mất mạng cũng cho ra đúng thông báo lỗi 「アクセス権限がありません」). Nên nâng thành **quy tắc chung của lượt chạy**: mọi lượt chạy phải có ≥ 1 TC luồng chính lưu thành công thì kết quả các TC Abnormal mới có giá trị.

**`[NIT]`** Theo `RULE-05`, nên tra tài liệu Chatwork API v2 mới nhất để lấy rate limit hiện hành trước khi chạy `TC-JOB001-02`.

---

## 4.5 TC trùng lặp nội dung

Đã rà **toàn bộ 23 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`).

**Không có `DUP-EXACT`, không có `DUP-INFLATE`, không có `DUP-CONFLICT`.**

Phát hiện **2 cặp gần trùng** — cả hai đều **KHÔNG đề nghị xóa**:

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Chặn URL sai định dạng | `NEW-15` (UI) | `NEW-2` (API) — **giữ cả hai**, không gộp | `DUP-SUBSET` (một phần) | Cùng `Abnormal`; cùng đối tượng "URL sai định dạng"; tiền đề tương đương (3 thông báo chờ). **Khác**: mã quan điểm (`FUNC-003` vs `TOOL-ERRHYG-001`), tầng kích hoạt (form UI vs gọi endpoint), và `NEW-2` kiểm thêm 2 thứ `NEW-15` không có: thiếu hẳn tham số, và phản hồi không lộ stack trace/đường dẫn mã nguồn. | `[MINOR]` |
| Chặn URL trùng phòng chat cùng bot | `NEW-16` (UI) | `NEW-5` (API) — **giữ cả hai**, không gộp | `DUP-SUBSET` | Cùng `FUNC-UNIQ-001`; cùng `Abnormal`; cùng đối tượng + thao tác; tiền đề tương đương (admin đã liên kết phòng A, nhân viên thử phòng A). **Khác**: tầng kích hoạt UI vs API; `NEW-16` kiểm thêm biến thể khoảng trắng đầu-cuối. | `[MINOR]` |

**Gate kiểm tra trước khi đề nghị xóa** — đã chạy lại BƯỚC 2 + 3.6 trên giả định xóa:
- Xóa `NEW-2` → `SEC-002`/vệ sinh phản hồi API mất cover, và nhánh "thiếu hẳn tham số" không còn TC nào → **đổi sang giữ**.
- Xóa `NEW-5` → `FUNC-UNIQ-001` mất vế tầng API → **đổi sang giữ**.

**Cặp KHÔNG phải trùng** (ghi lại để Leader khỏi rà lại):
- `NEW-13` (UI bấm lưu 2 lần) vs `NEW-4` (API gọi lặp 3 lần): khác `Loại case` (Abnormal vs Normal) và khác tiền đề (`NEW-13` = chưa liên kết → liên kết lần đầu rồi lưu lại; `NEW-4` = **đã** liên kết sẵn). Hai TC kiểm hai điều kiện `isFirstLink` khác nhau.
- `NEW-31` vs `NEW-33`: cùng `CONC-001`/`Boundary`/nhóm job nhưng **oracle ngược nhau** — `NEW-31` hỏi *"job có đọc hàng chờ trước khi lệnh dọn xong không"*, `NEW-33` hỏi *"lệnh dọn có nuốt sự kiện mới không"*.
- `NEW-6` vs `NEW-7`: khác nhánh code (`update` vs `create`). ⚠️ Chúng **trở thành trùng** nếu tiền đề `NEW-7` bị hỏng — xem `[BLOCKER] NEW-7` ở §4.1.
- `NEW-21` / `NEW-22` / `NEW-24`: cùng là đối chứng âm nhưng khác trục (bot khác / cột kênh khác / bản ghi đã gửi sẵn). Bộ 3 này viết rất chắc.

---

## 5. TCs đề xuất bổ sung

> **Đối chiếu kho TCs**: `ls kho-tcs/*.md` → kho **CHƯA có** `FA-006` (Notification Settings) lẫn `FA-028` (Delivery Error List). Không đối chiếu được TC cũ, không dẫn chiếu được `<ID kho>`. Đề nghị Leader cho chạy `/collect-tcs` cho FA-006 sau ticket này.
>
> **Chống trùng**: Đã đối chiếu **23 TC ở BƯỚC 0** + toàn bộ TC đề xuất với nhau — không TC đề xuất nào trùng theo 4 yếu tố. `GAP-5` (RULE-06) **cố ý không sinh TC mới** vì `NEW-27`/`NEW-28` đã cover đúng, chỉ cần **chạy** — đã chuyển thành issue ở §4.1.

### Trạng thái push lên Studio

**Đã push 4/12 TC** lên Studio task **#221** ngày **2026-09-04** (`testcase_create`, `client_ref` = `ID` → idempotent):

| ID (`client_ref`) | Studio `id` | `temp_id` |
|---|---|---|
| `TC-CONC001-03` | 15883 | `NEW-34` |
| `TC-REGSHARED001-01` | 15884 | `NEW-35` |
| `TC-REGSHARED001-02` | 15885 | `NEW-36` |
| `TC-JOB001-03` | 15886 | `NEW-37` |

**Chưa push (8 TC)**: `TC-CONC001-01` · `TC-CONC001-02` · `TC-REGSHARED001-03` · `TC-JOB001-01` · `TC-JOB001-02` · `TC-STATEDEP001-01` · `TC-COMPATLEGACY001-01` · `TC-DATACOUNT001-01`.

> ⚠️ Lưu ý khi đọc coverage sau lần push này: 4 TC vừa thêm ở trạng thái **draft, chưa chạy** → **chưa** làm thay đổi kết luận nào ở §1/§3/§3.6. Riêng `TC-JOB001-03` (`JOB-001`) mới chỉ lấp **một phần** BLOCKER `JOB-001` — phần "sổ cân bằng bản ghi vào/ra" và "rate limit 429" vẫn nằm ở `TC-JOB001-01`/`-02` chưa push.
> ⚠️ 3 TC còn thiếu của GAP-1 và GAP-3 (`TC-CONC001-01`, `TC-CONC001-02`, `TC-REGSHARED001-03`) chính là các TC gắn với **`REQ-009`** và **yokoten `RecoverNotifySettingCloneStaff`** — 2 BLOCKER `CONC-001` và `REG-SHARED-001` **chưa được gỡ**.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `TC-CONC001-01` | UI | `CONC-001` | Liên kết ChatWork | Normal | manual | staging | Admin liên kết trước, nhân viên liên kết sau trên cùng bot — ghi nhận hàng chờ của admin | - Bot đích bật kênh ChatWork, tần suất `「リアルタイム」`<br>- Có 1 tài khoản admin và 1 tài khoản nhân viên cùng quyền vào màn cài đặt thông báo<br>- Cả hai **chưa** liên kết phòng chat nào<br>- Có 2 phòng Chatwork thật (phòng A cho admin, phòng B cho nhân viên), token có quyền vào cả hai | 1. Dựng 4 thông báo đang chờ gửi ChatWork cho bot, ghi lại mã + thời điểm tạo của từng cái<br>2. Đăng nhập admin → mở màn liên kết ChatWork → lưu URL phòng A<br>3. Xác nhận màn báo thành công; ghi lại trạng thái 4 thông báo<br>4. Dựng thêm 3 thông báo mới cho bot, ghi lại mã<br>5. Mở phòng A, ghi lại tin nhắn cuối cùng<br>6. Đăng xuất, đăng nhập bằng nhân viên → mở màn liên kết ChatWork → lưu URL phòng B<br>7. Ghi lại trạng thái 3 thông báo ở bước 4 **ngay sau** khi nhân viên lưu<br>8. Chờ job chạy qua ít nhất 2 chu kỳ quét<br>9. Mở phòng A và phòng B, ghi lại toàn bộ tin nhận được ở mỗi phòng | 4 thông báo trước lần liên kết của admin; 3 thông báo phát sinh giữa 2 lần liên kết. Phòng A ≠ phòng B. | Ghi nhận **hành vi thực tế**, chưa chốt Đạt/Không đạt:<br>1. 4 thông báo ban đầu → đã gửi, phòng A **không** nhận tin cũ nào<br>2. Trạng thái 3 thông báo ở bước 4 sau khi nhân viên lưu: ghi rõ **đã gửi** hay **còn chờ**<br>3. Phòng A có nhận được 3 thông báo đó không — ghi rõ **có / không** kèm ảnh chụp<br>4. Nếu 3 thông báo bị đánh dấu đã gửi mà phòng A chưa từng nhận → **đây là mất thông báo hợp lệ của admin**, ghi rõ số lượng mất | | Lấp GAP-1 · cover impact F2, D1 · kịch bản (3) của CONC-001 · **Đánh giá spec: Spec không ghi (Studio khai `REQ-009`, Dev nêu ở §TỰ REVIEW — cần PO chốt)** · Evidence: ảnh chụp 2 phòng Chatwork + bảng trạng thái từng mã thông báo trước/sau · **KHÔNG tự kết luận Đạt — đưa PO xác nhận** |
| `TC-CONC001-02` | UI | `CONC-001` | Liên kết ChatWork | Abnormal | manual | staging | Admin và nhân viên bấm lưu URL gần đồng thời trên cùng bot | - Như `TC-CONC001-01`<br>- Chuẩn bị 2 trình duyệt/2 thiết bị, mỗi bên đăng nhập sẵn 1 tài khoản, cùng mở màn liên kết ChatWork của **cùng một bot**<br>- Dựng sẵn 5 thông báo đang chờ gửi ChatWork | 1. Ghi lại mã + trạng thái của 5 thông báo<br>2. Bên admin nhập URL phòng A, bên nhân viên nhập URL phòng B — **chưa bấm lưu**<br>3. Đếm 3-2-1 rồi bấm lưu ở cả hai bên trong vòng 1 giây<br>4. Ghi lại thông báo trên màn của từng bên<br>5. Đối chiếu URL đã lưu của từng tài khoản<br>6. Ghi lại trạng thái 5 thông báo và mốc gửi ChatWork gần nhất của từng cấu hình<br>7. Lặp lại toàn bộ 3 lần | 5 thông báo chờ gửi. Hai URL phòng chat khác nhau, lưu gần đồng thời. Lặp 3 lần. | Hệ thống **không được âm thầm xử lý trùng**: cả hai lần lưu đều báo kết quả rõ ràng (thành công hoặc báo xung đột), URL của mỗi tài khoản đúng như bên đó nhập. 5 thông báo **không được bị dọn 2 lần** gây lệch số. Ghi rõ ở mỗi lần thử: mấy bản ghi bị đánh dấu đã gửi, mốc gửi gần nhất của mỗi cấu hình. Không được xảy ra trường hợp một bên báo thành công nhưng URL lưu ra là của bên kia. | | Lấp GAP-1 · cover impact F1, F2, D2 · kịch bản (3) CONC-001 · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: quay màn hình 2 thiết bị + log DB trước/sau mỗi lần thử |
| `TC-CONC001-03` | UI | `CONC-001` | Liên kết ChatWork | Boundary | manual | staging | Cùng một admin lưu URL từ 2 tab trình duyệt song song | - Bot đích bật kênh ChatWork, **chưa** liên kết phòng chat<br>- Một tài khoản admin đăng nhập, mở **2 tab** cùng màn liên kết ChatWork<br>- Dựng 4 thông báo đang chờ gửi ChatWork | 1. Ghi lại mã + trạng thái 4 thông báo và mốc gửi ChatWork gần nhất<br>2. Tab 1 nhập URL phòng A, tab 2 nhập URL phòng B<br>3. Bấm lưu ở tab 1, ngay lập tức (trong 1 giây) bấm lưu ở tab 2<br>4. Tải lại cả 2 tab, ghi lại URL hiển thị ở mỗi tab<br>5. Ghi lại trạng thái 4 thông báo và mốc gửi ChatWork gần nhất<br>6. Chờ job chạy qua 2 chu kỳ, mở cả phòng A và phòng B ghi lại tin nhận được | 4 thông báo chờ gửi. Tab 1 = phòng A, tab 2 = phòng B, lưu cách nhau dưới 1 giây. | Chỉ **một** URL cuối cùng được lưu và cả 2 tab sau khi tải lại đều hiển thị **cùng một URL** đó. 4 thông báo chuyển sang đã gửi đúng **một lần**, mốc gửi ChatWork gần nhất chỉ bị đặt lại **một lần**. Không phòng nào (A hay B) nhận được thông báo cũ. Không có bản ghi nào bị bỏ sót hoặc bị xử lý hai lần. | | Lấp GAP-1 · cover impact F1, F2, D1, D2 · kịch bản (2) CONC-001 · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: ảnh chụp 2 tab sau reload + query trạng thái 4 mã thông báo |
| `TC-REGSHARED001-01` | UI | `REG-SHARED-001` | Bật/tắt công tắc kênh ChatWork | Normal | manual | staging | Tắt rồi bật lại công tắc ChatWork khi bot ĐÃ liên kết — thông báo cũ không bị bắn bù | - Bot đích **đã liên kết** phòng chat, kênh ChatWork đang **BẬT**, tần suất `「リアルタイム」`<br>- Có phòng Chatwork thật quan sát được<br>- Job gửi thông báo ChatWork đang chạy | 1. Mở màn 「通知設定」, **TẮT** công tắc kênh ChatWork, lưu<br>2. Dựng 5 sự kiện làm phát sinh thông báo cho bot, ghi lại mã từng cái<br>3. Ghi lại tin nhắn cuối cùng trong phòng chat đích<br>4. **BẬT** lại công tắc kênh ChatWork, lưu<br>5. Ghi lại trạng thái 5 thông báo ngay sau khi bật<br>6. Chờ job chạy qua ít nhất 2 chu kỳ quét<br>7. Mở phòng chat đích, ghi lại toàn bộ tin nhận được | 5 thông báo phát sinh trong lúc kênh ChatWork đang tắt. Tần suất `「リアルタイム」`. | Sau khi bật lại công tắc: 5 thông báo phát sinh lúc kênh đang tắt chuyển sang **đã gửi**, phòng chat **KHÔNG** nhận tin nào chứa 5 thông báo đó. Hành vi phải **giống hệt** luồng liên kết lần đầu đã được vá. Nếu phòng chat nhận được loạt tin cũ → **bug tương tự #38535 vẫn tồn tại ở luồng công tắc** (đúng yokoten Dev khai chưa sửa), raise ticket riêng. | | Lấp GAP-2 · cover impact **F3** (yokoten chưa sửa) · **Đánh giá spec: Spec ghi rõ — `feature-spec.md` BR-04 mô tả luồng này đã có mark-done sẵn** · Evidence: ảnh chụp phòng Chatwork trước/sau + trạng thái 5 mã thông báo · regression |
| `TC-REGSHARED001-02` | UI | `REG-SHARED-001` | Bật/tắt công tắc kênh ChatWork | Abnormal | manual | staging | Bật công tắc ChatWork khi người dùng CHƯA có bản ghi cấu hình — nhánh create của luồng công tắc | - Dùng tài khoản **chưa từng** có bản ghi cấu hình thông báo cho bot đích (kiểm ở tầng dữ liệu, không suy từ giao diện)<br>- Bot đích đã có URL phòng chat được người khác liên kết, phòng chat quan sát được<br>- Dựng 4 thông báo đang chờ gửi ChatWork | 1. Kiểm và ghi lại bằng chứng **chưa tồn tại** bản ghi cấu hình cho cặp bot + người dùng này<br>2. Ghi lại mã + trạng thái 4 thông báo và tin cuối trong phòng chat<br>3. Đăng nhập tài khoản đó, mở màn 「通知設定」<br>4. Bật công tắc kênh ChatWork và lưu<br>5. Ghi lại bản ghi cấu hình vừa được tạo và trạng thái 4 thông báo<br>6. Chờ job chạy qua 2 chu kỳ, mở phòng chat ghi lại tin nhận được | Tài khoản chưa có bản ghi cấu hình. 4 thông báo chờ gửi ChatWork. | Bản ghi cấu hình mới được tạo. 4 thông báo chuyển sang **đã gửi**, phòng chat **KHÔNG** nhận tin cũ nào. Đây là nhánh `create` của luồng công tắc — **cùng dạng nhánh đã làm #38535 bị re-open ngày 20/08 ở luồng liên kết**. Nếu phòng chat nhận loạt tin cũ → nhánh create của luồng công tắc chưa được vá, raise ticket riêng và đối chiếu với `NEW-7`. | | Lấp GAP-2 · cover impact **F3** · Đánh giá spec: Spec ghi rõ (BR-02 auto-create + BR-04 mark-done) · Evidence: bằng chứng trước/sau ở tầng dữ liệu + ảnh phòng Chatwork · regression |
| `TC-REGSHARED001-03` | Data | `REG-SHARED-001` | Lệnh khôi phục cấu hình admin/nhân viên | Normal | manual | staging | Chạy lệnh recover khôi phục URL phòng chat — thông báo cũ không bị bắn bù | - Bot đích có cấu hình thông báo của admin **đã từng** có URL phòng chat rồi bị xoá/mất (đúng tình huống lệnh recover xử lý)<br>- Kênh ChatWork đang bật, phòng chat quan sát được<br>- Cần Dev hoặc hạ tầng hỗ trợ chạy lệnh `RecoverNotifySettingCloneStaff`<br>- Dựng 4 thông báo đang chờ gửi ChatWork | 1. Ghi lại mã + trạng thái 4 thông báo và tin cuối trong phòng chat<br>2. Xác nhận cấu hình của admin đang **không** có URL phòng chat<br>3. Nhờ Dev chạy lệnh recover khôi phục URL phòng chat cho admin<br>4. Ghi lại URL phòng chat sau khi recover và trạng thái 4 thông báo<br>5. Chờ job chạy qua ít nhất 2 chu kỳ quét<br>6. Mở phòng chat, ghi lại toàn bộ tin nhận được | 4 thông báo chờ gửi ChatWork phát sinh trong lúc URL đang trống. | URL phòng chat được khôi phục. Câu hỏi cần trả lời: phòng chat **có nhận loạt 4 thông báo cũ không**. Ghi rõ **có / không** kèm ảnh chụp và số tin nhận được. Vì lệnh recover cũng đưa bot từ trạng thái chưa liên kết sang đã liên kết mà **không đi qua đoạn code vừa vá**, khả năng cao bug tái hiện ở đây — nếu đúng, raise ticket riêng và ghi rõ đây là yokoten Dev đã khai. | | Lấp GAP-3 · cover impact **F6** (yokoten chưa sửa) · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: ảnh phòng Chatwork + log lệnh recover · regression · **cần Dev hỗ trợ chạy lệnh** |
| `TC-JOB001-01` | API | `JOB-001` | Job gửi thông báo ChatWork | Normal | manual | product | Sổ cân bằng bản ghi vào/ra quanh thời điểm liên kết lần đầu | - Bot đích bật kênh ChatWork, **chưa** liên kết phòng chat, tần suất `「リアルタイム」`<br>- Job gửi thông báo ChatWork đang chạy<br>- Phòng chat thật quan sát được<br>- Truy cập được nhật ký job | 1. Dựng 10 thông báo đang chờ gửi ChatWork, ghi lại **danh sách mã đầy đủ**<br>2. Ghi lại tin cuối trong phòng chat<br>3. Liên kết phòng chat qua màn liên kết<br>4. Ngay sau khi lưu, tạo tiếp 5 sự kiện mới, ghi lại **danh sách mã**<br>5. Chờ job chạy qua ít nhất 3 chu kỳ quét<br>6. Lập bảng đối chiếu cho **cả 15 mã**: trạng thái cuối · có xuất hiện trong tin nhắn phòng chat không · có xuất hiện trong nhật ký job không | 10 thông báo trước liên kết + 5 thông báo sau liên kết = 15 mã theo dõi. | Bảng 15 dòng phải khép kín, **không mã nào rơi vào ô trống**:<br>- 10 mã trước liên kết: trạng thái **đã gửi**, **không** xuất hiện trong phòng chat, nhật ký job không có lời gọi gửi cho chúng<br>- 5 mã sau liên kết: trạng thái **đã gửi**, **có** xuất hiện đầy đủ trong tin nhắn phòng chat<br>- Tổng: 15 vào = 10 bỏ qua có chủ đích + 5 gửi thành công + 0 biến mất không giải thích được | | Lấp GAP-7 · cover impact F4, F5, D1 · `JOB-001` mục (4) "không bản ghi nào biến mất" · **RULE-08 → chạy product** · Đánh giá spec: Spec ghi rõ (`job-spec.md` §ChatWork job loop) · Evidence: bảng đối chiếu 15 mã + nhật ký job + ảnh phòng Chatwork |
| `TC-JOB001-02` | API | `JOB-001` | Job gửi thông báo ChatWork | Boundary | manual | product | Hàng chờ lớn ngay sau khi liên kết — job không dừng, không mất bản ghi khi chạm rate limit | - Bot đích bật kênh ChatWork, chưa liên kết phòng chat<br>- Job đang chạy, phòng chat thật quan sát được<br>- Đã tra tài liệu Chatwork API v2 mới nhất lấy rate limit hiện hành (RULE-05), ghi lại con số vào phiếu test | 1. Dựng khoảng 300 thông báo đang chờ gửi ChatWork, ghi lại tổng số<br>2. Liên kết phòng chat qua màn liên kết, ghi lại thời điểm bấm lưu<br>3. Ngay sau khi lưu, tạo liên tục các sự kiện mới **vượt ngưỡng rate limit đã tra** trong vài phút<br>4. Chờ job chạy qua ít nhất 3 chu kỳ quét<br>5. Rà nhật ký job tìm phản hồi 429 và hành vi sau đó<br>6. Đối chiếu tổng số bản ghi vào với số đã gửi thành công + số còn chờ + số vào trạng thái lỗi | ~300 thông báo tồn đọng trước liên kết + luồng sự kiện mới vượt rate limit sau liên kết. | Job **không dừng, không văng exception làm chết vòng lặp**. Khi gặp 429, nhật ký ghi rõ có chờ rồi thử lại (`job-spec.md` bước viii). 300 thông báo cũ **không** vào phòng chat. Thông báo mới **cuối cùng đều được gửi**, không cái nào biến mất im lặng. Tổng bản ghi vào = gửi thành công + còn chờ + lỗi có ghi nhận. | | Lấp GAP-7 · cover impact F4 · `JOB-001` mục (1)(2)(3) · **RULE-05** tra tài liệu Chatwork API trước khi chạy · **RULE-08 → chạy product** · Evidence: nhật ký job có 429 + bảng cân bằng số bản ghi |
| `TC-JOB001-03` | API | `JOB-001` | Job gửi thông báo ChatWork | Abnormal | manual | staging | Sau khi liên kết bằng token không còn quyền — thông báo mới không mất im lặng | - Bot đích bật kênh ChatWork, chưa liên kết phòng chat<br>- Có token Chatwork **hợp lệ lúc liên kết** nhưng sẽ bị thu hồi quyền vào phòng ngay sau đó<br>- Job đang chạy | 1. Dựng 3 thông báo chờ gửi ChatWork, ghi lại mã<br>2. Liên kết phòng chat thành công bằng token còn quyền<br>3. Thu hồi quyền của token vào phòng chat đích (hoặc xoá bot khỏi phòng)<br>4. Tạo 3 sự kiện mới, ghi lại mã<br>5. Chờ job chạy qua ít nhất 3 chu kỳ quét<br>6. Ghi lại trạng thái 3 thông báo mới và nội dung nhật ký job | 3 thông báo trước liên kết + 3 thông báo sau khi token mất quyền. | Job gặp lỗi 403 khi gửi. Theo `job-spec.md` bước vii, job **mark done + cập nhật thời gian** — nghĩa là 3 thông báo mới sẽ chuyển sang **đã gửi dù chưa hề tới phòng chat**. Ghi nhận rõ hành vi này kèm nhật ký. Câu hỏi cho PO/Dev: người dùng có được cảnh báo gì khi liên kết hỏng không, hay thông báo cứ **mất im lặng**? | | Lấp GAP-7 · cover impact F4 · Đánh giá spec: Spec ghi rõ (`job-spec.md` bước vii) nhưng **hành vi mất tin im lặng cần PO xác nhận** → §6 · Evidence: nhật ký job có 403 + trạng thái 3 mã thông báo |
| `TC-STATEDEP001-01` | UI | `STATE-DEP-001` | Liên kết ChatWork | Boundary | manual | staging | Liên kết với tần suất theo lịch (không phải realtime) — đo độ trễ của thông báo hợp lệ đầu tiên | - Bot đích bật kênh ChatWork với tần suất **`「1時間」`** (không dùng realtime)<br>- Chưa liên kết phòng chat<br>- Job đang chạy, phòng chat thật quan sát được | 1. Ghi lại mốc gửi ChatWork gần nhất và thời điểm gửi tiếp theo của bot **trước** khi liên kết<br>2. Dựng 3 thông báo chờ gửi ChatWork<br>3. Liên kết phòng chat, ghi lại **thời điểm chính xác** bấm lưu<br>4. Ghi lại mốc gửi ChatWork gần nhất **và thời điểm gửi tiếp theo** ngay sau khi lưu<br>5. Tạo 1 sự kiện mới, ghi lại thời điểm phát sinh<br>6. Theo dõi phòng chat, ghi lại **thời điểm chính xác** tin chứa sự kiện mới xuất hiện<br>7. Tính độ trễ = thời điểm nhận tin − thời điểm phát sinh sự kiện | Tần suất `「1時間」`. 3 thông báo trước liên kết + 1 sự kiện sau liên kết. | 3 thông báo cũ không vào phòng chat. Sự kiện mới **cuối cùng phải được gửi**. Ghi rõ **con số độ trễ đo được** và so với 1 giờ tần suất đã đặt: nếu độ trễ **vượt quá 1 chu kỳ** thì việc đặt lại mốc gửi đang làm lùi lịch thêm — đưa PO xác nhận có chấp nhận không. Đồng thời ghi lại giá trị **thời điểm gửi tiếp theo** sau khi liên kết: bản vá **không** đặt lại trường này, cần xác nhận nó không làm job bỏ qua chu kỳ. | | Lấp GAP-4 + GAP D2b · cover impact D2, F4 · **Studio `REQ-013` chưa có TC nào; toàn bộ TC job hiện tại ghim `「リアルタイム」` nên về cấu trúc không đo được độ trễ này** · Đánh giá spec: Spec ghi rõ (`job-spec.md` bước c: `timeSchedule = last_notify_chat_work_time + interval`) · Evidence: bảng mốc thời gian trước/sau + ảnh phòng Chatwork có dấu thời gian |
| `TC-COMPATLEGACY001-01` | Data | `COMPAT-LEGACY-001` | Job gửi thông báo ChatWork | Normal | manual | product | Xác định và test đúng phiên bản job đang chạy ở từng môi trường | - Có xác nhận từ Dev/hạ tầng: môi trường nào chạy `HandlePushNotifyChatwork` bản `linect-service`, môi trường nào chạy bản artisan cũ ở `app/Console/Commands`<br>- Bot đích bật kênh ChatWork, chưa liên kết phòng chat<br>- Phòng chat thật quan sát được | 1. Ghi vào phiếu test: môi trường đang test chạy **bản job nào**, lấy từ đâu (xác nhận của Dev / cấu hình / nhật ký)<br>2. Dựng 5 thông báo chờ gửi ChatWork<br>3. Liên kết phòng chat qua màn liên kết<br>4. Chờ job chạy qua ít nhất 2 chu kỳ quét<br>5. Ghi lại tin nhận được trong phòng chat và trạng thái 5 thông báo<br>6. **Lặp lại toàn bộ trên môi trường chạy bản job còn lại** | 5 thông báo trước liên kết. Chạy 2 lượt trên 2 môi trường ứng với 2 bản job. | Cả hai bản job đều cho **cùng kết quả**: phòng chat không nhận thông báo cũ, 5 bản ghi chuyển sang đã gửi. Nếu hai bản cho kết quả khác nhau → kết quả test ở môi trường này **không suy sang môi trường kia được**, phải ghi rõ và raise với Dev. Nếu bản artisan cũ đã bị tắt hoàn toàn → ghi nhận xác nhận đó vào phiếu test, coi như không áp dụng. | | Lấp GAP-6 · cover impact **F4** (03 ghi rõ job có 2 bản "cùng logic") · **RULE-09** cũ & mới song song · **RULE-08 → chạy product** · Đánh giá spec: Spec không ghi (đã hỏi Dev) · Evidence: xác nhận bản job đang chạy + kết quả 2 lượt |
| `TC-DATACOUNT001-01` | UI | `DATA-COUNT-001` | Danh sách lỗi phát hành (FA-028) | Normal | manual | staging | Màn Delivery Error List khớp với ngưỡng lỗi đã chụp lúc liên kết | - Bot đích bật kênh ChatWork, chưa liên kết phòng chat<br>- Bot có sẵn **5 bản ghi lỗi gửi tin chưa xác nhận** và 2 bản ghi lỗi **đã** xác nhận<br>- Truy cập được màn Delivery Error List (FA-028) | 1. Mở màn Delivery Error List, **đếm tay** số lỗi chưa xác nhận đang hiển thị, ghi lại con số<br>2. Ghi lại ngưỡng đếm lỗi gửi tin hiện tại của bot<br>3. Liên kết phòng chat qua màn liên kết<br>4. Ghi lại ngưỡng đếm lỗi gửi tin **sau** khi liên kết<br>5. Mở lại màn Delivery Error List, đếm tay lần nữa<br>6. Tạo 2 lỗi gửi tin mới, đếm tay lại trên màn<br>7. Chờ job chạy 2 chu kỳ, kiểm tra phòng chat có cảnh báo lỗi nào không | 5 lỗi chưa xác nhận + 2 lỗi đã xác nhận trước liên kết; 2 lỗi mới sau liên kết. | Ngưỡng đếm lỗi sau khi liên kết = **5**, đúng bằng số lỗi **chưa xác nhận** đếm tay trên màn (không tính 2 lỗi đã xác nhận, không phải 0). Danh sách lỗi trên màn **không bị thay đổi** bởi thao tác liên kết — vẫn đủ 5 dòng, không dòng nào bị đánh dấu đã xử lý. Sau khi thêm 2 lỗi mới: màn hiện 7, phòng chat nhận cảnh báo cho **phần lỗi mới**, không bắn bù 5 lỗi cũ. | | Lấp GAP-8 · cover impact **T2 (FA-028)**, D3 · `DATA-COUNT-001` đối chiếu màn + dữ liệu + phép đếm tay · bổ sung tầng UI cho `NEW-23`/`NEW-29` vốn chỉ ở tầng dữ liệu/job · Đánh giá spec: Spec ghi rõ (BR-06 error count snapshot) · Evidence: ảnh chụp màn FA-028 ở 3 thời điểm + con số đếm tay |

**Tổng: 12 TC bổ sung** — GAP-1 (3 TC, đủ Normal/Abnormal/Boundary theo RULE-01 vì `CONC-001` ưu tiên Cao) · GAP-2 (2) · GAP-3 (1) · GAP-4 + D2b (1) · GAP-6 (1) · GAP-7 (3) · GAP-8 (1).

---

## 6. Spec update needed

### 6.1 — `[BLOCKER]` Xung đột: `notify_setting` là **1 bản ghi / bot** hay **1 bản ghi / (bot + người dùng)**?

| Nguồn | Khẳng định |
|---|---|
| `spec-features/.../db/db-mapping.md` dòng 42 | *"**Ràng buộc nghiệp vụ**: Mỗi bot chỉ có **1 record** — query luôn dùng `where('bot_id', $botId)->first()`"* |
| `spec-features/.../feature-spec.md` **BR-11** | *"**Mỗi bot 1 record**. Query luôn dùng `WHERE bot_id = ? LIMIT 1`."* — Confidence **Cao** |
| `db-mapping.md` dòng 49 + 628 | `user_id` = *"ID user tạo record (admin user) — set tự động"* → **không** phải khoá tra cứu |
| `03-dev-impact.md` mục 2 (Dev) | *"…vì bản ghi cấu hình tra theo từng người dùng nên nhân viên thường rơi vào nhánh create"* |
| Studio `REQ-002` / `REQ-008` + TC `NEW-7`, `NEW-8` | Tiền đề: *"không tồn tại dòng cài đặt thông báo nào ứng với **cặp bot này và người dùng này**"* |

**Hai bên loại trừ nhau.** Nếu spec đúng (1 bản ghi/bot), thì tiền đề của `NEW-8` **không dựng được** khi admin đã có bản ghi cho bot đó — nhân viên sẽ đọc trúng bản ghi của admin và rơi vào nhánh `update`, không phải `create`; và expected của `NEW-8` (*"một bản ghi cài đặt mới được tạo cho đúng cặp bot và tài khoản nhân viên"*) là **sai chuẩn**. Vậy mà `NEW-8` vẫn `pass` trên local — nghĩa là hoặc spec đã lỗi thời, hoặc kết quả `pass` không đáng tin.

Đây cũng chính là **gốc rễ của `REQ-009`** (dọn chéo admin ↔ nhân viên): câu hỏi "người sau có dọn hàng chờ của người trước không" chỉ có nghĩa nếu mỗi người có bản ghi riêng.

→ **Không tự chọn bên.** Cần Dev xác nhận cardinality thật của `notify_setting`, rồi:
- Nếu **per-bot** → sửa `REQ-002`/`REQ-008` và expected của `NEW-7`/`NEW-8` trên Studio; xem lại kết quả `pass` của 2 TC này.
- Nếu **per-(bot, user)** → cập nhật `db-mapping.md` dòng 42 và **BR-11** trong `feature-spec.md`.

### 6.2 — `[MAJOR]` Xung đột: EP-11 có validate hay không?

| Nguồn | Khẳng định |
|---|---|
| `spec-features/.../web/api-spec.md` EP-11, bảng Request Parameters | `notification_room_url` → cột Validation ghi **"Không có validation"** |
| `spec-features/.../web/logic-spec.md` `ajaxSaveUrlChatWork()` | Luồng xử lý **3 bước**: lấy botId → update URL (hoặc tạo mới) → trả JSON. **Không có** nhánh từ chối nào |
| Studio `REQ-005` + TC `NEW-15`, `NEW-16`, `NEW-17`, `NEW-2`, `NEW-5` | **3 nhánh từ chối** với thông báo lỗi tiếng Nhật cụ thể: 「ChatworkルームURLが正しくありません。」 · 「このチャットワークURLはすでにアカウントに登録済みです。」 · 「指定したChatworkルームへのアクセス権限がありません。」 (dẫn nguồn `NotifySettingController.php:776-819`) |

5 TC (21,7% bộ TC) đang khẳng định hành vi mà spec trong repo nói là **không tồn tại**. Nhiều khả năng `spec-features/` đã lỗi thời so với code hiện tại, nhưng **không được tự kết luận**.
→ Nhờ Dev xác nhận 3 nhánh từ chối có thật trong `ajaxSaveUrlChatWork` không; nếu có → cập nhật `api-spec.md` EP-11 + `logic-spec.md`, đồng thời ghi cả quy ước **lỗi trả HTTP 200 kèm `success: false`** (CC-7) mà `NEW-2` đang dựa vào.

### 6.3 — `[MAJOR]` `REQ-009` — hành vi dọn chéo admin ↔ nhân viên chưa có chuẩn

Dev tự khai ở §TỰ REVIEW: *"người liên kết sau sẽ dọn luôn hàng chờ chưa gửi của người trước (tối đa 1 chu kỳ lịch gửi)"* và cho rằng *"đây đúng theo cách job đang hoạt động"*. Studio khai thành `REQ-009` với chỉ dẫn *"chuyển cho PO xác nhận, không tự chốt là đạt hay không đạt"*.

Hiện **không có dòng spec nào** mô tả hành vi mong đợi khi nhiều người cùng liên kết Chatwork trên 1 bot. `TC-CONC001-01` chỉ ghi nhận hành vi thực tế, không kết luận.
→ **PO phải chốt**: mất tối đa 1 chu kỳ thông báo của người liên kết trước là **chấp nhận được** hay là **bug**. Chốt xong mới bổ sung vào `feature-spec.md` §5 Business Rules.

### 6.4 — `[MAJOR]` `REQ-013` — độ trễ 1 chu kỳ sau khi đặt lại mốc gửi chưa có chuẩn

`job-spec.md` bước (c): `timeSchedule = last_notify_chat_work_time + schedule interval`. Bản vá đặt `last_notify_chat_work_time = thời điểm liên kết` → với tần suất theo lịch, thông báo hợp lệ **đầu tiên** sau khi liên kết bị lùi thêm đúng 1 chu kỳ (tới 24 giờ nếu bot đặt tần suất `「24時間」`).
→ PO xác nhận có chấp nhận không. Nếu không → Dev cần đặt `last_notify_chat_work_time` lùi về `now() - interval` thay vì `now()`. Đo bằng `TC-STATEDEP001-01`.

### 6.5 — `[MAJOR]` Yokoten: `feature-spec.md` **BR-04** cần soát lại sau bản vá

BR-04 hiện ghi: *"Khi bật lại smartphone (DB 0→request 1): UPDATE `mobile_notify.status = 1` cho tất cả records chưa gửi. **Tương tự cho ChatWork (`status_chat_work`)**"* — tức luồng công tắc **đã có sẵn** cơ chế mark-done. Nhưng Dev khai luồng này nằm trong **yokoten chưa sửa**.
→ Làm rõ: BR-04 có bao gồm nhánh `create` (người dùng chưa có bản ghi cấu hình) không? Nếu không, BR-04 đang mô tả thiếu và luồng công tắc còn nguyên bug dạng #38535. Kiểm bằng `TC-REGSHARED001-01/-02`.

### 6.6 — `[MINOR]` Bổ sung `next_notify_chat_work_time` vào mô tả phạm vi bản vá

`03-dev-impact.md` §4.2 liệt kê D1/D2/D3 nhưng không nhắc `next_notify_chat_work_time` — trường **quyết định job có quét bot hay không** (`job-spec.md` dòng 273). Cần Dev xác nhận: bản vá cố ý không chạm trường này, và việc đó không làm job bỏ qua chu kỳ ngay sau khi liên kết.

### 6.7 — `[NIT]` Rủi ro bảo mật sẵn có ngoài phạm vi ticket

`logic-spec.md` `ajaxSaveApiTokenChatWork()` ghi chú: *"API token được trả lại trong response — có thể lộ qua network logs"* (EP-12). Không thuộc phạm vi #38535 nhưng nằm cùng màn liên kết ChatWork.
→ Đề nghị mở ticket riêng theo `SEC-002`.
