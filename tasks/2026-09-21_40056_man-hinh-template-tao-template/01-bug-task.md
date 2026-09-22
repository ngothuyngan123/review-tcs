# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40056 — Màn hình template, tạo template` |
| Module / Màn hình | Message Template (FA-010 / SC-001) — màn danh sách mẫu tin nhắn `メッセージテンプレート` (`/basic/message-template`) + màn tạo mẫu tin nhắn / nhóm mẫu tin nhắn `テンプレート作成` (`/basic/template-v2/add-template`, `/basic/template-v2/create-group`) |

## Mô tả bug (bản dịch tiếng Việt)

Sửa lại http code cho đúng ý nghĩa với các api, ajax

validate required đầu vào

Mọi query đều PHẢI ràng buộc theo bot đang đăng nhập

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket dạng yêu cầu rà soát / hardening, không phải 1 ca lỗi cụ thể. -->

## Expected result

<!-- (trống — Redmine không ghi) -->

## Actual result

<!-- (trống — Redmine không ghi) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40056 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — description chỉ có 3 dòng yêu cầu, không có steps / expected / actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix + regression impact**.

⚠️ Đây là ticket **Bug API** dạng hardening theo **3 trục**, không phải 1 ca lỗi end-user:
1. **HTTP code** — endpoint ajax trả sai mã: lỗi nghiệp vụ và lỗi hệ thống trong `catch` đều trả `200`; ngược lại nhánh chặn khi đang sao lưu dữ liệu lại trả `500`.
2. **Validate required đầu vào** — thiếu tham số vẫn chạy query / ghi theo giá trị rỗng rồi báo thành công (xoá theo id `null`, ghi đè danh sách message con thành chuỗi rỗng).
3. **Ràng buộc bot đang đăng nhập** — dò id là chạm được dữ liệu bot khác (cross-tenant). Trục này mới bổ sung ở journal #136618 (2026-09-15), **SAU** lần fix đầu (journal #134899, 2026-09-07).

⚠️ **Đã fix 2 vòng** — cần verify cả 2 phạm vi:
- Vòng 1 (commit `aa7eb13d44`, 20 file): HTTP code + validate required + refix 2 lỗi do AI review vòng 1 phát hiện — endpoint `GET .../park-template/list-template/{id}` nhận id qua **đường dẫn** nên rule required luôn trượt ⇒ mọi request trả `422` (3 nơi gọi hỏng); nút bật/tắt gửi giãn cách khôi phục trạng thái bằng phép đảo giá trị nên lật ngược sai khi request thất bại.
- Vòng 2 (commit `4c60a17f92`, 21 file): bổ sung ràng buộc `bot_id` cho mọi truy vấn của 2 màn.

⚠️ **Phạm vi CỐ Ý loại trừ** — 4 câu truy vấn ở nhánh **di chuyển / sắp xếp mẫu tin nhắn** KHÔNG được thêm lọc bot trong ticket này, vì ticket **#40979** (triển khai ngang lọc `bot_id`) đang sửa đúng 4 dòng đó. ⇒ TC cross-tenant cho nhánh move/sort **không thuộc phạm vi #40056**.

⚠️ **Điểm cần chú ý khi test ràng buộc bot** (theo mô tả Dev):
- 2 bảng `tmp_introduction` / `tmp_location` **không có cột `bot_id`** → ràng buộc gián tiếp qua template cha; soạn message mới vẫn cho id rỗng như cũ.
- 2 endpoint copy panel truyền `action_id` từ client: bảng `t_actions` **không có cột `bot_id`** (quyền sở hữu nằm ở `t_actions_detail.bot_id`), hàm nhân bản action dùng chung ~110 nơi → Dev chặn tại **nơi gọi** bằng helper riêng, action **chưa có detail nào thì cho qua** để không chặn nhầm.
- Nhánh tạo/cập nhật nhóm mẫu tin nhắn là chỗ Dev đánh giá nguy hiểm nhất (dữ liệu ghi có cả `bot_id` → dò id kéo hẳn nhóm bot khác sang bot mình).

⚠️ **Mức verify của Dev chỉ là `lint`** — chưa chạy được trên dev stack (không có phiên đăng nhập). Toàn bộ hành vi runtime (HTTP code thật, message validate tiếng Nhật thật, lọc bot thật) **chưa từng chạy** trước khi chuyển test.

⚠️ Môi trường phát hiện: ticket không ghi rõ. Branch QA checkout: `ai_fixbug_40056` (repo sns-line, nhánh gốc `release_step_20260805`).

## Journal / note từ Redmine (nguyên văn)

**Journal #134899 — AI LME Fix bug — 2026-09-07:** (vòng fix 1 — HTTP code + validate required)

```
■ 1. NGUYÊN NHÂN
Các endpoint ajax của màn danh sách template và màn tạo template/nhóm template trả HTTP code sai ý nghĩa: lỗi nghiệp vụ (đang sao lưu dữ liệu nên không cho thao tác, không tìm thấy template, tên rỗng/quá dài, lưu thất bại, quá hạn sửa nội dung trước giờ gửi) và cả lỗi hệ thống trong khối catch đều trả 200 (nghĩa là thành công), màn hình phải tự đoán qua cờ status/success trong thân phản hồi nên hệ thống giám sát không thấy lỗi; ngược lại nhánh chặn khi đang sao lưu lại trả 500 (nghĩa là server sập) cho một lỗi nghiệp vụ bình thường. Ngoài ra hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc: thiếu tham số vẫn chạy truy vấn/ghi theo giá trị rỗng rồi báo thành công (xoá theo id null, ghi đè danh sách message con thành chuỗi rỗng), hoặc rơi vào lỗi hệ thống thật. Hai khối catch còn bắt nhầm lớp ngoại lệ (Doctrine\DBAL\Driver\Exception là interface mà \Exception không implement) nên chưa bao giờ chạy, và một khối lấy mã ngoại lệ PHP (thường bằng 0) làm HTTP code.

■ 2. CÁCH FIX
Refix theo AI review vòng 1 — sửa 2 lỗi bắt buộc: (1) Endpoint lấy danh sách message con của nhóm mẫu tin nhắn (GET .../park-template/list-template/{id}) nhận id qua ĐƯỜNG DẪN, trong khi hàm kiểm tra dùng chung chỉ đọc dữ liệu body/query nên rule bắt buộc luôn trượt ⇒ mọi request đều bị trả 422, làm màn tạo/sửa nhóm mẫu tin nhắn không nạp được danh sách message con (3 nơi gọi đều hỏng). Đã nạp tham số đường dẫn vào dữ liệu kiểm tra trước khi validate; đã rà lại toàn bộ endpoint được thêm kiểm tra trong lần fix trước (6 ở màn danh sách + 18 ở màn tạo) đối chiếu với định nghĩa route: chỉ endpoint này lấy tham số từ đường dẫn, các endpoint còn lại đều nhận qua body/query nên không dính. Đã chạy thử bằng script với vendor thật của repo: trước sửa dữ liệu kiểm tra rỗng (fail), sau sửa nhận đúng giá trị (pass). (2) Nút bật/tắt gửi giãn cách: nhánh lỗi mới thêm khôi phục trạng thái bằng phép đảo giá trị, nên khi người dùng mở modal bấm lưu mà KHÔNG đổi gì và request thất bại thì màn hình lật ngược sai trạng thái so với máy chủ (và đổi kiểu chuỗi thành luận lý). Đã chụp lại giá trị đang hiển thị trước khi ghi đè và khôi phục đúng giá trị đó cho cả biến hiển thị lẫn biến trong modal.

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l trên 2 file controller: No syntax errors detected; node --check trên 14 file JS đã sửa + file mới ajax-error.js: OK; Biên dịch 4 file blade bằng Illuminate BladeCompiler rồi php -l: No syntax errors detected; Chạy thử Illuminate\Validation\Factory với gói ngôn ngữ ja của dự án cho 10 tổ hợp rule: message hiển thị trọn tiếng Nhật (vd フォルダを選択してください。 / フォルダ名は20文字以内で入力してください。 / メッセージ内容の形式が正しくありません。); Rà lại từng nơi gọi bằng script đối chiếu ngược URL của khối $.ajax chứa nhánh lỗi vừa sửa: 21/21 khớp đúng endpoint dự kiến
   Bằng chứng: Doctrine\DBAL\Driver\Exception trong vendor là interface extends Throwable -> \Exception không implement, xác nhận 2 khối catch cũ không bao giờ chạy; Kiểm tra middleware ConvertEmptyStringsToNull có trong app/Http/Kernel.php -> chuỗi rỗng thành null nên rule nullable hoạt động đúng với các id màn hình cố ý gửi rỗng; Đối chiếu 7 màn khác cùng gọi /ajax/template-v2/get-data: không màn nào gửi template_id nên rule nullable không ảnh hưởng; Nút trang trước/trang sau của danh sách có v-if chặn nên page luôn >= 1, rule min:1 an toàn; Chưa chạy được trên dev stack (không có phiên đăng nhập) — verify dừng ở mức lint + compile + thử bộ validate

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40056 (nhánh gốc release_step_20260805, commit aa7eb13d44, 20 file)  [đã push]
```

**Journal #136618 — AI LME Fix bug — 2026-09-15:** (vòng fix 2 — bổ sung ràng buộc bot đang đăng nhập)

```
■ 2. CÁCH FIX
Bổ sung theo yêu cầu human (sau khi đã push): MỌI truy vấn của 2 màn trong phạm vi ticket phải ràng buộc theo bot đang đăng nhập — trước đây nhiều endpoint nhận id từ client rồi đọc/ghi/xoá chỉ theo id, nên tài khoản bất kỳ dò id là chạm được dữ liệu bot khác. Màn danh sách mẫu tin nhắn: endpoint điều phối (xoá thư mục, xoá 1 mẫu, xoá nhiều mẫu — câu xoá hàng loạt nhận thẳng danh sách id từ client), xoá mẫu tin nhắn, lấy danh sách message con của nhóm, xoá message trong nhóm, nhân bản mẫu tin nhắn. Màn tạo mẫu tin nhắn/nhóm: lưu mẫu tin nhắn (đổi tên/đổi thư mục), sắp xếp message con, xoá nhiều message con, lấy danh sách URL chuyển hướng, lấy dữ liệu thẻ giới thiệu và vị trí, tạo/cập nhật nhóm (chỗ này nguy hiểm nhất: dữ liệu ghi có cả bot_id nên dò id là kéo hẳn nhóm của bot khác sang bot mình), xem trước message con. 2 bảng tmp_introduction/tmp_location KHÔNG có cột bot_id nên ràng buộc gián tiếp qua template cha đã lọc bot (soạn message mới vẫn cho id rỗng như cũ). 2 endpoint copy panel truyền action_id từ client: bảng t_actions KHÔNG có cột bot_id (quyền sở hữu ở t_actions_detail.bot_id) và hàm nhân bản action đang dùng chung ~110 nơi, nên chặn tại nơi gọi bằng helper riêng trong controller (action chưa có detail nào thì cho qua để không chặn nhầm) thay vì sửa hàm chung. Đã xác minh 12/12 chỗ tạo template đều ghi bot_id nên lọc theo bot không làm mất dữ liệu hợp lệ. CỐ Ý không đụng 4 câu truy vấn ở nhánh di chuyển/sắp xếp mẫu tin nhắn vì ticket #40979 (triển khai ngang lọc bot_id) đang sửa đúng 4 dòng đó — tránh sửa trùng và xung đột khi merge.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40056 (nhánh gốc release_step_20260805, commit 4c60a17f92, 21 file)  [đã push]
```
