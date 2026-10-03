# 05 — Review Report (round 3)

> Draft cho Leader verify. Report chỉ ghi phần THIẾU + việc phải làm.
> Chiều (a) dùng `03-dev-impact.md` + phần `[+0910]` của `03-dev-impact.draft.md` (Journal #135591 — commit `b02fab7a41`, chưa merge vào file 03): `F1`–`F8` · `D1`–`D5` · `T1`–`T5`.
> Khác round 2: bộ TC không đổi (58 TC), nhưng **kết quả chạy đã đổi** — run 2026-09-25 13:17 (AI runner, env `local`) ghi đè `last_exec`: pass giảm từ 41 → 24, 28 TC thành `skip`, 1 TC `fail`.
> **Cập nhật 2026-09-28**: Leader đã chốt C1–C4 (§4) — các dòng liên quan ở §1 G4 · §5 I7 · §7 · §8 đã sửa theo kết luận.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `04-tc-list.md` — snapshot Studio task #177 fetch 2026-09-25 (Studio: MCP LME TEST STUDIO chưa kết nối lúc review) |
| Tổng số TC review | 58 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `BUG` + `F1`–`F8` + `D1`–`D5` + `T1`–`T5` | **8/19 mục có TC pass** — **CHƯA ĐỦ** |
| **(b) diff code** — 5 file + 6 hành vi đổi ở file 03 mục 2/3 (fallback vì Studio mất kết nối) + 3 điểm Studio `dev_impact` round 2 đã ghi | **6/14 điểm có TC pass** — **CHƯA ĐỦ** |

**Kết luận**: chỉ luồng **admin đặt hộ trên web** (salon + lesson) phần sinh action + 「プレビュー」 là có TC pass. **Kỳ vọng số 1 của ticket — khách nhận được tin — hiện 0 TC pass**. Cả 3 luồng của commit `b02fab7a41`, luồng app, cờ 「一度のみ」 đều chưa có kết luận. 2 GAP · 9 RISK.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — Expected 1 của ticket: *"Send được action của friend info cho user"* (output cuối trên LINE) | dev-impact | NEW-10 (salon), NEW-21 (lesson) | **RISK — cả 2 `skip`**. NEW-1 / NEW-11 pass nhưng expected dừng ở bản ghi action trong hệ thống / 「プレビュー」, không kiểm tin tới LINE (RULE-06). NEW-21 đã gắn ticket bug **#40675** nhưng vẫn `skip` → chưa rõ lesson có gửi tới khách thật không | `[BLOCKER]` |
| G2 | `F6` `EventBookingService::callbackChangeBooking` · `D3` · `D4` · `T4` Event Booking (FA-021) | dev-impact + diff code | NEW-53, NEW-54, NEW-55 | **RISK — cả 3 `skip`**. Luồng duy nhất Dev nói *trước đây không ghi dòng lịch sử nào* | `[BLOCKER]` |
| G3 | Webhook đổi lượt đặt sự kiện — không sinh dòng lịch sử / action thừa khi giữ nguyên đáp án, hoặc đáp án thuộc field không phải 選択 (BUG-R5, BUG-R7) | diff code | không có | **GAP** — NEW-53 chỉ test đổi đáp án có action | `[MAJOR]` |
| G4 | `F7` / `F8` `saveInfoFormBooking` (lesson + salon) · `T5` | dev-impact + diff code | NEW-29 | **RISK — TC duy nhất `blocked`**. Leader đã chốt C4: admin **sửa được** 「お客様情報」 sau khi đặt lịch → `blocked` của tester là do chưa bấm 「お客様情報を編集」. Luồng Dev đã sửa test được nhưng **chưa có bằng chứng nào** | `[BLOCKER]` |
| G5 | `D5` `friend_information_value.action` — cờ 「一度のみ」 (UPDATE) · BUG-R6 đổi logic sang xét cờ | dev-impact + diff code | NEW-3, NEW-13, NEW-28 | **RISK — cả 3 `skip`** (round 2 còn pass một phần). Chưa TC nào kiểm phạm vi ghi cờ đúng khách + đúng field (xem Q3) | `[BLOCKER]` |
| G6 | BUG-R6: khách đã nhận action qua luồng khác *"CÓ THỂ nhận thêm đúng 1 lần"* sau deploy | diff code | không có | **GAP** — NEW-28 chỉ dùng dữ liệu sinh sau bản vá (trùng Q5) | `[BLOCKER]` |
| G7 | `D2` · `T3` — dòng lịch sử cũ **không backfill** (BUG-R8) | dev-impact + diff code | NEW-17, NEW-19 (pass) · NEW-18 | **RISK — NEW-18 `fail`**, chưa có ticket bug, chưa rõ fail vì dòng cũ đổi sang 「プレビュー」 (lỗi thật) hay vì môi trường local không có dữ liệu cũ (TC ghi: thiếu dữ liệu thì phải `skip`) | `[BLOCKER]` |
| G8 | 2 file app `Api/CalendarSalonController.php` · `Api/CalendarLessonController.php` (Studio `spec_delta` round 2 — không có trong journal nào) | diff code | NEW-23, NEW-24 | **RISK — cả 2 `skip`**; mỗi màn chỉ 1 TC luồng chính (xem Q4) | `[MAJOR]` |
| G9 | Studio `dev_impact` round 2: khối kích hoạt action copy vào 7 nơi — các nhánh đối chứng âm chỉ test trên web | diff code | NEW-4 / 5 / 8 / 14 (web) | **RISK** — app + event + sửa form không có đối chứng âm; NEW-5 (giá trị không khớp) `skip` | `[MAJOR]` |
| G10 | Studio `dev_impact` round 2: so khớp option value đổi từ `==` sang `(string)!==` | diff code | NEW-55 (chỉ sự kiện) | **RISK — `skip`**; web salon/lesson chưa có case option dạng số | `[MAJOR]` |
| G11 | Studio `dev_impact` round 2: double-click 「予約追加」 phải chặn trùng | diff code | NEW-56, NEW-58, NEW-59 | **RISK — cả 3 `skip`** (trùng Q1) | `[MAJOR]` |

> G8 · G9 · G10 · G11 lấy từ `dev_impact` / `spec_delta` Studio mà round 2 đã đọc (2026-09-25). Round này **không đọc lại được** (MCP mất kết nối) → cần verify lại khi Studio kết nối.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 19 quan điểm Trigger khớp task · 9 chưa cover đủ (round 2: 6).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `CONC-001` | Cao | **RISK** — đủ 3 loại case (NEW-54 / 56 / 58 / 59) nhưng **cả 4 `skip`** | `[MAJOR]` |
| Q2 | `INTG-HOOK-001` | Cao | **RISK** — NEW-53 / 54 / 55 cả 3 `skip` (trùng G2) | `[MAJOR]` |
| Q3 | `DATA-DB-001` ★ | Cao | **GAP** — task có UPDATE `friend_information_value.action` (`D5`) nhưng không TC nào kiểm phạm vi ghi: khách khác / field khác / bot khác có bị ghi cờ theo không. Cờ ghi lan → khách khác không bao giờ nhận action | `[BLOCKER]` |
| Q4 | `SYNC-APP-001` | Trung bình → **Cao** (flow gửi tin cho khách) | **RISK** — NEW-23 / NEW-24 chỉ luồng chính, cả 2 `skip`; thiếu Abnormal + Boundary (RULE-01) | `[MAJOR]` |
| Q5 | `COMPAT-LEGACY-001` / `REG-RUN-001` | Cao | **GAP** — BUG-R6: chưa TC nào dùng dữ liệu 「一度のみ」 có sẵn trước deploy (trùng G6) | `[BLOCKER]` |
| Q6 | `DATA-ID-001` | Trung bình → **Cao** (một lượt đặt gán nhiều field) | **RISK** — TC duy nhất NEW-57 `skip` | `[MAJOR]` |
| Q7 | `MSG-004` | Cao | **RISK** — 4 TC kiểm tin tới LINE thật (NEW-10 / 21 / 41 / 48) **không TC nào pass**: 3 `skip`, NEW-48 `blocked` (trùng G1) | `[BLOCKER]` |
| Q8 | `REG-SHARED-001` / `LIFF-ENTRY-001` | Cao | **RISK** — regression khách tự đặt qua LIFF (NEW-26 / 27 / 28) round 2 pass, nay cả 3 `skip`; chỉ còn NEW-35 (info date) pass | `[MAJOR]` |
| Q9 | `MSG-002` | Cao | **RISK** — NEW-51 / NEW-52 (action course + staff + friend info cùng chạy) `skip`; NEW-49 / 50 cũng `skip` | `[MAJOR]` |

> Loại khỏi phạm vi (có kiểm chứng): `OUT-EXPORT-001` / `INTG-SHEET-001` / `INTG-CAL-001` — diff không chạm dữ liệu export / đồng bộ Google (file sửa đều là nhánh ghi friend info + gửi action). `PAY-STATE-001` — webhook thanh toán ở NEW-53 chỉ làm trigger, bản vá không đổi logic tiền.

---

## 3. TC trùng lặp nội dung

Đã rà 58 TC, **không phát hiện trùng lặp**.

- Các cặp salon ↔ lesson (NEW-1/11, NEW-3/13, NEW-6/15, NEW-7/16, NEW-10/21, NEW-26/27) là song sinh có chủ đích: salon và lesson là 2 bản code khác nhau (salon bọc ghi lịch sử trong điều kiện, lesson gọi thẳng — ghi chú NEW-6 / NEW-15) → giữ nguyên.
- NEW-17 / NEW-18 / NEW-19 cùng kiểm cột 「追加時アクション」 nhưng khác đối tượng (dòng mới · dòng cũ trước bản vá · đối chiếu dữ liệu liên kết) → không phải tập con.

---

## 4. Mâu thuẫn trong TCs

> ✅ **Leader đã chốt cả 4 mâu thuẫn (2026-09-28)** — cột `Leader chốt` là kết luận, cột `Việc cần làm` là thay đổi phải áp lên TC Studio (`testcase_update` / `testcase_delete`) rồi chạy lại.
>
> ✅ **Đã áp lên Studio task #177 (2026-09-28)**: sửa NEW-29 · NEW-36 · NEW-39 · NEW-43 · NEW-44 · NEW-48 · NEW-51 (`testcase_update`), xóa NEW-37 (`testcase_delete`). Studio còn 57 TC. **Còn lại: chạy lại 7 TC vừa sửa.**

| # | Loại | TC liên quan | Nội dung check | Leader chốt | Bên sai | Việc cần làm | Severity |
|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` + `CONF-TC` | NEW-36, NEW-37, NEW-39 | Info kiểu 「年月日」 có 「稼働設定」 (「一度のみ」 / 「何度でも稼働」) không | **Không có** thiết lập chạy 1 lần / nhiều lần | TC sai + spec sai (`friend-information/feature-spec.md:394` ghi 稼働設定 áp cho SCR-FRI-04). Kho `TC-FRI-78` + quan sát của tester đúng. Kết quả **Đạt** của AI runner local 2026-09-25 cho NEW-36 / 37 / 39 **không hợp lệ** — chấm Đạt trên một thiết lập không tồn tại | **NEW-37** (chỉ test 「一度のみ」 của date) → xóa. **NEW-36** → bỏ tiền đề 「何度でも稼働」, giữ trọng tâm "admin đặt hộ đổi ngày → lịch chạy action đăng ký lại theo ngày mới, không để 2 mốc song song". **NEW-39** → bỏ dòng 「稼働設定 = 一度のみ」 ở tiền đề, giữ trọng tâm 「実行しない」. Chạy lại NEW-36 / NEW-39 | `[MAJOR]` |
| C2 | `CONF-SPEC` | NEW-43, NEW-44 | Action của info 「ポイント」 kích hoạt khi điểm **đạt** hay **vượt** ngưỡng | Kích hoạt khi điểm **đúng bằng** ngưỡng; nhảy qua ngưỡng mà không bằng thì **không** kích hoạt | TC sai: NEW-43 đẩy điểm **vượt** ngưỡng (0 → 120 → 150) và đòi mỗi lượt đều gửi tin. Spec BR-02 *"Trigger khi đạt ngưỡng"* đúng nhưng cần ghi rõ | **NEW-43** → đổi dữ liệu để mỗi lượt đưa điểm **đúng bằng** ngưỡng (vd ngưỡng 100: 0 → 100, rồi reset về 0 → 100); expected 2 tin. **NEW-44** → thay câu "giữ nguyên so với trước bản vá ở 3 mức biên" bằng kết quả cụ thể từng mức (dưới / đúng / trên ngưỡng). Lượt đưa điểm vượt qua mà không bằng ngưỡng → expected **không** gửi tin | `[MAJOR]` |
| C3 | `CONF-KHO` | NEW-48, NEW-51 | Thứ tự gửi khi một lượt đặt kích hoạt nhiều action (friend info + course + staff) | **Không đảm bảo** thứ tự | TC sai: NEW-48 đòi *"không sai thứ tự · tin point đến SAU tin multi action"*, NEW-51 tên có *"đúng thứ tự"* | **NEW-48** → bỏ 2 ý về thứ tự, chỉ giữ "đúng 1 tin, đúng nội dung, không trùng". **NEW-51** → bỏ "đúng thứ tự" khỏi tên + bỏ dòng ghi nhận thứ tự ở expected; giữ "đúng 3 tin, đúng nội dung, không thiếu / trùng" | `[MAJOR]` |
| C4 | `CONF-KHO` | NEW-29 | Sau khi đã đặt lịch, admin có sửa được đáp án 「お客様情報」 không | **Sửa được** | Kho `TC-SLN-126` (*"disable không cho sửa"*) và kết quả `blocked` của tester chỉ đúng với **chế độ xem**, chưa bấm link 「お客様情報を編集」. Spec UI salon `ui-spec.md:233` + lesson `ui-spec.md:1404` đúng | NEW-29 bỏ `blocked`, chạy lại theo luồng 「お客様情報を編集」 → 「保存」 — thay bằng 4 TC tách salon / lesson ở §7 (TC-FRIEND001-01…04). Luồng `F7` / `F8` **test được** | `[BLOCKER]` cho tới khi G4 có TC pass |

**Đã rà** 58 TC, đối chiếu `spec-features/admin/friend-information/feature-spec.md` (BR-02, BR-04, dòng 394) · `salon-booking/ui/ui-spec.md` · `lesson-booking/ui/ui-spec.md` và `kho-tcs/fa015-*` · `fa019-*` · `fa020-*` · `fa021-*` (targeted grep) → 4 mâu thuẫn C1–C4, **đã chốt cả 4**; không phát hiện mâu thuẫn mới.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ | Chỉ **24/58 TC (41%) có kết quả `pass`**: 28 `skip` · 5 `blocked` · 1 `fail` | Chạy lại các TC `skip` trên môi trường có LINE OA thật (staging) trước khi đóng ticket |
| I2 | `[BLOCKER]` | NEW-18 | TC **`fail` chưa raise ticket bug**. Nếu dòng lịch sử cũ tự đổi sang 「プレビュー」 hoặc bị gán nhầm action → lỗi thật của bản vá; nếu local không có dòng cũ → TC phải là `skip` theo chính ghi chú của TC | Xem lý do fail trên Studio (`task_get_report`) → raise ticket hoặc đổi sang `skip` + chạy lại trên staging có dữ liệu trước deploy |
| I3 | `[MAJOR]` | 28 TC `skip` (NEW-3, 10, 13, 21, 23, 24, 26, 27, 28, 30, …) | Run AI local 2026-09-25 13:17 **ghi đè `last_exec`**: nhiều TC round 2 đã pass ở staging nay hiển thị `skip`. Không rõ `skip` do local không có LINE OA / app / cổng thanh toán, hay do chưa từng chạy được | Leader xem lịch sử run (`task_get_report`) để lấy lại kết quả staging; TC chỉ chạy được ở staging thì bỏ `local` khỏi `env_scope` |
| I4 | `[MAJOR]` | Toàn bộ | **RULE-08 / ENV-003**: 52 TC chạy `local`, 6 `staging`, **0 production**. Task chạm **job nền** (cột 「プレビュー」 phụ thuộc job xử lý `action_lineuser`) và **webhook thanh toán** (NEW-53…55) | Chạy tối thiểu NEW-10 / NEW-17 / NEW-53 trên production sau release |
| I5 | `[MAJOR]` | Diff vs file 03 | (Round 2, nguồn Studio `spec_delta`) Diff có 2 file app `Api/CalendarSalonController.php` + `Api/CalendarLessonController.php` **không có trong journal nào**; Redmine vẫn ghi *"2 luồng đặt lịch từ app chưa fix"*. Ghi chú NEW-23 / NEW-24 lại nói app được sửa ở `b02fab7a41` | Hỏi Dev 2 file Api thuộc commit / ticket nào (liên quan #40703?) → bổ sung mục 4.1 file 03, sửa ghi chú NEW-23 / NEW-24 |
| I6 | `[MAJOR]` | NEW-3, NEW-13, NEW-28 | **Expected không phán được Đạt/Không đạt**: NEW-3 / 13 trường hợp B ghi *"phải được BA xác nhận trước khi chấm"*, NEW-28 ghi *"KHÔNG tự chấm Đạt/Không đạt"*. Trong khi spec BR-04 đã rõ (`action_mode = 1` → chỉ trigger khi `friend_information_value.action` = NULL) và BUG-R6 xác nhận code nay xét theo cờ này | Sửa expected theo BR-04: trường hợp B **nhận 1 tin**; NEW-28 thứ tự 1 và 2 đều **đúng 1 tin**. NEW-3 / 13 còn không atomic (2 tiền điều kiện A/B) → tách |
| I7 | `[MAJOR]` | NEW-29, 36, 37, 39, 40, 43, 44, 48, 51 | Leader đã chốt C1–C4 → **9 TC phải sửa / xóa trên Studio** trước khi chạy lại: NEW-37 xóa · NEW-36 / 39 bỏ tiền đề 稼働設定 · NEW-43 / 44 sửa theo "đạt ngưỡng" · NEW-48 / 51 bỏ yêu cầu thứ tự · NEW-29 chạy lại qua 「お客様情報を編集」 (hoặc thay bằng §7 G4). **NEW-40** (cột 「追加時アクション」 của info date luôn 「設定なし」) không thuộc C1–C4 — vẫn `blocked`, cần Leader xem riêng | Sửa theo cột `Việc cần làm` ở §4 bằng `testcase_update` / `testcase_delete`, rồi chạy lại |
| I8 | `[MAJOR]` | NEW-29 | **Tên ngược với expected**: tên *"xác nhận VẪN chưa gửi action (known issue ngoài phạm vi)"*, expected đòi *"Khách nhận đúng 1 tin"*. Không atomic (salon + lesson chung 1 TC) | Đổi tên; tách salon / lesson (TC thay thế ở §7 G4) |
| I9 | `[MAJOR]` | NEW-1 | Expected dừng ở bản ghi action trong DB, không kiểm tin tới khách (RULE-06). Không sai vì NEW-10 kiểm phần này, nhưng NEW-10 đang `skip` → hiện không TC salon nào chứng minh khách nhận tin | Chạy NEW-10 (xem G1) |
| I10 | `[MINOR]` | NEW-23, NEW-24 | `Loại case` = `Abnormal` nhưng nội dung là luồng chính | Đổi sang `Normal` |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 58 TC, **không có TC nào ngoài phạm vi** theo đủ 3 tiêu chí. Riêng 1 nhóm nên chuyển sang bộ regression chung:

| # | TC | Vì sao | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-42 … NEW-48 (7 TC 「Lối ghi 2」: multi action ghi point) | Test lớp multi action → info ポイント → action. Diff không chạm lớp này: bản vá chỉ thêm code vào nhánh field kiểu 「選択」 (BUG-R5) | File 03 mục 3 không có file action engine / multi action | Giữ làm regression của ma trận friend info action nhưng đưa vào bộ regression chung của kho FA-015, không chạy lại mỗi vòng fix #38443 | `[NIT]` |

- Gate: X1 không phải TC duy nhất cover quan điểm nào đang Trigger (`FRIEND-001` đã có NEW-2 / NEW-12 / NEW-31 / NEW-32 pass).

---

## 7. TCs đề xuất bổ sung (12)

> ✅ **Đã sync lên Studio task #177 (2026-09-28)** — 9 TC, mã đã đổi để không trùng `client_ref` có sẵn: TC-INTGHOOK001-02 → **NEW-60** · TC-INTGHOOK001-03 → **NEW-61** · TC-FRIEND001-11 → **NEW-62** · TC-FRIEND001-12 → **NEW-63** · TC-SYNCAPP001-03 → **NEW-64** · TC-SYNCAPP001-04 → **NEW-65** · TC-FUNC004-06 → **NEW-66** · TC-DATADB001-01 → **NEW-67** · TC-DATADB001-02 → **NEW-68**.
> **Không sync**: TC-FRIEND001-01 / -02 (trùng NEW-29 sau khi Leader chốt sửa NEW-29) · TC-COMPATLEGACY001-01 (Leader loại).

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` · `fa019-datlichbaihoc-レッスン予約.md` · `fa020-datlichsalon-サロン・面談予約.md` · `fa021-eventbooking-イベント予約.md` (targeted grep) |
| Vùng regression phát hiện từ kho | FA-020 / FA-019 「Detail booking & lịch sử」 (`TC-SLN-126`) · FA-015 「Ghi giá trị từ màn admin」 (`TC-FRI-213`) · FA-021 「LINE user — đổi lịch」 (`TC-EBK-186`, `TC-EBK-187`) |
| Conflict expected vs kho | `TC-FRIEND001-01…04` (sửa 「お客様情報」) vs `TC-SLN-126` → C4 **đã chốt: sửa được** → TC đúng, kho `TC-SLN-126` cần sửa (§8 #4) |
| GAP / RISK dùng lại TC có sẵn (chạy lại, không viết mới) | G1 / Q7 → NEW-10, NEW-21 · G2 / Q2 → NEW-53 / 54 / 55 · G11 / Q1 → NEW-56 / 58 / 59 · Q6 → NEW-57 · Q8 → NEW-26 / 27 / 28 · Q9 → NEW-49…52 · G7 → triage NEW-18 (I2) |
| Căn cứ TC regression `R<x>` | R1 ← kho `TC-FRI-213` (xóa trắng giá trị trường Lựa chọn có action → không kích hoạt action ngoài ý) áp vào luồng sửa form mới (`F7` / `F8`) |
| Xác nhận chống trùng | Đã đối chiếu 58 TC ở BƯỚC 0 + 4 file kho — không TC đề xuất nào trùng. 12 TC này giữ nguyên nội dung round 2 (chưa được tạo trên Studio — Studio vẫn 58 TC) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGHOOK001-02 | UI | INTG-HOOK-001 | Event booking (イベント予約) — LINE user đổi lịch đặt chỗ | Boundary | auto | Tất cả | Event booking - Khách đổi lịch đặt chỗ sự kiện nhưng giữ nguyên đáp án kiểu lựa chọn thì không sinh dòng lịch sử mới và không gửi lại action | - Sự kiện 「TC38443_イベント」 có thanh toán UnivaPay, có 2 slot A và B còn chỗ<br>- Cả slot A và slot B đặt 「予約変更」 = 「全承認」, 「変更受付期限」 còn hạn<br>- Biểu mẫu đặt chỗ của sự kiện có câu hỏi liên kết field 「TC38443_選択E」 kiểu 選択肢, 「何度でも稼働」, 「オプションE1」 gắn action 「TC38443_ACT_E1」<br>- Khách T177_EV đã đặt 1 lượt ở slot A, trả lời 「オプションE1」, đã thanh toán và đã nhận 1 tin của 「TC38443_ACT_E1」 | 1. Ghi lại số dòng lịch sử của 「TC38443_選択E」 ở 「友だち詳細」 → tab 「友だち情報」 và số tin trong phòng chat LINE của T177_EV<br>2. T177_EV mở trang đặt chỗ sự kiện từ LINE → 「予約履歴」 → bấm 「詳細確認」 ở lượt đặt slot A<br>3. Ở màn 「予約詳細」 bấm 「予約内容変更」, chọn slot B<br>4. Ở câu hỏi liên kết 「TC38443_選択E」 giữ nguyên 「オプションE1」 → bấm 「決済する」 và hoàn tất thanh toán<br>5. Chờ màn 「決済処理を行っています」 kết thúc và khách nhận tin báo kết quả thanh toán<br>6. Đếm lại số dòng lịch sử và số tin | Đáp án: 「オプションE1」 (không đổi) · slot A → slot B | - Đổi lịch thành công, 「予約履歴」 hiện lượt đặt ở slot B<br>- Bảng lịch sử không có dòng mới cho 「TC38443_選択E」<br>- Khách không nhận thêm tin của 「TC38443_ACT_E1」 (ngoài tin báo thanh toán / action 「予約変更時」 nếu sự kiện có cấu hình) | | Lấp G3 · BUG-R7 + Studio dev_impact "cần kiểm không sinh dòng lịch sử thừa" · Chỉ Event booking cho LINE user đổi lịch — salon / lesson không có tính năng này (Leader 2026-09-28) · Luồng đi qua webhook UnivaPay module event_booking_change → callbackChangeBooking (event-booking feature-spec.md:1052-1062) · Đánh giá spec: Spec ghi rõ (SCR-EBD-20f) · Evidence: ảnh bảng lịch sử trước/sau + ảnh phòng chat |
| TC-INTGHOOK001-03 | UI | INTG-HOOK-001 | Event booking (イベント予約) — LINE user đổi lịch đặt chỗ | Abnormal | auto | Tất cả | Event booking - Khách đổi lịch đặt chỗ sự kiện và sửa đáp án field không phải kiểu lựa chọn thì không phát sinh action thông tin bạn bè | - Như TC-INTGHOOK001-02 (sự kiện có thanh toán UnivaPay, slot A và B đặt 「予約変更」 = 「全承認」, còn hạn đổi)<br>- Biểu mẫu đặt chỗ có thêm câu hỏi liên kết field 「TC38443_記述E」 kiểu 記述<br>- Khách T177_EV đang có 1 lượt đặt ở slot A | 1. Ghi lại số tin trong phòng chat của T177_EV và số dòng lịch sử của 「TC38443_記述E」<br>2. T177_EV mở trang đặt chỗ sự kiện từ LINE → 「予約履歴」 → 「詳細確認」 → bấm 「予約内容変更」, chọn slot B<br>3. Sửa câu trả lời 「TC38443_記述E」 thành giá trị mới, giữ nguyên các câu khác → bấm 「決済する」 và hoàn tất thanh toán<br>4. Chờ xử lý thanh toán xong<br>5. Mở 「友だち詳細」 → 「友だち情報」 và xem phòng chat | 「TC38443_記述E」: 「変更テスト」 · slot A → slot B | - Đổi lịch thành công<br>- Giá trị 「TC38443_記述E」 cập nhật thành 「変更テスト」, có đúng 1 dòng lịch sử mới, cột 「追加時アクション」 = 「設定なし」<br>- Khách không nhận tin action thông tin bạn bè nào<br>- Không lỗi hệ thống | | Lấp G3 · BUG-R5 "chỉ nhánh 選択 được chạm" · Chỉ Event booking có đổi lịch phía LINE user (salon / lesson không có) · Evidence: ảnh tab 友だち情報 + phòng chat |
| TC-FRIEND001-01 | UI | FRIEND-001 | Detail booking & lịch sử (salon) | Normal | auto | Tất cả | Salon - Admin sửa đáp án kiểu lựa chọn ở 「お客様情報を編集」 của lượt đặt đã có thì khách nhận action và lịch sử hiện 「プレビュー」 | - Lịch 「TC38443_サロン」, field 「TC38443_選択A」 「何度でも稼働」, 「オプションA」 gắn action 「TC38443_ACT_A」, 「オプションB」 không gắn action<br>- Khách T177_USER đã có 1 lượt đặt, đáp án 「オプションB」 | 1. Ghi lại số tin trong phòng chat và số dòng lịch sử của 「TC38443_選択A」<br>2. Mở 「予約カレンダー」 → bấm lượt đặt của T177_USER → sub-tab 「お客様情報」<br>3. Bấm 「お客様情報を編集」, đổi câu hỏi liên kết sang 「オプションA」 → 「保存」<br>4. Chờ job xử lý action xong<br>5. Xem phòng chat LINE của T177_USER<br>6. Mở 「友だち詳細」 → 「友だち情報」, bấm 「プレビュー」 ở dòng lịch sử mới | 「オプションB」 → 「オプションA」 | - Lưu thành công, sub-tab 「お客様情報」 hiện 「オプションA」<br>- Khách nhận đúng 1 tin của 「TC38443_ACT_A」<br>- Bảng lịch sử có 1 dòng mới, cột 「追加時アクション」 = 「プレビュー」, bấm vào mở đúng nội dung 「TC38443_ACT_A」 | | Lấp G4 · thay NEW-29 (tách salon) · Đánh giá spec: Spec ghi rõ (salon ui-spec.md:233) · Evidence: ảnh phòng chat + ảnh preview |
| TC-FRIEND001-02 | UI | FRIEND-001 | Detail booking & lịch sử (lesson) | Normal | auto | Tất cả | Lesson - Admin sửa đáp án kiểu lựa chọn ở 「お客様情報を編集」 của lượt đặt đã có thì khách nhận action và lịch sử hiện 「プレビュー」 | - Lịch 「TC38443_レッスン」, field 「TC38443_選択L」 「何度でも稼働」, 「オプションL1」 gắn action 「TC38443_ACT_L1」, 「オプションL2」 không gắn action<br>- Khách T177_USER2 đã có 1 lượt đặt, đáp án 「オプションL2」 | 1. Ghi lại số tin + số dòng lịch sử<br>2. Mở lịch lesson → lượt đặt của T177_USER2 → 「予約情報」 → 「お客様情報」<br>3. Bấm 「お客様情報を編集」, đổi sang 「オプションL1」 → 「保存」<br>4. Chờ job xử lý xong<br>5. Xem phòng chat + tab 「友だち情報」 | 「オプションL2」 → 「オプションL1」 | - Lưu thành công<br>- Khách nhận đúng 1 tin của 「TC38443_ACT_L1」<br>- Dòng lịch sử mới có 「プレビュー」 mở đúng nội dung | | Lấp G4 · thay NEW-29 (tách lesson) · Đánh giá spec: Spec ghi rõ (lesson ui-spec.md:1404) · Evidence: ảnh phòng chat + ảnh preview |
| TC-FRIEND001-11 | UI | FRIEND-001 | Detail booking & lịch sử (salon) | Boundary | auto | Tất cả | Salon - Sửa 「お客様情報」 với field 「一度のみ」 mà khách đã nhận action thì không gửi lại | - Field 「TC38443_選択A」 「一度のみ」, 「オプションA」 và 「オプションC」 đều gắn action<br>- T177_USER đã nhận action của field này qua 1 lượt đặt hộ (chọn 「オプションA」) | 1. Ghi lại số tin + số dòng lịch sử<br>2. Mở lượt đặt đó → 「お客様情報を編集」 → đổi sang 「オプションC」 → 「保存」<br>3. Chờ job xử lý<br>4. Xem phòng chat + tab 「友だち情報」 | 「オプションA」 → 「オプションC」 | - Giá trị cập nhật 「オプションC」, có 1 dòng lịch sử mới<br>- Khách không nhận thêm tin<br>- Cột 「追加時アクション」 của dòng mới = 「設定なし」 | | Lấp G4 · Đánh giá spec: Spec ghi rõ (friend-information BR-04) · Evidence: ảnh phòng chat + bảng lịch sử |
| TC-FRIEND001-12 | UI | FRIEND-001 | Detail booking & lịch sử (lesson) | Abnormal | auto | Tất cả | Lesson - Sửa 「お客様情報」 xóa trắng đáp án kiểu lựa chọn thì không kích hoạt action ngoài ý muốn | - Field 「TC38443_選択L」 「何度でも稼働」, 「オプションL1」 gắn action<br>- T177_USER2 có lượt đặt, đáp án 「オプションL1」, câu hỏi không bắt buộc | 1. Ghi lại số tin<br>2. Mở lượt đặt → 「お客様情報を編集」 → bỏ chọn câu hỏi liên kết → 「保存」<br>3. Chờ job xử lý<br>4. Xem phòng chat + tab 「友だち情報」 | Đáp án: (trống) | - Lưu thành công, không lỗi hệ thống<br>- Khách không nhận tin nào<br>- Tab 「友だち情報」 hiển thị giá trị trống (hoặc giữ nguyên — ghi nhận hành vi thật cho Leader) | | Lấp R1 · regression · dẫn từ kho TC-FRI-213 · Evidence: ảnh phòng chat + tab 友だち情報 |
| TC-SYNCAPP001-03 | UI | SYNC-APP-001 | App mobile (salon) | Boundary | manual | Tất cả | Salon app - Field 「一度のみ」 khách đã nhận action thì admin đặt hộ lại trên app không gửi lần 2 | - App quản trị di động đã đăng nhập bot A<br>- Field 「TC38443_選択A」 「一度のみ」, 「オプションA」 gắn action<br>- T177_USER đã nhận action của field này qua 1 lượt đặt hộ trên web | 1. Ghi lại số tin trong phòng chat của T177_USER<br>2. Trên app: mở lịch 「TC38443_サロン」 → thêm lượt đặt cho T177_USER, chọn 「オプションA」 → đăng ký<br>3. Chờ job xử lý<br>4. Trên web mở 「友だち詳細」 → 「友だち情報」<br>5. Xem phòng chat | 「オプションA」 | - Đặt lịch thành công trên app, hiển thị đúng trên web<br>- Khách không nhận thêm tin<br>- Dòng lịch sử mới (nếu có) = 「設定なし」 | | Lấp G8 + G9 + Q4 · manual vì app admin mobile (thiết bị thật) · Evidence: ảnh app + phòng chat |
| TC-SYNCAPP001-04 | UI | SYNC-APP-001 | App mobile (lesson) | Abnormal | manual | Tất cả | Lesson app - Chọn lựa chọn không gắn action thì không sinh action và lịch sử hiện 「設定なし」 | - App quản trị di động đã đăng nhập bot A<br>- Field 「TC38443_選択L」, 「オプションL2」 không gắn action<br>- T177_USER2 chưa có giá trị cho field | 1. Ghi lại số tin<br>2. Trên app: thêm lượt đặt lesson cho T177_USER2, chọn 「オプションL2」 → đăng ký<br>3. Trên web mở tab 「友だち情報」 của T177_USER2<br>4. Xem phòng chat | 「オプションL2」 | - Đặt chỗ thành công, giá trị = 「オプションL2」, có 1 dòng lịch sử, cột 「追加時アクション」 = 「設定なし」<br>- Khách không nhận tin action nào<br>- Không lỗi trên app | | Lấp G8 + G9 + Q4 · manual vì app admin mobile (thiết bị thật) · Evidence: ảnh app + tab 友だち情報 |
| TC-FUNC004-06 | UI | FUNC-004 | Admin thêm booking thủ công (salon) | Boundary | auto | Tất cả | Salon - Lựa chọn có tên dạng số gần giống nhau thì đặt hộ chỉ kích hoạt action của đúng lựa chọn được chọn | - Field 「TC38443_選択N」 kiểu 選択肢 「何度でも稼働」, 2 lựa chọn tên 「1」 và 「01」, mỗi lựa chọn gắn action riêng: 「ACT_1」 (text 「一番」), 「ACT_01」 (text 「ゼロ一番」)<br>- Form đặt lịch salon có câu hỏi liên kết field này<br>- T177_NUM chưa có giá trị | 1. Mở modal 「予約追加」 → chọn T177_NUM → chọn 「01」 → đăng ký<br>2. Chờ job xử lý, xem phòng chat<br>3. Đặt hộ lượt thứ 2 cho T177_NUM, chọn 「1」<br>4. Chờ job, xem phòng chat + tab 「友だち情報」 | 「01」 rồi 「1」 | - Lượt 1: khách nhận đúng 1 tin 「ゼロ一番」, không nhận 「一番」<br>- Lượt 2: khách nhận đúng 1 tin 「一番」<br>- Mỗi dòng lịch sử mở 「プレビュー」 đúng action của lựa chọn đó | | Lấp G10 · Studio dev_impact "so khớp đổi từ == sang (string)!==" · Evidence: ảnh phòng chat + preview từng dòng |
| TC-DATADB001-01 | UI | DATA-DB-001 | Admin thêm booking thủ công (salon) | Normal | auto | Tất cả | Salon - Cờ 「一度のみ」 chỉ ghi cho đúng khách và đúng field vừa đặt hộ | - Field X 「TC38443_選択A」 và field Y 「TC38443_選択B」, cả 2 「一度のみ」, lựa chọn đều gắn action (「ACT_A」, 「ACT_B」)<br>- 2 khách T177_DB1, T177_DB2 chưa có giá trị ở X và Y<br>- Form đặt lịch có câu hỏi liên kết X và Y | 1. Đặt hộ T177_DB1, chỉ trả lời X → đăng ký → chờ job<br>2. Đặt hộ T177_DB2, chỉ trả lời X → đăng ký → chờ job<br>3. Đặt hộ T177_DB1 lần 2, chỉ trả lời Y → đăng ký → chờ job<br>4. Đếm tin của từng khách | X = 「オプションA」, Y = 「オプションB」 | - Bước 1: T177_DB1 nhận 1 tin 「ACT_A」<br>- Bước 2: T177_DB2 vẫn nhận 1 tin 「ACT_A」 (cờ của DB1 không lan sang DB2)<br>- Bước 3: T177_DB1 nhận 1 tin 「ACT_B」 (cờ field X không lan sang field Y) | | Lấp Q3 + G5 · Boundary đã có NEW-3 / NEW-13 · Đánh giá spec: Spec ghi rõ (BR-04) · Evidence: ảnh phòng chat 2 khách |
| TC-DATADB001-02 | UI | DATA-DB-001 | Admin thêm booking thủ công (lesson) | Abnormal | auto | Tất cả | Lesson - Đặt hộ ở bot A không làm mất action 「一度のみ」 của bot B có field cùng tên | - Bot A và bot B đều có field 「TC38443_選択L」 「一度のみ」, 「オプションL1」 gắn action (bot A: 「ACT_A_L1」, bot B: 「ACT_B_L1」)<br>- Cùng tài khoản LINE test đã kết bạn cả 2 bot, chưa có giá trị ở cả 2<br>- Dùng 2 phiên đăng nhập riêng cho bot A / bot B | 1. Phiên bot A: đặt hộ lesson cho khách, chọn 「オプションL1」 → chờ job<br>2. Phiên bot B: đặt hộ lesson cho cùng khách, chọn 「オプションL1」 → chờ job<br>3. Xem phòng chat của khách với từng bot | 「オプションL1」 ở cả 2 bot | - Phòng chat bot A: 1 tin 「ACT_A_L1」<br>- Phòng chat bot B: vẫn nhận 1 tin 「ACT_B_L1」<br>- Tab 「友だち情報」 của mỗi bot chỉ có dòng lịch sử của bot đó | | Lấp Q3 · WHERE scope 2 tài khoản (DATA-DB-001 ★) · Evidence: ảnh phòng chat 2 bot |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Dữ liệu cũ & hồi quy (salon) | Normal | manual | staging | Salon - Khách đã nhận action 「一度のみ」 trước khi deploy bản vá thì admin đặt hộ sau deploy gửi tối đa thêm 1 lần | - Trên build trước bản vá: field 「TC38443_選択A」 「一度のみ」, 「オプションA」 gắn action; khách T177_OLD đã nhận tin action này qua khách tự đặt lịch (LIFF) hoặc qua 「友だち詳細」<br>- Sau đó deploy branch ai_fixbug_38443 | 1. Sau deploy, ghi lại số tin của T177_OLD<br>2. Admin đặt hộ salon cho T177_OLD, chọn 「オプションA」 → đăng ký → chờ job<br>3. Đếm tin<br>4. Admin đặt hộ lần nữa, cùng lựa chọn → chờ job<br>5. Đếm tin | 「オプションA」 | - Bước 3: khách nhận tối đa 1 tin (BUG-R6) — ghi nhận có/không để PO chấp nhận<br>- Bước 5: khách không nhận thêm tin (cờ đã được ghi) | | Lấp G6 + Q5 · BUG-R6 (Journal #135591) · manual vì cần dựng dữ liệu trên build cũ rồi deploy · Evidence: ảnh phòng chat trước/sau deploy |

---

## 8. Spec update needed

| # | Section spec / kho | Nội dung cần update | Nguồn | Ai làm |
|---|---|---|---|---|
| 1 | `spec-features/admin/friend-information/feature-spec.md:394` | Bỏ **SCR-FRI-04** (kiểu 年月日) khỏi danh sách màn có 「稼働設定」 — Leader chốt date không có chạy 1 lần / nhiều lần | C1 (đã chốt) | Người giữ `spec-features/` |
| 2 | `spec-features/admin/friend-information/feature-spec.md` BR-02 (ポイント: *"Trigger khi đạt ngưỡng"*) | Ghi rõ "đạt" = điểm **đúng bằng** ngưỡng thì kích hoạt, nhảy qua ngưỡng mà không bằng thì **không** kích hoạt (Leader chốt 2026-09-28). Kho `TC-FRI-94` bước U3 (150 điểm) đổi từ "ghi nhận thực tế" sang expected cụ thể | C2 (đã chốt) | Người giữ spec + `kho-tcs/data/` FA-015 |
| 3 | Kho FA-020 / FA-019 — các TC gửi nhiều action cùng lúc | Ghi rõ **không đảm bảo thứ tự gửi** giữa action friend info / course / staff. (`MT-10` về **ưu tiên** action course/staff vs action chung là câu hỏi khác — vẫn để nguyên trạng thái) | C3 (đã chốt) | `kho-tcs/data/` FA-020 |
| 4 | Kho `TC-SLN-126` (FA-020 「Detail booking & lịch sử」) | Sửa: chế độ xem disable, nhưng bấm 「お客様情報を編集」 thì **sửa được** và 「保存」 lưu thật. Bổ sung TC tương đương cho lesson (FA-019) nếu chưa có | C4 (đã chốt) | `kho-tcs/data/` FA-020 + FA-019 → `python kho-tcs/build.py md` + `sheet` |
| 5 | `03-dev-impact.md` mục 4.1 | Bổ sung `Api/CalendarSalonController.php` + `Api/CalendarLessonController.php` (có trong diff, không có trong journal); xác nhận quan hệ với bug #40703 | I5 §5 | Dev |
| 6 | `event-booking` — luồng đổi lượt đặt | Nêu rõ những đường nào đi qua `callbackChangeBooking`: chỉ webhook UnivaPay? Stripe? Đổi lượt 全承認 không thanh toán? Admin duyệt đổi lượt リクエスト制 (kho `TC-EBK-187`)? → quyết định có cần nhân NEW-53 cho từng đường | G2 §1 | Dev |
