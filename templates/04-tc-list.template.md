<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->

# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
>
> **Format bảng TC bám đúng sheet canonical "7. Ví dụ test case"** của [Bảng quan điểm test — HỢP NHẤT ELME v1.0](https://docs.google.com/spreadsheets/d/1IijLnq0gLZDFxOMWOYxXafz1Wnzv3W0g/edit?gid=1251796928#gid=1251796928). Không tự đổi tên cột / thêm cột.
>
> **Config sync TC human** (dòng `<!-- sync-tcs: ... -->` ở đầu file): target Google Sheet của `/sync-ai-tc` (push TC AI viết trong file này) và của `/sync-review-tc` **khi đích là Sheet**. Ghi 5 cột `TC No., Tiêu đề test case, Điều kiện tiền đề, Các bước thực hiện, Kết quả mong đợi` vào sheet TC human, bắt đầu tại cột `anchor` ("Main Function"), append xuống dưới data hiện có.
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

> **16 cột canonical.** Mỗi quan điểm ưu tiên **Cao** phải tách đủ **3 test case: Normal + Abnormal + Boundary** (RULE-01) — xem ví dụ mẫu ở sheet "7. Ví dụ test case".

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-XXX000-01 | | Normal | | | | | | Chưa test | | STAGING | | | | Spec ghi rõ | |
| TC-XXX000-02 | | Abnormal | | | | | | Chưa test | | STAGING | | | | | |
| TC-XXX000-03 | | Boundary | | | | | | Chưa test | | STAGING | | | | | |

### Chú thích cột

| Cột | Quy tắc |
|---|---|
| **TC No.** | `TC-<mã quan điểm bỏ dấu gạch>-<số thứ tự 2 chữ số>`, đánh lại từ `01` cho **mỗi** quan điểm. VD: `MSG-002` → `TC-MSG002-01`; `DATA-COUNT-001` → `TC-DATACOUNT001-01`; `PERM-001` → `TC-PERM001-03`. |
| **Mã quan điểm liên kết** | Mã ở tầng 1 ([checklist-lme.md](../framework/checklist-lme.md)) mà TC này cụ thể hóa. VD `PERM-002`. **Bắt buộc** — đây là cột để Leader/`/review-tc` map coverage. |
| **Loại case** | **CHỈ 3 giá trị**: `Normal` / `Abnormal` / `Boundary`. Không có loại nào khác. TC regression xếp vào `Normal` (luồng cũ vẫn chạy đúng) hoặc `Abnormal` (điều kiện lỗi cũ), ghi rõ "regression" ở **Ghi chú**. |
| **Tiêu đề test case** | Mô tả MỤC ĐÍCH cụ thể + chứa **keyword** giúp Leader suy luận impact (tên function / DB table / màn hình). VD: `generateLinkInviteStaff: bot standard 10/10 → fail`. |
| **Điều kiện tiền đề** | Account, data seed, feature flag, timezone — **đầy đủ**, người khác đọc dựng được env. Mỗi ý 1 dòng, bắt đầu bằng `- `. |
| **Các bước thực hiện** | Tuần tự, đánh số `1.` `2.` `3.`. Dùng `<br>` để xuống dòng trong bảng markdown. |
| **Dữ liệu test/input** | Giá trị input cụ thể + **phép tính tay** nếu TC có số đếm/tỷ lệ. VD: `5 friend, 3 người mở` / `Phép tính tay: 3/5 = 60%`. Không để "data dummy". |
| **Kết quả mong đợi** | **Đo lường được** — giá trị cụ thể, không "hiển thị đúng". Áp dụng **RULE-06** (đi tới output cuối chuỗi: LINE app / mobile app / Google / gateway / file / mail) + **RULE-07** (khớp DB + màn hình + output). |
| **Kết quả thực thi** | **CHỈ 3 giá trị**: `Đạt` / `Không đạt` / `Chưa test`. Draft luôn để `Chưa test`. |
| **Evidence thực tế** | **Để trống khi viết draft.** QA paste link/ảnh sau khi test — **BẮT BUỘC khi Đạt** (RULE-02). *Loại* evidence bắt buộc ghi ở **Ghi chú**. |
| **Môi trường test** | `STAGING` (mặc định) / `DEV` / `PRODUCTION`. **RULE-08**: media · domain · job · loadbalance · bill tiền → **không** kết luận từ staging, phải ghi `PRODUCTION`. |
| **Người thực hiện** / **Ngày thực hiện** | Để trống khi viết draft. QA fill sau khi run. |
| **Số ticket bug** | Để trống. Fill khi `Không đạt` → số ticket Redmine đã raise. |
| **Trạng thái đánh giá spec** | **CHỈ 3 giá trị**: `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Spec không định nghĩa hành vi → chọn `Spec không ghi` + ghi rõ **đã hỏi ai** ở Ghi chú. **Không tự suy diễn rồi cho Đạt.** |
| **Ghi chú** | Loại evidence bắt buộc (RULE-02) · lý do nếu quan điểm Cao thiếu 1 trong 3 loại case (RULE-01) · cảnh báo escalate · liên kết quan điểm khác · đánh dấu "regression". |

> **RULE-01 — pattern tối thiểu**: quan điểm ưu tiên **Cao** → **≥ 3 TC: Normal + Abnormal + Boundary**. Thiếu 1 trong 3 → **bắt buộc ghi lý do** ở Ghi chú (VD "quan điểm không có khái niệm biên"). Trung bình/Thấp → tối thiểu 1 Normal, khuyến khích thêm Abnormal.
>
> **Không có cột Priority** — độ ưu tiên suy ra từ **ưu tiên của mã quan điểm** ở tầng 1.

### Environment (note)

Mặc định **STAGING** (`staging.lme.jp`). Trường hợp đặc biệt:
- `DEV` (`form.watermeru.com`) — test sớm / verify source / reproduce race condition
- `PRODUCTION` (`step.lme.jp`) — smoke sau deploy; **bắt buộc** với media / domain / job / loadbalance / bill tiền (RULE-08). **Tránh** tạo/xoá data thật.

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
- [ ] Mọi TC có `Mã quan điểm liên kết`, steps rõ ràng, `Kết quả mong đợi` đo lường được
- [ ] `Tiêu đề test case` chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base quan điểm test LME (2 tầng)

**Tầng 1 — quan điểm**: [framework/checklist-lme.md](../framework/checklist-lme.md) (80 quan điểm + 12 RULE).
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
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC ghi `Môi trường test = PRODUCTION` (**RULE-08**)
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**)
- [ ] Mọi TC có `Trạng thái đánh giá spec`; case `Spec không ghi` đã ghi rõ **đã hỏi ai**
