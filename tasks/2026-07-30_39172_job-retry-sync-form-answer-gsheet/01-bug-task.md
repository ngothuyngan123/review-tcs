# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39172 — [JOB] Job retry sync form answer lên google sheet nếu chạy cho các bản ghi cũ chưa có đánh dấu id retry bị lỗi treo không update được status hoàn thành khi retry xong` |
| Redmine URL | https://redmine.watermelon.vn/issues/39172 |
| Auto-filled | `2026-07-30 by /new-task` |
| Ngày báo cáo | `2026-07-30` |
| Khách hàng / PM báo | `Thanh Duy Nguyen` (author Redmine, cũng là assignee) |
| Module / Màn hình | `Job nền — retry sync Form Answer lên Google Sheet` (không có category Redmine — suy từ subject) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester xác nhận>` (là **job nền**; theo Catalog D job chạy khác nhau dev/staging/**production** — RULE-08) |

> Tracker Redmine: **Bug tự detect** (auto-detected) · Status: **New** · Parent: **#33291** · Assigned to: **Thanh Duy Nguyen**.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description (phần intro trước "1. Nguyên nhân" — phần dev impact đã tách sang 03-dev-impact.md). KHÔNG diễn giải lại. -->

Có 1 case formAnswerResult không có result_error_google_id, nên ko update lại kết quả sync vào resultErrorGoogle.
Cần sửa lại khi set status STATUS_NEW của job retry thì cần update lại cả result_error_google_id vào.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- ⚠️ Redmine KHÔNG có section "Tái hiện bug" chính thức (bug JOB tự detect). Ngữ cảnh tái hiện suy từ mô tả + §4.3 đánh giá ảnh hưởng (file 03) — tester xác nhận lại. -->

1. Có bản ghi `form_answer_result` **cũ** với `result_error_google_id = 0/null` (back-link trống) bị lỗi sync Google Sheet.
2. Job retry chạy → set status bản ghi về `STATUS_NEW` (nhưng **không** set lại `result_error_google_id`).
3. Retry sync xong → success path không đóng được `ResultErrorGoogle` (check `result_error_google_id > 0` fail).
4. Quan sát: `ResultErrorGoogle` **treo mãi ở `STATUS_RUNNING`** (job retry chỉ pick `STATUS_NEW` nên không xử lý lại).

## Expected result

- Sau khi retry sync xong, `ResultErrorGoogle` chuyển `RUNNING → SUCCESS`, **không treo** (suy luận từ mô tả — Redmine không ghi expected riêng).

## Actual result

- `ResultErrorGoogle` **treo vô hạn ở `STATUS_RUNNING`**, status hoàn thành không được update.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue **không có attachment**.

## Ghi chú thêm của Leader

⚠️ **Bug JOB tự detect — không có bước tái hiện chính thức trong Redmine.** Root cause đã được Dev confirm chi tiết (file `03-dev-impact.md`, có cả code reference `HandleFormAnswerSyncGoogleSheetTask` dòng 839-840). **TCs nên tập trung: (1) reproduce bản ghi cũ `result_error_google_id = 0/null` → retry → verify `ResultErrorGoogle` RUNNING→SUCCESS; (2) nhánh retry DELETE (`status_sync_deleted = WAIT_RETRY`); (3) race đa luồng (set RUNNING trước khi reset NEW).**

- Có **link Test Studio** ở journal (không phải Google Sheet Link TCs): https://lme-test-studio.melonglobal.net/?screen=task-wizard&task=39&wtab=testcase — QA xác nhận đây có phải nguồn TC không; nếu có TC trên Sheet thì cung cấp URL + Row range để `/new-task` fetch vào file 04.
- Fix chạm **job nền + Google Sheet sync + concurrency (race)** → liên quan quan điểm `JOB-001`, `INTG-SHEET-001`, `CONC-001`, `STATE-001` khi review.
