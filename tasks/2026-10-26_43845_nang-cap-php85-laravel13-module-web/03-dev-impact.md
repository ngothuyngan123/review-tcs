# 03 — Đánh giá ảnh hưởng từ Dev

⚠️ **Ticket #43845 KHÔNG có section "Đánh giá ảnh hưởng" theo format chuẩn 4 mục (1. Nguyên nhân / 2. Cách fix / 3. Caller đã check / 4.1-4.3)** — đây là epic nâng cấp hạ tầng (Laravel 5.5→13, PHP 7.2→8.5) cho **toàn module PHP Web**, chia 21 task con, chạy 16 bàn giao tích hợp ở task cha. Nội dung dưới đây được tổng hợp từ:
1. Section "Quyết định đã chốt" (F-1…F-16) + "Thành phần dùng chung" (S-1…S-9) trong Redmine #43845.
2. `dev_impact` đã gộp của **MCP LME TEST STUDIO task #507** (bàn giao #16 — mới nhất, cập nhật 2026-10-25 19:04).

Do phạm vi đổi **1374 file trong 1 lần deploy**, mục 4.1/4.2/4.3 dưới đây là **DANH MỤC theo nhóm/khu vực**, không phải liệt kê từng function/data đơn lẻ (không khả thi ở quy mô này). Leader cần đọc kèm 2 attachment HTML gốc nếu cần chi tiết function-level.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (agent pipeline, không phải 1 dev người cụ thể) |
| Commit / Pull Request | `<không có link PR Github/Gitlab — chạy trong Dev Studio runner>`. Base code gộp qua nhiều commit: `6c09713530` (mốc chia task), `303a131b9c`, `787782ba56` (#43562), `2b83b02a8a`, `6f9eaac2ba`, ... (xem journal #43845 đầy đủ) |
| Branch | `release_step_20260930_v2` (base) → `ai_studio_implement_43845` (branch Studio task #507) |
| Ngày submit đánh giá | `2026-10-25` (bàn giao #16, cập nhật Studio) — ticket vẫn đang chạy tiếp (status Redmine: Đang fix) |
| Auto-filled | `2026-10-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ KHÔNG tick cho tới khi Leader đọc + xác nhận: do input không theo format chuẩn, bảng 4.1/4.2/4.3 dưới đây là tổng hợp ở mức NHÓM, rủi ro sót function/data cụ thể cao hơn ticket bug thông thường.

---

## 1. Nguyên nhân

<!-- Không phải "nguyên nhân bug" — là lý do cần nâng cấp, theo báo cáo scan đính kèm. -->

Module PHP Web (sns-line) đang chạy Laravel 5.5 / PHP 7.2 — các bản này hết hỗ trợ bảo mật, chặn nâng cấp thư viện (LINE SDK, Stripe, Google, xử lý ảnh, mail...). Báo cáo scan `upgrade-php85-laravel13-report.html` (quét nhánh `release_step_20260930_v2`, mã P1–P9/L1–L12) liệt kê các điểm không tương thích PHP 8.5 + Laravel 13 cần xử lý. Kế hoạch chia task bổ sung 22 điểm scan còn thiếu (G-1…G-22).

## 2. Cách fix

<!-- Chiến lược migrate — quyết định đã chốt 22/10/2026 (F-1…F-16), raw. -->

- **F-1** Một sprint, nhảy thẳng Laravel 5.5 → 13, PHP 7.2 → 8.5; **một lần deploy** production (không đổi dần).
- **F-2/F-3** Base `release_step_20260930_v2`, merge base mỗi khi có nhánh release mới; không phát hành sớm phần làm trên nền cũ (T2–T7).
- **F-4** `composer.lock` production (140 package) làm mốc — T1 bỏ khỏi `.gitignore` + commit; T8 nâng từ đó + commit lock mới. Production: LINE SDK 7.6.1, webpush 3.0.0 (KHÔNG phải 3.6.0/5.1.1 như báo cáo scan ghi sai); KHÔNG có PayPal Merchant SDK, payjp.
- **F-5** Nâng mọi gói cần nâng (LINE SDK → v12, Intervention Image → v3, Stripe → bản mới) — giữ hành vi, ưu tiên bản ít đổi API nhất.
- **F-6** Lỗi có sẵn từ trước: sửa luôn nếu không đổi spec; đổi spec/hành vi → giữ nguyên + ghi `docs/upgrade/pre-existing-bugs.md` (PB-n: file:dòng, hiện tượng, vì sao giữ, đề xuất sửa) → gom ticket riêng cuối sprint.
- **F-7** Stripe: nâng `stripe-php` mới nhất, API version mặc định SDK; sửa code theo response/param đổi để kết quả người dùng như cũ. Account Stripe đổi API version + webhook endpoint lúc deploy (ghi `deploy-notes.md`).
- **F-8** PayPal Merchant SDK / payjp không có trong production → code liên quan hiện lỗi khi chạy tới: giữ nguyên (không thêm package), ghi `pre-existing-bugs.md`; route payjp không còn đường tới → xoá.
- **F-9** Màn dùng Laravel Collective (T7): còn route/include → viết lại HTML thuần giữ đúng HTML + param form như cũ; không còn đường tới → xoá.
- **F-10** `catch (Exception)` → `Throwable` theo vùng (T19–T21), ưu tiên nhánh "ghi log rồi chạy tiếp"; không đổi hàng loạt.
- **F-11** Migration đã chạy production (`->change()`, `float(x,y)`) KHÔNG sửa; migration mới khai đủ modifier, tiền dùng decimal.
- **F-12** Mọi phiên đăng nhập cũ **hết hiệu lực sau deploy** (đổi cookie serialization 5.6.30) — chấp nhận, báo trước người dùng.
- **F-13** 21 task con không bàn giao riêng/không gửi Test Studio riêng — task cha gộp bản review đạt, review tích hợp, bàn giao 1 lần + regression đầy đủ + Test Studio.
- **F-14** Dev/review không cần staging (agent build/test trong runner Dev Studio PHP 8.5); staging/production cho QA là việc hậu bàn giao, không chặn sprint.
- **F-15** Lwaka, Saruwaka (dùng chung repo sns-line) **không** nâng trong sprint này.
- **F-16** 3 controller Auth không có route (`RegisterController`, `ForgotPasswordController`, `ResetPasswordController`) → xoá, không cài `laravel/ui`.

**Thành phần dùng chung (S-1…S-9)** — ảnh hưởng nhiều task con, risk tập trung:
- S-3 Trait `LegacyDateSerialization` (T5 làm; T9, T19–T21 dùng) — ngày giờ JSON.
- S-5 `config/hashing.php` (bcrypt 10 vòng, không rehash khi login — T8 làm; T10 dùng).
- S-8 `App\Services\Line\LineMessagingGateway` trên LINE SDK v12 (T16 làm; T17, T18 dùng).
- S-9 Mốc request LINE (body JSON SDK cũ) + mốc xử lý ảnh (T1 ghi; T15/T16/T17 so khớp).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- "Caller đã check" ở mức epic này = quy ước test bắt buộc cho mọi task con, không phải list caller function đơn lẻ. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `tools/upgrade/` (bộ quét, S-1) | T1 làm, mọi task con dùng để chứng minh hạng mục còn 0 | Đảm bảo không sót điểm scan P1-P9/L1-L12/G-1…G-22 |
| 2 | Test đặc tả hành vi cũ (S-2) | T1 làm, mọi task dùng — khoá **kết quả phía người dùng**, không khoá cách cài đặt | Cho phép viết lại logic rối nhưng giữ output |
| 3 | Mọi lớp tương thích dùng chung (URL sinh route, query builder orWhere mảng, exception, ngày giờ/Carbon, phân trang) | Thêm lớp compat thay vì sửa từng điểm gọi | Giảm diện sửa, nhưng tập trung rủi ro nếu lớp compat sai |
| 4 | `docs/upgrade/progress.md` / `deploy-notes.md` / `pre-existing-bugs.md` / `smoke-list.md` (S-7) | Mọi task con ghi | Theo dõi tiến độ + biến `.env`/bước deploy mới + lỗi có sẵn giữ nguyên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng (theo NHÓM — xem lưu ý đầu file)

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Sinh URL (`route()`) qua lớp tương thích mới | nhiều file (35+ lời gọi tên param lệch, vd `id` thay `bot_id`) | Direct | Laravel 5.5 tự điền ô trống tên param lệch, Laravel 13 ném lỗi → redirect loop nếu không có lớp compat (journal #147368) |
| F2 | Query builder — `where`/`orWhere` nhận mảng điều kiện lồng | お知らせ, salon/lesson/event booking overlap check, đếm bạn bè, duyệt hàng loạt lịch | Direct | Đổi cách nối điều kiện giữa Laravel 5.5 và 13; đã thêm lớp compat nối lại như production |
| F3 | Error handling: `catch (Exception)` → `Throwable`; JSON ajax lỗi (404/405/413/503); trang lỗi 503/419/429/4xx | T19–T21 vùng runtime PHP8 | Direct/Indirect | Message rỗng như production; trang bảo trì giữ view như cũ |
| F4 | Ngày giờ: cache TTL, `$dates`, JSON ngày, `Carbon::diffIn*()` | Trait `LegacyDateSerialization` (S-3) | Direct | T5/T6 làm; T9, T19–T21 dùng — ngày đặt lịch màn đổi bot giữ dạng chuỗi `Y-m-d H:i:s` như production |
| F5 | Thanh toán: Stripe v22 / UnivaPay Guzzle 7; booking sự kiện LIFF thanh toán trước (3DS) | `MobileEventBookingController`, Stripe webhook | Direct | Xác thực 3DS xong mới chốt đơn + gửi 1 tin hoàn tất; lần gọi lại sai booking/PI chưa succeeded/không phải Stripe → chặn, không ghi DB |
| F6 | LINE SDK v12 — gateway (`LineMessagingGateway`, S-8) + message builder + webhook signature | T16/T17/T18; webhook `/line/callback/add/{bot_id}` | Direct | Thiếu/sai `X-Line-Signature` → 401 không lưu; đúng → 200 lưu; bot không map (ví dụ "Olioa") → 403 |
| F7 | Chat realtime (1:1, チャット管理, chat nhóm, web mobile chat/list-notify) — socket JWT | `/ajax/chat/socket-token`, `/api/mobile/socket/token`, `node_serve` | Direct | Token chỉ phát khi user còn quyền với bot; app cũ đi vào `legacy_client` |
| F8 | Đặt chỗ/đổi lịch sự kiện — giới hạn số lượng, binding SQL | `MobileEventBookingController::handleKeepSlot`, LIFF | Direct | Số lượng phải nguyên trong `1…「1回の予約上限」`; đã vá binding SQL |
| F9 | Auto-reply — binding SQL text/id | `HandleCallbackMessage` | Direct | Vá SQL injection trong text tin nhắn / `auto_reply` id |
| F10 | Xử lý ảnh — Intervention Image v3 | mốc xử lý ảnh (S-9) | Direct | T15 làm; T16/T17 so khớp mốc |
| F11 | Export/import — CSV quản lý (tải file), Excel 4, Google apiclient | CSV管理, アフィリエイター管理/代理店 CSV | Direct | Đã vá lỗi tải CSV lỗi + IDOR CSV quản lý (tải file tuỳ ý, #44186) |
| F12 | Mail — Symfony Mailer; web push | gửi mail, web push | Direct | Nâng theo F-5 |
| F13 | Phân trang — lớp tương thích đếm phân trang dùng chung | web mobile, 解約一覧, affiliate, API app mobile/MCP có phân trang (kết quả form, thông báo, chat, danh sách bạn bè), danh sách ajax web | Direct | Đếm/phân trang theo nhóm từng sai ở nhiều vòng bàn giao (#147583, #147736...) |
| F14 | Phiên đăng nhập — cookie serialization, hashing (`config/hashing.php`, S-5) | T8/T10 | Direct | bcrypt 10 vòng, không rehash khi login; mọi session cũ hết hiệu lực sau deploy (F-12) |
| F15 | Bảo mật đã vá trong sprint (IDOR + SSRF) | CSV quản lý/friend info/tag/rich menu/image rich menu/scenario/cross analysis/broadcast/action schedule/template V2/Action (IDOR); chat/MCP/API liên kết (SSRF); 4 route Telecom không xác thực (gỡ); 3 header admin bỏ khối socket chết | Direct | Vá kèm theo sprint nâng cấp, không phải mục tiêu chính nhưng **phải regression riêng** vì đổi hành vi cho phép/chặn |
| F16 | 3 controller Auth không route (`RegisterController`, `ForgotPasswordController`, `ResetPasswordController`) | xoá hẳn, không cài `laravel/ui` | Direct | F-16 — xác nhận thật sự không còn route trước khi review |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `composer.lock` | UPDATE (bỏ khỏi `.gitignore`, chốt làm mốc T1, T8 nâng + commit lock mới) | 140 package, khớp production |
| D2 | Session / cookie (serialization `php`, `APP_KEY`, tên cookie phiên) | UPDATE (đổi serialization 5.6.30) | **Mọi phiên đăng nhập cũ hết hiệu lực sau deploy** (F-12) — cần báo trước người dùng |
| D3 | Cache (prefix `laravel`), Redis không prefix (kênh `message`, `source_message`) | giữ nguyên giá trị đang dùng, không chép config mẫu Laravel mới | Node_serve subscribe đúng kênh cũ |
| D4 | Migration mới (field tiền → decimal, modifier đầy đủ) | CREATE (migration mới) — migration cũ đã chạy production KHÔNG sửa | `schema:dump` để sau (F-11) |
| D5 | `docs/upgrade/*.md` (progress, deploy-notes, pre-existing-bugs, smoke-list, deploy.md) | CREATE/UPDATE | Không phải data user, nhưng là nguồn tra PB-n (lỗi có sẵn giữ nguyên) + smoke-list quy định phạm vi regression |
| D6 | `.env` / extension PHP 8.5 (sockets, imagick, bcmath, gmp, intl, gd, zip, exif, redis) | UPDATE (hạ tầng, lúc deploy) | Theo runbook `docs/upgrade/deploy.md`; KHÔNG bật `config:cache`/`optimize` (2.381 lời gọi `env()` ngoài thư mục config) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Toàn bộ màn `/basic`, `/admin`, web mobile (chọn bot, phân trang, session) | F1, F13, F14, D2 | High |
| T2 | Thanh toán & bán hàng V2 (Stripe 3DS, subscription, booking sự kiện có thanh toán trước) | F5 | High |
| T3 | Đặt lịch Salon/Lesson/Event — booking management, overlap check ca nhân viên, giới hạn số lượng | F2, F8 | High |
| T4 | LINE integration — webhook, chat realtime (1:1/group/web mobile), auto-reply, rich menu, scenario, broadcast | F6, F7, F9 | High |
| T5 | Quản lý bạn bè & tag — filter, folder, sort, cross analysis, CSV quản lý/export | F11, F15 | High |
| T6 | Báo cáo/thống kê — 月次売上, 解約一覧, CSV affiliate | F13 | Medium-High |
| T7 | API app mobile & API MCP (phân trang, filter) | F13, F15 | High |
| T8 | Bảo mật — IDOR loạt màn quản lý, SSRF, chữ ký webhook LINE, route Telecom | F15 | High (security regression — ưu tiên) |
| T9 | Form đăng ký web mobile, trang lỗi/bảo trì (503/419/429/4xx) | F3 | Medium |
| T10 | Toàn bộ job nền / queue / cron của module web | F1–F15 (framework-wide) | High — chưa test trên staging/production tại thời điểm fetch (2026-10-26) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — ⚠️ không có link PR cụ thể, chỉ có branch/commit base
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ ở epic này là quy ước test, không phải list caller
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ liệt kê theo NHÓM, Leader cân nhắc có cần chi tiết hơn từng khu vực không
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ **Riêng mục này cho ticket epic**: xác nhận có nên tách review theo từng mảng lớn (T1…T10 ở 4.3) thay vì review 1537 TC một lần
