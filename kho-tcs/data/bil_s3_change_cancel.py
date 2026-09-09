# -*- coding: utf-8 -*-
"""FA-026 商品販売 — Nhóm 17-19: Đổi thẻ · Hủy hợp đồng · Trang hoàn tất & 特商法 public.

Nguồn chính: 12. TCsLine_Item / tab「Improve bill tiền stripe」r38-r46,
             tab「Improve bill tiền univapay」r93-r112 / r157-r170 / r225-r232 / r252-r258,
             tab「test fix bug」r71-r81 (Bug #29472), tab「Quản lý sản phẩm」r324-r333.
"""
from _common import tc

CY = ("- Friend F1 đã mua SP-C (継続商品, テスト環境) và đang có hợp đồng 継続中\n"
      "- Bot A đã liên kết cổng thanh toán tương ứng")
CY_ERR = ("- Friend F1 có hợp đồng SP-C ở trạng thái BILL LỖI\n"
          "- Cách tạo data: bill success → sửa s_cycle_order_history cho hết c_expired_date "
          "và set count_bill_error > 0")

S3 = [
    # ══════ 17. LINE user — đổi thẻ ══════
    tc("LINE user — đổi thẻ", "FUNC-001", "Normal",
       "Đổi thẻ khi hợp đồng CHƯA hết hạn kỳ → chỉ cập nhật thẻ, KHÔNG bill tiền, KHÔNG tạo lịch sử",
       CY + "\n- c_expired_date của hợp đồng vẫn còn hạn (chưa tới kỳ bill)",
       "1. Ghi lại 4 số cuối thẻ hiện tại ở 注文詳細 và số dòng ở bảng 決済履歴\n"
       "2. F1 mở link type=product-change → nhập thẻ mới hợp lệ → xác nhận\n"
       "3. Mở lại 注文詳細 của hợp đồng\n4. Đối chiếu dashboard cổng thanh toán",
       "Thẻ cũ 4242… → thẻ mới 4000 0038 0000 0446",
       "- Phía LINE hiện màn đổi thẻ thành công\n"
       "- 注文詳細: thông tin thẻ đổi thành 4 số cuối của thẻ MỚI\n"
       "- Bảng 決済履歴 KHÔNG có dòng mới (không bill tiền)\n"
       "- 次回決済予定日 KHÔNG đổi\n- Cổng thanh toán không phát sinh giao dịch trừ tiền",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r38 + univapay r93 / r225 / r252."),

    tc("LINE user — đổi thẻ", "FUNC-001", "Normal",
       "Đổi thẻ khi hợp đồng ĐANG BILL LỖI → bill lại luôn, thành công thì gia hạn và reset đếm lỗi",
       CY_ERR,
       "1. Ghi lại c_expired_date, số lần lỗi và số dòng 決済履歴 trước khi thao tác\n"
       "2. F1 mở link type=product-change → nhập thẻ hợp lệ 4242 4242 4242 4242 → xác nhận\n"
       "3. Mở 注文詳細 của hợp đồng\n4. Đối chiếu dashboard cổng thanh toán",
       "Thẻ hợp lệ 4242 4242 4242 4242",
       "- Phía LINE hiện màn đổi thẻ thành công\n"
       "- 注文詳細: thông tin thẻ = thẻ mới; 次回決済予定日 được GIA HẠN sang kỳ tiếp\n"
       "- Bảng 決済履歴 có THÊM 1 dòng bill thành công đúng số tiền kỳ\n"
       "- Số lần lỗi được reset (hợp đồng không còn ở trạng thái 延滞)\n"
       "- Cổng thanh toán có giao dịch trừ tiền tương ứng",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r39-r41 + univapay r95 / r226 / r253. Spec §2.5: "
            "điều kiện retry bill = count_bill_error đã set VÀ c_expired_date < now()."),

    tc("LINE user — đổi thẻ", "PAY-002", "Abnormal",
       "Đổi thẻ có bill lại nhưng BILL FAIL → vẫn cập nhật thẻ mới, KHÔNG gia hạn, tăng số lần lỗi",
       CY_ERR,
       "1. Ghi lại c_expired_date và số lần lỗi hiện tại\n"
       "2. F1 mở link đổi thẻ → nhập thẻ fail 4000 0000 0000 0341 → xác nhận\n"
       "3. Quan sát màn hình phía LINE\n4. Mở 注文詳細 của hợp đồng",
       "Thẻ fail 4000 0000 0000 0341",
       "- Phía LINE hiện message báo lỗi thanh toán\n"
       "- 注文詳細: thông tin thẻ VẪN được cập nhật sang thẻ mới (hành vi logic cũ)\n"
       "- 次回決済予定日 KHÔNG đổi\n- Số lần lỗi tăng thêm 1",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r42-r43「thông tin card: update thông tin card mới "
            "(logic cũ từ trước case fail vẫn update lại thông tin card)」+ univapay r96 / r99."),

    tc("LINE user — đổi thẻ", "PAY-002", "Abnormal",
       "Đổi thẻ nhập SAI THẺ (4111…) → báo lỗi, giữ nguyên thẻ cũ",
       CY + "\n- Cổng UnivaPay",
       "1. Ghi lại 4 số cuối thẻ hiện tại\n2. F1 mở link đổi thẻ → nhập 4111 1111 1111 1111 → xác nhận\n"
       "3. Quan sát message lỗi\n4. Mở 注文詳細 đối chiếu thẻ",
       "Thẻ 4111 1111 1111 1111",
       "- Phía LINE hiện message báo lỗi (nội dung do cổng thanh toán trả về)\n"
       "- Ghi lại kết quả THẬT ở 注文詳細: thẻ giữ nguyên thẻ cũ HAY bị đổi sang thẻ mới\n"
       "- 次回決済予定日 không đổi, số lần lỗi không giảm",
       env="PRODUCTION",
       note="⚠ MÂU THUẪN TRONG CORPUS: univapay r232 ghi「vẫn giữ nguyên thông tin card cũ」nhưng cùng ô lại "
            "có chữ「update thông tin card mới」(2 câu chồng nhau, r258 cũng vậy); trong khi stripe r42-r43 khẳng "
            "định fail VẪN update thẻ mới. Đây là MT-15 — expected để mở, CẦN LEADER QUYẾT. "
            "Bug #29472 r79 ghi thêm: báo lỗi bằng TIẾNG ANH do univapay/stripe trả về."),

    tc("LINE user — đổi thẻ", "MSG-001", "Normal",
       "Đổi thẻ có bill lại — hợp đồng trial 0円 mua lần đầu → gửi action & notify KỲ ĐẦU",
       "- SP-C có trial và bill kỳ đầu 0円\n- F1 đã mua, hết trial, job bill LỖI\n"
       "- Cách tạo data: duplicate 1 bản ghi s_order_history từ bản gốc, sửa status_bill = 3 và "
       "amount_order > 0; sửa c_expired_date của s_cycle_order_history cho hết hạn",
       "1. F1 mở link đổi thẻ → nhập thẻ hợp lệ → xác nhận thành công\n"
       "2. Kiểm tra chat 1:1 của F1\n3. Kiểm tra notify phía admin",
       "Hợp đồng trial 0円, chưa từng bill thật",
       "- F1 nhận action của slot「初回決済時」\n"
       "- Notify:「【tên Bot】<line name> <tên qly item> の初回決済が行われました」",
       env="PRODUCTION",
       note="Nguồn: test fix bug r76 (Bug #29472: sau khi bill thất bại user vào change card nhưng action và "
            "notify đều không chạy)."),

    tc("LINE user — đổi thẻ", "MSG-001", "Normal",
       "Đổi thẻ có bill lại — hợp đồng đã từng bill kỳ đầu → gửi action & notify KỲ 2",
       "- SP-C có trial và CÓ giá kỳ đầu; F1 đã bill kỳ đầu thành công, kỳ tiếp job bill LỖI",
       "1. F1 mở link đổi thẻ → nhập thẻ hợp lệ → xác nhận thành công\n"
       "2. Kiểm tra chat 1:1 của F1\n3. Kiểm tra notify phía admin",
       "Hợp đồng đã bill kỳ đầu",
       "- F1 nhận action của slot「2回目以降決済時」\n"
       "- Notify:「【tên Bot】<line name> <tên qly item> の継続決済が行われました」",
       env="PRODUCTION",
       note="Nguồn: test fix bug r77-r78 (Bug #29472)."),

    tc("LINE user — đổi thẻ", "MSG-001", "Normal",
       "Đổi thẻ KHÔNG bill tiền → KHÔNG gửi action, KHÔNG gửi notify",
       CY + "\n- Hợp đồng vẫn còn hạn (chưa tới kỳ bill)",
       "1. F1 mở link đổi thẻ → nhập thẻ hợp lệ → xác nhận thành công\n"
       "2. Kiểm tra chat 1:1 của F1\n3. Kiểm tra notify phía admin",
       "Đổi thẻ thuần, không bill",
       "- F1 KHÔNG nhận action nào\n- Admin KHÔNG nhận notify nào",
       env="PRODUCTION",
       note="Nguồn: test fix bug r75「không action, không send notify」."),

    tc("LINE user — đổi thẻ", "MSG-001", "Abnormal",
       "Đổi thẻ BILL FAIL → không gửi action, nhưng CÓ gửi notify bill lỗi",
       CY_ERR,
       "1. F1 mở link đổi thẻ → nhập thẻ fail → xác nhận\n2. Kiểm tra chat 1:1 của F1\n"
       "3. Kiểm tra notify phía admin",
       "Thẻ fail",
       "- F1 KHÔNG nhận action「初回決済時」/「2回目以降決済時」\n"
       "- Có gửi notify case bill fail (đây là điểm đã từng bị bỏ sót, xem ListBug r23)",
       env="PRODUCTION",
       note="Nguồn: test fix bug r79 + ListBug r23「item chu kỳ => change card | case callback fail không gửi "
            "message bill fail | Fixed | OK」. regression"),

    tc("LINE user — đổi thẻ", "FUNC-001", "Normal",
       "稼働回数「1度のみ」của action bill — user đã từng nhận action rồi thì đổi thẻ không gửi lại",
       "- SP-C có action「2回目以降決済時」đặt 稼働回数 =「1度のみ」\n"
       "- F1 ĐÃ từng nhận action này trước đó\n- Hợp đồng của F1 đang ở trạng thái bill lỗi",
       "1. F1 mở link đổi thẻ → nhập thẻ hợp lệ → bill lại thành công\n2. Kiểm tra chat 1:1 của F1",
       "count_action_purchase_2st > 0",
       "- F1 KHÔNG nhận thêm action và KHÔNG nhận notify của action đó",
       env="PRODUCTION",
       note="Nguồn: test fix bug r80 (kèm cách tạo data của tester: sửa DB để reset)."),

    tc("LINE user — đổi thẻ", "FUNC-001", "Normal",
       "稼働回数「何度でも」→ mỗi lần đổi thẻ bill thành công đều gửi action + notify",
       "- SP-C có action「2回目以降決済時」đặt 稼働回数 =「何度でも」\n"
       "- F1 đã từng nhận action này, hợp đồng đang bill lỗi",
       "1. F1 mở link đổi thẻ → bill lại thành công\n2. Kiểm tra chat 1:1 của F1",
       "auto = 何度でも",
       "- F1 nhận action và notify bình thường (dù trước đó đã nhận rồi)",
       env="PRODUCTION",
       note="Nguồn: test fix bug r81."),

    tc("LINE user — đổi thẻ", "STATE-001", "Abnormal",
       "Mở link đổi thẻ khi đơn đang chờ webhook (status_webhook 0/3/4) → chặn",
       CY + "\n- Hợp đồng của F1 đang ở trạng thái chờ kết quả thanh toán",
       "1. F1 mở link type=product-change\n2. Đọc thông báo\n3. Lặp lại với status_webhook = 0 và = 4",
       "status_webhook = 3 / 0 / 4",
       "- Cả 3 trạng thái đều hiện lỗi「決済処理を行っていますので、操作できません。」\n"
       "- Không vào được màn nhập thẻ",
       note="Nguồn: Improve bill tiền univapay r166-r168. Spec BR-14. "
            "ListBug r12 ghi bug cũ:「access link change card và link cancel thì đang hiện message lỗi chưa đúng」. regression"),

    tc("LINE user — đổi thẻ", "STATE-001", "Normal",
       "Mở link đổi thẻ khi trạng thái bình thường (status_webhook NULL/1/2) → cho phép đổi thẻ",
       CY,
       "1. F1 mở link type=product-change với hợp đồng status_webhook = NULL → quan sát\n"
       "2. Lặp lại với status_webhook = 1 và = 2",
       "status_webhook = NULL / 1 / 2",
       "- Cả 3 trạng thái đều mở được màn nhập thẻ, đổi thẻ được",
       note="Nguồn: Improve bill tiền univapay r164-r165 + r169."),

    tc("LINE user — đổi thẻ", "STATE-001", "Abnormal",
       "Mở link đổi thẻ khi hợp đồng ĐÃ HỦY → báo「キャンセル済です」",
       CY + "\n- Hợp đồng của F1 đã bị hủy (status_bill = 3)",
       "1. F1 mở link type=product-change\n2. Đọc thông báo",
       "status_bill = 3",
       "- Hiện thông báo「キャンセル済です」\n- Không vào được màn nhập thẻ",
       note="Nguồn: Improve bill tiền univapay r170. Spec §2.5 bảng status_contract."),

    tc("LINE user — đổi thẻ", "SEC-001", "Normal",
       "Đổi thẻ sang thẻ 3DS cần xác thực → hiện popup, complete thì cập nhật thẻ mới",
       CY + "\n- Cổng Stripe, thẻ hiện tại là 4242 (không cần xác thực)",
       "1. F1 mở link đổi thẻ → nhập 4000 0000 0000 3220 → xác nhận\n"
       "2. Popup 3DS hiện → bấm complete\n3. Mở 注文詳細 đối chiếu thẻ\n"
       "4. Sửa c_expired_date cho hết hạn rồi chạy job bill → quan sát kết quả",
       "Thẻ 4000 0000 0000 3220 (cần xác thực MỌI giao dịch)",
       "- Popup 3DS hiện, complete xong thông tin thẻ được cập nhật\n"
       "- ⚠ Khi job bill chạy: dự kiến BILL LỖI vì thẻ này cần xác thực từng giao dịch mà job bill "
       "chạy off-session (không 3DS) → nếu bill thành công thì cần xác nhận lại với dev",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r33-r37 / r41-r45 (tester ghi「job sẽ bill lỗi do card này "
            "cần authen => đã báo cho a Thắng」). Đây là hạn chế đã biết, xem MT-16."),

    tc("LINE user — đổi thẻ", "SEC-001", "Normal",
       "Đổi thẻ sang thẻ 3DS chỉ xác thực 1 lần (…0446) → job bill kỳ sau chạy được bình thường",
       CY + "\n- Cổng Stripe",
       "1. F1 đổi thẻ sang 4000 0038 0000 0446, hoàn tất xác thực\n"
       "2. Sửa c_expired_date cho hết hạn\n3. Chạy job bill định kỳ\n4. Mở 注文詳細 + dashboard Stripe",
       "Thẻ 4000 0038 0000 0446",
       "- Job bill kỳ tới THÀNH CÔNG theo thẻ mới\n- 次回決済予定日 được gia hạn\n"
       "- Trên Stripe có giao dịch mới đúng số tiền",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r38 + r46."),

    tc("LINE user — đổi thẻ", "SEC-001", "Normal",
       "Đổi từ thẻ CẦN xác thực sang thẻ KHÔNG cần xác thực → job bill kỳ sau chạy bình thường",
       CY + "\n- Thẻ hiện tại là loại cần xác thực",
       "1. F1 đổi thẻ sang 4242 4242 4242 4242\n2. Sửa c_expired_date cho hết hạn → chạy job bill\n"
       "3. Mở 注文詳細 + dashboard Stripe",
       "Thẻ 4242 4242 4242 4242",
       "- Bill kỳ tới thành công theo thẻ mới, 次回決済予定日 được gia hạn",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r39-r40 / r49-r50."),

    tc("LINE user — đổi thẻ", "CONC-001", "Abnormal",
       "Double click nút xác nhận đổi thẻ → chỉ 1 request, không bill trùng",
       CY_ERR,
       "1. F1 mở link đổi thẻ, nhập thẻ hợp lệ\n2. Double click nhanh nút xác nhận (< 500ms)\n"
       "3. Mở bảng 決済履歴 của hợp đồng\n4. Đối chiếu dashboard cổng thanh toán",
       "Double click < 500ms",
       "- Chỉ có ĐÚNG 1 dòng bill mới trong 決済履歴\n"
       "- Cổng thanh toán chỉ có 1 giao dịch (không bị trừ tiền 2 lần)\n- Action/notify chỉ gửi 1 lần",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r231「Double click button bill」(TC gốc chỉ có tiêu đề). "
            "Kết quả mong đợi do AI viết theo tiền lệ r299/r312 — CẦN LEADER XÁC NHẬN."),

    # ══════ 18. LINE user — hủy hợp đồng ══════
    tc("LINE user — hủy hợp đồng", "FUNC-001", "Normal",
       "User bấm hủy ở trang 解約用ページ → hợp đồng chuyển ĐÃ HỦY, gửi action 解約時",
       CY + "\n- SP-C đã gắn action ở slot「解約時」",
       "1. F1 mở link type=product-cancel\n2. Đọc nội dung 解約案内 và nhãn nút hủy\n"
       "3. Bấm nút hủy → xác nhận\n4. Mở 販売履歴 継続 phía admin xem trạng thái hợp đồng\n"
       "5. Kiểm tra chat 1:1 của F1\n6. Đối chiếu dashboard cổng thanh toán",
       "Hợp đồng đang 継続中",
       "- Trang hủy hiện đúng nội dung và nhãn nút đã setting\n"
       "- Sau khi hủy: hợp đồng ở 販売履歴 chuyển trạng thái「キャンセル済」, có ngày hủy\n"
       "- F1 NHẬN action của slot「解約時」\n"
       "- Cột 継続中 của SP-C giảm 1\n"
       "- ⚠ Kiểm tra trên cổng thanh toán: subscription/recurring token có bị hủy không",
       env="PRODUCTION",
       note="Nguồn: r330 + r333 + r359 + r407 + r413. Spec §2.5: user_cancel='customer' → LUÔN chạy action "
            "「解約時」kể cả flagExecuteAction=0. ⚠ Spec R10: cancelCycle() của cron KHÔNG gọi API hủy "
            "subscription bên cổng → xem MT-17."),

    tc("LINE user — hủy hợp đồng", "STATE-001", "Abnormal",
       "Mở link hủy khi đơn đang chờ webhook (0/3/4) → chặn với message riêng",
       CY + "\n- Hợp đồng của F1 đang chờ kết quả thanh toán",
       "1. F1 mở link type=product-cancel\n2. Đọc thông báo\n3. Lặp lại với status_webhook = 0 và = 4",
       "status_webhook = 3 / 0 / 4",
       "- Cả 3 trạng thái đều hiện lỗi「決済処理を行っていますので、操作できません。」\n- Không hủy được",
       note="Nguồn: Improve bill tiền univapay r166-r168."),

    tc("LINE user — hủy hợp đồng", "STATE-001", "Abnormal",
       "Mở link hủy khi hợp đồng ĐÃ HỦY → báo「キャンセル済です」",
       CY + "\n- Hợp đồng của F1 đã hủy (status_bill = 3)",
       "1. F1 mở link type=product-cancel\n2. Đọc thông báo\n3. Kiểm tra không phát sinh action lần 2",
       "status_bill = 3",
       "- Hiện「キャンセル済です」\n- KHÔNG gửi thêm action「解約時」lần nữa",
       note="Nguồn: Improve bill tiền univapay r170 + spec §2.5 bảng status_contract."),

    tc("LINE user — hủy hợp đồng", "STATE-001", "Abnormal",
       "Mở link hủy khi CHƯA từng mua → báo「この商品は購入されていません。」",
       "- Friend F5 đã kết bạn nhưng chưa từng mua SP-C",
       "1. F5 mở link type=product-cancel của SP-C\n2. Đọc thông báo",
       "status_contract = 0 (unregister)",
       "- Hiện「この商品は購入されていません。」",
       note="Nguồn: test fix bug r207 / r221 / r235 / r249. Spec §2.5."),

    tc("LINE user — hủy hợp đồng", "DATA-001", "Normal",
       "Hủy hợp đồng khi ĐANG TRIAL → đếm số hợp đồng trial giảm, không phát sinh bill",
       CY + "\n- Hợp đồng của F1 đang ở trạng thái トライアル中",
       "1. Ghi lại cột「トライアル中」của SP-C ở list\n2. F1 mở link hủy → bấm hủy → xác nhận\n"
       "3. Xem lại cột「トライアル中」\n4. Chờ qua ngày hết trial, chạy job bill định kỳ\n"
       "5. Kiểm tra thẻ F1 và dashboard cổng thanh toán",
       "Hợp đồng トライアル中, trial còn 3 ngày",
       "- Cột「トライアル中」của SP-C giảm 1 ngay sau khi hủy\n"
       "- Sau ngày hết trial, job bill KHÔNG trừ tiền F1\n- Cổng thanh toán không phát sinh giao dịch mới",
       env="PRODUCTION",
       note="Suy luận của AI từ spec BR-09「Huỷ trong trial → number_trial(_test) − 1 và number_cancel(_test) + 1」"
            "+ §7.2 (job chỉ quét status_bill = 1). Corpus KHÔNG có TC hủy trong trial. CẦN LEADER XÁC NHẬN."),

    tc("LINE user — hủy hợp đồng", "FUNC-001", "Normal",
       "Sau khi hủy → user mở lại link MUA MỚI thì mua lại được (tạo hợp đồng mới)",
       CY,
       "1. F1 hủy hợp đồng ở link 解約\n2. F1 mở link type=product-detail\n3. Hoàn tất mua lại\n"
       "4. Mở 販売履歴 継続 đếm số hợp đồng của F1 cho SP-C",
       "Hợp đồng cũ status_bill = 3",
       "- Mua lại thành công\n- Có 2 bản ghi hợp đồng: 1 キャンセル済 (cũ) + 1 継続中/トライアル中 (mới)\n"
       "- 注文番号 của hợp đồng mới khác hợp đồng cũ",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r163 + Info tab「Bill chu kỳ => chỉ mua mới đc 1 lần - sau khi "
            "hết expired date => job bill (nếu muốn thành 1 sp mới để mua mới lại => sửa status_bill = 3)」."),

    # ══════ 19. Trang hoàn tất & 特商法 public ══════
    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Normal",
       "Trang 特定商取引法に基づく表記 hiển thị đúng nội dung đã nhập ở 各種設定",
       "- Đã nhập nội dung 特商法 ở tab 各種設定 →「事業者・特商法設定」của bot A",
       "1. F1 mở 商品ページ của SP\n2. Bấm vào text/link thông tin cửa hàng\n"
       "3. Đối chiếu nội dung với nội dung đã nhập ở màn admin",
       "Nội dung 特商法 có heading 事業者名 / 所在地 / 連絡先 …",
       "- Trang mở ra hiện ĐÚNG nội dung HTML đã nhập ở 各種設定 (giữ nguyên định dạng heading, list, link)\n"
       "- Trang này dùng chung cho MỌI sản phẩm của bot A",
       note="Nguồn: r278「nhấn vào text thì mở thông tin của hàng」+ r301 + r256. Spec SCR-BIL-25."),

    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Abnormal",
       "Bot CHƯA nhập nội dung 特商法 → trang public hiển thị thế nào",
       "- Bot B chưa từng nhập nội dung ở 各種設定 →「事業者・特商法設定」",
       "1. Friend mở 商品ページ của sản phẩm thuộc bot B\n2. Bấm vào link thông tin cửa hàng\n"
       "3. Quan sát trang trả về",
       "s_store_settings.info_store rỗng / chưa có bản ghi",
       "- Ghi lại kết quả THẬT: trang trống, trang lỗi hay có nội dung mặc định\n"
       "- Theo spec §2.3:「KHÔNG có bản ghi mặc định cấp hệ thống」→ dự kiến trang trống\n"
       "- KHÔNG được lỗi 500",
       note="Suy luận của AI từ spec §2.3 + §9.1 mục 15. Corpus KHÔNG có TC. Đây là điểm rủi ro pháp lý "
            "(特商法 bắt buộc theo luật) — xem MT-18."),

    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Normal",
       "Trang 最終確認 hiển thị đủ 6 mục 特商法 theo yêu cầu pháp luật",
       "- SP đã nhập nội dung「ご確認事項」ở wizard bước 3 gồm đủ mục ③〜⑥",
       "1. F1 mua sản phẩm tới trang 最終確認\n2. Đối chiếu nội dung hiển thị với yêu cầu 6 mục ①…⑥ "
       "của 改正特定商取引法\n3. Kiểm tra 2 mục ①② có tự động hiển thị không",
       "Nội dung ご確認事項 admin đã nhập",
       "- Mục ①② (thông tin sản phẩm, số tiền) tự động hiển thị từ dữ liệu đơn\n"
       "- Mục ③〜⑥ hiển thị đúng nội dung admin đã nhập ở wizard bước 3",
       note="Suy luận của AI từ spec §2.1 SCR-BIL-09 (khối cảnh báo pháp lý 改正特定商取引法 hiệu lực 2022-06-01). "
            "Corpus chỉ có r64 ở mức「user tự nhập text」. CẦN LEADER XÁC NHẬN danh sách 6 mục."),

    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Normal",
       "Sau mua thành công — option テキスト入力 → hiện trang nội dung đã nhập, nút xác nhận đúng nhãn",
       "- SP có flag_page_end = テキスト入力, đã nhập nội dung và nhãn nút ở wizard bước 4",
       "1. F1 mua sản phẩm thành công\n2. Quan sát trang sau khi thanh toán\n3. Bấm nút trên trang đó",
       "page_end_simple =「ご購入ありがとうございました」",
       "- Hiện trang có đúng nội dung đã nhập\n- Nút mang nhãn/màu đã setting\n"
       "- Bấm nút: quay về màn chat 1:1 của bot",
       note="Nguồn: r326 + r67. Spec BR-12 flag_page_end = 0."),

    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Normal",
       "Sau mua thành công — option 任意ページURL → redirect đúng URL, giữ được nội dung trang ngoài",
       "- SP có flag_page_end = URL với https://example.com/thanks",
       "1. F1 mua sản phẩm thành công\n2. Quan sát điều hướng sau khi thanh toán\n"
       "3. Kiểm tra có hiện cảnh báo「外部サイトに移動したため」không",
       "url_page_outsite_end = https://example.com/thanks",
       "- Chuyển sang đúng https://example.com/thanks\n"
       "- KHÔNG hiện message「外部サイトに移動したため」(sau đợt sửa domain — xem nhóm『Domain LIFF & redirect』)",
       env="PRODUCTION",
       note="Nguồn: r325 + Màn liên kết bill tiền r93「open item bill tiền => ko redirect sang domain khác nữa, "
            "ko hiển thị msg open ra trang ngoài」. regression"),

    tc("Trang hoàn tất & 特商法 public", "OUT-001", "Normal",
       "Sau mua thành công — option トーク画面に戻る → LIFF đóng, về màn chat 1:1",
       "- SP có flag_page_end = トーク画面に戻る",
       "1. F1 mua sản phẩm thành công trên LINE app\n2. Quan sát màn hình sau khi thanh toán",
       "flag_page_end = 2",
       "- LIFF đóng, quay về đúng màn chat 1:1 của bot A\n- Không hiện trang trung gian nào",
       note="Nguồn: r324 + r65 + Improve bill tiền univapay r293「Mua item success, redirect về màn talklist của line」."),

    tc("Trang hoàn tất & 特商法 public", "MSG-001", "Normal",
       "Sau mua thành công → action「申込完了時」và notify được gửi đúng 1 lần",
       "- SP đã gắn action ở slot「申込完了時」, 稼働回数 =「何度でも」",
       "1. F1 mua sản phẩm thành công\n2. Kiểm tra chat 1:1 của F1\n3. Kiểm tra notify phía admin\n"
       "4. Đếm số tin nhận được",
       "1 lần mua",
       "- F1 nhận ĐÚNG 1 lần nội dung action đã setting\n"
       "- Admin nhận notify「【tên Bot】<line name> <tên qly item> が購入されました」\n"
       "- Không có tin trùng lặp",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r5 + Improve bill tiền univapay r5 + test fix bug r48/r54."),

    tc("Trang hoàn tất & 特商法 public", "MSG-001", "Normal",
       "Sản phẩm thuộc テスト環境 → tin nhắn LINE có prefix cảnh báo thanh toán thử",
       "- SP-T thuộc テスト環境, có gắn action「申込完了時」",
       "1. F1 mua SP-T thành công bằng thẻ test\n2. Đọc tin nhắn F1 nhận được ở chat 1:1\n"
       "3. Lặp lại với sản phẩm 本番環境 SP-P",
       "SP-T: flag_environment = 0 · SP-P: flag_environment = 1",
       "- Tin của SP-T có prefix「【ご注意】これはテスト決済なので実際には課金されません」\n"
       "- Tin của SP-P KHÔNG có prefix này",
       env="PRODUCTION",
       note="Suy luận của AI từ spec §1.6 + BR-10. Corpus KHÔNG có TC kiểm prefix này. "
            "⚠ Spec R13 cảnh báo $textStart (prefix cảnh báo test) trong sendBillInfoMessage KHÔNG BAO GIỜ được dùng "
            "→ xem MT-19, khả năng cao TC này FAIL ở nhánh job bill."),
]
