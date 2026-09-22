# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #35363 bởi `/new-task` (2026-09-18). Metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35363 — [Friend info] Xóa friend info type date chưa xóa event_step_time` |
| Module / Màn hình | Friend Information (FA-015) — 友だち情報管理 `/basic/friend-information` (xóa 1 mục / xóa nhiều mục / xóa folder) + API mobile xóa trường/thư mục; liên quan Reminder Delivery (FA-022) — job nhắc theo mốc ngày |

## Mô tả bug (bản dịch tiếng Việt)

_(Description Redmine trống — ticket loại "Bug tự detect". Nội dung bug chỉ có ở tiêu đề + journal AI auto-fixbug, xem file 03.)_

Tiêu đề: Xóa trường friend info kiểu ngày (年月日) nhưng chưa xóa `event_step_time` (lịch gửi nhắc theo mốc ngày).

## Steps to reproduce

## Expected result

## Actual result

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

_(Redmine không có attachment.)_

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Fix do **AI auto-fixbug** thực hiện, verify mới ở mức **lint** — chưa chạy được trên DB dev (stack dev tắt), chưa có bằng chứng số bản ghi bị xóa thực tế.
- **Recover data**: dữ liệu tồn đọng từ các trường đã xóa TRƯỚC fix vẫn nằm trong `event_step`/`event_step_time` → job vẫn gửi khi tới mốc; cần chạy dọn 1 lần trên production (SELECT đếm trước + backup 2 bảng).
- Branch: `sns-line: ai_fixbug_35363` (gốc `release_step_20260805`, commit `2a337fc303`).

## Journal / note từ Redmine (nguyên văn)

**Journal #130711 — AI LME Fix bug — 2026-08-20:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
(Toàn văn mục 1–6 + TỰ REVIEW + BRANCH đã tách sang 03-dev-impact.md)

■ 5. RECOVER DATA
   ⚠ CÓ — Fix chỉ chặn phát sinh mới. Dữ liệu tồn đọng từ các trường thông tin đã bị xóa TRƯỚC khi có fix vẫn nằm trong event_step/event_step_time và job vẫn sẽ gửi tin khi tới mốc. Cần chạy dọn 1 lần trên production: tìm event_step type=3 có friend_info_id không bắt đầu bằng d_ và không còn tồn tại trong friend_information_setting, xóa event_step_time thuộc các bản ghi đó rồi xóa chính event_step. Nên chạy câu lệnh SELECT đếm trước để DEV/PM duyệt số lượng, và backup 2 bảng trước khi xóa. (phạm vi: 2 bảng event_step (type=3) + event_step_time, phạm vi toàn hệ thống (mọi bot đã từng xóa trường thông tin kiểu ngày))

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Helpers/functions.php: No syntax errors detected; php -l app/Http/Controllers/Basic/FriendInformationController.php: No syntax errors detected; php -l app/Http/Controllers/Api/Mobile/FriendInfoMobileController.php: No syntax errors detected; Không viết unit test: hàm mới thuần thao tác DB (delete theo quan hệ), không phải logic tính toán nên không tách test được nếu không hit DB
   Bằng chứng: Chưa kiểm chứng được trên DB dev: kết nối host.docker.internal:3306 báo Connection refused (stack dev đang tắt); Đối chiếu spec /workspace/share/spec/spec-features/admin/friend-info/feature-spec.md BR-07: trường kiểu ngày sinh event_step type=3 + event_step_time; spec không định nghĩa bước dọn khi xóa trường; Luồng lưu (saveSettingInfoFriend) đã có tiền lệ dọn: xóa event_step_time theo danh sách event_step_id rồi xóa event_step thừa - fix áp dụng đúng cách dọn này cho luồng xóa

» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=35363
```
