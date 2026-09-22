# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #211 (round 1 · runs local #521 / #1706 / #1719) |
| Tổng số TC review | 16 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 5/14 vùng ảnh hưởng đủ TC · 6 GAP · 3 RISK · 3 TC orphan.

> ⚠️ **Input thiếu (chiều diff code)**: `spec_delta` và `dev_impact` của Studio tính lúc **2026-08-26** trên base `release_step_20260623`. Chúng chỉ chứa diff **vòng 1** (1 file, +20/−1: validate + catch), **chưa có** guard chéo bot của v3 (commit `fff7807509`). `dev_impact` cũng vẫn ghi "3 màn gọi endpoint". Vì vậy phần v3 ở chiều (b) được suy từ `03-dev-impact.md` mục 2–3.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | **F3 + D4 + T2** — guard chủ sở hữu chéo bot trong `saveSettingInfoFriend` (HTTP 404 `設定が見つかりません`), bảo vệ `friend_information_value` / `friend_info_option_selects` / `total_user_has_value` của bot khác | dev-impact + diff code | không có | **GAP** — 0 TC. Cả nhánh chặn (id bot khác) lẫn nhánh cho qua theo bot đang chọn đều chưa test. Bộ TC viết trước v3 | `[BLOCKER]` |
| G2 | **F2** — catch block trả message chung `システムエラーが発生しました。…` cho **mọi** exception | diff code | NEW-20 · NEW-26 | **RISK** — fix dạng generic catch nhưng TC chỉ có 1–2 trigger mơ hồ ("group_id / setting_actions gây lỗi", "cố ý tạo exception"). Chưa đủ ≥ 3 trigger khác nhau + 1 trigger chưa biết | `[BLOCKER]` |
| G3 | **F5** — `editInfo` / luồng **sửa** trường có sẵn đi qua guard mới (Dev khẳng định guard là no-op với luồng hợp lệ) | diff code | không có (NEW-22 chỉ test **tạo mới**) | **GAP** — hành vi cũ "sửa trường của chính bot rồi lưu" chưa có TC chứng minh không hỏng | `[MAJOR]` |
| G4 | **D2 + T3** — trường mặc định 生年月日 (`d_4`, `action_info_friend_default.title`) nằm ngoài danh sách bỏ qua nên đi qua validate mới | dev-impact | không có (NEW-19 / NEW-28 chỉ test d_1 / d_2 / d_3 / d_6) | **GAP** — chưa test d_4 bị chặn khi 管理名 rỗng, cũng chưa test lưu cấu hình action của 生年月日 qua UI vẫn thành công | `[MAJOR]` |
| G5 | **F1** — validate 管理名 ở luồng **cập nhật** (id là trường có sẵn của bot) | dev-impact | NEW-13 / 14 / 15 / 16 / 17 / 18 đều dùng `id=''` (tạo mới) | **RISK** — chỉ test nhánh tạo mới; chưa test sửa trường có sẵn với 管理名 rỗng: 管理名 cũ phải giữ nguyên | `[MAJOR]` |
| G6 | **BUG** — replay đúng payload ticket `{id:"", title:"", group_id:0, type_data:4}` | dev-impact | NEW-14 (tái hiện nhưng dùng `type_data=2`, `group_id` hợp lệ) | **RISK** — không TC nào gửi đúng payload của ticket (folder `0` + kiểu 画像) | `[MINOR]` |
| G7 | NEW-24 · NEW-25 · NEW-27 (Tag Management) | orphan | — | Dev đính chính v3: màn tag gọi `saveTag()` → `/ajax/save-tag`, **không** gọi endpoint này. Actual của NEW-27 cũng ghi `postedToEndpoint=false`, message `管理名を入力してください。`. 3 TC này không chạm điểm sửa nào | `[MINOR]` |

- G1 → TC-PERM003-01/02/03 · G2 → TC-SEC002-01 · G3 → TC-PERM003-01 · G4 → TC-FUNC001-01 + TC-FUNC002-02 · G5 → TC-FUNC002-01.
- G6 không đề xuất TC mới: bổ sung biến thể payload vào NEW-14 (xem §4 I9).
- G7 không đề xuất TC mới: đề nghị Leader xóa / archive 3 TC trên Studio vì chúng không cover impact nào, và FA-012 được Dev xác nhận không bị ảnh hưởng.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp task · 5 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PERM-003` | Cao | **GAP** — 0 TC cách ly dữ liệu giữa 2 bot ở đường lưu định nghĩa trường (MAP-PERM-03: đổi id sang bot khác → từ chối). Cần đủ Normal + Abnormal + Boundary (RULE-01) | `[BLOCKER]` |
| Q2 | `DATA-DB-001` | Cao | **GAP** — fix v3 chính là bịt lỗi thiếu `WHERE bot_id` ở các câu UPDATE/DELETE kèm theo, nhưng không TC nào kiểm bot B không đổi sau request từ bot A | `[BLOCKER]` |
| Q3 | `FUNC-002` | Cao | **RISK** — nội dung "bỏ trống 管理名" có TC nhưng gắn mã lạ (NEW-21 `TOOL-VAL2-001`, NEW-14 `TOOL-KNOW-002`) hoặc mã khác (NEW-13 / NEW-15 `FUNC-003`) → theo quy tắc tính là chưa cover. Checklist còn yêu cầu đủ các luồng vào: **sửa** (chưa có) và trường mặc định d_4 (chưa có) | `[MAJOR]` |
| Q4 | `FUNC-004` | Cao | **RISK** — 5 pattern mới có biên 20 (NEW-16, NEW-18), biên+1 21 (NEW-17, NEW-23) và rỗng (NEW-14). Thiếu **biên−1 (19)** và **21 ký tự full-width** (NEW-18 chỉ chứng minh 20 Kanji lưu được, chưa chứng minh 21 Kanji bị chặn) | `[MAJOR]` |
| Q5 | `REG-SHARED-001` | Cao | **RISK** — 3 TC mang mã này (NEW-24 / 25 / 27) đều test sai đối tượng (xem G7). Nơi ảnh hưởng thật theo danh sách Dev: (a) `create.js` — đã cover bởi NEW-21 / 22 / 23 nhưng dưới mã khác; (b) mobile `FriendInfoMobileController::saveFriendInfoField` — **cùng lỗi, chưa fix** | `[MAJOR]` |

- Q1 + Q2 → TC-PERM003-01/02/03 (TC-PERM003-02 kiểm luôn DB/màn của bot B cho DATA-DB-001).
- Q3 → TC-FUNC002-01 (luồng sửa) + TC-FUNC002-02 (d_4), và đổi mã quan điểm của NEW-21 / NEW-14 sang `FUNC-002` (§4 I8).
- Q4 → không đề xuất TC mới: bổ sung dữ liệu vào NEW-16 / NEW-17 (§4 I10).
- Q5 → không đề xuất TC: mobile chưa có fix nên test sẽ fail chắc chắn. Đề nghị raise ticket (§4 I4).

**Đã loại khỏi phạm vi**:
- `FRIEND-001`: validate đặt trước nhánh xử lý theo type, fix không đổi logic từng type.
- `UI-INPUT-001` / `DEPLOY-ASSET-001`: diff chỉ 1 file PHP, không đổi JS/FE (theo `spec_delta` và mục 4.1 của Dev).
- `SEC-002`: Trigger (credential / token / payment) không khớp nghiêm ngặt. NEW-20 vẫn giữ vì chủ đề rò rỉ thông tin.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-28 (d_1 / d_2 / d_3 / d_6) | NEW-19 (chỉ d_1) → **xóa** | DUP-SUBSET | Cùng `TOOL-NEGCTRL-001` · cùng gọi EP-09 với id trường mặc định + title rỗng · cùng tiền đề admin + session · expected "không bị validate mới chặn, không SQLSTATE". Khác `Loại case` (Normal vs Abnormal) nhưng cùng ý định | `[MINOR]` |
| DUP-2 | NEW-20 (auto, dữ liệu cụ thể, mã `SEC-002`) | NEW-26 → **gộp**: đưa bước "kiểm tra application log" của NEW-26 vào NEW-20, rồi xóa NEW-26 | DUP-SUBSET | Cùng ép exception downstream trong EP-09 · cùng tiền đề · cùng expected "message chung, không SQL/stack, log vẫn ghi chi tiết" (NEW-20 ghi trong ngoặc, NEW-26 ghi thành bước). Mã khác nhau (`SEC-002` vs `OBS-001` mã lạ) | `[MINOR]` |

- **Gate đã chạy**: giả định xóa NEW-19 và NEW-26 → coverage §1 / §2 còn nguyên. NEW-28 vẫn cover d_1; NEW-20 cover F2 sau khi được gộp bước log. Tuy vậy **G2 vẫn còn**: sau khi gộp chỉ còn 1 TC trigger → cần thêm TC-SEC002-01 ở §5.
- `DUP-INFLATE`: không có.
- `DUP-CONFLICT`: không có.
- Xóa thật do human thực hiện trên Studio (`testcase_delete`).

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Tab Thông tin Studio task #211 | `spec_delta` / `dev_impact` lỗi thời: tính 2026-08-26 trên base `release_step_20260623`, chưa có commit guard `fff7807509`; requirement `REQ-006` vẫn ghi "Tag Management dùng chung endpoint". Sinh TC / review tiếp trên dữ liệu này sẽ tiếp tục sót guard | Recompute `spec_delta` trên base `release_step_20260827`; cập nhật `REQ-006` và thêm REQ cho guard chéo bot |
| I2 | `[MAJOR]` | Run #1719 (2026-09-19 05:35) | Report Dev tự mâu thuẫn: commit `fff7807509` vừa ghi "CHƯA PUSH" vừa ghi "[đã push]". Không xác định được run #1719 chạy trên code **có guard** hay không. Mục 6 VERIFY của Dev vẫn là số liệu vòng 1, mới ở mức lint | Hỏi Dev xác nhận commit HEAD của `ai_fixbug_39140`, rồi chạy lại toàn bộ bộ TC trên đúng commit đó |
| I3 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" chưa tick → F/D/T có thể thiếu hoặc map sai | Tester đọc lại Journal #137195 rồi tick |
| I4 | `[MAJOR]` | Mobile `FriendInfoMobileController::saveFriendInfoField` | Dev xác nhận cùng lỗi (thiếu validate + trả thẳng `getMessage` + **không guard bot**) nhưng xếp "ngoài phạm vi"; chưa thấy ticket theo dõi. Lỗ ghi/xoá dữ liệu chéo bot vẫn còn ở đường app | Leader raise ticket riêng cho mobile API (REG-SHARED-001) |
| I5 | `[MAJOR]` | Toàn bộ 16 TC (RULE-02) | `artifacts: []` ở cả 3 run. TC API có `actual` là body response (dùng được làm log). TC UI **NEW-21 / 22 / 23 / 24 / 25 / 27** không có screenshot nào | Runner đính kèm screenshot cho TC nhóm UI, hoặc Leader chấp nhận `actual` text làm evidence và ghi rõ |
| I6 | `[MAJOR]` | NEW-27 | Expected không đo lường được: "message 友だち情報（管理名）… **hoặc message validate tương ứng**". Thực tế màn tag trả `管理名を入力してください。` và không gửi request, nhưng TC vẫn pass → không chứng minh gì cho fix | Xóa cùng G7; nếu giữ thì expected phải ghi đúng message của màn tag |
| I7 | `[MAJOR]` | NEW-26 | Steps / dữ liệu không dựng lại được: "cố ý tạo exception ở downstream xử lý", "Payload hợp lệ nhưng tạo exception xử lý nội bộ" | Gộp vào NEW-20 (§3 DUP-2) |
| I8 | `[MINOR]` | NEW-21 · NEW-14 · NEW-19 · NEW-28 · NEW-26 | Mã quan điểm nội bộ Studio `TOOL-VAL2-001` / `TOOL-KNOW-002` / `TOOL-NEGCTRL-001` / `OBS-001` không có trong `checklist-lme.md` → không map được coverage | `testcase_update`: NEW-21 và NEW-14 → `FUNC-002`; NEW-28 → `FUNC-001` (regression); NEW-19 / NEW-26 xử lý theo §3 |
| I9 | `[MINOR]` | NEW-14 | Không replay đúng payload của ticket (`group_id:0`, `type_data:4`) — xem G6 | Thêm biến thể thứ 2 vào steps / data của NEW-14: `{id:"", title:"", group_id:0, type_data:4}` → cùng expected |
| I10 | `[MINOR]` | NEW-16 · NEW-17 | FUNC-004 thiếu biên−1 và biên+1 full-width — xem Q4 | NEW-16 thêm dữ liệu 19 ký tự; NEW-17 thêm dữ liệu 21 ký tự Kanji (vd `田中太郎佐藤鈴木高橋伊藤渡辺山本中村小林林`) |
| I11 | `[MINOR]` | NEW-20 | Steps cho phép "đối chiếu source catch block nếu không ép được exception runtime" → có thể pass mà không chạy runtime. Số dòng `~1465-1470` theo base cũ | Bỏ nhánh fallback kiểm tĩnh; cập nhật số dòng theo base `release_step_20260827` (catch :1577-1584) |
| I12 | `[MINOR]` | NEW-22 | Expected ghi "response {status:true}" nhưng actual ghi `saveResp=n/a` → phần response chưa được kiểm | Runner bắt response của request lưu, hoặc bỏ vế response khỏi expected |
| I13 | `[NIT]` | Toàn bộ | 3 run đều ở `local`; `dev` / `staging` / `prd` = 0 run. Task không thuộc RULE-08, nhưng chưa có kết quả trên môi trường deploy | Chạy lại ít nhất 1 lượt ở staging sau khi merge vào `release_step_20260827` |

---

## 5. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` (grep theo 管理名 / bot khác / 生年月日 / trường mặc định) |
| Vùng regression phát hiện từ kho | Nhóm "Sửa info" (TC-FRI-116 / 117) · "Thông tin mặc định & địa chỉ" (TC-FRI-294: trường mặc định không đổi được 管理名 nhưng cấu hình được action với 生年月日) · pattern cách ly bot ở API xóa / copy (TC-FRI-38 / 148 / 157) — **chưa có** TC cách ly bot cho API lưu định nghĩa trường |
| Conflict expected vs kho | Không. Kho MT-07 ("giới hạn 管理名 20 enforce ở đâu" — chờ quyết định) được fix này trả lời → đưa §6 |
| GAP dùng lại TC kho (không viết mới) | Không. TC-FRI-157 chỉ dùng làm mẫu thao tác "bắt request, đổi id sang bot khác" |
| Xác nhận chống trùng | Đã đối chiếu 16 TC ở BƯỚC 0 + kho FA-015 — **không TC đề xuất nào trùng**. TC-SEC002-01 khác NEW-20 ở trigger (ma trận ≥ 3 trigger + 1 trigger chưa biết) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM003-01 | UI | PERM-003 | Sửa info | Normal | auto | Tất cả | Sửa trường 選択肢 có sẵn của chính bot đang chọn rồi 保存 → lưu thành công sau khi thêm guard chủ sở hữu | - Đăng nhập admin bot A<br>- Bot A có trường 「TC39140-選択肢-&lt;timestamp&gt;」 kiểu 選択肢, 2 option 「A」「B」, có ≥ 1 bạn đã có giá trị | 1. Mở 友だち情報管理, click 管理名 của trường trên để vào màn sửa<br>2. Đổi 管理名 thành 「TC39140-sua-&lt;timestamp&gt;」, thêm option 「C」<br>3. Bấm 「保存」<br>4. Quay về danh sách, mở lại màn sửa của trường đó | 管理名 mới = 'TC39140-sua-&lt;timestamp&gt;' (≤ 20 ký tự) · option thêm = 'C' | - Lưu thành công, về danh sách, không có thông báo lỗi và không có 404 / `設定が見つかりません`<br>- Danh sách hiển thị 管理名 mới; 回答人数 không đổi<br>- Mở lại màn sửa: có đủ 3 option A / B / C | | Lấp G1, G3, Q1 · regression — luồng sửa đi qua guard mới · dẫn từ TC-FRI-116/117 · Đánh giá spec: Spec không ghi (guard là hành vi mới v3) · Evidence: screenshot danh sách + màn sửa sau khi lưu |
| TC-PERM003-02 | API | PERM-003 | Sửa info | Abnormal | auto | Tất cả | Gửi lại request lưu định nghĩa trường với id trường của BOT KHÁC → bị từ chối 404, dữ liệu bot kia không đổi | - Tài khoản admin bot A; biết id trường 「TC39140-B-選択肢」 (kiểu 選択肢, 「稼働設定」= 何度でも稼働) của bot B<br>- Trường ở bot B có option 「X」「Y」, 3 bạn đã có giá trị, 回答人数 = 3<br>- Chỉ dùng 2 bot test của QA | 1. Ở bot B: ghi lại 管理名, danh sách option, 回答人数 và giá trị của 3 bạn (màn 情報一覧)<br>2. Chuyển sang bot A, mở màn sửa 1 trường của bot A, bấm 「保存」 và bắt request `POST /basic/save-setting-info-friend`<br>3. Gửi lại request đó, đổi `id` thành id trường của bot B, `title` = 'hack', bỏ option 「Y」<br>4. Đọc HTTP status + body<br>5. Chuyển sang bot B, mở lại danh sách, màn sửa và 情報一覧 của trường đó | id = &lt;id trường bot B&gt; · title = 'hack' · option chỉ còn 'X' | - HTTP 404, body `{status:false, msg:'設定が見つかりません'}`, không có SQLSTATE / câu SQL<br>- Bot B: 管理名 vẫn 「TC39140-B-選択肢」, còn đủ option X / Y, 回答人数 vẫn = 3, 3 bạn giữ nguyên giá trị như bước 1<br>- Bot A: trường của bot A không bị đổi | | Lấp G1, Q1, Q2 · DATA-DB-001 (WHERE scope 2 bot) · MAP-PERM-03 · dẫn mẫu thao tác từ TC-FRI-157 · Đánh giá spec: Spec không ghi — theo Journal #137195 mục 4.2 · Evidence: request/response + screenshot màn bot B trước/sau |
| TC-PERM003-03 | API | PERM-003 | Sửa info | Boundary | auto | Tất cả | Tài khoản quản lý CẢ 2 bot, đang chọn bot A, gửi id trường bot B → vẫn bị chặn; chuyển sang bot B thì sửa trường đó bình thường | - 1 tài khoản là admin của cả bot A và bot B<br>- Bot B có trường 「TC39140-B-記述」 kiểu 記述<br>- Đang chọn bot A (bot context theo phiên đăng nhập) | 1. Đang ở bot A, bắt request lưu định nghĩa trường như TC-PERM003-02 bước 2<br>2. Gửi lại với `id` = id trường 「TC39140-B-記述」 của bot B, `title` = 'TC39140-B-doi'<br>3. Đọc HTTP status + body<br>4. Chuyển bot sang bot B (menu chọn bot), mở màn sửa trường đó, đổi 管理名 thành 'TC39140-B-doi', bấm 「保存」 | id = &lt;id trường bot B&gt; · title = 'TC39140-B-doi' | - Bước 3: HTTP 404 `設定が見つかりません` dù tài khoản có quyền với bot B — guard xét theo **bot đang chọn**, không theo quyền tài khoản; 管理名 ở bot B chưa đổi<br>- Bước 4: lưu thành công, danh sách bot B hiển thị 'TC39140-B-doi' | | Lấp G1, Q1 · MAP-PERM-01 (tài khoản thuộc nhiều bot) · Đánh giá spec: Spec không ghi — cần Dev xác nhận guard xét theo bot trong phiên · Evidence: response bước 3 + screenshot danh sách bot B |
| TC-FUNC002-01 | API | FUNC-002 | Sửa info | Abnormal | auto | Tất cả | Lưu định nghĩa trường có sẵn (luồng sửa) với 管理名 rỗng → trả message nghiệp vụ, 管理名 cũ giữ nguyên | - Đăng nhập admin bot A<br>- Bot A có trường 「TC39140-edit-rong」 kiểu 記述 | 1. Mở màn sửa trường 「TC39140-edit-rong」, bấm 「保存」 và bắt request `POST /basic/save-setting-info-friend`<br>2. Gửi lại request, giữ nguyên `id`, đổi `title` = ''<br>3. Đọc body<br>4. Mở lại danh sách 友だち情報管理 | id = &lt;id trường bot A&gt; · title = '' | - HTTP 200 `{status:false, msg:'友だち情報（管理名）を1つ以上設定して下さい。'}`, không SQLSTATE / câu SQL / tên bảng<br>- Danh sách vẫn hiển thị 管理名 「TC39140-edit-rong」 | | Lấp G5, Q3 · luồng vào "sửa" của FUNC-002 · Đánh giá spec: Spec không ghi (spec chỉ ghi validate client) · Evidence: response + screenshot danh sách |
| TC-FUNC001-01 | UI | FUNC-001 | Thông tin mặc định & địa chỉ | Normal | auto | Tất cả | Cấu hình action cho trường mặc định 生年月日 rồi 保存 → lưu thành công, không bị validate 管理名 mới chặn | - Đăng nhập admin bot A<br>- Bot A có 1 tag 「TC39140-誕生日」 | 1. Mở 友だち情報管理, vào folder thông tin cơ bản, click 「生年月日」<br>2. Thêm 1 cấu hình action: 月日, 0 日 後, 09:00, action = gắn tag 「TC39140-誕生日」<br>3. Bấm 「保存」<br>4. Mở lại màn 生年月日 | Action: 月日 · 0日後 · 09:00 · gắn tag 'TC39140-誕生日' | - Lưu thành công, không hiện 「友だち情報（管理名）を1つ以上設定して下さい。」 hay message lỗi hệ thống<br>- 管理名 「生年月日」 không đổi; mở lại màn thấy đúng cấu hình action vừa lưu | | Lấp G4 · regression d_4 — trường mặc định đi qua validate mới · dẫn từ TC-FRI-294 · Đánh giá spec: Spec ghi rõ (BR-10, TC-FRI-294) · Evidence: screenshot màn 生年月日 sau khi mở lại |
| TC-FUNC002-02 | API | FUNC-002 | Thông tin mặc định & địa chỉ | Abnormal | auto | Tất cả | Gọi thẳng API lưu trường mặc định 生年月日 (d_4) với 管理名 rỗng → bị chặn, cấu hình action cũ giữ nguyên | - Đăng nhập admin bot A<br>- Trường 生年月日 đã có cấu hình action từ TC-FUNC001-01 | 1. Mở màn 「生年月日」, bấm 「保存」 và bắt request `POST /basic/save-setting-info-friend`<br>2. Gửi lại request với `id` = 'd_4', `title` = '', xóa hết cấu hình action trong payload<br>3. Đọc body<br>4. Mở lại màn 「生年月日」 | id = 'd_4' · title = '' | - HTTP 200 `{status:false, msg:'友だち情報（管理名）を1つ以上設定して下さい。'}`, không SQLSTATE<br>- Màn 生年月日 vẫn còn cấu hình action của TC-FUNC001-01 (request bị chặn trước khi ghi) | | Lấp G4, Q3 · Đánh giá spec: Spec không ghi — theo Journal #137195 mục 4.2 (`action_info_friend_default.title` cùng được chặn) · Evidence: response + screenshot màn 生年月日 |
| TC-SEC002-01 | API | SEC-002 | Tạo info — chung | Abnormal | auto | Tất cả | Ma trận trigger lỗi hệ thống khi lưu định nghĩa trường → luôn trả message sạch, không bao giờ lộ SQLSTATE / SQL / stack | - Đăng nhập admin bot A, có CSRF + session hợp lệ<br>- Truy cập được application log của môi trường test | 1. Ở màn tạo mới trường, nhập 管理名 hợp lệ, bấm 「保存」 và bắt request `POST /basic/save-setting-info-friend`<br>2. Gửi lại request lần lượt với 4 biến thể ở cột Dữ liệu nhập (mỗi lần 管理名 khác nhau)<br>3. Với mỗi lần: đọc body, sau đó xem danh sách 友だち情報管理 có sinh trường mới không<br>4. Mở application log, tìm mốc `saveSettingInfoFriend failure >>` | (a) `group_id` = 'abc' · (b) `setting_actions` = chuỗi JSON hỏng `{"x":` · (c) `type_data` = 99 · (d) trigger chưa biết: `option_value` dài 300 ký tự với type 選択肢 · 管理名 = 'TC39140-err-a/b/c/d' | - Mỗi biến thể: body chỉ là message nghiệp vụ hoặc `システムエラーが発生しました。\n管理者へ問い合わせください。`; **không** chứa `SQLSTATE`, `insert into`, `friend_information_setting`, đường dẫn file hay stack trace<br>- Biến thể trả lỗi thì không sinh trường mới ở danh sách<br>- Biến thể trả message chung thì log có chi tiết exception tương ứng | | Lấp G2 · generic catch: ≥ 3 trigger + 1 trigger chưa biết (d) · khác NEW-20 ở tập trigger · biến thể nào lưu thành công thì ghi nhận để Dev xác nhận, không tự kết luận là bug · Đánh giá spec: Spec không ghi · Evidence: 4 response + đoạn log |

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/friend-information/feature-spec.md` — bảng field dòng 389 (「管理名」 "Max 20 ký tự (client)") + luồng EP-09 | Server cũng validate: 管理名 bắt buộc → 「友だち情報（管理名）を1つ以上設定して下さい。」; > 20 ký tự (`mb_strlen`) → 「友だち情報（管理名）は20文字以内で入力してください。」; áp dụng cho trường tự tạo và `d_4`, không áp dụng `d_1` / `d_2` / `d_3` / `d_6`. Chốt luôn kho FA-015 **MT-07** (giới hạn enforce ở đâu) | Journal #137195 vs spec "client only" · kho MT-07 đang chờ quyết định | Dev / Leader |
| 2 | Luồng EP-09 `POST /basic/save-setting-info-friend` | Thêm bước guard chủ sở hữu ở đầu hàm: id của bot khác → HTTP 404 `{status:false, msg:'設定が見つかりません'}`; id rỗng / `d_x` / id âm cho qua | Hành vi mới v3, spec chưa có | Dev |
| 3 | Luồng EP-09 — xử lý lỗi | Mọi exception trả `システムエラーが発生しました。\n管理者へ問い合わせください。`, chi tiết ghi log mốc `saveSettingInfoFriend failure >>` (đổi hợp đồng field `msg`) | Journal #137195 mục 4.2 | Dev |
| 4 | Studio task #211 — requirements | `REQ-006` ("Tag Management dùng chung endpoint") sai theo đính chính v3 → sửa / vô hiệu; thêm requirement cho guard chéo bot | Journal #137195 (3) vs `REQ-006` | Leader |
