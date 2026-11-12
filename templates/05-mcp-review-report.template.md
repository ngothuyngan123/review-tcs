# 05 — Review Report (task MCP)

> Draft cho Leader verify — sinh bởi `/review-tc-mcp`. Task nằm ở `MCP/<YYYY-MM-DD>_<ticket>_<slug>/`;
> vòng review ở tên file (`05-review-report.md` = round 1, `.round2.md` = round 2).
>
> **Chỉ ghi phần THIẾU + việc phải làm.** Ma trận tool × param, bảng rule, bảng prompt vẫn **bắt buộc chạy**
> nhưng là nháp nội bộ (scratchpad) — chỉ dòng `GAP` / `RISK` lên report (riêng §2 ghi đủ 7 rule).
> Chuẩn expected = docs tính năng ở `spec-features/mcp/docs/` + spec / kho (**KHÔNG** dùng `02-mcp-docs-review.md` — file đó chỉ để Leader đọc). Rule MCP = [framework/mcp-rules.md](../../framework/mcp-rules.md).
>
> **9 section**: §0 Nguồn · §1 Coverage tool × param · §2 Rule MCP bắt buộc · §3 E2E prompt · §4 Mâu thuẫn ·
> §5 Trùng lặp + issues khác · §6 TCs thừa · §7 TCs đề xuất bổ sung · §8 Spec update needed.
> ⚠️ §0 và tiêu đề §7 giữ **đúng format** của [05-review-report.template.md](../../templates/05-review-report.template.md) — `/sync-review-tc` parse 2 chỗ này.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #<id> — snapshot 04-tc-list.md fetch <ngày>` / `(2) Sheet <url> gid=<gid> — snapshot 04-tc-list.md` / `(3) 04-tc-list.md` |
| Tổng số TC review | `<n>` |

<!-- Đúng 2 dòng, như /review-tc. TC luôn đọc ở 04-tc-list.md; nguồn gốc (1)/(2)/(3) lấy từ header <!-- source: ... --> dòng đầu file 04 — giữ tiền tố để /sync-review-tc chọn đích push. -->

---

## 1. Coverage — hướng 2.1 (bám docs) + dev-impact

**Trả lời** (2 dòng bắt buộc):

| Chiều | Kết quả |
|---|---|
| **(a) tool × param** — ma trận MCP-RULE-06 dựng từ docs tính năng `spec-features/mcp/docs/<file>` | `<x>/<y> ô có TC` — **ĐỦ** / **CHƯA ĐỦ** |
| **(b) dev-impact** — `03-dev-impact.md` mục 4 (`F*` / `D*` / `T*`) + Studio `dev_impact` nếu có | `<x>/<y> mục có TC` — **ĐỦ** / **CHƯA ĐỦ** |

<!-- Mẫu số (a): mỗi tool × mỗi param × chiều áp dụng ở mcp-rules.md 2.2 (bắt buộc · kiểu · enum · biên · default · param lạ · kết hợp).
     Chiều không áp dụng cho param đó (vd param bool không có biên) → không đếm. Setting web mà docs MCP không có tool / param tương ứng → không thuộc mẫu số (MCP không expose).
     Chỉ ghi ĐỦ khi mọi ô có ≥ 1 TC và không ô nào RISK. -->

**Kết luận**: `<x>/<y> ô + mục đủ TC · <a> GAP · <b> RISK`.

| # | Tool · param / vùng | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `update_<x>.items[].max_length` | `tool×param` | `NEW-12` (max) | `RISK — có max, thiếu max+1` | `[MAJOR]` |
| G2 | `T2 — dữ liệu tạo qua MCP mở trên editor web` | `dev-impact` | `không có` | `GAP — 0 TC` | `[BLOCKER]` |

- Tham chiếu TC bằng **ID hiển thị trên nguồn** (Studio `NEW-xx`) — như §1 của [05-review-report.template.md](../../templates/05-review-report.template.md).
- `RISK` = có TC nhưng thiếu loại case / chưa chạy / **thiếu bước `get_*` verify** (MCP-RULE-05) / **thiếu mã HTTP** ở expected (RULE-13).
- Mỗi dòng `G<x>` **bắt buộc** có TC ở §7 (ngoại lệ như `/review-tc`: dùng lại TC kho / GAP giả có bằng chứng).

---

## 2. Rule MCP bắt buộc

> Ghi **đủ 7 dòng** (Leader cần thấy trạng thái từng rule kể cả khi OK). `Phạm vi` = tool / param ID mà rule áp vào.

| # | Rule | Phạm vi | Status | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|---|
| M1 | MCP-RULE-01 Bot A ↔ B | `<param ID: folder_id, tag_id, …>` | `OK / RISK / GAP` | | `<param ID nào × giá trị nào (cùng account / account khác / không tồn tại / sai loại) chưa có TC>` | |
| M2 | MCP-RULE-02 Staff | `<tool ghi + tool đọc>` | | | `<có quyền / không quyền / thu hồi khi token còn hạn>` | |
| M3 | MCP-RULE-03 Limit Free | | | | `<ngưỡng · vượt · đếm gộp web + MCP · khôi phục / copy trên web · Free cũ>` | |
| M4 | MCP-RULE-04 Trùng tên | | | | `<MCP vs MCP · MCP vs web · đổi tên qua update · bot khác · hoa/thường / khoảng trắng>` | |
| M5 | MCP-RULE-05 Get sau ghi | | | | `<TC create/update thiếu bước get_*: NEW-…>` | |
| M6 | MCP-RULE-06 Phủ param | — | — | — | `xem §1 chiều (a)` | — |
| M7 | MCP-RULE-07 Validate web → MCP | | | | `xem §2.1` | |

### 2.1 Kịch bản validate của web áp sang MCP

`<x>/<y> kịch bản áp dụng cho MCP đã có TC` — nguồn: `spec-features/…` + `kho-tcs/fa<xxx>-*.md` (+ sheet validate nếu human đưa link).
Chỉ liệt kê kịch bản **chưa có TC**:

| # | Validate (tham số MCP) | Nguồn | Expected (MCP-RULE-07) |
|---|---|---|---|
| V1 | `create_<x>.name` rỗng / chỉ khoảng trắng | `kho TC-<…>` | `400 hoặc 422 + message nêu rõ nguyên nhân` |

---

## 3. Coverage — hướng 2.2 E2E prompt (MCP-RULE-08)

`<x>/<y> tool đủ prompt` · `<a>/<b> prompt abnormal (mcp-rules.md 3.4)`. Chỉ liệt kê tool / ca **còn thiếu**:

| # | Tool | VN chi tiết | VN chung | Tiếng Nhật | Thiếu gì | Severity |
|---|---|---|---|---|---|---|
| P1 | `create_<x>` | `NEW-…` | `—` | `—` | `thiếu prompt chung + JP` | `[MAJOR]` |
| P2 | `(abnormal)` | — | — | — | `thiếu ca prompt nhắc dữ liệu bot khác` | `[MAJOR]` |

**Oracle của TC prompt đang có** — TC chấm theo câu trả lời chữ của AI thay vì chuỗi tool + param + trạng thái cuối → ghi ở đây:
`Không có` / `NEW-…: expected "AI trả lời đã tạo xong" — thiếu tool chain + get_*`.

---

## 4. Mâu thuẫn trong TCs

> Bắt buộc fill kể cả khi sạch. **KHÔNG tự chọn bên** — mọi loại đều nêu đủ 2 khả năng.
> `CONF-DOC` = expected của TC **trái docs MCP** ở `spec-features/mcp/docs/` → `(A) TC sai` / `(B) docs / code MCP cần update` ·
> `CONF-SPEC` / `CONF-KHO` / `CONF-TC` = như §4 của [05-review-report.template.md](../../templates/05-review-report.template.md).

| # | Loại | TC liên quan | Nội dung check | Expected của TC | Chuẩn đối chiếu | Đề xuất / khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-DOC` | `NEW-4` | `tạo trùng 管理名` | `cho phép` | `docs 04-form-survey.md §2: name không được trùng` | `(A) TC sai → sửa expected thành 400/422` / `(B) docs sai → Dev cập nhật docs` | `[MAJOR]` | `Leader` |

**Đã rà**: `<n>` TC × docs `spec-features/mcp/docs/<file>` + `<file spec + file kho>` — `<không phát hiện mâu thuẫn>` / `<C1..Cn>`.

---

## 5. TC trùng lặp + issues khác

### 5.1 Trùng lặp

> Tiêu chí **4 yếu tố** như BƯỚC 4b của `/review-tc`. Với TC MCP: `đối tượng + thao tác` = **tool + param + giá trị**.
> Bắt buộc fill: "Đã rà `<n>` TC, không phát hiện trùng lặp".

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|

### 5.2 Issues khác

> Chất lượng nguồn (pass rate, môi trường đã chạy, TC fail chưa ticket — BƯỚC 0.6 của `/review-tc`) trên cùng,
> rồi chất lượng từng TC. TC MCP hay sai: **thiếu mã HTTP** · **thiếu `get_*`** · sai kiểu mà không ghi **raw MCP client** · `Tiền điều kiện` không nói OAuth của account / staff nào.
> Không có → "Không có".

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|

---

## 6. TCs thừa / ngoài phạm vi task

> Flag khi đủ CẢ 3: (1) không chạm tool nào trong docs tính năng · (2) không map `F*`/`D*`/`T*` · (3) không thuộc MCP-RULE nào.
> Gate + cách ghi như §6 của [05-review-report.template.md](../../templates/05-review-report.template.md).
> Bắt buộc fill: "Đã rà `<n>` TC — không có TC nào ngoài phạm vi task".

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|

---

## 7. TCs đề xuất bổ sung (`<n>`)

<!-- `<n>` = số dòng TC thật trong bảng. Giữ nguyên cụm "TCs đề xuất bổ sung" — /sync-review-tc khớp theo cụm này. -->

> **15 cột** + quy tắc cột: y hệt §7 của [05-review-report.template.md](../../templates/05-review-report.template.md). Khác biệt riêng MCP:
> - **4 nguồn sinh TC** — mã ở đầu `Ghi chú`: `G<x>` (§1) · `M<x>` (§2, gồm `V<x>` của §2.1) · `P<x>` (§3) · `R<x>` (regression có căn cứ).
> - `Màn hình/chức năng` dòng đầu = **tên tool** đang test (TC hướng 2.1) / **chuỗi tool kỳ vọng** (TC prompt); cột `Surface` = `mcp` (thêm `, web` khi có bước kiểm màn web) → `/sync-review-tc` gắn `surfaces = ["mcp"]`.
> - TC `create_*` / `update_*` **có bước gọi `get_*`** (MCP-RULE-05, mẫu ở mcp-rules.md 2.3). Abnormal / Boundary ghi **mã HTTP** (400 hoặc 422 · 403 / 404).
> - TC **prompt E2E**: `Dữ liệu nhập` = prompt nguyên văn · `Chạy = manual` · `Ghi chú` mở đầu `Prompt: VN-chi tiết | VN-chung | JP-chi tiết | JP-chung` (mcp-rules.md 3.5).
> - Expected theo docs tính năng (`Ghi chú`: `theo docs <file> §<mục>`). Chỗ docs ↔ spec / kho mâu thuẫn → expected nêu cả 2 khả năng, `Ghi chú`: `Mâu thuẫn docs ↔ spec/kho — chờ Leader chốt` (trỏ dòng §4).

**Đã đối chiếu trước khi viết** (bắt buộc fill):

| Mục | Kết quả |
|---|---|
| Docs dùng làm chuẩn expected | `spec-features/mcp/docs/<file>[, …]` |
| File kho TCs đã đọc | `kho-tcs/<file>.md` / `kho-tcs chưa có FA-xxx` |
| Căn cứ TC regression `R<x>` | `<dòng dev_impact / ID kho / tool dùng chung>` / `Không có TC R` |
| Xác nhận chống trùng | Đã đối chiếu `<n>` TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM002-01 | API | PERM-002 | `update_<x><br>MCP sửa <Tên VN> <Tên JP>: truyền tag_id của bot khác cùng account` | Abnormal | auto | dev, local, prd, staging | mcp | | | 1. Gọi `update_<x>` với …<br>2. Gọi `get_<x>_detail` ở bot B | | - HTTP 403 hoặc 404<br>- `get_<x>_detail` bot B: không đổi | | Lấp `M1` · Evidence: request/response |
| TC-MCPE2E001-01 | API | MCP-E2E-001 | `create_<x> / update_<x><br>MCP prompt VN: <mục đích>` | Normal | manual | dev, local, prd, staging | mcp, web | | | 1. Mở <client AI>, kết nối connector MCP …<br>2. Gửi prompt ở Dữ liệu nhập<br>3. Xem log tool call<br>4. Gọi `get_<x>_detail` + mở màn web | `<prompt nguyên văn>` | - Tool được gọi: …<br>- Param: …<br>- get_*: … | | Prompt: VN-chi tiết · Lấp `P1` · manual vì client LLM thật (ChatGPT/Claude), phi tất định |

---

## 8. Spec update needed

> Nguồn: dòng §4 `CONF-DOC` / `CONF-SPEC` / `CONF-KHO` (docs ↔ spec / kho lệch) + param / hành vi chỉ docs MCP có mà spec-features chưa ghi.
> Không cần → đúng 1 dòng "Không cần update spec."

| # | Section spec | Nội dung cần update | Nguồn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/<feature>/feature-spec.md §<mục>` | | `C1 CONF-DOC` / `C2 CONF-SPEC` / `docs <file> §<mục> (chỉ MCP có)` | `Leader / PM` |
