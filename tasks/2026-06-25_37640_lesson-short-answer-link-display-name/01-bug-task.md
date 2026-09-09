# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37640 — [13-06-2026][No.11240][Lesson] Lesson: câu trả lời ngắn có bị ép liên kết vào tên hiển thị hệ thống không?` |
| Redmine URL | https://redmine.watermelon.vn/issues/37640 |
| Auto-filled | `2026-06-25 by /new-task` |
| Ngày báo cáo | `2026-06-15` |
| Khách hàng / PM báo | `AI LME CSS` (customer: info@naruki-juku.co.jp — Bot 成る木塾) |
| Module / Màn hình | `Lesson — レッスン予約 / お客様への質問項目` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (KH dùng thanh toán UnivaPay trong レッスン予約) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: info@naruki-juku.co.jp
Bot Name: 成る木塾

Đặt lịch học (レッスン予約)：二次試験対策
Khi sử dụng thanh toán (決済), câu trả lời ngắn (短文回答) có bị bắt buộc liên kết (連携) vào tên hiển thị hệ thống (システム表示名) theo spec không?
Nếu vậy, việc bắt buộc liên kết vào tên hiển thị hệ thống (システム表示名) có phải là quy định bởi pháp luật không?

[Bổ sung]
Khách hàng đang quản lý bằng cách nhập tên học sinh của phụ huynh vào tên hiển thị hệ thống (システム表示名), và họ không muốn nó bị liên kết (連携) với tên hiển thị hệ thống.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B9W62UG95

---

### 原文 (JP)
```
レッスン予約：二次試験対策
決済を利用する際、短文回答はシステム表示名へ強制的に連携される仕様になりますでしょうか？
その場合、システム表示名への強制連携は法律で決まっているものでしょうか？

[補足]
ユーザーはシステム表示名へ保護者の生徒名を入れて管理しており、システム表示名と連携させたくないとのことです。
```

### Chốt yêu cầu (từ comments + journals Redmine)
- 決済利用時に短文回答がシステム表示名へ自動的に連携される仕様 → KH (lớp luyện thi) nhập tên học sinh vào システム表示名 để dễ quản lý/tìm kiếm 1:1, không muốn bị câu trả lời thanh toán ghi đè.
- Comment chốt (筒井 和紀, 2026-06-17): **「Cho phép tùy chọn việc liên kết với tên hiển thị hệ thống, đồng thời cho phép chọn cả thông tin bạn bè khác (ngoài システム表示名) làm đối tượng liên kết」** → mong đối ứng.
- ホアン xác nhận: liên kết câu trả lời vẫn bắt buộc, nhưng **đích liên kết (連携先) được tự do chọn** (liên kết với thông tin người bạn nào cũng được).
- Phạm vi đối ứng đợt này: **Lesson (レッスン予約) + Salon (サロン予約)** trước (dự kiến 26/06). 商品販売 / イベント予約 sẽ lên kế hoạch sau.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — đây là inquiry/feature request từ KH. Để trống. -->

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

- https://redmine.watermelon.vn/attachments/download/26884/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-13%2015.41.45.png
- https://redmine.watermelon.vn/attachments/download/27386/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-23%2013.42.08.png
- https://redmine.watermelon.vn/attachments/download/27387/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-23%2013.42.47.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (Feature inquiry — không có section "Tái hiện bug") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
