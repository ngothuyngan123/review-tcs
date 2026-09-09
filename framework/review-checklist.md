# Review Checklist — cho Leader review TAY

> ⚠️ **Skill `/review-tc` KHÔNG đọc file này.** Quy trình tự động đã bao trọn nội dung cũ —
> xem bảng "Đã chuyển đi đâu" bên dưới. File này giữ lại cho Leader muốn review thủ công,
> hoặc dùng làm rubric khi đọc lại `05-review-report.md` do Claude sinh.

## Đã chuyển đi đâu

43/61 mục của bản cũ trùng nguyên si các bước trong [/review-tc](../.claude/commands/review-tc.md).
Đã gỡ khỏi file này để không còn 2–3 nơi định nghĩa cùng một thứ:

| Mục cũ | #box | Nay nằm ở |
|---|---|---|
| A.1 Bug root cause · A.2 Function impact · A.3 Data impact · A.4 Feature impact · A.5 Gap & orphan | 18 | **BƯỚC 2** coverage matrix + [coverage-matrix.md](coverage-matrix.md) — ma trận là nháp nội bộ, chỉ `GAP`/`RISK` ra **§1** report |
| A.6 Fix-shape adversarial check | 5 | **BƯỚC 2 chiều (b)** — 4 câu hỏi adversarial trên diff thật + [anti-patterns.md](anti-patterns.md) AP-1…AP-6; kết quả ra **§1** (chiều `diff code`) + **§4** (anti-pattern) |
| F.1 Quan điểm · F.2 Catalog · F.3 RULE | 16 | **BƯỚC 3** — [checklist-lme.index.md](checklist-lme.index.md) + [catalog-lme.index.md](catalog-lme.index.md), kết quả ra **§2** report (chỉ ghi quan điểm còn thiếu) |
| D Spec alignment | 3 | **BƯỚC 1** (nguồn spec) + §6 report |
| C — "không trùng lặp TC" | 1 | **BƯỚC 4b** — 4 yếu tố so trùng, kết quả ra **§3** report |
| E Hành chính | 3 | Bỏ hẳn — TC ID format do validator kiểm; mục ký duyệt đã bỏ khỏi report |

Phần còn lại (**B** + **C**) là thứ **không** bước nào khác làm — đã được nhúng thành bảng 10 mục
ở **BƯỚC 4a** của `/review-tc`, và giữ nguyên bên dưới cho người dùng tay.

---

## B. Chất lượng từng TC

### B.1 Rõ ràng
- [ ] Title mô tả **được mục đích**, không chung chung ("test A", "check B"), và chứa **keyword** (tên function / DB table / màn hình) để suy luận được impact
- [ ] Precondition đầy đủ (account, data seed, feature flag, timezone) — người khác đọc là **dựng lại được env**
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

- [ ] Tỷ lệ **Normal : Abnormal : Boundary** hợp lý (gợi ý: 40/35/25 — điều chỉnh theo bản chất task; task phân quyền/validation thì Abnormal + Boundary nhiều hơn)
- [ ] **Phân bố quan điểm hợp lý** — không dồn hết TC vào 1 quan điểm, không bỏ trống quan điểm ◯ ưu tiên Cao
- [ ] Có test cho các **role / permission** khác nhau (nếu feature có phân quyền)
- [ ] Có test **multi-device / responsive** (nếu là UI)
- [ ] Có test **i18n** nếu feature có multi-language (LME: JP/EN/VN,...)

<!-- Task cũ (trước 2026-07-16, format 10 cột): tỷ lệ Positive:Negative:Boundary:Regression ~30/25/25/20 + Priority phân bổ hợp lý (không 100% High/Low) -->
