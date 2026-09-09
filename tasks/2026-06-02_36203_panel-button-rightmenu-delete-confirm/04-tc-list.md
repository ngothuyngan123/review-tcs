<!-- sync-target: https://docs.google.com/spreadsheets/d/131XoTI-AM4S6OwKbwcFlMnNJr0jVtbmpcOnf1BkiScs/edit?gid=1417809174#gid=1417809174 -->
# 04 — TC List (fetch từ Redmine #36203 Link test case)

> ⚠️ **TCs read-only** — fetch nguyên văn từ Google Sheet master, KHÔNG sửa. Nếu thấy TC không còn đúng sau fix → báo Leader, không tự chỉnh ở đây.
>
> ⚠️ **Lưu ý mapping cột:** Tab nguồn "Template button" dùng layout cột **riêng** (Nhóm / Điều kiện / Precondition / Check item / Action / Expected / Status), KHÔNG khớp 10 cột chuẩn team. Đã map về template như sau, giữ nguyên giá trị cell:
> - **Precondition** ← (cột C "Điều kiện") + (cột D "Precondition phụ")
> - **Steps** ← (cột E "Check item") + (cột F "Action")
> - **Expected result** ← cột G; **Status** ← cột H
> - **TC ID** tự đánh số tham chiếu (sheet gốc cột A trống). **Type / Priority / Output note / Assignee**: sheet gốc không có → để trống.
>
> ℹ️ 2 dòng đầu range (sheet row 1575–1576) là **nội dung Đánh giá dev + Tái hiện case** dán vào sheet, KHÔNG phải TC → đã đưa vào `03-dev-impact.md` / `01-bug-task.md`, không liệt kê dưới đây.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc (nếu có) | `https://docs.google.com/spreadsheets/d/131XoTI-AM4S6OwKbwcFlMnNJr0jVtbmpcOnf1BkiScs/edit?gid=1417809174#gid=1417809174` (tab "Template button", line 1575–1617) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Template button standard | | | Khi tạo 5 panel; check khi kéo scroll về phía panel 1 | click vào icon 3 chấm của panel 4 | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | OK |
| TC002 | Template button standard | | | Khi tạo 6 panel; click hover vào icon 3 chấm của panell 5 | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | OK |
| TC003 | Template button standard | | | Khi tạo 7 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | OK |
| TC004 | Template button standard | | | Khi tạo 8 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | OK |
| TC005 | Template button standard | | | Khi tạo 9 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | OK |
| TC006 | Template button standard | | | Khi tạo 10 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái thành công<br>- Xóa panel thành công | | | OK |
| TC007 | Template button standard | | | Check khi send template cho user | | - Màn user hiển thị số panel tương ứng với template<br>- User click vào btn panel send action thành công cho user<br>( anh Tư bảo k ảnh hưởng chỗ này nên k cần check kỹ) | | | OK |
| TC008 | Template button standard | | | Check khi xóa panel; panle đã có thông tin ảnh, button,action | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | OK |
| TC009 | Template button standard | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | OK |
| TC010 | Template button standard | | | panle chưa có thông tin | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | OK |
| TC011 | Template button standard | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | OK |
| TC012 | Template button standard | | | check xóa panel liên tục | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | OK |
| TC013 | Template button standard | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn<br>- đóng modal | | | OK |
| TC014 | Template button color | | | Khi tạo 5 panel; check khi kéo scroll về phía panel 1 | click vào icon 3 chấm của panel 4 | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC015 | Template button color | | | Khi tạo 6 panel; click hover vào icon 3 chấm của panell 5 | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC016 | Template button color | | | Khi tạo 7 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC017 | Template button color | | | Khi tạo 8 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC018 | Template button color | | | Khi tạo 9 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC019 | Template button color | | | Khi tạo 10 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái thành công<br>- Xóa panel thành công | | | Not test |
| TC020 | Template button color | | | Check khi send template cho user | | - Màn user hiển thị số panel tương ứng với template<br>- User click vào btn panel send action thành công cho user<br>( anh Tư bảo k ảnh hưởng chỗ này nên k cần check kỹ) | | | Not test |
| TC021 | Template button color | | | Check khi xóa panel; panle đã có thông tin ảnh, button,action | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC022 | Template button color | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC023 | Template button color | | | panle chưa có thông tin | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC024 | Template button color | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC025 | Template button color | | | check xóa panel liên tục | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC026 | Template button color | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC027 | Template button image | | | Khi tạo 5 panel; check khi kéo scroll về phía panel 1 | click vào icon 3 chấm của panel 4 | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC028 | Template button image | | | Khi tạo 6 panel; click hover vào icon 3 chấm của panell 5 | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC029 | Template button image | | | Khi tạo 7 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC030 | Template button image | | | Khi tạo 8 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC031 | Template button image | | | Khi tạo 9 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái/phải thành công<br>- Xóa panel thành công | | | Not test |
| TC032 | Template button image | | | Khi tạo 10 panel | | - Click vào icon 3 chấm hiển thị lên thông tin để thao tác<br>- Copy panel thành công<br>- Đổi vị trí qua trái thành công<br>- Xóa panel thành công | | | Not test |
| TC033 | Template button image | | | Check khi send template cho user | | - Màn user hiển thị số panel tương ứng với template<br>- User click vào btn panel send action thành công cho user<br>( anh Tư bảo k ảnh hưởng chỗ này nên k cần check kỹ) | | | Not test |
| TC034 | Template button image | | | Check khi xóa panel; panle đã có thông tin ảnh, button,action | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC035 | Template button image | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC036 | Template button image | | | panle chưa có thông tin | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC037 | Template button image | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC038 | Template button image | | | check xóa panel liên tục | check hiển thị modal confirm xóa; click btn: 削除する xóa | - hiển thị modal confirm khi xóa<br>- xóa thành công panel<br>- modal hiển thị giống ở component | | | Not test |
| TC039 | Template button image | | | | click btn: キャンセル k xóa, tắt modal | - Xóa không thành công panel<br>- Panel vẫn còn | | | Not test |
| TC040 | Check tạo template Quick Reply | | | Dạng ảnh | | - tạo được template bình thường<br>- send được cho user | | | Not test |
| TC041 | Check tạo template Quick Reply | | | Dạng text | | | | | Not test |

<!-- Source: fetched từ Redmine #36203 Link test case, range A1575:J1617 tab "Template button" lúc 2026-06-02. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
