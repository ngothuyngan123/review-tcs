# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 1-9: Folder · Màn list · Tìm kiếm · CRUD scenario.

Nguồn chính: 04. TCsLine_Scenario / tab「Testcase」(master, 4/2024 → 06/2026).
Bổ sung: TCsLine_Improve chung / tab「#35968」(06/2026 sort) và「Test bug folder all màn」(#32468, 04/2026).
"""
from _common import tc

BOT = "- Đăng nhập admin (主管理者), bot A đang active, màn /basic/scenario"
BOT8 = ("- Bot A có ≥ 1 folder scenario và ≥ 1 scenario\n"
        "- Có sẵn dữ liệu để mở 8 điểm tham chiếu folder scenario: Chat 1:1 · Modal action "
        "(chat 1:1 / booking) · Message send all · Button (3-3) · Scenario · Remind (5-3) · "
        "Calendar 5-1 (設定 > 予約設定 > 設定する) · Bill tiền item 6 (単品商品 > テスト環境 > 商品編集 > アクション設定)")

S1 = [
    # ══════════════════════ 1. Folder scenario ══════════════════════
    tc("Folder scenario", "FUNC-001", "Normal",
       "Tạo folder tên 1–15 ký tự (latinh / JP full-width / half-width katakana) → INSERT category kind=11",
       BOT + "\n- Chưa tồn tại folder tên「キャンペーン」/「Folder-01」/「ｷｬﾝﾍﾟｰﾝ」",
       "1. Click「フォルダ追加」\n2. Nhập tên folder\n3. Click lưu\n4. Reload /basic/scenario\n"
       "5. Query `category` WHERE bot_id = A AND kind = 11 ORDER BY id DESC",
       "Lần 1:「キャンペーン」(JP full-width)\nLần 2:「Folder-01」(latinh + số + gạch)\n"
       "Lần 3:「ｷｬﾝﾍﾟｰﾝ」(half-width katakana)\nLần 4: đúng 15 ký tự「あいうえおかきくけこさしすせそ」",
       "- Cả 4 folder tạo thành công, folder MỚI NHẤT nằm ở CUỐI danh sách folder bên trái\n"
       "- DB `category`: có bản ghi mới với bot_id = A, kind = 11, name lưu verbatim (không mojibake)\n"
       "- Sau reload folder còn nguyên, tên hiển thị đúng",
       note="4 input cùng 1 kết quả → giữ chung 1 TC. Nguồn: r104"),

    tc("Folder scenario", "FUNC-UNIQ-001", "Normal",
       "Tạo folder TRÙNG TÊN folder đã có → vẫn tạo thành công (folder scenario KHÔNG unique)",
       BOT + "\n- Đã có folder tên「テスト」",
       "1. Click「フォルダ追加」\n2. Nhập đúng「テスト」\n3. Click lưu\n4. Query `category` WHERE bot_id = A AND kind = 11 AND name = 'テスト'",
       "「テスト」(trùng hoàn toàn folder đã có)",
       "- Tạo thành công, KHÔNG có message lỗi trùng tên\n"
       "- Danh sách folder có 2 dòng cùng tên「テスト」, cái mới ở cuối\n"
       "- DB: 2 bản ghi category khác id, cùng name",
       note="Khác với folder tag (có check trùng). Nguồn: r105"),

    tc("Folder scenario", "DATA-INPUT-001", "Boundary",
       "Tạo folder nhập 16 ký tự → báo lỗi フォルダ名は15文字以内で入力してください。",
       BOT,
       "1. Click「フォルダ追加」\n2. Nhập 16 ký tự\n3. Click lưu\n4. Query `category` kiểm tra không có bản ghi mới",
       "16 ký tự:「あいうえおかきくけこさしすせそた」",
       "- Hiển thị message lỗi 「フォルダ名は15文字以内で入力してください。」\n"
       "- Popup KHÔNG đóng, folder KHÔNG được tạo\n- DB: không có bản ghi category mới",
       note="Nguồn: r115"),

    tc("Folder scenario", "DATA-INPUT-001", "Abnormal",
       "Tạo folder để trống tên → báo lỗi フォルダ名を入力して下さい",
       BOT,
       "1. Click「フォルダ追加」\n2. Không nhập gì\n3. Click lưu",
       "(để trống)",
       "- Hiển thị message lỗi 「フォルダ名を入力して下さい」\n- Popup KHÔNG đóng, folder KHÔNG được tạo",
       note="Nguồn: r116"),

    tc("Folder scenario", "STATE-CLEAN-001", "Normal",
       "Sau khi tạo folder FAIL, nhập lại giá trị hợp lệ → tạo thành công (không kẹt trạng thái lỗi)",
       BOT,
       "1. Click「フォルダ追加」→ nhập 16 ký tự → lưu → thấy lỗi\n2. Xoá bớt còn 10 ký tự\n3. Click lưu\n4. Kiểm tra danh sách folder",
       "Lần 1: 16 ký tự → lỗi\nLần 2:「テストフォルダ」(7 ký tự)",
       "- Message lỗi biến mất\n- Folder「テストフォルダ」tạo thành công, nằm cuối danh sách\n- DB: có bản ghi category mới",
       note="Nguồn: r117"),

    tc("Folder scenario", "CONC-001", "Abnormal",
       "Double click nhanh button「フォルダ追加」và button lưu → chỉ tạo ĐÚNG 1 bản ghi folder",
       BOT,
       "1. Double click nhanh button「フォルダ追加」\n2. Nhập tên hợp lệ\n3. Double click nhanh button lưu\n"
       "4. Query `category` WHERE bot_id = A AND kind = 11 AND name = '<tên vừa nhập>'",
       "Tên folder:「二重クリック」",
       "- Bước 1 chỉ mở ĐÚNG 1 popup tạo folder\n- Bước 3 chỉ tạo ĐÚNG 1 bản ghi\n"
       "- DB: COUNT(*) = 1, không duplicate",
       note="Nguồn: r103, r120"),

    tc("Folder scenario", "STATE-CLEAN-001", "Normal",
       "Click キャンセル ở popup tạo folder → đóng popup, không tạo folder",
       BOT,
       "1. Click「フォルダ追加」\n2. Nhập tên「キャンセルテスト」\n3. Click「キャンセル」\n4. Kiểm tra danh sách folder + DB",
       "「キャンセルテスト」",
       "- Popup đóng lại\n- Danh sách folder KHÔNG có「キャンセルテスト」\n- DB: không có bản ghi category mới",
       note="Nguồn: r119"),

    tc("Folder scenario", "REG-SHARED-001", "Normal",
       "Folder scenario vừa tạo hiển thị đủ ở 8 điểm tham chiếu khác",
       BOT8 + "\n- Vừa tạo folder scenario mới tên「新フォルダ」",
       "1. Tạo folder scenario「新フォルダ」\n2. Lần lượt mở 8 điểm tham chiếu, mở dropdown/modal chọn scenario\n"
       "3. Kiểm tra danh sách folder trong mỗi điểm",
       "8 điểm: (1) Chat 1:1 · (2) Modal action (chat 1:1, booking) · (3) Message send all · (4) Button · "
       "(5) Scenario · (6) Remind · (7) Calendar 5-1 · (8) Bill tiền item 6",
       "- Cả 8 điểm đều hiển thị folder「新フォルダ」trong danh sách folder scenario\n- Tên folder đúng, vị trí đúng (cuối danh sách)",
       note="8 điểm cùng 1 kết quả → giữ chung 1 TC. Nguồn: r107-r114"),

    tc("Folder scenario", "FUNC-002", "Normal",
       "Đổi tên folder thành 1–15 ký tự → tên đổi, id folder giữ nguyên",
       BOT + "\n- Có folder「旧名前」đang chứa 2 scenario",
       "1. Hover folder「旧名前」→ click icon 3 chấm →「フォルダ名変更」\n2. Nhập tên mới\n3. Click lưu\n"
       "4. Query `category` WHERE id = <id folder>",
       "Tên mới:「新名前2026」(9 ký tự)",
       "- Danh sách folder hiển thị「新名前2026」\n- DB: category.name = '新名前2026', **id KHÔNG đổi**\n"
       "- 2 scenario bên trong vẫn còn nguyên (scenario.group_id không đổi)",
       note="Nguồn: r154"),

    tc("Folder scenario", "FUNC-UNIQ-001", "Normal",
       "Đổi tên folder thành TÊN TRÙNG folder khác → vẫn success",
       BOT + "\n- Có 2 folder「A」và「B」",
       "1. Đổi tên folder「B」thành「A」\n2. Click lưu\n3. Kiểm tra danh sách folder",
       "Tên mới:「A」(trùng folder đang có)",
       "- Đổi tên thành công, không báo lỗi trùng\n- Danh sách có 2 folder cùng tên「A」",
       note="Nguồn: r155"),

    tc("Folder scenario", "DATA-INPUT-001", "Boundary",
       "Đổi tên folder nhập > 15 ký tự hoặc để trống → validate, không lưu",
       BOT + "\n- Có folder「旧名前」",
       "1. Mở popup đổi tên folder\n2. Lần 1: nhập 16 ký tự → lưu\n3. Lần 2: xoá trắng → lưu\n4. Kiểm tra tên folder ngoài danh sách",
       "Lần 1: 16 ký tự\nLần 2: (để trống)",
       "- Cả 2 lần đều hiển thị message validate, popup không đóng\n- Tên folder ngoài danh sách vẫn là「旧名前」",
       note="2 input cùng kết quả (đều validate) → giữ chung. Nguồn: r165, r166"),

    tc("Folder scenario", "STATE-CLEAN-001", "Normal",
       "Nhập tên hợp lệ ở popup đổi tên nhưng KHÔNG lưu → tên folder giữ nguyên",
       BOT + "\n- Có folder「旧名前」",
       "1. Mở popup đổi tên folder, nhập「新名前」\n2. Đóng popup bằng dấu X (không bấm lưu)\n3. Kiểm tra danh sách folder",
       "「新名前」",
       "- Danh sách folder vẫn hiển thị「旧名前」\n- DB: category.name không đổi",
       note="Nguồn: r164"),

    tc("Folder scenario", "CONC-001", "Abnormal",
       "Double click button Lưu ở popup đổi tên → chỉ ghi nhận 1 lần",
       BOT + "\n- Có folder「旧名前」",
       "1. Mở popup đổi tên, nhập「新名前」\n2. Double click nhanh button Lưu\n3. Kiểm tra danh sách folder + DB",
       "「新名前」",
       "- Chỉ đổi tên 1 lần, popup đóng\n- DB: 1 bản ghi category, name = '新名前', không tạo bản ghi thừa",
       note="Nguồn: r152"),

    tc("Folder scenario", "UI-002", "Normal",
       "Icon 3 chấm chỉ hiện ở folder ĐÃ ADD và đang focus; hover hiện 2 mục (đổi tên / xoá)",
       BOT + "\n- Có folder mặc định 未分類 và ≥ 2 folder do user tạo",
       "1. Hover lần lượt vào folder 未分類 và các folder do user tạo\n2. Quan sát icon 3 chấm\n3. Hover vào icon 3 chấm của folder đang focus",
       "—",
       "- Folder 未分類: KHÔNG hiện icon 3 chấm\n- Chỉ folder do user tạo VÀ đang focus mới hiện icon 3 chấm\n"
       "- Hover icon 3 chấm → hiện popup 2 mục:「フォルダ名変更」và「フォルダ削除」",
       note="Nguồn: r151"),

    tc("Folder scenario", "REG-SHARED-001", "Normal",
       "Đổi tên folder scenario → 8 điểm tham chiếu đều hiển thị tên mới",
       BOT8 + "\n- Đã đổi tên folder scenario từ「旧名前」sang「新名前」",
       "1. Đổi tên folder scenario\n2. Lần lượt mở 8 điểm tham chiếu\n3. Kiểm tra tên folder hiển thị",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Cả 8 điểm hiển thị「新名前」, không còn「旧名前」",
       note="Nguồn: r156-r163"),

    tc("Folder scenario", "UI-002", "Normal",
       "Xoá folder: hiện popup confirm; double click button đồng ý → chỉ xoá 1 lần",
       BOT + "\n- Có folder「削除対象」KHÔNG chứa scenario nào",
       "1. Hover folder → icon 3 chấm →「フォルダ削除」\n2. Quan sát popup confirm\n3. Double click nhanh button đồng ý xoá\n4. Kiểm tra danh sách folder",
       "Folder「削除対象」",
       "- Bước 2: hiện popup confirm xoá\n- Bước 3: chỉ xoá 1 lần, popup đóng\n"
       "- Danh sách folder không còn「削除対象」\n- DB `category`: bản ghi bị xoá",
       note="Nguồn: r168, r169, r170, r172"),

    tc("Folder scenario", "DATA-CASCADE-001", "Abnormal",
       "Xoá folder ĐANG CHỨA scenario → xoá luôn toàn bộ scenario bên trong",
       BOT + "\n- Folder「削除対象」chứa 3 scenario, trong đó 1 scenario đang có friend start",
       "1. Xoá folder「削除対象」→ đồng ý\n2. Kiểm tra danh sách scenario ở tất cả folder\n"
       "3. Query `scenario` WHERE group_id = <id folder>\n4. Query `step_message` / `scenario_step_time` / `scenario_lineuser` của 3 scenario đó",
       "Folder chứa 3 scenario (S1, S2, S3); S3 đang có 5 friend start",
       "- Folder biến mất khỏi danh sách\n- Cả 3 scenario S1/S2/S3 bị xoá khỏi danh sách (không rơi về 未分類)\n"
       "- DB: scenario của folder bị xoá hết",
       spec="Đã hỏi leader",
       note="MT-05 — corpus r174 để『Cần Confirm: Xóa những bảng nào?』; spec BR-08 (feature-spec §7 mục 7) "
            "liệt kê cascade 8 bước cho XOÁ SCENARIO, chưa nói xoá FOLDER có cascade tương đương không. Nguồn: r173, r174"),

    tc("Folder scenario", "REG-SHARED-001", "Normal",
       "Xoá folder scenario → 8 điểm tham chiếu không còn folder đã xoá",
       BOT8 + "\n- Vừa xoá folder scenario「削除対象」",
       "1. Xoá folder scenario\n2. Lần lượt mở 8 điểm tham chiếu\n3. Kiểm tra danh sách folder scenario",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Cả 8 điểm KHÔNG còn folder「削除対象」trong dropdown/modal",
       note="Nguồn: r175-r182"),

    tc("Folder scenario", "STATE-CLEAN-001", "Normal",
       "Popup confirm xoá folder → click Cancel → folder vẫn còn nguyên",
       BOT + "\n- Có folder「削除対象」",
       "1. Mở popup confirm xoá folder\n2. Click Cancel\n3. Kiểm tra danh sách folder + DB",
       "Folder「削除対象」",
       "- Popup đóng, xoá bị huỷ\n- Folder「削除対象」vẫn còn trong danh sách\n- DB: bản ghi category còn nguyên",
       note="Nguồn: r183, r184"),

    tc("Folder scenario", "STATE-001", "Normal",
       "Ẩn folder フォルダを非表示 → chỉ ẩn tạm; reload hoặc vào lại màn scenario thì hiện lại bình thường",
       BOT + "\n- Panel folder đang mở",
       "1. Click icon ẩn folder「フォルダを非表示」→ panel folder đóng\n2. Reload trang /basic/scenario\n"
       "3. Quay lại: vào màn scenario từ menu\n4. Click icon mở lại folder",
       "—",
       "- Bước 1: panel folder đóng lại\n- Bước 2 và 3: panel folder HIỆN LẠI bình thường (trạng thái ẩn không được lưu)\n"
       "- Bước 4: panel folder mở ra",
       note="Nguồn: r147-r150"),

    tc("Folder scenario", "UI-003", "Normal",
       "Danh sách folder dài → có scroll, hiển thị đủ toàn bộ folder",
       BOT + "\n- Bot A có ≥ 30 folder scenario",
       "1. Mở màn /basic/scenario\n2. Scroll panel folder từ trên xuống dưới\n3. Đếm số folder hiển thị",
       "30 folder scenario",
       "- Panel folder có thanh scroll\n- Scroll xuống hiển thị đủ 30 folder, không mất folder nào\n- Folder cuối cùng nhìn thấy được trọn vẹn",
       note="Nguồn: r185, r146"),

    tc("Folder scenario", "STATE-CLEAN-001", "Abnormal",
       "Bug #32468: mở popup edit folder → copy tên → Cancel → mở popup tạo mới → paste + sửa → lưu; folder gốc KHÔNG bị đổi tên",
       BOT + "\n- Có folder「元フォルダ」",
       "1. Mở popup「フォルダ名変更」của「元フォルダ」, copy text tên folder\n2. Click Cancel đóng popup\n"
       "3. Click「フォルダ追加」, paste tên vừa copy rồi sửa thành「元フォルダ2」\n4. Click lưu\n"
       "5. Kiểm tra danh sách folder\n6. Query `category` WHERE bot_id = A AND kind = 11",
       "Copy「元フォルダ」→ paste + sửa thành「元フォルダ2」",
       "- Tạo mới folder「元フォルダ2」thành công, sinh id folder MỚI trong DB\n"
       "- Folder gốc「元フォルダ」GIỮ NGUYÊN tên, id không đổi\n- DB: 2 bản ghi category riêng biệt",
       note="Bug #32468 (10/2025), triển khai ngang folder all màn. Nguồn: TCsLine_Improve chung /「Test bug folder all màn」r55"),

    tc("Folder scenario", "FUNC-SEQ-001", "Normal",
       "Bug #32468: chuỗi thao tác liên tiếp Edit → Tạo mới / Sort / Xoá folder này / Xoá folder khác → mỗi thao tác tác động ĐÚNG folder",
       BOT + "\n- Có ≥ 4 folder scenario: F1, F2, F3, F4",
       "1. Edit tên F1 → lưu success\n2. Tiếp tục edit F1 lần 2 → lưu success → reload → edit F2\n"
       "3. Edit F1 success → ngay sau đó click「フォルダ追加」tạo folder mới\n"
       "4. Edit F1 success → ngay sau đó Sort folder\n5. Edit F1 success → ngay sau đó xoá chính F1\n"
       "6. Edit F1 success → ngay sau đó xoá F3\n7. Xoá F4 → ngay sau đó edit F2",
       "F1「フォルダ1」· F2「フォルダ2」· F3「フォルダ3」· F4「フォルダ4」",
       "- Mỗi thao tác tác động đúng folder mục tiêu, KHÔNG ghi đè nhầm folder khác\n"
       "- Tạo mới sinh id folder mới, tên folder vừa edit không bị ảnh hưởng\n"
       "- Sau xoá, folder còn lại giữ đúng tên và vị trí\n- DB `category`: đúng số bản ghi, đúng name theo từng id",
       note="Chuỗi thao tác liên tiếp không tách rời → giữ chung 1 TC. Nguồn:「Test bug folder all màn」r56-r62"),

    tc("Folder scenario", "FUNC-003", "Normal",
       "Tạo folder mới xong → tạo scenario trong folder đó → scenario hiện đúng ở folder mới",
       BOT,
       "1. Tạo folder「新規F」\n2. Click「新規作成」tạo scenario, chọn folder「新規F」\n"
       "3. Quay về màn list, click folder「新規F」\n4. Query `scenario` WHERE group_id = <id 新規F>",
       "Folder「新規F」· scenario「テストシナリオ」",
       "- Modal tạo scenario có option folder「新規F」\n- Scenario「テストシナリオ」hiển thị trong folder「新規F」\n"
       "- DB: scenario.group_id = id của 新規F",
       note="Nguồn:「Test bug folder all màn」r56"),

    # ══════════════════════ 2. Sắp xếp folder ══════════════════════
    tc("Sắp xếp folder", "CONC-001", "Abnormal",
       "Double click button「並べ替え」của panel folder → chỉ mở 1 popup sort",
       BOT + "\n- Có ≥ 6 folder scenario",
       "1. Double click nhanh button「並べ替え」ở panel folder\n2. Đếm số popup mở ra",
       "—",
       "- Chỉ mở ĐÚNG 1 popup sort folder",
       note="Nguồn: r121"),

    tc("Sắp xếp folder", "LIST-001", "Normal",
       "Popup sort folder: chỉ hiển thị folder CHƯA XOÁ của bot hiện tại, thứ tự mới nhất xuống cuối, khớp danh sách ngoài",
       BOT + "\n- Bot A có 6 folder; đã xoá 1 folder trước đó\n- Bot B (khác) cũng có folder scenario",
       "1. Mở popup sort folder\n2. Đối chiếu danh sách trong popup với danh sách ngoài panel\n3. Kiểm tra có folder của bot B hay folder đã xoá không",
       "Bot A: 6 folder còn sống + 1 folder đã xoá",
       "- Popup hiển thị đúng 6 folder của bot A\n- KHÔNG có folder đã xoá, KHÔNG có folder của bot B\n"
       "- Thứ tự trong popup KHỚP thứ tự ngoài panel; folder mới nhất ở CUỐI",
       note="Nguồn: r123, r124"),

    tc("Sắp xếp folder", "UI-002", "Normal",
       "Popup sort: chọn item hiện khung trước khi move; hover (...) hiện menu 一番上の移動 / 一番下の移動",
       BOT + "\n- Có ≥ 6 folder scenario",
       "1. Mở popup sort folder\n2. Select 1 folder để chuẩn bị kéo → quan sát khung\n3. Hover vào icon (...) của folder đó",
       "—",
       "- Bước 2: folder được select hiển thị khung (highlight) trước khi move\n"
       "- Bước 3: hiện menu 2 mục「一番上の移動」và「一番下の移動」",
       note="Nguồn: r126, r127"),

    tc("Sắp xếp folder", "UI-002", "Boundary",
       "Folder ở vị trí ĐẦU danh sách → disable 一番上の移動",
       BOT + "\n- Có 6 folder scenario",
       "1. Mở popup sort folder\n2. Hover icon (...) của folder ở vị trí #1\n3. Quan sát trạng thái 2 nút",
       "Folder #1 trong 6 folder",
       "- Nút「一番上の移動」bị DISABLE\n- Nút「一番下の移動」ENABLE",
       note="Nguồn: r128"),

    tc("Sắp xếp folder", "UI-002", "Boundary",
       "Folder ở vị trí CUỐI danh sách → disable 一番下の移動",
       BOT + "\n- Có 6 folder scenario",
       "1. Mở popup sort folder\n2. Hover icon (...) của folder ở vị trí cuối (#6)\n3. Quan sát trạng thái 2 nút",
       "Folder #6 trong 6 folder",
       "- Nút「一番下の移動」bị DISABLE\n- Nút「一番上の移動」ENABLE",
       note="Nguồn: r130"),

    tc("Sắp xếp folder", "FUNC-SORT-001", "Normal",
       "Folder ở vị trí #2 trở xuống: click 一番上の移動 → lên đầu; folder #2 từ dưới lên: click 一番下の移動 → xuống cuối",
       BOT + "\n- Có 6 folder scenario theo thứ tự F1..F6",
       "1. Mở popup sort folder\n2. Chọn F3 → click「一番上の移動」→ quan sát vị trí F3 và các folder khác\n"
       "3. Chọn F5 → click「一番下の移動」→ quan sát vị trí\n4. Click lưu → reload → kiểm tra `category.position`",
       "6 folder F1..F6",
       "- F3 lên vị trí #1, các folder khác dịch xuống 1 bậc đúng thứ tự\n"
       "- F5 xuống vị trí cuối, các folder khác dịch lên đúng thứ tự\n"
       "- Sau lưu + reload: `category.position` được update đúng, thứ tự giữ nguyên",
       note="Nguồn: r129, r131"),

    tc("Sắp xếp folder", "FUNC-SORT-001", "Normal",
       "Drop&drag folder (1 folder đầu↓cuối, 1 folder cuối↑đầu, nhiều folder) → category.position update đúng",
       BOT + "\n- Có 6 folder scenario F1..F6",
       "1. Mở popup sort folder\n2. Kéo F1 xuống cuối → click 保存\n3. Mở lại popup, kéo folder cuối lên đầu → 保存\n"
       "4. Mở lại popup, kéo 3 folder sang vị trí khác nhau → 保存\n5. Reload, query `category`.`position` WHERE kind = 11",
       "6 folder F1..F6",
       "- Cả 3 lần: vị trí folder ngoài panel thay đổi đúng như đã kéo\n"
       "- DB `category`.`position` được update đúng cho từng folder\n- Sau reload thứ tự giữ nguyên",
       note="3 thao tác cùng kết quả (position update đúng) → giữ chung. Nguồn: r132-r134"),

    tc("Sắp xếp folder", "STATE-CLEAN-001", "Normal",
       "Kéo-thả xong nhưng KHÔNG bấm 保存 (đóng bằng X) → danh sách folder giữ nguyên vị trí cũ",
       BOT + "\n- Có 6 folder scenario F1..F6",
       "1. Mở popup sort folder, kéo F1 xuống cuối\n2. Click dấu X đóng popup (không 保存)\n"
       "3. Kiểm tra thứ tự folder ngoài panel\n4. Mở lại popup sort → kiểm tra thứ tự trong popup",
       "6 folder F1..F6",
       "- Popup đóng\n- Thứ tự ngoài panel vẫn F1..F6 (không đổi)\n"
       "- Mở lại popup: thứ tự về default theo `category.position` đã lưu, không giữ thay đổi chưa save",
       note="Nguồn: r135, r136; #35968 r172"),

    tc("Sắp xếp folder", "REG-SHARED-001", "Normal",
       "Sau khi đổi vị trí folder success → màn scenario hiển thị đúng thứ tự mới",
       BOT + "\n- Vừa sort + lưu thứ tự folder mới",
       "1. Sort folder + 保存\n2. Quan sát panel folder ở màn /basic/scenario",
       "Thứ tự mới: F3, F1, F2, F4, F5, F6",
       "- Panel folder hiển thị đúng thứ tự F3, F1, F2, F4, F5, F6",
       note="Nguồn: r137"),

    tc("Sắp xếp folder", "REG-SHARED-001", "Abnormal",
       "Sau khi đổi vị trí folder scenario → 8 điểm tham chiếu phải hiển thị THỨ TỰ MỚI",
       BOT8 + "\n- Vừa sort + lưu thứ tự folder scenario mới",
       "1. Sort folder scenario + 保存\n2. Lần lượt mở 8 điểm tham chiếu\n3. Đối chiếu thứ tự folder trong dropdown với thứ tự ngoài màn scenario",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Cả 8 điểm hiển thị folder theo ĐÚNG thứ tự mới (giống màn /basic/scenario)",
       spec="Đã hỏi leader",
       note="MT-06 — corpus r138 đánh **NG**:『vị trí folder vẫn như cũ』ở Chat 1:1, các điểm r139-r145 bỏ trống "
            "vì đã dừng test. TC dự kiến FAIL → cần raise bug nếu vẫn tái hiện. Nguồn: r138-r145"),

    tc("Sắp xếp folder", "FUNC-SORT-001", "Normal",
       "#35968: sau khi kéo-thả folder, nút 一番上/一番下 ở icon 3 chấm vẫn tác động ĐÚNG folder (index không lệch)",
       BOT + "\n- Có 6 folder scenario",
       "1. Mở popup sort folder\n2. Kéo folder từ dưới lên đầu (chưa save)\n"
       "3. Hover icon 3 chấm của folder vừa kéo → kiểm tra trạng thái nút + click sort\n"
       "4. Lặp: kéo-thả rồi bấm nút lên/xuống XEN KẼ nhiều lần, chưa save\n5. Save → reload → kiểm tra thứ tự",
       "6 folder; ≥ 4 lượt thao tác xen kẽ kéo-thả và bấm nút",
       "- Sau mỗi lần kéo-thả, nút lên/xuống luôn tác động đúng folder ĐANG HIỂN THỊ (không lệch index)\n"
       "- Folder ở đầu → disable 一番上の移動; ở cuối → disable 一番下の移動 (đúng theo vị trí hiện tại sau kéo)\n"
       "- Sau save + reload: thứ tự đúng, không mất folder, không nhân đôi folder",
       note="Triển khai ngang #35968 (06/2026). Nguồn: TCsLine_Improve chung /「#35968」r162-r168, r171"),

    tc("Sắp xếp folder", "FUNC-SEQ-001", "Normal",
       "#35968: chuỗi Sort → Tạo mới folder → Sort → Xoá folder → Sort → mỗi bước hiển thị đúng vị trí",
       BOT + "\n- Có 6 folder scenario",
       "1. Sort folder + 保存 → kiểm tra vị trí\n2. Tạo mới 1 folder → kiểm tra vị trí folder mới\n"
       "3. Sort lại + 保存\n4. Xoá 1 folder → Sort lại + 保存\n5. Reload kiểm tra thứ tự cuối cùng",
       "6 folder ban đầu + 1 folder tạo mới",
       "- Sau mỗi lần save, folder hiển thị đúng vị trí mong muốn\n"
       "- Folder tạo mới hiển thị ở vị trí ĐẦU danh sách trong popup sort\n"
       "- Sau xoá + sort: thứ tự các folder còn lại đúng, không rớt folder",
       note="⚠️ #35968 r110 ghi folder mới ở vị trí ĐẦU trong popup sort, trong khi r104 (tab master) ghi folder mới "
            "xuống CUỐI panel folder ngoài — 2 ngữ cảnh khác nhau, cần verify lại. Nguồn:「#35968」r108-r110, r174"),

    # ══════════════════════ 3. Màn list scenario ══════════════════════
    tc("Màn list scenario", "UI-001", "Normal",
       "Check giao diện chung màn list scenario: căn lề · text · màu · font-size · bo góc · độ dày chữ khớp design",
       BOT + "\n- Có ≥ 5 folder và ≥ 10 scenario",
       "1. Mở /basic/scenario\n2. Đối chiếu với design XD: căn lề, text, màu (color), font-size, border-radius, font-weight",
       "Link design ghi ở tab Info của file 04. TCsLine_Scenario (4/2024)",
       "- Toàn bộ 6 thuộc tính khớp design, không lệch",
       note="Evidence: ảnh chụp màn hình + DevTools. Nguồn: r3"),

    tc("Màn list scenario", "UI-002", "Normal",
       "Hover vào button / icon / link → đổi màu và con trỏ chuyển thành hình bàn tay",
       BOT,
       "1. Hover lần lượt vào: button 新規作成 · button 並べ替え · icon 3 chấm · link tên scenario · nút 表示 của 3 cột đếm\n2. Quan sát màu và con trỏ",
       "—",
       "- Tất cả đổi màu khi hover\n- Con trỏ chuyển thành hình bàn tay (pointer), không phải mũi tên",
       note="Nguồn: r4"),

    tc("Màn list scenario", "CONC-001", "Abnormal",
       "Double click vào button và đường link trên màn list → chỉ thực thi 1 lần",
       BOT,
       "1. Double click nhanh từng button/link trên màn list scenario\n2. Quan sát số popup / số lần điều hướng",
       "—",
       "- Mỗi thao tác chỉ mở 1 popup hoặc điều hướng 1 lần, không nhân đôi",
       note="Nguồn: r5"),

    tc("Màn list scenario", "UI-003", "Normal",
       "Màn list scenario ở độ phân giải 1366 x 768 → không vỡ layout, không tràn ngang",
       BOT + "\n- Có ≥ 10 scenario, tên scenario dài 20 ký tự",
       "1. Đặt cửa sổ trình duyệt 1366 x 768\n2. Mở /basic/scenario\n3. Quan sát bảng danh sách và panel folder",
       "10 scenario, tên 20 ký tự JP",
       "- Không vỡ layout, không có thanh scroll ngang ở body\n- Bảng và panel folder hiển thị đủ cột",
       note="Nguồn: r6"),

    tc("Màn list scenario", "DATA-INPUT-001", "Boundary",
       "Nhập input với maxlength → không vỡ layout",
       BOT,
       "1. Mở modal tạo scenario, nhập 20 ký tự (max) vào 管理名\n2. Mở modal tạo folder, nhập 15 ký tự (max)\n3. Quan sát layout modal",
       "管理名: 20 ký tự JP · フォルダ名: 15 ký tự JP",
       "- Text nằm gọn trong ô input, không tràn ra ngoài\n- Modal không bị giãn/vỡ",
       note="Nguồn: r7"),

    tc("Màn list scenario", "DATA-TEXT-001", "Normal",
       "Các ô input trên màn list scenario tự động trim space đầu/cuối",
       BOT,
       "1. Tạo folder với tên có space đầu và cuối\n2. Tạo scenario với 管理名 có space đầu và cuối\n"
       "3. Search với từ khoá có space đầu/cuối\n4. Query DB kiểm tra giá trị lưu",
       "「  テスト  」(2 space đầu, 2 space cuối)",
       "- DB lưu「テスト」(đã trim space đầu/cuối)\n- Search vẫn ra kết quả đúng",
       note="Nguồn: r8, r274"),

    tc("Màn list scenario", "UI-003", "Normal",
       "Danh sách scenario nhiều bản ghi trên 1 trang → scroll hiển thị đủ",
       BOT + "\n- Folder đang chọn có 20 scenario (đầy 1 trang)",
       "1. Mở folder có 20 scenario\n2. Scroll từ đầu đến cuối bảng\n3. Đếm số dòng hiển thị",
       "20 scenario",
       "- Scroll mượt, hiển thị đủ 20 dòng, không mất dòng nào",
       note="Nguồn: r9"),

    tc("Màn list scenario", "UI-001", "Normal",
       "Placeholder / Tooltip trên màn list scenario đầy đủ đúng design",
       BOT,
       "1. Quan sát placeholder ô tìm kiếm 管理名\n2. Hover các icon có tooltip theo design\n3. Đối chiếu với design XD",
       "—",
       "- Placeholder và tooltip hiển thị đủ, nội dung khớp design",
       note="Nguồn: r10, r272"),

    tc("Màn list scenario", "OUT-001", "Normal",
       "Button マニュアル: hiển thị đúng design, click → mở link manual",
       BOT,
       "1. Quan sát button「マニュアル」\n2. Click vào button\n3. Quan sát trang mở ra",
       "—",
       "- Button hiển thị đúng design\n- Click mở ra link manual (tab mới)",
       note="Nguồn: r98, r99"),

    tc("Màn list scenario", "STATE-001", "Normal",
       "Icon ẩn menu メニューを非表示 → ẩn menu ở TẤT CẢ các màn; click mở lại → hiện lại",
       BOT,
       "1. Click icon「メニューを非表示」ở màn scenario\n2. Chuyển sang các màn khác (template, tag, form...) → kiểm tra menu\n"
       "3. Quay lại màn scenario, click icon mở lại menu",
       "—",
       "- Menu bị ẩn ở tất cả các màn, không chỉ màn scenario\n- Click mở lại → menu hiện lại ở tất cả các màn",
       note="Nguồn: r100, r101"),

    tc("Màn list scenario", "LIST-001", "Normal",
       "Folder CHƯA có scenario → bảng danh sách để trống (empty state)",
       BOT + "\n- Có folder「空フォルダ」chưa chứa scenario nào",
       "1. Click folder「空フォルダ」\n2. Quan sát bảng danh sách scenario bên phải",
       "Folder rỗng",
       "- Bảng danh sách để trống, không có dòng nào\n- Không hiển thị lỗi JS",
       note="Nguồn: r186"),

    tc("Màn list scenario", "LIST-001", "Normal",
       "Folder CÓ scenario → hiển thị scenario, cái mới nhất xuống CUỐI danh sách",
       BOT + "\n- Folder「テストF」có 3 scenario tạo lần lượt S1, S2, S3",
       "1. Click folder「テストF」\n2. Quan sát thứ tự 3 scenario\n3. Tạo thêm S4 trong cùng folder (KHÔNG tick「フォルダ内の一番上に追加する」)\n4. Quan sát vị trí S4",
       "S1, S2, S3 tạo theo thứ tự thời gian; S4 tạo sau",
       "- Thứ tự hiển thị: S1, S2, S3 (mới nhất xuống cuối)\n- Sau bước 3: S4 nằm ở CUỐI danh sách",
       note="Nguồn: r187, r804"),

    tc("Màn list scenario", "DATA-001", "Normal",
       "Cột 最終編集日時 ghi nhận đúng thời điểm cập nhật gần nhất của scenario",
       BOT + "\n- Có scenario S1, ghi lại giá trị 最終編集日時 hiện tại",
       "1. Ghi lại 最終編集日時 của S1\n2. Vào S1, lần lượt thực hiện: add msg · add action · xoá msg · xoá all action · "
       "edit time step · edit tên step · edit profile · sort msg\n3. Sau MỖI thao tác, quay ra màn list kiểm tra 最終編集日時",
       "8 loại thao tác trong scenario S1",
       "- Sau MỖI thao tác, 最終編集日時 cập nhật thành thời điểm vừa thao tác\n- Giá trị hiển thị đúng định dạng ngày giờ",
       note="Nguồn: r707, r828"),

    tc("Màn list scenario", "DATA-MIG-001", "Normal",
       "Scenario tạo TRƯỚC bản release (data cũ) → hiển thị đúng folder, đúng scenario next, đúng số lượng đang/đã chạy",
       BOT + "\n- Bot có scenario tạo từ trước bản release (data cũ), có gắn folder, có setting scenario next, đang có friend chạy",
       "1. Mở màn /basic/scenario\n2. Kiểm tra scenario data cũ: folder hiển thị · scenario next gắn ở action của step cuối\n"
       "3. Kiểm tra 3 cột đếm friend so với số liệu trước release\n4. Cho 1 friend chạy XONG scenario data cũ → kiểm tra next scenario",
       "Scenario data cũ có: 1 folder, 1 scenario next, 5 friend đang chạy, 3 friend đã xong",
       "- Hiển thị ĐÚNG folder của scenario cũ\n- Hiển thị ĐÚNG scenario next đã gắn vào action của step cuối\n"
       "- 3 cột đếm hiển thị đúng số lượng như trước release\n- Friend chạy xong → next đúng scenario đã setting",
       note="Nguồn: r11-r18 (khối『Check data cũ』)"),

    # ══════════════════════ 4. Tìm kiếm & phân trang list ══════════════════════
    tc("Tìm kiếm & phân trang list", "FUNC-SEARCH-001", "Normal",
       "Search theo 管理名: nhập text JP rồi Enter → search TOÀN BỘ folder, đóng menu folder khi hiện kết quả",
       BOT + "\n- Bot có scenario「キャンペーン2026」ở folder F1 và「キャンペーン旧」ở folder F2\n- Đang đứng ở folder F1",
       "1. Nhập「キャンペーン」vào ô tìm kiếm\n2. Nhấn Enter\n3. Quan sát kết quả và panel folder",
       "Từ khoá:「キャンペーン」",
       "- Kết quả trả về CẢ 2 scenario ở F1 và F2 (search all folder, không giới hạn folder đang chọn)\n"
       "- Panel/menu folder tự ĐÓNG khi hiển thị kết quả",
       note="Nguồn: r273, r275"),

    tc("Tìm kiếm & phân trang list", "FUNC-SEARCH-001", "Normal",
       "Search gần đúng / không phân biệt hoa-thường / kết quả nằm cùng trang hoặc khác trang → đều ra đúng",
       BOT + "\n- Có ≥ 25 scenario (2 trang), trong đó「Campaign2026」ở trang 1 và「campaignOld」ở trang 2",
       "1. Search「campaign」(chữ thường)\n2. Search「CAMPAIGN」(chữ hoa)\n3. Search「Camp」(gần đúng)\n4. Đối chiếu kết quả 3 lần",
       "Từ khoá:「campaign」/「CAMPAIGN」/「Camp」",
       "- Cả 3 lần đều trả về đủ「Campaign2026」và「campaignOld」\n- Không phân biệt hoa/thường, khớp gần đúng (LIKE)",
       note="3 input cùng 1 kết quả → giữ chung. Nguồn: r276-r279"),

    tc("Tìm kiếm & phân trang list", "LIST-001", "Normal",
       "Search ra nhiều kết quả → phân trang hoạt động đúng, các chức năng khác vẫn dùng được",
       BOT + "\n- Có ≥ 45 scenario có tên chứa「テスト」",
       "1. Search「テスト」\n2. Kiểm tra phân trang kết quả (số trang, nút <, >)\n3. Chuyển sang trang 2\n"
       "4. Trên trang kết quả, thử: tick chọn scenario · mở menu 3 chấm · click vào scenario để vào màn step",
       "45 scenario khớp từ khoá",
       "- Kết quả chia đúng 3 trang (20 bản ghi/trang)\n- Chuyển trang hiển thị đúng data trang đó\n"
       "- Các chức năng tick chọn / menu 3 chấm / vào màn step đều hoạt động bình thường trên trang kết quả",
       note="Nguồn: r280, r281"),

    tc("Tìm kiếm & phân trang list", "FUNC-SEARCH-001", "Normal",
       "Không nhập gì rồi Enter → hiển thị lại TOÀN BỘ scenario của folder đang chọn",
       BOT + "\n- Đang ở folder F1 có 8 scenario, vừa search ra 2 kết quả",
       "1. Xoá trắng ô tìm kiếm\n2. Nhấn Enter\n3. Đếm số scenario hiển thị",
       "(để trống)",
       "- Hiển thị lại đủ 8 scenario của folder F1",
       note="Nguồn: r282"),

    tc("Tìm kiếm & phân trang list", "FUNC-SEARCH-001", "Abnormal",
       "Search tên KHÔNG tồn tại → danh sách rỗng, không lỗi",
       BOT,
       "1. Nhập chuỗi không tồn tại「ZZZZ存在しない」\n2. Nhấn Enter\n3. Quan sát bảng kết quả",
       "「ZZZZ存在しない」",
       "- Bảng kết quả rỗng\n- Không hiển thị lỗi JS / lỗi server",
       note="Nguồn: r283"),

    tc("Tìm kiếm & phân trang list", "FUNC-SEARCH-001", "Normal",
       "Search hoạt động đúng ở CẢ 2 loại folder: 未分類 và folder do user tạo",
       BOT + "\n- Folder 未分類 có scenario「未分類テスト」; folder「F1」có scenario「F1テスト」",
       "1. Đứng ở folder 未分類 → search「テスト」\n2. Đứng ở folder F1 → search「テスト」\n3. So sánh 2 kết quả",
       "Từ khoá:「テスト」",
       "- Cả 2 lần đều trả về đủ「未分類テスト」và「F1テスト」(search xuyên folder)",
       note="Nguồn: r271"),

    tc("Tìm kiếm & phân trang list", "LIST-001", "Normal",
       "Phân trang màn list scenario: mặc định 20 bản ghi/trang, chuyển trang hiển thị đúng data",
       BOT + "\n- Folder đang chọn có 45 scenario",
       "1. Mở folder có 45 scenario\n2. Đếm số dòng ở trang 1\n3. Click nút > sang trang 2, trang 3\n4. Đối chiếu data từng trang",
       "45 scenario",
       "- Trang 1 và 2: đúng 20 bản ghi/trang; trang 3: 5 bản ghi\n- Data mỗi trang đúng, không lặp, không thiếu",
       spec="Spec không ghi",
       note="Corpus r390 ghi rõ 20 bản ghi/trang; spec logic-spec chỉ ghi『paginate』không nêu số mặc định → TC lấp chỗ spec thiếu. Nguồn: r390, r392"),

    tc("Tìm kiếm & phân trang list", "UI-002", "Abnormal",
       "Nút < / > khi bị disable → con trỏ KHÔNG được là hình bàn tay",
       BOT + "\n- Folder đang chọn chỉ có 5 scenario (1 trang duy nhất)",
       "1. Mở folder có 5 scenario\n2. Quan sát nút < và > (đang disable)\n3. Hover chuột vào nút disable",
       "5 scenario (chưa đủ 1 trang)",
       "- Nút < và > hiển thị trạng thái disable\n- Hover KHÔNG hiện hình bàn tay (giữ mũi tên mặc định)",
       spec="Đã hỏi leader",
       note="MT-07 — corpus r391 đánh **NG**:『disable nhưng khi hover vào vẫn hiển thị hình bàn tay』. TC dự kiến FAIL → cần raise bug. Nguồn: r391"),

    # ══════════════════════ 5. Tạo scenario ══════════════════════
    tc("Tạo scenario", "UI-001", "Normal",
       "Modal tạo scenario 新規作成 hiển thị khớp design; double click button chỉ mở 1 popup",
       BOT,
       "1. Double click nhanh button「新規作成」\n2. Đếm số popup mở ra\n3. Đối chiếu modal với design XD",
       "—",
       "- Chỉ mở ĐÚNG 1 popup tạo group scenario\n- Modal khớp design (bố cục, màu, nút)",
       note="Nguồn: r188, r189"),

    tc("Tạo scenario", "DATA-INPUT-001", "Abnormal",
       "管理名 để trống → cảnh báo, không tạo scenario",
       BOT,
       "1. Click「新規作成」\n2. Để trống 管理名\n3. Click「メッセージの登録に進む」",
       "(để trống)",
       "- Hiển thị cảnh báo 管理名 là trường bắt buộc\n- Modal không đóng, KHÔNG tạo scenario",
       note="Nguồn: r190, r191"),

    tc("Tạo scenario", "DATA-INPUT-001", "Boundary",
       "管理名 nhập 21 ký tự → cảnh báo; nhập đúng 20 ký tự → lưu thành công",
       BOT,
       "1. Nhập 21 ký tự vào 管理名 → lưu → quan sát\n2. Xoá bớt còn đúng 20 ký tự → lưu\n3. Query `scenario`.`name`",
       "Lần 1: 21 ký tự JP\nLần 2: 20 ký tự JP「あいうえおかきくけこさしすせそたちつてと」",
       "- 21 ký tự: hiển thị cảnh báo, không lưu\n- 20 ký tự: lưu thành công, `scenario.name` đúng 20 ký tự",
       note="Spec Validation Rules EP-02: name required, max:20. Nguồn: r192, r323"),

    tc("Tạo scenario", "DATA-TEXT-001", "Normal",
       "管理名 nhập tiếng Nhật → sau khi lưu hiển thị đúng, không mojibake; bộ đếm số ký tự đúng",
       BOT,
       "1. Nhập「日本語テストシナリオ」vào 管理名\n2. Quan sát bộ đếm số ký tự\n3. Lưu → xem tên ở màn list và trong DB",
       "「日本語テストシナリオ」(10 ký tự)",
       "- Bộ đếm hiển thị 10 (đếm đúng ký tự JP là 1)\n- Sau lưu: tên hiển thị đúng ở màn list, DB `scenario.name` lưu verbatim",
       note="Nguồn: r193, r194"),

    tc("Tạo scenario", "DATA-TEXT-001", "Normal",
       "管理名 nhập có space đầu/cuối → hệ thống tự trim trước khi lưu",
       BOT,
       "1. Nhập「  テストシナリオ  」(2 space đầu, 2 space cuối)\n2. Lưu\n3. Query `scenario`.`name` và xem tên ở màn list",
       "「  テストシナリオ  」",
       "- DB lưu「テストシナリオ」(đã trim)\n- Màn list hiển thị tên không có space thừa",
       note="Nguồn: r195"),

    tc("Tạo scenario", "UI-FIELD-001", "Normal",
       "Trường フォルダ: default = folder đang chọn; click bất kỳ vị trí nào trong ô → mở dropdown",
       BOT + "\n- Đang đứng ở folder「F1」",
       "1. Click「新規作成」\n2. Quan sát giá trị mặc định của trường フォルダ\n3. Click vào mép trái / giữa / mép phải của ô フォルダ",
       "Folder đang chọn:「F1」",
       "- Default hiển thị「F1」(folder đang chọn trước đó)\n- Click ở BẤT KỲ vị trí nào trong ô đều mở dropdown list folder",
       note="Nguồn: r196, r197"),

    tc("Tạo scenario", "LIST-001", "Normal",
       "Dropdown folder hiển thị đủ folder (1 folder / list ngắn / list dài có scroll) và ĐÚNG thứ tự như panel ngoài",
       BOT + "\n- Chuẩn bị 3 bot: bot X chỉ có 未分類; bot Y có 4 folder; bot Z có 25 folder",
       "1. Với mỗi bot, mở modal tạo scenario → mở dropdown フォルダ\n2. Đếm số folder hiển thị\n3. Đối chiếu thứ tự dropdown với thứ tự panel folder ngoài màn list",
       "Bot X: 1 folder (未分類) · Bot Y: 4 folder · Bot Z: 25 folder (có scroll)",
       "- Cả 3 bot: dropdown hiển thị ĐỦ folder đang có\n- Bot Z: dropdown có scroll, scroll xuống thấy đủ 25 folder\n"
       "- Thứ tự folder trong dropdown KHỚP thứ tự ngoài panel folder",
       note="3 quy mô cùng 1 kết quả → giữ chung. Nguồn: r198-r201"),

    tc("Tạo scenario", "UI-FIELD-001", "Normal",
       "Chọn folder khác trong dropdown → ghi nhận folder vừa chọn và tự đóng dropdown",
       BOT,
       "1. Mở dropdown フォルダ\n2. Chọn folder「F2」\n3. Quan sát ô フォルダ và dropdown",
       "Chọn folder「F2」",
       "- Ô フォルダ hiển thị「F2」\n- Dropdown TỰ ĐÓNG sau khi chọn",
       note="Nguồn: r202, r203"),

    tc("Tạo scenario", "CONC-001", "Abnormal",
       "Double click button「メッセージの登録に進む」→ chỉ tạo 1 scenario",
       BOT,
       "1. Nhập 管理名 hợp lệ\n2. Double click nhanh button「メッセージの登録に進む」\n"
       "3. Quay lại màn list, query `scenario` WHERE bot_id = A AND name = '<tên>'",
       "管理名:「二重クリック検証」",
       "- Chỉ tạo ĐÚNG 1 scenario\n- DB: COUNT(*) = 1",
       note="Nguồn: r204"),

    tc("Tạo scenario", "STATE-CLEAN-001", "Normal",
       "Click X hoặc click ra ngoài modal tạo scenario → đóng, KHÔNG lưu data đã nhập",
       BOT,
       "1. Mở modal, nhập 管理名「破棄テスト」, chọn folder khác\n2. Click dấu X\n3. Kiểm tra danh sách scenario\n"
       "4. Mở lại modal, nhập data, click ra ngoài vùng modal → quan sát",
       "管理名:「破棄テスト」",
       "- Bước 2: modal đóng, scenario KHÔNG được tạo\n"
       "- Bước 4: hoặc không phản ứng gì, hoặc đóng modal và KHÔNG lưu data",
       note="Nguồn: r205, r206"),

    tc("Tạo scenario", "STATE-CLEAN-001", "Abnormal",
       "Đóng modal tạo scenario (dấu X) rồi mở lại → toàn bộ dữ liệu đã nhập (kể cả FOLDER) phải được reset",
       BOT + "\n- Đang đứng ở folder「F1」",
       "1. Mở modal, nhập 管理名「abc」, đổi フォルダ sang「F3」\n2. Click X đóng modal\n"
       "3. Mở lại modal「新規作成」\n4. Quan sát giá trị 管理名 và フォルダ",
       "管理名「abc」· đổi folder từ F1 sang F3",
       "- 管理名 trống\n- フォルダ về lại「F1」(folder đang chọn), KHÔNG giữ「F3」",
       spec="Đã hỏi leader",
       note="MT-08 — corpus r219 đánh **NG**:『chưa reset folder』. TC dự kiến FAIL → cần raise bug. Nguồn: r218, r219"),

    tc("Tạo scenario", "FUNC-001", "Normal",
       "Tạo scenario ở folder KHÁC folder đang đứng → redirect màn step, scenario nằm cuối folder MỚI",
       BOT + "\n- Đang đứng ở folder「F1」, có folder「F2」",
       "1. Click「新規作成」, nhập 管理名, đổi フォルダ sang「F2」\n2. Click「メッセージの登録に進む」\n"
       "3. Quan sát trang được điều hướng tới\n4. Quay về màn list, mở folder F2\n5. Query `scenario` WHERE name = '<tên>'",
       "管理名:「新シナリオ」· folder đích: F2",
       "- Redirect sang màn list step của scenario vừa tạo (để tạo scenario con)\n"
       "- Trong folder F2: scenario mới nằm ở CUỐI danh sách\n- DB: scenario.group_id = id của F2",
       note="Nguồn: r207"),

    tc("Tạo scenario", "DATA-COUNT-001", "Normal",
       "Tạo scenario GIỮ NGUYÊN folder đang đứng → folder đó có thêm scenario, số lượng trong folder tăng 1",
       BOT + "\n- Folder「F1」đang có 4 scenario, số hiển thị (4)",
       "1. Ghi lại số scenario hiển thị ở folder F1\n2. Tạo scenario mới, giữ nguyên folder F1\n"
       "3. Quay về màn list, quan sát folder F1 và bảng scenario",
       "Folder F1: 4 → 5 scenario",
       "- Scenario mới hiển thị ở CUỐI danh sách folder F1\n- Số lượng cạnh folder F1 tăng từ (4) lên (5)",
       note="Nguồn: r208"),

    tc("Tạo scenario", "REG-SHARED-001", "Normal",
       "Scenario vừa tạo hiển thị ở popup sort và ở 8 điểm tham chiếu",
       BOT8 + "\n- Vừa tạo scenario「新シナリオ」ở folder F1",
       "1. Tạo scenario「新シナリオ」\n2. Mở popup sort group scenario → kiểm tra có「新シナリオ」không\n"
       "3. Lần lượt mở 8 điểm tham chiếu → kiểm tra dropdown scenario",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Popup sort có「新シナリオ」ở đúng vị trí\n- Cả 8 điểm tham chiếu đều hiển thị「新シナリオ」trong dropdown chọn scenario",
       note="Nguồn: r209-r217"),

    tc("Tạo scenario", "FUNC-001", "Normal",
       "Tạo scenario ở folder mặc định 未分類 → scenario nằm trong 未分類, hiển thị đủ ở 8 điểm tham chiếu",
       BOT8 + "\n- Đang đứng ở folder 未分類",
       "1. Click「新規作成」, giữ folder 未分類, nhập 管理名\n2. Lưu → quay lại màn list\n"
       "3. Kiểm tra vị trí scenario trong 未分類\n4. Kiểm tra 8 điểm tham chiếu",
       "管理名:「未分類シナリオ」· folder: 未分類",
       "- Scenario nằm trong folder 未分類 (scenario.group_id = 0)\n- Cả 8 điểm tham chiếu hiển thị scenario mới",
       note="Nguồn: r220-r230"),

    tc("Tạo scenario", "STATE-001", "Abnormal",
       "Tạo scenario ở folder 未分類 rồi chọn folder KHÁC trong modal → menu folder bên ngoài KHÔNG được tự đổi focus",
       BOT + "\n- Đang đứng ở folder 未分類",
       "1. Click「新規作成」\n2. Trong modal, đổi フォルダ sang「F3」\n3. QUAN SÁT panel folder bên ngoài (chưa bấm lưu)",
       "Đang ở 未分類, chọn F3 trong modal",
       "- Panel folder bên ngoài vẫn focus vào 未分類, KHÔNG tự nhảy sang F3 khi chưa lưu",
       spec="Đã hỏi leader",
       note="MT-09 — corpus r220 đánh OK nhưng ghi chú『chọn folder khác ở menu cũng đổi luôn sang focus thằng mới』, "
            "và r221 ghi『ở trên đang sai nên k test tiếp nữa』. Hành vi mong muốn chưa được chốt. Nguồn: r220, r221"),

    tc("Tạo scenario", "UI-FIELD-001", "Normal",
       "Checkbox「フォルダ内の一番上に追加する」CÓ tick → scenario mới nằm ĐẦU danh sách; trạng thái tick được nhớ cho lần sau và cho folder khác",
       BOT + "\n- Folder F1 đang có 3 scenario",
       "1. Click「新規作成」, TICK checkbox「フォルダ内の一番上に追加する」, nhập tên → lưu\n"
       "2. Quay về màn list, quan sát vị trí scenario mới\n3. Mở lại modal「新規作成」→ quan sát trạng thái checkbox\n"
       "4. Chuyển sang folder F2, mở modal「新規作成」→ quan sát checkbox",
       "Folder F1 có 3 scenario · scenario mới「先頭追加」",
       "- Scenario「先頭追加」nằm ở ĐẦU danh sách folder F1\n- Sau khi lưu success, hệ thống mở ra màn detail của scenario mới\n"
       "- Lần mở modal tiếp theo: checkbox VẪN đang tick\n- Ở folder F2 modal cũng ăn theo trạng thái tick",
       note="Khối『design mới』. Nguồn: r803"),

    tc("Tạo scenario", "UI-FIELD-001", "Normal",
       "Checkbox「フォルダ内の一番上に追加する」KHÔNG tick → scenario mới nằm CUỐI danh sách",
       BOT + "\n- Folder F1 đang có 3 scenario, checkbox đang bỏ tick",
       "1. Click「新規作成」, BỎ TICK checkbox, nhập tên → lưu\n2. Quay về màn list, quan sát vị trí scenario mới",
       "Folder F1 có 3 scenario · scenario mới「末尾追加」",
       "- Scenario「末尾追加」nằm ở CUỐI danh sách folder F1",
       note="Nguồn: r804"),

    # ══════════════════════ 6. Sửa scenario ══════════════════════
    tc("Sửa scenario", "CONC-001", "Abnormal",
       "Double click button 編集 hoặc double click vào dòng scenario → chỉ mở 1 lần màn chi tiết, data đầy đủ",
       BOT + "\n- Có scenario S1 với 管理名 và folder đã set",
       "1. Double click nhanh button「編集」của S1\n2. Quan sát số lần điều hướng\n"
       "3. Quay lại, double click nhanh vào dòng bản ghi S1\n4. Kiểm tra data hiển thị ở màn chi tiết",
       "Scenario S1「テストシナリオ」ở folder F1",
       "- Mỗi thao tác chỉ mở màn chi tiết 1 lần\n- Màn chi tiết hiển thị đầy đủ: 管理名, folder, danh sách step",
       note="Nguồn: r304, r305"),

    tc("Sửa scenario", "FUNC-002", "Normal",
       "Sửa 管理名 của scenario → nhấn Enter lưu thành công",
       BOT + "\n- Scenario S1 tên「旧名前」",
       "1. Mở màn chi tiết S1\n2. Sửa 管理名 thành「新名前」\n3. Nhấn Enter\n"
       "4. Quay về màn list kiểm tra tên\n5. Query `scenario`.`name` WHERE id = <S1>",
       "「旧名前」→「新名前」",
       "- Lưu thành công, không cần bấm nút riêng\n- Màn list hiển thị「新名前」\n- DB: scenario.name = '新名前'",
       note="Nguồn: r306"),

    tc("Sửa scenario", "FUNC-002", "Normal",
       "Đổi folder của scenario: 未分類 → folder khác, và folder khác → 未分類",
       BOT + "\n- Scenario S1 đang ở 未分類; có folder「F2」",
       "1. Mở màn chi tiết S1, đổi folder sang「F2」→ lưu\n2. Quay về màn list, kiểm tra S1 nằm ở folder nào\n"
       "3. Mở lại S1, đổi folder về 未分類 → lưu\n4. Kiểm tra lại + query `scenario`.`group_id`",
       "S1: 未分類 ⇄ F2",
       "- Bước 2: S1 nằm trong folder F2, không còn ở 未分類; `group_id` = id của F2\n"
       "- Bước 4: S1 quay về 未分類; `group_id` = 0",
       note="Nguồn: r307, r308"),

    tc("Sửa scenario", "FUNC-SORT-001", "Abnormal",
       "Đổi folder scenario từ folder A sang folder B (cả 2 đều không phải 未分類) → scenario phải nằm ở CUỐI danh sách folder B",
       BOT + "\n- Folder A chứa S1; folder B đang có 6 scenario",
       "1. Mở màn chi tiết S1, đổi folder từ A sang B → lưu\n2. Quay về màn list, mở folder B\n3. Quan sát VỊ TRÍ của S1 trong folder B",
       "Folder B có 6 scenario, S1 chuyển từ A sang",
       "- S1 nằm ở vị trí CUỐI danh sách folder B (vị trí thứ 7)",
       spec="Đã hỏi leader",
       note="MT-10 — corpus r309 đánh OK nhưng ghi chú『scenario hiển thị sai vị trí trong bảng (không ở cuối)』; "
            "r307/r308 cũng ghi chú vị trí bất thường (『sce đang ở đầu danh sách』/『scen đang ở vị trí thứ 7 từ trên xuống』). "
            "Quy tắc vị trí sau khi đổi folder chưa được chốt. Nguồn: r307-r310"),

    tc("Sửa scenario", "FUNC-002", "Normal",
       "Sửa ĐỒNG THỜI 管理名 và folder trong 1 lần lưu → cả 2 đều được cập nhật",
       BOT + "\n- Scenario S1「旧名前」ở folder A",
       "1. Mở màn chi tiết S1\n2. Đổi 管理名 thành「新名前」VÀ đổi folder sang B\n3. Lưu\n"
       "4. Query `scenario` WHERE id = <S1>: name, group_id",
       "「旧名前」/ folder A →「新名前」/ folder B",
       "- DB: name = '新名前' VÀ group_id = id của B\n- Màn list: S1 hiển thị tên mới, nằm trong folder B",
       note="Nguồn: r310"),

    tc("Sửa scenario", "REG-SHARED-001", "Normal",
       "Sau khi sửa 管理名 / folder scenario → 8 điểm tham chiếu hiển thị thông tin mới",
       BOT8 + "\n- Vừa sửa scenario S1 (đổi tên + đổi folder)",
       "1. Sửa 管理名 và folder của S1\n2. Lần lượt mở 8 điểm tham chiếu\n3. Kiểm tra tên scenario và folder chứa nó",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Cả 8 điểm hiển thị TÊN MỚI của scenario và nằm trong FOLDER MỚI",
       spec="Spec không ghi",
       note="Corpus r311-r318 để TRỐNG cả kết quả mong đợi lẫn kết quả thực thi → kết quả mong đợi do AI suy từ "
            "quy tắc của r156-r163 (đổi tên folder) và r210-r217 (tạo mới). CẦN LEADER XÁC NHẬN. Nguồn: r311-r318"),

    tc("Sửa scenario", "DATA-INPUT-001", "Abnormal",
       "Sửa scenario: xoá trắng 管理名 rồi lưu → highlight 管理名, không lưu",
       BOT + "\n- Scenario S1 có 管理名「旧名前」",
       "1. Mở màn chi tiết S1\n2. Xoá trắng 管理名\n3. Click lưu\n4. Query `scenario`.`name`",
       "(để trống)",
       "- Trường 管理名 được highlight báo lỗi bắt buộc\n- Không lưu, DB name vẫn là '旧名前'",
       note="Nguồn: r319"),

    tc("Sửa scenario", "UI-FIELD-001", "Normal",
       "Trường フォルダ khi sửa scenario là bắt buộc → mặc định luôn để 未分類 nếu chưa chọn",
       BOT + "\n- Scenario S1 chưa gán folder",
       "1. Mở màn chi tiết S1\n2. Quan sát giá trị mặc định trường フォルダ",
       "Scenario chưa gán folder",
       "- Trường フォルダ default hiển thị「未分類」, không để trống",
       note="Nguồn: r320"),

    tc("Sửa scenario", "DATA-INPUT-001", "Boundary",
       "Sửa 管理名: nhập 21 ký tự → cảnh báo; bộ đếm số ký tự hiển thị đúng",
       BOT + "\n- Scenario S1",
       "1. Mở màn chi tiết S1, nhập 21 ký tự vào 管理名\n2. Quan sát bộ đếm số ký tự và cảnh báo\n3. Click lưu",
       "21 ký tự JP",
       "- Bộ đếm hiển thị đúng số ký tự đã nhập\n- Hiển thị cảnh báo vượt 20 ký tự\n- Không lưu",
       note="Nguồn: r323, r325"),

    tc("Sửa scenario", "DATA-TEXT-001", "Abnormal",
       "Sửa 管理名 nhập TOÀN KHOẢNG TRẮNG → phải báo lỗi (coi như để trống), và trim space đầu/cuối khi lưu",
       BOT + "\n- Scenario S1「旧名前」",
       "1. Xoá 管理名, nhập 3 dấu cách「   」→ lưu\n2. Nhập「  新名前  」(có space đầu/cuối) → lưu\n"
       "3. Query `scenario`.`name`",
       "Lần 1:「   」(toàn space)\nLần 2:「  新名前  」",
       "- Lần 1: báo lỗi bắt buộc, KHÔNG lưu\n- Lần 2: DB lưu「新名前」(đã trim space đầu/cuối)",
       spec="Đã hỏi leader",
       note="MT-11 — corpus r324 và r326 đều đánh **NG**; r352 cũng ghi『nhập khoảng trắng vẫn đang success』cho tên "
            "quản lý message. TC dự kiến FAIL → cần raise bug. Nguồn: r324, r326"),

    tc("Sửa scenario", "UI-FIELD-001", "Normal",
       "Trường フォルダ ở màn sửa: default = folder hiện tại, click mở dropdown, chọn folder khác thì ghi nhận",
       BOT + "\n- Scenario S1 đang ở folder「F1」; bot có 4 folder",
       "1. Mở màn chi tiết S1\n2. Quan sát giá trị trường フォルダ\n3. Click vào ô フォルダ (nhiều vị trí)\n"
       "4. Kiểm tra danh sách trong dropdown (đủ folder, đúng thứ tự)\n5. Chọn folder khác",
       "Scenario ở F1; bot có 4 folder",
       "- Default hiển thị「F1」\n- Click bất kỳ vị trí nào trong ô đều mở dropdown\n"
       "- Dropdown đủ 4 folder, đúng thứ tự\n- Chọn folder khác → ô cập nhật giá trị vừa chọn",
       note="Nguồn: r327-r332"),

    tc("Sửa scenario", "DATA-001", "Normal",
       "Màn sửa nội dung scenario (phần dưới) hiển thị đầy đủ, đúng data đã nhập ban đầu",
       BOT + "\n- Scenario S1 có: 2 filter, 3 step (send ngay / 日時で指定 / 経過時間で指定), mỗi step có msg + action + profile",
       "1. Mở màn chi tiết S1\n2. Đối chiếu từng phần: filter · thời gian gửi từng step · message · action · profile · tên quản lý step",
       "S1: 2 filter, 3 step đủ 3 loại timing",
       "- Toàn bộ thông tin hiển thị đầy đủ, khớp với data đã nhập ban đầu",
       note="Nguồn: r333"),

    tc("Sửa scenario", "FUNC-SEQ-001", "Normal",
       "Chuỗi edit nội dung scenario: filter → time step → msg/action (add, xoá, edit, sort) → tên quản lý step → đều lưu đúng",
       BOT + "\n- Scenario S1 có 2 filter, 3 step",
       "1. Sửa nội dung filter\n2. Sửa time của 1 step\n3. Add msg → xoá msg → edit nội dung msg → sort msg\n"
       "4. Add action → xoá action\n5. Sửa tên quản lý step\n6. Reload màn chi tiết, đối chiếu toàn bộ",
       "Scenario S1 với 2 filter, 3 step",
       "- Sau mỗi thao tác, thay đổi được lưu và hiển thị đúng\n- Sau reload, toàn bộ thay đổi giữ nguyên (không mất)\n"
       "- `scenario`.`update_timestamp` được cập nhật",
       note="Khối『design mới』r805-r806. Nguồn: r805, r806"),

    # ══════════════════════ 7. Copy scenario ══════════════════════
    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: double click chỉ copy 1 lần; bản mới ở CUỐI danh sách, tên = {tên gốc}のコピー, cùng folder với bản gốc",
       BOT + "\n- Folder F1 có scenario S1「元シナリオ」, đang có 5 friend chạy và 3 friend đã xong",
       "1. Menu 3 chấm của S1 →「コピー」(double click nhanh)\n2. Quay về màn list, mở folder F1\n"
       "3. Quan sát tên và vị trí bản copy\n4. Query `scenario` WHERE bot_id = A ORDER BY id DESC LIMIT 2",
       "S1「元シナリオ」ở folder F1",
       "- Chỉ tạo ĐÚNG 1 bản copy\n- Tên bản copy =「元シナリオのコピー」\n"
       "- Bản copy nằm ở CUỐI danh sách, CÙNG folder F1 với bản gốc\n- DB: bản ghi scenario mới, group_id giống bản gốc",
       note="Nguồn: r40, r41, r394"),

    tc("Copy scenario", "DATA-COUNT-001", "Normal",
       "Copy scenario: 3 cột đếm friend (購読中 / 途中で終了 / 読了済) và send_count của từng step đều RESET về 0",
       BOT + "\n- S1 đang có 5 friend 購読中, 2 friend 途中で終了, 3 friend 読了済; step 1 đã send 10 người",
       "1. Copy S1\n2. Quan sát 3 cột đếm của bản copy ở màn list\n3. Vào màn step của bản copy, xem 配信済 của từng step\n"
       "4. Query `scenario`.`count_follow`/`count_stop`/`count_unfinish` và `step_message`.`send_count` của bản copy",
       "S1: 購読中 5 · 途中で終了 2 · 読了済 3 · step1 send_count = 10",
       "- 3 cột đếm của bản copy đều hiển thị 0人\n- 配信済 của mọi step bản copy = 0人\n"
       "- DB: count_follow = count_stop = count_unfinish = 0, send_count = 0",
       note="Nguồn: r42, r50, r79, r88, r807"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: các folder điều kiện filter được clone, DB sinh filter_manager id MỚI",
       BOT + "\n- S1 có 3 filter branch: 未分類(default), F-A (điều kiện tag), F-B (điều kiện ngày kết bạn)",
       "1. Ghi lại id các filter_manager của S1 (`filter_manager` WHERE parent_id = <S1>, type = 'scenario')\n"
       "2. Copy S1\n3. Vào màn step bản copy, đối chiếu danh sách filter branch\n"
       "4. Query `filter_manager` WHERE parent_id = <id bản copy> và `filters_v2` WHERE parent_type = 'filter_manager'",
       "S1 có 3 filter branch",
       "- Bản copy có ĐỦ 3 filter branch, tên và nội dung điều kiện GIỐNG bản gốc\n"
       "- DB: filter_manager của bản copy có id KHÁC bản gốc; filters_v2 tương ứng cũng sinh id mới",
       note="Nguồn: r43, r81"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: cả 3 loại step timing được clone đúng, step_message sinh id mới",
       BOT + "\n- S1 có 3 step: send ngay · 送信後 2 ngày lúc 10:00 · 経過時間 03時間30分後",
       "1. Ghi lại `step_message` id + delay_type/start_day/start_time của S1\n2. Copy S1\n"
       "3. Vào màn step bản copy, đối chiếu 3 step\n4. Query `step_message` WHERE scenario_id = <bản copy>",
       "3 step đủ 3 loại delay_type (1 / 0 / 2)",
       "- Bản copy có đủ 3 step, thời điểm gửi hiển thị GIỐNG bản gốc\n"
       "- DB: 3 bản ghi step_message mới, id KHÁC bản gốc, delay_type/start_day/start_time giữ nguyên giá trị",
       note="3 loại timing cùng 1 kết quả → giữ chung. Nguồn: r44-r46, r82-r84"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: message trong step — template TỰ TẠO / CLONE → sinh id mới; template GET THẲNG → giữ nguyên id gốc",
       BOT + "\n- S1 có 1 step chứa 3 message: (a) template tự tạo trong step, (b) template clone từ thư viện "
       "「テンプレートを引用して編集する」, (c) template dùng thẳng「テンプレートをそのまま利用する」",
       "1. Ghi lại `step_message`.`template_ids` của S1\n2. Copy S1\n"
       "3. Query `step_message`.`template_ids` WHERE scenario_id = <bản copy>\n4. Đối chiếu từng id với bản gốc",
       "3 message: tự tạo / clone / get thẳng",
       "- (a) và (b): id template MỚI (khác bản gốc)\n- (c): id template GIỮ NGUYÊN như bản gốc\n"
       "- Nội dung 3 message hiển thị giống hệt bản gốc",
       note="Nguồn: r47, r85"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: action của step được clone, sinh action_id MỚI",
       BOT + "\n- S1 có 1 step gắn action (gắn tag + đổi richmenu)",
       "1. Ghi lại `step_message`.`action_id` của S1\n2. Copy S1\n"
       "3. Vào bản copy, kiểm tra action hiển thị\n4. Query `step_message`.`action_id` WHERE scenario_id = <bản copy>",
       "Step có action: gắn tag「テストタグ」+ đổi richmenu",
       "- Action hiển thị giống bản gốc (đủ 2 action)\n- DB: action_id của bản copy KHÁC action_id bản gốc",
       note="Nguồn: r49, r87"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario: setting scenario next được copy sang bản mới",
       BOT + "\n- S1 có setting next sang scenario S2",
       "1. Copy S1\n2. Vào bản copy, kiểm tra phần next scenario\n3. Query `scenario`.`after_scenario_id_1` của bản copy",
       "S1 → next S2",
       "- Bản copy hiển thị next scenario = S2\n- DB: after_scenario_id_1 của bản copy = id của S2",
       note="Nguồn: r51, r80"),

    tc("Copy scenario", "DATA-ID-001", "Normal",
       "Sửa bản copy KHÔNG ảnh hưởng bản gốc và ngược lại (2 chiều độc lập)",
       BOT + "\n- Đã copy S1 thành S1-copy; cả 2 có cùng nội dung step",
       "1. Sửa nội dung message + time step + action ở S1-copy\n2. Mở S1 gốc kiểm tra nội dung\n"
       "3. Sửa nội dung message + action ở S1 gốc\n4. Mở S1-copy kiểm tra nội dung",
       "Sửa message text, đổi time step, thêm 1 action",
       "- Bước 2: S1 gốc GIỮ NGUYÊN nội dung cũ\n- Bước 4: S1-copy GIỮ NGUYÊN nội dung của nó, không bị ảnh hưởng",
       note="Nguồn: r396, r397, r398, r395"),

    tc("Copy scenario", "DATA-COPY-001", "Normal",
       "Copy scenario ĐANG có friend chạy → bản copy không kế thừa tiến trình, friend không bị chuyển sang bản copy",
       BOT + "\n- S1 đang có 5 friend 購読中, còn 2 step chưa gửi",
       "1. Copy S1\n2. Kiểm tra 3 cột đếm của S1 gốc và S1-copy\n"
       "3. Query `scenario_lineuser` WHERE scenario_id = <bản copy>\n"
       "4. Query `scenario_step_time` WHERE step_mesage_id IN (step của bản copy)\n"
       "5. Chờ tới giờ step tiếp theo → kiểm tra friend nhận msg từ scenario nào",
       "S1 có 5 friend đang chạy, còn 2 step chưa gửi",
       "- S1 gốc: 購読中 vẫn 5人; S1-copy: 購読中 0人\n"
       "- DB: KHÔNG có bản ghi scenario_lineuser hay scenario_step_time cho bản copy\n"
       "- Friend vẫn nhận step từ S1 GỐC, không nhận trùng từ bản copy",
       spec="Spec không ghi",
       note="Kết quả mong đợi do AI suy từ quy tắc『copy không copy sl đã send』(r42/r807) + spec copyScenario "
            "(logic-spec) chỉ clone step/filter/action chứ không clone scenario_lineuser. CẦN LEADER XÁC NHẬN."),

    # ══════════════════════ 8. Xóa scenario ══════════════════════
    tc("Xóa scenario", "CONC-001", "Abnormal",
       "Double click button xoá scenario → chỉ xoá 1 lần",
       BOT + "\n- Có scenario S1",
       "1. Menu 3 chấm →「削除」, double click nhanh button xoá\n2. Quan sát số popup / số lần gọi API",
       "Scenario S1",
       "- Chỉ mở 1 popup confirm và chỉ thực hiện xoá 1 lần",
       note="Nguồn: r361"),

    tc("Xóa scenario", "FUNC-004", "Normal",
       "Popup confirm xoá scenario: click OK → xoá thành công, scenario biến mất khỏi danh sách",
       BOT + "\n- Folder F1 có 3 scenario S1, S2, S3",
       "1. Xoá S2 → click OK ở popup confirm\n2. Quan sát danh sách scenario trong F1\n"
       "3. Query `scenario` WHERE id = <S2>",
       "Xoá S2 trong 3 scenario",
       "- Danh sách còn S1 và S3, mất S2\n- DB: bản ghi scenario S2 bị xoá",
       note="Nguồn: r362, r364, r822"),

    tc("Xóa scenario", "STATE-CLEAN-001", "Normal",
       "Popup confirm xoá scenario: click Cancel → scenario KHÔNG bị xoá",
       BOT + "\n- Folder F1 có scenario S2",
       "1. Xoá S2 → click Cancel ở popup confirm\n2. Kiểm tra danh sách + DB",
       "Scenario S2",
       "- Popup đóng, S2 vẫn còn trong danh sách\n- DB: bản ghi scenario S2 còn nguyên",
       note="Nguồn: r363"),

    tc("Xóa scenario", "STATE-001", "Abnormal",
       "Sau khi xoá scenario → popup sort group scenario phải cập nhật NGAY, không cần reload",
       BOT + "\n- Folder F1 có 5 scenario",
       "1. Xoá S2\n2. KHÔNG reload trang, mở popup sort group scenario\n3. Đếm số scenario trong popup",
       "Xoá 1 trong 5 scenario",
       "- Popup sort chỉ còn 4 scenario, KHÔNG còn S2",
       spec="Đã hỏi leader",
       note="MT-12 — corpus r365 đánh **NG**:『phải reset mới mất』. TC dự kiến FAIL → cần raise bug. Nguồn: r365"),

    tc("Xóa scenario", "REG-SHARED-001", "Normal",
       "Sau khi xoá scenario → 7 điểm tham chiếu không còn scenario đã xoá trong dropdown",
       BOT8 + "\n- Vừa xoá scenario S2 (S2 đang được gắn vào 1 action ở Chat 1:1)",
       "1. Xoá S2\n2. Lần lượt mở: Chat 1:1 · Modal action · Message send all · Scenario · Remind · Calendar 5-1 · Bill tiền item 6\n"
       "3. Kiểm tra dropdown chọn scenario",
       "Xoá scenario S2 đang được gắn ở 1 action",
       "- Cả 7 điểm KHÔNG còn S2 trong dropdown chọn scenario",
       note="Nguồn: r366-r372"),

    tc("Xóa scenario", "DATA-CASCADE-001", "Normal",
       "Xoá scenario → cascade xoá đủ 8 nhóm dữ liệu liên quan theo BR-08",
       BOT + "\n- Scenario S1 có: 3 step (có template category_id = -111), 2 filter branch, "
       "5 friend đang chạy (có bản ghi scenario_step_time + step_message_history), 1 action gắn scenario ở màn khác",
       "1. Ghi lại id của: scenario, step_message, filter_manager, filters_v2, action_detail liên quan\n"
       "2. Xoá S1\n3. Query lần lượt: `scenario_step_time` (theo step ids) · `step_message` · `scenario` · "
       "`scenario_lineuser` · `step_message_history` · `filters_v2` (type='scenario', data chứa scenario_id) · "
       "`action_detail` (type='scenario', data.id = S1, action IN (2,3))",
       "S1 với 3 step, 2 filter, 5 friend đang chạy",
       "- Tất cả bản ghi ở 7 bảng trên KHÔNG còn dữ liệu của S1 (xoá vĩnh viễn, không soft delete)\n"
       "- Các action ở màn khác đang trỏ tới S1 được cleanup, không còn tham chiếu mồ côi",
       spec="Đã hỏi leader",
       note="MT-05 — corpus r374 / r388 để『Cần Confirm: xóa thành công thì xóa thông tin những bảng nào?』; "
            "spec BR-08 (feature-spec §7 mục 7 + logic-spec deletedDataScenario) liệt kê đủ 8 bước → **TC lấp Gap này**. "
            "Ghi chú corpus r174:『Nếu scenario đã được add trong action của send all, remind, calendar, template, bill tiền...』. Nguồn: r374, r388"),

    tc("Xóa scenario", "DATA-CASCADE-001", "Abnormal",
       "Xoá scenario ĐANG start cho friend → friend dừng nhận step, dữ liệu tiến trình bị xoá",
       BOT + "\n- S1 đang có 5 friend 購読中, còn 2 step chưa tới giờ gửi",
       "1. Ghi lại `scenario_step_time` pending của 5 friend\n2. Xoá S1\n"
       "3. Query `scenario_step_time` / `scenario_lineuser` / `step_message_history` của S1\n"
       "4. Chờ qua thời điểm của 2 step chưa gửi → kiểm tra LINE app của 5 friend\n5. Kiểm tra màn my_page của 1 friend",
       "5 friend đang chạy, còn 2 step (1 step sau 30 phút, 1 step ngày mai 10:00)",
       "- Bản ghi pending trong `scenario_step_time` bị xoá\n- 5 friend KHÔNG nhận thêm message nào từ S1\n"
       "- Màn my_page của friend không còn hiển thị scenario S1",
       spec="Đã hỏi leader",
       note="MT-05 — corpus r373 / r387 để『Cần Confirm: lúc này data như nào?』. Kết quả mong đợi suy từ spec BR-08. Nguồn: r373, r387"),

    tc("Xóa scenario", "BULK-001", "Normal",
       "Xoá hàng loạt 一括削除: default disable → tick scenario thì enable; popup xác nhận → xoá thành công",
       BOT + "\n- Folder F1 có 5 scenario",
       "1. Quan sát trạng thái button「一括削除」khi chưa tick gì\n2. Tick 3 scenario → quan sát button\n"
       "3. Click「一括削除」→ quan sát popup xác nhận\n4. Đồng ý xoá\n5. Kiểm tra danh sách + trạng thái button sau khi xoá",
       "Tick 3 trong 5 scenario",
       "- Chưa tick: button DISABLE\n- Tick: button ENABLE\n- Hiện popup xác nhận\n"
       "- Sau xoá: 3 scenario biến mất, còn 2 scenario; button「一括削除」quay về DISABLE",
       note="Nguồn: r375-r379"),

    tc("Xóa scenario", "BULK-001", "Normal",
       "Sau xoá hàng loạt: danh sách folder, popup sort và 5 điểm tham chiếu đều cập nhật",
       BOT8 + "\n- Vừa xoá hàng loạt 3 scenario ở folder F1",
       "1. Xoá hàng loạt 3 scenario\n2. Kiểm tra số scenario hiển thị cạnh folder F1\n"
       "3. Mở popup sort group scenario\n4. Kiểm tra 5 điểm: Chat 1:1 · Modal action · Message send all · Scenario · Remind",
       "Xoá 3 scenario",
       "- Số lượng cạnh folder F1 giảm đúng 3\n- Popup sort không còn 3 scenario đã xoá\n"
       "- Cả 5 điểm tham chiếu không còn 3 scenario đã xoá",
       note="Nguồn: r380-r386"),

    # ══════════════════════ 9. Chuyển folder ══════════════════════
    tc("Chuyển folder", "BULK-001", "Normal",
       "Button 一括フォルダ変更: default disable; tick scenario → enable + hiển thị text số mục đang chọn",
       BOT + "\n- Folder F1 có 5 scenario",
       "1. Quan sát button「一括フォルダ変更」khi chưa tick\n2. Tick 2 scenario\n3. Quan sát button + text hiển thị",
       "Tick 2 trong 5 scenario",
       "- Chưa tick: button DISABLE\n- Tick 2: button「一括フォルダ変更」và「一括削除」đều ENABLE\n"
       "- Hiển thị dòng text ghi ĐANG CHỌN 2 mục",
       note="Nguồn: r284, r285"),

    tc("Chuyển folder", "CONC-001", "Abnormal",
       "Double click button 一括フォルダ変更 → chỉ mở 1 popup",
       BOT + "\n- Đã tick 2 scenario",
       "1. Double click nhanh button「一括フォルダ変更」\n2. Đếm số popup",
       "—",
       "- Chỉ mở ĐÚNG 1 popup 一括フォルダ変更",
       note="Nguồn: r286"),

    tc("Chuyển folder", "LIST-001", "Normal",
       "Popup 一括フォルダ変更: default hiển thị 未分類; list folder dài có scroll và đúng thứ tự",
       BOT + "\n- Bot có 25 folder scenario",
       "1. Tick scenario → mở popup「一括フォルダ変更」\n2. Quan sát folder được chọn mặc định\n"
       "3. Scroll danh sách folder trong popup\n4. Đối chiếu thứ tự với panel folder ngoài",
       "25 folder scenario",
       "- Default chọn folder「未分類」\n- Popup có scroll, hiển thị đủ 25 folder\n- Thứ tự khớp panel folder ngoài",
       note="Nguồn: r287, r288"),

    tc("Chuyển folder", "BULK-001", "Normal",
       "Move 1 scenario từ 未分類 sang folder khác → scenario chuyển đúng, số lượng 2 folder thay đổi đúng",
       BOT + "\n- 未分類 có 6 scenario; folder F2 có 3 scenario",
       "1. Đứng ở 未分類, tick 1 scenario → 一括フォルダ変更 → chọn F2 → xác nhận\n"
       "2. Kiểm tra danh sách 未分類 và F2\n3. Kiểm tra số lượng hiển thị cạnh 2 folder\n"
       "4. Query `scenario`.`group_id` của scenario vừa move",
       "Move 1 scenario: 未分類 (6) → F2 (3)",
       "- Scenario chuyển sang F2, KHÔNG còn trong 未分類\n- 未分類: 6 → 5; F2: 3 → 4\n- DB: group_id = id của F2",
       note="Nguồn: r289"),

    tc("Chuyển folder", "BULK-001", "Normal",
       "Move TOÀN BỘ scenario của 1 trang sang folder khác → chuyển đủ, số lượng 2 folder khớp",
       BOT + "\n- Folder F1 có đúng 20 scenario (đầy 1 trang); folder F2 có 3 scenario",
       "1. Tick checkbox chọn tất cả ở đầu bảng (chọn cả 20)\n2. 一括フォルダ変更 → chọn F2 → xác nhận\n"
       "3. Kiểm tra F1 và F2\n4. Query COUNT `scenario` WHERE group_id = <F2>",
       "Move 20 scenario: F1 (20) → F2 (3)",
       "- F1 rỗng (0 scenario); F2 có 23 scenario\n- Số lượng cạnh folder: F1 = 0, F2 = 23\n- DB: 20 bản ghi có group_id = F2",
       note="Nguồn: r290"),

    tc("Chuyển folder", "BULK-001", "Normal",
       "Move scenario từ folder đã tạo về 未分類, và từ folder A sang folder B → đều đúng",
       BOT + "\n- Folder A có 4 scenario; folder B có 2 scenario; 未分類 có 5 scenario",
       "1. Move 1 scenario từ A về 未分類 → kiểm tra 2 folder\n2. Move 1 scenario từ A sang B → kiểm tra 2 folder\n"
       "3. Query `scenario`.`group_id` sau mỗi lần move",
       "A (4) → 未分類 (5); A (3) → B (2)",
       "- Lần 1: A còn 3, 未分類 thành 6, group_id = 0\n- Lần 2: A còn 2, B thành 3, group_id = id của B\n"
       "- Cả 2 lần: scenario KHÔNG còn trong folder cũ",
       note="2 hướng move cùng 1 kết quả → giữ chung. Nguồn: r291, r292"),

    tc("Chuyển folder", "STATE-CLEAN-001", "Normal",
       "Sau khi 一括フォルダ変更 thành công → button quay về trạng thái DISABLE và popup sort cập nhật",
       BOT + "\n- Vừa move 2 scenario sang folder khác",
       "1. Move 2 scenario sang folder F2\n2. Quan sát trạng thái button「一括フォルダ変更」\n"
       "3. Mở popup sort group scenario ở folder nguồn và folder đích",
       "Move 2 scenario",
       "- Button「一括フォルダ変更」về DISABLE (bỏ tick tự động)\n"
       "- Popup sort của folder nguồn không còn 2 scenario; popup sort folder đích có thêm 2 scenario",
       note="Nguồn: r293, r294"),

    tc("Chuyển folder", "REG-SHARED-001", "Normal",
       "Sau khi chuyển folder scenario → 8 điểm tham chiếu hiển thị scenario ở FOLDER MỚI, đúng thứ tự",
       BOT8 + "\n- Vừa move 2 scenario từ folder A sang folder B",
       "1. Move 2 scenario từ A sang B\n2. Lần lượt mở 8 điểm tham chiếu, mở dropdown chọn scenario theo folder\n"
       "3. Kiểm tra 2 scenario nằm ở folder nào",
       "8 điểm: Chat 1:1 · Modal action · Message send all · Button · Scenario · Remind · Calendar 5-1 · Bill tiền item 6",
       "- Cả 8 điểm: 2 scenario xuất hiện dưới folder B, không còn dưới folder A\n"
       "- Tin nhắn gửi đi có đủ, đúng thứ tự các scenario có trong folder",
       note="Nguồn: r295-r302"),
]
