<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763#gid=412698763 | sheet=Improve 2026.05 | anchor=Main Function -->

# 04 — TC List (fetch từ Sheet "Improve 2026.05" — read-only, member verify)

> ⚠️ **CẢNH BÁO RANGE**: Redmine ghi `Row: 808 ~ 827`, nhưng rows 808–827 thực tế là TC của **richmenu sort** (không liên quan bug tag #38226). TC đúng của #38226 nằm tại **rows 828–847** (header section "SpecImprove #38226: [Detail friend][Tag]…" ở row 828, 18 TC ở rows 830–847). File này dùng range đúng (rows 830–847). **Tester confirm lại với Hạnh Nguyễn về số row trong Redmine.**
>
> ⚠️ **CẤU TRÚC NGUỒN**: Sheet "Improve 2026.05" KHÔNG phải bảng TC 10 cột phẳng — đây là sheet phân cấp (Main Function / Sub1…Sub5 / Expect Result), cột anchor = "Main Function". Bảng dưới đây là kết quả **forward-fill** các cell merge để mỗi dòng = 1 TC đọc được. **Giá trị từng cell giữ NGUYÊN văn**, chỉ ghép phân cấp vào cột Title + tách bậc sâu vào Steps. Cột "Status" lấy từ cột Actual/đánh dấu trong sheet (đang là `OK`).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763#gid=412698763 (tab "Improve 2026.05", rows 830–847) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check add tag | | | | Check add tag tại: **chat 1:1 right bar** | - Tại detail friend tag 現在ついているタグ, hiển thị folder A được mở sẵn<br>- Bên trong folder A hiển thị tag 1 | | | OK |
| TC002 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check add tag | | | | Check add tag tại: **left bar (avt friend)** | (như TC001 — folder A xổ sẵn, hiển thị tag 1) | | | OK |
| TC003 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check add tag | | | | Check add tag tại: **multi action (web)** | (như TC001 — folder A xổ sẵn, hiển thị tag 1) | | | OK |
| TC004 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check add tag | | | | Check add tag tại: **multi action (job)** — Check 1 modal | (như TC001 — folder A xổ sẵn, hiển thị tag 1) | | | OK |
| TC005 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check add tag | | | | Check add tag tại: **mobile** — check add chat 1:1 / check add trong detail | (như TC001 — folder A xổ sẵn, hiển thị tag 1) | | | OK |
| TC006 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check tag 1 được khôi phục lại | | | | web | - Không hiển thị được gắn cho friend nữa | | | OK |
| TC007 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check tag 1 change sang folder khác | | | | Folder được change đang hiển thị có tag khác được gắn | - Hiển thị folder đó đang được xổ có chứa tag 1 bên trong | | | OK |
| TC008 | Check hiển thị tag > folder A có tag bên trong > tag 1 được gắn cho friend tại folder A > Check tag 1 change sang folder khác | | | | Folder được change chỉ có tag 1 được gắn | - Hiển thị folder đó đang được xổ có chứa tag 1 bên trong | | | OK |
| TC009 | Check hiển thị tag > folder A có tag bên trong > tag 1 đang được gắn cho friend => gỡ tag 1 > Web | | | | Khi folder A chỉ có gắn tag 1 | - Tại detail friend tag 現在ついているタグ không hiển thị folder A bên dưới | | | OK |
| TC010 | Check hiển thị tag > folder A có tag bên trong > tag 1 đang được gắn cho friend => gỡ tag 1 > Web | | | | Khi folder A gắn thêm tag khác | - Tại detail friend tag 現在ついているタグ vẫn hiển thị folder A đang được xổ nhưng không hiển thị tag 1 bên trong nữa | | | OK |
| TC011 | Check hiển thị tag > folder A có tag bên trong > tag 1 đang được gắn cho friend => gỡ tag 1 > APP | | | | Khi folder A chỉ có gắn tag 1 | - Tại detail friend tag 現在ついているタグ không hiển thị folder A bên dưới | | | OK |
| TC012 | Check hiển thị tag > folder A có tag bên trong > tag 1 đang được gắn cho friend => gỡ tag 1 > APP | | | | Khi folder A gắn thêm tag khác | - Tại detail friend tag 現在ついているタグ vẫn hiển thị folder A đang được xổ nhưng không hiển thị tag 1 bên trong nữa | | | OK |
| TC013 | Check hiển thị tag > folder A có tag bên trong (end-to-end multi folder) | | | Friend đang có tag ở 2 folder (F1 có 2 tag, F2 có 1 tag, F3 không có tag) | 1. Mở màn 友だち詳細 của 1 friend đang có tag ở 2 folder (folder F1 có 2 tag, F2 có 1 tag, F3 không có tag)<br>2. Bấm tab 「タグ」 (現在ついているタグ)<br>3. Quan sát danh sách folder ngay khi vừa load | Folder F1 và F2 mở sẵn, hiển thị ngay bảng tag đang gắn (mũi tên caret ở trạng thái mở); tổng cộng thấy đủ 3 dòng tag mà không cần click gì thêm. Không hiển thị folder F3 | | | OK |
| TC014 | Check hiển thị tag > folder A có tag bên trong > User tự đóng 1 folder rồi reload | | | 2 folder có tag → mở sẵn cả 2 | Vào tab タグ (2 folder có tag → mở sẵn cả 2)<br>Bấm tên folder thứ 1 để đóng nó lại (chỉ còn folder 2 mở)<br>Thực hiện thao tác gỡ 1 tag (màn tự tải lại danh sách tag)<br>Quan sát lại trạng thái mở/đóng | Folder vẫn được xổ ra | | | OK |
| TC015 | Check hiển thị tag > folder A không được gắn tag nào | | | | (folder rỗng, không có tag) | Folder rỗng (không có tag) KHÔNG hiển thị tại 現在ついているタグ; chỉ folder có tag mới hiển thị và xổ tag được gắn. | | | OK |
| TC016 | Check hiển thị tag > Friend chưa có tag / không có folder nào | | | Friend chưa có tag / không có folder nào | Mở tab Tag | Hiển thị trống data với text タグが設定されていません。(không lỗi) | | | OK |
| TC017 | Check add/gỡ tag bình thường (regression) | | | | Add / gỡ tag như flow cũ | Đảm bảo vẫn add/gỡ tag bình thường<br>Lịch sử add/gỡ tag hiển thị đúng | | | OK |
| TC018 | check acc staff | | | Đăng nhập bằng account staff | Add / gỡ tag, xem tab Tag | - Đảm bảo vẫn add/gỡ tag bình thường<br>- Các folder có chứa tag được xổ sẵn<br>- Lịch sử add/gỡ tag hiển thị đúng | | | OK |

### Chú thích cột

- **Type / Priority / Output note / Assignee**: nguồn sheet không có → để trống, member fill khi review.
- **Status**: lấy từ cột đánh dấu trong sheet (`OK`). Giữ nguyên, KHÔNG sửa.

---

## Member tự check trước khi submit

`<member điền sau khi review>`

<!-- Source: fetched từ Redmine #38226 Link TCs, sheet "Improve 2026.05" (spreadsheet 1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I, gid 412698763). Redmine ghi Row 808-827 (SAI — là richmenu sort); range đúng dùng ở đây là rows 830-847 (18 TC), header section #38226 ở row 828. Fetched 2026-06-29. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
