# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35944 — [Bill tiền tool] Vẫn xảy ra case có nhiều slot trống của một plan` |
| Module / Màn hình | Bill tiền tool — màn **Thêm tài khoản mới** (Add New Account, FA-032) + API kiểm tra trước khi mua; liên quan Contract Plan & Payment (FA-031) |

## Mô tả bug (bản dịch tiếng Việt)

> Nguyên văn description Redmine (đã là tiếng Việt, chép nguyên văn):

Spec hiện tại của mình: Mỗi plan chỉ cho phép mua 1 slot trống

Nhưng khi mua liên tiếp nhiều slot trống của 1 plan bằng phương thức bill transfer => Sau đó chuyển khoản các khoản bill đó thì vẫn tạo được nhiều slot trống của một plan

## Steps to reproduce

> ⚠️ Ticket **không có** section "Tái hiện bug" riêng — 3 mục dưới đây tách thẳng từ câu mô tả trong description, không bổ sung thao tác nào ngoài nguyên văn.

1. Mua liên tiếp nhiều slot trống của **cùng 1 plan** bằng phương thức **bill transfer** (chuyển khoản).
2. Sau đó chuyển khoản (thanh toán) các khoản bill đó.

## Expected result

- Mỗi plan chỉ cho phép mua 1 slot trống.

## Actual result

- Vẫn tạo được nhiều slot trống của một plan.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #35944 không có attachment nào (Attachments (0)). -->

## Ghi chú thêm của Leader

- **Điều kiện tiên quyết**: tài khoản có plan còn slot; phương thức thanh toán **chuyển khoản (bill transfer / `type_bill = 3`)**; cần đặt được **≥ 2 bill liên tiếp** cùng 1 plan trước khi bill đầu vào tiền.
- **Bug liên quan tiền / hợp đồng** → theo **RULE-08**, kết luận cuối phải test trên **product**; không kết luận từ local/staging.
- Dev (AI auto-fixbug) ghi rõ trong journal: **"Không tái hiện được trên dev"** — MySQL `host.docker.internal:3306` báo Connection refused nên không dump được dữ liệu hợp đồng chờ chuyển khoản. Verify chỉ dừng ở mức **lint** (`php -l`) + `git diff --stat`, **không có bằng chứng chạy thực tế**.
- Dev tự nêu 2 rủi ro cần chú ý khi test:
  1. Khách đặt bill chuyển khoản rồi **không thanh toán và không bấm hủy** sẽ bị chặn mua thêm slot cùng gói cho tới khi hủy bill hoặc hợp đồng quá hạn.
  2. Kiểm tra **không khóa hàng (no lock)** → 2 tab bấm mua **đồng thời** vẫn có thể lọt; Dev coi đây là hạn chế sẵn có, không thuộc phạm vi ticket.
- Trạng thái ticket lúc fetch: **Fix done - Đợi test** | Assignee: Ngọc Ánh | Author: Ngô Thúy Ngần.

## Journal / note từ Redmine (nguyên văn)

**Journal #133416 — AI LME Fix bug — 2026-08-28:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Bộ đếm slot trống của mỗi gói chỉ tính hợp đồng đã kích hoạt. Hợp đồng mua bằng chuyển khoản chỉ được kích hoạt khi cổng thanh toán báo đã nhận tiền, nên slot vừa đặt mua còn đang chờ chuyển khoản không bị đếm. Vì vậy khách đặt liên tiếp nhiều bill cùng một gói đều lọt qua kiểm tra, và khi các khoản đó vào tiền thì mỗi hợp đồng sinh ra một slot trống, dẫn tới nhiều slot trống của cùng một gói.

■ 2. CÁCH FIX
Sửa 2 truy vấn đếm slot chưa gắn tài khoản của màn mua gói (trang Thêm tài khoản mới và API kiểm tra trước khi mua) để tính cả hợp đồng thanh toán bằng chuyển khoản chưa thu được tiền là đang giữ chỗ, thay vì chỉ đếm hợp đồng đã kích hoạt. Gom điều kiện dùng chung vào hàm applyUnconnectedSlotCondition trong cùng controller. Quét ngang 4 truy vấn tương tự ở UserController: đều là danh sách slot dùng được ngay nên giữ nguyên.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BotV2Controller::index (app/Http/Controllers/Admin/BotV2Controller.php)
BotV2Controller::getSlotUnconnectBot (app/Http/Controllers/Admin/BotV2Controller.php)
BotV2Controller::applyUnconnectedSlotCondition (app/Http/Controllers/Admin/BotV2Controller.php - thêm mới)
BotController::paymentBotSlotV2 (app/Http/Controllers/Admin/BotController.php - đọc, không sửa)
BotController::univapayCallback (app/Http/Controllers/Admin/BotController.php - đọc, không sửa)
ListPageController::cancelTransfer (app/Http/Controllers/V2/Bill/ListPageController.php - đọc, không sửa)
isContractWaitingTransfer (public/_assets/modules/bill/js/index.js - đối chiếu cách xác định đang chờ chuyển khoản)
getListUserMaster / showModalTypeContractNewStep (public/js/admin/bill_tool/index.js - đọc, không sửa)
UserController::initDataListBot / botsForUser / checkOnePlan (app/Http/Controllers/Admin/UserController.php - quét ngang, khác phạm vi)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/BotV2Controller.php
 • 4.2 Data ảnh hưởng:
   - Không có - fix chỉ đọc dữ liệu, không ghi/sửa bảng nào
 • 4.3 Tính năng liên quan:
   - Add New Account (FA-032) — chặn mua thêm slot trống khi đã có bill chuyển khoản cùng gói đang chờ thanh toán
   - Contract Plan & Payment (FA-031) — hợp đồng chờ chuyển khoản nay được tính là đang giữ chỗ slot

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/BotV2Controller.php: No syntax errors detected; git diff --stat origin/release_step_20260805...ai_fixbug_35944: 1 file, 35 insertions, 14 deletions
   Bằng chứng: BotController::paymentBotSlotV2 tạo hợp đồng chuyển khoản với is_active = inactive, sau khi tạo charge mới set status = 1 và status_payment = 0; univapayCallback khi nhận được tiền (type_bill = 3) mới set is_active = 1 và status_payment = 1 - đó là lúc slot trống trở nên hữu hình với bộ đếm cũ; Không tái hiện được trên dev: MySQL host.docker.internal:3306 báo Connection refused nên không dump được dữ liệu hợp đồng chờ chuyển khoản

■ TỰ REVIEW (AI)
Fix đúng root cause tại nguồn dữ liệu của cả 2 điểm kiểm tra phía server. Điều kiện đang chờ chuyển khoản lấy đúng theo cách màn danh sách hợp đồng đang dùng (payment_method = chuyển khoản và status_payment khác đã thu/lỗi thu), giữ nguyên các ràng buộc cũ nên chỉ THÊM tập hợp đồng chuyển khoản chưa thu tiền, không loại bỏ trường hợp nào đang được đếm.
 • Rủi ro / lưu ý khi test:
   - Khách đặt bill chuyển khoản rồi không thanh toán và không bấm hủy sẽ bị chặn mua thêm slot cùng gói cho tới khi hủy bill hoặc hợp đồng quá hạn - đúng theo spec mỗi gói chỉ 1 slot trống, màn hóa đơn có sẵn nút hủy chuyển khoản
   - Kiểm tra không khóa hàng nên 2 tab bấm mua ĐỒNG THỜI vẫn có thể lọt - hạn chế sẵn có của mọi giới hạn theo gói, không phải kịch bản của ticket (mua liên tiếp)
   - Hợp đồng chuyển khoản bị hủy bị xóa hẳn khỏi bảng (không phải xóa mềm) và hợp đồng đã hủy có status = 3 nên không chặn nhầm

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_35944 (nhánh gốc release_step_20260805, commit c3b7019dcd, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 9 phút 46 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=8f106e22-8551-498f-be75-4757fac903af
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=35944
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
