# Review Checklist — Leader dùng khi review TCs

Chạy qua checklist này cho từng lần review. Mỗi mục fail → ghi vào report với [severity](severity-levels.md).

> **Chú ý**: Checklist này là tiêu chí review **tổng quát** (áp dụng mọi dự án). Với dự án LME cụ thể, member **BẮT BUỘC** base thêm [checklist-lme.md](checklist-lme.md) — checklist chuẩn hóa từ sheet "Checklist web / Checklist job / Các tính năng chung" của team.

---

## A. Coverage (đối chiếu với `03-dev-impact.md`)

> File 04 KHÔNG có cột "Map to Impact". Leader/Claude **suy luận** mapping từ Title / Precondition / Steps / Expected của mỗi TC. Title TC phải chứa keyword (tên function / DB / màn hình) để dễ suy luận.

### A.1 Bug root cause
- [ ] Có **≥ 1 TC** verify trực tiếp **root cause đã fix** (Title chứa "reproduce" hoặc mô tả đúng flow KH)
- [ ] TC đó mô phỏng **chính xác** steps reproduce trong `01-bug-task.md`
- [ ] Expected result khớp với spec (sau fix), không chỉ "không lỗi"

### A.2 Function impact (mục 4.1)
- [ ] Mỗi function F1, F2,... đều có **≥ 1 TC** verify (Title TC chứa tên function → suy luận map Fx)
- [ ] Function `Direct` impact: có cả positive + negative + boundary
- [ ] Function `Indirect` impact: có ít nhất regression test

### A.3 Data impact (mục 4.2)
- [ ] Mỗi data D1, D2,... đều có **≥ 1 TC** verify trạng thái data sau thao tác (Title/Steps đề cập table/field → suy luận map Dx)
- [ ] CREATE/UPDATE: verify **cả giá trị đúng lẫn format** (encoding, timezone, trailing space,...)
- [ ] DELETE/soft-delete: verify **không bị ghost reference** ở nơi khác
- [ ] MIGRATE: verify **data cũ không mất, data mới đúng**
- [ ] Có boundary: null / empty / max length / max record count
- [ ] Có negative: invalid type / SQL injection / XSS input (nếu áp dụng)

### A.4 Feature impact (mục 4.3)
- [ ] Mỗi tính năng T1, T2,... đều có **≥ 1 regression TC** (Title/Steps đề cập màn hình/feature → suy luận map Tx)
- [ ] Tính năng `High` risk: có TC đi qua **full happy path end-to-end**
- [ ] Tính năng `Medium/Low`: có ít nhất smoke test

### A.5 Gap & orphan detection
- [ ] Không có impact nào trong 4.1/4.2/4.3 bị **bỏ sót**
- [ ] Không có TC nào lạc chủ đề (mọi TC thuộc scope BUG / Fx / Dx / Tx hoặc 1 mục checklist LME)
- [ ] TC có Title quá generic ("test feature X") không suy luận được → flag [MAJOR], đề nghị member rename

### A.6 Fix-shape adversarial check

> Đây là check **bắt buộc** sau khi A.1-A.5 đã pass coverage mechanical. Mục tiêu: catch các gap mà coverage matrix bị **đánh lừa bởi keyword** (vd: 1 TC map đúng F1 không có nghĩa F1 đã được verify đủ chiều).

- [ ] **Fix-shape identification**: đọc mục 2 `03-dev-impact.md` → identify fix shape (generic catch / specific check / validation / race-condition / cache / migration / soft-delete). Ghi rõ shape vào report.
- [ ] **Generic catch-all** → TCs verify với **≥ 3 trigger conditions khác nhau** + có **≥ 1 TC trigger condition CHƯA BIẾT** (test fallback generic). VD: fix payment error → cover ≥ `declined / insufficient / expired / 3DS_fail / network_timeout / unknown_code`.
- [ ] **Specific code check** → list **TẤT CẢ** condition Dev đã handle (hỏi Dev nếu cần), TCs cover từng cái một.
- [ ] **KH report symptom-only** (không nêu root cause) → TCs cover **≥ 2 plausible root causes** khác tạo cùng symptom đó. Hỏi Dev confirm có alternative root cause không.
- [ ] **Anti-pattern check**: rà nhanh [anti-patterns.md](anti-patterns.md) — bộ TCs có dính pattern AP-1 → AP-6 nào không?

---

## B. Chất lượng từng TC

### B.1 Rõ ràng
- [ ] Title mô tả **được mục đích**, không chung chung ("test A", "check B")
- [ ] Precondition đầy đủ (account, data seed, feature flag, timezone)
- [ ] Steps **tuần tự, rõ ràng**, không bỏ bước
- [ ] Expected **đo lường được** (có giá trị cụ thể, không "hiển thị đúng")

### B.2 Atomic
- [ ] 1 TC chỉ verify **1 mục đích chính**
- [ ] Nếu TC có ≥ 2 expected không liên quan → tách ra

### B.3 Độc lập
- [ ] TC có thể chạy **độc lập**, không phụ thuộc TC khác (trừ khi chain rõ ràng)
- [ ] Có cleanup / reset state rõ ràng

### B.4 Realistic
- [ ] Precondition **tạo được** trong môi trường test
- [ ] Data sample hợp lý (không dùng `"test"`, `"abc"` cho field nghiệp vụ)

---

## C. Chất lượng bộ TC (tổng thể)

- [ ] Tỷ lệ **Positive : Negative : Boundary : Regression** hợp lý (gợi ý: 30/25/25/20)
- [ ] **Không trùng lặp** TC (2 TC khác ID nhưng verify cùng thứ)
- [ ] **Priority phân bổ hợp lý** (không phải 100% High, không phải 100% Low)
- [ ] Có test cho các **role / permission** khác nhau (nếu feature có phân quyền)
- [ ] Có test **multi-device / responsive** (nếu là UI)
- [ ] Có test **i18n** nếu feature có multi-language (LME: JP/EN/VN,...)

---

## D. Spec alignment

- [ ] TCs **không mâu thuẫn** spec cũ (trừ khi spec được đánh dấu cần update)
- [ ] Nếu spec cần update (flag ở `02-spec-reference.md`) → có **note** trong report
- [ ] Có TC cho **mọi business rule** đã list trong `02-spec-reference.md`

---

## E. Hành chính

- [ ] TC IDs theo format chuẩn của team
- [ ] File 04-tc-list.md được lưu đúng folder review
- [ ] Tester ký tên / version đã điền

---

## F. Base checklist LME (bắt buộc với mọi task LME)

Kiểm tra member đã base [checklist-lme.md](checklist-lme.md) chưa. Checklist gồm 3 phần tương ứng 3 sheet gốc.

### F.1 Checklist web (§A trong checklist-lme.md)
- [ ] A.1 Function checklist — rà qua 22 item CL1-CL22, check các item **liên quan task** (upload file, format line user, hủy hợp đồng, trigger chat, setting action, xóa file media, phân trang, naming rule, link LINE friend, max data, CRUD đúng account, update/delete impact, search JP, copy/preview, plan limits, data input + upload ảnh, double click, thao tác liên tục, chuyển tab, reload, staff account)
- [ ] A.2 Non-function — 4 mục: URLs đo lường (8 URL không được đổi), Regression, Security (URL mới), Compatibility (Win+Mac, Android+iOS)

### F.2 Checklist job (§B trong checklist-lme.md)
- [ ] B.1 Job callback — nếu task chạm callback
- [ ] B.2 Job sync Java — CLJ01: Sync Google rate limit + retry (khi chạm Form/Salon/Lesson google sync)

### F.3 Các tính năng chung (§C trong checklist-lme.md)
Với **mỗi** feature chung mà task chạm đến → verify đã cover:
- [ ] C.1 Bill tiền — delay callback + 5 loại (bot/item/salon/lesson/event)
- [ ] C.2 Send message — 12 job + 7 web + 4 app + case message error + case friend block
- [ ] C.3 Friend info — 3 loại folder + 8 nơi hiển thị web + 5 line user + 1 app + 11 nơi update + 3 insert code
- [ ] C.4 Tag — 8 nơi hiển thị web + 1 app + 5 nơi update web + 1 app
- [ ] C.5 Google sheet — 4 tính năng liên kết + 5 case edge (chưa cấp/mất quyền, ký tự đặc biệt, xuống dòng, job retry 2 loại header form)
- [ ] C.6 Google calendar
- [ ] C.7 Plan limits — 5 case + 3 server profile
- [ ] C.8 Sort — 24+ màn có sort
