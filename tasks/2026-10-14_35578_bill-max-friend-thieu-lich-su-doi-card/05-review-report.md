# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #251 (ticket #35578, round 1, branch `ai_fixbug_35578`) |
| Tổng số TC review | 11 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 5/5 mục có TC (`BUG` · `F1` · `D1` · `T1` · `T2`) — **CHƯA ĐỦ**: cả 5 mục ở `RISK`, TC chạy thật đều `skip`, chỉ 2 TC đọc mã nguồn `pass` |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (1 file `PointSettingController.php`, +16 dòng) | 8/9 điểm có TC — **CHƯA ĐỦ**: 1 `GAP` (luồng gia hạn hợp đồng Dev nêu ở yokoten) · 8 `RISK` |

<!-- 9 điểm (b): (1) nhánh success acceptBillMaxFriendV2 ghi type 11 · (2) bản ghi mới bot_life_cycles · (3) không đổi payment_histories / bot_card_bill_friend · (4) hiển thị 操作履歴 + modal type 11 + bộ lọc · (5) rủi ro (a) hợp đồng chuyển khoản · (6) rủi ro (b) addState nuốt lỗi · (7) không backfill · (8) nhập lại đúng thẻ cũ qua form vẫn sinh lịch sử · (9) yokoten gia hạn hợp đồng. -->

**Kết luận**: 0/14 vùng ảnh hưởng đủ TC · 1 GAP · 13 RISK.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` · `F1` · `D1` · `T1` · `T2` + điểm (1)(2)(3)(4)(8): bill lại max friend bằng thẻ mới / thẻ đã lưu / thẻ mới bị từ chối / nhập lại thẻ cũ | dev-impact + diff code | NEW-1, NEW-2, NEW-3, NEW-5, NEW-6, NEW-7, NEW-9 (NEW-10, NEW-11 chỉ đọc mã) | `RISK` — 7 TC chạy thật đều `skip` ở staging (2026-10-12), chưa chạy prd. Pass duy nhất là 2 TC đọc mã nguồn, không chứng minh hệ thống chạy đúng | `[BLOCKER]` |
| G2 | Rủi ro (a): hợp đồng 銀行振込 trả phí max friend bằng thẻ → sinh dòng đổi thẻ chính | diff code | NEW-4 | `RISK` — chưa pass ở env nào. Tiền đề của NEW-4 mâu thuẫn kho `TC-BLP-336` (C1 §4) → chưa có chuẩn Đạt/Không đạt | `[MAJOR]` |
| G3 | Rủi ro (b): `BotLifeCycle::addState` nuốt lỗi — ghi lịch sử lỗi không được làm hỏng bill, cũng không được che lỗi | diff code | NEW-11 (đọc mã, pass) | `RISK` — chỉ đọc mã. Chưa có TC chạy thật khi ghi lịch sử lỗi, chưa kiểm lỗi có được ghi log | `[MAJOR]` |
| G4 | Không backfill lịch sử cho lần bill trước fix | diff code | NEW-8 | `RISK` — `skip` ở cả local và staging vì thiếu dữ liệu nền | `[MINOR]` |
| G5 | Yokoten Dev: gia hạn hợp đồng 「契約期間を1年延長する」 nhập thẻ mới cũng ghi đè thẻ chính mà không ghi lịch sử — Dev **không sửa** | diff code | không có | `GAP` — 0 TC. Quy tắc của fix (đổi thẻ chính phải có lịch sử) áp được cho nhánh này nhưng code nhánh này không đổi → đang sai sẵn | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 11 quan điểm Trigger khớp task (sau khi loại 5 mã ở dòng dưới bảng) · 9 chưa cover đủ · `DATA-001` đủ (NEW-9) · `ENV-003` chuyển §5 I2.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | `RISK` — luồng chính chỉ được cover bởi NEW-1, NEW-5, NEW-7, mà 3 TC này mang mã quan điểm Studio không thuộc checklist → tính là chưa cover. **Không cần TC mới**: đổi mã NEW-1 → `FUNC-001` trên Studio | `[BLOCKER]` |
| Q2 | `DATA-AUDIT-001` | Cao | `RISK` — chỉ có Normal (NEW-2; NEW-11 là đọc mã). Abnormal và Boundary nằm ở TC khác mã (NEW-6) hoặc mã lạ (NEW-7, NEW-8). Chưa kiểm "nhập thẻ nhiều lần trong 1 lượt → đúng 1 bản ghi, gắn đúng hợp đồng" (RULE-01, RULE-07) | `[MAJOR]` |
| Q3 | `PAY-STATE-001` | Cao | `RISK` — 2 Normal (NEW-4 đang mâu thuẫn kho, NEW-9). Abnormal có nội dung ở NEW-6 (mã `OUT-TRUTH-001`), thiếu Boundary → lấp bằng `TC-PAYABANDON001-01` (§7) | `[MAJOR]` |
| Q4 | `REG-SHARED-001` | Cao | `RISK` — NEW-10 mang mã này nhưng chỉ đọc mã của hàm đã sửa, không kiểm luồng tương tự Dev nêu ở yokoten | `[MAJOR]` |
| Q5 | `CONC-001` | Cao | `GAP` — 0 TC bấm đúp nút nộp thẻ / nộp trùng. Fix thêm lệnh ghi vào nhánh success → xử lý trùng sẽ sinh 2 dòng đổi thẻ | `[BLOCKER]` |
| Q6 | `PAY-ABANDON-001` | Cao | `GAP` — 0 TC rời luồng (đóng tab) ngay sau khi nộp thẻ mới | `[BLOCKER]` |
| Q7 | `STATE-001` | Cao | `GAP` — chuỗi charge → ghi đè thẻ chính → ghi lịch sử là ≥ 2 bước ghi tuần tự, chưa TC nào ngắt giữa chừng. Gộp chung TC với Q6 | `[BLOCKER]` |
| Q8 | `INTG-HOOK-002` | Trung bình | `GAP` — bill thành công phụ thuộc callback Univapay, chưa TC nào kiểm khi callback không tới / tới trễ | `[MAJOR]` |
| Q9 | `OUT-TRUTH-001` | Cao | `RISK` — có Normal (NEW-3) + Abnormal (NEW-6), thiếu Boundary → lấp bằng `TC-INTGHOOK002-01` (§7: màn không được báo hoàn tất giả khi chưa có callback) | `[MAJOR]` |

Đã loại khỏi phạm vi (nháp nội bộ, ghi lại để Leader tra): `DATA-DB-001` (fix chỉ INSERT, đoạn UPDATE `bot_contracts` không đổi — phần kiểm "đúng hợp đồng" đã gộp vào `TC-DATAAUDIT001-01`) · `INTG-HOOK-001` (lệnh ghi lịch sử nằm ở request đồng bộ, không nằm trong handler webhook — Dev mục 3) · `PAY-AMOUNT-001` / `PAY-BATCH-001` (Studio `dev_impact`: không đổi số tiền, không chạm job `HandleBillMaxFriend`) · `SEC-002` (NEW-11 đã chốt data lịch sử chỉ gồm gói / kỳ / 4 số cuối / phương thức, không chứa token) · `ENV-003` → xem §5 I2.

---

## 3. TC trùng lặp nội dung

Đã rà 11 TC, không phát hiện trùng lặp. NEW-2 và NEW-9 cùng đọc 4 số cuối trong modal đổi thẻ nhưng mục đích khác nhau (NEW-2: đủ trường modal · NEW-9: khớp màn – DB – Univapay); NEW-10 và NEW-11 đều đọc mã nhưng kiểm 2 việc khác nhau (vị trí/điều kiện · cấu trúc data/try-catch).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-4 vs kho `TC-BLP-336` (`kho-tcs/fa031-…md` L487) | Hợp đồng bill 銀行振込 thanh toán phí theo lượng bạn bè ở màn 「従量課金の決済」 | NEW-4 bước 2: "chọn phương thức thanh toán là thẻ tín dụng" → sinh dòng 「メインクレジットカード変更」, 決済カード情報 = thẻ mới | `TC-BLP-336`: "Bot bill transfer: chỉ hiện 銀行振込, KHÔNG hiện số thẻ · Không cho chọn phương thức khác phương thức của hợp đồng gốc" (SpecImprove) | (A) NEW-4 sai: UI không cho chọn thẻ → rủi ro (a) Dev nêu không vào được từ UI, NEW-4 cần xóa hoặc đổi tiền đề · (B) kho cũ: UI vẫn cho chọn thẻ → cập nhật `TC-BLP-336` | `[MAJOR]` | Dev (xác nhận code) + Leader |

**Đã rà**: 11 TC × `spec-features/admin/billing-plan/feature-spec.md` (L207-224 操作履歴, L563 BR-02, L713 HandleBillMaxFriend) + `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm 17 Thẻ chính & thẻ phụ, 18 Gia hạn, 23 Lịch sử thao tác, 33-34 Bill max friend) — 1 mâu thuẫn (C1). Không có `CONF-TC`, `CONF-SPEC`, `CONF-IGNORE`.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ nguồn | Pass 2/11 (18%). 2 TC pass (NEW-10, NEW-11) chỉ đọc mã nguồn. 9 TC chạy thật `skip` ở staging; NEW-4, NEW-8 chưa pass ở env nào. `aiResult=pass` của task **không** có nghĩa đã kiểm hành vi thật | Chạy lại NEW-1 → NEW-9 trên env có bot ≥ 100.000 bạn bè + Univapay test. Không đóng ticket khi chưa có ít nhất NEW-1, NEW-5, NEW-6 pass |
| I2 | `[MAJOR]` | Toàn bộ nguồn | RULE-08 / `ENV-003`: task bill tiền nhưng 0 TC chạy prd | Sau release: dùng ca KH thật đầu tiên bill lại max friend bằng thẻ mới để chạy NEW-2, NEW-3, NEW-9 ở chế độ chỉ đọc; chạy NEW-8 chỉ đọc trên prd |
| I3 | `[MAJOR]` | `03-dev-impact.md` mục 5 | RULE-04: Dev ghi "Không cần recover data" nhưng không có thống kê toàn hệ thống. Mọi hợp đồng prd đã bill lại max friend bằng thẻ mới trước fix (gồm ca retest 21/8) đang thiếu dòng đổi thẻ chính | Dev chạy query đếm số hợp đồng bị ảnh hưởng → Leader/PM chốt có Recover data không. Expected NEW-8 ("không backfill") phụ thuộc quyết định này |
| I4 | `[MAJOR]` | NEW-1 | Expected "THÊM đúng 2 dòng" bỏ qua dòng 決済エラー có thể sinh ra khi thẻ đã lưu bị từ chối ở bước 4. NEW-6 tự thừa nhận "có lịch sử lỗi được ghi theo hành vi hiện tại" → NEW-1 có thể Không đạt oan | Đếm theo từng loại: "thêm đúng 1 dòng 「メインクレジットカード変更」 + 1 dòng 「友だち数別の従量課金」; dòng 決済エラー (nếu có) không tính" |
| I5 | `[MAJOR]` | NEW-1 → NEW-9 | Spec thiếu: `billing-plan/feature-spec.md` chỉ mô tả job `HandleBillMaxFriend` (L713), không có luồng web bill lại max friend và quy tắc ghi type 11. Cả 11 TC để trống `Trạng thái đánh giá spec` → expected đang dựa vào code / Redmine | Leader xác nhận quy tắc (§8 #2, #3) rồi cập nhật `Trạng thái đánh giá spec` trên Studio |
| I6 | `[MINOR]` | NEW-2, NEW-3, NEW-9 | Tiền điều kiện = "Đã chạy xong TC 「Bill lại nhập thẻ mới thành công…」" → NEW-1 `skip` kéo cả 3 `skip` theo | Viết tiền điều kiện theo trạng thái dữ liệu (hợp đồng có dòng 「メインクレジットカード変更」 từ lần bill lại max friend bằng thẻ mới, 4 số cuối, thời điểm), cho phép dùng ca bất kỳ thỏa điều kiện |
| I7 | `[MINOR]` | NEW-8 | `skip` ở local + staging vì thiếu dữ liệu nền | Dùng chính ca retest 21/8 của #35578 (Journal #131899: chỉ có lịch sử bill max friend success, không có change main card) làm dữ liệu |
| I8 | `[MINOR]` | `03-dev-impact.md` mục 2 | Yokoten chỉ có kết luận "còn 1 chỗ (gia hạn)", không kê các luồng đã quét. Kho có ít nhất 4 luồng khác cũng thay thẻ chính bằng thẻ nhập mới: upgrade (`TC-BLP-85`), hợp đồng lại (`TC-BLP-211`), đổi kỳ (`TC-BLP-159`), 延滞中 đổi thẻ (`TC-BLP-140`) | Yêu cầu Dev kê từng luồng + đã ghi type 11 chưa (evidence của `REG-SHARED-001`) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 11 TC — không có TC nào ngoài phạm vi task. NEW-10, NEW-11 (đọc mã) map `F1` / `D1` và là TC duy nhất kiểm try-catch của `addState`; NEW-8 dẫn từ hành vi "không backfill" của Studio `dev_impact`.

---

## 7. TCs đề xuất bổ sung (6)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (targeted: nhóm 17, 18, 23, 33, 34) |
| Vùng regression phát hiện từ kho | Nhóm 18 Gia hạn hợp đồng (`TC-BLP-186`, `TC-BLP-187`) — luồng ghi đè thẻ chính Dev nêu ở yokoten |
| Conflict expected vs kho | NEW-4 vs `TC-BLP-336` → C1, đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | G2 → `TC-BLP-336` "Màn confirm max friend: phương thức thanh toán khóa theo phương thức của hợp đồng gốc" — chạy để chốt C1 |
| GAP không đẻ TC mới (trùng TC đã có, BƯỚC 5b) | G1 → chạy lại NEW-1…NEW-9 (§5 I1) · G4 → sửa dữ liệu của NEW-8 (§5 I7) · Q1 → đổi mã NEW-1 trên Studio |
| Căn cứ TC regression `R<x>` | Không có TC R — luồng gia hạn đã đi theo G5 |
| Xác nhận chống trùng | Đã đối chiếu 11 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATAAUDIT001-01 | UI | DATA-AUDIT-001 | Contract detail 契約詳細: Bill lại phí theo lượng bạn bè 従量課金 — nhập thẻ mới 2 lần trong 1 lượt | Boundary | auto | dev, local, prd, staging | web | Bill lại max friend: thẻ mới thứ nhất bị từ chối, thẻ mới thứ hai thành công → chỉ 1 dòng đổi thẻ chính, đúng thẻ thứ hai, đúng hợp đồng | - Env có cổng Univapay test; không dùng hợp đồng / thẻ khách hàng thật<br>- Đăng nhập admin owner của 2 bot test B01, B02 (cùng owner)<br>- B01: hợp đồng Pro bill thẻ, ≥ 100.000 bạn bè, đang bill lỗi phí theo lượng bạn bè — Detail hợp đồng 契約詳細 hiện banner 「決済エラー」<br>- Thẻ chính hiện tại của B01 = thẻ X, cổng test từ chối thẻ X<br>- B02: hợp đồng bill thẻ, Status hợp đồng ステータス 正常<br>- Thẻ A: đúng định dạng nhưng cổng test từ chối khi charge · Thẻ B: hợp lệ, charge thành công · 4 số cuối X, A, B khác nhau<br>- Trước khi chạy: chụp khối 操作履歴 của B01 và B02, đếm số dòng 「メインクレジットカード変更」 của từng bot | 1. Mở Detail hợp đồng 契約詳細 của B01, bấm 「決済にすすむ」 trên banner 「決済エラー」.<br>2. Ở bước 「内容確認」 giữ 「登録済みクレジットカード」, bấm 「決済情報の確認に進む」.<br>3. Ở bước 「決済情報確認」 bấm 「決済する」 — thẻ X bị từ chối, màn hiện form nhập thẻ.<br>4. Nhập thẻ A vào form, bấm nút nộp.<br>5. Nhập thẻ B vào form trên cùng màn, bấm nút nộp.<br>6. Chờ màn hiện 「従量課金決済が完了しました。」.<br>7. Mở Detail hợp đồng 契約詳細 của B01, xem khối 操作履歴 và mục 決済カード情報.<br>8. Mở chi tiết dòng 「メインクレジットカード変更」 mới nhất.<br>9. Mở Detail hợp đồng 契約詳細 của B02, xem khối 操作履歴. | Thẻ A (charge bị từ chối) · Thẻ B (charge thành công) | - Bước 4: báo lỗi thanh toán, không sang 「完了」<br>- Bước 6: hiện 「従量課金決済が完了しました。」<br>- B01 操作履歴: số dòng 「メインクレジットカード変更」 = trước + 1 — chỉ có dòng cho thẻ B, không có dòng cho thẻ A vì thẻ A không charge được<br>- Modal chi tiết: 変更後のクレジットカード = ****-****-****-<4 số cuối thẻ B><br>- B01 決済カード情報 = thẻ B<br>- B02 操作履歴: số dòng 「メインクレジットカード変更」 = trước — B02 không thao tác gì | | Lấp Q2 · Đánh giá spec: Spec không ghi (billing-plan chỉ liệt kê type 11, không mô tả luồng bill lại max friend) — cần Leader xác nhận · Evidence: ảnh 操作履歴 trước/sau của B01 + B02, ảnh modal, giao dịch Univapay của thẻ A (declined) và B (success) · Dòng 決済エラー của lần thẻ X / thẻ A bị từ chối (nếu có) không tính vào số dòng đổi thẻ · thiếu Abnormal ở TC này: đã có TC-DATAAUDIT001-02 |
| TC-DATAAUDIT001-02 | UI | DATA-AUDIT-001 | Contract detail 契約詳細: Bill lại 従量課金 bằng thẻ mới khi ghi Lịch sử thao tác 操作履歴 bị lỗi | Abnormal | auto | dev, local, staging | web | Ghi lịch sử đổi thẻ chính bị lỗi khi bill lại max friend bằng thẻ mới → thanh toán vẫn hoàn tất, lỗi được ghi log | - Env local / dev nơi Dev làm lỗi được việc ghi lịch sử hợp đồng (vd tạm thu quyền INSERT bảng bot_life_cycles của user DB) — khôi phục sau khi chạy<br>- Cổng Univapay test<br>- Đăng nhập admin owner bot test B01<br>- B01: hợp đồng Pro bill thẻ, ≥ 100.000 bạn bè (local được seed), đang bill lỗi phí theo lượng bạn bè — banner 「決済エラー」<br>- Thẻ chính hiện tại = thẻ X, cổng test từ chối thẻ X<br>- Thẻ B: hợp lệ, charge thành công, 4 số cuối khác X<br>- Ghi lại số dòng 「メインクレジットカード変更」 trong 操作履歴 và vị trí file log ứng dụng | 1. Bật chế độ lỗi ghi lịch sử theo hướng dẫn của Dev.<br>2. Mở Detail hợp đồng 契約詳細 của B01, bấm 「決済にすすむ」.<br>3. Ở 「内容確認」 giữ 「登録済みクレジットカード」, bấm 「決済情報の確認に進む」.<br>4. Ở 「決済情報確認」 bấm 「決済する」 — thẻ X bị từ chối, màn hiện form nhập thẻ.<br>5. Nhập thẻ B, bấm nút nộp.<br>6. Quan sát màn hình đến khi có kết quả.<br>7. Mở Detail hợp đồng 契約詳細, xem 決済カード情報 và 操作履歴.<br>8. Mở Lịch sử biên lai thanh toán 決済履歴.<br>9. Mở log ứng dụng, tìm lỗi ghi lịch sử quanh thời điểm bước 5.<br>10. Tắt chế độ lỗi. | Thẻ B (charge thành công) | - Bước 6: hiện 「従量課金決済が完了しました。」 — thanh toán đã thành công nên không báo lỗi cho user<br>- 決済カード情報 = thẻ B<br>- Lịch sử biên lai thanh toán 決済履歴 có 1 bản ghi phí theo lượng bạn bè mới; Univapay test có 1 charge thành công bằng thẻ B<br>- Banner 「決済エラー」 không còn<br>- 操作履歴: không có dòng 「メインクレジットカード変更」 mới (do ghi lỗi)<br>- Log ứng dụng có 1 dòng lỗi ghi lịch sử, nhận diện được hợp đồng của B01 — lỗi không bị nuốt im lặng | | Lấp G3 · căn cứ Studio `dev_impact` rủi ro (b): "BotLifeCycle::addState tự nuốt lỗi … cần đảm bảo không che lỗi thật" · bổ sung chạy thật cho NEW-11 (chỉ đọc mã) · không chạy prd vì phải cố ý làm lỗi ghi DB; TC kiểm hành vi code khi ghi lỗi, không kiểm khác biệt môi trường → RULE-08 không áp — Leader quyết · Đánh giá spec: Spec không ghi · Evidence: ảnh màn 完了, 決済カード情報, 操作履歴, 決済履歴 + dòng log lỗi · log không có dòng lỗi → báo Dev (lỗi bị che) |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Contract detail 契約詳細: Gia hạn hợp đồng 「契約期間を1年延長する」 bằng thẻ mới — lịch sử đổi thẻ chính | Normal | auto | dev, local, prd, staging | web | Gia hạn hợp đồng năm bằng thẻ mới (thẻ đã lưu bị từ chối) thành công → có đúng 1 dòng đổi thẻ chính trong 操作履歴 | - Env có cổng Univapay test; không dùng hợp đồng / thẻ khách hàng thật<br>- Đăng nhập admin owner bot test B03<br>- B03: hợp đồng Standard, Kỳ hạn thanh toán お支払い期間 = 年間一括, bill thẻ, Status hợp đồng ステータス 正常<br>- Thẻ chính hiện tại = thẻ X, cổng test từ chối thẻ X<br>- Thẻ B: hợp lệ, charge thành công, 4 số cuối khác X<br>- Ghi lại số dòng 「メインクレジットカード変更」 trong 操作履歴 của B03 | 1. Mở Detail hợp đồng 契約詳細 của B03, bấm 「契約期間を1年延長する」.<br>2. Ở step 1 cuộn hết 注意事項, tick checkbox, bấm 「決済に進む」.<br>3. Thẻ X bị từ chối — màn hiện step 2 nhập thẻ.<br>4. Nhập thẻ B, bấm thanh toán.<br>5. Chờ step 3 gia hạn thành công.<br>6. Mở Detail hợp đồng 契約詳細 của B03, xem 決済カード情報 và 操作履歴.<br>7. Mở chi tiết dòng 「メインクレジットカード変更」 mới nhất. | Thẻ B (charge thành công) | - Bước 5: hiện step 3 gia hạn thành công<br>- 決済カード情報 = thẻ B<br>- 操作履歴: số dòng 「メインクレジットカード変更」 = trước + 1 (nhóm 変更) — vì thẻ chính đã bị thay bằng thẻ B<br>- Modal chi tiết: 変更後のクレジットカード = ****-****-****-<4 số cuối thẻ B> | | Lấp G5 · Q4 · regression — luồng tương tự Dev nêu ở yokoten (Redmine Journal #133250 mục 2: "gia hạn hợp đồng nhập thẻ mới — chỉ ghi nhận, không sửa") · dẫn từ kho `TC-BLP-187` (gia hạn, thẻ đã lưu lỗi → step 2) · ⚠ dự kiến Không đạt trên branch `ai_fixbug_35578` vì nhánh này chưa sửa → Không đạt thì raise ticket riêng, không chặn #35578 · Đánh giá spec: Spec không ghi — chờ Leader chốt quy tắc §8 #2 · Evidence: ảnh 操作履歴 trước/sau, modal, giao dịch Univapay · thiếu Abnormal: gia hạn thẻ mới lỗi đã có kho `TC-BLP-187`; Boundary: không có khái niệm biên |
| TC-CONC001-01 | UI | CONC-001 | Contract detail 契約詳細: Bill lại 従量課金 — bấm đúp nút nộp form thẻ mới | Abnormal | auto | dev, local, prd, staging | web | Bấm đúp nút nộp form thẻ mới khi bill lại max friend → chỉ 1 lần charge, 1 dòng phí theo lượng bạn bè, 1 dòng đổi thẻ chính | - Env có cổng Univapay test; không dùng hợp đồng / thẻ khách hàng thật<br>- Đăng nhập admin owner bot test B01<br>- B01: hợp đồng Pro bill thẻ, ≥ 100.000 bạn bè, đang bill lỗi phí theo lượng bạn bè — banner 「決済エラー」<br>- Thẻ chính hiện tại = thẻ X, cổng test từ chối thẻ X<br>- Thẻ B: hợp lệ, charge thành công, 4 số cuối khác X<br>- Ghi lại số dòng 「メインクレジットカード変更」 và 「友だち数別の従量課金」 trong 操作履歴, số bản ghi trong 決済履歴 | 1. Mở Detail hợp đồng 契約詳細 của B01, bấm 「決済にすすむ」.<br>2. Ở 「内容確認」 giữ 「登録済みクレジットカード」, bấm 「決済情報の確認に進む」.<br>3. Ở 「決済情報確認」 bấm 「決済する」 — thẻ X bị từ chối, màn hiện form nhập thẻ.<br>4. Nhập thẻ B, bấm nút nộp 2 lần liên tiếp thật nhanh (double-click).<br>5. Chờ kết quả trên màn.<br>6. Mở Univapay test, lọc giao dịch theo thời điểm bước 4.<br>7. Mở Detail hợp đồng 契約詳細 của B01, xem 操作履歴.<br>8. Mở Lịch sử biên lai thanh toán 決済履歴. | Thẻ B (charge thành công) | - Màn hiện 「従量課金決済が完了しました。」, không lỗi 500, không báo trùng<br>- Univapay: đúng 1 charge thành công bằng thẻ B cho lần thao tác này<br>- 操作履歴: 「メインクレジットカード変更」 = trước + 1 và 「友だち数別の従量課金」 = trước + 1<br>- 決済履歴: số bản ghi = trước + 1 | | Lấp Q5 · fix thêm lệnh ghi vào nhánh success → xử lý trùng sẽ sinh 2 dòng đổi thẻ · Đánh giá spec: Spec không ghi · Evidence: log request + giao dịch Univapay + ảnh 操作履歴 trước/sau · thiếu Normal: bấm 1 lần đã có NEW-1; thiếu Boundary: kịch bản 2 tab cùng bill lại có cùng oracle với TC này — Leader quyết có tách không |
| TC-PAYABANDON001-01 | UI | PAY-ABANDON-001 | Contract detail 契約詳細: Bill lại 従量課金 — đóng tab ngay sau khi nộp thẻ mới | Abnormal | auto | dev, local, prd, staging | web | Đóng tab ngay sau khi nộp thẻ mới ở bill lại max friend → thẻ chính, lịch sử đổi thẻ và trạng thái thanh toán nhất quán với giao dịch thật | - Env có cổng Univapay test; không dùng hợp đồng / thẻ khách hàng thật<br>- Đăng nhập admin owner bot test B01<br>- B01: hợp đồng Pro bill thẻ, ≥ 100.000 bạn bè, đang bill lỗi phí theo lượng bạn bè — banner 「決済エラー」<br>- Thẻ chính hiện tại = thẻ X, cổng test từ chối thẻ X<br>- Thẻ B: hợp lệ, charge thành công, 4 số cuối khác X<br>- Ghi lại số dòng 「メインクレジットカード変更」 trong 操作履歴 và số bản ghi 決済履歴 | 1. Mở Detail hợp đồng 契約詳細 của B01, bấm 「決済にすすむ」.<br>2. Ở 「内容確認」 giữ 「登録済みクレジットカード」, bấm 「決済情報の確認に進む」.<br>3. Ở 「決済情報確認」 bấm 「決済する」 — thẻ X bị từ chối, màn hiện form nhập thẻ.<br>4. Nhập thẻ B, bấm nút nộp rồi đóng tab trình duyệt ngay, trước khi màn đổi.<br>5. Chờ 5 phút.<br>6. Mở Univapay test, kiểm tra giao dịch thẻ B.<br>7. Mở tab mới, mở Detail hợp đồng 契約詳細 của B01: xem banner, 決済カード情報, 操作履歴.<br>8. Mở Lịch sử biên lai thanh toán 決済履歴. | Thẻ B (charge thành công) | - 決済カード情報 = thẻ B ⇔ 操作履歴 có đúng 1 dòng 「メインクレジットカード変更」 mới; 決済カード情報 vẫn là thẻ X ⇔ không có dòng mới<br>- Univapay có charge thành công thẻ B ⇔ 決済履歴 có 1 bản ghi phí theo lượng bạn bè mới và banner 「決済エラー」 không còn<br>- Không có trạng thái: thẻ B đã bị trừ tiền mà sau 5 phút banner vẫn 「決済エラー」 | | Lấp Q6 · Q7 · Q3 (Boundary của PAY-STATE-001) · Đánh giá spec: Spec không ghi trạng thái cuối khi rời luồng — cần Dev xác nhận thiết kế (charge thành công qua callback thì thẻ chính có đổi sang thẻ B không) · Evidence: giao dịch Univapay + ảnh 契約詳細 / 操作履歴 / 決済履歴 sau 5 phút · thiếu Normal: luồng hoàn tất đã có NEW-1; Boundary: quan điểm chỉ có kịch bản rời luồng |
| TC-INTGHOOK002-01 | UI | INTG-HOOK-002 | Contract detail 契約詳細: Bill lại 従量課金 bằng thẻ mới khi callback Univapay không tới | Abnormal | auto | dev, local, staging | web | Callback Univapay không tới khi bill lại max friend bằng thẻ mới → không báo hoàn tất giả, không đổi thẻ chính mà thiếu lịch sử | - Env local / dev / staging có cổng Univapay test, Dev chặn được webhook `charge_finished` tới server<br>- Đăng nhập admin owner bot test B01<br>- B01: hợp đồng Pro bill thẻ, ≥ 100.000 bạn bè, đang bill lỗi phí theo lượng bạn bè — banner 「決済エラー」<br>- Thẻ chính hiện tại = thẻ X, cổng test từ chối thẻ X<br>- Thẻ B: hợp lệ, charge thành công, 4 số cuối khác X<br>- Ghi lại số dòng 「メインクレジットカード変更」 trong 操作履歴 và số bản ghi 決済履歴 | 1. Nhờ Dev chặn webhook `charge_finished` của Univapay test tới server.<br>2. Mở Detail hợp đồng 契約詳細 của B01, bấm 「決済にすすむ」.<br>3. Ở 「内容確認」 giữ 「登録済みクレジットカード」, bấm 「決済情報の確認に進む」.<br>4. Ở 「決済情報確認」 bấm 「決済する」 — thẻ X bị từ chối, màn hiện form nhập thẻ.<br>5. Nhập thẻ B, bấm nút nộp.<br>6. Chờ đến khi màn có kết quả, tối đa 5 phút.<br>7. Xem Detail hợp đồng 契約詳細 của B01: banner, 決済カード情報, 操作履歴.<br>8. Bỏ chặn webhook, gửi lại webhook của giao dịch thẻ B từ Univapay test.<br>9. Xem lại Detail hợp đồng 契約詳細 và Lịch sử biên lai thanh toán 決済履歴. | Thẻ B (charge thành công) | - Bước 6: màn không hiện 「従量課金決済が完了しました。」 khi chưa nhận callback; có thông báo hoặc trạng thái chờ rõ ràng, không loading vô hạn<br>- Bước 7: 決済カード情報 = thẻ B ⇔ có đúng 1 dòng 「メインクレジットカード変更」 mới; còn thẻ X ⇔ không có dòng mới<br>- Bước 9: 決済履歴 = trước + 1 bản ghi phí theo lượng bạn bè; banner 「決済エラー」 không còn<br>- Bước 9: quan hệ 決済カード情報 ⇔ dòng 「メインクレジットカード変更」 vẫn đúng như bước 7 | | Lấp Q8 · Q9 (Boundary của OUT-TRUTH-001) · không chạy prd vì phải chặn webhook thanh toán; TC kiểm cách code xử lý khi thiếu callback → RULE-08 không áp — Leader quyết · không dùng mốc chờ 2 phút làm oracle (chưa xác nhận — xem note NEW-6) · Đánh giá spec: Spec không ghi · Evidence: log webhook (chặn / gửi lại) + ảnh màn bước 6, 7, 9 |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/billing-plan/feature-spec.md` BR-02 (L563) | Ghi rõ phương thức thanh toán phí theo lượng bạn bè = phương thức của hợp đồng gốc; hợp đồng 銀行振込 có được trả bằng thẻ không | C1 `CONF-KHO` (NEW-4 vs `TC-BLP-336`) | Dev + Leader |
| 2 | `spec-features/admin/billing-plan/feature-spec.md` 操作履歴 (L207-224) | Thêm quy tắc: mọi luồng thay thẻ chính bằng thẻ **nhập mới** (đổi thẻ, bill lại max friend, gia hạn 「契約期間を1年延長する」, hợp đồng lại, upgrade, đổi kỳ) sinh đúng 1 dòng type 11; dùng thẻ đã lưu thì không sinh. Liên quan kho MT-20 (hợp đồng lại hiện thừa dòng đổi thẻ chính — đang chờ quyết định) | G5 §1 (yokoten gia hạn, Dev chưa sửa) | Leader / PM |
| 3 | `spec-features/admin/billing-plan/feature-spec.md` HandleBillMaxFriend (L713) | Bổ sung luồng web bill lại max friend (`acceptBillMaxFriendV2`, route `/admin/payment-max-friend/{id}/bill-again`): thẻ đã lưu lỗi → form thẻ mới → thành công thì ghi đè thẻ chính + ghi type 11; không fallback thẻ phụ (kho MT-08) | §5 I5 | Dev |
