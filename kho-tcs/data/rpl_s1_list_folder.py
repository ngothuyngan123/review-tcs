# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 1: Màn list, folder, bật/tắt, sắp xếp, xóa, tìm kiếm."""
from _common import tc

BOT = "- Đăng nhập admin, đang chọn bot A\n- Màn hình /basic/reply (自動応答)"
BOT2 = BOT + "\n- Có ≥2 folder: 未分類 (mặc định) + folder A + folder B tự tạo"

S1 = [
    # ═══════════════ Màn list — hiển thị & cột ═══════════════
    tc("Màn list — hiển thị & cột", "UI-001", "Normal",
       "SCR-RPL-01: màn 自動応答 hiển thị đủ header + sidebar フォルダ + toolbar 4 nút",
       BOT,
       "1. Truy cập /basic/reply\n2. Quan sát header, sidebar trái, toolbar phải\n3. Click link「マニュアル」",
       "Bot A đã có ≥1 quy tắc auto reply",
       "- Header hiện tiêu đề「自動応答」+ link「マニュアル」, click mở trang hướng dẫn lme.jp ở tab mới\n"
       "- Sidebar trái hiện khối「フォルダ」+ icon (+) tạo folder + icon sửa folder\n"
       "- Toolbar hiện đủ 4:「新規作成」「並べ替え」「一括フォルダ変更」「一括削除」",
       note="Evidence: ảnh full màn. Nguồn: ui-spec.md §SCR-RPL-01 — corpus TCs KHÔNG có TC check UI màn list, "
            "đây là TC lấp GAP do AI viết theo spec, CẦN LEADER XÁC NHẬN"),

    tc("Màn list — hiển thị & cột", "UI-FIELD-001", "Normal",
       "SCR-RPL-01: bảng danh sách hiển thị đúng 7 cột — 作成日 / 稼働状況 / キーワード / スケジュール + checkbox + 2 nút",
       BOT + "\n- Có 1 quy tắc dạng 全てのメッセージ và 1 quy tắc dạng キーワード có lịch trình",
       "1. Mở /basic/reply\n2. Đọc từng cột của 2 dòng quy tắc\n3. Đối chiếu với DB: SELECT id, created_at, is_stopped, "
       "keyword_reaction_type, time_reaction_type, day_of_week, start_time, end_time FROM auto_reply WHERE bot_id=A AND is_deleted=0",
       "Quy tắc 1: 全てのメッセージ, ON, 常に\nQuy tắc 2: keyword「予約」, OFF, 月火水 09:00~18:00",
       "- Cột「作成日」= created_at format YYYY.MM.DD\n"
       "- Cột「稼働状況」= ON khi is_stopped=0, OFF khi is_stopped=1\n"
       "- Cột「キーワード」: quy tắc 1 hiện「全てのメッセージ」; quy tắc 2 hiện keyword nối từ bảng keyword\n"
       "- Cột「スケジュール」: quy tắc 1 hiện「常に」; quy tắc 2 hiện「月,火,水 09:00~18:00」\n"
       "- Có checkbox chọn ở đầu dòng + nút sửa + nút xóa ở cuối dòng",
       note="Verify 2 tầng DB + màn hình (RULE-07). Nguồn: feature-spec.md §4 field #16-#19 — corpus KHÔNG có TC, "
            "TC lấp GAP do AI viết theo spec, CẦN LEADER XÁC NHẬN"),

    tc("Màn list — hiển thị & cột", "LIST-001", "Boundary",
       "SCR-RPL-01: folder rỗng (0 quy tắc) → bảng hiển thị empty state, sidebar hiện đếm (0)",
       BOT2 + "\n- Folder B chưa có quy tắc nào",
       "1. Mở /basic/reply\n2. Click folder B ở sidebar\n3. Quan sát bảng danh sách và số đếm cạnh tên folder",
       "Folder B: 0 quy tắc",
       "- Bảng hiện 0 dòng (empty state), KHÔNG lỗi JS, KHÔNG hiện dòng rỗng\n"
       "- Sidebar hiện「<tên folder B> (0)」\n- Toolbar vẫn thao tác được (新規作成 mở form với group_id = id folder B)",
       note="ui-spec.md §SCR-RPL-01 ghi rõ chỉ quan sát được màn 0 record. Corpus KHÔNG có TC empty state → GAP. "
            "TC do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Màn list — hiển thị & cột", "LIST-001", "Boundary",
       "SCR-RPL-01: folder có nhiều quy tắc (≥100) → kiểm tra phân trang / cuộn, không vỡ layout",
       BOT + "\n- Folder A có ≥100 quy tắc auto reply",
       "1. Mở /basic/reply, chọn folder A\n2. Cuộn hết danh sách\n3. Nếu có phân trang: chuyển sang trang 2, quay lại trang 1\n"
       "4. Đếm tổng số dòng so với COUNT(*) trong DB",
       "100 quy tắc trong 1 folder",
       "- Hiển thị đủ 100 quy tắc (qua cuộn hoặc phân trang), số dòng khớp COUNT(*) DB\n"
       "- Không vỡ layout, không treo trình duyệt\n- Sidebar hiện đúng số đếm (100)",
       note="Gap #16 của spec: 'Pagination khi danh sách có nhiều quy tắc — chưa quan sát được do danh sách trống'. "
            "TC lấp GAP do AI viết. MT-15. CẦN LEADER XÁC NHẬN có phân trang hay không"),

    # ═══════════════ Folder — tạo & sửa ═══════════════
    tc("Folder — tạo & sửa", "FUNC-001", "Normal",
       "addAndEditGroup: tạo folder mới ở màn 自動応答 → INSERT category kind=1",
       BOT,
       "1. Click icon (+) ở sidebar「フォルダ」\n2. Nhập tên folder\n3. Lưu\n4. Reload /basic/reply\n"
       "5. Query: SELECT * FROM category WHERE bot_id=A AND kind=1 ORDER BY id DESC",
       "Tên folder:「予約対応」",
       "- Folder hiện ở sidebar với số đếm (0)\n- DB: INSERT category mới (bot_id=A, kind=1, is_deleted=0)\n"
       "- Sau reload folder vẫn còn, tên lưu verbatim",
       note="kind=1 = folder auto reply (recover bảng category r4). Nguồn: Improve chung / Test bug folder all màn r4"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Abnormal",
       "Bug #32468: mở modal SỬA folder → copy tên → Cancel → mở modal TẠO MỚI → paste + sửa → lưu "
       "⇒ tạo folder mới, KHÔNG ghi đè lên folder đang sửa",
       BOT2,
       "1. Click icon sửa folder A → modal edit mở\n2. Copy text tên folder A trong ô nhập\n3. Click Cancel\n"
       "4. Click icon (+) tạo mới folder\n5. Paste tên đã copy, sửa thành tên khác\n6. Click lưu\n"
       "7. Query: SELECT id, name FROM category WHERE bot_id=A AND kind=1 ORDER BY id DESC",
       "Tên folder A gốc:「対応A」→ paste và sửa thành「対応A-2」",
       "- Tạo folder MỚI thành công, có id mới trong DB\n- Tên folder A gốc KHÔNG bị đổi (vẫn「対応A」)\n"
       "- Sidebar hiện cả 2 folder",
       note="Nguồn: Improve chung / Test bug folder all màn r4 (Bug #32468, 10/2025). "
            "Nguyên nhân gốc: mở modal add chưa clear id của folder edit"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Abnormal",
       "Bug #32468: ĐANG MỞ modal sửa folder → click sang modal tạo mới ⇒ ô nhập được clear, không update vào folder đang sửa",
       BOT2,
       "1. Click icon sửa folder A → modal edit mở, ô nhập đang có tên folder A\n"
       "2. KHÔNG đóng modal, click ngay nút tạo mới folder\n3. Quan sát ô nhập của modal create\n"
       "4. Nhập tên mới và lưu\n5. Query category WHERE bot_id=A AND kind=1",
       "Tên mới:「新規フォルダ」",
       "- Ô nhập của modal create RỖNG (không còn text của folder edit)\n"
       "- Lưu → tạo folder mới, folder A giữ nguyên tên và id",
       note="Nguồn: Improve chung / Test bug folder all màn r12 — cột Note ghi 'Lúc nhấn vào btn tạo mới thì chưa clear "
            "được input vẫn đang hiện text của folder edit' ⇒ ĐÂY LÀ ĐIỂM ĐÃ TỪNG LỖI, phải verify kỹ"),

    tc("Folder — tạo & sửa", "FUNC-SEQ-001", "Normal",
       "renameGroup: chuỗi sửa folder liên tiếp (sửa lần 1 → sửa lần 2 cùng folder → reload → sửa folder khác) "
       "⇒ mỗi lần lưu đúng folder, id không đổi",
       BOT2,
       "1. Sửa tên folder A lần 1 → lưu\n2. Sửa tên folder A lần 2 → lưu\n3. Reload trang\n"
       "4. Sửa tên folder B → lưu\n5. Query id + name của A và B",
       "A:「対応A」→「対応A1」→「対応A2」; B:「対応B」→「対応B1」",
       "- Sau mỗi lần lưu: tên đổi đúng folder được chọn\n- id của A và B KHÔNG đổi (không tạo record mới)\n"
       "- Tên B không bị ghi đè bởi thao tác trên A",
       note="Chuỗi thao tác liên tiếp nên giữ chung 1 TC (FUNC-SEQ). Nguồn: Test bug folder all màn r6"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Normal",
       "Sửa folder → nhập lần 1 chưa lưu → nhập tiếp lần 2 → lưu ⇒ lưu theo giá trị lần nhập CUỐI",
       BOT2,
       "1. Click sửa folder A\n2. Nhập tên「X1」(chưa lưu)\n3. Xóa, nhập tiếp「X2」\n4. Click lưu\n"
       "5. Query name + id của folder A",
       "Nhập lần 1「X1」, lần 2「X2」",
       "- category.name =「X2」\n- id folder giữ nguyên",
       note="Nguồn: Test bug folder all màn r16"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Normal",
       "Sửa folder → nhấn lưu → nhấn tạo mới folder ⇒ tên folder vừa sửa giữ nguyên, id không đổi",
       BOT2,
       "1. Sửa tên folder A → lưu thành công\n2. Click ngay nút tạo mới folder\n3. Đóng modal create không lưu\n"
       "4. Reload, query name + id folder A",
       "Tên mới của A:「対応A-new」",
       "- Tên folder A vẫn là「対応A-new」, KHÔNG bị reset hay ghi đè\n- id giữ nguyên",
       note="Nguồn: Test bug folder all màn r17"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Normal",
       "Cancel modal create rồi mở lại modal create ⇒ tạo folder mới thành công (state đã clear)",
       BOT2,
       "1. Mở modal tạo folder, nhập tên rồi Cancel\n2. Mở lại modal tạo folder\n3. Nhập tên khác, lưu\n"
       "4. Query category WHERE bot_id=A AND kind=1",
       "Lần 1 (cancel):「Tmp」; lần 2 (lưu):「対応C」",
       "- Chỉ tạo 1 folder「対応C」\n- KHÔNG tạo folder「Tmp」",
       note="Nguồn: Test bug folder all màn r18"),

    tc("Folder — tạo & sửa", "STATE-CLEAN-001", "Normal",
       "Cancel modal edit folder A → mở modal edit folder B → sửa → lưu ⇒ tên được update vào folder B (folder mở CUỐI)",
       BOT2,
       "1. Mở modal edit folder A rồi Cancel\n2. Mở modal edit folder B\n3. Sửa tên, lưu\n"
       "4. Query name của A và B",
       "Tên mới nhập:「対応B-new」",
       "- Folder B đổi tên thành「対応B-new」\n- Folder A giữ nguyên tên cũ",
       note="Nguồn: Test bug folder all màn r20"),

    tc("Folder — tạo & sửa", "FUNC-SEQ-001", "Normal",
       "Sau khi tạo folder mới → vào tạo quy tắc auto reply ⇒ màn 新規作成 mở với folder mới được chọn sẵn",
       BOT,
       "1. Tạo folder mới「対応D」\n2. Đang mở folder「対応D」, click「新規作成」\n"
       "3. Quan sát URL và giá trị dropdown「フォルダ」ở Phần 2 của form\n4. Lưu quy tắc, query auto_reply.category_id",
       "Folder mới「対応D」",
       "- URL = /basic/reply/new?group_id=<id folder 対応D>\n- Dropdown「フォルダ」chọn sẵn「対応D」\n"
       "- Sau lưu: auto_reply.category_id = id của folder 対応D",
       note="Nguồn: Test bug folder all màn r5 + r14"),

    # ═══════════════ Folder — xóa & cascade ═══════════════
    tc("Folder — xóa & cascade", "DATA-REF-001", "Normal",
       "deleteGroup: xóa folder chứa quy tắc dạng keyword ⇒ soft delete auto_reply + HARD delete keyword",
       BOT2 + "\n- Folder B chứa 1 quy tắc dạng keyword「keyC」",
       "1. Query trước: SELECT * FROM keyword WHERE keyword='keyC'\n2. Xóa folder B\n"
       "3. Query lại: SELECT * FROM category WHERE id=<B>; SELECT * FROM auto_reply WHERE category_id=<B>; "
       "SELECT * FROM keyword WHERE keyword='keyC'",
       "Keyword「keyC」",
       "- category.is_deleted = 1 (soft delete)\n- auto_reply.is_deleted = 1 (soft delete, cascade)\n"
       "- Bảng keyword: bản ghi「keyC」BỊ XÓA HẲN (hard delete, 0 dòng)\n- Sidebar không còn folder B",
       note="BR-04 + BR-07. Nguồn: Ver1.0 r47. ListBug của file gốc từng ghi lỗi 'xóa folder chứa autoreply dạng "
            "keyword thì trong tbl keyword vẫn còn' ⇒ đây là điểm ĐÃ TỪNG LỖI"),

    tc("Folder — xóa & cascade", "FUNC-UNIQ-001", "Normal",
       "Sau khi xóa folder chứa keyword「keyC」→ tạo lại auto reply mới với chính keyword「keyC」⇒ thêm thành công",
       BOT + "\n- Vừa xóa folder chứa quy tắc có keyword「keyC」ở TC trước",
       "1. Click「新規作成」\n2. Chọn「設定したキーワードに反応」, nhập keyword「keyC」\n3. Lưu\n"
       "4. Query: SELECT * FROM keyword WHERE keyword='keyC'",
       "Keyword「keyC」",
       "- Lưu thành công, KHÔNG báo「キーワードは既に登録されています。」\n"
       "- Bảng keyword có 1 bản ghi mới「keyC」gắn với auto_reply_id mới",
       note="Nguồn: Ver1.0 r48. Đây là cặp TC bắt buộc đi kèm TC xóa folder — chứng minh keyword đã được giải phóng"),

    tc("Folder — xóa & cascade", "DATA-REF-001", "Normal",
       "Xóa folder → các quy tắc bên trong không còn hiển thị ở bất kỳ folder nào (không rơi về 未分類)",
       BOT2 + "\n- Folder B chứa 2 quy tắc",
       "1. Xóa folder B\n2. Mở folder 未分類 và các folder còn lại\n3. Query: SELECT id, category_id, is_deleted "
       "FROM auto_reply WHERE category_id=<B>",
       "2 quy tắc trong folder B",
       "- 2 quy tắc KHÔNG xuất hiện ở 未分類 hay folder khác\n- DB: is_deleted=1, category_id giữ nguyên id folder đã xóa\n"
       "- Số đếm của 未分類 KHÔNG tăng",
       note="Suy luận từ BR-07 (cascade soft delete) — corpus không nói rõ quy tắc có rơi về 未分類 không. "
            "ĐÂY LÀ SUY LUẬN CỦA AI, CẦN LEADER XÁC NHẬN (MT-16)"),

    tc("Folder — xóa & cascade", "DATA-REF-001", "Normal",
       "recover bảng category: chạy lệnh recover ⇒ với kind=1 (auto reply), xóa bản ghi auto_reply map theo category_id đã xóa",
       "- Bot có folder auto reply đã bị xóa (category kind=1, is_deleted=1)\n- Còn bản ghi auto_reply map theo category_id đó",
       "1. Query trước: SELECT * FROM auto_reply WHERE category_id IN (SELECT id FROM category WHERE kind=1 AND is_deleted=1)\n"
       "2. Dev chạy lệnh recover bảng category\n3. Query lại đúng câu trên",
       "kind = 1 → autoreply; category_id ví dụ id 3814",
       "- Sau recover: các bản ghi auto_reply map theo category_id đã xóa được dọn đúng theo quy tắc recover\n"
       "- KHÔNG ảnh hưởng auto_reply thuộc folder còn sống",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="RULE-08: lệnh recover chạy trên môi trường thật. Nguồn: Improve chung / recover bảng category r4. "
            "Spec §7 KHÔNG mô tả job/command recover này ⇒ MT-17"),

    # ═══════════════ Folder — điều hướng & sắp xếp ═══════════════
    tc("Folder — điều hướng & sắp xếp", "STATE-001", "Normal",
       "Bug KH #38369: đổi tên folder ĐANG MỞ → sau khi lưu vẫn ở đúng folder vừa sửa",
       BOT2 + "\n- Đang mở folder A (không phải 未分類)",
       "1. Mở folder A\n2. Đổi tên folder A → lưu\n3. Quan sát folder đang active ở sidebar và danh sách bên phải",
       "Tên mới:「対応A-rename」",
       "- Sau khi lưu vẫn ở folder A (tên mới), sidebar highlight đúng folder A\n"
       "- Danh sách bên phải là quy tắc của folder A, KHÔNG nhảy về「未分類」",
       note="Nguồn: Ver1.0 r114 (Bug KH #38369, 07/2026)"),

    tc("Folder — điều hướng & sắp xếp", "STATE-001", "Normal",
       "Bug KH #38369: vào chế độ 並べ替え rồi Cancel ⇒ quay về đúng folder đang mở trước đó",
       BOT2 + "\n- Đang mở folder A",
       "1. Mở folder A\n2. Click「並べ替え」vào chế độ sắp xếp\n3. Click Cancel\n4. Quan sát folder active + danh sách",
       "—",
       "- Quay về đúng folder A\n- Danh sách hiển thị đúng quy tắc của folder A, KHÔNG nhảy về「未分類」",
       note="Nguồn: Ver1.0 r115"),

    tc("Folder — điều hướng & sắp xếp", "STATE-001", "Normal",
       "Bug KH #38369: đang ở folder A → thêm folder mới ⇒ folder đang mở xử lý đúng spec, không tự nhảy về 未分類",
       BOT2 + "\n- Đang mở folder A",
       "1. Mở folder A\n2. Thêm 1 folder mới (nhập tên → lưu)\n3. Quan sát folder active\n4. Reload trang",
       "Folder mới:「新規F」",
       "- Sau khi thêm: màn KHÔNG tự nhảy về「未分類」\n- Reload: giữ đúng folder đang mở (theo cookie folder_reply)",
       note="Nguồn: Ver1.0 r119. Spec EP-12 /basic/reply/set-cookie lưu folder đang chọn — corpus không ghi rõ "
            "sau khi thêm folder thì active là folder A hay folder mới ⇒ MT-18"),

    tc("Folder — điều hướng & sắp xếp", "STATE-001", "Normal",
       "Sort quy tắc rồi Bật/Tắt quy tắc ⇒ folder đang mở và trạng thái ON/OFF hiển thị đúng",
       BOT2 + "\n- Folder A có ≥3 quy tắc",
       "1. Mở folder A, click「並べ替え」, kéo đổi thứ tự, lưu\n2. Bật/Tắt 1 quy tắc trong folder A\n"
       "3. Quan sát folder active + thứ tự + trạng thái\n4. Reload",
       "Đổi vị trí quy tắc #1 ↔ #3",
       "- Vẫn ở folder A\n- Thứ tự mới được giữ sau reload\n- Trạng thái ON/OFF của quy tắc hiển thị đúng",
       note="Nguồn: Ver1.0 r116"),

    tc("Folder — điều hướng & sắp xếp", "STATE-001", "Normal",
       "Bug KH #38369: OFF quy tắc rồi F5 ⇒ folder đang mở và trạng thái rule hiển thị đúng",
       BOT2 + "\n- Đang mở folder A, có 1 quy tắc đang ON",
       "1. Mở folder A\n2. OFF 1 quy tắc\n3. Nhấn F5 reload trang\n4. Quan sát folder active + trạng thái quy tắc",
       "—",
       "- Sau F5 vẫn ở folder A\n- Quy tắc hiển thị OFF (is_stopped=1)",
       note="Nguồn: Ver1.0 r113"),

    tc("Folder — điều hướng & sắp xếp", "FUNC-001", "Normal",
       "sortFolder: kéo đổi thứ tự folder rồi lưu ⇒ thứ tự mới được giữ sau reload",
       BOT2 + "\n- Có ≥3 folder tự tạo",
       "1. Vào chế độ sắp xếp folder\n2. Kéo đổi thứ tự 2 folder\n3. Lưu\n4. Reload trang\n"
       "5. Query position của các folder trong bảng category (kind=1)",
       "Đổi vị trí folder A ↔ folder C",
       "- Sidebar hiện thứ tự mới\n- DB: category.position cập nhật đúng\n- Sau reload thứ tự giữ nguyên",
       spec="Spec không ghi",
       note="EP-06 action sortFolder có trong spec §6 nhưng KHÔNG có BR mô tả. Corpus KHÔNG có TC sort folder "
            "cho màn auto reply ⇒ TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    # ═══════════════ Bật/Tắt quy tắc ═══════════════
    tc("Bật/Tắt quy tắc", "STATE-001", "Normal",
       "Bug KH #38369: OFF quy tắc trong folder TỰ TẠO ⇒ is_stopped=1 và màn KHÔNG nhảy sang folder khác",
       BOT2 + "\n- Folder A có 1 quy tắc đang ON",
       "1. Mở folder A\n2. Gạt switch của quy tắc về OFF\n3. Quan sát folder đang mở ngay sau khi nhấn\n"
       "4. Reload danh sách\n5. Query: SELECT is_stopped FROM auto_reply WHERE id=<rule>",
       "1 quy tắc đang ON trong folder A",
       "- Ngay sau khi nhấn OFF: vẫn ở màn folder A\n- Sau reload vẫn ở folder A, KHÔNG nhảy sang「未分類」\n"
       "- DB: is_stopped = 1",
       note="Nguồn: Ver1.0 r108-r109 (Bug KH #38369 [01-07-2026][T11423]). Hiện tượng gốc: sau khi nhấn OFF màn "
            "tự nhảy về folder default"),

    tc("Bật/Tắt quy tắc", "STATE-001", "Normal",
       "turnOnItem: ON quy tắc trong folder tự tạo ⇒ is_stopped=0 và màn không nhảy folder",
       BOT2 + "\n- Folder A có 1 quy tắc đang OFF",
       "1. Mở folder A\n2. Gạt switch về ON\n3. Quan sát folder đang mở\n4. Reload\n"
       "5. Query is_stopped",
       "1 quy tắc đang OFF trong folder A",
       "- Vẫn ở folder A cả trước và sau reload\n- DB: is_stopped = 0\n- Cột「稼働状況」hiện ON",
       note="Nguồn: Ver1.0 r110"),

    tc("Bật/Tắt quy tắc", "STATE-001", "Normal",
       "ON/OFF quy tắc trong folder 未分類 ⇒ vẫn ở folder mặc định, trạng thái đúng",
       BOT + "\n- Folder 未分類 (category_id=0) có ≥1 quy tắc",
       "1. Mở folder「未分類」\n2. OFF 1 quy tắc → quan sát\n3. ON lại quy tắc đó → quan sát\n"
       "4. Query is_stopped sau mỗi lần",
       "Quy tắc thuộc category_id = 0",
       "- Cả 2 lần thao tác đều ở lại folder「未分類」\n- is_stopped chuyển 0→1→0 đúng theo thao tác",
       note="Boundary quan trọng: category_id=0 là convention (BR-14), không có record trong bảng category. "
            "Nguồn: Ver1.0 r117-r118"),

    tc("Bật/Tắt quy tắc", "CONC-001", "Abnormal",
       "ON/OFF nhiều quy tắc liên tiếp trong cùng folder ⇒ không lần nào bị chuyển folder, trạng thái cuối đúng",
       BOT2 + "\n- Folder A có ≥3 quy tắc",
       "1. Mở folder A\n2. ON/OFF liên tục ≥6 lần trên 3 quy tắc khác nhau (không chờ response)\n"
       "3. Reload trang\n4. Query is_stopped của cả 3 quy tắc",
       "Chuỗi thao tác: OFF#1, OFF#2, ON#1, OFF#3, ON#2, ON#3",
       "- KHÔNG lần nào bị chuyển sang folder khác\n"
       "- Sau reload: is_stopped của 3 quy tắc khớp đúng trạng thái thao tác cuối cùng của từng quy tắc",
       note="Chuỗi thao tác liên tiếp nên giữ chung 1 TC. Nguồn: Ver1.0 r112"),

    tc("Bật/Tắt quy tắc", "STATE-001", "Normal",
       "Folder có NHIỀU quy tắc: OFF 1 quy tắc ⇒ chỉ quy tắc đó đổi trạng thái, các quy tắc khác giữ nguyên",
       BOT2 + "\n- Folder A có ≥3 quy tắc, tất cả đang ON",
       "1. Mở folder A\n2. OFF quy tắc thứ 2\n3. Reload\n4. Query is_stopped của cả 3 quy tắc",
       "3 quy tắc trong folder A",
       "- Chỉ quy tắc thứ 2 có is_stopped=1\n- 2 quy tắc còn lại vẫn is_stopped=0\n- Vẫn ở folder A sau reload",
       note="Nguồn: Ver1.0 r111"),

    tc("Bật/Tắt quy tắc", "OUT-TRUTH-001", "Normal",
       "Sau khi ON/OFF: kiểm tra hiệu lực thật phía LINE — quy tắc OFF không gửi action, quy tắc ON gửi bình thường",
       BOT + "\n- 1 quy tắc keyword「テスト」có action gửi text\n- 1 friend LINE đã kết bạn với bot A",
       "1. Đặt quy tắc = ON, friend gửi「テスト」→ quan sát LINE app\n2. OFF quy tắc, friend gửi「テスト」lần 2 → quan sát\n"
       "3. ON lại, friend gửi lần 3 → quan sát",
       "Keyword「テスト」, action gửi text「こんにちは」",
       "- Lần 1 (ON): friend nhận được「こんにちは」trên LINE app\n"
       "- Lần 2 (OFF): friend KHÔNG nhận được tin nào\n- Lần 3 (ON): nhận lại bình thường",
       env="PRODUCTION",
       note="RULE-06 đi tới output cuối trên LINE app. Nguồn: Ver1.0 r120 'Check send auto reply được bình thường'. "
            "Job runtime lọc is_stopped!=1 (BR runtime)"),

    # ═══════════════ Sắp xếp & chuyển folder quy tắc ═══════════════
    tc("Sắp xếp & chuyển folder quy tắc", "FUNC-001", "Normal",
       "sortItem: kéo đổi thứ tự quy tắc trong folder ⇒ auto_reply.position cập nhật, thứ tự giữ sau reload",
       BOT2 + "\n- Folder A có ≥3 quy tắc",
       "1. Mở folder A, click「並べ替え」\n2. Kéo quy tắc cuối lên đầu\n3. Lưu\n4. Reload\n"
       "5. Query: SELECT id, position FROM auto_reply WHERE category_id=<A> AND is_deleted=0 ORDER BY position DESC",
       "3 quy tắc, đổi vị trí #3 lên #1",
       "- Danh sách hiện thứ tự mới\n- DB: position của các quy tắc cập nhật đúng\n- Sau reload giữ nguyên thứ tự",
       spec="Spec không ghi",
       note="BR-05 (position, sort theo position DESC) + EP-06 action sortItem. Corpus KHÔNG có TC sort quy tắc "
            "⇒ TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Sắp xếp & chuyển folder quy tắc", "BULK-001", "Normal",
       "moveItem 一括フォルダ変更: chọn nhiều quy tắc → chuyển sang folder khác ⇒ category_id cập nhật, số đếm 2 folder đổi đúng",
       BOT2 + "\n- Folder A có 3 quy tắc, folder B có 0 quy tắc",
       "1. Mở folder A, tick checkbox 2 quy tắc\n2. Click「一括フォルダ変更」, chọn folder B\n3. Xác nhận\n"
       "4. Quan sát số đếm ở sidebar\n5. Query category_id của 2 quy tắc",
       "Chuyển 2/3 quy tắc từ A sang B",
       "- Sidebar: A còn (1), B thành (2)\n- DB: category_id của 2 quy tắc = id folder B\n"
       "- Mở folder B thấy đúng 2 quy tắc đã chuyển",
       spec="Spec không ghi",
       note="EP-06 action moveItem. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Sắp xếp & chuyển folder quy tắc", "BULK-001", "Boundary",
       "一括フォルダ変更 khi KHÔNG chọn quy tắc nào ⇒ báo lỗi / không cho thao tác, không đổi dữ liệu",
       BOT2,
       "1. Mở folder A, KHÔNG tick checkbox nào\n2. Click「一括フォルダ変更」\n3. Query category_id của các quy tắc trong A",
       "0 quy tắc được chọn",
       "- Hệ thống chặn thao tác (nút disabled hoặc báo lỗi chọn ít nhất 1 mục)\n"
       "- KHÔNG có bản ghi auto_reply nào bị đổi category_id",
       spec="Spec không ghi",
       note="TC biên do AI viết theo UI-INPUT — spec không mô tả hành vi khi bỏ trống lựa chọn. CẦN LEADER XÁC NHẬN"),

    # ═══════════════ Xóa quy tắc & xóa hàng loạt ═══════════════
    tc("Xóa quy tắc & xóa hàng loạt", "DATA-REF-001", "Normal",
       "deleteItem: xóa 1 quy tắc dạng keyword ⇒ auto_reply soft delete + keyword HARD delete",
       BOT + "\n- Có 1 quy tắc dạng keyword「keyC」",
       "1. Query trước: SELECT * FROM keyword WHERE keyword='keyC'\n2. Click nút xóa của quy tắc, xác nhận\n"
       "3. Query lại: SELECT is_deleted FROM auto_reply WHERE id=<rule>; SELECT * FROM keyword WHERE keyword='keyC'",
       "Keyword「keyC」",
       "- auto_reply.is_deleted = 1\n- Bảng keyword: bản ghi「keyC」bị XÓA HẲN (0 dòng)\n"
       "- Quy tắc biến mất khỏi danh sách",
       note="BR-04. Nguồn: Ver1.0 r43. ListBug file gốc từng ghi lỗi 'xóa autoreply dạng keyword thì trong tbl "
            "keyword vẫn còn' ⇒ điểm ĐÃ TỪNG LỖI"),

    tc("Xóa quy tắc & xóa hàng loạt", "FUNC-UNIQ-001", "Normal",
       "Sau khi xóa quy tắc chứa keyword「keyC」→ tạo mới quy tắc với chính「keyC」⇒ thêm thành công",
       BOT + "\n- Vừa xóa quy tắc chứa keyword「keyC」",
       "1. Click「新規作成」\n2. Chọn「設定したキーワードに反応」, nhập「keyC」\n3. Lưu\n"
       "4. Query: SELECT * FROM keyword WHERE keyword='keyC'",
       "Keyword「keyC」",
       "- Lưu thành công, KHÔNG báo「キーワードは既に登録されています。」\n- Bảng keyword có 1 bản ghi mới「keyC」",
       note="Nguồn: Ver1.0 r44"),

    tc("Xóa quy tắc & xóa hàng loạt", "BULK-001", "Normal",
       "deleteItems 一括削除: chọn nhiều quy tắc dạng keyword → xóa hàng loạt ⇒ soft delete auto_reply + hard delete toàn bộ keyword",
       BOT + "\n- Có 3 quy tắc dạng keyword: keyC1, keyC2, keyC3",
       "1. Tick checkbox 3 quy tắc\n2. Click「一括削除」, xác nhận\n"
       "3. Query: SELECT id, is_deleted FROM auto_reply WHERE id IN (...); SELECT * FROM keyword WHERE keyword IN ('keyC1','keyC2','keyC3')",
       "3 keyword: keyC1, keyC2, keyC3",
       "- Cả 3 auto_reply có is_deleted = 1\n- Bảng keyword: KHÔNG còn dòng nào cho 3 keyword trên (hard delete)\n"
       "- Cả 3 quy tắc biến mất khỏi danh sách",
       note="Nguồn: Ver1.0 r45"),

    tc("Xóa quy tắc & xóa hàng loạt", "FUNC-UNIQ-001", "Normal",
       "Sau xóa hàng loạt → tạo lại quy tắc với keyword vừa xóa ⇒ thêm thành công",
       BOT + "\n- Vừa xóa hàng loạt các quy tắc chứa keyC1/keyC2/keyC3",
       "1. Tạo quy tắc mới với keyword「keyC1」\n2. Lưu\n3. Query bảng keyword",
       "Keyword「keyC1」",
       "- Lưu thành công, không báo trùng\n- Bảng keyword có bản ghi mới「keyC1」",
       note="Nguồn: Ver1.0 r46"),

    tc("Xóa quy tắc & xóa hàng loạt", "DATA-REF-001", "Normal",
       "1 quy tắc có NHIỀU keyword → xóa bớt 1 keyword trong form edit ⇒ chỉ keyword đó bị xóa khỏi bảng",
       BOT + "\n- 1 quy tắc dạng keyword có 3 keyword: k1, k2, k3",
       "1. Mở edit quy tắc\n2. Xóa dòng keyword「k2」\n3. Lưu\n"
       "4. Query: SELECT keyword FROM keyword WHERE auto_reply_id=<rule>",
       "3 keyword k1/k2/k3, xóa k2",
       "- Bảng keyword còn đúng 2 dòng: k1 và k3\n- k2 bị xóa hẳn\n- Màn list hiện keyword còn lại",
       note="Nguồn: Ver1.0 r49. Spec: EP-08 xóa keyword bị gỡ bằng whereNotIn"),

    tc("Xóa quy tắc & xóa hàng loạt", "SEC-ISO-001", "Normal",
       "2 bot cùng có keyword giống nhau: bot A chuyển quy tắc sang loại 全てのメッセージ ⇒ chỉ xóa keyword của bot A",
       "- Bot A và bot B đều có quy tắc dạng keyword với cùng chuỗi「共通キー」",
       "1. Query trước: SELECT k.* FROM keyword k JOIN auto_reply a ON k.auto_reply_id=a.id WHERE k.keyword='共通キー'\n"
       "2. Ở bot A: edit quy tắc, đổi 利用設定 sang「全てのメッセージに反応」, lưu\n3. Query lại đúng câu trên",
       "Keyword「共通キー」tồn tại ở cả bot A và bot B",
       "- Bảng keyword chỉ còn bản ghi thuộc auto_reply của BOT B\n- Bản ghi của bot A bị xóa\n"
       "- Quy tắc của bot B vẫn hoạt động bình thường phía LINE",
       note="BR-01 unique theo bot. Nguồn: Ver1.0 r50"),

    tc("Xóa quy tắc & xóa hàng loạt", "STATE-001", "Abnormal",
       "Xác nhận trước khi xóa: click nút xóa quy tắc rồi chọn Hủy ⇒ quy tắc KHÔNG bị xóa",
       BOT + "\n- Có ≥1 quy tắc",
       "1. Click nút xóa của 1 quy tắc\n2. Ở dialog xác nhận chọn Hủy/キャンセル\n"
       "3. Reload\n4. Query is_deleted của quy tắc đó",
       "—",
       "- Dialog xác nhận có hiện\n- Sau khi Hủy: quy tắc vẫn còn trong danh sách\n- DB: is_deleted = 0",
       spec="Spec không ghi",
       note="Gap #17 của spec: 'Xác nhận trước khi xóa (confirm dialog) — suy luận có confirm nhưng chưa quan sát được'. "
            "TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Xóa quy tắc & xóa hàng loạt", "BULK-001", "Abnormal",
       "一括削除 khi KHÔNG chọn quy tắc nào ⇒ bị chặn, không xóa nhầm bản ghi",
       BOT2 + "\n- Folder A có 3 quy tắc",
       "1. Mở folder A, KHÔNG tick checkbox nào\n2. Click「一括削除」\n"
       "3. Query: SELECT COUNT(*) FROM auto_reply WHERE category_id=<A> AND is_deleted=0",
       "0 quy tắc được chọn",
       "- Hệ thống chặn thao tác (nút disabled hoặc báo lỗi chọn ít nhất 1 mục)\n"
       "- COUNT vẫn = 3, KHÔNG bản ghi nào bị soft delete",
       spec="Spec không ghi",
       note="TC biên do AI viết — spec không mô tả hành vi khi bỏ trống lựa chọn ở thao tác hàng loạt. "
            "CẦN LEADER XÁC NHẬN"),

    tc("Xóa quy tắc & xóa hàng loạt", "BULK-001", "Normal",
       "一括削除: checkbox header『chọn tất cả』⇒ tick/bỏ tick đồng loạt, xóa đúng số bản ghi đã chọn",
       BOT2 + "\n- Folder A có 3 quy tắc",
       "1. Mở folder A, tick checkbox ở HEADER bảng\n2. Quan sát 3 checkbox của 3 dòng\n"
       "3. Bỏ tick header → quan sát\n4. Tick lại header, click「一括削除」, xác nhận\n"
       "5. Query auto_reply của folder A",
       "3 quy tắc trong folder A",
       "- Tick header: cả 3 dòng được tick\n- Bỏ tick header: cả 3 dòng bỏ tick\n"
       "- Sau xóa: cả 3 quy tắc có is_deleted = 1, danh sách trống, sidebar hiện (0)",
       spec="Spec không ghi",
       note="Checkbox『chọn tất cả』có trong ui-spec.md §Bảng dữ liệu cột #1. Corpus KHÔNG có TC ⇒ "
            "TC lấp GAP do AI viết"),

    tc("Xóa quy tắc & xóa hàng loạt", "DATA-COUNT-001", "Normal",
       "Sau khi xóa quy tắc ⇒ số đếm quy tắc ở sidebar folder giảm đúng",
       BOT2 + "\n- Folder A có 3 quy tắc (sidebar hiện「(3)」)",
       "1. Ghi lại số đếm của folder A ở sidebar\n2. Xóa 1 quy tắc\n3. Đọc lại số đếm ở sidebar\n"
       "4. Reload trang, đọc lại số đếm\n"
       "5. Query: SELECT COUNT(*) FROM auto_reply WHERE category_id=<A> AND is_deleted=0",
       "3 quy tắc → xóa 1 → kỳ vọng còn 2",
       "- Sidebar folder A chuyển từ「(3)」sang「(2)」ngay sau khi xóa\n"
       "- Sau reload vẫn hiện「(2)」\n- COUNT trong DB = 2 (khớp số hiển thị)",
       note="Field #21 Traceability (COUNT auto_reply WHERE category_id=X AND is_deleted=0). "
            "Corpus KHÔNG có TC bộ đếm ⇒ TC lấp GAP do AI viết"),

    tc("Màn list — hiển thị & cột", "DATA-REF-001", "Abnormal",
       "Quy tắc thuộc folder ĐÃ XÓA ⇒ không hiện ở bất kỳ folder nào, không làm sai số đếm 未分類",
       BOT2 + "\n- Đã xóa folder B (trước đó chứa 2 quy tắc)",
       "1. Ghi lại số đếm của「未分類」trước khi xóa folder B\n2. Xóa folder B\n"
       "3. Mở lần lượt「未分類」và các folder còn lại, đếm số quy tắc hiển thị\n"
       "4. So sánh số đếm「未分類」trước và sau",
       "Folder B chứa 2 quy tắc, bị xóa",
       "- 2 quy tắc của folder B KHÔNG hiện ở folder nào\n"
       "- Số đếm của「未分類」KHÔNG thay đổi so với trước khi xóa",
       note="Gắn MT-16 (quy tắc trong folder bị xóa đi đâu). TC do AI viết bổ sung cho nhóm màn list"),

    # ═══════════════ Tìm kiếm quy tắc ═══════════════
    tc("Tìm kiếm quy tắc", "LIST-001", "Normal",
       "searchByKeyWord: nhập từ khóa vào ô tìm kiếm ⇒ chỉ hiện quy tắc có keyword LIKE %từ khóa%, trong đúng folder đang mở",
       BOT2 + "\n- Folder A có 3 quy tắc: keyword「予約」,「予約変更」,「キャンセル」",
       "1. Mở folder A\n2. Nhập「予約」vào ô tìm kiếm\n3. Thực hiện tìm\n4. Xóa từ khóa / reload",
       "Từ khóa tìm:「予約」",
       "- Kết quả hiện 2 quy tắc:「予約」và「予約変更」\n- KHÔNG hiện「キャンセル」\n"
       "- Kết quả giới hạn trong folder A (không lẫn quy tắc folder khác)\n- Sau khi xóa từ khóa: hiện lại đủ 3 quy tắc",
       spec="Spec không ghi",
       note="EP-06 action searchByKeyWord tồn tại trong code (feature-spec §6) nhưng ui-spec.md §SCR-RPL-01 KHÔNG "
            "liệt kê ô tìm kiếm (Gap TB-03). Corpus TCs KHÔNG có TC search ⇒ MT-06. "
            "TC do AI viết theo code, CẦN LEADER XÁC NHẬN ô tìm kiếm có tồn tại trên UI không"),

    tc("Tìm kiếm quy tắc", "LIST-001", "Abnormal",
       "searchByKeyWord: tìm từ khóa không tồn tại ⇒ hiện 0 kết quả, không lỗi",
       BOT2,
       "1. Mở folder A\n2. Nhập chuỗi không tồn tại「zzzzz」\n3. Tìm",
       "Từ khóa:「zzzzz」",
       "- Danh sách hiện 0 dòng (empty state)\n- Không lỗi JS, không trắng màn",
       spec="Spec không ghi",
       note="Gắn với MT-06. TC do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Tìm kiếm quy tắc", "LIST-001", "Boundary",
       "searchByKeyWord: quy tắc dạng 全てのメッセージ (không có bản ghi keyword) ⇒ không xuất hiện trong kết quả tìm theo keyword",
       BOT + "\n- Folder A có 1 quy tắc 全てのメッセージ và 1 quy tắc keyword「予約」",
       "1. Mở folder A\n2. Tìm với từ khóa「予」\n3. Đối chiếu kết quả với DB (auto_reply JOIN keyword)",
       "Từ khóa:「予」",
       "- Chỉ hiện quy tắc keyword「予約」\n- Quy tắc 全てのメッセージ KHÔNG hiện (do query JOIN keyword)",
       spec="Spec không ghi",
       note="Suy luận từ pseudo-code 'SELECT auto_reply JOIN keyword' — INNER JOIN sẽ loại quy tắc không có keyword. "
            "ĐÂY LÀ SUY LUẬN CỦA AI, gắn MT-06, CẦN LEADER XÁC NHẬN"),
]
