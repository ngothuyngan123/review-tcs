# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 5: Runtime (webhook → callback_event → checkAutoReply → doAction → LINE API)."""
from _common import tc

RT = ("- Bot A đã liên kết LINE OA, webhook hoạt động\n"
      "- 1 friend LINE (F) đã kết bạn với bot A\n- Job Spring Boot HandlePostbackTask đang chạy (ENABLE_POSTBACK = true)")

S5 = [
    # ═══════════════ Runtime — nhận message & callback ═══════════════
    tc("Runtime — nhận message & callback", "INTG-LINE-001", "Normal",
       "Bot KHÔNG có auto reply: friend gửi 7 loại message ⇒ đều hiển thị được ở màn chat 1:1, không có tin trả về",
       RT + "\n- Bot A KHÔNG có quy tắc auto reply nào đang ON",
       "1. Friend F lần lượt gửi: text / sticker / location / ảnh / video / audio / file / text của nút button\n"
       "2. Sau mỗi lần, mở màn chat 1:1 kiểm tra message hiển thị\n"
       "3. Query: SELECT status FROM callback_event WHERE bot_id=A ORDER BY id DESC",
       "8 loại message: text, sticker, location, ảnh, video, audio, file, text của button",
       "- Cả 8 loại đều hiển thị đúng ở màn chat 1:1 (đúng dạng: ảnh xem được, video phát được, file tải được)\n"
       "- Friend KHÔNG nhận được tin trả về nào\n- callback_event chuyển sang status = 2 (STATUS_DONE)",
       env="PRODUCTION",
       note="8 loại cùng 1 kết quả nên giữ chung; điểm khác biệt (hiển thị đúng dạng) ghi ở Kết quả mong đợi. "
            "RULE-08 (media + job). Nguồn: TCsLine_JOB / Test callback friend r3-r10"),

    tc("Runtime — nhận message & callback", "INTG-LINE-001", "Normal",
       "Bot CÓ auto reply dạng 全てのメッセージ: friend gửi 7 loại message ⇒ hiển thị ở chat 1:1 VÀ nhận được action",
       RT + "\n- Bot A có 1 quy tắc auto reply dạng 全てのメッセージ đang ON, action gửi text「OK」",
       "1. Friend F lần lượt gửi: text / sticker / ảnh / video / audio / file / text của nút button\n"
       "2. Sau mỗi lần: kiểm tra màn chat 1:1 + LINE app của F",
       "7 loại message",
       "- Cả 7 loại: message của friend hiển thị đúng ở màn chat 1:1\n"
       "- Cả 7 loại: F nhận được「OK」trên LINE app (send action autoreply)\n"
       "- Màn chat 1:1 hiện message trả về với trigger「自動応答」",
       env="PRODUCTION",
       note="⚠️ Điểm quan trọng: quy tắc 全てのメッセージ phản ứng với CẢ sticker/ảnh/video/file, không chỉ text. "
            "Nguồn: TCsLine_JOB / Test callback friend r11-r17"),

    tc("Runtime — nhận message & callback", "ENV-002", "Normal",
       "Đổi domain callback của bot (cb.lmes.jp → cb-2.lmes.jp) ⇒ message của friend vẫn nhận được và auto reply vẫn chạy",
       RT + "\n- Bot A đang dùng callback https://cb.lmes.jp/line/callback/add/<bot_id>",
       "1. Ghi nhận hoạt động bình thường trên callback hiện tại\n"
       "2. Đổi webhook URL của bot sang https://cb-2.lmes.jp/line/callback/add/<bot_id>\n"
       "3. Friend F gửi text / ảnh / file / sticker — có và không có auto reply\n"
       "4. Kiểm tra màn chat 1:1 + LINE app + bảng callback_event",
       "2 domain callback: cb.lmes.jp và cb-2.lmes.jp",
       "- Trên cả 2 domain: message user gửi đến đều hiển thị được ở màn chat 1:1\n"
       "- Case có auto reply: F nhận được action; case không có: không nhận\n"
       "- callback_event ghi nhận đủ event, status kết thúc = 2",
       env="PRODUCTION",
       note="RULE-08: domain + job bắt buộc test PRODUCTION. Nguồn: TCsLine_JOB / Test callback friend r29 + r37-r40"),

    tc("Runtime — nhận message & callback", "JOB-001", "Normal",
       "callback_event state machine: message được xử lý ⇒ status 0 (NEW) → 1 (PROCESSING) → 2 (DONE)",
       RT + "\n- Bot A có 1 quy tắc auto reply đang ON",
       "1. Friend F gửi text trigger auto reply\n"
       "2. Poll bảng callback_event trong quá trình xử lý: SELECT id, type, status FROM callback_event "
       "WHERE bot_id=A ORDER BY id DESC LIMIT 1\n3. Ghi lại các giá trị status quan sát được",
       "1 message text trigger auto reply",
       "- Bản ghi callback_event được INSERT với type='message', status = 0\n"
       "- Chuyển sang status = 1 khi job poll (mỗi 500ms)\n- Kết thúc status = 2 (STATUS_DONE)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="RULE-08 (job). Spec §7 mô tả state machine 11 trạng thái. Corpus KHÔNG có TC theo dõi callback_event "
            "⇒ TC lấp GAP do AI viết theo spec"),

    tc("Runtime — nhận message & callback", "JOB-001", "Abnormal",
       "callback_event: tin nhắn từ GROUP chat ⇒ status = 10 (STATUS_IGNORE_GROUP_MESSAGE), không chạy auto reply",
       RT + "\n- Bot A được add vào 1 group LINE\n- Bot A có quy tắc auto reply dạng 全てのメッセージ đang ON",
       "1. Trong group, 1 thành viên gửi text trùng điều kiện auto reply\n"
       "2. Quan sát group trên LINE app\n3. Query: SELECT status FROM callback_event WHERE bot_id=A ORDER BY id DESC LIMIT 1",
       "Message text gửi trong group chat",
       "- Bot KHÔNG gửi auto reply vào group\n- callback_event.status = 10 (STATUS_IGNORE_GROUP_MESSAGE)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Spec §7 state machine giá trị 10. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết theo spec, "
            "CẦN LEADER XÁC NHẬN"),

    tc("Runtime — nhận message & callback", "JOB-001", "Abnormal",
       "callback_event: bot hết hạn > 7 ngày ⇒ status = 8 (STATUS_EXPIRED_BOT), auto reply không chạy",
       "- Bot A có hợp đồng đã hết hạn > 7 ngày\n- Bot A vẫn còn quy tắc auto reply đang ON",
       "1. Friend F gửi text trigger auto reply\n2. Quan sát LINE app của F\n"
       "3. Query: SELECT status FROM callback_event WHERE bot_id=A ORDER BY id DESC LIMIT 1",
       "Bot hết hạn > 7 ngày",
       "- F KHÔNG nhận được auto reply\n- callback_event.status = 8 (STATUS_EXPIRED_BOT)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Spec §7 state machine giá trị 8. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết theo spec"),

    tc("Runtime — nhận message & callback", "CONC-002", "Abnormal",
       "BR-22 concurrency lock: 1 friend gửi NHIỀU tin liên tiếp rất nhanh ⇒ không bị xử lý song song, action không trùng lặp",
       RT + "\n- Quy tắc keyword「テスト」đang ON, chế độ「1度のみアクション稼働」, action gửi text",
       "1. Friend F gửi「テスト」5 lần trong vòng 1 giây\n2. Đếm số tin nhắn F nhận được trên LINE app\n"
       "3. Query: SELECT COUNT(*) FROM auto_reply_history WHERE reply_id=<rule> AND line_id=<F>",
       "5 message「テスト」trong 1 giây từ cùng 1 friend",
       "- F nhận được ĐÚNG 1 tin trả về (do 1度のみ + lock theo line_id)\n"
       "- auto_reply_history có ĐÚNG 1 bản ghi cho cặp (F, rule)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-22 (ConcurrentHashMap lock theo line_id) + BR-16. Corpus KHÔNG có TC race condition cho auto reply "
            "⇒ TC lấp GAP do AI viết theo spec, RULE-08 bắt buộc PRODUCTION"),

    # ═══════════════ Runtime — match keyword & gửi action ═══════════════
    tc("Runtime — match keyword & gửi action", "MSG-USER-001", "Normal",
       "BR-15 multi-rule: 2 quy tắc cùng khớp 1 tin nhắn ⇒ CẢ 2 action đều chạy, mỗi rule ghi 1 auto_reply_history",
       RT + "\n- Quy tắc R1: keyword「予約」部分一致, action gửi text「A」\n"
       "- Quy tắc R2: 全てのメッセージ, action gửi text「B」\n- Cả 2 đang ON",
       "1. Friend F gửi「予約したい」\n2. Đếm và ghi lại các tin F nhận được trên LINE app\n"
       "3. Query: SELECT reply_id FROM auto_reply_history WHERE line_id=<F> ORDER BY id DESC",
       "Text「予約したい」khớp cả R1 và R2",
       "- F nhận được CẢ「A」và「B」\n- auto_reply_history có 2 bản ghi: (F, R1) và (F, R2)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="⚠️ BR-15: vòng lặp KHÔNG break sau match đầu tiên. Corpus Ver1.0 r25-r28 đánh dấu 'Not test' với lý do "
            "'ko cần check case kết hợp này' ⇒ MT-03. CẦN LEADER QUYẾT có đưa vào phạm vi test không"),

    tc("Runtime — match keyword & gửi action", "MSG-USER-001", "Boundary",
       "BR-18: text người dùng có khoảng trắng ở CUỐI ⇒ được trimEnd trước khi so khớp keyword 完全一致",
       RT + "\n- Quy tắc keyword「テスト」chế độ 完全一致, action gửi text",
       "1. Friend F gửi「テスト␣␣」(có 2 khoảng trắng cuối)\n2. Quan sát LINE app\n"
       "3. Friend F gửi「␣␣テスト」(có khoảng trắng ĐẦU)\n4. Quan sát LINE app",
       "Text 1:「テスト␣␣」; text 2:「␣␣テスト」",
       "- Text có khoảng trắng CUỐI: F NHẬN được action (đã trimEnd)\n"
       "- Text có khoảng trắng ĐẦU: ghi lại hành vi thật — có nhận được action không?",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="⚠️ job-spec.md:304 chỉ nói `TextUtils.trimEnd()` (trim CUỐI). Nhánh khoảng trắng ĐẦU KHÔNG được spec "
            "mô tả và corpus cũng không test ⇒ MT-02. CẦN LEADER QUYẾT hành vi mong đợi"),

    tc("Runtime — match keyword & gửi action", "MSG-USER-001", "Normal",
       "Runtime: quy tắc đang OFF (is_stopped=1) hoặc đã xóa (is_deleted=1) ⇒ KHÔNG được load, không chạy action",
       RT + "\n- Quy tắc R1 keyword「テスト」đang ON; quy tắc R2 keyword「テスト2」đang OFF; "
       "quy tắc R3 keyword「テスト3」đã bị xóa",
       "1. F gửi「テスト」→ quan sát\n2. F gửi「テスト2」→ quan sát\n3. F gửi「テスト3」→ quan sát",
       "3 keyword tương ứng 3 trạng thái rule: ON / OFF / đã xóa",
       "-「テスト」: F NHẬN được action\n-「テスト2」: KHÔNG nhận\n-「テスト3」: KHÔNG nhận",
       env="PRODUCTION",
       note="Spec §7: load rules WHERE is_stopped != 1 AND is_deleted != 1. "
            "Nguồn gián tiếp: Ver1.0 r120. Ma trận 3 trạng thái do AI bổ sung"),

    tc("Runtime — match keyword & gửi action", "MSG-001", "Normal",
       "BR-21: lần gửi đầu dùng replyToken (LINE Reply API); khi token hết hạn/đã dùng ⇒ fallback Push API",
       RT + "\n- Quy tắc auto reply có action gửi ≥2 message (VD 2 template + 1 text)",
       "1. Friend F gửi keyword trigger\n2. Quan sát toàn bộ message F nhận được trên LINE app\n"
       "3. Kiểm tra log/thống kê số message tính phí (Push API) vs miễn phí (Reply API)\n"
       "4. Đối chiếu thứ tự message trên LINE app với thứ tự cấu hình action",
       "Action gồm 3 message: template T1, template T2, text",
       "- F nhận đủ 3 message, ĐÚNG THỨ TỰ đã cấu hình\n"
       "- Message đầu gửi qua Reply API (không tính phí); các message sau fallback Push API",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-21 (SentMessageHelper.java:54-100) — ảnh hưởng CHI PHÍ LINE API. Nguồn: TCsLine_JOB / "
            "Send msg reply token r11『Check các tính năng khác có dùng reply token → auto reply』— corpus KHÔNG ghi "
            "kết quả mong đợi, AI viết theo spec. RULE-08 bắt buộc PRODUCTION"),

    tc("Runtime — match keyword & gửi action", "MSG-001", "Normal",
       "Send msg reply token: auto reply với các loại action gửi tin ⇒ friend nhận đủ, tương tự màn setting add old friend",
       RT + "\n- Quy tắc auto reply có nhiều loại action gửi tin",
       "1. Cấu hình quy tắc với: action text + template / add tag có action gửi message / add tag có action start scen / "
       "start scen / thêm friend info có action gửi tin\n2. Friend F gửi keyword trigger\n"
       "3. Quan sát LINE app + màn chat 1:1 sau mỗi cấu hình",
       "5 tổ hợp action gửi tin",
       "- Cả 5 tổ hợp: F nhận đủ message tương ứng trên LINE app\n"
       "- Màn chat 1:1 hiển thị đủ message với trigger「自動応答」",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Send msg reply token r11 — corpus liệt kê các action cần check nhưng KHÔNG ghi "
            "kết quả mong đợi cụ thể, AI viết kết quả đo lường được. TC ~3 năm tuổi (2023-06), CẦN VERIFY LẠI"),

    tc("Runtime — match keyword & gửi action", "MSG-001", "Normal",
       "Quote message: message auto reply đã gửi cho friend ⇒ khi friend quote lại, màn chat 1:1 hiển thị được dạng quote",
       RT + "\n- Quy tắc auto reply có action gửi text và action gửi template",
       "1. F gửi keyword trigger → nhận được message auto reply\n"
       "2. Trên LINE app, F quote lại message auto reply đó và gửi tiếp\n3. Mở màn chat 1:1 quan sát",
       "2 loại: action send text và action send template",
       "- Cả 2 loại: message quote hiển thị đúng dạng quote ở màn chat 1:1 (thấy được message gốc được quote)",
       env="PRODUCTION",
       note="Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / Content: Hiển thị msg r1117-r1118 — dòng "
            "『4. Action khi có callback: add friend thường, landing, auto reply』"),

    tc("Runtime — match keyword & gửi action", "INTG-HOOK-001", "Normal",
       "Start / stop scenario từ auto reply ⇒ màn chat 1:1 hiển thị đúng message start / stop scenario",
       RT + "\n- Có scenario S1\n- Quy tắc auto reply loại 全てのメッセージ và loại キーワード",
       "1. Cấu hình auto reply loại 全て với action start S1 → F trigger → xem màn chat 1:1\n"
       "2. Cấu hình auto reply loại キーワード với action start S1 → F trigger → xem màn chat 1:1\n"
       "3. Lặp lại với action STOP S1 cho cả 2 loại",
       "2 loại quy tắc × 2 hành động (start / stop) = 4 tổ hợp",
       "- Cả 4 tổ hợp: màn chat 1:1 hiện message hệ thống tương ứng (start scenario / stop scenario)\n"
       "- Message ghi nhận đúng nguồn là auto reply",
       env="PRODUCTION",
       note="Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / Content: Hiển thị msg r242-r243 (start), "
            "r322-r323 (stop), r1195 + r1210. ⚠️ r1195 đánh dấu 'Not test' ⇒ nhánh start scenario từ auto reply "
            "chưa từng được test ở màn chat"),

    tc("Runtime — match keyword & gửi action", "UI-003", "Normal",
       "Trigger hiển thị ở màn chat 1:1: message do auto reply gửi ⇒ hiện tính năng「自動応答」+ detail theo loại quy tắc",
       RT + "\n- Quy tắc A: 全てのメッセージ; quy tắc B: keyword chỉ định. Cả 2 có action gửi text",
       "1. F trigger quy tắc A → mở màn chat 1:1, click xem trigger của message\n"
       "2. F trigger quy tắc B → mở màn chat 1:1, click xem trigger",
       "2 loại quy tắc auto reply",
       "- Quy tắc A: Text tính năng =「自動応答」; Tên quản lý = hiện dấu「-」; detail action =「全てのメッセージ」\n"
       "- Quy tắc B: Text tính năng =「自動応答」; Tên quản lý = dấu「-」; detail action =「キーワード」",
       env="PRODUCTION",
       note="Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / Content: Hiển thị msg r1189-r1190. "
            "Tên quản lý hiện「-」vì form auto reply KHÔNG có trường nhập tên (Gap #13 của spec)"),

    # ═══════════════ Runtime — 自動確認済み (confirm message) ═══════════════
    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "Bug #31873: message thỏa mãn auto reply + KHÔNG bật tự động confirm ⇒ status của friend chuyển thành CHƯA confirm",
       RT + "\n- Màn チャット設定: KHÔNG tick checkbox tự động confirm message auto reply\n"
       "- Friend F đang có status_last_message = 1 (đã confirm)",
       "1. F gửi text thỏa mãn quy tắc auto reply\n2. Query: SELECT status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "3. Mở màn chat 1:1 xem trạng thái 未確認/確認済 ở góc trên bên phải",
       "F: status_last_message = 1 trước khi gửi",
       "- DB: status_last_message = 0 (chưa confirm)\n"
       "- Màn chat 1:1 hiện「未確認」và CHO PHÉP đổi trạng thái",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r150 (Bug #31873 [14-09-2025][8016]). "
            "Hiện tượng gốc: mở chat ở status 未確認 nhưng góc trên hiện 確認済 và không đổi được"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "Bug #31873: message thỏa mãn auto reply + CÓ bật tự động confirm ⇒ message mới được tự confirm, "
       "KHÔNG update status confirm của friend",
       RT + "\n- Màn チャット設定: ĐÃ tick tự động confirm message auto reply\n- Friend F có status_last_message = 1",
       "1. F gửi text thỏa mãn quy tắc auto reply\n2. Query status_last_message của F\n3. Mở màn chat 1:1 quan sát",
       "F: status_last_message = 1; đã bật tự động confirm auto reply",
       "- Message mới được tự động confirm\n- status_last_message của F KHÔNG bị đổi (vẫn = 1)\n"
       "- Màn chat 1:1 hiện「確認済」",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r151"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "Bug #31873: 3 loại message khác (nút button 【〇〇】/ stamp / message thường) × 2 chế độ confirm ⇒ status đúng theo chế độ",
       RT + "\n- Friend F có status_last_message = 1",
       "1. Với chế độ KHÔNG tự động confirm: F gửi lần lượt message nút button「【xx】」/ stamp / text thường → "
       "query status_last_message sau mỗi lần\n"
       "2. Với chế độ CÓ tự động confirm tương ứng: lặp lại 3 loại message → query lại",
       "3 loại message × 2 chế độ confirm = 6 tổ hợp",
       "- Không tự động confirm (cả 3 loại): status_last_message = 0 (chưa confirm)\n"
       "- Có tự động confirm (cả 3 loại): message được tự confirm, status_last_message KHÔNG đổi",
       env="PRODUCTION",
       note="Ma trận 6 điểm gom theo 2 kết quả, ghi rõ từng nhóm. "
            "Nguồn: TCsLine_JOB / Test fix bug KH r146-r149 + r152"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "チャット設定: tick checkbox「自動応答 [すべてのメッセージに反応] のメッセージ」⇒ tin nhắn trigger quy tắc loại "
       "全てのメッセージ được tự confirm",
       RT + "\n- Màn チャット設定 tab「メッセージの自動確認済み変更」\n- Có quy tắc auto reply loại 全てのメッセージ đang ON",
       "1. TICK checkbox「自動応答 [すべてのメッセージに反応] のメッセージ」, lưu\n"
       "2. Friend F gửi text\n3. Query bảng conversation của F (trạng thái confirm)\n4. Mở màn chat 1:1 quan sát",
       "Checkbox 自動応答 [すべてのメッセージに反応] = TICK",
       "- Tin nhắn đó được thực hiện confirm; bảng conversation ghi nhận trạng thái đã confirm\n"
       "- Màn chat 1:1 hiện「確認済」",
       env="PRODUCTION",
       note="Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / AI_TCs_Setting_chat_v1 r105 (BS_032)"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "チャット設定: BỎ tick「自動応答 [すべてのメッセージに反応] のメッセージ」⇒ tin nhắn KHÔNG được tự confirm",
       RT + "\n- Có quy tắc auto reply loại 全てのメッセージ đang ON",
       "1. BỎ TICK checkbox「自動応答 [すべてのメッセージに反応] のメッセージ」, lưu\n"
       "2. Friend F gửi text\n3. Query trạng thái confirm của conversation\n4. Mở màn chat 1:1",
       "Checkbox 自動応答 [すべてのメッセージに反応] = BỎ TICK",
       "- Tin nhắn KHÔNG được confirm\n- Màn chat 1:1 hiện「未確認」",
       env="PRODUCTION",
       note="Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / AI_TCs_Setting_chat_v1 r106 (BS_032)"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "チャット設定: tick / bỏ tick「自動応答 [設定したキーワードに反応] のメッセージ」⇒ áp dụng riêng cho quy tắc "
       "loại keyword chỉ định",
       RT + "\n- Có quy tắc auto reply loại キーワード chỉ định đang ON",
       "1. TICK checkbox「自動応答 [設定したキーワードに反応] のメッセージ」, lưu → F gửi keyword → query + xem chat 1:1\n"
       "2. BỎ TICK checkbox đó, lưu → F gửi keyword → query + xem chat 1:1",
       "Checkbox 自動応答 [設定したキーワードに反応]: tick và bỏ tick",
       "- Khi TICK: tin nhắn được confirm, màn chat hiện「確認済」\n"
       "- Khi BỎ TICK: tin nhắn KHÔNG được confirm, màn chat hiện「未確認」",
       env="PRODUCTION",
       note="2 checkbox riêng cho 2 loại quy tắc auto reply — điểm dễ lọt. "
            "Nguồn: 01. TCsLine_Chat1:1 (Improve 10/2024) / AI_TCs_Setting_chat_v1 r107-r108 (BS_032)"),

    tc("Runtime — 自動確認済み (confirm message)", "STATE-001", "Normal",
       "Bug #31873: action của auto reply (status chat / block / ẩn / bookmark) × 2 chế độ confirm ⇒ "
       "action thực hiện được VÀ status confirm hiển thị đúng",
       RT + "\n- Friend F có status_last_message = 1\n"
       "- Quy tắc auto reply lần lượt cấu hình 4 nhóm action: gắn/bỏ status chat, block/unblock, ẩn/bỏ ẩn, "
       "add/bỏ bookmark",
       "1. Với chế độ KHÔNG tự động confirm: F trigger từng nhóm action → query kết quả action + status confirm\n"
       "2. Với chế độ CÓ tự động confirm: lặp lại 4 nhóm action → query lại\n"
       "3. Đối chiếu màn chat 1:1 sau mỗi lần",
       "4 nhóm action × 2 chế độ confirm = 8 tổ hợp",
       "- Cả 8 tổ hợp: action được thực hiện đúng (id_status / is_blocked / is_hide / is_bookmark cập nhật)\n"
       "- Status confirm hiển thị ĐÚNG theo chế độ đã cấu hình, không bị lệch giữa DB và màn hình",
       env="PRODUCTION",
       note="Đây là root cause của Bug #31873: auto reply thực hiện action làm update conversation sai. "
            "Nguồn: TCsLine_JOB / Test fix bug KH r153-r178"),

    # ═══════════════ Runtime — friend bị block / ẩn ═══════════════
    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "BR-19: friend bị BOT block (is_blocked=1, blocked_by=1) và KHÔNG có rule cho inactive ⇒ bỏ qua message hoàn toàn",
       RT + "\n- Friend F bị bot block: conversation.is_blocked = 1, blocked_by = 1\n"
       "- Bot A CHỈ có quy tắc auto reply với 対象 =「有効友だち」(is_apply_active_friend = 1)",
       "1. F gửi text đến bot\n2. Query: SELECT is_blocked, status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "3. Query: SELECT status FROM callback_event WHERE bot_id=A ORDER BY id DESC LIMIT 1\n4. Xem màn chat 1:1",
       "F: is_blocked = 1, blocked_by = 1; bot chỉ có rule cho active friend",
       "- Bỏ qua message của F: KHÔNG update conversation\n- is_blocked vẫn = 1\n"
       "- KHÔNG update status_last_message\n- callback_event.status = 7 (STATUS_BLOCKED_BY_BOT)",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r218. Giá trị status = 7 do AI bổ sung theo spec §7 state machine"),

    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "BR-19: friend bị bot block + CÓ rule cho inactive (is_apply_active_friend=0) + user KHÔNG bị ẩn "
       "⇒ chạy auto reply, update status_last_message = 0",
       RT + "\n- Friend F: is_blocked = 1, is_hide = 0\n"
       "- Bot A CÓ quy tắc auto reply với 対象 =「ブロックした友だち」",
       "1. F gửi text trigger quy tắc\n2. Quan sát LINE app của F\n"
       "3. Query: SELECT is_blocked, is_hide, status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "4. Xem màn chat 1:1",
       "F: is_blocked = 1, is_hide = 0; rule cho ブロックした友だち",
       "- F NHẬN được action auto reply\n- DB: is_blocked = 1, is_hide = 0, status_last_message = 0 (chưa confirm)\n"
       "- Message hiển thị ở màn chat 1:1",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r221"),

    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "BR-19: friend bị bot block + BỊ ẨN (is_hide=1) + có rule inactive ⇒ được BỎ ẨN khi action chạy",
       RT + "\n- Friend F: is_blocked = 1, is_hide = 1\n- Bot A có quy tắc auto reply cho ブロックした友だち",
       "1. F gửi text trigger quy tắc\n2. Quan sát LINE app của F\n"
       "3. Query: SELECT is_blocked, is_hide, status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "4. Xem màn chat 1:1 / danh sách friend bị ẩn",
       "F: is_blocked = 1, is_hide = 1",
       "- F NHẬN được action\n- DB: is_hide chuyển từ 1 → 0 (được bỏ ẩn khi được action)\n"
       "- is_blocked vẫn = 1; status_last_message = 0\n- F xuất hiện lại ở danh sách chat",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r224. Khớp spec §Luồng inactive user bước 3 "
            "('nếu match → unhide conversation, lưu tin nhắn, update lastMessage')"),

    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "Friend đang BỊ ẨN (is_hide=1, không bị block): gửi tin đến bot ⇒ được bỏ ẩn + status chuyển chưa confirm",
       RT + "\n- Friend F: is_hide = 1, is_blocked = 0",
       "1. F gửi text đến bot\n2. Query is_hide + status_last_message của F\n3. Xem màn chat 1:1",
       "F: is_hide = 1",
       "- DB: is_hide = 0 (được bỏ ẩn)\n- status_last_message = 0 (chưa confirm)\n- F xuất hiện lại ở danh sách chat",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r215"),

    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "Old friend (đang là bạn nhưng chưa có bản ghi ở LME): gửi tin ⇒ tạo mới conversation + bot_line_user, "
       "auto reply vẫn chạy",
       RT + "\n- Friend F đang là bạn với bot A trên LINE nhưng CHƯA có bản ghi bot_line_user và conversation\n"
       "- Bot A có quy tắc auto reply dạng 全てのメッセージ",
       "1. F gửi text đến bot\n2. Quan sát LINE app của F\n"
       "3. Query: SELECT is_blocked, is_old_friend, status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "4. Query: SELECT is_blocked, is_friend, follow_at, affliater_id FROM bot_line_user WHERE line_user_id=<F>",
       "F: old friend chưa có bản ghi trong LME",
       "- Tạo conversation mới: is_blocked = 0, is_old_friend = 1, status_last_message = 0\n"
       "- Tạo bot_line_user mới: is_blocked = 0, is_friend = 1, follow_at = now(), có affliater_id\n"
       "- F NHẬN được auto reply",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r209-r210. Phần 'F nhận được auto reply' do AI bổ sung — "
            "corpus chỉ verify DB"),

    tc("Runtime — friend bị block / ẩn", "FRIEND-001", "Normal",
       "Friend unfollow bot rồi follow lại ⇒ is_blocked về 0, auto reply chạy lại bình thường",
       RT + "\n- Friend F đã unfollow bot A (is_blocked = 1, blocked_by = 0)",
       "1. F follow lại bot A trên LINE\n"
       "2. Query: SELECT is_blocked, status_last_message FROM conversation WHERE line_user_id=<F>\n"
       "3. Query: SELECT is_blocked, is_friend, follow_at FROM bot_line_user WHERE line_user_id=<F>\n"
       "4. F gửi text trigger auto reply → quan sát LINE app",
       "F: unfollow → follow lại",
       "- conversation: is_blocked = 0; status_last_message KHÔNG bị update\n"
       "- bot_line_user: is_blocked = 0, is_friend = 1, follow_at = now()\n- F NHẬN được auto reply",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r230-r231"),

    # ═══════════════ Runtime — lỗi gửi & retry ═══════════════
    tc("Runtime — lỗi gửi & retry", "MSG-005", "Normal",
       "Auto reply action send TEXT gửi thành công ⇒ hiển thị ở chat 1:1 và LINE app, KHÔNG hiện ở màn error list",
       RT + "\n- Quy tắc auto reply có action send text",
       "1. F gửi keyword trigger\n2. Quan sát LINE app của F\n3. Mở màn chat 1:1\n4. Mở màn エラーリスト (error list)",
       "Action send text, gửi thành công",
       "- F nhận được text trên LINE app\n- Màn chat 1:1 hiện message\n- Màn error list KHÔNG hiện message này",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r256"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Auto reply send text lỗi THUỘC nhóm được retry ⇒ hiện ở màn error list với text リトライ中",
       RT + "\n- Quy tắc auto reply có action send text\n- Dựng điều kiện gây lỗi gửi thuộc nhóm được retry",
       "1. F gửi keyword trigger, hệ thống gửi lỗi\n2. Mở màn error list\n3. Quan sát trạng thái của message",
       "Lỗi gửi thuộc nhóm được retry",
       "- Message lỗi hiển thị ở màn error list\n- Hiện text「リトライ中」(đang được retry)",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r257"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Auto reply send text lỗi KHÔNG thuộc nhóm retry ⇒ hiện ở error list, KHÔNG hiện リトライ中",
       RT + "\n- Dựng điều kiện gây lỗi gửi KHÔNG thuộc nhóm được retry",
       "1. F gửi keyword trigger, hệ thống gửi lỗi\n2. Mở màn error list\n3. Quan sát",
       "Lỗi gửi không thuộc nhóm retry",
       "- Message lỗi hiển thị ở màn error list\n- KHÔNG hiện text「リトライ中」\n"
       "- Cho phép thao tác: tick chọn, resend thủ công, xóa",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r258"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Normal",
       "Retry message lỗi của action autoreply: retry sau 1p / 2p / 5p THÀNH CÔNG ⇒ message chuyển sang chat 1:1 và LINE app, "
       "biến mất khỏi error list",
       RT + "\n- Message auto reply (action text hoặc template) đang lỗi và ở trạng thái リトライ中",
       "1. Chờ mốc retry 1 phút → nếu thành công: xem màn chat 1:1 + LINE app + error list\n"
       "2. Lặp lại quan sát ở mốc 2 phút và 5 phút cho các message lỗi khác",
       "3 mốc retry: 1p / 2p / 5p; 2 loại action: text và template",
       "- Message hiển thị ở màn chat 1:1: nội dung đúng, thay được tên friend và friend info, THỨ TỰ message đúng, "
       "trigger hiện「自動応答」\n"
       "- LINE user nhận đúng nội dung và đúng thứ tự\n- Message KHÔNG còn hiển thị ở màn error list",
       env="PRODUCTION",
       note="3 mốc × 2 loại action cùng 1 kết quả nên giữ chung. "
            "Nguồn: 16. TCsLine_ErrorList / improve 28/11 r259 / r261 / r263 / r268 / r270 / r272"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Retry message lỗi của action autoreply: retry 1p/2p vẫn FAIL ⇒ vẫn ở error list và tiếp tục retry (リトライ中)",
       RT + "\n- Message auto reply đang lỗi, ở trạng thái リトライ中",
       "1. Giữ nguyên điều kiện lỗi, chờ qua mốc retry 1 phút → xem error list\n2. Chờ qua mốc 2 phút → xem error list",
       "Retry lần 1 và lần 2 đều fail",
       "- Message VẪN hiển thị ở màn error list\n- VẪN hiện text「リトライ中」(còn được retry tiếp)",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r260 / r262 / r269 / r271"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Boundary",
       "Retry lần cuối (sau 5 phút) vẫn FAIL ⇒ DỪNG retry, bỏ text リトライ中, cho phép thao tác thủ công",
       RT + "\n- Message auto reply đã retry fail ở mốc 1p và 2p",
       "1. Giữ điều kiện lỗi, chờ qua mốc retry 5 phút\n2. Mở màn error list\n3. Thử tick chọn / resend / xóa message",
       "Retry lần cuối (5p) fail",
       "- Message vẫn ở màn error list nhưng KHÔNG còn được retry tiếp\n- KHÔNG hiện text「リトライ中」\n"
       "- Cho phép tick chọn, resend thủ công, xóa message",
       env="PRODUCTION",
       note="Biên cuối của chuỗi retry. Nguồn: 16. TCsLine_ErrorList / improve 28/11 r264 / r273 / r279"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Action autoreply có CẢ text và template: 1 phần gửi lỗi ⇒ error list ghi nhận đúng phần lỗi, "
       "retry 1p/2p fail → 5p thành công thì message về chat 1:1 đúng thứ tự",
       RT + "\n- Quy tắc auto reply có action gồm cả send text và send template",
       "1. F trigger, dựng điều kiện lỗi\n2. Xem error list ngay sau khi lỗi\n"
       "3. Theo dõi qua mốc retry 1p (fail), 2p (fail), 5p (success)\n4. Xem màn chat 1:1 + LINE app",
       "Action gồm text + template; retry 1p fail, 2p fail, 5p success",
       "- Ngay sau lỗi: message lỗi hiện ở error list với リトライ中\n"
       "- Sau 1p và 2p fail: vẫn ở error list, vẫn リトライ中\n"
       "- Sau 5p success: message hiện ở chat 1:1 và LINE app ĐÚNG THỨ TỰ, biến mất khỏi error list",
       env="PRODUCTION",
       note="Chuỗi thao tác liên tiếp theo thời gian nên giữ chung 1 TC. "
            "Nguồn: 16. TCsLine_ErrorList / improve 28/11 r274-r279"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Action callback (autoreply) chứa TEMPLATE RỖNG ⇒ send lỗi, hiện ở màn error-list với mã lỗi 006",
       "- Bot FREE plan\n- Quy tắc auto reply có action gửi template group RỖNG (không có template con)",
       "1. F gửi keyword trigger\n2. Quan sát LINE app của F\n3. Mở màn error list, đọc mã lỗi",
       "Template group rỗng; bot plan FREE",
       "- Send lỗi\n- Màn error-list hiện message lỗi với mã lỗi 006\n- F KHÔNG nhận được message",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r430. Corpus r266 ghi thêm『Bug Tester #33772: "
            "[Action autoreply] Message send lỗi nhưng vẫn hiển thị ở màn chat 1:1 ⇒ Lỗi từ trước do trong action "
            "có 1 template group rỗng』⇒ điểm ĐÃ TỪNG LỖI"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Normal",
       "Action callback (autoreply): gửi template group có template con / template đơn / action text ⇒ send success, "
       "không hiện ở error-list",
       "- Bot FREE plan\n- Quy tắc auto reply có 3 cấu hình action lần lượt: template group có con / template đơn / action text",
       "1. Với từng cấu hình: F gửi keyword trigger\n2. Quan sát LINE app + màn chat 1:1 + màn error-list",
       "3 cấu hình action; bot plan FREE",
       "- Cả 3: send success cho user, hiển thị ở màn chat 1:1 và phía LINE\n"
       "- KHÔNG hiện message ở màn error-list",
       env="PRODUCTION",
       note="3 cấu hình cùng 1 kết quả nên giữ chung. Nguồn: 16. TCsLine_ErrorList / improve 28/11 r431-r433"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Boundary",
       "Action callback (autoreply) KHÔNG chứa action text/template (VD chỉ gắn tag) ⇒ action vẫn chạy, "
       "KHÔNG gửi message nào, chat 1:1 và error-list không phát sinh dòng mới",
       "- Bot FREE plan\n- Quy tắc auto reply chỉ có action gắn tag (không có text/template)",
       "1. Đếm số message hiện có ở màn chat 1:1 của F\n2. F gửi keyword trigger\n"
       "3. Query tag_line_user của F\n4. Đếm lại message ở chat 1:1 + kiểm tra error-list",
       "Action chỉ gắn tag; bot plan FREE",
       "- Tag được gắn cho F (tag_line_user có bản ghi mới)\n- KHÔNG gửi message nào đến LINE user\n"
       "- Màn chat 1:1 chỉ tăng thêm message của friend, KHÔNG có message trả về\n- Error-list không phát sinh dòng mới",
       env="PRODUCTION",
       note="Nguồn: 16. TCsLine_ErrorList / improve 28/11 r434"),

    tc("Runtime — lỗi gửi & retry", "MSG-005", "Abnormal",
       "Spec Error Handling: 1 ActionDetail lỗi ⇒ chỉ action đó bị skip, các action còn lại VẪN chạy",
       RT + "\n- Quy tắc auto reply có 3 action: gắn tag T1 → gửi template RỖNG (gây lỗi) → gắn tag T2",
       "1. F gửi keyword trigger\n2. Query tag_line_user của F (kiểm tra T1 và T2)\n"
       "3. Quan sát LINE app của F\n4. Mở màn error list",
       "3 action, action giữa bị lỗi",
       "- T1 VÀ T2 đều được gắn cho F (action sau lỗi vẫn chạy)\n"
       "- Message template lỗi hiện ở error list\n- F không nhận được template lỗi nhưng vẫn được gắn tag",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="feature-spec §7 Error Handling: 'Exception trong doAction (mỗi ActionDetail) → try-catch → log + "
            "Chatwork notification → tiếp tục action tiếp'. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết theo spec, "
            "CẦN LEADER XÁC NHẬN"),
]
