# 01 — Bug Task từ khách hàng

> ⚠️ **Ticket cha của cả sprint, KHÔNG phải 1 bug đơn lẻ.** Auto-fill từ Redmine #45229 qua `/new-task` (`scripts/redmine_fetch.py`). Leader xác nhận: **tạo 1 folder cha, review theo từng lượt — gom các ticket con cùng tính năng (cùng nhóm T<n>) để review cùng nhau.**

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45229 — Sprint fix bug, bảo mật và hiệu năng PHP Web LME – 11/2026` |
| Module / Màn hình | **Sprint cha** — gom 21 nhóm (T1→T21), mỗi nhóm 1 task con `[PHP Web] Tn …` trên Redmine, mỗi nhóm có nhiều sub-issue riêng. Base: `release_staging_20261104` (PHP 8.5 + Laravel 13). Branch chung: `ai_studio_implement_45229` (sns-line) + `ai_studio_implement_45229` (linect-service, nhánh gốc `release-t09-2026`). Studio: **task #560** (feature tag `login-user`, 1225 TC, round hiện tại 1, status `tc-ready`). |

## Mô tả bug (bản dịch tiếng Việt)

Gom bug web (repo `sns-line`, module PHP Web) của các tracker **Bug tự detect, Improve nội bộ, Triển khai ngang, AI detect exception, AI detect performance** vào một sprint: sửa và test một lần.

- **Base:** `release_staging_20261104` (PHP 8.5 + Laravel 13).
- **Chia task con đúng 21 nhóm** dưới đây, mỗi nhóm một task con `[PHP Web] Tn …`; mỗi sub-issue giao cho task con của nhóm đó.
- Task con gộp vào task cha khi review xong; cả sprint bàn giao một lần.
- Ticket bảo mật T01–T22 (04/11) ghi số dòng của nhánh cũ `release_step_20260930_v2`: tìm lại vị trí theo tên hàm/route trên nhánh mới. Ticket AI detect ghi stack trace/thời gian đo trên production: kiểm lỗi còn trên nhánh mới trước khi sửa.
- Hiệu năng (T16–T20): sửa theo phân tích query (EXPLAIN, N+1, index); index mới trên bảng lớn ghi vào mục migration của bàn giao (chạy lúc nào, rollback).
- **Spec đã chốt** (ghi riêng vì ảnh hưởng expected TC): #37991 tag bị limit vẫn ghi lịch sử kèm trạng thái limit và action limit, preview cũng vậy. #41127 hợp đồng đang chờ chuyển khoản gia hạn mà user huỷ chuyển khoản hoặc đổi sang thẻ thì trả trạng thái và expired_date về như cũ (đổi thẻ: trả về trước rồi mới đổi).

### 21 nhóm (T1→T21) — thứ tự review đề xuất (giữ nguyên thứ tự Redmine)

| Nhóm | Tên nhóm | Mô tả ngắn | Sub-issue |
|---|---|---|---|
| T1 | Đăng nhập, 2FA, tài khoản, phiên | Gom mọi đường đăng nhập về một luồng 2FA; token reset an toàn; cấu hình session, logout, header bảo mật | #45150, #45156, #45163, #45167, #44081, #44098 |
| T2 | MCP OAuth và đăng nhập/API mobile phía server | Phần server trong sns-line (McpAuthController, LoginMobileController, API mobile). App Flutter để sau | #45157, #45152 |
| T3 | Route public, debug, API nội bộ, log và secret | Rà khối route public, xoá route debug, so key an toàn, rotate secret, lọc log | #45153, #45161, #45166, #43708 |
| T4 | Phân quyền theo bot_id, admin và nhân viên | Mọi ghi/xoá theo id phải kiểm tra bot và người sở hữu | #45159, #45162, #40979 |
| T5 | Upload và tải file | Một helper upload/download chung: allow-list, tên file do server sinh, kiểm tra quyền | #45164, #44620 |
| T6 | Form trả lời | XSS/SQLi của form, upload ảnh LIFF, lỗi emoji khi lưu câu trả lời | #45155, #43566, #43558 |
| T7 | Danh sách friend, bộ lọc, export, thông tin friend | Filter engine, export CSV, friend list, trường 国内住所. **#37991 spec đã chốt** | #45151, #45160, #41783, #37991, #44842 |
| T8 | Thanh toán và hợp đồng | Refund/payment-yearly, webhook Univapay, lịch sử slot. **#41127 spec đã chốt** | #45158, #41127, #44580 |
| T9 | Booking: bảo mật, Google Calendar/Sheet | Security T05 và các lỗi đồng bộ Google của Salon (#43557 và #43565 là cùng 1 lỗi) | #45154, #43556, #43557, #43565 |
| T10 | Salon/Lesson/Event: khung giờ, màn hình, LIFF | Khung đặt lịch, màn tuần/tháng, nhập CSV, preview action, LIFF event | #41706, #44795, #44897, #40822, #41698, #43567, #44689 |
| T11 | Affiliate/ASP | Security T16 và các lỗi màn ASP, đăng ký affiliate, thông báo hoa hồng | #45165, #43559, #44673, #44685, #44757, #44898 |
| T12 | Báo cáo và escape (hardening) | Escape tên LINE ở trang báo cáo và dữ liệu operator trong Blade/JS | #45168, #45169 |
| T13 | Chat 1:1, trigger, action, template | Các lỗi màn chat, trigger, modal action, template. #42241: gửi message gọi API lỗi trả 502, LBL tưởng server chết | #33315, #41126, #43555, #44617, #44649, #45174, #41192, #42241 |
| T14 | Lỗi 500 và UI chung | Exception thiếu kiểm tra null, nút mở tab mới, enable nút khi paste, CSV QR landing, path_intro | #43554, #38931, #37947, #36612, #41219, #37956 |
| T15 | Exception PHP do AI phát hiện | Exception thật trên production (SNSLineException): undefined index, deadlock, packet out of order, hết thời gian/bộ nhớ. Sửa nguyên nhân, không chỉ bọc try/catch | #45186, #42266, #41718, #41717, #41529 |
| T16 | Hiệu năng: đặt lịch Salon/Lesson, thông báo | Endpoint đặt/huỷ lịch, xoá staff/menu, đồng bộ Google, list khung giờ, thông báo salon (web + API mobile phía server) | #41712, #41345, #41469, #42535, #42270, #41491, #41755, #42595, #44642, #42825, #41524, #41504 |
| T17 | Hiệu năng: chat, template, gửi tin | Talk list v2 (300s), tải file chat, lưu/gửi template v2, lưu auto reply | #41236, #41656, #42269, #42532, #42863 |
| T18 | Hiệu năng: friend, tag, bộ lọc, rich menu, form | Lưu tag, list group tag, tag trong modal action, đếm filter broadcast, filter friend rich menu, sửa/copy form answer | #43380, #42862, #41554, #41516, #41711, #42534, #42533 |
| T19 | Hiệu năng: phân tích, thống kê admin | Cross analysis, initAnalysis, chart overview, thống kê admin hằng ngày và payment | #41502, #41505, #41515, #41761, #41506, #41710, #41509 |
| T20 | Hiệu năng: webhook, LIFF, đăng ký, khác | Webhook Univapay (311s), liff-access, register_v2, role access, metadata URL, point contract | #42838, #41309, #41625, #43194, #44641, #41152 |
| T21 | Lỗi production sau khi lên Laravel 13 / PHP 8.5 | B1–B11 đọc từ log production (B3 nằm ở #43554, nhóm T14) | #45230 |

**Tổng:** 21 nhóm · ~95 sub-issue. Risk theo requirement Studio (task #560, mục `requirements`): T1/T2/T3/T4/T8/T9 = `High`, các nhóm còn lại đa phần `Medium` (xem chi tiết per-nhóm khi review).

## Steps to reproduce / Expected / Actual

<!-- Không áp dụng — đây là ticket cha gom nhiều fix, không phải 1 bug tái hiện được. Steps/Expected/Actual nằm riêng ở mỗi sub-issue Redmine (xem cột Sub-issue ở bảng trên); fetch `/new-task <sub-issue-id>` riêng nếu cần review độc lập 1 ticket con cụ thể. -->

## Ảnh / video / log đính kèm

- [ ] Không có attachment ở ticket cha (0 attachment).

## Ghi chú thêm của Leader

- ⚠️ **Đây là ticket CHA — không tái hiện/test trực tiếp như 1 bug.** Review nên đi theo **từng nhóm T<n>** (gom các sub-issue cùng tính năng) — khớp với cách Dev deploy: mỗi nhóm = 1 task con `[PHP Web] Tn …`, gộp vào cha khi xong.
- Môi trường: base `release_staging_20261104`; đã chạy **92 lượt test tự động, toàn bộ ở env `local`** — **CHƯA chạy `dev`/`staging`/`prd`** (xem §ENV ở file 03) → áp RULE-08 cho các nhóm chạm bill tiền (T8) / media-upload (T5) / domain-job (T16-T20) / loadbalance.
- Sprint đã qua **32 vòng review** (v1→v32, tính tới Journal #153467 ngày 2026-11-09). Vòng 32 (mới nhất) **mở lại T9** cho 2 bug mới phát hiện ở Google Calendar (hồi quy OAuth 404, lộ token khi refresh token Google lỗi).
- **Deploy có nhiều bước thủ công bắt buộc trước/sau** (env mới `PUSH_NOTIFY_ALLOWED_IPS`, `LINE_LOGIN_CLIENT_ID/SECRET`, `EMAIL_API_TOKEN`, `KEY_CERTIFICATION_API`; pt-online-schema-change cho `line_user`/`bot_line_user`; 3+1 migration utf8mb4; 12 migration thêm index T16-T20; backup DB trước khi đổi charset) — xem đầy đủ ở file 03 mục "Migration/deploy". Review TC cho các nhóm T5/T6/T7/T8/T16-T20 **phải tính luôn rủi ro bước deploy sai thứ tự**, không chỉ code.
- **QA Test Studio lượt #7581 (10/11/2026) phát hiện**: bộ TC #45154 (T9) fail vì 4 fix cũ liên quan (BK-T1 #42413, BK-T2 #42414, CAL-T2 #42437, CAL-T4 #42439/#42791) **đang nằm trên nhánh riêng, CHƯA merge vào sprint #45229** — cần PM/Dev quyết merge hay để riêng trước khi review T9 (TC NEW-1098..1120 của task 560 sẽ còn fail tới khi merge).
- Có 2 việc **PM cần chốt hướng, chưa có trong code**: (a) #5426/#45599 — chat web mobile `/chat-mobile` gửi tin chữ vẫn lỗi `送信エラーです` (đợi PM chọn: làm lại theo route v2, khoá ô gửi, hay not_a_bug); (b) #45726 — bug mới log ngoài phạm vi sprint (ảnh rich menu tải nhiều ảnh ngoài quyền ⇒ HTTP 500, có sẵn ở base, không phải do sprint gây ra).
- **Review từng lượt theo nhóm nào trước** — gợi ý theo risk Studio: `High` trước (T1, T2, T3, T4, T8, T9) rồi `Medium` (còn lại); T21 (lỗi production sau Laravel 13/PHP 8.5) nên review song song với `framework/php-upgrade-checklist.md`.

## Dữ liệu định danh ca lỗi

<!-- Không áp dụng ở mức ticket cha — mỗi sub-issue có ca lỗi riêng, tra theo từng ticket khi review nhóm đó. -->

## Journal / note từ Redmine (nguyên văn, chọn lọc — chỉ journal có giá trị điều tra/tổng hợp nhất; 45 journal tổng, phần lớn là log merge từng vòng)

**Journal #153041 — Dev Studio — 2026-11-08 (tổng hợp vòng 31, đầy đủ nhất tới thời điểm fetch):**

```
Đánh giá ảnh hưởng — Rủi ro trung bình: Diff lớn chạm đăng nhập, upload, thanh toán, charset DB, bộ lọc friend, template và chat, đã qua 31 vòng review. Rủi ro chính là bước deploy: PUSH_NOTIFY_ALLOWED_IPS phải đặt trước, pt-osc và migration utf8mb4 đúng thứ tự, APP_ENV production phải đúng.
[Xem đầy đủ "File đã sửa" / "Migration" / "Lưu ý khi deploy" / "Điểm cần test" ở mục 3 file 03-dev-impact.md — nội dung quá dài, đã chuyển nguyên văn sang đó để tránh trùng lặp.]
Branch: ai_studio_implement_45229
- sns-line: ai_studio_implement_45229 (nhánh gốc release_staging_20261104 @8877b06f2c11, commit 85a061ec256cbe824b9eeb0fe94ba36a1b5b3002)
- linect-service: ai_studio_implement_45229 (nhánh gốc release-t09-2026 @f929d79140ad, commit 19b122ab88312c5ddb108787eb1e32819cb943b1)
```

**Journal #153467 — Dev Studio — 2026-11-09 (kế hoạch vòng 32, mới nhất):**

```
Dev Studio · Kế hoạch chia task con

Kế hoạch v32 mở lại T9 cho hai bug mới ở phần Google Calendar. Thứ nhất, liên kết Google của lịch đặt cũ thành công nhưng chuyển tới trang 404; đây là hồi quy do lần sửa bảo mật OAuth trước đó. Thứ hai, khi refresh token Google lỗi, log còn ghi nguyên exception nên lộ token. T13 làm việc nhỏ theo Review: tên PDF ở chat web mobile bỏ phần ?query. #5425 đã sửa; #5426 vẫn chờ PM chọn hướng.

Ảnh hưởng / rủi ro:
T9 chỉ đổi đích chuyển trang sau OAuth lịch đặt cũ (trả về như base) và nội dung log lỗi Google salon. T13 chỉ đổi chữ tên PDF ở chat web mobile. Cần kiểm lại luồng OAuth (lần đầu, replay, sai state) và đồng bộ booking salon khi Google lỗi.
```

**Journal #153605 — AI Auto test Lme — 2026-11-10 (kết quả QA lượt #7581, phát hiện branch chưa merge):**

```
QA (Test Studio, claude-qa) 10/11 — kết quả lượt #7581 (task 560, local, code web@85a061ec nhánh ai_studio_implement_45229):

Bộ TC #45154 (T05) mới chạy lộ các lỗ hổng booking/salon VẪN CÒN trên release_staging_20261104 và trên nhánh sprint, vì bản sửa của các ticket cũ chỉ nằm trên nhánh riêng, CHƯA merge (kiểm bằng git merge-base --is-ancestor):
- #42413 (BK-T1, nhánh ai_studio_implement_42413, "Fix done - Đợi test"): huỷ/đổi booking sự kiện bằng id của người khác (MobileEventBookingController cancelUserBooking, BookingEventController post-app-cancel/update — route không auth); đếm lại use_people/remain_limit; FE hiện thông báo lỗi server.
- #42414 (BK-T2, ai_studio_implement_42414): lịch đặt cũ — U1 gửi user_booking_id của U2 chiếm và đổi giờ booking; lịch sử/thông tin khách đọc theo LINE userId thô; đổi lịch chính chủ 500 "Undefined variable $lineUser".
- #42437 (CAL-T2, ai_studio_implement_42437, "Đang fix"): Salon/Lesson LIFF lịch sử/chi tiết booking theo line_user_id thô.
- #42439 / #42791 (CAL-T4, ai_studio_implement_42439): API Google sync/link/lịch sử + phân công staff của lịch bot khác; đổi staff đơn đã xoá ghi 0 dòng nhưng vẫn báo thành công, tạo remind, gọi Google.
Studio không mở ticket mới (trùng các ticket trên). Cần dev/PM quyết: merge các nhánh này vào sprint #45229 (hoặc release) hay để riêng; TC NEW-1098..1120 của task 560 sẽ còn fail cho tới khi merge.

Bug mới log từ lượt này: #45726 (ảnh rich menu tải nhiều ảnh ngoài quyền ⇒ HTTP 500, có sẵn ở base).
```

<!-- 42 journal còn lại: chủ yếu log "Đã gộp thêm: T<n> #<sub-issue> ai_studio_implement_<id> (<hash>, merge)" theo từng vòng review (v1→v31) — không trích hết vì chỉ lặp lại cấu trúc merge-log, không thêm thông tin điều tra mới. Cần xem chi tiết 1 vòng cụ thể → tra trực tiếp Redmine #45229 hoặc file --json đã lưu scratchpad. -->
