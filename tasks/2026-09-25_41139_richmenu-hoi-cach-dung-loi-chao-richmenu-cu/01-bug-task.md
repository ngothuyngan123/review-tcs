# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41139 bởi `/new-task` (2026-09-25). Tracker = **Support** (câu hỏi khách hàng, không phải Bug) — Dev chuyển thành task Java bổ sung điều kiện chặn job.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41139 — [19-09-2026] [30663] [Richmenu] Hỏi cách dừng lời chào & richmenu cũ của LME sau khi hủy hợp đồng (No.30663)` |
| Module / Màn hình | `<Redmine không có category>` — suy từ description: 友だち追加時設定 (あいさつメッセージ — lời chào khi thêm bạn) · リッチメニュー表示 (hiển thị richmenu) · 契約情報 / 解約 (hủy hợp đồng) · job nền Java dùng chung (action, callback, scenario, delay message, broadcast, notify). Studio task #328 gắn `feature=add-friend-setting`. |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — câu hỏi của người dùng) — 管理番号 (mã quản lý) 30663
担当 (phụ trách): 筒井
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1789804839983389
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=30663

Tên LOA: 株式会社fulme.【フルミー】 · Công cụ: リンク

Nội dung liên hệ:

Cảm ơn quý công ty đã hỗ trợ.
Hiện tại chúng tôi đã hủy hợp đồng LME (エルメ), nhưng vẫn giữ nguyên kết nối với tài khoản LINE chính thức (LINE公式アカウント).
Phía tài khoản LINE chính thức, chúng tôi đã cài đặt richmenu mới và 「あいさつメッセージ」(lời chào).
Tuy nhiên, khi thử thêm bạn mới để kiểm tra, chúng tôi phát hiện 2 điểm sau đây khác với nội dung đã cài đặt ở phía LINE chính thức:
- Hiển thị một richmenu khác, có vẻ là richmenu đã từng cài đặt trước đây trên LME.
- Tin nhắn chào ngay sau khi thêm bạn cũng gửi nội dung khác với nội dung hiện đang cài đặt ở phía LINE chính thức.

Ngoài ra, mã QR dùng để thêm bạn đã được đổi từ mã QR tạo trên LME sang mã QR do phía tài khoản LINE chính thức phát hành.
Vì vậy, chúng tôi cho rằng có khả năng các cài đặt phía LME như 「新規友だち追加時のあいさつメッセージ」(lời chào khi thêm bạn mới) hay 「リッチメニュー表示」(hiển thị richmenu) vẫn đang hoạt động ngay cả sau khi đã hủy hợp đồng.
Hiện tại do đã hủy hợp đồng nên chúng tôi không thể tự thay đổi các cài đặt trên LME.
Có cách nào để chỉ dừng 「あいさつメッセージの配信」(gửi lời chào) và 「リッチメニューの表示」(hiển thị richmenu) đang được thực hiện từ phía LME đối với bạn mới, mà không cần hủy kết nối với tài khoản LINE chính thức không?
Sau này, chúng tôi muốn chỉ áp dụng 「あいさつメッセージ」và 「リッチメニュー」đã cài đặt ở phía tài khoản LINE chính thức cho bạn mới.
Mong quý công ty xác nhận giúp, xin cảm ơn.

---

**[DETAIL TASK JAVA]** (Dev bổ sung trong description)

0. Base branch: `release-t08-2026`
1. Mô tả yêu cầu
   - Job ngoài check theo điều kiện `expired_date` bot quá hạn 7 ngày hoặc `status_bill_fail` = 5 để không thực hiện action, callback và tương tự các job khác thì thêm điều kiện check theo cột `status` trong bảng `bot_contact`. Nếu `status = 3` thì cũng chặn.
     - Từ `bot_id` query sang bảng `bot_slot` where `bot_id = ?`
     - Lấy được `bot_slots` → `bot_contract_id = bot_slots.bot_contract_id`
     - Lấy ra record `bot_contracts` có `id = bot_contract_id` lấy được ở trên
     - Lấy được `status` của `bot_contracts`
   - Chỉ cần kiểm tra `bot_contacts` cho trường hợp `expired_date` < hiện tại để tránh phải query lại nhiều. Và làm 1 map cache kết quả 1 phút.

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug". -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/30641/screenshot1.jpg
- https://redmine.watermelon.vn/attachments/download/30642/screenshot2.jpg
- https://redmine.watermelon.vn/attachments/download/30833/Screenshot%202026-09-23%20133814.png

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine (không có Section "Tái hiện bug") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: **Production** (khách hàng thật, bot đã hủy hợp đồng).
- Điều kiện chặn theo hợp đồng **chỉ áp dụng khi bot đã hết hạn** (`expired_date` < hiện tại) — journal #137835: bot chưa hết hạn chỉ chuyển được sang trạng thái chờ cancel và vẫn dùng bình thường; khi hết hạn, job crontab mới chuyển sang cancel.
- Kết quả cache 1 phút / bot → khi test, sau khi đổi trạng thái hợp đồng phải chờ tối đa 1 phút.
- Câu hỏi của khách còn phần **richmenu đã gán cho bạn cũ trước khi hủy** — fix chỉ chặn gán mới, không gỡ richmenu đã liên kết (Studio REQ-012 ghi nhận là khoảng trống).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<ticket không ghi>` |
| LOA / khách hàng | 株式会社fulme.【フルミー】 — 管理No 30663 |
| Đối tượng cấu hình | Lời chào khi thêm bạn + richmenu hiển thị mặc định đã cài trên LME trước khi hủy |
| Thời điểm lỗi | `<ticket không ghi — liên hệ 2026-09-19>` |
| Đối chứng | Lời chào + richmenu cài ở phía LINE公式アカウント (kỳ vọng được áp dụng thay cho LME) |

## Journal / note từ Redmine (nguyên văn)

**Journal #137563 — Do Van Tu TuDV — 2026-09-22:**

```
- Job ngoài check theo điều kiện expired_date bot quá hạn 7 ngày ngày hoặc status_bill_fail 5 để không thực hiện action, callback và tương tự các job khác thì thêm điều kiện check theo cột status trong bảng bot_contact. Nếu status = 3 thì cũng  chặn và không thực hiện action, callback và các job khác tương tự 

=> Từ bot_id query sang bảng bot_slot where bot_id = ?
=> Lấy được bot_slots => bot_contract_id = bot_slots.bot_contract_id
=> Lấy ra record bot_contracts có id = bot_contract_id lấy được ở trên
=> lấy được status của bot_contracts
```

**Journal #137835 — Do Van Tu TuDV — 2026-09-23:**

```
1. Bot chưa hết hạn chỉ chuyển được về trạng thái chờ cancel và vẫn dùng được bình thường
2. Khi nào bot hết hạn job crontab mới tự động chuyển về trạng thái cancel
=> khi nào bot hết hạn mới cần check status của hợp đồng đã cancel chưa
```

<!-- Journal #137226, #137229 (phản hồi Slack "đang kiểm tra") bỏ qua — không có nội dung điều tra. Journal #137972 (báo cáo đánh giá ảnh hưởng) chép vào file 03. -->
