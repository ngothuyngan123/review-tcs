# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder `tasks/<YYYY-MM-DD>_<ticket>_<slug>/`;
> vòng review nằm ở tên file (`05-review-report.md` = round 1, `.round2.md` = round 2).
>
> ⚠️ **Report chỉ ghi phần THIẾU + việc phải làm.** Bảng coverage 2 chiều và bảng quan điểm đối chiếu
> vẫn **bắt buộc chạy** ở BƯỚC 2 / 3 nhưng là **phân tích nội bộ — KHÔNG ghi vào file này**:
> chỉ những dòng `GAP` / `RISK` mới xuất hiện ở §1 / §2. Cái gì đã đủ TC thì **không viết dòng nào**.
> Đã bỏ khỏi report: Verdict · Tóm tắt cho member · Coverage matrix đầy đủ · Fix-shape table · Bảng quan điểm đầy đủ · Checklist · Ký duyệt.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #<id> / (2) Sheet <url> gid=<gid> rows <a>-<b> / (3) 04-tc-list.md` |
| Tổng số TC review | `<n>` |

<!-- Đúng 2 dòng, không thêm dòng khác. Cảnh báo chất lượng nguồn (pass rate / môi trường đã chạy /
     tác giả TC / evidence rỗng) KHÔNG ghi ở đây — flag nào thật sự là vấn đề thì đưa xuống §4. -->

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `<x>/<y> vùng ảnh hưởng đủ TC · <a> GAP · <b> RISK` — hoặc `Đủ coverage, không GAP`.

> Chỉ liệt kê phần **THIẾU**. Vùng nào đã đủ TC → **không ghi dòng nào**.
> **2 chiều bắt buộc rà** (BƯỚC 2):
> **(a) dev-impact** — `BUG` root cause + `F*` / `D*` / `T*` ở `03-dev-impact.md` mục 4 (thứ Dev **tự kê**).
> **(b) diff code** — ảnh hưởng suy từ **diff thật**, lấy ở **tab Thông tin của MCP LME TEST STUDIO**: `task_get_context(task_id, sections=["dev_impact","spec_delta"])` → `dev_impact` (điểm sửa · rủi ro hồi quy · hành vi đổi so với trước) + `spec_delta.files[]` / `diffStat`. Studio không có diff → fallback mục 1 + 2 + 3 của `03-dev-impact.md`. Chiều này bắt cái mà **dev-impact không kê ra**.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `F2 — <function>` | `dev-impact` | `không có` | `GAP — 0 TC cover` | `[BLOCKER]` |
| G2 | `<file / hàm nằm trong diff>` | `diff code` | `<TC No.>` | `RISK — fix là generic catch nhưng TC chỉ trigger 1 điều kiện` | `[MAJOR]` |
| G3 | `<TC No.>` | `orphan` | — | `TC không thuộc BUG / F* / D* / T* / quan điểm nào` | `[MINOR]` |

- `Chiều`: `dev-impact` · `diff code` · `orphan`.
- `Thiếu gì`: `GAP` = 0 TC cover · `RISK` = có TC nhưng thiếu loại case / chưa chạy (`skip` / `Chưa test`) / expected dừng trước output cuối (RULE-06) / chỉ verify UI không verify DB (RULE-07).
- Không đọc được diff (Studio `diffAvailable = false` **và** file 03 không mô tả điểm sửa) → ghi 1 dòng:
  `Input thiếu: không có diff — chiều (b) chỉ suy được từ mô tả cách fix`.
- Mỗi dòng ở đây **phải** có TC tương ứng ở §5, hoặc 1 câu giải thích vì sao không đề xuất TC.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `<n> quan điểm Trigger khớp task · <m> chưa cover đủ` — hoặc `Không thiếu quan điểm nào`.

> Chỉ liệt kê quan điểm **Trigger khớp task mà TC chưa cover đủ**. Quan điểm đã đủ → **không ghi**.
> Chọn quan điểm bằng [checklist-lme.index.md](../../framework/checklist-lme.index.md) + [catalog-lme.index.md](../../framework/catalog-lme.index.md), KHÔNG nạp toàn văn.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `<MSG-004>` | `Cao` | `GAP — 0 TC cover` | `[BLOCKER]` |
| Q2 | `<PERM-002>` | `Cao` | `RISK — có Normal, thiếu Abnormal + Boundary (RULE-01)` | `[MAJOR]` |

- Ưu tiên **Cao** + `GAP` → `[BLOCKER]` · **Trung bình** + `GAP` → `[MAJOR]`.
- Cột `Ưu tiên` của index ghi `Trung bình (→ Cao khi ...)` / `Trung bình → BẮT BUỘC (nâng Cao)` — **khớp điều kiện thì xử lý như Cao**.
- Quan điểm chỉ được cover bởi TC mang **mã lạ** (mã nội bộ Studio `TOOL-*`, không có trong `checklist-lme.md`) → tính là **chưa cover**.
- **KHÔNG** dùng §4 "Quan điểm chưa đủ bằng chứng" của checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) để flag BLOCKER/MAJOR — **RULE-11**, chỉ được nêu ở mức `[NIT]` (ghi xuống §4).

---

## 3. TC trùng lặp nội dung

> BƯỚC 4b. So theo **ý định test** (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương), KHÔNG so chuỗi.
> **Bắt buộc fill kể cả khi không có trùng** — ghi "Đã rà `<n>` TC, không phát hiện trùng lặp".

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `<TC No.>` | `<TC No.>` | `DUP-EXACT / DUP-SUBSET / DUP-INFLATE / DUP-CONFLICT` | | `[MINOR]` / `[MAJOR]` |

- **Gate đã chạy**: giả định xóa các TC trên → coverage §1 + quan điểm §2 còn nguyên? `Có / Không → đổi sang GỘP: <TC No.>`
- `DUP-INFLATE` → impact/quan điểm bị che GAP: `<liệt kê, đã thêm dòng tương ứng vào §1 / §2>`
- `DUP-CONFLICT` → **không xóa**, đã đưa vào §6 để Dev/Leader chốt: `<liệt kê>`
- Xóa thật do human thực hiện: nguồn Studio → `testcase_delete`; nguồn Sheet / file 04 → member tự xóa.

---

## 4. Issues khác

> Chỉ ghi issue **không phải GAP coverage** (GAP đã nằm ở §1 / §2): chất lượng nguồn TC (kết quả thực thi, môi trường đã chạy, evidence, tác giả TC, thiếu spec)
> và chất lượng từng TC (tiêu đề, tiền đề, steps, expected đo lường được, atomic, dữ liệu test).
> **Không có issue thật thì ghi "Không có"** — đừng đẻ issue cho đủ bảng.

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | | | |
| I2 | `[MAJOR]` | | | |
| I3 | `[MINOR]` | | | |
| I4 | `[NIT]` | | | |

<!-- Sắp xếp theo severity giảm dần. Issue về chất lượng NGUỒN (pass rate < 80%, 0 TC chạy production
     khi task dính RULE-08, evidence rỗng, TC fail chưa raise ticket, không tìm được spec) nằm TRÊN CÙNG. -->

---

## 5. TCs đề xuất bổ sung (`<n>`)

<!-- `<n>` = TỔNG SỐ DÒNG TC thật trong bảng dưới (không đếm row template rỗng, không đếm
     dòng "dùng lại TC kho"). VD có 20 TC đề xuất → tiêu đề ghi: ## 5. TCs đề xuất bổ sung (20).
     Không có TC nào → ## 5. TCs đề xuất bổ sung (0) + 1 dòng giải thích vì sao không cần bổ sung. -->

> Bảng dùng **12 cột của kho TCs** ([kho-tcs/README.md](../../kho-tcs/README.md)) — cùng format với output `/collect-tcs` — **cộng 2 cột `Chạy` / `Phạm vi ENV`** để map thẳng sang MCP LME TEST STUDIO. Tổng **14 cột**, **KHÔNG** phải 16 cột canonical của file 04.
> `/sync-review-tc` đọc bảng này rồi push về đúng nguồn TC gốc (Studio qua `testcase_create`, hoặc Sheet qua cột anchor "Main Function").
> Mỗi dòng `GAP` / `RISK` ở §1 + §2 phải có TC tương ứng ở đây (hoặc 1 câu giải thích vì sao không đề xuất).

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b — bắt buộc fill):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/<file>.md` / `kho-tcs chưa có FA-xxx — không đối chiếu được` |
| Vùng regression phát hiện từ kho | `<ID kho + nhóm chức năng, hoặc "không có">` |
| Conflict expected vs kho | `<TC đề xuất> vs <ID kho> → [MAJOR] SPEC-CONFLICT, đã đưa §6` / `Không` |
| GAP dùng lại TC kho (không viết mới) | `G<x> → <ID kho> "<tên case>"` / `Không` |
| Xác nhận chống trùng | Đã đối chiếu `<n>` TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-XXX000-01 | UI | | | Normal | manual | staging | | | | | | | Lấp `<G1 / Q1>` · Đánh giá spec: Spec ghi rõ · Evidence: `<loại>` |
| TC-XXX000-02 | API | | | Abnormal | manual | product | | | | | | | Lấp `<G2>` · RULE-08 · Evidence: `<loại>` |

> **Quy tắc cột** — xem [kho-tcs/README.md](../../kho-tcs/README.md) §Format 12 cột. Tóm tắt:
> - `ID` = `TC-<mã quan điểm bỏ gạch>-<nn>`, VD `TC-PERM002-01`. **Không trùng** ID trong bộ TC gốc và trong kho. ⚠️ KHÔNG dùng prefix tuần tự của kho (`TC-TAG-267`) — build kho đánh số lại mỗi lần chạy.
> - `Nhóm` = `UI` / `API` / `Data`, suy từ mã quan điểm theo `GROUP_MAP` ở [kho-tcs/data/_common.py](../../kho-tcs/data/_common.py) (khớp tiền tố dài nhất trước; không khớp → `UI`).
> - `Màn hình/chức năng` = nhóm chức năng trong màn (dùng đúng tên nhóm của file kho nếu kho đã có tính năng đó).
> - `Tên case` = mô tả thuần, **không** prefix `[<nhóm>]`, nhưng phải chứa keyword để Leader suy được impact.
> - `Loại case` **chỉ** `Normal` / `Abnormal` / `Boundary` — không có Regression (ghi chữ `regression` ở `Ghi chú`), không có cột Priority.
> - `Chạy` **chỉ** `auto` / `manual` → Studio `exec_mode`. Mặc định **`manual`**; `auto` chỉ khi TC thuần API/data chạy được bằng runner Studio.
> - `Phạm vi ENV` **chỉ** `Tất cả` / `staging` / `product` → Studio `env_scope`. Mặc định `staging`; **RULE-08** (media · domain · job · loadbalance · bill tiền · race · performance) → bắt buộc `product`; cần đối chiếu nhiều env → `Tất cả`.
> - `Kết quả thực thi` **để trống** — người test tự điền (khác file 04 ghi `Chưa test`).
> - `Ghi chú` gộp, ngăn bằng ` · `: **bắt buộc** `Lấp G<x> / Q<x>` · `Đánh giá spec: ...` · `Evidence: <loại>` (RULE-02) · `regression` · `dẫn từ <ID kho>`. **Không** ghi `Môi trường: ...` ở đây nữa — đã có cột `Phạm vi ENV`.
>   ⚠️ `Ghi chú` là cột **chỉ dùng trong file 05 này** — `/sync-review-tc` **KHÔNG** đẩy nó lên Studio hay Google Sheet. Thông tin nào cần có mặt trên test tool thì phải nằm ở cột riêng (`Phạm vi ENV`, `Chạy`, `Mã quan điểm`, ...), đừng nhét vào `Ghi chú`.
> - Copy sang `04-tc-list.md` (16 cột) → ánh xạ: `ID`→`TC No.` · `Tên case`→`Tiêu đề test case` · `Mã quan điểm`→`Mã quan điểm liên kết` · `Tiền điều kiện`→`Điều kiện tiền đề` · `Dữ liệu nhập`→`Dữ liệu test/input` · `Phạm vi ENV`→`Môi trường test`; tách `Ghi chú` trả lại `Trạng thái đánh giá spec`; `Kết quả thực thi` = `Chưa test`; `Nhóm`/`Màn hình/chức năng`/`Chạy` giữ trong `Ghi chú`.

---

## 6. Spec update needed

<!-- Bug fix đòi hỏi update spec cũ → ghi rõ để PM/Dev nắm. Không cần update → ghi đúng 1 dòng "Không cần update spec." -->

`Không cần update spec.` — hoặc:

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | | | `<TC vs spec / TC vs kho-tcs / DUP-CONFLICT §3>` | `Dev / Leader / PM` |
