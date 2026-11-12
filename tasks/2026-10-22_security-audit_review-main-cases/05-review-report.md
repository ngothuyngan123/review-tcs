# Review — LME Security Critical Main Cases (22/10/2026)

> **Loại review:** đối chiếu *kế hoạch test bảo mật* với *báo cáo audit nguồn* — KHÔNG phải task LME feature thường.
> Oracle = chính báo cáo audit. Không áp bộ máy `/review-tc` (Studio / dev-impact / 80 quan điểm / kho-tcs / spec-features) vì không phù hợp domain pentest.
> **Output là draft cho Leader verify.**

## 0. Nguồn

- **Kế hoạch (TC):** `LME_Security_Critical_Main_Cases_20261022.md` — C01–C20 (Critical) · X01–X05 (combo) · U01–U05 (Univapay).
- **Audit nguồn:** `security-audit-20261022.html` — branch `release_step_20260930_v2`, static code review. 68 phát hiện: **20 Critical · 28 High · 17 Medium · 3 Low**.

---

## 1. Coverage — kế hoạch bao được bao nhiêu báo cáo?

**Chiều A — 20 Critical: ĐỦ.** C01↔SEC-01 … C20↔SEC-20 map **1:1, không sót, không trùng**. Chất lượng từng case khá tốt (xem §5 các điểm cần siết).

**Chiều B — toàn báo cáo: CHƯA ĐỦ.** Kế hoạch tự giới hạn "20 Critical + Univapay (High)". Còn **47 phát hiện ngoài phạm vi** (27 High còn lại + 17 Medium + 3 Low). Trong đó **~10 phát hiện High có mức độ ngang Critical** (chiếm quyền toàn bộ tài khoản / thực thi lệnh trên prod / SQLi không cần đăng nhập / bàn đạp chuỗi tấn công) — **phải kéo vào P0/P1**, không nên xếp "ngắn hạn 1–2 tuần".

### Bảng GAP — High/Medium đáng bổ sung (xếp theo rủi ro)

| # | Finding (audit) | Vì sao ngang/cao hơn nhiều Critical đã test | Status |
|---|---|---|---|
| G1 | **Master password `PASS_LOGIN`** (High/auth) — 1 mật khẩu env đăng nhập MỌI tài khoản web/mobile/affiliate, so sánh `==` | Chiếm toàn bộ tài khoản bất kỳ, không log/cảnh báo. Tác động ≥ phần lớn IDOR Critical | **GAP** |
| G2 | **`/command` chạy Artisan trên prod** (High/debug) — điều kiện `&&` sai, chỉ cần truyền `type` | User thường chạy `auto_payment` (trừ tiền thật), `delete_landing`/`delete_richmenu` (xóa vĩnh viễn) | **GAP** |
| G3 | **`/b2/upload-url`** phát token Backblaze B2 (High/file) | Người lạ upload HTML/JS lên domain CDN → phishing/XSS trên domain hệ thống | **GAP** |
| G4 | **SQLi nhóm bộ lọc bạn bè** — `advanceFilterPost`, `scenario_stop_id`, `FilterController`, chat group `key`, `arr_template_ids` (High/sqli) | Đọc toàn bộ DB; **second-order**: filter lưu lại rồi chạy trong job | **GAP** |
| G5 | **SQLi không auth ở MyPage** `line_user_id` (High/sqli) | Đọc DB **không cần đăng nhập** | **GAP** |
| G6 | **Path traversal tải `.env`/mã nguồn** qua nhiều hàm download + `/basic/download-img-info` (no-auth) | Lấy secret tương đương C01/C02 nhưng qua endpoint khác → vá C01 vẫn thủng | **GAP** |
| G7 | **Upload đuôi client ở nhiều controller** (MessageTemplate, ChatService, ChatController, `/api/upload_image_common` no-auth) | Cùng rủi ro RCE/XSS như C10 nhưng ở đường khác → vá C10 vẫn thủng | **GAP** |
| G8 | **Open redirect / JS exec qua `url_back`** (High/xss) | `javascript:` chạy trên domain admin khi nạn nhân đang đăng nhập — **bàn đạp chuỗi** | **GAP** |
| G9 | **Stored XSS câu trả lời form (v-html màn admin)** (High/xss) | End user chèn `<img onerror>` → JS chạy trong phiên admin → gọi `/ajax/*` (miễn CSRF) chiếm bot | **GAP** |
| G10 | **CSRF miễn quá rộng** `/ajax/*`, `/login`, `/change_password`, `/postReset` | Kết hợp G8/G9 = chiếm tài khoản/bot qua phiên admin | **GAP** |
| G11 | IDOR còn lại: Booking Calendar cũ (~85 chỗ) + đọc chi tiết khách, App mobile (xóa/chặn bạn, hoàn tiền/hủy đơn, booking/notify/tag/sales), Popup CRUD, Booking event LIFF (ghi đè SĐT/email), order leak SĐT/email no-auth, MyPage no-auth ops, sửa/xóa thông báo toàn hệ thống | Cùng mẫu lỗi Critical C11–C19 nhưng ở màn/endpoint khác; nhiều cái no-auth hoặc thiệt hại tài chính | **GAP (P1)** |
| G12 | **Key hardcode + `/test-customer`** (Stripe `sk_test`, `OPEN_AI_API_KEY`, `EMAIL_API_TOKEN`) | Mở rộng phạm vi **rotate** của C20 — không rotate là chưa đóng được lỗ | **GAP** |

> Medium/Low (object `@json(Auth::user())` lộ token, `$e->getMessage()`, route test/debug, `/api/webhook-decode`, login-as token yếu, no throttle, Stripe webhook chưa verify, Google Maps key…) — chấp nhận để P2, nhưng **login throttle** và **Stripe webhook verify** nên gộp cùng đợt thanh toán (C08/U).

---

## 2. Quan điểm test còn thiếu trong các case ĐÃ có

- **Oracle SQLi chưa nêu rõ** (C06, C07): báo cáo đưa payload `... or sleep(5) ...` → **time-based blind** là cách phát hiện chính. Kế hoạch chỉ ghi "chuỗi kiểm thử SQLi". Bổ sung: đo thời gian phản hồi (sleep), và out-of-band nếu có. Thiếu oracle → dễ kết luận Pass sai.
- **Enumeration id tuần tự** (C14, C18, C19, và C13/C15): báo cáo lặp lại "id tăng dần / tuần tự 1..N" là vector chính. Cần 1 case quét dải id của shop khác, không chỉ "truyền 1 id của B".
- **Replay webhook LINE hợp lệ** (C05): X-series có idempotency cho Telecom (C08-05)/Univapay (U05) nhưng **C05 thiếu** case gửi lại 1 webhook LINE hợp lệ nhiều lần (tạo chat/scenario trùng).
- **Danh mục rotate hợp nhất** (C03/C04/C20/G12): báo cáo yêu cầu rotate Stripe/Univapay (mọi shop) · LINE channel token/secret · Firebase admin key · Google OAuth secret · OpenAI key · Email API token. Hiện rải rác ở nhiều case → **lập 1 checklist rotate chung** để không sót key.
- **Môi trường xác minh**: phần lớn chạy staging, nhưng C02 (log thật), C20 (git history + file công khai trên bản deploy), cấu hình prod (`APP_DEBUG`, nginx không chạy PHP trong `public/media` — liên quan C10/G7) **phải xác minh trên bản deploy thật / cùng dev-ops**. Thêm mục ENV rõ ràng cho các case này.

---

## 3. TC trùng lặp

- **C08 (Telecom) ↔ U01–U05 (Univapay)**: cùng mẫu "giả mạo webhook thanh toán" (thiếu/sai xác thực · sai số tiền/trạng thái · charge không thuộc đơn · replay). Không xóa — nhưng nên gom **1 sub-checklist thanh toán dùng chung** để 2 nhánh không phân kỳ, rồi mỗi nhánh chỉ ghi phần đặc thù (make_form_telecom hash leak cho Telecom; `GET /charges/{id}` đối chiếu cho Univapay). Gợi ý gộp cả **Stripe webhook verify** (Medium) vào đây.
- **C18 ↔ X05**: X05 ("request bị từ chối → kiểm DB/queue/dịch vụ ngoài") bổ trợ cho mọi case ghi/xóa, không trùng — giữ.

Không có trùng cần xóa.

---

## 4. Mâu thuẫn trong kế hoạch

**Không phát hiện mâu thuẫn** giữa kế hoạch và audit, và giữa các case với nhau.

- Kế hoạch xử lý đúng mức tin cậy: C06 ghi rõ "chưa xác nhận luồng chạy → Blocked/Chưa xác minh, không Pass" — khớp `Likely` của audit và tinh thần RULE-11 (chỉ bằng chứng chạy thật mới kết luận). ✔
- C16 phân biệt Confirmed (gán session) vs Likely (khai thác từng ajax) — đúng như audit. ✔
- Điều kiện đóng lỗi (§6 kế hoạch) nhất quán với nguyên tắc "401/403 chưa đủ" + rotate. ✔

---

## 5. Issues khác

- **[MAJOR]** Kế hoạch dán nhãn "P0.3" cho C06–C07 (SQLi) + X01–X05. Nhưng SQLi không-auth (C07) và chuỗi webhook (X01) là bề mặt người lạ — nên ngang P0.1. Thứ tự "P0.3" dễ bị hiểu là làm sau; §2 kế hoạch đã nói "không phải trì hoãn vá" nhưng nên nâng C07 lên P0.1.
- **[MINOR]** C01/C02/G6 cùng là "đọc file tùy ý trên server" nhưng rải 3 endpoint → sau khi vá cần **1 case regression chung**: quét lại tất cả hàm nhận đường dẫn từ client (grep `fileName`/`path`/`link_url`) chứ không chỉ 3 route đã biết (audit ghi rõ "chưa rà hết").
- **[MINOR]** Chưa có case kiểm "sau khi gỡ route, truy cập trả **404** (không phải 200 rỗng / vẫn chạy ngầm)" — áp cho C02, G2, G3, G12.
- **[NIT]** Trùng chủ đề với task repo đã có: `tasks/2026-10-19_43212_verify-webhook-line-signature` (C05) và `tasks/2026-10-21_43398_sql-injection` (C06/C07). Nên liên kết / tái dùng TC của 2 task đó thay vì viết lại từ đầu.

---

## 6. TC thừa / ngoài phạm vi

**Không có.** Mọi case C/X/U đều map về 1 phát hiện trong audit. C06-01 ("xác nhận command còn chạy ở prod") là bước điều kiện bắt buộc, giữ.

---

## 7. Main case đề xuất bổ sung

> Format theo chính kế hoạch gốc (Mã · Thao tác · Kết quả mong đợi) để drop-in trực tiếp. Giữ nguyên quy tắc "mỗi case chặn phải có case hợp lệ tương ứng; che secret; đối chiếu DB/queue/job".

### Nhóm P0 — High ngang Critical (account takeover / RCE / no-auth)

| Mã | Main case | Thao tác chính | Kết quả mong đợi |
|---|---|---|---|
| **C21** | Master password `PASS_LOGIN` | Đăng nhập bằng mật khẩu chung vào owner A, staff hạn quyền, affiliate, mobile; kiểm log/cảnh báo; mật khẩu thật vẫn đúng; sau khi bỏ backdoor thì mật khẩu chung bị từ chối | Không tài khoản nào đăng nhập được bằng mật khẩu chung; đăng nhập thật vẫn chạy; có audit log cho "login as" hợp lệ |
| **C22** | `/command` Artisan trên prod | User thường & người lạ gọi; thử từng `type` nguy hiểm (`auto_payment`, `delete_landing`, `delete_richmenu`); đối chiếu tiền/landing/richmenu trước-sau; kiểm route sau khi gỡ | Không thực thi lệnh Artisan qua web; không trừ tiền/xóa dữ liệu; route trả 404 |
| **C23** | `/b2/upload-url` phát token B2 | Người lạ lấy `uploadUrl`+`authorizationToken`; thử upload `.html/.js` lên CDN; case có auth hợp lệ | Không phát token cho request không quyền; không upload được loại file/ prefix ngoài whitelist |
| **C24** | SQLi nhóm bộ lọc bạn bè | Nối SQL qua tag/scenario/conversion id, `number_date`, `point`, keyword, `arr_template_ids`; **đo time-based (sleep)**; **second-order**: lưu filter → chờ job chạy lại; UNION; đối chiếu không đổi dữ liệu | Input là dữ liệu, không đổi logic truy vấn; không lộ lỗi SQL; filter lưu lại chạy an toàn trong job |
| **C25** | SQLi không auth MyPage | Gửi `line_user_id`/payload SQLi tới `/ajax/get_data_form_answer_my_page` không đăng nhập; time-based; chuỗi không phá dữ liệu | Validate/ép kiểu; không thực thi SQL; yêu cầu xác thực end user |
| **C26** | Path traversal tải `.env` (đa endpoint) | `?fileName=../../.env` ở CsvManagement, BookingEvent, ImageRichmenu, `download-img-info` (no-auth), User/AffiliateInfo; file hợp lệ vẫn tải | Không tải file ngoài thư mục cho phép; bắt auth; file hợp lệ vẫn tải |
| **C27** | Upload đuôi client (đa controller) | Upload `.php/.html/.svg` qua MessageTemplate, ChatService, ChatController, Api/ChatController, `/api/upload_image_common` (no-auth, `path2` traversal); đuôi kép/giả MIME; truy cập URL sau upload | File nguy hiểm bị chặn ở MỌI đường; media không thực thi mã; thư mục cố định |

### Nhóm P0/P1 — chuỗi & bàn đạp (XSS/CSRF/redirect)

| Mã | Main case | Thao tác chính | Kết quả mong đợi |
|---|---|---|---|
| **C28** | Open redirect / JS exec `url_back` | `?url_back=javascript:...` và URL ngoài tại trang payment success (admin đang đăng nhập) | Chỉ cho path nội bộ (`/`, không `//`) hoặc whitelist host; không chạy JS |
| **C29** | Stored XSS câu trả lời form (v-html) | End user gửi form chứa `<img onerror=...>`; mở màn admin/staff xem lịch sử trả lời | Giá trị được escape; JS không chạy trong phiên admin |
| **C30** | CSRF miễn quá rộng | Trang ngoài tự POST tới `/ajax/*` thay đổi dữ liệu, `/login`, `/change_password`, `/postReset` khi admin đang đăng nhập | Request thiếu CSRF token bị chặn; chỉ webhook thật được miễn |

### Nhóm P1 — IDOR còn lại (gom theo màn)

| Mã | Main case | Kết quả mong đợi |
|---|---|---|
| **C31** | Booking Calendar cũ: xóa/sửa lịch–staff–khóa học + đọc chi tiết khách của shop khác (bot_id từ request) | Lọc theo bot thực của phiên; không chạm dữ liệu shop khác |
| **C32** | App mobile: xóa/chặn bạn, hoàn tiền/hủy đơn trả trước, booking/notify/tag/sales theo `botId` client | Bot lấy từ token; kiểm owner/staff; không thao tác/đọc dữ liệu shop khác |
| **C33** | Popup: liệt kê/sửa/copy/xóa popup shop khác | Lọc theo bot hiện tại |
| **C34** | Booking event LIFF: sửa/hủy booking khách khác (ghi đè SĐT/email) | Xác thực `id_token`, so khớp `line_user_id` |
| **C35** | No-auth leak + MyPage: `/ajax/get-info-friend-order-index` lộ SĐT/email; `stopRemind`/`remove-tag`/`saveSetting` xóa theo id bất kỳ | Xác thực end user; chỉ trả/thao tác dữ liệu của chính họ |
| **C36** | User thường sửa/xóa thông báo toàn hệ thống | Chỉ `supper_admin`; không chèn được link phishing toàn hệ thống |

### Nhóm P0 — mở rộng rotate

| Mã | Main case | Kết quả mong đợi |
|---|---|---|
| **C37** | Key hardcode + `/test-customer` | `/test-customer` trả 404; Stripe `sk_test`/OpenAI/Email token cũ **mất hiệu lực** sau rotate; chức năng dùng key mới vẫn chạy |

### Chuỗi kết hợp bổ sung

| Mã | Chuỗi kiểm thử | Kết quả mong đợi |
|---|---|---|
| **X06** | Stored XSS form (C29) → JS trong phiên admin → gọi `/ajax/*` miễn CSRF (C30) → `bot-save`/`unfollow-line`/`supper-admin` | Không có bước nào thực thi được: XSS bị escape, CSRF bị chặn, hoặc IDOR bị chặn |
| **X07** | Master password (C21) → login as nạn nhân → thử các thao tác IDOR/thanh toán | Backdoor đã gỡ nên không vào được; nếu còn, mọi tác động sau đó phải quy về 1 lỗ gốc |
| **X08** | Credential Firebase adminsdk (C20) → thử dùng key cũ với Firebase (push/DB) sau rotate | Key cũ bị revoke; không thao tác được project Firebase |

---

## 8. Spec / quy trình cần cập nhật

- **Danh mục rotate hợp nhất** (từ C03/C04/C20/C37/G1): 1 bảng key × shop × trạng thái rotate × xác minh "key cũ mất hiệu lực" — điều kiện đóng mọi lỗ lộ secret.
- **Checklist regression "đọc file tùy ý"** (C01/C02/C26): grep toàn repo các hàm nhận đường dẫn từ client, không chỉ route đã liệt kê (audit tự nhận chưa rà hết ~1.100 ajax + ~120 mobile).
- **Nâng phân đợt**: C07 (SQLi no-auth) và X01 (webhook chain) lên P0.1 cùng nhóm bề mặt người lạ.
- Bổ sung vào `BE-coding-rules.md` + checklist `/review-code` (đúng như mục Trung hạn của audit) để chặn tái phát mẫu "tin `bot_id` từ request" và "nối chuỗi vào SQL".
