# 05 — Review Report (round 2)

> Draft cho Leader verify. Report chỉ ghi phần THIẾU + việc phải làm.
> Chiều (a) dùng `03-dev-impact.md` **+ phần `[+0910]` của `03-dev-impact.draft.md`** (Journal #135591 — commit `b02fab7a41`, chưa merge vào file 03): `F6`–`F8` · `D3`–`D5` · `T4`–`T5`.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) MCP LME TEST STUDIO — task #177 (ticket 38443, round 1, branch `ai_fixbug_38443`) |
| Tổng số TC review | 58 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `BUG` + `F1`–`F8` + `D1`–`D5` + `T1`–`T5` | **12/19 mục có TC** — **CHƯA ĐỦ** |
| **(b) diff code** — 7 file `spec_delta` + 8 điểm Studio `dev_impact` | **8/15 điểm có TC** — **CHƯA ĐỦ** |

**Kết luận**: luồng **admin đặt hộ trên web** (salon + lesson) và luồng khách tự đặt đã đủ TC pass. **Cả 3 luồng Dev bổ sung ở commit `b02fab7a41`** (webhook đổi lượt đặt sự kiện · sửa 「お客様情報」 của lượt đặt salon · của lượt đặt lesson) **chưa có TC nào pass**. Tổng: 2 GAP · 5 RISK.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `F6` `EventBookingService::callbackChangeBooking` · `D3` · `D4` · `T4` Event Booking (FA-021) — file `EventBookingService.php` (+42/−21) | dev-impact + diff code | NEW-53, NEW-54, NEW-55 | **RISK — cả 3 TC chưa chạy.** Đây là file sửa nhiều nhất của diff và là luồng duy nhất Dev nói *trước đây không ghi dòng lịch sử nào* | `[BLOCKER]` |
| G2 | Studio `dev_impact`: *"EventBookingService … nay thêm recordFriendInfoHistory('8001') … cần kiểm **không sinh dòng lịch sử thừa**"* | diff code | không có | **GAP** — NEW-53 chỉ test đổi đáp án có action. Chưa TC nào đổi lượt đặt mà **giữ nguyên đáp án**, hoặc đáp án thuộc field **không phải 選択** | `[MAJOR]` |
| G3 | `F7` / `F8` `saveInfoFormBooking` (lesson + salon) · `T5` — file `Basic/CalendarManagementController.php`, `Basic/CalendarSalonController.php` | dev-impact + diff code | NEW-29 | **RISK — TC duy nhất đang `blocked`** vì tester ghi *"sau khi booking rồi thì không sửa được nữa"*. Trong khi spec UI salon + lesson đều có link 「お客様情報を編集」 → nút 「保存」 gọi `saveInfoFormBooking` (xem C4 §4). Hiện **chưa có bằng chứng nào** cho luồng Dev đã sửa | `[BLOCKER]` |
| G4 | Studio `dev_impact`: *"double-click 予約追加 cũng cần chặn trùng"* | diff code | NEW-56 (+ NEW-58, NEW-59) | **RISK — chưa chạy** | `[MAJOR]` |
| G5 | Studio `dev_impact`: *"khối copy-paste vào **7 nơi** … sai lệch nhỏ giữa các bản … cần rà cả 7 nhánh"* | diff code | Web: NEW-1…NEW-20 · App: NEW-23, NEW-24 · Event/sửa form: xem G1/G3 | **RISK** — các nhánh đối chứng âm (không gắn action · 「一度のみ」 đã chạy · gán lại cùng giá trị) **chỉ test trên web**. Nhánh **app** chỉ có 1 TC luồng chính mỗi màn | `[MAJOR]` |
| G6 | Studio `dev_impact`: *"So khớp option value đổi từ `==` sang `(string)!==` ⇒ giá trị dạng số/định dạng lệch có thể đổi kết quả gửi"* | diff code | NEW-55 (chỉ sự kiện, chưa chạy) | **RISK** — chưa có TC pass nào; web salon/lesson chưa có case option dạng số | `[MAJOR]` |
| G7 | `D5` `friend_information_value.action` — cờ 「一度のみ」 (thao tác **UPDATE**) | dev-impact | NEW-3, NEW-13, NEW-28 | **RISK** — chưa có TC kiểm phạm vi ghi cờ: cờ chỉ được ghi cho **đúng khách + đúng field** (xem Q3) | `[BLOCKER]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 19 quan điểm Trigger khớp task · 6 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `CONC-001` | Cao | **RISK** — có đủ 3 loại case (NEW-54 / 56 / 58 / 59) nhưng **cả 4 TC chưa chạy** | `[MAJOR]` |
| Q2 | `INTG-HOOK-001` | Cao | **RISK** — N/A/B = NEW-53 / NEW-54 / NEW-55, **cả 3 chưa chạy** (trùng G1) | `[MAJOR]` |
| Q3 | `DATA-DB-001` ★ | Cao | **GAP** — task có UPDATE `friend_information_value.action` (`D5`) nhưng không TC nào kiểm phạm vi `WHERE`: khách khác / field khác / bot khác có bị ghi cờ theo không. Nếu cờ ghi lan thì khách khác sẽ **không bao giờ nhận action** | `[BLOCKER]` |
| Q4 | `SYNC-APP-001` | Trung bình → **Cao** (flow gửi tin cho khách) | **RISK** — NEW-23 / NEW-24 chỉ có luồng chính; thiếu Abnormal + Boundary trên app (RULE-01), trong khi app là 2/7 bản copy của khối logic (G5) | `[MAJOR]` |
| Q5 | `COMPAT-LEGACY-001` / `REG-RUN-001` | Cao | **GAP** — Dev nêu (`BUG-R6`, Journal #135591): 「一度のみ」 nay xét theo cờ, *"khách đã nhận action qua luồng khác CÓ THỂ nhận thêm đúng 1 lần"*. NEW-28 chỉ test dữ liệu sinh **sau** bản vá. Chưa TC nào dùng **dữ liệu có sẵn trước khi deploy** | `[BLOCKER]` |
| Q6 | `DATA-ID-001` | Trung bình → **Cao** (một lượt đặt gán nhiều field) | **RISK** — TC duy nhất NEW-57 chưa chạy | `[MAJOR]` |

> Loại khỏi phạm vi (có kiểm chứng): `OUT-EXPORT-001` / `INTG-SHEET-001` / `INTG-CAL-001` — diff không chạm dữ liệu export/đồng bộ Google (7 file đều là nhánh ghi friend info + gửi action). `PAY-STATE-001` — NEW-53 dùng webhook thanh toán chỉ làm trigger, bản vá không đổi logic tiền. `LIFF-ENTRY-001` — đã có NEW-26 / NEW-27 pass.

---

## 3. TC trùng lặp nội dung

Đã rà 58 TC, **không phát hiện trùng lặp**.

- Các cặp salon ↔ lesson (NEW-1/11, NEW-3/13, NEW-6/15, NEW-7/16, NEW-10/21, NEW-26/27) là **song sinh có chủ đích**: Studio `dev_impact` nêu 2 bản code khác nhau (*"salon gói history trong if changed, lesson gọi thẳng"*) → giữ nguyên.
- NEW-17 / NEW-18 / NEW-19 cùng kiểm cột 「追加時アクション」 nhưng khác đối tượng (dòng mới · dòng cũ trước bản vá · đối chiếu toàn bảng) → không phải tập con của nhau.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected của TC | Nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-36, NEW-37 | Info kiểu 「年月日」 (date) có 「稼働設定」 「一度のみ」 / 「何度でも稼働」 hay không | Có: NEW-36 kiểm 「何度でも稼働」, NEW-37 kiểm 「一度のみ」 cho date | Kho `TC-FRI-78` (màn tạo kiểu 年月日): chỉ có dropdown 「登録」 「月日」/「年月日」 + 2 ghi chú, **không có 稼働設定**. Tester (run 2026-09-10): *"Friend infor type date không có setting action 1 lần hay nhiều lần"*. ⚠️ Nhưng `friend-information/feature-spec.md` dòng 394 ghi 「稼働設定」 có ở `SCR-FRI-04` (màn kiểu date) | NEW-36 / NEW-37 sai chuẩn (test một thiết lập không tồn tại) **hoặc** spec đúng mà UI bị ẩn thiết lập | `[MAJOR]` | Leader / BA |
| C2 | `CONF-SPEC` | NEW-43, NEW-44 | Action của info 「ポイント」 kích hoạt khi điểm **đạt** hay **vượt** ngưỡng | Kích hoạt khi multi action đẩy điểm **vượt** ngưỡng (0 → 120 → 150) | `friend-information/feature-spec.md` BR-02: *"Trigger khi đạt ngưỡng"* (không nói rõ = hay ≥). Tester: *"chỉ send khi đạt đúng số point đã setting, chứ không send mỗi khi vượt ngưỡng"*. Kho `TC-FRI-94` để trường hợp 150 điểm ở dạng *"ghi nhận thực tế"* | TC sai (hiểu "đạt" thành "≥") **hoặc** spec cần ghi rõ "= đúng ngưỡng" | `[MAJOR]` | BA |
| C3 | `CONF-KHO` | NEW-48, NEW-51 | Thứ tự gửi khi một lượt đặt kích hoạt nhiều action (friend info + course + staff) | Chạy *"đúng số lượng, đúng nội dung, **đúng thứ tự**"* | Tester: *"ko đảm bảo thứ tự send"*. Kho FA-020 `MT-10` (thứ tự ưu tiên action course/staff vs action chung) còn **⏳ CHỜ QUYẾT ĐỊNH** | TC tự đặt ra quy tắc thứ tự chưa ai chốt **hoặc** hệ thống cần đảm bảo thứ tự | `[MAJOR]` | Leader / PO |
| C4 | `CONF-KHO` | NEW-29 | Sau khi đã đặt lịch, admin có sửa được đáp án 「お客様情報」 không | Sửa được; lưu xong khách nhận action | Spec UI: salon `ui-spec.md:233` + lesson `ui-spec.md:1404` có link 「お客様情報を編集」 → 「保存」 → `POST /ajax/calendar/save-info-form-booking`. Ngược lại kho `TC-SLN-126`: *"Toàn bộ ô bị disable, KHÔNG sửa được"*, tester cũng ghi không sửa được | Kho + tester mới nhìn chế độ xem (chưa bấm 「お客様情報を編集」) **hoặc** link đã bị gỡ khỏi UI mà spec chưa cập nhật (khi đó code Dev sửa là nhánh chết) | `[BLOCKER]` — quyết định luồng `F7` / `F8` có test được hay không | Dev / Leader |

**Đã rà** 58 TC, đối chiếu với `spec-features/admin/{friend-information,salon-booking,lesson-booking}/` và `kho-tcs/fa015-*` · `fa019-*` · `fa020-*` · `fa021-*` → 4 mâu thuẫn C1–C4. Cả 4 đều làm mất chuẩn chấm Đạt/Không đạt (C4 → G3 ở §1).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ | Chỉ **41/58 TC (70,7%) có kết quả `pass`**: 10 `blocked` + 7 chưa chạy (NEW-53…NEW-59) | Chạy 7 TC mới trước khi đóng ticket; xử lý 10 TC blocked theo I4 |
| I2 | `[MAJOR]` | Toàn bộ | **RULE-08 / ENV-003**: 51 TC chạy ở staging, **0 TC chạy production**. Task chạm **job nền** (cột 「プレビュー」 phụ thuộc job Java `linect-service` ghi `action_multi_capture_id`, theo Studio) và **webhook thanh toán** (NEW-53…NEW-55) | Chạy tối thiểu NEW-1 / NEW-10 / NEW-17 trên production sau release |
| I3 | `[MAJOR]` | Diff vs file 03 | Diff thật có **7 file**, Dev chỉ kê **5 file** (2 commit trên Redmine). **`Api/CalendarSalonController.php` + `Api/CalendarLessonController.php` (app) không có trong journal nào**. Redmine lại ghi *"2 luồng đặt lịch từ app … chưa fix"*, và Studio đã tách bug app sang **#40703**. Ghi chú của NEW-23 / NEW-24 nói app được sửa trong commit `b02fab7a41`, trong khi journal liệt kê 3 file khác | Hỏi Dev: 2 file Api thuộc ticket nào / commit nào → bổ sung vào mục 4.1 file 03, sửa ghi chú NEW-23 / NEW-24 |
| I4 | `[MAJOR]` | NEW-29, 36, 37, 38, 39, 40, 43, 44, 48, 51 | **10 TC `blocked` vì tester thấy hành vi thực tế khác expected**, nhưng TC chưa được sửa hay đóng: date không có 稼働設定 (NEW-36 / 37 / 39) · date mỗi booking sinh `event_step_time` riêng (NEW-38) · cột 「追加時アクション」 của date luôn là 「設定なし」 (NEW-40) · point chỉ bắn khi đúng ngưỡng (NEW-43 / 44) · không đảm bảo thứ tự gửi (NEW-48 / 51) · không sửa được form (NEW-29) | Leader chốt C1–C4 ở §4 → sửa expected trên Studio (`testcase_update`) hoặc xóa TC không còn nghĩa, rồi chạy lại |
| I5 | `[MAJOR]` | NEW-1 … NEW-20 | Nhóm TC web pass lúc **2026-09-09**, sớm hơn commit `b02fab7a41` (Journal 2026-09-10). Commit này sửa `Basic/CalendarSalonController.php` + `Basic/CalendarManagementController.php`, mà Studio `dev_impact` ghi là luồng *"web salon+lesson admin đặt hộ (Basic CalendarSalonController::createBooking, CalendarManagementController)"* | Xác nhận build đã chạy có đủ 7 file; nếu chưa → chạy lại NEW-1, 3, 7, 11, 13, 16, 17 |
| I6 | `[MAJOR]` | NEW-29 | **Tên ngược với expected**: tên *"xác nhận VẪN chưa gửi action (known issue ngoài phạm vi #38443)"*, expected lại đòi *"Khách nhận đúng 1 tin"*. REQ-016 đã nêu; NEW-23 / NEW-24 đã đổi tên, riêng NEW-29 chưa. TC còn **không atomic** (salon + lesson chung 1 TC) | Đổi tên; tách salon / lesson (TC thay thế ở §7 G3) |
| I7 | `[MINOR]` | NEW-23, NEW-24 | `Loại case` = `Abnormal`, nhưng nội dung là luồng chính (đặt hộ trên app có action → action chạy) | Đổi sang `Normal` |
| I8 | `[NIT]` | NEW-39 | Kết quả blocked chỉ ghi 1 URL LIFF, không nêu lý do | Hỏi tester lý do blocked |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 58 TC, **không có TC nào ngoài phạm vi** theo đủ 3 tiêu chí. Riêng 1 nhóm nên chuyển sang bộ regression chung:

| # | TC | Vì sao | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-42 … NEW-48 (7 TC 「Lối ghi 2」: multi action ghi point) | Test lớp **multi action → info ポイント → action**. Diff không chạm lớp này: cả 7 file chỉ sửa nhánh ghi friend info `type_data == 1` trong form đặt lịch (Studio: *"Chỉ type_data==1 (選択) được chạm"*) | `spec_delta.files[]` không có file của action engine / multi action | Giữ làm regression của ma trận friend info action, nhưng **đưa vào bộ regression chung của kho** (FA-015) thay vì chạy lại mỗi vòng fix #38443 | `[NIT]` |

- Gate: X1 không phải TC duy nhất cover quan điểm nào đang Trigger (`FRIEND-001` đã có NEW-2 / NEW-12 / NEW-31 / NEW-32).

---

## 7. TCs đề xuất bổ sung (12)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` · `fa019-datlichbaihoc-レッスン予約.md` · `fa020-datlichsalon-サロン・面談予約.md` · `fa021-eventbooking-イベント予約.md` (targeted grep/sed) |
| Vùng regression phát hiện từ kho | FA-020 / FA-019 nhóm 「Detail booking & lịch sử」 (`TC-SLN-126`) · FA-015 「Ghi giá trị từ màn admin」 (`TC-FRI-213`) · FA-021 「LINE user — đổi lịch」 (`TC-EBK-186`, `TC-EBK-187`) |
| Conflict expected vs kho | `TC-FRIEND001-01/02/03` (sửa 「お客様情報」) vs `TC-SLN-126` → C4 (§4 + §8) — TC viết theo spec UI, **chạy sau khi Dev chốt C4** |
| GAP dùng lại TC chưa chạy (không viết mới) | G1 → chạy NEW-53 / 54 / 55 · G4 → chạy NEW-56 / 58 / 59 · Q1 / Q2 / Q6 → chạy NEW-53…NEW-59 |
| Căn cứ TC regression `R<x>` | R1 ← kho `TC-FRI-213` (xóa trắng giá trị trường Lựa chọn có action → KHÔNG kích hoạt action ngoài ý) áp vào luồng sửa form mới (`F7` / `F8`) |
| Xác nhận chống trùng | Đã đối chiếu 58 TC ở BƯỚC 0 + 4 file kho — **không TC đề xuất nào trùng** (G1 / G4 / Q1 / Q2 / Q6 dùng lại TC có sẵn) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGHOOK001-01 | UI | INTG-HOOK-001 | LINE user — đổi lịch (sự kiện) | Boundary | auto | Tất cả | Sự kiện - Khách đổi lượt đặt nhưng giữ nguyên đáp án kiểu lựa chọn thì không sinh dòng lịch sử mới và không gửi lại action | - Như NEW-53: sự kiện có thanh toán, còn ≥ 2 lượt trống<br>- Field 「TC38443_選択E」 kiểu 選択肢, 「何度でも稼働」, 「オプションE1」 gắn action 「TC38443_ACT_E1」<br>- Khách T177_EV đã đặt 1 lượt, trả lời 「オプションE1」 và đã nhận 1 tin của action | 1. Ghi lại số dòng lịch sử của 「TC38443_選択E」 ở 「友だち詳細」 → tab 「友だち情報」 và số tin trong phòng chat LINE của T177_EV<br>2. T177_EV mở trang đặt chỗ sự kiện từ LINE → đổi sang lượt khác còn chỗ<br>3. Ở câu hỏi liên kết 「TC38443_選択E」 **giữ nguyên** 「オプションE1」<br>4. Hoàn tất thanh toán, chờ hàng đợi + job xử lý xong<br>5. Đếm lại số dòng lịch sử và số tin | Đáp án: 「オプションE1」 (không đổi) | - Đổi lượt đặt thành công<br>- Bảng lịch sử **không** có dòng mới cho 「TC38443_選択E」<br>- Khách **không** nhận thêm tin của 「TC38443_ACT_E1」 | | Lấp G2 · theo `dev_impact` "cần kiểm không sinh dòng lịch sử thừa" + BUG-R7 · Đánh giá spec: Spec không ghi (Dev ghi ở Journal #135591) · Evidence: ảnh bảng lịch sử trước/sau + ảnh phòng chat |
| TC-INTGHOOK001-02 | UI | INTG-HOOK-001 | LINE user — đổi lịch (sự kiện) | Abnormal | auto | Tất cả | Sự kiện - Đổi lượt đặt có trả lời field không phải kiểu lựa chọn thì không phát sinh action thông tin bạn bè | - Như TC trên<br>- Biểu mẫu đặt sự kiện có thêm câu hỏi liên kết field 「TC38443_記述E」 kiểu 記述 | 1. Ghi lại số tin trong phòng chat của T177_EV và số dòng lịch sử của 「TC38443_記述E」<br>2. T177_EV đổi lượt đặt, sửa câu trả lời 「TC38443_記述E」 thành giá trị mới, giữ nguyên các câu khác<br>3. Hoàn tất thanh toán, chờ xử lý xong<br>4. Mở 「友だち詳細」 → 「友だち情報」 | 「TC38443_記述E」: 「変更テスト」 | - Giá trị 「TC38443_記述E」 cập nhật thành 「変更テスト」, có đúng 1 dòng lịch sử mới, cột 「追加時アクション」 = 「設定なし」<br>- Khách không nhận tin mới nào<br>- Không lỗi hệ thống | | Lấp G2 · `dev_impact` "Chỉ type_data==1 (選択) được chạm" · Evidence: ảnh tab 友だち情報 + phòng chat |
| TC-FRIEND001-01 | UI | FRIEND-001 | Detail booking & lịch sử (salon) | Normal | auto | Tất cả | Salon - Admin sửa đáp án kiểu lựa chọn ở 「お客様情報を編集」 của lượt đặt đã có thì khách nhận action và lịch sử hiện 「プレビュー」 | - Lịch 「TC38443_サロン」, field 「TC38443_選択A」 **「何度でも稼働」**, 「オプションA」 gắn action 「TC38443_ACT_A」, 「オプションB」 không gắn action<br>- Khách T177_USER đã có 1 lượt đặt, đáp án 「オプションB」<br>- ⚠️ Chỉ chạy sau khi chốt C4 (§4) | 1. Ghi lại số tin trong phòng chat và số dòng lịch sử của 「TC38443_選択A」<br>2. Mở 「予約カレンダー」 → bấm lượt đặt của T177_USER → sub-tab 「お客様情報」<br>3. Bấm 「お客様情報を編集」, đổi câu hỏi liên kết sang 「オプションA」 → 「保存」<br>4. Chờ job xử lý action xong<br>5. Xem phòng chat LINE của T177_USER<br>6. Mở 「友だち詳細」 → 「友だち情報」, bấm 「プレビュー」 ở dòng lịch sử mới | 「オプションB」 → 「オプションA」 | - Lưu thành công, sub-tab 「お客様情報」 hiện 「オプションA」<br>- Khách nhận đúng 1 tin của 「TC38443_ACT_A」<br>- Bảng lịch sử có 1 dòng mới, cột 「追加時アクション」 = 「プレビュー」, bấm vào mở đúng nội dung 「TC38443_ACT_A」 | | Lấp G3 · thay NEW-29 (tách salon) · Đánh giá spec: Spec ghi rõ (salon `ui-spec.md:233`) · Evidence: ảnh phòng chat + ảnh preview |
| TC-FRIEND001-02 | UI | FRIEND-001 | Detail booking & lịch sử (lesson) | Normal | auto | Tất cả | Lesson - Admin sửa đáp án kiểu lựa chọn ở 「お客様情報を編集」 của lượt đặt đã có thì khách nhận action và lịch sử hiện 「プレビュー」 | - Lịch 「TC38443_レッスン」, field 「TC38443_選択L」 「何度でも稼働」, 「オプションL1」 gắn action 「TC38443_ACT_L1」, 「オプションL2」 không gắn action<br>- Khách T177_USER2 đã có 1 lượt đặt, đáp án 「オプションL2」<br>- ⚠️ Chỉ chạy sau khi chốt C4 | 1. Ghi lại số tin + số dòng lịch sử<br>2. Mở lịch lesson → lượt đặt của T177_USER2 → 「予約情報」 → 「お客様情報」<br>3. Bấm 「お客様情報を編集」, đổi sang 「オプションL1」 → 「保存」<br>4. Chờ job xử lý xong<br>5. Xem phòng chat + tab 「友だち情報」 | 「オプションL2」 → 「オプションL1」 | - Lưu thành công<br>- Khách nhận đúng 1 tin của 「TC38443_ACT_L1」<br>- Dòng lịch sử mới có 「プレビュー」 mở đúng nội dung | | Lấp G3 · thay NEW-29 (tách lesson) · Đánh giá spec: Spec ghi rõ (lesson `ui-spec.md:1404`, EP-82) · Evidence: ảnh phòng chat + ảnh preview |
| TC-FRIEND001-03 | UI | FRIEND-001 | Detail booking & lịch sử (salon) | Boundary | auto | Tất cả | Salon - Sửa 「お客様情報」 với field 「一度のみ」 mà khách đã nhận action thì không gửi lại | - Field 「TC38443_選択A」 **「一度のみ」**, 「オプションA」 và 「オプションC」 đều gắn action<br>- T177_USER đã nhận action của field này qua 1 lượt đặt hộ (chọn 「オプションA」)<br>- ⚠️ Chỉ chạy sau khi chốt C4 | 1. Ghi lại số tin + số dòng lịch sử<br>2. Mở lượt đặt đó → 「お客様情報を編集」 → đổi sang 「オプションC」 → 「保存」<br>3. Chờ job xử lý<br>4. Xem phòng chat + tab 「友だち情報」 | 「オプションA」 → 「オプションC」 | - Giá trị cập nhật 「オプションC」, có 1 dòng lịch sử mới<br>- Khách **không** nhận thêm tin (BR-04: 一度のみ chỉ chạy khi cờ action còn trống)<br>- Cột 「追加時アクション」 của dòng mới = 「設定なし」 | | Lấp G3 · Đánh giá spec: Spec ghi rõ (friend-information BR-04) · Evidence: ảnh phòng chat + bảng lịch sử |
| TC-FRIEND001-04 | UI | FRIEND-001 | Detail booking & lịch sử (lesson) | Abnormal | auto | Tất cả | Lesson - Sửa 「お客様情報」 xóa trắng đáp án kiểu lựa chọn thì không kích hoạt action ngoài ý muốn | - Field 「TC38443_選択L」 「何度でも稼働」, 「オプションL1」 gắn action<br>- T177_USER2 có lượt đặt, đáp án 「オプションL1」, câu hỏi không bắt buộc<br>- ⚠️ Chỉ chạy sau khi chốt C4 | 1. Ghi lại số tin<br>2. Mở lượt đặt → 「お客様情報を編集」 → bỏ chọn / để trống câu hỏi liên kết → 「保存」<br>3. Chờ job xử lý<br>4. Xem phòng chat + tab 「友だち情報」 | Đáp án: (trống) | - Lưu thành công, không lỗi hệ thống<br>- Khách **không** nhận tin nào<br>- Không có bản ghi action mới; tab 「友だち情報」 hiển thị giá trị trống (hoặc giữ nguyên — ghi nhận hành vi thật cho Leader) | | Lấp R1 · regression · dẫn từ kho `TC-FRI-213` · Evidence: ảnh phòng chat + tab 友だち情報 |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | App mobile (salon) | Boundary | manual | Tất cả | Salon app - Field 「一度のみ」 khách đã nhận action thì admin đặt hộ lại trên app không gửi lần 2 | - App quản trị di động đã đăng nhập bot A<br>- Field 「TC38443_選択A」 「一度のみ」, 「オプションA」 gắn action<br>- T177_USER đã nhận action của field này qua 1 lượt đặt hộ trên web | 1. Ghi lại số tin trong phòng chat của T177_USER<br>2. Trên app: mở lịch 「TC38443_サロン」 → thêm lượt đặt cho T177_USER, chọn 「オプションA」 → đăng ký<br>3. Chờ job xử lý<br>4. Trên web mở 「友だち詳細」 → 「友だち情報」<br>5. Xem phòng chat | 「オプションA」 | - Đặt lịch thành công trên app, hiển thị đúng trên web<br>- Khách **không** nhận thêm tin<br>- Dòng lịch sử mới (nếu có) = 「設定なし」 | | Lấp G5 + Q4 · manual vì app admin mobile (thiết bị thật) · Evidence: ảnh app + phòng chat |
| TC-SYNCAPP001-02 | UI | SYNC-APP-001 | App mobile (lesson) | Abnormal | manual | Tất cả | Lesson app - Chọn lựa chọn không gắn action thì không sinh action và lịch sử hiện 「設定なし」 | - App quản trị di động đã đăng nhập bot A<br>- Field 「TC38443_選択L」, 「オプションL2」 **không** gắn action<br>- T177_USER2 chưa có giá trị cho field | 1. Ghi lại số tin<br>2. Trên app: thêm lượt đặt lesson cho T177_USER2, chọn 「オプションL2」 → đăng ký<br>3. Trên web mở tab 「友だち情報」 của T177_USER2<br>4. Xem phòng chat | 「オプションL2」 | - Đặt chỗ thành công, giá trị = 「オプションL2」, có 1 dòng lịch sử, cột 「追加時アクション」 = 「設定なし」<br>- Khách không nhận tin action nào<br>- Không lỗi trên app | | Lấp G5 + Q4 · manual vì app admin mobile (thiết bị thật) · Evidence: ảnh app + tab 友だち情報 |
| TC-FUNC004-01 | UI | FUNC-004 | Admin thêm booking thủ công (salon) | Boundary | auto | Tất cả | Salon - Lựa chọn có tên dạng số gần giống nhau thì đặt hộ chỉ kích hoạt action của đúng lựa chọn được chọn | - Field 「TC38443_選択N」 kiểu 選択肢 「何度でも稼働」, 2 lựa chọn tên 「1」 và 「01」, mỗi lựa chọn gắn action riêng: 「ACT_1」 (text 「一番」), 「ACT_01」 (text 「ゼロ一番」)<br>- Form đặt lịch salon có câu hỏi liên kết field này<br>- T177_NUM chưa có giá trị | 1. Mở modal 「予約追加」 → chọn T177_NUM → chọn 「01」 → đăng ký<br>2. Chờ job xử lý, xem phòng chat<br>3. Đặt hộ lượt thứ 2 cho T177_NUM, chọn 「1」<br>4. Chờ job, xem phòng chat + tab 「友だち情報」 | 「01」 rồi 「1」 | - Lượt 1: khách nhận đúng 1 tin 「ゼロ一番」, **không** nhận 「一番」<br>- Lượt 2: khách nhận đúng 1 tin 「一番」<br>- Mỗi dòng lịch sử mở 「プレビュー」 đúng action của lựa chọn đó | | Lấp G6 · `dev_impact` "So khớp đổi từ == sang (string)!==" · Evidence: ảnh phòng chat + preview từng dòng |
| TC-DATADB001-01 | UI | DATA-DB-001 | Admin thêm booking thủ công (salon) | Normal | auto | Tất cả | Salon - Cờ 「一度のみ」 chỉ ghi cho đúng khách và đúng field vừa đặt hộ | - Field X 「TC38443_選択A」 và field Y 「TC38443_選択B」, cả 2 「一度のみ」, lựa chọn đều gắn action (「ACT_A」, 「ACT_B」)<br>- 2 khách T177_DB1, T177_DB2 chưa có giá trị ở X và Y<br>- Form đặt lịch có câu hỏi liên kết X và Y | 1. Đặt hộ T177_DB1, chỉ trả lời X → đăng ký → chờ job<br>2. Đặt hộ T177_DB2, chỉ trả lời X → đăng ký → chờ job<br>3. Đặt hộ T177_DB1 lần 2, chỉ trả lời Y → đăng ký → chờ job<br>4. Đếm tin của từng khách | X = 「オプションA」, Y = 「オプションB」 | - Bước 1: T177_DB1 nhận 1 tin 「ACT_A」<br>- Bước 2: T177_DB2 **vẫn** nhận 1 tin 「ACT_A」 (cờ của DB1 không lan sang DB2)<br>- Bước 3: T177_DB1 nhận 1 tin 「ACT_B」 (cờ field X không lan sang field Y) | | Lấp Q3 + G7 · Boundary đã có NEW-3 / NEW-13 · Đánh giá spec: Spec ghi rõ (BR-04) · Evidence: ảnh phòng chat 2 khách |
| TC-DATADB001-02 | UI | DATA-DB-001 | Admin thêm booking thủ công (lesson) | Abnormal | auto | Tất cả | Lesson - Đặt hộ ở bot A không làm mất action 「一度のみ」 của bot B có field cùng tên | - Bot A và bot B đều có field 「TC38443_選択L」 「一度のみ」, 「オプションL1」 gắn action (bot A: 「ACT_A_L1」, bot B: 「ACT_B_L1」)<br>- Cùng tài khoản LINE test đã kết bạn cả 2 bot, chưa có giá trị ở cả 2<br>- Dùng 2 phiên đăng nhập riêng cho bot A / bot B | 1. Phiên bot A: đặt hộ lesson cho khách, chọn 「オプションL1」 → chờ job<br>2. Phiên bot B: đặt hộ lesson cho cùng khách, chọn 「オプションL1」 → chờ job<br>3. Xem phòng chat của khách với từng bot | 「オプションL1」 ở cả 2 bot | - Phòng chat bot A: 1 tin 「ACT_A_L1」<br>- Phòng chat bot B: **vẫn** nhận 1 tin 「ACT_B_L1」<br>- Tab 「友だち情報」 của mỗi bot chỉ có dòng lịch sử của bot đó | | Lấp Q3 · WHERE scope 2 tài khoản (DATA-DB-001 ★) · Evidence: ảnh phòng chat 2 bot |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Dữ liệu cũ & hồi quy (salon) | Normal | manual | staging | Salon - Khách đã nhận action 「一度のみ」 trước khi deploy bản vá thì admin đặt hộ sau deploy gửi tối đa thêm 1 lần | - Trên build **trước bản vá**: field 「TC38443_選択A」 「一度のみ」, 「オプションA」 gắn action; khách T177_OLD đã nhận tin action này qua **khách tự đặt lịch** (LIFF) hoặc qua 「友だち詳細」<br>- Sau đó deploy branch `ai_fixbug_38443` | 1. Sau deploy, ghi lại số tin của T177_OLD<br>2. Admin đặt hộ salon cho T177_OLD, chọn 「オプションA」 → đăng ký → chờ job<br>3. Đếm tin<br>4. Admin đặt hộ lần nữa, cùng lựa chọn → chờ job<br>5. Đếm tin | 「オプションA」 | - Bước 3: khách nhận **tối đa 1** tin (BUG-R6: *"CÓ THỂ nhận thêm đúng 1 lần"*) — ghi nhận có/không để PO chấp nhận<br>- Bước 5: khách **không** nhận thêm tin (cờ đã được ghi) | | Lấp Q5 · BUG-R6 (Journal #135591) · manual vì cần dựng dữ liệu trên build cũ rồi deploy · Evidence: ảnh phòng chat trước/sau deploy |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update / chốt | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `friend-information/feature-spec.md` dòng 394 (「稼働設定」 áp cho SCR-FRI-02, **04**, 05) | Info kiểu date có 「一度のみ」/「何度でも稼働」 không? Kho `TC-FRI-78` và tester nói **không** → nếu đúng thì bỏ SCR-FRI-04 khỏi dòng này, xóa/sửa NEW-36 / NEW-37 / NEW-39 | C1 CONF-KHO | Leader / BA |
| 2 | `friend-information/feature-spec.md` BR-02 (ポイント: *"Trigger khi đạt ngưỡng"*) | Ghi rõ "đạt" là **= đúng ngưỡng** hay **≥ ngưỡng**; sửa NEW-43 / NEW-44 theo kết luận | C2 CONF-SPEC | BA |
| 3 | Kho FA-020 `MT-10` (thứ tự ưu tiên action) | Chốt: hệ thống có đảm bảo thứ tự gửi friend info → course → staff không. Không đảm bảo → bỏ phần "đúng thứ tự" ở NEW-48 / NEW-51 | C3 CONF-KHO | Leader / PO |
| 4 | `salon-booking/ui/ui-spec.md:233` · `lesson-booking/ui/ui-spec.md:1404` vs kho `TC-SLN-126` | Link 「お客様情報を編集」 còn trên UI không? Nếu còn → sửa `TC-SLN-126` (chỉ đúng với chế độ xem), chạy §7 G3. Nếu đã gỡ → `saveInfoFormBooking` Dev sửa ở `F7` / `F8` là nhánh không tới được từ UI, cần Dev xác nhận luồng gọi | C4 CONF-KHO | Dev / Leader |
| 5 | `03-dev-impact.md` mục 4.1 | Bổ sung `Api/CalendarSalonController.php` + `Api/CalendarLessonController.php` (có trong diff, không có trong journal nào); xác nhận quan hệ với bug #40703 | I3 §5 | Dev |
| 6 | `event-booking` — luồng đổi lượt đặt | Nêu rõ những đường nào đi qua `callbackChangeBooking`: chỉ webhook UnivaPay? Stripe? Đổi lượt 全承認 không thanh toán? Admin duyệt đổi lượt リクエスト制 (kho `TC-EBK-187`)? → quyết định có cần nhân NEW-53 cho từng đường | G1 §1 | Dev |
