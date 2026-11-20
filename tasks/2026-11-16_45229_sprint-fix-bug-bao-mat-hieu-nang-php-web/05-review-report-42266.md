# 05 — Review Report

> Draft cho Leader verify. **Sprint #45229 · T15 · sub-task #42266** — deadlock khi INSERT `oauth_refresh_tokens` (MCP OAuth), review 2026-11-19. Main case nằm ở §9.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #560` (task cha #45229, fetch 2026-11-19, 1287 TC) — lọc TC gắn `REQ-X-42266-*` (4) + `REQ-T15-OTHER-03` (2 — phạm vi thu hồi của `revokeForUser`, cùng diff `46cf693fa6`) |
| Tổng số TC review | 6 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` (mức sprint) không có mục riêng cho #42266 → dùng 7 mục Dev Studio tự kê ở requirement `REQ-X-42266` / `-01` / `-02` / `-03` + `REQ-T15-OTHER-03`: BUG deadlock · `revokeForUser` theo khoá chính từng lô 500 · `/token` + `/refresh` chạy lại ≤ 3 lần khi deadlock · refresh đồng thời nhiều token · cùng 1 token song song · tải trộn + lô > 500 · phạm vi thu hồi | `7/7 mục có TC` — **CHƯA ĐỦ** (3 RISK) |
| **(b) diff code** — 6 điểm: `OAuthRefreshToken::revokeForUser` (+30) · `McpAuthController` `/token` chạy lại · `/refresh` chạy lại · hành vi thu hồi đổi từ 1 câu UPDATE khoá bảng sang đọc-rồi-UPDATE từng lô · 2 nơi gọi `revokeForUser` Dev kê (đặt lại mật khẩu · gửi lại code đã dùng) · rủi ro hồi quy thu hồi atomic #45157 khi transaction chạy lại | `5/6 điểm có TC` — **CHƯA ĐỦ** (1 GAP · 3 RISK) |

**Kết luận**: `6/13 vùng ảnh hưởng đủ TC · 1 GAP · 6 RISK`.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Hành vi thu hồi theo user đổi: trước = 1 câu UPDATE khoá cả bảng; sau = đọc danh sách token rồi UPDATE theo khoá chính từng lô 500 | diff code | NEW-770 · NEW-686 (đặt lại mật khẩu khi **không** có refresh nào chạy cùng lúc) · NEW-684 (thu hồi theo user **+ client C2**, refresh chạy ở C1 — khác client) | **GAP** — 0 TC chạy đặt lại mật khẩu **đồng thời** với refresh của chính user đó. Token phát ra giữa lúc đọc danh sách và lúc UPDATE có thể không bị thu hồi ⇒ sau khi đặt lại mật khẩu vẫn còn refresh token dùng được (trái REQ-T2-MCP-MOBILE-03 "đặt lại mật khẩu thu hồi toàn bộ refresh token MCP") | `[BLOCKER]` |
| G2 | Nhánh chạy lại transaction khi deadlock ở `/token` + `/refresh` | dev-impact + diff code | NEW-684 · NEW-683 | **RISK** — (1) không TC nào xác nhận deadlock **đã thật sự xảy ra** rồi được chạy lại: NEW-684 B3 ghi "**nếu** InnoDB có deadlock thì…", không có deadlock vẫn Đạt; (2) nhánh hết 3 lượt / lỗi khoá DB khác: 0 TC, chưa có expected cho mã lỗi trả về và việc rollback (token cũ còn dùng được, không sinh token mồ côi). Unit test `tests/Unit/McpRefreshTokenDeadlockT15Test.php` có nhưng không thay được kiểm qua HTTP | `[MAJOR]` |
| G3 | BUG #42266 trên môi trường thật + rủi ro hồi quy #45157 | dev-impact + diff code | 6/6 TC chỉ Đạt ở `local` (run #7782, 13/11). NEW-685 chạy `dev` (run #7914, 17/11) **fail** | **RISK** — deadlock chỉ xảy ra dưới tải production nhiều web server; chưa TC nào chạy ngoài local mà Đạt; lần chạy dev duy nhất fail ở bước lấy token (`/api/mcp/oauth/token` 500, xem §5 I1); chưa có TC xác nhận sau release signature deadlock không còn | `[BLOCKER]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `7 quan điểm Trigger khớp task · 5 chưa cover đủ`.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `SEC-002` | Cao | **GAP** — 0/6 TC mang mã. Nội dung Normal (NEW-770 đặt lại ⇒ thu hồi) + Boundary (NEW-686 1.201 token) đã có nhưng gắn mã khác → gắn thêm `SEC-002`. **Abnormal** (đặt lại mật khẩu đồng thời với refresh) 0 TC → TC-SEC002-01 | `[BLOCKER]` |
| Q2 | `ENV-001` | Cao | **GAP** — token dùng 1 lần là kiểm tra quan trọng chạy qua nhiều web server, deadlock chỉ xuất hiện khi nhiều tiến trình ghi cùng bảng; 0 TC mang mã, 0 TC Đạt ngoài local → TC-ENV001-01 + chạy lại TC scope `all` trên staging / prd (§5 I2) | `[BLOCKER]` |
| Q3 | `CONC-001` | Cao | **RISK** — Normal NEW-683 · Abnormal NEW-685 (lần chạy mới nhất fail) · **thiếu Boundary** (RULE-01) → TC-CONC001-01 (giữ khoá dưới / vượt thời gian chờ khoá). NEW-684 mang mã Studio `TOOL-KNOW-002` → đổi sang `CONC-001` | `[MAJOR]` |
| Q4 | `DATA-DB-001` | Cao | **RISK** — chỉ NEW-770 (Normal) mang mã. Phạm vi `WHERE` trên 2 user + 2 client đã có ở NEW-769 (mã `TOOL-NEGCTRL-001`) và NEW-686 (mã `PERF-LARGE-001`) → đổi / gắn thêm mã, không cần TC mới | `[MAJOR]` |
| Q5 | `REG-SHARED-001` | Cao | **RISK** — `revokeForUser` dùng chung 2 nơi (đặt lại mật khẩu · gửi lại code đã dùng), cả 2 đã có TC (NEW-770 / NEW-686 · NEW-769 / NEW-684) nhưng 0 TC mang mã → gắn thêm mã. Đổi mật khẩu ở アカウント設定 **không** phải nơi gọi (Leader chốt 2026-11-19) | `[MAJOR]` |

**Đã loại khỏi phạm vi (có căn cứ):**
- 4 hướng đọc bảng `oauth_refresh_tokens`: web (đặt lại mật khẩu, MCP OAuth) đã xét ở trên · app quản trị di động dùng JWT app riêng (REQ-T2-MCP-MOBILE-07), không đọc bảng này · job nền và export: không có trong diff / requirement.
- `STATE-001`: ghi thu hồi + phát token mới nằm trong 1 transaction; rollback khi lỗi đã đưa vào TC-CONC001-01 B7–B8.
- `DEPLOY-LIVE-001` / `COMPAT-LEGACY-001`: #42266 không đổi schema, format token hay payload API — token phát trước release dùng như cũ.
- `PERF-LARGE-001`: NEW-686 (1.201 token, 3 lô) đủ.
- RULE-08: không chạm media / domain / job nền / bill tiền.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-360 (T2 #45157, cùng task #560) | NEW-685 → **gộp** | DUP-SUBSET | `CONC-001` · Abnormal · gửi song song cùng 1 refresh token tới `/api/mcp/oauth/refresh` · 1 token còn hiệu lực ⇒ đúng 1 request 200, còn lại 400 invalid_grant, không 500 "kể cả khi DB gặp deadlock — có thử lại" (NEW-360 B2) | `[MINOR]` |

- **Gate đã chạy**: NEW-685 là TC duy nhất gắn `REQ-X-42266-02` → **gộp, không xoá**: gắn thêm `REQ-X-42266-02` vào NEW-360 và chép "lặp 5 vòng" vào B2 của NEW-360, rồi mới xoá NEW-685. Leader muốn #42266 có bằng chứng riêng thì giữ cả 2.
- Đã rà 6 TC + 13 TC OAuth MCP của T2 (NEW-347…NEW-364): NEW-770 và NEW-686 khác nhau về quy mô (2 vs 1.201 token) và B4 (token mới sau đặt lại dùng được), không trùng. Ngoài DUP-1 không phát hiện trùng.

---

## 4. Mâu thuẫn trong TCs

Đã rà 6 TC × `spec-features/admin/login-user/feature-spec.md` (SCR-LGN-04…07 đặt lại mật khẩu — không có rule nào về refresh token MCP) · kho-tcs chưa có tính năng Đăng nhập / MCP OAuth · `framework/ignore-features.md` (không khớp) — không phát hiện mâu thuẫn. Expected giữa các TC (`invalid_grant` "Refresh token has expired or been revoked." · "Authorization code has already been used.") thống nhất.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-685 | Lần chạy mới nhất (run #7914, `dev`, 17/11) **fail ngay bước lấy token**: `POST /api/mcp/oauth/token` đổi code hợp lệ trả HTTP 500, chưa tới phần kiểm của #42266. **Chưa gắn ticket bug** (run tạo bug Studio 5950–5960 nhưng không gắn NEW-685). Cùng run, 8 TC OAuth của T2 (NEW-355…360 …) cũng 500 ở bước này. Transaction chạy lại bọc `/token` là thay đổi của #42266 → chưa loại được nguyên nhân do code | Xác định 500 do cấu hình dev (secret JWT MCP — tiền đề TC ghi thiếu secret là lỗi môi trường) hay do code; gắn bug hoặc ghi skipReason; chạy lại NEW-683 / 684 / 685 / 769 / 770 trên dev |
| I2 | `[MAJOR]` | Nguồn TC | 5/6 Đạt nhưng **toàn bộ chỉ ở `local`** (run #7782, 13/11). 4 TC scope `all` (NEW-683, 685, 769, 770) chưa chạy staging / prd. Nhánh đã thêm ≥ 4 vòng commit sau bản đã chạy (`85a061ec25` → `7f36738b68`) | Chạy lại 6 TC trên commit mới nhất; NEW-683 / 685 / 769 / 770 chạy thêm staging |
| I3 | `[MAJOR]` | Spec | Không có spec cho MCP OAuth (`/api/mcp/oauth/token`, `/refresh`) và cho việc thu hồi refresh token MCP khi đặt lại mật khẩu — `login-user/feature-spec.md` im lặng. Expected của 6 TC chỉ dựa vào requirement Studio | Dev bổ sung spec (§8 #1, #3) |
| I4 | `[MAJOR]` | Input thiếu từ Dev | (1) `03-dev-impact.md` mức sprint không có mục cho #42266. (2) `revokeForUser` chạy trong hay ngoài transaction đặt lại mật khẩu; token phát ra trong lúc thu hồi xử lý thế nào (G1) | Hỏi Dev; cập nhật G1 theo câu trả lời |
| I5 | `[MAJOR]` | NEW-684 | Expected không đo được nhánh chạy lại: B3 "nếu InnoDB có deadlock thì request vẫn trả 200/400" → nếu lượt chạy không sinh deadlock nào thì vẫn Đạt mà không kiểm REQ-X-42266 | Thêm bước đếm `lock_deadlocks` (`information_schema.INNODB_METRICS`) trước / sau 60 giây tải. Bằng 0 thì ghi "không kích hoạt được nhánh chạy lại", không kết luận Đạt cho phần này |
| I6 | `[MINOR]` | NEW-364 (T2) · REQ-T2-MCP-MOBILE-03 | Leader chốt 2026-11-19: đổi mật khẩu ở アカウント設定 **không** thu hồi refresh token MCP. NEW-364 vẫn để expected mở ("chỉ kết luận bug nếu #45157 yêu cầu"); tiêu đề REQ-T2-MCP-MOBILE-03 ghi "thu hồi khi đổi/đặt lại mật khẩu" — trái quyết định | NEW-364: sửa expected B4 thành `POST /api/mcp/oauth/refresh` với R1 ⇒ 200 (refresh token MCP không bị thu hồi). Sửa tiêu đề REQ-T2-MCP-MOBILE-03 thành "… thu hồi khi đặt lại mật khẩu". Xử lý ở lượt review T2 |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 6 TC — không có TC nào ngoài phạm vi task.

---

## 7. TCs đề xuất bổ sung (3)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | kho-tcs chưa có tính năng Đăng nhập / MCP OAuth — không đối chiếu được |
| Vùng regression phát hiện từ kho | Không có |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho | Không |
| Căn cứ TC regression `R<x>` | Không có TC R — vùng regression (2 nơi gọi `revokeForUser`, thu hồi atomic #45157) đã có TC ở NEW-769 / 770 / 685 và T2 NEW-359 / 360 |
| Xác nhận chống trùng | Đã đối chiếu 6 TC ở BƯỚC 0 + 13 TC OAuth MCP của T2 (NEW-347…364) — TC-SEC002-01 khác NEW-770 / 686 ở chỗ đặt lại mật khẩu chạy **đồng thời** với refresh; TC-CONC001-01 khác NEW-685 / 360 ở chỗ giữ khoá DB — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-SEC002-01 | API | SEC-002 | MCP OAuth + Đặt lại mật khẩu パスワード再設定: thu hồi refresh token khi đang có refresh đồng thời | Abnormal | auto | dev, local, staging | api, web | Đặt lại mật khẩu trong lúc 10 luồng đang refresh token MCP của chính user đó: sau khi đặt lại, không refresh token cũ nào còn dùng được | - Client MCP C1 tự đăng ký: `POST /api/mcp/oauth/register`, client_name `qa45229-42266-race-<timestamp>`, redirect_uris `["http://127.0.0.1:8765/callback"]` → ghi client_id, client_secret.<br>- User U: tài khoản admin test đã kích hoạt, KHÔNG bật 2FA, đọc được mail. U có 600 refresh token MCP còn hiệu lực trên C1 (seed SQL vào `oauth_refresh_tokens`, hoặc chạy luồng authorize PKCE S256 nhiều lần); tester giữ 10 token T01…T10 trong số đó.<br>- User V (đối chứng): có 1 refresh token R_V còn hiệu lực trên C1.<br>- Công cụ gửi song song ghi log từng request (thời điểm, HTTP status, 6 ký tự đầu của refresh_token mới). | 1. Mở `/reset_password`, nhập email U, bấm 「送信」. Mở link trong mail tới màn 「パスワード再設定」, nhập 「新しいパスワード」 + 「新しいパスワード（確認）」, **chưa** bấm xác nhận.<br>2. Khởi động 10 luồng: luồng i liên tục gọi `POST /api/mcp/oauth/refresh` (client_id, client_secret C1) bằng Ti, mỗi lần dùng refresh_token mới nhất vừa nhận.<br>3. Khi 10 luồng đang chạy, bấm xác nhận đặt lại mật khẩu; ghi thời điểm màn hoàn tất hiện ra (mốc M).<br>4. Cho 10 luồng chạy thêm 10 giây rồi dừng.<br>5. Mỗi luồng gọi refresh 1 lần bằng refresh_token mới nhất luồng đó nhận được.<br>6. Gọi refresh bằng R_V.<br>7. Đăng nhập lại MCP (authorize PKCE S256) bằng mật khẩu mới, đổi code lấy token, gọi refresh bằng refresh_token mới. | Token của U trên C1: 600 (> 1 lô 500)<br>Số luồng refresh: 10<br>Mật khẩu mới: `<mật khẩu tài khoản test mới>` | - B2–B4: mọi request refresh trả 200 hoặc 400 invalid_grant; không request nào 500.<br>- B3: đặt lại mật khẩu thành công (màn hoàn tất).<br>- Mọi request refresh gửi **sau mốc M** trả 400 `{"error":"invalid_grant","error_description":"Refresh token has expired or been revoked."}`.<br>- B5: cả 10 luồng ⇒ 400 invalid_grant (không token nào phát ra trước hoặc trong lúc đặt lại mật khẩu còn dùng được).<br>- B6: 200 (đặt lại mật khẩu của U không thu hồi token của V).<br>- B7: 200 (token cấp sau khi đăng nhập lại dùng được). | | Lấp G1 / Q1 · Rule: REQ-T2-MCP-MOBILE-03 "đặt lại mật khẩu thu hồi toàn bộ refresh token MCP" · Đánh giá spec: Spec không ghi (`login-user/feature-spec.md` không có rule MCP) — Dev xác nhận rule trước khi chạy · Có token sống sót thì ghi luồng + thời điểm phát so với M · Không chạy prd vì tải đồng thời + seed token · Evidence: log 10 luồng + ảnh màn hoàn tất |
| TC-CONC001-01 | API | CONC-001 | MCP OAuth (`POST /api/mcp/oauth/refresh`): refresh khi dòng token đang bị khoá DB | Boundary | auto | dev, local, staging | api | Giữ khoá dòng refresh token ngắn hơn thời gian chờ khoá thì refresh vẫn thành công; giữ quá thời gian chờ thì trả lỗi có kiểm soát và token cũ không bị thu hồi dở | - Client MCP C1 tự đăng ký: `POST /api/mcp/oauth/register`, client_name `qa45229-42266-lock-<timestamp>`, redirect_uris `["http://127.0.0.1:8765/callback"]`.<br>- User U (admin test đã kích hoạt, KHÔNG bật 2FA) có 2 refresh token R1, R2 còn hiệu lực trên C1, lấy bằng luồng OAuth thật (authorize PKCE S256 → `POST /api/mcp/oauth/token`).<br>- Có phiên MySQL A nối tới DB của môi trường. Ghi giá trị cũ của `innodb_lock_wait_timeout` rồi `SET GLOBAL innodb_lock_wait_timeout = 5`. | 1. Phiên A: `BEGIN; SELECT * FROM oauth_refresh_tokens WHERE token = '<R1>' FOR UPDATE;`<br>2. Gửi `POST /api/mcp/oauth/refresh` bằng R1 (client_id, client_secret C1); sau 2 giây, phiên A chạy `ROLLBACK;`. Ghi HTTP status + thời gian phản hồi.<br>3. Gọi refresh lại bằng R1.<br>4. Đếm số token còn hiệu lực của U trên C1 (N1).<br>5. Phiên A: `BEGIN; SELECT * FROM oauth_refresh_tokens WHERE token = '<R2>' FOR UPDATE;` — giữ khoá tới khi bước 6 có phản hồi.<br>6. Gửi `POST /api/mcp/oauth/refresh` bằng R2; ghi HTTP status, body, số giây chờ. Sau đó phiên A `ROLLBACK;`.<br>7. Đếm lại số token còn hiệu lực của U trên C1 (N2).<br>8. Gọi refresh bằng R2.<br>9. Trả `innodb_lock_wait_timeout` về giá trị cũ. | Thời gian chờ khoá: 5 giây (tạm)<br>Giữ khoá B1: 2 giây (dưới ngưỡng)<br>Giữ khoá B5: tới khi request trả về (vượt ngưỡng) | - B2: HTTP 200 có refresh_token mới; thời gian phản hồi ≈ 2 giây.<br>- B3: HTTP 400 `{"error":"invalid_grant","error_description":"Refresh token has expired or been revoked."}`.<br>- B6: request kết thúc (ghi số giây), HTTP 500 JSON `{"error":"server_error"}`; body không có HTML, stack trace, câu SQL hay token.<br>- B7: N2 = N1 (request B6 không sinh token mới).<br>- B8: HTTP 200 (R2 không bị thu hồi dở sau lỗi ở B6). | | Lấp G2 / Q3 · Boundary = thời gian giữ khoá dưới / vượt `innodb_lock_wait_timeout` · Deadlock thật không dựng được bằng thao tác tay; nhánh chạy lại sau deadlock dựa vào unit test `tests/Unit/McpRefreshTokenDeadlockT15Test.php` — Dev xác nhận test chạy trong CI · Đánh giá spec: Spec không ghi — HTTP 500 `server_error` lấy theo phản hồi thật của `/api/mcp/oauth/token` ở run #7914; Dev xác nhận mã lỗi + số giây tối đa trước khi chạy · Không chạy prd vì giữ khoá DB · Evidence: status + body + thời gian từng request, kết quả đếm N1 / N2 |
| TC-ENV001-01 | Data | ENV-001 | MCP OAuth (`/api/mcp/oauth/token`, `/api/mcp/oauth/refresh`): giám sát deadlock sau release trên production | Normal | manual | prd | web | 7 ngày sau release không còn exception deadlock ở bảng `oauth_refresh_tokens` | - Bản sprint #45229 đã release production.<br>- Có quyền xem room Chatwork SNSLineException và dashboard check-exception.<br>- Tra trước trên Redmine #42266 mốc trước release: số lần cảnh báo, server, thời điểm đầu / cuối. | 1. Ghi giờ release.<br>2. Mỗi ngày trong 7 ngày, lọc dashboard check-exception theo `Deadlock found` / `SQLSTATE[40001]` / `1213`.<br>3. Giữ lại các exception có câu SQL chạm `oauth_refresh_tokens`; ghi URL request, server, thời điểm.<br>4. Cùng ngày, lọc HTTP 500 của `/api/mcp/oauth/token` và `/api/mcp/oauth/refresh`. | Thời gian theo dõi: 7 ngày<br>Signature: `Deadlock found` · `SQLSTATE[40001]` · `1213` | - Không có exception deadlock nào ở `oauth_refresh_tokens` trong 7 ngày.<br>- Không có HTTP 500 ở `/api/mcp/oauth/token`, `/api/mcp/oauth/refresh` do lỗi DB.<br>- Nếu có: danh sách URL + server + thời điểm, mở lại #42266 kèm dữ liệu này. | | Lấp G3 / Q2 · chỉ prd vì deadlock chỉ xảy ra dưới tải thật nhiều web server · manual vì chỉ chạy trên production · Surface web vì phán quyết đọc trên dashboard trình duyệt · Input thiếu: số lần cảnh báo của #42266 trước release (tra Redmine) · Đánh giá spec: không áp dụng · Evidence: ảnh dashboard 7 ngày |

**Không đề xuất TC mới (có lý do):**
- **Q4** (`DATA-DB-001`) · **Q5** (`REG-SHARED-001`): nội dung đã có ở NEW-769 / 770 / 686 — chỉ đổi / gắn thêm mã. Đổi mật khẩu ở アカウント設定 không thu hồi refresh token MCP (Leader chốt 2026-11-19) → không cần TC cho nơi gọi thứ 3.
- Đổi mã quan điểm (không cần TC mới): NEW-684 → `CONC-001` · NEW-769 → `DATA-DB-001` (+ `REG-SHARED-001`) · NEW-770, NEW-686 gắn thêm `SEC-002`.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/login-user/feature-spec.md` — SCR-LGN-06 đặt lại mật khẩu (`POST /confirm_password`) | Thêm rule: đặt lại mật khẩu thu hồi toàn bộ refresh token MCP của user (mọi client), kể cả token phát ra trong lúc đặt lại; user khác không bị ảnh hưởng | Spec im lặng — rule chỉ có ở requirement Studio REQ-T2-MCP-MOBILE-03 / REQ-T15-OTHER-03 (§5 I3) | `Dev` |
| 2 | Spec アカウント設定 (`/admin/setting`) — đổi mật khẩu | Ghi rule đã chốt: đổi mật khẩu ở アカウント設定 **không** thu hồi refresh token MCP (chỉ đặt lại mật khẩu mới thu hồi). Sửa tiêu đề REQ-T2-MCP-MOBILE-03 trên Studio cho khớp | Leader chốt 2026-11-19 · §5 I6 | `Leader` (đã chốt) |
| 3 | Chưa có spec MCP OAuth (`/api/mcp/oauth/token`, `/api/mcp/oauth/refresh`) | Refresh token xoay vòng 1 lần; mã lỗi `invalid_grant` từng trường hợp; mã lỗi khi DB lỗi / hết lượt chạy lại (500 `server_error`?) | §5 I3, TC-CONC001-01 | `Dev` |

---

## 9. Main cases (`/pick-maincase`)

<!-- generated: /pick-maincase 2026-11-19 · pool: Studio task #560 (6 TC lọc REQ-X-42266-* + REQ-T15-OTHER-03) + §7 report này (3 TC chưa trên tool) -->

### 9.0 Tóm tắt

| Mục | Giá trị |
|---|---|
| Loại task | Fix bug — exception production do AI phát hiện (deadlock khi INSERT `oauth_refresh_tokens`); có commit fix `46cf693fa6` (thu hồi theo khoá chính từng lô + transaction `/token` `/refresh` chạy lại) |
| Bộ TC | 9 TC (Studio: 6 · §7 chưa trên tool: 3) |
| Main case | 6 TC (67% bộ TC) · Bắt buộc sau release: 2 |
| Slot chưa có main case | 0 |
| Input thiếu | `03-dev-impact.md` không có mục riêng #42266 |

Tỉ lệ 67% vượt mức gợi ý ~20% vì pool của 1 ticket chỉ có 9 TC; đã rà lại, mỗi case giữ slot riêng. NEW-683 bỏ ra vì NEW-684 (a) đã phủ refresh đồng thời nhiều token của cùng user.

### 9.1 Main cases (6)

| # | TC ID | Slot | Tên case | Surface | Môi trường chạy | Sau release | Tiêu chí đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 1 | NEW-684 | B1, B4 | Tải trộn 60 giây: 10 luồng refresh + 2 luồng gửi lại code đã dùng (thu hồi theo user + client) — không 500, token user V không bị đụng | api | local · đề xuất: dev, local, staging (seed token + tải 60 giây) | Không — tải đồng thời + seed DB | C1 BUG #42266 · REQ-X-42266-03 · `/refresh` + `/token` đều đi qua transaction chạy lại · C2 `CONC-001` Cao · C4 DB + log | Đúng kịch bản gốc · ⚠️ chưa đo deadlock có xảy ra (§5 I5) |
| 2 | NEW-770 | B2 | Đặt lại mật khẩu ⇒ thu hồi mọi refresh token MCP của user (2 client); token user khác vẫn dùng được; token cấp sau đặt lại dùng được | api, web | dev, local, prd, staging | Không — đổi mật khẩu tài khoản test; prd do #3 kiểm `/token` + `/refresh` | C1 REQ-T15-OTHER-03 · nơi gọi `revokeForUser` thứ 2 · C2 `SEC-002` / `DATA-DB-001` Cao · C3 luồng đặt lại mật khẩu thật · C4 refresh sau đặt lại | Đạt local 13/11 |
| 3 | NEW-769 | B3a | Gửi lại code đã dùng ⇒ chỉ thu hồi token của đúng user + client; client khác và user khác vẫn dùng được | api | dev, local, prd, staging | Bắt buộc — `/token` đang trả 500 trên dev (run #7914) chưa rõ nguyên nhân; xác nhận cấp + làm mới token trên prd | C1 REQ-T15-OTHER-03 · Dev nói "phạm vi thu hồi giữ như trước" → expected theo rule (C2 vẫn 200, V vẫn 200) · C2 `DATA-DB-001` Cao · C7 tuần tự, ít dựng | Đạt local 13/11 · mã `TOOL-NEGCTRL-001` → đổi `DATA-DB-001` |
| 4 | NEW-685 | B3b | Gửi song song cùng 1 refresh token × 5 vòng: mỗi vòng đúng 1 request 200, còn lại 400 invalid_grant | api | dev, local, prd, staging | Không — Abnormal đồng thời; chạy staging | C1 REQ-X-42266-02 · rủi ro hồi quy thu hồi atomic #45157 khi transaction chạy lại · C2 `CONC-001` Cao | ⚠️ fail dev 17/11 ở bước lấy token, chưa gắn bug (§5 I1) · DUP-1 với NEW-360 |
| 5 | TC-SEC002-01 (chưa trên tool) | B3c | Đặt lại mật khẩu trong lúc 10 luồng đang refresh: sau đó không token cũ nào dùng được | api, web | dev, local, staging | Không — tải đồng thời + seed token | C1 G1 — hành vi thu hồi đổi sang đọc-rồi-UPDATE từng lô · Dev ngầm khẳng định "đặt lại vẫn thu hồi toàn bộ" · C2 `SEC-002` Cao | Lỗi bảo mật nếu có token sống sót ⇒ không release |
| 6 | TC-ENV001-01 (chưa trên tool) | B6 | 7 ngày sau release không còn exception deadlock ở `oauth_refresh_tokens`, không 500 ở `/token` `/refresh` do lỗi DB | web | prd | Bắt buộc — deadlock chỉ thấy trên prd | C1 BUG #42266 · C2 `ENV-001` Cao · C5 đúng hạ tầng nhiều web server | `manual` vì chỉ chạy trên production |

**TC trong pool không chọn (3):**
- NEW-683: refresh đồng thời 5 token khác nhau của cùng user — đã nằm trong luồng (a) của NEW-684.
- NEW-686: đặt lại mật khẩu với 1.201 token (biên số lô) — biên phụ của cách cài đặt; rule "thu hồi toàn bộ" đã kiểm ở #2 và #5.
- TC-CONC001-01: Boundary giữ khoá DB — chạy ở vòng regression đầy đủ, không nằm trong tập nhỏ nhất.

### 9.2 Slot chưa có main case (0)

Không có.

### 9.3 Slot không áp dụng

| Slot | Lý do |
|---|---|
| B4b | Đổi mật khẩu ở アカウント設定 không gọi `revokeForUser` — Leader chốt 2026-11-19 không thu hồi refresh token MCP. Nơi gọi chỉ còn đặt lại mật khẩu (B2) và gửi lại code đã dùng (B1, B3a) |
| B5 | #42266 không đổi schema hay format token; deadlock làm transaction rollback, không để lại dữ liệu sai — token phát trước release dùng như cũ |

### 9.4 TC cần sửa trước khi chạy

| TC ID | Vấn đề | Cần sửa |
|---|---|---|
| NEW-684 | Expected B3 không bắt buộc deadlock đã xảy ra → có thể Đạt mà không kiểm nhánh chạy lại. Mã `TOOL-KNOW-002` không có trong checklist | Thêm bước đếm `lock_deadlocks` trước / sau tải (§5 I5); đổi mã sang `CONC-001` |
| NEW-685 | Fail dev ở bước lấy token (500), chưa gắn bug | Xử lý §5 I1, chạy lại trên dev + staging |
| NEW-769 | Mã `TOOL-NEGCTRL-001` không có trong checklist | Đổi sang `DATA-DB-001` (+ `REG-SHARED-001`) |
| TC-SEC002-01 · TC-ENV001-01 | Chưa có trên tool | `/sync-review-tc` sau khi Leader duyệt; Dev xác nhận rule ở §8 #1 trước khi chạy TC-SEC002-01 |
