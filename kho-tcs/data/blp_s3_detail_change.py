# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 12-18: màn chi tiết hợp đồng và các thao tác thay đổi hợp đồng.

Nguồn chính: TCsLine_Bill tiền_Improve2025 → tab「Quản lý hợp đồng」
  · r144-r184 (detail plan free) · r185-r305 (detail enterprise + Feature #37085)
  · r306-r403 (detail standard/pro) · r406-r481 (thẻ chính/phụ)
  · r482-r585 (đổi kỳ thanh toán / phương thức) · r793-r819 (extend)
  · r1545-r1579 (SpecImprove Test #36076 — hiển thị giá khi đổi kỳ)
"""
from _common import tc

DTL = ("- Đăng nhập owner của hợp đồng\n"
       "- Mở /basic/point-settings → click「契約詳細」của hợp đồng cần kiểm tra")
STD = "- Hợp đồng standard đang 正常, bill card, còn hạn\n" + DTL

S3 = [
    # ═════════════ 12. Detail hợp đồng — plan free ═════════════
    tc("Detail hợp đồng — plan free", "UI-001", "Normal",
       "Breadcrumb + title màn chi tiết hợp đồng",
       "- Hợp đồng plan free\n" + DTL,
       "1. Quan sát breadcrumb đầu trang\n2. Quan sát tiêu đề\n3. Click breadcrumb「契約情報・領収書」",
       "Hợp đồng free",
       "- Breadcrumb hiện「契約情報・領収書 > 契約詳細」\n- Tiêu đề「契約詳細」\n"
       "- Click breadcrumb → quay lại /basic/point-settings",
       note="Nguồn: r146, r147, r308."),

    tc("Detail hợp đồng — plan free", "DATA-001", "Normal",
       "Thông tin cơ bản của hợp đồng free: tên acc, status, ngày kết nối, plan",
       "- Hợp đồng plan free đã kết nối bot, ngày kết nối 2024/10/31\n" + DTL,
       "1. Đọc tên account + LINE ID\n2. Đọc ステータス\n3. Đọc LINE公式アカウント接続日\n4. Đọc ご契約プラン",
       "date_add_loa = 2024-10-31, contract_type = free",
       "- Hiện tên account + LINE ID\n- ステータス =「正常」\n"
       "- LINE公式アカウント接続日 =「2024年10月31日」\n- ご契約プラン =「フリー」",
       note="Nguồn: r149-r152. Field Matrix #13-#15."),

    tc("Detail hợp đồng — plan free", "UI-005", "Normal",
       "Plan free: khu 解約する hiện tooltip giải thích + nút disable",
       "- Hợp đồng plan free\n" + DTL,
       "1. Rê chuột lên「よくある質問を見る」ở khu 解約する\n2. Đọc nội dung\n3. Quan sát nút bên dưới",
       "contract_type = free",
       "- Tooltip hiện:「フリープランには解約操作はありません エルメの利用を終了したい場合は "
       "接続解除もしくはエルメアカウント削除を行なってください」\n"
       "- Nút「この操作は行えません」ở trạng thái disable, không click được",
       note="Nguồn: r157-r159."),

    tc("Detail hợp đồng — plan free", "UI-005", "Normal",
       "Plan free: khu 接続解除 và エルメアカウント削除 có tooltip + nút hoạt động",
       "- Hợp đồng plan free\n" + DTL,
       "1. Hover「よくある質問を見る」ở khu 接続解除 → đọc tooltip\n"
       "2. Hover ở khu エルメアカウント削除 → đọc tooltip\n"
       "3. Hover 2 nút「接続解除へ進む」và「エルメアカウント削除へ進む」",
       "contract_type = free",
       "- Tooltip 接続解除:「エルメとLINE公式アカウントの接続を解除します」\n"
       "- Tooltip アカウント削除:「エルメから全ての登録データを削除します 削除後はエルメに"
       "ログインできなくなります」\n- Cả 2 nút hover đổi con trỏ thành bàn tay (clickable)",
       note="Nguồn: r160-r162, r165-r167."),

    tc("Detail hợp đồng — plan free", "FUNC-001", "Normal",
       "Plan free: click 接続解除へ進む → mở modal xóa liên kết, bấm back thì quay lại detail",
       "- Hợp đồng plan free đã kết nối bot\n" + DTL,
       "1. Click「接続解除へ進む」\n2. Quan sát modal\n3. Bấm back/đóng modal",
       "—",
       "- Mở modal xóa liên kết bot\n- Bấm back: quay lại màn chi tiết hợp đồng, KHÔNG xóa liên kết",
       note="Nguồn: r163, r164."),

    tc("Detail hợp đồng — plan free", "FUNC-003", "Normal",
       "Modal 主管理者を変更する: 2 hyperlink mở đúng đích",
       "- Hợp đồng bất kỳ\n" + DTL,
       "1. Click「主管理者を変更する」→ mở modal\n2. Click hyperlink「マイページ」\n"
       "3. Quay lại, click hyperlink「主管理者変更申請フォーム」\n4. Đóng modal bằng nút close",
       "—",
       "- Link マイページ → mở tab mới /admin/setting\n"
       "- Link 主管理者変更申請フォーム → mở tab mới "
       "https://tayori.com/form/161edb9a4342dcd97474c0da90dba8bddcf5c11b\n"
       "- Nút close đóng modal",
       note="Nguồn: r182-r184, r216-r219, r239-r241. ⚠ feature-spec.md §9 [M1] ghi CHƯA tìm được endpoint "
            "đổi 主管理者 — TC này lấp Gap: hành vi thực tế là chuyển hướng ra form ngoài, không có API nội bộ."),

    tc("Detail hợp đồng — plan free", "UI-005", "Normal",
       "Bộ lọc lịch sử: placeholder 全件表示, chọn 1 status thì lọc đúng",
       "- Hợp đồng có ≥ 5 bản ghi lịch sử thuộc nhiều loại\n" + DTL,
       "1. Quan sát placeholder bộ lọc\n2. Click mở dropdown\n3. Chọn 1 loại status bất kỳ",
       "≥ 5 bản ghi lịch sử",
       "- Placeholder hiện「全件表示」\n- Mở dropdown hiện đủ các nhóm status\n"
       "- Chọn 1 status: danh sách chỉ còn bản ghi thuộc status đó",
       note="Nguồn: r170-r172, r225."),

    tc("Detail hợp đồng — plan free", "DATA-003", "Normal",
       "Calendar lịch sử: format + giá trị mặc định",
       "- Hợp đồng bất kỳ, ngày hiện tại 2026/01/14\n" + DTL,
       "1. Quan sát 開始日 và 終了日 mặc định\n2. Ghi lại format hiển thị",
       "Ngày hiện tại = 2026/01/14",
       "- Mặc định: từ ngày mồng 1 của tháng hiện tại đến ngày hiện tại\n"
       "- Format hiển thị yyyy.mm.dd (hoặc yyyy/mm/dd（曜）theo design)",
       note="Nguồn: r173, r174, r226-r233. ⚠ Corpus có 2 format khác nhau (r174 ghi "
            "「2025/12/16（火） から 2026/01/14（水）」, r226 ghi「yyyy.mm.dd」) — xem MT-16."),

    tc("Detail hợp đồng — plan free", "DATA-003", "Abnormal",
       "Calendar lịch sử: 終了日 < 開始日 → không chọn được; bằng nhau thì lọc đúng 1 ngày",
       "- Hợp đồng có lịch sử trong ngày 2026/01/15\n" + DTL,
       "1. Chọn 開始日 = 2026/02/01, thử chọn 終了日 = 2026/01/15\n"
       "2. Chọn 開始日 = 終了日 = 2026/01/15\n3. Quan sát danh sách",
       "From=2026/02/01 To=2026/01/15; From=To=2026/01/15",
       "- Không thể chọn ngày kết thúc nhỏ hơn ngày bắt đầu\n"
       "- From = To: hiển thị đúng dữ liệu trong ngày đó",
       note="Nguồn: r179, r180, r234, r235."),

    tc("Detail hợp đồng — plan free", "DATA-003", "Abnormal",
       "Nhập tay ngày filter lịch sử (không dùng datepicker) + kết hợp filter status",
       "- Hợp đồng có lịch sử trải nhiều tháng\n" + DTL,
       "1. Gõ tay ngày hợp lệ vào ô 開始日/終了日\n2. Gõ ngày sai định dạng (vd 2026/13/45)\n"
       "3. Xóa toàn bộ ô ngày\n4. Kết hợp gõ tay ngày + chọn filter status",
       "Ngày hợp lệ, ngày sai định dạng, ô rỗng",
       "- Ngày hợp lệ: lọc đúng khoảng đã gõ\n- Ngày sai định dạng: bị chặn/không áp dụng, không lỗi trang\n"
       "- Xóa hết ô ngày: quay về hiển thị mặc định\n- Kết hợp với status: lọc theo cả 2 điều kiện",
       note="Nguồn: r1497-r1514 (Support #35316, 17/04/2026)."),

    # ═════════════ 13. Detail hợp đồng — standard/pro ═════════════
    tc("Detail hợp đồng — standard/pro", "DATA-001", "Normal",
       "Đủ 9 trường thông tin hợp đồng standard/pro",
       STD,
       "1. Đọc lần lượt: ステータス, LINE公式アカウント接続日, ご契約プラン, お支払い開始日, "
       "ご利用料金, お支払い期間, 次回決済日, 決済方法, 主管理者\n"
       "2. Đối chiếu với bot_contracts",
       "Hợp đồng standard tháng, bill card, ngày bắt đầu 2024/10/31",
       "- ステータス 正常 · プラン スタンダード · お支払い開始日 2024年10月31日 (= datetime_first_payment)\n"
       "- ご利用料金 = số tiền + 円 (税込) khớp amount_payment\n- お支払い期間 = 毎月払い\n"
       "- 次回決済日 format yyyy年mm月dd日 khớp expired_date_contract\n"
       "- 決済方法 = クレジットカード + 4 số cuối\n- 主管理者 = tên owner",
       note="Nguồn: r191-r207, r587-r601. Field Matrix #13-#24."),

    tc("Detail hợp đồng — standard/pro", "UI-002", "Normal",
       "Ảnh đại diện: bot không có avatar → ảnh mặc định; có avatar png/jpg → hiển thị trong khung tròn",
       "- 3 bot: 1 không avatar, 1 avatar .png, 1 avatar .jpg\n" + DTL,
       "1. Mở detail của bot không có avatar\n2. Mở detail của bot avatar png\n"
       "3. Mở detail của bot avatar jpg\n4. Quan sát khung ảnh tròn",
       "3 bot: no-avatar, avatar.png, avatar.jpg",
       "- Bot không avatar: hiện ảnh mặc định\n- Bot có avatar png và jpg: hiện đúng ảnh LINE\n"
       "- Ảnh nằm gọn trong khung tròn, không méo/vỡ",
       note="Nguồn: r310, r311, r425-r428 (3 nhánh cùng nhóm kết quả → gộp, nêu đủ 3 loại ảnh)."),

    tc("Detail hợp đồng — standard/pro", "FUNC-001", "Normal",
       "Slot mới mua chưa kết nối bot, thanh toán bằng thẻ → vẫn mở được màn chi tiết",
       "- 4 slot mới mua chưa kết nối bot: standard năm/card, pro năm/card, standard tháng/card, pro tháng/card",
       "1. Với từng slot, click 契約詳細 ở màn list\n2. Quan sát thông tin thẻ hiển thị",
       "4 slot mới mua bằng thẻ",
       "Cả 4 slot đều mở được màn chi tiết và hiển thị thông tin thẻ đã đăng ký",
       note="Nguồn: r308-r314."),

    tc("Detail hợp đồng — standard/pro", "FUNC-007", "Abnormal",
       "Slot mua bằng chuyển khoản CHƯA thanh toán → không mở được màn chi tiết từ màn list",
       "- 1 slot mua mới bằng 銀行振込, chưa chuyển khoản",
       "1. Quan sát cột 8 của dòng đó ở màn list\n2. Thử click vào vùng nút",
       "status_payment chưa = 1",
       "Không hiện nút mở chi tiết hợp đồng (chỉ có 振込キャンセル); không vào được màn detail qua UI",
       note="Nguồn: r315, r316, r345, r346."),

    tc("Detail hợp đồng — standard/pro", "SEC-002", "Abnormal",
       "Truy cập detail-contract bằng URL khi hợp đồng chờ chuyển khoản → vào được nhưng mọi nút bị disable",
       "- Hợp đồng bill năm đang chờ chuyển khoản (chưa thanh toán)\n"
       "- Biết id hợp đồng",
       "1. Dán trực tiếp URL /basic/detail-contract/{id}\n"
       "2. Thử click「次回決済から月払いに変更する」\n3. Thử click「クレジットカードに変更する」\n"
       "4. Thử submit form thay đổi bằng cách bỏ thuộc tính disabled trên DevTools",
       "Hợp đồng chờ chuyển khoản",
       "- Vào được màn chi tiết nhưng 2 nút thay đổi hợp đồng bị disable\n"
       "- Bỏ disabled bằng DevTools rồi submit: server VẪN chặn, không thay đổi hợp đồng",
       note="Nguồn: r317, r318 (corpus ghi「chặn cả bên trong màn không cho phép nhập」). "
            "Bước 4 (bypass DevTools) do AI bổ sung theo SEC-002 — CẦN LEADER XÁC NHẬN mức chặn phía server."),

    tc("Detail hợp đồng — standard/pro", "STATE-003", "Abnormal",
       "Mua mới transfer chưa thanh toán, vào detail bằng URL rồi nhập thẻ lỗi + back → xóa hẳn hợp đồng",
       "- Hợp đồng mua mới bill transfer, chưa thanh toán (cả 2 trạng thái 口座発行中 và 入金待ち)",
       "1. Vào /basic/detail-contract/{id} bằng URL\n2. Nhập thẻ lỗi 4111 1111 1111 1111\n"
       "3. Bấm back\n4. Kiểm tra màn list và bảng bot_contracts",
       "2 trạng thái: chưa phát hành STK và đã phát hành STK",
       "Bản ghi bot_contracts của id đó bị xóa; dòng biến mất khỏi màn list",
       note="Nguồn: r321, r322 (2 dòng cùng expected → gộp). ⚠ Hành vi 'xóa luôn hợp đồng khi back' "
            "không có trong spec — rủi ro mất dữ liệu ngoài ý muốn, xem MT-17."),

    tc("Detail hợp đồng — standard/pro", "FUNC-001", "Normal",
       "Hợp đồng free vẫn vào được màn chi tiết bằng URL",
       "- Hợp đồng plan free",
       "1. Lấy id hợp đồng free, dán URL /basic/detail-contract/{id}",
       "contract_type = free",
       "Vào được màn chi tiết plan free, hiển thị đúng bố cục dành cho free",
       note="Nguồn: r323."),

    tc("Detail hợp đồng — standard/pro", "DATA-001", "Normal",
       "Detail hợp đồng bill transfer: hiện khối 振込先情報 theo trạng thái phát hành tài khoản",
       "- 2 hợp đồng bill transfer: 1 đang 口座発行中, 1 đã có số tài khoản\n" + DTL,
       "1. Mở detail hợp đồng đang chờ phát hành STK → đọc khối 振込先情報\n"
       "2. Mở detail hợp đồng đã phát hành STK → đọc khối 振込先情報",
       "2 hợp đồng transfer, release_date_transfer đã set",
       "- Chờ phát hành: hiện「YYYY/MM/DDに振込口座が発行されます」khớp release_date_transfer\n"
       "- Đã phát hành: hiện tên NH, chi nhánh + 支店, 普通口座 + số TK, tên (ｶ)ﾕﾆｳﾞｧﾍﾟｲｷｬｽﾄ, "
       "「※振込期限　YYYY年MM月DD日 23:59 まで」",
       note="Nguồn: r603, r604. Cột `release_date_transfer` KHÔNG có trong db-mapping của spec — xem MT-13."),

    tc("Detail hợp đồng — standard/pro", "STATE-001", "Normal",
       "Hợp đồng 延滞中 (thẻ): status kèm hạn cưỡng chế hủy = expired_date + 7 ngày",
       "- Hợp đồng bill card, expired_date_contract = 2026/03/01, đã quá hạn 2 ngày, bill lỗi\n" + DTL,
       "1. Đọc ステータス ở màn chi tiết\n2. Đọc dòng cảnh báo bên dưới\n"
       "3. So sánh ngày hiển thị với expired_date + 7",
       "expired_date_contract = 2026-03-01, status_payment=2, status_payment_fail<5",
       "- ステータス =「延滞中」\n"
       "- Dòng cảnh báo「〇月〇日までに決済が行われない場合、強制解約となります」với ngày = 2026/03/08\n"
       "- Ngày hiển thị ở màn list và màn chi tiết GIỐNG NHAU",
       note="Nguồn: r648, r650, r656 + r1695-r1720 (Bug KH #37109, 05/06/2026 — ngày 強制解約 hiển thị "
            "khác nhau giữa các trang). Evidence bắt buộc: ảnh cả 2 màn."),

    tc("Detail hợp đồng — standard/pro", "FUNC-001", "Normal",
       "Banner 延滞中 (thẻ): link クレジットカードの変更 và プリペイド型カード",
       "- Hợp đồng bill card đang 延滞中\n- Mở /basic/point-settings",
       "1. Click text「クレジットカードの変更」trong banner\n2. Quay lại, click text「プリペイド型カード」\n"
       "3. Quay lại, click nút「クレジットカードの変更」",
       "Hợp đồng 延滞中 bill card",
       "- 2 lối「クレジットカードの変更」(text và nút) đều mở màn đổi thẻ\n"
       "- Text「プリペイド型カード」mở tab mới https://vpc.lifecard.co.jp/",
       note="Nguồn: r651-r653."),

    tc("Detail hợp đồng — standard/pro", "FUNC-006", "Normal",
       "延滞中 (thẻ): nhập thẻ mới hợp lệ → bill ngay + cập nhật hợp đồng + tạo lịch sử",
       "- Hợp đồng standard bill card đang 延滞中",
       "1. Từ banner mở màn đổi thẻ\n2. Nhập thẻ mới hợp lệ, bấm thanh toán\n"
       "3. Quan sát màn list\n4. Kiểm tra bot_contracts và lịch sử hóa đơn",
       "Thẻ mới hợp lệ",
       "- Bill được thực hiện ngay khi đổi thẻ thành công\n"
       "- DB: status=1, status_payment=1, expired_date_contract được cộng thêm 1 kỳ, univa_last_four_card = thẻ mới\n"
       "- Lịch sử hóa đơn có bản ghi mới; màn list quay về status 正常",
       env="PRODUCTION",
       note="Nguồn: r654 + r23, r26 (tab hóa đơn). RULE-07 + RULE-08."),

    tc("Detail hợp đồng — standard/pro", "FUNC-006", "Abnormal",
       "延滞中 (thẻ): nhập thẻ mới bill lỗi → không cập nhật hợp đồng, không đổi thẻ",
       "- Hợp đồng standard bill card đang 延滞中",
       "1. Mở màn đổi thẻ, nhập thẻ lỗi 4111 1111 1111 1111\n2. Quan sát màn hình\n"
       "3. Kiểm tra bot_contracts và lịch sử hóa đơn",
       "Thẻ lỗi 4111 1111 1111 1111",
       "- Hiện màn đổi thẻ thất bại\n- DB: hợp đồng giữ nguyên 延滞中, univa_last_four_card KHÔNG đổi\n"
       "- KHÔNG tạo bản ghi lịch sử bill hiển thị cho user",
       note="Nguồn: r655 + r24, r27 (tab hóa đơn)."),

    tc("Detail hợp đồng — standard/pro", "STATE-001", "Normal",
       "Hợp đồng 延滞中 (chuyển khoản): hiện thông tin STK + không có nút bill lại",
       "- Hợp đồng standard năm bill transfer, đã quá hạn, chưa chuyển khoản\n" + DTL,
       "1. Đọc ステータス và banner cảnh báo\n2. Quan sát khối 振込先情報\n"
       "3. Liệt kê các nút thao tác còn enable",
       "payment_method=2, status_payment IN(2,5), status_payment_fail<5",
       "- ステータス「延滞中」kèm hạn cưỡng chế hủy\n- Hiển thị số tài khoản chuyển khoản\n"
       "- KHÔNG có nút「bill lại」bằng thẻ; các thao tác đổi kỳ/đổi phương thức/gia hạn vẫn enable",
       note="Nguồn: r687-r718 + tab「Compare logic cũ」r15."),

    # ═════════════ 14. Detail hợp đồng — enterprise ═════════════
    tc("Detail hợp đồng — enterprise", "DATA-001", "Normal",
       "Detail enterprise: không hiện tên/ảnh bot, hiện おまとめ割引 + số slot",
       "- 2 hợp đồng enterprise: 10 slot và 20 slot\n" + DTL,
       "1. Mở detail hợp đồng EP 10 slot → đọc mục tên account và ご契約プラン\n"
       "2. Mở detail hợp đồng EP 20 slot → đọc tương tự",
       "EP 10 slot và EP 20 slot",
       "- Không hiển thị tên và ảnh BOT\n"
       "- ご契約プラン hiện「おまとめ割引」+「10枠」/「20枠」+ tên plan gốc (スタンダード/プロ)\n"
       "- Ảnh đại diện là ảnh mặc định",
       note="Nguồn: r189, r190, r193, r250, r277."),

    tc("Detail hợp đồng — enterprise", "DATA-001", "Normal",
       "Detail enterprise: LINE公式アカウント接続日 chỉ hiện khi đã có slot kết nối",
       "- 1 hợp đồng EP chưa có slot nào kết nối bot, 1 hợp đồng EP đã có slot kết nối\n" + DTL,
       "1. Mở detail EP chưa kết nối → đọc LINE公式アカウント接続日\n2. Mở detail EP đã kết nối → đọc tương tự",
       "2 hợp đồng EP",
       "- EP chưa kết nối: KHÔNG hiển thị ngày kết nối; tên hiện「LINE公式アカウント未接続」\n"
       "- EP đã kết nối: hiện ngày kết nối và tên bot đầu tiên đã kết nối",
       note="Nguồn: r190, r192."),

    tc("Detail hợp đồng — enterprise", "FUNC-001", "Normal",
       "Nút おまとめ割引の契約を変更する (owner) → mở màn quản lý slot enterprise",
       "- Đăng nhập OWNER của hợp đồng enterprise\n" + DTL,
       "1. Click nút「おまとめ割引の契約を変更する」\n2. Quan sát URL\n"
       "3. Quay lại màn list, click text「おまとめ割引」của dòng EP",
       "Hợp đồng EP id = 1991",
       "Cả 2 lối đều mở /admin/bots/list-bot-enterprise/1991",
       note="Nguồn: r194, r251, r261."),

    tc("Detail hợp đồng — enterprise", "FUNC-005", "Normal",
       "Owner thao tác đủ 8 chức năng trên hợp đồng enterprise + ghi lịch sử",
       "- Đăng nhập OWNER của hợp đồng enterprise\n" + DTL,
       "1. Thực hiện lần lượt: đổi kỳ bill tháng↔năm, gia hạn hợp đồng, đổi phương thức bill, "
       "đổi thẻ chính, đổi thẻ phụ, đổi owner, hủy hợp đồng, hủy kết nối bot\n"
       "2. Sau mỗi thao tác mở khối 操作履歴 và kiểm tra bản ghi mới",
       "8 thao tác như phần bước",
       "- Cả 8 thao tác đều thực hiện được, hợp đồng cập nhật đúng\n"
       "- Mỗi thao tác sinh đúng 1 bản ghi trong 操作履歴 với loại sự kiện tương ứng",
       note="Nguồn: r252-r259 (8 dòng cùng expected → gộp, liệt kê đủ 8 thao tác ở Các bước). "
            "RULE-01: quan điểm ưu tiên Cao — TC Abnormal/Boundary tương ứng nằm ở nhóm 『Phân quyền & staff』."),

    tc("Detail hợp đồng — enterprise", "REG-001", "Normal",
       "Thao tác enterprise KHÔNG làm hỏng 8 trường thông tin còn lại",
       "- Hợp đồng enterprise vừa thực hiện 1 thao tác thay đổi\n" + DTL,
       "1. Ghi lại 8 trường trước thao tác\n2. Thực hiện thay đổi (vd đổi kỳ bill)\n"
       "3. Đọc lại 8 trường: お支払い開始日, ご利用料金, お支払い期間, 次回決済日, 決済方法, "
       "メイン決済カード情報, サブ決済カード情報, 主管理者",
       "Hợp đồng EP standard 10 slot",
       "Chỉ trường liên quan tới thao tác thay đổi; 7 trường còn lại giữ nguyên giá trị, không rỗng, không sai format",
       note="Nguồn: r260, r287. Đây là TC regression — ghi 'regression' ở Ghi chú theo quy chuẩn Loại case."),

    tc("Detail hợp đồng — enterprise", "FUNC-005", "Normal",
       "Màn quản lý slot enterprise: add bot mới / add bot có sẵn / xóa bot khỏi slot / 一括解除",
       "- Đăng nhập OWNER hợp đồng EP 10 slot, còn slot trống\n"
       "- Mở /admin/bots/list-bot-enterprise/{id}",
       "1. Add bot mới vào slot trống\n2. Add bot từ danh sách bot có sẵn vào slot trống\n"
       "3. Xóa 1 bot khỏi slot\n4. Bấm「一括解除」hủy kết nối nhiều bot cùng lúc\n"
       "5. Mở 操作履歴 của hợp đồng sau mỗi thao tác",
       "EP 10 slot, ≥ 3 bot",
       "- Cả 4 thao tác thực hiện được, số slot đã dùng cập nhật đúng\n"
       "- Mỗi thao tác đều sinh bản ghi trong 操作履歴 của hợp đồng",
       note="Nguồn: r262-r264, r267 (4 dòng cùng expected → gộp)."),

    tc("Detail hợp đồng — enterprise", "FUNC-005", "Normal",
       "Bot free được áp dụng vào slot enterprise / standard / pro trống",
       "- Owner có bot free và có slot trống của enterprise, standard, pro\n- Mở màn list bot",
       "1. Click「有料プランを適用」của bot free → chọn slot enterprise → save\n"
       "2. Lặp lại với slot standard\n3. Lặp lại với slot pro\n"
       "4. Kiểm tra bot_slots và màn list hợp đồng",
       "3 loại slot trống: enterprise, standard, pro",
       "Cả 3 lần: bot free được kết nối vào slot tương ứng thành công, "
       "bot_slots.bot_id được ghi và màn list hợp đồng hiện tên bot",
       note="Nguồn: r248, r295."),

    tc("Detail hợp đồng — enterprise", "FUNC-005", "Normal",
       "Mua mới hợp đồng enterprise (Feature #37085): owner mặc định là account đang đăng nhập",
       "- Đăng nhập account A\n- Mở /admin/confirm-contract-standard/enterprise/month",
       "1. Quan sát ô lựa chọn 主管理者 trên màn kết nối LOA\n2. Hoàn tất mua hợp đồng\n"
       "3. Kiểm tra owner của hợp đồng vừa tạo",
       "Account đang đăng nhập = A",
       "- Ô chọn owner bị DISABLE, mặc định là account A\n"
       "- Hợp đồng tạo thành công với owner = A",
       note="Nguồn: r242-r244 (Feature #37085, 06/2026)."),

    tc("Detail hợp đồng — enterprise", "FUNC-005", "Normal",
       "Mua hợp đồng standard/pro thường vẫn chọn được owner khác account đang đăng nhập",
       "- Đăng nhập account A, có thêm account B trong hệ thống",
       "1. Mua hợp đồng standard, chọn owner = A → hoàn tất, kiểm tra owner\n"
       "2. Mua hợp đồng pro, chọn owner = B → hoàn tất, kiểm tra owner",
       "2 lượt mua: owner = A và owner = B",
       "Cả 2 hợp đồng tạo thành công, mỗi hợp đồng có owner đúng như đã chọn; "
       "hợp đồng và lịch sử bill hiển thị ở account được chọn",
       note="Nguồn: r245, r246, r370, r371, r381, r382 (regression của Feature #37085)."),

    tc("Detail hợp đồng — enterprise", "UI-004", "Normal",
       "Owner có slot enterprise trống → màn list bot hiện thông báo + nút 詳細を見る",
       "- Đăng nhập OWNER hợp đồng EP còn slot trống\n- Mở màn list bot",
       "1. Quan sát khu thông báo trên màn list bot\n2. Click nút「詳細を見る」",
       "EP còn ≥ 1 slot trống",
       "- Hiện thông báo có slot trống của enterprise\n"
       "- Click「詳細を見る」→ mở màn quản lý slot enterprise",
       note="Nguồn: r247."),

    # ═════════════ 15. Đổi kỳ thanh toán ═════════════
    tc("Đổi kỳ thanh toán", "DATA-001", "Normal",
       "Bot chưa từng đổi kỳ thanh toán → bill_type_old = NULL và nút hiện đúng chiều",
       "- Hợp đồng standard năm, bill card, chưa đổi kỳ lần nào\n" + DTL,
       "1. Kiểm tra bot_contracts.bill_type_old\n2. Đọc nhãn nút đổi kỳ thanh toán",
       "bill_type_old = NULL, contract_bill_type = year",
       "- DB: bill_type_old = NULL\n- Nút hiện「次回決済から月払いに変更する」",
       note="Nguồn: r483, r484, r529, r530."),

    tc("Đổi kỳ thanh toán", "FUNC-006", "Normal",
       "Đổi năm → tháng (đang bill transfer): 3 bước và phải nhập thẻ",
       "- Hợp đồng standard năm, bill transfer, còn hạn\n" + DTL,
       "1. Click「次回決済から月払いに変更する」\n2. Quan sát step 1: ご利用料金, お支払い期間, 決済方法, ngày\n"
       "3. Bấm「クレジットカードの登録に進む」→ step 2 nhập thẻ hợp lệ\n4. Quan sát step 3",
       "Hợp đồng standard năm transfer, expired_date_contract = 2026/10/30",
       "- Màn「お支払い期間の変更」hiện đủ 3 step\n"
       "- Step 1: お支払い期間 hiện「年間一括払い → 月払い」, 決済方法「クレジットカード」, "
       "dòng「次回決済日：2026年10月31日から月払いに変更されます」(= expired_date + 1 ngày)\n"
       "- Step 3: hiện「お支払い期間変更のお申し込みありがとうございます。変更が完了いたしました。」",
       note="Nguồn: r488-r498. Ngày hiển thị = expired_date_contract + 1 ngày."),

    tc("Đổi kỳ thanh toán", "DATA-001", "Normal",
       "Sau khi đổi kỳ nhưng CHƯA tới ngày hết hạn → vẫn hiển thị kỳ CŨ + dòng thông báo",
       "- Hợp đồng standard năm vừa đăng ký đổi sang tháng, chưa tới expired_date\n" + DTL,
       "1. Đọc mục お支払い期間\n2. Đọc dòng chú thích ngày\n3. Đọc nhãn nút\n"
       "4. Kiểm tra bot_contracts.contract_bill_type và bill_type_old\n5. Xem số tiền ở màn list và màn detail",
       "contract_bill_type đã đổi thành month, bill_type_old = year",
       "- お支払い期間 VẪN hiện「年間一括払い」\n"
       "- Có dòng xám「次回決済日：2026年10月31日から月払いに変更されます」\n"
       "- Nhãn nút đổi thành「お支払い期間の変更」\n"
       "- Số tiền ở cả màn list và màn detail hiển thị theo GIÁ NĂM",
       note="Nguồn: r502, r503, r505, r520, r1547-r1556 (SpecImprove Test #36076). "
            "Đây là điểm hay nhầm: DB đã đổi nhưng UI phải giữ kỳ cũ tới ngày hết hạn."),

    tc("Đổi kỳ thanh toán", "DATA-001", "Normal",
       "Tới ngày hết hạn → kỳ thanh toán và số tiền chuyển sang giá trị mới, dòng xám biến mất",
       "- Hợp đồng đã đăng ký đổi năm → tháng, đã tới/qua expired_date và job bill đã chạy\n" + DTL,
       "1. Đọc mục お支払い期間\n2. Kiểm tra dòng xám\n3. Đọc số tiền ở màn detail và màn list",
       "Đã qua expired_date, job bill đã chạy",
       "- お支払い期間 chuyển thành「月払い」\n- Dòng xám「…から月払いに変更されます」biến mất\n"
       "- Số tiền ở cả 2 màn hiển thị theo GIÁ THÁNG",
       env="PRODUCTION",
       note="Nguồn: r506, r1552, r1553, r1556. RULE-08: phụ thuộc job → PRODUCTION."),

    tc("Đổi kỳ thanh toán", "STATE-002", "Normal",
       "Hoàn tác đổi kỳ trước ngày hết hạn → về trạng thái ban đầu",
       "- Hợp đồng standard năm đã đăng ký đổi sang tháng, chưa tới expired_date\n" + DTL,
       "1. Click nút「お支払い期間の変更」→ chọn hoàn tác về năm\n2. Hoàn tất\n"
       "3. Đọc お支払い期間, dòng xám, nhãn nút, nút đổi phương thức\n"
       "4. Kiểm tra bot_contracts.contract_bill_type",
       "bill_type_old = year",
       "- DB: contract_bill_type quay lại year\n- Dòng xám thông báo đổi kỳ biến mất\n"
       "- Nhãn nút quay lại「次回決済から月払いに変更する」\n- Nút「銀行振込に変更する」hiện lại",
       note="Nguồn: r505, r330, r336, r342, r522-r524, r1559-r1561."),

    tc("Đổi kỳ thanh toán", "FUNC-006", "Abnormal",
       "Đổi kỳ (transfer → phải nhập thẻ) mà thẻ lỗi → hủy charge transfer, hợp đồng về nguyên trạng",
       "- Hợp đồng standard năm bill transfer đang 入金待ち/口座発行中",
       "1. Bấm đổi năm → tháng\n2. Nhập thẻ lỗi 4111 1111 1111 1111\n"
       "3. Kiểm tra charge trên UnivaPay\n4. Kiểm tra bot_contracts",
       "Thẻ lỗi 4111 1111 1111 1111",
       "- UnivaPay: charge lúc transfer chuyển「Canceled」, thêm 1 bản ghi「Failed」\n"
       "- DB: quay về hợp đồng cũ — status=1, status_payment=1, expired_date_contract GIỮ NGUYÊN",
       env="PRODUCTION",
       note="Nguồn: r331, r337, r353, r360. RULE-08."),

    tc("Đổi kỳ thanh toán", "FUNC-006", "Normal",
       "Đổi kỳ sau khi nhập lại thẻ đúng → đăng ký thẻ mới, KHÔNG bill tiền ngay",
       "- Hợp đồng standard năm bill transfer, vừa nhập thẻ lỗi",
       "1. Nhập lại thẻ hợp lệ, bấm đăng ký\n2. Kiểm tra UnivaPay\n3. Kiểm tra bot_contracts",
       "Thẻ hợp lệ 4242 4242 4242 4242",
       "- Đổi năm → tháng thành công, màn detail hiện thẻ mới\n"
       "- UnivaPay: thêm bản ghi status「Authorized」(KHÔNG charge tiền)\n"
       "- DB: status_payment=1, expired_date_contract giữ nguyên",
       env="PRODUCTION",
       note="Nguồn: r332, r338, r354, r361."),

    tc("Đổi kỳ thanh toán", "FUNC-006", "Normal",
       "Đổi kỳ ở hợp đồng ĐANG 延滞中 → bill tiền ngay 1 tháng, expired_date cộng theo mốc cũ",
       "- Hợp đồng standard năm đang 延滞中 (chưa quá 7 ngày), bill transfer",
       "1. Bấm đổi năm → tháng, nhập thẻ hợp lệ\n2. Kiểm tra UnivaPay\n"
       "3. Kiểm tra bot_contracts và lịch sử hóa đơn",
       "expired_date cũ = 2026/03/01, thẻ hợp lệ",
       "- Bill thành công 1 tháng ngay khi đổi kỳ\n"
       "- UnivaPay: charge mới status「Successful」\n"
       "- DB: status_payment=1, payment_method=1, expired_date_contract = expired_date CŨ + 1 tháng",
       env="PRODUCTION",
       note="Nguồn: r395, r397, r366. Điểm khác biệt then chốt so với case còn hạn (không bill tiền)."),

    tc("Đổi kỳ thanh toán", "STATE-002", "Abnormal",
       "Bỏ dở luồng đổi kỳ ở step 1 hoặc step 2 → contract_bill_type không đổi",
       "- Hợp đồng standard năm, bill card\n" + DTL,
       "1. Vào màn đổi kỳ, ở step 1 bấm quay lại\n2. Kiểm tra contract_bill_type\n"
       "3. Vào lại, tới step 2 rồi bấm quay lại\n4. Kiểm tra contract_bill_type",
       "2 điểm thoát: step 1 và step 2",
       "Cả 2 lần: bot_contracts.contract_bill_type giữ nguyên giá trị cũ, không sinh dòng xám thông báo",
       note="Nguồn: r500, r501, r518, r519, r531, r532."),

    tc("Đổi kỳ thanh toán", "DATA-002", "Normal",
       "Đổi tháng → năm: nút đổi phương thức 銀行振込に変更する xuất hiện",
       "- Hợp đồng standard tháng, bill card\n" + DTL,
       "1. Đọc nhãn nút đổi kỳ\n2. Bấm「次回決済から年払いに変更する」và hoàn tất\n"
       "3. Đọc mục 決済方法 và các nút\n4. Kiểm tra ngày hiển thị",
       "contract_bill_type = month → year, expired_date = 2026/05/06",
       "- Sau khi đổi: hiện dòng「次回決済日:2026年05月07日から年払いに変更されます」(expired_date + 1 ngày)\n"
       "- Mục 決済方法 hiện thêm nút「銀行振込に変更する」cho phép đổi card → transfer\n"
       "- Số tiền ở màn list và detail vẫn theo GIÁ THÁNG cho tới ngày hết hạn",
       note="Nguồn: r529-r539, r1569-r1578."),

    tc("Đổi kỳ thanh toán", "UI-005", "Normal",
       "Hợp đồng bill THÁNG → không hiện nút đổi phương thức thanh toán",
       "- Hợp đồng standard tháng, bill card, chưa đăng ký đổi kỳ\n" + DTL,
       "1. Quan sát mục 決済方法",
       "contract_bill_type = month",
       "KHÔNG hiển thị nút「決済方法の変更」/「銀行振込に変更する」(bill tháng chỉ dùng thẻ)",
       note="Nguồn: r583."),

    # ═════════════ 16. Đổi phương thức thanh toán ═════════════
    tc("Đổi phương thức thanh toán", "UI-001", "Normal",
       "Nhãn nút đổi phương thức theo phương thức hiện tại",
       "- 1 hợp đồng bill transfer và 1 hợp đồng bill card (đều bill năm)\n" + DTL,
       "1. Mở detail hợp đồng transfer → đọc nhãn nút\n2. Mở detail hợp đồng card → đọc nhãn nút",
       "payment_method = 2 và = 1",
       "- Đang transfer → nút「クレジットカードに変更する」\n- Đang card → nút「銀行振込に変更する」",
       note="Nguồn: r541, r542."),

    tc("Đổi phương thức thanh toán", "FUNC-006", "Normal",
       "Đổi card → chuyển khoản: màn xác nhận + modal hoàn tất theo trạng thái phát hành STK",
       "- Hợp đồng standard năm, bill card, còn hạn\n" + DTL,
       "1. Click「銀行振込に変更する」→ đọc màn「決済方法変更の確認」\n2. Bấm「変更する」\n"
       "3. Quan sát modal hoàn tất khi tài khoản CHƯA phát hành\n"
       "4. Lặp lại kịch bản khi tài khoản ĐÃ phát hành, bấm「振込口座情報を確認する」",
       "expired_date_contract = 2026/10/31",
       "- Màn xác nhận hiện「クレジットカード → 銀行振込」\n"
       "- Chưa phát hành: modal hiện「次回決済日：2026年10月31日から銀行振込に変更されます」và "
       "「YYYY/MM/DDに振込口座が発行されます」(= expired_date − 30 ngày)\n"
       "- Đã phát hành: bấm「振込口座情報を確認する」mở màn thông tin tài khoản",
       note="Nguồn: r544-r551."),

    tc("Đổi phương thức thanh toán", "DATA-001", "Normal",
       "Sau khi đổi phương thức, trước ngày hết hạn → vẫn hiển thị phương thức CŨ + payment_method_old",
       "- Hợp đồng standard năm vừa đăng ký đổi card → transfer, chưa tới expired_date\n" + DTL,
       "1. Đọc mục 決済方法 ở màn list và màn detail\n2. Đọc dòng thông báo\n"
       "3. Kiểm tra bot_contracts.payment_method_old",
       "Đã đăng ký đổi sang transfer, chưa tới hạn",
       "- Vẫn hiển thị「クレジットカード」\n"
       "- Có dòng「次回決済日：2026年10月31日から銀行振込に変更されます」(+ dòng ngày phát hành STK nếu chưa phát hành)\n"
       "- DB: payment_method_old = phương thức cũ",
       note="Nguồn: r555, r556, r561, r576, r577."),

    tc("Đổi phương thức thanh toán", "DATA-001", "Normal",
       "Tới ngày hết hạn + job chạy → phương thức đổi thật, payment_method_old = NULL",
       "- Hợp đồng đã đăng ký đổi card → transfer, đã tới expired_date và job đã chạy\n" + DTL,
       "1. Đọc mục 決済方法\n2. Kiểm tra dòng thông báo\n3. Kiểm tra bot_contracts.payment_method_old\n"
       "4. Đọc khối 振込先情報",
       "Đã qua expired_date, job bill đã chạy",
       "- 決済方法 hiện「銀行振込」\n- Dòng thông báo biến mất\n"
       "- DB: payment_method_old = NULL\n- Khối 振込先情報 hiện thông tin chuyển khoản",
       env="PRODUCTION",
       note="Nguồn: r558, r559, r579. RULE-08: phụ thuộc job → PRODUCTION."),

    tc("Đổi phương thức thanh toán", "FUNC-006", "Normal",
       "Đổi chuyển khoản → thẻ: 3 step, phải nhập thẻ, ngày áp dụng = expired_date + 1 ngày",
       "- Hợp đồng standard năm, bill transfer, còn hạn\n" + DTL,
       "1. Click「決済方法の変更」\n2. Step 1 nhập thẻ hợp lệ\n"
       "3. Đọc step 2: お支払い期間, 決済方法, dòng ngày\n4. Bấm「変更する」→ quan sát step 3",
       "expired_date_contract = 2026/10/30, thẻ hợp lệ",
       "- Step 2 hiện「銀行振込 → クレジットカード」và dòng「YYYY/MM/DD からクレジットカード決済に"
       "変更されます」với ngày = expired_date + 1 ngày\n- Step 3 hiện màn hoàn tất\n"
       "- Sau đó màn detail hiện「次回決済日：…に登録したカードに請求が行われます」",
       note="Nguồn: r563-r576."),

    tc("Đổi phương thức thanh toán", "STATE-002", "Normal",
       "Hoàn tác đổi phương thức trước ngày hết hạn → hiển thị lại thông tin cũ",
       "- Hợp đồng đã đăng ký đổi phương thức, chưa tới expired_date\n" + DTL,
       "1. Bấm nút hoàn tác đổi phương thức\n2. Đọc mục 決済方法\n3. Kiểm tra payment_method_old",
       "Đã đăng ký đổi card → transfer",
       "- Hiển thị lại thông tin thẻ (phương thức cũ)\n- Dòng thông báo đổi phương thức biến mất",
       note="Nguồn: r557, r578."),

    tc("Đổi phương thức thanh toán", "STATE-002", "Abnormal",
       "Bỏ dở luồng đổi phương thức → payment_method không đổi",
       "- Hợp đồng standard năm\n" + DTL,
       "1. Vào màn đổi phương thức, thoát ở step 1\n2. Kiểm tra payment_method\n"
       "3. Vào lại, thoát ở step 2\n4. Kiểm tra payment_method",
       "2 điểm thoát: step 1 và step 2",
       "Cả 2 lần: bot_contracts.payment_method giữ nguyên giá trị cũ",
       note="Nguồn: r554, r574, r575."),

    tc("Đổi phương thức thanh toán", "FUNC-006", "Normal",
       "Đổi transfer → card khi hợp đồng ĐANG chờ chuyển khoản → hủy charge transfer trên UnivaPay",
       "- Hợp đồng standard năm bill transfer đang 入金待ち (status_payment=4/5/6)",
       "1. Bấm đổi phương thức sang thẻ, nhập thẻ hợp lệ\n2. Kiểm tra charge transfer trên UnivaPay\n"
       "3. Kiểm tra bot_contracts",
       "Charge transfer đang pending trên UnivaPay",
       "- Charge transfer cũ chuyển sang「Canceled」trên UnivaPay\n"
       "- DB: charge id transfer được thay bằng charge id thẻ mới",
       env="PRODUCTION",
       note="Nguồn: r329, r333, r335, r339, r380, r387. RULE-08."),

    # ═════════════ 17. Thẻ chính & thẻ phụ ═════════════
    tc("Thẻ chính & thẻ phụ", "UI-001", "Normal",
       "Màn đổi thẻ chính hiển thị đủ 3 bước",
       STD,
       "1. Click「メインカード情報を変更する」\n2. Quan sát thanh bước",
       "—",
       "Hiện đủ 3 bước:「① クレジットカード情報入力」·「② 契約内容確認」·「③ カード情報変更完了」",
       note="Nguồn: r407, r408."),

    tc("Thẻ chính & thẻ phụ", "DATA-001", "Normal",
       "Bước 2 契約内容確認 hiển thị đúng plan, số tiền, phương thức và 4 số cuối thẻ MỚI",
       STD + "\n- Đã nhập thẻ mới 5555 5555 5555 4444 ở bước 1",
       "1. Sang bước 2, đọc mục ご契約プラン, ご利用料金, 決済方法, 新規決済カード情報",
       "Plan standard năm, thẻ mới đuôi 4444",
       "- ご契約プラン hiện đúng plan (スタンダード / プロ)\n- ご利用料金 hiện số tiền theo chu kỳ (năm/2 năm)\n"
       "- 決済方法「クレジットカード」\n- 新規決済カード情報 format ****-****-****-4444",
       note="Nguồn: r422, r429-r434."),

    tc("Thẻ chính & thẻ phụ", "FUNC-006", "Normal",
       "Đổi thẻ chính khi hợp đồng CÒN HẠN → không bill tiền, chỉ cập nhật thẻ",
       STD,
       "1. Đổi thẻ chính sang thẻ hợp lệ mới\n2. Kiểm tra UnivaPay xem có charge tiền không\n"
       "3. Kiểm tra bot_contracts.univa_last_four_card và màn detail",
       "Hợp đồng còn hạn, thẻ mới hợp lệ",
       "- KHÔNG phát sinh giao dịch charge tiền\n"
       "- DB: univa_last_four_card = 4 số cuối thẻ mới; màn detail hiện thẻ mới\n"
       "- Bước 3 hiện「カード情報の変更が完了しました」",
       env="PRODUCTION",
       note="Nguồn: r436, r437, r22 (tab hóa đơn). RULE-08: bill tiền → PRODUCTION."),

    tc("Thẻ chính & thẻ phụ", "FUNC-006", "Abnormal",
       "Đổi thẻ chính thất bại → màn カード情報変更エラー, cho đăng ký thẻ khác",
       STD,
       "1. Nhập thẻ lỗi ở bước 1 → bấm thanh toán\n2. Đọc title và nội dung màn lỗi\n"
       "3. Bấm「別のカードを登録する」→ nhập thẻ đúng\n4. Kiểm tra thẻ hiển thị ở màn detail",
       "Thẻ lỗi 4111 1111 1111 1111, sau đó thẻ đúng",
       "- Màn lỗi title「カード情報変更エラー」, nội dung「カード情報の変更に失敗しました。"
       "※失敗の原因は、ご利用のカード会社様にご確認ください。」\n"
       "- Bấm「別のカードを登録する」quay lại màn nhập thẻ; nhập đúng thì đổi thẻ thành công",
       note="Nguồn: r439-r443."),

    tc("Thẻ chính & thẻ phụ", "FUNC-003", "Normal",
       "Đăng ký thẻ phụ: 2 bước, ghi vào subcard_bot_contracts",
       STD + "\n- Hợp đồng chưa có thẻ phụ",
       "1. Click「サブ決済カードを登録する」\n2. Đọc breadcrumb và mô tả\n"
       "3. Quan sát thanh bước\n4. Nhập thẻ hợp lệ, bấm「カードを登録する」\n"
       "5. Kiểm tra subcard_bot_contracts và màn detail",
       "Thẻ phụ 5555 5555 5555 4444",
       "- Breadcrumb「契約情報・領収書 > 契約詳細 > サブカードの登録」\n"
       "- Mô tả「メインカードの決済が失敗した場合に自動的にサブカードで決済を行います。」\n"
       "- 2 bước: ① クレジットカード情報入力 · ② 登録完了\n"
       "- DB: subcard_bot_contracts có bản ghi mới; màn detail hiện ****-****-****-4444",
       note="Nguồn: r450-r465."),

    tc("Thẻ chính & thẻ phụ", "DATA-001", "Normal",
       "Chưa có thẻ phụ → mục サブ決済カード情報 hiện 登録なし",
       STD + "\n- Hợp đồng chưa đăng ký thẻ phụ",
       "1. Đọc mục「サブ決済カード情報」",
       "subcard_bot_contracts không có bản ghi",
       "Hiển thị text「登録なし」",
       note="Nguồn: r210, r224 (Bill max friend)."),

    tc("Thẻ chính & thẻ phụ", "FUNC-003", "Abnormal",
       "Đăng ký thẻ phụ thất bại → màn lỗi riêng của sub card",
       STD,
       "1. Nhập thẻ lỗi ở màn đăng ký thẻ phụ\n2. Đọc nội dung màn lỗi\n"
       "3. Bấm「別のカードを登録する」rồi nhập thẻ đúng",
       "Thẻ lỗi 4111 1111 1111 1111",
       "- Màn lỗi hiện「サブカードの登録に失敗しました。※失敗の原因に関しましては、"
       "ご利用のカード会社様にご確認ください。」\n"
       "- Nhập lại thẻ đúng thì đăng ký thành công",
       note="Nguồn: r466-r470."),

    tc("Thẻ chính & thẻ phụ", "FUNC-003", "Normal",
       "Xóa thẻ phụ: modal xác nhận + xóa bản ghi DB",
       STD + "\n- Hợp đồng đã có thẻ phụ",
       "1. Click「カード情報を削除」→ đọc modal\n2. Click「閉じる」kiểm tra không xóa\n"
       "3. Mở lại, click「サブ決済カードを削除する」\n4. Kiểm tra màn detail và subcard_bot_contracts",
       "Hợp đồng có 1 thẻ phụ",
       "- Modal「サブ決済カードの削除」hiện text「サブ決済カードを削除しますがよろしいですか？」\n"
       "- Bấm 閉じる: không xóa\n"
       "- Bấm xóa: màn detail hiện「登録なし」và bản ghi trong subcard_bot_contracts bị xóa",
       note="Nguồn: r211-r213, r472-r476."),

    tc("Thẻ chính & thẻ phụ", "FUNC-003", "Normal",
       "Xóa → đăng ký lại → đổi thẻ phụ nhiều lần đều cập nhật đúng",
       STD + "\n- Hợp đồng đang có thẻ phụ",
       "1. Xóa thẻ phụ → đăng ký lại thẻ phụ mới → xóa lần nữa\n"
       "2. Đăng ký lại rồi đổi thẻ phụ lần 2, lần 3\n"
       "3. Sau mỗi bước kiểm tra subcard_bot_contracts.univa_last_four_card và màn list/detail",
       "3 lần đổi thẻ phụ liên tiếp",
       "Mỗi lần: subcard_bot_contracts cập nhật đúng 4 số cuối mới, "
       "màn detail và màn list hiển thị đồng bộ; không sinh bản ghi thẻ phụ trùng",
       note="Nguồn: r476-r481 (nhiều dòng cùng kết quả → gộp)."),

    tc("Thẻ chính & thẻ phụ", "REG-001", "Normal",
       "Đã có thẻ phụ vẫn đổi được thẻ chính; đổi thất bại thì giữ nguyên cả 2 thẻ",
       STD + "\n- Hợp đồng đã có cả thẻ chính và thẻ phụ",
       "1. Kiểm tra nút「メインカード情報を変更する」vẫn hiện\n"
       "2. Đổi thẻ chính thành công → kiểm tra bot_contracts.univa_last_four_card và thẻ phụ\n"
       "3. Đổi thẻ chính bằng thẻ lỗi → kiểm tra lại cả 2 thẻ",
       "Thẻ chính mới hợp lệ, sau đó thẻ lỗi",
       "- Nút đổi thẻ chính vẫn hiển thị khi đã có thẻ phụ\n"
       "- Thành công: chỉ thẻ chính đổi, thẻ phụ giữ nguyên\n"
       "- Thất bại: hiện modal lỗi, cả thẻ chính và thẻ phụ trên GUI + DB đều giữ nguyên",
       note="Nguồn: r445-r448. Ghi 'regression' theo quy chuẩn Loại case."),

    tc("Thẻ chính & thẻ phụ", "FUNC-006", "Normal",
       "Đổi thẻ khi hợp đồng ĐANG 延滞中 → đổi thẻ kèm bill tiền, chỉ lưu thẻ khi bill thành công",
       "- Hợp đồng chính đang 延滞中",
       "1. Đổi thẻ chính bằng thẻ hợp lệ → kiểm tra bill và thẻ lưu\n"
       "2. Lặp lại với thẻ lỗi → kiểm tra bill, thẻ lưu và trạng thái hợp đồng",
       "Thẻ hợp lệ và thẻ lỗi",
       "- Thẻ hợp lệ: bill thành công → thẻ mới được lưu, hợp đồng về 正常, có lịch sử bill\n"
       "- Thẻ lỗi: báo lỗi, KHÔNG lưu thẻ mới, hợp đồng giữ nguyên 延滞中",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r218-r221 + tab hóa đơn r23-r25. RULE-08."),

    tc("Thẻ chính & thẻ phụ", "UI-005", "Normal",
       "Hợp đồng đã hủy → ẩn nút đổi thẻ chính/phụ",
       "- Hợp đồng ở trạng thái 解約済み\n" + DTL,
       "1. Quan sát khu メイン決済カード情報 và サブ決済カード情報",
       "status = 3",
       "Ẩn các nút đổi/đăng ký thẻ (không cho thao tác thẻ trên hợp đồng đã hủy)",
       note="Nguồn: Bill max friend r222, r230, r235."),

    # ═════════════ 18. Gia hạn hợp đồng ═════════════
    tc("Gia hạn hợp đồng", "UI-001", "Normal",
       "Step 1 màn gia hạn: hiện đúng account, plan, chu kỳ, phương thức và số tiền",
       "- Hợp đồng standard năm bill card, còn hạn\n" + DTL,
       "1. Click「契約期間を1年延長する」\n2. Đọc các mục ở step 1\n"
       "3. Lặp lại với hợp đồng pro năm và hợp đồng bill transfer",
       "3 hợp đồng: standard năm/card, pro năm/card, standard năm/transfer",
       "- 対象アカウント: ảnh + tên bot (chưa kết nối thì hiện「LINE公式アカウント未接続」)\n"
       "- 選択したプラン:「スタンダードプラン」/「プロプラン」\n- chu kỳ:「年間一括払い」\n"
       "- Phương thức: card hiện「登録済みクレジットカード ****-****-****-1234」; "
       "transfer hiện「銀行振込（請求書の発行ができます）」\n- Số tiền đúng theo từng plan",
       note="Nguồn: r794-r801."),

    tc("Gia hạn hợp đồng", "UI-005", "Normal",
       "Checkbox 注意事項 ở màn gia hạn cũng phải cuộn hết mới tick được",
       "- Hợp đồng standard năm\n- Đang ở step 1 màn gia hạn",
       "1. Quan sát checkbox mặc định\n2. Thử tick khi chưa cuộn hết\n3. Cuộn hết rồi tick\n"
       "4. Kiểm tra nút「決済に進む」trước và sau khi tick",
       "—",
       "- Mặc định chưa tích\n- Chưa cuộn hết: checkbox disable\n"
       "- Cuộn hết: tick được, nút「決済に進む」chuyển sang enable và sang được step 2",
       note="Nguồn: r802-r807."),

    tc("Gia hạn hợp đồng", "FUNC-006", "Normal",
       "Gia hạn bằng thẻ đã đăng ký, bill thành công → bỏ qua step 2, expired_date + 1 năm",
       "- Hợp đồng standard năm bill card, expired_date = 2026/10/31, thẻ chính hợp lệ",
       "1. Vào màn gia hạn, tick 注意事項, bấm「決済に進む」\n2. Quan sát màn hình\n"
       "3. Kiểm tra bot_contracts.expired_date_contract và lịch sử bill",
       "expired_date cũ = 2026/10/31",
       "- KHÔNG hiện step 2 nhập thẻ, đi thẳng step 3 (gia hạn thành công)\n"
       "- DB: expired_date_contract = 2027/10/31 (cộng đúng 1 năm)\n- Có bản ghi lịch sử bill mới",
       env="PRODUCTION",
       note="Nguồn: r808, r814. RULE-07 + RULE-08."),

    tc("Gia hạn hợp đồng", "FUNC-006", "Abnormal",
       "Gia hạn bằng thẻ cũ bị lỗi → mở step 2 nhập thẻ; nhập tiếp thẻ lỗi thì không gia hạn",
       "- Hợp đồng standard năm bill card, thẻ chính bị từ chối",
       "1. Vào màn gia hạn, bấm「決済に進む」\n2. Quan sát màn hình\n"
       "3. Ở step 2 nhập thẻ lỗi → quan sát\n4. Kiểm tra expired_date_contract",
       "Thẻ chính lỗi, thẻ nhập thêm cũng lỗi",
       "- Hiện step 2 để nhập thẻ mới\n- Nhập thẻ lỗi: báo lỗi, KHÔNG cập nhật hợp đồng\n"
       "- expired_date_contract giữ nguyên, trạng thái vẫn 正常",
       note="Nguồn: r809, r812, r815, r816."),

    tc("Gia hạn hợp đồng", "STATE-003", "Normal",
       "Gia hạn bằng chuyển khoản: 3 trạng thái theo callback",
       "- Hợp đồng standard năm bill transfer, expired_date = 2026/10/31",
       "1. Vào màn gia hạn → bấm 決済に進む (tạo bill transfer)\n"
       "2. Kiểm tra màn list + expired_date khi CHƯA chuyển khoản\n"
       "3. Chuyển khoản → callback success → kiểm tra lại\n"
       "4. Kịch bản khác: không chuyển khoản → callback fail → kiểm tra lại",
       "expired_date cũ = 2026/10/31",
       "- Chưa chuyển khoản: status「入金待ち」(status_payment=4), expired_date GIỮ NGUYÊN 2026/10/31, "
       "hiện thông tin số tài khoản vừa tạo\n"
       "- Callback success: status「正常」, expired_date = 2027/10/31\n"
       "- Callback fail: status「正常」, expired_date GIỮ NGUYÊN 2026/10/31 (không bị hủy hợp đồng)",
       env="PRODUCTION",
       note="Nguồn: r810, r817-r819. RULE-08."),

    tc("Gia hạn hợp đồng", "FUNC-001", "Normal",
       "Nút điều hướng ở màn gia hạn: キャンセル và 契約詳細に戻る",
       "- Hợp đồng standard năm\n" + DTL,
       "1. Ở step 1 bấm「キャンセル」\n2. Thực hiện lại tới step 3, bấm「契約詳細に戻る」",
       "—",
       "- Bấm キャンセル ở step 1: quay lại màn chi tiết hợp đồng, không tạo giao dịch\n"
       "- Bấm 契約詳細に戻る ở step 3: quay lại màn chi tiết hợp đồng",
       note="Nguồn: r805, r813."),

    tc("Gia hạn hợp đồng", "FUNC-006", "Normal",
       "Gia hạn transfer: đổi kỳ năm → tháng lúc đang chờ chuyển khoản thì không bill thêm",
       "- Hợp đồng standard năm bill transfer vừa gia hạn, đang 入金待ち (status_payment=4)",
       "1. Bấm đổi kỳ năm → tháng, nhập thẻ hợp lệ\n"
       "2. Kiểm tra UnivaPay và bot_contracts",
       "status_payment = 4, thẻ hợp lệ",
       "- Charge transfer cũ chuyển「Canceled」\n"
       "- Đổi kỳ thành công nhưng KHÔNG bill tiền (charge thẻ mới chỉ Authorized)\n"
       "- DB: contract_bill_type = month, payment_method=1, expired_date_contract giữ nguyên",
       env="PRODUCTION",
       note="Nguồn: r379-r383, r387-r390."),
]
