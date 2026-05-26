# 01 — Bug Task từ khách hàng

> File này được sinh từ tiêu đề bug ở sheet `Quản lý hợp đồng` (row 1429) — phần dev report trong sheet không kèm steps reproduce chi tiết của KH. **Input thiếu** (steps reproduce / expected / actual nguyên văn) — Leader/Tester cần verify lại Redmine issue 36303 trước khi review final.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | KH #36303 (回答ID 28089) |
| Redmine URL | https://redmine.watermelon.vn/issues/36303 |
| Auto-filled | `chưa` — fetch Redmine fail (MCP auth 401, env vars chưa load) |
| Ngày báo cáo | 2026-05-07 |
| Khách hàng / PM báo | _<chưa rõ — verify Redmine>_ |
| Module / Màn hình | Quản lý hợp đồng — detail contract (Standard Plan slot chưa connect bot) |
| Priority | High (block thao tác hủy contract → ảnh hưởng billing) |
| Môi trường phát hiện | Production (step.lme.jp) — suy luận, verify Redmine |

## Mô tả bug (nguyên văn từ sheet, chưa verify với Redmine)

> **[07-05-2026][回答ID：28089][Khác] Hủy Standard Plan slot chưa kết nối báo lỗi 'không có quyền', thao tác bị chặn**
>
> Khách hàng có 1 Standard Plan slot chưa được kết nối bot. Khi thao tác hủy slot này, hệ thống báo lỗi "không có quyền" và chặn thao tác. KH không thực hiện được việc hủy contract của chính mình.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — MCP Redmine không fetch được (auth 401). Tester PHẢI mở Redmine 36303 và:
  - Xác nhận nguyên văn description + steps reproduce
  - Lấy screenshot / video / log nếu KH gửi kèm
  - Xác nhận môi trường KH phát hiện (Production / Staging)
  - Xác nhận role + tình trạng account KH (có phải staff cho bot khác không?)

## Steps to reproduce (suy luận từ dev impact — CHƯA verify)

1. Tạo account A. Account A đăng ký 1 Standard Plan slot (chưa connect bot)
2. Account A đồng thời được mời làm **staff cho bot B** (của owner khác), với role KHÔNG có quyền màn point setting
3. Login Account A → chuyển context sang bot B (đang select bot B)
4. Vào màn detail contract của Standard Plan slot (chưa connect) thuộc account A
5. Bấm thao tác hủy contract

## Expected result

- Account A là owner của contract → vào được detail contract và hủy thành công (bỏ qua check quyền theo bot)

## Actual result

- Hệ thống lấy quyền theo bot B đang select → A không có quyền màn point setting trên bot B → bị bounce với lỗi "không có quyền", thao tác hủy bị chặn

## Ảnh / video / log đính kèm

- [ ] Có screenshot — _verify Redmine_
- [ ] Có video — _verify Redmine_
- [ ] Có log / request-response — _verify Redmine_

## Ghi chú thêm của Leader

- Bug liên quan trực tiếp tới logic phân quyền `getRouteFromRoleAccess` — đang check theo bot đang select thay vì check ownership của contract.
- Scenario gốc: contract Standard Plan slot **chưa kết nối bot** — không có bot_id để check quyền → fallback về bot đang select → sai logic.
- Cần làm rõ: bug có xảy ra với plan types khác (Pro / Enterprise / Free)? Với contract đã connect bot rồi nhưng disconnect? Với max friend contract?
