# -*- coding: utf-8 -*-
"""FA-026 商品販売 — TC BỔ SUNG sau BƯỚC 7 (audit coverage).

Rà lại corpus phát hiện 3 khối chưa được phủ ở 6 file S1-S6:
  · Feature #30651 (24/02/2026) — thêm（税込）+ 2 cột 購入個数/決済金額 vào lịch sử + detail + CSV của 単品
  · Bug #28262 (15/02/2025) — thêm text khi nhiều friend thanh toán cùng item trong thời gian ngắn
  · Quản lý sản phẩm r378-r380 — authorize xác minh thẻ ở case trial 0円 và đổi thẻ (UnivaPay)
  · test fix bug r27-r28 — thứ tự ghi hàng đợi action so với lịch sử bill
"""
from _common import tc

HIS = "- Đăng nhập admin bot A, mở /basic/sales/index → tab「販売履歴」"
HIS1 = HIS + "\n- Đang ở sub-tab「単品商品」"
FR = "- Friend F1 đã kết bạn với bot A\n- SP là 単品商品 テスト環境, đã setting đủ 4 trang"
FRC = "- Friend F1 đã kết bạn với bot A\n- SP-C là 継続商品 テスト環境, đã setting đủ 5 trang"

S7 = [
    # ── Feature #30651 ────────────────────────────────────────────
    tc("Màn 販売履歴", "UI-001", "Normal",
       "★ Feature #30651 — cột 商品価格 của lịch sử 単品 có thêm chữ（税込）, lịch sử 継続 thì KHÔNG",
       HIS + "\n- Có ≥ 1 đơn 単品 và ≥ 1 hợp đồng 継続 ở CẢ 2 môi trường 本番 và テスト",
       "1. Mở 販売履歴 sub-tab 単品, môi trường 本番 → đọc tiêu đề cột giá\n"
       "2. Chuyển sang môi trường テスト → đọc lại\n"
       "3. Mở sub-tab 継続, môi trường 本番 → đọc tiêu đề cột giá\n4. Chuyển テスト → đọc lại",
       "2 sub-tab × 2 môi trường",
       "- Sub-tab 単品 (cả 本番 và テスト): tiêu đề cột là「商品価格（税込）」, giá trị = giá của 1 sản phẩm\n"
       "- Sub-tab 継続 (cả 本番 và テスト): KHÔNG có chữ（税込）",
       note="Nguồn: Quản lý sản phẩm r233-r236 (Feature #30651, 24/02/2026). "
            "⚠ Khác biệt 単品 / 継続 là CHỦ Ý theo task, không phải bug."),

    tc("Màn 販売履歴", "DATA-COUNT-001", "Normal",
       "★ Feature #30651 — lịch sử 単品 có thêm 2 cột 購入個数 và 決済金額; lịch sử 継続 KHÔNG có",
       HIS + "\n- Có đơn 単品 mua 3 sản phẩm, đơn giá 1.000円 (ở cả 本番 và テスト)\n- Có ≥ 1 hợp đồng 継続",
       "1. Mở 販売履歴 sub-tab 単品, môi trường 本番 → tìm 2 cột 購入個数 và 決済金額, đọc giá trị\n"
       "2. Tính tay: đơn giá × số lượng, đối chiếu với cột 決済金額\n"
       "3. Chuyển môi trường テスト → lặp lại\n4. Mở sub-tab 継続 (cả 2 môi trường) → kiểm 2 cột này",
       "Đơn giá 1.000円 × 3 sản phẩm = 3.000円",
       "- Sub-tab 単品 (cả 2 môi trường): có cột 購入個数 = 3 và cột 決済金額 = 3.000円 "
       "(= 1.000 × 3, khớp phép tính tay)\n"
       "- Sub-tab 継続 (cả 2 môi trường): KHÔNG có 2 cột này",
       note="Nguồn: Quản lý sản phẩm r237-r240 (Feature #30651)."),

    tc("Màn 販売履歴", "DATA-COUNT-001", "Normal",
       "★ Feature #30651 — màn 注文詳細 単品 cũng có 2 cột 購入個数 và 決済金額; 継続 KHÔNG có",
       HIS1 + "\n- Có đơn 単品 mua 3 sản phẩm, đơn giá 1.000円",
       "1. Mở 注文詳細 của đơn 単品 (môi trường 本番) → tìm 2 mục 購入個数 và 決済金額\n"
       "2. Đối chiếu với giá trị ở màn list\n3. Lặp lại ở môi trường テスト\n"
       "4. Mở 注文詳細 của hợp đồng 継続 (cả 2 môi trường) → kiểm 2 mục này",
       "Đơn giá 1.000円 × 3 = 3.000円",
       "- 注文詳細 単品 (cả 2 môi trường): 購入個数 = 3, 決済金額 = 3.000円, khớp với màn list\n"
       "- 注文詳細 継続 (cả 2 môi trường): KHÔNG có 2 mục này",
       note="Nguồn: Quản lý sản phẩm r241-r244 (Feature #30651)."),

    tc("Export CSV lịch sử", "OUT-001", "Normal",
       "★ Feature #30651 — file CSV của lịch sử 単品 có đủ 2 cột mới; CSV của 継続 KHÔNG có",
       HIS + "\n- Có đơn 単品 mua 3 sản phẩm đơn giá 1.000円 (ở cả 本番 và テスト)\n- Có ≥ 1 hợp đồng 継続",
       "1. Mở 販売履歴 sub-tab 単品 môi trường 本番 → bấm CSV書出し → mở file\n"
       "2. Tìm 2 cột 購入個数 và 決済金額, đối chiếu giá trị với màn hình\n"
       "3. Lặp lại ở môi trường テスト\n4. Export CSV ở sub-tab 継続 (cả 2 môi trường) → kiểm 2 cột này",
       "Đơn giá 1.000円 × 3 = 3.000円",
       "- CSV 単品 (cả 2 môi trường): có cột 購入個数 = 3 và 決済金額 = 3.000円, khớp với màn hình\n"
       "- CSV 継続 (cả 2 môi trường): KHÔNG có 2 cột này\n"
       "- Định dạng cột trong file khớp với bảng hiển thị bên ngoài",
       env="PRODUCTION",
       note="Nguồn: Quản lý sản phẩm r245-r248 (Feature #30651 — mục 4「Sửa export csv (bill 1 lần) vì đang "
            "format theo table bên ngoài list」). Liên quan MT-34 (chưa có danh sách cột chuẩn)."),

    # ── Bug #28262 ────────────────────────────────────────────────
    tc("LINE user — mua 単品", "MSG-002", "Normal",
       "★ Bug #28262 — nhiều friend thanh toán cùng 1 item trong thời gian ngắn → có text cảnh báo bổ sung",
       FR + "\n- SP là 単品商品, sẽ có nhiều friend thanh toán liên tiếp trong thời gian ngắn",
       "1. Cho 3 friend lần lượt mua cùng 1 SP 単品 trong vòng vài phút\n"
       "2. Với mỗi lần mua: quan sát TOÀN BỘ màn hình phía LINE (trang xác nhận, trang kết quả) "
       "tìm đoạn text cảnh báo mới được thêm\n"
       "3. Lặp lại với thẻ thường và thẻ 3D Secure (Stripe), rồi với cổng UnivaPay",
       "3 friend mua liên tiếp × (Stripe thẻ thường / Stripe 3DS / UnivaPay)",
       "- Cả 3 tổ hợp: mua thành công bình thường\n"
       "- Ghi lại VỊ TRÍ và NỘI DUNG CHÍNH XÁC của đoạn text cảnh báo được thêm theo Bug #28262\n"
       "- Text hiển thị giống nhau ở cả 3 tổ hợp",
       env="PRODUCTION",
       note="Nguồn: test fix bug r60-r63 (Bug #28262 [15-02-2025]:「Item: Có nhiều friend đã thanh toán cùng 1 "
            "item bill 1 lần nhiều lần trong thời gian ngắn ⇒ **Thêm text**」). TC gốc CHỈ CÓ TIÊU ĐỀ, "
            "KHÔNG ghi nội dung text — kết quả mong đợi để mở, CẦN LEADER XÁC NHẬN nội dung và vị trí text thật."),

    tc("LINE user — mua 継続", "MSG-002", "Normal",
       "★ Bug #28262 — text cảnh báo tương tự khi MUA MỚI và khi ĐỔI THẺ của item chu kỳ",
       FRC,
       "1. Cho 3 friend lần lượt mua mới cùng 1 SP-C trong thời gian ngắn → quan sát text cảnh báo\n"
       "2. Cho 3 friend lần lượt đổi thẻ (case có bill tiền luôn) trong thời gian ngắn → quan sát\n"
       "3. Lặp lại với thẻ thường và thẻ 3DS (Stripe), rồi với UnivaPay",
       "Mua mới × 3 tổ hợp thẻ/cổng · Đổi thẻ × 3 tổ hợp",
       "- Cả 6 tổ hợp: thao tác thành công bình thường\n"
       "- Text cảnh báo hiển thị giống với luồng 単品 (cùng nội dung, cùng vị trí)",
       env="PRODUCTION",
       note="Nguồn: test fix bug r64-r69 (Bug #28262). TC gốc chỉ có tiêu đề — CẦN LEADER XÁC NHẬN nội dung text."),

    # ── Authorize xác minh thẻ (UnivaPay) ─────────────────────────
    tc("LINE user — mua 継続", "PAY-001", "Normal",
       "Trial 0円 và đổi thẻ → thêm bước xác minh thẻ (authorize) với UnivaPay",
       FRC + "\n- SP-C dùng UnivaPay, có trial, KHÔNG set giá kỳ đầu (bill 0円)",
       "1. F1 mua SP-C → mở dashboard UnivaPay tra giao dịch của F1\n"
       "2. Đọc trạng thái giao dịch\n3. Sửa cho hết hạn trial → chạy job bill → tra lại UnivaPay\n"
       "4. F1 đổi thẻ → tra lại UnivaPay",
       "trial 0円, cổng UnivaPay",
       "- Bước 1-2: trên UnivaPay có giao dịch trạng thái Authorized (xác minh thẻ, KHÔNG trừ tiền)\n"
       "- Bước 3: sau khi hết trial, job bill tạo giao dịch trừ tiền thật\n"
       "- Bước 4: đổi thẻ cũng tạo giao dịch Authorized để xác minh thẻ mới",
       env="PRODUCTION",
       note="Nguồn: Quản lý sản phẩm r378-r380「khi bill là trial + không thanh toán và khi change card sẽ thêm "
            "authorize để univapay xác minh」+ r390. Liên quan Bug Tester #38077 (Authorized = thành công)."),

    # ── Thứ tự ghi hàng đợi action ────────────────────────────────
    tc("Action & notify theo sự kiện", "FUNC-SEQ-001", "Normal",
       "Thứ tự ghi nhận — bản ghi hàng đợi action được tạo SAU bản ghi lịch sử bill",
       "- SP-C có trial giá 500円, giá thật 1.000円, đã gắn action có chèn mã số tiền\n"
       "- F1 có hợp đồng đang trial",
       "1. Cho F1 bill qua giao diện (web) → đọc số tiền trong tin action nhận được\n"
       "2. Sửa cho hết hạn trial → chạy job bill → đọc số tiền trong tin action nhận được\n"
       "3. Với cả 2 lần: đối chiếu số tiền trong tin với dòng tương ứng ở bảng 決済履歴",
       "trial 500円 → bill thật 1.000円",
       "- Cả 2 luồng (bill từ web và bill từ job): tin action hiển thị số tiền = 1.000円 khi bill thật\n"
       "- Số tiền trong tin KHỚP với dòng lịch sử tương ứng (không bị lệch do thứ tự ghi)",
       env="PRODUCTION",
       note="Nguồn: test fix bug r27-r28 (Bug #26568) — tester ghi rõ「action line user sẽ insert SAU tbl "
            "s_order_history」, tức thứ tự ghi quyết định giá trị mã chèn có đúng hay không. "
            "Chuỗi thao tác liên tiếp không tách rời → giữ chung 1 TC."),
]
