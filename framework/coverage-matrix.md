# Coverage Matrix — Impact × TC

> Ma trận đối chiếu **từng impact** (từ `03-dev-impact.md`) với **từng TC** (từ `04-tc-list.md`).
> File 04 **không có** cột "Map to Impact" — Leader/Claude **suy luận** mapping từ Title / Precondition / Steps / Expected của mỗi TC.

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

| Impact | Loại | Priority Dev đánh giá | TCs cover (suy luận) | # TC cover | Status |
|---|---|---|---|---|---|
| BUG (root cause) | Fix | — | TC001 | 1 | OK |
| F1 — `<function_name>` | Function | Direct | TC002, TC005 | 2 | OK |
| F2 — `<function_name>` | Function | Indirect | — | **0** | **GAP** |
| D1 — `<table.column>` | Data | — | TC003, TC006, TC007 | 3 | OK |
| D2 — `<cache_key>` | Data | — | TC008 | 1 | RISK (chỉ 1 TC, không có boundary) |
| T1 — `<feature>` | Feature | High | TC004, TC009 | 2 | OK |
| T2 — `<feature>` | Feature | Medium | — | **0** | **GAP** |

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

1. **[review-checklist.md](review-checklist.md) §A.6** — Fix-shape adversarial check
2. **[anti-patterns.md](anti-patterns.md)** — rà 6 anti-pattern

Nếu chỉ tin matrix mechanical → dễ bỏ lọt **single-trigger generic-fix** (AP-1) và **symptom-only KH report** (AP-2). Xem ví dụ task #36443 (Univapay) trong AP-1.
