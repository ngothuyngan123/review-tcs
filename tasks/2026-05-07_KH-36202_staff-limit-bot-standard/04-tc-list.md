<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297 -->

# 04 — TC List (do member viết)

> ⚠️ **DRAFT do AI sinh** — member phải verify, chỉnh data sample, điền thông tin header trước khi submit.
> ✅ **Spec reference**: [02-spec-reference.md](02-spec-reference.md) (trích spec `staff-management/feature-spec.md`). Đặc biệt chú ý BR-005, BR-006, BR-007.
> ⚠️ **Format**: bảng TC dùng 10 cột chuẩn team (TC ID / Title / Type / Priority / Precondition / Steps / Expected result / Output note / Assignee / Status). Map to Impact + Environment **đã drop** — `/review-tc` sẽ suy luận coverage từ title/precondition/steps/expected của mỗi TC.
> 📝 **Approach**: viết từ góc nhìn **manual tester** — UI actions + observation. Không lead bằng DB query / schema field name. DB verification chỉ là bổ sung optional.
>
> **Câu hỏi đã resolve với Dev (2026-05-08):**
> - ✅ **Q1** Số `10` hard-code (không đọc config).
> - ✅ **Q2** Pending invite (status=0) KHÔNG count, chỉ active mới count → TC023.
> - ✅ **BR-006b** Standard tạo **TRƯỚC 2023-05-01** đối xử như Pro (unlimited) → TC024 + TC025.
> - ✅ **Q3** Bỏ qua chi tiết DB nhận diện pro — TC chỉ cần ghi "Bot pro plan", member dùng UI để dựng test data.
> - ✅ **Q5** TC008 expected đúng (per-bot hoặc tổng — không cần lock cụ thể, miễn message rõ).
> - ✅ **Q6** **KHÔNG có** soft-delete staff → drop C.7 case 3 (khôi phục).
> - ✅ **Bot downgrade (pre-cutoff/post-cutoff)**: chỉ system admin downgrade được, vẫn cho down bình thường → out-of-scope, không cần TC.
> - ✅ **Remove role staff**: count = 9 (đã cover bởi TC018 — delete staff release slot).
>
> **Câu hỏi out-of-scope (drop):**
> - ~~Q7 (REJECT status mechanics)~~ — internal state, không phải tester scope.
> - ~~Q8 (audit log)~~ — BotLifeCycle log internal, không phải tester scope.
> - ~~Q9 (cutoff field name)~~ — implementation detail, tester chỉ cần biết "bot tạo trước/sau 2023-05-01" để dựng test data.
>
> **Câu hỏi còn open:**
> - **Q4** Bot free legacy (pre-2021-07-01) có bị check max 10 không? — TC021 hiện flag.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | **v2** (round 1 review feedback áp dụng) |
| Link TC gốc (nếu có) | `<member điền sau khi import vào Sheet>` |
| Changelog v1 → v2 | + TC026 (F3 boundary tick-all) + TC027 (T2 link expired BR-001) + TC028 (T2 single-use BR-002). CL18 skip theo decision của member. |

---

## TC List

> **Default precondition cho mọi TC nói "Bot standard"** trong bảng dưới: bot có `contract_type='standard'` và **tạo TỪ 2023-05-01 trở đi** (post-cutoff, áp BR-006a limit 10). Bot legacy standard pre-2023-05-01 → xem riêng TC024 (treated as Pro, unlimited).

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Reproduce KH #36202 E2E: bot standard từ 0 staff, add tăng dần đến 10, cố add thứ 11 → bị chặn | Positive | High | Bot **mới** plan standard, **0 staff**. Login admin user chính. Có sẵn 11 email staff để invite. | 1. Vào màn quản lý staff (count hiển thị 0/10).<br>2. Lặp 10 lần: tạo invite link cho 1 email mới → staff đó accept invite. Sau mỗi vòng verify count tăng đúng (1/10, 2/10, ..., 10/10).<br>3. Khi count = 10/10, thử tạo invite cho email staff thứ 11. | Bước 2: 10 lần đều thành công, count cuối = 10/10. Bước 3: hệ thống chặn, hiển thị message lỗi "Bot đã đạt giới hạn 10 staff cho plan standard". Không tạo được invite thứ 11. KH scenario đã được fix. |  |  |  |
| TC002 | generateLinkInviteStaff: Bot standard 5/10 staff → tạo invite OK | Positive | High | Bot standard có 5 staff. | 1. Vào màn quản lý staff.<br>2. Tick chọn bot standard.<br>3. Click "Tạo invite link". | Tạo invite link thành công, link hiển thị copy được. |  |  |  |
| TC003 | generateLinkInviteStaff: Bot standard 9/10 (boundary) → tạo invite OK | Boundary | High | Bot standard có 9 staff. | 1. Tạo invite link cho staff thứ 10.<br>2. Staff thứ 10 accept. | Tạo invite OK. Sau khi accept, count = 10/10. |  |  |  |
| TC004 | generateLinkInviteStaff: Bot standard 10/10 → fail với error message | Negative | High | Bot standard có đúng 10 staff. | 1. Click "Tạo invite link".<br>2. Tick chọn bot standard 10/10. | Hiển thị message lỗi rõ ràng (không phải lỗi 500). Button có thể disabled hoặc submit bị reject. |  |  |  |
| TC005 | generateLinkInviteStaff: Bot free **(plan_type=2, tạo SAU 2021-07-01)** → fail (BR-005) | Negative | High | Bot plan **free** (`plan_type=2`), `created_at` SAU 2021-07-01. 0 staff. | 1. Vào màn invite-staff.<br>2. Quan sát danh sách bot có hiển thị bot free không. | Bot free này KHÔNG xuất hiện trong danh sách (BR-005 hide). Cảnh báo「※ フリープラン場合、スタッフの追加はできません。」hiển thị. |  |  |  |
| TC006 | Bot pro plan với 50 staff → tạo invite cho staff thứ 51 OK (unlimited) | Positive | Medium | Bot plan **pro**. Đã có 50 staff active. | 1. Vào màn invite-staff, tick chọn bot pro.<br>2. Nhập tên/email staff thứ 51.<br>3. Click "Tạo invite link".<br>4. Staff thứ 51 mở link và accept. | Bước 3: tạo invite thành công, không có message lỗi giới hạn. Bước 4: accept OK, count hiển thị 51 staff. Pro plan không bị giới hạn. |  |  |  |
| TC007 | acceptInviteStaff: Staff accept invite khi bot standard 5/10 → add OK | Positive | High | Bot standard 5/10 staff. Đã tạo invite link cho staff mới. | 1. Staff mở invite link (logged in account staff).<br>2. Tick chọn bot standard.<br>3. Click "Accept". | Accept thành công. Count bot standard = 6/10. Staff thấy bot trong dashboard. |  |  |  |
| TC008 | acceptInviteStaff: Accept multi-bot, 1 bot standard đã 10/10 → skip bot đó với message, bot còn slot vẫn add | Negative | High | Account staff được invite vào 3 bot: bot A (standard 10/10), bot B (standard 5/10), bot C (pro). | 1. Staff mở invite link.<br>2. Tick cả 3 bot A, B, C.<br>3. Click "Accept". | Bot A bị skip với message lỗi (per-bot hoặc tổng — TBD theo Dev). Bot B, C accept OK. Count: A=10/10 (không đổi), B=6/10, C+1. |  |  |  |
| TC009 | acceptInviteStaff race condition: 2 staff accept cùng lúc khi bot còn 1 slot | Boundary | High | Bot standard 9/10. Có 2 invite link đang chờ accept. | 1. Staff X và staff Y mở invite link cùng lúc (2 browser/incognito).<br>2. Cả 2 click "Accept" trong cùng < 1 giây. | 1 staff accept thành công (count = 10/10). 1 staff fail với message. KHÔNG có race condition tạo 11/10. |  |  |  |
| TC010 | invite_staft.js: tick 2/5 bot → BE chỉ nhận POST với 2 bot ID đã tick | Positive | High | Admin có 5 bot (mix plan). Mở DevTools Network tab. | 1. Vào màn tạo invite.<br>2. Tick chọn 2 bot.<br>3. Click "Tạo invite link".<br>4. Inspect request payload trong Network tab. | Request body chỉ chứa 2 bot ID đã tick (không phải all 5 bot). |  |  |  |
| TC011 | invite_staft.js: không tick bot nào → button disabled hoặc validation fail | Negative | Medium | Admin có ≥ 1 bot. | 1. Vào màn tạo invite.<br>2. KHÔNG tick bot nào.<br>3. Quan sát button "Tạo invite link". | Button disabled HOẶC click → hiển thị validation "Vui lòng chọn ít nhất 1 bot". Không submit request lên BE. |  |  |  |
| TC012 | User chính (主管理者) KHÔNG tính vào giới hạn 10 staff | Regression | High | Bot standard có user chính (主管理者) + đã invite + accept đủ 10 staff (副管理人/運用者/サポート). | 1. Login user chính, vào màn quản lý staff.<br>2. Quan sát danh sách staff hiển thị: user chính + 10 staff khác.<br>3. Thử tạo invite cho staff thứ 11. | Bước 2: danh sách hiển thị 11 dòng (1 user chính 主管理者 + 10 staff). Count limit hiển thị 10/10. Bước 3: tạo invite thứ 11 fail với message "Bot đã đạt giới hạn". User chính KHÔNG bị tính vào limit. |  |  |  |
| TC013 | Màn generate invite link admin: happy path E2E (mix standard + pro bot) | Regression | High | Admin có 1 bot standard (5/10) + 1 bot pro. | 1. Vào màn quản lý staff.<br>2. Click "Tạo invite link".<br>3. Tick cả 2 bot.<br>4. Nhập email.<br>5. Click "Tạo".<br>6. Copy link.<br>7. Mở link ở browser khác. | Link gen OK, copy OK, mở link ở browser khác load màn accept đúng. |  |  |  |
| TC014 | Màn accept bot của staff: happy path E2E | Regression | High | Có invite link valid cho staff mới gồm 2 bot. | 1. Staff mở invite link.<br>2. Login (nếu chưa).<br>3. Màn hiển thị 2 bot được invite.<br>4. Tick cả 2 bot.<br>5. Click "Accept". | Màn confirm "Đã thêm vào X bot". Staff thấy 2 bot trong dashboard. |  |  |  |
| TC015 | C.7 plan limit case "mở 2 tab": 2 tab cùng tạo invite cho bot standard 9/10 | Boundary | High | Bot standard 9/10. Login cùng admin ở 2 tab. | 1. Tab1: tạo invite cho staff X, để pending chưa submit.<br>2. Tab2: tạo invite cho staff Y, để pending.<br>3. Tab1 submit → success.<br>4. Tab2 submit. | Tab1 thành công (count 10/10). Tab2 fail với message "Bot đã đạt giới hạn". KHÔNG có race tạo 11/10. |  |  |  |
| TC016 | C.7 + CL5 double click: double click "Tạo invite" ở lần limit cuối | Boundary | High | Bot standard 9/10. | 1. Vào màn tạo invite.<br>2. Tick bot standard.<br>3. Nhập email.<br>4. Double click button "Tạo invite link" thật nhanh. | Chỉ 1 invite link được tạo. Click thứ 2 bị block (button disabled sau click 1, hoặc BE reject duplicate). KHÔNG tạo 2 invite + count nhảy lên 11/10. |  |  |  |
| TC017 | CL11 CRUD đúng bot: invite vào bot A không ảnh hưởng count bot B | Regression | High | Account admin có bot A (standard 5/10) + bot B (standard 8/10). | 1. Tạo invite chỉ tick bot A.<br>2. Staff mới accept invite (chỉ chọn bot A).<br>3. Quan sát count của 2 bot trên dashboard. | Bot A: count tăng 5/10 → 6/10. Bot B: vẫn 8/10 không đổi. Staff mới chỉ thấy bot A trong danh sách bot của họ, không thấy bot B. |  |  |  |
| TC018 | CL10 xóa staff: bot standard 10/10 → xóa 1 staff → release slot, tạo invite mới được | Regression | High | Bot standard đầy 10/10 staff. | 1. Xóa 1 staff bất kỳ.<br>2. Verify count = 9/10.<br>3. Tạo invite cho staff mới. | Sau xóa: count = 9/10. Tạo invite mới thành công. Slot được release. |  |  |  |
| TC019 | CL1 + BR-004 staff role: account staff không phân quyền → BE redirect adminIndex (KHÔNG phải button hide) | Negative | Medium | Bot có 1 staff (role > 0). Staff KHÔNG được cấp quyền `staff-management.inviteStaff`. | 1. Login bằng staff đó.<br>2. Truy cập trực tiếp `/admin/employees-management` qua URL.<br>3. Truy cập trực tiếp `/admin/invite-staff?bot_id=X` qua URL.<br>4. Thử POST `/admin/ajax/generate-link-invite-staff` qua API direct (Postman/cURL). | Bước 2-3: BE check `checkBotHasPermission(...)` → REDIRECT `adminIndex`, KHÔNG render màn staff management. Bước 4: BE trả 403/redirect, KHÔNG tạo invite. (Hành vi enforce ở backend, không chỉ UI hide.) |  |  |  |
| TC020 | Compatibility: error message hiển thị đúng trên Win+Chrome, Win+Edge, Mac+Safari | Regression | Medium | Bot standard 10/10. | Repeat TC004 trên 3 combo browser/OS. | Error message hiển thị nhất quán, không bị overflow, encode tiếng Việt/Nhật đúng. |  |  |  |
| TC021 | BR-005 legacy exception: Bot free **tạo TRƯỚC 2021-07-01** vẫn cho phép có staff (regression) | Regression | High | Bot plan free (`plan_type=2`), `created_at < 2021-07-01` (data legacy). Có sẵn 3 staff legacy. | 1. Vào màn quản lý staff, chọn bot free legacy.<br>2. Quan sát danh sách staff hiển thị.<br>3. Vào màn invite-staff, quan sát bot free legacy có trong danh sách bot không. | Bước 2: 3 staff legacy hiển thị bình thường, không bị xóa hay block. Bước 3: bot free legacy XUẤT HIỆN (BR-005 ngoại lệ). Verify với Dev (Q4): bot legacy này có bị áp limit 10 không hay vẫn unlimited. |  |  |  |
| TC022 | Check-at-accept-time: invite tạo khi bot 5/10, bot fill lên 10/10 trước khi staff accept → accept fail | Boundary | High | Bot standard 5/10. Admin tạo invite link X cho staff X. Sau đó (chưa accept), 5 staff khác được invite + accept → bot lên 10/10. | 1. Tạo invite link X cho staff X (count khi tạo: 5/10).<br>2. Lần lượt invite + accept 5 staff khác → count = 10/10.<br>3. Staff X mở invite link X (vẫn còn hợp lệ trong 24h).<br>4. Staff X click "Accept" cho bot. | Bước 4: BE check max staff TẠI THỜI ĐIỂM ACCEPT (theo dev impact mục 2 BE accept). Staff X bị skip với message "Bot đã đạt giới hạn". Count vẫn = 10/10, không lên 11/10. (Verify rule check không phải chỉ ở generate, mà cả ở accept.) |  |  |  |
| TC023 | Pending invite chưa accept KHÔNG count vào limit — admin tạo được nhiều invite hơn slot trống | Boundary | High | Bot standard có 8 staff đã active. Admin đã tạo sẵn 2 invite link cho 2 người khác (chưa ai accept). | 1. Quan sát count hiển thị: 8/10.<br>2. Vào màn invite-staff, tạo invite link thứ 3 cho 1 email mới.<br>3. 3 staff (2 invite cũ + 1 invite mới) lần lượt mở link và accept theo thứ tự. | Bước 2: tạo invite thứ 3 thành công (vì count vẫn 8/10, pending không tính). Bước 3: staff #1 accept → 9/10. Staff #2 accept → 10/10. Staff #3 accept → SKIP với message "Bot đã đạt giới hạn" (kết hợp TC022 — check tại accept time). Count cuối hiển thị 10/10, không vượt. |  |  |  |
| TC024 | Bot standard CŨ (tạo trước 2023-05-01) không bị giới hạn — đối xử như Pro | Regression | High | Bot standard tạo trước 2023-05-01 (vd contract date 2022-10-15). Đã có 12 staff active (vượt số 10 mới). | 1. Vào màn quản lý staff, chọn bot này.<br>2. Quan sát count + danh sách staff hiển thị.<br>3. Tạo invite cho staff thứ 13.<br>4. Staff thứ 13 mở link và accept. | Bước 2: 12 staff hiện đang hiển thị bình thường, không bị block. Bước 3: tạo invite thành công, không có message "đã đạt giới hạn". Bước 4: accept OK, count = 13. Bot standard cũ treated như Pro. |  |  |  |
| TC025 | Mix bot standard cũ + mới trong cùng 1 invite — chỉ bot mới bị limit | Boundary | Medium | Account admin có 2 bot:<br>- Bot A: standard cũ (tạo trước 2023-05-01) — 11 staff active<br>- Bot B: standard mới (tạo sau 2023-05-01) — 10 staff active | 1. Vào màn invite-staff, tick cả Bot A + Bot B.<br>2. Nhập email staff mới, tạo invite.<br>3. Staff mở link, tick cả 2 bot, click Accept. | Bước 2: tạo invite thành công cho cả 2 bot. Bước 3: Bot A → add staff thứ 12 OK (cũ, unlimited). Bot B → SKIP với message "Bot đã đạt giới hạn" (mới, 10/10). Rule áp riêng từng bot, không lan sang nhau. |  |  |  |
| TC026 | invite_staft.js: click "全てを選択" với account có nhiều bot mix plan → BE chỉ nhận bot đang hiển thị (free post-2021 đã bị hide) | Boundary | Medium | Admin có 5 bot: 1 free post-2021-07-01 (sẽ bị hide khỏi form), 1 free legacy (pre-2021-07-01), 2 standard cũ, 1 standard mới. Mở DevTools → Network. | 1. Vào màn invite-staff.<br>2. Quan sát danh sách bot hiển thị trong form (count expected = 4, không phải 5).<br>3. Click button "全てを選択／解除" để tick tất cả bot hiển thị.<br>4. Nhập tên staff, click "Tạo invite link".<br>5. Inspect Network payload của request POST. | Bước 2: chỉ 4 bot hiển thị (free post-2021-07-01 đã bị BR-005 hide). Bước 5: request body chứa đúng 4 bot ID đã tick — không thiếu bot nào trong 4 bot, không gửi nhầm bot free post-2021. |  |  |  |
| TC027 | acceptInviteStaff: link đã quá 24h từ khi tạo → fail với message hết hạn (BR-001) | Negative | High | Có invite link L được Admin tạo > 24h trước (test env có chức năng time-travel, hoặc tester chờ qua đêm, hoặc dùng tool dev nếu có). Link L chưa được ai accept. | 1. Staff mở link L sau 24h.<br>2. Quan sát màn hiển thị. | Hiển thị message lỗi "有効期限を超えました。再度招待をしてもらってください。" (hoặc tương đương). KHÔNG vào màn accept. KHÔNG có UserStaffBot mới được tạo. Bot count không thay đổi. |  |  |  |
| TC028 | acceptInviteStaff single-use: invite đã được Staff X accept → Staff Y mở cùng link fail (BR-002) | Negative | High | Admin tạo invite link L cho 1 bot. Staff X đã mở link L và click Accept thành công, đã thấy bot trong dashboard. | 1. Staff Y (account khác) mở cùng link L (lấy URL từ Admin hoặc Staff X share lại).<br>2. Quan sát màn hiển thị. | Hiển thị message "招待されたURLはすでに無効となっています。" (hoặc tương đương). Staff Y KHÔNG được join bot. Bot count không tăng. |  |  |  |

### Chú thích cột

- **Type**:
  - `Positive` — happy path đúng theo fix
  - `Negative` — input sai / điều kiện sai, verify xử lý lỗi
  - `Boundary` — giá trị biên (max, race condition, double-click, multi-tab)
  - `Regression` — verify tính năng cũ không bị ảnh hưởng
- **Priority**:
  - `High` — block release nếu fail
  - `Medium` — quan trọng nhưng có workaround
  - `Low` — nice-to-have
- **Output note** / **Assignee** / **Status**: để trống khi sinh draft. QA fill sau khi run TC. Status có dropdown trên Sheet: `OK` / `NG` / `Not test` / `NG -> Đã fix`.

---

### Phân bố

- Tổng: **28 TCs** (v2 — sau review round 1: thêm TC026/027/028)
- Theo Type: Positive 7 (25%) / Negative 7 (25%) / Boundary 8 (29%) / Regression 6 (21%)
- Smoke test trên Production sau deploy: TC001 + TC013 + TC014 (KHÔNG test create/delete trên data thật).
- Multi env: TC009 (race) + TC015 (multi-tab) + TC022 (check-at-accept timing) nên test trên Dev để dễ reproduce timing. TC020 cover Win+Mac compatibility.
- TC từ spec review: TC021 (legacy free), TC022 (check at accept time), TC023 (pending count), TC024 (legacy standard pre-2023-05-01), TC025 (mixed legacy + post-cutoff).
- **TC từ round 1 review feedback**: TC026 (F3 boundary tick-all), TC027 (T2 link expired BR-001), TC028 (T2 single-use BR-002).

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md`
- [x] Đã đọc kỹ `02-spec-reference.md` (đã có, trích từ feature-spec staff-management)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] Mỗi impact trong 4.1 / 4.3 đều có ≥ 1 TC verify (4.2 không có data) — Claude đã track khi sinh TC
- [x] Có TC verify trực tiếp bug fix (TC001 reproduce E2E flow KH)
- [x] Có TC regression cho mỗi tính năng trong 4.3 (TC013 cover màn generate invite, TC014 cover màn accept)
- [x] Có negative + boundary cho data — *N/A vì 4.2 không có data*
- [x] Mọi TC đều có steps rõ ràng, expected đo lường được

### Base checklist LME

**§A Checklist web**:
- [x] A.1 Function checklist:
  - [x] CL1 (staff role) — TC019
  - [x] CL5 (double click) — TC016
  - [x] CL10 (delete data ảnh hưởng) — TC018
  - [x] CL11 (CRUD đúng bot) — TC017
  - [ ] CL2 (reload sau save) — *member tự thêm nếu cần*
  - [ ] CL3, CL4 (chuyển tab, thao tác liên tục) — *member tự thêm nếu cần*
  - [ ] **CL18 (load UI trước, submit sau khi deploy)** — Member quyết SKIP ở v2 (out-of-scope cho phạm vi test hiện tại). Note với Leader nếu Leader yêu cầu lại.
- [x] A.2 Non-function:
  - [x] Regression (TC012, 013, 014, 017, 018, 020)
  - [x] Compatibility (TC020)
  - [ ] Security URLs — *N/A, không có URL mới*

**§B Checklist job**: N/A (không chạm callback / Google sync)

**§C Tính năng chung**:
- [x] **C.7 Plan limits** — 5 case:
  - [x] Tạo mới — TC001-008
  - [ ] Copy — *N/A cho staff*
  - [x] ~~Khôi phục soft-delete~~ — N/A (Dev confirm 2026-05-08: KHÔNG có soft-delete staff trong hệ thống)
  - [x] Mở 2 tab → thao tác — TC015
  - [x] Double click ở lần limit cuối — TC016
- [x] C.7 3 server profile — TC020 cover Win+Mac. Member nên test thêm bằng account staff thường (không phải admin) ở plan free để verify regression cho các plan.
- [ ] C.1 Bill tiền — N/A
- [ ] C.2 Send message — N/A
- [ ] C.3 Friend info — N/A
- [ ] C.4 Tag — N/A
- [ ] C.5 Google sheet — N/A
- [ ] C.6 Google calendar — N/A
- [ ] C.8 Sort — N/A

---

## Trạng thái câu hỏi với Dev/PM

Sau khi Dev clarify ngày 2026-05-08:

| # | Câu hỏi | Status |
|---|---|---|
| Q1 | Số 10 hard-code hay config? | ✅ **Hard-code 10** |
| Q2 | Pending invite có count? | ✅ KHÔNG count (chỉ active) → TC023 |
| Q3 | Pro plan identification? | ✅ Drop — tester chỉ cần "bot pro plan", không cần biết DB field |
| Q4 | Bot free legacy (pre-2021-07-01) có bị limit 10? | ⚠️ Còn open — TC021 đã flag, member verify khi run |
| Q5 | Multi-bot accept message format? | ✅ TC008 expected hiện đã đúng |
| Q6 | Soft-delete staff? | ✅ KHÔNG có → drop C.7 case 3 |
| Q7 | REJECT status mechanics? | ✅ Drop — internal state, không phải tester scope |
| Q8 | Audit log? | ✅ Drop — internal, không phải tester scope |
| Q9 | Cutoff field name? | ✅ Drop — implementation detail, tester chỉ cần "bot tạo trước/sau 2023-05-01" |
| BR-006b | Standard pre-2023-05-01 treated as Pro? | ✅ **Đúng** → TC024 + TC025 |
| Bot downgrade | Có cho downgrade khi > limit? | ✅ Vẫn cho down bình thường (chỉ admin master, out-of-scope bug này) |
| Remove role staff | Count thay đổi sao? | ✅ Count giảm xuống 9 — đã cover bởi TC018 (delete staff release slot) |

**Còn 1 câu open (Q4)**: bot free legacy pre-2021-07-01 có bị áp limit 10 không. Member chạy TC021 sẽ verify khi test. Nếu bị limit → cân nhắc thêm TC ghép limit + free legacy.
