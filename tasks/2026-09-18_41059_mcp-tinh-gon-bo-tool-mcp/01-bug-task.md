# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41059 bởi `/new-task` (2026-09-18). Tracker: **Improve nội bộ** (không phải bug khách báo).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41059 — [MCP] Tinh gọn bộ tool MCP` |
| Module / Màn hình | MCP server LME (bộ tool MCP: guide / folder / action / filter / broadcast / scenario step / autoreply / friend info / template / welcome / send_message / get_file_params) |

## Mô tả bug (bản dịch tiếng Việt)

1. Mục đích
- Bỏ các tool guide
- Gộp các tool tách riêng của từng tính năng lại.
- Phần description của từng trường đã có mô tả rồi, description của tool check lại chỉ cần đề cập tool làm tính năng gì.

2. Spec
- Đọc file lme-tool-refactor-plan-fn.html trong đính kèm để xem chi tiết các thay đổi

## Steps to reproduce

<!-- Ticket Improve — không có Section "Tái hiện bug". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Có tài liệu spec đính kèm

- `lme-tool-refactor-plan-fn.html` (25131 bytes) — https://redmine.watermelon.vn/attachments/download/30555/lme-tool-refactor-plan-fn.html

## Ghi chú thêm của Leader

- ⚠️ Ticket không có Section "Tái hiện bug" (task Improve nội bộ, không phải bug) — nội dung Dev (cách thực hiện + đánh giá ảnh hưởng) nằm ở journal #136848, đã map sang file 03. TCs nên tập trung verify thay đổi bộ tool + regression impact.
- Spec chi tiết nằm trong file đính kèm `lme-tool-refactor-plan-fn.html` (Dev còn nhắc `data/lme-tool-refactor-plan.html` và design `ai_impl/design-tool-consolidation-202609161904.md` trong repo).
- Deploy phải theo thứ tự **PHP → linect → MCP**; config `mcp.tools.disabled` ở các env stag/dev6/prod cần chỉnh khi deploy.

## Journal / note từ Redmine (nguyên văn)

**Journal #136848 — Thanh Duy Nguyen — 2026-09-17:**

```
Improve nội bộ #41059 [MCP] Tinh gọn bộ tool MCP

1. Mục đích
	- Giảm bộ tool MCP (~110 → 84 active): bỏ tool guide, gộp các tool tách lẻ theo tính năng, description tool chỉ nêu tool làm gì (chi tiết nằm ở description từng field). Spec: data/lme-tool-refactor-plan.html, design ai_impl/design-tool-consolidation-202609161904.md.

2. Cách thực hiện
	- Tool cũ comment @McpTool (giữ body); thêm tool gộp/mới: create/update/list_folder, create/update_action, create/update_filter, update_broadcast, create/update_scenario_step, create/update_autoreply, create/update_friend_info_field, create/update/get_group_template, send_message (text/template/media), get_file_params. Rename park → group.
	- Inline action thay bằng action_id (ActionRef, hydrate qua /mcp/get-action trong ActionChainUtil); nội dung guide chuyển vào typed schema/description (TokenDocs); cập nhật TestController, Postman, tool-annotations.js.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
	- Đã sweep reference tên tool cũ trong McpToolDef, model description, BroadcastService (edit_broadcast_info → update_broadcast), LmeApiService (get_image_fileparams → get_file_params); TextDataValidator bỏ check inline action. Compile pass, /wss-tool-annotations-review 0 deviation.

4. Đánh giá ảnh hưởng
        4.1 List function
            - Tool mới: McpFolderTool, McpActionTool, McpFilterTool, ActionChainUtil, WelcomeSettingMessageBuilder (file mới)
            - Tool sửa/gộp: McpBroadcastTool, McpScenarioTool, McpAutoReplyTool, McpFriendInfoTool, McpTemplateTool, McpTagTool, McpWelcomeMessageTool, McpChatTool
            - Model: ActionRef (mới), FormButton/ImageTapZone/FormTemplateData/TextUrlSetting (actions → ActionRef), BroadcastMessage, AutoReplyData, FriendInfoSettingAction
            - Service/Repo: LmeApiService.saveAction/getAction, CategoryRepository.findActiveByBotIdAndKind, StepMessageRepository.findActionIdByStepId
            - McpToolDef, TokenDocs, TestController, tool-annotations.js
        4.2 List những data bị update khi fix bug
            - application.properties: mcp.tools.disabled đổi thành create_autoreply,update_autoreply (các env stag/dev6/prod cần chỉnh khi deploy). Không đổi DB schema.
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Action: create_action → gắn vào create_tag/update_tag, template (button/tap zone/URL), welcome, scenario step; update_action check propagate
            - Broadcast: create_broadcast (action_id) + update_broadcast từng section info/schedule/template/action
            - Template/Folder: create/update group template, update_*_template move folder_id, create/update/list_folder đủ 5 type
            - Scenario/Filter/Friend info/Welcome: create/update_scenario_step, create/update_filter (scenario|broadcast), create/update_friend_info_field, update_welcome_message
            - send_message 3 nhánh text/template_id/media_items; get_file_params ảnh và file khác. Cần deploy PHP → linect → MCP theo thứ tự.

5. Commit / Branch
        5.1 Commit hoặc pull request
            - c1ce3c2 + 3722055
        5.2 Branch hiện tại của task
            - improve/mcp_2026_09_16
```
