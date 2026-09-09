# -*- coding: utf-8 -*-
"""FA-015 Quản lý thông tin bạn bè — Nhóm 1: Màn list · Folder · Sắp xếp & chuyển folder.

Nguồn chính:
- 10.2 TCsLine_friend_information / tab「test fix bug」(master, 08/2024 → 07/2026)
  khối Bug KH #36201 (05/2026 — cookie folder) r196-r228.
- TCsLine_Improve chung / tab「Test bug folder all màn」(Bug Tester #27083, 04/2026) r106-r122.
- TCsLine_Improve chung / tab「recover bảng category」(20/06/2025) r5-r18 (kind=12).
"""
from _common import tc

ADM = "- Đăng nhập admin bot A (plan có phí), mở /basic/friend-information"
F3 = ("- Bot A có 3 folder tự tạo:「予約情報」/「アンケート」/「Campaign-01」và folder mặc định"
      "「未分類」\n- Mỗi folder có ≥ 2 trường thông tin")

S1 = [
    # ══════════════════ Màn list thông tin ══════════════════
    tc("Màn list thông tin", "UI-001", "Normal",
       "Load /basic/friend-information: panel trái = cây folder, panel phải = bảng 4 cột",
       ADM + "\n" + F3,
       "1. Mở /basic/friend-information\n"
       "2. Đối chiếu tiêu đề trang, panel trái, panel phải\n"
       "3. Chụp màn hình toàn trang",
       "—",
       "- Tiêu đề trang hiển thị「友だち情報管理」\n"
       "- Panel trái: danh sách folder + số lượng item của từng folder; luôn có「未分類」ở đầu\n"
       "- Panel phải: bảng đúng 4 cột theo thứ tự「作成日」「管理名」「情報タイプ」「回答人数」\n"
       "- Có nút tạo folder (+) và nút「新規作成」",
       note="Evidence: ảnh chụp toàn màn hình. Nguồn: spec ui-spec.md §SCR-FRI-01 + corpus r197."),

    tc("Màn list thông tin", "UI-002", "Normal",
       "Cột「作成日」hiển thị đúng định dạng YYYY.MM.DD",
       ADM + "\n- Có ≥ 1 trường thông tin tạo ngày 2026-02-10",
       "1. Mở màn list\n2. Đọc giá trị cột「作成日」của trường đó",
       "Trường「chọn 1」tạo ngày 2026-02-10",
       "- Hiển thị đúng chuỗi「2026.02.10」(dấu chấm, không phải gạch ngang)",
       note="Evidence: ảnh chụp. Nguồn: spec ui-spec.md:79 (bảng mẫu)."),

    tc("Màn list thông tin", "UI-003", "Normal",
       "Cột「情報タイプ」hiển thị đúng nhãn JP cho từng kiểu đã tạo",
       ADM + "\n- Bot A có sẵn 1 trường mỗi kiểu: 選択肢 / 記述 / 年月日 / ポイント",
       "1. Mở màn list\n2. Đọc cột「情報タイプ」của 4 trường",
       "4 trường: type_select / type_kijutsu / type_date / type_point",
       "- 4 dòng hiển thị lần lượt「選択肢」「記述」「年月日」「ポイント」\n"
       "- Không hiển thị số enum (1/2/3/6) ra UI",
       note="Kiểu 画像/PDF tách riêng nhóm「Info kiểu Ảnh & PDF」vì có mâu thuẫn MT-01. Nguồn: r197."),

    tc("Màn list thông tin", "DATA-COUNT-001", "Normal",
       "Cột「回答人数」hiển thị đúng số bạn có giá trị, có hậu tố「人」và click được",
       ADM + "\n- Trường「Point 1」đang có đúng 2 bạn có giá trị",
       "1. Mở màn list\n2. Đọc cột「回答人数」của trường「Point 1」\n"
       "3. Click vào con số đó",
       "2 bạn: LINE user U1, U2 đã có giá trị",
       "- Hiển thị「2人」\n"
       "- Click điều hướng sang màn danh sách câu trả lời /basic/friend-information/item/{id}\n"
       "- Màn đó liệt kê đúng 2 bạn U1, U2",
       note="RULE-07: khớp màn list + màn detail count. Nguồn: r115, spec ui-spec.md:67."),

    tc("Màn list thông tin", "LIST-001", "Boundary",
       "Folder rỗng (không có trường thông tin nào) → panel phải hiển thị trạng thái rỗng, không lỗi",
       ADM + "\n- Tạo mới folder「Empty-01」chưa có trường nào",
       "1. Click folder「Empty-01」ở panel trái\n2. Quan sát panel phải\n3. Mở DevTools tab Console",
       "Folder「Empty-01」: 0 item",
       "- Panel phải hiển thị bảng rỗng (chỉ có header), KHÔNG hiển thị dòng dữ liệu cũ của folder trước\n"
       "- Panel trái hiển thị số lượng của folder =「0」\n"
       "- Console không có lỗi JS",
       note="Empty state — corpus không có TC; TC do AI bổ sung theo LIST-001, cần Leader xác nhận."),

    tc("Màn list thông tin", "FUNC-001", "Normal",
       "Click qua lại liên tục giữa các folder → panel phải luôn hiển thị đúng item của folder cuối cùng",
       ADM + "\n" + F3,
       "1. Click folder「予約情報」\n2. Click「アンケート」\n3. Click「Campaign-01」\n"
       "4. Click「未分類」\n5. Lặp lại chuỗi trên 3 lần liên tiếp, không chờ load xong\n"
       "6. Dừng ở「Campaign-01」và đối chiếu danh sách item",
       "4 folder, mỗi folder ≥ 2 item khác nhau rõ rệt",
       "- Panel phải hiển thị đúng item của「Campaign-01」(folder click cuối cùng)\n"
       "- Không bị hiển thị chồng/lẫn item của folder khác\n"
       "- Folder đang chọn được highlight đúng「Campaign-01」",
       note="Nguồn: r211, r222 (khối #36201)."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder: sau khi TẠO trường thông tin trong folder tự tạo → quay về list vẫn đứng tại folder đó",
       ADM + "\n- Có folder tự tạo「予約情報」",
       "1. Click folder「予約情報」\n2. Click「新規作成」\n3. Nhập 管理名, giữ nguyên folder =「予約情報」\n"
       "4. Click「保存」\n5. Quan sát folder đang được chọn ở màn list",
       "Lần lượt tạo với 情報タイプ: 選択肢 → 記述 → 年月日 → ポイント (4 lần, mỗi lần 1 trường mới)",
       "- Tạo trường thành công\n"
       "- Sau khi lưu, màn list mở đúng vào folder「予約情報」(KHÔNG bị reset về「未分類」)\n"
       "- Trường vừa tạo hiển thị trong folder đó",
       note="Bug KH #36201 (05/2026). 4 kiểu cùng 1 kết quả nên gộp 1 TC. Nguồn: r198-r203."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder: tạo trường sau khi RELOAD trang / sau khi SORT folder / sau khi SORT item → vẫn đứng đúng folder",
       ADM + "\n- Có folder tự tạo「予約情報」",
       "1. Tạo folder mới\n2. Thực hiện lần lượt 3 kịch bản:\n"
       "   (a) F5 reload màn list rồi tạo trường trong folder mới\n"
       "   (b) Sort folder rồi tạo trường trong folder mới\n"
       "   (c) Sort folder → sort item → tạo trường trong folder mới\n"
       "3. Mỗi kịch bản lặp 3 lần tạo liên tiếp",
       "3 kịch bản × 3 lần tạo = 9 lượt",
       "- Cả 9 lượt: tạo thành công và màn list đứng đúng tại folder vừa chọn\n"
       "- Không lượt nào bị nhảy về「未分類」",
       note="Nguồn: r204-r210 (#36201)."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder: sau khi XÓA trường thông tin → vẫn đứng tại folder đang xem",
       ADM + "\n- Folder「予約情報」có ≥ 2 trường",
       "1. Click folder「予約情報」\n2. Xóa 1 trường\n3. Quan sát folder đang chọn\n"
       "4. Tạo tiếp 1 trường mới\n5. Quan sát lại folder đang chọn",
       "Trường bị xóa: 「予約プラン」",
       "- Xóa thành công, màn list vẫn đứng tại「予約情報」\n"
       "- Sau khi tạo mới, vẫn đứng tại「予約情報」",
       note="Nguồn: r212-r213 (#36201)."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder: ở màn tạo/sửa ĐỔI folder đích → về list mở đúng folder ĐÃ CHỌN Ở FORM",
       ADM + "\n- Đang đứng tại folder khác「未分類」(vd「アンケート」)",
       "1. Click folder「アンケート」\n2. Click「新規作成」\n"
       "3. Tại form đổi dropdown「フォルダ」sang「予約情報」\n4. Click「保存」\n"
       "5. Quan sát folder màn list mở vào\n"
       "6. Lặp lại với thao tác EDIT một trường và đổi folder sang「未分類」",
       "Tạo: アンケート → chọn 予約情報\nEdit: 予約情報 → chọn 未分類",
       "- Trường mới nằm đúng trong folder đã chọn ở form (「予約情報」)\n"
       "- Màn list mở vào đúng folder đã chọn ở form, không phải folder đứng trước đó\n"
       "- Case edit: trường chuyển sang「未分類」và list mở vào「未分類」",
       note="⚠️ Corpus r214/r216 ghi 2 vế khác nhau trong cùng 1 ô (\"hiển thị ở đúng folder đã chọn ở màn tạo mới\" + "
            "\"list mở vào folder đã chọn TRƯỚC KHI nhấn tạo mới\") — xem MT-06. Nguồn: r214, r216."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder: EDIT / COPY trường mà KHÔNG đổi folder → về list vẫn đứng folder cũ",
       ADM + "\n- Đang ở folder「予約情報」có ≥ 1 trường",
       "1. Click folder「予約情報」\n2. Click 管理名 để vào màn edit → Click「保存」\n"
       "3. Quan sát folder màn list\n4. Thực hiện copy 1 trường → Click「保存」\n"
       "5. Quan sát lại folder màn list",
       "Không đổi dropdown フォルダ ở cả 2 thao tác",
       "- Edit thành công, list mở vào「予約情報」\n"
       "- Copy thành công, list mở vào「予約情報」",
       note="Nguồn: r215, r217, r225, r226."),

    tc("Màn list thông tin", "STATE-001", "Normal",
       "Cookie folder ở folder mặc định「未分類」: tạo / sort / xóa / edit / copy đều giữ nguyên「未分類」",
       ADM + "\n- Đang đứng ở folder「未分類」",
       "1. Tại「未分類」tạo 1 trường mới → quan sát\n2. Sort item rồi tạo tiếp 3 trường → quan sát\n"
       "3. Click qua lại nhiều folder rồi quay lại tạo → quan sát\n"
       "4. Xóa 1 trường → quan sát\n5. Edit và copy 1 trường → quan sát",
       "Toàn bộ thao tác thực hiện trong「未分類」",
       "- Mọi thao tác: list luôn mở vào folder「未分類」\n"
       "- Trường tạo/copy nằm trong「未分類」\n"
       "- Gán/gửi action cho trường mới hoạt động bình thường",
       note="Nguồn: r218-r226."),

    tc("Màn list thông tin", "PERM-001", "Normal",
       "Login user từ màn super admin → thao tác folder không bị ép về folder mặc định; logout sạch cookie",
       "- Có tài khoản super admin và bot A\n- Bot A đang có cookie folder trỏ tới「予約情報」",
       "1. Từ màn super admin, login vào bot A\n2. Mở /basic/friend-information, thao tác chọn folder\n"
       "3. Thực hiện tạo 1 trường\n4. Logout\n5. Login lại và mở lại màn",
       "—",
       "- Login thành công, thao tác chọn folder/tạo trường bình thường, không bị focus ép về「未分類」\n"
       "- Logout thành công, không còn phiên đăng nhập\n"
       "- Login lại mở màn không lỗi",
       note="Nguồn: r227-r228 (#36201)."),

    tc("Màn list thông tin", "SEC-ISO-001", "Abnormal",
       "Cách ly theo bot: cookie folder của bot A không áp cho bot B",
       "- Tài khoản quản lý 2 bot A và B, mỗi bot có folder riêng khác tên",
       "1. Ở bot A chọn folder「予約情報」\n2. Chuyển sang bot B, mở /basic/friend-information\n"
       "3. Quan sát folder đang chọn và danh sách item\n4. Quay lại bot A",
       "Bot A: folder「予約情報」· Bot B: folder「B-Folder」",
       "- Bot B mở vào folder hợp lệ CỦA BOT B (mặc định「未分類」nếu chưa có cookie), không lấy folder id của bot A\n"
       "- Danh sách trường của bot B không lẫn trường của bot A\n"
       "- Quay lại bot A vẫn giữ「予約情報」",
       note="Cookie lưu dạng {bot_id: folder_id} (spec BR-12). TC do AI bổ sung theo SEC-ISO-001, cần Leader xác nhận."),

    # ══════════════════ Tạo folder ══════════════════
    tc("Tạo folder", "FUNC-001", "Normal",
       "Tạo folder tên hợp lệ (latinh / JP full-width / half-width katakana) → hiện ở panel trái với count 0",
       ADM,
       "1. Click icon (+) ở panel folder\n2. Nhập tên folder\n3. Click「決定」\n"
       "4. Reload trang và kiểm tra lại",
       "Lần 1:「予約情報」(JP full-width)\nLần 2:「Campaign-01」(latinh + số + gạch)\n"
       "Lần 3:「ﾖﾔｸ」(half-width katakana)",
       "- Cả 3 folder xuất hiện ở panel trái, số lượng item hiển thị「0」\n"
       "- Sau reload cả 3 folder còn nguyên, tên lưu verbatim (không lỗi font)\n"
       "- Click vào folder mới → panel phải rỗng",
       note="3 input cùng 1 kết quả nên giữ chung 1 TC. Nguồn: spec ui-spec.md §SCR-FRI-07 + corpus khối folder r106."),

    tc("Tạo folder", "UI-INPUT-001", "Boundary",
       "Tên folder đúng 15 ký tự → lưu được; bộ đếm hiển thị 15/15",
       ADM,
       "1. Click (+)\n2. Nhập chuỗi đúng 15 ký tự\n3. Quan sát bộ đếm ký tự\n4. Click「決定」",
       "「あいうえおかきくけこさしすせそ」(15 ký tự JP)",
       "- Bộ đếm hiển thị 15/15\n- Lưu thành công, tên hiển thị đủ 15 ký tự không bị cắt",
       note="Giới hạn 15 ký tự theo spec ui-spec.md:215. Corpus không có TC cận biên → TC do AI bổ sung."),

    tc("Tạo folder", "UI-INPUT-001", "Boundary",
       "Tên folder 16 ký tự → bị chặn ở tầng input hoặc báo lỗi, KHÔNG lưu quá 15",
       ADM,
       "1. Click (+)\n2. Gõ 16 ký tự\n3. Thử paste chuỗi 30 ký tự\n4. Click「決定」\n"
       "5. Kiểm tra lại tên folder ở panel trái",
       "Gõ:「あいうえおかきくけこさしすせそた」(16)\nPaste: chuỗi 30 ký tự latinh",
       "- Ô nhập không nhận quá 15 ký tự (cả khi gõ và khi paste), HOẶC hiển thị message lỗi giới hạn 15 ký tự\n"
       "- Không có folder nào được tạo với tên > 15 ký tự",
       note="⚠️ Cơ chế (chặn input vs báo lỗi) chưa được spec chốt — xem MT-07. TC do AI bổ sung."),

    tc("Tạo folder", "UI-INPUT-001", "Abnormal",
       "Bỏ trống tên folder → không tạo được",
       ADM,
       "1. Click (+)\n2. Để trống ô tên\n3. Click「決定」\n4. Nhập toàn dấu cách rồi「決定」",
       "Lần 1: chuỗi rỗng\nLần 2: 5 dấu cách",
       "- Không tạo folder mới ở panel trái\n- Hiển thị message yêu cầu nhập tên (hoặc nút「決定」bị disable)",
       note="Corpus không có TC; TC do AI bổ sung theo UI-INPUT-001, cần Leader xác nhận behavior với chuỗi toàn space."),

    tc("Tạo folder", "FUNC-001", "Normal",
       "Tạo folder xong → tạo trường thông tin trong folder mới: form tạo mở sẵn folder mới",
       ADM,
       "1. Tạo folder mới「New-01」\n2. Ngay sau đó click「新規作成」\n"
       "3. Quan sát dropdown「フォルダ」ở form tạo",
       "Folder「New-01」vừa tạo",
       "- Dropdown「フォルダ」có sẵn「New-01」trong danh sách và đang được chọn\n"
       "- Lưu trường → trường nằm trong folder「New-01」, count folder tăng lên 1",
       note="Nguồn: Test bug folder all màn r107 (khối màn friend info)."),

    tc("Tạo folder", "CONC-001", "Abnormal",
       "Đang mở modal EDIT folder → click sang modal CREATE: tạo mới thành công, KHÔNG ghi đè tên folder đang edit",
       ADM + "\n- Có sẵn folder「予約情報」",
       "1. Click icon sửa của folder「予約情報」(modal edit mở)\n2. Sửa tên trong ô nhập nhưng chưa lưu\n"
       "3. Không đóng modal, click sang nút (+) tạo folder mới\n4. Nhập tên mới và「決定」\n"
       "5. Kiểm tra tên folder「予約情報」và folder mới",
       "Tên gõ dở ở modal edit:「予約情報-XX」\nTên folder mới:「Create-01」",
       "- Folder「Create-01」được tạo mới\n"
       "- Folder「予約情報」GIỮ NGUYÊN tên cũ, không bị đổi thành「予約情報-XX」\n"
       "- Số lượng folder tăng đúng 1",
       note="Bug Tester #27083 (04/2026) — kịch bản lẫn state giữa 2 modal. Nguồn: Improve chung/Test bug folder all màn r114."),

    tc("Tạo folder", "CONC-001", "Normal",
       "Copy tên folder từ modal edit → cancel → paste sang modal create (có sửa và không sửa)",
       ADM + "\n- Có sẵn folder「予約情報」",
       "1. Mở modal edit folder「予約情報」, copy text tên\n2. Click「キャンセル」\n"
       "3. Click (+), paste tên vừa copy, sửa thêm hậu tố → lưu\n"
       "4. Lặp lại nhưng paste và KHÔNG sửa gì → lưu\n"
       "5. Kiểm tra panel trái",
       "Lần 1:「予約情報-copy」\nLần 2:「予約情報」(trùng tên folder cũ)",
       "- Cả 2 lần tạo folder mới thành công, là bản ghi folder MỚI (id khác)\n"
       "- Tên folder gốc「予約情報」không bị ảnh hưởng\n"
       "- Trùng tên folder vẫn cho tạo (folder không unique)",
       note="⚠️ Vế 'trùng tên vẫn cho tạo' suy từ hành vi màn tag (corpus ghi 'Base theo testcase fix bug màn tag'); "
            "spec FA-015 không ghi rule unique folder — xem MT-08. Nguồn: r106, r115-r116."),

    tc("Tạo folder", "STATE-001", "Normal",
       "Cancel modal create rồi mở lại → tạo được bình thường, ô nhập sạch",
       ADM,
       "1. Click (+), nhập tên, click「キャンセル」\n2. Click (+) lần nữa\n"
       "3. Quan sát ô nhập\n4. Nhập tên mới và lưu",
       "Lần 1 gõ dở:「abc」\nLần 2:「New-02」",
       "- Lần mở thứ 2 ô nhập trống (không còn「abc」)\n- Tạo folder「New-02」thành công",
       note="Nguồn: r120."),

    # ══════════════════ Sửa folder ══════════════════
    tc("Sửa folder", "FUNC-001", "Normal",
       "Đổi tên folder → panel trái cập nhật tên mới, item bên trong không đổi",
       ADM + "\n- Folder「予約情報」có 2 trường thông tin",
       "1. Click icon sửa folder「予約情報」\n2. Đổi tên thành「予約情報-2026」\n3. Lưu\n"
       "4. Reload trang\n5. Click vào folder và đối chiếu danh sách trường",
       "Tên mới:「予約情報-2026」",
       "- Panel trái hiển thị tên mới sau khi lưu và sau reload\n"
       "- Folder vẫn là cùng 1 folder (không sinh folder mới)\n"
       "- 2 trường bên trong giữ nguyên, count không đổi",
       note="Nguồn: Test bug folder all màn r106-r113."),

    tc("Sửa folder", "FUNC-SEQ-001", "Normal",
       "Edit thành công lần 1 → edit tiếp lần 2 cùng folder → reload → edit folder khác: mỗi lần đều lưu đúng",
       ADM + "\n- Có ≥ 2 folder",
       "1. Edit folder F1 lần 1 → lưu\n2. Edit ngay folder F1 lần 2 → lưu\n"
       "3. Reload trang\n4. Edit folder F2 → lưu\n5. Đối chiếu tên cả 2 folder",
       "F1: A1 → A2 · F2: B1 → B2",
       "- F1 mang tên A2 (lần lưu cuối), F2 mang tên B2\n"
       "- Không folder nào bị ghi nhầm tên của folder kia\n"
       "- Số lượng folder không đổi",
       note="Chuỗi thao tác liên tiếp nên giữ 1 TC. Nguồn: r108-r113."),

    tc("Sửa folder", "FUNC-SEQ-001", "Normal",
       "Edit folder thành công → thao tác tiếp: tạo mới / sort folder / xóa chính folder vừa edit / xóa folder khác",
       ADM + "\n- Có ≥ 3 folder",
       "1. Edit folder F1 → lưu\n2. Thực hiện 1 trong 4 thao tác, mỗi lần bắt đầu lại từ bước 1:\n"
       "   (a) tạo folder mới\n   (b) sort folder\n   (c) xóa chính F1\n   (d) xóa folder F2 khác\n"
       "3. Reload và đối chiếu panel trái",
       "4 nhánh (a)(b)(c)(d)",
       "- Mỗi nhánh: thao tác sau thực hiện đúng, tên F1 sau edit không bị mất/ghi đè\n"
       "- Nhánh (c): F1 biến mất khỏi panel; các folder còn lại giữ nguyên tên và thứ tự\n"
       "- Nhánh (d): F2 biến mất, F1 vẫn mang tên mới",
       note="Nguồn: r108-r113."),

    tc("Sửa folder", "FUNC-SEQ-001", "Normal",
       "Edit folder ngay sau khi vừa XÓA một folder khác → vẫn lưu đúng folder đích",
       ADM + "\n- Có ≥ 3 folder F1, F2, F3",
       "1. Xóa folder F2\n2. Không reload, click icon sửa folder F3\n3. Đổi tên và lưu\n"
       "4. Reload và đối chiếu",
       "F3: C1 → C2",
       "- F3 mang tên C2\n- F1 không bị đổi tên\n- F2 vẫn ở trạng thái đã xóa (không quay lại)",
       note="Nguồn: r113."),

    tc("Sửa folder", "FUNC-001", "Normal",
       "Nhập tên lần 1 chưa lưu → nhập tiếp lần 2 → lưu: lấy giá trị lần lưu cuối, id folder không đổi",
       ADM,
       "1. Mở modal edit folder F1\n2. Gõ tên N1, KHÔNG lưu\n3. Gõ tiếp đè thành N2\n4. Lưu\n"
       "5. Reload và kiểm tra tên + số lượng item của F1",
       "N1 =「temp-1」· N2 =「final-2」",
       "- Tên folder =「final-2」\n- Vẫn là cùng folder cũ (item bên trong giữ nguyên, count không đổi)",
       note="Nguồn: r117-r118."),

    tc("Sửa folder", "STATE-001", "Normal",
       "Edit folder → lưu → bấm ngay nút tạo folder mới: tên folder vừa edit không bị đổi lần nữa",
       ADM,
       "1. Edit folder F1 → lưu\n2. Bấm ngay (+) mở modal create\n3. Đóng modal create (cancel)\n"
       "4. Reload và kiểm tra tên F1",
       "F1: A1 → A2",
       "- F1 giữ đúng tên A2\n- Không sinh folder mới nào",
       note="Nguồn: r119."),

    tc("Sửa folder", "STATE-001", "Normal",
       "Cancel modal edit rồi mở lại CÙNG folder → ô nhập hiển thị tên hiện tại, không giữ text gõ dở",
       ADM,
       "1. Mở modal edit F1, gõ đè tên mới, click「キャンセル」\n2. Mở lại modal edit F1\n"
       "3. Quan sát giá trị trong ô nhập",
       "Text gõ dở:「draft-name」",
       "- Ô nhập hiển thị tên hiện tại của F1, KHÔNG hiển thị「draft-name」\n"
       "- Tên F1 ở panel trái không đổi",
       note="Nguồn: r117, r121."),

    tc("Sửa folder", "CONC-001", "Abnormal",
       "Cancel modal edit folder F1 → mở modal edit folder F2 → lưu: tên chỉ ghi vào F2",
       ADM + "\n- Có 2 folder F1, F2",
       "1. Mở modal edit F1, gõ tên mới, click「キャンセル」\n2. Mở modal edit F2\n"
       "3. Nhập tên mới cho F2 → lưu\n4. Reload, đối chiếu tên F1 và F2",
       "F1 gõ dở:「X」· F2 nhập:「Y」",
       "- F2 mang tên「Y」\n- F1 GIỮ NGUYÊN tên cũ, không thành「X」",
       note="Đây là lõi Bug Tester #27083. Nguồn: r122."),

    tc("Sửa folder", "CONC-002", "Abnormal",
       "2 tài khoản cùng sửa 1 folder: người lưu sau ghi đè, màn người kia reload thấy dữ liệu mới, không lỗi",
       "- 2 tài khoản admin cùng bot A, cùng mở /basic/friend-information\n- Folder F1 tên「old」",
       "1. User A mở modal edit F1\n2. User B mở modal edit F1, đổi tên thành「B-name」→ lưu\n"
       "3. User A đổi tên thành「A-name」→ lưu\n4. User B reload màn list",
       "A-name / B-name",
       "- Không màn nào văng lỗi\n- Sau bước 3, F1 mang tên「A-name」(người lưu sau thắng)\n"
       "- User B reload thấy「A-name」\n- Item trong folder không bị mất",
       note="TC do AI bổ sung theo CONC-002 (corpus không có chiều đa người dùng cho folder), cần Leader xác nhận quy tắc last-write-win."),

    tc("Sửa folder", "UI-INPUT-001", "Boundary",
       "Sửa tên folder vượt 15 ký tự → bị chặn/báo lỗi giống lúc tạo",
       ADM + "\n- Có folder F1",
       "1. Mở modal edit F1\n2. Gõ và paste chuỗi 20 ký tự\n3. Lưu\n4. Kiểm tra tên hiển thị",
       "Chuỗi 20 ký tự latinh",
       "- Không lưu được tên > 15 ký tự (chặn input hoặc báo lỗi)\n- Tên F1 không bị cắt ngầm thành chuỗi khác",
       note="Đối xứng với TC tạo folder. TC do AI bổ sung — xem MT-07."),

    # ══════════════════ Xóa folder ══════════════════
    tc("Xóa folder", "FUNC-001", "Normal",
       "Xóa folder RỖNG → folder biến mất, các folder khác không đổi",
       ADM + "\n- Folder「Empty-01」không có trường nào",
       "1. Click icon xóa folder「Empty-01」\n2. Xác nhận xóa\n3. Reload trang",
       "Folder rỗng",
       "- Folder「Empty-01」không còn ở panel trái sau khi xóa và sau reload\n"
       "- Các folder khác giữ nguyên tên, thứ tự, count",
       note="Nguồn: khối folder r106-r113 + spec BR-01."),

    tc("Xóa folder", "DATA-REF-001", "Abnormal",
       "Xóa folder CÓ trường thông tin → cascade xóa trường + giá trị + hiển thị chat 1:1 bên trong",
       ADM + "\n- Folder「予約情報」có 3 trường (選択肢 có option gắn action, 年月日 có lịch, ポイント)\n"
       "- Mỗi trường có ≥ 2 bạn đang có giá trị\n- 1 trường đang được bật hiển thị ở right bar chat 1:1",
       "1. Ghi lại 回答人数 của 3 trường và danh sách bạn có giá trị\n"
       "2. Xóa folder「予約情報」và xác nhận\n3. Reload màn list\n"
       "4. Mở chat 1:1 của 1 bạn có giá trị, xem tab 友だち情報\n"
       "5. Mở màn 友だち詳細 (my_page) của bạn đó",
       "3 trường, 2 bạn/trường",
       "- Folder và cả 3 trường biến mất khỏi màn list\n"
       "- Right bar chat 1:1 không còn hiển thị trường đã xóa\n"
       "- Màn 友だち詳細 không còn giá trị của 3 trường đó\n"
       "- Không màn nào văng lỗi khi mở",
       note="Cascade theo spec BR-06. Corpus chỉ có mức tab「Change spec info type select」r71 (xóa folder → xóa "
            "friend_info_option_select); phần kiểm ở UI là AI bổ sung theo RULE-06/07."),

    tc("Xóa folder", "JOB-001", "Abnormal",
       "Xóa folder chứa trường 年月日 đang có lịch gửi → lịch gửi của trường đó bị dọn, không còn action mồ côi",
       ADM + "\n- Folder F có 1 trường 年月日 đã setting action, ≥ 2 bạn có giá trị và đã sinh lịch gửi tương lai\n"
       "- Có 1 trường 年月日 khác NGOÀI folder F cũng đang có lịch",
       "1. Ghi lại lịch gửi hiện có của cả 2 trường (màn thông tin bạn / log job)\n"
       "2. Xóa folder F\n3. Chờ tới thời điểm lịch cũ của trường trong F\n"
       "4. Kiểm tra LINE app của bạn thuộc trường trong F\n"
       "5. Chờ tới lịch của trường ngoài F và kiểm tra LINE app",
       "2 trường 年月日, mỗi trường 2 bạn",
       "- Bạn thuộc trường trong folder F KHÔNG nhận được action nào sau khi xóa folder\n"
       "- Bạn thuộc trường ngoài folder F VẪN nhận action đúng giờ\n"
       "- Job không báo lỗi trong log",
       env="PRODUCTION",
       note="RULE-08 (job) → PRODUCTION. Spec BR-06 mục 6 ghi 'implicit' xóa event_step/event_step_time — "
            "corpus không có TC → xem MT-09. TC do AI bổ sung."),

    tc("Xóa folder", "JOB-001", "Normal",
       "Job dọn category đã xóa (kind=12) → xóa dữ liệu các trường thuộc folder đó",
       "- Bot A có folder friend info bị đánh dấu đã xóa và còn trường bên trong\n"
       "- Job dọn category đang bật",
       "1. Xóa 1 folder friend info có 2 trường\n2. Chờ job dọn category chạy\n"
       "3. Mở lại màn /basic/friend-information\n"
       "4. Mở màn 友だち詳細 của bạn từng có giá trị ở trường trong folder đó",
       "Folder F: 2 trường, mỗi trường 2 bạn có giá trị",
       "- Sau khi job chạy, folder và 2 trường không còn xuất hiện ở bất kỳ màn nào\n"
       "- Màn 友だち詳細 không còn giá trị của 2 trường đó\n"
       "- Các folder/trường của bot khác không bị đụng",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung /「recover bảng category」(20/06/2025) dòng kind=12 → friend_information_setting. "
            "RULE-08 job → PRODUCTION."),

    tc("Xóa folder", "FUNC-001", "Abnormal",
       "Không thể xóa folder mặc định「未分類」và 2 folder hệ thống (thông tin cơ bản / địa chỉ)",
       ADM,
       "1. Quan sát folder「未分類」và các folder thông tin mặc định / địa chỉ ở panel trái\n"
       "2. Thử tìm và bấm icon xóa/sửa của các folder này",
       "「未分類」· folder thông tin mặc định · folder thông tin địa chỉ",
       "- Không có nút xóa (và không có nút đổi tên) cho「未分類」và 2 folder hệ thống\n"
       "- Không xóa được bằng thao tác UI",
       note="Spec BR-01/BR-10: 未分類 là folder ảo (group_id=0), -1/-2 là folder hệ thống. Corpus không có TC → AI bổ sung."),

    tc("Xóa folder", "SEC-001", "Abnormal",
       "Gọi trực tiếp API xóa folder với folder id của BOT KHÁC → không xóa nhầm",
       "- Tài khoản admin bot A\n- Biết id folder của bot B (không thuộc quyền phiên hiện tại)",
       "1. Đăng nhập bot A, mở màn friend information\n"
       "2. Dùng DevTools gửi lại request xóa folder nhưng thay group_id bằng id folder của bot B\n"
       "3. Kiểm tra panel folder của bot B",
       "group_id = id folder của bot B",
       "- Request bị từ chối (lỗi quyền / không tìm thấy)\n"
       "- Folder của bot B vẫn còn nguyên cùng toàn bộ trường bên trong",
       note="TC do AI bổ sung theo SEC-001 (spec Gap #2 chưa xác nhận phân quyền), cần Leader xác nhận."),

    # ══════════════════ Sắp xếp folder ══════════════════
    tc("Sắp xếp folder", "FUNC-001", "Normal",
       "Kéo thả đổi thứ tự folder → thứ tự mới giữ sau reload",
       ADM + "\n- Có 4 folder theo thứ tự F1, F2, F3, F4",
       "1. Click「並べ替え」(chế độ sắp xếp folder)\n2. Kéo F4 lên vị trí đầu\n3. Lưu\n"
       "4. Reload trang\n5. Đọc thứ tự folder ở panel trái",
       "Thứ tự mong muốn: F4, F1, F2, F3",
       "- Panel trái hiển thị đúng thứ tự F4, F1, F2, F3 ngay sau khi lưu\n"
       "- Sau reload thứ tự vẫn giữ nguyên\n"
       "- Count item của từng folder không đổi",
       note="Nguồn: khối folder r109 (Edit success => Sort folder) + spec field #18."),

    tc("Sắp xếp folder", "FUNC-001", "Normal",
       "Sort folder kéo lên đầu / xuống cuối / random nhiều folder",
       ADM + "\n- Có 6 folder F1..F6",
       "1. Kéo F6 lên đầu → lưu → reload\n2. Kéo F1 xuống cuối → lưu → reload\n"
       "3. Kéo random 3 folder về vị trí bất kỳ → lưu → reload\n4. Ghi lại thứ tự sau mỗi bước",
       "3 kịch bản sort trên cùng bộ 6 folder",
       "- Sau mỗi bước, thứ tự hiển thị đúng như thao tác kéo thả\n"
       "- Sau reload không bị nhảy về thứ tự cũ\n"
       "- Không folder nào bị mất khỏi panel",
       note="Nguồn: mẫu kịch bản sort ở Test bug folder all màn r299-r318 (áp cho màn friend info)."),

    tc("Sắp xếp folder", "DATA-COUNT-001", "Normal",
       "Sau khi sort folder → danh sách trường và số count của từng folder vẫn đúng",
       ADM + "\n- 4 folder có số trường lần lượt 2 / 0 / 5 / 1",
       "1. Ghi lại count từng folder\n2. Sort folder theo thứ tự đảo ngược → lưu\n"
       "3. Reload\n4. Click lần lượt từng folder và đếm số trường ở panel phải",
       "Count trước sort: 2 / 0 / 5 / 1",
       "- Count hiển thị ở panel trái sau sort vẫn là 2 / 0 / 5 / 1 gắn đúng folder tương ứng\n"
       "- Panel phải liệt kê đúng số trường của folder đang chọn\n"
       "- Không folder nào mất dữ liệu sau khi sort",
       note="Đối chứng bug 'sort folder xong mất data' của Bug Tester #27083 (màn Item) triển khai ngang sang friend info. "
            "Nguồn: r296, r299-r318."),

    tc("Sắp xếp folder", "FUNC-SEQ-001", "Normal",
       "Xóa 1 folder → sort các folder còn lại: thứ tự đúng, folder đã xóa không quay lại",
       ADM + "\n- Có 5 folder",
       "1. Xóa folder F3\n2. Sort các folder còn lại\n3. Lưu và reload\n4. Đối chiếu panel trái",
       "5 folder, xóa F3, sort 4 folder còn lại",
       "- F3 không xuất hiện lại\n- 4 folder còn lại theo đúng thứ tự vừa sort\n"
       "- Item trong từng folder hiển thị bình thường",
       note="Nguồn: r319-r322 (mẫu kịch bản #27083)."),

    tc("Sắp xếp folder", "ENV-001", "Normal",
       "Sort folder trên môi trường PRODUCTION → không mất folder/danh sách trường",
       "- Bot thật trên production có ≥ 5 folder friend info và ≥ 20 trường",
       "1. Ghi lại thứ tự + count folder\n2. Sort folder → lưu\n3. Reload trang\n"
       "4. Click lần lượt từng folder",
       "Bot production có dữ liệu thật",
       "- Thứ tự folder đúng theo thao tác\n- Không folder nào biến mất, count không về 0\n"
       "- Danh sách trường mỗi folder hiển thị đủ",
       env="PRODUCTION",
       note="Bug gốc #27083 chỉ tái hiện ở data thật/môi trường prod (corpus tách riêng 'môi trường test' vs "
            "'môi trường prod' r299-r318) → RULE-08."),

    # ══════════════════ Sắp xếp & chuyển folder item ══════════════════
    tc("Sắp xếp & chuyển folder item", "FUNC-001", "Normal",
       "Kéo thả sắp xếp trường trong 1 folder → thứ tự giữ sau reload",
       ADM + "\n- Folder F có 5 trường I1..I5",
       "1. Click「並べ替え」ở panel phải\n2. Kéo I5 lên đầu, I1 xuống cuối\n3. Lưu\n"
       "4. Reload và đọc lại thứ tự",
       "Thứ tự mong muốn: I5, I2, I3, I4, I1",
       "- Bảng hiển thị đúng thứ tự I5, I2, I3, I4, I1\n- Sau reload thứ tự không đổi\n"
       "- Không trường nào bị mất hoặc nhân đôi",
       note="Nguồn: r205, r208 (#36201) + spec EP-06 action=sortItem."),

    tc("Sắp xếp & chuyển folder item", "FUNC-SEQ-001", "Normal",
       "Sort item → tạo trường mới: trường mới xuất hiện đúng folder, thứ tự các trường cũ không loạn",
       ADM + "\n- Folder F có 3 trường",
       "1. Sort item trong folder F\n2. Tạo trường mới trong F (lặp 3 lần liên tiếp)\n"
       "3. Sau mỗi lần tạo, ghi lại thứ tự bảng",
       "3 lần tạo liên tiếp",
       "- Cả 3 trường mới đều nằm trong folder F\n"
       "- Thứ tự các trường đã sort trước đó không bị đảo lộn\n"
       "- Màn list vẫn đứng tại folder F sau mỗi lần tạo",
       note="Nguồn: r208-r210, r219-r221."),

    tc("Sắp xếp & chuyển folder item", "BULK-001", "Normal",
       "Chọn nhiều trường → 一括フォルダ変更 sang folder khác: item chuyển đủ, count 2 folder cập nhật",
       ADM + "\n- Folder A có 5 trường, folder B có 1 trường",
       "1. Ghi lại count folder A và B\n2. Ở folder A tick chọn 3 trường\n"
       "3. Click「一括フォルダ変更」, chọn folder B, xác nhận\n4. Reload\n"
       "5. Đếm lại số trường ở A và B",
       "Chuyển 3/5 trường từ A sang B",
       "- Folder A còn 2 trường, folder B có 4 trường\n"
       "- Count ở panel trái: A = 2, B = 4\n"
       "- 3 trường chuyển sang B giữ nguyên 管理名, 情報タイプ, 回答人数 và giá trị của bạn bè",
       note="Spec EP-06 action=moveItem. Corpus không có TC bulk move cho friend info → AI bổ sung theo BULK-001."),

    tc("Sắp xếp & chuyển folder item", "BULK-001", "Boundary",
       "一括フォルダ変更 chọn TẤT CẢ trường của folder → folder nguồn còn 0 item, vẫn tồn tại",
       ADM + "\n- Folder A có 4 trường",
       "1. Tick chọn tất cả 4 trường ở folder A\n2. Chuyển sang folder B\n3. Reload\n"
       "4. Click vào folder A",
       "Chuyển 4/4 trường",
       "- Folder A vẫn tồn tại ở panel trái với count「0」\n"
       "- Panel phải của A hiển thị trạng thái rỗng, không lỗi\n"
       "- Folder B nhận đủ 4 trường",
       note="TC do AI bổ sung theo BULK-001/LIST-001."),

    tc("Sắp xếp & chuyển folder item", "BULK-001", "Abnormal",
       "Không tick trường nào mà bấm 一括削除 / 一括フォルダ変更 → không thao tác gì, không lỗi",
       ADM + "\n- Folder A có 3 trường",
       "1. Không tick checkbox nào\n2. Bấm「一括削除」\n3. Bấm「一括フォルダ変更」\n"
       "4. Reload và đếm lại số trường",
       "0 trường được chọn",
       "- Không có trường nào bị xóa hoặc chuyển folder\n"
       "- Hiển thị thông báo yêu cầu chọn item (hoặc nút bị disable), không văng lỗi hệ thống",
       note="TC do AI bổ sung theo BULK-001, cần Leader xác nhận message thực tế."),

    tc("Sắp xếp & chuyển folder item", "BULK-001", "Abnormal",
       "一括削除 nhiều trường cùng lúc → xóa đủ, cascade giá trị + count, trường không chọn không bị đụng",
       ADM + "\n- Folder A có 5 trường, mỗi trường ≥ 2 bạn có giá trị",
       "1. Ghi lại 回答人数 của 5 trường\n2. Tick chọn 3 trường → click「一括削除」→ xác nhận\n"
       "3. Reload màn list\n4. Mở màn 友だち詳細 của 1 bạn có giá trị ở cả 5 trường\n"
       "5. Mở right bar chat 1:1 của bạn đó",
       "Xóa 3/5 trường",
       "- 3 trường biến mất khỏi màn list, 2 trường còn lại giữ nguyên 回答人数\n"
       "- Màn 友だち詳細 và right bar chat 1:1 không còn 3 trường đã xóa, vẫn hiển thị 2 trường còn lại\n"
       "- Không màn nào văng lỗi",
       note="Spec BR-06 cascade. RULE-07 (DB + màn hình + output). AI viết expected ở tầng UI."),

    tc("Sắp xếp & chuyển folder item", "PERF-LARGE-001", "Boundary",
       "Folder có số lượng trường lớn (≥ 100) → màn list load được, sort/chuyển folder vẫn đúng",
       "- Bot có 1 folder chứa ≥ 100 trường thông tin",
       "1. Mở folder đó, đo thời gian tới khi bảng hiển thị xong\n"
       "2. Cuộn hết bảng, kiểm tra có phân trang hay không\n"
       "3. Sort 1 trường từ cuối lên đầu → lưu → reload\n"
       "4. Chọn 20 trường → chuyển sang folder khác",
       "≥ 100 trường trong 1 folder",
       "- Trang hiển thị đủ danh sách (hoặc phân trang hoạt động đúng), không treo/timeout\n"
       "- Sort lưu đúng vị trí sau reload\n"
       "- 20 trường chuyển đủ sang folder đích, count 2 folder khớp",
       env="PRODUCTION",
       note="Spec Gap #5: pagination chưa xác nhận. TC do AI bổ sung theo PERF-LARGE-001 — cần Leader xác nhận có phân trang không."),

    tc("Sắp xếp & chuyển folder item", "CONC-001", "Abnormal",
       "Double-click nút lưu khi sort item → chỉ ghi 1 lần, thứ tự không loạn",
       ADM + "\n- Folder A có 5 trường",
       "1. Vào chế độ sort, kéo đổi vị trí\n2. Double-click nhanh nút lưu\n3. Reload\n"
       "4. Đối chiếu thứ tự và số lượng trường",
       "Double-click trong < 1 giây",
       "- Thứ tự đúng như thao tác kéo\n- Số trường không đổi (không nhân bản)\n"
       "- Không hiển thị lỗi",
       note="TC do AI bổ sung theo CONC-001 (double-click), cần Leader xác nhận."),
]
