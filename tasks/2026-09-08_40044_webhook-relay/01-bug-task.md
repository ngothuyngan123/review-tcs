# 01 — Bug Task từ khách hàng

> ⚠️ Ticket này là **Feature (Tính năng mới)**, không phải bug: Redmine #40044 tracker = `Feature`, status = `New`, target version = `2026-08`, parent = #38894. Vì vậy các section "Steps to reproduce / Expected / Actual" **để trống theo thiết kế** — không có bug để tái hiện.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40044 — Webhook転送` (Feature, parent #38894, version 2026-08) |
| Module / Màn hình | Màn mới 「Webhook転送」 — nằm ngay dưới 「接続設定」 trong menu trái; 2 tab: 「LINE公式アカウントデータ転送」 (chuyển tiếp LINE) và 「L Messageデータ転送」 (chuyển tiếp LME) |

## Mô tả bug (bản dịch tiếng Việt)

Tên gốc: **Webhook転送** (chuyển tiếp webhook).

- Mình nhận được webhook của LINE thì mình forward lại **toàn bộ webhook** cho bên đã liên kết với LME.
- Nên dùng chung webhook hay tách webhook ra? ⇒ **Tách ra**: webhook của LINE và webhook nội bộ (LME).
- Tag được add/remove ⇒ **Notify**.
- Friend info thay đổi ⇒ **Notify**.

**Tài liệu spec:**
- Link HTML (preview design): https://docs.missiona.co/product_lme/webhook-relay/ — *tài khoản login ghi nguyên văn trong description Redmine #40044; KHÔNG chép credential vào repo.*
- Link prototype: https://github.com/missiona-inc/prototype-lme/tree/main/webhook-relay

## Steps to reproduce

*(Không có — ticket Feature, không phải bug.)*

## Expected result

*(Không có — xem spec/prototype ở phần Mô tả và các journal bên dưới.)*

## Actual result

*(Không có — ticket Feature, không phải bug.)*

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*(Redmine #40044 KHÔNG có attachment nào.)*

## Ghi chú thêm của Leader

- ⚠️ **Ticket Feature — không tái hiện được bug.** TCs tập trung verify **spec tính năng mới + regression** lên các luồng bị chạm (nhận webhook, tag, friend info), không phải verify fix bug.
- **Branch dev**: `ai-feature-40044-v2` (journal #133926 — Nguyen Ngoc Hai).
- **Điều kiện dựng env test** (journal #133926):
  - `php artisan migrate` — 3 bảng mới
  - `php artisan access-feature:webhook-relay` — quyền màn + 5 sub-route
  - `php artisan config:clear && php artisan route:clear && php artisan view:clear`
  - ENV: `WEBHOOK_RELAY_ENABLED=true`, `WEBHOOK_RELAY_NOTIFY_ENABLED=true`
- **Phân quyền** (journal #133344): quyền mới nằm dưới mục 「LINE公式アカウント入れ替え」; mặc định **chỉ owner (主管理者)** có quyền, checkbox **không tích sẵn**.
- **Spec chốt thêm** (journal #133769): phần webhook phía LINE **không có Signing secret** (chỉ tab LME mới có).
- Redmine **KHÔNG có** section "Đánh giá ảnh hưởng phía dev" → xem cảnh báo ở `03-dev-impact.md`.
- Redmine **KHÔNG có** section "Link TCs" → bộ TC ở `04-tc-list.md` lấy từ **MCP LME TEST STUDIO** task #269.

## Journal / note từ Redmine (nguyên văn)

**Journal #133344 — Ngọc Ánh — 2026-08-28:**

```
Update spec: 
1. Add menu phía dưới phần 「接続設定」
・API連携
・Webhook転送
Link icon menu: 
API
https://fontawesome.com/icons/classic/thin/rectangle-api

webhook
https://fontawesome.com/icons/classic/thin/webhook

2. Phân quyền staff:
Add quyền phía dưới mục LINE公式アカウント入れ替え
Default: chỉ để quyền cho owner (主管理者), và không tích chọn checkbox
3. Update design: "Chuyển tiếp LINE" / "Chuyển tiếp LME", mỗi tab có phần thiết lập chuyển tiếp riêng.
Github　　：https://github.com/missiona-inc/prototype-lme/tree/main/webhook-relay
プレビュー：https://docs.missiona.co/product_lme/webhook-relay/
```

**Journal #133769 — Ngọc Ánh — 2026-09-03:**

```
Phần webhook: giữ nguyên theo design, phần webhook phía line không có Signing secret
```

**Journal #133926 — Nguyen Ngoc Hai — 2026-09-03:**

```
branch: ai-feature-40044-v2

php artisan migrate                       # 3 bảng mới
php artisan access-feature:webhook-relay  # quyền màn + 5 sub-route
php artisan config:clear && php artisan route:clear && php artisan view:clear

env:

WEBHOOK_RELAY_ENABLED=true
WEBHOOK_RELAY_NOTIFY_ENABLED=true
```
