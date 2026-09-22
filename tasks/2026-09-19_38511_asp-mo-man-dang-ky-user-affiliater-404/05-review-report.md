# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #193 (ticket 38511, round 1, branch `ai_fixbug_38511`) |
| Tổng số TC review | 8 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 3/8 vùng ảnh hưởng đủ TC · 0 GAP · 5 RISK · 1 vùng có TC nhưng **Không đạt** (mã hashid rác — NEW-4, xem §4 I1).

> Diff (Studio `spec_delta`): 1 file `app/Http/Controllers/Aff/AffiliateController.php`, +2 / −3 — bỏ `where role IN (0,1)` khỏi validator `exists_admin` của `AffiliateController::regist`.
> **Vấn đề chính**: vùng có đủ TC về nội dung, nhưng **cả 4 TC verify fix đều `skip`** (NEW-1, NEW-2, NEW-3, NEW-9). Hiện chỉ có kết quả của các TC phụ, còn chính fix thì chưa được chạy lần nào.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — ca lỗi thật trong ticket: owner B mã `vO3nqdjKW2Z8` (user id 409) bị 404 | `dev-impact` | NEW-9 (dựng owner role 2 giả định) — `skip` | RISK — chưa TC nào tái hiện bằng **đúng mã trong ticket**. Dev **chưa xác nhận role của user 409** (DB không kết nối được) → nếu 409 không phải role -1/2 thì TC dựng dữ liệu giả sẽ pass mà bug thật vẫn còn | `[MAJOR]` |
| G2 | `F1` nhánh mới — owner role 2 / role -1 mở được màn đăng ký | `diff code` | NEW-1 (role 2), NEW-2 (role -1) — cả 2 `skip` | RISK — chưa chạy. Có TC nhưng không có kết quả | `[MAJOR]` |
| G3 | `F1` nhánh cũ — owner role 0/1 vẫn mở được (fix không phá chỗ cũ) | `diff code` | NEW-3 — `skip` | RISK — chưa chạy; tiền đề có "role 1" có thể không tồn tại (xem §4 I7) | `[MAJOR]` |
| G4 | `T1` — hành vi MỚI đi hết chuỗi: owner role 2 đăng ký affiliater thành công rồi đăng nhập được | `diff code` (câu 4 — nới guard) | NEW-8 `pass` nhưng tiền đề "chủ bot tồn tại" không ghi role → thực tế chạy trên owner cũ | RISK — hành vi mới chỉ được test tới bước **mở màn**. Chưa có TC nào tạo affiliater dưới owner role 2/-1 rồi kiểm tài khoản đó dùng được | `[MAJOR]` |
| G5 | `T2` — URL hướng dẫn copy từ ASP管理 dùng được với owner mới | `dev-impact` | NEW-9 — `skip`, `manual` | RISK — chưa chạy. Không đề xuất TC mới — xem §5 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 4 quan điểm có Trigger khớp task (FUNC-001 · PERM-001 · OUT-TRUTH-001 · COMPAT-LEGACY-001) · 4 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | GAP theo mã quan điểm — TC luồng chính mang mã lạ (NEW-1, NEW-9 = `TOOL-KNOW-002`; NEW-2 = `RULE-09`; NEW-4, NEW-5 = `TOOL-NEGCTRL-001`) nên không được tính là cover. Về nội dung thì đã đủ: Normal (NEW-9/NEW-1), Abnormal (NEW-5), Boundary (role -1 / 2 là giá trị ngay ngoài tập role cũ `IN (0,1)` → NEW-1, NEW-2 thực chất là Boundary). **Cách sửa: đổi mã trên Studio, không viết TC mới** | `[BLOCKER]` |
| Q2 | `PERM-001` | Cao | RISK — fix thay đổi role nào được làm owner của màn đăng ký, nhưng **không có role matrix trong spec** (Input thiếu). NEW-1/2/3 cover đủ -1 / 0 / 1 / 2 về nội dung nhưng mang mã lạ và đều `skip` | `[MAJOR]` |
| Q3 | `OUT-TRUTH-001` | Cao | RISK — chỉ có Abnormal (NEW-7). Normal đang nằm ở NEW-8 nhưng mang mã `RULE-07`, và chạy trên owner cũ. Thiếu Boundary: owner **chưa từng có cấu hình affiliate** (`user_setting_aff = null`) đang bị nhét chung vào NEW-7 như 1 biến thể | `[MAJOR]` |
| Q4 | `COMPAT-LEGACY-001` | Cao | RISK — NEW-3 mang mã này nhưng nội dung là role cũ, không phải link cũ. URL login đang là `/aff/v2/login/...` → có thể còn bản v1. **Input thiếu**: màn login affiliater v1 còn dẫn sang `/affiliate/{mã}/regist` không? | `[MAJOR]` |

Đã loại khỏi phạm vi:
- `REG-URL-001`: danh sách URL của quan điểm này là URL đo conversion của LME (`/register/success`, `/basic/overview`...), không phải màn affiliater.
- `DATA-DB-001`: fix không có UPDATE/DELETE, luồng `createNewAff` không bị sửa.
- `FUNC-002` / `SEC-002`: form nhập + mật khẩu không nằm trong diff (root cause ở tầng guard mở màn).

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-9 | NEW-1 (gộp) | `DUP-SUBSET` | cùng quan điểm luồng chính × Normal × mở `/affiliate/{mã}/regist` của owner role 2 × `is_register_new_affiliate = 1` → cùng expected (form 3 ô + nút 「アカウント登録」). NEW-9 đi thêm đoạn ASP管理 → login trước khi tới đúng URL đó | `[MINOR]` |

- **Gate đã chạy**: xóa NEW-1 thì role 2 vẫn được cover bởi NEW-9 → coverage §1 / §2 còn nguyên. **Điều kiện**: NEW-9 phải chuyển sang `auto` và đã chạy `pass` (§4 I9). Chưa làm được thì giữ cả 2.
- NEW-4 vs NEW-5 **không trùng**: dữ liệu khác nhau (mã không decode được vs mã decode ra id không tồn tại), và đi qua 2 nhánh code khác nhau.
- Không có `DUP-INFLATE` / `DUP-CONFLICT`.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-4 | TC `fail` (mã hashid rác không trả 404) nhưng **chưa raise ticket** (`bug_tickets` rỗng). `dev_impact` trên Studio xác nhận đúng hành vi này: *"Hashids::decode trả mảng rỗng → count==0 → không vào nhánh validator → không ra 404 qua validator"*. Diff chỉ bỏ điều kiện role, nên nhiều khả năng lỗi này **có từ trước fix**, không phải do fix gây ra | Raise ticket riêng (ghi rõ đã có trước fix #38511 hay chưa, sau khi chạy lại trên branch release cũ). Chốt expected ở §6 #1 |
| I2 | `[BLOCKER]` | Toàn bộ | Tỷ lệ pass 3/8 = 37,5% (< 50%). 4 TC `skip` đều là TC verify fix (NEW-1/2/3/9) → **fix chưa được verify** | Chạy lại NEW-1, NEW-2, NEW-3, NEW-9 trên staging sau khi deploy `release_step_20260827`; đọc `task_get_report` để biết vì sao run #1718 skip |
| I3 | `[MAJOR]` | Spec | `spec-features/` **không có spec** cho màn đăng ký affiliater (`ASP管理 紹介者（登録）`) và màn ASP管理. `LME-SYSTEM-SPEC.md` chỉ có 1 dòng *"Affiliater — Guard riêng `/affiliate/*`"*. Expected hiện tại đều do AI suy từ code | Xem §6 #3. Trước mắt Leader xác nhận expected của NEW-4 và NEW-7 |
| I4 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine, checkbox "Tester verify auto-fill chính xác" **chưa tick** | Tester đọc lại Journal #131962 rồi tick |
| I5 | `[MAJOR]` `[AP-2]` | `BUG` | Root cause "owner role -1/2" là **suy luận từ code**, Dev ghi rõ không dump được role của user 409 | Hỏi Dev / tra DB staging role của user 409 trước khi đóng ticket. Chạy TC-FUNC001-01 (§5) với đúng mã trong ticket |
| I6 | `[MAJOR]` | NEW-1, NEW-2, NEW-4, NEW-5, NEW-8, NEW-9 | 6/8 TC mang mã **không có** trong `framework/checklist-lme.md` (`TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `RULE-09`, `RULE-07` — 2 mã sau là tên RULE, không phải quan điểm) | Sửa trên Studio (`testcase_update`): NEW-1/2/9 → `FUNC-001` (NEW-1, NEW-2 đổi `case_type` = Boundary); NEW-4/5 → `FUNC-001` Abnormal; NEW-8 → `OUT-TRUTH-001` |
| I7 | `[MAJOR]` | NEW-3 | Tiền đề cần "chủ bot role = 1 (user paid)", nhưng spec [login-user db-mapping](../../spec-features/admin/login-user/db/db-mapping.md) ghi DB comment chỉ có `-1/0/2`, **chưa rõ có row nào `role=1`** → TC có thể không dựng được dữ liệu | Hỏi Dev role 1 có tồn tại không. Nếu không có → bỏ biến thể role 1, ghi lý do ở `note` |
| I8 | `[MAJOR]` | NEW-5, NEW-7, NEW-8 | Chưa có evidence (RULE-02): Studio không trả về evidence cho các TC `pass` (NEW-5, NEW-7, NEW-8) | Đính kèm screenshot + status code (NEW-5), screenshot thông báo + tài khoản tạo được (NEW-8) |
| I9 | `[MINOR]` | NEW-9 | `exec_mode = manual` nhưng không thuộc 4 lý do được phép (production / thiết bị thật / mail thật / mắt người) — toàn bộ các bước làm được trên browser tự động | Đổi sang `auto` |
| I10 | `[MINOR]` | NEW-8 | Expected "giao diện hiển thị kết quả đăng ký thành công" không đo được — không ghi thông báo cụ thể hay màn chuyển tới | Ghi rõ nội dung thông báo / URL sau khi đăng ký |
| I11 | `[MINOR]` | NEW-5 vs NEW-4 | Oracle không thống nhất: NEW-5 dùng "Validator exists_admin thất bại (count == 0) → redirect màn 404" (chi tiết code, tester không quan sát được), NEW-4 dùng "HTTP status 404" | Viết lại expected NEW-5 theo điều quan sát được: status 404 + không có form |
| I12 | `[NIT]` | NEW-3 | Gộp role 0 và role 1 trong 1 TC → fail thì không biết role nào hỏng | Tách 2 TC (nếu role 1 tồn tại — I7) |

---

## 5. TCs đề xuất bổ sung (3)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | kho-tcs chưa có tính năng ASP管理 / đăng ký affiliater — không đối chiếu được. Đã grep `fa031-billtientool` (nhắc affiliate ở phần hoa hồng `payment_detail_aff`) và `fa033-backup` (filter アフィリエイター) — không liên quan màn đăng ký |
| Vùng regression phát hiện từ kho | Không có |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Xác nhận chống trùng | Đã đối chiếu 8 TC trên Studio + kho — **không TC đề xuất nào trùng**. TC-FUNC001-01 khác NEW-9 ở dữ liệu (mã thật trong ticket, không dựng owner giả); TC-OUTTRUTH001-01 đi tiếp sau NEW-1 (submit + đăng nhập); TC-OUTTRUTH001-02 tách biến thể `null` khỏi NEW-7 và làm trên owner role mới |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Màn login affiliater → màn đăng ký affiliater | Normal | auto | staging | Tái hiện ticket #38511: mở màn đăng ký từ link login của owner B (`vO3nqdjKW2Z8`) không còn 404 | - Staging đã deploy `release_step_20260827`<br>- Owner B (mã `vO3nqdjKW2Z8`, user id 409) và owner A (mã `eaNArJeWyE27`, user id 2) vẫn còn trên staging | 1. Mở `https://staging.lme.jp/aff/v2/login/vO3nqdjKW2Z8`<br>2. Tại màn login affiliater, bấm liên kết sang màn đăng ký<br>3. Quan sát URL và nội dung màn<br>4. Lặp lại bước 1–3 với `https://staging.lme.jp/aff/v2/login/eaNArJeWyE27` (đối chứng) | Mã owner B `vO3nqdjKW2Z8` · mã owner A `eaNArJeWyE27` | - Owner B: URL chuyển sang `/affiliate/vO3nqdjKW2Z8/regist`, màn 「ASP管理 紹介者（登録）」 hiển thị, **không** ra trang 404. Nếu owner B đang bật nhận thành viên → thấy form 「お名前」「メールアドレス」「パスワード」 + nút 「アカウント登録」; nếu đang tắt → thấy thông báo 「現在、新規アフィリエイターの登録を停止しています。」<br>- Owner A: vẫn mở được như trước fix | | Lấp G1, Q1 · Đánh giá spec: Spec không ghi (theo Expected của ticket) · Evidence: screenshot 2 màn + URL · Nếu owner B vẫn 404 sau fix → root cause của Dev sai (I5) |
| TC-OUTTRUTH001-01 | UI | OUT-TRUTH-001 | Màn đăng ký affiliater — đăng ký tài khoản | Normal | auto | staging | Owner role 2 (staff): đăng ký affiliater thành công và đăng nhập được bằng tài khoản vừa tạo | - Có owner role 2 (staff) đang bật nhận affiliater mới (「新規アフィリエイターの登録」 = bật)<br>- Có mã owner của user này (copy từ ASP管理)<br>- Chuẩn bị email chưa từng đăng ký affiliater dưới owner này | 1. Mở `/affiliate/<mã owner role 2>/regist`<br>2. Nhập 「お名前」「メールアドレス」「パスワード」<br>3. Bấm 「アカウント登録」 → ghi lại thông báo hiển thị<br>4. Mở `/aff/v2/login/<mã owner role 2>`, đăng nhập bằng email + mật khẩu vừa đăng ký<br>5. Mở màn ASP管理, chọn owner role 2, xem affiliater vừa tạo | お名前: `山田 花子` · メール: `qa38511-staff-<timestamp>@example.com` · パスワード: `Aff38511pass` | - Bước 3: báo đăng ký thành công, không lỗi<br>- Bước 4: đăng nhập thành công vào trang affiliater của owner role 2<br>- Bước 5: affiliater vừa tạo nằm dưới **đúng owner role 2** (không rơi sang owner khác / admin cha)<br>- Đăng ký lần 2 cùng email → không tạo thêm tài khoản | | Lấp G4, Q3 · Đánh giá spec: Spec không ghi — chờ §6 #2 chốt affiliater của owner staff thuộc về ai · Evidence: screenshot thông báo + màn sau đăng nhập + màn ASP管理 · RULE-07: kiểm thêm bản ghi `affiliaters` đúng `admin_id` |
| TC-OUTTRUTH001-02 | UI | OUT-TRUTH-001 | Màn đăng ký affiliater — trạng thái nhận thành viên | Boundary | auto | staging | Owner role 2 chưa từng có cấu hình affiliate: màn mở được nhưng báo tạm dừng, không có form | - Có owner role 2 (staff) **chưa từng mở / lưu** cài đặt affiliate (chưa có cấu hình nhận thành viên)<br>- Có mã owner của user này | 1. Mở `/affiliate/<mã owner role 2 chưa cấu hình>/regist`<br>2. Quan sát nội dung khối form | Owner role 2 chưa có cấu hình affiliate | - Màn 「ASP管理 紹介者（登録）」 mở được, **không** 404, không lỗi 500<br>- Hiển thị 「現在、新規アフィリエイターの登録を停止しています。」<br>- **Không** có 3 ô nhập và không có nút 「アカウント登録」 | | Lấp Q3 · Đánh giá spec: Spec không ghi (theo `member_add.blade.php` Dev dẫn) · Evidence: screenshot · Tách biến thể `null` khỏi NEW-7 và làm trên owner role mới — trước fix nhánh này không đi tới được với role 2 |

**Các dòng §1 / §2 không đề xuất TC mới:**
- **G2, G3, G5, Q1, Q2** — TC đã có đủ nội dung (NEW-1, NEW-2, NEW-3, NEW-9). Việc cần làm là **đổi mã quan điểm + chạy lại** (§4 I2, I6, I9), không viết thêm TC trùng.
- **Q4** — chưa biết màn login affiliater v1 còn tồn tại không, nên không viết TC. Dev xác nhận có thì bổ sung 1 TC: *login v1 → màn đăng ký của owner role 2*.

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | Màn đăng ký affiliater — xử lý mã owner không hợp lệ | Mã hashid rác (không decode được) phải ra 404 hay được phép render? Requirement REQ-002 / NEW-4 mong đợi 404; code thực tế (theo `dev_impact`) bỏ qua validator → NEW-4 `fail` | NEW-4 expected vs `dev_impact` Studio | Dev / Leader |
| 2 | Quy tắc owner ASP | Owner role 2 (staff) / role -1 (super admin) có được làm owner nhận affiliater không? Affiliater + hoa hồng (`payment_detail_aff`) của owner staff thuộc về staff hay admin cha? Dev kết luận guard role 0/1 "không phải quy tắc nghiệp vụ" nhưng không có spec xác nhận | Nhận định của Dev (Journal #131962) — không có spec đối chiếu | PM / Leader |
| 3 | `spec-features/` | Chưa có feature-spec cho ASP管理 và đăng ký / login affiliater (`/affiliate/*`, `/aff/v2/*`). Cần bổ sung, gồm role matrix owner (PERM-001) và việc còn màn login v1 hay không (Q4) | Không có nguồn spec | Leader |
