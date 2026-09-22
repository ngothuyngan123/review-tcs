# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: **journal #137231 (2026-09-19, AI LME Fix bug)** — bản fix **CÓ HIỆU LỰC**, commit `d552e8292b`.
> Mục 4.2 bổ sung từ journal #137225 (bản tự review v3, cùng nội dung data-impact, chi tiết hơn).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (auto-fixbug) — assignee ticket: **Kim Cúc** (`cucdtk`); human review: **Kieu Son Tung** (`tungks`) |
| Commit / Pull Request | Commit `d552e8292b` (repo `sns-line`) · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=34595 |
| Branch | `ai_fixbug_34595` — branch gốc **`release_step_20260827`** (journal #137183; báo cáo AI ghi `release_step_20260805`) |
| Ngày submit đánh giá | `2026-09-19` |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #137231 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## ⚠️ Lịch sử branch — hướng fix ĐÃ ĐỔI, đọc trước khi viết TC

Ticket qua **4 lượt AI auto-fixbug**, 2 hướng fix hoàn toàn khác nhau:

| Lượt | Journal | Ngày | File sửa | Hiệu lực |
|---|---|---|---|---|
| v1 | #133240 | 2026-08-27 | `app/Services/TemplateService.php` (`getTemplate` + `makeImageMapVer2`) — bỏ gắn `openExternalBrowser=1` cho link LIFF | ❌ **ĐÃ REVERT** (push nhầm lên origin, gỡ bằng commit revert trên chính branch) |
| v2 | #137222 | 2026-09-19 | `LiffController.php` — thêm nhận diện khách cho nhánh `product_id` | ⏩ thay bằng v3 |
| v3 | #137225 | 2026-09-19 | `LiffController.php` — **chỉ nhánh PC**; thêm giữ `lp_id`/`aff_id`, sửa log theo rule PSR-3 (commit `a85d1961ab`) | ⏩ thay bằng v4 |
| **v4** | **#137231** | **2026-09-19** | `LiffController.php` — **cả nhánh PC + nhánh điện thoại**, tách helper `resolveProductUrlByLineLogin` (commit `d552e8292b`, **+54/-0**) | ✅ **BẢN CÓ HIỆU LỰC** |

**Hiệu lực cuối cùng so với release: CHỈ sửa `app/Http/Controllers/LiffController.php`. `TemplateService.php` về nguyên trạng.**

> ⚠️ **Cảnh báo cho `/review-tc`**: 31 TC trên Studio task #248 được tạo `2026-08-27` — tức theo **bản fix v1 đã revert** (template button / image map / `openExternalBrowser`). Phạm vi code thật sẽ deploy là **nhánh `product_id` của `LiffController`**. Phải rà lại toàn bộ coverage theo mục 4 dưới đây, không theo bộ TC cũ.

---

## 1. Nguyên nhân

*(nguyên văn journal #137231, mục ■ 1)*

Khi khách mở link sản phẩm (sale/item) bằng trình duyệt ngoài TRÊN PC/DESKTOP, luồng chạy vào `LiffController::liffAppCallback` nhánh PC (điều kiện `!isMobileDevice()`, dòng 90) rồi vào case `'product_id'`. Nhánh này chỉ dựng lại link LIFF rồi hiển thị trang mã QR "mở bằng ứng dụng LINE" (view `qr_code_open_pc` — view này CHỈ render 1 mã QR, không có LIFF SDK, không ajax) — **KHÔNG hề nhận diện khách**, nên không lấy được mã định danh khách (`u_code`). Trong khi đó màn chi tiết sản phẩm chỉ gửi hành động "khi mở trang" khi URL có `u_code` (`SalesManagementV2Controller::orderDetail` dòng 1650), dẫn tới hành động không được gửi.

Đối chiếu nhánh biểu mẫu (`'unique_key'`) trong cùng hàm thì thấy chỗ thiếu: biểu mẫu có bước đọc access token đã lưu theo channel LINE Login của bot, gọi API lấy hồ sơ để suy ra khách, rồi chuyển thẳng tới trang biểu mẫu kèm định danh khách.

⚠ **LƯU Ý PHẠM VI (tự review v3 bổ sung):**
1. Bug này còn **MỘT đường thứ hai** — khi mở trên **ĐIỆN THOẠI**, luồng đi vào switch MOBILE (nhánh `else`, dòng 514) với case `'product_id'` RIÊNG ở dòng 613 → redirect sang route `open.mobile`. *(Ở v3 chưa đụng tới; v4 đã sửa cả nhánh này.)*
2. Biểu mẫu chạy được ngoài trình duyệt thực chất là nhờ bước **ĐỔI MÃ code OAuth** (dòng 980-1030) chứ không phải nhờ cookie; cookie access token là **đường tắt** và **NƠI DUY NHẤT ghi ra nó chính là luồng biểu mẫu đó** (dòng 1028, TTL 360 phút).

## 2. Cách fix

*(nguyên văn journal #137231, mục ■ 2)*

Cho **cả 2 đường đi** của link sản phẩm khi mở NGOÀI LINE (nhánh máy tính và nhánh điện thoại trong `LiffController::liffAppCallback` case `'product_id'`): nhận diện khách bằng access token đã lưu theo channel LINE Login của bot — giống cách nhánh biểu mẫu đang làm — rồi chuyển thẳng tới trang sản phẩm (**chi tiết / đổi / huỷ**) **KÈM `u_code`**, giữ nguyên tham số affiliate / landing page. Nhờ đó màn chi tiết sản phẩm gửi được hành động "khi mở trang".

Không nhận diện được thì **giữ nguyên hành vi cũ** (nhánh PC hiện trang "mở bằng ứng dụng LINE", nhánh mobile vào trang trung gian như trước). Phần dùng chung đã tách thành helper riêng `resolveProductUrlByLineLogin` để 2 nhánh không nhân đôi code.

⚠ **ĐIỀU KIỆN HIỆU LỰC (tự review v3)**: fix **CHỈ ăn khi trình duyệt đã có sẵn cookie access token LINE Login**, mà cookie đó **CHỈ do luồng BIỂU MẪU ghi ra** (dòng 1028, TTL 6 giờ) — khách mở link sản phẩm trong browser chưa từng đăng nhập qua biểu mẫu trong 6h thì cookie rỗng, rơi về trang QR như cũ và **action VẪN không gửi**. Muốn phủ hết cần bổ sung đường khởi tạo LINE Login (redirect authorize + xử lý code) — cần PM/BA + đăng ký `redirect_uri` trên LINE Login channel, **CHƯA làm**.

**Sửa thêm ở lượt tự review v3 (commit `a85d1961ab`), giữ nguyên trong v4:**
1. **Giữ lại `lp_id` và `aff_id`** trong URL redirect mới — bản fix gốc làm **RƠI `lp_id` hoàn toàn** và **rơi `aff_id` khi thiếu `aff_setting_id`**, trong khi luồng chuẩn trong LINE (`QRCodeController::checkFriend`) forward cả 3 và `orderDetail` nối tiếp chúng vào các bước mua sau (`enter-friend-info` → `confirm-order`) ⇒ **mất quy công landing page / affiliate**. Nay dựng query bằng `array_filter` + `http_build_query` (không tham số nào thì không thêm dấu `?`).
2. Đổi `Log::error($e)` sang `logError` + placeholder PSR-3 theo rule log dự án (chỉ dùng `logDebug` / `logInfo` / `logError`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `LiffController::resolveProductUrlByLineLogin` (`app/Http/Controllers/LiffController.php`) | **MỚI** | Helper dùng chung: cookie LINE Login → hồ sơ LINE → `u_code` → URL trang sản phẩm |
| 2 | `LiffController::liffAppCallback` case `'product_id'` **nhánh máy tính** (dòng ~277) | **ĐÃ SỬA** | Đường đi khi mở link sản phẩm bằng trình duyệt ngoài trên PC |
| 3 | `LiffController::liffAppCallback` case `'product_id'` **nhánh điện thoại** (dòng ~679) | **ĐÃ SỬA** (lỗi LATERAL phát hiện sau review) | Mở trên điện thoại đi đường riêng → redirect `open.mobile`, view dùng LIFF SDK, chưa login thì bật khách về app LINE |
| 4 | `LiffController::liffAppCallback` case `'unique_key'` (biểu mẫu, dòng 363 PC / 560 mobile) | Không sửa | **Mẫu đối chiếu** — nhánh chạy đúng |
| 5 | `LiffController` dòng 980-1030 — luồng đổi mã code OAuth của biểu mẫu | Không sửa | **NƠI DUY NHẤT trong toàn app ghi ra cookie access token theo channel** (`Cookie::queue`, TTL 360 phút) mà fix sản phẩm đang phụ thuộc |
| 6 | `QRCodeController::checkFriend` (`app/Http/Controllers/Basic/QRCodeController.php:3213-3250`) | Không sửa | Nơi dựng URL trang sản phẩm `/v2/order-item/detail·change·cancel/{itemCode}/{u_code}` cho luồng **trong LINE**; fix dựng URL giống hệt; căn cứ cho việc phải forward `lp_id`/`aff_id` |
| 7 | `SalesManagementV2Controller::orderDetail` (`...SalesManagementV2Controller.php:1613`) | Không sửa | **Chỉ gửi hành động khi có `u_code`** (dòng 1650); nhánh đó còn TẠO `bot_line_user_items` (1687-1693) và TĂNG `count_action_view_page` (1697) |
| 8 | `SalesManagementController::orderDetail` (bản cũ) | Không sửa | Chỉ đối chiếu — cùng điều kiện `u_code` |
| 9 | `QRCodeController::openExternalBrowser` / `openMobile` | Không sửa | Trang trung gian |
| 10 | `routes/web.php:3731` — `GET /liff-callback/{unique_id}` (name `liffCallback`) | Không sửa | **Lối vào HTTP DUY NHẤT** của hàm đã sửa, không có caller PHP nội bộ nào (route name `liffAppCallback` dòng 994 là controller KHÁC: `Basic\LiffAppController@store`) |
| 11 | `resources/views/qr_code_open_pc.blade.php` | Không sửa | Xác nhận view này chỉ render mã QR, không nhận diện khách |
| 12 | `resources/views/basic/qr_code/open_mobile.blade.php` | Không sửa | View nhánh mobile, dùng `liff.isLoggedIn()` + ajax `checkFriend` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `LiffController::resolveProductUrlByLineLogin` | `app/Http/Controllers/LiffController.php` | **Direct** (mới) | Helper: cookie LINE Login → API hồ sơ LINE → `u_code` → URL sản phẩm. Điểm tập trung mọi rủi ro của fix |
| F2 | `LiffController::liffAppCallback` case `'product_id'` — **nhánh PC** (`!isMobileDevice()`) | `app/Http/Controllers/LiffController.php:~277` | **Direct** | Trước: luôn hiện trang QR `qr_code_open_pc`. Sau: nhận diện được → redirect thẳng trang sản phẩm kèm `u_code` |
| F3 | `LiffController::liffAppCallback` case `'product_id'` — **nhánh điện thoại** | `app/Http/Controllers/LiffController.php:~679` | **Direct** | Trước: redirect `open.mobile`. Sau: nhận diện được → redirect thẳng trang sản phẩm kèm `u_code` |
| F4 | `SalesManagementV2Controller::orderDetail` | `...SalesManagementV2Controller.php:1613` | **Indirect** — tăng lưu lượng | Nhánh có `u_code` (dòng 1650) nay **thực sự được chạy** từ đường ngoài LINE: gửi action + ghi DB + tăng counter |
| F5 | `SalesManagementV2Controller::sendActionOrderItem('view_page', ...)` | `...SalesManagementV2Controller.php` | **Indirect** | **Side effect thật ra ngoài** — gửi action cho khách. Canh `number_action_show_page`, `flag_page_start != 2` |
| F6 | `LiffController::liffAppCallback` case `'unique_key'` (Form) | `app/Http/Controllers/LiffController.php:363/560` | **Indirect** — không sửa | **Phụ thuộc vận hành**: fix sản phẩm ăn nhờ cookie do luồng này ghi ra (dòng 1028). Đổi TTL / cách ghi cookie → fix này hỏng theo |
| F7 | `QRCodeController::checkFriend` | `...QRCodeController.php:3213-3250` | **Indirect** — không sửa | Luồng **trong LINE** giữ nguyên. Dùng để đối chứng regression: URL 2 đường phải tương đương |
| F8 | `TemplateService::getTemplate` / `makeImageMapVer2` | `app/Services/TemplateService.php` | **KHÔNG còn ảnh hưởng** | Bản fix v1 sửa 2 hàm này **đã revert** → nguyên trạng. ⚠️ Bộ TC Studio cũ vẫn bám vào đây |

### 4.2. List data bị update khi fix bug

> ⚠️ Dev khai ở lượt v2 là "không ghi dữ liệu" — **chưa đúng**, chính báo cáo v3/v4 đã tự đính chính.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_line_users` (`u_code`, `bot_id`, `is_blocked`) | **READ** | Lọc `bot_id` + `is_blocked = 0` để suy `u_code` |
| D2 | `line_users.line_id` | **READ** | Suy khách từ hồ sơ LINE trả về |
| D3 | `s_items.item_code` | **READ** | Dựng URL trang sản phẩm |
| D4 | Cookie **access token LINE Login** (theo channel) | **READ** | **Chỉ do luồng biểu mẫu ghi ra**, `Cookie::queue` dòng 1028, TTL 360 phút |
| D5 | `bot_line_user_items` | **CREATE** | INSERT khi khách chưa có bản ghi cho item đó (`SalesManagementV2Controller.php:1687-1693`) — hệ quả của đường đi mới |
| D6 | `bot_line_user_items.count_action_view_page` | **UPDATE** (+1) | Mỗi lần gửi action thành công (dòng 1697). Code sẵn có dùng **read-modify-write** → nguy cơ **đếm thiếu khi trùng request**; fix này **làm tăng lưu lượng** vào đó (Dev đề xuất đổi sang `increment()` ở ticket kỹ thuật riêng) |
| D7 | Action gửi ra ngoài cho khách — `sendActionOrderItem('view_page', ...)` | **SEND** (side effect thật) | Đúng mục đích ticket nhưng là tác động ra ngoài. QA phải canh **số lần gửi** (`number_action_show_page`, `flag_page_start != 2`) |
| D8 | Tham số theo dõi trên URL: `aff_id` / `aff_setting_id` / `lp_id` | **PASS-THROUGH** | v3 đã sửa để **không bị rơi** (trước đó mất `lp_id`, mất `aff_id` khi thiếu `aff_setting_id`) |
| D9 | Access token LINE của khách | **KHÔNG ghi log** | Chỉ gửi tới `api.line.me` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Sản phẩm đơn lẻ — Single Product / Sales (FA-026)** — link sản phẩm mở bằng trình duyệt ngoài, **cả PC lẫn điện thoại**; áp cho cả trang **chi tiết / đổi / huỷ** | F1, F2, F3, F4, D5, D6 | **High** |
| T2 | **Cấu hình hành động tự động — Action Settings (SC-004)** — hành động gắn cho sản phẩm không còn bị mất trên đường đi mới | F5, D7 | **High** |
| T3 | **QR Code Action / Landing Page (FA-017)** — URL đích mang `lp_id` → ảnh hưởng **quy công landing page** (bản fix gốc làm rơi `lp_id`) | D8 | **High** |
| T4 | **Affiliate — Chương trình giới thiệu (FA-027) / Quản lý chi trả affiliate (FS-013)** — URL đích mang `aff_id` + `aff_setting_id` → ảnh hưởng **quy công hoa hồng** cho đơn mua qua đường này | D8 | **High** |
| T5 | **Tạo biểu mẫu — Form Builder (FA-011)** — KHÔNG sửa, chỉ làm mẫu đối chiếu; **nhưng có phụ thuộc vận hành**: fix sản phẩm ăn nhờ cookie do luồng biểu mẫu ghi ra (dòng 1028) | F6, D4 | **Medium** |
| T6 | **Luồng mua hàng trong LINE (đường cũ, `QRCodeController::checkFriend`)** — phải không đổi | F7 | **Medium** — regression |
| T7 | **Message Template (FA-010)** — nút card/carousel, vùng ảnh image map | F8 | **Low** — `TemplateService` đã revert về nguyên trạng, **không còn thay đổi code**. TC vùng này là **regression thuần** |

---

## ⚠️ Phạm vi Dev CỐ Ý KHÔNG fix (ghi nhận để không viết TC sai kỳ vọng)

| # | Vùng | Trạng thái |
|---|---|---|
| X1 | **Gửi tin qua job** (broadcast / step / remind — `linect-service MessageBuilder`) | **CHƯA fix** — tin gửi tự động vẫn mất hành động. Cần task riêng cho job. ⚠️ Bộ TC Studio hiện có **4 TC `tc_group = job`** ở vùng này, trong đó **NEW-27 đang `fail` + đã raise bug #41140** |
| X2 | **Nhánh đặt lịch** (booking event FA-021 / lesson calendar FA-019) trong cùng hàm | **CHƯA fix** — Dev khai "có thể thiếu y hệt", cố ý không gộp vào ticket này |
| X3 | **Đường khởi tạo LINE Login** (redirect authorize + xử lý code OAuth) | **CHƯA làm** — cần PM/BA + đăng ký `redirect_uri`. Không có nó, fix chỉ ăn khi cookie biểu mẫu còn hạn 6h |
| X4 | `bot_line_user_items.count_action_view_page` dùng read-modify-write → đếm thiếu khi trùng request | **CHƯA fix** — Dev đề xuất ticket kỹ thuật riêng |

## ⚠️ Mức verify của Dev

**Chỉ tới `lint`.** Không kết nối được MySQL dev (`host.docker.internal:3306 refused`), không gửi được tin LINE trong container → **Dev chưa tái hiện, chưa chạy thật lần nào**.

- `php -l app/Http/Controllers/LiffController.php`: No syntax errors detected
- `git diff --stat origin/release_step_20260805...ai_fixbug_34595`: **1 file, +54/-0** (`TemplateService` đã về nguyên trạng nhờ commit revert)

**Rủi ro Dev tự nêu khi test:**
- Chỉ chạy được khi bot **có khai channel LINE Login** và trình duyệt **còn cookie phiên đăng nhập**; bot chưa khai → vẫn như cũ (hiện trang "mở bằng ứng dụng LINE").
- Cần tester xác nhận **cả 3 loại link sản phẩm** (chi tiết / đổi / huỷ) và **cả 2 môi trường PC + điện thoại**.
- Các nhánh đặt lịch trong cùng hàm có thể thiếu y hệt.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Đã xác nhận bộ TC Studio #248 (tạo 2026-08-27, theo bản fix v1 ĐÃ REVERT) có còn đúng phạm vi với bản fix v4 hay không**
