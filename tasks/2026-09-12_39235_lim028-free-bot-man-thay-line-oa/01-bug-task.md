# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39235 — [LME-Studio] LIM-028: bot gói Free (cả Free cũ và Free mới đã hết cửa sổ campaign) vẫn vào được màn thay LINE OA` |
| Module / Màn hình | `Bot / LOA Connection Settings (FA-038) — màn thay LINE OA (LINE公式アカウント入れ替え / LOA入れ替え), endpoint GET /admin/change-bots-new/{bot_id mã hoá Hashids}` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine viết sẵn bằng tiếng Việt — giữ nguyên văn, không dịch lại. -->

Bug từ LME Test Studio — severity Medium
Task: #42
Test case: NEW-154

Theo giới hạn LIM-028, bot gói Free không được dùng chức năng thay LINE OA; riêng bot Free mới chỉ được dùng trong 1 tháng cửa sổ campaign kể từ ngày tạo bot. Thực tế cả bot Free cũ (`plan_type=2`, `flag_contract_new=0`, tạo trước 2021-07-01) lẫn bot Free mới đã quá 1 tháng (`has_campaign=0`) đều vẫn mở được màn thay LINE OA bằng URL trực tiếp.

Nguyên nhân được nêu ngay trong ticket: hàm `adminChangeNewBot()` không có guard gói/campaign — guard này chỉ tồn tại ở `adminChangeBotSub()` (màn thay tài khoản phụ).

## Steps to reproduce

1. Chuẩn bị bot gói Free cũ (`plan_type=2`, `flag_contract_new=0`, ngày tạo trước 2021-07-01).
2. Đăng nhập bằng chủ tài khoản và chọn bot đó.
3. Gọi `GET /admin/change-bots-new/{mã định danh bot đã mã hoá bằng Hashids}`.
4. Lặp lại với bot Free mới có ngày tạo cách hiện tại 35 ngày và cờ `has_campaign=0`.

## Expected result

- Theo LIM-028, gói Free không được thay LINE OA; riêng bot Free mới chỉ được trong 1 tháng campaign.
- Ngoài phạm vi đó, truy cập màn thay LINE OA phải bị **chuyển hướng về trang chủ admin**.

## Actual result

- Cả hai trường hợp đều trả **HTTP 200** kèm nội dung màn thay LINE OA, **không có chuyển hướng**.
- Với bot Free mới quá 1 tháng, endpoint kiểm campaign `POST /admin/check-auth-bot` đã trả `{"success":false,"message":"Unauthorized access."}` nhưng màn thay LINE OA **vẫn mở được** — hàm `adminChangeNewBot()` không có guard gói/campaign (guard chỉ tồn tại ở `adminChangeBotSub()`).

## Ảnh / video / log đính kèm

- [x] Có file đính kèm (2 file, `content_type = application/octet-stream`, không rõ định dạng — tester mở trực tiếp trên Redmine để xác định)

- https://redmine.watermelon.vn/attachments/download/28627/6173 (`6173`, 16274 bytes)
- https://redmine.watermelon.vn/attachments/download/28628/6253 (`6253`, 16468 bytes)

## Ghi chú thêm của Leader

- **Bug do AI Auto test LME phát hiện** (author = `AI Auto test Lme`), không phải khách hàng báo. Nguồn: LME Test Studio task #42, test case `NEW-154`.
- **Bug đã được AI Auto-fixbug fix** — branch `ai_fixbug_39235` (gốc `release_step_20260805`, commit `3057ac6942`, 1 file, +10 dòng). Status Redmine: *Fix done - Đợi test*.
- ⚠️ **CONFLICT EXPECTED — cần Leader/PM chốt trước khi test**: ticket ghi expected là *"chuyển hướng về trang chủ admin"*, nhưng bản fix lại **trả trang chặn HTTP 200** (`change_bot_plan_blocked.blade.php`, thông báo 「スタンダードプラン以上のご契約でご利用できます」) rồi đưa sang **màn thêm/chọn tài khoản `/admin/bot-add`** — khác cả HTTP code lẫn đích đến so với `/basic/overview`. Dev chọn cách này để đồng nhất với màn thay tài khoản phụ (#39230). Nếu PM chốt theo đúng câu chữ ticket thì bản fix phải sửa lại.
- **Điều kiện tiên quyết dựng env**: cần bot ở đủ 3 nhánh dữ liệu — Free cũ (`plan_type=2`), Free mới (`plan_type=1` + `bot_contracts.contract_type='free'`), và bot trả phí (Standard cũ / Standard mới / Pro). Ngày tạo bot là biến quyết định (mốc = ngày tạo + 1 tháng, tính **hết ngày** 23:59:59).
- **Nhận diện gói Free toàn hệ thống** = `plan_type == 2` (Free cũ) **HOẶC** `bot_contracts.contract_type == 'free'` (Free mới) — đóng gói ở `Bots::isFreePlan()`.
- ⚠️ **Điểm hở Dev tự ghi nhận, KHÔNG fix trong ticket này**: guard phía API đổi LOA (`ChangeBotController::init` / `botCanChangeBot` / `execute`) vẫn chỉ nhận diện Free bằng `plan_type = 2` → bot **Free mới hết campaign về lý thuyết vẫn gọi thẳng API đổi LOA được**. Dev đề nghị tách ticket riêng.
- **Tần suất lỗi**: 100% (lỗi logic thiếu guard, không phải xác suất).
- **Môi trường verify của Dev**: chỉ ở mức **lint + đọc code** — MySQL dev (`host.docker.internal:3306`) không kết nối được trong phiên AI fix (Connection refused) → **chưa tái hiện được bằng dữ liệu thật**.

## Journal / note từ Redmine (nguyên văn)

> Redmine có **2 journal** (#133261 và #133262) nội dung **trùng nhau hoàn toàn** — cùng là báo cáo AI Auto-fixbug đăng 2026-08-27. Chép 1 bản dưới đây.

**Journal #133261 — AI LME Fix bug — 2026-08-27:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn thay LINE OA (/admin/change-bots-new) chỉ kiểm tra quyền truy cập theo tài khoản, KHÔNG kiểm tra gói cước và cửa sổ campaign. Quy tắc bot gói miễn phí chỉ được thay LINE OA trong 1 tháng kể từ ngày tạo bot mới chỉ được cài ở màn kế bên (thay tài khoản phụ) và ở phía giao diện, nên bot Free cũ lẫn Free mới đã hết campaign vẫn mở được màn hình này bằng URL trực tiếp.

■ 2. CÁCH FIX
Bổ sung chốt chặn theo gói ở phía máy chủ cho màn thay LINE OA (hàm dựng màn /admin/change-bots-new): bot gói miễn phí đã quá 1 tháng kể từ ngày tạo bot thì không vào được màn hình mà chuyển sang trang thông báo cần nâng cấp gói — dùng đúng trang chặn và đúng quy tắc campaign mà màn thay tài khoản phụ đang áp dụng. Điểm khác: nhận diện gói miễn phí bằng hàm dùng chung của model bot nên phủ cả Free cũ (plan_type = 2) lẫn Free mới (loại hợp đồng 'free'), trong khi guard cũ chỉ xét Free cũ. Quét ngang: các điểm còn lại trong luồng thay LINE OA (khởi tạo dữ liệu màn, thực thi đổi LOA) vẫn nhận diện gói miễn phí chỉ bằng plan_type = 2 — đã ghi nhận, không sửa ngoài phạm vi ticket.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BotController::adminChangeNewBot (app/Http/Controllers/Admin/BotController.php) — đã thêm guard
BotController::adminChangeBotSub (app/Http/Controllers/Admin/BotController.php) — guard mẫu đã có từ #39230
BotController::userCanAccessChangeBot (app/Http/Controllers/Admin/BotController.php) — guard quyền truy cập, giữ nguyên
BotController::checkAuthBot (app/Http/Controllers/Admin/BotController.php) — chỉ kiểm cột has_campaign, không chặn được truy cập màn
ChangeBotController::init (app/Http/Controllers/Ajax/ChangeBotController.php) — dữ liệu is_free_plan/has_campaign cho màn
ChangeBotController::botCanChangeBot + execute (app/Http/Controllers/Ajax/ChangeBotController.php) — guard phía API đổi LOA
Bots::isFreePlan (app/Bots.php) — nhận diện gói miễn phí dùng chung
change_new.js selectMethod/fetchPageData (public/_assets/modules/change_bots/js/change_new.js) — chặn phía giao diện
admin/bots/change_bot_plan_blocked.blade.php — trang thông báo chặn theo gói

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/BotController.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ thêm điều kiện chặn khi dựng màn hình, không đọc/ghi thay đổi dữ liệu
 • 4.3 Tính năng liên quan:
   - LOA Connection Settings (FA-038) — màn thay LINE OA (LOA入れ替え) nay chặn bot gói miễn phí đã hết campaign 1 tháng
   - Add New Account (FA-032) — người dùng bị chặn được đưa về trang thêm/chọn tài khoản (dùng lại trang chặn sẵn có)

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/BotController.php: No syntax errors detected; git diff --stat release_step_20260805...ai_fixbug_39235: 1 file, +10 dòng — đúng phạm vi
   Bằng chứng: Quy tắc campaign lấy nguyên từ BotController::adminChangeBotSub (#39230): free && now >= created_at + 1 tháng (cuối ngày) → chặn; Nhận diện gói miễn phí toàn hệ thống = plan_type == 2 (free cũ) HOẶC bot_contracts.contract_type == 'free' (free mới) — đóng gói sẵn ở Bots::isFreePlan(), đang dùng ở ChatController/ActionScheduleController/BackupController; Laravel Connector đặt PDO ATTR_EMULATE_PREPARES/STRINGIFY_FETCHES = false nên plan_type trả về kiểu số, phép so sánh chặt trong isFreePlan() chạy đúng; MySQL dev (host.docker.internal:3306) không kết nối được trong phiên này (Connection refused) → không tái hiện được bằng dữ liệu thật, chỉ kiểm chứng bằng đọc mã nguồn

■ TỰ REVIEW (AI)
Fix tối giản đúng root cause: thêm đúng 1 chốt chặn theo gói ở hàm dựng màn thay LINE OA, dùng lại trang chặn và quy tắc campaign sẵn có của màn cùng họ (#39230). Không đụng giao diện, không đụng API, không đổi dữ liệu. Bot gói trả phí và bot miễn phí còn trong campaign không bị ảnh hưởng.
 • Rủi ro / lưu ý khi test:
   - Kết quả mong đợi của tester ghi 'chuyển hướng về trang chủ admin'; bản fix dùng lại trang chặn sẵn có (báo 'cần gói Standard trở lên' rồi đưa về trang thêm/chọn tài khoản) để đồng nhất với màn thay tài khoản phụ đã chốt ở #39230 — người dùng vẫn bị đẩy ra khỏi màn thay LINE OA nhưng có thông báo lý do. Nếu PM muốn đúng chữ 'về trang chủ admin' thì đổi 1 dòng thành redirect('/basic/overview')
   - Trường hợp hiếm: bot miễn phí đang chạy dở tiến trình đổi LOA mà campaign hết hạn đúng lúc đó sẽ không mở lại được màn theo dõi tiến độ (cửa sổ vài phút). Có thể nới bằng cách cho qua khi còn bản ghi lịch đổi đang xử lý, nhưng sẽ thêm truy vấn nên chưa làm
   - Guard phía API đổi LOA vẫn nhận diện gói miễn phí hẹp hơn (chỉ free cũ) nên bot Free mới hết campaign về lý thuyết vẫn gọi thẳng API được — đã ghi ở phần quét ngang, nên tách ticket riêng

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39235 (nhánh gốc release_step_20260805, commit 3057ac6942, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 57 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=65ab5ea9-9536-4264-8eec-3a5594fb946a
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39235
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #133262 — AI LME Fix bug — 2026-08-27:** nội dung **trùng 100%** với Journal #133261 ở trên (báo cáo bị đăng 2 lần).
