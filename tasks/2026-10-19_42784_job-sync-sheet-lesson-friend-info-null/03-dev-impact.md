# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Redmine #42784 **không có section "Đánh giá ảnh hưởng" tách riêng trong Description** — nội dung đánh giá ảnh hưởng nằm trong các **Journal "Dev handoff"**. Ticket đã qua 3 vòng sửa (v1 → v2 → v3); mục dưới đây lấy theo **Journal #145234 (19/10/2026, mới nhất — v3)**, bản **supersede** v1/v2. ⚠️ **v2 (Journal #143042) đã mở rộng sang sửa cả job sync form answer, nhưng v3 đã REVERT toàn bộ phần đó** — chỉ còn giữ phần sửa job sync **lesson**. KHÔNG dùng nội dung form answer của v2 để viết TC.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (assignee Redmine) — đánh giá ảnh hưởng do "Dev Studio" biên soạn (Journal #145234, 2026-10-19) |
| Commit / Pull Request | `<chưa có link PR>` — commit cuối trên branch: `ef1e3561fdba63c5fc700b81c78d4bd2f838f26c` (nhánh gốc `release-t09-2026` @ `0766bf5302ff`) |
| Branch | `ai_studio_fixbug_42784` (repo `linect-service`) |
| Ngày submit đánh giá | 2026-10-19 (Journal #145234, bản v3) |
| Auto-filled | 2026-10-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`friend_info` của booking lesson là JSON array có phần tử `null` (dạng `[{...câu hỏi...}, null]`). `parseFriendInfo` giữ phần tử `null` trong danh sách, rồi `mappingFriendInfo` đọc giá trị của nó nên ném `NullPointerException`, và lỗi hiện ra là "Exception: null". Lần retry nào cũng lỗi y hệt nên sau 5 lần record bị đánh lỗi (status=2) và job gửi cảnh báo Chatwork "`#handleGoogleSheetException calendar lesson hết retry`". Nguyên nhân không đổi qua các vòng v1/v2/v3 — v3 chỉ thu hẹp lại phạm vi sửa (bỏ phần form answer).

## 2. Cách fix

- **Job sync Google Sheet lesson** (`HandleCalendarSyncGoogleSheetTask`): booking có `friend_info` chứa phần tử `null` vẫn lên sheet; phần tử `null` bị **bỏ qua** khi map cột; chỉ ghi log error `'#parseFriendInfo friend_info co phan tu null'`, **không gửi Chatwork** cho case này.
- **Job sync Google Sheet lesson**: câu trả lời `friend_info` dạng object key số không liên tục hiển thị `A,B` (trước đây hiển thị sai dạng `{0=A, 2=B}`); object rỗng `{}` → ô trống.
- **Job sync Google Sheet form answer**: **không thay đổi** so với bản base — phần sửa của vòng v2 (status_sync_sheet=4, log "khong co dong nao duoc ghi") đã **revert hoàn toàn** ở v3.
- Script recover lesson (chạy sau deploy): `docs/recovery/42784-reset-sync-lesson.sql`.

File đã sửa (java-job, diff v3 so với base):
```
.../googlesheet/HandleCalendarSyncGoogleSheetTask.java | 14 ++++++++++++++
1 file changed, 14 insertions(+)
```
(14 dòng trong 2 hàm private của job sync lesson — `parseFriendInfo` / `mappingFriendInfo` hoặc tương đương.)

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `parseFriendInfo` / `parseFriendInfoValue` (`HandleCalendarSyncGoogleSheetTask`) | Bỏ qua phần tử `null`; giữ nguyên xử lý mảng/object câu hỏi/`[]`/giá trị list-chuỗi-số-`"0"` | Dùng **chung** cho cả 4 luồng: thêm booking mới (append), dựng lại toàn sheet, cập nhật friend info (`type_sync=4`), insert bù |
| 2 | `HandleFormAnswerSyncGoogleSheetTask` (job sync form answer) | **Không đổi** — phần sửa vòng v2 (`status_sync_sheet=4`, log "khong co dong nao duoc ghi => ignore") đã **revert** | Dev loại khỏi phạm vi task #42784; ⚠️ môi trường test nào đã từng chạy bản v2 có thể còn **sót record ở status 4** — cần kiểm tra/dọn trước khi test v3 |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `parseFriendInfo` (bỏ qua phần tử `null` trong JSON array) | `HandleCalendarSyncGoogleSheetTask.java` | Direct | Áp dụng cho cả `friend_info` dạng mảng và object |
| F2 | `mappingFriendInfo` / map cột theo `friend_info` (không còn NPE khi gặp phần tử `null`; sửa hiển thị object key số không liên tục) | `HandleCalendarSyncGoogleSheetTask.java` | Direct | Case `{"0":"A","2":"B"}` trước đây hiển thị sai `{0=A, 2=B}`, nay hiển thị `A,B` |
| F3 | `#handleGoogleSheetException` / `handleGroup` (quyết định gửi Chatwork) | `HandleCalendarSyncGoogleSheetTask.java` | Indirect | Không gửi Chatwork cho case lỗi `friend_info` có `null` nữa; Chatwork cho các lỗi khác của job không đổi |
| F4 | `HandleFormAnswerSyncGoogleSheetTask` (toàn bộ) | `HandleFormAnswerSyncGoogleSheetTask.java` | **Không đổi** (đã revert) | ⚠️ Dễ nhầm với v2 — xác nhận diff v3 **không** còn chạm file này trước khi viết TC cho form answer |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_sync_googles.status` (record lesson/sheet lỗi "Exception: null") | UPDATE (script recover, chạy **sau** deploy) | `docs/recovery/42784-reset-sync-lesson.sql` — Bước 1 SELECT lấy danh sách id lỗi; Bước 2 `UPDATE ... SET status = 0 WHERE id IN (...) AND status = 2` (idempotent, chạy lại an toàn). Job tự sync lại, insert trùng tự bỏ qua. |
| D2 | `form_answer_result.status_sync_sheet` | **Không đổi** (phần recover form answer đã bỏ khỏi ticket ở v3) | Journal #143042 (v2) có đề cập giá trị `status_sync_sheet=4` + script recover form answer — **KHÔNG áp dụng cho v3** |

Ghi chú thêm: Journal #143597 (2026-10-13) cho thấy đã có 1 lần **recover tay thủ công** trước khi fix chính thức: `UPDATE calendar_sync_googles SET status = 0 WHERE id = 12307;` — khác với `recordId=12199` trong báo cáo gốc, cho thấy **nhiều record** đã bị ảnh hưởng bởi lỗi này trên production, không chỉ 1 record.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson booking — sync Google Sheet lesson (4 luồng: append booking mới, dựng lại toàn sheet, cập nhật friend info `type_sync=4`, insert bù) | F1, F2, F3, D1 | Medium — job nền, ảnh hưởng trực tiếp dữ liệu hiển thị trên Google Sheet của khách; sửa đúng hàm dùng chung cho cả 4 luồng nên regression nếu có sẽ lan ra cả 4 |
| T2 | Lesson booking — Chatwork alert khi job lỗi | F3 | Low — chỉ bớt 1 loại cảnh báo (case `friend_info` có `null`), các cảnh báo Chatwork khác của job không đổi |
| T3 | Job sync Google Sheet **form answer** | F4 (không đổi) | **Ngoài phạm vi task v3** — ⚠️ không viết/đề xuất TC mới cho hành vi form answer trong task này; nếu cần test hồi quy thì chỉ để xác nhận job vẫn chạy **y như bản base** (chưa từng đổi), không theo mô tả v2 |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ Xác nhận lại với Dev: diff v3 **chỉ còn** `HandleCalendarSyncGoogleSheetTask.java` (form answer đã revert) — tránh review/viết TC theo nội dung form answer của Journal #143042 (v2, đã lỗi thời)
