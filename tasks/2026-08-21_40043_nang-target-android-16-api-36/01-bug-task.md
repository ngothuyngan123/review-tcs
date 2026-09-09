# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40043 — Nâng target Android 16 (API 36) theo yêu cầu Google Play` |
| Redmine URL | https://redmine.watermelon.vn/issues/40043 |
| Auto-filled | `2026-08-21 by /new-task` |
| Ngày báo cáo | `2026-08-20` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set Category; theo nội dung đánh giá: **app mobile LME (Flutter, Android)** — ảnh hưởng toàn app) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — không phải bug môi trường web. Dev verify trên **máy thật Samsung SM-A556E chạy Android 16 (SDK 36)** + build `flavor dev` / `flavor prod` |

### Metadata Redmine bổ sung

| Trường | Giá trị |
|---|---|
| Tracker | **Feature** (KHÔNG phải Bug) |
| Project | Lme |
| Status | Closed (chuyển Closed lúc 2026-08-21 00:09 bởi Hoang Xuan Thang) |
| Assigned to | Thinh Nguyen (đổi từ user #175 → #111 lúc 2026-08-20 12:48) |
| Target version | (không set) |
| Attachments | 0 |
| Relations | (không có) |

## Mô tả bug (nguyên văn từ khách hàng)

> ⚠️ **Trường `description` của Redmine #40043 TRỐNG (0 ký tự).**
> Toàn bộ nội dung nghiệp vụ nằm ở **journal note #130654** (Đoàn Thị Bích Hảo, 2026-08-20 03:03) — đó là Section "Đánh giá ảnh hưởng" 4 mục, đã được đưa nguyên văn vào [03-dev-impact.md](03-dev-impact.md).

**Bối cảnh (trích nguyên văn mục 1 của journal #130654):**

```
Google Play yêu cầu tất cả app phải target Android 16 (API 36) trở lên. Từ 31/8/2026, nếu app không đạt cấp API mục tiêu trong vòng 1 năm kể từ ngày phát hành Android mới nhất, sẽ không thể cập nhật app trên Play
Console. App hiện đang target API 35 (Android 15) → không tuân thủ.
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Không có. Redmine #40043 là ticket Feature (nâng target SDK theo yêu cầu Google Play), không có section "Tái hiện bug". -->

## Expected result

<!-- Không có trong Redmine. -->

## Actual result

<!-- Không có trong Redmine. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #40043 có **0 attachment**.

## Ghi chú thêm của Leader

⚠️ **Đây là ticket Feature (nâng target SDK), KHÔNG phải bug tái hiện được** — không có Steps/Expected/Actual. Root cause là yêu cầu tuân thủ của Google Play, cách fix đã được Dev mô tả chi tiết ở [03-dev-impact.md](03-dev-impact.md). TCs nên tập trung verify **cách fix + regression impact toàn app**, không phải verify "bug đã hết".

⚠️ **Điểm cần chú ý khi viết/review TC** (suy từ mục 4 của Dev, xem file 03):
- Thay đổi là **build config + hành vi UI/OS**, không đụng data/API/DB → trọng tâm là **regression trên thiết bị thật**, không phải verify dữ liệu.
- Dev nêu 3 vùng **trực tiếp** cần test kỹ: nút Back / vuốt back toàn app (predictive back của Android 16); xem ảnh trong chat (`image_gallery.dart`: WillPopScope → PopScope); khóa xoay màn hình trên tablet/máy gập.
- Dev nêu vùng **gián tiếp** (đổi toàn bộ build engine → smoke test): media, realtime chat Socket.IO, push notification FCM + điều hướng khi bấm noti, booking salon/lesson/event, calendar (shift calendar ca qua đêm).
- Dev yêu cầu **regression thêm trên Android 13/14/15** — không chỉ Android 16.
- Ticket đã ở trạng thái **Closed** trước khi review TC → xác nhận với Leader phạm vi test còn hiệu lực.

**Input thiếu (cần hỏi lại Dev/PM trước khi chốt TCs):**
- Không có link Commit / Pull Request (chỉ có `branch code: master_branch_release_store`).
- Không có Link TCs (Google Sheet) trong Redmine.
- Không nêu build/version cụ thể để QA cài test (chỉ có `versionCode 397`).
- Không nêu danh sách thiết bị/OS bắt buộc trong ma trận test (chỉ có 1 máy Samsung SM-A556E / Android 16 Dev đã tự test).
