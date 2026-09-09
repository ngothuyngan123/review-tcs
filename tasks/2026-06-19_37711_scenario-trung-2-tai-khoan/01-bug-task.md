# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37711 — [16-06-2026][T11271][Scenario] Cùng một khách hiển thị thành 2 tài khoản trùng trên LME; cùng một scenario (ステップ配信) chạy trên cả hai, một bên đã xong nhưng bên kia vẫn tiếp tục — nghi lỗi đăng ký trùng, ảnh hưởng nhiều user.` |
| Redmine URL | https://redmine.watermelon.vn/issues/37711 |
| Auto-filled | `2026-06-19 by /new-task` |
| Ngày báo cáo | `2026-06-16` |
| Khách hàng / PM báo | `AI bug detect Lme` (User: support_tools@shatoku.com / Bot: 坂尾 拓優) |
| Module / Màn hình | `Scenario (ステップ配信 — Gửi tin theo bước)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (report KH, không nêu môi trường) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: support_tools@shatoku.com
Bot Name: 坂尾 拓優

Cảm ơn quý công ty đã luôn hỗ trợ.

Trên LME đang xảy ra hiện tượng cùng một người dùng (dường như là cùng một người) bị hiển thị thành 2 tài khoản.

Ví dụ）
Tên LINE: 坂尾 拓優
Tên LINE: haruka　và nhiều trường hợp khác

Với những người dùng trên, trên màn hình LME tồn tại 2 tài khoản có nội dung giống hệt nhau, và cùng một chiến dịch gửi theo bước (step) đang được thực thi cho cả hai tài khoản.

Ngoài ra, mặc dù ở một tài khoản đã hoàn tất phản hồi, nhưng ở tài khoản còn lại một chiến dịch gửi theo bước khác vẫn đang tiếp tục.

Hiện tượng tương tự cũng được xác nhận ở nhiều người dùng khác.

Đây có khả năng là lỗi do đăng ký trùng lặp (trùng tài khoản) hay không?

Nếu có cách kiểm tra hoặc cách khắc phục, rất mong được chỉ dẫn.

Trong lúc quý công ty bận rộn, rất xin lỗi đã làm phiền, mong được kiểm tra giúp. Xin chân thành cảm ơn.

Chức năng: Gửi tin theo bước / Scenario (ステップ配信) (ステップ配信)
Thời điểm phản hồi: 2026/06/16 12:16:27
Ảnh 1: data/screenshots/T11271_0.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11271
Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0BAS7Y7J3G
Nguồn: Tayori — task #11271 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/b32d7d857ce95265b954f2441fa042a98e6a5471/

---

### 原文 (JP)
```
お世話になっております。

エルメ上で、同一ユーザーと思われる方が2つのアカウントとして表示される事象が発生しております。

例）
LINE名：坂尾 拓優
LINE名：haruka　他多数

上記ユーザーについて、エルメ画面上で同一内容のアカウントが2つ存在しており、両方のアカウントに対して同じステップ配信が実行されている状況です。

また、一方のアカウントで回答が完了しているにもかかわらず、もう一方のアカウントでは別のステップ配信が継続されております。

同様の事象は他のユーザーでも複数名確認しております。

こちらは重複登録等による不具合の可能性がありますでしょうか。

確認方法や解消方法がございましたらご教示いただけますと幸いです。

ご多用中恐れ入りますが、ご確認の程よろしくお願いいたします。
```

<!-- TaskRef: cs_form:T11271 -->

> 📌 Bot/user liên quan (journal Ngọc Ánh): `bot_id: 150755`, `line_user_id: 54323076`.
> 📌 2 user chưa khôi phục xong (comment Slack 2026-06-17): アリサ / あべ まゆこ.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [x] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- ⚠️ Bug KH không có Section "Tái hiện bug" — không tái hiện được trực tiếp. Để trống. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine):
- スクリーンショット 2026-06-11 15.30.47.png — https://redmine.watermelon.vn/attachments/download/26963/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-11%2015.30.47.png
- スクリーンショット 2026-06-16 13.17.14.png — https://redmine.watermelon.vn/attachments/download/26965/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-16%2013.17.14.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

⚠️ Bản chất bug là **race condition** (web form/checkFriend đua với job follow-callback cùng line_id → tạo 2 line_user trùng). Khó tái hiện cố định — cần test theo hướng verify dedup logic + regression các điểm tạo line_user, không phụ thuộc reproduce 100% race.

⚠️ Lưu ý 2 hướng fix khác nhau trong lịch sử Redmine (xem file 03):
- Bản AI auto-fixbug (branch `ai_fixbug_37711`): guard ở phía **web** — QRCodeController::checkFriend + FormAnswerController::userOpenFormanswer.
- Bản dev cuối cùng — Kim Cúc (branch `m_202606_duplicate_line_user_37711`, commit `2f32444`): guard ở phía **job** — HandlePostbackTask (doHandleFollowEvent, checkAddOldFriend, checkAddGroupFriend, checkAddGroup + checkDuplicateLineUserAfterInsert mới).
→ File 03 lấy theo bản dev cuối cùng (Kim Cúc). **Leader cần confirm với Dev branch nào thực sự được merge để test đúng phạm vi.**
