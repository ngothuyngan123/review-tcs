# webhook — Hợp đồng Webhook転送 (chuyển tiếp dữ liệu ra ngoài)

Thư mục chứa **tài liệu hợp đồng Webhook転送** — dữ liệu LME **gửi ra** endpoint bên nhận + yêu cầu với endpoint đó. **Contract-first** (góc nhìn bên nhận), KHÁC spec **code-first** của màn cấu hình Webhook転送 ([admin/webhook-relay/](../admin/webhook-relay/) — FA-047, mô tả cơ chế bên trong LME: web config + job gửi).

## Nội dung

| File | Vai trò |
|---|---|
| [forward-contract-spec.md](forward-contract-spec.md) | Bản markdown — **workflow / skill đọc file này** (2 kênh LINE転送 / L Message転送, retry, chữ ký, built-in field, lỗi hiển thị…). **§0 có bảng đối chiếu mâu thuẫn** với code-first FA-047. |
| [docs/](docs/) | **Bản HTML gốc** nhà cung cấp. Hiện: `webhook_v1_1104.html` (bản 1.0.0 / 16-09-2026, WSSJ). |

## Quy ước

- Thêm version / markdown là bản workflow đọc / HTML là bản gốc — giống [api-public/README.md](../api-public/README.md).
- ⚠️ **Caveat bắt buộc khi trả lời khách**: flag job chuyển tiếp **mặc định TẮT trên production** (G-01, feature-spec FA-047), còn 2 lỗ hổng bảo mật (webhook LINE không kiểm `X-Line-Signature`, job không chống SSRF + follow redirect mang secret) → "chưa nên bật trên production", thời điểm bật thật phải xác nhận với dev/vận hành.
- ⚠️ **Điểm dễ sai**: `X-Lme-Signature` là **secret thô so sánh chuỗi** (chỉ kênh L Message転送), **KHÔNG** phải HMAC; kênh LINE転送 **không có chữ ký** (chỉ khuyến nghị IP/URL khó đoán/secret path). Xem §0 + §5.

## Ai dùng

- Skill [`/verify-support`](../../.claude/commands/verify-support.md) — câu hỏi khách về webhook đọc ở đây.
- Task test webhook (`Surface = api/job`, kênh chuyển tiếp).
