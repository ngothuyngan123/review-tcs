# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38835 — Residual IDOR: applyCouponCode vẫn tin botId từ request → gia hạn bots.expired_date của bot bất kỳ` |
| Module / Màn hình | Màn chi tiết hợp đồng bot — áp mã coupon (bill/detail) · API `/admin/ajax/apply-coupon-code`, `/admin/ajax/check-coupon-code` · Coupon Code Issue (FS-015) + Contract Plan & Payment (FA-031) |

## Mô tả bug (bản dịch tiếng Việt)

Bug do Auto-QA (AI LME TEST) phát hiện khi test ticket #38785: "IDOR billing: applyCouponCode/checkCouponCode gia hạn hợp đồng bot theo id từ request, không check owner".

**【Mô tả】**

Bản fix xác thực hợp đồng qua `Bots::dataBotContract(botContractId,...)` đã chặn được việc gia hạn hợp đồng (`bot_contracts.expired_date_contract`) của người khác. NHƯNG `botId` vẫn lấy thẳng từ request và câu `Bots::where(id,$botId)->update(expired_date)` chỉ kiểm bot tồn tại, KHÔNG kiểm bot thuộc user. Attacker chỉ cần sở hữu MỘT hợp đồng hợp lệ của chính mình + một coupon chưa dùng, truyền `botContractId` của mình (qua `dataBotContract`) nhưng `botId` của bot nạn nhân → gia hạn được `bots.expired_date` của bot bất kỳ. Đúng phần đề xuất ticket chưa hoàn tất: "verify BotContracts/Bots thuộc user (`getListBotId`) trước khi mutate `expired_date`" — mới verify Contract, chưa verify Bot.

**【Mức độ】** medium

**【Liên quan】**
- Ticket gốc: #38785
- Test case: TC-15
- Báo cáo đầy đủ (kèm ảnh/log): https://dashboard-test.melonglobal.net/automation-test/report.html?ticket=38785&bug=BUG-01

*(Ticket tạo tự động bởi pipeline automation-test.)*

## Steps to reproduce

1. Đăng nhập user A (có 1 hợp đồng hợp lệ + 1 coupon chưa dùng)
2. Gọi `apply-coupon-code` với `botContractId` = hợp đồng của A, `botId` = bot của nạn nhân B
3. Quan sát `bots.expired_date` của bot B

## Expected result

- Bot B không bị đổi hạn (không thuộc user A)

## Actual result

- `bots.expired_date` của bot B bị gia hạn (2026-08-15 → 2026-09-14)

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine không có attachment. Báo cáo Auto-QA kèm ảnh/log nằm ở link dashboard-test.melonglobal.net phía trên (ngoài Redmine). -->

## Ghi chú thêm của Leader

- **Bug do AI Auto-QA phát hiện, KHÔNG phải khách hàng báo** — repro bằng cách craft request API (thao túng tham số `botId`), FE bình thường không gửi được ca này. Steps 2 phải dùng công cụ gửi HTTP trực tiếp (session + `X-CSRF-TOKEN` của A), không bấm được trên UI.
- **Điều kiện tiên quyết dựng env**: cần **2 tài khoản** (A tấn công — có ≥ 1 hợp đồng bot còn hạn + 1 coupon chưa dùng `is_used=0`; B nạn nhân — sở hữu bot BV mà A không có quyền, BV không nằm trong `listBotAccept` / `listBotIdStaffManagement` của A). Coupon do system-admin phát hành.
- **Đây là bug bảo mật (IDOR) tầng API** — lỗi xảy ra 100% khi craft đúng request, không phải bug xác suất.
- Fix do **AI Auto-fixbug** thực hiện (branch `ai_small_38785`, commit `07166865b2`), mức verify mới chỉ là **lint** (`php -l`) — chưa có test chạy thật ở tầng nghiệp vụ. Xem file `03-dev-impact.md`.
- ⚠️ Journal #126738 và #126744 **nội dung trùng nhau hoàn toàn** (cùng phiên AI, cùng commit) — không phải 2 lần fix khác nhau.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — ticket chỉ ghi "bot của nạn nhân B", không nêu id cụ thể>` |
| Friend | `<không liên quan — bug ở tầng hợp đồng/bot>` |
| Đối tượng cấu hình | Hợp đồng bot của A (`botContractId`) + coupon chưa dùng của A; bot nạn nhân B (`botId` bị thao túng) |
| Thời điểm lỗi | `<chưa rõ — ticket tạo 2026-07-15 07:48>` |
| Đối chứng | `bots.expired_date` bot B: 2026-08-15 → 2026-09-14 (giá trị bị gia hạn sai ở bản lỗi) |

## Journal / note từ Redmine (nguyên văn)

**Journal #126738 — AI LME Fix bug — 2026-07-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Bản fix trước (#38785) xác thực hợp đồng qua Bots::dataBotContract nên chặn được gia hạn hợp đồng người khác, nhưng câu cập nhật bots.expired_date vẫn dùng botId lấy thẳng từ request và chỉ kiểm bot tồn tại, không kiểm bot có thuộc hợp đồng đã xác thực. Kẻ tấn công truyền botContractId hợp lệ của mình cùng botId của bot nạn nhân → gia hạn được hạn của bot bất kỳ (residual IDOR).

■ 2. CÁCH FIX
applyCouponCode: bỏ đọc botId từ request; sau khi xác thực hợp đồng qua Bots::dataBotContract, lấy botId = $botContract->bot_id (bot thật gắn với hợp đồng qua bot_slots) rồi mới lookup + update bots.expired_date. Nhờ đó chỉ gia hạn đúng bot của hợp đồng thuộc người đăng nhập, không thể gia hạn bot bất kỳ theo id request.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
applyCouponCode (app/Http/Controllers/Admin/UserController.php)
checkCouponCode (app/Http/Controllers/Admin/UserController.php)
Bots::dataBotContract (app/Bots.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/UserController.php
 • 4.2 Data ảnh hưởng:
   - Không có (chỉ đổi nguồn lấy botId khi cập nhật bots.expired_date, không migrate dữ liệu)
 • 4.3 Tính năng liên quan:
   - Coupon Code Issue (FS-015) — áp coupon chỉ gia hạn đúng bot của hợp đồng thuộc người đăng nhập
   - Contract Plan & Payment (FA-031) — chặn gia hạn bots.expired_date của bot người khác qua botId giả từ request

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l UserController.php: No syntax errors detected
   Bằng chứng: dataBotContract trả bots.id as bot_id qua join bot_slots — bot thật của hợp đồng đã lọc quyền (bots.id IN listBotAccept OR bot_contracts.admin_id==user)

■ TỰ REVIEW (AI)
Fix tối thiểu 1 dòng: derive botId từ hợp đồng đã xác thực thay vì tin request. Cùng pattern dataBotContract đã dùng nhất quán trong dự án.
 • Rủi ro / lưu ý khi test:
   - Nếu FE gửi botId khác bot của hợp đồng (trường hợp hợp lệ hiếm) sẽ gia hạn bot của hợp đồng — đúng ý nghĩa nghiệp vụ (coupon áp cho hợp đồng)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38785 (nhánh gốc release_step_20260623, commit 07166865b2, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 33 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=717f05e3-81f7-423b-ade2-82dc8a66305a
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38835
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #126744 — AI LME Fix bug — 2026-07-21:**

```
(Nội dung TRÙNG HOÀN TOÀN Journal #126738 — cùng phiên AI 717f05e3, cùng branch ai_small_38785, cùng commit 07166865b2. Không chép lại.)
```
