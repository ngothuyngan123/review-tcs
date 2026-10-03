# 05 — Review Report (round 3)

> Draft cho Leader verify. Ticket #41448 · Studio task #339 · review lại 2026-10-02 sau khi Dev vá thêm **2 bug MỚI** (#41822/#41823, commit `7087f665bd` → `a4c92a8626`) phát hiện qua chính TC đề xuất ở report round 2. Report trước: `05-review-report.md` (round 1) · `05-review-report.round2.md` (round 2).
>
> **Đã đọc comment của Leader để lại trên Studio trong quá trình review** (5 TC có `provenance.source = human`, `actor = ngannt@mcp`) — liệt kê ở mục "Comment Leader đã để lại" ngay dưới §0.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #339 (ticket 41448, round 1, branch `ai_fixbug_41448`) |
| Tổng số TC review | 77 |

### Comment Leader đã để lại trên Studio (đọc qua `testcase_get_history` / note) — đã incorporate vào review này

| TC | Nội dung comment Leader | Trạng thái |
|---|---|---|
| `NEW-32` (TC-FUNCDATE001-11) | Sửa dữ liệu boundary theo constraint thực tế: course trên UI chỉ tăng/giảm theo bước 5 phút (5,10,...,45), không dùng 1'/59' | Đã áp dụng — pass prd |
| `NEW-40` (TC-REGSHARED001-03) | Sửa theo nghiệp vụ thực tế: màn admin 予約カレンダー không có bước chọn Course → không áp oracle slot-2h của LIFF. Không trùng NEW-3/NEW-46 (2 TC đó kiểm job, TC này kiểm UI calendar admin) | Đã áp dụng — pass prd, **được xác nhận đúng** qua việc Dev reject bug #1509 (xem §4 C2) |
| `NEW-41` (TC-FUNC001-01) | Đây là POST-RELEASE CONFIRMATION, không phải regression chạy trước release. Chưa release / chưa có quyền account khách → trạng thái Skip/Blocked, **không tính là fail** | Đúng hiện trạng — vẫn `skip` |
| `NEW-66` (TC-FUNC004-11, **TC do chính round 2 đề xuất — G5**) | Map trực tiếp REQ-010 của vòng fix `a4c92a8626`. TC này **từng FAIL trên production** trước vòng fix mới: chưa có booking nhưng lượt đầu đã báo 「予約がいっぱいです」. Retest bắt buộc trên build chứa `a4c92a8626` | **Xem §1 — đây chính là bug #41822/#41823 mới, cần retest để đóng** |
| `NEW-67` (TC-FUNCDATE001-13) | Normal control cho REQ-010: xác nhận 1 lượt đặt hợp lệ trên lịch 個人 qua luồng không thanh toán được giữ lại sau recheck. Dùng cùng regression #41743 / commit `a4c92a8626` | Đã chạy — pass staging |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 + mục 4.4 mới (F10/F11, T10/T11, REQ-008/009/010) | 9/12 mục mới + cũ có TC Đạt · 1 đang **fail chờ retest** (REQ-010/G5) · 2 RISK (TC có nhưng chưa chạy) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` (computedAt 2026-10-02, diff `a4c92a8626` vs `release_step_20260930`, 2 file prod) | Cả 2 rủi ro Dev tự nêu đều **đã có TC**: "lịch 個人 nay xét nhánh 指名なし" → NEW-66/67/74; "rủi ro mở oan khung đầu ca 合算をする" → NEW-71 (đối chứng âm). **Nhưng NEW-70→74 (5 TC) chưa chạy lần nào** — **CHƯA ĐỦ** |

**Kết luận round 3**: Toàn bộ G1–G4 của round 2 **đã đóng có evidence Đạt trên staging/prd** (xem bảng dưới). G5 (calendar 個人) **đã bắt được bug thật** (#41822/#41823) — đúng như cảnh báo `[BLOCKER]` ở round 2 — và Dev đã vá (`a4c92a8626`); còn thiếu bước retest để đóng vòng lặp. Phát sinh **1 vùng mới** (G6: nhánh 合算をする/合算しない không nhận #41742) do chính commit vá bug mới gây ra — Dev đã tự viết đủ 5 TC (NEW-70–74) nhưng **chưa chạy**.

| G (round 2) | Trạng thái round 3 |
|---|---|
| G1 — Option 2 (上限を設定しない) thiếu cổng mới | ✅ Đóng — `TC-FUNC004-06/07` (NEW-58/59) pass. ⚠️ chỉ chạy `local`, chưa staging/prd — xem §5 I1 |
| G2 — 合算をする thiếu Abnormal (khoảng hở / nối ca bận) | ✅ Đóng — `TC-FUNC004-08/09` (NEW-60/61) pass. ⚠️ chỉ chạy `local` |
| G3 — nhánh 指名 chưa kiểm NV khác tan ca trong 片付け | ✅ Đóng — `TC-FUNCDATE001-12` (NEW-62) **pass prd** |
| G4 — happy-path thanh toán Stripe/UnivaPay | ✅ Đóng — `TC-PAYSTATE001-01/02` (NEW-63/64) **pass prd** |
| G5 — Calendar 個人 (0 TC ở round 1+2) | ⚠️ **TC đã bắt được bug thật #41822/#41823** (`TC-FUNC004-11` fail staging+prd 3 lần) → Dev vá `7087f665bd`/`a4c92a8626`. **Cần retest để đóng** — xem G5' dưới |

### GAP / RISK mới của round 3

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G5' | **Retest bug #41822/#41823 sau vá** — `TC-FUNC004-11` (NEW-66) đang ở trạng thái `last_exec = fail` (từ trước khi vá), bug Studio #1822 đang `stale` (chưa re-verify) | `dev-impact` (REQ-010) | `TC-FUNC004-11` (NEW-66), `TC-FUNC004-10` (NEW-65, hiện `error`), `TC-FUNCDATE001-13` (NEW-67, đã pass) | **RISK** — chưa có lần chạy nào xác nhận build chứa `a4c92a8626` sửa đúng cả 2 hướng: (a) không còn chặn oan lượt 2/3 do đếm hai lần, (b) hạn mức vẫn chặn đúng khi thật sự đầy. Run `local` #2542 đang chạy lúc viết report này — chưa có kết quả | `[BLOCKER]` |
| G6 | Nhánh **KHÔNG** nhận thay đổi #41742 (合算をする + 指名, 合算しない + 指名なし) phải giữ đúng hành vi đầu ca (REQ-009) + nhánh **CÓ** nhận (合算をする + 指名なし, REQ-008) | `diff code` | `TC` Dev tự viết: `NEW-70` (合算をする+指名なし đúng giờ vào ca BẬT), `NEW-71` (đối chứng âm: người vào ca đã bận), `NEW-72` (合算をする+指名), `NEW-73` (合算しない+指名なし), `NEW-74` (個人 đồng thời, hạn mức 1/2) | **RISK — đủ TC (5/5), nhưng 0/5 đã chạy**. Không cần đẻ TC mới (đã đủ N/A/B theo đúng yêu cầu Dev), chỉ cần chạy. Xem §5 I2 | `[MAJOR]` |

> G5' và G6 không cần TC mới — đã có TC sẵn (do chính Dev/pipeline viết sau khi điều tra bug), chỉ còn thiếu bước **chạy**.

### GAP mới phát hiện qua soi ma trận channel × option × vị trí × nghỉ (Leader yêu cầu 2026-10-02)

| # | Vùng thiếu | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|
| G7 | **Admin book (web + mobile) × 5/6 nhóm option** — chỉ Option 3 staff có TC qua admin-web (`NEW-3/40/54`) và admin-mobile (`NEW-46`); Option 1.1/1.2/2 staff và CẢ 2 option private **0 TC** qua 2 kênh này. Leader chốt trực tiếp 2026-10-02: admin book chỉ bị chặn bởi **course off / staff off / ngày nghỉ / Google block**, các ràng buộc khác (kể cả vượt `受付上限`) đều bypass | `NEW-3`, `NEW-40`, `NEW-46` (chỉ test job-assignment/grid-display ở option 3, không test 4 điều kiện chặn hay bypass limit) | **GAP** — chưa TC nào xác nhận đúng 4 điều kiện chặn + hành vi bypass limit, ở cả 2 kênh × cả 2 loại calendar | `[BLOCKER]` |
| G8 | **Booking qua ngày (overnight) × Option 1.1/1.2/2 staff + Option 2/3 private** — chỉ Option 3 staff có TC qua ngày (`NEW-6/29/30`) | Không có | **GAP** — rủi ro off-by-one ở mốc nửa đêm chưa được xác nhận ngoài option 3; đặc biệt Option 1.2 (tiếp sức) qua ranh giới ngày là case rủi ro cao nhất (2 nhân viên khác ngày) | `[MAJOR]` |
| G9 | **Calendar 個人 Option 3 × vị trí đầu ca** — `NEW-67` chỉ cuối ca, `NEW-69` chỉ giữa ca, `NEW-74` không gắn vị trí cụ thể | Không có | **GAP** — nghỉ trước (chuẩn bị) ở calendar 個人 chưa được xác nhận có tràn qua trước giờ mở cửa giống calendar nhiều nhân viên (`NEW-50/54`) | `[MAJOR]` |

§7 round này = **(14)** — xem bảng TC đề xuất bên dưới.

---

## 2. Thiếu so với quan điểm test

Không phát sinh quan điểm mới. 3 Q còn mở từ round 2:
- Q1 `PAY-STATE-001` — **Đóng**: `TC-PAYSTATE001-01/02` pass prd.
- Q2 `PAY-ABANDON-001` — còn mở, chưa có TC (giữ nguyên lý do round 2: chưa có oracle, cần Dev/Leader chốt ở §8).
- Q3 `JOB-001` — còn mở, vẫn chỉ là việc đổi mã quan điểm trên Studio (`JOB-002`/`RULE-TOOL-028` → `JOB-001`), không cần TC mới.

---

## 3. TC trùng lặp nội dung

Đã rà 77 TC (16 TC mới từ round 2 + round 3 so với 61 TC cũ) — **không phát hiện trùng lặp mới**. `NEW-70`–`NEW-74` không trùng bộ `NEW-58`–`69`: khác trục (round 2 kiểm option limit/calendar 個人 ở cấu hình KHÔNG nghỉ trước; round 3 kiểm riêng nhánh 合算をする/合算しない CÓ nghỉ trước, đúng điểm sửa của `a4c92a8626`).

---

## 4. Mâu thuẫn trong TCs

**C2 (từ round 2) — ĐÃ CHỐT, không còn là mâu thuẫn mở**: Dev đã **reject bug Studio #1509** ("lưới 予約管理 đánh dấu khung còn nhận đặt trong khi LIFF ẩn") với lý do chính thức *"admin sẽ hiển thị ON đến hết time lv"*. Điều này xác nhận đúng hướng Leader đã sửa ở `NEW-40`: **lưới admin KHÔNG cắt theo thời lượng Course**, không cần khớp 1:1 với LIFF. `#20823` (TC cũ từ #40128) còn giữ expected cũ *"Lưới admin 予約管理 nhất quán: không còn nhận đặt ở 19:00"* — **sai**, cần sửa theo rule vừa chốt.

⚠️ Phát sinh thêm: `#20823` ở lần chạy auto gần nhất đổi từ `pass` → **`error`** (không rõ lỗi hạ tầng hay lỗi thật) — xem §5 I3. Nên sửa expected **và** re-run trong 1 lần, tránh mất thêm 1 vòng.

C1 (TC-SLN-293 vs quy tắc Leader) — không có thông tin mới, vẫn chờ Leader cập nhật kho (§8 #2 cũ).

**C3 (mới) — `CONF-KHO`**: Leader chốt trực tiếp 2026-10-02: *"Admin book chỉ check điều kiện course off / staff off / ngày nghỉ và block time từ google là không được phép book. Còn các điều kiện khác vẫn book bình thường, kể cả vượt quá limit staff."* Kho `TC-SLN-115` (nguồn MT-13) ghi khác hẳn: *"Admin book KHÔNG bị chặn bởi mọi ràng buộc đặt lịch"* — liệt kê rõ cả case "staff KHÔNG có ca" (sub-case 1) và "khung giờ trùng block time sync từ Google" (sub-case 5) đều **bypass**, trái với lời Leader (staff off + Google block phải **chặn**). | Khả năng sai: (a) kho `TC-SLN-115` đã cũ / viết nhầm 2 sub-case đó, cần Leader xác nhận lại rồi sửa kho; (b) hoặc hành vi thực tế đổi theo thời gian (code có thể đã siết lại 2 điều kiện này sau khi kho được viết) — **chưa verify bằng TC thật**, 8 TC mới ở §7 (`G7`) dùng để verify. | `[MAJOR]` | Leader (xác nhận) → member (sửa kho nếu đúng) |

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | `NEW-58`–`61` (TC-FUNC004-06→09, G1+G2 round 2) | Cả 4 TC chỉ có `last_exec.env = local`. Đây là TC verify fix chính (option 2 + 合算をする), nên vẫn cần ít nhất 1 lần staging/prd trước khi coi là đóng hẳn G1/G2 | Chạy lại 4 TC này trên staging trong lần run kế tiếp |
| I2 | `[MAJOR]` | `NEW-70`→`74` (G6) | 5 TC Dev/pipeline tự viết cho REQ-008/009/010 (`合算をする`/`合算しない` × 指名/指名なし, 個人 đồng thời) **chưa chạy lần nào** (`exec: None`) | Đưa vào lần run kế tiếp trên staging; đây là TC verify chính của vòng vá `a4c92a8626`, không nên để "chưa chạy" trước khi release |
| I3 | `[MAJOR]` | `#20823` | Status đổi `pass` (round 2, 2026-09-30) → `error` (lần chạy gần nhất) không rõ lý do (hạ tầng hay thật). Đồng thời expected vẫn ghi sai theo C2 | Sửa expected theo C2 (lưới admin ON tới hết giờ làm, không cắt theo Course) **và** chạy lại trong 1 lần sửa — tránh tốn thêm 1 vòng review |
| I4 | `[MAJOR]` | `NEW-37` (TC-FUNC004-05, Option 1.2 tiếp sức) | Status đổi `pass` (round 2, 2026-09-30 06:46) → `skip`, có gắn ticket bug `#41746` (ticket đã closed) ở lần fetch này. Không rõ đây là skip do môi trường hay do TC bị đánh dấu lại sau thay đổi code | Hỏi Dev/runner lý do skip; nếu chỉ là carry-over từ bug cũ đã đóng thì chạy lại xoá trạng thái skip |
| I5 | `[MAJOR]` | `NEW-65` (TC-FUNC004-10, Calendar 個人 Option 2, round 2) | `exec: error` trên `local`. TC dùng 3 LINE user (U1/U2/U3) đặt cùng khung — nhiều khả năng là hạn chế của auto-runner (không mô phỏng được 3 session LINE khác nhau) hơn là lỗi app | Kiểm log lỗi của run; nếu đúng là hạn chế runner thì chuyển `exec_mode` sang `manual` cho riêng TC này, ghi rõ lý do ở `Ghi chú` |
| I6 | `[NIT]` | Bug #1822 | Studio đang đánh dấu bug `#41822` là **`stale`** (không phải `closed`/`fixed`) — nghĩa là hệ thống tự nhận biết TC đã đổi version (do Dev sửa thêm NEW-66/67 sau khi điều tra) nhưng **chưa có lần re-run nào xác nhận pass**. Đừng coi `stale` là "đã xong" | Chờ run `local` #2542 (đang chạy) hoặc chạy riêng `TC-FUNC004-10/11` trên staging, rồi review lại bug #1822 bằng tay |
| I7 | `[NIT]` | Mã quan điểm Studio lạ (round 3) | `NEW-70`–`73` dùng mã `FUNC-DATE-001` / `RULE-TOOL-029` / `TOOL-NEGCTRL-001` — `TOOL-NEGCTRL-001` không có trong `checklist-lme.md` (đã biết từ trước, không tính là cover ở §2) | Không cần hành động thêm, hệ quả đã nằm ở §2 |

---

## 6. TCs thừa / ngoài phạm vi task

Không có thay đổi so với round 2 (X1 `NEW-2`, X2 `NEW-40` — X2 đã được chứng minh **không thừa**, giữ nguyên theo C2/comment Leader ở §0).

---

## 7. TCs đề xuất bổ sung (14)

> Bổ sung theo yêu cầu trực tiếp của Leader (2026-10-02) sau khi soi ma trận **channel × option × vị trí × nghỉ** của cả 77 TC — xem phân tích đầy đủ trong tin nhắn review. 2 vùng thiếu G5'/G6 (viết ở §1 phần trên) **không cần TC mới** — chỉ phần dưới đây (G7, G8, G9) là TC mới thật.

**Business rule mới do Leader chốt trực tiếp (2026-10-02) — nguồn cho toàn bộ nhóm G7**:
> "Admin book chỉ check điều kiện course off / staff off / ngày nghỉ và block time từ Google là KHÔNG được phép book. Còn các điều kiện khác vẫn book bình thường, kể cả vượt quá limit staff."

⚠️ Quy tắc này **mâu thuẫn trực tiếp với kho `TC-SLN-115`** (kho ghi admin bypass luôn cả "staff không có ca" và "trùng block Google") — xem `CONF-KHO` mới ở §4 + §8 #8. TC mới ở nhóm G7 viết theo lời Leader (nguồn mới nhất, trực tiếp), **không** theo kho.

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` — `TC-SLN-115` (Admin thêm booking thủ công), `TC-SLN-263/267` (スタッフ自動割り当て — "cả 3 lối đặt lịch"), `TC-SLN-474/475/477` (App mobile — đối chiếu song song Web/App) |
| Vùng regression phát hiện từ kho | `TC-SLN-267`/`475`/`477` cho thấy kho vốn kỳ vọng **Web và App mobile đối xứng** — mọi TC admin-mobile ở đây đều viết đối chứng 1:1 với bản web tương ứng, đúng tinh thần đó |
| Conflict expected vs kho | `TC-SLN-115` — xem cảnh báo `CONF-KHO` ngay trên. Không tự chọn bên, giữ TC mới theo lời Leader, đẩy mâu thuẫn lên §4/§8 |
| GAP dùng lại TC kho (không viết mới) | Không — `TC-SLN-115` test trên cấu hình khác (không tách riêng per-option, không có calendar 個人) và theo quy tắc CŨ (đã bị Leader sửa), không dùng lại nguyên được |
| Căn cứ TC regression `R<x>` | Không có TC `R<x>` riêng — mọi TC ở đây đều map thẳng vào G7/G8/G9, không phải regression suy diễn |
| Xác nhận chống trùng | Đã đối chiếu 77 TC ở BƯỚC 0 — **không TC nào trùng**: đây là 3 trục (admin-bypass-rule, qua-ngày theo option, đầu-ca private-3) hoàn toàn chưa có TC nào trong 77 TC hiện tại (xem bảng channel×option và position×break ở phần phân tích) |

> Quy ước **Option limit** giữ như §7 trước: 1.1 = シフトの合算をしない · 1.2 = シフトの合算をする · 2 = 上限を設定しない · 3 = 上限を設定する (kèm setting limit N).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Admin thêm booking thủ công | Abnormal | manual | Tất cả | Admin book trên web: bị chặn khi course tắt, staff không có ca, ngày nghỉ, trùng block Google | - Lịch salon nhiều nhân viên. Option limit: 3, setting limit 2. Staff A set limit 1, Staff B set limit 1.<br>- Course C1 đang ON, Course C2 đang OFF (tắt hiển thị).<br>- Ngày X: Staff A có ca 12:00-20:00; Staff B KHÔNG có ca (nghỉ) ngày X.<br>- Ngày Y: cài 休業日 (ngày nghỉ) cho cả lịch.<br>- Staff A đã liên kết Google Calendar, có event block 15:00-16:00 ngày X. | 1. Admin mở 予約カレンダー, thử tạo booking course C2 (đang OFF) ngày X giờ bất kỳ.<br>2. Thử tạo booking course C1 cho Staff B ngày X (Staff B không có ca).<br>3. Thử tạo booking course C1 ngày Y (ngày nghỉ của lịch).<br>4. Thử tạo booking course C1 cho Staff A đúng khung 15:00-16:00 ngày X (trùng Google block). | Course C2 OFF; Staff B không ca; ngày Y 休業日; Staff A Google block 15:00-16:00 | Cả 4 bước đều KHÔNG tạo được booking, mỗi bước báo lỗi đúng nguyên nhân (course tắt, staff không có ca, ngày nghỉ, trùng lịch Google). Đây là 4 điều kiện DUY NHẤT admin book vẫn bị chặn theo quy tắc Leader chốt 2026-10-02. |  | Lấp G7 · quy tắc Leader chốt 2026-10-02: admin book chỉ chặn bởi course off / staff off / ngày nghỉ / Google block, các ràng buộc khác (limit, số lần đặt, 決済) đều bypass · CONF-KHO với TC-SLN-115 (kho ghi admin bypass luôn cả staff-off và Google-block) → xem §4 + §8 · manual vì bước 4 cần tài khoản Google Calendar thật để tạo block time (giống NEW-44/45) · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh thông báo lỗi 4 bước |
| TC-REGSHARED001-05 | UI | REG-SHARED-001 | Admin thêm booking thủ công | Boundary | auto | Tất cả | Admin book trên web: vượt limit cửa hàng và limit staff vẫn book được | - Lịch salon nhiều nhân viên. Option limit: 3, setting limit 1. Staff A set limit 1.<br>- Course C1 đang ON, Staff A có ca cả ngày, không ngày nghỉ, không Google block.<br>- Ngày X: Staff A đã có 1 booking course C1 chiếm đúng khung sẽ test (limit cửa hàng và limit Staff A đã dùng hết 1/1). | 1. Admin mở 予約カレンダー ngày X, thử tạo thêm 1 booking course C1 cho Staff A đúng khung đã đủ limit.<br>2. Kiểm tra booking mới có được tạo không, đếm tổng số booking ở khung đó. | Khung đã đủ limit cửa hàng (1) và limit Staff A (1) | Booking mới tạo THÀNH CÔNG — admin book không bị chặn bởi 受付上限, dù cả limit cửa hàng và limit staff đều đã đầy. Khung đó nay có 2 booking cùng giờ. |  | Lấp G7 · quy tắc Leader chốt 2026-10-02 (limit KHÔNG nằm trong 4 điều kiện chặn admin book) · đối chứng dương của TC-REGSHARED001-04 · Môi trường: Tất cả · Spec không ghi — trái TC-SLN-115 cột "điều kiện" nhưng khớp cột "kết quả" (booking vẫn thành công) · Evidence: ảnh 予約カレンダー có 2 booking cùng khung |
| TC-SYNCAPP001-02 | Job | SYNC-APP-001 | App mobile | Abnormal | manual | Tất cả | Admin book trên app mobile: bị chặn khi course tắt, staff không có ca, ngày nghỉ, trùng block Google | Như tiền điều kiện của TC-REGSHARED001-04, thêm: admin đã đăng nhập được app mobile. | 1-4. Lặp lại đúng 4 bước của TC-REGSHARED001-04 nhưng thực hiện trên app mobile thay vì web. | Course C2 OFF; Staff B không ca; ngày Y 休業日; Staff A Google block 15:00-16:00 | Cả 4 bước đều KHÔNG tạo được booking trên app mobile, cùng kết quả như trên web (TC-SLN-475/477 kho yêu cầu web và app nhất quán). |  | Lấp G7 · đối chứng kênh mobile của TC-REGSHARED001-04, bắt buộc vì chưa biết app mobile có cùng cơ chế chặn với web không · manual vì cần thiết bị/app thật + tài khoản Google Calendar thật · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh thông báo lỗi 4 bước trên app |
| TC-SYNCAPP001-03 | Job | SYNC-APP-001 | App mobile | Boundary | manual | Tất cả | Admin book trên app mobile: vượt limit cửa hàng và limit staff vẫn book được | Như tiền điều kiện của TC-REGSHARED001-05, thêm: admin đã đăng nhập được app mobile. | 1. Trên app mobile, thử tạo thêm 1 booking course C1 cho Staff A đúng khung đã đủ limit (giống TC-REGSHARED001-05).<br>2. Kiểm tra booking mới có được tạo không. | Khung đã đủ limit cửa hàng (1) và limit Staff A (1) | Booking mới tạo THÀNH CÔNG trên app mobile — cùng kết quả như trên web. Nếu app mobile CHẶN limit (khác web) thì đây là lệch kênh nghiêm trọng, cần báo Dev ngay. |  | Lấp G7 · đối chứng kênh mobile của TC-REGSHARED001-05 · manual vì cần thiết bị/app thật · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh app mobile có 2 booking cùng khung |
| TC-REGSHARED001-06 | UI | REG-SHARED-001 | Admin thêm booking thủ công | Abnormal | manual | Tất cả | Calendar 個人 — Admin book trên web: bị chặn khi course tắt, ngày nghỉ, trùng block Google | - Calendar loại 個人 (chỉ có staff 運営者), Option limit: 3, setting limit 2.<br>- Course C1 đang ON, Course C2 đang OFF.<br>- Ngày X: giờ làm việc 12:00-20:00. Ngày Y: cài 休業日 (ngày nghỉ) cho lịch.<br>- 運営者 đã liên kết Google Calendar, có event block 15:00-16:00 ngày X. | 1. Admin thử tạo booking course C2 (đang OFF) ngày X giờ bất kỳ.<br>2. Thử tạo booking course C1 ngày Y (ngày nghỉ).<br>3. Thử tạo booking course C1 đúng khung 15:00-16:00 ngày X (trùng Google block). | Course C2 OFF; ngày Y 休業日; Google block 15:00-16:00 ngày X | Cả 3 bước đều KHÔNG tạo được booking, mỗi bước báo lỗi đúng nguyên nhân. Calendar 個人 không có khái niệm "staff không có ca" riêng (chỉ 1 staff 運営者, giờ làm = giờ mở cửa lịch) nên chỉ còn 3/4 điều kiện so với calendar nhiều nhân viên. |  | Lấp G7 · bản calendar 個人 của TC-REGSHARED001-04 · manual vì bước 3 cần tài khoản Google Calendar thật · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh thông báo lỗi 3 bước |
| TC-REGSHARED001-07 | UI | REG-SHARED-001 | Admin thêm booking thủ công | Boundary | auto | Tất cả | Calendar 個人 — Admin book trên web: vượt limit vẫn book được | - Calendar loại 個人, Option limit: 3, setting limit 1.<br>- Ngày X: giờ làm việc 12:00-20:00, đã có 1 booking course C1 chiếm đúng khung sẽ test (limit đã dùng hết 1/1). | 1. Admin thử tạo thêm 1 booking course C1 đúng khung đã đủ limit ngày X.<br>2. Kiểm tra booking mới có được tạo không. | Khung đã đủ limit (1) | Booking mới tạo THÀNH CÔNG — admin book calendar 個人 cũng không bị chặn bởi 受付上限, giống calendar nhiều nhân viên. Khung đó nay có 2 booking cùng giờ. |  | Lấp G7 · bản calendar 個人 của TC-REGSHARED001-05 · liên quan trực tiếp bug #41822/#41823 (đếm limit calendar 個人 — xem lại sau khi vá a4c92a8626 không bị đếm sai theo hướng khác) · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh 予約カレンダー có 2 booking cùng khung |
| TC-SYNCAPP001-04 | Job | SYNC-APP-001 | App mobile | Abnormal | manual | Tất cả | Calendar 個人 — Admin book trên app mobile: bị chặn khi course tắt, ngày nghỉ, trùng block Google | Như tiền điều kiện của TC-REGSHARED001-06, thêm: admin đã đăng nhập được app mobile. | 1-3. Lặp lại đúng 3 bước của TC-REGSHARED001-06 nhưng thực hiện trên app mobile. | Course C2 OFF; ngày Y 休業日; Google block 15:00-16:00 ngày X | Cả 3 bước đều KHÔNG tạo được booking trên app mobile, cùng kết quả như trên web. |  | Lấp G7 · đối chứng kênh mobile của TC-REGSHARED001-06 · manual vì cần thiết bị/app thật + Google Calendar thật · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh thông báo lỗi 3 bước trên app |
| TC-SYNCAPP001-05 | Job | SYNC-APP-001 | App mobile | Boundary | manual | Tất cả | Calendar 個人 — Admin book trên app mobile: vượt limit vẫn book được | Như tiền điều kiện của TC-REGSHARED001-07, thêm: admin đã đăng nhập được app mobile. | 1. Trên app mobile, thử tạo thêm 1 booking đúng khung đã đủ limit ngày X.<br>2. Kiểm tra booking mới có được tạo không. | Khung đã đủ limit (1) | Booking mới tạo THÀNH CÔNG trên app mobile — cùng kết quả như trên web. |  | Lấp G7 · đối chứng kênh mobile của TC-REGSHARED001-07 · manual vì cần thiết bị/app thật · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh app mobile có 2 booking cùng khung |
| TC-FUNCDATE001-16 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Option 1.1 — booking qua ngày, khung sát ranh giới nửa đêm | - Option limit: 1.1. Staff A set limit 1.<br>- Không cài thời gian nghỉ trước / sau.<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: Staff A ca 18:00-00:30 (qua nửa đêm sang ngày X+1), chưa có booking. | 1. LIFF: chọn course 2h, 指名なし, ngày X.<br>2. Xem khung 22:00, 22:30, 23:00. | Course 2h · ngày X · ca Staff A 18:00-00:30 | 22:00 ON (phục vụ 22:00-00:00, trong ca). 22:30 ON (phục vụ 22:30-00:30, kết thúc đúng giờ tan ca). 23:00 OFF (phục vụ 23:00-01:00, vượt giờ tan ca 00:30). |  | Lấp G8 · option 1.1 chưa có TC nào qua ngày (chỉ option 3 có NEW-6/29/30) · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF 3 khung |
| TC-FUNCDATE001-17 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Option 1.2 — tiếp sức 2 nhân viên qua ranh giới nửa đêm | - Option limit: 1.2. Staff A set limit 1, Staff B set limit 1.<br>- Không cài thời gian nghỉ trước / sau.<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: Staff A ca 22:00-00:00 (ngày X); Staff B ca 00:00-02:00 (ngày X+1, nối tiếp liền Staff A), chưa có booking. | 1. LIFF: chọn course 2h, 指名なし, ngày X.<br>2. Xem khung 22:00 và 23:00.<br>3. Đặt khung 23:00 → mở booking trên 予約管理, kiểm ngày/giờ booking. | Course 2h · ngày X · Staff A 22:00-00:00 · Staff B 00:00(X+1)-02:00(X+1) | 22:00 ON: Staff A phục vụ trọn 22:00-00:00. 23:00 ON: phục vụ 23:00-01:00 vắt qua ngày X+1 (Staff A làm 23:00-00:00 rồi Staff B tiếp 00:00-01:00). Booking tạo ra đúng ngày/giờ, không lệch ngày do tiếp sức qua nửa đêm. |  | Lấp G8 · phép tiếp sức (#41746) chưa có TC nào qua ranh giới ngày — rủi ro off-by-one khi cộng/trừ ngày lúc nối ca 2 nhân viên khác ngày · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF + chi tiết booking |
| TC-FUNCDATE001-18 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Option 2 — booking qua ngày, khung sát ranh giới nửa đêm | - Option limit: 2. Staff A set limit 1.<br>- Không cài thời gian nghỉ trước / sau.<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: Staff A ca 20:00-02:00 (qua nửa đêm sang ngày X+1), chưa có booking. | 1. LIFF: chọn course 2h, 指名なし, ngày X.<br>2. Xem khung 23:30 và 00:30. | Course 2h · ngày X · ca Staff A 20:00-02:00 | 23:30 ON (phục vụ 23:30-01:30, nằm trong ca 20:00-02:00 dù vắt qua ngày X+1). 00:30 (ngày X+1, cùng luồng hiển thị) OFF (phục vụ 00:30-02:30, vượt giờ tan ca 02:00). |  | Lấp G8 · option 2 chưa có TC nào qua ngày · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF 2 khung, cả lưới ngày X và ngày X+1 |
| TC-FUNCDATE001-19 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Calendar 個人 · Option 2 — booking qua ngày | - Calendar loại 個人 (chỉ có staff 運営者), Option limit: 2.<br>- Không cài thời gian nghỉ trước / sau.<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: giờ làm việc 20:00-02:00 (qua nửa đêm sang ngày X+1), chưa có booking. | 1. LIFF: chọn course 2h, ngày X.<br>2. Xem khung 23:30. | Course 2h · ngày X · giờ làm 20:00-02:00 | 23:30 ON, đặt được (phục vụ 23:30-01:30, trong giờ làm việc dù vắt qua ngày X+1). |  | Lấp G8 · calendar 個人 chưa có TC nào qua ngày · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF |
| TC-FUNCDATE001-20 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Calendar 個人 · Option 3 limit 1 — booking qua ngày | - Calendar loại 個人, Option limit: 3, setting limit 1.<br>- Không cài thời gian nghỉ trước / sau.<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: giờ làm việc 20:00-02:00 (qua nửa đêm sang ngày X+1), đã có 1 booking 20:00-22:00. | 1. LIFF: chọn course 2h, ngày X.<br>2. Xem khung 23:30 (còn suất, chưa chiếm). | Course 2h · ngày X · giờ làm 20:00-02:00 · đã có booking 20:00-22:00 | 23:30 ON, đặt được — limit 1 chỉ tính đúng lượt đang bận (20:00-22:00), không ảnh hưởng khung 23:30 dù cùng ngày làm việc vắt qua nửa đêm. |  | Lấp G8 · calendar 個人 option 3 chưa có TC nào qua ngày · liên quan bug #41822/#41823 (đếm limit 個人) — ưu tiên chạy TC này sau khi vá a4c92a8626 · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF |
| TC-FUNCDATE001-21 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Calendar 個人 · Option 3 limit 1 — booking đầu ca, nghỉ trước không đẩy lùi giờ mở | - Calendar loại 個人 (chỉ có staff 運営者), Option limit: 3, setting limit 1.<br>- Nghỉ TRƯỚC 30 phút (không cài nghỉ sau).<br>- Đơn vị nhận đặt 30 phút. Course K120 (2 tiếng).<br>- Ngày X: giờ làm việc 12:00-20:00, chưa có booking. | 1. LIFF: chọn course 2h, ngày X.<br>2. Xem khung 12:00 và khung 11:30.<br>3. Đặt khung 12:00 → mở booking trên 予約管理. | Course 2h · ngày X · giờ làm 12:00-20:00 | 12:00 ON, đặt được: giờ phục vụ 12:00-14:00 nằm trong giờ làm, phần chuẩn bị 30 phút (11:30-12:00) được phép nằm TRƯỚC giờ mở cửa. 11:30 OFF: giờ phục vụ bắt đầu 11:30, TRƯỚC giờ mở cửa 12:00 của chính calendar. Booking tạo ra: 12:00-14:00. |  | Lấp G9 · calendar 個人 option 3 chưa có TC nào ở vị trí đầu ca (NEW-67 chỉ cuối ca, NEW-69 chỉ giữa ca) · Môi trường: Tất cả · Spec không ghi — quy tắc #40128/Leader 2026-09-29 (nghỉ trước được tràn qua trước giờ mở) · Evidence: ảnh LIFF + chi tiết booking |

---

## 8. Spec update needed

Giữ nguyên các mục mở của round 2 (§8 #1, #2, #4, #5, #6), cập nhật 2 mục:

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 3 (cập nhật) | Spec §2 (予約カレンダー admin) + Studio `#20823` | **Đã có quyết định chính thức** qua reject bug #1509: "lưới admin 予約カレンダー hiển thị khung ON đến hết giờ làm việc, không cắt theo thời lượng Course". Việc còn lại: ghi vào spec làm BR + sửa expected của `#20823` trên Studio | §4 C2 (round 3 — đã chốt) | Leader (ghi spec) / member (sửa TC) |
| 7 (mới) | `spec-features/admin/salon-booking/feature-spec.md` — hạn mức đếm theo lượt | Bổ sung BR: hạn mức mỗi nhân viên ở calendar **個人** phải đếm đúng 1 lần mỗi lượt đặt (bug #41822/#41823: trước đây đếm `staff_id=0` hai lần). Dev tự cảnh báo lỗi tương tự "CÓ THỂ còn ở `checkLimitShiftsNotCombined`" (スタッフ数の合計 + 合算しない) — **chưa có TC đo**, đề nghị Leader quyết có cần thêm TC đo riêng nhánh đó không trước khi release | Journal #139595 | Leader / Dev |
| 8 (mới) | `spec-features/admin/salon-booking/feature-spec.md` — mục "Admin thêm booking thủ công" + `kho-tcs/data/fa020_*.py` → `TC-SLN-115` | Leader chốt trực tiếp 2026-10-02: admin book **chỉ** bị chặn bởi course off / staff không có ca / ngày nghỉ / trùng block Google; **mọi** ràng buộc khác (kể cả vượt `受付上限`) đều bypass. Kho `TC-SLN-115` hiện ghi 2 sub-case này (staff off, Google block) cũng bypass — **sai theo quy tắc mới**, cần sửa lại 2 sub-case đó (giữ nguyên 4 sub-case còn lại: limit cửa hàng / limit staff / limit số lần đặt / 決済 vẫn bypass đúng). Sau khi 8 TC G7 ở §7 chạy xong và xác nhận đúng quy tắc mới → build lại kho | §4 C3 (CONF-KHO) | Leader |
