# 05 — Review Report (lượt 2)

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **MCP LME TEST STUDIO** — task #233 (ticket #33762), round 3, status `done` |
| Tổng số TC review | **25** |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

> **Chiều `dev-impact` (file 03): CHƯA ĐỦ** — `03-dev-impact.md` vẫn mô tả bản fix gốc *"đúng 2 file, 2 dòng đổi"*. Diff thật hiện tại là **4 file / 478 dòng**, gộp thêm **#40253** (chuẩn hoá nửa đêm) và **#40876** (update-flow lesson + salon), cộng **1 command hoàn toàn mới**. File 03 không còn phản ánh phạm vi đang test.
>
> **Chiều `diff code` (Studio `spec_delta`, `diffAvailable = true`): CHƯA ĐỦ** — `RecoverRemindAfterEndBooking.php` là file **mới 435 dòng**, chiếm **91% toàn bộ diff**, và có **0 TC**. 5 requirement của riêng nó (`REQ-107`…`REQ-111`, 2 mức High) đều trống.

**Kết luận: 6/16 vùng ảnh hưởng đủ TC · 6 GAP · 4 RISK.**

| # | Vùng ảnh hưởng | Chiều | TC cover | Status | Severity |
|---|---|---|---|---|---|
| G1 | `RecoverRemindAfterEndBooking.php` — command `recover:remind-after-end` (435 dòng mới, xoá + sửa + tạo lại `event_step_time`) | `diff code` | không có | `GAP` — `REQ-107` (dry-run mặc định, **High**) · `REQ-108` (xoá/sửa/giữ đúng, **High**) · `REQ-109` · `REQ-110` · `REQ-111` đều **0 TC**. Hai kết quả manual duy nhất chạm tới nó (*"Recover theo case 17"*) là **`blocked`** trên `prd` và **`skip`** trên `staging`, không gắn TC nào ⇒ chưa từng được kiểm chứng. Đây là đoạn code **ghi đè dữ liệu hàng loạt**, rủi ro cao nhất của cả task | `[BLOCKER]` |
| G2 | Phạm vi `WHERE` khi command chạy `--apply` | `diff code` | không có | `GAP` — chính `dev_impact` của Studio đặt đây là rủi ro cần test kỹ: *"command recover phải chạy dry-run trước, --apply đúng phạm vi WHERE (status=0, đúng bot/calendar), không đụng bản ghi đã gửi"*. Không TC nào dựng 2 bot rồi xác nhận bot B không bị chạm | `[BLOCKER]` |
| G3 | Bước **tạo lại** lịch gửi bị thiếu (`REQ-109`) chạy trên dữ liệu cũ | `diff code` | không có | `GAP` — command tạo lại bản ghi ở trạng thái chưa gửi cho lượt đặt còn hiệu lực. Trên môi trường thật, bước này có thể sinh hàng loạt lịch gửi cho booking cũ ⇒ khách nhận loạt remind quá hạn + tiêu thụ quota tin nhắn. Không TC nào đo số bản ghi tạo ra và hệ quả gửi | `[MAJOR]` |
| G4 | Command `--apply` chạy **đồng thời** với job gửi remind | `diff code` | không có | `GAP` — job `NewEventRemindTask` quét `status = 0` rồi đổi sang `status = 1` trước khi gửi; spec **BR-41** ghi rõ bản ghi đã `status = 1` **vẫn sẽ được gửi**. Command xoá/sửa trong lúc job đang nhặt là cửa sổ đua thật. `REQ-110` chỉ phủ chạy lại 2 lần tuần tự, không phủ đồng thời | `[MAJOR]` |
| G5 | Phạm vi lọc theo ngày của command (`REQ-111`) | `diff code` | không có | `GAP` — requirement tự ghi: *"Tham số giới hạn theo ngày chỉ áp cho bước tạo lại; bước rà bản ghi đang có vẫn duyệt và xoá bản ghi chưa gửi của lượt đặt đã qua"* và *"cần leader xác nhận đây là chủ ý hay thiếu điều kiện lọc"*. Chưa có TC ghi nhận hiện trạng để leader quyết → xem §8 | `[MAJOR]` |
| G6 | Bản vá **#40876** (update-flow lesson + salon) trên **production** | `diff code` | `NEW-29` · `NEW-30` · `NEW-31` · `NEW-33` · `NEW-35` · `NEW-36` (chỉ `staging`) | `RISK` — đợt chạy production duy nhất là **2026-09-14**, trước khi 8 TC của #40876 được tạo (**2026-09-17**). Toàn bộ nhóm update-flow chưa từng chạy trên `prd` | `[MAJOR]` |
| G7 | `03-dev-impact.md` so với diff thật | `dev-impact` | — | `RISK` — file 03 thiếu hẳn `F*`/`D*`/`T*` cho #40253, #40876 và command recover. Mọi kết luận coverage theo chiều (a) của lượt này phải dựa vào `dev_impact` của Studio thay cho file 03 | `[MAJOR]` |
| G8 | Deploy khi `event_step_time` còn bản ghi `status = 0` / `status = 1` | `diff code` | không có | `RISK` — bản vá đổi cách ghi + lệnh recover cùng lên một lượt. Kho đã có sẵn `TC-LSN-413` cho đúng tình huống này, chưa được dẫn vào bộ TC | `[MAJOR]` |
| G9 | Lối **app quản trị mobile** | `diff code` | `NEW-26` (thêm booking) | `RISK` — chỉ còn 1 lối trên app. Lối *duyệt yêu cầu trên app* đã được **Leader quyết loại ở lượt 1** (ghi ở §5 report lượt 1) — nêu lại để giữ dấu vết, **không đề xuất lại** | `[MINOR]` |

| G10 | **Ma trận biên mốc gửi** theo spec Leader chốt (§8 mục 6): `コース開始前` neo `start_time`, `コース終了後` neo `end_time`; mỗi khối × 2 kiểu (`日時で指定` / `経過時間で指定`) × các mốc biên | `diff code` | 4/18 ô có TC | `GAP` — bảng đối chiếu ngay dưới | `[BLOCKER]` |

**Bảng đối chiếu ma trận biên — 4/18 ô có TC**

| Khối | Kiểu | Ô biên | TC hiện có | Trạng thái |
|---|---|---|---|---|
| `コース開始前` (neo `start_time`) | `日時で指定` | `day = 0` | `NEW-5` (09:00 hợp lệ, 15:00 không hợp lệ) | ✅ |
| | | `day ≠ 0` | — | ❌ |
| | | giờ `00:00` | — | ❌ |
| | | giờ `23:59` | — | ❌ |
| | | giờ `00:01` | — | ❌ |
| | `経過時間で指定` | `0h00` | — | ❌ |
| | | `0h01` | — | ❌ |
| | | `23h59` | — | ❌ |
| `コース終了後` (neo `end_time`) | `日時で指定` | `day = 0` | `NEW-3` · `NEW-10` · `NEW-11` · `NEW-13` · `NEW-14` · `NEW-18` · `NEW-19` · `NEW-26` | ✅ |
| | | `day ≠ 0` | `NEW-20` (day=1, day=3) · `NEW-17` (day=1) | ✅ |
| | | giờ `00:00` | `NEW-34` (0 ngày / 1 ngày lúc 00:00) · `NEW-19` | ✅ |
| | | giờ `23:59` | — | ❌ |
| | | giờ `00:01` | — | ❌ |
| | `経過時間で指定` | `0h00` | — | ❌ ⚠️ chính là biên `mốc gửi = end_time` đang tranh chấp ở §4 `CONF-TC-01` |
| | | `0h01` | — | ❌ |
| | | `23h59` | — | ❌ |
| `salon` | — | booking **qua ngày**, mốc thoả | — | ❌ |
| | — | booking **qua ngày**, mốc không thoả | — | ❌ |

> TC `経過時間` hiện có (`NEW-27` · `NEW-32` · `NEW-33`) đều dùng đúng **một** giá trị `1 giờ`, không phải giá trị biên. TC salon hiện có (`NEW-35` · `NEW-36`) chạy trên khung `12:00 - 17:00` trong ngày, không phải booking qua ngày.

**Vùng đủ TC (không ghi chi tiết):** add-flow EP-69 · add-flow EP-41 · EP-42 duyệt đơn · EP-P12 khách LINE tự đặt · update-flow EP-73 lesson (`REQ-101`/`REQ-102`) · update-flow EP-73 salon (`REQ-105`).

> **Đã đóng so với lượt 1**: `EP-73` (Studio từng chấm `level = none`, nay `partial` với 4 TC) · khung nửa đêm `REQ-103`/`REQ-104` · salon đối chứng · `MSG-002` chuỗi gửi tới LINE · production đã có 13 TC chạy thật ngày 14/09 (`envAuto[prd].runs = 0` chỉ đếm run **auto**, không phản ánh manual).

---

## 2. Thiếu so với quan điểm test

**Kết luận: 14 quan điểm Trigger khớp task · 4 đủ · 6 GAP · 4 RISK.**

Phạm vi tính năng chốt trước khi quét (BƯỚC 3a), đối chiếu bảng *Coverage theo màn hình/chức năng* của `kho-tcs/fa019-datlichbaihoc-レッスン予約.md`: nhóm **29 リマインド — cài đặt** · **30 リマインド — job gửi & recover** · **16 Admin thêm booking thủ công** · **7 Tab 本日/新着の予約** · **20 受付枠 — thêm khung giờ** · **42–43 LINE user** · **48 App mobile** · **50 Phân quyền & môi trường**. Bốn hướng đọc: **web** (đủ) · **app quản trị di động** (G9) · **job nền** (Q1–Q4 dưới đây) · **export & tích hợp ngoài** — nhóm **36 Googleスプレッドシート連携** loại trừ vì command chỉ chạm `event_step_time`, không chạm bản ghi booking được đẩy lên Sheet.

| # | Mã quan điểm | Ưu tiên | Tình trạng | Severity |
|---|---|---|---|---|
| Q1 | `JOB-001` ★ — Job nền / batch | Cao | `GAP` — Trigger: *"BẮT BUỘC khi tính năng thêm/sửa job nền"*. Task **thêm mới** một command batch 435 dòng; Studio tự xếp `REQ-107`…`REQ-111` vào category `job`. 0 TC nào chạm command | `[BLOCKER]` |
| Q2 | `DATA-DB-001` ★ — WHERE scope + khoá mồ côi | Cao | `GAP` — Trigger: *"BẮT BUỘC với mọi chức năng có UPDATE hoặc DELETE"*. Command xoá + sửa + chèn hàng loạt. Checklist đòi dựng bản ghi ở **2 tài khoản** rồi xác nhận tài khoản B không đổi — chưa có TC nào | `[BLOCKER]` |
| Q3 | `CONC-001` — Đồng thời & Idempotency | Cao | `GAP` — Trigger: *"BẮT BUỘC khi có nút thực thi hành động quan trọng … / batch đa luồng"*. `--apply` và job gửi cùng đọc-ghi `event_step_time`. Xem G4 | `[MAJOR]` |
| Q4 | `REG-RUN-001` — Dữ liệu / job đang chạy dở khi release | Cao | `GAP` — Trigger: *"BẮT BUỘC với mọi release khi hệ thống có job/dữ liệu đang chạy dở"*. Xem G8; kho có `TC-LSN-413` | `[MAJOR]` |
| Q5 | `MSG-005` — Tiêu thụ quota tin nhắn | Cao | `GAP` — bước tạo lại của command (`REQ-109`) sinh thêm lịch gửi ⇒ thêm tin thật ⇒ tăng `free_send_count` của bot. Không TC nào đo. Xem G3 | `[MAJOR]` |
| Q6 | `ENV-003` ★ — Khác biệt dev / staging / production | Cao | `RISK` — production đã chạy thật 13 TC (14/09) nên **không còn là GAP như lượt 1**, nhưng toàn bộ nhóm #40876 và command recover chưa lên `prd`. Trigger *"chạm … job nền"* vẫn đang mở | `[MAJOR]` |
| Q7 | `COMPAT-LEGACY-001` ★ — Dữ liệu đời cũ chạy song song | Cao | `RISK` — Trigger liệt kê đích danh **`remind`**. `NEW-17` đã nâng cấp (biết quy nửa đêm sang ngày kế tiếp) nhưng vẫn chỉ **đếm** bản ghi sai. Chưa có TC dựng song song 2 thế hệ dữ liệu rồi chạy command lên cả hai — kho có `TC-LSN-415` | `[MAJOR]` |
| Q8 | `FUNC-004` — Giới hạn trên/dưới | Cao | `RISK` — 3 TC nhưng **cả 3 đều đứng trên một giả định đang tranh chấp** (biên `=` giờ kết thúc, xem §4 `CONF-TC-01`). Nếu chốt lại theo hướng ngược thì cả 3 expected phải sửa. Ngoài ra mã vẫn gắn nhầm: Trigger `FUNC-004` là *"giới hạn số lượng / ký tự / dung lượng"*, còn nội dung là biên thời gian ⇒ thuộc `FUNC-DATE-001` | `[MAJOR]` |
| Q9 | `SYNC-APP-001` — Web và app song song | Trung bình | `RISK` — xem G9, Leader đã quyết loại lối duyệt đơn trên app ở lượt 1 | `[MINOR]` |
| Q10 | `FUNC-DATE-001` ★ — Ngày giờ sát ranh giới | Cao | `GAP` — đối chiếu **ma trận biên do Leader chốt** (§8 mục 6) với 25 TC: chỉ **4/18 ô** có TC. Khối `コース開始前` gần như bỏ trống (1/8 ô); biên giờ **23:59** và **00:01** không xuất hiện ở bất kỳ TC nào của cả hai khối; kiểu `経過時間で指定` chưa có ô biên nào (`0h00`, `0h01`, `23h59`). Xem bảng đối chiếu ở G10 | `[BLOCKER]` |

> **Đã đủ, không ghi dòng**: `FUNC-001` · `MSG-002` (3 TC chạy thật trên `prd`, đi tới LINE app) · `STATE-DEP-001` (3 TC) · `REG-SHARED-001` (5 TC gồm salon).
>
> ⚠️ **Đính chính so với bản đầu của lượt 2**: `FUNC-DATE-001` ban đầu được chấm **đủ** (5 TC). Sau khi Leader cung cấp ma trận biên chuẩn, đánh giá lại thành **GAP `[BLOCKER]`** — 5 TC hiện có chỉ chạm 4/18 ô.

---

## 3. TC trùng lặp nội dung

Đã rà **25/25 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`) — **không phát hiện trùng lặp cần xoá hoặc gộp**.

| Cụm nghi trùng | TC | Vì sao KHÔNG phải trùng |
|---|---|---|
| Mốc `15:00 < 17:00` → không lập lịch | `NEW-10` · `NEW-13` · `NEW-14` · `NEW-26` | 4 **lối vào khác nhau** của cùng `addActionRemind`: thêm booking (EP-41) · duyệt đơn (EP-42) · khách LINE tự đặt (EP-P12) · app mobile. `REG-SHARED-001` yêu cầu *"test lại **từng mục**"* trong danh sách nơi ảnh hưởng |
| Mốc `= 17:00` → vẫn lập lịch | `NEW-3` · `NEW-11` · `NEW-30` | `NEW-3`/`NEW-11` là **add-flow** (EP-69 / EP-41); `NEW-30` là **update-flow** (EP-73, bấm lưu lại). Khác hàm, khác ticket |
| Khung nửa đêm 22:00~24:00 | `NEW-19` · `NEW-32` · `NEW-33` · `NEW-34` | `NEW-19` kiểu ngày add-flow · `NEW-32` đếm ngược add-flow · `NEW-33` đếm ngược **update-flow** · `NEW-34` so 2 cách chọn 0 ngày / 1 ngày (`REQ-106`, ghi nhận hạn chế). Bốn điểm dữ liệu khác nhau |
| Salon update-flow | `NEW-35` · `NEW-36` | Hai nửa đối nhau của `REQ-105`: `NEW-35` sửa xuống 15:00 → **xoá**; `NEW-36` sửa lên 18:00 → **tạo lại**. Xoá bất kỳ bên nào là mất một chiều |

⚠️ Không phải trùng, nhưng là **rủi ro tập trung**: 5 TC (`NEW-3` · `NEW-11` · `NEW-30` · `NEW-35` · `NEW-36`) cùng khẳng định *"biên bằng đúng giờ kết thúc là hợp lệ"*. Nếu §4 `CONF-TC-01` chốt theo hướng ngược lại thì **cả 5 pass hiện tại đều thành false pass** cùng lúc.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | Nội dung | Hai khả năng — **chưa chọn bên** |
|---|---|---|---|
| CONF-TC-01 | `CONF-TC` | **Biên `mốc gửi = giờ kết thúc`.** `NEW-3` · `NEW-11` · `NEW-30` · `NEW-35` · `NEW-36` đều kỳ vọng **CÓ** tạo bản ghi lịch gửi và đều `pass`. Ngược lại `NEW-23` kỳ vọng khách **nhận được tin** ở đúng biên đó, chạy `staging` 2026-09-14 02:03 → **fail**, actual ghi: *"Trên step cũng đang ko tạo bản ghi event_step_time trùng đúng time end"*. Cùng một quy tắc, hai quan sát loại trừ nhau | **(a)** quan sát trên `staging` sai / lệch môi trường ⇒ `NEW-23` cần chạy lại và ghi rõ env · **(b)** 5 TC kia là false pass ⇒ sản phẩm thật sự loại bỏ biên bằng nhau, và 5 expected phải viết lại |
| CONF-SPEC-01 | `CONF-SPEC` | Bug `#1046` → Redmine **#40899** sinh từ `NEW-23` bị **rejected** với lý do nguyên văn **`"Không bị lỗi"`**. Nhưng `REQ-004` của chính task ghi: *"Mốc gửi trùng đúng giờ kết thúc **vẫn được lập lịch** … Đây là biên của điều kiện loại bỏ."* Chấp nhận *"không tạo bản ghi ở biên bằng nhau"* là đúng thì `REQ-004` đang sai | **(a)** lý do reject đúng ⇒ phải sửa `REQ-004` + 5 TC ở trên · **(b)** `REQ-004` đúng ⇒ #40899 bị đóng nhầm, cần mở lại |
| CONF-KHO-01 | `CONF-KHO` | Tồn tại **hai lệnh recover cùng một loại dữ liệu**: kho FA-019 có `TC-LSN-409` — *"Support #33648: command `recover:remindLesson` — nhánh step gửi TRƯỚC không đổi"* (kèm `TC-LSN-410`/`411`/`412`); task này thêm command **mới** `recover:remind-after-end` (`RecoverRemindAfterEndBooking.php`). Cả hai cùng nhắm `event_step_time` của remind gửi-sau | **(a)** command mới thay thế command cũ ⇒ phải gỡ/đánh dấu lỗi thời `recover:remindLesson` và cập nhật `TC-LSN-409`…`412` của kho · **(b)** hai command phục vụ hai phạm vi khác nhau ⇒ phải ghi rõ ranh giới, vì chạy nhầm cái kia lên cùng dữ liệu là rủi ro thật |

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | `NEW-30` (Studio #18689) | **Fail sản phẩm bị đóng bằng manual pass, không raise ticket.** Run auto `#2051` (`staging`, 2026-09-25 01:51) chấm **fail** với bằng chứng tự kiểm: *"Sau khi bấm 保存 (không đổi gì): có 0 mốc gửi …, mong đợi đúng 1. Mã bản ghi ĐÃ ĐỔI/BIẾN MẤT … Đọc lại bằng phiên mới (độc lập với luồng test vừa chạy): []"*. Đây **không phải lỗi hạ tầng** — đúng hiện tượng của #40876 mục 2. Run `#2057` sau đó **chỉ chạy 1 TC là `NEW-35`**, không chạy lại `NEW-30`. Trạng thái `pass` hiện tại đến từ **manual result lúc 02:45:47, `by = null`, không note, không bug** | Chạy lại `NEW-30` trên `staging` và ghi người thực hiện. Nếu tái hiện → raise ticket ngay; nếu không → ghi triage giải thích vì sao lượt auto fail. `REQ-101` là mức **High**, không được đóng bằng pass không người ký |
| 2 | `[MAJOR]` | `NEW-32` · `NEW-33` · `NEW-34` · `NEW-36` (#18691/18692/18693/18695) | Bốn TC `error` ở run `#2051` (lỗi selector 「22:00~翌00:00」, trạng thái bẩn, URL fetch sai) cũng được đóng bằng **manual pass cùng khung 02:45–03:15, `by = null`, không note**. Lỗi hạ tầng thì re-run auto là hợp lệ, nhưng ở đây không có lượt auto nào chạy lại — chỉ có manual không ký tên | Chạy lại bằng auto sau khi sửa selector/dọn state, hoặc ghi rõ người chạy manual + bằng chứng cho từng TC |
| 3 | `[MAJOR]` | `03-dev-impact.md` | File 03 **lạc hậu**: vẫn ghi *"đúng 2 file, 2 dòng đổi"*, mục 4.1 chỉ có 2 file, không có #40253, không có #40876, không có command recover 435 dòng. Mục 5 còn đề xuất *"rà bằng câu SELECT … rồi xoá nếu xác nhận sai"* trong khi command tự động đã được viết | Yêu cầu Dev cập nhật file 03 theo diff hiện tại (4 file), bổ sung `F*`/`D*`/`T*` cho command recover trước khi đóng phiếu |
| 4 | `[MAJOR]` | `NEW-22` · `NEW-23` · `NEW-24` · `NEW-26` | 4 TC có `requirement_keys` **rỗng** → không xuất hiện trong lưới coverage của Studio. Đây đúng nhóm TC phủ chuỗi gửi tới LINE app thật (`MSG-002`) và lối app mobile — tức phần khó nhất lại không được tính vào coverage | Gắn `requirement_keys` cho 4 TC; nếu chưa có requirement tương ứng cho chuỗi gửi thật thì tạo mới |
| 5 | `[MAJOR]` | Coverage Studio | `summary` = **0/26 `covered`**, 26 `partial`. Không ref nào đạt mức phủ đủ dù đã 3 round | Rà lại từng ref `partial`, xác định còn thiếu chiều nào |
| 6 | `[MINOR]` | Vòng đời TC | **TC phát hiện bug lại bị gỡ khỏi bộ — lặp lại lần 2.** Lượt 1: `tc-13766` (sinh #40253) biến mất. Lượt này: `NEW-25` — TC đề xuất ở lượt 1, đã **sinh ra bug #1025 → Redmine #40876** — và `NEW-28` đều không còn trong 25 TC hiện tại. Coverage EP-73 nay do `NEW-29`/`31`/`33` gánh nên không thủng, nhưng nếp làm việc này khiến case đắt giá nhất rơi khỏi bộ regression | Giữ lại TC đã từng bắt bug trong bộ (RULE-12 mục 3: *"mọi case đã từng Không đạt và được fix"*) |
| 7 | `[MINOR]` | Task #233 | `status = done` nhưng `reviewed = false`, `reviewState = leader` — đã chuyển xong trong khi chưa có vòng duyệt nào của Leader | Duyệt trên Studio sau khi xử lý §1/§2/§4 |
| 8 | `[MINOR]` | Manual results | 3 kết quả manual **không gắn TC nào** (`tcId = null`), trong đó 2 dòng *"Recover theo case 17"* (`blocked` trên `prd`, `skip` trên `staging`) và 1 dòng fail 2026-09-11. Kết quả không gắn TC thì không vào được coverage và không truy vết được | Gắn về TC tương ứng, hoặc tạo TC cho command recover (§7) rồi chấm lại |

> **Anti-pattern**: `[AP-3]` Happy-path-only regression — dính ở G3: bước tạo lại của command chỉ được mô tả ở happy path, không có TC cho trạng thái biên (booking đã qua, booking đã huỷ, bản ghi đang `status = 1`).
> Không dính AP-1 · AP-2 · AP-4 (có `diffStat` đầy đủ từ Studio) · AP-5 · AP-6.
> **Spec**: đã dùng `spec-features/admin/lesson-booking/feature-spec.md` §4.5 + §8.7 (BR-37…BR-43, BR-P30) — không phát sinh dòng thiếu spec.

---

## 6. TCs thừa / ngoài phạm vi task

**Không có TC nào đủ điều kiện flag.**

Đã chạy gate 3 điều kiện trên cả 25 TC — không TC nào thoả đồng thời cả ba:

| TC từng nghi | Vì sao **không** flag |
|---|---|
| `NEW-5` (mốc gửi **trước** khi bắt đầu — đối chứng âm) | Map `REQ-005`; `dev_impact` nêu đích danh *"nhánh gửi-trước (is_after_day=0) … KHÔNG đổi"* ⇒ nằm trong rủi ro hồi quy Studio tự kê; Trigger `REG-SHARED-001` khớp |
| `NEW-27` (mốc gửi kiểu đếm ngược) | Map `REQ-005` + `REQ-104`; `dev_impact` nêu *"type_remind=2 (đếm ngược) KHÔNG đổi"*; sau đó #40876 mục 2 chứng minh nhánh này **có** hồi quy thật ⇒ càng thuộc phạm vi |
| `NEW-17` (rà soát dữ liệu cũ) | Map `REQ-010`; là trục bản-ghi-cũ của một bản vá ở tầng ghi |
| `NEW-22` · `NEW-23` · `NEW-24` (chuỗi gửi tới LINE app) | `requirement_keys` rỗng (đã ghi ở §5 mục 4) nhưng map thẳng `T2 — Reminder Delivery` của file 03 và Trigger `MSG-002` khớp ⇒ thiếu **nhãn**, không thừa **nội dung** |

Không TC nào test layer không bị chạm code.

---

## 7. TCs đề xuất bổ sung (10)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` — nhóm **30 リマインド — job gửi & recover** (19 TC) và nhóm **29 リマインド — cài đặt** (16 TC) |
| Vùng regression phát hiện từ kho | `TC-LSN-409` *"Support #33648: command `recover:remindLesson` — nhánh step gửi TRƯỚC không đổi"* · `TC-LSN-413` *"Restart job gửi remind trong lúc đang có bản ghi status = 1"* · `TC-LSN-415` *"Dữ liệu tạo TRƯỚC và SAU spec change #32367 cùng tồn tại"* |
| Conflict expected vs kho | **Có** — `CONF-KHO-01` ở §4: hai command recover cùng nhắm một loại dữ liệu. Đã đưa vào §8, **không tự chọn bên** |
| GAP dùng lại TC kho (không viết mới) | `G8`/`Q4` → **`TC-LSN-413`** · `Q7` → **`TC-LSN-415`** (đổi mốc so sánh sang ngày deploy `ai_fixbug_33762`) |
| Xác nhận chống trùng | Đã đối chiếu **25 TC** ở BƯỚC 0 + kho FA-019 — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNCDATE001-04 | UI | FUNC-DATE-001 | リマインド — cài đặt | Boundary | auto | Tất cả | Mốc gửi TRƯỚC khi bắt đầu, kiểu ngày 0 ngày — quét 3 mốc giờ biên 00:00 / 00:01 / 23:59 | - Khung tiếp nhận NGÀY MAI 12:00 - 17:00, có 1 lượt đặt đang hiệu lực<br>- Khối 「コース開始前」 chưa có mốc gửi nào | 1. Vào 「予約前後に送るリマインドメッセージ」 → khối 「コース開始前のメッセージ・アクション」<br>2. Thêm mốc 「日時で指定」, số ngày = 0, giờ 00:00, lưu, tra lịch gửi của lượt đặt<br>3. Xoá mốc vừa tạo, lặp lại với giờ 00:01, tra lịch gửi<br>4. Xoá mốc, lặp lại với giờ 23:59, tra lịch gửi<br>5. Ghi lại thời điểm gửi của từng lần | Khung ngày mai 12:00 - 17:00. Mốc gửi trước khi bắt đầu, 0 ngày, lần lượt 00:00 / 00:01 / 23:59 | Mốc 00:00 và 00:01 đều sớm hơn giờ bắt đầu 12:00 ⇒ mỗi lần tạo đúng 1 bản ghi lịch gửi, thời điểm gửi đúng bằng giờ đã chọn của ngày đặt lịch. Mốc 23:59 muộn hơn giờ bắt đầu 12:00 ⇒ KHÔNG tạo bản ghi nào. Cả 3 lần đều neo theo start_time, không dính dáng giờ kết thúc 17:00 |  | Lấp `G10` · `Q10` · Đánh giá spec: Spec ghi rõ (Leader chốt §8 mục 6) · Evidence: kết quả tra lịch gửi của 3 lần |
| TC-FUNCDATE001-05 | UI | FUNC-DATE-001 | リマインド — cài đặt | Normal | auto | Tất cả | Mốc gửi TRƯỚC khi bắt đầu, kiểu ngày N ngày khác 0 — mốc giờ biên vẫn neo theo giờ bắt đầu | - Khung tiếp nhận NGÀY KIA (cách hôm nay 2 ngày) 12:00 - 17:00, có 1 lượt đặt đang hiệu lực<br>- Khối 「コース開始前」 chưa có mốc gửi nào | 1. Thêm mốc 「日時で指定」 khối 「コース開始前」, số ngày = 1, giờ 23:59, lưu, tra lịch gửi<br>2. Xoá mốc, lặp lại với số ngày = 1, giờ 00:01, tra lịch gửi<br>3. Ghi lại thời điểm gửi của từng lần | Khung ngày kia 12:00 - 17:00. Mốc trước khi bắt đầu: 1 ngày lúc 23:59, rồi 1 ngày lúc 00:01 | Cả 2 mốc đều tạo đúng 1 bản ghi lịch gửi, thời điểm gửi rơi vào ngày trước ngày đặt lịch lúc 23:59 và 00:01 — đều sớm hơn giờ bắt đầu nên hợp lệ. Xác nhận số ngày khác 0 cũng neo theo start_time, không bị chặn nhầm |  | Lấp `G10` · `Q10` · Đánh giá spec: Spec ghi rõ (Leader chốt §8 mục 6) · Evidence: kết quả tra lịch gửi của 2 lần |
| TC-FUNCDATE001-06 | UI | FUNC-DATE-001 | リマインド — cài đặt | Boundary | auto | Tất cả | Mốc gửi TRƯỚC khi bắt đầu, kiểu thời gian trôi qua — quét biên 0h00 / 0h01 / 23h59 | - Khung tiếp nhận NGÀY MAI 12:00 - 17:00, có 1 lượt đặt đang hiệu lực<br>- Khối 「コース開始前」 chưa có mốc gửi nào | 1. Thêm mốc 「経過時間で指定」 khối 「コース開始前」 với 0 giờ 0 phút, lưu, tra lịch gửi<br>2. Xoá mốc, lặp lại với 0 giờ 1 phút, tra lịch gửi<br>3. Xoá mốc, lặp lại với 23 giờ 59 phút, tra lịch gửi<br>4. Ghi lại thời điểm gửi của từng lần | Khung ngày mai 12:00 - 17:00. Mốc trước khi bắt đầu kiểu trôi qua: 0h00, 0h01, 23h59 | 0h00 ⇒ thời điểm gửi đúng bằng giờ bắt đầu 12:00 — ghi nhận hệ thống có tạo bản ghi hay không và đối chiếu với quy tắc biên đã chốt. 0h01 ⇒ bản ghi lúc 11:59. 23h59 ⇒ bản ghi lúc 12:01 ngày hôm trước. Cả 3 đều neo theo start_time |  | Lấp `G10` · `Q10` · Đánh giá spec: Đã hỏi leader (biên 0h00 xem §4 `CONF-TC-01`) · Evidence: kết quả tra lịch gửi của 3 lần |
| TC-FUNCDATE001-07 | UI | FUNC-DATE-001 | リマインド — cài đặt | Boundary | auto | Tất cả | Mốc gửi SAU khi kết thúc, kiểu ngày trên khung thường — quét 3 mốc giờ biên 00:00 / 00:01 / 23:59 | - Khung tiếp nhận NGÀY MAI 12:00 - 17:00, có 1 lượt đặt đang hiệu lực<br>- Khối 「コース終了後」 chưa có mốc gửi nào | 1. Thêm mốc 「日時で指定」 khối 「コース終了後」, số ngày = 0, giờ 00:00, lưu, tra lịch gửi<br>2. Xoá mốc, lặp lại với số ngày = 0, giờ 00:01, tra lịch gửi<br>3. Xoá mốc, lặp lại với số ngày = 0, giờ 23:59, tra lịch gửi<br>4. Xoá mốc, lặp lại với số ngày = 1, giờ 00:01, tra lịch gửi<br>5. Ghi lại thời điểm gửi của từng lần | Khung ngày mai 12:00 - 17:00 (khung thường, KHÔNG qua nửa đêm). Mốc sau khi kết thúc: 0 ngày 00:00 · 0 ngày 00:01 · 0 ngày 23:59 · 1 ngày 00:01 | Mốc 0 ngày 00:00 và 0 ngày 00:01 đều sớm hơn giờ kết thúc 17:00 ⇒ KHÔNG tạo bản ghi nào. Mốc 0 ngày 23:59 muộn hơn 17:00 ⇒ tạo đúng 1 bản ghi lúc 23:59 cùng ngày. Mốc 1 ngày 00:01 rơi sang ngày hôm sau ⇒ tạo 1 bản ghi lúc 00:01 hôm sau. Cả 4 neo theo end_time. Ô 00:00 hiện chỉ được test trên khung nửa đêm (NEW-19, NEW-34), TC này bổ sung nhánh khung thường |  | Lấp `G10` · `Q10` · Đánh giá spec: Spec ghi rõ (Leader chốt §8 mục 6) · Evidence: kết quả tra lịch gửi của 4 lần |
| TC-FUNCDATE001-08 | UI | FUNC-DATE-001 | リマインド — cài đặt | Boundary | auto | Tất cả | Mốc gửi SAU khi kết thúc, kiểu thời gian trôi qua — quét biên 0h00 / 0h01 / 23h59 | - Khung tiếp nhận NGÀY MAI 12:00 - 17:00, có 1 lượt đặt đang hiệu lực<br>- Khối 「コース終了後」 chưa có mốc gửi nào | 1. Thêm mốc 「経過時間で指定」 khối 「コース終了後」 với 0 giờ 0 phút, lưu, tra lịch gửi<br>2. Xoá mốc, lặp lại với 0 giờ 1 phút, tra lịch gửi<br>3. Xoá mốc, lặp lại với 23 giờ 59 phút, tra lịch gửi<br>4. Ghi lại thời điểm gửi của từng lần | Khung ngày mai 12:00 - 17:00. Mốc sau khi kết thúc kiểu trôi qua: 0h00, 0h01, 23h59 | 0h00 ⇒ thời điểm gửi đúng bằng giờ kết thúc 17:00 — đây chính là biên đang tranh chấp ở §4 CONF-TC-01; ghi nhận chính xác hệ thống có tạo bản ghi hay không, không tự chấm đúng/sai mà đối chiếu với quyết định của Leader. 0h01 ⇒ bản ghi lúc 17:01. 23h59 ⇒ bản ghi lúc 16:59 ngày hôm sau. Cả 3 neo theo end_time |  | Lấp `G10` · `Q10` · **kết quả ô `0h00` là căn cứ chốt `CONF-TC-01`** · Đánh giá spec: Đã hỏi leader · Evidence: kết quả tra lịch gửi của 3 lần |
| TC-FUNCDATE001-09 | UI | FUNC-DATE-001 | リマインド salon — cập nhật mốc gửi (lịch salon) | Abnormal | auto | Tất cả | Salon với lượt đặt qua ngày — mốc gửi thoả và không thoả thời gian gửi | - Lịch salon có 1 lượt đặt qua ngày: bắt đầu NGÀY MAI 22:00, kết thúc NGÀY KIA 02:00<br>- Khối gửi sau khi kết thúc chưa có mốc gửi nào | 1. Thêm mốc 「日時で指定」 sau khi kết thúc, số ngày = 0, giờ 23:00, lưu, tra lịch gửi của lượt đặt<br>2. Xoá mốc, lặp lại với số ngày = 1, giờ 03:00, tra lịch gửi<br>3. Xoá mốc, lặp lại với mốc 「経過時間で指定」 0 giờ 1 phút sau khi kết thúc, tra lịch gửi<br>4. Ghi lại thời điểm gửi của từng lần | Lượt đặt salon qua ngày: ngày mai 22:00 → ngày kia 02:00. Mốc: 0 ngày 23:00 · 1 ngày 03:00 · trôi qua 0h01 | Mốc 0 ngày 23:00 rơi trước lúc kết thúc (ngày kia 02:00) ⇒ KHÔNG tạo bản ghi. Mốc 1 ngày 03:00 muộn hơn lúc kết thúc ⇒ tạo đúng 1 bản ghi lúc 03:00 ngày kia. Mốc trôi qua 0h01 ⇒ bản ghi lúc 02:01 ngày kia. Xác nhận salon tính end_time theo đúng ngày kết thúc thật, không quy nhầm về ngày bắt đầu |  | Lấp `G10` · `Q10` · Đánh giá spec: Spec ghi rõ (Leader chốt §8 mục 6) · Evidence: kết quả tra lịch gửi của 3 lần |
| TC-JOB001-02 | Job | JOB-001 | リマインド — job gửi & recover | Normal | auto | Tất cả | Chạy lệnh recover kèm tham số ghi thật — xoá đúng bản ghi sai, sửa đúng bản ghi lệch, giữ nguyên bản ghi đúng | - Dựng 3 bản ghi lịch gửi chưa gửi trên cùng lịch đặt: (A) mốc gửi sớm hơn giờ kết thúc — sai; (B) khung 22:00~24:00 bị tính về cùng ngày — lệch; (C) mốc gửi muộn hơn giờ kết thúc — đúng<br>- Ghi lại mã, thời điểm gửi, trạng thái và số lần gửi của cả 3 | 1. Chạy lệnh recover không kèm tham số ghi thật, đọc danh sách dự kiến<br>2. Chạy lại lệnh kèm tham số ghi thật<br>3. Tra lại từng bản ghi A, B, C<br>4. Đối chiếu danh sách dự kiến ở bước 1 với thay đổi thật ở bước 3 | 3 bản ghi A (sai) / B (lệch nửa đêm) / C (đúng) | Bản ghi A bị xoá. Bản ghi B được sửa đúng cột thời điểm gửi sang ngày kế tiếp, trạng thái và số lần gửi không đổi. Bản ghi C giữ nguyên hoàn toàn. Việc thật ở bước 3 khớp đúng danh sách dự kiến in ra ở bước 1 |  | Lấp `G1` · `Q1` · Đánh giá spec: Spec ghi rõ (REQ-108) · Evidence: log lệnh + bảng 3 bản ghi trước/sau |

| TC-DATADB001-01 | Data | DATA-DB-001 | リマインド — job gửi & recover | Abnormal | auto | Tất cả | Lệnh recover chạy cho bot A không được chạm dữ liệu bot B | - Hai bot A và B, mỗi bot có 1 lịch đặt bài học riêng<br>- Mỗi bot có cùng một kiểu bản ghi lịch gửi sai (mốc gửi sớm hơn giờ kết thúc, chưa gửi), đặt trùng ngày và trùng giờ gửi để lộ ra nếu điều kiện lọc thiếu bot<br>- Ghi lại mã bản ghi của cả 2 bot | 1. Đếm và ghi lại lịch gửi chưa gửi của bot A và bot B<br>2. Chạy lệnh recover kèm tham số ghi thật, giới hạn phạm vi vào bot A<br>3. Đếm lại lịch gửi của cả 2 bot<br>4. Mở màn cài đặt mốc gửi và danh sách booking của bot B, kiểm hiển thị bình thường | 2 bot, mỗi bot 1 bản ghi sai trùng ngày trùng giờ | Bản ghi sai của bot A bị xoá. Bản ghi của bot B không đổi — đúng mã cũ, đúng thời điểm gửi, đúng trạng thái. Màn của bot B mở bình thường, không lỗi. Nếu bản ghi bot B cũng mất ⇒ điều kiện lọc của lệnh thiếu phạm vi theo bot |  | Lấp `G2` · `Q2` · RULE-07 · Đánh giá spec: Đã hỏi leader · Evidence: bảng đếm trước/sau của cả 2 bot |
| TC-MSG005-01 | Job | MSG-005 | リマインド — job gửi & recover | Normal | manual | product | Bước tạo lại của lệnh recover không được làm khách nhận loạt remind quá hạn | - Môi trường có dữ liệu thật, nhiều lượt đặt đã qua bị thiếu lịch gửi<br>- Ghi lại số tin đã dùng trong ngày của bot trước khi chạy<br>- Có 1 khách LINE kiểm thử đã kết bạn, chuẩn bị điện thoại thật | 1. Chạy lệnh không kèm tham số ghi thật, đọc số bản ghi dự kiến tạo lại và danh sách lượt đặt tương ứng<br>2. Đối chiếu danh sách đó: có lượt đặt nào đã qua không, có mốc gửi nào đã ở quá khứ không<br>3. Chỉ khi bước 2 sạch mới chạy kèm tham số ghi thật<br>4. Theo dõi máy thật của khách kiểm thử trong 30 phút sau đó<br>5. Đọc lại số tin đã dùng trong ngày của bot | Dữ liệu thật của môi trường đích | Danh sách dự kiến tạo lại không chứa mốc gửi đã ở quá khứ. Sau khi chạy thật, khách kiểm thử không nhận loạt tin remind cũ. Số tin đã dùng trong ngày tăng đúng bằng số tin thực sự phải gửi, không nhảy vọt. Nếu bước 1 cho thấy sẽ tạo lại lịch gửi ở quá khứ ⇒ dừng, không chạy bước 3, báo lại ngay |  | Lấp `G3` · `Q5` · RULE-08 (bill tiền + job nền) · Đánh giá spec: Đã hỏi leader · Evidence: log dry-run + ảnh LINE app + số tin trước/sau · manual vì phải chạy trên production và quan sát LINE app thật |
| TC-ENV003-01 | UI | ENV-003 | リマインド — cài đặt | Normal | manual | product | Xác nhận lại bản vá update-flow lesson và salon trên production | - Bot production thật, có lịch đặt bài học và lịch salon đang dùng<br>- Trên mỗi bên: 1 khung tiếp nhận ngày mai 12:00 - 17:00, 1 lượt đặt đang hiệu lực, 1 mốc gửi sau khi kết thúc đặt 18:00 và đã có lịch gửi<br>- Đã xin phép dùng dữ liệu production và thống nhất dọn sau khi test | 1. Trên lịch bài học, sửa mốc gửi từ 18:00 xuống 15:00, lưu, rồi tra lịch gửi của lượt đặt<br>2. Sửa ngược về 18:00, lưu, tra lại<br>3. Lặp đúng 2 bước trên cho lịch salon<br>4. Trên lịch bài học, mở màn cài đặt mốc gửi và bấm lưu không đổi gì, tra lại lịch gửi<br>5. Dọn dữ liệu test đã tạo | Bot production. Mốc gửi 18:00 → 15:00 → 18:00 | Bước 1 và 3: lịch gửi bị xoá ở cả lesson lẫn salon vì 15:00 sớm hơn giờ kết thúc 17:00. Bước 2 và 3: lịch gửi được tạo lại đúng 18:00. Bước 4: bản ghi còn nguyên, không bị mất chỉ vì bấm lưu. Kết quả trùng khớp những gì đã chạy trên staging |  | Lấp `G6` · `Q6` · RULE-08 · Đánh giá spec: Spec ghi rõ (REQ-101, REQ-105) · Evidence: ảnh trên production + kết quả tra lịch gửi · manual vì chạy trên production |

**Truy vết ma trận biên Leader chốt (§8 mục 7) — 18/18 ô sau khi bổ sung**

| Khối | Kiểu | Ô biên | TC đã có | TC bổ sung |
|---|---|---|---|---|
| `コース開始前` | `日時で指定` | `day = 0` | `NEW-5` | — |
| | | `day ≠ 0` | — | `TC-FUNCDATE001-05` |
| | | giờ `00:00` | — | `TC-FUNCDATE001-04` |
| | | giờ `00:01` | — | `TC-FUNCDATE001-04` |
| | | giờ `23:59` | — | `TC-FUNCDATE001-04` |
| | `経過時間で指定` | `0h00` | — | `TC-FUNCDATE001-06` |
| | | `0h01` | — | `TC-FUNCDATE001-06` |
| | | `23h59` | — | `TC-FUNCDATE001-06` |
| `コース終了後` | `日時で指定` | `day = 0` | `NEW-3` · `NEW-10` · `NEW-11` · `NEW-13` · `NEW-14` · `NEW-18` · `NEW-26` | — |
| | | `day ≠ 0` | `NEW-20` · `NEW-17` | `TC-FUNCDATE001-07` (1 ngày 00:01) |
| | | giờ `00:00` | `NEW-19` · `NEW-34` — **chỉ khung nửa đêm** | `TC-FUNCDATE001-07` (khung thường) |
| | | giờ `00:01` | — | `TC-FUNCDATE001-07` |
| | | giờ `23:59` | — | `TC-FUNCDATE001-07` |
| | `経過時間で指定` | `0h00` | — | `TC-FUNCDATE001-08` ⚠️ là biên tranh chấp `CONF-TC-01` |
| | | `0h01` | — | `TC-FUNCDATE001-08` |
| | | `23h59` | — | `TC-FUNCDATE001-08` |
| `salon` | — | booking qua ngày, mốc **thoả** | — | `TC-FUNCDATE001-09` |
| | — | booking qua ngày, mốc **không thoả** | — | `TC-FUNCDATE001-09` |

> Gộp nhiều ô biên vào **một** TC theo từng cặp (khối × kiểu) là cố ý: mỗi TC vẫn giữ **một trọng tâm** — *"biên giờ của khối X kiểu Y"* — và mỗi giá trị đều có kết quả mong đợi riêng trong cột `Kết quả mong đợi`, nên vẫn chấm được từng ô. Cách này khớp với `NEW-34` mà Studio tự viết (so 2 cách chọn trong 1 TC).

**Nguồn của từng TC đề xuất:** `G10`/`Q10` (ma trận Leader chốt) → **6 TC, xếp đầu bảng** · `G1`→1 · `G2`→1 · `G3`→1 · `G6`→1.

**Dùng lại TC kho — không viết mới:**

| GAP | TC kho dùng lại | Cần chỉnh gì |
|---|---|---|
| `G8` · `Q4` | `TC-LSN-413` *"Restart job gửi remind trong lúc đang có bản ghi status = 1 (đã nhặt, chưa gửi)"* | Chạy trước/sau khi deploy nhánh `ai_fixbug_33762` lên môi trường đích |
| `Q7` | `TC-LSN-415` *"Dữ liệu tạo TRƯỚC và SAU spec change #32367 cùng tồn tại — hành vi phải nhất quán"* | Đổi mốc so sánh từ release #32367 sang **ngày deploy `ai_fixbug_33762`**; thêm bước chạy lệnh recover mới lên cả 2 thế hệ dữ liệu |

**GAP không đề xuất TC:** `G7` (file 03 lạc hậu) và `G9` (lối duyệt đơn trên app — Leader đã quyết loại ở lượt 1) là việc cập nhật input và quyết định phạm vi, không phải thứ lấp bằng TC.

**GAP mất TC do Leader quyết loại (2026-09-25):**

| GAP / quan điểm | TC đã bỏ | Hệ quả còn lại |
|---|---|---|
| `G1` · `Q1` — lệnh recover | ~~`TC-JOB001-01`~~ (dry-run mặc định, `REQ-107` **High**) · ~~`TC-JOB001-03`~~ (chạy lại lần 2, `REQ-110`) · ~~`TC-JOB001-04`~~ (không đụng bản ghi đã gửi / đang gửi, `REQ-108` + BR-41) | **Thu hẹp, chưa đóng.** Còn `TC-JOB001-02` phủ nhánh chính của `REQ-108` (xoá sai / sửa lệch / giữ đúng). `REQ-107` (dry-run) và `REQ-110` (idempotent) trở lại **0 TC**; nhánh bản ghi `status ≠ 0` không còn ai canh |
| `G4` · `Q3` — chạy đồng thời với job gửi | ~~`TC-CONC001-01`~~ | **GAP vẫn mở.** Cửa sổ đua giữa lệnh recover và job `NewEventRemindTask` (job đổi `status = 0 → 1` trước khi gửi, BR-41 nói bản ghi `status = 1` vẫn sẽ được gửi) không còn TC nào |
| `G5` — phạm vi lọc theo ngày của lệnh recover (`REQ-111`) | ~~`TC-JOB001-05`~~ | **GAP vẫn mở.** Dev tự nêu *"cần leader xác nhận đây là chủ ý hay thiếu điều kiện lọc"* — nay không còn TC ghi nhận hiện trạng làm căn cứ. Câu hỏi vẫn treo ở §8 mục 3 |
| `R1` — regression nhánh remind gửi TRƯỚC | ~~`TC-REGSHARED001-05`~~ | **Không còn TC.** `dev_impact` khẳng định *"Không đụng nhánh nhắc lịch gửi-TRƯỚC"*, nhưng khẳng định này không được kiểm chứng khi lệnh recover chạy. Kho có `TC-LSN-409` đúng nguyên tắc này, có thể dẫn lại nếu cần |

---

## 8. Spec update needed

| # | Vấn đề | Cần chốt |
|---|---|---|
| 1 | **Biên `mốc gửi = giờ kết thúc`** — `REQ-004` nói phải lập lịch; lý do reject Redmine #40899 (`"Không bị lỗi"`) lại chấp nhận việc không lập lịch. 5 TC đang pass dựa trên `REQ-004` | Chốt hành vi đúng ở biên bằng nhau. Nếu theo reject → sửa `REQ-004` + expected của `NEW-3`/`NEW-11`/`NEW-30`/`NEW-35`/`NEW-36`. Nếu theo `REQ-004` → mở lại #40899 |
| 2 | **Hai lệnh recover cùng loại dữ liệu** — `recover:remindLesson` (Support #33648, kho `TC-LSN-409`…`412`) và `recover:remind-after-end` (mới) | Chốt command nào là chuẩn. Nếu thay thế → đánh dấu lỗi thời command cũ và cập nhật 4 TC kho. Nếu song song → ghi rõ ranh giới phạm vi vào spec |
| 3 | **Phạm vi lọc theo ngày của lệnh recover** (`REQ-111`) — bước rà vẫn xoá bản ghi chưa gửi của lượt đặt đã qua dù nằm ngoài khoảng ngày, trong khi bước tạo lại thì tôn trọng khoảng ngày | Dev đã tự nêu *"cần leader xác nhận đây là chủ ý hay thiếu điều kiện lọc"*. Chốt rồi ghi vào spec; `TC-JOB001-05` (§7) ghi nhận hiện trạng làm căn cứ |
| 4 | **Hạn chế còn tồn của mốc gửi kiểu ngày với khung nửa đêm** (`REQ-106`) — khung 22:00~24:00 chọn *0 ngày sau lúc 00:00* thì không tạo được lịch gửi, phải chọn *1 ngày sau 00:00* | Dev ghi *"Đang chờ chốt xử lý trong ticket nào"*. Chốt: chấp nhận và ghi vào spec §8.7, hay tách ticket sửa. `NEW-34` đang ghi nhận hiện trạng, không chấm sai |
| 6 | **Spec neo mốc gửi — Leader đã chốt 2026-09-25, cần ghi vào `spec-features`** — `コース開始前` thì mốc gửi tính theo **`start_time`** của lượt đặt; `コース終了後` thì tính theo **`end_time`**. Kiến trúc: **web** tạo và xoá bản ghi `event_step_time` ngay khi add/sửa/xoá mốc gửi; **job** chỉ chạy theo dữ liệu web đã tạo, không tự quyết | Ghi 2 quy tắc này vào `spec-features/admin/lesson-booking/feature-spec.md` §8.7 (bổ sung cho **BR-38**/**BR-39**, hiện chỉ mô tả công thức mà không nói rõ neo theo mốc nào cho từng khối). Đây là chuẩn để chấm lại `CONF-TC-01` |
| 7 | **Ma trận biên bắt buộc — Leader đã chốt 2026-09-25** — mỗi khối (`開始前` / `終了後`) × 2 kiểu (`日時で指定` / `経過時間で指定`): kiểu ngày phải phủ `day = 0`, `day ≠ 0`, và các mốc giờ biên `00:00` · `23:59` · `00:01`; kiểu thời gian trôi qua phải phủ `0h00` · `0h01` · `23h59`. Salon phải thêm booking **qua ngày** với mốc thoả và không thoả | Hiện mới đạt **4/18 ô** (bảng đối chiếu ở §1 `G10`). 6 TC lấp ô trống đã viết ở §7. Sau khi chạy xong, cập nhật ma trận này vào kho `kho-tcs/fa019` nhóm **29 リマインド — cài đặt** để lần sau không phải dựng lại |
| 5 | **Mất lịch nhắc mà không có cảnh báo** — cả #40876 mục 2 lẫn lần fail của `NEW-30` ở run #2051 đều cho thấy chỉ cần mở màn cài đặt mốc gửi rồi bấm lưu là bản ghi có thể biến mất, màn hình không báo gì | Spec chưa định nghĩa UI phải làm gì khi thao tác lưu khiến lịch gửi bị xoá. Chốt: hiện cảnh báo số bản ghi sẽ bị xoá trước khi lưu, hay chấp nhận im lặng |

---

> Report này là **draft cho Leader verify**, không phải kết luận cuối. Nguồn: Studio task #233 round 3 (`testcase_list` 25 TC qua `scripts/parse_studio_tcs.py` · `task_get_context` dev_impact + spec_delta + 21 requirement · `task_get_report` 11 run auto + 55 kết quả manual + 3 bug · `review_list_comments` rỗng) · `01-bug-task.md` · `03-dev-impact.md` · `spec-features/admin/lesson-booking/feature-spec.md` §4.5 + §8.7 · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md`.
