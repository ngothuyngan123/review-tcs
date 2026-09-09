# -*- coding: utf-8 -*-
"""FA-015 — Nhóm 2: Tạo trường thông tin theo 6 kiểu dữ liệu.

Nguồn chính:
- 10.2 TCsLine_friend_information /「test fix bug」khối SpecImprove #33697 (01/2026) r144-r156
  (validate trùng option value) và khối #36201 r198-r203.
- 10.2 /「check setting-action-friend-info-date」(10/2025 → 04/2026) r3-r16 (setting action ngày tháng).
- TCsLine_ModalAction /「Thêm option random cho action friend infor point」(11/2023 + Feature #24521).
- 10.2 /「test fix bug」khối Bug KH #38469 + Support #38536 (07/2026) r276-r311, r501-r515.
"""
from _common import tc

ADM = "- Đăng nhập admin bot A (plan có phí), mở /basic/friend-information"
NEW = ADM + "\n- Click「新規作成」để mở màn tạo mới"
DUP_MSG = "選択肢の表示名が重複しています。異なる値を入力してください。"

S2 = [
    # ══════════════════ Tạo info — chung ══════════════════
    tc("Tạo info — chung", "UI-001", "Normal",
       "Màn tạo mới hiển thị đủ 3 field chung + dropdown 情報タイプ có đúng 6 lựa chọn",
       NEW,
       "1. Quan sát tiêu đề trang và 3 field chung\n2. Mở dropdown「情報タイプ選択」và liệt kê options\n"
       "3. Chụp màn hình",
       "—",
       "- Tiêu đề trang「友だち情報作成」\n"
       "- Có 3 field:「友だち情報（管理名）」(textbox),「フォルダ」(dropdown),「情報タイプ選択」(dropdown)\n"
       "- Dropdown 情報タイプ có đúng 6 lựa chọn:「選択肢」「記述」「年月日」「画像」「PDF」「ポイント」\n"
       "- Mặc định chọn「選択肢」, folder mặc định là folder đang đứng ở màn list\n"
       "- Có ghi chú「※保存後の変更不可」cạnh 情報タイプ",
       note="Evidence: ảnh chụp. Nguồn: spec ui-spec.md:93-95."),

    tc("Tạo info — chung", "UI-INPUT-001", "Normal",
       "管理名 hiển thị bộ đếm ký tự N/20文字 và cập nhật theo số ký tự đã gõ",
       NEW,
       "1. Gõ dần 5 → 12 → 20 ký tự vào 管理名\n2. Sau mỗi lần quan sát bộ đếm",
       "5 / 12 / 20 ký tự",
       "- Bộ đếm hiển thị lần lượt 5/20文字, 12/20文字, 20/20文字",
       note="Nguồn: spec ui-spec.md:93. Corpus không có TC → AI bổ sung."),

    tc("Tạo info — chung", "UI-INPUT-001", "Boundary",
       "管理名 đúng 20 ký tự → lưu được, hiển thị đủ ở màn list",
       NEW,
       "1. Nhập 管理名 đúng 20 ký tự\n2. Chọn 情報タイプ =「記述」\n3. Lưu\n"
       "4. Xem cột 管理名 ở màn list",
       "「あいうえおかきくけこさしすせそたちつてと」(20 ký tự JP)",
       "- Lưu thành công\n- Màn list hiển thị đủ 20 ký tự, không bị cắt giữa chừng",
       note="TC cận biên do AI bổ sung theo spec ui-spec.md:93."),

    tc("Tạo info — chung", "UI-INPUT-001", "Boundary",
       "管理名 21 ký tự (gõ và paste) → không lưu được quá 20 ký tự",
       NEW,
       "1. Gõ 21 ký tự vào 管理名\n2. Xóa, paste chuỗi 50 ký tự\n3. Lưu\n"
       "4. Kiểm tra 管理名 hiển thị ở màn list",
       "Gõ 21 ký tự JP · paste 50 ký tự latinh",
       "- Ô nhập không nhận quá 20 ký tự (cả gõ và paste), HOẶC báo lỗi giới hạn khi lưu\n"
       "- Không tồn tại trường nào có 管理名 dài hơn 20 ký tự",
       note="⚠️ Spec chỉ ghi 'max 20 ký tự (client)', chưa chốt chặn-input hay báo lỗi — xem MT-07. AI bổ sung."),

    tc("Tạo info — chung", "UI-INPUT-001", "Abnormal",
       "Bỏ trống 管理名 → không lưu được",
       NEW,
       "1. Để trống 管理名\n2. Chọn 情報タイプ bất kỳ\n3. Click「保存」\n"
       "4. Nhập toàn dấu cách rồi lưu lại",
       "Lần 1: rỗng · Lần 2: 5 dấu cách",
       "- Không tạo trường mới\n- Hiển thị message yêu cầu nhập 管理名\n"
       "- Màn list không xuất hiện dòng trống",
       note="Spec ui-spec.md:93 ghi 'Bắt buộc: Có'. Corpus không có TC → AI bổ sung; hành vi với chuỗi toàn space cần Leader xác nhận."),

    tc("Tạo info — chung", "DATA-TEXT-001", "Normal",
       "管理名 nhận ký tự đặc biệt / emoji / JP full-width & half-width → lưu và hiển thị verbatim",
       NEW,
       "1. Lần lượt tạo 4 trường kiểu「記述」với 4 tên khác nhau\n2. Sau mỗi lần lưu, đọc lại 管理名 ở màn list\n"
       "3. Vào màn edit đọc lại giá trị trong ô nhập",
       "「予約情報」·「ﾖﾔｸ情報」·「A&B<test>」·「予約😀」",
       "- Cả 4 trường lưu thành công\n"
       "- Màn list và màn edit hiển thị đúng chuỗi đã nhập, không bị escape thành &amp;/&lt; hoặc mất emoji",
       note="4 input cùng 1 kết quả nên gộp 1 TC. TC do AI bổ sung theo DATA-TEXT-001."),

    tc("Tạo info — chung", "FUNC-001", "Normal",
       "Dropdown フォルダ liệt kê đủ folder và lưu đúng folder đã chọn",
       NEW + "\n- Bot A có 3 folder tự tạo",
       "1. Mở dropdown「フォルダ」\n2. Đối chiếu danh sách với panel folder ở màn list\n"
       "3. Chọn folder thứ 3, nhập 管理名, lưu\n4. Về màn list kiểm tra trường nằm ở folder nào",
       "3 folder tự tạo +「未分類」",
       "- Dropdown liệt kê đủ「未分類」+ 3 folder tự tạo, không chứa folder của bot khác\n"
       "- Trường mới nằm đúng folder thứ 3, count folder đó +1",
       note="Nguồn: spec ui-spec.md:94 + corpus r214."),

    tc("Tạo info — chung", "STATE-001", "Normal",
       "Nút quay lại / hủy ở màn tạo → không tạo trường, dữ liệu nhập dở không lưu",
       NEW,
       "1. Nhập 管理名 và cấu hình option\n2. Rời màn tạo bằng nút quay lại (không bấm 保存)\n"
       "3. Về màn list đếm số trường\n4. Vào lại màn tạo mới",
       "管理名 =「draft-info」",
       "- Không có trường「draft-info」ở màn list, count folder không đổi\n"
       "- Màn tạo mới mở lại với form trống",
       note="TC do AI bổ sung theo STATE-001 (corpus không có), cần Leader xác nhận có popup cảnh báo mất dữ liệu hay không."),

    tc("Tạo info — chung", "FUNC-001", "Abnormal",
       "情報タイプ bị khóa ở màn EDIT (không đổi được sau khi lưu)",
       ADM + "\n- Có sẵn trường「type_select」kiểu 選択肢 đã lưu",
       "1. Mở màn edit của「type_select」\n2. Thử mở dropdown「情報タイプ選択」\n"
       "3. Thử đổi sang「ポイント」",
       "Trường kiểu 選択肢",
       "- Dropdown 情報タイプ ở trạng thái disabled, không mở/không đổi được\n"
       "- Hiển thị ghi chú「※保存後の変更不可」\n"
       "- Sau khi lưu, 情報タイプ ở màn list vẫn là「選択肢」",
       note="Spec ui-spec.md:95 + feature-spec BR-02."),

    tc("Tạo info — chung", "SEC-001", "Abnormal",
       "Gọi trực tiếp API lưu setting với type_data khác type đã lưu → không đổi được kiểu",
       ADM + "\n- Trường「type_select」kiểu 選択肢 (type_data=1) đã có 3 bạn có giá trị",
       "1. Mở màn edit, bấm 保存 và bắt request bằng DevTools\n"
       "2. Gửi lại request với type_data = 6 (ポイント)\n3. Reload màn list và màn edit",
       "type_data: 1 → 6",
       "- 情報タイプ ở màn list vẫn là「選択肢」\n"
       "- Giá trị của 3 bạn không bị hỏng/mất\n"
       "- Request bị từ chối hoặc bị bỏ qua trường type_data",
       note="TC do AI bổ sung theo SEC-001 — spec chỉ ghi disabled ở client, không nêu chặn phía server. Cần Leader xác nhận (xem MT-07)."),

    tc("Tạo info — chung", "STATE-DEP-001", "Abnormal",
       "Bot đang trong tiến trình backup → mọi thao tác lưu/xóa trường bị chặn có thông báo",
       "- Bot A đang có tiến trình backup ở trạng thái đang chạy",
       "1. Mở màn tạo mới, nhập 管理名, click「保存」\n2. Thử xóa 1 trường ở màn list\n"
       "3. Thử tạo folder mới",
       "Bot đang backup",
       "- Cả 3 thao tác đều bị chặn, hiển thị thông báo bot đang backup\n"
       "- Không trường/folder nào được tạo hoặc xóa\n"
       "- Sau khi backup xong, thao tác lại thành công",
       note="Spec BR-07 backup lock (áp cho mọi thao tác write). Corpus không có TC → AI bổ sung."),

    tc("Tạo info — chung", "PERM-001", "Abnormal",
       "Account staff không có quyền màn 友だち情報管理 → không vào được, hiện message quyền",
       "- Tài khoản staff (副管理人 / 運用者) chưa được cấp quyền màn friend information",
       "1. Đăng nhập bằng account staff\n2. Rê chuột vào mục menu 友だち情報管理\n"
       "3. Click vào mục menu\n4. Gõ thẳng URL /basic/friend-information",
       "Staff chưa cấp quyền",
       "- Rê chuột hiện message:\n操作できません。\nこの機能の操作権限が付与されていません。\n"
       "主管理者に操作権限を付与してもらうことで操作が可能となります。\n"
       "- Click không mở được màn\n- Gõ thẳng URL cũng không vào được màn",
       note="Nguồn: TCsLine_Improve chung /「Phân quyền」(2023-11-10) r4, r7-r12 — áp cho màn friend info. "
            "⚠️ TC gốc > 2 năm và spec Gap #2 ghi 'chưa xác nhận phân quyền' → CẦN VERIFY LẠI, xem MT-12."),

    # ══════════════════ Info kiểu Lựa chọn ══════════════════
    tc("Info kiểu Lựa chọn", "UI-001", "Normal",
       "Màn tạo kiểu 選択肢 hiển thị đủ khối「選択肢・アクション」",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Quan sát khối「選択肢・アクション」\n2. Bấm「追加」2 lần\n3. Chụp màn hình",
       "—",
       "- Có nút「追加」thêm dòng lựa chọn\n"
       "- Có radio「稼働設定」với 2 lựa chọn「一度のみ」/「何度でも稼働」, mặc định「一度のみ」\n"
       "- Mỗi dòng lựa chọn có: textbox tên lựa chọn, nút「設定する」(action), 3 icon lên/xuống/xóa\n"
       "- Bấm「追加」2 lần → có 2 dòng lựa chọn",
       note="Evidence: ảnh chụp. Nguồn: spec ui-spec.md:97-112."),

    tc("Info kiểu Lựa chọn", "FUNC-001", "Normal",
       "Tạo trường 選択肢 với nhiều option → lưu thành công, gán được cho bạn bè",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Nhập 管理名「予約プラン」\n2. Thêm 3 option\n3. Lưu\n"
       "4. Mở màn 友だち詳細 của 1 bạn, chọn giá trị cho trường này\n5. Về màn list xem 回答人数",
       "3 option: 「プランA」「プランB」「プランC」\nBạn U1 chọn「プランB」",
       "- Trường lưu thành công, màn list hiển thị 情報タイプ =「選択肢」\n"
       "- Màn 友だち詳細 hiển thị đúng 3 option để chọn\n"
       "- Sau khi gán, giá trị của U1 hiển thị「プランB」ở màn 友だち詳細 và right bar chat 1:1\n"
       "- 回答人数 của trường =「1人」",
       note="RULE-07. Nguồn: r155, r198."),

    tc("Info kiểu Lựa chọn", "FUNC-UNIQ-001", "Abnormal",
       "Nhập 2 option TRÙNG TÊN trong cùng 1 trường → báo lỗi, không lưu",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Nhập 管理名\n2. Thêm 2 option cùng giá trị\n3. Click「保存」\n"
       "4. Lặp lại với cặp giá trị số",
       "Lần 1: option 1 =「0」, option 2 =「0」\nLần 2: option 1 =「1」, option 2 =「1」",
       "- Hiển thị message lỗi:\n" + DUP_MSG + "\n"
       "- Trường KHÔNG được lưu (màn list không có trường mới)",
       note="SpecImprove #33697 (01/2026). Nguồn: r145-r146."),

    tc("Info kiểu Lựa chọn", "FUNC-UNIQ-001", "Boundary",
       "2 option chỉ khác nhau dấu cách đầu/cuối → vẫn coi là trùng, báo lỗi",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Thêm option 1 =「プランA」\n2. Thêm option 2 =「 プランA 」(có space đầu và cuối)\n"
       "3. Click「保存」",
       "「プランA」vs「 プランA 」",
       "- Hiển thị message lỗi:\n" + DUP_MSG + "\n- Trường không được lưu",
       note="Nguồn: r147 (#33697) — xác nhận so sánh có trim."),

    tc("Info kiểu Lựa chọn", "FUNC-001", "Normal",
       "Sau khi bị báo lỗi trùng option → sửa thành giá trị hợp lệ → lưu được",
       NEW + "\n- Đang ở màn tạo và vừa bị báo lỗi trùng option",
       "1. Sửa option 2 thành giá trị khác\n2. Click「保存」\n3. Về màn list kiểm tra",
       "option 1 =「0」, option 2 sửa thành「1」",
       "- Message lỗi biến mất\n- Trường lưu thành công và hiển thị ở màn list\n"
       "- Vào lại màn edit thấy đủ 2 option「0」và「1」",
       note="Nguồn: r148 (#33697)."),

    tc("Info kiểu Lựa chọn", "FUNC-UNIQ-001", "Normal",
       "2 trường 選択肢 KHÁC NHAU trong cùng folder được phép có option trùng tên",
       ADM + "\n- Folder F đã có trường Info-1 kiểu 選択肢 với option「0」",
       "1. Tạo trường Info-2 kiểu 選択肢 trong cùng folder F\n2. Nhập option có cùng giá trị「0」\n"
       "3. Lưu\n4. Gán Info-2 =「0」cho bạn U1\n5. Kiểm tra giá trị của U1 ở 2 trường",
       "Info-1 option「0」· Info-2 option「0」· U1 được gán Info-2",
       "- Info-2 lưu thành công (không báo lỗi trùng)\n"
       "- U1 chỉ ghi nhận giá trị ở Info-2, Info-1 vẫn trống\n"
       "- 回答人数: Info-2 = 1人, Info-1 giữ nguyên",
       note="Phạm vi unique = trong cùng 1 trường. Nguồn: r149 (#33697)."),

    tc("Info kiểu Lựa chọn", "FUNC-UNIQ-001", "Abnormal",
       "Copy trường 選択肢 rồi tạo option trùng trong bản copy → vẫn báo lỗi trùng",
       ADM + "\n- Có trường 選択肢 với 2 option",
       "1. Copy trường đó\n2. Ở màn copy, thêm 1 option trùng tên với option sẵn có\n3. Lưu",
       "Option trùng:「プランA」",
       "- Hiển thị message lỗi:\n" + DUP_MSG + "\n- Bản copy không được lưu",
       note="Nguồn: r156 (#33697)."),

    tc("Info kiểu Lựa chọn", "FUNC-001", "Normal",
       "Gắn action cho từng option qua dialog action → lưu và hiển thị preview đúng",
       NEW + "\n- Bot A có sẵn 1 tag「VIP」và 1 kịch bản",
       "1. Tạo trường 選択肢 với 2 option\n2. Option 1: bấm「設定する」→ chọn action gắn tag「VIP」\n"
       "3. Option 2: chọn action gửi kịch bản\n4. Lưu\n5. Vào lại màn edit đọc preview action của 2 option",
       "Option 1 → tag「VIP」· Option 2 → kịch bản S1",
       "- Lưu thành công\n"
       "- Màn edit hiển thị preview action đúng loại và đúng tên đối tượng cho từng option\n"
       "- 2 option không bị dùng chung 1 action",
       note="SC-004. Nguồn: spec SCR-FRI-06 + corpus r231, r267."),

    tc("Info kiểu Lựa chọn", "FUNC-001", "Normal",
       "Bạn bè chọn option có action → action chạy đúng ở phía LINE",
       "- Trường 選択肢「予約プラン」, option「プランA」gắn action gửi tin nhắn text\n"
       "- Bạn U1 chưa có giá trị ở trường này\n- 稼働設定 =「一度のみ」",
       "1. Ở màn 友だち詳細 của U1, gán giá trị「プランA」\n2. Mở LINE app của U1\n"
       "3. Kiểm tra lịch sử ở màn 友だち詳細",
       "U1 ← 「プランA」",
       "- U1 nhận đúng tin nhắn text đã cấu hình trên LINE app\n"
       "- Màn 友だち詳細 ghi lịch sử gán giá trị\n- 回答人数 tăng 1",
       note="RULE-06 (đi tới output cuối = LINE app). Nguồn: r267 (vế 'action gắn tag chạy bình thường phía line user')."),

    tc("Info kiểu Lựa chọn", "STATE-001", "Normal",
       "稼働設定 =「一度のみ」→ gán lại cùng option lần 2 KHÔNG chạy action lần nữa",
       "- Trường 選択肢, option「プランA」gắn action gửi text, 稼働設定 =「一度のみ」\n"
       "- U1 đã được gán「プランA」và đã nhận tin nhắn 1 lần",
       "1. Ở màn 友だち詳細 của U1, đổi sang「プランB」rồi đổi lại「プランA」\n"
       "2. Mở LINE app của U1 đếm số tin nhắn nhận được",
       "Gán「プランA」lần 2",
       "- U1 KHÔNG nhận thêm tin nhắn của action「プランA」(tổng vẫn 1 tin)\n"
       "- Giá trị hiển thị ở 友だち詳細 vẫn cập nhật đúng「プランA」",
       note="Spec BR-04 (action_mode=1 chỉ chạy khi chưa từng chạy). Corpus không có TC trực tiếp → AI bổ sung, cần Leader xác nhận."),

    tc("Info kiểu Lựa chọn", "STATE-001", "Normal",
       "Đổi 稼働設定 sang「何度でも稼働」→ bạn đã từng chạy action được chạy lại",
       "- Như TC trên: U1 đã nhận action 1 lần với 稼働設定「一度のみ」",
       "1. Vào màn edit trường, đổi 稼働設定 sang「何度でも稼働」→ lưu\n"
       "2. Ở 友だち詳細 của U1 gán lại「プランA」\n3. Mở LINE app của U1",
       "稼働設定: 一度のみ → 何度でも稼働",
       "- U1 nhận thêm 1 tin nhắn nữa (tổng 2 tin)\n"
       "- Các bạn khác chưa từng có giá trị không bị gửi nhầm",
       note="Spec BR-04 (mode 2 → reset trigger cho toàn bộ giá trị). Corpus không có TC → AI bổ sung, cần Leader xác nhận."),

    tc("Info kiểu Lựa chọn", "FUNC-001", "Normal",
       "Sắp xếp thứ tự option bằng icon lên/xuống → thứ tự hiển thị đúng ở màn 友だち詳細",
       ADM + "\n- Trường 選択肢 có 3 option A, B, C",
       "1. Vào màn edit, dùng icon mũi tên đưa C lên đầu\n2. Lưu\n3. Vào lại màn edit đọc thứ tự\n"
       "4. Mở màn 友だち詳細 của 1 bạn, mở danh sách option của trường này",
       "Thứ tự mong muốn: C, A, B",
       "- Màn edit hiển thị C, A, B\n- Danh sách chọn ở 友だち詳細 cũng theo thứ tự C, A, B\n"
       "- Giá trị bạn bè đã gán không bị đổi theo",
       note="Nguồn: spec ui-spec.md:110 (3 icon) + corpus tab「Change spec info type select」r6 "
            "(sort option không làm đổi dữ liệu option)."),

    tc("Info kiểu Lựa chọn", "DATA-REF-001", "Normal",
       "Xóa 1 option ở màn edit → option biến mất, bạn đang giữ option đó mất giá trị, count cập nhật",
       ADM + "\n- Trường 選択肢 có 3 option A, B, C\n- U1 =「A」, U2 =「B」, 回答人数 = 2人",
       "1. Vào màn edit, xóa option A → lưu\n2. Về màn list đọc 回答人数\n"
       "3. Mở 友だち詳細 của U1 và U2\n4. Click vào 回答人数 xem danh sách bạn",
       "Xóa option A (U1 đang giữ)",
       "- Trường còn 2 option B, C\n"
       "- U1 không còn giá trị ở trường này, U2 vẫn giữ「B」\n"
       "- 回答人数 =「1人」, danh sách câu trả lời chỉ còn U2",
       note="Nguồn: tab「Change spec info type select」r24 (xóa option → xóa bản ghi của user + update count)."),

    tc("Info kiểu Lựa chọn", "DATA-REF-001", "Normal",
       "Xóa option đang được gắn action → action con bị dọn, màn edit không lỗi",
       ADM + "\n- Trường 選択肢 có option A gắn action tag, option B gắn action kịch bản",
       "1. Vào màn edit, xóa option A → lưu\n2. Mở lại màn edit\n"
       "3. Kiểm tra preview action của option B\n4. Mở màn quản lý tag kiểm tra tag còn tồn tại",
       "Xóa option A (có action tag)",
       "- Màn edit mở bình thường, không hiển thị alert lỗi\n"
       "- Option B vẫn giữ đúng action kịch bản\n"
       "- Tag「VIP」vẫn tồn tại ở màn quản lý tag (không bị xóa theo)",
       note="Nguồn: r242, r254, r266 ('Check case xóa option bên trong ⇒ không ảnh hưởng tới tag được gắn')."),

    tc("Info kiểu Lựa chọn", "LIST-001", "Boundary",
       "Trường 選択肢 không có option nào → lưu hay báo lỗi?",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Nhập 管理名, KHÔNG thêm option nào\n2. Click「保存」\n"
       "3. Nếu lưu được: mở 友だち詳細 của 1 bạn xem trường này",
       "0 option",
       "- Ghi nhận hành vi thực tế: lưu được hay báo lỗi bắt buộc ≥ 1 option\n"
       "- Nếu lưu được: màn 友だち詳細 hiển thị trường với danh sách chọn rỗng, không văng lỗi",
       spec="Spec không ghi",
       note="⚠️ Spec và corpus đều không nói — xem MT-10. TC do AI bổ sung, cần Leader chốt expected."),

    tc("Info kiểu Lựa chọn", "PERF-LARGE-001", "Boundary",
       "Trường 選択肢 với số lượng option lớn (50 option) → lưu, hiển thị và gán giá trị đều đúng",
       NEW + "\n- Chọn 情報タイプ =「選択肢」",
       "1. Thêm 50 option với tên khác nhau\n2. Lưu, đo thời gian lưu\n"
       "3. Mở lại màn edit đếm số option\n4. Mở 友だち詳細 của 1 bạn và chọn option thứ 50",
       "50 option:「opt-01」…「opt-50」",
       "- Lưu thành công, không timeout\n- Màn edit hiển thị đủ 50 option đúng thứ tự\n"
       "- Chọn được option thứ 50 cho bạn, giá trị hiển thị đúng ở 友だち詳細 và right bar chat 1:1",
       note="TC do AI bổ sung theo PERF-LARGE-001 — spec không nêu giới hạn số option, cần Leader xác nhận có giới hạn không."),

    # ══════════════════ Info kiểu Mô tả ══════════════════
    tc("Info kiểu Mô tả", "UI-001", "Normal",
       "Kiểu 記述 chỉ có 3 field chung, KHÔNG có khối cấu hình action",
       NEW + "\n- Chọn 情報タイプ =「記述」",
       "1. Quan sát toàn bộ form\n2. Chụp màn hình\n3. Nhập 管理名 và lưu\n4. Mở lại màn edit",
       "管理名 =「メモ」",
       "- Form chỉ có 管理名, フォルダ, 情報タイプ và nút「保存」\n"
       "- KHÔNG có khối option/action/稼働設定\n- Lưu và mở lại edit đều đúng, không có khối action",
       note="Nguồn: spec ui-spec.md §SCR-FRI-03."),

    tc("Info kiểu Mô tả", "DATA-TEXT-001", "Normal",
       "Giá trị kiểu 記述 nhận text dài / xuống dòng / ký tự đặc biệt → lưu và hiển thị đúng 3 nơi",
       "- Có trường「メモ」kiểu 記述\n- Bạn U1 chưa có giá trị",
       "1. Ở 友だち詳細 của U1, nhập giá trị và lưu\n2. Đọc lại giá trị tại 友だち詳細\n"
       "3. Mở right bar chat 1:1 của U1\n4. Mở màn danh sách câu trả lời của trường",
       "Text 3 dòng, có ký tự「&」「<」「>」và emoji, tổng ~300 ký tự",
       "- Cả 3 nơi hiển thị đúng nội dung đã nhập (giữ xuống dòng, không escape sai, không mất emoji)\n"
       "- 回答人数 =「1人」",
       note="RULE-07 (3 tầng hiển thị). TC do AI bổ sung theo DATA-TEXT-001."),

    tc("Info kiểu Mô tả", "FUNC-001", "Normal",
       "Kiểu 記述 không trigger action nào khi gán/đổi giá trị",
       "- Trường「メモ」kiểu 記述\n- Bạn U1 đang mở LINE app",
       "1. Gán giá trị cho U1\n2. Đổi giá trị 2 lần\n3. Xóa giá trị\n"
       "4. Kiểm tra LINE app của U1 sau mỗi thao tác",
       "3 lần thay đổi + 1 lần xóa",
       "- U1 KHÔNG nhận bất kỳ tin nhắn/action nào từ trường này\n"
       "- Giá trị và 回答人数 vẫn cập nhật đúng theo từng thao tác",
       note="Spec ui-spec.md:129 ('không trigger action'). TC do AI bổ sung."),

    # ══════════════════ Info kiểu Ngày tháng — setting ══════════════════
    tc("Info kiểu Ngày tháng — setting", "UI-001", "Normal",
       "Màn tạo kiểu 年月日 hiển thị đủ cấu hình lịch + 2 dòng ghi chú hành vi",
       NEW + "\n- Chọn 情報タイプ =「年月日」",
       "1. Quan sát khối「アクション設定」\n2. Mở dropdown「登録」liệt kê lựa chọn\n"
       "3. Đọc 2 dòng ghi chú hiển thị trên màn\n4. Chụp màn hình",
       "—",
       "- Có dropdown「登録」với 2 lựa chọn「月日」và「年月日」\n"
       "- Có ô nhập số ngày「から {N} 日」, lựa chọn「前」/「後」, ô nhập giờ HH:mm, nút cấu hình action\n"
       "- Hiển thị đủ 2 ghi chú:\n"
       "「登録「月日」を選択した場合、毎年その月日にアクションが稼働します。」\n"
       "「登録「年月日」を選択した場合、1度しかアクションは稼働しません。」",
       note="Evidence: ảnh chụp. Nguồn: spec ui-spec.md:139-149."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Normal",
       "Tạo trường 年月日 kiểu「月日」+ gửi TRƯỚC N ngày → lưu và sinh lịch gửi cho bạn đã có giá trị",
       NEW + "\n- Chọn 情報タイプ =「年月日」\n- Có sẵn 2 bạn U1, U2 sẽ được gán giá trị sau khi lưu",
       "1. Cấu hình「登録」=「月日」, số ngày = 3,「前」, giờ = 09:00, gắn action gửi text\n"
       "2. Lưu\n3. Gán giá trị ngày cho U1 và U2\n"
       "4. Mở màn 友だち詳細 của U1 kiểm tra giá trị đã lưu\n"
       "5. Chờ tới ngày giờ dự kiến và kiểm tra LINE app của U1, U2",
       "U1 = 2026-09-10 · U2 = 2026-09-20 · gửi trước 3 ngày lúc 09:00\n"
       "→ dự kiến U1 nhận 2026-09-07 09:00, U2 nhận 2026-09-17 09:00",
       "- Trường lưu thành công, màn list hiển thị 情報タイプ =「年月日」\n"
       "- U1 nhận action đúng 2026-09-07 09:00, U2 đúng 2026-09-17 09:00 trên LINE app\n"
       "- Không bạn nào nhận sớm/muộn hoặc nhận trùng lặp",
       env="PRODUCTION",
       note="RULE-06 + RULE-08 (job). Nguồn: r3 tab「check setting-action-friend-info-date」."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Normal",
       "Tạo trường 年月日 kiểu「月日」+ gửi SAU N ngày → lịch gửi tính đúng chiều sau",
       NEW + "\n- Chọn 情報タイプ =「年月日」\n- Bạn U1 sẽ được gán giá trị",
       "1. Cấu hình「登録」=「月日」, số ngày = 5,「後」, giờ = 20:00, gắn action gửi text\n"
       "2. Lưu và gán giá trị cho U1\n3. Chờ tới thời điểm dự kiến, kiểm tra LINE app của U1",
       "U1 = 2026-09-10, gửi sau 5 ngày lúc 20:00 → dự kiến 2026-09-15 20:00",
       "- U1 nhận action đúng 2026-09-15 20:00\n- Không nhận vào 2026-09-05 (sai chiều trước/sau)",
       env="PRODUCTION",
       note="Đối chứng Bug Tester #35967 (04/2026 — logic compare before/after bị ngược). Nguồn: r4-r8, r196."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Normal",
       "Kiểu「月日」lặp hàng năm: sau khi gửi xong năm nay, tự sinh lịch cho năm kế tiếp",
       "- Trường 年月日 kiểu「月日」đã setting action\n- Bạn U1 có giá trị và vừa được gửi action năm nay",
       "1. Chờ job gửi action cho U1 xong\n2. Kiểm tra LINE app U1 nhận đúng 1 tin\n"
       "3. Kiểm tra lịch gửi kế tiếp của U1 (màn quản lý/log job)\n"
       "4. Đối chiếu năm của lịch mới",
       "U1 nhận action năm 2026 → lịch mới cho năm 2027",
       "- U1 nhận đúng 1 tin ở năm hiện tại\n"
       "- Sinh đúng 1 lịch mới cho cùng ngày/tháng của năm kế tiếp\n"
       "- KHÔNG tồn tại 2 lịch cùng thời điểm chờ gửi",
       env="PRODUCTION",
       note="Đây là lõi Bug #32287 (10/2025 — gửi duplicate). Nguồn: r3, r86-r88."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Normal",
       "Kiểu「年月日」chỉ chạy 1 lần: sau khi gửi xong KHÔNG sinh lịch năm sau",
       "- Trường 年月日 kiểu「年月日」đã setting action\n- Bạn U1 có giá trị thỏa mãn và đã nhận action",
       "1. Chờ job gửi action cho U1\n2. Kiểm tra LINE app U1\n"
       "3. Kiểm tra còn lịch gửi nào của U1 cho trường này không\n4. Chờ qua mốc cùng ngày năm sau",
       "U1 = 2026-09-10, kiểu 年月日",
       "- U1 nhận đúng 1 tin duy nhất\n- Không còn lịch chờ gửi nào cho U1 ở trường này\n"
       "- Năm sau U1 KHÔNG nhận lại action",
       env="PRODUCTION",
       note="Nguồn: r91, r107 ('action info setting map theo ngày tháng năm ⇒ không insert')."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Kiểu「月日」, giá trị đã qua mốc gửi trong năm nay → lịch nhảy sang năm kế tiếp",
       "- Trường 年月日 kiểu「月日」, gửi trước 1 ngày lúc 09:00\n- Hôm nay là 2026-08-20",
       "1. Gán cho U1 giá trị ngày đã qua trong năm nay\n"
       "2. Kiểm tra lịch gửi của U1\n3. Xác nhận U1 không nhận action ngay",
       "U1 = 2026-03-15 (đã qua) → dự kiến lịch 2027-03-14 09:00",
       "- Sinh lịch cho 2027-03-14 09:00 (năm kế tiếp)\n- U1 không nhận action ngay tại thời điểm gán",
       env="PRODUCTION",
       note="Nguồn: r90, r106 + spec BR-08 (addYear)."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Kiểu「年月日」, giá trị đã qua mốc gửi → KHÔNG sinh lịch, không gửi",
       "- Trường 年月日 kiểu「年月日」, gửi sau 1 ngày\n- Hôm nay là 2026-08-20",
       "1. Gán cho U1 giá trị quá khứ\n2. Kiểm tra lịch gửi\n3. Chờ 24h và kiểm tra LINE app U1",
       "U1 = 2023-04-18 (quá khứ > 1 năm)",
       "- Không sinh lịch gửi nào cho U1\n- U1 không nhận action nào",
       env="PRODUCTION",
       note="Nguồn: r91, r216, r259 (khối #34675)."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Số ngày offset = 0 → gửi đúng ngày giá trị, tại giờ đã cấu hình",
       "- Trường 年月日 kiểu「月日」, số ngày = 0, giờ 10:00, có action",
       "1. Gán cho U1 giá trị là ngày mai\n2. Chờ tới 10:00 ngày mai\n3. Kiểm tra LINE app U1",
       "U1 = ngày mai, offset 0 ngày, giờ 10:00",
       "- U1 nhận action đúng ngày giá trị lúc 10:00, không lệch ngày",
       env="PRODUCTION",
       note="Nguồn: r199-r203 (case 'send sau 0 ngày'). Spec field #11 ghi 'Integer ≥ 0'."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Giờ gửi đã qua trong ngày hôm nay → lịch dời sang mốc hợp lệ kế tiếp, không gửi ngay",
       "- Trường 年月日 kiểu「月日」có action\n- Hiện tại 15:00, cấu hình giờ gửi 09:00",
       "1. Gán cho U1 giá trị sao cho mốc gửi rơi đúng hôm nay 09:00 (đã qua)\n"
       "2. Kiểm tra lịch gửi của U1\n3. Theo dõi LINE app U1 trong 30 phút",
       "Mốc tính ra = hôm nay 09:00, thời điểm thao tác 15:00",
       "- U1 KHÔNG nhận action ngay\n- Lịch dời sang cùng mốc của năm kế tiếp (kiểu 月日)",
       env="PRODUCTION",
       note="Nguồn: r361-r362, r365-r366 ('giờ thỏa mãn (> time now)' vs 'giờ k thỏa mãn (< time now)')."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Giá trị ngày 29/02 năm nhuận → mốc gửi tính đúng, không lỗi ngày không tồn tại",
       "- Trường 年月日 kiểu「年月日」, gửi sau 800 ngày\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2024-02-29\n2. Kiểm tra mốc gửi dự kiến\n3. Chờ tới mốc và kiểm tra LINE app U1",
       "U1 = 2024-02-29, gửi sau 800 ngày → dự kiến 2026-05-09",
       "- Mốc gửi = 2026-05-09 (đúng phép cộng 800 ngày từ 2024-02-29)\n"
       "- U1 nhận action đúng ngày đó, không lỗi ngày không hợp lệ",
       env="PRODUCTION",
       note="Nguồn: r209-r210 (#34675, case năm nhuận)."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-DATE-001", "Boundary",
       "Mốc gửi rơi vào 29/02 của năm nhuận tương lai → tính đúng ngày",
       "- Trường 年月日 kiểu「年月日」\n- Hôm nay 2026-04-18",
       "1. Gán U1 = 2026-04-30, cấu hình gửi sau 670 ngày → kiểm tra mốc\n"
       "2. Đổi cấu hình gửi sau 671 ngày → kiểm tra lại mốc",
       "670 ngày → dự kiến 2028-02-29 · 671 ngày → dự kiến 2028-03-01",
       "- Mốc gửi lần lượt là 2028-02-29 và 2028-03-01\n- Không bị nhảy sai 1 ngày quanh 29/02",
       env="PRODUCTION",
       note="Nguồn: r212 (#34675)."),

    tc("Info kiểu Ngày tháng — setting", "UI-INPUT-001", "Abnormal",
       "Số ngày offset nhập chữ / số âm / bỏ trống → bị chặn hoặc báo lỗi",
       NEW + "\n- Chọn 情報タイプ =「年月日」",
       "1. Nhập ô số ngày lần lượt các giá trị không hợp lệ\n2. Mỗi lần bấm「保存」\n"
       "3. Ghi lại hành vi thực tế của từng giá trị",
       "「abc」·「-5」·「1.5」· bỏ trống · số Nhật「１０」",
       "- Không lưu được cấu hình với các giá trị không hợp lệ (chặn nhập hoặc báo lỗi)\n"
       "- Số Nhật full-width được tự chuyển sang số latinh (nếu chấp nhận)",
       spec="Spec không ghi",
       note="⚠️ Spec chỉ ghi 'Integer ≥ 0', không nêu message. Cơ chế số Nhật suy từ hành vi ô random point "
            "(ModalAction r7/r79) — cần Leader xác nhận, xem MT-10."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-MULTI-001", "Normal",
       "1 trường 年月日 có nhiều dòng cấu hình action → mỗi dòng sinh lịch riêng, gửi đủ",
       NEW + "\n- Chọn 情報タイプ =「年月日」",
       "1. Thêm 2 dòng cấu hình: (a) trước 3 ngày 09:00 gửi text A, (b) sau 1 ngày 20:00 gửi text B\n"
       "2. Lưu và gán giá trị cho U1\n3. Chờ qua cả 2 mốc, kiểm tra LINE app U1",
       "U1 = 2026-09-10 → dự kiến nhận A ngày 09-07 09:00 và B ngày 09-11 20:00",
       "- U1 nhận đủ 2 tin đúng 2 mốc, đúng nội dung tương ứng\n- Không tin nào bị thiếu hoặc trùng",
       env="PRODUCTION",
       note="TC do AI bổ sung theo FUNC-MULTI-001 (spec BR-03 cho phép mảng setting_actions), cần Leader xác nhận."),

    tc("Info kiểu Ngày tháng — setting", "FUNC-001", "Normal",
       "Trường 年月日 KHÔNG gắn action → lưu được, không sinh lịch, chỉ lưu giá trị",
       NEW + "\n- Chọn 情報タイプ =「年月日」",
       "1. Nhập 管理名, không cấu hình action nào → lưu\n2. Gán giá trị ngày cho U1\n"
       "3. Kiểm tra 友だち詳細 của U1\n4. Chờ qua ngày giá trị, kiểm tra LINE app U1",
       "U1 = ngày mai, không có action",
       "- Lưu thành công\n- Giá trị hiển thị đúng ở 友だち詳細 và right bar chat 1:1, 回答人数 = 1人\n"
       "- U1 không nhận action nào",
       note="TC do AI bổ sung theo FUNC-001, cần Leader xác nhận."),

    # ══════════════════ Info kiểu Điểm ══════════════════
    tc("Info kiểu Điểm", "UI-001", "Normal",
       "Màn tạo kiểu ポイント hiển thị khối「ポイント到達時アクション」",
       NEW + "\n- Chọn 情報タイプ =「ポイント」",
       "1. Quan sát khối cấu hình riêng của kiểu điểm\n2. Bấm nút thêm dòng ngưỡng\n3. Chụp màn hình",
       "—",
       "- Hiển thị khối「ポイント到達時アクション」\n"
       "- Có radio「稼働設定」(一度のみ / 何度でも稼働)\n"
       "- Mỗi dòng có ô nhập ngưỡng điểm + nút cấu hình action",
       note="Evidence: ảnh chụp. Spec Gap #4 ghi 'giao diện chi tiết khi click 追加 chưa được chụp' → TC này lấp Gap. "
            "Nguồn: spec ui-spec.md:168."),

    tc("Info kiểu Điểm", "FUNC-001", "Normal",
       "Bạn đạt ĐÚNG ngưỡng điểm → action tương ứng chạy",
       "- Trường ポイント「会員ポイント」, ngưỡng 100 điểm gắn action gửi text\n- U1 đang có 0 điểm",
       "1. Cộng điểm cho U1 lên đúng 100\n2. Kiểm tra LINE app U1\n"
       "3. Kiểm tra giá trị điểm hiển thị ở 友だち詳細",
       "U1: 0 → 100 điểm (ngưỡng = 100)",
       "- U1 nhận đúng tin nhắn của action ngưỡng 100\n"
       "- 友だち詳細 và right bar chat 1:1 hiển thị 100 điểm\n- 回答人数 tăng 1",
       note="Nguồn: r31 ('khi user được gán số point = số point setting thì có action được bình thường'). RULE-06."),

    tc("Info kiểu Điểm", "FUNC-001", "Boundary",
       "Điểm dưới ngưỡng / vượt ngưỡng → hành vi action khác nhau",
       "- Trường ポイント, ngưỡng 100 điểm có action\n- U1, U2, U3 đều 0 điểm",
       "1. Đặt U1 = 99 điểm → kiểm tra LINE app U1\n2. Đặt U2 = 100 điểm → kiểm tra LINE app U2\n"
       "3. Đặt U3 = 150 điểm → kiểm tra LINE app U3",
       "99 / 100 / 150 điểm, ngưỡng 100",
       "- U1 (99) KHÔNG nhận action\n- U2 (100) nhận action\n"
       "- U3 (150): ghi nhận hành vi thực tế có nhận action hay không",
       spec="Spec không ghi",
       note="⚠️ Spec chỉ ghi 'khi tổng điểm đạt ngưỡng → trigger', không nói vượt ngưỡng có tính không — xem MT-11. "
            "AI bổ sung TC cận biên."),

    tc("Info kiểu Điểm", "FUNC-UNIQ-001", "Abnormal",
       "Nhập 2 ngưỡng điểm TRÙNG NHAU → báo lỗi trùng, không lưu",
       NEW + "\n- Chọn 情報タイプ =「ポイント」",
       "1. Thêm 2 dòng ngưỡng cùng giá trị\n2. Click「保存」\n3. Lặp lại với giá trị chữ",
       "Lần 1: ngưỡng「A」và「A」\nLần 2: ngưỡng「1」và「1」",
       "- Hiển thị message lỗi:\n" + DUP_MSG + "\n- Trường không được lưu",
       note="⚠️ Message nói「選択肢の表示名」nhưng áp cho kiểu ポイント (ngưỡng điểm) — dùng chung message, xem MT-05. "
            "Nguồn: r150-r151 (#33697)."),

    tc("Info kiểu Điểm", "FUNC-UNIQ-001", "Boundary",
       "2 ngưỡng điểm chỉ khác dấu cách đầu/cuối → vẫn báo trùng",
       NEW + "\n- Chọn 情報タイプ =「ポイント」",
       "1. Nhập ngưỡng 1 =「100」, ngưỡng 2 =「 100 」\n2. Click「保存」",
       "「100」vs「 100 」",
       "- Hiển thị message lỗi:\n" + DUP_MSG + "\n- Trường không được lưu",
       note="Nguồn: r152 (#33697)."),

    tc("Info kiểu Điểm", "FUNC-001", "Normal",
       "Sau khi báo lỗi trùng ngưỡng → sửa hợp lệ → lưu được và gán được điểm cho bạn",
       NEW + "\n- Vừa bị báo lỗi trùng ngưỡng",
       "1. Sửa ngưỡng 2 thành giá trị khác → lưu\n2. Gán điểm cho U1 đạt ngưỡng 2\n"
       "3. Kiểm tra LINE app U1 và giá trị ở 友だち詳細",
       "Ngưỡng: 100 và 200 · U1 = 200 điểm",
       "- Lưu thành công\n- U1 nhận action của ngưỡng 200\n- 友だち詳細 hiển thị 200 điểm",
       note="Nguồn: r153-r155 (#33697)."),

    tc("Info kiểu Điểm", "FUNC-UNIQ-001", "Normal",
       "2 trường ポイント khác nhau trong cùng folder được phép trùng ngưỡng",
       ADM + "\n- Folder F đã có trường Point-1 ngưỡng「A」",
       "1. Tạo Point-2 kiểu ポイント trong folder F với ngưỡng「A」\n2. Lưu\n"
       "3. Gán điểm cho U1 ở Point-2\n4. Kiểm tra giá trị của U1 ở cả 2 trường",
       "Point-1 ngưỡng「A」· Point-2 ngưỡng「A」",
       "- Point-2 lưu thành công, không báo lỗi trùng\n"
       "- U1 chỉ ghi nhận điểm ở Point-2, Point-1 vẫn trống",
       note="Nguồn: r154 (#33697)."),

    tc("Info kiểu Điểm", "UI-INPUT-001", "Abnormal",
       "Ô random điểm (from~to): bỏ trống / from > to / nhập chữ → bị chặn hoặc báo lỗi",
       "- Mở dialog action, chọn action friend info kiểu ポイント, chọn「ランダム」",
       "1. Bỏ trống from và to → lưu\n2. Nhập from = 10, to = 5 → lưu\n"
       "3. Nhập chữ vào from → quan sát\n4. Nhập số Nhật full-width「１０」→ quan sát",
       "rỗng · 10~5 · 「abc」·「１０」",
       "- Bỏ trống: báo lỗi bắt buộc nhập\n- from > to: không lưu được\n"
       "- Nhập chữ: bị chặn không nhập được\n- Số Nhật tự chuyển thành số latinh 10",
       note="Nguồn: ModalAction /「Thêm option random...」r4-r7, r76-r79 (11/2023). "
            "⚠️ TC gốc ~2.8 năm — CẦN VERIFY LẠI."),

    tc("Info kiểu Điểm", "UI-INPUT-001", "Boundary",
       "Random điểm: from = to → luôn lấy đúng số đó; from < to → giá trị nằm trong khoảng",
       "- Trường ポイント + action ghi đè điểm kiểu ランダム",
       "1. Cấu hình from = to = 7, action cho 5 bạn khác nhau → đọc điểm từng bạn\n"
       "2. Đổi từ 3~6, action cho 5 bạn khác → đọc điểm từng bạn",
       "from=to=7 (5 lần) · from=3, to=6 (5 lần)",
       "- Trường hợp from=to: cả 5 bạn đều nhận đúng 7 điểm\n"
       "- Trường hợp 3~6: điểm của mỗi bạn nằm trong 3..6",
       note="Nguồn: ModalAction r10-r11, r82-r83. CẦN VERIFY LẠI (TC gốc 11/2023)."),

    tc("Info kiểu Điểm", "DATA-001", "Boundary",
       "Random điểm với khoảng thập phân → giá trị nhận được nằm trong khoảng thập phân đó",
       "- Trường ポイント + action ghi đè điểm kiểu ランダム",
       "1. Cấu hình from = 1.5, to = 2.5\n2. Thực hiện action cho 5 bạn\n"
       "3. Đọc giá trị điểm của từng bạn ở 友だち詳細",
       "from = 1.5, to = 2.5, 5 bạn",
       "- Giá trị điểm của mỗi bạn nằm trong khoảng 1.5..2.5\n- Hiển thị đúng phần thập phân, không bị làm tròn ngầm",
       spec="Spec không ghi",
       note="⚠️ Spec BR-03 ghi ngưỡng điểm là Integer nhưng corpus cho phép random thập phân — xem MT-11. "
            "Nguồn: ModalAction r8, r80."),

    tc("Info kiểu Điểm", "DATA-001", "Normal",
       "Random điểm cho NHIỀU bạn cùng lúc → mỗi bạn 1 giá trị random riêng",
       "- Trường ポイント + action ghi đè điểm ランダム 3~6\n- Màn danh sách bạn bè có ≥ 10 bạn",
       "1. Ở màn danh sách bạn bè, chọn 10 bạn\n2. Thực hiện action ghi đè điểm ランダム 3~6\n"
       "3. Mở màn danh sách câu trả lời của trường và đọc giá trị 10 bạn",
       "10 bạn, khoảng 3~6",
       "- Mỗi bạn có giá trị riêng nằm trong 3..6\n"
       "- KHÔNG phải cả 10 bạn cùng 1 giá trị\n- 回答人数 = 10人",
       note="Nguồn: ModalAction r24, r94 ('mỗi user random 1 point'). CẦN VERIFY LẠI (11/2023)."),

    tc("Info kiểu Điểm", "DATA-001", "Normal",
       "Cùng 1 cấu hình random chạy nhiều lần cho 1 bạn → mỗi lần ra giá trị khác nhau (không cố định)",
       "- Trường ポイント + action ghi đè điểm ランダム 3~6, 稼働設定「何度でも稼働」\n- Bạn U1",
       "1. Thực hiện action cho U1 lần 1 → ghi giá trị\n2. Lặp lại 5 lần\n"
       "3. So sánh 6 giá trị thu được",
       "6 lần action, khoảng 3~6",
       "- Tất cả giá trị nằm trong 3..6\n"
       "- Các giá trị KHÔNG giống hệt nhau cả 6 lần (thực sự random, không cache 1 giá trị)",
       note="Nguồn: ModalAction r12, r84."),

    tc("Info kiểu Điểm", "OUT-PREVIEW-001", "Normal",
       "Preview action điểm: ghi đè chỉ định / ghi đè ngẫu nhiên hiển thị đúng text",
       "- Trường ポイント「会員ポイント」\n- Đang ở màn tạo/sửa 1 trường friend info khác, mở dialog action",
       "1. Chọn action friend info → trường「会員ポイント」→「ポイント上書き」kiểu chỉ định 50\n"
       "2. Lưu action, đọc text preview\n3. Đổi sang kiểu ngẫu nhiên 2~5, lưu, đọc lại preview",
       "Chỉ định 50 · Ngẫu nhiên 2~5",
       "- Chỉ định hiển thị:「【友だち情報】会員ポイント(登録) 50 ポイント」\n"
       "- Ngẫu nhiên hiển thị:「【友だち情報】会員ポイント(登録) ランダム 2 ~ 5」",
       note="Bug KH #38469 (07/2026). Nguồn: r276-r277, r501-r502."),

    tc("Info kiểu Điểm", "OUT-PREVIEW-001", "Normal",
       "Preview action điểm: cộng điểm / trừ điểm hiển thị đúng ký hiệu プラス / マイナス",
       "- Trường ポイント「会員ポイント」, đang mở dialog action",
       "1. Chọn cộng điểm chỉ định 10 → lưu → đọc preview\n2. Cộng điểm ngẫu nhiên 3~6 → đọc preview\n"
       "3. Trừ điểm chỉ định 20 → đọc preview\n4. Trừ điểm ngẫu nhiên 6~8 → đọc preview",
       "+10 · +ランダム3~6 · -20 · -ランダム6~8",
       "- Lần lượt hiển thị:\n"
       "「【友だち情報】会員ポイント（プラス） 10」\n"
       "「【友だち情報】会員ポイント（プラス）ランダム 3 ~ 6」\n"
       "「【友だち情報】会員ポイント（マイナス）20」\n"
       "「【友だち情報】会員ポイント（マイナス）ランダム 6 ~ 8」",
       note="Support #38536 (07/2026 — thống nhất text 2 loại cộng/trừ). Nguồn: r278-r281, r503-r504."),

    tc("Info kiểu Điểm", "OUT-PREVIEW-001", "Normal",
       "Preview action「登録情報を削除」(xóa thông tin đăng ký) hiển thị đúng và KHÁC với ghi đè điểm",
       "- Trường ポイント「会員ポイント」, đang mở dialog action",
       "1. Chọn action「登録情報を削除」→ lưu → đọc preview\n"
       "2. Đổi sang「ポイント上書き」chỉ định → lưu → đọc preview\n3. Đổi ngược lại → đọc preview",
       "登録情報を削除 ⇄ ポイント上書き",
       "- 「登録情報を削除」hiển thị đúng:「【友だち情報】登録情報を削除」\n"
       "- 「ポイント上書き」hiển thị:「【友だち情報】会員ポイント(登録) <N> ポイント」\n"
       "- 2 text KHÔNG bị hiển thị lẫn lộn khi đổi qua lại",
       note="Đây chính là hiện tượng Bug KH #38469 (màn tạo hiện 登録情報を削除 cho action ghi đè điểm). "
            "Nguồn: r282, r285-r286."),

    tc("Info kiểu Điểm", "OUT-PREVIEW-001", "Normal",
       "Đổi qua lại giữa các loại action điểm NGAY TRONG màn tạo → preview cập nhật đúng theo lựa chọn cuối",
       "- Đang ở màn tạo 1 trường friend info kiểu 年月日, mở dialog action friend info kiểu ポイント",
       "1. Chọn ghi đè chỉ định → đổi sang cộng điểm → đọc preview\n"
       "2. Cộng điểm ngẫu nhiên → đổi sang trừ điểm ngẫu nhiên → đọc preview\n"
       "3. Trừ điểm → đổi sang 登録情報を削除 → đọc preview\n"
       "4. 登録情報を削除 → đổi sang ghi đè ngẫu nhiên → đọc preview",
       "4 chuỗi đổi loại action liên tiếp",
       "- Sau mỗi lần đổi, preview hiển thị đúng loại action ĐANG chọn\n"
       "- Không giữ lại text của loại action trước đó",
       note="Chuỗi thao tác liên tiếp nên giữ 1 TC. Nguồn: r283-r286 (#38469)."),

    tc("Info kiểu Điểm", "REG-SHARED-001", "Normal",
       "Preview action điểm hiển thị đúng ở mọi màn có dialog action (auto-reply, conversion, richmenu, QR, form, booking event)",
       "- Trường ポイント「会員ポイント」\n- Đã có sẵn 1 auto-reply, 1 conversion, 1 richmenu, 1 QR code, 1 form, 1 booking event",
       "1. Ở từng màn, mở dialog action → chọn action friend info ポイント ghi đè chỉ định → lưu\n"
       "2. Đọc text preview tại từng màn\n3. Lặp với ghi đè ngẫu nhiên",
       "6 màn × 2 kiểu (chỉ định / ngẫu nhiên)",
       "- Cả 6 màn hiển thị đúng format:「【友だち情報】会員ポイント(登録) <N> ポイント」và「... ランダム <from> ~ <to>」\n"
       "- Không màn nào bị đổi design hay thiếu text",
       note="6 điểm cùng 1 kết quả nên gộp 1 TC (liệt kê đủ ở Dữ liệu test). Nguồn: r516-r573 (Support #38536)."),

    tc("Info kiểu Điểm", "REG-RUN-001", "Normal",
       "Sau khi sửa text preview, action điểm vẫn CHẠY đúng cho bạn bè (ghi đè / cộng / trừ / xóa)",
       "- Trường ポイント「会員ポイント」, U1 đang có 50 điểm",
       "1. Chạy action ghi đè 100 cho U1 → đọc điểm\n2. Chạy action cộng 20 → đọc điểm\n"
       "3. Chạy action trừ 30 → đọc điểm\n4. Chạy action xóa điểm → đọc điểm",
       "U1: 50 → ghi đè 100 → +20 → -30 → xóa",
       "- Sau bước 1: 100 điểm\n- Sau bước 2: 120 điểm\n- Sau bước 3: 90 điểm\n"
       "- Sau bước 4: không còn giá trị điểm, 回答人数 giảm 1\n"
       "- Giá trị khớp giữa 友だち詳細, right bar chat 1:1 và màn danh sách câu trả lời",
       note="RULE-07. Nguồn: r306-r309 (#38469 — verify action không bị ảnh hưởng sau khi fix preview)."),

    # ══════════════════ Info kiểu Ảnh & PDF ══════════════════
    tc("Info kiểu Ảnh & PDF", "MEDIA-001", "Normal",
       "Tạo trường kiểu 画像 trong folder tự tạo → lưu thành công",
       NEW + "\n- Đang đứng ở folder tự tạo「予約情報」",
       "1. Nhập 管理名, chọn 情報タイプ =「画像」\n2. Lưu\n"
       "3. Quan sát màn list: trường có xuất hiện trong folder「予約情報」không\n"
       "4. Ghi lại kết quả thực tế",
       "情報タイプ =「画像」, folder tự tạo",
       "- Lưu thành công, không báo lỗi\n"
       "- ⚠️ Ghi nhận thực tế: trường có hiển thị trong danh sách của folder hay KHÔNG",
       spec="Đã hỏi leader",
       note="⚠️ MÂU THUẪN MT-01: corpus r201, r326 expect 'tạo thành công + đứng tại folder vừa tạo'; "
            "spec logic-spec.md:62 nói type 4/5 bị loại khỏi query danh sách theo folder. Nguồn: r201, r326, r341."),

    tc("Info kiểu Ảnh & PDF", "MEDIA-001", "Normal",
       "Tạo trường kiểu PDF trong folder tự tạo → lưu thành công",
       NEW + "\n- Đang đứng ở folder tự tạo「予約情報」",
       "1. Nhập 管理名, chọn 情報タイプ =「PDF」\n2. Lưu\n"
       "3. Quan sát màn list và ghi lại kết quả thực tế",
       "情報タイプ =「PDF」, folder tự tạo",
       "- Lưu thành công, không báo lỗi\n- ⚠️ Ghi nhận thực tế trường có hiển thị trong folder hay không",
       spec="Đã hỏi leader",
       note="⚠️ MT-01 (như TC trên). Nguồn: r202, r327, r342."),

    tc("Info kiểu Ảnh & PDF", "MEDIA-001", "Normal",
       "Gán giá trị ảnh cho bạn → hiển thị đúng ở 友だち詳細, right bar chat 1:1 và mở xem được ảnh",
       "- Có trường kiểu 画像\n- Bạn U1 chưa có giá trị",
       "1. Ở 友だち詳細 của U1 upload 1 ảnh JPG\n2. Lưu\n3. Đọc lại giá trị tại 友だち詳細\n"
       "4. Mở right bar chat 1:1 của U1\n5. Click mở ảnh ở kích thước đầy đủ",
       "Ảnh JPG ~1MB",
       "- Ảnh hiển thị ở cả 友だち詳細 và right bar chat 1:1\n"
       "- Click mở được ảnh đầy đủ, không lỗi 404/không tải được\n- 回答人数 tăng 1",
       env="PRODUCTION",
       note="RULE-08 (media → PRODUCTION). Nguồn: r201, r326 (corpus chỉ ghi 'gán/tạo value cho friend info thành công') "
            "→ expected chi tiết do AI viết."),

    tc("Info kiểu Ảnh & PDF", "MEDIA-001", "Normal",
       "Gán giá trị PDF cho bạn → tải/mở được file đúng nội dung",
       "- Có trường kiểu PDF\n- Bạn U1 chưa có giá trị",
       "1. Ở 友だち詳細 của U1 upload 1 file PDF\n2. Lưu và đọc lại giá trị\n"
       "3. Mở right bar chat 1:1 của U1\n4. Tải file về và mở kiểm tra nội dung",
       "File PDF 3 trang, ~2MB",
       "- Tên file hiển thị đúng ở 友だち詳細 và right bar chat 1:1\n"
       "- File tải về mở được, đủ 3 trang, đúng nội dung đã upload\n- 回答人数 tăng 1",
       env="PRODUCTION",
       note="RULE-06 (đi tới file tải về) + RULE-08. Nguồn: r202, r327."),

    tc("Info kiểu Ảnh & PDF", "MEDIA-001", "Abnormal",
       "Upload sai định dạng cho trường 画像 / PDF → bị chặn, không lưu giá trị",
       "- Có 1 trường kiểu 画像 và 1 trường kiểu PDF\n- Bạn U1",
       "1. Ở trường 画像 thử upload file .pdf và file .exe\n"
       "2. Ở trường PDF thử upload file .jpg\n3. Sau mỗi lần ghi lại thông báo và 回答人数",
       "画像 ← .pdf, .exe · PDF ← .jpg",
       "- Cả 3 lần đều bị chặn, hiển thị thông báo sai định dạng\n"
       "- Không lưu giá trị nào, 回答人数 không tăng",
       spec="Spec không ghi",
       note="TC do AI bổ sung theo MEDIA-001 — spec không nêu ràng buộc định dạng/dung lượng cho 2 kiểu này (Gap #1). "
            "Cần Leader xác nhận danh sách định dạng hợp lệ."),

    tc("Info kiểu Ảnh & PDF", "MEDIA-CLEAN-001", "Normal",
       "Xóa trường 画像 / PDF → file media không còn truy cập được qua màn hình",
       "- Trường kiểu 画像 có 2 bạn đã upload ảnh\n- Trường kiểu PDF có 2 bạn đã upload file",
       "1. Ghi lại 回答人数 của 2 trường\n2. Xóa cả 2 trường ở màn list\n"
       "3. Mở 友だち詳細 của 4 bạn liên quan\n4. Mở right bar chat 1:1 của họ",
       "2 trường × 2 bạn",
       "- 2 trường biến mất khỏi màn list\n"
       "- 友だち詳細 và right bar không còn hiển thị ảnh/PDF của 2 trường đó\n"
       "- Không màn nào văng lỗi khi mở",
       env="PRODUCTION",
       note="TC do AI bổ sung theo MEDIA-CLEAN-001 (spec BR-06 không nói rõ có xóa file vật lý không) — cần Leader xác nhận."),
]
