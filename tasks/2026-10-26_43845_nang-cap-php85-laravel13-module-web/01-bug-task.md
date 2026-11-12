# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43845 — Nâng cấp module PHP Web lên PHP 8.5 + Laravel 13` |
| Module / Màn hình | `Toàn bộ module PHP Web (sns-line) — KHÔNG phải 1 màn/feature cụ thể` |

⚠️ **Ticket này KHÔNG phải bug thông thường** — là **epic/parent ticket** cho 1 sprint nâng cấp hạ tầng (Laravel 5.5 → 13, PHP 7.2 → 8.5) trong một lần release, không đổi spec. Không có section "Tái hiện bug" trong Redmine (không áp dụng — không phải bug tái hiện được từ hành vi lỗi, mà là thay đổi hạ tầng có chủ đích). Steps/Expected/Actual bên dưới để trống.

**21 task con đã tạo sẵn** (chạy song song theo lane, dependency "làm sau"): #43846 T1 Mốc hành vi và bộ quét → #43866 T21 Rà runtime PHP 8 (màn quản trị, chat, phần còn lại). Task cha #43845 gộp bản review đạt của 21 task con, review tích hợp, rồi bàn giao một lần + regression đầy đủ + Test Studio (quyết định F-13).

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine đã ở tiếng Việt — giữ nguyên văn, không diễn giải lại. -->

Nâng module PHP Web (sns-line) của LME từ Laravel 5.5 / PHP 7.2 lên Laravel 13 / PHP 8.5 trong một lần release. Hệ thống phải chạy ổn định trên bản mới, không đổi spec: người dùng cuối thấy và nhận được kết quả như cũ; logic bên trong được phép viết lại đơn giản hơn.

**Tài liệu đính kèm** (xem mục Ảnh/log bên dưới):
- Báo cáo scan `upgrade-php85-laravel13-report.html` — quét nhánh `release_step_20260930_v2` ngày 22/10/2026. Mã P1–P9, L1–L12 và mục §x được ticket + task con trỏ vào.
- Kế hoạch chia task `chia-task-nang-cap-lme.html` — 21 task con, 22 điểm scan còn thiếu (G-1…G-22, đối chiếu commit `6c09713530`), quyết định + cài đặt Dev Studio cho sprint.

**Quyết định đã chốt (22/10/2026)** — raw, tham chiếu khi viết/review TC (đầy đủ ở `03-dev-impact.md`):
- F-1 Một sprint, nhảy thẳng Laravel 5.5 → 13, PHP 7.2 → 8.5; một lần deploy production.
- F-4 composer.lock production (140 package) là mốc; production chạy LINE SDK 7.6.1, webpush 3.0.0 — **không** có PayPal Merchant SDK / payjp.
- F-6 Lỗi có sẵn từ trước: sửa luôn nếu không đổi spec; nếu đổi spec/hành vi thì giữ nguyên + ghi `docs/upgrade/pre-existing-bugs.md` (PB-n), gom ticket riêng cuối sprint.
- F-7 Stripe nâng lên stripe-php mới nhất, API version mặc định SDK — sửa code theo response/param đổi, giữ kết quả người dùng như cũ.
- F-8 PayPal Merchant SDK / payjp không có trong production → code liên quan hiện lỗi khi chạy tới; giữ nguyên (không thêm package), ghi `pre-existing-bugs.md`; route payjp không còn đường tới thì xoá.
- F-9 Màn dùng Laravel Collective (T7): còn route/include → viết lại HTML thuần giữ đúng HTML + param form như cũ; không còn đường tới → xoá.
- F-12 Mọi phiên đăng nhập cũ **hết hiệu lực sau deploy** (đổi cookie serialization) — chấp nhận, báo trước người dùng.
- F-15 Lwaka, Saruwaka (dùng chung repo sns-line) **không** nâng trong sprint này.
- F-16 3 controller Auth (`RegisterController`, `ForgotPasswordController`, `ResetPasswordController`) không có route → xoá, không cài `laravel/ui`.

## Steps to reproduce

<!-- Không áp dụng — không phải bug tái hiện được, là thay đổi hạ tầng có chủ đích. -->

## Expected result

- Hành vi/kết quả phía người dùng cuối (màn hình, dữ liệu lưu/hiển thị, tin LINE, mail, file xuất, API/JSON trả ra, thứ tự hiển thị) **giữ nguyên như production Laravel 5.5 / PHP 7.2**, trừ các điểm đã chốt thay đổi có chủ đích ở F-6/F-7/F-8/F-9/F-12/F-16 và các bản sửa lỗi có sẵn (PB-n) được Leader duyệt.

## Actual result

<!-- Không áp dụng ở mức ticket cha — actual result cụ thể nằm ở bug do Test Studio/QA phát hiện qua từng bàn giao, xem "Ghi chú thêm của Leader" bên dưới. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response (báo cáo scan HTML)

- `upgrade-php85-laravel13-report.html` — https://redmine.melonglobal.net/attachments/download/36112/upgrade-php85-laravel13-report.html
- `chia-task-nang-cap-lme.html` — https://redmine.melonglobal.net/attachments/download/36114/chia-task-nang-cap-lme.html

## Ghi chú thêm của Leader

⚠️ **Input thiếu / input quá lớn — đọc trước khi dùng file này:**
- Ticket có **41 journal** trải từ 2026-10-22 đến 2026-10-26, mỗi journal là 1 bàn giao/round của Dev Studio (agent) — **KHÔNG chép hết nguyên văn vào đây** vì dung lượng quá lớn (digest gốc ~280KB). Mục "Journal nguyên văn" bên dưới chỉ tóm các bàn giao gần nhất; full history xem trực tiếp Redmine #43845 hoặc 2 file đính kèm.
- **MCP LME TEST STUDIO đã có task #507** cho ticket này: branch `ai_studio_implement_43845`, status `done-ai`, **16 bàn giao (handoffs)**, **1537 TC**, `aiResult = fail`, exec `pass 522 / fail 22 / other 810 / untested 183`, `reviewState = tester` (chưa review xong), tier tự động mới chạy `lower` (local/dev) — **chưa chạy staging/production**. File `04-tc-list.md` sẽ lấy từ nguồn này (BƯỚC 6b) do Redmine không có "Link TCs".
- **Môi trường**: F-14 nói Dev/review không cần staging, agent build/test trong runner Dev Studio (PHP 8.5). QA/regression trên staging + production (thêm extension `sockets`) là việc hậu bàn giao, **chưa chạy** tại thời điểm fetch (2026-10-26) theo `envAuto` của Studio (staging = 0%, prd = 0%).
- Phạm vi đổi **1374 file** trong 1 lần deploy — rủi ro cao theo chính Dev Studio tự đánh giá ở hầu hết các bàn giao ("Rủi ro cao... regression đầy đủ là bắt buộc").
- Ticket gốc **chưa Closed/Resolved** (status hiện tại: `Đang fix`) → theo RULE-11 của framework, các mục chưa có evidence hợp lệ (ticket chưa đóng) không được flag `[BLOCKER]`/`[MAJOR]` khi review — chỉ nêu ở mức `[NIT]`/gợi ý cho tới khi ticket đóng.
- Khi chạy `/review-tc` hoặc `/write-tc` cho task này: do quy mô (1537 TC, 21 task con, toàn module), nên cân nhắc tách theo từng mảng lớn (thanh toán, đặt lịch, LINE/chat, bảo mật IDOR, phân trang/API app+MCP...) thay vì review 1 lần toàn bộ — **quyết định này để Leader chốt**, `/new-task` không tự tách.

## Journal / note từ Redmine (nguyên văn, chỉ các bàn giao gần nhất có giá trị — xem lý do rút gọn ở trên)

**Journal #148095 — Dev Studio — 2026-10-24 (bàn giao gần nhất có "Đánh giá ảnh hưởng" đầy đủ trước các journal chỉ sửa tài liệu/PB nhỏ):**
```
Module PHP Web lên PHP 8.5 + Laravel 13 trong một lần release, đã gộp base release_step_20260930_v2 tới 6f9eaac2ba. Bản gộp gồm các vá bảo mật mới (chữ ký webhook LINE, binding SQL auto-reply, số lượng đặt chỗ sự kiện, tắt route Telecom, token socket JWT). Kết quả phía người dùng giữ như production nhờ các lớp tương thích. Khi test ưu tiên webhook LINE, chat realtime, đặt chỗ sự kiện và regression đầy đủ trên QA PHP 8.5.

Đánh giá ảnh hưởng — Rủi ro cao: Nâng khung và PHP nhiều bậc trên toàn module trong một lần release, kèm nhiều vá bảo mật mới của base (webhook, socket) trong cùng một release.
- Mọi màn web, API app mobile, API MCP, webhook LINE, cron và queue: regression đầy đủ theo docs/upgrade/smoke-list.md.
- Test Studio nên chạy lại trên bản giao này: nhận tin LINE qua webhook, chat realtime web và app, đặt / đổi lịch sự kiện (giới hạn số lượng) và auto-reply theo từ khoá.
```

**Journal #147368 — Dev Studio — 2026-10-22 (root cause 1 lỗi chặn đăng nhập điển hình do nâng cấp — ví dụ hành vi khác biệt Laravel 5.5 vs 13):**
```
Đã tìm ra nguyên nhân lỗi chặn sau đăng nhập. Code cũ gọi route với tên tham số lệch, ví dụ 'id' thay cho 'bot_id'. Laravel 5.5 vẫn tự điền vào ô còn trống, còn Laravel 13 ném lỗi, rồi Handler chuyển về trang chủ nên lặp redirect. Đã tái hiện lỗi và đếm được 35 lời gọi cùng kiểu. Kế hoạch v7 cho task cha thêm một lớp sinh URL giữ cách cũ, kèm test và quét lại. Sau khi sửa, task cha bàn giao lại để Test Studio chạy từ đầu.
```

<!-- 39 journal còn lại: liệt kê per-round decision/bugfix nhỏ hơn (PB-n, bàn giao #1-16) — xem Redmine #43845 trực tiếp hoặc dev_impact đã gộp ở 03-dev-impact.md (lấy từ MCP LME TEST STUDIO task #507, handoff #16, cập nhật 2026-10-25). -->
