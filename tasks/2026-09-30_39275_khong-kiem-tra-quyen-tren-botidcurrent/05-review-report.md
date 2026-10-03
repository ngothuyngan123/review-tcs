# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #238 (ticket 39275, round 1, branch `ai_fixbug_39275`) |
| Tổng số TC review | 21 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 7/8 mục có TC — **CHƯA ĐỦ** (`BUG` · F1 · F2 · D1 · D2 · D3 · T1 · T2; F3/T3 = ~10 endpoint chat khác, Dev tự loại khỏi phạm vi → không tính) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (1 file `ChatController.php`, +17/−3) | 4/7 điểm có TC — **CHƯA ĐỦ** (guard mới · nhánh (a) chặn · nhánh (b) cho phép bot khác phiên thuộc quyền · nhánh (c) rỗng → bot phiên · luồng hợp lệ như cũ · count ghi theo bot đã kiểm · `Log::warning` mới) |

**Kết luận**: 11/15 vùng ảnh hưởng đủ TC · 0 GAP · 4 RISK (G1 tính cho cả 2 chiều).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | T2 multi-tab + nhánh (b) "bot khác phiên nhưng thuộc quyền" × **bộ lọc danh sách** + hành vi đổi "count ghi theo bot đã kiểm" | `dev-impact` + `diff code` | NEW-2 · NEW-3 · NEW-7 · NEW-10 · NEW-14 | **RISK** — nhánh (b) chỉ được test với *không lọc* và *lọc thẻ*. Bộ lọc 送信予約中の友だち đã lộ lệch: run 2338 NEW-7 thực tế **0/2 hội thoại bot A được xác nhận** (service dò lịch gửi theo bot phiên = C), nhưng TC không có oracle nên vẫn `pass`. 4 bộ lọc còn lại (未確認 · 確認済み · 非表示中 · グループ) + từ khoá chưa test với bot khác phiên | `[BLOCKER]` |
| G2 | Nhánh (b) — guard chỉ xét **phạm vi bot**, không xét **quyền tính năng** của vai trò staff | `diff code` | NEW-18 | **RISK** — run 2338: staff có vai trò không có quyền Chat 1:1 bị chặn ở giao diện nhưng **gọi thẳng endpoint vẫn thành công (HTTP 200 `success:true`) và đổi dữ liệu bot B**. Expected của NEW-18 là "ghi nhận, không kết luận" → không có TC nào phán quyết được. ✅ **Leader chốt 2026-09-30 (C3)**: phải chặn ở cả giao diện và API, API trả 403 hoặc 404 → hành vi hiện tại của fix là **lỗi**, Dev phải bổ sung kiểm quyền tính năng | `[BLOCKER]` |
| G3 | Nhánh (a) chặn — contract phản hồi khi bị từ chối | `diff code` | NEW-5 · NEW-12 · NEW-13 · NEW-16 · NEW-17 · NEW-20 · NEW-21 | **RISK** — mọi TC chặn đều lấy oracle `HTTP 200 + success=false` (theo hành vi code). ✅ **Leader chốt 2026-09-30 (C1)**: cross-bot / bot không tồn tại = **403 hoặc 404** → fix hiện tại trả 200 là **không đạt**, Dev sửa mã trả về; 7 TC phải đổi expected — xem §4 C1 | `[BLOCKER]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 13 quan điểm Trigger khớp task · 12 chưa cover đủ. Trong đó **8 quan điểm** (Q2 · Q4 · Q5 · Q6 · Q7 · Q9 và phần gắn mã của Q3 · Q8) **nội dung đã có TC** nhưng TC mang mã nội bộ Studio hoặc mã lệch → chỉ cần **gắn lại mã quan điểm trên Studio**, không đẻ TC. Thiếu thật: **Q1 · Q3 · Q8 · Q10 · Q11 · Q12**. Đủ: `PERM-004` (NEW-11 + NEW-21).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PERM-001` | Cao | **GAP thực chất** — TC duy nhất (NEW-18) không có oracle; thực tế endpoint chấp nhận staff không có quyền Chat 1:1 (xem G2) | `[BLOCKER]` |
| Q2 | `PERM-002` | Cao | RISK RULE-01 — chỉ Abnormal mang mã (NEW-5, NEW-13). Normal (NEW-9/NEW-10) và Boundary (NEW-19/NEW-20) có nội dung nhưng mang mã lạ → gắn lại mã | `[MAJOR]` |
| Q3 | `PERM-003` | Cao | RISK — tính năng nhiều bot / đổi bot phiên: 0 TC mang mã; nội dung nằm ở NEW-2 (`CONC-001`) + NEW-7, và NEW-7 đang che lệch ở bộ lọc 送信予約中 (G1) | `[MAJOR]` |
| Q4 | `FUNC-001` | Cao | RISK RULE-01 — chỉ Normal (NEW-1). Boundary (NEW-8) + Abnormal (NEW-12) mang mã lạ → gắn lại mã | `[MAJOR]` |
| Q5 | `DATA-DB-001` | Cao | RISK — 0 TC mang mã. Kiểm `WHERE` scope 2 tài khoản đã có ở NEW-5 / NEW-12 / NEW-16 → gắn lại mã | `[MAJOR]` |
| Q6 | `DATA-COUNT-001` | Cao | RISK — 0 TC mang mã; nội dung ở NEW-14 (`OUT-TRUTH-001`), NEW-3, NEW-2 → gắn lại mã | `[MAJOR]` |
| Q7 | `BULK-001` | Cao | RISK — bộ lọc + thao tác hàng loạt: 0 TC mang mã (NEW-3 mang mã lạ); chưa có ma trận bộ lọc × bot khác phiên (G1) | `[MAJOR]` |
| Q8 | `CONC-001` | Cao | RISK RULE-01 — có Normal (NEW-2) + Abnormal (NEW-6), **thiếu Boundary**, không ghi lý do | `[MAJOR]` |
| Q9 | `SEC-ISO-001` | Cao | RISK — nhiều tab tải dữ liệu nhiều bot: nội dung đã có ở NEW-2 / NEW-14 (badge từng bot) nhưng không TC nào mang mã → gắn lại mã | `[MAJOR]` |
| Q10 | `OUT-TRUTH-001` | Cao | GAP — khi bị từ chối, FE chỉ xử lý nhánh success (`chat-v2.js:2945`) → người dùng bấm 決定 **không thấy gì**. NEW-5 cố ý loại điểm này ra; NEW-14 mang mã này nhưng kiểm bộ đếm. Expected giao diện chưa có ai chốt (REQ-009 (3)) | `[MAJOR]` |
| Q11 | `REG-SHARED-001` | Cao | GAP — Dev nêu ~10 endpoint chat khác dùng `botIdCurrent` thô nhưng **không kê tên**; Studio coverage `EP-13 /basic/update-status-confirm` = none | `[MAJOR]` |
| Q12 | `SYNC-APP-001` | Cao (Leader 2026-09-30: chức năng này phải test cả PC và App mobile) | GAP — 0 TC chạy trên App mobile: chưa có TC bấm 全て確認済みに変更 trên App với 5 bộ lọc, cũng chưa có TC bộ đếm phía App sau hành vi đổi "count ghi theo bot đã kiểm" (kho TC-CHT-398/400) | `[BLOCKER]` |

---

## 3. TC trùng lặp nội dung

Đã rà 21 TC, **không phát hiện trùng lặp**. Các cặp gần nhau đã xét và giữ nguyên: NEW-5 vs NEW-12 (khác đường kích hoạt: sửa request do màn phát ra vs gọi thẳng endpoint) · NEW-1 vs NEW-9 (UI vs contract phản hồi) · NEW-2 vs NEW-10 (multi-tab thật vs tham số bot khác cùng chủ) · NEW-3 vs NEW-14 (lọc thẻ cùng bot vs bot khác phiên) · NEW-13 vs NEW-20 (bot không tồn tại vs sai kiểu).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-5 · NEW-12 · NEW-13 · NEW-16 · NEW-17 · NEW-20 · NEW-21 | Mã HTTP khi bị từ chối (cross-bot / bot không tồn tại / sai kiểu) | `HTTP 200` + `success=false` + 「この権限は許可されていません。」 (theo hành vi fix, tiền lệ #39153) | `framework/checklist-lme.md` RULE-13 bảng 1.1: cross-bot / không tồn tại = **403 hoặc 404**; sai kiểu (`abc`, mảng, `true`) = **400**. Leader chốt 2026-09-30: RULE-13 áp cả ajax nội bộ admin, ví dụ đúng `POST /basic/chat/confirm-message` | ✅ **Leader chốt 2026-09-30: 403 hoặc 404** → fix trả sai mã, Dev sửa; NEW-5 · NEW-12 · NEW-13 · NEW-16 · NEW-17 · NEW-21 đổi expected sang `HTTP 403 hoặc 404`. NEW-20 (sai kiểu `abc` / mảng / `true`) — RULE-13 ghi **400**, chưa rõ quyết định 403/404 có áp cho nhánh này không → xác nhận thêm | `[BLOCKER]` — đúng rule của root cause | ✅ Leader đã chốt · Dev sửa code |
| C2 | `CONF-SPEC` | NEW-2 · NEW-10 · NEW-11 · NEW-14 | Gửi `botIdCurrent` là bot khác bot phiên nhưng thuộc quyền user | Được chấp nhận, ghi dữ liệu vào bot đó | `spec-features/admin/chat-11/web/logic-spec.md:240`: "Bot scoping: Mọi query đều filter theo `bot_id = getBotId()` từ session" | (1) Spec cũ hơn fix — nhánh multi-tab là chủ đích → update spec · (2) Fix mở rộng quá phạm vi spec → thu hẹp về bot phiên | `[MAJOR]` | PM / Leader |
| C3 | `CONF-KHO` | NEW-18 | Staff vai trò không có quyền Chat 1:1 gọi thẳng endpoint của bot được mời | "Ghi nhận thực tế, KHÔNG tự kết luận" (run 2338: endpoint chấp nhận, dữ liệu bot B bị đổi) | Kho TC-CHT-423 "thao tác bị chặn ở giao diện: gọi trực tiếp API cũng PHẢI bị chặn ở tầng máy chủ" · TC-CHT-426 | ✅ **Leader chốt 2026-09-30: chặn ở cả giao diện và API, API trả 403 hoặc 404** → kho TC-CHT-423 đúng; NEW-18 thiếu oracle và endpoint đang lỗi quyền. NEW-18 đổi expected theo quyết định này (hoặc thay bằng TC-PERM001-01 ở §7) | `[BLOCKER]` — nâng từ MAJOR vì là lỗ hổng quyền đã xác nhận | ✅ Leader đã chốt · Dev sửa code |
| C4 | `CONF-KHO` | NEW-6 | Double click 決定 | "Nếu lần gọi thứ hai vẫn được gửi đi thì không được làm thay đổi thêm dữ liệu" (chấp nhận 2 request) | Kho TC-CHT-43: "Chỉ phát sinh 1 request xác nhận" | (1) TC nới oracle · (2) Kho quá chặt — thao tác idempotent nên 2 request chấp nhận được. Run 2338 thực tế chỉ 1 request → không ảnh hưởng kết quả hiện tại | `[MAJOR]` | Leader |

**Đã rà**: 21 TC × `spec-features/admin/chat-11/` (`feature-spec.md` BR-01…BR-17 — không có BR nào cho 全て確認済みに変更; `web/api-spec.md` EP-12; `web/logic-spec.md:240`) + `framework/checklist-lme.md` RULE-13 + `kho-tcs/fa001-chat11-11チャット.md` (nhóm 全て確認済みに変更 TC-CHT-33…43 · Bộ đếm chưa xác nhận TC-CHT-398…409 · Phân quyền staff TC-CHT-423…430) — 4 mâu thuẫn C1…C4. Không có `CONF-TC`.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-7 · NEW-18 · NEW-21 | **`pass` không phản ánh kết quả thật** — pass rate 20/21 bị thổi phồng, thực chất 17/21. NEW-7 & NEW-18 có expected "ghi nhận, KHÔNG tự kết luận" (không đo lường được) nhưng runner chấm `pass` trong khi actual lộ lệch: NEW-7 bot A 0/2 hội thoại được xác nhận; NEW-18 dữ liệu bot B bị đổi. NEW-21 expected `success=false` + thông báo nhưng actual là `HTTP 302` → `/admin/pre-select-bot`, vẫn `pass` | NEW-18: expected đã có (C3 — chặn, 403 hoặc 404, dữ liệu bot B không đổi) → sửa trên Studio, chạy lại sẽ **fail** với code hiện tại → raise bug. NEW-21: đổi expected sang 403 hoặc 404 (C1); actual hiện là 302 redirect của middleware → cũng lệch. NEW-7: vẫn chờ Leader chốt REQ-009 (2) (§7 TC-BULK001-01 đưa sẵn expected). Đổi kết quả 3 TC về `Chưa test` cho tới khi chạy lại |
| I2 | `[BLOCKER]` | NEW-20 | TC `fail` (run 2338): `botIdCurrent` dạng mảng → **HTTP 500** `Array to string conversion` tại `ChatController.php:206` (dòng `Log::warning` do chính fix thêm). Studio bug #1474 `open` nhưng `redmine_id = null` — **chưa raise ticket Redmine** | Raise Redmine từ Studio bug #1474 (hoặc ghi vào ticket gốc #39275 vì dòng lỗi nằm trong diff). Expected đúng theo RULE-13: sai kiểu = **400** (không phải 200 + `success=false` như TC đang ghi — xem C1) |
| I3 | `[MAJOR]` | NEW-15 | RULE-13 — expected "điều hướng về màn đăng nhập (hoặc trả về phản hồi không cho phép)" không ghi mã HTTP; actual run 2338 ra 302 (không phiên) và 419 (cookie cũ) | Ghi mã cụ thể: không phiên / phiên hết hạn = **401**; nếu Leader chấp nhận redirect của middleware web thì ghi rõ `302 → /logout` làm ngoại lệ |
| I4 | `[MINOR]` | Toàn bộ 21 TC | `env_scope` chỉ khai `local`, 2 run đều ở local (run 595 skip hết do lỗi checkout). Ticket đang Re-open "để test" — chưa TC nào chạy ở dev/staging | Khai `Phạm vi ENV = Tất cả` (task không dính RULE-08) và chạy lại ở staging trước khi đóng ticket |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-15 | Test layer **không bị chạm code**: chặn khi chưa đăng nhập nằm ở middleware nhóm route (`routes/web.php:882`), chạy trước controller; guard mới nằm trong controller nên không thể mở đường vòng bỏ qua đăng nhập | `spec_delta.files[]` chỉ có `ChatController.php`; `dev_impact` không nhắc middleware | ✅ **Đã xoá trên Studio 2026-09-30** (Leader duyệt, #14217) | `[NIT]` |

- **Gate đã chạy**: NEW-15 không phải TC duy nhất cover impact / quan điểm nào (`AUTH-SESSION-001` là mã nội bộ Studio) → flag hợp lệ. Các TC còn lại đều map được `BUG` / F / D / T hoặc rủi ro hồi quy Studio (NEW-4 smoke = RULE-12, NEW-17 = `Log::warning` trong diff).

---

## 7. TCs đề xuất bổ sung (8)

> ✅ **Đã sync lên Studio task #238 (2026-09-30)**: TC-PERM001-01 → **NEW-22** (#21200) · TC-REGSHARED001-01 → **NEW-23** (#21201) · TC-SYNCAPP001-02 → **NEW-24** (#21202). 5 TC còn lại chưa sync.

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` (nhóm 全て確認済みに変更 · Filter danh sách bạn bè · Bộ đếm chưa xác nhận · Phân quyền staff & môi trường) |
| Vùng regression phát hiện từ kho | TC-CHT-35…38 (bộ lọc × 全て確認済み) · TC-CHT-43 (double click) · TC-CHT-398/400 (bộ đếm web + App mobile) · TC-CHT-423/426 (API phải chặn như UI) |
| Conflict expected vs kho | NEW-18 vs TC-CHT-423 → C3 · NEW-6 vs TC-CHT-43 → C4 (đã đưa §4 + §8). TC đề xuất không conflict kho |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression | Không có TC `R<x>` — regression sibling / App mobile đã lên §2 (Q11, Q12) |
| Xác nhận chống trùng | Đã đối chiếu 21 TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** |

**Không đẻ TC mới — xử lý trên TC có sẵn:**
- **G3** — trùng 4 yếu tố với NEW-5 / NEW-12 / NEW-13 / NEW-16 / NEW-17 / NEW-21 (BƯỚC 5b) → **sửa expected trên Studio** thành `HTTP 403 hoặc 404` (Leader chốt C1 2026-09-30); không tạo TC song song. NEW-20 chờ xác nhận sai kiểu = 400 hay 403/404.
- **Q2 · Q4 · Q5 · Q6 · Q9** — nội dung đã có, chỉ **gắn lại mã quan điểm trên Studio**: NEW-9 / NEW-10 → `PERM-002` Normal · NEW-19 → `PERM-002` Boundary · NEW-8 → `FUNC-001` Boundary · NEW-12 → `FUNC-001` Abnormal + `DATA-DB-001` · NEW-14 → `DATA-COUNT-001` · NEW-2 → thêm `SEC-ISO-001` / `PERM-003`.
- **Q10** — expected giao diện khi bị từ chối **chưa có ai chốt** (REQ-009 (3)); không viết TC với oracle tự suy. Leader chốt ở §8 dòng 6 rồi bổ sung.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-BULK001-01 | UI | BULK-001 | 全て確認済みに変更 | Normal | auto | Tất cả | Nhiều tab: lọc 送信予約中の友だち ở tab cũ của bot A khi phiên đã chuyển sang bot C, 全て確認済みに変更 xác nhận đúng hội thoại bot A đang hiển thị | Tài khoản X sở hữu BOT-A-39275 và BOT-C-39275. Bot A có 2 hội thoại chưa xác nhận đang có lịch gửi chờ và 1 hội thoại chưa xác nhận không có lịch gửi. Bot C có 1 hội thoại chưa xác nhận đang có lịch gửi chờ. Ghi lại số tin chưa đọc của bot A (3) và bot C (1) ở màn chọn bot | 1. Tab 1: đăng nhập X, chọn bot A, mở Chat 1:1, chọn bộ lọc 送信予約中の友だち, xác nhận danh sách hiện 2 hội thoại<br>2. Tab 2 cùng trình duyệt: vào màn chọn bot, chuyển sang bot C<br>3. Quay lại tab 1, không tải lại trang, bấm 全て確認済みに変更 rồi 決定<br>4. Sau khi tab 1 tải lại, xoá bộ lọc, xem trạng thái 3 hội thoại của bot A<br>5. Tab 2: mở Chat 1:1 của bot C, xem hội thoại đang có lịch gửi<br>6. Mở màn chọn bot, xem số tin chưa đọc của bot A và bot C | Bộ lọc 送信予約中の友だち; tab 1 giữ bot A đã nạp lúc mở trang, bot của phiên lúc bấm là bot C | Request trả thành công. 2 hội thoại có lịch gửi của bot A mất dấu chưa xác nhận, lịch gửi của 2 hội thoại đó vẫn ở trạng thái chờ, không bị huỷ; hội thoại bot A không có lịch gửi vẫn chưa xác nhận. Số tin chưa đọc bot A = 1. Hội thoại của bot C vẫn chưa xác nhận, số tin chưa đọc bot C vẫn = 1 | | Lấp G1 · Q7 · Q3 · run 2338 NEW-7: bot A 0/2 hội thoại được xác nhận (service dò lịch gửi theo bot phiên) · expected theo quy tắc "toàn bộ = toàn bộ kết quả đang lọc của bot đang thao tác" (NEW-3, kho TC-CHT-35/36) — Leader chốt 2026-09-30 (#39278): xác nhận theo bộ lọc đang chọn, lịch gửi không bị huỷ; phần bot phiên vs bot tab vẫn chờ REQ-009 (2) · Đánh giá spec: Đã hỏi leader · Evidence: ảnh danh sách trước/sau + phản hồi request |
| TC-BULK001-02 | UI | BULK-001 | 全て確認済みに変更 | Normal | auto | Tất cả | Nhiều tab: 全て確認済みに変更 với 4 bộ lọc còn lại, từ khoá và thẻ khi bot của phiên khác bot đang mở | Tài khoản X sở hữu BOT-A-39275 và BOT-C-39275. Bot A có: 2 bạn bè chưa ẩn chưa xác nhận (1 bạn bè có 3 tin chưa đọc), 1 bạn bè đang ẩn còn tin chưa xác nhận, 1 nhóm LINE có tin chưa xác nhận, 1 bạn bè tên chứa 山田 chưa xác nhận, 2 hội thoại gắn thẻ TAG-39275 chưa xác nhận. Bot C có ít nhất 1 hội thoại chưa xác nhận cho mỗi bộ lọc. Dựng lại dữ liệu trước mỗi lần | 1. Tab 1: đăng nhập X, chọn bot A, mở Chat 1:1, áp bộ lọc đầu tiên trong dữ liệu nhập<br>2. Tab 2: chuyển bot của phiên sang bot C<br>3. Tab 1 không tải lại, bấm 全て確認済みに変更 rồi 決定<br>4. Đối chiếu hội thoại bot A trong và ngoài bộ lọc, số tin chưa đọc bot A và bot C<br>5. Dựng lại dữ liệu, lặp với bộ lọc tiếp theo | Lần lượt: 全ての友だち（非表示除く） · 非表示中 · グループ · 未確認 · từ khoá 山田 · thẻ TAG-39275 kết hợp 未確認 | Mỗi lần: chỉ hội thoại bot A đang hiện ở tab 1 theo bộ lọc chuyển sang đã xác nhận; hội thoại bot A ngoài bộ lọc giữ nguyên (全ての友だち（非表示除く）: bạn bè đang ẩn vẫn chưa xác nhận; 非表示中: chỉ bạn bè đang ẩn được xác nhận, bạn bè chưa ẩn giữ nguyên; グループ: chỉ nhóm LINE); số tin chưa đọc bot A bằng số hội thoại bot A còn chưa xác nhận thực tế; toàn bộ hội thoại và số tin chưa đọc bot C không đổi | | Lấp G1 · Q7 · 5 bộ lọc theo Leader chốt 2026-09-30 (#39278) — 送信予約中の友だち ở TC-BULK001-01 · dẫn từ kho TC-CHT-36 + TC-CHT-37, thêm điều kiện bot khác phiên — nhánh fix mới mở · NEW-3 / NEW-14 chỉ test thẻ, NEW-2 test bộ lọc mặc định nhưng không có bạn bè đang ẩn · Đánh giá spec: Đã hỏi leader · Evidence: ảnh + phản hồi từng lần |
| TC-BULK001-03 | UI | BULK-001 | 全て確認済みに変更 | Boundary | auto | Tất cả | Nhiều tab: bộ lọc không khớp hội thoại nào của bot A nhưng khớp hội thoại của bot phiên (bot C) | Tài khoản X sở hữu BOT-A-39275 và BOT-C-39275. Bot A có 2 hội thoại chưa xác nhận, không hội thoại nào có lịch gửi. Bot C có 2 hội thoại chưa xác nhận đang có lịch gửi chờ | 1. Tab 1: đăng nhập X, chọn bot A, mở Chat 1:1, chọn bộ lọc 送信予約中の友だち, danh sách rỗng<br>2. Tab 2: chuyển bot của phiên sang bot C<br>3. Tab 1 không tải lại, bấm 全て確認済みに変更 rồi 決定<br>4. Tab 2: mở Chat 1:1 bot C, xem 2 hội thoại<br>5. Màn chọn bot: xem số tin chưa đọc bot A và bot C | Bộ lọc 送信予約中の友だち; bot A không có lịch gửi, bot C có 2 | Không lỗi. 2 hội thoại bot C vẫn chưa xác nhận, số tin chưa đọc bot C = 2. 2 hội thoại bot A vẫn chưa xác nhận, số tin chưa đọc bot A = 2 | | Lấp G1 · đối chứng âm cho nghi vấn nhánh 送信予約中 dò theo bot phiên (NEW-7) · dẫn từ kho TC-CHT-39 · Đánh giá spec: Spec không ghi · Evidence: ảnh 2 bot |
| TC-PERM001-01 | API | PERM-001 | Phân quyền staff & môi trường | Abnormal | auto | Tất cả | Staff được mời vào bot B với vai trò không có quyền Chat 1:1 gọi thẳng endpoint xác nhận toàn bộ — bị chặn ở máy chủ | Tài khoản Y sở hữu BOT-B-39275, mời tài khoản Z làm staff (đã chấp nhận, không phải quản trị) với vai trò KHÔNG được cấp menu Chat 1:1. Bot B có 2 hội thoại chưa xác nhận. Z có bot riêng làm bot của phiên | 1. Đăng nhập Z, chọn bot riêng của Z<br>2. Mở màn Chat 1:1 của bot B theo đường giao diện, ghi kết quả<br>3. Gửi POST /basic/chat/confirm-message với botIdCurrent = id bot B, các tham số khác như màn Chat 1:1 gửi<br>4. Ghi mã HTTP và phản hồi<br>5. Đăng nhập Y ở trình duyệt khác, mở Chat 1:1 bot B, xem 2 hội thoại và số tin chưa đọc | botIdCurrent = id bot B | Bước 2 bị chặn. Bước 3 bị từ chối với HTTP 403 hoặc 404, không trả kết quả thành công. Ở bước 5: 2 hội thoại bot B vẫn chưa xác nhận, số tin chưa đọc bot B vẫn = 2 | | Lấp G2 · Q1 · dẫn từ kho TC-CHT-423 + TC-CHT-426 · run 2338 NEW-18: endpoint trả HTTP 200 success:true và đổi dữ liệu bot B · expected theo Leader chốt 2026-09-30 (C3): chặn ở cả giao diện và API, API trả 403 hoặc 404 · với code hiện tại dự kiến FAIL → raise bug · Đánh giá spec: Đã hỏi leader · Evidence: phản hồi + ảnh |
| TC-CONC001-01 | UI | CONC-001 | 全て確認済みに変更 | Boundary | auto | Tất cả | Hai người cùng bot bấm 全て確認済みに変更 gần như đồng thời — bộ đếm không âm, không lệch | Tài khoản X (chủ) và staff Z (có quyền Chat 1:1) cùng bot BOT-A-39275, đăng nhập ở 2 trình duyệt riêng. Bot A có 3 hội thoại chưa xác nhận, số tin chưa đọc = 3 | 1. Trình duyệt 1: X mở Chat 1:1 bot A; trình duyệt 2: Z mở Chat 1:1 bot A<br>2. Cả 2 bấm 全て確認済みに変更 để mở hộp thoại<br>3. Bấm 決定 ở 2 trình duyệt cách nhau dưới 1 giây<br>4. Tải lại cả 2 trình duyệt, xem danh sách và badge<br>5. Màn chọn bot: xem số tin chưa đọc bot A | 2 phiên đăng nhập riêng, bấm 決定 cách nhau dưới 1 giây | Cả 2 request trả thành công, không lỗi hệ thống. 3 hội thoại đã xác nhận; badge và số tin chưa đọc bot A = 0, không hiện số âm; không hội thoại nào của bot khác bị đổi | | Lấp Q8 · RULE-01 Boundary cho CONC-001 (NEW-2 Normal, NEW-6 Abnormal) · dẫn từ kho TC-CHT-43 · 2 phiên riêng vì bot context theo session · Đánh giá spec: Spec không ghi · Evidence: ảnh 2 trình duyệt + phản hồi |
| TC-REGSHARED001-01 | API | REG-SHARED-001 | Quick action — xác nhận, ẩn, block | Abnormal | auto | Tất cả | Endpoint cùng họ /basic/update-status-confirm (quick action xác nhận) nhận botIdCurrent của bot tài khoản khác — phải bị chặn | Tài khoản X sở hữu BOT-A-39275; tài khoản Y sở hữu BOT-B-39275, không mời nhau. Bot B có 1 hội thoại chưa xác nhận, đã biết id hội thoại | 1. Đăng nhập X, chọn bot A<br>2. Gửi POST /basic/update-status-confirm với conversationIds = id hội thoại bot B, status = 1, type = 1:1, botIdCurrent = id bot B<br>3. Ghi mã HTTP và phản hồi<br>4. Đăng nhập Y, mở Chat 1:1 bot B, xem hội thoại đó và số tin chưa đọc | conversationIds = id hội thoại bot B; status = 1; botIdCurrent = id bot B | Bị từ chối với HTTP 403 hoặc 404. Hội thoại bot B vẫn chưa xác nhận, số tin chưa đọc bot B không đổi | | Lấp Q11 · regression sibling · căn cứ Studio dev_impact "botIdCurrent thô còn ở ~10 endpoint chat khác" + coverage Studio EP-13 = none + api-spec EP-13 · Dev xác nhận CHƯA sửa trong ticket này → có thể fail: dùng làm bằng chứng cho ticket yokoten, Leader quyết chạy ở vòng này hay chuyển ticket riêng · Đánh giá spec: Spec không ghi · Evidence: phản hồi |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | Bộ đếm chưa xác nhận | Normal | manual | Tất cả | Sau khi xác nhận toàn bộ ở tab cũ (bot khác bot phiên), số tin chưa đọc trên App mobile đúng cho từng bot | Tài khoản X sở hữu BOT-A-39275 (3 hội thoại chưa xác nhận) và BOT-C-39275 (2 hội thoại chưa xác nhận). App mobile đã đăng nhập X | 1. Web tab 1: chọn bot A, mở Chat 1:1<br>2. Web tab 2: chuyển bot của phiên sang bot C<br>3. Tab 1 không tải lại, bấm 全て確認済みに変更 rồi 決定<br>4. Mở App mobile, xem số tin chưa đọc của bot A và bot C<br>5. Trên App mobile mở danh sách chat của bot A và bot C | Không nhập liệu | App mobile: bot A hiện 0 và danh sách chat bot A không còn hội thoại chưa xác nhận; bot C vẫn hiện 2, 2 hội thoại vẫn chưa xác nhận | | Lấp Q12 · dẫn từ kho TC-CHT-398/400 (bộ đếm hiển thị web + App mobile) · hành vi đổi "count ghi theo bot đã kiểm" (Studio dev_impact) · manual vì thiết bị thật App mobile · Đánh giá spec: Spec không ghi · Evidence: ảnh App mobile |
| TC-SYNCAPP001-02 | UI | SYNC-APP-001 | 全て確認済みに変更 | Normal | manual | Tất cả | App mobile: 全て確認済みに変更 xác nhận đúng hội thoại theo từng bộ lọc trong 5 bộ lọc | Tài khoản X sở hữu BOT-A-39275, App mobile đã đăng nhập X và chọn bot A. Bot A có: 2 bạn bè chưa ẩn chưa xác nhận, 1 bạn bè đang ẩn còn tin chưa xác nhận, 1 nhóm LINE có tin chưa xác nhận, 1 bạn bè có lịch gửi chờ chưa xác nhận. Dựng lại dữ liệu trước mỗi lần | 1. Trên App mobile mở danh sách chat của bot A, chọn bộ lọc đầu tiên trong dữ liệu nhập<br>2. Bấm chức năng xác nhận toàn bộ (全て確認済みに変更) và xác nhận<br>3. Xem danh sách theo bộ lọc vừa chọn và danh sách của các bộ lọc khác<br>4. Mở web Chat 1:1 bot A, đối chiếu cùng hội thoại và số tin chưa đọc<br>5. Dựng lại dữ liệu, lặp với bộ lọc tiếp theo | Lần lượt: 全ての友だち（非表示除く） · 非表示中 · グループ · 未確認 · 送信予約中の友だち | Mỗi lần: chỉ hội thoại thuộc bộ lọc đang chọn chuyển sang đã xác nhận, hội thoại ngoài bộ lọc giữ nguyên; lịch gửi chờ không bị huỷ; web hiển thị cùng trạng thái và số tin chưa đọc bot A bằng số hội thoại còn chưa xác nhận | | Lấp Q12 · Leader chốt 2026-09-30 (#39278): chức năng này test đủ 5 bộ lọc trên cả PC và App mobile · chưa rõ App dùng chung EP-12 hay endpoint riêng — nếu dùng chung thì guard mới của fix cũng áp cho App · manual vì thiết bị thật App mobile · Đánh giá spec: Đã hỏi leader · Evidence: ảnh App + web |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/web/api-spec.md` EP-12 (Response) + **fix `ChatController::confirmReadMessage`** | ✅ Chốt 2026-09-30: bị từ chối cross-bot / bot không tồn tại → **403 hoặc 404** (Dev sửa code, đang trả 200 + `success=false`). Còn mở: sai kiểu `botIdCurrent` (chữ, mảng, boolean) = 400 theo RULE-13 hay cũng 403/404 | C1 `CONF-SPEC` | ✅ Leader đã chốt · Dev sửa |
| 2 | `spec-features/admin/chat-11/web/logic-spec.md:240` (Bot scoping) | Nêu nhánh multi-tab: chấp nhận `botIdCurrent` thuộc danh sách bot user có quyền (sở hữu / staff đã chấp nhận), ghi dữ liệu + bộ đếm vào đúng bot đó — hoặc thu hẹp fix về bot phiên | C2 `CONF-SPEC` | PM / Leader |
| 3 | `feature-spec.md` §Actor (Staff) + kho MT-17 + **fix guard** | ✅ Chốt 2026-09-30: staff vai trò không có quyền Chat 1:1 → **chặn ở cả giao diện và API, API trả 403 hoặc 404**. Dev bổ sung kiểm quyền tính năng vào guard (hiện chỉ kiểm phạm vi bot). Cập nhật spec §Actor + đóng MT-17 phần này ở kho | C3 `CONF-KHO` | ✅ Leader đã chốt · Dev sửa |
| 4 | Kho TC-CHT-43 | Chốt oracle double click: bắt buộc chỉ 1 request, hay chấp nhận 2 request miễn không đổi thêm dữ liệu | C4 `CONF-KHO` | Leader |
| 5 | `spec-features/admin/chat-11/web/api-spec.md` EP-12 (Request params) | Spec ghi `conversationIds` bắt buộc và không có `botIdCurrent`; màn thực tế gửi `searchKey / searchTag / page / searchStatusOr / searchStatusAnd / botIdCurrent / lineId / filterTypeFriend / filterFriendOrAnd`, không có `conversationIds` (payload FE run 2338) | Payload thực tế vs spec | Dev |
| 6 | Chat 1:1 — bộ lọc 送信予約中の友だち + phản hồi giao diện khi bị từ chối | REQ-009 (2): bộ lọc lịch gửi ở tình huống multi-tab dò theo bot nào (run 2338 NEW-7: theo bot phiên → bot A không được xác nhận). REQ-009 (3): giao diện có hiện thông báo khi bị từ chối không (hiện FE im lặng) | G1 · Q10 | Leader + Dev |
