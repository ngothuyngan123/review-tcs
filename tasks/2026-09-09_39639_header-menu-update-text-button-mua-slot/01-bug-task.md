# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #39639 bằng `/new-task` (2026-09-09). ⚠️ Ticket này là **tracker Feature** (yêu cầu đổi text), KHÔNG phải bug report — không có section "Tái hiện bug".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39639 — [Header/Menu] Update text của button mua slot` |
| Module / Màn hình | `Header / Menu — nút thêm LOA (アカウント追加) trên màn 「アカウント一覧」` (Redmine không có field Category; màn cụ thể `/admin/home` lấy từ Studio task #112, cần Leader xác nhận) |

## Mô tả bug (bản dịch tiếng Việt)

Tên gốc: フリープラン未使用時のボタンテキスト変更 (Đổi text button khi chưa dùng free plan)

- **Case chưa có bot free**: hiển thị text 「フリープランでLINE公式アカウント追加」
- **Case đã có bot free**: hiển thị text 「有料プランを契約してLINE公式アカウント追加」 và dòng ghi chú phí dưới button 「※フリープランはすでにご利用中のため、ご選択いただけません。」

Design gốc: https://www.figma.com/design/TsVi9zegcbiNWnEoaSM45G/01--02-%E3%83%98%E3%83%83%E3%83%80%E3%83%BC-%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC?node-id=3689-6310&t=Me0P2IYaA1qHni82-0

Design clone: https://www.figma.com/design/v4c7hyx4m64oVB02QQMn6l/-AI--10-08-2026--01--02-%E3%83%98%E3%83%83%E3%83%80%E3%83%BC-%E3%83%A1%E3%83%8B%E3%83%A5%E3%83%BC?node-id=5004-69&p=f&t=B1I484hnMSyHiJOL-0

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — ticket là yêu cầu thay đổi text, không phải bug report. -->

## Expected result

<!-- Xem "Mô tả bug" ở trên: expected chính là 2 case text mà ticket yêu cầu. -->

## Actual result

<!-- Không có — ticket không mô tả hành vi hiện tại. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #39639 không có attachment. Chỉ có 2 link Figma ghi ở phần "Mô tả bug". -->

## Ghi chú thêm của Leader

- ⚠️ **Không có section "Tái hiện bug"** trong Redmine — ticket là **Feature** (đổi text button), không phải bug. TCs nên tập trung verify 2 nhánh hiển thị (đã có / chưa có bot free) + regression vùng bị ảnh hưởng.
- ⚠️ **Không có section "Đánh giá ảnh hưởng phía dev"** — xem cảnh báo trong `03-dev-impact.md`.
- Target version Redmine: `2026-08`. Author + Assignee: Ngọc Ánh. Created 2026-08-13, updated 2026-09-09.
- Điều kiện tiền đề cốt lõi để test: cần **2 tài khoản admin** — 1 tài khoản **đã có** LOA gói Free còn hiệu lực, 1 tài khoản **chưa có** LOA gói Free nào.
- Liên quan business rule: giới hạn **1 bot free/admin** chỉ áp dụng cho admin đăng ký **sau 2021-07-01** (`flagChangeFreePlan`) — xem `spec-features/admin/bot-add-v2/feature-spec.md` BR-004 + `bot-edit` BR-35/BR-36. Cần Leader xác nhận text mới hiển thị thế nào với admin đăng ký **trước** 2021-07-01 (được có nhiều bot free) — ticket KHÔNG nói.
- Môi trường phát hiện: Redmine không ghi.

## Journal / note từ Redmine (nguyên văn)

**Journal #135417 — Tuấn Anh Trần — 2026-09-09:**

```
ảnh hưởng: text button upgrade plan khi có bot free và chưa có bot free
```
