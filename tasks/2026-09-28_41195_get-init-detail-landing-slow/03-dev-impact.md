# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.
>
> ⚠️ Ticket #41195 đã qua **6 vòng auto-fixbug** (Journal #137424 → #138926, 2026-09-21 → 2026-09-28). File này **chỉ chép Journal MỚI NHẤT (#138926, 2026-09-28)** — bản tổng hợp/cuối cùng, bao gồm và ghi đè toàn bộ nội dung các vòng trước. Lịch sử đầy đủ 6 vòng xem ở `01-bug-task.md` mục "Journal / note từ Redmine".

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `32138de948` (repo `sns-line`, 3 file — vòng fix cuối) — `<chưa có link PR>`. Lịch sử commit các vòng trước: a65732db21 → 8068076166 → 5783fd952d → 3ec0049f52 → e942090680 → **32138de948 (mới nhất)** |
| Branch | `ai_small_41195` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-28` (Journal #138926) |
| Auto-filled | `2026-09-28 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (Journal #138926 + lịch sử 5 vòng trước ở file 01) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Endpoint `POST /ajax/v2/landing/get-init-detail-landing` phục vụ màn Chi tiết dữ liệu của QR/Trang đích (tab thống kê theo ngày / danh sách bạn bè / trang đích). **Ba nút nghẽn gốc:**

1. Tab Trang đích ghép bảng lượt mở với bảng nhật ký click qua cột `collect_id` vốn **không có chỉ mục**, nên mỗi dòng lượt mở phải quét cạn bảng nhật ký click dùng chung toàn hệ thống — câu ghép nặng này còn chạy **3 lần trong một request** (dòng tổng, đếm phân trang, danh sách); ghép phụ theo mã trang đích cũng thiếu chỉ mục.
2. Thống kê của ngày hôm nay bọc hàm `DATE()` lên cột thời gian nên **không dùng được chỉ mục**, phải mở toàn bộ lịch sử click của trang đích — chạy ở **MỌI lần mở màn mặc định**.
3. Tab danh sách bạn bè ghép mốc thêm bạn đầu tiên bằng **hai vòng lặp lồng nhau trong PHP** (số dòng × số bạn) nên bản xuất CSV của trang đích nhiều lượt click treo rất lâu.

**Bổ sung phát hiện ở subtask #41667** (sau khi vòng fix trước đã release và tester đo lại): tab 「友だち一覧」 vẫn chậm **352.3s**. Nguyên nhân: vòng fix trước áp `CONVERT(detail_landing_click.line_id USING utf8) COLLATE utf8_unicode_ci` cho **MỌI** chỗ ghép `detail_landing_click` ↔ `line_user`, kể cả câu đếm số bạn bị chặn (`totalBlock`). Ở câu đếm đó, điều kiện lọc `conversation.is_blocked = 1` mới là điều kiện chọn lọc nhất nên MySQL lái từ `conversation` → `line_user` (theo khóa chính `tb_line_user_id`) rồi **TRA** `detail_landing_click` theo `line_id`; bọc `CONVERT` lên chính cột được tra làm chỉ mục `detail_landing_click_bot_line_landing_index (bot_id, line_id(64), landing_id)` **vô hiệu** ⇒ bảng log về kiểu truy cập `ALL` (206.859 dòng, `Using join buffer`), bị quét lại cho từng bạn bị chặn. Tức chiều `CONVERT` (cần cho chỉ mục `line_user.line_id`) chỉ đúng khi `detail_landing_click` là bảng **LÁI**; ở câu đếm này nó lại là bảng **được tra** nên `CONVERT` chỉ có hại.

## 2. Cách fix

Tối ưu endpoint chi tiết dữ liệu QR/trang đích, **KHÔNG đổi dữ liệu trả về và KHÔNG đổi schema** — toàn bộ tối ưu nằm ở phía câu truy vấn (migration index của các vòng đầu đã bị **xoá hẳn** ở vòng fix 4, vì production đã có sẵn các chỉ mục cần dùng).

1. Đổi điều kiện thống kê ngày hôm nay (`handleAttributeCurrentDay`) từ `DATE(time_click) = hôm nay` sang khoảng nửa mở `[00:00:00 hôm nay, 00:00:00 ngày mai)` để dùng được chỉ mục (tương đương tuyệt đối với cột DATETIME: bản ghi 23:59:59 vẫn lấy, NULL vẫn bị loại).
2. Thay hai vòng lặp lồng nhau tính cờ đã chặn ở tab danh sách bạn bè (tab2) bằng **bảng tra theo `line_id`** (số dòng + số bạn thay vì số dòng × số bạn) — nguyên nhân treo khi xuất CSV.
3. Câu đếm số bạn bị chặn (`totalBlock`, tab2): quay lại **correlated `NOT EXISTS`** đúng đoạn code human chỉ định (alias `o`: `bot_id = botId`, `line_id = dòng ngoài`, `action = 2`, `landing_id != landing hiện tại`, `time_click < dòng ngoài`), bỏ derived table pre-aggregate mà ticket #32481 đã thay vào — derived table phải `GROUP BY` TOÀN BỘ click `action=2` của cả bot nên mỗi request dựng bảng tạm rất lớn; bản `NOT EXISTS` bám được chỉ mục `detail_landing_click(bot_id, line_id, landing_id)` (migration `2026_09_15_103000` của #40997, đã có trong release branch). Kèm lợi ích: `botId`/`landingId` đi qua binding tham số thay vì nối chuỗi vào SQL thô.
4. Gỡ nút nghẽn **lệch collation** ở phép ghép `detail_landing_click.line_id = line_user.line_id`: `detail_landing_click.line_id` là `utf8mb4_unicode_ci` còn `line_user.line_id` là `utf8_unicode_ci` (bảng cũ charset utf8) → MySQL phải nâng vế utf8 (cột CÓ chỉ mục) lên utf8mb4 cho TỪNG dòng ⇒ chỉ mục `line_user.line_id` vô hiệu. Sửa: hạ vế `detail_landing_click.line_id` về utf8 bằng hằng dùng chung `DetailLandingClick::JOIN_LINE_ID_UTF8 = "CONVERT(detail_landing_click.line_id USING utf8) COLLATE utf8_unicode_ci"` ở `QRCodeController::ajaxInitDataDetailV2` (nhánh keyword + nhánh totalBlock ban đầu) và `DetailLandingClick::firstAddFriends` (nhánh keyword).
5. Bỏ hẳn migration tạo chỉ mục (`2026_09_21_100000`) vì DB thật đã có sẵn — branch không còn thay đổi schema nào.
6. Áp fix collation sang **case tương tự**: **SỬA** `app/Http/Controllers/Ajax/PopupAjaxController.php:643` (`initDataDetailClick`, tab2 màn Chi tiết lượt bấm Popup FA-018, chạy MỌI lần mở tab) — dùng lại hằng `JOIN_LINE_ID_UTF8` + thêm import `Illuminate\Support\Facades\DB`. **KHÔNG SỬA (cố ý)** `QrActionHistoryRepository.php:25` và `NotifyController.php:190` vì ở đó `line_user` được lấy trước theo khóa chính / đứng vai bảng ngoài nên chỉ mục `detail_landing_click` vẫn dùng được — bọc `CONVERT` sẽ làm **hỏng** chiều index đang dùng. Grep toàn repo xác nhận đúng 5 vị trí ghép `detail_landing_click` ↔ `line_user`, không sót.
7. **[SPEC BỔ SUNG 2026-09-28 — subtask #41667, vòng fix mới nhất]** Câu đếm số bạn bị chặn (ô 「ブロック」) ở tab 「友だち一覧」: **BỎ** `CONVERT(...USING utf8) COLLATE utf8_unicode_ci` khỏi điều kiện ghép `line_user` của **CHÍNH câu đếm này**, quay lại so thẳng hai cột `detail_landing_click.line_id = line_user.line_id` (giữ nguyên `NOT EXISTS` của vòng trước). Nhánh **CÓ** từ khóa vẫn kế thừa join `CONVERT` từ `$queryDetail` (câu danh sách cần chiều đó) nên thêm điều kiện so thẳng **tương đương** ở `WHERE` để nếu câu đếm lái từ `conversation` thì MySQL vẫn còn đường bám chỉ mục. Docblock hằng `JOIN_LINE_ID_UTF8` bổ sung luật dùng **theo CHIỀU** (chỉ bọc `CONVERT` khi `detail_landing_click` là bảng lái; khi `detail_landing_click` là bảng được tra thì phải so thẳng) để không tái phạm. 3 vị trí còn lại (QRCodeController nhánh keyword, `DetailLandingClick::firstAddFriends`, `PopupAjaxController` tab2) giữ `CONVERT` vì ở đó `detail_landing_click` vẫn là bảng lái.

**Bằng chứng Dev đưa ra:**
- Chỉ mục hiện có của `detail_landing_click` trên release: `PK(id)`, `landing_id` (2020_06_15), `code` (2025_06_13), `(bot_id, line_id(64), landing_id)` (2026_09_15_103000 của #40997) — KHÔNG có `collect_id`, KHÔNG có `(landing_id, time_click)` trong migration repo (production được human xác nhận đã có sẵn ngoài migration).
- Harness so sánh thuật toán cũ/mới trên 300 bộ dữ liệu ngẫu nhiên (cờ `is_blocked`) + 9 mốc thời gian biên (điều kiện ngày) — khớp 100%.
- Dựng lại câu truy vấn bằng Illuminate query builder (`MySqlGrammar`) để in SQL + binding, xác nhận sinh đúng câu `CONVERT`/`NOT EXISTS` dự kiến, tham số hoá đúng thứ tự.
- Tester #41667 đo thực tế trên dữ liệu quy mô thật (200.055 dòng log, 1 landing 50.000 dòng/10.000 bạn, 1.200 bạn bị chặn): câu đếm 352.3s → 0.2s sau khi bỏ `CONVERT`, EXPLAIN `type=ALL` (206.859 dòng, join buffer) → `type=ref` (`ref=const,func,const`), kết quả số đếm giữ nguyên (545).
- ⚠️ **Chưa chạy được EXPLAIN trên DB dev** trong toàn bộ 6 vòng fix — MySQL `host.docker.internal:3306` liên tục connection refused từ container; số liệu cải thiện của vòng cuối lấy từ phép đo thực tế của tester ở #41667, KHÔNG phải EXPLAIN tự chạy của AI.
- **Lưu ý hành vi biên** (từ vòng fix 2, chưa đổi): khi một bạn có lượt thêm bạn ở trang đích KHÁC trùng CHÍNH XÁC tới giây với lượt ở trang đích đang xem, bản derived table (code cũ trước #32481) loại bạn đó khỏi số đếm, bản `NOT EXISTS` (code sau fix) thì vẫn tính — đây là quay về đúng hành vi gốc trước #32481, không phải hành vi mới.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `QRCodeController::ajaxInitDataDetailV2` — `app/Http/Controllers/Basic/QRCodeController.php` | **ĐÃ SỬA** — 2 chỗ ghép `line_user` (nhánh keyword giữ `CONVERT`; nhánh totalBlock bỏ `CONVERT`, so thẳng + thêm điều kiện tương đương cho nhánh có từ khóa); NOT EXISTS thay derived table | Điểm fix chính — câu đếm 「ブロック」 và câu danh sách trang đích |
| 2 | `QRCodeController::handleAttributeCurrentDay` — cùng file | **ĐÃ SỬA** — `DATE()=hôm nay` → khoảng nửa mở | Chạy ở MỌI lần mở màn mặc định (tab 数値情報) |
| 3 | `QRCodeController::ajaxInitDataDetail` (bản v1) — cùng file | Không sửa | Đã kiểm: không ghép `line_user`, không ảnh hưởng |
| 4 | `DetailLandingClick::firstAddFriends` + hằng `JOIN_LINE_ID_UTF8` — `app/DetailLandingClick.php` | **ĐÃ SỬA** — dùng `JOIN_LINE_ID_UTF8` (nhánh keyword), bảng tra theo `line_id` thay vòng lặp lồng nhau | Nguyên nhân treo khi xuất CSV trang đích nhiều click |
| 5 | `DetailLandingClick::lineUser` — cùng file | Không sửa | `hasOne` eager load bằng `whereIn` giá trị literal → không bị lệch collation |
| 6 | `CollectOpenLanding::detailLandingClick` — `app/CollectOpenLanding.php` | Không sửa | Hưởng lợi gián tiếp từ chỉ mục `collect_id` có sẵn trên production |
| 7 | `initDetailLanding` / `initDetailClickDay` — `public/js/qr_code/v2/detail.js` | Không sửa | Đã kiểm, không cần đổi vì response giữ nguyên |
| 8 | `PopupAjaxController::initDataDetailClick` — `app/Http/Controllers/Ajax/PopupAjaxController.php` | **ĐÃ SỬA** (vòng fix 5) — dùng `JOIN_LINE_ID_UTF8` + thêm import `DB` facade | Case tương tự — bảng lái vẫn là `detail_landing_click`, cần `CONVERT` |
| 9 | `QrActionHistoryRepository::paginateByFriend` — `app/Repositories/Eloquents/QrActionHistoryRepository.php` | Không sửa (cố ý) | `line_user` lấy trước theo khóa chính → chỉ mục `detail_landing_click` vẫn dùng được; bọc `CONVERT` sẽ hỏng chiều index |
| 10 | `NotifyController` subquery qr_code — `app/Http/Controllers/Api/NotifyController.php:190` | Không sửa (cố ý) | `line_user` là bảng ngoài trong subquery tương quan → không dính lỗi collation. Điểm còn tồn (yokoten, ngoài phạm vi): subquery thiếu `bot_id` nên chưa dùng hết chỉ mục — mỗi trang chỉ 10 dòng nên chưa đáng lo |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `QRCodeController::ajaxInitDataDetailV2` (EP-53) | `app/Http/Controllers/Basic/QRCodeController.php` | Direct | Rewrite query: NOT EXISTS thay derived table, bỏ `DATE()`, chiều `CONVERT` theo bảng lái |
| F2 | `QRCodeController::handleAttributeCurrentDay` | cùng file | Direct | Khoảng nửa mở thay `DATE(time_click)=hôm nay` |
| F3 | `DetailLandingClick::firstAddFriends` + hằng `JOIN_LINE_ID_UTF8` | `app/DetailLandingClick.php` | Direct | Bảng tra theo `line_id` thay vòng lặp lồng nhau; dùng hằng CONVERT dùng chung |
| F4 | `PopupAjaxController::initDataDetailClick` | `app/Http/Controllers/Ajax/PopupAjaxController.php` | Direct | Áp cùng hằng `JOIN_LINE_ID_UTF8` (case tương tự, ngoài phạm vi endpoint gốc nhưng cùng root cause) |
| F5 | `CollectOpenLanding::detailLandingClick` | `app/CollectOpenLanding.php` | Indirect | Hưởng lợi gián tiếp từ chỉ mục `collect_id` có sẵn trên production, không sửa code |
| F6 | `QrActionHistoryRepository::paginateByFriend`, `NotifyController` subquery | tương ứng | Indirect (đã loại trừ) | Rà nhưng cố ý KHÔNG sửa — khác chiều index, xem mục 3 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `detail_landing_click` | Không CREATE/UPDATE/DELETE dữ liệu — chỉ đổi **cách viết điều kiện ghép** trong câu SELECT/COUNT | Migration index của các vòng đầu đã bị **xoá hẳn** ở vòng fix 4 (production đã có sẵn `(landing_id, time_click)`, `(bot_id, line_id, landing_id)`) — branch hiện tại **KHÔNG đổi schema** |
| D2 | `line_user` | Không đổi | Không đổi schema/dữ liệu; chỉ ảnh hưởng ở việc chỉ mục `line_id` có được dùng hay không tuỳ chiều `CONVERT` |
| D3 | Kết quả trả về (JSON EP-53, phân trang, thứ tự sắp xếp, file CSV) | Không đổi | Dev khẳng định nhiều lần qua các vòng: chỉ đổi cách viết truy vấn, không đổi output — cần Tester verify độc lập vì AI chưa chạy được EXPLAIN/so dữ liệu thật trên dev |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | QR Code Action / Landing (FA-017) — màn 「QRコードアクション（詳細データ）」: tab 数値情報 (ngày hôm nay) | F2 | Medium — logic điều kiện ngày đổi, cần verify đúng biên 00:00:00/23:59:59 theo timezone Asia/Tokyo |
| T2 | QR Code Action / Landing (FA-017) — tab 友だち一覧: đếm 「ブロック」, tìm theo tên bạn, cờ đã chặn từng dòng, xuất CSV | F1, F3, D1, D2 | **High** — nhiều vòng fix đã đảo qua đảo lại (CONVERT ↔ so thẳng) cho cùng 1 câu đếm; RỦI RO CAO NHẤT của ticket này |
| T3 | QR Code Action / Landing (FA-017) — tab LP連携 + xuất CSV trang đích nhiều lượt click | F1, D1 | High — nguyên nhân gốc ban đầu (treo 398s), cần verify hết treo với dữ liệu lớn |
| T4 | Popup (FA-018) — tab2 màn Chi tiết lượt bấm Popup | F4 | Medium — case tương tự áp muộn hơn (vòng fix 5), ít vòng verify hơn EP-53 chính |
| T5 | QR Landing recover commands (ngoài glossary) — `RecoverDuplicateCollectCommand` / `RecoverDeviceCollectCommand` / `RecoverCollectLandingCommand` | F5 | Low — hưởng lợi gián tiếp, không sửa code, chỉ cần smoke check không lỗi |
| T6 | EP-55 (`GET /ajax/v2/landing/{id}/collect-friend`) — dùng chung `firstAddFriends` | F3 | Medium — Dev tự nhận yêu cầu regression ở `task_get_context` (REQ-007) nhưng KHÔNG liệt kê tường minh trong journal 4.3 — Leader nên đối chiếu |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
