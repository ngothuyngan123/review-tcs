# Check máy docs — Đặc tả chi tiết LME Public API v1 (Phase 1) · bản 1.3.0 16/11/2026

> Kết quả là ỨNG VIÊN `DOC-EX` / `DOC-INT` — AI mở L<n> xác nhận trước khi ghi report.

## 1. JSON trong khối code

ok 70 · fragment 1 · nhiều dòng 4 · có placeholder (bỏ qua) 2 · **không parse được 0**

## 2. Số học phân trang

| L | JSON path | Vấn đề |
|---|---|---|
| L536 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |
| L558 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |
| L590 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |

## 3. Số epoch (giây) trong docs — so với ngày phát hành docs 16/11/2026

| L | Giá trị | UTC | JST |
|---|---|---|---|
| L335 | `1763280060` | 2025-11-16 08:01:00 UTC | 2025-11-16 17:01:00 JST |

## 4. Anchor nội bộ

Không có link hỏng / id trùng.

## 5. Code tabs (khối `EX` trong script) ↔ request mẫu cùng endpoint

Khớp toàn bộ (12 code tabs).
