<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 | sheet=Task nhỏ + fix bug KH | anchor=Main Function -->
<!-- sync-target: https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 -->

# 04 — TC List (fetch từ Redmine #38312 Link TCs)

> ⚠️ **CẢNH BÁO RANGE** — Redmine ghi `row 237~284`, nhưng khi fetch thực tế:
> - **Rows 237–241** thuộc **task KHÁC** (`TC-NEW-04..07` + Regression "Share URL event chưa set ảnh tiêu đề" — bug OGP Facebook), **KHÔNG phải #38312** → đã **loại**.
> - Block #38312 thật bắt đầu ở **row 242** (dòng header `Bug Tester #38312...`) và kết thúc ở **row 290** (không phải 284). Range Redmine `~284` **cắt cụt** nhóm "Check job check callback bill tiền booking" (thiếu row 285–290).
> - File này lấy **đúng block #38312 = rows 242–290**. Tester **verify lại range** với người viết TC (Thanh Phương) trước khi review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` (nguồn: Thanh Phương — journal Redmine) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` (fetch read-only từ Sheet) |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 — sheet `Task nhỏ + fix bug KH`, rows 242–290 |

---

## TC List

> ⚠️ Sheet nguồn dùng **format phân cấp (anchored)**: `Main Function` / `Sub1` / `Sub2` / `Sub3` → không phải 10 cột chuẩn team. Giữ nguyên cấu trúc gốc để KHÔNG làm sai lệch TC.
> - Cột `Main Function` / `Sub1` / `Sub2` trống trong Sheet (do gộp ô) đã được **fill-forward** từ nhóm phía trên để mỗi dòng tự đủ nghĩa — **giá trị cell KHÔNG bị sửa**.
> - `Expected` / `Actual` / `Status` giữ **nguyên văn** cell (kể cả typo "clcik", "Boooking").

### Block header (row 242, nguyên văn từ Sheet)

```
Bug Tester #38312 Khi lưu lịch sử thay đổi friend info chưa lưu được action preview
1. Nguyên nhân: Chưa xử lý lưu được preview action friend info
2. Cách fix: - Lưu preview action lịch sử friend info
3. Đã check function/data
4. Đánh giá ảnh hưởng
  4.1 List function: handleOrderCallback (EventBookingService.php); saveAdminBooking (BookingEventDayController.php)
  4.2 List data update: k có
  4.3 Tính năng ảnh hưởng: Admin booking; Booking event có callback univapay
```

### TCs (rows 243–290)

| # | Main Function | Sub1 | Sub2 | Sub3 | Expected result | Status (Sheet) |
|---|---|---|---|---|---|---|
| 1 | Check admin thao tác ở web | Admin booking mới | Event có info KHÔNG liên kết friend info setting | | Booking success, không gán friend info | OK staging |
| 2 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info name | Booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text 設定なし | OK staging |
| 3 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info email | | OK staging |
| 4 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | OK staging |
| 5 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | OK staging |
| 6 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info text | | OK staging |
| 7 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | OK staging |
| 8 | Check admin thao tác ở web | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | Booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | OK staging |
| 9 | Check admin thao tác ở web | Admin approve booking | Event có info KHÔNG liên kết friend info setting | | approve booking success, không gán friend info _(Note: khi user book đã update luôn friend info; khi admin approve nếu value không đổi thì không update lại value và không tạo lịch sử friend info)_ | OK staging |
| 10 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info name | approve booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text 設定なし | OK staging |
| 11 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info email | | OK staging |
| 12 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | OK staging |
| 13 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | OK staging |
| 14 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info text | | OK staging |
| 15 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | OK staging |
| 16 | Check admin thao tác ở web | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | approve booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | OK staging |
| 17 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info KHÔNG liên kết friend info setting | | Edit booking success, không gán friend info | OK staging |
| 18 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info name | Edit booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text 設定なし | OK staging |
| 19 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info email | | OK staging |
| 20 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | OK staging |
| 21 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | OK staging |
| 22 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info text | | OK staging |
| 23 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | OK staging |
| 24 | Check admin thao tác ở web | Admin edit friend info của booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | Edit booking success, gán được info value cho user; Tạo được lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | OK staging |
| 25 | Check admin thao tác ở app (Ở app không có edit booking) | Admin booking mới | Event có info KHÔNG liên kết friend info setting | | Booking success, không gán friend info _(Note: Ở app không có booking mới)_ | Reject |
| 26 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info name | Booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text 設定なし | Reject |
| 27 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info email | | Reject |
| 28 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | Reject |
| 29 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | Reject |
| 30 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info text | | Reject |
| 31 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | Reject |
| 32 | Check admin thao tác ở app | Admin booking mới | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | Booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | Reject |
| 33 | Check admin thao tác ở app | Admin approve booking | Event có info KHÔNG liên kết friend info setting | | approve booking success, không gán friend info | OK staging |
| 34 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info name | approve booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text 設定なし | OK staging |
| 35 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info email | | OK staging |
| 36 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | OK staging |
| 37 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | OK staging |
| 38 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info text | | OK staging |
| 39 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | OK staging |
| 40 | Check admin thao tác ở app | Admin approve booking | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | approve booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | OK staging |
| 41 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info KHÔNG liên kết friend info setting | | Booking success, không gán friend info | OK staging |
| 42 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info name | Booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text 設定なし | OK staging |
| 43 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info email | | OK staging |
| 44 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info số điện thoại | | OK staging |
| 45 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info tỉnh | | OK staging |
| 46 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info text | | OK staging |
| 47 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select KHÔNG setting action | | OK staging |
| 48 | Check job check callback bill tiền booking | Khi có callback success => update friend info cho user | Event có info CÓ liên kết friend info setting | Liên kết với info select + trong value của select CÓ setting action | Booking success, gán được info value; Tạo lịch sử friend info => Cột action hiện text プレビュー -> clcik thì hiện được preview action | OK staging |

---

## Member tự check trước khi submit

<!-- Đây là TC fetch read-only từ Sheet. Member/Leader review theo /review-tc. -->

- [ ] Đã verify lại **range TC đúng** với người viết (do Redmine ghi lệch 237~284, thực tế 242~290).

<!-- Source: fetched từ Redmine #38312 Link TCs, tab "Task nhỏ + fix bug KH", block #38312 rows 242–290 (Redmine ghi 237~284 — lệch, đã hiệu chỉnh). KHÔNG sửa TCs này nếu chưa confirm với Leader. Fetch lúc 2026-07-02. -->
