# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #42274 KHÔNG có section "Đánh giá ảnh hưởng phía dev".** Ticket này là **re-test / audit chủ động**: AI tự rà soát bug lịch sử + review code + business spec rồi đính kèm kết quả qua `index.html` + `test-cases.csv`, KHÔNG phải Dev nộp đánh giá ảnh hưởng sau khi fix. Chưa có Dev nào được assign (`Assignee: -`), chưa có commit/PR, chưa có gì được fix — toàn bộ 14 đầu việc trong audit đều ở trạng thái **"Chưa sửa"**.
>
> Theo **RULE-11** (chỉ ticket Closed/Resolved/Fix done/Released mới là bằng chứng hợp lệ), nội dung audit ở đây **KHÔNG được coi là "Dev tự kê" impact** — nó là **candidate risk do AI tự phân tích**, chưa qua Dev xác nhận. Mục 1–4 dưới đây để trống đúng chuẩn template; nội dung audit được tách riêng ở **Phụ lục** cuối file để không bịa đặt thành Dev assessment.
>
> `/write-tc` và `/review-tc` chạy trên folder này cần tự quyết định cách dùng Phụ lục (gợi ý: dùng để đối chiếu/bổ sung ở BƯỚC 3a–5a, KHÔNG dùng làm nguồn "dev-impact" ở BƯỚC 2a).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Assignee trống trên Redmine>` |
| Commit / Pull Request | `<chưa có — chưa có bản fix nào>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `<không áp dụng — không có Dev assessment>` |
| Auto-filled | `2026-10-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

<!-- Không tick được cho ticket này — Redmine không có section "Đánh giá ảnh hưởng" để verify. -->

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp. Ticket #42274 không có section "Đánh giá ảnh hưởng phía dev". Xem Phụ lục cho candidate root cause do AI tự audit (chưa Dev xác nhận).>`

## 2. Cách fix

`<Input thiếu — chưa có bản fix. Toàn bộ 14 đầu việc trong Phụ lục đang ở trạng thái "Chưa sửa".>`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

`<Input thiếu — không áp dụng vì chưa có fix nào được thực hiện.>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

`<Input thiếu theo nghĩa "Dev tự kê". Xem bảng "Bằng chứng source cần sửa" theo từng FIX-ID ở Phụ lục — đây là file/function AI tự đọc source xác định, chưa qua Dev xác nhận.>`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | | | Direct / Indirect | `<Input thiếu>` |

### 4.2. List data bị update khi fix bug

`<Input thiếu — chưa có bản fix nên chưa có data migration/update nào được Dev kê.>`

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | | CREATE / UPDATE / DELETE / MIGRATE | `<Input thiếu>` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

`<Input thiếu theo nghĩa "Dev tự kê". 14 đầu việc FIX-01–FIX-14 ở Phụ lục là candidate tính năng/luồng rủi ro do AI tự audit — dùng tham khảo, KHÔNG thay cho mục này.>`

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | | F1, D1 | `<Input thiếu>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — **N/A, không có fix**
- [ ] Mục 2 (cách fix) có thể trace về code — **N/A**
- [ ] Mục 3 đã check đủ caller — **N/A**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **N/A, dùng Phụ lục thay thế**
- [ ] Mục 4.2 không thiếu data — **N/A**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — Leader đối chiếu Phụ lục `FIX-01`–`FIX-14` + `VERIFY-01`–`05`
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — **cần Leader assign Dev trước, ticket hiện chưa có Assignee**

---

## Phụ lục — Audit nội bộ AI (đính kèm `index.html`, KHÔNG phải Dev assessment)

> Nguồn: attachment `index.html` của Redmine #42274 — báo cáo "LME · Kết quả rà soát và danh sách fix Calendar" (Calendar Salon & Calendar Booking), snapshot 24/09/2026, cập nhật 29/09/2026 15:22. 3 nhánh phân tích: (1) bug lịch sử KH 1.01–1.15, (2) review code trực tiếp 2.01–2.13, (3) business/spec 2.14–2.26 → gộp thành 14 đầu việc `FIX-01`–`FIX-14` (từ 41 mục phân tích) + 5 nhóm `VERIFY-01`–`05` (chưa mở thành bug) + `DOC-01` (sửa tài liệu). Report tự ghi: *"Đây là danh sách đầu việc, không phải 14 bug độc lập đã tái hiện E2E... Tất cả vẫn ở trạng thái chưa sửa."* và *"Chưa xác nhận SHA đang deploy production."*
>
> Dùng bảng này để **đối chiếu khi viết/review TC** (BƯỚC 3a/5a của `/write-tc`, `/review-tc`), **KHÔNG** dùng làm nguồn "dev-impact" ở BƯỚC 2a vì chưa qua Dev xác nhận (RULE-11).

### Bảng tổng hợp FIX-01 – FIX-14

| FIX-ID | Mức | Trạng thái | Phạm vi bug trên source | Nguồn (nhánh · mã) | TC liên quan (`04-tc-list.md`) |
|---|---|---|---|---|---|
| FIX-01 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon**: bảo vệ quyền sở hữu và trạng thái khi sửa/xóa booking — đường sửa/xóa nhận `bookingId` nhưng chưa ràng buộc đủ user/calendar/payment status; cleanup đến trễ có thể xóa booking hợp lệ | Lịch sử 1.06·H1-39566 · Code 2.01·SALON-01 · Spec 2.14·BIZ-01, 2.22·BIZ-09 | TC-A01 · TC-A02 · H1-39566-T1 · H1-39566-T2 · BIZ-T01 |
| FIX-02 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon**: server phải tự quyết giá/trạng thái duyệt/paid — code đang dùng `amount`, `approve_type`, cờ payment từ client, thiếu đối soát server | Code 2.02·SALON-02 · Spec 2.20·BIZ-07, 2.14·BIZ-01 | TC-A03 · TC-A04 · BIZ-T11 |
| FIX-03 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon**: giữ đúng sức chứa khi nhiều khách đặt đồng thời — chỉ loại trùng cùng giây + cùng `start_time`, không bảo vệ các khoảng thời gian chồng nhau khác | Lịch sử 1.01·H1-38280 · Code 2.03·SALON-03 · Spec 2.19·BIZ-06 | TC-A05 · H1-38280-T2 · BIZ-T10 |
| FIX-04 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Lesson**: giữ đúng sức chứa ở luồng miễn phí tự duyệt — 2 request có thể insert ở 2 giây khác nhau, không bị cơ chế loại trùng chặn | Lịch sử 1.01·H1-38280 · Code 2.10·BKG-03 · Spec 2.15·BIZ-02 | TC-A17 · H1-38280-T1 |
| FIX-05 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon & Lesson**: gửi lại yêu cầu hủy không được tự rút hủy — payload chỉ có `id`, API tự đảo hành động theo status hiện tại, gửi lại có thể đảo ý định ban đầu | Code 2.04·SALON-04, 2.08·BKG-01 · Spec 2.17·BIZ-04 | TC-A06 · BIZ-T07 |
| FIX-06 | Trung bình | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon**: rút hủy phải khôi phục đúng booking do admin tạo — nhánh khôi phục đọc `admin_id` trong khi admin tạo ghi `booking_by`, status 2 có thể khôi phục sai thành 1 | Code 2.04·SALON-04 · Spec 2.17·BIZ-04 | TC-A07 |
| FIX-07 | Trung bình | Chưa sửa — **có proof PHP cô lập** | **Salon**: staff phải phủ đủ giờ bắt đầu/kết thúc booking qua đêm — helper chọn staff qua đêm kiểm giờ kết thúc nhưng thiếu kiểm staff đã vào ca tại giờ bắt đầu booking | Lịch sử 1.02·H1-40128 · Code 2.05·SALON-05 · Spec 2.18·BIZ-05, 2.21·BIZ-08 | TC-A08 · TC-A09 · BIZ-T08 |
| FIX-08 | Trung bình | Chưa sửa — **có proof PHP cô lập** | **Salon**: sửa/import ca không được bỏ bảo vệ booking qua đêm — helper đếm booking phủ ca so sai giờ/ngày, booking qua đêm bị đếm lệch ca | Lịch sử 1.03·H1-38520 · Code 2.06·SALON-06 · Spec 2.21·BIZ-08, 2.22·BIZ-09 | TC-A10 · TC-A11 · BIZ-T13 · BIZ-T16 |
| FIX-09 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon**: đồng bộ Google phải giữ & chạy lại phần bị lỗi — event lỗi vẫn tiến mốc đồng bộ; event nhiều ngày ghi dở lại bị coi hoàn tất | Lịch sử 1.05·H1-41035 · Code 2.07·SALON-07 · Spec 2.23·BIZ-10 | TC-A12 · TC-A13 · H1-41035-T1 · H1-41035-T2 · BIZ-T17 · BIZ-T18 |
| FIX-10 | Cao | Chưa sửa — **có proof PHP cô lập** | **Lesson**: rút hủy phải cập nhật counter và bảo vệ slot còn booking — nhánh rút hủy return trước khi cập nhật counter/history/sync; guard xóa slot tin counter cũ | Code 2.08·BKG-01 · Spec 2.17·BIZ-04, 2.22·BIZ-09 | TC-A14 · TC-A15 · BIZ-T06 · BIZ-T15 |
| FIX-11 | Trung bình | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Salon/Lesson**: không gửi reminder của booking đã hủy/xóa — hủy chỉ dọn event chưa xử lý; reminder đã vào queue không được worker đối chiếu lại trạng thái booking trước gửi | Lịch sử 1.14·H1-41383 · Code 2.09·BKG-02 · Spec 2.24·BIZ-11 | TC-A16 · H1-41383-T1 · H1-41383-T2 · BIZ-T19 |
| FIX-12 | Cao | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Lesson**: cùng booking Stripe chỉ được thu tiền một lần — 2 lượt duyệt đọc trạng thái trước khi gọi gateway, không có khóa xử lý / mã chống thu trùng | Code 2.11·BKG-04 · Spec 2.20·BIZ-07, 2.15·BIZ-02 | TC-A18 · TC-A19 · BIZ-T12 |
| FIX-13 | Trung bình | Chưa sửa — rủi ro có bằng chứng source, cần test tích hợp | **Monitor**: không dừng hoặc bỏ sót booking cần kiểm — vòng kiểm dừng sau exception, kẹt ở khoảng trống ID, hoặc bỏ record đã quét rồi mới được duyệt | Code 2.12·BKG-05 · Spec 2.26·BIZ-13 | TC-A20 · BIZ-T22 |
| FIX-14 | Cao | Chưa sửa — **có proof PHP cô lập** | **Lesson**: đổi LINE sang guest không được ghi đè waitlist người khác — UI giữ `lineUserId` cũ sau đổi mode; service tìm/dùng lại waitlist theo ID đó ngay khi đang tạo guest | Lịch sử 1.10·H1-41329, 1.11·H1-36729 · Code 2.13·BKG-06 · Spec 2.16·BIZ-03 | TC-A21 · TC-A22 · H1-41329-T2 · BIZ-T04 · BIZ-T05 |

**Ghi chú gộp quan trọng** (nguyên văn từ report, để tránh hiểu nhầm khi viết TC):
- Không gộp chỉ vì cùng triệu chứng: Salon và Lesson giữ suất ở source khác nhau nên tách riêng `FIX-03` (Salon) và `FIX-04` (Lesson).
- Một mục phân tích có thể tách thành nhiều FIX khác nhau: `SALON-04` tách `FIX-05` và `FIX-06`; `BKG-01` nối `FIX-05` và `FIX-10`.
- `FIX-05`/`FIX-06`/`FIX-10` cùng chạm luồng hủy/rút hủy — nên giao cùng người/cùng PR nhưng giữ 3 bộ tiêu chí test riêng, không đóng việc này chỉ vì việc kia pass.
- Mọi `FIX-01`–`FIX-14` đều kèm dòng *"Chưa chạy HTTP/DB/gateway toàn luồng; cần đối chiếu SHA deploy trước khi áp dụng."* → QA phải tự chạy E2E, không coi "có proof PHP cô lập" là đã pass.

### Nhóm chưa mở thành bug — cần xác minh / chốt business / khóa phạm vi trước

| Mã | Trạng thái | Việc cần làm | Khi nào thành FIX mới | Nguồn |
|---|---|---|---|---|
| VERIFY-01 | Cần xác minh đường thao tác | Xác minh response cũ/lỗi tải slot Salon: UI có tạo 2 request chồng nhau khi loading? Response sai thứ tự / HTTP 500 trên Safari/LINE iOS? | Chỉ mở FIX khi tái hiện được ảnh hưởng UI hoặc thống nhất expected xử lý lỗi | 1.08·H1-40378 · TC H1-40378-T1, H1-40378-T2 |
| VERIFY-02 | Cần test lại | Retest các bug lịch sử chưa xác nhận còn trên source: H1-40128, H1-38520, H1-40910, H1-40050, H1-41090, H1-41329, H1-36729 | Nếu fail → nối vào FIX hiện có nếu trùng nguyên nhân; chỉ mở FIX mới nếu nguyên nhân/đường sửa khác | 1.02/1.03/1.04/1.07/1.09/1.10/1.11 · TC tương ứng H1-*-T1 |
| VERIFY-03 | Cần quyết định business | Chốt các policy còn mở trước khi đánh pass/fail: pending giữ chỗ, quyền admin vượt capacity, buffer cuối ca, gán staff, giá cũ/mới, deadline, xóa dữ liệu liên quan, doAction | Không tạo bug chỉ vì policy chưa chốt; sau khi chốt, test nhánh expected đã chọn | 2.15/2.16/2.18/2.19/2.20/2.21/2.22/2.24·BIZ-* · TC BIZ-T02, T03, T09, T10, T11, T14, T20 |
| VERIFY-04 | Cần khóa phạm vi | Xác nhận phạm vi Calendar Booking legacy: module, route/job còn chạy, policy chuyển hướng | Không dùng review Salon/Lesson để kết luận legacy hết bug; chỉ thêm FIX khi có bằng chứng cụ thể | 2.25·BIZ-12 · TC BIZ-T21 |
| VERIFY-05 | Chưa coi là bug source | Các ca đang được giải thích bằng setting/lịch sử cấu hình: provider, unlimited/fixed limit, setting hiệu lực tại lúc gửi reminder | Không mở FIX từ ticket cũ nếu hành vi đúng setting; chỉ mở khi test chứng minh sai rule đã thống nhất | 1.12·H1-38314, 1.13·H1-40108, 1.15·H1-37751 · TC tương ứng |
| DOC-01 | Sửa tài liệu | Cập nhật mapping route khách Salon trong spec (LIFF → `Mobile\CalendarSalonController`, ghi đúng version source) | Đầu việc tài liệu, không tạo bug source bên cạnh FIX-01/02 | 2.14·BIZ-01 · TC BIZ-T01 |

### Giới hạn đã công bố của report (đọc trước khi dùng)

- "209 là số báo cáo, không phải 209 lỗi code đã xác nhận. 36 có evidence nguồn trực tiếp; 173 còn dựa tracker hiện tại và lịch sử tracker truy cập được."
- "4 lỗi có proof PHP cô lập; chưa chạy application E2E. Các ca ở ba nhánh có thể liên quan cùng một cơ chế lỗi, không cộng thành tổng số bug độc lập."
- Mức độ nghiêm trọng (Cao/Trung bình/Thấp/Chưa xếp lỗi) là đánh giá định tính theo đường dùng/code, **chưa có số liệu tần suất sử dụng thực tế**; tách biệt với mức chắc chắn của bằng chứng.
