# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41059 bởi `/new-task` — nguồn: **journal #136848** (description không có Section "Đánh giá ảnh hưởng"; Dev ghi đủ 5 mục ở journal).
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (người viết journal; Redmine chưa gán assignee) |
| Commit / Pull Request | `c1ce3c2` + `3722055` |
| Branch | `improve/mcp_2026_09_16` |
| Ngày submit đánh giá | 2026-09-17 |
| Auto-filled | 2026-09-18 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Ticket Improve — Dev ghi mục này là "Mục đích":

- Giảm bộ tool MCP (~110 → 84 active): bỏ tool guide, gộp các tool tách lẻ theo tính năng, description tool chỉ nêu tool làm gì (chi tiết nằm ở description từng field). Spec: `data/lme-tool-refactor-plan.html`, design `ai_impl/design-tool-consolidation-202609161904.md`.

## 2. Cách fix

- Tool cũ comment `@McpTool` (giữ body); thêm tool gộp/mới: `create/update/list_folder`, `create/update_action`, `create/update_filter`, `update_broadcast`, `create/update_scenario_step`, `create/update_autoreply`, `create/update_friend_info_field`, `create/update/get_group_template`, `send_message` (text/template/media), `get_file_params`. Rename park → group.
- Inline action thay bằng `action_id` (ActionRef, hydrate qua `/mcp/get-action` trong ActionChainUtil); nội dung guide chuyển vào typed schema/description (TokenDocs); cập nhật TestController, Postman, tool-annotations.js.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | McpToolDef | Sweep reference tên tool cũ | Đổi tên / gộp tool |
| 2 | Model description | Sweep reference tên tool cũ | Đổi tên / gộp tool |
| 3 | BroadcastService | `edit_broadcast_info` → `update_broadcast` | Gộp tool broadcast |
| 4 | LmeApiService | `get_image_fileparams` → `get_file_params` | Gộp tool file params |
| 5 | TextDataValidator | Bỏ check inline action | Action chuyển sang `action_id` |

> Dev ghi: Compile pass, `/wss-tool-annotations-review` 0 deviation.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Tool mới: McpFolderTool, McpActionTool, McpFilterTool, ActionChainUtil, WelcomeSettingMessageBuilder | file mới | Direct | |
| F2 | Tool sửa/gộp: McpBroadcastTool, McpScenarioTool, McpAutoReplyTool, McpFriendInfoTool, McpTemplateTool, McpTagTool, McpWelcomeMessageTool, McpChatTool | | Direct | |
| F3 | Model: ActionRef (mới), FormButton/ImageTapZone/FormTemplateData/TextUrlSetting (actions → ActionRef), BroadcastMessage, AutoReplyData, FriendInfoSettingAction | | Direct | |
| F4 | Service/Repo: LmeApiService.saveAction/getAction, CategoryRepository.findActiveByBotIdAndKind, StepMessageRepository.findActionIdByStepId | | Direct | |
| F5 | McpToolDef, TokenDocs, TestController, tool-annotations.js | | Direct | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `application.properties`: `mcp.tools.disabled` đổi thành `create_autoreply,update_autoreply` | UPDATE (config) | Các env stag/dev6/prod cần chỉnh khi deploy. Không đổi DB schema. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Action: `create_action` → gắn vào `create_tag`/`update_tag`, template (button/tap zone/URL), welcome, scenario step; `update_action` check propagate | F1, F3, F4 | `<Dev chưa ghi>` |
| T2 | Broadcast: `create_broadcast` (action_id) + `update_broadcast` từng section info/schedule/template/action | F2 | `<Dev chưa ghi>` |
| T3 | Template/Folder: create/update group template, `update_*_template` move `folder_id`, `create/update/list_folder` đủ 5 type | F1, F2, F4 | `<Dev chưa ghi>` |
| T4 | Scenario/Filter/Friend info/Welcome: `create/update_scenario_step`, `create/update_filter` (scenario\|broadcast), `create/update_friend_info_field`, `update_welcome_message` | F1, F2 | `<Dev chưa ghi>` |
| T5 | `send_message` 3 nhánh text/template_id/media_items; `get_file_params` ảnh và file khác | F2, F4 | `<Dev chưa ghi>` |
| T6 | Thứ tự deploy PHP → linect → MCP | D1 | `<Dev chưa ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
