<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763 | sheet=Improve 2026.05 | anchor=Main Function -->

# 04 — TC List (fetched từ Redmine #38206 Link TCs)

> ⚠️ **TCs READ-ONLY** — fetch nguyên văn từ Google Sheet master (tab "Improve 2026.05", row 755–796). KHÔNG sửa Title/Steps/Expected dù nghi không còn đúng sau fix. Mọi đề xuất sửa/bổ sung đưa vào `05-review-report.md`.
>
> Sheet này dùng **format phân cấp** (anchored "Main Function"): mỗi nhóm Main Function (cột B) trải xuống nhiều dòng con; cột C/D là điều kiện/sub-condition; cột E là step chi tiết; cột Expected (H) + Status (J). Ô trống = "kế thừa giá trị dòng trên" (merged cell). Giữ nguyên cấu trúc gốc.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763 (tab "Improve 2026.05", row 755–796) |

> **Row 755** trong Sheet là bản **đánh giá ảnh hưởng của Dev** (không phải TC) — nội dung đã phản ánh ở `03-dev-impact.md`. Bảng dưới bắt đầu từ row 756.

---

## TC List (giữ nguyên cấu trúc Sheet)

| Row | Main Function (B) | Điều kiện (C) | Sub-condition (D) | Steps (E) | Expected (H) | Status (J) |
|---|---|---|---|---|---|---|
| 756 | Tái hiện bug: Khi sort tại màn tag, vào màn detail friend tại modal edit tag và modal filter đang không hiển thị đúng thứ tự các tag<br>Expect: Hiển thị thứ tự tag tại màn detail friend giống với màn quản lý tag | | | | | OK staging |
| 757 | Check hiển thị thứ tự tag_id tại màn tag khớp với thứ tự detail friend tag | Check khi folder có ít tag | Check khi sort tag | Sort tag => check detail friend tag | - Thứ tự tag tại detail friend giống màn tag List<br>- Không hiển thị các tag đã bị xóa | OK staging |
| 758 | | | | Check khi sort tag => sort tiếp => check detail friend tag | | OK staging |
| 759 | | | | Check khi sort tag => xóa tag => check detail friend tag | | OK staging |
| 760 | | | | Check khi sort tag => thêm tag => check detail friend tag | | OK staging |
| 761 | | | Check khi tạo tag => check bên detail tag | | | OK staging |
| 762 | | | Check khi xóa tag => check detail tag | | | OK staging |
| 763 | | Check khi folder có nhiều tag | Check khi sort tag => check detail friend tag | Sort tag => check detail friend tag | | OK staging |
| 764 | | | | Check khi sort tag => sort tiếp => check detail friend tag | | OK staging |
| 765 | | | | Check khi sort tag => xóa tag => check detail friend tag | | OK staging |
| 766 | | | | Check khi sort tag => thêm tag => check detail friend tag | | OK staging |
| 767 | | | Check khi tạo tag => check bên detail tag | | | OK staging |
| 768 | | | Check khi xóa tag => check detail tag | | | OK staging |
| 769 | | Check các case khác liên quan tới modal filter + modal edit | Check modal filter filter bình thường | | Hiển thị đúng kết quả filter ra | OK staging |
| 770 | | | Check khi modal edit thao tác bình thường | | Thực hiện add/gỡ tag được bình thường | OK staging |
| 771 | Check hiển thị thứ tự landing_id tại màn qr landing khớp với thứ tự detail friend landing | Check khi folder có ít QR | Check khi sort QR | Sort QR=> check detail friend QR | - Thứ tự QR tại detail friend giống màn QR List<br>- Không hiển thị QR đã bị xóa | Not test |
| 772 | | | | Check khi sort QR => sort tiếp => check detail friend QR | | OK |
| 773 | | | | Check khi sort QR=> xóa QR=> check detail friend QR | | OK |
| 774 | | | | Check khi sort QR=> thêm QR=> check detail friend QR | | OK |
| 775 | | | Check khi tạo QR=> check bên detail QR | | | OK |
| 776 | | | Check khi xóa QR=> check detail QR | | | OK |
| 777 | | Check khi folder có nhiều QR | Check khi sort QR=> check detail friend QR | Sort QR=> check detail friend QR | | OK |
| 778 | | | | Check khi sort QR=> sort tiếp => check detail friend QR | | OK |
| 779 | | | | Check khi sort QR => xóa QR=> check detail friend QR | | OK |
| 780 | | | | Check khi sort QR=> thêm QR=> check detail friend QR | | OK |
| 781 | | | Check khi tạo QR=> check bên detail friend QR | | | OK |
| 782 | | | Check khi xóa QR=> check detail friend QR | | | OK |
| 783 | | Check các case khác liên quan tới modal filter | Check modal filter filter bình thường | | Hiển thị đúng kết quả filter ra | OK |
| 784 | Check hiển thị thứ tự richmenu_id tại màn richmenu khớp với thứ tự detail friend richmenu | Check khi folder có ít richmenu | Check khi sort richmenu | Sort richmenu=> check detail friend richmenu | - Thứ tự richmenu tại detail friend giống màn richmenu List<br>- Không hiển thị richmenu đã bị xóa | Not test |
| 785 | | | | Check khi sort richmenu=> sort tiếp => check detail friend richmenu | | OK |
| 786 | | | | Check khi sort richmenu=> xóa richmenu=> check detail friend richmenu | | OK |
| 787 | | | | Check khi sort richmenu=> thêm richmenu=> check detail friend richmenu | | OK |
| 788 | | | Check khi tạo richmenu=> check bên detail richmenu | | | OK |
| 789 | | | Check khi xóa richmenu=> check detail richmenu | | | OK |
| 790 | | Check khi folder có nhiều richmenu | Check khi sort richmenu=> check detail friend richmenu | Sort richmenu=> check detail friend richmenu | | Not test |
| 791 | | | | Check khi sort richmenu=> sort tiếp => check detail friend richmenu | | OK |
| 792 | | | | Check khi sort richmenu=> xóa richmenu=> check detail friend richmenu | | OK |
| 793 | | | | Check khi sort richmenu=> thêm richmenu=> check detail friend richmenu | | OK |
| 794 | | | Check khi tạo richmenu=> check bên detail friend richmenu | | | OK |
| 795 | | | Check khi xóa richmenu=> check detail friend richmenu | | | OK |
| 796 | | Check các case khác liên quan tới modal filter | Check modal filter filter bình thường | | Hiển thị đúng kết quả filter ra | OK |

---

## Member tự check trước khi submit

<member điền sau khi review>

<!-- Source: fetched từ Redmine #38206 Link TCs, range A755:J796 tab "Improve 2026.05" lúc 2026-06-26. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
