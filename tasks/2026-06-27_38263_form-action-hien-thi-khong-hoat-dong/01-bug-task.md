# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38263 — [27-06-2026][T11392][Form] Khách báo action khi hiển thị form không hoạt động, nhờ kiểm tra.` |
| Redmine URL | https://redmine.watermelon.vn/issues/38263 |
| Auto-filled | `2026-06-27 by /new-task` |
| Ngày báo cáo | `2026-06-27` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn: KH riofukunaga@re-akiya.co.jp — Bot AKIYATO — qua Tayori task #11392) |
| Module / Màn hình | `Form` (Form Builder — action khi mở/hiển thị form) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — KH thật báo qua Tayori (Production); tester chọn env test, mặc định Staging staging.lme.jp>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: riofukunaga@re-akiya.co.jp
Bot Name: AKIYATO

Cảm ơn anh/chị đã hỗ trợ.

Khi hiển thị form, action không hoạt động nên nhờ anh/chị kiểm tra giúp.

Tên friend: Rio
Chức năng: Tạo form (フォーム作成)
Thời điểm phản hồi: 2026/06/27 11:34:51
Ảnh 1: data/screenshots/T11392_0.png
Ảnh 2: data/screenshots/T11392_1.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11392
Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BDFUU69U5
Nguồn: Tayori — task #11392 (操作方法に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/fbc767baffe25debc92a476eaaf0c0729180dd29/

---

h3. 原文 (JP)

お世話になっております。

フォーム表示時アクションが作動しないのでご確認お願いいたします。

<!-- TaskRef: cs_form:T11392 -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — xem note Leader bên dưới. -->

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

- https://redmine.watermelon.vn/attachments/download/27626/screenshot1.png
- https://redmine.watermelon.vn/attachments/download/27627/screenshot2.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (description chỉ là phản hồi của KH, không có Steps/Expected/Actual) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (action loại "chỉ lần đầu" khi mở form lần đầu) + regression action loại "mọi lần".
