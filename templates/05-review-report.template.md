# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder `tasks/<YYYY-MM-DD>_<ticket>_<slug>/`;
> vòng review nằm ở tên file (`05-review-report.md` = round 1, `.round2.md` = round 2).
>
> ⚠️ **Report chỉ ghi phần THIẾU + việc phải làm.** Bảng coverage 2 chiều và bảng quan điểm đối chiếu
> vẫn **bắt buộc chạy** ở BƯỚC 2 / 3 nhưng là **phân tích nội bộ — KHÔNG ghi vào file này**:
> chỉ những dòng `GAP` / `RISK` mới xuất hiện ở §1 / §2. Cái gì đã đủ TC thì **không viết dòng nào**.
>
> **9 section**: §0 Nguồn · §1 Coverage · §2 Quan điểm thiếu · §3 Trùng lặp · §4 Mâu thuẫn ·
> §5 Issues khác · §6 TCs thừa · §7 TCs đề xuất bổ sung · §8 Spec update needed.
>
> **KHÔNG ghi vào report** (bỏ 2026-09-21): cột `Evidence thực tế` rỗng · danh sách mã quan điểm không có
> trong `checklist-lme.md` (hệ quả đã nằm ở §2) · checkbox "Tester verify auto-fill chính xác" chưa tick.
> Đã bỏ từ trước: Verdict · Tóm tắt cho member · Coverage matrix đầy đủ · Fix-shape table · Bảng quan điểm đầy đủ · Checklist · Ký duyệt.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #<id> / (2) Sheet <url> gid=<gid> rows <a>-<b> / (3) 04-tc-list.md` |
| Tổng số TC review | `<n>` |

<!-- Đúng 2 dòng, không thêm dòng khác. Cảnh báo chất lượng nguồn (pass rate / môi trường đã chạy)
     KHÔNG ghi ở đây — flag nào thật sự là vấn đề thì đưa xuống §5. -->

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời** (2 dòng bắt buộc — câu hỏi chính của Leader: *TCs đã cover đủ 2 chiều chưa?*):

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | `<x>/<y> mục có TC` — **ĐỦ** / **CHƯA ĐỦ** |
| **(b) diff code** — suy từ diff thật (Studio `dev_impact` + `spec_delta`) | `<x>/<y> điểm có TC` — **ĐỦ** / **CHƯA ĐỦ** / **KHÔNG ĐÁNH GIÁ ĐƯỢC — Input thiếu: Studio chưa có diff** |

<!-- Mẫu số <y>: (a) = BUG root cause + từng F* + D* + T* ở mục 4 file 03.
     (b) = mỗi file/điểm sửa trong spec_delta.files[] + mỗi rủi ro hồi quy + mỗi hành vi đổi so với trước.
     Chỉ ghi ĐỦ khi MỌI mục có ≥ 1 TC và không mục nào ở trạng thái RISK. Không có diff → KHÔNG ĐÁNH GIÁ ĐƯỢC. -->

**Kết luận**: `<x>/<y> vùng ảnh hưởng đủ TC · <a> GAP · <b> RISK` — hoặc `Đủ coverage, không GAP`.

> Chỉ liệt kê phần **THIẾU**. Vùng nào đã đủ TC → **không ghi dòng nào**.
> **2 chiều bắt buộc rà** (BƯỚC 2):
> **(a) dev-impact** — `BUG` root cause + `F*` / `D*` / `T*` ở `03-dev-impact.md` mục 4 (thứ Dev **tự kê**).
> **(b) diff code** — ảnh hưởng suy từ **diff thật**, lấy ở **tab Thông tin của MCP LME TEST STUDIO**: `task_get_context(task_id, sections=["dev_impact","spec_delta"])` → `dev_impact` (điểm sửa · rủi ro hồi quy · hành vi đổi so với trước) + `spec_delta.files[]` / `diffStat`. Studio không có diff → fallback mục 1 + 2 + 3 của `03-dev-impact.md`. Chiều này bắt cái mà **dev-impact không kê ra**.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `F2 — <function>` | `dev-impact` | `không có` | `GAP — 0 TC cover` | `[BLOCKER]` |
| G2 | `<file / hàm nằm trong diff>` | `diff code` | `NEW-9` | `RISK — fix là generic catch nhưng TC chỉ trigger 1 điều kiện` | `[MAJOR]` |

> ⚠️ **ID khi tham chiếu TC (áp dụng cho §1 · §2 · §3 · §4 · §5 · §6)**: dùng **ID hiển thị trên nguồn**, để Leader mở đúng bản ghi:
> - Nguồn **Studio** → `temp_id` dạng **`NEW-7`** / `NEW-28` (cột `TC No.` của `04-tc-list.md` đã là ID này; mã theo quan điểm nằm ở cột `Ghi chú`). Không có `temp_id` → `#<studio id>`.
> - Nguồn **Sheet / file 04 do người viết** → dùng đúng ID trong cột đầu của nguồn.
> - **Không** tự đặt lại mã `TC-<quan điểm>-<nn>` cho TC đã tồn tại — mã đó chỉ dùng cho **TC mới đề xuất ở §7** (chưa có trên tool nên chưa có ID).

- `Chiều`: `dev-impact` · `diff code`. ⚠️ **Không còn `orphan`** — TC không thuộc vùng nào chuyển sang **§6 TCs thừa**.
- `Thiếu gì`: `GAP` = 0 TC cover · `RISK` = có TC nhưng thiếu loại case / chưa chạy (`skip` / `Chưa test`) / expected dừng trước output cuối (RULE-06) / chỉ verify UI không verify DB (RULE-07).
- Không đọc được diff (Studio `diffAvailable = false` **và** file 03 không mô tả điểm sửa) → ghi 1 dòng:
  `Input thiếu: không có diff — chiều (b) chỉ suy được từ mô tả cách fix`.
- Mỗi dòng ở đây **BẮT BUỘC** có TC tương ứng ở §7. Chỉ **2 ngoại lệ** được thay TC bằng 1 câu giải thích:
  (1) kho-tcs đã có TC cover đúng GAP đó → dẫn chiếu `<ID kho>`; (2) GAP giả đã loại bằng bằng chứng spec/kho
  (BƯỚC 5a — "Trigger quan điểm ≠ bằng chứng có ảnh hưởng").

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
- **KHÔNG** dùng §4 "Quan điểm chưa đủ bằng chứng" của checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) để flag BLOCKER/MAJOR — **RULE-11**, chỉ được nêu ở mức `[NIT]` (ghi xuống §5).

---

## 3. TC trùng lặp nội dung

> BƯỚC 4b. So theo **ý định test** (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương), KHÔNG so chuỗi.
> **Bắt buộc fill kể cả khi không có trùng** — ghi "Đã rà `<n>` TC, không phát hiện trùng lặp".

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-8` | `NEW-7` | `DUP-EXACT / DUP-SUBSET / DUP-INFLATE` | | `[MINOR]` / `[MAJOR]` |

<!-- ID dùng đúng ID hiển thị trên nguồn (Studio: NEW-xx) — xem ghi chú ở §1. -->


- **Gate đã chạy**: giả định xóa các TC trên → coverage §1 + quan điểm §2 còn nguyên? `Có / Không → đổi sang GỘP: <TC No.>`
- `DUP-INFLATE` → impact/quan điểm bị che GAP: `<liệt kê, đã thêm dòng tương ứng vào §1 / §2>`
- Xóa thật do human thực hiện: nguồn Studio → `testcase_delete`; nguồn Sheet / file 04 → member tự xóa.
- ⚠️ 2 TC cùng nội dung check nhưng **expected loại trừ nhau** KHÔNG ghi ở đây — đó là **mâu thuẫn**, ghi ở **§4** (`CONF-TC`).

---

## 4. Mâu thuẫn trong TCs

> BƯỚC 4c. Hỏi: *TC này có **trái** một chuẩn nào đó không?* — 3 loại:
> `CONF-TC` = 2 TC cùng `đối tượng + thao tác` + tiền đề tương đương nhưng `Kết quả mong đợi` **loại trừ nhau** ·
> `CONF-SPEC` = expected trái **Business rule** ở `spec-features/<feature>/feature-spec.md` ·
> `CONF-KHO` = expected trái **TC kho** ở `kho-tcs/fa<xxx>-*.md` cùng chức năng.
> **Bắt buộc fill kể cả khi sạch.** **KHÔNG tự chọn bên, KHÔNG sửa TC** — mỗi dòng nêu đủ 2 khả năng.

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-TC` | `NEW-8` vs `NEW-15` | `<cùng thao tác + tiền đề gì>` | `<expected của NEW-8>` | `<expected của NEW-15>` | `1 trong 2 TC sai chuẩn` | `[MAJOR]` | `Dev / Leader` |
| C2 | `CONF-SPEC` | `NEW-3` | `<hành vi gì>` | `<expected của TC>` | `feature-spec.md §<mục> BR-<nn>: "<trích>"` | `TC sai` / `spec cũ hơn bản fix → cần update` | `[MAJOR]` | `Dev / PM` |
| C3 | `CONF-KHO` | `NEW-21` | `<hành vi gì>` | `<expected của TC>` | `<ID kho> "<tên case>"` | `TC sai` / `kho cũ hơn bản fix → cần update` | `[MAJOR]` | `Leader` |

**Đã rà**: `<n>` TC × `spec-features/<feature>/feature-spec.md` + `kho-tcs/<file>.md` — `<không phát hiện mâu thuẫn>` /
`<liệt kê C1..Cn>`. Không có file kho / spec của tính năng → ghi rõ (`kho-tcs chưa có FA-xxx` / `không có spec`),
**không** ghi là "đã rà sạch".

- Mỗi dòng ở đây **bắt buộc** có 1 dòng tương ứng ở **§8 Spec update needed**.
- `CONF-SPEC` trái đúng rule thuộc root cause / `BUG` → `[BLOCKER]`.
- Mâu thuẫn làm một vùng ảnh hưởng / quan điểm **mất chuẩn đánh giá Đạt–Không đạt** → thêm dòng `RISK` ở §1 / §2.

---

## 5. Issues khác

> Chỉ ghi issue **không phải GAP coverage** (§1 / §2), **không phải mâu thuẫn** (§4), **không phải TC thừa** (§6):
> chất lượng nguồn TC (kết quả thực thi, môi trường đã chạy, thiếu spec) và chất lượng từng TC
> (tiêu đề, tiền đề, steps, expected đo lường được, atomic, dữ liệu test).
> **Không có issue thật thì ghi "Không có"** — đừng đẻ issue cho đủ bảng.
>
> ⛔ **3 thứ KHÔNG được ghi** (bỏ 2026-09-21): cột `Evidence thực tế` rỗng · danh sách mã quan điểm không có
> trong `checklist-lme.md` · checkbox "Tester verify auto-fill chính xác" chưa tick.

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | | | |
| I2 | `[MAJOR]` | | | |
| I3 | `[MINOR]` | | | |
| I4 | `[NIT]` | | | |

<!-- Sắp xếp theo severity giảm dần. Issue về chất lượng NGUỒN (pass rate < 80%, 0 TC chạy production
     khi task dính RULE-08, TC fail chưa raise ticket, không tìm được spec) nằm TRÊN CÙNG. -->

---

## 6. TCs thừa / ngoài phạm vi task

> BƯỚC 4d. Trả lời: *có TC nào không cần test trong phạm vi task này không?*
> **Flag khi đủ CẢ 3**: (1) không map được `BUG`/`F*`/`D*`/`T*` · (2) không nằm trong điểm sửa / rủi ro hồi quy /
> hành vi đổi mà Studio `dev_impact` + `spec_delta` nêu · (3) không thuộc quan điểm nào Trigger khớp task.
> **Cộng thêm**: TC test **layer KHÔNG bị chạm code** (root fix ở layer A, TC test layer downstream không đổi).
> **Bắt buộc fill kể cả khi không có** — ghi "Đã rà `<n>` TC — không có TC nào ngoài phạm vi task".

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | `NEW-14` | `không map BUG/F*/D*/T* · không nằm trong diff · không thuộc quan điểm nào trigger` | `spec_delta.files[] không có <file>` | `bỏ khỏi phạm vi task` | `[MINOR]` |
| X2 | `NEW-22` | `test layer <B> — root fix ở layer <A>, layer <B> không bị chạm code` | `dev_impact chỉ nêu <A>` | `chuyển sang bộ regression chung của kho` | `[NIT]` |

- **Gate đã chạy**: TC bị flag có phải **TC duy nhất** cover một impact / quan điểm không? `Không` → flag hợp lệ ·
  `Có` → **bỏ khỏi bảng này**.
- TC regression **dẫn được** từ rủi ro hồi quy của Studio hoặc vùng regression kho-tcs → **KHÔNG** phải TC thừa.
- Không chắc ý định của TC → **không flag**, thay bằng 1 dòng `[NIT]` ở §5 hỏi member.
- **Không tự xóa** — human xóa trên Studio (`testcase_delete`) hoặc member tự xóa ở Sheet / file 04.

---

## 7. TCs đề xuất bổ sung (`<n>`)

<!-- `<n>` = TỔNG SỐ DÒNG TC thật trong bảng dưới (không đếm row template rỗng, không đếm
     dòng "dùng lại TC kho"). VD có 20 TC đề xuất → tiêu đề ghi: ## 7. TCs đề xuất bổ sung (20).
     Không có TC nào → ## 7. TCs đề xuất bổ sung (0) + 1 dòng giải thích vì sao không cần bổ sung. -->

> Bảng dùng **12 cột của kho TCs** ([kho-tcs/README.md](../../kho-tcs/README.md)) — cùng format với output `/collect-tcs` — **cộng 2 cột `Chạy` / `Phạm vi ENV`** để map thẳng sang MCP LME TEST STUDIO. Tổng **14 cột**, **KHÔNG** phải 16 cột canonical của file 04.
> `/sync-review-tc` đọc bảng này rồi push về đúng nguồn TC gốc (Studio qua `testcase_create`, hoặc Sheet qua cột anchor "Main Function").
> **3 nguồn sinh TC** — mã ghi ở đầu cột `Ghi chú`:
> - **`G<x>`** = dòng `GAP` / `RISK` ở §1 — **bắt buộc** có TC (2 ngoại lệ: dùng lại TC kho / GAP giả đã loại bằng bằng chứng).
> - **`Q<x>`** = dòng ở §2 — 1 TC cụ thể, hoặc 1 câu giải thích vì sao không đề xuất.
> - **`R<x>`** = **regression theo đánh giá của AI**, không đến từ §1/§2: suy từ `dev_impact.rủi ro hồi quy` của Studio ·
>   vùng regression bắt được khi đối chiếu kho-tcs · nơi gọi chung / sibling flow của hàm bị sửa.
>   **Bắt buộc nêu căn cứ** ở `Ghi chú` — không có căn cứ thì không đẻ TC.

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b — bắt buộc fill):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/<file>.md` / `kho-tcs chưa có FA-xxx — không đối chiếu được` |
| Vùng regression phát hiện từ kho | `<ID kho + nhóm chức năng, hoặc "không có">` |
| Conflict expected vs kho | `<TC đề xuất> vs <ID kho> → CONF-KHO, đã đưa §4 + §8` / `Không` |
| GAP dùng lại TC kho (không viết mới) | `G<x> → <ID kho> "<tên case>"` / `Không` |
| Căn cứ TC regression `R<x>` | `<dòng rủi ro hồi quy của Studio / <ID kho> / caller cụ thể>` — hoặc `Không có TC R` |
| Xác nhận chống trùng | Đã đối chiếu `<n>` TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-XXX000-01 | UI | | | Normal | auto | staging | | | | | | | Lấp `<G1 / Q1>` · Đánh giá spec: Spec ghi rõ · Evidence: `<loại>` |
| TC-XXX000-02 | API | | | Abnormal | manual | product | | | | | | | Lấp `<G2>` · RULE-08 · manual vì môi trường production · Evidence: `<loại>` |
| TC-XXX000-03 | UI | | | Normal | auto | staging | | | | | | | Lấp `<R1>` · regression · dẫn từ `<ID kho / dòng dev_impact>` · Evidence: `<loại>` |

> **Quy tắc cột** — xem [kho-tcs/README.md](../../kho-tcs/README.md) §Format 12 cột. Tóm tắt:
> - `ID` = `TC-<mã quan điểm bỏ gạch>-<nn>`, VD `TC-PERM002-01`. **Không trùng** ID trong bộ TC gốc và trong kho. ⚠️ KHÔNG dùng prefix tuần tự của kho (`TC-TAG-267`) — build kho đánh số lại mỗi lần chạy.
> - `Nhóm` = `UI` / `API` / `Data`, suy từ mã quan điểm theo `GROUP_MAP` ở [kho-tcs/data/_common.py](../../kho-tcs/data/_common.py) (khớp tiền tố dài nhất trước; không khớp → `UI`).
> - `Màn hình/chức năng` = nhóm chức năng trong màn (dùng đúng tên nhóm của file kho nếu kho đã có tính năng đó).
> - `Tên case` = mô tả thuần, **không** prefix `[<nhóm>]`, nhưng phải chứa keyword để Leader suy được impact.
> - `Loại case` **chỉ** `Normal` / `Abnormal` / `Boundary` — không có Regression (ghi chữ `regression` ở `Ghi chú`), không có cột Priority.
> - `Chạy` **chỉ** `auto` / `manual` → Studio `exec_mode`. **Mặc định `auto`** — bám quy tắc chọn `exec_mode` của Studio (`skill_doc_get`: "⛔ ĐỪNG mặc định manual"):
>   - `auto` khi runner Studio kiểm chứng tự động được ở local bằng **bất kỳ tầng nào**: browser tự động (kể cả TC nhóm `UI`), gọi API, dispatch job / mô phỏng callback LINE, unit/integration, kiểm tra tĩnh source. **Nhóm `UI` ≠ `manual`.** Bước "bạn bè thao tác trên LINE" (gửi tin, trả lời trích dẫn, bấm nút, kết bạn) **không** phải lý do `manual` — runner mô phỏng được callback.
>   - `manual` **CHỈ** khi bắt buộc 1 trong 4: **(1)** `Phạm vi ENV = product` (production / dữ liệu khách hàng thật); **(2)** thiết bị thật — app admin mobile, kết quả phải nhìn trên app LINE thật (RULE-06), camera quét QR; **(3)** email / mail thật trong hộp thư; **(4)** mắt người phán đoán — so ảnh trước/sau, font, màu, bố cục.
>   - TC `manual` **bắt buộc** ghi lý do ở `Ghi chú`: `manual vì <1 trong 4 lý do>`. Không nêu được lý do thuộc 4 nhóm trên → để `auto`.
> - `Phạm vi ENV` **chỉ** `Tất cả` / `staging` / `product` → Studio `env_scope`. Mặc định `staging`; **RULE-08** (media · domain · job · loadbalance · bill tiền · race · performance) → bắt buộc `product`; cần đối chiếu nhiều env → `Tất cả`.
> - `Kết quả thực thi` **để trống** — người test tự điền (khác file 04 ghi `Chưa test`).
> - `Ghi chú` gộp, ngăn bằng ` · `: **bắt buộc** `Lấp G<x> / Q<x> / R<x>` (TC `R<x>` thêm `regression` + căn cứ) · `Đánh giá spec: ...` · `Evidence: <loại>` (RULE-02) · `regression` · `dẫn từ <ID kho>`. **Không** ghi `Môi trường: ...` ở đây nữa — đã có cột `Phạm vi ENV`.
>   ⚠️ `Ghi chú` là cột **chỉ dùng trong file 05 này** — `/sync-review-tc` **KHÔNG** đẩy nó lên Studio hay Google Sheet. Thông tin nào cần có mặt trên test tool thì phải nằm ở cột riêng (`Phạm vi ENV`, `Chạy`, `Mã quan điểm`, ...), đừng nhét vào `Ghi chú`.
> - Copy sang `04-tc-list.md` (16 cột) → ánh xạ: `ID`→`TC No.` · `Tên case`→`Tiêu đề test case` · `Mã quan điểm`→`Mã quan điểm liên kết` · `Tiền điều kiện`→`Điều kiện tiền đề` · `Dữ liệu nhập`→`Dữ liệu test/input` · `Phạm vi ENV`→`Môi trường test`; tách `Ghi chú` trả lại `Trạng thái đánh giá spec`; `Kết quả thực thi` = `Chưa test`; `Nhóm`/`Màn hình/chức năng`/`Chạy` giữ trong `Ghi chú`.

---

## 8. Spec update needed

<!-- Bug fix đòi hỏi update spec cũ → ghi rõ để PM/Dev nắm. Không cần update → ghi đúng 1 dòng "Không cần update spec." -->

`Không cần update spec.` — hoặc:

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | | | `<C1 CONF-TC / C2 CONF-SPEC / C3 CONF-KHO ở §4>` | `Dev / Leader / PM` |

<!-- Mỗi dòng ở §4 phải có đúng 1 dòng tương ứng ở đây. -->
