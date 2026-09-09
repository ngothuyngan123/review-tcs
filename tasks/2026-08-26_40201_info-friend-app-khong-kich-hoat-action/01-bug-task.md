# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40201 — [26-08-2026][T11981][Info friend] Cập nhật thông tin friend từ ứng dụng smartphone không kích hoạt action (đổi trạng thái đối ứng, bắt đầu step配信) như khi thao tác trên PC.` |
| Redmine URL | https://redmine.watermelon.vn/issues/40201 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-08-26` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn: OEM — 管理番号 TY-11981; user KH: mikuri-r.lillyline@lillyholdings.co.jp / Bot 「カーコネクションズ」) |
| Module / Màn hình | `Info friend` — 友だち情報管理 (Quản lý thông tin friend), folder「★顧客状況」/ quản lý名「顧客対応状況」 |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` — KH thật báo qua OEM nên nhiều khả năng **Production (step.lme.jp)**; tester confirm lại |
| Tracker / Status Redmine | `Bug KH` / `Fix done - Đợi test` |
| Assigned to (Redmine) | `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #40201. KHÔNG diễn giải lại. -->

```
User: mikuri-r.lillyline@lillyholdings.co.jp
Bot Name: カーコネクションズ

Về action thông qua thao tác trên app
【Mục liên quan】
- Quản lý thông tin friend
-Tên folder「★顧客状況」
-Tên quản lý「顧客対応状況」
Về các lựa chọn, đã cài đặt 2 action sau.
・Thay đổi trạng thái đối ứng
・Bắt đầu step配信

【Thao tác đã thực hiện và kết quả】
①Từ app smartphone, thay đổi thông tin friend「顧客対応状況」của「テスト（リリー）」thành「検討中」。
→Kết quả, trạng thái đối ứng không thay đổi, cũng không được thêm vào subscribe step配信「検討中」（action đã cài đặt không được kích hoạt）
→Trên PC chỉ có thông tin friend là thay đổi
②Thực hiện thao tác tương tự, từ màn hình quản lý trên trình duyệt PC
→Kết quả, trạng thái đối ứng đã đổi thành「検討中」, cũng được thêm ngay vào subscribe step配信「検討中」（action được kích hoạt bình thường）

【Muốn hỏi】
Khi cập nhật thông tin friend từ app smartphone, có phải spec là action đã cài đặt（gắn trạng thái đối ứng・bắt đầu step配信）sẽ không được kích hoạt không ạ?
Hay đây có khả năng là bug ạ?
Về mặt vận hành, chúng tôi cũng dự tính trường hợp client cập nhật thông tin friend từ app, nên muốn xác nhận lại.

Xin lỗi vì đã làm phiền, mong được xác nhận giúp.

Tên friend: テスト（リリー）
Chức năng: App smartphone (スマホアプリ)
Thời điểm phản hồi: 2026/08/26 11:27:25
Ảnh 1: data/screenshots/T11981_0.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11981

Nguồn: OEM đã tạo ticket trên Slack — 管理番号 TY-11981
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BSJR628JX
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1787713296277319

---

h3. 内容 từ Slack (OEM)
<pre>
【操作方法に関するお問い合わせフォーム】
アプリでの操作によるアクションについて
【該当項目】
- 友だち情報管理
-フォルダ名「★顧客状況」
-管理名「顧客対応状況」
選択肢について、以下2つのアクションを設定しております。
・対応ステータスの変更
・ステップ配信の開始

【行った操作と結果】
①スマホアプリから、「テスト（リリー）」の友だち情報「顧客対応状況」を「検討中」に変更。
→ 結果、対応ステータスも変わらず、ステップ配信「検討中」の購読にも追加されない（設定されているアクションが発火しない）
→PC上では友だち情報のみ変更される
②同じ操作を、PCのブラウザ管理画面から行う
→ 結果、対応ステータスが「検討中」に変わり、ステップ配信「検討中」の購読にもすぐに追加されました（アクションが正常に発火）

【質問したいこと】
スマホアプリから友だち情報を更新した場合、設定しているアクション（対応ステータス付与・ステップ配信開始）が発火しない仕様なのでしょうか。
それとも不具合の可能性がありますでしょうか。
運用上、クライアントがアプリから友だち情報を更新する場面も想定しておりますため、確認させていただきたく存じます。

お手数をおかけいたしますが、ご確認のほどよろしくお願いいたします。
</pre>

<!-- TaskRef: cs_form:T11981 oem_slack -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguồn: journal Redmine của **Hạnh Nguyễn** (2026-08-26) — "Thao tác tái hiện".

Tiền đề: `Friend info type select có option A chứa action status chat và scenario`

1. Thực hiện login vào App L message
2. Thực hiện add friend info type select đã setup trước đó cho friend
3. set value A cho friend
4. Quan sát

> Bổ sung từ mô tả KH (nguyên văn, 【Thao tác đã thực hiện và kết quả】):
> - ①Từ app smartphone, thay đổi thông tin friend「顧客対応状況」của「テスト（リリー）」thành「検討中」。
> - ②Thực hiện thao tác tương tự, từ màn hình quản lý trên trình duyệt PC

## Expected result

- (theo ② của KH — đường PC) `→Kết quả, trạng thái đối ứng đã đổi thành「検討中」, cũng được thêm ngay vào subscribe step配信「検討中」（action được kích hoạt bình thường）`
- Tức: cập nhật friend info từ **app smartphone** phải kích hoạt action gắn ở option **giống hệt** thao tác trên PC (đổi trạng thái đối ứng + bắt đầu step配信).

## Actual result

- (theo ① của KH — đường app) `→Kết quả, trạng thái đối ứng không thay đổi, cũng không được thêm vào subscribe step配信「検討中」（action đã cài đặt không được kích hoạt）`
- `→Trên PC chỉ có thông tin friend là thay đổi`
- (theo journal QA Hạnh Nguyễn) `Hiện tại: Status chat và scenario được set trong value A không được set cho friend`

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- [screenshot1.png](https://redmine.watermelon.vn/attachments/download/29409/screenshot1.png) — attachment #29409

Link tham chiếu khác (từ description):
- Dashboard CS: https://dashboard.melonglobal.net/css-analytics/?id=T11981
- Slack item (OEM): https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BSJR628JX
- Slack thread: https://l-message.slack.com/archives/C0BALS7S73L/p1787713296277319

## Ghi chú thêm của Leader

- KH đặt câu hỏi **"spec hay bug?"** (【Muốn hỏi】). Dev đã kết luận ở file 03: **không phải spec — là bug** ở API app. Khi review TC cần bám kết luận này.
- Bug **chỉ xảy ra trên đường API của app điện thoại** với **trường kiểu lựa chọn (select)**; đường PC không dính.
- Ticket đang ở trạng thái `Fix done - Đợi test` — đã có branch fix `ai_fixbug_40201`, chờ QA test.
