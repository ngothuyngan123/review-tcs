# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43723 — Xóa vĩnh viễn đơn hàng/booking theo id, không cần đăng nhập` |
| Module / Màn hình | Bug tự detect (security) — màn xác nhận mua sản phẩm trả bằng Stripe (`最終確認ページ`, confirm-order) + endpoint `POST /ajax/items/delete-order-confirm-fail` (`SalesManagementV2Controller.php`); cùng họ lỗi với 3 endpoint `delete-*-confirm-fail` khác (Lesson `Mobile/CalendarController.php`, Salon `Mobile/CalendarSalonController.php`, Event `MobileEventBookingController.php`) — **3 endpoint này KHÔNG thuộc phạm vi nhánh fix của task #43723** (xem Ghi chú thêm của Leader). |

## Mô tả bug (bản dịch tiếng Việt)

Tác động / cách khai thác: 4 endpoint "delete-*-confirm-fail" (Sales, Lesson, Salon, Event) xóa cứng (forceDelete/destroy) bản ghi theo id gửi lên tuần tự, của bất kỳ shop nào.

Vị trí code: `SalesManagementV2Controller.php:5203`; `Mobile/CalendarController.php:1396`; `Mobile/CalendarSalonController.php:2182`; `MobileEventBookingController.php:1653`.

Cách sửa (đề xuất của người báo cáo): Chỉ xóa bản ghi pending vừa tạo, thuộc LINE user đã xác thực (id_token) hoặc có token một lần.

Mức tin cậy: Confirmed.

## Steps to reproduce

1. Không đăng nhập (route nằm ngoài middleware đăng nhập, `/ajax/*` được miễn CSRF).
2. Gửi `POST /ajax/items/delete-order-confirm-fail` với `orderId` là id tuần tự của một đơn hàng (của bất kỳ shop/khách nào), không cần biết mã PaymentIntent/charge_id của đơn đó.
3. Controller `forceDelete()`/`destroy()` bản ghi theo id client gửi, không kiểm người gọi có phải chủ đơn và đơn có đang ở trạng thái tạm (`status_webhook=3`) hay không.

## Expected result

- Chỉ được xoá bản ghi **pending** vừa tạo, **thuộc đúng người** (xác thực bằng token một lần gắn phiên tạo đơn, hoặc id_token LINE user) — người khác / id không khớp / đơn đã chốt phải bị chặn (403), không đụng DB.

## Actual result

- Ai cũng xoá vĩnh viễn được đơn hàng/booking của **bất kỳ shop nào** bằng cách gửi id tuần tự — không cần đăng nhập, không cần biết mã PaymentIntent.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue #43723 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

⚠️ Đây là **bug tự detect (security/pentest)**, tracker "Bug Tester" — không có section "Tái hiện bug" dạng Steps/Expected/Actual riêng trong Redmine. Steps/Expected/Actual ở trên suy từ mục "Tác động / cách khai thác" + nội dung đánh giá ảnh hưởng của Dev (file `03-dev-impact.md`).

⚠️ **Phạm vi nhánh fix hiện tại (`ai_studio_fixbug_43723`) CHỈ sửa endpoint Sales** (`POST /ajax/items/delete-order-confirm-fail`, màn xác nhận mua sản phẩm Stripe). **3 endpoint còn lại (Lesson/Salon/Event) vẫn còn lỗ hổng**, phụ thuộc các nhánh khác chưa phát hành: Event `#42413`, Salon/Lesson chọn 1 trong 2 nhánh `#42436` hoặc `#43402` (đang xung đột, Leader phải chốt). Ticket `#43723` chỉ đóng hẳn khi cả 3 nhánh này đã release.

⚠️ **Fix đã qua 4 vòng dev handoff trong cùng ngày 2026-10-22** (journal #146588 → #146628 → #146867 → #147158), mỗi vòng vá thêm 1 lỗ hổng phụ do QA/automation Test Studio phát hiện trên vòng trước. **File `03-dev-impact.md` dùng vòng cuối (#147158, 17:15, commit `71a1069fdbc9`) làm chuẩn** vì đã gộp đủ các lớp bảo vệ — các vòng trước coi như lịch sử, không dùng làm oracle cho TC.

Tóm tắt diễn biến 4 vòng (để hiểu vì sao có `delete_token` + transaction + che log — không phải thiết kế ban đầu):
- V1 (#146588/#146628): chỉ thêm kiểm `charge_id` (mã PaymentIntent) khớp đơn tạm.
- V2 (#146867): QA tìm bug con `#3753` (nghi TrimStrings cắt khoảng trắng làm sai lệch so khớp `charge_id`) — Dev kết luận **không phải bug** (xem Business rule ở `03-dev-impact.md`); V2 thêm báo lỗi Chatwork khi exception 500.
- V3 (#147158, bản chốt): phát hiện lỗ hổng cốt lõi — **chỉ cần biết đúng `charge_id` là xoá được, không cần là chủ đơn** (không cookie/token cũng xoá được nếu biết mã) → thêm `delete_token` một lần gắn session trình duyệt đã tạo đơn (sống 30 phút), xoá đơn+hợp đồng định kỳ trong 1 transaction, che mã PaymentIntent/SQL khỏi log & Chatwork, và loại trừ riêng path `ajax/items/delete-order-confirm-fail` khỏi middleware `TrimStrings` toàn cục (10 bug con `#43948`–`#43961` được tạo và đã fix ở vòng này).

⚠️ **Rule đã chốt theo Dev — dùng làm oracle khi viết TC** (không suy ngược từ tên bug):
- Bug `#3753`/`#43948`: `TrimStrings` **vẫn cắt khoảng trắng ở mọi endpoint khác**; **chỉ riêng** `ajax/items/delete-order-confirm-fail` được loại trừ — `orderId=" 3528"` → **400** (không coi là đã chuẩn hoá), `charge_id=" C7 "` đúng mã sau khi trim → **403** (so khớp nguyên văn, có khoảng trắng = sai).
- `#43949` (asset version không bump): **không phải bug, không đổi code** — rule dự án cấm nhánh fix bug tự bump `sns-line.version`; JS cũ vẫn an toàn (403, đơn tạm chờ job dọn ~15 phút); quyết định bump version ở release là của đội release, QA **phải hard-reload (Ctrl+F5)** trước khi test để nạp JS mới.
- Giả lỗi DB khi xoá hợp đồng định kỳ → **500**, đơn **và** hợp đồng tạm cùng giữ nguyên (transaction) — không có trạng thái xoá dở 1 trong 2.
- Request xoá thành công gọi lại lần 2 (replay) hoặc token quá 30 phút → **403**, không phải lỗi khác.
- 3 endpoint Lesson/Salon/Event: **không thuộc nhánh này**, không viết TC verify-fix cho 3 endpoint đó ở task #43723 (chỉ ghi nhận GAP/risk nếu cần, chờ nhánh riêng).

## Dữ liệu định danh ca lỗi

<!-- Lỗi logic ở tầng endpoint (thiếu auth + thiếu check chủ đơn), áp dụng cho mọi bot/mọi đơn hàng — không gắn với 1 ca lỗi cụ thể. Dữ liệu cần dựng env test (đơn tạm Stripe 1 lần/định kỳ, token, charge_id) xem mục "Điểm cần test" trong journal ở 03-dev-impact.md / Studio task #498. -->

## Journal / note từ Redmine (nguyên văn)

<!-- 4 journal Dev Studio (#146588, #146628, #146867, #147158) đã chuyển nguyên văn theo 4 mục Đánh giá ảnh hưởng vào file 03-dev-impact.md (dùng journal #147158 — vòng cuối — làm nội dung chính thức mục 1-4; 3 journal trước giữ lại dạng tóm tắt diễn biến ở "Ghi chú thêm của Leader" trên). -->
