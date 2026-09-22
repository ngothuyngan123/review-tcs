# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn**: Redmine #38835 **KHÔNG có** section "Đánh giá ảnh hưởng" trong description. Nội dung dưới đây lấy **nguyên văn** từ **Journal #126738 (AI LME Fix bug, 2026-07-21)** — báo cáo tự động của hệ thống **Auto-fixbug LME**, mục ■ 1 → ■ 6. Journal #126744 trùng hoàn toàn.
>
> ⚠️ **Fix do AI sinh, mức verify mới chỉ là `lint` (`php -l`)** — chưa có test nghiệp vụ nào chạy thật ở phía Dev.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Kim Cúc |
| Commit / Pull Request | commit `07166865b2` (1 file) — không có link PR. Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38835 |
| Branch | `ai_small_38785` (repo `sns-line`, nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | 2026-07-21 |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #126738 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn ■ 1:

Bản fix trước (#38785) xác thực hợp đồng qua `Bots::dataBotContract` nên chặn được gia hạn hợp đồng người khác, nhưng câu cập nhật `bots.expired_date` vẫn dùng `botId` lấy thẳng từ request và chỉ kiểm bot tồn tại, không kiểm bot có thuộc hợp đồng đã xác thực. Kẻ tấn công truyền `botContractId` hợp lệ của mình cùng `botId` của bot nạn nhân → gia hạn được hạn của bot bất kỳ (residual IDOR).

## 2. Cách fix

> Nguyên văn ■ 2:

`applyCouponCode`: bỏ đọc `botId` từ request; sau khi xác thực hợp đồng qua `Bots::dataBotContract`, lấy `botId = $botContract->bot_id` (bot thật gắn với hợp đồng qua `bot_slots`) rồi mới lookup + update `bots.expired_date`. Nhờ đó chỉ gia hạn đúng bot của hợp đồng thuộc người đăng nhập, không thể gia hạn bot bất kỳ theo id request.

**Bằng chứng Dev đưa ra (■ 6 VERIFY)**: `dataBotContract` trả `bots.id as bot_id` qua join `bot_slots` — bot thật của hợp đồng đã lọc quyền (`bots.id IN listBotAccept` OR `bot_contracts.admin_id == user`).

**Tự review của AI (■ TỰ REVIEW)**: Fix tối thiểu 1 dòng: derive `botId` từ hợp đồng đã xác thực thay vì tin request. Cùng pattern `dataBotContract` đã dùng nhất quán trong dự án.

**Rủi ro / lưu ý khi test (Dev nêu)**: Nếu FE gửi `botId` khác bot của hợp đồng (trường hợp hợp lệ hiếm) sẽ gia hạn bot của hợp đồng — đúng ý nghĩa nghiệp vụ (coupon áp cho hợp đồng).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn ■ 3 (Dev chỉ liệt kê tên, không ghi cột "thay đổi" / "lý do" — phần trong ngoặc là ánh xạ theo mục 2, KHÔNG phải chữ của Dev):

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `applyCouponCode` (`app/Http/Controllers/Admin/UserController.php`) | Đã sửa — bỏ đọc `botId` từ request, derive từ `$botContract->bot_id` | Function chứa lỗi IDOR |
| 2 | `checkCouponCode` (`app/Http/Controllers/Admin/UserController.php`) | Đã check — Dev không ghi có sửa | Bước preview dùng chung luồng coupon |
| 3 | `Bots::dataBotContract` (`app/Bots.php`) | Đã check — Dev không ghi có sửa | Nguồn xác thực hợp đồng + nguồn `bot_id` mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Nguyên văn ■ 4.1 của Dev chỉ liệt kê **file thay đổi**, không liệt kê function. Bảng dưới gộp ■ 4.1 (file) với ■ 3 (function đã check) để có tag `F*` dùng cho coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `applyCouponCode` — API `/admin/ajax/apply-coupon-code` | `app/Http/Controllers/Admin/UserController.php` | Direct | **Function duy nhất Dev khai có sửa.** Nguồn `botId` đổi từ request → `$botContract->bot_id` |
| F2 | `checkCouponCode` — API `/admin/ajax/check-coupon-code` | `app/Http/Controllers/Admin/UserController.php` | Indirect | Dev khai "đã check" ở ■ 3, không khai có sửa. ⚠️ Tiêu đề ticket nêu cả `checkCouponCode`, nhưng ■ 2 chỉ mô tả sửa `applyCouponCode` |
| F3 | `Bots::dataBotContract` | `app/Bots.php` | Indirect | Không sửa, nhưng sau fix **toàn bộ** tính đúng của `botId` phụ thuộc function này (trust boundary mới) |

**■ 4.1 nguyên văn (File thay đổi):** `app/Http/Controllers/Admin/UserController.php`

### 4.2. List data bị update khi fix bug

> Nguyên văn ■ 4.2: **"Không có (chỉ đổi nguồn lấy `botId` khi cập nhật `bots.expired_date`, không migrate dữ liệu)"**

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.expired_date` | UPDATE (runtime) | Dev khai "không có data ảnh hưởng" theo nghĩa **không migrate**. Nhưng **đối tượng bị UPDATE đã đổi** (trước: bot theo `botId` request; sau: bot của hợp đồng) → vẫn là chiều cần verify |
| D2 | `bot_contracts.expired_date_contract` | UPDATE (runtime) | Không đổi bởi fix này (#38785 đã xử lý), nhưng nằm chung transaction apply coupon |
| D3 | `coupon_management.is_used` / `user_id` / `user_email` / `bot_name` | UPDATE (runtime) | `bot_name` suy từ bot được gia hạn → **đổi theo fix** (lấy `view_name` của bot hợp đồng thay vì bot theo request) |
| D4 | `bot_life_cycles` (record `type=29` APPLY_COUPON) | CREATE (runtime) | `admin_id` / `bot_id` ghi log suy từ bot hợp đồng → đổi theo fix |

⚠️ **D1–D4 KHÔNG có trong khai báo của Dev** (Dev ghi "Không có") — suy ra từ ■ 2 + nội dung TC Studio, cần Leader/Dev xác nhận.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn ■ 4.3:

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Coupon Code Issue (FS-015)** — áp coupon chỉ gia hạn đúng bot của hợp đồng thuộc người đăng nhập | F1, D1, D3, D4 | `<Dev không ghi mức>` |
| T2 | **Contract Plan & Payment (FA-031)** — chặn gia hạn `bots.expired_date` của bot người khác qua `botId` giả từ request | F1, D1, D2 | `<Dev không ghi mức>` |

## 5. Recover data (nguyên văn ■ 5)

✔ Không cần recover data.

⚠️ Ticket **không đề cập** việc dò/khôi phục các bot đã bị gia hạn sai bởi lỗ hổng này trước khi fix (nếu đã bị khai thác trên môi trường thật).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ Dev **không liệt kê caller khác** gọi `applyCouponCode` / `dataBotContract`; cần xác nhận còn nơi nào khác update `bots.expired_date` theo `botId` từ request không
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ 4.1 chỉ ghi **file**, không ghi function
- [ ] Mục 4.2 không thiếu data — ⚠️ Dev ghi **"Không có"**, xem cảnh báo D1–D4
- [ ] Mục 4.3 cover được cả happy path lẫn edge case của tính năng — ⚠️ Dev **không ghi mức nguy cơ regression**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
