# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41688 qua `/new-task` (`scripts/redmine_fetch.py`).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41688 — [28-09-2026] [TY-12233] [Cross Analysis] Đổi trục tung cross analysis, danh sách phân tích không hiển thị` |
| Module / Màn hình | `Cross Analysis (クロス分析) — màn tạo mới / chỉnh sửa cross analysis, thao tác thêm/đổi trục tung (縦軸)` |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12233
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790578147747079
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12233

Số quản lý　：TY-12233
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C4Q8XTFDH
Email ：skillskip.miyaji@gmail.com
Tên LOA　　：スキルスキップ
Phụ trách　 ：沖原
Công cụ　 ：リンク
Nội dung yêu cầu
Sau khi đổi trục tung của cross analysis, danh sách phân tích không hiển thị.
https://www.loom.com/share/4d42dc57ff9648e19b409c1bd5ca26cd

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" theo format chuẩn -->

## Expected result

-

## Actual result

-

⚠️ Redmine #41688 không có section "Tái hiện bug"/"Steps to reproduce" theo format chuẩn — ticket này đến từ luồng OEM Slack support (khách hàng báo qua support, không phải luồng bug-detect nội bộ có template sẵn), nên Steps/Expected/Actual để trống. Tuy nhiên **root cause đã được Dev xác định cụ thể** qua phân tích request thật (xem `03-dev-impact.md`) và khách hàng có gửi **video repro** (link Loom ở mô tả + Journal #139045: "thêm trục tung vào cross analysis hiện có → việc liên kết bị hủy ngay lập tức"). TCs nên tập trung verify cách fix (FE không gửi `line_user_ids` khi lưu, BE trả lỗi 400 khi `filter_by` không hợp lệ thay vì mặc định = 1, FE hiển thị message lỗi khi lưu thất bại) + regression trên luồng tạo mới / lưu / copy cross analysis, đặc biệt với bot có filter friends lớn.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [x] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.watermelon.vn/attachments/download/31113/screenshot1.png
- Video repro (khách hàng gửi): https://www.loom.com/share/4d42dc57ff9648e19b409c1bd5ca26cd

## Ghi chú thêm của Leader

- Môi trường: Redmine không ghi rõ "Production"/"Staging", nhưng đây là ticket OEM khách hàng thật (dashboard `dashboard.melonglobal.net`, email khách `skillskip.miyaji@gmail.com`) → hiểu là **Production**.
- Tần suất lỗi: **không phải 100% mọi cross analysis** — theo Dev (03-dev-impact §1), lỗi chỉ xảy ra khi filter gốc của cross analysis đủ lớn để request FE vượt `max_input_vars` của PHP (case thật ghi nhận filter ~68,000 friends → 12,466 input vars). Cross analysis với filter nhỏ không gặp lỗi này.
- Bug KHÔNG tự phục hồi: cross analysis đã bị hỏng trước fix (filter_by bị ghi đè sai) cần khách hàng chọn lại tiêu chí phân tích, fix chỉ chặn lỗi phát sinh mới.
- Lưu ý dịch thuật: "trục tung" = 縦軸 (trục Y của bảng cross analysis) — tiêu chí thứ 2 dùng để phân tích chéo, khác "trục hoành" (横軸).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra theo email skillskip.miyaji@gmail.com / TY-12233 trên dashboard nội bộ>` |
| Friend | `N/A — bug không gắn với 1 friend cụ thể, xảy ra ở tầng lưu cross analysis` |
| Đối tượng cấu hình | Cross analysis `「まる/愛犬との暮らしと働き方コラボ」` (tên xác nhận ở Journal #139044) |
| Thời điểm lỗi | Request thật Dev bắt được: `12,466 input vars`, `line_user_ids` có `12,450` phần tử đứng trước `filter_by` trong payload |
| Đối chứng | `N/A — chưa có case cross analysis filter nhỏ chạy đúng được đối chiếu trong ticket` |

## Journal / note từ Redmine (nguyên văn)

**Journal #139044 — AI bug detect Lme — 2026-09-28:**

```
Comment slack ngày 2026-09-26 18:04:00

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã luôn ủng hộ.

Sau khi xác nhận, chúng tôi thấy rằng trong cross analysis「まる/愛犬との暮らしと働き方コラボ」, thông tin friend được thiết lập ở trục tung hiện đang ở trạng thái không tồn tại.

Trường hợp thông tin friend đã thiết lập trong cross analysis bị xóa, v.v., thì thông tin friend sẽ ở trạng thái không tồn tại.

Vì vậy, mong quý khách thiết lập lại thông tin friend trong cross analysis.

Ngoài ra, nếu vấn đề vẫn không được cải thiện, rất mong quý khách cho biết cụ thể các bước thao tác đang thực hiện trong cross analysis.

Xin cảm ơn quý khách.
```

**Journal #139045 — AI bug detect Lme — 2026-09-28:**

```
Comment slack ngày 2026-09-28 10:13:00

お客様
Cảm ơn quý vị đã xác nhận.

Đây là video màn hình quay lại việc thêm trục tung vào cross analysis hiện có.
https://www.loom.com/share/4d42dc57ff9648e19b409c1bd5ca26cd
Việc liên kết bị hủy ngay lập tức, không biết đây có phải là lỗi từ phía エルメ không ạ?

Mong quý vị xác nhận giúp.

宮地
```

<!-- Ghi chú: hồi đáp lần đầu của support (沖原) nghi ngờ nhầm là do friend info bị xóa — sau đó khách gửi video phản bác + Dev điều tra sâu hơn mới ra root cause thật (03-dev-impact.md §1: max_input_vars bị vượt). Đừng dùng nhận định ban đầu của support làm root cause. -->
