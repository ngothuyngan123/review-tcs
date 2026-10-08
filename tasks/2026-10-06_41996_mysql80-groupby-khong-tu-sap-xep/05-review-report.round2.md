# 05 — Review Report (round 2)

> Draft cho Leader verify. Round 2 — review bộ TC Studio task #369 (ticket #41996) sau 4 lượt bàn giao của Dev (v1 → v4, nhánh `ai_studio_implement_41996` @ `d9359107f6`).
> `03-dev-impact.md` vẫn là bản đánh giá gốc (journal #140123). Phần Dev sửa thêm ở v1–v4 (D-1 → D-8) lấy từ journal Redmine #140732 → #141002 và Studio `dev_impact`.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #369 (round 2, `status = done-ai`, `aiResult = fail`, branch `ai_studio_implement_41996`) |
| Tổng số TC review | 65 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 | 24/33 mục có TC đạt (`BUG` + F1–F19 + T1–T15, trừ F9 / T10 — IG-01 Booking Manager cũ) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` + bàn giao v1–v4 | 21/31 điểm có TC đạt (20 file, trừ `BookingManagerController.php` — IG-01 · 7 thay đổi hành vi D-1, D-2, D-4, D-5, D-6, D-7, D-8 · 4 rủi ro: hành vi trên MySQL 8, hiệu năng, cache JS, số đếm đã lưu từ trước) — **CHƯA ĐỦ** |

**Kết luận**: 1 GAP · 4 RISK. So với round 1, các sửa D-1 (API export 「ブロックされた友だち」), D-2 (bộ đếm kịch bản), D-4 (bảng URL分析) và D-6 (courseList lịch bài học) đều đã có TC **pass trên đúng code** — đã đóng.

**Lý do chính các mục còn lại chưa đạt: lượt chạy #2841 và #2859 chạy trên code cũ.** Studio ghi 2 lượt này checkout `ai_studio_implement_41996_v1` @ `7d829abd`. Bản này **thiếu 5 commit** của v2 → v4: `8afb8bd4d5`, `962e17c5d9`, `70bfc2d1dd`, `8c5e26fbd7`, `d9359107f6` (bug #42334). Mọi kết quả `fail` / `error` của 2 lượt này **không phải kết luận về bản fix**.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — GROUP BY không còn tự sắp xếp **trên MySQL 8** | `dev-impact` + `diff code` | NEW-42, NEW-43, NEW-44, NEW-48 (đều `skip`), NEW-45 (`pass`) | **RISK** — Vẫn chưa có env MySQL 8. Lượt #2859 dò: DB runner là `MySQL 5.6.51`, không có host MySQL 8 nào, nên 4 TC skip. **NEW-45 được đánh `pass` tay** (loantt, 2026-10-08 05:30, không có run, không có evidence) dù tiền điều kiện là `SELECT VERSION() = 8.0.x`, và lượt #2859 chạy 1 giờ trước đó vừa skip chính TC này vì không có MySQL 8. Toàn bộ 50 TC pass đều chạy trên 5.6, nên chỉ chứng minh "không lỗi SQL, thứ tự = cột GROUP BY tăng dần". **Chưa chứng minh được bản fix sửa đúng lỗi MySQL 8.** | `[BLOCKER]` |
| G2 | F18 / T13 + D-5 — 支払い報酬: sắp 「報酬額」 ở server, 会計用CSV cùng thứ tự (`SupperAdminController.php`, `affiliater.js`) | `dev-impact` + `diff code` | NEW-40, NEW-61, NEW-62, NEW-63, NEW-64, NEW-65 | **RISK** — Cả 6 TC chạy ở lượt #2841 trên code v1, chưa có D-5. Log của #42331 / #42332 ghi rõ "bấm 「報酬額」: KHÔNG có XHR", tức JS cũ, sắp ở trình duyệt. Vì vậy NEW-40 / 62 / 63 `fail`, NEW-61 / 65 `error`, và **#42300 bị Re-open oan**. **Chưa có kết quả nào trên code D-5.** Đây là CSV kế toán khách dùng để chuyển khoản. | `[MAJOR]` |
| G3 | F3 / T3 `FriendlistController` — (i) D-8 sắp theo tin cuối ở lọc nâng cao cũ · (ii) `csvExport` 4 nhánh | `dev-impact` + `diff code` | (i) NEW-6 · (ii) chỉ còn NEW-45 | **RISK + GAP**. **(i)** NEW-6 `fail` ở #2841 trên code v1, chưa có D-8, nên #42248 Re-open oan. Hành vi mới của v4 (bạn chưa có hội thoại **vẫn có trong danh sách**, đứng cuối khi `desc`, đứng đầu khi `asc`, `total` bằng lúc không sắp) **không TC nào kiểm** → GAP. **(ii)** NEW-8, NEW-9 (export CSV 友だちリスト chọn tay / theo lọc, 2 khối `type_filter`) **đã bị xoá khỏi task**. Export của 友だちリスト chỉ còn NEW-45, mà NEW-45 đòi MySQL 8 (xem G1). → **4 nhánh `csvExport` không còn TC regression chạy được trên env hiện có.** | `[MAJOR]` |
| G4 | F14 / T11 + D-7 — bảng URL分析 hiện 「0回クリック」 khi URL chưa có click (`detail_setting.blade.php`) | `diff code` | NEW-67 (`error`) | **RISK** — NEW-67 chạy ở #2841 trên code v1, chưa có commit `962e17c5d9`, nên `error` "không chấm được". Chưa có kết quả. | `[MINOR]` |

Không đề xuất TC mới cho G1, G2, G4 vì TC đã có, chỉ cần **chạy lại đúng code / đúng env** (xem §5 I1, I2). G3 có 2 TC đề xuất ở §7.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 17 quan điểm có Trigger khớp task · 13 đã cover đủ về thiết kế · 4 dòng thiếu.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `ENV-003` ★ · `PERF-LARGE-001` | Cao | **RISK** — trùng G1. Cả TC tái hiện (NEW-42, NEW-43, NEW-44, NEW-45) và TC đo hiệu năng (NEW-48) đều cần DB MySQL 8; riêng NEW-48 cần dữ liệu quy mô thật (máy B). Runner hiện chỉ có 5.6. Không đẻ thêm TC; cần người cấp DB MySQL 8 cho slot test (§5 I2). | `[BLOCKER]` |
| Q2 | `DEPLOY-ASSET-001` ★ | Cao | **RISK** — release sửa JS (`affiliater.js`) và Blade (`detail_setting.blade.php`). Chỉ có NEW-65 (Abnormal, `error` vì sai nhánh). Thiếu Normal (sau `view:clear` + tăng `sns-line.version`, trình duyệt nạp JS và view mới). Dev **không tăng `?v=`** của `affiliater.js` mà chỉ dặn tester Ctrl+F5. Nếu release không tăng version thì khách đang mở màn 支払い報酬 vẫn dùng JS cũ và CSV vẫn lệch thứ tự. Quyết định ở §8 #3. | `[MAJOR]` |
| Q3 | `REG-SHARED-001` | Cao | **GAP (giữ từ round 1)** — Dev bàn giao v1 → v4 có liệt kê nhiều mục "quét ngang, chưa sửa" nhưng **vẫn chưa có số ticket** nào. Các mục chưa có ticket: lọc nâng cao v2 inner join bỏ bạn chưa có hội thoại · `order[column]` của API aff-transfer đưa thẳng vào ORDER BY · `AffTransferExport` lazy-load bill không lọc tháng · lệnh recover `RecoverCountFriendFollowScenatio` và job ±1 đếm theo bản ghi, khác cách đếm mới của `countScenario`. Câu hỏi round 1 về luồng **gửi tin / bulk action > 200** có chia lô trên kết quả GROUP BY hay không **chưa được trả lời**. | `[MAJOR]` |
| Q4 | `FUNC-001` · `FUNC-004` · `DATA-COUNT-001` · `OUT-EXPORT-001` · `MSG-USER-001` | Cao | **RISK — RULE-01**: bộ 65 TC có 2 Abnormal (NEW-53, NEW-65), cả hai thuộc quan điểm khác. Leader đã chốt round 1 là không bổ sung Abnormal cho phân trang → chỉ còn việc member ghi lý do "fix chỉ thêm ORDER BY, không có input mới" vào `Ghi chú` của các quan điểm này. | `[MINOR]` |

Mã Studio lạ ở round 2 (`UI-TABLE-001`, `SEC-INJECT-001`, `TOOL-OLDREC-001`, `RULE-TOOL-029`, `API-CONTRACT-001`…) đều có TC nội dung đúng, nên không gây GAP thêm. Q2 là chỗ duy nhất quan điểm Cao chỉ còn 1 TC.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| D1 | NEW-46 | NEW-35 | `DUP-SUBSET` (sau khi sửa expected ở §4 C1) | `DATA-COUNT-001` · Normal · xoá 1 step ở màn step kịch bản rồi đọc 3 cột đếm · dữ liệu 3 trạng thái, 1 bạn có 2 bản ghi | `[MINOR]` |
| D2 | NEW-61 + NEW-64 | NEW-40 | `DUP-SUBSET` | `LIST-001` / `OUT-EXPORT-001` · Normal · tab 支払い報酬: sắp 「報酬額」 rồi xuất 会計用CSV · tiền đề nhiều affiliater, 2 người cùng số tiền. Phần "không sắp → theo mã người dùng" của NEW-40 chưa có ở NEW-64 → **gộp** phần này vào NEW-64 trước khi xoá NEW-40 | `[MINOR]` |

Đã rà 65 TC. Các cặp dễ nhầm nhưng không trùng:
- NEW-33 ↔ NEW-51: 1 URL / nhiều URL + URL không đăng ký.
- NEW-46 ↔ NEW-57 ↔ NEW-58 ↔ NEW-59: xoá step / xoá filter / API app / dữ liệu đếm cũ.
- NEW-10 ↔ NEW-44: MySQL 5.6 / MySQL 8.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-TC` + `CONF-SPEC` | NEW-35, NEW-36, NEW-37 vs NEW-46, NEW-57, NEW-58, NEW-59 | Giá trị 3 cột đếm kịch bản sau khi gọi `countScenario` (xoá step / lệnh recover) | NEW-35 / 36 / 37: "giống base" = **số dòng của nhóm bạn ID nhỏ nhất** (2/3/1 · 1/0/0 · 2/1/0) | NEW-46 / 57 / 58 / 59: **số bạn khác nhau** theo trạng thái · spec `scenario/feature-spec.md` §3 (「Số bạn đang theo dõi (N人)」) · Dev D-2 (v1) đổi `countScenario` sang đếm bạn khác nhau · bug #42333 (AI tự kết luận "TC chờ cập nhật") | (1) NEW-35 / 36 / 37 viết theo hành vi cũ trước D-2 → **TC cần sửa** (khả năng gần như chắc chắn: kết quả thực tế 3/2/2 · 2/0/0 · 1/3/0 đúng bằng số bạn) · (2) Leader muốn giữ hành vi 5.7 → D-2 phải revert (trái spec §3) | `[MAJOR]` | Leader |
| C2 | `CONF-SPEC` | NEW-49 | CSV管理 với điều kiện khớp 0 bạn | `Kết quả mong đợi`: "job xử lý xong, 対象人数 = 0人, nút 「作成中」 disabled, không chuyển sang 「CSVダウンロード」" | Steps bước 2–3 của cùng TC vẫn là "Chờ trạng thái chuyển sang có nút 「CSVダウンロード」 · Tải file, mở". Spec `csv-management/feature-spec.md` dòng 146: `filter_update_status == 30` **và** `total_line_user == 0` → 「作成中」 disabled | (1) Expected đúng spec, steps chưa sửa theo → TC không chạy được tới bước 3 · (2) Steps đúng (phải tải được file rỗng), spec / expected sai | `[MAJOR]` | Leader |
| C3 | `CONF-SPEC` (giữ từ round 1 C2) | NEW-3, NEW-50 | Thứ tự tag ở 「未分類」 khi tìm theo từ khoá ở タグ管理 | NEW-3: thứ tự tạo (`tags.id`) · NEW-50: bước 3 "chờ Leader chốt" | `tag-management/feature-spec.md` BR-15: tag sắp theo `position` | (1) Kết quả tìm kiếm theo `id` (như bản fix) · (2) Theo `position` như danh sách thường. **NEW-50 đang `pass` dù expected bước 3 chưa có giá trị chốt** → kết quả pass không có nghĩa | `[MINOR]` | Leader |
| C4 | `CONF-IGNORE` | không có TC (NEW-31 đã xoá khỏi task) | F9 / T10 ở `03-dev-impact.md` · `BookingManagerController.php` (+7) trong diff · Studio `dev_impact` dòng "booking manager" | — | `ignore-features.md IG-01 — Booking Manager cũ đã bỏ` | Đánh giá ảnh hưởng ghi tính năng đã bỏ → không tạo TC bổ sung | `[MINOR]` | Dev |

**Đã rà**: 65 TC × các nguồn sau. Kho chưa có FA-014 / FA-017 / FA-024 / màn super admin, nên các TC của những màn này không đối chiếu kho được.
- spec: `scenario/feature-spec.md` §3 / §6 · `csv-management/feature-spec.md` (BR-09, bảng nút) · `tag-management/feature-spec.md` BR-15
- kho: `kho-tcs/fa009-*` (Bộ đếm friend, MT-01) · `fa012-*` (Count người gắn tag) · `fa021-*` (`TC-EBK-313/314`)

C1 – C3 kèm 1 dòng ở §8. C4 không sinh §8.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Lượt #2841, #2859 — 17 TC: NEW-6, NEW-35 → 37, NEW-39, NEW-40, NEW-42 → 45, NEW-48, NEW-61 → 67 | **Chạy trên code sai nhánh**: runner checkout `ai_studio_implement_41996_v1` @ `7d829abd` (override), không phải HEAD `d9359107f6`. Hệ quả: #42248, #42300 bị Re-open oan; #42331, #42332 được tạo từ code cũ. Tỷ lệ pass hiện tại 50/65 (77%) chưa phản ánh bản fix. | Deploy đúng `d9359107f6` lên slot test, reload PHP-FPM / opcache, chạy `php artisan view:clear`, rồi chạy lại 17 TC trên. Đóng #42334 sau khi xác nhận. Chuyển #42331 / #42332 về trạng thái chờ chạy lại, không giao Dev sửa. |
| I2 | `[MAJOR]` | Toàn bộ 65 TC chỉ chạy `local` (MySQL 5.6.51) | **RULE-08 / ENV-003**: task chạm job nền (`handle:export_csv`, job step kịch bản, lệnh recover) mà 0 TC chạy prd, và không có env MySQL 8. | Cấp DB MySQL 8.0 (host + dump `sns_line`, quyền ghi) cho slot test theo đúng yêu cầu ghi ở kết quả #2859, rồi chạy NEW-42 / 43 / 44 / 45. NEW-48 cần quyền đọc máy B. |
| I3 | `[MAJOR]` | NEW-45 | Đánh `pass` tay không có run, không có evidence, trong khi tiền điều kiện (`SELECT VERSION() = 8.0.x`) không đạt được trên env hiện có. Lượt #2859 chạy trước đó 1 giờ đã skip chính TC này vì thiếu MySQL 8. | Người chạy (loantt) bổ sung evidence: kết quả `SELECT VERSION()` + 5 file CSV. Không có thì đổi về chưa chạy. |
| I4 | `[MAJOR]` | Nhóm `api`: NEW-5, NEW-6, NEW-7, NEW-15, NEW-16, NEW-32, NEW-58, NEW-60, NEW-66 | **RULE-13 (giữ từ round 1)**: `Kết quả mong đợi` không ghi mã HTTP. Riêng NEW-6: v4 trước đây trả `HTTP 200 success=false` khi lỗi SQL, nên expected phải ghi rõ cả `HTTP 200` **và** `success=true`. | Bổ sung mã HTTP cho mọi lần gọi. |
| I5 | `[MAJOR]` | Toàn bộ 65 TC | `Trạng thái đánh giá spec` vẫn trống (giữ từ round 1). Quy tắc thứ tự (ID / collation / bản ghi URL tạo trước / sắp 報酬額 theo số đã đổi…) lấy từ ticket và Dev, spec không ghi. | Leader chốt §8 #4 rồi đánh `Đã hỏi leader` trên Studio. |
| I6 | `[MAJOR]` | Màn super admin 支払い報酬, API aff-transfer | Dev ghi `order[column]` của API aff-transfer **đưa thẳng vào ORDER BY** (nguy cơ SQL injection ở màn super admin), và D-5 vừa chạm đúng API này. Dev xếp "ngoài phạm vi" nhưng chưa có ticket. | Leader mở ticket riêng (whitelist cột sắp) trước khi đóng #41996. Không đẻ TC trong task này. |
| I7 | `[MINOR]` | `03-dev-impact.md` · Studio `spec_delta` | (1) File 03 chưa có các sửa v1 → v4 (D-1 → D-8, thêm 2 file `affiliater.js`, `detail_setting.blade.php`). (2) Studio `spec_delta` tính lúc 2026-10-07 10:17, `FriendlistController.php` vẫn +11 dòng. Bàn giao v4 (`d9359107f6`) thêm +6 dòng ở file này, tức diff Studio chưa gồm D-8. | Bổ sung mục 2 / 4.1 / 4.3 file 03 theo bàn giao v4. Tính lại `spec_delta` trên Studio. |
| I8 | `[MINOR]` | Bộ đếm kịch bản — luồng huỷ hợp đồng (`StepMessageSpec`) | Dev kê luồng huỷ hợp đồng là 1 trong các nơi gọi `countScenario`, nhưng không nêu thao tác nào trên UI dẫn tới luồng này. Các nơi gọi khác (xoá step, xoá filter, app mobile, job lưu step, lệnh recover) đều đã có TC. | Dev nêu cách kích hoạt; nếu có lối vào thật thì bổ sung 1 TC, không có thì ghi "code chết". |
| I9 | `[MINOR]` | #23800 | Giữ từ round 1: dẫn chiếu "kho FL-116" không tra được (kho hiện tại `TC-FRL-116` là case bulk action); bước 3 "Gọi API danh sách bạn bè" chưa ghi endpoint; tag mang số ticket khác (`TC38336_COUNT`). | Sửa nguồn kho, ghi endpoint cụ thể, đổi tên dữ liệu theo #41996. |
| I10 | `[NIT]` | NEW-59 | Expected bước 1 ghi số đếm cũ giữ nguyên ("Dev: số đã lưu không tự đổi"). Nếu Leader quyết chạy lệnh recover sau deploy (§8 #2) thì expected này đổi. | Sửa sau khi chốt §8 #2. |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 65 TC — không có TC nào ngoài phạm vi task.
- NEW-56 (エラーリスト v2 không đổi) và NEW-66 (API lịch chế độ ngày không đổi) là regression dẫn từ bàn giao v2 / v3 của Dev ("màn v2 không đổi", "chế độ day không đổi").
- NEW-31 (Booking Manager cũ) đã xoá khỏi task.

---

## 7. TCs đề xuất bổ sung (2)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa013-friendlist-友だちリスト.md` (bảng Coverage; nhóm 2 「Sắp xếp & phân trang」 `TC-FRL-09/10`; nhóm 4 「Lọc nâng cao 絞り込み」) |
| Vùng regression phát hiện từ kho | Không có thêm. `TC-FRL-09/10` là sắp theo 友だち追加日時 ở màn v2, không phải sắp theo tin cuối của EP-06 cũ. |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | Không có TC R |
| Xác nhận chống trùng | Đã đối chiếu 65 TC ở BƯỚC 0 + `fa013`, **không TC đề xuất nào trùng**. TC-LIST001-02 khác NEW-6 ở dữ liệu "bạn chưa có hội thoại" và tiêu chí vị trí đầu/cuối. TC-OUTEXPORT001-02 khác NEW-45 ở chỗ không đòi MySQL 8 và kiểm đủ 2 khối `type_filter`. |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-LIST001-02 | API | LIST-001 | Friend list 友だちリスト: lọc nâng cao cũ (EP-06) sắp theo tin nhắn cuối 最終メッセージ | Boundary | auto | dev, local, staging | Lọc nâng cao cũ sắp theo thời điểm tin nhắn cuối: bạn chưa có hội thoại vẫn có trong danh sách, đứng cuối khi giảm dần, đứng đầu khi tăng dần, tổng không đổi | - Đăng nhập admin bot B qua 「/login-v2」 (có session + CSRF)<br>- App chạy nhánh `ai_studio_implement_41996` từ commit `d9359107f6` trở lên<br>- Tag 「QA41996-LT」 gắn cho đúng 5 bạn F01…F05<br>- F01, F02, F03 đã có hội thoại với bot B, thời điểm tin nhắn cuối lần lượt 2026-10-01 09:00 / 10:00 / 11:00<br>- F04, F05 kết bạn nhưng **chưa có hội thoại** với bot B (chưa từng nhắn, bot chưa gửi tin)<br>- F01 có thêm hội thoại ở bot khác C với thời điểm tin cuối 2026-10-05 (mới hơn mọi tin ở bot B) | 1. Gọi `GET /basic/friendlist/advance-filter` với điều kiện tag 「QA41996-LT」, page = 1, không truyền tham số sắp xếp; ghi `total` và danh sách bạn.<br>2. Gọi lại cùng điều kiện, thêm `sort_last_time_increase=desc`; ghi thứ tự.<br>3. Gọi lại với `sort_last_time_increase=asc`; ghi thứ tự. | Tag QA41996-LT: F01, F02, F03 có hội thoại · F04, F05 chưa có hội thoại · F01 có tin mới hơn ở bot C | - Bước 1: HTTP 200, `success=true`, `total = 5`<br>- Bước 2: HTTP 200, `success=true`, `total = 5`; thứ tự F03 → F02 → F01 → F04 → F05 (F04, F05 chưa có hội thoại nên đứng cuối; giữa F04 và F05 theo ID bạn bè tăng dần)<br>- Bước 3: HTTP 200, `success=true`, `total = 5`; thứ tự F04 → F05 → F01 → F02 → F03<br>- Thứ tự của F01 tính theo tin cuối ở bot B (09:00), không theo tin 2026-10-05 ở bot C | | Lấp G3 (i) · hành vi mới của D-8 (bàn giao v4, điểm test A18) · nhóm API vì gửi request trực tiếp; Dev xác nhận JS hiện không gửi `sort_last_time_increase` nên không có thao tác UI · không chạy prd vì phải dựng hội thoại ở 2 bot · Đánh giá spec: Spec ghi rõ tham số hợp lệ (friend-list EP-06), spec không ghi vị trí bạn chưa có hội thoại — theo bàn giao Dev · Evidence: response JSON 3 lần gọi |
| TC-OUTEXPORT001-02 | UI | OUT-EXPORT-001 | Friend list 友だちリスト: export CSV xuất CSV — chọn tay và theo điều kiện, trước/sau 絞込み | Normal | auto | dev, local, staging | Export CSV ở 友だちリスト ở cả 4 nhánh (chọn tay / theo điều kiện × chưa lọc / sau 絞込み): đủ dòng, không lặp, thứ tự giống bản trước fix | - Đăng nhập admin bot B<br>- Bot B có 12 bạn F01…F12 đang theo dõi, kết bạn theo đúng thứ tự số (F01 sớm nhất)<br>- Tag 「QA41996-EXP」 gắn cho F03, F07, F09, F11 theo thứ tự F11 → F09 → F07 → F03<br>- F09 đã chặn bot | 1. Mở 「友だちリスト」, chưa áp 絞込み, tick lần lượt F08, F02, F05; bấm export CSV, tải file A.<br>2. Bỏ tick, chọn xuất toàn bộ bạn (theo điều kiện, chưa lọc); export, tải file B.<br>3. Bấm 「絞込み」 → điều kiện tag 「QA41996-EXP」 → áp dụng; ghi 「検索結果：N人」.<br>4. Tick lần lượt F11, F03; export, tải file C.<br>5. Bỏ tick, chọn xuất theo điều kiện; export, tải file D.<br>6. Lặp bước 1–5 trên bản trước fix `release_step_20260930_v2` (cùng DB), ghi thứ tự 4 file. | 12 bạn · 3 bạn chọn tay chưa lọc · tag 4 bạn (1 bạn chặn bot) · 2 bạn chọn tay sau lọc | - File A: đúng 3 dòng F02, F05, F08 (không theo thứ tự tick)<br>- File B: số dòng bằng số bạn hiển thị khi chưa lọc, không lặp<br>- File C: đúng 2 dòng F03, F11<br>- File D: số dòng bằng 「検索結果」 ở bước 3 (cách tính bạn chặn bot giống bản trước fix), không lặp<br>- Thứ tự dòng của cả 4 file **giống hệt** bản trước fix ở bước 6<br>- Header và cột của 4 file giống bản trước fix; mọi lần export không thông báo lỗi | | Lấp G3 (ii) · thay cho NEW-8 / NEW-9 đã bị xoá — nếu Leader cố ý xoá 2 TC này thì bỏ TC đề xuất này · không chạy prd vì bước 6 phải chạy bản trước fix trên cùng DB · chạy được trên MySQL 5.6 (regression, so với bản trước fix chạy 5.6). Thứ tự trên MySQL 8 đã do NEW-45 kiểm · Đánh giá spec: Spec không ghi thứ tự dòng CSV · Evidence: 8 file CSV (4 file × 2 bản) |

G1, G2, G4: không đề xuất TC mới — TC đã có (NEW-42 → 45, NEW-48 · NEW-40, NEW-61 → 65 · NEW-67), chỉ cần chạy lại đúng code / đúng env theo §5 I1, I2.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `scenario/feature-spec.md` §3 + §6 · kho FA-009 `MT-01` · NEW-35 / 36 / 37 | (a) Xác nhận 3 cột đếm = số bạn khác nhau theo trạng thái (theo D-2), rồi sửa expected NEW-36 (2/0/0) và NEW-37 (1/3/0), xoá NEW-35 (§3 D1). (b) Chốt ánh xạ `is_following` 0/2 ↔ 読了済 / 途中で終了 (kho MT-01 còn chờ). | §4 C1 · #42333 | Leader |
| 2 | `scenario/web/logic-spec.md` BR-10 | Ghi rõ 3 cách đếm đang cùng tồn tại: `countScenario` (số bạn) · job ±1 · lệnh recover `RecoverCountFriendFollowScenatio` (số bản ghi). Chốt có chạy recover toàn hệ thống sau deploy để sửa số đếm đã lưu sai hay không (ảnh hưởng expected NEW-59). | Bàn giao v1 của Dev · §5 I10 | Leader / PM |
| 3 | Quy trình release (không phải spec) | Chốt có tăng `sns-line.version` (config `sns-line.php`) khi release để `affiliater.js` mới được nạp. Không tăng → NEW-65 chắc chắn FAIL và khách đang mở màn vẫn bị CSV lệch. | §2 Q2 · bàn giao v3 / v4 | Leader / đội release |
| 4 | `friend-list` EP-06 · `tag-management` · `friend-filter` · `friend-information` · `qr-landing` · `event-booking` · `csv-management` · màn super admin 支払い報酬 | Ghi quy tắc thứ tự mặc định + khoá phụ (giữ từ round 1 §8 #3), thêm 2 điểm mới: sắp 「報酬額」 theo số đã đổi (`報酬額の変更`) và vị trí bạn chưa có hội thoại khi sắp theo tin cuối | §5 I5 | Dev / Leader |
| 5 | `tag-management/feature-spec.md` BR-15 | Giữ từ round 1 §8 #2: kết quả tìm tag theo từ khoá ở 「未分類」 sắp theo `position` hay `tags.id` → rồi điền expected bước 3 của NEW-50 | §4 C3 | Leader |
| 6 | `csv-management/feature-spec.md` (bảng nút, dòng 146) | Xác nhận: điều kiện khớp 0 bạn → job xong (`status = 30`) nhưng nút vẫn hiện 「作成中」 disabled, không có 「CSVダウンロード」. Đây là hành vi đúng hay cần nút riêng cho trường hợp 0 người — rồi sửa steps NEW-49 | §4 C2 | Leader |
