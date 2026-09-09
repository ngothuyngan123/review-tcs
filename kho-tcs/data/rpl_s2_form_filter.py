# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 2: Phần 1 của form (アクション稼働対象絞り込み) + modal filter SC-003."""
from _common import tc

FORM = ("- Đăng nhập admin, bot A\n- Màn /basic/reply/new (form tạo quy tắc auto reply)\n"
        "- Quy tắc dùng 利用設定 =「全てのメッセージに反応」, action = gửi text「OK」")
FR = "\n- Có ≥2 friend LINE đã kết bạn với bot A để dựng các trạng thái đối chiếu"

S2 = [
    # ═══════════════ Form — lọc đối tượng 絞り込み ═══════════════
    tc("Form — lọc đối tượng 絞り込み", "UI-FIELD-001", "Normal",
       "Phần 1「アクション稼働対象絞り込み」: chọn radio 有効友だち ⇒ is_apply_active_friend = 1",
       FORM,
       "1. Ở Phần 1 chọn radio「有効友だち」\n2. Cấu hình action, click「登録」\n"
       "3. Query: SELECT is_apply_active_friend FROM auto_reply WHERE id=<rule>",
       "Radio「有効友だち」",
       "- Lưu thành công\n- DB: auto_reply.is_apply_active_friend = 1\n- Mở lại edit: radio「有効友だち」được chọn sẵn",
       note="Field #1 Traceability Matrix. Corpus TCs KHÔNG test trực tiếp field này ở tầng form (chỉ có ở Backup r7) "
            "⇒ TC lấp GAP do AI viết theo spec"),

    tc("Form — lọc đối tượng 絞り込み", "UI-FIELD-001", "Normal",
       "Phần 1: chọn radio ブロックした友だち ⇒ is_apply_active_friend = 0 (tập rule cho user bị block)",
       FORM,
       "1. Chọn radio「ブロックした友だち」\n2. Lưu\n"
       "3. Query: SELECT is_apply_active_friend FROM auto_reply WHERE id=<rule>\n4. Mở lại edit quan sát radio",
       "Radio「ブロックした友だち」",
       "- DB: auto_reply.is_apply_active_friend = 0\n- Mở lại edit: radio「ブロックした友だち」được chọn sẵn",
       note="BR-19: 2 tập rules riêng theo trạng thái conversation.isBlockedByBot(). Nguồn gián tiếp: Backup (job) r8. "
            "TC tầng form do AI viết"),

    tc("Form — lọc đối tượng 絞り込み", "DATA-COUNT-001", "Normal",
       "対象人数 (EP-15): số người hiển thị khớp số friend thỏa mãn điều kiện lọc, click mở đúng danh sách",
       FORM + FR + "\n- Bot A có 10 friend active, trong đó 3 friend gắn tag「VIP」",
       "1. Ở Phần 1 click「絞込み」, thêm điều kiện tag =「VIP」(bao gồm 1 trong các tag), lưu modal\n"
       "2. Đọc số ở「対象人数」\n3. Click vào số đó\n4. Đếm số friend trong danh sách mở ra",
       "10 friend active, 3 friend có tag「VIP」→ 対象人数 kỳ vọng = 3人",
       "-「対象人数」hiển thị「3人」\n- Click mở danh sách friend đúng 3 friend có tag VIP\n"
       "- Số hiển thị khớp với COUNT query line_user + bot_line_user theo filter",
       note="Field #2 (EP-15, tính realtime, không lưu DB). Nguồn: TCsLine_JOB / Test fix bug KH r39 "
            "'các màn khác / autoreply: Hiện đúng số người thỏa mãn filter, click thì mở friend list hiện list friend đúng'"),

    tc("Form — lọc đối tượng 絞り込み", "UI-FIELD-001", "Normal",
       "対象条件: sau khi lưu modal filter, ô 対象条件 hiển thị tóm tắt điều kiện đã thiết lập (text_preview)",
       FORM + "\n- Đã thiết lập 2 điều kiện AND: tag「VIP」+ ステップ購読状況",
       "1. Mở modal「絞込み」, thêm 2 điều kiện AND, click「保存」\n2. Quan sát ô「対象条件」trên form\n"
       "3. Query: SELECT text_preview FROM filters_v2 WHERE parent_type='auto_reply' AND parent_id=<rule>",
       "2 điều kiện AND: tag「VIP」+ scenario「新規歓迎」",
       "- Ô「対象条件」hiện chuỗi tóm tắt ghép từ text_preview của các filter item\n"
       "- Nội dung khớp với dữ liệu trong filters_v2",
       note="Field #3. Corpus TCs KHÔNG test 対象条件 ⇒ TC lấp GAP do AI viết theo spec"),

    tc("Form — lọc đối tượng 絞り込み", "DATA-REF-001", "Normal",
       "saveFilterV2 (EP-16): lưu filter ⇒ DELETE toàn bộ filters_v2 cũ + INSERT mới với parent_type='auto_reply'",
       FORM + "\n- Quy tắc đã có sẵn 3 điều kiện filter",
       "1. Query trước: SELECT id, type, operator FROM filters_v2 WHERE parent_type='auto_reply' AND parent_id=<rule>\n"
       "2. Mở modal filter, xóa 2 điều kiện, thêm 1 điều kiện khác, lưu\n3. Query lại đúng câu trên",
       "Trước: 3 điều kiện. Sau: 2 điều kiện (1 cũ giữ lại + 1 mới)",
       "- Toàn bộ id filters_v2 cũ biến mất (DELETE), sinh id mới\n- Còn đúng 2 bản ghi với parent_type='auto_reply'\n"
       "- Mở lại modal hiện đúng 2 điều kiện",
       note="Spec §SCR-RPL-03 luồng lưu filter + BR-13. Corpus KHÔNG test tầng DB của filter ⇒ TC lấp GAP do AI viết"),

    tc("Form — lọc đối tượng 絞り込み", "REG-SHARED-001", "Normal",
       "Modal「絞り込み」hiển thị đủ 11 loại điều kiện lọc theo spec",
       FORM,
       "1. Click「絞込み」mở modal\n2. Mở panel chọn loại điều kiện\n3. Liệt kê toàn bộ loại điều kiện hiển thị",
       "—",
       "- Modal có 2 khu vực:「全て満たす」(AND) và「どれか1つ以上満たす」(OR)\n"
       "- Panel liệt kê 11 loại: タグ / 友だち名 / 友だち追加日 / ステップ購読状況 / QRコードアクション / "
       "コンバージョン / 確認状況 / 友だち情報 / 対応ステータス / アフィリエイター / 新規・既存 友だち",
       spec="Spec không ghi",
       note="MT-05: spec ghi 11 loại nhưng「確認状況」có tin cậy THẤP (TB-04, có thể deprecated). Corpus TCs chỉ test "
            "5 loại (tag / scenario / conversion / QR / friend info). TC đối chiếu do AI viết, CẦN LEADER XÁC NHẬN "
            "danh sách loại điều kiện thật trên UI"),

    # ═══════════════ Filter — tag & ステップ ═══════════════
    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK1「選択したタグを1つ以上含む」: friend KHÔNG có tag nào trong list ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Có 3 tag: T1, T2, T3\n- Friend F0 không gắn tag nào",
       "1. Mở modal filter, thêm điều kiện tag ĐK1 với list [T1, T2, T3], lưu\n2. Lưu quy tắc\n"
       "3. Friend F0 gửi tin nhắn đến bot\n4. Quan sát LINE app của F0 và màn chat 1:1",
       "Friend F0: 0 tag. List tag điều kiện: T1, T2, T3",
       "- F0 KHÔNG nhận được action (không có tin nhắn trả về trên LINE app)\n"
       "- Màn chat 1:1 không hiện message auto reply cho F0",
       env="PRODUCTION",
       note="RULE-06 verify tới LINE app. Nguồn: Modal Filter / Sửa filter autoreply r4 (08/2023 — TC ~3 năm tuổi, "
            "CẦN VERIFY LẠI)"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK1: friend có 1 hoặc nhiều tag nằm trong list ⇒ CHẠY action",
       FORM + FR + "\n- Friend F1 gắn tag T1; friend F2 gắn T1+T2",
       "1. Thêm điều kiện tag ĐK1 với [T1, T2, T3], lưu\n2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "F1: {T1}; F2: {T1, T2}. List điều kiện: T1, T2, T3",
       "- Cả F1 và F2 đều nhận được action trên LINE app\n- Màn chat 1:1 hiện message auto reply với trigger 自動応答",
       env="PRODUCTION",
       note="2 friend cùng 1 kết quả nên giữ chung. Nguồn: Sửa filter autoreply r5 — TC ~3 năm tuổi, CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK2「選択したタグを全て含む」: friend không có tag nào trong list ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F0 không gắn tag nào",
       "1. Thêm điều kiện tag ĐK2 với [T1, T2], lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: 0 tag. List điều kiện: T1, T2 (phải có TẤT CẢ)",
       "- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r6 — CẦN VERIFY LẠI (08/2023)"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Boundary",
       "Filter tag ĐK2: friend có MỘT PHẦN tag trong list (không đủ hết) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F1 chỉ gắn tag T1",
       "1. Thêm điều kiện tag ĐK2 với [T1, T2], lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: {T1}. Điều kiện yêu cầu {T1, T2}",
       "- F1 KHÔNG nhận được action (thiếu T2)",
       env="PRODUCTION",
       note="Biên quan trọng của ĐK2 — phân biệt với ĐK1. Nguồn: Sửa filter autoreply r7 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK2: friend có ĐỦ TẤT CẢ tag được chọn ⇒ CHẠY action",
       FORM + FR + "\n- Friend F2 gắn cả T1 và T2",
       "1. Thêm điều kiện tag ĐK2 với [T1, T2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát LINE app",
       "F2: {T1, T2}. Điều kiện {T1, T2}",
       "- F2 nhận được action trên LINE app",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r8 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK3「選択したタグを1つ以上含む人を除く」: friend KHÔNG có tag nào trong list ⇒ CHẠY action",
       FORM + FR + "\n- Friend F0 không gắn tag nào",
       "1. Thêm điều kiện tag ĐK3 (loại trừ) với [T1, T2, T3], lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: 0 tag",
       "- F0 NHẬN được action (vì không nằm trong tập bị loại trừ)",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r9 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK3: friend có ≥1 tag trong list ⇒ KHÔNG chạy action (bị loại trừ)",
       FORM + FR + "\n- Friend F1 gắn T1",
       "1. Thêm điều kiện tag ĐK3 với [T1, T2, T3], lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: {T1}",
       "- F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r10 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK4「選択したタグを全て含む人を除く」: friend không có tag nào ⇒ CHẠY action",
       FORM + FR + "\n- Friend F0 không gắn tag nào",
       "1. Thêm điều kiện tag ĐK4 với [T1, T2], lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: 0 tag",
       "- F0 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r11 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Boundary",
       "Filter tag ĐK4: friend có MỘT PHẦN tag (không đủ hết) ⇒ VẪN CHẠY action",
       FORM + FR + "\n- Friend F1 chỉ gắn T1",
       "1. Thêm điều kiện tag ĐK4 với [T1, T2], lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: {T1}. Điều kiện loại trừ người có ĐỦ {T1, T2}",
       "- F1 NHẬN được action (chưa đủ tập tag nên không bị loại)",
       env="PRODUCTION",
       note="Biên phân biệt ĐK3 vs ĐK4. Nguồn: Sửa filter autoreply r12 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag ĐK4: friend có ĐỦ TẤT CẢ tag ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2 gắn cả T1 và T2",
       "1. Thêm điều kiện tag ĐK4 với [T1, T2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát LINE app",
       "F2: {T1, T2}",
       "- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r13 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter tag đặt ở khối OR「どれか1つ以上満たす」: chạy lại đủ 4 điều kiện tag ⇒ kết quả giống khối AND khi chỉ có 1 điều kiện",
       FORM + FR + "\n- Dựng đủ friend cho 4 điều kiện tag như các TC trên",
       "1. Với từng ĐK1→ĐK4: thêm điều kiện tag vào khối OR (thay vì AND), lưu\n"
       "2. Cho friend tương ứng gửi tin nhắn\n3. Quan sát LINE app",
       "4 điều kiện tag × các trạng thái friend đã dựng ở TC trên",
       "- Kết quả có/không action của cả 4 điều kiện GIỐNG khi đặt ở khối AND (vì chỉ có 1 điều kiện trong nhóm)\n"
       "- filters_v2.operator = 'or'",
       env="PRODUCTION",
       note="4 điều kiện cùng 1 kết luận nên giữ chung. Nguồn: Sửa filter autoreply r29-r32 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "INTG-HOOK-001", "Abnormal",
       "Bug ghi nhận trong corpus: đặt CÙNG LÚC filter tag và filter conversion ở khối OR ⇒ từng bị lỗi, phải verify lại",
       FORM + FR + "\n- Có tag T1 và conversion CV1",
       "1. Thêm vào khối OR: điều kiện tag T1 + điều kiện conversion CV1\n2. Lưu modal, lưu quy tắc\n"
       "3. Friend thỏa mãn CHỈ tag T1 gửi tin → quan sát\n4. Friend thỏa mãn CHỈ conversion CV1 gửi tin → quan sát",
       "Khối OR gồm 2 điều kiện khác loại: tag T1 + conversion CV1",
       "- Cả 2 friend đều nhận được action (thỏa mãn 1 trong 2 điều kiện OR)\n- Không lỗi khi lưu, không lỗi khi job chạy",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r29 — cột Test Result ghi 'case set cùng filter conversion bị lỗi "
            "(step logic cũ cũng bị)'. ĐÂY LÀ ĐIỂM ĐÃ TỪNG LỖI, TC ~3 năm tuổi, BẮT BUỘC VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK1「配信中」: friend chưa từng được start scenario ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Scenario S1 tồn tại\n- Friend F0 chưa có bản ghi scenario_lineuser",
       "1. Thêm điều kiện ステップ購読状況 ĐK1 (đang được start scenario S1), lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: chưa có bản ghi scenario_lineuser",
       "- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r14 — CẦN VERIFY LẠI (08/2023)"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK1: friend đang được start scenario (scenario_lineuser.is_following = 1) ⇒ CHẠY action",
       FORM + FR + "\n- Friend F1 có scenario_lineuser với is_following = 1 cho S1",
       "1. Thêm điều kiện ステップ ĐK1 cho S1, lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: scenario_lineuser(S1).is_following = 1",
       "- F1 nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r15 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Boundary",
       "Filter ステップ ĐK1: friend ĐÃ được add scenario nhưng đã bị stop (is_following = 0 hoặc 2) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2 có scenario_lineuser(S1).is_following = 0; friend F3 có is_following = 2",
       "1. Thêm điều kiện ステップ ĐK1 cho S1, lưu\n2. F2 gửi tin → quan sát\n3. F3 gửi tin → quan sát",
       "F2: is_following = 0 (đã stop); F3: is_following = 2 (đã gửi xong)",
       "- Cả F2 và F3 đều KHÔNG nhận được action",
       env="PRODUCTION",
       note="2 trạng thái cùng 1 kết quả nên giữ chung. Nguồn: Sửa filter autoreply r16 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK2「未登録」: friend chưa được start scenario ⇒ CHẠY action",
       FORM + FR + "\n- Friend F0 chưa có bản ghi scenario_lineuser",
       "1. Thêm điều kiện ステップ ĐK2 (không đăng ký) cho S1, lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: chưa có scenario_lineuser",
       "- F0 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r17 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK2: friend đang được start scenario (is_following = 1) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F1 có is_following = 1 cho S1",
       "1. Thêm điều kiện ステップ ĐK2 cho S1, lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: is_following = 1",
       "- F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r18 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Boundary",
       "Filter ステップ ĐK2: friend đã được add scenario nhưng đã stop (is_following = 0 / 2) ⇒ CHẠY action",
       FORM + FR + "\n- Friend F2: is_following = 0; friend F3: is_following = 2",
       "1. Thêm điều kiện ステップ ĐK2 cho S1, lưu\n2. F2 gửi tin → quan sát\n3. F3 gửi tin → quan sát",
       "F2: is_following = 0; F3: is_following = 2",
       "- Cả F2 và F3 đều NHẬN được action (ĐK2 gồm cả người chưa add và người đã stop)",
       env="PRODUCTION",
       note="Đây là điểm dễ nhầm nhất của ĐK2 — corpus ghi rõ 'bao gồm cả những user chưa được add scen và những "
            "user được add nhưng đã stop'. Nguồn: Sửa filter autoreply r19 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-DATE-001", "Normal",
       "Filter ステップ ĐK3: lọc theo mốc「user gửi message đến ngày xxx」⇒ chạy action đúng theo mốc ngày",
       FORM + FR + "\n- Friend F1 đang ở scenario S1, đã nhận tới step ngày thứ 3",
       "1. Thêm điều kiện ステップ ĐK3 với mốc ngày cụ thể, lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app\n"
       "4. Đổi mốc ngày sang giá trị KHÔNG khớp, lặp lại bước 2-3",
       "Mốc khớp: ngày thứ 3; mốc không khớp: ngày thứ 5",
       "- Mốc khớp: F1 nhận được action\n- Mốc không khớp: F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Corpus chỉ ghi 1 dòng 'Điều kiện 3: user gửi message đến ngày xxx' + Expect 'OK', KHÔNG có kết quả "
            "mong đợi chi tiết ⇒ AI tự viết kết quả đo lường được. Nguồn: Sửa filter autoreply r20 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK4「既読」(is_following = 2): friend đang start scenario (=1) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F1: is_following = 1",
       "1. Thêm điều kiện ステップ ĐK4 cho S1, lưu\n2. F1 gửi tin nhắn\n3. Quan sát",
       "F1: is_following = 1",
       "- F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r21 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK4: friend đã stop scenario (is_following = 0) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2: is_following = 0",
       "1. Thêm điều kiện ステップ ĐK4 cho S1, lưu\n2. F2 gửi tin nhắn\n3. Quan sát",
       "F2: is_following = 0",
       "- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r22 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK4: friend đã gửi xong scenario (is_following = 2) ⇒ CHẠY action",
       FORM + FR + "\n- Friend F3: is_following = 2",
       "1. Thêm điều kiện ステップ ĐK4 cho S1, lưu\n2. F3 gửi tin nhắn\n3. Quan sát",
       "F3: is_following = 2",
       "- F3 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r23 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Boundary",
       "Filter ステップ ĐK4: friend chưa từng được add scenario ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F0 chưa có bản ghi scenario_lineuser",
       "1. Thêm điều kiện ステップ ĐK4 cho S1, lưu\n2. F0 gửi tin nhắn\n3. Quan sát",
       "F0: chưa có bản ghi",
       "- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r24 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ ĐK5「未読」(phần bù của ĐK4): friend đang start (=1) hoặc đã stop (=0) hoặc chưa add ⇒ CHẠY action; "
       "friend đã gửi xong (=2) ⇒ KHÔNG chạy",
       FORM + FR + "\n- F1: is_following=1; F2: is_following=0; F0: chưa có bản ghi; F3: is_following=2",
       "1. Thêm điều kiện ステップ ĐK5 cho S1, lưu\n2. Lần lượt F1, F2, F0, F3 gửi tin nhắn\n3. Quan sát LINE app từng friend",
       "4 trạng thái: is_following = 1 / 0 / (chưa có) / 2",
       "- F1, F2, F0: NHẬN được action\n- F3 (is_following=2): KHÔNG nhận được action",
       env="PRODUCTION",
       note="Gộp 4 điểm ma trận vì cùng thể hiện 1 quy tắc phần bù; kết quả từng điểm ghi rõ ở cột Kết quả mong đợi. "
            "Nguồn: Sửa filter autoreply r25-r28 — CẦN VERIFY LẠI"),

    tc("Filter — tag & ステップ", "FUNC-MULTI-001", "Normal",
       "Filter ステップ đặt ở khối OR: chạy lại đủ 5 điều kiện ⇒ kết quả giống khối AND khi chỉ có 1 điều kiện",
       FORM + FR + "\n- Dựng đủ friend cho 5 điều kiện ステップ như các TC trên",
       "1. Với từng ĐK1→ĐK5: thêm điều kiện ステップ vào khối OR, lưu\n2. Cho friend tương ứng gửi tin nhắn\n3. Quan sát",
       "5 điều kiện ステップ × các trạng thái friend",
       "- Kết quả có/không action của cả 5 điều kiện GIỐNG khi đặt ở khối AND\n- filters_v2.operator = 'or'",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r33-r37 — CẦN VERIFY LẠI"),

    # ═══════════════ Filter — conversion & QRコード ═══════════════
    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter コンバージョン ĐK1「全て access」: friend chưa access conversion nào trong list ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Có 2 conversion CV1, CV2\n- Friend F0 chưa access conversion nào",
       "1. Thêm điều kiện conversion ĐK1 với [CV1, CV2], lưu\n2. F0 gửi tin nhắn\n3. Quan sát LINE app",
       "F0: 0 conversion",
       "- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r39 — cột ghi chú của corpus nêu 'Logic hiện tại đang check user access "
            "1 trong các conversion đã chọn ⇒ cần confirm lại' ⇒ MT-07, CẦN LEADER XÁC NHẬN ngữ nghĩa ĐK1"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Boundary",
       "Filter コンバージョン ĐK1: friend access MỘT PHẦN conversion (không đủ hết) ⇒ VẪN CHẠY action",
       FORM + FR + "\n- Friend F1 chỉ access CV1",
       "1. Thêm điều kiện conversion ĐK1 với [CV1, CV2], lưu\n2. F1 gửi tin nhắn\n3. Quan sát LINE app",
       "F1: access {CV1}; điều kiện [CV1, CV2]",
       "- F1 NHẬN được action",
       env="PRODUCTION",
       note="⚠️ Đây chính là điểm nghi vấn: nhãn ĐK1 là「全て」nhưng hành vi corpus ghi nhận là「1つ以上」. "
            "Nguồn: Sửa filter autoreply r40 — gắn MT-07, CẦN LEADER QUYẾT"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter コンバージョン ĐK1: friend đã access TẤT CẢ conversion được chọn ⇒ CHẠY action",
       FORM + FR + "\n- Friend F2 access cả CV1 và CV2",
       "1. Thêm điều kiện conversion ĐK1 với [CV1, CV2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát",
       "F2: access {CV1, CV2}",
       "- F2 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r41 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter コンバージョン ĐK2 (loại trừ): friend chưa access conversion nào ⇒ CHẠY action",
       FORM + FR + "\n- Friend F0 chưa access conversion nào",
       "1. Thêm điều kiện conversion ĐK2 (trừ người đã access tất cả) với [CV1, CV2], lưu\n2. F0 gửi tin\n3. Quan sát",
       "F0: 0 conversion",
       "- F0 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r42 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Boundary",
       "Filter コンバージョン ĐK2: friend access MỘT PHẦN conversion ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F1 chỉ access CV1",
       "1. Thêm điều kiện conversion ĐK2 với [CV1, CV2], lưu\n2. F1 gửi tin\n3. Quan sát",
       "F1: access {CV1}",
       "- F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r43 — cùng nghi vấn ngữ nghĩa như MT-07"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter コンバージョン ĐK2: friend đã access TẤT CẢ conversion ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2 access cả CV1 và CV2",
       "1. Thêm điều kiện conversion ĐK2 với [CV1, CV2], lưu\n2. F2 gửi tin\n3. Quan sát",
       "F2: access {CV1, CV2}",
       "- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r44 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter コンバージョン đặt ở khối OR ⇒ kết quả giống khối AND khi chỉ có 1 điều kiện",
       FORM + FR + "\n- Dựng friend như 2 điều kiện conversion ở trên",
       "1. Thêm điều kiện conversion vào khối OR, lưu\n2. Cho từng friend gửi tin\n3. Quan sát",
       "2 điều kiện conversion × 3 trạng thái friend",
       "- Kết quả giống khối AND\n- filters_v2.operator = 'or'",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r45 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコードアクション ĐK1: friend chưa kết bạn qua landing nào trong list (chưa có bản ghi detail_landing_click) "
       "⇒ KHÔNG chạy action",
       FORM + FR + "\n- Có 2 landing L1, L2\n- Friend F0 chưa quét QR / chưa có bản ghi detail_landing_click",
       "1. Thêm điều kiện QRコードアクション ĐK1 với [L1, L2], lưu\n2. F0 gửi tin nhắn\n3. Quan sát",
       "F0: không có bản ghi detail_landing_click",
       "- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r46 — CẦN VERIFY LẠI (08/2023)"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Boundary",
       "Filter QRコード ĐK1: friend CHỈ quét QR nhưng KHÔNG bấm kết bạn (detail_landing_click.action = 1) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F1 có bản ghi detail_landing_click với action = 1 (chỉ quét, không add friend)",
       "1. Thêm điều kiện QRコード ĐK1 với [L1, L2], lưu\n2. F1 gửi tin nhắn\n3. Quan sát\n"
       "4. Query detail_landing_click của F1 xác nhận action = 1",
       "F1: detail_landing_click.action = 1 (điều kiện yêu cầu action = 2 — kết bạn qua QR)",
       "- F1 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Biên quan trọng: phân biệt 'quét QR' (action=1) và 'kết bạn qua QR' (action=2). "
            "Nguồn: Sửa filter autoreply r47 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK1: friend kết bạn qua ≥1 landing trong list ⇒ CHẠY action",
       FORM + FR + "\n- Friend F2 kết bạn qua L1 (detail_landing_click.action = 2)",
       "1. Thêm điều kiện QRコード ĐK1 với [L1, L2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát",
       "F2: kết bạn qua L1",
       "- F2 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r48 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK2「全ての landing」: friend không kết bạn qua landing nào / chỉ quét không add ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F0 chưa có bản ghi; friend F1 có action = 1",
       "1. Thêm điều kiện QRコード ĐK2 với [L1, L2], lưu\n2. F0 gửi tin → quan sát\n3. F1 gửi tin → quan sát",
       "F0: không có bản ghi; F1: action = 1",
       "- Cả F0 và F1 đều KHÔNG nhận được action",
       env="PRODUCTION",
       note="2 trạng thái cùng kết quả nên giữ chung. Nguồn: Sửa filter autoreply r49-r50 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Boundary",
       "Filter QRコード ĐK2: friend kết bạn qua MỘT PHẦN landing (không đủ hết) ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2 chỉ kết bạn qua L1",
       "1. Thêm điều kiện QRコード ĐK2 với [L1, L2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát",
       "F2: kết bạn qua {L1}; điều kiện yêu cầu {L1, L2}",
       "- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r51 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK2: friend kết bạn qua TẤT CẢ landing được chọn ⇒ CHẠY action",
       FORM + FR + "\n- Friend F3 kết bạn qua cả L1 và L2",
       "1. Thêm điều kiện QRコード ĐK2 với [L1, L2], lưu\n2. F3 gửi tin nhắn\n3. Quan sát",
       "F3: kết bạn qua {L1, L2}",
       "- F3 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r52 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK3 (loại trừ ≥1 landing): friend chưa kết bạn qua landing nào / chỉ quét ⇒ CHẠY action",
       FORM + FR + "\n- Friend F0 chưa có bản ghi; friend F1 có action = 1",
       "1. Thêm điều kiện QRコード ĐK3 với [L1, L2], lưu\n2. F0 gửi tin → quan sát\n3. F1 gửi tin → quan sát",
       "F0: không có bản ghi; F1: action = 1",
       "- Cả F0 và F1 đều NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r53-r54 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK3: friend kết bạn qua ≥1 landing trong list ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F2 kết bạn qua L1",
       "1. Thêm điều kiện QRコード ĐK3 với [L1, L2], lưu\n2. F2 gửi tin nhắn\n3. Quan sát",
       "F2: kết bạn qua {L1}",
       "- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r55 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK4 (loại trừ ĐỦ landing): friend chưa kết bạn / chỉ quét / kết bạn một phần ⇒ CHẠY action",
       FORM + FR + "\n- F0 chưa có bản ghi; F1 action=1; F2 kết bạn qua {L1}",
       "1. Thêm điều kiện QRコード ĐK4 với [L1, L2], lưu\n2. Lần lượt F0, F1, F2 gửi tin nhắn\n3. Quan sát từng friend",
       "3 trạng thái: không bản ghi / action=1 / kết bạn 1 trong 2 landing",
       "- Cả 3 friend đều NHẬN được action",
       env="PRODUCTION",
       note="3 điểm cùng 1 kết quả nên giữ chung. Nguồn: Sửa filter autoreply r56-r58 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード ĐK4: friend kết bạn qua TẤT CẢ landing được chọn ⇒ KHÔNG chạy action",
       FORM + FR + "\n- Friend F3 kết bạn qua cả L1 và L2",
       "1. Thêm điều kiện QRコード ĐK4 với [L1, L2], lưu\n2. F3 gửi tin nhắn\n3. Quan sát",
       "F3: kết bạn qua {L1, L2}",
       "- F3 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r59 — CẦN VERIFY LẠI"),

    tc("Filter — conversion & QRコード", "FUNC-MULTI-001", "Normal",
       "Filter QRコード đặt ở khối OR ⇒ kết quả giống khối AND khi chỉ có 1 điều kiện",
       FORM + FR + "\n- Dựng friend như 4 điều kiện QR ở trên",
       "1. Thêm điều kiện QRコード vào khối OR, lưu\n2. Cho từng friend gửi tin\n3. Quan sát",
       "4 điều kiện QR × các trạng thái friend",
       "- Kết quả giống khối AND\n- filters_v2.operator = 'or'",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r60 — CẦN VERIFY LẠI"),

    # ═══════════════ Filter — 友だち情報 ═══════════════
    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type SELECT ĐK1「選択肢を全て含む」⇒ chạy action khi friend có đủ các lựa chọn đã chọn",
       FORM + FR + "\n- Có friend info type select「性別」với option 男/女\n- Friend F1 có giá trị khớp, F0 không có giá trị",
       "1. Thêm điều kiện 友だち情報 select ĐK1, lưu\n2. F1 gửi tin → quan sát\n3. F0 gửi tin → quan sát",
       "F1: có đủ option được chọn; F0: chưa có giá trị",
       "- F1 NHẬN được action\n- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r61 — corpus chỉ ghi Expect 'OK', AI viết kết quả đo lường được. "
            "CẦN VERIFY LẠI (08/2023)"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type SELECT ĐK2「選択肢を全て除く」⇒ loại trừ friend có đủ các lựa chọn đã chọn",
       FORM + FR + "\n- Friend F1 có đủ option được chọn; friend F0 không có giá trị",
       "1. Thêm điều kiện 友だち情報 select ĐK2, lưu\n2. F1 gửi tin → quan sát\n3. F0 gửi tin → quan sát",
       "F1: có đủ option; F0: chưa có giá trị",
       "- F1 KHÔNG nhận được action\n- F0 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r62 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type SELECT ĐK3「値がある」: friend CÓ giá trị ⇒ chạy action; friend KHÔNG có giá trị ⇒ không chạy",
       FORM + FR + "\n- Friend F1 có giá trị friend info select; friend F0 chưa có",
       "1. Thêm điều kiện 友だち情報 select ĐK3 (có value), lưu\n2. F1 gửi tin → quan sát\n3. F0 gửi tin → quan sát",
       "F1: có value; F0: không có value",
       "- F1 NHẬN được action\n- F0 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Gộp 2 nhánh của cùng 1 điều kiện, kết quả từng nhánh ghi rõ. Nguồn: Sửa filter autoreply r63-r64 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type SELECT ĐK4「値がない」: friend CÓ giá trị ⇒ không chạy; friend KHÔNG có giá trị ⇒ chạy action",
       FORM + FR + "\n- Friend F1 có giá trị; friend F0 chưa có",
       "1. Thêm điều kiện 友だち情報 select ĐK4 (không có value), lưu\n2. F1 gửi tin → quan sát\n3. F0 gửi tin → quan sát",
       "F1: có value; F0: không có value",
       "- F1 KHÔNG nhận được action\n- F0 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r65-r66 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type TEXT 完全一致: chỉ friend có value TRÙNG KHỚP HOÀN TOÀN mới chạy action",
       FORM + FR + "\n- Friend info type text「会員番号」\n- F1 value =「A123」; F2 value =「A123456」; F0 chưa có value",
       "1. Thêm điều kiện 友だち情報 text, chế độ 完全一致, giá trị「A123」, lưu\n"
       "2. Lần lượt F1, F2, F0 gửi tin nhắn\n3. Quan sát LINE app từng friend",
       "Setting text =「A123」(toàn phần)",
       "- F1 (value đúng「A123」): NHẬN được action\n- F2 (value「A123456」): KHÔNG nhận\n- F0 (không có value): KHÔNG nhận",
       env="PRODUCTION",
       note="Gộp 3 điểm ma trận vì cùng 1 chế độ so khớp, kết quả từng điểm ghi rõ. "
            "Nguồn: Sửa filter autoreply r67-r69 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type TEXT 部分一致: friend có value CHỨA chuỗi setting mới chạy action",
       FORM + FR + "\n- F1 value =「A123456」; F2 value =「B999」; F0 chưa có value",
       "1. Thêm điều kiện 友だち情報 text, chế độ 部分一致, giá trị「A123」, lưu\n"
       "2. Lần lượt F1, F2, F0 gửi tin nhắn\n3. Quan sát",
       "Setting text =「A123」(1 phần)",
       "- F1 (value chứa「A123」): NHẬN được action\n- F2 (không chứa): KHÔNG nhận\n- F0 (không có value): KHÔNG nhận",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r70-r72 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type TEXT — điều kiện LOẠI TRỪ 完全一致 ⇒ friend khớp hoàn toàn bị loại, còn lại chạy action",
       FORM + FR + "\n- F1 value =「A123」; F2 value =「A123456」",
       "1. Thêm điều kiện 友だち情報 text loại trừ, chế độ 完全一致, giá trị「A123」, lưu\n"
       "2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "Loại trừ friend có value =「A123」",
       "- F1 KHÔNG nhận được action\n- F2 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r73 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type TEXT — điều kiện LOẠI TRỪ 部分一致 ⇒ friend có value chứa chuỗi bị loại",
       FORM + FR + "\n- F1 value =「A123456」; F2 value =「B999」",
       "1. Thêm điều kiện 友だち情報 text loại trừ, chế độ 部分一致, giá trị「A123」, lưu\n"
       "2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "Loại trừ friend có value CHỨA「A123」",
       "- F1 KHÔNG nhận được action\n- F2 NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r74 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 type TEXT — điều kiện「có friend_info_value」/「không có friend_info_value」",
       FORM + FR + "\n- F1 có bản ghi friend_info_value; F0 không có",
       "1. Thêm điều kiện「có value」, lưu → F1 và F0 lần lượt gửi tin, quan sát\n"
       "2. Đổi sang điều kiện「không có value」, lưu → F1 và F0 lần lượt gửi tin, quan sát",
       "F1: có friend_info_value; F0: không có",
       "- Điều kiện「có value」: F1 NHẬN action, F0 KHÔNG nhận\n"
       "- Điều kiện「không có value」: F1 KHÔNG nhận, F0 NHẬN action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r75-r76 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-DATE-001", "Normal",
       "Filter 友だち情報 type DATE — lọc theo MỐC thời gian, chỉ nhập ngày/tháng (không năm)",
       FORM + FR + "\n- Friend info type date「誕生日」\n- F1 có giá trị 03/15; F2 có giá trị 07/20",
       "1. Thêm điều kiện 友だち情報 date, chế độ mốc thời gian, nhập ngày/tháng = 03/15, lưu\n"
       "2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "Mốc: ngày 15 tháng 3 (không chỉ định năm)",
       "- F1 (khớp mốc ngày/tháng): NHẬN được action\n- F2: KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r77 — corpus Expect 'OK', AI viết kết quả đo lường được. CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-DATE-001", "Normal",
       "Filter 友だち情報 type DATE — lọc theo MỐC thời gian, nhập đủ ngày/tháng/năm",
       FORM + FR + "\n- F1 có giá trị 2025/03/15; F2 có giá trị 2026/03/15",
       "1. Thêm điều kiện date, chế độ mốc, nhập 2025/03/15, lưu\n2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "Mốc: 2025/03/15 (đủ năm)",
       "- F1 (đúng cả năm): NHẬN được action\n- F2 (khác năm, cùng ngày/tháng): KHÔNG nhận được action",
       env="PRODUCTION",
       note="Cặp TC phân biệt có/không có năm — cùng ngày/tháng nhưng khác năm cho kết quả khác nhau. "
            "Nguồn: Sửa filter autoreply r78 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-DATE-001", "Normal",
       "Filter 友だち情報 type DATE — lọc theo KHOẢNG thời gian, chỉ nhập ngày/tháng",
       FORM + FR + "\n- F1 giá trị 03/15 (trong khoảng); F2 giá trị 09/01 (ngoài khoảng)",
       "1. Thêm điều kiện date, chế độ khoảng thời gian, từ 03/01 đến 03/31, lưu\n"
       "2. F1 gửi tin → quan sát\n3. F2 gửi tin → quan sát",
       "Khoảng: 03/01 ~ 03/31 (không chỉ định năm)",
       "- F1 NHẬN được action\n- F2 KHÔNG nhận được action",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r79 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-DATE-001", "Boundary",
       "Filter 友だち情報 type DATE — khoảng thời gian đủ ngày/tháng/năm, kiểm tra 2 đầu biên",
       FORM + FR + "\n- F1 = 2025/03/01 (biên đầu); F2 = 2025/03/31 (biên cuối); F3 = 2025/04/01 (ngoài)",
       "1. Thêm điều kiện date, khoảng 2025/03/01 ~ 2025/03/31, lưu\n"
       "2. Lần lượt F1, F2, F3 gửi tin nhắn\n3. Quan sát từng friend",
       "Khoảng 2025/03/01 ~ 2025/03/31",
       "- F1 (đúng biên đầu): NHẬN action\n- F2 (đúng biên cuối): NHẬN action\n- F3 (ngoài 1 ngày): KHÔNG nhận",
       env="PRODUCTION",
       note="Corpus r80 chỉ ghi 'nhập ngày/tháng/năm' + Expect 'OK' — AI bổ sung 2 đầu biên theo RULE-01. CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Boundary",
       "Filter 友だち情報 type POINT — ma trận 5 toán tử so sánh (=, >=, >, <=, <) với cùng mốc điểm",
       FORM + FR + "\n- Friend info type point「ポイント」\n- F_eq = 100 điểm; F_gt = 150 điểm; F_lt = 50 điểm",
       "1. Với từng toán tử =, >=, >, <=, < và mốc setting = 100:\n"
       "   a. Thêm điều kiện 友だち情報 point, lưu\n   b. Lần lượt F_eq / F_gt / F_lt gửi tin nhắn\n"
       "   c. Quan sát LINE app từng friend",
       "Mốc setting = 100. Friend: 100 / 150 / 50 điểm",
       "- Toán tử「=」: chỉ F_eq nhận action\n- Toán tử「>=」: F_eq và F_gt nhận\n- Toán tử「>」: chỉ F_gt nhận\n"
       "- Toán tử「<=」: F_eq và F_lt nhận\n- Toán tử「<」: chỉ F_lt nhận",
       env="PRODUCTION",
       note="Ma trận 5 toán tử × 3 mốc điểm, kết quả từng ô ghi rõ trong Kết quả mong đợi nên giữ chung 1 TC. "
            "Nguồn: Sửa filter autoreply r81-r85 — CẦN VERIFY LẠI (08/2023)"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Filter 友だち情報 (4 type: select / text / date / point) đặt ở khối OR ⇒ kết quả giống khối AND khi chỉ có 1 điều kiện",
       FORM + FR + "\n- Dựng friend cho cả 4 type như các TC trên",
       "1. Với từng type select / text / date / point: thêm điều kiện vào khối OR, lưu\n"
       "2. Cho friend tương ứng gửi tin nhắn\n3. Quan sát",
       "4 type friend info × các trạng thái friend đã dựng",
       "- Kết quả có/không action giống khi đặt ở khối AND\n- filters_v2.operator = 'or'",
       env="PRODUCTION",
       note="Nguồn: Sửa filter autoreply r86-r89 — CẦN VERIFY LẠI"),

    tc("Filter — 友だち情報", "FUNC-MULTI-001", "Normal",
       "Kết hợp AND + OR: quy tắc có cả khối 全て満たす và khối どれか1つ以上満たす ⇒ chỉ friend thỏa cả 2 khối mới chạy action",
       FORM + FR + "\n- Khối AND: tag「VIP」; khối OR: friend info point >= 100 hoặc scenario S1 đang chạy\n"
       "- F1: VIP + 150 điểm; F2: VIP + 50 điểm + không ở S1; F3: không VIP + 150 điểm",
       "1. Thêm điều kiện vào cả 2 khối, lưu modal, lưu quy tắc\n2. Lần lượt F1, F2, F3 gửi tin nhắn\n3. Quan sát",
       "F1 thỏa AND + OR; F2 thỏa AND, không thỏa OR; F3 không thỏa AND",
       "- F1 NHẬN được action\n- F2 KHÔNG nhận\n- F3 KHÔNG nhận",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Corpus KHÔNG có TC kết hợp AND + OR cho auto reply ⇒ TC lấp GAP do AI viết theo spec §SCR-RPL-03. "
            "CẦN LEADER XÁC NHẬN ngữ nghĩa kết hợp giữa 2 khối"),
]
