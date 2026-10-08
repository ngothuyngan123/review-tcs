# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41004 — [AI][Bug Exception] Undefined variable: flagCycle (View: /var/www/html/sns-line/resources/views/basic/sales/#/order/enter-payment-info-...)` |
| Module / Màn hình | Single Product / Sales (FA-026) — màn nhập thông tin thanh toán (`enter-payment-info.blade.php`) & đổi thẻ (change card) của sản phẩm bán hàng định kỳ — nhánh sản phẩm **không tồn tại / không công khai (đã xoá/ẩn)** |

## Mô tả bug (bản dịch tiếng Việt)

Ticket tự tạo bởi hệ thống check-exception AI (từ exception bắn lên Chatwork).

*Phân loại:* php_code_error — *Rủi ro:* medium
*Số lần cảnh báo:* 2 — *Số user lỗi:* 0
*Room:* SNSLineException — *Server:* step.lme.jp/
*Lần đầu:* 2026-09-15 08:10 UTC — *Lần cuối:* 2026-09-15 08:18 UTC

**Signature (đã chuẩn hóa):**
```
Undefined variable: flagCycle (View: /var/www/html/sns-line/resources/views/basic/sales/#/order/enter-payment-info.blade.php)
```

**Exception mẫu (mới nhất):**
```
Server: step.lme.jp/
User: info@tralab.jp (114978)
BotId: 153485
Undefined variable: flagCycle (View: /var/www/html/sns-line/resources/views/basic/sales/v2/order/enter-payment-info.blade.php) — dòng 156
```

## Steps to reproduce

> ⚠️ Không có journal QA tái hiện bằng tay trên Redmine. Steps dưới đây **suy ra từ root cause do AI Auto-fixbug mô tả** (Journal #137967 + #140116 ở mục "Journal / note từ Redmine" bên dưới) — Leader/Tester cần tự dựng lại trên môi trường test để xác nhận trước khi chốt TC verify.

1. Có 1 sản phẩm bán hàng định kỳ (single product) đã bị **xoá hoặc chuyển sang không công khai**.
2. Khách hàng (friend) mở đường dẫn **đổi thẻ thanh toán / đổi đăng ký** của sản phẩm đó (link cũ đã gửi trước khi sản phẩm bị xoá/ẩn, hoặc link tĩnh không kiểm tra lại).
3. Hệ thống vào `SalesManagementV2Controller::orderChange`, không tìm thấy sản phẩm theo mã → chạy nhánh trả về sớm (early-return), vẫn render `enter-payment-info.blade.php` nhưng (tuỳ thời điểm — xem 2 journal fix riêng biệt) thiếu biến `flagCycle` truyền sang view.
4. View dùng biến `flagCycle` trực tiếp ở dòng 156/162 không bọc kiểm tra tồn tại → PHP ném `Undefined variable: flagCycle`.

## Expected result

- Hiện thông báo lỗi tiếng Nhật thông thường (vd `商品が非公開か、存在していません` — sản phẩm không công khai hoặc không tồn tại), KHÔNG văng lỗi hệ thống (exception trắng trang).

## Actual result

- PHP ném lỗi `Undefined variable: flagCycle` → khách hàng nhận trang lỗi hệ thống (exception) thay vì thông báo nghiệp vụ tiếng Nhật.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- Không có attachment Redmine (`issue.attachments` rỗng) — log là exception signature + exception mẫu, đã chép nguyên văn ở "Mô tả bug" trên.

## Ghi chú thêm của Leader

- Trạng thái ticket: **Fix done - Đợi test**, Priority Normal. Ticket này được fix **2 lần** (2 journal AI fixbug riêng biệt, cách nhau gần 2 tuần) — xem rõ ở `03-dev-impact.md`.
- ⚠️ **QUAN TRỌNG — 2 branch fix KHÔNG được merge vào nhau**, theo đúng lời Dev tự ghi ở journal #140116/#140117:
  - `ai_small_41004` (fix lần 1, #137967, 2026-09-23) — có thêm `$flagCycle ?? 0` ở blade, **nhưng THIẾU** fix của #42041.
  - `ai_fixbug_41004` (fix lần 2, #140116/#140117, 2026-10-05) — có fix nhánh `orderChange` (relapse của chính #41004) + fix #42041, **nhưng KHÔNG có** fix blade default của lần 1.
  - ⇒ Nếu QA checkout nhầm 1 trong 2 branch, sẽ **KHÔNG thấy đủ cả 2 lần fix**. Cần hỏi Dev/Leader xem branch nào sẽ merge lên release thực tế, hoặc yêu cầu Dev gộp 2 branch trước khi test.
  - Dev ghi thêm: **Test Studio hiện đang dựng test từ branch `ai_small_41004`** — branch đó KHÔNG có commit #42041. Phải trỏ Test Studio sang `ai_fixbug_41004` thì mới thấy được fix lần 2 + #42041.
- ⚠️ Ticket **#42041** (bug con — sản phẩm không công khai vẫn hiện form đổi thẻ) được Dev **tự gộp fix vào cùng commit `d01e9e391d`** của #41004 lần 2, dù là ticket Redmine riêng. Leader cần xác nhận có tách TCs cho #42041 ra review riêng hay vẫn review chung ở đây.
- Dev tự nhận (journal #140116): view `enter-payment-info.blade.php` **vẫn còn dùng biến `flagCycle` không bọc kiểm tra tồn tại** ở dòng 156/162 — nếu sau này có nhánh early-return mới quên truyền biến này, lỗi sẽ **tái diễn lần 3**. Dev cố ý không sửa tận gốc (ngoài phạm vi fix tối giản) — Leader cân nhắc có nên yêu cầu Dev bọc kiểm tra tồn tại trong view không.
- #42041 còn 1 điểm **PO chưa chốt**: có nên chặn hẳn việc đổi thẻ khi sản phẩm đã ẩn cho khách đang có hợp đồng không (xem FA-031 ở mục 4.3 file 03).
- Môi trường gốc phát hiện: `step.lme.jp` (production/step — không ghi rõ là prod hay staging trong ticket, cần Leader xác nhận lại tên môi trường thật).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `153485` (ca exception mẫu mới nhất) |
| Friend | user: `info@tralab.jp` (id `114978`) |
| Đối tượng cấu hình | Sản phẩm bán hàng định kỳ (single product) đã bị xoá/ẩn — không có ID sản phẩm cụ thể trong log |
| Thời điểm lỗi | Lần đầu 2026-09-15 08:10 UTC — Lần cuối 2026-09-15 08:18 UTC (2 lần cảnh báo, trước khi fix lần 1) |
| Đối chứng | Không có case đối chứng chạy đúng ghi trong ticket — Dev tự verify bằng render Blade compile, không có repro thật trên môi trường |

## Journal / note từ Redmine (nguyên văn)

**Journal #137967 — AI LME Fix bug — 2026-09-23:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Ở màn nhập thông tin thanh toán của tính năng bán sản phẩm, khi khách mở đường dẫn đổi thẻ/đổi đăng ký mà sản phẩm không còn tồn tại (đã bị xoá), phần xử lý thoát sớm chỉ gửi sang giao diện đúng hai dữ liệu là nội dung lỗi và danh sách loại thẻ, nhưng giao diện vẫn luôn kiểm tra thêm một cờ trạng thái đã đăng ký. Cờ này không được gửi nên trang báo lỗi hệ thống thay vì hiện thông báo tiếng Nhật thông thường. Lỗi có từ 2023, chỉ bắn khi khách bấm vào đường dẫn của sản phẩm đã bị xoá (nội dung thông báo có nhắc cả trường hợp để ẩn, nhưng nhánh này chỉ chạy khi sản phẩm không tồn tại).

■ 2. CÁCH FIX
Sửa 2 lớp cho màn nhập thông tin thanh toán của sản phẩm bán hàng: (1) nhánh thoát sớm khi sản phẩm không tồn tại/không công khai nay gửi thêm cờ trạng thái đã đăng ký (giá trị mặc định 0 đã có sẵn trong hàm) sang giao diện — đúng nguyên nhân gây lỗi hệ thống; (2) giao diện lấy cờ đó theo kiểu có giá trị mặc định khi thiếu, nên mọi luồng khác nếu quên gửi cũng chỉ hiện thông báo lỗi tiếng Nhật thay vì văng lỗi trắng trang. Hành vi hiển thị không đổi với luồng bình thường (cờ = 0 hoặc 1).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
SalesManagementV2Controller::orderChange (app/Http/Controllers/Basic/SalesManagementV2Controller.php:1892-2035)
SalesManagementV2Controller::viewEnterPaymentInfo (cùng file:2163-2283 — luồng đã truyền đủ cờ, không đổi)
SalesManagementV2Controller::viewEnterFriendInfo / confirmOrder (cùng file:2037, 2318 — đã truyền đủ cờ)
Giao diện enter-payment-info (resources/views/basic/sales/v2/order/enter-payment-info.blade.php:156,162)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/SalesManagementV2Controller.php
   - resources/views/basic/sales/v2/order/enter-payment-info.blade.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ sửa luồng hiển thị, không đụng dữ liệu/bảng nào
 • 4.3 Tính năng liên quan:
   - Single Product / Sales (FA-026) — màn nhập thông tin thanh toán & đổi thẻ của sản phẩm bán hàng: trường hợp sản phẩm bị xoá/ẩn nay hiện thông báo tiếng Nhật thay vì lỗi hệ thống

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l SalesManagementV2Controller.php: No syntax errors detected; php -l enter-payment-info.blade.php: No syntax errors detected; Biên dịch giao diện bằng bộ biên dịch Blade rồi php -l bản biên dịch: OK; Render bản biên dịch với ĐÚNG bộ dữ liệu của nhánh thoát sớm: bản cũ = 'Undefined variable: flagCycle' (dòng 156 & 162, khớp log ngoại lệ), bản đã sửa = không lỗi + hiện đúng '商品が非公開か、存在していません'
   Bằng chứng: Log ngoại lệ chỉ đúng dòng 156 của giao diện = @if($flagCycle == 1); toàn bộ phần thân trang nằm trong khối bảo vệ 162-1229 nên nhánh lỗi chỉ chạy tới dòng 156; git blame: nhánh thoát sớm thiếu biến có từ 2023-07-27 (commit 32d1fb10e8d), không phải hồi quy mới

■ TỰ REVIEW (AI)
Fix tối thiểu, đúng nguyên nhân: bổ sung biến còn thiếu ở nhánh thoát sớm + lấy biến có mặc định ở giao diện. Không đổi luồng nghiệp vụ, không đụng thanh toán/dữ liệu. Đã tái hiện lỗi và xác nhận hết lỗi bằng cách render giao diện đã biên dịch.
 • Rủi ro / lưu ý khi test:
   - Rủi ro thấp: giá trị mặc định 0 giữ đúng ý nghĩa 'chưa đăng ký' như biến khởi tạo trong controller
   - Các màn cùng mẫu (xác nhận đơn / nhập thông tin bạn bè) chưa bọc mặc định — hiện chưa lỗi nên không sửa để tránh ngoài phạm vi, đã ghi ở phần triển khai ngang

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41004 (nhánh gốc release_step_20260827, commit 8600ec8ccd, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 18 phút 53 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=2ba1acd0-9fdf-4a33-89e2-13363e1b747b
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41004
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #140116 — AI LME Fix bug — 2026-10-05:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn đổi thẻ thanh toán của sản phẩm định kỳ có nhánh trả về sớm khi không tìm thấy sản phẩm theo mã. Nhánh này vẫn hiển thị giao diện nhập thông tin thanh toán nhưng chỉ truyền sang 2 biến là danh sách thương hiệu thẻ và thông báo lỗi, thiếu biến cờ chu kỳ. Giao diện dùng biến cờ này trực tiếp (không bọc kiểm tra tồn tại) ngay ở phần hiển thị trang lỗi, nên PHP ném lỗi biến chưa định nghĩa và khách hàng nhận trang lỗi máy chủ thay vì thông báo sản phẩm không tồn tại. Đây là lỗi vá thiếu: một lần sửa trước đó đã bổ sung biến danh sách thương hiệu thẻ vào đúng nhánh này nhưng bỏ sót biến cờ chu kỳ.

■ 2. CÁCH FIX
(1) #41004: bổ sung biến cờ chu kỳ vào mảng biến truyền cho giao diện tại nhánh trả về sớm khi sản phẩm không tồn tại của màn đổi thẻ thanh toán bản mới — hết lỗi hệ thống, hiện đúng thông báo lỗi tiếng Nhật. (2) #42041 (bug con, commit d01e9e391d): cũng màn đổi thẻ này, khi khách mở đường dẫn (không phải xem trước) mà sản phẩm đã bị chuyển sang không công khai thì báo "sản phẩm không công khai hoặc không tồn tại" thay vì vẫn hiện form đổi thẻ — giống màn đổi thẻ bản cũ và màn nhập thanh toán bản mới; chế độ xem trước của quản trị viên giữ nguyên.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
SalesManagementV2Controller::orderChange (app/Http/Controllers/Basic/SalesManagementV2Controller.php:1892 - nhánh lỗi dòng 1902, điểm đã sửa)
SalesManagementV2Controller::viewEnterPaymentInfo (app/Http/Controllers/Basic/SalesManagementV2Controller.php:2163 - có truyền đủ, không lỗi)
SalesManagementV2Controller::viewEnterFriendInfo (app/Http/Controllers/Basic/SalesManagementV2Controller.php:2037 - có truyền đủ)
SalesManagementV2Controller::confirmOrder (app/Http/Controllers/Basic/SalesManagementV2Controller.php:2318 - có truyền đủ)
SalesManagementV2Controller::orderCancel (app/Http/Controllers/Basic/SalesManagementV2Controller.php:1799 - nhánh trả sớm an toàn, giao diện bọc kiểm tra đủ)
SalesManagementController::orderIndex (app/Http/Controllers/Basic/SalesManagementController.php:1569 - có truyền đủ)
enter-payment-info.blade.php (resources/views/basic/sales/v2/order/ - dòng 156, 162 dùng biến không bọc kiểm tra)
cancel.blade.php / detail.blade.php / order_detail.blade.php (đã rà, mọi biến đều bọc kiểm tra tồn tại)
[#42041] SalesManagementV2Controller::orderChange dòng 1922 — thêm kiểm status_valid != 1 trong nhánh không phải preview
[#42041] SalesManagementController::orderChange (bản cũ) + viewEnterPaymentInfo — mẫu đối chứng cùng thông báo
[#42041] orderCancel / changeCardItem / changeCardUnivapay — không kiểm status_valid (ghi yokoten, chưa sửa)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/SalesManagementV2Controller.php
 • 4.2 Data ảnh hưởng:
   - Không có - chỉ đổi điều kiện hiển thị; nhánh #42041 chỉ đọc s_items.status_valid
 • 4.3 Tính năng liên quan:
   - Single Product / Sales (FA-026) - màn đổi thẻ thanh toán sản phẩm định kỳ bản mới: (#41004) sản phẩm không tồn tại hiện thông báo lỗi thay cho lỗi máy chủ; (#42041) sản phẩm không công khai hiện thông báo lỗi thay cho form đổi thẻ
   - Contract Plan & Payment (FA-031) - khách đang hợp đồng sản phẩm đã bị ẩn KHÔNG tự đổi thẻ qua đường dẫn được nữa (giống bản cũ) — PO chưa chốt

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: runtime-data
   Lệnh: php -l app/Http/Controllers/Basic/SalesManagementV2Controller.php: No syntax errors detected; Biên dịch giao diện bằng đúng bộ biên dịch Blade của Laravel trong vendor rồi chạy phần luôn được render (khi có thông báo lỗi): TRƯỚC fix ném đúng lỗi 'Undefined variable: flagCycle' như ticket, SAU fix render thành công; Kiểm tra nội dung render sau fix: hiện đúng ô thông báo lỗi tiếng Nhật, không hiện nhầm khối 'đã đăng ký sản phẩm'; git diff --stat origin/release_step_20260827...ai_fixbug_41004: 1 file changed, 1 insertion; [#42041] Harness verify/42041/harness.php gọi THẬT orderChange + render view: TRƯỚC fix sản phẩm ẩn vẫn hiện form (khớp kết quả tester); SAU fix ẩn+link khách → báo lỗi, không có nút đổi; công khai và preview không đổi
   Bằng chứng: Lịch sử git: commit 32d1fb10e8 'fix exception' trước đây đã vá đúng nhánh trả về sớm này nhưng chỉ thêm biến danh sách thương hiệu thẻ, bỏ sót biến cờ chu kỳ - xác nhận đây là vá thiếu chứ không phải code chết; Khối nội dung chính của giao diện nằm trong điều kiện từ dòng 162 đến 1229, bị bỏ qua khi có thông báo lỗi; vùng còn lại (dòng 1-161) mọi biến khác đều bọc kiểm tra tồn tại nên chỉ thiếu đúng biến cờ chu kỳ; Không tái hiện được qua web dev (http://host.docker.internal:8000 không truy cập được tại thời điểm chạy) - đã thay bằng kiểm chứng biên dịch + chạy thật giao diện

■ TỰ REVIEW (AI)
Fix tối giản đúng root cause: thêm 1 dòng truyền biến cờ chu kỳ vào giao diện ở nhánh trả về sớm. Biến đã được khởi tạo bằng 0 ở đầu hàm trước điểm trả về nên giá trị truyền xuống luôn hợp lệ và giao diện đi đúng nhánh hiển thị thông báo lỗi. Không đổi hành vi của luồng bình thường (sản phẩm tồn tại) vì nhánh đó vốn đã truyền đủ biến. Đã kiểm chứng bằng cách chạy thật phần giao diện được render.
 • Rủi ro / lưu ý khi test:
   - Rủi ro rất thấp: thay đổi 1 dòng, chỉ thêm biến vào mảng truyền cho giao diện, không đụng truy vấn hay dữ liệu
   - Giao diện enter-payment-info vẫn còn dùng biến cờ chu kỳ không bọc kiểm tra tồn tại ở dòng 156/162 - nếu sau này có thêm nhánh trả về sớm mới mà quên truyền biến thì lỗi tái diễn. Cách chống tận gốc là bọc kiểm tra tồn tại trong giao diện, nhưng nằm ngoài phạm vi fix tối giản của ticket này - để reviewer quyết định
   - [#42041] Test Studio đang dựng bản test từ ai_small_41004 — branch đó KHÔNG có commit #42041 ⇒ phải trỏ Test Studio sang ai_fixbug_41004 thì retest mới thấy fix
   - [#42041] 2 branch cha lệch nhau: ai_small_41004 có thêm blade $flagCycle ?? 0 (ghi chú Redmine #41004 nhắc tới) nhưng thiếu fix #42041; ai_fixbug_41004 ngược lại — chỉ merge 1 trong 2
   - [#42041] PO chưa chốt việc chặn đổi thẻ khi sản phẩm đã ẩn

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41004 (nhánh gốc release_step_20260827, commit d01e9e391d, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 20 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=cc5302a0-1cad-4d40-b2a5-8142d995b59f
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41004
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

> Journal #140117 (cùng tác giả, cùng thời điểm 2026-10-05) là **bản lặp nguyên văn** của Journal #140116 — không chép lại lần 2, xem #140116 trên.
