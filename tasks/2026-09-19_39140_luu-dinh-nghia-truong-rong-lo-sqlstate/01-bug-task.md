# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #39140 bởi `/new-task` (2026-09-19). Metadata Redmine tra thẳng trên ticket.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39140 — [LME-Studio] Lưu định nghĩa trường với 管理名 rỗng trả về chuỗi lỗi SQL thô (rò rỉ SQLSTATE) thay vì message sạch` |
| Module / Màn hình | Friend Information Management (FA-015) — màn 友だち情報管理 (form tạo/sửa định nghĩa trường thông tin bạn bè, SCR-FRI-02) · API `POST /basic/save-setting-info-friend` |

## Mô tả bug (bản dịch tiếng Việt)

*Bug từ LME Test Studio* — severity Low
Task: #17
Test case: id 1958

## Steps to reproduce

1. Đăng nhập Admin (basic_access), context bot hợp lệ
2. Gọi `POST /basic/save-setting-info-friend` với payload `{id:"", title:"", group_id:0, type_data:4}`
3. Quan sát body JSON trả về

## Expected result

- Hoặc BE validate required và trả message nghiệp vụ sạch (vd 「友だち情報（管理名）を1つ以上設定して下さい。」), hoặc lưu bình thường — KHÔNG trả chuỗi SQLSTATE thô ra client.

## Actual result

- HTTP 200 `{status:false, msg:"SQLSTATE[23000]: Integrity constraint violation: 1048 Column 'title' cannot be null (SQL: insert into `friend_information_setting` ...)"}`. Message SQL thô lộ cấu trúc bảng/câu lệnh cho client; không có validate required ở BE nên lỗi rơi xuống tầng DB.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- phpunit log 1958 — https://redmine.watermelon.vn/attachments/download/28508/phpunit%20log%201958

## Ghi chú thêm của Leader

- Bug do **AI Auto test** tự detect (tracker "Bug tự detect"), không phải khách hàng báo.
- **Không tái hiện được qua giao diện** — FE (`create.js`) đã chặn 管理名 rỗng sẵn; chỉ tái hiện bằng **gọi thẳng API**.
- Fix đã qua **3 vòng** (journal #131890 → #137195, 2026-09-19). Vòng v3 **mở rộng phạm vi** so với ticket:
  - Thêm guard chủ sở hữu chéo bot (request mang id của bot khác → HTTP 404 `設定が見つかりません`) — lỗi bảo mật phát hiện khi AI tự review.
  - **Đính chính**: Tag Management (FA-012) **KHÔNG** gọi endpoint này (`saveInforFriend` trong `add_tag.js` / `edit_v2.js` là code chết) → caller sống duy nhất là màn 友だち情報管理.
- Branch fix `ai_fixbug_39140`, base `release_step_20260827` (journal #137188). Fix **chưa merge vào release** tại thời điểm fetch.
- Mobile (`FriendInfoMobileController::saveFriendInfoField`) có cùng lỗi nhưng Dev khai **ngoài phạm vi**.

## Journal / note từ Redmine (nguyên văn)

> Journal #131890 (AI LME Fix bug, 2026-08-21) là báo cáo fix vòng 1. Journal #137195 bên dưới **thay thế** nó: giữ nguyên mục 1–2 và bổ sung guard chéo bot + đính chính caller. Xem bản đầy đủ trên Redmine; nội dung đã parse vào `03-dev-impact.md`.

**Journal #137188 — Kieu Son Tung — 2026-09-19:**

```
branch release release_step_20260827
```

**Journal #137195 — AI LME Fix bug — 2026-09-19:** (trích mục CẬP NHẬT v3 — các mục 1–6 đầy đủ đã chép vào `03-dev-impact.md`)

```
■ CẬP NHẬT 2026-09-19 (tự review v3): (1) nhánh đã được merge release mới nhất release_step_20260827 (commit 74015bf5ad do tungks thực hiện) — nhánh nay 0 commit behind release, merge sạch, không làm rơi fix; fix VẪN CHƯA vào release nên cần human merge PR ai_fixbug_39140 → release_step_20260827. (2) THEO YÊU CẦU HUMAN, đã fix thêm lỗi BẢO MẬT phát hiện khi tự review (commit fff7807509, CHƯA PUSH): endpoint lưu định nghĩa trường chỉ có middleware basic_access và lấy id trần từ request mà không kiểm chủ sở hữu — câu update chính có lọc bot_id nhưng các câu kèm theo thì không, nên admin của bot A gửi id của bot B là sửa/xoá được dữ liệu bot B (set null cột action, xoá option/value, ghi đè bộ đếm). Dùng lại helper isInfoSettingOfCurrentBot() mà #40697 đã thêm làm guard ngay cửa vào hàm, trả HTTP 404 (không dùng abort() vì sẽ bị khối catch nuốt thành lỗi hệ thống 200); mã mặc định d_x, mã âm và trường hợp tạo mới vẫn đi tiếp như cũ. Đã kiểm không hồi quy: màn sửa (editInfo) vốn đã kiểm chủ sở hữu bằng đúng 2 nguồn của helper trước khi render id ra trang, nên guard là no-op với mọi luồng hợp lệ. (3) ĐÍNH CHÍNH report: hàm saveInforFriend trong public/js/tag/add_tag.js và public/js/tag/edit_v2.js là CODE CHẾT (không nơi nào gọi; nút 保存 của 2 màn thẻ gọi saveTag() → /ajax/save-tag), nên caller sống duy nhất của endpoint này là màn 友だち情報管理 (create.js) — Tag Management KHÔNG bị ảnh hưởng như report ban đầu khai.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39140 (nhánh gốc release_step_20260827, commit fff7807509, 1 file)  [đã push]
```
