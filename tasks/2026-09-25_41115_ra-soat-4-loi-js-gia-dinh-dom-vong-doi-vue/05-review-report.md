# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #329 (ticket 41115, round 1, branch `ai_fixbug_41115`) |
| Tổng số TC review | 26 (NEW-1 → NEW-26) |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 12/12 mục có TC, trong đó 5 mục RISK (BUG, F2, T6, F4, T3) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (5 file, +51/−16) | 10/12 điểm có TC, 1 GAP + 1 RISK — **CHƯA ĐỦ** |

**Kết luận**: 17/24 vùng ảnh hưởng đủ TC về mặt thiết kế · 1 GAP · 3 RISK (gộp dòng trùng giữa 2 chiều). ⚠️ Cả 26 TC **chưa chạy** (xem I1 ở §5) → chưa vùng nào có kết luận Đạt.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` mục 1a — `updated()` khi không vẽ `#confirm_term`: tổ hợp **`type_contract_new == 0` && `type_campaign == 1`** (điều kiện tái hiện ticket ghi) | dev-impact | NEW-2 (đi đường khác: màn hoàn tất `success=1`), NEW-6 (campaign trên bot hợp đồng mới, chỉ `local`) | RISK — không TC nào dựng đúng tổ hợp ticket nêu. Ghi chú NEW-2/NEW-6 tự kết luận tổ hợp này "không tới được từ giao diện" nhưng không dẫn bằng chứng; theo spec, `flag_contract_new = 0` là **hợp đồng kiểu cũ (trước 01/05/2023)**, không phải "không mua mới" → nhánh hợp đồng cũ chưa được test (liên quan Q1) | `[MAJOR]` |
| G2 | `F2` / `T6` — `bill_tool/index.js`: handler cuộn dùng chung cho **3 nhánh blade** `main-step.blade.php:195/411/664` + khối jQuery ready chạy ở **lần tải trang đầu** | dev-impact + diff code | NEW-1, 3, 4, 5 (mua mới qua 「プラン選択」), NEW-6 (campaign) | RISK — chưa TC nào đi nhánh `upgrade_flag == 1` / `typeUpgrade == 'max_friend'` (nâng cấp gói từ 契約情報 / màn cảnh báo max friend — kho TC-BLP-76~78, TC-BLP-326). Đây cũng là lối vào **thẳng bước 1 lúc tải trang**, tức đúng nhánh jQuery ready mà commit tự review `0150dedda4` sửa; bộ TC hiện chỉ vào bước 1 qua đổi bước trong trang | `[MAJOR]` |
| G3 | `F4` / `T3` — resize ở **màn Salon** (`calendar_salon/calendar_detail.js`) | dev-impact + diff code | NEW-12 (週, 月), NEW-13 (日) | RISK — thiếu chế độ 「一覧」 (kể cả tab シフト) và các **tab khác** của màn chi tiết Salon. Listener gắn ở `window` nên chạy ở mọi tab — màn Lesson đã có NEW-8 (一覧) + NEW-10 (tab khác), màn Salon không có cặp tương ứng (`dev_impact`: "mục 2 cùng pattern ở 2 file — phải test cả hai") | `[MAJOR]` |
| G4 | Diff mục 3 — guard `$refs.scrollDiv` trong **`mounted`** (`calendar-management.js`) | diff code | không có | GAP — NEW-11/15/16/14 đi `updated`/`beforeDestroy`/`handleScroll`; chưa TC nào tải trang khi vùng cuộn **chưa được vẽ lúc mount** (F5 khi đang ở 週, hoặc tải lại khi đang ở tab khác của màn chi tiết Salon) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 13 quan điểm Trigger khớp task · 10 chưa cover đủ. Có 15/26 TC mang mã `TOOL-*` / `RULE-TOOL-*` nên không được tính là cover — nhiều dòng dưới đây sửa được bằng cách **đổi mã quan điểm** trên Studio, không cần TC mới.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `COMPAT-LEGACY-001` | Cao | GAP — 0 TC cho bot **hợp đồng kiểu cũ** (`flag_contract_new = 0`, spec `detail-contract/db/db-mapping.md:86`) vào bước 1 của bill-tool. Đây là 1 vế của điều kiện tái hiện mục 1 (RULE-09) | `[BLOCKER]` |
| Q2 | `DATA-CACHE-001` | Trung bình → Cao (trang đặt lịch là output user-facing) | GAP — chưa có kịch bản (1): **tab mở sẵn trước deploy**, không F5, thao tác tiếp | `[BLOCKER]` |
| Q3 | `DEPLOY-ASSET-001` | Cao (tuyệt đối: `bill_tool/index.js` nằm trong luồng thanh toán) | RISK — chỉ có Normal (NEW-25); thiếu Abnormal + Boundary (RULE-01). Boundary hợp lý: trang đặt lịch mở lại trong **trình duyệt in-app của LINE** (webview giữ cache) sau release | `[MAJOR]` |
| Q4 | `LIFF-ENTRY-001` | Cao | RISK — TC tái hiện mục 4 (NEW-21/22/23/24) chỉ mở trang đặt lịch bằng nút **xem trước trên PC**; 0 TC ở điểm vào **in-app LINE**. Chỉ cần trục "điểm vào": fix không đổi logic kết bạn / link cũ-mới | `[MAJOR]` |
| Q5 | `REG-URL-001` | Trung bình → Cao (CR chạm màn thanh toán) | RISK — lỗi mục 1 nổ **lúc tải trang ở bước ≠ 1**, tức đúng các URL hoàn tất thanh toán. NEW-2 (mã `TOOL-KNOW-002`) chỉ thử 1 biến thể (`success=1&type_contract=standard`); chưa có ma trận URL `*_success` + `bot-add-v2?status=successful` + biến thể `/` cuối / param thừa | `[MAJOR]` |
| Q6 | `REG-SHARED-001` | Cao | RISK — chỉ có NEW-12 (Abnormal). Normal đang nằm ở NEW-9 / NEW-13 (`TOOL-NEGCTRL-001`) → đổi mã; thiếu Boundary (Salon 一覧 / tab khác — trùng G3) | `[MAJOR]` |
| Q7 | `FUNC-001` | Cao | RISK RULE-01 — chỉ Normal (NEW-1, NEW-17). Các ca Abnormal tái hiện lỗi (NEW-2, NEW-7, NEW-11, NEW-21) đang mang `TOOL-KNOW-002` → đổi mã; thiếu Boundary | `[MAJOR]` |
| Q8 | `CONC-001` | Cao | RISK RULE-01 — có Normal (NEW-3) + Abnormal (NEW-18), thiếu Boundary (số lần vẽ lại lớn / modal ở chế độ không phải 日) | `[MAJOR]` |
| Q9 | `FUNC-004` | Cao | RISK RULE-01 — chỉ Boundary (NEW-4), không ghi lý do thiếu Normal/Abnormal. Normal thực tế là NEW-1 → ghi lý do ở `note` NEW-4 là đủ, không cần TC mới | `[MAJOR]` |
| Q10 | `UI-001` | Trung bình → Cao (luồng đặt lịch user-facing) | RISK — kiểm tra hiển thị trang đặt lịch sau 「戻る」 chỉ nằm ở TC mã `TOOL-*` (NEW-21, NEW-22, NEW-23) → đổi mã, không cần TC mới | `[MAJOR]` |

Đã loại khỏi phạm vi (Trigger khớp nhưng không có ảnh hưởng): `OUT-PREVIEW-001` (fix không chạm preview, preview chỉ là lối vào test) · `PAY-*` / `ENV-003` / RULE-08 (diff chỉ thêm guard JS, TC dừng trước 「決済に進む」, không đổi luồng thanh toán) · `SYNC-APP-001` (app quản trị di động là native — xin Dev xác nhận ở I5) · `STATE-CLEAN-001` (trigger là hủy hợp đồng / ngắt kết nối, không khớp).

---

## 3. TC trùng lặp nội dung

Đã rà 26 TC, không phát hiện trùng lặp. Các cặp gần nhau đều khác ít nhất 1 trong 4 yếu tố: NEW-1 vs NEW-4 khác mã quan điểm + loại case; NEW-3 vs NEW-5 khác thao tác (đổi chu kỳ vs huỷ rồi vào lại); NEW-7 / NEW-8 / NEW-10 khác chế độ hoặc tab; NEW-11 vs NEW-14 khác thao tác.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-1, NEW-4 | Gợi ý 「注意事項を最後までスクロールして確認してください。」 khi chưa cuộn hết | NEW-1: khối 注意事項 "hiển thị **kèm dòng gợi ý**"; NEW-4: "dòng gợi ý **vẫn hiển thị**" ở mốc 50% và gần đáy | kho `TC-BLP-72`: checkbox disable, **hover** lên checkbox mới hiện **tooltip** với nội dung đó | ✅ **Leader chốt 2026-09-28**: không có dòng chữ luôn hiện. Tooltip 「注意事項を最後までスクロールして確認してください。」 hiện khi hover vào **dòng chữ** 「注意事項を読み、解約や返金について内容を理解しました」 **và** vào **ô checkbox** ở dòng đó → **NEW-1, NEW-4 sai expected**. Kho `TC-BLP-72` đúng nhưng mới nêu hover lên checkbox, thiếu hover lên dòng chữ | `[MAJOR]` | Leader (đã chốt) |

**Đã rà**: 26 TC × `spec-features/admin/bot-add-v2`, `detail-contract`, `billing-plan`, `lesson-booking` (§4.2), `salon-booking` + `kho-tcs/fa031`, `fa019`, `fa020` (vùng xác nhận plan, calendar ngày/tuần/tháng/list, LINE user chọn slot, ca làm). Spec **không** mô tả khối 注意事項 và ngưỡng cuộn (xem I2) → không đối chiếu `CONF-SPEC` được cho mục 1.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 26 TC | 0/26 TC đã chạy (0% Đạt, `exec.untested = 26` ở cả 4 env). Chưa có kết luận test nào | Chạy bộ TC (sau khi bổ sung §7) trước khi đóng ticket |
| I2 | `[MAJOR]` | NEW-1 → NEW-6 (bill-tool) | Input thiếu: spec cho khối 注意事項 / ngưỡng cuộn / đánh dấu đã đọc. `spec-features/` không có; REQ-002 của Studio dẫn `admin/bot-add/ui/ui-spec.md:228-229` nhưng file này không có trong `spec-features/`. Chuẩn duy nhất là kho `TC-BLP-72~74` + Leader chốt tooltip (C1, 2026-09-28) | Sửa expected NEW-1 / NEW-4 trên Studio (`testcase_update`): bỏ "dòng gợi ý hiển thị", thay bằng "hover vào dòng chữ 「注意事項を読み、解約や返金について内容を理解しました」 hoặc ô checkbox khi chưa cuộn hết → hiện tooltip 「注意事項を最後までスクロールして確認してください。」"; ở NEW-4 kiểm tooltip tại mốc 1 và mốc 2. ✅ **Đã sửa trên Studio 2026-09-28** (NEW-1 #20284 v2, NEW-4 #20287 v2; `spec_status` = Đã hỏi leader) |
| I3 | `[MAJOR]` | NEW-2, NEW-6 (ghi chú) | Ghi chú TC khẳng định "code ép kiểu hợp đồng thành mới khi có chiến dịch nên tổ hợp hợp đồng cũ + chiến dịch không tới được", ngược với ticket + Dev (Journal #137393 xác nhận tổ hợp này gây lỗi lúc tải trang). TC còn hiểu `type_contract_new` là "mua mới", trong khi spec định nghĩa `flag_contract_new` là hợp đồng kiểu cũ/mới theo mốc 01/05/2023 | Hỏi Dev: tổ hợp `type_contract_new=0 && type_campaign=1` dựng bằng dữ liệu nào (bot cũ tạo trước 01/05/2023 + `has_campaign=1`?). Dev xác nhận không tới được → G1 / TC-COMPATLEGACY001-02 là GAP giả, bỏ |
| I4 | `[MAJOR]` | NEW-21, NEW-22, NEW-23, NEW-24 | Tiền đề thiếu setting **ưu tiên hiển thị tuần/tháng phía LINE user** (Feature #27978, kho `TC-LSN-561`). Nếu lịch đang để 「月」, NEW-21 (ca tái hiện chính) không mở mặc định ở tab 週 → không tái hiện được lỗi | Thêm vào tiền đề: "setting hiển thị ưu tiên = 週". Cân nhắc thêm biến thể setting = 月 → chuyển sang 週 → 戻る (NEW-23 đã gần đúng, chỉ cần ghi rõ setting) |
| I5 | `[MAJOR]` `[AP-6]` | `03-dev-impact.md` mục 3 | Dev chỉ liệt kê caller cho **mục 3** (mixin Salon). Mục 1 / 2 / 4 không có danh sách màn nạp `bill_tool/index.js`, `booking_news/booking.js`, `calendar_management/calendar_detail.js`. Cụ thể cần xác nhận: (a) màn **gia hạn hợp đồng** / **hợp đồng lại** (kho `TC-BLP-185`: cũng có checkbox 注意事項 phải cuộn hết) có dùng chung `bill_tool/index.js` không; (b) `booking_news/booking.js` có trang nào khác ngoài `Mobile\CalendarController@index` dùng không; (c) app quản trị di động có mở các màn này qua webview không | Dev bổ sung danh sách. Nhánh nào dùng chung → thêm TC regression tương ứng |
| I6 | `[MINOR]` | NEW-3 | Kết quả mong đợi có ý không đo được: "Người dùng chỉ có thể xác nhận một lần, **không phát sinh callback nhiều lần**" — tester thủ công không quan sát được "callback" | Giữ phép đo DevTools (số listener `scroll` = 1) làm oracle chính; bỏ hoặc cụ thể hoá ý "callback" |
| I7 | `[NIT]` | NEW-16 | Mã `STATE-CLEAN-001` có trigger là hủy hợp đồng / ngắt kết nối, không khớp nội dung "rời màn khi đang ở 週" | Đổi sang `FUNC-SEQ-001` hoặc `REG-SHARED-001` |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 26 TC — không có TC nào ngoài phạm vi task. NEW-26 (khác trình duyệt) có ghi chú tự nhận "không nằm trong scope lỗi gốc", nhưng là TC duy nhất cover `UI-002` nên giữ. NEW-24 là regression cho các điểm Dev tự rà (`booking.js:560/589/695`), không phải TC thừa.

---

## 7. TCs đề xuất bổ sung (14)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` · `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (bảng Coverage + vùng grep) |
| Vùng regression phát hiện từ kho | FA-031 #8 Xác nhận plan — upgrade (`TC-BLP-76~78`), #33 Bill max friend (`TC-BLP-325/326`), #36 Redirect sau bill success (`TC-BLP-360~363`); FA-020 #8 Hiển thị list & tab シフト (`TC-SLN-78~80`); FA-019 #42 LINE user chọn slot (`TC-LSN-549`, `TC-LSN-561`) |
| Conflict expected vs kho | NEW-1/NEW-4 vs `TC-BLP-72` → C1 ở §4 + §8, Leader đã chốt tooltip (2026-09-28). TC-COMPATLEGACY001-01 đã bổ sung bước kiểm tooltip theo chuẩn này |
| GAP dùng lại TC kho (không viết mới) | Không — TC kho kiểm luồng nghiệp vụ (tiền, plan), không kiểm lỗi JS / số listener |
| Căn cứ TC regression `R<x>` | R1: `dev_impact` mục 3 ("guard `$refs.scrollDiv` ở `updated`… đổi timepicker sang `.off/.on`") + kho `TC-SLN-80` (tab シフト → シフト追加 / 詳細 mở modal ca ở chế độ 一覧) |
| Xác nhận chống trùng | Đã đối chiếu 26 TC ở BƯỚC 0 + 3 file kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Xác nhận plan — upgrade | Normal | auto | staging | Bot hợp đồng kiểu cũ (trước 01/05/2023) nâng cấp gói: bước 1 hiện khối 注意事項, cuộn hết một lượt mở khoá ô đồng ý, Console sạch | - Đăng nhập owner của 1 bot standard hợp đồng kiểu cũ (tạo trước 01/05/2023, không trong thời gian chiến dịch)<br>- DevTools mở tab Console, đã xoá log | 1. Vào 「契約情報・領収書」 (/basic/point-settings), bấm nâng cấp lên pro<br>2. Chờ bước 1 xác nhận hợp đồng tải xong<br>3. Chưa cuộn, rê chuột vào dòng chữ 「注意事項を読み、解約や返金について内容を理解しました」, rồi rê chuột vào ô checkbox ở dòng đó<br>4. Cuộn khối 注意事項 tới đáy đúng 1 lượt<br>5. Tick ô đồng ý, quan sát nút 「決済に進む」 và Console | Bot standard hợp đồng cũ | - Bước 1 hiển thị khối 注意事項, ô đồng ý đang khoá<br>- Bước 3: rê chuột vào dòng chữ và vào ô checkbox đều hiện tooltip 「注意事項を最後までスクロールして確認してください。」<br>- Sau 1 lượt cuộn tới đáy: ô đồng ý mở khoá, tick được<br>- Tick xong: 「決済に進む」 bấm được<br>- Console: 0 lỗi (không có lỗi Cannot read properties of null) |  | Lấp Q1 · Lấp G1 · Đánh giá spec: Đã hỏi leader (tooltip khi hover dòng chữ + checkbox, chốt 2026-09-28 — C1) · Evidence: screenshot bước 1 + Console · Dừng trước 決済に進む, không tạo hợp đồng |
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | Campaign 初月無料 | Abnormal | auto | staging | Bot hợp đồng kiểu cũ đang trong chiến dịch mở màn đăng ký gói: khối điều khoản không vẽ nhưng trang không lỗi JS khi tải và khi vẽ lại | - Bot **hợp đồng kiểu cũ** + đang trong thời gian chiến dịch (tổ hợp `type_contract_new=0` & `type_campaign=1` theo ticket; nhờ Dev dựng dữ liệu)<br>- Đăng nhập owner bot đó, DevTools Console đã xoá log | 1. Mở màn đăng ký/nâng cấp gói theo đường chiến dịch của bot<br>2. Quan sát trang + Console ngay sau khi tải xong<br>3. Bấm qua lại 「毎月払い」↔「年間払い」 5 lần<br>4. Quan sát Console sau mỗi lần | Số lần đổi chu kỳ: 5 | - Trang hiển thị đủ nội dung bước đang xem, các nút còn bấm được<br>- Console: 0 lỗi lúc tải trang và sau 5 lần đổi chu kỳ |  | Lấp Q1 · Lấp G1 · Ca tái hiện đúng điều kiện ticket mục 1a · Nếu Dev xác nhận tổ hợp không tồn tại (I3) → bỏ TC này · Thiếu Boundary vì cặp cũ/mới không có biên ở tầng guard JS · Evidence: screenshot Console |
| TC-FUNC001-01 | UI | FUNC-001 | Xác nhận plan — upgrade | Normal | auto | staging | Nâng cấp free → standard vào thẳng bước 1 lúc tải trang: 1 lượt cuộn mở khoá ô đồng ý, khối điều khoản chỉ có 1 listener scroll | - Owner bot free (hợp đồng kiểu mới)<br>- DevTools mở sẵn | 1. Ở 「契約情報・領収書」 bấm nâng cấp lên standard<br>2. Chờ bước 1 tải xong (tải trang mới, không qua 「プラン選択」)<br>3. Ở Elements chọn khối 注意事項 → Event Listeners → đếm listener `scroll`<br>4. Cuộn tới đáy 1 lượt, tick ô đồng ý<br>5. Quan sát 「決済に進む」 + Console | Upgrade free → standard, 毎月払い | - Số listener `scroll` trên khối 注意事項 = 1<br>- Sau 1 lượt cuộn: ô đồng ý mở khoá; tick xong 「決済に進む」 bấm được<br>- Console: 0 lỗi |  | Lấp G2 · Nhánh blade `upgrade_flag == 1` + khối jQuery ready (commit `0150dedda4`) · Đánh giá spec: Spec không ghi · Evidence: screenshot Event Listeners + Console |
| TC-FUNC001-02 | UI | FUNC-001 | Bill max friend — cảnh báo & upgrade | Normal | auto | staging | Nâng cấp do vượt giới hạn bạn bè (max_friend) vào bước 1: khối điều khoản cuộn hết mới mở khoá, Console sạch | - Bot free vượt 50.000 bạn bè đang hiện màn cảnh báo (dựng dữ liệu như kho `TC-BLP-325`)<br>- DevTools Console đã xoá log | 1. Ở màn cảnh báo bấm 「アップグレードにすすむ」<br>2. Chờ bước 1 xác nhận hợp đồng pro tải xong<br>3. Cuộn khối 注意事項 tới đáy 1 lượt, tick ô đồng ý<br>4. Quan sát 「決済に進む」 + Console | Tổng bạn bè: 50.001 | - Bước 1 hiển thị khối 注意事項, ô đồng ý khoá trước khi cuộn hết<br>- Sau 1 lượt cuộn: mở khoá; tick xong 「決済に進む」 bấm được<br>- Console: 0 lỗi |  | Lấp G2 · Nhánh blade `typeUpgrade == 'max_friend'` · dẫn từ `TC-BLP-326` · Evidence: screenshot Console |
| TC-FUNC001-03 | UI | FUNC-001 | Xác nhận plan — upgrade | Abnormal | auto | staging | F5 tại bước 1 nâng cấp rồi đổi chu kỳ nhiều lần: vẫn chỉ 1 listener scroll, ô đồng ý trở về khoá | - Đang ở bước 1 nâng cấp standard → pro, đã cuộn hết + tick ô đồng ý<br>- DevTools mở sẵn | 1. Bấm F5 (tải lại thường)<br>2. Quan sát ô đồng ý sau khi tải lại<br>3. Bấm qua lại 「毎月払い」↔「年間払い」 5 lần<br>4. Đếm listener `scroll` trên khối 注意事項<br>5. Cuộn tới đáy 1 lượt, quan sát ô đồng ý + Console | Số lần đổi chu kỳ: 5 | - Sau F5: ô đồng ý khoá, chưa tick<br>- Sau 5 lần đổi chu kỳ: listener `scroll` = 1 (không cộng dồn giữa jQuery ready và `updated`)<br>- 1 lượt cuộn tới đáy: mở khoá<br>- Console: 0 lỗi |  | Lấp G2 · Lấp Q7 (Abnormal) · `dev_impact`: "mục 1 chia sẻ handler giữa updated() và jQuery ready — kiểm cả lần load đầu lẫn re-render" · Evidence: screenshot Event Listeners |
| TC-FUNC001-04 | UI | FUNC-001 | Calendar theo tuần | Boundary | auto | staging | Tải lại màn chi tiết lịch Salon khi vùng cuộn chưa được vẽ lúc mount (đang ở 週 / đang ở tab khác) không sinh lỗi | - Lịch Salon loại スタッフ có ca làm trong tuần hiện tại<br>- DevTools Console bật "Preserve log", đã xoá log | 1. Ở tab 「予約カレンダー」 chọn 「週」, bấm F5<br>2. Quan sát Console + chế độ hiển thị sau khi tải lại<br>3. Chuyển sang tab 「コース・スタッフ」, bấm F5<br>4. Quan sát Console<br>5. Quay lại 「予約カレンダー」 → 「日」, cuộn ngang bảng lịch | — | - Bước 1–4: Console 0 lỗi lúc tải trang, dù trang mở lại ở chế độ/tab nào<br>- Bước 5: bảng chế độ ngày cuộn ngang được, cột nhân viên vẫn dính trái |  | Lấp G4 · Guard `$refs.scrollDiv` trong `mounted` (`dev_impact` mục 3) · Evidence: screenshot Console (Preserve log) |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Hiển thị theo list & tab シフト | Abnormal | auto | staging | Đổi kích thước cửa sổ ở chế độ 「一覧」 (tab booking và tab シフト) của lịch Salon không sinh lỗi JS | - Lịch Salon có booking + ca làm trong tháng hiện tại<br>- Tab 「予約カレンダー」, DevTools Console đã xoá log | 1. Chọn 「一覧」, ở tab danh sách booking kéo thu nhỏ rồi phóng to chiều ngang cửa sổ (kéo liên tục)<br>2. Quan sát Console + danh sách<br>3. Chuyển sang tab シフト trong chế độ 「一覧」, lặp lại thao tác kéo<br>4. Quan sát Console + danh sách ca | Mỗi tab kéo 2 lượt | - Console: 0 lỗi trong và sau khi kéo<br>- Danh sách booking / ca hiển thị đủ dòng, phân trang giữ nguyên |  | Lấp G3 · Lấp Q6 · Cặp đối xứng với NEW-8 bên Lesson · dẫn từ `TC-SLN-78`, `TC-SLN-79` · Evidence: screenshot Console |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Calendar theo tuần | Boundary | auto | staging | Đổi kích thước cửa sổ khi đang ở tab khác của màn chi tiết lịch Salon không sinh lỗi JS | - Tab 「予約カレンダー」 đang ở 「週」<br>- DevTools Console đã xoá log | 1. Chuyển lần lượt sang tab 「コース・スタッフ」, 「予約設定」, 「決済連携」<br>2. Ở mỗi tab kéo đổi chiều ngang cửa sổ 2 lượt, quan sát Console<br>3. Quay lại 「予約カレンダー」 | 3 tab × 2 lượt kéo | - Cả 3 tab: Console 0 lỗi, nội dung tab co giãn bình thường<br>- Quay lại 「予約カレンダー」: lịch tuần đúng tuần, đủ dữ liệu |  | Lấp G3 · Lấp Q6 (Boundary) · Cặp đối xứng với NEW-10 bên Lesson (listener gắn ở `window`) · Evidence: screenshot Console |
| TC-CONC001-01 | UI | CONC-001 | Ca làm việc — thêm & ghi đè | Boundary | auto | staging | Ở chế độ 「一覧」 → tab シフト, mở/đóng modal ca nhiều lần rồi chọn giờ 1 lần: chỉ cập nhật 1 lần, lưu đúng giờ | - Lịch Salon loại スタッフ, nhân viên S1 có 1 ca ngày D<br>- Tab 「予約カレンダー」 chế độ 「一覧」 → tab シフト<br>- DevTools mở sẵn | 1. Bấm 「シフト追加」 rồi đóng modal, lặp 5 lần<br>2. Bấm 「詳細」 ở dòng ca của S1 để mở màn sửa ca<br>3. Mở bộ chọn giờ bắt đầu, chọn 09:30 đúng 1 lần<br>4. Quan sát ô giờ + tab Network<br>5. Lưu, mở lại và đối chiếu | Giờ bắt đầu mới: 09:30 | - Ô giờ nhảy thẳng sang 09:30, không nhấp nháy qua giá trị khác<br>- Bấm lưu chỉ phát sinh 1 request lưu (Network)<br>- Mở lại: giờ bắt đầu = 09:30<br>- Console: 0 lỗi |  | Lấp R1 · regression · Lấp Q8 (Boundary) · Căn cứ: trước fix `updated()` có thể dừng ở `$refs.scrollDiv` khi không ở 日, sau fix chạy tiếp tới `initializeTimePickers` ở mọi chế độ → hành vi mới ở 週/月/一覧 (`dev_impact` mục 3) · dẫn từ `TC-SLN-80` · Evidence: screenshot Network + Console |
| TC-DATACACHE001-01 | UI | DATA-CACHE-001 | Môi trường & regression | Abnormal | manual | product | Tab mở sẵn từ trước release (không F5) thao tác tiếp trên màn Salon và bill-tool, sau F5 thường thì hết lỗi | - Trước release: mở sẵn màn chi tiết lịch Salon (tab 「予約カレンダー」) và bước 1 màn nâng cấp gói, **không** đóng tab<br>- Release bản fix lên production | 1. Sau release, trên tab Salon còn mở, không F5: chuyển 「週」, đổi tuần 2 lần, quan sát Console<br>2. Bấm F5 thường (không Ctrl+F5), lặp lại bước 1<br>3. Trên tab bill-tool còn mở: đổi chu kỳ 3 lần, cuộn 注意事項, quan sát; rồi F5 thường và lặp lại | — | - Trước F5: tab vẫn dùng JS cũ, thao tác không làm trắng trang / mất dữ liệu (lỗi cũ có thể còn trên Console)<br>- Sau F5 thường: Network tải file JS query version mới (200), thao tác ở bước 1 và 3 không còn lỗi Console |  | Lấp Q2 · manual vì môi trường production (thời điểm release) · Evidence: screenshot Console trước/sau F5 + Network |
| TC-DEPLOYASSET001-01 | UI | DEPLOY-ASSET-001 | LINE user — chọn 受付枠 | Boundary | manual | product | Trang đặt lịch bài học mở lại trong trình duyệt in-app của LINE sau release nhận JS mới: tab 週 bấm 「戻る」 không lỗi | - Trước release: trên điện thoại thật, bạn bè đã mở link đặt lịch bài học trong app LINE (webview đã cache JS cũ)<br>- Release bản fix lên production<br>- Setting hiển thị ưu tiên = 週 | 1. Sau release, mở lại link đặt lịch từ tin nhắn / richmenu trong app LINE (không xoá cache)<br>2. Chọn khoá học → bước chọn ngày giờ, giữ tab 「週」<br>3. Chọn 1 khung giờ còn chỗ → sang bước nhập thông tin<br>4. Bấm 「戻る」 | Thiết bị: 1 iOS + 1 Android | - Quay về bước chọn ngày giờ, bảng khung giờ tuần hiển thị đủ, khung giờ cũ bị bỏ chọn<br>- Trang không đứng / trắng; bấm tiếp các khung giờ khác vẫn được |  | Lấp Q3 · manual vì thiết bị thật (webview LINE) + production · Evidence: quay màn hình 2 thiết bị |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE user — mở link & entry | Normal | manual | staging | Bạn bè mở trang đặt lịch bài học trong app LINE, ở tab 週 bấm 「戻る」 từ bước nhập thông tin vẫn quay về bảng tuần | - Lịch bài học đang bật, khung giờ còn chỗ trong tuần hiện tại, setting hiển thị ưu tiên = 週<br>- Tài khoản LINE thật đã kết bạn với bot | 1. Trong app LINE, mở link đặt lịch bài học từ tin nhắn<br>2. Chọn khoá học, xác nhận tab mặc định 「週」<br>3. Chọn 1 khung giờ còn chỗ → sang 「お客様情報を入力してください」<br>4. Bấm 「戻る」<br>5. Chọn khung giờ khác, đi tiếp tới bước nhập thông tin | — | - Bước 4: về 「希望日時を選んでください」, tab 「週」, bảng khung giờ đủ, khung giờ cũ bỏ chọn<br>- Bước 5: sang bước nhập thông tin bình thường |  | Lấp Q4 · manual vì kết quả phải nhìn trên app LINE thật (webview, RULE-06) · Evidence: quay màn hình điện thoại |
| TC-REGURL001-01 | UI | REG-URL-001 | Redirect sau bill success | Normal | auto | Tất cả | Các URL hoàn tất thanh toán mở màn hoàn tất, không lỗi JS do thiếu khối điều khoản | - Đăng nhập owner<br>- DevTools Console bật Preserve log | 1. Lần lượt mở: `/monthly/standard_success`, `/yearly/standard_success`, `/monthly/pro_success`, `/yearly/pro_success`, `/admin/bot-add-v2?status=successful`<br>2. Mỗi URL: ghi status code + quan sát màn cuối + Console | 5 URL | - Mỗi URL: 200 (hoặc redirect về đúng màn hoàn tất), không treo spinner<br>- Console: không có lỗi liên quan `confirm_term` / `null` lúc tải trang |  | Lấp Q5 · jQuery ready của `bill_tool/index.js` chạy ở bước ≠ 1 (NEW-2 mới thử 1 biến thể) · dẫn từ `TC-BLP-360~363` · Evidence: screenshot Network status + Console |
| TC-REGURL001-02 | UI | REG-URL-001 | Redirect sau bill success | Boundary | auto | Tất cả | Biến thể URL hoàn tất có dấu 「/」 cuối và param thừa không treo, không lỗi JS | - Như TC-REGURL001-01 | 1. Mở `/monthly/standard_success/` (có `/` cuối)<br>2. Mở `/admin/bot-add-v2?status=successful&foo=1`<br>3. Quan sát màn + Console | 2 biến thể | - Cả 2 biến thể hiển thị màn đúng hoặc redirect hợp lệ, không treo spinner<br>- Console: 0 lỗi |  | Lấp Q5 · Evidence: screenshot Console |

Q7 / Q9 / Q10 và phần Normal của Q6: **không đề xuất TC mới** — chỉ cần đổi `viewpoint` trên Studio (`testcase_update`): NEW-2 / NEW-7 / NEW-11 / NEW-21 → `FUNC-001` (Abnormal); NEW-9 / NEW-13 → `REG-SHARED-001` (Normal); NEW-22 / NEW-23 → `UI-001`; ghi lý do RULE-01 ở `note` NEW-4 (Normal = NEW-1).

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/bot-add-v2` (chưa có mục khối 注意事項) + kho `TC-BLP-72` | Leader đã chốt (2026-09-28): khi chưa cuộn hết khối 注意事項, hover vào dòng chữ 「注意事項を読み、解約や返金について内容を理解しました」 **hoặc** ô checkbox → hiện tooltip 「注意事項を最後までスクロールして確認してください。」 (không có dòng chữ luôn hiện). Việc còn lại: (1) bổ sung mô tả này + ngưỡng cuộn + đánh dấu đã đọc vào spec; (2) kho `TC-BLP-72` (và `TC-BLP-185` màn gia hạn nếu cùng UI) thêm bước hover lên dòng chữ | C1 `CONF-KHO` ở §4 | Leader (đã chốt) — người cập nhật spec/kho |
