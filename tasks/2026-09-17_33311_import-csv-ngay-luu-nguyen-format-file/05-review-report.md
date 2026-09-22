# 05 — Review Report

> Draft cho Leader verify. Cập nhật 2026-09-18 theo 7 yêu cầu Leader chốt (bảng đầu §1).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #227 (ticket 33311, round 1) |
| Tổng số TC review | 21 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `9/17 vùng ảnh hưởng đủ TC · 10 dòng thiếu (2 GAP · 8 RISK)`

**Đối chiếu 8 yêu cầu Leader (2026-09-18)** — 8 định dạng hợp lệ: `yyyy-MM-dd` · `yyyy-M-d` · `yyyy-MM-d` · `yyyy-M-dd` · `yyyy/MM/dd` · `yyyy/M/d` · `yyyy/M/dd` · `yyyy/MM/d`. Câu "ngoài 4 format trên" hiểu là **ngoài 8 định dạng này**.

| # | Yêu cầu Leader | Trạng thái | TC hiện có | Cần làm |
|---|---|---|---|---|
| 1 | 8 định dạng → lưu `yyyy-MM-dd`, cho cả 生年月日 và friend info 年月日 | Chưa đủ | NEW-1 (生年月日), NEW-2 (年月日): mỗi TC mới 4/8 — thiếu `yyyy-MM-d`, `yyyy-M-dd`, `yyyy/M/dd`, `yyyy/MM/d` | Bổ sung 4 dòng vào NEW-1 và NEW-2 (G3) |
| 2 | Ngoài 8 định dạng → không lưu | Chưa đủ | NEW-18 — không nêu chạy cột nào, actual *"エラー"* chưa rõ nguồn | TC-FUNC003-01 (G4) |
| 3 | Ngày không tồn tại `2025-02-29` / `2025-13-01` / `2025-00-10` → không lưu | Gần đủ | 年月日: NEW-7 đủ 3 ngày (mã lạ) · 生年月日: NEW-8 thiếu `2025-00-10` | Bổ sung `2025-00-10` vào NEW-8, đổi mã NEW-7 (G2) |
| 4 | Action của 生年月日 và 年月日 chạy đúng, cả chế độ 「月日」 và 「年月日」 | Thiếu 3/4 ô | NEW-4: chỉ 年月日, không nêu chế độ | TC-FUNC001-01 (「年月日」), TC-FRIEND001-01 (「月日」) (G5) |
| 5 | E2E: import → lưu DB → chạy action → lịch sử ở 友だち詳細 | Chưa có | — (NEW-5 chỉ kiểm lịch sử trong DB) | TC-FUNC001-01 (G8) |
| 6 | Giá trị không đổi → không insert trùng `event_step_time` | Chưa có | — (NEW-20 import lặp nhưng không bật action, không kiểm lịch gửi) | TC-STATEDEP001-02, TC-COMPATLEGACY001-01 (G6) |
| 7 | Xoá info → xoá `event_step_time` | Chưa đủ | NEW-10 có ý xoá lịch cho 年月日, nhưng tiền đề không đảm bảo đang có lịch; 生年月日 không kiểm lịch | Bổ sung NEW-10 (G7) |
| 8 | Ngày có khoảng trắng đầu/cuối → job tự trim rồi lưu `yyyy-MM-dd` (Leader bổ sung 2026-09-18) | Chưa có | — | TC-FUNC003-02 (G4) |

`Input thiếu: không có diff` — Studio `spec_delta.diffAvailable = false` (không tìm thấy ref `origin/staging-t07-2026`). Chiều (b) chỉ suy được từ `dev_impact` của Studio + mục 1/2/3 của file 03.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `D3` `csv_filter_upload_history.message_error` · `T2` · Expect ticket (2) "**Báo lỗi** không cho import vào" | `dev-impact` | NEW-14, NEW-7, NEW-9, NEW-11 | **RISK** — spec FA-014: `message_error` **không có nơi nào hiển thị** (§3.3, §9 B-03; job-spec §8.2), Dev chỉ sửa job Java. Kết quả chạy tay NEW-14: *"không báo error -> expect: không tạo bản ghi trong bảng friend_information_value"*, vẫn ghi Đạt ⇒ người dùng **không thấy lỗi**. Chờ chốt §6 #1 rồi sửa NEW-14 (I1) | `[BLOCKER]` |
| G2 | `BUG` (2) — ngày không tồn tại · triệu chứng KH *"Import success và chat 11 hiển thị Invalid date"* | `dev-impact` | NEW-7, NEW-8, NEW-3, NEW-9, NEW-14 | **RISK** — 生年月日 (NEW-8) thiếu `2025-00-10`; với 年月日, `2025-00-10` chỉ có ở NEW-7 (mã lạ). Không TC nào mở Chat 1:1 của bạn có dòng bị loại. Bổ sung `2025-00-10` vào NEW-8; bổ sung vào NEW-14 bước mở Chat 1:1 bạn bị loại → trống / giữ giá trị cũ, không `Invalid date` | `[MAJOR]` |
| G3 | `T1` — 8 định dạng × 2 loại info | `dev-impact` | NEW-1, NEW-2 | **RISK** — mỗi TC 4/8 định dạng. Bổ sung 4 dòng định dạng lẫn (`yyyy-MM-d`, `yyyy-M-dd`, `yyyy/M/dd`, `yyyy/MM/d`) vào **cả** NEW-1 và NEW-2; dùng tháng hoặc ngày < 10 để thấy rõ khác biệt (vd `2026-03-9`, `2026-3-09`, `2026/3/09`, `2026/03/9`) | `[MAJOR]` |
| G4 | `T1` / `T2` — ngoài 8 định dạng → không lưu; khoảng trắng đầu/cuối → trim rồi lưu — cả 2 loại info | `dev-impact` | NEW-18 | **RISK** — NEW-18 không nêu cột; actual *"đang báo text エラー"* ≠ expected và mâu thuẫn NEW-14 (I9). Chưa TC nào có khoảng trắng; mục 2 file 03 của Dev **không nhắc bước trim**. → TC-FUNC003-01, TC-FUNC003-02 | `[MAJOR]` |
| G5 | `T4` — action theo ngày: {生年月日, 年月日} × {「月日」, 「年月日」} | `dev-impact` | NEW-4 | **GAP** — action của **生年月日: 0 TC** (nhánh 生年月日 của job nay đi qua hàm chuẩn hoá mới); NEW-4 không nêu chế độ. → TC-FUNC001-01, TC-FRIEND001-01 | `[BLOCKER]` |
| G6 | `T4` — giá trị không đổi → không insert trùng `event_step_time` | `dev-impact` | — | **GAP** — value nay được chuẩn hoá trước khi so với giá trị đang lưu; chưa TC nào import lại cùng ngày (cùng hoặc khác định dạng) rồi đếm lịch gửi. → TC-STATEDEP001-02 (dữ liệu mới), TC-COMPATLEGACY001-01 (bản ghi cũ) | `[BLOCKER]` |
| G7 | `T5` — cột ngày trống → xoá value **và** `event_step_time` | `dev-impact` | NEW-10 | **RISK** — tiền đề NEW-10 không đảm bảo 2 trường đang có lịch gửi; expected không kiểm lịch của 生年月日. Bổ sung NEW-10: 2 trường đều cài action + đang có lịch → sau import cả 2 lịch bị xoá, không nhận tin tới mốc | `[MAJOR]` |
| G8 | `T4` — `friend_info_history` + hiển thị lịch sử ở 友だち詳細 (E2E) | `dev-impact` | NEW-5 (mã lạ `DATA-HIST-001`) | **RISK** — NEW-5 chỉ kiểm DB, chỉ nhánh tạo mới của 年月日; chưa có nhánh cập nhật, chưa có 生年月日, chưa có luồng E2E. → TC-FUNC001-01 | `[MAJOR]` |
| G9 | Dòng có ngày sai bị **bỏ qua cả dòng** (Studio `dev_impact`: *"row có ngày null … bị skip"*) — hành vi siết lại | `diff code` | NEW-7, NEW-8, NEW-9 | **RISK** — 3 TC chỉ kiểm ô ngày; chưa kiểm tag / friend info khác của cùng dòng không được ghi, action tag không chạy. → TC-DATA001-01 | `[MAJOR]` |
| G10 | Dữ liệu import **trước fix** (đang lưu `yyyy/MM/dd` hoặc ngày không tồn tại) | `diff code` | NEW-16 (mã lạ, chỉ kiểm "không bị migrate"), NEW-20 (dữ liệu mới) | **RISK** — chưa TC nào import lên bản ghi cũ. → TC-COMPATLEGACY001-01, TC-COMPATLEGACY001-02 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `17 quan điểm Trigger khớp task · 13 chưa cover đủ`

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `OUT-TRUTH-001` · `UI-003` | Cao · Trung bình → Cao (rủi ro false success) | **RISK** — preview không kiểm ngày (FA-014 BR-13) → 「インポートされました。」 → job loại dòng → lịch sử vẫn 「完了済」 (B-02). Người dùng thấy import thành công dù dữ liệu bị loại; NEW-14 có kết quả thực tế ngược expected. Chung gốc G1 — chờ §6 #1 | `[BLOCKER]` |
| Q2 | `FRIEND-001` | Cao | **RISK** — 8 định dạng mới phủ 4/8 mỗi loại info; action của 生年月日 0 TC; chế độ 「月日」 0 TC. → bổ sung NEW-1/NEW-2 + TC-FUNC001-01, TC-FRIEND001-01 | `[BLOCKER]` |
| Q3 | `STATE-DEP-001` | Cao | **RISK** — NEW-4 chỉ có Normal. Thiếu: import ngày sai cho bạn đang có lịch (Abnormal), import lại cùng giá trị không sinh trùng lịch (Boundary), xoá info xoá lịch (NEW-10 chưa đủ). → TC-STATEDEP001-01, TC-STATEDEP001-02, bổ sung NEW-10 | `[BLOCKER]` |
| Q4 | `FUNC-001` | Cao | **RISK** — NEW-13, NEW-1 dừng ở DB / lịch sử import; chưa có luồng tới output cuối (tin LINE, lịch sử 友だち詳細 — RULE-06). → TC-FUNC001-01 | `[MAJOR]` |
| Q5 | `DATA-AUDIT-001` | Cao | **RISK** — chỉ NEW-5 (mã lạ), 1 trường / 1 thao tác. Hạ từ `[BLOCKER]` vì NEW-5 đã Đạt, chỉ cần đổi mã + bổ sung. → TC-FUNC001-01 (cả 2 loại info, tạo mới + cập nhật, xem ở 友だち詳細) | `[MAJOR]` |
| Q6 | `COMPAT-LEGACY-001` | Cao | **RISK** — chỉ NEW-20 (Normal, dữ liệu mới); thiếu bản ghi tạo trước fix (RULE-09). → TC-COMPATLEGACY001-01, -02 | `[MAJOR]` |
| Q7 | `DATA-MIG-001` | Cao | **GAP** — chỉ NEW-16 (mã lạ), NEW-16 pass hiển nhiên vì fix không có migration. Hạ xuống `[MAJOR]`: dữ liệu cũ hỏng **từ trước fix** → Leader tách ticket recovery (RULE-04, I6). → TC-COMPATLEGACY001-02 phủ phần "sửa dữ liệu cũ" | `[MAJOR]` |
| Q8 | `FUNC-003` | Trung bình → Cao (field ngày) | **RISK** — mới có NEW-8 (Abnormal) và NEW-18 (chưa rõ cột). Chưa có 全角, chữ 年月日, số chữ số sai, kèm giờ (Abnormal) và khoảng trắng đầu/cuối được trim (Boundary). → TC-FUNC003-01, TC-FUNC003-02 | `[MAJOR]` |
| Q9 | `DATA-001` | Cao | **RISK** — NEW-15 (N), NEW-19 (B); thiếu Abnormal: dòng bị loại không để lại dữ liệu ở nơi hiển thị. → TC-DATA001-01 | `[MAJOR]` |
| Q10 | `ENV-003` | Cao | **RISK** — job nền, 21/21 TC chỉ khai và chỉ chạy `local` (RULE-08). Không TC mới: chạy lại TC chính ở staging + production (I2) | `[MAJOR]` |
| Q11 | `JOB-001` | Cao | **RISK** — gần nhất là NEW-9 / NEW-18 nhưng mang mã lạ `JOB-002`; chưa đối chiếu số dòng file = số dòng import + số dòng bị loại. Không TC mới: đổi mã NEW-9 + bổ sung bước đếm | `[MAJOR]` |
| Q12 | `FUNC-004` | Cao | **RISK** — giới hạn "`message_error` tối đa 50 row" chỉ test 60 dòng (NEW-11). Không TC mới: bổ sung 49 / 50 / 51 dòng vào NEW-11 | `[MAJOR]` |

**RULE-01 theo từng mã — không tính GAP** (loại case còn thiếu đã có TC mang mã khác cover): `FUNC-002` (B: NEW-10 · N/A: NEW-1, NEW-12) · `FUNC-DATE-001` (B: NEW-3 · A: NEW-8) · `DATA-DB-001` (N: NEW-17) · `REG-SHARED-001` (A: NEW-12 · N: NEW-6) → đổi mã (I7) + ghi lý do ở `Ghi chú` trên Studio.

**Đã loại khỏi phạm vi** (kịch bản không đi qua đoạn code đã sửa):
- `DATA-DB-001` kiểm `WHERE` trên 2 bot — fix không đổi điều kiện ghi/xoá.
- Các màn **đọc** ngày khác (My page app, export CSV, modal filter) — tầng đọc không bị sửa; Chat 1:1 (NEW-15) và 友だち詳細 (TC-FUNC001-01) đã đủ làm smoke.
- `REG-SHARED-001` cho lối **ghi** 年月日 khác (QR landing có import param, form, multi action) — không thuộc code sửa; nếu có cùng lỗi thì đã có từ trước → hỏi Dev, tách ticket.
- `PERF-LARGE-001` — cách đọc file không đổi.

---

## 3. TC trùng lặp nội dung

Đã rà **21 TC**, **không phát hiện trùng lặp** theo 4 yếu tố.

| Cặp gần giống | Lý do không tính trùng |
|---|---|
| NEW-9 ↔ NEW-14 | Cùng dữ liệu trộn đúng/sai, khác lối vào (tạo bản ghi trực tiếp ↔ upload trên màn) và khác đầu ra (DB ↔ lịch sử import) |
| NEW-7 ↔ NEW-9 | NEW-7 có `2025-00-10`, NEW-9 không; NEW-9 kiểm thêm dòng hợp lệ vẫn import |
| NEW-19 ↔ NEW-3 / NEW-15 | Phần DB của NEW-19 nằm trong NEW-3, nhưng NEW-19 thêm bước hiển thị Chat 1:1 — xem I14 |
| NEW-1 ↔ NEW-13 | Cùng 生年月日, nhưng NEW-13 end-to-end qua upload trên màn, NEW-1 phủ nhiều định dạng |

- **Gate đã chạy**: không đề nghị xóa TC nào. `DUP-INFLATE`: không có. `DUP-CONFLICT`: không có.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-14 | Kết quả thực tế **ngược expected** nhưng vẫn ghi Đạt, chưa raise ticket. Expected: *"Lịch sử import … hiển thị message_error"*; actual: *"không báo error -> expect: không tạo bản ghi trong bảng friend_information_value"* — tester tự đổi expected lúc chạy | Đổi NEW-14 về **Không đạt** tới khi Leader chốt §6 #1. Chốt "phải báo lỗi trên màn" → raise bug; chốt "chỉ loại dòng" → sửa expected qua `testcase_update` rồi chạy lại |
| I2 | `[MAJOR]` | 21/21 TC | **RULE-08 / ENV-003** — job nền nhưng `env_scope` của 21 TC chỉ `local`, 21/21 kết quả chạy ở `local`. Runner auto 2 lần đều **skip 16/16**: `SOURCE_BRANCH_MISSING` | Đổi `env_scope` sang `Tất cả`; chạy lại tối thiểu NEW-13, NEW-14, NEW-15, NEW-1, NEW-2, NEW-7, NEW-4 + các TC action mới ở **staging + production** bằng bot + bạn test nội bộ |
| I3 | `[MAJOR]` | 21/21 TC | **RULE-02** — `task_get_report`: 22/22 lượt chạy tay `evidence: []`, 18/22 lượt `actual = null` → kết quả tự khai | Đính kèm screenshot 「インポート履歴」 / Chat 1:1 + kết quả query DB trước/sau |
| I4 | `[MAJOR]` | Task #227 | **Không xác nhận được lần chạy 2026-09-17 dùng code fix**: Studio khai branch `release-t07-2026`, fix ở `m_202608_import-csv-date-format_33311` (commit `044f472f`); runner báo chưa có branch; `spec_delta` không diff được | Ghi commit đã deploy vào kết quả; cập nhật branch của task trên Studio |
| I5 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill (`2026-09-17 by /new-task`) nhưng **chưa tick "Tester verify auto-fill chính xác"** | Tester đọc lại Journal #132130 rồi tick |
| I6 | `[MAJOR]` | Dữ liệu đã lưu trước fix · NEW-16 | **RULE-04** — chưa có thống kê toàn hệ thống + quyết định recovery. 3 loại bản ghi sai: (a) 年月日 dạng `yyyy/MM/dd`, `yyyy/M/d`…; (b) ngày không tồn tại (`Invalid date`); (c) **生年月日 `xxxx-02-29` năm không nhuận đã bị nắn thành `xxxx-02-28`** — đúng định dạng nên query theo định dạng không ra. NEW-16 chỉ xác nhận "không migrate" | Dev query phạm vi (a)(b) theo bot; (c) đối chiếu file CSV gốc / log import. Leader quyết recovery ở ticket riêng |
| I7 | `[MAJOR]` | NEW-5, NEW-6, NEW-7, NEW-9, NEW-16, NEW-18 | **6 TC mang mã quan điểm không có trong `checklist-lme.md`** → không tính cover | Đổi mã trên Studio: NEW-5 → `DATA-AUDIT-001` · NEW-6 → `REG-SHARED-001` · NEW-7 → `FRIEND-001` · NEW-9 → `JOB-001` · NEW-16 → `DATA-MIG-001` · NEW-18 → `FUNC-003` |
| I8 | `[MAJOR]` | NEW-12 | Expected sai tầng: *"Row A bị reject với thông báo 「有効な: ユーザーID ではありません。」… Row B import bình thường"* — thông báo này của **preview Laravel**, preview **dừng cả file** (FA-014 BR-13); job chỉ bỏ dòng A. Actual *"đang báo text エラ"* ⇒ dòng B không thể import, vẫn Đạt. `spec_ids` ghi `BR-09` (spec-features: BR-09 là nút CSVダウンロード) | Tách expected theo lối vào: upload trên màn → preview báo lỗi, không file nào được enqueue; tạo bản ghi trực tiếp → job bỏ dòng A, import dòng B. Sửa nguồn thành BR-13 |
| I9 | `[MAJOR]` | NEW-18 | Actual *"đang báo text エラー"* ≠ expected (dòng bị loại). Spec FA-014: preview **không** kiểm ngày → cần evidence `エラー` đến từ đâu (hay file sai số cột → BR-14); mâu thuẫn NEW-14 (*"không báo error"*). Không nêu cột 生年月日 hay 年月日 | Đính kèm evidence + file CSV; Dev xác nhận nguồn `エラー`. Ghi rõ chạy cho cả 2 cột (hoặc gộp vào TC-FUNC003-01) |
| I10 | `[MAJOR]` | NEW-1 … NEW-12 | Bước **"Tạo csv_filter_upload_history (upload_status=1) trỏ file"** = ghi DB trực tiếp, bỏ qua preview + modal 「アクション稼働に関する確認」 + 「アップロード」. Tester tay không dựng lại được nếu không có quyền DB, kết quả có thể khác luồng KH (NEW-12) | Viết lại bằng thao tác màn: 「CSV管理」→「インポート」→「ファイル選択」→ modal →「アップロード」→ chờ 「完了済」. Chỉ giữ cách ghi DB trực tiếp cho runner auto |
| I11 | `[MAJOR]` | NEW-17 … NEW-21 | 5 TC bổ sung 2026-09-17 có bước quá gọn (*"Import file CSV"*, *"Kiểm tra kết quả DB"*); expected NEW-20 *"không tạo dữ liệu không nhất quán"* không đo được | Bổ sung bước thao tác màn. NEW-20 có thể gộp vào TC-STATEDEP001-02 (yêu cầu Leader #6) |
| I12 | `[MAJOR]` | [AP-3] `T4` (NEW-4, NEW-5) | Regression action + lịch sử chỉ chạy trên trạng thái sạch (bạn chưa có giá trị) | Đã đề xuất TC-FUNC001-01 (có bạn đang có giá trị), TC-STATEDEP001-01, TC-STATEDEP001-02 |
| I13 | `[MINOR]` | NEW-4 | Không nêu chế độ action của trường 年月日 (「月日」 hay 「年月日」) → không biết đang phủ ô nào của yêu cầu Leader #4 | Ghi rõ chế độ ở tiền đề |
| I14 | `[MINOR]` | NEW-21 | Lượt chạy 1 ghi *"chỉ support định dạng shift-JIS"* (UTF-8 hỏng) nhưng vẫn Đạt; lượt 2 *"support cả 2 định dạng"* | Ghi rõ khác biệt giữa 2 lượt (file, BOM, encoding) |
| I15 | `[NIT]` | NEW-19 | [AP-5] Phần DB đã có ở NEW-3; tầng hiển thị Chat 1:1 không bị sửa | Cân nhắc gộp bộ dữ liệu biên vào NEW-15 |
| I16 | `[NIT]` | NEW-13 | Chỉ kiểm 生年月日 trong DB, chưa nhìn trên màn | Thêm 1 bước: Chat 1:1 hiển thị đúng 生年月日 |

---

## 5. TCs đề xuất bổ sung (9)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` (nhóm "Ghi giá trị từ tính năng khác", "Action gán friend info", MT-16) · `kho-tcs/fa013-friendlist-友だちリスト.md` (Import/Export CSV đã tách khỏi kho FA-013). **kho-tcs chưa có FA-014 CSV管理** — không đối chiếu được phần import |
| Vùng regression phát hiện từ kho | `TC-FRI-221` / `TC-FRI-222` (import CSV cập nhật giá trị + 回答人数) · `TC-FRI-243` (import 年月日 → lịch gửi) |
| Conflict expected vs kho | Không. Yêu cầu Leader #5 (import chạy action) cùng chiều `TC-FRI-243` và khối r279-r281 của **MT-16** → MT-16 coi như đã chốt, cần cập nhật kho (§6 #6) |
| GAP dùng lại TC kho | Không — `TC-FRI-221/222/243` không có định dạng ngày / dòng bị loại / bản ghi cũ |
| Xác nhận chống trùng | Đã đối chiếu 21 TC ở BƯỚC 0 + 2 file kho — **không TC đề xuất nào trùng**. G2, G3, G7 xử lý bằng bổ sung dữ liệu/bước vào NEW-8, NEW-14, NEW-1, NEW-2, NEW-10 thay vì viết TC mới |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Import CSV — luồng end-to-end | Normal | manual | Tất cả | Import CSV ngày → lưu đúng → action 「年月日」 gửi tin đúng giờ → 友だち詳細 hiển thị lịch sử (生年月日 + friend info 年月日) | - Bot test nội bộ<br>- 生年月日 và trường friend info kiểu 年月日 `I1` đều cài action gửi tin text, chế độ 「年月日」, giờ gửi = thời điểm test + 30 phút<br>- `U1` (LINE thật) chưa có 生年月日 và `I1`<br>- `U2` (LINE thật) đang có 生年月日 và `I1` = một ngày khác hôm nay (nhập tay ở Chat 1:1) | 1. Chuẩn bị file CSV đúng cấu trúc import có cột 「生年月日」 và `友だち情報_<id I1>`, 1 dòng cho `U1`, 1 dòng cho `U2`<br>2. 「CSV管理」→ tab 「インポート」→ 「ファイル選択」 chọn file → modal 「アクション稼働に関する確認」 chọn 「友だち情報 登録時アクション」=「稼働させる」→ 「アップロード」<br>3. Chuyển tab / F5 tới khi 「インポート履歴」 là 「完了済」<br>4. Mở Chat 1:1 của `U1`, `U2`, xem 生年月日 và `I1`<br>5. Tới giờ gửi, mở LINE app `U1`, `U2`<br>6. Mở 友だち詳細 của `U1`, `U2`, xem lịch sử thay đổi thông tin | 生年月日 = hôm nay dạng `yyyy/M/d`, `I1` = hôm nay dạng `yyyy-M-dd` (vd `2026/9/18`, `2026-9-18`) — cho cả `U1` và `U2` | - Bước 4: 生年月日 và `I1` của 2 bạn hiển thị đúng ngày hôm nay, click ra ngoài date picker không báo sai format<br>- Bước 5: mỗi bạn nhận đúng 1 tin cho 生年月日 và 1 tin cho `I1`, đúng giờ gửi<br>- Bước 6: `U1` có lịch sử thêm mới, `U2` có lịch sử cập nhật (cũ → hôm nay) cho cả 2 trường |  | Lấp G5 · G8 · Q2 · Q4 · Q5 · Đánh giá spec: Đã hỏi leader (yêu cầu #4, #5 ngày 2026-09-18) · Evidence: screenshot Chat 1:1 + LINE app + lịch sử 友だち詳細 · RULE-06 · RULE-08: kết luận cuối ở product |
| TC-FRIEND001-01 | UI | FRIEND-001 | Import CSV — action theo ngày | Normal | manual | Tất cả | Action chế độ 「月日」 của 生年月日 và friend info 年月日 chạy đúng sau import (năm trong CSV khác năm hiện tại) | - Bot test nội bộ<br>- 生年月日 và `I1` cài action gửi tin text, chế độ 「月日」, giờ gửi = thời điểm test + 30 phút<br>- `U1` (LINE thật) chưa có 生年月日 và `I1` | 1. Chuẩn bị file CSV có cột 「生年月日」 và `友だち情報_<id I1>`, 1 dòng cho `U1`<br>2. Upload với 「友だち情報 登録時アクション」=「稼働させる」, chờ 「完了済」<br>3. Mở Chat 1:1 `U1`, xem 2 trường<br>4. Tới giờ gửi, mở LINE app `U1` | Cùng tháng-ngày với hôm nay, năm quá khứ: 生年月日 = `1990/9/18`, `I1` = `2020-09-18` | - 2 trường hiển thị 1990/09/18 và 2020/09/18<br>- Tới giờ gửi hôm nay, `U1` nhận đúng 1 tin cho mỗi trường |  | Lấp G5 · Q2 · Đánh giá spec: Đã hỏi leader (yêu cầu #4) · Evidence: screenshot Chat 1:1 + LINE app |
| TC-STATEDEP001-01 | UI | STATE-DEP-001 | Import CSV — action theo ngày | Abnormal | manual | Tất cả | Import ngày không tồn tại cho bạn đang có lịch gửi → giá trị và lịch gửi cũ giữ nguyên (生年月日 + 年月日) | - Bot test nội bộ<br>- 生年月日 và `I1` cài action gửi tin text, chế độ 「年月日」, giờ gửi = thời điểm test + 30 phút<br>- `U1` (LINE thật) đang có 生年月日 và `I1` = hôm nay (nhập tay ở Chat 1:1) → đã có lịch gửi | 1. Chuẩn bị file CSV có cột 「生年月日」 và `友だち情報_<id I1>`, 1 dòng cho `U1`<br>2. Upload với 「友だち情報 登録時アクション」=「稼働させる」, chờ 「完了済」<br>3. Mở Chat 1:1 `U1`, xem 2 trường<br>4. Tới giờ gửi, mở LINE app `U1` | 生年月日 = `2025-02-29`, `I1` = `2025-13-01` | - 2 trường vẫn là ngày hôm nay, không `Invalid date`<br>- Tới giờ gửi, `U1` nhận đúng 1 tin cho mỗi trường (lịch cũ không bị huỷ, không sinh thêm) |  | Lấp Q3 · Đánh giá spec: Đã hỏi leader (yêu cầu #3) · Evidence: screenshot Chat 1:1 + LINE app · regression — dẫn từ TC-FRI-243 |
| TC-STATEDEP001-02 | UI | STATE-DEP-001 | Import CSV — action theo ngày | Boundary | manual | Tất cả | Import lại CÙNG ngày (cùng hoặc khác định dạng) → không sinh trùng lịch gửi (生年月日 + 年月日) | - Bot test nội bộ<br>- 生年月日 và `I1` cài action gửi tin text, chế độ 「年月日」, giờ gửi = thời điểm test + 30 phút<br>- `U1` (LINE thật) đang có 生年月日 và `I1` = hôm nay → đã có đúng 1 lịch gửi mỗi trường | 1. Chuẩn bị 2 file CSV có cột 「生年月日」 và `友だち情報_<id I1>`, 1 dòng cho `U1`<br>2. Upload file 1 với 「友だち情報 登録時アクション」=「稼働させる」, chờ 「完了済」<br>3. Upload file 2 cùng lựa chọn, chờ 「完了済」<br>4. Kiểm tra lịch gửi của `U1` (bảng `event_step_time`)<br>5. Tới giờ gửi, mở LINE app `U1` | File 1: 2 cột = hôm nay dạng `yyyy-MM-dd` (vd `2026-09-18`)<br>File 2: 2 cột = hôm nay dạng `yyyy/M/d` (vd `2026/9/18`) | - Sau cả 2 lần import, mỗi trường vẫn đúng 1 lịch gửi<br>- Tới giờ gửi, `U1` nhận đúng 1 tin cho mỗi trường |  | Lấp G6 · Q3 · Đánh giá spec: Đã hỏi leader (yêu cầu #6) · Evidence: kết quả query lịch gửi trước/sau + LINE app · Có thể thay NEW-20 (I11) |
| TC-DATA001-01 | UI | DATA-001 | Import CSV — dòng có ngày sai | Abnormal | manual | Tất cả | Dòng CSV có ngày không tồn tại bị loại cả dòng: tag và friend info text không được ghi, action tag không chạy | - Bot test nội bộ<br>- Trường friend info kiểu 年月日 `I1` và kiểu text `I2`; tag `T1` có action gửi tin text khi gắn tag<br>- `U1`, `U2` (LINE thật) chưa có `I1`, `I2`, chưa gắn `T1` | 1. Chuẩn bị file CSV có cột `友だち情報_<id I1>`, `友だち情報_<id I2>`, `タグ_<id T1>`, mỗi bạn 1 dòng<br>2. Upload, ở modal chọn 「タグ追加時アクション」=「稼働させる」, chờ 「完了済」<br>3. Mở Chat 1:1 `U1`, `U2`, xem `I1`, `I2` và tag<br>4. Mở LINE app `U1`, `U2` | `U1`: `I1`=`2025-13-01`, `I2`=`Khách hàng VIP`, `T1`=`1`<br>`U2`: `I1`=`2026/3/9`, `I2`=`Khách hàng thường`, `T1`=`1` | - `U1`: `I1`, `I2` trống, không gắn `T1`; không nhận tin action tag<br>- `U2`: `I1` = 2026/03/09, `I2` = `Khách hàng thường`, đã gắn `T1`; nhận đúng 1 tin action tag |  | Lấp G9 · Q9 · Đánh giá spec: Spec không ghi — theo mục 2 file 03 "row không được import"; Leader chốt "bỏ cả dòng" hay "chỉ bỏ ô ngày" (§6 #3) · Evidence: screenshot Chat 1:1 + LINE app · regression — dẫn từ TC-FRI-221 |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Import CSV — dữ liệu cũ trước fix | Boundary | manual | Tất cả | Import lại cùng ngày lên bản ghi cũ đang lưu dạng `yyyy/MM/dd` → hiển thị đúng, không sinh trùng lịch gửi | - Bot test nội bộ; `I1` cài action gửi tin text, chế độ 「年月日」, giờ gửi = thời điểm test + 30 phút<br>- `U1` (LINE thật) có `I1` = hôm nay lưu dạng cũ `yyyy/MM/dd`, do import CSV **trước khi deploy fix** (môi trường chưa deploy branch fix, hoặc bạn test trên production đã import trước ngày release) → Chat 1:1 không hiển thị được ngày | 1. Chuẩn bị file CSV cột `友だち情報_<id I1>`, 1 dòng cho `U1`<br>2. Upload với 「友だち情報 登録時アクション」=「稼働させる」, chờ 「完了済」<br>3. Mở Chat 1:1 `U1`, mở date picker `I1` rồi click ra ngoài<br>4. Tới giờ gửi, mở LINE app `U1` | `I1` = hôm nay dạng `yyyy-MM-dd` (vd đang lưu `2026/09/18`, import `2026-09-18`) | - `I1` hiển thị đúng ngày hôm nay, click ra ngoài không báo sai format<br>- Tới giờ gửi, `U1` nhận đúng 1 tin (không nhận 2 lần) |  | Lấp G6 · G10 · Q6 · Đánh giá spec: Đã hỏi leader (yêu cầu #6) · Evidence: screenshot Chat 1:1 trước/sau + LINE app · RULE-09 |
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | Import CSV — dữ liệu cũ trước fix | Abnormal | manual | Tất cả | Bản ghi cũ đang hiện `Invalid date` (import trước fix) được sửa bằng import ngày hợp lệ | - Bot test nội bộ; trường 年月日 `I1`<br>- `U1` có `I1` = `2025-13-01` lưu từ import CSV **trước khi deploy fix** → Chat 1:1 đang hiện `Invalid date` | 1. Chuẩn bị file CSV cột `友だち情報_<id I1>`, 1 dòng cho `U1`<br>2. Upload với 「稼働させない」, chờ 「完了済」<br>3. Mở Chat 1:1 `U1`, mở date picker `I1` rồi click ra ngoài | `I1` = `2025/12/1` | - `I1` hiển thị 2025/12/01, không còn `Invalid date`, click ra ngoài không báo sai format |  | Lấp G10 · Q6 · Q7 · Đánh giá spec: Spec không ghi · Evidence: screenshot Chat 1:1 trước/sau · Đầu vào cho quyết định recovery (RULE-04, I6) |
| TC-FUNC003-01 | UI | FUNC-003 | Import CSV — định dạng ngày | Abnormal | manual | Tất cả | Ngày ngoài 8 định dạng cho phép → không lưu, cả 生年月日 và friend info 年月日 | - Bot test nội bộ; trường 年月日 `I1`<br>- 7 bạn `U1`…`U7` chưa có 生年月日 và `I1` | 1. Chuẩn bị file CSV có cột 「生年月日」 và `友だち情報_<id I1>`, mỗi bạn 1 dòng, cùng 1 giá trị ở cả 2 cột theo Dữ liệu nhập; lưu Shift-JIS<br>2. Upload với 「稼働させない」, chờ 「完了済」<br>3. Mở Chat 1:1 từng bạn, xem 生年月日 và `I1` | `U1`: `２０２６/０３/０９` (số 全角)<br>`U2`: `2026／03／09` (dấu ／ 全角)<br>`U3`: `2026年3月9日`<br>`U4`: `2026/ 03/09` (khoảng trắng ở giữa)<br>`U5`: `26/3/9` (năm 2 chữ số)<br>`U6`: `2026/003/09` (tháng 3 chữ số)<br>`U7`: `2026/03/09 10:00` (kèm giờ) | - Cả 7 bạn: 生年月日 và `I1` trống, không hiện `Invalid date` |  | Lấp G4 · Q8 · Đánh giá spec: Đã hỏi leader (yêu cầu #2) · Evidence: screenshot Chat 1:1 từng bạn · Khác NEW-18 (`.` / `dd/MM/yyyy` / 8 chữ số liền) · Khoảng trắng đầu/cuối tách sang TC-FUNC003-02 |
| TC-FUNC003-02 | UI | FUNC-003 | Import CSV — định dạng ngày | Boundary | manual | Tất cả | Ngày có khoảng trắng đầu/cuối → job tự trim rồi lưu `yyyy-MM-dd`, cả 生年月日 và friend info 年月日 | - Bot test nội bộ; trường 年月日 `I1`<br>- 3 bạn `U1`…`U3` chưa có 生年月日 và `I1` | 1. Chuẩn bị file CSV có cột 「生年月日」 và `友だち情報_<id I1>`, mỗi bạn 1 dòng, cùng 1 giá trị ở cả 2 cột theo Dữ liệu nhập (giữ nguyên khoảng trắng khi lưu file)<br>2. Upload với 「稼働させない」, chờ 「完了済」<br>3. Mở Chat 1:1 từng bạn, xem 生年月日 và `I1`, mở date picker rồi click ra ngoài | `U1`: ` 2026/3/9` (khoảng trắng đầu)<br>`U2`: `2026-03-09 ` (khoảng trắng cuối)<br>`U3`: `  2026/03/9  ` (2 khoảng trắng ở cả đầu và cuối) | - Cả 3 bạn: 生年月日 và `I1` hiển thị 2026/03/09, click ra ngoài date picker không báo sai format |  | Lấp G4 · Q8 · Đánh giá spec: Đã hỏi leader (trim khoảng trắng, 2026-09-18) · Evidence: screenshot Chat 1:1 từng bạn |

- **Nhóm đã ghi đè `GROUP_MAP`**: cả 9 TC là `UI` — bước đều là thao tác màn + LINE app; query lịch gửi ở TC-STATEDEP001-02 chỉ là bước kiểm bổ sung.
- **Bổ sung vào TC cũ thay vì viết mới**: NEW-1, NEW-2 (+4 định dạng lẫn — G3) · NEW-8 (+`2025-00-10` — G2) · NEW-14 (+`2025-00-10` + mở Chat 1:1 bạn bị loại — G2) · NEW-10 (tiền đề có lịch gửi cho cả 2 trường + kiểm lịch bị xoá — G7) · NEW-11 (+49/50/51 dòng — Q12) · NEW-9 (đổi mã + bước đếm dòng — Q11).
- **G1 / Q1**: không đề xuất TC cho tới khi chốt §6 #1 — sau đó sửa NEW-14.
- **Q10**: không TC mới — chạy lại ở staging/production (I2).

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/csv-management/feature-spec.md` §3.3 + §9 B-03 · `db/db-mapping.md` D-08 · `job/job-spec.md` §8.2 | Spec ghi `message_error` là "cột chết — 0 writer, 0 reader UI". Sau fix job **có ghi** (tối đa 50 row) nhưng vẫn **không hiển thị ở đâu**. Cần chốt Expect ticket *"Báo lỗi không cho import vào"* có bắt buộc báo trên 「インポート履歴」 không | Ticket #33311 Expect (2) vs mục 2 file 03 vs NEW-14 actual | Leader / PM + Dev |
| 2 | feature-spec §2.3 Bước A (lưu ý 4: 「※友だち情報タイプ「年月日」は指定フォーマット( YYYY/MM/DD )以外は正常にインポートされません」) · §2.3 Bước D | Ghi rule Leader đã chốt (2026-09-18): 生年月日 và 年月日 nhận **8 định dạng** (`yyyy-MM-dd`, `yyyy-M-d`, `yyyy-MM-d`, `yyyy-M-dd`, `yyyy/MM/dd`, `yyyy/M/d`, `yyyy/M/dd`, `yyyy/MM/d`), lưu `yyyy-MM-dd`; khoảng trắng đầu/cuối → job tự trim rồi lưu; ngoài 8 định dạng hoặc ngày không tồn tại → không lưu. Cân nhắc sửa câu lưu ý trên màn. ⚠️ Mục 2 file 03 của Dev chỉ nêu 4 pattern → Dev xác nhận code nhận đủ 4 định dạng lẫn | Leader 2026-09-18 vs mục 2 file 03 | Đã chốt — Dev cập nhật spec + xác nhận code |
| 3 | feature-spec §5 (BR-13 / BR-14) · §2.3 Bước D | Rule mới: job loại **cả dòng** khi cột ngày sai. Chốt "bỏ cả dòng" hay "chỉ bỏ ô ngày" | Studio `dev_impact` + mục 2 file 03 · TC-DATA001-01 | Leader |
| 4 | feature-spec §5 BR-24 · §2.3 Bước D | Ghi rule Leader đã chốt: giá trị không đổi → **không insert trùng `event_step_time`**, so theo ngày sau chuẩn hoá (kể cả bản ghi cũ dạng `yyyy/MM/dd`); xoá info (ô trống) → **xoá `event_step_time`** | Leader 2026-09-18 · TC-STATEDEP001-02, TC-COMPATLEGACY001-01, NEW-10 | Đã chốt — Dev cập nhật spec |
| 5 | feature-spec §2.3 Bước D | Leader chốt (2026-09-18): job **tự trim khoảng trắng đầu/cuối** trước khi lưu. Mục 2 file 03 của Dev **không nhắc bước trim** → Dev xác nhận code đã trim, nếu chưa thì phải bổ sung. Cần chốt thêm: **khoảng trắng 全角 (`　`, U+3000)** có được trim không — Java `String.trim()` không cắt ký tự này. Số / dấu ／ 全角 vẫn **không** chuyển → không lưu | TC-FUNC003-01, TC-FUNC003-02 | Dev (trim) · Leader (全角スペース) |
| 6 | `kho-tcs/fa015-…` MT-16 · `TC-FRI-243` | Leader yêu cầu import chạy action theo ngày (yêu cầu #4, #5) → chốt MT-16 theo khối r279-r281 (import cập nhật / thêm lịch gửi), cập nhật kho | Kho FA-015 r124 vs r279-r281 | Leader xác nhận → cập nhật kho |
