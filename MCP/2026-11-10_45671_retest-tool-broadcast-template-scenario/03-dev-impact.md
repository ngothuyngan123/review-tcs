# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU**: Redmine #45671 **không có** section "Đánh giá ảnh hưởng phía dev" — đây là task QA tự khởi tạo (tracker **Test**, re-test scope MCP tool hiện có), không phải bug Dev đánh giá nguyên nhân/cách fix. File này giữ nguyên skeleton để tương thích workflow `/review-mcp-tc` + `/write-tc-mcp`, nhưng **không có impact `F*`/`D*`/`T*`/`BUG` nào do Dev kê** — coverage §1 của report phải dựa vào **chiều `diff code`** (Studio `task_get_context` → `dev_impact`/`spec_delta`) thay cho chiều `dev-impact`, hoặc dựa thẳng vào scope 6 mục ở `01-bug-task.md` + rule `framework/mcp-rules.md`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<không áp dụng — task QA re-test, không phải bug Dev fix>` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `<không áp dụng>` |
| Auto-filled | `2026-11-10 by /new-task-mcp` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Redmine #45671 và xác nhận: ticket không có section "Đánh giá ảnh hưởng" (đúng như ghi ở trên), scope 6 mục ở file 01 khớp mô tả ticket.

---

## 1. Nguyên nhân

<!-- Không áp dụng — không phải bug fix. Task yêu cầu re-test hành vi HIỆN TẠI của MCP tool broadcast/template/scenario (tạo/update) đối chiếu với web. -->

Không có root cause cụ thể — mục tiêu là audit coverage test hiện có, không phải verify 1 bug fix cụ thể.

## 2. Cách fix

<!-- Không áp dụng. -->

Không có fix — đây là re-test diện rộng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Không áp dụng — không có danh sách caller do Dev kê. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<không áp dụng>` | | |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Không có `F*` / `D*` / `T*` do Dev kê — danh sách dưới đây là **scope test do QA Leader xác định** (từ mô tả ticket #45671), KHÔNG map 1:1 với "impact Dev tự kê" theo quy ước thường của `/review-mcp-tc` BƯỚC 2 chiều (a). Dùng kèm chiều (b) diff code (Studio `task_get_context`) khi review.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `create_broadcast` / `update_broadcast` | MCP server | Direct | Validate + lưu DB + loại tin nhắn (Phần A) |
| F2 | `create_scenario` / `update_scenario` / `create_scenario_step` / `update_scenario_step` | MCP server | Direct | Validate + lưu DB + loại tin nhắn (Phần A) |
| F3 | `create/update_text/image/form/location/group_template` | MCP server | Direct | Validate + lưu DB + loại tin nhắn (Phần A) |
| F4 | `create/update_action` · `create/update_filter` · `filter_friends` | MCP server | Direct | Dùng chung bởi F1-F3 |
| F5 | `list_folders` · `create_folder` · `update_folder` | MCP server | Direct | Dùng chung bởi F2-F3 |
| F6 | `get_*` / `list_*` tương ứng (`get_scenario_detail`, `get_template_detail`, `get_group_template_detail`, `list_broadcasts`, `list_broadcast_templates`, `list_templates`, `list_scenarios`) | MCP server | Indirect | Dùng cho bước "get sau ghi" (MCP-RULE-05) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Bảng broadcast + bảng con (nội dung tin, filter, action, lịch gửi) | CREATE / UPDATE | Phải khớp dữ liệu tạo từ web |
| D2 | Bảng scenario + scenario_step + folder | CREATE / UPDATE | Phải khớp dữ liệu tạo từ web |
| D3 | Bảng template (text/image/form/location/group) + media (ảnh/video/audio/pdf) | CREATE / UPDATE | Đặc biệt path/mime/size/thumbnail media (mục 2 file 01) |
| D4 | Bảng action chain, filter friend, folder (dùng chung) | CREATE / UPDATE | Liên kết tới D1-D3 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Broadcast (配信) — tạo/sửa trên web | F1, D1 | Medium — regression nếu MCP ghi lệch validate/DB so với web |
| T2 | Scenario (kịch bản) — tạo/sửa trên web | F2, D2 | Medium |
| T3 | Template (mẫu tin) — tạo/sửa trên web, mọi loại tin nhắn | F3, D3 | High — nhiều loại tin nhắn (text/image/imagemap/video/audio/location/sticker/4 loại button) |
| T4 | Gửi tin LINE thực tế (broadcast/scenario job nền) | F1, F2 | High — Phần B, chỉ verify được bằng manual + `prd` |
| T5 | Phân quyền staff + bảo mật cross-bot | F1-F5 | High — rule MCP bắt buộc (MCP-RULE-01, MCP-RULE-02) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) — N/A, đã ghi rõ lý do không áp dụng
- [ ] Mục 2 (cách fix) — N/A, đã ghi rõ lý do không áp dụng
- [ ] Mục 3 — N/A, đã ghi rõ lý do không áp dụng
- [ ] Mục 4.1 không thiếu function trong scope 6 mục ở `01-bug-task.md`
- [ ] Mục 4.2 không thiếu data (đặc biệt: media file path/mime/size/thumbnail)
- [ ] Mục 4.3 cover được cả automation (Phần A) lẫn manual (Phần B/C)
- [ ] Đã đối chiếu `docs/_tool-inventory.md` (sau khi chạy `/review-mcp-docs`) để xác nhận danh sách tool ở mục 4.1 đầy đủ, không thiếu tool mới phát sinh
