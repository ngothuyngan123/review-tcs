# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #40171 bằng `/new-task`. Nguồn: **journal #133070** — báo cáo *"★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST"* của user `AI LME Fix bug` lúc 2026-08-26T08:09:53Z. Redmine **description KHÔNG chứa** section "Đánh giá ảnh hưởng"; toàn bộ nội dung dưới đây lấy từ journal đó, giữ nguyên văn.

---

## ⚠️ CẢNH BÁO INPUT — mâu thuẫn trong chính báo cáo của Dev

Báo cáo Auto-fixbug mô tả **2 vòng fix**, và các mục sau đó **không được cập nhật đồng bộ**:

| Mục | Nói cách fix là gì |
|---|---|
| **2. Cách fix** | *Vòng 1*: `CAST(conversation.line_id AS SIGNED)` tại 9 subquery → *Vòng 2 (spec bổ sung của người phụ trách)*: **bỏ CAST**, dùng `conversation.tb_line_user_id` (`Conversation::FILTER_LINE_USER_COLUMN`). Test yêu cầu subquery select `tb_line_user_id`. |
| **6. VERIFY** | *"truy vấn con đổi thành select **CAST(conversation.line_id AS SIGNED)**"* → mô tả kết quả của **vòng 1** |
| **TỰ REVIEW (AI)** | *"chỉ đổi KIỂU của cột trả về... dùng SIGNED (không phải UNSIGNED)"* và liệt kê `tb_line_user_id` vào nhóm **KHÔNG chọn lần này** vì *"tb_line_user_id cho phép NULL nên có nguy cơ lọc thiếu bạn bè"* |

**Rủi ro:** nếu code cuối cùng thật sự dùng `tb_line_user_id` (theo mục 2), thì chính rủi ro mà AI tự nêu ở TỰ REVIEW — **cột NULL → subquery loại mất bạn bè → số đếm / danh sách lọc bị THIẾU** — vẫn chưa được xử lý hoặc chưa được giải thích là đã xử lý ra sao.

👉 **Leader phải hỏi Dev chốt trước khi giao viết/review TC:**
1. Code trên branch `ai_small_40171` (commit `e131fdbf80`) cuối cùng dùng `CAST(line_id AS SIGNED)` hay `tb_line_user_id`?
2. Nếu dùng `tb_line_user_id`: cột này có row nào NULL không (bot cũ / conversation tạo trước khi thêm cột)? Có backfill chưa? → đây là **điểm bắt buộc phải có TC đối chiếu số đếm trước/sau fix trên bot có dữ liệu cũ**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — người tạo ticket: `Do Van Tu TuDV`; assignee hiện tại: `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | repo `sns-line`, commit `e131fdbf80` (2 file) — `<không có link PR Github/Gitlab trong ticket>`. Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=69daea9b-bf31-47ae-8c9f-8d3ad9b69caf · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40171 |
| Branch | `ai_small_40171` (nhánh gốc `release_step_20260805`) — **đã push origin** |
| Ngày submit đánh giá | `2026-08-26` (journal #133070, 08:09:53Z) |
| Auto-filled | `2026-08-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn từ journal #133070:

Bộ lọc bạn bè đếm số người bằng truy vấn con dạng: `bot_line_user.line_user_id IN (SELECT line_id FROM conversation WHERE ...)`. Cột `line_id` của bảng hội thoại khai báo là chuỗi (varchar 255) dù chỉ chứa số, còn `line_user_id` là số nguyên. Hai vế của `IN` khác kiểu dữ liệu nên MySQL không dựng được bảng tạm cho truy vấn con mà phải đổi sang truy vấn con phụ thuộc, tức chạy LẠI truy vấn con cho TỪNG dòng bạn bè. Bot có nhiều bạn bè thì câu đếm chạy rất lâu. Dạng truy vấn con này **mới xuất hiện từ ticket 39667** (trước đó lấy danh sách ra mảng PHP nên không vướng lỗi so kiểu).

## 2. Cách fix

> Nguyên văn từ journal #133070:

**Vòng 1:** ép subquery lọc bạn bè trả về kiểu số bằng `CAST(conversation.line_id AS SIGNED)` tại **9 subquery** trong bộ lọc (`advanceFilter` + nhóm AND/OR của `advanceFilterPost`), để MySQL materialize subquery 1 lần thay vì chạy dependent subquery theo từng dòng bạn bè.

**Vòng 2 (spec bổ sung của người phụ trách):** bỏ `CAST`, thay bằng `SELECT` thẳng cột int có sẵn `conversation.tb_line_user_id` (hằng `Conversation::FILTER_LINE_USER_COLUMN`) — cột này lưu chính `line_user.id` = `bot_line_user.line_user_id` (đúng khoá mà quan hệ `lineUser()` và các join sẵn có trong `Conversation.php` đang dùng), nên 2 vế của `IN` đã cùng kiểu số mà **KHÔNG** phải convert dữ liệu cột `line_id`. **Điều kiện lọc và kết quả trả về giữ nguyên.**

Test `tests/Feature/FriendFilterSubqueryTypeTest.php` cập nhật: chặn cả dạng cũ (`select line_id` varchar) lẫn dạng trung gian (`CAST line_id`), yêu cầu subquery select `tb_line_user_id`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn danh sách của Dev, convert sang bảng. Cột "Thay đổi" / "Lý do" lấy đúng chú thích Dev ghi trong ngoặc; ô ghi `<Dev không ghi>` = Dev chỉ liệt kê tên, không mô tả thêm.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::lineIdAsInt` — `app/Conversation.php` | **Hàm mới** | Dev ghi "hàm mới" |
| 2 | `Conversation::advanceFilter` — `app/Conversation.php` | Có sửa (nằm trong 9 subquery ở mục 2) | Nơi sinh subquery lọc bạn bè |
| 3 | `Conversation::advanceFilterPost` — `app/Conversation.php` | Có sửa (nhóm AND/OR, nằm trong 9 subquery ở mục 2) | Nơi sinh subquery lọc bạn bè |
| 4 | `FilterController::initDataFilter` — `app/Http/Controllers/Basic/FilterController.php` | Đã check | "nơi gọi câu count trong ticket" |
| 5 | `FilterV2::initDataFilter` — `app/FilterV2.php` | Đã check | `<Dev không ghi>` |
| 6 | `FriendlistController::index/getListFriend` — `app/Http/Controllers/Basic/FriendlistController.php` | Đã check | `<Dev không ghi>` |
| 7 | `BotLineUser::makeDataTalkList` — `app/BotLineUser.php` | Đã check | `<Dev không ghi>` |
| 8 | `ConversationReplicate::advanceFilterPost` — `app/ConversationReplicate.php` | Đã kiểm, **không sửa** | "vẫn dùng mảng PHP, không bị lỗi so kiểu" |
| 9 | `FriendMemoRepository::resolveConversationId` — `app/Repositories/Eloquents/FriendMemoRepository.php` | Đã kiểm (tham chiếu) | "bằng chứng line_id là chuỗi chứa id số" |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Mục 4.1 trong báo cáo Dev thực chất là **"File thay đổi"**, KHÔNG phải list function. Nguyên văn:
>
> - `app/Conversation.php`
> - `tests/Feature/FriendFilterSubqueryTypeTest.php`
>
> Bảng dưới ghép từ mục 3 + mục 4.1 để có tag `F*` dùng cho coverage matrix. Cột "Mức độ ảnh hưởng" là **suy ra từ lời Dev**, chưa được Dev xác nhận trực tiếp — Leader confirm lại.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::lineIdAsInt` | `app/Conversation.php` | Direct (hàm mới) | Hàm sinh biểu thức cột cho subquery |
| F2 | `Conversation::advanceFilter` | `app/Conversation.php` | Direct | Trong 9 subquery được sửa |
| F3 | `Conversation::advanceFilterPost` (gồm nhóm AND/OR) | `app/Conversation.php` | Direct | Trong 9 subquery được sửa |
| F4 | `FilterController::initDataFilter` | `app/Http/Controllers/Basic/FilterController.php` | Indirect (caller) | Nơi gọi đúng câu count trong ticket |
| F5 | `FilterV2::initDataFilter` | `app/FilterV2.php` | Indirect (caller) | Dùng chung bộ lọc; theo 4.3 là đường đi của Rich Menu |
| F6 | `FriendlistController::index` / `getListFriend` | `app/Http/Controllers/Basic/FriendlistController.php` | Indirect (caller) | Màn danh sách bạn bè |
| F7 | `BotLineUser::makeDataTalkList` | `app/BotLineUser.php` | Indirect (caller) | Danh sách trò chuyện |
| F8 | `ConversationReplicate::advanceFilterPost` | `app/ConversationReplicate.php` | Không đổi (Dev đã kiểm) | Vẫn dùng mảng PHP → không dính lỗi so kiểu |
| F9 | `tests/Feature/FriendFilterSubqueryTypeTest.php` | `tests/Feature/` | Test file (đã cập nhật) | Khoá hình dạng SQL, không phải function sản phẩm |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2 của Dev: **"Không có — thay đổi chỉ nằm trong câu SELECT, không có lệnh ghi/sửa/xoá dữ liệu"**.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Dev khẳng định không ghi/sửa/xoá dữ liệu |

**Bảng / cột chỉ ĐỌC (không bị ghi) — liên quan trực tiếp tới fix, cần cho việc dựng dữ liệu test:**

| Bảng.cột | Kiểu (theo Dev) | Vai trò trong fix |
|---|---|---|
| `conversation.line_id` | `varchar(255)` | Cột **cũ** dùng trong subquery → nguồn lỗi so kiểu |
| `conversation.tb_line_user_id` | int (`Conversation::FILTER_LINE_USER_COLUMN`) | Cột **mới** subquery select (theo mục 2 vòng 2). ⚠️ Dev ghi cột này **cho phép NULL** |
| `bot_line_user.line_user_id` | `int(11)` | Vế trái của `IN` |
| `friend_information_value.line_id` | `int(11)` | Dev ghi: **đã là int → không dính lỗi so kiểu** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn 8 mục Dev liệt kê. Cột "Nguy cơ regression" **Dev KHÔNG ghi** — để Leader/tester điền.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Filter / Segment (SC-003)** — câu đếm số người của bộ lọc chạy truy vấn con một lần thay vì lặp theo từng bạn bè; **số đếm không đổi** | F1, F2, F3, F4 | `<Dev không ghi — Leader điền>` |
| T2 | **Friend List (FA-013)** — màn danh sách bạn bè khi lọc theo trạng thái chat / nhãn hội thoại / bạn bè cũ chạy nhanh hơn, **danh sách trả về không đổi** | F2, F3, F6 | `<Dev không ghi — Leader điền>` |
| T3 | **Broadcast (FA-008)** — số người nhận hiển thị trước khi gửi tin hàng loạt dùng chung bộ lọc này | F2, F3 | `<Dev không ghi — Leader điền>` |
| T4 | **Cross Analysis (FA-024)** — đếm và lấy danh sách bạn bè theo bộ lọc trong phân tích chéo | F2, F3 | `<Dev không ghi — Leader điền>` |
| T5 | **Chat / Talk Management (FA-002)** — danh sách trò chuyện lọc theo điều kiện bạn bè (`makeDataTalkList`) | F7 | `<Dev không ghi — Leader điền>` |
| T6 | **Step Delivery / Scenario (FA-009)** — bộ lọc điều kiện của kịch bản đi qua cùng hàm lọc | F2, F3 | `<Dev không ghi — Leader điền>` |
| T7 | **Rich Menu (FA-004)** — điều kiện hiển thị của chuyển rich menu dùng chung bộ lọc qua `FilterV2` | F5 | `<Dev không ghi — Leader điền>` |
| T8 | **CSV Management (FA-014)** — job xuất CSV bạn bè theo bộ lọc dùng chung hàm lọc | F2, F3 | `<Dev không ghi — Leader điền>` |

---

## 5. Recover data (nguyên văn từ Dev)

✔ **Không cần recover data**

## 6. Verify của Dev (nguyên văn từ Dev)

**Mức: `unit-test`**

**Lệnh đã chạy:**
- `php -l app/Conversation.php` → No syntax errors detected
- `php -l tests/Feature/FriendFilterSubqueryTypeTest.php` → No syntax errors detected
- `vendor/bin/phpunit --filter FriendFilterSubqueryTypeTest` → OK (11 tests, 21 assertions)
- Chạy chính test đó trên code **TRƯỚC** khi fix: Tests 11, Failures 10 — xác nhận test bắt đúng thay đổi, không phải test rỗng
- `vendor/bin/phpunit --filter PlanLimitGuardTest` (test có sẵn) → OK (7 tests, 18 assertions) — bộ test cũ không bị ảnh hưởng
- Dump câu SQL sinh ra (chỉ `toSql`, không kết nối DB): truy vấn con đổi thành `select CAST(conversation.line_id AS SIGNED) from conversation`, thứ tự và giá trị tham số binding giữ nguyên

**Bằng chứng:**
- Kiểu cột: `conversation.line_id` = `varchar(255)`, `bot_line_user.line_user_id` = `int(11)` (`share/db/db-structure/tables/*.sql`) → hai vế `IN` khác kiểu
- `line_id` của bảng hội thoại chứa `line_user.id` dạng chuỗi: `FriendMemoRepository::resolveConversationId` tra bằng `where('line_id', (string) $lineUserId)`; các model `Messages*` join `conversation.line_id = line_user.id`
- Các bảng khác dùng trong bộ lọc (`friend_information_value.line_id`) đã là `int(11)` nên không dính lỗi so kiểu — khớp với việc SQL trong ticket chỉ hiện truy vấn con của bảng `conversation`
- ⚠️ **CHƯA EXPLAIN được trên môi trường dev**: MySQL `host.docker.internal:3306` và web `:8000` đều **Connection refused** trong lúc xử lý — **cần dev/QA chạy EXPLAIN để đo trước/sau**

## 7. Tự review của AI + rủi ro khi test (nguyên văn từ Dev)

Fix tối thiểu, đúng nguyên nhân gốc: chỉ đổi KIỂU của cột trả về trong truy vấn con (varchar sang số) mà giữ nguyên bảng, điều kiện lọc và thứ tự tham số. Không có nhánh nghiệp vụ nào bị đổi. Tập kết quả không đổi vì MySQL vốn đã ép chuỗi về số khi so với cột int; dùng `SIGNED` (không phải `UNSIGNED`) để giá trị âm hoặc chuỗi không hợp lệ không bị tràn thành số dương lớn. Trường hợp xấu nhất cũng không tệ hơn hiện tại: nếu MySQL vẫn chọn cách chạy theo từng dòng thì điều kiện đẩy xuống vẫn không dùng được index y như trước, còn nếu chọn được bảng tạm thì nhanh hơn hẳn. Đã bổ sung test khoá hình dạng SQL (đã chứng minh test FAIL trên code cũ).

**Rủi ro / lưu ý khi test (nguyên văn — đây là input quan trọng nhất để viết TC):**
- **CHƯA đo được trước/sau bằng EXPLAIN** vì MySQL và web dev trong container đều không kết nối được lúc xử lý — đề nghị dev/QA chạy EXPLAIN trên **bot nhiều bạn bè** để xác nhận truy vấn con chuyển sang `MATERIALIZED` và đo thời gian
- Nếu bảng `conversation` của bot quá lớn, bảng tạm materialize có thể **vượt `tmp_table_size` và rơi xuống đĩa** — vẫn nhanh hơn nhiều so với chạy lại theo từng dòng, nhưng nên theo dõi
- Cách tối ưu triệt để hơn (đổi sang `EXISTS` tương quan, hoặc dùng cột số `conversation.tb_line_user_id` thay cho `line_id`) **KHÔNG chọn lần này** vì: `EXISTS` chỉ nhanh khi có index phù hợp trên `(bot_id, line_id)` mà chưa xác minh được index thật; còn **`tb_line_user_id` cho phép NULL nên có nguy cơ lọc thiếu bạn bè**. Nếu DBA xác nhận index và `tb_line_user_id` luôn có giá trị thì có thể tối ưu thêm ở ticket sau.
  - 🔴 **Mâu thuẫn với mục 2 (vòng 2 nói ĐÃ dùng `tb_line_user_id`)** — xem cảnh báo đầu file.
- **Base branch** dùng `release_step_20260805` theo cấu hình hiện tại; trên origin còn `release_staging_20260810` và `release_step_20260827` mới hơn — nếu release đích khác thì **human chọn lại nhánh gốc trước khi push**

## 8. Bối cảnh liên quan

- Dạng subquery gây chậm **mới xuất hiện từ ticket #39667** → khi rà regression / TC cũ, nên tra ticket #39667 để biết bộ lọc nào được đổi sang subquery ở lần đó.
- Thời gian AI xử lý: 2 giờ 34 phút.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **⚠️ phải chốt CAST hay `tb_line_user_id` trước (xem cảnh báo đầu file)**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **⚠️ 4.1 gốc chỉ là list FILE, bảng F* là do `/new-task` ghép từ mục 3**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — **⚠️ Dev không điền mức nguy cơ regression cho T1–T8**
- [ ] Đã hỏi Dev: `conversation.tb_line_user_id` có row NULL không / đã backfill chưa
- [ ] Đã yêu cầu Dev hoặc QA chạy **EXPLAIN + đo thời gian trước/sau** trên bot nhiều bạn bè (Dev chưa làm được)
