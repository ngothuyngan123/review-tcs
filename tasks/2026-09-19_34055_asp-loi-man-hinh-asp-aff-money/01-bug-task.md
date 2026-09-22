# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #34055 bằng `/new-task` (2026-09-19). Metadata Redmine (ngày báo cáo, người báo, priority, URL) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34055 — [ASP] Lỗi màn hình ASP aff-money` |
| Module / Màn hình | Affiliate Reward Program (FA-027) — màn tiền thưởng cộng tác viên ASP (`aff-money`, 「ASP管理 紹介者（成約情報）」), tab 成約状況 (tình trạng chốt hợp đồng) — ô chọn bot |

## Mô tả bug (bản dịch tiếng Việt)

> Description Redmine không có phần mô tả của khách hàng / CS — chỉ có đánh giá ảnh hưởng phía Dev (đã tiếng Việt, chép nguyên văn):

```
1. Nguyên nhân
    - Trong logic có 1 query get list allbot nhiều record dẫn đến việc bùng RAM tạm thời, request bị kill 
2. Cách fix
    - Fix dùng chuck để lấy ra từng block record 
3. Đã check và sửa các function sử dụng đến function/data vừa sửa
4. Đánh giá ảnh hưởng
	4.1 List function
        - ajaxAffMoneyV2 (app/Http/Controllers/Affiliate/AffiliaterController.php)
	4.2 List những data bị update khi fix bug 
	4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
        - màn hình ASP aff tab 成約状況 (chỉ cần check show list bot đầy đủ chỗ select bot)
5. PR: https://bitbucket.org/snstool/sns-line/pull-requests/9507/diff
```

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #34055 không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Điều kiện tái hiện: tài khoản quản lý (admin) có **rất nhiều bot** → query lấy toàn bộ bot làm bùng RAM PHP, request bị kill (lỗi 500 / trắng màn). Tài khoản ít bot không tái hiện được.
- Theo journal AI auto-fixbug (2026-08-27): **PR 9507 ghi ở description KHÔNG có trên nhánh release** (`origin/release_step_20260805` vẫn là bản lỗi) → AI fix lại ở nhánh `ai_fixbug_34055` (commit `2f2a40d022`): chunk 200 bản ghi + `orderBy('id')` + bỏ 2 dòng `Log::info` theo từng bot.
- AI không tái hiện được trên dev (DB không kết nối, không có tài khoản ASP nhiều bot) → chỉ verify mức lint + đọc code.
- Rủi ro còn lại AI tự nêu: truy vấn hợp đồng vẫn N+1 (1 query/bot) → tài khoản cực nhiều bot vẫn có thể chậm/timeout; `affBotDetailV2` cùng file có pattern y hệt **chưa sửa** (yokoten).
- Branch release (journal 2026-09-19): `release_step_20260827`.

## Journal / note từ Redmine (nguyên văn)

**Journal #133252 — AI LME Fix bug — 2026-08-27:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn hình tiền thưởng ASP (tab tình trạng chốt hợp đồng) nạp TOÀN BỘ danh sách bot của tài khoản quản trị vào bộ nhớ cùng lúc để dựng ô chọn bot. Tài khoản có rất nhiều bot làm bộ nhớ tăng đột biến, request vượt giới hạn RAM của PHP nên bị kill giữa chừng và màn hình báo lỗi. Vòng lặp còn ghi 2 dòng log gỡ lỗi cho MỖI bot, khuếch đại thêm tải ghi đĩa theo số bot.

■ 2. CÁCH FIX
Sửa hàm dựng danh sách bot của màn tiền thưởng ASP: thay vì lấy hết bot một lần rồi lặp, nay duyệt theo từng khối 200 bản ghi (chunk) nên bộ nhớ dùng tại một thời điểm không tăng theo tổng số bot; thêm sắp xếp theo id để việc chia khối ổn định. Bỏ 2 dòng log gỡ lỗi in ra cho mỗi bot trong vòng lặp (log thừa từ lần sửa cũ, ghi theo số bot). Điều kiện lọc bot (hợp đồng pro/enterprise_pro/bot cũ/bot dùng thử) và dữ liệu trả về cho ô chọn bot giữ NGUYÊN. Quét ngang thấy 1 chỗ y hệt ở affBotDetailV2 cùng file — CHƯA sửa vì ngoài phạm vi ticket, đã ghi ở mục yokoten để human quyết định.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ajaxAffMoneyV2 (app/Http/Controllers/Affiliate/AffiliaterController.php) — hàm được sửa
affMoneyV2 (app/Http/Controllers/Affiliate/AffiliaterController.php) — chỉ trả view, không đụng
money_v2.js: list_option = response.listBot (public/js/affiliater/money_v2.js) — nơi tiêu thụ danh sách bot, dữ liệu trả về không đổi
affBotDetailV2 (app/Http/Controllers/Affiliate/AffiliaterController.php) — có pattern y hệt, KHÔNG sửa (ngoài scope, xem yokoten)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Affiliate/AffiliaterController.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đọc, không ghi/sửa dữ liệu
 • 4.3 Tính năng liên quan:
   - Affiliate Reward Program (FA-027) — màn hình tiền thưởng của cộng tác viên ASP, tab tình trạng chốt hợp đồng: ô chọn bot và bảng số liệu thưởng

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Affiliate/AffiliaterController.php: No syntax errors detected; Kiểm tra Laravel 5.5 có Builder::chunk: vendor/laravel/framework/.../Concerns/BuildsQueries.php:18 public function chunk($count, callable $callback) — OK; git diff --stat origin/release_step_20260805...ai_fixbug_34055: đúng 1 file, 13 thêm / 13 bớt
   Bằng chứng: Không tái hiện được trên dev (MySQL host.docker.internal:3306 Connection refused, không có tài khoản ASP nhiều bot để dựng lại OOM); Đối chiếu lịch sử: git log -L cho thấy vòng lặp + 2 dòng Log::info được thêm ngày 2024-10-10 (commit 4eb951d0dd, '[asp trial] fix bug') — log gỡ lỗi bị bỏ quên trong nhánh production; PR 9507 nêu ở mô tả ticket KHÔNG có trên release: file trên origin/release_step_20260805 vẫn y hệt bản lỗi (không có chunk) ⇒ bug vẫn còn, phải fix lại

■ TỰ REVIEW (AI)
Diff chỉ đụng đúng đoạn dựng danh sách bot trong ajaxAffMoneyV2. Logic lọc bot giữ nguyên từng ký tự (điều kiện hợp đồng, bot dùng thử, bot cũ); biến $listBot vẫn là mảng PHP nên JSON trả về cho ô chọn bot giữ đúng kiểu mảng như trước. Thêm orderBy('id') là bắt buộc để chunk chia khối ổn định — thứ tự này trùng thứ tự thực tế trước đây (quét theo index admin_id trả về theo khoá chính) nên ô chọn bot không đổi thứ tự. Bỏ Log::info không ảnh hưởng logic (facade Log vẫn dùng 45 chỗ khác trong file nên import vẫn hợp lệ). Cách verify cho tester: mở màn tiền thưởng ASP bằng tài khoản cộng tác viên có nhiều bot, tab tình trạng chốt hợp đồng phải load được (không lỗi 500/trắng màn) và ô chọn bot hiển thị ĐỦ danh sách bot đủ điều kiện như trước.
 • Rủi ro / lưu ý khi test:
   - Chưa chạy được trên dev (DB không kết nối được) nên chỉ verify ở mức lint + đọc code; cần tester xác nhận ô chọn bot vẫn đủ bot trên tài khoản thật
   - Truy vấn hợp đồng vẫn chạy 1 lần/bot (N+1) — chunk chỉ chặn bùng RAM, KHÔNG giảm số truy vấn; nếu tài khoản quá nhiều bot vẫn có thể chậm/timeout. Cố ý giữ nguyên để fix tối giản đúng phạm vi ticket
   - Chỗ y hệt ở affBotDetailV2 vẫn còn nguy cơ (xem yokoten)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_34055 (nhánh gốc release_step_20260805, commit 2f2a40d022, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 2 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=cc1929ff-9b66-4b2a-9895-3ac0e573dd5f
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=34055
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #133253 — AI LME Fix bug — 2026-08-27:**

```
(Trùng nguyên văn Journal #133252 — hệ thống AI auto-fixbug post 2 lần.)
```

**Journal #137187 — Kieu Son Tung — 2026-09-19:**

```
branch release: release_step_20260827
```
