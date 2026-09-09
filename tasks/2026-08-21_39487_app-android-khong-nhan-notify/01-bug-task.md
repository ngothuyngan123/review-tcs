# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39487 — [Step][Notify setting][App][Android] Phía app android không nhận được notify (nhận notify bị chập chờn lúc được lúc không)` |
| Redmine URL | https://redmine.watermelon.vn/issues/39487 |
| Auto-filled | `2026-08-21 by /new-task` |
| Ngày báo cáo | `2026-08-07` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` (author) |
| Module / Màn hình | `<chưa rõ — Redmine không set category, không có custom field Module>` — suy từ prefix subject: **Notify setting (通知設定) / App Android** |
| Priority | `Medium` (Redmine `priority = Normal`) |
| Môi trường phát hiện | `Production (step.lme.jp)` — suy từ prefix `[Step]` trong subject. **Tester verify lại**, description không ghi env rõ ràng. |

### Metadata Redmine bổ sung (không có trong template gốc)

| Trường | Giá trị |
|---|---|
| Project / Tracker | `Lme` / `Bug Tester` |
| Status hiện tại | `Fix done - Đợi test` (đổi từ `New` lúc 2026-08-18 bởi Thinh Nguyen) |
| Assigned to | `Đoàn Thị Bích Hảo` |
| Done ratio | `100%` |
| Attachments / Relations | `0` / `0` — Redmine **không có** ảnh, video, log, ticket liên kết |
| Journals | `1` (journal #129164 — đánh giá của Dev, xem `03-dev-impact.md`) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #39487. KHÔNG diễn giải lại. -->

```
Steps:
1. Sinh sự kiện notify 
2. Quan sát app android

Actuasl:
2. Không nhận được notify

Expected:
2. Nhận được notify
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Sinh sự kiện notify
2. Quan sát app android

## Expected result

- Bước 2: Nhận được notify

## Actual result

- Bước 2: Không nhận được notify

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> `issue.attachments = []` — Redmine #39487 **không đính kèm** file nào.

## Ghi chú thêm của Leader

> ⚠️ **Steps trong Redmine cực kỳ sơ sài** — chỉ 2 dòng, KHÔNG ghi: loại sự kiện notify nào, bot nào, tài khoản nào, máy Android nào (model / OS version), app version, đã bật 「スマートフォンアプリ」 ở màn 通知設定 chưa. Đây là input mỏng nhất trong 4 file — TCs sẽ phải dựng lại điều kiện từ `03-dev-impact.md`.

> ⚠️ **Bug KHÓ TÁI HIỆN theo bản chất** — Dev mô tả trong journal: *"Triệu chứng: thỉnh thoảng mất thông báo, mở lại app thì hết, rất khó tái hiện."* Điều kiện tái hiện thật (theo Dev) là **2 máy Android cùng model + cùng bản firmware**, hoặc **2 tài khoản khác nhau cùng một `device_id`** — không phải 1 máy đơn lẻ như Steps mô tả. TCs verify fix **bắt buộc** dựng được kịch bản multi-device / multi-account.

> ⚠️ Bug liên quan trực tiếp tới ticket **#39559** (đã có folder review `tasks/2026-08-13_39559_app-smartphone-khong-nhan-thong-bao/`) — cùng feature `notify-setting`, cùng cơ chế `user_firebase_token`. #39559 là fix **backend**, #39487 là fix **app Android**. Redmine không khai báo relation giữa 2 ticket này (`relations = []`) — Leader nên xác nhận với Dev để tránh review trùng / bỏ sót.
