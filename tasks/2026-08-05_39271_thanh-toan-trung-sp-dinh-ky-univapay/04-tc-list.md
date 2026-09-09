# Test case — Ticket 39271

> Nguồn: `39271.xlsx` — sheet `Test case`. Tổng số case: **34**.

## Tổng quan

| Tiêu chí | Phân bố |
|---|---|
| Nhóm | UI: 8, API: 16, Job / Cron: 6, Data / Kiểm tra tĩnh: 4 |
| Loại case | Normal: 12, Abnormal: 18, Boundary: 4 |
| Cách chạy | manual: 5, auto: 29 |
| Kết quả thực thi | pass: 31, skip: 3 |

## Danh sách case

| No. | Nhóm | Màn hình / Chức năng | Loại case | Tên case | Chạy | Kết quả |
|---|---|---|---|---|---|---|
| NEW-7 | ui | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Khách mua gói định kỳ lần đầu trên màn xác nhận mua và nhận đủ kết quả | manual | pass |
| NEW-13 | ui | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Khách bấm mua lần thứ hai khi lần đầu chưa có kết quả thì bị chặn trên màn hình | manual | pass |
| NEW-14 | ui | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Khách đóng màn giữa lúc chờ kết quả rồi quay lại mua ngay thì bị chặn | manual | pass |
| NEW-15 | ui | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Bấm nút mua liên tiếp nhiều lần và mua song song trên hai màn | manual | pass |
| NEW-17 | ui | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Đối soát cổng UnivaPay trên môi trường thật sau khi thao tác mua bị chặn | manual | skip |
| NEW-1 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Mua gói định kỳ khi khách chưa có gói nào đang chờ thanh toán | auto | pass |
| NEW-2 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Gói đang chờ thanh toán của khách khác không chặn khách đang mua | auto | pass |
| NEW-3 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Gói đang chờ thanh toán của sản phẩm khác không chặn sản phẩm đang mua | auto | pass |
| NEW-4 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Gói đã hủy dù còn trạng thái chờ vẫn cho khách mua lại | auto | skip |
| NEW-5 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Gói đã kết thúc chu kỳ vẫn cho khách mua gói mới | auto | pass |
| NEW-6 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Normal | Sản phẩm thanh toán một lần không bị đoạn chặn mới ảnh hưởng | auto | pass |
| NEW-8 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Chặn mua lại khi gói định kỳ đang chờ chưa xử lý kết quả thanh toán | auto | pass |
| NEW-9 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Chặn mua lại khi gói định kỳ đang ở trạng thái quá hạn chờ kết quả | auto | pass |
| NEW-10 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Chặn mua lại khi gói định kỳ đang ở trạng thái quá hạn chờ phản hồi từ cổng | auto | pass |
| NEW-11 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Khi bị chặn không phát sinh đơn hàng, không đổi tồn kho, không gọi cổng thanh toán | auto | pass |
| NEW-12 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Bị chặn phải trả về lỗi nghiệp vụ có thông báo, không phải lỗi hệ thống | auto | pass |
| NEW-16 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Abnormal | Sản phẩm hết hàng và đang có gói chờ thì ưu tiên báo đang xử lý thanh toán | auto | pass |
| NEW-18 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Boundary | Gói đã có kết quả thanh toán thành công thì chặn khách mua tiếp | auto | pass |
| NEW-19 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Boundary | Gói có kết quả thanh toán lỗi thì không chặn khách mua lại | auto | pass |
| NEW-20 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay | Boundary | Nhập số lượng mua bằng 0 khi đang có gói chờ vẫn báo lỗi số lượng trước | auto | pass |
| NEW-31 | api | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán Stripe | Normal | Mua gói định kỳ qua thẻ Stripe giữ nguyên hành vi sau bản sửa | auto | pass |
| NEW-21 | job | Cron đối soát thanh toán UnivaPay quá hạn | Normal | Cron đối soát chốt trạng thái gói chờ quá 15 phút để khách mua lại được | auto | pass |
| NEW-22 | job | Cron đối soát thanh toán UnivaPay quá hạn | Abnormal | Gói chờ không có mã giao dịch thì cron không chốt được trạng thái | auto | skip |
| NEW-23 | job | Cron đối soát thanh toán UnivaPay quá hạn | Boundary | Gói chờ mới tạo dưới 15 phút thì cron chưa chốt và vẫn chặn mua | auto | pass |
| NEW-24 | job | Job thu tiền định kỳ UnivaPay | Normal | Job thu tiền định kỳ vẫn thu tiền bình thường cho gói đã chốt trạng thái | auto | pass |
| NEW-25 | job | Job thu tiền định kỳ UnivaPay | Abnormal | Job thu tiền định kỳ vẫn bỏ qua gói đang chờ kết quả thanh toán | auto | pass |
| NEW-26 | job | Job thu tiền định kỳ UnivaPay | Abnormal | Kết quả thanh toán về sau khi khách bị chặn vẫn cập nhật đúng gói cũ | auto | pass |
| NEW-27 | data | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) | Normal | (Kiểm tra kỹ thuật) Điều kiện chặn đúng phạm vi khách, sản phẩm, gói và trạng thái chờ | auto | pass |
| NEW-28 | data | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) | Normal | (Kiểm tra kỹ thuật) Vị trí đoạn chặn nằm trước bước tính tồn kho và trước lời gọi cổng | auto | pass |
| NEW-29 | data | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) | Abnormal | (Kiểm tra kỹ thuật) Điều kiện chặn không lọc theo chế độ môi trường của sản phẩm | auto | pass |
| NEW-30 | data | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) | Abnormal | (Kiểm tra kỹ thuật) Luồng thẻ Stripe cùng màn chưa có đoạn chặn tương tự | auto | pass |
| NEW-32 | ui | Sales > Confirm Order (UnivaPay) | Abnormal | Kiểm tra chặn mua trùng khi UnivaPay không sử dụng Webhook | auto | pass |
| NEW-33 | ui | Sales > Confirm Order (UnivaPay) | Abnormal | Kiểm tra chặn mua lại sau khi redirect URL | auto | pass |
| NEW-34 | ui | Sales > Confirm Order (UnivaPay) | Abnormal | Kiểm tra chặn mua lại sau khi redirect màn hình Text | auto | pass |

---

## Chi tiết case

### Nhóm `ui` — UI

#### NEW-7 — Khách mua gói định kỳ lần đầu trên màn xác nhận mua và nhận đủ kết quả

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | FUNC-001 |
| Spec ID | TICKET-39271, spec: payment/job-spec.md §2 |
| Chạy | manual |
| Phạm vi env | dev, staging, prd |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:50:55 |
| ID Ticket bug | - |

**Tiền điều kiện**

Có bot đã cấu hình UnivaPay và có sản phẩm định kỳ đang bán. Tài khoản LINE thật đã kết bạn với bot, chưa mua sản phẩm này. Có quyền xem dashboard UnivaPay tương ứng.

**Các bước thực hiện**

1. Mở link mua sản phẩm định kỳ bằng tài khoản LINE thật
2. Nhập thông tin khách và thông tin thẻ theo màn hình
3. Bấm nút 「購入する」 và chờ tới khi màn hình báo kết quả
4. Mở màn quản lý đơn hàng phía quản trị để đối chiếu gói định kỳ vừa tạo
5. Mở dashboard UnivaPay và đếm số giao dịch phát sinh cho khách này

**Dữ liệu nhập**

Sản phẩm định kỳ hàng tháng, số lượng 1, thẻ thử nghiệm hợp lệ.

**Kết quả mong đợi**

Màn hình chuyển sang trang hoàn tất theo cấu hình sản phẩm (hoặc màn chờ nếu bot dùng cơ chế nhận kết quả bất đồng bộ). Phía quản trị hiện đúng 1 gói định kỳ mới. Dashboard UnivaPay có đúng 1 giao dịch, không có giao dịch trùng. Khách nhận được tin nhắn kết quả trên LINE.

**Ghi chú**

Manual vì cần thiết bị LINE thật, thẻ thật/thử nghiệm và đối chiếu dashboard cổng thanh toán — không tự động hóa ở local được.

---

#### NEW-13 — Khách bấm mua lần thứ hai khi lần đầu chưa có kết quả thì bị chặn trên màn hình

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-ABANDON-001 |
| Spec ID | TICKET-39271, source: public/js/sales/v2/confirm-order.js:246-252 |
| Chạy | manual |
| Phạm vi env | dev, staging, prd |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:51:00 |
| ID Ticket bug | - |

**Tiền điều kiện**

Bot cấu hình nhận kết quả thanh toán bất đồng bộ (có đăng ký nhận phản hồi từ cổng). Tài khoản LINE thật, sản phẩm định kỳ đang bán. Có thể tạm chặn đường phản hồi từ cổng về hệ thống để giữ đơn ở trạng thái chờ.

**Các bước thực hiện**

1. Mở link mua sản phẩm định kỳ bằng tài khoản LINE thật, nhập thông tin và bấm 「購入する」
2. Giữ cho kết quả thanh toán chưa về (tạm chặn đường phản hồi từ cổng)
3. Xác nhận gói định kỳ vừa tạo đang ở trạng thái chờ kết quả
4. Mở lại link mua sản phẩm đó bằng chính tài khoản LINE này, nhập lại thông tin và bấm 「購入する」 lần thứ hai
5. Quan sát hộp thoại hiện ra và trạng thái nút 「購入する」
6. Mở dashboard UnivaPay đếm số giao dịch phát sinh cho khách này

**Dữ liệu nhập**

Cùng tài khoản LINE, cùng sản phẩm định kỳ, số lượng 1, cùng thẻ.

**Kết quả mong đợi**

Lần bấm thứ hai hiện hộp thoại cảnh báo với đúng nội dung 「決済処理を行っていますので、操作できません。」, màn hình KHÔNG chuyển sang trang hoàn tất, nút 「購入する」 được bật lại để khách có thể thử lại sau. Dashboard UnivaPay chỉ có đúng 1 giao dịch — không phát sinh lần trừ tiền thứ hai.

**Ghi chú**

Đây là tái hiện trực tiếp bug gốc ở góc nhìn khách hàng. Manual vì cần thiết bị LINE thật và đối chiếu dashboard cổng thanh toán.

---

#### NEW-14 — Khách đóng màn giữa lúc chờ kết quả rồi quay lại mua ngay thì bị chặn

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-ABANDON-001 |
| Spec ID | TICKET-39271, spec: payment/job-spec.md bảng J3 |
| Chạy | manual |
| Phạm vi env | dev, staging, prd |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:51:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Bot cấu hình nhận kết quả thanh toán bất đồng bộ. Tài khoản LINE thật, sản phẩm định kỳ đang bán, khách chưa mua sản phẩm này.

**Các bước thực hiện**

1. Mở link mua sản phẩm định kỳ, nhập thông tin và bấm 「購入する」
2. Trong lúc màn hình còn hiện thông báo đang xử lý thanh toán, đóng hẳn màn hình mua
3. Mở lại link mua sản phẩm đó ngay lập tức bằng chính tài khoản này
4. Nhập lại thông tin và bấm 「購入する」
5. Quan sát thông báo hiện ra

**Dữ liệu nhập**

Cùng tài khoản LINE, cùng sản phẩm định kỳ, số lượng 1.

**Kết quả mong đợi**

Lần mua thứ hai bị chặn với thông báo 「決済処理を行っていますので、操作できません。」, không phát sinh giao dịch thứ hai ở cổng thanh toán.

**Ghi chú**

Kịch bản rời luồng thanh toán giữa chừng — đúng cách khách hàng thật tạo ra trạng thái chờ. Manual vì cần thao tác đóng màn trên thiết bị thật.

---

#### NEW-15 — Bấm nút mua liên tiếp nhiều lần và mua song song trên hai màn

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | CONC-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | manual |
| Phạm vi env | dev, staging, prd |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:09:42 |
| ID Ticket bug | - |

**Tiền điều kiện**

Tài khoản LINE thật, sản phẩm định kỳ đang bán, khách chưa mua sản phẩm này. Chuẩn bị được hai màn mua cùng lúc trên cùng tài khoản.

**Các bước thực hiện**

1. Mở link mua sản phẩm định kỳ, nhập đủ thông tin
2. Bấm nút 「購入する」 hai lần thật nhanh liên tiếp
3. Ghi lại số gói định kỳ được tạo và số giao dịch ở dashboard UnivaPay
4. Làm sạch dữ liệu, sau đó mở hai màn mua cùng sản phẩm trên cùng tài khoản
5. Bấm 「購入する」 ở cả hai màn gần như cùng lúc
6. Đếm lại số gói định kỳ được tạo và số giao dịch ở dashboard UnivaPay

**Dữ liệu nhập**

Cùng tài khoản LINE, cùng sản phẩm định kỳ, số lượng 1, hai lần bấm cách nhau dưới 1 giây.

**Kết quả mong đợi**

Theo mục tiêu của ticket, khách chỉ được đăng ký 1 gói định kỳ và chỉ bị trừ tiền 1 lần cho mỗi lần mua có chủ đích: chỉ 1 gói định kỳ được tạo và dashboard UnivaPay chỉ có 1 giao dịch.

**Ghi chú**

CẦN DEV/LEADER KẾT LUẬN nếu kết quả khác kỳ vọng: đoạn chặn đọc dữ liệu trước rồi mới ghi bản ghi gói ở bước sau, giữa hai bước không có khóa, nên hai yêu cầu đến gần như cùng lúc về lý thuyết vẫn có thể cùng lọt qua. Nếu tester thấy 2 gói/2 giao dịch, hãy báo là giới hạn kỹ thuật cần dev xác nhận, KHÔNG tự kết luận bản sửa hỏng — bug gốc là bấm lại sau nhiều giây, vốn đã được đoạn chặn xử lý.

---

#### NEW-17 — Đối soát cổng UnivaPay trên môi trường thật sau khi thao tác mua bị chặn

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | RULE-06 |
| Spec ID | TICKET-39271, knowledge: ENV-PAY, knowledge: RULE-06 |
| Chạy | manual |
| Phạm vi env | prd |
| Kết quả thực thi | skip |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:18:33 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã chạy xong kịch bản khách bấm mua lần thứ hai bị chặn trên môi trường chạy thật. Có quyền truy cập dashboard UnivaPay của tài khoản bán hàng tương ứng.

**Các bước thực hiện**

1. Ghi lại thời điểm và tài khoản khách đã thực hiện thao tác mua bị chặn
2. Mở dashboard UnivaPay, lọc giao dịch theo khách và theo khoảng thời gian đó
3. Đối chiếu danh sách giao dịch trên cổng với danh sách đơn hàng phía quản trị

**Dữ liệu nhập**

Khoảng thời gian thực hiện thao tác bị chặn; mã khách hàng ở cổng thanh toán.

**Kết quả mong đợi**

Số giao dịch trên cổng UnivaPay khớp đúng số đơn hàng phía quản trị, không có giao dịch nào phát sinh tại thời điểm thao tác bị chặn.

**Ghi chú**

Manual và chỉ chạy trên môi trường thật vì bill tiền chỉ đối soát đầy đủ được với tài khoản thật của cổng thanh toán. Chỉ đọc dữ liệu, không thao tác gì trên cổng.

---

#### NEW-32 — Kiểm tra chặn mua trùng khi UnivaPay không sử dụng Webhook

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Sales > Confirm Order (UnivaPay) |
| Loại case | Abnormal |
| Mã quan điểm | CONC-001 |
| Spec ID | - |
| Chạy | auto |
| Phạm vi env | - |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:14:44 |
| ID Ticket bug | - |

**Tiền điều kiện**

Cửa hàng cấu hình UnivaPay không sử dụng Webhook; Chưa sở hữu subscription; Sản phẩm định kỳ

**Các bước thực hiện**

1. Mở Confirm Order
2. Nhấn Mua
3. Khi giao dịch đầu còn pending quay lại nhấn Mua lần nữa

**Dữ liệu nhập**

Cùng customer + cùng product

**Kết quả mong đợi**

Hiển thị 「決済処理を行っていますので、操作できません。」; Không tạo transaction/subscription mới

---

#### NEW-33 — Kiểm tra chặn mua lại sau khi redirect URL

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Sales > Confirm Order (UnivaPay) |
| Loại case | Abnormal |
| Mã quan điểm | CONC-001 |
| Spec ID | - |
| Chạy | auto |
| Phạm vi env | - |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:14:38 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã cấu hình Redirect URL sau thanh toán; Thanh toán thành công

**Các bước thực hiện**

1. Mua sản phẩm
2. Redirect sang URL
3. Back trình duyệt
4. Nhấn Mua lại

**Dữ liệu nhập**

Cùng customer + cùng product

**Kết quả mong đợi**

Không tạo transaction/subscription mới; Không cho phép thanh toán lại

---

#### NEW-34 — Kiểm tra chặn mua lại sau khi redirect màn hình Text

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Sales > Confirm Order (UnivaPay) |
| Loại case | Abnormal |
| Mã quan điểm | CONC-001 |
| Spec ID | - |
| Chạy | auto |
| Phạm vi env | - |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:14:41 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã cấu hình hiển thị màn hình Text sau thanh toán; Thanh toán thành công

**Các bước thực hiện**

1. Mua sản phẩm
2. Hiển thị màn hình Text
3. Back trình duyệt
4. Nhấn Mua lại

**Dữ liệu nhập**

Cùng customer + cùng product

**Kết quả mong đợi**

Không tạo transaction/subscription mới; Không phát sinh request thanh toán mới

---

### Nhóm `api` — API

#### NEW-1 — Mua gói định kỳ khi khách chưa có gói nào đang chờ thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | FUNC-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:51:44 |
| ID Ticket bug | - |

**Tiền điều kiện**

Có 1 bot đã cấu hình cổng UnivaPay. Có 1 sản phẩm định kỳ (chu kỳ hàng tháng) còn hàng. Khách A đã kết bạn với bot và chưa từng mua sản phẩm này — không tồn tại gói định kỳ nào của khách A cho sản phẩm này.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: xác nhận khách A không có gói định kỳ nào của sản phẩm này
2. Gửi yêu cầu xác nhận mua sản phẩm định kỳ đó cho khách A với số lượng 1, kèm thông tin thẻ hợp lệ
3. Xem nội dung phản hồi trả về cho màn hình khách
4. Kiểm tra dữ liệu gói định kỳ và đơn hàng vừa phát sinh của khách A

**Dữ liệu nhập**

Sản phẩm: sản phẩm định kỳ hàng tháng, còn hàng. Khách: A. Số lượng: 1. Thẻ: thẻ thử nghiệm hợp lệ của UnivaPay.

**Kết quả mong đợi**

Yêu cầu KHÔNG bị từ chối bởi thông báo 「決済処理を行っていますので、操作できません。」. Luồng đi tiếp tới bước thanh toán và trả về kết quả thành công hoặc đang chờ theo cấu hình bot. Phát sinh đúng 1 gói định kỳ mới cho khách A với sản phẩm này.

**Ghi chú**

Đây là case xương sống chứng minh đoạn chặn mới không cản luồng mua bình thường. Kỹ thuật: endpoint POST /ajax/payment-credit-card-item-v2-univapay; guard tại SalesManagementV2Controller.php:4920-4937.

---

#### NEW-2 — Gói đang chờ thanh toán của khách khác không chặn khách đang mua

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | TOOL-NEGCTRL-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:57:08 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách B đã có 1 gói định kỳ còn hiệu lực của sản phẩm X đang ở trạng thái chờ kết quả thanh toán. Khách A chưa có gói nào của sản phẩm X.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo cho khách B một gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Sản phẩm X. Khách B: gói còn hiệu lực, trạng thái chờ chưa xử lý kết quả. Khách A: mua mới, số lượng 1.

**Kết quả mong đợi**

Khách A KHÔNG bị chặn, không hiện thông báo 「決済処理を行っていますので、操作できません。」, luồng mua đi tiếp bình thường. Gói đang chờ của khách B giữ nguyên, không bị thay đổi.

**Ghi chú**

Đối chứng âm cho trục khách hàng. Kỹ thuật: điều kiện chặn lọc theo line_user_id.

---

#### NEW-3 — Gói đang chờ thanh toán của sản phẩm khác không chặn sản phẩm đang mua

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | TOOL-NEGCTRL-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:57:13 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X đang ở trạng thái chờ kết quả thanh toán. Sản phẩm Y là sản phẩm định kỳ khác, còn hàng, khách A chưa mua.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo cho khách A gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán
2. Gửi yêu cầu xác nhận mua sản phẩm Y cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A. Sản phẩm X: gói còn hiệu lực, trạng thái chờ. Sản phẩm Y: mua mới, số lượng 1.

**Kết quả mong đợi**

Khách A mua sản phẩm Y KHÔNG bị chặn, luồng mua đi tiếp bình thường. Gói đang chờ của sản phẩm X giữ nguyên.

**Ghi chú**

Đối chứng âm cho trục sản phẩm. Kỹ thuật: điều kiện chặn lọc theo item_id.

---

#### NEW-4 — Gói đã hủy dù còn trạng thái chờ vẫn cho khách mua lại

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | TOOL-NEGCTRL-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | skip |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 07:52:25 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có 1 gói định kỳ của sản phẩm X ở trạng thái ĐÃ HỦY, nhưng trường trạng thái kết quả thanh toán vẫn đang là chờ.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ của khách A cho sản phẩm X, đặt trạng thái gói là đã hủy và trạng thái kết quả thanh toán là chờ chưa xử lý
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X. Gói: trạng thái gói = đã hủy, trạng thái kết quả thanh toán = chờ chưa xử lý.

**Kết quả mong đợi**

Khách A KHÔNG bị chặn và mua lại được — vì gói cũ đã hủy, không còn hiệu lực để coi là đang thu tiền.

**Ghi chú**

Đối chứng âm cho trục trạng thái gói. Kỹ thuật: điều kiện chặn yêu cầu status_bill = 1; gói hủy là status_bill = 3. Cách hiểu ý nghĩa status_bill là suy ra từ mã nguồn (tạo mới = 1, hủy = 3), cần dev đính chính nếu sai.

---

#### NEW-5 — Gói đã kết thúc chu kỳ vẫn cho khách mua gói mới

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | TOOL-NEGCTRL-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:00:29 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có 1 gói định kỳ của sản phẩm X ở trạng thái ĐÃ KẾT THÚC (hết số kỳ), trường trạng thái kết quả thanh toán còn là chờ.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ của khách A cho sản phẩm X, đặt trạng thái gói là đã kết thúc và trạng thái kết quả thanh toán là chờ
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X. Gói: trạng thái gói = đã kết thúc, trạng thái kết quả thanh toán = chờ.

**Kết quả mong đợi**

Khách A KHÔNG bị chặn và đăng ký lại được gói mới cho sản phẩm X.

**Ghi chú**

Đối chứng âm cho trục trạng thái gói, giá trị 'đã kết thúc' (status_bill = 2).

---

#### NEW-6 — Sản phẩm thanh toán một lần không bị đoạn chặn mới ảnh hưởng

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Normal |
| Mã quan điểm | TOOL-NEGCTRL-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4955 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:02:26 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đang có 1 gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán. Sản phẩm Z là sản phẩm thanh toán một lần, còn hàng.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo cho khách A gói định kỳ của sản phẩm X ở trạng thái chờ kết quả thanh toán
2. Gửi yêu cầu xác nhận mua sản phẩm Z (thanh toán một lần) cho khách A với số lượng 1
3. Xem nội dung phản hồi và kiểm tra đơn hàng phát sinh

**Dữ liệu nhập**

Khách A. Sản phẩm X: gói định kỳ đang chờ. Sản phẩm Z: loại thanh toán một lần, số lượng 1.

**Kết quả mong đợi**

Mua sản phẩm một lần vẫn thành công, không hiện thông báo 「決済処理を行っていますので、操作できません。」. Phát sinh đúng 1 đơn hàng cho sản phẩm Z.

**Ghi chú**

Trục loại thanh toán: đoạn chặn chỉ tra bảng gói định kỳ nên về lý thuyết không chạm sản phẩm mua một lần, nhưng vì nó đặt trước cả nhánh phân loại nên vẫn phải kiểm chứng thực tế.

---

#### NEW-8 — Chặn mua lại khi gói định kỳ đang chờ chưa xử lý kết quả thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-STATE-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:02:42 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán là CHƯA XỬ LÝ.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ còn hiệu lực của khách A cho sản phẩm X với trạng thái kết quả thanh toán là chưa xử lý
2. Gửi yêu cầu xác nhận mua lại sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về cho màn hình khách

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1. Gói hiện có: còn hiệu lực, trạng thái kết quả thanh toán = chưa xử lý.

**Kết quả mong đợi**

Yêu cầu bị từ chối ngay, phản hồi báo lỗi với đúng nội dung 「決済処理を行っていますので、操作できません。」. Không phát sinh gói định kỳ hay đơn hàng mới.

**Ghi chú**

Trục trạng thái chờ, giá trị chưa xử lý (hằng số STATUS_WEBHOOK_UNPROCESSED = 0).

---

#### NEW-9 — Chặn mua lại khi gói định kỳ đang ở trạng thái quá hạn chờ kết quả

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-STATE-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:04:39 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán là QUÁ HẠN CHỜ.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ còn hiệu lực của khách A cho sản phẩm X với trạng thái kết quả thanh toán là quá hạn chờ
2. Gửi yêu cầu xác nhận mua lại sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1. Gói hiện có: còn hiệu lực, trạng thái kết quả thanh toán = quá hạn chờ.

**Kết quả mong đợi**

Yêu cầu bị từ chối với đúng nội dung 「決済処理を行っていますので、操作できません。」. Không phát sinh dữ liệu mới.

**Ghi chú**

Trục trạng thái chờ, giá trị quá hạn (hằng số STATUS_WEBHOOK_TIMEOUT = 3) — trạng thái mà bot không dùng cơ chế nhận kết quả bất đồng bộ sẽ rơi vào.

---

#### NEW-10 — Chặn mua lại khi gói định kỳ đang ở trạng thái quá hạn chờ phản hồi từ cổng

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-STATE-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:04:40 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán là QUÁ HẠN CHỜ PHẢN HỒI TỪ CỔNG.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ còn hiệu lực của khách A cho sản phẩm X với trạng thái kết quả thanh toán là quá hạn chờ phản hồi từ cổng
2. Gửi yêu cầu xác nhận mua lại sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1. Gói hiện có: còn hiệu lực, trạng thái kết quả thanh toán = quá hạn chờ phản hồi từ cổng.

**Kết quả mong đợi**

Yêu cầu bị từ chối với đúng nội dung 「決済処理を行っていますので、操作できません。」. Không phát sinh dữ liệu mới.

**Ghi chú**

Trục trạng thái chờ, giá trị quá hạn chờ phản hồi (hằng số STATUS_WEBHOOK_TIMEOUT_WEBHOOK = 4) — trạng thái được đặt khi bot dùng cơ chế nhận kết quả bất đồng bộ mà chưa có kết quả. Đây chính là trạng thái sinh ra kịch bản trừ tiền trùng của bug gốc.

---

#### NEW-11 — Khi bị chặn không phát sinh đơn hàng, không đổi tồn kho, không gọi cổng thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | RULE-07 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4955 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:04:48 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán. Sản phẩm X có bật quản lý tồn kho, còn 5 sản phẩm.

**Các bước thực hiện**

1. Ghi lại số bản ghi gói định kỳ, số bản ghi đơn hàng và số tồn kho còn lại của sản phẩm X trước khi thao tác
2. Gửi yêu cầu xác nhận mua lại sản phẩm X cho khách A với số lượng 1
3. Đếm lại số bản ghi gói định kỳ và đơn hàng của khách A cho sản phẩm X
4. Xem lại số tồn kho còn lại của sản phẩm X
5. Kiểm tra dashboard hoặc nhật ký giao dịch của cổng UnivaPay trong khoảng thời gian thao tác

**Dữ liệu nhập**

Khách A, sản phẩm X (bật tồn kho, còn 5), số lượng mua 1. Gói hiện có: còn hiệu lực, trạng thái chờ.

**Kết quả mong đợi**

Số bản ghi gói định kỳ và đơn hàng không tăng. Tồn kho vẫn là 5. Không có giao dịch mới nào phát sinh ở cổng UnivaPay. Nhật ký hệ thống có dòng ghi nhận việc chặn kèm mã gói đang xử lý.

**Ghi chú**

Chứng minh yêu cầu 'không có tác dụng phụ' — đoạn chặn chỉ đọc dữ liệu và đứng trước cả bước tính tồn kho lẫn lời gọi cổng. Phần đối chiếu cổng ở môi trường không có tài khoản thật thì kiểm bằng nhật ký gọi ra ngoài.

---

#### NEW-12 — Bị chặn phải trả về lỗi nghiệp vụ có thông báo, không phải lỗi hệ thống

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | TOOL-ERRHYG-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4930-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:04:56 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A đã có 1 gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán.

**Các bước thực hiện**

1. Gửi yêu cầu xác nhận mua lại sản phẩm X cho khách A với dữ liệu hợp lệ
2. Kiểm tra mã trạng thái và cấu trúc phản hồi trả về
3. Kiểm tra nội dung thông báo lỗi và các thông tin đi kèm trong phản hồi

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1, thông tin khách hợp lệ.

**Kết quả mong đợi**

Phản hồi trả về là kết quả xử lý bình thường của máy chủ (không phải lỗi 500), nội dung báo lỗi nghiệp vụ với đúng câu 「決済処理を行っていますので、操作できません。」. Phản hồi không chứa mã thẻ, mã token, mã khách hàng ở cổng thanh toán hay bất kỳ thông tin nhạy cảm nào.

**Ghi chú**

Gộp quan điểm vệ sinh mã lỗi và quan điểm không lộ thông tin nhạy cảm vào cùng một case vì cùng kiểm trên một phản hồi. Kỹ thuật: guard trả HTTP 200 với {result:'error', error_message:...}.

---

#### NEW-16 — Sản phẩm hết hàng và đang có gói chờ thì ưu tiên báo đang xử lý thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | TOOL-ERRHYG-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4967 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:05:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Sản phẩm X bật quản lý tồn kho và đã hết hàng. Khách A có gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: đặt tồn kho sản phẩm X về 0 và tạo gói định kỳ đang chờ cho khách A
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Đọc nội dung thông báo lỗi trả về

**Dữ liệu nhập**

Sản phẩm X: bật tồn kho, còn 0. Khách A: gói còn hiệu lực, trạng thái chờ. Số lượng mua 1.

**Kết quả mong đợi**

Thông báo trả về là 「決済処理を行っていますので、操作できません。」, KHÔNG phải thông báo hết hàng 「在庫がないので、購入できません。販売者に連絡してください。」 — vì việc kiểm tra thanh toán đang xử lý đứng trước việc kiểm tra tồn kho.

**Ghi chú**

Kiểm chứng vị trí của đoạn chặn trong chuỗi kiểm tra, quan sát được qua thông báo nào được trả ra trước.

---

#### NEW-18 — Gói đã có kết quả thanh toán thành công thì chặn khách mua tiếp

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Boundary |
| Mã quan điểm | FUNC-004 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937, source: app/OrderHistory.php:13-17 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:05:10 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có 1 gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán là ĐÃ XỬ LÝ XONG.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: đặt trạng thái kết quả thanh toán của gói là đã xử lý xong
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1. Gói hiện có: còn hiệu lực, trạng thái kết quả = đã xử lý xong.

**Kết quả mong đợi**

- Khách bị chặn, hiển thị màn thông báo lỗi
- Khách hàng chỉ được sở hữu 01 order của cùng sản phẩm tại một thời điểm theo business rule
- TH này sẽ không còn hiện message 決済処理を行っていますので、操作できません。 mà sẽ hiện màn thông báo lỗi

**Ghi chú**

Biên ở đây là biên của tập giá trị trạng thái, không phải biên số lượng hay số ký tự. Giá trị 'đã xử lý xong' (=1) nằm ngay sát tập bị chặn {0,3,4} nên phải kiểm riêng.

---

#### NEW-19 — Gói có kết quả thanh toán lỗi thì không chặn khách mua lại

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Boundary |
| Mã quan điểm | FUNC-004 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937, source: app/OrderHistory.php:13-17 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:08:52 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có 1 gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán là LỖI.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: đặt trạng thái kết quả thanh toán của gói là lỗi
2. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 1
3. Xem nội dung phản hồi trả về

**Dữ liệu nhập**

Khách A, sản phẩm X, số lượng 1. Gói hiện có: còn hiệu lực, trạng thái kết quả = lỗi.

**Kết quả mong đợi**

Khách KHÔNG bị chặn và mua lại được — thanh toán trước đó đã thất bại nên không còn coi là đang xử lý.

**Ghi chú**

Giá trị 'lỗi' (=2) nằm giữa tập bị chặn {0,3,4} nên là giá trị biên quan trọng — nếu bị chặn nhầm thì khách thanh toán hỏng sẽ không bao giờ mua lại được.

---

#### NEW-20 — Nhập số lượng mua bằng 0 khi đang có gói chờ vẫn báo lỗi số lượng trước

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán UnivaPay |
| Loại case | Boundary |
| Mã quan điểm | FUNC-004 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4915-4937 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:09:49 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán.

**Các bước thực hiện**

1. Gửi yêu cầu xác nhận mua sản phẩm X cho khách A với số lượng 0
2. Đọc nội dung thông báo lỗi trả về
3. Lặp lại với số lượng -1 và đọc thông báo

**Dữ liệu nhập**

Số lượng mua: 0, sau đó -1. Khách A, sản phẩm X, gói đang chờ.

**Kết quả mong đợi**

Cả hai lần đều báo 「購入数量は1以上で入力してください。」 — thứ tự kiểm tra số lượng đứng trước kiểm tra thanh toán đang xử lý và không bị bản sửa làm đảo lộn.

**Ghi chú**

Biên số lượng: 0 và số âm. Case này khẳng định bản sửa không chèn nhầm vào trước bước kiểm tra dữ liệu đầu vào cơ bản.

---

#### NEW-31 — Mua gói định kỳ qua thẻ Stripe giữ nguyên hành vi sau bản sửa

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Màn xác nhận mua sản phẩm (LINE friend) — thanh toán Stripe |
| Loại case | Normal |
| Mã quan điểm | REG-SHARED-001 |
| Spec ID | redmine: journal 2026-08-03T08:06:42Z, source: routes/web.php:3855, 3862 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:16:05 |
| ID Ticket bug | - |

**Tiền điều kiện**

Có bot cấu hình cổng Stripe và sản phẩm định kỳ bán qua Stripe. Khách A đã kết bạn với bot.

**Các bước thực hiện**

1. Gửi yêu cầu xác nhận mua sản phẩm định kỳ qua thẻ Stripe cho khách A với số lượng 1
2. Xem nội dung phản hồi và kiểm tra gói định kỳ phát sinh
3. Lặp lại kịch bản trên với dữ liệu chuẩn bị sẵn: khách A đang có gói định kỳ Stripe ở trạng thái chờ kết quả thanh toán

**Dữ liệu nhập**

Sản phẩm định kỳ thanh toán qua Stripe, khách A, số lượng 1.

**Kết quả mong đợi**

Hành vi của luồng Stripe giống hệt trước bản sửa: mua thành công ở lần đầu, và ở lần có gói đang chờ thì KHÔNG xuất hiện thông báo mới 「決済処理を行っていますので、操作できません。」 do bản sửa này sinh ra. Ghi lại hành vi thực tế để đối chiếu với kết quả chạy trên nhánh gốc.

**Ghi chú**

Regression đối chứng: chứng minh bản sửa không rò rỉ sang luồng thanh toán khác. Nếu muốn kết luận chắc chắn, chạy cùng kịch bản này trên nhánh gốc release_step_20260623 và so sánh hai kết quả.

---

### Nhóm `job` — Job / Cron

#### NEW-21 — Cron đối soát chốt trạng thái gói chờ quá 15 phút để khách mua lại được

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Cron đối soát thanh toán UnivaPay quá hạn |
| Loại case | Normal |
| Mã quan điểm | PAY-ABANDON-001 |
| Spec ID | spec: payment/job-spec.md bảng J3, source: SalesService.php:2563-2690, TICKET-39271 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:15:36 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X, trạng thái chờ kết quả thanh toán, ĐÃ có mã giao dịch của cổng, thời điểm tạo cách hiện tại hơn 15 phút. Cổng trả về kết quả giao dịch là thành công.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ đang chờ, có mã giao dịch, thời điểm tạo lùi hơn 15 phút
2. Xác nhận trước khi chạy cron: gửi yêu cầu mua lại sản phẩm X cho khách A và thấy bị chặn
3. Chạy cron đối soát thanh toán quá hạn
4. Kiểm tra lại trạng thái kết quả thanh toán của gói định kỳ
5. Gửi lại yêu cầu mua sản phẩm X cho khách A

**Dữ liệu nhập**

Gói định kỳ: còn hiệu lực, trạng thái chờ, có mã giao dịch, tạo cách đây 20 phút. Kết quả tra cứu ở cổng: thành công.

**Kết quả mong đợi**

- Sau khi cron chạy, trạng thái kết quả thanh toán của gói chuyển sang đã xử lý xong (hoặc lỗi nếu cổng trả thất bại), và lần gửi yêu cầu mua sau đó KHÔNG còn bị chặn. Việc chặn chỉ là tạm thời, không khóa vĩnh viễn.
- TH kết quả thanh toán là success => Yêu cầu mua của user vẫn sẽ bị chặn do spec user chỉ được phép mua 1 hợp đồng của cùng 1 sản phẩm tại 1 thời điểm => TH này sẽ không còn hiện message 決済処理を行っていますので、操作できません。 mà sẽ hiện màn thông báo lỗi
- TH kết quả thanh toán là failed => yêu cầu mua của user được chấp nhận, không bị chặn, không bị báo lỗi nữa

**Ghi chú**

Đây là đường thoát nghiệp vụ quan trọng nhất của bản sửa. Kỹ thuật: lệnh recover:payment_univapay_timeout chạy mỗi 5 phút, khối xử lý gói định kỳ trong SalesService::getOrderTimeout yêu cầu created_at cũ hơn 15 phút.

---

#### NEW-22 — Gói chờ không có mã giao dịch thì cron không chốt được trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Cron đối soát thanh toán UnivaPay quá hạn |
| Loại case | Abnormal |
| Mã quan điểm | INTG-HOOK-002 |
| Spec ID | source: SalesService.php:2563-2575, source: CycleOrderHistory.php:89, TICKET-39271 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | skip |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:15:49 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X, trạng thái chờ kết quả thanh toán, KHÔNG có mã giao dịch của cổng, thời điểm tạo cách hiện tại hơn 15 phút.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ đang chờ, để trống mã giao dịch, thời điểm tạo lùi hơn 30 phút
2. Chạy cron đối soát thanh toán quá hạn
3. Kiểm tra lại trạng thái kết quả thanh toán của gói
4. Gửi yêu cầu mua lại sản phẩm X cho khách A và đọc thông báo
5. Chạy cron thêm một lần nữa rồi lặp lại bước gửi yêu cầu mua

**Dữ liệu nhập**

Gói định kỳ: còn hiệu lực, trạng thái chờ, mã giao dịch để trống, tạo cách đây 30 phút.

**Kết quả mong đợi**

CẦN LEADER XÁC NHẬN trước khi chấm đạt/không đạt. Ghi nhận thực tế quan sát được: trạng thái gói có được chốt hay không, và khách có mua lại được hay không. Theo mục tiêu ticket, khách không được kẹt vĩnh viễn ở trạng thái không mua được.

**Ghi chú**

ĐIỂM CẦN LÀM RÕ: khối xử lý gói định kỳ trong cron đối soát yêu cầu có mã giao dịch của UnivaPay hoặc Stripe khác rỗng, trong khi mã này khi tạo gói lấy từ thông tin ủy quyền và có thể để trống. Nếu rơi vào trường hợp đó, gói giữ nguyên trạng thái chờ mãi và đoạn chặn mới sẽ khóa khách không cho mua lại. Đây là hệ quả mới do bản sửa tạo ra, cần dev/leader xác nhận hành vi mong đợi và cách xử lý.

---

#### NEW-23 — Gói chờ mới tạo dưới 15 phút thì cron chưa chốt và vẫn chặn mua

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Cron đối soát thanh toán UnivaPay quá hạn |
| Loại case | Boundary |
| Mã quan điểm | FUNC-004 |
| Spec ID | source: SalesService.php:2563-2575, spec: payment/job-spec.md bảng J3 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:15:31 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X, trạng thái chờ, có mã giao dịch, thời điểm tạo cách hiện tại 14 phút.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: tạo gói định kỳ đang chờ với thời điểm tạo lùi 14 phút
2. Chạy cron đối soát thanh toán quá hạn và kiểm tra trạng thái gói
3. Gửi yêu cầu mua lại sản phẩm X cho khách A và đọc thông báo
4. Điều chỉnh thời điểm tạo lùi thành 16 phút, chạy lại cron và kiểm tra trạng thái gói
5. Gửi lại yêu cầu mua sản phẩm X cho khách A

**Dữ liệu nhập**

Thời điểm tạo gói: lùi 14 phút, sau đó lùi 16 phút. Ngưỡng theo mô tả kỹ thuật của cron là 15 phút.

**Kết quả mong đợi**

Ở mốc 14 phút: cron chưa chốt trạng thái, khách vẫn bị chặn với thông báo 「決済処理を行っていますので、操作できません。」. Ở mốc 16 phút: cron chốt trạng thái và khách mua lại được.

**Ghi chú**

Nguồn của mốc 15 phút: điều kiện thời gian trong khối xử lý gói định kỳ của cron đối soát (SalesService::getOrderTimeout). Đây là mốc kỹ thuật đọc từ mã nguồn, chưa thấy tài liệu nghiệp vụ quy định — nếu leader có con số khác thì sửa lại case này.

---

#### NEW-24 — Job thu tiền định kỳ vẫn thu tiền bình thường cho gói đã chốt trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Job thu tiền định kỳ UnivaPay |
| Loại case | Normal |
| Mã quan điểm | PAY-BATCH-001 |
| Spec ID | spec: payment/job-spec.md §4.1, source: HandleSendActionTrialV2.php:149-160 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 04:55:38 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X, trạng thái kết quả thanh toán đã xử lý xong, đã đến hạn thu tiền kỳ tiếp theo.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: đặt hạn thu tiền của gói về quá khứ và trạng thái kết quả thanh toán là đã xử lý xong
2. Chạy job thu tiền định kỳ
3. Kiểm tra đơn hàng phát sinh cho kỳ mới và hạn thu tiền kỳ kế tiếp của gói

**Dữ liệu nhập**

Gói định kỳ chu kỳ hàng tháng, hạn thu tiền lùi 1 ngày, trạng thái kết quả = đã xử lý xong.

**Kết quả mong đợi**

Job thu tiền cho kỳ mới bình thường: phát sinh 1 đơn hàng cho kỳ này và hạn thu tiền của gói được dời sang chu kỳ kế tiếp. Bản sửa không làm job bỏ sót kỳ thu tiền hợp lệ.

**Ghi chú**

Regression cho vùng dùng chung bộ trạng thái kết quả thanh toán. Job này nằm ở mã nguồn web (lệnh Laravel), không phải dự án job.

---

#### NEW-25 — Job thu tiền định kỳ vẫn bỏ qua gói đang chờ kết quả thanh toán

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Job thu tiền định kỳ UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | PAY-BATCH-001 |
| Spec ID | source: HandleSendActionTrialV2.php:149-155, spec: payment/job-spec.md §4.1 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | AI (thanhntp) |
| Thời gian thực hiện | 2026-08-05 04:21:19 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X đã đến hạn thu tiền, nhưng trạng thái kết quả thanh toán đang là chờ.

**Các bước thực hiện**

1. Chuẩn bị dữ liệu: đặt hạn thu tiền lùi 1 ngày và trạng thái kết quả thanh toán là chờ
2. Chạy job thu tiền định kỳ
3. Đếm số đơn hàng phát sinh cho gói này
4. Kiểm tra nhật ký job và hạn thu tiền của gói

**Dữ liệu nhập**

Gói định kỳ đến hạn, trạng thái kết quả thanh toán = chờ (lần lượt thử với chưa xử lý, quá hạn, quá hạn chờ phản hồi).

**Kết quả mong đợi**

Job không thu tiền cho gói này, không phát sinh đơn hàng mới, nhật ký ghi nhận việc bỏ qua vì thanh toán đang xử lý. Đây là hành vi đã có trước bản sửa và phải giữ nguyên.

**Ghi chú**

Case này chứng minh guard mới và job dùng cùng một cách hiểu 'đang xử lý thanh toán', không sinh mâu thuẫn giữa hai nơi. Dùng 1 test case với 3 giá trị dữ liệu thay vì tách 3 case vì cùng một nguyên nhân gốc.

---

#### NEW-26 — Kết quả thanh toán về sau khi khách bị chặn vẫn cập nhật đúng gói cũ

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Job thu tiền định kỳ UnivaPay |
| Loại case | Abnormal |
| Mã quan điểm | INTG-HOOK-001 |
| Spec ID | spec: payment/job-spec.md §3.2, §3.3, TICKET-39271 |
| Chạy | auto |
| Phạm vi env | dev, local, staging |
| Kết quả thực thi | pass |
| Người thực hiện | thanhntp |
| Thời gian thực hiện | 2026-08-05 08:10:19 |
| ID Ticket bug | - |

**Tiền điều kiện**

Khách A có gói định kỳ còn hiệu lực của sản phẩm X ở trạng thái chờ kết quả thanh toán, đã ghi nhận mã giao dịch của cổng.

**Các bước thực hiện**

1. Gửi yêu cầu mua lại sản phẩm X cho khách A và xác nhận bị chặn
2. Gửi thông báo kết quả thanh toán thành công từ cổng cho đúng mã giao dịch của gói đang chờ
3. Kiểm tra trạng thái gói định kỳ và số bản ghi gói của khách A cho sản phẩm X
4. Gửi lại đúng thông báo kết quả đó lần thứ hai
5. Đếm lại số đơn hàng và số lần ghi nhận thu tiền của gói

**Dữ liệu nhập**

Thông báo kết quả thanh toán thành công, gửi 2 lần với cùng nội dung và cùng mã giao dịch.

**Kết quả mong đợi**

Gói cũ được cập nhật sang trạng thái đã xử lý xong, KHÔNG phát sinh gói định kỳ thứ hai. Lần gửi thông báo thứ hai bị bỏ qua, số đơn hàng và số lần ghi nhận thu tiền không tăng thêm.

**Ghi chú**

Kiểm chứng việc chặn phía màn mua không phá cơ chế chống xử lý trùng đã có ở phía nhận kết quả thanh toán. Chỉ giữ nhánh trùng và về trễ; không dựng nhánh sai thứ tự vì phần code đó không nằm trong diff.

---

### Nhóm `data` — Data / Kiểm tra tĩnh

#### NEW-27 — (Kiểm tra kỹ thuật) Điều kiện chặn đúng phạm vi khách, sản phẩm, gói và trạng thái chờ

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) |
| Loại case | Normal |
| Mã quan điểm | TOOL-SPECFIRST-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4920-4937, source: app/OrderHistory.php:13-17 |
| Chạy | auto |
| Phạm vi env | Tất cả |
| Kết quả thực thi | pass |
| Người thực hiện | AI (thanhntp) |
| Thời gian thực hiện | 2026-08-05 07:33:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã lấy về nhánh sửa lỗi của ticket 39271 và có thể đọc mã nguồn.

**Các bước thực hiện**

1. Mở phần xử lý xác nhận mua sản phẩm qua UnivaPay trong mã nguồn
2. Đọc điều kiện của đoạn kiểm tra chặn mua trùng vừa được thêm
3. Đối chiếu tên các hằng số trạng thái được dùng với bảng trạng thái của hệ thống

**Dữ liệu nhập**

Nhánh ai_fixbug_39271.

**Kết quả mong đợi**

Điều kiện chặn gồm đủ 4 vế: gói còn hiệu lực, đúng sản phẩm đang mua, đúng khách đang mua, và trạng thái kết quả thanh toán thuộc nhóm đang chờ gồm chưa xử lý, quá hạn, quá hạn chờ phản hồi. Các hằng số dùng là hằng số dùng chung của hệ thống, không phải số cứng viết tay.

**Ghi chú**

Kiểm tra tĩnh trên mã nguồn, không cần dựng ứng dụng. Kỹ thuật: guard tại SalesManagementV2Controller.php:4920-4937, hằng số App\OrderHistory STATUS_WEBHOOK_UNPROCESSED/TIMEOUT/TIMEOUT_WEBHOOK.

---

#### NEW-28 — (Kiểm tra kỹ thuật) Vị trí đoạn chặn nằm trước bước tính tồn kho và trước lời gọi cổng

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) |
| Loại case | Normal |
| Mã quan điểm | TOOL-SPECFIRST-001 |
| Spec ID | TICKET-39271, source: SalesManagementV2Controller.php:4915-4975 |
| Chạy | auto |
| Phạm vi env | Tất cả |
| Kết quả thực thi | pass |
| Người thực hiện | AI (thanhntp) |
| Thời gian thực hiện | 2026-08-05 07:33:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã lấy về nhánh sửa lỗi của ticket 39271.

**Các bước thực hiện**

1. Mở phần xử lý xác nhận mua sản phẩm qua UnivaPay
2. Xác định vị trí của đoạn chặn so với bước kiểm tra số lượng, bước tính tồn kho, bước lấy thông tin thẻ từ cổng và bước tạo bản ghi đơn hàng
3. Đọc nội dung đoạn chặn để xác nhận nó chỉ truy vấn dữ liệu

**Dữ liệu nhập**

Nhánh ai_fixbug_39271.

**Kết quả mong đợi**

Đoạn chặn đứng sau bước kiểm tra số lượng mua và đứng TRƯỚC bước tính tồn kho, trước bước lấy thông tin thẻ từ cổng và trước bước tạo bản ghi. Trong đoạn chặn chỉ có câu lệnh đọc dữ liệu, ghi nhật ký và trả về phản hồi — không có câu lệnh ghi, sửa hay xóa dữ liệu.

**Ghi chú**

Kiểm tra tĩnh; là căn cứ để khẳng định việc chặn không có tác dụng phụ lên dữ liệu và tiền của khách.

---

#### NEW-29 — (Kiểm tra kỹ thuật) Điều kiện chặn không lọc theo chế độ môi trường của sản phẩm

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) |
| Loại case | Abnormal |
| Mã quan điểm | DATA-DB-001 |
| Spec ID | source: SalesManagementV2Controller.php:4920-4955 |
| Chạy | auto |
| Phạm vi env | Tất cả |
| Kết quả thực thi | pass |
| Người thực hiện | AI (thanhntp) |
| Thời gian thực hiện | 2026-08-05 07:33:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã lấy về nhánh sửa lỗi của ticket 39271.

**Các bước thực hiện**

1. Đọc điều kiện lọc của đoạn chặn mua trùng
2. Đọc điều kiện lọc của truy vấn tính tồn kho ngay bên dưới
3. So sánh hai điều kiện xem có cùng lọc theo chế độ môi trường của sản phẩm hay không
4. Chuẩn bị dữ liệu: tạo gói định kỳ đang chờ ở chế độ thử nghiệm rồi thử mua cùng sản phẩm ở chế độ chính thức, ghi lại kết quả

**Dữ liệu nhập**

Nhánh ai_fixbug_39271; dữ liệu thử: 1 gói đang chờ ở chế độ thử nghiệm, 1 lần mua ở chế độ chính thức của cùng sản phẩm và cùng khách.

**Kết quả mong đợi**

CẦN LEADER XÁC NHẬN. Ghi nhận thực tế: đoạn chặn không lọc theo chế độ môi trường trong khi truy vấn tồn kho ngay bên dưới có lọc. Báo cáo lại xem lần mua ở chế độ chính thức có bị chặn bởi bản ghi ở chế độ thử nghiệm hay không, để leader quyết định đây là hành vi cố ý hay cần bổ sung điều kiện lọc.

**Ghi chú**

Mức rủi ro thấp vì chế độ môi trường được lấy theo cấu hình sản phẩm, chỉ lệch khi quản trị đổi chế độ của sản phẩm sau khi đã có đơn. Ghi nhận để leader quyết, không tự đánh trượt bản sửa.

---

#### NEW-30 — (Kiểm tra kỹ thuật) Luồng thẻ Stripe cùng màn chưa có đoạn chặn tương tự

| Thuộc tính | Giá trị |
|---|---|
| Màn hình / Chức năng | Mã nguồn đoạn chặn mua trùng (kiểm tra tĩnh) |
| Loại case | Abnormal |
| Mã quan điểm | REG-SHARED-001 |
| Spec ID | redmine: journal 2026-08-03T08:06:42Z, source: routes/web.php:3855, 3862 |
| Chạy | auto |
| Phạm vi env | Tất cả |
| Kết quả thực thi | pass |
| Người thực hiện | AI (thanhntp) |
| Thời gian thực hiện | 2026-08-05 07:33:09 |
| ID Ticket bug | - |

**Tiền điều kiện**

Đã lấy về nhánh sửa lỗi của ticket 39271.

**Các bước thực hiện**

1. Mở phần xử lý xác nhận mua sản phẩm qua thẻ Stripe của cùng màn
2. Tìm xem có đoạn kiểm tra chặn mua trùng tương tự hay không
3. Ghi lại kết quả rà soát vào báo cáo cho leader

**Dữ liệu nhập**

Nhánh ai_fixbug_39271; phạm vi rà: phần xử lý mua sản phẩm qua thẻ Stripe.

**Kết quả mong đợi**

Ghi nhận đúng thực trạng: luồng thẻ Stripe không có đoạn chặn tương tự. Đây là điểm nằm NGOÀI phạm vi ticket theo xác nhận của dev, KHÔNG được tính là không đạt cho ticket này; kết quả rà soát được chuyển cho leader để quyết định có mở ticket riêng hay không.

**Ghi chú**

Case này tồn tại để phần rà soát vùng ảnh hưởng có bằng chứng, không phải để đánh giá bản sửa. Kỹ thuật: các đường xử lý mua qua Stripe nằm ở SalesStripePaymentController.

---
