# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 5-11: mua mới / upgrade hợp đồng, nhập thẻ, chuyển khoản, hủy chuyển khoản.

Nguồn chính: TCsLine_Bill tiền_Improve2025 → tab「Màn hình bill tiền」(12/2025 → 07/2026,
647 dòng, 531 TC lá) và tab「List main case」(347 dòng — bộ main case).
Bổ sung: TCsLine_Bill tiền → tab「Improve bill tiền 12/2024」(12/2024 → 01/2025, 405 TC lá),
         tab「Bill tiền univapay: 3D secure」(03/2025), tab「Feature #36994」(07/2026 — お住まい).
"""
from _common import tc

PLAN = ("- Đăng nhập LME bằng tài khoản owner\n"
        "- Mở màn chọn plan (click「LINE公式アカウント追加」ở màn list bot)")
NEW = PLAN + "\n- Chưa có slot trống của plan định mua"

S2 = [
    # ═════════════ 5. Màn chọn plan ═════════════
    tc("Màn chọn plan", "FUNC-001", "Normal",
       "3 lối vào đều mở đúng màn chọn plan",
       "- Đăng nhập owner có ít nhất 1 bot free",
       "1. Click nút「LINE公式アカウント追加」\n2. Quay lại, vào màn add bot rồi click\n"
       "3. Quay lại, click nút upgrade của 1 bot\n4. So sánh 3 màn mở ra",
       "3 lối vào: nút thêm LOA / màn add bot / nút upgrade",
       "Cả 3 lối vào đều mở màn「プラン選択」với cùng bố cục và cùng bảng giá",
       note="Nguồn: r5-r7 (3 dòng cùng expected → gộp, liệt kê đủ 3 lối vào)."),

    tc("Màn chọn plan", "UI-001", "Normal",
       "Title màn chọn plan + toggle chu kỳ mặc định 年間払い 10%OFF",
       PLAN,
       "1. Đọc tiêu đề màn hình\n2. Quan sát toggle chu kỳ thanh toán ở trạng thái mặc định",
       "—",
       "- Tiêu đề「プラン選択」\n- Toggle mặc định đang chọn「年間払い 10%OFF」",
       note="Nguồn: r32, r33."),

    tc("Màn chọn plan", "DATA-002", "Normal",
       "Toggle 年間払い 10%OFF ↔ 毎月払い → giá của tất cả plan đổi tương ứng",
       PLAN,
       "1. Chọn「年間払い 10%OFF」→ ghi lại giá standard và pro\n"
       "2. Chuyển sang「毎月払い」→ ghi lại giá standard và pro\n3. Đối chiếu",
       "Môi trường PRODUCTION: standard 10.780円/tháng, pro 33.000円/tháng",
       "- 年間払い: standard hiện 9.702円/1 tháng, pro hiện 29.700円/1 tháng (giảm 10% so với giá niêm yết)\n"
       "- 毎月払い: standard 10.780円/1 tháng, pro 33.000円/1 tháng (giá niêm yết)",
       env="PRODUCTION",
       note="Nguồn: r34, r35, r38, r39, r44, r45. ⚠ Giá trên dev/staging khác PRODUCTION "
            "(standard 4.050/4.500) → RULE-08: giá tiền phải verify trên PRODUCTION. Xem MT-06."),

    tc("Màn chọn plan", "UI-001", "Normal",
       "Khối cuối màn (お申し込み時の注意点) đồng bộ giá và trạng thái nút với khối đầu màn",
       PLAN,
       "1. Ghi lại giá + trạng thái nút của 3 plan ở khối đầu màn\n"
       "2. Cuộn xuống khối「お申し込み時の注意点」\n3. Đối chiếu từng plan",
       "3 plan: free / standard / pro",
       "- Plan free bị disable ở đầu màn thì cuối màn cũng disable\n"
       "- Giá của standard/pro ở 2 khối giống hệt nhau\n- Switch chu kỳ thì cả 2 khối cùng đổi",
       note="Nguồn: r73, r74."),

    tc("Màn chọn plan", "FUNC-001", "Normal",
       "Nút お申し込み時の注意点をもっと見る → auto scroll tới đúng mục",
       PLAN,
       "1. Click nút「お申し込み時の注意点をもっと見る」",
       "—",
       "Trang tự cuộn tới mục「お申し込み時の注意点」, không mở tab mới",
       note="Nguồn: r50."),

    tc("Màn chọn plan", "FUNC-001", "Normal",
       "Nút 比較表をもっと見る → mở đầy đủ bảng so sánh tính năng",
       PLAN,
       "1. Quan sát khối「プラン別機能比較表」ở trạng thái mặc định\n2. Click「比較表をもっと見る」",
       "—",
       "- Mặc định: bảng so sánh bị thu gọn / không hiển thị đầy đủ\n- Sau click: hiện full bảng so sánh",
       note="Nguồn: r54, r55."),

    tc("Màn chọn plan", "FUNC-001", "Normal",
       "Các hyperlink liên hệ mở đúng URL ở tab mới",
       PLAN,
       "1. Click「お問い合わせフォーム」\n2. Quay lại, click「おまとめ割引についてお問い合わせ」",
       "—",
       "- お問い合わせフォーム → mở Google Form "
       "https://docs.google.com/forms/d/e/1FAIpQLSffFQMzqWEMZ0rx8tjzdb8IMXUdA1Td8RQcbIYHiPYvxNraPg/viewform\n"
       "- おまとめ割引 → mở tab mới https://tayori.com/form/e7166cd66118f681415917e9c952befc3fcbaffa",
       note="Nguồn: r51, r52, r53."),

    tc("Màn chọn plan", "FUNC-001", "Normal",
       "Chọn plan enterprise → mở form liên hệ OEM, không đi tới màn thanh toán",
       PLAN,
       "1. Chọn plan おまとめ (enterprise)\n2. Quan sát hành vi",
       "—",
       "Mở link form OEM https://tayori.com/form/e7166cd66118f681415917e9c952befc3fcbaffa; "
       "KHÔNG mở màn xác nhận plan / màn nhập thẻ",
       note="Nguồn: r383 (Màn hình bill tiền). ⚠ Đối lập với Feature #37085 (06/2026) cho phép mua "
            "enterprise qua /admin/confirm-contract-standard/enterprise/month — xem MT-07."),

    # ═════════════ 6. Rule slot trống & bot free ═════════════
    tc("Rule slot trống & bot free", "FUNC-004", "Normal",
       "User tạo TRƯỚC 01/07/2021 → tạo được không giới hạn bot free",
       "- Đăng nhập user có users.created_at < 2021-07-01, đã có 1 bot free",
       "1. Mở màn chọn plan\n2. Click plan free\n3. Hoàn tất add bot free",
       "users.created_at = 2020-05-10, đã có 1 bot free",
       "Cho phép add, mở màn /admin/bot-add-v2 và tạo được bot free thứ 2 thành công",
       note="Nguồn: r356, r357 (Màn hình bill tiền)."),

    tc("Rule slot trống & bot free", "FUNC-004", "Abnormal",
       "User tạo SAU 01/07/2021 đã có 1 bot free → nút plan free bị disable",
       "- Đăng nhập user có users.created_at >= 2021-07-01, đã có 1 bot free",
       "1. Mở màn chọn plan\n2. Quan sát nút của plan free",
       "users.created_at = 2024-01-15, đã có 1 bot free",
       "Nút plan free hiển thị「ご利用中のプランです」và bị disable, không mở được màn add bot free",
       note="Nguồn: r17, r391, r359 (báo lỗi 現在のプランは利用できない機能…). "
            "⚠ Corpus có 2 mô tả khác nhau (disable nút vs báo lỗi) — xem MT-08."),

    tc("Rule slot trống & bot free", "FUNC-004", "Normal",
       "Bot free đã upgrade lên plan khác → nút ご利用中のプランです enable trở lại, click sang màn tạo bot",
       "- Đăng nhập user tạo sau 01/07/2021\n- Bot free duy nhất đã được upgrade lên standard",
       "1. Mở màn chọn plan\n2. Quan sát nút plan free\n3. Click nút",
       "Bot free cũ đã upgrade → user hiện không còn bot free nào đang dùng",
       "- Nút「ご利用中のプランです」ở trạng thái enable\n- Click → mở màn tạo bot free",
       note="Nguồn: r36, r37, r57, r58."),

    tc("Rule slot trống & bot free", "FUNC-004", "Normal",
       "User chưa có bot free + không có slot trống → chọn plan trả phí hiện cảnh báo nhưng vẫn cho mua",
       "- Đăng nhập user chưa có bot free nào, không có slot trống nào",
       "1. Mở màn chọn plan\n2. Chọn plan standard (hoặc pro)\n3. Đọc message\n4. Bấm OK",
       "0 bot free, 0 slot trống",
       "- Hiện message「フリープランが利用可能ですが有料プランの契約操作を…」\n"
       "- Bấm OK: vẫn mở được popup/màn xác nhận plan và mua được plan trả phí",
       note="Nguồn: r11, r385, r3 (List main case)."),

    tc("Rule slot trống & bot free", "FUNC-004", "Abnormal",
       "Đang có slot trống của plan nào thì KHÔNG mua thêm slot của plan đó (4 tổ hợp)",
       "- Đăng nhập user tạo sau 01/07/2021 đã có 1 bot free\n"
       "- Chuẩn bị lần lượt 4 trạng thái slot trống: standard / pro / enterprise-standard / enterprise-pro",
       "1. Với mỗi trạng thái slot trống, mở màn chọn plan\n"
       "2. Chọn plan CÙNG loại với slot đang trống\n3. Đọc message lỗi",
       "4 tổ hợp: slot trống standard→chọn standard; pro→pro; EP-standard→standard; EP-pro→pro",
       "Cả 4 tổ hợp đều chặn, hiện message「{tên plan có slot}プランの未接続枠が存在する状態での"
       "有料プラン契約はできません。」và KHÔNG mở màn xác nhận plan",
       note="Nguồn: r19, r24, r25, r30, r393, r396, r397, r400 (cùng 1 quy tắc, 4 tổ hợp cùng expected → gộp). "
            "SpecChange #30442 (24/06/2025): EP-standard chặn cả standard."),

    tc("Rule slot trống & bot free", "FUNC-004", "Normal",
       "Có slot trống plan A → vẫn mua được plan B khác loại",
       "- Đăng nhập user tạo sau 01/07/2021 đã có 1 bot free\n- Đang có 1 slot trống standard",
       "1. Mở màn chọn plan\n2. Chọn plan pro\n3. Quan sát hành vi",
       "Slot trống = standard; plan chọn = pro",
       "Cho phép mua: mở màn xác nhận plan pro, không hiện message chặn",
       note="Nguồn: r20, r21, r394, r395, r398, r399."),

    tc("Rule slot trống & bot free", "FUNC-004", "Abnormal",
       "Có slot trống của CẢ standard và pro → chọn plan nào cũng bị chặn",
       "- Đăng nhập user đang có 1 slot trống standard VÀ 1 slot trống pro",
       "1. Mở màn chọn plan\n2. Chọn standard → đọc message\n3. Chọn pro → đọc message",
       "2 slot trống: standard + pro",
       "Cả 2 lựa chọn đều bị chặn với message「{tên plan có slot}プランの未接続枠が存在する状態での"
       "有料プラン契約はできません。」",
       note="Nguồn: r31, r401."),

    tc("Rule slot trống & bot free", "FUNC-005", "Normal",
       "Enterprise: mua slot mới ở màn quản lý slot → tăng số slot của hợp đồng EP",
       "- Đăng nhập owner của hợp đồng enterprise 10 slot\n"
       "- Mở /admin/bots/list-bot-enterprise/{id}",
       "1. Bấm tăng số slot của enterprise\n2. Hoàn tất thanh toán\n"
       "3. Quay lại màn chi tiết hợp đồng và kiểm tra lịch sử thao tác",
       "Hợp đồng EP 10 slot → tăng lên 11 slot",
       "- Số slot hợp đồng tăng đúng, màn detail hiện「おまとめ割引 11枠」\n"
       "- Lịch sử thao tác hợp đồng ghi nhận thao tác thay đổi slot",
       note="Nguồn: r265, r266 (Quản lý hợp đồng)."),

    # ═════════════ 7. Xác nhận plan — mua mới ═════════════
    tc("Xác nhận plan — mua mới", "UI-001", "Normal",
       "Step 1 mua mới: title + 対象アカウント + plan đã chọn hiển thị đúng",
       NEW,
       "1. Chọn plan standard →「このプランを利用する」\n2. Đọc title, mục 対象アカウント và 選択したプラン\n"
       "3. Quay lại, lặp với plan pro",
       "2 plan: standard và pro",
       "- standard: title「スタンダード プランを利用する」, 選択したプラン =「スタンダードプラン」\n"
       "- pro: title「プロプランを利用する」, 選択したプラン =「プロプラン」\n"
       "- 対象アカウント hiện「新規LINE公式アカウント接続」",
       note="Nguồn: r78-r82."),

    tc("Xác nhận plan — mua mới", "UI-005", "Normal",
       "Đang ở step 1, click sang step 2/3 trên thanh bước → bị disable",
       NEW,
       "1. Ở step 1, click vào nhãn step 2\n2. Click vào nhãn step 3",
       "—",
       "Cả 2 nhãn step 2 và step 3 đều disable, không click được, vẫn ở step 1",
       note="Nguồn: r83, r84."),

    tc("Xác nhận plan — mua mới", "FUNC-003", "Abnormal",
       "Bỏ chọn 主管理者 → chặn và báo lỗi",
       NEW,
       "1. Ở step 1, bỏ chọn 主管理者\n2. Bấm「決済に進む」",
       "主管理者 rỗng",
       "Hiện message「主管理者を選択してください。」, không sang step 2",
       note="Nguồn: r85."),

    tc("Xác nhận plan — mua mới", "FUNC-003", "Normal",
       "Chọn 主管理者 nhiều lần → luôn giữ đúng owner cuối cùng",
       NEW + "\n- Tài khoản có ≥ 3 user để chọn làm 主管理者",
       "1. Chọn owner A\n2. Chọn owner B\n3. Chọn lại owner C\n4. Quan sát giá trị hiển thị",
       "3 user A, B, C",
       "Ô 主管理者 hiển thị đúng owner C (lựa chọn cuối cùng)",
       note="Nguồn: r86."),

    tc("Xác nhận plan — mua mới", "DATA-001", "Normal",
       "Chu kỳ bill mặc định = 毎月払い; đổi sang năm thì mục お支払い方法 đổi theo",
       NEW,
       "1. Quan sát tab chu kỳ mặc định\n2. Chọn tab bill năm\n3. Đọc mục お支払い方法",
       "—",
       "- Mặc định là bill tháng, お支払い方法 hiện「月払い」\n"
       "- Chọn bill năm: hiển thị tab năm, お支払い方法 hiện「年間一括払い」",
       note="Nguồn: r87-r89."),

    tc("Xác nhận plan — mua mới", "DATA-002", "Normal",
       "Tick 2年分まとめて払い → số tiền = giá năm × 2",
       NEW,
       "1. Chọn tab bill năm\n2. Ghi lại số tiền お支払い総額\n3. Tick「2年分まとめて払い」\n4. So sánh số tiền",
       "Plan standard bill năm (PRODUCTION: 116.424円)",
       "Số tiền hiển thị = 232.848円 (税込) = đúng gấp đôi giá 1 năm",
       env="PRODUCTION",
       note="Nguồn: r90, r122, r123. RULE-08: bill tiền phải verify trên PRODUCTION."),

    tc("Xác nhận plan — mua mới", "DATA-001", "Normal",
       "Bill tháng chỉ có card; bill năm có card + chuyển khoản",
       NEW,
       "1. Chọn tab bill tháng → liệt kê option phương thức thanh toán\n"
       "2. Chọn tab bill năm → liệt kê option",
       "—",
       "- Bill tháng: chỉ có option「クレジットカード」\n"
       "- Bill năm: có「クレジットカード」và「銀行振込（請求書の発行ができます）」",
       note="Nguồn: r91, r92, r40, r41."),

    tc("Xác nhận plan — mua mới", "STATE-002", "Normal",
       "Chọn transfer rồi quay lại tab bill tháng → tự reset về thanh toán thẻ",
       NEW,
       "1. Chọn tab bill năm\n2. Chọn option「銀行振込」\n3. Chuyển lại tab bill tháng\n"
       "4. Quan sát option đang chọn và title step 2",
       "—",
       "- Option quay về「クレジットカード」\n- Title step 2 hiện「クレジットカード情報入力」\n"
       "- Bấm tiếp thì đi tới màn nhập thẻ, KHÔNG mở modal chuyển khoản",
       note="Nguồn: r95."),

    tc("Xác nhận plan — mua mới", "UI-005", "Normal",
       "Checkbox 注意事項 bị disable cho tới khi cuộn hết nội dung",
       NEW,
       "1. Quan sát checkbox「注意事項を読み、解約や返金について内容を理解しました」khi mới vào\n"
       "2. Rê chuột lên checkbox khi chưa cuộn hết\n"
       "3. Cuộn khối 注意事項 tới cuối\n4. Click checkbox",
       "—",
       "- Mặc định: checkbox chưa tích và disable\n"
       "- Hover khi chưa cuộn hết: hiện tooltip「注意事項を最後までスクロールして確認してください。」\n"
       "- Sau khi cuộn hết: checkbox enable và tick được",
       note="Nguồn: r99-r101, r550-r556."),

    tc("Xác nhận plan — mua mới", "STATE-002", "Normal",
       "Đã tick 注意事項 rồi đổi tab chu kỳ / đổi owner → checkbox giữ nguyên trạng thái tích",
       NEW,
       "1. Cuộn hết 注意事項 và tick checkbox\n2. Chuyển tab bill tháng ↔ năm\n"
       "3. Chọn lại 主管理者\n4. Quan sát checkbox",
       "—",
       "Checkbox vẫn giữ trạng thái đã tích ở cả 2 thao tác",
       note="Nguồn: r102, r103."),

    tc("Xác nhận plan — mua mới", "FUNC-003", "Abnormal",
       "Chưa tick 注意事項 → nút 決済に進む không bấm được",
       NEW,
       "1. Không tick checkbox 注意事項\n2. Bấm「決済に進む」",
       "—",
       "Nút disable, không sang step 2, không tạo bot_contract nào",
       note="Nguồn: r105."),

    tc("Xác nhận plan — mua mới", "FUNC-001", "Normal",
       "Nút キャンセル ở step 1 → quay lại màn chọn plan, không tạo hợp đồng",
       NEW,
       "1. Ở step 1 bấm「キャンセル」\n2. Kiểm tra bảng bot_contracts",
       "—",
       "- Quay lại màn「プラン選択」\n- DB: KHÔNG phát sinh bản ghi bot_contracts mới",
       note="Nguồn: r104."),

    # ═════════════ 8. Xác nhận plan — upgrade ═════════════
    tc("Xác nhận plan — upgrade", "UI-001", "Normal",
       "Step 1 upgrade: hiện tên bot ở 対象アカウント, KHÔNG cho chọn owner",
       "- Đăng nhập owner của bot free「テストBOT」\n"
       "- Click nút upgrade của bot free đó → màn chọn plan → chọn standard",
       "1. Quan sát mục 対象アカウント\n2. Quan sát mục 主管理者",
       "Bot free「テストBOT」",
       "- 対象アカウント hiện tên bot「テストBOT」(không phải 新規LINE公式アカウント接続)\n"
       "- KHÔNG có ô chọn 主管理者 (khác luồng mua mới)",
       note="Nguồn: r42, r63, r141, r143."),

    tc("Xác nhận plan — upgrade", "DATA-002", "Normal",
       "Upgrade standard → pro giữa kỳ: số tiền tính theo ngày còn lại (日割り)",
       "- Bot standard tháng đang 正常, còn 20 ngày tới expired_date_contract\n"
       "- Click upgrade lên pro",
       "1. Quan sát mục お支払い総額 ở step 1\n2. Tự tính lại: (giá pro − giá standard) × 20/30\n"
       "3. Sau khi bill xong, mở màn lịch sử hóa đơn xem cột 備考",
       "Bot standard tháng, remain = 20 ngày",
       "- Số tiền hiển thị khớp phép tính theo ngày còn lại\n"
       "- Cột 備考 của hóa đơn hiện「アップグレード 日割り（20日分）」\n"
       "- DB: payment_histories.remain_day_upgrade = 20",
       env="PRODUCTION",
       note="Nguồn: r843 (SpecImprove #33149, 21/10/2025) + r32 (List main case). "
            "RULE-08: bill tiền → PRODUCTION. Chi tiết công thức 日割り KHÔNG có trong spec — xem MT-09."),

    tc("Xác nhận plan — upgrade", "FUNC-006", "Normal",
       "Upgrade free → standard/pro bằng thẻ: bill thành công thì đổi plan + tạo lịch sử",
       "- Bot free đang hoạt động, owner có thẻ hợp lệ",
       "1. Upgrade bot free lên standard, chọn bill card, nhập thẻ hợp lệ\n"
       "2. Sau khi hoàn tất, mở /basic/point-settings\n3. Mở màn lịch sử hóa đơn\n"
       "4. Kiểm tra bảng bot_contracts và bots",
       "Bot free → standard tháng, thẻ 4242 4242 4242 4242",
       "- Màn list hợp đồng: plan đổi thành スタンダード, status 正常\n"
       "- Lịch sử hóa đơn có bản ghi mới của tháng hiện tại\n"
       "- DB: bot_contracts.contract_type = standard, status=1, status_payment=1; "
       "bots.plan_type và expired_date được cập nhật",
       note="Nguồn: r410, r411, r19 (tab hóa đơn). RULE-07: kiểm cả DB + màn hình + lịch sử."),

    tc("Xác nhận plan — upgrade", "FUNC-006", "Abnormal",
       "Upgrade bằng thẻ nhưng bill lỗi → giữ nguyên plan cũ, không tạo lịch sử",
       "- Bot free đang hoạt động",
       "1. Upgrade bot free lên standard, nhập thẻ lỗi 4111 1111 1111 1111\n"
       "2. Quan sát màn hình\n3. Kiểm tra bot_contracts, bots và lịch sử hóa đơn",
       "Thẻ lỗi 4111 1111 1111 1111",
       "- Hiện lỗi, ở lại màn nhập thẻ để nhập lại\n"
       "- DB: bot vẫn plan free (bots.plan_type không đổi), hợp đồng cũ giữ nguyên\n"
       "- KHÔNG tạo bản ghi lịch sử bill hiển thị cho user",
       note="Nguồn: r12 (Màn hình bill tiền r429), r20 (tab hóa đơn), r64."),

    tc("Xác nhận plan — upgrade", "STATE-003", "Normal",
       "Upgrade bằng chuyển khoản, CHƯA chuyển tiền → hợp đồng chưa được nâng cấp, tính năng vẫn theo plan cũ",
       "- Bot free đang hoạt động",
       "1. Upgrade bot free lên standard, chọn bill năm + 銀行振込\n"
       "2. Hoàn tất đăng ký, KHÔNG chuyển tiền\n3. Mở /basic/point-settings\n"
       "4. Vào 1 màn tính năng bị giới hạn theo plan free",
       "Bot free → standard năm, phương thức 銀行振込",
       "- Màn list: hiện plan スタンダード với status「入金待ち」\n"
       "- Các tính năng vẫn bị giới hạn theo bot free\n"
       "- Chưa có bản ghi trong lịch sử hóa đơn của user và admin",
       note="Nguồn: r412, r363, r374 (Màn hình bill tiền)."),

    tc("Xác nhận plan — upgrade", "STATE-003", "Normal",
       "Upgrade bằng chuyển khoản, đã chuyển tiền (callback success) → nâng cấp thành công",
       "- Bot free đã đăng ký upgrade standard năm bằng 銀行振込, đang 入金待ち",
       "1. Thực hiện chuyển khoản / gọi callback success từ UnivaPay\n"
       "2. Mở /basic/point-settings\n3. Mở lịch sử hóa đơn\n4. Kiểm tra bảng bot_contracts",
       "Callback charge_finished = success",
       "- Màn list: plan スタンダード, status 正常\n- Lịch sử hóa đơn có bản ghi mới\n"
       "- DB: bot_contracts.status=1, status_payment=1; lịch sử hoa hồng affiliate được tạo (nếu có aff)",
       note="Nguồn: r413, r364. RULE-06: đi tới output cuối (màn list + hóa đơn), không dừng ở callback."),

    tc("Xác nhận plan — upgrade", "STATE-003", "Abnormal",
       "Upgrade bằng chuyển khoản, KHÔNG chuyển tiền (callback fail) → về lại plan cũ",
       "- Bot free đã đăng ký upgrade standard năm bằng 銀行振込, đang 入金待ち",
       "1. Để quá hạn chuyển khoản / gọi callback fail\n2. Mở /basic/point-settings\n"
       "3. Kiểm tra bot_contracts và lịch sử hóa đơn",
       "Callback charge_finished = failed",
       "- Màn list: plan quay lại フリー\n- Các tính năng vẫn bị giới hạn theo bot free\n"
       "- KHÔNG có bản ghi lịch sử bill",
       note="Nguồn: r414, r418. ⚠ Với case MAX FRIEND thì spec mới lại giữ plan pro và chuyển sang "
            "cancel hợp đồng (Bill max friend r17) — hành vi khác nhau, xem MT-10."),

    tc("Xác nhận plan — upgrade", "FUNC-006", "Normal",
       "Upgrade standard → pro bằng thẻ cũ: bill thẻ cũ thành công thì không phải nhập lại thẻ",
       "- Bot standard tháng, bill card, thẻ chính hợp lệ",
       "1. Click upgrade lên pro\n2. Bấm bill bằng thẻ đã đăng ký\n"
       "3. Quan sát màn hình sau khi bill\n4. Kiểm tra lịch sử bill của user và admin",
       "Bot standard tháng, thẻ chính hợp lệ",
       "- KHÔNG hiện màn nhập thẻ, đi thẳng tới màn hoàn tất\n"
       "- Hợp đồng đổi thành pro, hiện đúng ở màn list\n- Có bản ghi lịch sử bill mới ở cả user và admin",
       note="Nguồn: r428."),

    tc("Xác nhận plan — upgrade", "FUNC-006", "Abnormal",
       "Upgrade standard → pro, thẻ cũ bill lỗi → mở màn nhập thẻ mới, chưa đổi plan",
       "- Bot standard tháng, thẻ chính đã hết hạn/bị từ chối",
       "1. Click upgrade lên pro → bấm bill bằng thẻ cũ\n2. Quan sát màn hình\n"
       "3. Kiểm tra plan của bot và lịch sử bill",
       "Thẻ chính bill fail",
       "- Hiện màn nhập thẻ mới\n- Plan của bot GIỮ NGUYÊN standard\n- KHÔNG tạo lịch sử bill",
       note="Nguồn: r429, r433."),

    tc("Xác nhận plan — upgrade", "FUNC-006", "Normal",
       "Thẻ cũ lỗi → nhập thẻ mới bill thành công → upgrade thành công bằng thẻ mới",
       "- Bot standard tháng, thẻ chính bill lỗi",
       "1. Click upgrade lên pro → thẻ cũ lỗi → mở màn nhập thẻ\n"
       "2. Nhập thẻ mới hợp lệ, bấm 決済する\n3. Kiểm tra plan, lịch sử bill và 4 số cuối thẻ ở màn detail",
       "Thẻ mới 5555 5555 5555 4444",
       "- Upgrade thành công, plan = pro\n- Có lịch sử bill mới\n"
       "- Màn detail hợp đồng hiện 4 số cuối thẻ MỚI (4444)",
       note="Nguồn: r430, r7 (tab hóa đơn)."),

    tc("Xác nhận plan — upgrade", "STATE-002", "Abnormal",
       "Thẻ cũ lỗi → user đóng màn nhập thẻ mà không bill → không đổi plan, không tạo lịch sử",
       "- Bot standard tháng, thẻ chính bill lỗi",
       "1. Click upgrade lên pro → thẻ cũ lỗi → mở màn nhập thẻ\n"
       "2. Đóng màn hình / bấm back mà không bấm bill\n3. Kiểm tra bot_contracts và lịch sử bill",
       "—",
       "- Plan giữ nguyên standard\n- KHÔNG tạo lịch sử bill\n- Không phát sinh bot_contract thừa",
       note="Nguồn: r431, r435."),

    tc("Xác nhận plan — upgrade", "CONC-001", "Abnormal",
       "Nhập thẻ bill lỗi 2 lần liên tiếp ở luồng mua mới → không tạo nhiều bot_contract rác",
       "- Đăng nhập user chưa có slot standard",
       "1. Mua mới hợp đồng standard, nhập thẻ lỗi → báo lỗi\n"
       "2. Nhập lại thẻ lỗi lần 2 → báo lỗi\n3. Đếm số bản ghi bot_contracts của user",
       "2 lần nhập thẻ lỗi liên tiếp",
       "Chỉ tồn tại 1 bản ghi bot_contracts (status=0, status_payment=2); KHÔNG sinh 2 bản ghi",
       note="Nguồn: r10, r11 (tab Improve màn download quản lý hóa đơn)."),

    tc("Xác nhận plan — upgrade", "CONC-002", "Abnormal",
       "Bill fail rồi mới có callback success muộn → hệ thống vẫn hoàn tất hợp đồng đúng 1 lần",
       "- Đã mua mới hợp đồng standard, nhập thẻ và nhận kết quả fail",
       "1. Gọi callback success của UnivaPay cho charge đó (qua Postman)\n"
       "2. Mở /basic/point-settings\n3. Kiểm tra bot_contracts, bot_slots và lịch sử bill",
       "Callback charge_finished = success đến SAU khi web đã báo fail",
       "- bot_contracts: status=1, status_payment=1\n- Tạo mới bot_slot map với bot\n"
       "- Lịch sử bill cập nhật type=1\n- Chỉ 1 bản ghi lịch sử, không nhân đôi",
       note="Nguồn: r12, r15, r18, r21 (tab hóa đơn) + r329-r356 (Improve bill tiền 12/2024)."),

    tc("Xác nhận plan — upgrade", "CONC-002", "Abnormal",
       "Upgrade transfer đang 入金待ち, user bấm hủy hợp đồng rồi mới có callback UnivaPay",
       "- Bot free upgrade lên standard bằng transfer, status_payment = 6 (đang chờ chuyển khoản)",
       "1. User bấm hủy hợp đồng ở màn detail\n"
       "2. Gọi callback UnivaPay (success và fail ở 2 lần thử riêng)\n"
       "3. Kiểm tra trạng thái hợp đồng và số bản ghi lịch sử bill",
       "status_payment = 6, callback đến SAU thao tác hủy",
       "- Trạng thái hợp đồng không bị nhảy về active do callback muộn\n"
       "- Không tạo lịch sử bill trùng\n- Ghi log đủ để truy vết thứ tự sự kiện",
       note="Nguồn: r483, r492, r493 (Improve bill tiền 12/2024). ⚠ Corpus KHÔNG ghi rõ kết quả cuối cùng "
            "cho từng nhánh callback → cần Leader chốt, xem MT-11."),

    tc("Xác nhận plan — upgrade", "CONC-002", "Abnormal",
       "Upgrade transfer có 2 bill chuyển khoản song song → xử lý đúng theo thứ tự callback",
       "- Bot free upgrade standard bằng transfer, phát sinh 2 charge transfer (bill1, bill2)",
       "1. Cho callback bill1 success, bill2 success\n2. Lặp lại với bill1 success/bill2 fail\n"
       "3. Lặp lại với bill1 fail/bill2 success\n4. Lặp lại với cả 2 fail\n"
       "5. Lặp lại với bill2 success rồi bill1 mới fail\n"
       "6. Mỗi lần kiểm tra trạng thái hợp đồng + số lịch sử bill",
       "5 tổ hợp callback như phần bước",
       "- Mỗi tổ hợp: trạng thái hợp đồng nhất quán, KHÔNG có 2 lịch sử bill cho cùng 1 kỳ\n"
       "- Callback fail đến SAU callback success không được hạ trạng thái hợp đồng đang active",
       note="Nguồn: r486-r491 (Improve bill tiền 12/2024). ⚠ Corpus chỉ liệt kê tổ hợp, không ghi expected "
            "chi tiết từng nhánh — expected ở đây do AI suy luận theo nguyên tắc idempotent, CẦN LEADER XÁC NHẬN. Xem MT-11."),

    # ═════════════ 9. Nhập thẻ & 3D Secure ═════════════
    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Normal",
       "Màn nhập thẻ hiển thị đủ 5 field của widget UnivaPay",
       "- Đang ở step 2「クレジットカード情報入力」của luồng mua mới",
       "1. Quan sát widget nhập thẻ\n2. Liệt kê các field",
       "—",
       "Hiển thị đủ 5 field: 電話番号 · カード名義 · カード番号 · 有効期限（月/年）· セキュリティコード",
       note="Nguồn: r108-r112, r409-r414 (Quản lý hợp đồng)."),

    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Normal",
       "Mục お住まい: là dropdown bắt buộc, đúng 2 option 日本 / 日本国外",
       "- Đang ở màn nhập thẻ (bước ①「クレジットカード情報入力」)",
       "1. Tìm mục「お住まい」\n2. Mở dropdown và đọc danh sách option\n"
       "3. Quan sát giá trị mặc định",
       "—",
       "- Có mục「お住まい」, control là dropdown (không phải textbox)\n"
       "- Đúng 2 option:「日本」và「日本国外」, không thừa/thiếu\n"
       "- Mặc định chưa chọn, hiện placeholder「選択してください」",
       note="Nguồn: Feature #36994 r3-r5 (07/2026). ⚠ Kết quả thực tế của tester ghi KHÔNG có marker「必須」"
            "(do widget UnivaPay) — đây là điểm lệch giữa TC và hiện trạng, xem MT-12."),

    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Abnormal",
       "Không chọn お住まい → chặn ở client, không tạo giao dịch",
       "- Đang ở màn nhập thẻ, đã nhập đủ 5 field thẻ hợp lệ và tick đồng ý",
       "1. Để trống「お住まい」\n2. Bấm「決済する」\n3. Kiểm tra UnivaPay xem có charge nào được tạo không",
       "5 field thẻ hợp lệ, お住まい rỗng",
       "- Hiện message lỗi「お住まいを選択してください。」\n- KHÔNG sang bước ②\n"
       "- KHÔNG gọi charge, UnivaPay không phát sinh giao dịch",
       note="Nguồn: Feature #36994 r10 (kết quả thực tế đã xác nhận message)."),

    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Normal",
       "Chọn 日本 hoặc 日本国外 → đều đi tiếp, không phát sinh field điều kiện",
       "- Đang ở màn nhập thẻ, đã nhập đủ field thẻ hợp lệ và tick đồng ý",
       "1. Chọn お住まい =「日本」→ bấm 決済する\n"
       "2. Lặp lại với「日本国外」→ quan sát form trước khi bấm",
       "2 giá trị: 日本 và 日本国外",
       "- Cả 2 lựa chọn đều không báo lỗi và sang được bước ②\n"
       "- Chọn 日本国外 KHÔNG làm hiện thêm field mới, không đổi validation",
       note="Nguồn: Feature #36994 r11, r12."),

    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Abnormal",
       "Bỏ trống các field thẻ → validate từng trường, không đi tới màn lỗi thẻ",
       "- Đang ở màn nhập thẻ",
       "1. Bỏ trống toàn bộ field\n2. Bấm「決済する」\n3. Quan sát từng ô\n"
       "4. Điền thiếu 1 field bất kỳ rồi bấm lại",
       "Form rỗng và form thiếu 1 field",
       "- Hiện message validate ngay tại từng field còn trống\n"
       "- KHÔNG chuyển sang màn「カード情報変更エラー」/ màn nhập thẻ lỗi\n- Không gọi charge",
       note="Nguồn: r1298-r1310 (Bug KH #34792, 17/03/2026 — trước fix vẫn đi tới màn nhập thẻ lỗi)."),

    tc("Nhập thẻ & 3D Secure", "FUNC-003", "Abnormal",
       "Không tick 個人情報取得への同意 → chặn với message この項目は必須です",
       "- Đang ở màn nhập thẻ, đã nhập đủ field thẻ hợp lệ",
       "1. Bỏ trống checkbox「個人情報取得への同意」\n2. Bấm「決済する」",
       "Checkbox chưa tick",
       "Hiện message「この項目は必須です」, không thực hiện thanh toán",
       note="Nguồn: r115, r415."),

    tc("Nhập thẻ & 3D Secure", "FUNC-001", "Normal",
       "Link 個人情報の取扱いについて mở trang UnivaPay",
       "- Đang ở màn nhập thẻ",
       "1. Click text「個人情報の取扱いについて」",
       "—",
       "Mở https://univapaycast.com/handling02/",
       note="Nguồn: r417, r458."),

    tc("Nhập thẻ & 3D Secure", "FUNC-001", "Normal",
       "Nút 前の画面に戻る khi đã nhập thẻ → quay lại step trước, không lưu thẻ",
       "- Đang ở màn nhập thẻ, đã nhập đủ thông tin thẻ",
       "1. Bấm「前の画面に戻る」\n2. Kiểm tra 4 số cuối thẻ ở màn detail hợp đồng",
       "Thẻ 5555 5555 5555 4444 đã nhập nhưng chưa bấm 決済する",
       "- Quay lại màn trước\n- Thông tin thẻ KHÔNG được lưu (univa_last_four_card giữ giá trị cũ)\n"
       "- Không phát sinh giao dịch trên UnivaPay",
       note="Nguồn: r114, r418, r419."),

    tc("Nhập thẻ & 3D Secure", "SEC-001", "Abnormal",
       "Double-click nút 決済する → chỉ tạo đúng 1 giao dịch",
       "- Đang ở màn nhập thẻ, đã nhập đủ thông tin thẻ hợp lệ",
       "1. Double-click nhanh nút「決済する」\n2. Kiểm tra danh sách charge trên UnivaPay\n"
       "3. Đếm bản ghi payment_histories của hợp đồng",
       "Thẻ hợp lệ 4242 4242 4242 4242",
       "- UnivaPay chỉ ghi nhận 1 giao dịch\n- payment_histories chỉ có 1 bản ghi mới\n"
       "- Không tạo 2 bot_contract",
       env="PRODUCTION",
       note="Nguồn: r113. RULE-08: race condition + bill tiền → PRODUCTION."),

    tc("Nhập thẻ & 3D Secure", "FUNC-006", "Normal",
       "Bill có 3D Secure: xác thực thành công → hợp đồng được tạo/upgrade",
       "- Thẻ test có bật 3D Secure trên UnivaPay",
       "1. Mua mới hợp đồng standard bằng thẻ 3DS\n2. Hoàn tất popup xác thực 3D Secure\n"
       "3. Kiểm tra hợp đồng và giao dịch trên UnivaPay",
       "Thẻ có 3D Secure, xác thực đúng",
       "- Hiện popup xác thực 3D Secure trước khi charge\n"
       "- Xác thực đúng: bill thành công, hợp đồng được tạo, UnivaPay ghi status Successful",
       env="PRODUCTION",
       note="Nguồn: tab「Bill tiền univapay: 3D secure」r4, r6, r8 (03/2025). "
            "Ghi chú của tester: staging chưa có tài khoản bật 3DS → RULE-08 PRODUCTION."),

    tc("Nhập thẻ & 3D Secure", "FUNC-006", "Abnormal",
       "Bill có 3D Secure: xác thực thất bại → báo lỗi 3D認証に失敗しました, ở lại màn nhập thẻ",
       "- Thẻ test có bật 3D Secure",
       "1. Mua mới hợp đồng standard bằng thẻ 3DS\n2. Cố tình nhập sai mã xác thực 3DS\n"
       "3. Đóng popup và quan sát màn hình\n4. Kiểm tra bot_contracts",
       "Thẻ 3DS, xác thực sai",
       "- Hiện popup 3DS lỗi, sau đó message「3D認証に失敗しました。」\n"
       "- Đóng popup vẫn ở màn nhập thẻ\n- Hợp đồng KHÔNG được tạo/upgrade",
       env="PRODUCTION",
       note="Nguồn: tab 3D secure r5."),

    tc("Nhập thẻ & 3D Secure", "MSG-001", "Abnormal",
       "Message lỗi thanh toán phải bằng tiếng Nhật, không lọt tiếng Anh",
       "- Bot standard, thao tác upgrade lên pro bằng thẻ cũ",
       "1. Gây lỗi bill (dùng thẻ 4111 1111 1111 1111)\n2. Đọc toàn bộ message lỗi hiển thị",
       "Thẻ lỗi 4111 1111 1111 1111",
       "Message lỗi hiển thị bằng tiếng Nhật (ví dụ「一般エラーが発生しました。詳細情報は管理画面で"
       "確認できます。」), KHÔNG hiện chuỗi lỗi tiếng Anh thô từ UnivaPay",
       note="Nguồn: tab 3D secure r14 (ghi chú staging:「đang hiện msg lỗi tiếng anh」) + r496. "
            "⚠ Đây là lỗi từng ghi nhận, cần verify lại sau fix."),

    # ═════════════ 10. Chuyển khoản — tạo & thông tin tài khoản ═════════════
    tc("Chuyển khoản — tạo & thông tin tài khoản", "FUNC-006", "Normal",
       "Chọn 銀行振込 → hiện màn お申し込みありがとうございます + thông tin tài khoản",
       "- Đang ở step 1 mua mới, chọn plan standard bill năm",
       "1. Chọn phương thức「銀行振込（請求書の発行ができます）」\n2. Bấm 決済に進む\n"
       "3. Quan sát màn hình kết quả",
       "Plan standard, bill năm, phương thức transfer",
       "- Hiện màn「お申し込みありがとうございます。振込期日までにお振込が確認でき次第、ご契約完了となります。」\n"
       "- Hiển thị thông tin tài khoản chuyển khoản\n- Màn /basic/point-settings có bản ghi status 入金待ち",
       note="Nguồn: r94, r119, r120, r15 (List main case)."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "DATA-003", "Normal",
       "Hạn chuyển khoản = ngày bill + 7 ngày, format yyyy年mm月dd日 23:59 まで",
       "- Vừa đăng ký mua mới standard năm bằng 銀行振込 ngày 2026/10/13",
       "1. Đọc mục thời hạn chuyển khoản trên màn kết quả\n"
       "2. Đối chiếu bot_contracts.expired_date_bank_transfer",
       "Ngày đăng ký = 2026/10/13",
       "- Hiển thị「2026年10月20日 23:59 まで」(= ngày bill + 7 ngày)\n"
       "- DB: expired_date_bank_transfer khớp giá trị hiển thị",
       note="Nguồn: r121 + r1722 (regression: job tạo bill transfer có お支払い期限 = expired_date + 7 ngày)."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "DATA-002", "Normal",
       "Số tiền chuyển khoản đúng theo plan và số năm",
       "- Đang ở màn thông tin chuyển khoản sau khi đăng ký",
       "1. Đăng ký standard bill 1 năm → ghi số tiền\n2. standard bill 2 năm → ghi số tiền\n"
       "3. pro bill 1 năm → ghi số tiền\n4. pro bill 2 năm → ghi số tiền",
       "4 tổ hợp plan × số năm",
       "- standard 1 năm: 116.424円 (税込)\n- standard 2 năm: 232.848円 (税込)\n"
       "- pro 1 năm: 356.400円 (税込)\n- pro 2 năm: 712.800円 (税込)",
       env="PRODUCTION",
       note="Nguồn: r122-r125. RULE-08: bill tiền → PRODUCTION."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "DATA-001", "Normal",
       "Bill transfer lưu thêm bank_branch_code và bank_account_holder_name",
       "- Vừa đăng ký hợp đồng bằng 銀行振込, đã phát hành số tài khoản",
       "1. Mở modal thông tin chuyển khoản trên web\n"
       "2. Đối chiếu tên chi nhánh và tên người nhận hiển thị với dữ liệu lưu ở bot_contracts",
       "Hợp đồng bill transfer đã có univa_account_number",
       "- Web hiện: tên ngân hàng, tên chi nhánh + 支店, loại/số tài khoản, tên người nhận (ｶ)ﾕﾆｳﾞｧﾍﾟｲｷｬｽﾄ\n"
       "- DB lưu đủ bank_branch_code và bank_account_holder_name khớp với hiển thị",
       note="Nguồn: r324-r349 (Màn hình bill tiền). Spec KHÔNG liệt kê 2 cột này trong db-mapping — xem MT-13."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "NOTI-MAIL-001", "Normal",
       "Job phát hành số tài khoản xong → gửi mail thông báo cho user",
       "- Hợp đồng bill transfer ở trạng thái 口座発行中 (univa_account_number IS NULL)\n"
       "- Có quyền chạy job recover:RecoverUpdateInfoUnivapay",
       "1. Chạy job recover (hoặc chờ chu kỳ 5 phút)\n"
       "2. Kiểm tra bot_contracts.univa_account_number\n3. Mở hộp thư của admin hợp đồng",
       "request_get_bank_transfer.status = 0",
       "- univa_account_number được ghi giá trị\n- Trạng thái đổi từ 口座発行中 sang 入金待ち\n"
       "- Admin nhận được mail thông báo số tài khoản chuyển khoản (nội dung khớp thông tin trên web)",
       env="PRODUCTION",
       note="Nguồn: r323 (Màn hình bill tiền) + job-spec RecoverUpdateInfoUnivapay (feature-spec.md §7). "
            "RULE-06: đi tới output cuối là email. RULE-08: job → PRODUCTION."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "FUNC-003", "Normal",
       "Nút 請求書のダウンロード trên màn chuyển khoản → tải hóa đơn đúng danh xưng",
       "- Đang ở màn「銀行振込口座のご案内」sau khi đăng ký transfer",
       "1. Click「請求書のダウンロード」\n2. Nhập 宛名「株式会社テスト」\n"
       "3. Lần lượt chọn 御中 / 様 / 設定無し và tải\n4. Mở từng file PDF",
       "宛名 =「株式会社テスト」, 3 danh xưng",
       "- Mỗi lần tải được 1 file PDF\n"
       "- Nội dung PDF hiện đúng「株式会社テスト 御中」/「… 様」/ chỉ tên (khi 設定無し)\n"
       "- Không hiện text「株式会社」thừa phía trước danh xưng",
       note="Nguồn: r127-r136 + r327-r344 (Bug KH #32953, 01/12/2025 — bỏ text 株式会社). "
            "RULE-06: bắt buộc mở file PDF."),

    tc("Chuyển khoản — tạo & thông tin tài khoản", "FUNC-001", "Normal",
       "Nút ホームに戻る ở màn chuyển khoản → về /admin/home",
       "- Đang ở màn「銀行振込口座のご案内」",
       "1. Click「ホームに戻る」",
       "—",
       "Đóng màn hiện tại và chuyển về /admin/home",
       note="Nguồn: r126."),

    # ═════════════ 11. Hủy chuyển khoản ═════════════
    tc("Hủy chuyển khoản", "FUNC-007", "Normal",
       "Nút 振込キャンセル CHỈ hiện với hợp đồng mua mới lần đầu",
       "- Chuẩn bị 6 hợp đồng đang chờ chuyển khoản gồm: mua mới standard năm (口座発行中), "
       "mua mới standard năm (入金待ち), mua mới pro năm (口座発行中), mua mới pro năm (入金待ち), "
       "upgrade free→standard, upgrade free→pro",
       "1. Mở /basic/point-settings\n2. Quan sát nút ở cột 8 của từng dòng",
       "6 hợp đồng như tiền đề",
       "Cả 6 dòng đều hiện nút「振込キャンセル」màu đỏ",
       note="Nguồn: r1517-r1522 (Specchange 03/2026, 20/04/2026)."),

    tc("Hủy chuyển khoản", "FUNC-007", "Normal",
       "Hợp đồng UPDATE (đổi phương thức / extend / job bill / upgrade standard→pro) → hiện 契約詳細, không hiện 振込キャンセル",
       "- Chuẩn bị 4 hợp đồng đang 入金待ち sinh từ: đổi phương thức card→transfer, extend hợp đồng, "
       "job bill định kỳ, upgrade standard→pro",
       "1. Mở /basic/point-settings, quan sát nút cột 8 của 4 dòng\n"
       "2. Click「契約詳細」và quan sát các nút thay đổi hợp đồng bên trong",
       "4 hợp đồng update như tiền đề",
       "- Cả 4 dòng hiện status 入金待ち và nút「契約詳細」(KHÔNG có 振込キャンセル)\n"
       "- Trong màn chi tiết, các nút thay đổi hợp đồng bị disable",
       note="Nguồn: r1523, r1524, r1527, r1528 (Specchange 03/2026). "
            "⚠ Bug KH #36835 (28/05/2026) từng báo ngược lại — nút không hiện khi cần; xem MT-14."),

    tc("Hủy chuyển khoản", "FUNC-007", "Normal",
       "Hợp đồng lại (từ đã hủy / cưỡng chế hủy) bằng transfer → VẪN hiện nút 振込キャンセル",
       "- 1 hợp đồng 解約済み và 1 hợp đồng 強制解約, mỗi cái đã bấm 再契約 bằng 銀行振込",
       "1. Mở /basic/point-settings\n2. Quan sát status và nút của 2 dòng",
       "2 hợp đồng tái ký bằng transfer",
       "Cả 2 dòng hiện status 入金待ち và có nút「振込キャンセル」",
       note="Nguồn: r1525, r1526."),

    tc("Hủy chuyển khoản", "FUNC-007", "Normal",
       "Hủy chuyển khoản của hợp đồng MUA MỚI → xóa hẳn bản ghi + charge UnivaPay chuyển Canceled",
       "- Có hợp đồng mua mới standard năm (hoặc pro năm) đang 入金待ち / 口座発行中",
       "1. Click「振込キャンセル」→ xác nhận「振込キャンセルを実行する」\n"
       "2. Quan sát màn list\n3. Kiểm tra bot_contracts\n4. Kiểm tra charge trên UnivaPay",
       "4 tổ hợp: mua standard năm và mua pro năm × (入金待ち, 口座発行中)",
       "- Dòng biến mất khỏi màn list\n- DB: bản ghi bot_contracts bị xóa\n"
       "- UnivaPay: charge của lần bill transfer chuyển sang status「Canceled」",
       env="PRODUCTION",
       note="Nguồn: r66, r79, r80, r93, r94, r324-r327, r1529-r1532 (nhiều dòng cùng expected → gộp, "
            "liệt kê đủ 4 tổ hợp ở Dữ liệu test). RULE-08: bill tiền → PRODUCTION."),

    tc("Hủy chuyển khoản", "STATE-003", "Normal",
       "Hủy chuyển khoản của UPGRADE khi hợp đồng cũ CÒN HẠN → quay về hợp đồng cũ nguyên trạng",
       "- Bot free/standard upgrade lên plan cao hơn bằng transfer, đang 入金待ち\n"
       "- expired_date_contract của hợp đồng cũ > hiện tại",
       "1. Click「振込キャンセル」→ xác nhận\n2. Quan sát plan và status ở màn list\n"
       "3. Kiểm tra bot_contracts",
       "Upgrade free→standard, free→pro, standard→pro; expired_date_contract > now",
       "- Màn list hiện lại đúng plan TRƯỚC khi upgrade\n"
       "- DB: status=1, expired_date_contract giữ nguyên giá trị cũ\n"
       "- Riêng case upgrade từ free: payment_method = 1 và expired_date = NULL",
       note="Nguồn: r67, r81-r86, r1533, r1534 + r35 (List main case) + Bug KH #34622 (26/02/2026)."),

    tc("Hủy chuyển khoản", "STATE-003", "Boundary",
       "Hủy chuyển khoản khi hợp đồng cũ QUÁ HẠN nhưng chưa quá 7 ngày → về trạng thái 延滞中",
       "- Hợp đồng upgrade bằng transfer đang 入金待ち\n"
       "- expired_date_contract của hợp đồng cũ đã quá hạn 3 ngày",
       "1. Click「振込キャンセル」→ xác nhận\n2. Quan sát status ở màn list\n3. Kiểm tra bot_contracts",
       "expired_date < now < expired_date + 7 ngày",
       "- Màn list hiện status「延滞中」\n"
       "- DB: status=1, status_payment=2, status_payment_fail thuộc (0,5)",
       note="Nguồn: r35 (List main case), r95-r102, r109."),

    tc("Hủy chuyển khoản", "STATE-003", "Boundary",
       "Hủy chuyển khoản khi hợp đồng cũ đã QUÁ 7 NGÀY → chuyển thành đã hủy",
       "- Hợp đồng upgrade bằng transfer đang 入金待ち\n"
       "- expired_date_contract của hợp đồng cũ đã quá hạn 8 ngày",
       "1. Click「振込キャンセル」→ xác nhận\n2. Quan sát status\n3. Kiểm tra bot_contracts",
       "expired_date + 7 ngày < now",
       "- Màn list hiện status đã hủy\n"
       "- DB: status=3, status_payment=2, cancel_by=1, user_cancel_id != NULL, date_cancel_contract được cập nhật",
       note="Nguồn: r35, r36, r37 (List main case). ⚠ Corpus tại r81-r86 lại ghi 'Expired_date + 7 > now → "
            "Đã hủy' (ngược logic) — xem MT-15."),

    tc("Hủy chuyển khoản", "STATE-003", "Normal",
       "Hủy chuyển khoản của EXTEND → khôi phục expired_date về giá trị trước khi gia hạn",
       "- Hợp đồng standard năm bill transfer, đã bấm gia hạn 1 năm, đang 入金待ち",
       "1. Ghi lại expired_date_contract trước khi extend\n2. Click「振込キャンセル」→ xác nhận\n"
       "3. Kiểm tra expired_date_contract và status",
       "expired_date trước extend = 2026/10/31",
       "- Hợp đồng trở về trạng thái trước khi gia hạn (status=1)\n"
       "- expired_date_contract quay lại 2026/10/31, KHÔNG cộng thêm 1 năm",
       note="Nguồn: r70, r85, r86, r36 (List main case). Đối chiếu BR-05 (feature-spec.md §5)."),

    tc("Hủy chuyển khoản", "STATE-003", "Normal",
       "Hủy chuyển khoản của hợp đồng TÁI KÝ → trạng thái quay lại đúng loại hủy trước đó",
       "- 1 hợp đồng từng 解約済み và 1 hợp đồng từng 強制解約, cả 2 đã 再契約 bằng transfer, đang 入金待ち",
       "1. Click「振込キャンセル」ở từng dòng → xác nhận\n2. Quan sát status ở màn list",
       "2 hợp đồng tái ký từ 解約済み và 強制解約",
       "Trạng thái quay lại đúng loại hủy trước đó (解約済み / 強制解約), không thành hợp đồng active",
       note="Nguồn: r89-r92, r103-r106."),

    tc("Hủy chuyển khoản", "UI-005", "Normal",
       "Đóng modal 振込み（お申し込み）のキャンセル bằng X/閉じる → không hủy gì",
       "- Có hợp đồng đang 入金待ち với nút 振込キャンセル",
       "1. Click「振込キャンセル」→ mở modal\n2. Click X\n3. Mở lại modal, click「閉じる」\n"
       "4. Kiểm tra trạng thái hợp đồng",
       "—",
       "- Modal đóng ở cả 2 cách\n- Hợp đồng giữ nguyên status 入金待ち\n- Charge UnivaPay không bị cancel",
       note="Nguồn: r71."),
]
