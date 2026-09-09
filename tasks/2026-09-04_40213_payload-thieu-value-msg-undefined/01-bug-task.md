# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40213 — [LME-Studio] Payload thiếu trường giá trị làm hàm lưu thông tin bạn bè crash: phản hồi thất bại TRỐNG (hộp thoại hiện 「undefined」) và dữ liệu bị ghi dở dang` |
| Redmine URL | https://redmine.watermelon.vn/issues/40213 |
| Auto-filled | `2026-09-04 by /new-task` |
| Ngày báo cáo | `2026-08-26` |
| Khách hàng / PM báo | `AI Auto test Lme` (tracker: Bug Tester — bug do LME Test Studio tự sinh, KHÔNG phải khách hàng báo) |
| Module / Màn hình | Chat 1:1 (FA-001) — tab 「友だち情報」 / modal 「友だち情報の表示」 · endpoint `POST /ajax/saveSettingDisplayInfoV2` <br> *(Redmine không có category; giá trị lấy từ Studio task #271 `feature = chat-1on1` + `screen` của bộ TC — tester verify lại)* |
| Priority | `Medium` (Redmine priority = Normal; **lưu ý** description ghi `severity High`) |
| Môi trường phát hiện | `Local` — runner LME Test Studio (`/workspace/source/sns-line--runner-slot-0-web`). **KHÔNG** phát hiện trên Production/Staging. |
| Trạng thái Redmine | `Fix done - Đợi test` · assigned_to = `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

*Bug từ LME Test Studio* — severity High
Task: #229
Test case: NEW-17

> ⚠️ **Lưu ý provenance**: `Task: #229 / Test case: NEW-17` ở trên là task Studio **NƠI PHÁT HIỆN** bug này. Task Studio dùng để **test bản fix của #40213** là **task #271** (round 1, branch `ai_fixbug_38944`). Task #271 cũng có một TC tên `NEW-17` nhưng là TC KHÁC (do `trangnq@mcp` thêm ngày 2026-09-04) — đừng nhầm hai TC này.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

*Các bước tái hiện:* (nguyên văn)

1. Đăng nhập admin web, chọn bot có mục thông tin bạn bè kiểu 「選択肢」 (2 lựa chọn) chưa nằm trong danh sách hiển thị của khung chat 1:1.
2. Ghi lại danh sách mục đang hiển thị và vị trí cuối file storage/logs/laravel.log.
3. Gửi POST /ajax/saveSettingDisplayInfoV2 kèm cookie phiên và mã chống giả mạo, với lineId = mã bạn bè, idsDelete = [], sortList = {"sort_ids":"","sort_position":[]} và infos = [{"id":"","bot_id":<bot>,"type":1,"id_setting":<mục 選択肢>,"type_data":1,"title":"<tên mục>","valueOption":[{"value":"オプションA"},{"value":"オプションB"}]}] — cố ý BỎ HẲN khóa "value".
4. Đọc mã trạng thái HTTP và nguyên văn nội dung phản hồi.
5. Đọc phần nhật ký mới sinh ra trong storage/logs/laravel.log.
6. Mở Chat 1:1 → tab 「友だち情報」 ở cột phải và so sánh danh sách mục với lúc trước khi gọi.

## Expected result

*Kết quả mong đợi:* (nguyên văn)

Endpoint phải cho kết quả XÁC ĐỊNH: nhật ký KHÔNG có dòng "Undefined property: stdClass::$value", và phản hồi hoặc báo thành công, hoặc báo thất bại KÈM msg giải thích lý do dữ liệu không hợp lệ. FE hiển thị alert(data.msg) nên msg rỗng làm người dùng thấy hộp thoại 「undefined」. Không được để lại dữ liệu ghi dở dang (hàm không mở transaction).

## Actual result

*Kết quả thực tế:* (nguyên văn)

[api] Lưu danh sách hiển thị khi một mục tùy chỉnh thiếu trường giá trị — điểm dùng chung chưa được vá — KHÔNG ĐẠT 2/3 điểm kiểm: phản hồi XÁC ĐỊNH: hoặc báo thành công, hoặc báo thất bại KÈM thông báo giải thích (body={"success":false}) | nhật ký KHÔNG có dòng "Undefined property: stdClass::$value" (thực tế=1 · mong đợi=0 · [2026-08-26 15:13:47] testing.ERROR: ErrorException: Undefined property: stdClass::$value in /workspace/source/sns-line--runner-slot-0-web/app/Http/Controllers/ChatController.php:4717) — Ghi chú: danh sách hiển thị: trước=4 mục, sau=5 mục — đã THÊM: TC38944_選択2 | Ghi dở dang: dòng danh sách hiển thị đã được tạo TRƯỚC điểm crash (saveSettingDisplayInfoV2 không mở transaction — DB::beginTransaction bị comment)

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- `log` — https://redmine.watermelon.vn/attachments/download/29419/log

## Ghi chú thêm của Leader

- ⚠️ **Phạm vi fix ĐÃ BỊ THU HẸP so với 3 kỳ vọng của ticket.** Dev (Auto-fixbug, journal 2026-08-26) chỉ sửa **1 dòng**: thêm msg 「保存に失敗しました。入力内容をご確認ください。」 vào nhánh thất bại. **Cố ý KHÔNG fix** 2 kỳ vọng còn lại theo quyết định của human:
  - kỳ vọng "log không còn `Undefined property: stdClass::$value`" → **vẫn còn** (không bọc `isset`);
  - kỳ vọng "không để lại dữ liệu ghi dở dang" → **vẫn còn** (transaction vẫn bị comment).
  ⇒ Khi review TC, 2 nhóm TC bám 2 kỳ vọng này **được dự báo Không đạt theo thiết kế**, không phải bug mới. Leader cần quyết: sửa expected của TC, hay tách ticket riêng.
- ⚠️ **Mâu thuẫn nội tại trong file 03**: mục 4.2 ghi *"từ nay được hoàn tác bằng giao dịch"* nhưng mục 2 ghi rõ *"KHÔNG bật lại giao dịch"*. Kết quả chạy thật (Studio run #840) xác nhận **dữ liệu vẫn ghi dở dang** ⇒ câu ở 4.2 là **SAI**. Xem cảnh báo trong `03-dev-impact.md`.
- Bug không do khách hàng báo — do AI Auto test sinh từ Studio task #229. TCs verify fix nằm ở Studio task #271 (đã fetch vào `04-tc-list.md`).
