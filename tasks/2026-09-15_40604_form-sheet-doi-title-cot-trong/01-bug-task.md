# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40604 — [06-09-2026][30251][Form] Khách báo cột K (参加希望日時) trong Google Sheets liên kết với form bị trống ở một số câu trả lời cũ dù dữ liệu vẫn lưu đúng trong hệ thống, hỏi cách đồng bộ lại.` |
| Module / Màn hình | `Form — liên kết câu trả lời form với Google Spreadsheet (フォーム回答 Google スプレッドシート連携)` |

## Mô tả bug (bản dịch tiếng Việt)

OEM ĐÃ TẠO TICKET SLACK

User: jan29yudai@gmail.com
Bot Name: Yudai | ボディメイクコーチ

Đang liên kết câu trả lời form của L Message với Google Spreadsheet.
Trong danh sách câu trả lời, câu trả lời 「参加希望日時」 được lưu bình thường, nhưng trong Google Spreadsheet chỉ có một số người trả lời ở giữa bị trống cột tương ứng（K列）.
Không có filter hay ẩn dòng, đã tạo lại sheet và thử trả lời test nhưng cột K của các câu trả lời cũ vẫn không được phản ánh.
Anh/chị có thể kiểm tra giúp có cách nào để đồng bộ lại bao gồm cả câu trả lời cũ, hoặc khả năng đây là lỗi liên kết không ạ

Thời điểm phản hồi: 2026/09/06 15:40:00

Nội dung từ Slack (OEM) — dịch:
> Đang liên kết câu trả lời form của L Message với Google Spreadsheet.
> Ở danh sách câu trả lời (回答一覧) thì câu trả lời 「参加希望日時」 được lưu bình thường, nhưng trên Google Spreadsheet chỉ những người trả lời ở giữa mới bị trống cột tương ứng (K列).
> Không có filter, không ẩn dòng; đã tạo lại sheet và cũng đã trả lời test, nhưng cột K của các câu trả lời cũ vẫn không được phản ánh — nhờ điều tra nguyên nhân.
>
> Form đã tạo: オンライン授業申込 (Đăng ký lớp học online)

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=30251
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BVD14FCHG
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788743641317349

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — để trống, xem Ghi chú thêm của Leader. -->

## Expected result

- *(Redmine không có mục "Kết quả mong đợi" — dưới đây suy từ mô tả của KH, cần Leader xác nhận)* Trên Google Spreadsheet liên kết với form, cột 参加希望日時 (K列) có dữ liệu ở **tất cả** câu trả lời, kể cả câu trả lời cũ, giống như dữ liệu hiển thị ở màn 回答一覧.

## Actual result

- *(suy từ mô tả của KH)* Cột K (参加希望日時) bị **trống ở một số câu trả lời cũ** (nhóm người trả lời ở giữa) trên Spreadsheet, dù dữ liệu vẫn lưu và hiển thị đúng ở màn danh sách câu trả lời trong LME. Tạo lại sheet để sync lại từ đầu vẫn trống.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40604 không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không có section "Tái hiện bug" trong Redmine** (Steps trống) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Điều kiện tiên quyết dựng env: form đã bật liên kết Google Spreadsheet, có **câu trả lời cũ được lưu trước khi đổi title câu hỏi**, rồi **đổi title 1 câu hỏi** và cho **sync lại từ đầu** (sheet rỗng / chưa có cột 回答ID).
- Chỉ xảy ra ở **nhánh sync lại từ đầu** (sheet mới tạo / chưa có cột 回答ID) — nhánh append dòng mới không bị (theo mục 1 file 03). Vì vậy KH "tạo lại sheet" vẫn thấy trống.
- Không phải lỗi 100% mọi câu trả lời — chỉ các câu trả lời có `name` (title cũ) khác title hiện tại của form_detail.
- Môi trường phát hiện: **Production** (bot KH thật, user jan29yudai@gmail.com).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `195346` |
| Friend | `<không có — bug ở tầng sync sheet, không gắn 1 friend cụ thể>` |
| Đối tượng cấu hình | Form `オンライン授業申込` — `form_id: 235311`; câu hỏi lỗi: `参加希望日時` (cột K trên sheet) |
| Link Spreadsheet liên kết | https://docs.google.com/spreadsheets/d/1tni-WTE96KfE7XVL0EdHm5ovhOWF8rQTe7nwadVVAuM/edit?gid=1822985366#gid=1822985366 |
| Thời điểm lỗi | `2026/09/06 15:40:00` (thời điểm KH phản hồi) |
| Đối chứng | Câu trả lời mới (test answer sau khi tạo lại sheet) vẫn ra đúng cột; chỉ câu trả lời cũ trống |

## Journal / note từ Redmine (nguyên văn)

**Journal #134690 — Ngô Thúy Ngần — 2026-09-07:**

```
bot_id: 195346
form_id: 235311
Link spread: https://docs.google.com/spreadsheets/d/1tni-WTE96KfE7XVL0EdHm5ovhOWF8rQTe7nwadVVAuM/edit?gid=1822985366#gid=1822985366
```

**Journal #136197 — Thanh Duy Nguyen — 2026-09-12:**

```
Vấn đề: Khi form_detail thay đổi title, trường hợp sync lại mới, các câu trả lời cũ đang lưu title cũ bị sync lỗi không map được.
=> Sửa lại map câu trả lời với header theo form_detail_id trước, nếu không có form_detail_id thì map theo title như logic hiện tại. (Vì có trường hợp câu trả lời từ lâu rồi ko có form_detail_id trong data)

VD data:
[ { "name": "お名前（ニックネーム可）", "type": "name", "value": "あかつき", "note": "", "point": 0, "page": "198118", "pageName": "スタートページ", "form_detail_id": "11869316" }, { "name": "生年月日", "type": "date_time", "value": { "date": "1960/04/27" }, "note": "", "point": 0, "page": "198118", "pageName": "スタートページ", "form_detail_id": "11869317" }, { "name": "性別", "type": "select2_5", "value": "男性", "note": "", "point": 0, "page": "198118", "pageName": "スタートページ", "form_detail_id": "11869320" }, { "name": "お悩み", "type": "text_8", "value": "お金の苦労が絶えず、肉体的に辛い仕事をせざるを得ない。\nこの苦労から早く抜け出したい。", "note": "", "point": 0, "page": "198118", "pageName": "スタートページ", "form_detail_id": "11869321" }, { "name": "叶えたい未来", "type": "text_8", "value": "色々と助けてもらった兄妹に恩返しをしたい。", "note": "", "point": 0, "page": "198118", "pageName": "スタートページ", "form_detail_id": "11869322" } ]
```

<!-- Journal #134694, #134698 là comment support gửi KH (không có nội dung điều tra) → bỏ qua. Journal #136470 là "Đánh giá ảnh hưởng" → xem 03-dev-impact.md. -->
