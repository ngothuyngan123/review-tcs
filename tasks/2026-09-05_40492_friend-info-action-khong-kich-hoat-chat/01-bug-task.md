# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40492` — [04-09-2026][T12067][Info friend] Sau khi đổi thủ công 友だち情報【来院状態】qua chat 1:1, đối ứng ステータス・ステップ配信 cài trong friend info action không kích hoạt dù đã refresh màn hình (giống ca 【お問い合わせNo.11981】). |
| Redmine URL | https://redmine.watermelon.vn/issues/40492 |
| Auto-filled | `2026-09-05 by /new-task` |
| Ngày báo cáo | `2026-09-04` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn: Tayori task #12067 → Slack ユーザー問い合わせ) |
| Module / Màn hình | `Info friend` (友だち情報管理) — điểm phát sinh: Chat 1:1 → panel 友だち情報 |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `Production` — tài khoản khách thật `tokyoeyeclinic.lillyline@lillyholdings.co.jp`, bot `GCT Tokyoアイクリニック` |

> **Field bổ sung từ Redmine** (không có trong template):
>
> | Trường | Giá trị |
> |---|---|
> | Tracker | `Bug KH` (đổi từ `Bug KH cần xử lý nội bộ` ngày 2026-09-05) |
> | Status | `Fix done - Đợi test` |
> | Assigned to | `Ngô Thúy Ngần` |
> | Parent task | `#40400` |
> | Category | `Info friend` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
WSSJ TẠO TASK ĐIỀU TRA NỘI BỘ (chưa có ticket Slack)

User: tokyoeyeclinic.lillyline@lillyholdings.co.jp
Bot Name: GCT Tokyoアイクリニック

Đây là tài khoản đang xảy ra hiện tượng giống 【お問い合わせNo.11981】.
① Vào qua QRコードアクション【院内QR】
② Ở Q2 của フォーム（ご来院アンケート）, chọn 「老視用ICLと白内障系で迷い中」
→ 友だち情報【来院状態】ghi nhận thành 「治療未定」
③ Đổi thủ công 友だち情報【来院状態】qua chat 1:1
→ Dù đã refresh màn hình, 対応ステータス・ステップ配信 đã cài trong 友だち情報アクション vẫn không kích hoạt

Tên friend: テスト（リリー）
Chức năng: Quản lý thông tin bạn bè (友だち情報管理)
Thời điểm phản hồi: 2026/09/04 13:30:29
Ảnh 1: data/screenshots/T12067_0.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12067
Nguồn: Tayori — task #12067 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/89c743d3bd52d35727579a0525c87a2ee8dcf543/

---

h3. 原文 (JP)
<pre>
【お問い合わせNo.11981】と同じ現象が起きているアカウントです。
①QRコードアクション【院内QR】より流入
②フォーム（ご来院アンケート）のQ2で「老視用ICLと白内障系で迷い中」を選択
→友だち情報【来院状態】に「治療未定」が記録される
③1:1チャットにて手動で友だち情報【来院状態】を変更
→画面更新をしても、友だち情報アクションに設定している対応ステータス・ステップ配信が発火しない
</pre>

<!-- TaskRef: cs_form:T12067 -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguồn: journal #134108 — **Thanh Phương** (2026-09-04 07:18), section `* Tái hiện bug`. Nguyên văn:

1. Friend info A có type `select`, có setting action + chọn option **chạy action nhiều lần**
2. Form answer có setting action khi submit form có action gán friend info A
3. Line user submit form được action gán friend info value
4. Admin vào màn chat 1:1 thay đổi friend info value của line user

> Luồng khách báo (nguyên văn description, ①②③):
>
> ① Vào qua QRコードアクション【院内QR】
> ② Ở Q2 của フォーム（ご来院アンケート）, chọn 「老視用ICLと白内障系で迷い中」 → 友だち情報【来院状態】ghi nhận thành 「治療未定」
> ③ Đổi thủ công 友だち情報【来院状態】qua chat 1:1

## Expected result

- Mỗi khi thay đổi info value thì **send được action của friend info value** cho user (journal #134108).
- 対応ステータス (trạng thái đối ứng) đổi theo cấu hình action + ステップ配信 (kịch bản phát theo bước) được khởi động.

## Actual result

- Khi thay đổi friend info value thì **không send được action** của friend info value cho user, **mặc dù friend info setting để chế độ chạy action nhiều lần** (journal #134108).
- Dù đã refresh màn hình, 対応ステータス・ステップ配信 cài trong 友だち情報アクション vẫn không kích hoạt.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [x] Có video
- [ ] Có log / request-response

| # | File | Link |
|---|---|---|
| 1 | `screenshot1.png` (1.9 MB, 2026-09-04) | https://redmine.watermelon.vn/attachments/download/29912/screenshot1.png |
| 2 | `画面収録_20260904_1323_圧縮.mp4` (1.9 MB, 2026-09-05) | https://redmine.watermelon.vn/attachments/download/29951/%E9%80%95%EF%BD%BB%E9%AB%B1%EF%BD%A2%E8%9C%BF%E6%9C%B1%E9%B9%B8_20260904_1323_%E8%9D%A8%EF%BD%A7%E9%82%B5%EF%BD%AE.mp4 |

Link ngoài (từ description):
- Dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12067
- Tayori: https://tayori.com/admin/task/89c743d3bd52d35727579a0525c87a2ee8dcf543/
- Slack list item: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BUZLKFW59
- Slack thread: https://l-message.slack.com/archives/C0BALS7S73L/p1788567185332959?thread_ts=1788567185.332959&cid=C0BALS7S73L

## Ghi chú thêm của Leader

- **Ca lặp lại**: khách nêu rõ giống 【お問い合わせNo.11981】 → cần check ticket cũ đó đã fix/đóng chưa, tránh fix lặp hoặc regression quay lại.
- **Điều kiện tiên quyết để tái hiện** (từ journal #134108): friend info phải là **type select**, **có gắn action ở option**, và setting vận hành phải là **chạy action nhiều lần**; friend đã từng được gán giá trị trước đó (qua QR action / form) → cờ đã-chạy khác rỗng.
- ⚠️ **Fix đã đổi hành vi thấy được ở chế độ chạy MỘT LẦN** (Dev tự nêu ở mục TỰ REVIEW file 03): trước fix action chạy **lặp** mỗi lần sửa ở chat, sau fix chỉ chạy **đúng một lần**. Đây là siết theo spec nhưng là behavior change — TC regression phải cover.
- ⚠️ Dev **chưa chạy end-to-end** (MySQL dev không kết nối được), mới lint + đối chiếu spec → rủi ro cao, cần test thực tế kỹ.
