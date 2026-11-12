# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT NGUỒN KHÁC CHUẨN**: Redmine #44557 **KHÔNG có** section "Đánh giá ảnh hưởng phía dev" (ticket là subtask QA retest, không phải bug Dev tự báo). Theo đúng chỉ định của ticket ("Dữ liệu kế thừa từ Test Studio"), nội dung dưới đây lấy từ `task_get_context(task_id=515, sections=["dev_impact","spec_delta","info_pack"])` của **MCP LME TEST STUDIO** — Studio đã tự tính diff/dev_impact cho task 515 (kế thừa từ task cha `task_id=507` / #43845, diff giữa base `303a131b9c` và test `646ca07206c2`). Đây là **diff code thật**, không phải Dev tự kê tay — vẫn cần Dev/Leader xác nhận lại khi review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Redmine #44557 chỉ ghi assignee QA (Tran Loan), không ghi Dev>` |
| Commit / Pull Request | `<chưa có link PR>` — diff xác minh giữa base `303a131b9c` và test `646ca07206c2` (theo Studio task 515) |
| Branch | `ai_studio_implement_43845` (release/production base đối chiếu: `origin/release_step_20260930_v2`) |
| Ngày submit đánh giá | `<không có — không phải Dev submit, là Studio tự tính diff lúc 2026-10-26>` |
| Auto-filled | `2026-10-26 by /new-task` — nguồn: MCP LME TEST STUDIO `task_id=515` (kế thừa `task_id=507` / #43845) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ nội dung dưới là Studio tự tính từ diff code, KHÔNG phải Dev tự kê → bắt buộc đối chiếu lại với Dev/PR thật trước khi tick.

---

## 1. Nguyên nhân

Không phải bug — đây là **thay đổi code do nâng cấp PHP 8.5 + Laravel 13**:

- `ImageRichmenuController` chuyển toàn bộ đọc/lưu/filesize/orient/copy ảnh sang `ImageService` mới (291 dòng) — thay cho xử lý ảnh cũ (Intervention Image v2 → v3). Rủi ro: ảnh nền/icon/slot/tab/ảnh render đổi định dạng, alpha, hướng và chất lượng so với trước nâng cấp.
- `catch Exception` đổi thành `catch Throwable` + `reportCaughtError`: lỗi PHP 8 có thể đổi đường trả JSON/log — cần kiểm UI không báo "thành công" khi file/bản ghi chưa hoàn tất lưu.
- Route và framework đổi toàn cục (Laravel 13) → vẫn có candidate regression ở CSRF/session, render Blade, response cũ và file response — dù file JS tạo/list ảnh không khác base.
- Quota tên trùng / IDOR cách ly bot đã nằm trong base bàn giao từ trước (không phải tính năng mới của task này), nhưng vẫn là candidate regression vì task yêu cầu test lại toàn luồng.

## 2. Cách fix

(Không phải "fix" mà là **migrate logic xử lý ảnh sang API mới**, theo diff đã xác minh của Studio)

- `ImageService` (mới, 291 dòng): giữ `quality` mặc định **90**, `autoOrientation=false`, `decodeAnimation=false`, dùng encoder tương thích — đây là **chủ đích code**, không phải bằng chứng ảnh thực tế trên môi trường test đã khớp 100% với trước nâng cấp.
- `resizeImageToMaxSize` dùng `ImageService`, gọi `orient` rồi giữ tỉ lệ/ép `int`; nhánh ảnh ≤2048px **không save** — giữ đúng hành vi có sẵn (test nguồn `PB-T15-7`).
- `ImageRichmenuController`: 246 dòng thay đổi (đọc/lưu/filesize/orient/copy chuyển sang gọi `ImageService`).
- `RichMenuService` (V2): 47 dòng thay đổi. `RichMenuController` (V2): 64 dòng thay đổi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Theo diffStat thật của Studio (task 507, lọc theo file liên quan Richmenu/Image) — KHÔNG phải Dev tự liệt kê. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `app/Http/Controllers/Basic/ImageRichmenuController.php` | 246 dòng +/- | Chuyển đọc/lưu/filesize/orient/copy ảnh sang `ImageService` |
| 2 | `app/Services/ImageService.php` | +291 dòng (mới) | Service xử lý ảnh mới dùng Intervention Image v3 |
| 3 | `app/Services/V2/RichMenuService.php` | 47 dòng +/- | Caller gián tiếp của luồng ảnh rich menu V2 |
| 4 | `app/Http/Controllers/V2/RichMenuController.php` | 64 dòng +/- | Caller gián tiếp — route/response rich menu V2 |
| 5 | `app/RichMenus.php`, `RichMenuItems.php`, `RichMenuFilterFriend.php`, `RichMenuSwitchItem.php`, `RichMenusReplicate.php`, `ImageRichMenu.php`, `DetailClickRichMenu.php`, `SettingDisplayRichMenuHistory.php`, `Models/RichMenuHistory.php` | 2–4 dòng mỗi file | Model/entity liên quan — khớp đổi toàn cục do nâng cấp Laravel 13, không phải logic nghiệp vụ mới |
| 6 | `app/Console/Commands/ForceDeleteRichmenuCommand.php`, `RecoverDelRichmenu30052023.php`, `RecoverRichmenuDefault.php`, `recoverSwitchRichmenu.php` | 3–33 dòng mỗi file | Command xử lý xóa/khôi phục rich menu — candidate ảnh hưởng tới ảnh đã tạo khi recover |
| 7 | `tests/Unit/ImageServiceTest.php` (mới, 334 dòng), `tests/Upgrade/ForceDeleteRichmenuT19Test.php` (mới, 220 dòng) | — | Test Dev/Studio đã viết kèm diff — tham khảo, không thay cho TC review |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Upload/lưu/đọc filesize/orient/copy ảnh rich menu | `ImageRichmenuController.php` | Direct | Chuyển toàn bộ sang gọi `ImageService` |
| F2 | Resize/orient/encode ảnh (quality 90, autoOrientation=false, decodeAnimation=false) | `ImageService.php` (mới) | Direct | Dùng Intervention Image v3; chủ đích giữ hành vi cũ nhưng chưa có bằng chứng ảnh thực tế khớp |
| F3 | `resizeImageToMaxSize` — nhánh ≤2048px không save | `ImageService.php` | Direct | Giữ hành vi có sẵn `PB-T15-7` — cần verify lại trên thư viện mới |
| F4 | Exception handling khi xử lý ảnh lỗi (`catch Throwable` + `reportCaughtError`) | `ImageRichmenuController.php` | Direct | Đổi đường trả JSON/log khi lỗi PHP 8 — cần đảm bảo UI không báo sai thành công |
| F5 | Luồng Rich Menu V2 (tạo/sửa dùng ảnh đã upload) | `RichMenuService.php`, `RichMenuController.php` (V2) | Indirect | Điểm tích hợp trực tiếp với ảnh đã tạo — nằm trong phạm vi kiểm tra của ticket |
| F6 | Command khôi phục/xóa rich menu liên quan ảnh | `ForceDeleteRichmenuCommand.php`, `RecoverDelRichmenu30052023.php`, `RecoverRichmenuDefault.php`, `recoverSwitchRichmenu.php` | Indirect | Job nền — candidate ảnh hưởng gián tiếp tới ảnh đã tạo khi recover |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | File ảnh nền/icon/slot/tab lưu trên disk (upload/resize/orient/encode) | UPDATE | Rủi ro đổi format, alpha, hướng, chất lượng ảnh đầu ra so với production |
| D2 | Response JSON / log khi xử lý ảnh lỗi | UPDATE | `catch Throwable` đổi đường trả lỗi — cần kiểm log/response không đổi hợp đồng (contract) |
| D3 | Record ảnh rich menu (tên quản lý, quota, kiểm trùng tên) | (không đổi — thuộc base bàn giao cũ) | Candidate regression vì task yêu cầu test lại toàn luồng, không phải tính năng mới |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Tạo ảnh rich menu (「リッチメニュー画像作成」) — /basic/image-richmenu: upload, resize 2048px, render chữ/layout, xuất ảnh 2500px | F1, F2, F3, D1 | High |
| T2 | Tạo/sửa/sao chép/tải/xóa ảnh rich menu (danh sách, folder, hàng loạt) | F1, F4, D1, D3 | Medium |
| T3 | Điểm tích hợp: dùng ảnh đã tạo để thiết lập Rich Menu (V2) | F5 | Medium |
| T4 | Xử lý lỗi khi upload/xử lý ảnh thất bại (UI không báo sai thành công) | F4, D2 | Medium |
| T5 | Khôi phục/xóa rich menu liên quan ảnh đã tạo (job/command nền) | F6 | Low — ngoài phạm vi chính của ticket (không bao gồm regression toàn bộ quản lý Rich Menu), chỉ theo dõi nếu chạm điểm tích hợp ảnh |

---

## Spec reference (Studio `specRefs`, task 515 — chỉ liệt kê, đọc chi tiết tại `spec-features/` nếu có)

`image-rich-menu/SCR-IRM-01` (danh sách/folder/grid/selection/sort/copy/download/delete) · `SCR-IRM-02` (create/edit/designer/modals/tab/nền/chữ/output) · `BR-01` (cách ly bot) · `BR-02` (quota tạo/sao chép) · `BR-03` (upload/nén/2048, tách giới hạn FE/BE) · `BR-04` (2500×1686 hoặc 2500×843 theo layout) · `BR-05` (layout large/compact) · `BR-06` (folder kind=19 và chưa phân loại) · `BR-07` (single/multi-tab) · `BR-08` (slugify tên/tên file) · `BR-09` (rủi ro không nguyên tử ở thao tác nhiều bước) · `BR-10` (hard delete, khác biệt xóa folder/item) · `EP-01..EP-16` (endpoint `/basic/image-richmenu*`, `/ajax/*`).

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ **Riêng mục này**: đã xác nhận với Dev thật của #43845 rằng nội dung Studio tự tính (ở trên) khớp với PR/commit thực tế, vì Redmine #44557 không có Dev tự kê.
