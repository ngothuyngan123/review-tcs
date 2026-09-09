# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #38369 bởi `/new-task` — tester verify rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38369 — [01-07-2026][T11423][Auto reply] Khi tắt (OFF) tự động trả lời thì màn hình tự nhảy sang một trang (thư mục) khác.` |
| Redmine URL | https://redmine.watermelon.vn/issues/38369 |
| Auto-filled | `2026-07-01 by /new-task` |
| Ngày báo cáo | `2026-07-01` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn: Tayori task #11423 — user `mitsuya.k@kmsuke.jp`, Bot `横浜Fマリノス`) |
| Module / Màn hình | `Auto reply — Tự động trả lời (自動応答)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill; bug từ KH thật, khả năng Production (step.lme.jp)>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: mitsuya.k@kmsuke.jp
Bot Name: 横浜Fマリノス

Khi chuyển tự động trả lời sang OFF thì
màn hình bị chuyển sang một trang (thư mục) khác

Chức năng: Tự động trả lời (自動応答)
Thời điểm phản hồi: 2026/07/01 00:33:24

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11423
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BEDHQNK33
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1782872318965259
Nguồn: Tayori — task #11423 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/5b68c0d74bbbe3f85e112189f0bde062d96afacd/

---

h3. 原文 (JP)
自動応答をOFFに切り替えをした際に
画面が違うページ（フォルダ）に切り替わってしまう
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có heading "Tái hiện bug" riêng — các bước dưới đây suy ra trực tiếp từ Mô tả bug, tester verify lại. -->

1. Mở màn **Tự động trả lời (自動応答)** của bot, mở một thư mục (folder) bất kỳ đang chứa rule auto reply.
2. Tắt (**OFF**) công tắc tự động trả lời của một rule trong thư mục đang mở.

## Expected result

- Sau khi OFF, màn hình **giữ nguyên** thư mục (folder) đang mở.

## Actual result

- Màn hình tự nhảy sang một trang (thư mục) khác (theo đánh giá Dev: nhảy về thư mục mặc định **未分類 / Chưa phân loại**).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38369 không có attachment. -->

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Bug do hệ thống AI bug detect phát hiện, đã được Auto-fixbug LME fix + submit đánh giá ảnh hưởng (xem `03-dev-impact.md`).
