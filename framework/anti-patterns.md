# Anti-patterns — pattern dễ bỏ lọt khi review TCs

> Khi review (manual hoặc qua `/review-tc`), rà nhanh checklist dưới. Mỗi anti-pattern có cách detect + severity nếu dính.

---

## AP-1: Single-trigger generic-fix

**Triệu chứng**: Mục 2 dev-impact ghi cách fix dạng generic ("set error message return về frontend", "handle exception", "catch error", "thêm try-catch"). TCs chỉ test với **1 trigger condition** duy nhất.

**Tại sao dễ bỏ lọt**: Coverage matrix mechanical map TC → Fx (function impact) → status OK vì có TC. Nhưng impl có thể là `if (error.code === X) return error.message` (specific) thay vì `try { ... } catch (e) { return e.message }` (generic). Các trigger khác vẫn silent fail.

**Cách detect**:
1. Đọc mục 2 dev-impact, tìm keyword: `set error message`, `return error`, `handle exception`, `try-catch`, `fallback message`.
2. Nếu match → đếm số trigger condition khác nhau trong steps của TCs verify error. < 3 → flag [BLOCKER].
3. Hỏi: "Có TC nào trigger với error code CHƯA BIẾT TRƯỚC không?" Nếu không → flag [BLOCKER] về missing generic-catch verification.

**Ví dụ real**: task #36443 Univapay — fix generic, TCs chỉ test `bill > max` (1 trigger = `AMOUNT_EXCEEDED`). Bỏ sót card_declined / insufficient_funds / 3DS_fail / network_timeout / unknown_code.

---

## AP-2: Symptom-only KH report

**Triệu chứng**: File 01 (bug task) mô tả KH thấy **hiện tượng** ("màn quay lại", "không load được", "hiển thị sai số") nhưng KH KHÔNG nói rõ error message / error code / root cause. Dev tái hiện 1 case duy nhất trong "Steps to reproduce".

**Tại sao dễ bỏ lọt**: TCs viết bám sát "Steps to reproduce" của Dev → chỉ cover 1 root cause Dev đoán. KH thực tế có thể gặp root cause khác mà cũng tạo cùng symptom.

**Cách detect**:
1. Trong file 01: tìm trong "Mô tả bug" + "Actual result" — có ghi error message / error code / log cụ thể không?
2. Nếu chỉ ghi hiện tượng → flag [MAJOR]: "Hỏi Dev có alternative root cause không. TCs cover ≥ 2 plausible root causes."

**Ví dụ real**: task #36443 — KH chỉ thấy "màn hình tự quay về trước khi bấm nút mua". Dev đoán "vượt max" để tái hiện. Có thể KH gặp 3DS fail / network timeout cũng cho ra symptom giống.

---

## AP-3: Happy-path-only regression

**Triệu chứng**: Mục 4.3 dev impact list nhiều feature `T1, T2, T3` (regression scope). TCs có 1 TC mỗi T với precondition "data sạch, account standard, no edge state". Không có TC chạy regression với feature liền kề ở trạng thái lỗi / empty / max.

**Tại sao dễ bỏ lọt**: "Có TC cho Tx" → matrix tick OK. Nhưng regression không phải chỉ verify "happy path còn chạy" mà phải verify "edge state cũ không bị break thêm".

**Cách detect**:
1. Với mỗi Tx trong 4.3 → đếm TC cover. Nếu chỉ 1 TC và precondition không có edge state → flag [MAJOR].

---

## AP-4: Specific code-check disguised as generic catch

**Triệu chứng**: Mục 2 viết "set error message generic" nhưng khi đọc PR diff (nếu có link) → thực tế là `if (error.code === A) ... else if (error.code === B) ...`. Code path chỉ handle error codes Dev biết trước.

**Tại sao dễ bỏ lọt**: Review chỉ đọc file 03, không đọc code. Nếu PR link trống ở mục "Thông tin" → không thể verify.

**Cách detect**:
1. Nếu mục "Commit / Pull Request" trống → flag [MAJOR]: "Yêu cầu Dev cung cấp PR link để review có thể verify fix shape thực tế."
2. Đặt câu hỏi adversarial trong report: "Fix là generic catch-all hay specific code-check? Nếu specific, list tất cả code đã handle?"

---

## AP-5: Layer-downstream over-coverage (mirror của AP-1)

**Triệu chứng**: Bug fix ở **layer A** (vd: controller). TCs test **cả** layer A + layer B (vd: model / service / DB raw) dù layer B không bị chạm code.

**Tại sao dễ bỏ lọt**: Coverage matrix không phân biệt "TC cần cover" vs "TC nice-to-have". Tester có xu hướng over-test.

**Cách detect**:
1. Với mỗi TC → trace xem có touch code path Dev đã sửa không. Nếu không → flag [NIT] ORPHAN, đề nghị remove hoặc re-label là regression.

**Tham chiếu**: memory `feedback_root_cause_layer_focus.md`.

---

## AP-6: Mục 3 dev-impact trống (caller chưa list)

**Triệu chứng**: Mục 3 "Đã check và sửa các function sử dụng đến function/data vừa sửa" trống — chỉ có heading.

**Tại sao dễ bỏ lọt**: Coverage matrix dựa trên 4.1/4.2/4.3 → mục 3 trống không trigger flag tự động.

**Cách detect**:
1. Đọc mục 3 — nếu trống / chỉ có heading → flag [MAJOR]: "Yêu cầu Dev list caller. Có thể có function khác cùng pattern bug, cùng cần fix."

---

## Cách dùng khi review

Trong `/review-tc` BƯỚC 3c, sau khi identify fix-shape → rà nhanh AP-1 → AP-6. Mỗi AP dính → ghi vào §4 report với prefix `[AP-N]`.
