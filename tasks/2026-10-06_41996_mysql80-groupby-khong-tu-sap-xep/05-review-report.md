# 05 — Review Report

> Draft cho Leader verify. Round 1 — review bộ TC Studio task #369 (ticket #41996).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #369 (round 1, `status = tc-ready`, branch `ai_small_41996`) |
| Tổng số TC review | 44 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 30/33 mục có TC (`BUG` + F1–F19 + T1–T15, trừ F9 / T10 đã loại vì booking manager cũ đã bỏ; 4.2 không có D*) — **CHƯA ĐỦ** |
| **(b) diff code** — suy từ diff thật (Studio `dev_impact` + `spec_delta`, `diffAvailable = true`) | 27/30 điểm có TC (18 file + 12 rủi ro hồi quy / hành vi đổi; không tính `BookingManagerController.php` vì booking manager cũ đã bỏ) — **CHƯA ĐỦ** |

**Kết luận**: 0 vùng đạt OK (44/44 TC chưa chạy — xem §5 I1) · 1 GAP · 2 RISK. Theo thiết kế, 18/18 file trong phạm vi đều có ≥ 1 TC đi qua.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — GROUP BY không còn tự sắp xếp **trên MySQL 8** | `dev-impact` + `diff code` (rủi ro: lỗi SQL lúc chạy, Dev mới kiểm bằng lint) | NEW-42, NEW-43 (`env_scope = local`); 25 TC khác cũng chỉ có `local` | **RISK** — Theo ghi chú của Studio, DB local là **MySQL 5.6** → NEW-42/43 sẽ BLOCKED, và mọi TC còn lại chỉ chứng minh "không hỏng thêm" (5.6 vẫn tự sắp xếp nên base cũng PASS). Hai TC kiểm trên MySQL 8 chỉ phủ trang thành viên tag, クロス分析, エラーリスト, EP-06 và QR tab poster. **Không có TC nào trên MySQL 8** cho file CSV mà khách tải về (job CSV管理 + export của 友だちリスト), dù đây là output khách nhìn thấy trực tiếp và là chỗ Studio cảnh báo "thứ tự dòng CSV". | `[BLOCKER]` |
| G2 | F15 / T12 `countScenario` — ghi `scenario.count_follow/stop/unfinish` | `dev-impact` + `diff code` (rủi ro: nhiều nơi gọi chung) | NEW-35, NEW-36 (xoá step), NEW-37 (lệnh recover) | **RISK** — 2 vấn đề. **(i) Câu 5**: Dev giữ hành vi 5.7, theo đó mỗi cột là số **dòng của nhóm bạn có ID nhỏ nhất**, không phải số bạn. Cả 3 TC chỉ kiểm "giống base", không có TC nào kiểm theo quy tắc nghiệp vụ "số bạn theo trạng thái" (spec + kho, §4 C1). Đây là số liệu khách thấy ở màn danh sách kịch bản. **(ii) Câu 3**: hàm được gọi ở ≥ 7 nơi nhưng chỉ có TC cho luồng xoá step và lệnh recover. Thiếu job `CreateOrUpdateScenarioStepMessage` (job nền), luồng huỷ hợp đồng `StepMessageSpec`, app `ScenarioMobileController`, xoá filter step. | `[MAJOR]` |
| G3 | Rủi ro hồi quy hiệu năng — ORDER BY trên bảng hàng chục triệu dòng có thể sinh thêm filesort trên 8.0 (Studio `dev_impact`: "chỉ đo được trên máy B") | `diff code` (rủi ro hồi quy) | không có (NEW-42 bước 4 chỉ ghi EXPLAIN của 1 câu, không có tiêu chí) | **GAP** — 0 TC đo plan và thời gian trước/sau fix cho `tag_line_user` (168M), `line_user` (62M), `bot_line_user` (50M), `friend_information_value` (51M), `collect_open_landings` (33M). Dev chưa chạy EXPLAIN (DB dev connection refused). | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 15 quan điểm có Trigger khớp task · 11 đã cover đủ về thiết kế · 4 dòng thiếu (gộp 12 mã).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` · `FUNC-004` · `DATA-COUNT-001` · `OUT-EXPORT-001` · `FRIEND-001` · `MSG-001` · `MSG-USER-001` | Cao (OUT-EXPORT-001 nâng Cao) | **RISK — RULE-01**: cả bộ 44 TC có **0 Abnormal** (37 Normal + 7 Boundary). FUNC-001 không có TC nào mang mã này. FUNC-004 chỉ có Boundary (NEW-7, NEW-14, NEW-36). DATA-COUNT-001 có Normal + Boundary. OUT-EXPORT-001, FRIEND-001, MSG-001, MSG-USER-001 chỉ có Normal. Chỉ NEW-2 ghi lý do không có Abnormal. Leader đã chốt (2026-10-06) **không bổ sung TC Abnormal** cho phân trang. Với Boundary của export, TC-OUTEXPORT001-01 kiểm trường hợp 0 bạn khớp. Các quan điểm còn lại: member ghi lý do "fix chỉ thêm ORDER BY, không có input mới" vào `Ghi chú`. | `[MAJOR]` |
| Q2 | `ENV-003` ★ · `JOB-001` ★ | Cao | **RISK — nội dung có nhưng mang mã lạ**, nên tính là chưa cover. ENV-003 (thêm DB server MySQL 8) chỉ có NEW-42/43 (`TOOL-KNOW-002`), và 2 TC này lại bị BLOCKED vì env (G1). JOB-001 (sửa job `handle:export_csv`, `countScenario` gọi từ job) chỉ có NEW-37 (`JOB-002`); NEW-10…14 mang mã khác. Đề nghị đổi `viewpoint` trên Studio: NEW-42/43 → `ENV-003`, NEW-37 → `JOB-001`, cùng các mã lạ khác: NEW-35 → `DATA-COUNT-001`, NEW-18 → `FRIEND-001`, NEW-30 → `FUNC-SEQ-001`, NEW-15/NEW-32 → `LIST-001`. Phần thiếu thật về env đã ở G1; phần thiếu về job đã ở G2. | `[MAJOR]` |
| Q3 | `PERF-LARGE-001` | TB → **Cao** (export + phân tích) | **GAP** — 0 TC (trùng G3). | `[BLOCKER]` |
| Q4 | `REG-SHARED-001` | Cao | **GAP** — Dev ghi "quét ngang: các bản Replicate chết + vị trí phía job/MCP ghi vào yokoten" nhưng **không có số ticket**. Báo cáo audit cũng ghi 22 vị trí bổ sung "chưa rà từng chỗ". Ngoài ra, `Conversation::advanceFilterPost` (không có orderBy) là hàm dùng chung. Chưa có danh sách xác nhận các luồng **chọn đối tượng để gửi tin / thao tác hàng loạt** (bulk action > 200 qua job ở kho FA-013 nhóm 6–10, gửi broadcast theo filter) có phân trang/chia lô bằng LIMIT/OFFSET trên kết quả GROUP BY hay không. Nếu có, MySQL 8 có thể **gửi trùng hoặc bỏ sót bạn**, nặng hơn nhiều so với lỗi hiển thị. Không đề xuất TC vì code chưa sửa: yêu cầu Dev xác nhận và link ticket yokoten trước khi đóng #41996. | `[MAJOR]` |

Quan điểm đã xét và loại (căn cứ ở scratchpad):
- `CONC-003`: FE không đổi, chỉ đổi query PHP.
- `BULK-001`: các thao tác hàng loạt ở 友だち情報管理 / 友だちリスト chọn theo ID, không theo vị trí dòng. Riêng việc chọn tập gửi đã chuyển sang Q4.
- `SEC-ISO-001`: điều kiện WHERE `bot_id` không đổi.
- `DATA-DB-001`: câu UPDATE `scenario` không nằm trong diff, chỉ giá trị đếm đổi; phần này đã ở G2.
- `DATA-MIG-001` / `DATA-BACKUP-001`: không đổi schema.
- `SYNC-APP-001`: chỉ API lịch bài học của app bị chạm, NEW-32 đã cover; màn web không nằm trong diff.
- `COMPAT-LEGACY-001`: nhánh filter cũ/v2 đã có NEW-4…NEW-9.
- `INTG-*` / `PERM-*` / `DEPLOY-LIVE-001`: không đổi đồng bộ ngoài, phân quyền hay payload. NEW-15/NEW-32 đã kiểm cấu trúc response.

---

## 3. TC trùng lặp nội dung

Đã rà 44 TC, không phát hiện trùng lặp. Các cặp dễ nhầm đã kiểm:
- NEW-10 ↔ NEW-15: file do daemon sinh / API trả dữ liệu, khác tầng.
- NEW-11/12 ↔ NEW-16: job / API của cùng hàm `getConversationBlocked`, khác nơi gọi.
- NEW-9 ↔ #23800: thứ tự + số dòng CSV / đối chiếu số đếm 4 nguồn.
- NEW-1/17/34 ↔ NEW-42: MySQL 5.x regression / MySQL 8 tái hiện.
- NEW-5/24 ↔ NEW-43: tương tự cặp trên.
- NEW-35 ↔ NEW-36: dữ liệu nhiều trạng thái / trạng thái rỗng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` + `CONF-KHO` | NEW-35, NEW-36, NEW-37 | Giá trị 3 cột đếm của kịch bản (購読中 / 途中で終了 / 読了済) sau khi gọi `countScenario` | NEW-35: 3 bạn đang theo dõi (L1 × 2 dòng, L2, L3) → `count_follow = 2`; `is_following = 2` → `count_stop`, `is_following = 0` → `count_unfinish` | Spec `scenario/feature-spec.md` §3 (cột 「購読中の友だち」 = "Số bạn đang theo dõi (N人)") + §6 (`0` = 読了済 → `count_stop`, `2` = 途中で終了 → `count_unfinish`) · Kho FA-009 `TC-SCE-312…317` (đếm theo số bạn, mỗi bạn ±1) · kho `MT-01` / `MT-37` đang **chờ quyết định** về ánh xạ 0/2 | (1) TC đúng theo code hiện tại (Dev xác nhận hàm "vốn đã sai nghĩa"), và spec/kho mô tả hành vi mong muốn mà code **chưa từng đạt** → cần ticket sửa riêng · (2) spec/kho sai, và cột đếm thật sự là số dòng nhóm đầu (khó tin vì cột này hiển thị cho khách) | `[MAJOR]` | Leader / PM (+ Dev mở ticket) |
| C2 | `CONF-SPEC` | NEW-3 | Thứ tự các tag ở nhóm 「未分類」 khi tìm theo từ khoá ở タグ管理 | Thứ tự tạo tag (`tags.id` tăng dần), "nếu màn có sắp xếp riêng thì đối chiếu với base" | Spec `tag-management/feature-spec.md` BR-15: tag sắp xếp theo `position` (kéo thả sắp xếp → position = index + 1). Kho `TC-TAG-28`: import CSV chèn ngược nên position ≠ thứ tự id | (1) TC đúng: kết quả tìm kiếm cố ý theo id như 5.7 · (2) spec đúng: kết quả tìm kiếm phải theo position như danh sách thường; hành vi 5.7 đã lệch sẵn và fix hiện tại giữ nguyên chỗ lệch | `[MINOR]` | Leader |

**Đã rà**: 44 TC × các spec sau:
- `spec-features/admin/scenario/feature-spec.md` (§3, §6), `tag-management/feature-spec.md` (BR-15)
- `event-booking`, `friend-information`, `friend-list`, `csv-management`, `qr-landing` (đọc theo các mục mà TC trích)

và các file kho `kho-tcs/fa009-*` (Bộ đếm friend, MT-01, MT-37), `fa012-*` (Màn list tag, Count, Sort), `fa013-*` (Sắp xếp & phân trang, bảng Coverage), `fa015-*` (Màn danh sách câu trả lời), `fa021-*` (Danh sách người tham gia `TC-EBK-313/314`).

Lưu ý:
- **Kho chưa có** FA-017 (QR/LP), FA-024 (クロス分析), FA-014 (CSV管理) và các màn quản trị hệ thống. Vì vậy NEW-10…18, NEW-24…28, NEW-38…41 không đối chiếu kho được.
- **Spec không có** cho クロス分析 và các màn quản trị hệ thống (§5 I6).
- Không có `CONF-TC`. NEW-30 khớp kho `TC-EBK-313`.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 44 TC | **0/44 TC đã chạy** (`exec.untested = 44`, `last_exec = null`). Tỷ lệ pass 0%, chưa có kết luận nào về bản fix. | Chạy bộ TC (sau khi xử lý G1–G3) trước khi đóng ticket. |
| I2 | `[MAJOR]` | 25/44 TC chỉ có `env_scope = local` (NEW-5…16, NEW-23…28, NEW-33…37, NEW-42, NEW-43) | **RULE-08 / ENV-003**: bug chỉ xảy ra trên MySQL 8, nhưng Studio ghi DB local là MySQL 5.6. Task có chạm job nền (`handle:export_csv`, job scenario) mà không TC nào có `prd`. | Xác nhận env nào đã lên MySQL 8 (`SELECT VERSION()`) và chạy TC §7 G1 ở đó. Ghi version DB vào evidence của mọi TC. |
| I3 | `[MAJOR]` | NEW-3, NEW-17, NEW-19, NEW-23, NEW-35, NEW-36, NEW-37, NEW-41 | Oracle "**giống base**" không ghi base chạy trên DB nào. Trên MySQL 8, base chính là bản lỗi: thứ tự và nhóm đầu không cố định giữa các lần chạy, nên so với base không kết luận được Đạt hay Không đạt. | Ghi rõ "base = `release_step_20260930_v2` chạy trên MySQL 5.7/5.6 (hành vi production hiện tại)", hoặc thay bằng giá trị cụ thể như NEW-35 đã làm (2/3/1). |
| I4 | `[MAJOR]` | NEW-5, NEW-6, NEW-7, NEW-15, NEW-16, NEW-32 | **RULE-13**: TC gọi thẳng endpoint nhưng `Kết quả mong đợi` không ghi mã HTTP (chỉ ghi `result = ok` / cấu trúc response). | Bổ sung "HTTP 200" cho mọi lần gọi, kể cả trang rỗng (`page=2` của NEW-7). |
| I5 | `[MAJOR]` | Toàn bộ 44 TC | Thứ tự mong đợi (ID tăng dần, giá trị theo collation, bản ghi URL tạo trước…) lấy từ "Hướng xử lý" của ticket, **spec không ghi** (NEW-1, NEW-3 tự nêu). Tuy vậy, `Trạng thái đánh giá spec` để trống, có nguy cơ tự suy rồi cho Đạt. | Leader chốt quy tắc thứ tự theo §8 #3 rồi ghi `Đã hỏi leader` trên Studio. |
| I6 | `[MAJOR]` | NEW-17…20 (クロス分析), NEW-38…41 (quản trị hệ thống) | `Input thiếu: spec cho クロス分析 (FA-024) và các màn quản trị hệ thống (ASP管理, bot free, chuyển khoản affiliate, 解約理由)`. `spec-features/` không có thư mục tương ứng, nên không có chuẩn để đánh giá Expected. | Bổ sung spec, hoặc Leader xác nhận expected của 8 TC này. |
| I7 | `[MAJOR]` | #23800 | (1) Ghi "tái dùng kho FL-116", nhưng `kho-tcs/fa013-*` hiện tại có `TC-FRL-116` là case bulk action last message, nên không tra ngược được. (2) Bước 4 "Gọi API danh sách bạn bè với cùng điều kiện lọc" không nêu endpoint/payload, người khác không chạy lại được. (3) Tag `TC38336_COUNT` mang số của ticket khác. | Sửa nguồn kho cho đúng. Ghi endpoint cụ thể (vd EP-06 `/basic/friendlist/advance-filter` hoặc API export của NEW-15). Đổi tên dữ liệu theo #41996. |
| I8 | `[MINOR]` | NEW-24 | Ghi chú yêu cầu "lặp lại bước 1-3 sau khi đổi chế độ đếm", nhưng thao tác này không nằm trong `Các bước thực hiện` → dễ bị bỏ qua khi chạy auto. | Đưa vào steps (bước 5–6) hoặc tách thành 1 TC riêng cho `type_count = 0`. |
| I9 | `[MINOR]` | NEW-4 / T2 | Dev kê T2 = "Broadcast (FA-008) — danh sách người nhận". Studio lại xác định `public/js/broadcast/filter.js` không được view nào nạp, nên endpoint chỉ còn dùng ở 自動応答 cũ và cài đặt tin nhắn kịch bản. Hai nguồn lệch nhau về phạm vi. | Dev xác nhận màn broadcast hiện tại có còn gọi `POST /filter/get-list-user` không. Nếu không, sửa 4.3 của file 03. |
| I10 | `[MINOR]` | 3 vị trí Dev bỏ qua | Dev bỏ qua `AffiliaterController::ajaxAffMoneyV2`, `ConversionController::visitedConversion` vì "đã có ORDER BY", và `HandleExportCsv2` vì "code chết". (`BookingManagerController:4480` không còn xét vì booking manager cũ đã bỏ.) | Dev dán đoạn code có orderBy của 2 vị trí và chứng minh `HandleExportCsv2` không có lệnh/route gọi. Không cần TC. |
| I11 | `[NIT]` | NEW-42 | 1 TC gộp 3 màn và thêm bước EXPLAIN. Khi fail sẽ không rõ màn nào hỏng. | Ghi kết quả riêng từng màn trong evidence. Phần EXPLAIN đã chuyển sang TC-PERFLARGE001-01. |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 44 TC, có 1 TC ngoài phạm vi task.

| TC | Lý do | Đề xuất | Severity |
|---|---|---|---|
| NEW-31 | Leader xác nhận (2026-10-06) booking manager cũ đã bỏ → F9 / T10 (`BookingManagerController::ajaxFilterBookingByCondition`) ngoài phạm vi test. NEW-31 là TC duy nhất của vùng này nên xoá không làm mất cover của impact nào còn trong phạm vi. | Xoá NEW-31 trên Studio (`testcase_delete`) | `[MINOR]` |

Các TC còn lại đều trong phạm vi:
- #23800 (đối chiếu số đếm 4 nguồn) là regression dẫn từ rủi ro hồi quy của Studio ("số đếm phải giữ nguyên").
- NEW-41 (解約理由): sau truy vấn còn `sortByDesc` nên ORDER BY mới chỉ ảnh hưởng các bản ghi trùng giá trị. TC vẫn là TC duy nhất của `UserController`, nên giữ.

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa009-phathanhtheobuoc-ステップ配信.md` (Bộ đếm friend, MT-01, MT-37) · `fa012-quanlythe-タグ管理.md` (nhóm 5, 9, 10, 12; `TC-TAG-28`, `TC-TAG-151`) · `fa013-friendlist-友だちリスト.md` (bảng Coverage, nhóm 2, 6) · `fa015-quanlythongtinbanbe-友だち情報管理.md` (Màn danh sách câu trả lời) · `fa021-eventbooking-イベント予約.md` (`TC-EBK-313/314`). **Kho chưa có FA-014 / FA-017 / FA-024**, nên không đối chiếu được. |
| Vùng regression phát hiện từ kho | `TC-TAG-28` (import CSV chèn ngược → position ≠ id) → R1 · `TC-SCE-312…317` (bộ đếm theo số bạn) → TC-DATACOUNT001-01 |
| Conflict expected vs kho | Không có TC đề xuất nào trái kho. Hai conflict của TC hiện có đã đưa vào §4 (C1, C2) + §8 |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | R1: spec tag BR-15 + kho `TC-TAG-28` |
| Xác nhận chống trùng | Đã đối chiếu 44 TC ở BƯỚC 0 + 5 file kho, **không TC đề xuất nào trùng**. TC-ENV003-01 khác NEW-10 ở DB MySQL 8 + đối chiếu base. TC-ENV003-02 khác NEW-8/9 ở DB MySQL 8. TC-DATACOUNT001-01 khác NEW-35 ở oracle theo quy tắc nghiệp vụ. |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENV003-01 | Job | ENV-003 | CSV管理 — tạo file tải về | Normal | auto | dev, local, prd, staging | Trên DB MySQL 8: file CSV do job 「handle:export_csv」 sinh ra theo đúng ID bạn bè tăng dần, 3 lần xuất giống hệt nhau (bản fix); ghi lại thứ tự ở bản trước fix | - Env đã chạy DB MySQL 8: `SELECT VERSION()` ra `8.0.x`, ghi lại cùng branch đang deploy<br>- Bot kiểm thử B có ≥ 40 bạn đang theo dõi<br>- Tag 「QA41996-CSV」 gắn qua màn 友だち詳細 cho 40 bạn, **theo thứ tự ngược** với ID trang 友だち詳細 (bạn có ID lớn gắn trước)<br>- Job 「handle:export_csv」 đang chạy | 1. Mở 「CSV管理」 → tạo file tải về.<br>2. Nhập 「書き出し名（管理用）」 = 「QA41996-CSV-1」, chọn 「有効友だち」, bấm 「絞込み」 → điều kiện tag 「QA41996-CSV」, chọn cột 「LINE登録名」 + 「友だちID」, bấm lưu.<br>3. Chờ tới khi xuất hiện 「CSVダウンロード」, tải file.<br>4. Lặp bước 1–3 thêm 2 lần với tên 「QA41996-CSV-2」, 「QA41996-CSV-3」.<br>5. So sánh thứ tự dòng của 3 file với danh sách ID bạn bè.<br>6. (Đối chứng) Trên cùng DB, deploy `release_step_20260930_v2`, lặp bước 1–3 một lần, ghi lại thứ tự. | 40 bạn gắn tag ngược thứ tự ID · 3 lần xuất | - Bản fix: 「対象人数」 = 40人 cả 3 lần<br>- Mỗi file đúng 40 dòng dữ liệu, không lặp, không thiếu<br>- Thứ tự dòng = ID bạn bè tăng dần, **giống hệt nhau ở cả 3 file**<br>- Bản trước fix (bước 6): ghi lại thứ tự thực tế. Nếu khác ID tăng dần → bằng chứng tái hiện lỗi. Nếu trùng → ghi "không tái hiện với dữ liệu này", không kết luận fix sai | | Lấp G1 · Q2 · env phải là MySQL 8, nếu còn 5.x thì ghi blocked, không kết luận · dữ liệu dựng qua UI nên chạy được trên prd (bot kiểm thử) sau khi prd lên MySQL 8 — RULE-08 job nền · Đánh giá spec: Spec không ghi (thứ tự theo ticket mục 3) · Evidence: `SELECT VERSION()` + 3 file CSV + file của bản trước fix |
| TC-ENV003-02 | UI | ENV-003 | 友だちリスト — export CSV | Normal | auto | dev, local, staging | Trên DB MySQL 8: export CSV từ 友だちリスト sau 絞込み cho cùng thứ tự ở 3 lần xuất (bản fix) | - Env DB MySQL 8 (`SELECT VERSION()` = `8.0.x`)<br>- Bot kiểm thử B: dùng lại tag 「QA41996-CSV」 (40 bạn, gắn ngược thứ tự) của TC-ENV003-01 | 1. Mở 「友だちリスト」, bấm 「絞込み」 → điều kiện tag 「QA41996-CSV」 → áp dụng, ghi 「検索結果：N人」.<br>2. Chọn xuất theo điều kiện, bấm export CSV, tải file.<br>3. Lặp bước 2 thêm 2 lần.<br>4. Không áp lọc, tick tay 5 bạn bất kỳ theo thứ tự ngẫu nhiên, export, lặp 2 lần. | 40 bạn khớp lọc · 5 bạn chọn tay | - 「検索結果」 = 40人; 3 file theo điều kiện có đúng 40 dòng, không lặp, **cùng một thứ tự** ở cả 3 lần<br>- 2 file chọn tay có đúng 5 dòng, cùng thứ tự ở 2 lần, không theo thứ tự tick<br>- Mọi lần export trả file, không thông báo lỗi | | Lấp G1 · không chạy prd vì phải dựng 40 bạn có tag · Đánh giá spec: Spec không ghi · Evidence: `SELECT VERSION()` + 5 file CSV |
| TC-DATACOUNT001-01 | UI | DATA-COUNT-001 | シナリオ — danh sách kịch bản | Normal | auto | dev, local, staging | Sau khi xoá 1 step, 3 cột 「購読中の友だち」 / 「途中で終了した友だち」 / 「読了済の友だち」 hiển thị đúng **số bạn** theo trạng thái | - Bot kiểm thử B, kịch bản 「QA41996-SC」 có 3 step S1/S2/S3<br>- Start kịch bản cho 5 bạn: 3 bạn còn đang nhận (còn lịch gửi S3); 1 bạn đã nhận hết; 1 bạn bị stop giữa chừng từ màn 友だち詳細<br>- 1 trong 3 bạn đang nhận được start lại thêm 1 lần (để có 2 bản ghi) | 1. Mở danh sách kịch bản, ghi 3 cột của 「QA41996-SC」.<br>2. Vào màn step, xoá step S1, xác nhận.<br>3. Quay lại danh sách kịch bản, ghi lại 3 cột.<br>4. Bấm 「表示」 ở từng cột, đếm số bạn trong danh sách. | 3 bạn đang nhận (1 bạn có 2 bản ghi) · 1 bạn đọc xong · 1 bạn dừng giữa chừng | - Sau bước 2: 購読中 = **3人** · 読了済 = **1人** · 途中で終了 = **1人**<br>- Mỗi cột bằng đúng số bạn ở danh sách 「表示」 (bước 4) | | Lấp G2 (câu 5) · **kỳ vọng FAIL ở cả base lẫn fix**: Dev xác nhận `countScenario` ghi số dòng của nhóm bạn ID nhỏ nhất. FAIL → raise ticket riêng, **không chặn #41996** · ánh xạ 読了済/途中で終了 ↔ trạng thái theo spec §6, chờ chốt §8 #1 (kho MT-01) · không chạy prd vì phải dựng trạng thái · Đánh giá spec: Spec ghi rõ (§3 「Số bạn đang theo dõi (N人)」) · Evidence: screenshot danh sách + 3 danh sách 表示 |
| TC-JOB001-01 | Job | JOB-001 | シナリオ — lưu step (job 「CreateOrUpdateScenarioStepMessage」) | Normal | auto | dev, local, prd, staging | Sửa nội dung 1 step của kịch bản đang chạy: job tạo/cập nhật step chạy xong, 3 cột đếm giữ nguyên như trước khi sửa | - Bot kiểm thử B, kịch bản 「QA41996-SCJ」 có 2 step, đang có 4 bạn đang nhận (còn lịch gửi step 2), không có bạn ở trạng thái khác<br>- Ghi lại 3 cột đếm ở danh sách kịch bản trước khi sửa | 1. Mở màn step của 「QA41996-SCJ」, sửa nội dung text của step 2, bấm lưu.<br>2. Chờ job xử lý xong (thông báo lưu xong / trạng thái step không còn đang xử lý).<br>3. Mở lại danh sách kịch bản, đọc 3 cột.<br>4. So với giá trị ở tiền điều kiện. | 4 bạn đang nhận · sửa text step 2 | - Lưu thành công, không lỗi job<br>- 3 cột đếm sau khi sửa **bằng đúng** giá trị trước khi sửa (sửa nội dung step không đổi trạng thái bạn nào)<br>- 4 bạn vẫn nhận step 2 đúng giờ | | Lấp G2 (câu 3 — nơi gọi job) · RULE-08 job nền → scope có prd, dữ liệu dựng qua UI trên bot kiểm thử · Dev xác nhận luồng lưu step có gọi `CreateOrUpdateScenarioStepMessage` → `countScenario` · Đánh giá spec: Spec không ghi · Evidence: screenshot trước/sau + log job |
| TC-PERFLARGE001-01 | Data | PERF-LARGE-001 | Thành viên tag · lọc nâng cao/export bạn bè · クロス分析 · QR tab poster | Normal | auto | dev, local, prd, staging | So sánh plan và thời gian truy vấn trước/sau khi thêm ORDER BY trên MySQL 8, cho 4 truy vấn trên bảng lớn | - Env DB MySQL 8 có dữ liệu quy mô thật (máy B theo ticket), chỉ đọc<br>- Chọn bot có nhiều bạn nhất, tag có nhiều thành viên nhất, trường friend info có nhiều giá trị nhất, trang đích QR có nhiều lượt quét nhất<br>- Lấy SQL thực tế (kèm tham số) của 4 màn ở `release_step_20260930_v2` và `ai_small_41996` | 1. Chạy `EXPLAIN` từng câu ở bản trước fix, ghi index / rows / Extra.<br>2. Chạy `EXPLAIN` từng câu ở bản sau fix, ghi lại.<br>3. Đo thời gian mỗi câu 5 lần (sau 1 lần làm nóng), ghi median.<br>4. Với câu export CSV của bot lớn nhất, đo thêm thời gian job sinh file trên UI. | 4 truy vấn: thành viên tag (`tag_line_user` 168M) · lọc nâng cao/export (`bot_line_user` 50M) · giá trị クロス分析 (`friend_information_value` 51M) · QR tab poster (`collect_open_landings` 33M) | - Sau fix: Extra **không xuất hiện thêm** `Using filesort` / `Using temporary` so với trước fix, **hoặc** có xuất hiện nhưng median tăng ≤ 20%<br>- Cùng index với trước fix<br>- Tập ID trả về trước và sau fix giống nhau (chỉ khác thứ tự) | | Lấp G3 · Q3 · ngưỡng 20% là đề xuất, Leader chỉnh nếu có SLA · chỉ đọc nên chạy được trên prd sau khi prd lên MySQL 8 · Đánh giá spec: Spec không ghi · Evidence: output EXPLAIN 2 bản + bảng 5 lần đo |
| TC-OUTEXPORT001-01 | Job | OUT-EXPORT-001 | CSV管理 — tạo file tải về | Boundary | auto | dev, local, prd, staging | CSV管理 với điều kiện không khớp bạn nào: job chạy xong, 対象人数 = 0人, file chỉ có dòng tiêu đề | - Bot kiểm thử B; tag 「QA41996-EMPTY」 mới tạo, chưa gắn cho ai<br>- Job 「handle:export_csv」 đang chạy | 1. Mở 「CSV管理」 → tạo file tải về, tên 「QA41996-EMPTY」, chọn 「有効友だち」, 絞込み tag 「QA41996-EMPTY」, chọn 2 cột, lưu.<br>2. Chờ trạng thái chuyển sang có nút 「CSVダウンロード」.<br>3. Tải file, mở. | Điều kiện khớp 0 bạn | - Bản ghi không kẹt ở trạng thái đang tạo (job xử lý xong)<br>- 「対象人数」 = 0人<br>- File tải được, có đúng 1 dòng tiêu đề, 0 dòng dữ liệu, không thông báo lỗi | | Lấp Q1 · biên rỗng của GROUP BY + ORDER BY trong job · RULE-08 job nền → scope có prd, dữ liệu dựng qua UI · Đánh giá spec: Spec không ghi · Evidence: screenshot trạng thái + file CSV |
| TC-LIST001-01 | UI | LIST-001 | タグ管理 — tìm kiếm tag | Boundary | auto | dev, local, prd, staging | Tìm tag theo từ khoá khi các tag ở 「未分類」 đã được kéo thả sắp xếp lại: ghi lại thứ tự kết quả so với thứ tự danh sách | - Bot kiểm thử B; trong 「未分類」 tạo lần lượt 3 tag 「QA41996KW_1」, 「QA41996KW_2」, 「QA41996KW_3」<br>- Dùng chức năng sắp xếp tag, kéo thả thành thứ tự 3 → 1 → 2 rồi lưu | 1. Mở 「タグ管理」, ở 「未分類」 ghi thứ tự 3 tag (không tìm kiếm).<br>2. Nhập từ khoá 「QA41996KW_」, thực hiện tìm.<br>3. Ghi thứ tự 3 tag ở nhóm 「未分類」 trong kết quả.<br>4. Tìm lại 2 lần, so sánh. | Thứ tự tạo 1, 2, 3 · thứ tự sau kéo thả 3, 1, 2 | - Bước 1: 3 → 1 → 2 (theo position, BR-15)<br>- Bước 3: **chờ Leader chốt §8 #2**. Theo spec BR-15 là 3 → 1 → 2; theo bản fix (`tags.id`) là 1 → 2 → 3<br>- 3 lần tìm cho cùng một thứ tự, số người từng tag đúng | | Lấp R1 · regression · căn cứ: spec tag BR-15 + kho `TC-TAG-28` (position ≠ id trong dùng thực tế) · Đánh giá spec: Spec ghi rõ (BR-15) — mâu thuẫn §4 C2 · Evidence: screenshot bước 1 + 3 lần tìm |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `scenario/feature-spec.md` §3 + §6 · `scenario/web/logic-spec.md` BR-10 · kho FA-009 `MT-01` / `MT-37` | (a) Chốt 3 cột đếm = **số bạn** theo trạng thái (spec + kho) hay số dòng nhóm đầu (code `countScenario` hiện tại). Nếu là số bạn → Dev mở ticket sửa `countScenario`, sau đó sửa expected NEW-35/36/37. (b) Chốt ánh xạ `is_following` 0/2 ↔ `count_stop` / `count_unfinish` (spec §6 trái với NEW-35 và corpus 03/2025) | §4 C1 · §1 G2 | Leader / PM + Dev |
| 2 | `tag-management/feature-spec.md` BR-15 | Kết quả tìm tag theo từ khoá ở 「未分類」 sắp theo `position` (như danh sách) hay theo `tags.id` (như 5.7 / bản fix) | §4 C2 · §7 R1 | Leader |
| 3 | `friend-list` EP-06 + export · `tag-management` (trang thành viên) · `friend-filter` (get-list-user) · `friend-information` SCR-FI-04 · `qr-landing` (データ詳細 3 tab) · `event-booking` (参加者 gom theo ngày) · `csv-management` | Ghi quy tắc thứ tự mặc định + khoá phụ khi người dùng đã chọn sắp xếp (bản fix: theo cột GROUP BY tăng dần, đặt sau sắp xếp của người dùng). Với danh sách giá trị chữ, ghi rõ **collation** (MySQL 8 mặc định `utf8mb4_0900_ai_ci` khác `utf8mb4_general_ci` của 5.7, có thể đổi thứ tự kana/Latinh dù đã có ORDER BY) | Bản fix #41996 (spec chưa ghi — §5 I5) | Dev / Leader |
| 4 | Spec URL Analytics / エラーリスト | Khi cùng URL có 2 bản ghi trong bot, hiển thị bản ghi tạo trước (theo 5.7, NEW-34) hay cộng gộp click | NEW-34 ghi "có hợp lý nghiệp vụ hay không là câu hỏi cho leader" | Leader |
| 5 | Thiếu spec FA-024 クロス分析 + màn quản trị hệ thống (ASP管理 / bot free / chuyển khoản affiliate / 解約理由) | Bổ sung spec, ít nhất Business rules về thứ tự và số đếm | §5 I6 | Leader |
