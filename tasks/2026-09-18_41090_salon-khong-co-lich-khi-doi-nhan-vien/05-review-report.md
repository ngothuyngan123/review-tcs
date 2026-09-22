# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #313 (ticket 41090, round 1, branch `ai_fixbug_41090`) |
| Tổng số TC review | 19 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 8/14 vùng ảnh hưởng đủ TC · 3 GAP · 3 RISK · 1 orphan

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F3 — `copyBookingStepTime` (lối vào 「同じ内容で予約」, 1 trong 5 điểm reset cờ) | `dev-impact` | `NEW-10` (skip) · `#18807` (skip, chế độ tuần) | RISK — lối vào duy nhất trong 5 lối được sửa mà **0 TC có kết quả**; chưa có chiều ngược (lịch sử đưa về NV không ca) | `[MAJOR]` |
| G2 | T1 — khách hoàn tất đặt lịch sau khi đổi NV (luồng chính tới output cuối) | `dev-impact` | `NEW-2` (skip) | RISK — TC duy nhất đi hết luồng đặt lịch + đối chiếu lịch sử khách / màn admin **chưa chạy** | `[MAJOR]` |
| G3 | `selectStaff` với lựa chọn 「指定しない」 sau NV không ca | `diff code` | không có | GAP — `dev_impact` yêu cầu test "đổi qua lại staff có/không ca"; 「指定しない」 cũng đi qua `selectStaff` nhưng dữ liệu là ca gộp của mọi NV (kho TC-SLN-432) — chưa TC nào chọn | `[MAJOR]` |
| G4 | Chuỗi NV không ca → NV không ca → NV có ca (rủi ro "chớp nhẹ" Dev tự nêu) | `diff code` | không có | GAP — Dev ghi: sau khi reset cờ, thông báo biến mất rồi hiện lại nếu NV mới cũng không ca. Nhánh "reset rồi phải bật lại" chỉ được test theo chiều có ca → không ca (`NEW-5`), chưa test không ca → không ca | `[MAJOR]` |
| G5 | NV chỉ có ca ở tháng xa (REQ-002 "kể cả tháng xa phải chuyển tháng mới thấy") qua đường đổi NV | `diff code` | `#18808` (pass — chỉ calendar khoá học, không đổi NV) | RISK — sau khi reset cờ, `initDataBooking` phải dò tháng và **không** bật lại cờ; chưa TC nào kết hợp đổi NV + ca ở tháng xa | `[MAJOR]` |
| G6 | F6 — chốt an toàn `initializeFullCalendar()` return sớm khi thiếu `#calendar` | `dev-impact` | không có | GAP — nhánh dự phòng, Dev nói không còn tới được vì cờ đã tắt trước → **không dựng được qua UI**, không đề xuất TC; Leader hỏi Dev xác nhận / review code | `[MINOR]` |
| G7 | `NEW-16`, `NEW-17` | `orphan` | — | Test nguồn tạo/xoá ca từ App Mobile — không thuộc BUG / F* / T* của fix (xem §4 I8) | `[MINOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 11 quan điểm Trigger khớp task · 5 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | RISK — TC mang mã này chỉ có `NEW-2` + `NEW-16`, **cả 2 skip** → 0 TC Đạt. TC reproduce chính `NEW-1` và đối chứng âm `NEW-5` mang mã lạ (`TOOL-*`) nên không tính. Kể cả sau khi đổi mã (§4 I9) vẫn thiếu **Boundary** (RULE-01) | `[MAJOR]` |
| Q2 | `REG-SHARED-001` | Cao | RISK — 8 TC Normal + 1 Boundary (`#18808`), **thiếu Abnormal** (RULE-01): chưa có lối vào nào được test theo chiều đưa về trạng thái không ca | `[MAJOR]` |
| Q3 | `CONC-003` | Trung bình | GAP — đổi NV sinh request mới; chưa TC nào kiểm response của NV trước về muộn có ghi đè màn NV đang chọn không. `NEW-3` ghi "vòng cuối thao tác nhanh" ở data nhưng note nói đã bỏ race, steps không có (§4 I5) | `[MAJOR]` |
| Q4 | `LIFF-ENTRY-001` (+ `UI-001` surface LIFF) | Cao | RISK — 18/19 TC chạy bằng trình duyệt tự động ở staging; bug do khách thật báo qua link trong LINE, **chưa TC nào mở trong in-app browser LINE trên máy thật**. Ma trận trạng thái kết bạn / link cũ-mới không liên quan fix → chỉ cần điểm vào in-app | `[MAJOR]` |
| Q5 | `DEPLOY-ASSET-001` | Cao | RISK — `NEW-14` Đạt ở `local`, chạy tay; TC đòi mốc trước/sau **release thật** nên local không chứng minh được. Không đề xuất TC mới — chạy lại `NEW-14` khi deploy staging và lúc release production | `[MAJOR]` |

- **Đã loại khỏi phạm vi**: rà `REG-SHARED-001` sang chức năng tương tự (Lesson FA-019 / Event FA-021). Kho `fa019` (TC-LSN-549…559) chỉ có logic tự nhảy tuần/tháng, không có màn thông báo 「予約できる日程がありません」 che khung lịch. Dev đã quét ngang: màn lesson / quản lý đặt chỗ giữ khung lịch trong trang. → Không đề xuất TC.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-1` (pass) | `NEW-18` (skip) | `DUP-SUBSET` | `TOOL-KNOW-002` · Normal · chọn NV không ca → quay lại chọn NV có ca ở 「月を先に表示」 · tiền đề tương đương (chỉ khác ca được tạo bằng App Mobile, nguồn tạo ca không nằm trong phạm vi fix) → expected giống nhau: thông báo biến mất, lịch tháng hiện ngày của NV có ca | `[MINOR]` |

- **Đã rà 19 TC**: chỉ có 1 nhóm trùng.
- **Gate đã chạy**: giả định xoá `NEW-18` → coverage §1 và quan điểm §2 vẫn giữ nguyên (`NEW-1` đã Đạt). Có.
- Không có `DUP-INFLATE` / `DUP-CONFLICT`.
- Xoá thật do human thực hiện qua `testcase_delete` trên Studio.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — run 1682 | Tỷ lệ Đạt **13/19 = 68%** (< 80%). 6 TC `skip`: `NEW-2`, `NEW-10`, `#18807`, `NEW-16`, `NEW-17`, `NEW-18`. Trong đó có TC duy nhất đi hết luồng đặt lịch và cả 2 TC của lối vào 「同じ内容で予約」 | Chạy lại ít nhất `NEW-2`, `NEW-10`. Nếu skip vì thiếu data (đơn cũ đã kết thúc/huỷ) thì dựng data rồi chạy tay |
| I2 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill bởi /new-task nhưng checkbox "Tester verify auto-fill chính xác" chưa tick. F1–F7 do /new-task tách từ mục 2+3 (Dev chỉ ghi 1 file) | Tester đọc lại Journal #137010, đối chiếu diff và tick |
| I3 | `[MAJOR]` | Spec | `spec-features/admin/salon-booking/` chỉ có field `is_show_month` ([db-mapping.md:73](../../spec-features/admin/salon-booking/db/db-mapping.md)). Không có rule phía LINE user: khi nào hiện 「予約できる日程がありません」, ngưỡng dò tháng, hành vi khi đổi NV. Expected của bộ TC đang dựa vào kho TC-SLN-435/436 + REQ Studio | Xem §6 |
| I4 | `[MAJOR]` | `NEW-14` | Đạt ở `local` (chạy tay 08:43) trong khi tiền đề đòi trình duyệt đã cache bản cũ **trước release** và kiểm tham số phiên bản **sau release** → local không có mốc release thật | Chạy lại khi deploy branch lên staging, và kiểm lại sau release production |
| I5 | `[MAJOR]` | `NEW-3` | 3 nơi nói khác nhau: data "5 vòng; vòng cuối thao tác nhanh không chờ nạp xong" · steps "lặp 2-3 lần" · note "bỏ kiểm tra race condition". Người chạy không biết phải chạy gì | Sửa data khớp steps (N vòng, chờ nạp xong mỗi vòng). Phần thao tác nhanh tách sang `TC-CONC003-01` (§5) |
| I6 | `[MAJOR]` | `#18807` | Tiền đề "Môi trường đã deploy commit `c9889e70a1`" là commit của #40378, không phải ticket này (`9cbd4412ee` / `ai_fixbug_41090`). TC chạy ở bảng tuần nên không đi qua lối vào lịch tháng được sửa | Đổi tiền đề sang branch/commit của #41090, ghi rõ đây là regression chế độ tuần |
| I7 | `[MINOR]` | `NEW-11` | Expected viết "Chuyển tháng và 「今日」 vẫn chạy đúng ở bước 5" nhưng bước 5 chỉ là "Kiểm tra lịch vẫn hiển thị đúng"; data ghi 3 vòng, steps ghi 2-3 lần | Thêm bước bấm mũi tên tháng + 「今日」 vào bước 5, thống nhất số vòng |
| I8 | `[MINOR]` | `NEW-16`, `NEW-17` | **[AP-5]** Test nguồn tạo/xoá ca trên App Mobile — tầng này không bị chạm code (fix chỉ sửa `booking.js` phía khách). App mobile có thêm/sửa/xoá ca thật (kho TC-SLN-476), nhưng đó là regression riêng của app. Ngoài ra `env_tag = local-only` mâu thuẫn với `env_scope = all` | Bỏ khỏi task #313, hoặc chuyển thành regression dẫn chiếu TC-SLN-476 |
| I9 | `[MINOR]` | `NEW-1`, `NEW-18`, `NEW-5`, `NEW-12` | Mã quan điểm Studio không có trong `checklist-lme.md` (`TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `RULE-TOOL-029`) → không map được coverage | `testcase_update`: `NEW-1` → `FUNC-001` · `NEW-5` → `FUNC-001` (Abnormal) · `NEW-12` → `REG-SHARED-001` · `NEW-18` xem §3 |
| I10 | `[NIT]` | Nguồn — evidence | Input thiếu: `testcase_list` không trả `Evidence thực tế` → chưa kiểm được RULE-02 cho 13 TC Đạt | Xem evidence của run 1682 bằng `task_get_report` trên Studio |

---

## 5. TCs đề xuất bổ sung (6)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 44–48 LINE user, 24 スタッフ自動割り当て, 52 App mobile) · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (TC-LSN-549…559) |
| Vùng regression phát hiện từ kho | TC-SLN-432 (danh sách staff có 「指定しない」) · TC-SLN-436 (logic chọn tháng hiển thị khi các tháng đầu không có ca) · TC-SLN-454 (「同じ内容で予約」) · TC-SLN-476 (App mobile thêm/sửa/xoá ca) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không. TC-SLN-436 chỉ mở tháng lần đầu, không qua đổi NV → dẫn chiếu ở `TC-FUNC001-01` |
| Xác nhận chống trùng | Đã đối chiếu 19 TC ở BƯỚC 0 + 2 file kho trên — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | LINE user — chọn slot | Boundary | manual | Tất cả | Lịch tháng: đổi từ NV không ca sang NV chỉ có ca ở tháng thứ ba → không hiện 予約できる日程がありません, mở đúng tháng có ca | - Calendar salon loại スタッフ C1 đang công khai, 「システムワード変更 / 表示設定」 chọn 「月を先に表示」<br>- NV-A: không có ca nào từ hôm nay trở đi<br>- NV-C: KHÔNG có ca ở tháng hiện tại và tháng kế tiếp, chỉ có ca còn trống ở tháng thứ ba<br>- Thời hạn nhận đặt lịch bao trọn tháng thứ ba<br>- LINE user U1 đã là bạn của OA | 1. U1 mở link đặt lịch C1, đi tới bước chọn nhân viên<br>2. Chọn NV-A, chờ nạp xong → màn hiện 「予約できる日程がありません」<br>3. Bấm 「戻る」, chọn NV-C, chờ nạp xong<br>4. Đọc tiêu đề tháng và các ngày được đánh dấu còn khung<br>5. Bấm 1 ngày còn khung | Tháng hiện tại = T. Ca NV-C: 2 ngày trong tháng T+2 (vd ngày 10 và 20, 10:00–12:00) | - Bước 3: thông báo 「予約できる日程がありません」 KHÔNG hiện; khối lịch tháng hiện đầy đủ (nút 「今日」, tab 「週」/「月」, bảng tháng)<br>- Bước 4: lịch mở thẳng tháng T+2, chỉ ngày 10 và 20 được đánh dấu còn khung<br>- Bước 5: sang bước chọn giờ, hiện khung 10:00–12:00 | | Lấp G5 · Lấp Q1 (Boundary) · Đánh giá spec: Spec không ghi — chuẩn lấy từ kho TC-SLN-436 B1 + REQ-002 Studio, cần Leader xác nhận · Evidence: screenshot bước 2, 3, 4 · regression — dẫn từ TC-SLN-436 |
| TC-FUNC001-02 | UI | FUNC-001 | LINE user — chọn slot | Abnormal | manual | Tất cả | Lịch tháng: chuỗi NV không ca → NV không ca khác → NV có ca, thông báo và lịch đổi đúng ở từng bước | - Calendar salon loại スタッフ C1, 「月を先に表示」<br>- NV-A và NV-C: đều không có ca nào từ hôm nay trở đi<br>- NV-B: có ca còn trống ở ≥ 3 ngày trong tháng hiện tại<br>- Mở console trình duyệt (PC) hoặc dùng máy test có xem được log | 1. Mở link đặt lịch C1, chọn NV-A, chờ nạp xong<br>2. Bấm 「戻る」, chọn NV-C, chờ nạp xong<br>3. Quan sát màn hình và console<br>4. Bấm 「戻る」, chọn NV-B, chờ nạp xong<br>5. Bấm 1 ngày còn khung | NV-A, NV-C: 0 ca. NV-B: ca ngày 5, 12, 20 tháng hiện tại | - Bước 1 và bước 3: hiện 「予約できる日程がありません」 kèm 「前ページに戻って再選択してください。」, KHÔNG còn khối lịch tháng. Trong lúc chờ nạp, thông báo có thể tắt rồi hiện lại (Dev đã nêu, chấp nhận), nhưng cuối cùng phải hiện thông báo, không đứng ở lịch tháng rỗng<br>- Console không có lỗi JavaScript ở bước 3<br>- Bước 4: thông báo biến mất, lịch tháng hiện đúng ngày 5, 12, 20<br>- Bước 5: sang bước chọn giờ | | Lấp G4 · Lấp Q1 (Abnormal bổ sung cho NEW-5) · Đánh giá spec: Spec không ghi — hành vi theo mô tả rủi ro của Dev (Journal #137010) · Evidence: video bước 1–5 + screenshot console |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | LINE user — chọn コース/スタッフ | Normal | manual | Tất cả | Lịch tháng: đổi từ NV không ca sang 「指定しない」 → hiện lịch theo ca gộp của các NV | - Calendar salon loại スタッフ C1, 「月を先に表示」, danh sách staff phía khách có nút 「指定しない」<br>- NV-A: không có ca nào từ hôm nay trở đi<br>- NV-B: có ca còn trống trong tháng hiện tại<br>- Không có NV nào khác đang bật | 1. Mở link đặt lịch C1, chọn NV-A → màn hiện 「予約できる日程がありません」<br>2. Bấm 「戻る」, chọn 「指定しない」, chờ nạp xong<br>3. Đọc các ngày được đánh dấu còn khung<br>4. Bấm 1 ngày còn khung | NV-B: ca ngày 8 và 15 tháng hiện tại, 13:00–15:00 | - Bước 2: thông báo 「予約できる日程がありません」 biến mất, khối lịch tháng hiện đầy đủ<br>- Bước 3: ngày 8 và 15 được đánh dấu còn khung (lấy từ ca của NV-B)<br>- Bước 4: sang bước chọn giờ, hiện khung 13:00–15:00 | | Lấp G3 · Đánh giá spec: Spec không ghi — nút 「指定しない」 theo kho TC-SLN-432 · Evidence: screenshot bước 1, 2, 3 · regression — dẫn từ TC-SLN-432 |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | LINE user — lịch sử & copy | Abnormal | manual | Tất cả | 「同じ内容で予約」 từ đơn cũ của NV nay không còn ca → hiện 予約できる日程がありません, không giữ lịch của NV trước | - Calendar salon loại スタッフ C1, 「月を先に表示」, có khoá K1<br>- NV-B: có ca còn trống trong tháng hiện tại<br>- NV-A: hiện KHÔNG có ca nào từ hôm nay trở đi<br>- LINE user U1 có 1 đơn cũ đã kết thúc (hoặc đã huỷ) với khoá K1 + NV-A, nên nút 「同じ内容で予約」 hiện ở màn chi tiết lịch sử | 1. U1 mở link đặt lịch C1, chọn K1 → NV-B, chờ lịch tháng của NV-B hiện đủ<br>2. Bấm menu góc trên → 「予約履歴一覧」<br>3. Mở đơn cũ của NV-A, bấm 「同じ内容で予約」, chờ nạp xong<br>4. Quan sát màn hình và console | Đơn cũ: K1 + NV-A, trạng thái đã kết thúc | - Bước 3: màn về bước chọn ngày giờ với K1 + NV-A được chọn sẵn và hiện 「予約できる日程がありません」<br>- KHÔNG còn hiện các ngày còn khung của NV-B từ bước 1<br>- Console không có lỗi JavaScript | | Lấp G1 · Lấp Q2 (Abnormal) · Đánh giá spec: Spec không ghi — luồng copy theo kho TC-SLN-454 · Evidence: screenshot bước 1 và 3 · Ngoài TC này vẫn phải chạy lại NEW-10 (chiều thuận) |
| TC-CONC003-01 | UI | CONC-003 | LINE user — chọn slot | Normal | manual | product | Mạng chậm: đổi NV không ca sang NV có ca khi request của NV trước chưa trả về → màn theo đúng NV chọn sau cùng | - Calendar salon loại スタッフ C1, 「月を先に表示」<br>- NV-A: không có ca nào từ hôm nay trở đi<br>- NV-B: có ca còn trống trong tháng hiện tại<br>- Mở link bằng Chrome PC, DevTools → Network → Throttling = Slow 3G | 1. Mở link đặt lịch C1 tới bước chọn nhân viên<br>2. Chọn NV-A, KHÔNG chờ nạp xong: bấm ngay 「戻る」 rồi chọn NV-B<br>3. Chờ toàn bộ request trong Network chạy xong<br>4. Ghi nhận màn hình<br>5. Làm lại theo chiều ngược: chọn NV-B, chưa nạp xong thì bấm 「戻る」 và chọn NV-A; chờ xong rồi ghi nhận | Throttling Slow 3G | - Bước 4: màn hiện lịch tháng của NV-B, KHÔNG bị response muộn của NV-A đổi thành 「予約できる日程がありません」<br>- Bước 5: màn hiện 「予約できる日程がありません」 của NV-A, KHÔNG hiện ngày của NV-B<br>- Không loading vô hạn, console không có lỗi JavaScript | | Lấp Q3 · race → Phạm vi ENV product (chỉ xem lịch, không tạo đơn) · Đánh giá spec: Spec không ghi · Evidence: video + screenshot Network thể hiện thứ tự response |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE user — mở link & entry | Normal | manual | Tất cả | Mở link đặt lịch trong app LINE trên máy thật (iOS + Android): đổi NV không ca sang NV có ca → lịch tháng hiện lại | - Calendar salon loại スタッフ C1, 「月を先に表示」, NV-A không ca, NV-B có ca còn trống trong tháng hiện tại<br>- Link đặt lịch C1 được gửi cho U1 bằng tin nhắn LINE<br>- U1 đã là bạn của OA; có 1 iPhone và 1 máy Android cài LINE bản mới nhất | 1. Trên iPhone, U1 bấm link trong tin nhắn LINE (mở in-app browser)<br>2. Chọn NV-A → ghi nhận thông báo<br>3. Bấm 「戻る」, chọn NV-B<br>4. Bấm 1 ngày còn khung<br>5. Lặp bước 1–4 trên máy Android | Máy thật iOS + Android, LINE bản mới nhất | - Bước 2: hiện 「予約できる日程がありません」<br>- Bước 3: thông báo biến mất, lịch tháng hiện đúng ngày có ca của NV-B, bố cục không vỡ<br>- Bước 4: sang bước chọn giờ<br>- Kết quả giống nhau trên iOS và Android | | Lấp Q4 · RULE-01: không đề xuất Abnormal/Boundary — ma trận trạng thái kết bạn / link cũ-mới không nằm trong phạm vi fix (chỉ sửa JS phía khách) · Đánh giá spec: Spec không ghi · Evidence: screen recording trên 2 máy |

- **G2**: không viết TC mới — chạy lại `NEW-2` (nội dung đủ 3 tầng: màn khách · lịch sử khách · màn admin).
- **G6**: không đề xuất TC — nhánh dự phòng không tái hiện được qua UI; Leader hỏi Dev hoặc review code.
- **G7**: không đề xuất TC — xem §4 I8.
- **Q5**: không viết TC mới — chạy lại `NEW-14` trên staging khi deploy và sau release production (§4 I4).

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/salon-booking/feature-spec.md` — luồng LINE user (bước chọn ngày giờ) | Bổ sung rule: (a) 「月を先に表示」/「週を先に表示」 (`is_show_month`) quyết định chế độ mở ban đầu; (b) điều kiện hiện 「予約できる日程がありません」 (không còn ca từ hôm nay trở đi, ngưỡng dò tuần/tháng); (c) đổi NV / khoá học / tab / 「同じ内容で予約」 phải tính lại trạng thái theo lựa chọn mới | Spec thiếu, expected đang dựa kho TC-SLN-435/436 + REQ-002 Studio | Dev / Leader |
