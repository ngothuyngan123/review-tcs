# 01 — Bug Task từ khách hàng

> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45671 — [MCP] Re-test tool tạo/update dữ liệu Broadcast, Template, Scenario (validate + lưu DB + loại tin nhắn + send LINE)` |
| Module / Màn hình | `LME MCP server — tool tạo/update của Broadcast (配信), Template (mẫu tin), Scenario (kịch bản) + tool dùng chung (action, filter, folder)` |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Tracker **Test** — đây **KHÔNG phải bug** khách hàng báo, mà là **task QA tự khởi tạo** (author: AI LME CSS theo yêu cầu QA Leader) để re-test toàn bộ MCP tool liên quan đến TẠO / UPDATE dữ liệu của Broadcast, Template, Scenario. TCs nên bám theo nội dung mô tả dưới đây (đã có đủ scope + tool list + rule bắt buộc), KHÔNG cần khung Steps to reproduce / nguyên nhân-cách fix.

MỤC ĐÍCH
Re-test toàn bộ MCP tool liên quan đến TẠO / UPDATE dữ liệu của Broadcast (配信), Template (mẫu tin), Scenario (kịch bản) trên LME MCP server — đảm bảo hành vi (validate + dữ liệu lưu DB + gửi LINE) tương đương tính năng tương ứng bên web.

Phạm vi: chỉ TẠO / UPDATE. MCP hiện KHÔNG expose tool XÓA (delete) cho broadcast/template/scenario → không đưa thao tác xóa vào task này (xác nhận lại danh sách tool thực tế ở `_tool-inventory.md` khi review docs).

**TOOL TRONG PHẠM VI**

- Broadcast: `list_broadcasts` · `list_broadcast_templates` · `create_broadcast` · `update_broadcast`
- Scenario: `list_scenarios` · `get_scenario_detail` · `create_scenario` · `update_scenario` · `create_scenario_step` · `update_scenario_step`
- Template: `list_templates` · `get_template_detail` · `create/update_text_template` · `create/update_image_template` · `create/update_form_template` (Form/Carousel) · `create/update_location_template` · `create/update_group_template` · `get_group_template_detail`
- Dùng chung / hỗ trợ: `create/update_action` · `create/update_filter` · `filter_friends` · `list_folders` · `create_folder` · `update_folder`

Ghi chú: các tool `list_*` / `get_*` ở trên là công cụ dùng cho bước "get sau ghi" (verify từng param đã lưu đúng).

**PHẦN A — VALIDATE & LƯU DB & LOẠI TIN NHẮN (trọng tâm chính, test tự động)**

1. Validate đầy đủ như web — áp mọi kịch bản validate của màn web tương ứng sang MCP (thiếu field bắt buộc, null, rỗng/chỉ khoảng trắng, sai kiểu, ngoài enum, biên ký tự/số lượng, param phụ thuộc theo type, param lạ không lưu rác). Chặn cả kịch bản web chặn ngầm. 400 hoặc 422 đều Đạt, message tiếng Anh/khác web OK. Test sai kiểu dữ liệu phải qua **raw MCP client**. 2 rule bắt buộc đi kèm: **không trùng tên quản lý (管理名)** trong cùng bot (cùng tên bot khác → cho phép) · **limit bot Free** đếm gộp web + MCP (copy/khôi phục trên web khi đã đủ limit cũng bị chặn).
2. Dữ liệu lưu DB giống web mọi case (đặc biệt file/ảnh/media) — mỗi create/update thành công phải `get_*` verify từng param + đối chiếu editor web. Media đối chiếu qua `get_image/video/audio/pdf_fileparams` (path, mime, size, thumbnail). Imagemap: số vùng tap + toạ độ + action từng vùng.
3. Phủ đủ các loại tin nhắn (ở cả template và broadcast/scenario step): text · image · image map · video · rich video · audio · location · sticker · button standard · button color · button image · button quick. Mỗi button gắn từng loại action (URL, tin nhắn, postback, gắn tag, chạy scenario); sticker packageId/stickerId hợp lệ vs không hợp lệ; text token thay thế (友だち名, URL token); carousel/nhiều bubble giữ thứ tự.
4. Bảo mật & phân quyền (rule MCP bắt buộc) — bảo mật bot A↔B: truyền ID con của bot B (template_id, scenario_id, tag_id, action_id, folder_id, lmePage.id...) → 403/404, dữ liệu bot B không đổi (4 giá trị: ID bot khác cùng account · ID account khác · ID không tồn tại · ID sai loại). Phân quyền staff: staff không có quyền tính năng → mọi tool bị chặn kể cả `list_*`/`get_*` (403); quyền bị thu hồi khi OAuth token còn hiệu lực → lần gọi kế tiếp vẫn bị chặn.

**PHẦN B — SEND LINE SUCCESS (tách nhóm riêng, chạy MANUAL)**

Lý do tách riêng: AI test hiện CHƯA kiểm thử được việc gửi thành công phía LINE (cần mắt người xác nhận tin tới app LINE thật). Nhóm này chạy manual, phạm vi env phải có `prd`.

5. Gửi tin thật tới LINE — template + action tạo qua MCP → gửi tới friend LINE thật → verify nhận được + render đúng từng loại tin (chú ý imagemap, carousel, button image, sticker, video/rich video, audio, location). Broadcast gửi thật: filter/絞り込み配信 áp đúng tập người nhận; 予約配信 (đặt lịch) → job nền gửi đúng thời điểm. Scenario: đăng ký friend → job nền bắn từng step đúng thời điểm/thứ tự/delay. Button action bấm trên LINE chạy đúng.

**PHẦN C — E2E QUA CLIENT AI (rule MCP-RULE-08, chạy MANUAL)**

6. Prompt ngôn ngữ tự nhiên — prompt chi tiết (MCP-E2E-001) + prompt chung (MCP-E2E-002), VN chính + JP đại diện, cho mỗi tool ghi. Oracle: chuỗi tool gọi đúng + thứ tự + param resolve đúng bot + trạng thái cuối khớp (`get_*` + màn web) — KHÔNG chấm câu trả lời chữ. Prompt abnormal: thiếu dữ liệu bắt buộc · nhắc tên không tồn tại · thao tác dữ liệu bot khác · account staff không có quyền.

**MÔI TRƯỜNG TEST**
- Case validate/lưu DB/bảo mật/phân quyền: `dev, local, staging` (tự động).
- Case send LINE/media gửi thật/job gửi/đặt lịch/E2E qua client AI: bắt buộc có `prd`, chạy manual.

## Steps to reproduce

<!-- Không áp dụng — task QA re-test theo scope, không phải bug tái hiện. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment trên Redmine (0).

## Ghi chú thêm của Leader

- ⚠️ Ticket **không phải bug tái hiện** — task QA tự khởi tạo để re-test scope MCP tool broadcast/template/scenario. TCs bám theo mô tả ở trên (6 mục Phần A/B/C) thay vì khung Steps to reproduce.
- Phạm vi task **chỉ TẠO / UPDATE** — không có thao tác XÓA (MCP không expose tool delete cho broadcast/template/scenario).
- Phần B (send LINE success) và Phần C (E2E qua client AI) **chạy manual**, tách riêng khỏi Phần A (automation) — AI test hiện chưa kiểm thử được việc gửi thành công phía LINE.
- Studio **đã có task #566** (feature `broadcast`) cho ticket này, status `writing-tc`, đã sinh **111 TC** (100% do tool/AI viết, 0% chạy) — xem `04-tc-list.md`.

## Journal / note từ Redmine (nguyên văn)

<!-- Không có journal nào có notes (ticket mới tạo, 0 journal). -->
