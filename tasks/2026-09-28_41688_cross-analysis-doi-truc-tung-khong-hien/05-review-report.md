# 05 — Review Report

> Draft cho Leader verify — `/review-tc` 2026-09-28, round 1. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) MCP LME TEST STUDIO — task #334 (ticket 41688, round 1, branch `ai_fixbug_41688`) |
| Tổng số TC review | 20 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `BUG` + F1–F4 + D1–D2 + T1–T4 (11 mục) | 10/11 mục có TC — **CHƯA ĐỦ** (1 GAP · 1 RISK) |
| **(b) diff code** — 2 file `spec_delta` + 6 điểm `dev_impact` Studio (8 điểm) + 2 điểm adversarial | 8/8 điểm Studio có TC nhưng 2 RISK; 2 điểm adversarial Dev/Studio chưa kê — **CHƯA ĐỦ** |

**Kết luận**: nội dung 16/21 vùng có TC đủ chiều · 2 GAP · 3 RISK. ⚠️ **0/20 TC đã chạy** → chưa vùng nào đạt `OK` thật (xem I1).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F3 — `getDataCrossReset()` (đọc dữ liệu đã lưu, Dev kê ở 4.1) | `dev-impact` | không có | GAP — 3/4 hàm đọc của F3 có TC (`initDataCross` NEW-7 · `copyCross` NEW-1 · `initAnalysis` NEW-20), riêng `getDataCrossReset` không TC nào nêu thao tác đi qua | `[MAJOR]` |
| G2 | D1 — `line_ids_parent` lưu `[]`: nơi đọc **export CSV** (`exportCsv` EP-23) | `dev-impact` + `diff code` (câu hỏi 3) | NEW-20 (chỉ 分析リスト + drill-down) | GAP — danh sách "không đọc `line_ids_parent`" của Dev chỉ có `initDataCross` / `resultCrossAnalysis` / command, **không có `exportCsv`**; màn có export CSV (cột 対象人数 — xem task #38674) mà 0 TC export sau fix | `[MAJOR]` |
| G3 | FE nhánh `.fail` của `saveCross()` — hiện alert khi lưu thất bại | `diff code` (câu hỏi 2) | NEW-9 | RISK — **generic-fix chỉ test 1 trigger** (400 do thiếu `filter_by`). Thiếu phiên/CSRF hết hạn, mất mạng, 500 / lỗi chưa biết → fallback message + tắt overlay | `[BLOCKER]` |
| G4 | Hành vi đổi `line_ids_parent`: bản ghi **cũ** (còn ID) vs bản ghi mới (`[]`) | `diff code` (câu hỏi 4) | NEW-20 | RISK — biến thể bản ghi cũ trong NEW-20 là **tùy chọn** ("ghi rõ khi không có dữ liệu cũ") → có thể skip; không TC nào bắt buộc sửa-lưu lại cross cũ rồi so số liệu | `[MAJOR]` |
| G5 | Root cause thứ 2 hợp lý: trục tung trỏ tới **friend info / tag đã xóa** (chẩn đoán ban đầu của support, Journal #139044) | `diff code` (AP-2 symptom-only) | không có (NEW-10 chỉ dựng dữ liệu hỏng kiểu `filter_friend_info_id=0`) | RISK — ticket báo triệu chứng "danh sách không hiển thị", có 2 nguyên nhân hợp lý mà TC chỉ phủ 1 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 24 quan điểm Trigger khớp task · 10 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-DB-001` | Cao | GAP phần `WHERE` — task có UPDATE nhưng không TC nào lưu `cross_analysis` của bot khác từ phiên bot A (RULE-07 · RULE-13 403/404). NEW-15 chỉ kiểm từ chối trên chính bot | `[BLOCKER]` |
| Q2 | `OUT-EXPORT-001` | Trung bình → nâng Cao | GAP — 0 TC export CSV cross analysis sau fix (trùng G2) | `[BLOCKER]` |
| Q3 | `FUNC-002` | Cao | RISK — nội dung validate form đã có ở NEW-11 nhưng mang mã lạ `TOOL-VAL2-001` → không tính cover. **Chỉ cần đổi mã NEW-11 sang `FUNC-002`**, không đẻ TC | `[MAJOR]` |
| Q4 | `DATA-COUNT-001` | Cao | RISK — số 対象人数 / ô bảng chỉ được phủ bởi NEW-20 (mã lạ) + NEW-7, cả 2 là Normal; thiếu Boundary (parent filter khớp 0 friend sau khi bỏ `line_user_ids`) — RULE-01 | `[MAJOR]` |
| Q5 | `DATA-REF-001` | Cao | RISK — nhánh copy có NEW-1; thiếu nhánh **xóa đối tượng được tham chiếu** (tag / friend info đang làm trục tung) — trùng G5 | `[MAJOR]` |
| Q6 | `UI-003` | Trung bình → Cao (rủi ro false success) | RISK — NEW-9 tự ghi nhận FE cập nhật lạc quan 条件保存日時 + tắt cảnh báo rời trang **trước** khi có kết quả máy chủ (edit.js:474-486), nhưng expected bắt tester reload rồi mới phán → không TC nào kiểm màn hình **trước reload** sau khi lưu thất bại | `[MAJOR]` |
| Q7 | `ENV-003` | Cao | RISK — root cause phụ thuộc cấu hình PHP `max_input_vars` của từng env + quy mô bot (~68,000 friend) + job phân tích; 0 TC ghim `product` (RULE-08) | `[MAJOR]` |
| Q8 | `DEPLOY-LIVE-001` | Cao | RISK — release đổi payload request. NEW-19 phủ payload bản cũ **vượt ngưỡng**; thiếu case tab còn giữ JS cũ gửi payload **nhỏ** (có `line_user_ids` + `filter_by` hợp lệ) → BE mới phải bỏ qua `line_user_ids` và lưu đúng | `[MAJOR]` |
| Q9 | `DATA-BACKUP-001` | Cao | RISK — `cross_analysis` nằm trong phạm vi データコピー (FA-033, bảng #34) và fix đổi dữ liệu ghi (`line_ids_parent = []`); bộ TC không có TC copy bot. **Dùng lại kho** TC-BK-282 / 283 / 284 / 293, không viết mới (xem §7) | `[MAJOR]` |
| Q10 | `COMPAT-LEGACY-001` | Cao | RISK — bản ghi cũ vs mới của `line_ids_parent` (RULE-09) — trùng G4 | `[MAJOR]` |

Đã xét và loại khỏi phạm vi (không đề xuất TC):
- `SYNC-APP-001` — không có bằng chứng クロス分析 có mặt trên app quản trị di động (spec-features/admin/index.md chỉ ghi route web `/basic/cross-analysis`).
- `PAY-LIMIT-001` — fix không chạm kiểm tra hạn mức gói; quirk copy dùng hạn mức 2 đã được NEW-1 ghi chú.
- `FUNC-DATE-001` · `CONC-001` · `REG-RUN-001` · `PERM-001/002` — logic ngày, đồng thời, job đang chạy, phân quyền không nằm trong 2 file bị sửa.
- `JOB-001` — job `HandelCrossAnalysis*` không bị sửa; đường đọc của job đã được NEW-2/3/5/20 đi qua (chờ job tính xong).

---

## 3. TC trùng lặp nội dung

Đã rà 20 TC, **không phát hiện trùng lặp**.

- Các cặp chồng lấn đã xét và **giữ nguyên** vì khác trọng tâm: NEW-13 vs NEW-17 (phần giá trị hợp lệ 1/2/3 — NEW-13 kiểm hợp đồng phản hồi, NEW-17 kiểm biên) · NEW-15 vs NEW-17 (NEW-15 kiểm toàn bộ cột + số bản ghi `filters_v2` không đổi, NEW-17 kiểm biên giá trị) · NEW-6 vs NEW-8 bước 5 (NEW-8 trọng tâm cache JS).
- **Gate**: không đề nghị xóa TC nào → coverage §1 / §2 giữ nguyên.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-15 · NEW-16 · NEW-17 (và `dev_impact` Studio) | Mã HTTP khi `filter_by` là số **ngoài tập** {1,2,3} (0, -1, 4, 9) | `dev_impact`: "filter_by không hợp lệ → trả HTTP 400" cho mọi trường hợp | `checklist-lme.md` mục 1.1 RULE-13: thiếu tham số / sai format = **400**; đúng cấu trúc nhưng **enum ngoài danh sách = 422** | Code / TC theo 400 là lệch quy ước · hoặc quy ước cần ngoại lệ cho endpoint này | `[MAJOR]` | Dev / Leader |

**Đã rà**: 20 TC × `framework/checklist-lme.md` §1.1 + `kho-tcs/fa033-backup-データコピー.md` (nhóm "Copy クロス分析", TC-BK-279 → 294) — không phát hiện `CONF-TC` / `CONF-KHO`. ⚠️ **Không có spec** `spec-features/` cho FA-024 và **kho-tcs chưa có FA-024** → không đối chiếu được Business rule, không ghi là "đã rà sạch" cho phần spec.

Ghi chú: NEW-14 tự nêu "đặc tả tính năng (lỗi nghiệp vụ trả 200 kèm cờ thất bại)" — đó là spec nội bộ của Studio, không có trong repo; chuẩn dùng cho review là RULE-13.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 20 TC | 0/20 TC đã chạy (pass 0%) — bộ TC chưa có kết luận test nào | Chạy bộ TC trên Studio trước khi Leader duyệt; ưu tiên NEW-3 · NEW-6 · NEW-9 · NEW-15 · NEW-19 (đi thẳng root cause + cách fix) |
| I2 | `[BLOCKER]` | [AP-1] NEW-9 | Fix FE "hiện message lỗi khi lưu thất bại" là generic catch nhưng chỉ test 1 trigger | Xem G3 — thêm 3 TC trigger khác nhau + fallback lỗi chưa biết |
| I3 | `[MAJOR]` | Spec FA-024 | Không có `spec-features/` cho クロス分析 (index ghi CHƯA) → không có chuẩn để đánh giá Expected; mọi expected hiện dựa vào `dev_impact` + requirement Studio | Leader chốt nguồn spec; bổ sung spec FA-024 (xem §8) |
| I4 | `[MAJOR]` | Toàn bộ (RULE-08) | Task có job phân tích + root cause phụ thuộc cấu hình server/quy mô bot, nhưng 0 TC ghim chạy `product` | Xem Q7 |
| I5 | `[MAJOR]` | NEW-15 · NEW-16 · NEW-17 | RULE-13 — expected nhánh bị từ chối **không ghi mã HTTP** (chỉ ghi thông báo / "không lỗi máy chủ") | Bổ sung mã HTTP cụ thể theo kết quả chốt ở C1 |
| I6 | `[MAJOR]` | NEW-9 | Expected bắt "BẮT BUỘC tải lại trang trước khi phán quyết" → né đúng trạng thái màn hình ngay sau khi lưu thất bại, là chỗ FE cập nhật lạc quan 条件保存日時 | Giữ bước reload để kiểm dữ liệu, thêm expected **trước reload**; hoặc tách sang TC của Q6 |
| I7 | `[MAJOR]` | [AP-2] ticket | Ticket là symptom-only, support và Dev chẩn đoán 2 nguyên nhân khác nhau; TC chỉ phủ nguyên nhân của Dev | Xem G5 — hỏi Dev hành vi mong đợi khi trục tung trỏ tới đối tượng đã xóa |
| I8 | `[MINOR]` | NEW-12 | Expected chấp nhận cả (a) lưu thành công và (b) lưu thất bại → gần như không fail được trừ trường hợp mất tiêu chí im lặng | Chốt với Dev ngưỡng kỳ vọng (số giá trị trường friend info mà màn phải lưu được) |
| I9 | `[MINOR]` | NEW-19 · NEW-12 · NEW-17 | Mã quan điểm lệch nội dung: NEW-19 gắn `ENV-001` (validate đa server) nhưng thực chất là payload bản cũ → `DEPLOY-LIVE-001`; NEW-12 gắn `ENV-003` nhưng là dữ liệu lớn → `PERF-LARGE-001`; NEW-17 gắn `FUNC-004` (giới hạn số lượng) nhưng là biên enum | Đổi mã để coverage theo quan điểm phản ánh đúng |
| I10 | `[NIT]` | NEW-21 | `env_scope = local` nhưng bước kiểm "sau triển khai bảng cấu hình không đổi" có ý nghĩa ở staging/production; phần "không có migration" đã thấy ngay ở `spec_delta` (2 file) | Cân nhắc chạy bước so bảng trước/sau deploy ở staging |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 20 TC — **không có TC nào ngoài phạm vi task**.

- NEW-12 (tham số `friend_info_sorted` nằm ngoài 2 file bị sửa) — giữ: cùng lớp lỗi với root cause (mảng lớn trong payload lưu), dẫn được từ REQ-010.
- NEW-16 (log cảnh báo) — giữ: dẫn từ REQ-012 / commit `bf12f8350b`.

---

## 7. TCs đề xuất bổ sung (13)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs chưa có FA-024 — không đối chiếu được`; đã đọc `kho-tcs/fa033-backup-データコピー.md` nhóm "Copy クロス分析" |
| Vùng regression phát hiện từ kho | FA-033 — copy bot mang `cross_analysis` sang bot nhận (TC-BK-279 → 294) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | **Q9 → TC-BK-282** "Copy mục phân tích theo THẺ", **TC-BK-283** "…theo THÔNG TIN BẠN BÈ", **TC-BK-284** "…theo NGÀY KẾT BẠN", **TC-BK-293** "Mục phân tích đã copy được job chạy lại theo dữ liệu bot nhận". Cần chỉnh: mục phân tích ở bot A phải **tạo/lưu trên bản fix** (`line_ids_parent` rỗng) để kiểm dữ liệu mới đi qua copy bot |
| Căn cứ TC regression `R<x>` | Không có TC R — rủi ro hồi quy của Studio đã được bộ TC phủ; vùng kho đã xử lý bằng dùng lại (Q9) |
| Xác nhận chống trùng | Đã đối chiếu 20 TC ở BƯỚC 0 + kho FA-033 — **không TC đề xuất nào trùng**. Q3 xử lý bằng đổi mã NEW-11, không đẻ TC |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-OUTTRUTH001-01 | UI | OUT-TRUTH-001 | クロス分析 — Lưu cấu hình (lỗi phiên) | Abnormal | auto | Tất cả | Lưu cấu hình khi phiên đăng nhập hoặc mã chống giả mạo biểu mẫu đã hết hạn thì màn hình báo lỗi, không coi là đã lưu | Đăng nhập admin, chọn bot test. Có danh sách phân tích TC41688_sess_timestamp đã lưu với trục tung 「タグ」 + 2 tag; ghi lại cấu hình và 条件保存日時 hiện tại | 1. Mở màn chỉnh sửa của TC41688_sess_timestamp<br>2. Ở tab trình duyệt khác, đăng xuất khỏi admin (hoặc xóa cookie phiên) rồi quay lại tab đang mở<br>3. Đổi tiêu chí: bỏ bớt 1 tag, bấm 「選択した内容で基準軸を登録」<br>4. Bấm 「この内容で分析リストを作成・更新」<br>5. Ghi lại thông báo, trạng thái lớp chờ, địa chỉ trang, 条件保存日時 đang hiển thị<br>6. Đăng nhập lại, mở màn chỉnh sửa và 分析リスト của danh sách | Danh sách TC41688_sess_timestamp · trục 「タグ」 2 tag → bỏ 1 tag · phiên đã hết hạn | Màn hình hiện thông báo lỗi (không im lặng), lớp chờ tắt, không hiện 「保存しました」, không điều hướng, 条件保存日時 không đổi. Sau khi đăng nhập lại, cấu hình vẫn là 「タグ」 với đủ 2 tag, 分析リスト hiển thị như trước |  | Lấp G3 · trigger 1/3 của generic-fix FE · Đánh giá spec: Spec không ghi — nội dung thông báo khi máy chủ không trả message cần Dev xác nhận · Evidence: ảnh màn hình thông báo + HAR request/response |
| TC-OUTTRUTH001-02 | UI | OUT-TRUTH-001 | クロス分析 — Lưu cấu hình (mất mạng) | Abnormal | auto | Tất cả | Lưu cấu hình khi mất kết nối mạng thì màn hình báo lỗi và không kẹt lớp chờ | Đăng nhập admin, chọn bot test. Có danh sách TC41688_net_timestamp đã lưu với trục 「友だち情報」; ghi lại cấu hình và 条件保存日時 | 1. Mở màn chỉnh sửa của TC41688_net_timestamp<br>2. Đổi trục tung sang 「タグ」, chọn 2 tag, bấm 「選択した内容で基準軸を登録」<br>3. Chuyển trình duyệt sang chế độ ngoại tuyến (DevTools → Network → Offline)<br>4. Bấm 「保存・更新」<br>5. Ghi lại thông báo, trạng thái lớp chờ, 条件保存日時<br>6. Bật lại mạng, tải lại màn chỉnh sửa, kiểm cấu hình và 分析リスト | Danh sách TC41688_net_timestamp · trục cũ 「友だち情報」 → trục mới 「タグ」 · mạng Offline | Màn hình hiện thông báo lỗi, lớp chờ tắt trong thời gian hợp lý, không điều hướng, không báo thành công. Sau khi có mạng và tải lại, cấu hình vẫn là trục 「友だち情報」 cũ, 分析リスト không đổi |  | Lấp G3 · trigger 2/3 · Đánh giá spec: Spec không ghi · Evidence: ảnh màn hình + console |
| TC-OUTTRUTH001-03 | UI | OUT-TRUTH-001 | クロス分析 — Lưu cấu hình (lỗi máy chủ chưa biết) | Abnormal | auto | Tất cả | Máy chủ trả lỗi 500 không có nội dung thông báo thì màn hình vẫn hiện thông báo lỗi dự phòng | Đăng nhập admin, chọn bot test. Có danh sách TC41688_500_timestamp đã lưu với trục 「友だち登録日」; bật công cụ ghi đè phản hồi của trình duyệt (DevTools Local overrides hoặc proxy) cho request lưu cấu hình | 1. Mở màn chỉnh sửa của TC41688_500_timestamp<br>2. Đặt quy tắc: request lưu cấu hình phân tích trả mã 500 với thân rỗng<br>3. Đổi khoảng ngày của trục tung, bấm 「選択した内容で基準軸を登録」<br>4. Bấm nút 「分析リスト」 trong vùng bảng<br>5. Ghi lại thông báo, lớp chờ, địa chỉ trang<br>6. Tắt quy tắc, tải lại màn chỉnh sửa | Danh sách TC41688_500_timestamp · phản hồi 500 thân rỗng | Màn hình hiện thông báo lỗi dự phòng (không để trống, không hiện chữ undefined), lớp chờ tắt, không điều hướng sang 分析リスト, không báo thành công. Sau khi tải lại, cấu hình cũ giữ nguyên |  | Lấp G3 · trigger 3/3 = lỗi chưa biết (fallback) · Đánh giá spec: Spec không ghi — hỏi Dev nội dung thông báo dự phòng · Evidence: ảnh màn hình + HAR |
| TC-OUTEXPORT001-01 | UI | OUT-EXPORT-001 | クロス分析 — Xuất CSV 分析リスト | Normal | auto | Tất cả | Xuất CSV của danh sách phân tích tạo sau bản fix cho cả 3 loại trục tung, số liệu khớp màn 分析リスト | Đăng nhập admin, chọn bot test có parent filter P khớp số friend biết trước. Tạo và lưu trên bản fix 3 danh sách: TC41688_csv_tag (trục 「タグ」), TC41688_csv_finfo (trục 「友だち情報」), TC41688_csv_date (trục 「友だち登録日」), mỗi danh sách có parent filter P và 1 mục phân tích; job đã tính xong | 1. Mở 分析リスト của TC41688_csv_tag, ghi lại 対象人数 và toàn bộ bảng<br>2. Dùng chức năng xuất CSV trên màn này, tải file về<br>3. Đối chiếu cột 対象人数 và từng ô của file với màn hình<br>4. Lặp lại bước 1–3 cho TC41688_csv_finfo và TC41688_csv_date | 3 danh sách, mỗi loại trục 1 danh sách · parent filter P | Cả 3 file tải về được; 対象人数 trong file bằng số friend của P và bằng số trên màn hình; nhãn trục tung và mọi ô khớp màn hình (ô 0 hiện 0, không trống) |  | Lấp G2 + Q2 · export đọc dữ liệu có line_ids_parent rỗng — Dev chưa liệt kê exportCsv (EP-23) trong danh sách đã xác nhận · RULE-01: không đề xuất Abnormal/Boundary vì fix không chạm lớp export, chỉ đổi dữ liệu đầu vào · Đánh giá spec: Spec không ghi · Evidence: file CSV + ảnh 分析リスト |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | クロス分析 — Màn chỉnh sửa (reset dữ liệu) | Normal | auto | Tất cả | Thao tác reset dữ liệu trên màn chỉnh sửa trả về đúng trục tung và tiêu chí đã lưu | Đăng nhập admin, chọn bot test. Có danh sách TC41688_reset_timestamp đã lưu trên bản fix với trục 「タグ」 + 2 tag và parent filter P. Dev đã xác nhận thao tác nào trên UI gọi getDataCrossReset | 1. Mở màn chỉnh sửa của TC41688_reset_timestamp<br>2. Đổi trục tung sang 「友だち情報」, chọn 1 trường nhưng CHƯA lưu<br>3. Thực hiện thao tác reset dữ liệu (thao tác gọi getDataCrossReset do Dev xác nhận)<br>4. Ghi lại trục tung, tag, số người thuộc bộ lọc đang hiển thị<br>5. Tải lại trang và so sánh | Danh sách TC41688_reset_timestamp · trục đã lưu 「タグ」 2 tag | Sau thao tác reset, màn hiển thị lại đúng trục 「タグ」 với đủ 2 tag và đúng số người thuộc parent filter P (tính lại, không phụ thuộc line_ids_parent rỗng); không hiện nhầm 「友だち情報」, không lỗi |  | Lấp G1 · F3 getDataCrossReset · Input thiếu: tên nút/thao tác UI gọi hàm này — hỏi Dev trước khi chạy · Đánh giá spec: Spec không ghi · Evidence: ảnh màn trước/sau reset |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | クロス分析 — Bản ghi cũ trước fix | Normal | auto | Tất cả | Danh sách phân tích lưu trước bản fix (còn danh sách LINE user) vẫn cho số liệu đúng sau khi sửa và lưu lại trên bản fix | Môi trường có danh sách phân tích đã lưu TRƯỚC khi deploy bản fix, trục 「タグ」 hoặc 「友だち登録日」, đang hiển thị 分析リスト có dòng (bản ghi cũ còn line_ids_parent có ID). Ghi lại 対象人数 và bảng trước khi deploy | 1. Sau deploy, mở 分析リスト của danh sách cũ, làm mới kết quả, chờ job xong, so với số đã ghi<br>2. Mở màn chỉnh sửa, không đổi gì, bấm 「保存・更新」<br>3. Mở lại 分析リスト, chờ job xong, so 対象人数 và từng ô<br>4. Mở một ô có giá trị lớn hơn 0 để xem danh sách friend | 1 danh sách cũ lưu trước deploy · số liệu ghi trước deploy | Trước và sau khi lưu lại trên bản fix, 対象人数, nhãn trục và từng ô không đổi (dữ liệu friend không đổi); drill-down ra đúng số friend của ô; trục tung không bị nhảy về 「友だち情報」 |  | Lấp G4 + Q10 · RULE-09 cũ & mới song song · hành vi đổi: line_ids_parent từ có ID → rỗng · Đánh giá spec: Spec không ghi · Evidence: ảnh 分析リスト trước/sau |
| TC-DATAREF001-01 | UI | DATA-REF-001 | クロス分析 — Trục tung trỏ tới friend info đã xóa | Abnormal | auto | Tất cả | Xóa trường friend info đang làm trục tung thì danh sách phân tích báo rõ trạng thái và sửa lại được bằng cách chọn lại tiêu chí | Đăng nhập admin, chọn bot test. Tạo trường friend info TC41688_fi_del có giá trị ở ≥3 friend; tạo và lưu danh sách TC41688_ref_fi với trục 「友だち情報」 = TC41688_fi_del, 分析リスト đã có dòng | 1. Vào màn quản lý 友だち情報, xóa trường TC41688_fi_del<br>2. Mở 分析リスト của TC41688_ref_fi, làm mới kết quả<br>3. Mở màn chỉnh sửa của TC41688_ref_fi, ghi lại trục tung và thông báo hiển thị<br>4. Chọn lại trục 「タグ」 với 2 tag có friend, bấm 「選択した内容で基準軸を登録」 rồi 「保存・更新」<br>5. Mở lại 分析リスト | Trường TC41688_fi_del · danh sách TC41688_ref_fi | Bước 2–3: không lỗi máy chủ, không trang trắng; màn cho người dùng biết tiêu chí trục tung không còn tồn tại (hành vi cụ thể cần Leader chốt). Bước 4–5: lưu thành công, 分析リスト hiển thị bảng có dòng theo 2 tag |  | Lấp G5 + Q5 · root cause thứ 2 theo chẩn đoán support (Journal #139044) · Đánh giá spec: Spec không ghi — hỏi Leader hiển thị mong đợi · Evidence: ảnh màn chỉnh sửa + 分析リスト |
| TC-DATAREF001-02 | UI | DATA-REF-001 | クロス分析 — Trục tung trỏ tới tag đã xóa | Abnormal | auto | Tất cả | Xóa 1 trong các tag đang làm trục tung thì danh sách phân tích vẫn hiển thị theo tag còn lại, không rỗng toàn bộ | Đăng nhập admin, chọn bot test. Tạo 2 tag TC41688_tagA, TC41688_tagB đều có friend; tạo và lưu danh sách TC41688_ref_tag với trục 「タグ」 = 2 tag trên, 分析リスト đã có dòng | 1. Vào màn タグ管理, xóa TC41688_tagA<br>2. Mở 分析リスト của TC41688_ref_tag, làm mới kết quả, ghi lại nhãn và số liệu<br>3. Mở màn chỉnh sửa, ghi lại tag đang hiển thị ở trục tung<br>4. Bấm 「保存・更新」 không đổi gì, mở lại 分析リスト | Tag TC41688_tagA (bị xóa), TC41688_tagB · danh sách TC41688_ref_tag | Không lỗi máy chủ; 分析リスト vẫn hiển thị dòng của TC41688_tagB với số liệu đúng; tag đã xóa không làm cả bảng thành rỗng; lưu lại thành công và trục vẫn là 「タグ」 |  | Lấp G5 + Q5 · biến thể tag của root cause thứ 2 · Đánh giá spec: Spec không ghi — hỏi Leader cách hiển thị tag đã xóa · Evidence: ảnh 分析リスト trước/sau |
| TC-DATADB001-01 | API | DATA-DB-001 | クロス分析 — Lưu cấu hình (EP-16) | Abnormal | auto | Tất cả | Gửi request lưu cấu hình với mã danh sách phân tích của bot khác thì bị từ chối và dữ liệu bot kia không đổi | Có 2 bot A, B cùng tài khoản admin. Bot B có danh sách TC41688_bot_b trục 「タグ」 2 tag, ghi lại toàn bộ cấu hình và 条件保存日時. Đăng nhập admin, đang chọn bot A, có cookie phiên và mã chống giả mạo biểu mẫu | 1. Gửi POST /basic/saveCrossAnalysis từ phiên bot A với mã danh sách = id của TC41688_bot_b, trục tung = 3, khoảng ngày hợp lệ, tên mới<br>2. Ghi lại mã HTTP và nội dung phản hồi<br>3. Chuyển sang bot B, mở màn chỉnh sửa và 分析リスト của TC41688_bot_b | id của TC41688_bot_b · filter_by = 3 · tên mới TC41688_hijack | Phản hồi HTTP 403 hoặc 404; TC41688_bot_b ở bot B giữ nguyên trục 「タグ」, 2 tag, tên cũ, 条件保存日時 cũ; không có danh sách mới nào xuất hiện ở bot A |  | Lấp Q1 · RULE-07 kiểm WHERE trên 2 bot · RULE-13 cross-bot = 403/404 · Đánh giá spec: Spec không ghi · Evidence: request/response + ảnh cấu hình bot B |
| TC-DATACOUNT001-01 | UI | DATA-COUNT-001 | クロス分析 — 分析リスト số liệu | Boundary | auto | Tất cả | Parent filter khớp 0 friend thì danh sách phân tích lưu được và mọi con số bằng 0 | Đăng nhập admin, chọn bot test. Có tag TC41688_empty chưa gắn cho friend nào | 1. Tạo danh sách TC41688_zero, trục 「タグ」 chọn 2 tag có friend<br>2. Đặt parent filter = có tag TC41688_empty (khớp 0 friend), thêm 1 mục phân tích<br>3. Bấm 「保存・更新」<br>4. Mở 分析リスト, chờ job xong, ghi lại 対象人数 và bảng<br>5. Mở lại màn chỉnh sửa, ghi số người thuộc bộ lọc | Tag TC41688_empty (0 friend) · 2 tag trục có friend | Lưu thành công; 対象人数 = 0, mọi ô = 0 (hiển thị 0, không trống, không lỗi); màn chỉnh sửa hiện số người thuộc bộ lọc = 0; trục tung vẫn là 「タグ」 |  | Lấp Q4 · RULE-01 bổ sung Boundary cho DATA-COUNT-001 · Abnormal không áp dụng vì đếm không có input sai · Đánh giá spec: Spec không ghi · Evidence: ảnh 分析リスト + màn chỉnh sửa |
| TC-UI003-01 | UI | UI-003 | クロス分析 — Lưu cấu hình (trạng thái màn khi thất bại) | Abnormal | auto | Tất cả | Lưu thất bại thì màn hình không hiện dấu hiệu đã lưu trước khi tải lại trang | Đăng nhập admin, chọn bot test. Có danh sách TC41688_optimistic đã lưu, ghi lại 条件保存日時. Chuẩn bị công cụ sửa request của trình duyệt để xóa tham số trục tung khỏi request lưu | 1. Mở màn chỉnh sửa của TC41688_optimistic<br>2. Bật quy tắc xóa tham số trục tung khỏi request lưu<br>3. Bỏ bớt 1 tag rồi bấm 「保存・更新」<br>4. KHÔNG tải lại trang: ghi lại 条件保存日時 đang hiển thị và thông báo<br>5. Bấm sang màn khác (link menu) và ghi lại có cảnh báo rời trang hay không | Danh sách TC41688_optimistic · request bị xóa tham số trục tung | Sau khi máy chủ trả lỗi: 条件保存日時 trên màn vẫn là giá trị cũ; khi rời trang vẫn có cảnh báo thay đổi chưa lưu. Không có dấu hiệu nào khiến người dùng tưởng đã lưu thành công |  | Lấp Q6 · false success — NEW-9 ghi nhận code cập nhật lạc quan (edit.js:474-486) · Đánh giá spec: Spec không ghi — căn cứ REQ-005 Studio "không được coi là đã lưu thành công" · Evidence: ảnh màn trước reload |
| TC-ENV003-01 | UI | ENV-003 | クロス分析 — Lưu cấu hình với bot lớn | Boundary | manual | product | Trên production, lưu danh sách phân tích có parent filter khớp số friend lớn thì trục tung được giữ đúng | Production, bot test nội bộ có số friend lớn nhất có thể (ghi số thật). Ghi max_input_vars của production nếu Dev cung cấp được. Có danh sách TC41688_prd_big trục 「友だち情報」 | 1. Mở màn chỉnh sửa TC41688_prd_big, bật Network<br>2. Đổi trục sang 「タグ」 chọn 2 tag, đặt parent filter khớp nhiều friend nhất có thể, bấm 「選択した内容で基準軸を登録」<br>3. Bấm 「保存・更新」, ghi số tham số request, có hay không line_user_ids, mã phản hồi<br>4. Tải lại màn chỉnh sửa<br>5. Mở 分析リスト, chờ job production tính xong | Bot test production · số friend parent filter lớn nhất có được | Request không chứa line_user_ids; lưu thành công; sau tải lại trục là 「タグ」 với 2 tag; 分析リスト production có dòng và số liệu khớp parent filter |  | Lấp Q7 · RULE-08: cấu hình PHP và job phân tích production khác staging · manual vì môi trường production · Đánh giá spec: Spec không ghi · Evidence: HAR + ảnh 分析リスト |
| TC-DEPLOYLIVE001-01 | API | DEPLOY-LIVE-001 | クロス分析 — Lưu cấu hình (EP-16) | Normal | auto | Tất cả | Request lưu theo định dạng màn hình cũ với ít phần tử danh sách LINE user vẫn được bản fix chấp nhận và lưu đúng | Đăng nhập admin, chọn bot test, có cookie phiên và mã chống giả mạo biểu mẫu. Có danh sách TC41688_oldjs trục 「友だち情報」 | 1. Gửi POST /basic/saveCrossAnalysis theo đúng thứ tự payload bản cũ: line_user_ids gồm 20 phần tử đứng trước filter_by = 2 cùng 2 tag hợp lệ<br>2. Ghi mã HTTP và phản hồi<br>3. Mở màn chỉnh sửa và 分析リスト của TC41688_oldjs | line_user_ids 20 phần tử · filter_by = 2 · 2 tag | Phản hồi HTTP 200 với trạng thái thành công và mã danh sách; cấu hình lưu là trục 「タグ」 đúng 2 tag; 分析リスト có dòng. Tham số line_user_ids bị bỏ qua, không gây lỗi |  | Lấp Q8 · tab còn giữ JS cũ trong lúc deploy không bật maintain · Đánh giá spec: Spec không ghi · Evidence: request/response |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `framework/checklist-lme.md` §1.1 RULE-13 ↔ `saveCrossAnalysis` (EP-16) | Chốt mã HTTP khi `filter_by` là số ngoài {1,2,3}: giữ 400 như code hiện tại (cần ghi ngoại lệ) hay đổi sang 422 theo quy ước; cập nhật expected NEW-15 / NEW-16 / NEW-17 theo kết quả | C1 `CONF-SPEC` ở §4 | Dev / Leader |
| 2 | `spec-features/admin/` — chưa có thư mục cho FA-024 クロス分析 | Bổ sung Business rule: `filter_by` ∈ {1 友だち情報, 2 タグ, 3 友だち登録日}, lưu thiếu/sai → từ chối không ghi dữ liệu; `line_ids_parent` không còn được lưu/đọc; danh sách nơi đọc cấu hình (edit, copy, 分析リスト, export CSV, job) | I3 ở §5 | Leader / PM |
