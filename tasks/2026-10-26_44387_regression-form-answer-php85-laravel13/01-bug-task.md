# 01 — Bug Task từ khách hàng

> ⚠️ Ticket này **không phải bug report** — đây là subtask QA tách riêng phạm vi **Form Answer** từ task nâng cấp lớn #43845 (Nâng cấp module PHP Web lên PHP 8.5 + Laravel 13). Mục tiêu là **regression test**, không phải verify fix 1 bug cụ thể. File này được điền bám khung template gần nhất có thể; các section không áp dụng (Steps/Expected/Actual to reproduce theo nghĩa bug) được ghi rõ "không áp dụng".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44387 — [#43845] Regression tính năng Form Answer trên PHP 8.5 / Laravel 13` |
| Module / Màn hình | Form Answer (toàn bộ): danh sách form, tạo/sửa form, quản lý trang/rẽ nhánh, thiết kế, tin nhắn/action, cài đặt khác, CSS/JS, preview, thư mục, xóa/khôi phục; trang trả lời phía khách (các phiên bản còn hỗ trợ); kết quả trả lời, chi tiết câu trả lời, tính điểm/chẩn đoán, remind, xuất CSV; liên kết Google Spreadsheet + job tạo sheet/đồng bộ; cập nhật thông tin bạn bè + lịch sử + action phát sinh từ câu trả lời; API app + điểm tích hợp liên quan trực tiếp Form Answer |

## Mô tả bug (bản dịch tiếng Việt)

**Không áp dụng theo nghĩa "bug"** — đây là task QA con tách từ #43845 (Nâng cấp module PHP Web/sns-line từ Laravel 5.5/PHP 7.2 lên Laravel 13/PHP 8.5 trong 1 lần release, không đổi spec, logic bên trong được phép viết lại đơn giản hơn).

Nội dung ticket #44387 nguyên văn (đã dịch/giữ cấu trúc gốc, ticket viết sẵn bằng tiếng Việt):

- **Task nguồn và mục tiêu**: Task cha/nguồn #43845. #44387 là subtask QA tách riêng phạm vi Form Answer từ #43845, không phải yêu cầu phát triển tính năng mới. Mục tiêu: kiểm tra tính năng Form Answer trên bản nâng cấp, bảo đảm hành vi và kết quả phía người dùng theo yêu cầu đã chốt tại #43845.
- **Nhánh và mốc đối chiếu**: Nhánh cần test `ai_studio_implement_43845`. Dùng bản bàn giao mới nhất của #43845; ghi lại commit thực tế khi chạy test. Mốc đối chiếu: nhánh/commit production base được ghi trong bản bàn giao tương ứng của #43845. **Kế thừa các thay đổi spec, ngoại lệ và khác biệt đã được chấp nhận tại #43845 — không mặc định mọi kết quả khác production đều là bug.**
- **Dữ liệu kế thừa từ Test Studio**: Studio task nguồn `task_id=507`, ticket #43845. Đọc `task_get_context(task_id=507)` để lấy requirement/bàn giao/quyết định liên quan. Đọc toàn bộ testcase của `task_id=507`, chọn TC thuộc Form Answer làm input cho subtask này. Giữ tham chiếu TC nguồn dạng `#43845 / NEW-xxx`. **Không tự sửa/xóa TC của task nguồn.** Kết quả test ở task nguồn chỉ tham khảo — subtask này ghi nhận kết quả chạy trên commit/môi trường thực tế của mình.

## Steps to reproduce

Không áp dụng (không phải bug cụ thể) — xem mục "Dữ liệu định danh ca lỗi" bên dưới cho các điểm nóng Dev đã lưu ý khi test Form Answer.

## Expected result

Hành vi và kết quả phía người dùng của Form Answer trên bản PHP 8.5/Laravel 13 **giống bản production** (trừ các khác biệt/ngoại lệ đã được chấp nhận tại #43845 — xem `03-dev-impact.md`).

## Actual result

Chưa test — kết quả sẽ ghi vào `04-tc-list.md` / `05-review-report.md` khi chạy TC trên môi trường thực tế của subtask này.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment ở #44387. Task cha #43845 có 2 attachment (tài liệu, không phải ảnh/log ca lỗi):
- `upgrade-php85-laravel13-report.html` — https://redmine.melonglobal.net/attachments/download/36112/upgrade-php85-laravel13-report.html (báo cáo scan PHP8.5/Laravel13, mã P1–P9/L1–L12)
- `chia-task-nang-cap-lme.html` — https://redmine.melonglobal.net/attachments/download/36114/chia-task-nang-cap-lme.html (kế hoạch chia 21 task con + 22 điểm scan thiếu G-1…G-22)

## Ghi chú thêm của Leader

- ⚠️ **Task nâng version PHP/Laravel** — theo CLAUDE.md, khi review/viết TC cho task này phải đọc thêm [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md) làm trục quét bổ sung (điểm nóng PHP8 A1–A6, lib nâng version LINE SDK v12/Intervention v3/Stripe/UnivaPay/Mail/WebPush/Google/CSV/Collective, auth/mã hoá, 3 surface web/app/LINE user-LIFF).
- Branch test: `ai_studio_implement_43845`. Release ref: `release_step_20260930_v2`.
- Dev Studio (handoff #16, bàn giao mới nhất tại thời điểm fetch 2026-10-26): chỉ bổ sung tài liệu lỗi có sẵn PB-T25-6 (chat nhóm trống do checkFriend — **có sẵn ở production**, không báo lại); code giống bàn giao #15.
- Bàn giao #15 (gộp base `303a131b9c`): TrustProxies thêm IP `142.91.106.63` — ảnh hưởng IP khách/https/URL tuyệt đối khi đi qua proxy tin cậy; request **không** qua proxy tin cậy phải bỏ qua header `X-Forwarded-*`.
- Dev impact tổng (toàn #43845, KHÔNG riêng Form Answer) xem đầy đủ ở `03-dev-impact.md` mục 1 — lấy từ Studio `task_id=507` field `dev_impact` + `info_pack.dev`.
- **TC Form Answer của task này lấy từ MCP LME TEST STUDIO `task_id=507` (ticket #43845)**, lọc theo screen/spec_ids liên quan Form Answer — xem `04-tc-list.md`. TC là **read-only**, tham chiếu dạng `#43845 / NEW-xxx`.
- Input thiếu: ticket #44387 không có section "Đánh giá ảnh hưởng phía dev" theo format chuẩn (4 mục Nguyên nhân/Cách fix/Caller/Đánh giá ảnh hưởng) — vì đây không phải 1 bug fix đơn lẻ mà là 1 subtask quét lại 1 tính năng trong 1 cuộc nâng cấp framework lớn (21 task con). `03-dev-impact.md` được tổng hợp từ dữ liệu Studio `task_id=507` (`requirements` + `spec_delta.files` lọc theo Form Answer + `dev_impact` chung), KHÔNG phải Dev tự điền theo format 4 mục — Leader/Tester cần verify lại.

## Dữ liệu định danh ca lỗi

Không áp dụng — ticket không có 1 ca lỗi cụ thể (nhánh test toàn bộ tính năng Form Answer trên bản nâng cấp).

## Journal / note từ Redmine (nguyên văn)

Không có journal (0 journal có notes) trên #44387 tại thời điểm fetch (2026-10-26).
