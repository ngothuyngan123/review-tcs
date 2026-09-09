<!-- sync-target: https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 -->
# 04 — TC List (fetch từ Redmine #37109 Link TCs)

> ⚠️ **Lưu ý format**: Tab nguồn **"Quản lý hợp đồng"** dùng layout **checklist** (Hạng mục → Mô tả case → Điều kiện → Expected → Status), **KHÔNG** phải bảng TC chuẩn 10 cột. Mapping bên dưới đã giữ **nguyên văn** giá trị cell, có chú thích cột gốc. Các cột `Type / Priority / Steps / Assignee` trống vì tab nguồn không có. Cột **TC ID** = số dòng trên Sheet (để trace). Title = ghép `[Hạng mục (B)] — [Mô tả case (C)]`.
>
> 🔒 TCs này là **read-only** — fetch từ Sheet master, **KHÔNG sửa** dù nghi không còn đúng sau fix; mọi thay đổi phải confirm với Leader.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 (tab "Quản lý hợp đồng", row 1624~1642) |

---

> **Row 1624** (không phải TC): ô col B chứa bản copy "Đánh giá ảnh hưởng" của bug #37109 — nội dung **trùng** `03-dev-impact.md`, xem file đó thay vì lặp lại tại đây.

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1625 | **▼ Overdue credit card** (section header) | | | | | | | | |
| 1626 | Check điều kiện để hiển thị status overdue — Bot bị hết hạn expired bị bill lỗi nhưng time quá hạn chưa quá 7 ngày | | | Bot contract có:<br>- payment_menthod =1 (card)<br>- status =1 (đang hợp đồng)<br>- expired_date <now & now - expired_date < 7 ngày<br>- status_payment = 2 (bill fail)<br>- status_payment_fail != (0,5) | | Hiển thị trạng thái hợp đồng overdue credit card | | | OK |
| 1627 | Check banner cảnh báo — Check UI | | | | | | | | OK |
| 1628 | Check hiển thị ngày cancel hợp đồng | | | | | ngày cancel = expired_date + 7 ngày<br>format 〇︎月〇︎日 | | | OK |
| 1629 | Check detail hợp đồng — status ステータス | | | | | 延滞中<br>〇︎月〇︎日までに決済が行われない場合、強制解約となります<br>=> hiện đúng ngày cancel hợp đồng<br>ngày cancel = expired_date + 7 ngày<br>format 〇︎月〇︎日 | | | OK |
| 1630 | Check click text クレジットカードの変更 | | | | | Hiện màn change card クレジットカードの変更 | | | OK |
| 1631 | Check click text プリペイド型カード | | | | | open new tab https://vpc.lifecard.co.jp/ | | | OK |
| 1632 | check click button クレジットカードの変更 | | | | | Hiện màn change card クレジットカードの変更 | | | OK |
| 1633 | Check màn change card — nhập card bill success | | | | | nhập card success thì thực hiện bill tiền luôn<br>    + lưu lại thông tin main card mới<br>    + update lại các thông tin hợp đồng + tạo lịch sử bill tiền | | | OK |
| 1634 | (Check màn change card) — nhập card bill fail | | | | | Hiện màn change card fail<br>không update hợp đồng, không update thông tin card | | | OK |
| 1635 | **▼ Overdue bank transfer** (section header) | | | | | | | | |
| 1636 | Check điều kiện để hiển thị status overdue — Bot bị hết hạn expired nhưng user vẫn chưa chuyển khoản và time hết hạn chưa quá 7 ngày | | | Bot contract có:<br>- payment_menthod =2 (transfer)<br>- status =1 (đang hợp đồng)<br>- expired_date <now & now - expired_date < 7 ngày<br>- status_payment = 5 (đợi chuyển khoản) | | Hiển thị trạng thái hợp đồng overdue transfer | | | OK |
| 1637 | Check banner cảnh báo — Check UI | | | | | | | | OK |
| 1638 | Check hiển thị ngày cancel hợp đồng | | | | | ngày cancel = expired_date + 7 ngày | | | OK |
| 1639 | Check click text 指定口座 | | | | | Hiện modal thông tin chuyển khoản ngân hàng | | | OK |
| 1640 | check click button 振込口座を確認する | | | | | | | | OK |
| 1641 | Check detail hợp đồng — status ステータス | | | | | 延滞中<br>〇︎月〇︎日までに決済が行われない場合、強制解約となります<br>=> hiện đúng ngày cancel hợp đồng | | | OK |
| 1642 | Regression detail-bill-fail (max-friend bill fail): overdueDate() dùng cardBillMaxFriend không bị ảnh hưởng — Có data trigger màn max-friend bill fail (`cardBillMaxFriend`). | | | | | Ngày 強制解約 hiển thị đúng như trước fix (logic riêng cardBillMaxFriend, không dùng getOverDueDay của index.js). | | | OK |

---

## Member tự check trước khi review

<!-- member điền sau khi review -->

<!-- Source: fetched từ Redmine #37109 Link TCs, range A1624:J1642 tab "Quản lý hợp đồng" lúc 2026-06-09. Tab resolve bằng range + content match (Sheets API không expose gid/sheetId). KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
