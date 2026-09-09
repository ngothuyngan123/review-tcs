# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 2: modal quick action, profile người gửi, header, CRUD 対応ステータス."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3"
QA = (BOT + "\n- Friend A, B, C là bạn bè của bot A\n"
      "- Đã click vào avatar của friend để mở modal クイックアクション")
TAGSET = "- Folder tag F1 có T1, T2; folder F2 có T3"

S2 = [
    # ═══════════════ Quick action — bookmark & 対応ステータス ═══════════════
    tc("Quick action — bookmark & 対応ステータス", "UI-001", "Normal",
       "Click avatar bạn bè — mở modal クイックアクション, hiện số bạn bè đã chọn",
       BOT + "\n- Friend A, B là bạn bè của bot",
       "1. Click vào avatar của friend A trong danh sách\n2. Quan sát modal mở ra\n"
       "3. Tick thêm avatar của friend B\n4. Đọc dòng 選択中のユーザー",
       "Chọn 1 friend, sau đó 2 friend",
       "- Modal クイックアクション mở ra với 5 nhóm action: ブックマーク / 対応ステータス変更 / "
       "確認状況を変更 / 非表示・ブロック / タグ編集\n"
       "- 選択中のユーザー hiển thị đúng số bạn bè đang chọn (1 rồi 2)",
       note="Nguồn: Leftbar+Header r198, r200"),

    tc("Quick action — bookmark & 対応ステータス", "UI-INPUT-001", "Abnormal",
       "Không chọn action nào mà bấm thực thi — hiện validate",
       QA,
       "1. Mở modal クイックアクション cho friend A\n2. Không tick action nào\n3. Click nút 実行する",
       "0 action được chọn",
       "- Hiển thị thông báo 「アクションを選択してください。」\n"
       "- Modal không đóng, không thay đổi dữ liệu friend A",
       note="Nguồn: Leftbar+Header r201"),

    tc("Quick action — bookmark & 対応ステータス", "UI-004", "Normal",
       "Đóng modal クイックアクション bằng nút X — không thực thi gì",
       QA + "\n- Friend A chưa bookmark",
       "1. Tick option ブックマークする\n2. KHÔNG click 実行する, click X đóng modal\n"
       "3. Quan sát trạng thái bookmark của A\n4. Mở lại modal, kiểm tra tick",
       "Tick bookmark rồi đóng X",
       "- A vẫn ở trạng thái chưa bookmark\n- Mở lại modal: không option nào còn tick (modal reset)",
       note="Nguồn: Leftbar+Header r202, r204, r211"),

    tc("Quick action — bookmark & 対応ステータス", "UI-003", "Normal",
       "Nhóm ブックマーク — mặc định không tick, có đúng 2 lựa chọn",
       QA,
       "1. Mở modal クイックアクション\n2. Quan sát nhóm ブックマーク",
       "Modal vừa mở",
       "- Nhóm ブックマーク có đúng 2 lựa chọn: 「ブックマークする」và「ブックマークを外す」\n"
       "- Mặc định KHÔNG lựa chọn nào được tick",
       note="Nguồn: Leftbar+Header r203"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "ブックマークする — bạn bè chưa bookmark thì được thêm bookmark",
       QA + "\n- Friend A CHƯA bookmark",
       "1. Tick ブックマークする\n2. Click 実行する\n3. Quan sát dòng của A trong danh sách\n"
       "4. Kiểm tra DB: SELECT is_bookmark FROM conversation WHERE ... (A)",
       "Friend A chưa bookmark",
       "- Dòng A hiện icon bookmark góc trên bên phải\n- A được đẩy lên đầu danh sách\n"
       "- DB: conversation.is_bookmark = 1",
       note="Verify DB + màn hình. Nguồn: Leftbar+Header r205"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "ブックマークする với bạn bè ĐÃ bookmark — giữ nguyên, không lỗi",
       QA + "\n- Friend B ĐÃ bookmark",
       "1. Mở modal cho B, tick ブックマークする\n2. Click 実行する\n3. Kiểm tra trạng thái và DB",
       "Friend B đã bookmark",
       "- B vẫn ở trạng thái đã bookmark, is_bookmark vẫn = 1\n- Không lỗi, không nhân đôi bản ghi",
       note="Nguồn: Leftbar+Header r206"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "ブックマークを外す — gỡ bookmark của bạn bè đang bookmark",
       QA + "\n- Friend B ĐÃ bookmark",
       "1. Tick ブックマークを外す\n2. Click 実行する\n3. Quan sát dòng B và DB",
       "Friend B đã bookmark",
       "- Icon bookmark của B biến mất, B rời khỏi cụm đầu danh sách\n- DB: is_bookmark = 0",
       note="Nguồn: Leftbar+Header r208"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "ブックマークを外す với bạn bè CHƯA bookmark — giữ nguyên",
       QA + "\n- Friend A CHƯA bookmark",
       "1. Tick ブックマークを外す\n2. Click 実行する\n3. Kiểm tra trạng thái và DB",
       "Friend A chưa bookmark",
       "- A vẫn chưa bookmark, is_bookmark vẫn = 0, không lỗi",
       note="Nguồn: Leftbar+Header r207"),

    tc("Quick action — bookmark & 対応ステータス", "UI-INPUT-001", "Boundary",
       "Nhóm ブックマーク chỉ cho chọn 1 lựa chọn — tick cái sau bỏ cái trước",
       QA,
       "1. Tick ブックマークする\n2. Tick tiếp ブックマークを外す\n3. Quan sát 2 ô tick\n4. Click 実行する",
       "Tick lần lượt 2 option",
       "- Chỉ ブックマークを外す còn tick, ブックマークする tự bỏ tick\n"
       "- Kết quả thực thi theo option chọn sau cùng (gỡ bookmark)",
       note="Nguồn: Leftbar+Header r209, r210"),

    tc("Quick action — bookmark & 対応ステータス", "BULK-001", "Normal",
       "Bookmark hàng loạt — chọn nhiều bạn bè rồi thực thi",
       BOT + "\n- Friend A, B, C đều CHƯA bookmark",
       "1. Tick avatar của A, B, C\n2. Ở modal: tick ブックマークする\n3. Click 実行する\n"
       "4. Quan sát danh sách + kiểm tra is_bookmark của cả 3",
       "3 friend chưa bookmark",
       "- Cả 3 friend đều hiện icon bookmark và lên đầu danh sách\n- DB: is_bookmark = 1 cho đủ 3 bản ghi",
       note="Nguồn: Leftbar+Header r213, r312"),

    tc("Quick action — bookmark & 対応ステータス", "UI-003", "Normal",
       "Nhóm 対応ステータス変更 — hiển thị đủ danh sách status kèm lựa chọn 「なし」",
       QA + "\n- Bot A có 5 status mặc định + status tự tạo「保留」",
       "1. Mở modal クイックアクション\n2. Quan sát nhóm 対応ステータス変更",
       "6 status + tuỳ chọn xoá status",
       "- Có lựa chọn 「対応ステータスなし」 + đủ 6 status theo đúng thứ tự ở màn cài đặt\n"
       "- Mặc định không lựa chọn nào được tick",
       note="Nguồn: Leftbar+Header r214"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "Gán 対応ステータス cho bạn bè chưa có status và cho bạn bè đang có status khác",
       QA + "\n- Friend A không có status\n- Friend B đang có status「トラブル」",
       "1. Mở modal cho A: tick status「対応中」→ 実行する → kiểm tra badge của A\n"
       "2. Mở modal cho B: tick status「対応中」→ 実行する → kiểm tra badge của B\n"
       "3. Kiểm tra DB: SELECT id_status FROM conversation",
       "Status đích: 対応中",
       "- Cả A và B đều chuyển sang badge「対応中」đúng màu\n- DB: id_status của cả 2 trỏ tới status 対応中",
       note="Gộp 2 điểm vì cùng kết quả. Nguồn: Leftbar+Header r216, r217"),

    tc("Quick action — bookmark & 対応ステータス", "FUNC-001", "Normal",
       "Gán lại đúng status bạn bè đang có — giữ nguyên, không lỗi",
       QA + "\n- Friend C đang có status「対応中」",
       "1. Mở modal cho C, tick status「対応中」\n2. Click 実行する\n3. Kiểm tra badge và id_status",
       "Friend C đã có status 対応中",
       "- C vẫn ở status 対応中, id_status không đổi, không lỗi",
       note="Nguồn: Leftbar+Header r218"),

    tc("Quick action — bookmark & 対応ステータス", "BULK-001", "Normal",
       "Gán 対応ステータス hàng loạt — áp dụng cho mọi bạn bè đã chọn",
       BOT + "\n- Friend A (không status), B (トラブル), C (対応中)",
       "1. Tick avatar A, B, C\n2. Tick status「フォロー」\n3. Click 実行する\n4. Kiểm tra badge của cả 3 + DB",
       "3 friend với 3 trạng thái status khác nhau",
       "- Cả 3 đều chuyển sang badge「フォロー」\n- DB: id_status của cả 3 trỏ tới status フォロー",
       note="Nguồn: Leftbar+Header r223"),

    # ═══════════════ Quick action — xác nhận, ẩn, block ═══════════════
    tc("Quick action — xác nhận, ẩn, block", "UI-003", "Normal",
       "Nhóm 確認状況を変更 — đúng 2 lựa chọn, mặc định không tick",
       QA,
       "1. Mở modal クイックアクション\n2. Quan sát nhóm 確認状況を変更",
       "Modal vừa mở",
       "- Có đúng 2 lựa chọn: 「確認済」に変更 và 「未確認」に変更\n- Mặc định không tick",
       note="Nguồn: Leftbar+Header r224"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "「確認済」に変更 — bạn bè chưa xác nhận chuyển sang đã xác nhận, badge menu giảm",
       QA + "\n- Friend A có 3 tin chưa xác nhận\n- Ghi lại badge số tin chưa đọc ở menu 1:1チャット",
       "1. Tick 「確認済」に変更\n2. Click 実行する\n3. Quan sát dòng A, badge menu (không reload)\n"
       "4. Kiểm tra DB: confirm_count của A và bots.count_user_unconfirm",
       "Friend A: 3 tin chưa xác nhận",
       "- Chấm xanh của A biến mất realtime, không cần F5\n"
       "- Badge ở menu 1:1チャット giảm đi 1 (số bạn bè chưa xác nhận)\n"
       "- DB: conversation.confirm_count = 0; bots.count_user_unconfirm giảm 1",
       note="Verify 3 tầng DB + danh sách + badge menu (RULE-07). Nguồn: Leftbar+Header r80-r83, r227"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "「未確認」に変更 — bạn bè đã xác nhận chuyển ngược lại chưa xác nhận",
       QA + "\n- Friend B đã xác nhận hết tin (confirm_count = 0), có ≥1 tin nhắn từ friend",
       "1. Tick 「未確認」に変更\n2. Click 実行する\n3. Quan sát dòng B và badge menu\n"
       "4. Kiểm tra DB: confirm_count, has_status_0, has_status_1, bảng unconfirm_message",
       "Friend B đã xác nhận",
       "- Dòng B hiện lại chấm xanh, badge menu tăng 1\n"
       "- DB: confirm_count > 0, has_status_0 = 1, has_status_1 = 0\n"
       "- Bảng unconfirm_message có bản ghi message_id của hội thoại B",
       note="Nguồn: Leftbar+Header r228, r75-r79 + improve count comfirm_message r49-r52"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "Đổi trạng thái xác nhận về đúng trạng thái đang có — giữ nguyên",
       QA + "\n- Friend A đã xác nhận, friend B chưa xác nhận",
       "1. Với A: tick 「確認済」に変更 → 実行する → kiểm tra\n"
       "2. Với B: tick 「未確認」に変更 → 実行する → kiểm tra",
       "A đã xác nhận · B chưa xác nhận",
       "- A vẫn đã xác nhận, B vẫn chưa xác nhận\n- confirm_count không đổi, không lỗi, badge menu không đổi",
       note="Gộp 2 điểm vì cùng kết quả. Nguồn: Leftbar+Header r226, r229"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "Đổi trạng thái xác nhận cho NHÓM LINE — hoạt động như bạn bè cá nhân",
       BOT + "\n- Nhóm G1 có 2 tin chưa xác nhận",
       "1. Tick avatar nhóm G1 → modal クイックアクション\n2. Tick 「確認済」に変更 → 実行する\n"
       "3. Kiểm tra dòng G1, badge menu, DB confirm_count + bots.count_user_unconfirm\n"
       "4. Lặp lại với 「未確認」に変更",
       "Nhóm G1: 2 tin chưa xác nhận",
       "- Nhóm G1 chuyển đúng trạng thái xác nhận như friend cá nhân\n"
       "- Badge menu và bots.count_user_unconfirm cập nhật đúng cho cả nhóm",
       note="Nguồn: Leftbar+Header r84-r92"),

    tc("Quick action — xác nhận, ẩn, block", "UI-003", "Normal",
       "Nhóm 非表示・ブロック — đúng 2 lựa chọn 非表示にする / ブロックする",
       QA,
       "1. Mở modal クイックアクション\n2. Quan sát nhóm 非表示・ブロック",
       "Modal vừa mở",
       "- Có đúng 2 lựa chọn: 「非表示にする」và「ブロックする」\n- Mặc định không tick",
       note="Nguồn: Leftbar+Header r235"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "非表示にする — bạn bè bị ẩn khỏi danh sách và có message hệ thống",
       QA + "\n- Friend A đang hiển thị bình thường",
       "1. Tick 非表示にする → 実行する\n2. Quan sát danh sách với filter 全ての友だち và filter 非表示中\n"
       "3. Mở hội thoại A xem message hệ thống\n"
       "4. Kiểm tra DB: is_hide, datetime_hide của conversation A",
       "Friend A đang hiển thị",
       "- A biến mất khỏi filter 全ての友だち, xuất hiện ở filter 非表示中\n"
       "- Khung hội thoại A có message hệ thống「非表示しました」kèm tên staff và ngày giờ ẩn\n"
       "- DB: is_hide = 1, datetime_hide có giá trị",
       note="Nguồn: Leftbar+Header r237 + Content: Hiển thị msg r66-r68"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "非表示にする với bạn bè ĐANG ẩn hoặc đang bị block — vẫn ẩn, không lỗi",
       BOT + "\n- Friend D đang ẩn\n- Friend E bị bot block\n- Friend F đã block bot",
       "1. Với từng friend D, E, F: mở modal quick action, tick 非表示にする → 実行する\n"
       "2. Kiểm tra trạng thái ẩn và nội dung hội thoại của từng friend",
       "D đang ẩn · E bot block friend · F friend block bot",
       "- Cả 3 đều ở trạng thái ẩn (is_hide = 1), không lỗi\n"
       "- E và F: hội thoại vẫn hiển thị message block kèm thời gian block",
       note="Gộp 3 điểm vì cùng kết quả. Nguồn: Leftbar+Header r238-r240"),

    tc("Quick action — xác nhận, ẩn, block", "STATE-DEP-001", "Abnormal",
       "Ẩn bạn bè đang có tin CHƯA xác nhận — tin tự động chuyển thành đã xác nhận",
       QA + "\n- Friend G có 3 tin chưa xác nhận, đang hiển thị bình thường",
       "1. Ghi lại confirm_count của G và badge menu\n2. Tick 非表示にする → 実行する\n"
       "3. Chọn filter 非表示中, quan sát dòng G\n"
       "4. Kiểm tra DB: confirm_count, has_status_0/1 của G, bots.count_user_unconfirm, bảng unconfirm_message",
       "Friend G: 3 tin chưa xác nhận",
       "- G không còn chấm xanh chưa đọc\n"
       "- DB: confirm_count = 0, has_status_1 = 1, has_status_0 = 0\n"
       "- Bản ghi unconfirm_message của G bị xoá; bots.count_user_unconfirm giảm 1",
       spec="Đã hỏi leader",
       note="MT-08: hành vi này khớp BR-05 (feature-spec.md:467) nhưng TC gốc ghi 「spec cũ là ẩn đi thì sẽ confirm」 "
            "→ cần Leader chốt còn đúng không. Nguồn: Leftbar+Header r241 + improve count comfirm_message r31"),

    tc("Quick action — xác nhận, ẩn, block", "FUNC-001", "Normal",
       "ブロックする — bot block bạn bè, hội thoại hiện message block",
       QA + "\n- Friend H đang bình thường",
       "1. Tick ブロックする → 実行する\n2. Mở hội thoại H, quan sát message hệ thống\n"
       "3. Thử gõ và gửi tin nhắn cho H\n4. Kiểm tra DB: is_blocked của conversation H",
       "Friend H",
       "- Hội thoại H có message hệ thống「ブロックしました」kèm tên staff và ngày giờ\n"
       "- Không gửi được tin nhắn cho H\n- DB: conversation.is_blocked = 1",
       note="Nguồn: Leftbar+Header r242 + Content: Hiển thị msg r44-r46, r52"),

    tc("Quick action — xác nhận, ẩn, block", "STATE-DEP-001", "Abnormal",
       "Sau khi block — action nào còn chạy, action nào bị chặn",
       BOT + "\n- Friend H vừa bị bot block",
       "1. Mở modal quick action cho H\n"
       "2. Lần lượt thực thi từng action ở cột Dữ liệu test\n3. Ghi nhận action nào có hiệu lực",
       "5 action: ブックマーク · 対応ステータス変更 · 確認状況を変更 · 非表示 · タグ編集",
       "- ブックマーク, 対応ステータス変更, 非表示: THỰC HIỆN ĐƯỢC, dữ liệu thay đổi đúng\n"
       "- 確認状況を変更 và タグ編集: KHÔNG thực hiện được với bạn bè đã bị block",
       spec="Spec không ghi",
       note="Spec chat-11 chỉ có BR-09 chặn GỬI TIN khi block, không nói action nào bị chặn. "
            "Nguồn: Leftbar+Header r243-r247, r284"),

    tc("Quick action — xác nhận, ẩn, block", "BULK-001", "Normal",
       "Ẩn / block hàng loạt nhiều bạn bè cùng lúc",
       BOT + "\n- Friend A, B, C đang hiển thị bình thường",
       "1. Tick avatar A, B, C\n2. Tick 非表示にする → 実行する → kiểm tra cả 3\n"
       "3. Bỏ ẩn 3 friend, làm lại với ブロックする",
       "3 friend",
       "- Ẩn hàng loạt: cả 3 chuyển is_hide = 1, biến mất khỏi filter 全ての友だち\n"
       "- Block hàng loạt: cả 3 chuyển is_blocked = 1, hội thoại đều có message block",
       note="Nguồn: Leftbar+Header r252, r536, r537"),

    # ═══════════════ Quick action — tag & kết hợp action ═══════════════
    tc("Quick action — tag & kết hợp action", "UI-003", "Normal",
       "Nhóm タグ編集 — 2 tab つける / はずす, bắt buộc chọn tab mới thao tác được",
       QA + "\n" + TAGSET,
       "1. Mở modal クイックアクション → nhóm タグ編集\n2. Quan sát 2 tab và trạng thái mặc định\n"
       "3. Kiểm tra danh sách folder/tag hiển thị, thử cuộn khi nhiều tag",
       TAGSET,
       "- Có 2 tab: 「つける」(gắn tag) và「はずす」(gỡ tag), mặc định KHÔNG tab nào được tick\n"
       "- Hiện đủ folder và tag đúng thứ tự như màn Quản lý thẻ, nhiều tag thì có scroll",
       note="Nguồn: Leftbar+Header r253-r255"),

    tc("Quick action — tag & kết hợp action", "FUNC-001", "Normal",
       "Gắn tag qua quick action — chọn tab つける + chọn tag rồi thực thi",
       QA + "\n" + TAGSET + "\n- Friend A chưa có tag nào",
       "1. Ở nhóm タグ編集: tick tab つける\n2. Chọn tag T1 (và thử thêm T2 cùng folder, T3 khác folder)\n"
       "3. Click 実行する\n4. Kiểm tra tab タグ管理 ở cột phải và DB tag_line_user",
       "T1, T2 (folder F1), T3 (folder F2)",
       "- Tag đã chọn được gắn cho A, hiển thị ở tab タグ管理 của cột phải\n"
       "- DB: bảng tag_line_user có bản ghi cho từng tag đã chọn\n"
       "- Chọn nhiều tag cùng folder hay khác folder đều gắn đủ",
       note="Gộp 3 điểm (1 tag / nhiều tag cùng folder / nhiều tag khác folder) vì cùng kết quả. "
            "Nguồn: Leftbar+Header r257-r259"),

    tc("Quick action — tag & kết hợp action", "UI-INPUT-001", "Abnormal",
       "Chọn tag nhưng KHÔNG tick tab つける — không gắn được tag",
       QA + "\n" + TAGSET + "\n- Friend A chưa có tag",
       "1. KHÔNG tick tab つける\n2. Chọn tag T1\n3. Click 実行する\n"
       "4. Kiểm tra tab タグ管理 của A và DB tag_line_user",
       "Chọn tag mà không chọn tab",
       "- Tag T1 KHÔNG được gắn cho A\n- Không có bản ghi mới trong tag_line_user",
       note="Nguồn: Leftbar+Header r264"),

    tc("Quick action — tag & kết hợp action", "MSG-001", "Normal",
       "Gắn tag có cài đặt action gửi tin — bạn bè nhận tin, tag chỉ hiển thị 1 lần",
       QA + "\n" + TAGSET + "\n- Tag T1 có action gửi tin nhắn text, cho phép gửi nhiều lần\n- Friend A ĐÃ có tag T1",
       "1. Ở modal quick action: tick つける, chọn T1 (tag A đã có)\n2. Click 実行する\n"
       "3. Kiểm tra app LINE của friend A\n4. Kiểm tra tab タグ管理 của A",
       "Tag T1 có action gửi tin, gửi nhiều lần",
       "- Friend A NHẬN được tin nhắn của action (dù đã có tag)\n"
       "- Tab タグ管理 chỉ hiển thị T1 MỘT lần, không nhân đôi\n"
       "- Chat 1:1 hiển thị tin vừa gửi kèm marker action",
       note="Đi tới output cuối (app LINE) theo RULE-06. Nguồn: Leftbar+Header r260"),

    tc("Quick action — tag & kết hợp action", "UI-INPUT-001", "Abnormal",
       "Chọn tag rồi bỏ chọn hết, không chọn tag mới — hiện validate",
       QA + "\n" + TAGSET,
       "1. Tick tab つける, chọn T1\n2. Bỏ chọn T1, không chọn tag khác\n3. Click 実行する",
       "Chọn rồi bỏ chọn hết tag",
       "- Hiện thông báo validate, không thực thi\n- Không thay đổi tag của friend",
       note="Nguồn: Leftbar+Header r262, r274"),

    tc("Quick action — tag & kết hợp action", "UI-002", "Normal",
       "Khu vực 選択したタグ — hiển thị tag đang chọn, cuộn ngang khi nhiều, bỏ tag đồng bộ 2 nơi",
       QA + "\n- Bot A có ≥10 tag ở nhiều folder",
       "1. Tick tab つける, chọn 8 tag ở nhiều folder\n2. Quan sát khu vực 選択したタグ\n"
       "3. Bấm bỏ 1 tag ngay tại khu vực 選択したタグ\n4. Kiểm tra tick của tag đó trong danh sách folder",
       "8 tag ở nhiều folder",
       "- 選択したタグ hiển thị đủ 8 tag, có scroll ngang khi tràn\n"
       "- Bỏ tag ở 選択したタグ thì tick của tag đó trong folder cũng bị bỏ theo (đồng bộ 2 nơi)",
       note="Nguồn: Leftbar+Header r265-r267"),

    tc("Quick action — tag & kết hợp action", "FUNC-001", "Normal",
       "Gỡ tag qua tab はずす — gỡ đúng tag đã chọn",
       QA + "\n" + TAGSET + "\n- Friend A đang có T1, T2, T3",
       "1. Tick tab はずす\n2. Chọn T1 (thử thêm nhiều tag cùng folder, khác folder)\n3. Click 実行する\n"
       "4. Kiểm tra tab タグ管理 của A và DB tag_line_user",
       "Gỡ T1; gỡ T1+T2 (cùng folder); gỡ T1+T3 (khác folder)",
       "- Tag đã chọn bị gỡ khỏi A, biến mất ở tab タグ管理\n"
       "- DB: bản ghi tag_line_user tương ứng bị xoá; tag KHÔNG chọn vẫn còn nguyên",
       note="Gộp 3 điểm vì cùng kết quả. Nguồn: Leftbar+Header r271-r273"),

    tc("Quick action — tag & kết hợp action", "FUNC-001", "Abnormal",
       "Gỡ tag mà bạn bè KHÔNG có — không ảnh hưởng gì",
       QA + "\n" + TAGSET + "\n- Friend B không có tag T3",
       "1. Tick tab はずす, chọn T3\n2. Click 実行する\n3. Kiểm tra tag hiện có của B",
       "Gỡ tag mà friend không có",
       "- Không lỗi, danh sách tag của B không đổi\n- Không xoá nhầm tag khác",
       note="Nguồn: Leftbar+Header r269"),

    tc("Quick action — tag & kết hợp action", "DATA-REF-001", "Normal",
       "Xoá tag ở màn Quản lý thẻ — bạn bè đang gắn tag đó mất tag ở chat 1:1",
       BOT + "\n" + TAGSET + "\n- Friend A đang gắn T1",
       "1. Ghi lại tag của A ở tab タグ管理\n2. Sang màn Quản lý thẻ, xoá tag T1\n"
       "3. Quay lại chat 1:1, mở lại tab タグ管理 của A\n4. Mở modal quick action → nhóm タグ編集",
       "Xoá tag T1 khỏi hệ thống",
       "- Tab タグ管理 của A không còn T1\n- Modal quick action cũng không còn T1 trong danh sách chọn",
       note="Nguồn: Leftbar+Header r280"),

    tc("Quick action — tag & kết hợp action", "FUNC-MULTI-001", "Normal",
       "Kết hợp nhiều action trong 1 lần thực thi — tất cả đều được áp dụng",
       BOT + "\n" + TAGSET + "\n- Friend A: chưa bookmark, không status, chưa xác nhận, đang hiển thị, chưa có tag",
       "1. Mở modal quick action cho A\n"
       "2. Tick đồng thời các action ở cột Dữ liệu test\n3. Click 実行する\n"
       "4. Kiểm tra từng kết quả: bookmark, status, trạng thái xác nhận, ẩn, tag",
       "Tổ hợp 2 action: (bookmark + status) · (bookmark + xác nhận) · (bookmark + ẩn) · (bookmark + tag) · "
       "(status + xác nhận) · (status + ẩn/block) · (status + tag) · (xác nhận + tag) · (ẩn/block + tag)\n"
       "Tổ hợp 3 action, 4 action và cả 5 action cùng lúc",
       "- Mọi tổ hợp: TẤT CẢ action được tick đều có hiệu lực đúng, không action nào bị bỏ qua\n"
       "- Kết quả kiểm tra được ở 3 nơi: danh sách bạn bè, khung hội thoại, tab タグ管理",
       note="Gộp các tổ hợp vì cùng kết quả 「áp dụng option vừa chọn」. Riêng tổ hợp có ブロック xem TC block. "
            "Nguồn: Leftbar+Header r281-r311"),

    tc("Quick action — tag & kết hợp action", "STATE-DEP-001", "Abnormal",
       "Kết hợp 確認状況を変更 =「未確認」với 非表示 — kết quả ngược với lựa chọn",
       BOT + "\n- Friend I đang có tin chưa xác nhận, đang hiển thị bình thường",
       "1. Mở modal quick action cho I\n2. Tick 「未確認」に変更 VÀ 非表示にする cùng lúc\n"
       "3. Click 実行する\n4. Chọn filter 非表示中, kiểm tra trạng thái xác nhận của I và DB confirm_count",
       "Chọn 未確認 + 非表示 cùng lúc",
       "- Ghi nhận kết quả thực tế và đối chiếu với quyết định của Leader ở MT-08\n"
       "- Theo hành vi hiện tại: I bị ẩn VÀ chuyển thành ĐÃ xác nhận (ngược với lựa chọn 未確認)",
       spec="Đã hỏi leader",
       note="MT-08: TC gốc ghi 「chọn option chưa confirm nhưng friend vẫn bị hiển thị đã confirm là đúng」 — "
            "người dùng chọn 未確認 mà nhận kết quả ngược. Nguồn: Leftbar+Header r289"),

    tc("Quick action — tag & kết hợp action", "CONC-001", "Abnormal",
       "Double click nút 実行する — chỉ thực thi 1 lần",
       QA + "\n" + TAGSET + "\n- Tag T1 có action gửi tin nhắn",
       "1. Tick tab つける + tag T1\n2. Double click nhanh nút 実行する\n"
       "3. Kiểm tra Network, tab タグ管理 của friend, và app LINE của friend",
       "Double click trong < 300ms, tag có action gửi tin",
       "- Chỉ 1 request được gửi\n- Tag chỉ gắn 1 lần\n- Friend chỉ nhận 1 tin nhắn action, không nhận 2 tin",
       note="Đi tới output cuối app LINE (RULE-06). Nguồn: Leftbar+Header r212, r222, r233, r251, r263, r275"),

    # ═══════════════ Profile người gửi — quản lý ═══════════════
    tc("Profile người gửi — quản lý", "UI-001", "Normal",
       "Icon cài đặt cạnh 送信ユーザー名 — đổi màu khi click và mở đúng 2 lựa chọn",
       BOT,
       "1. Quan sát khu vực 送信ユーザー名 phía trên ô nhập tin, đọc màu icon cài đặt\n"
       "2. Click vào icon\n3. Quan sát menu bung ra",
       "Trạng thái mặc định của màn chat",
       "- Mặc định icon màu xám\n"
       "- Sau khi click: icon chuyển xanh, hiện 2 lựa chọn 「送信者名を変更」và「チャット設定を開く」",
       note="Nguồn: Leftbar+Header r318, r319"),

    tc("Profile người gửi — quản lý", "UI-001", "Normal",
       "Modal 送信者名を変更 — hiển thị danh sách profile, có scroll khi nhiều",
       BOT + "\n- Bot A có profile mặc định 初期設定 + 6 profile tự tạo (3 có ảnh, 3 không ảnh, có tên ngắn và tên dài)",
       "1. Click icon cài đặt → 送信者名を変更\n2. Quan sát modal: nền tối phía sau, modal căn giữa\n"
       "3. Đọc danh sách profile, thử cuộn\n4. Quan sát avatar và tên của từng profile",
       "7 profile (1 mặc định + 6 tự tạo)",
       "- Modal căn giữa, nền phía sau tối\n- Hiện đủ 7 profile, danh sách dài thì có scroll\n"
       "- Profile có ảnh hiện đúng ảnh; profile không ảnh hiện ảnh mặc định\n"
       "- Tên dài không vỡ layout\n- Mặc định đang chọn 初期設定 (profile gốc của bot)",
       note="Nguồn: Leftbar+Header r320-r327"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Normal",
       "Đổi profile người gửi — 送信ユーザー名 và DB cập nhật theo profile đã chọn",
       BOT + "\n- Bot A có profile P1 (có ảnh, tên「営業 山田」)",
       "1. Mở modal 送信者名を変更, chọn P1\n2. Click 変更する\n"
       "3. Quan sát khu vực 送信ユーザー名 ở màn chat\n"
       "4. Gửi 1 tin nhắn cho friend, kiểm tra hiển thị ở chat 1:1 và trên app LINE của friend",
       "Profile P1: tên「営業 山田」, có ảnh",
       "- 送信ユーザー名 hiển thị「営業 山田」\n"
       "- Tin nhắn vừa gửi hiển thị tên + avatar của P1 ở chat 1:1\n"
       "- Trên app LINE, friend thấy tên + avatar của P1",
       note="Đi tới output cuối app LINE (RULE-06). Nguồn: Leftbar+Header r329"),

    tc("Profile người gửi — quản lý", "UI-INPUT-001", "Boundary",
       "Modal chọn profile — chỉ chọn được 1 profile tại một thời điểm",
       BOT + "\n- Bot A có ≥3 profile",
       "1. Mở modal 送信者名を変更\n2. Chọn P1 rồi chọn tiếp P2\n3. Quan sát trạng thái chọn\n4. Click 変更する",
       "Chọn lần lượt P1 rồi P2",
       "- Chỉ P2 còn được chọn, P1 tự bỏ chọn\n- 送信ユーザー名 đổi theo P2 (profile chọn sau cùng)",
       note="Nguồn: Leftbar+Header r330, r331"),

    tc("Profile người gửi — quản lý", "STATE-CLEAN-001", "Abnormal",
       "Chọn profile rồi đóng modal bằng X — không đổi profile",
       BOT + "\n- Đang dùng profile 初期設定",
       "1. Mở modal 送信者名を変更, chọn P1\n2. KHÔNG click 変更する, click X đóng modal\n"
       "3. Quan sát 送信ユーザー名\n4. Mở lại modal kiểm tra profile đang chọn",
       "Chọn P1 rồi đóng X",
       "- 送信ユーザー名 vẫn là profile 初期設定\n- Mở lại modal: 初期設定 vẫn đang được chọn",
       note="Nguồn: Leftbar+Header r328"),

    tc("Profile người gửi — quản lý", "UI-INPUT-001", "Abnormal",
       "Thêm profile — validate ảnh 送信ユーザー画像 chỉ nhận PNG",
       BOT,
       "1. Click ＋追加 mở modal 送信ユーザーの新規追加\n"
       "2. Lần lượt thử upload từng file ở cột Dữ liệu test\n3. Ghi nhận kết quả từng lần",
       "PNG hợp lệ · PNG có tên file tiếng Nhật · PNG có tên chứa khoảng trắng · JPG · GIF · JPEG",
       "- 3 file PNG (kể cả tên tiếng Nhật / có khoảng trắng): upload thành công\n"
       "- JPG, GIF, JPEG: hiện thông báo「png画像を選択してください。」hoặc không hiện file để chọn\n"
       "- Ảnh không bắt buộc: bỏ trống vẫn lưu được profile",
       spec="Đã hỏi leader",
       note="MT-11: chỗ này chỉ nhận PNG nhưng upload ảnh ở friend info (Rightbar r112) lại nhận cả PNG và JPG. "
            "Nguồn: Leftbar+Header r343-r348"),

    tc("Profile người gửi — quản lý", "UI-INPUT-001", "Abnormal",
       "Thêm profile — 送信ユーザー名 là trường bắt buộc, tự trim khoảng trắng",
       BOT,
       "1. Mở modal 送信ユーザーの新規追加\n2. Lần lượt nhập từng giá trị ở cột Dữ liệu test rồi bấm 保存\n"
       "3. Ghi nhận thông báo lỗi hoặc kết quả lưu",
       "Bỏ trống · chỉ nhập khoảng trắng · 1 ký tự · tên tiếng Nhật · tên có khoảng trắng đầu và cuối",
       "- Bỏ trống: hiện「送信ユーザー名を入力してください。」, không lưu\n"
       "- Chỉ khoảng trắng: hiện thông báo validate, không lưu\n"
       "- 1 ký tự và tên tiếng Nhật: lưu thành công\n"
       "- Tên có khoảng trắng đầu/cuối: tự trim rồi mới lưu",
       note="Nguồn: Leftbar+Header r349-r358"),

    tc("Profile người gửi — quản lý", "UI-INPUT-001", "Boundary",
       "Giới hạn độ dài 送信ユーザー名 — xác định ngưỡng thực tế",
       BOT,
       "1. Mở modal 送信ユーザーの新規追加\n"
       "2. Nhập lần lượt các độ dài ở cột Dữ liệu test (dùng ký tự latinh và ký tự tiếng Nhật)\n"
       "3. Ghi nhận: ký tự thứ mấy thì không gõ được nữa; ở độ dài nào thì báo lỗi khi bấm 保存\n"
       "4. Kiểm tra giá trị thực lưu trong DB bots_profiles.nick_name",
       "Độ dài: 1 · 19 · 20 · 21 · 30 · 31 ký tự — thử cả latinh và tiếng Nhật",
       "- Ghi nhận ngưỡng thực tế và đối chiếu với quyết định của Leader ở MT-07\n"
       "- Ở ngưỡng vượt giới hạn: phải chặn nhập hoặc báo lỗi rõ ràng, KHÔNG cắt âm thầm\n"
       "- Giá trị lưu DB khớp đúng với giá trị hiển thị",
       spec="Đã hỏi leader",
       note="MT-07: corpus tự mâu thuẫn — Leftbar r352「20 ký tự success」, r356「Nhập 20 ký tự → không nhập được ký tự 31」, "
            "r387「Nhập 31 ký tự → invalid」. Spec không ghi giới hạn nào"),

    tc("Profile người gửi — quản lý", "STATE-CLEAN-001", "Abnormal",
       "Nhập đủ thông tin profile rồi đóng bằng X hoặc 戻る — không lưu",
       BOT,
       "1. Mở modal thêm profile, nhập tên + upload ảnh PNG hợp lệ\n"
       "2. Click X → kiểm tra danh sách profile\n"
       "3. Lặp lại, lần này click 戻る → kiểm tra danh sách profile",
       "Tên + ảnh hợp lệ, thoát bằng X và bằng 戻る",
       "- Cả 2 cách thoát: profile KHÔNG được tạo\n- Mở lại modal thêm: các trường đã reset trống",
       note="Nguồn: Leftbar+Header r359, r360"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Normal",
       "Thêm profile thành công và chọn làm người gửi — tin cũ giữ profile cũ",
       BOT + "\n- Friend A đã có vài tin nhắn gửi bằng profile 初期設定",
       "1. Thêm profile P_new (tên + ảnh PNG), bấm 保存\n2. Kiểm tra DB bots_profiles có bản ghi mới\n"
       "3. Chọn P_new làm người gửi, gửi 1 tin cho A\n"
       "4. Quan sát tin CŨ và tin MỚI ở chat 1:1 và trên app LINE",
       "Profile P_new",
       "- DB: bots_profiles có bản ghi mới với nick_name và avt_path đúng, is_default = 0\n"
       "- Tin MỚI hiển thị profile P_new ở cả chat 1:1 và app LINE\n"
       "- Tin CŨ vẫn hiển thị profile cũ, KHÔNG bị đổi theo",
       note="Nguồn: Leftbar+Header r361, r363"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Normal",
       "Sửa profile — cập nhật ảnh và tên, phản ánh ở mọi màn liên quan",
       BOT + "\n- Profile P1 đang được chọn làm người gửi, đã có ảnh",
       "1. Mở modal sửa profile P1, đổi tên và thay ảnh mới → 保存\n"
       "2. Kiểm tra hiển thị ở: modal chọn profile, màn Broadcast (送信者), chat 1:1, app LINE của friend\n"
       "3. Gửi 1 tin mới rồi kiểm tra lại app LINE",
       "P1: đổi tên và đổi ảnh",
       "- Cả 4 nơi (modal chọn profile / màn Broadcast / chat 1:1 / app LINE) đều hiển thị thông tin MỚI\n"
       "- Tin nhắn gửi sau khi sửa mang tên + ảnh mới",
       note="Đi tới output cuối (RULE-06). Nguồn: Leftbar+Header r393, r394, r397-r400 + Profile sender r30, r54"),

    tc("Profile người gửi — quản lý", "STATE-CLEAN-001", "Abnormal",
       "Sửa profile rồi thoát bằng X / 戻る — thông tin cũ được giữ",
       BOT + "\n- Profile P1 có tên và ảnh cũ",
       "1. Mở sửa P1, đổi tên + thay ảnh mới\n2. Click X → kiểm tra P1 ở modal chọn profile và màn Broadcast\n"
       "3. Lặp lại, lần này click 戻る → kiểm tra tương tự",
       "Đổi cả tên và ảnh, thoát bằng X và bằng 戻る",
       "- Cả 2 cách thoát: P1 giữ nguyên tên và ảnh CŨ ở mọi màn\n- Không lưu thay đổi",
       note="Nguồn: Leftbar+Header r373, r374, r391, r392, r395, r396, r401, r402"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Normal",
       "Sửa ảnh profile — xoá ảnh cũ không thay ảnh mới thì về ảnh mặc định",
       BOT + "\n- Profile P1 đang có ảnh",
       "1. Mở sửa P1, xoá ảnh hiện có, KHÔNG chọn ảnh mới\n2. Click 保存\n"
       "3. Quan sát avatar của P1 ở modal chọn profile\n4. Gửi 1 tin bằng P1, kiểm tra app LINE",
       "Xoá ảnh, không thay ảnh mới",
       "- P1 hiển thị ảnh mặc định của hệ thống\n- Tin nhắn gửi bằng P1 hiển thị ảnh mặc định ở cả chat 1:1 và app LINE",
       note="Nguồn: Leftbar+Header r376"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Abnormal",
       "Profile mặc định 初期設定 — không có chức năng sửa và xoá",
       BOT,
       "1. Mở modal 送信者名を変更\n2. Quan sát dòng profile 初期設定\n3. Thử tìm nút sửa / xoá của dòng này",
       "Profile mặc định của bot",
       "- Dòng 初期設定 KHÔNG có nút sửa và KHÔNG có nút xoá\n- Chỉ chọn được làm người gửi",
       note="Nguồn: Leftbar+Header r336, r366"),

    tc("Profile người gửi — quản lý", "FUNC-001", "Normal",
       "Xoá profile — có xác nhận, xoá xong biến mất khỏi danh sách",
       BOT + "\n- Profile P2 tồn tại, KHÔNG phải profile đang chọn",
       "1. Bấm xoá P2\n2. Quan sát nội dung alert xác nhận\n3. Bấm Hủy → kiểm tra P2 còn không\n"
       "4. Bấm xoá lại → bấm OK → kiểm tra danh sách và DB bots_profiles",
       "Profile P2",
       "- Alert hiện đúng nội dung「送信ユーザー名「〇〇」を削除しますがよろしいですか？」\n"
       "- Bấm Hủy: P2 vẫn còn\n- Bấm OK: P2 biến mất khỏi modal và khỏi bảng bots_profiles",
       note="Nguồn: Leftbar+Header r337, r338"),

    tc("Profile người gửi — quản lý", "STATE-DEP-001", "Abnormal",
       "Xoá profile ĐANG được chọn — hệ thống tự quay về profile mặc định",
       BOT + "\n- Profile P1 đang được chọn làm người gửi",
       "1. Xoá P1 (bấm OK ở alert)\n2. KHÔNG chọn profile mới, đóng modal bằng X\n"
       "3. Quan sát 送信ユーザー名 ở màn chat\n4. Gửi 1 tin nhắn, kiểm tra profile hiển thị",
       "Xoá chính profile đang dùng",
       "- Hệ thống tự chọn về profile 初期設定\n- Tin nhắn gửi sau đó mang profile mặc định của bot",
       note="Nguồn: Leftbar+Header r339"),

    tc("Profile người gửi — quản lý", "DATA-REF-001", "Abnormal",
       "Xoá profile — ảnh hưởng tới Broadcast và tới tin nhắn cũ đã gửi bằng profile đó",
       BOT + "\n- Profile P1 đang được chọn ở 1 bản ghi Broadcast\n"
       "- Friend A có tin nhắn cũ đã gửi bằng P1",
       "1. Ghi lại profile hiển thị của tin cũ ở chat 1:1 của A\n2. Xoá profile P1\n"
       "3. Mở bản ghi Broadcast, kiểm tra profile đang chọn\n"
       "4. Mở lại chat 1:1 của A, kiểm tra hiển thị của tin nhắn cũ",
       "P1 dùng ở Broadcast + đã gửi tin cho A",
       "- Broadcast: profile tự chuyển về mặc định\n"
       "- Ghi nhận hiển thị thực tế của tin nhắn CŨ ở chat 1:1 (còn tên P1 hay chuyển về tên bot) và đối chiếu quyết định Leader",
       spec="Đã hỏi leader",
       note="TC gốc để câu hỏi mở 「Text hiển thị trên màn chat 1:1 sẽ như nào」 → chưa ai chốt. "
            "Nguồn: Leftbar+Header r340, r341"),

    tc("Profile người gửi — quản lý", "SYNC-APP-001", "Normal",
       "Nút reload profile — lấy thông tin mới nhất khi bot thay đổi tên/ảnh",
       BOT + "\n- Bot A vừa được đổi tên và ảnh ở màn cài đặt bot",
       "1. Mở modal 送信者名を変更, quan sát dòng 初期設定\n2. Click icon reload\n"
       "3. Quan sát lại tên và ảnh của 初期設定\n"
       "4. Không thay đổi gì ở bot → click reload lần nữa\n5. Double click icon reload",
       "Bot vừa đổi tên + ảnh",
       "- Sau reload lần 1: 初期設定 hiển thị tên và ảnh MỚI của bot\n"
       "- Reload khi bot không đổi gì: không hiện tượng bất thường\n"
       "- Double click reload: chỉ gửi 1 request, không lỗi",
       note="Gộp 3 nhánh vì cùng thuộc 1 chuỗi thao tác reload. Nguồn: Leftbar+Header r333-r335"),

    # ═══════════════ Profile người gửi — áp dụng khi gửi ═══════════════
    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi bằng profile GỐC của bot ở chat 1:1 (web) — mọi loại tin đều mang profile bot",
       BOT + "\n- Đang chọn profile 初期設定 (profile gốc của bot)\n- Friend A là bạn bè của bot",
       "1. Với từng loại nội dung ở cột Dữ liệu test: gửi cho friend A từ chat 1:1 trên web\n"
       "2. Sau mỗi lần gửi: kiểm tra avatar + tên người gửi ở chat 1:1\n"
       "3. Kiểm tra avatar + tên hiển thị trên app LINE của friend A",
       "Text nhập trực tiếp · media · PDF · template text · template button standard / color / image / quick · "
       "template gửi từ modal multi action · template 紹介 (cũ)",
       "- TẤT CẢ: chat 1:1 hiển thị ảnh và tên của bot gốc\n"
       "- TẤT CẢ: app LINE phía friend cũng hiển thị ảnh và tên của bot gốc",
       note="Gộp 10 điểm vì CÙNG kết quả. Đi tới output cuối app LINE (RULE-06). "
            "Nguồn: Profile sender r4-r14 (Bug KH #33072 12/2025)"),

    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi bằng profile SENDER khác ở chat 1:1 (web) — mọi loại tin đều mang profile đã chọn",
       BOT + "\n- Đã chọn profile P1 (tên「営業 山田」+ ảnh riêng) làm người gửi\n- Friend A là bạn bè của bot",
       "1. Với từng loại nội dung ở cột Dữ liệu test: gửi cho friend A từ chat 1:1 web\n"
       "2. Kiểm tra avatar + tên người gửi ở chat 1:1\n3. Kiểm tra avatar + tên trên app LINE của friend A",
       "Text nhập trực tiếp · media · PDF · template text / sticker / location / media / 紹介 · "
       "template button standard 1 panel / standard nhiều panel / color / image / quick · "
       "template và text gửi từ modal multi action",
       "- TẤT CẢ: chat 1:1 hiển thị ảnh và tên「営業 山田」của P1\n"
       "- TẤT CẢ: app LINE phía friend hiển thị ảnh và tên của P1, KHÔNG phải của bot gốc",
       note="Gộp 14 điểm vì CÙNG kết quả. Đây chính là bug KH #33072. Nguồn: Profile sender r15-r29"),

    tc("Profile người gửi — áp dụng khi gửi", "SYNC-APP-001", "Normal",
       "Gửi bằng profile sender trên APP MOBILE — profile áp dụng đúng ở cả 2 phía",
       "- Đăng nhập app mobile LME bằng account admin của bot A\n- Friend A là bạn bè của bot",
       "1. Ở app mobile, chọn profile 初期設定 → gửi text, media, template (button các loại), multi action\n"
       "2. Đổi sang profile P1 → gửi lại từng loại\n"
       "3. Với mỗi lần: kiểm tra hiển thị ở chat 1:1 (app + web) và trên app LINE của friend",
       "Profile 初期設定 và P1; các loại: text · media · template text/sticker/location/media/紹介 · "
       "button standard 1 panel / nhiều panel / color / image / quick · multi action",
       "- Gửi bằng 初期設定: cả chat 1:1 và app LINE đều hiện ảnh + tên bot gốc\n"
       "- Gửi bằng P1: cả chat 1:1 và app LINE đều hiện ảnh + tên của P1",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả; tách web/app vì là 2 client khác nhau (SYNC-APP). "
            "Nguồn: Profile sender r34-r55"),

    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Profile sender áp dụng đúng khi Send test từ màn Template",
       BOT + "\n- Có group template T gồm nhiều template con đủ loại\n- Friend A đã đăng ký là tài khoản test",
       "1. Chọn profile 初期設定 → send test cả group T và send test 1 template con → kiểm tra 2 phía\n"
       "2. Đổi sang profile P1 → lặp lại với đủ loại template con ở cột Dữ liệu test\n"
       "3. Lặp lại bằng nút quick test ở màn list template",
       "Loại template con: text · sticker · location · media · 紹介 · button standard 1 panel / nhiều panel / "
       "color / image / quick",
       "- Send test bằng 初期設定: chat 1:1 và app LINE đều hiện profile bot gốc\n"
       "- Send test bằng P1: chat 1:1 và app LINE đều hiện profile P1\n"
       "- Đúng với cả 2 đường: modal preview send test và nút quick test",
       note="Gộp vì cùng kết quả. Nguồn: Profile sender r56-r81"),

    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Profile sender áp dụng đúng khi Send test từ màn Broadcast",
       BOT + "\n- Có bản ghi Broadcast B với message thêm trực tiếp và message lấy từ template\n"
       "- Friend A đã đăng ký là tài khoản test",
       "1. Chọn profile 初期設定 → send test B (message trực tiếp và message từ template) → kiểm tra 2 phía\n"
       "2. Đổi sang profile P1 → lặp lại với các loại ở cột Dữ liệu test\n"
       "3. Lặp lại bằng nút quick test ở màn list Broadcast",
       "Message trực tiếp: button standard / color / image / quick · "
       "Message từ template: text · sticker · location · media · 紹介 · button các loại",
       "- Send test bằng 初期設定: chat 1:1 và app LINE hiện profile bot gốc\n"
       "- Send test bằng P1: chat 1:1 và app LINE hiện profile P1",
       note="Gộp vì cùng kết quả. Nguồn: Profile sender r82-r104"),

    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Đổi profile giữa chừng — tin gửi sau mang profile mới, tin trước giữ profile cũ",
       BOT + "\n- Đang dùng profile P1, đã gửi vài tin cho friend A",
       "1. Gửi tin M1 bằng P1\n2. Đổi sang profile P2\n3. Gửi tin M2\n"
       "4. Quan sát M1 và M2 ở chat 1:1 và trên app LINE của A",
       "P1 → P2, 2 tin nhắn liên tiếp",
       "- M1 giữ profile P1 (tên + ảnh cũ)\n- M2 mang profile P2\n"
       "- Hiển thị nhất quán ở cả chat 1:1 và app LINE",
       note="Nguồn: Profile sender r31, r55, r97"),

    tc("Profile người gửi — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi vào NHÓM LINE bằng profile gốc và bằng profile sender",
       BOT + "\n- Bot A đang ở trong nhóm LINE G1",
       "1. Chọn profile 初期設定, gửi 1 tin vào nhóm G1 → kiểm tra chat 1:1 và app LINE của thành viên nhóm\n"
       "2. Đổi sang profile P1, gửi 1 tin vào G1 → kiểm tra lại",
       "Nhóm G1, profile 初期設定 và P1",
       "- Tin gửi bằng 初期設定: hiện ảnh + tên bot gốc ở cả 2 phía\n"
       "- Tin gửi bằng P1: hiện ảnh + tên của P1 ở cả 2 phía",
       note="Nguồn: Profile sender r32, r33"),

    # ═══════════════ Header hội thoại ═══════════════
    tc("Header hội thoại", "UI-FIELD-001", "Normal",
       "Header hội thoại — avatar và tên bạn bè, tên dài không vỡ layout",
       BOT + "\n- Friend có avatar và friend không avatar\n- Friend tên ngắn và friend tên rất dài",
       "1. Mở lần lượt 4 friend (có/không avatar × tên ngắn/dài)\n2. Quan sát vùng header cột giữa",
       "4 friend với 4 tổ hợp avatar/tên",
       "- Friend có avatar hiện đúng ảnh, không avatar hiện ảnh mặc định\n"
       "- Tên dài được xử lý (cắt hoặc xuống dòng), không tràn ra ngoài header",
       note="Nguồn: Leftbar+Header r406-r409"),

    tc("Header hội thoại", "UI-002", "Normal",
       "Hover và click vào tên bạn bè ở header — tooltip và mở màn chi tiết",
       BOT + "\n- Đang mở hội thoại của friend A",
       "1. Hover chuột lên vùng tên friend ở header\n2. Quan sát con trỏ, màu sắc và tooltip\n"
       "3. Double click vào tên\n4. Quay lại, double click vào ảnh",
       "Friend A",
       "- Hover: con trỏ thành hình bàn tay, vùng đổi màu, hiện tooltip「友だち詳細ページを表示」\n"
       "- Double click tên: chuyển sang màn chi tiết bạn bè (my_page)\n"
       "- Double click ảnh: phóng to ảnh đại diện",
       note="Nguồn: Leftbar+Header r410-r413"),

    tc("Header hội thoại", "FUNC-001", "Normal",
       "Bookmark ở header — hover hiện tooltip, click bật/tắt, double click chỉ tính 1 lần",
       BOT + "\n- Friend A CHƯA bookmark",
       "1. Hover icon bookmark ở header, đọc tooltip\n2. Click 1 lần → kiểm tra trạng thái + is_bookmark\n"
       "3. Click lần nữa → kiểm tra\n4. Double click nhanh → kiểm tra Network và is_bookmark",
       "Friend A, bật/tắt bookmark",
       "- Hover: hiện tooltip「ブックマークする」\n"
       "- Click lần 1: chuyển sang đã bookmark (is_bookmark = 1), icon ở danh sách xuất hiện\n"
       "- Click lần 2: về chưa bookmark (is_bookmark = 0)\n"
       "- Double click: chỉ 1 request, trạng thái chỉ đổi 1 lần",
       note="Gộp vì là chuỗi thao tác liên tiếp trên cùng 1 nút. Nguồn: Leftbar+Header r414-r417"),

    tc("Header hội thoại", "REG-URL-001", "Normal",
       "Nút copy link chia sẻ ở header — copy đúng và có thông báo",
       BOT + "\n- Đang mở hội thoại của friend A",
       "1. Hover icon link ở header, đọc tooltip\n2. Double click vào icon link\n"
       "3. Quan sát thông báo\n4. Dán nội dung clipboard vào ô văn bản và mở link đó ở tab mới",
       "Friend A",
       "- Hover hiện tooltip「共有リンクをコピー」\n"
       "- Sau khi click: hiện thông báo「コピーしました」và tự đóng\n"
       "- Link dán ra mở đúng màn chat 1:1 của friend A",
       note="Nguồn: Leftbar+Header r418, r419"),

    tc("Header hội thoại", "UI-003", "Normal",
       "Dropdown 対応ステータス ở header — hiện đủ 5 status mặc định với bot/friend mới",
       BOT + "\n- Bot MỚI vừa tạo, friend MỚI vừa kết bạn, chưa chỉnh sửa status",
       "1. Mở hội thoại friend mới\n2. Hover icon bút cạnh trường status, đọc tooltip\n"
       "3. Click vào trường status, quan sát dropdown\n"
       "4. Kiểm tra DB: SELECT name_status, position FROM status_chat WHERE bot_id = <bot mới>",
       "Bot mới + friend mới",
       "- Hover icon bút: hiện tooltip「対応ステータスを編集」và icon đổi màu\n"
       "- Dropdown hiện đủ 5 status mặc định: 見込みあり / 対応中 / フォロー / トラブル / 対応完了\n"
       "- DB: bảng status_chat có đúng 5 bản ghi mặc định cho bot mới",
       note="Verify DB + màn hình. Nguồn: Leftbar+Header r420-r422"),

    tc("Header hội thoại", "UI-002", "Boundary",
       "Dropdown 対応ステータス khi có nhiều status — giới hạn chiều cao 400px và có scroll",
       BOT + "\n- Bot A đã tạo ≥20 対応ステータス",
       "1. Mở dropdown status ở header\n2. Đo chiều cao dropdown\n3. Thử cuộn bên trong dropdown",
       "20 status",
       "- Dropdown giãn chiều cao theo số status nhưng TỐI ĐA 400px\n"
       "- Khi vượt 400px thì có thanh cuộn, không bị cắt mất status",
       note="Nguồn: Leftbar+Header r424"),

    tc("Header hội thoại", "COMPAT-LEGACY-001", "Normal",
       "Dropdown 対応ステータス của bot cũ — hiện đúng danh sách status đã chỉnh sửa",
       BOT + "\n- Bot CŨ đã từng thêm/sửa/xoá status (khác bộ 5 mặc định)",
       "1. Mở hội thoại 1 friend của bot cũ\n2. Click trường status\n"
       "3. Đối chiếu dropdown với bảng status_chat của bot cũ",
       "Bot cũ có danh sách status đã chỉnh sửa",
       "- Dropdown hiện đúng danh sách status hiện có của bot cũ (không reset về 5 mặc định)\n"
       "- Thứ tự khớp cột position trong status_chat",
       note="Nguồn: Leftbar+Header r421, r423, r432"),

    tc("Header hội thoại", "FUNC-001", "Normal",
       "Chọn status ở dropdown header — badge cập nhật ở header và ở danh sách",
       BOT + "\n- Friend A chưa có status",
       "1. Mở dropdown status, hover từng status quan sát hiệu ứng\n2. Click chọn status「対応中」\n"
       "3. Quan sát badge ở header và ở dòng A trong danh sách\n"
       "4. Kiểm tra DB conversation.id_status của A",
       "Status 対応中",
       "- Badge「対応中」xuất hiện ở cả header và dòng A trong danh sách, đúng màu\n"
       "- DB: id_status trỏ tới status 対応中",
       note="Verify DB + 2 vị trí trên màn hình. Nguồn: Leftbar+Header r425, r426"),

    # ═══════════════ 対応ステータス — CRUD ═══════════════
    tc("対応ステータス — CRUD", "UI-001", "Normal",
       "Modal 対応ステータス編集 — mở đúng thiết kế, có scroll khi nhiều status",
       BOT + "\n- Bot A có ≥15 対応ステータス",
       "1. Click icon bút cạnh trường status ở header\n2. Quan sát modal (nền tối, căn giữa)\n"
       "3. Thử cuộn danh sách status\n4. Hover nút thêm status, đọc tooltip",
       "15 status",
       "- Modal căn giữa, nền phía sau tối, các thành phần đúng thiết kế\n"
       "- Danh sách dài có scroll\n- Hover nút thêm: hiện tooltip「対応ステータスを追加」",
       note="Nguồn: Leftbar+Header r427-r430"),

    tc("対応ステータス — CRUD", "FUNC-001", "Normal",
       "Thêm status mới — nhập hợp lệ thì lưu và hiện ở mọi nơi dùng status",
       BOT + "\n- Bot A có 5 status mặc định",
       "1. Mở modal 対応ステータス編集, bấm icon thêm\n"
       "2. Nhập lần lượt từng giá trị ở cột Dữ liệu test, click ra ngoài để lưu\n"
       "3. Sau mỗi lần: kiểm tra danh sách trong modal, dropdown ở header, modal 絞り込み, modal quick action\n"
       "4. Kiểm tra DB status_chat",
       "1 ký tự · 10 ký tự · tiếng Nhật · chữ hoa và chữ thường · có khoảng trắng đầu và cuối · "
       "chuỗi trùng tên với status đã có",
       "- Tất cả giá trị trên đều lưu thành công\n"
       "- Tên có khoảng trắng đầu/cuối: tự trim rồi lưu\n"
       "- Cho phép trùng tên với status đã có\n"
       "- Status mới hiện đủ ở: modal chỉnh sửa, dropdown header, modal 絞り込み, modal quick action; DB có bản ghi mới",
       note="Gộp 6 điểm vì cùng kết quả 「lưu thành công」. Nguồn: Leftbar+Header r455-r460, r462-r464"),

    tc("対応ステータス — CRUD", "UI-INPUT-001", "Abnormal",
       "Thêm status — bỏ trống tên thì báo lỗi",
       BOT,
       "1. Mở modal 対応ステータス編集, bấm icon thêm\n2. Không nhập gì, click ra ngoài\n3. Quan sát thông báo",
       "Tên status để trống",
       "- Hiện thông báo「ステータス必ず指定してください。」\n- Không tạo bản ghi mới trong status_chat",
       note="Nguồn: Leftbar+Header r443, r461"),

    tc("対応ステータス — CRUD", "UI-INPUT-001", "Boundary",
       "Tên status — giới hạn 10 ký tự",
       BOT,
       "1. Mở modal 対応ステータス編集\n2. Nhập lần lượt độ dài ở cột Dữ liệu test, lưu và ghi nhận kết quả\n"
       "3. Kiểm tra giá trị lưu trong status_chat.name_status",
       "9 ký tự · 10 ký tự · 11 ký tự · 11 ký tự tiếng Nhật",
       "- 9 và 10 ký tự: lưu thành công, DB lưu đủ\n"
       "- 11 ký tự (cả latinh và tiếng Nhật): hiện「ステータス名は10文字以下にしてください。」, không lưu\n"
       "- Đếm theo KÝ TỰ, không phải byte (11 ký tự tiếng Nhật vẫn báo lỗi)",
       note="Khớp spec BR-12 (feature-spec.md:474 — mb_strlen ≤ 10). Nguồn: Leftbar+Header r440, r441, r444"),

    tc("対応ステータス — CRUD", "FUNC-001", "Normal",
       "Sửa tên status — cập nhật ở mọi nơi hiển thị status",
       BOT + "\n- Friend A đang gắn status「対応中」",
       "1. Mở modal 対応ステータス編集, đổi tên「対応中」thành「対応中2026」\n2. Lưu\n"
       "3. Kiểm tra: badge của A ở danh sách và header, dropdown header, modal 絞り込み, modal quick action\n"
       "4. Kiểm tra DB status_chat.name_status",
       "Đổi tên 対応中 → 対応中2026",
       "- Tất cả 4 nơi hiển thị tên MỚI\n- DB cập nhật name_status\n"
       "- Friend A vẫn giữ nguyên liên kết status (id_status không đổi)",
       note="Nguồn: Leftbar+Header r445-r448"),

    tc("対応ステータス — CRUD", "FUNC-001", "Normal",
       "Đổi màu status — cập nhật màu badge ở mọi nơi, cho phép trùng màu với status khác",
       BOT + "\n- Friend A đang gắn status「対応中」màu X\n- Status「フォロー」đang màu Y",
       "1. Đổi màu「対応中」từ X sang Z → lưu → kiểm tra màu badge ở danh sách, header, dropdown, modal 絞り込み\n"
       "2. Đổi màu「対応中」sang đúng màu Y (trùng với フォロー) → lưu → kiểm tra",
       "Màu X → Z, sau đó Z → Y (trùng màu với status khác)",
       "- Đổi màu thành công, badge đổi màu đồng loạt ở mọi nơi\n"
       "- Cho phép 2 status trùng màu, không báo lỗi",
       note="Nguồn: Leftbar+Header r449-r454"),

    tc("対応ステータス — CRUD", "FUNC-001", "Normal",
       "Sắp xếp status bằng kéo thả — thứ tự mới áp dụng ở mọi nơi",
       BOT + "\n- Bot A có ≥5 status",
       "1. Mở modal 対応ステータス編集\n2. Kéo status ĐẦU tiên xuống dưới → lưu\n"
       "3. Kéo status CUỐI lên trên → lưu\n4. Kéo nhiều status liên tiếp → lưu\n"
       "5. Kiểm tra thứ tự ở: dropdown header, modal 絞り込み, modal quick action; DB status_chat.position",
       "≥5 status, 3 kiểu thao tác kéo thả",
       "- Mỗi lần kéo thả: có khung gợi ý vị trí trước khi thả\n"
       "- Thứ tự mới áp dụng đúng ở cả 3 nơi hiển thị và DB status_chat.position",
       note="Gộp 3 kiểu kéo vì cùng kết quả. Nguồn: Leftbar+Header r433-r439"),

    tc("対応ステータス — CRUD", "FUNC-001", "Normal",
       "Xoá status — có xác nhận, bạn bè đang dùng status đó về なし",
       BOT + "\n- Friend A và B đang gắn status「トラブル」",
       "1. Mở modal 対応ステータス編集, bấm xoá「トラブル」\n2. Quan sát alert xác nhận\n"
       "3. Bấm Hủy → kiểm tra status còn không\n4. Bấm xoá lại → OK\n"
       "5. Kiểm tra badge của A, B; dropdown header; modal 絞り込み; DB conversation.id_status của A và B",
       "Status「トラブル」đang được 2 friend sử dụng",
       "- Alert hiện「対応ステータス「〇〇」を削除しますがよろしいですか？」; bấm Hủy thì status còn nguyên\n"
       "- Bấm OK: status biến mất khỏi danh sách, dropdown và modal 絞り込み\n"
       "- Friend A và B không còn badge status; DB: id_status = NULL",
       note="Khớp spec BR-06 (feature-spec.md:468 — cascade reset id_status). "
            "Nguồn: Leftbar+Header r465-r471"),

    tc("対応ステータス — CRUD", "CONC-001", "Abnormal",
       "Double click icon thêm status — chỉ tạo 1 dòng nhập mới",
       BOT,
       "1. Mở modal 対応ステータス編集\n2. Double click nhanh icon thêm status\n3. Quan sát danh sách",
       "Double click trong < 300ms",
       "- Chỉ xuất hiện 1 dòng nhập mới, con trỏ focus vào dòng đó\n- Không tạo 2 dòng trống",
       note="Nguồn: Leftbar+Header r455"),

    tc("対応ステータス — CRUD", "DATA-001", "Abnormal",
       "Thêm nhiều status liên tiếp — màu của status trước không bị đổi theo",
       BOT + "\n- Bot A có sẵn danh sách status",
       "1. Bấm thêm status 1, nhập tên và đổi màu cho status 1 → lưu\n"
       "2. Bấm thêm status 2, nhập tên, click ra ngoài → lưu → kiểm tra màu status 1\n"
       "3. Đổi màu cho status 2 → kiểm tra màu status 1 và 2\n"
       "4. Bấm thêm status 3, nhập tên, click ra ngoài → lưu → kiểm tra màu status 1 và 2\n"
       "5. Đổi màu status 3 → kiểm tra màu cả 3\n"
       "6. Gán 3 status vừa tạo cho 3 friend, kiểm tra màu badge",
       "3 status thêm liên tiếp, mỗi cái 1 màu khác nhau",
       "- Sau mỗi bước: màu của các status TRƯỚC ĐÓ không bị thay đổi\n"
       "- Cả 3 status giữ đúng màu đã đặt ở modal, ở dropdown và ở badge của friend",
       note="Là 1 chuỗi thao tác liên tiếp không tách rời (FUNC-SEQ). "
            "Nguồn: file 01. TCsLine_Chat1:1 (cũ) → tab Test fix bug KH r3-r10"),
]
