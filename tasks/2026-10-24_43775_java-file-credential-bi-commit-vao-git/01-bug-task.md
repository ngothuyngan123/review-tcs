# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43775 — [java] File credential bị commit vào git, 1 file tải được qua web` |
| Module / Màn hình | `Job nền java (linect-service) — notify-setting / FirebaseMessagingModel (push app mobile qua Firebase, subscribe/unsubscribe topic). Ticket gốc còn nêu 4 file credential ở module php-web (public/client_secret.json, public/dev_secret.json, storage/credentials_dev.json, storage/snsline-lme-firebase-adminsdk-*.json) nhưng Dev (DungDV) đã chốt KHÔNG sửa trong ticket này — chỉ sửa job (xem Ghi chú thêm).` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nội dung Redmine đã là tiếng Việt — giữ nguyên văn, không diễn giải lại. -->

Tác động / cách khai thác
- public/client_secret.json (Google OAuth secret, tải trực tiếp qua URL), public/dev_secret.json, storage/credentials_dev.json, storage/snsline-lme-firebase-adminsdk-*.json (private key Firebase Admin – toàn quyền project).

Vị trí code
- các file trên (có trong git ls-files)

Cách sửa
- Xóa khỏi repo & lịch sử git, rotate key, nạp qua env, không đặt trong public/.

Mức tin cậy
- Confirmed

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #43775 không có attachment (0). -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine theo nghĩa "thao tác → lỗi" thông thường — đây là **phát hiện audit bảo mật tĩnh** (file credential nằm thẳng trong git / public/), không phải flow người dùng. Root cause + cách fix đã được Dev confirm đầy đủ qua đánh giá ảnh hưởng (file 03, nguồn: journal #146950 / #147096 / #147481) — TCs nên tập trung verify cách fix (đọc key từ file ngoài repo, xử lý lỗi file thiếu/hỏng) + regression các luồng dùng chung credentials, **không** verify theo kiểu repro bug cũ.

- Priority Redmine: `Immediate` | Status: `Đang fix` | Tracker: `Bug Tester`.
- Branch fix: `ai_studio_fixbug_43775` (từ `release-t09-2026`) — xem chi tiết commit ở file 03.
- **Phạm vi task bị thu hẹp so với báo cáo gốc**: ticket báo 4 file ở `php-web` (`public/client_secret.json`, `public/dev_secret.json`, `storage/credentials_dev.json`, `storage/snsline-lme-firebase-adminsdk-*.json`) + 1 file ở `java-job` (`FirebaseMessagingModel` chứa private key Firebase Admin viết thẳng). Dev **chỉ sửa job** (DungDV chốt) — 4 file `php-web` + nhánh `release-callback-t09-2026` (module callback, cùng lỗi) vẫn CHƯA xử lý, ghi nhận là follow-up ngoài phạm vi. Leader cân nhắc mở ticket riêng cho 2 phần này — không nên kỳ vọng TCs của task #43775 cover được chúng.
- **3 bug con phát sinh trong quá trình AI review/test** (Test Studio task #506, round 2 — journal #147481), cần Leader quyết định trước khi review TC:
  - `#44009` — Dev đề xuất Reject (lỗi `makeJar` do thiếu `converter-jackson`, có sẵn từ base, không do ticket này sửa).
  - `#44010` — Dev đề xuất Reject + cập nhật kỳ vọng testcase Studio `32074` (bỏ phần kiểm `bots.count_app_notify`, đã ngừng ghi có chủ ý từ `#38562`).
  - `#44011` — ĐÃ fix trong round 2 (commit `linect-service@8db0b92a19cf`): `init()` thiếu bắt `RuntimeException` khi file key rỗng/khoảng trắng/mảng JSON → thiếu log + Chatwork (job vẫn dừng đúng, chỉ thiếu cảnh báo).
- Rủi ro deploy Dev nêu nhiều lần: **mọi server job** phải có file key `snsline-lme-firebase-adminsdk-jpi8r-1982b7d90a.json` (hoặc khai báo `FIREBASE_CREDENTIALS_FILE`) **trước khi deploy** — thiếu file ⇒ job không khởi động, lặp lại mỗi chu kỳ crontab + spam Chatwork `[To:6395420]`.
- Rotate key Firebase Admin đã lộ + xóa khỏi lịch sử git là việc vận hành (ops), **không rollback được** — ngoài phạm vi code review của task này nhưng Leader nên note theo dõi riêng.

Dev impact đầy đủ (nguyên nhân / cách fix / function caller / 4.1-4.2-4.3) xem **file 03** — nguồn là 3 journal Redmine (`#146950`, `#147096`, `#147481`), không có section "Đánh giá ảnh hưởng" tách riêng trong `description` của ticket này.
