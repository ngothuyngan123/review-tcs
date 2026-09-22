# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40806 — [10-09-2026][T12116][Booking Event] Khách báo ít nhất 2 người đăng ký sự kiện ngày 9/9 nói đã đăng ký nhưng không có xác nhận, hệ thống không lưu lịch sử đăng ký; khi thử lại real-time phát hiện thao tác bấm nút quay lại gây lỗi đăng ký bất thường.` |
| Module / Màn hình | Đặt lịch sự kiện (イベント予約 / Event Booking — FA-021) — trang đăng ký sự kiện trên LIFF (bước nhập → màn xác nhận → hoàn tất) |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: schuzlmither@gmail.com
Bot Name: マリエ｜CommuCom

Khi nhận đăng ký sự kiện tổ chức vào ngày 9/9, chỉ tính riêng những gì đã biết cũng có 2 người liên hệ nói rằng 「申し込んだが連絡がこない」 (đã đăng ký nhưng không nhận được liên lạc).
Khi kiểm tra thì không thấy tên người đó trong danh sách đăng ký (申込み一覧), không thể xác nhận được lịch sử đăng ký (申込履歴).

Với 1 người, tôi đã vừa trao đổi qua chat theo thời gian thực vừa nhờ họ thao tác đăng ký, thì phát hiện có vẻ có lỗi thao tác: khi bấm 「もどる」 (quay lại) thì lại đăng ký được？
Không rõ ngoài 2 người đã tự liên hệ này có ai gặp tình trạng tương tự hay không, nhưng mong quý công ty giải thích rõ nguyên nhân lỗi nêu trên.

Chức năng: Đặt lịch sự kiện (イベント予約)
Thời điểm phản hồi: 2026/09/10 09:15:34
Ảnh 1: data/screenshots/T12116_0.jpg

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12116

Ticket Slack do OEM đăng — 管理番号 TY-12116
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1789022520536439

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" riêng. Các bước dưới đây trích từ mô tả hiện tượng của khách trong Journal #135615 / #135618 — chưa được QA/Dev tái hiện thành công. -->

1. Từ LINE, mở trang đăng ký sự kiện (LIFF) của sự kiện 「令和コミュ入門セミナー」.
2. Nhập đầy đủ thông tin đăng ký.
3. Bấm nút đăng ký / xác nhận (「申し込む」).
4. Màn hình hiển thị 「ありがとうございます」.
5. KHÔNG bấm 「もどる」 → không xuất hiện 「リクエストお待ちください」, đơn đăng ký không được ghi nhận.
6. Bấm 「もどる」 → lúc này 「リクエストお待ちください」 mới xuất hiện, đơn đăng ký được phản ánh (trường hợp friend 「平野れみ」).

## Expected result

- Sau khi nhập đầy đủ thông tin và hoàn tất thao tác đăng ký, đơn phải được ghi nhận vào hệ thống và hiển thị trong danh sách đăng ký (申込み一覧) / lịch sử đăng ký (申込履歴).
- Người đăng ký phải nhận được tin nhắn xác nhận đã tiếp nhận đăng ký.

## Actual result

- Tên người đăng ký KHÔNG có trong danh sách đăng ký, không xác nhận được lịch sử đăng ký.
- KHÔNG ai trong số các friend bị ảnh hưởng nhận được tin nhắn xác nhận tiếp nhận đăng ký.
- Chỉ khi bấm 「もどる」 thì đơn mới được ghi nhận (ít nhất với 1 friend).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.jpg — https://redmine.watermelon.vn/attachments/download/30293/screenshot1.jpg

## Ghi chú thêm của Leader

- ⚠️ **Bug KHÔNG tái hiện được** — cả khách hàng lẫn phía công ty đều chưa tái hiện được (Journal #135615, #135618). Dev cũng ghi rõ ở mục 6 VERIFY: "CHƯA tái hiện được trên thiết bị thật: container không có iPhone/LINE". TCs nên tập trung verify **cách fix + regression impact**, không phụ thuộc vào việc tái hiện bug gốc.
- ⚠️ **Tần suất lỗi không phải 100%** — khách ghi rõ "có người gặp, có người không gặp" (「同様の方がいるかはわかりません」). Số người báo lỗi tăng dần: 2 người (10/09) → 4 người (10/09 chiều) → thêm makiko (11/09) = **5 friend**.
- **Môi trường phát hiện: Production** — bot thật của khách OEM (マリエ｜CommuCom), sự kiện thật ngày 09/09.
- **Điều kiện tiên quyết để test (fixture quan trọng)**: sự kiện phải có **≥ 10 mục thông tin khách hàng (friend info)** + nội dung đầu trang/mô tả đủ dài để tổng chiều cao trang **≥ 2 lần chiều cao viewport** — đây là điều kiện tạo ra scroll thật, gốc của bug.
- **Thiết bị**: bug chỉ xảy ra trên **LINE in-app browser (WebView) của iOS + Android**, chưa tái hiện trên desktop.
- ⚠️ **ĐỔI HÀNH VI sau fix (Dev cảnh báo QA)**: URL không còn thêm `#top` → bấm **nút Back của LINE** sẽ **THOÁT LIFF** thay vì chỉ cuộn trang như trước.
- **Kết luận từ log production (Dev)**: KHÔNG có dữ liệu nào bị mất — request đăng ký của các khách bị ảnh hưởng **chưa bao giờ tới server** (access log 3 ngày: 0 request `/ajax/booking-event/payment` từ IP của họ). App log 08/09 (12GB): payment event booking error = 0, TokenMismatch = 0.
- **Root cause là giả thuyết khớp nhất với dữ kiện, chưa phải bằng chứng trực tiếp** (Dev tự ghi ở mục TỰ REVIEW). Beacon lỗi JS được thêm chính là để lần sau có bằng chứng trực tiếp.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `82152` |
| booking_event_id | `40574` |
| Sự kiện | `令和コミュ入門セミナー` — tổ chức ngày 2026/09/09 |
| Friend bị lỗi (5 người) | `yukinko — line_user_id 21771991` · `kana — 26997736` · `Mayo — 49047405` · `平野れみ — 13073264` · `makiko (chưa có ID)` |
| Đối tượng cấu hình | b_slot `529452` — `number_people = null`, `date_deadline = 2026-09-09 23:59`, `type_times_booking = 1` |
| Thời điểm lỗi | `2026/09/08 09:26:07` (yukinko mở form, không có POST payment) · sự kiện `2026/09/09` |
| Đối chứng | `u_code 3Ak3B03J7r` — vào form 05/09 không submit được, tới 09/09 mất **5 phút 06 giây** sau khi form render mới bấm được nút → đăng ký thành công. 6/6 đơn có thật đều tạo thành công và gửi action `21212607`. |

## Journal / note từ Redmine (nguyên văn)

**Journal #135615 — Ngô Thúy Ngần — 2026-09-10:**

```
bot_id: 82152
booking_event_id: 40574
Check 4 friend:
yukinko: 21771991
kana: 26997736
Mayo: 49047405
平野れみ: 13073264

Hiện tượng của khách:
Sau khi nhập đầy đủ thông tin và nhấn nút đăng ký, màn hình hiển thị 'ありがとうございます'. Nếu không nhấn back【もどる】 thì sẽ không xuất hiện 'リクエストお待ちください'.

Ngoài ra, tất cả những người này đều cho biết không nhận được tin nhắn xác nhận rằng hệ thống đã tiếp nhận đăng ký.

Đối với người dùng 「平野れみ」 nêu trên, có vẻ như sau khi nhấn back thì đơn đăng ký mới được phản ánh thành công.

Hiện tượng này dường như có người gặp, có người không gặp, và phía chúng tôi hiện vẫn chưa tái hiện được lỗi.
```

**Journal #135618 — AI bug detect Lme — 2026-09-10:**

```
Comment slack ngày 2026-09-10 14:50:00

お客様
Cảm ơn đã liên hệ
・Xin cho biết tên quản lý của sự kiện đặt chỗ đang gặp vấn đề.
令和コミュ入門セミナー
・Xin cho biết tên friend của 2 người không đặt chỗ được.
yukinko
kana
Mayo
平野れみ
Ngoài ra có thêm 2 người khác cũng báo cáo cùng hiện tượng, hiện tổng cộng là 4 người.

・Cả 2 người đều gặp cùng triệu chứng không đặt chỗ được phải không ạ？
Người liên quan cho biết「全部入力して申し込む押すとありがとうございますがでて【もどる】をタッチしないとリクエストお待ちくださいがでてくる」.
Không ai trong số họ nhận được thông báo là đã tiếp nhận.
Chị 「平野れみ」 nói trên có vẻ khi bấm 【もどる】thì đăng ký đã được ghi nhận.

Có vẻ có người bị và có người không bị triệu chứng này, phía chúng tôi chưa xác nhận tái hiện được.
```

**Journal #136155 — AI bug detect Lme — 2026-09-11:**

```
Comment slack ngày 2026-09-11 20:55:00

お客様
Chúng tôi xin thông báo là người dưới đây cũng gặp phải hiện tượng tương tự.
makiko

Ngoài ra, có khả năng còn có người khác gặp phải nữa nên mong quý công ty điều tra giúp.
```
