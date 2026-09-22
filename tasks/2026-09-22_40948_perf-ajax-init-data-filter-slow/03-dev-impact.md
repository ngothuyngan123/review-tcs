# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `62edff4a8e` (repo `sns-line`, 1 file) — `<chưa có link PR>` |
| Branch | `ai_small_40948` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-21` (Journal #137322) |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Endpoint `/ajax/init-data-filter` chạy câu truy vấn lọc bạn bè (rất nặng) **HAI lần** cho mỗi request: một lần đếm số người, một lần nữa lấy toàn bộ danh sách ID bạn bè rồi dựng thành đối tượng và đóng gói ra JSON. Danh sách ID đó lại được trả cho gần như **mọi màn hình gọi tới**, trong khi chỉ màn tạo file CSV và phân tích chéo mới thực sự đọc nó. Bot nhiều bạn bè và bộ lọc rỗng (quét toàn bộ bạn bè) thì chi phí gấp đôi này kéo request lên hàng chục giây.

## 2. Cách fix

Trong `FilterController::initDataFilter`, thay **3 cặp lệnh đếm-rồi-lấy-toàn-bộ-ID** bằng hàm dùng chung `countFilterResult`: chạy câu lọc đúng **MỘT lần**, chỉ lấy danh sách ID cho **5 loại màn** thực sự đọc nó (tạo file CSV, phân tích chéo, 3 màn cấu hình gửi tin sau khi đặt lịch), còn lại chỉ đếm.

Hàm `countFilterResult` và hằng danh sách màn **lấy nguyên từ ticket #40986** (đang chờ review) để hai nhánh gộp lại không đụng nhau.

**Quét ngang:** cùng mẫu lỗi còn ở `saveFilterV2` (đã xử lý ở #40986) và ở **API lọc phía mobile (ngoài phạm vi)**.

**Bằng chứng Dev đưa ra:**
- Câu SQL cách cũ `select('bot_line_user.line_user_id')->get()` và cách mới `pluck()` sinh SQL **giống nhau** (builder có `columns = NULL`).
- `stripTableForPluck('bot_line_user.line_user_id') = 'line_user_id'` → mảng trả ra `[['line_user_id'=>id],...]` **trùng định dạng cũ**, giao diện không phải sửa.
- Builder do `advanceFilterPost` trả về có `groups=NULL`, `distinct=false`, `limit=NULL` (cả khi bộ lọc rỗng lẫn khi có điều kiện AND/OR) → `count(*)` bằng đúng số dòng lấy về.
- Chỉ **2 chỗ** trong giao diện đọc `response.line_user_ids` của endpoint này: `public/js/friendlist/modal_filter_v2.js` và `public/js/talk_list/modal_filter_message.js` (đều cho `csv_create_download_file` + `cross_analysis`) — cả 2 đều nằm trong danh sách trắng.
- Các màn lịch (`calendar-*-setting-status-send-after-booking`) đọc `line_user_ids` từ response của `save-filter-v2` chứ **không phải** endpoint này, nhưng vẫn giữ trong danh sách trắng cho an toàn.
- `public/js/schedules/plan.js` lưu cả response nhưng **chỉ đọc `number_filter`**.

⚠️ **Mức verify của Dev chỉ là `lint`** — `php -l` pass; **chưa chạy unit test / chưa kiểm chứng trên dữ liệu thật** (MySQL dev không kết nối được — Connection refused). **Chưa đo được thời gian phản hồi thực tế**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FilterController::initDataFilter` — `app/Http/Controllers/Basic/FilterController.php` | **ĐÃ SỬA** — thay 3 cặp đếm + lấy toàn bộ ID bằng `countFilterResult` | Điểm fix chính |
| 2 | `FilterController::countFilterResult` — `app/Http/Controllers/Basic/FilterController.php` | **THÊM MỚI** — chép nguyên văn từ nhánh #40986 | Hàm dùng chung: chạy câu lọc 1 lần, chỉ lấy ID cho màn trong danh sách trắng |
| 3 | `FilterController::saveFilterV2` — `app/Http/Controllers/Basic/FilterController.php` | Không sửa ở nhánh này | Cùng mẫu lỗi nhưng đã xử lý ở #40986 |
| 4 | `FilterController::countAllFriend` — `app/Http/Controllers/Basic/FilterController.php` | Không sửa | Đã check, không ảnh hưởng |
| 5 | `Conversation::advanceFilterPost` — `app/Conversation.php` | Không sửa | Nguồn sinh builder lọc — đã verify `groups/distinct/limit` NULL nên `count(*)` tương đương |
| 6 | `initDataFilter` — `public/js/friendlist/modal_filter_v2.js` | Không sửa | 1 trong 2 chỗ đọc `line_user_ids` (csv_create_download_file, cross_analysis) — nằm trong danh sách trắng |
| 7 | `initDataFilter` — `public/js/talk_list/modal_filter_message.js` | Không sửa | Chỗ còn lại đọc `line_user_ids` (cùng 2 loại màn) — nằm trong danh sách trắng |
| 8 | `getDataFilter` — `public/js/schedules/plan.js` | Không sửa | Lưu cả response nhưng chỉ đọc `number_filter` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FilterController::initDataFilter` (endpoint `POST /ajax/init-data-filter`) | `app/Http/Controllers/Basic/FilterController.php` | Direct | Điểm sửa duy nhất — **file thay đổi duy nhất của nhánh fix** |
| F2 | `FilterController::countFilterResult` | `app/Http/Controllers/Basic/FilterController.php` | Direct (thêm mới) | Chép nguyên văn từ #40986 — rủi ro xung đột merge nếu #40986 đổi nội dung |
| F3 | `Conversation::advanceFilterPost` | `app/Conversation.php` | Indirect | Không sửa; là nguồn builder lọc, kết luận "count(*) = số dòng" phụ thuộc vào builder này |
| F4 | JS đọc `line_user_ids`: `initDataFilter` (`modal_filter_v2.js`) · `initDataFilter` (`modal_filter_message.js`) · `getDataFilter` (`plan.js`) | `public/js/...` | Indirect | Không sửa; là bên tiêu thụ response bị đổi nội dung |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Không có** — thay đổi chỉ ở tầng **đọc** dữ liệu, không ghi/sửa bảng nào. Dev xác nhận **không cần recover data**. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend Filter (SC-003)** — modal lọc bạn bè dùng chung: nạp lại điều kiện lọc + đếm số người nay chỉ chạy truy vấn 1 lần | F1, F2 | High |
| T2 | **CSV Management (FA-014)** — màn tạo file CSV vẫn nhận đủ danh sách ID bạn bè như cũ | F1 | High |
| T3 | **Cross Analysis (FA-024)** — màn phân tích chéo vẫn nhận đủ danh sách ID bạn bè như cũ | F1 | High |
| T4 | **Auto Reply (FA-003)** — chỉ dùng số người lọc được, nay **không còn nhận mảng ID** thừa | F1 | Medium |
| T5 | **Action Schedule (FA-016)** — chỉ dùng số người lọc được, nay **không còn nhận mảng ID** thừa | F1 | Medium |
| T6 | **Rich Menu (FA-004)** — màn cấu hình hiển thị rich menu chỉ dùng số người lọc được | F1 | Medium |
| T7 | **Broadcast (FA-008)** — không đổi (trước nay vẫn không nhận mảng ID) | F1 | Low |

**Rủi ro / lưu ý khi test (Dev tự nêu):**

1. `countFilterResult` + hằng danh sách màn chép **NGUYÊN VĂN** từ nhánh #40986 (cùng file, chưa merge release). Hai nhánh cùng lên thì git gộp sạch vì phần thêm giống hệt nhau; nhưng nếu **#40986 bị sửa nội dung trong lúc review** thì xung đột ở khối này — người duyệt cần gộp thủ công.
2. Các màn **ngoài danh sách trắng** nay nhận `line_user_ids` **rỗng**. Dev đã rà toàn bộ `public/js` + `resources/views`, không nơi nào đọc trường này ngoài 2 màn CSV và phân tích chéo; màn mới cần thì phải thêm loại màn vào hằng danh sách trắng.
3. **Chưa đo được thời gian thực tế** vì MySQL dev không kết nối được — mức cải thiện chỉ là **suy luận** (2 lượt truy vấn nặng → 1 lượt + bỏ tải toàn bộ ID cho phần lớn màn).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
