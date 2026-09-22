# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40378 — [29-08-2026][T12013][Salon] Chức năng đặt lịch phỏng vấn salon không hiển thị ngày giờ trống dù còn khung trống, khiến nhiều hội viên (ước tính hơn 100/200 người sau webinar) không đặt lịch được.` |
| Module / Màn hình | Salon・Đặt lịch phỏng vấn (サロン・面談予約) — FA-020. Màn **đặt lịch phía hội viên** (LIFF mở trong ứng dụng LINE): bảng giờ trống (xem tuần), lịch ngày trống (xem tháng), bước chọn nhân viên, bước chọn khoá học, luồng 「Đặt lại」 từ lịch sử đặt. |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: community@10xc.jp
Bot Name: SHIFTAI個別面談LINE

`Tư vấn`
【Về hiện tượng ngày giờ có thể đặt không hiển thị trong đặt lịch phỏng vấn salon】

Cảm ơn quý công ty đã hỗ trợ.
Về 「đặt lịch phỏng vấn salon」(サロン面談予約), mặc dù khung có thể đặt vẫn còn dư dả, nhưng đang phát sinh hiện tượng không có bất kỳ ngày giờ nào có thể đặt được hiển thị trên màn hình phía hội viên, nên muốn nhờ quý công ty xác nhận tình trạng.

`＜Tình trạng phát sinh＞`
Sau khi webinar kết thúc lúc 8/28 19:00〜21:00, khoảng 200 người đã chuyển sang LINE phỏng vấn cá nhân, nhưng chỉ xác nhận được 70 người hoàn tất đặt lịch. Nhiều hội viên đã liên lạc phản ánh rằng 「không hiển thị ngày giờ có thể đặt, không đặt được」.

`＜Nội dung đã xác nhận phía chúng tôi＞`
① Khung đặt lịch vẫn còn dư, không phải tình trạng thiếu khung trống
② Ở màn hình quản trị của đặt lịch phỏng vấn salon, không có thiết lập lọc để ẩn ngày giờ
③ Đã kiểm tra nội dung thiết lập nhưng chưa xác định được nguyên nhân khiến ngày giờ không hiển thị

`＜Nguyên nhân có thể xảy ra＞`
① Lần này, đã thiết lập luồng gửi tin theo bước (ステップ配信 / Step配信) dẫn tới trang đặt lịch phức tạp hơn trước. Muốn xác nhận xem việc phân nhánh, action, thông tin lúc chuyển trang của Step配信 có ảnh hưởng đến việc hiển thị ngày giờ có thể đặt hay không
② Đã tăng số lượng người phụ trách phỏng vấn (面談担当者) đăng ký cho lần này. Muốn xác nhận xem khi số người phụ trách được đăng ký ở quy mô vài chục người có thể xảy ra tình trạng khung đặt lịch bị chậm trễ phản ánh, lỗi hiển thị, giới hạn đăng ký hay không

`＜Điểm muốn xác nhận＞`
① Việc phân nhánh, action của Step配信, hay cách chuyển tới trang đặt lịch có thể khiến ngày giờ có thể đặt không hiển thị hay không ạ
② Khi đăng ký người phụ trách phỏng vấn ở quy mô vài chục người thì có giới hạn, chậm trễ phản ánh, lỗi hiển thị nào không ạ
③ Có tồn tại thiết lập nào khác kiểm soát việc hiển thị ngày giờ như thời gian có thể tiếp nhận (受付可能期間), cài đặt công khai (公開設定), liên kết menu với người phụ trách, phán định đặt lịch đã có (既存予約判定), giới hạn số lượng đặt lịch (予約上限) hay không ạ
④ Có thể xác nhận xem quanh thời điểm 8/28 21:00 có xảy ra tình trạng truy cập tập trung, lỗi hệ thống, xử lý chậm trễ hay không ạ
⑤ Xin hướng dẫn về biện pháp khắc phục có thể thực hiện ở thời điểm hiện tại, cũng như thiết lập/log nên ưu tiên xác nhận

Nếu cần URL form, thông tin tài khoản, ảnh chụp màn hình phát sinh phục vụ điều tra, chúng tôi sẽ chia sẻ ngay. Vì muốn tiến hành hướng dẫn lại cho hội viên, mong quý công ty có thể xác nhận tình trạng sớm trong phạm vi có thể ạ.

Chức năng: Salon・Đặt lịch phỏng vấn (サロン・面談予約)
Thời điểm phản hồi: 2026/08/29 00:31:20

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12013

Nguồn: OEM đã tạo ticket trên Slack — 管理番号 TY-12013

## Steps to reproduce

> ⚠️ Redmine **KHÔNG có section 「Tái hiện bug」** chuẩn. Các bước dưới đây **trích từ mô tả tái hiện của chính khách hàng** ở Journal #134656 (2026-09-05) và Journal #135014 (2026-09-08) — không phải Dev/QA viết.

1. Dùng **iPhone** (Safari / WKWebView — trình duyệt trong ứng dụng LINE) mở LINE bot `SHIFTAI個別相談LINE`.
2. Vào màn **đặt lịch phỏng vấn salon** `SHIFT AI 個別面談` (salon ID `22739`) — salon có **vài chục nhân viên phụ trách** đăng ký.
3. Quan sát bảng ngày giờ có thể đặt (xem tuần / xem tháng).
4. **Tải lại (reload) trang nhiều lần liên tiếp**, xen kẽ chuyển tuần / chuyển tháng.
5. Lặp lại vào thời điểm có nhiều người truy cập đồng thời (ngay sau webinar, ~21:00 ngày 28/8).

## Expected result

- Màn đặt lịch **luôn hiển thị đầy đủ** ngày giờ còn khung trống trong 受付可能期間 (khách cài 10 ngày), **ổn định qua mọi lần tải lại**.
- Nếu nạp dữ liệu thất bại → hội viên phải **thấy thông báo lỗi**, không được hiểu nhầm là hết khung đặt.

## Actual result

- Ngày giờ có thể đặt **lúc hiển thị lúc không hiển thị**: tải lại thì khung giờ hiện ra, tải lại thêm lần nữa thì lại biến mất — lặp đi lặp lại.
- Khi không hiển thị: lịch **rỗng hoàn toàn**, không có thông báo lỗi nào → hội viên hiểu nhầm là hết khung đặt và bỏ cuộc.
- Hệ quả: ~200 người chuyển sang LINE phỏng vấn cá nhân nhưng chỉ **70 người** đặt lịch thành công.
- Khách nhận xét thêm: 「bản thân màn hình đặt lịch hoạt động nặng」 (Journal #135014).
- Sang ngày hôm sau lịch trở lại hiển thị bình thường; nhưng đến **07/09** hiện tượng **vẫn tái diễn** ở màn 「2026年9月7日 - 13日」.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [x] Có video
- [ ] Có log / request-response

- Attachment Redmine: [sc 2026-09-06 10.18.07.jpg](https://redmine.watermelon.vn/attachments/download/30022/sc%202026-09-06%2010.18.07.jpg) — ảnh chụp màn hình xem lịch đặt trên trình duyệt Elme cùng thời điểm lỗi (Journal #134659).
- Ảnh / video khách gửi (Google Drive, test bằng tài khoản `浦野一輝`): https://drive.google.com/drive/folders/1BaPfxgruFdJycAmJVYqHUPRQH6xorBRB?usp=sharing (Journal #134658)
- Ảnh DevTools do human chụp 2026-09-08 (nêu trong báo cáo AI fixbug): payload `listDates` các ngày 14-18/09 mỗi ngày ~500-550 phần tử.

## Ghi chú thêm của Leader

- ⚠️ **Bug KHÔNG tái hiện 100%** — mang tính **ngẫu nhiên, phụ thuộc thời điểm / tải server / thiết bị**. Theo phân tích của Dev, hiện tượng **chỉ xảy ra trên iOS** (Safari / WKWebView chủ động huỷ synchronous XHR khi chạy quá lâu hoặc khi tab bị đưa xuống nền). → TC phải test **lặp lại nhiều lần trên thiết bị thật iPhone**, không kết luận từ 1 lần chạy PASS.
- **Môi trường phát hiện: Production** (bot thật của khách `SHIFTAI個別面談LINE` / `SHIFTAI個別相談LINE`, salon ID `22739`). Đặc tính lỗi phụ thuộc **độ trễ mạng + tải server thật** → theo RULE-08, không kết luận từ local/staging nếu không dựng được lịch nhiều nhân viên + dữ liệu lớn tương đương.
- **Điều kiện tiên quyết để dựng env test**: salon có **vài chục nhân viên phụ trách** + nhiều ca làm → payload `listDates` phình to (~500-550 phần tử/ngày), request nạp giờ trống chạy lâu. Salon ít nhân viên **sẽ không tái hiện được**.
- Truy cập bằng **LIFF trong ứng dụng LINE trên iPhone** mới đúng ca bug gốc. Test trên Chrome desktop / Android không phản ánh đúng hành vi huỷ sync XHR.
- **Đã loại trừ nhánh cấu hình** (khách xác nhận ở Journal #134656): 受付可能期間 = 10 ngày · Cài đặt công khai = ON · **KHÔNG** dùng liên kết menu–người phụ trách · **KHÔNG** dùng kiểm tra lịch đặt hiện có · **KHÔNG** dùng giới hạn số lượt đặt. Cấu hình không thể cho kết quả khác nhau giữa 2 lần tải cách nhau vài giây.
- **Đã loại trừ nhánh Step配信**: エルメサポート trả lời chính thức (Journal #134479) — phân nhánh / action của Step配信 và cách chuyển hướng sang trang đặt lịch **không** gây ra việc ngày có thể đặt không hiển thị.
- ⚠️ **Vấn đề ⑤ (tự động phân bổ nhân viên sai thứ tự ưu tiên) là VẤN ĐỀ KHÁC, KHÔNG thuộc phạm vi fix này.** Đã được WSSサポーター kết luận 03/09 là do phía khách: Google Calendar của nhân viên OA社 đã kín lịch + 2 nhân viên để cài đặt OFF. Khách cũng tự tách bạch ở Journal #134656 mục ⑤. Ticket từng bị **Reject 04/09 với lý do "các staff đã full lịch"** — tức đóng nhầm vấn đề chính bằng kết luận của vấn đề khác — sau đó được mở lại. **TC KHÔNG cần cover luồng auto-assign staff theo ưu tiên.**
- ⚠️ **Có 2 báo cáo AI auto-fixbug trong ticket** — bản đầu (Journal #135579, commit `182f45844f`: tối ưu số truy vấn + dedupe `listDates` + báo lỗi, sửa 3 file gồm 2 file PHP) **đã bị ROLLBACK hoàn toàn khỏi branch**. Bản **hiệu lực** là Journal #135581, commit `c9889e70a1`, **chỉ sửa 1 file JS**. File `03-dev-impact.md` bám theo bản #135581. **Không viết TC theo bản #135579.**
- ⚠️ Dev **chưa bump `config/sns-line.php`** theo quy ước → client có thể còn **cache `booking.js` bản cũ**. Phải xác nhận đội release đã cache-bust trước khi test, nếu không TC sẽ FAIL/PASS sai.
- ⚠️ Rủi ro Dev tự nêu, cần QA đánh giá: bấm nhanh liên tiếp prev/next tuần/tháng nay có thể để **2 request chồng nhau**, response về sau đè lên response trước (trước đây sync XHR nên tuần tự).
- ⚠️ Request bị trình duyệt huỷ **vẫn im lặng** (status = 0, không rơi vào handler `$.ajaxSetup` redirect `/lme/timeout`) — fix chỉ làm request không bị huỷ nữa, **chưa** thêm timeout / retry / banner báo lỗi.
- ⚠️ Phần tính toán phía server **không đổi** — màn hình vẫn nặng như cũ (server dò tối đa 4 tuần cho xem tuần, tới 3 tháng cho xem tháng).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Tài khoản khách | `community@10xc.jp` |
| Bot / LINE | `SHIFTAI個別面談LINE` (nơi khác trong ticket ghi `SHIFTAI個別相談LINE`) |
| Salon (đặt lịch) | `SHIFT AI 個別面談` — **salon ID `22739`** |
| Friend test của khách | `浦野一輝` (khách tự test, có ảnh/video trên Google Drive) |
| Thời điểm lỗi | `2026/08/28 ~21:00` (sau webinar 19:00〜21:00) — tái diễn `2026/09/07 18:00` ở màn tuần `2026年9月7日 - 13日` |
| Cấu hình salon lúc lỗi | 受付可能期間 = 10 ngày · 公開設定 = ON · KHÔNG dùng menu–担当者 · KHÔNG dùng 既存予約判定 · KHÔNG dùng 予約上限 · phương thức đặt: 「指定なし」 tự động phân bổ nhân viên theo ưu tiên |
| Quy mô nhân viên | Vài chục người phụ trách phỏng vấn; payload `listDates` ~500-550 phần tử/ngày |
| Đối chứng | Ngày hôm sau (29/8) lịch hiển thị bình thường → cùng cấu hình, khác kết quả |

## Journal / note từ Redmine (nguyên văn)

**Journal #133974 — AI bug detect Lme — 2026-09-03:**

```
Comment slack ngày 2026-09-03 18:53:47

WSSサポーター
Sau khi kiểm tra log tại thời điểm đặt lịch được xác định và tình trạng của từng nhân viên, chúng tôi xác nhận rằng tất cả nhân viên phía OA đều đang ở trạng thái không thể nhận đặt lịch trong khung giờ đó.

Cụ thể tình trạng như sau.

• OA社_山口：Tại thời điểm đặt lịch, do trên Google Calendar đã đăng ký lịch trình 18:00〜20:00 nên bị loại khỏi danh sách ứng viên đặt lịch
※Lịch trình đó đã bị xóa vào lúc 2026/08/29 23:28:37.
• OA社_西城：Do trên Google Calendar đã đăng ký lịch trình 18:00〜20:00 nên bị loại khỏi danh sách ứng viên đặt lịch
• OA社_五十：Cài đặt nhân viên đang ở trạng thái OFF
• OA社_横川：Cài đặt nhân viên đang ở trạng thái OFF
• OA社_鈴木：Do trên Google Calendar đã đăng ký lịch trình 09:00〜23:55 nên bị loại khỏi danh sách ứng viên đặt lịch
• OA社_小原：Do trên Google Calendar đã đăng ký lịch trình 13:00〜23:59 nên bị loại khỏi danh sách ứng viên đặt lịch
```

**Journal #134120 — AI LME Fix bug — 2026-09-04:**

```
[Dashboard] Đổi trạng thái: Chờ review → Reject
Lý do: các staff đã full lịch
```

**Journal #134479 — AI bug detect Lme — 2026-09-05:**

```
Comment slack ngày 2026-09-05 14:40:00

沖原 裕樹（エルメサポート）
Cảm ơn quý công ty đã hỗ trợ.

＞① Có khả năng việc phân nhánh/action của step配信 hoặc cách chuyển hướng sang trang đặt lịch làm cho ngày giờ có thể đặt không hiển thị không?
⇒Bản thân việc phân nhánh của step配信 hay cách chuyển hướng sang trang đặt lịch không gây ra việc ngày có thể đặt không hiển thị.

＞② Có giới hạn số lượng, độ trễ phản ánh, lỗi hiển thị nào khi đăng ký người phụ trách phỏng vấn quy mô vài chục người không?
⇒Hiện tại không có báo cáo nào về độ trễ hay lỗi như vậy.

＞③ Có tồn tại các thiết lập riêng để kiểm soát việc hiển thị lịch như thời gian tiếp nhận, cài đặt công khai, liên kết menu-người phụ trách, phán định đặt lịch đã tồn tại, giới hạn số lượng đặt lịch không?
⇒Các chức năng đó có tồn tại trong エルメ.
Về mục thiết lập của từng chức năng, xin vui lòng tham khảo manual dưới đây.

Khoảng thời gian có thể tiếp nhận：https://lme.jp/manual/can_not_resarvation/#toc11
Cài đặt công khai：https://lme.jp/manual/can_not_resarvation/#toc2
Liên kết menu và người phụ trách：https://lme.jp/manual/salon/#toc24
Phán định đặt lịch đã tồn tại：https://lme.jp/manual/salon/#toc39
Giới hạn số lượng đặt lịch：https://lme.jp/manual/salon/#toc39

＞④ Có thể xác nhận xem vào khoảng 8/28 21:00 có xảy ra tình trạng truy cập tập trung, lỗi hệ thống, xử lý chậm trễ nào không?
⇒Không có phát sinh đặc biệt nào như vậy.
```

**Journal #134656 — AI bug detect Lme — 2026-09-05:** ★ **bằng chứng tái hiện quan trọng nhất**

```
Comment slack ngày 2026-09-05 22:34:00

お客様
Cảm ơn quý công ty đã hỗ trợ.
Cảm ơn đã kiểm tra chi tiết giúp chúng tôi. Xin được bổ sung thêm về từng mục.

① Về step gửi tin (step delivery)
Chúng tôi đã hiểu rằng bản thân cách phân nhánh hay cách chuyển đến trang đặt lịch không phải là nguyên nhân khiến ngày giờ có thể đặt không hiển thị.

② Về số lượng người phụ trách và việc hiển thị lịch
Chúng tôi đã hiểu rằng không có báo cáo về độ trễ hay lỗi phát sinh do số lượng người phụ trách.

Tuy nhiên, vào khoảng 21h ngày 28/8, chính điện thoại của tôi cũng đã xác nhận hiện tượng ngày giờ có thể đặt lịch lúc hiển thị lúc không hiển thị. Khi tải lại trang thì khung giờ hiện ra, nhưng sau đó tải lại thêm lần nữa thì lại biến mất — trong quá trình kiểm tra lặp đi lặp lại, việc hiển thị cứ thay đổi như vậy.

Lần này, điều chúng tôi muốn nhờ điều tra nhất chính là nguyên nhân xảy ra hiện tượng này.

③ Về cài đặt liên quan đến hiển thị lịch
Cài đặt tại thời điểm đó như sau.

・Thời gian có thể tiếp nhận：đã đặt là 10 ngày, nhưng trong khoảng thời gian đó ngày giờ lúc hiển thị lúc không hiển thị
・Cài đặt công khai：đã để ON (bật)
・Liên kết giữa menu và người phụ trách：bản thân chức năng menu không được sử dụng
・Kiểm tra lịch đặt hiện có・Giới hạn số lượt đặt：tại thời điểm đó chưa sử dụng. Sắp tới chúng tôi đang cân nhắc sử dụng

④ Về hiện tượng xảy ra vào khoảng 21h ngày 28/8
Chúng tôi được biết là không xảy ra tình trạng truy cập tập trung, lỗi hệ thống hay xử lý bị trễ, nhưng việc chuyển đổi hiển thị/không hiển thị như trên thì chúng tôi đã thực tế xác nhận được.

Sau đó, đến ngày hôm sau lịch đã trở lại trạng thái hiển thị bình thường nên chúng tôi đã hướng dẫn lại việc đặt lịch cho hội viên.

Chúng tôi muốn nhờ quý công ty kiểm tra dựa trên tình huống và log tại thời điểm đó, xem đây là hiện tượng chỉ xảy ra tạm thời, hay là hành vi có thể xảy ra do đặc tính hệ thống hoặc điều kiện cụ thể nào đó.

⑤ Về việc tự động phân bổ nhân viên
Chúng tôi đã hiểu rằng việc nhân viên bên công ty OA không nhận được lịch đặt là do nguyên nhân từ cài đặt đặt lịch và tình trạng Google Calendar bên phía chúng tôi. Xin lỗi vì đã làm phiền quý công ty kiểm tra.

Đây là một hiện tượng khác, không liên quan đến việc lịch đặt lúc hiển thị lúc không hiển thị vào ngày 28/8.
Chúng tôi hiểu rằng câu trả lời cho mục ⑤ lần này là về nội dung tự động phân bổ nhân viên, nên mong quý công ty trả lời riêng về việc lịch đặt hiển thị không ổn định.

Nếu cần thêm thông tin để điều tra, xin vui lòng chỉ rõ những mục cần thiết.
```

**Journal #134658 / #134659 — AI bug detect Lme — 2026-09-06:**

```
Comment slack ngày 2026-09-06 10:16:00
お客様
Thực tế đang ở tình trạng không thể đặt lịch như thế này.
Tôi đang test bằng tài khoản cá nhân của mình tên là 浦野一輝.
https://drive.google.com/drive/folders/1BaPfxgruFdJycAmJVYqHUPRQH6xorBRB?usp=sharing

Comment slack ngày 2026-09-06 10:18:00
お客様
Cùng thời điểm đó, khi bấm vào xem lịch đặt trên trình duyệt của Elme thì hiển thị như thế này.
```

**Journal #135014 — AI bug detect Lme — 2026-09-08:** ★ **xác nhận VẪN tái diễn**

```
Comment slack ngày 2026-09-07 18:03:12

沖原裕樹
・LINE：SHIFTAI個別相談LINE
・Đặt lịch salon：SHIFT AI 個別面談

Ở đây, có vẻ như màn hình đặt lịch 「2026年9月7日 - 13日」 có lúc hiển thị và có lúc không hiển thị.
Do bản thân màn hình đặt lịch hoạt động nặng, liệu có phải đang xảy ra lỗi gì đó không?
```
