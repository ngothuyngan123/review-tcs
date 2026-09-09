# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38765 — [07-07-2026][QR Landing] Đề xuất: URL không hợp lệ của 「s.lmes.jp」 nên hiện trang báo link lỗi thay vì redirect về màn hình login` |
| Module / Màn hình | `QR Landing (category Redmine) — trang lỗi trên domain public rút gọn/QR 「s.lmes.jp」; vòng fix mới nhất mở rộng sang 「sl.lmes.jp」 (short link) + 「form.lmes.jp」 (form)` |

## Mô tả bug (bản dịch tiếng Việt)

> Tracker Redmine = **SpecImprove** (đề xuất cải tiến spec), không phải bug tái hiện được theo format thường.

Tên gốc: エルメURLのログイン画面リダイレクト修正

User:
Bot Name:

Đây là phần xác nhận về spec của 「https://s.lmes.jp/」 của LME.

Hiện tại, khi truy cập URL có gắn thêm chuỗi không hợp lệ phía sau như 「https://s.lmes.jp/test」, hệ thống tự động redirect về 「https://s.lmes.jp/」 và hiển thị màn hình đăng nhập của LME.

Với spec này, khi người dùng LME gửi URL của QR code action (QRコードアクション) cho friend mà lỡ làm hỏng URL, thì phía friend sẽ thấy màn hình đăng nhập của LME, gây nhầm lẫn trong một số trường hợp.

Vì vậy, tôi nghĩ khi truy cập URL không hợp lệ thì không nên redirect về 「https://s.lmes.jp/」, mà nên hiển thị một trang hướng dẫn với nội dung kiểu 「このリンクは無効です」 (link này không hợp lệ).

Không biết về việc này thì thế nào ạ?

Link thread: (không có)
Link item: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BFGM2L26A?record_id=Rec0BFFDQDUF7

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" riêng → để trống theo quy tắc /new-task. Thao tác tái hiện nằm ngay trong phần Mô tả bug ở trên. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/28951/photo_2026-08-07_17-12-31.jpg — đính kèm bởi Ngọc Ánh 2026-08-10, là **design chốt của trang lỗi**.

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được theo format Redmine chuẩn** — ticket là **SpecImprove** (đề xuất đổi spec), không có section "Tái hiện bug" và không có section "Đánh giá ảnh hưởng" trong description. Root cause + cách fix do **AI Auto-fixbug** cung cấp qua journal (đã trích vào `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.
- ⚠️ **Spec đã đổi giữa chừng — 2 vòng fix, expected KHÁC nhau**:
  - Vòng 1 (journal 2026-07-16, commit `9234b77f8d`): text 「このリンクは無効です」, chỉ áp cho **1 domain** suy từ `URL_OUTSIDE_STEP`.
  - Vòng 3 (journal 2026-08-20, commit `d8cbf9c4b7`, theo spec bổ sung của human 20/08): text 「お探しのページが見つかりませんでした。」, áp cho **đúng 3 domain public** `s.lmes.jp` / `sl.lmes.jp` / `form.lmes.jp`.
  - **Chốt design của BA** (journal 2026-08-10 — Ngọc Ánh): trang **CHỈ có 1 dòng** 「お探しのページが見つかりませんでした。」, **bỏ dòng text phía dưới** — tức bỏ 「下記のボタンより、TOPページへお戻りください。」 và nút 「TOPページへ戻る」.
  - → **Expected hiện hành = vòng 3 + design BA.** TC nào còn dùng text 「このリンクは無効です」 là bám spec CŨ.
- Điều kiện tiên quyết dựng env test: `APP_DEBUG=false` (guard chỉ chạy khi tắt chế độ gỡ lỗi; nếu đã cache config thì phải xoá cache), và phải trỏ hostname `s.lmes.jp` / `sl.lmes.jp` / `form.lmes.jp` về server test qua file `hosts` mới mở được bằng trình duyệt.
- Env liên quan: `URL_OUTSIDE_STEP`, `URL_OUTSIDE_STEP_V2`, `INVALID_LINK_DOMAINS`. Khai `INVALID_LINK_DOMAINS` sẽ **thay thế toàn bộ** danh sách mặc định → rủi ro mất tính năng nếu khai thiếu ở môi trường thật.
- Domain quản trị (`step.lme.jp`) **giữ nguyên hành vi cũ** (redirect về màn đăng nhập) — đây là vùng regression bắt buộc.
- ⚠️ **Ticket từng bị auto-close nhầm** (journal 2026-08-21: Fix done → Closed để khớp Slack List), sau đó Ngô Thúy Ngần **mở lại về `New`** ngày 2026-09-07 kèm gán fixed_version. Trạng thái hiện tại: **New** · assignee **Kim Cúc** · Commit Date `2026-08-20`.

## Journal / note từ Redmine (nguyên văn)

**Journal #126457 — AI LME Fix bug — 2026-07-16:** *(vòng 1 — status → Fix done, Commit Date 2026-07-16)*

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Trên domain rút gọn/QR (s.lmes.jp), URL không khớp route nào (vd /test) khiến Laravel ném NotFoundHttpException. Bộ xử lý ngoại lệ toàn cục, với người chưa đăng nhập, lại redirect về trang gốc / — chính là màn đăng nhập LME, gây nhầm lẫn cho friend nhận link QR bị hỏng.

■ 2. CÁCH FIX
Thêm trang lỗi thân thiện errors/invalid_link.blade.php (「このリンクは無効です」) và bổ sung guard trong Exception Handler: khi request thuộc domain QR/rút gọn (host khớp URL_OUTSIDE_STEP) và lỗi thuộc nhóm không tìm thấy (NotFound/ModelNotFound/MethodNotAllowed/404) thì trả trang này với HTTP 404, thay vì redirect về màn đăng nhập. Domain quản trị chính giữ nguyên hành vi cũ.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Handler::render (app/Exceptions/Handler.php)
Handler::isQrLandingDomain (app/Exceptions/Handler.php)
Handler::isNotFoundLikeException (app/Exceptions/Handler.php)
errors/invalid_link.blade.php (resources/views/errors)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Exceptions/Handler.php
   - resources/views/errors/invalid_link.blade.php
 • 4.2 Data ảnh hưởng:
   - Không có
 • 4.3 Tính năng liên quan:
   - QR Code Action / Landing (FA-017) — URL không hợp lệ trên domain rút gọn s.lmes.jp hiện trang báo link lỗi thay vì màn đăng nhập

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Exceptions/Handler.php: No syntax errors; blade view mới không cần lint runtime
   Bằng chứng: Guard đặt TRƯỚC mọi nhánh redirect(/) trong Handler nên chặn hết case not-found trên domain QR

■ TỰ REVIEW (AI)
Guard domain-aware đặt sau khối JSON (API vẫn trả JSON) và trước mọi nhánh redirect(/) nên bắt trọn NotFound/404 trên domain QR. Fallback an toàn: URL_OUTSIDE_STEP rỗng → trả false → giữ hành vi cũ. Không đụng DB, không đụng hot path click-tracking.
 • Rủi ro / lưu ý khi test:
   - Nếu URL_OUTSIDE_STEP không phải s.lmes.jp trong 1 môi trường nào đó thì cần kiểm lại giá trị env; hiện code build URL QR đều dùng env này nên đồng nhất

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38765 (nhánh gốc release_step_20260623, commit 9234b77f8d, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 44 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=8f3c6825-26e3-434a-8431-84473e52c9a7
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38765
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #128409 — Ngô Thúy Ngần — 2026-08-07:**

```
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BC36RSQBF?record_id=Rec0BFF8M1B44
```

**Journal #128587 — Ngọc Ánh — 2026-08-10:** *(chốt design — đính kèm `photo_2026-08-07_17-12-31.jpg`)*

```
Design: Chỉ có text お探しのページが見つかりませんでした, bỏ phnaf text dòng dưới
```

**Journal #130769 — AI LME Fix bug — 2026-08-20:** *(vòng 3 — Commit Date 2026-07-16 → 2026-08-20)*

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Trên domain rút gọn/QR (s.lmes.jp), URL không khớp route nào (vd /test) khiến Laravel ném NotFoundHttpException. Bộ xử lý ngoại lệ toàn cục, với người chưa đăng nhập, lại redirect về trang gốc / — chính là màn đăng nhập LME, gây nhầm lẫn cho friend nhận link QR bị hỏng.

■ 2. CÁCH FIX
Vòng 3 (spec bổ sung của human 20/08): rule hiện trang お探しのページが見つかりませんでした。 áp cho ĐÚNG 3 domain public s.lmes.jp (QR/rút gọn), sl.lmes.jp (short link), form.lmes.jp (form); mọi domain khác kể cả domain quản trị giữ nguyên hành vi cũ (redirect về màn đăng nhập). Thay Handler::isQrLandingDomain (chỉ so 1 host từ URL_OUTSIDE_STEP) bằng isInvalidLinkDomain + invalidLinkDomains: danh sách mặc định 3 host + host suy ra từ URL_OUTSIDE_STEP/URL_OUTSIDE_STEP_V2 cho staging, override toàn bộ bằng env INVALID_LINK_DOMAINS. So khớp host chính xác, không phân biệt hoa thường. Verify: php -l + test 15 case khớp/không khớp domain đều đúng. Commit d8cbf9c4b7 (chưa push).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Handler::render (app/Exceptions/Handler.php)
Handler::isQrLandingDomain (app/Exceptions/Handler.php)
Handler::isNotFoundLikeException (app/Exceptions/Handler.php)
errors/invalid_link.blade.php (resources/views/errors)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Exceptions/Handler.php
   - resources/views/errors/invalid_link.blade.php
 • 4.2 Data ảnh hưởng:
   - Không có
 • 4.3 Tính năng liên quan:
   - QR Code Action / Landing (FA-017) — URL không hợp lệ trên domain rút gọn s.lmes.jp hiện trang báo link lỗi thay vì màn đăng nhập

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Exceptions/Handler.php: No syntax errors; blade view mới không cần lint runtime
   Bằng chứng: Guard đặt TRƯỚC mọi nhánh redirect(/) trong Handler nên chặn hết case not-found trên domain QR

■ TỰ REVIEW (AI)
Guard domain-aware đặt sau khối JSON (API vẫn trả JSON) và trước mọi nhánh redirect(/) nên bắt trọn NotFound/404 trên domain QR. Fallback an toàn: URL_OUTSIDE_STEP rỗng → trả false → giữ hành vi cũ. Không đụng DB, không đụng hot path click-tracking.
 • Rủi ro / lưu ý khi test:
   - Nếu URL_OUTSIDE_STEP không phải s.lmes.jp trong 1 môi trường nào đó thì cần kiểm lại giá trị env; hiện code build URL QR đều dùng env này nên đồng nhất

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38765 (nhánh gốc release_step_20260623, commit d8cbf9c4b7, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 44 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=17aedce7-ab50-4bd7-b23c-f6a6d374a38a
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38765
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #132150 — AI bug detect Lme — 2026-08-21:** *(auto-close — đã bị mở lại ngày 2026-09-07)*

```
Auto-close (rà soát subtask OPEN dưới parent 「CHECK REPORT FROM CUSTOMER」 ⇄ Slack List CS, 2026-08-21 JST):
Task tương ứng trên Slack List đã ở trạng thái ĐÓNG — CH2 wssj_check (archived): 対応ステータス =「クローズ待ち」.
Redmine vẫn còn open (Fix done - Đợi test) nên đóng lại cho khớp trạng thái Slack. Nếu vẫn còn việc phải xử lý, mở lại ticket và cập nhật status trên Slack List.
```
