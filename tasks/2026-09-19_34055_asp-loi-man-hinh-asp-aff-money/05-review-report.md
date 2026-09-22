# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #252 (round 1, branch `ai_fixbug_34055`) — fetch 2026-09-19, gồm run staging #1717 đang chạy |
| Tổng số TC review | 5 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 2/8 vùng ảnh hưởng đủ TC (F2 `money_v2.js`, T1 ô chọn bot với số bot nhỏ) · 2 GAP · 4 RISK

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` + `F1 ajaxAffMoneyV2` — mở màn với tài khoản **> 200 bot** (bùng RAM, gộp danh sách qua nhiều khối chunk 200) | `dev-impact` + `diff code` | NEW-7, NEW-4 | `RISK` — cả 2 **skip** ở staging (tài khoản staging lớn nhất 85 bot / 40 bot đủ điều kiện), chỉ pass ở **local** (run #803). Root cause gắn với giới hạn RAM PHP của từng môi trường → chưa có bằng chứng nào trên môi trường khách gặp lỗi | `[BLOCKER]` |
| G2 | `F3 affBotDetailV2` — cùng file, **pattern y hệt, chưa sửa** (yokoten) | `dev-impact` + `diff code` | không có | `GAP` — 0 TC. Tài khoản nhiều bot mở màn chi tiết theo bot vẫn có thể bị lỗi y hệt bug này | `[BLOCKER]` |
| G3 | `T2` bảng số liệu thưởng + 3 chỉ số tổng khi chọn bot / 「全件表示」 / đổi tháng (REQ-004) | `dev-impact` | NEW-4 (bước 5 chỉ kiểm "không lỗi", chạy local) | `RISK` — không TC nào kiểm **số liệu** đổi theo bot/tháng, và kiểm ô chọn bot giữ nguyên sau khi đổi tháng | `[MAJOR]` |
| G4 | Hành vi đổi: thêm `orderBy('id')` → thứ tự option ô chọn bot | `diff code` | NEW-6 | `RISK` — mới pass local; run staging #1717 chưa có kết quả NEW-6 | `[MINOR]` |
| G5 | Bỏ 2 dòng `Log::info` theo từng bot (REQ-006) | `diff code` | không có | `GAP` — không có TC. Không đề xuất TC UI (xem §5) | `[NIT]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 5 quan điểm có Trigger khớp task · 5 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PERF-LARGE-001` | Trung bình → **nâng Cao** (chính là root cause của bug) | `GAP` — 0 TC gắn mã này. Nội dung NEW-7 (mã lạ `TOOL-KNOW-002`) + NEW-4 (`FUNC-004`) đúng quan điểm nhưng chỉ pass local; thiếu Abnormal (tài khoản cực nhiều bot → rủi ro N+1 timeout mà AI tự nêu) | `[BLOCKER]` |
| Q2 | `REG-SHARED-001` | Cao | `GAP` — fix bug có thể tồn tại ở chức năng tương tự (`affBotDetailV2`) nhưng 0 TC | `[BLOCKER]` |
| Q3 | `FUNC-004` | Cao | `RISK` — chỉ có Boundary 201 (NEW-4, staging skip). Thiếu đúng biên **200** (vừa đủ 1 khối) và **0** bot đủ điều kiện (RULE-01, 5 pattern) | `[MAJOR]` |
| Q4 | `PERM-001` | Cao | `RISK` — nội dung đã cover ở NEW-2 (BOT-H thuộc tài khoản quản lý khác không hiện, pass staging) nhưng gắn mã lạ `TOOL-NEGCTRL-001` → theo quy tắc chưa tính là cover. **Chỉ cần đổi mã trên Studio**, không cần TC mới | `[MAJOR]` |
| Q5 | `LIST-001` | Trung bình | `GAP` — màn có filter bot + tháng + phân trang, 0 TC kiểm filter giữ đúng (trùng G3) | `[MAJOR]` |

- `OUT-TRUTH-001` (NEW-1, NEW-6): Trigger là "thao tác lưu/gửi/đồng bộ có thông báo kết quả" → **không khớp** màn chỉ đọc này; không tính là quan điểm của task (xem I11).

---

## 3. TC trùng lặp nội dung

Đã rà 5 TC, không phát hiện trùng lặp.

- NEW-1 và NEW-2 cùng dựng BOT-A..BOT-D và cùng kiểm 4 bot hợp lệ còn hiện, nhưng khác `loại case` (Normal / Abnormal) và NEW-2 thêm oracle loại trừ → không trùng theo 4 yếu tố.
- NEW-7 và NEW-4 cùng kiểm nhiều khối chunk, nhưng khác mục đích: NEW-7 kiểm không OOM với ≥ 300 bot, NEW-4 kiểm biên đúng 201 + chọn bot ở khối cuối → giữ cả hai.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — kết quả thực thi | Chỉ 3/5 TC pass (60% < 80%). 2 TC skip (NEW-7, NEW-4) lại chính là 2 TC cover root cause. Run staging #1717 vẫn `running` | Chờ run #1717 xong; chạy NEW-7/NEW-4 ở môi trường dựng được ≥ 201 bot, hoặc thay bằng TC production (§5 TC-PERFLARGE001-01) |
| I2 | `[MAJOR]` | Nguồn — môi trường (RULE-08 / ENV) | Bug là tràn RAM / hiệu năng trên production. 0 TC chạy production; cả 5 TC gắn `local-only`, staging không có dữ liệu đủ lớn | Leader chốt verify production **chỉ đọc** bằng tài khoản ASP thật nhiều bot (§5). **Input thiếu**: ticket không ghi tài khoản / admin nào gặp lỗi → hỏi CS/Dev |
| I3 | `[MAJOR]` | Nguồn — bug Studio #815 + TC đã xóa | Run local #803 có 24 kết quả (1 fail) nhưng task hiện chỉ còn 5 TC → 19 TC đã bị xóa, gồm TC fail gốc của bug #815 (chưa đăng nhập mở `/v2/affiliate/aff-money` → HTTP 500). Bug #815 `open`, **chưa có Redmine**. REQ-004..010 mất cover theo | Raise Redmine riêng cho #815 (lỗi middleware đăng nhập ASP, ngoài phạm vi fix #34055). Xác nhận với người xóa (Studio `testcase_get_history`) việc xóa 19 TC là có chủ đích |
| I4 | `[MAJOR]` | NEW-1 | Expected ghi "không có lỗi JavaScript trên console" nhưng run #1717 vẫn ghi nhận lỗi JS `datepicker-ja ... 'regional'` (bug #816) mà vẫn chấm **pass** → kết quả mâu thuẫn expected. Bug #816 `stale`, chưa có Redmine | Chọn 1: sửa expected thành "không có lỗi JS mới, ngoài lỗi đã biết #816" + raise Redmine #816; hoặc chấm Không đạt. Sửa bằng `testcase_update` trên Studio |
| I5 | `[MAJOR]` | Nguồn — evidence (RULE-02) | Run staging #1717: `artifacts = []` cho mọi TC; chỉ NEW-6 có screenshot, và là ở run local | Đính kèm screenshot ô chọn bot + DevTools Network (status / thời gian của request ajax) cho mỗi TC |
| I6 | `[MAJOR]` | Nguồn — spec | Không có spec FA-027 / màn tiền thưởng ASP trong `spec-features/` → **Input thiếu: spec cho điều kiện lọc bot của ô chọn bot**. Điều kiện (bot đời cũ / pro / enterprise_pro / dùng thử còn hạn) chỉ lấy từ đọc code | Leader/Dev xác nhận điều kiện lọc bot là đúng nghiệp vụ, không phải chỉ "giữ nguyên như code cũ" |
| I7 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine (2026-09-19 by /new-task) nhưng ô "Tester verify auto-fill chính xác" chưa tick | Tester đọc lại Redmine rồi tick |
| I8 | `[MAJOR]` | Nguồn — branch | Studio test trên `ai_fixbug_34055` (gốc `release_step_20260805`); journal 2026-09-19 báo release `release_step_20260827`. Description trỏ PR 9507, AI báo PR này không có trên release | Dev xác nhận bản fix nào nằm trong `release_step_20260827` và staging đang deploy bản nào, trước khi coi run #1717 là hợp lệ |
| I9 | `[MAJOR]` | NEW-1, NEW-2 | Tiền điều kiện dựng bằng cờ DB (cờ hợp đồng mới, mốc hết hạn dùng thử, cờ xóa) → không dựng được bằng thao tác người dùng trên staging (run #1717: NEW-1 thiếu BOT-D dùng thử; NEW-2 phải đổi tài khoản vì tài khoản gán sẵn không vào được portal ASP) | Viết lại tiền điều kiện theo thứ nhìn thấy trên màn (bot plan プロ / エンタープライズプロ, bot đang 7日間トライアル, bot đã xóa ở màn LINE公式アカウント一覧); ghi rõ tài khoản staging dùng được |
| I10 | `[MINOR]` | NEW-6 | Expected "sắp theo bots.id tăng dần" — tester không thấy id trên UI | Ghi theo "thứ tự tạo bot" (bot tạo trước đứng trước), đối chiếu bằng danh sách bot của tài khoản quản lý |
| I11 | `[NIT]` | NEW-1, NEW-6, NEW-7, NEW-2 | Mã quan điểm lệch: `OUT-TRUTH-001` không khớp trigger; `TOOL-KNOW-002` / `TOOL-NEGCTRL-001` là mã nội bộ Studio | Đổi mã trên Studio: NEW-1 → `FUNC-004` (Normal), NEW-6 → `LIST-001`, NEW-7 → `PERF-LARGE-001`, NEW-2 → `PERM-001` |

---

## 5. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | kho-tcs chưa có FA-027 / màn tiền thưởng ASP → không đối chiếu được |
| Vùng regression phát hiện từ kho | Không có |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Xác nhận chống trùng | Đã đối chiếu 5 TC ở BƯỚC 0 — không TC đề xuất nào trùng (TC-FUNC004-01 = biên 200 ≠ NEW-4 biên 201; TC-PERFLARGE001-01 = production thật ≠ NEW-7 dữ liệu seed) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERFLARGE001-01 | UI | PERF-LARGE-001 | Portal ASP — màn tiền thưởng 「ASP管理 紹介者（成約情報）」 · ô chọn bot | Normal | manual | product | Production: tài khoản ASP có nhiều bot nhất mở được màn tiền thưởng và ô chọn bot hiện đủ bot | Bản fix #34055 đã release. Tài khoản cộng tác viên ASP thật gắn với tài khoản quản lý có **> 200** bot plan プロ / エンタープライズプロ (ưu tiên đúng tài khoản đã gặp lỗi). Ghi trước số bot plan プロ / エンタープライズプロ của tài khoản quản lý đó và tên bot tạo sau cùng | 1. Mở DevTools tab Network.<br>2. Đăng nhập portal cộng tác viên ASP.<br>3. Mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」, chờ tải xong.<br>4. Ghi status + thời gian của request tải dữ liệu.<br>5. Xổ ô chọn bot, đếm option (không tính 「全件表示」).<br>6. Tìm bot tạo sau cùng trong danh sách. | Tài khoản ASP thật > 200 bot (Input thiếu — CS/Dev cung cấp) | Request tải dữ liệu trả 200, màn không trắng, không 500, không timeout. Số option ≥ số bot plan プロ / エンタープライズプロ đã ghi; bot tạo sau cùng có trong danh sách. Chỉ thao tác xem, không sửa dữ liệu | | Lấp G1, Q1 · RULE-08 · manual vì môi trường production · Đánh giá spec: Spec không ghi · Evidence: screenshot ô chọn bot + screenshot Network (status, thời gian) |
| TC-PERFLARGE001-02 | UI | PERF-LARGE-001 | Portal ASP — màn tiền thưởng · ô chọn bot | Abnormal | auto | Tất cả | Tài khoản 1000 bot đủ điều kiện — màn tiền thưởng vẫn tải được, không timeout | Môi trường seed được bot + hợp đồng (local/dev — staging không tạo thêm bot được). Tài khoản quản lý có 1000 bot plan プロ, bot tạo sau cùng tên 「LAST-1000」 | 1. Đăng nhập portal cộng tác viên ASP.<br>2. Mở màn tiền thưởng, ghi status + thời gian của request tải dữ liệu.<br>3. Xổ ô chọn bot, đếm option.<br>4. Tìm 「LAST-1000」. | 1000 bot plan プロ | Request trả 200 trong thời gian cho phép (Leader chốt ngưỡng, vd ≤ 30s), không 500 / timeout / trắng màn. Có đúng 1000 option bot + 「全件表示」, có 「LAST-1000」 | | Lấp Q1 · kiểm rủi ro N+1 query hợp đồng AI tự nêu · Đánh giá spec: Spec không ghi · Evidence: screenshot Network + số option đếm được · Phạm vi ENV: chỉ chạy ở env seed được data |
| TC-FUNC004-01 | UI | FUNC-004 | Portal ASP — màn tiền thưởng · ô chọn bot | Boundary | auto | Tất cả | Tài khoản đúng 200 bot đủ điều kiện (vừa đủ 1 khối) — ô chọn bot hiện đủ 200 bot | Tài khoản quản lý có đúng 200 bot plan プロ; bot tạo đầu tiên tên 「FIRST-200」, bot tạo sau cùng tên 「LAST-200」 | 1. Đăng nhập portal cộng tác viên ASP.<br>2. Mở màn tiền thưởng, chờ tải xong.<br>3. Xổ ô chọn bot, đếm option.<br>4. Kiểm option đầu và cuối. | 200 bot plan プロ | Đúng 201 option: 「全件表示」 + 200 bot, không trùng lặp. Option bot đầu tiên 「FIRST-200」, option cuối 「LAST-200」. Màn không lỗi | | Lấp Q3 · nguồn giới hạn: chunk 200 trong code fix · biên+1 = NEW-4 (201) · biên−1 (199) không đề xuất vì cùng nhánh 1 khối như 200 · Đánh giá spec: Spec không ghi · Evidence: screenshot ô chọn bot |
| TC-FUNC004-02 | UI | FUNC-004 | Portal ASP — màn tiền thưởng · ô chọn bot | Abnormal | auto | staging | Tài khoản không có bot đủ điều kiện — ô chọn bot chỉ có 「全件表示」, màn không lỗi | Tài khoản quản lý chỉ có bot plan フリー đã hết dùng thử và bot đã xóa, không có bot プロ / エンタープライズプロ | 1. Đăng nhập portal cộng tác viên ASP.<br>2. Mở màn tiền thưởng, chờ tải xong.<br>3. Xổ ô chọn bot.<br>4. Đổi tháng sang tháng trước. | 0 bot đủ điều kiện | Ô chọn bot chỉ có 1 option 「全件表示」; bảng hiển thị trạng thái rỗng; không 500, không lỗi JS mới (ngoài #816); đổi tháng vẫn không lỗi | | Lấp Q3 · pattern 0 của FUNC-004 — chunk không trả khối nào, danh sách bot phải là mảng rỗng · Đánh giá spec: Spec không ghi · Evidence: screenshot ô chọn bot + console |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Portal ASP — màn chi tiết theo bot (hàm `affBotDetailV2`) | Normal | manual | product | Tài khoản ASP nhiều bot mở màn chi tiết theo bot — xác nhận rủi ro yokoten của affBotDetailV2 | Cùng tài khoản ASP thật > 200 bot như TC-PERFLARGE001-01. **Input thiếu**: đường vào màn chi tiết theo bot trên portal ASP — Dev xác nhận | 1. Đăng nhập portal cộng tác viên ASP, mở DevTools Network.<br>2. Mở màn chi tiết theo bot (theo đường Dev chỉ).<br>3. Ghi status + thời gian request.<br>4. Kiểm màn hiển thị đủ dữ liệu. | Tài khoản ASP thật > 200 bot | Màn tải được, không 500 / trắng màn / timeout. Nếu lỗi → raise ticket yokoten cho `affBotDetailV2` (chưa fix trong #34055) | | Lấp G2, Q2 · regression · manual vì môi trường production · chỉ 1 Normal: Abnormal/Boundary viết sau khi Dev quyết định có fix affBotDetailV2 hay không (RULE-01) · Đánh giá spec: Spec không ghi · Evidence: screenshot màn + Network |
| TC-LIST001-01 | UI | LIST-001 | Portal ASP — màn tiền thưởng · lọc theo bot / tháng | Normal | auto | staging | Chọn bot rồi đổi tháng — bảng số liệu và 3 chỉ số tổng lọc đúng, ô chọn bot giữ nguyên danh sách | Tài khoản ASP staging có ≥ 2 bot đủ điều kiện, trong đó có bot có thành quả trong tháng hiện tại và bot không có | 1. Mở màn tiền thưởng, ghi 3 chỉ số tổng + số dòng bảng ở 「全件表示」.<br>2. Chọn bot có thành quả → ghi lại bảng + 3 chỉ số.<br>3. Chọn bot không có thành quả.<br>4. Chọn lại 「全件表示」.<br>5. Đổi sang tháng trước rồi xổ ô chọn bot. | Tài khoản staging hiện có (40 bot đủ điều kiện) | Bước 2: bảng chỉ còn dòng của bot đó, 3 chỉ số = tổng của bot đó. Bước 3: bảng rỗng, chỉ số 0, không lỗi. Bước 4: về đúng số liệu bước 1. Bước 5: số liệu đổi theo tháng; ô chọn bot vẫn đủ số option, đúng thứ tự như bước 1 | | Lấp G3, Q5 · regression · Đánh giá spec: Spec không ghi · Evidence: screenshot bảng + chỉ số ở từng bước |
| TC-LIST001-02 | UI | LIST-001 | Portal ASP — màn tiền thưởng · phân trang | Boundary | auto | staging | Bảng thành quả > 10 dòng — phân trang 10 dòng/trang vẫn đúng sau fix | Tài khoản ASP staging có ≥ 11 dòng thành quả trong 1 tháng | 1. Mở màn tiền thưởng, chọn tháng có ≥ 11 dòng.<br>2. Kiểm trang 1.<br>3. Sang trang 2.<br>4. Chọn 1 bot rồi kiểm phân trang. | ≥ 11 dòng thành quả | Trang 1 có 10 dòng, trang 2 có phần còn lại, tổng khớp chỉ số; chọn bot thì phân trang tính lại theo bot, không lỗi | | Lấp G3 (REQ-008) · regression · Đánh giá spec: Spec không ghi · Evidence: screenshot từng trang |

- **G4** (thứ tự option): không đề xuất TC mới — chờ NEW-6 có kết quả ở run staging #1717.
- **G5** (bỏ `Log::info`): không đề xuất TC UI — tester không quan sát được log server. Dev xác nhận qua diff, hoặc đọc `laravel.log` staging sau khi mở màn nếu Leader yêu cầu.

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | FA-027 — màn tiền thưởng ASP (chưa có trong `spec-features/`) | Ghi rõ điều kiện bot được hiện ở ô chọn bot (bot đời cũ / プロ / エンタープライズプロ / đang dùng thử còn hạn; loại bot đã xóa, không hợp đồng, thuộc tài khoản khác) và thứ tự option = thứ tự tạo bot | Hành vi chỉ suy từ code (NEW-1, NEW-2, NEW-6); `orderBy('id')` mới thêm ở bản fix | Dev / Leader |
| 2 | FA-027 — màn tiền thưởng: expected về lỗi JS | NEW-1 yêu cầu "không lỗi JS" nhưng lỗi #816 có từ trước fix | I4 | Leader |
