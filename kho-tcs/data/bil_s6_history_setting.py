# -*- coding: utf-8 -*-
"""FA-026 商品販売 — Nhóm 26-34: Lịch sử · Hoàn tiền · CSV · Thuế · 各種設定 · Liên kết cổng · Domain · Phân quyền.

Nguồn chính: 12. TCsLine_Item / tab「Quản lý sản phẩm」r179-r231 + r370-r373,
             tab「Màn liên kết bill tiền」(Bug #32455/#32370 ẩn app ID · Bug #32535 webhook domain ·
             Support #32786 domain s.lmes.jp, 06/2024 → 01/2026 — tab master của màn liên kết),
             tab「test fix bug」r299-r368 (Bug #32729 export CSV ký tự đặc biệt, 11/2025),
             tab「Test invoice (stripe)」(thuế + hóa đơn),
             tab「improve bill tiền 3D secure」r61-r67 (refund).
"""
from _common import tc

HIS = "- Đăng nhập admin bot A, mở /basic/sales/index → tab「販売履歴」"
HIS1 = HIS + "\n- Đang ở sub-tab「単品商品」"
HIS2 = HIS + "\n- Đang ở sub-tab「継続商品」"
SET = "- Đăng nhập admin bot A, mở /basic/sales/index → tab「各種設定」"

S6 = [
    # ══════ 26. Màn 販売履歴 ══════
    tc("Màn 販売履歴", "UI-001", "Normal",
       "List 販売履歴 単品 hiển thị đủ 7 cột và nút mở chi tiết",
       HIS1 + "\n- Có ≥ 1 đơn 単品 決済成功 trong 30 ngày gần nhất",
       "1. Mở tab 販売履歴 sub-tab 単品\n2. Đối chiếu từng cột với 注文詳細 của đơn đó",
       "1 đơn 単品 của friend F1",
       "- Hiện đủ: ngày giờ bill · ảnh + tên user mua · 注文番号 · tên sản phẩm · số tiền · "
       "決済システム · 決済ステータス\n- Nút mở chi tiết mở đúng màn 注文詳細 của đơn đó",
       note="Nguồn: Quản lý sản phẩm r179-r187."),

    tc("Màn 販売履歴", "UI-001", "Normal",
       "List 販売履歴 継続 hiển thị đủ cột và các trạng thái hợp đồng",
       HIS2 + "\n- Có ≥ 4 hợp đồng ở các trạng thái khác nhau",
       "1. Mở sub-tab 継続\n2. Đối chiếu các cột\n3. Đọc cột trạng thái của từng hợp đồng",
       "4 hợp đồng: 継続中 · トライアル中 · bill lỗi · キャンセル済",
       "- Hiện đủ: ngày giờ · user mua · 注文番号 · tên sản phẩm · số tiền · 決済システム · trạng thái\n"
       "- 4 trạng thái hiển thị đúng và phân biệt được\n- Nút mở chi tiết mở đúng 注文詳細 継続",
       note="Nguồn: r205-r213 + r223-r226."),

    tc("Màn 販売履歴", "DATA-001", "Normal",
       "★ 注文番号 của 単品 và của 継続 là 2 DÃY SỐ RIÊNG BIỆT",
       HIS + "\n- Có ít nhất 1 đơn 単品 và 1 hợp đồng 継続",
       "1. Mở sub-tab 単品, ghi lại 注文番号 của đơn mới nhất\n"
       "2. Mở sub-tab 継続, ghi lại 注文番号 của hợp đồng mới nhất\n"
       "3. Mở 注文詳細 của hợp đồng 継続, ghi lại 注文番号 của từng KỲ trong bảng 決済履歴\n"
       "4. So sánh 3 dãy số",
       "3 loại số: đơn 単品 · hợp đồng 継続 · kỳ của hợp đồng",
       "- 注文番号 của HỢP ĐỒNG 継続 thuộc dãy số RIÊNG (thường nhỏ hơn nhiều)\n"
       "- 注文番号 của từng KỲ trong 決済履歴 lại thuộc CÙNG dãy với đơn 単品\n"
       "- 2 dãy có thể trùng con số nhưng là 2 đối tượng khác nhau",
       note="Suy luận của AI từ spec §1.4 + Field Matrix #47/#48. Corpus KHÔNG có TC. "
            "Đây là điểm dễ nhầm khi đối soát với kế toán — CẦN LEADER XÁC NHẬN."),

    tc("Màn 販売履歴", "ENV-001", "Normal",
       "Filter môi trường 本番 / テスト ở 販売履歴 → chỉ hiện đơn thuộc môi trường tương ứng",
       HIS1 + "\n- Có đơn của cả sản phẩm 本番 và sản phẩm テスト",
       "1. Chọn filter môi trường「本番」→ đếm số đơn và kiểm tra tên sản phẩm\n"
       "2. Chọn「テスト」→ đếm số đơn\n3. Lặp lại ở sub-tab 継続",
       "Đơn của cả 2 môi trường",
       "- Filter 本番: chỉ hiện đơn của sản phẩm 本番\n- Filter テスト: chỉ hiện đơn của sản phẩm テスト\n"
       "- Không lẫn giữa 2 môi trường ở cả 2 sub-tab",
       note="Nguồn: r188-r189 + r214-r215."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Filter theo KHOẢNG NGÀY bill; mặc định 30 ngày gần nhất",
       HIS1 + "\n- Có đơn ở nhiều mốc thời gian: trong 30 ngày, 45 ngày trước, 90 ngày trước",
       "1. Mở tab 販売履歴 lần đầu → quan sát khoảng ngày mặc định và số đơn hiển thị\n"
       "2. Đổi khoảng ngày phủ cả 90 ngày → đếm lại\n3. Đặt khoảng ngày chỉ chứa 1 ngày có đơn → đếm",
       "Đơn ở 3 mốc: 10 ngày · 45 ngày · 90 ngày trước",
       "- Mặc định: khoảng 30 ngày gần nhất, chỉ hiện đơn trong 30 ngày\n"
       "- Mở rộng khoảng: hiện thêm đơn 45 và 90 ngày trước\n- Thu hẹp: chỉ hiện đơn đúng ngày đó",
       note="Nguồn: r190 + r216 (TC gốc chỉ có tiêu đề「filter theo ngày bill」). Mặc định 30 ngày lấy từ "
            "spec §2.2. ⚠ Spec Field Matrix #46: cột hiển thị là created_at nhưng LỌC lại theo payment_date "
            "(単品) → xem MT-30."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Search theo tên user mua (cả LINE name và system name) và theo tên sản phẩm",
       HIS1 + "\n- F1 có LINE name「Taro」và system name「山田太郎」, có đơn của SP「テスト単品」",
       "1. Nhập「Taro」vào ô tìm kiếm → đếm kết quả\n2. Nhập「山田太郎」→ đếm kết quả\n"
       "3. Nhập「テスト単品」→ đếm kết quả\n4. Nhập chuỗi không tồn tại → quan sát",
       "「Taro」·「山田太郎」·「テスト単品」· chuỗi không tồn tại",
       "- Cả 3 từ khóa hợp lệ đều tìm ra đơn của F1\n"
       "- Chuỗi không tồn tại: hiện danh sách rỗng, không lỗi",
       note="Nguồn: r191-r192 + r217-r218. Spec §2.2: khớp 4 trường LIKE (line_user.name, view_name, "
            "s_items.name, id đơn)."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Modal 絞り込み — lọc theo SẢN PHẨM cụ thể",
       HIS1 + "\n- Có đơn của ≥ 2 sản phẩm khác nhau",
       "1. Mở modal「絞り込み」\n2. Ở khối 商品選択 chọn 1 sản phẩm → bấm 決定\n3. Đếm và đối chiếu kết quả",
       "2 sản phẩm có đơn, chọn 1",
       "- Chỉ hiện đơn của sản phẩm đã chọn\n- Không lẫn đơn của sản phẩm khác",
       note="Nguồn: r193 + r219. ⚠ Spec §2.2 bước 2: danh sách folder trong modal sắp xếp KHÁC panel sidebar và "
            "KHÔNG lọc type_payment → xem MT-31."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Modal 絞り込み — lọc theo 決済システム (全て / Stripe / UnivaPay)",
       HIS1 + "\n- Có đơn của cả 2 cổng thanh toán",
       "1. Mở modal, chọn 全て → đếm\n2. Chọn Stripe → đếm + đối chiếu cột 決済システム\n"
       "3. Chọn UnivaPay → đếm + đối chiếu",
       "Đơn của cả Stripe và UnivaPay",
       "- 全て: hiện tất cả\n- Stripe: chỉ đơn Stripe\n- UnivaPay: chỉ đơn UnivaPay",
       note="Nguồn: r194-r196 + r220-r222."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Modal 絞り込み 単品 — lọc theo 決済ステータス (全て / 決済成功 / 返金済み)",
       HIS1 + "\n- Có 2 đơn 決済成功 và 1 đơn 返金済み",
       "1. Mở modal, chọn 全て → đếm\n2. Chọn 決済成功 → đếm\n3. Chọn 返金済み → đếm",
       "2 đơn thành công · 1 đơn hoàn tiền",
       "- 全て: 3 đơn\n- 決済成功: 2 đơn\n- 返金済み: 1 đơn",
       note="Nguồn: r197-r199. Spec SCR-BIL-17 xác nhận chỉ có 3 lựa chọn này cho 単品."),

    tc("Màn 販売履歴", "FUNC-FILTER-001", "Normal",
       "Modal 絞り込み 継続 — lọc theo trạng thái hợp đồng (継続中 / トライアル中 / bill lỗi / キャンセル済)",
       HIS2 + "\n- Có 4 hợp đồng ở 4 trạng thái khác nhau",
       "1. Mở modal, lần lượt chọn từng trạng thái → đếm kết quả mỗi lần",
       "4 hợp đồng, mỗi trạng thái 1 hợp đồng",
       "- Mỗi lựa chọn trả về đúng 1 hợp đồng tương ứng, không lẫn trạng thái khác",
       note="Nguồn: r223-r226. ⚠ Spec §9.1 mục 8 nói「KHÔNG có badge 決済エラー」→ nhãn của hợp đồng bill lỗi "
            "cần đối chiếu thực tế, xem MT-09."),

    tc("Màn 販売履歴", "UI-002", "Normal",
       "Badge 決済ステータス là LINK mở dashboard cổng thanh toán đúng giao dịch",
       HIS1 + "\n- Có 1 đơn 単品 UnivaPay và 1 hợp đồng 継続 UnivaPay",
       "1. Ở list 単品 bấm badge 決済ステータス của đơn → quan sát trang mở ra\n"
       "2. Ở list 継続 bấm badge của hợp đồng → quan sát trang mở ra",
       "1 đơn 単品 · 1 hợp đồng 継続",
       "- 単品: mở trang giao dịch (charge) tương ứng trên dashboard UnivaPay\n"
       "- 継続: mở trang recurring token tương ứng trên dashboard UnivaPay\n"
       "- Cả 2 đều mở đúng bản ghi của đơn đang xem, không phải trang danh sách chung",
       note="Suy luận của AI từ spec §2.2「Badge 決済ステータス là hyperlink ra dashboard cổng thanh toán」. "
            "Corpus chỉ có TC tương đương ở improve bill tiền 3D secure r57-r58 (phía Stripe). CẦN LEADER XÁC NHẬN."),

    tc("Màn 販売履歴", "UI-001", "Normal",
       "注文詳細 単品 hiển thị đủ thông tin đơn + thông tin user + khối 友だち情報 đúng thứ tự",
       HIS1 + "\n- Đơn của F1 có 5 mục 友だち情報 đã nhập, thứ tự setting: A → B → C → D → E",
       "1. Mở 注文詳細 của đơn\n2. Đối chiếu thông tin đơn, thông tin user\n"
       "3. Đối chiếu THỨ TỰ 5 mục trong khối 友だち情報 với thứ tự setting ở wizard bước 2",
       "5 mục theo thứ tự A → B → C → D → E",
       "- Hiện đủ thông tin đơn (số tiền, ngày, sản phẩm, thẻ) và thông tin user\n"
       "- Khối 友だち情報 hiện đúng 5 giá trị theo ĐÚNG thứ tự setting",
       note="Nguồn: r200-r201. Spec SCR-BIL-18: khối 友だち情報 render từ JSON và được sắp xếp lại theo "
            "b_c_info_setting.order_index."),

    tc("Màn 販売履歴", "UI-001", "Normal",
       "注文詳細 継続 hiển thị bảng 決済履歴 đủ 6 cột theo từng kỳ",
       HIS2 + "\n- Hợp đồng của F1 đã bill 3 kỳ",
       "1. Mở 注文詳細 của hợp đồng\n2. Đọc bảng 決済履歴: đếm số dòng và các cột\n"
       "3. Đối chiếu 決済回数 với số kỳ đã bill thật",
       "3 kỳ đã bill",
       "- Bảng có 3 dòng\n- Mỗi dòng có: 決済回数 · 請求日 · 決済日 · 注文番号 · 決済額(税込) · ステータス\n"
       "- 決済回数 chạy 1, 2, 3",
       note="Nguồn: r227-r229. ⚠ Spec Field Matrix #58 + R-L2: 決済回数 KHÔNG có cột DB, chỉ là chỉ số dòng → "
            "nếu 1 kỳ lỗi sinh nhiều bản ghi thì con số này KHÔNG phản ánh số kỳ thật, xem MT-32."),

    tc("Màn 販売履歴", "DATA-COUNT-001", "Abnormal",
       "★ 決済回数 khi hợp đồng có kỳ LỖI xen giữa → số hiển thị có còn đúng không",
       HIS2 + "\n- Hợp đồng của F1: kỳ 1 thành công · kỳ 2 LỖI · kỳ 3 thành công",
       "1. Mở 注文詳細 của hợp đồng\n2. Đọc cột 決済回数 của 3 dòng trong 決済履歴\n"
       "3. Đối chiếu với SỐ KỲ ĐÃ THANH TOÁN THÀNH CÔNG thật (2 kỳ)",
       "3 dòng lịch sử, 2 kỳ thành công",
       "- Ghi lại giá trị THẬT của cột 決済回数 ở 3 dòng\n"
       "- Theo spec: cột này là chỉ số dòng nên sẽ hiện 1, 2, 3 — KHÔNG phản ánh 2 kỳ thanh toán thành công\n"
       "- Nếu vậy thì admin dễ hiểu nhầm số kỳ đã thu tiền → cần raise",
       note="Suy luận của AI từ spec Field Matrix #58. Corpus KHÔNG có TC. Đây là MT-32 — CẦN LEADER QUYẾT."),

    tc("Màn 販売履歴", "DATA-001", "Normal",
       "販売価格 của hợp đồng ĐANG CHẠY hiển thị giá HIỆN TẠI, hợp đồng đã kết thúc hiển thị giá snapshot",
       HIS2 + "\n- Hợp đồng H1 đang 継続中 (đăng ký khi giá 3.000円)\n"
       "- Hợp đồng H2 đã キャンセル済 (đăng ký khi giá 3.000円)",
       "1. Đổi giá sản phẩm thành 5.000円 → 保存\n"
       "2. Mở 販売履歴 継続 đọc cột 販売価格 của H1 và H2\n3. Mở 注文詳細 từng hợp đồng đối chiếu",
       "Giá cũ 3.000円 → giá mới 5.000円",
       "- H1 (đang chạy): hiển thị 5.000円 (giá hiện tại)\n"
       "- H2 (đã kết thúc): hiển thị 3.000円 (giá lúc đăng ký)",
       note="Suy luận của AI từ spec Field Matrix #53「status_bill == 1 ? s_items.amount : "
            "s_cycle_order_history.amount_item」. Corpus KHÔNG có TC. Liên quan MT-03 — CẦN LEADER XÁC NHẬN."),

    tc("Màn 販売履歴", "LIST-001", "Boundary",
       "販売履歴 rỗng (bot chưa có đơn nào) → hiện empty state, không lỗi",
       "- Bot mới chưa có đơn hàng nào",
       "1. Mở tab 販売履歴 sub-tab 単品\n2. Mở sub-tab 継続\n3. Thử export CSV",
       "0 đơn",
       "- Cả 2 sub-tab hiện trạng thái rỗng, không lỗi JS/500\n"
       "- Export CSV: hoặc bị chặn với thông báo, hoặc tải về file chỉ có dòng tiêu đề — không lỗi",
       note="Suy luận của AI — corpus không có TC empty state. CẦN LEADER XÁC NHẬN hành vi export khi rỗng."),

    tc("Màn 販売履歴", "LIST-002", "Normal",
       "Phân trang 販売履歴 20 dòng/trang",
       HIS1 + "\n- Có ≥ 25 đơn 単品 trong khoảng ngày đang lọc",
       "1. Đếm số dòng trang 1\n2. Sang trang 2, đếm số dòng và kiểm tra không trùng 注文番号\n"
       "3. Đổi bộ lọc rồi quay lại → kiểm tra về trang 1",
       "25 đơn",
       "- Trang 1: 20 dòng\n- Trang 2: 5 dòng, không trùng với trang 1\n"
       "- Sau khi đổi bộ lọc: quay về trang 1",
       note="Suy luận của AI từ spec §2.2 (phân trang 20/trang). Corpus có r94/r178 cho màn detail. "
            "CẦN LEADER XÁC NHẬN."),

    # ══════ 27. Hoàn tiền & hủy phía admin ══════
    tc("Hoàn tiền & hủy phía admin", "PAY-003", "Normal",
       "Hoàn tiền — chọn「thực hiện trả tiền tự động」→ gọi API hoàn tiền, đơn chuyển 返金済み",
       HIS1 + "\n- Có đơn 単品 決済成功 của F1, cổng Stripe, số tiền 1.000円",
       "1. Mở 注文詳細 của đơn → bấm「返金する」\n2. Ở màn xác nhận chọn phương án trả tiền tự động → xác nhận\n"
       "3. Đọc lại trạng thái đơn ở 販売履歴 và 注文詳細\n4. Mở dashboard Stripe tra giao dịch\n"
       "5. Xem cột 販売数 và số liệu thống kê của sản phẩm",
       "Đơn 1.000円 Stripe",
       "- Đơn chuyển badge「返金済み」, có ngày hoàn tiền\n"
       "- Trên Stripe: giao dịch chuyển trạng thái refunded\n"
       "- Số liệu doanh số của sản phẩm giảm tương ứng, số lượt hoàn tiền tăng 1",
       env="PRODUCTION",
       note="Nguồn: r202-r203 + improve bill tiền 3D secure r61 option 1. "
            "⚠ Spec R9: cập nhật thống kê tháng khi refund ĐÃ COMMENT OUT ở V2 → xem MT-33."),

    tc("Hoàn tiền & hủy phía admin", "PAY-003", "Normal",
       "Hoàn tiền — chọn「chỉ đổi trạng thái nội bộ」→ KHÔNG gọi API cổng, đơn vẫn chuyển 返金済み",
       HIS1 + "\n- Có đơn 単品 決済成功 của F1, cổng Stripe",
       "1. Mở 注文詳細 → bấm「返金する」\n2. Chọn phương án chỉ đổi trạng thái nội bộ → xác nhận\n"
       "3. Đọc lại trạng thái đơn\n4. Mở dashboard Stripe tra giao dịch",
       "Đơn 1.000円 Stripe",
       "- Đơn bên LME chuyển「返金済み」\n"
       "- Trên Stripe: giao dịch VẪN ở trạng thái thành công (KHÔNG bị hoàn tiền)",
       env="PRODUCTION",
       note="Nguồn: r204 + improve bill tiền 3D secure r62 option 2."),

    tc("Hoàn tiền & hủy phía admin", "PAY-003", "Normal",
       "Hoàn tiền đơn theo cơ chế thanh toán CŨ và MỚI đều thành công (Bug #29752)",
       HIS + "\n- Có 4 đơn: 2 đơn cơ chế cũ (1 đơn 単品 + 1 kỳ của hợp đồng), 2 đơn cơ chế mới",
       "1. Hoàn tiền từng đơn một, quan sát kết quả\n2. Với mỗi đơn: đối chiếu dashboard cổng thanh toán\n"
       "3. Tick chọn NHIỀU đơn cùng lúc (trộn cả cũ và mới) → bấm 一括返金実行\n"
       "4. Đọc lại trạng thái từng đơn",
       "2 đơn cơ chế cũ + 2 đơn cơ chế mới",
       "- Cả 4 đơn đều hoàn tiền THÀNH CÔNG, không hiện thông báo lỗi\n"
       "- Hoàn tiền hàng loạt trộn cũ/mới: tất cả đều chuyển 返金済み\n"
       "- Dashboard cổng thanh toán ghi nhận đúng",
       env="PRODUCTION",
       note="Nguồn: test fix bug r82-r89 (Bug #29752「Item: Hiển thị thông báo lỗi khi hoàn tiền」— nguyên nhân: "
            "bỏ cơ chế bill cũ chuyển sang payment intent nhưng vẫn lưu payment_new = 0). regression"),

    tc("Hoàn tiền & hủy phía admin", "PAY-003", "Normal",
       "Hoàn tiền đơn UnivaPay — cả cơ chế cũ và mới",
       HIS1 + "\n- Có đơn 単品 UnivaPay 決済成功",
       "1. Mở 注文詳細 → bấm「返金する」→ chọn trả tiền tự động → xác nhận\n"
       "2. Đọc lại trạng thái đơn\n3. Mở dashboard UnivaPay tra giao dịch\n"
       "4. Lặp lại với phương án chỉ đổi trạng thái nội bộ",
       "Đơn UnivaPay",
       "- Phương án tự động: đơn 返金済み và giao dịch trên UnivaPay chuyển refunded\n"
       "- Phương án nội bộ: đơn 返金済み nhưng giao dịch trên UnivaPay giữ nguyên",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r65-r67 (tester ghi「case cũ: do ko có bill card có thể refund」— "
            "nghĩa là case cơ chế cũ của UnivaPay CHƯA test được, cần chuẩn bị data)."),

    tc("Hoàn tiền & hủy phía admin", "STATE-001", "Abnormal",
       "Không cho hoàn tiền đơn đang chờ xử lý thanh toán",
       HIS1 + "\n- Có đơn ở trạng thái「決済処理中」(status_webhook ∈ {0,3,4})",
       "1. Mở 注文詳細 của đơn → kiểm tra nút「返金する」\n"
       "2. Quay ra list, tick chọn đơn này cùng 1 đơn hợp lệ → bấm 一括返金実行\n"
       "3. Đọc lại trạng thái 2 đơn",
       "1 đơn đang xử lý + 1 đơn hợp lệ",
       "- Màn 注文詳細: nút「返金する」bị ẨN\n"
       "- 一括返金実行: chỉ hoàn tiền đơn hợp lệ, BỎ QUA đơn đang xử lý\n"
       "- Nếu ép gọi refund đơn đang xử lý → lỗi「決済処理を行っていますので、操作できません。」",
       note="Nguồn: Improve bill tiền univapay r27-r29 + ListBug r24. Spec BR-14."),

    tc("Hoàn tiền & hủy phía admin", "FUNC-001", "Normal",
       "Admin hủy 1 hợp đồng — có tùy chọn CÓ / KHÔNG thực hiện action",
       HIS2 + "\n- SP-C đã gắn action ở slot「解約時」\n- Có 2 hợp đồng H1, H2 đang 継続中 của 2 friend",
       "1. Mở 注文詳細 H1 → bấm hủy hợp đồng → chọn CÓ thực hiện action → xác nhận\n"
       "2. Kiểm tra chat 1:1 của friend H1\n"
       "3. Mở 注文詳細 H2 → bấm hủy → chọn KHÔNG thực hiện action → xác nhận\n"
       "4. Kiểm tra chat 1:1 của friend H2",
       "H1: có action · H2: không action",
       "- Cả H1 và H2 đều chuyển trạng thái「キャンセル済」\n"
       "- Friend H1 NHẬN action「解約時」\n- Friend H2 KHÔNG nhận action nào",
       env="PRODUCTION",
       note="Nguồn: r230「Hiện comfirm hủy (có thực hiện action hay không)」+ r408."),

    tc("Hoàn tiền & hủy phía admin", "BULK-001", "Normal",
       "一括解約実行 — hủy nhiều hợp đồng cùng lúc cho cả Stripe và UnivaPay",
       HIS2 + "\n- Có 4 hợp đồng đang 継続中: 2 dùng Stripe, 2 dùng UnivaPay",
       "1. Tick chọn cả 4 hợp đồng → bấm「一括解約実行」→ xác nhận\n"
       "2. Đọc lại trạng thái 4 hợp đồng\n3. Kiểm tra chat 1:1 của 4 friend\n"
       "4. Kiểm tra dashboard cả Stripe và UnivaPay",
       "4 hợp đồng, 2 cổng",
       "- Cả 4 hợp đồng chuyển「キャンセル済」\n- 4 friend nhận action「解約時」(nếu chọn có action)\n"
       "- Kiểm tra trên cổng thanh toán: subscription/recurring token của cả 4 phải ở trạng thái đã hủy",
       env="PRODUCTION",
       note="Nguồn: r370-r373「hủy từng hợp đồng và nhiều hợp đồng của cả stripe và univapay」. "
            "⚠ Spec R32: thao tác hàng loạt LUÔN trả success dù từng đơn lỗi → xem MT-21. "
            "⚠ Spec R10: có thể không hủy subscription bên cổng → xem MT-17."),

    tc("Hoàn tiền & hủy phía admin", "DATA-COUNT-001", "Normal",
       "Sau khi admin hủy hợp đồng → các bộ đếm của sản phẩm cập nhật đúng",
       HIS2 + "\n- SP-C có 3 hợp đồng: 1 đang トライアル中, 2 đang 継続中",
       "1. Ghi lại cột「トライアル中」và「継続中」của SP-C ở list sản phẩm\n"
       "2. Hủy hợp đồng đang トライアル中\n3. Đọc lại 2 cột\n"
       "4. Hủy 1 hợp đồng đang 継続中\n5. Đọc lại 2 cột",
       "1 trial + 2 継続中",
       "- Sau bước 2: cột「トライアル中」giảm 1\n- Sau bước 4: cột「継続中」giảm 1\n"
       "- Không cột nào bị âm hoặc sai lệch",
       env="PRODUCTION",
       note="Suy luận của AI từ spec §2.5 + BR-09 (hủy trong trial → number_trial −1, number_cancel +1). "
            "Corpus KHÔNG có TC đếm. CẦN LEADER XÁC NHẬN."),

    tc("Hoàn tiền & hủy phía admin", "PAY-003", "Normal",
       "Hoàn tiền 1 KỲ của hợp đồng 継続 (khác với hủy cả hợp đồng)",
       HIS2 + "\n- Hợp đồng của F1 đã bill 3 kỳ thành công",
       "1. Mở 注文詳細 của hợp đồng → ở bảng 決済履歴 chọn kỳ thứ 2 → bấm hoàn tiền\n"
       "2. Đọc lại trạng thái kỳ 2 và trạng thái HỢP ĐỒNG\n3. Đối chiếu dashboard cổng thanh toán\n"
       "4. Chạy job bill kỳ tiếp → kiểm tra hợp đồng vẫn bill bình thường",
       "3 kỳ, hoàn tiền kỳ 2",
       "- Kỳ 2 chuyển「返金済み」\n- HỢP ĐỒNG vẫn ở trạng thái「継続中」(không bị hủy)\n"
       "- Cổng thanh toán ghi nhận hoàn tiền đúng 1 giao dịch\n- Kỳ tiếp vẫn bill bình thường",
       env="PRODUCTION",
       note="Nguồn: r231「Nhấn hoàn tiền => Ra màn comfirm hoàn tiền giống bill 1 lần」+ r409. "
            "Bước 4 là suy luận của AI — CẦN LEADER XÁC NHẬN."),

    # ══════ 28. Export CSV lịch sử ══════
    tc("Export CSV lịch sử", "OUT-001", "Normal",
       "Export CSV 販売履歴 単品 → file tải về đúng định dạng tên và đủ dữ liệu đang lọc",
       HIS1 + "\n- Có 5 đơn 単品 trong khoảng ngày đang lọc",
       "1. Bấm「CSV書出し」\n2. Mở file tải về\n3. Đối chiếu số dòng và nội dung với bảng đang hiển thị\n"
       "4. Kiểm tra tên file",
       "5 đơn 単品",
       "- File tải về không lỗi\n- Đủ 5 dòng dữ liệu, nội dung khớp bảng\n"
       "- Tên file theo định dạng「単品商品販売履歴_<tên bot>_<ngày giờ>.csv」",
       env="PRODUCTION",
       note="Nguồn: test fix bug r301 + spec §9.2 mục 16 (định dạng tên file). "
            "⚠ Spec §9.2 mục 16: danh sách cột CSV chưa được liệt kê đầy đủ trong spec → xem MT-34."),

    tc("Export CSV lịch sử", "OUT-001", "Normal",
       "Export CSV 販売履歴 継続 → tên file dùng tiền tố 継続商品販売履歴",
       HIS2 + "\n- Có 3 hợp đồng trong khoảng ngày đang lọc",
       "1. Bấm「CSV書出し」\n2. Mở file và kiểm tra tên file + số dòng",
       "3 hợp đồng",
       "- Tên file theo định dạng「継続商品販売履歴_<tên bot>_<ngày giờ>.csv」\n"
       "- Đủ 3 dòng dữ liệu",
       env="PRODUCTION",
       note="Nguồn: test fix bug r321 + spec §9.2 mục 16."),

    tc("Export CSV lịch sử", "OUT-002", "Normal",
       "★ Bug #32729 — tên bot chứa ký tự cấm của hệ điều hành → tự thay thế, export không lỗi",
       "- Chuẩn bị bot có tên chứa lần lượt các ký tự: / · * · \\ · : · ?\n- Bot có ≥ 1 đơn 単品",
       "1. Với mỗi ký tự: đổi tên bot → mở 販売履歴 単品 → bấm CSV書出し\n"
       "2. Quan sát có bị lỗi / chuyển màn 404 không\n3. Kiểm tra tên file tải về",
       "Tên bot chứa: / · * · \\ · : · ?",
       "- Cả 5 trường hợp: export THÀNH CÔNG, KHÔNG bị chuyển sang màn 404\n"
       "- Ký tự cấm được tự động thay bằng ký tự hợp lệ (- hoặc _)\n- File mở được bình thường",
       env="PRODUCTION",
       note="Nguồn: test fix bug r300-r305 (Bug #32729 — case KH: tên bot「安井百合子/隠さないで魅せよう」có ký tự / "
            "làm export bị lỗi chuyển màn 404). 5 ký tự cùng 1 kết quả → giữ chung 1 TC. regression"),

    tc("Export CSV lịch sử", "OUT-002", "Normal",
       "Tên bot chứa ký tự đặc biệt latinh → export thành công, một số ký tự giữ nguyên",
       "- Bot có tên chứa ` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [ ] | . ,",
       "1. Đổi tên bot thành chuỗi chứa các ký tự trên\n2. Export CSV ở cả 2 sub-tab\n"
       "3. Kiểm tra tên file và nội dung file",
       "Tên bot chứa ` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [ ] | . ,",
       "- Export thành công, file không lỗi\n"
       "- Một số ký tự được thay bằng - hoặc _, một số ký tự giữ nguyên trong tên file",
       env="PRODUCTION",
       note="Nguồn: test fix bug r306 + r324."),

    tc("Export CSV lịch sử", "OUT-002", "Normal",
       "Tên bot tiếng Nhật (hiragana/katakana/kanji/ký tự đặc biệt JP/emoji) → tên file hiển thị đúng",
       "- Chuẩn bị bot có các tên như liệt kê ở cột Dữ liệu test\n- Bot có đơn ở cả 2 sub-tab",
       "1. Với mỗi tên bot: export CSV ở sub-tab 単品 và 継続\n"
       "2. Đọc tên file tải về, kiểm tra có mojibake không\n3. Mở file kiểm tra nội dung",
       "まことボット智恵助 · チャット・ボットーさん · 【テスト】（木）〜！＠＃＄％＾＆＊ · ■FLOA Japan. · "
       "∞TO.KI.YO∞ · 《Teoria -ﾃｵﾘｱ-》 · AIボット🤖_Ver1 · こーだい/プレゼント専用🎁 · infinity NAO 🦁 · "
       "戸張賢治🏀&🍻 · 『WCL』坂本よしたか · ｻﾎﾟ24#NMM(4/25~) · 💎ｱｲﾘｽﾄ/ayuri💎 · Yuta&Tamon🔥🔥",
       "- Tất cả các tên: export thành công\n"
       "- Tên file hiển thị đúng tiếng Nhật/emoji, không mojibake\n"
       "- Ký tự / được thay bằng -",
       env="PRODUCTION",
       note="Nguồn: test fix bug r307-r316 (単品) + r325-r331 (継続). 14 input cùng 1 kết quả → giữ chung 1 TC."),

    tc("Export CSV lịch sử", "OUT-002", "Normal",
       "Tên bot tiếng Việt có dấu và tên bot RẤT DÀI → export không lỗi",
       "- Bot 1: tên tiếng Việt có dấu\n- Bot 2: tên dài「スーパーインテリジェントチャットボットのマコトさん"
       "ですよろしくお願いします」",
       "1. Export CSV ở cả 2 sub-tab cho từng bot\n2. Kiểm tra tên file và mở file",
       "Tên tiếng Việt có dấu · tên dài (~40 ký tự JP)",
       "- Cả 2 trường hợp: export không lỗi, file lưu đúng, mở được",
       env="PRODUCTION",
       note="Nguồn: test fix bug r317-r318 + r332-r333."),

    tc("Export CSV lịch sử", "COMPAT-001", "Normal",
       "Export CSV trên máy Mac (Safari và Chrome) → tên file lưu đúng",
       "- Bot có tên chứa ký tự đặc biệt\n- Có máy Mac với Safari và Chrome",
       "1. Trên Mac + Safari: export CSV cả 2 sub-tab → kiểm tra tên file\n"
       "2. Trên Mac + Chrome: lặp lại",
       "Mac Safari · Mac Chrome",
       "- Cả 2 trình duyệt: export thành công, tên file lưu đúng, ký tự cấm được thay",
       env="PRODUCTION",
       note="Nguồn: test fix bug r319-r320 + r334-r335."),

    tc("Export CSV lịch sử", "OUT-001", "Normal",
       "Export CSV chỉ các đơn ĐÃ TICK CHỌN",
       HIS1 + "\n- Có 5 đơn 単品 trong khoảng ngày đang lọc",
       "1. Tick chọn 2 đơn bất kỳ\n2. Bấm「CSV書出し」\n3. Mở file, đếm số dòng dữ liệu",
       "5 đơn, chọn 2",
       "- File chỉ có 2 dòng dữ liệu tương ứng 2 đơn đã tick",
       env="PRODUCTION",
       note="Suy luận của AI từ spec §2.2 bước 3「lọc theo list_order_id_selected nếu có」. "
            "Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN."),

    tc("Export CSV lịch sử", "OUT-001", "Abnormal",
       "★ Bot có view_name RỖNG → export CSV có bị trả file rỗng không",
       "- Bot có trường tên hiển thị (view_name) rỗng\n- Bot có ≥ 1 đơn",
       "1. Mở 販売履歴 → bấm CSV書出し\n2. Quan sát trình duyệt có tải file về không\n3. Mở file nếu có",
       "view_name rỗng",
       "- Ghi lại kết quả THẬT: có tải được file không, file có nội dung không\n"
       "- Theo spec R19: khi view_name rỗng thì tên file không được gán → trình duyệt nhận response RỖNG\n"
       "- Nếu tái hiện được thì raise bug",
       env="PRODUCTION",
       note="Suy luận của AI từ spec R19. Corpus KHÔNG có TC. Đây là MT-35 — CẦN LEADER QUYẾT có đưa vào bộ chạy."),

    tc("Export CSV lịch sử", "REG-001", "Normal",
       "★ Triển khai ngang — kiểm tra tên file download của các tính năng KHÁC không bị ảnh hưởng",
       "- Bot có tên chứa ký tự / (VD「安井百合子/隠さないで魅せよう」)\n"
       "- Có sẵn dữ liệu ở các tính năng liệt kê bên dưới",
       "1. Lần lượt thực hiện download/export ở: Chat 1:1 (file gửi/nhận, file info friend ở rightbar) · "
       "Image richmenu (1 ảnh trong detail, 1 ảnh ngoài list, nhiều ảnh) · Form (CSV màn list, CSV kết quả, "
       "file PDF đính kèm) · Quản lý CSV · QL info friend · QR action (CSV list, CSV thống kê) · "
       "Event (参加者リスト theo list/theo ngày/theo slot) · Lesson (export slot) · "
       "Salon (lịch làm việc, Google calendar CSV) · Cross analysis · ASP (2 tab) · "
       "friend-history · point-setting (領収書) · plan-estimation (見積書) · Mua slot bill tiền (請求書) · "
       "Quản lý hoa hồng giới thiệu (支払い明細書)\n"
       "2. Với mỗi lần: kiểm tra file tải về được và tên file không chứa ký tự cấm",
       "Tên bot / tên quản lý chứa ký tự /",
       "- TẤT CẢ các tính năng trên đều download được, không lỗi 404\n"
       "- Tên file không chứa ký tự cấm của hệ điều hành\n"
       "- Các tính năng dùng tên fix cứng (領収書 / 見積書 / 請求書 / 支払い明細書) vẫn giữ đúng tên",
       env="PRODUCTION",
       note="Nguồn: test fix bug r336-r362 (khối「TEST TRIỂN KHAI NGANG CÁC TÍNH NĂNG KHÁC」của Bug #32729). "
            "⚠ Đây là TC của TÍNH NĂNG KHÁC, giữ lại vì cùng gốc fix — CẦN LEADER XÁC NHẬN có giữ trong kho "
            "FA-026 hay tách sang kho của từng tính năng. r339 ghi 1 lỗi còn tồn:「Image richmenu: nhập tên quản lý "
            "安井百合子/隠さないで魅せよう thì đang báo lỗi không save được」."),

    tc("Export CSV lịch sử", "REG-001", "Normal",
       "★ Triển khai ngang — liên kết Google Spreadsheet / Calendar với tên chứa ký tự /",
       "- Tên quản lý của form / salon / lesson / QR code chứa ký tự /",
       "1. Form: liên kết Google Spread → kiểm tra tên file sinh ra\n"
       "2. Salon: liên kết Google Spread → kiểm tra\n3. Lesson: liên kết Google Spread → kiểm tra\n"
       "4. QR code: liên kết Google Spread → kiểm tra\n"
       "5. Salon: sync từ LME lên Google Calendar với tên course/staff chứa / → kiểm tra\n"
       "6. Salon: sync từ Google Calendar về LME với title event chứa / → kiểm tra",
       "Tên quản lý chứa ký tự /",
       "- Tất cả 6 luồng: liên kết/sync thành công, không lỗi\n"
       "- Tên file/sự kiện sinh ra hợp lệ",
       env="PRODUCTION",
       note="Nguồn: test fix bug r363-r368. ⚠ TC của TÍNH NĂNG KHÁC — cùng lý do như TC trên, CẦN LEADER XÁC NHẬN."),

    # ══════ 29. Thuế & hóa đơn ══════
    tc("Thuế & hóa đơn", "PAY-001", "Normal",
       "Mua sản phẩm Stripe → sinh được hóa đơn có thuế trên Stripe (10% và 8%)",
       "- Bot A đã liên kết Stripe\n- SP-10 setting thuế 10%, SP-8 setting thuế 8%",
       "1. F1 mua SP-10 thành công\n2. Mở dashboard Stripe tìm invoice của giao dịch\n"
       "3. Kiểm tra invoice có tải về được không và mức thuế ghi nhận\n4. Lặp lại với SP-8",
       "SP-10: thuế 10% · SP-8: thuế 8%",
       "- Cả 2 sản phẩm: trên Stripe có invoice tương ứng, tải về được\n"
       "- Invoice của SP-10 ghi thuế 10%, SP-8 ghi thuế 8%\n"
       "- Thuế là 内税 (đã bao gồm trong giá), khớp nhãn「（税込）」ở màn lịch sử",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r14-r15 + r16-r17. Spec BR-08 (inclusive = true → 内税)."),

    tc("Thuế & hóa đơn", "PAY-001", "Normal",
       "Hóa đơn được sinh ở cả 3 luồng: mua mới · đổi thẻ · job bill định kỳ",
       "- Bot A đã liên kết Stripe\n- SP-C là 継続商品 Stripe, thuế 10%",
       "1. F1 mua mới SP-C → kiểm tra invoice trên Stripe\n"
       "2. F1 đổi thẻ có bill lại → kiểm tra invoice mới\n"
       "3. Chạy job bill kỳ tiếp → kiểm tra invoice mới\n4. Lặp lại toàn bộ với mức thuế 8%",
       "3 luồng × 2 mức thuế",
       "- Cả 3 luồng đều sinh invoice trên Stripe với mức thuế đúng theo setting\n"
       "- Không luồng nào bị thiếu invoice",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r14-r21."),

    tc("Thuế & hóa đơn", "PAY-001", "Abnormal",
       "★ Sản phẩm UnivaPay có setting thuế → có sinh hóa đơn thuế không?",
       "- Bot A đã liên kết UnivaPay\n- SP-U là sản phẩm UnivaPay, setting thuế 10%",
       "1. F1 mua SP-U thành công\n2. Kiểm tra dashboard UnivaPay có hóa đơn/thông tin thuế không\n"
       "3. Đọc nhãn cột số tiền ở màn 販売履歴 phía admin\n4. Lặp lại với job bill kỳ tiếp (nếu là 継続)",
       "SP-U: cổng UnivaPay, tax_item = 10",
       "- Ghi lại kết quả THẬT: UnivaPay có ghi nhận thuế không\n"
       "- Theo spec R38/BR-08: UnivaPay HOÀN TOÀN KHÔNG xử lý thuế (createDataInvoice chỉ gọi ở nhánh Stripe) "
       "dù tax_item vẫn được lưu và UI vẫn hiện「（税込）」\n"
       "- Nếu đúng vậy thì UI đang gây hiểu nhầm cho admin và khách hàng",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r22-r23「check item bill univapay bill được bình thường」(TC gốc chỉ "
            "kiểm bill được, KHÔNG kiểm thuế). Đây là MT-08 — CẦN LEADER QUYẾT."),

    tc("Thuế & hóa đơn", "DATA-001", "Abnormal",
       "Admin XÓA tax id bên Stripe → lần bill sau tự tạo lại tax id mới",
       "- Bot A đã liên kết Stripe (đã sinh sẵn các tax rate)\n- SP Stripe có setting thuế",
       "1. Vào dashboard Stripe xóa/vô hiệu hóa các tax rate đang dùng\n"
       "2. F1 mua sản phẩm → quan sát kết quả\n3. Kiểm tra invoice trên Stripe\n"
       "4. Kiểm tra hệ thống có lưu tax id mới không",
       "Xóa tax id phía Stripe",
       "- Lần bill tiếp theo: hệ thống TỰ TẠO tax id mới và dùng được\n"
       "- Mua hàng vẫn thành công, invoice vẫn có thuế đúng mức",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r24「Khi có bill tiền mới thì tạo tax id mới và update vào bảng s_strip_bot」."),

    # ══════ 30. 各種設定 — 特商法 ══════
    tc("各種設定 — 特商法", "FUNC-001", "Normal",
       "Nhập & lưu「事業者・特商法設定」→ hiển thị đúng ở trang public của MỌI sản phẩm",
       SET,
       "1. Mở sub-tab「事業者・特商法設定」\n2. Nhập nội dung có heading, danh sách, link bằng editor\n"
       "3. Lưu → reload màn hình đối chiếu\n4. Mở trang 特商法 public từ 2 sản phẩm KHÁC NHAU của bot A",
       "Nội dung có: heading 事業者名 · 所在地 · 連絡先 · 1 link ngoài",
       "- Sau reload nội dung được giữ nguyên, định dạng không mất\n"
       "- Trang public của CẢ 2 sản phẩm đều hiện cùng nội dung này (setting cấp bot)\n- Link bấm mở được",
       note="Nguồn: r256「Setting thông tin cửa hàng」(TC gốc chỉ có tiêu đề). Kết quả mong đợi do AI viết theo "
            "spec SCR-BIL-20 — CẦN LEADER XÁC NHẬN."),

    tc("各種設定 — 特商法", "FUNC-001", "Normal",
       "Nhập & lưu template「最終確認画面 ご確認事項」→ nút「テンプレートを引用」ở wizard nạp đúng nội dung",
       SET,
       "1. Mở sub-tab「最終確認画面」\n2. Nhập nội dung template → lưu → reload đối chiếu\n"
       "3. Mở màn edit 1 sản phẩm → wizard bước 3 → bấm「テンプレートを引用」\n4. Đối chiếu nội dung nạp vào",
       "Template「ご確認事項のテンプレート」",
       "- Sau reload template được giữ nguyên\n"
       "- Nút 引用 ở wizard nạp ĐÚNG nội dung template này vào editor\n"
       "- 1 template cấp bot dùng chung cho nhiều sản phẩm",
       note="Nguồn: r257「Setting chung cho màn comfirm」+ r63. Spec SCR-BIL-21."),

    tc("各種設定 — 特商法", "SEC-002", "Abnormal",
       "Editor 特商法 hỗ trợ nhập Source code → kiểm tra nội dung HTML được render an toàn",
       SET,
       "1. Ở editor 特商法 mở chế độ Source code\n2. Nhập HTML có thẻ script và thẻ iframe\n3. Lưu\n"
       "4. Mở trang 特商法 public → quan sát kết quả render\n5. Mở DevTools kiểm tra script có chạy không",
       "HTML chứa <script>alert(1)</script> và <iframe src=...>",
       "- Ghi lại kết quả THẬT: nội dung có bị lọc không, script có chạy không\n"
       "- Theo spec SCR-BIL-25, trang public render thẳng bằng {!! !!} (không escape) → "
       "nếu script chạy được thì đây là lỗ hổng XSS, raise ngay",
       note="Suy luận của AI từ spec §2.4 SCR-BIL-25 (render thẳng info_store) + R35 (mass assignment). "
            "Corpus KHÔNG có TC bảo mật. Đây là MT-36 — CẦN LEADER QUYẾT có đưa vào bộ chạy."),

    # ══════ 31. Liên kết UnivaPay ══════
    tc("Liên kết UnivaPay", "INTG-001", "Normal",
       "★ Bug #32455/#32370 — màn liên kết UnivaPay KHÔNG còn ô nhập App ID",
       "- Đăng nhập admin bot A, mở màn hình liên kết cổng thanh toán",
       "1. Mở màn liên kết mới UnivaPay → quan sát các ô nhập\n2. Mở màn edit liên kết đã có → quan sát",
       "Bot chưa liên kết và bot đã liên kết",
       "- Cả màn liên kết mới và màn edit đều KHÔNG hiện ô nhập App ID nữa\n"
       "- Chỉ còn các ô token / secret / callback ID",
       note="Nguồn: Màn liên kết bill tiền r25 + r32 (Bug #32455 + #32370 — nguyên nhân: KH nhập app id sai; "
            "cách fix: gọi API lấy tự động nên không cần user nhập, ẩn ô input đi). regression"),

    tc("Liên kết UnivaPay", "INTG-001", "Normal",
       "Liên kết UnivaPay với thông tin ĐÚNG → thành công, tự lấy được App ID",
       "- Bot A chưa liên kết UnivaPay\n- Có sẵn token/secret hợp lệ của tài khoản UnivaPay テスト và 本番",
       "1. Nhập token/secret hợp lệ cho cả 2 môi trường → bấm lưu\n2. Quan sát thông báo\n"
       "3. Reload màn hình xem thông tin liên kết\n4. Mua thử 1 sản phẩm 単品 để xác nhận bill được",
       "token/secret hợp lệ (テスト + 本番)",
       "- Liên kết thành công\n- App ID được lấy tự động (không cần nhập), lưu cho cả 2 môi trường\n"
       "- Sau reload thông tin liên kết hiển thị đúng\n- Mua thử sản phẩm bill được bình thường",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r26 + r29."),

    tc("Liên kết UnivaPay", "FUNC-VALID-001", "Abnormal",
       "Liên kết UnivaPay với thông tin SAI hoặc bỏ trống → báo lỗi rõ ràng, không lưu",
       "- Bot A chưa liên kết UnivaPay",
       "1. Bỏ trống toàn bộ ô nhập → bấm lưu → đọc thông báo\n"
       "2. Nhập token/secret không chính xác → bấm lưu → đọc thông báo\n3. Reload kiểm tra không lưu nhầm",
       "Ô trống · token/secret sai",
       "- Cả 2 trường hợp: hiện thông báo lỗi rõ ràng tại đúng ô\n"
       "- KHÔNG lưu liên kết\n- Reload: bot vẫn ở trạng thái chưa liên kết",
       note="Nguồn: Màn liên kết bill tiền r27-r28 (TC gốc chỉ có tiêu đề, tester ghi「BỔ SUNG GIÚP T CÁC CASE "
            "LIÊN QUAN ĐẾN SETTING TRÊN UNIVAPAY -> Xem msg mình hiển thị」). Kết quả mong đợi do AI viết — "
            "CẦN LEADER XÁC NHẬN nội dung message thật."),

    tc("Liên kết UnivaPay", "DATA-001", "Normal",
       "Edit liên kết — không sửa token/secret → App ID KHÔNG thay đổi",
       "- Bot A đã liên kết UnivaPay ở cả 2 môi trường",
       "1. Ghi lại App ID hiện tại (テスト và 本番)\n2. Mở màn edit, KHÔNG sửa gì → bấm lưu\n"
       "3. Đối chiếu lại App ID của cả 2 môi trường",
       "Không sửa token/secret",
       "- App ID của cả テスト và 本番 đều KHÔNG thay đổi",
       note="Nguồn: Màn liên kết bill tiền r33 + r36."),

    tc("Liên kết UnivaPay", "DATA-001", "Normal",
       "Edit liên kết — sửa sang token/secret của CÙNG App ID → App ID không đổi",
       "- Bot A đã liên kết UnivaPay",
       "1. Ghi lại App ID hiện tại\n2. Nhập token/secret khác NHƯNG thuộc cùng App ID → lưu\n"
       "3. Đối chiếu App ID",
       "token/secret khác, cùng App ID",
       "- App ID KHÔNG thay đổi\n- Liên kết vẫn hoạt động (mua thử bill được)",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r34 + r37."),

    tc("Liên kết UnivaPay", "DATA-001", "Normal",
       "Edit liên kết — sửa sang token/secret của App ID KHÁC → App ID được cập nhật",
       "- Bot A đã liên kết UnivaPay",
       "1. Ghi lại App ID hiện tại của môi trường テスト\n"
       "2. Nhập token/secret của một App ID KHÁC → lưu\n3. Đối chiếu App ID\n"
       "4. Lặp lại cho môi trường 本番\n5. Mua thử 1 sản phẩm để xác nhận bill được",
       "token/secret của App ID khác",
       "- App ID được CẬP NHẬT sang App ID mới, đúng theo từng môi trường\n"
       "- Mua thử bill được bình thường",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r35 + r38-r39."),

    tc("Liên kết UnivaPay", "CONC-001", "Abnormal",
       "Double click nút lưu ở màn liên kết → chỉ xử lý 1 lần, không tạo bản ghi trùng",
       "- Bot A chưa liên kết UnivaPay, đã nhập thông tin hợp lệ",
       "1. Double click nhanh nút lưu (< 500ms)\n2. Quan sát thông báo\n3. Reload màn hình\n"
       "4. Kiểm tra thông tin liên kết chỉ có 1 bộ",
       "Double click < 500ms",
       "- Chỉ xử lý 1 lần, không hiện 2 thông báo\n- Thông tin liên kết lưu đúng 1 bộ, không trùng lặp",
       note="Nguồn: Màn liên kết bill tiền r30 + r40 + r70 (TC gốc chỉ có tiêu đề). Kết quả mong đợi do AI viết "
            "theo tiền lệ các TC double click khác — CẦN LEADER XÁC NHẬN."),

    tc("Liên kết UnivaPay", "INTG-001", "Normal",
       "★ Bug #32535 — callback ID có URL webhook thuộc domain hợp lệ → lưu thành công, GIỮ NGUYÊN URL",
       "- Bot A đang liên kết UnivaPay\n- Trên UnivaPay có sẵn webhook với URL thuộc domain hợp lệ của hệ thống",
       "1. Nhập callback ID trỏ tới webhook có URL domain hợp lệ (2 domain hệ thống) → lưu\n"
       "2. Đọc thông báo\n3. Kiểm tra URL webhook trên UnivaPay có bị đổi không\n4. Reload màn hình",
       "callback ID của webhook thuộc 2 domain hợp lệ của hệ thống",
       "- Lưu thành công\n- URL webhook trên UnivaPay GIỮ NGUYÊN (không bị hệ thống ghi đè)\n"
       "- Reload: callback ID đã lưu vẫn hiển thị",
       note="Nguồn: Màn liên kết bill tiền r46-r47 + r55-r56 (Bug #32535「Khi liên kết UnivaPay xuất hiện lỗi "
            "webhookIDが間違っています」— nguyên nhân: lúc check webhook url đang chưa check đủ domain)."),

    tc("Liên kết UnivaPay", "INTG-001", "Normal",
       "Callback ID có URL webhook thuộc domain KHÁC, trên UnivaPay chưa có webhook domain chuẩn → tự sửa URL",
       "- Bot A đang liên kết UnivaPay\n"
       "- Trên UnivaPay: KHÔNG có webhook nào thuộc 2 domain chuẩn của hệ thống",
       "1. Nhập callback ID của webhook có URL domain khác → lưu\n2. Đọc thông báo\n"
       "3. Kiểm tra URL webhook đó trên UnivaPay",
       "callback ID của webhook domain lạ",
       "- Phía hệ thống: lưu thành công\n"
       "- Trên UnivaPay: URL webhook được TỰ ĐỘNG sửa về domain chuẩn của hệ thống",
       note="Nguồn: Màn liên kết bill tiền r48-r49 + r57-r58."),

    tc("Liên kết UnivaPay", "INTG-001", "Abnormal",
       "Callback ID domain khác NHƯNG trên UnivaPay ĐÃ có webhook domain chuẩn → báo lỗi, không sửa được URL",
       "- Bot A đang liên kết UnivaPay\n"
       "- Trên UnivaPay ĐÃ tồn tại 1 webhook thuộc domain chuẩn của hệ thống",
       "1. Nhập callback ID của webhook có URL domain khác → lưu\n2. Đọc thông báo\n"
       "3. Kiểm tra URL webhook trên UnivaPay",
       "Đã có webhook domain chuẩn trên UnivaPay",
       "- Phía hệ thống: báo lỗi「Webhook IDが間違っています。再度確認してください。」\n"
       "- Trên UnivaPay: URL webhook KHÔNG được cập nhật",
       note="Nguồn: Màn liên kết bill tiền r50-r51 + r59-r60."),

    tc("Liên kết UnivaPay", "FUNC-001", "Normal",
       "Không nhập callback ID → vẫn lưu được (webhook là tùy chọn)",
       "- Bot A đang ở màn liên kết UnivaPay",
       "1. Nhập token/secret hợp lệ, để TRỐNG callback ID → lưu\n2. Đọc thông báo\n"
       "3. Mua thử 1 sản phẩm để xác nhận vẫn bill được (theo cơ chế polling)",
       "callback ID rỗng",
       "- Lưu thành công\n- Mua sản phẩm vẫn bill được (không webhook thì dùng polling)",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r45 + r54."),

    tc("Liên kết UnivaPay", "FUNC-001", "Normal",
       "Nhập lại callback ID ĐÃ tồn tại trong hệ thống → vẫn lưu thành công",
       "- Có bot khác đã dùng chính callback ID này",
       "1. Nhập callback ID trùng với bot khác → lưu\n2. Đọc thông báo\n3. Reload kiểm tra",
       "callback ID trùng với bot khác",
       "- Lưu thành công (không bị chặn trùng)",
       note="Nguồn: Màn liên kết bill tiền r53 + r63."),

    tc("Liên kết UnivaPay", "FUNC-VALID-001", "Abnormal",
       "Nhập callback SAI rồi nhập ĐÚNG rồi reload → giữ được giá trị đã lưu",
       "- Bot A đang ở màn liên kết UnivaPay",
       "1. Nhập callback ID sai → lưu → đọc thông báo lỗi\n2. Nhập callback ID đúng → lưu → đọc thông báo\n"
       "3. Reload màn hình → đọc lại giá trị callback ID",
       "callback sai → callback đúng → reload",
       "- Bước 1: báo lỗi\n- Bước 2: lưu thành công\n"
       "- Bước 3: sau reload vẫn hiển thị được callback ID đã lưu (giá trị đúng)",
       note="Nguồn: Màn liên kết bill tiền r52 + r62. Chuỗi thao tác liên tiếp không tách rời → giữ chung 1 TC."),

    tc("Liên kết UnivaPay", "JOB-002", "Normal",
       "Job kiểm tra webhook — URL đúng domain hệ thống → giữ nguyên, đánh dấu hoạt động",
       "- Bot A đã liên kết UnivaPay có webhook\n- Job kiểm tra webhook chạy hằng ngày",
       "1. Trên UnivaPay đổi URL webhook từ domain hệ thống này sang domain hệ thống kia (đều hợp lệ)\n"
       "2. Chạy job kiểm tra webhook\n3. Kiểm tra URL trên UnivaPay và trạng thái webhook phía hệ thống",
       "Đổi giữa 2 domain hợp lệ của hệ thống",
       "- Trên UnivaPay: URL webhook KHÔNG bị đổi\n"
       "- Phía hệ thống: webhook được đánh dấu ở trạng thái hoạt động",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r64-r65."),

    tc("Liên kết UnivaPay", "JOB-002", "Normal",
       "Job kiểm tra webhook — URL bị đổi sang domain LẠ → job tự sửa về domain chuẩn",
       "- Bot A đã liên kết UnivaPay có webhook",
       "1. Trên UnivaPay đổi URL webhook sang một domain lạ\n2. Chạy job kiểm tra webhook\n"
       "3. Kiểm tra URL trên UnivaPay và trạng thái webhook phía hệ thống\n"
       "4. Lặp lại trong tình huống domain chuẩn ĐÃ bị webhook khác chiếm",
       "URL webhook bị đổi sang domain lạ",
       "- Trường hợp domain chuẩn còn trống: job tự sửa URL về domain chuẩn, webhook ở trạng thái hoạt động\n"
       "- Trường hợp domain chuẩn đã bị chiếm: KHÔNG sửa được, webhook bị đánh dấu KHÔNG hoạt động",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r66-r67."),

    tc("Liên kết UnivaPay", "JOB-002", "Normal",
       "Job kiểm tra webhook — webhook chuyển từ hoạt động sang NGỪNG → job kích hoạt lại",
       "- Bot A có webhook đang ở trạng thái hoạt động phía hệ thống",
       "1. Trên UnivaPay chuyển webhook sang trạng thái ngừng hoạt động\n2. Chạy job kiểm tra webhook\n"
       "3. Kiểm tra trạng thái webhook trên UnivaPay và phía hệ thống\n"
       "4. Lặp lại trong tình huống domain chuẩn đã bị chiếm (job không sửa được)",
       "webhook active → inactive",
       "- Trường hợp sửa được: trên UnivaPay webhook chuyển lại trạng thái hoạt động, phía hệ thống giữ nguyên\n"
       "- Trường hợp không sửa được: phía hệ thống cập nhật trạng thái tương ứng",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r68-r69."),

    tc("Liên kết UnivaPay", "FUNC-001", "Normal",
       "Setting brand card — mặc định sau khi liên kết chọn 2 loại đầu tiên",
       "- Bot A vừa liên kết cổng thanh toán UnivaPay thành công (lần đầu)",
       "1. Mở màn setting bill tiền\n2. Quan sát các loại brand card đang được tick\n"
       "3. Hủy liên kết rồi liên kết lại → quan sát lại",
       "Bot mới liên kết",
       "- Mặc định tick sẵn 2 loại brand card đầu tiên (visa và master card)\n"
       "- Sau khi hủy liên kết rồi liên kết lại: GIỮ NGUYÊN setting cũ (không reset về mặc định)",
       note="Nguồn: Màn liên kết bill tiền r7-r8."),

    tc("Liên kết UnivaPay", "FUNC-001", "Normal",
       "Setting brand card — tick / bỏ tick TỰ ĐỘNG LƯU ngay, không cần bấm nút lưu",
       "- Bot A đã liên kết UnivaPay",
       "1. Ở màn setting bill tiền tick thêm 1 loại brand card → KHÔNG bấm nút lưu → reload trang\n"
       "2. Kiểm tra loại card vừa tick còn được chọn không\n"
       "3. Bỏ tick toàn bộ các loại card → reload trang → kiểm tra\n"
       "4. Mở màn nhập thẻ phía LINE đối chiếu",
       "Tick thêm 1 loại → bỏ tick toàn bộ",
       "- Bước 2: loại card vừa tick VẪN được chọn sau reload (auto-save)\n"
       "- Bước 3: sau reload không loại nào được chọn\n"
       "- Màn nhập thẻ phía LINE hiển thị khớp với setting hiện tại",
       note="Nguồn: Màn liên kết bill tiền r9-r10 + r11-r22."),

    tc("Liên kết UnivaPay", "COMPAT-LEGACY-001", "Normal",
       "Recover dữ liệu brand card cũ → bot cũ được gán đúng bộ brand card",
       "- Có bot với dữ liệu brand card ở định dạng cũ (2 nhóm giá trị khác nhau)",
       "1. Chạy tiến trình recover dữ liệu brand card\n"
       "2. Với nhóm giá trị thứ nhất: mở màn setting bill tiền quan sát các loại card được tick\n"
       "3. Với nhóm giá trị thứ hai: mở màn setting bill tiền quan sát",
       "2 nhóm dữ liệu brand card cũ",
       "- Nhóm 1: sau recover hiển thị chọn 2 loại card đầu tiên (visa + master)\n"
       "- Nhóm 2: sau recover hiển thị chọn CẢ 5 loại card",
       note="Nguồn: Màn liên kết bill tiền r3-r6. regression"),

    tc("Liên kết UnivaPay", "SEC-001", "Normal",
       "Hủy liên kết cổng thanh toán — yêu cầu nhập mật khẩu admin",
       "- Bot A đã liên kết UnivaPay",
       "1. Bấm hủy liên kết → quan sát màn xác nhận\n2. Nhập mật khẩu SAI → xác nhận → đọc thông báo\n"
       "3. Nhập mật khẩu ĐÚNG → xác nhận\n4. Reload màn hình kiểm tra trạng thái liên kết\n"
       "5. Mở trang mua sản phẩm phía LINE",
       "Mật khẩu sai · mật khẩu đúng",
       "- Mật khẩu sai: báo lỗi, KHÔNG hủy liên kết\n"
       "- Mật khẩu đúng: hủy liên kết thành công\n"
       "- Sau khi hủy: trang mua phía LINE báo「決済できません。管理者に連絡してください。」",
       note="Suy luận của AI từ spec §2.3「@unlinkPaymentMethod — Hash::check(password, Auth::user()->password)」"
            "+ §2.4 (chặn khi chưa cấu hình cổng). Corpus KHÔNG có TC hủy liên kết. CẦN LEADER XÁC NHẬN. "
            "⚠ Spec R40: hủy liên kết KHÔNG xóa nhóm khóa test UnivaPay → xem MT-37."),

    # ══════ 32. Liên kết Stripe ══════
    tc("Liên kết Stripe", "INTG-001", "Normal",
       "Liên kết Stripe lần đầu → tạo đủ 4 mức thuế (test/live × 8%/10%) và lưu lại",
       "- Bot A chưa liên kết Stripe\n- Có tài khoản Stripe hợp lệ",
       "1. Thực hiện luồng liên kết Stripe (OAuth) tới khi hoàn tất\n"
       "2. Mở dashboard Stripe kiểm tra các tax rate được tạo\n"
       "3. Đối chiếu id tax rate lưu ở hệ thống với id trên Stripe\n4. Mua thử sản phẩm thuế 10% và 8%",
       "4 mức thuế: test 8% · test 10% · live 8% · live 10%",
       "- Liên kết thành công\n- Trên Stripe có đủ 4 tax rate tương ứng\n"
       "- Id lưu ở hệ thống khớp với id trên Stripe\n- Mua thử: invoice có thuế đúng mức",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r11. Spec §2.3 EP-30 linkPayment tạo 4 TaxRate."),

    tc("Liên kết Stripe", "INTG-001", "Normal",
       "Hủy liên kết Stripe cũ → liên kết sang tài khoản khác → tạo lại 4 mức thuế mới",
       "- Bot A đã liên kết Stripe với tài khoản X\n- Có tài khoản Stripe Y khác",
       "1. Ghi lại 4 id tax rate hiện tại\n2. Hủy liên kết Stripe\n3. Liên kết sang tài khoản Y\n"
       "4. Đối chiếu 4 id tax rate mới với id trên tài khoản Y\n5. Mua thử sản phẩm",
       "Tài khoản X → tài khoản Y",
       "- 4 id tax rate được cập nhật sang id của tài khoản Y\n"
       "- Mua thử: giao dịch và invoice ghi nhận ở tài khoản Y",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r12."),

    tc("Liên kết Stripe", "COMPAT-LEGACY-001", "Normal",
       "Recover các liên kết Stripe CŨ → bổ sung đủ 4 mức thuế cho bot đã liên kết từ trước",
       "- Có bot đã liên kết Stripe TRƯỚC khi có tính năng thuế (chưa có tax rate)",
       "1. Chạy tiến trình recover liên kết cũ\n2. Đối chiếu 4 id tax rate lưu ở hệ thống với Stripe\n"
       "3. Mua thử sản phẩm thuế 10% và 8% → kiểm tra invoice",
       "Bot liên kết Stripe từ trước",
       "- Sau recover: đủ 4 id tax rate được lưu và khớp với Stripe\n"
       "- Mua thử: invoice có thuế đúng mức",
       env="PRODUCTION",
       note="Nguồn: Test invoice (stripe) r13. regression"),

    tc("Liên kết Stripe", "PERM-001", "Abnormal",
       "Sản phẩm dùng Stripe nhưng bot CHƯA liên kết Stripe → chặn ở trang nhập thẻ",
       "- Bot A có sản phẩm setting cổng Stripe nhưng CHƯA liên kết Stripe",
       "1. Friend mở 商品ページ → bấm mua → nhập friend info → sang trang nhập thẻ\n2. Đọc thông báo",
       "Chưa liên kết Stripe",
       "- Hiện thông báo「決済できません。管理者に連絡してください。」\n- Không vào được form nhập thẻ",
       note="Suy luận của AI từ spec §2.4 SCR-BIL-24「CHẶN khi chưa cấu hình cổng: thiếu bản ghi UnivaPay / "
            "thiếu public key Stripe / payment_method rỗng」. Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN."),

    # ══════ 33. Domain LIFF & redirect ══════
    tc("Domain LIFF & redirect", "LIFF-ENTRY-002", "Normal",
       "★ Support #32786 — mở link bill item KHÔNG còn hiện cảnh báo「外部サイトに移動したため」",
       "- Bot đã được recover domain LIFF/token về cấu hình chuẩn\n"
       "- Có sẵn: button có multi action · button không multi action · image map có/không multi action",
       "1. Mở link bill item từ BUTTON (có multi action) → quan sát domain và cảnh báo\n"
       "2. Mở từ BUTTON (không multi action) → quan sát\n3. Mở từ IMAGE MAP (có multi action) → quan sát\n"
       "4. Mở từ IMAGE MAP (không multi action) → quan sát",
       "4 điểm vào × cùng 1 sản phẩm bill item",
       "- Cả 4 điểm vào: mở thẳng ra domain chuẩn của hệ thống\n"
       "- KHÔNG bị redirect sang domain khác nữa\n"
       "- KHÔNG hiện message「外部サイトに移動したため」",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r91-r106 (Support #32786 — nguyên nhân: liff callback trỏ về domain "
            "này còn các tính năng bill tiền redirect về domain kia). RULE-08: domain → PRODUCTION."),

    tc("Domain LIFF & redirect", "FUNC-VALID-001", "Abnormal",
       "Nhập token UnivaPay có domain KHÔNG khớp môi trường server → báo lỗi domain",
       "- Đang ở màn liên kết bill tiền của bot A",
       "1. Chưa nhập gì → bấm lưu → quan sát có báo lỗi domain không\n"
       "2. Nhập token có domain KHỚP với server → lưu → quan sát\n"
       "3. Nhập token có domain KHÔNG khớp server → lưu → đọc thông báo lỗi\n"
       "4. Nhập token 1 domain nhưng token đó đăng ký NHIỀU domain trong đó có domain đúng → lưu",
       "4 tình huống domain như bước 1-4",
       "- Bước 1: KHÔNG báo lỗi domain\n- Bước 2: KHÔNG báo lỗi, lưu thành công\n"
       "- Bước 3: báo lỗi sai domain, thông báo nêu rõ domain hợp lệ cho môi trường đó\n"
       "- Bước 4: KHÔNG báo lỗi, lưu thành công",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r74-r77 (Support #32786). Nội dung message theo môi trường: "
            "テスト環境用のドメインは「s.lmes.jp」のみ / 本番環境用のドメインは「go.lmes.jp」のみ."),

    tc("Domain LIFF & redirect", "JOB-002", "Normal",
       "Job recover domain — bot CHƯA setting token → recover endpoint về domain chuẩn",
       "- Bot chưa setting token UnivaPay, endpoint URL đang là domain cũ",
       "1. Chạy job recover domain\n2. Kiểm tra endpoint URL của bot sau khi recover\n"
       "3. Mở link bill item của bot đó trên LINE app",
       "Bot chưa setting token",
       "- Endpoint URL được recover về domain chuẩn của môi trường\n"
       "- Mở link bill item ra đúng domain chuẩn",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r79 + r90."),

    tc("Domain LIFF & redirect", "JOB-002", "Abnormal",
       "Job recover domain — token và endpoint KHÔNG khớp domain → chỉ báo lỗi khi admin bấm lưu",
       "- Bot có endpoint URL và domain token thuộc 2 domain khác nhau",
       "1. Chạy job recover domain\n2. Kiểm tra endpoint URL sau recover\n"
       "3. Mở màn liên kết bill tiền, KHÔNG sửa gì → bấm lưu → đọc thông báo",
       "endpoint và token khác domain",
       "- Job KHÔNG tự recover được domain token của khách hàng\n"
       "- Khi admin bấm lưu ở màn liên kết mới báo lỗi sai domain",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r80-r81."),

    tc("Domain LIFF & redirect", "REG-001", "Normal",
       "Sau recover domain → bill tiền của ITEM · EVENT · SALON · LESSON đều hoạt động bình thường",
       "- Bot đã chạy recover domain\n- Có sẵn: 1 item bill tiền · 1 event có bill · 1 salon có bill · 1 lesson có bill",
       "1. Mua item bill tiền → kiểm tra thành công\n2. Booking event có bill → kiểm tra\n"
       "3. Booking salon có bill → kiểm tra\n4. Booking lesson có bill → kiểm tra",
       "4 luồng bill tiền",
       "- Cả 4 luồng đều bill tiền thành công, không lỗi domain\n- Không hiện cảnh báo chuyển trang ngoài",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r83-r86. regression"),

    tc("Domain LIFF & redirect", "LIFF-ENTRY-002", "Normal",
       "Mở link bill trực tiếp TRONG và NGOÀI app LINE → đều ra domain chuẩn và bill được",
       "- Bot đã recover domain, đã setting token đúng domain chuẩn",
       "1. Mở link item bill tiền trực tiếp TRONG app LINE → quan sát domain, hoàn tất mua\n"
       "2. Mở cùng link NGOÀI app LINE (trình duyệt) → quan sát domain, hoàn tất mua\n"
       "3. Lặp lại với cả item bill 1 lần và item chu kỳ",
       "2 cách mở × 2 loại item",
       "- Cả 4 trường hợp: mở ra domain chuẩn, bill tiền thành công",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r117-r124 + r134-r141 (đã ghi rõ「đã check cả bill 1 lần + chu kỳ」)."),

    tc("Domain LIFF & redirect", "INTG-001", "Normal",
       "Nhập token domain chuẩn → hệ thống tự cập nhật LIFF app form về cùng domain",
       "- Bot đang có LIFF app form ở domain cũ",
       "1. Ghi lại domain của LIFF app form hiện tại\n"
       "2. Ở màn liên kết bill tiền nhập token có domain chuẩn → lưu thành công\n"
       "3. Kiểm tra lại domain của LIFF app form\n4. Mở link item bill tiền trên LINE app",
       "LIFF app form domain cũ → token domain chuẩn",
       "- Sau khi lưu token: LIFF app form được tự động đổi sang domain chuẩn\n"
       "- Link item mở ra đúng domain chuẩn",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r115-r116 + r151-r152."),

    tc("Domain LIFF & redirect", "COMPAT-LEGACY-001", "Normal",
       "Link item chuyển từ LIFF app QR landing sang LIFF app form",
       "- Bot có LIFF app QR landing và LIFF app form khác domain nhau",
       "1. Ở màn list item, copy link 商品ページ\n2. Đối chiếu link dùng LIFF app nào\n"
       "3. Mở link trên LINE app và ngoài LINE app",
       "2 LIFF app khác domain",
       "- Link item sử dụng LIFF app FORM (không còn dùng LIFF app QR landing)\n"
       "- Mở được ở cả trong và ngoài LINE app",
       env="PRODUCTION",
       note="Nguồn: Màn liên kết bill tiền r115 mục 2「mh list item: link item => chuyển sang sử dụng link liff "
            "app form (trước đây dùng liff app QR landing)」. regression"),

    # ══════ 34. Phân quyền & môi trường ══════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Tài khoản STAFF truy cập màn 商品販売 → theo đúng lưới phân quyền của bot",
       "- Bot A có tài khoản staff được mời\n- Đăng nhập bằng tài khoản staff",
       "1. Staff mở /basic/sales/index → quan sát có vào được không\n"
       "2. Nếu vào được: thử tạo sản phẩm · sửa · xóa · hoàn tiền · hủy hợp đồng · export CSV · "
       "liên kết cổng thanh toán\n3. Ghi lại thao tác nào bị chặn, thao tác nào cho phép",
       "Tài khoản staff",
       "- Ghi lại kết quả THẬT cho từng thao tác\n"
       "- Route bị chặn phải hiện thông báo「この権限は許可されていません。」\n"
       "- KHÔNG được lỗi 500 hoặc trắng màn",
       note="Nguồn: Màn liên kết bill tiền r31 / r41 / r71 + Improve bill tiền stripe r62 + univapay r274/r290 "
            "(「Check account staff」— TC gốc chỉ có tiêu đề, KHÔNG có kết quả mong đợi). "
            "⚠ Spec §9.4 mục 3: danh sách route trong whitelist staff CHƯA XÁC MINH → xem MT-38."),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "★ Truy cập TRỰC TIẾP API bill-item bằng tài khoản không có quyền / không đăng nhập",
       "- Ghi lại request của các thao tác: lưu sản phẩm · hoàn tiền 1 đơn · hủy hợp đồng\n"
       "- Có công cụ gửi request trực tiếp",
       "1. Đăng xuất (hoặc dùng tài khoản của bot KHÁC)\n"
       "2. Gửi lại từng request đã ghi, chỉ đổi id sang bản ghi của bot A\n"
       "3. Ghi lại HTTP status và kiểm tra dữ liệu bot A có bị thay đổi không",
       "3 request: lưu sản phẩm · hoàn tiền · hủy hợp đồng",
       "- Ghi lại kết quả THẬT cho từng request\n"
       "- Theo spec R5: nhóm route thanh toán + bill-item AJAX KHÔNG có middleware auth, chỉ dựa vào "
       "botId gửi từ client → nếu thao tác thành công thì đây là lỗ hổng NGHIÊM TRỌNG (hoàn tiền/hủy "
       "hợp đồng của bot khác), raise ngay",
       note="Suy luận của AI từ spec R5 + R12 (IDOR ở orderHistoryDetail không lọc bot_id). "
            "Corpus KHÔNG có TC bảo mật tầng API. Đây là MT-39 — CẦN LEADER QUYẾT có đưa vào bộ chạy. "
            "Tham chiếu quy tắc: bug quyền ở tầng API phải rà TẤT CẢ màn sibling cùng lưới phân quyền."),

    tc("Phân quyền & môi trường", "SEC-002", "Abnormal",
       "★ Gọi API lưu sản phẩm với dữ liệu vi phạm ràng buộc client (giá 0円, tên siêu dài)",
       "- Ghi lại request lưu sản phẩm bằng DevTools",
       "1. Sửa payload: giá = 0 → gửi request → kiểm tra list sản phẩm\n"
       "2. Sửa payload: tên quản lý 10.000 ký tự → gửi → kiểm tra\n"
       "3. Sửa payload: giá âm → gửi → kiểm tra\n"
       "4. Với mỗi trường hợp tạo được: mở trang mua phía LINE xem hiển thị thế nào",
       "giá = 0 · tên 10.000 ký tự · giá âm",
       "- Ghi lại kết quả THẬT cho từng payload\n"
       "- Theo spec R6/BR-15: saveItem KHÔNG có validation server và endpoint được miễn CSRF → "
       "nếu tạo được sản phẩm giá 0円 hoặc tên 10.000 ký tự thì raise ngay\n"
       "- Đặc biệt kiểm: sản phẩm giá 0円 có mua được không, có sinh đơn 0円 không",
       note="Suy luận của AI từ spec R6 + BR-15 + §5.2. Corpus KHÔNG có TC. Đây là MT-02 (cùng gốc) — "
            "CẦN LEADER QUYẾT."),

    tc("Phân quyền & môi trường", "SEC-002", "Abnormal",
       "★ Upload file KHÔNG PHẢI ảnh qua ô upload ảnh sản phẩm",
       "- Đang ở wizard bước 1 của màn tạo sản phẩm\n- Chuẩn bị file .php và file .exe đổi đuôi thành .jpg",
       "1. Upload file .php (đổi đuôi .jpg) → quan sát kết quả\n"
       "2. Upload file .exe (đổi đuôi .jpg) → quan sát\n"
       "3. Nếu upload được: lấy đường dẫn file trả về, thử truy cập trực tiếp bằng trình duyệt\n"
       "4. Upload file ảnh rất lớn (VD 50MB) → quan sát",
       "file .php · file .exe (đổi đuôi) · ảnh 50MB",
       "- Ghi lại kết quả THẬT cho từng file\n"
       "- Theo spec R34: uploadFile KHÔNG validate MIME/kích thước TRƯỚC khi lưu vào thư mục 0777 → "
       "nếu file .php lưu được và truy cập được thì đây là lỗ hổng NGHIÊM TRỌNG, raise ngay",
       env="PRODUCTION",
       note="Suy luận của AI từ spec R34 + Field Matrix #16. Corpus chỉ có r419-r420 (ảnh 0KB, ảnh không extension). "
            "Đây là MT-40 — CẦN LEADER QUYẾT."),

    tc("Phân quyền & môi trường", "ENV-002", "Normal",
       "Sản phẩm 本番 và テスト dùng khóa API tách riêng — không lẫn giao dịch",
       "- Bot A đã liên kết cổng thanh toán ở CẢ 2 môi trường\n- Có SP-P (本番) và SP-T (テスト) cùng cổng",
       "1. Mua SP-T bằng thẻ test → kiểm tra giao dịch xuất hiện ở dashboard môi trường TEST của cổng\n"
       "2. Mua SP-P bằng thẻ thật → kiểm tra giao dịch xuất hiện ở dashboard môi trường LIVE\n"
       "3. Kiểm tra 販売履歴 với filter môi trường tương ứng",
       "SP-T (テスト) · SP-P (本番)",
       "- Giao dịch của SP-T CHỈ xuất hiện ở dashboard môi trường test\n"
       "- Giao dịch của SP-P CHỈ xuất hiện ở dashboard môi trường live\n"
       "- 販売履歴 với từng filter hiển thị đúng đơn tương ứng",
       env="PRODUCTION",
       note="Suy luận của AI từ spec §1.6 + BR-10. Corpus có r24-r26 (filter list) nhưng KHÔNG kiểm tách khóa API. "
            "CẦN LEADER XÁC NHẬN — đặc biệt là bước 2 (giao dịch thật bằng thẻ thật)."),

    tc("Phân quyền & môi trường", "ENV-002", "Normal",
       "Bộ đếm thống kê của sản phẩm tách riêng theo môi trường 本番 / テスト",
       "- SP có cả đơn ở môi trường 本番 và đơn ở môi trường テスト (2 sản phẩm khác nhau cùng loại)",
       "1. Mua 2 đơn của sản phẩm テスト → xem cột 販売数 khi filter テスト\n"
       "2. Chuyển filter sang 本番 → xem cột 販売数 của sản phẩm 本番\n"
       "3. Đối chiếu 2 con số không cộng dồn lẫn nhau",
       "2 đơn テスト · N đơn 本番",
       "- Bộ đếm ở filter テスト chỉ tính đơn テスト\n- Bộ đếm ở filter 本番 chỉ tính đơn 本番\n"
       "- Không cộng dồn giữa 2 môi trường",
       note="Suy luận của AI từ spec §1.6「Bộ counter thống kê tách đôi: number_trial vs number_trial_test, "
            "sum_sales vs sum_sales_test」. Corpus có r24 kèm cảnh báo của tester「khi nào chọn MT test thì hiện "
            "count cả các sp được mua ở MT test」. CẦN LEADER XÁC NHẬN."),

    tc("Phân quyền & môi trường", "SYNC-APP-001", "Normal",
       "API mobile chỉ trả dữ liệu môi trường 本番",
       "- Bot A có sản phẩm và đơn ở cả 2 môi trường\n- Có app mobile đã đăng nhập bot A",
       "1. Mở app mobile, vào phần bán hàng / thông báo đơn hàng\n"
       "2. Đối chiếu danh sách sản phẩm và đơn hiển thị với dữ liệu 2 môi trường trên web",
       "Sản phẩm/đơn ở cả 本番 và テスト",
       "- App mobile CHỈ hiển thị dữ liệu môi trường 本番\n- KHÔNG hiển thị sản phẩm/đơn của môi trường テスト",
       note="Suy luận của AI từ spec §1.6「API mobile chỉ trả dữ liệu 本番」. Corpus KHÔNG có TC. "
            "Liên quan Bug KH #36443 (App + API app). CẦN LEADER XÁC NHẬN."),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Sản phẩm phiên bản CŨ không lẫn vào danh sách phiên bản mới",
       "- Bot A có cả sản phẩm phiên bản cũ (màn /basic/list-items-old) và sản phẩm phiên bản hiện hành",
       "1. Mở màn 商品一覧 hiện hành → đếm số sản phẩm và đối chiếu tên\n"
       "2. Mở màn danh sách sản phẩm phiên bản cũ → đối chiếu\n"
       "3. Kiểm tra màn 商品一覧 có ghi chú dừng tính năng cũ không",
       "Sản phẩm cũ + sản phẩm mới",
       "- Màn hiện hành CHỈ hiện sản phẩm phiên bản mới, không lẫn sản phẩm cũ\n"
       "- Màn cũ chỉ hiện sản phẩm cũ\n- Có ghi chú dừng tính năng ở màn list item cũ",
       note="Nguồn: r377「thêm ghi chú dừng tính năng ở màn list item (cũ)」+ spec §1.5 (V2 luôn lọc "
            "is_product_new = 1)."),
]
