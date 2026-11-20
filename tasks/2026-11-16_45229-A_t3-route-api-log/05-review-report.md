# 05 — Review Report

> Draft cho Leader verify. **Lượt A của sprint #45229 — T3 (#45153 · #45161 · #45166 · #43708)**, review 2026-11-16.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #560` (task cha #45229) — lọc 43/1225 TC: 38 TC gắn `REQ-T3-*` + 5 TC nhóm T1 / T4 / INTEGRATION test đúng điểm T3 (NEW-193, NEW-417, NEW-798, NEW-799, NEW-800) |
| Tổng số TC review | 43 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 (BUG + F1–F15 + D1–D4 + T1–T7) | `11/27 mục có TC` — **CHƯA ĐỦ** (3 GAP · 13 RISK) |
| **(b) diff code** — 35 file T3 trong `spec_delta` + 3 rủi ro deploy ở journal | `9/21 điểm có TC` — **CHƯA ĐỦ** (2 GAP · 8 RISK · 2 không đánh giá được: `routes/web.php` 353 dòng và `routes/api.php` −5 dòng — thiếu danh sách route, xem §5 I3) |

**Kết luận**: `20/48 vùng ảnh hưởng đủ TC · 5 GAP · 21 RISK · 2 không đánh giá được` — gom thành 11 dòng dưới.

Loại khỏi mẫu số chiều (b) — file thuộc nhóm khác, review ở lượt của nhóm đó: `SecurityHeaders.php`, `MobileAccess.php`, `MobileAuthenticate.php`, `McpAuthController.php` (T1 / T2) · `AffiliateAuthenticate*.php` (T11) · `VerifyUnivapayWebhook.php` (T8) · `Console/Kernel.php` (T21).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | AC-H10 "bật lại CSRF" — F13 · `VerifyCsrfToken.php` (6 dòng) | dev-impact + diff code | không có (NEW-652 / NEW-653 cố ý dùng CSRF hợp lệ của phiên khách → chỉ kiểm lớp đăng nhập) | **GAP** — không TC nào dùng phiên chủ bot gửi request **thiếu / sai CSRF** tới route vừa chuyển nhóm | `[BLOCKER]` |
| G2 | Secret chuyển sang env — F12 · T6 · `config/sns-line.php` (Twilio) · `config/open_ai.php` · `Admin/UserController.php` (LINE Login) | dev-impact + diff code | NEW-978 (mail ✓) · NEW-417 (KEY ✓) · NEW-193 (LINE Login — **fail**, bug #45985 status New) | **GAP** — Twilio, OpenAI: 0 TC. Danh sách env bắt buộc ở journal vòng 31 **không có biến Twilio / OpenAI** → prd có thể chạy với key rỗng. LINE Login chưa kiểm được vì callback 500 (#45985, có sẵn ở base) | `[BLOCKER]` |
| G3 | Job Java thật gọi API nội bộ sau khi siết key — D1 · T4 · rủi ro deploy "KEY_CERTIFICATION_API của web phải trùng key job" | dev-impact + diff code | NEW-975 (skip `unsupported`) · NEW-656 / NEW-657 (gọi tay bằng curl) · NEW-1049 (chỉ push-notify) | **RISK** — chưa lượt nào chứng minh job thật vẫn qua kiểm key: tin / ảnh / postback (NEW-975 skip); action シナリオ / リマインダ do job gọi `start-scenario-api` / `start-remind`: 0 TC. Sai key là hỏng toàn hệ thống | `[BLOCKER]` |
| G4 | Trang khách vẫn public — T2 | dev-impact | NEW-662 (API, gọi không cookie) · NEW-663 · NEW-664 · NEW-665 (skip) | **RISK** — đặt lịch salon / lesson và mua sản phẩm trên LIFF: 0 TC; NEW-665 (sự kiện + thanh toán) skip. Đã có tiền lệ chặn nhầm trang khách trong chính sprint này: **#45370** (đăng ký affiliater bị chặn) | `[BLOCKER]` |
| G5 | Route quản trị lẻ — F2 · T1 | dev-impact | NEW-652 (**error**) · NEW-671 (mark-read ✓) | **RISK** — chiều chặn khách: NEW-652 chưa có kết quả. Chiều chủ bot vẫn dùng được: kết nối Stripe / PayPal, đăng ký thông báo PC trình duyệt — 0 TC | `[MAJOR]` |
| G6 | Route đọc dữ liệu friend + dò file — F1 · F9 | dev-impact | NEW-650 (skip `need-prep`) · NEW-974 (skip `need-prep`) | **RISK** — lỗ hổng đọc PII khi chưa đăng nhập và oracle dò file chưa được chứng minh đã đóng | `[MAJOR]` |
| G7 | `check_bot_member` nhánh System Admin — F3 · T3 · `CheckBotMember.php` · `AdminAccess.php` (+24) | dev-impact + diff code | NEW-668 (staff hợp lệ) · NEW-798 / NEW-799 / NEW-800 (staff bị thu hồi) | **RISK** — System Admin đăng nhập hộ user rồi thao tác: 0 TC (journal: check_bot_member áp cho "staff, System Admin, đổi bot"). Thay đổi trong `AdminAccess.php` không TC nào chạm | `[MAJOR]` |
| G8 | push-notify sau load balancer — rủi ro journal "IP lấy theo TrustProxies, sai cấu hình proxy làm job bị 403" | diff code | NEW-1010 (B5 giả `X-Forwarded-For` — chạy local, không có proxy) · NEW-973 · NEW-1011 | **RISK** — chưa kiểm trên môi trường có LB: header giả có vượt allowlist không, job thật có bị 403 không (RULE-08 loadbalance) | `[MAJOR]` |
| G9 | Server ảnh thật — T5 · rủi ro deploy "bật `UPLOAD_IMAGE_REQUIRE_KEY` sau khi server ảnh lên bản mới" | dev-impact + diff code | NEW-658 · NEW-659 (local, gọi thẳng API) | **RISK** — chưa TC upload ảnh từ màn quản trị qua server ảnh thật khi cờ bật, ảnh tới LINE user (RULE-08 media / domain) | `[MAJOR]` |
| G10 | Route trùng / chết — F15 | dev-impact | NEW-998 (skip `partial`) · NEW-999 ✓ | **RISK** — 6 màn dùng route từng khai trùng (サイトスクリプト, タグ管理, URL分析, gửi thử ステップ配信, copy シナリオ, import CSV) chưa chạy | `[MAJOR]` |
| G11 | Deploy `.htaccess` + gỡ package log-viewer — F14 · D3 · `public/.htaccess` · `composer.json` | dev-impact + diff code | NEW-661 (skip — cần Apache) · NEW-971 (local) | **RISK** — chưa kiểm sau deploy thật: manifest `bootstrap/cache` cũ làm app không boot; rule `.htaccess` chỉ có hiệu lực trên Apache staging / prd | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `21 quan điểm Trigger khớp task · 10 chưa cover đủ` (gom 8 dòng).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PERM-002` | Cao | **RISK** — có Normal (NEW-1011) + Abnormal (NEW-650, 651, 653, 799, 972, 973, 1010), **thiếu Boundary** (RULE-01): biên dải IP / CIDR của allowlist. NEW-652 (chặn khách ở route lẻ) đang mang mã khác → đổi sang `PERM-002` | `[MAJOR]` |
| Q2 | `SEC-002` | Cao | **RISK** — Normal chỉ có ở NEW-656, Boundary chỉ có ở NEW-655, bug gốc AC-C7 ở NEW-657 — cả 3 mang mã không thuộc checklist nên chưa tính cover → đổi 3 TC sang `SEC-002`. Chưa có biên **so khớp key gần đúng** (thừa khoảng trắng, khác hoa thường, thiếu / thừa 1 ký tự) | `[MAJOR]` |
| Q3 | `LIFF-ENTRY-001` | Cao | **GAP** ma trận điểm vào — ① in-app: form / affiliate / huỷ đơn định kỳ ✓ · sự kiện (NEW-665 skip) · **salon / lesson / mua sản phẩm: 0 TC** · ④ **PC đang có phiên quản trị bot khác: 0 TC**. Cả 3 TC hiện có chỉ là Normal. Ô ② ③ và trục kết bạn / link cũ-mới: có skipReason (dưới bảng) | `[BLOCKER]` |
| Q4 | `OUT-TRUTH-001` | Cao | **GAP** — chỉ NEW-669 (マイページ, mang mã khác) kiểm "hết phiên thì không báo thành công giả"; các màn khác dùng route vừa chuyển nhóm (lưu bộ lọc, 注文編集, QR landing) 0 TC. Bug #45428 chỉ sửa thông báo ở マイページ | `[BLOCKER]` |
| Q5 | `INTG-LINE-001` · `MSG-USER-001` · `JOB-001` | Cao | **RISK** — luồng thật LINE → job → API nội bộ chỉ có NEW-975 (skip, mang mã khác → đổi sang `INTG-LINE-001`) và NEW-1049 (chỉ push-notify). Action シナリオ / リマインダ qua job: 0 TC | `[BLOCKER]` |
| Q6 | `NOTI-MAIL-001` | Trung bình → nâng Cao (mail chứa link xác thực) | **GAP** — NEW-978 chỉ kiểm mail tới, không bấm link kích hoạt; trong khi `MailApiService` / `ActiveAccount` đổi cách lấy token và route đăng ký bị rà lại | `[BLOCKER]` |
| Q7 | `DEPLOY-LIVE-001` | Cao | **GAP** — release không maintain, job Java và server ảnh deploy riêng (journal: job "khuyến nghị deploy sau web", cờ upload bật "sau khi server ảnh lên bản mới"); 0 TC kiểm khoảng thời gian web mới chạy cùng job / server ảnh cũ | `[BLOCKER]` |
| Q8 | `MEDIA-001` | Trung bình → Cao (ảnh hiển thị cho khách cuối) | **RISK** — NEW-658 / NEW-659 không mang `MEDIA-001` (đổi NEW-659 sang `MEDIA-001`); chưa kiểm ảnh upload tới LINE user | `[MAJOR]` |

**Đã loại khỏi phạm vi (có căn cứ):**
- `LIFF-ENTRY-001` ô ② trình duyệt ngoài · ③ button trong tin · trục kết bạn · trục link cũ/mới: thay đổi T3 là middleware **phiên quản trị** (`check_login` / `check_bot_member`), không đọc `id_token` / `u_code` / trạng thái bạn bè / domain → mọi điểm vào **không có cookie quản trị** đi chung 1 nhánh, đã có NEW-662 (gọi không cookie). Riêng ô ④ PC **có** cookie quản trị là nhánh khác → Q3.
- `PERM-004` thiếu Boundary (mời lại staff sau khi thu hồi): thuộc lượt review T4.
- `SYNC-APP-001`: app mobile gọi `/api/mobile/*` bằng token, không qua nhóm route phiên — chờ Dev xác nhận 5 dòng xoá ở `routes/api.php` (§5 I3).
- `PAY-*`: PayPal / Stripe chỉ đổi middleware của route kết nối, không đổi luồng tiền → chỉ cần TC regression (TC-FUNC001-01 / -03).

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-1010 | NEW-973 → **gộp** vào NEW-1010 | DUP-SUBSET (một phần) | `PERM-002` · Abnormal · push-notify khi allowlist khác rỗng: caller ngoài danh sách bị từ chối, caller trong danh sách được nhận · cùng tiền đề app TEST với allowlist khác rỗng | `[MINOR]` |

- **Gate đã chạy**: xóa NEW-973 làm mất 2 bước chỉ nó có (B2 gửi bằng cookie tài khoản B · B4 cặp user / bot không hợp lệ) → **đổi sang GỘP**: chép 2 bước này vào NEW-1010 rồi mới xóa NEW-973.
- Đã rà 43 TC, ngoài DUP-1 không phát hiện trùng lặp.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-973 B4 · NEW-1011 B4 · NEW-1049 B1 | push-notify với `userId` không thuộc bot | Không tạo thông báo ("cặp user không thuộc bot ⇒ không tạo notification") | `spec-features/admin/notify-setting/web/api-spec.md` EP-18 (L622-634): "Tìm bot → tìm admin user → insert vào bảng `notification_pc`" · `userId`: "chỉ dùng cho log, user thực sự lấy từ bot.admin_id" | (A) Dev đã đổi code để kiểm cặp user / bot → spec cũ hơn bản f