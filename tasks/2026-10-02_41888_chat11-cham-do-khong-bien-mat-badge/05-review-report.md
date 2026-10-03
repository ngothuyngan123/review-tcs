# 05 — Review Report

> Draft cho Leader verify. Round 1.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #351 (ticket 41888, round 1, `tc-ready`) |
| Tổng số TC review | 22 (10 AI job #1269 · 12 tester `haodtb@mcp` thêm tay) |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 13/13 mục có TC thiết kế, 2 mục RISK (F6, F8) + **0/22 TC đã chạy** — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (1 file `Basic/ChatController.php` +7/−1) | 7/8 điểm có TC, thiếu biên `confirm_count ≥ 2` + lối vào song song (nhóm / màn cũ / App mobile) + **0/22 TC đã chạy** — **CHƯA ĐỦ** |

**Kết luận**: 0/21 vùng ảnh hưởng đủ TC **đã chạy** · 0 GAP · 4 RISK do thiết kế (bảng dưới). Mọi vùng còn lại (BUG, F1–F5, F7, D1, D2, T1, T2; diff b1, b3–b7) đã có TC thiết kế đủ — chỉ còn RISK vì chưa chạy (xem §5 I1).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F6 — 2 lối vào cùng kiểu chặn #41634 không sửa (`/basic/rec_message`, `/basic/update-status-confirm`). Dev nói "lối vào đã chết" nhưng note của `NEW-3` ghi màn chat nhóm cũ `/basic/chat/group` **vẫn gọi** `/basic/rec_message`; spec chat-11 Luồng 6/EP-13 vẫn gán EP-13 cho SCR-CHT-01 | `dev-impact` + `diff code` (câu 3 + câu 5) | `NEW-3` (chỉ soi Network cho 2 nút ở Chat 1:1 V3, hội thoại bình thường) · `NEW-19`, `NEW-20` (hội thoại nhóm **không lệch**) | RISK — quy tắc mới "hội thoại lệch phải xác nhận được" chưa được thử trên hội thoại **nhóm lệch** và trên màn cũ; nếu lối vào cũ còn sống thì lỗi kẹt chấm đỏ **vẫn còn sẵn** ở nhánh Dev nói "không đổi" | `[MAJOR]` |
| G2 | App mobile — thao tác xác nhận trên app (kho `TC-CHT-400` bước 4) đi endpoint riêng, mục 3 file 03 không kê caller app | `diff code` (câu 3, hướng đọc #2) | `NEW-11` (app xác nhận hội thoại **bình thường**) · `NEW-12` (web → app) | RISK — chưa TC nào bấm xác nhận **hội thoại lệch trên App mobile**; nếu app có guard giống #41634 thì khách dùng app vẫn kẹt | `[MAJOR]` |
| G3 | b2 — điều kiện mới `confirm_count = 0` → chặn; ngược lại cho qua. Kho `TC-CHT-398` + MT-19: `confirm_count` **tăng 1 mỗi tin** (2, 3…), không chỉ 0/1 | `diff code` (câu 2) | `NEW-1`, `NEW-2`, `NEW-7`, `NEW-10` H1 — **tất cả dựng cờ = 1** | RISK — thiếu biên hội thoại lệch có `confirm_count ≥ 2` (nhánh false của điều kiện mới ngoài giá trị 1) | `[MAJOR]` |
| G4 | F8 / b8 — nguồn sinh lệch (job `linect`, `HandleImportCsv`) **không sửa** → `dev_impact`: "lệch vẫn có thể tái phát" | `dev-impact` + `diff code` | `NEW-4`, `NEW-21`, `NEW-22` (tin mới trên hội thoại **chưa từng lệch**) | RISK — chưa TC nào kiểm hội thoại **vừa được reset từ lệch** nhận tin mới thì về đúng trạng thái chưa xác nhận đồng bộ (chấm đỏ + badge + tab 未確認のみ) rồi xác nhận lại bình thường | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 13 quan điểm Trigger khớp task (FUNC-001 · DATA-001 · DATA-COUNT-001 · DATA-DB-001 · CONC-003 · PERM-003 · SEC-ISO-001 · SYNC-APP-001 · REG-SHARED-001 · COMPAT-LEGACY-001 · OUT-TRUTH-001 · UI-003 · MSG-USER-001) · 6 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-001` | Cao | GAP — sau khi reset hội thoại lệch, không TC nào kiểm nơi khác **đọc cùng cờ** `confirm_count`: bộ lọc 「未確認」/「確認済み」 ở danh sách bạn bè Chat 1:1 (kho nhóm #2 "Filter danh sách bạn bè"). `NEW-1` chỉ đối chiếu chấm đỏ + badge + tab 未確認のみ | `[BLOCKER]` |
| Q2 | `DATA-COUNT-001` | Cao | RISK — RULE-01: có Normal (`NEW-2`), Boundary chỉ ở `NEW-21` (đề nghị bỏ ở §6) → **thiếu Abnormal + Boundary đúng vùng fix**. Boundary lấp bằng G3; Abnormal = hội thoại lệch đang **ẩn** (loại khỏi badge) | `[MAJOR]` |
| Q3 | `FUNC-001` | Cao | RISK — chỉ `NEW-4` (Normal) mang mã hợp lệ; Abnormal/Boundary nằm ở `NEW-8`/`NEW-10` nhưng mang mã ngoài checklist nên không tính | `[MAJOR]` |
| Q4 | `SYNC-APP-001` | Trung bình → Cao (flow user-facing) | RISK — `NEW-11`/`NEW-12` chỉ hội thoại bình thường, thiếu hội thoại lệch trên App mobile → lấp bằng G2 | `[MAJOR]` |
| Q5 | `COMPAT-LEGACY-001` / `REG-SHARED-001` | Cao | RISK — RULE-09: chỉ test màn Chat 1:1 V3; màn chat cũ / chat nhóm cũ cùng kiểu chặn chưa test với dữ liệu lệch → lấp bằng G1 | `[MAJOR]` |
| Q6 | `PERM-003` · `SEC-ISO-001` | Cao | RISK — RULE-01: mỗi mã chỉ 1 TC Abnormal (`NEW-9`, `NEW-6`), không ghi lý do thiếu Normal/Boundary ở Ghi chú | `[MINOR]` |

- Q3: **không đẻ TC mới** — đề nghị đổi mã quan điểm trên Studio của `NEW-8` (Abnormal) và `NEW-10` (Boundary) sang `FUNC-001` (nội dung đã đúng).
- Q6: **không đẻ TC mới** — Normal tương đương `NEW-7` (cùng bot → 200); đề nghị ghi lý do "không có khái niệm biên" vào Ghi chú `NEW-6`/`NEW-9`.
- Đã loại (có lý do, không ghi GAP): `CONC-001` double-click — badge được **đếm lại** bằng `totalUserConfirmMessage`, không trừ dồn, `NEW-5` đủ · `JOB-001` — job `linect` không bị sửa · `STATE-001` — fix không thêm bước ghi mới.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-7`, `NEW-8` | `NEW-10` dòng H1 + H2 → bỏ 2 dòng này khỏi ma trận, giữ H3–H5 | `DUP-SUBSET` | API `POST /basic/confirm-message` · H1 = hội thoại lệch isConfirm=1 → 200 reset (= `NEW-7`); H2 = đã xác nhận thật → 422 không đổi dữ liệu (= `NEW-8`, `NEW-8` kiểm thêm `last_time_count_user_confirm`) | `[MINOR]` |
| DUP-2 | `NEW-20` | `NEW-19` → gộp vào `NEW-20` | `DUP-SUBSET` | `REG-SHARED-001` · Normal · xác nhận hội thoại nhóm G có tin chưa xác nhận → G hết chấm đỏ, badge giảm, reload giữ; `NEW-20` bước 4–5 đã bao trọn và kiểm thêm cô lập 1:1 ↔ nhóm | `[MINOR]` |

- **Gate đã chạy**: bỏ H1/H2 của `NEW-10` và `NEW-19` → REQ-001/002, `REG-SHARED-001`, coverage §1 còn nguyên (do `NEW-7`, `NEW-8`, `NEW-20` giữ).
- Không có `DUP-INFLATE`.
- Xóa/gộp do human thực hiện trên Studio (`testcase_update` / `testcase_delete`).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | `NEW-3` (bước 7), `NEW-7`…`NEW-10` | Endpoint mà nút 「確認済みに変更」 ở Chat 1:1 gọi | Chỉ gọi `POST /basic/confirm-message`; không gọi `/basic/update-status-confirm` | `spec-features/admin/chat-11/web/api-spec.md` EP-12: nút xác nhận dùng `POST /basic/chat/confirm-message` → `confirmReadMessage`; `feature-spec.md` Luồng 6: header SCR-CHT-01 gọi `/basic/update-status-confirm` (EP-13) | TC bám code mới (spec reverse-engineer từ màn cũ) **hoặc** spec đúng và Chat 1:1 V3 còn đường gọi EP-13 → ảnh hưởng G1 | `[MAJOR]` | Dev |

**Đã rà**: 22 TC × `spec-features/admin/chat-11/` (feature-spec Luồng 5–7 + BR-01…17, api-spec EP-12/13) + `spec-features/admin/chat-management/feature-spec.md` (BR-01, BR-06, BR-07) + `kho-tcs/fa001-chat11-11チャット.md` (nhóm #4, #10, #41; MT-19). Không phát hiện `CONF-TC` / `CONF-KHO`. Kho FA-002 (Quản lý chat) **chưa có** — không đối chiếu được.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 22 TC | **0/22 TC đã chạy** (`exec.untested = 22`, `last_exec = null`). `envAuto.local.runs = 1` nhưng không ghi kết quả vào TC nào. Dev cũng chỉ verify mức lint, chưa chạy runtime | Chạy bộ TC (ít nhất NEW-1, NEW-7, NEW-8, NEW-10) trước khi coi là đã verify fix; làm rõ lần run `local` bị mất kết quả |
| I2 | `[MAJOR]` | Ticket / phạm vi fix | `[AP-2]` Symptom-only: fix chỉ mở lại "đường tự chữa" (nút xác nhận), **2 nguồn gây lệch không fix** — job `linect` ghi 2 bước không nguyên tử; `HandleImportCsv` cột ステータスメッセージ=0 đặt `confirm_count=1` mà không tạo `unconfirm_message` (note `NEW-1`). Khách vẫn sẽ gặp chấm đỏ "ma" | Leader/Dev chốt: tạo ticket riêng cho 2 nguồn lệch, hoặc ghi rõ ngoài phạm vi #41888 (xem §8 #3) |
| I3 | `[MAJOR]` | `NEW-9` | RULE-13: lượt 3 (id không tồn tại) expected ghi "lỗi 4xx sạch" — chung chung | Ghi mã cụ thể: 404 (hoặc 403) theo bảng 1.1 |
| I4 | `[MAJOR]` | `NEW-17` | Expected không đo lường được: chấp nhận cả "UI cho phép" lẫn "UI chặn". Kho `TC-CHT-104`: 確認状況を変更 **không thực hiện được** với bạn bè đã bị block | Hỏi Dev hành vi của nút 「確認済みに変更」 khi mở chat của bạn bè bị block, rồi viết 1 expected |
| I5 | `[MAJOR]` | `NEW-13`, `NEW-14`, `NEW-15`, `NEW-19` | Steps không nói thao tác nào ("thực hiện thao tác đánh dấu đã xác nhận", "mở màn có chức năng chọn nhiều user"): nút 「確認済みに変更」 trong khung chat, quick action 確認状況を変更, hay 「全て確認済みに変更」 — 3 thao tác đi 3 endpoint khác nhau | Ghi rõ màn + nút + thao tác |
| I6 | `[MAJOR]` | 19/22 TC (trừ `NEW-5`, `NEW-8`, `NEW-10`) | Thiếu `Trạng thái đánh giá spec`; spec chat-11 **không mô tả** guard 422 「未読メッセージがありません。」 nên expected đang dựa theo ticket/code | Ghi `Spec không ghi · đã hỏi <ai>` hoặc `Đã hỏi leader` |
| I7 | `[MINOR]` | Toàn bộ 22 TC | RULE-02: Ghi chú không nêu loại evidence bắt buộc (ảnh badge trước/sau, HAR request, kết quả query DB) | Bổ sung `Evidence: <loại>` |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | `NEW-14`, `NEW-15` | Xác nhận một phần / 「全て確認済みに変更」 trên hội thoại **bình thường** — đi endpoint bulk, không qua `confirmMessage` | `spec_delta.files[]` chỉ `Basic/ChatController.php` (`confirmMessage`); kho đã có `TC-CHT-34`…`TC-CHT-43` | Chuyển sang bộ regression chung của kho | `[NIT]` |
| X2 | `NEW-16`, `NEW-18` | Block / unblock rồi tính lại badge — luồng block không bị chạm code | `dev_impact` không nêu block; kho `TC-CHT-404` đã cover | Chuyển sang bộ regression chung của kho | `[NIT]` |
| X3 | `NEW-21`, `NEW-22` | Badge tăng khi có tin mới — layer job `linect` không bị chạm code | `dev_impact`: "job linect không sửa"; kho `TC-CHT-398`, `TC-CHT-409` | Chuyển sang bộ regression chung của kho (biên DATA-COUNT-001 thay bằng TC-DATACOUNT001-01 ở §7) | `[NIT]` |

- **Gate đã chạy**: không TC nào ở trên là TC duy nhất của 1 impact/quan điểm — `DATA-COUNT-001` còn `NEW-2` (+ §7), `MSG-USER-001` còn `NEW-17`.
- Không flag `NEW-11`, `NEW-12`, `NEW-13` (hướng App mobile / lỗi I5 cần làm rõ trước).

---

## 7. TCs đề xuất bổ sung (15)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` (nhóm #2, #4, #7, #10, #39, #41; MT-19). Kho FA-002 chưa có — không đối chiếu được |
| Vùng regression phát hiện từ kho | `TC-CHT-400` (xác nhận trên web / App mobile / nhóm) · `TC-CHT-398` (bộ đếm tăng theo số tin) · nhóm #2 Filter 未確認/確認済み |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho | Không — `TC-CHT-400` dùng dữ liệu bình thường, không dựng lệch |
| Căn cứ TC regression `R<x>` | R1 ← T2 file 03 + chat-management BR-01/BR-07 (EP-05 đổi trạng thái tin) · **R2–R8 = ma trận cross check "đánh dấu chưa xác nhận ở tính năng A → xác nhận ở tính năng B"**: trạng thái lưu ở 2 nguồn (cờ `conversation.confirm_count` + bảng `unconfirm_message`), mỗi tính năng ghi 2 nguồn theo cách riêng — căn cứ: csv-management `job-spec.md:315-317` + `db-mapping.md:664` (CSV =1 xoá hết tin chưa đọc, cờ hội thoại cập nhật "có điều kiện"; CSV =0 chỉ tạo tin từ tin cuối) · chat-11 BR-05 (ẩn = tự xác nhận) · chat-management BR-01/BR-07 · kho `TC-CHT-34`, `TC-CHT-95`, `TC-CHT-102`, `TC-CHT-400` · journal Dev #139744 (workaround quick action / 全て確認済み chưa được chứng minh gỡ được hội thoại lệch) |
| Oracle chung cho R2–R8 | Sau **mỗi** thao tác đánh dấu và **mỗi** thao tác xác nhận, đối chiếu 4 nơi phải khớp nhau: chấm đỏ ở danh sách Chat 1:1 · tab 「未確認のみ」 ở チャット管理 · badge menu 1:1チャット · App mobile (TC có app) |
| Ô ma trận chưa đề xuất TC | CSV =0 → Quản lý chat: hội thoại lệch **không có tin** ở tab 「未確認のみ」 nên không xác nhận được từ đây — chưa có quy tắc đúng → đưa §8 #5, không bịa expected |
| Xác nhận chống trùng | Đã đối chiếu 22 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Group chat | Abnormal | auto | Tất cả | Hội thoại nhóm LINE bị lệch (có chấm đỏ nhưng không có tin chưa xác nhận) bấm 確認済みに変更 phải xoá được chấm đỏ | Đăng nhập admin, chọn bot test có ít nhất 1 nhóm LINE G. Dựng G ở trạng thái lệch: cờ chưa xác nhận của hội thoại = 1 nhưng không còn tin chưa xác nhận nào (cần hỗ trợ Dev ghi dữ liệu vì import CSV không áp cho nhóm). Mở DevTools tab Network. | 1. Mở 1:1チャット, F5, ghi số badge nhóm/menu.<br>2. Ở danh sách nhóm, xác nhận G đang có chấm đỏ.<br>3. Mở チャット管理 tab 未確認のみ, xác nhận không có tin nào của G.<br>4. Quay lại, chọn G, bấm 確認済みに変更.<br>5. Quan sát thông báo, chấm đỏ của G, badge; ghi lại URL request ở tab Network.<br>6. F5 và kiểm tra lại. | Nhóm G: cờ chưa xác nhận = 1, 0 tin chưa xác nhận | Không hiện 未読メッセージがありません。; chấm đỏ của G biến mất; badge giảm đúng 1 (ẩn nếu về 0); sau F5 không kẹt lại. Request đi tới /basic/confirm-message (nếu đi tới /basic/rec_message hoặc /basic/update-status-confirm thì ghi lại và báo Dev — lối vào chưa được sửa). | | Lấp G1, Q5 · regression · dẫn từ note NEW-3 + kho TC-CHT-400 bước 5 · Đánh giá spec: Spec không ghi · Evidence: ảnh trước/sau + HAR |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Lối vào cũ /basic/chat/group và header 対応ステータス | Abnormal | auto | Tất cả | Màn chat cũ còn truy cập được: xác nhận hội thoại lệch không bị kẹt lỗi 未読メッセージがありません。 | Đăng nhập admin, chọn bot test. Dựng bạn bè X lệch bằng Export CSV, sửa cột ステータスメッセージ của X = 0, Import lại (X chỉ có tin ở hệ chat mới). Mở DevTools tab Network. | 1. Truy cập trực tiếp URL /basic/chat/group (màn chat nhóm cũ). Ghi lại màn có mở được không.<br>2. Nếu mở được: chọn hội thoại lệch, bấm nút xác nhận; ghi request và thông báo.<br>3. Ở Chat 1:1 V3, mở X, đổi 対応ステータス trên header sang một trạng thái khác; ghi request phát sinh.<br>4. Kiểm tra chấm đỏ của X và badge sau mỗi bước, F5 lại. | Bạn bè X: lệch qua import CSV, ステータスメッセージ = 0 | Bước 1: màn cũ không mở được (redirect / 404) thì ghi nhận lối vào đã chết đúng như Dev nói. Nếu mở được: bấm xác nhận không hiện 未読メッセージがありません。 và chấm đỏ/badge cập nhật đúng. Bước 3: đổi 対応ステータス không làm xuất hiện thông báo 未読メッセージがありません。 và không làm chấm đỏ của X kẹt lại; ghi rõ endpoint được gọi. | | Lấp G1, Q5 · RULE-09 · nhóm Data theo GROUP_MAP COMPAT-LEGACY · Đánh giá spec: spec chat-11 Luồng 6 gán EP-13 cho SCR-CHT-01 (xem C1) · Evidence: HAR + ảnh |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | App mobile | Normal | manual | Tất cả | Hội thoại lệch xác nhận trên App mobile phải xoá chấm đỏ trên app và đồng bộ badge sang web | Cùng 1 bot đăng nhập trên App mobile và web. Dựng bạn bè X lệch bằng Export CSV, sửa cột ステータスメッセージ của X = 0, Import lại. Trên web xác nhận X có chấm đỏ, tab 未確認のみ không có tin của X; ghi badge web = N. | 1. Trên App mobile, mở danh sách chat, xác nhận X có dấu chưa đọc.<br>2. Mở hội thoại X trên app, bấm thao tác xác nhận (đã đọc).<br>3. Quan sát thông báo trên app, dấu chưa đọc của X, badge app.<br>4. Trên web, chờ realtime hoặc F5; kiểm tra chấm đỏ X và badge.<br>5. Đóng/mở lại app, kiểm tra lại X. | Bạn bè X: lệch qua import CSV; badge web ban đầu N | Trên app: không hiện lỗi kiểu 未読メッセージがありません。; X hết dấu chưa đọc; badge app giảm 1. Trên web: X hết chấm đỏ, badge = N−1. Mở lại app không xuất hiện lại. | | Lấp G2, Q4 · manual vì thiết bị thật App mobile · dẫn từ kho TC-CHT-400 bước 4 · Đánh giá spec: Spec không ghi · Evidence: ảnh app + web |
| TC-DATACOUNT001-01 | UI | DATA-COUNT-001 | Bộ đếm chưa xác nhận | Boundary | auto | Tất cả | Hội thoại lệch có bộ đếm chưa xác nhận lớn hơn 1 bấm 確認済みに変更 vẫn xoá được chấm đỏ | Đăng nhập admin, chọn bot test. Bạn bè X ở trạng thái lệch với bộ đếm chưa xác nhận của hội thoại = 3 và 0 tin chưa xác nhận (cần hỗ trợ Dev ghi dữ liệu). Đối chứng Y lệch với bộ đếm = 1. | 1. Mở 1:1チャット, F5, ghi badge N.<br>2. Xác nhận X, Y đều có chấm đỏ; tab 未確認のみ không có tin của X, Y.<br>3. Mở X, bấm 確認済みに変更; quan sát thông báo, chấm đỏ, badge.<br>4. Lặp lại với Y.<br>5. F5, kiểm tra lại X, Y, badge. | X: bộ đếm = 3, 0 tin chưa xác nhận<br>Y: bộ đếm = 1, 0 tin chưa xác nhận | Cả X và Y: không hiện 未読メッセージがありません。, chấm đỏ biến mất, bộ đếm của hội thoại về 0. Badge sau mỗi lần giảm đúng theo số hội thoại còn chưa xác nhận (không âm). Sau F5 không kẹt lại. | | Lấp G3, Q2 · Boundary của điều kiện mới confirm_count = 0 · dẫn từ kho TC-CHT-398 + MT-19 (bộ đếm tăng theo số tin) · Đánh giá spec: Spec không ghi · Evidence: ảnh + kết quả DB do Dev cung cấp |
| TC-FUNC001-01 | UI | FUNC-001 | Quick action — xác nhận, ẩn, block | Normal | auto | Tất cả | Hội thoại vừa được reset từ trạng thái lệch nhận tin mới phải về chưa xác nhận đồng bộ và xác nhận lại được | Đăng nhập admin, chọn bot test. Dựng bạn bè X lệch bằng Export CSV, sửa cột ステータスメッセージ của X = 0, Import lại. Ở X bấm 確認済みに変更 thành công (X hết chấm đỏ). Ghi badge N. | 1. Bạn bè X gửi 1 tin văn bản tới bot.<br>2. Trên web quan sát X, badge, tab 未確認のみ của チャット管理.<br>3. Mở X, bấm 確認済みに変更.<br>4. Quan sát chấm đỏ, badge, tab 未確認のみ; F5 lại. | Tin từ X: テスト41888-再送 | Sau bước 1–2: X có chấm đỏ, badge = N+1, tab 未確認のみ có tin テスト41888-再送 (cả 3 nơi khớp nhau). Sau bước 3: không lỗi, X hết chấm đỏ, badge = N, tab 未確認のみ không còn tin của X; F5 giữ nguyên. | | Lấp G4 · dẫn từ dev_impact "nguồn sinh lệch không sửa nên lệch vẫn có thể tái phát" · bước bạn bè gửi tin chạy auto bằng mô phỏng callback · Đánh giá spec: Spec ghi rõ (chat-management BR-01) · Evidence: ảnh 3 nơi |
| TC-DATA001-01 | UI | DATA-001 | Filter danh sách bạn bè | Normal | auto | Tất cả | Sau khi xác nhận hội thoại lệch, bộ lọc 未確認 và 確認済み của danh sách bạn bè cập nhật đúng | Đăng nhập admin, chọn bot test. Dựng bạn bè X lệch bằng Export CSV, sửa cột ステータスメッセージ của X = 0, Import lại. | 1. Ở 1:1チャット chọn bộ lọc 未確認: xác nhận X có trong danh sách.<br>2. Mở X, bấm 確認済みに変更.<br>3. Chọn lại bộ lọc 未確認, rồi bộ lọc 確認済み; tìm X.<br>4. Nhập tên X vào ô tìm kiếm kết hợp bộ lọc 未確認 rồi 確認済み.<br>5. F5 và lặp lại bước 3. | Bạn bè X: lệch qua import CSV | Trước xác nhận: X nằm trong bộ lọc 未確認. Sau xác nhận: X không còn ở 未確認, có trong 確認済み; tìm kiếm theo tên cho kết quả giống hệt (không còn X ở 未確認); F5 giữ nguyên. | | Lấp Q1 · dẫn từ chat-11 Luồng 5 (filter unconfirm = confirm_count) + kho nhóm #2 · Đánh giá spec: Spec ghi rõ · Evidence: ảnh trước/sau từng bộ lọc |
| TC-DATACOUNT001-02 | UI | DATA-COUNT-001 | Bộ đếm chưa xác nhận | Abnormal | auto | Tất cả | Hội thoại lệch đang bị ẩn bấm 確認済みに変更: reset được cờ nhưng badge không đổi | Đăng nhập admin, chọn bot test. Bạn bè X đang ẩn (非表示中) và ở trạng thái lệch: cờ chưa xác nhận = 1, 0 tin chưa xác nhận (ẩn X trước, rồi Export CSV, sửa ステータスメッセージ của X = 0, Import lại; kiểm X vẫn ở 非表示中). Ghi badge N. | 1. Ở 1:1チャット chọn bộ lọc 非表示中, mở X.<br>2. Bấm 確認済みに変更.<br>3. Quan sát thông báo, trạng thái X, badge.<br>4. F5, kiểm tra X vẫn ở 非表示中 và badge. | Bạn bè X: đang ẩn + lệch | Không hiện 未読メッセージがありません。, không lỗi 5xx; X không còn trạng thái chưa xác nhận; X vẫn ở 非表示中; badge giữ nguyên N (hội thoại ẩn không được tính). | | Lấp Q2 · dẫn từ dev_impact (badge = cờ 1, không chặn, không ẩn) + chat-11 BR-05 · Đánh giá spec: Spec ghi rõ (BR-05) · Evidence: ảnh trước/sau |
| TC-DATA001-02 | UI | DATA-001 | Quản lý chat (チャット管理) | Normal | auto | Tất cả | Hội thoại vừa reset từ lệch: đổi tin sang 未確認 ở チャット管理 phải làm chấm đỏ và badge xuất hiện lại | Đăng nhập admin, chọn bot test. Bạn bè X từng lệch đã được reset bằng 確認済みに変更 (X không chấm đỏ). Ghi badge N. | 1. Mở チャット管理, tab すべて, tìm tin mới nhất của X.<br>2. Chọn tin đó, chọn 未確認, bấm 変更.<br>3. Mở tab 未確認のみ tìm tin của X.<br>4. Mở 1:1チャット kiểm tra chấm đỏ X và badge.<br>5. Ở チャット管理 đổi tin đó lại 確認済, kiểm tra lại X và badge. | Bạn bè X: hội thoại vừa reset | Sau bước 2: tin của X có ở tab 未確認のみ; X có chấm đỏ; badge = N+1. Sau bước 5: tin rời tab 未確認のみ, X hết chấm đỏ, badge = N. Không phát sinh lệch mới. | | Lấp R1 · regression · dẫn từ T2 file 03 + chat-management BR-01/BR-07 · Đánh giá spec: Spec ghi rõ · Evidence: ảnh 2 màn |
| TC-DATA001-03 | UI | DATA-001 | Quick action — xác nhận, ẩn, block | Normal | auto | Tất cả | Cross check: hội thoại lệch do import CSV được xác nhận bằng quick action 確認状況を変更 → 「確認済」に変更 | Đăng nhập admin, chọn bot test. Dựng bạn bè X lệch: Export CSV có cột ステータスメッセージ, sửa ô của X = 0, Import lại (X chỉ có tin ở hệ chat mới). Kiểm X có chấm đỏ, tab 未確認のみ không có tin của X. Ghi badge N. | 1. Ở danh sách bạn bè 1:1チャット, tick avatar X để mở modal クイックアクション.<br>2. Chọn 「確認済」に変更, bấm 実行する.<br>3. Đối chiếu 3 nơi: chấm đỏ X, tab 未確認のみ ở チャット管理, badge menu.<br>4. F5 và đối chiếu lại 3 nơi. | Bạn bè X: lệch qua import CSV ステータスメッセージ = 0 | Không lỗi; X hết chấm đỏ; tab 未確認のみ vẫn không có tin của X; badge = N−1; sau F5 cả 3 nơi giữ nguyên và khớp nhau. | | Lấp R2 · regression · cross check CSV=0 → quick action · dẫn từ kho TC-CHT-95 + journal Dev #139744 (workaround) · Đánh giá spec: Spec không ghi · Evidence: ảnh 3 nơi trước/sau |
| TC-BULK001-01 | UI | BULK-001 | 全て確認済みに変更 | Normal | auto | Tất cả | Cross check: 全て確認済みに変更 xác nhận được cả hội thoại lệch do import CSV lẫn hội thoại chưa xác nhận bình thường | Đăng nhập admin, chọn bot test. Bạn bè X lệch (import CSV ステータスメッセージ = 0, X chỉ có tin ở hệ chat mới). Bạn bè Y chưa xác nhận bình thường (Y gửi 1 tin tới bot). Không có bạn bè chưa xác nhận nào khác. Ghi badge N (= 2). | 1. Ở 1:1チャット chọn bộ lọc 未確認, xác nhận có X và Y.<br>2. Bấm 全て確認済みに変更, bấm 決定 ở popup.<br>3. Đối chiếu 3 nơi cho X và Y: chấm đỏ, tab 未確認のみ, badge menu.<br>4. F5 và đối chiếu lại. | X: lệch qua import CSV<br>Y: 1 tin LINE chưa xác nhận | X và Y đều hết chấm đỏ; tab 未確認のみ không còn tin của Y (X vốn không có); badge về 0 và ẩn; bộ lọc 未確認 trống; F5 giữ nguyên. | | Lấp R3 · regression · cross check CSV=0 / tin LINE → 全て確認済み · dẫn từ kho TC-CHT-34 + journal Dev #139744 (workaround) · Đánh giá spec: Spec không ghi · Evidence: ảnh 3 nơi |
| TC-DATA001-04 | UI | DATA-001 | Quick action — xác nhận, ẩn, block | Normal | auto | Tất cả | Cross check: ẩn bạn bè (非表示にする) tự xác nhận được hội thoại lệch do import CSV | Đăng nhập admin, chọn bot test. Bạn bè X lệch (import CSV ステータスメッセージ = 0, X chỉ có tin ở hệ chat mới), đang hiển thị (chưa ẩn). Ghi badge N. | 1. Mở modal クイックアクション của X, chọn 非表示にする, bấm 実行する.<br>2. Đối chiếu badge menu, tab 未確認のみ.<br>3. Chọn bộ lọc 非表示中, mở X: kiểm chấm đỏ và message hệ thống 非表示しました.<br>4. F5 và đối chiếu lại. | Bạn bè X: lệch qua import CSV | X chuyển sang 非表示中, có message 非表示しました; X không còn trạng thái chưa xác nhận; badge = N−1; tab 未確認のみ không có tin của X; F5 giữ nguyên. | | Lấp R4 · regression · cross check CSV=0 → ẩn bạn bè · dẫn từ chat-11 BR-05 + kho TC-CHT-102 · Đánh giá spec: Spec ghi rõ (BR-05) · Evidence: ảnh 3 nơi |
| TC-DATA001-05 | UI | DATA-001 | Import CSV — ステータスメッセージ | Normal | auto | Tất cả | Cross check: hội thoại chưa xác nhận do tin LINE / Chat 1:1 / チャット管理 tạo ra được xác nhận bằng import CSV ステータスメッセージ = 1 | Đăng nhập admin, chọn bot test. Chuẩn bị 3 bạn bè đang đã xác nhận: A gửi 1 tin LINE tới bot (chưa xác nhận do tin đến); B ở Chat 1:1 bấm 未確認に変更; C ở チャット管理 chọn tin mới nhất của C, chọn 未確認, bấm 変更. Kiểm A, B, C đều có chấm đỏ và đều có tin ở tab 未確認のみ. Ghi badge N. | 1. Export CSV có cột ステータスメッセージ cho A, B, C.<br>2. Sửa ô ステータスメッセージ của A, B, C thành 1, lưu file.<br>3. Import lại, chờ báo hoàn tất.<br>4. Đối chiếu 3 nơi cho từng bạn bè: chấm đỏ, tab 未確認のみ, badge menu.<br>5. F5 và đối chiếu lại; mở từng hội thoại xem nút cạnh ô nhập. | A: chưa xác nhận do tin LINE<br>B: chưa xác nhận do Chat 1:1<br>C: chưa xác nhận do チャット管理<br>CSV: ステータスメッセージ = 1 | Cả A, B, C: hết chấm đỏ, không còn tin ở tab 未確認のみ, nút cạnh ô nhập là 未確認に変更; badge = N−3; không bạn bè nào bị lệch kiểu còn chấm đỏ mà tab trống hoặc ngược lại; F5 giữ nguyên. | | Lấp R5 · regression · cross check (tin LINE / Chat 1:1 / チャット管理) → CSV=1 · dẫn từ csv-management job-spec 315-317 + db-mapping 664 (cờ hội thoại cập nhật có điều kiện) · Đánh giá spec: Spec ghi rõ một phần (điều kiện chưa mô tả) · Evidence: file CSV + ảnh 3 nơi |
| TC-DATA001-06 | UI | DATA-001 | Quản lý chat (チャット管理) | Boundary | auto | Tất cả | Cross check: hội thoại có 2 tin chưa xác nhận, xác nhận 1 tin ở チャット管理 thì vẫn chưa xác nhận, xác nhận nốt ở Chat 1:1 thì hết | Đăng nhập admin, chọn bot test. Bạn bè X gửi 2 tin văn bản tới bot (cả 2 chưa xác nhận). Ghi badge N. | 1. Ở チャット管理 tab 未確認のみ, chọn 1 trong 2 tin của X, chọn 確認済, bấm 変更.<br>2. Đối chiếu 3 nơi: chấm đỏ X, tab 未確認のみ, badge menu.<br>3. Ở 1:1チャット mở X, bấm 確認済みに変更.<br>4. Đối chiếu lại 3 nơi; F5. | Tin X: テスト41888-1, テスト41888-2 | Sau bước 1: tab 未確認のみ còn đúng 1 tin của X; X vẫn có chấm đỏ; badge giữ N. Sau bước 3: không hiện 未読メッセージがありません。; X hết chấm đỏ; tab 未確認のみ không còn tin của X; badge = N−1; F5 giữ nguyên. | | Lấp R6 · regression · cross check チャット管理 (một phần) → Chat 1:1 · dẫn từ chat-management BR-01 (existence-based) + kho TC-CHT-400 · Đánh giá spec: Spec ghi rõ · Evidence: ảnh 3 nơi mỗi bước |
| TC-DATA001-07 | UI | DATA-001 | Quản lý chat (チャット管理) | Normal | auto | Tất cả | Cross check: Chat 1:1 bấm 未確認に変更 rồi xác nhận ở チャット管理 | Đăng nhập admin, chọn bot test. Bạn bè Y có ít nhất 1 tin, đang đã xác nhận. Ghi badge N. | 1. Ở 1:1チャット mở Y, bấm 未確認に変更.<br>2. Đối chiếu 3 nơi: chấm đỏ Y, tab 未確認のみ có tin của Y, badge = N+1.<br>3. Ở チャット管理 tab 未確認のみ chọn tin của Y, chọn 確認済, bấm 変更.<br>4. Đối chiếu lại 3 nơi; mở Y xem nút cạnh ô nhập; F5. | Bạn bè Y: hội thoại có tin, đã xác nhận | Sau bước 1: Y có chấm đỏ, tab 未確認のみ có tin mới nhất của Y, badge = N+1. Sau bước 3: Y hết chấm đỏ, tab không còn tin của Y, badge = N, nút cạnh ô nhập là 未確認に変更; F5 giữ nguyên, không lệch. | | Lấp R7 · regression · cross check Chat 1:1 → チャット管理 (chiều ngược R1) · dẫn từ chat-management BR-01/BR-07 + kho TC-CHT-401 · Đánh giá spec: Spec ghi rõ · Evidence: ảnh 3 nơi |
| TC-SYNCAPP001-02 | UI | SYNC-APP-001 | App mobile | Normal | manual | Tất cả | Cross check App mobile và web: đánh dấu chưa xác nhận trên app rồi xác nhận trên web, và ngược lại | Cùng 1 bot đăng nhập trên App mobile và web. Bạn bè A và B có tin, đang đã xác nhận. Ghi badge web N. | 1. Trên app, đánh dấu A chưa xác nhận.<br>2. Trên web đối chiếu 3 nơi cho A (chấm đỏ, tab 未確認のみ, badge = N+1).<br>3. Trên web mở A, bấm 確認済みに変更; kiểm A trên web và trên app.<br>4. Trên web mở B, bấm 未確認に変更; kiểm B trên app.<br>5. Trên app xác nhận B; kiểm B trên web (3 nơi). | A: đánh dấu ở app, xác nhận ở web<br>B: đánh dấu ở web, xác nhận ở app | Mỗi bước: trạng thái A/B trên app và web giống nhau; web không hiện 未読メッセージがありません。 ở bước 3; badge web tăng/giảm đúng 1 theo từng bước, kết thúc = N; app không còn dấu chưa đọc của A, B. | | Lấp R8 · regression · cross check App mobile ↔ web · manual vì thiết bị thật App mobile · dẫn từ kho TC-CHT-400 + chat-management BR-07 (FCM cập nhật badge app) · Đánh giá spec: Spec ghi rõ (BR-07) · Evidence: ảnh app + web từng bước |

- Q3, Q6: không đề xuất TC mới (lý do ở §2).

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/web/api-spec.md` EP-12 + `feature-spec.md` | Ghi endpoint thực tế của nút 「確認済みに変更」/「未確認に変更」 ở Chat 1:1 V3 (`POST /basic/confirm-message` → `Basic\ChatController@confirmMessage`), guard 422 「未読メッセージがありません。」 (#41634) và điều kiện mới: chỉ chặn khi 0 tin chưa xác nhận **và** `confirm_count = 0` (#41888) | C1 `CONF-SPEC` | Dev |
| 2 | `feature-spec.md` Luồng 6 / EP-13 + `ChatController::confirm` (`/basic/rec_message`) | Xác nhận 2 lối vào cũ còn caller không (màn chat nhóm cũ, header 対応ステータス). Còn caller → quy tắc "hội thoại lệch phải xác nhận được" chưa áp cho nhánh đó (lỗi có sẵn) | C1 + G1 | Dev / Leader |
| 3 | `spec-features/admin/csv-management` + chat-11 (job `linect`) | Chốt hành vi đúng khi import CSV cột ステータスメッセージ = 0 với bạn bè chỉ có tin ở hệ chat mới (hiện sinh hội thoại lệch), và việc ghi 2 bước không nguyên tử của `linect` — có tạo ticket riêng không | I2 | Dev / PM |
| 4 | `chat-management` mục Kiến trúc Confirm/Unconfirm ("confirm_count 1 = has unconfirm") | Kho MT-19: bộ đếm tăng theo số tin (2, 3…). Chốt badge đếm `confirm_count = 1` hay `> 0` — ảnh hưởng expected của TC-DATACOUNT001-01 | G3 | Leader |
| 5 | `chat-management` (tab 「未確認のみ」) + `csv-management` job import | Hội thoại lệch do CSV =0 (cờ = 1, không có bản ghi tin) **không xuất hiện** ở tab 「未確認のみ」 → không xác nhận được từ チャット管理. Chốt đây là hành vi chấp nhận được (chỉ gỡ ở Chat 1:1 / quick action / 全て確認済み / ẩn) hay CSV =0 phải tạo bản ghi tin để チャット管理 thấy được | §7 ô ma trận chưa đề xuất TC | Dev / Leader |
| 6 | `csv-management/job/job-spec.md:315-317` + `db-mapping.md:664` | Mô tả rõ điều kiện cập nhật cờ hội thoại khi import ステータスメッセージ = 1 (hiện ghi "có điều kiện" nhưng không nêu điều kiện) — expected của TC-DATA001-05 phụ thuộc điểm này | §7 R5 | Dev |
