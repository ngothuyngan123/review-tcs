# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40607 — [07-09-2026] [30087] [Scenario] Nhiều action không chạy khi dùng tính năng bốc thăm giới hạn số người` |
| Module / Màn hình | `Friend Information (FA-015) — màn 友だち情報管理 (quản lý thông tin friend): xóa value thủ công / 一括削除; hiển thị lịch sử ở màn 友だち詳細` |

> ⚠️ **Phạm vi ticket đã ĐỔI so với tiêu đề.** Tiêu đề + nội dung khách hàng nói về 3 hiện tượng của tính năng bốc thăm (抽選). Cả 3 đã được điều tra và **kết luận KHÔNG phải bug** (Journal #135149 + #135767). Bug thực sự được fix trên branch `ai_fixbug_40607` là **lịch sử friend info không fill tên người thao tác khi xóa value thủ công** — phát sinh từ điều tra của QA ở Journal #134709, repro ở Journal #135750. TCs phải bám theo **scope fix thực tế**, không phải theo tiêu đề ticket.

## Mô tả bug (bản dịch tiếng Việt)

**Nguồn:** OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 30087
**担当:** 筒井 · **Công cụ:** リンク · **Tên LOA:** パンのトラ
**Tài khoản L Message:** info+tramscope@line-marketing.co.jp

Chúng tôi đã tham khảo hướng dẫn (https://lme.jp/manual/lucky-draw/) và thực hiện chương trình bốc thăm có giới hạn số người, nhưng có vài hành vi khác với dự kiến xảy ra nên mong được xác nhận.

**① Mong được giải thích nguyên nhân vì sao dù đã nhấn nút 「【抽選スタート！】」 nhưng action sau khi tap nút không hoạt động.**

Friend：木原卓也

1. Block ở phía màn hình chat LINE（app LINE của friend）
2. Quét QR code action
3. Bỏ chặn (unblock)

Đây là luồng thao tác, sau đó nhấn nút template.

**② Có trường hợp template không hiển thị**

Friend：k.yukie — 8/29 12:11

Về phần nút của template, đã cài đặt số lần tap là 「何度でも可能」 và thử test. Mong được giải thích lý do vì sao khi đó nhấn nút nhưng template không hiển thị.

**③ Sau khi cộng điểm, template trúng thưởng không hiển thị**

Friend：Mao — 8/29 14:40

Trong quản lý thông tin friend, đã cài đặt để khi bốc thăm cộng 「1ポイント」 thì tag tương ứng sẽ được gắn, nhưng action không hoạt động. Mong được giải thích lý do. （Tag thì đã được gắn）

---

**Bug phát sinh từ điều tra (scope fix thực tế):** Ở màn 友だち情報管理, khi xóa value của friend info một cách thủ công (xóa từng mục hoặc 一括削除), dòng lịch sử hiển thị ở màn 友だち詳細 **không fill tên người thao tác** — chỉ hiện chữ 手動 trơn (hoặc hiện là tự động).

## Steps to reproduce

*(theo Journal #135750 — Ngô Thúy Ngần, 2026-09-10)*

1. Vào màn quản lý friend info (友だち情報管理) → Click vào số người 回答人数
2. Tại màn hình danh sách những người được gắn value info → Click chọn và bấm nút 一括削除
3. Mở màn detail line user 友だち詳細 → xem lịch sử của friend info vừa xóa

## Expected result

- Cột người thao tác của dòng lịch sử hiển thị `手動（<Tên user đã thao tác xóa>）`

## Actual result

- Lịch sử của friend info **không fill thông tin người thao tác xóa info** — chỉ hiện 手動 trơn (hoặc hiện là tự động)

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.watermelon.vn/attachments/download/30031/screenshot1.png
- screenshot2.png — https://redmine.watermelon.vn/attachments/download/30032/screenshot2.png
- image.png — https://redmine.watermelon.vn/attachments/download/30147/image.png
- image.png — https://redmine.watermelon.vn/attachments/download/30148/image.png

## Ghi chú thêm của Leader

- **Môi trường phát hiện: Production** — tài khoản khách hàng thật (LOA パンのトラ, bot_id 155192). Ticket không có repro trên staging/dev.
- ⚠️ **3 hiện tượng gốc của khách (①②③) KHÔNG phải bug** — kết luận ở Journal #135767:
  - ① + ②: tag (`36時間抽選会_1等当選_日曜` / `36時間抽選会`) đã **đạt giới hạn số người gán** → action gắn với tag đó không được kích hoạt.
  - ③: action của tag `36時間抽選会_1等当選_土曜日` được cấu hình **tự gán chính tag đó** → action tiếp theo (hiển thị template trúng thưởng) không chạy.
  - → Là **hành vi theo thiết kế** (limit tag + skip khi tag đã tồn tại), không có code fix. Nếu Leader muốn phủ, xếp vào nhóm TC **xác nhận spec / UX cảnh báo**, không phải TC verify fix.
- ⚠️ **Branch fix hiện tại chỉ cover bug lịch sử friend info** (1 file, 5 insertions / 2 deletions). Phần sửa điểm nhận webhook LINE **đã bị GỠ** khỏi branch theo yêu cầu dev → ticket này **không còn bản sửa nào cho triệu chứng gốc**.
- ⚠️ **Dòng lịch sử ghi TRƯỚC bản fix vẫn trống tên vĩnh viễn, KHÔNG bù được** (tên là snapshot lúc ghi, query đọc đã bỏ join bảng user). Tester phải verify trên **data mới tạo sau khi deploy**, không dùng data cũ — nếu không sẽ kết luận nhầm "fix không ăn".
- ⚠️ Dev tự review nêu **3 lỗi khác trong cùng hàm xóa vẫn CÒN**: không ghi lịch sử cho 6 field mặc định · bộ đếm sai khi xóa hàng loạt · bản mobile không ghi lịch sử. Leader cân nhắc đưa vào regression scope hay tách ticket.
- ⚠️ Dev **không verify được bằng data thật** (không truy cập được DB khách, server dev nội bộ MySQL từ chối kết nối) → mức verify chỉ là `lint`. Rủi ro cao, TC phải verify end-to-end trên môi trường có DB.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `155192` |
| Friend ① | `木原卓也 — line_user_id: 32323213` |
| Friend ② | `k.yukie — line_user_id: 50454446` |
| Friend ③ | `Mao — line_user_id: 60597214` |
| Đối tượng cấu hình | friend info `36時間抽選会_日曜日` / `36時間抽選会_土曜日` (kiểu point) · tag `2351283` (`36時間抽選会_1等当選_日曜`) · tag `2243561` (`36時間抽選会_1等当選_土曜日`) · action `20731604` (add tag 2243561) · action `21170264` (tag tự add chính nó) · template `【修正後】抽選開始_日曜` / `【修正後】テスト抽選開始_土曜` · QR `36時間抽選会（土曜日）` |
| Thời điểm lỗi | Đăng ký 1 point: `2026/08/29 14:27:39` · **Xóa thủ công value không fill tên: `2026/08/29 14:28:36`** · Case ③: `2026/08/29 14:40:33` |
| Đối chứng | Màn 友だち詳細 · chat 1:1 · API mobile — đều truyền đủ id người thao tác + mã nguồn thủ công nên **hiển thị đúng tên** (dùng làm case đối chứng cho TC) |

## Journal / note từ Redmine (nguyên văn)

**Journal #134709 — Ngô Thúy Ngần — 2026-09-07:**

```
bot_id: 155192

① Mong được giải thích nguyên nhân vì sao dù đã nhấn nút 「【抽選スタート！】」 nhưng action sau khi tap nút không hoạt động.

Friend：木原卓也

1.Block ở phía màn hình chat LINE（app LINE của friend）
2.Quét QR code action
3.Bỏ chặn (unblock)
Đây là luồng thao tác, sau đó nhấn nút template.

*--> line_user_id: 32323213
Check lịch sử quét QR lúc 2026/08/29 (土) 14:27 => Gửi template 【修正後】抽選開始_日曜 => User tap button lúc 2026-08-29 14:27:39 có thấy lịch sử đăng ký info point 36時間抽選会_日曜日 là 1 point => Sau đó thấy lịch sử xóa thủ công value của info này lúc 2026-08-29 14:28:36 nhưng lại không thấy fill tên user đã thao tác?
+ Check xem tại sao lúc đăng ký 1 point ko thấy chạy action
+ Check xem tại sao lúc xóa value thủ công không hiển thị fill tên user thao tác ở lịch sử*


② Có trường hợp template không hiển thị
Friend：k.yukie
8/29 12:11

Về phần nút của template, đã cài đặt số lần tap là 「何度でも可能」 và thử test.
Mong được giải thích lý do vì sao khi đó nhấn nút nhưng template không hiển thị.

*--> line_user_id: 50454446
Check xem tại sao lúc tap button không chạy action*

③ Sau khi cộng điểm, template trúng thưởng không hiển thị

Friend：Mao
8/29 14:40

Trong quản lý thông tin friend, đã cài đặt để khi bốc thăm cộng 「1ポイント」 thì tag tương ứng sẽ được gắn, nhưng action không hoạt động.
Mong được giải thích lý do. （Tag thì đã được gắn）

*--> line_user_id: 60597214*
```

**Journal #135149 — Thanh Duy Nguyen — 2026-09-08:**

```
1. line_user_id: 32323213
+ Check xem tại sao lúc đăng ký 1 point ko thấy chạy action
=> Action add tag bị limit: ADD is limit tagId 2351283


2. line_user_id: 50454446
Có trường hợp template không hiển thị. Check xem tại sao lúc tap button không chạy action
=> Khách bấm nhiều button. Check vẫn thấy action bình thường. Có gửi template. Action add tag thì tag tồn tại nên skip.
Chưa rõ khách report cụ thể cái nào


3. line_user_id: 60597214
Action 20731604 add tag 2243561 => Đã có add tag.
Trong tag có action 21170264 add tag 2243561 => Tự add tag chính tag này nên ko action
```

**Journal #135750 — Ngô Thúy Ngần — 2026-09-10:**

```
Thao tác tái hiện:
1. Vào màn quản lý friend info => Click vào số người 回答人数
2. Tại màn hình danh sách những người được gắn value info => Click chọn và bấm nút 一括削除

BUG: Tại màn detail line user 友だち詳細, lịch sử của friend info không fill thông tin người thao tác xóa info
Expect: Fill là 手動（<Tên user đã thao tác xóa>）
```

**Journal #135767 — AI bug detect Lme (Comment slack 2026-09-10 20:23:28 — WSSサポーター) — 2026-09-10:**

```
Về 3 trường hợp đã xác nhận, chúng tôi xin báo cáo kết quả điều tra.
① Bạn bè：木原卓也
Do số lượng gán tối đa của tag 「36時間抽選会_1等当選_日曜」 đã đạt giới hạn, nên action được cài đặt cho tag đó đã không được kích hoạt.
② Bạn bè：k.yukie（8/29 12:11）
Giống như ①, nguyên nhân là do số lượng gán tối đa của tag 「36時間抽選会」 đã đạt giới hạn.
Do đó, sau khi tap nút, action được cài đặt đã không được kích hoạt, và template cũng không được hiển thị.
③ Bạn bè：Mao（8/29 14:40）
Trường hợp này được cho là do nội dung cài đặt của action.
Trong QR code 「36時間抽選会（土曜日）」 có:
action gửi template 「【修正後】テスト抽選開始_土曜」, và action gán tag 「36時間抽選会」.
Trong template đó, khi tap nút 「【抽選スタート！】」，
・Gán điểm ngẫu nhiên vào thông tin friend 「36時間抽選会_土曜日」
・Gán tag theo kết quả trúng thưởng
thì các action trên sẽ được thực thi.
Trong thao tác lúc 8/29 14:40:33, ở lần tap nút đầu tiên đã gán 1 điểm, sau đó action gán tag 「36時間抽選会_1等当選_土曜日」 đã được thực thi.
Tuy nhiên, bản thân action được cài đặt cho tag 「36時間抽選会_1等当選_土曜日」 lại được cài đặt để gán chính tag 「36時間抽選会_1等当選_土曜日」 đó.
Do đó, action tiếp theo để hiển thị template trúng thưởng được cho là đã không được kích hoạt bình thường.
Trên đây là nguyên nhân đã xác nhận được lần này.
```
