# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40734 — [09-09-2026][T12108][Form] Khách báo dữ liệu form không được đồng bộ vào Google Spreadsheet liên kết dù đã cài đặt đúng, hiện tượng lặp lại nhiều lần ở các form khác nhau.` |
| Module / Màn hình | Form — Tạo form (フォーム作成) › Liên kết Google Spreadsheet (Googleスプレッドシート連携); job đồng bộ câu trả lời form lên spreadsheet |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: nakamura@green-i.co.jp
Bot Name: BIZFIT

Tôi liên hệ vì gặp sự cố liên quan đến 「Googleスプレッドシート連携」 (liên kết Google Spreadsheet) trong chức năng tạo form.

Dù đã hoàn tất thiết lập liên kết với Google Spreadsheet, dữ liệu gửi từ form không được phản ánh vào spreadsheet liên kết.

Trước đây cũng từng xảy ra hiện tượng tương tự và đã xử lý khôi phục một lần, nhưng hiện tượng tương tự lại tiếp tục lặp lại ở một form khác.

▼Cách khôi phục đã thực hiện trước đây
━━━━━━━━━━━
■Cách khôi phục spreadsheet

Nếu thông tin không còn được phản ánh đúng vào sheet, vui lòng thực hiện khôi phục theo các bước sau.

① Nhấn vào dấu「＋」ở góc dưới bên trái spreadsheet để tạo sheet mới.
② Nhấn chuột phải vào sheet đang chứa thông tin hiện tại và xóa sheet đó.
③ Thêm câu trả lời mới
④ Sau khi thực hiện thao tác trên, các câu trả lời trước đó cũng sẽ được phản ánh.
━━━━━━━━━━━

Anh/chị có thể cho tôi biết nguyên nhân gốc rễ và cách giải quyết, bao gồm cả biện pháp phòng ngừa tái phát trong tương lai không ạ?

【詳細情報】(Thông tin chi tiết)
Để phục vụ việc điều tra sự cố, tôi xin ghi rõ các thông tin cần thiết như sau.

Thời điểm phát sinh：2026年9月9日 (2026/09/09)

Tên form đối tượng / URL：
BW申し込み＞9/17(木)BW19申込

Rất xin lỗi vì đã làm phiền lúc anh/chị đang bận, mong anh/chị xác nhận và hỗ trợ xử lý giúp tôi.

Chức năng: Tạo form (フォーム作成)
Thời điểm phản hồi: 2026/09/09 09:51:57

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12108

Ticket Slack do OEM đăng — 管理番号 TY-12108
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C1B4XCS72
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788921711488229

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — khách chỉ mô tả hiện tượng, không đưa bước tái hiện.
     Điều kiện tái hiện dưới đây trích từ Journal #136168 (Dev Thanh Duy Nguyen, mục 1 Nguyên nhân) — KHÔNG phải do khách cung cấp. -->

*(Khách không cung cấp bước tái hiện. Điều kiện tái hiện do Dev xác nhận ở Journal #136168:)*

1. Có form đã liên kết Google Spreadsheet và **sheet của trang đã có sẵn dữ liệu** (đã đồng bộ ít nhất 1 lần trước đó).
2. LINE user mở form rồi bấm gửi mà **không nhập câu trả lời nào**.
3. Chờ job đồng bộ chạy → mở spreadsheet kiểm tra dòng tương ứng.

> ⚠️ Chỉ xảy ra khi sheet **đã có sẵn dữ liệu**. Sheet còn trống thì vẫn ghi bình thường — đây là lý do cách khôi phục của khách (xóa sheet, tạo sheet mới) làm dữ liệu hiện lại đủ.

## Expected result

*(Không có trong Redmine — khách không ghi mục "Kết quả mong đợi" riêng.)*

## Actual result

*(Không có trong Redmine — khách không ghi mục "Kết quả thực tế" riêng; hiện tượng nằm trong phần Mô tả bug ở trên.)*

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- bug_form_answer_sync_sheet_inconsistency.md (6607 bytes) — https://redmine.watermelon.vn/attachments/download/30368/bug_form_answer_sync_sheet_inconsistency.md

## Ghi chú thêm của Leader

- ⚠️ **Bug không có bước tái hiện chính thức từ khách** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- **Điều kiện tiên quyết bắt buộc để tái hiện**: sheet của trang **đã có sẵn dữ liệu**. Sheet trống → không tái hiện được (job vẫn ghi đúng).
- **Không phải lỗi 100% mọi câu trả lời** — chỉ dính bản ghi mà phần dữ liệu không chứa câu trả lời thật (mở form bấm gửi không nhập gì).
- **Dữ liệu đã mất không tự khôi phục**: record bị bỏ qua vẫn bị đánh dấu "đã đồng bộ" nên job không ghi lại lần nữa → cần bước rà soát + khôi phục riêng (RULE-04).
- **Hiện tượng lặp lại ở nhiều form khác nhau** → phạm vi rà soát có thể vượt ngoài 1 form khách báo.
- Môi trường phát hiện: **Production** (bot BIZFIT của khách, spreadsheet Google thật).
- Đã yêu cầu khách cấp quyền edit spreadsheet cho `css.wss.2025@gmail.com` để xem lịch sử chỉnh sửa (Journal #135315, #135515) — khách xác nhận đã cấp (Journal #135553).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — Bot Name: BIZFIT>` |
| Tài khoản khách | `nakamura@green-i.co.jp` |
| Friend | `中村 和之` (tên hiển thị trên spreadsheet) |
| Đối tượng cấu hình | Form `BW申し込み＞9/17(木)BW19申込` — form **228620** (Dev nêu ở Journal #136168) |
| Thời điểm lỗi | Câu trả lời `2026/08/19 10:47` (2026.08.19(水) 10:47) — record mẫu bị bỏ qua |
| Thời điểm khách báo | `2026/09/09 09:51:57` |
| Đối chứng | Trả lời form có nhập nội dung → vẫn lên sheet bình thường; sheet còn trống → ghi đủ cả dữ liệu cũ |

## Journal / note từ Redmine (nguyên văn)

**Journal #135315 — AI bug detect Lme — 2026-09-09:**

```
Comment slack ngày 2026-09-09 12:08:08

WSSサポーター
Xin lỗi vì sự bất tiện, nhưng để điều tra, quý khách có thể chia sẻ giúp 2 điểm sau được không ạ.
・Thông tin về câu trả lời form chưa được liên kết vào Google Spreadsheet (dữ liệu câu trả lời tương ứng)
・Để xác nhận lịch sử chỉnh sửa, cấp quyền chỉnh sửa cho css.wss.2025@gmail.com vào spreadsheet đối tượng
```

**Journal #135515 — AI bug detect Lme — 2026-09-09:**

```
Comment slack ngày 2026-09-09 19:00:00

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã sử dụng dịch vụ.

Xin lỗi vì đã làm phiền, nhưng mong quý khách cho biết các thông tin sau đây.

・Tên friend chưa được phản ánh vào spreadsheet
・Thời điểm trả lời của friend chưa được phản ánh vào spreadsheet

Ngoài ra, để phục vụ điều tra chi tiết, quý khách có thể cấp quyền chỉnh sửa spreadsheet của form 「9/17(木)BW19申込」 mà quý khách đã liên hệ, cho địa chỉ email dưới đây được không ạ？

css.wss.2025@gmail.com

Rất mong quý khách thông cảm và hợp tác.
```

**Journal #135553 — AI bug detect Lme — 2026-09-10:**

```
Comment slack ngày 2026-09-10 11:29:00

お客様
Cảm ơn quý khách đã sử dụng dịch vụ.

・Tên friend không được phản ánh vào spreadsheet
→中村 和之

・Thời gian trả lời của friend không được phản ánh vào spreadsheet
→2026.08.19(水) 10:47

Chúng tôi nghĩ rằng quyền truy cập đã được cấp, nên mong quý khách kiểm tra giúp.
```

**Journal #136168 — Thanh Duy Nguyen — 2026-09-12:**

```
1. Nguyên nhân
   - Khách mở form rồi bấm gửi mà không nhập câu trả lời nào thì job hiểu nhầm là "câu trả lời này không thuộc trang nào", nên bỏ qua luôn, không ghi dòng nào lên Google Sheet.
   - Chỉ xảy ra khi sheet đã có sẵn dữ liệu. Sheet còn trống thì vẫn ghi bình thường, nên khách xoá sheet tạo lại thì thấy dữ liệu hiện ra đủ, đúng như khách mô tả. Record bị bỏ qua vẫn bị đánh dấu là "đã đồng bộ" nên job không ghi lại lần nữa (record mẫu: 2026-08-19 10:47, form 228620).

2. Cách fix
   - Sửa lại điều kiện: chỉ cần câu trả lời thuộc trang đang ghi là tạo 1 dòng trên sheet, kể cả khi khách không nhập nội dung nào. Dòng đó có 回答ID, thời gian, tên LINE user, các cột câu hỏi để trống - giống hệt cách sheet trống đang ghi.
   - Thêm mã câu trả lời vào log để lần sau tra được record nào bị bỏ qua.
```

*(Phần mục 3 → 5 của Journal #136168 đã map đầy đủ vào `03-dev-impact.md`.)*
