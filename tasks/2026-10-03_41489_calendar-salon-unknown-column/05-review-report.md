# 05 — Review Report

> Draft cho Leader verify. Ticket #41489 — fix whitelist cột khi lưu câu hỏi form đặt lịch Salon (`update-setting-form`).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #353 (round 1, branch `ai_fixbug_41489`) |
| Tổng số TC review | 16 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời:**

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 5/7 mục đủ TC (`BUG`, `T1` mới ở mức RISK) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (2 file, +41/-1) | 7/9 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 12/16 vùng ảnh hưởng đủ TC · 2 GAP · 2 RISK

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — luồng UI thật sinh ra payload có `friend_information_setting` trên production | `dev-impact` | `NEW-1` (UI), `NEW-10` (API) | **RISK** — Dev mục 1 nói *"payload của màn này kèm khoá phụ"*, nhưng note `NEW-1`/`NEW-10` nói *"màn hình hiện tại không chắc gửi field này"* ⇒ lỗi chỉ tái hiện được bằng gọi API tay, **chưa xác định thao tác UI nào của khách sinh ra lỗi**. `NEW-1` chưa thử `表示方法` và tuỳ chọn tải sẵn câu trả lời friend info (`enable_load_friend_information`) trên câu `link_friend_information=3` — cả 2 field có trong payload exception. Chạy 100% local. | `[MAJOR]` |
| G2 | `T1` — câu hỏi sau khi sửa được dùng ở **form đặt lịch phía LINE user (LIFF)** | `dev-impact` | `NEW-1`…`NEW-8` | **RISK — RULE-06**: mọi TC dừng ở màn admin + DB. Câu hỏi là input của form LIFF và của việc ghi câu trả lời vào friend info → field hợp lệ bị lọc mất (vd `enable_load_friend_information`, `options_information_friend`) chỉ lộ ra ở output cuối. | `[MAJOR]` |
| G3 | Cột `can_delete` / `order` vẫn nằm trong `UPDATABLE_COLUMNS` — client vẫn sửa được qua API | `diff code` | không có (`NEW-12` chỉ test `calendar_id`/`bot_id`/`deleted_at`/`created_at`) | **GAP** — fix chốt quy tắc *"client không được đổi cột hệ thống"* nhưng Studio `dev_impact` ghi *"còn mở: can_delete/order vẫn client sửa được"*. Gửi `can_delete=1` cho câu mặc định (名前 `-1` / メール `-3`) → có thể xoá được câu bắt buộc khi đang bật 決済 (BR-05). Câu 5 BƯỚC 2: quy tắc mới chưa áp cho nhánh này. | `[MAJOR]` |
| G4 | FE vẫn "nuốt" lỗi khi lưu thất bại (`updateFormQuestion` chỉ ghi console) | `diff code` | không có | **GAP** — đây là nửa còn lại của triệu chứng khách gặp (*"bấm lưu không được mà không thấy lỗi, tưởng đã lưu"*). Fix chỉ chặn 1 nguyên nhân 500; mọi lỗi lưu khác (419 hết session, mất mạng, 5xx khác) vẫn false success. Studio `dev_impact` ghi *"còn mở: FE vẫn nuốt lỗi 500"*. | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp task · 9 chưa cover đủ — trong đó **3 GAP thật cần TC mới** (Q1–Q3), 4 dòng còn lại (Q4–Q7) chỉ cần **đổi mã quan điểm / ghi lý do RULE-01**, không cần TC mới.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-DB-001` | Cao | **GAP** — task có UPDATE nhưng không TC nào kiểm `WHERE` scope trên 2 tài khoản: gửi `id` câu hỏi của **bot B** (hoặc của calendar khác cùng bot) vào endpoint của calendar bot A. `NEW-12` chỉ đổi `calendar_id`/`bot_id` trong body, không đổi `id` mục tiêu. Có Normal (`NEW-2`), thiếu Abnormal. | `[BLOCKER]` |
| Q2 | `LIFF-ENTRY-001` + `DATA-001` | Cao | **GAP** — 0 TC đi tới form đặt lịch phía LINE user sau khi sửa câu hỏi (cùng nội dung G2). | `[BLOCKER]` |
| Q3 | `OUT-TRUTH-001` + `UI-003` (→ Cao: rủi ro false success) | Cao | **GAP** — 0 TC kiểm "lưu thất bại thì UI phải báo lỗi" (cùng nội dung G4). | `[BLOCKER]` |
| Q4 | `FUNC-001` | Cao | **RISK — RULE-01**: chỉ có Normal (`NEW-3`, `NEW-4`). Nội dung Abnormal/Boundary đã có ở `NEW-10` (payload lạ) và `NEW-11` (rỗng sau lọc) nhưng mang mã Studio `TOOL-KNOW-002` / `TOOL-ERRHYG-001` → không tính cover. **Đề xuất đổi mã** `NEW-10` → `FUNC-001` (Abnormal), `NEW-11` → `FUNC-001` (Boundary) trên Studio. | `[MAJOR]` |
| Q5 | `FRIEND-001` | Cao | **RISK — RULE-01**: chỉ Normal (`NEW-5`, `NEW-6`), không ghi lý do thiếu Abnormal/Boundary. Fix không đổi logic friend info → đủ nếu ghi lý do ở `Ghi chú`; R2 ở §7 bổ sung thêm 1 nhánh `link=3` lưu lần đầu. | `[MAJOR]` |
| Q6 | `FUNC-SEQ-001` | Trung bình | **RISK** — thao tác tạo → sửa → sort trên cùng danh sách chỉ có ở `NEW-8` mang mã lạ `RULE-TOOL-029`. **Đề xuất đổi mã** `NEW-8` → `FUNC-SEQ-001`. | `[MAJOR]` |
| Q7 | `REG-SHARED-001` | Cao | **RISK — RULE-01**: Lesson chỉ có Normal (`NEW-16`), không ghi lý do. Lesson không bị sửa code → smoke Normal là đủ, chỉ cần ghi lý do ở `Ghi chú`. | `[MAJOR]` |

Đã loại khỏi phạm vi (kèm căn cứ):
- `DEPLOY-LIVE-001` / `DEPLOY-ASSET-001` — fix chỉ nới phía server, không đổi JS/asset và không đổi payload client phải gửi; JS cũ đang mở trên trình duyệt vẫn tương thích (chính payload kiểu client cũ đã được gửi ở `NEW-10`).
- `COMPAT-LEGACY-001` / `DATA-MIG-001` — câu hỏi Salon không phải đối tượng từng version-up, không có migration (Dev mục 4.2); dữ liệu cũ đã được `NEW-7` phủ.
- `SYNC-APP-001` — kho FA-020 nhóm "App mobile" (TC-SLN-474…478) chỉ có lưới / ca / booking, không có cài đặt câu hỏi; chưa có căn cứ app gọi `updateSettingForm` → hỏi Dev ở §5 (I6), không đẻ TC.
- `INTG-SHEET-001` · `JOB-001` · `MSG-*` · `PAY-*` — fix không đổi dữ liệu ghi ra Sheet / job / tin nhắn / thanh toán; regression BR-05 (bắt buộc 名前 + メール khi bật 決済) đưa vào R1.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-16` | `NEW-17` → **gộp** vào `NEW-16` | `DUP-SUBSET` | Smoke regression Lesson × Normal × sửa nội dung câu 「単一選択」 + tên lựa chọn trên UI rồi reload × lịch Lesson test → expected "lưu thành công, không 500, giá trị đúng sau reload". Khác biệt duy nhất: `NEW-17` dùng câu đã liên kết friend info có sẵn. | `[MINOR]` |

- **Gate đã chạy**: giả định bỏ `NEW-17` → `REQ-008` + `REG-SHARED-001` vẫn được `NEW-16` cover. Vì `NEW-17` có tiền đề khác (câu liên kết friend info) nên đề xuất **gộp** (thêm 1 câu liên kết friend info vào tiền đề `NEW-16`), không xóa thẳng.
- Không có `DUP-INFLATE`.
- Đã rà 16 TC — các cặp gần nhau khác (`NEW-1`/`NEW-10`: UI vs API; `NEW-13`/`NEW-15`: gửi request vs kiểm tĩnh schema) khác tầng kiểm chứng, không phải trùng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | `NEW-11` | POST `update-setting-form` chỉ chứa `id` + field không phải cột (không còn field hợp lệ nào sau lọc) | *"theo implementation hiện tại trả HTTP 200 và không update"* — expected viết theo hành vi code | `checklist-lme.md` §1.1 RULE-13: request **thiếu tham số / sai cấu trúc → 400**. Không được sửa expected cho khớp code. | (1) TC sai quy ước → expected phải là `400`, code đang trả 200 cần báo Dev · (2) Leader coi "không có gì để cập nhật" là no-op hợp lệ → chốt ngoại lệ `200` và ghi lại quy ước | `[MAJOR]` | Dev / Leader |

**Đã rà**: 16 TC × `spec-features/admin/salon-booking/feature-spec.md` (§2.4, §2.5, Field #47–#48, BR-05) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 31 「予約時のお客様への質問項目」 TC-SLN-316…322, nhóm 41 「決済連携」, nhóm 47 LINE user nhập form, nhóm 52 App mobile, nhóm 54 Dữ liệu cũ) — ngoài C1 không phát hiện `CONF-TC` / `CONF-KHO`. `NEW-7` (câu mặc định không xoá được) khớp TC-SLN-316.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn spec · 16/16 TC | `feature-spec.md` FA-020 **không mô tả hành vi lưu 「質問項目」** — §9.3 tự ghi "chưa capture modal 質問項目", endpoint `update-setting-form` không có trong §6.4; chỉ có Field #47–#48 + BR-05. Cả 16 TC để trống `Trạng thái đánh giá spec` ⇒ expected (toast, mã HTTP, field được lưu) là tự suy từ code. | Member điền `Spec không ghi` + ghi đã hỏi ai cho từng TC; PM bổ sung spec (xem §8 #4). |
| I2 | `[MAJOR]` | `NEW-13`, `NEW-9` | **RULE-13**: có bước gửi request trực tiếp nhưng expected không ghi mã HTTP (`NEW-13`: *"trả thành công"*; `NEW-9`: chỉ kiểm log). | Ghi `HTTP 200` cụ thể vào `Kết quả mong đợi`. |
| I3 | `[MINOR]` | `NEW-1`…`NEW-8` | **RULE-07**: kiểm DB chỉ nằm ở `Ghi chú` ("Oracle DB (local)"), `Kết quả mong đợi` chỉ có UI → chạy tay / chạy staging dễ bỏ tầng DB. | Đưa các điều kiện DB vào `Kết quả mong đợi`. |
| I4 | `[MINOR]` | `NEW-13` | `Loại case = Boundary` nhưng nội dung là quét đủ field hợp lệ (Normal) — làm `DATA-DB-001` trông như đã có Boundary. | Đổi `Normal`; Boundary thật của whitelist là `NEW-11` (rỗng sau lọc). |
| I5 | `[MINOR]` | `NEW-17` | `tc_group = api` nhưng toàn bộ bước là thao tác UI, không gửi request. | Đổi `ui` (hoặc gộp theo DUP-1). |
| I6 | `[NIT]` | Hướng đọc "app quản trị di động / API khác" (BƯỚC 3a) | Dev mục 3 chỉ kê caller web `Basic\CalendarSalonController::updateSettingForm`; chưa rõ app admin mobile hoặc API nào khác gọi `CalendarSalonSettingSendFormService::updateSettingForm`. | Hỏi Dev xác nhận; nếu có → bổ sung 1 TC sửa câu hỏi từ app. |
| I7 | `[NIT]` | Toàn bộ 16 TC | 16/16 Đạt nhưng chỉ chạy `local` bởi AI; Dev cũng chưa chạy được runtime trên DB dev. | Chạy lại tối thiểu `NEW-1`, `NEW-10`, `NEW-12` trên staging trước khi đóng ticket. |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 16 TC — không có TC nào ngoài phạm vi task. `NEW-16` / `NEW-17` (Lesson, layer không bị sửa code) dẫn được từ Studio `dev_impact` ("Lesson cùng lỗi chưa sửa") + `REQ-008` nên không tính là thừa; phần lặp giữa 2 TC đã xử ở §3.

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết:**

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (đọc chọn lọc: bảng Coverage 54 nhóm, MT-11/27, TC-SLN-316…322, 444, 449, 474–475, 488) |
| Vùng regression phát hiện từ kho | TC-SLN-316/317 (名前 + メール bắt buộc khi bật 決済 — BR-05) · TC-SLN-319 (sửa câu đã có câu trả lời) · TC-SLN-322 (Bug #29678 lưu lần đầu khi liên kết friend info) · TC-SLN-444 (LINE user điền form) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không — TC kho mô tả luồng chung, không có bước kiểm chứng sau bản fix whitelist |
| Căn cứ TC regression `R<x>` | R1: BR-05 + TC-SLN-316 (câu mặc định đi qua cùng đường ghi `updateSettingForm`) · R2: TC-SLN-322 + note `NEW-8` "lần sửa đầu tiên của câu vừa tạo đi qua bước lọc mới" |
| Xác nhận chống trùng | Đã đối chiếu 16 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng. Q2 dùng chung TC với G2, Q3 dùng chung TC với G4. Q4–Q7 không đẻ TC (xử bằng đổi mã / ghi lý do). |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | 予約時のお客様への質問項目 | Normal | auto | dev, local, prd, staging | Câu 「単一選択」 liên kết friend info có sẵn — đổi 表示方法 và tuỳ chọn tải sẵn câu trả lời friend info đều lưu được, không 500 | - Đăng nhập admin bot test, chọn bot<br>- Friend info dạng lựa chọn 「QA41489_肝臓病」 (はい / いいえ)<br>- Lịch Salon 「QA41489_Salon」 có câu 「単一選択」 「QA41489_肝臓病の診断を受けている」, 必須, chọn 「すでに作成済みの友だち情報に回答を記録」 → 「QA41489_肝臓病」 (giống ca production: form_type=3, link_friend_information=3) | 1. Mở 「QA41489_Salon」 → tab 「予約設定」 → 「お客様への質問項目」, mở DevTools tab Network<br>2. Chọn câu 「QA41489_肝臓病の診断を受けている」<br>3. Đổi 「表示方法」 sang cách còn lại → quan sát request lưu và toast<br>4. Bật rồi tắt tuỳ chọn tải sẵn câu trả lời từ friend info (field `enable_load_friend_information`, nhãn đối chiếu trên màn) → quan sát request<br>5. Ở mỗi request lưu, ghi lại payload có chứa key `friend_information_setting` hay không<br>6. Tải lại trang, mở lại câu hỏi | 表示方法: đổi qua lại 2 lựa chọn<br>Tuỳ chọn tải sẵn: bật → tắt | - Mỗi lần lưu: HTTP 200, toast 「編集が保存されました」, không request nào trả 500<br>- Sau tải lại: 表示方法 + trạng thái tải sẵn đúng lần lưu cuối; vẫn liên kết 「QA41489_肝臓病」 với 2 lựa chọn<br>- DB `calendar_salon_setting_send_forms`: chỉ `display_method` / `enable_load_friend_information` của đúng dòng này đổi<br>- Ghi rõ thao tác nào có `friend_information_setting` trong payload (để Dev xác nhận trigger thật của lỗi production) | | Lấp G1 · Đánh giá spec: Spec không ghi — hỏi Dev thao tác UI nào sinh payload exception · Evidence: HAR / screenshot Network + toast + query DB trước/sau |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE user — nhập form & xác nhận | Normal | auto | dev, local, prd, staging | Sau khi sửa câu hỏi liên kết friend info, form đặt lịch phía LINE user hiển thị câu hỏi mới và ghi câu trả lời vào đúng friend info | - Như TC-FUNC001-01; lịch 「QA41489_Salon」 đang bật, có course + staff có ca trống<br>- LINE user U1 đã kết bạn bot test, đã có 1 booking cũ trả lời 「はい」 cho câu này<br>- Admin vừa sửa câu hỏi thành 「QA41489_肝臓病」の診断を受けていますか？ và đổi tên lựa chọn 「はい」 → 「はい（診断あり）」 | 1. U1 mở LIFF đặt lịch của 「QA41489_Salon」 → chọn course / staff / slot → tới màn nhập thông tin<br>2. Quan sát câu hỏi + lựa chọn + đánh dấu bắt buộc<br>3. Bỏ trống câu hỏi → bấm xác nhận<br>4. Chọn 「いいえ」 → hoàn tất đặt lịch<br>5. Admin mở detail booking mới + booking cũ của U1; mở friend info 「QA41489_肝臓病」 của U1 | Câu trả lời: いいえ | - Bước 2: hiển thị nội dung câu hỏi mới, lựa chọn 「はい（診断あり）」 / 「いいえ」, có dấu bắt buộc<br>- Bước 3: báo lỗi bắt buộc, không qua được bước xác nhận<br>- Bước 4: đặt lịch thành công, U1 nhận tin xác nhận đặt lịch trên LINE<br>- Booking mới: `friend_info` lưu 「いいえ」; friend info 「QA41489_肝臓病」 của U1 = 「いいえ」<br>- Booking cũ: câu trả lời 「はい」 giữ nguyên | | Lấp G2 · Lấp Q2 (+ DATA-001) · RULE-06 · dẫn từ TC-SLN-444, TC-SLN-319 · Đánh giá spec: Spec không ghi (spec §2.6 chỉ nêu "form nhập thông tin từ calendar_salon_setting_send_forms") · Evidence: screenshot LIFF + detail booking + friend info U1 |
| TC-DATADB001-01 | API | DATA-DB-001 | 予約時のお客様への質問項目 | Abnormal | auto | dev, local, staging | Gửi `can_delete=1` / `order` qua update-setting-form cho câu mặc định 名前 / メール — client không được đổi cột hệ thống | - Đăng nhập web quản trị admin bot test (session + CSRF token)<br>- Lịch 「QA41489_Salon」 có 2 câu mặc định 名前 (friend_information_id = -1) và メール (-3), `can_delete = 0`<br>- Lịch đã liên kết Stripe test và đang bật 「決済機能の利用」<br>- Ghi lại `can_delete`, `order` hiện tại của 2 câu | 1. POST `/basic/calendar-salon/{id lịch}/update-setting-form` với `id` = câu メール, `sub_question` mới, kèm `can_delete=1`, `order=999`<br>2. Kiểm mã HTTP + response<br>3. Tải lại 「お客様への質問項目」 → kiểm nút xoá của câu メール và thứ tự danh sách<br>4. Gọi API xoá câu hỏi với `id` câu メール<br>5. Kiểm tab 「決済連携」 | sub_question = QA41489_メール補足<br>can_delete = 1<br>order = 999 | - Bước 2: HTTP 200, `sub_question` được lưu<br>- DB: `can_delete` vẫn = 0, `order` không đổi<br>- Bước 3: câu メール không có nút xoá, thứ tự không đổi<br>- Bước 4: không xoá được (HTTP 422), câu メール vẫn tồn tại<br>- Bước 5: 決済 vẫn bật, 名前 + メール vẫn bắt buộc (BR-05) | | Lấp G3 · Đánh giá spec: Spec không ghi — cần Leader/Dev chốt `can_delete` / `order` có bị loại khỏi `UPDATABLE_COLUMNS` không (§8 #2); hiện Studio ghi "client vẫn sửa được" ⇒ dự kiến **Không đạt** · Evidence: request/response + query DB trước/sau · không chạy prd vì dự kiến Không đạt — `can_delete=1` có thể làm xoá được câu bắt buộc メール của lịch đang bật 決済 |
| TC-OUTTRUTH001-01 | UI | OUT-TRUTH-001 | 予約時のお客様への質問項目 | Abnormal | auto | dev, local, prd, staging | Lưu câu hỏi thất bại (chặn request / hết session) — UI phải báo lỗi, không hiện toast thành công | - Đăng nhập admin bot test, chọn bot<br>- Lịch 「QA41489_Salon」 có câu 「短文回答」 「QA41489_連絡先」 | 1. Mở 「お客様への質問項目」, chọn 「QA41489_連絡先」<br>2. DevTools → Network → chặn URL chứa `update-setting-form` (Block request URL)<br>3. Sửa nội dung câu hỏi, rời ô nhập → quan sát màn hình<br>4. Bỏ chặn; mở tab khác đăng xuất (session hết hạn), quay lại sửa câu hỏi → quan sát<br>5. Đăng nhập lại, tải lại trang, mở câu hỏi | Nội dung sửa: QA41489_連絡先_失敗テスト | - Bước 3 + 4: KHÔNG hiện toast 「編集が保存されました」; hiện thông báo lỗi lưu thất bại (bước 4 có thể chuyển về màn đăng nhập)<br>- Bước 5: nội dung câu hỏi vẫn là giá trị cũ (không có "đã lưu giả") | | Lấp G4 · Lấp Q3 (+ UI-003) · Đánh giá spec: Spec không ghi message lỗi — PM chốt (§8 #3); Studio ghi "FE vẫn nuốt lỗi 500" ⇒ dự kiến **Không đạt**, Leader quyết định tách ticket FE · Evidence: screen recording + Network |
| TC-DATADB001-02 | API | DATA-DB-001 | 予約時のお客様への質問項目 | Abnormal | auto | dev, local, staging | update-setting-form với `id` câu hỏi của bot khác / calendar khác — không được sửa bản ghi ngoài phạm vi | - 2 bot test A, B (cùng tài khoản test, không dùng bot khách thật), mỗi bot có lịch Salon có câu 「長文回答」 trùng tên 「QA41489_共通質問」<br>- Bot A có thêm lịch 「QA41489_Salon2」 cũng có câu 「QA41489_共通質問」<br>- Đăng nhập web quản trị admin bot A (session + CSRF token)<br>- Ghi lại id + nội dung 3 câu hỏi | 1. POST `/basic/calendar-salon/{lịch Salon bot A}/update-setting-form` với `id` = câu 「QA41489_共通質問」 của **bot B**, `question` mới<br>2. Kiểm mã HTTP<br>3. Lặp lại với `id` = câu của 「QA41489_Salon2」 (cùng bot A, khác lịch)<br>4. Query DB 3 câu hỏi; mở màn câu hỏi của bot B (đăng nhập admin bot B) và của 「QA41489_Salon2」 | question = QA41489_越権更新 | - Bước 1: HTTP 403 hoặc 404; câu của bot B không đổi (DB + màn bot B)<br>- Bước 3: HTTP 404 (câu không thuộc lịch trong URL); câu của 「QA41489_Salon2」 không đổi<br>- Câu cùng tên trong lịch Salon bot A cũng không đổi (không update nhầm theo tên) | | Lấp Q1 · RULE-07 (trùng tên 2 tài khoản) · RULE-13 · Đánh giá spec: Spec không ghi · Evidence: request/response + query DB trước/sau trên cả 2 bot · không chạy prd vì gửi `id` bản ghi của bot khác — nếu lỗ hổng tồn tại sẽ ghi đè dữ liệu bot khác, nhầm `id` là sửa dữ liệu khách thật |
| TC-UIFIELD001-01 | UI | UI-FIELD-001 | 予約時のお客様への質問項目 | Normal | auto | dev, local, prd, staging | Lịch đang bật 決済 — sửa bổ sung của câu mặc định 名前 / メール vẫn lưu, 2 câu vẫn bắt buộc | - Đăng nhập admin bot test, chọn bot<br>- Lịch 「QA41489_Salon」 đã liên kết Stripe (môi trường テスト) và bật 「決済機能の利用」 → 名前 (-1) + メール (-3) đang bật + bắt buộc | 1. Mở 「お客様への質問項目」 → chọn câu 名前, sửa 「補足」 → rời ô nhập<br>2. Chọn câu メール, sửa 「補足」 → rời ô nhập<br>3. Thử tắt 「必須」 / tắt hiển thị của 2 câu<br>4. Tải lại trang; mở tab 「決済連携」<br>5. LINE user mở LIFF đặt lịch tới màn nhập thông tin | 補足 名前: QA41489_フルネームで入力<br>補足 メール: QA41489_決済確認用 | - Bước 1–2: toast 「編集が保存されました」, không 500<br>- Bước 3: không tắt được (giữ bắt buộc + hiển thị)<br>- Bước 4: 補足 mới được giữ; 決済 vẫn bật<br>- Bước 5: 名前 + メール hiển thị bắt buộc kèm 補足 mới | | Lấp R1 · regression · dẫn từ TC-SLN-316 + BR-05 (cùng đường ghi `updateSettingForm` đã thêm bước lọc) · Đánh giá spec: Spec ghi rõ (BR-05) · Evidence: screenshot admin + LIFF |
| TC-FRIEND001-01 | UI | FRIEND-001 | 予約時のお客様への質問項目 | Normal | auto | dev, local, prd, staging | Tạo câu 「単一選択」 mới liên kết friend info có sẵn — lưu được ngay lần đầu | - Đăng nhập admin bot test, chọn bot<br>- Friend info dạng lựa chọn 「QA41489_来店経験」 (初めて / 2回目以上)<br>- Lịch 「QA41489_Salon」 | 1. 「お客様への質問項目」 → 「この項目を追加」 → 「単一選択」<br>2. Nhập nội dung câu hỏi<br>3. Chọn 「すでに作成済みの友だち情報に回答を記録」 → 「QA41489_来店経験」 → rời ô nhập (lưu LẦN ĐẦU)<br>4. Tải lại trang, mở câu vừa tạo | Câu hỏi: QA41489_ご来店は初めてですか | - Bước 3: toast 「編集が保存されました」 ngay lần đầu, không 500<br>- Bước 4: câu hỏi còn đó, liên kết 「QA41489_来店経験」 với 2 lựa chọn 初めて / 2回目以上<br>- DB: `link_friend_information = 3`, `friend_information_id` = id của 「QA41489_来店経験」 | | Lấp R2 · regression · dẫn từ TC-SLN-322 (Bug #29678) + note `NEW-8` "lần sửa đầu của câu vừa tạo đi qua bước lọc mới" · Lấp thêm Q5 (nhánh link=3 khi tạo mới) · Đánh giá spec: Spec không ghi · Evidence: screenshot + query DB |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | Quy ước response `update-setting-form` | Request không còn field hợp lệ sau lọc trả `200` (no-op) hay `400` (thiếu tham số) theo RULE-13 | C1 CONF-SPEC (`NEW-11`) | Dev / Leader |
| 2 | `feature-spec.md` §2.4 + Field #47–#48 | `can_delete` / `order` có được client sửa qua `update-setting-form` không — fix chốt "client không đổi cột hệ thống" nhưng 2 cột này vẫn nằm trong whitelist | G3 | Dev / Leader |
| 3 | `feature-spec.md` §2.4 (質問項目) | Hành vi UI khi lưu câu hỏi thất bại (message lỗi, không toast thành công) | G4 | PM |
| 4 | `feature-spec.md` §2.4 + §6.4 | Bổ sung mô tả modal 「予約時のお客様への質問項目」 (5 kiểu câu, 3 chế độ liên kết friend info, cách lưu từng field) + endpoint `POST /basic/calendar-salon/{id}/update-setting-form` — hiện §9.3 ghi "chưa capture" | I1 | PM |
