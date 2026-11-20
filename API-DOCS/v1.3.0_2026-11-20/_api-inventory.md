# Inventory docs Public API — Đặc tả chi tiết LME Public API v1 (Phase 1) · bản 1.3.0 (16/11/2026)

> Nguồn: `spec-features/api-public/docs/api-detail-spec_vi_1120.html` · sinh bởi `scripts/api_docs_extract.py inventory` · **L = số dòng trong file HTML nguồn** (dùng để trích dẫn trong report).
> Ô trống = docs không ghi → nguyên liệu `DOC-MISS`. KHÔNG sửa tay — chạy lại script.

## Endpoint (12)

| # | Method · Path | Tiêu đề | L |
|---|---|---|---|
| 1 | `GET /friends` | Lấy danh sách friend | L450 |
| 2 | `GET /friends/detail` | Lấy chi tiết friend | L588 |
| 3 | `GET /tags` | Lấy danh sách tag | L738 |
| 4 | `GET /friend-info-fields` | Lấy danh sách friend info field | L802 |
| 5 | `GET /scenarios` | Lấy danh sách scenario | L887 |
| 6 | `POST /messages/push` | Gửi message (text / image / video / audio) | L949 |
| 7 | `POST /messages/template` | Gửi template message | L1059 |
| 8 | `GET /templates` | Lấy danh sách template | L1145 |
| 9 | `GET /conversations` | Lấy danh sách conversation | L1200 |
| 10 | `GET /conversations/detail` | Lấy message gần nhất của friend | L1330 |
| 11 | `GET /handling-statuses` | Lấy danh sách trạng thái xử lý | L1596 |
| 12 | `POST /do_action` | Thực hiện hàng loạt action trên friend | L1636 |

## `GET /friends` — Lấy danh sách friend (L450)

### [input] Request header (L456)
| L | Header | Bắt buộc | Mô tả |
|---|---|---|---|
| L457 | X-LME-API-KEY | Bắt buộc | API key (2.2). |

### [input] Query parameter (L459)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L460 | page | integer | Tuỳ chọn | Trang cần lấy, từ 1 (2.8). | 1 |
| L461 | limit | integer | Tuỳ chọn | Số friend/trang, 1–500. > 500 bị kẹp về 500 + warnings. | 100 |
| L462 | line_names | string, CSV | Tuỳ chọn | Tìm gần đúng (chứa chuỗi) theo tên LINE hoặc tên quản lý trong LME, không phân biệt hoa/thường. Ký tự % _ được hiểu theo nghĩa đen. Nhiều tên → OR. | Không lọc theo tên |
| L463 | tag_ids | integer, CSV | Tuỳ chọn | Tag ID (từ /tags). Nhiều tag → OR (friend có ít nhất 1 tag). Mọi ID phải tồn tại trong bot, nếu không → 404. | Không lọc theo tag |
| L464 | emails | string, CSV | Tuỳ chọn | Email khớp chính xác. Nhiều email → OR. | Không lọc theo email |
| L465 | added_date_from | date | Tuỳ chọn | Ngày kết bạn từ (bao gồm), YYYY-MM-DD, giờ Nhật. | Không giới hạn đầu |
| L466 | added_date_to | date | Tuỳ chọn | Ngày kết bạn đến (bao gồm cả ngày đó), YYYY-MM-DD. Phải ≥ added_date_from. | Không giới hạn cuối |

### [output] Response (L471)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L474 | data.total_items | integer | — | Tổng số friend khớp điều kiện. |
| L475 | data.total_pages | integer | — | Tổng số trang theo limit đã áp dụng. |
| L476 | data.warnings | array<string> | — | Chỉ xuất hiện khi có cảnh báo. Hiện có: limit_clamped (limit > 500 đã bị kẹp). |
| L477 | data.friend_detail[] | array<FriendSummary> | — | Friend của trang hiện tại. Mảng rỗng khi không có kết quả. |

### [field] Object FriendSummary (L480)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L483 | lmessage_friend_id | integer | — | Friend ID của LME — dùng cho mọi endpoint khác. |
| L484 | line_friend_id | string | Có | LINE user ID. |
| L485 | line_name | string | — | Tên hiển thị LINE. Chuỗi rỗng "" nếu không có. |
| L486 | system_name | string | Có | Tên quản lý đặt trong LME (システム表示名). |
| L487 | email | string | Có | Email đã lưu. |
| L488 | phone | string | Có | Số điện thoại đã lưu. |
| L489 | added_time | date | Có | Ngày kết bạn, YYYY-MM-DD. Với friend old là ngày LME ghi nhận friend (không phải ngày kết bạn thật với LINE OA). |
| L490 | friendtype | string | — | new — 新規友だち: kết bạn với LINE OA sau khi LINE OA đã kết nối LME. old — 既存友だち: đã là friend của LINE OA từ trước khi kết nối LME, được LME lấy về sau (ví dụ bằng chức năng 既存友だち情報取得). Vì vậy friend old có thể có added_time mới hơn friend new. |

### [error] Lỗi riêng (L493)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L494 | 400 | invalid_request | Parameter 'page' has an invalid format (expected a numeric value). | page/limit không phải số nguyên | Truyền số nguyên |
| L495 | 400 | invalid_request | limit must be a positive integer (1..500), got: 0 | limit ≤ 0 | Dùng 1–500 |
| L496 | 422 | validation_error | tag_ids must contain positive integer IDs (comma-separated), got: abc | tag_ids không phải số nguyên dương | Truyền ID số, phân tách dấu phẩy |
| L497 | 404 | not_found | tag_ids not found: [999]. Use GET /v1/tags to list available tags. | Tag không tồn tại / đã xoá / thuộc bot khác | Làm mới danh sách tag |
| L498 | 422 | validation_error | added_date_from must be in format YYYY-MM-DD | Sai định dạng ngày (cả added_date_to) | Dùng YYYY-MM-DD, ví dụ 2026-11-01 |
| L499 | 422 | validation_error | added_date_from must be <= added_date_to | Khoảng ngày đảo ngược | Đổi lại thứ tự |

## `GET /friends/detail` — Lấy chi tiết friend (L588)

### [input] Query parameter (L594)
| L | Parameter | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L595 | lmessage_friend_id | integer | Bắt buộc | Friend ID của LME. Mỗi request lấy 1 friend. |

### [output] Response (L599)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L602 | data.friend.lmessage_friend_id | integer | — | Friend ID của LME. |
| L603 | data.friend.line_friend_id | string | Có | LINE user ID. |
| L604 | data.friend.line_name | string | Có | Tên hiển thị LINE. |
| L605 | data.friend.system_name | string | Có | Tên quản lý (giá trị của field -1). |
| L606 | data.friend.email | string | Có | Giá trị field -3. |
| L607 | data.friend.phone | string | Có | Giá trị field -2. |
| L608 | data.friend.tags[] | array<FriendTag> | — | Tag đang gắn. Mảng rỗng nếu không có. |
| L609 | data.friend.friend_info[] | array<FriendInfo> | — | Friend info. Chỉ gồm field friend đã có dữ liệu — field chưa từng nhập (built-in hay custom) không xuất hiện trong mảng, chứ không được trả kèm value: null. Muốn biết đủ danh sách field của bot, dùng /friend-info-fields. |
| L610 | data.friend.scenarios[] | array<FriendScenario> | — | Scenario friend đã tham gia. |

### [field] Object FriendTag (L613)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L616 | id | integer | — | Tag ID. |
| L617 | name | string | — | Tên tag. |

### [field] Object FriendInfo (L620)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L623 | id | integer | — | Field ID (âm = built-in, xem 7.2). |
| L624 | type | string | Có | TEXT POINT DATE SELECT IMAGE FILE. |
| L625 | name | string | — | Tên field. |
| L626 | value | string \| number | Có | Chuẩn hoá theo type: POINT → number (số nguyên hoặc thập phân; không parse được → null); DATE → YYYY-MM-DD (giá trị cũ dạng 2002.06.21, 2026/1/5 được chuẩn hoá; giá trị không nhận dạng được là ngày thì trả nguyên chuỗi đã lưu — client nên kiểm tra định dạng trước khi parse); SELECT → nhãn option (string, không phải option_id — kể cả field -6); IMAGE/FILE → URL string; TEXT → string. Field chưa có … |

### [field] Object FriendScenario (L629)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L632 | id | integer | — | Scenario ID. |
| L633 | name | string | — | Tên scenario. |
| L634 | status | string | — | following (đang chạy), completed (đã chạy hết), stopped (đã dừng). |

### [error] Lỗi riêng (L637)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L638 | 400 | invalid_request | Missing required parameter 'lmessage_friend_id'. | Không truyền param | Thêm lmessage_friend_id |
| L639 | 400 | invalid_request | Parameter 'lmessage_friend_id' has an invalid format (expected a numeric value). | Truyền line_friend_id (U…) hoặc chuỗi | Dùng ID số từ /friends |
| L640 | 404 | not_found | Friend not found | Friend không tồn tại hoặc thuộc bot khác | Kiểm tra lại ID / API key |

## `GET /tags` — Lấy danh sách tag (L738)

### [input] Query parameter (L744)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L745 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L746 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L749)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L752 | data.tags[] | array<Tag> | — | Danh sách tag. Mảng rỗng nếu bot chưa có tag. |
| L753 | data.warnings | array<string> | — | Chỉ khi limit > 500: ["limit_clamped"]. |
| L754 | pagination | Pagination | — | Khối phân trang (2.8). |

### [field] Object Tag (L757)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L760 | id | integer | — | Tag ID. |
| L761 | name | string | — | Tên tag. |
| L762 | friend_count | integer | — | Số friend đang gắn tag. |

## `GET /friend-info-fields` — Lấy danh sách friend info field (L802)

### [input] Query parameter (L808)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L809 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L810 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L813)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L816 | data.fields[] | array<FriendInfoField> | — | Danh sách friend info field (built-in trước, custom sau). |
| L817 | data.warnings | array<string> | — | Chỉ khi limit > 500. |
| L818 | pagination | Pagination | — | Khối phân trang (2.8). |

### [field] Object FriendInfoField (L821)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L824 | field_id | integer | — | Field ID. Âm = built-in, dương = custom. |
| L825 | title | string | — | Tên field. |
| L826 | field_type | string | — | TEXT POINT DATE SELECT IMAGE FILE (7.1). |
| L827 | options | array<Option> | Có | Chỉ có giá trị khi field_type = SELECT và field đã cấu hình option; còn lại luôn null. Field -6 (都道府県名) luôn trả đủ 47 option (7.3). |

### [field] Object Option (L830)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L833 | option_id | integer | — | Option ID — dùng cho option_id của action friend_info.set. |
| L834 | label | string | — | Nhãn option — là giá trị thấy được ở /friends/detail. |

### [other] Giá trị chấp nhận khi ghi (/do_action) (L874)
| L | field_type | Giá trị hợp lệ |
|---|---|---|
| L875 | TEXT | Chuỗi bất kỳ. API không giới hạn độ dài ở bước kiểm tra. |
| L876 | POINT | Số nguyên, cho phép số âm (ví dụ -5). Không nhận số thập phân. API không giới hạn min/max ở bước kiểm tra. |
| L877 | DATE | YYYY-MM-DD. |
| L878 | SELECT | option_id trong options[]. |
| L879 | IMAGE / FILE | URL HTTPS — ràng buộc ở friend_info. |

## `GET /scenarios` — Lấy danh sách scenario (L887)

### [input] Query parameter (L893)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L894 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L895 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L898)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L901 | data.scenarios[] | array<Scenario> | — | Danh sách scenario. Mảng rỗng nếu bot chưa có scenario. |
| L902 | data.warnings | array<string> | — | Chỉ khi limit > 500. |
| L903 | pagination | Pagination | — | Khối phân trang (2.8). |

### [field] Object Scenario (L906)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L909 | scenario_id | integer | — | Scenario ID. |
| L910 | name | string | — | Tên scenario. |
| L911 | followers_count | integer | — | Số friend đang nhận scenario (購読中). |
| L912 | completed_count | integer | — | Số friend đã nhận hết scenario (読了済). |
| L913 | dropped_count | integer | — | Số friend dừng giữa chừng (途中停止). |

## `POST /messages/push` — Gửi message (text / image / video / audio) (L949)

### [input] Request header (L956)
| L | Header | Bắt buộc | Mô tả |
|---|---|---|---|
| L957 | X-LME-API-KEY | Bắt buộc | Key scope full. |
| L958 | Content-Type | Bắt buộc | application/json |
| L959 | Idempotency-Key | Khuyến nghị | ≤ 100 ký tự (2.9). Bỏ trống → không chống gửi trùng. |

### [input] Request body (L962)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L963 | friend_id | integer \| string | Bắt buộc | Friend nhận message. Kiểu phụ thuộc id_type: số (12345 hoặc "12345") với lmessage_friend_id; chuỗi U… với line_friend_id. | 400 |
| L964 | id_type | string | Tuỳ chọn | lmessage_friend_id \| line_friend_id (phân biệt chữ hoa/thường). | lmessage_friend_id |
| L965 | messages | array<Message> | Bắt buộc | 1–5 phần tử, gửi theo thứ tự. | 400 |
| L966 | mark_confirmed | boolean | Tuỳ chọn | true → đánh dấu conversation là đã đọc (確認済み) sau khi gửi. | false (giữ nguyên trạng thái đã đọc) |

### [other] Cách tính hạn mức gửi tin (L974)
| L | Hạn mức | Cách đếm |
|---|---|---|
| L977 | Gói free của LME (1.000 tin/tháng) | 1 request gửi thành công = 1 tin, dù request có 1 hay 5 phần tử, và dù template nhóm nở ra bao nhiêu message. Nếu toàn bộ message trong request gửi lỗi, tin đó được hoàn lại. Bot gói trả phí của LME không bị đếm. |
| L978 | Gói LINE Official Account | Do LINE đếm theo số lần LME gọi API gửi của LINE. LME gửi tối đa 5 message mỗi lần gọi: request có ≤ 5 message tính 1 tin; request /messages/template nở ra hơn 5 message (template nhóm) được gửi thành nhiều lần gọi và tính nhiều tin. |

### [error] Lỗi riêng (L983)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L984 | 400 | invalid_request | friend_id is required. | Thiếu friend_id | Thêm field |
| L985 | 422 | validation_error | id_type must be one of lmessage_friend_id\|line_friend_id, got: line_user_id | Giá trị id_type lạ | Dùng 1 trong 2 giá trị |
| L986 | 422 | validation_error | friend_id must be a numeric lmessage_friend_id. | Gửi U… nhưng quên id_type=line_friend_id | Thêm id_type hoặc dùng ID số |
| L987 | 404 | not_found | friend not found: 12345 / friend not found, line_friend_id: U… | Friend không thuộc bot | Kiểm tra ID |
| L988 | 400 | invalid_request | messages is required. | Thiếu messages | Thêm mảng |
| L989 | 422 | validation_error | messages must be a non-empty array. | messages: [] | Ít nhất 1 phần tử |
| L990 | 422 | validation_error | messages exceeds max 5 per request. | > 5 phần tử | Tách thành nhiều request |
| L991 | 400 | invalid_request | messages[0].type is required. | Thiếu type hoặc phần tử null | Thêm type |
| L992 | 422 | validation_error | messages[0].type must be one of text\|image\|video\|audio, got: sticker | Loại message không hỗ trợ | Dùng text/image/video/audio; loại khác gửi qua template |
| L993 | 422 | validation_error | messages[i] … (xem mục 5) | Vi phạm ràng buộc text/media/preview/duration | Xem bảng lỗi của từng message object |
| L994 | 403 | quota_exceeded | 月1000通の配信上限が超えました。 | Hết hạn mức tin/tháng của gói | Chờ kỳ sau hoặc nâng gói |
| L995 | 403 | quota_exceeded | LINEプランの配信上限に達しました。 | Hết hạn mức tin của gói LINE Official Account | Chờ kỳ sau hoặc nâng gói LINE OA |
| L996 | 422 | validation_error | Bot plan expired (over 7 days). Sending is disabled. | Gói LME của bot đã hết hạn quá 7 ngày | Gia hạn gói trên LME |
| L997 | 422 | validation_error | ブロックしていますので送信できません。 | Friend đã chặn LINE OA (block_status = "blocked") hoặc LME đã chặn friend (block_status = "block") | Không retry. Với blocked: chờ friend bỏ chặn. Với block: bỏ chặn trên LME hoặc bằng /do_action block.unblock |
| L998 | 422 | validation_error | (nội dung do hệ thống gửi tin trả về) | Hệ thống gửi tin LME từ chối message | Đọc error.message, sửa nội dung |
| L999 | 400/409 | invalid_request / conflict / in_progress | — | Lỗi Idempotency-Key | 2.9 |

## `POST /messages/template` — Gửi template message (L1059)

### [input] Request body (L1073)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1076 | friend_id | integer \| string | Bắt buộc | Như /messages/push. | 400 |
| L1077 | id_type | string | Tuỳ chọn | lmessage_friend_id \| line_friend_id. | lmessage_friend_id |
| L1078 | templates | array<TemplateItem> | Bắt buộc | 1–5 phần tử, gửi theo thứ tự. | 400 |
| L1079 | mark_confirmed | boolean | Tuỳ chọn | Như /messages/push. | false |

### [field] Object TemplateItem (L1082)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1085 | template_id | integer | Bắt buộc | Template ID từ /templates. | 400 |
| L1086 | edited_content | string | Tuỳ chọn | Nội dung text thay thế cho lần gửi này (token được thay như Text message; chuỗi rỗng = không thay thế). Tối đa 5.000 ký tự (giới hạn text của LINE). API chưa kiểm tra độ dài field này: vượt 5.000 ký tự thì request vẫn trả 200 nhưng LINE từ chối lúc gửi — message không tới friend và không xuất hiện ở /conversations/detail. Chỉ dùng với template loại text; template loại khác → 422 và không message n… | Gửi nội dung gốc của template |

### [error] Lỗi riêng (L1091)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1092 | 400 / 422 / 404 | — | friend_id is required. … | Lỗi friend (giống /messages/push) | — |
| L1093 | 400 | invalid_request | templates is required. | Thiếu templates | Thêm mảng |
| L1094 | 422 | validation_error | templates must be a non-empty array. | Mảng rỗng | ≥ 1 phần tử |
| L1095 | 422 | validation_error | templates exceeds max 5 per request. | > 5 phần tử | Tách request |
| L1096 | 400 | invalid_request | templates[0].template_id is required. | Thiếu template_id | Thêm ID |
| L1097 | 404 | not_found | templates[0] template_id not found: 7001 | Template không tồn tại, đã xoá (vào thùng rác), nằm trong thư mục ẩn, hoặc thuộc bot khác | Làm mới /templates |
| L1098 | 422 | validation_error | templates[0] edited_content is only allowed for text templates, template 7001 has type: … | Dùng edited_content với template không phải text | Bỏ edited_content |
| L1099 | 403 | quota_exceeded | 月1000通の配信上限が超えました。 | Hết hạn mức gửi tin | Chờ kỳ sau / nâng gói |
| L1100 | 403 | quota_exceeded | LINEプランの配信上限に達しました。 | Hết hạn mức tin của gói LINE Official Account | Chờ kỳ sau / nâng gói LINE OA |
| L1101 | 422 | validation_error | Bot plan expired (over 7 days). Sending is disabled. | Gói LME của bot đã hết hạn quá 7 ngày | Gia hạn gói trên LME |
| L1102 | 422 | validation_error | ブロックしていますので送信できません。 | Friend đã chặn LINE OA hoặc LME đã chặn friend (như /messages/push) | Không retry |
| L1103 | 422 | validation_error | templates[0] template 7001 has no sendable message. | Template nhóm không chứa template con nào gửi được. Template đơn rỗng không bị chặn ở bước này: request vẫn 200 nhưng gửi lỗi sau đó | Kiểm tra template trên LME |
| L1104 | 422 | validation_error | (nội dung do hệ thống gửi tin trả về) | Hệ thống gửi tin từ chối | Đọc error.message |

## `GET /templates` — Lấy danh sách template (L1145)

### [input] Query parameter (L1151)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1152 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L1153 | limit | integer | Tuỳ chọn | 1–500. | 100 |

### [output] Response (L1156)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1159 | data.templates[] | array<TemplateSummary> | — | Danh sách template. Mảng rỗng nếu không có. |
| L1160 | data.warnings | array<string> | — | Chỉ khi limit > 500. |
| L1161 | pagination | Pagination | — | Khối phân trang (2.8). |

### [field] Object TemplateSummary (L1164)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1167 | template_id | integer | — | Template ID. |
| L1168 | name | string | — | Tên template. |

## `GET /conversations` — Lấy danh sách conversation (L1200)

### [input] Query parameter (L1206)
| L | Parameter | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1207 | page | integer | Tuỳ chọn | Trang, từ 1. | 1 |
| L1208 | limit | integer | Tuỳ chọn | 1–500. | 100 |
| L1209 | confirm_status | integer | Tuỳ chọn | 0 = đã đọc (確認済み), 1 = chưa đọc (未確認 — đang chờ trả lời). | Cả hai |
| L1210 | handling_status_ids | integer, CSV | Tuỳ chọn | Status ID từ /handling-statuses. Nhiều giá trị → OR. | Không lọc |
| L1211 | handling_status_names | string, CSV | Tuỳ chọn | Tên trạng thái xử lý, khớp chính xác, không phân biệt hoa/thường. Gộp OR với handling_status_ids. | Không lọc |
| L1212 | line_names | string, CSV | Tuỳ chọn | Tìm gần đúng theo tên LINE hoặc tên quản lý, không phân biệt hoa/thường. Nhiều tên → OR. | Không lọc |
| L1213 | tag_ids | integer, CSV | Tuỳ chọn | Tag ID của friend. Gộp với tag_names. | Không lọc |
| L1214 | tag_names | string, CSV | Tuỳ chọn | Tên tag, khớp chính xác, không phân biệt hoa/thường. | Không lọc |
| L1215 | tag_mode | string | Tuỳ chọn | or = có ít nhất 1 tag; and = có đủ tất cả tag. Chỉ có tác dụng khi có tag_ids/tag_names. | or |
| L1216 | display_status | string | Tuỳ chọn | display = đang hiển thị, hidden = đã ẩn, all = cả hai. | display |

### [output] Response (L1220)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1223 | data.conversations[] | array<Conversation> | — | Danh sách conversation của trang hiện tại. Mảng rỗng nếu không có. |
| L1224 | data.warnings | array<string> | — | Chỉ khi limit > 500. |
| L1225 | pagination | Pagination | — | Khối phân trang (2.8). |

### [field] Object Conversation (L1228)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1231 | lmessage_friend_id | integer | — | Dùng cho /conversations/detail, /friends/detail, /do_action. |
| L1232 | line_friend_id | string | Có | LINE user ID. |
| L1233 | line_name | string | — | Tên LINE; "" nếu không có. |
| L1234 | system_name | string | Có | Tên quản lý trong LME. |
| L1235 | last_message | string | Có | Nội dung tóm tắt của tin nhắn cuối. |
| L1236 | last_message_date | datetime | Có | Thời điểm tin nhắn cuối, +09:00. |
| L1237 | confirm_status | string | — | read (確認済み) \| unread (未確認). |
| L1238 | handling_status | HandlingStatus | Có | Trạng thái xử lý {id, name}; null nếu chưa gắn. |

### [error] Lỗi riêng (L1241)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1242 | 400 | invalid_request | Parameter 'limit' has an invalid format (expected a numeric value). | page/limit sai | 2.8 |
| L1243 | 422 | validation_error | confirm_status must be 0 (read) or 1 (unread), got: 2 | Giá trị khác 0/1 | Dùng 0 hoặc 1 |
| L1244 | 422 | validation_error | handling_status_ids must contain positive integer IDs (comma-separated), got: x | ID không phải số nguyên dương (tương tự tag_ids) | Sửa giá trị |
| L1245 | 404 | not_found | handling_status_ids not found: [99]. Use GET /v1/handling-statuses to list available statuses. | Status không tồn tại / thuộc bot khác | Làm mới danh sách |
| L1246 | 404 | not_found | handling_status_names not found: [フォローアップ]. … | Tên không khớp chính xác | Kiểm tra chính tả |
| L1247 | 404 | not_found | tag_ids not found: [999]. … / tag_names not found: [VIPP]. … | Tag không tồn tại | Làm mới /tags |
| L1248 | 422 | validation_error | tag_mode must be or\|and, got: xor | Giá trị lạ | or / and |
| L1249 | 422 | validation_error | display_status must be display\|hidden\|all, got: show | Giá trị lạ | Dùng 1 trong 3 giá trị |

## `GET /conversations/detail` — Lấy message gần nhất của friend (L1330)

### [other] Giới hạn (L1335)
| L | Hạng mục | Giới hạn |
|---|---|---|
| L1336 | Số message | Tối đa 100 message gần nhất. Không lấy được message cũ hơn qua API này. |
| L1337 | Thứ tự | Mới nhất trước (messages[0] là message mới nhất). |
| L1338 | Phạm vi lịch sử | Bot gói free: 180 ngày gần nhất. Bot trả phí: 365 ngày gần nhất. |
| L1339 | Message lỗi | Message gửi thất bại (trạng thái ERROR) không được trả về — khớp với màn hình chat của LME. |

### [input] Query parameter (L1343)
| L | Parameter | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1344 | lmessage_friend_id | integer | Bắt buộc | Friend cần lấy hội thoại. |

### [output] Response (L1347)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1350 | data.lmessage_friend_id | integer | — | Friend đã truy vấn. |
| L1351 | data.messages[] | array<ConversationMessage> | — | 0–100 message, mới nhất trước. |
| L1352 | data.handling_status | HandlingStatus | Có | Trạng thái xử lý hiện tại {id, name}. |
| L1353 | data.display_status | string | — | display \| hidden. |
| L1354 | data.block_status | string | — | normal \| blocked (friend đã chặn LINE OA) \| block (LME đã chặn friend). |
| L1355 | data.favorite | string | — | yes \| no. |

### [field] Object ConversationMessage (L1358)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1361 | delivery_date | datetime | — | Thời điểm gửi/nhận, +09:00. |
| L1362 | sender | string | — | friend (friend gửi) \| LINE_OA (bot/nhân viên gửi, kể cả gửi tự động). |
| L1363 | message_type | string | — | Loại message — xem 7.4. |
| L1364 | data | MessageData | Có | Nội dung đã chuẩn hoá theo message_type: text, image, video, audio, file, action_from_booking → string; template, broadcast, event, action, scenario → mảng (scenario có thể là string khi không còn dữ liệu template); pdf, sticker, location, stop_scenario, scenario_empty_step, start_remind, stop_remind, action_from_booking_salon/lesson → object; dòng log hệ thống có thể là null. Ví dụ đầy đủ từng lo… |

### [error] Lỗi riêng (L1367)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1368 | 400 | invalid_request | Missing required parameter 'lmessage_friend_id'. | Thiếu param | Thêm param |
| L1369 | 400 | invalid_request | Parameter 'lmessage_friend_id' has an invalid format (expected a numeric value). | Không phải số | Dùng ID số |
| L1370 | 404 | not_found | Conversation not found | Friend chưa có hội thoại hoặc thuộc bot khác | Kiểm tra ID |

### [other] Ví dụ data theo từng message_type (L1489)
| L | message_type | Phát sinh khi | sender | Ví dụ data |
|---|---|---|---|---|
| L1490 | text | Friend hoặc nhân viên nhắn văn bản; message gửi qua /messages/push (type text); template gửi kèm edited_content; thông báo trả lời form; dòng log hệ thống | friend / LINE_OA | "注文した商品の配送状況を教えてください" |
| L1491 | image | Friend gửi ảnh; nhân viên/API gửi ảnh | friend / LINE_OA | "https://p.lmes.jp/msg_template/line-user/media-step/2001/image/image_10001_100000000000000001_1794390000001.jpeg" |
| L1492 | video | Friend/nhân viên/API gửi video | friend / LINE_OA | "https://p.lmes.jp/msg_template/line-user/media-step/2001/video/video_10004_100000000000000004_1794390000004.mp4" |
| L1493 | audio | Friend/nhân viên/API gửi audio. URL có thể kèm ?duration=<ms> | friend / LINE_OA | "https://p.lmes.jp/msg_template/media/voices/1001/2001/sample_voice02.m4a?duration=728086" |
| L1494 | file | Friend gửi file | friend | "https://p.lmes.jp/msg_template/line-user/media-step/2001/file/file_10002_100000000000000002_1794390000002.pdf" |
| L1495 | pdf | Nhân viên gửi PDF từ màn hình chat | LINE_OA | { "file_name": "sample_guide.pdf", "file_size": 401609, "url": "https://p.lmes.jp/msg_template/media/pdf/1001/2001/sample_guide.pdf", "file_name_original": "ご案内資料.pdf" } |
| L1501 | sticker | Friend/nhân viên gửi sticker. ID là string | friend / LINE_OA | { "packageId": "11538", "stickerId": "51626506" } |
| L1502 | location | Friend gửi vị trí. latitude/longitude có thể là string hoặc null; title có thể null | friend | { "address": "東京都千代田区丸の内1丁目9-1", "latitude": "35.681236", "title": null, "longitude": null } |
| L1508 | template | Gửi template từ chat, auto reply, rich menu, /messages/template… Mảng các phần tử của template (xem bảng con bên dưới) | LINE_OA | [ { "type": "text", "content": "ご予約ありがとうございます。" }, { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample01/sample01.png" } ] |
| L1512 | broadcast | Message broadcast (一斉配信) | LINE_OA | [ { "type": "text", "content": "【11月限定】会員様限定セールのお知らせ" } ] |
| L1513 | scenario — message | Một step của scenario được gửi. Nếu không còn dữ liệu template của step (ví dụ template đã bị xoá), data có thể là string thay vì mảng | LINE_OA | [ { "type": "text", "content": "ご登録ありがとうございます！" } ] |
| L1514 | scenario — ghi nhận bắt đầu | Friend được cho vào scenario (ghi nhận, không phải message gửi đi). start_day là string hoặc number; start_time dạng "0:00" hoặc "00:00:00"; cả hai có thể null | LINE_OA | [ { "scenario_name": "新規登録フォロー", "start_day": "0", "start_time": "0:00" } ] |
| L1515 | stop_scenario | Scenario của friend bị dừng | LINE_OA | { "scenario_name": "新規登録フォロー" } hoặc{ "scenario_name": "新規登録フォロー", "start_day": null, "start_time": null } |
| L1516 | scenario_empty_step | Scenario chạy tới step không có nội dung. Các field có thể đều null | LINE_OA | { "scenario_name": null, "start_day": null, "start_time": null } |
| L1517 | event | Message của sự kiện / nhắc lịch (リマインダ) | LINE_OA | [ { "type": "text", "content": "明日10:00からセミナーを開催します。" } ] |
| L1518 | start_remind | Friend được đăng ký nhắc lịch. startDateTime dạng YYYY-MM-DD HH:mm (giờ Nhật), có thể null | LINE_OA | { "remind_name": "セミナー前日リマインド", "startDateTime": "2026-11-10 18:28" } |
| L1519 | stop_remind | Huỷ nhắc lịch của friend | LINE_OA | { "remind_name": "セミナー前日リマインド", "startDateTime": null } |
| L1520 | action | Message gửi bởi action (アクション) — ví dụ khi bấm rich menu, nút, trả lời form | LINE_OA | [ { "type": "buttons", "content": { "data": [ { "title": "キャンペーン", "text": "参加はこちら", "buttons": [ { "label": "参加する" } ] } ] } }, { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample02/sample02.jpg" } ] |
| L1524 | action_from_booking | Thông báo tự động từ đặt lịch / thanh toán. data là string | LINE_OA | "決済に失敗しました。\nカードのご利用枠や有効期限などをご確認いただき\n再度、購入手続きを行なってください。" |
| L1525 | action_from_booking_salon | Thông báo tự động của đặt lịch salon. type = loại thông báo (予約受付時アクション, 予約キャンセル時アクション, 予約前後のリマインドメッセージ…) | LINE_OA | { "type": "予約受付時アクション", "calendar_name": "渋谷店", "content": "田中様\n\n下記の通り、予約が完了いたしました。\n\n◇ 予約日時\n2026年11月17日（火）10:00-11:00\n\n◇ ご予約コース名\nカット\n\n◇ コース料金\n1,600円" } |
| L1530 | action_from_booking_lesson | Thông báo tự động của đặt lịch lesson. Cấu trúc giống salon | LINE_OA | { "type": "予約キャンセル時アクション", "calendar_name": "ヨガ教室", "content": "田中様\n\n下記の通り、キャンセルが完了いたしました。\n\n◇ 予約日時\n2026年11月24日（火）13:00-14:00" } |
| L1535 | unknown | Loại chưa được phân loại (hiện gồm: message gửi bởi action khi friend trả lời form). data giữ nguyên dữ liệu gốc, có thể null | LINE_OA | null |

### [other] Phần tử con của template / broadcast / scenario / event / action (L1540)
| L | type | Dạng content | Ví dụ |
|---|---|---|---|
| L1541 | text | string — nội dung template đã lưu. Token (ví dụ {name}) có thể còn ở dạng token, không phải giá trị friend thực nhận | { "type": "text", "content": "田中様、ご来店ありがとうございました。" } |
| L1542 | image | URL string (gồm cả imagemap) | { "type": "image", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample01/sample01.png" } |
| L1543 | video | URL string | { "type": "video", "content": "https://p.lmes.jp/msg_template/media/images/1001/2001/sample_video.mp4" } |
| L1544 | audio | object {file_name, file_size, url}. file_size có thể là -1 hoặc null khi không xác định | { "type": "audio", "content": { "file_name": "sample_voice01.m4a", "file_size": 4708093, "url": "https://p.lmes.jp/msg_template/media/voices/1001/2001/sample_voice01.m4a?duration=290816" } } |
| L1548 | sticker | object {packageId, stickerId} (string) | { "type": "sticker", "content": { "packageId": "8515", "stickerId": "16581243" } } |
| L1549 | location | object {address, latitude, longitude, title} — trong template toạ độ là number | { "type": "location", "content": { "address": "東京都千代田区丸の内1丁目", "latitude": 35.6812, "longitude": 139.7671, "title": "東京駅" } } |
| L1551 | buttons — panel | object {data: [{title, text, buttons: [{label}]}]}; mỗi phần tử data là 1 panel (carousel có nhiều panel) | { "type": "buttons", "content": { "data": [ { "title": "", "text": "コースA", "buttons": [ { "label": "予約する" }, { "label": "詳細" } ] }, { "title": "", "text": "コースB", "buttons": [ { "label": "予約する" } ] } ] } } |
| L1554 | buttons — quick reply | object {flag_type_content_quick_reply, text, content, buttons: [{label}]}. flag_type_content_quick_reply: 1 = nội dung là văn bản, 2 = nội dung là ảnh (text/content là URL ảnh) | { "type": "buttons", "content": { "flag_type_content_quick_reply": 1, "text": "ご希望の時間帯を選んでください", "content": "ご希望の時間帯を選んでください", "buttons": [ { "label": "午前" }, { "label": "午後" } ] } } |
| L1559 | introduction | object {friend_name, template_id, url_addfriend, content} (giới thiệu tài khoản) | { "type": "introduction", "content": { "friend_name": "LMEサポート", "template_id": 34353, "url_addfriend": "https://line.me/R/ti/p/@lme-support", "content": "こちらもご登録ください" } } |

### [other] Message gửi qua API sẽ hiển thị lại thế nào (L1565)
| L | Request đã gửi | message_type khi đọc lại | data |
|---|---|---|---|
| L1566 | /messages/push — type: text | text | Nguyên văn text trong request — token chưa được thay (ví dụ vẫn là {name}様) |
| L1567 | /messages/push — type: image / video | image / video | Nguyên văn url đã gửi |
| L1568 | /messages/push — type: audio | audio | URL string (url đã gửi) |
| L1569 | /messages/template — không có edited_content | template | Mảng phần tử của template |
| L1570 | /messages/template — có edited_content | text | Nội dung edited_content (token chưa được thay) |

### [other] Lưu ý khi xử lý data (L1577)
| L | data | Sự kiện |
|---|---|---|
| L1578 | null | Các dòng log còn lại (ví dụ kết bạn, friend chặn / bỏ chặn LINE OA, xoá message) |
| L1579 | "ブロックしました" | LME chặn friend |
| L1580 | "ブロックを解除しました" | LME bỏ chặn friend |
| L1581 | "非表示しました" | LME ẩn hội thoại |
| L1582 | "メッセージ受信により追加" | Friend được thêm vào LME khi nhắn tin tới LINE OA |

## `GET /handling-statuses` — Lấy danh sách trạng thái xử lý (L1596)

### [output] Response (L1602)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1605 | data[] | array<HandlingStatus> | — | Toàn bộ trạng thái (mảng phẳng, không có khối pagination). Mảng rỗng nếu bot chưa tạo trạng thái nào. |

### [field] Object HandlingStatus (L1608)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L1611 | id | integer | — | Status ID. |
| L1612 | name | string | — | Tên trạng thái. |

## `POST /do_action` — Thực hiện hàng loạt action trên friend (L1636)

### [input] Request body (L1662)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1663 | lmessage_friend_ids | array<integer> | Bắt buộc | 1–100 friend (đếm sau khi bỏ trùng). Giới hạn cứng: > 100 → 422. | 400 |
| L1664 | actions | array<Action> | Bắt buộc | 1–10 action. Giới hạn cứng: > 10 → 422. | 400 |

### [other] Bảng phân loại action (L1667)
| L | type | Mục đích | action | Field riêng |
|---|---|---|---|---|
| L1668 | tag | Gắn / gỡ tag | add remove | tag_ids |
| L1669 | friend_info | Cập nhật friend info | set clear today point_replace point_plus point_minus point_clear | field_id value option_id |
| L1670 | scenario | Chạy / dừng / chạy tiếp scenario | start stop resume | scenario_id start_from |
| L1671 | handling_status | Gắn / gỡ trạng thái xử lý | attach detach | handling_status_id |
| L1672 | block | Chặn / bỏ chặn / ẩn / hiện trong chat 1:1 | block unblock hide show | — |
| L1673 | favorite | Bật / tắt favorite | add remove | — |
| L1674 | confirm_status | Đã đọc / chưa đọc (確認/未確認) | confirm unconfirm | — |

### [error] Lỗi riêng (cấp request) (L1679)
| L | HTTP | code | message (ví dụ) | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L1680 | 400 | invalid_request | lmessage_friend_ids is required. | Thiếu field | Thêm mảng |
| L1681 | 422 | validation_error | lmessage_friend_ids must be a non-empty array. | Mảng rỗng | ≥ 1 friend |
| L1682 | 422 | validation_error | lmessage_friend_ids exceeds max 100 per request. | > 100 friend | Chia lô 100 |
| L1683 | 404 | not_found | lmessage_friend_ids not found: [99901, 99902] | Không friend nào thuộc bot | Kiểm tra ID / API key |
| L1684 | 400 | invalid_request | actions is required. | Thiếu field | Thêm mảng |
| L1685 | 422 | validation_error | actions must be a non-empty array. | Mảng rỗng | ≥ 1 action |
| L1686 | 422 | validation_error | actions exceeds max 10 per request. | > 10 action | Tách request |
| L1687 | 400 | invalid_request | actions[0].type is required. | Thiếu type / phần tử null | Thêm type |
| L1688 | 422 | validation_error | actions[0] unknown type 'tags'. Valid: tag\|friend_info\|scenario\|handling_status\|block\|favorite\|confirm_status. | Sai type | Dùng giá trị hợp lệ |
| L1689 | 422 | validation_error | actions[0] invalid action for type 'tag'. Allowed: add\|remove. | Thiếu hoặc sai action | Xem bảng phân loại |
| L1690 | 404 / 422 | — | actions[i] … | Lỗi riêng từng loại action | mục 6 |

## Bảng ngoài endpoint (quy ước chung · object · bảng giá trị · changelog)

#### › 2. Quy ước chung › 2.1 Base URL & version
### [other] 2.1 Base URL & version (L226)
| L | Môi trường | Base URL |
|---|---|---|
| L229 | Production | https://api.lmes.jp/v1 |
| L230 | Staging | https://api-stg.lmes.jp/v1 |

#### › 2. Quy ước chung › 2.2 Xác thực
### [other] Quyền (scope) của key (L242)
| L | Scope | Được gọi | Gọi endpoint ghi (POST) |
|---|---|---|---|
| L245 | full | Mọi endpoint (GET + POST) | Cho phép |
| L246 | read | Chỉ GET | 403 forbidden "API key is read-only" |

### [other] Vòng đời key (L249)
| L | Trạng thái key | Kết quả khi gọi API | Cách xử lý |
|---|---|---|---|
| L252 | Đang hoạt động, còn hạn | 2xx | — |
| L253 | Hết hạn (kể cả khi LME đã chuyển key sang 無効) | 401 "API key expired" | Phát hành key mới. LME không có chức năng gia hạn hay kích hoạt lại key. |
| L254 | Đã xoá | 401 "API key has been deleted" | Phát hành key mới. |
| L255 | Bot của key đã bị xoá | 403 "Bot not found or not accessible" | Liên hệ quản trị viên bot. |

#### › 2. Quy ước chung › 2.3 Định dạng request
### [other] 2.3 Định dạng request (L260)
| L | Hạng mục | Quy ước |
|---|---|---|
| L263 | JSON lỗi cú pháp / sai kiểu field | 400 invalid_request "Request body is invalid (malformed JSON or wrong field type)." — ví dụ "tag_ids": "101" thay vì mảng số. |
| L264 | Field lạ trong body | Bị bỏ qua, không báo lỗi. Kiểm tra kỹ chính tả tên field — gõ sai tên field bắt buộc sẽ nhận lỗi "… is required". |
| L265 | Ngày | YYYY-MM-DD (ISO 8601, ví dụ 2026-11-16). Ngày không tồn tại (ví dụ 2026-02-30) bị từ chối như sai định dạng (422). |
| L266 | Ngày giờ (response) | YYYY-MM-DDTHH:mm:ss+09:00 — luôn theo giờ Nhật (JST, UTC+9). |
| L267 | Múi giờ | Mọi filter ngày (ví dụ added_date_from) được hiểu theo giờ Nhật. |

#### › 2. Quy ước chung › 2.4 Định dạng response
### [field] Lỗi (L291)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L294 | success | boolean | — | true khi HTTP 2xx, false khi lỗi. |
| L295 | request_id | string | — | ID duy nhất của request, dạng req_YYYYMMDD_xxxxxxxx. Trùng với header X-Request-Id, trừ response replay của idempotency (xem 2.9). Ghi log giá trị này và gửi kèm khi liên hệ hỗ trợ. |
| L296 | data | object \| array | — | Dữ liệu trả về; cấu trúc theo từng endpoint ở mục 4. Các POST không trả data (field vắng mặt). |
| L297 | pagination | Pagination | — | Chỉ có ở endpoint phân trang dạng chuẩn (xem 2.8). Vắng mặt ở endpoint khác. |
| L298 | error.code | string | — | Mã lỗi máy đọc được — dùng giá trị này để rẽ nhánh xử lý. |
| L299 | error.message | string | — | Mô tả cho người đọc (tiếng Anh, riêng lỗi từ hệ thống gửi tin có thể là tiếng Nhật). Nội dung có thể thay đổi — không so khớp chuỗi message trong code. |

#### › 2. Quy ước chung › 2.5 Response header
### [other] 2.5 Response header (L303)
| L | Header | Có ở | Mô tả |
|---|---|---|---|
| L306 | X-Request-Id | Mọi response | ID của lần gọi này. Thường giống request_id trong body. Ngoại lệ: response replay của idempotency (có Idempotency-Replayed: true) — body là bản lưu từ lần gọi đầu nên mang request_id cũ, còn header mang ID mới của lần gọi lại. Khi liên hệ hỗ trợ, gửi cả hai. |
| L307 | X-RateLimit-Limit | Mọi response /v1 (kể cả 401/403) | Hạn mức/phút của nhóm request hiện tại: 300 (GET) hoặc 60 (POST). |
| L308 | X-RateLimit-Remaining | Mọi response /v1 | Số request còn lại trong phút hiện tại. Với response lỗi xác thực (chưa xác định được bot) giá trị bằng X-RateLimit-Limit. |
| L309 | X-RateLimit-Reset | Mọi response /v1 | Thời điểm cửa sổ reset, Unix epoch (giây, UTC). Ví dụ 1763280060. |
| L310 | Retry-After | Chỉ 429 | Số giây cần chờ trước khi gọi lại (≥ 1). |
| L311 | Idempotency-Replayed | POST trả lại kết quả đã lưu | true khi response là bản lưu từ lần gọi trước cùng Idempotency-Key — request không được thực thi lại. |

#### › 2. Quy ước chung › 2.6 Status code & mã lỗi
### [error] 2.6 Status code & mã lỗi (L315)
| L | HTTP | error.code | Ý nghĩa | Retry? | Ví dụ nguyên nhân |
|---|---|---|---|---|---|
| L318 | 200 | — | Thành công | — | — |
| L319 | 400 | invalid_request | Request sai định dạng | Không — sửa request | JSON lỗi, thiếu field/param bắt buộc, sai kiểu số, Content-Type sai, limit ≤ 0, Idempotency-Key > 100 ký tự |
| L320 | 401 | unauthorized | Xác thực thất bại | Không | Thiếu/sai key, key hết hạn, key đã xoá |
| L321 | 403 | forbidden | Không có quyền | Không | Key read gọi POST, bot đã xoá |
| L322 | 403 | quota_exceeded | Hết hạn mức gửi tin của gói dịch vụ | Không (đến kỳ sau hoặc nâng gói) | Gói free vượt 1.000 tin/tháng: "月1000通の配信上限が超えました。"; hết hạn mức tin của gói LINE Official Account: "LINEプランの配信上限に達しました。" |
| L323 | 404 | not_found | Không tìm thấy | Không | Friend/tag/scenario/template/field/option/trạng thái xử lý không tồn tại, đã xoá, hoặc thuộc bot khác; endpoint/version không tồn tại |
| L324 | 409 | conflict | Xung đột idempotency | Không — dùng key mới | Idempotency-Key đã dùng cho request có body/path khác |
| L325 | 409 | in_progress | Request cùng key đang xử lý | Có — chờ vài giây | Gửi lại cùng Idempotency-Key khi lần đầu chưa xong |
| L326 | 422 | validation_error | Đúng định dạng nhưng giá trị không hợp lệ | Không — sửa giá trị | Vượt giới hạn số lượng/độ dài, sai enum, action không hợp với field type, URL media không truy cập được, friend đã chặn LINE OA hoặc bị LME chặn, hệ thống gửi tin LME từ chối |
| L327 | 429 | rate_limited | Vượt rate limit | Có — sau Retry-After giây | > 300 GET/phút hoặc > 60 POST/phút của bot |
| L328 | 500 | server_error | Lỗi phía server | GET: có — backoff. POST: cẩn thận — request có thể đã được thực thi (xem 2.9) | "Internal server error" |

### [error] Lỗi chung — áp dụng cho mọi endpoint (L332)
| L | HTTP | code | message | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|---|
| L335 | 401 | unauthorized | Missing X-LME-API-KEY header | Không gửi header hoặc header rỗng | Thêm header X-LME-API-KEY |
| L336 | 401 | unauthorized | Invalid API key | Key gõ sai, thừa ký tự, hoặc key của môi trường khác | Kiểm tra key và Base URL |
| L337 | 401 | unauthorized | API key has been deleted | Key đã bị xoá | Phát hành key mới |
| L338 | 401 | unauthorized | API key expired | Quá expires_at | Phát hành key mới |
| L339 | 403 | forbidden | API key is no longer active | Trạng thái key không hợp lệ. Không phát sinh khi dùng bình thường — key hết hạn trả 401 "API key expired" | Phát hành key mới |
| L340 | 403 | forbidden | API key is read-only | Key read gọi POST | Dùng key full |
| L341 | 403 | forbidden | Bot not found or not accessible | Bot gắn với key đã bị xoá | Liên hệ quản trị viên bot |
| L342 | 400 | invalid_request | Content-Type must be application/json | POST thiếu/sai Content-Type | Gửi Content-Type: application/json |
| L343 | 400 | invalid_request | Request body is invalid (malformed JSON or wrong field type). | Body không phải JSON hợp lệ hoặc field sai kiểu | Kiểm tra JSON và kiểu từng field |
| L344 | 404 | not_found | Endpoint not found: {METHOD} {path} | Sai path hoặc sai method | Đối chiếu Danh sách API |
| L345 | 429 | rate_limited | Rate limit exceeded: 300 requests/minute (read) | Vượt hạn mức phút | Chờ Retry-After giây |
| L346 | 500 | server_error | Internal server error | Lỗi không lường trước phía LME | GET: retry với exponential backoff. POST: xem 2.9 trước khi retry. Nếu lặp lại, gửi request_id cho bộ phận hỗ trợ |

#### › 2. Quy ước chung › 2.7 Rate limit
### [other] 2.7 Rate limit (L350)
| L | Nhóm | Method | Hạn mức |
|---|---|---|---|
| L353 | Đọc | GET | 300 request / phút / bot |
| L354 | Ghi | POST | 60 request / phút / bot |

#### › 2. Quy ước chung › 2.8 Phân trang
### [field] 2.8 Phân trang (L367)
| L | Parameter | Type | Mặc định | Quy tắc |
|---|---|---|---|---|
| L370 | page | integer | 1 | Bắt đầu từ 1. Bỏ trống, 0 hoặc số âm → coi là 1. Trang vượt quá tổng số trang → mảng rỗng (vẫn 200). Không phải số → 400. |
| L371 | limit | integer | 100 | 1–500. 0 hoặc âm → 400 "limit must be a positive integer (1..500), got: 0". Lớn hơn 500 → tự kẹp về 500 và response có data.warnings: ["limit_clamped"]. Không phải số → 400. |

### [field] Khối pagination (object Pagination) (L375)
| L | Field | Type | Có thể null | Mô tả |
|---|---|---|---|---|
| L378 | page | integer | — | Trang đã trả về (sau khi chuẩn hoá). |
| L379 | limit | integer | — | Số record/trang đã áp dụng (sau khi kẹp). |
| L380 | total_items | integer | — | Tổng số record khớp điều kiện. |
| L381 | total_pages | integer | — | ceil(total_items / limit); 0 khi không có record. |
| L382 | has_next | boolean | — | true nếu còn trang sau. |

### [other] Khác biệt giữa các endpoint (L385)
| L | Endpoint | Cách trả phân trang |
|---|---|---|
| L388 | GET /tags, /friend-info-fields, /scenarios, /templates, /conversations | Khối pagination ở cấp gốc. |
| L389 | GET /friends | Không có khối pagination; dùng data.total_items và data.total_pages. Duyệt tới khi page ≥ data.total_pages. |
| L390 | GET /handling-statuses | Không phân trang — trả toàn bộ. |
| L391 | GET /conversations/detail | Không phân trang — cố định tối đa 100 message gần nhất. |

#### › 2. Quy ước chung › 2.9 Idempotency & retry
### [other] 2.9 Idempotency & retry (L397)
| L | Hạng mục | Quy tắc |
|---|---|---|
| L400 | Áp dụng | POST /messages/push, POST /messages/template, POST /do_action. GET bỏ qua header này. |
| L401 | Giá trị | Chuỗi do bạn tự sinh, tối đa 100 ký tự (vượt → 400 "Idempotency-Key must be at most 100 characters."). Khuyến nghị UUID v4 hoặc ID nghiệp vụ duy nhất (ví dụ order-8812-shipped). |
| L402 | Ký tự khuyến nghị | Khuyến nghị chỉ dùng chữ cái ASCII A–Z a–z, chữ số 0–9, dấu gạch ngang - và gạch dưới _. Server không chặn ký tự khác, nhưng tránh ký tự đặc biệt, dấu cách, ký tự có dấu hoặc tiếng Nhật — giá trị header HTTP không bảo đảm truyền đúng các ký tự này, nên lần retry có thể bị coi là key khác. |
| L403 | Khoảng trắng | Server cắt (trim) khoảng trắng ở hai đầu trước khi so khớp và đếm độ dài: " abc " và "abc" là cùng một key. Header rỗng hoặc chỉ có khoảng trắng được coi như không gửi. |
| L404 | Phạm vi | Duy nhất theo API key. Hai key khác nhau dùng cùng giá trị không ảnh hưởng nhau. |
| L405 | Thời gian lưu | Kết quả thành công được lưu ít nhất 24 giờ. Sau 24 giờ, bản lưu bị dọn định kỳ — thời điểm dọn không cố định, nên không dựa vào việc dùng lại cùng key sau 24 giờ (có thể nhận replay hoặc được thực thi như request mới). Mỗi thao tác nghiệp vụ nên dùng một key riêng. |
| L406 | "Cùng request" | So khớp method + path + body (byte-by-byte). Đổi thứ tự field hay khoảng trắng trong JSON cũng bị coi là request khác. |
| L407 | Không gửi header | Không có chống trùng — mỗi lần gọi đều được thực thi. |

### [other] Hành vi khi gửi lại cùng key (L410)
| L | Tình huống | Response |
|---|---|---|
| L413 | Lần đầu (key mới) | Thực thi bình thường. Chỉ response 2xx được lưu. |
| L414 | Lần đầu đã thành công, gửi lại đúng request | Trả lại nguyên response đã lưu + header Idempotency-Replayed: true. Không thực thi lại. Body giữ request_id của lần đầu; header X-Request-Id là ID mới của lần gọi lại. |
| L415 | Lần đầu đã thành công, gửi lại với body/path khác | 409 conflict "Idempotency-Key already used with a different request (method/path/body mismatch)." |
| L416 | Lần đầu đang xử lý | 409 in_progress "A request with this Idempotency-Key is still being processed." — chờ vài giây rồi gửi lại. Nếu lần đầu treo quá 60 giây, server giải phóng key và thực thi lại. |
| L417 | Lần đầu bị lỗi (4xx/5xx) | Không lưu — gửi lại cùng key sẽ được thực thi lại (sau khi bạn sửa request). Riêng lỗi 500 với POST: request có thể đã được thực thi một phần — với /messages/*, kiểm tra /conversations/detail trước khi gửi lại. |

#### › 3. Danh sách API
### [other] 3. Danh sách API (L425)
| L | Method | Path | Mục đích | Scope | Rate limit | Idempotency |
|---|---|---|---|---|---|---|
| L428 | GET | /v1/friends | Danh sách friend (lọc tên, tag, email, ngày kết bạn) | read / full | Đọc | — |
| L429 | GET | /v1/friends/detail | Chi tiết 1 friend (tag, friend info, scenario) | read / full | Đọc | — |
| L430 | GET | /v1/tags | Danh sách tag | read / full | Đọc | — |
| L431 | GET | /v1/friend-info-fields | Danh sách friend info field + option | read / full | Đọc | — |
| L432 | GET | /v1/scenarios | Danh sách scenario | read / full | Đọc | — |
| L433 | POST | /v1/messages/push | Gửi 1–5 message text/image/video/audio | full | Ghi | Có |
| L434 | POST | /v1/messages/template | Gửi 1–5 template có sẵn | full | Ghi | Có |
| L435 | GET | /v1/templates | Danh sách template | read / full | Đọc | — |
| L436 | GET | /v1/conversations | Danh sách conversation (lọc đã đọc, trạng thái xử lý, tag…) | read / full | Đọc | — |
| L437 | GET | /v1/conversations/detail | 100 message gần nhất của 1 friend + trạng thái | read / full | Đọc | — |
| L438 | GET | /v1/handling-statuses | Danh sách trạng thái xử lý | read / full | Đọc | — |
| L439 | POST | /v1/do_action | Chạy 1–10 action trên 1–100 friend | full | Ghi | Có |

#### › 5. Message object › Thuộc tính chung
### [field] Thuộc tính chung (L1779)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1780 | type | string | Bắt buộc | text \| image \| video \| audio. Không phân biệt hoa/thường. |

### [field] Kiểm tra URL media (image / video / audio) (L1785)
| L | Field | Request kiểm tra | Redirect |
|---|---|---|---|
| L1786 | url (image / video / audio) | HEAD. Nếu response HEAD không có Content-Length, server gửi thêm 1 GET để đếm dung lượng (dừng ngay khi vượt giới hạn) | Được theo |
| L1787 | preview_url (image / video) | GET (1 lần) | Không — 3xx là lỗi |

### [other] Kiểm tra URL media (image / video / audio) (L1790)
| L | Kiểm tra | message (ví dụ) |
|---|---|---|
| L1791 | URL bắt đầu bằng https:// hoặc http:// | messages[1] image requires a valid http(s) url. |
| L1792 | Độ dài ≤ 2.000 ký tự | messages[1] url exceeds 2000 chars. |
| L1793 | URL hợp lệ, có host | messages[1] media url is not a valid URL. / … has no host. |
| L1794 | Host phân giải được DNS | messages[1] media url host cannot be resolved: cdn.example.invalid |
| L1795 | Host là địa chỉ public (không phải localhost, IP nội bộ 10.x / 172.16–31.x / 192.168.x, link-local…) | messages[1] media url must be a public URL (internal address rejected). |
| L1796 | Kết nối được trong 5 giây | messages[1] media url is not reachable: … |
| L1797 | HTTP status < 400 (redirect được theo) | messages[1] media url returned HTTP 404. |
| L1798 | Content-Type thuộc danh sách cho phép (nếu server trả header này) | messages[1] unsupported media Content-Type 'image/gif' for type=image. Allowed: [image/jpeg, image/jpg, image/png]. |
| L1799 | Kích thước ≤ giới hạn (theo Content-Length; thiếu header thì đếm byte khi tải) | messages[1] image exceeds max size 10MB (Content-Length=12582912). |

#### › 5. Message object › Text message
### [field] Text message (L1805)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1806 | type | string | Bắt buộc | text |
| L1807 | text | string | Bắt buộc | Nội dung, 1–5.000 ký tự, không được chỉ toàn khoảng trắng. Đếm theo UTF-16 code unit — emoji và một số ký tự đặc biệt có thể tính 2 ký tự. Xuống dòng dùng \n. Token trong bảng dưới được thay bằng giá trị thật lúc gửi. |

### [other] Token trong text (L1811)
| L | Token | Thay bằng | Ví dụ kết quả |
|---|---|---|---|
| L1812 | {name} hoặc [name] | Tên LINE của friend | {name}様 → 田中太郎様 |
| L1813 | [FRIEND_INFO_system_name] [FRIEND_INFO_phone] [FRIEND_INFO_email] [FRIEND_INFO_birthday] [FRIEND_INFO_province] [FRIEND_INFO_zip_code] [FRIEND_INFO_district] [FRIEND_INFO_township] [FRIEND_INFO_building] | Giá trị built-in field tương ứng (-1, -2, -3, -4, -6, -7, -8, -9, -10) | [FRIEND_INFO_province] → 東京都 |
| L1814 | [FRIEND_INFO_<field_id>] | Giá trị custom field (field_id dương từ /friend-info-fields). Field IMAGE/FILE → URL xem file | [FRIEND_INFO_5001] → 20 |
| L1815 | [date] | Ngày gửi (giờ Nhật), dạng MM月DD日(曜) — tháng và ngày luôn 2 chữ số | 01月05日(月) |
| L1816 | [date add=N] | Ngày gửi + N ngày (N có thể âm), dạng như [date] | [date add=3] → 01月08日(木) |
| L1817 | [date_format=…] | Ngày gửi theo định dạng chỉ định. Chỉ nhận 7 định dạng: Y年n月j日(D) Y年n月j日 n月j日 n/j(D) Y/n/j(D) Y/n/j n/j (Y năm, n tháng 2 chữ số, j ngày 2 chữ số, D thứ). Định dạng khác giữ nguyên chuỗi | [date_format=Y/n/j] → 2026/01/05 |
| L1818 | [date add=N format=…] | Ngày gửi + N ngày theo 1 trong 7 định dạng trên | [date add=7 format=n/j] → 01/12 |
| L1819 | [remain to=YYYY-MM-DD] | Số ngày còn lại từ hôm nay tới ngày chỉ định (0 nếu ngày đó đã qua hoặc là hôm nay) | [remain to=2026-01-31] → 26 |

### [error] Token trong text (L1827)
| L | Lỗi (422) | Khi nào |
|---|---|---|
| L1828 | messages[0] text requires non-blank text. | Thiếu text, rỗng, hoặc chỉ khoảng trắng |
| L1829 | messages[0] text exceeds 5000 chars. | > 5.000 ký tự |
| L1830 | messages[0] preview_url is only allowed for image/video messages. | Text kèm preview_url |

#### › 5. Message object › Image message
### [field] Image message (L1835)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1836 | type | string | Bắt buộc | image | — |
| L1837 | url | string | Bắt buộc | URL ảnh gốc. JPEG/PNG (image/jpeg, image/jpg, image/png), tối đa 10 MB, ≤ 2.000 ký tự. | 422 |
| L1838 | preview_url | string | Tuỳ chọn | Ảnh thu nhỏ hiển thị trong khung chat. Ràng buộc chặt hơn url — xem bảng dưới. | Dùng url làm preview |

### [other] Ràng buộc preview_url (image & video) (L1841)
| L | Ràng buộc | Lỗi (422) khi vi phạm |
|---|---|---|
| L1842 | Bắt buộc https:// (không chấp nhận http) | messages[1] preview_url must be a valid https url. |
| L1843 | ≤ 2.000 ký tự | messages[1] preview_url exceeds 2000 chars. |
| L1844 | Host public, phân giải được | … preview_url must be a public URL (internal address rejected). / … host cannot be resolved |
| L1845 | Không redirect (trả 3xx là lỗi) và status < 300 | messages[1] preview_url returned HTTP 302 (redirects are not allowed for preview_url). |
| L1846 | JPEG/PNG. Nếu server không trả Content-Type, đuôi URL phải là .jpg/.jpeg/.png | messages[1] preview_url must be JPEG/PNG, got Content-Type 'image/webp'. |
| L1847 | Tối đa 1 MB | messages[1] preview_url exceeds max size 1MB (Content-Length=…). |
| L1848 | Chỉ dùng cho image/video | messages[3] preview_url is only allowed for image/video messages. |

#### › 5. Message object › Video message
### [field] Video message (L1857)
| L | Field | Type | Bắt buộc | Mô tả | Khi bỏ trống |
|---|---|---|---|---|---|
| L1858 | type | string | Bắt buộc | video | — |
| L1859 | url | string | Bắt buộc | URL video MP4 (video/mp4), tối đa 200 MB, ≤ 2.000 ký tự. | 422 |
| L1860 | preview_url | string | Khuyến nghị | Ảnh bìa video, JPEG/PNG ≤ 1 MB, HTTPS, không redirect (bảng ràng buộc ở Image). Luôn truyền field này để friend thấy đúng ảnh bìa. | Dùng ảnh bìa mặc định của LME (ảnh "no thumbnail") |

#### › 5. Message object › Audio message
### [field] Audio message (L1869)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1870 | type | string | Bắt buộc | audio |
| L1871 | url | string | Bắt buộc | URL file M4A/MP3 (audio/m4a, audio/x-m4a, audio/mp4, audio/aac, audio/mpeg, audio/mp3), tối đa 200 MB. |
| L1872 | duration | integer | Bắt buộc | Độ dài file tính bằng millisecond, số nguyên dương (ví dụ 60 giây = 60000). Hiển thị trên LINE — hãy truyền đúng độ dài thật. |

### [error] Audio message (L1874)
| L | Lỗi (422) | Khi nào |
|---|---|---|
| L1875 | messages[3] audio requires duration (milliseconds). | Thiếu duration |
| L1876 | messages[3] duration must be a positive integer (milliseconds). | duration ≤ 0 |
| L1877 | messages[3] preview_url is only allowed for image/video messages. | Audio kèm preview_url |

#### › 5. Message object › Tóm tắt giới hạn
### [other] Tóm tắt giới hạn (L1883)
| L | Hạng mục | Giới hạn |
|---|---|---|
| L1884 | Message / request | 1–5 |
| L1885 | Text | 1–5.000 ký tự (UTF-16) |
| L1886 | URL (url, preview_url) | ≤ 2.000 ký tự |
| L1887 | Image | JPEG/PNG ≤ 10 MB |
| L1888 | Preview | JPEG/PNG ≤ 1 MB, HTTPS, không redirect |
| L1889 | Video | MP4 ≤ 200 MB |
| L1890 | Audio | M4A/MP3 ≤ 200 MB, duration bắt buộc |
| L1891 | Timeout kiểm tra URL | 5 giây / lần truy cập |

#### › 6. Action object
### [field] 6. Action object (L1899)
| L | Field chung | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1900 | type | string | Bắt buộc | Loại action. Không phân biệt hoa/thường. |
| L1901 | action | string | Bắt buộc | Thao tác, giá trị hợp lệ theo type. Thiếu → 422 "invalid action for type …". |

#### › 6. Action object › tag — gắn / gỡ tag
### [field] tag — gắn / gỡ tag (L1905)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1906 | action | string | Bắt buộc | add (gắn) \| remove (gỡ). Gắn tag đã có / gỡ tag chưa gắn không gây lỗi. add có thể kích hoạt hành động gắn với tag — xem tác dụng phụ. |
| L1907 | tag_ids | array<integer> | Bắt buộc | Tag ID từ /tags, ≥ 1 phần tử. Tất cả phải tồn tại trong bot. |

### [error] tag — gắn / gỡ tag (L1909)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1910 | 422 | actions[0] tag requires non-empty tag_ids. | Thiếu hoặc rỗng tag_ids |
| L1911 | 404 | actions[0] tag_ids not found: [999] | Tag không tồn tại / đã xoá / bot khác |

#### › 6. Action object › friend_info — cập nhật friend info
### [field] friend_info — cập nhật friend info (L1916)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1917 | action | string | Bắt buộc | set clear today point_replace point_plus point_minus point_clear — xem ma trận bên dưới. |
| L1918 | field_id | integer | Bắt buộc | Field ID từ /friend-info-fields (âm = built-in, dương = custom). |
| L1919 | value | string | Có điều kiện | Giá trị mới, bắt buộc với set (trừ SELECT) và point_replace/plus/minus. Được trim khoảng trắng 2 đầu. |
| L1920 | option_id | integer | Có điều kiện | Bắt buộc với set trên field SELECT (không nhận value). Lấy từ options[]; field -6 dùng STT 1–47 (7.3). |

### [other] Ma trận action × kiểu field (L1923)
| L | action | TEXT | DATE | POINT | SELECT | IMAGE | FILE | Kết quả |
|---|---|---|---|---|---|---|---|---|
| L1924 | set | value bất kỳ | value = YYYY-MM-DD | value số nguyên | option_id | value = URL ảnh | value = URL file | Ghi đè giá trị |
| L1925 | clear | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Xoá giá trị |
| L1926 | today | — | ✓ | — | — | — | — | Ghi ngày hiện tại (giờ Nhật) |
| L1927 | point_replace | — | — | value số nguyên | — | — | — | Đặt điểm = value |
| L1928 | point_plus | — | — | value số nguyên | — | — | — | Cộng value |
| L1929 | point_minus | — | — | value số nguyên | — | — | — | Trừ value |
| L1930 | point_clear | — | — | ✓ | — | — | — | Xoá điểm |

### [error] Lỗi (L1936)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1937 | 422 | actions[1] friend_info requires field_id. | Thiếu field_id |
| L1938 | 404 | actions[1] friend_info field_id not found: 5009 | Field không tồn tại / bot khác / built-in không có trong 7.2 |
| L1939 | 422 | actions[1] friend_info set on SELECT field requires option_id (value is not accepted). | set SELECT thiếu option_id (kể cả khi đã gửi value) |
| L1940 | 404 | actions[1] option_id not found in field 5002: 9 | Option không thuộc field; field -6 ngoài 1–47 ("valid: 1..47") |
| L1941 | 422 | actions[1] friend_info set requires value. | set thiếu / rỗng value |
| L1942 | 422 | actions[1] DATE field value must be in format YYYY-MM-DD, got: 2026/11/16 | Sai định dạng ngày |
| L1943 | 422 | actions[1] POINT field value must be an integer, got: 1.5 | set POINT không phải số nguyên |
| L1944 | 422 | actions[1] friend_info today only applies to DATE fields, field 5001 is not a DATE field. | today trên field không phải DATE |
| L1945 | 422 | actions[1] friend_info point_plus only applies to POINT fields, field -3 is not a POINT field. | point_* trên field không phải POINT |
| L1946 | 422 | actions[1] friend_info point_plus requires value (number). | Thiếu value |
| L1947 | 422 | actions[1] friend_info point_plus value must be an integer, got: ten | value không phải số nguyên |
| L1948 | 422 | actions[1] invalid action for type 'friend_info'. Allowed: set\|clear\|today\|point_replace\|point_plus\|point_minus\|point_clear. | Sai action |

#### › 6. Action object › scenario — chạy / dừng / chạy tiếp
### [field] scenario — chạy / dừng / chạy tiếp (L1959)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1960 | action | string | Bắt buộc | start — chạy scenario từ đầu; resume — chạy từ ngày chỉ định; stop — dừng scenario. |
| L1961 | scenario_id | integer | Có điều kiện | Bắt buộc với start/resume (phải tồn tại, chưa xoá). Với stop: không cần — xem lưu ý bên dưới. |
| L1962 | start_from | integer | Có điều kiện | Bắt buộc với resume: ngày bắt đầu trong scenario, ≥ 0 (ví dụ 3 = chạy tiếp từ ngày thứ 3). Bị bỏ qua với start (luôn từ ngày 0). |

### [error] scenario — chạy / dừng / chạy tiếp (L1964)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1965 | 422 | actions[2] scenario start/resume requires scenario_id. | Thiếu scenario_id |
| L1966 | 404 | actions[2] scenario_id not found: 88 | Scenario không tồn tại / đã xoá / bot khác |
| L1967 | — | (không lỗi, response 200) | start_from lớn hơn ngày của step cuối: không step nào được gửi, scenario của friend chuyển sang completed; nếu scenario có cài scenario chạy tiếp sau khi kết thúc (終了後シナリオ) thì scenario đó được bắt đầu |
| L1968 | 422 | actions[2] scenario resume requires start_from (>=0). | resume thiếu hoặc âm start_from |
| L1969 | 422 | actions[2] invalid action for type 'scenario'. Allowed: start\|stop\|resume. | Sai action |

#### › 6. Action object › handling_status — trạng thái xử lý
### [field] handling_status — trạng thái xử lý (L1983)
| L | Field | Type | Bắt buộc | Mô tả |
|---|---|---|---|---|
| L1984 | action | string | Bắt buộc | attach — gắn trạng thái (thay trạng thái cũ); detach — gỡ trạng thái hiện tại. |
| L1985 | handling_status_id | integer | Có điều kiện | Bắt buộc với attach; bỏ qua với detach. Từ /handling-statuses. |

### [error] handling_status — trạng thái xử lý (L1987)
| L | HTTP | message | Khi nào |
|---|---|---|---|
| L1988 | 422 | actions[3] handling_status attach requires handling_status_id. | Thiếu ID |
| L1989 | 404 | actions[3] handling_status_id not found: 99 | Không tồn tại / bot khác |
| L1990 | 422 | actions[3] invalid action for type 'handling_status'. Allowed: attach\|detach. | Sai action |

#### › 6. Action object › block / favorite / confirm_status
### [other] block / favorite / confirm_status (L1997)
| L | type | action | Kết quả | Xem lại ở |
|---|---|---|---|---|
| L1998 | block | block | LME chặn friend (không nhận message từ friend trong chat 1:1) | block_status = "block" |
| L1999 | unblock | Bỏ chặn | block_status = "normal" |  |
| L2000 | hide | Ẩn conversation khỏi danh sách chat 1:1 | display_status = "hidden" |  |
| L2001 | show | Hiện lại conversation | display_status = "display" |  |
| L2002 | favorite | add | Đánh dấu favorite (lên đầu /conversations) | favorite = "yes" |
| L2003 | remove | Bỏ favorite | favorite = "no" |  |
| L2004 | confirm_status | confirm | Đánh dấu đã đọc (確認済み) | confirm_status = "read" |
| L2005 | unconfirm | Đánh dấu chưa đọc (未確認) | confirm_status = "unread" |  |

#### › 7. Bảng giá trị › 7.1 Kiểu friend info field
### [other] 7.1 Kiểu friend info field (L2018)
| L | field_type | Tên trên LME | Giá trị đọc ra (/friends/detail) | Cách ghi (/do_action) |
|---|---|---|---|---|
| L2019 | TEXT | 記述式 | string | set + value |
| L2020 | POINT | ポイント | number | point_* + value số nguyên |
| L2021 | DATE | 日付 | YYYY-MM-DD | set + value / today |
| L2022 | SELECT | 選択式 | nhãn option (string) | set + option_id |
| L2023 | IMAGE | 画像 | URL string | set + value URL |
| L2024 | FILE | ファイル | URL string | set + value URL |

#### › 7. Bảng giá trị › 7.2 Built-in field (ID âm)
### [other] 7.2 Built-in field (ID âm) (L2029)
| L | field_id | Tên (JP) | Ý nghĩa | field_type |
|---|---|---|---|---|
| L2030 | -1 | システム表示名 | Tên quản lý (= system_name) | TEXT |
| L2031 | -2 | 携帯電話 | Số điện thoại (= phone) | TEXT |
| L2032 | -3 | メールアドレス | Email (= email) | TEXT |
| L2033 | -4 | 生年月日 | Ngày sinh | DATE |
| L2034 | -6 | 都道府県名 | Tỉnh/thành (47 option cố định) | SELECT |
| L2035 | -7 | 郵便番号 | Mã bưu điện | TEXT |
| L2036 | -8 | 市区町村名 | Quận/huyện/thành phố | TEXT |
| L2037 | -9 | 町名/番地 | Địa chỉ/số nhà | TEXT |
| L2038 | -10 | 建物名・部屋番号 | Toà nhà/số phòng | TEXT |

#### › 7. Bảng giá trị › 7.3 Option của field -6 (都道府県名)
### [other] 7.3 Option của field -6 (都道府県名) (L2043)
| L | ID | Tỉnh | ID | Tỉnh | ID | Tỉnh | ID | Tỉnh |
|---|---|---|---|---|---|---|---|---|
| L2044 | 1 | 北海道 | 13 | 東京都 | 25 | 滋賀県 | 37 | 香川県 |
| L2045 | 2 | 青森県 | 14 | 神奈川県 | 26 | 京都府 | 38 | 愛媛県 |
| L2046 | 3 | 岩手県 | 15 | 新潟県 | 27 | 大阪府 | 39 | 高知県 |
| L2047 | 4 | 宮城県 | 16 | 富山県 | 28 | 兵庫県 | 40 | 福岡県 |
| L2048 | 5 | 秋田県 | 17 | 石川県 | 29 | 奈良県 | 41 | 佐賀県 |
| L2049 | 6 | 山形県 | 18 | 福井県 | 30 | 和歌山県 | 42 | 長崎県 |
| L2050 | 7 | 福島県 | 19 | 山梨県 | 31 | 鳥取県 | 43 | 熊本県 |
| L2051 | 8 | 茨城県 | 20 | 長野県 | 32 | 島根県 | 44 | 大分県 |
| L2052 | 9 | 栃木県 | 21 | 岐阜県 | 33 | 岡山県 | 45 | 宮崎県 |
| L2053 | 10 | 群馬県 | 22 | 静岡県 | 34 | 広島県 | 46 | 鹿児島県 |
| L2054 | 11 | 埼玉県 | 23 | 愛知県 | 35 | 山口県 | 47 | 沖縄県 |
| L2055 | 12 | 千葉県 | 24 | 三重県 | 36 | 徳島県 |  |  |

#### › 7. Bảng giá trị › 7.4 message_type và dạng data — MessageData (/conversations/detail)
### [other] 7.4 message_type và dạng data — MessageData (/conversations/detail) (L2059)
| L | message_type | Ý nghĩa | Dạng data |
|---|---|---|---|
| L2060 | text | Tin nhắn văn bản, thông báo trả lời form, dòng log hệ thống | string \| null |
| L2061 | image, video, audio | Media | string — URL (audio có thể kèm ?duration=) |
| L2062 | file | File friend gửi | string — URL |
| L2063 | pdf | PDF nhân viên gửi | object {file_name, file_size, url, file_name_original} |
| L2064 | sticker | Sticker | object {packageId, stickerId} (string) |
| L2065 | location | Vị trí | object {address, latitude, longitude, title} |
| L2066 | template, broadcast, event, action | Template / broadcast / nhắc lịch / action | array [{type, content}] |
| L2067 | scenario | Step của scenario hoặc ghi nhận bắt đầu scenario | array — phần tử là {type, content} hoặc {scenario_name, start_day, start_time}; có thể là string khi không còn dữ liệu template |
| L2068 | stop_scenario, scenario_empty_step | Dừng scenario / step rỗng | object {scenario_name, start_day?, start_time?} |
| L2069 | start_remind, stop_remind | Đăng ký / huỷ nhắc lịch | object {remind_name, startDateTime} |
| L2070 | action_from_booking | Thông báo đặt lịch / thanh toán | string |
| L2071 | action_from_booking_salon, action_from_booking_lesson | Thông báo đặt lịch salon / lesson | object {type, calendar_name, content} |
| L2072 | unknown | Loại chưa phân loại (hiện gồm action khi trả lời form) | nguyên trạng, thường null |

#### › 7. Bảng giá trị › 7.5 Trạng thái
### [field] 7.5 Trạng thái (L2077)
| L | Field | Giá trị | Ý nghĩa |
|---|---|---|---|
| L2078 | confirm_status | read / unread | Đã đọc (確認済み) / chưa đọc (未確認). Ở query của /conversations dùng số: 0 = read, 1 = unread. |
| L2079 | block_status | normal / blocked / block | Bình thường / friend đã chặn LINE OA / LME đã chặn friend. |
| L2080 | display_status | display / hidden | Hiển thị / đã ẩn trong chat 1:1. |
| L2081 | favorite | yes / no | Có / không favorite. |
| L2082 | scenarios[].status | following / completed / stopped | Đang nhận / đã nhận hết / đã dừng. |
| L2083 | sender | friend / LINE_OA | Friend gửi / bot hoặc nhân viên gửi. |
| L2084 | friendtype | old / new | 既存友だち (đã là friend trước khi LINE OA kết nối LME) / 新規友だち (kết bạn sau khi kết nối). Xem /friends. |

#### › 8. Lịch sử cập nhật
### [other] 8. Lịch sử cập nhật (L2092)
| L | Bản | Ngày | Nội dung thay đổi |
|---|---|---|---|
| L2095 | 1.3.0 | 16/11/2026 | Viết lại toàn bộ tài liệu theo dạng API reference, đối chiếu với hành vi thực tế của server. Không thay đổi API — chỉ bổ sung và sửa mô tả: ① Thêm ví dụ curl / Python / Node.js / Ruby cho cả 12 endpoint. ② Bổ sung bảng lỗi riêng cho từng endpoint (HTTP, code, message, nguyên nhân, cách xử lý) và thứ tự kiểm tra xác thực. ③ Ghi nhận 3 mã lỗi đã có nhưng chưa được mô tả: quota_exceeded (403), in_pro… |
| L2115 | 1.2.0 | 28/09/2026 | ① Bổ sung bảng built-in friend info field (ID âm) ở GET /friend-info-fields. ② Field -6 (都道府県名) là SELECT với 47 option cố định, option_id = STT 1–47; /do_action friend_info.set field -6 nhận option_id (ngoài 1..47 → 404; gửi value thay option_id → 422). |
| L2116 | 1.1.0 | 21/09/2026 | ① Resource thuộc bot khác trả 404. ② Đổi "compliant status" → "handling status" (/handling-statuses, data.handling_status). ③ GET /conversations (message gần nhất) đổi thành GET /conversations/detail; GET /conversations mới là danh sách conversation. ④ /do_action thêm confirm_status. ⑤ Bỏ tiền tố filters. ở query; /friends thêm line_names, đổi tag_id → tag_ids, email → emails. ⑥ Tách line_name / s… |
| L2117 | 1.0.0 | 10/09/2026 | Bản đầu tiên. |

## Tổng hợp

- 12 endpoint · 94 bảng · 137 dòng param/field (input + object) · 111 dòng lỗi

### Param kiểu ID theo endpoint (nguyên liệu ma trận bot A ↔ B — DOC-SEC)

| Endpoint | Param ID (L) |
|---|---|
| `GET /friends` | `tag_ids` (L463), `lmessage_friend_id` (L483), `line_friend_id` (L484) |
| `GET /friends/detail` | `lmessage_friend_id` (L595), `id` (L616), `id` (L623), `id` (L632) |
| `GET /tags` | `id` (L760) |
| `GET /friend-info-fields` | `field_id` (L824), `option_id` (L833) |
| `GET /scenarios` | `scenario_id` (L909) |
| `POST /messages/push` | `friend_id` (L963) |
| `POST /messages/template` | `friend_id` (L1076), `template_id` (L1085) |
| `GET /templates` | `template_id` (L1167) |
| `GET /conversations` | `handling_status_ids` (L1210), `tag_ids` (L1213), `lmessage_friend_id` (L1231), `line_friend_id` (L1232) |
| `GET /conversations/detail` | `lmessage_friend_id` (L1344) |
| `GET /handling-statuses` | `id` (L1611) |
| `POST /do_action` | `lmessage_friend_ids` (L1663) |

Param ID trong object (message / action):

- `tag_ids` (L1907, 6. Action object › tag — gắn / gỡ tag)
- `field_id` (L1918, 6. Action object › friend_info — cập nhật friend info)
- `option_id` (L1920, 6. Action object › friend_info — cập nhật friend info)
- `scenario_id` (L1961, 6. Action object › scenario — chạy / dừng / chạy tiếp)
- `handling_status_id` (L1985, 6. Action object › handling_status — trạng thái xử lý)
