<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->

# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
>
> **Format bảng TC = 14 cột, giống hệt bảng §7 "TCs đề xuất bổ sung" của `05-review-report.md`** (Leader chốt 2026-10-07). TC member / `/write-tc` viết và TC `/review-tc` đề xuất dùng chung 1 format. Không tự đổi tên cột / thêm cột.
>
> File 04 cũ giữ nguyên format lúc tạo, không convert: **16 cột canonical** (2026-07-16 → 2026-10-06, kể cả snapshot Studio do `scripts/parse_studio_tcs.py` sinh) · **10 cột** (trước 2026-07-16).
>
> **Config sync TC human** (dòng `<!-- sync-tcs: ... -->` ở đầu file): target Google Sheet của `/sync-ai-tc` (push TC AI viết trong file này) và của `/sync-review-tc` **khi đích là Sheet**. Ghi 5 cột `ID, Tên case, Tiền điều kiện, Các bước thực hiện, Kết quả mong đợi` vào sheet TC human, bắt đầu tại cột `anchor` ("Main Function"), append xuống dưới data hiện có.
>
> ⚠️ `/sync-review-tc` **định tuyến theo nguồn TC gốc** ghi ở §0 của `05-review-report.md`: nguồn Studio → push thẳng MCP `testcase_create` (config này KHÔNG dùng tới) · nguồn Sheet → append vào chính Sheet đó · nguồn file 04 → hỏi human.
> - `url` = URL Google Sheet TC human/master · `sheet` = tên tab · `anchor` = cột header canh vị trí (mặc định `Main Function`).
> - **Khác** dòng `<!-- sync-target: ... -->` của `/sync-tc` (push từ cột A + header block vào tab AI pre-create).
> - Sheet human dạng merged-cell (cột anchor chỉ điền ở dòng đầu mỗi block) → **bắt buộc truyền `--row <n>`** khi sync, không dùng auto-detect (sẽ đếm sai và đè data cũ).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<tên>` |
| Ngày submit | `YYYY-MM-DD` |
| Version TCs | `v1 / v2 / ...` (sau mỗi vòng review) |
| Link TC gốc (nếu có) | `<TestRail / Excel / Sheet URL>` |

---

## TC List

> **14 cột.** Mỗi quan điểm ưu tiên **Cao** phải tách đủ **3 test case: Normal + Abnormal + Boundary** (RULE-01).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-XXX000-01 | UI | | `<Tên VN/EN> <Tên JP>: <nội dung>` | Normal | auto | dev, local, prd, staging | | | | | | | `BUG` · Đánh giá spec: Spec ghi rõ · Evidence: `<loại>` |
| TC-XXX000-02 | API | | | Abnormal | auto | dev, local, staging | | | | | | | `F1` · không chạy prd vì `<case ảnh hưởng server>` · Đánh giá spec: Spec ghi rõ · Evidence: `<loại>` |
| TC-XXX000-03 | UI | | | Boundary | auto | dev, local, prd, staging | | | | | | | `T1` · regression · dẫn từ `<ID kho>` · Đánh giá spec: Spec không ghi (đã hỏi `<ai>`) · Evidence: `<loại>` |

### Chú thích cột

**Quy tắc từng cột = mục "Quy tắc cột" §7 của [05-review-report.template.md](05-review-report.template.md)** — nguồn duy nhất, đọc ở đó. Chỉ khác ở `Ghi chú`:

| Cột | Quy tắc tóm tắt |
|---|---|
| **ID** | `TC-<mã quan điểm bỏ dấu gạch>-<nn>`, đánh từ `01` cho **mỗi** quan điểm. VD `MSG-002` → `TC-MSG002-01`; `DATA-COUNT-001` → `TC-DATACOUNT001-01`. |
| **Nhóm** | `UI` / `API` / `Data` / `Job` — theo `GROUP_MAP`, nhưng **cách kiểm chứng thắng** (gửi request trực tiếp → `API`; chỉ thao tác màn hình → không `API`; kiểm job nền → `Job`). |
| **Mã quan điểm** | Mã tầng 1 ([checklist-lme.md](../framework/checklist-lme.md)) mà TC cụ thể hóa. **Bắt buộc** — cột để Leader / `/review-tc` map coverage. |
| **Màn hình/chức năng** | `<Tên VN/EN> <Tên JP>: <nội dung test ngắn gọn>`. VD `Friend list 友だちリスト: Filter friend info 友だち情報 kiểu text テキスト`. |
| **Loại case** | **Chỉ** `Normal` / `Abnormal` / `Boundary`. TC regression xếp `Normal` / `Abnormal` + ghi `regression` ở Ghi chú. |
| **Chạy** | `auto` / `manual` (Studio `exec_mode`), **mặc định `auto`**. `manual` chỉ khi scope chỉ `prd` · thiết bị thật · mail thật · mắt người phán đoán → ghi `manual vì <lý do>`. |
| **Phạm vi ENV** | Env code Studio, 3 tổ hợp: `dev, local, prd, staging` (**mặc định**) · `prd` (tài khoản khách hàng thật) · `dev, local, staging` (abnormal ảnh hưởng server). **RULE-08** → phải chứa `prd`. |
| **Tên case** | Mục đích cụ thể + **keyword** để Leader suy impact (function / DB table / màn hình). Không prefix `[<nhóm>]`. |
| **Tiền điều kiện** | Account, data seed, feature flag, timezone — **đầy đủ**. Mỗi ý 1 dòng `- `, ngăn `<br>`. **TC phải tự đầy đủ**: chép đủ dữ liệu TC dùng (từng bạn ở trạng thái nào…); **cấm** `Như TC-…` / `như NEW-…` / `xem bảng …` — lên test tool từng TC đứng riêng. Bạn bè test viết tắt `F01`, `F02` … (khai báo `システム表示名 <PREFIX>_F01 …`). |
| **Các bước thực hiện** | Mỗi bước 1 dòng, đánh số `1.` `2.`, ngăn `<br>`. |
| **Dữ liệu nhập** | Giá trị cụ thể + **phép tính tay** nếu có số đếm / tỷ lệ. Không "data dummy". |
| **Kết quả mong đợi** | Mỗi kết quả 1 dòng `- `, ngăn `<br>`; **đo lường được**, ghi thẳng số + tập người kèm lý do (`7 bạn — F03 (đã dừng), F04 (đã đọc xong)…`); **cấm** `Đúng bằng TC-…`. **RULE-06** (output cuối chuỗi) + **RULE-07** (DB + màn hình + output); nhóm `API` ghi mã HTTP (**RULE-13**). |
| **Kết quả thực thi** | **Để trống** khi viết draft. |
| **Ghi chú** | Ngăn bằng ` · `: **(1) impact cover** `BUG` / `F<n>` / `D<n>` / `T<n>` (thay `Lấp G/Q/R` của §7) · (2) `regression` + `dẫn từ <ID kho>` · (3) `Đánh giá spec: Spec ghi rõ / Spec không ghi (đã hỏi <ai>) / Đã hỏi leader` · (4) `Evidence: <loại>` (RULE-02) · (5) lý do thiếu loại case (RULE-01) / lý do `manual` / `chỉ prd` / `không chạy prd` / cảnh báo conflict. |

> **RULE-01 — pattern tối thiểu**: quan điểm ưu tiên **Cao** → **≥ 3 TC: Normal + Abnormal + Boundary**. Thiếu 1 trong 3 → **bắt buộc ghi lý do** ở Ghi chú (VD "quan điểm không có khái niệm biên"). Trung bình/Thấp → tối thiểu 1 Normal, khuyến khích thêm Abnormal.
>
> **Không có cột Priority** (ưu tiên suy từ mã quan điểm) · **không có cột Map to Impact** (impact ghi đầu `Ghi chú`). Kết quả chạy, evidence, người chạy, ticket bug ghi trên Studio / Sheet sau khi test, không ghi trong file này.

### Environment (note)

Mặc định chạy **cả 4 env** `dev, local, prd, staging`. Domain tham chiếu:
- `staging` — `staging.lme.jp`
- `dev` — `form.watermeru.com` (test sớm / verify source / reproduce race condition)
- `prd` — `step.lme.jp`. Có trong scope **bắt buộc** với media / domain / job / loadbalance / bill tiền (RULE-08). **Tránh** tạo/xoá data thật; case abnormal có thể ảnh hưởng server → bỏ `prd` khỏi scope (`dev, local, staging`).

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc spec của tính năng (`spec-features/<feature>/feature-spec.md`, hoặc link spec leader đưa trực tiếp)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC** verify tính năng cũ không hỏng cho mỗi tính năng trong 4.3 (ghi "regression" ở Ghi chú)
- [ ] Có **ít nhất 1 Abnormal + 1 Boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC có `Mã quan điểm`, steps rõ ràng, `Kết quả mong đợi` đo lường được
- [ ] `Tên case` chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base quan điểm test LME (2 tầng)

**Tầng 1 — quan điểm**: [framework/checklist-lme.md](../framework/checklist-lme.md) (80 quan điểm + 13 RULE).
**Tầng 2 — catalog**: [framework/catalog-lme.md](../framework/catalog-lme.md).

Điền bảng quan điểm đã duyệt cho task này (◯ = áp dụng / × = không, **× bắt buộc ghi lý do** — RULE-03):

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã tra | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| | | | | | |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2 và **duyệt hết** khối tương ứng (Catalog C không lấy 1-2 dòng đại diện)
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Normal + Abnormal + Boundary (**RULE-01**), thiếu thì đã ghi lý do ở Ghi chú
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài (LINE app / mobile app / Google / gateway / file / mail) → `Kết quả mong đợi` đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output; có TC kiểm `WHERE` scope trên 2 tài khoản nếu task có UPDATE/DELETE (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → TC liên quan có `Phạm vi ENV` **chứa `prd`** (**RULE-08**)
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**)
- [ ] Mọi TC có `Đánh giá spec: ...` ở Ghi chú; case `Spec không ghi` đã ghi rõ **đã hỏi ai**
