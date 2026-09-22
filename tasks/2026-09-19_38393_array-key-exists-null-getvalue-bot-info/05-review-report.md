# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #195 (ticket 38393, round 1, branch `ai_fixbug_38393`) |
| Tổng số TC review | 7 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 3/10 vùng ảnh hưởng đủ TC (happy path `F2`, happy path `F3`, unit `F1`) · 3 GAP · 4 RISK

> Chiều `diff code`: tab Thông tin của Studio (`spec_delta` + `dev_impact`) được tính lúc **2026-08-24 trên commit `3a0fd43306`**. Nó **chưa có** commit tự review v1 `9df5f81524` (journal #137191, 2026-09-19). Vì vậy chiều (b) được bổ sung từ `03-dev-impact.md` mục 2 + 3.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` / `F5` / `T1` — `Ajax/ChangeBotController::init` (GET `/change-bot/init`, màn LINE公式アカウント入れ替え FA-044). Đây là **nơi exception thật sự bắn ra production** (18 lần) | `dev-impact` | không có | **GAP** — cả 7 TC chỉ test `reGetAvatarBot` / `reGetProfileBot` / helper. Chưa có TC nào mở màn đổi LOA khi đã có 予約 mà credential LOA mới lỗi, tức luồng gây ra ticket | `[BLOCKER]` |
| G2 | `F2` / `F3` + `D1–D4` — điều kiện mới `&& is_array($infoBot)` ở `reGetProfileBot:1212` và `reGetAvatarBot:11400` (tự review v1). Khi body không phải JSON → vào nhánh else, **giữ nguyên** ảnh/tên cũ | `diff code` | `NEW-3`, `NEW-6` | **RISK** — nhánh false chỉ có 2 TC. Cả 2 đang `skip`, dùng mã lạ `TOOL-KNOW-002`, và expected viết theo bản fix cũ ("DB ghi rỗng `bot_image=''`"), **ngược** với hành vi hiện tại. Biên `{}` / `[]` (decode ra mảng rỗng nên qua được `is_array`) chưa có TC | `[BLOCKER]` |
| G3 | `F4` — `BotController::changeNewBotStep1` (POST `/ajax/admin/step1-change-new-bot`). Bọc update `bots_profiles` bằng `if(!empty($infoBot))` (v1). Đây là nơi regression thứ 2 | `dev-impact` | không có | **GAP** — 0 TC. Input thiếu: spec chưa rõ luồng UI hiện hành nào còn gọi endpoint này. Spec FA-044 api-spec ghi "vẫn sống cho luồng thêm bot" (`add_bot.js` / `add_bot_v5.js` / `step5qr.js`), còn bot-add-v2 chỉ gọi khi có `botIdChange` (G-09 chưa rõ) | `[MAJOR]` |
| G4 | `F1` — `getValue()` dùng chung: 20 caller / 8 file | `diff code` | `NEW-7` | **RISK** — chỉ có test tĩnh/unit cho helper và 2/20 caller. Nhóm (A) "8 điểm CHỈ ĐỌC" Dev chưa kê tên. Chưa có TC smoke nào cho caller có guard (`step2Check` luồng thêm bot…) | `[MAJOR]` |
| G5 | `F2` / `F3` — nhánh LINE trả lỗi 401 (catch có sẵn trước fix) | `dev-impact` | `NEW-2`, `NEW-5` | **RISK** — TC đúng ý định nhưng cả 2 `skip`, chưa có kết luận | `[MAJOR]` |
| G6 | `T2` — Chat 1:1 có **2 điểm vào** (`detail_content.blade.php:409` nút 初期設定 + modal プロフィール設定 `setting_profile.blade.php:37`) | `dev-impact` | `NEW-4`, `NEW-5`, `NEW-6` | **RISK** — các bước chỉ ghi "khu vực profile mặc định, bấm 初期設定", không rõ đi qua điểm vào nào. Điểm còn lại chưa được đi qua | `[MINOR]` |
| G7 | `T3` — màn ADMIN `confirm_contract_standard.blade.php:643` (duyệt hợp đồng) gọi `reGetAvatarBot` | `dev-impact` | không có | **GAP** — 0 TC. Chỉ có điểm vào 情報更新 ở màn LOA接続設定 (NEW-1..3) | `[MINOR]` |

- G1 → §5 `TC-INTGLINE001-01`, `-02` + dùng lại kho `TC-CB-11` cho chiều Normal.
- G2 → sửa `NEW-3` / `NEW-6` (§4 I5) + §5 `TC-INTGLINE001-03`, `-04` (biên `{}`).
- G3 → **không đề xuất TC chi tiết**: chưa xác định được thao tác UI nào gọi `step1-change-new-bot`, và viết steps lúc này là bịa. Leader cần hỏi Dev (a) màn/nút hiện hành gọi endpoint và (b) cách giả lập `/v2/bot/info` lỗi **sau** bước `step2-check`. Có câu trả lời thì viết 1 TC Abnormal: "profile 初期設定 của bot không bị ghi NULL". Nếu Dev xác nhận endpoint không còn được gọi từ UI → verify tĩnh diff là đủ.
- G4 → §5 `TC-REGSHARED001-01` (smoke luồng thêm bot) + hỏi Dev danh sách nhóm (A).
- G5 → không cần TC mới: chạy lại `NEW-2` / `NEW-5`.
- G6 → dùng lại kho `TC-CHT-135` (icon reload trong modal 送信者名を変更) cho điểm vào modal + sửa steps NEW-4..6 (§4 I7).
- G7 → không đề xuất: màn admin nội bộ, `spec-features/` không có spec. Endpoint EP-05 đã có NEW-1/NEW-2. Hỏi Dev đường vào nếu Leader muốn smoke.
- `D2` mirror `bot_category.bot_view_name`: không đề xuất TC. Nhánh ghi thành công không bị fix chạm tới, và nguy cơ lệch là vấn đề có sẵn từ trước.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 5 quan điểm Trigger khớp task (`FUNC-001` · `INTG-LINE-001` · `OUT-TRUTH-001` · `REG-SHARED-001` · `DATA-DB-001`) · 3 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `INTG-LINE-001` | Cao | **RISK** — gọi LINE `/v2/bot/info` ở 3 luồng, nhưng không TC nào mang mã này. 4 TC có nội dung khớp (`NEW-2/3/5/6`) đều `skip`, và 2 trong đó dùng mã lạ `TOOL-KNOW-002`. Luồng FA-044 `/init` chưa có TC nào (G1). Loại lỗi mới test 2/≥3 (401, body null); thiếu body không phải JSON và biên `{}` | `[BLOCKER]` |
| Q2 | `OUT-TRUTH-001` | Cao | **RISK** — sau v1, body hỏng → server trả `success:true` với ảnh/tên **CŨ**. Người dùng thấy "đồng bộ xong" trong khi không có gì được đồng bộ (**false success**). Không TC nào kiểm tra thông báo này có khớp thực tế không. `NEW-2`/`NEW-5` (Abnormal) thì `skip`; không có Normal/Boundary mang mã này | `[MAJOR]` |
| Q3 | `REG-SHARED-001` | Cao | **RISK** — chỉ có `NEW-7` (Abnormal, unit tĩnh), chưa test lại **từng nơi** Dev kê (xem G4). Normal/Boundary gộp vào data_input của NEW-7, đã có lý do trong Ghi chú, chấp nhận | `[MAJOR]` |

- Đã loại khỏi phạm vi: `PERM-003` (trigger "change bot") — fix không chạm logic phân quyền/ownership của màn đổi LOA (`BR-10`). `DATA-DB-001` phần WHERE scope 2 tài khoản — fix không đổi `WHERE`, v1 chỉ bỏ qua lệnh UPDATE. Phần "DB giữ nguyên" đã được verify ở G2. RULE-08 không kích hoạt: không có media upload, domain, job hay bill tiền; `pictureUrl` là URL do LINE cấp.
- Mã `TOOL-KNOW-002` (NEW-3, NEW-6) không có trong `checklist-lme.md` nên **không tính là cover**.

---

## 3. TC trùng lặp nội dung

Đã rà 7 TC, không phát hiện trùng lặp. Các cặp NEW-1/NEW-4, NEW-2/NEW-5, NEW-3/NEW-6 cùng quan điểm và cùng loại case, nhưng khác đối tượng (endpoint `reGetAvatarBot` ở màn LOA接続設定 so với `reGetProfileBot` ở chat 1:1), nên không trùng.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Nguồn — 7 TC | Chỉ 3/7 TC `pass` (**42.9% < 50%**). 4 TC `skip` (NEW-2, 3, 5, 6) chính là toàn bộ nhánh lỗi mà fix nhắm tới. 3 TC pass đều là happy path hoặc unit tĩnh | Chạy lại 4 TC skip (sau khi sửa NEW-3/NEW-6 theo I5). Chưa được kết luận fix đạt |
| I2 | `[MAJOR]` | Nguồn — Studio tab Thông tin | `spec_delta` / `dev_impact` tính lúc 2026-08-24 trên commit `3a0fd43306`. `dev_impact` ghi "HTTP 200 + body null → empty string", nay đã **sai** sau v1 `9df5f81524`. `requirements` REQ-03/REQ-06 cũng mô tả "DB update ảnh/tên = rỗng" | Tính lại context/requirements của task #195 trên Studio theo commit mới nhất |
| I3 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill bởi `/new-task` 2026-09-19, checkbox "Tester verify auto-fill chính xác" **chưa tick**. F/D/T có thể thiếu hoặc map sai | Tester đối chiếu journal #137191 rồi tick |
| I4 | `[MAJOR]` | `NEW-1`, `NEW-4`, `NEW-7` | RULE-02: 3 TC `pass` (run #1729, AI chạy, staging) nhưng `testcase_list` không có evidence. Chưa xác nhận được đã kiểm tra đủ 3 tầng DB + màn + response | Mở run #1729 trên Studio kiểm tra artifact (query DB trước/sau, screenshot, response JSON). Thiếu thì chạy lại |
| I5 | `[MAJOR]` | `NEW-3`, `NEW-6` | (a) Expected viết theo bản fix cũ (`success:true, img:'', nick_name:''`, DB ghi rỗng). Sau v1 phải là **giữ nguyên** `bots.bot_image/view_name` + `bots_profiles(is_default=1)`, không exception. (b) Expected có câu "ASSUMPTION cần confirm" nên không đo lường được. (c) Mã `TOOL-KNOW-002` không có trong checklist. (d) `[AP-1]` nhánh mới chỉ có 1 trigger (body `null`) | Sửa trên Studio (`testcase_update`): expected = giữ nguyên dữ liệu cũ + response theo chốt ở §6 #1. Thêm data_input body HTML / không phải JSON. Đổi mã sang `INTG-LINE-001` |
| I6 | `[MAJOR]` | `NEW-3`, `NEW-6` | Tiền đề "Bind stub GuzzleHttp\Client" — người khác không dựng lại được env (stub ở đâu, bật bằng cách nào, env nào hỗ trợ) | Ghi rõ cơ chế stub của runner (local/dev). Nếu chỉ runner làm được thì giữ `auto`, ghi rõ không chạy được trên production |
| I7 | `[MAJOR]` | `NEW-4`, `NEW-5`, `NEW-6` | Bước "Ở khu vực profile mặc định, bấm 初期設定" mơ hồ. Chat có 2 điểm vào (nút 初期設定 ở `detail_content` và icon reload trong modal 送信者名を変更 / プロフィール設定, xem kho `TC-CHT-135`) | Ghi rõ đường vào: menu → màn → nút. Nên tách 1 TC cho mỗi điểm vào, hoặc ghi rõ TC này chỉ cover điểm nào |
| I8 | `[MAJOR]` | Spec — chat 1:1 | `spec-features/admin/chat-11` không mô tả `/ajax/reget-profile-bot` (Studio cũng ghi "gap spec"). Không có chuẩn cho expected của NEW-4..6 | Input thiếu: spec cho chức năng reload profile 初期設定 ở chat. Bổ sung spec hoặc Leader chốt expected |
| I9 | `[MINOR]` | `NEW-5` (Ghi chú) | Studio ghi nhận quirk FE có sẵn: `chat-v2.js` kiểm tra `a.status==0` trong khi controller trả `success`/`msg`. Khi 401, FE gán `nick_name`/`avt_path = undefined` và không alert. Lỗi này có từ trước, fix #38393 không chạm | Leader cân nhắc raise ticket riêng. Không mở scope TC ở ticket này |
| I10 | `[NIT]` | Dev-impact vs spec | Dev ghi `/ajax/change-bot/init`, spec FA-044 ghi `/admin/ajax/change-bot/init` | Không ảnh hưởng TC (TC đi qua UI) |
| I11 | `[NIT]` | Build test | Release đã có patch độc lập `$infoBot ?? []` ở `ChangeBotController.php:53/54/57` (commit `b285b3acd9`). G1 có thể pass nhờ patch đó dù `getValue` chưa merge | Ghi rõ commit/build khi chạy G1 |

---

## 5. TCs đề xuất bổ sung (5)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa039-changebot-LINE公式アカウント入れ替え機能.md` (nhóm "Menu & điều kiện truy cập") · `kho-tcs/fa001-chat11-11チャット.md` (nhóm "Profile người gửi — quản lý"). Kho chưa có tab cho `bot-edit` (LOA接続設定) / `bot-add-v2` |
| Vùng regression phát hiện từ kho | `TC-CB-11` (đã có 予約 → vào thẳng màn đã đặt lịch) · `TC-CHT-135` (icon reload 初期設定 trong modal 送信者名を変更) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | G1 chiều Normal → `TC-CB-11` "Bot đã có đặt lịch đổi LOA active → vào màn đổi LOA bị điều hướng NGAY sang màn đã đặt lịch" (bổ sung kiểm tra ảnh/tên LOA mới hiển thị đúng) · G6 → `TC-CHT-135` "Nút reload profile — lấy thông tin mới nhất khi bot thay đổi tên/ảnh" |
| Xác nhận chống trùng | Đã đối chiếu 7 TC ở BƯỚC 0 + 2 file kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGLINE001-01 | UI | INTG-LINE-001 | Đổi LOA (LINE公式アカウント入れ替え) — màn đã đặt lịch | Abnormal | auto | Tất cả | Mở màn đổi LOA khi đã có 予約 nhưng credential LOA mới hết hiệu lực — màn vẫn hiển thị, không lỗi 500 | - Đăng nhập Admin chủ (主管理者) của bot A, plan Standard trở lên (gói free không đặt lịch được)<br>- Bot A đã tạo 1 đặt lịch đổi sang LOA B (chọn 「…予約をする」 → nhập Channel ID/secret của LOA B → 「この内容で接続する」), đang ở màn 「入れ替え予約が設定されています」<br>- Sau đó vào LINE Developers của channel Messaging API LOA B → **reissue Channel secret**, để secret đã lưu trong đặt lịch hết hiệu lực | 1. Vào sidebar 「エルメシステム設定」 → 「LINE公式アカウント入れ替え」<br>2. Chờ trang tải xong, quan sát màn hiển thị<br>3. Quan sát khu vực thông tin LOA mới (ảnh đại diện + tên)<br>4. Bấm F5 tải lại trang 2 lần | Bot A plan Standard · LOA B có Channel secret đã reissue sau khi đặt lịch | - Trang tải xong, **không** hiện màn lỗi 500 / trang trắng / loading mãi<br>- Vẫn vào màn đã đặt lịch 「入れ替え予約が設定されています」<br>- Ảnh + tên LOA mới hiển thị rỗng (hoặc placeholder), không hiện ảnh/tên của LOA khác<br>- Nút 「接続予約を削除」 và 「LINE公式アカウント 入れ替えを実行」 vẫn hiển thị<br>- Tải lại nhiều lần: kết quả giống nhau, log server không có `array_key_exists() expects parameter 2 to be array, null given` |  | Lấp G1 · Lấp Q1 · Đánh giá spec: Spec không ghi (FA-044 chỉ ghi `/init` gọi 4 LINE API live; hành vi khi lỗi lấy theo Dev: "hiện tên/ảnh rỗng thay vì HTTP 500") · Evidence: screenshot màn sau khi tải + log server khoảng thời gian test · regression — Normal dùng lại kho `TC-CB-11` · Boundary: không áp dụng (lỗi credential là nhị phân, không có biên) · Ghi rõ commit/build khi chạy (xem §4 I11) |
| TC-INTGLINE001-02 | UI | INTG-LINE-001 | Đổi LOA (LINE公式アカウント入れ替え) — xoá đặt lịch | Abnormal | auto | Tất cả | Từ màn đã đặt lịch tải lỗi thông tin LOA mới, vẫn xoá được đặt lịch | - Như TC-INTGLINE001-01 (đã có 予約 sang LOA B, Channel secret LOA B đã reissue)<br>- Đang ở màn 「入れ替え予約が設定されています」, ảnh/tên LOA mới hiển thị rỗng | 1. Bấm 「接続予約を削除」<br>2. Ở popup xác nhận, bấm 「削除する」<br>3. Quan sát màn quay về<br>4. Tải lại trang 「LINE公式アカウント入れ替え」 | Như TC-INTGLINE001-01 | - Popup xác nhận hiện ra, bấm 「削除する」 không báo lỗi<br>- Quay về màn chọn phương thức, không thẻ nào đang được chọn<br>- Tải lại trang: không còn vào màn đã đặt lịch (đặt lịch đã bị huỷ)<br>- Không có màn lỗi 500 ở bất kỳ bước nào |  | Lấp G1 · Lấp Q1 · Đánh giá spec: Spec ghi rõ (FA-044 §2.3 B1: xoá đặt lịch → soft-cancel `status=5`, về SCR-CHB-02 với `selectedMethod=null`) · Evidence: screenshot từng bước + trạng thái đặt lịch sau khi xoá |
| TC-INTGLINE001-03 | UI | INTG-LINE-001 | LOA接続設定 (bot-edit) — nút 情報更新 | Boundary | auto | staging | 情報更新 khi LINE trả HTTP 200 với body JSON rỗng `{}` — ảnh/tên bot không bị xoá trắng | - Đăng nhập admin, đã chọn bot A (channel_access_token hợp lệ); ảnh + tên bot A hiện tại đã biết (ghi lại trước khi test)<br>- Runner bật stub cho LINE `GET /v2/bot/info`: HTTP 200, body `{}` (JSON rỗng: decode ra mảng rỗng, vẫn qua được kiểm tra `is_array`) | 1. Mở màn 「LOA接続設定」 của bot A<br>2. Bấm 「情報更新」<br>3. Quan sát thông báo / trang tải lại<br>4. Quan sát ảnh + tên bot trên màn LOA接続設定<br>5. Mở chat 1:1 → modal 送信者名を変更, xem dòng 初期設定<br>6. Lặp lại bước 1–4 với body `[]` | Stub LINE `/v2/bot/info` → 200 + `{}`; lần 2 → 200 + `[]` | - Không lỗi 500 / không exception<br>- Ảnh + tên bot trên màn LOA接続設定 **giữ nguyên** giá trị trước khi test, không bị trắng<br>- Dòng 初期設定 trong modal 送信者名を変更 cũng giữ nguyên ảnh + tên<br>- Thông báo cho người dùng khớp thực tế (xem §6 #1: nếu Dev chốt báo lỗi thì phải hiện lỗi, không được báo thành công) |  | Lấp G2 · Lấp Q1 · Lấp Q2 · Đánh giá spec: Spec không ghi — expected "giữ nguyên" lấy theo mục đích tự review v1 của Dev, cần Dev xác nhận `{}`/`[]` cũng đi nhánh else · Evidence: screenshot trước/sau ở 2 màn + response 情報更新 · staging vì cần stub LINE, không làm được trên production · Nếu thực tế bị xoá trắng → raise bug (guard v1 bỏ sót mảng rỗng) |
| TC-INTGLINE001-04 | UI | INTG-LINE-001 | Chat 1:1 — reload profile 初期設定 | Boundary | auto | staging | Reload profile 初期設定 ở chat khi LINE trả HTTP 200 với body JSON rỗng `{}` — ảnh/tên không bị xoá trắng | - Đăng nhập admin, đã chọn bot A (token hợp lệ); ảnh + tên dòng 初期設定 hiện tại đã biết<br>- Runner bật stub LINE `GET /v2/bot/info`: HTTP 200, body `{}` | 1. Mở chat 1:1 (/basic/chat-v3), mở 1 cuộc trò chuyện bất kỳ<br>2. Mở modal 送信者名を変更<br>3. Ở dòng 初期設定, bấm icon reload<br>4. Quan sát ảnh + tên dòng 初期設定<br>5. Đóng modal, mở lại, quan sát lần nữa<br>6. Mở màn 「LOA接続設定」 xem ảnh + tên bot<br>7. Lặp lại bước 2–4 với body `[]` | Stub LINE `/v2/bot/info` → 200 + `{}`; lần 2 → 200 + `[]` | - Không lỗi, overlay loading tắt, không đứng màn<br>- Ảnh + tên 初期設定 **giữ nguyên**, không trắng, không hiện `undefined`<br>- Mở lại modal / màn LOA接続設定: ảnh + tên vẫn là giá trị cũ |  | Lấp G2 · Lấp Q1 · Lấp Q2 · Đánh giá spec: Spec không ghi (chat-11 không có spec reload profile — §4 I8) · Evidence: screenshot trước/sau + response reload · staging vì cần stub LINE · điểm vào modal theo kho `TC-CHT-135` |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Thêm tài khoản LINE mới (bot-add-v2) — kết nối Messaging API | Normal | auto | Tất cả | Thêm LOA mới với credential hợp lệ — tên + ảnh bot lấy từ LINE hiển thị đúng sau fix getValue | - Đăng nhập admin có slot trống để thêm bot<br>- Có 1 LOA C chưa kết nối LME, Channel ID/secret Messaging API + LINE Login hợp lệ; biết tên hiển thị + ảnh đại diện của LOA C trên LINE Official Account Manager | 1. Vào luồng thêm tài khoản LINE mới (新規アカウント追加)<br>2. Đi hết wizard: nhập Channel ID/secret Messaging API + LINE Login → bật webhook → 次へ進む<br>3. Ở bước QR test, dùng điện thoại quét QR, kết bạn và gửi sticker<br>4. Sau khi kết nối xong, quan sát tên + ảnh bot ở màn hoàn tất / header / 「LOA接続設定」<br>5. Mở chat 1:1 → modal 送信者名を変更, xem dòng 初期設定 | LOA C mới, credential hợp lệ | - Wizard chạy hết, không lỗi<br>- Tên + ảnh bot hiển thị đúng tên + ảnh của LOA C trên LINE (không rỗng, không NULL)<br>- Dòng 初期設定 ở chat hiển thị đúng tên + ảnh LOA C |  | Lấp G4 · Lấp Q3 · regression — caller `step2Check` (nằm trong guard `if($infoBot)`, Dev nói hành vi không đổi) đi qua nhánh mảng hợp lệ của `getValue` · Đánh giá spec: Spec ghi rõ (bot-add-v2: `/v2/bot/info` → UPDATE `bots.view_name`/`bot_image`, hiển thị SCR-BAV-08) · Evidence: screenshot tên/ảnh ở 2 màn so với LINE OA Manager · Bước quét QR bằng điện thoại có thể mô phỏng callback, vẫn `auto` |

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | bot-edit `feature-spec.md` Luồng 「情報更新」 (EP-05) + spec chat (reload 初期設定) | Chốt **response khi LINE trả 200 nhưng body không phải JSON**. Sau v1, server trả `success:true` kèm ảnh/tên **cũ** và không đồng bộ gì, nên người dùng tưởng đã cập nhật (false success — `OUT-TRUTH-001`). Trước fix, trường hợp này vào catch và trả `success:false '認証できませんでした。'`. Cần chốt: giữ `success:true` hay trả lỗi | Journal #137191 mục 4.2 (API contract) vs spec EP-05 (chỉ mô tả nhánh thành công + lỗi 認証) | Dev / Leader |
| 2 | Studio task #195 `requirements` REQ-03 / REQ-06 | Đang ghi "sau fix … DB update ảnh/tên = rỗng", đã sai sau v1 → đổi thành "giữ nguyên ảnh/tên cũ" | Journal #137191 (v1) vs REQ-03/REQ-06 | Leader (sửa trên Studio) |
| 3 | `change-bot/web/api-spec.md` + `bot-add-v2` G-09 | Làm rõ luồng UI hiện hành nào còn gọi `/ajax/admin/step1-change-new-bot` (`changeNewBotStep1`), để test được regression thứ 2 của v1 (G3) | Journal #137191 mục 3 vs api-spec ("vẫn sống cho luồng thêm bot") vs bot-add-v2 (chỉ khi `botIdChange`) | Dev |
