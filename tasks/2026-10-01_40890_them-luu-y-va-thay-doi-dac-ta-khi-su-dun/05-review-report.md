# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #330 (ticket 40890, round 3, branch `ai-feature-40890`) |
| Tổng số TC review | 23 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 7/7 mục có TC — **ĐỦ** (yêu cầu chính: banner trên 2 item mặc định · F1 partial · F2 form Lesson · F3 form Salon · T1 · T2 · T3 preview/màn khách; D1 = không có data) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (3 file blade, +30/−0) | 5/7 điểm có TC — **CHƯA ĐỦ** (3 file sửa · rủi ro quên 1 hệ · rủi ro rò banner sang item tự thêm · rủi ro xô lệch layout panel ③ · điều kiện hiển thị theo item mặc định, độc lập trạng thái) |

**Kết luận**: 12/14 vùng ảnh hưởng đủ TC · 0 GAP · 2 RISK.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Rủi ro hồi quy (2) của `dev_impact`: "banner rò rỉ sang item admin tự thêm nếu điều kiện sai" — đúng ranh giới human chốt: *"2 item default loại メールアドレス và お名前. Các item khác thì không add"* | `diff code` | NEW-10 · NEW-21 · NEW-7 | **RISK** — TC âm tính chỉ dùng câu hỏi tự thêm "trơn" (nội dung `TC40890 tu them…`, không liên kết friend info). Chưa có TC cho biến thể **dễ nhầm nhất**: câu hỏi tự thêm **trông giống item mặc định** — cùng nội dung 「お名前を入力してください」/「メールアドレスを入力してください」, liên kết friend info họ tên / email, 入力内容 = メールアドレス. Cấu hình này có thật (kho `TC-LSN-374` "item KHÁC cũng liên kết vào họ tên / email"). Nếu Dev nhận diện theo loại/liên kết thay vì theo item mặc định, chỉ biến thể này mới bắt được | `[MAJOR]` |
| G2 | Điều kiện hiển thị "theo item mặc định" phải **độc lập trạng thái của chính item** | `diff code` | NEW-9 · NEW-19 · NEW-6 | **RISK** — độc lập theo trạng thái 決済連携 đã test, nhưng mọi TC đều để 2 item mặc định ở 表示 + 必須. Khi 決済連携 = 利用なし, admin tắt hiển thị / đổi sang 任意 được (kho `TC-LSN-372`, `TC-SLN-316`) → chưa TC nào xác nhận banner vẫn hiện ở trạng thái đó (human chốt: đối tượng add là 2 item mặc định, không kèm điều kiện trạng thái) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp task · 5 chưa cover đủ. Trong đó **Q1 · Q2 · Q3 nội dung đã có TC** nhưng TC mang mã lạ / mã catalog / mã RULE → chỉ cần **gắn lại mã trên Studio**, không đẻ TC. Thiếu thật: **Q4 · Q5**. Đủ: `UI-003` (NEW-11) · `FUNC-SEQ-001` (NEW-7, NEW-22) · `FUNC-004` (NEW-16) · `PERM-001` (NEW-15).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `UI-001` | Trung bình | RISK — 0 TC mang mã. Nội dung hiển thị banner (vị trí · nguyên văn · màu · khoảng cách · chỉ-đọc) nằm ở NEW-3 (`I18N-001`), NEW-4 / NEW-8 (`UIC-06` — mã catalog), NEW-5 (`UIC-12` — mã catalog), NEW-18 (`RULE-TOOL-028`) → gắn lại `UI-001`, chuyển `UIC-06`/`UIC-12` sang trường `catalog` | `[MINOR]` |
| Q2 | `OUT-PREVIEW-001` | Cao | RISK — màn có toggle 「プレビュー」; nội dung đã có ở NEW-13 nhưng mang mã `TOOL-NEGCTRL-001` → gắn lại mã. RULE-01: Normal + Abnormal đã nằm trong NEW-13; Boundary không áp dụng (banner tĩnh, không có biên) — ghi lý do vào Ghi chú NEW-13 | `[MAJOR]` |
| Q3 | `REG-SHARED-001` | Cao | RISK RULE-01 — chỉ NEW-17 (Normal) mang mã. Abnormal của hệ Salon có ở NEW-21 (`TOOL-NEGCTRL-001`), Boundary ở NEW-20 (`RULE-12` — là RULE, không phải mã quan điểm) → gắn lại mã. TC đề xuất `TC-REGSHARED001-01` (G1 bản Salon) bổ sung thêm 1 Abnormal | `[MAJOR]` |
| Q4 | `COMPAT-LEGACY-001` | Cao | RISK RULE-01 — NEW-14 / NEW-23 chỉ Normal, không ghi lý do thiếu Abnormal / Boundary. Biên đáng test: lịch cũ có item họ tên / email mà cờ "không cho xoá" không còn đúng (spec lesson-booking **RA-06**: `updateSettingForm` mass-assignment đổi được `can_delete` của mục hệ thống). Chưa có bằng chứng dữ liệu như vậy tồn tại → **không đẻ TC**, hỏi Dev (§8 #3); nếu Dev xác nhận không có → ghi lý do vào Ghi chú NEW-14 / NEW-23 | `[MAJOR]` |
| Q5 | `DATA-ID-001` | Trung bình → Cao (màn chọn đối tượng để thao tác) | RISK RULE-01 — chỉ Boundary (NEW-6: item mặc định đổi nội dung vẫn hiện banner). Thiếu Abnormal: item **không phải** mặc định nhưng trùng nội dung / liên kết → lấp bằng G1 (`TC-DATAID001-01`) | `[MAJOR]` |

Đã loại khỏi phạm vi (nháp quét 50 nhóm Coverage của `kho-tcs/fa019-*.md` + 31 nhóm FA-020):
- `SYNC-APP-001` — App mobile chỉ có xem/thao tác booking (kho nhóm 48: `TC-LSN-615`/`616`), không có màn setting 質問項目.
- `JOB-*` · `OUT-EXPORT-001` · `INTG-*` · `LIFF-ENTRY-*` — diff chỉ 3 file blade admin, không chạm API/BE/DB/Job; màn khách đã có đối chứng âm NEW-13.
- `ENV-003` / RULE-08 — không chạm media / domain / job / thanh toán (banner tĩnh, không đổi logic 決済).

---

## 3. TC trùng lặp nội dung

Đã rà 23 TC, không phát hiện trùng lặp. Các cặp Lesson ↔ Salon (NEW-1/3 ↔ NEW-17 · NEW-4/5 ↔ NEW-18 · NEW-9 ↔ NEW-19 · NEW-12/16 ↔ NEW-20 · NEW-10/11 ↔ NEW-21 · NEW-14 ↔ NEW-23) khác `đối tượng` (2 file `setting_form.blade.php` riêng) → không tính trùng. Bước 4 của NEW-8 (kéo-thả + tải lại) chồng một phần với NEW-22 — xử lý ở §5 I1 (atomic), không đề nghị xóa TC.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-16 · NEW-20 | Ô 「質問内容」 khi nhập ký tự thứ 51 | Ký tự thứ 51 **không nhập vào được**, bộ đếm dừng 50/50; dán 60 ký tự bị **cắt còn 50** (chặn tại ô nhập) | Kho `TC-LSN-355` bước 3: "Nhập 51 ký tự → **báo lỗi vượt ký tự**" (cho nhập rồi báo lỗi) | ✅ **Leader chốt 2026-10-01**: chặn nhập ở ký tự thứ 51 → NEW-16 / NEW-20 **đúng**, kho cũ. **Đã update kho** `TC-LSN-355` (`kho-tcs/data/lsn_s6_setting.py` → build md + sheet) | `[MAJOR]` → đã xử lý | Leader |

**Đã rà**: 23 TC × `spec-features/admin/lesson-booking/feature-spec.md` (BR-07, BR-50, RA-06) + `spec-features/admin/salon-booking/feature-spec.md` + `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm 28 「予約時のお客様への質問項目」, 31 TC) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 31, 7 TC) — 1 mâu thuẫn (C1). Spec Salon **không mô tả nội dung panel ③ của màn 質問項目** (feature-spec mục open question "Nội dung modal edit từng mục trong 予約設定 … 質問項目") → phía Salon chỉ đối chiếu được với kho.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | NEW-8 | Không atomic — gộp 2 mục đích không liên quan: banner chỉ-đọc (REQ-006) + kéo-thả sắp xếp được lưu sau tải lại (RG-05). Bước 4 đã được NEW-22 cover (kéo-thả + tải lại + banner theo đúng item) | Bỏ bước 4 khỏi NEW-8, để NEW-8 chỉ kiểm banner chỉ-đọc |
| I2 | `[MINOR]` | NEW-15 · NEW-22 | Tiền đề ghi "lịch Lesson **hoặc** Salon" → chạy 1 hệ là `pass`, không chứng minh được cả 2 hệ (đúng rủi ro (1) của `dev_impact`: quên 1 hệ) | Sửa tiền đề / data thành "chạy lần lượt trên cả 2 hệ", expected tách kết quả từng hệ |
| I3 | `[MINOR]` | NEW-22 · NEW-23 | `exec_mode = manual` nhưng không thuộc 4 lý do được phép (production / thiết bị thật / mail thật / mắt người) — kéo-thả và mở lịch cũ runner làm được | Đổi `exec_mode` sang `auto` trên Studio |
| I4 | `[MINOR]` | NEW-22 · NEW-23 | `requirement_keys` rỗng (2 TC người thêm tay) → không trace được về requirement | Gắn REQ-001 + REQ-003 (NEW-22), REQ-008 (NEW-23) |
| I5 | `[NIT]` | NEW-9 · NEW-19 | Expected chỉ nêu ẩn 「表示設定」「回答設定」 khi bật 決済連携; kho `TC-LSN-371` ghi ẩn cả 「入力内容」 | Bổ sung 「入力内容」 vào expected để bắt đủ hành vi cũ |
| I6 | `[NIT]` | 23/23 TC | `env_scope = all` nhưng 100% chỉ chạy `local` (3 run, 0 run dev/staging/prd). Không thuộc RULE-08 nên không bắt buộc production | Chạy lại 1 vòng staging trước khi đóng task |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 23 TC — không có TC nào ngoài phạm vi task. NEW-12 · NEW-16 · NEW-20 (smoke panel ③) dẫn từ rủi ro hồi quy (3) của `dev_impact`; NEW-13 (preview + màn khách) dẫn từ RG-06 / OOS-06; NEW-9 · NEW-19 dẫn từ "độc lập trạng thái 決済連携" của `dev_impact` → đều không phải TC thừa.

---

## 7. TCs đề xuất bổ sung (3)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm 28, 37, 43, 48, 50) · `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 31) |
| Vùng regression phát hiện từ kho | `TC-LSN-374` (item tự thêm liên kết họ tên / email) → nguồn của G1 · `TC-LSN-372` / `TC-SLN-316` (item mặc định tắt / 任意 khi không dùng 決済) → nguồn của G2 |
| Conflict expected vs kho | Không (C1 ở §4 là của TC hiện có, không phải TC đề xuất) |
| GAP dùng lại TC kho (không viết mới) | Không — kho chưa có TC nào kiểm banner (tính năng mới) |
| Căn cứ TC regression `R<x>` | Không có TC R — rủi ro hồi quy (1)(3) của `dev_impact` đã đủ TC |
| Xác nhận chống trùng | Đã đối chiếu 23 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng (NEW-10/21 dùng câu hỏi tự thêm không liên kết; NEW-6 sửa item mặc định, không tạo item giống mặc định) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATAID001-01 | UI | DATA-ID-001 | 予約時のお客様への質問項目 | Abnormal | auto | Tất cả | Lesson: câu hỏi tự thêm trùng nội dung và liên kết friend info họ tên / email với item mặc định — KHÔNG hiện banner lưu ý thanh toán | - Đăng nhập admin, chọn bot cần kiểm tra<br>- Lịch 「レッスン予約」 riêng của TC: TC40890-lesson-dup-<ngày giờ><br>- Tab 「決済連携」 = 「利用なし」<br>- Khối ② đang có đủ 2 item mặc định 「お名前を入力してください」 và 「メールアドレスを入力してください」 | 1. Mở 予約管理 › lịch TC40890-lesson-dup › tab 「予約設定」 › 「お客様への質問項目」<br>2. Ở khối ①, bấm 「短文回答」 thêm câu hỏi Q1: 質問内容 = お名前を入力してください, liên kết friend info = họ tên (system name). Click ra ngoài để lưu<br>3. Thêm câu hỏi Q2 loại 「短文回答」: 質問内容 = メールアドレスを入力してください, 入力内容 = メールアドレス, liên kết friend info = メールアドレス. Click ra ngoài để lưu<br>4. Chọn Q1 ở khối ②, quan sát panel ③<br>5. Chọn Q2 ở khối ②, quan sát panel ③<br>6. Chọn item mặc định 「お名前を入力してください」, quan sát panel ③<br>7. Tải lại trang, lặp lại bước 4 → 6 | Q1: 短文回答 · 質問内容 お名前を入力してください · liên kết họ tên<br>Q2: 短文回答 · 質問内容 メールアドレスを入力してください · 入力内容 メールアドレス · liên kết メールアドレス | - Bước 4, 5: panel ③ của Q1 và Q2 KHÔNG có banner 決済機能を利用の場合…; panel ③ có link 「この項目を削除」<br>- Bước 6: item mặc định hiện banner ngay dưới thanh 「③ 編集」, không có link 「この項目を削除」<br>- Bước 7: sau tải lại, kết quả giống hệt bước 4 → 6 |  | Lấp G1 + Q5 · Đánh giá spec: Spec ghi rõ (human chốt 2026-10-01: "2 item default loại メールアドレス và お名前. Các item khác thì không add") · dẫn từ kho TC-LSN-374 · Evidence: ảnh chụp panel ③ của Q1, Q2 và item mặc định · Dọn: xóa Q1, Q2 sau khi chạy |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | 予約時のお客様への質問項目 | Abnormal | auto | Tất cả | Salon: câu hỏi tự thêm trùng nội dung và liên kết friend info họ tên / email với item mặc định — KHÔNG hiện banner lưu ý thanh toán | - Đăng nhập admin, chọn bot cần kiểm tra<br>- Lịch 「サロン・面談予約」 riêng của TC: TC40890-salon-dup-<ngày giờ><br>- Tab 「決済連携」 = 「利用なし」<br>- Khối ② đang có đủ 2 item mặc định 「お名前を入力してください」 và 「メールアドレスを入力してください」 | 1. Mở 予約管理 › lịch TC40890-salon-dup › tab 「予約設定」 › 「お客様への質問項目」<br>2. Ở khối ①, bấm 「短文回答」 thêm câu hỏi Q1: 質問内容 = お名前を入力してください, liên kết friend info = họ tên (system name). Click ra ngoài để lưu<br>3. Thêm câu hỏi Q2 loại 「短文回答」: 質問内容 = メールアドレスを入力してください, 入力内容 = メールアドレス, liên kết friend info = メールアドレス. Click ra ngoài để lưu<br>4. Chọn Q1, quan sát panel ③<br>5. Chọn Q2, quan sát panel ③<br>6. Chọn item mặc định 「メールアドレスを入力してください」, quan sát panel ③<br>7. Tải lại trang, lặp lại bước 4 → 6 | Q1: 短文回答 · 質問内容 お名前を入力してください · liên kết họ tên<br>Q2: 短文回答 · 質問内容 メールアドレスを入力してください · 入力内容 メールアドレス · liên kết メールアドレス | - Bước 4, 5: panel ③ của Q1 và Q2 KHÔNG có banner 決済機能を利用の場合…; panel ③ có link 「この項目を削除」<br>- Bước 6: item mặc định hiện banner ngay dưới thanh 「③ 編集」, không có link 「この項目を削除」<br>- Bước 7: sau tải lại, kết quả giống hệt bước 4 → 6 |  | Lấp G1 + Q3 · Đánh giá spec: Spec ghi rõ (human chốt 2026-10-01) · Salon có file setting_form riêng nên không suy kết quả từ Lesson · Evidence: ảnh chụp panel ③ của Q1, Q2 và item mặc định · Dọn: xóa Q1, Q2 sau khi chạy |
| TC-DATAID001-02 | UI | DATA-ID-001 | 予約時のお客様への質問項目 | Boundary | auto | Tất cả | Item mặc định họ tên / email đang tắt hiển thị và 任意 — banner lưu ý thanh toán VẪN hiện | - Đăng nhập admin, chọn bot cần kiểm tra<br>- Lịch 「レッスン予約」 riêng của TC: TC40890-lesson-off-<ngày giờ><br>- Tab 「決済連携」 = 「利用なし」 (chỉ khi không dùng thanh toán mới tắt / đổi 任意 được item mặc định) | 1. Mở tab 「予約設定」 › 「お客様への質問項目」, chọn item 「お名前を入力してください」<br>2. Đặt 「表示設定」 = 非表示, 「回答設定」 = 任意, click ra ngoài để lưu<br>3. Quan sát panel ③<br>4. Chọn item 「メールアドレスを入力してください」, đặt 「回答設定」 = 任意 (giữ 表示), lưu, quan sát panel ③<br>5. Tải lại trang, chọn lần lượt 2 item mặc định, quan sát panel ③<br>6. Trả 2 item về 表示 + 必須 | Item họ tên: 非表示 + 任意<br>Item email: 表示 + 任意 | - Bước 3, 4, 5: banner hiện đủ, đúng vị trí (dưới 「③ 編集」, trên 「質問内容」) và đúng nguyên văn ở cả 2 item mặc định — không phụ thuộc 表示設定 / 回答設定 của item<br>- Thao tác đổi 表示設定 / 回答設定 vẫn lưu thành công như trước khi có banner |  | Lấp G2 · Đánh giá spec: Spec ghi rõ (human chốt 2026-10-01: đối tượng add là 2 item mặc định, không kèm điều kiện trạng thái) · dẫn từ kho TC-LSN-372 / TC-SLN-316 · Evidence: ảnh chụp panel ③ 2 item ở trạng thái 非表示 / 任意 · Salon dùng chung partial banner — chạy thêm trên lịch Salon nếu còn thời gian |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/lesson-booking/feature-spec.md` (SCR-LSN-16, nhóm BR-50) + `spec-features/admin/salon-booking/feature-spec.md` (màn 質問項目) | Thêm business rule mới: panel ③「編集」 hiện banner 「決済機能を利用の場合「お名前」「メールアドレス」項目は決済システム側への連携のため必須回答となります。」 chỉ khi item đang chọn là 1 trong 2 item mặc định họ tên / email; mọi item khác không hiện; không phụ thuộc trạng thái 決済連携 | Spec change #40890 (human chốt 2026-10-01) — spec-features chưa có | PM |
| 2 | Kho `TC-LSN-355` (FA-019, nhóm 28) | ✅ Đã xong 2026-10-01 — Leader chốt chặn nhập ký tự thứ 51 (dán thì cắt còn 50); kho `TC-LSN-355` đã sửa theo | §4 C1 `CONF-KHO` | Leader |
| 3 | Lesson spec RA-06 + điều kiện hiển thị banner | Dev xác nhận: banner nhận diện item mặc định theo cờ "không cho xoá" (`can_delete = 0`) hay theo friend info họ tên / email (`-1` / `-3`)? Có dữ liệu lịch cũ / do mass-assignment `updateSettingForm` mà item họ tên / email có `can_delete ≠ 0` không? Nếu có → banner không hiện ở item mặc định đó, trái spec human chốt | §2 Q4 | Dev |
