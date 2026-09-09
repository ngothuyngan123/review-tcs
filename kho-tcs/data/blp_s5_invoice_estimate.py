# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 25-28: màn lịch sử thanh toán / lãnh thụ thư (SCR-BLP-03) và báo giá (SCR-BLP-05).

Nguồn chính: TCsLine_Bill tiền → tab「Improve màn download quản lý hóa đơn」
  (09/2025 → 11/2025, 349 dòng, 323 TC lá — Feature #30564, Bug #32649, Bug KH #32953).
Bổ sung: tab「Estimation」(09/2023, phần lớn CHỈ CÓ TIÊU ĐỀ), tab「Task nhỏ」(Feature #29722 —
         design biên lai), tab「Quản lý hợp đồng」r828-r849 (SpecImprove #33313, #33149).
"""
from _common import tc

INV = ("- Đăng nhập owner có ≥ 12 giao dịch thanh toán trải nhiều tháng\n"
       "- Mở /basic/payment-history (từ nút「領収書の発行」)")

S5 = [
    # ═════════════ 25. Lịch sử thanh toán — theo năm ═════════════
    tc("Lịch sử thanh toán — theo năm", "UI-001", "Normal",
       "Title màn lịch sử thanh toán + view mặc định theo năm",
       INV,
       "1. Mở /basic/payment-history\n2. Đọc tiêu đề\n3. Quan sát chế độ hiển thị mặc định",
       "≥ 12 giao dịch",
       "- Tiêu đề「決済履歴・領収書のダウンロード」\n- Mặc định hiển thị theo NĂM (年間決済一覧)",
       note="Nguồn: r34, r35."),

    tc("Lịch sử thanh toán — theo năm", "DATA-003", "Normal",
       "Year picker: mặc định năm hiện tại, nút </> đổi năm, F5 reset về mặc định",
       INV,
       "1. Đọc giá trị year picker mặc định\n2. Click「<」→ ghi giá trị\n3. Click「>」→ ghi giá trị\n"
       "4. Click mở dropdown năm\n5. Nhấn F5 và đọc lại year picker",
       "Năm hiện tại = 2026",
       "- Mặc định hiện「2026年」\n- Click < → 2025年; click > → 2026年\n"
       "- Click box mở droplist các năm\n- Sau F5: quay lại năm hiện tại (mặc định)",
       note="Nguồn: r36-r41."),

    tc("Lịch sử thanh toán — theo năm", "DATA-002", "Normal",
       "Bảng 12 tháng: format 年月 + số tiền + nút xem chi tiết",
       INV,
       "1. Quan sát bảng bên trái\n2. Đếm số dòng\n3. Đọc format cột 年月 và cột ご請求額",
       "Năm 2026 có giao dịch ở 3 tháng",
       "- Hiện đủ 12 dòng tháng, thứ tự từ nhỏ tới lớn (tháng 1 → tháng 12)\n"
       "- Cột 年月 format「yyyy年mm月分」\n"
       "- Cột ご請求額 hiện tổng tiền của tháng + 円",
       note="Nguồn: r46, r47, r49."),

    tc("Lịch sử thanh toán — theo năm", "LIST-002", "Abnormal",
       "Tháng không có giao dịch → hiện - 円 và nút xem chi tiết bị disable",
       INV + "\n- Năm đang xem có ≥ 1 tháng không phát sinh giao dịch",
       "1. Tìm dòng tháng không có giao dịch\n2. Đọc cột ご請求額\n3. Quan sát nút「詳細を確認 >」",
       "Tháng 07/2026 không có giao dịch",
       "- Cột ご請求額 hiện「- 円」\n- Nút「詳細を確認 >」bị disable, không click được",
       note="Nguồn: r51, r52."),

    tc("Lịch sử thanh toán — theo năm", "FUNC-001", "Normal",
       "Click 詳細を確認 → mở panel chi tiết đúng tháng, title format yyyy年mm月 詳細",
       INV,
       "1. Click「詳細を確認 >」của tháng 03/2026\n2. Đọc title panel bên phải",
       "Tháng 03/2026 có 5 giao dịch",
       "Panel phải hiện title「2026年03月 詳細」và danh sách giao dịch của đúng tháng đó",
       note="Nguồn: r54, r56."),

    tc("Lịch sử thanh toán — theo năm", "DATA-002", "Normal",
       "Tổng tiền tháng = tổng các giao dịch hợp lệ trong tháng đó",
       INV + "\n- Tháng 03/2026 có 3 giao dịch: 10.780円, 10.780円, 116.424円",
       "1. Đọc ご請求額 của tháng 03/2026 ở panel trái\n"
       "2. Mở chi tiết tháng, cộng tay cột 利用料 của các dòng\n3. So sánh 2 con số",
       "3 giao dịch: 10.780 + 10.780 + 116.424 = 138.  (tự tính: 137.984円)",
       "Tổng ở panel trái = tổng cộng tay các dòng chi tiết = 137.984円 "
       "(chỉ tính bản ghi hợp lệ: type=1, status_refund=0, năm thì chỉ lấy parent_month=1)",
       note="Nguồn: r49 + BR-06 (feature-spec.md §5). RULE-07: đối chiếu số tổng với số chi tiết."),

    tc("Lịch sử thanh toán — theo năm", "FUNC-001", "Normal",
       "Dropdown chuyển giữa 年間決済一覧 và 月次決済一覧",
       INV,
       "1. Click dropdown「年間決済一覧」\n2. Đọc các option\n3. Chọn「月次決済一覧」\n"
       "4. Quan sát màn hình\n5. Double-click dropdown",
       "—",
       "- Dropdown có 2 option:「年間決済一覧」và「月次決済一覧」\n"
       "- Chọn 月次決済一覧: màn chuyển sang chế độ hiển thị theo tháng\n"
       "- Double-click: đóng droplist, không lỗi",
       note="Nguồn: r42-r45, r169-r171. ⚠ Chế độ「月次決済一覧」KHÔNG có trong feature-spec.md §2 "
            "(spec chỉ mô tả panel năm + panel chi tiết tháng) — xem MT-22."),

    # ═════════════ 26. Lịch sử thanh toán — theo tháng & lọc ═════════════
    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-003", "Normal",
       "Calendar From ~ To: format + mặc định từ ngày 1 của năm hiện tại đến hôm nay",
       INV + "\n- Đang ở chế độ 月次決済一覧",
       "1. Đọc giá trị mặc định của Calendar From và To\n2. Ghi lại format hiển thị",
       "Ngày hiện tại = 2026/08/24",
       "- Format yyyy.mm.dd\n- Mặc định: From = 2026.01.01, To = 2026.08.24 (ngày hiện tại)",
       note="Nguồn: r132-r137."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-003", "Abnormal",
       "Calendar: To < From không chọn được; To = From lọc đúng 1 ngày",
       INV + "\n- Có giao dịch trong ngày 2026/03/15",
       "1. Chọn From = 2026/04/01, thử chọn To = 2026/03/15\n"
       "2. Chọn From = To = 2026/03/15\n3. Quan sát danh sách",
       "From=2026/04/01 To=2026/03/15; From=To=2026/03/15",
       "- Không chọn được To nhỏ hơn From\n"
       "- From = To = 2026/03/15: chỉ hiện giao dịch trong ngày đó",
       note="Nguồn: r138, r139."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Checkbox 全期間: bật thì hiện toàn bộ hóa đơn mọi thời điểm",
       INV,
       "1. Quan sát trạng thái mặc định của「全期間」\n2. Click bật「全期間」\n"
       "3. Đếm số bản ghi và so với khi lọc theo calendar\n4. Click lại lần nữa",
       "≥ 12 giao dịch trải 2 năm",
       "- Mặc định 全期間 KHÔNG được chọn\n"
       "- Bật: hiện toàn bộ hóa đơn của mọi năm, nút chuyển màu xanh đậm\n"
       "- Bật lại lần nữa vẫn giữ trạng thái hiển thị toàn bộ",
       note="Nguồn: r141-r144."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "STATE-002", "Normal",
       "Đang ở 全期間 → giá trị calendar giữ nguyên, không bị reset",
       INV,
       "1. Chọn khoảng calendar 2026/03/01 ~ 2026/03/31\n2. Bật「全期間」\n"
       "3. Quan sát giá trị 2 ô calendar",
       "From=2026/03/01, To=2026/03/31",
       "2 ô calendar VẪN giữ giá trị 2026.03.01 ~ 2026.03.31 (không bị xóa/đổi)",
       note="Nguồn: r140."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Modal 絞り込み: lọc theo 料金プラン",
       INV + "\n- Có hóa đơn của cả 3 loại bot: free, standard, pro",
       "1. Click nút「絞り込み」\n2. Không chọn plan nào → áp dụng, đếm bản ghi\n"
       "3. Chỉ chọn 1 plan (standard) → áp dụng, đếm bản ghi\n4. Chọn cả 3 plan → áp dụng, đếm bản ghi",
       "Hóa đơn của free, standard, pro",
       "- Không chọn plan nào: hiện toàn bộ hóa đơn cả 3 loại\n"
       "- Chọn 1 plan: chỉ hiện hóa đơn của plan đó\n- Chọn tất cả: hiện toàn bộ",
       note="Nguồn: r150-r153."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Modal 絞り込み: lọc theo 決済方法",
       INV + "\n- Có hóa đơn bill card và bill transfer",
       "1. Mở modal filter, chọn 1 option 決済方法 → áp dụng\n"
       "2. Chọn cả 2 option → áp dụng\n3. Không chọn option nào → áp dụng",
       "Hóa đơn card và transfer",
       "- Chọn 1 option: chỉ hiện hóa đơn có phương thức đó\n"
       "- Chọn all hoặc không chọn: hiện cả 2 loại phương thức",
       note="Nguồn: r154-r156."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Modal 絞り込み: lọc theo bot (1 bot / nhiều bot / tất cả)",
       INV + "\n- Tài khoản có ≥ 3 bot đều có hóa đơn",
       "1. Mở modal filter, quan sát bảng bot (tên + LINE ID)\n"
       "2. Chọn 1 bot → áp dụng\n3. Chọn 2 bot → áp dụng\n4. Chọn tất cả → áp dụng",
       "3 bot có hóa đơn",
       "- Bảng bot hiện đủ tên bot và LINE ID tương ứng\n"
       "- Chọn 1 bot: chỉ hiện hóa đơn của bot đó (kết hợp với filter plan/phương thức nếu có)\n"
       "- Chọn nhiều/tất cả: hiện hóa đơn của các bot đã chọn",
       note="Nguồn: r158-r163."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "STATE-002", "Normal",
       "Đóng modal filter bằng 閉じる: lần đầu không áp dụng, các lần sau giữ filter hiện tại",
       INV,
       "1. Mở modal filter lần đầu, chọn vài option, bấm「閉じる」→ quan sát danh sách\n"
       "2. Mở lại, áp dụng 1 filter thật\n"
       "3. Mở lại lần nữa, đổi option rồi bấm「閉じる」→ quan sát danh sách",
       "—",
       "- Lần đầu bấm 閉じる: KHÔNG áp dụng filter, màn hình giữ nguyên\n"
       "- Các lần sau bấm 閉じる: giữ nguyên kết quả của lần lọc hiện tại (không áp dụng thay đổi mới)",
       note="Nguồn: r164, r165. ⚠ Hành vi khác nhau giữa lần đầu và lần sau — dễ nhầm, cần Leader xác nhận "
            "đây là chủ ý hay lỗi; xem MT-23."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Có filter → nút đổi màu xanh + hiện nút X; bấm X xóa filter",
       INV,
       "1. Áp dụng 1 filter bất kỳ\n2. Quan sát nút「絞り込み」\n3. Bấm nút X cạnh nút filter\n"
       "4. Quan sát danh sách",
       "Filter theo plan standard",
       "- Sau khi lọc: nút chuyển màu xanh, hiện thêm nút X\n"
       "- Bấm X: xóa toàn bộ filter đã đặt, hiện lại toàn bộ hóa đơn",
       note="Nguồn: r148, r149."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "FUNC-002", "Normal",
       "Lọc nhiều lần liên tiếp / lọc → bỏ lọc → lọc lại đều cho kết quả đúng",
       INV + "\n- Có ≥ 3 bot và cả 2 phương thức thanh toán",
       "1. Lọc theo bot A → ghi kết quả\n2. Lọc lại theo bot B → ghi kết quả\n"
       "3. Bấm X bỏ lọc → ghi kết quả\n4. Lọc lại theo bot A + phương thức card → ghi kết quả",
       "3 lần lọc + 1 lần bỏ lọc",
       "Mỗi lần lọc trả đúng tập hóa đơn thỏa điều kiện hiện tại, "
       "không cộng dồn kết quả của lần lọc trước",
       note="Nguồn: r166, r167."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-001", "Normal",
       "Bảng chi tiết hóa đơn hiển thị đủ 8 cột đúng nguồn dữ liệu",
       INV + "\n- Đang mở chi tiết 1 tháng có ≥ 3 giao dịch",
       "1. Liệt kê các cột của bảng\n2. Đối chiếu từng ô với payment_histories",
       "3 giao dịch trong tháng",
       "- 8 cột: 契約(更新)日 | LINE公式アカウント名 | 利用料 (税込) | 契約プラン | 支払い | "
       "決済方法 | 備考 | 課金ID\n"
       "- Cột LINE公式アカウント名 hiện ảnh + tên đầy đủ, hover ra tooltip tên đầy đủ\n"
       "- 利用料 hiện số tiền + 円; 課金ID hiện univa_charge_id",
       note="Nguồn: r64, r70-r73, r84, r180-r203. Field Matrix #28-#32."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-001", "Normal",
       "Cột 契約プラン hiện 4 giá trị và giữ đúng plan TẠI THỜI ĐIỂM thanh toán",
       INV + "\n- Có hóa đơn của bot free, standard, pro và bill theo số bạn bè\n"
       "- Có 1 bot đã upgrade standard → pro sau khi đã bill vài kỳ",
       "1. Đọc cột 契約プラン của 4 loại hóa đơn\n"
       "2. Với bot đã upgrade: đọc plan của hóa đơn kỳ TRƯỚC upgrade và kỳ SAU upgrade",
       "4 loại hóa đơn + 1 bot đã upgrade",
       "- 4 giá trị:「スタンダード」「プロ」「従量課金」「フリー」\n"
       "- Hóa đơn kỳ trước upgrade giữ plan CŨ, kỳ sau hiện plan MỚI (không lấy plan hiện tại áp cho hết)",
       note="Nguồn: r75, r77, r110, r112, r193, r195."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-001", "Normal",
       "Cột 支払い giữ chu kỳ TẠI THỜI ĐIỂM bill dù sau đó đổi chu kỳ",
       "- Bot standard bill THÁNG đã bill kỳ 1, sau đó đổi sang bill NĂM\n"
       "- Bot standard bill NĂM đã bill kỳ 1, sau đó đổi sang bill THÁNG\n" + INV,
       "1. Đọc cột 支払い của hóa đơn kỳ 1 ở cả 2 bot\n"
       "2. Đối chiếu payment_histories.reason (plan_month / plan_year)",
       "2 bot, mỗi bot đổi chu kỳ sau khi đã bill",
       "- Bot bill tháng: hóa đơn kỳ 1 vẫn hiện「毎月払い」(reason = plan_month) sau khi đổi sang năm\n"
       "- Bot bill năm: hóa đơn kỳ 1 vẫn hiện「年間一括払い」(reason = plan_year) sau khi đổi sang tháng\n"
       "- Hóa đơn của bot free hiện「-」",
       note="Nguồn: r264-r266, r277-r292 (Bug #32649, 30/10/2025 — phí hiện 116.424 yên nhưng phương thức "
            "ghi trả theo tháng). Đây chính là bug gốc → Loại case Normal + ghi 'regression'."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-001", "Normal",
       "Cột 決済方法 hiện クレジットカード（下4桁）hoặc 銀行振込",
       INV + "\n- Có hóa đơn bill card (thẻ đuôi 1234) và hóa đơn bill transfer",
       "1. Đọc cột 決済方法 của 2 dòng",
       "type_bill IN(1,2) và type_bill=3",
       "- Bill card:「クレジットカード (下4桁 1234)」\n- Bill transfer:「銀行振込」",
       note="Nguồn: r80, r115, r198."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "DATA-001", "Normal",
       "Cột 備考 hiện 3 dạng ghi chú theo loại giao dịch",
       INV + "\n- Có hóa đơn: upgrade giữa kỳ (còn 15 ngày), bill theo số bạn bè 10~20万, enterprise 30 slot",
       "1. Đọc cột 備考 của 3 dòng\n2. Đối chiếu payment_histories.reason_detail và remain_day_upgrade",
       "3 loại hóa đơn như tiền đề",
       "- Upgrade:「アップグレード 日割り（15日分）」(có hậu tố 日分)\n"
       "- Max friend:「有効友だち10~20万人」\n- Enterprise:「おまとめプラン 30枠」",
       note="Nguồn: r82, r117, r200, r843 (SpecImprove #33149, 21/10/2025 thêm hậu tố 日分)."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "LIST-005", "Normal",
       "Sort theo cột 契約(更新)日 — mặc định + đảo chiều",
       INV + "\n- Tháng đang xem có ≥ 5 giao dịch với ngày khác nhau",
       "1. Ghi lại thứ tự mặc định\n2. Click mũi tên V → ghi thứ tự\n3. Click mũi tên ^ → ghi thứ tự",
       "5 giao dịch ngày 01, 05, 12, 20, 28",
       "- Mặc định: hiển thị theo ngày tạo mới nhất trước\n"
       "- Click V: sắp DESC\n- Click ^: sắp ASC\n- Hover mũi tên hiện hiệu ứng đậm",
       note="Nguồn: r64-r69, r182-r185. ⚠ r64 ghi 'Sắp xếp default: từ cũ nhất >> mới nhất' còn r67 ghi "
            "'Hiển thị theo ngày tạo mới nhất' — mâu thuẫn trong cùng 1 tab, xem MT-24."),

    tc("Lịch sử thanh toán — theo tháng & lọc", "LIST-003", "Normal",
       "Phân trang bảng hóa đơn: 10 / 20 / 50 / 100 và điều hướng < >",
       INV + "\n- Tháng đang xem có ≥ 120 giao dịch",
       "1. Lần lượt chọn 10, 20, 50, 100 bản ghi/trang và đếm số dòng\n"
       "2. Ở trang 1 click「<」\n3. Click「>」sang trang 2 rồi click số trang N",
       "≥ 120 giao dịch",
       "- 4 mức phân trang hiển thị đúng số dòng tương ứng\n"
       "- Ở trang đầu, nút「<」không click được; ở trang cuối, nút「>」không click được\n"
       "- Click số trang N: hiện đúng trang N",
       note="Nguồn: r125-r130, r250-r255."),

    # ═════════════ 27. Tải lãnh thụ thư ═════════════
    tc("Tải lãnh thụ thư", "UI-001", "Normal",
       "2 tab 一括発行 / 個別発行: mặc định 一括発行 được chọn",
       INV + "\n- Đang mở chi tiết 1 tháng có ≥ 3 hóa đơn",
       "1. Quan sát 2 tab\n2. Ghi lại tab đang chọn mặc định\n3. Chuyển sang tab 個別発行",
       "3 hóa đơn trong tháng",
       "- Mặc định tab「一括発行」được chọn, tab「個別発行」màu xám\n"
       "- Chuyển tab 個別発行: mỗi dòng hóa đơn có thêm checkbox",
       note="Nguồn: r58-r60, r86-r88."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Tab 一括発行: nút tải hàng loạt mở modal 領収書ダウンロード設定",
       INV + "\n- Đang ở tab 一括発行 của tháng có 3 hóa đơn",
       "1. Hover nút tải hàng loạt\n2. Click nút\n3. Quan sát modal",
       "3 hóa đơn",
       "- Hover: nút đậm lên\n- Click: mở modal「領収書ダウンロード設定」",
       note="Nguồn: r61, r62."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Abnormal",
       "Tab 個別発行: không tích checkbox nào → nút tải hàng loạt bị disable",
       INV + "\n- Đang ở tab 個別発行",
       "1. Không tích checkbox nào\n2. Quan sát nút tải hàng loạt\n"
       "3. Tích 1 checkbox → quan sát lại\n4. Bỏ tích, tích checkbox all → quan sát lại",
       "3 hóa đơn",
       "- Không tích: nút disable\n- Tích 1 hoặc tích all: nút enable",
       note="Nguồn: r90-r92, r173-r175."),

    tc("Tải lãnh thụ thư", "LIST-006", "Normal",
       "Checkbox all chỉ chọn hết dòng của TRANG hiện tại",
       INV + "\n- Tháng có ≥ 30 hóa đơn, phân trang 10/trang, đang ở tab 個別発行",
       "1. Ở trang 1, tích checkbox ở tiêu đề (chọn all)\n2. Sang trang 2\n"
       "3. Quan sát các checkbox ở trang 2",
       "30 hóa đơn, phân trang 10",
       "- Trang 1: 10 dòng đều được tích\n"
       "- Trang 2: các checkbox KHÔNG tự động tích",
       note="Nguồn: r103, r186."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Tải riêng lẻ: nút download từng dòng, disable với hóa đơn plan free",
       INV + "\n- Tháng có hóa đơn của bot standard/pro và bot free",
       "1. Quan sát nút download ở dòng hóa đơn standard/pro\n2. Hover nút\n"
       "3. Quan sát nút ở dòng hóa đơn plan free\n4. Click nút của dòng standard",
       "Hóa đơn standard, pro và free",
       "- Dòng standard/pro: nút download enable, hover ra tooltip「領収書ダウンロード」\n"
       "- Dòng plan free: nút download DISABLE\n- Click nút: mở modal「領収書ダウンロード設定」",
       note="Nguồn: r121-r123, r204-r207."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Modal 領収書ダウンロード設定: ô 宛名 free text, không giới hạn, không bắt buộc",
       INV,
       "1. Mở modal tải hóa đơn\n2. Đọc nhãn ô 宛名\n3. Nhập chuỗi 500 ký tự tiếng Nhật + ký tự đặc biệt\n"
       "4. Xóa trống rồi bấm tải",
       "Chuỗi 500 ký tự hỗn hợp; và chuỗi rỗng",
       "- Nhãn ô hiện「宛名 未入力の場合は、宛名が空欄で発行されます。」, không có placeholder\n"
       "- Nhập được free text, không bị chặn độ dài, cho phép trùng với lần trước\n"
       "- Bỏ trống vẫn tải được (không required)",
       note="Nguồn: r211-r217."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Setting 宛名の自動入力: bật/tắt điều khiển ô nhập tên tự động",
       INV,
       "1. Mở modal tải hóa đơn → khu「宛名の自動入力」\n2. Đọc giá trị mặc định của「自動入力の利用」\n"
       "3. Quan sát ô「宛名をご入力ください」khi đang「利用しない」\n"
       "4. Bật sang「利用する」và quan sát lại ô nhập",
       "—",
       "- Mặc định「利用しない」(không sử dụng)\n"
       "- Khi 利用しない: ô nhập bị disable, không click được, chữ tiêu đề màu #888888\n"
       "- Khi 利用する: ô nhập enable, chữ tiêu đề màu #222222",
       note="Nguồn: r218-r221."),

    tc("Tải lãnh thụ thư", "DATA-004", "Normal",
       "Lưu 宛名の自動入力 → lần tải sau ô 宛名 tự điền sẵn giá trị đã lưu",
       INV,
       "1. Mở modal, bật「利用する」, nhập「株式会社テスト」, bấm「保存する」\n"
       "2. Đóng modal, mở lại modal tải hóa đơn của 1 dòng khác\n3. Quan sát ô 宛名",
       "宛名 tự động =「株式会社テスト」",
       "- Lưu thành công\n- Lần mở modal sau: ô「宛名」tự điền sẵn「株式会社テスト」",
       note="Nguồn: r228-r230."),

    tc("Tải lãnh thụ thư", "STATE-002", "Normal",
       "Bấm 閉じる ở màn setting 宛名の自動入力 → không lưu, quay lại modal tải",
       INV,
       "1. Mở setting「宛名の自動入力」, bật 利用する và nhập「テスト」\n2. Bấm「閉じる」\n"
       "3. Mở lại setting và quan sát giá trị",
       "宛名 =「テスト」nhập nhưng không save",
       "- Quay lại modal「領収書ダウンロード設定」\n- Giá trị vừa nhập KHÔNG được lưu",
       note="Nguồn: r231-r233."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Radio 敬称: mặc định 御中, tải PDF hiện đúng danh xưng đã chọn",
       INV,
       "1. Mở modal tải, quan sát radio 敬称 mặc định\n"
       "2. Nhập 宛名「株式会社テスト」, chọn 御中 → tải và mở PDF\n"
       "3. Lặp lại với「様」\n4. Lặp lại với「無し」",
       "宛名 =「株式会社テスト」; 3 danh xưng",
       "- Mặc định radio đang chọn「御中」\n"
       "- PDF lần 1:「株式会社テスト 御中」· lần 2:「株式会社テスト 様」· lần 3: chỉ「株式会社テスト」\n"
       "- Không có text「株式会社」thừa do hệ thống tự thêm",
       note="Nguồn: r237-r245, r327-r335 (Bug KH #32953, 01/12/2025). RULE-06: mở file PDF để đối chiếu."),

    tc("Tải lãnh thụ thư", "FUNC-003", "Normal",
       "Chọn danh xưng A rồi đổi sang B trước khi lưu → tải theo lựa chọn CUỐI CÙNG",
       INV,
       "1. Mở modal, chọn 御中\n2. Đổi sang 様\n3. Bấm tải và mở PDF",
       "Chọn lần lượt 御中 → 様",
       "PDF hiện danh xưng「様」(lựa chọn cuối cùng)",
       note="Nguồn: r241."),

    tc("Tải lãnh thụ thư", "DATA-001", "Normal",
       "Hóa đơn tải về hiển thị cột 決済方法 đúng phương thức thanh toán",
       INV + "\n- Có hóa đơn bill card (thẻ 1234) và hóa đơn bill transfer",
       "1. Tải hóa đơn của giao dịch bill card, mở PDF, tìm mục 決済方法\n"
       "2. Tải hóa đơn của giao dịch bill transfer, mở PDF",
       "2 hóa đơn: card đuôi 1234 và transfer",
       "- PDF có mục tiêu đề「決済方法」\n"
       "- Bill card:「クレジットカード（1234）」\n- Bill transfer:「銀行振込」",
       note="Nguồn: r829-r831 (SpecImprove #33313, 08/11/2025). RULE-06: mở PDF."),

    tc("Tải lãnh thụ thư", "REG-001", "Normal",
       "Cột 決済方法 + danh xưng đúng ở TẤT CẢ lối tải hóa đơn",
       INV + "\n- Có hóa đơn ở nhiều trạng thái hợp đồng",
       "1. Tải hàng loạt theo năm\n2. Tải đơn lẻ theo năm\n3. Tải theo tháng với 20 bản ghi\n"
       "4. Tải theo tháng với 3 bản ghi\n5. Tải với 3 danh xưng khác nhau\n"
       "6. Tải hóa đơn cũ (trước khi thêm cột)\n"
       "7. Tải từ màn quản lý hợp đồng: case chờ chuyển khoản / chờ tài khoản / bill transfer",
       "9 lối tải như phần bước",
       "Cả 9 lối tải đều: hiện đúng danh xưng, có cột 決済方法 với giá trị đúng "
       "(クレジットカード（xxxx）hoặc 銀行振込)",
       note="Nguồn: r832-r840 (9 dòng cùng expected → gộp, liệt kê đủ 9 lối tải). Ghi 'regression'."),

    tc("Tải lãnh thụ thư", "PERF-001", "Boundary",
       "Tải toàn bộ hóa đơn khi số bản ghi lớn (10/20/50/100 trang)",
       INV + "\n- Tài khoản có lượng hóa đơn đủ tạo 100 trang ở mức 10 bản ghi/trang",
       "1. Chọn 全期間, tích checkbox all\n2. Bấm tải hàng loạt ở từng mức phân trang 10/20/50/100\n"
       "3. Kiểm tra số hóa đơn trong file tải về so với tổng bản ghi",
       "≥ 1000 hóa đơn",
       "- Tải được toàn bộ hóa đơn (không chỉ trang hiện tại)\n"
       "- Nếu không gộp hết vào 1 file thì tải nhiều file riêng biệt cùng lúc\n"
       "- Không timeout, không mất bản ghi",
       env="PRODUCTION",
       note="Nguồn: r93, r176, r256-r259. RULE-08: performance → PRODUCTION."),

    tc("Tải lãnh thụ thư", "SEC-001", "Abnormal",
       "Double-click nút tải → xử lý đúng, không sinh file rác",
       INV,
       "1. Double-click nút download của 1 dòng hóa đơn\n2. Đếm số file tải về\n"
       "3. Double-click nút tải hàng loạt\n4. Đếm số lần tải",
       "1 hóa đơn và 1 nhóm hóa đơn",
       "- Ghi nhận đúng hành vi thực tế: corpus ghi double-click tải 2 lần cùng hóa đơn\n"
       "- Không sinh lỗi, không tạo bản ghi thừa trong payment_histories",
       note="Nguồn: r124, r178. ⚠ Corpus coi 'tải 2 lần' là expected — cần Leader chốt đây có phải hành vi "
            "mong muốn không (thường nên chặn double submit); xem MT-25."),

    tc("Tải lãnh thụ thư", "DATA-001", "Normal",
       "Nội dung file 領収書: ngày phát hành, phân trang, danh sách khoản bill, tổng tiền",
       INV + "\n- Tháng có ≥ 25 giao dịch (để hóa đơn có nhiều trang)",
       "1. Tải hóa đơn gộp của tháng\n2. Mở PDF, đọc mục ngày phát hành\n"
       "3. Đọc chỉ số trang\n4. Đếm số bản ghi trang 1 và các trang sau\n5. Đọc mục 合計",
       "≥ 25 giao dịch trong tháng",
       "- Ngày phát hành = ngày tải, format「2026年〇〇月〇〇日」\n"
       "- Chỉ số trang format「1/3ページ」\n"
       "- Trang đầu tối đa 10 bản ghi, từ trang 2 tối đa 20 bản ghi/trang\n"
       "- Mục 合計 = tổng tiền các khoản bill trong tháng (cộng tay khớp)",
       note="Nguồn: tab「Task nhỏ」r10-r13 (Feature #29722, 23/04/2025). RULE-06 + RULE-07."),

    tc("Tải lãnh thụ thư", "FUNC-001", "Normal",
       "Chưa chọn bot nào vẫn vào được màn hóa đơn và thao tác bình thường",
       "- Đăng nhập owner nhưng CHƯA chọn bot nào ở header",
       "1. Mở /basic/payment-history\n2. Thử lọc và tải 1 hóa đơn",
       "Chưa select bot",
       "Màn hóa đơn mở bình thường, lọc và tải hóa đơn hoạt động đúng",
       note="Nguồn: r260."),

    # ═════════════ 28. Phát hành báo giá ═════════════
    tc("Phát hành báo giá", "UI-001", "Normal",
       "Màn 見積書発行: form 4 bước cho plan standard/pro",
       "- Đăng nhập admin (không phải staff)\n- Mở /admin/plan-estimation",
       "1. Quan sát form\n2. Liệt kê 4 bước và loại input của từng bước",
       "—",
       "- ① 宛名を入力: textbox + selectbox danh xưng (御中 mặc định / 様 / なし)\n"
       "- ② お申し込み予定プランを選択: dropdown, default「選択してください」, "
       "option スタンダード / プロ / おまとめ\n"
       "- ③ 決済期間を選択: radio 毎月払い (default) / 年間一括払い\n"
       "- ④ 接続枠数を選択: spinbutton số, default = 1",
       note="Nguồn: tab「Estimation」r3-r15. TC gốc CHỈ CÓ TIÊU ĐỀ, kết quả mong đợi do AI viết lại từ "
            "nội dung tiêu đề + feature-spec.md §2 SCR-BLP-05 — CẦN LEADER XÁC NHẬN."),

    tc("Phát hành báo giá", "FUNC-003", "Abnormal",
       "Ô 宛名 không validate độ dài → nhập chuỗi rất dài phải không vỡ layout",
       "- Mở /admin/plan-estimation",
       "1. Nhập chuỗi 500 ký tự vào ô 宛名\n2. Quan sát layout form\n3. Bấm tính tiền và tải PDF\n"
       "4. Mở PDF xem phần tên",
       "Chuỗi 500 ký tự",
       "- Không bị chặn nhập (không validate độ dài)\n"
       "- Form và PDF KHÔNG bị vỡ layout / tràn chữ",
       note="Nguồn: tab Estimation r3 (ghi chú của tester:「nhập số lượng lớn bị vỡ layout」). "
            "⚠ Đây là lỗi đã ghi nhận 09/2023 — CẦN VERIFY LẠI, dự kiến FAIL → raise bug nếu tái hiện."),

    tc("Phát hành báo giá", "FUNC-003", "Abnormal",
       "Chưa chọn plan mà bấm 料金を計算 → không tính được",
       "- Mở /admin/plan-estimation",
       "1. Để dropdown plan ở「選択してください」\n2. Bấm「料金を計算」",
       "Plan chưa chọn",
       "Không tính ra số tiền / hiện thông báo yêu cầu chọn plan; không tạo được PDF",
       note="Nguồn: tab Estimation r9 (chỉ có tiêu đề). Kết quả mong đợi do AI viết — CẦN LEADER XÁC NHẬN."),

    tc("Phát hành báo giá", "DATA-002", "Abnormal",
       "Ô số slot: chặn số thập phân và số âm; bỏ trống hiểu là 0",
       "- Mở /admin/plan-estimation, đã chọn plan standard",
       "1. Nhập「1.5」vào ô số slot\n2. Nhập「-1」\n3. Xóa trống ô rồi bấm tính tiền",
       "Giá trị: 1.5 · -1 · rỗng",
       "- Số thập phân và số âm bị chặn không nhập được\n- Bỏ trống: hệ thống hiểu là 0",
       note="Nguồn: tab Estimation r13, r14."),

    tc("Phát hành báo giá", "DATA-002", "Normal",
       "Tính tiền standard/pro theo chu kỳ và số slot",
       "- Mở /admin/plan-estimation trên PRODUCTION",
       "1. Chọn standard + 毎月払い + 1 slot → bấm 料金を計算\n"
       "2. Chọn pro + 毎月払い + 1 slot\n3. Chọn standard + 年間一括払い + 1 slot\n"
       "4. Chọn pro + 年間一括払い + 1 slot\n5. Đổi số slot thành 3 và kiểm tra số tiền × 3",
       "4 tổ hợp plan × chu kỳ, số slot 1 và 3",
       "- Số tiền hiển thị ở「お支払い金額（税込）」đúng theo bảng giá của từng tổ hợp\n"
       "- Đổi số slot: tổng tiền = đơn giá × số slot",
       env="PRODUCTION",
       note="Nguồn: tab Estimation r16-r19. ⚠ Giá trong TC gốc (09/2023: standard tháng 4.500, năm 48.600) "
            "KHÁC bảng giá hiện hành (10.780 / 116.424) — TC > 2 năm tuổi, CẦN VERIFY LẠI giá. Xem MT-26."),

    tc("Phát hành báo giá", "DATA-002", "Normal",
       "Plan enterprise: hiện thêm dropdown loại EP + selectbox slot 10~100 (default 10)",
       "- Mở /admin/plan-estimation trên PRODUCTION",
       "1. Chọn plan「おまとめ」\n2. Quan sát dropdown phụ và ô số slot\n"
       "3. Chọn EP standard + 毎月払い + 10 slot → tính tiền\n"
       "4. Chọn EP pro + 年間一括払い + 10 slot → tính tiền",
       "EP standard và EP pro, 10 slot",
       "- Hiện dropdown phụ: 選択してください (default) / スタンダード / プロ\n"
       "- Ô số slot chuyển thành selectbox 10→100, default 10\n"
       "- Số tiền hiển thị đúng theo bảng giá EP hiện hành",
       env="PRODUCTION",
       note="Nguồn: tab Estimation r25-r33. ⚠ Giá trong TC gốc (EP standard tháng 40.500) là giá 2023 — "
            "CẦN VERIFY LẠI. Xem MT-26."),

    tc("Phát hành báo giá", "DATA-001", "Normal",
       "File PDF 見積書: đủ tiêu đề, danh xưng, tổng tiền, ngày phát hành, thông tin công ty",
       "- Đã tính tiền cho standard + 毎月払い + 1 slot, 宛名 =「株式会社テスト」danh xưng 御中",
       "1. Bấm「見積書をダウンロード」\n2. Mở file PDF\n"
       "3. Đọc: tiêu đề, danh xưng, 御見積金額, 発行日, thông tin công ty",
       "宛名「株式会社テスト」+ 御中",
       "- Tiêu đề「見積書」\n- Danh xưng「株式会社テスト 御中」\n"
       "- 御見積金額 khớp số tiền đã tính ở màn hình\n- 発行日 = ngày tải, đúng format\n"
       "- Thông tin công ty:「株式会社ミショナ 〒150-0043 東京都渋谷区道玄坂1丁目10番8号 "
       "渋谷道玄坂東急ビル2F−C」",
       note="Nguồn: tab Estimation r38-r42. RULE-06: bắt buộc mở PDF."),

    tc("Phát hành báo giá", "DATA-002", "Normal",
       "File PDF: tên item, số lượng, đơn giá (đã trừ 10%), thành tiền, VAT, tổng",
       "- Đã tạo báo giá standard + 年間一括払い + 3 slot",
       "1. Tải PDF và mở\n2. Đọc dòng 品目, 数量, 単価, 金額\n3. Đọc 小計, 消費税(内税), 合計\n"
       "4. Tự tính: 単価 = đơn giá trên tool − 10%; 金額 = 単価 × 数量; 消費税 = 10% số tiền",
       "standard năm, 3 slot",
       "- 品目 =「スタンダードプラン 年間一括払い」(đúng theo plan × chu kỳ)\n"
       "- 数量 = 3\n- 単価 = đơn giá trên tool trừ 10%\n- 金額 = 単価 × 3\n"
       "- 消費税 (内税) = 10% số tiền; 合計 = 小計 + VAT (khớp phép tính tay)",
       env="PRODUCTION",
       note="Nguồn: tab Estimation r43-r58. RULE-08: liên quan tiền → PRODUCTION."),

    tc("Phát hành báo giá", "DATA-001", "Normal",
       "File PDF: 8 tên item tương ứng 8 tổ hợp plan × chu kỳ",
       "- Mở /admin/plan-estimation",
       "1. Lần lượt tạo báo giá cho 8 tổ hợp và mở PDF đọc dòng 品目",
       "8 tổ hợp: standard/pro × tháng/năm; EP-standard/EP-pro × tháng/năm",
       "- スタンダードプラン 毎月払い / 年間一括払い\n- プロプラン 毎月払い / 年間一括払い\n"
       "- おまとめプラン（スタンダード）毎月払い / 年間一括払い\n"
       "- おまとめプラン（プロ）毎月払い / 年間一括払い",
       note="Nguồn: tab Estimation r43-r50 (8 dòng cùng dạng → gộp, liệt kê đủ 8 tổ hợp)."),

    tc("Phát hành báo giá", "DATA-001", "Normal",
       "File PDF: mục 備考 hiện đúng nội dung cố định",
       "- Đã tạo 1 báo giá bất kỳ",
       "1. Mở PDF, đọc mục「備考」",
       "—",
       "Hiện text「請求書の発行は行なっておりません。料金プランが変更された場合、本見積書に記載の"
       "金額は無効となります。L Message利用料金は株式会社ユニヴァ・ペイキャストの提供…」",
       note="Nguồn: tab Estimation r59 (chỉ có tiêu đề, nội dung trích từ cột path). "
            "Cần đối chiếu nguyên văn với bản hiện hành."),

    tc("Phát hành báo giá", "FUNC-003", "Normal",
       "Danh xưng trên 見積書 hoạt động như màn hóa đơn (3 giá trị)",
       "- Mở /admin/plan-estimation",
       "1. Tạo báo giá với 宛名 + 御中 → mở PDF\n2. Lặp lại với 様\n3. Lặp lại với なし\n"
       "4. Lặp lại 3 lần trên nhưng bỏ trống 宛名",
       "宛名 có/không × 3 danh xưng = 6 tổ hợp",
       "- Có tên: hiện「<tên> 御中」/「<tên> 様」/ chỉ「<tên>」\n"
       "- Không tên: chỉ hiện「御中」/「様」/ không hiện gì\n- Không có text「株式会社」thừa phía trước",
       note="Nguồn: r336-r341 (Bug KH #32953 áp cho cả màn Estimation)."),
]
