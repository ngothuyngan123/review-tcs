# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #176 (ticket 35363, round 1, branch `ai_fixbug_35363`) |
| Tổng số TC review | 22 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 9/13 vùng ảnh hưởng đủ TC · 2 GAP · 2 RISK (BUG + T2 gộp thành G1) · 1 nhóm orphan

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` + `T2` — Reminder Delivery (FA-022): sau khi xóa trường, job `NewEventRemindTask` **không còn gửi tin** cho LINE user (hậu quả cuối mà ticket muốn chặn) | `dev-impact` | `NEW-19` (skip — `SOURCE_BRANCH_MISSING`: project job chưa có branch run) | `RISK` — 21 TC pass chỉ chứng minh **dữ liệu đầu vào của job đã sạch** (đếm DB ở local); chưa TC nào quan sát output cuối trên LINE app (RULE-06), chưa chạy staging/production (RULE-08) | `[BLOCKER]` |
| G2 | Tương tác fix ↔ job kiểu「月日」(lặp hàng năm): job gửi xong sẽ **clone** `event_step_time` +1 năm (spec §7 bước 3). Trường 月日 đã gửi năm nay rồi mới bị xóa → mốc năm sau do job sinh phải bị dọn theo | `diff code` | không có — NEW-1 / NEW-2 / NEW-20 đều dùng「年月日」(1 lần); NEW-2 tự sửa status trong DB, không đi qua job clone | `GAP` — nhánh 月日 (đường sinh mồ côi "vĩnh viễn" nếu fix sót) chưa có TC | `[MAJOR]` |
| G3 | Mục 5 Recover data — dọn `event_step` (type=3) + `event_step_time` tồn đọng từ trường đã xóa **trước** fix, chạy 1 lần trên production | `dev-impact` | `NEW-17` (chỉ xác nhận "fix không tự dọn") · `NEW-18` (chỉ soát bot test) | `GAP` — không TC nào verify **script dọn**: đếm trước/sau toàn hệ thống (RULE-04), dọn đúng mồ côi, KHÔNG đụng trường còn sống / `d_*` / type khác / bot khác | `[BLOCKER]` |
| G4 | `NEW-21`, `NEW-22` — xóa **giá trị** ngày của từng friend (màn 情報一覧 / 友だち詳細) | `orphan` | — | Luồng `HelperService` / `deleteDataFriendInfo` **không bị sửa** (Dev mục 2 đã loại trừ) — không map BUG/F/D/T nào. Giữ làm regression nhẹ được, nhưng không tính vào coverage của fix | `[NIT]` |

> Chiều `diff code`: Studio `spec_delta` có diff (`diffAvailable=true`, 3 file, +37 dòng). 5 điểm gọi hàm mới (`deleteItem` NEW-1 · `deleteItems` NEW-6 · `deleteGroup` NEW-7 · mobile `deleteFriendInfoField` NEW-9 · `deleteFriendInfoFolder` NEW-10) đều có TC pass. Nhánh danh sách rỗng (NEW-3/4/8), lọc `bot_id` (NEW-12/15), lọc `type=3` + `d_4` (NEW-16), hard-delete mốc đã gửi (NEW-2) đều đủ → không ghi dòng.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 12 quan điểm Trigger khớp task · 5 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `MSG-002` (+ `ENV-003`) | Cao | `GAP` — tin đặt lịch "không gửi sau khi xóa trường" chỉ có NEW-19, mang mã lạ `JOB-002` **và** skip. 0 TC chạy production dù task chạm job nền | `[BLOCKER]` |
| Q2 | `CONC-001` | Cao | `GAP` — không TC nào xóa trường **trong lúc job đang xử lý** mốc của trường đó (job poll 5s, đa luồng; mốc ở `SENDING` + clone 月日 có thể sinh lại bản ghi sau khi hàm dọn đã chạy) | `[BLOCKER]` |
| Q3 | `REG-RUN-001` | Cao | `GAP` — dữ liệu lịch nhắc tồn đọng từ trước release (Dev mục 5) chưa có TC verify phương án dọn — trùng G3 | `[BLOCKER]` |
| Q4 | `DATA-DB-001` | Cao | `RISK` — nội dung đã đủ (2 bot: NEW-15 web / NEW-12 mobile; type khác + sinh nhật: NEW-16), nhưng các TC này gắn mã lạ `TOOL-NEGCTRL-001` → chỉ NEW-18 (Normal) mang mã đúng. **Không cần TC mới** — gắn lại mã trên Studio (xem I4) | `[MAJOR]` |
| Q5 | `SYNC-APP-001` | Trung bình (→ Cao: flow critical) | `RISK` — NEW-9 / NEW-10 gọi thẳng `/api/mobile/*`, chưa verify trên **app mobile admin** thật (RULE-06). `Input thiếu`: chưa rõ app có UI xóa trường/folder friend info không | `[MAJOR]` |

- Q5 không đề xuất TC mới: hỏi Dev app mobile admin có màn xóa trường / folder friend info không → có thì chạy lại kịch bản NEW-9 / NEW-10 qua UI app (đổi `Nhóm` sang UI); không có thì giữ nguyên dạng API.
- Đã loại khỏi phạm vi: `DATA-REF-001` (nơi tham chiếu trường — filter/form/action — không bị fix chạm), `JOB-001` (job Java **không sửa**, Studio `dev_impact`: "Không sửa job bên linect-service"), `DATA-BACKUP-001` (copy bot FA-033 không bị chạm, fix không thêm bảng).

---

## 3. TC trùng lặp nội dung

Đã rà 22 TC, không phát hiện trùng lặp. Các cặp giống nhau về kịch bản nhưng **khác entry point** nên giữ cả: NEW-5 (web) / NEW-14 (mobile) — backup lock · NEW-7 (web) / NEW-10 (mobile) — xóa folder · NEW-15 (web, 2 bot) / NEW-12 (mobile, id bot khác) · NEW-1 (1 dòng nhắc, kiểm cascade bảng cũ) / NEW-2 (nhiều dòng + mốc đã gửi).

- **Gate đã chạy**: không đề nghị xóa TC nào.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ 22 TC | **RULE-08 / ENV-003**: 22/22 TC chạy ở `local` (run #404 ngày 2026-08-21 + run #1658 ngày 2026-09-18, runner AI), 0 TC staging/production. Task chạm job nền (FA-022) | Chạy lại bộ core (NEW-1, 6, 7, 9, 10, 19) trên staging; G1 bắt buộc production. Kiểm `ENABLE_EVENT_REMIND` đang bật trước khi chạy (kho MT-17: spec ghi mặc định `0` = tắt) |
| I2 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine (`2026-09-18 by /new-task`) nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** | Tester đọc lại journal #130711 rồi tick |
| I3 | `[MAJOR]` | NEW-21, NEW-22 | TC do thanhntp viết: thiếu `Mã quan điểm` + `Loại case`; NEW-22 để trống tiền điều kiện, dồn tiền điều kiện vào bước 1 ("Friend A có ngày cũ và reminder"); NEW-21 bước "Mở màn quản lý bạn bè" mơ hồ (lần chạy thật dùng `/basic/friend-information/item/<id>` → 一括削除). Người khác không dựng lại được env | Bổ sung tiền đề (trường 年月日 có action, 2 friend có giá trị tương lai), ghi đúng màn (情報一覧 / 友だち詳細), gắn `FRIEND-001` + `Normal` |
| I4 | `[MAJOR]` | NEW-13 | `Kết quả mong đợi` để ngỏ mã trạng thái ("tester ghi lại rồi báo leader") → không đo lường được, không kết luận Đạt/Không đạt được. Lần chạy thật: cả 2 lần gọi đều trả **HTTP 200** | Leader/Dev chốt hành vi (xem §6 mục 3), rồi sửa expected trên Studio |
| I5 | `[MINOR]` | 12 TC mang mã lạ + 2 TC trống mã | Mã không có trong `checklist-lme.md` → không map được coverage: `TOOL-NEGCTRL-001` (NEW-3, 12, 15, 16) · `TOOL-ERRHYG-001` (NEW-11, 13) · `TOOL-KNOW-002` (NEW-1) · `SELECT-SCOPE-001` (NEW-6) · `DATA-RETENTION-001` (NEW-2) · `TOOL-OLDREC-001` (NEW-17) · `API-001` (NEW-9) · `JOB-002` (NEW-19) · trống (NEW-21, 22) | Gắn lại mã trên Studio (`testcase_update`): NEW-3/12/15/16/2 → `DATA-DB-001` · NEW-1/6 → `FUNC-001` · NEW-11/13 → `FUNC-002` · NEW-17 → `REG-RUN-001` · NEW-9 → `SYNC-APP-001` · NEW-19 → `MSG-002` |
| I6 | `[MINOR]` | 21 TC pass | **RULE-02**: evidence chỉ là text `actual` do runner tự ghi (số đếm trước/sau), `artifacts` rỗng — không có ảnh chụp query / screenshot | Với các TC core (NEW-1, 6, 7, 9, 10) đính kèm ảnh chụp câu query trước/sau khi chạy trên staging |
| I7 | `[MINOR]` | NEW-20 | Dữ liệu test `管理名 = TC35363_LIFE_NGAY_MOI` dài 21 ký tự, vượt giới hạn 20 → runner phải tự đổi thành `TC35363_LIFE_MOI` mới chạy được | Sửa dữ liệu test trên Studio (≤ 20 ký tự) |
| I8 | `[NIT]` | NEW-21, NEW-22 | `[AP-5]` phủ layer không bị chạm: luồng xóa giá trị từng friend không nằm trong diff | Giữ nếu Leader muốn regression nhẹ; không bắt buộc cho ticket này |
| I9 | `[NIT]` | NEW-22 (run #1658) | Runner ghi nhận ngoài phạm vi: cùng một trường, màn 友だち詳細 lưu `2026/11/27` (dấu `/`) còn đường khác lưu `2026-11-12` (dấu `-`). Lịch nhắc vẫn tính đúng | Leader xem có cần tách ticket riêng không — không thuộc #35363 |

---

## 5. TCs đề xuất bổ sung (4)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` (nhóm Xóa folder · Xóa info · Job action ngày tháng · MT-09 · MT-17) |
| Vùng regression phát hiện từ kho | TC-FRI-35 (xóa folder chứa 年月日 → không gửi) · TC-FRI-153 (xóa trường 年月日 → không gửi) · TC-FRI-246 (月日 job sinh lịch năm sau) |
| Conflict expected vs kho | Không. MT-09 ("xóa trường/folder có dọn lịch không?") nay đã có câu trả lời từ fix → §6 |
| GAP dùng lại TC kho (không viết mới) | **G1 / Q1 → TC-FRI-153** "Xóa trường 年月日 đang có lịch gửi → lịch bị dọn, bạn không nhận action mồ côi" + **TC-FRI-35** "Xóa folder chứa trường 年月日 đang có lịch gửi → …". Cả 2 đã ở PRODUCTION, quan sát LINE app thật → chạy trên branch fix; bổ sung tiền đề "job `ENABLE_EVENT_REMIND` đang bật". Đồng thời chạy lại **NEW-19** trên staging sau khi Studio có branch cho project job |
| Xác nhận chống trùng | Đã đối chiếu 22 TC ở BƯỚC 0 + kho FA-015 — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FRIEND001-01 | UI | FRIEND-001 | Xóa info | Boundary | manual | product | Xóa trường「月日」(lặp hàng năm) sau khi job đã gửi năm nay → lịch năm sau do job sinh cũng bị dọn, không gửi lại | - Bot test A, job gửi action ngày tháng đang bật<br>- Trường 年月日「TC35363_MD」: 登録「月日」, 0 日, 前, giờ gửi = hiện tại + 10 phút, action gửi text「TC35363-MD」<br>- Friend U1 (tài khoản LINE test) có giá trị ngày = hôm nay | 1. Chờ tới giờ gửi, xác nhận U1 nhận「TC35363-MD」trên LINE app<br>2. Xác nhận U1 đã có lịch gửi cho **năm sau** (job tự sinh)<br>3. Mở 友だち情報管理, menu (…) của「TC35363_MD」→「削除」→ OK<br>4. Kiểm tra lịch gửi của U1 cho trường này<br>5. Mở chat 1:1 của U1 | Trường kiểu 月日 · 1 friend LINE thật | - Bước 1: U1 nhận đúng 1 tin<br>- Bước 4: không còn lịch gửi nào của trường (kể cả mốc năm sau vừa sinh)<br>- Bước 5: tin đã gửi năm nay vẫn còn trong lịch sử chat 1:1 | | Lấp G2 · Đánh giá spec: Spec không ghi (BR-06 chưa nói lịch do job clone) · Evidence: screenshot LINE app + ảnh chụp query lịch gửi của U1 trước/sau bước 3 · RULE-01: Normal/Abnormal đã có ở NEW-1, NEW-20 · dẫn từ TC-FRI-246 |
| TC-CONC001-01 | UI | CONC-001 | Xóa info | Abnormal | manual | product | Xóa trường 年月日 đúng lúc job đang gửi mốc của trường đó → sau lượt quét không còn lịch nào của trường, job không lỗi, trường đối chứng vẫn gửi | - Bot test A, job đang bật<br>- Trường「TC35363_RACE」kiểu「月日」, action gửi text「TC35363-RACE」<br>- ≥ 200 friend có giá trị ngày sao cho **cùng một mốc gửi** (hiện tại + 5 phút) — dùng Import CSV giá trị<br>- Trường đối chứng「TC35363_RACE_CTRL」kiểu 年月日, 1 friend, mốc gửi = hiện tại + 15 phút | 1. Ghi số lịch gửi của「TC35363_RACE」<br>2. Tới đúng giờ gửi, khi tài khoản LINE test đầu tiên vừa nhận tin → lập tức xóa「TC35363_RACE」(menu (…) →「削除」→ OK)<br>3. Chờ 2 chu kỳ quét của job<br>4. Kiểm tra lịch gửi còn lại của「TC35363_RACE」(cả năm nay lẫn năm sau)<br>5. Chờ mốc của trường đối chứng, kiểm tra LINE app | 200 friend cùng mốc · 1 trường đối chứng | - Bước 4: 0 lịch gửi (không có lịch năm sau nào được job sinh lại sau khi xóa)<br>- Log job không có exception do lịch trỏ tới trường/lịch đã xóa<br>- Bước 5: friend của trường đối chứng nhận đúng 1 tin đúng giờ | | Lấp Q2 · RULE-08 (race + job) → product · Đánh giá spec: Spec không ghi — hành vi với tin đang ở trạng thái 送信中 cần Dev chốt (§6 mục 4) · Evidence: log job + ảnh chụp query trước/sau + screenshot LINE app · RULE-01: Normal = NEW-1, không có biên số lượng riêng |
| TC-REGRUN001-01 | Data | REG-RUN-001 | Xóa info | Normal | manual | Tất cả | Script dọn dữ liệu tồn đọng xóa hết lịch nhắc của trường 年月日 đã xóa trước khi deploy fix → tới mốc không gửi | - Trên **release cũ** (chưa có fix): tạo trường 年月日「TC35363_OLD」có action, 2 friend có mốc gửi tương lai (≥ 1 ngày), rồi xóa trường → tạo sẵn lịch mồ côi<br>- Deploy branch fix<br>- Có script dọn Dev cung cấp (Redmine mục 5) | 1. Chạy câu SELECT đếm Dev cung cấp (toàn hệ thống), ghi số lượng<br>2. Backup 2 bảng lịch nhắc<br>3. Chạy script dọn<br>4. Chạy lại câu SELECT đếm<br>5. Tới mốc gửi cũ của 2 friend, kiểm tra LINE app | 2 lịch mồ côi dựng có chủ đích | - Bước 1: số lượng > 0, có 2 lịch của「TC35363_OLD」<br>- Bước 4: số lượng = 0<br>- Bước 5: 2 friend KHÔNG nhận tin | | Lấp G3 · Lấp Q3 · RULE-04 (query toàn hệ thống trước/sau) · chạy staging trước, production khi dọn thật · Đánh giá spec: Spec không ghi · Evidence: ảnh chụp kết quả SELECT trước/sau + screenshot LINE app |
| TC-REGRUN001-02 | Data | REG-RUN-001 | Xóa info | Abnormal | manual | Tất cả | Script dọn tồn đọng KHÔNG đụng lịch nhắc của trường còn sống, sinh nhật 生年月日, lịch loại khác và bot khác | - Như TC-REGRUN001-01, thêm trên cùng bot: trường 年月日「TC35363_ALIVE」còn sống có lịch · trường 生年月日 đã setting action có lịch · 1 lịch loại khác (vd lịch nhắc từ đặt lịch)<br>- Bot B có trường 年月日 còn sống có lịch | 1. Ghi số lịch gửi của từng nhóm đối chứng<br>2. Chạy script dọn<br>3. Đếm lại từng nhóm đối chứng<br>4. Tới mốc của「TC35363_ALIVE」, kiểm tra LINE app | 4 nhóm đối chứng | - Số lịch gửi của cả 4 nhóm đối chứng giữ nguyên<br>- Bước 4: friend của「TC35363_ALIVE」nhận đúng 1 tin đúng giờ | | Lấp G3 · Lấp Q3 · Đánh giá spec: Spec không ghi · Evidence: ảnh chụp query đếm từng nhóm trước/sau · RULE-01: không có biên số lượng riêng cho script dọn |

---

## 6. Spec update needed

1. **`spec-features/admin/friend-information/feature-spec.md` §BR-06 bước 6** ghi "Implicit: xoá `event_step` + `event_step_time` (type=3)". Trước fix #35363 điều này **sai** (đó chính là bug). Sửa thành khẳng định: gọi `deleteEventStepFriendInfo(friendInfoId, botId)` ở 5 điểm (`deleteItem` / `deleteItems` / `deleteGroup` + mobile `deleteFriendInfoField` / `deleteFriendInfoFolder`), dọn cả mốc đã gửi. Bổ sung bước dọn lịch vào "Luồng: Xoá hàng loạt items" (SCR-FRI-01) và luồng xóa folder. Bảng "Mobile API" §6 thiếu 2 endpoint `delete-friend-info-field` / `delete-friend-info-folder`.
2. **Kho `kho-tcs/fa015-…md` — MT-09** ("xóa trường/folder có dọn lịch không?") → chốt: **CÓ**, từ fix #35363. Expected của TC-FRI-35 / TC-FRI-153 giữ nguyên.
3. **NEW-13 / mobile `delete-friend-info-folder` với folder không tồn tại hoặc đã xóa**: Studio input ghi 404「folder not found」, code hiện tại trả **200** kèm danh sách (nhánh 404 nằm ở hàm đổi tên folder). Dev/Leader chốt hành vi đúng.
4. **Xóa trường trong lúc job đang gửi** (TC-CONC001-01): mốc đang ở `SENDING` (status=1) có được gửi nốt không, và job có được clone mốc 月日 năm sau cho trường đã xóa không — spec §7 chưa định nghĩa. Dev chốt để làm expected.
