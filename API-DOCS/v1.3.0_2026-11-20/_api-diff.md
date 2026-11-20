# Diff cấu trúc docs Public API — bản 1.3.0 → 1.3.0

> Cũ: `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html` · Mới: `spec-features/api-public/docs/api-detail-spec_vi_1120.html` · L cũ / L mới = số dòng trong từng file HTML.
> **Heuristic** — khớp theo tên param/field và message lỗi. Mỗi dòng là ỨNG VIÊN: mở L hai bên để xác nhận trước khi ghi `DOC-VER`. Đổi câu chữ message lỗi sẽ hiện thành 1 dòng bớt + 1 dòng thêm.

## 1. Endpoint

| Trạng thái | Endpoint | L cũ | L mới |
|---|---|---|---|
| giữ | `GET /friends` | L488 | L450 |
| giữ | `GET /friends/detail` | L619 | L588 |
| giữ | `GET /tags` | L746 | L738 |
| giữ | `GET /friend-info-fields` | L802 | L802 |
| giữ | `GET /scenarios` | L874 | L887 |
| giữ | `POST /messages/push` | L928 | L949 |
| giữ | `POST /messages/template` | L1038 | L1059 |
| giữ | `GET /templates` | L1117 | L1145 |
| giữ | `GET /conversations` | L1164 | L1200 |
| giữ | `GET /conversations/detail` | L1286 | L1330 |
| giữ | `GET /handling-statuses` | L1545 | L1596 |
| giữ | `POST /do_action` | L1578 | L1636 |

## 2. Thay đổi theo endpoint

| Endpoint | Loại | Thay đổi | Key | Cũ | Mới |
|---|---|---|---|---|---|
| `GET /friends` | output | đổi kiểu | `data.friend_detail[]` | array<object> (L513) | array<FriendSummary> (L477) |
| `GET /friends` | output | bớt | `…[].added_time` | L520 | — |
| `GET /friends` | output | bớt | `…[].email` | L518 | — |
| `GET /friends` | output | bớt | `…[].friendtype` | L521 | — |
| `GET /friends` | output | bớt | `…[].line_friend_id` | L515 | — |
| `GET /friends` | output | bớt | `…[].line_name` | L516 | — |
| `GET /friends` | output | bớt | `…[].lmessage_friend_id` | L514 | — |
| `GET /friends` | output | bớt | `…[].phone` | L519 | — |
| `GET /friends` | output | bớt | `…[].system_name` | L517 | — |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.email` | string \| null (L635) | string (L606) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.friend_info[]` | array<object> (L638) | array<FriendInfo> (L609) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.line_friend_id` | string \| null (L632) | string (L603) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.line_name` | string \| null (L633) | string (L604) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.phone` | string \| null (L636) | string (L607) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.scenarios[]` | array<object> (L643) | array<FriendScenario> (L610) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.system_name` | string \| null (L634) | string (L605) |
| `GET /friends/detail` | output | đổi kiểu | `data.friend.tags[]` | array<object> (L637) | array<FriendTag> (L608) |
| `GET /friends/detail` | output | bớt | `…friend_info[].id` | L639 | — |
| `GET /friends/detail` | output | bớt | `…friend_info[].name` | L641 | — |
| `GET /friends/detail` | output | bớt | `…friend_info[].type` | L640 | — |
| `GET /friends/detail` | output | bớt | `…friend_info[].value` | L642 | — |
| `GET /friends/detail` | output | bớt | `…scenarios[].status` | L644 | — |
| `GET /tags` | output | thêm | `data.tags[]` | — | L752 |
| `GET /tags` | output | bớt | `data.tags[].friend_count` | L760 | — |
| `GET /tags` | output | bớt | `data.tags[].id` | L758 | — |
| `GET /tags` | output | bớt | `data.tags[].name` | L759 | — |
| `GET /tags` | output | đổi kiểu | `pagination` | object (L762) | Pagination (L754) |
| `GET /friend-info-fields` | output | thêm | `data.fields[]` | — | L816 |
| `GET /friend-info-fields` | output | bớt | `data.fields[].field_id` | L814 | — |
| `GET /friend-info-fields` | output | bớt | `data.fields[].field_type` | L816 | — |
| `GET /friend-info-fields` | output | bớt | `data.fields[].options` | L817 | — |
| `GET /friend-info-fields` | output | bớt | `data.fields[].title` | L815 | — |
| `GET /friend-info-fields` | output | đổi kiểu | `pagination` | object (L821) | Pagination (L818) |
| `GET /friend-info-fields` | output | bớt | `…options[].label` | L819 | — |
| `GET /friend-info-fields` | output | bớt | `…options[].option_id` | L818 | — |
| `GET /scenarios` | output | thêm | `data.scenarios[]` | — | L901 |
| `GET /scenarios` | output | bớt | `data.scenarios[].completed_count` | L889 | — |
| `GET /scenarios` | output | bớt | `data.scenarios[].dropped_count` | L890 | — |
| `GET /scenarios` | output | bớt | `data.scenarios[].followers_count` | L888 | — |
| `GET /scenarios` | output | bớt | `data.scenarios[].name` | L887 | — |
| `GET /scenarios` | output | bớt | `data.scenarios[].scenario_id` | L886 | — |
| `GET /scenarios` | output | đổi kiểu | `pagination` | object (L892) | Pagination (L903) |
| `POST /messages/push` | input | đổi kiểu | `messages` | array<Message object> (L944) | array<Message> (L965) |
| `POST /messages/template` | input | đổi kiểu | `templates` | array<object> (L1055) | array<TemplateItem> (L1078) |
| `POST /messages/template` | input | bớt | `templates[].edited_content` | L1057 | — |
| `POST /messages/template` | input | bớt | `templates[].template_id` | L1056 | — |
| `GET /templates` | output | thêm | `data.templates[]` | — | L1159 |
| `GET /templates` | output | bớt | `data.templates[].name` | L1130 | — |
| `GET /templates` | output | bớt | `data.templates[].template_id` | L1129 | — |
| `GET /templates` | output | đổi kiểu | `pagination` | object (L1132) | Pagination (L1161) |
| `GET /conversations` | output | thêm | `data.conversations[]` | — | L1223 |
| `GET /conversations` | output | bớt | `data.conversations[].lmessage_friend_id` | L1185 | — |
| `GET /conversations` | output | đổi kiểu | `pagination` | object (L1194) | Pagination (L1225) |
| `GET /conversations` | output | bớt | `…[].confirm_status` | L1191 | — |
| `GET /conversations` | output | bớt | `…[].handling_status` | L1192 | — |
| `GET /conversations` | output | bớt | `…[].last_message` | L1189 | — |
| `GET /conversations` | output | bớt | `…[].last_message_date` | L1190 | — |
| `GET /conversations` | output | bớt | `…[].line_friend_id` | L1186 | — |
| `GET /conversations` | output | bớt | `…[].line_name` | L1187 | — |
| `GET /conversations` | output | bớt | `…[].system_name` | L1188 | — |
| `GET /conversations/detail` | output | đổi kiểu | `data.handling_status` | object \| null (L1310) | HandlingStatus (L1352) |
| `GET /conversations/detail` | output | đổi kiểu | `data.messages[]` | array<object> (L1305) | array<ConversationMessage> (L1351) |
| `GET /conversations/detail` | output | bớt | `…[].data` | L1309 | — |
| `GET /conversations/detail` | output | bớt | `…[].delivery_date` | L1306 | — |
| `GET /conversations/detail` | output | bớt | `…[].message_type` | L1308 | — |
| `GET /conversations/detail` | output | bớt | `…[].sender` | L1307 | — |
| `GET /handling-statuses` | output | đổi kiểu | `data[]` | array<object> (L1552) | array<HandlingStatus> (L1605) |
| `GET /handling-statuses` | output | bớt | `data[].id` | L1553 | — |
| `GET /handling-statuses` | output | bớt | `data[].name` | L1554 | — |
| `POST /do_action` | input | đổi kiểu | `actions` | array<Action object> (L1603) | array<Action> (L1664) |

## 3. Mục lục (h2/h3) thêm / bớt

| Thay đổi | Mục | L |
|---|---|---|
| bớt | 9. Hỗ trợ | cũ L2063 |
| bớt | 7.4 message_type và dạng data (/conversations/detail) | cũ L1988 |
| thêm | 7.4 message_type và dạng data — MessageData (/conversations/detail) | mới L2058 |

Tổng: 12 endpoint · 70 thay đổi param/field/lỗi (ứng viên).
