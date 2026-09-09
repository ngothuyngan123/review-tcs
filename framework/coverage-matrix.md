# Coverage Matrix — Impact × TC

> Ma trận đối chiếu **từng impact** (từ `03-dev-impact.md`) với **từng TC** (từ `04-tc-list.md`).
> File 04 **không có** cột "Map to Impact" — map **quan điểm** đọc thẳng ở cột `Mã quan điểm liên kết`; map **impact BUG/F/D/T** thì Leader/Claude **suy luận** từ `Tiêu đề test case` / `Điều kiện tiền đề` / `Các bước thực hiện` / `Kết quả mong đợi` của mỗi TC.
> _(Task cũ trước 2026-07-16, format 10 cột: suy luận từ Title / Precondition / Steps / Expected result; TC ID dạng `TC001`.)_

---

## Cách dùng

1. Liệt kê **tất cả** impact từ `03-dev-impact.md` (BUG, F1..Fn, D1..Dn, T1..Tn) vào cột đầu.
2. Đọc qua từng TC trong `04-tc-list.md`. Với mỗi TC, suy luận impact nào TC đó cover dựa vào:
   - **Title** chứa tên function → map về `Fx`
   - **Title/Steps** đề cập DB table/field → map về `Dx`
   - **Title/Steps** đề cập màn hình/feature → map về `Tx`
   - **Title** "reproduce KH"/"verify bug fix" → map về `BUG`
3. Tính tổng cột **# TC cover** — nếu = 0 → GAP; nếu ≤ 1 với impact `High` → RISK.

---

## Template bảng

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| BUG (root cause) | Fix | TC-FUNC001-01 | 1 | 1/1 | OK |
| F1 — `<function_name>` | Function | TC-FUNC002-01, TC-FUNC004-02 | 2 | 2/2 | OK |
| F2 — `<function_name>` | Function | — | **0** | — | **GAP** |
| D1 — `<table.column>` | Data | TC-DATADB001-01, -02, -03 | 3 | 3/3 | OK |
| D2 — `<cache_key>` | Data | TC-DATACACHE001-01 | 1 | 0/1 | RISK (chỉ 1 TC, chưa chạy) |
| T1 — `<feature>` | Feature | TC-REG001-01, -02 | 2 | 2/2 | OK |
| T2 — `<feature>` | Feature | — | **0** | — | **GAP** |

> **6 cột này là bản chốt** cho [/review-tc BƯỚC 2](../.claude/commands/review-tc.md) — nhưng là **nháp nội bộ**: từ 2026-09-05 ma trận đầy đủ **KHÔNG còn ghi vào report**. Chỉ dòng `GAP` / `RISK` / `orphan` được chuyển sang **§1** của [templates/05-review-report.template.md](../templates/05-review-report.template.md) (kèm cột `Chiều` = `dev-impact` / `diff code` / `orphan`); dòng `OK` chỉ đếm vào câu Kết luận.
> `Exec` = `<số pass>/<số TC>`, **chỉ điền khi nguồn TC là MCP LME TEST STUDIO**; nguồn khác ghi `—`.
> Không còn cột `Priority` — độ ưu tiên suy từ mã quan điểm; quan điểm thiếu TC ghi ở **§2** report.

### Status legend

- **OK** — đủ coverage (có ≥ 1 TC + đủ chiều positive/negative/boundary/regression theo loại impact)
- **RISK** — có TC nhưng chưa đủ chiều
- **GAP** — **không TC nào** cover → **MUST fix** trước merge

---

## Reverse matrix — TC nào lạc chủ đề

| TC ID | Title | Cover impact nào? | Status |
|---|---|---|---|
| TC001 | Reproduce KH ... | BUG | OK |
| TC002 | generateLinkInviteStaff: ... | F1 | OK |
| TCxxx | Test general feature X | **không thuộc scope dev-impact** | **ORPHAN — đề nghị remove** |

TC không thuộc scope BUG / F* / D* / T* → **case thừa** hoặc member viết case **lạc chủ đề** → đề nghị remove hoặc map lại.

---

## Khi suy luận không chắc chắn

- TC title quá generic (vd "Test feature A") → Leader/Claude flag: "TC này map impact nào không rõ — đề nghị member đặt tên rõ hơn".
- TC steps mô tả nhiều scenario → có thể map nhiều impact, nhưng nên tách thành nhiều TC atomic hơn.
- Nếu thực sự không xác định được → flag là **ambiguous** trong report, không tự bịa.

---

## Giới hạn của coverage matrix

Coverage matrix **map TC → impact bằng keyword** — không suy luận về **trigger space** hay **fix shape**. Sau khi build matrix xong và status đều OK, **bắt buộc** chạy thêm:

1. **[/review-tc BƯỚC 2 chiều (b)](../.claude/commands/review-tc.md)** — 4 câu hỏi adversarial trên diff thật (Studio `dev_impact` + `spec_delta`)
2. **[anti-patterns.md](anti-patterns.md)** — rà 6 anti-pattern

Nếu chỉ tin matrix mechanical → dễ bỏ lọt **single-trigger generic-fix** (AP-1) và **symptom-only KH report** (AP-2). Xem ví dụ task #36443 (Univapay) trong AP-1.
