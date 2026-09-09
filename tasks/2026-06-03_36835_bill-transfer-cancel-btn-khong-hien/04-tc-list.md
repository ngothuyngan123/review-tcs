<!-- sync-target: https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 -->
# 04 — TC List (fetched từ Sheet, read-only)

> ⚠️ TCs dưới đây **fetch nguyên văn** từ Redmine #36835 Link TCs — tab **"Quản lý hợp đồng"** (gid 223705530), **Line 255-297**. KHÔNG sửa giá trị cell dù bug fix có thể đổi behavior. Member/Leader chỉ dùng để review coverage.
>
> Tab này dùng **cấu trúc TC phân cấp** (Main Function → Sub1…Sub5 → Expect Result), KHÔNG phải bảng 10 cột TC-ID chuẩn của team. Vì vậy bảng dưới giữ nguyên layout gốc của Sheet (cột A–J). Ô trống = **kế thừa giá trị từ dòng phía trên** (cách đọc nested test thông thường). Cột "Row" = số dòng trong Sheet để trace ngược.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 (tab "Quản lý hợp đồng", Line 255-297) |

---

## Ghi chú trong Sheet (Row 255-256 — KHÔNG phải TC)

- **Row 255** — block tham chiếu bug + đánh giá ảnh hưởng Dev (đã đưa vào [03-dev-impact.md](03-dev-impact.md)).
- **Row 256** — Tái hiện case KH (đã đưa vào [01-bug-task.md](01-bug-task.md)) + điều kiện kỹ thuật:
  > `1105` — check điều kiện: `univa_account_number = null`, `status_payment != 1,2`, `payment_method = 2`

---

## TC List (Row 257-297 — fetch nguyên văn)

| Row | A: Assignee | B: Main Function | C: Sub1 | D: Sub2 | E: Sub3 | F: Sub4 | G: Sub5 | H: Note | I: Expect Result | J: Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 257 | | Check khi mua mới hợp đồng | bill 1 năm | thanh toán tranfer | check khi stk chưa được phát hành<br>chưa thanh toán | check khi vào detail bằng id bot contract | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card<br>check db: | |
| 258 | | | | | check khi stk đã được phát hành<br>chưa thanh toán | check khi vào detail bằng id bot contract | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card<br>check db: | |
| 259 | | | | | khi plan chưa add bot | check GUI | | - hiển thị status chờ chuyển khoản<br>- hủy chuyển khoản thành công<br>- | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card<br>check db: | |
| 260 | | | | | | check db | | | - khi nhấn change từ tranfer sang card => db thực hiện hủy đi change id đợi chuyển khoản cũ<br>- check db: | |
| 261 | | | | | khi plan đã add bot standard | check GUI | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card<br>check db: | |
| 262 | | | | | | check db | | | - khi nhấn change từ tranfer sang card => db thực hiện hủy đi change id đợi chuyển khoản cũ<br>- check db: | |
| 263 | | | | | khi plan đã add bot pro | check GUI | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card<br>check db: | |
| 264 | | | | | | check db | | | - khi nhấn change từ tranfer sang card => db thực hiện hủy đi change id đợi chuyển khoản cũ<br>- check db: | |
| 265 | | | | | check plan enterprice | | | | | |
| 266 | | | bill 2 năm | | | | | | | |
| 267 | | Check khi detail hợp đồng đang bill năm<br>đang thanh toán card | check khi click vào button: 銀行振込に変更する<br>change phương thức thanh toán | check khi đến hạn expired_date | chưa thanh toán chuyển khoản | check GUI | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card | OK |
| 268 | | | | | | Check db | | | - check các trường thay đổi trong db<br>- payment)method=2 | |
| 269 | | | | check khi chưa đến hạn expired_date | | check GUI | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>決済方法の変更: back lại phương thức cũ<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được back lại phương thức cũ | OK |
| 270 | | | | | | Check db | | | - check các trường thay đổi trong db | |
| 271 | | | | check khi đến hạn expired_date | chưa phát hành stk | check GUI | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card | |
| 272 | | | | | | Check db | | | - check các trường thay đổi trong db | |
| 273 | | Check khi detail hợp đồng đang bill năm<br>đang thanh toán tranfer | chưa thanh toán chuyển khoản | tạo id tranfer trong 30 ngày | Check GUI | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 274 | | | | | Check thao tác thực hiện change từ năm sang tháng | | | | - Thực hiện change thành công => lúc change phải thực hiện nhập card<br>- check db:change id tranfer đã được hủy | |
| 275 | | | | | - thao tác thực hiện được change từ tranfer sang card | | | | - Thực hiện change thành công => lúc change phải thực hiện nhập card<br>- check db:change id tranfer đã được hủy | |
| 276 | | | chưa phát hành stk | Check GUI | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 277 | | | | Check thao tác | Check thao tác thực hiện change từ năm sang tháng | | | | - Thực hiện change thành công => lúc change phải thực hiện nhập card<br>- check db:change id tranfer đã được hủy | |
| 278 | | | | | - thao tác thực hiện được change từ tranfer sang card | | | | - Thực hiện change thành công => lúc change phải thực hiện nhập card<br>- check db:change id tranfer đã được hủy | |
| 279 | | Check upgade | upgrade từ free lên standard | thanh toán tranfer<br>chưa thanh toán | | | | | - button ở màn list không được vào màn detail contract | OK |
| 280 | | | | đang chờ phát hành số tài khoản | | | | | - button ở màn list không được vào màn detail contract | OK |
| 281 | | | upgrade từ standard lên pro | thanh toán tranfer<br>chưa thanh toán | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button<br>- thao tác thực hiện được change từ năm sang tháng<br>- thao tác thực hiện được change từ tranfer sang card | OK |
| 282 | | | | | thao tác thực hiện được change từ năm sang tháng | | | | - thực hiện change thành công => lúc change phải thực hiện nhập card<br>- check db:change id tranfer đã được hủy | |
| 283 | | | | | thao tác thực hiện được change từ tranfer sang card | check khi bill failse | | | đợi chốt | |
| 284 | | | | | | check khi bill thành công | | | - upgare lên plan pro | |
| 285 | | | | đang chờ phát hành số tài khoản | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 286 | | Đang chờ thanh toán lại | hủy hợp đồng => hợp đồng lại | thanh toán tranfer<br>chưa thanh toán | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 287 | | | | đang chờ phát hành số tài khoản | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 288 | | Quá hạn (expired + 7 ngày < now) | hợp đồng đã bị cancel | | | | | | - check job chạy đã cancel được hủy hợp đồng hay chưa | |
| 289 | | Gia hạn hợp đồng<br>Extent | thanh toán tranfer<br>chưa thanh toán | | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 290 | | | đang chờ phát hành số tài khoản | | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 291 | | Overdue | | | | | | | - check các button k bị disiable:<br>次回決済から月払いに変更する: change từ năm sang tháng, enable button<br>クレジットカードに変更する: change từ tranfer sang card, enable button | |
| 292 | | | check thao tác thực hiện được change từ năm sang tháng | | | | | | | |
| 293 | | | check thao tác thực hiện được change từ tranfer sang card | | | | | | | |
| 294 | | Check account staff | | | | | | | | |
| 295 | | | | | | | | | | |
| 296 | | Change card information | | | | | | | | |
| 297 | CucDTK | Change card information | click từ btn : メインカード情報を変更する | | | | | | - mở modal thay đổi thông tin card | |

---

## Member tự check trước khi submit

- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] Mỗi impact trong 4.1 / 4.2 / 4.3 có ít nhất 1 TC verify
- [ ] Có ít nhất 1 TC verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có ít nhất 1 TC regression cho mỗi tính năng trong 4.3
- [ ] Title TC chứa keyword giúp Leader nhận ra impact TC đó cover

<!-- Source: fetched từ Redmine #36835 Link TCs, range A255:J297 tab "Quản lý hợp đồng" (gid 223705530) lúc 2026-06-03. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
