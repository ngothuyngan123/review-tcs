# 01 — Bug Task từ khách hàng

> Auto-filled `2026-09-12` by `/new-task 40153` (Redmine REST API).
> ⚠️ Ticket này là **SpecImprove (thay đổi spec / tính năng mới)**, KHÔNG phải bug report. Không có Steps/Expected/Actual.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40153 — [Onboarding trải nghiệm]Sau khi trải nghiệm/đang trải nghiệm mà user close/nhảy trang khác thì mình đều xóa data init` |
| Module / Màn hình | `<Redmine không ghi category>` — suy từ tiêu đề: **màn 体験 (trải nghiệm) trong wizard thêm bot** (Onboarding). Studio ghi `feature = bot-add`, màn `体験 SCR-45→50 (wizard thêm bot, bước 6)`. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine vốn đã là tiếng Việt — chép nguyên văn, không diễn giải. -->

> Sau khi trải nghiệm/đang trải nghiệm mà user close/nhảy trang khác thì mình đều xóa data init

⚠️ Đây là **toàn bộ** nội dung description của Redmine #40153 (93 ký tự). Ticket **không có** section "Tái hiện bug", **không có** section "Đánh giá ảnh hưởng phía dev", **không có** "Link TCs", **không có** attachment, **không có** journal nào kèm note.

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — để trống. -->

## Expected result

<!-- Redmine không có — để trống. Yêu cầu hành vi mong đợi được Dev/AI kê chi tiết ở 17 requirement trong `03-dev-impact.md` mục 5 (nguồn: Studio). -->

## Actual result

<!-- Redmine không có — để trống. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40153 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Đây không phải bug tái hiện được** — ticket là **SpecImprove** yêu cầu thay đổi hành vi: rời màn 体験 (đóng tab / nhảy trang) ⇒ **xóa data init** đã seed cho bot đó. TCs phải tập trung verify **hành vi mới + phạm vi xóa + regression vùng không được chạm**, không phải verify "fix bug".
- ⚠️ **Redmine THIẾU section "Đánh giá ảnh hưởng phía dev"** → `03-dev-impact.md` được fill từ **MCP LME TEST STUDIO task #284** (tab Thông tin), KHÔNG phải từ Redmine. Leader cần xác nhận với Dev trước khi dùng làm chuẩn coverage.
- `Commit Date` (custom field Redmine): **2026-09-14**.
- Branch implement: `ai-feature-40153` (repo `sns-line`). Toàn bộ implement ở **web (sns-line)**; `linect-service` không liên quan (Laravel Job thay Spring Boot).
- Môi trường: Studio đã chạy TCs **chỉ ở `local`** (3 run, 60/68 TC auto). Chưa chạy dev / staging / **production** → ⚠️ **RULE-08** (media · file QR/ảnh · job nền · gỡ rich menu qua LINE API) **không kết luận được từ local**.
- Trạng thái Redmine: `New` · Author/Assignee: `Ngọc Ánh` · Created `2026-08-25` · Updated `2026-09-11`.

## Dữ liệu định danh ca lỗi

<!-- Ticket không có ca lỗi cụ thể (không phải bug report) — bỏ section. -->

## Journal / note từ Redmine (nguyên văn)

<!--
Redmine #40153 có 2 journal nhưng đều KHÔNG có notes (chỉ đổi field):
- #135428 (2026-09-09, Ngọc Ánh): set custom field "Commit Date" = 2026-09-14
- #136019 (2026-09-11, AI Auto test Lme): đổi assignee 89 -> 155
→ Không có journal nào có giá trị điều tra.
-->
