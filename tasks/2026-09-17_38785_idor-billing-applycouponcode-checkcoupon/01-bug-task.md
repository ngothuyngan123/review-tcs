# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38785 — IDOR billing: applyCouponCode/checkCouponCode gia hạn hợp đồng bot theo id từ request, không check owner` |
| Module / Màn hình | Màn chi tiết hợp đồng (契約情報 — `/detail-contract/{id}`) → modal nhập mã coupon (クーポンコード). API: `/ajax/check-coupon-code` · `/ajax/apply-coupon-code`. Liên quan Coupon Code Issue (FS-015) + Contract Plan & Payment (FA-031). |

## Mô tả bug (bản dịch tiếng Việt)

Lỗ hổng **IDOR (Insecure Direct Object Reference) ở tầng billing** — ticket do hệ thống tự detect (tracker "Bug tự detect"), không phải khách hàng báo.

- Vị trí: `app/Http/Controllers/Admin/UserController.php:9606`
- `applyCouponCode` / `checkCouponCode` (dòng 9560) đọc `botContractId` / `botId` **thẳng từ request**; sau khi chỉ validate coupon tồn tại + chưa dùng, chạy:
  - `BotContracts::where('id', $botContractId)->update(expired_date_contract)`
  - `Bots::where('id', $botId)->update(expired_date)`
- **Không kiểm** coupon / bot / contract có thuộc `Auth::user()` hay không.
- Route chỉ nằm dưới middleware `check_login` → **bất kỳ user nào đã đăng nhập cũng gia hạn được hợp đồng trả phí của bot người khác** bằng một coupon chưa dùng bất kỳ.

**Đề xuất (trong ticket gốc):** scope coupon theo `admin_id`; verify `BotContracts` / `Bots` thuộc user (qua `getListBotId`) **trước khi** mutate `expired_date`.

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" — ticket do hệ thống tự detect từ source code. -->

## Expected result

<!-- Trống — xem Steps to reproduce. -->

## Actual result

<!-- Trống — xem Steps to reproduce. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38785 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket thuộc tracker **"Bug tự detect"** (phát hiện từ đọc code, không có ca lỗi thật từ khách hàng). Root cause đã được AI Auto-fixbug confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung **verify cách fix + regression impact**, không phải reproduce.
- **Priority ticket = Urgent**, status hiện tại = **Fix done - Đợi test**.
- ⚠️ **Đây là bug billing (gia hạn hợp đồng trả phí)** → theo **RULE-08**, kết luận không được rút ra từ môi trường `local`/`staging`. Toàn bộ 10 TC đã chạy trên Studio đều ở `env = local` (xem file 04).
- **Cần tối thiểu 2 tài khoản test** để dựng ca IDOR: `userA` = chủ hợp đồng HA (bot BA); `userB` = user khác, **không** phải chủ HA và **không** có quyền `pointSettings` trên BA. Thêm 1 tài khoản **staff có quyền `pointSettings`** để cover nhánh `listBotAccept`.
- **Điều kiện dữ liệu bắt buộc:** hợp đồng dùng để test phải có bản ghi **`bot_slots` hợp lệ** — `Bots::dataBotContract` inner join `bot_slots`, thiếu bản ghi này thì hợp đồng đúng chủ vẫn bị chặn (rủi ro do chính fix gây ra, xem REQ-006 / TC `NEW-9` ở file 04).
- **Coupon test** phải ở trạng thái `coupon_management.is_used = 0`; mỗi coupon chỉ dùng được 1 lần → chuẩn bị đủ số coupon cho số TC apply thành công.
- **Mâu thuẫn cần Leader chốt:** báo cáo Dev ghi *"botId vẫn lấy từ request như cũ"*, nhưng TC `NEW-8` / `NEW-12` trên Studio ghi ngược lại là *"BE bỏ qua botId từ request, lấy từ `$botContract->bot_id` qua bot_slots"* (dẫn diff `-$botId=$request->botId`). Phải xác minh trên code/diff thật trước khi chốt expected của nhóm TC này.

## Journal / note từ Redmine (nguyên văn)

**Journal #125990 — AI LME Fix bug — 2026-07-14:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Hai API áp/kiểm coupon (checkCouponCode, applyCouponCode) chỉ nằm sau đăng nhập nhưng đọc thẳng mã coupon + id hợp đồng bot + id bot từ request rồi gia hạn hạn hợp đồng, không kiểm coupon/hợp đồng/bot có thuộc người đang đăng nhập không. Bất kỳ user nào cũng có thể dùng 1 coupon chưa dùng để gia hạn hợp đồng trả phí của bot người khác (IDOR).

■ 2. CÁCH FIX
checkCouponCode + applyCouponCode: thay truy vấn hợp đồng thô (BotContracts::where id) bằng Bots::dataBotContract(botContractId, getListBotIdStaffManagement(userId,pointSettings), userId) — hàm chuẩn dự án tự lọc quyền (chỉ trả hợp đồng khi bot thuộc quyền staff của user HOẶC bot_contracts.admin_id = user), trả null → coupon không hợp lệ, không gia hạn. botId vẫn lấy từ request như cũ. Coupon giữ nguyên lookup theo coupon_code. Bỏ 1 truy vấn hợp đồng bị lặp.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
checkCouponCode (app/Http/Controllers/Admin/UserController.php)
applyCouponCode (app/Http/Controllers/Admin/UserController.php)
Bots::dataBotContract (app/Bots.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/UserController.php
 • 4.2 Data ảnh hưởng:
   - Không có (chỉ đổi cách lấy/kiểm quyền hợp đồng)
 • 4.3 Tính năng liên quan:
   - Coupon Code Issue (FS-015) — chỉ chủ/staff-có-quyền của hợp đồng mới áp/kiểm được coupon
   - Contract Plan & Payment (FA-031) — gia hạn hợp đồng chỉ khi hợp đồng thuộc quyền người đăng nhập

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l UserController.php: No syntax errors
   Bằng chứng: Bots::dataBotContract lọc bots.id IN listBotAccept OR bot_contracts.admin_id==user; dùng nhất quán ở PointSettingController/ListPageController/BotEnterPriseController cho thao tác billing

■ TỰ REVIEW (AI)
Fix theo phản hồi human: xác thực quyền hợp đồng bằng Bots::dataBotContract (chuẩn dự án billing); botId giữ nguyên lấy từ request; coupon không đổi.
 • Rủi ro / lưu ý khi test:
   - botId lấy từ request như hành vi gốc — cập nhật Bots.expired_date theo botId client; quyền đã kiểm ở tầng hợp đồng qua dataBotContract

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38785 (nhánh gốc release_step_20260623, commit 48877bb5b3, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 43 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=a28dcb78-203f-43dc-9dd8-83c28f131a5f
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38785
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #125991 — AI LME Fix bug — 2026-07-14:** nội dung **trùng hoàn toàn** Journal #125990 (hệ thống Auto-fixbug post 2 lần) — không chép lại.
