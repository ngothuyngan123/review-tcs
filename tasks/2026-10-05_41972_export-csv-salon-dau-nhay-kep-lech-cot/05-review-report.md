# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; vòng review = round 1.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #359 (ticket 41972, round 1) |
| Tổng số TC review | 19 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 3/7 mục có TC — **CHƯA ĐỦ** (BUG · F1 · T1 đủ; F2 · T2 · T3 · T4 có TC nhưng **0 TC được chạy**) |
| **(b) diff code** — Studio `dev_impact` + mục 1–3 file 03 | 4/9 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 7/18 vùng ảnh hưởng đủ TC · 2 GAP · 9 RISK (trùng nhau: 4 RISK của chiều (a) và 2 RISK của chiều (b) cùng nằm ở CSV bạn bè — gộp vào G1). Gồm 2 vùng Leader bổ sung phạm vi ngày 2026-10-05 (G5 · G6): yêu cầu *"3 loại file CSV do job sinh, dữ liệu chứa `"` không bị sai/lệch"*.

> Input thiếu: Studio `diffAvailable = false` (không tìm thấy ref `m_202609_fix_salon_csv_41972`) — chiều (b) dựa trên `dev_impact` Studio (suy từ đọc source) + mục 1–3 file 03, chưa đối chiếu được diff thật của commit `e73e25a4`.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F2 `HandleExportCsvTask.convertToStringLine` + T2 (最終メッセージ受信日時 rỗng — 「年齢」 Dev kê ở T2 đã ẩn khỏi tool, bỏ khỏi phạm vi) + T3 (chữ "null" trong tên/email giữ nguyên) + T4 (bỏ chọn 対応マーク / 流入経路) — CSV bạn bè | dev-impact + diff code | NEW-15 · NEW-16 · NEW-17 · NEW-18 | **RISK** — cả 4 TC `skip`, `env_scope` chỉ `local`. Lý do skip ghi ở TC là *"job Java tắt ở production, Laravel là bản live"* — **trái spec** (xem C1 §4): spec ghi job Java là luồng **đang chạy production**. Nếu spec đúng, hàm sửa trực tiếp đi production mà chưa được chạy lần nào | `[BLOCKER]` |
| G2 | Viết lại escape `"` ở CSV bạn bè — file này **đã** escape `"`→`""` từ trước (spec `job-spec.md` dòng 352, #35640) → rủi ro escape 2 lần | diff code | NEW-18 | **RISK** — TC `skip`; expected của ô 「LINE表示名」 không đo lường được (xem I4) | `[MAJOR]` |
| G3 | Rủi ro Studio *"ô null / ô ghép chuỗi có null sẽ lộ chữ null"* — CSV bạn bè: cột Thông tin bạn bè 「友だち情報_{id}」 không có giá trị, không có Ghi chú riêng 「個別メモ」, ô có giá trị đúng bằng `null` | diff code | không có | **GAP** — NEW-15 chỉ chọn 単一選択項目 + 基本情報, không chọn cột 友だち情報 nào; không TC nào ở CSV bạn bè dùng giá trị đúng bằng `null` (rule mới của fix) | `[MAJOR]` |
| G4 | File CSV xuất trước deploy không tự đổi; xuất lại cho kết quả đúng (mục 4.2 Dev) | diff code | NEW-4 | **RISK** — TC `skip`; tiền đề phụ thuộc chuẩn bị file **trước** deploy nên dễ không chạy được (xem I6) | `[MINOR]` |
| G5 | CSV lịch sử chat 1:1 (Cài đặt chat 「チャット設定」 → 「チャットのCSVエクスポート」): friend name chứa `"`, nội dung chat chứa `"` | phạm vi Leader chốt 2026-10-05 | không có | **GAP** — 0 TC. ⚠️ Exporter chat 1:1 (`HandleExportCsvChat11Task`) **không có** trong file 03 / commit `e73e25a4` → Dev phải xác nhận đã sửa, nếu chưa thì TC dự kiến fail | `[BLOCKER]` |
| G6 | CSV quản lý CSV: Thông tin bạn bè 「友だち情報」 chứa `"` ở nhiều kiểu mục | phạm vi Leader chốt 2026-10-05 | NEW-18 (1 mục text, giá trị `""`) | **RISK** — chỉ 1 kiểu mục, TC `skip`; expected của NEW-18 (giữ `"`) trái hành vi Leader xác nhận (`"` → `?`), xem C2 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 6 quan điểm Trigger khớp task · 5 chưa cover đủ (JOB-001 đủ theo nội dung: NEW-6 đối chiếu số dòng vào/ra; retry / rate limit không áp dụng vì job không gọi API ngoài).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `OUT-EXPORT-001` | Cao (nâng — export CSV) | **RISK** — TC Normal duy nhất mang mã này (NEW-2) `skip`; Abnormal chỉ có ở TC mang mã nội bộ Studio (NEW-8 · NEW-12 · NEW-13) → không tính cover. Nội dung các TC Normal/Abnormal **đã đúng** quan điểm này (NEW-5 · NEW-10 · NEW-8 · NEW-12) — chỉ thiếu gắn mã | `[MAJOR]` |
| Q2 | `DATA-TEXT-001` | Cao (nâng — text đi ra file export) | **RISK** — chỉ có Normal (NEW-7 pass, NEW-16 skip); thiếu Abnormal + Boundary (RULE-01). Catalog DI-01 (ký tự 機種依存 ①㈱髙﨑, emoji, kana nửa độ rộng) chưa test kèm dấu `"` trong file SHIFT-JIS | `[MAJOR]` |
| Q3 | `ENV-003` | Cao | **GAP** — job nền (RULE-08) nhưng 0/19 TC chạy ngoài `local`; NEW-1 · NEW-2 (scope `all`, Google Calendar + Excel thật) đều `skip`; 15/19 TC `env_scope` chỉ `local` | `[BLOCKER]` |
| Q4 | `COMPAT-LEGACY-001` | Cao | **GAP** — CSV bạn bè có 2 tác nhân sinh file (Laravel `handle:export_csv` cũ ↔ job Java hiện hành); không TC nào xác nhận file thực tế ở staging/prd do tác nhân nào sinh, tức bản fix có tới tay khách hay không (C1) | `[BLOCKER]` |
| Q5 | `REG-SHARED-001` | Cao | **GAP** — Leader chốt (2026-10-05) exporter thứ 3 `HandleExportCsvChat11Task` (CSV lịch sử chat 1:1) thuộc phạm vi, nhưng Dev chưa kê và 0 TC. TC CSV bạn bè (NEW-18) `skip` | `[BLOCKER]` |

- Q1: **không đẻ TC mới** — đổi mã quan điểm trên Studio (`testcase_update`): NEW-5 · NEW-10 → `OUT-EXPORT-001` Normal; NEW-8 · NEW-12 → `OUT-EXPORT-001` Abnormal (nội dung đã khớp `Kiểm tra` (1)(5)(7) của quan điểm).
- Q3: phần CSV salon **không đẻ TC mới** — chạy NEW-1 · NEW-2 ở **staging + prd** (scope `all` có sẵn), kèm kho `TC-SLN-471` (job export CSV lịch sử sync — PRODUCTION). Phần CSV bạn bè → `TC-COMPATLEGACY001-01` ở §7.
- Q5: lấp bằng `TC-OUTEXPORT001-02` · `TC-OUTEXPORT001-03` (chat 1:1) ở §7; Dev vẫn phải bổ sung F3 vào file 03 (I5).

---

## 3. TC trùng lặp nội dung

Đã rà 19 TC, không phát hiện trùng lặp. Các cặp gần giống đã xét và giữ cả hai vì khác tầng kiểm chứng / môi trường: NEW-1 ↔ NEW-5 (LINE + Excel thật ↔ job tự động `local`) · NEW-2 ↔ NEW-11 (Google Calendar thật ↔ dữ liệu dựng `local`) · NEW-3 ↔ NEW-1 (luồng UI với dữ liệu dựng ↔ dữ liệu thật).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-15 · NEW-16 · NEW-17 · NEW-18 | Tác nhân sinh CSV bạn bè trên production → quyết định phạm vi ENV của TC và bản fix F2 có tới production không | `Ghi chú` TC: *"Job Java xuất CSV bạn bè TẮT ở production (Laravel HandleExportCsv là bản live) ⇒ TC chỉ local"* | `csv-management/web/logic-spec.md` §8.1 (a): *"Luồng HIỆN HÀNH — job Spring Boot HandleExportCsvTask … 94/208 bản ghi dạng `_{14 số}.csv`, mới nhất 2026-04-15 … Java đang là tác nhân chạy trên production"*; (b): Laravel *"đã ngừng sinh file mới"* (dừng 2024-07-29). `feature-spec.md` dòng 758: Laravel command *"là DI SẢN"* | (1) Ghi chú TC sai → NEW-15..18 phải mở `env_scope` ra staging/prd và G1 là `[BLOCKER]` thật · (2) Spec cũ hơn cấu hình production hiện tại (spec tự đánh tin cậy **Thấp** cho flag prod — `job-spec.md` câu hỏi mở #1) → fix F2 không có hiệu lực ở prd, cần ghi rõ cho PM | `[MAJOR]` | Dev |

| C2 | `CONF-SPEC` | NEW-18 vs `TC-OUTEXPORT001-04` (§7) | Dấu `"` trong dữ liệu friend ở CSV bạn bè xuất ra thế nào | NEW-18: 「システム表示名」 = `佐藤"VIP"`, 「個別メモ」 = `メモ"重要",確認`, 「友だち情報_メモ欄41972」 = `""` — *"mỗi dấu nháy kép hiển thị đúng 1 lần"* | Leader xác nhận 2026-10-05: *"encoding kiểu shift-JIS nên `"` sẽ bị đổi thành `?`"* (TC-OUTEXPORT001-04 viết theo xác nhận này). Đối chiếu `csv-management/job/job-spec.md` dòng 352: `convertToStringLine` *"Escape `"` → `""`"* — tức `"` được giữ. Lưu ý: `"` có trong bảng mã SHIFT-JIS; ghi chú NEW-18 chỉ ra phép đổi `"`→`?` nằm trong code (`HandleExportCsvTask.java:434`) và **chỉ cho tên LINE** | (1) Phép đổi `?` chỉ áp cho tên LINE → NEW-18 đúng cho 3 trường còn lại, TC-OUTEXPORT001-04 phải sửa expected thành giữ `"` · (2) Mọi trường đều đổi `?` → NEW-18 sai, spec job-spec dòng 352 cần update | `[MAJOR]` | Dev |

**Đã rà**: 19 TC × `spec-features/admin/salon-booking/feature-spec.md` §7.1.3 + `job/job-spec.md` §3.3 / §4.3 · `spec-features/admin/csv-management/feature-spec.md` + `job/job-spec.md` + `web/logic-spec.md` · `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (TC-SLN-372 · 471 · 484). Không có `CONF-TC`, không có `CONF-KHO`. **kho-tcs chưa có FA-014 (CSV管理)** — phần CSV bạn bè không đối chiếu được kho.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — toàn bộ | Chỉ 10/19 TC (52,6%) `pass`; 9 TC `skip` = không có kết luận: NEW-1 · NEW-2 · NEW-3 · NEW-4 · NEW-15 · NEW-16 · NEW-17 · NEW-18 · NEW-19. Toàn bộ CSV bạn bè (F2) và toàn bộ TC đối chiếu bằng Excel thật đều nằm trong nhóm `skip` | Chạy lại sau khi chốt C1; NEW-1 · NEW-2 chạy tay ở staging + prd |
| I2 | `[MAJOR]` | Nguồn — toàn bộ | RULE-08 / ENV-003: task sửa **2 job nền** nhưng 19/19 TC chỉ chạy `local`, 0 TC production | Xem Q3; mở `env_scope` NEW-15..18 theo kết quả C1 |
| I3 | `[MAJOR]` | 19/19 TC | Cột `Trạng thái đánh giá spec` trống ở mọi TC — đặc biệt NEW-9 (expected = *"hành vi Dev chọn — chờ PO xác nhận"*) và NEW-18 đang dựa trên hành vi chưa ai chốt | Điền `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`; NEW-9 · NEW-18 ghi `Spec không ghi` + link §8 #2 / #3 |
| I4 | `[MAJOR]` | NEW-18 | Expected không đo lường được: *"ký tự hiển thị thay cho dấu nháy (\" hay ?) GHI NHẬN THỰC TẾ, chưa kết luận pass/fail cho tới khi PO chốt"*. Leader đã xác nhận 2026-10-05: CSV bạn bè đổi `"` thành `?` | Sửa expected ô 「LINE表示名」 của NEW-18 trên Studio: `鈴木"一郎` → `鈴木?一郎`, đúng 1 ô. 3 trường còn lại của NEW-18 chờ C2 |
| I5 | `[BLOCKER]` | Phạm vi Dev (REG-SHARED-001) | Leader chốt CSV chat 1:1 thuộc phạm vi task, nhưng file 03 + commit `e73e25a4` chỉ sửa 2 file; `HandleExportCsvChat11Task` (cùng thư mục `threads/csv/`) không được kê | Dev xác nhận đã sửa / chưa sửa exporter chat 1:1; bổ sung F3 + T5 vào `03-dev-impact.md` |
| I8 | `[MAJOR]` | NEW-15 | Bước 3 chọn 「年齢」 và expected kiểm 「年齢」 rỗng (friend A) / tuổi tính từ 1995-01-01 (friend B) — mục 「年齢」 đã không còn dùng trên tool (Leader xác nhận 2026-10-05; spec `csv-management/db/db-mapping.md` U-07: `d_5` bị ẩn khỏi UI) → bước không thao tác được | Sửa NEW-15 trên Studio (`testcase_update`): bỏ 「年齢」 khỏi bước 3 + expected, giữ 「生年月日」 để kiểm ô trống. Báo Dev bỏ 「年齢」 khỏi T2 ở file 03 |
| I6 | `[MINOR]` | NEW-4 | Tiền đề yêu cầu xuất bản A **trước** deploy — bỏ lỡ thời điểm là không chạy được (TC đang `skip`) | Đổi tiền đề: dùng file đã xuất trước deploy còn trên server (bản ghi cũ của bảng `calendar_salon_download_csv_sync_google_calendar`, cột `file`) |
| I7 | `[MINOR]` | NEW-6 · NEW-9 · NEW-11 | Gắn `FUNC-004` (giới hạn số ký tự / số lượng) nhưng không kiểm giới hạn nào — nội dung là vị trí biên của dấu `"` / giá trị `null` | Đổi mã sang `OUT-EXPORT-001` (NEW-6 · NEW-11) và `DATA-TEXT-001` (NEW-9) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 19 TC — không có TC nào ngoài phạm vi task. NEW-13 (「表示しない」) · NEW-14 (header) · NEW-19 (xuống dòng trong tiêu đề) dẫn được từ `dev_impact` Studio (use_verification_code · header có xuống dòng) và catalog DI-19.

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm Googleカレンダー連携 · Job nền & monitor · Phân quyền & môi trường) · `kho-tcs/fa041-caidatchat-チャット設定.md` (nhóm CSV export — nội dung file) · **kho-tcs chưa có FA-014 (CSV管理) — không đối chiếu được** |
| Vùng regression phát hiện từ kho | TC-SLN-372 (tải CSV ở tab データ同期履歴) · TC-SLN-471 (job export CSV lịch sử sync, PRODUCTION, SHIFT-JIS) · TC-SLN-484 (tên ký tự đặc biệt → CSV mở Excel không lỗi font) · TC-CST-113 (5 cột) · TC-CST-115 (送信者名) · TC-CST-121 (nội dung chứa `,` / `"` escape đúng chuẩn) · TC-CST-125 (tên file per-friend chứa tên friend) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Q3 (phần salon) → TC-SLN-471 *"Job export CSV lịch sử đồng bộ Google — encoding và nội dung"* — bổ sung dữ liệu: 1 booking của friend có tên LINE chứa `"`, 1 sự kiện Google có tiêu đề `打合せ"A社","B社"` (chạy cùng NEW-1 · NEW-2) |
| Căn cứ TC regression `R<x>` | R1 ← kho TC-SLN-484 (gộp vào `TC-DATATEXT001-01`) |
| Xác nhận chống trùng | Đã đối chiếu 19 TC ở BƯỚC 0 + kho FA-020 + FA-041 — không TC đề xuất nào trùng. `TC-OUTEXPORT001-03` gần với kho TC-CST-121 nhưng TC kho dựa trên file mẫu có sẵn (không có dữ liệu cụ thể, Not Tested); Leader yêu cầu TC riêng cho ticket này nên viết với dữ liệu dựng được |

- **G1, G2, G4 không đẻ TC mới** (BƯỚC 5b — TC đã có: NEW-15..18 · NEW-18 · NEW-4; thiếu là do chưa chạy / expected / tiền đề → xử ở I1 · I4 · I6). G1 có thêm `TC-COMPATLEGACY001-01` cho phần môi trường thật.
- Q1 không đẻ TC — lý do ở §2.
- G5 (chat 1:1) → `TC-OUTEXPORT001-02` · `-03`; G6 (friend info chứa `"`) → `TC-OUTEXPORT001-04` — bổ sung theo yêu cầu Leader 2026-10-05.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-COMPATLEGACY001-01 | Job | COMPAT-LEGACY-001 | Quản lý CSV 「CSV管理」 — xuất CSV danh sách bạn bè | Normal | auto | dev, local, prd, staging | CSV bạn bè trên môi trường thật do job Java sinh và áp bản fix: chữ null giữ nguyên, ô trống không hiện null | - Môi trường đã deploy nhánh `m_202609_fix_salon_csv_41972`<br>- Bot test B; friend F1 có Tên hiển thị hệ thống 「システム表示名」 = nullpo, Email 「メールアドレス」 = null@gmail.com, tên LINE = 鈴木"一郎<br>- Friend F2 chưa từng gửi tin cho bot, chưa có Ngày sinh 「生年月日」<br>- Gắn tag 「T41972」 cho F1, F2 | 1. Đăng nhập admin bot B, mở Quản lý CSV 「CSV管理」.<br>2. Bấm Tạo mới 「新規作成」, nhập Tên xuất 「書き出し名」 = 41972_env.<br>3. Bấm Lọc 「絞込み」, lọc theo tag 「T41972」.<br>4. Chọn Thời điểm nhận tin cuối 「最終メッセージ受信日時」 và 基本情報: 「システム表示名」, 「メールアドレス」, 「生年月日」.<br>5. Bấm 「この条件でCSVを作成・更新」, chờ dòng hiện nút Tải CSV 「CSVダウンロード」.<br>6. Bấm 「CSVダウンロード」, ghi lại tên file tải về.<br>7. Mở file bằng Excel tiếng Nhật. | F1: nullpo / null@gmail.com / 鈴木"一郎<br>F2: không nhắn tin, không ngày sinh | - Tên file dạng `41972_env_<id>_<14 chữ số>.csv` (quy ước job Java), KHÔNG phải dạng `_<8 chữ số>.csv` (Laravel cũ)<br>- Dòng F1: 「システム表示名」 = nullpo, 「メールアドレス」 = null@gmail.com<br>- Dòng F2: 「最終メッセージ受信日時」, 「生年月日」 rỗng, không hiện chữ null<br>- Mọi dòng dữ liệu có số ô bằng dòng nhãn tiêu đề |  | Lấp G1 · Q3 · Q4 · Đánh giá spec: Spec ghi rõ (`csv-management/web/logic-spec.md` §8.1 (a)/(b) — quy ước tên file 2 tác nhân) · Tên file ra dạng 8 chữ số → fix KHÔNG có hiệu lực ở môi trường đó, báo Dev ngay · Không thay thế NEW-15..18 · Evidence: file CSV tải về + ảnh màn 「CSV管理」 |
| TC-OUTEXPORT001-01 | Job | OUT-EXPORT-001 | Quản lý CSV 「CSV管理」 — xuất CSV danh sách bạn bè | Abnormal | auto | dev, local, prd, staging | CSV bạn bè: cột Thông tin bạn bè 「友だち情報」 không có giá trị và ô đúng bằng chữ null xuất rỗng, không lệch cột | - Môi trường đã deploy nhánh fix, job Java xuất CSV bạn bè đang chạy<br>- Bot B có 3 Thông tin bạn bè 「友だち情報」: 41972_text (văn bản), 41972_date (ngày), 41972_select (chọn 1)<br>- Friend F3 đã nhắn tin cho bot, KHÔNG nhập giá trị nào cho 3 mục trên, KHÔNG có Ghi chú riêng 「個別メモ」, 「システム表示名」 = null<br>- Friend F4 (đối chứng): 3 mục = annull / 2026-10-01 / lựa chọn 1, 「個別メモ」 = null確認<br>- Gắn tag 「T41972b」 cho F3, F4 | 1. Mở Quản lý CSV 「CSV管理」 → bấm Tạo mới 「新規作成」.<br>2. Bấm Lọc 「絞込み」, lọc theo tag 「T41972b」.<br>3. Chọn 「個別メモ」, 基本情報 「システム表示名」 và 3 mục 友だち情報 41972_text / 41972_date / 41972_select.<br>4. Bấm 「この条件でCSVを作成・更新」, chờ nút 「CSVダウンロード」.<br>5. Tải file, mở bằng Excel tiếng Nhật. | F3: 「システム表示名」 = null (đúng 4 ký tự), 3 友だち情報 trống, 0 個別メモ<br>F4: annull / 2026-10-01 / lựa chọn 1 / null確認 | - Mọi dòng dữ liệu có số ô bằng dòng nhãn tiêu đề<br>- Dòng F3: 3 ô 「友だち情報_41972_*」 và ô 「個別メモ」 rỗng, không ô nào chứa chữ null<br>- Dòng F3: ô 「システム表示名」 rỗng (theo cách fix Dev: ô đúng bằng "null" → rỗng)<br>- Dòng F4: 3 ô 友だち情報 = annull / 2026-10-01 / lựa chọn 1; 「個別メモ」 = null確認 |  | Lấp G3 · căn cứ Studio `dev_impact`: *"ô ghép chuỗi có null ở giữa sẽ lộ chữ null"* + *"cột memo"*; cột `友だち情報_{id}` lấy từ `findListFriendInfo` (`csv-management/job/job-spec.md` §4.1) · Đánh giá spec: Spec không ghi (ô đúng bằng "null" — chờ PO, §8 #3) · Evidence: file CSV |
| TC-DATATEXT001-01 | Job | DATA-TEXT-001 | Googleカレンダー連携 — CSV lịch sử đồng bộ 「データ同期履歴」 | Boundary | auto | dev, local, prd, staging | CSV salon chiều 「エルメ → Googleカレンダー」: tên có ký tự 機種依存 kèm dấu nháy kép vẫn đúng 1 ô và không lỗi font | - Môi trường đã deploy nhánh fix, job xuất CSV salon đang chạy<br>- Lịch salon riêng cho TC, nhân viên S đã liên kết Google Calendar, đồng bộ 「エルメ → Googleカレンダー」<br>- Friend F có tên LINE và 「システム表示名」 theo dữ liệu nhập; tháng hiện tại có 1 dòng lịch sử đồng bộ chiều エルメ → Google gắn F, trạng thái 登録 | 1. Mở lịch salon → tab Cài đặt đặt lịch 「予約設定」 → 「Googleカレンダー連携」 → 「データ同期履歴」.<br>2. Mở modal 「連携履歴 CSVダウンロード」, chọn tháng hiện tại + chiều 「エルメ → Googleカレンダー」, bấm 「ダウンロード」.<br>3. Chờ nút 「CSVダウンロード」, tải file.<br>4. Mở file bằng Excel tiếng Nhật. | Tên LINE: ①㈱髙﨑"様<br>「システム表示名」: ｶﾅ"ﾃｽﾄ (kana nửa độ rộng) | - Dòng tiêu đề 8 ô, dòng dữ liệu 8 ô<br>- Ô 「予約者LINE名」 = ①㈱髙﨑"様 đúng nguyên văn (không thành ?, không lỗi font)<br>- Ô 「予約者システム表示名」 = ｶﾅ"ﾃｽﾄ<br>- Các ô ngày / giờ / 「登録・削除・手動削除」 đúng cột |  | Lấp Q2 · R1 regression · dẫn từ kho TC-SLN-484 (CSV mở bằng Excel không lỗi font) · Đánh giá spec: Spec không ghi — spec chỉ ghi "SHIFT-JIS", không ghi bảng mã MS932 / Windows-31J; Shift_JIS chuẩn không có ①㈱髙﨑 → ra `?` là lỗi có sẵn (không do fix) nhưng phải báo · Evidence: file CSV + ảnh Excel |
| TC-DATATEXT001-02 | Job | DATA-TEXT-001 | Googleカレンダー連携 — CSV lịch sử đồng bộ 「データ同期履歴」 | Abnormal | auto | dev, local, prd, staging | CSV salon chiều 「Googleカレンダー → エルメ」: tiêu đề sự kiện có emoji kèm dấu nháy kép không làm job lỗi và không lệch cột | - Môi trường đã deploy nhánh fix, job xuất CSV salon đang chạy<br>- Lịch salon riêng cho TC, nhân viên S đã liên kết Google Calendar, đồng bộ 「Googleカレンダー → エルメ」 bật<br>- Ở 「連携設定」 của S, 「Googleカレンダー スケジュールタイトルの表示」 = 「表示する」<br>- Tháng hiện tại có 2 sự kiện Google đã đồng bộ về エルメ theo dữ liệu nhập | 1. Mở 「データ同期履歴」 → modal 「連携履歴 CSVダウンロード」.<br>2. Chọn tháng hiện tại + chiều 「Googleカレンダー → エルメ」, bấm 「ダウンロード」.<br>3. Quan sát trạng thái trên modal đến khi hiện nút 「CSVダウンロード」.<br>4. Tải file, mở bằng Excel tiếng Nhật. | Sự kiện 1 (10:00): 会議😀"至急"<br>Sự kiện 2 (11:00): 定例MTG | - Yêu cầu xuất hoàn tất: hiện nút 「CSVダウンロード」, không kẹt ở 「CSV作成中」<br>- Mỗi dòng dữ liệu đúng 9 ô<br>- Dòng 1: ô 「スケジュールタイトル」 chứa 会議 và "至急" đúng thứ tự, dấu nháy hiện đúng 1 lần mỗi chỗ<br>- Dòng 2: 「スケジュールタイトル」 = 定例MTG, các ô khác đúng cột |  | Lấp Q2 · Abnormal vì emoji nằm ngoài bảng mã SHIFT-JIS — rủi ro encoder ném lỗi làm job ghi trạng thái lỗi · Cách hiển thị riêng ký tự emoji (mất / thành ?) là hành vi có sẵn, ngoài phạm vi fix — chỉ ghi nhận, không dùng để kết luận · Đánh giá spec: Spec không ghi · Evidence: file CSV + ảnh modal |
| TC-OUTEXPORT001-02 | Job | OUT-EXPORT-001 | Cài đặt chat 「チャット設定」 — CSV export — nội dung file | Normal | auto | dev, local, prd, staging | CSV lịch sử chat 1:1: tên friend chứa dấu nháy kép và dấu phẩy nằm đúng 1 ô 「送信者名」, không lệch cột | - Môi trường đã deploy bản fix của exporter chat 1:1 (Dev xác nhận ở I5)<br>- Bot B gói trả phí; friend F có tên hiển thị = 山田"太郎",様<br>- Trong 7 ngày gần nhất: F gửi 2 tin 「こんにちは」, 「予約したいです」; admin trả lời 1 tin 「承知しました」 trên màn Chat 1:1 「1:1チャット」<br>- Gắn tag 「T41972c」 cho F | 1. Mở Cài đặt chat 「チャット設定」 → tab Xuất CSV chat 「チャットのCSVエクスポート」 → sub-tab Tạo dữ liệu 「データ作成」.<br>2. Chọn ngày bắt đầu = hôm nay − 7 ngày, ngày kết thúc = hôm nay.<br>3. Thêm điều kiện lọc theo tag 「T41972c」.<br>4. Bấm 「エクスポート条件の確認に進む」 → bấm Bắt đầu 「作業開始」.<br>5. Chờ job xong, mở sub-tab Lịch sử tạo 「作成履歴」, bấm 「ダウンロード」.<br>6. Mở file bằng Excel tiếng Nhật. | Tên friend: 山田"太郎",様 | - Tải được file, không lỗi tải xuống<br>- Dòng tiêu đề cột đúng 5 ô: 「送信者タイプ」·「送信者名」·「送信日」·「送信時刻」·「内容」<br>- 3 dòng dữ liệu, mỗi dòng đúng 5 ô<br>- 2 dòng 「送信者タイプ」 = 友だち: 「送信者名」 = 山田"太郎",様 đúng nguyên văn (dấu nháy hiện 1 lần, dấu phẩy không tách cột)<br>- 「内容」 lần lượt = こんにちは / 予約したいです / 承知しました |  | Lấp G5 · Q5 · regression · dẫn từ kho TC-CST-113 (5 cột) · TC-CST-115 (送信者名) · Đánh giá spec: Đã hỏi leader (yêu cầu Leader 2026-10-05; spec chat-setting chưa quét tab CSV — kho MT-01) · File chat 1:1 là UTF-8 BOM (kho MT-20 / QA-030), khác 2 CSV SHIFT-JIS nên `"` phải giữ nguyên · Tên file per-friend chứa tên friend (TC-CST-125) — tên có `"` có thể bị đổi khi lưu trên Windows: ghi lại tên file thực tế, không dùng để kết luận · Evidence: file CSV + ảnh Excel |
| TC-OUTEXPORT001-03 | Job | OUT-EXPORT-001 | Cài đặt chat 「チャット設定」 — CSV export — nội dung file | Boundary | auto | dev, local, prd, staging | CSV lịch sử chat 1:1: nội dung chat chứa dấu nháy kép, dấu phẩy và xuống dòng nằm đúng 1 ô 「内容」 | - Môi trường đã deploy bản fix của exporter chat 1:1 (Dev xác nhận ở I5)<br>- Bot B gói trả phí; friend G tên hiển thị = テスト友だちG (không ký tự đặc biệt)<br>- Trong 7 ngày gần nhất có 4 tin theo dữ liệu nhập, gửi theo đúng thứ tự<br>- Gắn tag 「T41972d」 cho G | 1. Mở 「チャット設定」 → 「チャットのCSVエクスポート」 → 「データ作成」.<br>2. Chọn khoảng ngày hôm nay − 7 ngày ~ hôm nay, lọc theo tag 「T41972d」.<br>3. Bấm 「エクスポート条件の確認に進む」 → 「作業開始」.<br>4. Ở 「作成履歴」 bấm 「ダウンロード」.<br>5. Mở file bằng trình soạn thảo văn bản, xem dạng thô của 4 dòng dữ liệu.<br>6. Mở file bằng Excel tiếng Nhật. | Tin 1 (friend): 明日"10時",会議室A<br>Tin 2 (friend): "OK"<br>Tin 3 (friend, 2 dòng): 確認しました + xuống dòng + "了解"です<br>Tin 4 (admin): 了解です、"至急"対応します | - Đúng 4 dòng dữ liệu (tin 3 không bị tách thành 2 dòng), mỗi dòng đúng 5 ô<br>- 「内容」 khớp nguyên văn: 明日"10時",会議室A / "OK" / 確認しました⏎"了解"です / 了解です、"至急"対応します<br>- Dạng thô tin 1 = `"明日""10時"",会議室A"` (escape `"` → `""`)<br>- Excel: dấu nháy hiện đúng 1 lần, các ô 「送信者名」·「送信日」·「送信時刻」 không bị đẩy lệch |  | Lấp G5 · Q5 · regression · dẫn từ kho TC-CST-121 (escape `,` / `"`) + TC-CST-120 (nội dung nhiều dòng) · Đánh giá spec: Đã hỏi leader (yêu cầu Leader 2026-10-05) · Evidence: file CSV dạng thô + ảnh Excel |
| TC-OUTEXPORT001-04 | Job | OUT-EXPORT-001 | Quản lý CSV 「CSV管理」 — xuất CSV danh sách bạn bè | Boundary | auto | dev, local, prd, staging | CSV bạn bè: Thông tin bạn bè 「友だち情報」 chứa dấu nháy kép ở nhiều kiểu mục được đổi thành ? và không lệch cột | - Môi trường đã deploy nhánh fix, job Java xuất CSV bạn bè đang chạy<br>- Bot B có 3 Thông tin bạn bè 「友だち情報」: 41972_q_text (văn bản 1 dòng), 41972_q_memo (văn bản nhiều dòng), 41972_q_select (chọn 1, có lựa chọn 「"VIP"会員」)<br>- Friend H đã nhắn tin cho bot, giá trị 3 mục theo dữ liệu nhập; friend I (đối chứng) 3 mục không chứa dấu nháy<br>- Gắn tag 「T41972e」 cho H, I | 1. Mở Quản lý CSV 「CSV管理」 → bấm Tạo mới 「新規作成」.<br>2. Bấm Lọc 「絞込み」, lọc theo tag 「T41972e」.<br>3. Ở 「友だち情報」 chọn 3 mục 41972_q_text / 41972_q_memo / 41972_q_select.<br>4. Bấm 「この条件でCSVを作成・更新」, chờ nút 「CSVダウンロード」.<br>5. Tải file, mở bằng Excel tiếng Nhật. | H — 41972_q_text: 青"山",店<br>H — 41972_q_memo: 1行目"A" + xuống dòng + 2行目<br>H — 41972_q_select: "VIP"会員<br>I — 3 mục: 通常 / メモ / 一般会員 | - Đúng 2 dòng dữ liệu (memo nhiều dòng không tách dòng), mỗi dòng có số ô bằng dòng nhãn tiêu đề<br>- Dòng H: 「友だち情報_41972_q_text」 = 青?山,店 · 「友だち情報_41972_q_memo」 = 1行目?A? ⏎ 2行目 · 「友だち情報_41972_q_select」 = ?VIP?会員<br>- Dòng H: dấu phẩy trong 青?山,店 không tách cột<br>- Dòng I: 3 ô = 通常 / メモ / 一般会員 |  | Lấp G6 · Đánh giá spec: Đã hỏi leader — Leader xác nhận 2026-10-05 `"` bị đổi thành `?` ở CSV bạn bè. ⚠️ Mâu thuẫn C2 (§4): spec job-spec dòng 352 + NEW-18 ghi `"` được giữ và escape `""`; Dev chốt C2 xong mới chạy · Evidence: file CSV |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `csv-management/job/job-spec.md` §1.3 + câu hỏi mở #1 (flag production) · `Ghi chú` NEW-15..18 trên Studio | Chốt production đang sinh CSV bạn bè bằng job Java (`ENABLE_HANDLE_EXPORT_CSV`) hay Laravel command → sửa bên sai (spec hoặc ghi chú + `env_scope` TC) | C1 `CONF-SPEC` ở §4 | Dev |
| 2 | `csv-management/feature-spec.md` (format cột CSV bạn bè) + `job/job-spec.md` dòng 352 | Leader đã xác nhận 2026-10-05: CSV bạn bè đổi `"` thành `?`. Cần ghi vào spec, và chốt phạm vi áp dụng: **chỉ tên LINE** (code `HandleExportCsvTask.java:434`) hay **mọi trường** (システム表示名 · 個別メモ · 友だち情報) | C2 `CONF-SPEC` ở §4 · I4 | Dev |
| 4 | `chat-setting/feature-spec.md` (chưa có tab 「チャットのCSVエクスポート」 — kho FA-041 MT-01) | Ghi rule escape của CSV chat 1:1: trường chứa `"` / `,` / xuống dòng bọc `"..."`, `"` → `""`, encoding UTF-8 BOM | G5 · Q5 | Dev |
| 3 | `salon-booking/job/job-spec.md` §4.3 + `csv-management/job/job-spec.md` §4.1 | Rule mới của fix: ô có giá trị **đúng bằng** `null` → xuất rỗng ở cả 2 CSV (Studio REQ-011 — *"chờ PO xác nhận"*). Friend / sự kiện có tên đúng là "null" sẽ mất giá trị trong file | NEW-9 · TC-OUTEXPORT001-01 | PM |
