# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40563 — [05-09-2026] [TY-12058] [Richmenu] Rich menu không biến mất sau khi ngắt kết nối tài khoản LME` |
| Module / Màn hình | `Richmenu (リッチメニュー) — LINE公式アカウント入れ替え機能 (đổi LOA) / màn 接続設定 · màn chi tiết hợp đồng (接続解除)` |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12058
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788590263198559
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12058

Mã quản lý: TY-12058
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BV6S979T4
Địa chỉ: mirei.yada.pianoroom@gmail.com
Tên LOA (LOA名): 発達支援ピアノ講師認定講座
Phụ trách (担当): 沖原
Công cụ (ツール): リンク (link)

**Nội dung liên hệ (問い合わせ内容):**

Sau khi thực hiện ngắt kết nối (接続解除), rich menu vốn được hiển thị từ エルメ (LME) vẫn không biến mất và tiếp tục hiển thị với friend.

Tài khoản エルメ đã kết nối trước đây: mirei.yada.pianoroom@gmail.com
LINE ID: @481zcgwm
Channel ID: 2011211317
Channel secret: `<có trên Redmine #40563 — không chép vào repo>`

---

**Diễn biến làm rõ qua trao đổi với CS (xem Journal bên dưới):**

- Khách hàng **KHÔNG** thực hiện thao tác 接続解除 (hủy kết nối) từ màn hình chi tiết hợp đồng. Thứ khách hàng đã làm là **「LINE公式アカウント入れ替え機能」** (chức năng đổi LINE Official Account) — đổi LOA đang kết nối với エルメ từ `@481zcgwm` (cũ) sang `@019nxejl` (mới).
- Sau khi đổi LOA, rich menu do エルメ đẩy lên OA **cũ** `@481zcgwm` vẫn còn hiển thị với friend của OA cũ, dù OA cũ không còn kết nối với エルメ.
- Khách hàng thử vào màn hủy kết nối thì bị chặn: không tick được ô 「リッチメニューを削除した」 (đã xóa rich menu) nên không đi tiếp được bước sau.
- CS ban đầu hướng dẫn "rich menu sẽ tự ẩn trong vòng 24h sau khi hủy kết nối" và nghi ngờ rich menu được set từ LINE Official Account Manager — khách hàng xác nhận LINE Official Account Manager **không** có thiết lập rich menu, và OA cũng **không** kết nối công cụ nào khác ngoài エルメ.

## Steps to reproduce

<!-- Redmine KHÔNG có Section "Tái hiện bug" — ticket là inquiry từ khách hàng qua Slack, không có step tái hiện chính thức. Step dưới đây suy từ diễn biến trao đổi + đánh giá ảnh hưởng của Dev (file 03), CẦN Leader xác nhận trước khi dùng làm chuẩn. -->

1. Có 1 bot エルメ đang kết nối LOA cũ `@481zcgwm`, trên OA cũ đã đẩy rich menu từ エルメ và friend đang thấy rich menu đó.
2. Dùng chức năng 「LINE公式アカウント入れ替え機能」 để đổi LOA kết nối từ `@481zcgwm` sang OA mới `@019nxejl`.
3. Đợi job `ChangeBotJob` chạy hết các bước.
4. Mở LINE bằng tài khoản friend của OA **cũ** `@481zcgwm` → xem rich menu.

## Expected result

- Rich menu do エルメ đẩy lên OA cũ `@481zcgwm` bị **xóa thật** khỏi OA cũ → friend của OA cũ không còn thấy rich menu.
- Rich menu được dựng lại đầy đủ trên OA mới `@019nxejl`.

## Actual result

- Rich menu trên OA cũ `@481zcgwm` **không bị xóa**, friend của OA cũ vẫn tiếp tục thấy rich menu (kéo dài nhiều ngày, quá 24h).
- Log production xác nhận `#deleteRichMenu ... status=404` — 3/3 lệnh xóa rich menu đều trả 404 (xem Journal #135570).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log production `#deleteRichMenu status=404` ở Journal #135570 (không phải file attachment; Redmine attachments = 0).

## Ghi chú thêm của Leader

- **Môi trường phát hiện: Production** (tài khoản khách hàng thật, OEM report qua Slack).
- ⚠️ **Bug không có Section "Tái hiện bug" trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03) + log production 404. TCs nên tập trung verify **cách fix** (token cũ vs token mới khi xóa richmenu) + **regression impact** của job `ChangeBotJob`.
- ⚠️ **Nhầm lẫn thuật ngữ trong ticket**: tiêu đề ticket ghi "ngắt kết nối" (接続解除) nhưng thao tác thực tế của khách là **đổi LOA** (LINE公式アカウント入れ替え). Đây là 2 flow khác nhau — TC phải bám flow **đổi LOA**, không phải flow hủy kết nối.
- ⚠️ Tài khoản khách đang ở **gói Free**, mà theo CS thì 「LINE公式アカウント入れ替え機能」 chỉ dùng được với gói trả phí — khách nói từng đổi khi tính năng đang được miễn phí. → Cần làm rõ với Dev/CS: điều kiện plan để dùng chức năng đổi LOA, và có cần TC cho nhánh phân quyền plan hay không.
- ⚠️ Ràng buộc UI liên quan: màn 接続解除 bắt buộc tick 「リッチメニューを削除した」 mới cho đi tiếp — khách bị kẹt vì rich menu trên OA cũ không xóa được. Đây là **triệu chứng phụ** đáng test kèm.
- Bug đã được **đóng** (2026-09-10) do khách báo rich menu đã tự biến mất, nhưng Dev vẫn xác định được root cause thật và đã fix (commit + branch ở file 03).
- **Dữ liệu tồn đọng**: các bot đã đổi LOA **trước** khi có fix vẫn còn rich menu mồ côi trên OA cũ — fix không tự dọn, cần thống kê và dọn tay (Studio REQ-014).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Tài khoản エルメ | `mirei.yada.pianoroom@gmail.com` — LOA名 `発達支援ピアノ講師認定講座`, gói **Free** |
| LOA cũ (trước khi đổi) | `@481zcgwm` — Channel ID `2011211317` · Channel secret: `<có trên Redmine, không chép vào repo>` |
| LOA mới (sau khi đổi) | `@019nxejl` |
| Đối tượng cấu hình | Rich menu trên OA cũ — `richmenu-9fb635cd1a7c003fae3d1bc69f1c436a` · `richmenu-ff64ad87e2aa2b1d773b06e90fe76dfd` · `richmenu-f43246e49f2e1b1b0214fabb74d695dd` (cả 3 đều `deleteRichMenu status=404`) |
| Thời điểm lỗi | Thao tác đổi LOA: `2026/09/03` khoảng sau 13:00 (khách nhớ không chắc chắn); `2026/09/03 20:27` là lúc khách thao tác ở màn 接続設定 |
| Đối chứng | Rich menu dựng lại trên OA mới `@019nxejl` hiển thị bình thường — chỉ OA cũ bị sót |

## Journal / note từ Redmine (nguyên văn)

**Journal #134640 — AI bug detect Lme — 2026-09-05:**

```
Comment slack ngày 2026-09-05 19:44:57

WSSサポーター
Sau khi kiểm tra, chúng tôi không thấy lịch sử ngắt kết nối LOA liên quan đến người dùng này trong log từ ngày 31/8 trở đi.

Xin lỗi vì đã làm phiền, nhưng quý khách có thể vui lòng xác nhận lại thời điểm đã thực hiện ngắt kết nối LOA lần này được không ạ?
```

**Journal #134924 — AI bug detect Lme — 2026-09-07:**

```
Comment slack ngày 2026-09-07 17:00:00

お客様
⇒Việc 「移行」ở đây có phải là đã sử dụng 「LINE公式アカウント入れ替え機能」 của エルメ không ạ
Vâng, đúng như anh/chị nói ạ.

⇒Việc 「チャネルIDの変更」ở đây cụ thể là đã thực hiện thao tác gì, ở màn hình nào ạ
Từ menu bên trái trang danh sách tài khoản của エルメ,
tôi đã thay đổi từ phần cài đặt kết nối.
```

**Journal #135030 — AI bug detect Lme — 2026-09-08:**

```
Comment slack ngày 2026-09-07 17:53:00

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã liên hệ.

Sau khi kiểm tra, chúng tôi xác nhận tài khoản エルメ của quý khách đang ở gói Free.
「LINE公式アカウント入れ替え機能」chỉ có thể sử dụng với gói trả phí, nên tài khoản gói Free không thể sử dụng chức năng này.

Ngoài ra, dù chỉnh sửa Channel ID v.v. ở màn hình「接続設定」của エルメ, cũng không thể thay đổi chính tài khoản LINE chính thức đang kết nối với エルメ.

Xin xác nhận lại, trước đây quý khách có kết nối tài khoản LINE chính thức「@481zcgwm」với エルメ, có đúng không?

Nếu đúng, quý khách đã thực hiện thao tác「接続解除」từ màn hình chi tiết hợp đồng chưa?

・Về việc hủy kết nối
https://lme.jp/manual/cancellation/

Xin lỗi vì phải xác nhận lại nhiều lần, nhưng quý khách có thể xác nhận thời điểm đã đổi tài khoản LINE chính thức kết nối với エルメ từ「@481zcgwm」sang「@019nxejl」bằng「LINE公式アカウント入れ替え機能」là 2026年09月03日 - 20:27, có đúng không?

Rất mong quý khách phản hồi.
```

**Journal #135032 — AI bug detect Lme — 2026-09-08:**

```
Comment slack ngày 2026-09-07 18:48:00

お客様
Cảm ơn đã liên hệ.

＞「LINE公式アカウント入れ替え機能」chỉ có thể sử dụng với gói trả phí
Quý khách nói vậy, nhưng tôi nhớ rằng đã từng đổi tài khoản vào lúc chức năng đổi tài khoản chính thức đang miễn phí.
Hình như có một thời gian bên phía cung cấp dịch vụ đó miễn phí, không biết có đúng không.

＞Xin xác nhận lại, trước đây quý khách có kết nối tài khoản LINE chính thức「@481zcgwm」với エルメ, có đúng không?
Vâng, điều này là đúng, không có gì sai.

＞Nếu đúng, quý khách đã thực hiện thao tác「接続解除」từ màn hình chi tiết hợp đồng chưa?
Tôi xin lỗi rất nhiều, tôi đã không thực hiện thao tác này.

Bây giờ tôi đã thử vào màn hình hủy kết nối,
nhưng nếu không tick vào ô「リッチメニューを削除した」thì không thể tiếp tục bước sau.
Có thể là do khi còn kết nối với「@481zcgwm」, tôi đã không xóa rich menu mà đã thực hiện đổi sang「@019nxejl」bằng「LINE公式アカウント入れ替え機能」,
nên khi hủy kết nối, tôi không thể tick vào ô「リッチメニューを削除した」,
và không thể thực hiện hủy kết nối được.

Rất mong được xác nhận lại giúp tôi.
Xin lỗi vì đã gây phiền phức.
```

**Journal #135033 — AI bug detect Lme — 2026-09-08:**

```
Comment slack ngày 2026-09-07 20:49:00

お客様
Xin lỗi vì đã làm phiền nhiều lần.
Về phần trả lời phía trên

＞Nếu đúng, quý khách đã thực hiện thao tác「接続解除」từ màn hình chi tiết hợp đồng chưa?

〜tôi xin gửi lại phần trả lời từ đoạn này trở xuống.

Tôi rất xin lỗi, nhưng tôi đã không thực hiện thao tác này.
Tôi không thực hiện hủy kết nối, mà đã thao tác「LINE公式アカウント入れ替え機能」.

Ở「LINE公式アカウント入れ替え機能」, hiện tại đã kết nối thành công từ「@481zcgwm」sang「@019nxejl」.

Vì vậy, tôi nghĩ nếu bây giờ thực hiện hủy kết nối thì「@019nxejl」sẽ bị hủy kết nối.

Và rich menu đã được thiết lập trên tài khoản LINE chính thức「@481zcgwm」vẫn còn hiển thị với bạn bè của「@481zcgwm」.

Rất mong được xác nhận lại giúp tôi.
```

**Journal #135122 — AI bug detect Lme — 2026-09-08:**

```
Comment slack ngày 2026-09-08 12:55:00

お客様
Cảm ơn quý công ty đã luôn hỗ trợ.

＞ Thời điểm thực hiện đổi từ 「@481zcgwm」 sang 「@019nxejl」 bằng 「LINE公式アカウント入れ替え機能」
Trí nhớ của tôi không rõ ràng nên xin lỗi, nhưng tôi nghĩ chắc chắn là ngày 3 tháng 9. Thời điểm 20:27 là lúc tôi thực hiện cài đặt kết nối. Bản thân thao tác đổi tài khoản thì tôi nghĩ đã thực hiện sau 13 giờ.

＞ Hiện tại rich menu có vẫn tiếp tục hiển thị trên ứng dụng LINE của friend không ạ？
Vâng, vẫn tiếp tục hiển thị ạ.

Mong quý công ty hỗ trợ.
```

**Journal #135570 — Thanh Duy Nguyen — 2026-09-10:**

```
#deleteRichMenu richMenuId=richmenu-9fb635cd1a7c003fae3d1bc69f1c436a status=404
#deleteRichMenu richMenuId=richmenu-ff64ad87e2aa2b1d773b06e90fe76dfd status=404
#deleteRichMenu richMenuId=richmenu-f43246e49f2e1b1b0214fabb74d695dd status=404
```

**Journal #135587 — AI bug detect Lme — 2026-09-10:**

```
Comment slack ngày 2026-09-10 14:33:00

お客様
Cảm ơn quý công ty đã hỗ trợ.

Về rich menu mà chúng tôi đã trao đổi trong vụ việc này,
sáng nay tôi đã kiểm tra thì thấy hiển thị đã biến mất.
Xin lỗi vì đã gây phiền phức cho quý công ty.

Cảm ơn quý công ty đã hỗ trợ xử lý.

矢田美麗
```
