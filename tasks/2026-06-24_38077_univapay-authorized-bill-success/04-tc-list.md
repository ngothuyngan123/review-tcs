<!-- sync-tcs: url=<chọn 1 trong 2 nguồn bên dưới khi sync> | sheet=<tên tab tương ứng> | anchor=Main Function -->
<!-- NGUỒN 1 (Lesson): url=https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=110079709 | sheet=Sửa bill tiền univapay | anchor=Main Function -->
<!-- NGUỒN 2 (Item):   url=https://docs.google.com/spreadsheets/d/1Uwdi0PvJE9l1rCYudLhopn52jjO0zbZ9VrqcTwX-XIM/edit?gid=1072366690 | sheet=Improve bill tiền univapay | anchor=Main Function -->

# 04 — TC List (fetched từ Redmine #38077 Link TCs — READ-ONLY)

> ⚠️ **Đây là TC HUMAN có sẵn**, fetch từ 2 sheet master qua Link TCs trong Redmine — **KHÔNG sửa nội dung** (Title / Precondition / Steps / Expected giữ nguyên giá trị cell từ Sheet).
> Cấu trúc gốc Sheet là phân cấp **Main Function → Sub1 (kịch bản) → Sub2 (status univapay) → Expect Result**; đã convert sang bảng 10 cột chuẩn team.
> Cột **Type / Priority** do AI suy luận từ status case (Authorized = case fix chính của bug 38077; Successful = baseline; Failed = nhánh lỗi) — KHÔNG có trong Sheet gốc, Leader chỉnh nếu cần.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<TC human có sẵn — Thanh Phương map trong Redmine>` |
| Ngày submit | `2026-06-24` (fetched) |
| Version TCs | `fetched-v1` |
| Link TC gốc (nếu có) | Lesson: [Sheet](https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=110079709) tab "Sửa bill tiền univapay" rows 167~173 · Item: [Sheet](https://docs.google.com/spreadsheets/d/1Uwdi0PvJE9l1rCYudLhopn52jjO0zbZ9VrqcTwX-XIM/edit?gid=1072366690) tab "Improve bill tiền univapay" rows 318~327 |

---

## TC List

### A. Lesson booking — tab "Sửa bill tiền univapay" (Main Function: Check job get kết quả bill univapay)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-L01 | Check job get kết quả bill univapay — Check booking mới — status = Successful | Regression | Medium | Booking mới được tạo qua flow bill univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Successful` | update thông tin booking<br>- bảng calendar_course_bookings<br> + payment_status =1<br> + status_webhook =1<br> + update thông tin thanh toán thêm charge id<br> + send action booking, add remind booking => CHECK TRIGGER HIỂN THỊ TRÊN CHAT 1:1<br> + sync booking lên google spreed<br>- bảng calendar_course_receptions giữ nguyên<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 168 | | |
| TC-L02 | Check job get kết quả bill univapay — Check booking mới — status = Failed | Negative | Medium | Booking mới được tạo qua flow bill univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Failed` | xóa booking<br>+ không send action booking, không add remind booking<br>- bảng calendar_course_receptions update lại:<br>+ total_booking -1<br>+ total_approve -1<br>- send message thanh toán fail cho user<br>決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき再度、購入手続きを行なってください。 | Sheet row 169 | | |
| TC-L03 | Check job get kết quả bill univapay — Check booking mới — status = Authorized | Positive | High | Booking mới được tạo qua flow bill univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Authorized` | Update được giống case status = Successful<br><br>update thông tin booking<br>- bảng calendar_course_bookings<br> + payment_status =1<br> + status_webhook =1<br> + update thông tin thanh toán thêm charge id<br> + send action booking, add remind booking => CHECK TRIGGER HIỂN THỊ TRÊN CHAT 1:1<br> + sync booking lên google spreed<br>- bảng calendar_course_receptions giữ nguyên<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 170 · **case fix chính #38077** | | |
| TC-L04 | Check job get kết quả bill univapay — Check case approve booking — status = Successful | Regression | Medium | Booking ở trạng thái chờ approve; admin approve booking → bill univapay; job get kết quả bill chạy | Univapay trả về `status = Successful` | update booking:<br><br>update status_webhook =1<br>update status =1<br>update payment_status =1, update thông tin charge<br>send action booking, add remind => CHECK TRIGGER HIỂN THỊ TRÊN CHAT 1:1<br>sync google sheet<br>không send message bill thành công giống case book mới<br><br>- bảng calendar_course_receptions update lại:<br>+ total_booking +1<br>+ total_approve +1<br>+ total_request -1 | Sheet row 171 | | |
| TC-L05 | Check job get kết quả bill univapay — Check case approve booking — status = Failed | Negative | Medium | Booking ở trạng thái chờ approve; admin approve booking → bill univapay; job get kết quả bill chạy | Univapay trả về `status = Failed` | update booking:<br><br>update status_webhook =2<br>không change status booking<br>không update payment_status<br>không send action booking, add remind<br>không sync google sheet<br>không send message bill fail giống case book mới<br><br>- bảng calendar_course_receptions giữ nguyên | Sheet row 172 | | |
| TC-L06 | Check job get kết quả bill univapay — Check case approve booking — status = Authorized | Positive | High | Booking ở trạng thái chờ approve; admin approve booking → bill univapay; job get kết quả bill chạy | Univapay trả về `status = Authorized` | Update được giống case status = Successful<br><br>update status_webhook =1<br>update status =1<br>update payment_status =1, update thông tin charge<br>send action booking, add remind => CHECK TRIGGER HIỂN THỊ TRÊN CHAT 1:1<br>sync google sheet<br>không send message bill thành công giống case book mới<br><br>- bảng calendar_course_receptions update lại:<br>+ total_booking +1<br>+ total_approve +1<br>+ total_request -1 | Sheet row 173 · **case fix chính #38077** | | |

### B. Item — tab "Improve bill tiền univapay" (Main Function: Check job get kết quả bill)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-I01 | Check job get kết quả bill — Check item bill 1 lần — status = Successful | Regression | Medium | Mua mới item bill 1 lần qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Successful` | Update bảng s_order_history<br>- status_webhook =1<br>- send action mua item success<br>- send notify 【tên Bot】<line name> <tên qly item> が購入されました<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 319 | | |
| TC-I02 | Check job get kết quả bill — Check item bill 1 lần — status = Failed | Negative | Medium | Mua mới item bill 1 lần qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Failed` | - xóa bản ghi bảng s_order_history<br>- không send action<br>- send notify case bill fail 【tên Bot】<line name> <tên qly item> の決済に失敗しました<br>- send message thanh toán fail cho user<br>決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき再度、購入手続きを行なってください。 | Sheet row 320 | | |
| TC-I03 | Check job get kết quả bill — Check item bill 1 lần — status = Authorized | Positive | High | Mua mới item bill 1 lần qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Authorized` | Update được giống case status = Successful<br><br>Update bảng s_order_history<br>- status_webhook =1<br>- send action mua item success<br>- send notify 【tên Bot】<line name> <tên qly item> が購入されました<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 321 · **case fix chính #38077** | | |
| TC-I04 | Check job get kết quả bill — Check item bill chu kỳ: Mua mới item — status = Successful | Regression | Medium | Mua mới item bill chu kỳ qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Successful` | Check update db<br>1. Bảng s_cycle_order_history<br>- status_trial =1<br>- status_bill =1<br>- status_webhook =1<br>2. Bảng s_order_history<br>- status_order =1<br>- status_webhook =1<br><br>- send action cho user<br>- send notify bill item<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 322 | | |
| TC-I05 | Check job get kết quả bill — Check item bill chu kỳ: Mua mới item — status = Failed | Negative | Medium | Mua mới item bill chu kỳ qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Failed` | Xóa bản ghi 2 bảng s_cycle_order_history và s_order_history<br><br>- send action case bill fail<br>- send notify case bill fail 【tên Bot】<line name> <tên qly item> の決済に失敗しました | Sheet row 323 | | |
| TC-I06 | Check job get kết quả bill — Check item bill chu kỳ: Mua mới item — status = Authorized | Positive | High | Mua mới item bill chu kỳ qua univapay (callback); job get kết quả bill chạy | Univapay trả về `status = Authorized` | Update được giống case status = Successful<br><br>Check update db<br>1. Bảng s_cycle_order_history<br>- status_trial =1<br>- status_bill =1<br>- status_webhook =1<br>2. Bảng s_order_history<br>- status_order =1<br>- status_webhook =1<br><br>- send action cho user<br>- send notify bill item<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 324 · **case fix chính #38077** | | |
| TC-I07 | Check job get kết quả bill — Check item bill chu kỳ: Change card có bill tiền — status = Successful | Regression | Medium | Item bill chu kỳ; user change card có phát sinh bill tiền qua univapay; job get kết quả bill chạy | Univapay trả về `status = Successful` | check update db:<br>1. Bảng s_cycle_order_history<br>- status_bill =1<br>- status_webhook =1<br>- thông tin card: update thông tin card mới<br>- expired_date: update lại expired_date<br>- count_bill_error = Null<br><br>2. Bảng s_order_history<br>- status_order =1<br>- status_webhook =1<br><br>- send action bill lần 2<br>- send notify 【tên Bot】<line name> <tên qly item> の継続決済が行われました<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 325 | | |
| TC-I08 | Check job get kết quả bill — Check item bill chu kỳ: Change card có bill tiền — status = Failed | Negative | Medium | Item bill chu kỳ; user change card có phát sinh bill tiền qua univapay; job get kết quả bill chạy | Univapay trả về `status = Failed` | check update db:<br>1. Bảng s_cycle_order_history<br>- status_bill =1<br>- status_webhook =2<br>- thông tin card: update thông tin card mới (logic cũ từ trước case fail vẫn update lại thông tin card)<br>- expired_date không update<br>- count_bill_error +1<br><br>2. Bảng s_order_history<br>- status_order =3<br>- status_webhook =2<br><br>- send action case bill fail<br>- send notify case bill fail 【tên Bot】<line name> <tên qly item> の決済に失敗しました<br>- send message thanh toán fail cho user<br>決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき再度、購入手続きを行なってください。 | Sheet row 326 | | |
| TC-I09 | Check job get kết quả bill — Check item bill chu kỳ: Change card có bill tiền — status = Authorized | Positive | High | Item bill chu kỳ; user change card có phát sinh bill tiền qua univapay; job get kết quả bill chạy | Univapay trả về `status = Authorized` | Update được giống case status = Successful<br><br>check update db:<br>1. Bảng s_cycle_order_history<br>- status_bill =1<br>- status_webhook =1<br>- thông tin card: update thông tin card mới<br>- expired_date: update lại expired_date<br>- count_bill_error = Null<br><br>2. Bảng s_order_history<br>- status_order =1<br>- status_webhook =1<br><br>- send action bill lần 2<br>- send notify 【tên Bot】<line name> <tên qly item> の継続決済が行われました<br>- send message thanh toán thành công cho user<br>決済が完了しました。 | Sheet row 327 · **case fix chính #38077** | | |

### Chú thích cột

- **Type** (AI suy luận, không có trong Sheet): `Positive` = case Authorized (đúng theo fix #38077) / `Regression` = case Successful (baseline không được đổi) / `Negative` = case Failed.
- **Priority** (AI suy luận): `High` = 5 case Authorized (trực tiếp verify fix) / `Medium` = case Successful + Failed (regression baseline).
- **Output note**: ghi row gốc trên Sheet để Leader trace ngược. **KHÔNG** sửa Expected.
- **Status**: để trống — QA fill sau khi run (`OK` / `NG` / `Not test` / `NG -> Đã fix`).

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Job get kết quả bill univapay (callback) → cần trigger được webhook/callback từ univapay sandbox; verify sớm có thể dùng **Dev** (`form.watermeru.com`).

---

## Member tự check trước khi submit

> File này là TC **fetched read-only** — phần check dưới để Leader đối chiếu khi `/review-tc`.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] Có TC verify trực tiếp bug fix: 5 case **Authorized** (TC-L03, TC-L06, TC-I03, TC-I06, TC-I09) phải behave giống Successful
- [ ] **Mỗi impact** 4.1 / 4.3 có ≥1 TC: F1 getBookingTimeout (booking lesson) ↔ nhóm A · F2 getOrderTimeout (bill item) ↔ nhóm B
- [ ] Có ≥1 TC regression cho mỗi tính năng trong 4.3 (Successful/Failed baseline)
- [ ] Cân nhắc thiếu: TC cho **status univapay khác** (pending / canceled / unknown) ngoài 3 status Successful/Failed/Authorized — Leader xác nhận khi review

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md):
- [ ] §B.1 Job callback (task chạm job callback univapay)
- [ ] §C.1 Bill tiền

<!-- Source: fetched từ Redmine #38077 Link TCs.
     Lesson: spreadsheet 1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE tab "Sửa bill tiền univapay" range A167:N173 (rows 168-173 = 6 TCs).
     Item:   spreadsheet 1Uwdi0PvJE9l1rCYudLhopn52jjO0zbZ9VrqcTwX-XIM tab "Improve bill tiền univapay" range A318:N327 (rows 319-327 = 9 TCs).
     Fetched 2026-06-24 qua service account (google-sheets MCP pending approval → dùng Sheets API trực tiếp). KHÔNG sửa Expected nếu chưa confirm với Leader. -->
