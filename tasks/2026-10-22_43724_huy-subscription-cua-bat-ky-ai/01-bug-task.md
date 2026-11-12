# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43724 — Hủy subscription (đơn định kỳ) của bất kỳ ai` |
| Module / Màn hình | Hợp đồng đơn định kỳ (cycle order) — trang 解約 (huỷ hợp đồng) phía khách V1/V2 + API `/ajax/(mobile/)cancel-cycle-order` |

## Mô tả bug (bản dịch tiếng Việt)

**Tác động / cách khai thác**
- Bản vá #40699 chỉ kiểm tra khi có session; không có session thì bỏ qua kiểm tra → gửi `cycle_order_id` tuần tự là hủy hàng loạt.

**Vị trí code**
- `SalesManagementV2Controller.php:1225`; `SalesManagementController.php:1333` · `/ajax/(mobile/)cancel-cycle-order`

**Cách sửa (theo đề xuất của người phát hiện)**
- Bắt buộc LINE user đã xác thực khớp `cycle->line_user_id`.

**Mức tin cậy**
- Confirmed

## Steps to reproduce

<!-- Suy trực tiếp từ "Tác động / cách khai thác" ở trên — ticket này là báo cáo rà soát bảo mật, không phải báo lỗi kèm case cụ thể. -->

1. Không đăng nhập admin (không có session).
2. Gửi POST tới `/ajax/cancel-cycle-order` (V1) hoặc `/ajax/mobile/cancel-cycle-order` (V2) với `cycle_order_id` bất kỳ (số tự tăng, không kèm thông tin định danh khách).
3. Lặp lại với các `cycle_order_id` tuần tự khác nhau (của bot/khách khác nhau).

## Expected result

- Request không có session / không xác thực đúng chủ hợp đồng phải bị chặn (`success:false`), hợp đồng không bị huỷ.

## Actual result

- Request không có session bỏ qua toàn bộ kiểm tra quyền sở hữu, huỷ được hợp đồng theo đúng `cycle_order_id` gửi lên → huỷ được hợp đồng của bất kỳ bot/khách nào mà không cần biết gì khác ngoài ID.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có attachment trên Redmine. -->

## Ghi chú thêm của Leader

- Ticket dạng **phát hiện qua rà soát bảo mật** (không phải khách báo lỗi) — không có môi trường phát hiện / case lỗi cụ thể ghi trên Redmine.
- Dev đã fix qua **2 vòng** (xem Journal nguyên văn bên dưới):
  - **Vòng 1** (#146607): fix lỗ hổng bảo mật chính — bắt buộc `u_code` khớp chủ hợp đồng khi request không có session (V1 + V2 + JS trang 解約).
  - **Vòng 2** (#146992): trong lúc QA vòng 1 phát sinh thêm bug phụ — bộ đếm `count_action_cancel` bị cộng **gấp đôi** (2 thay vì 1) ở MỌI luồng huỷ có action (không riêng luồng vừa sửa) — đã mở + fix các bug con QA `#43899`–`#43904` và bug automation Test Studio `#3771`–`#3775`, cùng 1 commit `sns-line@d9c85776ee65`.
- ⚠️ **Rủi ro khi deploy**: trình duyệt LINE cache `page-cancel.js` cũ (chưa gửi `u_code`) → khách hợp lệ tạm thời **không huỷ được** tới khi tải lại trang. Dev đề nghị đội release tăng `sns-line.version` khi deploy; tester phải Ctrl+F5 trang 解約 trước khi test.
- ⚠️ Dev xác nhận **không cần recover dữ liệu** — ticket là phát hiện rà soát bảo mật, chưa có báo cáo khách bị huỷ ngoài ý muốn; DB không phân biệt được huỷ hợp lệ với huỷ do khai thác (không có cột người huỷ).
- 2 việc **ngoài phạm vi task #43724** Dev đề xuất mở ticket riêng (không đưa vào coverage TC của task này):
  1. Soát access log production (từ 2023-02 tới khi deploy) tìm dấu hiệu khai thác (nhiều `cycle_order_id` liên tiếp từ 1 IP / không có Referer từ `/v2/order-item/cancel/`).
  2. Endpoint đổi thẻ công khai `/ajax/change-card-item/v2` (`changeCardItem` V2) cũng tra hợp đồng chỉ theo `cycle_id`, không kiểm chủ hợp đồng — lỗ hổng tương tự, chưa fix trong ticket này.
- Studio đã có task fix-bug #495 (branch `ai_studio_fixbug_43724`, round 1, status `tc-ready`) với 26 TC AI sinh — xem `04-tc-list.md`. TC toàn bộ chạy ở `staging` (0 TC chạy `prd`) → RULE-08 cần lưu ý khi Leader đánh giá coverage bill tiền / job nền.

## Journal / note từ Redmine (nguyên văn)

**Journal #146579 — Dev Studio — 2026-10-22:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Route `/ajax/mobile/cancel-cycle-order` (V2, trang 解約 của khách) và `/ajax/cancel-cycle-order` (V1) là route công khai, `/ajax/*` được miễn CSRF. Bản vá #40699 chỉ so bot của hợp đồng với bot trong session khi có session; request không đăng nhập bỏ qua mọi kiểm tra rồi huỷ theo `cycle_order_id` gửi lên. Request của trang khách chỉ có `cycle_order_id` (số tự tăng), không có gì định danh khách, nên lần lượt từng id là huỷ được hợp đồng của mọi bot. Nhận định của người báo là đúng.

Hướng sửa:
- D-1 V2 cancelCycleOrder: không có session thì bắt buộc u_code của đúng chủ hợp đồng
- D-2 Trang 解約 gửi kèm u_code khi huỷ
- D-3 V1 cancelCycleOrder: thêm đúng kiểm tra như D-1

Ảnh hưởng / rủi ro:
Chỉ đổi hai hàm huỷ hợp đồng (V1, V2) và file JS của trang 解約 phía khách; màn quản trị có đăng nhập không đổi hành vi. Rủi ro: trình duyệt LINE còn giữ cache file JS cũ (chưa gửi u_code) sẽ huỷ thất bại cho tới khi tải bản mới, vì tham số version do đội release tăng khi deploy.
```

**Journal #146607 — Dev Studio — 2026-10-22:**

```
Dev handoff — 22/10 10:13 · nhánh ai_studio_fixbug_43724

Nguyên nhân:
Route `/ajax/mobile/cancel-cycle-order` (V2, trang 解約 của khách) và `/ajax/cancel-cycle-order` (V1) là route công khai, `/ajax/*` được miễn CSRF. Bản vá #40699 chỉ so bot của hợp đồng với bot trong session khi có session; request không đăng nhập bỏ qua mọi kiểm tra rồi huỷ theo `cycle_order_id` gửi lên. Request của trang khách chỉ có `cycle_order_id` (số tự tăng), không có gì định danh khách, nên lần lượt từng id là huỷ được hợp đồng của mọi bot. Nhận định của người báo là đúng.

Nội dung thay đổi:
- Trang 解約 của khách (/v2/order-item/cancel/{item_code}/{u_code}): nút 解約 gửi thêm u_code của khách.
- API /ajax/mobile/cancel-cycle-order (V2): request không đăng nhập bị từ chối (success:false) nếu u_code không phải của chủ hợp đồng.
- API /ajax/cancel-cycle-order (V1): request không đăng nhập được kiểm như trên.

File đã sửa (php-web):
  .../Basic/SalesManagementController.php            |  11 +
  .../Basic/SalesManagementV2Controller.php          |  12 +
  public/js/sales/v2/page-cancel.js                  |   1 +
  tests/Feature/CancelCycleOrderOwnerTest.php        | 268 +++++++++++++++++++++
  4 files changed, 292 insertions(+)

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi chạm luồng khách thật huỷ hợp đồng có thu tiền. Nếu u_code không tới server (trình duyệt còn cache JS cũ), khách hợp lệ bị từ chối huỷ cho tới khi tải lại trang.
- Màn chi tiết hợp đồng quản trị V2 (/ajax/sales/cancel-cycle-order, cùng hàm V2): có session nên không đi vào kiểm tra mới; cần test hồi quy huỷ hợp đồng.
- Màn hợp đồng quản trị V1 (cycle_order_history, edit_cycle_order) gọi /ajax/cancel-cycle-order có session, hành vi không đổi.
- Action huỷ (action_cancel_payment_id) và bộ đếm count_action_cancel chỉ chạy sau khi qua kiểm tra; khách hợp lệ vẫn nhận như cũ.
- Khách đã chặn bot không huỷ được, trùng với điều kiện trang 解約 đang áp dụng.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Ticket là phát hiện rà soát bảo mật, chưa có báo cáo khách bị huỷ ngoài ý muốn. DB không phân biệt được huỷ hợp lệ với huỷ do khai thác (không có cột người huỷ, log hành động chỉ ghi khi đăng nhập), nên không viết được câu truy vấn xác định bản ghi bị hại; việc soát access log production được ghi thành follow-up.

Lưu ý khi deploy:
- Không bump sns-line.version. Đề nghị đội release tăng version như thường lệ khi deploy để trình duyệt tải page-cancel.js mới; nếu không, khách đang mở trang cũ phải tải lại.

Việc cần người làm thêm (ngoài phạm vi task):
- Đội vận hành soát access log production từ 2023-02 tới khi deploy, tìm các request POST /ajax/mobile/cancel-cycle-order hoặc /ajax/cancel-cycle-order có nhiều mã hợp đồng liên tiếp từ cùng một IP hoặc không có Referer từ trang /v2/order-item/cancel/. Nếu tìm thấy, lập danh sách hợp đồng bị huỷ và báo shop.
- Rà soát bảo mật riêng: endpoint đổi thẻ công khai /ajax/change-card-item/v2 (SalesManagementV2Controller::changeCardItem) cũng tra hợp đồng chỉ theo cycle_id, không kiểm tra chủ hợp đồng; nên mở ticket riêng.
- Đội release tăng sns-line.version khi deploy để trình duyệt LINE tải bản page-cancel.js mới.
- Soát access log production của /ajax/mobile/cancel-cycle-order, /ajax/sales/cancel-cycle-order và /ajax/cancel-cycle-order (request không session) để xem đã có hợp đồng nào bị huỷ trái phép chưa; DB không lưu người huỷ.
- Ticket riêng: changeCardItem V2 (/ajax/change-card-item/v2) lấy hợp đồng theo cycle_id mà không kiểm tra chủ sở hữu.
- Đội release tăng sns-line.version khi deploy để trình duyệt LINE tải bản page-cancel.js mới; bản cũ trong cache không gửi u_code nên sẽ không huỷ được hợp đồng.
- Siết xác thực khách trên các trang bán hàng: kiểm LIFF ID token phía server, vì hiện u_code lấy được qua /ajax/get-ucode-by-line-user-id chỉ cần botId và LINE userId.
- Soát production bot_line_user có u_code trùng (GROUP BY u_code HAVING COUNT(*)>1). Nếu có thì cấp lại u_code cho các dòng trùng.
- Soát access log production các request POST /ajax/(mobile/)cancel-cycle-order có dấu hiệu khai thác (nhiều id liên tiếp từ một IP, Referer không phải trang /v2/order-item/cancel/).
- changeCardItem V2 (/ajax/change-card-item/v2) tra hợp đồng theo cycle_id mà không kiểm chủ sở hữu, nên làm ticket riêng (thiết kế đã ghi).

Điểm cần test:
- Khách mở trang 解約 bằng URL có u_code, và qua LIFF khi URL không có u_code: bấm 解約 thành công, hợp đồng chuyển sang 解約, action huỷ chạy như cũ.
- POST /ajax/mobile/cancel-cycle-order khi không đăng nhập và không có u_code: trả success:false, hợp đồng không đổi.
- Không đăng nhập, gửi u_code của khách khác cùng bot, của bot khác, giá trị 'preview' hoặc của khách đã chặn bot: trả success:false, không đổi dữ liệu, không gửi action.
- POST /ajax/cancel-cycle-order (V1) khi không đăng nhập: trả success:false.
- Quản trị huỷ hợp đồng của bot mình ở màn chi tiết đơn định kỳ V2 và màn hợp đồng V1: vẫn thành công; đổi id sang hợp đồng của bot khác: vẫn bị chặn.
- Huỷ nhiều hợp đồng cùng lúc (一括解約) ở danh sách V2: không bị ảnh hưởng.
- Hợp đồng đang chờ xử lý thanh toán: khách hợp lệ vẫn nhận thông báo 「決済処理を行っていますので、操作できません。」.
- Khách mở trang 解約 bằng URL có u_code, bấm 解約: hợp đồng chuyển 解約 và action huỷ chạy như cũ.
- Khách mở trang 解約 qua LIFF (URL không có u_code): trang tự chuyển sang URL có u_code, bấm 解約 thành công.
- POST /ajax/mobile/cancel-cycle-order khi không đăng nhập, chỉ gửi cycle_order_id: trả success:false, hợp đồng không đổi, khách không nhận tin huỷ.
- Như trên nhưng gửi u_code của khách khác cùng bot, của bot khác, 'preview', hoặc của khách đã chặn bot: trả success:false, dữ liệu không đổi.
- Quản trị huỷ hợp đồng của bot mình ở V2 (chi tiết hợp đồng) và V1 (màn hợp đồng): vẫn thành công. Đổi id sang hợp đồng của bot khác: bị chặn.
- 一括解約 ở danh sách hợp đồng V2 không đổi hành vi.
- Hợp đồng đang chờ xử lý thanh toán: khách hợp lệ vẫn thấy 「決済処理を行っていますので、操作できません。」.
- Trước khi test, tải lại trang 解約 bằng Ctrl+F5 để lấy page-cancel.js mới.

Branch: ai_studio_fixbug_43724
- sns-line: ai_studio_fixbug_43724 (nhánh gốc release_step_20260930_v2 @4ae243379f82, commit ed709c409dbba9cc62dd4b3b310abd741c26fc69)
```

**Journal #146992 — Dev Studio — 2026-10-22:**

```
Dev handoff — 22/10 15:59 · nhánh ai_studio_fixbug_43724

Nguyên nhân:
Hàm dùng chung `sendActionOrderItem('cancel', …)` tự cộng `count_action_cancel` thêm 1 trước khi gửi action 解約時. Khi hàm trả về 1, các nơi gọi trong luồng huỷ hợp đồng lại cộng 1 lần nữa, nên mỗi lần huỷ có action thì bộ đếm tăng 2. Lỗi đã có từ trước, không do bản vá v1; #42198 đã sửa đúng lỗi này ở luồng đổi thẻ nhưng chưa sửa ở luồng huỷ.

Nội dung thay đổi:
- Trang 解約 khách V2 và API /ajax/mobile/cancel-cycle-order, /ajax/cancel-cycle-order: khi không đăng nhập chỉ huỷ được nếu mã khách khớp chủ hợp đồng và khách chưa chặn bot (vòng 1).
- Huỷ hợp đồng có action 解約時 (khách V2, admin chi tiết V2, 一括解約, admin V1): bộ đếm action 解約時 tăng 1 thay vì 2.
- Tự huỷ hợp đồng khi thanh toán lỗi (đổi thẻ V1 lỗi từ 3 lần, webhook UnivaPay, cron thu tiền Stripe, cron trial): bộ đếm action 解約時 tăng 1 thay vì 2.

Bug QA con:
- #43899 đã sửa (commit sns-line@d9c85776ee65): Gọi API huỷ không đăng nhập bằng mã khách đúng chủ: đã bỏ phần +1 lặp ở nơi gọi, bộ đếm tăng đúng 1. Phần chặn/cho phép (ed709c409d) giữ nguyên.
- #43900 đã sửa (commit sns-line@d9c85776ee65): Đã bỏ phần +1 lặp ở cả 7 nơi gọi sendActionOrderItem('cancel'), vì hàm này đã tự +1; mỗi lần huỷ có action giờ tăng đúng 1.
- #43902 đã sửa (commit sns-line@d9c85776ee65): Admin chi tiết V2: chọn 実行する thì bộ đếm tăng 1; chọn 実行しない thì không đổi.
- #43903 đã sửa (commit sns-line@d9c85776ee65): Luồng khách V2 (kể cả mở qua LIFF) giờ tăng đúng 1. Phần 'điểm vào LINE thật / tag do job xử lý' là giới hạn của môi trường test, không phải lỗi code.
- #43904 đã sửa (commit sns-line@d9c85776ee65): Khách chặn bot vẫn bị chặn; bỏ chặn thì huỷ được và bộ đếm tăng đúng 1.

Bug automation Test Studio:
- Bug #3771 đã sửa (commit sns-line@d9c85776ee65): Đã bỏ phần +1 lặp ở 7 nơi gọi sendActionOrderItem('cancel'); bộ đếm tăng đúng 1 (cùng lỗi với #43900).
- Bug #3772 đã sửa (commit sns-line@d9c85776ee65): Khách mở trang 解約 V2 qua LIFF: bộ đếm tăng đúng 1 (cùng lỗi với #43903).
- Bug #3773 đã sửa (commit sns-line@d9c85776ee65): Khách chặn bot vẫn bị chặn; bỏ chặn thì huỷ được và bộ đếm tăng 1 (cùng lỗi với #43904).
- Bug #3774 đã sửa (commit sns-line@d9c85776ee65): Admin chi tiết V2: chọn 実行する thì tăng 1, chọn 実行しない thì không đổi (cùng lỗi với #43902).
- Bug #3775 đã sửa (commit sns-line@d9c85776ee65): Gọi API huỷ không đăng nhập bằng mã khách đúng chủ: bộ đếm tăng 1 (cùng lỗi với #43899).

File đã sửa (php-web):
  app/Console/Commands/HandleBillStripe.php          |   6 +-
  app/Console/Commands/HandleSendActionTrialV2.php   |   6 +-
  .../Basic/SalesManagementController.php            |  17 +-
  .../Basic/SalesManagementV2Controller.php          |  26 +-
  .../Basic/SalesStripePaymentController.php         |   6 +-
  app/Services/Sales/SalesService.php                |   7 +-
  public/js/sales/v2/page-cancel.js                  |   1 +
  tests/Feature/CancelCycleOrderOwnerTest.php        | 268 +++++++++++++++++++++
  8 files changed, 299 insertions(+), 38 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Vòng này chỉ xoá một lệnh cập nhật thừa ở 7 chỗ, hàm dùng chung không đổi; harness đã xác nhận bộ đếm đúng ở 3 luồng qua endpoint.
- Action 解約時 đặt 'chỉ 1 lần': việc quyết định gửi dựa vào bộ đếm == 0, không đổi.
- Màn admin chi tiết đơn định kỳ V2 và 一括解約 (/ajax/sales/cancel-cycle-order): trạng thái huỷ, number_cancel*, thông báo app admin.
- Màn admin V1 lịch sử đơn định kỳ: huỷ khi có phiên đăng nhập.
- Đổi thẻ V1 (/ajax/change-card-item) lỗi nhiều lần dẫn tới tự huỷ hợp đồng.
- Job webhook UnivaPay và các cron handle:bill_stripe, handle:HandleSendActionTrialV2 (07:00): luồng tự huỷ khi thanh toán lỗi.
- Bảng bot_line_user_item (count_action_cancel, status_contract): java-job và java-mcp không đọc cột bộ đếm.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — count_action_cancel chỉ được đọc trong sendActionOrderItem để so với 0 (sản phẩm đặt action 'chỉ 1 lần'); giá trị 2 hay 1 cho cùng kết quả. Không màn hình nào hiển thị nó, và java-job, java-mcp, app mobile đều không đọc. Sửa dữ liệu cũ không làm thay đổi hành vi nào.

Lưu ý khi deploy:
- Không bump version JS: tester và khách cần tải lại cứng trang 解約 (Ctrl+F5).

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio cần môi trường có app LINE và source java-job để kiểm điểm vào LIFF thật và tag QA43724_LIFF (#43903); việc này nằm ngoài phần sửa code.
- Các luồng cron/webhook tự huỷ khi thanh toán lỗi (HandleBillStripe, HandleSendActionTrialV2, webhook UnivaPay, đổi thẻ V1 lỗi từ 3 lần) không tái hiện được trên môi trường test; nên theo dõi log job_crontab sau khi deploy.
- Luồng khách V2 cancelCycleOrder nên bỏ qua flagExecuteAction gửi từ request (tham số này chỉ dành cho admin) để tránh action 解約時 chạy hai lần.

Điểm cần test:
- Khách huỷ ở trang 解約 có mã khách (hoặc qua LIFF nếu có app LINE): action 解約時 chạy 1 lần, count_action_cancel tăng đúng 1.
- Admin ở chi tiết hợp đồng V2: chọn 実行する thì tăng 1; chọn 実行しない thì không đổi và không có action.
- Gọi API huỷ không đăng nhập với mã khách đúng chủ hợp đồng: tăng 1. Mã khách sai hoặc khách đã chặn bot: success=false, dữ liệu không đổi.
- Admin huỷ hợp đồng có action ở màn V1: tăng 1.
- 一括解約 V2 với 実行する: mỗi hợp đồng tăng 1.
- Sản phẩm đặt action 解約時 chỉ chạy 1 lần: lần huỷ đầu gửi action, các lần sau của cùng khách–sản phẩm không gửi (như cũ).
- Hồi quy v1: các ca chặn/cho phép huỷ giữ nguyên; tests/Feature/CancelCycleOrderOwnerTest.php vẫn pass; php -l các file đã sửa.
- Khách huỷ ở trang 解約 V2 (URL có mã khách, và qua LIFF): action 解約時 chạy 1 lần, count_action_cancel tăng đúng 1.
- Admin chi tiết hợp đồng V2 (SCR-BIL-19): chọn 実行する thì bộ đếm tăng 1; chọn 実行しない thì không đổi và không có action.
- API huỷ không đăng nhập: mã khách đúng chủ thì success:true và tăng 1; mã sai hoặc khách đã chặn bot thì success:false và không đổi; bỏ chặn thì huỷ được và tăng 1.
- Admin màn V1 huỷ hợp đồng có action: tăng 1.
- Sản phẩm đặt action 解約時 'chỉ 1 lần': lần huỷ đầu gửi action; hợp đồng sau của cùng khách–sản phẩm không gửi, bộ đếm vẫn +1 (như cũ).
- Hồi quy: trạng thái hợp đồng, number_cancel*, thông báo admin không đổi; tải lại cứng trang 解約 (Ctrl+F5) trước khi test.

Branch: ai_studio_fixbug_43724
- sns-line: ai_studio_fixbug_43724 (nhánh gốc release_step_20260930_v2 @4ae243379f82, commit d9c85776ee65634fdf5c7e9e059167039a65fc90)
```
