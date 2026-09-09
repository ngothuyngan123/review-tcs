# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38727 — [Friend info][Detail friend] Khi form gắn câu trả lời vào friend info, Khi friend đó bị xóa, vẫn ghi lịch sử friend info nhưng không có tên quản lý 管理名` |
| Module / Màn hình | Friend info (友だち情報) — màn **Chi tiết friend › tab 友だち情報 › khối lịch sử thêm friend info (友だち情報追加履歴)**; nguồn ghi dữ liệu: **Form trả lời** có câu hỏi gắn 友だち情報 |

## Mô tả bug (bản dịch tiếng Việt)

Một câu hỏi trong form được cấu hình gắn câu trả lời vào một friend info (友だち情報) đã tạo sẵn (tùy chọn `すでに作成済みの友だち情報に回答を記録`). Sau khi friend info đó **bị xóa** ở màn quản lý friend info, friend vẫn trả lời form được, nhưng hệ thống **vẫn ghi một dòng lịch sử friend info** trỏ tới bản ghi đã bị xóa — dòng lịch sử này **không có tên quản lý (管理名)** của friend info, hiển thị trống ở tab friend info của màn chi tiết friend.

## Steps to reproduce

1. Set form có add câu hỏi dạng radio button
2. Radio button set `友だち情報の選択` = `すでに作成済みの友だち情報に回答を記録`
3. Chọn friend info A ⇒ lưu form
4. Thực hiện xóa friend info A tại màn friend info
5. Thực hiện trả lời form
6. Check detail friend vừa trả lời, tab friend info

## Expected result

- Không ghi lịch sử friend info đã bị xóa
- Hiển thị form result của friend bình thường
- Hiển thị detail câu trả lời của friend đó bình thường

## Actual result

- Vẫn ghi lịch sử friend info nhưng **không có tên quản lý 管理名** của friend info đó

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38727 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

- **Tracker**: `Bug tự detect` — bug do team tự phát hiện, không phải khách hàng báo. Status hiện tại: `Fix done - Đợi test` (done_ratio 100%).
- ⚠️ **Phạm vi fix bị giới hạn có chủ đích** (Journal #125841 — Hạnh Nguyễn, 2026-07-13): chỉ nhánh `すでに作成済みの友だち情報に回答を記録` (chọn friend info có sẵn) được xử lý theo đúng Expect trong ticket. Nhánh `自動で友だち情報を生成して回答を連携` (tự sinh friend info) **chưa sửa** — lý do dev đưa ra là performance + xử lý đồng thời nhiều user trả lời. ⇒ TC cho nhánh tự sinh **không được coi là fail** nếu hệ thống không tạo lại friend info mới; nhưng vẫn phải verify là **không sinh lịch sử mồ côi**.
- ⚠️ **Hàm bị sửa là hàm dùng chung** (`recordFriendInfoHistory` ở `app/Helpers/functions.php`) — Dev ghi rõ các luồng khác (đặt lịch / booking) cũng bị ảnh hưởng theo. Vùng regression rộng hơn form ⇒ xem `03-dev-impact.md`.
- Bản ghi **mồ côi cũ đã tồn tại trong DB trước khi fix** vẫn được giữ nguyên (không recover data) ⇒ màn lịch sử phải mở được bình thường với dữ liệu cũ thiếu 管理名.
- Môi trường phát hiện: ticket không ghi rõ.

## Dữ liệu định danh ca lỗi

<!-- Không có bot_id / friend cụ thể trong ticket. Dưới đây là bằng chứng DB dev do Dev đính kèm ở Journal #133033 (mục VERIFY) — dùng để dựng/đối chiếu case dữ liệu cũ. -->

| Mục | Giá trị |
|---|---|
| bot_id | `<ticket không ghi>` |
| Friend | `<ticket không ghi>` |
| Đối tượng cấu hình | Dòng `friend_info_history` mồ côi trên **DB dev**: `id=13, setting=1285, friend_info_name=NULL` · `id=14, setting=1287, friend_info_name=NULL` (setting đã bị xóa) |
| Thời điểm lỗi | `<ticket không ghi>` |
| Đối chứng | Trường friend info **còn tồn tại** ⇒ lịch sử phải có đủ thư mục + 管理名 + giá trị đăng ký |

## Journal / note từ Redmine (nguyên văn)

**Journal #125841 — Hạnh Nguyễn — 2026-07-13:**

```
Confirm:
1. Item Form chọn friend info có sẵn trong hệ thống: すでに作成済みの友だち情報に回答を記録 => Expext hiện tại trong redmine đúng rồi
2. Item Form chọn friend info tự tạo: 自動で友だち情報を生成して回答を連携 => Chưa sửa. Lý do: Hiện tại logic của mình lưu lại info id tự tạo khi click save form. Nếu info bị xóa => Khi friend trả lời check tạo friend info id mới sẽ bị tốn performance + xử lý case nhiều user trả lời cùng lúc cũng phức tạp
```

**Journal #133033 — AI LME Fix bug — 2026-08-26:** báo cáo Auto-fixbug (nguyên nhân / cách fix / đánh giá ảnh hưởng) — chép nguyên văn ở [03-dev-impact.md](03-dev-impact.md).
