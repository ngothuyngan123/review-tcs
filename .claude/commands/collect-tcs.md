---
description: Gom TCs rời rạc của 1 tính năng từ nhiều file Google Sheet trên Drive → loại trùng, xử lý conflict theo TC mới nhất, format lại 12 cột của kho, đối chiếu spec-features và xuất ra kho TCs tổng hợp (1 tab / tính năng, tên tab "<Mã màn hình> <Tên VN> (<Tên JP>)").
argument-hint: <tên tính năng, vd "Tag" hoặc "FA-012" — để trống sẽ liệt kê cho chọn>
---

Bạn là Test Leader gom kho TCs cho dự án LME. Nhiệm vụ: lấy TCs rời rạc của **1 tính năng** nằm rải ở nhiều file Google Sheet trên Drive, gộp thành **một bộ TCs chuẩn duy nhất**, đối chiếu với spec, và xuất vào **kho TCs tổng hợp** (mỗi tính năng = 1 tab).

**Tính năng cần gom:** `$ARGUMENTS`

Nếu `$ARGUMENTS` trống → liệt kê các tính năng đã có trong `spec-features/admin/` kèm trạng thái (đã gom / chưa gom, tra ở [kho-tcs/README.md](../../kho-tcs/README.md)), hỏi user chọn 1. **KHÔNG tự đoán.**

> **Chạy MỘT tính năng mỗi lần.** Xong thì DỪNG, báo cáo, chờ user duyệt rồi mới chạy tính năng tiếp theo.

---

## Bối cảnh cố định

| Thứ | Giá trị |
|---|---|
| Folder TCs nguồn trên Drive | `1eWgC1GnG6n8JvYGcBcbyPZLfDRiJLIKG` (57 file, ~700 tab) |
| Kho TCs đích | id lưu ở [kho-tcs/.sheet-id](../../kho-tcs/.sheet-id) (gitignored) |
| Spec đối chiếu | `spec-features/admin/<feature>/` |
| Code sinh output | [kho-tcs/build.py](../../kho-tcs/build.py) + `kho-tcs/data/*.py` |
| Script liệt kê nguồn | [scripts/list_tc_sources.py](../../scripts/list_tc_sources.py) |
| Script lấy grid (bung merged cell) | [scripts/fetch_grid.py](../../scripts/fetch_grid.py) |

---

## BƯỚC 1 — TÌM NGUỒN

```
python scripts/list_tc_sources.py <keyword>              # lọc theo tính năng
python scripts/list_tc_sources.py <keyword> --json s.json # kèm xuất JSON
python scripts/list_tc_sources.py                        # xem toàn bộ 57 file
```

Script đã tự lo: phân trang Drive, **retry 503** (Sheets API hay lỗi rải rác khi quét nhiều file),
lọc tab không phải TC (`Info`, `ListBug`, `Q&A`, `Bug UI/logic`, `Copy of *`, `Sheet*`, …),
bỏ qua chính file kho TCs đích, và khớp keyword theo **ranh giới từ** (nếu không `tag` sẽ
khớp nhầm `sTAGing`).

Sau khi chạy:

1. **Nếu script báo file KHÔNG đọc được** → chạy lại cho tới khi sạch. Đừng kết luận thiếu nguồn
   khi còn file lỗi.
2. **Quét thêm bằng từ khoá phụ** — tên tính năng tiếng Việt/Nhật/viết tắt (VD `tag` · `thẻ` · `タグ`).
3. **Mở thủ công các file "chung"** dù keyword không khớp: `TCsLine_Improve chung`, `TCsLine_JOB`,
   `TCsLine_ModalAction`, `TCsLine_Modal Filter`, `TCsLine_MCP` — chúng chứa tab lẻ của nhiều tính năng.

**Output bước này**: bảng `<file> · <tab> · <số dòng>` in ra cho user duyệt trước khi đọc.

---

## BƯỚC 2 — XÁC ĐỊNH NIÊN ĐẠI TỪNG TAB

Đây là cơ sở để xử lý conflict. Với mỗi file có tab liên quan:

1. Đọc tab **`Info`** — cấu trúc `Date | Content | Link testcase`. Đây là nguồn ngày đáng tin nhất.
2. Bổ sung từ: ngày trong **tên tab** (`Improve tag t2/2025`), ngày trong **header cột kết quả**
   (`Bug KH #35869 4//2026`), và `modifiedTime` của file.
3. Xác định đâu là **tab master còn sống** — tab được cập nhật liên tục qua nhiều đợt
   (nhận biết: có nhiều cột kết quả test theo từng ticket). Tab này thắng các tab lẻ cũ.

**Cảnh báo bắt buộc**: nếu 2 khối TC mâu thuẫn nhau mà **niên đại gần nhau** (cùng tháng, hoặc
ngày ticket và ngày test lệch nhau), phải ghi rõ *"quy tắc ưu tiên TC mới nhất là căn cứ YẾU ở
trường hợp này"* và nêu lý do thật sự chọn khối nào (VD: chi tiết hơn, phân biệt được nhiều case hơn).

---

## BƯỚC 3 — ĐỌC DỮ LIỆU (BẮT BUỘC BUNG MERGED CELL)

⚠️ **Đây là chỗ dễ sai nhất.** Các file TCs cũ dùng cấu trúc cây
`Assign | Main Function | Sub1..Sub5 | Expect Result` với **ô gộp (merged cell)**.
Đọc bằng `values.get` thuần sẽ trả ô rỗng → **sai phân cấp**, TC bị gán nhầm nhóm cha.

**Luôn dùng**:
```
python scripts/fetch_grid.py <spreadsheet_id> <out.json> "<tab 1>" "<tab 2>" ...
```
Script này lấy `sheets.merges` từ API và bung giá trị ô gộp ra từng dòng.

Sau khi có grid, dump dạng cây để ĐỌC (không parse máy móc rồi tin ngay):
- Tìm dòng header chứa `Main Function`; các cột path = `Main Function` + các cột `Sub*` liên tiếp.
- Cột kết quả = cột chứa `Expect Result`.
- Dòng có `Expect Result` không rỗng = 1 TC lá.

**Lưu ý cấu trúc thực tế**:
- Có 2 dòng header (dòng 2 và dòng 3) — bỏ qua dòng thứ 2.
- Xen giữa TC có **dòng mô tả bug** (text rất dài, gộp hết các cột path) — đây là header khối,
  KHÔNG phải TC. Nhận biết: độ dài > 200 ký tự.
- Có dòng bị **mồ côi** (Main Function rỗng do tác giả phá merge) — đọc bằng mắt để gán đúng khối,
  đừng tin forward-fill.
- File MCP dùng format **phẳng** khác hẳn (`TC ID | MCP Tool | Category | Scenario | ...`) —
  xử lý riêng, và hỏi user có đưa vào phạm vi không (xem BƯỚC 8).

---

## BƯỚC 4 — LOẠI TRÙNG & XỬ LÝ CONFLICT

| Tình huống | Xử lý |
|---|---|
| Cùng đường dẫn chức năng + **cùng** kết quả mong đợi | Giữ 1, ghi cả 2 nguồn ở `Ghi chú` |
| Cùng chức năng + kết quả mong đợi **khác nhau** | **Ưu tiên TC mới nhất** → đưa vào bảng mâu thuẫn nếu ảnh hưởng hành vi |
| TC thuộc luồng đã bị đợt improve mới thay thế | Loại; ghi vào bảng mâu thuẫn nếu ảnh hưởng hành vi |
| TC chỉ có tiêu đề, **không có** kết quả mong đợi | GIỮ nội dung nhưng phải **tự viết** kết quả mong đợi đo lường được; ghi rõ ở `Ghi chú`: "TC gốc chỉ có tiêu đề" |
| TC quá cũ (> 2 năm) | Giữ nhưng ghi rõ tuổi + "CẦN VERIFY LẠI" ở `Ghi chú` |

**Truy vết bắt buộc**: mỗi TC ghi nguồn ở cột `Ghi chú` dạng `Nguồn: r<số dòng>` (hoặc
`<file>/<tab> r<số dòng>` nếu khác file chính).

---

## BƯỚC 5 — ĐỐI CHIẾU SPEC-FEATURES

Đọc `spec-features/admin/<feature>/`: `feature-spec.md`, `web/logic-spec.md`, `web/api-spec.md`, `db/db-mapping.md`.

Soi 5 loại lệch:

1. **TC vs spec khác nhau** → mâu thuẫn thật, cần Leader quyết.
2. **Spec tự mâu thuẫn** (BR nói A, pseudo-code nói B, response mẫu nói C) → nêu cả 3 chỗ kèm `file:line`.
3. **Rule chỉ có trong TC, spec không ghi** → spec bỏ sót, đề xuất bổ sung.
4. **TC lấp Gap của spec** (spec ghi "chưa xác nhận" / confidence Thấp mà TC đã test thật) → đề xuất đóng Gap.
5. **Vùng mù giữa 2 spec** (VD form con của shared component chưa ai scan) → nêu rõ ảnh hưởng bao nhiêu tính năng.

**Bảng mâu thuẫn — 10 cột bắt buộc**:
`ID · Mức độ · Trạng thái · Chủ đề · TCs nói gì (nguồn) · Spec nói gì (nguồn) · Vì sao mâu thuẫn · TC liên quan · QUYẾT ĐỊNH CỦA LEADER · Việc phải làm tiếp`

- `ID` = `MT-01`, `MT-02`, …
- `Mức độ` = `CAO` (ảnh hưởng hành vi người dùng cuối) / `TRUNG BÌNH` / `THẤP`
- `Trạng thái` = `⏳ CHỜ QUYẾT ĐỊNH` → `✅ ĐÃ CHỐT`
- Cột `Spec nói gì` phải có **`file:line`** cụ thể, không nói chung chung.
- Cột `QUYẾT ĐỊNH` để **TRỐNG** cho Leader điền — **TUYỆT ĐỐI không tự chọn bên nào**.

---

## BƯỚC 6 — VIẾT TC THEO 12 CỘT CỦA KHO

> ⚠️ Kho TCs dùng **format riêng 12 cột**, **KHÁC** 16 cột canonical của `/write-tc` và
> `/review-tc` (task folder). Đừng lẫn 2 format.

| # | Cột | Ghi chú |
|---|---|---|
| 1 | `ID` | `TC-<PREFIX>-<nn>` — `build.py` tự sinh |
| 2 | `Nhóm` | `UI` / `API` / `Data` — tầng kiểm chứng, tự suy từ mã quan điểm |
| 3 | `Mã quan điểm` | mã trong [framework/checklist-lme.md](../../framework/checklist-lme.md) |
| 4 | `Màn hình/chức năng` | nhóm chức năng trong màn — chính là tham số `sec` của `tc()` |
| 5 | `Loại case` | `Normal` / `Abnormal` / `Boundary` |
| 6 | `Tên case` | tiêu đề TC |
| 7 | `Tiền điều kiện` | |
| 8 | `Các bước thực hiện` | |
| 9 | `Dữ liệu nhập` | |
| 10 | `Kết quả mong đợi` | |
| 11 | `Kết quả thực thi` | **luôn để trống** — người test tự điền |
| 12 | `Ghi chú` | |

**Đã bỏ** so với 16 cột canonical: `Evidence thực tế` · `Môi trường test` · `Người thực hiện` ·
`Ngày thực hiện` · `Số ticket bug` · `Trạng thái đánh giá spec`. Hai cột `Môi trường test` và
`Trạng thái đánh giá spec` **không mất thông tin**: vẫn truyền `env=` / `spec=` cho `tc()` như cũ,
`build.py` tự ghép vào đầu cột `Ghi chú` dạng `Môi trường: PRODUCTION · Đánh giá spec: Đã hỏi leader · <ghi chú>`.

### Cột `Nhóm` (UI / API / Data)

- `UI` — kiểm chứng bằng mắt trên màn hình (admin hoặc LINE user).
- `API` — kiểm chứng ở tầng xử lý server: gửi tin, job nền, tích hợp ngoài, thanh toán,
  phân quyền, đồng thời, hiệu năng.
- `Data` — kiểm chứng ở tầng dữ liệu: DB, đếm số, tham chiếu, migration, dữ liệu cũ.

Suy **tự động** từ mã quan điểm theo bảng `GROUP_MAP` trong
[kho-tcs/data/_common.py](../../kho-tcs/data/_common.py) — không cần khai báo tay.
Chỗ nào bảng suy sai thì ghi đè từng TC bằng `group="API"` trong lời gọi `tc()`.
Thêm quan điểm mới mà chưa có trong `GROUP_MAP` → mặc định rơi vào `UI`, **nhớ bổ sung tiền tố vào bảng**.

### Đánh số và tiêu đề

- **ID** = `TC-<PREFIX>-<nn>` chạy **TUẦN TỰ theo thứ tự màn hình/chức năng**
  (VD `TC-TAG-01` → `TC-TAG-266`). **KHÔNG** đánh lại theo mã quan điểm.
- **Tên case** = mô tả thuần, **KHÔNG** còn prefix `[<nhóm chức năng>]` — nhóm chức năng
  đã có cột riêng `Màn hình/chức năng`.
- Thứ tự nhóm khai báo ở `SECTIONS_*` trong [kho-tcs/data/_common.py](../../kho-tcs/data/_common.py).
  **Hỏi user thứ tự nhóm** nếu tính năng mới chưa có.

### Quy tắc TÁCH TC

> **Mỗi kết quả mong đợi khác nhau = 1 TC riêng.**

Giữ chung 1 TC **chỉ khi**:
- Nhiều input khác nhau nhưng **cùng 1 kết quả** (latinh / JP full-width / half-width đều lưu OK)
- Các bước là **1 chuỗi thao tác liên tiếp** không tách rời (race condition, `FUNC-SEQ-*`)
- Verify **3 tầng** DB + màn hình + output của **cùng 1 hành động** (RULE-07 — không phải nhiều state)

Ví dụ đúng: cột hiển thị có 3 state (không limit / chưa đạt / đã đạt, mỗi state 1 expected khác nhau)
→ **3 TC**. Ma trận N điểm mà **kết quả khác nhau** → **N TC**; ma trận N điểm mà **cùng kết quả**
→ **1 TC** liệt kê đủ N điểm ở cột `Dữ liệu nhập`.

### Nội dung từng cột

- `Tiền điều kiện`: đủ để người khác dựng được env — account, data seed, số lượng bản ghi cụ thể.
- `Các bước thực hiện`: đánh số `1.` `2.` `3.`, xuống dòng bằng `\n` (build.py tự đổi thành `<br>` cho markdown).
- `Dữ liệu nhập`: giá trị nghiệp vụ cụ thể, có phép tính tay nếu có số đếm. Không "data dummy".
- `Kết quả mong đợi`: **đo lường được**. Áp **RULE-06** (đi tới output cuối: LINE app / app mobile /
  file tải về / mail) và **RULE-07** (khớp DB + màn hình + output).
- `Kết quả thực thi`: **để trống**, không điền `Chưa test`.
- `Ghi chú`: nguồn `r<dòng>` · loại evidence bắt buộc · mã mâu thuẫn `MT-xx` · cảnh báo tuổi TC ·
  lý do giữ chung nếu TC gộp nhiều input.
- Vẫn truyền cho `tc()` như cũ (build.py tự ghép vào `Ghi chú`):
  - `env=`: `PRODUCTION` bắt buộc với media · domain · **job** · loadbalance · bill tiền ·
    race condition · performance (**RULE-08**).
  - `spec=`: `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`.
    Dùng `Đã hỏi leader` cho TC gắn với mâu thuẫn đã được Leader chốt.

---

## BƯỚC 7 — AUDIT COVERAGE

Trước khi xuất, đối chiếu bộ TC với **2 nguồn**:

1. **Danh sách chức năng của user** (nếu user đưa) — mỗi mục phải có ≥ 1 TC.
2. **Corpus nguồn** — duyệt lại khối `Check UI` và các dòng chỉ-có-tiêu-đề trong tab gốc,
   đảm bảo không bỏ sót.

Đặc biệt kiểm 5 chỗ hay lọt:
- Khối `Check UI` (title màn hình, link manual, các nút thao tác, menu 3 chấm) — thường bị bỏ vì không có expected.
- **Toàn bộ field editable** của màn edit — đối chiếu **Field Traceability Matrix** trong `feature-spec.md`.
- Ma trận điểm gắn/kích hoạt — đếm đủ số điểm theo corpus, đừng gộp nhóm.
- Empty state của từng màn.
- Case bulk thật sự (nhiều bản ghi), không chỉ 1 bản ghi.

In bảng `<nhóm chức năng> · <số TC> · <dải TC No.>` cho user duyệt.

---

## BƯỚC 8 — XUẤT KẾT QUẢ

1. Viết TC vào `kho-tcs/data/<feature>_s<n>_<tên>.py`, dùng helper `tc(sec, vp, kind, ...)`.
2. Viết bảng mâu thuẫn vào `kho-tcs/data/<feature>_conflicts.py`.
3. Đăng ký feature trong `FEATURES` ở `kho-tcs/build.py`, khai báo:
   `code` · `vi` · `jp` · `prefix` · `sections` · `parts` · `conflicts` · `spec` ·
   `sources` (tab đã gộp + niên đại) · `excluded` (tab đã loại + lý do).
4. Sinh output:
   ```
   python kho-tcs/build.py md      # markdown trong kho-tcs/ để review + diff bằng git
   python kho-tcs/build.py sheet   # đẩy lên Google Sheet (tự áp định dạng chuẩn)
   python kho-tcs/build.py format  # CHỈ đồng bộ định dạng, KHÔNG ghi đè dữ liệu trong tab
   ```

### Định dạng tab — KHÔNG chỉnh tay trên Sheet

Mọi tab tính năng dùng **cùng một định dạng chuẩn, lấy từ tab `FA-012 Quản lý thẻ (タグ管理)`**:
đóng băng **1 dòng đầu + 4 cột đầu** (`ID` · `Nhóm` · `Mã quan điểm` · `Màn hình/chức năng`),
độ rộng cột `[80, 64, 64, 80, 73, 244, 244, 244, 200, 244, 80, 300]` px.

Khai báo ở `TAB_WIDTHS` / `TAB_FROZEN_ROWS` / `TAB_FROZEN_COLS` đầu [build.py](../../kho-tcs/build.py) —
`build.py sheet` và `build.py format` đều tự áp. **Muốn đổi thì sửa hằng số rồi chạy lại
`build.py format`**, không chỉnh tay từng tab trên Google Sheet (chỉnh tay sẽ bị ghi đè ở lần build sau).

### Tên tab — BẮT BUỘC 3 phần

```
<Mã màn hình> <Tên tiếng Việt> (<Tên màn hình tiếng Nhật>)
```

VD user gõ `/collect-tcs tính năng chat 1:1` → tab `FA-001 Chat 1:1 (1:1チャット)`.

- `code` — mã màn hình `FA-0xx`, tra ở [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) §Bảng feature.
- `vi` — **tên tiếng Việt user gõ khi chạy skill** (bỏ chữ "tính năng"). Không tự đổi thành tên khác.
- `jp` — tên màn hình tiếng Nhật, lấy ở cột `Tên JP` cùng bảng feature. **Không có trong bảng →
  hỏi user**, KHÔNG tự dịch.

`build.py` tự ghép 3 phần này; thiếu bất kỳ khoá nào là lỗi dừng build.
Đổi tên tab một feature đã gộp → `to_sheet()` **rename tab cũ theo `code`** (giữ nguyên `gid`,
không xoá tạo lại), nên link cũ và comment của Leader không mất.

### Bố cục sheet đích

| Tab | Nội dung |
|---|---|
| `_README` | quy ước chung của kho |
| `_Nguồn & phạm vi` | nguồn đã gộp / đã loại (kèm lý do) / spec đối chiếu — của **TẤT CẢ** màn hình |
| `_Mâu thuẫn cần quyết` | bảng mâu thuẫn của tất cả màn hình |
| `<code> <vi> (<jp>)` | 1 tab / tính năng — **DÒNG 1 là dòng tiêu đề cột**, TC bắt đầu từ dòng 2 |

⚠️ Tab tính năng **KHÔNG** có khối mô tả (Kho TCs tổng hợp / Nguồn đã gộp / Đã loại / Spec đối chiếu)
phía trên bảng nữa — toàn bộ đã dồn về `_Nguồn & phạm vi`. Bản markdown trong `kho-tcs/` vẫn giữ
các khối này để review và diff bằng git.

**Về Google Sheet đích**: service account **không tạo được file mới** (Google đã bỏ Drive storage
cho service account). Sheet phải do user tạo, share quyền **Editor** cho
`mcp-shhets@snappy-run-490703-k8.iam.gserviceaccount.com`, rồi lưu `spreadsheetId` vào
`kho-tcs/.sheet-id`. Lần đầu chạy có thể tạo file bằng Drive connector của user rồi share.

---

## QUY TẮC BẤT BIẾN

**Không bịa.** Chỉ dùng nội dung có trong tab nguồn + spec-features. Nếu phải suy luận
(VD suy quy tắc chung ra một nhánh Leader chưa nói), **ghi rõ ở `Ghi chú` rằng đây là suy luận
của AI và cần Leader xác nhận** — không trình bày như sự thật.

**Không tự quyết mâu thuẫn.** Cột quyết định để trống. Khi Leader đã chốt, ghi nguyên văn quyết
định vào bảng, cập nhật `Trạng thái` = `✅ ĐÃ CHỐT`, sửa expected của TC liên quan cho khớp, và
liệt kê việc phải sửa spec ở cột `Việc phải làm tiếp`.

**Quyết định của Leader có thể khác TC gốc.** Khi đó viết TC theo **quyết định**, và ghi ở `Ghi chú`
rằng TC gốc nói khác + **dự kiến FAIL → cần raise bug**. Đừng lặng lẽ theo TC gốc.

**Nêu rõ khi quyết định chưa phủ hết.** Nếu quyết định của Leader để hở một nhánh, tạo TC cho nhánh
đó với `Trạng thái đánh giá spec = Đã hỏi leader` và nêu câu hỏi cụ thể trong báo cáo cuối.

**Không tự loại nguồn.** Tab bị loại khỏi phạm vi phải liệt kê ở `excluded` kèm lý do và **hỏi user
xác nhận** trong báo cáo (VD: tab MCP test tầng tool chứ không phải màn admin → nên tách sheet riêng).

**Không kết luận UI từ mô tả.** Không có tool soi giao diện LME. Với TC dựa vào mô tả cũ, ghi rõ
tuổi TC và "CẦN VERIFY LẠI", đừng trình bày như hiện trạng.

---

## BÁO CÁO CUỐI (in ra cho user, KHÔNG ghi vào file)

1. Link Google Sheet.
2. Bảng nguồn đã gộp (file · tab · niên đại) và nguồn đã loại (kèm lý do, hỏi xác nhận).
3. Tổng số TC + bảng coverage theo nhóm chức năng.
4. Số mâu thuẫn theo mức độ; nêu 3–5 mâu thuẫn nặng nhất bằng văn xuôi, mỗi cái nói rõ
   TC nói gì / spec nói gì / vì sao quan trọng.
5. Các gap của spec mà TC lấp được (đề xuất đóng Gap).
6. Câu hỏi còn treo cần user quyết.
7. **DỪNG** — chờ user duyệt rồi mới sang tính năng tiếp theo.
