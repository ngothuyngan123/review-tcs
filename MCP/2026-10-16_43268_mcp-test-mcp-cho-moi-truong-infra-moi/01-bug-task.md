# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine `/new-task-mcp 43268`. File này **chỉ giữ thông tin cần để viết/review TC**.
> ⚠️ Ticket này **KHÔNG phải bug report** — đây là task hạ tầng: test regression MCP trên infra proxy mới (apache → 2 backend leasedweb/contabo) qua 3 transport (http / sse / httpv2), 6 tổ hợp. Các mục "Steps to reproduce" / "Expected" / "Actual" không áp dụng, xem thay thế ở "Ghi chú thêm của Leader".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43268 — [mcp] test mcp cho môi trường infra mới` |
| Module / Màn hình | `MCP server (backend-mcp-line) — hạ tầng proxy apache + 2 backend (leasedweb / contabo), 3 transport (http / sse / httpv2)` |

## Mô tả bug (bản dịch tiếng Việt)

Infra cũ: client → nginx làm proxy → 1 backend java MCP (hỗ trợ sse / http / http v2).

Infra mới: client → apache làm proxy → rẽ sang 1 trong 2 backend java MCP: server A (leasedweb) hoặc server B (contabo), vẫn hỗ trợ cả 3 transport sse / http / http v2. Endpoint test: `https://test-mcp.lmes.jp`.

**Chọn test case**: hiện Test Studio chưa có kho TC cho MCP. Quy trình: lấy list TC từ Google Sheet + mô tả mục đích task, dùng ChatGPT chọn những TC của tính năng hay dùng → gửi anh Vinh review → import vào Test Studio → chạy automation test. (Đã import — xem `04-tc-list.md`: 65 TC trên Studio task #458, nguồn file `MCP_43268_65TC_IMPORT_FIXED`, tất cả `tc_group = api`, `surfaces = mcp`, chưa chạy.)

**Cách automation test từng môi trường**:
1. Vinh sửa config domain.
2. Duy sửa config apache, chọn backend leasedweb / contabo.
3. Tester thực hiện automation test; sau khi test xong, Duy check log để confirm đúng môi trường đã test.

**Lặp lại cho 6 tổ hợp** (regression trên từng môi trường):
1. http + backend leasedweb
2. http + backend contabo
3. sse + backend leasedweb
4. sse + backend contabo
5. httpv2 + backend leasedweb
6. httpv2 + backend contabo

## Steps to reproduce

<!-- Không áp dụng — đây là task test hạ tầng, không phải bug cụ thể. Quy trình chạy 6 lượt regression ghi ở "Mô tả bug" trên. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- Attachment Redmine: `Task74_API_34TC_IMPORT_FIXED.xlsx` — https://redmine.melonglobal.net/attachments/download/34221/Task74_API_34TC_IMPORT_FIXED.xlsx
- Docs MCP đã tải: `docs/Task74_API_34TC_IMPORT_FIXED.xlsx` — ⚠️ đây là 34 TC **Public API** (task Studio #74, nguồn #39641), KHÔNG phải bộ TC MCP của task này và cũng không phải tài liệu tool MCP. Bộ TC MCP đúng (`MCP_43268_65TC_IMPORT_FIXED`, 65 TC) do human gửi trực tiếp 2026-10-16, chưa có trên Redmine.

## Ghi chú thêm của Leader

- ⚠️ Ticket không có section "Tái hiện bug" / "Đánh giá ảnh hưởng phía dev" đúng format chuẩn — bản chất là task **regression hạ tầng**, không phải fix bug nên không có root cause / cách fix từ Dev. Xem `03-dev-impact.md` để biết cách map 4 mục F/D/T cho task dạng này.
- Bộ TC trên Studio task #458: **65 TC** (import lại 2026-10-16 từ `MCP_43268_65TC_IMPORT_FIXED`; 166 TC cũ bị lệch cột đã đánh dấu xóa, khôi phục được trên Studio). **Toàn bộ chưa chạy** — chưa có kết luận Đạt/Không đạt nào cho infra mới.
- Theo `task_get_context` Studio (info_pack + critique), các điểm cần lưu khi review/viết thêm TC:
  - **Giả định cần Duy xác nhận**: apache trỏ CỐ ĐỊNH 1 backend mỗi lượt test (không phân tải luân phiên) — nếu thực tế có load-balance, SSE có thể bị chia sang 2 server → cần thêm case sticky session.
  - **Chưa rõ khác biệt kỹ thuật `http` vs `httpv2`** — code chỉ thấy 2 chế độ (SSE và STATELESS streamable HTTP); nhánh `production-http` lại để `protocol=SSE` trong properties. Cần hỏi Dev mapping đúng trước khi gán expected theo transport.
  - Cần biết **build/nhánh đang deploy trên mỗi backend** (nhiều nhánh release có danh sách tool bị tắt khác nhau: `production`, `production-http`, `production-sse`, `release-product-202609-v2`, `release-staging`) — nếu 2 backend khác build, `tools/list` lệch không phải lỗi hạ tầng.
  - Cần tài khoản test + cách cấp Bearer token hợp lệ cho automation (OAuth qua `auth_server_url` hay token cấp sẵn) — ticket không ghi.
  - `/health` không phân biệt được backend (service name cố định) — chỉ log phía server mới xác nhận đúng backend đã test.
  - `RULE-MCP-001` (Studio knowledge): KHÔNG dùng `/call-tool` (TestController) để kết luận cho hạ tầng mới — phải đi đúng giao thức MCP thật (`initialize` → `tools/list` → `tools/call`).
  - `RULE-MCP-002`: bắt buộc có case gọi `bot_id` không thuộc user phải bị từ chối (401/403) nhất quán qua proxy mới.
  - `RULE-TOOL-042`: tool ghi gọi qua `linect-service` — mỗi backend mới phải kết nối được linect; lỗi tool ghi không có nghĩa thiếu phía PHP.
  - Phạm vi **loại trừ** (Studio excludedOrDeferred): không phủ toàn bộ ~120 tool, chỉ bộ "tính năng hay dùng" đã duyệt; không test cutover production / failover tự động giữa 2 server.
- Spec-features KHÔNG có mục MCP infra — không có spec tương ứng cho task này (ghi nhận ở `03-dev-impact.md`).

## Dữ liệu định danh ca lỗi

<!-- Không có ca lỗi cụ thể — task hạ tầng, không phải bug báo bởi khách hàng. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #144856 — Bùi Pháp — 2026-10-16:**

```
Bộ test case dùng để test
```
