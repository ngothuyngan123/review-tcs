# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm; bảng coverage 2 chiều và bảng quan điểm đã chạy nội bộ.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #327 (ticket 41329, round 1, branch `ai_fixbug_41329`) |
| Tổng số TC review | 20 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 4/4 mục có TC — **ĐỦ** (`BUG` · `F1` · `F2` · `T1`; `D1` = "không có data" nên không tính) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (1 file, 1+/1−) | 7/7 điểm có TC — **ĐỦ** |

**Kết luận**: 11/11 vùng ảnh hưởng đủ TC · 0 GAP · 0 RISK.

> Đối chiếu nội bộ (không liệt kê chi tiết): reset cờ trong `callAjaxCreateBooking` → NEW-2 · NEW-5 · NEW-12 · NEW-20; tự tính giờ kết thúc khi bấm ô trống / đổi giờ bắt đầu / đổi khóa ở lần mở thứ 2 trở đi → NEW-3 · NEW-4 · NEW-6 · NEW-7; người dùng chủ động bỏ chọn ô rồi lần sau ô trở về mặc định → NEW-8; smoke màn 予約管理 → NEW-17; dữ liệu lưu đúng → NEW-2 · NEW-3 · NEW-14. Tất cả `pass` trên staging.
> Sibling field dùng chung khối reset (không nằm trong diff) → đề xuất ở §7 dạng `R1`, không tính GAP.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 12 quan điểm Trigger khớp task · 8 chưa cover đủ (gom thành 6 dòng).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `REG-SHARED-001` | Cao | RISK — mới smoke màn 予約管理 (NEW-17). Dev **tự ghi nhận** màn Đặt lịch bài học (Lesson, FA-019) lệch cùng kiểu ở lựa chọn 「予約時アクションの実行」 nhưng không sửa; checklist ghi rõ cặp Salon / Lesson / Booking Event là điểm hay lặp lại. 0 TC nào kiểm Lesson | `[BLOCKER]` |
| Q2 | `DATA-CACHE-001` + `DEPLOY-LIVE-001` | Cao | GAP — release sửa JS, không bật maintain: chưa có TC "tab mở sẵn từ trước khi deploy, không tải lại, bấm 登録する" | `[BLOCKER]` |
| Q3 | `DEPLOY-ASSET-001` | Cao | RISK — TC duy nhất (NEW-18) đang `skip`, chưa có kết luận. Chỉ có Normal; Abnormal/Boundary không có ý nghĩa với cache-bust (được miễn RULE-01) | `[MAJOR]` |
| Q4 | `FUNC-DATE-001` + `FUNC-003` (nâng Cao vì là field ngày giờ) | Cao | RISK — Boundary duy nhất (NEW-13, qua nửa đêm) đang **mâu thuẫn kho** (C1 ở §4) nên mất chuẩn đánh giá; Abnormal chỉ có NEW-10 (tích lại ô khi thiếu ngày/giờ) | `[MAJOR]` |
| Q5 | `SYNC-APP-001` | Trung bình | RISK — app quản trị di động có luồng admin đặt lịch (kho TC-SLN-477). Chưa rõ app có ô 「コース所要時間を基準に終了時間を設定」 và có dính cùng lỗi reset hay không. Bản fix chỉ sửa JS web | `[MAJOR]` |
| Q6 | `FUNC-SEQ-001` | Trung bình | RISK — NEW-2 / NEW-3 / NEW-4 / NEW-5 / NEW-12 mỗi TC chỉ ở **1 chế độ xem** từ đầu đến cuối; chưa TC nào đổi chế độ xem 「日」→「週」→「月」 giữa các lần đặt, hoặc sang tab khác của màn rồi quay lại 「予約カレンダー」 mà không tải lại trang (bổ sung theo yêu cầu Leader 2026-09-24) | `[MAJOR]` |

- Đã cover đủ (không ghi dòng): `FUNC-001` (Normal NEW-1/NEW-2 · Abnormal NEW-8 · Boundary NEW-12 — Abnormal và Boundary nằm dưới mã khác nhưng có nội dung thật) · `UI-FIELD-001` · `UI-001` · `OUT-TRUTH-001`.
- Đã loại khỏi phạm vi (kèm lý do): `DATA-DB-001` (create = INSERT, fix không đổi dữ liệu) · `STATE-DEP-001` / `MSG-USER-001` (payload gửi lên không đổi; nếu 「予約時アクションの実行」 bị reset lệch thì `R1` đã bắt) · `INTG-CAL-001` / `INTG-SHEET-001` / `JOB-001` (layer downstream không bị chạm code) · `CONC-001` (nút 登録する không đổi; kho TC-SLN-116) · `COMPAT-LEGACY-001` (form cũ chỉ khác phần câu hỏi, không chạm ô tự tính) · `FUNC-002` (validate form không đổi; kho TC-SLN-101→104).

---

## 3. TC trùng lặp nội dung

Đã rà 20 TC, không phát hiện trùng lặp.

- NEW-2 (Normal, 2 lượt) và NEW-12 (Boundary, 5 lượt) cùng luồng nhưng khác `Loại case` → không trùng đủ 4 yếu tố.
- NEW-2 / NEW-5 / NEW-20 khác đường mở modal (ô lưới ↔ nút 「予約追加」 ↔ đan xen).
- NEW-14 là NEW-2 cộng thêm bước đối chiếu dữ liệu nhưng không kiểm trạng thái ô → không phải tập con.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-13 (+ tiền đề NEW-19, ghi chú NEW-3) | Admin thêm đặt lịch có giờ kết thúc ≤ giờ bắt đầu theo đồng hồ (23:30 → 00:30; 14:00 → 11:00) | NEW-13: **lưu thành đơn qua đêm**, kết thúc 00:30 hôm sau. NEW-19: đơn 14:00→11:00 dựng được bằng UI (bỏ chọn ô + nhập tay). NEW-3: "modal không có bước chặn giờ kết thúc nhỏ hơn giờ bắt đầu" | kho **TC-SLN-104** B5/B6 "Validate ngày giờ của booking thủ công": giờ kết thúc < hoặc = giờ bắt đầu → lỗi 「開始時間は終了時間よりも前の時間を設定して下さい」 | TC Studio sai (thực tế modal chặn) / kho cũ hơn code hiện tại (đã cho phép đơn qua đêm). Lưu ý: NEW-13 được đánh `pass` trên staging ngày 2026-09-24 | `[MAJOR]` | Dev / Leader |
| C2 | `CONF-KHO` | NEW-9 | Admin thêm đặt lịch vào khung 10:00-11:00 của nhân viên A đã có đặt lịch | Lỗi 「指定の時間帯はブロックされています。予約時間を変更してください。」, modal không đóng, không tạo đặt lịch | kho **TC-SLN-115** "Admin book KHÔNG bị chặn bởi mọi ràng buộc đặt lịch" (kể cả nhân viên / lịch đã đạt 受付上限) — kho **MT-13** (CAO, chờ quyết định) | TC Studio sai / kho chưa phân biệt "trùng khung đã có booking" với "đạt 受付上限". Lưu ý: NEW-9 được đánh `pass` trên staging | `[MAJOR]` | Leader |

**Đã rà**: 20 TC × `spec-features/admin/salon-booking/feature-spec.md` §2.2 + `ui/ui-spec.md` (modal 「予約追加」) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 11 "Admin thêm booking thủ công", TC-SLN-101→118). Không có `CONF-TC`; không có `CONF-SPEC` với hành vi chính (spec ghi checkbox `default checked`, khớp bản fix). Nhiều TC trích `BR-04` / `BR-05` nhưng hai BR này trong spec là rule khác (xem I3 ở §5, không tính là mâu thuẫn).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — Lesson (FA-019) | Journal Dev #137865 mục 2 ghi nhận màn Đặt lịch bài học **có cùng lỗi reset lệch mặc định** ở 「予約時アクションの実行」, nhưng chỉ ghi nhận, **không có ticket**. Nếu sau lượt thêm đầu tiên giá trị bị đổi âm thầm, lượt sau có thể chạy/không chạy action gửi tin cho khách ngoài ý admin | Leader raise ticket riêng cho Lesson (và nhờ Dev rà luôn Event booking FA-021); chạy TC `TC-REGSHARED001-01/02` ở §7 làm bằng chứng. Không chặn ticket 41329 |
| I2 | `[MAJOR]` | NEW-11 | `Kết quả mong đợi` không đo được: bước 4 ghi "ghi nhận trạng thái… báo leader/PO", người chạy "không tự kết luận đạt/không đạt", nhưng TC lại được đánh `pass` | Leader chốt hành vi mong đợi khi **đóng modal không lưu rồi mở lại** (xem §8 #3), rồi sửa expected NEW-11 trên Studio (`testcase_update`) thành giá trị cụ thể |
| I3 | `[MINOR]` | NEW-3 · NEW-9 · NEW-13 · NEW-14 | `spec_ids` trích `BR-05` ("quy tắc đơn qua đêm") và `BR-04` ("khung bị chặn"), nhưng trong `feature-spec.md` BR-04 là khởi tạo settings, BR-05 là điều kiện bật thanh toán. Spec không có rule đơn qua đêm / chặn khung cho admin booking | Sửa `spec_ids` trên Studio; rule thật đưa vào §8 #1-#2 |
| I4 | `[MINOR]` | NEW-14 | `env_scope = local` (ghi chú: "dev/staging/production không cho truy vấn trực tiếp") nhưng `last_exec` ghi `pass` trên **staging** | Hỏi QA quyend đã đối chiếu dữ liệu bằng cách nào trên staging; sửa `env_scope` hoặc ghi evidence cho khớp |
| I5 | `[MINOR]` | NEW-3 · NEW-6 | Gắn mã `STATE-DEP-001` (hành động phụ thuộc đã lên lịch: remind/gửi tin) nhưng nội dung là field phụ thuộc lựa chọn (giờ kết thúc theo khóa / khung) → đúng ra là `UI-FIELD-001` | Sửa mã quan điểm trên Studio |
| I6 | `[MINOR]` | NEW-15 · NEW-16 · NEW-19 | 3 TC `skip` trên staging, không ghi lý do (NEW-18 đã xử lý ở Q3) | Ghi lý do skip; NEW-19 phụ thuộc chốt C1 (§4) mới dựng được đơn "dấu vết lỗi cũ" |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 20 TC — không có TC nào ngoài phạm vi task.

- NEW-15 / NEW-16 (API EP-A57) test layer backend không bị chạm code, nhưng Studio `dev_impact` nêu thẳng "create-booking EP-A57 nhận dữ liệu không đổi" là rủi ro hồi quy phải xác nhận → theo gate thì **không** tính là TC thừa. Cả 2 đang `skip`; Leader có thể cân nhắc chuyển sang bộ regression chung của kho.

---

## 7. TCs đề xuất bổ sung (5)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 11, 52) · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (grep 予約時アクション) |
| Vùng regression phát hiện từ kho | TC-SLN-111 / TC-SLN-112 (option 「すでに情報が登録されている場合、自動入力する」 luôn tick sẵn mỗi lần mở — Support #28264) · TC-SLN-477 (app mobile admin đặt lịch) |
| Conflict expected vs kho | NEW-13 / NEW-19 vs TC-SLN-104 → C1; NEW-9 vs TC-SLN-115 → C2 (đã đưa §4 + §8). TC đề xuất không tạo conflict mới |
| GAP dùng lại TC kho (không viết mới) | **Q4** → chốt C1 xong thì chạy lại **TC-SLN-104** "Validate ngày giờ của booking thủ công" (B5/B6) làm Abnormal cho `FUNC-DATE-001` · **Q3** → không viết mới, **chạy NEW-18** trên staging ngay sau lần deploy branch fix (và production khi release) · **Q5** → không viết TC: chưa xác minh được app có ô tương đương hay không, không bịa label; Dev xác nhận ở §8 #4 |
| Căn cứ TC regression `R<x>` | R1: bản fix sửa **đúng khối reset form** trong `callAjaxCreateBooking` (journal #137865 mục 3); cùng khối đó còn reset 2 field khác mà spec (`ui-spec.md` modal 「予約追加」) quy định mặc định; Dev đã thấy kiểu lệch này ở Lesson; kho TC-SLN-112 chỉ kiểm lúc mở / đóng modal, chưa kiểm **sau khi tạo thành công** |
| Xác nhận chống trùng | Đã đối chiếu 20 TC ở BƯỚC 0 + kho FA-020 / FA-019 — **không TC đề xuất nào trùng** (NEW-5 chỉ kiểm khách hàng + khóa trống, không kiểm 2 option còn lại; TC-FUNCSEQ001-01 khác NEW-2/3/4/12 ở chỗ đổi chế độ xem + chuyển tab giữa các lượt) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Admin thêm booking thủ công | Normal | auto | Tất cả | Salon — sau khi thêm đặt lịch thành công, cả 3 lựa chọn của modal 「予約追加」 (tự tính giờ kết thúc · 自動入力 · 予約時アクションの実行) trở về mặc định | - Đăng nhập admin, chọn đúng bot test (KHÔNG dùng tài khoản khách bulkclinic@gmail.com)<br>- Lịch salon test loại スタッフ, có khóa 60 phút, nhân viên A có ca phủ 10:00 và 14:00 hôm nay<br>- Lịch **chưa** cài tin nhắn / action khi đặt lịch (tránh gửi tin ra ngoài)<br>- Khách F1 là bạn bè đang hiển thị trên エルメ<br>- Trang vừa tải lại | 1. Tab 「予約カレンダー」, chế độ 「日」 → bấm ô trống 10:00 của nhân viên A<br>2. Ghi lại trạng thái lần mở đầu: ô 「コース所要時間を基準に終了時間を設定」, ô 「すでに情報が登録されている場合、自動入力する」, radio 「予約時アクションの実行」<br>3. Chọn F1 + khóa 60 phút; **đổi cả 3**: bỏ chọn ô tự tính (nhập giờ kết thúc 11:00), bỏ tick 自動入力, chọn 「実行しない」 → 「登録する」<br>4. Không tải lại trang: bấm ô trống 14:00 của nhân viên A<br>5. Quan sát lại 3 lựa chọn | Lượt 1: F1 · 10:00-11:00 · khóa 60 phút · 3 lựa chọn đổi khỏi mặc định<br>Lượt 2: mở modal ở khung 14:00 | - Bước 2: tự tính = được chọn · 自動入力 = được tick · 「実行する」 được chọn (đúng mặc định trong ui-spec)<br>- Bước 3: đặt lịch 10:00-11:00 tạo thành công, modal đóng<br>- Bước 5: **cả 3** lựa chọn giống hệt bước 2 — tự tính được chọn (giờ 14:00-15:00, ô giờ kết thúc bị khóa), 自動入力 được tick, 「実行する」 được chọn; không lựa chọn nào giữ giá trị của lượt 1 |  | Lấp R1 · regression · căn cứ: cùng khối reset `callAjaxCreateBooking` (journal #137865 mục 3) + Dev ghi nhận lệch ở Lesson + kho TC-SLN-112 · Đánh giá spec: Spec ghi rõ (ui-spec.md modal 「予約追加」) · Evidence: screenshot modal bước 2 và bước 5 |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Lesson (FA-019) — Admin thêm booking thủ công | Normal | auto | Tất cả | Lesson — mở modal thêm đặt chỗ thủ công lần 2 sau khi tạo thành công, 「予約時アクションの実行」 và 自動入力 giữ đúng trạng thái như lần mở đầu | - Đăng nhập admin bot test<br>- Lịch bài học (レッスン予約) test đang ON, có khóa và ≥ 2 khung tiếp nhận còn chỗ hôm nay<br>- Lịch **chưa** cài tin nhắn / action khi đặt chỗ<br>- Khách F1, F2 là bạn bè đang hiển thị trên エルメ<br>- Trang vừa tải lại | 1. Tab 「予約カレンダー」 → mở modal thêm đặt chỗ thủ công (header 「定員：…」) ở khung thứ nhất<br>2. Ghi lại trạng thái lần mở đầu của 「予約時アクションの実行」 và ô 「すでに情報が登録されている場合、自動入力する」<br>3. Chọn F1, **giữ nguyên** các lựa chọn → 「登録する」<br>4. Không tải lại trang: mở modal thêm đặt chỗ ở khung thứ hai<br>5. Quan sát 2 lựa chọn | Lượt 1: F1 · khung 1 · giữ mặc định<br>Lượt 2: khung 2 | - Lượt 1 tạo đặt chỗ thành công<br>- Bước 5: 「予約時アクションの実行」 và 自動入力 **giống hệt** bước 2 | | Lấp Q1 · Dev tự ghi nhận Lesson lệch ở 「予約時アクションの実行」 (journal #137865 mục 2) → **dự kiến Không đạt**; fail thì raise ticket riêng (I1), không chặn ticket 41329 · Đánh giá spec: Spec không ghi (lesson ui-spec không ghi giá trị mặc định) — chuẩn = trạng thái lần mở đầu · Evidence: screenshot bước 2 và bước 5 |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Lesson (FA-019) — Admin thêm booking thủ công | Abnormal | auto | Tất cả | Lesson — chọn 「実行しない」 ở lượt 1 thì lượt thêm kế tiếp không ghi nhớ lựa chọn đó | Như TC-REGSHARED001-01 | 1. Mở modal thêm đặt chỗ ở khung thứ nhất, ghi lại trạng thái mặc định của 「予約時アクションの実行」<br>2. Chọn F1, chọn 「実行しない」 → 「登録する」<br>3. Không tải lại trang: mở modal ở khung thứ hai<br>4. Quan sát 「予約時アクションの実行」 | Lượt 1: F1 · 「実行しない」<br>Lượt 2: khung 2 | - Bước 4: 「予約時アクションの実行」 trở về đúng trạng thái đã ghi ở bước 1, không giữ 「実行しない」 của lượt 1 |  | Lấp Q1 · Boundary không áp dụng (lựa chọn chỉ có 2 giá trị) · regression · Đánh giá spec: Spec không ghi · Evidence: screenshot bước 1 và bước 4 |
| TC-DEPLOYLIVE001-01 | UI | DEPLOY-LIVE-001 | Admin thêm booking thủ công | Normal | auto | Tất cả | Salon — tab 「予約カレンダー」 mở sẵn từ trước khi deploy, không tải lại, vẫn thêm đặt lịch thành công và dữ liệu đúng | - Lịch salon test như TC-FUNC001-01<br>- Phối hợp với người deploy: biết thời điểm branch `ai_fixbug_41329` lên môi trường đang test | 1. **Trước** khi deploy: mở màn lịch salon → Tab 「予約カレンダー」, chế độ 「日」<br>2. Deploy bản fix; **không tải lại** tab<br>3. Bấm ô trống 10:00 → chọn F1 + khóa 60 phút → 「登録する」<br>4. Không tải lại: bấm ô trống 14:00 → chọn F1 + khóa 60 phút → 「登録する」<br>5. Tải lại trang bình thường (F5, không Ctrl+F5) → mở chi tiết 2 đặt lịch | Lượt 1: 10:00 · khóa 60 phút<br>Lượt 2: 14:00 · khóa 60 phút | - Bước 3-4: cả 2 lượt tạo thành công, không lỗi hệ thống (không 500, không thông báo lỗi lạ), modal đóng bình thường<br>- Bước 5: đặt lịch lưu đúng giờ đã thấy trên modal lúc bấm 「登録する」 (tab còn chạy JS cũ nên lượt 2 có thể còn hiện tượng cũ; chỉ cần không lỗi và không lưu nửa vời) |  | Lấp Q2 (DATA-CACHE-001 kiểm tra (1) + DEPLOY-LIVE-001) · payload EP-A57 không đổi theo Studio dev_impact → kỳ vọng tương thích · cần phối hợp thời điểm deploy · Đánh giá spec: Spec không ghi · Evidence: screenshot tab cũ + chi tiết 2 đặt lịch sau F5 |
| TC-FUNCSEQ001-01 | UI | FUNC-SEQ-001 | Admin thêm booking thủ công | Normal | auto | Tất cả | Salon — đặt lịch liên tiếp qua các chế độ xem 「日」→「週」→「月」, chuyển tab rồi tải lại trang: ô 「コース所要時間を基準に終了時間を設定」 luôn được tích | - Đăng nhập admin, chọn đúng bot test (KHÔNG dùng tài khoản khách bulkclinic@gmail.com)<br>- Lịch salon test loại スタッフ, có khóa 60 phút đang hoạt động<br>- Nhân viên A có ca phủ 10:00 hôm nay, 14:00 của 1 ngày khác trong tuần, và còn ngày trống trong tháng<br>- Khách F1 là bạn bè đang hiển thị trên エルメ<br>- Đang ở Tab 「予約カレンダー」, trang vừa tải lại | 1. Chế độ 「日」, hôm nay → bấm ô trống 10:00 của nhân viên A → quan sát ô tích → chọn F1 + khóa 60 phút → 「登録する」<br>2. **Không tải lại**: chuyển sang 「週」 → bấm ô trống 14:00 của ngày khác → quan sát ô tích, ô giờ kết thúc, cặp giờ → chọn F1 + khóa 60 phút → 「登録する」<br>3. **Không tải lại**: chuyển sang 「月」 → bấm 1 ngày còn trống → quan sát ô tích → sửa giờ bắt đầu thành 13:00 → quan sát giờ kết thúc → chọn F1 + khóa 60 phút → 「登録する」<br>4. **Không tải lại**: sang tab 「本日／新着の予約」, quay lại tab 「予約カレンダー」 → mở modal bằng nút 「予約追加」 → quan sát ô tích → đóng modal<br>5. Tải lại trang (F5 thường) → mở modal bằng nút 「予約追加」 → quan sát ô tích<br>6. Đối chiếu 3 đặt lịch vừa tạo trên lưới lịch | Lượt 1: 「日」 · hôm nay 10:00 · khóa 60 phút<br>Lượt 2: 「週」 · ngày khác 14:00 · khóa 60 phút<br>Lượt 3: 「月」 · 1 ngày trống · giờ bắt đầu 13:00 · khóa 60 phút | - Bước 1: ô được tích, giờ 10:00-11:00, ô giờ kết thúc bị khóa; tạo thành công<br>- Bước 2: ô **vẫn được tích**, ô giờ kết thúc bị khóa, giờ 14:00-15:00 (không giữ 11:00 của lượt trước); tạo thành công<br>- Bước 3: ô **vẫn được tích**; đổi giờ bắt đầu 13:00 thì giờ kết thúc tự đổi thành 14:00; tạo thành công<br>- Bước 4: sau khi chuyển tab và quay lại, ô **được tích**<br>- Bước 5: sau khi tải lại, ô **được tích**<br>- Bước 6: 3 đặt lịch hiển thị đúng khung 10:00-11:00 · 14:00-15:00 · 13:00-14:00, không đơn nào lệch giờ hay kéo sang ngày hôm sau |  | Lấp Q6 · bổ sung theo yêu cầu Leader 2026-09-24 (reload · chuyển tab · đặt ở tab ngày/tuần/tháng) · Đánh giá spec: Spec ghi rõ (ui-spec.md: checkbox default checked) · Evidence: screenshot modal ở bước 2, 3, 4, 5 + lưới lịch bước 6 |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `feature-spec.md` §2.2 "Luồng thêm đặt lịch thủ công" + kho TC-SLN-104 | Chốt: admin thêm đặt lịch với giờ kết thúc ≤ giờ bắt đầu (kể cả khi giờ tự tính vượt 24:00, VD 23:30 + 60 phút) là **báo lỗi** hay **lưu đơn qua đêm** (`end_date_booking` = hôm sau). Ghi thành BR mới, cập nhật TC bên sai | C1 `CONF-KHO` | Dev / Leader |
| 2 | `feature-spec.md` §2.2 + kho MT-13 / TC-SLN-115 | Chốt: admin thêm đặt lịch vào khung **đã có đặt lịch** của cùng nhân viên có bị chặn bằng 「指定の時間帯はブロックされています…」 không — phân biệt với trường hợp "đạt 受付上限" mà kho nói admin được bỏ qua | C2 `CONF-KHO` | Leader |
| 3 | `ui/ui-spec.md` modal 「予約追加」 | Ghi rõ trạng thái các lựa chọn khi mở lại modal: (a) sau khi tạo thành công — về mặc định (khớp bản fix #41329); (b) sau khi **đóng modal không lưu** — về mặc định hay giữ lựa chọn? (tiền lệ kho TC-SLN-112: 自動入力 luôn tick lại mỗi lần mở) | I2 (NEW-11) | Leader / PM |
| 4 | Spec app quản trị di động (FA-020 app) | Dev xác nhận app có ô "tự tính giờ kết thúc theo thời lượng khóa" không, và luồng reset sau khi tạo có cùng lỗi không; có thì tách ticket | Q5 | Dev |
