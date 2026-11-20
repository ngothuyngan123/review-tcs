# 03 — Đối chiếu câu hỏi khách (category API public, 10–11/2026) với docs Public API 1.3.0

> Report cho Leader đọc. Không gửi đi đâu, không ghi Redmine.
> `L<n>` = số dòng trong `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html` (đọc qua bản text của `scripts/api_docs_extract.py`).
> "Câu trả lời gửi khách" = comment của エルメサポート / WSSサポーター đã gửi khách trên Slack. Ghi chú nội bộ của dev chỉ dùng để đối chiếu, ghi rõ khi trích.
> Cột `Quyết định Leader` để trống cho Leader ghi.

## 0. Nguồn

| Trường | Giá trị |
|---|---|
| Ticket cha | #41821 `CHECK REPORT FROM CUSTOMER 10/2026` (144 ticket con cả 2 tháng) · #44892 `… 11/2026` |
| Lọc | Category = `API public` → **14 ticket** (10 ticket tháng 10, 4 ticket tháng 11). Đã đọc đủ mô tả + toàn bộ comment |
| Docs đối chiếu | Public API v1 bản **1.3.0** (16/11/2026) |
| Spec phụ | `spec-features/admin/api-integration/web/logic-spec.md` (key: số lượng, hạn dùng, tên) |
| Không xét | Câu hỏi về Webhook (docs Webhook riêng: `spec-features/webhook/`), giá gói, quyền nhân viên, app mobile, chuyển đổi từ tool khác — ngoài phạm vi docs API |

### Danh sách 14 ticket

| Ticket | Mã | Tháng | Chủ đề | Trạng thái |
|---|---|---|---|---|
| #42161 | TY-12333 | 10 | Dùng API/Webhook, gắn lại tag, ảnh hưởng tính năng, `mark_confirmed` | Closed |
| #42337 | TY-12350 | 10 | Lọc đối tượng khi gửi tin qua API | Closed |
| #42669 | TY-12367 | 10 | Chuyển từ L Step: gói, LINE user ID, custom API | Closed |
| #42670 | TY-12357 | 10 | Phát URL quà qua GAS/Webhook/API | Closed |
| #42671 | TY-12384 | 10 | Cập nhật trạng thái xử lý có điều kiện, rollback, thứ tự action | Closed |
| #42842 | TY-12401 | 10 | Không phát hành được API key (bug KH) | Closed |
| #43645 | TY-12465 | 10 | 10 điểm: gói, gửi hàng loạt, do_action, rate limit, idempotency, kết quả gửi, lịch sử | Closed |
| #43646 | TY-12476 | 10 | Chuyển hệ thống: step giữa chừng, idempotency, cập nhật thuộc tính, block_status | Closed |
| #44351 | 32587 | 10 | Xem tag ID ở đâu | Closed |
| #44397 | TY-12514 | 10 | 401 khi gọi API tag (khách gọi nhầm API khác) | Closed |
| #45054 | TY-12611 | 11 | E1–E9: lấy lịch sử > 100 tin, đếm 100 tin, phân biệt tin, đọc an toàn, file đính kèm | **KH Feedback** (khách hỏi lại 11/11, chưa trả lời) |
| #45318 | TY-12650 | 11 | Đổi key sắp hết hạn sang key không thời hạn | Closed |
| #46091 | — | 11 | Vượt rate limit 60/phút khi gửi 70 người | Closed |
| #46186 | TY-12756 | 11 | Tag gắn qua do_action không lên số người ở タグ管理 | **New** (đang điều tra) |

---

## 1. Tóm tắt

| Câu hỏi | Trả lời ngắn |
|---|---|
| 1. Docs có khớp nội dung đã trả lời khách không? | **Phần lớn khớp, nhưng có 4 chỗ câu trả lời gửi khách trái docs** (idempotency trả 409, `type: point`, `display_status=all`, "không phân biệt được gửi hàng loạt / step") và **5 chỗ lệch nhẹ hoặc docs thiếu điều đã trả lời** (§2). |
| 2. Docs đã trả lời được hết câu hỏi của khách chưa? | **Chưa.** Trong 22 nhóm câu hỏi về API: 4 nhóm docs trả lời đủ, 13 nhóm chỉ trả lời một phần, 5 nhóm docs không nói gì (§3). Câu bị hỏi nhiều nhất mà docs không có: **API dùng được ở gói nào, có tốn phí không** (4 ticket). |
| 3. Docs đã nêu rõ toàn bộ param chưa? | **Chưa.** 12 param / trạng thái chưa định nghĩa rõ, trong đó 6 điểm khách đã phải hỏi (§4). |

---

## 2. Câu 1 — Docs có khớp với câu trả lời đã gửi khách không

### 2.1 Chỗ không khớp

| # | Chỗ A — câu trả lời gửi khách | Chỗ B — docs 1.3.0 | Mâu thuẫn là gì | (A) | (B) | Mức | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| QA-1 | **#43646** (28/10, 02/11): "Nếu request đầu tiên đã được xử lý bình thường, khi gửi lại sẽ trả về HTTP 409" · "không thể phân biệt đã hoàn tất / đang xử lý / thất bại một phần từ 409" | **L441** · gửi lại đúng request sau khi lần đầu thành công: "Trả lại nguyên response đã lưu + header Idempotency-Replayed: true"<br>**L443** · đang xử lý → 409 `in_progress`; **L442** · khác nội dung → 409 `conflict` | Theo docs, lần đầu xong thì gửi lại nhận **200 (bản lưu)**, và 409 có `error.code` phân biệt "đang xử lý" với "khác nội dung". Khách được báo ngược lại nên sẽ viết sai nhánh xử lý retry | Câu trả lời sai → đính chính với khách #43646 (ghi chú dev 26/10 cũng ghi "chạy xong → trả request_id giống lần đầu", đúng với docs) | Server thật trả 409 → sửa docs L441 | `[MAJOR]` | |
| QA-2 | **#43646** (28/10) · mục 4: "Khi clear điểm, hãy chỉ định point cho type và dùng point_clear" | **L1608** · `type` = `friend_info`, action có `point_clear` (**L1866**); không có `type` là `point` | Khách làm theo sẽ gửi `"type": "point"` → bị 422 "unknown type" | Câu trả lời sai → đính chính: `{"type":"friend_info","action":"point_clear","field_id":…}` | Docs thêm ví dụ `point_clear` ở mục friend_info cho rõ | `[MAJOR]` | |
| QA-3 | **#45054** (09/11) · E5④: "Khi muốn lấy cả đã xác nhận và chưa xác nhận, có thể chỉ định display_status=all" | **L1180** · `display_status` = hiển thị / ẩn<br>**L1173** · `confirm_status` = đã đọc / chưa đọc, bỏ trống = cả hai | Câu trả lời lẫn 2 tham số. `display_status=all` là lấy cả hội thoại **đã ẩn**, không liên quan đã đọc / chưa đọc. Khách đã hỏi lại 11/11 (E5), chưa được trả lời | Câu trả lời sai → đính chính trong lần trả lời tới (ghi chú dev 17/11 E5-1 đã đúng) | — (docs đúng) | `[MAJOR]` | |
| QA-4 | **#45054** (09/11) · E3②: "Không thể phân biệt từ response API các loại gửi như trả lời tự động, tin chào, **gửi hàng loạt, gửi theo bước**, gửi hẹn giờ, template gửi thủ công" | **L1461** · `message_type = broadcast` = 一斉配信<br>**L1462** · `scenario` = 1 step của scenario<br>**L1996** · `template` / `broadcast` / `event` / `action` là các loại riêng | Docs cho thấy gửi hàng loạt và gửi theo bước **có** `message_type` riêng; câu trả lời nói không phân biệt được. Khách đang dựa vào điểm này để quyết định có dùng hay không | Câu trả lời quá rộng → đính chính: phân biệt được broadcast / step / nhắc lịch / action; **không** phân biệt được auto reply, tin chào, template gửi tay (cùng là `template`) và tin nhân viên gõ với text gửi qua API (cùng `text` + `LINE_OA`) | Server không trả đúng các loại này → sửa §7.4 docs | `[MAJOR]` | |
| QA-5 | **#45054** (09/11) · E5②: "last_message_date được cập nhật khi nhân viên gửi riêng; với tin gửi tự động như gửi hàng loạt hay theo bước thì **không** được cập nhật" | **L1190** · `last_message_date` = "Thời điểm tin nhắn cuối" (không có ngoại lệ) | Docs không nói tin tự động bị loại. Khách đọc docs sẽ hiểu mọi tin (kể cả broadcast) đều cập nhật, dùng field này để phát hiện thay đổi sẽ sót | Câu trả lời đúng hành vi → docs bổ sung ngoại lệ | Câu trả lời sai → đính chính | `[MAJOR]` | |
| QA-6 | **#42161** (09/10) · mục 4: "Khi thao tác tag **hoặc thông tin friend** qua API, nếu có thiết lập sub-action thì sub-action cũng được thực thi" | **L1591–L1596** · Tác dụng phụ: chỉ nêu `tag.add` và `scenario.start/resume`, không nhắc `friend_info` | Khách được báo ghi friend info qua API cũng chạy action; docs không có → khách khác đọc docs sẽ không biết, có thể bị gửi tin ngoài ý muốn | Câu trả lời đúng → docs bổ sung (trùng `DOC-CLEAR` friend info trong report 02) | Câu trả lời sai → đính chính | `[MAJOR]` | |
| QA-7 | **#43645** (28/10) · mục 4: rate limit "áp dụng theo **từng tài khoản L Message**" | **L383** · "Tính **theo bot**: nhiều API key của cùng 1 bot dùng chung hạn mức" | 1 tài khoản L Message có thể có nhiều bot (khách hỏi ở mục 10 cùng ticket). Câu trả lời khiến khách hiểu các bot dùng chung hạn mức. Ghi chú dev 27/10 ghi "Tính theo bot (OA)" — đúng docs | Câu trả lời dùng từ chưa chuẩn → lần sau ghi "theo từng bot (LINE公式アカウント)" | Server tính theo tài khoản → sửa docs L383 | `[MINOR]` | |
| QA-8 | **#43645**, **#43646**: Idempotency-Key "hiệu lực **24 giờ**" / "giữ 24 giờ kể từ request đầu tiên" | **L431** · "lưu **ít nhất** 24 giờ… thời điểm dọn không cố định… có thể nhận replay hoặc được thực thi như request mới" | Câu trả lời nói đúng 24 giờ, docs nói tối thiểu 24 giờ rồi không chắc. Khách dùng lại key sau đúng 24 giờ sẽ gặp kết quả không đoán trước | Docs đúng → lần sau trả lời "ít nhất 24 giờ, không dùng lại key" | Server dọn đúng 24 giờ → docs ghi chắc | `[MINOR]` | |
| QA-9 | **#45054** (09/11) · E2④: "Khi một thao tác gửi gồm nhiều tin nhắn, **mỗi tin** được đếm là 1 tin" (trong giới hạn 100) | **L1457** · `template` là **1 dòng**, `data` là mảng các phần tử (template nhiều bong bóng nằm trong 1 dòng) | Theo docs, template nhiều bong bóng chỉ chiếm 1 trong 100 dòng; câu trả lời nói mỗi bong bóng tính 1. Ghi chú dev 04/11 cũng ghi "template nhiều bong bóng tính 1, dòng sự kiện hệ thống cũng bị tính" | Câu trả lời sai → đính chính | Docs sai → sửa mục ví dụ `data` | `[MINOR]` | |
| QA-10 | **#44397** (26/10): dẫn link `lme.jp/apireference/#sec2-1`, `#sec2-2`, `#sec2-4` (page/limit), `#sec2-7` (request_id), `#sec2-8` (401), `#sec4-1` (tags) | Docs 1.3.0 · không có anchor `#secX-Y` (anchor dạng `#base-url`, `#pagination`…); số mục cũng đổi: 2.4 là Định dạng response, 2.7 là Rate limit, 2.8 là Phân trang | Khi bản 1.3.0 thay bản đang public, link trong câu trả lời cũ sẽ trỏ sai mục hoặc không tới mục nào | Docs giữ thêm anchor cũ `#secX-Y` để link cũ vẫn chạy | Chấp nhận; câu trả lời sau dẫn theo anchor mới | `[MINOR]` | |

### 2.2 Chỗ khớp (đã đối chiếu)

| Nội dung đã trả lời khách | Ticket | Docs |
|---|---|---|
| Tin gửi qua API được tính vào số tin như gửi từ màn hình quản lý | #42161, #43645 | L956 |
| `messages/push` / `messages/template` chỉ gửi cho 1 friend, không có API gửi hàng loạt | #43645, #46091 | L942 |
| do_action 100 friend / 10 action là giới hạn cứng; 1 action sai → cả request bị từ chối; lỗi riêng lẻ không làm request thất bại, không rollback | #43645, #42671 | L1585, L1589, L1602 |
| Rate limit cửa sổ cố định theo phút, 429 kèm `Retry-After`; request lỗi xác thực không bị trừ | #43645, #46091 | L383–L386 |
| Request bị 429 không được thực thi, LME không tự gửi lại; chống trùng chỉ khi có `Idempotency-Key` | #46091 | L386, L433 |
| Idempotency: phạm vi theo key, ≤ 100 ký tự, chỉ lưu response 2xx, request lỗi gửi lại được | #43645, #43646 | L430, L440, L444 |
| `success: true` = đã nhận vào hàng đợi, không phải đã tới người nhận | #43645, #45054 | L949 |
| `/conversations/detail` tối đa 100 tin mới nhất, không phân trang; 180 / 365 ngày theo gói LME; tin gửi lỗi không trả về | #43645, #45054 | L1292–L1295 |
| `block_status`: `block` = LME chặn, `blocked` = friend chặn OA, `normal` | #43646 | L1312 |
| `mark_confirmed=false` không đổi trạng thái đã đọc | #42161 | L945 |
| Gắn lại tag đã có thì không chạy lại | #42161 | L1842 |
| API gửi không có lọc đối tượng; lọc bằng `/conversations`, liên kết khách theo tên / email | #42337 | L498–L504, L1170+ |
| Base URL, `/v1`, header `X-LME-API-KEY`, định dạng key, `page` / `limit` (mặc định 100, tối đa 500) | #44397 | L226, L242, L240, L397 |
| Lấy tag ID bằng `GET /tags` | #44351 | L746+ |
| Xoay key: key cũ dùng tới khi hết hạn | #45318 | L263 |
| Các action chạy tuần tự → gắn rồi gỡ cùng tag trong 1 request thì tag mất | #46186 | L1584 |

---

## 3. Câu 2 — Docs đã trả lời được hết câu hỏi của khách chưa

> Đủ = khách đọc docs là tự trả lời được · Một phần = docs có nhưng thiếu ý khách hỏi · Không = docs không nói.

| # | Câu hỏi của khách | Ticket | Docs | Docs có / thiếu gì | Đề xuất bổ sung |
|---|---|---|---|---|---|
| CQ-1 | API dùng được ở gói nào, có tốn phí, có cần đăng ký không | #42161, #42669, #43645, #45054 | **Không** | Docs không nhắc gói / phí | Thêm 1 dòng ở §1: mọi gói dùng được, không phí, không cần đăng ký |
| CQ-2 | Rate limit có dùng chung với màn hình quản trị không, có khác theo gói không; request 422 / replay có bị trừ không | #43645 | Một phần | L383 có "theo bot"; không nói màn hình quản trị không dùng chung, không khác theo gói, 422 và replay vẫn bị trừ | Ghi rõ 3 ý này ở §2.7 |
| CQ-3 | Có API / Webhook lấy kết quả gửi thực tế, tra theo `request_id` không | #43645, #45054 | Một phần | L949 nói 200 = vào hàng đợi; không nói "không có API tra kết quả, `request_id` chỉ để liên hệ hỗ trợ" | Ghi rõ ở §4 messages/push |
| CQ-4 | Gửi cùng nội dung cho nhiều người thế nào | #43645, #46091 | Một phần | Docs chỉ cho thấy push 1 friend; không nói không có gửi hàng loạt, không gợi ý cách | Thêm mục "Gửi cho nhiều friend": lặp push, hoặc tạo step rồi `scenario.start` qua do_action |
| CQ-5 | Dùng LINE user ID để gắn tag / cập nhật friend info | #42669 | Một phần | Push nhận `line_friend_id` (L943), nhưng do_action chỉ nhận `lmessage_friend_ids` (L1602) và `/friends` không lọc theo LINE user ID (L498–L504) → không có cách đổi LINE user ID sang `lmessage_friend_id` trừ duyệt toàn bộ danh sách | Nói rõ hạn chế, hoặc thêm filter `line_friend_ids` cho `/friends` |
| CQ-6 | Lấy tin cũ hơn 100, phân trang detail, gửi lại sự kiện | #45054 | **Đủ** | L1292 "Không lấy được message cũ hơn qua API này" | — |
| CQ-7 | 100 tin đếm thế nào (gửi + nhận, template nhiều bong bóng, dòng log, tin trước khi bật API) | #45054 | Một phần | Ví dụ cho thấy template 1 dòng, log là 1 dòng; không có câu nói rõ cách đếm, không nói tin trước khi bật API | Thêm cách đếm vào bảng Giới hạn (L1291+) |
| CQ-8 | Phân biệt tin nhân viên gửi tay với tin tự động; có ID tin nhắn không | #45054 | Một phần | `message_type` phân biệt broadcast / step / event / action (L1996); không nói tin nhân viên gõ và text API cùng là `text` + `LINE_OA`, không nói **không có** ID tin nhắn / cách khử trùng | Thêm 1 đoạn "Không có ID tin nhắn" + bảng loại gửi nào ra `message_type` nào |
| CQ-9 | Gọi GET có làm đổi trạng thái đã đọc / trạng thái xử lý không | #45054 | **Không** | Docs không nói | Ghi ở §1: GET chỉ đọc, không đổi trạng thái |
| CQ-10 | `last_message_date` đổi khi nào; lấy phần thay đổi thế nào; thứ tự khi phân trang | #45054 | Một phần | L419 có cảnh báo lệch trang; không có ngoại lệ tin tự động (QA-5) | Bổ sung điều kiện cập nhật `last_message_date` |
| CQ-11 | Hội thoại đã ẩn / friend đã chặn có lấy được không | #45054 | Một phần | `/friends` gồm cả friend chặn (L491), `display_status=all` (L1180); không nói `/conversations/detail` vẫn lấy được hội thoại đã ẩn | Ghi 1 câu ở `/conversations/detail` |
| CQ-12 | URL file đính kèm hết hạn khi nào, có cần xác thực không | #45054 | **Không** | L1437 chỉ nói "luôn dùng nguyên URL được trả về" | Ghi thời hạn / điều kiện truy cập URL media |
| CQ-13 | Idempotency: thời hạn, request đồng thời, khác nội dung, retry sau timeout / 429 / 5xx, request lỗi có bị coi là đã dùng | #43645, #43646 | **Đủ** | L429–L455 | — |
| CQ-14 | Gửi lại cùng key, phân biệt "đã xong / đang chạy / thất bại một phần" | #43646 | Một phần | Phân biệt được replay (L441) và `in_progress` (L443); "thất bại một phần" của do_action không biết được (response không liệt kê — L1588) nhưng docs không nói thẳng | Ghi rõ: do_action không báo kết quả từng friend / action |
| CQ-15 | Action giữa chừng lỗi có rollback không; có cập nhật có điều kiện (CAS) không; có bị thao tác tay xen vào không | #42671 | Một phần | L1589 chỉ nói không rollback **friend khác**; không nói rollback giữa các action của cùng friend, không có CAS, không khoá loại trừ | Bổ sung 3 ý ở "Cách hoạt động" của do_action |
| CQ-16 | Cập nhật friend info: bỏ field / chuỗi rỗng / `null` / xoá; chọn nhiều; thay toàn bộ tag | #43646 | Một phần | Có `clear`, "set requires value" (L1855); không nói `null`, không nói 選択肢 chọn 1 hay nhiều, không có thao tác "thay toàn bộ tag" | Thêm bảng hành vi `value` rỗng / `null` / thiếu; ghi rõ không có thay toàn bộ |
| CQ-17 | Cập nhật thuộc tính / tag mà **không** kích hoạt action | #43646 | **Không** | Docs không nói có hay không cách tắt (ghi chú dev: không có) | Ghi rõ "không có tuỳ chọn tắt action" ở Tác dụng phụ |
| CQ-18 | Bắt đầu scenario từ 1 tin cụ thể trong ngày, giữ thời điểm gửi cũ | #43646 | Một phần | `resume` + `start_from` theo **ngày** (L1898); không nói không chọn được tin trong ngày | Ghi giới hạn này ở mục scenario |
| CQ-19 | Nhiều key cùng lúc, tối đa bao nhiêu, hết hạn lúc mấy giờ, gia hạn được không | #45318 | Một phần | Có xoay key (L263); thiếu: tối đa 10 key / bot, hết hạn 00:00 JST ngày hôm sau, không gia hạn được | Bổ sung vào §2.2 (xem §4 P8) |
| CQ-20 | Lỗi khi phát hành key, cần kiểm tra gì | #42842 | **Không** | Docs không có giới hạn tên key, số key, các lỗi khi phát hành | Thêm bảng lỗi phát hành key ở §2.2 |
| CQ-21 | Request bị 429 có hiện ở 「送信エラー」 trên màn hình không | #46091 | **Không** | L386 chỉ nói không thực thi | Ghi: không hiện ở màn hình, client tự ghi lại |
| CQ-22 | Tag ID xem ở đâu | #44351 | **Đủ** | `GET /tags` | — |

Tổng: **Đủ 3** (CQ-6, 13, 22) · **Một phần 13** · **Không 6** (CQ-1, 9, 12, 17, 20, 21).

> Ngoài phạm vi docs API (không tính): Webhook — chữ ký, gửi lại, định dạng chuyển tiếp (#42161, #42669, #43645, #45054 E4, #42670) · giá gói, số nhân viên, quyền nhân viên, app mobile, chuyển đổi (#42669, #45054 E6–E9).

---

## 4. Câu 3 — Param / trạng thái chưa được định nghĩa rõ

| # | Param / trạng thái | Docs hiện ghi | Chưa rõ ở đâu | Phát hiện từ | Đề xuất ghi vào docs |
|---|---|---|---|---|---|
| P1 | `block_status` | **L1312**, **L2009** · 3 giá trị `normal` / `blocked` / `block` | Không nói khi **cả hai bên cùng chặn** thì trả gì | #43646 (khách hỏi; trả lời: `block`) | Thêm: cả hai cùng chặn → `block` |
| P2 | `last_message_date`, `last_message` | **L1189–L1190** · "Thời điểm / nội dung tin nhắn cuối" | Tin nào làm cập nhật (theo câu trả lời: tin gửi tự động không cập nhật) | #45054 | Liệt kê loại tin có / không cập nhật |
| P3 | Giới hạn 100 tin của `/conversations/detail` | **L1292** · "Tối đa 100 message gần nhất" | Đơn vị đếm: dòng hay bong bóng; dòng log hệ thống có chiếm chỗ không; tin trước khi bật API | #45054 | Thêm cách đếm (QA-9 phải chốt trước) |
| P4 | `friend_info.value` | **L1855** · bắt buộc với `set`, được trim | `value: null`, `value: ""`, không gửi `value` lần lượt trả gì (400 theo §2.3 hay 422 "requires value") | #43646 (ghi chú dev: `null` → 422) | Bảng 3 trường hợp × mã lỗi |
| P5 | Field 選択肢 (`SELECT`) | **L1856** · `option_id` (1 giá trị) | Không nói field có cho chọn nhiều không, không có cách gán nhiều option | #43646 | Ghi rõ 1 option / lần `set` |
| P6 | Thời gian lưu Idempotency-Key | **L431** · "ít nhất 24 giờ", dọn không cố định | Sau 24 giờ không xác định được kết quả; câu trả lời gửi khách lại nói đúng 24 giờ (QA-8) | #43645, #43646 | Chốt 1 cách nói cho docs và câu trả lời |
| P7 | Rate limit — loại request bị trừ | **L385** · 401 / 403 / 400-Content-Type không bị trừ | Không nói 404 / 422 / replay idempotency có bị trừ (ghi chú dev: 422 và replay bị trừ) | #43645 | Liệt kê đủ |
| P8 | API key: hạn dùng, số lượng, tên | **L240** · "hạn dùng (để trống = vĩnh viễn)" | Màn hình có 4 lựa chọn 1日 / 1週間 / 30日 / 無期限, mặc định 30日 (không có "để trống"); hết hạn 23:59:59 JST ngày hiển thị; tối đa **10 key / bot**; tên ≤ 50 ký tự, không trùng; không gia hạn được | #45318, #42842 · spec `logic-spec.md` L189, L245, L287 | Bảng thuộc tính key ở §2.2 |
| P9 | URL media trong `data` | **L1437** · "luôn dùng nguyên URL được trả về" | Thời hạn hiệu lực, có cần xác thực không | #45054 | Ghi thời hạn / điều kiện truy cập |
| P10 | `scenario.resume` · `start_from` | **L1898** · ngày bắt đầu, ≥ 0 | Không có max (vượt số ngày scenario thì sao); không chọn được tin trong ngày | #43646 · report 02 `DOC-CLEAR` | Thêm max + giới hạn "theo ngày" |
| P11 | Kết quả từng friend / action của `/do_action` | **L1588–L1589** | Response chỉ có `success` + `request_id`; không có trường nào cho biết friend bị bỏ qua / action lỗi riêng lẻ — docs có nói "không liệt kê" nhưng không nói cách kiểm tra lại | #43645, #43646 | Thêm cách kiểm tra khuyến nghị (gọi `/friends/detail`) |
| P12 | Request bị 429 | **L386** · không được thực thi | Không xuất hiện ở 「送信エラー」 trên màn hình (theo câu trả lời #46091) | #46091 | Ghi 1 câu ở §2.7 |

> Ngoài 12 điểm trên, report 02 (`02-api-docs-review.md`) đã liệt kê thêm các param thiếu thông tin khác chưa có khách hỏi: độ dài TEXT / khoảng POINT không giới hạn, `edited_content` > 5.000, `duration` max, số giá trị CSV, ngày không tồn tại, token `[FRIEND_INFO_<id>]` của bot khác.

---

## 5. Việc nên làm

### Đính chính với khách (ưu tiên)

- [ ] **#43646**: QA-1 (gửi lại cùng key sau khi xong → 200 replay, không phải 409) · QA-2 (`type: "friend_info"` + `action: "point_clear"`).
- [ ] **#45054** (khách đang chờ trả lời lần 2): QA-3 (`display_status` ≠ đã đọc / chưa đọc) · QA-4 (broadcast / step **có** `message_type` riêng) · QA-9 (cách đếm 100 tin) — sửa luôn trong câu trả lời tới.
- [ ] **#43645**: QA-7 (rate limit tính theo bot, không theo tài khoản) — nếu Leader thấy cần.

### Bổ sung docs (gửi WSSJ cùng câu hỏi ở report 02)

- [ ] Gói / phí API (CQ-1) — bị hỏi 4 lần.
- [ ] Tác dụng phụ của `friend_info` + không có cách tắt action (QA-6, CQ-17).
- [ ] Điều kiện cập nhật `last_message_date` (QA-5, P2) và cách đếm 100 tin (P3).
- [ ] Thuộc tính API key: hạn dùng, giờ hết hạn, tối đa 10 key, tên, không gia hạn, lỗi phát hành (P8, CQ-19, CQ-20).
- [ ] `block_status` khi cả hai cùng chặn (P1); `value` null / rỗng (P4); `start_from` (P10); request bị trừ rate limit (P7).
- [ ] Giữ anchor cũ `#secX-Y` khi public bản 1.3.0 (QA-10).

### Theo dõi

- #46186 (New): khách nói tag hiện ở chi tiết friend nhưng タグ管理 = 0; điều tra hiện kết luận do gắn + gỡ cùng tag trong 1 request. Hai ý này chưa khớp nhau (nếu tag đã bị gỡ thì chi tiết friend cũng không còn tag) — cần xác nhận lại trước khi trả lời khách.
