# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36709 by `/new-task` lúc 2026-05-26.
> Tester verify rồi tick checkbox "Tester verify auto-fill chính xác" bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36709 — [23-05-2026][11009][Form] Form 「1Mアンケート」 — submit không reflect kết quả, page reset về top (T CLINIC)` |
| Redmine URL | https://redmine.watermelon.vn/issues/36709 |
| Auto-filled | 2026-05-26 by `/new-task` |
| Ngày báo cáo | 2026-05-23 |
| Khách hàng / PM báo | AI CSS (T CLINIC — user: sagara@tclinic-official.com) |
| Module / Màn hình | Form (form 「1Mアンケート」 — form rẽ nhánh nhiều page) |
| Priority | Medium (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi rõ env, nhưng đối tượng là T CLINIC customer form) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: sagara@tclinic-official.com
Bot Name: T CLINIC

Về form 「1Mアンケート」, khi KH nhập thông tin và nhấn nút submit thì kết quả không được reflect, đồng thời page tự cuộn về đầu trang (top).

[Bổ sung]
Ảnh đính kèm do phía wssj chụp.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B5P9S00KY

---

h3. 原文 (JP)
<pre>
「1Mアンケート」というフォームについて、入力してボタンを押しても結果に反映されず、一番上に戻る。

[補足]
添付画像については弊社側で撮影
</pre>

<!-- TaskRef: user_report:Rec0B5P9S00KY -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Tái hiện bug được dev Thanh Phương ghi lại (Redmine journal #119442 ngày 2026-05-26):

1. Mở setting một form rẽ nhánh đang có 1 page.
2. Nhấn add thêm 1 page mới.
3. Nhấn xóa page vừa tạo.
4. Reload màn hình setting form.
5. Nhấn Save form.
6. Mở public link của form vừa save, nhập thông tin và nhấn Submit.

## Expected result

- Sau bước 5, setting form được lưu nhất quán: page cuối có `next_page_type = END_FORM` và `next_page_setting = null` (không self-reference).
- Sau bước 6, form hiển thị màn kết quả / cảm ơn (response được reflect). Page không reset về top.

## Actual result

- Sau bước 5, setting page hiện tại bị lưu thành `next_page_setting` trỏ về chính nó (self-reference).
- Sau bước 6, submit không reflect kết quả; page tự cuộn về top và user không trả lời / hoàn thành form được.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine):
- https://redmine.watermelon.vn/attachments/download/26034/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-23%20144934.png
- https://redmine.watermelon.vn/attachments/download/26035/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-23%20145006.png

## Ghi chú thêm của Leader

- Redmine parent issue: #36192.
- Bug được khách hàng (T CLINIC, AI CSS report ngày 2026-05-23) báo, nhưng **steps tái hiện chính thức** do dev Thanh Phương ghi trong journal — tester nên verify lại tái hiện được trên môi trường staging trước khi viết TC.
- Section "Đánh giá ảnh hưởng" do Thanh Phương (Frontend / Form team) submit ngày 2026-05-26 — xem [03-dev-impact.md](03-dev-impact.md).
- Tracker = "Bug KH" (báo từ khách hàng) — Priority Normal trong Redmine map sang Medium theo convention; nếu T CLINIC là enterprise customer thì cần xác nhận lại với Leader xem có cần bump lên High không.
