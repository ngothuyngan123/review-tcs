# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #40909 — **Journal #136301 (AI LME Fix bug, 2026-09-14)** — báo cáo AI AUTO-FIXBUG. Chép nguyên văn, chỉ sắp xếp vào bảng của template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — QA tiếp nhận: Ngô Thúy Ngần |
| Commit / Pull Request | repo `sns-line`, commit `9c79ed9182` (1 commit, 5 file) — `<chưa có link PR>` |
| Branch | `ai_small_40909` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | 2026-09-14 |
| Auto-filled | `2026-09-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Lưu mẫu tin nhắn mất tới 246 giây vì mỗi lần lưu lại sinh thêm bản ghi liên kết chuyển hướng thay vì cập nhật bản cũ: câu chống trùng so khớp theo CHUỖI đường dẫn, mà cột lưu đường dẫn chỉ dài 255 ký tự nên đường dẫn dài (769 ký tự) bị cắt âm thầm lúc ghi (kết nối cơ sở dữ liệu đang tắt chế độ nghiêm ngặt), lần lưu sau so sánh không bao giờ khớp nên luôn tạo mới. Bản ghi nhân đôi liên tục, và với MỖI bản ghi hệ thống lại gọi ra máy chủ bên ngoài lấy dữ liệu xem trước đường dẫn dù dữ liệu đó đã có sẵn trong bộ nhớ đệm — mỗi lần gọi là 2 lượt tải mạng chờ tối đa 10 giây và 60 giây, không giới hạn số lần. Bảng liên kết cũng chưa có chỉ mục nào ngoài khoá chính nên mỗi lần dò trùng đều quét toàn bảng. Ghi nhật ký còn dump trọn nội dung gửi lên 2 lần cộng ghi từng phần tử trong vòng lặp, làm phình file nhật ký (5,4 GB/ngày) và tốn thêm thời gian ghi đĩa.

## 2. Cách fix

Sửa trên nhánh `ai_small_40909` (`sns-line`, 5 file):

1. Đổi điều kiện chống trùng bản ghi chuyển hướng từ so CHUỖI đường dẫn sang so theo **mã liên kết đường dẫn** (mẫu tin + bot + mã đường dẫn, ưu tiên bản mới nhất) ở **cả bản web và bản API** — hết cảnh nhân đôi bản ghi mỗi lần lưu.
2. **Chỉ gọi lấy dữ liệu xem trước** ra trang đích **khi chưa có dữ liệu lưu sẵn**, tái dùng dữ liệu cũ và bỏ luôn lượt ghi đè thừa — từ 3 lượt gọi mạng mỗi đường dẫn mỗi lần lưu xuống còn 0 khi đã có dữ liệu.
3. Thêm bước **nâng cấp cơ sở dữ liệu**: nới cột đường dẫn sang kiểu văn bản dài + thêm chỉ mục (mẫu tin, mã đường dẫn) để hết quét toàn bảng.
4. Thêm **lệnh dọn dữ liệu rác** xoá bản ghi trùng, giữ bản mới nhất, có chế độ chạy thử.
5. **Giảm ghi nhật ký**: bỏ lần dump trùng nội dung gửi lên ở tầng điều khiển và gộp ghi nhật ký trong vòng lặp thành một dòng ngắn.
6. Thêm **cảnh báo nhật ký** khi đường dẫn dài quá sức chứa cột mà tra không ra bản ghi, để phát hiện sớm nếu bảng đường dẫn cũng bị cắt.

> **Rà ngang (nguyên văn):** bản API cùng lỗi đã sửa cùng lúc; **màn nạp dữ liệu xem trước và hàm dò đường dẫn trong nội dung tin còn dùng so chuỗi — ghi nhận, chưa sửa (ngoài phạm vi).**

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TemplateV2Service::saveText` — `app/Services/Templates/TemplateV2Service.php` | ĐÃ SỬA | Đổi dedupe sang `url_id`; chỉ fetch metadata khi chưa có cache |
| 2 | `ApiTemplateService::saveText` — `app/Services/Templates/ApiTemplateService.php` | ĐÃ SỬA | Bản API mobile cùng lỗi, sửa cùng lúc |
| 3 | `TemplateV2Controller::saveTemplate` — `app/Http/Controllers/Basic/TemplateV2Controller.php` | ĐÃ SỬA | Bỏ dump payload trùng, gộp log vòng lặp |
| 4 | `TemplateV2Controller::ajaxMetadataUrlAll` — cùng file | **RÀ SOÁT, KHÔNG SỬA** | Còn dùng so chuỗi URL — ngoài phạm vi |
| 5 | `getMetadataContent` — `app/Helpers/functions.php` | Không sửa | Số lượt gọi giảm do caller đổi điều kiện |
| 6 | `Metadata::getMetaV2` — `app/Services/Metadata.php` | Không sửa | Giữ nguyên timeout 10s + 60s (hạ ảnh hưởng toàn hệ thống) |
| 7 | `detectUrlInMessageTextV2` — `app/Helpers/functions.php` | **RÀ SOÁT, KHÔNG SỬA** | Còn dùng so chuỗi URL — ngoài phạm vi |
| 8 | `CleanDuplicateTemplateUrlRedirect::handle` — `app/Console/Commands/CleanDuplicateTemplateUrlRedirect.php` | **MỚI** | Lệnh dọn bản ghi trùng, có `--dry-run` |
| 9 | `ChangeUrlTextAddIndexTemplateUrlRedirectTable::up` — `database/migrations/2026_09_14_100000_change_url_text_add_index_template_url_redirect_table.php` | **MỚI** | Nới cột URL sang TEXT + thêm index |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Journal ghi mục 4.1 là **"File thay đổi"** (5 file) — bảng dưới ghép với mục 3 để có đủ function. Cột "Mức độ ảnh hưởng" tổng hợp từ mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TemplateV2Service::saveText` | `app/Services/Templates/TemplateV2Service.php` | Direct | Đổi điều kiện dedupe + bỏ fetch metadata thừa |
| F2 | `ApiTemplateService::saveText` | `app/Services/Templates/ApiTemplateService.php` | Direct | Bản API mobile, cùng cách chống trùng |
| F3 | `TemplateV2Controller::saveTemplate` | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Direct | Giảm log (bỏ dump payload trùng) |
| F4 | `CleanDuplicateTemplateUrlRedirect::handle` | `app/Console/Commands/CleanDuplicateTemplateUrlRedirect.php` | Direct (MỚI) | Lệnh `recover:cleanDuplicateTemplateUrlRedirect`, có `--dry-run` / `--chunk` |
| F5 | `ChangeUrlTextAddIndexTemplateUrlRedirectTable::up` | `database/migrations/2026_09_14_100000_...php` | Direct (MỚI) | Migration nới cột + thêm index |
| F6 | `TemplateV2Controller::ajaxMetadataUrlAll` | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Indirect | **Rà soát, KHÔNG sửa** — còn so chuỗi URL |
| F7 | `detectUrlInMessageTextV2` | `app/Helpers/functions.php` | Indirect | **Rà soát, KHÔNG sửa** — còn so chuỗi URL |
| F8 | `getMetadataContent` / `Metadata::getMetaV2` | `app/Helpers/functions.php` · `app/Services/Metadata.php` | Indirect | Không sửa; số lượt gọi giảm từ 3 → 0 khi đã có cache |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `template_url_redirect.url` | MIGRATE | Đổi kiểu từ `varchar(255)` sang TEXT (nới rộng, **KHÔNG mất dữ liệu cũ**); từ nay lưu được đường dẫn dài nguyên vẹn |
| D2 | `template_url_redirect` — index `(template_id, url_id)` | MIGRATE | Thêm chỉ mục tổng hợp; **chạy ALTER khoá bảng một lần, nên chạy giờ thấp điểm** |
| D3 | `template_url_redirect` — dữ liệu rác cũ | DELETE | **CẦN dọn** bằng `recover:cleanDuplicateTemplateUrlRedirect` (giữ bản `id` lớn nhất); không chạy thì bản ghi trùng cũ vẫn còn nhưng **KHÔNG sinh thêm** |
| D4 | `url.metadata` / `url.has_metadata` | UPDATE | Từ nay **chỉ ghi khi vừa lấy mới**; trước đây bị ghi đè mỗi lần lưu mẫu tin |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Message Template (FA-010)** — màn soạn/lưu mẫu tin nhắn loại văn bản có đường dẫn | F1, F3, D1, D2, D3 | High — hết nhân đôi bản ghi chuyển hướng, thời gian lưu giảm mạnh |
| T2 | **Template Message (SC-001)** — luồng lưu mẫu tin dùng chung qua API (bản mobile/API) | F2, D1, D3 | High — áp cùng cách chống trùng |
| T3 | **URL Analytics (FA-023)** — bảng liên kết chuyển hướng + bộ nhớ đệm dữ liệu xem trước của đường dẫn | F6, F8, D3, D4 | Medium — dữ liệu xem trước không còn bị ghi đè mỗi lần lưu; link rút gọn đã phát tán phải còn sống sau khi dọn rác |
| T4 | **Broadcast (FA-008)** — dùng lại cùng mẫu tin | T1 | Low — hưởng lợi gián tiếp; **không đổi logic gửi** |

---

## 5. RECOVER DATA (nguyên văn từ journal)

⚠️ **CÓ** — Dữ liệu rác đã sinh từ trước: bảng `template_url_redirect` có nhiều bản ghi trùng cùng `(template_id, url_id)`. Chạy lệnh mới `recover:cleanDuplicateTemplateUrlRedirect` (xem trước bằng `--dry-run`) để xoá bản cũ, giữ bản `id` lớn nhất. Chạy **SAU khi đã chạy migration** (có chỉ mục thì gom nhóm mới nhanh) và **vào giờ thấp điểm**. Ngoài ra nên chạy lại `recover:templateUrlRedirect` để ghi lại cột `url` đầy đủ cho các bản ghi cũ bị cắt.

**Phạm vi:** Toàn bộ bot có mẫu tin chứa đường dẫn dài trên 255 ký tự; nặng nhất là `botId 41216` trong ticket.

## 6. VERIFY của Dev (mức: lint)

- `php -l` cho 5 file đã sửa/thêm: No syntax errors detected.
- Nạp lớp qua composer autoload: lệnh mới đăng ký đúng tên `recover:cleanDuplicateTemplateUrlRedirect` với 2 tuỳ chọn `dry-run` / `chunk`; lớp migration `ChangeUrlTextAddIndexTemplateUrlRedirectTable` khởi tạo OK.
- `git diff origin/release_step_20260805...ai_small_40909` chỉ gồm đúng 5 file, 1 commit, cha là đỉnh `origin/release_step_20260805`.
- ⚠️ **CHƯA chạy được migration + lệnh dọn dữ liệu**: MySQL dev `host.docker.internal:3306` Connection refused.

**Bằng chứng Dev dẫn:** `database/migrations/2025_09_30_152713:17` — `template_url_redirect.url` khai báo `string('url', 255)` · `config/database.php:53` — connection mysql đặt `'strict' => false` nên MySQL cắt chuỗi âm thầm thay vì báo lỗi · `share/db/db-refined/.../template_url_redirect.sql` — bảng chỉ có `PRIMARY(id)`, không có chỉ mục nào cho `template_id`/`url_id` · `app/Services/Metadata.php:104` và `:113` — `getMetaV2` gọi 2 lượt curl (header timeout 10s, tải HTML timeout 60s), không cache, không giới hạn số lần · `app/Helpers/functions.php:9861` — `getMetadataContent` gọi `getMetaV2($url, 60)` · Trước fix, mỗi phần tử đường dẫn gọi `getMetadataContent` tới 3 lần/lần lưu (dòng 734 + 746 hoặc 769) = **6 lượt curl**.

## 7. Rủi ro / lưu ý khi test (AI tự review — nguyên văn)

1. **CHƯA thêm ràng buộc duy nhất `(template_id, url_id)`** như tác giả đề xuất: dữ liệu hiện có đang trùng nên thêm chỉ mục duy nhất sẽ làm migration FAIL lúc triển khai. Đề nghị trình tự: (1) chạy migration này, (2) chạy lệnh dọn rác, (3) mới thêm migration chỉ mục duy nhất ở **ticket kế tiếp**.
2. **Phụ thuộc giả định rằng `url_id` ổn định giữa các lần lưu.** Cột `url.url` là `varchar(500)`: nếu đường dẫn dài hơn 500 ký tự thì việc tra bảng đường dẫn cũng trượt và sinh mã mới mỗi lần lưu, khi đó chống trùng theo `url_id` **vẫn chưa đủ**. Đã thêm log cảnh báo để xác nhận trên môi trường thật; nếu log này xuất hiện thì cần ticket nới cột `url.url` (bảng dùng kết nối riêng `mysql_url`, là quyết định vận hành).
3. **Đổi hành vi có chủ ý:** dữ liệu xem trước đường dẫn **KHÔNG còn được làm mới mỗi lần lưu** mẫu tin (chỉ lấy khi chưa có). Cách này giống hàm dò đường dẫn trong nội dung tin vốn đã làm vậy; nếu nghiệp vụ muốn làm mới định kỳ thì dùng lệnh `recover:GetMetaDataUrl` sẵn có.
4. Vẫn **giữ nguyên thời gian chờ mạng 10 giây + 60 giây** khi thực sự phải lấy dữ liệu xem trước lần đầu. Hạ mức chờ này ảnh hưởng toàn hệ thống nên để ngoài phạm vi.
5. **ALTER nới cột + thêm chỉ mục trên bảng lớn sẽ khoá bảng một lúc** — cần chạy giờ thấp điểm.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
