# -*- coding: utf-8 -*-
"""FA-026 商品販売 — Nhóm 20-21: Cơ chế thanh toán (UnivaPay callback/webhook · Stripe tạo order trước).

Nguồn chính: 12. TCsLine_Item / tab「Improve bill tiền univapay」(tab master của cơ chế bill,
             05/2025 → 06/2026: Bug KH #33787 18+29/1/2026 · Bug KH #36443 5/2026 · Bug Tester #38077 6/2026)
             và tab「Improve bill tiền stripe」r1-r46 (10/2025 change spec).

★ NIÊN ĐẠI QUAN TRỌNG — thời gian chờ kết quả bill trên UI:
  · bản gốc (05/2025)  : 2 phút 5 giây
  · 18/01/2026 (#33787): sửa thành 1 phút
  · 29/01/2026 (#33787): sửa thành 5 giây  ← MỚI NHẤT, khớp spec (retry 5 lần × sleep 1s)
  Toàn bộ TC dưới đây viết theo mốc 5 GIÂY.
"""
from _common import tc

UNI = ("- SP là 単品商品 テスト環境, cổng UnivaPay\n"
       "- Friend F1 đã kết bạn, đang ở màn 最終確認 của luồng mua")
UNIC = ("- SP-C là 継続商品 テスト環境, cổng UnivaPay\n"
        "- Friend F1 đã kết bạn, đang ở màn 最終確認 của luồng mua")
WH_ON = "- Bot A CÓ dùng webhook: s_strip_bot có univapay_webhook_id và status_webhook = 1"
WH_OFF = "- Bot A KHÔNG dùng webhook: s_strip_bot chưa có univapay_webhook_id (hoặc status_webhook ≠ 1)"

S4 = [
    # ══════ 20. Bill UnivaPay — callback & webhook ══════
    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế KHÔNG webhook — bấm mua tạo ngay bản ghi đơn ở trạng thái chờ xử lý",
       UNI + "\n" + WH_OFF,
       "1. F1 bấm 購入する ở màn 最終確認\n2. NGAY LẬP TỨC mở 販売履歴 phía admin tìm đơn của F1\n"
       "3. Đọc trạng thái hiển thị của đơn",
       "Cổng UnivaPay, không webhook",
       "- Đơn xuất hiện ngay ở 販売履歴 với trạng thái「決済処理中」\n"
       "- Nút 返金 của đơn này bị ẩn / không bấm được",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r4 (status_order=1, status_webhook=3) + r27."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế KHÔNG webhook — có kết quả trong 5 giây, bill SUCCESS → về màn chat, đơn thành 決済成功",
       UNI + "\n" + WH_OFF,
       "1. F1 bấm 購入する với thẻ đúng (4242…)\n2. Quan sát màn hình phía LINE\n"
       "3. Mở 販売履歴 đọc trạng thái đơn\n4. Kiểm tra chat 1:1 của F1 và notify admin",
       "Thẻ đúng 4242…, kết quả về < 5 giây",
       "- Phía LINE: mua success, redirect về màn chat 1:1 (không hiện màn chờ)\n"
       "- 販売履歴: đơn chuyển sang「決済成功」, nút 返金 dùng được\n"
       "- F1 nhận action「申込完了時」\n"
       "- Admin nhận notify「【tên Bot】<line name> <tên qly item> が購入されました」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r5 + r198 (mốc 5s theo bản sửa 29/1/2026)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Cơ chế KHÔNG webhook — bill FAIL trong 5 giây → xóa đơn, báo lỗi, không action, có notify lỗi",
       UNI + "\n" + WH_OFF,
       "1. F1 bấm 購入する với thẻ sai 4111 1111 1111 1111\n2. Quan sát màn hình phía LINE\n"
       "3. Mở 販売履歴 tìm đơn của F1\n4. Kiểm tra chat 1:1 F1 và notify admin",
       "Thẻ 4111 1111 1111 1111",
       "- Phía LINE hiện message báo bill lỗi\n"
       "- KHÔNG còn đơn nào của F1 ở 販売履歴 (bản ghi tạm đã bị xóa)\n"
       "- F1 KHÔNG nhận action\n"
       "- Admin nhận notify「【tên Bot】<line name> <tên qly item> の決済に失敗しました」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r6 + r201."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Abnormal",
       "Cơ chế KHÔNG webhook — QUÁ 5 giây chưa có kết quả → hiện màn thông báo chờ theo design mới",
       UNI + "\n" + WH_OFF + "\n- Mô phỏng chậm: throttle network hoặc tắt charge finish trên merchant",
       "1. F1 bấm 購入する với thẻ đúng\n2. Chờ quá 5 giây\n3. Quan sát màn hình phía LINE\n"
       "4. Mở 販売履歴 đọc trạng thái đơn",
       "Kết quả bill về sau > 5 giây",
       "- Phía LINE hiện MÀN THÔNG BÁO CHỜ theo design mới "
       "(https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs)\n"
       "- KHÔNG tự động quay về màn chat\n"
       "- 販売履歴: đơn ở trạng thái「決済処理中」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r7 + r199 (r199 ghi status_webhook = 4). "
            "⚠ Mốc thời gian: bản gốc 2p5s → 18/1/2026 sửa 1p → 29/1/2026 sửa 5s. Viết theo mốc MỚI NHẤT."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế KHÔNG webhook — kết quả về sau khi đã hiện màn chờ, bill SUCCESS → gửi tin LINE báo thành công",
       UNI + "\n" + WH_OFF,
       "1. Tạo tình huống quá 5 giây chưa có kết quả (đã hiện màn chờ)\n"
       "2. Chờ tới khi cổng trả kết quả success\n3. Mở 販売履歴 đọc trạng thái đơn\n"
       "4. Kiểm tra chat 1:1 của F1",
       "Kết quả success về sau màn chờ",
       "- Đơn chuyển sang「決済成功」\n- F1 nhận action「申込完了時」\n"
       "- Admin nhận notify が購入されました\n"
       "- ★ F1 nhận THÊM tin nhắn LINE「決済が完了しました。」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r8. Đây là điểm phân biệt so với case < 5s (không có tin này)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Cơ chế KHÔNG webhook — kết quả về sau màn chờ, bill FAIL → gửi tin LINE báo lỗi kèm hướng dẫn",
       UNI + "\n" + WH_OFF,
       "1. Tạo tình huống quá 5 giây chưa có kết quả với thẻ sai\n2. Chờ tới khi cổng trả kết quả fail\n"
       "3. Mở 販売履歴\n4. Kiểm tra chat 1:1 của F1",
       "Kết quả fail về sau màn chờ",
       "- Đơn bị xóa khỏi 販売履歴\n- F1 KHÔNG nhận action\n- Admin nhận notify 決済に失敗しました\n"
       "- ★ F1 nhận tin nhắn LINE「決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき"
       "再度、購入手続きを行なってください。」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r9."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế CÓ webhook — bấm mua tạo bản ghi ở trạng thái chờ callback (khác trạng thái cơ chế cũ)",
       UNI + "\n" + WH_ON,
       "1. F1 bấm 購入する\n2. NGAY LẬP TỨC mở 販売履歴 đọc trạng thái đơn\n"
       "3. So sánh với trạng thái ghi nhận ở cơ chế KHÔNG webhook",
       "Bot có webhook (status_webhook của s_strip_bot = 1)",
       "- Đơn xuất hiện ở 販売履歴 với trạng thái「決済処理中」\n"
       "- Nút 返金 bị ẩn\n"
       "- Trạng thái nội bộ khác cơ chế cũ (chờ callback thay vì chờ polling) nhưng "
       "MÀN HÌNH ADMIN hiển thị GIỐNG NHAU",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r13 (status_webhook=0) vs r4 (status_webhook=3) + r28."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế CÓ webhook — callback về trong 5 giây, SUCCESS → về màn chat, đơn 決済成功",
       UNI + "\n" + WH_ON,
       "1. F1 bấm 購入する với thẻ đúng\n2. Quan sát màn hình phía LINE\n3. Mở 販売履歴\n"
       "4. Kiểm tra chat 1:1 F1 + notify admin",
       "Thẻ đúng, callback < 5 giây",
       "- Phía LINE: mua success, redirect về màn chat\n- Đơn chuyển「決済成功」\n"
       "- Có action「申込完了時」và notify が購入されました",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r14 + r233."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Abnormal",
       "Cơ chế CÓ webhook — quá 5 giây chưa có callback → hiện màn chờ; quá 5 phút vẫn chưa có → đơn chuyển trạng thái chờ job",
       UNI + "\n" + WH_ON + "\n- Vào merchant UnivaPay TẮT sự kiện charge finished để chặn callback",
       "1. F1 bấm 購入する\n2. Quan sát màn hình sau 5 giây\n3. Chờ tiếp quá 5 phút\n"
       "4. Mở 販売履歴 đọc trạng thái đơn",
       "Tắt charge finished trên merchant",
       "- Sau 5 giây: hiện màn thông báo chờ theo design mới\n"
       "- Sau 5 phút: đơn vẫn ở「決済処理中」, KHÔNG bị xóa, chờ job quét (xem nhóm『Job cứu đơn treo』)\n"
       "- Chưa gửi action / notify nào",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r17 + r20 (status_webhook chuyển 4) + r234."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Cơ chế CÓ webhook — callback về SAU 5 phút, SUCCESS → cập nhật đơn + gửi tin báo thành công",
       UNI + "\n" + WH_ON,
       "1. Tạo tình huống callback về sau 5 phút (bật lại charge finished sau khi đã quá 5 phút)\n"
       "2. Mở 販売履歴 đọc trạng thái đơn\n3. Kiểm tra chat 1:1 F1 và notify admin",
       "Callback success về sau 5 phút",
       "- Đơn chuyển「決済成功」\n- F1 nhận action「申込完了時」\n- Admin nhận notify が購入されました\n"
       "- F1 nhận tin LINE「決済が完了しました。」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r21."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Cơ chế CÓ webhook — callback về SAU 5 phút, FAIL → xóa đơn + gửi tin báo lỗi",
       UNI + "\n" + WH_ON,
       "1. Tạo tình huống callback fail về sau 5 phút\n2. Mở 販売履歴\n3. Kiểm tra chat 1:1 F1 + notify admin",
       "Callback fail về sau 5 phút",
       "- Đơn bị xóa khỏi 販売履歴\n- KHÔNG gửi action\n- Admin nhận notify 決済に失敗しました\n"
       "- F1 nhận tin LINE「決済に失敗しました。…」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r22."),

    tc("Bill UnivaPay — callback & webhook", "STATE-001", "Abnormal",
       "★ Đang bill mà friend bấm BACK → hiện message cảnh báo, KHÔNG hủy giao dịch",
       UNI,
       "1. F1 bấm 購入する\n2. Trong lúc đang quay chờ kết quả, bấm nút BACK của trình duyệt/LIFF\n"
       "3. Đọc message hiện ra → bấm OK\n4. Quan sát màn hình sau khi bấm OK\n5. Mở 販売履歴",
       "Bấm back khi đang bill",
       "- Hiện message:「この画面を離れた後も、決済処理は継続されます。/ 決済の成功・失敗が確定しましたら"
       "LINEへのメッセージ送信で結果をお知らせいたします。/ 決済結果が送信されるまでは、決済操作は行わないでください。」\n"
       "- Bấm OK: hiện lại màn nhập thẻ (KHÔNG back được về màn chat)\n"
       "- Giao dịch vẫn tiếp tục chạy, đơn không bị hủy",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r202 + r211 + r236 + r243 (Bug KH #33787, 18/1/2026 — "
            "cách fix: bắt case close và back và hiển thị message)."),

    tc("Bill UnivaPay — callback & webhook", "STATE-001", "Abnormal",
       "★ Đang bill mà friend bấm X (đóng) → hiện cùng message cảnh báo, KHÔNG hủy giao dịch",
       UNI,
       "1. F1 bấm 購入する\n2. Trong lúc đang chờ kết quả, bấm nút X đóng LIFF\n"
       "3. Đọc message → bấm OK\n4. Mở 販売履歴 kiểm tra đơn",
       "Bấm X khi đang bill",
       "- Hiện đúng message この画面を離れた後も、決済処理は継続されます。…\n"
       "- Giao dịch vẫn chạy tiếp, đơn không bị hủy\n"
       "- Kết quả cuối cùng vẫn được thông báo qua tin nhắn LINE",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r203 + r212 + r237 + r244."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "★ Đang bill mà LỖI HỆ THỐNG → hiện màn thông báo theo design, không im lặng đóng màn",
       UNI + "\n- Mô phỏng lỗi hệ thống (nhờ dev inject lỗi ở nhánh thanh toán)",
       "1. F1 bấm 購入する\n2. Kích hoạt lỗi hệ thống trong lúc đang bill\n3. Quan sát màn hình phía LINE",
       "Lỗi hệ thống trong khi bill",
       "- Hiện MÀN THÔNG BÁO theo design mới\n"
       "- KHÔNG tự động quay lại màn hình trước khi bấm nút mua\n- KHÔNG im lặng không báo gì",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r204 + r213 + r238 + r245. Liên quan Bug KH #36443 "
            "(「sau khi hiển thị 処理完了まで2〜3分かかる場合があります。 thì màn hình tự quay lại trước khi bấm "
            "nút mua → không thanh toán được」— nguyên nhân: lỗi univapay chưa hiển thị message cho user)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Bug KH #36443 — số tiền VƯỢT hạn mức tài khoản UnivaPay → hiện message lỗi rõ ràng cho user",
       UNI + "\n- Tài khoản UnivaPay テスト có hạn mức tối đa 500.000円",
       "1. Tạo SP-A giá 499.999円, SP-B giá 500.000円, SP-C giá 500.001円 (cùng cổng UnivaPay)\n"
       "2. F1 mua lần lượt cả 3 sản phẩm\n3. Với mỗi lần: quan sát màn hình phía LINE và 販売履歴",
       "499.999 / 500.000 / 500.001 円",
       "- 499.999円 và 500.000円: mua thành công, redirect về màn talklist của LINE\n"
       "- 500.001円: bill FAIL và HIỂN THỊ MESSAGE LỖI cho user (không im lặng, không tự đóng màn)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r293-r295 (Bug KH #36443, 5/2026). Biên hạn mức tài khoản test."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Bug KH #36443 — vượt hạn mức với item CHU KỲ → cũng hiện message lỗi",
       UNIC + "\n- Tài khoản UnivaPay テスト có hạn mức tối đa 500.000円",
       "1. Tạo 3 sản phẩm 継続 giá 499.999 / 500.000 / 500.001円\n2. F1 mua lần lượt cả 3\n"
       "3. Quan sát màn hình và 販売履歴",
       "499.999 / 500.000 / 500.001 円",
       "- 499.999円 và 500.000円: mua thành công, redirect về màn talklist\n"
       "- 500.001円: bill fail, hiển thị message lỗi cho user",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r296-r298 + r304-r306."),

    tc("Bill UnivaPay — callback & webhook", "COMPAT-001", "Abnormal",
       "Bug KH #36443 — tái hiện trên CẢ Android và iPhone → message lỗi giống nhau",
       "- Tài khoản UnivaPay hạn mức 500.000円\n- SP 単品 giá 500.001円\n"
       "- Có sẵn LINE app trên cả Android và iPhone",
       "1. Trên LINE app Android: mở page item → bấm mua → xác nhận\n"
       "2. Lặp lại y hệt trên LINE app iPhone\n3. So sánh message và hành vi màn hình",
       "500.001円 trên 2 hệ điều hành",
       "- Cả 2 thiết bị đều hiển thị message lỗi (không silent fail, không tự đóng màn)\n"
       "- Nội dung message giống nhau giữa Android và iPhone",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r313 (TC-NEW-03 — case do KH report explicit về compatibility)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Thẻ bị từ chối (card declined) → hiển thị message lỗi rõ ràng, không silent fail",
       UNI + "\n- Tài khoản UnivaPay sandbox",
       "1. F1 mở page item → bấm mua\n2. Nhập thẻ 4111 1111 1111 1111 (declined)\n3. Xác nhận thanh toán\n"
       "4. Lặp lại ở cả 2 cấu hình: CÓ webhook và KHÔNG webhook",
       "Thẻ 4111 1111 1111 1111",
       "- Hiển thị message lỗi rõ ràng cho user (nội dung nói được lý do thẻ bị từ chối)\n"
       "- KHÔNG silent fail, KHÔNG quay về talklist im lặng\n"
       "- Kết quả giống nhau ở cả 2 cấu hình webhook",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r315 (TC-NEW-06). ⚠ Spec R18: getMessageError fallback luôn rơi "
            "vào processing_error → message gốc của cổng bị nuốt → xem MT-20."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Thẻ không đủ số dư (insufficient funds) → message lỗi dễ hiểu cho người dùng cuối",
       UNI + "\n- Tài khoản UnivaPay sandbox có test card cho case số dư không đủ",
       "1. F1 mở page item → bấm mua\n2. Nhập test card insufficient funds → xác nhận",
       "Test card insufficient (theo tài liệu UnivaPay)",
       "- Hiển thị message lỗi, nội dung dễ hiểu với người mua (VD「残高が不足しています」)\n"
       "- Không hiện lỗi kỹ thuật thô",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r316 (TC-NEW-07). Tester ghi「MT test không test được case lỗi "
            "do k đủ số dư」→ cần môi trường sandbox riêng, CẦN LEADER XÁC NHẬN có chạy được không."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "★ Bug Tester #38077 — UnivaPay trả status = Authorized phải coi là BILL THÀNH CÔNG (単品)",
       UNI + "\n- Có đơn của F1 đang chờ job quét kết quả bill",
       "1. Trên UnivaPay đặt trạng thái giao dịch = Authorized\n2. Chạy job quét kết quả bill\n"
       "3. Mở 販売履歴 đọc trạng thái đơn\n4. Kiểm tra chat 1:1 F1 + notify admin",
       "status trên UnivaPay = Authorized",
       "- Xử lý GIỐNG HỆT case Successful:\n"
       "  · Đơn chuyển「決済成功」\n  · Gửi action「申込完了時」\n"
       "  · Notify「【tên Bot】<line name> <tên qly item> が購入されました」\n"
       "  · Tin LINE「決済が完了しました。」\n- KHÔNG bị coi là fail, KHÔNG xóa đơn",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r321 (Bug Tester #38077, 6/2026 — MỚI NHẤT của tab)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Job quét kết quả — UnivaPay trả Successful (単品) → đơn thành công + gửi đủ action/notify/tin LINE",
       UNI + "\n- Có đơn của F1 đang chờ job quét",
       "1. Đảm bảo giao dịch trên UnivaPay ở trạng thái Successful\n2. Chạy job quét kết quả bill\n"
       "3. Mở 販売履歴 + chat 1:1 F1 + notify admin",
       "status trên UnivaPay = Successful",
       "- Đơn chuyển「決済成功」\n- Gửi action「申込完了時」\n- Notify が購入されました\n"
       "- Tin LINE「決済が完了しました。」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r319."),

    tc("Bill UnivaPay — callback & webhook", "PAY-002", "Abnormal",
       "Job quét kết quả — UnivaPay trả Failed (単品) → xóa đơn + notify lỗi + tin LINE báo lỗi",
       UNI + "\n- Có đơn của F1 đang chờ job quét",
       "1. Đảm bảo giao dịch trên UnivaPay ở trạng thái Failed\n2. Chạy job quét kết quả bill\n"
       "3. Mở 販売履歴 + chat 1:1 F1 + notify admin",
       "status trên UnivaPay = Failed",
       "- Đơn bị xóa khỏi 販売履歴\n- KHÔNG gửi action\n- Notify 決済に失敗しました\n"
       "- Tin LINE「決済に失敗しました。 カードのご利用枠や有効期限などを…」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r320."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "★ Bug Tester #38077 — Authorized coi là thành công ở cả 継続 MUA MỚI và 継続 ĐỔI THẺ",
       UNIC + "\n- Có 1 hợp đồng mua mới và 1 lượt đổi thẻ đang chờ job quét",
       "1. Đặt trạng thái cả 2 giao dịch trên UnivaPay = Authorized\n2. Chạy job quét kết quả bill\n"
       "3. Mở 販売履歴 継続: đọc trạng thái hợp đồng mua mới và bảng 決済履歴 của hợp đồng đổi thẻ\n"
       "4. Kiểm tra chat 1:1 F1",
       "status = Authorized (2 luồng)",
       "- Hợp đồng mua mới: chuyển「継続中/トライアル中」như case Successful, có action + notify\n"
       "- Hợp đồng đổi thẻ: thông tin thẻ cập nhật, 次回決済予定日 được gia hạn, số lần lỗi reset\n"
       "- Cả 2 đều KHÔNG bị coi là fail",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r324 + r327 (Bug Tester #38077)."),

    tc("Bill UnivaPay — callback & webhook", "STATE-001", "Normal",
       "Trạng thái hiển thị & quyền refund ở màn lịch sử theo status_webhook của đơn",
       "- Bot A có 5 đơn 単品 với status_webhook lần lượt: NULL · 1 · 0 · 3 · 4 (status_order = 1)",
       "1. Mở 販売履歴 単品\n2. Đọc trạng thái hiển thị của 5 đơn\n"
       "3. Với từng đơn: mở 注文詳細 kiểm tra nút 返金する có hiện không\n"
       "4. Ở màn list tick chọn cả 5 đơn → bấm 一括返金実行",
       "status_webhook: NULL · 1 · 0 · 3 · 4",
       "- Đơn NULL và 1: hiện trạng thái bình thường, CÓ nút 返金する\n"
       "- Đơn 0, 3, 4: hiện「決済処理中」, ẨN nút 返金する ở màn detail\n"
       "- 一括返金実行: BỎ QUA 3 đơn đang xử lý, chỉ hoàn tiền 2 đơn hợp lệ\n"
       "- Nếu ép refund đơn đang xử lý → báo lỗi「決済処理を行っていますので、操作できません。」",
       note="Nguồn: Improve bill tiền univapay r26-r31 + ListBug r24. Spec BR-14."),

    tc("Bill UnivaPay — callback & webhook", "STATE-001", "Normal",
       "Màn 注文詳細 継続 — trạng thái kỳ thanh toán hiển thị 支払い処理中 khi đang chờ webhook",
       "- Bot A có hợp đồng 継続 với kỳ đang chờ webhook (status_webhook ∈ {0,3,4}), status_bill = 1",
       "1. Mở 注文詳細 của hợp đồng\n2. Đọc trạng thái của KỲ trong bảng 決済履歴\n"
       "3. Đọc trạng thái của HỢP ĐỒNG ở phần trên",
       "status_webhook = 0 / 3 / 4 · status_bill = 1",
       "- Trạng thái KỲ hiển thị「支払い処理中」\n"
       "- Trạng thái HỢP ĐỒNG vẫn hiển thị「継続中」(không đổi theo kỳ)",
       note="Nguồn: Improve bill tiền univapay r174-r176. ListBug r25 ghi bug cũ「text status chưa đúng」→ regression."),

    tc("Bill UnivaPay — callback & webhook", "STATE-001", "Abnormal",
       "Màn list 販売履歴 継続 — không cho HỦY hợp đồng đang chờ webhook",
       "- Bot A có 3 hợp đồng: 1 đang chờ webhook (0/3/4) + 2 bình thường",
       "1. Mở 販売履歴 継続, tick chọn cả 3 hợp đồng\n2. Bấm「一括解約実行」→ xác nhận\n"
       "3. Đọc lại trạng thái 3 hợp đồng",
       "3 hợp đồng, 1 đang chờ webhook",
       "- 2 hợp đồng bình thường: chuyển「キャンセル済」\n"
       "- Hợp đồng đang chờ webhook: BỎ QUA, vẫn ở trạng thái cũ\n"
       "- Không lỗi 500",
       note="Nguồn: Improve bill tiền univapay r181 + ListBug r25 mục 3「Không cho phép cancel」. "
            "⚠ Spec R32: thao tác hàng loạt LUÔN trả success dù từng đơn lỗi → admin không biết đơn nào bị bỏ qua "
            "→ xem MT-21."),

    tc("Bill UnivaPay — callback & webhook", "REG-001", "Normal",
       "Regression — đổi cơ chế bill UnivaPay không làm hỏng bill tiền của Salon / Lesson / Booking Event",
       "- Bot A có sẵn: 1 calendar salon có bill tiền · 1 lesson có bill tiền · 1 booking event có bill tiền\n"
       "- Cùng dùng cổng UnivaPay",
       "1. Đặt lịch salon có thanh toán → hoàn tất\n2. Đặt lịch lesson có thanh toán → hoàn tất\n"
       "3. Đặt booking event có thanh toán → hoàn tất\n4. Với mỗi loại: mở màn quản lý tương ứng kiểm tra đơn "
       "và kiểm tra action gửi cho friend",
       "3 luồng booking có bill tiền",
       "- Cả 3 luồng đều booking + bill tiền THÀNH CÔNG\n"
       "- Thông tin thanh toán được lưu vào đúng màn quản lý của từng tính năng\n"
       "- Action của booking gửi bình thường",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r222-r224. regression — 3 tính năng cùng 1 loại kết quả → 1 TC. "
            "⚠ Chi tiết TC của từng tính năng nằm ở file TCsLine_SalonCalendar / LessonCalendar / EventBooking "
            "(đã loại khỏi phạm vi kho FA-026)."),

    tc("Bill UnivaPay — callback & webhook", "CONC-001", "Abnormal",
       "Double click nút mua khi số tiền vượt hạn mức → chỉ 1 request, message lỗi chỉ hiện 1 lần",
       UNI + "\n- SP giá vượt hạn mức tài khoản UnivaPay",
       "1. Mở page item trên LINE app\n2. Double click rất nhanh nút mua (interval < 500ms)\n"
       "3. Xác nhận trên màn confirm nếu có\n4. Mở Network tab / DB log đếm số request thanh toán\n"
       "5. Đếm số toast lỗi hiển thị",
       "Double click < 500ms, số tiền vượt hạn mức",
       "- Chỉ 1 request thanh toán được gửi\n- Message lỗi hiển thị đúng 1 lần (không stack 2 toast)\n"
       "- Ở trường hợp số tiền hợp lệ: chỉ 1 giao dịch thành công, user KHÔNG bị charge 2 lần",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r299 + r308 + r312 (TC-NEW-02)."),

    tc("Bill UnivaPay — callback & webhook", "PAY-001", "Normal",
       "Bot CHƯA setting Webhook ID → luồng mua vẫn chạy được theo cơ chế polling",
       UNI + "\n" + WH_OFF + "\n- s_strip_bot KHÔNG có univapay_webhook_id",
       "1. F1 mua sản phẩm bằng thẻ đúng\n2. Quan sát màn hình phía LINE\n3. Mở 販売履歴 đọc trạng thái đơn",
       "Không có webhook ID",
       "- Mua thành công bình thường (hệ thống polling kết quả thay vì chờ callback)\n"
       "- Đơn ở trạng thái 決済成功",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r289「Check setting không Webhook ID」(TC gốc chỉ có tiêu đề). "
            "Kết quả mong đợi do AI viết theo spec §2.4 isProcessWithWebhook — CẦN LEADER XÁC NHẬN."),

    # ══════ 21. Bill Stripe — tạo order trước ══════
    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Bấm mua (Stripe) → tạo TRƯỚC bản ghi đơn ở trạng thái chờ, chưa phải 決済成功",
       "- SP là 単品商品 テスト環境 cổng Stripe\n- Friend F1 đang ở màn 最終確認",
       "1. F1 bấm 購入する\n2. NGAY LẬP TỨC mở 販売履歴 tìm đơn của F1\n3. Đọc trạng thái đơn",
       "Cổng Stripe",
       "- Đơn đã xuất hiện ở 販売履歴 ngay khi bấm mua\n- Trạng thái là「決済処理中」, chưa phải 決済成功",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r4 (status_webhook = 3). Spec §2.4 EP-80 paymentIntent "
            "tạo trước bản ghi với status_webhook = 3."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe — bill SUCCESS bằng thẻ thường → GIỮ bản ghi, chuyển 決済成功, gửi action + notify",
       "- SP 単品 テスト環境 cổng Stripe, đã gắn action「申込完了時」",
       "1. F1 mua với thẻ 4242 4242 4242 4242\n2. Mở 販売履歴 đọc trạng thái đơn\n"
       "3. Kiểm tra chat 1:1 F1 + notify admin\n4. Đối chiếu dashboard Stripe",
       "Thẻ 4242 4242 4242 4242",
       "- Đơn KHÔNG bị xóa, chuyển sang「決済成功」\n- F1 nhận action「申込完了時」\n"
       "- Admin nhận notify が購入されました\n- Trên Stripe có giao dịch thành công đúng số tiền",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r5."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe — bill SUCCESS bằng thẻ 3DS (complete) → cùng kết quả với thẻ thường",
       "- SP 単品 テスト環境 cổng Stripe",
       "1. F1 mua với thẻ 4000 0038 0000 0446 → popup 3DS → bấm complete\n2. Mở 販売履歴\n"
       "3. Kiểm tra chat 1:1 + notify + dashboard Stripe",
       "Thẻ 4000 0038 0000 0446 + complete 3DS",
       "- Đơn chuyển「決済成功」\n- Có action「申込完了時」và notify\n- Trên Stripe có giao dịch thành công",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r6."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe — bill FAIL bằng thẻ 0341 → XÓA bản ghi đơn, không action, có notify lỗi",
       "- SP 単品 テスト環境 cổng Stripe, đã gắn action「申込完了時」",
       "1. F1 mua với thẻ 4000 0000 0000 0341\n2. Mở 販売履歴 tìm đơn của F1\n"
       "3. Kiểm tra chat 1:1 F1 + notify admin",
       "Thẻ 4000 0000 0000 0341",
       "- KHÔNG còn đơn nào của F1 ở 販売履歴 (bản ghi tạm đã bị xóa)\n"
       "- F1 KHÔNG nhận action\n- Admin nhận notify case bill fail",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r7."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe — popup 3DS bấm FAIL/hủy → xóa bản ghi đơn, không action",
       "- SP 単品 テスト環境 cổng Stripe",
       "1. F1 mua với thẻ 3DS → ở popup bấm fail hoặc hủy\n2. Mở 販売履歴 tìm đơn\n"
       "3. Kiểm tra chat 1:1 + notify",
       "Thẻ 3DS + thao tác fail/hủy",
       "- Đơn tạm bị xóa khỏi 販売履歴\n- Không gửi action\n- Có notify case bill fail",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r8."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe — job quét kết quả bill SUCCESS → cập nhật đơn + gửi thêm tin LINE 決済が完了しました",
       "- Có đơn Stripe của F1 đang ở trạng thái chờ (status_webhook = 3, update_at đã quá 15 phút)",
       "1. Chạy job quét kết quả bill Stripe\n2. Mở 販売履歴 đọc trạng thái đơn\n"
       "3. Kiểm tra chat 1:1 F1 + notify admin",
       "Đơn chờ > 15 phút, kết quả thật là success",
       "- Đơn chuyển「決済成功」\n- F1 nhận action「申込完了時」\n- Admin nhận notify が購入されました\n"
       "- F1 nhận tin LINE「決済が完了しました。」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r9. Cách tạo data (theo tester): bill success → sửa "
            "status_webhook = 3 → sửa update_at về trước hiện tại 14 phút."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe — job quét kết quả bill FAIL → xóa đơn + tin LINE báo lỗi",
       "- Có đơn Stripe của F1 ở trạng thái chờ, kết quả thật là fail",
       "1. Chạy job quét kết quả bill Stripe\n2. Mở 販売履歴\n3. Kiểm tra chat 1:1 F1 + notify admin",
       "Đơn chờ, kết quả thật là fail",
       "- Đơn bị xóa khỏi 販売履歴\n- KHÔNG gửi action\n- Admin nhận notify 決済に失敗しました\n"
       "- F1 nhận tin LINE「決済に失敗しました。 カードのご利用枠や有効期限などを…」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r10. Cách tạo data (theo tester): bill fail → tạo 1 bản ghi fake "
            "trong s_order_history với order id vừa bị xóa."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Abnormal",
       "★ 10/2025 CHANGE SPEC — đóng trình duyệt ở popup 3DS (chưa bill) → job KHÔNG tính là bill fail",
       "- SP 単品 テスト環境 cổng Stripe",
       "1. F1 mua với thẻ 3DS → popup xác nhận hiện ra\n2. ĐÓNG TRÌNH DUYỆT (không bấm complete/fail)\n"
       "3. Chờ job quét kết quả bill chạy\n4. Mở 販売履歴 · chat 1:1 F1 · notify admin",
       "Đóng trình duyệt ở popup 3DS",
       "- Bản ghi đơn bị XÓA\n- KHÔNG gửi action\n- KHÔNG gửi notify\n"
       "- KHÔNG gửi tin nhắn báo thanh toán thất bại cho user",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r11 / r21 / r29 / r46 — ghi rõ「10/2025: Change spec: case này khi "
            "job quét sẽ không tính là bill fail」. Đây là SPEC MỚI thay thế hành vi cũ (trước đó coi là fail)."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe 継続 — trial KHÔNG có giá kỳ đầu → tạo bản ghi hợp đồng và kỳ ở trạng thái ĐÃ XỬ LÝ ngay (không bill)",
       "- SP-C 継続 テスト環境 cổng Stripe, có trial, KHÔNG set giá kỳ đầu",
       "1. F1 mua SP-C\n2. NGAY sau khi bấm mua, mở 販売履歴 継続 đọc trạng thái hợp đồng\n"
       "3. Mở 注文詳細 đọc bảng 決済履歴\n4. Đối chiếu dashboard Stripe",
       "flag_trial=1 · flag_first=0",
       "- Hợp đồng tạo ngay với trạng thái「トライアル中」(KHÔNG qua trạng thái 決済処理中)\n"
       "- Bảng 決済履歴 có 1 dòng số tiền 0円 ở trạng thái đã xử lý\n"
       "- Trên Stripe: có SetupIntent lưu thẻ, KHÔNG có giao dịch trừ tiền",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r13 (status_webhook = 1 ngay từ đầu — khác các case còn lại)."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe 継続 — 3 pattern CÓ bill kỳ đầu (trial+giá đầu · không trial+giá đầu · không trial+không giá đầu) "
       "đều tạo bản ghi ở trạng thái CHỜ rồi chuyển 決済成功",
       "- 3 sản phẩm 継続 テスト環境 cổng Stripe tương ứng 3 pattern",
       "1. Với mỗi sản phẩm: F1 mua bằng thẻ 4242 4242 4242 4242\n"
       "2. NGAY sau khi bấm mua: mở 販売履歴 継続 đọc trạng thái\n"
       "3. Sau khi có kết quả: đọc lại trạng thái hợp đồng và bảng 決済履歴\n"
       "4. Kiểm tra chat 1:1 F1",
       "Pattern 1: trial + giá đầu 500円\nPattern 2: không trial + giá đầu 500円\nPattern 3: không trial + không giá đầu (3.000円)",
       "- Cả 3 pattern: ngay sau khi bấm mua, hợp đồng ở trạng thái「決済処理中」\n"
       "- Sau khi có kết quả success: hợp đồng chuyển「トライアル中」(pattern 1) hoặc「継続中」(pattern 2, 3)\n"
       "- Bảng 決済履歴 có 1 dòng đúng số tiền tương ứng (500 / 500 / 3.000円)\n"
       "- F1 nhận action「申込完了時」và「初回決済時」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r14-r16, r22-r24, r30-r32. 3 pattern cùng 1 CHUỖI trạng thái "
            "(chờ → thành công) nhưng khác số tiền → liệt kê đủ 3 ở cột Dữ liệu test."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe 継続 — bill FAIL khi mua mới → XÓA CẢ hợp đồng lẫn kỳ, gửi action bill fail + notify",
       "- SP-C 継続 テスト環境 cổng Stripe, đã gắn action「決済エラー発生時」",
       "1. F1 mua SP-C với thẻ fail 4000 0000 0000 0341\n2. Quan sát màn hình phía LINE\n"
       "3. Mở 販売履歴 継続 tìm hợp đồng của F1\n4. Kiểm tra chat 1:1 F1 + notify admin",
       "Thẻ 4000 0000 0000 0341",
       "- Phía LINE hiện message bill lỗi, quay về màn nhập thẻ\n"
       "- KHÔNG còn bản ghi hợp đồng NÀO của F1 cho SP-C\n"
       "- F1 nhận action case bill fail\n"
       "- Admin nhận notify「【tên Bot】<line name> <tên qly item> の決済に失敗しました」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r17-r18 / r25-r26 / r33-r34."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe đổi thẻ CÓ bill lại — thành công → cập nhật thẻ + gia hạn + reset đếm lỗi + thêm dòng 決済履歴",
       "- Hợp đồng SP-C của F1 đang bill lỗi, cổng Stripe",
       "1. Ghi lại 次回決済予定日 và số dòng 決済履歴\n"
       "2. F1 đổi thẻ bằng 4242 4242 4242 4242 (hoặc thẻ 3DS rồi complete)\n"
       "3. Mở 注文詳細 đối chiếu\n4. Kiểm tra dashboard Stripe",
       "Thẻ 4242 4242 4242 4242 / thẻ 3DS 4000 0038 0000 0446",
       "- Thông tin thẻ ở 注文詳細 = thẻ mới\n- 次回決済予定日 được gia hạn\n"
       "- Số lần lỗi reset (hợp đồng thoát trạng thái 延滞)\n- 決済履歴 có thêm 1 dòng bill thành công\n"
       "- Trên Stripe có giao dịch trừ tiền tương ứng",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r39-r41. 2 loại thẻ cùng 1 kết quả → giữ chung 1 TC."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe đổi thẻ CÓ bill lại — job quét sau đó phát hiện FAIL → gửi tin LINE báo lỗi, tăng đếm lỗi",
       "- Hợp đồng SP-C của F1 đang bill lỗi, cổng Stripe",
       "1. F1 đổi thẻ bằng thẻ fail 4000 0000 0000 0341\n2. Chờ / chạy job quét kết quả bill\n"
       "3. Mở 注文詳細 đọc 次回決済予定日 và số lần lỗi\n4. Kiểm tra chat 1:1 F1",
       "Thẻ fail 4000 0000 0000 0341",
       "- 次回決済予定日 KHÔNG đổi\n- Số lần lỗi tăng thêm 1\n"
       "- Thông tin thẻ vẫn được cập nhật sang thẻ mới\n"
       "- F1 nhận tin LINE「決済に失敗しました。 カードのご利用枠や有効期限などを…」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r45."),

    tc("Bill Stripe — tạo order trước", "PAY-001", "Normal",
       "Stripe — mua sản phẩm có tên chứa ký tự đặc biệt/JP/emoji → dashboard Stripe hiển thị đúng tên",
       "- Bot A đã liên kết Stripe\n- Tạo các sản phẩm với 表示商品名 lần lượt chứa các loại ký tự bên dưới",
       "1. Với mỗi sản phẩm: F1 mua bằng thẻ 4242 4242 4242 4242 → thành công\n"
       "2. Mở dashboard Stripe, tra giao dịch tương ứng\n3. Đọc phần description của giao dịch",
       "Tên = 0 · space đầu · space cuối · nhiều space giữa · "
       "``~!@#$%^&()+=_\"<>{}[]|.,/*\\:? · ・ー【】〜！＠＃＄％＾＆＊（）「」｜￥；。→■∞ · "
       "まことボット智恵助 · AIボット🤖_Ver1 · こーだい/プレゼント専用🎁 · tên có xuống dòng",
       "- Tất cả các trường hợp: mua thành công\n"
       "- Trên Stripe, description của giao dịch hiển thị đúng tên sản phẩm (không mojibake, không rỗng)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r49-r58 (SpecImprove #34857, 3/2026 — thêm description khi thanh toán "
            "stripe). 10 input cùng 1 kết quả → giữ chung 1 TC. Áp cho cả 単品 (r49-r58) và 継続 (r64-r73)."),

    tc("Bill Stripe — tạo order trước", "PAY-002", "Abnormal",
       "Stripe — mua FAIL với sản phẩm có tên đặc biệt → giao dịch vẫn được ghi nhận bên Stripe với status failed",
       "- Sản phẩm có 表示商品名 chứa ký tự đặc biệt + emoji",
       "1. F1 mua với thẻ fail 4000 0000 0000 0341\n2. Mở dashboard Stripe tra giao dịch\n"
       "3. Lặp lại với thẻ 3DS rồi bấm fail/hủy",
       "Thẻ 4000 0000 0000 0341 · thẻ 3DS 4000 0038 0000 0446 + fail",
       "- Cả 2 trường hợp: trên Stripe vẫn ghi nhận giao dịch với trạng thái failed\n"
       "- Description vẫn hiển thị đúng tên sản phẩm",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r59-r60 / r74-r75."),

    tc("Bill Stripe — tạo order trước", "COMPAT-LEGACY-001", "Normal",
       "Đơn theo cơ chế THANH TOÁN CŨ vẫn mở được màn giao dịch bên Stripe từ màn lịch sử",
       "- Bot A có đơn cũ (payment_new = 0) và đơn mới (payment_new = 1) trong 販売履歴",
       "1. Mở 注文詳細 của 1 đơn CŨ 単品 → bấm badge/link 決済ステータス\n"
       "2. Lặp lại với 1 đơn CŨ của hợp đồng 継続\n3. Lặp lại với đơn MỚI (単品 và 継続)",
       "payment_new = 0 (cũ) và = 1 (mới)",
       "- Cả 4 trường hợp đều mở được màn giao dịch tương ứng bên Stripe\n"
       "- 単品: link gắn đúng charge id · 継続: link gắn đúng customer id",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r57-r58. regression"),

    tc("Bill Stripe — tạo order trước", "COMPAT-LEGACY-001", "Normal",
       "Hợp đồng bill theo logic CŨ → sau khi đổi thẻ thì chuyển sang bill theo logic MỚI",
       "- Hợp đồng của F1 được tạo theo cơ chế cũ (payment_new = 0)",
       "1. F1 đổi thẻ → sửa cho hết hạn kỳ → chạy job bill theo logic mới\n"
       "2. Mở 注文詳細 kiểm tra bill thành công và thông tin thẻ\n3. Đối chiếu dashboard Stripe",
       "Hợp đồng payment_new = 0 → đổi thẻ",
       "- Bill kỳ mới thành công theo thẻ mới\n- Hợp đồng chuyển sang dùng cơ chế thanh toán mới\n"
       "- 次回決済予定日 được gia hạn",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r56「tbl cycle_order_history. payment_new update thành 1 / "
            "trường strip_pm_id có data」. regression"),
]
