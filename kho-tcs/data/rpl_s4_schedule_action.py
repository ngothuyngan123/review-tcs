# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 4: スケジュール設定, số lần chạy, copy quy tắc, modal アクション設定 (SC-004)."""
from _common import tc

FORM = ("- Đăng nhập admin, bot A\n- Màn /basic/reply/new (form tạo quy tắc auto reply)\n"
        "- Quy tắc dùng 利用設定 =「全てのメッセージに反応」cho gọn")
FR = "\n- 1 friend LINE đã kết bạn với bot A"
ACT = ("- Đăng nhập admin, bot A\n- Màn /basic/reply/new, đã mở modal「アクション設定」(SC-004)"
       "\n- Bot A có sẵn dữ liệu gốc của loại action đang test (folder default + folder tự tạo)")

S4 = [
    # ═══════════════ Form — スケジュール設定 ═══════════════
    tc("Form — スケジュール設定", "FUNC-001", "Normal",
       "反応設定 =「常に（24時間/365日）反応する」⇒ time_reaction_type = 0, day_of_week/start_time/end_time = NULL",
       FORM,
       "1. Ở Phần 4 chọn「常に（24時間/365日）反応する」\n2. Lưu\n"
       "3. Query: SELECT time_reaction_type, day_of_week, start_time, end_time FROM auto_reply WHERE id=<rule>\n"
       "4. Xem cột「スケジュール」ở màn list",
       "反応設定 = 常に",
       "- DB: time_reaction_type = 0, day_of_week = NULL, start_time = NULL, end_time = NULL\n"
       "- Màn list cột「スケジュール」hiện「常に」\n- Form ẩn khối 曜日設定 và 時間帯設定",
       note="Nguồn: TCsLine_BackUp / Backup (job) r5 (start_time = end_time = day_of_week = NULL). "
            "Tầng form do AI viết bổ sung theo spec field #10-#13"),

    tc("Form — スケジュール設定", "FUNC-001", "Normal",
       "反応設定 =「反応する曜日・時間を設定する」⇒ hiện 曜日設定 + 時間帯設定; lưu đúng định dạng day_of_week phân cách ';'",
       FORM,
       "1. Chọn「反応する曜日・時間を設定する」\n2. Tick 月火水木金 (5 ngày)\n3. Đặt 時間帯 09:00 ~ 18:00\n4. Lưu\n"
       "5. Query: SELECT time_reaction_type, day_of_week, start_time, end_time FROM auto_reply WHERE id=<rule>\n"
       "6. Xem cột「スケジュール」ở màn list",
       "曜日 = 月火水木金; 時間帯 = 09:00 ~ 18:00",
       "- DB: time_reaction_type = 1, day_of_week =「1;2;3;4;5」, start_time = 09:00, end_time = 18:00\n"
       "- Màn list cột「スケジュール」hiện「月,火,水,木,金 09:00~18:00」",
       note="BR-06: 1=月 → 7=日, phân cách ';'. Nguồn: Backup (job) r6 + feature-spec §4 field #11-#13. "
            "Corpus KHÔNG có TC kiểm tra định dạng day_of_week ⇒ TC lấp GAP do AI viết"),

    tc("Form — スケジュール設定", "FUNC-001", "Boundary",
       "曜日設定: dùng nút「全選択」⇒ tick đủ 7 ngày, day_of_week =「1;2;3;4;5;6;7」",
       FORM,
       "1. Chọn「反応する曜日・時間を設定する」\n2. Click「全選択」\n3. Đặt 時間帯 00:00 ~ 23:59, lưu\n"
       "4. Query day_of_week",
       "全選択 (7 ngày)",
       "- 7 checkbox 月火水木金土日 đều được tick\n- DB: day_of_week =「1;2;3;4;5;6;7」",
       spec="Spec không ghi",
       note="Nút「全選択」có trong ui-spec.md §Phần 4. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết"),

    tc("Form — スケジュール設定", "UI-INPUT-001", "Abnormal",
       "BR-10: giờ bắt đầu ≥ giờ kết thúc ⇒ báo lỗi 時間帯を正しく指定して下さい。, không lưu",
       FORM,
       "1. Chọn「反応する曜日・時間を設定する」, tick 月\n2. Đặt 時間帯 = 18:00 ~ 09:00 (bắt đầu > kết thúc)\n"
       "3. Click「登録」\n4. Đổi thành 09:00 ~ 09:00 (bằng nhau), click「登録」\n"
       "5. Query auto_reply mới nhất của bot A",
       "Lần 1: 18:00 ~ 09:00; lần 2: 09:00 ~ 09:00",
       "- Cả 2 lần đều báo lỗi「時間帯を正しく指定して下さい。」\n- KHÔNG tạo bản ghi auto_reply",
       note="BR-10 (end > start). 2 input cùng 1 kết quả nên giữ chung. Corpus KHÔNG có TC validate giờ ⇒ "
            "TC lấp GAP do AI viết theo spec"),

    tc("Form — スケジュール設定", "UI-INPUT-001", "Abnormal",
       "Chọn 反応する曜日・時間 nhưng KHÔNG tick ngày nào ⇒ hành vi khác nhau giữa flow legacy và flow V2",
       FORM,
       "1. Chọn「反応する曜日・時間を設定する」\n2. KHÔNG tick ngày nào\n3. Đặt 時間帯 09:00 ~ 18:00\n"
       "4. Click「登録」\n5. Query: SELECT day_of_week FROM auto_reply WHERE id=<rule mới nhất>",
       "0 ngày được tick; 時間帯 09:00 ~ 18:00",
       "- Ghi lại hành vi THẬT: có báo lỗi「曜日は最低1つを選択して下さい。」hay lưu thành công với day_of_week rỗng/NULL?\n"
       "- Nếu lưu thành công: friend gửi tin trong khung giờ 09:00~18:00 có nhận action không?",
       spec="Đã hỏi leader",
       note="⚠️ SPEC TỰ MÂU THUẪN: Validation Flow LEGACY (logic-spec.md:596) có rule「曜日は最低1つを選択して下さい。」"
            "nhưng Validation Flow V2 (logic-spec.md:607-612) KHÔNG có rule này. Flow V2 là flow đang dùng ⇒ MT-12. "
            "Corpus KHÔNG có TC. CẦN LEADER QUYẾT hành vi đúng"),

    tc("Form — スケジュール設定", "FUNC-DATE-001", "Boundary",
       "Runtime: quy tắc có lịch trình ⇒ friend gửi tin TRONG khung giờ nhận action, NGOÀI khung giờ không nhận",
       FORM + FR + "\n- Quy tắc lịch trình: 月火水木金, 09:00 ~ 18:00, action gửi text",
       "1. Đặt thời gian test vào ngày thứ 2, lúc 10:00 → friend gửi tin → quan sát LINE app\n"
       "2. Vẫn ngày thứ 2, lúc 08:59 → friend gửi tin → quan sát\n"
       "3. Vẫn ngày thứ 2, lúc 18:01 → friend gửi tin → quan sát\n"
       "4. Ngày Chủ nhật (ngoài 曜日 đã chọn), lúc 10:00 → friend gửi tin → quan sát",
       "曜日 = 月〜金; 時間帯 09:00~18:00. 4 mốc: T2 10:00 / T2 08:59 / T2 18:01 / CN 10:00",
       "- T2 10:00 (trong lịch): NHẬN được action\n- T2 08:59 (trước giờ): KHÔNG nhận\n"
       "- T2 18:01 (sau giờ): KHÔNG nhận\n- CN 10:00 (ngoài ngày): KHÔNG nhận",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Ma trận 4 mốc, kết quả từng mốc ghi rõ. RULE-08 (job) + RULE-06 (output LINE). "
            "Corpus KHÔNG có TC runtime cho lịch trình ⇒ TC lấp GAP do AI viết theo spec §7 (bước ④ kiểm tra time match)"),

    # ═══════════════ Form — số lần chạy & lưu quy tắc ═══════════════
    tc("Form — số lần chạy & lưu quy tắc", "UI-FIELD-001", "Normal",
       "Phần 5: radio「何度でもアクション稼働」(mặc định) ⇒ response_number = 1",
       FORM,
       "1. Mở form tạo mới, quan sát radio mặc định ở Phần 5\n2. Cấu hình action, lưu\n"
       "3. Query: SELECT response_number FROM auto_reply WHERE id=<rule>",
       "Giữ nguyên mặc định",
       "- Radio「何度でもアクション稼働」được chọn sẵn khi mở form\n- DB: response_number = 1",
       note="ui-spec.md §Phần 5 ghi「何度でもアクション稼働」checked trong snapshot. "
            "Corpus không test tầng form ⇒ TC lấp GAP do AI viết"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-001", "Normal",
       "BR-16 runtime:「何度でもアクション稼働」(response_number=1) ⇒ friend gửi keyword NHIỀU LẦN đều nhận action mỗi lần",
       FORM + FR + "\n- Quy tắc keyword「テスト」, chọn「何度でもアクション稼働」, action gửi text「OK」",
       "1. Friend gửi「テスト」lần 1 → quan sát LINE app\n2. Gửi lần 2 → quan sát\n3. Gửi lần 3 → quan sát\n"
       "4. Query: SELECT COUNT(*) FROM auto_reply_history WHERE reply_id=<rule> AND line_id=<friend>",
       "Gửi keyword「テスト」3 lần",
       "- Cả 3 lần friend đều nhận được「OK」\n- auto_reply_history có ≥1 bản ghi cho cặp (line_id, reply_id)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-16. Corpus CHỈ có TC ở tầng backup dữ liệu (Backup (job) r9 'setting action 1 lần/nhiều lần'), "
            "KHÔNG có TC runtime ⇒ MT-04, TC lấp GAP do AI viết theo spec"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-001", "Normal",
       "BR-16 runtime:「1度のみアクション稼働」(response_number=0) ⇒ friend chỉ nhận action LẦN ĐẦU, các lần sau bị skip",
       FORM + FR + "\n- Quy tắc keyword「テスト2」, chọn「1度のみアクション稼働」, action gửi text「OK」\n"
       "- Friend F chưa từng trigger quy tắc này (auto_reply_history rỗng)",
       "1. Friend gửi「テスト2」lần 1 → quan sát LINE app\n"
       "2. Query auto_reply_history WHERE reply_id=<rule> AND line_id=<F>\n"
       "3. Friend gửi「テスト2」lần 2 → quan sát\n4. Friend gửi lần 3 → quan sát",
       "Gửi keyword「テスト2」3 lần bởi cùng 1 friend",
       "- Lần 1: friend NHẬN được「OK」; auto_reply_history có 1 bản ghi (line_id, reply_id)\n"
       "- Lần 2 và 3: friend KHÔNG nhận được gì; auto_reply_history KHÔNG thêm bản ghi mới",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-16 (only_once). ĐÂY LÀ FIELD CHÍNH CỦA FORM nhưng corpus KHÔNG có TC runtime ⇒ MT-04. "
            "TC do AI viết theo spec, CẦN LEADER XÁC NHẬN"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-001", "Boundary",
       "BR-16:「1度のみ」— friend KHÁC chưa từng trigger vẫn nhận được action (history theo cặp line_id + reply_id)",
       FORM + "\n- Quy tắc「1度のみ」keyword「テスト2」\n- Friend F1 đã trigger 1 lần; friend F2 chưa từng trigger",
       "1. F2 gửi「テスト2」→ quan sát LINE app của F2\n"
       "2. Query auto_reply_history WHERE reply_id=<rule>",
       "F1 đã có history; F2 chưa có",
       "- F2 NHẬN được action (history tính theo từng line_id)\n- auto_reply_history có 2 bản ghi: (F1, rule) và (F2, rule)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Gắn MT-04. TC do AI viết theo BR-16"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-001", "Abnormal",
       "BR-08: sửa quy tắc đang TẮT (OFF) qua flow V2 ⇒ is_stopped bị RESET về 0 (tự động bật lại)",
       FORM + "\n- Quy tắc R đang OFF (is_stopped = 1)",
       "1. Xác nhận trên màn list: quy tắc R hiện OFF\n2. Mở edit R, sửa 1 field bất kỳ (VD đổi folder)\n"
       "3. Click「登録」\n4. Quay lại màn list quan sát cột「稼働状況」\n"
       "5. Query: SELECT is_stopped FROM auto_reply WHERE id=<R>",
       "Quy tắc R: is_stopped = 1 trước khi sửa",
       "- Ghi lại hành vi THẬT: sau khi lưu, quy tắc R hiện ON hay vẫn OFF?\n"
       "- Query DB xác nhận giá trị is_stopped",
       spec="Đã hỏi leader",
       note="⚠️ BR-08 (logic-spec.md dòng ReplyController.php:1020,1034): 'Khi lưu qua flow V2, is_stopped LUÔN reset "
            "về 0'. Nghĩa là admin tắt quy tắc rồi vào sửa ⇒ quy tắc TỰ BẬT LẠI, có thể gửi tin ngoài ý muốn. "
            "Corpus KHÔNG có TC nào cho hành vi này ⇒ MT-13. CẦN LEADER QUYẾT: cố ý hay là bug"),

    tc("Form — số lần chạy & lưu quy tắc", "SEC-ISO-001", "Abnormal",
       "BR-09: đổi bot ở tab khác giữa chừng rồi lưu quy tắc ⇒ báo 別のアカウントに切り替えたので、要求を処理できません。",
       FORM + "\n- Mở 2 tab: tab 1 là form tạo quy tắc của bot A, tab 2 dùng để đổi bot",
       "1. Tab 1: mở form tạo quy tắc bot A, điền dữ liệu (chưa lưu)\n2. Tab 2: đổi sang bot B\n"
       "3. Quay lại tab 1, click「登録」\n4. Query auto_reply của cả bot A và bot B",
       "botIdCurrent (request) = bot A; getBotId() (session) = bot B",
       "- Báo lỗi「別のアカウントに切り替えたので、要求を処理できません。」\n"
       "- KHÔNG tạo quy tắc ở bot A lẫn bot B",
       spec="Spec không ghi",
       note="BR-09 (ReplyController.php:935-938). Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết theo spec"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-DEP-001", "Abnormal",
       "BR-02 backup lock: bot đang backup ⇒ chặn tạo/sửa/xóa quy tắc auto reply (HTTP 500 + MESSAGE_NOTIFY_BACKUP)",
       "- Bot A đang có BackupHistory ở trạng thái 0 hoặc 1 (đang backup)\n- Mở màn /basic/reply của bot A",
       "1. Thử tạo quy tắc mới → click「登録」\n2. Thử sửa 1 quy tắc → click「登録」\n"
       "3. Thử xóa 1 quy tắc\n4. Thử xóa 1 folder\n5. Quan sát response và DB sau mỗi thao tác",
       "BackupHistory.status ∈ {0, 1}",
       "- Cả 4 thao tác đều bị chặn: HTTP 500 + hiển thị thông báo backup (MESSAGE_NOTIFY_BACKUP)\n"
       "- KHÔNG có bản ghi auto_reply / category nào bị thay đổi",
       spec="Spec không ghi",
       note="BR-02. 4 thao tác cùng 1 cơ chế chặn nên giữ chung. Corpus (TCsLine_BackUp) chỉ test dữ liệu SAU backup, "
            "KHÔNG test chặn thao tác TRONG khi backup ⇒ MT-14, TC lấp GAP do AI viết"),

    tc("Form — số lần chạy & lưu quy tắc", "SEC-ISO-001", "Abnormal",
       "Bug Tester #33107: bot A truy cập trực tiếp URL màn tạo/edit/copy quy tắc của bot B ⇒ bị chặn",
       "- Đang đăng nhập và chọn bot A\n- Biết group_id (folder) và reply_id của bot B",
       "1. Nhập URL /basic/reply/new?group_id=<folder của bot B> → quan sát\n"
       "2. Nhập URL /basic/reply/new?group_id=0&reply_id=<quy tắc của bot B> → quan sát\n"
       "3. Nhập URL /basic/reply/new?group_id=0&copy_id=<quy tắc của bot B> → quan sát",
       "3 URL của bot B: group_id=6754, reply_id=18888, copy_id=18888",
       "- Cả 3 URL: bot A KHÔNG xem/sửa/copy được dữ liệu của bot B\n"
       "- Ghi lại hành vi thật: redirect về đâu / báo lỗi gì / form trống",
       spec="Spec không ghi",
       note="Nguồn: Improve chung / Improve nhỏ r335-r337 (Bug Tester #33107) — corpus KHÔNG ghi kết quả mong đợi "
            "cụ thể (chỉ liệt kê URL). AI tự viết kết quả đo lường được; spec Authorization chỉ ghi getBotId() filter, "
            "KHÔNG mô tả hành vi khi truy cập URL bot khác ⇒ MT-19. CẦN LEADER XÁC NHẬN hành vi mong đợi"),

    tc("Form — số lần chạy & lưu quy tắc", "UI-FIELD-001", "Normal",
       "Phần 2「フォルダ」: dropdown chọn folder khi TẠO MỚI ⇒ auto_reply.category_id = id folder đã chọn",
       FORM + "\n- Bot A có ≥2 folder auto reply",
       "1. Mở /basic/reply/new (không truyền group_id)\n2. Quan sát giá trị mặc định của dropdown「フォルダ」\n"
       "3. Chọn folder A trong dropdown\n4. Lưu\n"
       "5. Query: SELECT category_id FROM auto_reply WHERE id=<rule>\n6. Mở màn list, chọn folder A",
       "Dropdown「フォルダ」chọn folder A",
       "- Giá trị mặc định của dropdown là「未分類」\n- Sau lưu: auto_reply.category_id = id folder A\n"
       "- Quy tắc hiện trong folder A ở màn list, không hiện ở「未分類」",
       note="Field #4 Traceability (category_id, `0` = 未分類 theo BR-14). "
            "Corpus KHÔNG có TC dropdown folder trên form ⇒ TC lấp GAP do AI viết"),

    tc("Form — số lần chạy & lưu quy tắc", "UI-FIELD-001", "Normal",
       "Phần 2「フォルダ」: ĐỔI folder khi SỬA quy tắc ⇒ quy tắc chuyển sang folder mới, số đếm 2 folder đổi đúng",
       FORM + "\n- Quy tắc R đang ở folder A; folder B tồn tại",
       "1. Ghi lại số đếm của folder A và B ở sidebar\n2. Mở edit R, đổi dropdown「フォルダ」sang folder B\n"
       "3. Lưu\n4. Đọc lại số đếm 2 folder\n5. Query category_id của R\n6. Mở folder B kiểm tra R có ở đó không",
       "Đổi folder A → folder B",
       "- auto_reply.category_id = id folder B\n- Sidebar: folder A giảm 1, folder B tăng 1\n"
       "- R hiện trong folder B, không còn ở folder A",
       note="Nhánh EDIT của field #4 — dễ lọt. TC lấp GAP do AI viết"),

    tc("Form — số lần chạy & lưu quy tắc", "UI-FIELD-001", "Boundary",
       "Phần 2「フォルダ」: chọn「未分類」⇒ auto_reply.category_id = 0 (convention, không có record trong bảng category)",
       FORM,
       "1. Mở form tạo mới, chọn dropdown「フォルダ」=「未分類」\n2. Lưu\n"
       "3. Query: SELECT category_id FROM auto_reply WHERE id=<rule>\n"
       "4. Query: SELECT * FROM category WHERE id=0 — xác nhận không tồn tại record\n"
       "5. Mở màn list, chọn「未分類」",
       "Dropdown =「未分類」",
       "- auto_reply.category_id = 0\n- Bảng category KHÔNG có record id=0 (未分類 là convention)\n"
       "- Quy tắc hiện trong nhóm「未分類」ở màn list",
       note="BR-14 Default folder 未分類. Biên quan trọng vì code xử lý items_default riêng. "
            "TC lấp GAP do AI viết"),

    tc("Form — số lần chạy & lưu quy tắc", "STATE-001", "Abnormal",
       "Footer「戻る」: điền dữ liệu rồi bấm 戻る ⇒ quay lại danh sách, KHÔNG lưu quy tắc",
       FORM,
       "1. Mở form tạo mới, điền đủ keyword + lịch trình + action\n2. Click「戻る」\n"
       "3. Quan sát trang đích\n4. Query: SELECT COUNT(*) FROM auto_reply WHERE bot_id=A AND is_deleted=0 "
       "— so với trước khi mở form",
       "Form đã điền đủ dữ liệu nhưng không lưu",
       "- Quay về /basic/reply (màn danh sách)\n- COUNT auto_reply KHÔNG tăng\n"
       "- Không có bản ghi keyword / t_actions mới",
       spec="Spec không ghi",
       note="ui-spec.md §Footer actions:「戻る」quay lại danh sách. Spec KHÔNG nói có dialog cảnh báo mất dữ liệu "
            "hay không. Corpus KHÔNG có TC ⇒ TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN có cần cảnh báo không"),

    # ═══════════════ Copy quy tắc ═══════════════
    tc("Copy quy tắc", "FUNC-001", "Normal",
       "BR-11: copy quy tắc ⇒ deep clone t_actions → t_actions_detail → filters_v2; KHÔNG clone keyword",
       "- Đang ở màn /basic/reply của bot A\n- Quy tắc R có: 3 keyword, 2 điều kiện filter (has_filters=1), 2 action",
       "1. Thực hiện thao tác copy quy tắc R (URL /basic/reply/new?copy_id=<R>)\n"
       "2. Quan sát form: ô keyword, ô 対象条件, khối アクション設定\n3. Bổ sung keyword mới, lưu\n"
       "4. Query: t_actions / t_actions_detail / filters_v2 của quy tắc mới so với R\n"
       "5. Query bảng keyword của quy tắc mới",
       "Quy tắc R: 3 keyword, 2 filter, 2 action",
       "- Form copy: ô keyword TRỐNG (không clone keyword)\n"
       "- Khối アクション設定 hiện đủ 2 action đã clone; 対象条件 hiện 2 điều kiện đã clone\n"
       "- DB: t_actions / t_actions_detail / filters_v2 của quy tắc mới có id KHÁC R (bản sao độc lập)\n"
       "- Bảng keyword của quy tắc mới chỉ có keyword vừa nhập tay",
       spec="Spec không ghi",
       note="BR-11 + TB-02. ⚠️ ui-spec.md KHÔNG mô tả nút copy trên UI (Gap TB-02) nhưng corpus có 8 TC "
            "「Check copy」đã chạy OK trên staging ⇒ đề xuất ĐÓNG Gap TB-02. Corpus KHÔNG kiểm tra 'keyword không "
            "được clone' ⇒ phần đó do AI bổ sung theo BR-11. Gắn MT-20"),

    tc("Copy quy tắc", "FUNC-001", "Normal",
       "Copy quy tắc rồi KHÔNG sửa action đã copy ⇒ lưu thành công, action bản sao hoạt động độc lập với bản gốc",
       "- Quy tắc R có action gửi template T1\n- Đang ở màn /basic/reply",
       "1. Copy quy tắc R\n2. Nhập keyword mới, KHÔNG mở modal action\n3. Lưu\n"
       "4. Sửa action của quy tắc R GỐC (đổi sang template T2)\n"
       "5. Mở lại quy tắc copy, kiểm tra action\n6. Friend gửi keyword của bản copy → quan sát",
       "R: action gửi T1. Sau đó R đổi thành T2",
       "- Quy tắc copy vẫn giữ action gửi T1 (không bị ảnh hưởng bởi thay đổi ở R)\n"
       "- Friend nhận được template T1",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r59 / r63 / r66 / r69 (Check copy — 'không edit action đã copy'). "
            "Phần verify độc lập với bản gốc do AI bổ sung theo BR-11 deep clone"),

    tc("Copy quy tắc", "FUNC-001", "Normal",
       "Copy quy tắc rồi CÓ sửa action đã copy ⇒ chỉ bản copy đổi, quy tắc gốc giữ nguyên action",
       "- Quy tắc R có action gửi template T1",
       "1. Copy quy tắc R\n2. Mở modal action, đổi sang template T2\n3. Nhập keyword mới, lưu\n"
       "4. Mở lại quy tắc R gốc, kiểm tra action\n5. Query t_actions_detail của cả 2 quy tắc",
       "Bản copy đổi action từ T1 → T2",
       "- Quy tắc copy: action gửi T2\n- Quy tắc R gốc: VẪN gửi T1\n"
       "- DB: 2 bản ghi t_actions_detail độc lập, id khác nhau",
       note="Nguồn: Ver1.0 r59 / r63 / r66 / r69 (Check copy — 'Có edit action đã copy')"),

    tc("Copy quy tắc", "FUNC-001", "Abnormal",
       "Copy quy tắc nhưng KHÔNG nhập keyword rồi lưu ⇒ báo キーワードを1つ以上設定して下さい。",
       "- Quy tắc R dạng keyword",
       "1. Copy quy tắc R (ô keyword trống do không clone)\n2. Giữ 利用設定 =「設定したキーワードに反応」\n"
       "3. Click「登録」ngay\n4. Query auto_reply mới nhất",
       "Ô keyword: trống sau khi copy",
       "- Báo lỗi「キーワードを1つ以上設定して下さい。」\n- KHÔNG tạo quy tắc mới",
       spec="Spec không ghi",
       note="Hệ quả trực tiếp của BR-11 (không clone keyword) + Validation V2. TC do AI viết ghép 2 rule, "
            "CẦN LEADER XÁC NHẬN"),

    # ═══════════════ Action — 友だち情報 ═══════════════
    tc("Action — 友だち情報", "REG-SHARED-001", "Normal",
       "Bug KH #35729: tạo mới action 友だち情報 ở folder TỰ TẠO (4 type text/select/date/point) "
       "⇒ t_actions_detail.data lưu \"group_open\": <id group>",
       ACT + "\n- Có folder friend info tự tạo chứa 4 info type: text, select, date, point",
       "1. Mở modal action, chọn「友だち情報」\n2. Chọn lần lượt 4 info của folder tự tạo (text / select / date / point)\n"
       "3. Lưu action, lưu quy tắc\n"
       "4. Query: SELECT data FROM t_actions_detail WHERE type='friend_info' AND ... — đọc key group_open\n"
       "5. Friend trigger auto reply → quan sát giá trị friend info được ghi",
       "4 type friend info trong folder tự tạo",
       "- Tạo mới action thành công (không lỗi)\n"
       "- DB: t_actions_detail.data chứa \"group_open\": <id của group friend info>\n"
       "- Friend trigger auto reply → giá trị friend info được ghi đúng",
       env="PRODUCTION",
       note="4 type cùng 1 kết quả nên giữ chung. Verify 3 tầng: modal + DB + output (RULE-07). "
            "Nguồn: Ver1.0 r57 + r67 + r101"),

    tc("Action — 友だち情報", "REG-SHARED-001", "Normal",
       "Bug KH #35729: EDIT action 友だち情報 (thêm/sửa/xóa) ⇒ lưu \"group_open\": 0 và action vẫn chạy đúng",
       ACT + "\n- Quy tắc đã có action 友だち情報",
       "1. Mở edit quy tắc → mở modal action\n2. Thêm 1 friend info, sửa 1 friend info, xóa 1 friend info\n"
       "3. Lưu\n4. Query t_actions_detail.data — đọc key group_open\n5. Friend trigger auto reply → quan sát",
       "3 thao tác edit trên action friend info",
       "- Edit thành công, KHÔNG hiển thị lỗi「Undefined property: stdClass::$group_open」\n"
       "- DB: t_actions_detail.data chứa \"group_open\": 0\n- Friend trigger auto reply → action chạy bình thường",
       env="PRODUCTION",
       note="⚠️ MÂU THUẪN NỘI BỘ: Ver1.0 r58 (khối Bug #35729, 04/2026) nói EDIT lưu group_open = 0, "
            "nhưng Ver1.0 r98-r101 (khối Task #35989 recover, cũng 04/2026) nói folder default → 0, "
            "folder mặc định hệ thống → -1, folder địa chỉ → -2, folder tự tạo → group_id ⇒ MT-21. "
            "Nguồn: Ver1.0 r58 / r62 / r65 / r68"),

    tc("Action — 友だち情報", "REG-SHARED-001", "Abnormal",
       "Bug KH #35729 (tái hiện): action friend info DỮ LIỆU CŨ không có key \"group_open\" ⇒ mở modal edit "
       "KHÔNG hiển thị lỗi Undefined property",
       ACT + "\n- Quy tắc có action 友だち情報 kiểu dữ liệu CŨ: đã xóa key \"group_open\" khỏi t_actions_detail.data bằng DB",
       "1. Xóa key \"group_open\" trong t_actions_detail.data của action friend info (tái hiện data cũ)\n"
       "2. Mở màn edit quy tắc\n3. Click vào「アクション設定」mở modal\n4. Quan sát modal",
       "t_actions_detail.data KHÔNG có key \"group_open\"",
       "- Modal action mở bình thường\n- KHÔNG hiển thị lỗi「Undefined property: stdClass::$group_open」\n"
       "- Action friend info hiển thị được (code set group_open = 0 khi thiếu)",
       note="Đây là TC tái hiện bug gốc. Nguồn: Ver1.0 r55-r56 (Bug KH #35729 [09-04-2026][27659]). "
            "Cách fix: kiểm tra group id có tồn tại không, nếu không set = 0"),

    tc("Action — 友だち情報", "DATA-REF-001", "Normal",
       "Đã setting action friend info → XÓA friend info gốc ⇒ action chứa friend info đó bị xóa khỏi quy tắc, "
       "mở modal action khác vẫn thành công",
       ACT + "\n- Quy tắc có action friend info FI1 và action friend info FI2",
       "1. Sang màn 友だち情報管理, xóa FI1\n2. Quay lại mở edit quy tắc auto reply\n"
       "3. Mở modal「アクション設定」\n4. Query: SELECT * FROM t_actions_detail WHERE id=<action chứa FI1>",
       "Xóa friend info FI1 đang được action tham chiếu",
       "- Action chứa FI1 bị xóa khỏi quy tắc auto reply\n- Mở modal setting action khác vẫn thành công (không lỗi)\n"
       "- DB: bảng t_actions_detail bị xóa bản ghi có action id đã bị xóa",
       note="Nguồn: Ver1.0 r60 + r70"),

    tc("Action — 友だち情報", "REG-SHARED-001", "Normal",
       "Task #35989 recover: action friend info ở folder DEFAULT ⇒ group_open = 0",
       ACT + "\n- Có friend info ở folder default (folder chưa phân loại)",
       "1. Tạo/edit action friend info chọn info thuộc folder default (4 type: text/select/date/point)\n2. Lưu\n"
       "3. Query t_actions_detail.data — đọc group_open\n4. Friend trigger auto reply → quan sát",
       "4 type friend info trong folder default",
       "- Tạo/edit action thành công\n- DB: t_actions_detail.data chứa \"group_open\" = 0\n"
       "- Friend trigger auto reply → nhận đúng action",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r98 (Task #35989, 04/2026). Gắn MT-21"),

    tc("Action — 友だち情報", "REG-SHARED-001", "Normal",
       "Task #35989 recover: action friend info ở folder MẶC ĐỊNH HỆ THỐNG (tên/SDT/email/ngày sinh) ⇒ group_open = -1",
       ACT,
       "1. Tạo/edit action friend info chọn lần lượt: Tên hệ thống / SDT / Email / Ngày sinh\n2. Lưu\n"
       "3. Query t_actions_detail.data — đọc group_open\n4. Friend trigger auto reply → quan sát",
       "4 info hệ thống: Tên / SDT / Email / Ngày sinh",
       "- Tạo/edit action thành công\n- DB: t_actions_detail.data chứa \"group_open\" = -1\n"
       "- Friend trigger auto reply → nhận đúng action",
       env="PRODUCTION",
       note="Giá trị âm -1 là quy ước riêng, KHÔNG có trong db-mapping.md ⇒ MT-21. Nguồn: Ver1.0 r61 + r99"),

    tc("Action — 友だち情報", "REG-SHARED-001", "Normal",
       "Task #35989 recover: action friend info ở folder ĐỊA CHỈ (info_id -6 → -10) ⇒ group_open = -2",
       ACT + "\n- Bot có folder thông tin địa chỉ 5 trường (Feature #29832)",
       "1. Tạo/edit action friend info chọn lần lượt 5 info địa chỉ: info_id -6, -7, -8, -9, -10\n2. Lưu\n"
       "3. Query t_actions_detail.data — đọc group_open\n4. Friend trigger auto reply → quan sát",
       "5 info địa chỉ: info_id -6 / -7 / -8 / -9 / -10",
       "- Tạo/edit action thành công cho cả 5 info\n- DB: t_actions_detail.data chứa \"group_open\" = -2\n"
       "- Friend trigger auto reply → nhận đúng action",
       env="PRODUCTION",
       note="5 info cùng 1 kết quả nên giữ chung. Giá trị -2 KHÔNG có trong db-mapping.md ⇒ MT-21. "
            "Nguồn: Ver1.0 r64 + r100"),

    tc("Action — 友だち情報", "DATA-MIG-001", "Normal",
       "Task #35989: chạy lệnh recover trên tài khoản KH ⇒ modal multi action mở bình thường sau recover",
       "- Account KH có action friend info / template / scenario / richmenu / remind kiểu dữ liệu CŨ "
       "(thiếu group_open hoặc selected_group_id)\n- Dev đã log ra danh sách bản ghi lỗi",
       "1. Trước recover: query DB xem data bản ghi lỗi (thiếu group_open / selected_group_id)\n"
       "2. Truy cập account KH trên web, mở màn setting action đó → quan sát modal\n"
       "3. Dev chạy lệnh recover\n4. Vào lại màn setting action đó → quan sát modal\n"
       "5. Query lại DB xác nhận key đã được set",
       "Bản ghi t_actions_detail.data thiếu group_open / selected_group_id",
       "- Trước recover: modal multi action hiển thị bình thường (do fix #35729 đã set mặc định 0)\n"
       "- Sau recover: modal multi action vẫn hiển thị bình thường\n"
       "- DB: key group_open / selected_group_id đã được set đúng theo id group/category của từng type",
       env="PRODUCTION",
       note="RULE-08: lệnh recover chạy trên production account KH. Nguồn: Ver1.0 r97 + r106 (Task #35989)"),

    # ═══════════════ Action — テンプレート & ステップ ═══════════════
    tc("Action — テンプレート & ステップ", "REG-SHARED-001", "Normal",
       "Bug KH #35729: action テンプレート ở folder default và folder KHÁC default ⇒ lưu \"selected_group_id\" = category_id",
       ACT + "\n- Bot có template ở folder default và ở folder tự tạo",
       "1. Mở modal action, chọn「テンプレート」, chọn template ở folder DEFAULT → lưu\n"
       "2. Query t_actions_detail.data — đọc selected_group_id\n"
       "3. Sửa action, chọn template ở folder KHÔNG phải default → lưu\n4. Query lại\n"
       "5. Friend trigger auto reply → quan sát template nhận được trên LINE app",
       "2 template: 1 ở folder default, 1 ở folder tự tạo",
       "- Cả 2 trường hợp: edit action thành công\n"
       "- DB: t_actions_detail.data chứa \"selected_group_id\" = category_id của folder tương ứng\n"
       "- Friend trigger auto reply → nhận đúng template trên LINE app",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r72-r73 + r102"),

    tc("Action — テンプレート & ステップ", "REG-SHARED-001", "Normal",
       "Tạo mới action テンプレート ⇒ t_actions_detail lưu selected_group_id và friend nhận được template",
       ACT,
       "1. Tạo quy tắc mới, mở modal action, chọn「テンプレート」\n2. Chọn 1 template, lưu action, lưu quy tắc\n"
       "3. Query t_actions_detail\n4. Friend trigger auto reply → quan sát LINE app",
       "1 template bất kỳ",
       "- Tạo mới action thành công\n- DB: t_actions_detail có lưu selected_group_id\n"
       "- Friend nhận được template trên LINE app",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r74"),

    tc("Action — テンプレート & ステップ", "DATA-REF-001", "Normal",
       "Đã setting action テンプレート → XÓA template gốc ⇒ action chứa template đó bị xóa khỏi quy tắc",
       ACT + "\n- Quy tắc có action gửi template T1 và 1 action khác",
       "1. Sang màn quản lý template, xóa T1\n2. Mở edit quy tắc auto reply, mở modal action\n"
       "3. Query t_actions_detail WHERE id=<action chứa T1>",
       "Xóa template T1 đang được action tham chiếu",
       "- Action chứa T1 bị xóa khỏi quy tắc\n- Mở modal setting action khác vẫn thành công\n"
       "- DB: t_actions_detail xóa bản ghi có action id đã bị xóa",
       note="Nguồn: Ver1.0 r76"),

    tc("Action — テンプレート & ステップ", "REG-SHARED-001", "Normal",
       "Bug KH #35729: action ステップ (scenario) ở folder default và không default ⇒ lưu selected_group_id = 0",
       ACT + "\n- Bot có scenario ở folder default và folder tự tạo",
       "1. Mở modal action, chọn「ステップ」, chọn scenario ở folder DEFAULT → lưu → query\n"
       "2. Sửa sang scenario ở folder KHÔNG default → lưu → query\n"
       "3. Friend trigger auto reply → quan sát scenario được start",
       "2 scenario: folder default và folder tự tạo",
       "- Cả 2 trường hợp: edit thành công\n- DB: t_actions_detail.data có selected_group_id = 0\n"
       "- Friend trigger auto reply → scenario được start (tạo bản ghi scenario_lineuser / scenario_step_time)",
       env="PRODUCTION",
       note="⚠️ Corpus ghi rõ scenario luôn lưu selected_group_id = 0 (khác template lưu category_id) — "
            "chi tiết này KHÔNG có trong db-mapping.md ⇒ MT-21. Nguồn: Ver1.0 r78-r79 + r103"),

    tc("Action — テンプレート & ステップ", "INTG-HOOK-001", "Normal",
       "Action ステップ từ auto reply: start scenario từ đầu / từ giữa / stop ⇒ scenario_lineuser + scenario_step_time đúng",
       ACT + "\n- Có scenario S1 nhiều step\n- Friend F chưa được add vào S1",
       "1. Cấu hình action「ステップ」= start S1 từ đầu → F gửi keyword → query scenario_lineuser + scenario_step_time\n"
       "2. Đổi action = start từ giữa (step giữa) → F gửi keyword → query lại\n"
       "3. Đổi action = stop S1 → F gửi keyword → query lại + xem màn chat 1:1",
       "3 chế độ action ステップ: start từ đầu / start từ giữa / stop",
       "- Start từ đầu: tạo scenario_lineuser (is_follow=1) + scenario_step_time từ step đầu\n"
       "- Start từ giữa: scenario_step_time bắt đầu từ step được chọn\n"
       "- Stop: scenario_lineuser.is_follow = 0, XÓA toàn bộ scenario_step_time của F; màn chat 1:1 hiện message stop",
       env="PRODUCTION",
       note="3 chế độ có 3 kết quả khác nhau, ghi rõ từng chế độ. Nguồn: TCsLine_ModalAction / Improve action 1.0 "
            "r7-r9 (02/2023). ⚠️ Cột Note của corpus r9 ghi 'k có message stop' ⇒ điểm ĐÃ TỪNG LỖI, TC ~3.5 năm tuổi, "
            "CẦN VERIFY LẠI"),

    tc("Action — テンプレート & ステップ", "DATA-REF-001", "Normal",
       "Đã setting action ステップ → XÓA scenario gốc ⇒ action chứa scenario đó bị xóa khỏi quy tắc",
       ACT + "\n- Quy tắc có action start scenario S1",
       "1. Sang màn ステップ配信, xóa S1\n2. Mở edit quy tắc auto reply, mở modal action\n"
       "3. Query t_actions_detail WHERE id=<action chứa S1>",
       "Xóa scenario S1 đang được action tham chiếu",
       "- Action chứa S1 bị xóa khỏi quy tắc\n- Mở modal setting action khác vẫn thành công\n"
       "- DB: t_actions_detail xóa bản ghi tương ứng",
       note="Nguồn: Ver1.0 r82"),

    # ═══════════════ Action — リッチメニュー & リマインド ═══════════════
    tc("Action — リッチメニュー & リマインド", "REG-SHARED-001", "Normal",
       "Bug KH #35729: action リッチメニュー ở folder default và không default ⇒ lưu selected_group_id = group_id",
       ACT + "\n- Bot có richmenu ở folder default và folder tự tạo",
       "1. Mở modal action, chọn「リッチメニュー」, chọn richmenu folder DEFAULT → lưu → query\n"
       "2. Sửa sang richmenu folder KHÔNG default → lưu → query\n"
       "3. Friend trigger auto reply → mở LINE app kiểm tra richmenu hiển thị",
       "2 richmenu: folder default và folder tự tạo",
       "- Cả 2: edit action thành công\n- DB: t_actions_detail.data có selected_group_id = group_id tương ứng\n"
       "- Friend trigger auto reply → richmenu của friend đổi đúng trên LINE app",
       env="PRODUCTION",
       note="RULE-06 verify tới LINE app. Nguồn: Ver1.0 r84-r85 + r104"),

    tc("Action — リッチメニュー & リマインド", "REG-SHARED-001", "Normal",
       "Tạo mới action リッチメニュー ⇒ lưu selected_group_id và richmenu được áp cho friend",
       ACT,
       "1. Tạo quy tắc mới, mở modal action, chọn「リッチメニュー」\n2. Chọn 1 richmenu, lưu\n"
       "3. Query t_actions_detail\n4. Friend trigger auto reply → kiểm tra LINE app",
       "1 richmenu bất kỳ",
       "- Tạo mới action thành công\n- DB: t_actions_detail có lưu selected_group_id\n"
       "- Richmenu của friend đổi đúng trên LINE app",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r86"),

    tc("Action — リッチメニュー & リマインド", "DATA-REF-001", "Normal",
       "Đã setting action リッチメニュー → XÓA richmenu gốc ⇒ action chứa richmenu đó bị xóa khỏi quy tắc",
       ACT + "\n- Quy tắc có action đổi richmenu RM1",
       "1. Sang màn リッチメニュー, xóa RM1\n2. Mở edit quy tắc auto reply, mở modal action\n"
       "3. Query t_actions_detail WHERE id=<action chứa RM1>",
       "Xóa richmenu RM1 đang được action tham chiếu",
       "- Action chứa RM1 bị xóa khỏi quy tắc\n- Mở modal setting action khác vẫn thành công\n"
       "- DB: t_actions_detail xóa bản ghi tương ứng",
       note="Nguồn: Ver1.0 r88"),

    tc("Action — リッチメニュー & リマインド", "REG-SHARED-001", "Normal",
       "Bug KH #35729: action リマインド ở folder default và không default ⇒ lưu selected_group_id = category_id",
       ACT + "\n- Bot có remind ở folder default và folder tự tạo",
       "1. Mở modal action, chọn「リマインド」, chọn remind folder DEFAULT → lưu → query\n"
       "2. Sửa sang remind folder KHÔNG default → lưu → query\n"
       "3. Friend trigger auto reply → query event_step_time",
       "2 remind: folder default và folder tự tạo",
       "- Cả 2: edit action thành công\n- DB: t_actions_detail.data có selected_group_id = category_id tương ứng\n"
       "- Friend trigger auto reply → tạo bản ghi event_step_time cho friend",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r90-r91 + r105"),

    tc("Action — リッチメニュー & リマインド", "REG-SHARED-001", "Normal",
       "Tạo mới action リマインド ⇒ lưu selected_group_id và remind được start cho friend",
       ACT,
       "1. Tạo quy tắc mới, mở modal action, chọn「リマインド」\n2. Chọn 1 remind, lưu\n"
       "3. Query t_actions_detail\n4. Friend trigger auto reply → query event_step_time",
       "1 remind bất kỳ",
       "- Tạo mới action thành công\n- DB: t_actions_detail có lưu selected_group_id\n"
       "- event_step_time có bản ghi mới cho friend",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r92"),

    tc("Action — リッチメニュー & リマインド", "DATA-REF-001", "Normal",
       "Đã setting action リマインド → XÓA remind gốc ⇒ action chứa remind đó bị xóa khỏi quy tắc",
       ACT + "\n- Quy tắc có action リマインド RE1",
       "1. Sang màn リマインド配信, xóa RE1\n2. Mở edit quy tắc auto reply, mở modal action\n"
       "3. Query t_actions_detail WHERE id=<action chứa RE1>",
       "Xóa remind RE1 đang được action tham chiếu",
       "- Action chứa RE1 bị xóa khỏi quy tắc\n- Mở modal setting action khác vẫn thành công\n"
       "- DB: t_actions_detail xóa bản ghi tương ứng",
       note="Nguồn: Ver1.0 r94"),

    tc("Action — リッチメニュー & リマインド", "FUNC-001", "Normal",
       "Copy quy tắc có action リッチメニュー / リマインド ⇒ action được clone, sửa bản copy không ảnh hưởng bản gốc",
       ACT + "\n- Quy tắc R có action richmenu RM1 và action remind RE1",
       "1. Copy quy tắc R\n2. Trường hợp A: không sửa action đã copy → lưu\n"
       "3. Trường hợp B: copy lần nữa, sửa action richmenu sang RM2 → lưu\n"
       "4. Mở lại quy tắc R gốc kiểm tra action\n5. Query t_actions_detail của 3 quy tắc",
       "R: {RM1, RE1}. Bản copy B đổi RM1 → RM2",
       "- Bản copy A: giữ nguyên RM1 + RE1\n- Bản copy B: RM2 + RE1\n"
       "- Quy tắc R gốc: VẪN RM1 + RE1\n- 3 quy tắc có 3 bộ t_actions_detail độc lập",
       note="Nguồn: Ver1.0 r87 + r93 (Check copy của richmenu và remind)"),

    # ═══════════════ Action — タグ/対応ステータス/ブロック/ブックマーク ═══════════════
    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「タグ」: gắn/gỡ tag cho friend khi auto reply chạy ⇒ tag_line_user cập nhật đúng",
       ACT + "\n- Bot có tag T1 (chưa gắn cho friend F) và tag T2 (đã gắn cho F)",
       "1. Cấu hình action:「タグ」gắn T1 + gỡ T2\n2. Lưu quy tắc\n3. Friend F gửi keyword trigger\n"
       "4. Query: SELECT * FROM tag_line_user WHERE line_user_id=<F>\n5. Mở màn 友だち詳細 của F xem danh sách tag",
       "Action: gắn T1, gỡ T2",
       "- DB tag_line_user: có bản ghi (F, T1); KHÔNG còn bản ghi (F, T2)\n"
       "- Màn 友だち詳細 của F: hiện T1, không hiện T2",
       env="PRODUCTION",
       note="Verify 2 tầng DB + màn hình. Nguồn: TCsLine_BackUp / Backup (job) r12 + TCsLine_ModalAction / "
            "Add tag mới ở modal action r19. Corpus KHÔNG có TC gắn/gỡ tag từ auto reply ở tầng runtime chi tiết ⇒ "
            "phần chi tiết do AI viết theo spec §7 doAction type 'tag'"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "FUNC-MULTI-001", "Normal",
       "BR-20 tag action chaining: tag được gắn CÓ action riêng ⇒ doAction đệ quy, action của tag cũng chạy",
       ACT + "\n- Tag T1 có gắn sẵn action riêng (VD start scenario S2)\n- Quy tắc auto reply có action gắn T1",
       "1. Friend F gửi keyword trigger auto reply\n2. Query tag_line_user cho F\n"
       "3. Query scenario_lineuser / scenario_step_time của F cho S2\n4. Quan sát LINE app của F",
       "Tag T1 có chained action = start scenario S2",
       "- F được gắn tag T1\n- Action của tag T1 CŨNG chạy: F được start vào scenario S2\n"
       "- F nhận đủ output của cả 2 tầng action trên LINE app",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-20 (HandlePostbackTask.java:3364-3899, có ignoreHandled map chống lặp vô hạn). "
            "Corpus KHÔNG có TC chaining ⇒ TC lấp GAP do AI viết theo spec, CẦN LEADER XÁC NHẬN"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「対応ステータス」: đổi trạng thái đối ứng của conversation khi auto reply chạy",
       ACT + "\n- Bot có status_chat「対応中」\n- Friend F đang ở status khác",
       "1. Cấu hình action「対応ステータス」= 対応中\n2. Lưu quy tắc\n3. F gửi keyword trigger\n"
       "4. Query: SELECT id_status FROM conversation WHERE line_user_id=<F>\n5. Mở màn chat 1:1 xem status của F",
       "Status「対応中」",
       "- DB: conversation.id_status = id của「対応中」\n- Màn chat 1:1 hiện status「対応中」cho F",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r153-r154 + Backup (job) r18"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「対応ステータス」: BỎ gắn status ⇒ is_status = NULL",
       ACT + "\n- Friend F đang có status「対応中」",
       "1. Cấu hình action「対応ステータス」= bỏ gắn status\n2. F gửi keyword trigger\n"
       "3. Query conversation của F\n4. Xem màn chat 1:1",
       "Action: bỏ gắn status",
       "- DB: is_status = NULL\n- Màn chat 1:1 hiện F không còn status",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r155-r156"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「ブロック」: block friend khi auto reply chạy ⇒ is_blocked = 1, blocked_by = 1 ở cả conversation và bot_line_user",
       ACT + "\n- Friend F đang bình thường (is_blocked = 0)",
       "1. Cấu hình action「ブロック」= block friend\n2. Lưu quy tắc\n3. F gửi keyword trigger\n"
       "4. Query: SELECT is_blocked, blocked_by FROM conversation WHERE line_user_id=<F>\n"
       "5. Query: SELECT is_blocked FROM bot_line_user WHERE line_user_id=<F> AND bot_id=A\n"
       "6. Mở màn chat 1:1 / friend list xem trạng thái F",
       "Action block friend",
       "- conversation: is_blocked = 1, blocked_by = 1\n- bot_line_user: is_blocked = 1\n"
       "- Màn friend list hiện F ở nhóm bị bot block",
       env="PRODUCTION",
       note="Verify 3 tầng: 2 bảng DB + màn hình (RULE-07). Nguồn: TCsLine_JOB / Test fix bug KH r159-r161"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「ブロック」: unblock friend ⇒ is_blocked = 0 ở cả conversation và bot_line_user",
       ACT + "\n- Friend F đang bị bot block (is_blocked = 1)\n"
       "- Quy tắc có 対象 =「ブロックした友だち」để rule chạy được cho user bị block",
       "1. Cấu hình action「ブロック」= unblock friend\n2. F gửi keyword trigger\n"
       "3. Query conversation + bot_line_user của F\n4. Xem màn friend list",
       "Action unblock friend",
       "- conversation: is_blocked = 0\n- bot_line_user: is_blocked = 0\n- F trở lại danh sách friend bình thường",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r162-r164"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action ẩn/bỏ ẩn friend: ẩn friend ⇒ is_hide = 1 và conversation được đổi trạng thái confirm",
       ACT + "\n- Friend F đang hiển thị (is_hide = 0)",
       "1. Cấu hình action ẩn friend\n2. F gửi keyword trigger\n"
       "3. Query: SELECT is_hide, confirm_count, status_last_message, has_status_0, has_status_1 "
       "FROM conversation WHERE line_user_id=<F>\n4. Xem màn chat 1:1 / friend list",
       "Action ẩn friend",
       "- conversation.is_hide = 1\n"
       "- Khi ẩn: confirm_count = 0, status_last_message = 1, has_status_0 = 0, has_status_1 = 1\n"
       "- F không còn hiện ở danh sách chat mặc định",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r169-r170"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action bỏ ẩn friend ⇒ is_hide = 0, status confirm hiển thị đúng",
       ACT + "\n- Friend F đang bị ẩn (is_hide = 1)",
       "1. Cấu hình action bỏ ẩn friend\n2. F gửi keyword trigger\n3. Query is_hide + status confirm\n"
       "4. Xem màn chat 1:1",
       "Action bỏ ẩn friend",
       "- conversation.is_hide = 0\n- Status confirm hiển thị đúng trên màn chat 1:1",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r171-r172"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "REG-SHARED-001", "Normal",
       "Action「ブックマーク」: add / bỏ bookmark cho conversation của friend",
       ACT + "\n- Friend F chưa được bookmark",
       "1. Cấu hình action add bookmark → F gửi keyword trigger → query is_bookmark → xem màn chat 1:1\n"
       "2. Đổi action sang bỏ bookmark → F gửi keyword trigger → query is_bookmark → xem màn chat 1:1",
       "2 chế độ: add bookmark / bỏ bookmark",
       "- Add: conversation.is_bookmark = 1, màn chat 1:1 hiện icon bookmark\n"
       "- Bỏ: conversation.is_bookmark = 0, icon bookmark biến mất",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB / Test fix bug KH r175-r178 + Backup (job) r16"),

    tc("Action — タグ/対応ステータス/ブロック/ブックマーク", "MSG-001", "Normal",
       "Action「テキスト」: gửi text trực tiếp từ auto reply ⇒ friend nhận được text, màn chat 1:1 hiện message với trigger 自動応答",
       ACT,
       "1. Cấu hình action「テキスト」với nội dung có chèn tên friend\n2. Lưu quy tắc\n3. Friend F gửi keyword trigger\n"
       "4. Quan sát LINE app của F\n5. Mở màn chat 1:1 xem message và trigger",
       "Text:「{friend_name}さん、こんにちは」",
       "- F nhận được text trên LINE app, tên friend được thay đúng\n"
       "- Màn chat 1:1 hiện message trả về, trigger hiển thị「自動応答」",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r10 + 01. TCsLine_Chat1:1 (Improve 10/2024) / Content: Hiển thị msg r1189-r1190 "
            "(trigger hiển thị 自動応答 + tên qly hiện dấu -)"),

    # ═══════════════ Action — dữ liệu gốc bị xóa ═══════════════
    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "Triển khai ngang #37710: quy tắc CHỈ CÓ 1 action, xóa dữ liệu gốc của action đó "
       "⇒ mở detail auto-reply bình thường, KHÔNG hiện alert Trying to get property 'details' of non-object",
       "- Đang ở màn /basic/reply của bot A\n"
       "- Quy tắc R có ĐÚNG 1 action, lần lượt test với từng loại: scenario / template / remind / tag / richmenu / "
       "friend info / status chat",
       "1. Với mỗi loại action: tạo quy tắc R chỉ có 1 action của loại đó\n"
       "2. Sang màn gốc của loại đó, XÓA dữ liệu gốc (scenario/template/remind/tag/richmenu/friend info/status chat)\n"
       "3. Mở detail quy tắc R\n4. Mở modal「アクション設定」\n5. Quan sát preview action và nội dung modal",
       "7 loại action: scenario / template / remind / tag / richmenu / friend info / status chat",
       "- Mở detail auto-reply BÌNH THƯỜNG, KHÔNG hiện alert「Trying to get property 'details' of non-object」\n"
       "- KHÔNG hiển thị action đã bị xóa gốc, KHÔNG hiển thị cả preview của action đó\n"
       "- Áp dụng cho cả 7 loại",
       note="7 loại cùng 1 kết quả nên giữ chung. Nguồn: Improve chung / Improve nhỏ r543, r546, r549, r552, r555, "
            "r558, r561 (Triển khai ngang #37710)"),

    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "#37710: quy tắc có NHIỀU action, chỉ xóa dữ liệu gốc của 1 action ⇒ action đó biến mất, các action khác giữ nguyên "
       "và vẫn chạy phía LINE",
       "- Quy tắc R có 3 action, trong đó 1 action tham chiếu dữ liệu sẽ bị xóa\n"
       "- Lặp lại cho 7 loại action như TC trước",
       "1. Xóa dữ liệu gốc của 1 action (VD xóa scenario đang được set)\n2. Mở detail quy tắc R + modal action\n"
       "3. Friend gửi keyword trigger auto reply\n4. Quan sát LINE app của friend",
       "7 loại action; mỗi lần chỉ xóa gốc của 1 action, giữ lại 2 action còn lại",
       "- Mở detail bình thường, không alert lỗi\n- Action bị xóa gốc KHÔNG hiển thị (cả preview)\n"
       "- 2 action còn lại vẫn hiển thị đầy đủ\n"
       "- Phía LINE user: KHÔNG chạy action đã bị xóa; các action còn lại chạy bình thường",
       env="PRODUCTION",
       note="Corpus ghi rõ 'Check bổ sung phía line user: không chạy action đã bị xóa, các action còn lại chạy bình "
            "thường'. Nguồn: Improve chung / Improve nhỏ r544, r547, r550, r553, r556, r559, r562"),

    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "#37710: xóa dữ liệu gốc của TẤT CẢ action bên trong quy tắc ⇒ mở detail bình thường, không action nào hiển thị",
       "- Quy tắc R có nhiều action, xóa hết dữ liệu gốc của tất cả\n- Lặp lại cho 7 loại action",
       "1. Xóa dữ liệu gốc của TẤT CẢ action trong quy tắc R\n2. Mở detail quy tắc R + modal action\n"
       "3. Friend gửi keyword trigger\n4. Quan sát LINE app",
       "7 loại action, xóa toàn bộ dữ liệu gốc",
       "- Mở detail bình thường, KHÔNG alert lỗi\n- KHÔNG hiển thị action nào, KHÔNG hiển thị preview nào\n"
       "- Friend KHÔNG nhận được action nào",
       env="PRODUCTION",
       note="Nguồn: Improve chung / Improve nhỏ r545, r548, r551, r554, r557, r560, r563"),

    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "#37710: bên trong multi action CÓ setting filter → xóa dữ liệu gốc của filter (khi filter chỉ có 1 action_id) "
       "⇒ mở detail bình thường, không hiển thị filter đã xóa",
       "- Quy tắc R có action bên trong đã setting filter (VD filter = tag T1)\n- Test cả filter AND và filter OR",
       "1. Xóa tag T1 (dữ liệu gốc của filter)\n2. Mở detail quy tắc R\n3. Mở modal action, xem phần filter bên trong\n"
       "4. Friend trigger auto reply → quan sát",
       "Filter = tag, chỉ có 1 action_id trong filter; test cả khối AND và OR",
       "- Mở detail auto-reply bình thường, KHÔNG alert「Trying to get property 'details' of non-object」\n"
       "- KHÔNG hiển thị tag đã xóa, KHÔNG hiển thị preview của tag đã xóa\n- Action đó KHÔNG chạy phía LINE user",
       env="PRODUCTION",
       note="Nguồn: Improve chung / Improve nhỏ r892 (Triển khai ngang #37710)"),

    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "#37710: filter bên trong multi action có NHIỀU action_id → chỉ xóa 1 ⇒ chỉ mục đó biến mất, các mục khác giữ nguyên",
       "- Quy tắc R có action với filter chứa nhiều action_id (nhiều tag/scenario)\n- Test cả filter AND và OR",
       "1. Xóa dữ liệu gốc của 1 action_id trong filter\n2. Mở detail quy tắc R + modal action\n"
       "3. Friend trigger → quan sát",
       "Filter nhiều action_id; xóa 1",
       "- Mở detail bình thường, không alert lỗi\n- Chỉ mục bị xóa gốc biến mất khỏi filter\n"
       "- Các mục còn lại trong filter giữ nguyên và vẫn có hiệu lực lọc",
       env="PRODUCTION",
       note="Nguồn: Improve chung / Improve nhỏ r893"),

    tc("Action — dữ liệu gốc bị xóa", "DATA-REF-001", "Abnormal",
       "#37710: xóa TẤT CẢ action_id trong filter của multi action ⇒ mở detail bình thường, filter trống",
       "- Quy tắc R có action với filter chứa nhiều action_id\n- Test cả filter AND và OR",
       "1. Xóa dữ liệu gốc của TẤT CẢ action_id trong filter\n2. Mở detail quy tắc R + modal action\n"
       "3. Friend trigger → quan sát",
       "Filter nhiều action_id; xóa hết",
       "- Mở detail bình thường, KHÔNG alert lỗi\n- KHÔNG hiển thị mục nào trong filter, không hiện preview\n"
       "- Ghi lại hành vi: action còn chạy (không còn điều kiện lọc) hay không chạy",
       env="PRODUCTION",
       note="Nguồn: Improve chung / Improve nhỏ r894 — corpus KHÔNG nói rõ action còn chạy hay không khi filter rỗng "
            "hoàn toàn ⇒ điểm cần Leader xác nhận"),

    tc("Action — dữ liệu gốc bị xóa", "REG-RUN-001", "Normal",
       "#37710 regression: các action KHÔNG bị xóa gốc vẫn hiển thị và gửi được cho friend bình thường",
       "- Quy tắc R có 7 action đầy đủ, KHÔNG xóa dữ liệu gốc nào",
       "1. Mở detail quy tắc R + modal action\n2. Friend gửi keyword trigger\n3. Quan sát LINE app + màn chat 1:1\n"
       "4. Lặp lại kiểm tra cho từng loại: scenario / template / remind / tag / richmenu / friend info / status chat",
       "7 loại action đầy đủ dữ liệu gốc",
       "- Hiển thị đầy đủ 7 action + preview\n- Friend nhận được đủ output của cả 7 action",
       env="PRODUCTION",
       note="TC regression bắt buộc sau khi sửa logic ẩn action đã xóa. "
            "Nguồn: Improve chung / Improve nhỏ r950-r956"),

    # ═══════════════ Action — recover & đổi tên ═══════════════
    tc("Action — recover & đổi tên", "REG-SHARED-001", "Normal",
       "Bug #29412: đổi tên dữ liệu gốc ở màn gốc ⇒ tên action trong modal action của auto reply được cập nhật theo",
       "- Quy tắc auto reply đã gắn các action: remind / richmenu / friend info / status chat",
       "1. Mở modal action của quy tắc, ghi lại tên hiển thị của từng action\n"
       "2. Sang màn gốc của từng loại, đổi tên sang tên khác\n"
       "3. Quay lại mở modal action của quy tắc auto reply\n4. So sánh tên hiển thị",
       "4 loại action: remind / richmenu / friend info / status chat",
       "- Tên của các action tương ứng được UPDATE theo tên mới ở màn gốc\n- Không hiện tên cũ",
       note="Nguồn: TCsLine_ModalAction / Update tên action r45 (04/2025) — dòng『auto reply』của ma trận "
            "triển khai ngang cho ~20 màn"),

    tc("Action — recover & đổi tên", "MSG-001", "Normal",
       "Support [name]: action text của auto reply gửi qua job ⇒ thay được biến tên friend",
       "- Quy tắc auto reply có action text chứa biến tên friend\n- Friend F có tên hiển thị LINE là「山田」",
       "1. Cấu hình action text có chèn biến tên\n2. F gửi keyword trigger\n"
       "3. Quan sát LINE app của F\n4. Quan sát màn chat 1:1",
       "Text có biến tên friend; friend name =「山田」",
       "- LINE app của F: tên được thay đúng thành「山田」\n- Màn chat 1:1 hiển thị nội dung đã thay tên",
       env="PRODUCTION",
       note="Nguồn: TCsLine_ModalAction / Support name r9 + r16 (12/2023) — auto reply nằm trong danh sách "
            "『Check các case Send từ job』. TC ~2.7 năm tuổi, CẦN VERIFY LẠI"),

    tc("Action — recover & đổi tên", "REG-SHARED-001", "Normal",
       "Thêm option random cho action friend info kiểu point từ auto reply ⇒ ghi đè / cộng point đúng theo cấu hình",
       "- Friend info type point「ポイント」\n- Friend F đang có 100 điểm",
       "1. Cấu hình action friend info point, chế độ「ghi đè」kiểu chỉ định giá trị 50 → F trigger → query point\n"
       "2. Đổi sang chế độ「cộng point」kiểu chỉ định giá trị 30 → F trigger → query point\n"
       "3. Đối chiếu với màn 友だち詳細 của F",
       "F ban đầu 100 điểm. Ghi đè 50 → kỳ vọng 50. Sau đó cộng 30 → kỳ vọng 80",
       "- Sau ghi đè: friend_info_value = 50 (không phải 150)\n- Sau cộng: friend_info_value = 80 (50 + 30)\n"
       "- Màn 友だち詳細 hiển thị đúng giá trị mỗi lần",
       env="PRODUCTION",
       note="Có phép tính tay ở cột Dữ liệu test. Nguồn: TCsLine_ModalAction / Thêm option random cho action friend "
            "infor point r30, r72, r99 (11/2023) — dòng『autoreply』. TC ~2.8 năm tuổi, CẦN VERIFY LẠI"),
]
