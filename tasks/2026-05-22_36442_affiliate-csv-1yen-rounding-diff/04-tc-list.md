<!-- sync-target: https://docs.google.com/spreadsheets/d/1EENdNqrbOXVhLNctkQjEP024TSj0bot5-ocvDKHB_R0/edit?gid=833089149#gid=833089149 -->
# 04 — Test Cases (fetched từ Redmine Link TCs)

> **Source**: Fetched từ Google Sheet tab `Improve admin v2.0` (gid=833089149) lúc 2026-05-22, theo Redmine #36442 chỉ định `line: 521-538`.
> **TCs READ-ONLY** — KHÔNG sửa expected/title của TCs cũ này dù bug fix đổi behavior. Đây là baseline để Leader đánh giá coverage.
> **Lưu ý format sheet**: Sheet `Improve admin v2.0` dùng cấu trúc phân cấp 10 cột (Assignee / Main Function / Sub1 / Sub2 / Sub3 / Sub4 / Sub5 / Actual Result / Status / Comment staff) — **không khớp** 10 cột chuẩn template (TC ID / Title / Type / Priority / Precondition / Steps / Expected / Output note / Assignee / Status). Bảng dưới giữ nguyên cấu trúc source để verify map row-to-row. Khi chạy `/sync-tc` cần check kỹ mapping với target sheet.
> **Cell rỗng = merge từ row trên** (visual merged cell trong Sheet). Row 532 trở đi nhiều cell rỗng vì kế thừa từ Sub1 = "check data khi down load xuống" của row 532.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester | `<member điền sau khi review>` |
| Ngày viết | `<member điền>` |
| Version | `<member điền>` |
| Link Sheet gốc | https://docs.google.com/spreadsheets/d/1EENdNqrbOXVhLNctkQjEP024TSj0bot5-ocvDKHB_R0/edit?gid=833089149#gid=833089149 |
| Range fetched | `A521:J538` (18 rows) |

---

## TC List (raw từ Sheet)

| Src row | Assignee (A) | Main Function (B) | Sub1 (C) | Sub2 (D) | Sub3 (E) | Sub4 (F) | Sub5 (G) | Actual Result (H) | Status (I) | Comment (J) |
|---|---|---|---|---|---|---|---|---|---|---|
| 521 | | | Support #36442: [15-05-2026][Admin] Master admin — sai lệch 1円 trang đại lý vs CSV (32 user, dư 32 yên)<br>1. Nguyên nhân<br>   - Trên màn hình admin số tiền 報酬額 được làm tròn xuống, còn khi download csv thì số tiền đang đc làm tròn với số gần nhất<br>   => có sự lệch 1円<br>2. Cách fix<br>   - ở frontend màn hình admin và download csv: làm tròn với số gần nhất<br>3. Đã check và sửa các function sử dụng đến function/data vừa sửa<br>4. Đánh giá ảnh hưởng<br>        4.1 List function<br>            - public/\_assets/modules/supper\_admin/js/affiliater.js<br>            - exportCsvV2 (app/Http/Controllers/Admin/AffiliateInfoController.php)<br>        4.2 List những data bị update khi fix bug<br>            - k có<br>        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng<br>            - màn hình admin 商品決済<br>            - export csv 振込用CSV tại màn 商品決済 | | | | | | | |
| 522 | | | Tái hiện case KH:<br>1. Ở admin => vào màn 代理店報酬<br>2. Down load csv ở Cột 1 振込用CSV của tháng 4<br>Hiện tượng: Hiển thị amount ở admin chênh lệch, không làm tròn<br>ở csv down load về có làm tròn | Query 1 user sai số amount<br>SELECT sum(amount \* rate / 100 - sub\_amount) FROM \`payment\_detail\_aff\` WHERE \`user\_id\` = 54333 and (payment\_detail\_aff.type\_bill IN (1,2) OR (payment\_detail\_aff.type\_bill = 3 AND payment\_detail\_aff.status\_transfer = 1)) AND payment\_detail\_aff.flag\_display = 1 and payment\_detail\_aff.status\_refund = 0 and ( (payment\_detail\_aff.created\_at BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59' AND payment\_detail\_aff.remain\_day < 365) OR (payment\_detail\_aff.payment\_date BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59' AND payment\_detail\_aff.remain\_day >= 365 AND payment\_detail\_aff.parent\_month = 0) OR (payment\_detail\_aff.created\_at BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59' AND payment\_detail\_aff.remain\_day >= 365 AND payment\_detail\_aff.parent\_month = 1)) group by user\_id | | | | | query tổng user trong tháng 4<br>select affiliate\_info.\*, users.username, users.company\_name, pd.amount, pd.count\_pm from affiliate\_info inner join (SELECT user\_id, SUM(amount \* (rate / 100) - sub\_amount) AS amount, COUNT(\*) AS count\_pm FROM payment\_detail\_aff where (payment\_detail\_aff.type\_bill IN (1,2) OR (payment\_detail\_aff.type\_bill = 3 AND payment\_detail\_aff.status\_transfer = 1)) AND payment\_detail\_aff.flag\_display = 1 and payment\_detail\_aff.status\_refund = 0 AND ((payment\_detail\_aff.created\_at BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59' AND payment\_detail\_aff.remain\_day < 365) OR (payment\_detail\_aff.payment\_date BETWEEN '2026-04-01 00:00:00' AND '2026-04-30 23:59:59' AND payment\_detail\_aff.remain\_day >= 365 AND payment\_detail\_aff.parent\_month = 0) OR (payment\_detail\_aff.created\_at BETWEEN '2026-04-01 [...truncated by source...]) | |
| 523 | | | Check hiển tổng số account ở admin | check khi số amount có các số lẻ phía sau | ,5<br>ví dụ: ¥ 15,557 | | | - làm tròn l: ¥ 15,558<br>- check ở màn hình admin số amount đã được làm tròn<br>- check down load csv số amount đã được làm tròn | Not test | |
| 524 | | | | | ,6<br>ví dụ: ¥ 18,627 | | | - làm tròn lên: ¥ 18,628<br>- check ở màn hình admin số amount đã được làm tròn<br>- check down load csv số amount đã được làm tròn | Not test | |
| 525 | | | | | ammount: 12382.6 | | | - làm tròn lên : ¥ 12,383<br>- check ở màn hình admin số amount đã được làm tròn<br>- check down load csv số amount đã được làm tròn | Not test | |
| 526 | | | | | amount: 3810.8 | | | - làm tròn lên : ¥ 3,811<br>- check ở màn hình admin số amount đã được làm tròn<br>- check down load csv số amount đã được làm tròn | Not test | |
| 527 | | | | check hiển thị tổng số tiền | | | | - trường: 振込金額<br>- hiển thị tổng số tiền sau khi đã làm tròn | Not test | |
| 528 | | | | check khi edit số amount | | | | - down load về hiển thị theo số amount mới edit | Not test | |
| 529 | | | check khi có user đăng ký affliate | | | | | - hiển thị lên list data với số amount tổng tương ứng | Not test | |
| 530 | | | Check khi nhấn double down load | nhấn down load liền tục | | | | - down load về thành công<br>- hiển thị số amount tương ứng với GUI | Not test | |
| 531 | CucDTK | 会計用CSV: down load csv thanh toán | check format | | | | | - format cvs down load:<br>https://docs.google.com/spreadsheets/d/1j0yIzyveUMvf21GuRtjK4mCJy5UTercWPjaAWGkDwc4/edit?gid=0#gid=0 | Not test | |
| 532 | CucDTK | | check data khi down load xuống | 代理店登録名: Tên đăng ký đại lý | | | | - name trong bảng affiliate\_info<br>- data down load về hiển thị giống trên GUI | | |
| 533 | CucDTK | | | 銀行名: Tên ngân hàng | | | | - bank\_name trong bảng affiliate\_info<br>- data down load về hiển thị giống trên GUI | | |
| 534 | CucDTK | | | 支店名: Tên chi nhánh | | | | - branch\_name trong bảng affiliate\_info<br>- data down load về hiển thị giống trên GUI | | |
| 535 | CucDTK | | | 口座番号: Số tài khoản | | | | - account\_number trong bảng affiliate\_info<br>- data down load về hiển thị giống trên GUI | | |
| 536 | CucDTK | | | 口座名義: Tên tài khoản | | | | - account\_holder\_name trong bảng affiliate\_info<br>- data down load về hiển thị giống trên GUI | | |
| 537 | CucDTK | | | 振込金額: Số tiền chuyển khoản | | | | - data down load về hiển thị giống trên GUI<br>- số amount đã được làm tròn như trên GUI | Not test | |
| 538 | CucDTK | | | インボイス登録: Đăng ký hóa đơn | | | | - type\_aff bảng affliate\_info | Not test | |

---

## ⚠️ Cảnh báo dành cho Leader / Reviewer

1. **Row 521 và 522 không phải TC** — là heading impact (521) và reference query (522) mà Dev/QA paste vào Sheet để context. Khi sync hoặc đếm coverage thì exclude 2 rows này.

2. **Row 532-536 không có Status** (col I trống) — visual có thể là merge với row 537 hoặc đơn giản chưa fill. Verify với Cúc (QA viết bộ TC) trước khi run.

3. **Merge cell context** — Sub1 (cột C) của các row 524, 525, 526 trống vì kế thừa từ row 523 "Check hiển tổng số account ở admin". Tương tự, Sub1 của row 532-538 kế thừa "check data khi down load xuống" / "会計用CSV" từ row 531. Khi review từng TC độc lập, **đọc cùng row parent** để hiểu context.

4. **Coverage gap quan sát ban đầu** (Leader cần verify ở step `/review-tc`):
   - **Halfway boundary** (¥X.5 case): Row 523 chỉ có `,5` ví dụ ¥15,557 → cover được half-yen rounding. Nhưng **rule round-to-nearest có khác biệt** giữa "banker's rounding" và "round half up" tại boundary .5 → cần TC riêng cover cả 2 hướng.
   - **Negative amount / 0 amount / amount âm**: hiện không có TC cho amount = 0 hoặc sub\_amount > amount (negative reward).
   - **Multi-user CSV**: 32 user lệch 1円 — nhưng TC hiện chỉ verify per-user. Có TC nào verify **tổng các user** trong CSV khớp với sum trên GUI không?
   - **Function caller bị sót** (mục 3 dev-impact trống): nếu có job batch tổng hợp doanh số đại lý dùng cùng logic làm tròn → chưa có TC regression.

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH: GUI vs CSV cùng amount sau làm tròn)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2 — **chú ý halfway .5 boundary**
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME (xem [framework/checklist-lme.md](../../framework/checklist-lme.md))

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§B Checklist job**: (khả năng không áp dụng — verify nếu có job batch dùng cùng logic làm tròn)
- [ ] B.1 Job callback (nếu chạm callback)
- [ ] B.2 Job sync Java — CLJ01 (nếu chạm Google sync)

**§C Các tính năng chung** (chọn feature mà task chạm đến):
- [ ] C.1 Bill tiền — **HIGH liên quan** (đây là feature về tiền hoa hồng đại lý)

---

<!-- Source: fetched từ Redmine #36442 Link TCs, tab "Improve admin v2.0" gid=833089149 range A521:J538 lúc 2026-05-22. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
