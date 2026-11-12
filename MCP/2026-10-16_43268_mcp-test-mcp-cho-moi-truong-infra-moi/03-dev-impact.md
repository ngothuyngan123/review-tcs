# 03 — Đánh giá ảnh hưởng từ Dev

⚠️ **INPUT THIẾU: Redmine #43268 chưa có "Đánh giá ảnh hưởng phía dev"** (không có section Nguyên nhân / Cách fix / Function caller / 4.1-4.2-4.3). Ticket này **không phải bug fix** — là task regression hạ tầng (đổi proxy nginx→apache + thêm backend thứ 2), nên không có root cause/code fix từ Dev theo nghĩa thông thường.
Nội dung 4 mục dưới được suy ra từ `task_get_context` (info_pack + critique) của **MCP LME TEST STUDIO task #458** — đây là phân tích tự động của Studio (nguồn: Redmine description + source code `backend-mcp-line`), **KHÔNG phải Dev tự kê**. `/review-mcp-tc` BƯỚC 2 phải coi các mục F/D/T dưới là **gợi ý tham khảo**, vẫn cần hỏi Vinh/Duy xác nhận trước khi chốt — xem các "Giả định" / "Mâu thuẫn" được liệt kê trong `01-bug-task.md` → "Ghi chú thêm của Leader".

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Assignee Redmine: Bùi Pháp; theo mô tả: Vinh (domain config) + Duy (apache config + check log) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` — Studio ghi nhận nhiều nhánh release khác nhau đang deploy (`production`, `production-http`, `production-sse`, `release-product-202609-v2`, `release-staging`) với danh sách tool bị tắt khác nhau; chưa xác nhận backend leasedweb/contabo build nhánh nào |
| Ngày submit đánh giá | `<không có>` |
| Auto-filled | `2026-10-16 by /new-task-mcp` (nguồn: Studio `task_get_context`, không phải Dev) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ không áp dụng theo nghĩa gốc (không có section Dev) — đổi thành: đã đọc lại mục 1-4 dưới (suy từ Studio), xác nhận với Vinh/Duy trước khi dùng làm input cho `/review-mcp-tc`.

---

## 1. Nguyên nhân

Không áp dụng (không phải bug). **Lý do task**: hạ tầng MCP cũ chỉ có 1 proxy (nginx) → 1 backend Java duy nhất. Hạ tầng mới thêm 1 lớp apache làm proxy, rẽ sang 1 trong 2 backend Java độc lập (server A trên leasedweb, server B trên contabo), vẫn giữ 3 kiểu transport cũ (sse / http / http v2). Mục tiêu: xác nhận cả 2 backend mới hoạt động đúng như backend cũ qua endpoint `https://test-mcp.lmes.jp`, trước khi áp dụng production.

## 2. Cách fix

Không áp dụng (không phải bug fix) — đây là đổi hạ tầng (infra change), không có code diff kèm ticket. Quy trình vận hành đổi môi trường test (Studio ghi lại từ description):
1. Vinh sửa config domain.
2. Duy sửa config apache để chọn backend leasedweb hoặc contabo.
3. Tester chạy automation test.
4. Duy check log server để xác nhận đúng backend đã test (vì response `/health` không phân biệt được backend — service name cố định).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Không có — không phải code fix. Endpoint/role liên quan (suy từ Studio elements, KHÔNG phải Dev kê): -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `GET /sse` (chế độ SSE — Bearer token, event-stream) | Route qua apache → 1 trong 2 backend | Transport `sse` |
| 2 | `POST /mcp` (chế độ STATELESS / streamable HTTP) | Route qua apache → 1 trong 2 backend | Transport `http` / `httpv2` — **chưa xác nhận mapping chính xác** |
| 3 | `GET /health` | Không đổi logic, chỉ không phân biệt được backend | Dùng để xác nhận lên đúng server |
| 4 | `GET /.well-known/oauth-authorization-server`, `/.well-known/openid-configuration`, `/.well-known/jwks.json` | Route qua apache | Auth/OAuth discovery |
| 5 | `GET /uploads/ai-images/{filename}` | File nằm trên đĩa local riêng từng server | Ảnh AI không đồng bộ giữa 2 backend → cần test riêng từng backend |
| 6 | `POST /call-tool` (TestController, cửa test nội bộ) | Cần xác nhận có bị chặn qua apache không | **RULE-MCP-001**: không dùng tool này để kết luận cho hạ tầng mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | MCP handshake `initialize → tools/list → tools/call` | `backend-mcp-line` (cả 2 backend) | Direct | Phải full handshake qua MCP thật, không qua `/call-tool` (RULE-MCP-001) |
| F2 | Auth Bearer token / OAuth discovery qua proxy mới | `McpController` `.well-known/*` | Direct | Token sai/hết hạn phải trả 401 nhất quán qua apache; gọi `bot_id` không thuộc user phải bị từ chối (RULE-MCP-002) |
| F3 | SSE streaming dài hạn qua apache | config apache (buffer/timeout/header) | Direct | Tool chạy lâu không bị proxy cắt trước request-timeout |
| F4 | Tool ghi (write) qua `linect-service` | mọi tool có side-effect (tag/template/scenario/broadcast/...) | Direct | Mỗi backend mới phải kết nối được linect-service riêng — lỗi ở đây không phải lỗi phía PHP |
| F5 | Tool đọc dữ liệu tiếng Nhật/emoji + định dạng ngày giờ | mọi tool trả text/date | Indirect | Phải giống nhau trên cả 2 backend (encoding/timezone server) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có thay đổi schema/DB — chỉ đổi routing hạ tầng (proxy + backend) | — | Đối chiếu dữ liệu tool ghi bằng API/tool đọc trên môi trường ngoài, **không** assert trực tiếp DB (RULE-TOOL-020) |
| D2 | File ảnh AI trên đĩa local mỗi server (`/uploads/ai-images/`) | READ | Không đồng bộ giữa leasedweb/contabo — file không tồn tại ở 1 server vẫn là 404 hợp lệ, không phải bug |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | http + backend leasedweb | F1, F2 | High |
| T2 | http + backend contabo | F1, F2 | High |
| T3 | sse + backend leasedweb | F1, F3 | High |
| T4 | sse + backend contabo | F1, F3 | High |
| T5 | httpv2 + backend leasedweb | F1, F2 | High |
| T6 | httpv2 + backend contabo | F1, F2 | High |
| T7 | Bộ tool "tính năng hay dùng" (Tag/Template/Scenario/Welcome Message/Action/Broadcast/Auto Reply/Gửi tin chat/Bot — theo 65 TC đã import Studio #458) | F4, F5 | Medium — chỉ bộ hay dùng được chọn, không phủ toàn bộ ~120 tool (loại trừ có chủ đích) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — ⚠️ N/A, đã thay bằng mô tả đổi hạ tầng
- [ ] Mục 2 (cách fix) có thể trace về code — ⚠️ N/A, không có code diff
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **cần Vinh/Duy xác nhận** 6 endpoint ở mục 3 đã đủ
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — **đặc biệt 2 điểm chưa rõ**: (1) khác biệt kỹ thuật thật giữa `http` và `httpv2`, (2) apache route cố định 1 backend/lượt hay có load-balance luân phiên
