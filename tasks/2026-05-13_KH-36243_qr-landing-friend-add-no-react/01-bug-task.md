# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #36243 ngày 2026-05-13 (REST API fetch). Raw JSON: [_redmine-36243-raw.json](_redmine-36243-raw.json).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | KH #36243 (回答ID 10810) |
| Redmine URL | https://redmine.watermelon.vn/issues/36243 |
| Auto-filled | `2026-05-13 by /write-tc` (REST fetch) |
| Tracker / Category | Bug KH / QR Landing |
| Status | New |
| Priority (Redmine) | Normal |
| Parent issue | #36192 |
| Author | AI CSS (id 160) |
| Assignee | AI CSS (id 160) |
| Ngày báo cáo (created_on) | 2026-05-05 |
| Updated_on | 2026-05-13 |
| Khách hàng / Bot | User `t.fukushima@hashtag.ne.jp` — Bot `HASH HACK` |
| Module / Màn hình | QR Landing → màn add friend (LIFF callback / friend-add button) |
| Môi trường phát hiện | Production (KH report) — đã reproduce trên staging (xem journal #117754) |

## Mô tả bug (nguyên văn description từ Redmine)

> **Subject:** [05-05-2026][10810][QR Landing] 2 case khách báo 'friend-add button không react' (1 case khi add qua QRCA) — confirm có phải bug LINE không?

```
User: t.fukushima@hashtag.ne.jp
Bot Name: HASH HACK

Có **2 case** khách báo: button `友だち追加` (add friend) không react khi tap.

→ Khách hỏi: đây có phải vấn đề từ phía LINE không?

**Chi tiết:**
- Trong 2 case, **1 case** xảy ra khi user **add friend mới qua QR Code Action (QRCA)** — friend-add button không react.

Cần team check / điều tra giùm xem có phải bug LME / QRCA hay là vấn đề LINE-side.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B16FTDV1V
```

### 原文 (JP)

```
友だち追加ボタンが反応しないとのお問い合わせが2件届いていますが、こちらはLINE側の問題でしょうか？
1件はQRコードアクション経由の新規友だち追加時に友だち追加ボタンが反応しないとのことです。
```

TaskRef: `user_report:Rec0B16FTDV1V`

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — đã đọc lại Redmine 36243 (description + 5 journals + 3 attachments) và xác nhận:
  - Description match nguyên văn customer report
  - Steps to reproduce + dev impact (journal #118286) đầy đủ
  - 3 ảnh attachment đã được kiểm tra (id 25623, 25630, 25631)
  - Thông tin LINE Android version 26.6.0/26.6.1 đã đối chiếu LINE Developers news (journal #117779)
  - Không bỏ sót journal nào

## Steps to reproduce (theo journal #118286 — Ngần)

1. Dùng **device Android** (LINE version 26.6.0 hoặc 26.6.1)
2. Quét QR landing để add friend (URL ví dụ: `https://go.lmes.jp/landing-qr/2002341759-JRn2awBD?uLand=7nUI4Q` — từ journal #117754)
3. Tại màn landing, **tap button `友だち追加` (Add Friend)**

## Expected result

- Button `友だち追加` **react ngay khi tap** → chuyển sang flow add friend của LINE
- Friend được add vào bot LINE Official Account
- Hệ thống LME ghi nhận friend mới (qua webhook / LIFF callback)

## Actual result

- Button `友だち追加` **không phản hồi** khi tap trên Android
- Reproduce được trên **2 bot khác nhau cùng môi trường staging** (journal #117754): friend `道下裕希` ở bot `エルメサポート` tap button kết bạn của bot `エルグラムサポート` → không phản hồi
- KH report (journal #117733): user `佐々木繭美` không thể đăng ký qua QRCA từ tài khoản `小川直美｜虹色つまみアーティスト` — đối tượng ảnh hưởng: **toàn bộ 3 QR Code Action**

## Root cause (LINE-side context — journal #117779)

- Từ kỳ nghỉ Golden Week (~2026-04-29), số report tăng trên Android.
- **LINE Android 26.6.0 / 26.6.1** support **edge-to-edge** (từ 26.3.0 trở đi) → các nút bottom của LIFF app / LINE Mini App bị **chồng lên vùng navigation bar** → tap không phản hồi.
- LINE 15.13.1 / 15.15.1 (iOS) **không reproduce được**.
- LINE Developers thông báo: https://developers.line.biz/ja/news/2026/05/11/liff-outage/
- Đối thủ L Step đã fix; UTAGE chưa fix (theo KH journal #117858).

## Ảnh / video / log đính kèm

- [x] Có screenshot — 3 file:
  - [25623 — Screenshot KH (Ngọc Ánh upload 2026-05-07)](https://redmine.watermelon.vn/attachments/download/25623/____________________________2026-05-06_140120__1_.png) (162 KB)
  - [25630 — Photo từ device Android (Ngần upload 2026-05-07)](https://redmine.watermelon.vn/attachments/download/25630/image_1101517_612410512948330582_1777856416091.jpg) (74 KB)
  - [25631 — SnapCrab repro staging (Ngần upload 2026-05-07)](https://redmine.watermelon.vn/attachments/download/25631/SnapCrab_NoName_2026-5-7_14-40-2_No-00.png) (95 KB)
- [ ] Có video
- [x] Có URL reproduce staging — `https://go.lmes.jp/landing-qr/2002341759-JRn2awBD?uLand=7nUI4Q`

## Journals (full timeline)

| ID | Người | Thời gian | Nội dung |
|---|---|---|---|
| 117733 | Ngọc Ánh | 2026-05-07 03:53 | KH bổ sung: `kamine@xross-skill.com` (小川直美｜受講生専用LINE), đối tượng = toàn bộ 3 QR Code Action. User `佐々木繭美` không đăng ký được qua QRCA |
| 117754 | Ngô Thúy Ngần | 2026-05-07 07:30 | Reproduce trên staging: friend `道下裕希` ở bot `エルメサポート` tap button kết bạn `エルグラムサポート` → không phản hồi. URL repro: `https://go.lmes.jp/landing-qr/2002341759-JRn2awBD?uLand=7nUI4Q` |
| 117779 | Ngọc Ánh | 2026-05-08 02:17 | **LINE-side root cause confirmed**: LINE Android 26.6.0/26.6.1 edge-to-edge → nút bottom chồng navigation bar. LINE 15.13.1/15.15.1 không reproduce. LINE Developers đã announce |
| 117858 | Ngọc Ánh | 2026-05-11 08:15 | KH so sánh: L Step đã fix; UTAGE chưa. Hỏi WSS có đối ứng nào không. Link LINE news: https://developers.line.biz/ja/news/2026/05/11/liff-outage/ |
| 118286 | Ngô Thúy Ngần | 2026-05-13 10:56 | **Dev impact**: root cause "liff và mini app đang lỗi" trên Android. Fix: check liff login của liff app khi mở trên Android. Function impact: `resources/views/liff_callback.blade.php`. Sheet TCs row 3452-3494 |

## Ghi chú thêm của Leader

- **Bug hybrid LINE-side + LME-side**: LINE đã announce vấn đề (edge-to-edge support trong Android 26.3.0+) → root cause **không thuộc về LME**, nhưng LME vẫn cần workaround vì:
  - L Step (đối thủ) đã fix được → KH so sánh và pressure WSS phải fix.
  - LIFF callback của LME có thể adjust để tránh vùng navigation bar bị che.
- **Dev report sơ sài** (journal #118286): mới chỉ note `check liff login của liff app khi mở trên Android` + 1 file `liff_callback.blade.php`. Chưa nói rõ:
  - Logic check là gì (detect Android version? detect LIFF version? fallback nào?)
  - Behavior change UI/UX trên Android cụ thể (move button lên trên? thêm padding bottom?)
- **Câu hỏi mở cho Leader / dev verify:**
  - Fix có cover cả 3 use case không: (a) add friend qua QRCA, (b) add friend qua LINE OA profile page button, (c) add friend qua landing QR thông thường?
  - iOS có bị ảnh hưởng không (theo LINE thì không, nhưng cần regression test)?
  - LINE Android version cụ thể nào bị (chỉ 26.6.0/26.6.1, hay tất cả 26.3.0+)?
  - Member đã viết TCs sẵn ở [Google Sheet rows 3452-3494](https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763) — cần convert sang `04-tc-list.md` để review.
