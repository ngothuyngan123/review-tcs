<!-- sync-tcs: url=<CHƯA CÓ — user sẽ gửi URL Sheet TC human/master sau> | sheet=<tên tab> | anchor=Main Function -->

# 04 — TC List (do member viết)

> Draft sinh bởi `/write-tc` từ `01-bug-task.md` + `03-dev-impact.md` (Redmine #36768). **Member phải verify lại từng TC + điền data thật trước khi submit cho Leader.**
>
> ⚠️ **Sync target CHƯA có URL** — trước khi chạy `/sync-ai-tc`, điền `url=` + `sheet=` ở dòng `sync-tcs` đầu file (user sẽ gửi sau).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | `<member điền>` |

Bot test (Staging): 【マーケ】エルメ `@281qduvu` (basicId) — Premium ID `@lmessage`. Cần thêm **1 bot KHÔNG có premiumId** để test fallback.

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Header (v2 basic) — bot có premiumId → hiển thị premiumId thay vì basicId (Spec 1, displayLineId) | Positive | High | Login bot có premium_id (`@lmessage`) trên Staging | 1. Login vào bot `@lmessage`<br>2. Mở header → popup thông tin bot / QR<br>3. Xem field "LINE ID" | Field LINE ID hiển thị `@lmessage` (premiumId), KHÔNG hiển thị basicId `@281qduvu` | | | |
| TC002 | Header (admin) — copy LINE ID trả về premiumId (premium-first) | Positive | High | Login bot có premium_id, layout admin v2 | 1. Mở header → popup bot info<br>2. Bấm nút copy cạnh LINE ID<br>3. Paste vào ô text bất kỳ | Giá trị paste = `@lmessage` (premiumId), khớp với giá trị đang hiển thị | | | |
| TC003 | Header — bot KHÔNG có premiumId → fallback hiển thị basicId (line_id) | Boundary | High | Bot có `premium_id` = null/empty (bot chưa từng có premiumId) | 1. Login bot không có premiumId<br>2. Mở header popup bot info<br>3. Xem + copy LINE ID | Hiển thị + copy = basicId `line_id` (không rỗng, không hiển "null") | | | |
| TC004 | Header legacy (basic & admin cũ) — hiển thị LINE ID premium-first không vỡ layout | Regression | Medium | Bot có premiumId | 1. Mở header ở layout legacy (`layout/basic/header`, `layout/admin/header`)<br>2. Xem field LINE ID | Hiển thị premiumId đúng, layout không vỡ, copy hoạt động | | | |
| TC005 | Button 情報更新 — get lại premiumId, LINE ID đổi ngay không reload (Spec 2) | Positive | High | Bot vừa được LINE cấp premiumId nhưng DB đang lưu basicId (premium_id cũ null) | 1. Mở header, LINE ID đang hiện basicId<br>2. Bấm button 情報更新<br>3. Quan sát field LINE ID (KHÔNG reload trang) | LINE ID tự đổi sang premiumId ngay tại chỗ; DB `bots.premium_id` được ghi | | | |
| TC006 | Button 情報更新 — LINE trả premiumId rỗng → giữ nguyên, không xóa premium_id cũ | Boundary | High | Bot đang có `premium_id` = `@lmessage`; giả lập LINE trả về không có premiumId | 1. Bấm 情報更新<br>2. Xem LINE ID + kiểm tra DB `premium_id` | premium_id cũ KHÔNG bị ghi đè rỗng; LINE ID vẫn hiển `@lmessage` | | | |
| TC007 | Add bot mới có premiumId → premium_id lưu đúng, các màn hiển premiumId (Spec 1) | Positive | High | Có channel access token của bot có premiumId | 1. Admin → Add bot bằng token bot có premiumId<br>2. Hoàn tất add<br>3. Mở header + list bot | `bots.premium_id` được lưu; header + list hiển premiumId của bot mới | | | |
| TC008 | Change bot (đổi token sang bot có premiumId) → premium_id cập nhật | Positive | High | Bot hiện tại đang null premium_id; có token bot có premiumId | 1. Admin → Change bot bằng token mới (bot có premiumId)<br>2. Xem header + list bot | premium_id được cập nhật theo bot mới; hiển thị premiumId | | | |
| TC009 | Add bot KHÔNG có premiumId → premium_id để null, hiển thị basicId | Boundary | Medium | Token của bot chưa có premiumId | 1. Add bot bằng token bot không premiumId<br>2. Xem header + list bot | `premium_id` = null; mọi màn hiển basicId, không lỗi | | | |
| TC010 | Fetch bot info khi LINE API lỗi → premium_id không bị ghi rỗng (giữ giá trị cũ) | Negative | High | Bot đang có premium_id = `@lmessage`; giả lập LINE bot/info trả lỗi (5xx/timeout) khi mở chat / change bot | 1. Trigger luồng fetch bot info (mở chat 1:1 / change bot) trong lúc LINE API lỗi<br>2. Kiểm tra DB `premium_id` + màn hiển thị | premium_id cũ giữ nguyên `@lmessage` (không bị set null/rỗng); màn hiển vẫn premiumId | | | |
| TC011 | アカウント検索 (admin) — search theo premiumId tìm ra bot (CL-Func-9, orWhere premium_id) | Positive | High | Bot `@lmessage` tồn tại; login admin có quyền アカウント検索 | 1. Vào Admin → アカウント検索<br>2. Nhập từ khóa `lmessage` (premiumId)<br>3. Search | Kết quả trả về bot `@lmessage`; bảng hiển premiumId | | | |
| TC012 | アカウント検索 — search theo basicId vẫn hoạt động (regression sau khi thêm orWhere premium_id) | Regression | High | Bot có basicId `@281qduvu` | 1. Admin → アカウント検索<br>2. Nhập từ khóa `281qduvu` (basicId)<br>3. Search | Vẫn tìm ra đúng bot (search basicId không bị regression) | | | |
| TC013 | アカウント検索 — bảng kết quả (tab user/bot) + màn chi tiết hiển + copy premiumId | Positive | Medium | Có bot có premiumId + bot không premiumId trong kết quả | 1. Search ra danh sách gồm cả 2 loại bot<br>2. Xem cột LINE ID tab user & tab bot<br>3. Mở chi tiết + copy | Bot có premiumId → hiển/copy premiumId; bot không có → basicId; đúng từng dòng (CL-Func-11) | | | |
| TC014 | Bill 請求 index — card overdue / max friend hiển LINE ID premium-first (T2) | Positive | High | Bot có premiumId + có bản ghi bill (overdue / max friend) | 1. Vào màn Bill 請求 index<br>2. Xem LINE ID ở các card (overdue, max friend)... (6 chỗ) | Tất cả chỗ hiển LINE ID = premiumId của bot | | | |
| TC015 | Bill detail / detail-bill-fail / cancel_page — hiển premiumId | Positive | Medium | Bot có premiumId, có bill detail + 1 bill fail | 1. Mở Bill detail<br>2. Mở detail-bill-fail<br>3. Mở cancel_page | Cả 3 màn hiển LINE ID = premiumId | | | |
| TC016 | Bill sort modal — hiển đúng LINE ID premium-first sau khi sort (C.8 Sort) | Regression | Medium | Nhiều bot bill, ≥1 có premiumId | 1. Mở Bill index → mở sort modal<br>2. Sort theo tiêu chí bất kỳ<br>3. Xem LINE ID từng dòng | Sau sort, mỗi dòng hiển đúng premiumId/basicId tương ứng bot, không lệch dòng | | | |
| TC017 | Super admin — chi tiết bot + chi tiết user (tab info) hiển premiumId | Positive | Medium | Quyền super admin; bot có premiumId | 1. Super admin → mở chi tiết bot<br>2. Mở chi tiết user → tab info | Cả 2 màn hiển LINE ID = premiumId (view `supper_admin/tab_info`) | | | |
| TC018 | Trang chọn bot admin (pre_select_bot) + danh sách bot (index_v3) — cột LINE ID + search premiumId | Positive | Medium | Admin có nhiều bot, ≥1 có premiumId | 1. Vào trang chọn bot (pre_select_bot) + list bot index_v3<br>2. Xem cột LINE ID<br>3. Search theo premiumId | Cột LINE ID hiển premium-first; search premiumId ra đúng bot | | | |
| TC019 | Backup — màn processing + chọn tài khoản đích (data copy) hiển premiumId | Positive | Medium | Có bot nguồn + bot đích có premiumId | 1. Vào flow Backup → màn processing<br>2. Màn chọn tài khoản đích | LINE ID hiển premium-first ở cả 2 màn (ScreenController / BackupService) | | | |
| TC020 | Job update:premium_id — chạy thủ công → bot có premiumId được cập nhật DB (F3, TC-10) | Positive | Medium | Bot có channel_access_token + LINE có premiumId; DB premium_id đang null | 1. Chạy `php artisan update:premium_id` (hoặc chờ job 03:20)<br>2. Kiểm tra DB `bots.premium_id` + màn hiển | premium_id được ghi = premiumId từ LINE; màn hiển premiumId | | | |
| TC021 | Job update:premium_id — 1 bot LINE API lỗi → job bỏ qua, tiếp tục bot khác (TC-12) | Negative | Medium | ≥2 bot; giả lập 1 bot gọi getLineInfoBot lỗi | 1. Chạy job update:premium_id<br>2. Xem log job + DB các bot | Bot lỗi bị skip (không dừng job); các bot còn lại vẫn được update; job hoàn tất | | | |
| TC022 | Job update:premium_id — bot trả premiumId rỗng → không ghi đè premium_id cũ | Boundary | Medium | Bot có premium_id cũ; LINE trả premiumId rỗng | 1. Chạy job<br>2. Kiểm tra DB `premium_id` của bot đó | Giá trị cũ giữ nguyên (không set null/rỗng) | | | |
| TC023 | Job update:premium_id — đăng ký schedule daily 03:20 (F7, Kernel) | Regression | Low | Env đã deploy branch feature/premium-id-36768 | 1. Chạy `php artisan schedule:list`<br>2. Tìm command `update:premium_id` | Command xuất hiện trong list, lịch chạy dailyAt 03:20 | | | |
| TC024 | Migration add premium_id — data bot cũ còn nguyên, hiển basicId, không vỡ (TC-18, D1) | Boundary | High | DB có bot cũ (trước migration) chưa có premium_id | 1. Sau khi chạy `php artisan migrate`<br>2. Kiểm tra cột `bots.premium_id` (null cho bot cũ)<br>3. Mở header/list các bot cũ | Cột premium_id tồn tại, bot cũ = null; mọi màn hiển basicId bình thường (không lỗi, không hiện "null") | | | |
| TC025 | URL chat / add-friend (generateUrlToChat) vẫn dùng basicId — KHÔNG đổi sang premiumId (T10) | Regression | High | Bot có premiumId `@lmessage`, basicId `@281qduvu` | 1. Lấy URL add friend / link chat (lin.ee) của bot<br>2. Kiểm tra ID trong URL | URL vẫn theo basicId `line_id` (`@281qduvu`), KHÔNG dùng premiumId | | | |
| TC026 | Copy LINE ID header — copy đúng premiumId trên Win + Mac (hotkey & chuột phải) (CL-Func-24) | Boundary | Low | Bot có premiumId | 1. Header popup → copy LINE ID bằng nút<br>2. Thử trên Chrome Win + Safari/Chrome Mac | Copy ra `@lmessage` chính xác trên cả Win + Mac | | | |
| TC027 | premium_id stale — LINE đổi premiumId nhưng job chưa chạy → hiển giá trị cũ tới lần đồng bộ kế (T11) | Boundary | Medium | Bot có premium_id cũ; LINE đã đổi premiumId mới; job chưa chạy | 1. Xem LINE ID (đang là premium cũ)<br>2. Bấm 情報更新 (hoặc chạy job)<br>3. Xem lại LINE ID | Trước đồng bộ: hiển premium cũ; sau 情報更新/job: cập nhật premium mới đúng | | | |

### Chú thích cột

- **Type**: `Positive` happy path / `Negative` input-điều kiện sai / `Boundary` biên (null/empty/rỗng/stale/multi-platform) / `Regression` verify tính năng cũ không regression.
- **Priority**: `High` block release / `Medium` có workaround / `Low` nice-to-have.
- **Output note** / **Assignee** / **Status**: để trống — QA fill sau khi run.

### Environment (note)

Mặc định **Staging** (`staging.lme.jp`), bot `@lmessage`.
- TC006 / TC010 / TC021 / TC022 cần **giả lập LINE API** (trả rỗng / lỗi) → có thể cần env `Dev` hoặc mock; ghi rõ khi run.
- TC020 / TC023 chạy artisan command → cần quyền server/console.
- TC024 verify migration → thực hiện trên env vừa deploy.

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có) — **KHÔNG có file 02**, tham chiếu `templates/LME-SYSTEM-SPEC.md`, member nên bổ sung file 02 sau
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [x] Có **ít nhất 1 TC** verify trực tiếp spec (TC001/005/007 core Spec 1/2)
- [x] Có **ít nhất 1 TC regression** cho tính năng High trong 4.3
- [x] Có **ít nhất 1 negative + 1 boundary** cho data quan trọng (D2: TC010 negative + TC022 boundary)
- [x] Mọi TC đều có steps rõ ràng, expected đo lường được
- [x] Title TC chứa keyword giúp Leader map impact

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md).

**§A Checklist web**:
- [x] A.1 Function checklist — **CL-Func-9** (search premiumId: TC011/012/018), **CL-Func-11** (đúng bot: TC013), **CL-Func-24** (copy Win/Mac: TC026), **TC-18** (migration: TC024), **TC-10** (LINE API job: TC020/021), **TC-12** (job lỗi bỏ qua: TC021)
- [x] A.2 Non-function: **Regression** (TC004/012/016/023/024/025). Security: không có màn/URL mới → member verify staff-access nếu cần. Compatibility: TC026 (Win+Mac copy)

**§B Checklist job**:
- [ ] B.1 Job callback — không chạm callback
- [ ] B.2 CLJ01 sync Java — **KHÔNG áp dụng** (job gọi LINE API, không phải Google sync). TC-10 cover quan điểm rate-limit/retry LINE API

**§C Các tính năng chung**:
- [x] C.1 Bill tiền — chỉ **display** LINE ID (TC014/015/016), KHÔNG chạm payment gateway → không cần error-scenario cards
- [ ] C.2 Send message — không chạm
- [ ] C.3 Friend info — không chạm (line_id ở đây là của FRIEND, đã loại khỏi scope theo journal)
- [ ] C.4 Tag — không chạm
- [ ] C.5 Google sheet — không chạm
- [ ] C.6 Google calendar — không chạm
- [ ] C.7 Plan limits — không chạm
- [x] C.8 Sort — Bill sort modal (TC016)

<!-- Internal coverage map (KHÔNG sync — chỉ để Leader/`/review-tc` verify):
BUG/Spec1 display: TC001-004,013,014,015,017,018,019 | Spec2 情報更新: TC005,006 | Spec3 job: TC020-023
F1 displayLineId: TC001,003 | F2 accessor: TC001,013 | F3 command: TC020-023 | F4 write premium_id: TC005,007,008,010 | F5 display+search: TC011,012,013,018 | F6 blade: TC004,014,015,017 | F7 schedule: TC023
D1 migration: TC024 | D2 premium_id value: TC005,007,010(neg),022(bound) | D3 appends: covered gián tiếp qua display TCs
T1:TC001-004 | T2:TC014-016 | T3:TC011-013 | T4:TC017 | T5:TC018 | T6:TC019 | T7:TC007-009 | T8:TC005-006 | T9:TC020-023 | T10:TC025 | T11:TC027
-->
