# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38761 — [14-07-2026][Popup] Chức năng 「ポップアップ」 của LME có bị ảnh hưởng bởi chính sách Google hạ đánh giá popup nút Back không?` |
| Redmine URL | https://redmine.watermelon.vn/issues/38761 |
| Auto-filled | 2026-07-21 by /new-task |
| Ngày báo cáo | 2026-07-14 |
| Khách hàng / PM báo | AI LME CSS |
| Module / Màn hình | Popup (「ポップアップ」) |
| Priority | Medium (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (câu hỏi về hành vi trên trình duyệt/smartphone của khách; Redmine không ghi rõ môi trường) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User:
Bot Name:

https://help.utage-system.com/archives/26634

Có vẻ từ sau ngày 15/06/2026, thao tác hiển thị popup khi người dùng bấm nút Back trên smartphone đã trở thành đối tượng bị Google hạ đánh giá (SEO). Vậy chức năng 「ポップアップ」 hiện tại của LME có thuộc diện bị ảnh hưởng này không?

Link thread: (không có)
Link item: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BFGM2L26A?record_id=Rec0BHXLQ76G0

---

h3. 原文 (JP)
<pre>
https://help.utage-system.com/archives/26634

スマートフォンで戻るボタンを押した際にポップアップを表示する動作が2026年6月15日以降、Googleでの評価を下げる対象となったようですが、今のエルメの「ポップアップ」機能にも該当されますでしょうか？
</pre>

<!-- TaskRef: wssj_check:Rec0BHXLQ76G0 -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — để trống. -->

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

- photo_2026-07-13_19-27-30.jpg — https://redmine.watermelon.vn/attachments/download/28253/photo_2026-07-13_19-27-30.jpg

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine (ticket dạng câu hỏi support từ khách) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). Ticket đã chuyển sang **nhánh B — sửa code**: bỏ can thiệp nút Back theo chính sách Google (từ 15/06/2026) + thêm chú thích ở màn thiết lập popup. TCs nên tập trung verify **cách fix** (gỡ `history.pushState` + `popstate` ở kiểu `close_page` và ở Lịch Salon) + **regression impact** (2 kiểu popup còn lại, booking Salon).
