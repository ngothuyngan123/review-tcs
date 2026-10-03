# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41772 bởi `/new-task` (2026-09-30). Metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41772 — [30-09-2026][31351][Lesson] Lịch (calendar) đặt lịch lesson tự động chuyển về vô hiệu ngay sau khi bật lại, khiến khách không thể sử dụng chức năng đặt lịch lesson.` |
| Module / Màn hình | Đặt lịch bài học / レッスン予約 (FA-019, calendar_management) — màn danh sách lịch (`/basic/calendar-management`), nút bật/tắt 有効/無効 |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: xx.ayms2.xx@gmail.com
Bot Name: LIZUM HOME

Về quyền hỗ trợ của Elme, tôi đã thay đổi quyền thao tác, hiện đang ở trạng thái có quyền đặt lịch lesson.

Hiện tại tôi đã đăng ký 2 lịch (calendar).
Để cập nhật•thêm khóa học (course) vào một trong hai lịch đó, tôi đã tạm thời chuyển cả hai lịch sang trạng thái vô hiệu.

Sau khi cập nhật•thêm khóa học, khi thử bật lại lịch (chuyển sang hữu hiệu), nó chỉ hữu hiệu trong tích tắc rồi tự động chuyển ngay về vô hiệu.

Hiện đang trong tình trạng không thể sử dụng chức năng đặt lịch lesson.

Chức năng: Đang sử dụng chức năng đặt lịch lesson của Elme, nhưng không thể bật lại lịch đã từng bị vô hiệu hóa. (エルメのレッスン予約機能を使っているが、一度無効にしたものを有効にできなくなった。)
Thời điểm phản hồi: 2026/09/30 13:39:00

Nội dung từ Slack (OEM, nguyên văn JP):
> エルメのサポート権限ですが、操作権限を変更しており、レッスン予約の権限はある状態です。
> 現在カレンダーを2つ登録しています。
> うち一つにコースを更新•追加するため、一度二つともカレンダーを無効に変更しました。
> コースの更新•追加後に、再度カレンダーを有効にしようとすると、一瞬有効になったあと、自動ですぐに無効に切り替わります。
> レッスン予約機能が使えない状況です。

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" tách riêng — nội dung trên chính là mô tả tái hiện do khách/OEM cung cấp (không có block Steps/Expected/Actual riêng biệt). -->

## Expected result

## Actual result

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue #41772 không có attachment (0). -->

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được theo format Steps/Expected/Actual chuẩn trong Redmine — nhưng root cause đã được Dev confirm rõ qua đánh giá ảnh hưởng (file 03), kèm bằng chứng tái hiện trực tiếp ở mục 6 VERIFY. TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: Production (bot khách OEM 31351, LIZUM HOME).
- Không phải lỗi quyền thao tác (操作権限) như khách suy đoán ban đầu — Dev xác nhận nguyên nhân thực sự là request PARTIAL UPDATE của nút toggle 有効/無効 trượt validate `calendar_name = required`.
- Ticket do "AI bug detect Lme" tạo; fix do "AI LME Fix bug" (auto-fixbug) thực hiện.
- Cả 2 release đang dính bug (theo Dev): `release_staging_20260910` và `release_step_20260930`.
- Bug do xung đột thứ tự merge giữa 2 fix cũ: #41104 (2026-09-18, toggle bỏ gửi `calendar_name`) và #40050 (cherry-pick vào release 2026-09-25, thêm rule `calendar_name = required`) — không phải lỗi của riêng 1 commit.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ>` — Bot Name: LIZUM HOME (user xx.ayms2.xx@gmail.com) |
| Friend | Không áp dụng — bug ở màn quản trị (calendar-management), không liên quan friend cụ thể |
| Đối tượng cấu hình | 2 lịch (calendar) đăng ký cho chức năng đặt lịch lesson — đã tạm chuyển cả 2 sang vô hiệu để sửa course, sau đó bật lại bị lỗi |
| Thời điểm lỗi | 2026/09/30 13:39:00 (thời điểm phản hồi) |
| Đối chứng | Theo Dev: nút toggle 有効/無効 chỉ gửi `enable_use_calendar` → trượt validate `calendar_name = required` → HTTP 400 → cờ không ghi vào DB, JS lật checkbox về trạng thái cũ mà không báo lỗi |

## Journal / note từ Redmine (nguyên văn)

> Nội dung đầy đủ (mục 1 nguyên nhân · 2 cách fix · 3 function đã check · 4 đánh giá ảnh hưởng) đã tách vào `03-dev-impact.md`. Phần dưới đây là phần KHÔNG nằm trong 4 mục của file 03.

**Journal #139397 — AI LME Fix bug — 2026-09-30:**

```
■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/CalendarManagementController.php: No syntax errors detected; node --check public/js/calendar_management/index.js: OK; Bảng đối chiếu validator standalone (Illuminate\Validation 5.5 của repo) trên 7 payload thật: payload toggle CŨ TRƯỢT (validation.required -> 400) / MỚI ĐI QUA; modal tên rỗng + tên 11 ký tự vẫn TRƯỢT như trước; gradle compileJava: N/A (không sửa Java); vendor/bin/phpunit: N/A (fix ở Controller + JS, không thuộc app/Services|app/Helpers)
   Bằng chứng: Tái hiện trực tiếp nguyên nhân: payload nút 有効/無効 chỉ có enable_use_calendar nên trượt rule calendar_name=required -> HTTP 400 (hasStructureFailure) -> cờ không bao giờ ghi vào DB; nhánh error của JS lật checkbox về trạng thái cũ mà không báo gì.; Không phá lớp chặn cũ: 2 ca chặn của #40050/#41104 (tên rỗng, tên 11 ký tự) vẫn TRƯỢT y như trước; guard chặn trùng 管理名 vẫn chạy khi request has(calendar_name).; Truy đúng 2 commit sinh regression: 64fc537f15 (#40050, thêm required) + 15f0110b10 (#41104, toggle bỏ gửi tên). git branch -r --contains 15f0110b10 -> chỉ 2 release branch: release_staging_20260910 + release_step_20260930 => ra production cùng đợt release 2026-09-30, khớp mốc khách báo 30/09 13:39 JST.; Job Java KHÔNG liên quan (kiểm chứng ở tự review v2): entity linect-service CalendarManagement chỉ map id/bot_id/store_name/calendar_name, KHÔNG có cột enable_use_calendar.; CHƯA kiểm: chưa bấm tay end-to-end trên web dev host; QA cần retest theo reproduceSteps + HARD-RELOAD trình duyệt (index.js còn cache theo ?v= cũ, ticket fix không được bump version).

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41772 (nhánh gốc release_step_20260930)  [đã push]

» Thời gian AI xử lý: 10 phút 30 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=4eda7c38-8974-430c-b4e2-17f7274b66e1
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41772
```
