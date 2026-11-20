# Diff cấu trúc docs Public API — bản 1.2.0 → 1.3.0

> Cũ: `spec-features/api-public/docs/api_v1_1104.html` · Mới: `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html` · L cũ / L mới = số dòng trong từng file HTML.
> **Heuristic** — khớp theo tên param/field và message lỗi. Mỗi dòng là ỨNG VIÊN: mở L hai bên để xác nhận trước khi ghi `DOC-VER`. Đổi câu chữ message lỗi sẽ hiện thành 1 dòng bớt + 1 dòng thêm.

## 1. Endpoint

| Trạng thái | Endpoint | L cũ | L mới |
|---|---|---|---|
| giữ | `GET /friends` | L197 | L488 |
| giữ | `GET /friends/detail` | L250 | L619 |
| giữ | `GET /tags` | L325 | L746 |
| giữ | `GET /friend-info-fields` | L363 | L802 |
| giữ | `GET /scenarios` | L506 | L874 |
| giữ | `POST /messages/push` | L550 | L928 |
| giữ | `POST /messages/template` | L600 | L1038 |
| giữ | `GET /templates` | L633 | L1117 |
| giữ | `GET /conversations` | L675 | L1164 |
| giữ | `GET /conversations/detail` | L734 | L1286 |
| giữ | `GET /handling-statuses` | L800 | L1545 |
| giữ | `POST /do_action` | L831 | L1578 |

## 2. Thay đổi theo endpoint

| Endpoint | Loại | Thay đổi | Key | Cũ | Mới |
|---|---|---|---|---|---|
| `GET /friends` | input | thêm | `X-LME-API-KEY` | — | L495 |
| `GET /friends` | output | đổi kiểu | `data.friend_detail[].added_time` | date (L215) | date \| null (L520) |
| `GET /friends` | output | đổi kiểu | `data.friend_detail[].line_friend_id` | string (L217) | string \| null (L515) |
| `GET /friends` | output | thêm | `data.warnings` | — | L512 |
| `GET /friends` | error | thêm | `added_date_from must be <= added_date_to` | — | L530 |
| `GET /friends` | error | thêm | `added_date_from must be in format yyyy-mm-dd` | — | L529 |
| `GET /friends` | error | thêm | `limit must be a positive integer (1..500), got: 0` | — | L526 |
| `GET /friends` | error | thêm | `parameter 'page' has an invalid format (expected a numeric value).` | — | L525 |
| `GET /friends` | error | thêm | `tag_ids must contain positive integer ids (comma-separated), got: abc` | — | L527 |
| `GET /friends` | error | thêm | `tag_ids not found: [999]. use get /v1/tags to list available tags.` | — | L528 |
| `GET /friends/detail` | output | bớt | `data.friend` | L258 | — |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.friend_info[].type` | string (L270) | string \| null (L640) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.line_friend_id` | string (L260) | string \| null (L632) |
| `GET /friends/detail` | output | bớt | `data.friend.scenarios[].id` | L274 | — |
| `GET /friends/detail` | output | bớt | `data.friend.scenarios[].name` | L275 | — |
| `GET /friends/detail` | output | bớt | `data.friend.tags[].id` | L266 | — |
| `GET /friends/detail` | output | bớt | `data.friend.tags[].name` | L267 | — |
| `GET /friends/detail` | error | thêm | `friend not found` | — | L650 |
| `GET /friends/detail` | error | thêm | `missing required parameter 'lmessage_friend_id'.` | — | L648 |
| `GET /friends/detail` | error | thêm | `parameter 'lmessage_friend_id' has an invalid format (expected a numeric value).` | — | L649 |
| `GET /tags` | output | bớt | `data.tags[]` | L332 | — |
| `GET /tags` | output | thêm | `data.warnings` | — | L761 |
| `GET /friend-info-fields` | output | bớt | `data.fields[]` | L370 | — |
| `GET /friend-info-fields` | output | thêm | `data.warnings` | — | L820 |
| `GET /friend-info-fields` | output | thêm | `…options[].label` | — | L819 |
| `GET /friend-info-fields` | output | thêm | `…options[].option_id` | — | L818 |
| `GET /scenarios` | output | bớt | `data.scenarios[]` | L515 | — |
| `GET /scenarios` | output | thêm | `data.warnings` | — | L891 |
| `POST /messages/push` | input | thêm | `Content-Type` | — | L937 |
| `POST /messages/push` | input | thêm | `X-LME-API-KEY` | — | L936 |
| `POST /messages/push` | input | đổi kiểu | `messages[]` | array<object> (L566) | array<Message object> (L944) |
| `POST /messages/push` | input | chuyển sang mục object | `messages[].duration` | L571 | L1808 (5. Message object › Audio message) |
| `POST /messages/push` | input | chuyển sang mục object | `messages[].preview_url` | L570 | L1726 (5. Message object › Thuộc tính chung) |
| `POST /messages/push` | input | chuyển sang mục object | `messages[].text` | L568 | L1746 (5. Message object › Text message) |
| `POST /messages/push` | input | chuyển sang mục object | `messages[].type` | L567 | L1719 (5. Message object › Thuộc tính chung) |
| `POST /messages/push` | input | chuyển sang mục object | `messages[].url` | L569 | L1725 (5. Message object › Thuộc tính chung) |
| `POST /messages/push` | error | thêm | `(nội dung do hệ thống gửi tin trả về)` | — | L977 |
| `POST /messages/push` | error | thêm | `bot plan expired (over 7 days). sending is disabled.` | — | L975 |
| `POST /messages/push` | error | thêm | `friend not found: 12345 / friend not found, line_friend_id: u…` | — | L966 |
| `POST /messages/push` | error | thêm | `friend_id is required.` | — | L963 |
| `POST /messages/push` | error | thêm | `friend_id must be a numeric lmessage_friend_id.` | — | L965 |
| `POST /messages/push` | error | thêm | `id_type must be one of lmessage_friend_id\|line_friend_id, got: line_user_id` | — | L964 |
| `POST /messages/push` | error | thêm | `lineプランの配信上限に達しました。` | — | L974 |
| `POST /messages/push` | error | thêm | `messages exceeds max 5 per request.` | — | L969 |
| `POST /messages/push` | error | thêm | `messages is required.` | — | L967 |
| `POST /messages/push` | error | thêm | `messages must be a non-empty array.` | — | L968 |
| `POST /messages/push` | error | thêm | `messages[0].type is required.` | — | L970 |
| `POST /messages/push` | error | thêm | `messages[0].type must be one of text\|image\|video\|audio, got: sticker` | — | L971 |
| `POST /messages/push` | error | thêm | `messages[i] … (xem mục 5)` | — | L972 |
| `POST /messages/push` | error | thêm | `ブロックしていますので送信できません。` | — | L976 |
| `POST /messages/push` | error | thêm | `月1000通の配信上限が超えました。` | — | L973 |
| `POST /messages/template` | input | bớt | `Idempotency-Key` | L609 | — |
| `POST /messages/template` | input | thêm | `templates[].edited_content` | — | L1057 |
| `POST /messages/template` | error | thêm | `(nội dung do hệ thống gửi tin trả về)` | — | L1076 |
| `POST /messages/template` | error | thêm | `bot plan expired (over 7 days). sending is disabled.` | — | L1073 |
| `POST /messages/template` | error | thêm | `friend_id is required. …` | — | L1064 |
| `POST /messages/template` | error | thêm | `lineプランの配信上限に達しました。` | — | L1072 |
| `POST /messages/template` | error | thêm | `templates exceeds max 5 per request.` | — | L1067 |
| `POST /messages/template` | error | thêm | `templates is required.` | — | L1065 |
| `POST /messages/template` | error | thêm | `templates must be a non-empty array.` | — | L1066 |
| `POST /messages/template` | error | thêm | `templates[0] edited_content is only allowed for text templates, template 7001 has type: …` | — | L1070 |
| `POST /messages/template` | error | thêm | `templates[0] template 7001 has no sendable message.` | — | L1075 |
| `POST /messages/template` | error | thêm | `templates[0] template_id not found: 7001` | — | L1069 |
| `POST /messages/template` | error | thêm | `templates[0].template_id is required.` | — | L1068 |
| `POST /messages/template` | error | thêm | `ブロックしていますので送信できません。` | — | L1074 |
| `POST /messages/template` | error | thêm | `月1000通の配信上限が超えました。` | — | L1071 |
| `GET /templates` | output | bớt | `data.templates[]` | L642 | — |
| `GET /templates` | output | thêm | `data.warnings` | — | L1131 |
| `GET /conversations` | output | bớt | `data.conversations[]` | L693 | — |
| `GET /conversations` | output | đổi kiểu | `data.conversations[].last_message` | string (L698) | string \| null (L1189) |
| `GET /conversations` | output | đổi kiểu | `data.conversations[].last_message_date` | datetime (L699) | datetime \| null (L1190) |
| `GET /conversations` | output | đổi kiểu | `data.conversations[].line_friend_id` | string (L695) | string \| null (L1186) |
| `GET /conversations` | output | thêm | `data.warnings` | — | L1193 |
| `GET /conversations` | error | thêm | `confirm_status must be 0 (read) or 1 (unread), got: 2` | — | L1199 |
| `GET /conversations` | error | thêm | `display_status must be display\|hidden\|all, got: show` | — | L1205 |
| `GET /conversations` | error | thêm | `handling_status_ids must contain positive integer ids (comma-separated), got: x` | — | L1200 |
| `GET /conversations` | error | thêm | `handling_status_ids not found: [99]. use get /v1/handling-statuses to list available statuses.` | — | L1201 |
| `GET /conversations` | error | thêm | `handling_status_names not found: [フォローアップ]. …` | — | L1202 |
| `GET /conversations` | error | thêm | `parameter 'limit' has an invalid format (expected a numeric value).` | — | L1198 |
| `GET /conversations` | error | thêm | `tag_ids not found: [999]. … / tag_names not found: [vipp]. …` | — | L1203 |
| `GET /conversations` | error | thêm | `tag_mode must be or\|and, got: xor` | — | L1204 |
| `GET /conversations/detail` | error | thêm | `conversation not found` | — | L1319 |
| `GET /conversations/detail` | error | thêm | `missing required parameter 'lmessage_friend_id'.` | — | L1317 |
| `GET /conversations/detail` | error | thêm | `parameter 'lmessage_friend_id' has an invalid format (expected a numeric value).` | — | L1318 |
| `POST /do_action` | input | bớt | `Idempotency-Key` | L863 | — |
| `POST /do_action` | input | đổi kiểu | `actions[]` | array<object> (L853) | array<Action object> (L1603) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].action` | L855 | L1837 (6. Action object) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].field_id` | L857 | L1854 (6. Action object › friend_info — cập nhật friend info) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].handling_status_id` | L862 | L1915 (6. Action object › handling_status — trạng thái xử lý) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].option_id` | L859 | L1856 (6. Action object › friend_info — cập nhật friend info) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].scenario_id` | L860 | L1897 (6. Action object › scenario — chạy / dừng / chạy tiếp) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].start_from` | L861 | L1898 (6. Action object › scenario — chạy / dừng / chạy tiếp) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].tag_ids[]` | L856 | L1843 (6. Action object › tag — gắn / gỡ tag) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].type` | L854 | L1836 (6. Action object) |
| `POST /do_action` | input | chuyển sang mục object | `actions[].value` | L858 | L1855 (6. Action object › friend_info — cập nhật friend info) |
| `POST /do_action` | error | thêm | `actions exceeds max 10 per request.` | — | L1625 |
| `POST /do_action` | error | thêm | `actions is required.` | — | L1623 |
| `POST /do_action` | error | thêm | `actions must be a non-empty array.` | — | L1624 |
| `POST /do_action` | error | thêm | `actions[0] invalid action for type 'tag'. allowed: add\|remove.` | — | L1628 |
| `POST /do_action` | error | thêm | `actions[0] unknown type 'tags'. valid: tag\|friend_info\|scenario\|handling_status\|block\|favorite\|confirm_status.` | — | L1627 |
| `POST /do_action` | error | thêm | `actions[0].type is required.` | — | L1626 |
| `POST /do_action` | error | thêm | `actions[i] …` | — | L1629 |
| `POST /do_action` | error | thêm | `lmessage_friend_ids exceeds max 100 per request.` | — | L1621 |
| `POST /do_action` | error | thêm | `lmessage_friend_ids is required.` | — | L1619 |
| `POST /do_action` | error | thêm | `lmessage_friend_ids must be a non-empty array.` | — | L1620 |
| `POST /do_action` | error | thêm | `lmessage_friend_ids not found: [99901, 99902]` | — | L1622 |

## 3. Mục lục (h2/h3) thêm / bớt

| Thay đổi | Mục | L |
|---|---|---|
| bớt | API index | cũ L182 |
| bớt | Chi tiết API Phase 1 | cũ L196 |
| bớt | Error chung | cũ L166 |
| bớt | Gửi message (text / media) | cũ L550 |
| bớt | Mục đích | cũ L147 |
| bớt | Quy định chung | cũ L151 |
| bớt | Response chung | cũ L161 |
| bớt | Đối ứng use case | cũ L176 |
| thêm | 6. Action object | mới L1833 |
| thêm | Audio message | mới L1804 |
| thêm | 2.1 Base URL & version | mới L225 |
| thêm | block / favorite / confirm_status | mới L1925 |
| thêm | 7.2 Built-in field (ID âm) | mới L1957 |
| thêm | 7. Bảng giá trị | mới L1945 |
| thêm | 4. Chi tiết API | mới L483 |
| thêm | 3. Danh sách API | mới L462 |
| thêm | friend_info — cập nhật friend info | mới L1851 |
| thêm | Gửi message (text / image / video / audio) | mới L928 |
| thêm | handling_status — trạng thái xử lý | mới L1912 |
| thêm | Hướng dẫn chuyển đổi từ tài liệu 1.2.0 | mới L2047 |
| thêm | 9. Hỗ trợ | mới L2063 |
| thêm | 2.9 Idempotency & retry | mới L421 |
| thêm | Image message | mới L1770 |
| thêm | 7.1 Kiểu friend info field | mới L1947 |
| thêm | 5. Message object | mới L1714 |
| thêm | 7.4 message_type và dạng data (/conversations/detail) | mới L1988 |
| thêm | 7.3 Option của field -6 (都道府県名) | mới L1971 |
| thêm | 2.8 Phân trang | mới L391 |
| thêm | 2. Quy ước chung | mới L223 |
| thêm | 2.7 Rate limit | mới L375 |
| thêm | 2.5 Response header | mới L328 |
| thêm | scenario — chạy / dừng / chạy tiếp | mới L1894 |
| thêm | 2.6 Status code & mã lỗi | mới L340 |
| thêm | tag — gắn / gỡ tag | mới L1840 |
| thêm | Text message | mới L1743 |
| thêm | Thuộc tính chung | mới L1717 |
| thêm | 7.5 Trạng thái | mới L2006 |
| thêm | Tóm tắt giới hạn | mới L1818 |
| thêm | 1. Tổng quan | mới L202 |
| thêm | Video message | mới L1792 |
| thêm | 2.2 Xác thực | mới L239 |
| thêm | 2.3 Định dạng request | mới L280 |
| thêm | 2.4 Định dạng response | mới L296 |

Tổng: 12 endpoint · 106 thay đổi param/field/lỗi (ứng viên).
