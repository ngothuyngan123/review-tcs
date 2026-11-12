# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`) rồi parse section "Đánh giá ảnh hưởng", fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Văn Đức Nguyễn` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `MCP + linect: m_202609_mcp_create_form_answer_39446` · `PHP lme: feature/improve-api-for-mcp` |
| Ngày submit đánh giá | `<chưa rõ — description không ghi ngày submit riêng, issue tạo 2026-08-07, journal branch cập nhật 2026-09-30>` |
| Auto-filled | `2026-10-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Feature mới — không có "nguyên nhân bug". Giữ nguyên mục đích theo Redmine (đã chép đầy đủ ở 01-bug-task.md mục "Mô tả bug"). -->

Không áp dụng — đây là Feature mới (tạo tool MCP `create_form_survey` / `update_form_survey`), không phải bug fix. Xem mục đích ở `01-bug-task.md`.

## 2. Cách fix

<!-- Feature mới — xem "Cách thực hiện" đã chép ở 01-bug-task.md. -->

Xem mục "Cách thực hiện" ở `01-bug-task.md` (MCP typed model + FormSurveyPayloadBuilder + McpFormSurveyTool + 11 method LmeApiService; linect relay 11 endpoint HMAC; PHP FormAnswerMcpService port từ branch cũ + 7 method mới + FormAnswerMobileController + routes api-job-auth).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Entity `FormAnswerDetail` | Thêm mapping cột `typeoption` có sẵn | Read-only, không ảnh hưởng caller cũ |
| 2 | PHP `upsertFormDetail` | Mở rộng key mới dạng optional | Service mới port, chưa có caller cũ trên branch |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `McpFormSurveyTool.createFormSurvey` / `updateFormSurvey` | MCP | Direct | Entry point 2 tool mới |
| F2 | `FormSurveyPayloadBuilder.*` | MCP | Direct | Validate limit theo web trước khi dispatch |
| F3 | `LmeApiService` (+11 method form-survey) | MCP | Direct | Gọi xuống linect |
| F4 | `TestController` (+2 case) | MCP | Direct | Test case nội bộ cho 2 tool |
| F5 | `McpFormSurveyController` (11 endpoint) | linect | Direct | Relay HMAC |
| F6 | `McpModel.forwardFormSurvey` (+11 request*) | linect | Direct | Forward request xuống PHP |
| F7 | `ILmeWebService` (+11 khai báo) | linect | Direct | Interface khai báo 11 method |
| F8 | `FormAnswerMcpService.saveField/deleteField/savePage/addPage/removePage/setNextPage/saveReminders` | PHP lme | Direct | Port từ branch cũ + mirror logic web (saveV3 mapping, next_page branching, Events type=6 reminder) |
| F9 | `FormAnswerMobileController` | PHP lme | Direct | Controller mới cho route MCP |
| F10 | `routes/api.php` (+11 route) | PHP lme | Direct | Route mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `FormAnswerDetail.typeoption` (mapping cột có sẵn) | UPDATE (code mapping, không migration) | Read-only, không đổi schema |
| — | Không có migration/config khác | — | Dev xác nhận "Không có (không migration/config; chỉ ghi dữ liệu nghiệp vụ qua API)" |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Tool MCP mới — test `POST /call-tool` (bot test `y2kWN2`): tạo form, thêm/sửa/xóa 21 loại field, page + phân nhánh BRANCH, design/settings/diagnostic/reminder | F1-F4 | — (tính năng mới, verify theo spec) |
| T2 | Web フォーム編集 — form tạo từ MCP phải mở/sửa bình thường trên editor v3 (field shape, selectable JSON, branching) | F5-F10, D1 | High |
| T3 | Reminder (Events type=6) — step tạo từ MCP tính `sent_date_time` đúng, không phá step tạo từ web | F8 | Medium |
| T4 | Friend info — field link friend info từ MCP sinh `friend_information_setting` + sync option/tag đúng | F8, D1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
