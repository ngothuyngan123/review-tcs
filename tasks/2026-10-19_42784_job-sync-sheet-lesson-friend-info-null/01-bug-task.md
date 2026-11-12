# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42784 — [JOB] Job sync google sheet lesson gặp lỗi khi trong friend_info có object null` |
| Module / Màn hình | Job sync Google Sheet lesson (`HandleCalendarSyncGoogleSheetTask`) — tính năng Lesson booking (lịch bài học), hàng đợi `calendar_sync_googles` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine gốc đã ở dạng log/Chatwork alert (VN + log), giữ nguyên văn, không diễn giải lại. -->

`#handleGoogleSheetException calendar lesson hết retry - calendarId 7692 - recordId 12199 - Exception: null`

Kèm theo nội dung `friend_info` của record lỗi (JSON array), trong đó có 1 phần tử là `null`:

```json
[
  {
    "id": "26668",
    "form_type": "1",
    "question": "入学者本人",
    "sub_question": null,
    "required": "true",
    "rules": "required_calendar",
    "friend_information_id": "-1",
    "display_method": "1",
    "date_beginning": null,
    "value": "渡邊芭奈",
    "value_preview": null,
    "recording_time": "false",
    "time": null
  },
  null
]
```

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- `bug_form_answer_sync_sheet_inconsistency.md` — https://redmine.melonglobal.net/attachments/download/32896/bug_form_answer_sync_sheet_inconsistency.md
  (⚠️ Tài liệu đính kèm nói về bug sync **form answer** — Dev đã quyết định **tách ra ticket riêng**, không nằm trong phạm vi sửa của #42784 bản cuối, xem Journal #145234 bên dưới.)

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được qua "Steps to reproduce" trong Redmine** — ticket được tạo tự động từ cảnh báo Chatwork `#handleGoogleSheetException ... hết retry` (job background), không có thao tác UI để tái hiện. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify cách fix (bỏ qua phần tử `null` trong `friend_info`, không gửi Chatwork cho case này) + regression các luồng sync lesson khác dùng chung `parseFriendInfo` / `parseFriendInfoValue`.

⚠️ **Ticket đã qua nhiều vòng sửa (v1 → v2 → v3)**: v2 (Journal #143042) có mở rộng sang sửa cả job sync **form answer**, nhưng v3 (Journal #145234, mới nhất 2026-10-19) đã **revert toàn bộ phần form answer**, chỉ còn giữ phần sửa job sync **lesson**. Dev yêu cầu mở ticket riêng cho bug form answer nếu cần xử lý. → Khi viết/review TC, **chỉ tập trung job sync lesson**, không viết TC cho hành vi form answer theo v1/v2 (đã không còn trong diff).

⚠️ Môi trường: Bug phát sinh trên production (job Java sync lesson đã bật từ commit `b03c94939` ngày 15/09/2026, release-t08-2026). Bản fix (v3) **chưa verify runtime với Google Sheet thật** — Dev tự nhận "đã kiểm bằng harness trên class thật, chưa verify runtime với Google Sheet thật" (Journal #145234).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tester tra trên DB qua calendarId/recordId>` |
| Friend | `<chưa rõ — JSON mẫu có value "渡邊芭奈" nhưng đây là giá trị form, không chắc là tên friend>` |
| Đối tượng cấu hình | Lesson booking — `calendarId=7692`, `recordId=12199` (bản ghi lỗi gốc trong `calendar_sync_googles`, status=2, lỗi "Exception: null" do `friend_info` chứa phần tử `null`) |
| Thời điểm lỗi | Ticket tạo `2026-10-12`; lỗi lặp lại mỗi lần retry (5 lần) rồi record bị đánh ERROR và gửi Chatwork |
| Đối chứng | Booking có `friend_info` bình thường (mảng/object không có phần tử `null`) vẫn sync OK — theo giải thích Dev ở Journal #142943/#143041 |

## Journal / note từ Redmine (nguyên văn)

**Journal #142943 — Dev Studio — 2026-10-12:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
friend_info của booking lesson là JSON array có phần tử null ([{...}, null]). `parseFriendInfo` dùng `JsonParser.fromStringToArrayOrObject`, hàm này giữ phần tử null trong list; `mappingFriendInfo` tìm được vị trí cột "" cho phần tử null rồi gọi `info.getValue()` → NullPointerException với message null. `handleGroup` ghi lỗi "Exception: null"; lần retry nào cũng lỗi y hệt nên sau 5 lần record thành ERROR và gửi Chatwork như trong ticket.

Hướng sửa:
- D-1 Bỏ qua phần tử null trong friend_info khi sync sheet lesson
- D-2 Script recover: đặt lại các record sync lesson bị lỗi 'Exception: null'

Ảnh hưởng / rủi ro:
Chỉ đổi job sync Google Sheet lesson (HandleCalendarSyncGoogleSheetTask): booking có phần tử null trong friend_info sẽ sync được, phần tử null bị bỏ qua. Booking có friend_info bình thường giữ nguyên hành vi. Không đổi schema, không đổi contract với web. Cần kiểm thử đủ các luồng append, dựng lại sheet rỗng, cập nhật friend info và insert bù.
```

**Journal #143041 — Dev Studio — 2026-10-12:**

```
Dev Studio · Nguyên nhân & hướng sửa (v2)

Nguyên nhân:
friend_info của booking lesson là JSON array có phần tử null ([{...}, null]). `parseFriendInfo` giữ phần tử null trong danh sách, rồi `mappingFriendInfo` gọi `info.getValue()` trên null nên ném NullPointerException, message rỗng thành "Exception: null". Lần retry nào cũng lỗi y hệt, sau 5 lần record bị đánh lỗi và Chatwork báo "calendar lesson het retry". Nguyên nhân không đổi so với v1.

Hướng sửa:
- D-1 Bỏ gửi Chatwork khi friend_info có phần tử null, chỉ giữ log

Ảnh hưởng / rủi ro:
Hành vi sync giống v1: phần tử null bị bỏ qua và booking vẫn lên sheet. Thay đổi duy nhất là case này không còn tin Chatwork, chỉ còn dòng log #parseFriendInfo. Các Chatwork khác của job không đổi.
```

**Journal #143042 — Dev Studio — 2026-10-12:**

```
Dev handoff — v2 · nhánh ai_studio_fixbug_42784

Nguyên nhân:
friend_info của booking lesson là JSON array có phần tử null ([{...}, null]). `parseFriendInfo` giữ phần tử null trong danh sách, rồi `mappingFriendInfo` gọi `info.getValue()` trên null nên ném NullPointerException, message rỗng thành "Exception: null". Lần retry nào cũng lỗi y hệt, sau 5 lần record bị đánh lỗi và Chatwork báo "calendar lesson het retry". Nguyên nhân không đổi so với v1.

Nội dung thay đổi:
- Job sync Google Sheet lesson: booking có friend_info chứa phần tử null vẫn lên sheet; phần tử null bị bỏ qua; chỉ ghi log error '#parseFriendInfo friend_info co phan tu null', không gửi Chatwork.
- Job sync Google Sheet lesson: câu trả lời friend_info dạng object key số không liên tục hiển thị A,B (trước đây {0=A, 2=B}); object rỗng => ô trống.
- Job sync Google Sheet form answer: câu trả lời không ghi được dòng nào ở bất kỳ page nào (line user không tồn tại, data rỗng/hỏng, page không thuộc form) => status_sync_sheet = 4 kèm log 'khong co dong nao duoc ghi => ignore'; log cuối batch tách 'synced X - ignored Y'.
- Hai script recover trong tài liệu task: lesson (docs/recovery/42784-reset-sync-lesson.sql) và form answer (docs/recovery/42784-reset-sync-form-answer.sql).

File đã sửa (java-job):
  .../HandleCalendarSyncGoogleSheetTask.java         | 14 ++++++++++
  .../HandleFormAnswerSyncGoogleSheetTask.java       | 32 ++++++++++++++++++++--
  2 files changed, 43 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi nhỏ trong 2 class của job, chỉ đổi kết quả ở các trường hợp trước đây lỗi hoặc ghi sai. Đã kiểm bằng harness trên class thật và kiểm chứng ngược trên base; chưa verify runtime với Google Sheet thật.
- Lesson: thêm dòng booking mới, dựng lại toàn sheet, cập nhật friend info (type_sync=4), insert bù — đều dùng parseFriendInfo/parseFriendInfoValue.
- Lesson: friend_info bình thường (mảng, object câu hỏi, [], giá trị list/chuỗi/số/"0") phải giữ nguyên kết quả như trước.
- Form answer batch (handleSyncBatch): sheet đã có dữ liệu, form nhiều page hoặc 1 sheet, câu trả lời có sẵn, append nhiều lô, lỗi Google giữa chừng (requeue/fallback).
- Form answer per-result (handle): resume từ page lỗi, dựng lại sheet rỗng, form không có page.
- Bảng form_answer_result.status_sync_sheet: dùng thêm giá trị 4 có sẵn cho trường hợp mới; web chỉ set 0 khi tạo, job chỉ poll 0 nên màn web không bị ảnh hưởng.
- Bảng result_error_googles: record bị bỏ qua có result_error_google_id được đóng SUCCESS như các case bỏ qua khác.

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Đặt lại calendar_sync_googles lesson/sheet lỗi 'Exception: null' (friend_info có phần tử null) từ status 2 về 0 để job sync lại — docs/recovery/42784-reset-sync-lesson.sql: Bước 1 chạy SELECT trong file để lấy danh sách id. Bước 2: UPDATE calendar_sync_googles SET status = 0, updated_at = NOW() WHERE id IN (<id bước 1>) AND status = 2;
- [Recover · Sau deploy] Đặt lại form_answer_result đã đánh dấu SYNC nhưng thiếu dòng trên Google Sheet (status_sync_sheet 1 về 0) để job ghi bù — docs/recovery/42784-reset-sync-form-answer.sql: Điền @from/@to trong file (@to = thời điểm #40734 lên production). Bước 1 chạy SELECT để lấy id. Bước 2 theo lô ~500 id: UPDATE form_answer_result SET status_sync_sheet = 0 WHERE id IN (<id bước 1>) AND status_sync_sheet = 1 AND (result_error_google_id IS NULL OR result_error_google_id = 0);

Recover dữ liệu: Cần recover — Các record sync lesson đã bị đánh lỗi vì lỗi này sẽ không được retry nữa, nên booking thiếu dòng trên Google Sheet của khách. Phương án recover không đổi so với v1.
- Ảnh hưởng: calendar_sync_googles (sheet, lesson) bị status=2 với lỗi 'Exception: null'
- Ảnh hưởng: Dòng booking bị thiếu trên Google Sheet lesson của khách
- Khoảng thời gian: Từ khi job Java sync lesson được bật trên production (commit b03c94939 ngày 15/09/2026, có trong release-t08-2026) tới khi bản sửa chạy
- Cách recover: Sau khi deploy, chạy script docs/recovery/42784-reset-sync-lesson.sql: chế độ đếm (SELECT) trước, sau đó UPDATE status 2→0 với điều kiện status = 2 (idempotent). Job sẽ tự sync lại; insert trùng tự bỏ qua.
- Ảnh hưởng tới khách: Chỉ ghi bổ sung các dòng còn thiếu lên Google Sheet của chính khách, không gửi tin nhắn nào.

Lưu ý khi deploy:
- Chỉ deploy module job (linect-service). Hai script recover chạy sau khi bản job mới đã chạy.
- Script form answer: người chạy điền @to = thời điểm #40734 lên production trước khi chạy.

Việc cần người làm thêm (ngoài phạm vi task):
- Sau khi deploy: chạy script recover docs/recovery/42784-reset-sync-lesson.sql trên production, chạy chế độ đếm trước rồi mới UPDATE.
- Web (sns-line) vẫn lưu friend_info lesson có phần tử null: cần điều tra và sửa riêng ở module web.
- Lỗi job sync form answer trong file đính kèm ticket cần một ticket riêng.
- Sau khi deploy D-4, người phụ trách chạy script docs/recovery/42784-reset-sync-form-answer.sql trên DB thật: điền @to bằng ngày #40734 lên production, chạy SELECT trước rồi UPDATE theo lô.
- Record form answer có result_error_google_id > 0 mà script D-5 liệt kê thì cần xử lý riêng; script không tự cập nhật các record này.
- Script recover lesson của v1 (docs/recovery/42784-reset-sync-lesson.sql) vẫn cần chạy sau khi deploy.
- Job form answer, nhánh dựng lại sheet rỗng: khi câu trả lời cũ có line user không tồn tại, ignoreSync đang gọi lên record đang xử lý thay vì bỏ qua câu trả lời cũ (lỗi cũ ngoài diff, trạng thái cuối vẫn đúng) — nên sửa ở ticket riêng.
- Kiểm trên production xem có ô sheet lesson đã ghi sai dạng {0=A, 2=B} trước bản sửa không; nếu có, cần dựng lại sheet hoặc cập nhật friend info các booking đó.

Điểm cần test:
- Booking có friend_info [{câu hỏi, giá trị}, null]: sync thành công, log có dòng #parseFriendInfo báo phần tử null, không có tin Chatwork nào cho case này.
- Các điểm kiểm thử khác của v1 giữ nguyên: append, dựng lại sheet rỗng, cập nhật friend info, insert bù, friend_info bình thường, script recover.
- Lesson: booking friend_info [{câu hỏi, giá trị}, null] sync OK, log có '#parseFriendInfo ... phan tu null', không có tin Chatwork.
- Lesson: value {"0":"A","2":"B"} => ô A,B; ["A","B"] => A,B; {} => ô trống; friend_info dạng object {"0":{..},"2":null} sync OK.
- Form answer 2 page (formType 2), sheet đã có dữ liệu: câu trả lời chỉ có data page 2 => dòng ở sheet page 2, status 1; câu trả lời có sẵn ở sheet page 1 => không ghi trùng, status 1.
- Form answer: record chỉ có marker trang hoặc page chỉ có upload_file => 1 dòng base, status 1 (hồi quy #40734).
- Form answer: line user không tồn tại, data rỗng/hỏng, page không thuộc form => không ghi dòng, status 4, log 'khong co dong nao duoc ghi => ignore'.
- Form answer: resume từ page lỗi => status 1 và result_error_google SUCCESS; sheet rỗng (dựng lại) => status 1 như cũ.
- Recover form answer: chạy SELECT trên dữ liệu thật trước; sau UPDATE + job chạy, record lên sheet, không trùng 回答ID, log 'synced X - ignored Y'.
- Recover lesson: SELECT bước 1 ra đúng record lỗi 'Exception: null'; sau UPDATE booking thiếu dòng xuất hiện trên sheet.

Branch: ai_studio_fixbug_42784
- linect-service: ai_studio_fixbug_42784 (nhánh gốc release-t09-2026 @0766bf5302ff, commit 4f769f7a757276a192b8e7bd93282fe68dc1e211)
```

**Journal #143597 — Thanh Duy Nguyen — 2026-10-13:**

```
Đã tạm recover friend info và chạy lại bản ghi cho khách

UPDATE calendar_sync_googles SET status = 0 WHERE id = 12307;
```

**Journal #145234 — Dev Studio — 2026-10-19:**

```
Dev handoff — 19/10 12:24 · nhánh ai_studio_fixbug_42784

Nguyên nhân:
friend_info của booking lesson là JSON array có phần tử null. `parseFriendInfo` giữ phần tử null trong danh sách, rồi `mappingFriendInfo` đọc giá trị của nó nên ném NullPointerException và lỗi hiện ra là "Exception: null". Lần retry nào cũng lỗi y hệt nên sau 5 lần record bị đánh lỗi. Nguyên nhân không đổi so với v1; v3 chỉ thu hẹp phạm vi sửa.

Nội dung thay đổi:
- Job sync Google Sheet lesson: booking có friend_info chứa phần tử null vẫn lên sheet; phần tử null bị bỏ qua; chỉ ghi log error '#parseFriendInfo friend_info co phan tu null', không gửi Chatwork.
- Job sync Google Sheet lesson: câu trả lời friend_info dạng object key số không liên tục hiển thị A,B (trước đây {0=A, 2=B}); object rỗng => ô trống.
- Job sync Google Sheet form answer: không thay đổi so với bản base (phần sửa của vòng 2 đã revert).
- Script recover lesson trong tài liệu task (docs/recovery/42784-reset-sync-lesson.sql).

File đã sửa (java-job):
  .../googlesheet/HandleCalendarSyncGoogleSheetTask.java     | 14 ++++++++++++++
  1 file changed, 14 insertions(+)

Đánh giá ảnh hưởng — Rủi ro thấp: 14 dòng trong 2 hàm private của job sync lesson, chỉ đổi kết quả ở các trường hợp trước đây lỗi hoặc ghi sai. Đã kiểm bằng harness trên class thật và kiểm chứng ngược; chưa verify runtime với Google Sheet thật.
- Lesson: thêm dòng booking mới, dựng lại toàn sheet, cập nhật friend info (type_sync=4), insert bù — đều dùng chung parseFriendInfo/parseFriendInfoValue.
- Lesson: friend_info bình thường (mảng, object câu hỏi, [], giá trị list/chuỗi/số/"0") phải giữ nguyên kết quả như trước.
- Job sync form answer: sau revert phải chạy y như base; nếu môi trường test từng chạy bản vòng 2 thì có thể còn record ở status 4.

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Đặt lại calendar_sync_googles lesson/sheet lỗi 'Exception: null' (friend_info có phần tử null) từ status 2 về 0 để job sync lại — docs/recovery/42784-reset-sync-lesson.sql: Bước 1: chạy câu SELECT trong file để lấy danh sách id. Bước 2: UPDATE calendar_sync_googles SET status = 0, updated_at = NOW() WHERE id IN (<id bước 1>) AND status = 2;

Recover dữ liệu: Cần recover — Các record sync lesson đã bị đánh lỗi sẽ không được retry, nên booking bị thiếu dòng trên sheet của khách. Phần recover form answer đã bỏ khỏi ticket.
- Ảnh hưởng: calendar_sync_googles (sheet, lesson) bị status=2 với lỗi 'Exception: null'
- Ảnh hưởng: Dòng booking bị thiếu trên Google Sheet lesson của khách
- Khoảng thời gian: Từ khi job Java sync lesson được bật trên production (commit b03c94939 ngày 15/09/2026, có trong release-t08-2026) tới khi bản sửa chạy
- Cách recover: Sau khi deploy, chạy docs/recovery/42784-reset-sync-lesson.sql: chạy phần đếm trước, rồi UPDATE status từ 2 về 0 với điều kiện status = 2 (chạy lại an toàn). Job sẽ tự sync lại.
- Ảnh hưởng tới khách: Chỉ ghi bổ sung các dòng còn thiếu lên Google Sheet của chính khách, không gửi tin nhắn nào.

Lưu ý khi deploy:
- Chỉ deploy module job (linect-service). Script recover lesson chạy sau khi bản job mới đã chạy.

Việc cần người làm thêm (ngoài phạm vi task):
- Lỗi sync form answer bị đánh dấu SYNC dù không ghi được dòng nào (file đính kèm ticket) đã bỏ khỏi ticket này; nếu vẫn cần sửa thì tạo ticket riêng.
- Sau khi deploy: chạy script recover lesson docs/recovery/42784-reset-sync-lesson.sql, chạy phần đếm trước rồi mới UPDATE.
- Web (sns-line) vẫn lưu friend_info lesson có phần tử null; cần điều tra và sửa riêng ở module web.
- Sau khi deploy, người phụ trách chạy script docs/recovery/42784-reset-sync-lesson.sql trên DB thật để sync lại các booking lesson đã hết lượt retry.
- Bug form answer trong file đính kèm ticket (record không ghi được dòng nào vẫn bị đánh dấu đã sync, cần recover record cũ) đã bỏ khỏi ticket theo quyết định của Duy NT — mở ticket riêng nếu vẫn muốn xử lý.
- Kiểm trên production xem có ô sheet lesson đã ghi sai dạng {0=A, 2=B} trước bản sửa không; nếu có, cần dựng lại sheet hoặc cập nhật friend info các booking đó.

Điểm cần test:
- Diff nhánh so với base chỉ còn file sync lesson; file sync form answer không khác base.
- Compile lại sau revert theo cách các vòng trước (bản sao /tmp và dependency tạm, không commit build.gradle).
- Hồi quy lesson: booking có friend_info [{...}, null] sync được, chỉ ghi log, không gửi Chatwork.
- Hồi quy lesson: value {"0":"A","2":"B"} ra A,B; value dạng array như cũ.
- Sync form answer chạy như bản base.
- Lesson: booking friend_info [{câu hỏi, giá trị}, null] (null ở đầu/giữa/cuối) sync OK cả khi append lẫn khi dựng lại sheet; log có '#parseFriendInfo ... phan tu null'; không có tin Chatwork.
- Lesson: value {"0":"A","2":"B"} => ô A,B; ["A","B"] => A,B; {} => ô trống; friend_info dạng object {"0":{..},"2":null} sync OK.
- Lesson: cập nhật friend info (type_sync=4) của booking có phần tử null => các cột cập nhật đúng.
- Form answer: câu trả lời bình thường vẫn lên sheet, status 1 như bản base.
- Recover lesson: SELECT bước 1 ra đúng record lỗi 'Exception: null'; sau UPDATE và job chạy, booking thiếu dòng xuất hiện trên sheet.

Branch: ai_studio_fixbug_42784
- linect-service: ai_studio_fixbug_42784 (nhánh gốc release-t09-2026 @0766bf5302ff, commit ef1e3561fdba63c5fc700b81c78d4bd2f838f26c)
```
