# 02 — Review docs MCP

> Report cho Leader đọc — sinh bởi `/review-docs-mcp`. Task MCP nằm ở `MCP/<YYYY-MM-DD>_<ticket>_<slug>/`.
>
> **Không lệnh nào đọc / gate file này** — `/write-tc-mcp` và `/review-tc-mcp` bám thẳng docs ở `spec-features/mcp/docs/`.
> Docs sai / thiếu → Leader yêu cầu cập nhật docs ở `spec-features/mcp/docs/` (lần chạy sau của 2 lệnh trên tự bám bản mới).
> Chạy lại `/review-docs-mcp` → **giữ nguyên** ghi chú đã điền (merge theo mã `DOC-*`), chỉ thêm dòng mới.
>
> Cột `Quyết định Leader` = **ghi chú tuỳ chọn** của Leader (vd `Theo docs` · `Theo spec` · `Khác: …`), không phải đầu vào của lệnh nào.

## 0. Nguồn

| Trường | Giá trị |
|---|---|
| Docs MCP | `spec-features/mcp/docs/<NN-tính-năng>.md` (human cấp, theo tính năng task chạm) |
| Spec đối chiếu | `spec-features/admin/<feature>/feature-spec.md` (+ `ui-spec` / `api-spec` / `db-mapping` nếu có) — `không có spec` thì ghi rõ |
| Kho TCs đối chiếu | `kho-tcs/fa<xxx>-*.md` — `kho-tcs chưa có FA-xxx` thì ghi rõ |
| Quy mô | `<n> tool · <m> param` — chi tiết ở `_tool-inventory.md` (folder task) |

---

## 1. Tóm tắt inventory

| Tool | Thao tác | Số param | Bắt buộc | Tính năng LME (FA-xxx) |
|---|---|---|---|---|
| `create_<x>` | tạo | `<n>` | `<k>` | `FA-0xx <Tên VN> (<Tên JP>)` |

<!-- 1 dòng / tool. Bảng param đầy đủ KHÔNG chép ở đây — nằm ở _tool-inventory.md (folder task). -->

---

## 2. Mâu thuẫn nội tại docs MCP (`DOC-INT`)

> Cùng 1 tool / param mà docs mô tả **khác nhau** ở 2 chỗ: enum / limit / bắt buộc lệch giữa các mục ·
> ví dụ JSON trái schema · mã lỗi / hành vi lỗi mâu thuẫn · tên param khác nhau giữa mô tả và ví dụ.
> Không có → ghi "Đã rà `<n>` tool — không phát hiện mâu thuẫn nội tại."

| # | Tool · param | Docs ghi (chỗ A) | Docs ghi (chỗ B) | Khả năng | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| DOC-INT-1 | `update_<x>.items[].type` | `§4.2: enum 12 loại` | `§5 ví dụ: "MOVE_FIELD" (không có trong enum)` | `(A) ví dụ sai` / `(B) enum thiếu` | `[MAJOR]` | |

---

## 3. Docs trái spec-features / kho-tcs (`DOC-SPEC`)

> Docs ghi **trái** Business rule ở `spec-features/` hoặc trái **quyết định Leader** đã có trong kho-tcs
> (cột `QUYẾT ĐỊNH` / dòng `MT-xx`). **KHÔNG tự chọn bên** — nêu đủ 2 khả năng.
> Không có → "Đã rà `<n>` param × `<file spec + file kho>` — không phát hiện mâu thuẫn."

| # | Tool · param | Docs ghi | Đối chiếu (nguồn + vị trí) | Khả năng | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| DOC-SPEC-1 | `create_<x>.name` | `cho phép trùng tên` | `feature-spec.md BR-03: "管理名 không được trùng"` | `(A) docs/code MCP sai` / `(B) spec cũ → cần update` | `[BLOCKER]` | |

---

## 4. Docs thiếu so với spec-features (`DOC-MISS`)

> 3 nhóm, ghi đủ cả 3 (nhóm nào sạch thì 1 dòng "Không thiếu"):
> **(a) Setting / field web có mà docs MCP không có** → MCP có cần hỗ trợ không?
> **(b) Validate spec có mà docs không ghi** → MCP có chặn không, chặn ra mã gì?
> **(c) Docs không nói gì về 4 rule bắt buộc** ở [framework/mcp-rules.md](../../framework/mcp-rules.md):
> MCP-RULE-01 bot A ↔ B · MCP-RULE-02 staff không quyền · MCP-RULE-03 limit bot Free · MCP-RULE-04 trùng tên quản lý.

| # | Nhóm | Tool · param / setting | Spec / web có | Docs MCP | Câu hỏi cho Leader | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-MISS-1 | `(a) setting web` | `<setting>` | `feature-spec.md §<mục>` | `không có` | `MCP có cần set được <setting> không?` | `[MAJOR]` | |
| DOC-MISS-2 | `(b) validate` | `create_<x>.<param>` | `spec: tối đa 50 ký tự` | `không ghi limit` | `MCP chặn ở 51 ký tự, trả 400/422?` | `[MAJOR]` | |
| DOC-MISS-3 | `(c) MCP-RULE-02` | mọi tool `<tính năng>` | `PERM-001 — staff không quyền bị chặn` | `không nói` | `Staff không quyền <tính năng> gọi tool (cả tool đọc) → 403?` | `[BLOCKER]` | |

---

## 5. Docs có, spec không có (`DOC-EXTRA`) — thông tin

> Param / hành vi chỉ MCP có (vd field chỉ tồn tại ở MCP). Không phải lỗi — là **ứng viên cập nhật spec**,
> và nhắc `/review-tc-mcp` không lấy hành vi này áp ngược cho TC web.

| # | Tool · param | Docs ghi | Ghi chú | Quyết định Leader |
|---|---|---|---|---|
| DOC-EXTRA-1 | | | `spec-features chưa có — đề xuất bổ sung` | |

---

## 6. Tổng hợp

| Severity | DOC-INT | DOC-SPEC | DOC-MISS | DOC-EXTRA | Tổng |
|---|---|---|---|---|---|
| `[BLOCKER]` | | | | — | |
| `[MAJOR]` | | | | — | |
| `[MINOR]` / `[NIT]` | | | | | |

**Bước tiếp theo**: Leader đọc report, yêu cầu cập nhật docs ở `spec-features/mcp/docs/` nếu cần → Studio chưa có TC: `/write-tc-mcp <folder>` · Studio đã có TC: `/review-tc-mcp <folder>` (cả 2 không cần file này).
