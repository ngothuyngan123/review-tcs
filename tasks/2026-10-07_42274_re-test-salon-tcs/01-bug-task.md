# 01 — Bug Task từ khách hàng

> ⚠️ **Ticket #42274 KHÔNG phải ticket bug đơn lẻ** — đây là ticket **re-test** (QA chủ động rà soát lại tính năng Salon/Lesson theo bộ TC do AI gen sẵn, dựa trên audit bug lịch sử + code + business spec). Không có Steps/Expected/Actual của 1 ca lỗi cụ thể như ticket bug thông thường. Auto-fill từ Redmine `#42274` qua `/new-task`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42274 — [SALON] [Re-test v1] Re-test tính năng salon theo list testcase sẵn có` |
| Module / Màn hình | Calendar Salon & Calendar Booking (Mobile — `CalendarSalonController` / `CalendarController` / `CalendarCourseBookingService` / `CalendarSalonLineBookingService` / Google Calendar sync / event-remind worker / monitor job) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nội dung Redmine gốc đã là tiếng Việt — giữ nguyên văn. -->

Bối cảnh: Tính năng salon nhận nhiều bug từ phía khách hàng nên cần re-test lại xem có phát hiện bug nào hay không để assign team dev fix.

AI đã tiến hành rà soát 1 lượt theo lịch sử bug KH, review trực tiếp code và business spec. Từ đó đưa ra đánh giá các phần có thể phát sinh bug.

Hãy đọc file `index.html` và file `test-cases.csv`.

Nhiệm vụ: Cần re-test theo list testcase mà AI đã gen.

## Steps to reproduce

<!-- Không áp dụng — ticket không mô tả 1 ca lỗi cụ thể để tái hiện. Xem "Dữ liệu định danh ca lỗi" bên dưới cho bộ data mẫu AI đã chuẩn bị theo từng claim. -->

## Expected result

<!-- Không áp dụng ở cấp ticket. Expected cụ thể của từng TC xem `04-tc-list.md` (cột "Kết quả mong đợi" lấy từ `test-cases.csv`). -->

## Actual result

<!-- Chưa có — toàn bộ 65 TC trong `test-cases.csv` đang ở trạng thái "Chưa chạy theo các bước này". Đây là audit chủ động (proactive), không phải báo cáo lỗi KH đã xảy ra. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Khác — 2 file attachment chứa toàn bộ nội dung audit + TC list (xem bên dưới)

Attachments (2) từ Redmine #42274:
- `test-cases.csv` (179021 bytes) — https://redmine.melonglobal.net/attachments/download/31922/test-cases.csv — 65 TC đã gen, nguồn cho `04-tc-list.md`.
- `index.html` (1517421 bytes) — https://redmine.melonglobal.net/attachments/download/31923/index.html — Báo cáo audit đầy đủ "LME · Kết quả rà soát và danh sách fix Calendar" (snapshot 24/09/2026, cập nhật 29/09/2026), 3 nhánh phân tích (bug lịch sử 1.01–1.15 · review code 2.01–2.13 · business/spec 2.14–2.26) gộp thành 14 đầu việc `FIX-01`–`FIX-14` + 5 nhóm `VERIFY-01`–`05` + `DOC-01` chưa mở thành bug. Đã rút gọn phần `FIX-01`–`FIX-14` vào phụ lục của `03-dev-impact.md`.

## Ghi chú thêm của Leader

- ⚠️ Đây là ticket **re-test / audit chủ động**, KHÔNG phải ticket bug 1 ca cụ thể → không có Dev impact assessment chuẩn (xem cảnh báo lớn ở đầu `03-dev-impact.md`).
- Toàn bộ 14 đầu việc `FIX-01`–`FIX-14` trong `index.html` đang ở trạng thái **"Chưa sửa"** — report tự nhận: "Đây là danh sách đầu việc, không phải 14 bug độc lập đã tái hiện E2E... Tất cả vẫn ở trạng thái chưa sửa." → theo **RULE-11**, không có ticket Closed/Resolved/Fix done nào làm bằng chứng — mọi finding ở đây chỉ là **candidate rủi ro do AI tự audit**, cần QA chạy TC để xác nhận trước khi tạo ticket bug riêng giao Dev.
- 4 nhóm có "proof PHP cô lập" (FIX-07, FIX-08, FIX-10, FIX-14) — tức AI đã tự viết test PHP cô lập để chứng minh logic sai, nhưng **chưa chạy HTTP/DB/gateway toàn luồng (E2E)** trên môi trường thật. QA cần retest bằng thao tác thật, không coi proof PHP này là đã pass E2E.
- Report chưa xác nhận SHA code đang audit có khớp với SHA đang deploy production hay không ("Chưa xác nhận SHA đang deploy production") → QA nên đối chiếu môi trường test với source đã audit trước khi kết luận pass/fail.
- 65 TC trong `test-cases.csv` chia theo 3 nhóm nguồn: `H1-*` (21 TC — xuất phát từ bug lịch sử khách hàng), `TC-A*` (22 TC — xuất phát từ review code trực tiếp), `BIZ-T*` (22 TC — xuất phát từ đối chiếu business/spec).
- `test-cases.csv` không gắn mã quan điểm theo 80-quan-điểm chuẩn của [framework/checklist-lme.md](../../framework/checklist-lme.md) — khi review/bổ sung TC (`/review-tc`) cần tự map thêm.
- Không có Dev / Assignee được gán trên ticket Redmine (`Assignee: -`).
