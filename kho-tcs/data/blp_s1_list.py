# -*- coding: utf-8 -*-
"""FA-031 契約プラン・決済情報 (Bill tiền tool) — Nhóm 1-4: màn danh sách hợp đồng.

Nguồn chính: TCsLine_Bill tiền_Improve2025 → tab「Quản lý hợp đồng」(12/2025 → 07/2026,
1731 dòng, 1506 TC lá — tab MASTER còn sống, 15 cột kết quả theo ticket).
Bổ sung: tab「Compare logic cũ」(bảng đối chiếu status list bot cũ ↔ list hợp đồng mới).
"""
from _common import tc

ADM = ("- Đăng nhập LME bằng tài khoản 主管理者 (owner) có ≥ 1 hợp đồng\n"
       "- Mở /basic/point-settings (「契約情報・領収書」)")
MIX = (ADM + "\n- Dữ liệu seed: 1 hợp đồng 正常, 1 hợp đồng 延滞中, 1 hợp đồng 入金待ち, "
       "1 hợp đồng 解約済み, 1 hợp đồng 強制解約")

S1 = [
    # ═════════════ 1. Màn list hợp đồng — hiển thị & lọc ═════════════
    tc("Màn list hợp đồng — hiển thị & lọc", "UI-001", "Normal",
       "Mở màn danh sách hợp đồng → title 契約情報・領収書 + đủ 3 nút header + bảng 8 cột",
       MIX,
       "1. Mở /basic/point-settings\n"
       "2. Đọc tiêu đề trang\n"
       "3. Quan sát vùng header và bảng danh sách",
       "Tài khoản có 5 hợp đồng như phần tiền đề",
       "- Tiêu đề trang hiển thị「契約情報・領収書」\n"
       "- Header có 3 nút:「ご契約に関する注意事項」·「接続解除履歴」·「領収書の発行」\n"
       "- Bảng có đủ 8 cột: LINE公式アカウント名 | ご利用プラン | ステータス | "
       "ご利用料金/振込情報 | 決済方法 | 次回決済(更新)日 | LOA接続日 | 契約の変更・解約",
       note="Nguồn: r7, r9. Đối chiếu feature-spec.md §2 SCR-BLP-01."),

    tc("Màn list hợp đồng — hiển thị & lọc", "FUNC-001", "Normal",
       "Click「ご契約に関する注意事項」→ mở modal điều khoản hợp đồng",
       ADM,
       "1. Mở /basic/point-settings\n2. Click nút「ご契約に関する注意事項」",
       "—",
       "- Mở modal「ご契約に関する注意事項」\n"
       "- Nội dung nêu: thẻ tín dụng hiện tên「L Message / エルメッセージ」trên sao kê; "
       "hủy hợp đồng không hoàn tiền theo ngày; không downgrade được; hợp đồng tự động gia hạn; "
       "chuyển khoản vào tài khoản「ｶ)ﾕﾆｳﾞｧﾍﾟｲｷｬｽﾄ」",
       note="Nguồn: r8. Nội dung modal đối chiếu feature-spec.md §2 (Modal điều khoản hợp đồng)."),

    tc("Màn list hợp đồng — hiển thị & lọc", "FUNC-001", "Normal",
       "Click/double-click「領収書の発行」→ chuyển sang màn lịch sử hóa đơn",
       ADM,
       "1. Mở /basic/point-settings\n2. Click nút「領収書の発行」\n3. Quay lại, double-click cùng nút đó",
       "—",
       "- Chuyển sang /basic/payment-history\n"
       "- Double-click chỉ mở 1 lần, không mở 2 tab / không lỗi JS",
       note="Nguồn: r9."),

    tc("Màn list hợp đồng — hiển thị & lọc", "FUNC-001", "Normal",
       "Click「接続解除履歴」→ chuyển sang màn lịch sử ngắt kết nối",
       ADM,
       "1. Mở /basic/point-settings\n2. Click nút「接続解除履歴」",
       "—",
       "Chuyển sang màn「接続解除履歴」(/basic/disconnect-history)",
       note="Nguồn: r15."),

    tc("Màn list hợp đồng — hiển thị & lọc", "LIST-001", "Normal",
       "Mặc định 2 checkbox 契約中 + 解約済み đều tích → hiện tất cả hợp đồng",
       MIX,
       "1. Mở /basic/point-settings\n2. Quan sát 2 checkbox lọc\n3. Đếm số dòng hiển thị",
       "5 hợp đồng gồm cả đang hợp đồng và đã hủy",
       "- Cả 2 checkbox「契約中」và「解約済み」đều được tích sẵn\n"
       "- Danh sách hiện đủ 5 hợp đồng (cả đang hợp đồng lẫn đã hủy)",
       note="Nguồn: r10."),

    tc("Màn list hợp đồng — hiển thị & lọc", "LIST-001", "Normal",
       "Bỏ tích「契約中」→ chỉ còn hợp đồng đã hủy",
       MIX,
       "1. Bỏ tích checkbox「契約中」\n2. Quan sát danh sách",
       "—",
       "Chỉ hiển thị các hợp đồng có trạng thái 解約済み / 強制解約; "
       "không còn dòng 正常 / 延滞中 / 入金待ち",
       note="Nguồn: r11."),

    tc("Màn list hợp đồng — hiển thị & lọc", "LIST-001", "Normal",
       "Bỏ tích「解約済み」→ chỉ còn hợp đồng đang hợp đồng",
       MIX,
       "1. Bỏ tích checkbox「解約済み」\n2. Quan sát danh sách",
       "—",
       "Chỉ hiển thị hợp đồng đang hiệu lực (正常 / 延滞中 / 入金待ち / 口座発行中 / 解約待ち); "
       "không còn dòng 解約済み / 強制解約",
       note="Nguồn: r12. ⚠ TC gốc ghi ngược 2 dòng r11/r12 (bỏ 契約中 → 'Chỉ hiển thị List hợp đồng đã hủy'); "
            "đã sửa lại theo nghĩa đúng — xem MT-01."),

    tc("Màn list hợp đồng — hiển thị & lọc", "LIST-002", "Abnormal",
       "Bỏ tích cả 2 checkbox → hiện empty state アカウントが接続されていません",
       MIX,
       "1. Bỏ tích cả「契約中」và「解約済み」\n2. Quan sát vùng danh sách",
       "—",
       "Bảng trống, hiển thị màn/empty text「アカウントが接続されていません」",
       note="Nguồn: r13."),

    tc("Màn list hợp đồng — hiển thị & lọc", "FUNC-001", "Normal",
       "Click「フリープランで接続する」khi chưa có bot free → sang màn add bot",
       "- Đăng nhập owner CHƯA có bot free nào\n- Mở /basic/point-settings",
       "1. Quan sát nút「フリープランで接続する」\n2. Click nút",
       "User tạo sau 01/07/2021, chưa có bot free",
       "Chuyển sang màn add bot (/admin/bot-add-v2)",
       note="Nguồn: r14, r31 (List main case)."),

    tc("Màn list hợp đồng — hiển thị & lọc", "LIST-002", "Abnormal",
       "Tài khoản chưa có hợp đồng nào → empty state của màn list",
       "- Đăng nhập tài khoản mới tạo, chưa kết nối LOA và chưa mua slot nào",
       "1. Mở /basic/point-settings\n2. Quan sát vùng danh sách",
       "Tài khoản 0 hợp đồng",
       "Hiển thị text「まだデータがありません」/「アカウントが接続されていません」, "
       "không hiện bảng rỗng có header lỗi",
       note="Nguồn: r16. ⚠ Corpus ghi text ở khối 接続解除履歴; cần verify text chính xác trên màn list — xem MT-02."),

    # ═════════════ 2. Cột & trạng thái hợp đồng ═════════════
    tc("Cột & trạng thái hợp đồng", "UI-001", "Normal",
       "Cột LINE公式アカウント名 hiện tên account ở trên, LINE ID ở dưới",
       ADM + "\n- Hợp đồng đã kết nối bot「テストBOT」LINE ID @test001",
       "1. Mở /basic/point-settings\n2. Quan sát ô cột 1 của dòng hợp đồng đã kết nối bot",
       "bot view_name =「テストBOT」, line_id = @test001",
       "- Dòng trên: tên account LINE「テストBOT」\n- Dòng dưới: LINE ID @test001\n- Có ảnh đại diện bot",
       note="Nguồn: r25. Field Matrix #1-#3 (feature-spec.md §4)."),

    tc("Cột & trạng thái hợp đồng", "UI-002", "Boundary",
       "Tên account > 20 ký tự → cắt 3 chấm, hover hiện tooltip đầy đủ",
       ADM + "\n- Bot có view_name dài 30 ký tự",
       "1. Quan sát ô tên account\n2. Rê chuột lên tên",
       "view_name = 「あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ」(30 ký tự)",
       "- Hiển thị tối đa 20 ký tự + dấu「…」\n- Hover hiện tooltip đầy đủ 30 ký tự\n- Không vỡ layout dòng",
       note="Nguồn: r26; Bug Tester #35852 (r564-r570 tab Màn hình bill tiền — tên 主管理者 dài)."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Slot đã mua nhưng chưa kết nối bot → hiện LINE公式アカウント未接続, không có LINE ID",
       ADM + "\n- Có 1 slot standard đã thanh toán nhưng chưa kết nối LOA",
       "1. Quan sát dòng của slot chưa kết nối\n"
       "2. Kiểm tra bảng bot_slots của slot đó",
       "bot_slots.bot_id = NULL",
       "- Cột 1 hiện text「LINE公式アカウント未接続」\n- Không hiển thị LINE ID\n"
       "- DB: bot_slots.bot_id = NULL",
       note="Nguồn: r27."),

    tc("Cột & trạng thái hợp đồng", "FUNC-001", "Normal",
       "Slot chưa kết nối + hợp đồng đang active → text xanh gạch chân, click mở màn liên kết bot",
       ADM + "\n- Slot standard chưa kết nối bot, hợp đồng status = 正常",
       "1. Quan sát text「LINE公式アカウント未接続」\n2. Click vào text đó",
       "Slot standard, bot_contracts.status = 1",
       "- Text hiển thị màu xanh, có gạch chân (dạng link)\n"
       "- Click → mở màn liên kết bot cho đúng slot đó",
       note="Nguồn: r28, r29."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Kết nối bot vào slot trống (standard / pro / enterprise) → tên bot thay thế text 未接続",
       ADM + "\n- Có slot trống của cả 3 loại: standard, pro, enterprise",
       "1. Click text 未接続 của slot standard → hoàn tất liên kết bot\n"
       "2. Lặp lại với slot pro\n"
       "3. Lặp lại với slot enterprise\n"
       "4. Quay lại /basic/point-settings và kiểm tra bảng bot_slots",
       "3 slot: standard, pro, enterprise",
       "- Cả 3 dòng: text「LINE公式アカウント未接続」được thay bằng tên bot vừa kết nối\n"
       "- DB: bot_slots.bot_id được ghi giá trị bot vừa liên kết cho từng slot",
       note="Nguồn: r30-r32 (3 dòng cùng kết quả → gộp 1 TC, liệt kê đủ 3 loại slot ở Dữ liệu test)."),

    tc("Cột & trạng thái hợp đồng", "UI-001", "Normal",
       "Hợp đồng enterprise → cột 1 hiện おまとめ割引 + số slot 枠",
       ADM + "\n- Có 1 hợp đồng enterprise 10 slot và 1 hợp đồng enterprise 20 slot",
       "1. Quan sát cột 1 của 2 dòng hợp đồng enterprise",
       "Hợp đồng EP 10 slot và EP 20 slot",
       "- Hợp đồng 10 slot: hiện「おまとめ割引」+「10枠」\n"
       "- Hợp đồng 20 slot: hiện「おまとめ割引」+「20枠」\n"
       "- KHÔNG hiển thị tên và ảnh của bot",
       note="Nguồn: r33, r250, r277."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Cột ご利用プラン hiện đúng tên plan theo contract_type",
       ADM + "\n- Có hợp đồng free, standard, pro",
       "1. Quan sát cột「ご利用プラン」của 3 dòng",
       "contract_type = free / standard / pro",
       "- free →「フリー」\n- standard →「スタンダード」\n- pro →「プロ」",
       note="Nguồn: r34. Field Matrix #4."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Cột ご利用プラン hiện thêm chu kỳ thanh toán theo contract_bill_type",
       ADM + "\n- Có 4 hợp đồng: standard/tháng, standard/năm, pro/tháng, pro/năm",
       "1. Quan sát dòng thứ 2 của cột「ご利用プラン」ở cả 4 hợp đồng",
       "contract_bill_type = month / year",
       "- standard + năm →「スタンダード」/「年間一括払い」\n"
       "- standard + tháng →「スタンダード」/「月払い」\n"
       "- pro + năm →「プロ」/「年間一括払い」\n"
       "- pro + tháng →「プロ」/「月払い」",
       note="Nguồn: r35-r38 (4 dòng, cùng quy tắc hiển thị → gộp, liệt kê đủ 4 tổ hợp)."),

    tc("Cột & trạng thái hợp đồng", "STATE-001", "Normal",
       "Cột ステータス hiện đủ 6 trạng thái theo điều kiện DB",
       MIX + "\n- Thêm 1 hợp đồng 口座発行中",
       "1. Quan sát cột「ステータス」của từng dòng\n"
       "2. Đối chiếu với bot_contracts.status / status_payment / payment_method / expired_date_contract",
       "6 hợp đồng ứng với 6 trạng thái",
       "- 正常 (status=1, status_payment IN(0,1), expired > now)\n"
       "- 延滞中 (status=1, bill lỗi, expired_date_contract < now)\n"
       "- 口座発行中 (payment_method=2, status_payment=5, univa_account_number IS NULL)\n"
       "- 入金待ち (payment_method=2, status_payment NOT IN(1,2), có univa_account_number)\n"
       "- 解約済み (status=3, cancel_by=1)\n"
       "- 強制解約 (status=3, cancel_by=0)",
       note="Nguồn: r39 + tab「Compare logic cũ」r3-r18. Đối chiếu feature-spec.md §2 bảng trạng thái computed. "
            "Corpus có thêm 解約待ち (status=2) — xem TC riêng ở nhóm 『Hủy hợp đồng & chờ hủy』."),

    tc("Cột & trạng thái hợp đồng", "UI-003", "Normal",
       "Hover icon i của status 入金待ち → tooltip giải thích thời gian kích hoạt",
       ADM + "\n- Có 1 hợp đồng status 入金待ち",
       "1. Rê chuột lên icon「i」cạnh chữ 入金待ち\n2. Đọc nội dung tooltip",
       "Hợp đồng bill transfer, status_payment = 4",
       "Tooltip hiện đúng nguyên văn:「決済システムが随時入金を確認していますので通常はお振込操作後、"
       "数分~数時間で有料プランが有効化されます。土日祝を挟む場合は有効化が遅れる可能性があります。」",
       note="Nguồn: r40."),

    tc("Cột & trạng thái hợp đồng", "UI-003", "Normal",
       "Hover icon i của status 強制解約 → tooltip nêu lý do 7 ngày",
       ADM + "\n- Có 1 hợp đồng status 強制解約",
       "1. Rê chuột lên icon「i」cạnh chữ 強制解約\n2. Đọc nội dung tooltip",
       "bot_contracts.status=3, cancel_by=0",
       "Tooltip hiện đúng nguyên văn:「決済予定日から7日以上決済が行われなかったため、強制解約となりました。"
       "「アカウントの操作」から再契約を行うことで、解約時の状態から利用の再開が可能です。」",
       note="Nguồn: r44."),

    tc("Cột & trạng thái hợp đồng", "UI-002", "Abnormal",
       "Cuộn trang khi đang mở pop-over icon i → pop-over KHÔNG bị che khuất",
       ADM + "\n- Danh sách có ≥ 15 hợp đồng để trang có thanh cuộn\n- Có hợp đồng 強制解約 và 入金待ち",
       "1. Hover/click icon「i」ở dòng 強制解約 để mở pop-over\n"
       "2. Cuộn trang lên/xuống\n"
       "3. Lặp lại với dòng 入金待ち",
       "≥ 15 hợp đồng",
       "- Pop-over hiển thị đầy đủ, không bị dòng/khối phía dưới đè lên (z-index đúng)\n"
       "- Cuộn trang thì pop-over bám đúng icon hoặc đóng lại, không bị cắt nửa",
       note="Nguồn: r1145-r1153 (Bug KH #34384, 10/02/2026). Evidence bắt buộc: ảnh chụp lúc đang cuộn."),

    tc("Cột & trạng thái hợp đồng", "DATA-002", "Normal",
       "Cột ご利用料金 format số tiền: 0 → ¥ 0; khác 0 → ¥ số tiền / 月",
       ADM + "\n- Có 1 hợp đồng free (amount_payment = 0) và 1 hợp đồng standard tháng",
       "1. Quan sát cột「ご利用料金」ở cả 2 dòng",
       "amount_payment = 0 và amount_payment = 10780",
       "- Hợp đồng free: hiển thị「¥ 0」\n- Hợp đồng standard tháng: hiển thị「¥ 10,780 / 月」(có dấu phân cách nghìn)",
       note="Nguồn: r54, r55."),

    tc("Cột & trạng thái hợp đồng", "DATA-002", "Normal",
       "Status 入金待ち → cột 4 hiện 振込情報 kèm hạn chuyển khoản format yyyy/mm/dd hh:mm",
       ADM + "\n- Có 1 hợp đồng bill transfer đang 入金待ち",
       "1. Quan sát cột「ご利用料金 / 振込情報」của dòng 入金待ち\n"
       "2. Đối chiếu với bot_contracts.expired_date_bank_transfer",
       "expired_date_bank_transfer = 2026-02-11 23:59",
       "Hiển thị text hạn chuyển khoản + ngày giờ đúng format yyyy/mm/dd hh:mm, khớp expired_date_bank_transfer",
       note="Nguồn: r56. Field Matrix #11."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Hợp đồng đã hủy / cưỡng chế hủy → cột ご利用料金 hiện dấu \"-\"",
       ADM + "\n- Có 1 hợp đồng 解約済み và 1 hợp đồng 強制解約",
       "1. Quan sát cột「ご利用料金」của 2 dòng đã hủy",
       "status = 3 (cancel_by = 1 và cancel_by = 0)",
       "Cả 2 dòng đều hiển thị「-」, không hiển thị số tiền cũ",
       note="Nguồn: r57, r58 (2 dòng cùng expected → gộp, nêu đủ 2 loại hủy)."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Cột 決済方法 hiện đúng 3 dạng: 銀行振込 / カード決済(下4桁) / \"-\"",
       ADM + "\n- 3 hợp đồng: bill transfer, bill card (thẻ đuôi 1234), slot chưa có bot_contracts",
       "1. Quan sát cột「決済方法」của 3 dòng\n"
       "2. Đối chiếu univa_last_four_card",
       "payment_method = 2 / 1 (univa_last_four_card=1234) / không có bot_contracts",
       "- transfer →「銀行振込」\n- card →「カード決済（下4桁 1234）」\n- không có hợp đồng →「-」",
       note="Nguồn: r59. Field Matrix #8, #21."),

    tc("Cột & trạng thái hợp đồng", "DATA-001", "Normal",
       "Cột LOA接続日 lấy theo ngày add bot; không có bot thì lấy ngày thanh toán",
       ADM + "\n- 1 hợp đồng đã kết nối bot ngày 2026/03/01\n"
       "- 1 slot đã mua ngày 2026/03/05 nhưng chưa kết nối bot",
       "1. Quan sát cột「LOA接続日」của 2 dòng\n"
       "2. Đối chiếu bot_contracts.date_add_loa",
       "date_add_loa = 2026-03-01 / slot chưa kết nối",
       "- Dòng đã kết nối: hiện 2026/03/01 (ngày add bot)\n"
       "- Dòng chưa kết nối bot: hiện ngày thanh toán (2026/03/05)",
       note="Nguồn: r29 (List main case) + r1064-r1069. Đối chiếu Field Matrix #10 (`date_add_loa`) — "
            "spec KHÔNG mô tả nhánh fallback 'không có bot thì lấy ngày thanh toán', xem MT-03."),

    tc("Cột & trạng thái hợp đồng", "FUNC-001", "Normal",
       "Nút cột 8 theo trạng thái: 契約詳細 / 詳細を確認 / 振込キャンセル / アカウントの操作",
       MIX,
       "1. Quan sát cột「契約の変更・解約」của từng dòng theo trạng thái\n"
       "2. Ghi lại nhãn + màu nút",
       "5 trạng thái như tiền đề",
       "- 正常 → nút「契約詳細」màu xanh da trời\n"
       "- 延滞中 → nút「詳細を確認」màu đỏ\n"
       "- 口座発行中 → nút「振込キャンセル」màu đỏ\n"
       "- 解約済み / 強制解約 → nút「アカウントの操作」màu xám",
       note="Nguồn: r60, r62, r64, r72, r74. Đối chiếu feature-spec.md §2 bảng 'Nút Action theo trạng thái'."),

    tc("Cột & trạng thái hợp đồng", "FUNC-001", "Normal",
       "Click 契約詳細 → mở đúng màn chi tiết hợp đồng tương ứng plan",
       ADM + "\n- Có hợp đồng free, standard, pro, enterprise ở trạng thái 正常",
       "1. Click「契約詳細」ở từng dòng của 4 plan\n2. Quan sát URL và nội dung màn chi tiết",
       "4 hợp đồng free / standard / pro / enterprise",
       "- Mỗi lần đều mở /basic/detail-contract/{id} đúng id của dòng vừa click\n"
       "- Nội dung màn chi tiết đúng theo plan (free/standard/pro/enterprise)",
       note="Nguồn: r43, r61."),

    tc("Cột & trạng thái hợp đồng", "FUNC-001", "Normal",
       "Click 詳細を確認 ở dòng 延滞中 → mở modal chi tiết lỗi thanh toán",
       ADM + "\n- Có 1 hợp đồng 延滞中 (bill card lỗi, chưa quá 7 ngày)",
       "1. Click nút「詳細を確認」màu đỏ",
       "status=1, status_payment=2, status_payment_fail < 5",
       "Mở modal chi tiết lỗi thanh toán (決済エラー) của đúng hợp đồng đó",
       note="Nguồn: r63, r78."),

    tc("Cột & trạng thái hợp đồng", "FUNC-001", "Normal",
       "Click アカウントの操作 ở hợp đồng đã hủy / cưỡng chế hủy → mở màn account tương ứng",
       ADM + "\n- 1 hợp đồng 解約済み và 1 hợp đồng 強制解約",
       "1. Click「アカウントの操作」ở dòng 解約済み\n"
       "2. Quay lại, click「アカウントの操作」ở dòng 強制解約",
       "cancel_by = 1 và cancel_by = 0",
       "- Dòng 解約済み → mở màn account đã hủy\n- Dòng 強制解約 → mở màn account cưỡng chế hủy",
       note="Nguồn: r73, r75."),

    # ═════════════ 3. Sắp xếp, tìm kiếm & phân trang ═════════════
    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-003", "Normal",
       "Phân trang: chọn 10 và 100 bản ghi/trang",
       ADM + "\n- Tài khoản có ≥ 120 hợp đồng",
       "1. Chọn phân trang = 10 → đếm số dòng\n2. Chọn phân trang = 100 → đếm số dòng",
       "≥ 120 hợp đồng",
       "- Chọn 10: hiển thị đúng 10 dòng/trang\n- Chọn 100: hiển thị đúng 100 dòng/trang\n"
       "- Số trang tính lại đúng theo tổng bản ghi",
       note="Nguồn: r18, r19."),

    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-004", "Abnormal",
       "Search: bỏ trống hoặc chỉ nhập dấu cách → đóng textbox, không lọc",
       ADM,
       "1. Click mở textbox Search, không nhập gì → bấm Search\n"
       "2. Mở lại, nhập 3 dấu cách → bấm Search",
       "Chuỗi rỗng và chuỗi \"   \" (3 space)",
       "- Cả 2 trường hợp: textbox đóng lại, danh sách giữ nguyên như trước khi search\n"
       "- Không gọi request lọc rỗng, không hiện empty state",
       note="Nguồn: r20, r21 (2 dòng cùng expected → gộp, nêu đủ 2 input)."),

    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-004", "Normal",
       "Search theo keyword có kết quả → chỉ hiện dòng khớp",
       ADM + "\n- Có bot「テストBOT」và bot「サンプルBOT」",
       "1. Mở textbox Search, nhập「テスト」\n2. Bấm Search\n3. Đối chiếu danh sách",
       "keyword =「テスト」",
       "- Chỉ hiển thị hợp đồng có tên account chứa「テスト」\n- KHÔNG hiển thị dòng「サンプルBOT」",
       note="Nguồn: r22."),

    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-002", "Abnormal",
       "Search keyword không tồn tại → empty state アカウントが接続されていません",
       ADM,
       "1. Nhập keyword「zzzzzz」vào Search\n2. Bấm Search",
       "keyword =「zzzzzz」",
       "Hiển thị text「アカウントが接続されていません」, bảng không còn dòng nào",
       note="Nguồn: r23."),

    tc("Sắp xếp, tìm kiếm & phân trang", "FUNC-002", "Normal",
       "Modal sắp xếp hợp đồng: chỉ chứa hợp đồng có status được phép kéo thả",
       ADM + "\n- Có đủ hợp đồng: 正常, 延滞中, 入金待ち, 口座発行中, 解約済み, 強制解約",
       "1. Click nút「Sắp xếp」→ mở modal\n2. Liệt kê các hợp đồng có trong modal",
       "6 hợp đồng theo 6 trạng thái",
       "- Modal CHỈ chứa hợp đồng có status khác 延滞中 / 入金待ち / 口座発行中 / 解約済み(hủy thường) / 強制解約\n"
       "- Các trạng thái bị ghim vị trí cố định không xuất hiện trong modal",
       note="Nguồn: r28 (List main case), r1053. ⚠ Corpus dùng cách diễn đạt phủ định khó hiểu — "
            "cần Leader chốt danh sách status được sắp xếp, xem MT-04."),

    tc("Sắp xếp, tìm kiếm & phân trang", "FUNC-002", "Normal",
       "Kéo thả sắp xếp rồi Save → thứ tự lưu lại, không xáo trộn dòng bị ghim",
       ADM + "\n- Có 5 hợp đồng 正常 và 1 hợp đồng 延滞中",
       "1. Mở modal sắp xếp\n2. Kéo hợp đồng thứ 5 lên vị trí 1\n3. Bấm Save\n"
       "4. Reload /basic/point-settings\n5. Kiểm tra bot_contracts.position",
       "5 hợp đồng 正常 + 1 hợp đồng 延滞中",
       "- Sau save: hợp đồng vừa kéo nằm ở đầu nhóm 正常\n"
       "- Hợp đồng 延滞中 VẪN ghim trên cùng danh sách, không bị đẩy xuống\n"
       "- DB: bot_contracts.position của các dòng được cập nhật đúng thứ tự mới",
       note="Nguồn: r28 (List main case), r1054-r1059. EP-09 save-contract-position (feature-spec.md §6)."),

    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-005", "Normal",
       "Thứ tự ghim mặc định: 延滞中 → 入金待ち/口座発行中 trên đầu, 強制解約/hủy job dưới cùng",
       MIX + "\n- Thêm 1 hợp đồng 口座発行中",
       "1. Mở /basic/point-settings với đủ các trạng thái\n2. Ghi lại thứ tự dòng từ trên xuống",
       "6 hợp đồng đủ 6 trạng thái",
       "- Nhóm ghim đầu: 延滞中 (đầu tiên), rồi 入金待ち và 口座発行中\n"
       "- Nhóm bình thường (正常) ở giữa, sắp theo position DESC\n"
       "- Nhóm ghim cuối: 強制解約 và hợp đồng bị job hủy",
       note="Nguồn: r30 (List main case), r1074. Đối chiếu BR-01 + thứ tự query "
            "ORDER BY position DESC, date_cancel_contract DESC, id DESC (feature-spec.md §5)."),

    tc("Sắp xếp, tìm kiếm & phân trang", "LIST-005", "Normal",
       "Sort theo cột 次回決済(更新)日 → đảo chiều ASC/DESC đúng",
       ADM + "\n- Có ≥ 5 hợp đồng với expired_date_contract khác nhau",
       "1. Click mũi tên sort ở cột「次回決済(更新)日」lần 1\n2. Click lần 2\n"
       "3. Đối chiếu thứ tự với giá trị expired_date_contract",
       "5 hợp đồng có ngày hết hạn: 01/03, 15/03, 02/04, 20/05, 01/07",
       "- Lần 1: sắp xếp theo 1 chiều (ASC hoặc DESC) đúng thứ tự ngày\n"
       "- Lần 2: đảo ngược chiều\n- Dòng ghim theo trạng thái vẫn giữ nguyên vị trí ghim",
       note="Nguồn: r1060-r1063. ⚠ Corpus không ghi rõ chiều mặc định — "
            "TC yêu cầu ghi nhận chiều thực tế; xem MT-05."),

    # ═════════════ 4. Banner cảnh báo & modal ở màn list ═════════════
    tc("Banner cảnh báo & modal ở màn list", "UI-004", "Normal",
       "Có hợp đồng 延滞中 → banner 決済エラー hiện ở đầu màn hình",
       ADM + "\n- Có 1 hợp đồng 延滞中",
       "1. Mở /basic/point-settings\n2. Quan sát vùng trên cùng của trang",
       "1 hợp đồng bill lỗi, expired_date_contract < now",
       "- Hiện banner「決済エラー」ở đầu màn hình\n- Banner có nút「詳細を確認」",
       note="Nguồn: r76. Đối chiếu feature-spec.md §2 (Banner lỗi thanh toán)."),

    tc("Banner cảnh báo & modal ở màn list", "UI-004", "Boundary",
       "Nhiều hợp đồng 延滞中 → hiện đủ banner, có thanh cuộn khi quá nhiều",
       ADM + "\n- Có 5 hợp đồng cùng ở trạng thái 延滞中",
       "1. Mở /basic/point-settings\n2. Đếm số banner 決済エラー\n3. Thử cuộn trong vùng banner",
       "5 hợp đồng 延滞中",
       "- Hiện đủ 5 banner 決済エラー ở đầu màn hình\n"
       "- Khi vượt chiều cao vùng hiển thị thì có scroll trong vùng banner, không đẩy bảng xuống quá xa",
       note="Nguồn: r77."),

    tc("Banner cảnh báo & modal ở màn list", "UI-004", "Normal",
       "Tổng bạn bè vượt 50.000 → banner アップグレードが必要です với hạn nâng cấp",
       "- Đăng nhập owner của bot free có tổng bạn bè 50.001 người\n- Mở /basic/point-settings",
       "1. Quan sát banner phía trên bảng danh sách\n2. Đọc nội dung banner",
       "Tổng friend = 50.001",
       "Hiện banner nội dung「総友だち数が50,000人を超えました。YYYY/MM/DDまでにプロプランへの"
       "アップグレードが必要です。」với YYYY/MM/DD thay bằng hạn thực tế",
       note="Nguồn: feature-spec.md §2 (Banner nâng cấp plan) + Bill max friend r49, r79. "
            "⚠ Bug KH #34409 (11/02/2026): từng hiện nhầm mốc 100.000 khi chưa đạt — bắt buộc kiểm tra mốc hiển thị."),

    tc("Banner cảnh báo & modal ở màn list", "FUNC-001", "Normal",
       "Click 振込情報 ở dòng chờ chuyển khoản → mở modal 銀行振込口座のご案内",
       ADM + "\n- Có hợp đồng 入金待ち đã phát hành số tài khoản",
       "1. Click nút「振込情報」\n2. Quan sát modal\n3. Click「閉じる」rồi thử lại với nút X",
       "univa_account_number đã có giá trị",
       "- Mở modal「銀行振込口座のご案内」hiện tên NH, chi nhánh, số tài khoản, tên người nhận, hạn chuyển khoản\n"
       "- Click「閉じる」hoặc X đều đóng modal, không mất dữ liệu màn nền",
       note="Nguồn: r45, r46, r1078."),

    tc("Banner cảnh báo & modal ở màn list", "FUNC-001", "Normal",
       "Chuyển khoản thành công → dòng hợp đồng hiện nút 請求書, click tải được hóa đơn",
       ADM + "\n- Hợp đồng bill transfer đã chuyển khoản thành công (status_payment = 1)",
       "1. Quan sát dòng hợp đồng\n2. Click nút「請求書」",
       "payment_histories mới nhất của contract: status_transfer=1, type_bill=3",
       "- Dòng hiện nút「請求書」\n"
       "- Click → tải xuống đúng hóa đơn gần nhất của hợp đồng đó (khớp amount và status ở payment_histories)",
       note="Nguồn: r41, r42, r38 (List main case)."),

    tc("Banner cảnh báo & modal ở màn list", "FUNC-003", "Normal",
       "Modal 請求書の宛名: nhập tên + chọn danh xưng → hóa đơn tải về đúng tên + danh xưng",
       ADM + "\n- Hợp đồng bill transfer đã chuyển khoản",
       "1. Click「請求書」→ mở modal「請求書の宛名」\n"
       "2. Nhập「株式会社テスト」vào ô 宛名\n3. Chọn danh xưng「御中」→ tải\n"
       "4. Lặp lại với「様」và「設定なし」",
       "宛名 =「株式会社テスト」; danh xưng lần lượt 御中 / 様 / 設定なし",
       "- File PDF tải về hiện「株式会社テスト 御中」\n- Lần 2 hiện「株式会社テスト 様」\n"
       "- Lần 3 chỉ hiện「株式会社テスト」, không có danh xưng",
       note="Nguồn: r47-r52. RULE-06: phải mở file PDF tải về để đối chiếu, không dừng ở thông báo tải xong."),

    tc("Banner cảnh báo & modal ở màn list", "FUNC-003", "Abnormal",
       "Modal 請求書の宛名: không nhập tên → hóa đơn không có tên, vẫn tải được",
       ADM + "\n- Hợp đồng bill transfer đã chuyển khoản",
       "1. Click「請求書」\n2. Để trống ô 宛名\n3. Bấm tải",
       "宛名 rỗng",
       "- Tải xuống được file PDF\n- Trên hóa đơn không hiển thị tên, chỉ hiển thị danh xưng đã chọn (mặc định 御中)",
       note="Nguồn: r49, r242, r243."),

    tc("Banner cảnh báo & modal ở màn list", "UI-005", "Normal",
       "Đóng modal 請求書の宛名 bằng nút X → không tải hóa đơn, không lưu dữ liệu nhập",
       ADM + "\n- Hợp đồng bill transfer đã chuyển khoản",
       "1. Click「請求書」\n2. Nhập tên「テスト」\n3. Click nút X\n4. Mở lại modal",
       "宛名 =「テスト」",
       "- Modal đóng, KHÔNG tải file nào\n- Mở lại modal: ô 宛名 trống (không lưu giá trị vừa nhập)",
       note="Nguồn: r53, r246-r249."),
]
