# 05 — Review Report

> Draft cho Leader verify. Bug #38668 — Create google sheet qrlanding fail do lỗi phía google (FA-017 QR Code Action / Landing).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | Studio task #180 (ticket 38668, branch `ai_small_38668`, round 1, `aiResult=pass`, `reviewState=leader`) |
| Tổng số TC review | 28 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 14 vùng ảnh hưởng (a) + 6 file diff (b) · **9 vùng đủ TC · 2 GAP · 4 RISK**.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `F2 — QRCodeController::saveLandingV2`, **nhánh sao chép QR** (`mode='copy'`, BR-17 spec FA-017: copy **không** copy `google_sheet_id` ⇒ landing bản sao phải tự tạo sheet mới) | `diff code` | không có | **GAP — 0 TC** đi qua nhánh copy. Copy QR khi Google lỗi: landing bản sao có được lưu mã lỗi để job retry nhặt không, hay im lặng với mã lỗi rỗng (thành ca REQ-011 vĩnh viễn) | `[BLOCKER]` |
| G3 | `F1 — Landing::resolveGoogleSheetErrorCode` (3 nhánh suy mã lỗi: HTTP code `Google_Service_Exception` → `reason` → fallback) | `diff code` | `NEW-2` · `NEW-22` · `NEW-9` (mã lỗi **set sẵn trong DB**) | **GAP — không TC nào ép exception KHÔNG phải `Google_Service_Exception`** (timeout mạng / DNS fail / cURL error). Nhánh fallback quyết định mã lỗi lưu ra là số hay chữ → quyết định **có retry hay không**. Resolve ra chuỗi chữ ⇒ không retry ⇒ **bug gốc lặp lại nguyên vẹn** | `[BLOCKER]` |
| G4 | `F3 / T2 — JobInsertStatisticDataActionLandingToGoogleSheet` (job thống kê hàng ngày) | `dev-impact` | `NEW-19` (1 TC, 1 landing lỗi) | **RISK — [AP-3] happy-path-only.** REQ-003 yêu cầu "vẫn xử lý bình thường các landing khác" nhưng expected chỉ kiểm landing lỗi X1; không TC nào xác nhận job **không dừng giữa chừng** và vẫn ghi thống kê cho landing còn lại | `[MAJOR]` |
| G5 | `F5 — Kernel::schedule` (`landing:retry-create-google-sheet`, `everyMinute` + `withoutOverlapping`) | `dev-impact` | `NEW-18` | **RISK — chỉ verify TĨNH** (đọc file đăng ký lịch + `artisan list`). Không TC nào xác nhận job **thật sự chạy mỗi phút** trên server có scheduler (cron) ở môi trường thật | `[MAJOR]` |
| G6 | `F6 / D1 — migration `add_google_sheet_retry_to_landing_table`` | `dev-impact` | `NEW-25` (pass) · `NEW-28` (**skip**) | **RISK — TC rollback/rủi ro phát hành bị `skip`, không có kết luận.** Thêm 3 cột + index trên bảng `landing` cỡ production chưa được đo thời gian khóa bảng (release **không bật maintain**) | `[MAJOR]` |
| G7 | `T1 — QR Code Action / Landing`, output cuối chuỗi = **file Google Sheet thật** | `dev-impact` | `NEW-17` · `NEW-4` | **RISK — RULE-06.** Expected dừng ở "`google_sheet_id` khác rỗng" + "icon 「スプレッドシート表示」 có link đúng id". Không TC nào **mở sheet thật** để verify sheet tồn tại, đúng tên, đúng 4 cột header 「日時 / URL読み込み / 友だち追加・ブロック解除 / アクション稼働」 (LUỒNG 5 spec FA-017) | `[MAJOR]` |

> **Đã loại khỏi bảng GAP — `landing_connect_google.status = 4` (R-17)**: job thử lại mới lọc `status = DONE(2)`, nên bot mang giá trị `4` không được nhặt. Nhưng cron `landing:insert_google_sheet` **vốn đã** lọc `DONE(2)` từ **trước** bản vá ⇒ đây là **nợ có sẵn của tính năng, không phải thiếu sót của bộ TC cho fix #38668**, và fix không làm nó tệ hơn. Chuyển thành câu hỏi thiết kế cho Dev/PO ở **§6 mục 2**. ⚠️ Con số "8/20 dòng = 40%" trong spec là **toàn bộ bảng ở DB mà spec đọc (20 dòng, không phải production)** — spec tự ghi "dấu hiệu cần điều tra, **không phải thống kê đại diện**"; không được dùng để nói "40% khách hàng".
>
> `F7 — GoogleSheetService::createSheet` và `T3 — Form Builder (FA-011) / Lesson (FA-019) / Salon (FA-020)`: **không flag**. `spec_delta` của Studio xác nhận diff đúng 6 file / 272 dòng thêm / 0 dòng xoá, **không có** `app/Helpers/GoogleSheetService.php` ⇒ layer downstream không bị chạm code, không cần TC (tránh [AP-5] over-coverage).

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 21 quan điểm Trigger khớp task · **8 chưa cover đủ**.

<!-- Q2 (COMPAT-LEGACY-001) đã gỡ sau khi kiểm chứng: (a) status=4 là nợ có sẵn R-17, không thuộc phạm vi fix — chuyển §6 mục 2; (b) catalog MAP-GS-07 "2 loại header spreadsheet" là của FORM, không áp cho landing (sheet landing có header 4 cột cố định). Mã Q3…Q10 giữ nguyên để không vỡ tham chiếu "Lấp Qx" ở §5. -->


| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `JOB-001` | Cao (BẮT BUỘC — thêm job nền + gọi API bên thứ 3 theo lô) | **GAP — 0 TC.** Catalog `JOB-01` (rate limit API bên thứ 3, RULE-05) + `JOB-02` (retry **có backoff**, ghi log từng lần) đều không được test. Job retry **không có backoff**: 5 lần × 1 phút ⇒ chỉ chịu được sự cố Google **5 phút**; sự cố 503 thực tế thường dài hơn ⇒ landing kẹt vĩnh viễn | `[BLOCKER]` |
| Q3 | `DATA-BACKUP-001` | Cao (BẮT BUỘC — tính năng **thêm cột bảng DB**) | **GAP — 0 TC ở nhánh khôi phục dữ liệu xoá mềm.** `NEW-14` mới kiểm "landing xoá mềm không bị job nhặt"; chưa ai kiểm QR **khôi phục lại từ thùng rác** (BR-11/BR-12 FA-017, catalog `MAP-PLAN-03`) thì việc **đồng bộ dữ liệu lên Google Sheet còn chạy bình thường không**. ⚠️ Nhánh **copy bot (FA-033) đã loại khỏi phạm vi** — xem ghi chú dưới bảng | `[MAJOR]` |
| Q4 | `ENV-003` | Cao (BẮT BUỘC — job nền, **không được đánh × với lý do "đã pass"**) | **RISK — 28/28 TC chạy ở `local`**, 0 TC ở `staging` / `prd`. RULE-08: job nền + gọi Google API thật + scheduler không được kết luận từ local | `[MAJOR]` |
| Q5 | `INTG-SHEET-001` | Cao (BẮT BUỘC — ghi dữ liệu ra spreadsheet ngoài) | **RISK — thiếu chiều.** (a) không verify nội dung sheet thật (G7, RULE-06); (b) catalog `MAP-GS-03` "mất quyền / mất liên kết sau khi đã liên kết" chưa test; (c) **429 `RESOURCE_EXHAUSTED` (quota Google)** — lỗi tạm thời phổ biến nhất — rơi vào nhánh `< 500` nên **không được retry** | `[MAJOR]` |
| Q6 | `PERF-LARGE-001` | Trung bình → **Cao** (sync/export) | **GAP — 0 TC khối lượng lớn.** Job quét mỗi phút bằng `whereRaw REGEXP '^[0-9]+$' + CAST(...) > 500` — **REGEXP không dùng được index**; index mới `idx_landing_gsheet_retry_count` không phục vụ điều kiện này ⇒ full scan bảng `landing` 60 lần/giờ trên production | `[MAJOR]` |
| Q7 | `CONC-001` | Cao | **RISK — thiếu case.** `NEW-13` chỉ chạy job retry 3 lượt liên tiếp. Chưa test **job daily `landing:insert_google_sheet` (02:10) chạy đồng thời job retry** trên cùng landing — `withoutOverlapping` chỉ khoá job retry với chính nó, không khoá chéo 2 job ⇒ nguy cơ tạo **2 spreadsheet** cho 1 landing | `[MAJOR]` |
| Q8 | `STATE-CLEAN-001` | Cao | **RISK — dừng nửa chừng.** `NEW-6` mới verify "ngắt liên kết không reset số lần thử lại", chưa đi tiếp bước **liên kết lại**. Lúc nối lại, bot về trạng thái chờ ⇒ việc tạo sheet thuộc **lệnh tạo sheet cũ** (không đọc số lần thử lại), còn job thử lại mới thì không đụng bot ở trạng thái này ⇒ cần xác minh landing nào được tạo sheet lại, và **mã lỗi + số lần thử lại cũ có được dọn không** (lệnh cũ có trước bản vá, không biết 3 cột mới) — còn sót thì lần ngắt-nối sau landing mới kẹt vì hết 5 lượt | `[MAJOR]` |
| Q10 | `REG-RUN-001` | Cao (BẮT BUỘC — release khi có job đang chạy dở) | **GAP — 0 TC.** Catalog `JOB-04`: deploy / restart khi job retry đang xử lý dở. *(Hạ từ `[BLOCKER]` xuống `[MAJOR]` vì `withoutOverlapping` + tăng `retry_count` bằng SQL atomic đã giảm rủi ro — Leader chốt lại nếu không đồng ý.)* | `[MAJOR]` |

> **Đã loại khỏi phạm vi review** (kiểm chứng bằng kho + spec, không phải GAP): **sao chép dữ liệu bot 「データコピー」 (FA-033)** — QR code / trang đích **không nằm trong 13 loại dữ liệu được copy** (spec FA-033 BR-05/BR-06; kho `kho-tcs/fa033-backup-データコピー.md` `TC-BK-329` + `TC-BK-333`: "màn QR / trang đích ở bot B TRỐNG"). Bảng `landing` không bị copy bot đụng tới ⇒ 3 cột mới không phát sinh rủi ro ở luồng này, **không cần TC**.
>
> **Đã loại khỏi phạm vi review — `UI-003` (thông báo khi tạo sheet lỗi)**: Leader xác nhận hệ thống **không có cảnh báo** nào khi tạo QR mà bước tạo sheet lỗi. Đây là **hành vi đã biết và đúng BR-20** (lỗi tạo sheet không làm gãy luồng tạo QR), không phải điều cần TC đi phát hiện. Muốn bổ sung cảnh báo cho người dùng là **CR mới**, không thuộc phạm vi test của fix #38668.
>
> `SEC-002` Cao: có `NEW-23` (log không lộ token) nhưng thiếu Normal + Boundary (RULE-01) và chưa test `google_sheet_error_message` lưu **nguyên văn** phản hồi Google (403 thường kèm email chủ tài khoản) → xem I6 ở §4 (TC tương ứng đã tạm gác, xem ghi chú cuối §5).

---

## 3. TC trùng lặp nội dung

Đã rà **28/28 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-8` — "502, 503, 504 đều được đưa vào danh sách thử lại" | `NEW-7` — "Job thử lại nhặt đúng landing đủ điều kiện với mã lỗi 503" | `DUP-SUBSET` | Cùng `Normal` · cùng đối tượng+thao tác (job retry nhặt landing có mã lỗi server) · cùng tiền đề (bot status DONE, token khác rỗng nhưng không hợp lệ, landing chưa có sheet, retry_count 0) · cùng expected (retry_count 0→1 + nội dung lỗi bị ghi đè). 503 của `JOB002-01` **nằm trọn** trong tập 502/503/504 | `[MINOR]` |

- **Gate đã chạy**: giả định xoá `NEW-7` → chạy lại BƯỚC 2 + 3 trên 27 TC còn lại: coverage §1 và quan điểm §2 **không đổi** (nhánh "landing đủ điều kiện được nhặt" vẫn do `NEW-8` giữ). ⇒ Đề xuất **gộp** (giữ `NEW-8`, mang phần kiểm "job không phát sinh lỗi treo" của `JOB002-01` sang), không xoá trắng.
- `DUP-INFLATE`: **không có** — không nhóm trùng nào đang che GAP.
- `DUP-CONFLICT`: **không có**.
- Chồng lấn nhẹ (không đề nghị xoá): `NEW-9` (4xx + mã dạng chữ không retry) và `NEW-15` (biên 499/500/501) cùng khẳng định "≤ 500 không retry" nhưng khác `Loại case` và khác tập dữ liệu → giữ cả hai, xem I8 §4.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ 28 TC (nguồn) | **Môi trường đã chạy: 28/28 ở `local`**, `staging` / `dev` / `prd` đều 0 run. Task chạm **job nền + API Google + scheduler** ⇒ RULE-08 / `ENV-003` không cho kết luận từ local. 24/28 TC do `pipeline` (AI) chạy, 4 TC manual (`anhtt`) | Chạy lại bộ TC cốt lõi (job retry, tạo sheet thật, scheduler) trên `staging` + `prd` trước khi đóng ticket |
| I2 | `[MAJOR]` | Toàn bộ 28 TC (nguồn) | **Evidence trống** — 27 TC ghi `Đạt` nhưng cột `Evidence thực tế` rỗng (RULE-02: không tick Đạt khi chưa đính đúng loại bằng chứng). ⚠️ `testcase_list` không trả field evidence → **chưa kết luận được là thiếu thật** | Leader mở Studio task #180 đối chiếu evidence của các TC `pass`; thiếu thật thì yêu cầu bổ sung log job + ảnh sheet + ảnh bản ghi landing |
| I3 | `[MAJOR]` | 15/28 TC | **7 mã quan điểm không có trong `framework/checklist-lme.md`**: `TOOL-NEGCTRL-001`(4) · `JOB-002`(4) · `TOOL-AXIS-001`(2) · `TOOL-OLDREC-001`(2) · `TOOL-KNOW-002` · `OBS-001` · `TOOL-ERRHYG-001`. Các TC này **không tính là cover** ở §1/§2 ⇒ coverage quan điểm thực tế thấp hơn con số TC gợi ý | Map lại về mã chuẩn (vd `JOB-002` → `JOB-001`, `OBS-001` → `SEC-002`/`JOB-001`, `TOOL-OLDREC-001` → `COMPAT-LEGACY-001`), hoặc bổ sung mã mới vào checklist theo RULE-10 |
| I4 | `[MAJOR]` | `03-dev-impact.md` | Checkbox **"Tester verify auto-fill chính xác" chưa tick** (file auto-fill `2026-09-15 by /new-task`) ⇒ F/D/T chưa có người xác nhận | Tester đọc lại Redmine #38668 journal #125584, đối chiếu mục 4.1/4.2/4.3 rồi tick |
| I5 | `[MAJOR]` | `[AP-1]` — fix dạng helper dùng chung `resolveGoogleSheetErrorCode` | Fix gom xử lý lỗi về 1 helper 3 nhánh, dùng ở **3 điểm gọi**. TC hiện có mới trigger **mã lỗi set sẵn trong DB** + 2 trigger thật (token không hợp lệ, phản hồi thiếu `spreadsheetId`), **thiếu trigger "lỗi chưa biết"** (exception ngoài `Google_Service_Exception`) | Xem `G3` §1 — TC tương ứng (`TC-INTGSHEET001-01`) đã tạm gác vì khó ép lỗi timeout; cần Dev chứng minh nhánh fallback bằng cách khác |
| I6 | `[MAJOR]` | `NEW-23` | `SEC-002` (Cao) chỉ có 1 `Abnormal` — thiếu `Normal` + `Boundary` (RULE-01), và chưa test `google_sheet_error_message` lưu **nguyên văn** phản hồi Google (lỗi 403/401 thường kèm email chủ tài khoản Google = PII) | TC đề xuất (`TC-SEC002-02`) đã tạm gác vì khó lấy lỗi 403 kèm email — tối thiểu Dev xác nhận cột nội dung lỗi không hiển thị ra màn hình nào |
| I7 | `[MINOR]` | `NEW-28` | Trạng thái `skip` — **không có kết luận test** cho đúng phần rủi ro Dev tự nêu (quên chạy migration / chạy lùi migration) | Chạy lại trên DB test riêng, hoặc ghi rõ lý do skip vào Studio |
| I8 | `[NIT]` | `NEW-9` vs `NEW-15` | 2 TC cùng khẳng định "≤ 500 không retry" ở 2 góc (tập 4xx/chữ vs biên 499/500/501) — không trùng nhưng dư một phần | Giữ nguyên; khi chạy lại chỉ cần 1 lần dựng dữ liệu chung cho cả 2 |
| I9 | `[NIT]` | `03-dev-impact.md` mục "Commit / Pull Request" | Không có link PR, chỉ có branch + commit hash `801925eb26`. *(Không nâng lên `[MAJOR]` như `[AP-4]` vì Studio `spec_delta` đã cung cấp `diffStat` 6 file để đối chiếu fix shape.)* | Dev bổ sung link PR khi có |

---

## 5. TCs đề xuất bổ sung (4)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | (1) **`kho-tcs` chưa có `FA-017`** (QR Code Action / Landing) — không đối chiếu được cho tính năng chính. (2) `kho-tcs/fa033-backup-データコピー.md` — đã đọc vì có TC đề xuất chạm luồng copy bot |
| Vùng regression phát hiện từ kho | Không có. **Kho FA-033 dùng để LOẠI 1 GAP giả**: `TC-BK-329` + `TC-BK-333` xác nhận "màn QR / trang đích ở bot đích TRỐNG" — QR/landing không nằm trong 13 loại dữ liệu được copy (BR-05/BR-06 FA-033) ⇒ bỏ TC "copy bot mang theo mã sheet/mã lỗi", thay bằng nhánh khôi phục xoá mềm |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Nguồn spec đã dùng | `spec-features/admin/qr-landing/feature-spec.md` — LUỒNG 1 (BR-17, BR-20), LUỒNG 5 (BR-21, BR-22, cron `landing:insert_google_sheet` 02:10), §2.9 Cụm H, §R-17 (`status = 4` = 40% dữ liệu thật), §4.5 Index |
| Xác nhận chống trùng | Đã đối chiếu **28 TC** ở BƯỚC 0 — **không TC đề xuất nào trùng** theo 4 yếu tố |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Danh sách QR action — sao chép QR | Abnormal | manual | product | Sao chép QR action khi Google đang lỗi — bản sao có lưu mã lỗi để job thử lại nhặt không | - Bot đã liên kết Google, trạng thái liên kết hoàn tất<br>- Có sẵn 1 QR action A **đã có** spreadsheet (dòng A hiện icon 「スプレッドシート表示」)<br>- Chặn đường ra Google của server test (hoặc làm hỏng thông tin xác thực) để mọi lệnh gọi Google thất bại | 1. Vào 「QRコードアクション」, tick QR action A<br>2. Bấm sao chép (mode copy), đặt tên khác<br>3. Lưu, quay lại màn danh sách<br>4. Mở bản ghi landing của QR bản sao xem mã lỗi / nội dung lỗi / số lần thử lại<br>5. Mở Google đường truyền lại, đợi job thử lại chạy 1 phút<br>6. Tải lại màn danh sách | Tên QR bản sao: `QR売上分析（コピー）` | - Bước 3: tạo bản sao thành công, không báo lỗi đỏ, dòng QR mới xuất hiện<br>- Bước 3: QR bản sao **KHÔNG** mang `google_sheet_id` của QR A (BR-17) ⇒ chưa có icon 「スプレッドシート表示」<br>- Bước 4: bản sao có **mã lỗi khác rỗng** (vd `503`) + nội dung lỗi khác rỗng, số lần thử lại = 0<br>- Bước 6: sau khi mạng thông, job tự tạo sheet ⇒ dòng bản sao hiện icon 「スプレッドシート表示」, mã lỗi về rỗng<br>- ⚠️ Nếu bước 4 mã lỗi **rỗng** ⇒ nhánh copy không đi qua chỗ lưu lỗi ⇒ bản sao kẹt vĩnh viễn (lỗi, raise ticket) | | Lấp `G1` · Đánh giá spec: Spec ghi rõ (BR-17/BR-20 FA-017) · Evidence: ảnh màn danh sách trước/sau + ảnh bản ghi landing bản sao · regression |
| TC-INTGSHEET001-02 | Data | INTG-SHEET-001 | Job thử lại → file Google Sheet thật | Normal | manual | product | Thử lại thành công — mở sheet thật trên Google Drive kiểm tên, 4 cột tiêu đề và dữ liệu | - Bot test liên kết **tài khoản Google thật** (có quyền mở Drive để kiểm chứng)<br>- 1 landing đã có số liệu quét/kết bạn của ít nhất 1 ngày trước đó, chưa có spreadsheet, mã lỗi `503`, số lần thử lại 2 | 1. Cho đường ra Google hoạt động bình thường<br>2. Đợi job thử lại chạy (tối đa 1 phút)<br>3. Tải lại màn 「QRコードアクション」, bấm icon 「スプレッドシート表示」 của landing<br>4. Trong Google Drive mở file vừa tạo, đọc tên file + dòng tiêu đề + dữ liệu<br>5. Hôm sau (sau 02:10) mở lại file, kiểm dòng của ngày hôm trước | Tài khoản Google thật của team QA | - Bước 3: icon 「スプレッドシート表示」 xuất hiện, bấm mở đúng 1 spreadsheet mới<br>- Bước 4: file **mở được bằng chính tài khoản đã liên kết**, dòng 1 đúng 4 cột 「日時 / URL読み込み / 友だち追加・ブロック解除 / アクション稼働」, có đủ các dòng lịch sử trước đó<br>- Bước 4: mã lỗi + nội dung lỗi của landing đã về rỗng, số lần thử lại **giữ nguyên 2** (để tra cứu)<br>- Bước 5: job hàng ngày append thêm đúng **1 dòng của hôm qua**, không ghi đè dòng cũ | | Lấp `G7` + `Q5` · **RULE-06 output cuối chuỗi** · Đánh giá spec: Spec ghi rõ (LUỒNG 5 FA-017) · Evidence: ảnh chụp file Google Sheet (tên + header + dữ liệu) 2 ngày liên tiếp |
| TC-DATABACKUP001-01 | Data | DATA-BACKUP-001 | Thùng rác QR action 「削除済み」→ 「復元する」 | Normal | manual | product | QR khôi phục từ thùng rác vẫn đồng bộ dữ liệu lên Google Sheet bình thường | - Bot test đã liên kết Google, trạng thái hoàn tất<br>- Landing R1: **đã có** spreadsheet và đã có số liệu quét/kết bạn của hôm trước<br>- Landing R2: **chưa có** spreadsheet (mã lỗi `503`)<br>- Xoá mềm cả R1 và R2 từ màn danh sách QR | 1. Mở thùng rác 「削除済み」, bấm 「復元する」 cho R1 và R2<br>2. Về màn 「QRコードアクション」, kiểm dòng R1 / R2 và icon 「スプレッドシート表示」<br>3. Quét QR R1 vài lần để phát sinh số liệu mới<br>4. Hôm sau (sau 02:10) mở sheet của R1, kiểm dòng dữ liệu mới<br>5. Kiểm R2 đã được tạo sheet chưa | R1 (có sheet, có số liệu) · R2 (chưa có sheet) | - Bước 2: cả 2 QR quay lại danh sách; R1 vẫn còn icon 「スプレッドシート表示」 mở đúng file sheet cũ<br>- Bước 4: **sheet của R1 nhận thêm đúng 1 dòng số liệu của ngày vừa quét** — việc đồng bộ chạy lại bình thường sau khi khôi phục, không mất dòng nào và không tạo sheet mới<br>- Bước 5: R2 được tạo spreadsheet và hiện icon 「スプレッドシート表示」 | | Lấp `Q3` · regression · Catalog `MAP-PLAN-03` (khôi phục dữ liệu đã xoá mềm) · Đánh giá spec: Spec ghi rõ (BR-11 / BR-12 FA-017 §2.8 Cụm G) · Evidence: ảnh danh sách sau khôi phục + ảnh sheet của R1 có dòng mới |
| TC-STATECLEAN001-02 | UI | STATE-CLEAN-001 | Ngắt liên kết rồi liên kết lại Google 「Googleスプレッドシート連携」 | Abnormal | manual | product | Ngắt rồi liên kết lại Google — landing nào được tạo sheet lại, dấu vết lỗi cũ có được dọn không | - Bot test đang liên kết Google hoàn tất<br>- Landing K1: chưa có spreadsheet, mã lỗi `503`, số lần thử lại **5**<br>- Landing K2: chưa có spreadsheet, mã lỗi `503`, số lần thử lại **2**<br>- Landing K3: **đã có** spreadsheet | 1. Bấm 「Googleアカウントの接続を解除する」, xác nhận<br>2. Kiểm 3 landing: mã spreadsheet / mã lỗi / số lần thử lại<br>3. Liên kết lại Google (cùng tài khoản)<br>4. Ghi lại **trạng thái liên kết ngay sau khi nối lại** (chờ xử lý / đang xử lý / hoàn tất) và theo dõi tới khi về hoàn tất<br>5. Theo dõi log: **lệnh nào** tạo sheet cho 3 landing — lệnh tạo sheet cũ (chạy cho bot ở trạng thái chờ/lỗi) hay job thử lại mới (chỉ chạy cho bot hoàn tất)<br>6. Mở màn 「QRコードアクション」 xem dòng nào có icon 「スプレッドシート表示」<br>7. Với landing đã có sheet lại: kiểm mã lỗi + số lần thử lại còn sót giá trị cũ không | 3 landing K1/K2/K3 | - Bước 2: mã spreadsheet của **cả 3** landing về rỗng (BR-22, kể cả bản xoá mềm); số lần thử lại và mã lỗi **giữ nguyên** (K1 = 5, K2 = 2)<br>- Bước 6: **cả K1, K2, K3 đều được tạo sheet lại** — vì lúc bot vừa nối lại, việc tạo sheet thuộc **lệnh cũ** (lọc theo trạng thái chờ/lỗi, chỉ cần thiếu mã sheet), lệnh này **không đọc** số lần thử lại và mã lỗi. Số lần thử lại = 5 của K1 **không phải** điều kiện chặn ở luồng này<br>- Bước 5 phải chỉ ra đúng thủ phạm: nếu log cho thấy job thử lại mới nhặt bot vừa nối lại thì **sai thiết kế** (nó chỉ được chạy với bot hoàn tất) — raise ticket<br>- Bước 7 — **điểm rủi ro chính của TC này**: lệnh tạo sheet cũ có trước bản vá nên **không biết 3 cột mới**. Nếu sau khi tạo sheet thành công mà mã lỗi `503` + số lần thử lại 5 của K1 **vẫn còn nguyên** ⇒ dữ liệu rác; đến lần ngắt-nối lại **sau đó** (hoặc khi sheet bị xoá lần nữa) landing mới thật sự kẹt vì đã hết 5 lượt. Ghi rõ hiện trạng và đẩy §6<br>- ⚠️ Nếu bước 6 có landing **không** được tạo sheet lại ⇒ ngược với suy luận trên, nghĩa là lệnh cũ không chạy / không cover ⇒ ghi nhận và **hỏi Dev** lệnh tạo sheet cũ hiện có nằm trong lịch chạy không | | Lấp `Q8` · Đối chiếu REQ-012 Studio — **REQ-012 chỉ xét trong phạm vi job thử lại**, TC này kiểm cả lệnh tạo sheet cũ · Đánh giá spec: **Spec không ghi** — spec FA-017 §8.2 liệt kê 5 cron **không có** lệnh tạo sheet cũ ⇒ **bắt buộc hỏi Dev** lệnh đó chạy theo lịch hay chạy tay · Evidence: log 2 lệnh ở bước 5 + ảnh 3 bản ghi landing tại bước 2 / 6 / 7 |

> **11 TC đề xuất đã TẠM GÁC theo quyết định Leader (2026-09-18)** — lý do: **khó dựng môi trường test**. Các `GAP` / `RISK` tương ứng ở §1 · §2 **vẫn còn nguyên**, chỉ là chưa có TC để lấp:
>
> | GAP / RISK còn treo | TC đã tạm gác | Vì sao khó dựng |
> |---|---|---|
> | `G3` — nhánh fallback `resolveGoogleSheetErrorCode` | `TC-INTGSHEET001-01` | Phải ép lệnh gọi Google **treo tới timeout** ở tầng mạng (drop gói), không phải trả lỗi HTTP |
> | `G4` — job thống kê hàng ngày, 1 landing lỗi không chặn landing khác | `TC-REGSHARED001-03` | Phải ép lỗi **riêng cho 1 landing** trong khi các landing khác vẫn gọi Google bình thường |
> | `G5` + `Q4` — job chạy thật mỗi phút trên server có scheduler | `TC-ENV003-01` | Cần quyền theo dõi scheduler + log trên staging/production |
> | `G6` — migration trên bảng `landing` cỡ production | `TC-DEPLOYLIVE001-02` | Cần DB test riêng khôi phục từ bản sao production (≥ 500.000 bản ghi) |
> | `Q1` — rate limit + backoff của job | `TC-JOB001-01` · `TC-JOB001-02` | Cần 100 landing lỗi + ép chạm hạn mức Google, và chặn mạng liên tục 10 phút |
> | `Q5(c)` — Google trả `429 RESOURCE_EXHAUSTED` | `TC-INTGSHEET001-03` | Phải ép Google trả đúng 429 (vượt hạn mức thật hoặc proxy giả lập) |
> | `Q6` — khối lượng lớn, truy vấn `REGEXP` không dùng index | `TC-PERFLARGE001-01` | Cần bảng `landing` cỡ production + đo tải DB trong 30 phút |
> | `Q7` — job hàng ngày và job thử lại chạy đồng thời | `TC-CONC001-02` | Phải bắn 2 job lệch nhau < 1 giây, lặp 3 lần |
> | `Q10` — khởi động lại ứng dụng giữa lúc job đang chạy | `TC-REGRUN001-01` | Phải cắt tiến trình job đúng lúc đang xử lý giữa danh sách |
> | `SEC-002` (I6 §4) — nội dung lỗi chứa email chủ tài khoản | `TC-SEC002-02` | Phải thu hồi quyền Google để lấy đúng lỗi 403 có kèm email |
>
> ⇒ **Hệ quả cần Leader biết**: 4 TC còn lại chỉ lấp `G1` · `G7` · `Q3` · `Q8`. Các dòng còn treo ở trên **chưa có ai kiểm**, trong đó `G3` là `[BLOCKER]` (nhánh quyết định "có retry hay không") và `Q1` là `[BLOCKER]`. Nếu không mở lại TC thì phải chấp nhận rủi ro đó khi release, hoặc chuyển sang cách kiểm nhẹ hơn (Dev tự chứng minh bằng unit test / đọc code cùng Leader).
>
> **Ghi chú RULE-01**: `INTG-SHEET-001` (Cao) hiện chỉ còn `Normal` (`TC-INTGSHEET001-02`); chiều `Abnormal` + `Boundary` nằm trong nhóm đã tạm gác ⇒ quan điểm này **chưa đạt RULE-01**, đã phản ánh ở `Q5` §2.

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | Quy tắc thử lại tạo Google Sheet — ngưỡng `GOOGLE_SHEET_RETRY_MIN_CODE = 500` | Chốt **danh sách mã lỗi được thử lại**. Hiện `> 500` loại cả: `429 RESOURCE_EXHAUSTED` (vượt hạn mức — lỗi tạm thời đáng thử lại nhất), `500 internalError`, và **mọi lỗi có `reason` dạng chữ**. ⚠️ Log trong chính ticket #38668 là `"code": 503` kèm `"reason": "backendError"` — nếu exception không mang HTTP code mà chỉ có `reason` chữ thì ca gốc **không được thử lại** | REQ-005 Studio (Dev tự ghi "diễn giải của dev, chưa được ticket khẳng định — cần PO xác nhận") (TC `TC-INTGSHEET001-03` đã tạm gác) | **PO** + Dev |
| 2 | FA-017 §2.9 Cụm H / LUỒNG 5 — điều kiện lọc `landing_connect_google.status` | **Nợ có sẵn (R-17), không do fix #38668 gây ra** — nêu ở đây để PO quyết có gộp vào ticket này không: giá trị `status = 4` không có trong hằng số model, mà **cả** cron `landing:insert_google_sheet` (có từ trước) **lẫn** job thử lại mới đều lọc `DONE(2)` ⇒ bot mang giá trị `4` vừa không được đẩy dữ liệu vừa không được thử lại. Việc cần làm trước: **query phân bố `status` trên production** để biết nhóm này có thật và lớn đến đâu — số "8/20 = 40%" trong spec là toàn bộ bảng ở DB spec đọc, spec tự ghi **không phải thống kê đại diện**. Có thật và đáng kể → mở ticket riêng, **không nhét vào phạm vi test của #38668** | `spec-features/admin/qr-landing/feature-spec.md` §R-17 (nợ có sẵn, không phải conflict với TC nào) | **Dev** (ý nghĩa của `4` + query production) → PO quyết phạm vi |
| 3 | Chính sách thử lại — số lần và giãn cách | Chốt việc **5 lần × 1 phút = chỉ chịu được sự cố Google 5 phút**, không có backoff giãn dần. Sự cố 503 của Google thường kéo dài hơn ⇒ landing kẹt vĩnh viễn dù Google đã hồi phục. Đề nghị: giãn cách tăng dần, hoặc cho phép reset số lần thử lại từ giao diện | Ticket #38668 chỉ ghi "Expect cần retry lại 5 lần" (không nói nhịp) (TC `TC-JOB001-02` đã tạm gác) | **PO** |
| 4 | FA-017 BR-22 + §8.2 danh sách cron | 2 việc phải chốt: **(a)** lệnh tạo sheet cũ (`app:create-google-sheet`, lọc bot ở trạng thái chờ/lỗi) hiện **có nằm trong lịch chạy không** — spec FA-017 §8.2 liệt kê 5 cron và **không có** lệnh này, trong khi nó là đường tạo sheet duy nhất sau khi khách nối lại Google. **(b)** Lệnh cũ có trước bản vá nên **không dọn** `google_sheet_error_code` / `google_sheet_retry_count`: sau khi nó tạo sheet thành công, landing vẫn mang mã lỗi cũ và số lần thử lại cũ ⇒ dữ liệu rác, và đến lần ngắt-nối lại sau đó landing hết 5 lượt mới thật sự kẹt | REQ-012 Studio **chỉ xét phạm vi job thử lại**, chưa xét lệnh cũ — `TC-STATECLEAN001-02` | **Dev** (a) + PO (b) |
| 5 | Xử lý dữ liệu tồn trước khi phát hành bản vá | Chốt cách xử lý landing đã mất sheet **trước** khi phát hành (mã lỗi rỗng ⇒ không nằm trong tập thử lại): chạy lệnh khôi phục thủ công `LandingCreateGoogleSheetMissingCommand`, hay cập nhật mã lỗi bằng tay? Cần trước ngày release | REQ-011 Studio + `NEW-10` (đã pass, xác nhận nhóm này không được thử lại) | **PO** + vận hành |
