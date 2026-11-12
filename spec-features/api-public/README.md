# api-public — Hợp đồng Public API `/v1/*` (external integration)

Thư mục chứa **tài liệu hợp đồng Public API** của LME — phần mà hệ thống **bên ngoài** (CRM/SFA, EC, automation tool) gọi bằng API key `lme_live_sk_`. Đây là **contract-first** (tài liệu nhà cung cấp phát hành), KHÁC spec **code-first** của màn quản trị API key ([admin/api-integration/](../admin/api-integration/) — FA-046).

## Nội dung

| File | Vai trò |
|---|---|
| [public-api-spec.md](public-api-spec.md) | Bản markdown theo style project — **workflow / skill đọc file này** (endpoint, param, sample, rate limit, error, do_action, 47 tỉnh…). Có §0 đối chiếu với code-first FA-046. |
| [docs/](docs/) | **Bản HTML gốc** nhà cung cấp (authoritative, để diff khi có version mới). Hiện: `api_v1_1104.html` (bản 1.2.0 / 28-09-2026, WSSJ→Missiona). |

## Quy ước

- **Thêm version mới**: bỏ HTML mới vào `docs/` (giữ tên gốc có mốc ngày), **giữ** bản cũ; cập nhật `public-api-spec.md` theo bản mới nhất + ghi version ở header + mục "Lịch sử cập nhật".
- **Markdown là bản workflow đọc**; HTML là bản gốc đối chiếu. Nội dung lệch nhau → tin HTML, sửa markdown.
- ⚠️ **Caveat bắt buộc khi trả lời khách**: route `/v1/*` + middleware + job hết hạn key **chưa thấy trong source đã clone** ([admin/api-integration/web/api-spec.md §7](../admin/api-integration/web/api-spec.md)) → doc là **oracle expected**, nhưng **chưa verify bằng code runtime**; thời điểm **bật thực tế trên production** phải xác nhận riêng với dev/vận hành.

## Ai dùng

- Skill [`/verify-support`](../../.claude/commands/verify-support.md) — câu hỏi khách về Public API đọc ở đây.
- Task test Public API (`Surface = public-api`).
