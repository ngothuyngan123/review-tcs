# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38552 — [07-07-2026][TY-11470][Form] Form 六甲お子様アンケートフォーム (ペット有) có 13 câu trả lời nhưng spreadsheet chỉ hiển thị 4` |
| Redmine URL | https://redmine.watermelon.vn/issues/38552 |
| Auto-filled | `2026-07-11 by /new-task` |
| Ngày báo cáo | `2026-07-07` |
| Khách hàng / PM báo | `AI LME CSS` (author Redmine) — end user: `delamyoujin189@gmail.com`, bot `studio chikutaku` |
| Module / Màn hình | `Form` (category Redmine) — cụ thể: đồng bộ câu trả lời form lên Google Sheet |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env; bug do KH báo nên nhiều khả năng Production (step.lme.jp)>` |

Bổ sung (từ journal Redmine — Ngô Thúy Ngần, 2026-07-07):
- `bot_id` = 163932
- `form_id` = 200539
- Link spreadsheet KH: https://docs.google.com/spreadsheets/d/1cEv-rizCgjSsKOejuhL-kRcZ2aE4JacEElfy2PIxjao
- Parent issue: #38389

## Mô tả bug (nguyên văn từ khách hàng)

```
User: delamyoujin189@gmail.com
Bot Name: studio chikutaku

【Form hỏi đáp về cách thao tác (操作方法に関するお問い合わせフォーム)】
Mặc dù form 六甲お子様アンケートフォーム(ペット有) có 13 câu trả lời, nhưng trên spreadsheet chỉ hiển thị 4 câu.
Tại sao lại như vậy?

Link thread: https://l-message.slack.com/archives/C0BALS7S73L/p1783425385407679
Link item: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BF7DQFQCX
```

### 原文 (JP)

```
【操作方法に関するお問い合わせフォーム】
六甲お子様アンケートフォーム(ペット有)の回答が13件あるにも関わらずスプレッドシートには4件しか表示されていません。
なぜでしょうか？
```

### Comments (bổ sung từ khách)

**筒井 和紀** (2026-07-07 20:59) — `css.wss.2025@gmail.com` — đã được thêm quyền vào địa chỉ này.

**WSSサポーター** (2026-07-08 11:38) — "Trong spreadsheet đang xảy ra hiện tượng **lệch cột dữ liệu**, nên người dùng đang không thể xem được toàn bộ câu trả lời. Trước mắt, chúng tôi đã khôi phục lại. Nguyên nhân đang được kiểm tra nên mong anh/chị chờ trong giây lát."

**Thanh Duy Nguyen** (2026-07-09) — "A Thắng thảo luận chốt luôn write từ cột A, nếu có trường hợp lệch cột do KH sửa dẫn đến cột A ko có dữ liệu có thể bị ghi đè lên thì lỗi KH."

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguồn: journal Redmine của **Thanh Phương** (2026-07-11) — section "Tái hiện Bug".

1. Tạo form mới => User trả lời form và được sync google
2. Vào edit tạo thêm các câu hỏi cho form
3. User vào trả lời lại form trong đó 1 trong các câu hỏi mới được add thêm line user không nhập câu trả lời => Khi sync lên google thì cột không có câu trả lời sẽ để trống
4. Line user tiếp tục trả lời form lần nữa => Result form bị fill lệch cột

## Expected result

- `<Redmine không ghi tường minh mục "Expected">` — suy từ mô tả bug + cách fix: mỗi bản ghi trả lời mới phải được append **bắt đầu từ cột A**, không lệch cột; spreadsheet hiển thị **đủ toàn bộ** câu trả lời (13/13, không phải 4).

## Actual result

- Dòng ghi mới bị **lệch sang phải** (fill lệch cột) khi trên sheet tồn tại dòng có cột A trống → câu trả lời hiển thị sai/thiếu (form có 13 câu trả lời nhưng spreadsheet chỉ hiển thị 4).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #38552 **không có attachment**. Có link Slack thread + link spreadsheet thực tế của KH (xem mục "Bổ sung" phía trên).

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Bug **tái hiện được** — Dev đã cung cấp steps (xem trên).
- Quyết định nghiệp vụ đã chốt (journal 2026-07-09): **luôn write từ cột A**. Trường hợp KH tự sửa sheet làm cột A trống dẫn đến bị **ghi đè** → chấp nhận, coi là lỗi KH. TC nên bám quyết định này, không treat "ghi đè dòng KH sửa" là bug.
