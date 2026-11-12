# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder mới + fill các section bên dưới (cùng với `03-dev-impact.md`).
> 2. **Paste tay** — nếu không có Redmine link, member paste nội dung task bug.
>
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39446 — [MCP] Tính năng tạo formanswer` |
| Module / Màn hình | `MCP tool tạo/cập nhật 回答フォーム (form survey) — create_form_survey / update_form_survey` |

## Mô tả bug (bản dịch tiếng Việt)

<!--
Ticket này là **Feature** (Tracker: Feature), không phải bug report từ khách hàng — không có section "Tái hiện bug" trong Redmine.
Nội dung dưới đây là nguyên văn mục 1 + 2 + 3 (Mục đích / Cách thực hiện / Đã check caller) của section "Đánh giá ảnh hưởng" — giữ nguyên vì đã là tiếng Việt, không diễn giải lại.
Mục 4 (Đánh giá ảnh hưởng chi tiết) + mục 5 (Branch) chuyển sang `03-dev-impact.md`.
-->

**1. Mục đích**
- Cho AI client tạo và cập nhật 回答フォーム qua MCP: 2 tool `create_form_survey` (tạo vỏ form) + `update_form_survey` (mảng items 12 thao tác: field CRUD 21 loại, page/phân nhánh, button, header image, design, message/action, diagnostic, settings) — spec theo `docs/04-form-survey.md` §4-5 (đính kèm ticket, xem mục "Ảnh / video / log đính kèm").

**2. Cách thực hiện**
- MCP: typed model `mcp/model/formsurvey` + `FormSurveyPayloadBuilder` (validate limit theo web) + `McpFormSurveyTool` (pre-validate toàn bộ items gồm DB refs trước khi áp, dispatch tuần tự) + 11 method `LmeApiService`.
- linect relay 11 endpoint `/mcp/*` (HMAC); PHP port `FormAnswerMcpService` từ branch cũ + 7 method mới mirror logic web (saveV3 mapping, addPage/removePage, next_page branching, Events type=6 reminder), controller `FormAnswerMobileController` + routes `api-job-auth`.

**3. Đã check và sửa các function sử dụng đến function/data vừa sửa**
- Toàn bộ là code mới/additive; entity `FormAnswerDetail` chỉ thêm mapping cột `typeoption` có sẵn (read-only, không ảnh hưởng caller). PHP `upsertFormDetail` mở rộng key mới dạng optional — service mới port, chưa có caller cũ trên branch.

## Steps to reproduce

<!-- Không áp dụng — đây là Feature mới, không phải bug tái hiện được. Xem "Mục đích" ở trên để biết tool/behavior cần verify. -->

## Expected result

- 2 tool MCP `create_form_survey` / `update_form_survey` hoạt động đúng theo spec `docs/04-form-survey.md` §4-5: tạo form, CRUD 21 loại field, page/phân nhánh (BRANCH), button, header image, design, message/action, diagnostic, settings — không phá vỡ form tạo/sửa trên web editor v3 hay reminder (Events type=6) tạo từ web.

## Actual result

<!-- Không có — feature chưa release, chưa có bug thực tế ghi nhận trên ticket này. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

<!-- Thực chất là 2 file đính kèm spec/test asset, KHÔNG phải log lỗi: -->
- `form-answer.zip` — https://redmine.melonglobal.net/attachments/download/28845/form-answer.zip
- `04-form-survey.md` (spec §4-5 được Dev dẫn chiếu ở mục "Cách thực hiện") — https://redmine.melonglobal.net/attachments/download/31226/04-form-survey.md

## Ghi chú thêm của Leader

⚠️ Đây là ticket **Feature** (tạo mới tool MCP), không phải bug fix — "Mô tả bug" ở trên thực chất là mô tả tính năng. Tool test bằng bot `y2kWN2` qua `POST /call-tool` (theo mục 4.3 ở `03-dev-impact.md`).

## Dữ liệu định danh ca lỗi

<!-- Không có ca lỗi cụ thể — ticket là feature mới, chưa có case thực tế trên production. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #139476 — Văn Đức Nguyễn — 2026-09-30:**

```
branch: m_202609_mcp_create_form_answer_39446
```

**Journal #139632 — Ngô Thúy Ngần — 2026-10-01:**

```
Tên gốc: MCPのフォーム作成
```
