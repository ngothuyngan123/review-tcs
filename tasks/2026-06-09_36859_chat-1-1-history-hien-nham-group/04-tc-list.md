<!-- sync-target: https://docs.google.com/spreadsheets/d/1ZOlqNd6P-kTgiw6f-9G6G88LLmVGzFY12UTy2Xs8Yrk/edit?gid=740905541 -->
# 04 — TC List (fetched từ Sheet)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1ZOlqNd6P-kTgiw6f-9G6G88LLmVGzFY12UTy2Xs8Yrk/edit?gid=740905541 (tab "Content: Hiển thị msg", Line 1565–1604, cột "Bug KH #36859") |

---

## TC List

> Fetch từ Sheet master. Cấu trúc cột gốc của tab khác template chuẩn (chỉ có TC ID / Module / Test Scenario / Steps / Expected Result / [cột status "Bug KH #36859"]). Các cột Type / Priority / Precondition / Output note / Assignee để trống — member fill khi review. Giá trị giữ NGUYÊN từ Sheet, KHÔNG sửa.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | [Chat 1:1] Mở hội thoại 1:1 bình thường | | | | Chọn friend A | Hiển thị đúng lịch sử chat và tên friend A | | | OK |
| TC002 | [Chat Group] Mở nhóm LINE bình thường | | | | Chọn group A | Hiển thị đúng lịch sử chat và tên group A | | | Test Bug |
| TC003 | [Race Condition] Chuyển từ hội thoại A sang B khi A đang loading | | | | Mở A → ngay lập tức mở B | Chỉ hiển thị lịch sử và tên của B | | | Test Bug |
| TC004 | [Race Condition] Chuyển A → B → C liên tục | | | | Click liên tục 3 hội thoại | Chỉ hiển thị dữ liệu của C | | | Test Bug |
| TC005 | [Race Condition] Response của A về sau khi đã chuyển sang B | | | | Mock network delay | Response của A bị bỏ qua<br>Hiển thị đúng lịch sử chat của B | | | Test Bug |
| TC006 | [Race Condition] Response của B về trước, A về sau | | | | Mở A → B nhanh | Hiển thị đúng lịch sử chat của B<br>Không bị ghi đè bởi dữ liệu A | | | Test Bug |
| TC007 | [Race Condition] Chuyển giữa 2 hội thoại liên tục nhiều lần | | | | A ↔ B nhiều lần | Không hiển thị sai lịch sử chat | | | Test Bug |
| TC008 | [Race Condition] Chuyển giữa group và friend | | | | Group A → Friend B | Hiển thị đúng dữ liệu Friend B | | | Test Bug |
| TC009 | [Refresh] Refresh khi đang ở hội thoại A | | | | Trigger refresh | Hiển thị đúng dữ liệu A | | | Test Bug |
| TC010 | [Refresh] Refresh xong mới chuyển hội thoại | | | | Mở A → refresh → mở B | Hiển thị đúng dữ liệu B | | | Test Bug |
| TC011 | [Send Message] Gửi tin nhắn tại A | | | | Send message | Lịch sử chat A cập nhật đúng | | | Test Bug |
| TC012 | [Send Message] Gửi tin nhắn rồi chuyển B ngay | | | | Send tại A → mở B | Không hiển thị dữ liệu A trên B | | | Test Bug |
| TC013 | [User Info] Kiểm tra tên user 1:1 | | | | Mở nhiều friend | Tên user đúng | | | Test Bug |
| TC014 | [User Info] Kiểm tra avatar user | | | | Mở nhiều friend | Avatar đúng | | | Test Bug |
| TC015 | [Group Info] Kiểm tra tên nhóm | | | | Mở nhiều group | Tên nhóm đúng | | | Test Bug |
| TC016 | [Group Info] Kiểm tra avatar nhóm | | | | Mở nhiều group | Avatar nhóm đúng | | | Test Bug |
| TC017 | [Pagination] Scroll load page tiếp theo khi đang xem friend | | | | Scroll friend list | Không đổi hội thoại đang chọn | | | OK |
| TC018 | [Pagination] Scroll load page tiếp theo khi đang xem group | | | | Scroll friend list | Không đổi hội thoại đang chọn | | | OK |
| TC019 | [Pagination] Đang xem group có bot_line_user_id = null rồi load more | | | | Scroll xuống cuối | Không bị chuyển sang hội thoại đầu tiên | | | Test Bug |
| TC020 | [Pagination] Load nhiều page liên tiếp | | | | Scroll nhiều lần | Không bị reset current conversation | | | Test Bug |
| TC021 | [Pagination] Load more khi hội thoại hiện tại là friend | | | | Scroll nhiều lần | Vẫn giữ hội thoại hiện tại | | | Test Bug |
| TC022 | [Pagination] Load more khi hội thoại hiện tại là group | | | | Scroll nhiều lần | Vẫn giữ hội thoại hiện tại | | | Test Bug |
| TC023 | [Search] Search friend | | | | Nhập keyword | Kết quả đúng | | | Test Bug |
| TC024 | [Search] Search khi đang mở group | | | | Mở group → search | Không bị đổi hội thoại ngoài ý muốn | | | Test Bug |
| TC025 | [Search] Clear search | | | | Search → Clear | Danh sách hiển thị đúng | | | Test Bug |
| TC026 | [Filter] Filter friend list | | | | Apply filter | Kết quả đúng | | | Test Bug |
| TC027 | [Filter] Filter khi đang mở group | | | | Apply filter | Không bị đổi hội thoại hiện tại | | | Test Bug |
| TC028 | [Filter] Clear filter | | | | Apply → Clear | Danh sách hiển thị đúng | | | Test Bug |
| TC029 | [Initial Load] Load màn Chat lần đầu | | | | Mở màn Chat | Auto select hội thoại đầu tiên | | | OK |
| TC030 | [Initial Load] Load màn Chat khi item đầu là group | | | | Mở màn Chat | Auto select đúng group đầu tiên | | | OK |
| TC031 | [Regression] Search sau khi fix | | | | Search nhiều lần | Hoạt động bình thường | | | Test Bug |
| TC032 | [Regression] Filter sau khi fix | | | | Filter nhiều lần | Hoạt động bình thường | | | Test Bug |
| TC033 | [Regression] Pagination sau khi fix | | | | Scroll load more | Hoạt động bình thường | | | Test Bug |
| TC034 | [Regression] Refresh sau khi fix | | | | Refresh nhiều lần | Không hiển thị sai lịch sử | | | Test Bug |
| TC035 | [Mixed Scenario] Đang xem group → load more → search → filter | | | | Thực hiện liên tiếp các thao tác | Vẫn hiển thị đúng hội thoại đang chọn | | | Test Bug |
| TC036 | Check mở màn hình chat từ màn detail friend (my_page) | | | | | Hiển thị đúng lịch sử chat của friend | | | Test Bug |
| TC037 | Check account staff thao tác | | | | | Hiển thị đúng lịch sử chat của từng friend giống như khi user chính thao tác | | | Test Bug |
| TC038 | Check đang mở 1 hội thoại thì có add friend mới | | | | | Vẫn hiển thị đúng hội thoại đang chọn<br>Khi reload màn hình mới hiện friend mới | | | Test Bug |
| TC039 | - Mở hội thoại của friend A -> friend A gửi message đến bot | | | | | Friend A hiển thị được message mới | Ở dev đang k có socket phải reload màn hình mới hiện message mới | | Test Bug |
| TC040 | - Mở hội thoại của friend A -> mở sang hội thoại friend B -> friend A gửi message đến bot | | | | | Friend B hiển thị đúng message, không bị hiện message của friend A<br>Friend A hiển thị được last message mới | | | Test Bug |

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3

<!-- Source: fetched từ Redmine #36859 Link TCs, tab "Content: Hiển thị msg", range A1565:J1604 (Line 1565–1604, header tại Line 1564) lúc 2026-06-09. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
