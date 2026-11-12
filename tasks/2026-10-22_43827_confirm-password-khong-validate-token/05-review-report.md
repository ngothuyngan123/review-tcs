# 05 — Review Report

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) MCP LME TEST STUDIO — task #505, ticket 43827 |
| Tổng số TC review | 25 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 13/13 mục có TC — **ĐỦ (về thiết kế)** |
| **(b) diff code** — suy từ diff thật (Studio `dev_impact` + `spec_delta`, 3 file) | 3/3 file + hành vi mới có TC — **ĐỦ (về thiết kế)** |

**Kết luận**: Thiết kế đủ coverage cả 2 chiều, **0 GAP** vùng ảnh hưởng. ⚠️ Nhưng **0/25 TC đã chạy** → mọi kết luận "Đạt" đều chưa có bằng chứng thực thi (RISK thực thi — xem §5 I1), và 5 TC luồng mobile **dự kiến FAIL** vì nhánh fix chưa implement (xem §5 I2). 2 dòng RISK quan điểm ở §2.

- dev-impact 13 mục đều có TC: `BUG` (id-bypass) = NEW-11 · `F1 confirmPassword` = NEW-9/11/12/13/14/15/16/19 · `F2 v3 blade (token thay id)` = NEW-1 (verify payload có token, không id) · `F3 v2 blade` = NEW-2 · `D1 password`/`D2 reset_token=null`/`D3 is_active`/`D4 remember_token_reset_pass`/`D5 oauth_refresh_tokens.is_revoked` = NEW-9 · `T1 reset v2` = NEW-2/6 · `T2 reset v3` = NEW-1/5 · `T3 session sau đổi` = NEW-3 · `T4 mobile change_password` = NEW-20/22/23/25/21.
- diff 3 file đều có TC đi qua: `AuthController@confirmPassword` (validate token + hạn 24h + định danh theo token) = NEW-9/11/12/14/18/19 · `reset-password-v3.blade.php` = NEW-1 · `reset_password_v2.blade.php` = NEW-2. Hành vi mới (siết: thiếu token → từ chối) có cả 2 nhánh true/false (NEW-9 hợp lệ 200 · NEW-11/12 thiếu/sai token → từ chối).

---

## 2. Thiếu so với quan điểm test

**Kết luận**: ~15 quan điểm Trigger khớp task · **2 chưa cover đủ** (đều ở mức RISK — có TC cho feature chính, thiếu sibling/sub-scenario).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `REG-SHARED-001` | Cao | RISK — bug pattern "không kiểm hạn token lúc submit" còn ở sibling **V1 web `POST /change_password` (EP-16)**: spec chỉ validate `token exists`, KHÔNG kiểm 24h, KHÔNG clear `reset_token` (S-10). Mobile sibling đã có TC (NEW-22/23/25), web V1 thì chưa. | `[MAJOR]` |
| Q2 | `CONC-001` | Cao | RISK — token dùng-1-lần đã cover tuần tự (NEW-4 tab2, NEW-14 reuse) nhưng **thiếu kịch bản 2 request song song cùng token** (race, scenario 4 của CONC-001). NEW-14 ghi chú chủ động hoãn với lý do "hậu quả thấp". | `[MINOR]` |

> Các quan điểm Cao khác đã cover đủ (không ghi): FUNC-001, FUNC-003, FUNC-DATE-001 (biên 23h59/24h: NEW-18/19/25), DATA-DB-001 (WHERE scope 2 tài khoản: NEW-9 control C + NEW-13), PERM-002 (NEW-11/12/17), SEC-001 (cross-account NEW-13), SEC-002 (log NEW-10), STATE-CLEAN-001 (NEW-9), DEPLOY-LIVE-001 (NEW-24), COMPAT-LEGACY-001 (v2 cũ NEW-2/6), SYNC-APP-001 (mobile NEW-20/22/23/25). NOTI-MAIL-001 KHÔNG tính (fix không chạm luồng gửi mail).

---

## 3. TC trùng lặp nội dung

Đã rà 25 TC, **không phát hiện trùng lặp**. Các cặp dễ nhầm đã kiểm và xác nhận KHÁC ý định:
- NEW-8 (UI: FE chặn + server báo trùng pass) vs NEW-15 (API: tầng BE độc lập) — khác **surface/layer**, bổ sung nhau.
- NEW-11 (id, không token → từ chối) vs NEW-12 (token sai/bịa + id) vs NEW-16 (token sai kiểu dữ liệu) — khác loại input abnormal.
- NEW-4 (UI tab2 reuse) vs NEW-14 (API reuse token) vs NEW-7 (GET mở lại link đã dùng → màn lỗi) — khác surface + bước.
- NEW-18/19 (web API biên 24h) vs NEW-25 (mobile biên 24h) — khác surface (web vs mobile).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A (TC/Studio) | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-11, NEW-12, NEW-14, NEW-19 (và ghi chú NEW-4/5/6/24) | Mã HTTP khi token thiếu/sai/hết hạn/đã dùng ở `POST /confirm_password` | Studio-internal-spec: **410** + FE chuyển SCR-LU-07 (các TC ghi "4xx" để treo chờ chốt) | repo `spec-features/.../web/api-spec.md` EP-12 = **422** `errors.token`; fix trả **422** | ✅ **ĐÃ CHỐT (2026-10-22): mã = 422** (khớp repo spec hiện hành; kỳ vọng 410 là Studio-internal, thuộc redesign SCR-LU-07 task 36016 chưa áp dụng) | `[MAJOR]` → **Resolved** | Leader (chốt 422) |

> ✅ **C1 đã xử lý (2026-10-22)**: NEW-12 (#31948), NEW-14 (#31950), NEW-19 (#31955) đã cập nhật trên Studio (`testcase_update`, version → 3) — `expected` + `data_input` đổi "4xx" → **422**, `note` ghi nhận đã chốt. NEW-11 vốn đã 422. Snapshot `04-tc-list.md` đã refresh khớp Studio. **NEW-16 KHÔNG đổi** — ô "4xx" ở đó là test token **sai kiểu dữ liệu** (mảng/object/số), thuộc I5 + RULE-13 ("400 hoặc 422"), không phải quyết định 410-vs-422 của C1.

**Đã rà**: 25 TC × `spec-features/admin/login-user/feature-spec.md` + `web/api-spec.md` (EP-12/EP-16) — phát hiện C1 (đã chốt 422). **`kho-tcs` chưa có FA-040 (login-user) → không đối chiếu được `CONF-KHO`.** Không có tính năng IGNORE nào bị nhắc → không có `CONF-IGNORE`.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ 25 TC (nguồn) | **Chưa chạy TC nào** (0 pass / 0 fail / 25 chưa chạy). "Có TC ≠ đã test" — coverage ở §1 mới là coverage *thiết kế*, chưa có kết luận Đạt. | Chạy bộ TC. Ưu tiên nhóm bảo mật core trước (NEW-9/11/12/13 — đổi pass qua `id`, cross-account), chạy được ở `env-safe`/`local`. |
| I2 | `[MAJOR]` | NEW-20, NEW-21, NEW-22, NEW-23, NEW-25 | **Nhánh fix efbc04e51f CHƯA implement luồng mobile** `/change_password` kiểm hạn 24h + ghi thời điểm phát hành token (critique #223, REQ-011/012). Studio `dev_impact` xác nhận "CHƯA có trong nhánh ⇒ TC dự kiến FAIL". → 4 TC sẽ FAIL (NEW-22/25/21 + biên), NEW-23 (đối chứng) phải giữ PASS. | Chốt scope: mobile fix thuộc task này (⇒ Dev bổ sung commit rồi mới chạy) hay task riêng (⇒ tách 5 TC sang task sau). Đưa §8. |
| I3 | `[MAJOR]` | NEW-4, NEW-5, NEW-6, NEW-24 | **UX gap do fix**: token hết hạn/không hợp lệ/trang mở trước release → BE trả 422 `errors.token` NHƯNG FE v2/v3 chỉ render `errors.password/repeat_password` → người dùng **không thấy thông báo** (spinner tắt, đứng im). Phần bảo mật (không đổi pass) PASS; phần "phản hồi rõ ràng" (REQ-006, SCR-LU-07, BR-20) FAIL. | Chốt: sửa FE render `errors.token` / chuyển SCR-LU-07, hay chấp nhận tạm (secure nhưng im lặng) chờ redesign task 36016. Đưa §8. |
| I4 | ~~`[MAJOR]`~~ → **Resolved** | NEW-12, NEW-14, NEW-19 | **RULE-13**: 3 TC ghi chung "4xx". | ✅ **Đã xử lý 2026-10-22** — Leader chốt C1 = 422; đã `testcase_update` expected/data_input "4xx" → **422** trên Studio (v→3), snapshot refresh. |
| I5 | `[MINOR]` | NEW-16 | Expected trộn `422` và `4xx` trong cùng TC (test token sai kiểu dữ liệu: mảng/object/số); có "quan sát thêm" (mảng 1 phần tử token thật có thể được chấp nhận; 2 token → nguy cơ 500) ở ghi chú nhưng chưa thành bước/expected rõ. **Chưa đổi** — khác bản chất C1 (datatype, không phải 410-vs-422). | Theo RULE-13, chuẩn hóa các dòng token mảng/object/số thành `400 hoặc 422` + "không 500"; nếu muốn kiểm nhánh 500 thì thêm 1 dòng dữ liệu riêng. **Cần Leader xác nhận** trước khi sửa trên Studio. |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 25 TC — **không có TC nào ngoài phạm vi task**.

- 5 TC mobile (NEW-20/21/22/23/25) **không** phải TC thừa: tuy nhánh hiện tại chưa chạm `/change_password`, chúng **dẫn trực tiếp từ Studio `dev_impact` + requirements REQ-011/012 (critique #223)** → thuộc phạm vi đã chốt (gate 4d: "regression dẫn được từ Studio → không flag"). Vấn đề thuộc **fix chưa đủ**, đã nêu ở §5 I2.
- NEW-23 (đối chứng âm) tuy "dự kiến PASS ngay cả trước fix" nhưng là **negative control bắt buộc** cho #223 (bảo đảm Dev sửa chỗ phát hành token không gây báo-hết-hạn-sai) → giữ.

---

## 7. TCs đề xuất bổ sung (2)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs` **chưa có FA-040 (login-user)** — không đối chiếu được |
| Vùng regression phát hiện từ kho | Không có (chưa có kho FA-040) |
| Conflict expected vs kho | Không (không có kho) |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R` | R1 ← Studio `dev_impact` "web V1 /postReset sinh cùng link /change_password, không ghi reset_token_expired" + repo spec EP-16 (chỉ validate `exists`, không kiểm hạn, S-10 không clear token) · R2 ← `CONC-001` Kiểm tra kịch bản (4) race + ghi chú NEW-14 chủ động hoãn |
| Xác nhận chống trùng | Đã đối chiếu 25 TC BƯỚC 0 — không TC nào test V1 web `/change_password` kiểm hạn, không TC nào bắn 2 request song song → **không trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | API | REG-SHARED-001 | Reset password V1 パスワード再設定(旧): API POST /change_password (EP-16) — kiểm hạn token 24h khi submit | Abnormal | auto | dev, local, staging | api | Gọi POST /change_password (V1) với token đã quá 24 giờ thì bị từ chối và mật khẩu tài khoản không đổi | Môi trường local, có quyền ghi DB slot.<br>User U (email riêng của run, ví dụ qa43827-v1-<runid>@example.com), mật khẩu hiện tại P1 (thoả quy tắc), có `reset_token = T_U`, thời điểm phát hành token (`reset_token_expired`) = hiện tại − 25 giờ (link quá hạn, chưa dùng).<br>Phiên ẩn danh có CSRF (GET /reset_password). | 1. Gửi POST /change_password (kèm CSRF) với `token = T_U`, `password = re-password = Rs43827!a`.<br>2. Ghi lại phản hồi (status, có/không redirect tới /change_password_success, lỗi hiển thị).<br>3. Query `users.password` và `users.reset_token` của U, so với giá trị trước bước 1.<br>4. Mở /login, đăng nhập U + Rs43827!a, sau đó U + P1. | token = T_U<br>phát hành token = hiện tại − 25 giờ<br>password = re-password = Rs43827!a | - Bước 2: KHÔNG redirect tới /change_password_success; request bị từ chối ở trường token (link hết hạn). Theo RULE-13 nếu trả JSON: **400 hoặc 422**; nếu V1 redirect-withErrors thì phải có lỗi token, không vào màn success.<br>- Bước 3: `users.password` của U KHÔNG đổi; không bị auto-login.<br>- Bước 4: U + Rs43827!a đăng nhập thất bại; U + P1 vẫn thành công. | | Lấp Q1 · regression · dẫn từ Studio dev_impact "web V1 /postReset sinh cùng link /change_password, không ghi reset_token_expired" + spec EP-16 chỉ validate token `exists`, KHÔNG kiểm 24h (S-10). ⚠️ Có thể NGOÀI scope nhánh này (Dev ghi "questions") — Leader chốt (đã nêu §8). Đánh giá spec: Spec không ghi (hành vi V1 chưa chốt). Evidence: status/body + query users.password & reset_token trước/sau + ảnh đăng nhập. manual không cần (runner gọi API + ghi DB ở local). |
| TC-CONC001-01 | API | CONC-001 | Reset password V2 パスワード再設定: API POST /confirm_password — 2 request song song cùng 1 token (race, token dùng 1 lần) | Abnormal | auto | dev, local, staging | api | Bắn 2 request /confirm_password đồng thời với cùng 1 token hợp lệ thì chỉ 1 đổi mật khẩu thành công, request còn lại bị từ chối | Môi trường local, có quyền đọc/ghi DB slot.<br>User A dành riêng cho test đặt lại mật khẩu, mật khẩu hiện tại P_A; `reset_token = T_A` hợp lệ (< 24h), chưa dùng.<br>Phiên ẩn danh có CSRF (GET /reset_password). | 1. Chuẩn bị 2 request POST /confirm_password (kèm CSRF, header AJAX) cùng `token = T_A`: request X có `password = repeat_password = Rs43827!a`; request Y có `password = repeat_password = Rs43827#b`.<br>2. Gửi X và Y gần như đồng thời (song song, chênh < 50ms).<br>3. Ghi lại HTTP status + body của cả X và Y.<br>4. Query `users.reset_token` của A.<br>5. Mở /login, đăng nhập A + Rs43827!a, rồi A + Rs43827#b, rồi A + P_A. | token = T_A<br>password X = Rs43827!a<br>password Y = Rs43827#b | - Bước 3: **đúng 1** request trả HTTP 200 (có redirect_url); request còn lại trả **400 hoặc 422** `errors.token` (token đã dùng). TUYỆT ĐỐI không có trường hợp cả X và Y cùng 200.<br>- Bước 4: `users.reset_token` của A = NULL.<br>- Bước 5: mật khẩu của request thành công đăng nhập được; mật khẩu request còn lại thất bại; P_A thất bại. | | Lấp Q2 · regression · dẫn từ CONC-001 Kiểm tra kịch bản (4) race + ghi chú NEW-14 chủ động hoãn ("không phủ 2 request song song"). Đánh giá spec: Spec ghi rõ (token dùng 1 lần — BR-17 / §6.6). Evidence: status/body 2 request + query reset_token + ảnh đăng nhập. manual không cần (runner bắn song song + ghi DB ở local). |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/login-user/web/api-spec.md` EP-12 + Studio BR-20/SCR-LU-07 | ✅ **ĐÃ CHỐT 422 (2026-10-22)** — khớp repo spec + fix; NEW-12/14/19 đã cập nhật trên Studio. Studio-internal-spec còn ghi 410 (thuộc redesign SCR-LU-07 task 36016) → nếu sau này làm redesign thì mới cần đổi. | §4 C1 (CONF-SPEC) | Leader (đã chốt) |
| 2 | SCR-LU-07 / REQ-006 (hiển thị lỗi token lúc submit) | Fix trả 422 `errors.token` nhưng FE v2/v3 không render → quyết định: sửa FE hiển thị lỗi (hoặc chuyển màn SCR-LU-07) **hay** chấp nhận tạm (im lặng nhưng vẫn an toàn) chờ redesign task 36016. | §5 I3 | Leader / PM |
| 3 | REQ-011 / REQ-012 — mobile `/change_password` kiểm hạn 24h + ghi thời điểm phát hành token (critique #223) | Chốt: luồng mobile có thuộc task #43827 không. Nếu có → nhánh `efbc04e51f` cần bổ sung commit (kiểm hạn ở `/change_password` + ghi `reset_token_expired` lúc `/api/mobile/send-link-reset-password`) trước khi NEW-20/21/22/23/25 chạy được. | §5 I2 | Leader / Dev |
