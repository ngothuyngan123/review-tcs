# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42764 — Auto reply – Route public detail & lưu/xoá auto reply` |
| Module / Màn hình | 自動応答 (Auto reply) — `Basic\ReplyController` (web, màn danh sách + tạo/sửa/sao chép) + `Api\Mobile\AutoreplyMobileController` (API mobile/MCP) |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Ticket này có nguồn gốc là **security audit IDOR** (Template / Broadcast / Scenario), không phải bug khách hàng báo qua reproduce steps thông thường. Mô tả dưới đây là nguyên văn nội dung audit (dịch sát), không phải "Steps to reproduce / Expected / Actual" kiểu cổ điển.

Controller: `Basic\ReplyController`
Nguồn: security audit IDOR (Template / Broadcast / Scenario)

**1. IDOR-MSG-10 [Immediate] — Auto reply · Route PUBLIC đọc/ghi detail auto reply**
- Vị trí: `Basic\ReplyController.php:910-946 initDataDetailAutoReply`, `:1061-1125 saveDataDetailAutoReply`
- Route: `POST /ajax/init-data-detail-auto-reply`, `/ajax/save-data-detail-auto-reply` (web.php:4124/4128) — **PUBLIC** · param `id`, `copyId`, `list_keyword[].id`, `action_id`, `category_id` (middleware: PUBLIC)
- Vấn đề / Fix: `AutoReply::where('id')` đọc/ghi; `Keyword::where('id')->update`; clone action → đưa route vào BASIC (cần login); scope theo `bot_id`; keyword theo `auto_reply_id` sở hữu

**2. IDOR-MSG-11 [High] — Auto reply · Lưu / xoá / move auto reply theo id**
- Vị trí: `Basic\ReplyController.php:298-413 save`, `:606-677 deleteItem(s)/moveItem`
- Route: `POST /basic/reply/save`, `/ajax/get-list-group` — **LOGIN** · param `item_id(s)` (middleware: LOGIN, nhưng không scope bot_id)
- Vấn đề / Fix: `AutoReply::findOrFail`, `Keyword` where `auto_reply_id` ->delete() → kiểm id sở hữu trước khi ghi/xoá

Cùng lỗ hở này còn tồn tại ở **API MCP/mobile** (`AutoreplyMobileController`) — phát hiện ở vòng v2 khi Dev review lại: init/save/delete/toggle/move auto reply theo id mà không kiểm bot (công cụ AI MCP `create_autoreply` / `update_autoreply` gọi `save-autoreply` cũng bị ảnh hưởng).

## Steps to reproduce

<!-- Không có — ticket gốc là audit tìm lỗ hổng qua đọc code, không phải case tái hiện cụ thể. Case tái hiện cụ thể nhất là bug con #43617 (xem Journal note bên dưới). -->

## Expected result

- Route init/save detail auto reply phải yêu cầu đăng nhập (không còn PUBLIC).
- Mọi id client gửi lên (auto reply id, copyId, action_id, category_id, keyword id, item_id(s)) chỉ được đọc/ghi/xoá khi thuộc `bot_id` đang đăng nhập (web) hoặc bot gọi API (MCP/mobile) — id của bot khác → chặn (403/404/400 tuỳ loại lỗi), không ghi gì.

## Actual result

- Route PUBLIC cho phép đọc/ghi detail auto reply không cần đăng nhập.
- Các thao tác lưu/xoá/move/toggle không kiểm id có thuộc bot hiện tại — id của bot khác vẫn thao tác được (IDOR), kể cả qua API MCP/mobile.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42764 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

- Ticket đi qua **7 vòng fix** (v1 → v7) trong cùng 1 branch `ai_studio_implement_42764`, có nhiều bug con phát sinh trong lúc fix (QA + automation Test Studio) — xem đầy đủ ở `03-dev-impact.md` và journal bên dưới.
- **2 ticket liên quan cùng tính năng, PHẢI phát hành cùng lúc để đóng hết các thao tác IDOR của bug con #43617**: `#42765` (IDOR thư mục auto reply — updateAutoreplyFolder / folder_move_id / buildListCategoryResponse ở API mobile **chưa fix**, vẫn còn lỗ) và `#42759` (modal action). → review/viết TC cho #42764 cần biết rõ ranh giới: KHÔNG cover phần thư mục API mobile (thuộc #42765) và modal action (thuộc #42759).
- Bản fix **chưa có trên nhánh release/staging nào** tại thời điểm journal cuối (2026-10-22): staging `release_staging_20261014_v3` chỉ mới có tới commit vòng 5 (`5640e9f98b`), vòng 6+7 (`2abe1c5ab5`, `ced6de1f9c`) chưa merge. QA/Test Studio retest phải dùng build từ branch `ai_studio_implement_42764`.
- Vòng 7 sửa JS (`create.js`) không tăng `sns-line.version` → tester/QA **phải Ctrl+F5 (hard reload)** trước khi test, nếu không sẽ chạy nhầm JS cũ.
- Dữ liệu lệch cũ trên production (không thuộc phạm vi fix, chỉ ghi nhận): auto reply id 24, 25 (bot 2) trỏ folder của bot 35; có 1 auto reply trỏ action đã mất — cần query phạm vi trên production và Recover data riêng nếu muốn.
- Không có migration / thay đổi schema DB ở bất kỳ vòng nào (Dev đã kiểm diff xác nhận).

## Journal / note từ Redmine (nguyên văn)

**Journal #142835 — Dev Studio — 2026-10-12:**
```
Dev Studio · Nội dung thực hiện (v1)

Thiết kế v1 đã xong, sẵn sàng thực thi. Hai route nạp/lưu chi tiết auto reply sẽ chuyển vào nhóm route cần đăng nhập, đúng như spec mô tả. Mọi id do client gửi lên (auto reply, bản sao, action, thư mục, keyword) đều được kiểm có thuộc bot đang đăng nhập không, ở các chỗ: lưu V2, lưu form cũ, xoá một/nhiều và di chuyển. Id của bot khác bị chặn bằng 403 và không ghi gì. Thiết kế thêm một chỗ lộ dữ liệu cùng endpoint: ô tìm kiếm để trống trả về auto reply của mọi bot. Phần thư mục, sắp xếp và id liên kết của form cũ thuộc ticket #42765. Không đổi FE.

Hướng sửa:
- D-1 Chuyển 2 route init/save detail auto reply vào nhóm ajax cần đăng nhập
- D-2 initDataDetailAutoReply chỉ đọc/sao chép auto reply của bot hiện tại
- D-3 saveDataDetailAutoReply kiểm id, action_id, category_id, keyword id trước khi ghi
- D-4 save (form cũ) tìm auto reply theo id + bot, xoá keyword theo id đã xác nhận
- D-5 deleteItem / deleteItems / moveItem chặn id của bot khác
- D-6 searchByKeyWord nhánh từ khoá rỗng lọc theo bot
- D-7 Kiểm tra: php -l, test guard nếu có DB test cục bộ, log khi chặn

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng màn 自動応答 (danh sách, tạo/sửa/sao chép) ở web: không đổi schema, FE hay contract với job (job chỉ đọc action_id/keyword). Rủi ro chính là xung đột merge với #42431 (routes) và #42765 (cùng ReplyController); cần test hồi quy luồng sửa/sao chép/xoá/di chuyển bình thường.
```

**Journal #142923 — Dev Studio — 2026-10-12:**
```
Dev Studio · Nội dung thực hiện (v2)

Thiết kế v2 bổ sung đúng mục review yêu cầu phải sửa: API auto reply mà công cụ AI (MCP) gọi vẫn đọc, ghi, xoá keyword, bật/tắt và di chuyển auto reply theo id mà không kiểm bot. Phần kiểm quyền đã làm ở web được tách thành một trait dùng chung, rồi áp cùng quy tắc cho API này, giữ nguyên các key response. MCP đã xử lý được lỗi 4xx nên dùng 400/403/404 như web. Vòng này cũng thêm test cho hai nhánh sao chép, và đổi dòng log theo đúng helper. Phần thư mục của API thuộc ticket #42765.

Hướng sửa:
- D-8 Tách helper kiểm quyền auto reply thành trait dùng chung, web dùng trait
- D-9 API MCP/mobile auto reply kiểm id thuộc bot ở init/save/delete/toggle/move
- D-10 Test hai nhánh sao chép (web) và test chặn IDOR cho API mobile
- D-11 Log deleteItem dùng logDebug có placeholder

Ảnh hưởng / rủi ro:
Ảnh hưởng màn 自動応答 trên web (chỉ refactor helper, hành vi giữ nguyên) và công cụ auto reply của MCP: thao tác với id của bot khác giờ trả lỗi 4xx. Không đổi schema và repo MCP. Có thể xung đột merge với #42765 vì cùng hai controller; cần hồi quy cả web lẫn MCP với id của bot mình.
```

**Journal #143983 — Dev Studio — 2026-10-14 (v3, 5 bug QA):**
```
Thiết kế v3 xử lý cả 5 bug QA, đều nằm trong khối kiểm payload lưu chi tiết dùng chung cho web và API mobile. Bốn điểm sửa: id sai định dạng trả 400, action không tồn tại trả 404 và không lưu, payload thiếu thư mục thì giữ thư mục đang lưu (auto reply cũ nằm trong thư mục của bot khác lưu lại được), API mobile lưu thành công trả thêm success:true mà không bỏ khoá cũ. Hai bug sau đều có từ trước khi sửa, nhưng vẫn sửa vì đi ngược điều thiết kế đã cam kết.

Hướng sửa: D-12 action_id/category_id sai định dạng trả 400 thay vì 403 · D-13 action_id không tồn tại trả 404, không lưu · D-14 Payload thiếu category_id thì giữ thư mục đang lưu, tạo mới thì về 0 · D-15 API mobile save-autoreply thành công trả thêm success:true · D-16 Test cho các nhánh 400, 404, thiếu category_id và response success.
```

**Journal #144006 — Dev Studio — 2026-10-14 (v4, bug automation #2755):**
```
Thiết kế v4 sửa bug automation #2755. Màn tạo mới auto reply lấy thư mục (group_id) từ URL mà không kiểm, nên một link mang thư mục của bot khác làm form gửi đi thư mục đó và bị chặn 403. Bản sửa chỉ nhận group_id khi đó là thư mục còn sống của bot đang chọn, nếu không thì về 未分類, áp dụng cả khi nạp dữ liệu màn tạo mới.

Hướng sửa: D-17 Màn tạo mới chỉ nhận group_id là thư mục còn sống của bot đang chọn · D-18 Init chế độ tạo mới chuẩn hoá category_id theo cùng quy tắc · D-19 Test thư mục mặc định khi tạo mới.
```

**Journal #144059 — Dev Studio — 2026-10-14 (v5 — 2 bug automation KHÔNG phải lỗi code):**
```
Thiết kế v5 kết luận hai bug automation không phải lỗi code, vì mọi kiểm tra nghiệp vụ trong log Test Studio đều đạt. Ở bug sao chép, bộ test chỉ không bắt kịp request nạp dữ liệu của ca copy_id=abc, còn màn vẫn quay về danh sách, không lộ dữ liệu và không tạo bản ghi. Ở bug xoá, bộ test đếm luôn cả request mở thư mục ở bước 1. Vòng này chỉ thêm test đơn vị cho nhánh sao chép với id không tồn tại và id sai định dạng; code sản phẩm không đổi.

Hướng sửa: D-20 Thêm test hồi quy sao chép với copy_id không tồn tại hoặc sai định dạng. Hai bug automation nên được đóng là không phải lỗi code, kèm bằng chứng từ chính log của Test Studio.
```

**Journal #146634 — Dev Studio — 2026-10-22 (v6, bug #43617 — bật/tắt):**
```
Thiết kế v6 đã đối chiếu từng thao tác trong bug #43617 với code đã bàn giao. Xem chi tiết, sao chép, sửa, xoá và chuyển auto reply của bot khác đều đã bị chặn. Riêng bật/tắt trên web vẫn trả "thành công" dù DB không đổi, nên lần này sửa cho trả lỗi 403. Phần action thuộc ticket #42759, phần thư mục thuộc #42765. Bản sửa của ticket này chưa có trên nhánh release/staging nào, nên QA có thể đã test trên bản cũ; cần retest trên bản build từ nhánh task.

Hướng sửa: D-21 Bật/tắt auto reply của bot khác trên web trả lỗi thay vì thành công giả · D-22 Test bật/tắt với id bot khác, sai định dạng, không tồn tại và id của bot.
```

**Journal #146801 — Dev Studio — 2026-10-22 (v7, bug automation #3714 — loading UI):**
```
Thiết kế v7 sửa bug automation #3714. Phía server đã đúng: lưu với thư mục của bot khác trả 403, với id không tồn tại trả 404, và không lưu gì. Lỗi nằm ở màn tạo/sửa: lớp loading tắt bằng hiệu ứng mờ dần, nhưng hộp alert hiện ngay sau đó và chặn hiệu ứng, nên loading vẫn còn trên màn. Bản sửa chỉ đổi JS của màn này: tắt hẳn loading trước khi hiện alert, và hiện câu lỗi chung khi response không có message. Không tăng version asset, nên QA cần tải lại cứng trang.

Hướng sửa: D-23 Màn tạo/sửa auto reply tắt hẳn loading trước khi hiện alert lỗi lưu · D-24 Kiểm tra cú pháp JS và ghi rõ mức đã verify.
```

**Journal #146834 — Dev Studio — 2026-10-22 (Dev handoff cuối cùng, v1–v7):**
```
Đóng lỗ IDOR của auto reply ở màn 自動応答 (web) và API MCP/mobile, kèm các sửa bug QA/automation của các vòng sau.

Bug QA con:
- #43033 đã sửa: API mobile save-autoreply khi lưu thành công trả thêm success:true, vẫn giữ status:true, data.id và msg.
- #43034 đã sửa: action_id/category_id sai định dạng giờ trả HTTP 400 「データが見つかりません。」 thay vì 403, cả ở web lẫn API mobile.
- #43035 đã sửa: Lệch duy nhất là bước 2–3 thiếu success:true, nay đã thêm.
- #43036 đã sửa: action_id không có trong t_actions giờ trả HTTP 404 và không lưu; giữ nguyên action đang lưu thì vẫn lưu được.
- #43037 đã sửa: Khi payload thiếu hoặc null category_id: lúc sửa thì giữ thư mục đang lưu, lúc tạo mới thì về 0. Auto reply cũ nằm trong thư mục bot khác giờ lưu được, không còn lỗi PHP.
- #43080 KHÔNG đổi code: không phải lỗi code, cả 15/15 kiểm tra nghiệp vụ đều OK. Request showGroup là bước mở thư mục ở bước 1, còn thao tác xoá chỉ gửi 1 request deleteItem.
- #43081 KHÔNG đổi code: ca bot B và 999999999 trả đúng success:false kèm redirect. Ca abc cũng về danh sách và không lộ dữ liệu; chỉ là bộ test không bắt được request init.
- #43617 đã sửa (commit sns-line@9bd384e63b82, sns-line@0917f7cfcebd, sns-line@2abe1c5ab5f6): Get detail, sửa, sao chép, xoá và chuyển auto reply của bot khác (web + API) đã bị chặn từ v1–v2; v6 thêm bật/tắt trên web báo 403. Bug được tạo 5 phút sau khi gộp staging nên nhiều khả năng test bản chưa có fix; cần retest trên bản build có 2abe1c5ab5. Thư mục thuộc #42765, action thuộc #42759.

Bug automation Test Studio:
- Bug #2793 không phải bug: Request init đã chạy và trả success:false kèm redirect; create.js gọi init trước rồi mới chuyển trang theo redirect. Nên kiểm ca abc theo URL cuối và dữ liệu, hoặc chờ request trước khi trang chuyển.
- Bug #2794 không phải bug: Kiểm tra "chỉ 1 request" đã đếm cả showGroup của bước mở thư mục. deleteItem trong index.js chỉ gửi 1 request và không gọi showGroup.
- Bug #3714 đã sửa (commit sns-line@ced6de1f9cd5): Server vốn đã đúng (403/404, không lưu). create.js giờ tắt hẳn loading trước khi hiện alert ở nhánh lỗi lưu. Tải lại cứng trang trước khi chạy lại NEW-6.

Việc cần người làm thêm (ngoài phạm vi task):
- Cho Test Studio: test case NEW-4 (#2793) nên kiểm ca copy_id=abc bằng kết quả (URL cuối, dữ liệu không lộ, số đếm), hoặc chờ request init trước khi trang chuyển; test case AR-021 (#2794) chỉ nên đếm request phát sinh sau khi bấm 「削除」.
- Cho người làm #42765: API mobile còn IDOR thư mục ở updateAutoreplyFolder (đổi tên folder theo id không ràng bot), ở buildListCategoryResponse (đọc folder theo group_id không ràng bot) và folder_move_id của moveAutoreply; nên dùng lại trait AutoReplyOwnershipGuardTrait.
- Auto reply id 24, 25 (bot 2) trỏ folder của bot 35 trên DB điều tra — dữ liệu lệch cũ, cần rà trên production nếu muốn dọn.
- Phát hành #42765 (thư mục auto reply) và #42759 (action) cùng #42764 thì mới đóng đủ các thao tác nêu trong #43617.

Lưu ý khi deploy:
- Gộp lại nhánh task vào staging/release để lấy commit 2abe1c5ab5 và ced6de1f9c (staging release_staging_20261014_v3 hiện mới có tới 5640e9f98b); đã thử gộp và không có xung đột.
- Không tăng sns-line.version: người dùng và tester cần tải lại cứng để nhận create.js mới.

Branch: ai_studio_implement_42764 (nhánh gốc release_step_20260930_v2 @46765b418f67, commit cuối ced6de1f9cd5b0dd751fd01e6eb9e9dfab5387cb)
```
