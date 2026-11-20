# Inventory docs Public API — Đặc tả chi tiết LME Public API v1 (Phase 1) · bản 1.3.0 (16/11/2026)

> Nguồn: `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html` · sinh bởi `scripts/api_docs_extract.py inventory` · **L = số dòng trong file HTML nguồn** (dùng để trích dẫn trong report).
> Ô trống = docs không ghi → nguyên liệu `DOC-MISS`. KHÔNG sửa tay — chạy lại script.

## Endpoint (12)

| # | Method · Path | Tiêu đề | L |
|---|---|---|---|
| 1 | `GET /friends` | Lấy danh sách friend | L488 |
| 2 | `GET /friends/detail` | Lấy chi tiết friend | L619 |
| 3 | `GET /tags` | Lấy danh sách tag | L746 |
| 4 | `GET /friend-info-fields` | Lấy danh sách friend info field | L802 |
| 5 | `GET /scenarios` | Lấy danh sách scenario | L874 |
| 6 | `POST /messages/push` | Gửi message (text / image / video / audio) | L928 |
| 7 | `POST /messages/template` | Gửi template message | L1038 |
| 8 | `GET /templates` | Lấy danh sách template | L1117 |
| 9 | `GET /conversations` | Lấy danh sách conversation | L1164 |
| 10 | `GET /conversations/detail` | Lấy message gần nhất của friend | L1286 |
| 11 | `GET /handling-statuses` | Lấy danh sách trạng thái xử lý | L1545 |
| 12 | `POST /do_action` | Thực hiện hàng loạt action trên friend | L1578 |

## `GET /friends` — Lấy danh sách friend (L488)

### [input] Request header (L494)
| L | Header | Bắt buộc | Mô tả |
|---|---|---|---|
| L495 | X-LME-API-KEY | Bắt buộc | API key (2.2). |

### [input] Query parameter (L497)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L498 | page | integer | Tuỳ chọn | Trang cần lấy, từ 1 (2.8). | 1 |
| L499 | limit | integer | Tuỳ chọn | Số friend/trang, 1–500. > 500 bị kẹp về 500 + warnings. | 100 |
| L500 | line_names | string, CSV | Tuỳ chọn | Tìm gần đúng (chứa chuỗi) theo tên LINE hoặc tên quản lý trong LME, không phân biệt hoa/thường. Ký tự % _ được hiểu theo nghĩa đen. Nhiều tên → OR. | Không lọc theo tên |
| L501 | tag_ids | integer, CSV | Tuỳ chọn | Tag ID (từ /tags). Nhiều tag → OR (friend có ít nhất 1 tag). Mọi ID phải tồn tại trong bot, nếu không → 404. | Không lọc theo tag |
| L502 | emails | string, CSV | Tuỳ chọn | Email khớp chính xác. Nhiều email → OR. | Không lọc theo email |
| L503 | added_date_from | date | Tuỳ chọn | Ngày kết bạn từ (bao gồm), YYYY-MM-DD, giờ Nhật. | Không giới hạn đầu |
| L504 | added_date_to | date | Tuỳ chọn | Ngày kết bạn đến (bao gồm cả ngày đó), YYYY-MM-DD. Phải ≥ added_date_from. | Không giới hạn cuối |

### [output] Response (L509)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L510 | data.total_items | integer | Tổng số friend khớp điều kiện. |
| L511 | data.total_pages | integer | Tổng số trang theo limit đã áp dụng. |
| L512 | data.warnings | array<string> | Chỉ xuất hiện khi có cảnh báo. Hiện có: limit_clamped (limit > 500 đã bị kẹp). |
| L513 | data.friend_detail[] | array<object> | Friend của trang hiện tại. Mảng rỗng khi không có kết quả. |
| L514 | …[].lmessage_friend_id | integer | Friend ID của LME — dùng cho mọi endpoint khác. |
| L515 | …[].line_friend_id | string \| null | LINE user ID. |
| L516 | …[].line_name | string | Tên hiển thị LINE. Chuỗi rỗng "" nếu không có. |
| L517 | …[].system_name | string \| null | Tên quản lý đặt trong LME (システム表示名). |
| L518 | …[].email | string \| null | Email đã lưu. |
| L519 | …[].phone | string \| null | Số điện thoại đã lưu. |
| L520 | …[].added_time | date \| null | Ngày kết bạn, YYYY-MM-DD. Với friend old là ngày LME ghi nhận friend (không phải ngày kết bạn thật với LINE OA). |
| L521 | …[].friendtype | string | new — 新規友だち: kết bạn với LINE OA sau khi LINE OA đã kết nối LME. old — 既存友だち: đã là friend của LINE OA từ trước khi kết nối LME, được LME lấy về sau (ví dụ bằng chức năng 既存友だち情報取得). Vì vậy friend old có thể có added_time mới hơn friend new. |

### [error] Lỗi riêng (L524)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L525 | 400 | invalid_request | Parameter 'page' has an invalid format (expected a numeric value). | page/limit không phải số nguyên | Truyền số nguyên |
| L526 | 400 | invalid_request | limit must be a positive integer (1..500), got: 0 | limit ≤ 0 | Dùng 1–500 |
| L527 | 422 | validation_error | tag_ids must contain positive integer IDs (comma-separated), got: abc | tag_ids không phải số nguyên dương | Truyền ID số, phân tách dấu phẩy |
| L528 | 404 | not_found | tag_ids not found: [999]. Use GET /v1/tags to list available tags. | Tag không tồn tại / đã xoá / thuộc bot khác | Làm mới danh sách tag |
| L529 | 422 | validation_error | added_date_from must be in format YYYY-MM-DD | Sai định dạng ngày (cả added_date_to) | Dùng YYYY-MM-DD, ví dụ 2026-11-01 |
| L530 | 422 | validation_error | added_date_from must be <= added_date_to | Khoảng ngày đảo ngược | Đổi lại thứ tự |

## `GET /friends/detail` — Lấy chi tiết friend (L619)

### [input] Query parameter (L625)
| L | Parameter | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L626 | lmessage_friend_id | integer | Bắt buộc | Friend ID của LME. Mỗi request lấy 1 friend. |

### [output] Response (L630)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L631 | data.friend.lmessage_friend_id | integer | Friend ID của LME. |
| L632 | data.friend.line_friend_id | string \| null | LINE user ID. |
| L633 | data.friend.line_name | string \| null | Tên hiển thị LINE. |
| L634 | data.friend.system_name | string \| null | Tên quản lý (giá trị của field -1). |
| L635 | data.friend.email | string \| null | Giá trị field -3. |
| L636 | data.friend.phone | string \| null | Giá trị field -2. |
| L637 | data.friend.tags[] | array<object> | Tag đang gắn: {id, name}. Mảng rỗng nếu không có. |
| L638 | data.friend.friend_info[] | array<object> | Friend info: {id, type, name, value}. Chỉ gồm field friend đã có dữ liệu — field chưa từng nhập (built-in hay custom) không xuất hiện trong mảng, chứ không được trả kèm value: null. Muốn biết đủ danh sách field của bot, dùng /friend-info-fields. |
| L639 | …friend_info[].id | integer | Field ID (âm = built-in, xem 7.2). |
| L640 | …friend_info[].type | string \| null | TEXT POINT DATE SELECT IMAGE FILE. |
| L641 | …friend_info[].name | string | Tên field. |
| L642 | …friend_info[].value | string \| number \| null | Chuẩn hoá theo type: POINT → number (số nguyên hoặc thập phân; không parse được → null); DATE → YYYY-MM-DD (giá trị cũ dạng 2002.06.21, 2026/1/5 được chuẩn hoá; giá trị không nhận dạng được là ngày thì trả nguyên chuỗi đã lưu — client nên kiểm tra định dạng trước khi parse); SELECT → nhãn option (string, không phải option_id — kể cả field -6); IMAGE/FILE → URL string; TEXT → string. Field chưa có … |
| L643 | data.friend.scenarios[] | array<object> | Scenario friend đã tham gia: {id, name, status}. |
| L644 | …scenarios[].status | string | following (đang chạy), completed (đã chạy hết), stopped (đã dừng). |

### [error] Lỗi riêng (L647)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L648 | 400 | invalid_request | Missing required parameter 'lmessage_friend_id'. | Không truyền param | Thêm lmessage_friend_id |
| L649 | 400 | invalid_request | Parameter 'lmessage_friend_id' has an invalid format (expected a numeric value). | Truyền line_friend_id (U…) hoặc chuỗi | Dùng ID số từ /friends |
| L650 | 404 | not_found | Friend not found | Friend không tồn tại hoặc thuộc bot khác | Kiểm tra lại ID / API key |

## `GET /tags` — Lấy danh sách tag (L746)

### [input] Query parameter (L752)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L753 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L754 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L757)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L758 | data.tags[].id | integer | Tag ID. |
| L759 | data.tags[].name | string | Tên tag. |
| L760 | data.tags[].friend_count | integer | Số friend đang gắn tag. |
| L761 | data.warnings | array<string> | Chỉ khi limit > 500: ["limit_clamped"]. |
| L762 | pagination | object | 2.8. |

## `GET /friend-info-fields` — Lấy danh sách friend info field (L802)

### [input] Query parameter (L808)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L809 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L810 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L813)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L814 | data.fields[].field_id | integer | Field ID. Âm = built-in, dương = custom. |
| L815 | data.fields[].title | string | Tên field. |
| L816 | data.fields[].field_type | string | TEXT POINT DATE SELECT IMAGE FILE (7.1). |
| L817 | data.fields[].options | array<object> \| null | Chỉ có giá trị khi field_type = SELECT và field đã cấu hình option; còn lại luôn null. Field -6 (都道府県名) luôn trả đủ 47 option (7.3). |
| L818 | …options[].option_id | integer | Option ID — dùng cho option_id của action friend_info.set. |
| L819 | …options[].label | string | Nhãn option — là giá trị thấy được ở /friends/detail. |
| L820 | data.warnings | array<string> | Chỉ khi limit > 500. |
| L821 | pagination | object | 2.8. |

### [other] Giá trị chấp nhận khi ghi (/do_action) (L861)
| L | field_type | Giá trị hợp lệ |
|---|---|---|
| L862 | TEXT | Chuỗi bất kỳ. API không giới hạn độ dài ở bước kiểm tra. |
| L863 | POINT | Số nguyên, cho phép số âm (ví dụ -5). Không nhận số thập phân. API không giới hạn min/max ở bước kiểm tra. |
| L864 | DATE | YYYY-MM-DD. |
| L865 | SELECT | option_id trong options[]. |
| L866 | IMAGE / FILE | URL HTTPS — ràng buộc ở friend_info. |

## `GET /scenarios` — Lấy danh sách scenario (L874)

### [input] Query parameter (L880)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L881 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L882 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L885)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L886 | data.scenarios[].scenario_id | integer | Scenario ID. |
| L887 | data.scenarios[].name | string | Tên scenario. |
| L888 | data.scenarios[].followers_count | integer | Số friend đang nhận scenario (購読中). |
| L889 | data.scenarios[].completed_count | integer | Số friend đã nhận hết scenario (読了済). |
| L890 | data.scenarios[].dropped_count | integer | Số friend dừng giữa chừng (途中停止). |
| L891 | data.warnings | array<string> | Chỉ khi limit > 500. |
| L892 | pagination | object | 2.8. |

## `POST /messages/push` — Gửi message (text / image / video / audio) (L928)

### [input] Request header (L935)
| L | Header | Bắt buộc | Mô tả |
|---|---|---|---|
| L936 | X-LME-API-KEY | Bắt buộc | Key scope full. |
| L937 | Content-Type | Bắt buộc | application/json |
| L938 | Idempotency-Key | Khuyến nghị | ≤ 100 ký tự (2.9). Bỏ trống → không chống gửi trùng. |

### [input] Request body (L941)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L942 | friend_id | integer \| string | Bắt buộc | Friend nhận message. Kiểu phụ thuộc id_type: số (12345 hoặc "12345") với lmessage_friend_id; chuỗi U… với line_friend_id. | 400 |
| L943 | id_type | string | Tuỳ chọn | lmessage_friend_id \| line_friend_id (phân biệt chữ hoa/thường). | lmessage_friend_id |
| L944 | messages | array<Message object> | Bắt buộc | 1–5 phần tử, gửi theo thứ tự. | 400 |
| L945 | mark_confirmed | boolean | Tuỳ chọn | true → đánh dấu conversation là đã đọc (確認済み) sau khi gửi. | false (giữ nguyên trạng thái đã đọc) |

### [other] Cách tính hạn mức gửi tin (L953)
| L | Hạn mức | Cách đếm |
|---|---|---|
| L956 | Gói free của LME (1.000 tin/tháng) | 1 request gửi thành công = 1 tin, dù request có 1 hay 5 phần tử, và dù template nhóm nở ra bao nhiêu message. Nếu toàn bộ message trong request gửi lỗi, tin đó được hoàn lại. Bot gói trả phí của LME không bị đếm. |
| L957 | Gói LINE Official Account | Do LINE đếm theo số lần LME gọi API gửi của LINE. LME gửi tối đa 5 message mỗi lần gọi: request có ≤ 5 message tính 1 tin; request /messages/template nở ra hơn 5 message (template nhóm) được gửi thành nhiều lần gọi và tính nhiều tin. |

### [error] Lỗi riêng (L962)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L963 | 400 | invalid_request | friend_id is required. | Thiếu friend_id | Thêm field |
| L964 | 422 | validation_error | id_type must be one of lmessage_friend_id\|line_friend_id, got: line_user_id | Giá trị id_type lạ | Dùng 1 trong 2 giá trị |
| L965 | 422 | validation_error | friend_id must be a numeric lmessage_friend_id. | Gửi U… nhưng quên id_type=line_friend_id | Thêm id_type hoặc dùng ID số |
| L966 | 404 | not_found | friend not found: 12345 / friend not found, line_friend_id: U… | Friend không thuộc bot | Kiểm tra ID |
| L967 | 400 | invalid_request | messages is required. | Thiếu messages | Thêm mảng |
| L968 | 422 | validation_error | messages must be a non-empty array. | messages: [] | Ít nhất 1 phần tử |
| L969 | 422 | validation_error | messages exceeds max 5 per request. | > 5 phần tử | Tách thành nhiều request |
| L970 | 400 | invalid_request | messages[0].type is required. | Thiếu type hoặc phần tử null | Thêm type |
| L971 | 422 | validation_error | messages[0].type must be one of text\|image\|video\|audio, got: sticker | Loại message không hỗ trợ | Dùng text/image/video/audio; loại khác gửi qua template |
| L972 | 422 | validation_error | messages[i] … (xem mục 5) | Vi phạm ràng buộc text/media/preview/duration | Xem bảng lỗi của từng message object |
| L973 | 403 | quota_exceeded | 月1000通の配信上限が超えました。 | Hết hạn mức tin/tháng của gói | Chờ kỳ sau hoặc nâng gói |
| L974 | 403 | quota_exceeded | LINEプランの配信上限に達しました。 | Hết hạn mức tin của gói LINE Official Account | Chờ kỳ sau hoặc nâng gói LINE OA |
| L975 | 422 | validation_error | Bot plan expired (over 7 days). Sending is disabled. | Gói LME của bot đã hết hạn quá 7 ngày | Gia hạn gói trên LME |
| L976 | 422 | validation_error | ブロックしていますので送信できません。 | Friend đã chặn LINE OA (block_status = "blocked") | Không retry. Bỏ qua friend này cho tới khi friend bỏ chặn |
| L977 | 422 | validation_error | (nội dung do hệ thống gửi tin trả về) | Hệ thống gửi tin LME từ chối message | Đọc error.message, sửa nội dung |
| L978 | 400/409 | invalid_request / conflict / in_progress | — | Lỗi Idempotency-Key | 2.9 |

## `POST /messages/template` — Gửi template message (L1038)

### [input] Request body (L1052)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1053 | friend_id | integer \| string | Bắt buộc | Như /messages/push. | 400 |
| L1054 | id_type | string | Tuỳ chọn | lmessage_friend_id \| line_friend_id. | lmessage_friend_id |
| L1055 | templates | array<object> | Bắt buộc | 1–5 phần tử, gửi theo thứ tự. | 400 |
| L1056 | templates[].template_id | integer | Bắt buộc | Template ID từ /templates. | 400 |
| L1057 | templates[].edited_content mới | string | Tuỳ chọn | Nội dung text thay thế cho lần gửi này (token được thay như Text message; chuỗi rỗng = không thay thế). Nên giữ ≤ 5.000 ký tự — giới hạn text của LINE. Chỉ dùng với template loại text; template loại khác → 422 và không message nào được gửi. /templates hiện không trả loại template — hãy ghi lại loại khi tạo template trên LME, hoặc thử trên staging. Template gốc trên LME không bị sửa. | Gửi nội dung gốc của template |
| L1058 | mark_confirmed | boolean | Tuỳ chọn | Như /messages/push. | false |

### [error] Lỗi riêng (L1063)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1064 | 400 / 422 / 404 | — | friend_id is required. … | Lỗi friend (giống /messages/push) | — |
| L1065 | 400 | invalid_request | templates is required. | Thiếu templates | Thêm mảng |
| L1066 | 422 | validation_error | templates must be a non-empty array. | Mảng rỗng | ≥ 1 phần tử |
| L1067 | 422 | validation_error | templates exceeds max 5 per request. | > 5 phần tử | Tách request |
| L1068 | 400 | invalid_request | templates[0].template_id is required. | Thiếu template_id | Thêm ID |
| L1069 | 404 | not_found | templates[0] template_id not found: 7001 | Template không tồn tại, đã xoá (vào thùng rác), nằm trong thư mục ẩn, hoặc thuộc bot khác | Làm mới /templates |
| L1070 | 422 | validation_error | templates[0] edited_content is only allowed for text templates, template 7001 has type: … | Dùng edited_content với template không phải text | Bỏ edited_content |
| L1071 | 403 | quota_exceeded | 月1000通の配信上限が超えました。 | Hết hạn mức gửi tin | Chờ kỳ sau / nâng gói |
| L1072 | 403 | quota_exceeded | LINEプランの配信上限に達しました。 | Hết hạn mức tin của gói LINE Official Account | Chờ kỳ sau / nâng gói LINE OA |
| L1073 | 422 | validation_error | Bot plan expired (over 7 days). Sending is disabled. | Gói LME của bot đã hết hạn quá 7 ngày | Gia hạn gói trên LME |
| L1074 | 422 | validation_error | ブロックしていますので送信できません。 | Friend đã chặn LINE OA | Không retry |
| L1075 | 422 | validation_error | templates[0] template 7001 has no sendable message. | Template không có nội dung gửi được (ví dụ template nhóm rỗng) | Kiểm tra template trên LME |
| L1076 | 422 | validation_error | (nội dung do hệ thống gửi tin trả về) | Hệ thống gửi tin từ chối | Đọc error.message |

## `GET /templates` — Lấy danh sách template (L1117)

### [input] Query parameter (L1123)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1124 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L1125 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L1128)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L1129 | data.templates[].template_id | integer | Template ID. |
| L1130 | data.templates[].name | string | Tên template. |
| L1131 | data.warnings | array<string> | Chỉ khi limit > 500. |
| L1132 | pagination | object | 2.8. |

## `GET /conversations` — Lấy danh sách conversation (L1164)

### [input] Query parameter (L1170)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1171 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L1172 | limit | integer | Tuỳ chọn | 1–500. | 100 |
| L1173 | confirm_status | integer | Tuỳ chọn | 0 = đã đọc (確認済み), 1 = chưa đọc (未確認 — đang chờ trả lời). | Cả hai |
| L1174 | handling_status_ids | integer, CSV | Tuỳ chọn | Status ID từ /handling-statuses. Nhiều giá trị → OR. | Không lọc |
| L1175 | handling_status_names | string, CSV | Tuỳ chọn | Tên trạng thái xử lý, khớp chính xác, không phân biệt hoa/thường. Gộp OR với handling_status_ids. | Không lọc |
| L1176 | line_names | string, CSV | Tuỳ chọn | Tìm gần đúng theo tên LINE hoặc tên quản lý, không phân biệt hoa/thường. Nhiều tên → OR. | Không lọc |
| L1177 | tag_ids | integer, CSV | Tuỳ chọn | Tag ID của friend. Gộp với tag_names. | Không lọc |
| L1178 | tag_names | string, CSV | Tuỳ chọn | Tên tag, khớp chính xác, không phân biệt hoa/thường. | Không lọc |
| L1179 | tag_mode | string | Tuỳ chọn | or = có ít nhất 1 tag; and = có đủ tất cả tag. Chỉ có tác dụng khi có tag_ids/tag_names. | or |
| L1180 | display_status | string | Tuỳ chọn | display = đang hiển thị, hidden = đã ẩn, all = cả hai. | display |

### [output] Response (L1184)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L1185 | data.conversations[].lmessage_friend_id | integer | Dùng cho /conversations/detail, /friends/detail, /do_action. |
| L1186 | …[].line_friend_id | string \| null | LINE user ID. |
| L1187 | …[].line_name | string | Tên LINE; "" nếu không có. |
| L1188 | …[].system_name | string \| null | Tên quản lý trong LME. |
| L1189 | …[].last_message | string \| null | Nội dung tóm tắt của tin nhắn cuối. |
| L1190 | …[].last_message_date | datetime \| null | Thời điểm tin nhắn cuối, +09:00. |
| L1191 | …[].confirm_status | string | read (確認済み) \| unread (未確認). |
| L1192 | …[].handling_status | object \| null | {id, name}; null nếu chưa gắn. |
| L1193 | data.warnings | array<string> | Chỉ khi limit > 500. |
| L1194 | pagination | object | 2.8. |

### [error] Lỗi riêng (L1197)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1198 | 400 | invalid_request | Parameter 'limit' has an invalid format (expected a numeric value). | page/limit sai | 2.8 |
| L1199 | 422 | validation_error | confirm_status must be 0 (read) or 1 (unread), got: 2 | Giá trị khác 0/1 | Dùng 0 hoặc 1 |
| L1200 | 422 | validation_error | handling_status_ids must contain positive integer IDs (comma-separated), got: x | ID không phải số nguyên dương (tương tự tag_ids) | Sửa giá trị |
| L1201 | 404 | not_found | handling_status_ids not found: [99]. Use GET /v1/handling-statuses to list available statuses. | Status không tồn tại / thuộc bot khác | Làm mới danh sách |
| L1202 | 404 | not_found | handling_status_names not found: [フォローアップ]. … | Tên không khớp chính xác | Kiểm tra chính tả |
| L1203 | 404 | not_found | tag_ids not found: [999]. … / tag_names not found: [VIPP]. … | Tag không tồn tại | Làm mới /tags |
| L1204 | 422 | validation_error | tag_mode must be or\|and, got: xor | Giá trị lạ | or / and |
| L1205 | 422 | validation_error | display_status must be display\|hidden\|all, got: show | Giá trị lạ | Dùng 1 trong 3 giá trị |

## `GET /conversations/detail` — Lấy message gần nhất của friend (L1286)

### [other] Giới hạn (L1291)
| L | Hạng mục | Giới hạn |
|---|---|---|
| L1292 | Số message | Tối đa 100 message gần nhất. Không lấy được message cũ hơn qua API này. |
| L1293 | Thứ tự | Mới nhất trước (messages[0] là message mới nhất). |
| L1294 | Phạm vi lịch sử | Bot gói free: 180 ngày gần nhất. Bot trả phí: 365 ngày gần nhất. |
| L1295 | Message lỗi | Message gửi thất bại (trạng thái ERROR) không được trả về — khớp với màn hình chat của LME. |

### [input] Query parameter (L1299)
| L | Parameter | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1300 | lmessage_friend_id | integer | Bắt buộc | Friend cần lấy hội thoại. |

### [output] Response (L1303)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L1304 | data.lmessage_friend_id | integer | Friend đã truy vấn. |
| L1305 | data.messages[] | array<object> | 0–100 message, mới nhất trước. |
| L1306 | …[].delivery_date | datetime | Thời điểm gửi/nhận, +09:00. |
| L1307 | …[].sender | string | friend (friend gửi) \| LINE_OA (bot/nhân viên gửi, kể cả gửi tự động). |
| L1308 | …[].message_type | string | Loại message — xem 7.4. |
| L1309 | …[].data | string \| array \| object \| null | Nội dung đã chuẩn hoá theo message_type: text, image, video, audio, file, action_from_booking → string; template, broadcast, event, action, scenario → mảng (scenario có thể là string khi không còn dữ liệu template); pdf, sticker, location, stop_scenario, scenario_empty_step, start_remind, stop_remind, action_from_booking_salon/lesson → object; dòng log hệ thống có thể là null. Ví dụ đầy đủ từng lo… |
| L1310 | data.handling_status | object \| null | {id, name} trạng thái xử lý hiện tại. |
| L1311 | data.display_status | string | display \| hidden. |
| L1312 | data.block_status | string | normal \| blocked (friend đã chặn LINE OA) \| block (LME đã chặn friend). |
| L1313 | data.favorite | string | yes \| no. |

### [error] Lỗi riêng (L1316)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1317 | 400 | invalid_request | Missing required parameter 'lmessage_friend_id'. | Thiếu param | Thêm param |
| L1318 | 400 | invalid_request | Parameter 'lmessage_friend_id' has an invalid format (expected a numeric value). | Không phải số | Dùng ID số |
| L1319 | 404 | not_found | Conversation not found | Friend chưa có hội thoại hoặc thuộc bot khác | Kiểm tra ID |

### [other] Ví dụ data theo từng message_type (L1438)
| L | message_type | Phát sinh khi | sender | Ví dụ data |
|---|---|---|---|---|
| L1439 | text | Friend hoặc nhân viên nhắn văn bản; message gửi qua /messages/push (type text); template gửi kèm edited_content; thông báo trả lời form; dòng log hệ thống | friend / LINE_OA | "注文した商品の配送状況を教えてください" |
| L1440 | image | Friend gửi ảnh; nhân viên/API gửi ảnh | friend / LINE_OA | "https://p.lmes.jp/msg_template/line-user/media-step/2001/image/image_10001_100000000000000001_1794390000001.jpeg" |
| L1441 | video | Friend/nhân viên/API gửi video | friend / LINE_OA | "https://p.lmes.jp/msg_template/line-user/media-step/2001/video/video_10004_100000000000000004_1794390000004.mp4" |
| L1442 | audio | Friend/nhân viên/API gửi audio. URL có thể kèm ?duration=<ms> | friend / LINE_OA | "https://p.lmes.jp/msg_template/media/voices/1001/2001/sample_voice02.m4a?duration=728086" |
| L1443 | file | Friend gửi file | friend | "https://p.lmes.jp/msg_template/line-user/media-step/2001/file/file_10002_100000000000000002_1794390000002.pdf" |
| L1444 | pdf | Nhân viên gửi PDF từ màn hình chat | LINE_OA | { "file_name": "sample_guide.pdf", "file_size": 401609, "url": "https://p.lmes.jp/msg_template/media/pdf/1001/2001/sample_guide.pdf", "file_name_original": "ご案内資料.pdf" } |
| L1450 | sticker | Friend/nhân viên gửi sticker. ID là string | friend / LINE_OA | { "packageId": "11538", "stickerId": "51626506" } |
| L1451 | location | Friend gửi vị trí. latitude/longitude có thể là string hoặc null; title có thể null | friend | { "address": "東京都千代田区丸の内1丁目9-1", "latitude": "35.681236", "title": null, "longitude": null } |
| L1457 | template | Gửi template từ chat, auto reply, rich menu, /messages/template… Mảng các phần tử của template (xem bảng con bên dưới) | LINE_OA | [ { "type": "text", "content": "ご予約ありがとうございます。" }, { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample01/sample01.png" } ] |
| L1461 | broadcast | Message broadcast (一斉配信) | LINE_OA | [ { "type": "text", "content": "【11月限定】会員様限定セールのお知らせ" } ] |
| L1462 | scenario — message | Một step của scenario được gửi. Nếu không còn dữ liệu template của step (ví dụ template đã bị xoá), data có thể là string thay vì mảng | LINE_OA | [ { "type": "text", "content": "ご登録ありがとうございます！" } ] |
| L1463 | scenario — ghi nhận bắt đầu | Friend được cho vào scenario (ghi nhận, không phải message gửi đi). start_day là string hoặc number; start_time dạng "0:00" hoặc "00:00:00"; cả hai có thể null | LINE_OA | [ { "scenario_name": "新規登録フォロー", "start_day": "0", "start_time": "0:00" } ] |
| L1464 | stop_scenario | Scenario của friend bị dừng | LINE_OA | { "scenario_name": "新規登録フォロー" } hoặc{ "scenario_name": "新規登録フォロー", "start_day": null, "start_time": null } |
| L1465 | scenario_empty_step | Scenario chạy tới step không có nội dung. Các field có thể đều null | LINE_OA | { "scenario_name": null, "start_day": null, "start_time": null } |
| L1466 | event | Message của sự kiện / nhắc lịch (リマインダ) | LINE_OA | [ { "type": "text", "content": "明日10:00からセミナーを開催します。" } ] |
| L1467 | start_remind | Friend được đăng ký nhắc lịch. startDateTime dạng YYYY-MM-DD HH:mm (giờ Nhật), có thể null | LINE_OA | { "remind_name": "セミナー前日リマインド", "startDateTime": "2026-11-10 18:28" } |
| L1468 | stop_remind | Huỷ nhắc lịch của friend | LINE_OA | { "remind_name": "セミナー前日リマインド", "startDateTime": null } |
| L1469 | action | Message gửi bởi action (アクション) — ví dụ khi bấm rich menu, nút, trả lời form | LINE_OA | [ { "type": "buttons", "content": { "data": [ { "title": "キャンペーン", "text": "参加はこちら", "buttons": [ { "label": "参加する" } ] } ] } }, { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample02/sample02.jpg" } ] |
| L1473 | action_from_booking | Thông báo tự động từ đặt lịch / thanh toán. data là string | LINE_OA | "決済に失敗しました。\nカードのご利用枠や有効期限などをご確認いただき\n再度、購入手続きを行なってください。" |
| L1474 | action_from_booking_salon | Thông báo tự động của đặt lịch salon. type = loại thông báo (予約受付時アクション, 予約キャンセル時アクション, 予約前後のリマインドメッセージ…) | LINE_OA | { "type": "予約受付時アクション", "calendar_name": "渋谷店", "content": "田中様\n\n下記の通り、予約が完了いたしました。\n\n◇ 予約日時\n2026年11月17日（火）10:00-11:00\n\n◇ ご予約コース名\nカット\n\n◇ コース料金\n1,600円" } |
| L1479 | action_from_booking_lesson | Thông báo tự động của đặt lịch lesson. Cấu trúc giống salon | LINE_OA | { "type": "予約キャンセル時アクション", "calendar_name": "ヨガ教室", "content": "田中様\n\n下記の通り、キャンセルが完了いたしました。\n\n◇ 予約日時\n2026年11月24日（火）13:00-14:00" } |
| L1484 | unknown | Loại chưa được phân loại (hiện gồm: message gửi bởi action khi friend trả lời form). data giữ nguyên dữ liệu gốc, có thể null | LINE_OA | null |

### [other] Phần tử con của template / broadcast / scenario / event / action (L1489)
| L | type | Dạng content | Ví dụ |
|---|---|---|---|
| L1490 | text | string — nội dung template đã lưu. Token (ví dụ {name}) có thể còn ở dạng token, không phải giá trị friend thực nhận | { "type": "text", "content": "田中様、ご来店ありがとうございました。" } |
| L1491 | image | URL string (gồm cả imagemap) | { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample01/sample01.png" } |
| L1492 | video | URL string | { "type": "video", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample_video.mp4" } |
| L1493 | audio | object {file_name, file_size, url}. file_size có thể là -1 hoặc null khi không xác định | { "type": "audio", "content": { "file_name": "sample_voice01.m4a", "file_size": 4708093, "url": "https://p.lmes.jp/msg_template/media/voices/1001/2001/sample_voice01.m4a?duration=290816" } } |
| L1497 | sticker | object {packageId, stickerId} (string) | { "type": "sticker", "content": { "packageId": "8515", "stickerId": "16581243" } } |
| L1498 | location | object {address, latitude, longitude, title} — trong template toạ độ là number | { "type": "location", "content": { "address": "東京都千代田区丸の内1丁目", "latitude": 35.6812, "longitude": 139.7671, "title": "東京駅" } } |
| L1500 | buttons — panel | object {data: [{title, text, buttons: [{label}]}]}; mỗi phần tử data là 1 panel (carousel có nhiều panel) | { "type": "buttons", "content": { "data": [ { "title": "", "text": "コースA", "buttons": [ { "label": "予約する" }, { "label": "詳細" } ] }, { "title": "", "text": "コースB", "buttons": [ { "label": "予約する" } ] } ] } } |
| L1503 | buttons — quick reply | object {flag_type_content_quick_reply, text, content, buttons: [{label}]}. flag_type_content_quick_reply: 1 = nội dung là văn bản, 2 = nội dung là ảnh (text/content là URL ảnh) | { "type": "buttons", "content": { "flag_type_content_quick_reply": 1, "text": "ご希望の時間帯を選んでください", "content": "ご希望の時間帯を選んでください", "buttons": [ { "label": "午前" }, { "label": "午後" } ] } } |
| L1508 | introduction | object {friend_name, template_id, url_addfriend, content} (giới thiệu tài khoản) | { "type": "introduction", "content": { "friend_name": "LMEサポート", "template_id": 34353, "url_addfriend": "https://line.me/R/ti/p/@lme-support", "content": "こちらもご登録ください" } } |

### [other] Message gửi qua API sẽ hiển thị lại thế nào (L1514)
| L | Request đã gửi | message_type khi đọc lại | data |
|---|---|---|---|
| L1515 | /messages/push — type: text | text | Nguyên văn text trong request — token chưa được thay (ví dụ vẫn là {name}様) |
| L1516 | /messages/push — type: image / video | image / video | Nguyên văn url đã gửi |
| L1517 | /messages/push — type: audio | audio | URL string (url đã gửi) |
| L1518 | /messages/template — không có edited_content | template | Mảng phần tử của template |
| L1519 | /messages/template — có edited_content | text | Nội dung edited_content (token chưa được thay) |

### [other] Lưu ý khi xử lý data (L1526)
| L | data | Sự kiện |
|---|---|---|
| L1527 | null | Các dòng log còn lại (ví dụ kết bạn, friend chặn / bỏ chặn LINE OA, xoá message) |
| L1528 | "ブロックしました" | LME chặn friend |
| L1529 | "ブロックを解除しました" | LME bỏ chặn friend |
| L1530 | "非表示しました" | LME ẩn hội thoại |
| L1531 | "メッセージ受信により追加" | Friend được thêm vào LME khi nhắn tin tới LINE OA |

## `GET /handling-statuses` — Lấy danh sách trạng thái xử lý (L1545)

### [output] Response (L1551)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L1552 | data[] | array<object> | Toàn bộ trạng thái (mảng phẳng, không có khối pagination). Mảng rỗng nếu bot chưa tạo trạng thái nào. |
| L1553 | data[].id | integer | Status ID. |
| L1554 | data[].name | string | Tên trạng thái. |

## `POST /do_action` — Thực hiện hàng loạt action trên friend (L1578)

### [input] Request body (L1601)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1602 | lmessage_friend_ids | array<integer> | Bắt buộc | 1–100 friend (đếm sau khi bỏ trùng). Giới hạn cứng: > 100 → 422. | 400 |
| L1603 | actions | array<Action object> | Bắt buộc | 1–10 action. Giới hạn cứng: > 10 → 422. | 400 |

### [other] Bảng phân loại action (L1606)
| L | type | Mục đích | action | Field riêng |
|---|---|---|---|---|
| L1607 | tag | Gắn / gỡ tag | add remove | tag_ids |
| L1608 | friend_info | Cập nhật friend info | set clear today point_replace point_plus point_minus point_clear | field_id value option_id |
| L1609 | scenario | Chạy / dừng / chạy tiếp scenario | start stop resume | scenario_id start_from |
| L1610 | handling_status | Gắn / gỡ trạng thái xử lý | attach detach | handling_status_id |
| L1611 | block | Chặn / bỏ chặn / ẩn / hiện trong chat 1:1 | block unblock hide show | — |
| L1612 | favorite | Bật / tắt favorite | add remove | — |
| L1613 | confirm_status | Đã đọc / chưa đọc (確認/未確認) | confirm unconfirm | — |

### [error] Lỗi riêng (cấp request) (L1618)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1619 | 400 | invalid_request | lmessage_friend_ids is required. | Thiếu field | Thêm mảng |
| L1620 | 422 | validation_error | lmessage_friend_ids must be a non-empty array. | Mảng rỗng | ≥ 1 friend |
| L1621 | 422 | validation_error | lmessage_friend_ids exceeds max 100 per request. | > 100 friend | Chia lô 100 |
| L1622 | 404 | not_found | lmessage_friend_ids not found: [99901, 99902] | Không friend nào thuộc bot | Kiểm tra ID / API key |
| L1623 | 400 | invalid_request | actions is required. | Thiếu field | Thêm mảng |
| L1624 | 422 | validation_error | actions must be a non-empty array. | Mảng rỗng | ≥ 1 action |
| L1625 | 422 | validation_error | actions exceeds max 10 per request. | > 10 action | Tách request |
| L1626 | 400 | invalid_request | actions[0].type is required. | Thiếu type / phần tử null | Thêm type |
| L1627 | 422 | validation_error | actions[0] unknown type 'tags'. Valid: tag\|friend_info\|scenario\|handling_status\|block\|favorite\|confirm_status. | Sai type | Dùng giá trị hợp lệ |
| L1628 | 422 | validation_error | actions[0] invalid action for type 'tag'. Allowed: add\|remove. | Thiếu hoặc sai action | Xem bảng phân loại |
| L1629 | 404 / 422 | — | actions[i] … | Lỗi riêng từng loại action | mục 6 |

## Bảng ngoài endpoint (quy ước chung · object · bảng giá trị · changelog)

#### › 2. Quy ước chung › 2.1 Base URL & version
### [other] 2.1 Base URL & version (L226)
| L | Môi trường | Base URL | Ghi chú |
|---|---|---|---|
| L229 | Production | https://api.lmes.jp/v1 | Dữ liệu thật — message gửi đi là gửi thật tới LINE. |
| L230 | Staging | https://api-stg.lmes.jp/v1 | Dùng key phát hành trên môi trường staging. Key production không dùng được ở staging và ngược lại. |

#### › 2. Quy ước chung › 2.2 Xác thực
### [other] Quyền (scope) của key (L247)
| L | Scope | Được gọi | Gọi endpoint ghi (POST) |
|---|---|---|---|
| L250 | full | Mọi endpoint (GET + POST) | Cho phép |
| L251 | read | Chỉ GET | 403 forbidden "API key is read-only" |

### [other] Vòng đời key (L254)
| L | Trạng thái key | Kết quả khi gọi API | Cách xử lý |
|---|---|---|---|
| L257 | Đang hoạt động, còn hạn | 2xx | — |
| L258 | Hết hạn (expires_at đã qua) | 401 "API key expired" | Phát hành key mới. |
| L259 | Bị vô hiệu hoá / thu hồi | 403 "API key is no longer active" | Kích hoạt lại trên LME hoặc phát hành key mới. |
| L260 | Đã xoá | 401 "API key has been deleted" | Phát hành key mới. |
| L261 | Bot của key đã bị xoá | 403 "Bot not found or not accessible" | Liên hệ quản trị viên bot. |

#### › 2. Quy ước chung › 2.3 Định dạng request
### [other] 2.3 Định dạng request (L281)
| L | Hạng mục | Quy ước |
|---|---|---|
| L284 | Giao thức | Chỉ HTTPS. |
| L285 | GET | Parameter đặt ở query string, encode UTF-8 percent-encoding. Không gửi body. |
| L286 | POST | Body JSON UTF-8, header Content-Type: application/json bắt buộc (cho phép kèm ; charset=utf-8). Thiếu/sai → 400 "Content-Type must be application/json". |
| L287 | JSON lỗi cú pháp / sai kiểu field | 400 invalid_request "Request body is invalid (malformed JSON or wrong field type)." — ví dụ "tag_ids": "101" thay vì mảng số. |
| L288 | Field lạ trong body | Bị bỏ qua, không báo lỗi. Kiểm tra kỹ chính tả tên field — gõ sai tên field bắt buộc sẽ nhận lỗi "… is required". |
| L289 | Giá trị enum | type, action, tag_mode, display_status không phân biệt hoa/thường và được trim khoảng trắng. |
| L290 | Nhiều giá trị trong 1 query parameter | Phân tách bằng dấu phẩy (tag_ids=101,102) hoặc lặp parameter (tag_ids=101&tag_ids=102). Giá trị rỗng và trùng lặp bị bỏ. Tên có chứa dấu phẩy không lọc được bằng filter theo tên — dùng filter theo ID. |
| L291 | Ngày | YYYY-MM-DD (ISO 8601, ví dụ 2026-11-16). |
| L292 | Ngày giờ (response) | YYYY-MM-DDTHH:mm:ss+09:00 — luôn theo giờ Nhật (JST, UTC+9). |
| L293 | Múi giờ | Mọi filter ngày (ví dụ added_date_from) được hiểu theo giờ Nhật. |

#### › 2. Quy ước chung › 2.4 Định dạng response
### [field] Lỗi (L316)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L319 | success | boolean | true khi HTTP 2xx, false khi lỗi. |
| L320 | request_id | string | ID duy nhất của request, dạng req_YYYYMMDD_xxxxxxxx. Trùng với header X-Request-Id, trừ response replay của idempotency (xem 2.9). Ghi log giá trị này và gửi kèm khi liên hệ hỗ trợ. |
| L321 | data | object \| array | Dữ liệu trả về. Các POST không trả data (field vắng mặt). |
| L322 | pagination | object | Chỉ có ở endpoint phân trang dạng chuẩn (xem 2.8). Vắng mặt ở endpoint khác. |
| L323 | error.code | string | Mã lỗi máy đọc được — dùng giá trị này để rẽ nhánh xử lý. |
| L324 | error.message | string | Mô tả cho người đọc (tiếng Anh, riêng lỗi từ hệ thống gửi tin có thể là tiếng Nhật). Nội dung có thể thay đổi — không so khớp chuỗi message trong code. |

#### › 2. Quy ước chung › 2.5 Response header
### [other] 2.5 Response header (L329)
| L | Header | Có ở | Mô tả |
|---|---|---|---|
| L332 | X-Request-Id | Mọi response | ID của lần gọi này. Thường giống request_id trong body. Ngoại lệ: response replay của idempotency (có Idempotency-Replayed: true) — body là bản lưu từ lần gọi đầu nên mang request_id cũ, còn header mang ID mới của lần gọi lại. Khi liên hệ hỗ trợ, gửi cả hai. |
| L333 | X-RateLimit-Limit | Mọi response /v1 (kể cả 401/403) | Hạn mức/phút của nhóm request hiện tại: 300 (GET) hoặc 60 (POST). |
| L334 | X-RateLimit-Remaining | Mọi response /v1 | Số request còn lại trong phút hiện tại. Với response lỗi xác thực (chưa xác định được bot) giá trị bằng X-RateLimit-Limit. |
| L335 | X-RateLimit-Reset | Mọi response /v1 | Thời điểm cửa sổ reset, Unix epoch (giây, UTC). Ví dụ 1763280060. |
| L336 | Retry-After | Chỉ 429 | Số giây cần chờ trước khi gọi lại (≥ 1). |
| L337 | Idempotency-Replayed | POST trả lại kết quả đã lưu | true khi response là bản lưu từ lần gọi trước cùng Idempotency-Key — request không được thực thi lại. |

#### › 2. Quy ước chung › 2.6 Status code & mã lỗi
### [error] 2.6 Status code & mã lỗi (L341)
| L | HTTP | error.code | Ý nghĩa | Retry? | Ví dụ nguyên nhân |
|---|---|---|---|---|---|
| L344 | 200 | — | Thành công | — | — |
| L345 | 400 | invalid_request | Request sai định dạng | Không — sửa request | JSON lỗi, thiếu field/param bắt buộc, sai kiểu số, Content-Type sai, limit ≤ 0, Idempotency-Key > 100 ký tự |
| L346 | 401 | unauthorized | Xác thực thất bại | Không | Thiếu/sai key, key hết hạn, key đã xoá |
| L347 | 403 | forbidden | Không có quyền | Không | Key bị vô hiệu hoá, key read gọi POST, bot đã xoá |
| L348 | 403 | quota_exceeded | Hết hạn mức gửi tin của gói dịch vụ | Không (đến kỳ sau hoặc nâng gói) | Gói free vượt 1.000 tin/tháng: "月1000通の配信上限が超えました。"; hết hạn mức tin của gói LINE Official Account: "LINEプランの配信上限に達しました。" |
| L349 | 404 | not_found | Không tìm thấy | Không | Friend/tag/scenario/template/field/option/trạng thái xử lý không tồn tại, đã xoá, hoặc thuộc bot khác; endpoint/version không tồn tại |
| L350 | 409 | conflict | Xung đột idempotency | Không — dùng key mới | Idempotency-Key đã dùng cho request có body/path khác |
| L351 | 409 | in_progress | Request cùng key đang xử lý | Có — chờ vài giây | Gửi lại cùng Idempotency-Key khi lần đầu chưa xong |
| L352 | 422 | validation_error | Đúng định dạng nhưng giá trị không hợp lệ | Không — sửa giá trị | Vượt giới hạn số lượng/độ dài, sai enum, action không hợp với field type, URL media không truy cập được, friend đã chặn LINE OA, hệ thống gửi tin LME từ chối |
| L353 | 429 | rate_limited | Vượt rate limit | Có — sau Retry-After giây | > 300 GET/phút hoặc > 60 POST/phút của bot |
| L354 | 500 | server_error | Lỗi phía server | GET: có — backoff. POST: cẩn thận — request có thể đã được thực thi (xem 2.9) | "Internal server error" |

### [error] Lỗi chung — áp dụng cho mọi endpoint (L358)
| L | HTTP | code | message | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L361 | 401 | unauthorized | Missing X-LME-API-KEY header | Không gửi header hoặc header rỗng | Thêm header X-LME-API-KEY |
| L362 | 401 | unauthorized | Invalid API key | Key gõ sai, thừa ký tự, hoặc key của môi trường khác | Kiểm tra key và Base URL |
| L363 | 401 | unauthorized | API key has been deleted | Key đã bị xoá | Phát hành key mới |
| L364 | 401 | unauthorized | API key expired | Quá expires_at | Phát hành key mới |
| L365 | 403 | forbidden | API key is no longer active | Key bị vô hiệu hoá/thu hồi | Kích hoạt lại hoặc phát hành key mới |
| L366 | 403 | forbidden | API key is read-only | Key read gọi POST | Dùng key full |
| L367 | 403 | forbidden | Bot not found or not accessible | Bot gắn với key đã bị xoá | Liên hệ quản trị viên bot |
| L368 | 400 | invalid_request | Content-Type must be application/json | POST thiếu/sai Content-Type | Gửi Content-Type: application/json |
| L369 | 400 | invalid_request | Request body is invalid (malformed JSON or wrong field type). | Body không phải JSON hợp lệ hoặc field sai kiểu | Kiểm tra JSON và kiểu từng field |
| L370 | 404 | not_found | Endpoint not found: {METHOD} {path} | Sai path hoặc sai method | Đối chiếu Danh sách API |
| L371 | 429 | rate_limited | Rate limit exceeded: 300 requests/minute (read) | Vượt hạn mức phút | Chờ Retry-After giây |
| L372 | 500 | server_error | Internal server error | Lỗi không lường trước phía LME | GET: retry với exponential backoff. POST: xem 2.9 trước khi retry. Nếu lặp lại, gửi request_id cho bộ phận hỗ trợ |

#### › 2. Quy ước chung › 2.7 Rate limit
### [other] 2.7 Rate limit (L376)
| L | Nhóm | Method | Hạn mức |
|---|---|---|---|
| L379 | Đọc | GET | 300 request / phút / bot |
| L380 | Ghi | POST | 60 request / phút / bot |

#### › 2. Quy ước chung › 2.8 Phân trang
### [field] 2.8 Phân trang (L393)
| L | Parameter | Type | Mặc định | Quy tắc |
|---|---|---|---|---|
| L396 | page | integer | 1 | Bắt đầu từ 1. Bỏ trống, 0 hoặc số âm → coi là 1. Trang vượt quá tổng số trang → mảng rỗng (vẫn 200). Không phải số → 400. |
| L397 | limit | integer | 100 | 1–500. 0 hoặc âm → 400 "limit must be a positive integer (1..500), got: 0". Lớn hơn 500 → tự kẹp về 500 và response có data.warnings: ["limit_clamped"]. Không phải số → 400. |

### [field] Khối pagination (L401)
| L | Field | Type | Mô tả |
|---|---|---|---|
| L404 | page | integer | Trang đã trả về (sau khi chuẩn hoá). |
| L405 | limit | integer | Số record/trang đã áp dụng (sau khi kẹp). |
| L406 | total_items | integer | Tổng số record khớp điều kiện. |
| L407 | total_pages | integer | ceil(total_items / limit); 0 khi không có record. |
| L408 | has_next | boolean | true nếu còn trang sau. |

### [other] Khác biệt giữa các endpoint (L411)
| L | Endpoint | Cách trả phân trang |
|---|---|---|
| L414 | GET /tags, /friend-info-fields, /scenarios, /templates, /conversations | Khối pagination ở cấp gốc. |
| L415 | GET /friends | Không có khối pagination; dùng data.total_items và data.total_pages. Duyệt tới khi page ≥ data.total_pages. |
| L416 | GET /handling-statuses | Không phân trang — trả toàn bộ. |
| L417 | GET /conversations/detail | Không phân trang — cố định tối đa 100 message gần nhất. |

#### › 2. Quy ước chung › 2.9 Idempotency & retry
### [other] 2.9 Idempotency & retry (L423)
| L | Hạng mục | Quy tắc |
|---|---|---|
| L426 | Áp dụng | POST /messages/push, POST /messages/template, POST /do_action. GET bỏ qua header này. |
| L427 | Giá trị | Chuỗi do bạn tự sinh, tối đa 100 ký tự (vượt → 400 "Idempotency-Key must be at most 100 characters."). Khuyến nghị UUID v4 hoặc ID nghiệp vụ duy nhất (ví dụ order-8812-shipped). |
| L428 | Ký tự khuyến nghị | Khuyến nghị chỉ dùng chữ cái ASCII A–Z a–z, chữ số 0–9, dấu gạch ngang - và gạch dưới _. Server không chặn ký tự khác, nhưng tránh ký tự đặc biệt, dấu cách, ký tự có dấu hoặc tiếng Nhật — giá trị header HTTP không bảo đảm truyền đúng các ký tự này, nên lần retry có thể bị coi là key khác. |
| L429 | Khoảng trắng | Server cắt (trim) khoảng trắng ở hai đầu trước khi so khớp và đếm độ dài: " abc " và "abc" là cùng một key. Header rỗng hoặc chỉ có khoảng trắng được coi như không gửi. |
| L430 | Phạm vi | Duy nhất theo API key. Hai key khác nhau dùng cùng giá trị không ảnh hưởng nhau. |
| L431 | Thời gian lưu | Kết quả thành công được lưu ít nhất 24 giờ. Sau 24 giờ, bản lưu bị dọn định kỳ — thời điểm dọn không cố định, nên không dựa vào việc dùng lại cùng key sau 24 giờ (có thể nhận replay hoặc được thực thi như request mới). Mỗi thao tác nghiệp vụ nên dùng một key riêng. |
| L432 | "Cùng request" | So khớp method + path + body (byte-by-byte). Đổi thứ tự field hay khoảng trắng trong JSON cũng bị coi là request khác. |
| L433 | Không gửi header | Không có chống trùng — mỗi lần gọi đều được thực thi. |
| L434 | Khi hệ thống chống trùng gặp sự cố | Server vẫn xử lý request (không trả lỗi) nhưng không chống trùng cho request đó. Trường hợp hiếm, nhưng phía bạn vẫn nên có cơ chế tự kiểm tra trùng cho thao tác quan trọng. |

### [other] Hành vi khi gửi lại cùng key (L437)
| L | Tình huống | Response |
|---|---|---|
| L440 | Lần đầu (key mới) | Thực thi bình thường. Chỉ response 2xx được lưu. |
| L441 | Lần đầu đã thành công, gửi lại đúng request | Trả lại nguyên response đã lưu + header Idempotency-Replayed: true. Không thực thi lại. Body giữ request_id của lần đầu; header X-Request-Id là ID mới của lần gọi lại. |
| L442 | Lần đầu đã thành công, gửi lại với body/path khác | 409 conflict "Idempotency-Key already used with a different request (method/path/body mismatch)." |
| L443 | Lần đầu đang xử lý | 409 in_progress "A request with this Idempotency-Key is still being processed." — chờ vài giây rồi gửi lại. Nếu lần đầu treo quá 60 giây, server giải phóng key và thực thi lại. |
| L444 | Lần đầu bị lỗi (4xx/5xx) | Không lưu — gửi lại cùng key sẽ được thực thi lại (sau khi bạn sửa request). |

### [other] Chiến lược retry khuyến nghị (L447)
| L | Kết quả | Nên retry? | Cách |
|---|---|---|---|
| L450 | Timeout / lỗi mạng (không nhận được response) | Có | Giữ nguyên Idempotency-Key và body; backoff 1s → 2s → 4s… tối đa 5 lần. Nếu lần đầu đã xong → nhận replay; nếu đang xử lý → nhận 409 in_progress. |
| L451 | 500 với GET | Có | Backoff như trên. |
| L452 | 500 với POST | Cẩn thận | Response lỗi không được lưu, nên gửi lại cùng key sẽ được thực thi lại — Idempotency-Key không chặn trùng trong trường hợp này. Với /messages/*, message có thể đã vào hàng đợi gửi trước khi lỗi xảy ra: kiểm tra /conversations/detail trước khi gửi lại. /do_action chủ yếu là thao tác ghi đè (gắn tag, đặt giá trị…) nên gửi lại thường an toàn, trừ point_plus/point_minus và scenario.start. |
| L453 | 429 | Có | Chờ Retry-After. |
| L454 | 409 in_progress | Có | Chờ 2–5 giây, gửi lại cùng key. |
| L455 | 400 / 401 / 403 / 404 / 409 conflict / 422 | Không | Sửa request; nếu đổi body thì dùng key mới. |

#### › 3. Danh sách API
### [other] 3. Danh sách API (L463)
| L | Method | Path | Mục đích | Scope | Rate limit | Idempotency |
|---|---|---|---|---|---|---|
| L466 | GET | /v1/friends | Danh sách friend (lọc tên, tag, email, ngày kết bạn) | read / full | Đọc | — |
| L467 | GET | /v1/friends/detail | Chi tiết 1 friend (tag, friend info, scenario) | read / full | Đọc | — |
| L468 | GET | /v1/tags | Danh sách tag | read / full | Đọc | — |
| L469 | GET | /v1/friend-info-fields | Danh sách friend info field + option | read / full | Đọc | — |
| L470 | GET | /v1/scenarios | Danh sách scenario | read / full | Đọc | — |
| L471 | POST | /v1/messages/push | Gửi 1–5 message text/image/video/audio | full | Ghi | Có |
| L472 | POST | /v1/messages/template | Gửi 1–5 template có sẵn | full | Ghi | Có |
| L473 | GET | /v1/templates | Danh sách template | read / full | Đọc | — |
| L474 | GET | /v1/conversations | Danh sách conversation (lọc đã đọc, trạng thái xử lý, tag…) | read / full | Đọc | — |
| L475 | GET | /v1/conversations/detail | 100 message gần nhất của 1 friend + trạng thái | read / full | Đọc | — |
| L476 | GET | /v1/handling-statuses | Danh sách trạng thái xử lý | read / full | Đọc | — |
| L477 | POST | /v1/do_action | Chạy 1–10 action trên 1–100 friend | full | Ghi | Có |

#### › 5. Message object › Thuộc tính chung
### [field] Thuộc tính chung (L1718)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1719 | type | string | Bắt buộc | text \| image \| video \| audio. Không phân biệt hoa/thường. |

### [field] Kiểm tra URL media (image / video / audio) (L1724)
| L | Field | Request kiểm tra | Redirect |
|---|---|---|---|
| L1725 | url (image / video / audio) | HEAD. Nếu response HEAD không có Content-Length, server gửi thêm 1 GET để đếm dung lượng (dừng ngay khi vượt giới hạn) | Được theo |
| L1726 | preview_url (image / video) | GET (1 lần) | Không — 3xx là lỗi |

### [other] Kiểm tra URL media (image / video / audio) (L1729)
| L | Kiểm tra | message (ví dụ) |
|---|---|---|
| L1730 | URL bắt đầu bằng https:// hoặc http:// | messages[1] image requires a valid http(s) url. |
| L1731 | Độ dài ≤ 2.000 ký tự | messages[1] url exceeds 2000 chars. |
| L1732 | URL hợp lệ, có host | messages[1] media url is not a valid URL. / … has no host. |
| L1733 | Host phân giải được DNS | messages[1] media url host cannot be resolved: cdn.example.invalid |
| L1734 | Host là địa chỉ public (không phải localhost, IP nội bộ 10.x / 172.16–31.x / 192.168.x, link-local…) | messages[1] media url must be a public URL (internal address rejected). |
| L1735 | Kết nối được trong 5 giây | messages[1] media url is not reachable: … |
| L1736 | HTTP status < 400 (redirect được theo) | messages[1] media url returned HTTP 404. |
| L1737 | Content-Type thuộc danh sách cho phép (nếu server trả header này) | messages[1] unsupported media Content-Type 'image/gif' for type=image. Allowed: [image/jpeg, image/jpg, image/png]. |
| L1738 | Kích thước ≤ giới hạn (theo Content-Length; thiếu header thì đếm byte khi tải) | messages[1] image exceeds max size 10MB (Content-Length=12582912). |

#### › 5. Message object › Text message
### [field] Text message (L1744)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1745 | type | string | Bắt buộc | text |
| L1746 | text | string | Bắt buộc | Nội dung, 1–5.000 ký tự, không được chỉ toàn khoảng trắng. Đếm theo UTF-16 code unit — emoji và một số ký tự đặc biệt có thể tính 2 ký tự. Xuống dòng dùng \n. Token trong bảng dưới được thay bằng giá trị thật lúc gửi. |

### [other] Token trong text (L1750)
| L | Token | Thay bằng | Ví dụ kết quả |
|---|---|---|---|
| L1751 | {name} hoặc [name] | Tên LINE của friend | {name}様 → 田中太郎様 |
| L1752 | [FRIEND_INFO_system_name] [FRIEND_INFO_phone] [FRIEND_INFO_email] [FRIEND_INFO_birthday] [FRIEND_INFO_province] [FRIEND_INFO_zip_code] [FRIEND_INFO_district] [FRIEND_INFO_township] [FRIEND_INFO_building] | Giá trị built-in field tương ứng (-1, -2, -3, -4, -6, -7, -8, -9, -10) | [FRIEND_INFO_province] → 東京都 |
| L1753 | [FRIEND_INFO_<field_id>] | Giá trị custom field (field_id dương từ /friend-info-fields). Field IMAGE/FILE → URL xem file | [FRIEND_INFO_5001] → 20 |
| L1754 | [date] | Ngày gửi (giờ Nhật), dạng n月j日(D) | 11月16日(月) |
| L1755 | [date add=N] | Ngày gửi + N ngày (N có thể âm) | [date add=3] → 11月19日(木) |

### [error] Token trong text (L1763)
| L | Lỗi (422) | Khi nào |
|---|---|---|
| L1764 | messages[0] text requires non-blank text. | Thiếu text, rỗng, hoặc chỉ khoảng trắng |
| L1765 | messages[0] text exceeds 5000 chars. | > 5.000 ký tự |
| L1766 | messages[0] preview_url is only allowed for image/video messages. | Text kèm preview_url |

#### › 5. Message object › Image message
### [field] Image message (L1771)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1772 | type | string | Bắt buộc | image | — |
| L1773 | url | string | Bắt buộc | URL ảnh gốc. JPEG/PNG (image/jpeg, image/jpg, image/png), tối đa 10 MB, ≤ 2.000 ký tự. | 422 |
| L1774 | preview_url | string | Tuỳ chọn | Ảnh thu nhỏ hiển thị trong khung chat. Ràng buộc chặt hơn url — xem bảng dưới. | Dùng url làm preview |

### [other] Ràng buộc preview_url (image & video) (L1777)
| L | Ràng buộc | Lỗi (422) khi vi phạm |
|---|---|---|
| L1778 | Bắt buộc https:// (không chấp nhận http) | messages[1] preview_url must be a valid https url. |
| L1779 | ≤ 2.000 ký tự | messages[1] preview_url exceeds 2000 chars. |
| L1780 | Host public, phân giải được | … preview_url must be a public URL (internal address rejected). / … host cannot be resolved |
| L1781 | Không redirect (trả 3xx là lỗi) và status < 300 | messages[1] preview_url returned HTTP 302 (redirects are not allowed for preview_url). |
| L1782 | JPEG/PNG. Nếu server không trả Content-Type, đuôi URL phải là .jpg/.jpeg/.png | messages[1] preview_url must be JPEG/PNG, got Content-Type 'image/webp'. |
| L1783 | Tối đa 1 MB | messages[1] preview_url exceeds max size 1MB (Content-Length=…). |
| L1784 | Chỉ dùng cho image/video | messages[3] preview_url is only allowed for image/video messages. |

#### › 5. Message object › Video message
### [field] Video message (L1793)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1794 | type | string | Bắt buộc | video | — |
| L1795 | url | string | Bắt buộc | URL video MP4 (video/mp4), tối đa 200 MB, ≤ 2.000 ký tự. | 422 |
| L1796 | preview_url | string | Khuyến nghị | Ảnh bìa video, JPEG/PNG ≤ 1 MB, HTTPS, không redirect (bảng ràng buộc ở Image). Luôn truyền field này để friend thấy đúng ảnh bìa. | Dùng ảnh bìa mặc định của LME (ảnh "no thumbnail") |

#### › 5. Message object › Audio message
### [field] Audio message (L1805)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1806 | type | string | Bắt buộc | audio |
| L1807 | url | string | Bắt buộc | URL file M4A/MP3 (audio/m4a, audio/x-m4a, audio/mp4, audio/aac, audio/mpeg, audio/mp3), tối đa 200 MB. |
| L1808 | duration | integer | Bắt buộc | Độ dài file tính bằng millisecond, số nguyên dương (ví dụ 60 giây = 60000). Hiển thị trên LINE — hãy truyền đúng độ dài thật. |

### [error] Audio message (L1810)
| L | Lỗi (422) | Khi nào |
|---|---|---|
| L1811 | messages[3] audio requires duration (milliseconds). | Thiếu duration |
| L1812 | messages[3] duration must be a positive integer (milliseconds). | duration ≤ 0 |
| L1813 | messages[3] preview_url is only allowed for image/video messages. | Audio kèm preview_url |

#### › 5. Message object › Tóm tắt giới hạn
### [other] Tóm tắt giới hạn (L1819)
| L | Hạng mục | Giới hạn |
|---|---|---|
| L1820 | Message / request | 1–5 |
| L1821 | Text | 1–5.000 ký tự (UTF-16) |
| L1822 | URL (url, preview_url) | ≤ 2.000 ký tự |
| L1823 | Image | JPEG/PNG ≤ 10 MB |
| L1824 | Preview | JPEG/PNG ≤ 1 MB, HTTPS, không redirect |
| L1825 | Video | MP4 ≤ 200 MB |
| L1826 | Audio | M4A/MP3 ≤ 200 MB, duration bắt buộc |
| L1827 | Timeout kiểm tra URL | 5 giây / lần truy cập |

#### › 6. Action object
### [field] 6. Action object (L1835)
| L | Field chung | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1836 | type | string | Bắt buộc | Loại action. Không phân biệt hoa/thường. |
| L1837 | action | string | Bắt buộc | Thao tác, giá trị hợp lệ theo type. Thiếu → 422 "invalid action for type …". |

#### › 6. Action object › tag — gắn / gỡ tag
### [field] tag — gắn / gỡ tag (L1841)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1842 | action | string | Bắt buộc | add (gắn) \| remove (gỡ). Gắn tag đã có / gỡ tag chưa gắn không gây lỗi. add có thể kích hoạt hành động gắn với tag — xem tác dụng phụ. |
| L1843 | tag_ids | array<integer> | Bắt buộc | Tag ID từ /tags, ≥ 1 phần tử. Tất cả phải tồn tại trong bot. |

### [error] tag — gắn / gỡ tag (L1845)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1846 | 422 | actions[0] tag requires non-empty tag_ids. | Thiếu hoặc rỗng tag_ids |
| L1847 | 404 | actions[0] tag_ids not found: [999] | Tag không tồn tại / đã xoá / bot khác |

#### › 6. Action object › friend_info — cập nhật friend info
### [field] friend_info — cập nhật friend info (L1852)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1853 | action | string | Bắt buộc | set clear today point_replace point_plus point_minus point_clear — xem ma trận bên dưới. |
| L1854 | field_id | integer | Bắt buộc | Field ID từ /friend-info-fields (âm = built-in, dương = custom). |
| L1855 | value | string | Có điều kiện | Giá trị mới, bắt buộc với set (trừ SELECT) và point_replace/plus/minus. Được trim khoảng trắng 2 đầu. |
| L1856 | option_id | integer | Có điều kiện | Bắt buộc với set trên field SELECT (không nhận value). Lấy từ options[]; field -6 dùng STT 1–47 (7.3). |

### [other] Ma trận action × kiểu field (L1859)
| L | action | TEXT | DATE | POINT | SELECT | IMAGE | FILE | Kết quả |
|---|---|---|---|---|---|---|---|---|
| L1860 | set | value bất kỳ | value = YYYY-MM-DD | value số nguyên | option_id | value = URL ảnh | value = URL file | Ghi đè giá trị |
| L1861 | clear | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Xoá giá trị |
| L1862 | today | — | ✓ | — | — | — | — | Ghi ngày hiện tại (giờ Nhật) |
| L1863 | point_replace | — | — | value số nguyên | — | — | — | Đặt điểm = value |
| L1864 | point_plus | — | — | value số nguyên | — | — | — | Cộng value |
| L1865 | point_minus | — | — | value số nguyên | — | — | — | Trừ value |
| L1866 | point_clear | — | — | ✓ | — | — | — | Xoá điểm |

### [error] Lỗi (L1872)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1873 | 422 | actions[1] friend_info requires field_id. | Thiếu field_id |
| L1874 | 404 | actions[1] friend_info field_id not found: 5009 | Field không tồn tại / bot khác / built-in không có trong 7.2 |
| L1875 | 422 | actions[1] friend_info set on SELECT field requires option_id (value is not accepted). | set SELECT thiếu option_id (kể cả khi đã gửi value) |
| L1876 | 404 | actions[1] option_id not found in field 5002: 9 | Option không thuộc field; field -6 ngoài 1–47 ("valid: 1..47") |
| L1877 | 422 | actions[1] friend_info set requires value. | set thiếu / rỗng value |
| L1878 | 422 | actions[1] DATE field value must be in format YYYY-MM-DD, got: 2026/11/16 | Sai định dạng ngày |
| L1879 | 422 | actions[1] POINT field value must be an integer, got: 1.5 | set POINT không phải số nguyên |
| L1880 | 422 | actions[1] friend_info today only applies to DATE fields, field 5001 is not a DATE field. | today trên field không phải DATE |
| L1881 | 422 | actions[1] friend_info point_plus only applies to POINT fields, field -3 is not a POINT field. | point_* trên field không phải POINT |
| L1882 | 422 | actions[1] friend_info point_plus requires value (number). | Thiếu value |
| L1883 | 422 | actions[1] friend_info point_plus value must be an integer, got: ten | value không phải số nguyên |
| L1884 | 422 | actions[1] invalid action for type 'friend_info'. Allowed: set\|clear\|today\|point_replace\|point_plus\|point_minus\|point_clear. | Sai action |

#### › 6. Action object › scenario — chạy / dừng / chạy tiếp
### [field] scenario — chạy / dừng / chạy tiếp (L1895)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1896 | action | string | Bắt buộc | start — chạy scenario từ đầu; resume — chạy từ ngày chỉ định; stop — dừng scenario. |
| L1897 | scenario_id | integer | Có điều kiện | Bắt buộc với start/resume (phải tồn tại, chưa xoá). Với stop: không cần — xem lưu ý bên dưới. |
| L1898 | start_from | integer | Có điều kiện | Bắt buộc với resume: ngày bắt đầu trong scenario, ≥ 0 (ví dụ 3 = chạy tiếp từ ngày thứ 3). Bị bỏ qua với start (luôn từ ngày 0). |

### [error] scenario — chạy / dừng / chạy tiếp (L1900)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1901 | 422 | actions[2] scenario start/resume requires scenario_id. | Thiếu scenario_id |
| L1902 | 404 | actions[2] scenario_id not found: 88 | Scenario không tồn tại / đã xoá / bot khác |
| L1903 | 422 | actions[2] scenario resume requires start_from (>=0). | resume thiếu hoặc âm start_from |
| L1904 | 422 | actions[2] invalid action for type 'scenario'. Allowed: start\|stop\|resume. | Sai action |

#### › 6. Action object › handling_status — trạng thái xử lý
### [field] handling_status — trạng thái xử lý (L1913)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1914 | action | string | Bắt buộc | attach — gắn trạng thái (thay trạng thái cũ); detach — gỡ trạng thái hiện tại. |
| L1915 | handling_status_id | integer | Có điều kiện | Bắt buộc với attach; bỏ qua với detach. Từ /handling-statuses. |

### [error] handling_status — trạng thái xử lý (L1917)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1918 | 422 | actions[3] handling_status attach requires handling_status_id. | Thiếu ID |
| L1919 | 404 | actions[3] handling_status_id not found: 99 | Không tồn tại / bot khác |
| L1920 | 422 | actions[3] invalid action for type 'handling_status'. Allowed: attach\|detach. | Sai action |

#### › 6. Action object › block / favorite / confirm_status
### [other] block / favorite / confirm_status (L1927)
| L | type | action | Kết quả | Xem lại ở |
|---|---|---|---|---|
| L1928 | block | block | LME chặn friend (không nhận message từ friend trong chat 1:1) | block_status = "block" |
| L1929 | unblock | Bỏ chặn | block_status = "normal" |  |
| L1930 | hide | Ẩn conversation khỏi danh sách chat 1:1 | display_status = "hidden" |  |
| L1931 | show | Hiện lại conversation | display_status = "display" |  |
| L1932 | favorite | add | Đánh dấu favorite (lên đầu /conversations) | favorite = "yes" |
| L1933 | remove | Bỏ favorite | favorite = "no" |  |
| L1934 | confirm_status | confirm | Đánh dấu đã đọc (確認済み) | confirm_status = "read" |
| L1935 | unconfirm | Đánh dấu chưa đọc (未確認) | confirm_status = "unread" |  |

#### › 7. Bảng giá trị › 7.1 Kiểu friend info field
### [other] 7.1 Kiểu friend info field (L1948)
| L | field_type | Tên trên LME | Giá trị đọc ra (/friends/detail) | Cách ghi (/do_action) |
|---|---|---|---|---|
| L1949 | TEXT | 記述式 | string | set + value |
| L1950 | POINT | ポイント | number | point_* + value số nguyên |
| L1951 | DATE | 日付 | YYYY-MM-DD | set + value / today |
| L1952 | SELECT | 選択式 | nhãn option (string) | set + option_id |
| L1953 | IMAGE | 画像 | URL string | set + value URL |
| L1954 | FILE | ファイル | URL string | set + value URL |

#### › 7. Bảng giá trị › 7.2 Built-in field (ID âm)
### [other] 7.2 Built-in field (ID âm) (L1959)
| L | field_id | Tên (JP) | Ý nghĩa | field_type |
|---|---|---|---|---|
| L1960 | -1 | システム表示名 | Tên quản lý (= system_name) | TEXT |
| L1961 | -2 | 携帯電話 | Số điện thoại (= phone) | TEXT |
| L1962 | -3 | メールアドレス | Email (= email) | TEXT |
| L1963 | -4 | 生年月日 | Ngày sinh | DATE |
| L1964 | -6 | 都道府県名 | Tỉnh/thành (47 option cố định) | SELECT |
| L1965 | -7 | 郵便番号 | Mã bưu điện | TEXT |
| L1966 | -8 | 市区町村名 | Quận/huyện/thành phố | TEXT |
| L1967 | -9 | 町名/番地 | Địa chỉ/số nhà | TEXT |
| L1968 | -10 | 建物名・部屋番号 | Toà nhà/số phòng | TEXT |

#### › 7. Bảng giá trị › 7.3 Option của field -6 (都道府県名)
### [other] 7.3 Option của field -6 (都道府県名) (L1973)
| L | ID | Tỉnh | ID | Tỉnh | ID | Tỉnh | ID | Tỉnh |
|---|---|---|---|---|---|---|---|---|
| L1974 | 1 | 北海道 | 13 | 東京都 | 25 | 滋賀県 | 37 | 香川県 |
| L1975 | 2 | 青森県 | 14 | 神奈川県 | 26 | 京都府 | 38 | 愛媛県 |
| L1976 | 3 | 岩手県 | 15 | 新潟県 | 27 | 大阪府 | 39 | 高知県 |
| L1977 | 4 | 宮城県 | 16 | 富山県 | 28 | 兵庫県 | 40 | 福岡県 |
| L1978 | 5 | 秋田県 | 17 | 石川県 | 29 | 奈良県 | 41 | 佐賀県 |
| L1979 | 6 | 山形県 | 18 | 福井県 | 30 | 和歌山県 | 42 | 長崎県 |
| L1980 | 7 | 福島県 | 19 | 山梨県 | 31 | 鳥取県 | 43 | 熊本県 |
| L1981 | 8 | 茨城県 | 20 | 長野県 | 32 | 島根県 | 44 | 大分県 |
| L1982 | 9 | 栃木県 | 21 | 岐阜県 | 33 | 岡山県 | 45 | 宮崎県 |
| L1983 | 10 | 群馬県 | 22 | 静岡県 | 34 | 広島県 | 46 | 鹿児島県 |
| L1984 | 11 | 埼玉県 | 23 | 愛知県 | 35 | 山口県 | 47 | 沖縄県 |
| L1985 | 12 | 千葉県 | 24 | 三重県 | 36 | 徳島県 |  |  |

#### › 7. Bảng giá trị › 7.4 message_type và dạng data (/conversations/detail)
### [other] 7.4 message_type và dạng data (/conversations/detail) (L1989)
| L | message_type | Ý nghĩa | Dạng data |
|---|---|---|---|
| L1990 | text | Tin nhắn văn bản, thông báo trả lời form, dòng log hệ thống | string \| null |
| L1991 | image, video, audio | Media | string — URL (audio có thể kèm ?duration=) |
| L1992 | file | File friend gửi | string — URL |
| L1993 | pdf | PDF nhân viên gửi | object {file_name, file_size, url, file_name_original} |
| L1994 | sticker | Sticker | object {packageId, stickerId} (string) |
| L1995 | location | Vị trí | object {address, latitude, longitude, title} |
| L1996 | template, broadcast, event, action | Template / broadcast / nhắc lịch / action | array [{type, content}] |
| L1997 | scenario | Step của scenario hoặc ghi nhận bắt đầu scenario | array — phần tử là {type, content} hoặc {scenario_name, start_day, start_time}; có thể là string khi không còn dữ liệu template |
| L1998 | stop_scenario, scenario_empty_step | Dừng scenario / step rỗng | object {scenario_name, start_day?, start_time?} |
| L1999 | start_remind, stop_remind | Đăng ký / huỷ nhắc lịch | object {remind_name, startDateTime} |
| L2000 | action_from_booking | Thông báo đặt lịch / thanh toán | string |
| L2001 | action_from_booking_salon, action_from_booking_lesson | Thông báo đặt lịch salon / lesson | object {type, calendar_name, content} |
| L2002 | unknown | Loại chưa phân loại (hiện gồm action khi trả lời form) | nguyên trạng, thường null |

#### › 7. Bảng giá trị › 7.5 Trạng thái
### [field] 7.5 Trạng thái (L2007)
| L | Field | Giá trị | Ý nghĩa |
|---|---|---|---|
| L2008 | confirm_status | read / unread | Đã đọc (確認済み) / chưa đọc (未確認). Ở query của /conversations dùng số: 0 = read, 1 = unread. |
| L2009 | block_status | normal / blocked / block | Bình thường / friend đã chặn LINE OA / LME đã chặn friend. |
| L2010 | display_status | display / hidden | Hiển thị / đã ẩn trong chat 1:1. |
| L2011 | favorite | yes / no | Có / không favorite. |
| L2012 | scenarios[].status | following / completed / stopped | Đang nhận / đã nhận hết / đã dừng. |
| L2013 | sender | friend / LINE_OA | Friend gửi / bot hoặc nhân viên gửi. |
| L2014 | friendtype | old / new | 既存友だち (đã là friend trước khi LINE OA kết nối LME) / 新規友だち (kết bạn sau khi kết nối). Xem /friends. |

#### › 8. Lịch sử cập nhật
### [other] 8. Lịch sử cập nhật (L2022)
| L | Bản | Ngày | Nội dung thay đổi |
|---|---|---|---|
| L2025 | 1.3.0 | 16/11/2026 | Viết lại toàn bộ tài liệu theo dạng API reference, đối chiếu với hành vi thực tế của server. Không thay đổi API — chỉ bổ sung và sửa mô tả: ① Thêm ví dụ curl / Python / Node.js / Ruby cho cả 12 endpoint. ② Bổ sung bảng lỗi riêng cho từng endpoint (HTTP, code, message, nguyên nhân, cách xử lý) và thứ tự kiểm tra xác thực. ③ Ghi nhận 3 mã lỗi đã có nhưng chưa được mô tả: quota_exceeded (403), in_pro… |
| L2043 | 1.2.0 | 28/09/2026 | ① Bổ sung bảng built-in friend info field (ID âm) ở GET /friend-info-fields. ② Field -6 (都道府県名) là SELECT với 47 option cố định, option_id = STT 1–47; /do_action friend_info.set field -6 nhận option_id (ngoài 1..47 → 404; gửi value thay option_id → 422). |
| L2044 | 1.1.0 | 21/09/2026 | ① Resource thuộc bot khác trả 404. ② Đổi "compliant status" → "handling status" (/handling-statuses, data.handling_status). ③ GET /conversations (message gần nhất) đổi thành GET /conversations/detail; GET /conversations mới là danh sách conversation. ④ /do_action thêm confirm_status. ⑤ Bỏ tiền tố filters. ở query; /friends thêm line_names, đổi tag_id → tag_ids, email → emails. ⑥ Tách line_name / s… |
| L2045 | 1.0.0 | 10/09/2026 | Bản đầu tiên. |

## Tổng hợp

- 12 endpoint · 82 bảng · 90 dòng param/field (input + object) · 110 dòng lỗi

### Param kiểu ID theo endpoint (nguyên liệu ma trận bot A ↔ B — DOC-SEC)

| Endpoint | Param ID (L) |
|---|---|
| `GET /friends` | `tag_ids` (L501) |
| `GET /friends/detail` | `lmessage_friend_id` (L626) |
| `GET /tags` | — |
| `GET /friend-info-fields` | — |
| `GET /scenarios` | — |
| `POST /messages/push` | `friend_id` (L942) |
| `POST /messages/template` | `friend_id` (L1053), `templates[].template_id` (L1056) |
| `GET /templates` | — |
| `GET /conversations` | `handling_status_ids` (L1174), `tag_ids` (L1177) |
| `GET /conversations/detail` | `lmessage_friend_id` (L1300) |
| `GET /handling-statuses` | — |
| `POST /do_action` | `lmessage_friend_ids` (L1602) |

Param ID trong object (message / action):

- `tag_ids` (L1843, 6. Action object › tag — gắn / gỡ tag)
- `field_id` (L1854, 6. Action object › friend_info — cập nhật friend info)
- `option_id` (L1856, 6. Action object › friend_info — cập nhật friend info)
- `scenario_id` (L1897, 6. Action object › scenario — chạy / dừng / chạy tiếp)
- `handling_status_id` (L1915, 6. Action object › handling_status — trạng thái xử lý)
