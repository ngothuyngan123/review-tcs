# 04 — Rà ví dụ response · docs Public API v1 bản `1.3.0` (`16/11/2026`)

> Report cho Leader đọc. Yêu cầu Leader (2026-11-19): **docs phải có đủ ví dụ cho mọi response**.
> `L<n>` = số dòng trong [api-detail-spec_vi_v1.3.0.html](../../spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html).
> Mã `RX-*` chỉ dùng trong file này, không trùng mã `DOC-*` của [02-api-docs-review.md](02-api-docs-review.md).
> Cột `Quyết định Leader` để trống cho Leader ghi.

## 0. Nguồn & tiêu chí

| Hạng mục | Nội dung |
|---|---|
| Docs | Bản `1.3.0`, đọc qua bản text của `scripts/api_docs_extract.py` |
| Cách đếm | Rà tay toàn bộ docs + script đếm field output đã xuất hiện trong ví dụ (null / rỗng / từng giá trị enum) |
| Report liên quan | 02: `DOC-EX-1..4` · `DOC-INT-4` · `DOC-VER-4` — không lặp lại ở đây · 03: `QA-1` · `P11` · `CQ-21` |
| Ngoài phạm vi | Ví dụ request (mục 5 / 6) · code mẫu Python / Node.js / Ruby (chỉ là code gửi request) |

**Tiêu chí "đủ ví dụ response"** (dùng cho cả report):

| Mã | Tiêu chí |
|---|---|
| R1 | Mỗi endpoint có ≥ 1 ví dụ 200 đầy đủ |
| R2 | Mỗi biến thể 200 mà docs mô tả (mảng rỗng, field `null`, giá trị enum, replay, kẹp `limit`…) có ví dụ JSON |
| R3 | Mỗi cặp `HTTP` · `error.code` có thể xảy ra ở endpoint có ≥ 1 ví dụ body đầy đủ |
| R4 | Message lỗi trong bảng ghi đủ, không còn `…` hay "(nội dung do hệ thống trả về)" |
| R5 | Có ví dụ raw HTTP kèm header: header chung · 429 có `Retry-After` · replay có `Idempotency-Replayed` |
| R6 | Mỗi field kiểu `… \| null` xuất hiện `null` ở ít nhất 1 ví dụ, kèm câu "khi nào null" |

## 1. Tóm tắt

| Hạng mục | Docs định nghĩa | Có ví dụ | Thiếu |
|---|---|---|---|
| R1 · Endpoint có ví dụ 200 | 12 | 12 | 0 |
| R3 · Dòng lỗi trong mọi bảng lỗi (lỗi chung 16 · lỗi riêng endpoint 60 · mục 5 là 22 · mục 6 là 21) | 119 | 3 (cả 3 là 404: L608 · L739 · L1275) | 116 |
| R3 · Cặp `HTTP` · `error.code` theo endpoint | 31 | 3 | 28 |
| R3 · Lỗi chung 401 · 403 `forbidden` · 429 · 500 | 4 | 0 (chỉ có khung lỗi chung L307) | 4 |
| R3 · 3 endpoint POST (`/messages/push` · `/messages/template` · `/do_action`, gồm mục 5 và 6) | 83 dòng lỗi | 0 | 83 |
| R5 · Header response | 6 header | 0 | 6 |
| R2 / R6 · Biến thể 200 | — | — | 15 biến thể (§5) + replay (RX-7) chưa có ví dụ JSON; 3 trong số đó chỉ tả bằng lời (RX-33 · RX-35 · RX-36) |
| R4 · Message lỗi chưa đủ | — | — | 5 chỗ |

**Kết luận: docs CHƯA đạt yêu cầu.**
- Ví dụ 200 đủ cho cả 12 endpoint, phần lớn biến thể đã có.
- Ví dụ lỗi gần như không có: 3 / 119 dòng, cả 3 đều là 404 ở endpoint GET.
- 3 endpoint POST không có ví dụ lỗi nào. Đây là nơi xử lý lỗi sai gây gửi trùng tin hoặc mất tin.
- Không có ví dụ nào cho thấy header response. Cả 3 khối `HTTP/1.1 404` (L608 · L739 · L1275) chỉ có dòng trạng thái.
- 2 chỗ thiếu ví dụ đã gây trả lời sai hoặc làm khách phải hỏi: replay (#43646, report 03 `QA-1`) và 429 (#46091).

## 2. Ma trận theo endpoint

| Endpoint | Ví dụ 200 | Biến thể 200 đã có | Biến thể 200 còn thiếu | Dòng lỗi riêng | Ví dụ lỗi | Cặp `HTTP` · `code` chưa có ví dụ |
|---|---|---|---|---|---|---|
| `GET /friends` | L536 | Lọc email L558 · field null L579 · không có kết quả L590 · kẹp `limit` L597 | `line_friend_id` null · `added_time` null (RX-28) | 6 | 1 (404 L608) | 400 `invalid_request` · 422 `validation_error` |
| `GET /friends/detail` | L656 | Đủ kiểu field L684 · friend chưa có dữ liệu L721 | `line_name` null · `line_friend_id` null · `type` null · `value` null / thập phân / chuỗi gốc (RX-29, RX-30, RX-31) | 3 | 1 (404 L739) | 400 `invalid_request` |
| `GET /tags` | L770 | Trang 2 L785 · không có tag L796 | Kẹp `limit` (RX-27) | 0 (chỉ page/limit) | 0 | 400 `invalid_request` |
| `GET /friend-info-fields` | L829 | SELECT chưa có option (`options: null`) L855 | Kẹp `limit` (RX-27) | 0 | 0 | 400 `invalid_request` |
| `GET /scenarios` | L900 | Nhiều scenario, số đếm 0 L911 | Kẹp `limit` (RX-27) | 0 | 0 | 400 `invalid_request` |
| `POST /messages/push` | L1026 | — | Replay (RX-7) | 16 | 0 | 400 · 404 · 422 · 403 `quota_exceeded` · 409 `conflict` · 409 `in_progress` |
| `POST /messages/template` | L1108 | — | Replay (RX-7) | 13 | 0 | 400 · 404 · 422 · 403 `quota_exceeded` · 409 `conflict` · 409 `in_progress` |
| `GET /templates` | L1139 | Trang vượt tổng số trang L1152 | Kẹp `limit` (RX-27) | 0 | 0 | 400 `invalid_request` |
| `GET /conversations` | L1211 | Không filter, favorite, chưa gắn trạng thái L1232 | Ví dụ 3 chỉ có request (RX-33) · `line_friend_id` null · `last_message_date` null (RX-32) | 8 | 1 (404 L1275) | 400 `invalid_request` · 422 `validation_error` |
| `GET /conversations/detail` | L1326 | Friend chặn + ẩn + dòng log `null` L1418 | `block_status: "block"` · `favorite: "yes"` · `messages: []` · `data` dạng string · `unknown` có dữ liệu… (RX-34 → RX-39) | 3 | 0 | 400 `invalid_request` · 404 `not_found` |
| `GET /handling-statuses` | L1561 | Bot chưa có trạng thái L1572 | — | 0 | 0 | — |
| `POST /do_action` | L1704 | — | Replay (RX-7) · có friend bị bỏ qua (RX-40) · gắn rồi gỡ cùng tag (RX-41) | 11 (+ 21 dòng lỗi ở mục 6) | 0 | 400 · 404 · 422 · 409 `conflict` · 409 `in_progress` |

## 3. Ví dụ lỗi còn thiếu

### 3.1 Lỗi chung — áp cho mọi endpoint

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-1 | **L368–L369** · Lỗi chung: 400 "Content-Type must be application/json" · "Request body is invalid…" | Không | Body 400 khi POST thiếu `Content-Type` và khi JSON lỗi | Không biết lỗi trả về dạng nào khi body hỏng | `[MINOR]` | |
| RX-2 | **L361–L364** · Lỗi chung: 401 (4 message) | Không | Body 401 "API key expired" + header `X-RateLimit-Remaining` = `X-RateLimit-Limit` (L334) | Không phân biệt "phát hành lại key" với "sửa cấu hình" | `[MINOR]` | |
| RX-3 | **L365–L367** · Lỗi chung: 403 `forbidden` (3 message) | Không | Body 403 "API key is read-only" khi key `read` gọi POST | — | `[MINOR]` | |
| RX-4 | **L233–L234** · 2.1: 404 "Unsupported API version…" · "Endpoint not found…" | Không | Body 404 khi gọi sai path / sai method | Lẫn với 404 do ID sai, rồi làm mới cache vô ích (L216 khuyên làm mới cache khi gặp 404) | `[MINOR]` | |
| RX-5 | **L353**, **L371** · 2.6: 429 `rate_limited` | Không | Raw HTTP 429 có `Retry-After`, `X-RateLimit-Limit` · `Remaining: 0` · `Reset`, cho cả GET và POST | Khách #46091 phải hỏi cách xử lý 429. Docs chỉ có message của nhóm đọc "300 requests/minute (read)", không có message của POST (RX-43) | `[MAJOR]` | |
| RX-6 | **L354**, **L372** · 2.6: 500 `server_error` | Không | Body 500 + câu nhắc "POST có thể đã được thực thi" | — | `[MINOR]` | |

### 3.2 Idempotency — 3 endpoint POST

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-7 | **L441** · 2.9: "Trả lại nguyên response đã lưu + header Idempotency-Replayed: true" · **L332**: `X-Request-Id` khác `request_id` | Không | Raw HTTP 200 replay: `Idempotency-Replayed: true`, `X-Request-Id` mới khác `request_id` cũ trong body | #43646 đã trả lời khách sai: "gửi lại thì nhận 409" (report 03 `QA-1`). Client không biết 2 ID khác nhau là đúng | `[MAJOR]` | |
| RX-8 | **L442** · 2.9: 409 `conflict` "Idempotency-Key already used with a different request…" | Không | Body 409 `conflict` | Gửi lại với body khác, tưởng request đang chạy nên chờ mãi | `[MAJOR]` | |
| RX-9 | **L443** · 2.9: 409 `in_progress` "…still being processed." | Không | Body 409 `in_progress` | Không thấy 2 loại 409 khác nhau ở `error.code`, xử lý chung một nhánh | `[MAJOR]` | |
| RX-10 | **L427** · 2.9: 400 "Idempotency-Key must be at most 100 characters." | Không | Body 400 | — | `[NIT]` | |

### 3.3 `POST /messages/push` · `POST /messages/template` · mục 5 Message object

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-11 | **L973–L974**, **L1071–L1072** · Lỗi riêng: 403 `quota_exceeded` "月1000通の配信上限が超えました。" · "LINEプランの配信上限に達しました。" | Không | 2 body 403 (gói free LME · gói LINE OA) | Không biết `error.message` ở đây là tiếng Nhật. Không phân biệt 2 trường hợp vì cùng `code` (RX-47) | `[MAJOR]` | |
| RX-12 | **L976**, **L1074** · 422 "ブロックしていますので送信できません。" | Không | Body 422 friend đã chặn LINE OA | Retry mãi một friend không bao giờ nhận được tin | `[MAJOR]` | |
| RX-13 | **L975**, **L1073** · 422 "Bot plan expired (over 7 days)…" | Không | Body 422 | — | `[MINOR]` | |
| RX-14 | **L977**, **L1076** · 422 "(nội dung do hệ thống gửi tin trả về)" | Không. Docs không có message mẫu nào | ≥ 1 message thật hay gặp | Không biết message dạng gì, tiếng gì, nên không log hay hiển thị cho người vận hành được | `[MAJOR]` | |
| RX-15 | **L963–L971** · Lỗi friend + mảng `messages` (9 dòng) | Không | 400 thiếu `friend_id` · 422 vượt 5 phần tử · 404 friend (cả 2 kiểu `id_type`, L966) | — | `[MINOR]` | |
| RX-16 | **L1065–L1070**, **L1075** · Lỗi `templates` (6 dòng) | Không | 404 `template_id` · 422 `edited_content` (kèm giá trị `type` thật, RX-42) · 422 template không gửi được | — | `[MINOR]` | |
| RX-17 | **L1729–L1740** · 5 Kiểm tra URL media (9 dòng + cảnh báo HEAD 405 / 403) | Không | 1 body 422 cho `url` (vd S3 presigned trả 403 khi gọi HEAD) + 1 body 422 cho `preview_url` bị redirect | Docs tự cảnh báo đây là lỗi tích hợp hay gặp nhất (L1740) mà không có response mẫu | `[MAJOR]` | |
| RX-18 | **L1763–L1766**, **L1777–L1784**, **L1810–L1813** · text · preview · audio (13 dòng) | Không | ≥ 1 body có `messages[i]` | Không thấy chỉ số `messages[i]` đánh từ 0, khó biết lỗi ở phần tử nào | `[MINOR]` | |

### 3.4 `POST /do_action` · mục 6 Action object

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-19 | **L1619–L1628** · Lỗi cấp request (10 dòng) | Không | 400 thiếu `actions` · 422 vượt 100 friend · 422 sai `type` | — | `[MINOR]` | |
| RX-20 | **L1622** · 404 "lmessage_friend_ids not found: [99901, 99902]" | Không | Body 404 khi tất cả friend không thuộc bot | — | `[MINOR]` | |
| RX-21 | **L1845–L1920** · Lỗi từng action (21 dòng) + **L1870** URL IMAGE / FILE | Không | 404 `actions[0] tag_ids not found` · 422 `actions[1] DATE field value…` · 422 URL field IMAGE | Bảng mục 6 không có cột `error.code` (RX-48), không có ví dụ thì client phải tự đoán `code` | `[MAJOR]` | |

### 3.5 Endpoint GET

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-22 | **L525–L530** /friends · **L1198–L1205** /conversations (11 dòng 400 / 422) | Chỉ có 404 tag (L608, L1275) | 400 `limit=0` · 422 sai định dạng ngày · 422 `confirm_status=2` | — | `[MINOR]` | |
| RX-23 | **L648–L649** /friends/detail · **L1317–L1318** /conversations/detail · 400 thiếu / sai `lmessage_friend_id` | Không | 1 body 400 | — | `[NIT]` | |
| RX-24 | **L1319** · /conversations/detail: 404 "Conversation not found" | Không | Body 404, ghi rõ khác 404 friend | Friend có thật nhưng chưa có hội thoại, client lại tưởng ID friend sai | `[MINOR]` | |
| RX-25 | **L765**, **L824**, **L895**, **L1134** · 4 endpoint list: "Chỉ lỗi page/limit (400)" | Không | 1 ví dụ chung ở 2.8 là đủ | — | `[NIT]` | |

## 4. Header response

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-26 | **L330–L337** · 2.5: 6 header `X-Request-Id` · `X-RateLimit-Limit` · `-Remaining` · `-Reset` · `Retry-After` · `Idempotency-Replayed` | Không có ví dụ nào kèm header. 3 khối `HTTP/1.1 404` chỉ có dòng trạng thái | 1 raw HTTP 200 có đủ header chung (429 → RX-5 · replay → RX-7) | Không thấy header thật trông thế nào, khó làm theo khuyến nghị đọc `X-RateLimit-Remaining` (L389) | `[MINOR]` | |

## 5. Biến thể 200 còn thiếu ví dụ

| # | Chỗ docs mô tả (L + mục + trích) | Ví dụ hiện có | Cần thêm ví dụ | Client có thể làm sai thế nào | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| RX-27 | **L397** · 2.8: `limit` > 500 → kẹp + `data.warnings` · áp cho 5 endpoint có khối `pagination` | Chỉ có /friends (L597), mà /friends không có khối `pagination` | `/tags?limit=1000` → `data.warnings` + `pagination.limit: 500` | Không biết `warnings` nằm cạnh `tags` hay trong `pagination` | `[MINOR]` | |
| RX-28 | **L515**, **L520** · /friends: `line_friend_id`, `added_time` kiểu `… \| null` | Không. Ví dụ 3 (L579) "các field khác null" vẫn có 2 field này | 1 friend có 2 field này `null` + câu "khi nào null" | Client lưu vào cột NOT NULL sẽ lỗi | `[MINOR]` | |
| RX-29 | **L632–L633** · /friends/detail: `line_friend_id`, `line_name` kiểu `string \| null` | Không | Friend 12401 (L583, `line_name: ""` ở /friends) gọi /friends/detail → trả `""` hay `null` | Liên quan `DOC-INT-4` report 02: cùng friend mà 2 endpoint trả khác nhau | `[MINOR]` | |
| RX-30 | **L640** · `friend_info[].type` kiểu `string \| null` | Không. Docs cũng không nói khi nào `null` | 1 phần tử `type: null` + lý do | Client rẽ nhánh theo `type` bị lọt nhánh | `[MINOR]` | |
| RX-31 | **L642** · `friend_info[].value`: POINT có thể thập phân · POINT không parse được → `null` · DATE không nhận dạng được → trả nguyên chuỗi · bản ghi rỗng → `null` | Chỉ có số nguyên (L674, L706) và DATE chuẩn | `value: 12.5` · `value: null` · DATE dạng chuỗi gốc | Client khai báo POINT là integer, gặp số thập phân thì lỗi parse | `[MINOR]` | |
| RX-32 | **L1186**, **L1190** · /conversations: `line_friend_id`, `last_message_date` kiểu `… \| null` | Không | 1 hội thoại có 2 field này `null` + khi nào `null` | Client sắp xếp theo `last_message_date` lỗi khi gặp `null` | `[MINOR]` | |
| RX-33 | **L1272–L1273** · /conversations Ví dụ 3 (`display_status=hidden`) | Chỉ có request + 1 câu "cùng cấu trúc" | Body thật | — | `[NIT]` | |
| RX-34 | **L1312**, **L2009** · `block_status: "block"` (LME chặn friend) | Không (chỉ có `normal` L1413, `blocked` L1430) | 1 ví dụ `block` | Liên quan report 03 `P1` (cả 2 bên cùng chặn thì trả gì) | `[MINOR]` | |
| RX-35 | **L1313** · `favorite: "yes"` | Chỉ tả bằng lời (L1230) | Body /conversations/detail?lmessage_friend_id=12346 | — | `[NIT]` | |
| RX-36 | **L1434** · /conversations/detail Ví dụ 3 `messages: []` | Chỉ tả bằng lời | Body thật | — | `[NIT]` | |
| RX-37 | **L1309**, **L1462** · `scenario` có thể là string khi template của step đã bị xoá | Không | 1 dòng `message_type: "scenario"`, `data` dạng string | Client đọc `data` như mảng thì lỗi | `[MINOR]` | |
| RX-38 | **L1484** · `unknown`: "data giữ nguyên dữ liệu gốc, có thể null" | Chỉ có `null` | 1 ví dụ `unknown` có dữ liệu | Không biết dữ liệu gốc dạng gì để bỏ qua an toàn | `[MINOR]` | |
| RX-39 | **L1463** `start_day` là number, `start_time` "00:00:00" · **L1503** quick reply `flag_type_content_quick_reply: 2` · **L1537** URL tương đối `/msg_template/…` | Không | 1 ví dụ cho mỗi dạng | — | `[NIT]` | |
| RX-40 | **L1588** · /do_action: friend không thuộc bot bị bỏ qua, vẫn 200 | Không | Request lẫn 1 ID sai → 200, body giống hệt thành công | Client tưởng đã áp cho đủ friend (report 03 `P11`) | `[MINOR]` | |
| RX-41 | **L1584** · /do_action: action chạy tuần tự theo thứ tự khai báo | Không | `tag.add` rồi `tag.remove` cùng tag → 200, kết quả cuối là không có tag | Khách #46186 gặp đúng trường hợp này: API trả `success: true` nhưng tag không được tính | `[MINOR]` | |

## 6. Message lỗi ghi chưa đủ (R4)

| # | Chỗ (L + mục + trích) | Đang ghi | Thiếu gì | Severity | Quyết định Leader |
|---|---|---|---|---|---|
| RX-42 | **L1070** · /messages/template: "…template 7001 has type: …" | Giá trị `type` bị cắt | Danh sách giá trị `type` có thể có. /templates không trả loại template (L1158), nên message này là cách duy nhất để client biết loại | `[MINOR]` | |
| RX-43 | **L371** · Lỗi chung 429: "Rate limit exceeded: 300 requests/minute (read)" | Chỉ có message nhóm đọc | Message của nhóm ghi (POST, 60 / phút) | `[MINOR]` | |
| RX-44 | **L977**, **L1076** · 422 "(nội dung do hệ thống gửi tin trả về)" | Không có mẫu | Xem RX-14 | — | |
| RX-45 | **L1202–L1203** · /conversations 404: "handling_status_names not found: [フォローアップ]. …" · "tag_ids not found: [999]. …" | Phần cuối bị cắt | Câu đầy đủ (ví dụ L1279 có đủ câu cho `tag_names`) | `[NIT]` | |
| RX-46 | **L1735** · 5: "media url is not reachable: …" | Lý do bị cắt | Các lý do có thể có (timeout, TLS, từ chối kết nối…) | `[NIT]` | |

## 7. Điểm mâu thuẫn / dễ hiểu sai phát hiện khi rà

| # | Chỗ A (L + mục + trích) | Chỗ B (L + mục + trích) | Mâu thuẫn là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| RX-47 | **L324** · 2.4: "không so khớp chuỗi message trong code" · **L323**: "dùng `error.code` để rẽ nhánh" | **L973–L977** · /messages/push: cùng 422 `validation_error` cho friend chặn OA, gói hết hạn, hệ thống gửi tin từ chối · cùng 403 `quota_exceeded` cho gói LME và gói LINE OA | Mỗi trường hợp cần xử lý khác nhau (bỏ friend / gia hạn gói / sửa nội dung / chờ tháng sau / nâng gói LINE OA). Nhưng chúng dùng chung `error.code`, nên client chỉ phân biệt được bằng message, mà docs lại cấm so khớp message | Thêm `error.code` riêng (hoặc mã phụ) cho từng trường hợp | Ghi rõ các message này cố định, được phép so khớp, rồi đưa nguyên văn vào ví dụ | `[MAJOR]` | |
| RX-48 | **L1845**, **L1872**, **L1900**, **L1917** · Bảng lỗi mục 6 chỉ có cột `HTTP` · `message` · `Khi nào` | **L1618** · Bảng lỗi cấp request của /do_action có cột `code` | Lỗi từng action không ghi `error.code`. Client phải tự đoán 422 = `validation_error`, 404 = `not_found` | Thêm cột `code` vào bảng mục 5 và mục 6 | Thêm 1 câu chung: "mọi lỗi ở mục 5 / 6: 422 = `validation_error`, 404 = `not_found`" | `[MINOR]` | |

## 8. Ví dụ đề xuất WSSJ bổ sung

> Các khối dưới đây **dựng từ câu chữ của docs** (dẫn `L<n>`). `request_id`, ID và thời điểm là dữ liệu giả. Chỗ docs chưa có thì ghi `<…>`.
> WSSJ cần thay bằng response thật trước khi đưa vào docs.

**Ưu tiên 1 — `[MAJOR]`** (RX-5 · RX-7 · RX-8 · RX-9 · RX-11 · RX-12 · RX-14 · RX-17 · RX-21 · RX-47 — RX-47 cần WSSJ trả lời câu hỏi 1 ở §9 trước khi viết ví dụ)

Replay (RX-7, theo L441 + L332):

```http
HTTP/1.1 200
Idempotency-Replayed: true
X-Request-Id: req_20261116_8f1e22c0
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 57
X-RateLimit-Reset: 1794816120

{ "success": true, "request_id": "req_20261116_7a0060b3" }
```

409 đang xử lý / khác nội dung (RX-9, RX-8, theo L443 · L442):

```json
{ "success": false, "request_id": "req_20261116_9c0d1e2f",
  "error": { "code": "in_progress", "message": "A request with this Idempotency-Key is still being processed." } }
{ "success": false, "request_id": "req_20261116_9c0d1e30",
  "error": { "code": "conflict", "message": "Idempotency-Key already used with a different request (method/path/body mismatch)." } }
```

429 ở POST (RX-5, theo L336 · L353):

```http
HTTP/1.1 429
Retry-After: 18
X-Request-Id: req_20261116_a1b2c3d4
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1794816120

{ "success": false, "request_id": "req_20261116_a1b2c3d4",
  "error": { "code": "rate_limited", "message": "<message nhóm ghi — docs chưa ghi>" } }
```

403 hết hạn mức · 422 friend chặn OA (RX-11, RX-12, theo L973 · L976):

```json
{ "success": false, "request_id": "req_20261116_b2c3d4e5",
  "error": { "code": "quota_exceeded", "message": "月1000通の配信上限が超えました。" } }
{ "success": false, "request_id": "req_20261116_c3d4e5f6",
  "error": { "code": "validation_error", "message": "ブロックしていますので送信できません。" } }
```

422 URL media (RX-17, theo L1736 · L1740):

```json
{ "success": false, "request_id": "req_20261116_d4e5f6a7",
  "error": { "code": "validation_error", "message": "messages[1] media url returned HTTP 403." } }
```

422 lỗi từng action của /do_action (RX-21, theo L1878 · L1847; `code` là suy luận, xem RX-48):

```json
{ "success": false, "request_id": "req_20261116_e5f6a7b8",
  "error": { "code": "validation_error", "message": "actions[1] DATE field value must be in format YYYY-MM-DD, got: 2026/11/16" } }
{ "success": false, "request_id": "req_20261116_f6a7b8c9",
  "error": { "code": "not_found", "message": "actions[0] tag_ids not found: [999]" } }
```

RX-14 không dựng được: docs không có message mẫu nào. WSSJ phải cung cấp.

**Ưu tiên 2 — `[MINOR]`:** RX-1 → RX-4 · RX-6 · RX-13 · RX-15 → RX-16 · RX-18 → RX-20 · RX-22 · RX-24 · RX-26 → RX-32 · RX-34 · RX-37 · RX-38 · RX-40 · RX-41 · RX-42 · RX-43 · RX-48

**Ưu tiên 3 — `[NIT]`:** RX-10 · RX-23 · RX-25 · RX-33 · RX-35 · RX-36 · RX-39 · RX-45 · RX-46

## 9. Câu hỏi gửi WSSJ

> Chỉ để Leader copy, không gửi đi đâu.

| # | Câu hỏi | Liên quan |
|---|---|---|
| 1 | [1.3.0 · 2.4 / 4 /messages/push] Các trường hợp friend chặn OA, gói hết hạn, hệ thống gửi tin từ chối (cùng 422 `validation_error`) và 2 loại `quota_exceeded` có thể có `error.code` riêng không? Nếu không, có xác nhận các message này cố định để client được phép so khớp không? (trái với L324) | RX-47 |
| 2 | [1.3.0 · 2.6] Message của 429 với nhóm ghi (POST) là gì? | RX-43 |
| 3 | [1.3.0 · 4 /messages/template] Giá trị `type` trong message "…has type: …" gồm những giá trị nào? | RX-42 |
| 4 | [1.3.0 · 4 /messages/push] Cho vài message thật hay gặp của lỗi 422 "(nội dung do hệ thống gửi tin trả về)". | RX-14 |
| 5 | [1.3.0 · 4 /friends, /friends/detail, /conversations] Khi nào `line_friend_id`, `added_time`, `last_message_date`, `friend_info[].type` là `null`? /friends/detail trả `""` hay `null` cho friend không có tên LINE? | RX-28 → RX-32 |
| 6 | [1.3.0 · 6] Lỗi ở bảng mục 5 / 6 có `error.code` là `validation_error` (422) và `not_found` (404) không? | RX-48 |
| 7 | [1.3.0 · toàn bộ] Bản sau có thể bổ sung ≥ 1 ví dụ body cho mỗi cặp `HTTP` · `error.code` của từng endpoint (28 cặp đang thiếu, §2), kèm ví dụ raw HTTP có header (replay, 429) không? | §1 · §8 |
