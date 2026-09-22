# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #235 (ticket 39231, round 3, branch `ai_fixbug_39231`) |
| Tổng số TC review | 57 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 3/12 vùng ảnh hưởng đủ TC (F1 · D1 · D4) · 1 GAP · 6 RISK.

> Loại khỏi phạm vi (Leader chốt 2026-09-19): `T3` "Đổi chủ quản lý chính của bot" — Dev đánh giá ảnh hưởng sai; kéo theo `F6` `acceptOwnerBot` (luồng đổi owner, Dev đề xuất ticket riêng). TC liên quan trên Studio: NEW-60 đã xóa · NEW-63 chờ xóa. Số `G6` bỏ trống, không đánh lại số.

> Diff (Studio `spec_delta`): 1 file `app/Http/Controllers/Admin/StaffManagementController.php` (+110 / −3). Coverage tính theo **run staging #1713 (2026-09-19)** — run duy nhất chắc chắn chạy sau commit tự review v1 `4e658d206e`. Run local #1673 (2026-09-18) có trước ngày journal ghi commit này nên **không** được tính là đã verify code hiện tại (cần Studio xác nhận run #1673 chạy trên commit nào).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — kịch bản gốc của ticket: LINE OA Standard hợp đồng mới 9 staff → người thứ 10 chấp nhận được, người kế tiếp bị chặn, số staff giữ 10 (+ `F5` / `T2` giới hạn 10 staff) | `dev-impact` | NEW-5 · NEW-6 · NEW-20 (· NEW-45 trùng) | RISK — cả 4 TC **skip** trên staging (kho tài nguyên chỉ có 1 tài khoản エルメ, không dựng được 9–10 staff). Chỉ pass ở run local #1673. Expected của ticket **chưa được verify trên code hiện tại** | `[BLOCKER]` |
| G2 | `F2` normalizeAcceptedBots bản v1 + `D2` user_staff_bots — vai trò / chủ sở hữu / người được mời / mã lời mời lấy từ bản ghi lời mời, không tin client | `diff code` | NEW-51 · NEW-52 · NEW-53 · NEW-54 · NEW-55 | RISK — 5 TC **chưa chạy lần nào ở môi trường nào** (skip #1713). NEW-13 cùng vùng đang **fail** (xem I1). Không có bằng chứng nào cho phần hardening bảo mật của v1 | `[BLOCKER]` |
| G3 | `F2` — mã liên kết người được mời (`user_staff_id`) theo TC note vẫn lấy từ client, chỉ kiểm khác rỗng | `diff code` | NEW-57 | RISK — NEW-57 `pass` nhưng expected chỉ là "không 500 + ghi lại hành vi thật", chưa có chuẩn đúng/sai → đẩy §6 #3 | `[MAJOR]` |
| G4 | `F3` getDetailInviteStaffByCode (EP-07) — `is_array(bot_role)` + bot thiếu owner vẫn hiện nhưng owner để trống | `dev-impact` | NEW-23 · NEW-24 · NEW-25 · NEW-27 · NEW-58 · NEW-3 | RISK — cả 6 TC skip trên staging (cần ghi DB để làm hỏng `bot_role`); NEW-58 (hành vi mới của v1) chưa chạy lần nào | `[MAJOR]` |
| G5 | `F4` markUserVisitedLinkInvite (EP-11) — `is_array` + bỏ qua item thiếu `user_id_root`, vẫn ghi cờ đã truy cập | `dev-impact` | NEW-28 (pass) · NEW-29 · NEW-30 · NEW-31 · NEW-59 · NEW-2 | RISK — chỉ NEW-28 (dữ liệu hợp lệ) pass; toàn bộ nhánh dữ liệu hỏng + nhánh UI 「承認せずにキャンセルする」 skip; NEW-59 (hành vi mới v1) chưa chạy lần nào | `[MAJOR]` |
| G7 | `D3` / `D4` — chốt chặn trả lỗi sớm: không bật `is_confirmed`, **không xoá session luồng mời**; màn hình hiện thông báo mới | `diff code` | NEW-4 (UI) · NEW-17 · NEW-42 · NEW-62 (API, pass) | RISK — đường UI duy nhất ra thông báo mới (NEW-4) skip trên staging; không TC nào verify phía UI rằng session còn giữ (tải lại trang chủ → modal hiện lại → duyệt lại được) | `[MAJOR]` |
| G8 | `T1` — regression phần sau chốt chặn của luồng accept (Studio `dev_impact`: "Regress toàn luồng accept … race-guard, Firebase, is_confirmed=1, limit 10"): BR-003 race-guard · BR-010 log `BotLifeCycle type=24` · BR-011 đăng ký Firebase topic | `diff code` | NEW-18 (· NEW-43 trùng) cho BR-003, skip | GAP — Firebase topic + log ADD_STAFF: 0 TC. Danh sách bot đưa vào các bước này nay là kết quả của `normalizeAcceptedBots` nên thuộc phạm vi hồi quy | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 16 quan điểm Trigger khớp task · 4 chưa cover đủ (PERM-002 / PERM-003 / SEC-001 có TC nhưng chưa chạy → đã tính ở G2).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q2 | `CONC-001` | Cao | GAP — MAP-PLAN-04 / 05: **2 người cùng bấm 「承認する」 khi LINE OA đang 9 staff** và **double click 「承認する」** — 0 TC. Đây đúng là ngưỡng của bug gốc (staff phải giữ 10) và nhánh `rollbackStaffIfOverLimit` chưa được TC nào gọi tới. NEW-18/NEW-43 chỉ cover BR-003 (1 lời mời, 2 người), là 2 bản trùng và đều skip | `[BLOCKER]` |
| Q3 | `PERM-004` (→ Cao: staff truy cập được PII friend) | Cao | GAP — không TC nào verify **quyền thật sự có hiệu lực** sau khi chấp nhận: B đăng nhập, chọn LINE OA X và chỉ thao tác được chức năng của vai trò trong lời mời. TC hiện có dừng ở màn 「スタッフ管理」 của A (RULE-06). Càng cần sau v1 vì vai trò nay bị ép theo lời mời (NEW-51) | `[BLOCKER]` |
| Q4 | `PAY-LIMIT-001` / `FUNC-004` | Cao | RISK — MAP-PLAN-06: thiếu case gói **không** bị giới hạn (theo Studio `dev_impact`, limit chỉ áp `plan_type=1` + standard + `flag_contract_new=1`) — LINE OA đã 10 staff nhưng không thuộc diện giới hạn vẫn phải chấp nhận được. Mọi TC giới hạn hiện có đều skip (G1) | `[MAJOR]` |
| Q5 | `SYNC-APP-001` (→ Cao: luồng critical user-facing) | Cao | GAP — BR-011 đăng ký Firebase topic sau khi accept → app mobile admin của staff mới nhận thông báo của LINE OA: 0 TC (xem G8) | `[BLOCKER]` |

Đã loại khỏi phạm vi (có lý do):
- `STATE-001` — fix chỉ thêm `return` sớm **trước** mọi bước ghi; trạng thái nửa vời duy nhất thấy được (nhánh limit bật `is_confirmed=1` rồi mới chặn — note của NEW-6) là hành vi có từ #39230 → đưa §6 #6, không đề xuất TC.
- `REG-SHARED-001` — 2 hàm dùng chung EP-07 / EP-11 chỉ còn 1 consumer là luồng invite staff (luồng đổi owner bị loại theo chốt của Leader), đã tính ở G4 / G5. Số `Q1` bỏ trống.
- `DEPLOY-LIVE-001` / `COMPAT-LEGACY-001` (lời mời staff phát hành trước deploy) — `generateLinkInviteStaff` không sửa, `bot_role` vẫn là `[{bot_id, role_id, user_id_root}]` ([logic-spec.md:117](../../spec-features/admin/staff-management/web/logic-spec.md)) → dữ liệu cũ và mới cùng hình dạng.
- `FUNC-DATE-001` — logic hết hạn 24h không sửa; fix chỉ cần giữ thứ tự thông báo (hết hạn trước chốt chặn) — NEW-19 cover, chỉ cần chạy lại (I2).

---

## 3. TC trùng lặp nội dung

Đã rà 57 TC — 15 TC đề nghị xóa / gộp.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-8 | NEW-33 (xóa) | `DUP-EXACT` | Trùng nguyên văn tiêu đề + tiền đề + expected (không gửi tham số `bots`) | `[MINOR]` |
| DUP-2 | NEW-9 | NEW-34 (xóa) | `DUP-EXACT` | Trùng nguyên văn (`bots` = mảng rỗng) | `[MINOR]` |
| DUP-3 | NEW-10 | NEW-35 (xóa) | `DUP-EXACT` | Trùng nguyên văn (`bots` sai kiểu) | `[MINOR]` |
| DUP-4 | NEW-11 | NEW-36 (xóa) | `DUP-EXACT` | Trùng nguyên văn (phần tử không phải đối tượng) | `[MINOR]` |
| DUP-5 | NEW-15 | NEW-40 (xóa) | `DUP-EXACT` | Trùng nguyên văn (mã mời không tồn tại + `bots` rỗng) | `[MINOR]` |
| DUP-6 | NEW-16 | NEW-41 (xóa) | `DUP-EXACT` | Trùng nguyên văn (lời mời đã dùng + `bots` rỗng) | `[MINOR]` |
| DUP-7 | NEW-17 | NEW-42 (xóa) · NEW-62 (gộp) | `DUP-EXACT` / `DUP-SUBSET` | FUNC-SEQ-001 · Abnormal · lỗi nghiệp vụ rồi chấp nhận lại cùng link · expected "lần 2 thành công, link chưa bị vô hiệu". NEW-62 là bản mơ hồ hơn của NEW-17 | `[MINOR]` |
| DUP-8 | NEW-18 | NEW-43 (xóa) | `DUP-INFLATE` | CONC-001 · Abnormal · BR-003 người khác đã nhận cùng lời mời — trùng nguyên văn, khiến CONC-001 trông như có 2 TC trong khi chỉ có 1 kịch bản và kịch bản đó skip → đã mở lại ở Q2 | `[MAJOR]` |
| DUP-9 | NEW-19 | NEW-44 (xóa) | `DUP-EXACT` | Trùng nguyên văn (quá 24h + `bots` rỗng) | `[MINOR]` |
| DUP-10 | NEW-20 | NEW-45 (xóa) | `DUP-INFLATE` | OUT-TRUTH-001 · Boundary · lời mời 2 LINE OA, 1 cái đã đủ 10 — trùng nguyên văn, làm G1 trông có 4 TC giới hạn thay vì 3 | `[MAJOR]` |
| DUP-11 | NEW-56 | NEW-14 (xóa) · NEW-61 (gộp) | `DUP-EXACT` / `DUP-SUBSET` | PERM/SEC · Abnormal · client gửi thêm LINE OA ngoài lời mời · expected "chỉ ghi LINE OA trong lời mời". NEW-56 có expected đo được; NEW-14 / NEW-61 chỉ ghi chung chung "không tạo quyền cho dữ liệu giả mạo". Phần "vai trò giả mạo" của NEW-61 đã có ở NEW-51 | `[MINOR]` |
| DUP-12 | NEW-8 / NEW-9 | NEW-49 (gộp) | `DUP-SUBSET` | DATA-DB-001 · lỗi nghiệp vụ không tạo dữ liệu staff — NEW-8 / NEW-9 đã kiểm dữ liệu staff + lời mời không đổi. NEW-49 manual/local, expected mơ hồ | `[MINOR]` |
| DUP-13 | NEW-3 | NEW-48 (gộp) | `DUP-SUBSET` | Mở link mời có `bot_role` hỏng → trang chủ không lỗi, modal không hiện. NEW-3 có expected đo được (HTTP 200 + `bots:[]`) | `[MINOR]` |

- **Gate đã chạy**: xóa 15 TC trên, coverage §1 / §2 giữ nguyên. NEW-48 là TC duy nhất **pass** của vùng G4-UI (local) → đề xuất **gộp** vào NEW-3 (chạy lại NEW-3), không xóa trước khi NEW-3 có kết quả.
- `DUP-INFLATE` → mở lại coverage: DUP-8 → Q2 · DUP-10 → G1.
- `DUP-CONFLICT`: không có.
- Xóa thật do human thực hiện trên Studio (`testcase_delete`).

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-13 | TC **fail** trên staging (#1713, xác minh 2 lần). Studio bug #1109 `open` nhưng **chưa có Redmine id**. Actual: phần tử có `user_invite_id = ""` → HTTP 200 `{"success":true}`, lời mời bị bật `is_confirmed=1`, **nhưng dòng staff 招待中 vẫn ở trạng thái chờ, không có staff nào được thêm**. Tức là **báo thành công giả + đốt link mời** (OUT-TRUTH-001 / UI-003 false success). Đây là lỗi do chính commit v1 (run cũ trên local pass) | Raise ticket Redmine từ bug #1109, gửi Dev; không đóng #39231 khi chưa xử lý. Hành vi đúng cần Dev chốt ở §6 #1. Sau khi fix phải chạy lại cả G2 (NEW-51 → 55) vì cùng cơ chế ghi đè khoá từ lời mời |
| I2 | `[MAJOR]` | Toàn bộ bộ TC | Kết quả thực thi: 29/57 pass (51%) · 1 fail · 26 skip · 1 chưa chạy. 26 TC skip vì staging **thiếu tài khoản エルメ thứ 2** (9 TC), **không được ghi DB** để làm hỏng `bot_role` / lùi `created_at` (13 TC), không dựng được LINE OA 9–10 staff (4 TC). 8 TC chưa chạy lần nào ở bất kỳ môi trường nào: NEW-51 · 52 · 53 · 54 · 55 · 58 · 59 | Bổ sung tài khoản B + LINE OA 9 staff vào test-resources của staging (hoặc chạy trên local có DB), rồi chạy lại toàn bộ TC skip trên commit `4e658d206e` |
| I3 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine bằng `/new-task` nhưng checkbox "Tester verify auto-fill chính xác" chưa tick | Tester đọc lại journal #137185 và tick checkbox |
| I4 | `[MAJOR]` | 28 TC: `TOOL-ERRHYG-001` (7) · `TOOL-KNOW-002` (6) · `API-CONTRACT-001` (4) · `SEC-INJECT-001` (3) · `TOOL-PAIRWISE-001` (3) · `TOOL-NEGCTRL-001` (2) · `TOOL-VAL2-001` (2) · `API-001` (1) | Mã quan điểm không có trong `checklist-lme.md` → không tính là cover ở §2. Toàn bộ nhánh "dữ liệu dị dạng → lỗi nghiệp vụ" (NEW-8 → 12, NEW-24/25/29/30) chỉ mang mã lạ | Map lại sang mã chuẩn trên Studio: nhánh input dị dạng → `FUNC-003` · client gửi dữ liệu giả mạo → `PERM-002` / `SEC-001` · giữ nguyên thông báo cũ → `OUT-TRUTH-001` |
| I5 | `[MAJOR]` | NEW-47 · NEW-57 · NEW-27 · NEW-31 | Expected **không đo được**: "không 500 + ghi lại hành vi thật để đối chiếu". NEW-47 và NEW-57 đang `pass` nhưng pass này không chứng minh được hành vi đúng | Dev chốt hành vi (§6 #2, #3) rồi sửa expected trên Studio. NEW-27 / NEW-31: Studio `dev_impact` đã ghi `is_array` → danh sách rỗng, sửa expected thành giá trị cụ thể |
| I6 | `[MAJOR]` | NEW-7 · NEW-14 · NEW-61 · NEW-49 · NEW-48 | Expected chung chung ("xử lý theo `bot_role`", "không tạo quyền cho dữ liệu giả mạo", "trang vẫn thao tác bình thường") — không chỉ ra giá trị cần kiểm | NEW-7: ghi rõ dòng staff của B trên LINE OA X ở trạng thái chấp nhận, vai trò = vai trò của lời mời. Các TC còn lại: xóa/gộp theo §3 |
| I8 | `[MINOR]` | NEW-4 | Chưa kiểm phần "không xoá session luồng mời" của fix (G7) | Thêm bước: sau khi đóng hộp thoại lỗi, tải lại trang chủ → modal 「アカウント権限の承認」 hiện lại; sửa lại dữ liệu lời mời cho hợp lệ → bấm 「承認する」 thành công |
| I9 | `[MINOR]` | 22 TC gắn `REQ-002` · `REQ-003` · `REQ-006` · `REQ-007` | Các requirement này không còn `active` trên Studio (task chỉ còn REQ-001 · 004 · 005 · 008 · 009) → trace TC ↔ requirement bị đứt | Kích hoạt lại hoặc gắn TC sang requirement đang active |

---

## 5. TCs đề xuất bổ sung (5)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | kho-tcs chưa có FA-035 — không đối chiếu được |
| Vùng regression phát hiện từ kho | Không có (kho trống) — vùng regression lấy từ `03-dev-impact.md` mục 3 / 4.3 + Studio `dev_impact` |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Xác nhận chống trùng | Đã đối chiếu 57 TC ở BƯỚC 0 — **không TC đề xuất nào trùng**. G1 · G2 · G4 · G5 không đề xuất TC mới (TC đã đủ ý, chỉ thiếu chạy → I2); G3 → §6 #3; G7 → bổ sung bước vào NEW-4 (I8) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC001-01 | UI | CONC-001 | Chấp nhận lời mời staff — modal 「アカウント権限の承認」 | Abnormal | auto | Tất cả | 2 người cùng bấm 「承認する」 khi LINE OA Standard hợp đồng mới đang có 9 staff — chỉ 1 người được thêm, số staff dừng ở 10 | LINE OA X gói Standard hợp đồng mới do A sở hữu, đang đúng 9 staff đã chấp nhận. A phát hành 2 link mời còn hạn: link 1 cho B, link 2 cho C. B và C đăng nhập ở 2 trình duyệt riêng, đã mở link của mình và đang thấy modal | 1. B và C bấm 「承認する」 gần như cùng lúc (chênh < 1 giây).<br>2. Đọc hộp thoại / kết quả ở cả 2 trình duyệt.<br>3. A mở màn 「スタッフ管理」 của X, đếm số staff | 9 staff + 2 lời mời | Đúng 1 trong 2 người thành công; người còn lại nhận thông báo 「こちらのLINE公式アカウントではスタッフ数が上限（10人まで）に達しています。」. Màn 「スタッフ管理」 của X hiển thị đúng 10 staff (không tính 「主管理者」), không bao giờ 11. Không có HTTP 500 | | Lấp Q2 · MAP-PLAN-04 · kiểm nhánh `rollbackStaffIfOverLimit` · Đánh giá spec: Spec ghi rõ (expected ticket #39231: "số staff giữ nguyên 10") · Evidence: screenshot 2 trình duyệt + màn 「スタッフ管理」 |
| TC-CONC001-02 | UI | CONC-001 | Chấp nhận lời mời staff — modal 「アカウント権限の承認」 | Boundary | auto | Tất cả | Double click 「承認する」 ở lời mời cuối cùng trước ngưỡng — chỉ tạo 1 staff, không báo lỗi giả | LINE OA X gói Standard hợp đồng mới đang 9 staff; A phát hành link mời cho B; B đã mở link, modal đang hiện | 1. B double click nhanh 「承認する」.<br>2. Quan sát hộp thoại và tab Network.<br>3. A mở màn 「スタッフ管理」 của X | 9 staff | B được thêm đúng 1 lần (X có 10 staff, B xuất hiện 1 dòng). Không hiện thông báo lỗi giới hạn hay URL vô hiệu cho B dù request thứ 2 bị từ chối. Không HTTP 500 | | Lấp Q2 · MAP-PLAN-05 · Đánh giá spec: Spec không ghi (hành vi request thứ 2 cần Leader chốt nếu khác) · Evidence: HAR + screenshot |
| TC-PAYLIMIT001-01 | UI | PAY-LIMIT-001 | Chấp nhận lời mời staff — giới hạn 10 staff theo gói | Normal | auto | Tất cả | LINE OA không thuộc diện giới hạn (Standard hợp đồng cũ / Pro) đã có 10 staff — người thứ 11 vẫn chấp nhận được | LINE OA X đang có 10 staff, thuộc gói **không** phải Standard hợp đồng mới (VD Standard `flag_contract_new=0`). A phát hành link mời cho B | 1. B mở link, bấm 「承認する」.<br>2. A mở màn 「スタッフ管理」 của X | 10 staff, gói ngoài diện giới hạn | Không hiện thông báo giới hạn; X có 11 staff, trong đó có B với đúng vai trò của lời mời | | Lấp Q4 · MAP-PLAN-06 · Đánh giá spec: Spec không ghi (điều kiện giới hạn lấy từ Studio `dev_impact`; BR-006 chưa cập nhật — §6 #5) · Evidence: screenshot màn 「契約情報」 (gói) + 「スタッフ管理」 |
| TC-PERM004-01 | UI | PERM-004 | Chấp nhận lời mời staff → quyền thao tác trên LINE OA | Normal | auto | Tất cả | Sau khi chấp nhận lời mời vai trò 「サポート」, staff chỉ thao tác được chức năng cấp cho 「サポート」 | A phát hành link mời B vào LINE OA X với vai trò 「サポート」. Ở màn 「操作権限を変更する」 của X, 「サポート」 **không** được cấp 1 chức năng cụ thể (VD 一斉配信), 「運用者」 có | 1. B mở link, bấm 「承認する」.<br>2. B chọn LINE OA X làm LINE OA đang thao tác.<br>3. B mở menu trái, tìm chức năng không được cấp; truy cập thẳng URL của chức năng đó.<br>4. B mở 1 chức năng được cấp | Vai trò lời mời: 「サポート」 | Bước 2: B chọn được X. Bước 3: chức năng không được cấp không hiện ở menu, truy cập thẳng URL bị chặn/chuyển về trang chủ. Bước 4: chức năng được cấp mở bình thường. Màn 「スタッフ管理」 của A hiển thị B với 「操作権限」 = 「サポート」 | | Lấp Q3 · RULE-06 output cuối · bổ trợ NEW-51 (vai trò bị ép theo lời mời) · Đánh giá spec: Spec ghi rõ (BR-009, SCR-EMP-03) · Evidence: screenshot menu + URL bị chặn |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | Chấp nhận lời mời staff → app mobile admin (Firebase topic) | Normal | manual | Tất cả | Sau khi chấp nhận lời mời, app mobile admin của staff mới nhận thông báo của LINE OA được mời | B đã đăng nhập app mobile admin LME trên điện thoại thật (có Firebase token), chưa là staff của X. A phát hành link mời B vào X | 1. B chấp nhận lời mời trên web.<br>2. Friend nhắn 1 tin vào LINE OA X.<br>3. Quan sát điện thoại của B | 1 tin nhắn text từ friend | Điện thoại của B nhận push notification của tin nhắn mới trên LINE OA X; mở app thấy X trong danh sách LINE OA | | Lấp G8 · Q5 · BR-011 · manual vì thiết bị thật (app mobile admin) · Đánh giá spec: Spec ghi rõ (BR-011) · Evidence: screen record điện thoại |

- G8 phần log `BotLifeCycle type=24` (BR-010): **không đề xuất TC** — `Input thiếu: spec-features chưa ghi màn nào hiển thị log BotLifeCycle`. Hỏi Dev màn/nơi xem log ADD_STAFF rồi bổ sung.

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update / cần chốt | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | FA-035 SCR-EMP-06 EP-19 | Phần tử `bots` có khoá định danh rỗng (`user_invite_id = ""`): theo TC NEW-13 phải trả lỗi 「承認できるLINE公式アカウントがありません…」; theo v1 server lấy lại khoá từ lời mời. **Thực tế đang ra cả 2 sai**: `success:true` + đốt link nhưng không thêm staff. Chốt 1 hành vi đúng | NEW-13 fail vs Studio `dev_impact` (v1) | Dev + Leader |
| 2 | FA-035 EP-19 / EP-07 | Lời mời có phần tử thiếu `role_id` → staff được lưu vai trò gì (có thể = 0, trùng 「主管理者」)? | NEW-47 (expected chưa chốt) | Dev |
| 3 | FA-035 EP-19 | `user_staff_id` (mã liên kết người được mời) có cần đối chiếu với lời mời + phiên đăng nhập như 4 khoá còn lại không? | NEW-57 note vs journal #137185 | Dev |
| 4 | FA-035 SCR-EMP-06 luồng accept | Cập nhật luồng EP-19: (a) `bots` không còn tin client — lọc theo `invite_staffs.bot_role`, vai trò / chủ sở hữu / người được mời lấy từ lời mời + phiên đăng nhập; (b) bước xoá session nay nằm **sau** chốt chặn; (c) thông báo mới 「承認できるLINE公式アカウントがありません。招待元にご確認をお願いします。」 | Spec hiện ghi "Body `{bots:[...]}` … Với mỗi bot: …", xoá session ở bước 2 | Dev |
| 5 | FA-035 BR-006 | BR-006 ghi "chưa xác nhận có áp dụng cho invite URL flow" + thông báo legacy 「スタンダードプランの上限に達しています…」. Thực tế (#39230/#39231) invite flow có áp giới hạn 10, thông báo 「こちらのLINE公式アカウントではスタッフ数が上限（10人まで）に達しています。」, điều kiện `plan_type=1` + standard + `flag_contract_new=1` | NEW-6 / NEW-20 vs spec BR-006 | Dev / PM |
| 6 | FA-035 BR-002 / BR-006 | Khi accept bị chặn vì đủ 10 staff, lời mời **vẫn bị bật `is_confirmed=1`** → link không dùng lại được dù chưa thêm staff (trạng thái nửa vời, STATE-001). Có đúng ý đồ không? | NEW-6 note | Leader / Dev |
