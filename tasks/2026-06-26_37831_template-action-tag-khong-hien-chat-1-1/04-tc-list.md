<!-- sync-target: https://docs.google.com/spreadsheets/d/1ZOlqNd6P-kTgiw6f-9G6G88LLmVGzFY12UTy2Xs8Yrk/edit?gid=740905541#gid=740905541 -->

# 04 — TC List (fetch read-only từ Sheet human)

> ⚠️ TCs dưới đây fetch **read-only** từ Sheet human (tab "Content: Hiển thị msg", dòng 1612–1678). **KHÔNG sửa** giá trị (Title/Steps/Expected/Status) — giữ nguyên như Sheet, kể cả khi nghi không còn đúng sau fix. Sheet dùng format phân cấp của team (Main Function → Sub-function → Case → Step), KHÔNG phải 10 cột chuẩn template; ô trống = merge với ô phía trên.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1ZOlqNd6P-kTgiw6f-9G6G88LLmVGzFY12UTy2Xs8Yrk/edit?gid=740905541#gid=740905541 (Sheet "Content: Hiển thị msg", dòng 1612–1678) |

---

## TC List

> Tiêu đề bug (cột B, dòng 1612): **Bug KH #37831: [18-06-2026][T11287][Template] Khách báo 2 lỗi về Template: template gửi qua action khi thêm tag không hiển thị trên màn hình chat 1:1 ở trang quản trị (dù điện thoại nhận được), và tên quản lý template chứa ký tự '&' nửa chiều rộng hiển thị sai**

| Main Function | Sub-function | Case | Steps | Expected result | Output note | Status |
|---|---|---|---|---|---|---|
| **1. Template gửi qua Action không hiển thị ở chat 1:1** | | | | | | |
| | Send action template bởi web | Giữ nguyên các template con → send | Chỉ edit template group (edit name, edit folder ..) | Hiển thị đúng nội dung template mới nhất<br>- Check màn chat 1:1<br>- check phía line user | | Test Bug |
| | | Thêm template con | thêm template 2 → send | | | Test Bug |
| | | | thêm tiếp template 3 → send | | | Test Bug |
| | | | thêm template 4,5 → send | | | Test Bug |
| | | Xóa template con | Xóa template 4,5 → send | | | Test Bug |
| | | | Xóa template 3 → send | | | Test Bug |
| | | | Xóa template 2 → send | | | Test Bug |
| | | Thay đổi thứ tự các template con → gửi | sort lần 1 → gửi | | | Test Bug |
| | | | sort lần 2 → gửi | | | Test Bug |
| | | | sort nhiều lần liên tiếp → gửi | | | Test Bug |
| | | Edit nội dung template con | edit lần 1 → gửi | | | Test Bug |
| | | | edit tiếp lần 2 → gửi | | | Test Bug |
| | | | edit nhiều lần → gửi | | | Test Bug |
| | | kết hợp nhiều thao tác cùng lúc | - xoa template 1<br>- edit template 2<br>- tạo thêm template 3<br>- đổi thứ tự template<br>=> gửi template | | | Test Bug |
| | | Check template đơn hoạt động đúng | send template đơn<br>→ vào edit nội dung template đơn → send lại | | | Test Bug |
| | | Verify refresh chat | - gửi template<br>- refesh màn hình chat | Tin nhắn vẫn hiển thị đúng | | Test Bug |
| | | Check send nhiều action template 1 lần | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send action template cho nhiều user cùng lúc | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send template chứa nhiều template con (10 template con) | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | Send action template bởi job | Giữ nguyên các template con → send | Chỉ edit template group (edit name, edit folder ..) | Hiển thị đúng nội dung template mới nhất<br>- Check màn chat 1:1<br>- check phía line user | | OK |
| | | Thêm template con | thêm template 2 → send | | | OK |
| | | | thêm tiếp template 3 → send | | Bug Tester #37907 | OK |
| | | | thêm template 4,5 → send | | | OK |
| | | Xóa template con | Xóa template 4,5 → send | | | OK |
| | | | Xóa template 3 → send | | | OK |
| | | | Xóa template 2 → send | | | OK |
| | | Thay đổi thứ tự các template con → gửi | sort lần 1 → gửi | | | NG |
| | | | sort lần 2 → gửi | | | NG |
| | | | sort nhiều lần liên tiếp → gửi | | | NG |
| | | Edit nội dung template con | edit lần 1 → gửi | | | OK |
| | | | edit tiếp lần 2 → gửi | | | OK |
| | | | edit nhiều lần → gửi | | | OK |
| | | kết hợp nhiều thao tác cùng lúc | - xoa template 1<br>- edit template 2<br>- tạo thêm template 3<br>- đổi thứ tự template<br>=> gửi template | | | Test Bug |
| | | Check template đơn hoạt động đúng | send template đơn<br>→ vào edit nội dung template đơn → send lại | | | Test Bug |
| | | Verify refresh chat | - gửi template<br>- refesh màn hình chat | Tin nhắn vẫn hiển thị đúng | | OK |
| | | Check send nhiều action template 1 lần | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send action template cho nhiều user cùng lúc | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send template chứa nhiều template con (10 template con) | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | Send template ở app mobile | Giữ nguyên các template con → send | Chỉ edit template group (edit name, edit folder ..) | Hiển thị đúng nội dung template mới nhất<br>- Check màn chat 1:1<br>- check phía line user | | OK |
| | | Thêm template con | thêm template 2 → send | | | OK |
| | | | thêm tiếp template 3 → send | | | OK |
| | | | thêm template 4,5 → send | | | OK |
| | | Xóa template con | Xóa template 4,5 → send | | | OK |
| | | | Xóa template 3 → send | | | OK |
| | | | Xóa template 2 → send | | | OK |
| | | Thay đổi thứ tự các template con → gửi | sort lần 1 → gửi | | | OK |
| | | | sort lần 2 → gửi | | | OK |
| | | | sort nhiều lần liên tiếp → gửi | | | OK |
| | | Edit nội dung template con | edit lần 1 → gửi | | | OK |
| | | | edit tiếp lần 2 → gửi | | | OK |
| | | | edit nhiều lần → gửi | | | OK |
| | | kết hợp nhiều thao tác cùng lúc | - xoa template 1<br>- edit template 2<br>- tạo thêm template 3<br>- đổi thứ tự template<br>=> gửi template | | | OK |
| | | Check template đơn hoạt động đúng | send template đơn<br>→ vào edit nội dung template đơn → send lại | | | Test Bug |
| | | Verify refresh chat | - gửi template<br>- refesh màn hình chat | Tin nhắn vẫn hiển thị đúng | | Test Bug |
| | | Check send nhiều action template 1 lần | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send action template cho nhiều user cùng lúc | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| | | Check send template chứa nhiều template con (10 template con) | | Hiện đúng template phía user và màn chat 1:1 | | Test Bug |
| **2. Hiển thị tên Template chứa "&" và ký tự half-width** | Template name chứa "&" full-width | A＆B | | | Hiển thị đúng tên template đã nhập ở các màn<br>Ký tự & hiển thị đúng, không bị hiện thành &amp; | | OK |
| | Template name chứa "&" half-width | A&B | | | | | OK |
| | Template name chứa nhiều dấu "&" cả full-width và half-width | A&B&C＆D | | | | | OK |
| | Template name chứa ký tự half-width | ABC123-_() | | | | | OK |
| | Template name chứa ký tự full-width + half-width | ＡＢＣ123 | | | | | OK |
| | Tiếng Nhật + "&" | - テスト＆サンプル<br>- テスト&サンプル | | | | | OK |
| | Tiếng Nhật + half-width | ﾃｽﾄABC123 | | | | | OK |
| | Template name chứa HTML special characters | < > & ' " | | | | | OK |

> **Lưu ý cột:** Sheet gốc cột D = "Case", cột E = "Steps" cho nhóm 1; với nhóm 2 cột C = case name, cột D = giá trị input mẫu. Bảng trên gộp theo đúng vị trí ô gốc.

<!-- Source: fetched từ Redmine #37831 Link TCs (journal #122638), range A1612:J1678 tab "Content: Hiển thị msg" lúc 2026-06-26. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
