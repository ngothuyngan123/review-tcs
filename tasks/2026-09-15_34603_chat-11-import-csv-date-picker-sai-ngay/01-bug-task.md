# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34603 — [Chat 1:1] Khi import CSV dạng date/birthday theo format support sau thì khi click vào ko hiển thị được đúng ngày đó trên date picker` |
| Module / Màn hình | `Chat 1:1 (FA-001) — panel 友だち情報 (Thông tin bạn bè) → trường kiểu 年月日 (date) / 誕生日 (birthday)` |

## Mô tả bug (bản dịch tiếng Việt)

> Description Redmine đã viết bằng tiếng Việt — giữ nguyên văn, không diễn giải lại.

1. Import CSV friend infor dạng date/ birthday theo các format support sau:
   - `yyyy-M-d`
   - `yyyy-MM-d`
   - `yyyy-M-dd`
   - `yyyy/MM/dd`
   - `yyyy/M/d`
   - `yyyy/M/dd`
   - `yyyy/MM/d`

2. tbl `friend_information_value` vẫn insert được đúng value theo định dạng trên. Nhưng ở Chat 1:1 thì đang hiển thị chung về format `yyyy.mm.dd`.

3. Chat 1:1: Click vào value ⇒ đang hiển thị date picker ko lấy được date tương ứng, bị hiển thị về value `yyyy.mm.dd`. Click ra ngoài thì bị báo lỗi sai format.

## Steps to reproduce

1. Import CSV friend information với trường kiểu **date (年月日)** / **birthday (誕生日)**, dùng 1 trong 7 format được support: `yyyy-M-d`, `yyyy-MM-d`, `yyyy-M-dd`, `yyyy/MM/dd`, `yyyy/M/d`, `yyyy/M/dd`, `yyyy/MM/d`.
2. Kiểm tra tbl `friend_information_value` — value được insert đúng theo định dạng gốc của file CSV.
3. Vào màn **Chat 1:1** → panel 友だち情報 → click vào value của trường ngày vừa import.
4. Click ra ngoài ô (blur).

## Expected result

- Chat 1:1 ⇒ click vào value ⇒ hiển thị date picker **lấy được date tương ứng** (đúng ngày đang lưu).

## Actual result

- Click vào value ⇒ date picker **không lấy được date tương ứng**, bị hiển thị về value `yyyy.mm.dd` (ô nhập bị bỏ trắng, date picker không mở đúng tháng/ngày).
- Click ra ngoài ⇒ **báo lỗi sai format** (`日付のフォーマットが無効です。`).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `26-02-2026-01-41-54.png` — https://redmine.watermelon.vn/attachments/download/23657/26-02-2026-01-41-54.png

## Ghi chú thêm của Leader

- **Điều kiện tiên quyết**: cần friend info field kiểu `年月日` và/hoặc trường 誕生日 mặc định; data phải được nạp qua **import CSV** (không phải chọn từ date picker) để value giữ nguyên định dạng gốc — giá trị chọn từ date picker luôn ra `yyyy-mm-dd` nên **không tái hiện được bug**.
- **Tần suất**: 100% với mọi value không đủ 2 chữ số tháng/ngày hoặc dùng dấu `/`.
- **Môi trường phát hiện**: ticket không ghi rõ env; bug nằm ở tầng client JS nên tái hiện được ở mọi env có data import CSV.
- Fix là **client-side only** (`public/js/chats/chat-v2.js`) → lưu ý cache asset JS sau deploy (REQ-007 phía Studio).
- ⚠️ Dev **KHÔNG tái hiện được trên dev** tại thời điểm fix (MySQL + web `host.docker.internal` Connection refused). Verify của Dev chỉ ở mức `lint` + chạy thử riêng hàm `normalizeDateItemValue` tách rời, **chưa chạy thật trên màn hình** → TCs phải verify end-to-end trên UI thật.
- ⚠️ Hành vi phụ Dev tự nêu: mở ô ngày rồi rời ô mà **không đổi gì** vẫn ghi lại giá trị theo chuẩn `yyyy-mm-dd` và **sinh 1 dòng lịch sử thay đổi thông tin bạn bè**. Cần TC xác nhận đây là hành vi chấp nhận được, không phải bug mới.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — ticket không ghi>` |
| Friend | `<chưa rõ — ticket không ghi>` |
| Đối tượng cấu hình | Friend info field kiểu `年月日` / 誕生日, value import từ CSV (vd `2026/1/5`, `2026-1-5`, `2026-01-5`, `2026-1-05`, `2026/01/05`, `2026/1/05`, `2026/01/5`) |
| Thời điểm lỗi | `2026/02/26` (ngày tạo ticket) |
| Đối chứng | Value đã ở dạng `yyyy-mm-dd` đủ 2 chữ số → click vào hiển thị đúng ngày, không lỗi |

## Journal / note từ Redmine (nguyên văn)

**Journal #133387 — AI LME Fix bug — 2026-08-28:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Ô sửa ngày trong khung Thông tin bạn bè của màn Chat 1:1 là ô nhập ngày chuẩn của trình duyệt, chỉ chấp nhận chuỗi yyyy-mm-dd đủ 2 chữ số. Giá trị nhập từ file CSV được lưu nguyên định dạng gốc (2026/1/5, 2026-1-5, 2026/01/05...) nên trình duyệt coi là không hợp lệ, bỏ trắng ô và bộ chọn ngày không lấy được ngày tương ứng. Khi bấm ra ngoài, màn hình gửi lại đúng chuỗi gốc đó lên máy chủ và bị chặn bởi bước kiểm tra định dạng chặt (chỉ nhận đủ 2 chữ số) nên hiện thông báo sai định dạng.

■ 2. CÁCH FIX
Sửa màn Chat 1:1 (public/js/chats/chat-v2.js): thêm 2 hàm nhận diện trường ngày và chuẩn hoá giá trị ngày, gọi ngay trong editItemInfo trước khi mở ô sửa — mọi định dạng đã lưu (2026-1-5, 2026-01-5, 2026-1-05, 2026/1/5, 2026/1/05, 2026/01/5, 2026/01/05, kèm cả phần giờ) được đổi về yyyy-mm-dd đủ 2 chữ số để ô nhập ngày của trình duyệt hiển thị đúng ngày và giá trị gửi lên khi rời ô qua được bước kiểm tra định dạng. Giá trị không đọc được thành ngày thì giữ nguyên, không tự ý ghi đè. Quét ngang: các chỗ dùng ô nhập ngày khác đều nhận giá trị do người dùng chọn từ bộ chọn nên không dính lỗi này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
editItemInfo (public/js/chats/chat-v2.js)
isDateItemInfo (public/js/chats/chat-v2.js — thêm mới)
normalizeDateItemValue (public/js/chats/chat-v2.js — thêm mới)
saveItemInfo (public/js/chats/chat-v2.js)
formatString (public/js/chats/chat-v2.js)
initFriendInfo (public/js/chats/chat-v2.js)
ChatController::getInfoDisplayChat (app/Http/Controllers/ChatController.php)
ChatController::saveSettingDisplayInfoItem (app/Http/Controllers/ChatController.php)
HandleImportCsv::readDataCSV_V1 (app/Console/Commands/HandleImportCsv.php)
friend_info.blade.php khối sửa ngày (resources/views/basic/chat/tab_right_side/friend_info.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - public/js/chats/chat-v2.js
 • 4.2 Data ảnh hưởng:
   - Không có — không sửa cấu trúc hay dữ liệu sẵn có. Chỉ khi người dùng mở ô sửa ngày trong Chat 1:1 rồi rời ô thì giá trị đang lưu được ghi lại theo chuẩn yyyy-mm-dd (đúng như máy chủ vẫn chuẩn hoá khi lưu).
 • 4.3 Tính năng liên quan:
   - 1-on-1 Chat (FA-001) — khung Thông tin bạn bè: ô sửa ngày và bộ chọn ngày hiển thị đúng giá trị đang lưu
   - Friend Information (FA-015) — trường kiểu Năm tháng ngày và ngày sinh khi sửa từ màn chat được lưu theo định dạng chuẩn

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: node --check public/js/chats/chat-v2.js: OK (không có file PHP nào bị sửa nên không cần php -l); Chạy thử riêng hàm normalizeDateItemValue trích từ file đã sửa với 7 định dạng nêu trong ticket: 2026-1-5 / 2026-01-5 / 2026-1-05 / 2026/01/05 / 2026/1/5 / 2026/1/05 / 2026/01/5 đều ra 2026-01-05; Chuỗi kèm giờ (2026-01-05 00:00:00, 2026-01-05T00:00:00) ra 2026-01-05; chuỗi rỗng / null / abc / 05-01-2026 / 2026-13-45 / 2026-02-30 đều trả null nên giữ nguyên giá trị gốc; git diff --stat origin/release_step_20260805...ai_fixbug_34603: chỉ 1 file public/js/chats/chat-v2.js, +31 dòng
   Bằng chứng: Ô nhập trong resources/views/basic/chat/tab_right_side/friend_info.blade.php dòng 79 là input type=date gắn thẳng v-model vào giá trị lấy từ DB; ChatController::saveSettingDisplayInfoItem chặn giá trị không khớp yyyy-mm-dd hoặc yyyy/mm/dd đủ 2 chữ số và trả về thông báo 日付のフォーマットが無効です。 (dòng 4537 cho ngày sinh mặc định, 4677 cho trường tự tạo kiểu Năm tháng ngày) — khớp triệu chứng báo lỗi sai format ở bước 3 của ticket; Bài học #37418 trong knowledge/lessons.md đã ghi nhận friend_information_value.value chứa cả 2 kiểu dấu / và - nên phía lọc phải xử lý cả hai; KHÔNG tái hiện được trên dev: MySQL host.docker.internal:3306 và web host.docker.internal:8000 đều không kết nối được tại thời điểm xử lý (Connection refused)

■ TỰ REVIEW (AI)
Bản sửa gói gọn trong màn Chat 1:1, thêm 2 hàm nhỏ và 5 dòng gọi trong editItemInfo, không đụng máy chủ, không đụng luồng nhập CSV, không đổi cách hiển thị danh sách. Đúng mong đợi ghi trong ticket là bộ chọn ngày phải lấy được ngày tương ứng. Đã đối chiếu bản sửa với nhánh phát hành mới nhất trên origin (nhánh phát hành trong máy đang tụt 79 commit nên đã lấy lại bản trên origin làm gốc).
 • Rủi ro / lưu ý khi test:
   - Khi người dùng mở ô sửa ngày rồi rời ô mà không đổi gì, giá trị đang lưu sẽ được ghi lại theo chuẩn yyyy-mm-dd và sinh 1 dòng lịch sử thay đổi thông tin bạn bè. Đây là hành vi vốn có của màn này (rời ô là lưu) và máy chủ cũng luôn chuẩn hoá về yyyy-mm-dd khi lưu, nên không tạo giá trị mới lạ.
   - Giá trị không đọc được thành ngày (chuỗi rác, ngày không tồn tại như 2026-02-30) vẫn giữ nguyên và vẫn báo lỗi định dạng khi rời ô — giữ đúng hành vi cũ, cố ý không tự ý sửa dữ liệu.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_34603 (nhánh gốc release_step_20260805, commit 8901ae8ce7, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 8 phút 38 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=4fb4f149-3211-4a3a-8ca7-2c6d587aabf0
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=34603
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
