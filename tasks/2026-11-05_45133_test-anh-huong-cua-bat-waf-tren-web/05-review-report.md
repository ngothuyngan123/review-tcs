# 05 — Review Report

> Draft cho Leader verify. Task #45133 — Test ảnh hưởng của bật WAF trên web (Redmine tracker `Test`, không phải bug fix — không có code diff).
> Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #546 (retest, round 1, status `tc-ready`) |
| Tổng số TC review | 274 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 | Redmine không có "Đánh giá ảnh hưởng phía Dev" (task hạ tầng, không có `F*`/`D*`). Đánh giá theo T1–T12 của file 03 (do `/new-task` suy từ REQ Studio): **9/12 mục có TC — CHƯA ĐỦ** (T7, T9, T10 chỉ có TC phía admin) |
| **(b) diff code** — Studio `dev_impact` (`diffAvailable=false`, WAF là hạ tầng, không sửa code) | **14/17 điểm rủi ro có TC — CHƯA ĐỦ** (thiếu: thanh toán + callback thanh toán · đặt lịch phía LINE user · callback Google Calendar). Điểm "editor TinyMCE/CKEditor" tính có TC cho 5/7 nơi; template-v2 + お知らせ chưa định vị được ô editor → §5 I10 |

**Kết luận**: 4 GAP (G1–G4) · RISK chung: 274/274 TC chưa chạy (§5 I1) — không lặp lại "chưa chạy" ở từng dòng.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | T10 + smoke 「thanh toán」 (RULE-12): trang mua của LINE user `/v2/order-item/*` + cổng Stripe/UnivaPay + webhook UnivaPay `charge_finished` | dev-impact · diff code | NEW-160, NEW-180 (chỉ xem, không giao dịch) | GAP — 0 TC có giao dịch thật đi qua WAF; không TC nào nhận webhook/callback thanh toán | [BLOCKER] |
| G2 | T7 + smoke 「đặt lịch」: trang đặt lịch LINE user — lesson `/mobile/calendar/{hash}`, salon (LIFF), event `/mobile/event-booking/index/{hash}` | dev-impact · diff code | NEW-225, NEW-247, NEW-253 (admin đặt hộ) | GAP — 0 TC LINE user tự đặt chỗ | [BLOCKER] |
| G3 | T9: trang QR công khai `/landing-qr/{liffId}?uLand=` + `POST /ajax/v2/landing/{id}/count-scan-qr-code` | dev-impact · diff code | NEW-195, NEW-205 (chỉ sao chép URL / mã) | GAP — 0 TC mở アクションURL như khách | [BLOCKER] |
| G4 | Callback Google Calendar (OAuth liên kết lịch) — `dev_impact` ghi rõ | diff code | NEW-241 (lịch salon đã liên kết sẵn, không đi qua callback) | GAP — 0 TC đi qua callback OAuth Google Calendar | [MAJOR] |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 24 quan điểm Trigger khớp task · 19 chưa cover đủ (8 thiếu TC / thiếu ô · 7 thiếu loại case RULE-01 · 4 chỉ được cover bởi mã ngoài checklist).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `REG-URL-001` | Trung bình → Cao (CR chạm login / thanh toán / kết nối bot) | GAP — 0 TC mở 8 URL đo lường conversion (`/register/success` · `/admin/home` · `/basic/overview` · 4 trang `*_success` · `/admin/bot-add-v2?status=successful`) + biến thể "/" cuối + param thừa sau khi bật WAF | [BLOCKER] |
| Q2 | `LIFF-ENTRY-001` | Cao | RISK — form trang khách chỉ mở bằng đường dẫn trên browser, note ghi "đã bỏ qua bước mở LIFF" (#37385, NEW-10, NEW-12, #37388, #37390, NEW-13). Thiếu ô ① in-app LINE · ② URL LIFF trên trình duyệt ngoài (`/open-external-browser/{type}/{id}`) · ④ PC · user CHƯA kết bạn. Trang item / event / salon / lesson / QR: 0 ô (đã tính ở G1–G3) | [BLOCKER] |
| Q3 | `INTG-HOOK-001` | Cao | GAP — 0 TC nhận webhook ngoài qua WAF (UnivaPay `charge_finished` → `WebhookUnivapayControler`). Lấp chung G1 | [BLOCKER] |
| Q4 | `COMPAT-LEGACY-001` | Cao | RISK — 1 TC Normal (NEW-2). Không TC nào mở form qua link domain cũ `step3.lmes.jp` và mới `s.lmes.jp` (prd tách domain → WAF có thể cấu hình theo hostname). Thiếu Abnormal / Boundary không ghi lý do | [MAJOR] |
| Q5 | `INTG-CAL-001` | Cao | RISK — NEW-241 dùng lịch đã liên kết sẵn, không đi qua callback OAuth. Lấp chung G4 | [MAJOR] |
| Q6 | `ENV-002` | Trung bình | GAP — 0 TC kiểm rule WAF + danh sách ngoại lệ áp **cùng thời điểm** (Studio knowledge đã nêu ENV-002, `routes/web.php:1875` nhưng không có TC) | [MAJOR] |
| Q7 | `ENV-003` | Cao | RISK — NEW-257 (gate môi trường) thiếu media `p.lmes.jp`, trang LIFF đặt lịch / mua / QR, webhook thanh toán, API app, prd 2 server; thiếu Abnormal không lý do. Xử lý bằng bổ sung NEW-257 (§5 I5), không đẻ TC mới | [MAJOR] |
| Q8 | `SYNC-APP-001` | Trung bình → Cao (flow critical) | GAP — app quản trị mobile gọi `/api/mobile/*` (vd `/api/mobile/calendar-lesson/*`); Studio tạm loại chờ xác nhận domain, 0 TC | [MAJOR] |
| Q9 | `FUNC-001` (thiếu Abnormal) · `REG-SHARED-001` (39 Normal) · `OUT-TRUTH-001` (thiếu Boundary) · `OUT-EXPORT-001` (12 Normal) · `DATA-TEXT-001` (thiếu Abnormal) · `MEDIA-001` (thiếu Abnormal) · `OUT-PREVIEW-001` (1 Normal) | Cao | RISK — RULE-01 thiếu loại case, không ghi lý do. Thực tế phần Abnormal của WAF đã nằm ở nhóm "khi bị WAF chặn" (NEW-3, NEW-34, NEW-73…) và Boundary ở nhóm body lớn (NEW-4, NEW-5, NEW-122…) → chỉ cần ghi lý do vào `note`, không đẻ TC | [MAJOR] |
| Q10 | `LIST-001` · `UI-INPUT-001` · `NOTI-MAIL-001` · `SEC-002` | Trung bình / Trung bình / Cao / Cao | RISK — chỉ được cover bởi TC gắn mã ngoài checklist: tìm kiếm / lọc / phân trang (16 TC `SEARCH-001`), ô nhập text (33 TC `SEC-INJECT-001`), mail reset mật khẩu / 2FA / đổi email (NEW-58, NEW-61, NEW-217 gắn `AUTH-SESSION-001`). Đổi mã trên Studio, không cần TC mới | [MAJOR] |

Đã loại khỏi phạm vi (WAF chỉ lọc request, không đổi logic nghiệp vụ): `PERM-*` · `CONC-*` · `PERF-*` (Studio loại đo hiệu năng) · `JOB-*` / `MSG-001..003` (job gửi tin không đi qua WAF web) · `DATA-DB-001` / `PAY-AMOUNT-001` / `PAY-PLAN-001` (không đổi ghi DB / tính tiền) · `DEPLOY-*` (không đổi asset/payload).

---

## 3. TC trùng lặp nội dung

Đã rà 274 TC, không phát hiện trùng lặp. Các nhóm cùng ý định nhưng khác màn / khác handler FE (vd 9 TC "khi bị WAF chặn" NEW-3, NEW-34, NEW-73, NEW-94, NEW-120, NEW-134, NEW-188, NEW-242, NEW-255; 3 TC tốc độ thao tác NEW-20, NEW-65, NEW-123) không tính là trùng — mỗi TC đi qua endpoint / JS xử lý lỗi riêng.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: 274 TC × `spec-features/admin/{login-user, bill-item, payment-system-integration, qr-landing, lesson-booking, salon-booking, event-booking, form-answer}` + `kho-tcs/fa007` (TC-SAF-43…47), `fa010` (TC-TMT-117), `fa011` (TC-FORM-119, TC-FORM-263) — **không phát hiện mâu thuẫn**. Giới hạn 5.000 ký tự (NEW-35, NEW-88) và 20.000 ký tự (NEW-4, NEW-7) khớp kho. `spec-features/admin/form-answer` không có rule 20.000 ký tự → §8. Không có mục IGNORE (`IG-01`) trong TC / dev_impact.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | [BLOCKER] | Nguồn — 274 TC | 274/274 TC chưa chạy (Studio `exec.untested = 274`, pass 0%) — chưa có kết luận nào | Chạy sau khi NEW-257 chốt môi trường |
| I2 | [BLOCKER] | Nguồn — 274 TC | `env_scope = all` cho toàn bộ TC (gồm `local`, `dev` — không có WAF; chính Studio critique ghi "chạy local thì mọi case pass giả"). 0 TC có kết quả trên prd dù task chạm media / domain / thanh toán (RULE-08 / ENV-003) | Đổi `env_scope` toàn task sang env đã xác nhận bật WAF (`staging, prd`); đặt NEW-257 làm điều kiện chạy trước cả task |
| I3 | [MAJOR] | Nguồn — spec | Không có tài liệu WAF (rule set, Block/Count, ngưỡng body/rate, domain nào sau WAF, danh sách ngoại lệ); `spec-features/` không có; 274 TC `spec_status` trống. Expected của NEW-7, NEW-20, NEW-57, NEW-257 treo vào "chính sách đã xác nhận" | Infra cung cấp tài liệu cấu hình (không chứa bí mật) trước khi chạy; ghi đánh giá spec cho TC |
| I4 | [MAJOR] | [AP-6] file 03 mục 3 | Không có danh sách luồng/endpoint đi qua WAF + danh sách ngoại lệ (callback Google, webhook UnivaPay, pixel/popup, gọi nội bộ từ linect-service / MCP — Studio assumption #3) | Yêu cầu Infra/Dev kê danh sách, đối chiếu lại coverage |
| I5 | [MAJOR] | NEW-257 | Bảng domain bước 1 thiếu: media `p.lmes.jp` · trang LIFF đặt lịch (`/mobile/calendar/…`, `/mobile/event-booking/…`) · trang mua `/v2/order-item/*` · QR `/landing-qr/…`, `/open-mobile/…`, `/open-external-browser/…` · webhook `/mobile/univapay-callback-payment` · API app `/api/mobile/*` · domain cũ `step.lmes.jp` / `step3.lmes.jp` vs `s.lmes.jp`. Không hỏi prd 2 server (ENV-003: smoke theo từng router) | Bổ sung các dòng trên vào bảng bước 1; hỏi Infra WAF đặt trước hay sau load balancer |
| I6 | [MAJOR] | NEW-57 | Expected "khớp chính sách đã xác nhận" — không có con số. Spec `login-user` S-03: app **không có rate limit** trên `/login`, `/login-v2`, `/reset_password`… ⇒ mọi giới hạn / 429 ở login chỉ đến từ WAF | Ghi ngưỡng N + thời gian khoá do Infra cấp vào `data_input`; expected: dưới N → lỗi xác thực của app; chạm N → status + trang cụ thể của WAF |
| I7 | [MINOR] | 274 TC | `surfaces` trống → Studio chạy như web. TC trang khách / nhận tin LINE (#37385, NEW-9, NEW-10, NEW-11, NEW-12, #37388, #37390, NEW-13, NEW-28, NEW-101, NEW-114, NEW-115, NEW-210…) có mặt chính là `line-friend` | Gắn `surfaces` theo mặt tiếp xúc |
| I8 | [MINOR] | NEW-7 | Nhánh 20.001 chỉ thử CSS; JS chỉ "khoảng 20.000 — ghi độ dài thực" và có nhánh "giới hạn chưa chốt → blocked". Kho TC-FORM-263 đã chốt 20.000 cho cả CSS và JS | Thêm JS 20.000 / 20.001, bỏ nhánh blocked |
| I9 | [MINOR] | #37388 | Expected chép từ case kho đợt khác: "Luồng v1 hoạt động bình thường sau thay đổi HTTP/error handling" — không khớp bối cảnh WAF, không ghi status request như các TC WAF khác | Sửa expected: request chuyển trang / gửi trả 200, không 403 / trang chặn WAF |
| I10 | [NIT] | Input thiếu | Studio `dev_impact` kê TinyMCE ở template-v2 và CKEditor ở system-notifications (`/admin/notify/notifications/push`), nhưng NEW-29…36 chỉ có text / panel / media, NEW-140…144 chỉ tiêu đề / URL / ảnh; `spec-features/` không mô tả editor | Hỏi Dev ô nào là rich text → bổ sung TC nếu có |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 274 TC — không có TC nào ngoài phạm vi task. Task là hồi quy toàn web sau thay đổi hạ tầng dùng chung; mọi TC map được T1–T12 và quan điểm `REG-SHARED-001` (WAF soi mọi request).

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa011` (form) · `fa019` (lesson) · `fa020` (salon) · `fa021` (event) · `fa026` (bán hàng) · `fa007` · `fa010` — đọc theo nhóm "LINE user — …", "Public & URL form", "Googleカレンダー連携", "callback & webhook". `kho-tcs` chưa có QRコードアクション (qr-landing) và 決済システム連携 Stripe — không đối chiếu được |
| Vùng regression phát hiện từ kho | Nhóm phía LINE user của FA-011 / 019 / 020 / 021 / 026 (mở link & entry, nhập form, mua hàng, thẻ & 3D Secure, webhook UnivaPay) — Studio chưa dùng TC nào trong các nhóm này |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Xem danh sách ngay dưới bảng này |
| Căn cứ TC regression `R<x>` | R1: Studio `info_pack.impacts` "callback từ hệ thống ngoài (… thanh toán)" + spec `payment-system-integration` §2.3 Stripe OAuth callback (`code`, `state`) |
| Xác nhận chống trùng | Đã đối chiếu 274 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng |

**Dùng lại TC kho** (ticket yêu cầu "dùng TC kho có sẵn cho tính năng cơ bản") — thêm vào Studio task #546, chỉnh chung cho mọi dòng: chạy trên env đã bật WAF (sau NEW-257), mở Network ghi status từng request, ô nhập tự do dùng thêm chuỗi đặc biệt `TC45133 <b>&'"</b> ' OR 1=1 -- 😀`, kết quả `403/406/413/429` hoặc trang chặn WAF = Không đạt:

- **G1 / Q3** (mua hàng + webhook): `TC-BIL-142` "Mua 単品 số lượng = 1 → tạo 1 đơn" · `TC-BIL-144` "Mua 単品 bằng Stripe và bằng UnivaPay đều thành công" · `TC-BIL-212` "Cơ chế CÓ webhook — bấm mua tạo bản ghi chờ callback" (+ các case kế tiếp của nhóm webhook) · `TC-BIL-133` "Thẻ 3D Secure … mua thành công" · `TC-BIL-146` "Mua thất bại do thẻ bị từ chối". Chỉnh thêm: dùng sản phẩm 「テスト環境」 + thẻ test để chạy được trên prd (RULE-08).
- **G2** (đặt lịch phía LINE user): `TC-LSN-541` "Đã kết bạn … vào được từ 3 lối" · `TC-LSN-564` "Form booking: 3 kiểu liên kết friend info khi LINE user tự đặt" · `TC-SLN-423` "Ma trận trạng thái kết bạn × lối vào link đặt lịch" · `TC-SLN-443` "Điền form câu hỏi và hoàn tất đặt lịch" · `TC-EBK-150` "Mở link đặt chỗ bằng LINE app" · `TC-EBK-152` "Mở link bằng app NGOÀI LINE" · `TC-EBK-170` "Đặt chỗ không bill tiền → tạo booking".
- **G4 / Q5** (callback Google Calendar): `TC-SLN-358` "Liên kết Google Calendar mới → sync booking hiện có lên Google". Chỉnh thêm: bot test riêng chưa liên kết, ghi status của redirect quay về LME (che `code`/`state`).
- **Q2** (ma trận điểm vào form): `TC-FORM-409` "User CHƯA kết bạn mở form → redirect màn kết bạn" · `TC-FORM-411` "Mở form được từ đủ 6 đường" · `TC-FORM-412` "Mở form trên PC, iOS, Android và trình duyệt ngoài LINE". Chỉnh thêm: KHÔNG bỏ qua bước mở LIFF.
- **Q4** (link cũ / mới): `TC-FORM-457` "Form cũ redirect domain: step3.lmes.jp và s.lmes.jp đều mở được từ LINE".
- **Q7, Q9, Q10**: không đẻ TC — sửa NEW-257 (§5 I5), ghi lý do RULE-01 vào `note`, đổi mã quan điểm trên Studio.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGURL001-01 | UI | REG-URL-001 | Đăng nhập / tổng quan ログイン・概要: 8 URL đo lường conversion sau khi bật WAF | Normal | auto | staging, prd | web | 8 URL đo lường conversion (đăng ký, home, overview, 4 trang mua gói, thêm bot) mở đúng màn của LME khi đã bật WAF | - Env đã bật WAF chế độ Block; domain admin (production: `https://step.lme.jp`, staging: domain admin staging tương ứng) đã được Infra xác nhận nằm sau WAF.<br>- Đã đăng nhập tài khoản admin test (2FA tắt), tài khoản có ≥ 1 bot gói standard.<br>- Mở DevTools ▸ Network, bật Preserve log. | 1. Mở tab mới, dán URL số 1 ở Dữ liệu nhập (ghép với domain admin của env), bấm Enter.<br>2. Ghi status của request đầu tiên, URL cuối cùng trên thanh địa chỉ và chụp màn hình.<br>3. Lặp bước 1–2 cho URL số 2 → 8. | 1. `/register/success`<br>2. `/admin/home`<br>3. `/basic/overview`<br>4. `/monthly/standard_success`<br>5. `/yearly/standard_success`<br>6. `/monthly/pro_success`<br>7. `/yearly/pro_success`<br>8. `/admin/bot-add-v2?status=successful` | - Cả 8 URL: request đầu trả 200, hoặc 301/302 rồi trang cuối trả 200 trên domain LME<br>- Không URL nào trả 403 / 406 / 429 hay trang chặn của WAF (trang không có giao diện LME)<br>- Trang cuối hiển thị xong trong ≤ 10 giây, không loading vô hạn |  | Lấp Q1 · Đánh giá spec: Spec ghi rõ (checklist-lme REG-URL-001) · chỉ staging+prd vì local/dev không có WAF (áp tương tự tổ hợp deploy thật — Leader xác nhận) · Evidence: ảnh màn hình + status 8 URL |
| TC-REGURL001-02 | UI | REG-URL-001 | Đăng nhập / tổng quan ログイン・概要: biến thể có dấu "/" cuối của URL đo lường | Boundary | auto | staging, prd | web | 8 URL đo lường conversion có thêm dấu "/" cuối vẫn mở đúng màn, không bị WAF chặn | - Env đã bật WAF chế độ Block; domain admin (production: `https://step.lme.jp`) đã được Infra xác nhận nằm sau WAF.<br>- Đã đăng nhập tài khoản admin test (2FA tắt), tài khoản có ≥ 1 bot gói standard.<br>- Mở DevTools ▸ Network, bật Preserve log. | 1. Mở tab mới, dán URL số 1 ở Dữ liệu nhập (ghép với domain admin của env), bấm Enter.<br>2. Ghi status của request đầu tiên, URL cuối cùng và chụp màn hình.<br>3. Lặp bước 1–2 cho URL số 2 → 8. | 1. `/register/success/`<br>2. `/admin/home/`<br>3. `/basic/overview/`<br>4. `/monthly/standard_success/`<br>5. `/yearly/standard_success/`<br>6. `/monthly/pro_success/`<br>7. `/yearly/pro_success/`<br>8. `/admin/bot-add-v2/?status=successful` | - Cả 8 URL: trả 200, hoặc 301/302 về URL không có "/" cuối rồi trả 200<br>- Màn cuối là cùng màn với URL không có "/" cuối<br>- Không 403 / 404 / 406 / 429 hay trang chặn của WAF<br>- Không loading vô hạn (quá 10 giây) |  | Lấp Q1 · Đánh giá spec: Spec ghi rõ (checklist-lme REG-URL-001: biến thể có/không "/") · chỉ staging+prd vì local/dev không có WAF · Evidence: ảnh màn hình + status 8 URL |
| TC-REGURL001-03 | UI | REG-URL-001 | Đăng nhập / tổng quan ログイン・概要: URL đo lường kèm param quảng cáo thừa | Abnormal | auto | staging, prd | web | URL đo lường conversion kèm param quảng cáo thừa (utm, gclid, fbclid, yclid, giá trị tiếng Nhật encode) không bị WAF chặn, không treo | - Env đã bật WAF chế độ Block; domain admin (production: `https://step.lme.jp`) đã được Infra xác nhận nằm sau WAF.<br>- Đã đăng nhập tài khoản admin test (2FA tắt), tài khoản có ≥ 1 bot gói standard.<br>- Mở DevTools ▸ Network, bật Preserve log. | 1. Mở tab mới, dán `/register/success` + chuỗi param ở Dữ liệu nhập (nối bằng `?`), bấm Enter.<br>2. Ghi status request đầu, URL cuối và chụp màn hình.<br>3. Lặp bước 1–2 cho `/basic/overview`, `/monthly/standard_success`, `/yearly/pro_success`.<br>4. Mở `/admin/bot-add-v2?status=successful` + chuỗi param (nối bằng `&`), ghi status và chụp màn hình. | Chuỗi param: `utm_source=google&utm_medium=cpc&utm_campaign=%E7%A7%8B%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%9A%E3%83%BC%E3%83%B3&gclid=Cj0KCQjwTC45133abcdefghijklmnopqrstuvwxyz0123456789&fbclid=IwAR0TC45133abcdefghij0123456789&yclid=TC45133.1234567890` | - Cả 5 URL: kết quả giống URL không có param (200, hoặc 301/302 rồi 200 trên domain LME)<br>- Không 403 / 406 / 414 / 429 hay trang chặn của WAF<br>- Không loading vô hạn (quá 10 giây) |  | Lấp Q1 · Đánh giá spec: Spec ghi rõ (checklist-lme REG-URL-001: param thừa không được treo) · chỉ staging+prd vì local/dev không có WAF · Evidence: ảnh màn hình + status 5 URL |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | QR code action QRコードアクション: LINE user mở アクションURL công khai trên app LINE và trên PC | Normal | manual | staging, prd | line-friend, web | LINE user mở アクションURL của QRコードアクション sau khi bật WAF — trang mở được, action gắn tag chạy, lượt mở được đếm | - Env đã bật WAF chế độ Block; domain của アクションURL (`…/landing-qr/{liffId}?uLand=…`) đã được Infra xác nhận nằm sau WAF.<br>- Bot test có LIFF ID; đã tạo tag 「TC45133-QR-タグ」.<br>- Tạo QR code action QRコードアクション, quản lý 管理名 「TC45133-QR-<hhmm>」, hành động アクション = gắn tag 「TC45133-QR-タグ」, trạng thái 稼働状況 ON.<br>- Bạn bè test システム表示名 TC45133_F01 (gọi tắt F01) đã kết bạn bot test, chưa có tag 「TC45133-QR-タグ」; điện thoại đăng nhập LINE của F01.<br>- 1 PC có Chrome, mở DevTools ▸ Network. | 1. Admin mở QRコードアクション, bấm 「アクションURL（QRコード）」 của 「TC45133-QR-<hhmm>」, sao chép URL.<br>2. Admin mở màn chi tiết データ詳細 của QR, ghi số lượt hiện tại.<br>3. Admin gửi URL cho F01 qua chat 1:1 1:1チャット.<br>4. Trên điện thoại F01, bấm URL trong LINE, chờ trang xử lý xong.<br>5. Trên PC mở cùng URL bằng Chrome.<br>6. Ghi status request `GET /landing-qr/…` và `POST /ajax/v2/landing/{id}/count-scan-qr-code` trên PC.<br>7. Admin mở chi tiết bạn bè 友だち詳細 của F01, tab タグ.<br>8. Admin tải lại データ詳細 của QR. | URL: アクションURL sao chép ở bước 1 | - Bước 4: trang mở trong LINE, không trang chặn WAF, không treo; luồng kết thúc như trước khi bật WAF<br>- Bước 6: `GET /landing-qr/…` trả 200, hiện trang QR cho PC; `POST …/count-scan-qr-code` trả 200; không 403 / 406 / 429<br>- Bước 7: F01 có tag 「TC45133-QR-タグ」 (action chạy khi F01 mở URL)<br>- Bước 8: số lượt tăng ≥ 1 so với bước 2 |  | Lấp G3 · kho-tcs chưa có QRコードアクション — không đối chiếu được · Đánh giá spec: Spec ghi rõ (qr-landing SCR-QRL-36, EP-63 / EP-64) · manual vì bước 4 trên app LINE thật · chỉ staging+prd vì local/dev không có WAF · Evidence: ảnh điện thoại + HAR Network PC |
| TC-ENV002-01 | UI | ENV-002 | WAF — thời điểm bật rule / ngoại lệ trên production: luồng phụ thuộc ngoại lệ chạy ngay sau khi bật | Normal | manual | prd | line-friend, web | Ngay sau thời điểm bật WAF (hoặc đổi rule / danh sách ngoại lệ) trên production, chat real-time, gửi ảnh, pixel conversion và popup nhúng hoạt động ngay | - Infra báo trước thời điểm T bật WAF chế độ Block (hoặc cập nhật rule / ngoại lệ) trên production.<br>- Bot test nội bộ trên production có bạn bè test システム表示名 TC45133_F01 (gọi tắt F01); điện thoại đăng nhập LINE của F01.<br>- Conversion test 「TC45133-CV」 đã gắn mã pixel lên trang ngoài do team quản lý; popup test 「TC45133-POP」 đang bật, đã gắn mã nhúng lên cùng trang ngoài đó.<br>- Admin mở sẵn chat 1:1 1:1チャット hội thoại F01, DevTools ▸ Network bật Preserve log. | 1. Trong vòng 10 phút sau T, F01 gửi tin 「TC45133-ENV002-in」 tới bot.<br>2. Quan sát 1:1チャット (không tải lại trang).<br>3. Admin gửi 1 ảnh JPG ~2MB tới F01 từ 1:1チャット.<br>4. Trên LINE của F01, mở ảnh vừa nhận.<br>5. Mở trang ngoài có pixel + popup bằng trình duyệt điện thoại F01.<br>6. Ghi status request pixel và request popup.<br>7. Sau thời gian cập nhật số liệu, admin mở chi tiết 「TC45133-CV」. | Tin: 「TC45133-ENV002-in」 · ảnh JPG ~2MB | - Bước 2: tin của F01 hiện trên 1:1チャット không cần tải lại<br>- Bước 4: F01 xem được ảnh<br>- Bước 6: request pixel và popup trả 200, popup hiện trên trang; không 403 / 429 hay trang chặn WAF<br>- Bước 7: conversion ghi nhận F01<br>- Có luồng lỗi → ghi thời điểm, URL, status để Infra đối chiếu thời điểm áp ngoại lệ |  | Lấp Q6 · Đánh giá spec: Spec ghi rõ (checklist-lme ENV-002) · chỉ prd vì phải kiểm đúng thời điểm bật cấu hình trên production · manual vì chỉ prd · Evidence: ảnh chat + ảnh LINE + HAR + thời điểm T |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | App quản trị mobile LME エルメアプリ: đăng nhập, chat, xem đặt chỗ sau khi bật WAF | Normal | manual | staging, prd | mobile-app, line-friend | App mobile LME đăng nhập, gửi / nhận tin có ký tự đặc biệt và xem danh sách đặt chỗ lesson khi domain API app nằm sau WAF | - Infra xác nhận domain app mobile LME gọi (`/api/mobile/*`) có nằm sau WAF không; KHÔNG nằm sau WAF ⇒ ghi skip lý do "domain API app không qua WAF".<br>- Điện thoại cài app LME bản mới nhất; tài khoản admin test (2FA tắt).<br>- Bot test có bạn bè test システム表示名 TC45133_F01 (gọi tắt F01) đã kết bạn; điện thoại khác đăng nhập LINE của F01.<br>- Bot test có lịch đặt bài học レッスン予約 「TC45133-APP-LSN」 với ≥ 1 đặt chỗ. | 1. Mở app LME, đăng nhập bằng tài khoản admin test.<br>2. Chọn bot test.<br>3. Mở chat của F01, gửi tin ở Dữ liệu nhập.<br>4. Trên LINE của F01, xem tin nhận được.<br>5. F01 gửi lại 「TC45133-APP-返信」.<br>6. Trên app LME, xem chat của F01.<br>7. Mở danh sách đặt chỗ của 「TC45133-APP-LSN」 trên app. | Tin: `TC45133-APP <b>&'"</b> ' OR 1=1 -- 😀` | - Bước 1–2: đăng nhập và chọn bot thành công, không màn lỗi kết nối<br>- Bước 3: tin gửi thành công, hiển thị nguyên văn trên app<br>- Bước 4: F01 nhận đúng nguyên văn `TC45133-APP <b>&'"</b> ' OR 1=1 -- 😀`<br>- Bước 6: tin 「TC45133-APP-返信」 hiện trong chat của app<br>- Bước 7: danh sách đặt chỗ hiển thị đủ, không lỗi tải |  | Lấp Q8 · Đánh giá spec: Spec ghi rõ (lesson-booking: app admin dùng `/api/mobile/calendar-lesson/*`) · Studio đã tạm loại API app (excludedOrDeferred) — chạy khi Infra xác nhận domain · manual vì app mobile LME + app LINE trên thiết bị thật · chỉ staging+prd vì local/dev không có WAF · Evidence: ảnh màn app + ảnh LINE |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Liên kết thanh toán 決済システム連携設定: hoàn tất liên kết Stripe (OAuth Connect) và callback về LME | Normal | auto | staging, prd | web | Liên kết Stripe bằng OAuth Connect — callback quay về LME không bị WAF chặn, màn hiện trạng thái đã liên kết | - Env đã bật WAF chế độ Block; domain callback của LME đã được Infra xác nhận nằm sau WAF.<br>- Bot test riêng CHƯA liên kết Stripe (không dùng bot đang bán hàng); tài khoản Stripe test do team cấp.<br>- Mở DevTools ▸ Network, bật Preserve log. | 1. Mở 決済システム連携設定 của bot test, ghi trạng thái Stripe chưa liên kết.<br>2. Bấm nút liên kết Stripe.<br>3. Trên trang Stripe, đăng nhập tài khoản Stripe test và chọn tài khoản để kết nối.<br>4. Theo redirect quay về LME; ghi URL (che `code`, `state`), status và thông báo.<br>5. Tải lại 決済システム連携設定.<br>6. Huỷ liên kết Stripe của bot test theo quy trình của team. | Tài khoản Stripe test do team cấp (không ghi mật khẩu / code / token vào evidence) | - Bước 4: request callback về LME trả 200 (hoặc 302 về 決済システム連携設定), không 403 / 406 hay trang chặn WAF<br>- Bước 5: màn hiển thị Stripe đã liên kết với tài khoản Stripe test<br>- Lỗi cấu hình phía Stripe (redirect URI sai) → ghi lỗi cấu hình, không gán cho WAF |  | Lấp R1 · regression · căn cứ: Studio info_pack "callback từ hệ thống ngoài (… thanh toán)" + spec payment-system-integration §2.3 (Stripe OAuth callback `code`, `state`); NEW-180 chỉ xem · Đánh giá spec: Spec ghi rõ · RULE-05: tra tài liệu Stripe Connect mới nhất trước khi chạy · chỉ staging+prd vì local/dev không có WAF · Evidence: HAR (đã che code/state) + ảnh màn |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/form-answer` | Không có rule giới hạn 20.000 ký tự cho custom CSS / JS / thân カスタムHTML (Studio dẫn BR-17; kho TC-FORM-119, TC-FORM-263 đã chốt) | Spec thiếu so với kho (BƯỚC 1) | Leader |
| 2 | `spec-features/admin/login-user` S-03 | Ghi "không có rate limit" trên các route login. Sau khi bật WAF, nếu WAF có rule rate / brute-force cho các route này → bổ sung giới hạn ở tầng WAF (ngưỡng, phản hồi) | §5 I6 | Infra / Dev |
| 3 | Tài liệu hạ tầng WAF (ngoài `spec-features/`) | Chưa có: domain nằm sau WAF, Block/Count, rule set, ngưỡng body / rate, danh sách ngoại lệ | §5 I3, I4 | Infra / Leader |
