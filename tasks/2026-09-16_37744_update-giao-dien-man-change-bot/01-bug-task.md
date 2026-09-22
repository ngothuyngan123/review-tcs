# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37744 — Update lại giao diện màn change bot` (tên gốc JP: `LOA入れ替え機能（デザインを更新）`) |
| Module / Màn hình | `Change bot (LINE公式アカウント入れ替え機能 — chức năng thay thế LINE OA) — phần connect bot mới` · URL `/admin/change-bots-new/{id}` (category Redmine: `Change bot`) |

## Mô tả bug (bản dịch tiếng Việt)

Trước đó task tháng 5 phần connect bot mới ở màn change bot mình đang để giao diện cũ => Expect: Update lại theo giao diện mới.

- Tên gốc (JP): `LOA入れ替え機能（デザインを更新）` — chức năng thay thế LINE OA (cập nhật design).
- Design gốc (Figma): https://www.figma.com/design/uxNxjEpTtsVi99qClN6JMc/00-%E5%85%A5%E3%82%8C%E6%9B%BF%E3%81%88%E6%A9%9F%E8%83%BD%E3%80%801%E3%83%B6%E6%9C%88%E7%84%A1%E6%96%99%E9%96%8B%E6%94%BE?node-id=0-1&p=f&t=IwMdwMoTGizyZfXE-0
- Design clone (Figma): https://www.figma.com/design/sS2Nn8LkzXxZQA7ANi1Py3/-AI--00-%E5%85%A5%E3%82%8C%E6%9B%BF%E3%81%88%E6%A9%9F%E8%83%BD%E3%80%801%E3%83%B6%E6%9C%88%E7%84%A1%E6%96%99%E9%96%8B%E6%94%BE?node-id=2-2&p=f&t=YZmEEuUXF6dUSEYi-0
- Link QA: https://aun-mypage.tools/web/visual/show/gBjeCsP7VAi9zpJi5s86EG0W2vYc8tyA

> ⚠️ Ticket này là **tracker `Feature`**, không phải Bug — nội dung là yêu cầu cập nhật giao diện theo design mới, Redmine KHÔNG có section "Tái hiện bug".

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" — ticket là Feature request. -->

## Expected result

- Phần connect bot mới ở màn Change bot hiển thị theo **giao diện mới** (bám design Figma + Link QA ở trên).

## Actual result

- Phần connect bot mới ở màn Change bot vẫn đang để **giao diện cũ** (từ task tháng 5).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #37744 KHÔNG có attachment. 3 link design/QA ở trên nằm trong description, không phải attachment. -->

## Ghi chú thêm của Leader

- **Tracker `Feature` / Status `Closed` (2026-08-21) / Target version `2026-06` / Parent `#36376 [06/2026]`** — task đổi giao diện, không có ca lỗi tái hiện. TC nên tập trung vào **đối chiếu UI với design mới** + **regression luồng change bot (connect bot mới) không đổi hành vi**.
- **Input thiếu:** Redmine KHÔNG có section "Đánh giá ảnh hưởng phía dev" → xem cảnh báo ở `03-dev-impact.md`.
- **Input thiếu:** description không nêu môi trường phát hiện, không nêu account/bot test cụ thể.
- Nguồn spec UI duy nhất hiện có = 2 link Figma + Link QA (aun-mypage.tools). Chỉ dùng được nếu Leader/member mở được link — không truy cập được thì coi như **không có spec UI**, phải hỏi lại người tạo ticket.
- Branch fix: `release_staging_20260704` (nhánh gốc `release_staging_20260527`) — xem journal nguyên văn bên dưới.
- ⚠️ **Bản chất màn**: theo phân tích diff trên MCP LME TEST STUDIO (xem phụ lục `03-dev-impact.md`), màn `/admin/change-bots-new/{id}` **thực tế là wizard nhiều bước** (nhập kênh → webhook → xác nhận, dùng Vue), **không phải landing page marketing tĩnh** như spec `SCR-BE-03` cũ mô tả. Đừng viết/review TC theo spec cũ.

## Journal / note từ Redmine (nguyên văn)

**Journal #126940 — Ngô Thúy Ngần — 2026-07-22:**

```
branch: release_staging_20260704 (nhánh gốc: release_staging_20260527)
```
