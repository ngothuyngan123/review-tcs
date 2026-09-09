# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36836 — [27-05-2026][QR Landing] Yêu cầu cho đổi tên file / chỉ định nơi lưu trước khi tải QR ở QR code action (QRコードアクション)` |
| Redmine URL | https://redmine.watermelon.vn/issues/36836 |
| Auto-filled | `2026-06-04 by /new-task` |
| Ngày báo cáo | `2026-05-28` |
| Khách hàng / PM báo | `AI LME CSS` |
| Module / Màn hình | `QR Landing` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi env; fix nằm ở header v2) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User:
Bot Name:

Về việc đổi tên file khi tải xuống của QR code action (QRコードアクション):

[補足 / Bổ sung]
Sau khi thực hiện tải xuống, QR được download ngay lập tức. Có thể sửa spec để TRƯỚC khi tải cho phép "đổi tên file" (ファイル名変更) hoặc "chỉ định nơi lưu" (保存先の指定) được không?

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DV32EMRS?record_id=Rec0B6J5RC2V7

---

### 原文 (JP)

```
QRコードアクションのダウンロード時のファイル名変更について

[補足]
ダウンロード実行後、すぐQRがダウンロードされますが、その前に「ファイル名変更」や「保存先の指定」を行えるように仕様修正することは可能でしょうか？
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Lấy từ journal "Tái hiện bug" (Ngọc Ánh) + description. Đây là SpecImprove, không phải defect — "steps" mô tả hành vi hiện tại. -->

1. Mở popup QRコード trên header (header v2).
2. Bấm nút tải QR (QR code action / QRコードアクション).

## Expected result

- Trước khi tải, hệ thống cho phép người dùng **"đổi tên file" (ファイル名変更)** hoặc **"chỉ định nơi lưu" (保存先の指定)**.
- (Journal Tái hiện bug — Ngọc Ánh): khi bấm nút tải QR ở popup QRコード trên header, cho người dùng đổi tên file hay chọn nơi lưu.

## Actual result

- Sau khi bấm tải, QR được **download ngay lập tức**, không cho người dùng đổi tên file hay chọn nơi lưu.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachment từ Redmine #36836:
- `スクリーンショット 2026-05-27 22.36.35.png` (504 KB) — https://redmine.watermelon.vn/attachments/download/26127/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-27%2022.36.35.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- ⚠️ Đây là **SpecImprove** (tracker Redmine = SpecImprove), **không phải defect** — yêu cầu cải tiến spec. Parent issue: #36192.
- Hành vi root đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **luồng "Lưu thành" (Save As) mới** (đổi tên + chọn nơi lưu trước khi tải) + **fallback cross-browser** (trình duyệt không hỗ trợ File System Access API) + **regression** các màn tải file khác dùng chung endpoint `/ajax/download-file-chat11`.
