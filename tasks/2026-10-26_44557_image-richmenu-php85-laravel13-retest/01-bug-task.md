# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44557 — [#43845] Regression tính năng リッチメニュー(/basic/image-richmenu) trên PHP 8.5 / Laravel 13` |
| Module / Màn hình | `Tạo ảnh rich menu (「リッチメニュー画像作成」) — /basic/image-richmenu` |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây **KHÔNG phải bug ticket thông thường** — là **subtask QA retest** tách riêng phạm vi "Tạo ảnh Rich Menu" từ ticket cha #43845 (Nâng cấp module PHP Web lên PHP 8.5 + Laravel 13), không phải yêu cầu phát triển tính năng mới.

### Task nguồn và mục tiêu

- Task cha / nguồn: #43845 — Nâng cấp module PHP Web lên PHP 8.5 + Laravel 13.
- Tính năng: リッチメニュー画像作成.
- URL: /basic/image-richmenu.
- Mục tiêu: bảo đảm tính năng hoạt động đúng trên bản nâng cấp, giữ hành vi và kết quả phía người dùng theo yêu cầu đã chốt tại #43845.

### Nhánh và mốc đối chiếu

- Nhánh cần test: `ai_studio_implement_43845`.
- Dùng bản bàn giao mới nhất của #43845; ghi lại commit thực tế khi chạy test.
- Mốc đối chiếu: nhánh/commit production base được ghi trong bản bàn giao tương ứng của #43845.
- Kế thừa các thay đổi spec, ngoại lệ và khác biệt đã được chấp nhận tại #43845. **Không mặc định mọi kết quả khác production đều là bug.**

### Phạm vi kiểm tra

- Danh sách ảnh: hiển thị dữ liệu cũ, thư mục, lưới ảnh và các thao tác hàng loạt.
- Tạo mới, chỉnh sửa, lưu và mở lại ảnh: tên quản lý, layout, chữ, ảnh nền và các thành phần được hỗ trợ.
- Upload và xử lý ảnh nền: kiểm tra định dạng, dung lượng, kích thước và thông báo lỗi theo spec hiện hành.
- Xử lý ảnh trên thư viện mới: thu nhỏ ảnh nền, render chữ, bố cục, màu sắc và chất lượng ảnh đầu ra.
- Kiểm tra ảnh nền lớn được thu về 2048 px và ảnh xuất có khung 2500 px theo testcase nguồn; đối chiếu đầy đủ kích thước theo layout thực tế.
- Sao chép ảnh; bản sao giữ đúng nội dung và có thể chỉnh sửa độc lập.
- Tải xuống một ảnh và tải xuống hàng loạt: tên file, định dạng, kích thước và nội dung ảnh.
- Xóa ảnh đơn lẻ/hàng loạt; xác nhận và hủy thao tác.
- Quản lý thư mục và các thao tác tìm kiếm, sắp xếp, phân trang nếu tính năng hiện hành có hỗ trợ.
- Phân quyền, cách ly dữ liệu giữa các bot và xử lý đối tượng không tồn tại.
- Kiểm tra điểm tích hợp sử dụng ảnh đã tạo để thiết lập Rich Menu nếu có hỗ trợ.

**Không bao gồm**: regression toàn bộ tính năng quản lý Rich Menu, gán Rich Menu cho bạn bè hoặc thống kê lượt tap; chỉ kiểm tra điểm tích hợp trực tiếp với ảnh đã tạo.

### Dữ liệu kế thừa từ Test Studio (do ticket chỉ định)

- Studio task nguồn: `task_id=507`, ticket #43845 (task cha, nâng cấp toàn bộ PHP 8.5/Laravel 13, 2018 TC).
- Studio task con của chính ticket này: **`task_id=515`**, status `tc-ready`, round 1, **đã có sẵn 45 TC kế thừa** (7 trực tiếp · 1 chỉ lấy phần builder · 7 tích hợp có điều kiện · 30 ngoài mô tả màn hình, theo `scope.impacts` của task 515) — xem [04-tc-list.md](04-tc-list.md).
- Giá trị đã xác định trong cột Màn hình/Chức năng: Tạo ảnh rich menu (「リッチメニュー画像作成」) — nhưng ticket yêu cầu **không chỉ lọc theo tên màn hình**, phải kiểm thêm TC xử lý ảnh dùng chung có ảnh hưởng trực tiếp.
- Giữ tham chiếu TC nguồn dạng `#43845 / NEW-xxx`; không tự sửa/xóa TC của task nguồn (507) — TC là read-only, muốn sửa thì sửa trên Studio rồi fetch lại.
- Kết quả test ở task nguồn (507) chỉ dùng tham khảo; task con (515) phải tự ghi nhận kết quả chạy trên commit + môi trường thực tế của mình — **45/45 TC hiện đều `(chưa chạy)`**.

## Steps to reproduce

<!-- Không có — đây là subtask QA retest phạm vi, không phải bug cụ thể. -->

## Expected result

<!-- Không có — xem "Mục tiêu" + "Phạm vi kiểm tra" ở trên. -->

## Actual result

<!-- Không có. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #44557 không có attachment (0). -->

## Ghi chú thêm của Leader

- ⚠️ **Không phải bug ticket** — Steps/Expected/Actual để trống có chủ đích. Phạm vi là **retest coverage** tính năng Tạo ảnh Rich Menu sau nâng cấp PHP 8.5 + Laravel 13, kế thừa quyết định/spec đã chốt tại #43845.
- Môi trường test: theo nhánh `ai_studio_implement_43845`; mốc đối chiếu production ghi trong bản bàn giao #43845 (release_ref Studio: `origin/release_step_20260930_v2`).
- File [03-dev-impact.md](03-dev-impact.md) KHÔNG lấy từ Dev tự kê (Redmine #44557 không có section "Đánh giá ảnh hưởng") — lấy từ `task_get_context` của Studio task 515 (kế thừa diff/dev_impact đã tính sẵn từ task cha 507), theo đúng chỉ định của ticket. Cần Dev xác nhận lại khi review.

<!-- Không có "Dữ liệu định danh ca lỗi" — ticket không có ca lỗi cụ thể. -->

<!-- Không có journal/note — Redmine #44557 có 0 journal. -->
