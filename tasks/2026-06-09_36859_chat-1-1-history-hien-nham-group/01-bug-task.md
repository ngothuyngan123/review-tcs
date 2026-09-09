# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36859 — [29-05-2026][11073][Chat 1:1] Lịch sử chat 1:1 của friend 「鈴音」 hiển thị nhầm thành nhóm LINE 「【エーナビ】HRteam（旧リアステージ）」, tên user sai 「國本 康秀」` |
| Redmine URL | https://redmine.watermelon.vn/issues/36859 |
| Auto-filled | `2026-06-09 by /new-task` |
| Ngày báo cáo | `2026-05-29` |
| Khách hàng / PM báo | `AI LME CSS` (KH thật: y-kunimoto@circus-group.jp / Bot: 転職エージェントナビ by circus) |
| Module / Màn hình | `Chat 1:1 (1:1チャット)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ>` — bug do KH báo (nghi Production) |

## Mô tả bug (nguyên văn từ khách hàng)

User: y-kunimoto@circus-group.jp
Bot Name: 転職エージェントナビ by circus

Trong chat 1:1 (1:1チャット), lịch sử chat (チャット履歴) của friend 「鈴音」 đang bị hiển thị thành nhóm LINE (LINEグループ)「【エーナビ】HRteam（旧リアステージ）」, đồng thời tên user hiển thị trong chat là 「國本 康秀」.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B71B8CNN8

---

### 原文 (JP)
> 1:1チャットで友だち「鈴音」のチャット履歴が、LINEグループ「【エーナビ】HRteam（旧リアステージ）」として表示されており、またチャット内のユーザー名が「國本 康秀」と表示されている。

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Bug KHÔNG tái hiện được (Dev confirm) — xem Ghi chú Leader. -->
1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video — (KH có gửi video qua journal, link OneDrive, xem Ghi chú Leader)
- [ ] Có log / request-response

Attachments:
- https://redmine.watermelon.vn/attachments/download/26147/SnapCrab_NoName_2026-5-29_15-28-33_No-00.png
- https://redmine.watermelon.vn/attachments/download/26148/image%20(7)%20(2).png
- https://redmine.watermelon.vn/attachments/download/26408/snapcrab_noname_2026-6-5_16-2-10_no-00.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Context bổ sung từ journals Redmine:
- (Ngần) `bot_id 35547`, `conversation_id 12886607`.
- (Ngọc Ánh, 2026-06-05) Sau khi tắt extension trình duyệt, hiện tượng có vẻ cải thiện 1 lần nhưng KH báo **tái diễn**. KH gửi video: trong nửa sau video, KH click vào nhóm 「【エーナビ】サポーターズ」 nhưng nội dung hiển thị lại là cuộc trò chuyện của 「【エーナビ】WithR」 (→ khẳng định lỗi hiển thị nhầm hội thoại khi thao tác chuyển nhanh).
  - Link video (OneDrive): https://1drv.ms/v/c/44d82fa4a0f5a544/IQCtMRXOxOKKSJDggf0u8TNaAfI4zI_Pavtx_tDSmxBAUFk
- Issue từng auto-close (Slack 「終了」 2026-06-01) → auto-reopen (Slack 「(W)確認中」 2026-06-09) → status hiện tại: **KH Feedback**.
