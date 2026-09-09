# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38871 — [Broadcast] [Modal filter] Khi xóa tag thì chưa xóa khỏi filter hiện tại` |
| Module / Màn hình | Broadcast (FA-008) — modal filter 「絞り込み」→「設定」 lọc đối tượng theo tag; liên đới màn Quản lý tag 「タグ管理」 (FA-012) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine đã viết sẵn bằng tiếng Việt — giữ nguyên văn, không dịch lại. -->

Thao tác:
1. Tạo broadcast có filter tag A
2. Vào màn quản lý tag xóa tag A đó
3. Quay lại màn broadcast => Click mở modal filter

BUG: Modal filter không hiển thị tên tag đã xóa. Check DB bảng `filters_v2` vẫn lưu tag đã filter và `text_preview` cũng vẫn hiển thị filter tag đã bị xóa
=> Expect: Khi xóa tag thì xóa khỏi filter

## Steps to reproduce

1. Tạo broadcast có filter tag A
2. Vào màn quản lý tag xóa tag A đó
3. Quay lại màn broadcast => Click mở modal filter

## Expected result

- Khi xóa tag thì xóa khỏi filter — tag A phải bị gỡ khỏi bộ lọc của broadcast, kể cả dưới DB.

## Actual result

- Modal filter không hiển thị tên tag đã xóa.
- Check DB bảng `filters_v2`: vẫn lưu tag đã filter, và `text_preview` cũng vẫn hiển thị filter tag đã bị xóa.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/28266/tag-1.png
- https://redmine.watermelon.vn/attachments/download/28267/tag-2.png

## Ghi chú thêm của Leader

- **Ticket do AI auto-detect** (tracker `Bug tự detect`), status hiện tại `Fix done - Đợi test`. Người tạo & assignee: Ngô Thúy Ngần. Fix do hệ thống **Auto-fixbug LME** thực hiện (journal #132539), branch `ai_fixbug_38871`, commit `44884f971e`, 1 file, 48+/29-.
- ⚠️ **Bug KHÔNG tái hiện được trên dev khi fix** — journal ghi rõ MySQL `host.docker.internal:3306` báo *Connection refused*, web `:8000` không phản hồi. Root cause dựa trên **phân tích code tĩnh** + bằng chứng ép kiểu ở 10 chỗ đọc filter. Nếu môi trường KH có nguyên nhân khác (vd bộ lọc lưu `bot_id` khác) thì fix này chưa đủ.
- ⚠️ **Fix chỉ đúng cho các lần xóa tag TỪ NAY.** Dữ liệu bộ lọc đã bị bỏ sót trước đó (gồm chính broadcast trong ticket) **vẫn còn id tag không tồn tại + `text_preview` cũ**; tag đã bị xóa nên không còn sự kiện nào kích hoạt dọn lại. Dev ghi nhận cần script dọn 1 lần nhưng **ngoài phạm vi ticket, chờ human quyết định**. → Khi test phải dùng **data mới tạo**, không dùng lại data cũ của ticket (sẽ fail dù fix đúng).
- ⚠️ **Thay đổi hành vi có chủ ý**: bản ghi `filters_v2` chỉ khớp `LIKE` do trùng chuỗi con nay được **giữ nguyên** thay vì bị ghi đè `text_preview` (code cũ có thể ghi đè, thậm chí xóa nhầm khi thiếu trường `tags_search`). Đây là hành vi MỚI so với code cũ — cần verify, không coi là bug.
- **Yokoten chưa xử lý**: bản sao y hệt ở API app `TagMobileController::deletedDataTag` **chưa sửa** — Dev ghi nhận, không thuộc phạm vi ticket web này.
- **Liên quan**: `#38700` đã lo phần ẩn hiển thị tag đã xóa trên UI (nên modal không hiện tên tag dù DB còn lưu). Parent `#26684` là ticket umbrella nên fix không gộp branch.
- **Phạm vi rộng hơn broadcast**: `filters_v2 type='tag'` dùng chung cho mọi `parent_type` — `broadcast` / `step_message` / `auto_reply` / `modal_action` / `action_schedule` / `filter_manager`.
- **Tần suất**: ticket không ghi tỷ lệ tái hiện. Theo root cause, lỗi chỉ kích hoạt khi bot có **ít nhất 1 bản ghi filter lệch dạng** → không phải 100% mọi bot.

## Journal / note từ Redmine (nguyên văn)

**Journal #132539 — AI LME Fix bug — 2026-08-24:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi xóa tag, hàm dọn dữ liệu của màn quản lý tag quét mọi bộ lọc tag của bot bằng LIKE rồi giả định danh sách tag trong bộ lọc luôn là mảng id sạch. Chỉ cần 1 bản ghi bộ lọc bất kỳ trong bot lưu khác dạng (id đơn lẻ, thiếu trường, hoặc dạng đối tượng {id,name} kiểu cũ) là vòng lặp văng lỗi, bị khối bắt lỗi bao ngoài nuốt và dừng dọn toàn bộ các bộ lọc còn lại — nên bộ lọc của broadcast vẫn giữ tag đã xóa kèm text_preview cũ. Mọi nơi ĐỌC bộ lọc trong hệ thống đều đã ép kiểu mảng cho trường này, riêng chỗ dọn lúc xóa thì không.

■ 2. CÁCH FIX
Làm chắc bước dọn bộ lọc khi xóa tag trong TagController::deletedDataTag (fix ĐỘC LẬP branch ai_fixbug_38871, parent Redmine #26684 là ticket umbrella nên không gộp branch): (1) mỗi bộ lọc được xử lý trong khối bắt lỗi riêng nên 1 bản ghi dữ liệu lệch dạng không còn chặn việc dọn các bộ lọc còn lại (và không chặn luôn phần dọn action + gỡ tag khỏi bạn bè phía sau); (2) chuẩn hóa danh sách tag của bộ lọc về mảng id trước khi so khớp (chấp nhận id đơn lẻ hoặc phần tử dạng {id,name} của dữ liệu cũ); (3) chỉ sửa/xóa bộ lọc THỰC SỰ chứa tag vừa xóa — bản ghi chỉ khớp do trùng chuỗi con giữ nguyên (trước đây bị ghi đè text_preview, thậm chí bị xóa nhầm khi thiếu trường tags_search). Bộ lọc hết tag vẫn bị xóa và text_preview vẫn được dựng lại theo tag còn lại như cũ. Yokoten: bản sao y hệt ở API app (TagMobileController) chưa sửa — ghi nhận, không thuộc phạm vi ticket web này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
TagController::deletedDataTag (app/Http/Controllers/Basic/TagController.php) — hàm dọn dữ liệu khi xóa tag, chỗ sửa
TagController::ajaxDeleteTags (app/Http/Controllers/Basic/TagController.php) — xóa tag từ màn quản lý tag v2, gọi deletedDataTag
TagController::deleteTag / manageTag case deleteTag|deleteGroup (app/Http/Controllers/Basic/TagController.php) — các đường xóa tag còn lại, cùng gọi deletedDataTag
FilterV2::saveFilter (app/FilterV2.php) — nơi ghi bộ lọc tag, xác nhận cột type='tag' và bot_id
FilterV2::initDataFilter (app/FilterV2.php) — nơi đọc bộ lọc cho modal, xác nhận đều ép kiểu (array) tags_search
BroadcastV2Controller::saveBroadcast / getDataFilter (app/Http/Controllers/Basic/BroadcastV2Controller.php) — vòng đời bộ lọc của broadcast (parent_type='broadcast')
TagMobileController::deletedDataTag (app/Http/Controllers/Api/Mobile/TagMobileController.php) — bản sao cùng pattern, chỉ rà không sửa

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/TagController.php
 • 4.2 Data ảnh hưởng:
   - filters_v2.data / filters_v2.text_preview — dòng lọc type='tag' của bot: nay được gỡ id tag vừa xóa (hoặc xóa cả dòng khi không còn tag) đúng như kỳ vọng ticket
   - filters_v2 — bản ghi chỉ khớp LIKE do trùng chuỗi con nay KHÔNG còn bị ghi đè text_preview / xóa nhầm (giảm rủi ro mất dữ liệu so với trước)
   - tag_line_user + actions/action_detail — phần dọn phía sau vòng lặp bộ lọc nay luôn chạy tới nơi, không bị dừng giữa chừng do 1 bộ lọc lỗi
 • 4.3 Tính năng liên quan:
   - Tag Management (FA-012) — xóa tag dọn sạch tham chiếu trong bộ lọc, bền với dữ liệu bộ lọc lệch dạng
   - Friend Filter / Segment (SC-003) — bộ lọc bạn bè theo tag được cập nhật/xóa đúng khi tag bị xóa
   - Broadcast (FA-008) — bộ lọc đối tượng của tin gửi hàng loạt không còn giữ tag đã xóa (triệu chứng báo trong ticket)
   - Step Delivery / Scenario (FA-009), Auto Reply (FA-003) — bộ lọc tag của các tính năng này cùng dùng chung bảng filters_v2 nên cũng được dọn đúng

■ 5. RECOVER DATA
   ⚠ CÓ — Fix chỉ đúng cho các lần xóa tag TỪ NAY. Các bộ lọc đã bị bỏ sót trước đó (gồm chính broadcast trong ticket) vẫn còn id tag không tồn tại + text_preview cũ trong filters_v2; tag đã bị xóa nên không còn sự kiện nào kích hoạt dọn lại. Cần 1 script dọn 1 lần (rà filters_v2 type='tag', bỏ id không còn trong bảng tags, dựng lại text_preview, xóa dòng nếu rỗng) — chờ human quyết định vì nằm ngoài phạm vi ticket. (phạm vi: filters_v2 (type='tag') của các bot có tag đã xóa — mọi parent_type: broadcast / step_message / auto_reply / modal_action / action_schedule / filter_manager)

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/TagController.php: No syntax errors detected; script PHP tách riêng test logic chuẩn hóa tags_search 6 dạng (mảng id / 1 tag / id đơn lẻ / dạng {id,name} cũ / thiếu trường / chỉ trùng chuỗi con): ALL PASS; git diff --stat release_step_20260805...ai_fixbug_38871: 1 file, 48+/29-
   Bằng chứng: 10 chỗ ĐỌC bộ lọc trong repo đều ép kiểu (array) tags_search (FilterV2:907,1139 · FilterController:344,587 · CrossAnalysisController:1100,1353 · ActionScheduleController:1665 · FriendlistController:4554 · FilterV2Replicate:566,772) ⇒ dữ liệu trường này thực tế có dạng khác mảng; riêng nhánh dọn lúc xóa không phòng vệ; Ngay trong cùng hàm deletedDataTag, nhánh dọn action đã chủ động ép kiểu ((array)$data['ids']) cho trường danh sách tương tự ⇒ pattern lệch dạng là có thật trong dữ liệu; KHÔNG kiểm chứng được bằng data runtime: MySQL host.docker.internal:3306 báo Connection refused và web :8000 không phản hồi tại thời điểm xử lý

■ TỰ REVIEW (AI)
Fix nằm gọn trong 1 hàm dọn dữ liệu, giữ nguyên hành vi mong muốn (gỡ tag khỏi bộ lọc, xóa bộ lọc khi hết tag, dựng lại text_preview) và chỉ thêm lớp phòng vệ: xử lý độc lập từng bộ lọc + chuẩn hóa dạng dữ liệu + chỉ ghi khi bộ lọc thực sự chứa tag vừa xóa. Không đổi API, không đổi schema, không đụng luồng đọc/hiển thị (#38700 đã lo phần ẩn hiển thị).
 • Rủi ro / lưu ý khi test:
   - Chưa tái hiện được trên dev (DB/web dev down) nên root cause dựa vào phân tích code + bằng chứng ép kiểu ở 10 chỗ đọc; nếu môi trường KH có nguyên nhân khác (vd bộ lọc lưu bot_id khác) thì fix này chưa đủ — cần log lỗi 'deletedDataTag filter_id ... error' mới thêm để chẩn đoán tiếp
   - Dữ liệu cũ đã bỏ sót không tự dọn (xem mục recover data)
   - Bản ghi chỉ khớp LIKE nay được giữ nguyên thay vì bị ghi đè text_preview — đây là chủ ý (tránh mất dữ liệu), nhưng là thay đổi hành vi so với code cũ

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_38871 (nhánh gốc release_step_20260805, commit 44884f971e, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 12 phút 55 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=1e38daf1-e884-4639-9826-c650e05d7283
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38871
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
