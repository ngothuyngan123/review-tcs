# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37831 — [18-06-2026][T11287][Template] Khách báo 2 lỗi về Template: template gửi qua action khi thêm tag không hiển thị trên màn hình chat 1:1 ở trang quản trị (dù điện thoại nhận được), và tên quản lý template chứa ký tự '&' nửa chiều rộng hiển thị sai khi…` |
| Redmine URL | https://redmine.watermelon.vn/issues/37831 |
| Auto-filled | 2026-06-26 by /new-task |
| Ngày báo cáo | 2026-06-18 |
| Khách hàng / PM báo | AI bug detect Lme (author) — assigned_to: Kieu Son Tung |
| Module / Màn hình | Template |
| Priority | Medium (Redmine: Normal) |
| Môi trường phát hiện | Production (step.lme.jp) |

## Mô tả bug (nguyên văn từ khách hàng)

```
User: 2004minami65@gmail.com
Bot Name: ミショナ採用

Cảm ơn anh/chị đã hỗ trợ.
Tôi là Shibukawa, phụ trách LINE tuyển dụng của Mishona.
Xin phép liên hệ qua cửa sổ hỗ trợ chung.
Tôi đã phát hiện hiện tượng nghi là lỗi của Lme nên xin nhờ kiểm tra giúp.

① Template được gửi đi bằng action khi thêm tag thì xem được trên điện thoại đã nhận, nhưng KHÔNG hiển thị trên màn hình chat 1:1 trong trang quản trị Lme.

Tag liên quan: tag 「❌️面談｜不合格」 trong folder 「【初回】面談」.
Template chỉ lọc gửi riêng cho những người có tag Lancers thì không hiển thị.
https://step.lme.jp/basic/tag/edit-tag/39336

Cũng có những tag khác được thiết lập tương tự, nhưng các tag đó vẫn hiển thị bình thường trên chat 1:1 ở trang quản trị.

② Phần tên quản lý template có chứa ký tự 「&」 (nửa chiều rộng) hiển thị bị lỗi.
Xem ở danh sách template thì không sao, nhưng khi mở chi tiết thì hiển thị thành 「&」.
Đổi sang chữ in 「＆」 (full-width) thì có vẻ không bị lỗi.
Ví dụ: https://step.lme.jp/basic/template-v2/create-group?template_id=7142322

Tên friend: 渋川みな美（テスト配信）
Chức năng: Template (テンプレート)
Thời điểm phản hồi: 2026/06/18 12:32:53
Ảnh 1: data/screenshots/T11287_0.png
Ảnh 2: data/screenshots/T11287_1.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11287
Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0BBC9NQTJA
Nguồn: Tayori — task #11287 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/fccba1573a33ec668367d6cf0d94d5d03c0998b8/

---

h3. 原文 (JP)
お世話になっております。
ミショナ採用LINE担当の澁川です。
一般の窓口から問い合わせ失礼します。
エルメの不具合と思われる事象を確認しましたのでご確認お願いいたします。

①タグ追加時のアクションで配信するテンプレートが、配信されたスマホからは見れるが、エルメ管理画面の1：1チャットのトーク画面では表示されない。

該当のタグ：「【初回】面談」フォルダの「❌️面談｜不合格」タグ
ランサーズタグ有りの方だけに絞り込みで配信するテンプレートが表示されない。
https://step.lme.jp/basic/tag/edit-tag/39336

他にも同様の設定をしているタグもありますが、その他は問題なく管理画面の1:1チャットにも表示されます。

②テンプレート管理名に「&」（半角）がはいっている部分の表示がおかしい。
テンプレート一覧で見ると問題ないですが、詳細を開いたときに「&」と表示。
大文字の「＆」に変更すると問題ないようです。
例：https://step.lme.jp/basic/template-v2/create-group?template_id=7142322
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguồn: journal QA Thanh Phương (#122638, 2026-06-19) — "Tái hiện Bug".

1. Tạo tag có action template → add tag cho user lần 1 ⇒ user được send template.
2. Vào edit template (add / xóa / edit nội dung template con) → add lại tag cho user ⇒ user được send template.

## Expected result

- Ở màn chat 1:1 trang quản trị hiển thị **nội dung template mới nhất** (giống nội dung mà phía LINE user nhận được).
- (Bug ②) Tên quản lý template chứa ký tự `&` nửa chiều rộng hiển thị đúng ở màn chi tiết, không bị đổi thành `&amp;`.

## Actual result

- Ở màn chat 1:1 hiện **nội dung template chưa edit** (cũ), trong khi phía LINE user vẫn nhận đúng nội dung mới.
- (Bug ②) Mở chi tiết template thấy ký tự `&` nửa chiều rộng hiển thị sai (thành `&amp;`); đổi sang `＆` full-width thì không bị.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine):
- screenshot1.png — https://redmine.watermelon.vn/attachments/download/27145/screenshot1.png
- screenshot2.png — https://redmine.watermelon.vn/attachments/download/27146/screenshot2.png

## Ghi chú thêm của Leader

⚠️ **Bug gồm 2 lỗi riêng** (① template gửi qua action không hiện ở chat 1:1, ② ký tự `&` nửa chiều rộng hiển thị sai). Bug được báo qua AI bug detect → có **2 lần đánh giá ảnh hưởng khác nhau** (xem `03-dev-impact.md`): bản fix mới nhất (human dev, 2026-06-26) chỉ xử lý bug ①. Cần xác nhận với Dev xem bug ② đã được fix & deploy trong cùng release chưa trước khi viết/review TC.
