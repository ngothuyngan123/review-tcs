# Check máy docs — Đặc tả chi tiết LME Public API v1 (Phase 1) · bản 1.3.0 16/11/2026

> Kết quả là ỨNG VIÊN `DOC-EX` / `DOC-INT` — AI mở L<n> xác nhận trước khi ghi report.

## 1. JSON trong khối code

ok 70 · fragment 1 · nhiều dòng 4 · có placeholder (bỏ qua) 2 · **không parse được 0**

## 2. Số học phân trang

| L | JSON path | Vấn đề |
|---|---|---|
| L505 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |
| L527 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |
| L559 | `$.data` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |

## 3. Số epoch (giây) trong docs — so với ngày phát hành docs 16/11/2026

| L | Giá trị | UTC | JST |
|---|---|---|---|
| L309 | `1763280060` | 2025-11-16 08:01:00 UTC | 2025-11-16 17:01:00 JST |

## 4. Anchor nội bộ

Không có link hỏng / id trùng.

## 5. Code tabs (khối `EX` trong script) ↔ request mẫu cùng endpoint

Khớp toàn bộ (12 code tabs).

## 6. Ví dụ ↔ bảng field của docs (field · kiểu · tập giá trị)

| L | Endpoint | Lệch |
|---|---|---|
| L713 | `GET /friends/detail` | `data.friend.system_name` = `null` trái kiểu `string` (bảng L605) |
| L713 | `GET /friends/detail` | `data.friend.email` = `null` trái kiểu `string` (bảng L606) |
| L713 | `GET /friends/detail` | `data.friend.phone` = `null` trái kiểu `string` (bảng L607) |
| L1377 | `GET /conversations/detail` | `data.handling_status` = `{"id": 12, "name": "対応中"}` trái kiểu `HandlingStatus` (bảng L1352) |
| L1469 | `GET /conversations/detail` | `data.handling_status` = `null` trái kiểu `HandlingStatus` (bảng L1352) |

## 7. Dữ liệu mẫu giữa các ví dụ (cùng ID mà khác giá trị)

Nhất quán.

## 8. Số phần tử mảng ↔ phân trang

| L | Endpoint | Lệch |
|---|---|---|
| L505 | `GET /friends` | `data.friend_detail` có 1 phần tử; theo total_items=250, page=1, limit=100 phải là 100 — không ghi rút gọn |
| L1175 | `GET /templates` | `data.templates` có 2 phần tử; theo total_items=24, page=1, limit=100 phải là 24 — không ghi rút gọn |

> Mục 6–8 là ứng viên `DOC-INT` (ví dụ ↔ docs / ví dụ bất hợp lý). Các quy tắc ngữ nghĩa (thứ tự sắp xếp, quy tắc riêng endpoint, câu chuyện dữ liệu giữa endpoint) vẫn phải rà tay.
