# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **journal #8 Redmine #37603** — note của bot `AI LME Fix bug`, 2026-08-24T06:15:54Z (journal #7 lúc 06:15:34Z **trùng y hệt**, đã bỏ trùng).
> Dev là **hệ thống Auto-fixbug LME**, không phải người → mục 3/4 dưới đây là output máy sinh, Leader cần soi kỹ trước khi giao TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine hiện tại: Ngô Thúy Ngần |
| Commit / Pull Request | `<không có link PR>` — commit `71c4781e78` (1 file, 15 thêm / 1 xoá). Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=37603 · Phiên AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=9f22015b-47d0-4769-b8bc-240b8b5a05e7 |
| Branch | `ai_small_37603` (repo `sns-line`, nhánh gốc `release_step_20260805`, đỉnh origin `fcc06a7fbd`) — **đã push** |
| Ngày submit đánh giá | `2026-08-24` |
| Auto-filled | `2026-09-04 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

*(nguyên văn mục ■ 1. NGUYÊN NHÂN)*

Trong hàm dùng chung xử lý hành động của Bán hàng, nhánh sự kiện "mở trang sản phẩm" so sánh với biến sản phẩm CHƯA HỀ ĐƯỢC GÁN (biến này chỉ được truy vấn ở nhánh "đăng ký hoàn tất"), nên điều kiện luôn sai và loại kích hoạt luôn bị ghi thành mã của sản phẩm bán định kỳ. Vì vậy modal Trigger scenario ở màn Chi tiết bạn bè luôn hiển thị tên tính năng "bán hàng định kỳ" dù sản phẩm là bán 1 lần. Ngoài ra một số điểm gọi không truyền id sản phẩm nên ngay cả nhánh "đăng ký hoàn tất" cũng có thể ghi sai loại.

## 2. Cách fix

*(nguyên văn mục ■ 2. CÁCH FIX)*

Refix vòng 1 theo AI review: TẠO LẠI branch ai_small_37603 từ ĐÚNG đỉnh origin/release_step_20260805 (fcc06a7fbd). Branch cũ bị tách nhầm từ commit LOCAL 966971f6ae của ticket #40053 nên mang theo 165 commit / 81 file lạ (gồm cả 1 migration DB) — bấm Push sẽ kéo nhầm code chưa duyệt. Cách làm an toàn (branch chưa push lên origin, không vi phạm rule no-history-rewrite): git fetch origin release_step_20260805 → tạo worktree /tmp/wt37603 từ origin/release_step_20260805 (không đụng HEAD cây source dùng chung, đang ở ai_small_38843) → cherry-pick commit fix d75311d5f6 → git branch -f ai_small_37603 71c4781e78 → xoá worktree. NỘI DUNG FIX GIỮ NGUYÊN (không sửa logic): hàm dùng chung getSItemForActionOrderItem + gọi ở nhánh view_page và contract trong app/Helpers/functions.php. Kiểm chứng sau khi tạo lại: parent của commit = fcc06a7fbd = đúng đỉnh origin/release_step_20260805; git log origin/release_step_20260805..ai_small_37603 = ĐÚNG 1 commit; git diff --name-only = ĐÚNG 1 file app/Helpers/functions.php (15 thêm / 1 xoá); php -l sạch; diff trên dashboard đã render lại theo base ĐÚNG.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

*(convert từ list plain của mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN — giữ nguyên chú thích trong ngoặc của Dev)*

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `sendActionOrderItem` — `app/Helpers/functions.php:6693` | **Sửa** | Hàm dùng chung xử lý action Bán hàng — nơi chứa nhánh `view_page` dùng biến sản phẩm chưa gán |
| 2 | `getSItemForActionOrderItem` — `app/Helpers/functions.php:6680` | **Thêm mới** | Hàm dùng chung gom việc lấy sản phẩm, có fallback lấy `item_id` từ `bot_line_user_item` |
| 3 | `sendAction` — `app/Helpers/functions.php:8069` | Không sửa | Nơi INSERT `action_lineuser.type_start_scenario` |
| 4 | `SalesManagementV2Controller::orderDetail` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php:1694` | Không sửa | Điểm gọi `view_page` **có** truyền id sản phẩm |
| 5 | `SalesManagementController::orderDetail` — `app/Http/Controllers/Basic/SalesManagementController.php:1525` | Không sửa | Điểm gọi `view_page` **KHÔNG** truyền id sản phẩm → phụ thuộc fallback |
| 6 | `SalesStripePaymentController` — `app/Http/Controllers/Basic/SalesStripePaymentController.php:264,439` | Không sửa | Điểm gọi `contract` **không** truyền id sản phẩm → phụ thuộc fallback |
| 7 | `ResolveTriggerTypeTrait::resolveTriggerTypeLabel` — `app/Traits/ResolveTriggerTypeTrait.php:130-149` | Không sửa | Phía hiển thị, chỉ đọc mã |
| 8 | `ChatController` mapping 12001/13001 — `app/Http/Controllers/ChatController.php:6854` và `Api/ChatController.php:5660` | Không sửa | Phía hiển thị (Web + API app) |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Dev ghi mục 4.1 là **"File thay đổi"** chứ không phải "function bị ảnh hưởng". Bảng dưới được dựng lại từ mục 3 + 4.1 nguyên văn; **không** thêm function nào Dev chưa nêu.

### 4.1. List function bị ảnh hưởng

*(nguyên văn 4.1: File thay đổi — `app/Helpers/functions.php`)*

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `sendActionOrderItem` (nhánh `view_page` + nhánh `contract`) | `app/Helpers/functions.php:6693` | Direct | **File duy nhất bị sửa.** Biến `$sItem` chưa gán ở nhánh `view_page` → điều kiện luôn false → luôn ghi 13001 |
| F2 | `getSItemForActionOrderItem` | `app/Helpers/functions.php:6680` | Direct | Hàm **mới thêm**, có fallback `bot_line_user_item.item_id` khi caller không truyền productId |
| F3 | `sendAction` | `app/Helpers/functions.php:8069` | Indirect | Nơi INSERT `action_lineuser.type_start_scenario` — nhận giá trị từ F1 |
| F4 | `SalesManagementController::orderDetail` (caller `view_page` V1) | `SalesManagementController.php:1525` | Indirect | Không truyền productId → **chỉ đúng nhờ fallback của F2** |
| F5 | `SalesStripePaymentController` (caller `contract`) | `SalesStripePaymentController.php:264,439` | Indirect | Không truyền productId → **chỉ đúng nhờ fallback của F2** |
| F6 | `SalesManagementV2Controller::orderDetail` (caller `view_page` V2) | `SalesManagementV2Controller.php:1694` | Indirect | Có truyền productId → đi nhánh chính |
| F7 | `ResolveTriggerTypeTrait::resolveTriggerTypeLabel` | `ResolveTriggerTypeTrait.php:130-149` | Indirect | Phía hiển thị, **chỉ đọc mã** — Dev khẳng định không phải sửa |
| F8 | `ChatController` / `Api/ChatController` mapping 12001/13001 | `ChatController.php:6854`, `Api/ChatController.php:5660` | Indirect | Phía hiển thị Web + API app, **chỉ đọc mã** |

### 4.2. List data bị update khi fix bug

*(nguyên văn mục 4.2)*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `action_lineuser.type_start_scenario` | CREATE (bản ghi mới) | Nguyên văn: "các bản ghi CŨ của sản phẩm bán 1 lần đã lưu 13001 (đúng phải là 12001) và một phần 13002 (đúng phải 12002); **dữ liệu cũ không tự sửa**, chỉ bản ghi mới sau khi deploy mới đúng" |
| D2 | `s_items.type_payment` | READ (chỉ đọc thêm, không ghi) | Là điều kiện phân loại 1 lần (`=0`) vs định kỳ (`!=0`) |
| D3 | `bot_line_user_item.item_id` | READ (chỉ đọc thêm, không ghi) | Nguồn của **fallback** khi caller không truyền productId |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

*(nguyên văn mục 4.3 — Dev **không** ghi mức High/Medium/Low)*

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Single Product / Sales (FA-026)** — sự kiện hành động khi hiển thị trang sản phẩm và khi đăng ký hoàn tất nay ghi đúng loại sản phẩm 1 lần / định kỳ | F1, F2, D1, D2 | `<Dev không ghi>` |
| T2 | **Step Delivery / Scenario (FA-009)** — nhãn nguồn kích hoạt của kịch bản trong modal Chi tiết bạn bè hiển thị đúng tên tính năng | F7, F8, D1 | `<Dev không ghi>` |
| T3 | **Friend Information (FA-015)** — lịch sử/nhãn nguồn thay đổi hiển thị theo cùng mã kích hoạt này | F7, F8, D1 | `<Dev không ghi>` |

---

## 5. Recover data (mục ■ 5 của báo cáo AI — KHÔNG có trong template chuẩn, giữ vì ảnh hưởng phạm vi test)

⚠ **CÓ** — Các bản ghi `action_lineuser` cũ của sản phẩm BÁN 1 LẦN đang lưu `type_start_scenario=13001` (và một phần 13002) nên modal vẫn hiển thị sai cho dữ liệu quá khứ. Nếu muốn hiển thị đúng cả lịch sử thì cần UPDATE các bản ghi này sang 12001/12002 dựa trên `s_items.type_payment=0`.

- Phạm vi: bảng `action_lineuser` (join `s_items` theo `from_id`/`product_id`, điều kiện `type_payment=0` và `type_start_scenario IN (13001,13002)`).
- Cần **DBA/human chạy có backup**; fix code này **KHÔNG** tự sửa dữ liệu cũ.

## 6. Verify của Dev (mục ■ 6 — mức: **lint**)

Nguyên văn phần **Bằng chứng** (rút gọn các lệnh git kiểm branch, giữ nguyên phần liên quan logic):

- `app/Helpers/functions.php:6707` (bản gốc) dùng biến `$sItem` **chưa gán** ở nhánh `view_page` — biến chỉ được truy vấn ở nhánh `contract` dòng 6759 → điều kiện luôn false → luôn ghi 13001, **khớp đúng ghi nhận của tester** (`action_lineuser.id=79603` lưu 13001).
- `SalesManagementController.php:1525` gọi `sendActionOrderItem('view_page', ...)` chỉ 5 tham số → id sản phẩm = null, nên chỉ sửa biến chưa gán là **chưa đủ**, phải có fallback lấy `item_id` từ `bot_line_user_item`.
- `php -l app/Helpers/functions.php`: No syntax errors detected.
- **PHPUnit: không có test class nào phủ `sendActionOrderItem`/`getSItemForActionOrderItem`** (grep `tests/` không ra) → N/A.
- ⚠️ **MySQL dev `host.docker.internal:3306` không kết nối được (Connection refused) → không dump được dữ liệu thực tế để đối chiếu, kết luận dựa trên ĐỌC CODE.**

## 7. Tự review + rủi ro khi test (do AI ghi)

Tự review: Fix tối thiểu, đúng root cause: biến sản phẩm chưa gán ở nhánh hiển thị trang sản phẩm. Gom việc lấy sản phẩm vào 1 hàm dùng chung, có fallback lấy id sản phẩm từ bản ghi `bot_line_user_item` nên bao cả điểm gọi cũ không truyền id. Phía hiển thị (modal, lịch sử) không phải sửa vì chỉ đọc mã. Không đổi hành vi cho sản phẩm định kỳ (vẫn 13001/13002). [Vòng refix 1] Nội dung code KHÔNG đổi so với vòng trước — chỉ tạo lại branch từ đúng đỉnh `origin/release_step_20260805`.

Rủi ro / lưu ý khi test (nguyên văn):
- Thêm 1 truy vấn SELECT `s_items` cho mỗi lần chạy hành động ở sự kiện hiển thị trang sản phẩm (trước đây nhánh này không query) — tần suất thấp, chỉ khi sản phẩm có gán hành động.
- Nếu bản ghi `bot_line_user_item` trỏ sai `item_id` thì mã kích hoạt vẫn sai; các điểm gọi hiện tại đều tạo bản ghi này theo đúng item nên rủi ro thấp.
- Dữ liệu cũ vẫn hiển thị sai cho tới khi được recover (xem mục 5).
- Branch đã được tạo lại (`git branch -f`) nên SHA commit đổi từ `d75311d5f6` → `71c4781e78`; branch chưa từng push lên origin nên không ảnh hưởng ai, nhưng nếu có ai đã checkout local bản cũ thì phải lấy lại.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader nên soi (ghi nhận từ chính nội dung Redmine, không suy diễn thêm)

- Verify của Dev **chỉ ở mức `lint`**, **không có unit test** phủ 2 hàm bị sửa, và **không kết nối được DB** để đối chiếu dữ liệu thật → toàn bộ kết luận dựa trên đọc code.
- Mục 4.3 **không có mức High/Medium/Low** → Leader cần tự gán trước khi chấm coverage.
- Bug **đã reopen 1 lần** (journal #3 "Check vẫn bị lỗi") → vòng test này phải cover lại flow của vòng fix trước.
- Data cũ **không được sửa** (mục 5) → TC trên dữ liệu cũ sẽ vẫn hiển thị `継続商品販売`; đây **không** phải fail của fix, nhưng cần TC ghi nhận phạm vi legacy.
