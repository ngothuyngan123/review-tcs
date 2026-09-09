# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bởi `/new-task` — nguồn: **journal #128206** của [Redmine #39404](https://redmine.watermelon.vn/issues/39404), post bởi **Thanh Duy Nguyen** lúc `2026-08-05T12:26:10Z`.
>
> ⚠️ Journal tự ghi tiêu đề **"📊 Báo cáo đánh giá ảnh hưởng (AI tạo tự động)"** → nội dung dưới đây do **AI sinh**, chưa có dấu vết Dev người xác nhận trong ticket. Leader phải verify với Dev trước khi dùng làm base coverage.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Redmine `assigned_to` trống; journal đánh giá ảnh hưởng post bởi `Thanh Duy Nguyen` |
| Commit / Pull Request | `0022f93d066b9a949e275467cd4d5977e1b97f01` (commit hash, ticket không kèm URL) |
| Branch | `m_202608_backupbot-check-limit_39404` (base branch: `release-t07-2026`) |
| Ngày submit đánh giá | `2026-08-05` |
| Auto-filled | `2026-08-24 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục 1 journal #128206 -->

- Job backup (`BackupBotTask`) clone toàn bộ `b_event_detail` từ bot nguồn sang bot đích mà không check limit số event theo plan, nên bot plan standard mới (limit 10) / free mới (limit 2) bị vượt quá số lượng cho phép sau khi backup.
- Màn web chỉ chặn ở phía tạo mới (`BookingEventDayManagementController::ajaxGetListEventBooking`), không chặn đường backup.

## 2. Cách fix

<!-- Nguyên văn mục 2 journal #128206 -->

- Sau khi backup hoàn tất, thêm bước `checkLimitBEventDetail`: lấy limit theo plan của bot đích, đếm toàn bộ `b_event_detail` (`type_event_new = 1`) của bot đích gồm cả bản ghi có sẵn lẫn bản ghi vừa clone; nếu vượt limit thì gọi `api/clear_b_event_detail` (`event_detail_id`, `bot_id`, `_token`) xóa các bản ghi thừa, xóa từ id mới nhất trở xuống nên ưu tiên xóa đúng bản ghi vừa được backup tạo ra.
- Limit theo plan: free mới `2`, standard mới `10`, plan cũ (`flag_contract_new = 0`) và pro không giới hạn; plan free còn check thêm `users.created_at` trước `2021-07-01` thì tính là plan cũ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục 3 journal #128206, convert bullet → bảng -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Các method thêm mới — caller duy nhất: `BackupBotTask$HandleBackup.startBackup` | Không đổi signature/behavior của function cũ | "chỉ có 1 caller duy nhất là `BackupBotTask$HandleBackup.startBackup`; không đổi signature/behavior của function cũ nên không ảnh hưởng caller hiện có" |
| 2 | `BackupBotTask$HandleBackup.checkLimitBEventDetail` | Bọc `try/catch` riêng, chạy **sau** khi `backupHistory` đã set `STATUS_COMPLETED_BACKUP` | "lỗi ở bước này không làm fail luồng backup" |

> ⚠️ **Caller list chỉ có 1 entry** — Leader cần chất vấn: mục 3 chỉ khẳng định "method mới nên không ảnh hưởng", **không liệt kê caller nào của `startBackup`**. Nếu `startBackup` có nhiều đường trigger (job schedule, retry, manual từ màn 「データコピー」), cần verify từng đường.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục 4.1 journal #128206. Dev KHÔNG ghi cột Direct/Indirect. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BackupBotTask$HandleBackup.startBackup` | BackupBotTask | `<Dev không ghi>` | thêm lời gọi `checkLimitBEventDetail` |
| F2 | `BackupBotTask$HandleBackup.checkLimitBEventDetail` / `getLimitBEventDetail` / `isUserCreatedBeforeNewFreePlan` | BackupBotTask | `<Dev không ghi>` | **mới** |
| F3 | `BackupBotTask.clearBEventDetail` + `ISnslineService.clearBEventDetail` + `ClearBEventDetailResponse` | BackupBotTask / ISnslineService / ClearBEventDetailResponse (file mới) | `<Dev không ghi>` | **mới** |
| F4 | `BEventDetailRepository.findIdNewEventByBotIdOrderByIdDesc`, `BotRepository.findContractTypeById`, `UsersRepository.findCreatedAtById` | Repository layer | `<Dev không ghi>` | **mới** |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2 journal #128206 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Hằng số `Constants.PlanLimit` (contract type free/standard, mốc `2021-07-01`, limit `2` / `10`) | CREATE (hằng số code) | "Không có thay đổi DDL / migration / config.properties" |
| D2 | `b_event_detail` — bản ghi thừa của **bot đích** | DELETE | "xóa qua `api/clear_b_event_detail` phía sns-line" — data bị xóa **khi chạy job** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 journal #128206. Dev KHÔNG ghi mức nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Backup bot** — backup sang bot đích plan standard mới, tổng event vượt 10 thì còn đúng 10 bản ghi, các bản ghi cũ giữ nguyên, bản ghi vừa clone bị xóa trước | F1, F2, D2 | `<Dev không ghi>` |
| T2 | **Backup bot plan free mới** — còn đúng 2 event; bot plan cũ (`flag_contract_new = 0`) và plan pro thì **không** bị xóa bản ghi nào | F2, D1, D2 | `<Dev không ghi>` |
| T3 | **Event booking (予約イベント)** của bot đích — danh sách event sau backup khớp số lượng và **không mất event có sẵn** của bot đích | D2 | `<Dev không ghi>` |
| T4 | **Phụ thuộc API `api/clear_b_event_detail` bên sns-line** — cần API này đã deploy; nếu API trả lỗi thì có log `#clearBEventDetail onFailure` và notify chatwork | F3 | `<Dev không ghi>` |

---

## 5. Ghi chú giả định của Dev (nguyên văn — **cần dev confirm**)

> Journal #128206 tự đánh dấu 3 điểm sau là **giả định chưa confirm**. Đây là điểm rủi ro cao nhất của ticket — mỗi giả định sai là một nhánh bug lọt.

- Đếm theo `type_event_new = 1` (event kiểu mới), bám đúng cách web đếm limit tại `BookingEventDayManagementController`.
- Phân loại plan lấy `contract_type` từ `bot_contracts` join `bot_slots`, giống logic web; mốc created `2021-07-01` lấy theo `users.created_at` của `admin_id` (giống helper `checkPlanFreeBotLimitFeature`).
- `_token` gửi lên dùng `ConfigFile.API_SERVER_CERT` (giá trị của `KEY_CERTIFICATION_API`) vì phía PHP so sánh với `env('KEY_CERTIFICATION_API')`.
  ⚠️ **Mâu thuẫn với description ticket** — description ghi `_token: ConfigFile.API_CERT_KEY`, journal đánh giá ghi `ConfigFile.API_SERVER_CERT`. Journal #128353 của reporter chỉ nói *"_token web đã có rồi"*. **Leader phải chốt giá trị đúng trước khi member viết TC cho REQ-006.**

---

## 6. Input thiếu / cần Leader chất vấn Dev

- ❗ **Không có Dev người xác nhận** — báo cáo do AI sinh, `assigned_to` trống. Theo RULE-11, đây chưa phải bằng chứng hợp lệ (chỉ ticket Closed/Resolved/Fix done/Released mới là).
- ❗ **Mục 3 caller list rỗng** — chỉ khẳng định "method mới", không liệt kê caller thật của `startBackup`.
- ❗ **Cột Direct/Indirect (4.1) và Nguy cơ regression (4.3) đều trống** — Dev không phân loại mức độ.
- ❗ **Journal #130730 (2026-08-20)** cảnh báo `backup_config` bảng `image_map_items` sai cột `booking_event_id` → `b_event_detail`. Journal này đến **15 ngày sau** báo cáo đánh giá và **không** xuất hiện trong 4.1/4.2/4.3. Nếu config backup map sai cột thì phạm vi bản ghi `b_event_detail` bị clone/xóa có thể khác hẳn đánh giá trên → **Leader phải làm rõ trước khi chốt coverage**.
- ❗ **Mốc "staff bot free trước 11-11-2024 bot free được add 1 staff"** trong description **không** được nhắc lại ở bất kỳ mục nào của đánh giá ảnh hưởng.
- ❗ **Ảnh `Screenshot 2026-07-28 201451.png` dòng 22** — spec bổ sung nằm trong ảnh, đánh giá ảnh hưởng không tham chiếu tới.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **hiện đang rỗng, bắt buộc hỏi**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Đã chốt giá trị `_token` (`API_CERT_KEY` vs `API_SERVER_CERT`)
- [ ] Đã làm rõ phạm vi journal #130730 (`backup_config` / `image_map_items`)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
