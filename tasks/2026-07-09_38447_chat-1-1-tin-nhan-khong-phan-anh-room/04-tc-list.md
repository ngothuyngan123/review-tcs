<!-- sync-target: https://docs.google.com/spreadsheets/d/1Yo9Qp4kfeqvpxl85uXFT3-MbrECSQbT0kK0PiSgyUjM/edit?gid=1706615087#gid=1706615087 -->

# 04 — TC List (fetch từ Redmine #38447 Link TCs — read-only)

> ⚠️ **TCs này fetch nguyên văn từ Google Sheet human (tab "Test callback friend", row 198~243).** KHÔNG sửa Title/Expected dù bug fix đổi behavior. Đây là input read-only cho `/review-tc`.
>
> Sheet nguồn có cấu trúc lồng (Main Function → nhóm scenario → case → biến thể → expected → note → status). Đã map: **Precondition** = nhóm scenario (cột C), **Title** = case (cột D), **Steps** = biến thể (cột E), **Expected** = cột F, **Output note** = cột G, **Status** = cột H. Ô merge được fill xuống. Ô trống ở nguồn giữ trống (nguồn dùng merge kế thừa expected từ hàng trên).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | v1 |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1Yo9Qp4kfeqvpxl85uXFT3-MbrECSQbT0kK0PiSgyUjM/edit?gid=1706615087#gid=1706615087 (tab "Test callback friend", row 198~243) |

---

## TC List

### Main Function 1 — Check các case callback thường (Không bị gộp chung callback)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | send 1 message | | | User send message chat 1:1 đến bot | - | Tạo đủ các message cho user => hiển thị ở màn hình chat 1:1<br>- update được status của friend là uncomfirm<br>- Số count user uncomfirm update đúng | | | OK |
| TC002 | send nhiều message liên tiếp | | | User send message chat 1:1 đến bot | - | | | | OK |
| TC003 | 2 user cùng gửi message đến bot | | | User send message chat 1:1 đến bot | - | - Tạo đủ message cho các user =>hiển thị ở màn chat 1:1<br>- status comfirm và số count comfirm update được đúng | | | OK |
| TC004 | 3 user cùng gửi message đến bot | | | User send message chat 1:1 đến bot | - | | | | OK |
| TC005 | Check có 2 callback message cùng lúc thỏa mãn autoreply | | | User send message chat 1:1 đến bot | - | - tạo đủ các message<br>- Action được đầy đủ cho từng callback, không bị send duplicate | | | OK |
| TC006 | Check có 2 callback message cùng lúc trong đó:<br>- có callback thỏa mãn autoreply<br>- có callback không thỏa mãn autoreply | | | User send message chat 1:1 đến bot | - | - tạo đủ các message<br>- Action được đúng cho từng callback, không bị send duplicate | | | OK |
| TC007 | friend gửi message media đến bot | | | User send message chat 1:1 đến bot | - | Message media hiển thị được bình thường trên chat 1:1 | | | OK |
| TC008 | Có nhiều postback của button cùng lúc | | | User send message chat 1:1 đến bot | 1 user click button nhiều lần | - Action được đúng cho từng callback, không bị send duplicate | action cùng 1 button trong vòng 3s thì sẽ chỉ action 1 lần | | OK |
| TC009 | Có nhiều postback của button cùng lúc | | | User send message chat 1:1 đến bot | nhiều user cùng click button | - Action được đúng cho từng callback, không bị send duplicate | | | OK |
| TC010 | Có nhiều postback của richmenu cùng lúc | | | User send message chat 1:1 đến bot | 1 user click richmenu nhiều lần | - Action được đúng cho từng callback, không bị send duplicate | action cùng 1 vùng của richmenu trong vòng 3s thì sẽ chỉ action 1 lần | | OK |
| TC011 | Có nhiều postback của richmenu cùng lúc | | | User send message chat 1:1 đến bot | nhiều user cùng click richmenu | | | | OK |
| TC012 | Có nhiều postback của image map cùng lúc | | | User send message chat 1:1 đến bot | 1 user click image nhiều lần | - Action được đúng cho từng callback, không bị send duplicate | action cùng 1 vùng của image trong vòng 3s thì sẽ chỉ action 1 lần | | OK |
| TC013 | Có nhiều postback của image map cùng lúc | | | User send message chat 1:1 đến bot | nhiều user cùng click image | | | | OK |
| TC014 | Có nhiều postback của video cùng lúc | | | User send message chat 1:1 đến bot | - | - Action được đúng cho từng callback, không bị send duplicate | | | OK |
| TC015 | Check có nhiều callback resend Line cùng lúc | | | User send message chat 1:1 đến bot | - | Action được đúng cho user | | | OK |
| TC016 | Check dummy data | | | User send message chat 1:1 đến bot | 1 user có nhiều callback đến vào cùng 1 thời điểm | | | | OK |
| TC017 | Check dummy data | | | User send message chat 1:1 đến bot | nhiều user có callback vào cùng 1 thời điểm | | | | OK |
| TC018 | Có callback follow bot: friend chưa có conversation hoặc conversation không bị bot block | | | User send message chat 1:1 đến bot | - | xử lý callback được bình thường | | | OK |
| TC019 | Có callback follow nhưng conversion đang bị block bởi bot | | | User send message chat 1:1 đến bot | - | | | | OK |
| TC020 | Callback unfollow | | | User send message chat 1:1 đến bot | - | | | | OK |
| TC021 | send 1 message | | | User send message đến group | - | Tạo đủ các message cho group => hiển thị ở màn hình chat 1:1<br>- update được status của group là uncomfirm<br>- Số count user uncomfirm update đúng | | | OK |
| TC022 | send nhiều message liên tiếp | | | User send message đến group | - | | | | OK |
| TC023 | 2 user cùng gửi message đến group | | | User send message đến group | - | | | | OK |
| TC024 | 3 user cùng gửi message đến group | | | User send message đến group | - | | | | OK |
| TC025 | User click button được gủi trong group | | | User send message đến group | 1 user click | - Có tạo message cho các callback message<br>- Callback postback thì bỏ qua không action do chưa support send action cho group | | | OK |
| TC026 | User click button được gủi trong group | | | User send message đến group | nhiều user cùng click | | | | OK |
| TC027 | Check dummy data | | | User send message đến group | 1 user có nhiều callback đến vào cùng 1 thời điểm | Tạo đủ các message cho group => hiển thị ở màn hình chat 1:1<br>- update được status của group là uncomfirm<br>- Số count user uncomfirm update đúng | | | OK |
| TC028 | Check dummy data | | | User send message đến group | nhiều user có callback vào cùng 1 thời điểm | | | | OK |
| TC029 | Check có callback message của friend và callback message của group cùng lúc | | | User send message đến group | - | - Tạo đủ message cho friend và group<br>- status comfirm và số count uncomffirm update đúng | | | OK |
| TC030 | Check có callback của 2 group khác nhau cùng lúc | | | User send message đến group | - | Tạo đủ các message cho từng group => hiển thị ở màn hình chat 1:1<br>- update được status của group là uncomfirm<br>- Số count user uncomfirm update đúng | | | OK |
| TC031 | Callback join group | | | User send message đến group | - | xử lý callback được bình thường | | | OK |
| TC032 | Callback leave group | | | User send message đến group | - | | | | OK |

### Main Function 2 — Check case các callback gị gộp chung với nhau bởi Line

> **Cách test (áp dụng cả nhóm):** 1. Dùng postman call để tạo 1 callback có chứa nhiều callback bên trong. 2. Để các callback bị ignore ở trên, các callback không bị ignore ở dưới. 3. Job chạy xử lý callback chỉ ignore đúng callback lỗi, các callback còn lại vẫn được xử lý đúng.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC033 | Tạo 1 callback gồm:<br>- 1 callback follow của friend A nhưng conversion đang bị block bởi bot<br>- 1 callback message của friend B | | | Callback gộp chung (postman) | - | - Callback follow bị ignore -> Friend A vẫn hiện trạng thái bị block bởi bot<br>- callback message được xử lý => Tạo được message cho friend B | Duy bảo tạm thời không test các case loại callback khác nhau, sẽ chỉ add thêm monitor để theo dõi | | Reject |
| TC034 | Tạo 1 callback gồm:<br>- 1 callback message của friend A có source ≠ user/group (set type = room)<br>- 1 callback message của friend B có source = user<br>- 1 callback message của friend C có source = group | | | Callback gộp chung (postman) | - | - Callback 1 bị ignore -> Friend A không tạo message<br>- callback 2,3 được xử lý => Tạo được message cho friend B và C | V | | OK |
| TC035 | Tạo 1 callback gồm:<br>- 1 postback của friend A có source ≠ user<br>- 1 postback message của friend B có source = user<br>- 1 callback message của friend C có source = group | | | Callback gộp chung (postman) | - | - postback 1 bị ignore -> Friend A không được action<br>- postback 2 được xử lý => Friend B được send action<br>- callback 3 được xử lý =. friend C được tạo message | | | OK |
| TC036 | Tạo 1 callback gồm:<br>- 1 callback video nhưng not found user<br>- 1 callback message thường<br>- 1 callback message media | | | Callback gộp chung (postman) | - | - Callback 1 bị ignore<br>- callback 2,3 được xử lý => Tạo được message cho friend | Hiện tại case này đang chỉ sửa lý callback của video, còn callback của message sẽ không xử lý tiếp được => Case type callback khác nhau này tạm thời để sau | | Reject |
| TC037 | Tạo 1 callback gồm nhiều callback message thường | | | Callback gộp chung (postman) | - | Xử lý được tất cả các callback:<br>- Tạo đủ message cho user<br>- send autoreply nếu thỏa mãn | V | | OK |
| TC038 | Tạo 1 callback gồm nhiều callback group | | | Callback gộp chung (postman) | - | | | | OK |
| TC039 | Tạo 1 callback gồm nhiều postback | | | Callback gộp chung (postman) | - | | | | OK |
| TC040 | Tạo 1 callback gồm callback group + callback message thường | | | Callback gộp chung (postman) | - | | | | OK |
| TC041 | Tạo 1 callback gồm callback group + postback user | | | Callback gộp chung (postman) | - | | | | OK |
| TC042 | Tạo Callback complete video gồm NOT_FRIEND + Friend VideoPlayComplete | | | Callback gộp chung (postman) | - | | | | OK |
| TC043 | Gửi callback chứa nhiều VideoPlayComplete. | | | Callback gộp chung (postman) | - | | | | OK |
| TC044 | Callback follow đầu BLOCKED_BY_BOT.<br>Callback Follow sau hợp lệ. | | | Callback gộp chung (postman) | - | | - Case này dùng postman test nếu tạo 2 callback của 2 user khác nhau thì cả 2 callback đấy khi chạy đều là của 1 user => Case này không check được Duy bảo add monitor để check thêm liệu có case này hay không<br>- Case set 2 callback follow của cùng 1 user thì nếu user bị bot block thì expect là cả 2 callback đều bị ignore => sau khi xử lý toàn bộ callback thì is_block của friend không bị thay đổi | | OK |
| TC045 | Gửi callback nhiều event hỗn hợp (Message, Postback, Follow, Video...). | | | Callback gộp chung (postman) | - | | Duy bảo tạm thời không test các case loại callback có cả follow và callback khác chung nhau => add thêm monitor để chek thêm có tồn tại case này không | | Reject |

### Chú thích cột

- **Type / Priority / Assignee**: nguồn Sheet không có → để trống.
- **Status** (từ nguồn): `OK` = pass, `Reject` = case bị loại/không test (xem Output note để biết lý do).
- **Output note**: giữ nguyên ghi chú của Dev/Tester trong Sheet (vd "V" = verified, ghi chú của "Duy bảo").

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Các case callback gộp chung (Main Function 2) cần dùng **postman** để tạo callback đa event.

---

## Member tự check trước khi submit

<member điền sau khi review>

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3

<!-- Source: fetched từ Redmine #38447 Link TCs (journal #125207), range A198:J243 tab "Test callback friend" lúc 2026-07-09. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
