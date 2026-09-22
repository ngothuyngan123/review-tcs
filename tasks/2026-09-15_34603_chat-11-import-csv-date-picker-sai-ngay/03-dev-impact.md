# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME)` — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `commit 8901ae8ce7` (repo `sns-line`) — không có link PR trong ticket |
| Branch | `ai_fixbug_34603` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-28` (Journal #133387) |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn mục **■ 1. NGUYÊN NHÂN** — Journal #133387.

Ô sửa ngày trong khung Thông tin bạn bè của màn Chat 1:1 là ô nhập ngày chuẩn của trình duyệt, chỉ chấp nhận chuỗi `yyyy-mm-dd` đủ 2 chữ số. Giá trị nhập từ file CSV được lưu nguyên định dạng gốc (`2026/1/5`, `2026-1-5`, `2026/01/05`...) nên trình duyệt coi là không hợp lệ, bỏ trắng ô và bộ chọn ngày không lấy được ngày tương ứng. Khi bấm ra ngoài, màn hình gửi lại đúng chuỗi gốc đó lên máy chủ và bị chặn bởi bước kiểm tra định dạng chặt (chỉ nhận đủ 2 chữ số) nên hiện thông báo sai định dạng.

## 2. Cách fix

> Nguyên văn mục **■ 2. CÁCH FIX** — Journal #133387.

Sửa màn Chat 1:1 (`public/js/chats/chat-v2.js`): thêm 2 hàm nhận diện trường ngày và chuẩn hoá giá trị ngày, gọi ngay trong `editItemInfo` trước khi mở ô sửa — mọi định dạng đã lưu (`2026-1-5`, `2026-01-5`, `2026-1-05`, `2026/1/5`, `2026/1/05`, `2026/01/5`, `2026/01/05`, kèm cả phần giờ) được đổi về `yyyy-mm-dd` đủ 2 chữ số để ô nhập ngày của trình duyệt hiển thị đúng ngày và giá trị gửi lên khi rời ô qua được bước kiểm tra định dạng. Giá trị không đọc được thành ngày thì giữ nguyên, không tự ý ghi đè. Quét ngang: các chỗ dùng ô nhập ngày khác đều nhận giá trị do người dùng chọn từ bộ chọn nên không dính lỗi này.

**Kết quả verify của Dev (mức `lint`, trích ■ 6. VERIFY):**

- `node --check public/js/chats/chat-v2.js` → OK (không sửa file PHP nên không chạy `php -l`).
- Chạy thử riêng hàm `normalizeDateItemValue` tách rời với 7 định dạng trong ticket: `2026-1-5` / `2026-01-5` / `2026-1-05` / `2026/01/05` / `2026/1/5` / `2026/1/05` / `2026/01/5` → đều ra `2026-01-05`.
- Chuỗi kèm giờ (`2026-01-05 00:00:00`, `2026-01-05T00:00:00`) → `2026-01-05`.
- Chuỗi rỗng / `null` / `abc` / `05-01-2026` / `2026-13-45` / `2026-02-30` → trả `null` nên **giữ nguyên giá trị gốc**.
- `git diff --stat origin/release_step_20260805...ai_fixbug_34603`: chỉ **1 file** `public/js/chats/chat-v2.js`, **+31 dòng**.

⚠️ **KHÔNG tái hiện được trên dev**: MySQL `host.docker.internal:3306` và web `host.docker.internal:8000` đều Connection refused tại thời điểm xử lý → **chưa có bằng chứng chạy thật trên UI**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục **■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN** — Dev list dạng plain, convert sang bảng template.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `editItemInfo` — `public/js/chats/chat-v2.js` | **Sửa** — gọi 2 hàm mới trước khi mở ô sửa | Điểm fix chính: chuẩn hoá value trước khi bind vào `input type=date` |
| 2 | `isDateItemInfo` — `public/js/chats/chat-v2.js` | **Thêm mới** | Nhận diện trường thuộc kiểu ngày |
| 3 | `normalizeDateItemValue` — `public/js/chats/chat-v2.js` | **Thêm mới** | Chuẩn hoá mọi định dạng đã lưu về `yyyy-mm-dd`; không parse được → trả `null`, giữ nguyên giá trị gốc |
| 4 | `saveItemInfo` — `public/js/chats/chat-v2.js` | Không sửa — đã check | Hàm gửi giá trị lên server khi rời ô |
| 5 | `formatString` — `public/js/chats/chat-v2.js` | Không sửa — đã check | Hàm format hiển thị (`yyyy.mm.dd` ở danh sách) |
| 6 | `initFriendInfo` — `public/js/chats/chat-v2.js` | Không sửa — đã check | Khởi tạo panel 友だち情報 |
| 7 | `ChatController::getInfoDisplayChat` — `app/Http/Controllers/ChatController.php` | Không sửa — đã check | API trả dữ liệu hiển thị panel |
| 8 | `ChatController::saveSettingDisplayInfoItem` — `app/Http/Controllers/ChatController.php` | Không sửa — đã check | Validate định dạng ngày phía server (dòng 4537 cho 誕生日 mặc định, 4677 cho trường tự tạo kiểu 年月日) |
| 9 | `HandleImportCsv::readDataCSV_V1` — `app/Console/Commands/HandleImportCsv.php` | Không sửa — đã check | Luồng import CSV sinh ra data định dạng gốc |
| 10 | `friend_info.blade.php` khối sửa ngày — `resources/views/basic/chat/tab_right_side/friend_info.blade.php` | Không sửa — đã check | Dòng 79: `input type=date` bind thẳng `v-model` vào giá trị lấy từ DB |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ kê **file thay đổi** ở mục 4.1 (1 file). Bảng dưới suy từ mục 2 + 3, giữ nguyên nội dung Dev cung cấp — không thêm impact mới.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `editItemInfo` | `public/js/chats/chat-v2.js` | Direct | Điểm sửa chính — thêm 5 dòng gọi 2 hàm mới trước khi mở ô sửa |
| F2 | `isDateItemInfo` (mới) | `public/js/chats/chat-v2.js` | Direct | Hàm mới — nhận diện trường kiểu ngày |
| F3 | `normalizeDateItemValue` (mới) | `public/js/chats/chat-v2.js` | Direct | Hàm mới — chuẩn hoá value; giá trị không parse được trả `null` |
| F4 | `saveItemInfo` | `public/js/chats/chat-v2.js` | Indirect | Nhận value đã chuẩn hoá → payload gửi server đổi so với trước fix |
| F5 | `ChatController::saveSettingDisplayInfoItem` | `app/Http/Controllers/ChatController.php` | Indirect | **Không sửa code** — nhưng nay nhận value đã chuẩn hoá nên qua được validate; vẫn phải tự chặn khi request không đi qua UI |
| F6 | `formatString` / `initFriendInfo` / `ChatController::getInfoDisplayChat` | `chat-v2.js` / `ChatController.php` | Indirect | Không sửa — đường hiển thị danh sách (`yyyy.mm.dd`) giữ nguyên |

⚠️ **Lưu ý cho Leader**: `editItemInfo` là **hàm dùng chung cho mọi loại trường** trong panel 友だち情報 (text, số, lựa chọn, điểm, ảnh, PDF...), không riêng trường ngày → phải kiểm regression các loại trường còn lại (Studio đã kê ở REQ-004).

### 4.2. List data bị update khi fix bug

> Nguyên văn mục **■ 4.2 Data ảnh hưởng**: "Không có — không sửa cấu trúc hay dữ liệu sẵn có."

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_information_value.value` | UPDATE (gián tiếp, do người dùng) | **Không migrate**. Chỉ khi người dùng mở ô sửa ngày trong Chat 1:1 rồi rời ô thì giá trị đang lưu được **ghi lại theo chuẩn `yyyy-mm-dd`** (đúng như server vẫn chuẩn hoá khi lưu) |
| D2 | Bảng lịch sử thay đổi thông tin bạn bè | CREATE (gián tiếp) | Lần rời ô **đầu tiên** của value định dạng cũ sinh **1 bản ghi** cũ→mới, kể cả khi người dùng không đổi gì. Dev khẳng định đây là hành vi vốn có (rời ô là lưu) |
| D3 | Schema / migration | Không có | Không đụng cấu trúc DB, không cần recover data (mục ■ 5) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục **■ 4.3 Tính năng liên quan**.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — khung 友だち情報: ô sửa ngày và bộ chọn ngày hiển thị đúng giá trị đang lưu | F1, F2, F3, F4 | High |
| T2 | **Friend Information (FA-015)** — trường kiểu 年月日 và 誕生日 khi sửa từ màn chat được lưu theo định dạng chuẩn | F4, F5, D1, D2 | High |
| T3 | Các trường **không phải ngày** trong cùng panel 友だち情報 (text / số / lựa chọn / điểm / ảnh / PDF) | F1 (hàm dùng chung) | Medium — Dev **không kê**, bổ sung từ REQ-004 phía Studio |

## BUG — root cause / cách fix (tag dùng cho coverage)

| Tag | Nội dung |
|---|---|
| `BUG` | `input type=date` của trình duyệt chỉ nhận `yyyy-mm-dd` đủ 2 chữ số; value import CSV lưu nguyên định dạng gốc → ô bỏ trắng + server validate chặt chặn khi blur. Fix = chuẩn hoá value phía client ngay trước khi mở ô sửa (`editItemInfo`), giá trị không parse được thì giữ nguyên. |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn cần hỏi Dev / lưu ý khi review

1. `editItemInfo` là **hàm dùng chung** cho mọi loại trường nhưng Dev **không liệt kê danh sách loại trường đã kiểm** ở mục 4.3 → rủi ro regression trường text có giá trị trông giống ngày bị tự chuẩn hoá.
2. Fix chỉ ở **client JS** — request gọi thẳng API (không qua UI) vẫn dùng validate cũ. Cần xác nhận đây là chủ đích (server là tầng chặn cuối).
3. Dev **không tái hiện được trên dev** (Connection refused) → toàn bộ verify là lint + unit thủ công, **không có evidence UI**.
4. Bug gốc nói value `yyyy.mm.dd` hiển thị ở panel — cần xác nhận cách **hiển thị danh sách** (`yyyy.mm.dd`) không đổi sau fix.
