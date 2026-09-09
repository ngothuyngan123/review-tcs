# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 6: Backup / đổi bot / phân quyền / môi trường."""
from _common import tc

BK = ("- Bot A (bot gốc) đã cấu hình đầy đủ auto reply: folder, quy tắc keyword, quy tắc all message, "
      "lịch trình, action, filter\n- Đã chạy job backup sang bot mới B")

S6 = [
    # ═══════════════ Backup & đổi bot ═══════════════
    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): FOLDER auto reply của bot gốc được backup sang bot mới",
       BK,
       "1. Chạy job backup bot A → bot B\n2. Mở /basic/reply của bot B\n"
       "3. So sánh danh sách folder ở sidebar với bot A\n"
       "4. Query: SELECT name, position FROM category WHERE bot_id=B AND kind=1 AND is_deleted=0",
       "Bot A có ≥2 folder auto reply",
       "- Bot B có đủ folder auto reply với tên giống bot A\n- DB: category kind=1 của bot B khớp số lượng và tên",
       env="PRODUCTION",
       note="RULE-08: job backup bắt buộc PRODUCTION. Nguồn: TCsLine_BackUp / Backup (job) r2 + Backup 1.0 r3. "
            "⚠️ Backup 1.0 r3 có 2 lần kết quả NG ⇒ điểm ĐÃ TỪNG LỖI"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc dạng KEYWORD (keyword_reaction_type=1) được backup đủ keyword",
       BK + "\n- Bot A có quy tắc dạng keyword với ≥2 keyword",
       "1. Chạy backup\n2. Mở màn /basic/reply của bot B, mở quy tắc tương ứng\n"
       "3. Query: SELECT a.keyword_reaction_type, k.keyword FROM auto_reply a LEFT JOIN keyword k "
       "ON k.auto_reply_id=a.id WHERE a.bot_id=B",
       "Quy tắc keyword với keyword_reaction_type = 1",
       "- Bot B: auto_reply.keyword_reaction_type = 1\n- Bảng keyword của bot B có đủ các keyword như bot A",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r3 + Backup 1.0 r4"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc dạng ALL MESSAGE (keyword_reaction_type=0) được backup, không sinh keyword thừa",
       BK + "\n- Bot A có quy tắc dạng 全てのメッセージ",
       "1. Chạy backup\n2. Mở quy tắc tương ứng ở bot B\n"
       "3. Query keyword_reaction_type + bảng keyword của quy tắc đó ở bot B",
       "Quy tắc 全てのメッセージ",
       "- Bot B: keyword_reaction_type = 0\n- Bảng keyword: 0 bản ghi cho quy tắc này",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r4. ⚠️ Backup 1.0 r5 ghi 'Không có' ở nhiều đợt ⇒ nhánh này ít được test lại"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc 常に反応 (time action = luôn) ⇒ bot B có start_time = end_time = day_of_week = NULL",
       BK + "\n- Bot A có quy tắc với 反応設定 =「常に（24時間/365日）反応する」",
       "1. Chạy backup\n2. Query: SELECT time_reaction_type, start_time, end_time, day_of_week FROM auto_reply "
       "WHERE bot_id=B\n3. Mở màn list bot B xem cột「スケジュール」",
       "反応設定 = 常に",
       "- Bot B: time_reaction_type = 0, start_time = NULL, end_time = NULL, day_of_week = NULL\n"
       "- Màn list bot B cột「スケジュール」hiện「常に」",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r5 + Backup 1.0 r6"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc CÓ set ngày/giờ ⇒ bot B giữ nguyên day_of_week / start_time / end_time",
       BK + "\n- Bot A có quy tắc lịch trình 月〜金 09:00~18:00",
       "1. Chạy backup\n2. Query day_of_week / start_time / end_time của quy tắc ở bot B\n"
       "3. Mở màn list bot B xem cột「スケジュール」",
       "曜日 = 月〜金 (「1;2;3;4;5」); 時間帯 09:00~18:00",
       "- Bot B: day_of_week =「1;2;3;4;5」, start_time = 09:00, end_time = 18:00\n"
       "- Màn list hiện「月,火,水,木,金 09:00~18:00」",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r6. ⚠️ Backup 1.0 r7 ghi 'Không có' ở nhiều đợt ⇒ ít được test lại"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc cho 有効友だち (is_apply_active_friend=1) được backup đúng",
       BK + "\n- Bot A có quy tắc với 対象 =「有効友だち」",
       "1. Chạy backup\n2. Query: SELECT is_apply_active_friend FROM auto_reply WHERE bot_id=B\n"
       "3. Mở form edit quy tắc ở bot B xem radio Phần 1",
       "対象 =「有効友だち」",
       "- Bot B: is_apply_active_friend = 1\n- Form edit hiện radio「有効友だち」được chọn",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r7 + Backup 1.0 r8"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): quy tắc cho ブロックした友だち (is_apply_active_friend=0) được backup đúng",
       BK + "\n- Bot A có quy tắc với 対象 =「ブロックした友だち」",
       "1. Chạy backup\n2. Query is_apply_active_friend của quy tắc đó ở bot B\n3. Mở form edit ở bot B",
       "対象 =「ブロックした友だち」",
       "- Bot B: is_apply_active_friend = 0\n- Form edit hiện radio「ブロックした友だち」được chọn",
       env="PRODUCTION",
       note="⚠️ Backup 1.0 r9 ghi kết quả NG ở đợt đầu ⇒ điểm ĐÃ TỪNG LỖI, phải verify kỹ. "
            "Nguồn: Backup (job) r8 + Backup 1.0 r9"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): setting số lần chạy action (1 lần / nhiều lần) được backup đúng",
       BK + "\n- Bot A có 1 quy tắc「1度のみアクション稼働」và 1 quy tắc「何度でもアクション稼働」",
       "1. Chạy backup\n2. Query: SELECT id, response_number FROM auto_reply WHERE bot_id=B\n"
       "3. Mở form edit từng quy tắc ở bot B xem radio Phần 5",
       "2 quy tắc: response_number = 0 và = 1",
       "- Bot B giữ đúng response_number của từng quy tắc\n- Form edit hiện đúng radio tương ứng",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r9 + Backup 1.0 r10"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): action TEXT / BOOKMARK / FRIEND INFO / STATUS CHAT / BLOCK-ẨN của auto reply được backup",
       BK + "\n- Bot A có quy tắc với 5 loại action: text, bookmark, friend info, status chat, block/ẩn friend",
       "1. Chạy backup\n2. Mở modal action của quy tắc ở bot B\n"
       "3. Query t_actions_detail của quy tắc ở bot B\n4. Friend của bot B trigger auto reply → quan sát",
       "5 loại action",
       "- Cả 5 action hiển thị đủ trong modal action của bot B\n- t_actions_detail có đủ bản ghi\n"
       "- Friend bot B trigger → nhận đủ output của 5 action",
       env="PRODUCTION",
       note="⚠️ Backup 1.0 r17/r19/r20 ghi NG với lý do 'chưa tạo được action này' ⇒ 3 loại (bookmark, status chat, "
            "block/ẩn) TỪNG KHÔNG TEST ĐƯỢC. Nguồn: Backup (job) r10, r16-r19 + Backup 1.0 r11, r17-r20"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): action SCENARIO của auto reply ⇒ bot B phải lấy đúng id scenario TƯƠNG ỨNG đã tạo ở bot B",
       BK + "\n- Bot A có quy tắc auto reply với action start scenario S1",
       "1. Chạy backup\n2. Query: SELECT data FROM t_actions_detail WHERE type='scenario' — của quy tắc ở bot B\n"
       "3. So sánh id scenario trong data với id scenario S1 ĐÃ ĐƯỢC BACKUP sang bot B\n"
       "4. Friend bot B trigger → query scenario_lineuser",
       "Action start scenario S1",
       "- t_actions_detail của bot B trỏ tới id scenario của BOT B (không phải id của bot A)\n"
       "- Friend bot B trigger → được start vào scenario tương ứng của bot B",
       env="PRODUCTION",
       note="⚠️ Backup 1.0 r12 ghi 1 lần NG ⇒ điểm ĐÃ TỪNG LỖI. Nguồn: Backup (job) r11 + Backup 1.0 r12"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): action TAG của auto reply ⇒ bot B lấy đúng tag tương ứng đã backup sang bot B",
       BK + "\n- Bot A có quy tắc auto reply với action gắn tag T1",
       "1. Chạy backup\n2. Query t_actions_detail type='tag' của quy tắc ở bot B\n"
       "3. So sánh id tag với tag T1 đã backup sang bot B\n4. Friend bot B trigger → query tag_line_user",
       "Action gắn tag T1",
       "- t_actions_detail trỏ tới id tag của BOT B\n- Friend bot B trigger → được gắn tag tương ứng của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r12 + Backup 1.0 r13"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): action TEMPLATE của auto reply ⇒ bot B lấy đúng id template tương ứng ở bot B",
       BK + "\n- Bot A có quy tắc auto reply với action gửi template T1",
       "1. Chạy backup\n2. Query t_actions_detail type='template' ở bot B\n"
       "3. So sánh id template với template đã backup sang bot B\n4. Friend bot B trigger → quan sát LINE app",
       "Action gửi template T1",
       "- t_actions_detail trỏ tới id template của BOT B\n- Friend bot B nhận đúng template của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r13 + Backup 1.0 r14"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): action RICH MENU của auto reply ⇒ bot B lấy đúng id rich menu tương ứng ở bot B",
       BK + "\n- Bot A có quy tắc auto reply với action đổi richmenu RM1",
       "1. Chạy backup\n2. Query t_actions_detail type='richmenu' ở bot B\n"
       "3. So sánh id với richmenu đã backup sang bot B\n4. Friend bot B trigger → kiểm tra richmenu trên LINE app",
       "Action đổi richmenu RM1",
       "- t_actions_detail trỏ tới id richmenu của BOT B\n- Richmenu của friend bot B đổi đúng trên LINE app",
       env="PRODUCTION",
       note="⚠️ Backup 1.0 r15 ghi 'Không có' ở nhiều đợt ⇒ ít được test lại. "
            "Nguồn: Backup (job) r14 + Backup 1.0 r15"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Abnormal",
       "Backup (job): action REMIND của auto reply ⇒ bot B phải lấy id remind của BOT B, KHÔNG được trỏ về bot gốc",
       BK + "\n- Bot A có quy tắc auto reply với action リマインド RE1",
       "1. Chạy backup\n2. Query t_actions_detail type='remind' của quy tắc ở bot B, đọc id remind trong data\n"
       "3. Query danh sách remind của bot B, đối chiếu id\n4. Friend bot B trigger → query event_step_time",
       "Action リマインド RE1",
       "- t_actions_detail của bot B trỏ tới id remind thuộc BOT B\n"
       "- KHÔNG được trỏ tới id remind của bot gốc\n- Friend bot B trigger → tạo event_step_time đúng remind của bot B",
       env="PRODUCTION",
       note="⚠️ ĐÂY LÀ BUG ĐÃ ĐƯỢC GHI NHẬN: Backup 1.0 r16 ghi NG — 't_action_detail đang lấy id remind của bot gốc' "
            "và note tiếp 'chỗ này c check lại thấy vẫn lỗi'. BẮT BUỘC verify lại. "
            "Nguồn: Backup (job) r15 + Backup 1.0 r16"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Abnormal",
       "Backup (job): FILTER của quy tắc auto reply — xác nhận trạng thái hỗ trợ backup",
       BK + "\n- Bot A có quy tắc auto reply đã setting filter (filters_v2, parent_type='auto_reply')",
       "1. Chạy backup\n2. Mở form edit quy tắc ở bot B, xem ô「対象条件」và mở modal「絞込み」\n"
       "3. Query: SELECT * FROM filters_v2 WHERE parent_type='auto_reply' AND parent_id=<quy tắc bot B>",
       "Quy tắc có ≥1 điều kiện filter",
       "- Ghi lại hành vi THẬT: filter có được backup sang bot B không?\n"
       "- Nếu không: form bot B hiện 対象条件 trống, filters_v2 không có bản ghi",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="⚠️ Corpus ghi cột staging =「Chưa support」cho dòng Filter (Backup (job) r20; Backup 1.0 r21 ghi "
            "'Chưa support' ở TOÀN BỘ 10 đợt). Spec KHÔNG nói gì về việc backup filter ⇒ MT-22. "
            "CẦN LEADER QUYẾT: filter có nằm trong phạm vi backup không"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup (job): trạng thái ON/OFF (is_stopped) của quy tắc được backup đúng",
       BK + "\n- Bot A có 1 quy tắc ON (is_stopped=0) và 1 quy tắc OFF (is_stopped=1)",
       "1. Chạy backup\n2. Query: SELECT id, is_stopped FROM auto_reply WHERE bot_id=B\n"
       "3. Mở màn list bot B xem cột「稼働状況」của 2 quy tắc",
       "2 quy tắc: is_stopped = 0 và = 1",
       "- Bot B: quy tắc ON có is_stopped = 0, quy tắc OFF có is_stopped = 1\n"
       "- Màn list bot B hiện đúng ON / OFF",
       env="PRODUCTION",
       note="⚠️ Backup 1.0 r23 ghi 'Không có' ở nhiều đợt ⇒ nhánh OFF ít được test lại. "
            "Nguồn: Backup (job) r21-r22 + Backup 1.0 r22-r23"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Change bot: sau khi đổi bot ⇒ auto reply GIỮ NGUYÊN keyword và setting action của bot cũ",
       "- Bot A đã cấu hình auto reply đầy đủ\n- Thực hiện chức năng change bot (đổi LINE OA liên kết)",
       "1. Thực hiện change bot\n2. Mở /basic/reply\n3. So sánh danh sách quy tắc, keyword, action với trước khi đổi\n"
       "4. Query auto_reply + keyword + t_actions_detail",
       "Toàn bộ cấu hình auto reply của bot cũ",
       "- Giữ nguyên các keyword\n- Giữ nguyên setting action của từng quy tắc\n- DB không mất bản ghi",
       env="PRODUCTION",
       note="Nguồn: 15.3 TCsLine_ChangeBot / Change bot r200"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Change bot: friend MỚI của bot mới gửi keyword hợp lệ ⇒ bot mới gửi action tương ứng",
       "- Đã thực hiện change bot xong\n- Có friend MỚI kết bạn với bot sau khi change",
       "1. Friend mới gửi keyword hợp lệ\n2. Quan sát LINE app của friend mới\n3. Mở màn chat 1:1",
       "Keyword hợp lệ của quy tắc đã cấu hình trước khi change bot",
       "- Bot mới gửi action tương ứng cho friend mới\n- Màn chat 1:1 hiện message với trigger「自動応答」",
       env="PRODUCTION",
       note="Nguồn: 15.3 TCsLine_ChangeBot / Change bot r201"),

    # ═══════════════ Phân quyền & môi trường ═══════════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff KHÔNG có quyền màn 自動応答: hover menu ⇒ hiện message 操作できません。…, KHÔNG click vào được",
       "- Có account staff (副管理人 / 運用者 / サポート) bị TẮT quyền màn 自動応答\n- Đăng nhập bằng account staff đó",
       "1. Ở menu trái, di chuột đến mục「自動応答」\n2. Quan sát icon + text hiển thị\n3. Thử click vào mục đó\n"
       "4. Cuộn trang xuống rồi hover lại, kiểm tra vị trí text",
       "3 loại role staff: 副管理人 / 運用者 / サポート — đều bị tắt quyền màn 自動応答",
       "- Hiện icon khóa + message:\n"
       "「操作できません。\nこの機能の操作権限が付与されていません。\n主管理者に操作権限を付与してもらうことで操作が可能となります。」\n"
       "- KHÔNG click vào được màn hình\n- Khi cuộn trang: text hiển thị đúng vị trí menu, không lệch",
       note="3 role cùng 1 kết quả nên giữ chung. Nguồn: TCsLine_Improve chung / Phân quyền r4-r5 + r7 + r12 + r17 "
            "(11/2023 — TC ~2.8 năm tuổi, CẦN VERIFY LẠI)"),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff CÓ quyền màn 自動応答 ⇒ hover không hiện text lỗi, click vào được và thao tác bình thường",
       "- Account staff được BẬT quyền màn 自動応答",
       "1. Đăng nhập bằng staff\n2. Hover mục「自動応答」→ quan sát\n3. Click vào\n"
       "4. Thử tạo / sửa / xóa 1 quy tắc auto reply",
       "Staff được cấp quyền màn 自動応答",
       "- KHÔNG hiện text lỗi khi hover\n- Click vào màn hình bình thường\n"
       "- Tạo / sửa / xóa quy tắc thành công như account chính",
       note="Nguồn: TCsLine_Improve chung / Phân quyền r6 + r8. ⚠️ Corpus của file AutoReply có 4 dòng "
            "'Check account staff' (Ver1.0 r52, r96, r121, r199) nhưng KHÔNG ghi kết quả mong đợi ⇒ "
            "phần thao tác CRUD do AI bổ sung"),

    tc("Phân quyền & môi trường", "PERM-004", "Abnormal",
       "Staff KHÔNG có quyền: truy cập TRỰC TIẾP URL /basic/reply và /basic/reply/new ⇒ bị chặn ở tầng API, không chỉ ẩn menu",
       "- Account staff bị TẮT quyền màn 自動応答",
       "1. Đăng nhập staff\n2. Gõ thẳng URL /basic/reply vào thanh địa chỉ → quan sát\n"
       "3. Gõ thẳng URL /basic/reply/new?group_id=0 → quan sát\n"
       "4. Gọi trực tiếp API POST /ajax/get-list-group (action deleteItem) bằng devtool → quan sát response\n"
       "5. Query auto_reply xác nhận không bị đổi dữ liệu",
       "Staff không quyền; 2 URL + 1 API call trực tiếp",
       "- Cả 3 lối vào đều bị CHẶN (redirect hoặc trả lỗi quyền), KHÔNG chỉ ẩn menu\n"
       "- KHÔNG có bản ghi auto_reply nào bị xóa/sửa",
       spec="Đã hỏi leader",
       note="⚠️ Gap #18 của spec: 'Cơ chế kiểm tra quyền Staff — không phát hiện middleware riêng, tin cậy "
            "Trung bình'. logic-spec.md §Authorization ghi rõ 'Không phát hiện kiểm tra quyền Staff' ⇒ MT-23. "
            "Corpus KHÔNG có TC gọi API trực tiếp ⇒ TC do AI viết. CẦN LEADER QUYẾT"),

    tc("Phân quyền & môi trường", "PERM-002", "Normal",
       "Thay đổi setting phân quyền của staff cho màn 自動応答 ⇒ có hiệu lực ngay ở cả 2 chiều",
       "- Account staff 副管理人 đang ĐƯỢC phép mở màn 自動応答",
       "1. Admin chính đổi setting: TẮT quyền màn 自動応答 của staff đó\n"
       "2. Staff reload trang, hover mục「自動応答」→ quan sát + thử click\n"
       "3. Admin chính BẬT lại quyền\n4. Staff reload, hover + click → quan sát",
       "2 chiều đổi quyền: được phép → không được phép → được phép",
       "- Sau khi tắt quyền: hover hiện message「操作できません。…」, không click được\n"
       "- Sau khi bật lại: click vào màn hình bình thường",
       note="Nguồn: TCsLine_Improve chung / Phân quyền r22-r23 (11/2023 — CẦN VERIFY LẠI)"),

    tc("Phân quyền & môi trường", "ENV-001", "Normal",
       "Regression môi trường: cùng bộ TC chính của auto reply chạy đúng trên DEV / STAGING / PRODUCTION",
       "- Bộ TC chính: tạo quy tắc keyword, tạo quy tắc all message, cấu hình action, friend trigger\n"
       "- Có tài khoản test trên cả 3 môi trường",
       "1. Chạy bộ TC chính trên DEV → ghi kết quả\n2. Chạy trên STAGING → ghi kết quả\n"
       "3. Chạy trên PRODUCTION (tài khoản test) → ghi kết quả\n4. So sánh 3 kết quả",
       "Bộ TC chính × 3 môi trường",
       "- Kết quả GIỐNG NHAU trên cả 3 môi trường\n"
       "- Nếu lệch: ghi rõ môi trường nào lệch và lệch ở bước nào",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="RULE-08 + ENV. Corpus của file AutoReply có cột kết quả riêng cho staging ('staging 12/7') nhưng KHÔNG "
            "có TC đối chiếu chéo môi trường ⇒ TC lấp GAP do AI viết"),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Abnormal",
       "Flow LEGACY: các endpoint cũ /basic/reply/edit/{id}, /basic/reply/store, /basic/reply/save — "
       "còn dùng được hay đã chết?",
       "- Bot A có quy tắc auto reply\n- Có thể gọi trực tiếp URL/endpoint legacy",
       "1. Truy cập /basic/reply/edit/<reply_id> → quan sát view hiển thị\n"
       "2. Nếu form legacy mở được: nhập dữ liệu, submit POST /basic/reply/save → quan sát\n"
       "3. Query auto_reply + filters (bảng legacy) + filters_v2 sau khi submit\n"
       "4. Mở lại quy tắc bằng flow V2 (/basic/reply/new?reply_id=...) kiểm tra dữ liệu",
       "3 endpoint legacy: EP-03 edit, EP-04 store, EP-05 save",
       "- Ghi lại hành vi THẬT: form legacy còn mở được không, submit có lưu không\n"
       "- Nếu lưu được: dữ liệu ghi vào bảng `filters` (legacy) hay `filters_v2`?\n"
       "- Mở lại bằng flow V2: dữ liệu hiển thị có đúng không (nguy cơ mất filter)",
       spec="Đã hỏi leader",
       note="⚠️ BR-13 Filter dual system + §1 Dual Flow: spec ghi 'Flow V2 là flow đang được sử dụng. Flow Legacy "
            "vẫn tồn tại trong code nhưng có thể không còn được dùng — tin cậy TRUNG BÌNH'. Corpus KHÔNG có TC nào "
            "cho flow legacy ⇒ MT-24. CẦN LEADER QUYẾT có đưa flow legacy vào phạm vi test không"),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Abnormal",
       "BR-03 legacy: nội dung text reply được base64_encode khi lưu / decode khi đọc ⇒ dữ liệu cũ hiển thị đúng",
       "- Bot có quy tắc auto reply được tạo từ flow LEGACY (reply_kind=1, reply_content là chuỗi base64)",
       "1. Query: SELECT reply_kind, reply_content FROM auto_reply WHERE reply_kind=1 — xác nhận là base64\n"
       "2. Mở màn list /basic/reply xem quy tắc đó\n3. Mở form edit quy tắc đó\n"
       "4. Friend trigger quy tắc → quan sát LINE app",
       "Quy tắc legacy có reply_content = chuỗi base64",
       "- Màn list và form edit hiển thị nội dung ĐÃ DECODE (đọc được, không phải chuỗi base64)\n"
       "- Friend nhận được nội dung text đúng trên LINE app",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-03 (ReplyController.php:153-154, AutoReply.php:56). Corpus KHÔNG có TC dữ liệu legacy ⇒ "
            "TC lấp GAP do AI viết, gắn MT-24"),

    tc("Phân quyền & môi trường", "PERF-LARGE-001", "Boundary",
       "Hiệu năng runtime: bot có SỐ LƯỢNG LỚN quy tắc auto reply đang ON ⇒ friend vẫn nhận action trong thời gian chấp nhận được",
       "- Bot A có ≥100 quy tắc auto reply đang ON (nhiều dạng keyword khác nhau)\n- Friend F đã kết bạn",
       "1. F gửi text khớp 1 quy tắc ở CUỐI danh sách\n2. Bấm giờ từ lúc gửi đến lúc nhận được action\n"
       "3. Lặp lại 5 lần, ghi thời gian từng lần\n4. Query callback_event xem có event nào bị treo status = 1 không",
       "≥100 quy tắc ON; đo 5 lần",
       "- F nhận được action trong thời gian chấp nhận được (ghi rõ số giây đo được)\n"
       "- KHÔNG có event nào treo ở status = 1 (PROCESSING)\n- KHÔNG mất action",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Spec §7: job duyệt TỪNG rule, KHÔNG break sau match (BR-15) ⇒ số rule càng nhiều càng chậm. "
            "Corpus KHÔNG có TC hiệu năng ⇒ TC lấp GAP do AI viết. RULE-08 bắt buộc PRODUCTION"),

    tc("Phân quyền & môi trường", "REG-SPEC-001", "Abnormal",
       "NHE-06: thứ tự XỬ LÝ rule ở runtime so với thứ tự HIỂN THỊ ở màn list (position DESC)",
       "- Bot A có 3 quy tắc cùng khớp 1 text, mỗi quy tắc gửi 1 text khác nhau (A / B / C)\n"
       "- Sắp xếp trên màn list theo thứ tự: C, B, A (position DESC)",
       "1. Ghi lại thứ tự hiển thị 3 quy tắc trên màn list\n2. Friend F gửi text khớp cả 3\n"
       "3. Ghi lại THỨ TỰ 3 message F nhận được trên LINE app\n4. So sánh 2 thứ tự",
       "3 quy tắc cùng khớp; thứ tự hiển thị C → B → A",
       "- Ghi lại thứ tự thực tế F nhận được (A/B/C theo trình tự nào)\n"
       "- Kết luận: thứ tự runtime có khớp thứ tự hiển thị không",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="⚠️ job-spec.md:394 'Các rules được load từ DB theo thứ tự mặc định (không ORDER BY position)' trong khi "
            "CRUD sort theo position DESC (BR-05) ⇒ thứ tự UI có thể KHÁC thứ tự runtime (NHE-06) ⇒ MT-25. "
            "Corpus KHÔNG có TC. CẦN LEADER QUYẾT thứ tự nào là đúng"),
]
