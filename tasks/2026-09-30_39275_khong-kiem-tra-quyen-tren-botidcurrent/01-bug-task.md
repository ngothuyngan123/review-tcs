# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39275 — [LME-Studio] Không kiểm tra quyền trên botIdCurrent: tài khoản quản trị khác có thể đánh dấu đã xác nhận toàn bộ hội thoại của bot không thuộc quyền` |
| Module / Màn hình | `Chat 1:1 (FA-001) — API POST /basic/chat/confirm-message, kích hoạt bởi nút 「全て確認済みに変更」(chuyển tất cả thành đã xác nhận) ở màn chat 1:1` |

## Mô tả bug (bản dịch tiếng Việt)

Bug từ LME Test Studio — severity High. Task: #48 (Studio, tại thời điểm ticket được tạo — task hiện tại trên Studio là #238, xem ghi chú Leader bên dưới). Test case: NEW-33.

## Steps to reproduce

1. Chuẩn bị 2 tài khoản quản trị: X sở hữu bot A, Y sở hữu bot B (bot B có hội thoại chưa xác nhận kèm bản ghi tin chưa xác nhận).
2. Đăng nhập bằng tài khoản X và chọn bot A làm bot hiện tại.
3. Gửi POST /basic/chat/confirm-message với bộ tham số bình thường nhưng đặt botIdCurrent = định danh bot B.
4. Truy vấn lại các hội thoại và bản ghi tin chưa xác nhận của bot B.

## Expected result

- Yêu cầu bị từ chối hoặc bị giới hạn trong phạm vi bot mà tài khoản đang đăng nhập có quyền; dữ liệu bot B giữ nguyên 4 cờ, thời điểm cập nhật và bản ghi tin chưa xác nhận.

## Actual result

- KHÔNG ĐẠT (2/3 điểm kiểm tra): không hội thoại nào của bot B bị đổi (4 cờ + thời điểm cập nhật) | bản ghi tin chưa xác nhận của bot B còn nguyên (thực tế 0/6).
- Tái hiện ở run #105 (vòng 1, local): KHÔNG ĐẠT (2/3 điểm kiểm tra) — cùng nội dung trên.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- log TC 7884 — https://redmine.watermelon.vn/attachments/download/28663/log%20TC%207884
- log TC 7884 — https://redmine.watermelon.vn/attachments/download/28664/log%20TC%207884

## Ghi chú thêm của Leader

- Severity: **High** (khai báo trong description).
- ⚠️ **Timeline ticket đáng chú ý** — không phải bug mới, đã đi qua nhiều vòng:
  - 2026-08-25 (journal #132965): Dev **reject** bug #318 lần đầu, lý do "fix sau".
  - 2026-08-26 (journal #133051): AI Auto-fixbug đã fix xong trên branch `ai_fixbug_39275` — nội dung đầy đủ ở `03-dev-impact.md`.
  - 2026-09-20 (journal #137272): "Gom task fix bug -> Refer #41144" — ticket này có thể đã bị **gộp/theo dõi tiếp ở #41144**. Leader nên đối chiếu thêm ticket #41144 trước khi chốt review, tránh lệch/trùng phạm vi.
  - 2026-09-30 (journal #139363, tác giả Ngô Thúy Ngần): "Mở lại ticket để test" — ticket đang ở status **Re-open**.
- Task trên **MCP LME TEST STUDIO** ứng với ticket này hiện là **task_id = 238** (không phải #48 như ghi trong description gốc — có thể do renumber hệ thống Studio; đã xác nhận qua `task_list(ticket_id=39275)` chỉ trả đúng 1 kết quả, không archived, round 1).
- Task #238 có **21 TC**, exec 20 pass / 1 fail, **toàn bộ chỉ chạy trên môi trường `local`** (0 TC ở dev/staging/prd) → theo RULE-08, **chưa đủ căn cứ** kết luận hành vi thật trên production/staging cho các case nhạy cảm (nếu có).
- 1 TC **fail** trên Studio: `NEW-20` — "Gửi mã bot sai kiểu dữ liệu — bị từ chối sạch, không lỗi hệ thống" — hiện **chưa gắn ticket bug** nào. Leader lưu ý khi đọc coverage ở file 05.
- 9/15 mã quan điểm mà Studio gắn cho các TC **không có trong `framework/checklist-lme.md`** (`AUTH-SESSION-001`, `SELECT-SCOPE-001`, `RULE-12`, `TOOL-OLDREC-001`, `API-001`, `TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `OBS-001`, `TOOL-ERRHYG-001`) — `/review-tc` sẽ không map coverage được cho các mã này, cần đọc trực tiếp nội dung TC khi review.
- Dev tự nêu **yokoten** (quét ngang) trong journal #133051: còn **~10 endpoint chat khác** dùng `botIdCurrent` thô kiểu tương tự (xoá thẻ, thao tác nhanh, gửi tin/gửi file ở controller chat cũ) **chưa được sửa trong ticket này** — cần ticket riêng. Đây là GAP ngoài phạm vi fix hiện tại, không phải regression của chính bug #39275.

## Dữ liệu định danh ca lỗi

<!-- Ticket dùng nhãn vai trò (bot A / bot B, tài khoản X / Y) thay vì ID cụ thể — không có bot_id / line_user_id thật trong nội dung Redmine. -->

| Mục | Giá trị |
|---|---|
| bot_id | `<không có ID cụ thể — mô tả vai trò: bot A (chủ = tài khoản X), bot B (chủ = tài khoản Y)>` |
| Friend | `<không nêu cụ thể — chỉ yêu cầu bot B có ≥1 hội thoại chưa xác nhận kèm bản ghi tin chưa xác nhận>` |
| Đối tượng cấu hình | `botIdCurrent (tham số request POST /basic/chat/confirm-message)` |
| Thời điểm lỗi | `Tái hiện ở run #105 (vòng 1, môi trường local)` |
| Đối chứng | `<không nêu case đối chứng trong Redmine>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #132965 — AI Auto test Lme — 2026-08-25:**
```
[LME Test Studio] Reject bug #318

Lý do: fix sau
```

**Journal #133051 — AI LME Fix bug — 2026-08-26:**
```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Endpoint "đánh dấu đã xác nhận toàn bộ hội thoại" của màn chat 1:1 lấy thẳng tham số botIdCurrent do trình duyệt gửi lên làm id bot rồi cập nhật hội thoại và xoá bản ghi tin chưa xác nhận theo id đó, nhưng không hề kiểm tra tài khoản đang đăng nhập có quyền trên bot đó hay không. Tham số này sinh ra để xử lý trường hợp mở nhiều tab (tab cũ còn giữ bot đã chọn lúc mở trang), nên hoàn toàn do phía trình duyệt quyết định. Hậu quả: một tài khoản quản trị bất kỳ chỉ cần đổi botIdCurrent thành id bot của người khác là xoá sạch dấu chưa xác nhận và đổi trạng thái toàn bộ hội thoại của bot đó; ngoài ra số hội thoại chưa xác nhận lại được ghi cho bot trong phiên đăng nhập nên hai bên đều lệch.

■ 2. CÁCH FIX
Thêm kiểm tra phạm vi bot ở đầu endpoint xác nhận toàn bộ hội thoại: dùng helper sẵn có getBotIdInScope để đối chiếu botIdCurrent do trình duyệt gửi lên với danh sách bot mà tài khoản đang đăng nhập được phép thao tác (bot của chính phiên đăng nhập vẫn đi thẳng như cũ, nên không phá luồng quản trị mở bot khách). Bot ngoài phạm vi thì ghi log cảnh báo và trả về thông báo không có quyền, không chạm vào dữ liệu. Bot hợp lệ thì dùng đúng id bot đã kiểm cho cả bước xử lý hội thoại lẫn bước cập nhật số hội thoại chưa xác nhận (trước đây đếm và ghi cho bot của phiên đăng nhập nên lệch với bot vừa xử lý). Quét ngang: cùng kiểu dùng botIdCurrent thô còn tồn ở nhiều endpoint chat khác (xoá thẻ, thao tác nhanh, gửi tin/gửi file ở controller chat cũ) — chỉ ghi nhận, không sửa ngoài phạm vi ticket.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ChatController::confirmReadMessage (app/Http/Controllers/Basic/ChatController.php:199)
ConversationService::confirmReadMessage (app/Services/ConversationService.php:264)
getBotIdInScope (app/Helpers/functions.php:397)
getListBotId (app/Helpers/functions.php:10658)
getBotId (app/Helpers/functions.php:386)
changeConfirm (public/js/chats/chat-v2.js:2925)
Route chat.confirmReadMessage (routes/web.php:1792)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/ChatController.php
 • 4.2 Data ảnh hưởng:
   - Không có (chỉ chặn ghi trái phép; không đổi cấu trúc bảng conversation / unconfirm_message / bots)
 • 4.3 Tính năng liên quan:
   - 1-on-1 Chat (FA-001) — nút "chuyển tất cả thành đã xác nhận" ở màn chat 1:1: nay chỉ chạy trên bot mà tài khoản đăng nhập có quyền, và số hội thoại chưa xác nhận được cập nhật đúng bot vừa xử lý

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/ChatController.php: No syntax errors detected; git diff --stat origin/release_step_20260805...ai_fixbug_39275: 1 file changed, 17 insertions(+), 3 deletions(-)
   Bằng chứng: Helper getBotIdInScope đã có sẵn trên release (app/Helpers/functions.php:397) và đang được 3 endpoint mẫu tin dùng cùng kiểu (TemplateV2Controller:1222/1424, TemplateService:2611) — fix tự chứa trên release, không phụ thuộc branch khác; Màn chat gửi botIdCurrent = Session current_bot_id lúc render trang (resources/views/basic/chat/index.blade.php:107) nên luồng hợp lệ luôn là bot thuộc quyền user ⇒ guard không chặn nhầm thao tác thật; Spec chat 1:1 (share/spec/spec-features/admin/chat-1on1/web/logic-spec.md:240) nêu nguyên tắc mọi query phải scope theo bot của phiên đăng nhập — fix đưa endpoint về đúng nguyên tắc này (mở rộng tối thiểu cho trường hợp nhiều tab, giới hạn trong các bot user có quyền); Không verify được runtime: MySQL dev host.docker.internal:3306 Connection refused tại thời điểm fix

■ TỰ REVIEW (AI)
Diff 1 file, 17 dòng thêm: chặn ghi chéo bot bằng helper đã có sẵn trên release, giữ nguyên luồng hợp lệ (bot của phiên đăng nhập đi thẳng, bot khác nhưng thuộc quyền user vẫn cho phép để không phá trường hợp mở nhiều tab). Trả HTTP 200 kèm success=false + thông báo tiếng Nhật đúng theo tiền lệ đã merge của cùng loại lỗi (#39153) vì JS các màn này không hiện gì ở nhánh lỗi HTTP. Bổ sung dùng đúng id bot đã kiểm cho bước cập nhật số hội thoại chưa xác nhận để đếm và ghi cùng một bot.
 • Rủi ro / lưu ý khi test:
   - Nếu có màn/luồng nào gọi endpoint này với botIdCurrent của bot mà user KHÔNG được cấp quyền (vd tài khoản hệ thống thao tác hộ mà không đổi session) thì sẽ bị chặn — đã rà: chỉ chat-v2.js gọi endpoint này và luôn gửi bot của session lúc render, nên rủi ro thấp
   - Trường hợp nhiều tab: nay số hội thoại chưa xác nhận được ghi cho bot trong botIdCurrent thay vì bot của session (đúng bot vừa xử lý) — thay đổi có chủ ý, khác hành vi cũ
   - Còn ~10 endpoint chat khác cùng kiểu lỗ hổng chưa sửa (đã liệt kê ở yokoten) — cần ticket riêng

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39275 (nhánh gốc release_step_20260805, commit f9c4705b1a, 1 file)  [đã push]
```

**Journal #137272 — AI LME CSS — 2026-09-20:**
```
Gom task fix bug -> Refer #41144
```

**Journal #139363 — Ngô Thúy Ngần — 2026-09-30:**
```
Mở lại ticket để test
```
