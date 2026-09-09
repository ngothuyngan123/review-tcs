# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 19-24: hủy hợp đồng, cưỡng chế hủy, hợp đồng lại, ngắt kết nối LOA, lịch sử.

Nguồn chính: TCsLine_Bill tiền_Improve2025 → tab「Quản lý hợp đồng」
  · r130-r143 (màn account đã hủy / cưỡng chế hủy) · r606-r645 (27 modal lịch sử)
  · r720-r792 (trạng thái hủy + hợp đồng lại) · r1079-r1129 (force hủy + job hủy)
  · r1535-r1543 (Specchange 03/2026 — 解約待ち) · r1656-r1694 (Support #37337, Bug KH #36492)
Bổ sung: tab「Check lịch sử hợp đồng」(103 dòng — ma trận 27 loại lịch sử).
"""
from _common import tc

DTL = ("- Đăng nhập owner của hợp đồng\n"
       "- Mở /basic/point-settings → click「契約詳細」")
PAID = "- Hợp đồng standard đang 正常, còn hạn\n" + DTL

S4 = [
    # ═════════════ 19. Hủy hợp đồng & chờ hủy ═════════════
    tc("Hủy hợp đồng & chờ hủy", "UI-005", "Normal",
       "Khu 解約する của plan trả phí: nội dung + nút 有料プラン解約へ進む",
       PAID,
       "1. Cuộn tới khu「解約する」\n2. Đọc nội dung\n3. Click「有料プラン解約へ進む」",
       "contract_type = standard",
       "- Nội dung hiện「有料プランを解約できます。ダウングレードはできません」\n"
       "- Click nút → mở modal chọn lý do hủy",
       note="Nguồn: r220, r221."),

    tc("Hủy hợp đồng & chờ hủy", "FUNC-007", "Normal",
       "Hủy hợp đồng khi CÒN HẠN → chuyển sang 解約待ち, giữ quyền dùng tới hết hạn",
       PAID + "\n- expired_date_contract = 2026/12/31 (còn hạn)",
       "1. Vào khu 解約する → hoàn tất luồng hủy (chọn lý do + nhập mật khẩu)\n"
       "2. Quay lại /basic/point-settings, đọc status\n3. Kiểm tra bot_contracts.status\n"
       "4. Mở 1 tính năng bất kỳ của bot",
       "expired_date_contract = 2026/12/31",
       "- Màn list hiện status「解約待ち」\n- DB: bot_contracts.status = 2\n"
       "- Bot vẫn dùng được các tính năng tới hết expired_date",
       note="Nguồn: r1082, r1535, tab「Compare logic cũ」r17."),

    tc("Hủy hợp đồng & chờ hủy", "LIST-001", "Normal",
       "Hợp đồng 解約待ち nằm ở nhóm checkbox 契約中, không nằm ở 解約済み",
       "- Có 1 hợp đồng 解約待ち, 1 hợp đồng 解約済み, 1 hợp đồng 強制解約\n"
       "- Mở /basic/point-settings",
       "1. Chỉ tích「契約中」→ ghi danh sách\n2. Chỉ tích「解約済み」→ ghi danh sách",
       "3 hợp đồng như tiền đề",
       "- Tích 契約中: hiện hợp đồng 解約待ち\n"
       "- Tích 解約済み: hiện hợp đồng 解約済み và 強制解約 (KHÔNG có 解約待ち)",
       note="Nguồn: r1536, r1537 (Specchange 03/2026)."),

    tc("Hủy hợp đồng & chờ hủy", "FUNC-007", "Normal",
       "Hợp đồng 解約待ち vẫn mở được màn chi tiết và có nút 解約取消",
       "- Có 1 hợp đồng đang 解約待ち",
       "1. Click「契約詳細」ở dòng 解約待ち\n2. Đọc status ở màn chi tiết\n"
       "3. Quan sát nút「解約取消」\n4. Click「解約取消」\n5. Kiểm tra status và lịch sử",
       "bot_contracts.status = 2",
       "- Mở được màn chi tiết, status hiện「解約待ち」\n"
       "- Có nút「解約取消」; click thì hủy bỏ việc hủy, hợp đồng quay lại 正常 (status=1)\n"
       "- 操作履歴 ghi 2 bản ghi:「解約申し込み」và「解約の取り消し」",
       note="Nguồn: r1538-r1543 (Specchange 03/2026 mục 2: 解約待ち cho phép vào detail)."),

    tc("Hủy hợp đồng & chờ hủy", "FUNC-007", "Abnormal",
       "Nhập mật khẩu xong nhưng nút 解約 không bấm được → phải bấm được và hủy thành công",
       PAID,
       "1. Vào luồng hủy hợp đồng\n2. Chọn lý do hủy\n3. Nhập mật khẩu đúng\n"
       "4. Quan sát trạng thái nút「解約」và bấm nút",
       "Mật khẩu đúng của tài khoản đang đăng nhập",
       "- Sau khi nhập mật khẩu hợp lệ, nút「解約」chuyển sang enable\n"
       "- Bấm được và hoàn tất luồng hủy; hợp đồng chuyển sang 解約待ち/解約済み theo hạn",
       note="Nguồn: r1685-r1694 (Bug KH #36492, 18/05/2026 — nút 解約 không bấm được sau khi nhập password). "
            "Evidence bắt buộc: video thao tác."),

    tc("Hủy hợp đồng & chờ hủy", "FUNC-007", "Normal",
       "Hủy hợp đồng khi ĐANG 延滞中 → hủy luôn (status=3), không qua 解約待ち",
       "- Hợp đồng standard đang 延滞中 (quá hạn, bill lỗi)\n" + DTL,
       "1. Thực hiện luồng hủy hợp đồng\n2. Đọc status ở màn list\n3. Kiểm tra bot_contracts",
       "status=1, status_payment=2, expired_date < now",
       "- Màn list hiện status đã hủy\n- DB: status = 3 ngay lập tức (không qua trạng thái 2)",
       note="Nguồn: r1100-r1109."),

    tc("Hủy hợp đồng & chờ hủy", "JOB-001", "Normal",
       "Hợp đồng 解約待ち tới ngày hết hạn → job chuyển sang 解約済み và dọn dữ liệu",
       "- Hợp đồng 解約待ち (status=2), expired_date_contract = hôm nay\n"
       "- Quyền chạy job job:check_auto_payment_univapay",
       "1. Chờ/chạy job lúc 06:30\n2. Đọc status ở màn list\n3. Kiểm tra bot_contracts và rich_menus của bot\n"
       "4. Mở 操作履歴 của hợp đồng",
       "status=2, expired_date_contract = ngày chạy job",
       "- Màn list hiện「解約済み」\n- DB: status=3, cancel_by=1, date_cancel_contract = ngày job chạy\n"
       "- rich_menus của bot bị ẩn (status_line=0)\n- 操作履歴 có bản ghi hủy hợp đồng",
       env="PRODUCTION",
       note="Nguồn: r1090-r1099 + job-spec Phase 5 (feature-spec.md §7). RULE-08: job → PRODUCTION."),

    tc("Hủy hợp đồng & chờ hủy", "DATA-001", "Normal",
       "Force hủy plan free: bot free không có thao tác hủy hợp đồng",
       "- Hợp đồng plan free\n" + DTL,
       "1. Quan sát khu 解約する\n2. Thử tìm đường vào /basic/detail-contract/{id}/cancel bằng URL",
       "contract_type = free",
       "- Nút「この操作は行えません」disable\n"
       "- Truy cập URL cancel trực tiếp: bị chặn, không hủy được hợp đồng free",
       note="Nguồn: r157-r159, r1079-r1081. Bước 2 (URL) do AI bổ sung theo SEC-002 — CẦN LEADER XÁC NHẬN."),

    # ═════════════ 20. Cưỡng chế hủy & màn account đã hủy ═════════════
    tc("Cưỡng chế hủy & màn account đã hủy", "STATE-001", "Normal",
       "Màn account CƯỠNG CHẾ HỦY: status + text nêu ngày dự kiến thanh toán",
       "- Bot có hợp đồng 強制解約 (status=3, cancel_by=0)\n"
       "- Từ màn home chọn nhanh vào bot đó",
       "1. Quan sát status\n2. Đọc dòng text bên dưới\n3. Kiểm tra tên account + LINE ID",
       "expired_date_contract = 2026/03/01",
       "- status hiện「強制解約済」\n"
       "- Text「このアカウントの契約は決済予定日（2026/03/01）より7日間、決済が成功しなかったため"
       "強制解約されました。」với ngày được thay đúng\n- Tiêu đề hiện tên acc + LINE ID",
       note="Nguồn: r138, r139, r721-r723."),

    tc("Cưỡng chế hủy & màn account đã hủy", "STATE-001", "Normal",
       "Màn account HỦY THƯỜNG: text nêu ngày + tên user đã thao tác hủy",
       "- Bot có hợp đồng 解約済み do user bấm hủy (cancel_by=1, user_id_cancel = user A)\n"
       "- Từ màn home chọn nhanh vào bot đó",
       "1. Quan sát status\n2. Đọc dòng text bên dưới\n3. Đối chiếu tên user với users.username của user_id_cancel",
       "Ngày hủy 2026/03/05 12:34, user A =「田中太郎」",
       "- status hiện「解約済」\n"
       "- Text「このアカウントの契約は2026/03/05 12:34に田中太郎によって解約されました。」\n"
       "- Tên user hiển thị khớp users.username của user_id_cancel",
       note="Nguồn: r732-r734 + r1488-r1494 (Bug KH #35635, 04/04/2026 — từng hiện tên user KHÔNG có "
            "trong danh sách staff). Evidence bắt buộc: ảnh màn hình + query users."),

    tc("Cưỡng chế hủy & màn account đã hủy", "FUNC-001", "Normal",
       "Màn account đã hủy / cưỡng chế hủy: 3 nút điều hướng hoạt động đúng",
       "- 1 bot 解約済み và 1 bot 強制解約",
       "1. Với từng màn, click「こちら」ở khu 再契約する\n2. Click「再契約へ進む」\n"
       "3. Click「接続解除へ進む」\n4. Click「契約情報一覧に戻る」/「戻る」",
       "2 loại màn: đã hủy và cưỡng chế hủy",
       "- 「こちら」mở tab mới https://lme.jp/manual/how_to_cancel/#downgrade\n"
       "- 「再契約へ進む」mở màn hợp đồng lại\n- 「接続解除へ進む」mở màn hủy liên kết bot\n"
       "- 「契約情報一覧に戻る」/「戻る」quay về /basic/point-settings",
       note="Nguồn: r133-r136, r140-r143, r724-r726, r730, r735-r737, r741 (2 màn cùng hành vi → gộp)."),

    tc("Cưỡng chế hủy & màn account đã hủy", "FUNC-003", "Normal",
       "Màn account đã hủy: nút 過去決済分の領収書ダウンロード tải được biên lai cũ",
       "- Bot 解約済み đã từng có ≥ 2 giao dịch thanh toán thành công",
       "1. Click「過去決済分の領収書ダウンロード」\n2. Nhập thông tin biên lai trong modal\n"
       "3. Tải file và mở nội dung PDF\n4. Lặp lại trên bot 強制解約",
       "Bot có 2 giao dịch thành công trong quá khứ",
       "- Mở modal nhập thông tin biên lai (UI giống màn lịch sử bill tiền)\n"
       "- Tải được file 領収書 của đúng bot đó, nội dung khớp giao dịch trong payment_histories",
       note="Nguồn: r727-r729, r738-r740. RULE-06: phải mở file PDF."),

    tc("Cưỡng chế hủy & màn account đã hủy", "JOB-001", "Normal",
       "Job cưỡng chế hủy sau 7 ngày bill lỗi → ẩn richmenu + ghi lịch sử FORCE_CANCEL",
       "- Hợp đồng bill card, bill lỗi liên tục tới lần thứ 5 (status_payment_fail = 5)\n"
       "- Bot có ≥ 1 richmenu đang hiển thị",
       "1. Chạy job job:check_auto_payment_univapay\n2. Đọc status ở màn list\n"
       "3. Kiểm tra bot_contracts và rich_menus\n4. Mở 操作履歴 của hợp đồng\n"
       "5. Kiểm tra richmenu phía LINE app",
       "status_payment_fail = 5, bot có richmenu đang hiển thị",
       "- Màn list hiện「強制解約」\n- DB: status=3, cancel_by=0, date_cancel_contract = ngày job chạy\n"
       "- rich_menus: status_line=0, status_link=2, is_updated=2\n"
       "- Trên LINE app: richmenu của bot KHÔNG còn hiển thị\n- 操作履歴 ghi loại 強制解約",
       env="PRODUCTION",
       note="Nguồn: r1110-r1129, r453, r461 + Bug #32358 (10/10/2025 — hủy tự động không clear richmenu). "
            "RULE-06: đi tới output cuối là LINE app. RULE-08: job → PRODUCTION."),

    tc("Cưỡng chế hủy & màn account đã hủy", "JOB-001", "Normal",
       "Sau khi job cưỡng chế hủy → ngày hôm sau job KHÔNG bill lại nữa",
       "- Hợp đồng đã bị job cưỡng chế hủy hôm qua (status=3)",
       "1. Chạy lại job job:check_auto_payment_univapay hôm sau\n"
       "2. Kiểm tra UnivaPay có charge mới không\n3. Kiểm tra payment_histories",
       "status=3, cancel_by=0",
       "- KHÔNG phát sinh charge mới trên UnivaPay\n- KHÔNG thêm bản ghi payment_histories\n"
       "- Trạng thái hợp đồng giữ nguyên 強制解約",
       env="PRODUCTION",
       note="Nguồn: r453, r461, r578, r586."),

    tc("Cưỡng chế hủy & màn account đã hủy", "DATA-001", "Normal",
       "Hủy hợp đồng khi bot chưa liên kết LOA → xóa hẳn bot_contract",
       "- Slot standard đã mua nhưng CHƯA kết nối bot, đang chờ chuyển khoản/bill lỗi",
       "1. Để callback bill fail (hoặc chạy job hủy)\n2. Kiểm tra màn list và bot_contracts",
       "bot_slots.bot_id = NULL",
       "Bản ghi bot_contracts bị XÓA (không để lại dòng 解約済み), dòng biến mất khỏi màn list",
       note="Nguồn: r605 (Màn hình bill tiền). Đối chiếu job-spec Phase 5: "
            "'Nếu không còn bot_slot: DELETE bot_slots + DELETE bot_contracts'."),

    # ═════════════ 21. Hợp đồng lại ═════════════
    tc("Hợp đồng lại", "UI-001", "Normal",
       "Step 1 màn hợp đồng lại: mặc định chu kỳ bill hiện tại, cho phép đổi",
       "- Bot có hợp đồng 解約済み, chu kỳ cũ là năm",
       "1. Vào màn account đã hủy → click「再契約へ進む」\n"
       "2. Quan sát ô chọn chu kỳ bill mặc định\n3. Thử đổi sang tháng",
       "contract_bill_type cũ = year",
       "- Mặc định chọn đúng chu kỳ bill hiện tại của bot (年間一括払い)\n"
       "- Cho phép đổi sang「月払い」; có tooltip giải thích",
       note="Nguồn: r743, r747, r749."),

    tc("Hợp đồng lại", "UI-001", "Normal",
       "Step 1: 4 option phương thức thanh toán (main card / sub card / thẻ mới / chuyển khoản)",
       "- Bot 解約済み plan standard, có thẻ chính đuôi 1234 và thẻ phụ đuôi 5678",
       "1. Quan sát danh sách option phương thức thanh toán\n"
       "2. Lặp lại với bot KHÔNG có thẻ phụ",
       "Bot có thẻ chính 1234 + thẻ phụ 5678; và bot không có thẻ phụ",
       "- Option 1「登録済みクレジットカード ****-****-****-1234」(main card)\n"
       "- Option 2「登録済みクレジットカード ****-****-****-5678」(sub card) — ẩn khi bot không có thẻ phụ\n"
       "- Option 3「新規クレジットカード」\n- Option 4「銀行振込（請求書の発行ができます）」",
       note="Nguồn: r750-r754."),

    tc("Hợp đồng lại", "DATA-002", "Normal",
       "Tick 2年分まとめて払い ở màn hợp đồng lại → số tiền × 2",
       "- Bot 解約済み plan standard, chọn chu kỳ năm",
       "1. Ghi số tiền お支払い総額 khi chưa tick\n2. Tick「2年分まとめて払い」\n3. So sánh số tiền",
       "Plan standard năm (PRODUCTION: 116.424円)",
       "Số tiền = 232.848円 (税込), đúng gấp đôi giá 1 năm",
       env="PRODUCTION",
       note="Nguồn: r748. RULE-08."),

    tc("Hợp đồng lại", "FUNC-006", "Normal",
       "Hợp đồng lại bằng thẻ đã lưu (main/sub) thành công → bỏ qua step 2, sang thẳng step 3",
       "- Bot 解約済み plan standard, thẻ chính và thẻ phụ đều hợp lệ",
       "1. Chọn option main card → bấm 決済に進む\n2. Quan sát màn hình và trạng thái hợp đồng\n"
       "3. Lặp lại kịch bản với option sub card",
       "2 option: main card và sub card, thẻ hợp lệ",
       "- Cả 2 trường hợp: KHÔNG hiện step 2, sang thẳng step 3 (hợp đồng lại thành công)\n"
       "- Bill tiền thành công, tạo lịch sử bill\n- Trạng thái bot chuyển sang 正常, ngày hết hạn được cập nhật",
       env="PRODUCTION",
       note="Nguồn: r763, r765, r784. RULE-08."),

    tc("Hợp đồng lại", "FUNC-006", "Abnormal",
       "Hợp đồng lại bằng thẻ đã lưu bị lỗi → ở lại step 1, cho chọn option khác",
       "- Bot 解約済み plan standard, thẻ chính và thẻ phụ đều bị từ chối",
       "1. Chọn option main card → bấm 決済に進む\n2. Quan sát màn hình\n"
       "3. Chọn option sub card → bấm 決済に進む\n4. Quan sát màn hình",
       "Thẻ chính và thẻ phụ đều lỗi",
       "- Cả 2 lần: hiện message báo lỗi, VẪN ở lại step 1\n"
       "- User có thể chọn sang option khác để bill\n- Hợp đồng giữ nguyên trạng thái đã hủy",
       note="Nguồn: r764, r766."),

    tc("Hợp đồng lại", "FUNC-006", "Normal",
       "Hợp đồng lại bằng thẻ MỚI → mở step 2 nhập thẻ, thành công thì sang step 3",
       "- Bot 解約済み plan standard",
       "1. Chọn option「新規クレジットカード」→ bấm 決済に進む\n2. Nhập thẻ mới hợp lệ, bấm bill\n"
       "3. Kiểm tra trạng thái hợp đồng, lịch sử bill và 4 số cuối thẻ",
       "Thẻ mới 5555 5555 5555 4444",
       "- Mở step 2 nhập thẻ\n- Bill thành công → step 3 hợp đồng lại thành công\n"
       "- Trạng thái 正常, có lịch sử bill mới, thẻ chính = 4444",
       env="PRODUCTION",
       note="Nguồn: r767, r768, r781."),

    tc("Hợp đồng lại", "FUNC-006", "Abnormal",
       "Hợp đồng lại bằng thẻ mới nhưng bill lỗi → ở lại step 2, không cập nhật hợp đồng",
       "- Bot 解約済み plan standard",
       "1. Chọn「新規クレジットカード」→ step 2 nhập thẻ lỗi\n2. Quan sát màn hình\n"
       "3. Kiểm tra bot_contracts",
       "Thẻ lỗi 4111 1111 1111 1111",
       "- Báo lỗi, VẪN ở step 2 để nhập lại thẻ\n- Hợp đồng KHÔNG được cập nhật (vẫn 解約済み)",
       note="Nguồn: r769, r777."),

    tc("Hợp đồng lại", "STATE-003", "Normal",
       "Hợp đồng lại bằng chuyển khoản: 3 trạng thái theo callback",
       "- Bot 解約済み plan standard, chu kỳ năm, expired_date cũ = 2026/03/01",
       "1. Chọn option「銀行振込」→ bấm 決済に進む\n"
       "2. Khi CHƯA chuyển khoản: đọc status + expired_date + thông tin số tài khoản\n"
       "3. Chuyển khoản → callback success → đọc lại status\n"
       "4. Kịch bản khác: không chuyển khoản → callback fail → đọc lại status + expired_date",
       "expired_date cũ = 2026/03/01",
       "- Chưa chuyển khoản: status「入金待ち」(status_payment=0), expired_date = expired_date cũ + 1 năm, "
       "hiện thông tin số tài khoản vừa tạo\n"
       "- Callback success: status「正常」\n"
       "- Callback fail: status quay lại「解約済み」, expired_date = expired_date CŨ",
       env="PRODUCTION",
       note="Nguồn: r770, r778, r785-r787. ⚠ r787 ghi chú của tester: 'Check Logic từ trước đang KHÔNG "
            "update lại status của hợp đồng' — nghi ngờ hành vi thực tế khác expected, xem MT-18."),

    tc("Hợp đồng lại", "FUNC-006", "Normal",
       "Hợp đồng lại có ĐỔI chu kỳ bill → bill đúng số tiền và cập nhật chu kỳ mới",
       "- Bot 解約済み plan standard",
       "1. Hợp đồng lại: đổi từ tháng sang năm, bill card → kiểm tra số tiền, expired_date, contract_bill_type\n"
       "2. Kịch bản 2: đổi từ tháng sang năm, bill transfer\n"
       "3. Kịch bản 3: đổi từ năm sang tháng, card → card\n"
       "4. Kịch bản 4: đổi từ năm sang tháng, transfer → card",
       "4 kịch bản đổi chu kỳ như phần bước",
       "- Mỗi kịch bản bill đúng số tiền theo chu kỳ MỚI, expired_date cộng đúng kỳ mới\n"
       "- contract_bill_type cập nhật đúng; kịch bản 2 và 4 còn đổi payment_method và lưu thẻ mới nếu có",
       env="PRODUCTION",
       note="Nguồn: r788-r791 (4 dòng cùng nhóm kết quả → gộp, liệt kê đủ 4 kịch bản). RULE-08."),

    tc("Hợp đồng lại", "DATA-001", "Normal",
       "Hợp đồng lại → datetime_first_payment cập nhật thành ngày hiện tại",
       "- Bot 解約済み (hoặc 強制解約), datetime_first_payment cũ = ngày 15",
       "1. Ghi lại datetime_first_payment cũ\n2. Thực hiện hợp đồng lại thành công vào ngày 03 của tháng\n"
       "3. Kiểm tra bot_contracts.datetime_first_payment và expired_date_contract",
       "datetime_first_payment cũ = ngày 15; ngày thực hiện = ngày 03",
       "- datetime_first_payment = ngày hiện tại (ngày 03)\n"
       "- expired_date_contract tính theo ngày 03 (không giữ mốc ngày 15 cũ)",
       note="Nguồn: tab「Cố định ngày bill tiền」r11-r13, r17, r18 (07/2023). "
            "⚠ TC > 2 năm tuổi — CẦN VERIFY LẠI trên bản hiện hành."),

    tc("Hợp đồng lại", "UI-001", "Normal",
       "Step 3 hợp đồng lại: hiện đúng tên plan + nút ホームに戻る",
       "- Vừa hợp đồng lại thành công cho plan standard và plan pro",
       "1. Ở step 3, đọc text plan\n2. Bấm「ホームに戻る」",
       "2 plan: standard và pro",
       "- standard hiện「スタンダードプラン」, pro hiện「プロプラン」\n"
       "- Bấm「ホームに戻る」→ về /admin/home",
       note="Nguồn: r782, r783."),

    # ═════════════ 22. Ngắt kết nối LOA & xóa account ═════════════
    tc("Ngắt kết nối LOA & xóa account", "FUNC-007", "Normal",
       "Plan free đã kết nối bot: ngắt kết nối → XÓA luôn hợp đồng khỏi màn quản lý",
       "- Hợp đồng plan free đã kết nối bot\n" + DTL,
       "1. Quan sát nút「接続解除」\n2. Click「接続解除へ進む」→ xác nhận\n"
       "3. Kiểm tra màn /basic/point-settings\n4. Kiểm tra bot_contracts và bot_slots",
       "contract_type = free, đã kết nối bot",
       "- Nút「接続解除」hiển thị và click được\n"
       "- Sau khi ngắt: hợp đồng biến mất khỏi màn quản lý hợp đồng\n"
       "- DB: bản ghi bot_contracts và bot_slots tương ứng bị XÓA",
       note="Nguồn: r1657-r1659 (Support #37337). ⚠ Xóa hẳn dữ liệu — evidence bắt buộc: "
            "ảnh màn hình + query DB trước/sau."),

    tc("Ngắt kết nối LOA & xóa account", "UI-005", "Abnormal",
       "Plan free CHƯA kết nối bot (do super admin downgrade) → nút 接続解除 hiện nhưng disable",
       "- Slot standard chưa kết nối bot, được super admin downgrade thành free\n" + DTL,
       "1. Quan sát nút「接続解除」\n2. Thử click",
       "contract_type = free, bot_slots.bot_id = NULL",
       "- Nút「接続解除」hiển thị nhưng KHÔNG click được (disable)\n"
       "- Các nút khác hiển thị bình thường theo design",
       note="Nguồn: r1660 (Support #37337)."),

    tc("Ngắt kết nối LOA & xóa account", "FUNC-007", "Normal",
       "Hợp đồng trả phí ở trạng thái 解約待ち → vẫn ngắt kết nối LOA được",
       "- Hợp đồng standard ở trạng thái 解約待ち (status=2), đã kết nối bot\n" + DTL,
       "1. Quan sát nút「接続解除へ進む」\n2. Click và hoàn tất ngắt kết nối\n"
       "3. Kiểm tra màn list và bot_slots",
       "status = 2",
       "- Nút「接続解除へ進む」hiển thị và click được\n"
       "- Ngắt kết nối thành công, bot_slots.bot_id được gỡ\n"
       "- Bản ghi được ghi vào lịch sử ngắt kết nối",
       note="Nguồn: r1656-r1683 (Support #37337, 11192 — sau khi hủy gói trả phí không ngắt kết nối được)."),

    tc("Ngắt kết nối LOA & xóa account", "DATA-004", "Normal",
       "Đã 接続解除 → job bill KHÔNG được trừ tiền hợp đồng đó nữa",
       "- Bot đã 接続解除 ngày 2026/04/08, hợp đồng standard bill card\n"
       "- expired_date_contract rơi vào 2026/04/12",
       "1. Chạy job bill ngày 2026/04/12\n2. Kiểm tra UnivaPay có charge không\n"
       "3. Kiểm tra payment_histories và bot_contracts",
       "Ngày ngắt kết nối 2026/04/08 < ngày bill 2026/04/12",
       "- KHÔNG phát sinh charge trên UnivaPay\n- KHÔNG có bản ghi payment_histories mới\n"
       "- Hợp đồng không bị gia hạn thêm kỳ",
       env="PRODUCTION",
       note="Nguồn: r1654, r1655 (Bug KH #36373, 12/05/2026 — đã ngắt kết nối vẫn bị trừ tiền). "
            "Fix 22/5: xóa luôn slot khi ngắt kết nối. RULE-08: job + bill tiền → PRODUCTION."),

    tc("Ngắt kết nối LOA & xóa account", "FUNC-007", "Normal",
       "Nút エルメアカウント削除へ進む → xóa toàn bộ dữ liệu tài khoản LME",
       "- Tài khoản test riêng, plan free, KHÔNG dùng chung dữ liệu với case khác\n" + DTL,
       "1. Click「エルメアカウント削除へ進む」\n2. Hoàn tất luồng xác nhận\n"
       "3. Thử đăng nhập lại bằng tài khoản đó",
       "Tài khoản test dùng 1 lần",
       "- Tài khoản LME bị xóa\n- Không đăng nhập lại được bằng tài khoản đó",
       note="Nguồn: r165-r168. ⚠ Thao tác KHÔNG hoàn tác được — bắt buộc dùng tài khoản test riêng."),

    # ═════════════ 23. Lịch sử thao tác hợp đồng ═════════════
    tc("Lịch sử thao tác hợp đồng", "UI-001", "Normal",
       "Khu 操作履歴: title アクティビティログ + danh sách theo thời gian",
       "- Hợp đồng có ≥ 5 bản ghi lịch sử\n" + DTL,
       "1. Cuộn tới khu 操作履歴\n2. Đọc title\n3. Kiểm tra thứ tự thời gian các bản ghi",
       "≥ 5 bản ghi bot_life_cycles",
       "- Title hiển thị「アクティビティログ」\n"
       "- Danh sách hiện đúng các thao tác của hợp đồng, sắp theo thời gian",
       note="Nguồn: r236, r607."),

    tc("Lịch sử thao tác hợp đồng", "FUNC-001", "Normal",
       "Click 1 dòng lịch sử → mở modal chi tiết tương ứng",
       "- Hợp đồng có bản ghi lịch sử bill tiền\n" + DTL,
       "1. Click/double-click vào 1 dòng lịch sử\n2. Quan sát modal mở ra",
       "1 bản ghi lịch sử bất kỳ",
       "Mở modal chi tiết đúng loại sự kiện của dòng vừa click; double-click không mở 2 modal",
       note="Nguồn: r608."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Normal",
       "Nhóm 1 (Start): lịch sử liên kết LOA — plan free và plan trả phí",
       "- 1 bot liên kết plan free, 1 bot liên kết plan standard\n" + DTL,
       "1. Mở modal lịch sử của bot free (type=1) → đọc nội dung\n"
       "2. Mở modal lịch sử của bot standard (type=2) → đọc nội dung",
       "bot_life_cycles: status=1 type=1 và status=1 type=2",
       "- type=1: tiêu đề「LINE公式アカウント接続（フリープラン）」, hiện tên acc, plan, "
       "thời gian YYYY/MM/DD hh:mm, user thao tác\n"
       "- type=2: tiêu đề「LINE公式アカウント接続（〇〇プラン）」với đủ các trường trên",
       note="Nguồn: r609-r611 + tab「Check lịch sử hợp đồng」r3-r9."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Normal",
       "Nhóm 2 (Bill): 8 loại lịch sử thanh toán hiển thị đúng tiêu đề và đủ trường",
       "- Hợp đồng đã trải qua các sự kiện: bắt đầu tháng, bắt đầu năm, upgrade, "
       "job bill tháng, job bill năm, tái ký tháng, tái ký năm, bill theo số bạn bè\n" + DTL,
       "1. Mở lần lượt 8 modal lịch sử tương ứng\n2. Đối chiếu tiêu đề và các trường",
       "bot_life_cycles type = 3, 4, 5, 6, 7, 8, 9, 10",
       "- 〇〇プラン　月払い開始 (type=3) · 〇〇プラン　年間一括払い開始 (type=4)\n"
       "- 〇〇プラン　更新（毎月）(type=5) · 〇〇プラン　更新（年間一括）(type=8)\n"
       "- プロプラン　アップグレード（日割り）(type=7) · 友だち数別の従量課金 (type=6)\n"
       "- 〇〇プラン　月払い再契約 / 年払い再契約 (type=9) · 1年間の契約延長 (type=10)\n"
       "- Mỗi modal đủ trường: tên acc, plan, thời gian, số tiền, kỳ hạn, phương thức thanh toán, user thao tác",
       note="Nguồn: r612-r626 + tab「Check lịch sử hợp đồng」r10-r46 (gộp theo nhóm, liệt kê đủ 8 loại). "
            "⚠ Tab Check lịch sử ghi nhận 3 NG chưa fix: r14 'upgrade free→pro năm lại có thêm lịch sử gia hạn', "
            "r34/r37 'tái ký bị hiện thêm lịch sử đổi thẻ chính', r39/r40 'không lấy được thông tin thời gian "
            "extend / thông tin bot' — xem MT-19."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Normal",
       "Nhóm 3 (Change): 8 loại lịch sử thay đổi hợp đồng",
       "- Hợp đồng đã trải qua: đổi thẻ chính, đăng ký/đổi/xóa thẻ phụ, đổi phương thức 2 chiều, "
       "đổi kỳ 2 chiều, đổi LOA, thêm/xóa staff\n" + DTL,
       "1. Mở lần lượt các modal lịch sử nhóm Change\n2. Đối chiếu tiêu đề và trường hiển thị",
       "bot_life_cycles type = 11, 12, 13, 24, 14, 22, 15, 16, 25",
       "- メインクレジットカード変更 (11) · サブクレジットカード登録 (12) · サブクレジットカード変更 (13) · "
       "サブカード削除 (24)\n- 決済方法変更 transfer→card (14) và card→transfer (22)\n"
       "- 支払い期間変更 年間一括→毎月 (15) và 毎月→年間一括 (16)\n"
       "- Change LOA · 追加/削除スタッフ (24/25)\n"
       "- Mỗi modal hiện đủ trường liên quan (thông tin thẻ sau khi đổi, phương thức trước→sau, staff…)",
       note="Nguồn: r629-r639 + tab Check lịch sử r47-r52. ⚠ Corpus ghi type=24 cho CẢ 'xóa sub card' và "
            "'thêm staff', type=16 cho CẢ 'đổi kỳ tháng→năm' và 'change LOA' — trùng mã type, xem MT-20."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Normal",
       "Nhóm 4 (Hủy/Lỗi): 5 loại lịch sử hủy và lỗi thanh toán",
       "- Hợp đồng đã trải qua: hủy chuyển khoản, yêu cầu hủy, hủy bỏ việc hủy, đã hủy, cưỡng chế hủy, bill lỗi\n" + DTL,
       "1. Mở lần lượt các modal nhóm hủy/lỗi\n2. Đối chiếu trường hiển thị",
       "bot_life_cycles status=4, type = 17, 18, 27, 19, 21, 20",
       "- cancel transfer (17) · 解約申し込み (18) · 解約の取り消し (27) · 解約済み (19) · "
       "強制解約 (21) · 決済エラー (20)\n"
       "- Modal 決済エラー hiển thị thêm ID thanh toán và số lần thanh toán\n"
       "- Modal 解約済み/強制解約 hiển thị thời gian hủy và user thao tác",
       note="Nguồn: r640-r645. Đối chiếu feature-spec.md §2 (bảng loại sự kiện, 決済エラー = type 20)."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Abnormal",
       "Modal lịch sử của hợp đồng mua mới CHƯA kết nối bot → ẩn dòng tên bot",
       "- Hợp đồng standard vừa mua mới, chưa kết nối LOA",
       "1. Mở màn chi tiết hợp đồng → khu 操作履歴\n"
       "2. Mở modal lịch sử「〇〇プラン　月払い開始」\n3. Quan sát dòng tên bot",
       "bot_slots.bot_id = NULL",
       "Modal ẩn dòng tên bot (không hiện tên bot rỗng / không hiện nhầm plan free)",
       note="Nguồn: r1155-r1168 (Bug KH #34408, 11/02/2026 — standard plan lại hiện free plan "
            "và 'chưa kết nối LOA')."),

    tc("Lịch sử thao tác hợp đồng", "DATA-004", "Normal",
       "Job bill hàng tháng → lịch sử bot_life_cycle lưu charge id của THÁNG HIỆN TẠI",
       "- Hợp đồng standard tháng bill card, đã có lịch sử bill của tháng trước",
       "1. Chạy job bill tháng này\n2. Mở modal lịch sử「〇〇プラン　更新（毎月）」\n"
       "3. Đối chiếu charge id trong modal với charge id vừa tạo trên UnivaPay\n"
       "4. Lặp lại với hợp đồng bill năm (modal 更新（年間一括）)",
       "Hợp đồng đã có ≥ 2 kỳ bill",
       "Modal lịch sử hiển thị charge id của kỳ bill VỪA CHẠY, không phải charge id của tháng cũ",
       env="PRODUCTION",
       note="Nguồn: r1723-r1731 (Bug KH #39059, 25/07/2026). RULE-08: job + bill tiền → PRODUCTION."),

    tc("Lịch sử thao tác hợp đồng", "DATA-001", "Normal",
       "Lịch sử bill tiền hiển thị đúng THẺ đã dùng tại thời điểm thanh toán",
       "- Hợp đồng đã bill bằng thẻ đuôi 1234, sau đó đổi thẻ chính sang đuôi 4444, rồi bill kỳ mới",
       "1. Mở màn lịch sử thanh toán\n"
       "2. Đọc cột 決済方法 của bản ghi kỳ CŨ và kỳ MỚI\n"
       "3. Đối chiếu payment_histories.last_four_card của từng bản ghi",
       "Thẻ cũ 1234 (kỳ 1), thẻ mới 4444 (kỳ 2)",
       "- Bản ghi kỳ 1 hiện「クレジットカード（1234）」\n- Bản ghi kỳ 2 hiện「クレジットカード（4444）」\n"
       "- Không lấy thẻ hiện tại áp cho toàn bộ lịch sử",
       note="Nguồn: r1229-r1291 (SpecImprove #34505, 19/03/2026 — thêm cột payment_histories.last_four_card). "
            "Cột `last_four_card` KHÔNG có trong db-mapping của spec — xem MT-13."),

    # ═════════════ 24. Lịch sử ngắt kết nối LOA ═════════════
    tc("Lịch sử ngắt kết nối LOA", "UI-001", "Normal",
       "Màn 接続解除履歴: breadcrumb + cảnh báo + bảng 3 cột",
       "- Tài khoản đã từng ngắt kết nối ≥ 1 LOA\n- Mở /basic/disconnect-history",
       "1. Đọc breadcrumb và tiêu đề\n2. Đọc dòng cảnh báo\n3. Liệt kê các cột của bảng",
       "≥ 1 bản ghi ngắt kết nối",
       "- Breadcrumb「TOP > 接続解除履歴」\n"
       "- Cảnh báo「接続解除したLINE公式アカウントの復元はできません。」\n"
       "- Bảng 3 cột: 接続解除日時 | LINE公式アカウント名 | 操作したユーザー",
       note="Nguồn: r15 + feature-spec.md §2 SCR-BLP-04."),

    tc("Lịch sử ngắt kết nối LOA", "DATA-001", "Normal",
       "Dữ liệu bảng lấy snapshot tại thời điểm ngắt (không đổi khi bot đổi tên)",
       "- Đã ngắt kết nối bot tên「テストBOT」bởi user「田中太郎」ngày 2026/03/01 10:00",
       "1. Mở /basic/disconnect-history\n2. Đối chiếu 3 cột với bot_life_cycles type=28\n"
       "3. Đổi tên bot khác (nếu bot còn tồn tại) rồi reload trang",
       "bot_life_cycles type=28, data->bot_name =「テストBOT」",
       "- 接続解除日時 = time_action (2026/03/01 10:00)\n"
       "- LINE公式アカウント名 lấy từ data->bot_name + data->bot_line_id (snapshot)\n"
       "- 操作したユーザー lấy từ data->operator_name\n"
       "- Đổi tên bot sau đó KHÔNG làm đổi tên trong lịch sử",
       note="Nguồn: feature-spec.md §2 SCR-BLP-04 + Field Matrix #33-#35. Corpus KHÔNG có TC chi tiết "
            "cho màn này → TC do AI viết dựa trên spec, CẦN LEADER XÁC NHẬN. Xem MT-21."),

    tc("Lịch sử ngắt kết nối LOA", "LIST-002", "Abnormal",
       "Chưa từng ngắt kết nối LOA nào → empty state まだデータがありません",
       "- Tài khoản chưa từng ngắt kết nối LOA",
       "1. Mở /basic/disconnect-history\n2. Quan sát vùng bảng",
       "0 bản ghi bot_life_cycles type=28",
       "Hiển thị text「まだデータがありません」, không hiện bảng lỗi",
       note="Nguồn: r16."),

    tc("Lịch sử ngắt kết nối LOA", "LIST-003", "Boundary",
       "Nhiều bản ghi ngắt kết nối → phân trang 100 bản ghi/trang hoạt động đúng",
       "- Tài khoản có ≥ 150 bản ghi ngắt kết nối LOA",
       "1. Mở /basic/disconnect-history\n2. Đếm số dòng trang 1\n3. Sang trang 2 và đếm",
       "≥ 150 bản ghi",
       "- Trang 1 hiện 100 bản ghi\n- Trang 2 hiện phần còn lại\n"
       "- Không mất/nhân đôi bản ghi giữa 2 trang",
       note="Nguồn: EP-06 /ajax/bot-life-cycle?per_page=100 (feature-spec.md §2). "
            "TC do AI viết theo spec — corpus không có, CẦN LEADER XÁC NHẬN. Xem MT-21."),
]
