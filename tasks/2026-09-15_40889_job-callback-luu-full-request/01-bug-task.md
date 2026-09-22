# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40889 — [JOB] Job xử lý callback + nhận callback request từ phía LINE support lưu và xử lý request đầy đủ` |
| Module / Màn hình | Job xử lý callback LINE (`HandlePostbackTask`) · Receiver callback LINE (Webhook java — ghi `callback_event`) · Job chuyển tiếp Webhook転送 Kênh 1 (`HandleForwardCallbackEventTask`) |

## Mô tả bug (bản dịch tiếng Việt)

> Đây là ticket **Improve nội bộ** (không phải bug khách hàng báo). Nội dung Redmine đã viết bằng tiếng Việt — chép nguyên văn:

- Feature #40044: Webhook転送 (chuyển tiếp webhook) yêu cầu forward — **gửi nguyên trạng event mà LINE OA nhận được**.
- Mục đích forward là để dùng được nhiều tool song song.
- Các ý cần sửa:
  + Webhook java nhận callback **lưu lại nguyên request** vào database `callback_event`.
  + Job xử lý callback + download media **support thêm case full request** (vẫn support cả case cũ).

Branch callback: `m_202609_forward_webhook_40475_release-callback`
Branch job thường: `m_202609_forward_webhook_40475_cb_full_request`

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket là Improve nội bộ, không có ca lỗi khách báo. -->

## Expected result

<!-- (trống — xem mục 4.3 của 03-dev-impact.md để biết hành vi kỳ vọng sau fix) -->

## Actual result

<!-- (trống) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40889 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Không có section "Tái hiện bug" trong Redmine** — đây là **Improve nội bộ** (tracker: Improve nội bộ, không phải Bug), root cause + cách fix đã được Dev mô tả đầy đủ ở đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung **verify cách fix + regression impact + tương thích ngược row format cũ**.
- **Ticket cha / liên quan**: Feature **#40044** (Webhook転送 — forward nguyên trạng event) và **#40475** (release forward webhook). Yêu cầu nghiệp vụ gốc "gửi nguyên trạng" nằm ở #40044.
- **2 branch** cần dựng env test (không phải 1): `m_202609_forward_webhook_40475_release-callback` (receiver/callback) + `m_202609_forward_webhook_40475_cb_full_request` (job thường). Deploy thiếu 1 trong 2 → hành vi không nhất quán.
- **Thay đổi chỉ áp dụng cho row MỚI** — row cũ trong `callback_event` giữ nguyên format `[{...}]`, **không backfill** → bắt buộc test dữ liệu hỗn hợp (cũ + mới xen kẽ trong cùng vòng chạy job).
- Case đặc biệt LINE gửi: bấm **検証 (Verify webhook URL)** trên LINE Developers → body có `events` rỗng → kỳ vọng row về `STATUS_UNKNOWN_TYPE`, job không văng lỗi parse.
- Kiểm tra **tiếng Nhật / emoji không bị escape `\uXXXX`** là một trong các mục tiêu chính của fix (xem REQ-002 trên Studio).

## Journal / note từ Redmine (nguyên văn)

> Redmine #40889 có **1 journal** (#136198 — Thanh Duy Nguyen — 2026-09-12) và toàn bộ nội dung là **đánh giá ảnh hưởng phía Dev** → đã chép nguyên văn sang [03-dev-impact.md](03-dev-impact.md). Không lặp lại ở đây.
