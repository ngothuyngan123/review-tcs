# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36491 bằng `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #36491 — [18-05-2026][10942][QR Landing] QRコードアクション — đã set 終了時期 nhưng status không tự OFF |
| Redmine URL | https://redmine.watermelon.vn/issues/36491 |
| Auto-filled | 2026-05-19 by /new-task |
| Ngày báo cáo | 2026-05-18 |
| Khách hàng / PM báo | AI CSS (báo hộ KH user `takeuchi@imk-holdings.co.jp`, bot `Dr.小林弘幸`) |
| Module / Màn hình | QR Landing — QRコードアクション (QR code action), list page |
| Priority | Medium (Redmine Normal) |
| Môi trường phát hiện | Production (`step.lme.jp`) — screenshot filename của KH có `[step.lme.jp]` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: takeuchi@imk-holdings.co.jp
Bot Name: Dr.小林弘幸

QRコードアクション (QR code action) — khách đã set 終了時期 (end date) nhưng status (稼働) không tự chuyển OFF khi đến hạn.

[補足 / Note bổ sung]
Đối tượng: tất cả items trong folder 「菌活1日目」
※ Image trong screenshot là 「菌活1日目見込み」

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B4DK6BDDY
```

### 原文 (JP)

```
QRコードアクションで、終了時期を設定しても稼働がOFFにならない

[補足]
対象：「菌活1日目」フォルダにある、全て
※画像は「菌活1日目見込み」
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ journal #118642 "Tái hiện bug" của Hạnh Nguyễn (2026-05-19). KH gốc chỉ mô tả hiện tượng; Dev tái hiện qua kịch bản toggle thủ công sau khi đã đến start_time. -->

**Setup**:
1. Thực hiện set schedule tự động ON/OFF cho QR.
2. Chọn loại có cả **start time** và **end time** (option `終了日時を設定する`).

**Thao tác**:
1. Tới `start_time` → QR tự chuyển = **ON**.
2. Thực hiện thủ công QR = **OFF** tại màn list.
3. Sau đó bật thủ công lại QR = **ON**.

## Expected result

- Tới thời điểm `end_time`, QR luôn được tự động **OFF** (auto-OFF theo schedule).

## Actual result

- QR khi tới `end_time` vẫn hiển thị **ON** → schedule auto-OFF không hoạt động sau khi user toggle thủ công.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments từ Redmine:
- https://redmine.watermelon.vn/attachments/download/25816/FireShot%20Capture%20063%20-%20QR%E3%82%B3%E3%83%BC%E3%83%89%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%EF%BC%88%E7%B7%A8%E9%9B%86%EF%BC%89%20-%20%5Bstep.lme.jp%5D.png (màn edit QR code action)
- https://redmine.watermelon.vn/attachments/download/25817/FireShot%20Capture%20062%20-%20QR%E3%82%B3%E3%83%BC%E3%83%89%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%EF%BC%88%E4%B8%80%E8%A6%A7%EF%BC%89%20-%20%5Bstep.lme.jp%5D.png (màn list QR code action)

## Ghi chú thêm của Leader

- Bug KH report qua Slack list `Rec0B4DK6BDDY` (xem link trong description).
- Bug **không tái hiện trực tiếp được từ steps gốc của KH** — KH chỉ thấy hiện tượng "set 終了時期 nhưng status không OFF". Dev (Hạnh Nguyễn) tái hiện được qua flow: **toggle thủ công OFF rồi ON lại sau khi đã đến start_time** → flag `time_qr_off_status` bị reset sai. Đây là root cause Dev confirm.
- Function fix: `QRCodeController@ajaxUpdateBasicQrs` (QRCodeController.php:999-1024) — xem `03-dev-impact.md`.
- TCs tham chiếu (Dev đã viết template trong Sheet master tab "Improve 1.0" row 3546-3562) — xem `04-tc-list.md`.
- Issue assigned_to = Kieu Son Tung; journal Section "Đánh giá ảnh hưởng" do **Hạnh Nguyễn** submit (2026-05-19) — cần confirm rõ ai là dev fix chính nếu cần hỏi lại impact.
