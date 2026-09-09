# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 (Đặt lịch bài học) — Nhóm 1-6: màn list calendar, wizard tạo, giới hạn plan, コース.

Nguồn chính: 11.2 TCsLine_LessonCalendar
  - tab「Calendar list」(05/2024 → 2025, 56 TC lá) — màn list + wizard tạo calendar + tạo course đầu
  - tab「Quản lý course」(05/2024 → 02/2026, 129 TC lá) — CRUD course, action/filter cấp course,
    Bug KH #34561 (02/2026), Support #27091 (11/2024), Feature #27496 (01/2024 — OFF course)
  - tab「Task nhỏ + fix bug KH」r111-r143 — Bug #30002 ưu tiên action course
Bổ sung: TCsLine_Limit all tính năng → tab「Limit Lesson」(tab RỖNG — không dùng được).
Spec đối chiếu: spec-features/admin/lesson-booking/ (BR-01…BR-10, BR-30, BR-31, BR-44).
"""
from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A đã liên kết LINE OA, gói standard\n"
       "- Bot A đã đăng ký LIFF ID cho tính năng đặt lịch\n"
       "- Mở menu 予約管理 > レッスン予約 (/basic/calendar-management)")
CAL = (ADM + "\n- Đã có 1 lesson calendar「レッスンA」(管理名「レA」) đang ON, "
       "có 1 course「初心者向けトレーニング」(system_name「初心者」, 1h00, 5.000 yên)")

S1 = [
    # ══════════════════ 1. Màn list calendar ══════════════════
    tc("Màn list calendar", "FUNC-001", "Normal",
       "Bot chưa có lesson calendar nào → hiện message rỗng",
       ADM + "\n- Bot A CHƯA tạo lesson calendar nào (`calendar_management` rỗng với bot_id này)",
       "1. Mở /basic/calendar-management\n2. Quan sát vùng danh sách",
       "0 calendar",
       "- Hiện message「まだ登録されたカレンダー予約がありません。」\n"
       "- Không hiện card calendar nào\n"
       "- Nút 新規作成 vẫn bấm được",
       note="Nguồn: Calendar list r3. Spec §3.1 SCR-LSN-01."),

    tc("Màn list calendar", "UI-002", "Normal",
       "Popup hướng dẫn nút 新規作成 hiện lần đầu, bấm X thì tắt vĩnh viễn cho account đó",
       ADM + "\n- Account admin A chưa từng bấm X trên popup hướng dẫn",
       "1. Mở /basic/calendar-management lần đầu → quan sát popup\n"
       "2. Bấm icon X trên popup\n"
       "3. Vào màn khác rồi quay lại · logout/login lại · mở bằng cửa sổ ẩn danh",
       "Tài khoản admin A",
       "- Bước 1: hiện popup「新規作成をクリックして、はじめのカレンダー予約を作成しましょう。」\n"
       "- Bước 2: popup ẩn đi\n"
       "- Bước 3: cả 3 lối vào lại đều KHÔNG hiện popup nữa",
       note="Nguồn: Calendar list r4-r6 (verify 3 lối vào lại — RULE-07)."),

    tc("Màn list calendar", "UI-002", "Normal",
       "Popup hướng dẫn vẫn hiện với account admin khác chưa bấm X",
       ADM + "\n- Admin A đã bấm X tắt popup · Admin B cùng bot A chưa bấm",
       "1. Logout admin A\n2. Đăng nhập admin B\n3. Mở /basic/calendar-management",
       "2 tài khoản admin trên cùng bot A",
       "- Admin B VẪN hiện popup hướng dẫn ⇒ cờ lưu theo user, không theo bot",
       note="Nguồn: Calendar list r7."),

    tc("Màn list calendar", "UI-001", "Normal",
       "Nút よくある質問 và マニュアル mở đúng tab mới",
       ADM,
       "1. Mở màn list\n2. Bấm nút「よくある質問」\n3. Quay lại, bấm nút「マニュアル」",
       "—",
       "- Mỗi nút mở 1 tab mới\n- URL đích là trang FAQ / manual của LME, không báo 404",
       note="Nguồn: Calendar list r17-r18 — TC gốc CHỈ CÓ TIÊU ĐỀ, kết quả mong đợi do AI bổ sung "
            "(mức tối thiểu đo được: mở tab mới + không 404). Cần Leader xác nhận URL đích."),

    tc("Màn list calendar", "LIST-001", "Normal",
       "Popup sắp xếp: đổi vị trí bằng nút rồi Lưu → thứ tự đổi ở màn list",
       CAL + "\n- Bot có 3 calendar theo thứ tự C1, C2, C3",
       "1. Bấm nút sắp xếp → hiện popup\n2. Dùng nút mũi tên đưa C3 lên đầu\n3. Bấm Lưu\n4. Reload màn list",
       "3 calendar C1, C2, C3",
       "- Popup sắp xếp hiện đúng 3 calendar\n"
       "- Sau khi lưu và reload: thứ tự là C3, C1, C2\n"
       "- Cột `calendar_management.order` đổi tương ứng",
       note="Nguồn: Calendar list r19, r21."),

    tc("Màn list calendar", "LIST-001", "Normal",
       "Popup sắp xếp: đổi vị trí bằng drag&drop rồi Lưu → thứ tự đổi",
       CAL + "\n- Bot có 3 calendar C1, C2, C3",
       "1. Mở popup sắp xếp\n2. Kéo thả C1 xuống cuối\n3. Bấm Lưu\n4. Reload màn list",
       "3 calendar",
       "- Sau reload thứ tự là C2, C3, C1",
       note="Nguồn: Calendar list r22."),

    tc("Màn list calendar", "LIST-001", "Abnormal",
       "Popup sắp xếp: đổi vị trí nhưng KHÔNG lưu → thứ tự giữ nguyên",
       CAL + "\n- Bot có 3 calendar C1, C2, C3",
       "1. Mở popup sắp xếp\n2. Đổi vị trí C3 lên đầu\n3. Đóng popup không bấm Lưu\n4. Reload màn list",
       "3 calendar",
       "- Thứ tự vẫn là C1, C2, C3 (không đổi)\n- `calendar_management.order` không đổi",
       note="Nguồn: Calendar list r20."),

    tc("Màn list calendar", "UI-001", "Normal",
       "Popup preview khi bấm 新規作成 — 3 nút điều hướng",
       ADM,
       "1. Bấm nút 新規作成 → hiện popup preview\n"
       "2. Bấm link「サロン・面談予約はこちら」\n3. Quay lại, bấm「イベント予約はこちら」\n"
       "4. Quay lại, bấm icon X\n5. Bấm 新規作成 lại rồi bấm「次にすすむ」",
       "—",
       "- Bước 1: popup preview hiện data giới thiệu, mở ở tab mới\n"
       "- Bước 2: điều hướng sang màn đặt lịch salon (/basic/calendar-salon)\n"
       "- Bước 3: điều hướng sang màn イベント予約\n"
       "- Bước 4: đóng popup, quay về màn list calendar\n"
       "- Bước 5: hiện popup tạo calendar mới",
       note="Nguồn: Calendar list r23-r27."),

    tc("Màn list calendar", "UI-001", "Normal",
       "Cột 管理名, URL booking/history, icon Google, ảnh trên card calendar",
       CAL + "\n- Calendar「レッスンA」đã liên kết Google Spreadsheet và đã set ảnh ở màn トップ設定",
       "1. Mở màn list\n2. Quan sát card của「レッスンA」\n"
       "3. Bấm nút copy URL booking\n4. Bấm nút copy URL history",
       "1 calendar đã liên kết GG + có ảnh top page",
       "- Hiện đúng 管理名「レA」\n- Có icon liên kết Google Calendar/Sheet\n"
       "- Hiện ảnh đã setting ở màn トップ設定\n"
       "- Bấm copy: hiện TOÀN BỘ text URL (không cắt) và copy được vào clipboard\n"
       "- Dán URL vào trình duyệt mở đúng trang booking / trang lịch sử",
       note="Nguồn: Calendar list r48-r49, r51, r54-r56 (RULE-06: đi tới output cuối = mở được URL)."),

    tc("Màn list calendar", "STATE-001", "Normal",
       "Hủy liên kết Google → icon liên kết biến mất khỏi card",
       CAL + "\n- Calendar đang liên kết Google Spreadsheet",
       "1. Vào tab 全体設定 > Googleスプレッドシート連携 → bấm hủy liên kết\n"
       "2. Quay lại màn list calendar",
       "1 calendar đã liên kết",
       "- Card calendar KHÔNG còn hiển thị icon liên kết Google",
       note="Nguồn: Calendar list r50."),

    tc("Màn list calendar", "STATE-001", "Normal",
       "Toggle ON/OFF calendar — default ON",
       CAL,
       "1. Mở màn list, quan sát toggle của calendar vừa tạo",
       "Calendar mới tạo",
       "- Toggle ON/OFF ở trạng thái ON\n- `calendar_management.enable_use_calendar` = 1",
       note="Nguồn: Calendar list r46."),

    tc("Màn list calendar", "STATE-001", "Abnormal",
       "OFF calendar → LINE user mở URL booking và URL lịch sử đều bị chặn",
       CAL + "\n- Đã có 1 LINE user U1 là bạn của bot A và đã booking 1 lần",
       "1. Tắt toggle calendar về OFF\n2. Dùng LINE user U1 mở URL booking\n"
       "3. U1 mở URL lịch sử booking",
       "URL booking + URL history của calendar đã OFF",
       "- Bước 2 và 3: LINE user thấy màn báo lỗi「この予約は現在利用できません。」\n"
       "- Không vào được màn chọn course",
       env="PRODUCTION",
       note="Nguồn: Calendar list r47 + Booking phía line user r4. ⚠️ MT-01 — TC gốc Calendar list r47 "
            "nói「hiển thị 404」, TC gốc Booking phía line user r4 nói「báo lỗi この予約は現在利用できません。」. "
            "Đã lấy theo bản mới hơn (tab Booking phía line user) và khớp spec BR-P01."),

    tc("Màn list calendar", "FUNC-002", "Normal",
       "Popup đổi 管理名 — hiện tên hiện tại, sửa & lưu thành công",
       CAL,
       "1. Bấm icon edit cạnh 管理名\n2. Quan sát giá trị mặc định\n"
       "3. Sửa thành「レB」(2 ký tự)\n4. Lưu\n5. Reload màn list",
       "管理名 mới =「レB」",
       "- Bước 2: ô nhập hiện đúng 管理名 hiện tại「レA」\n"
       "- Bước 5: card hiện「レB」; `calendar_management.calendar_name` = 「レB」",
       note="Nguồn: Calendar list r52, r58. ⚠️ Spec A-02: endpoint POST /{id}/edit là IDOR + mass "
            "assignment (nằm ngoài middleware checkLessonCalendarInBot) — xem MT-16."),

    tc("Màn list calendar", "FUNC-002", "Abnormal",
       "管理名 để trống → báo lỗi required",
       CAL,
       "1. Bấm icon edit 管理名\n2. Xóa hết nội dung\n3. Bấm Lưu",
       "Chuỗi rỗng",
       "- Báo lỗi required, KHÔNG lưu\n- `calendar_management.calendar_name` giữ giá trị cũ",
       note="Nguồn: Calendar list r59."),

    tc("Màn list calendar", "FUNC-004", "Boundary",
       "管理名 — biên 10 ký tự và 11 ký tự",
       CAL,
       "1. Nhập 管理名 đúng 10 ký tự tiếng Nhật → Lưu\n"
       "2. Nhập 管理名 11 ký tự tiếng Nhật → Lưu",
       "10 ký tự: 「あいうえおかきくけこ」\n11 ký tự: 「あいうえおかきくけこさ」",
       "- 10 ký tự: lưu thành công, màn list hiện đủ 10 ký tự\n"
       "- 11 ký tự: báo lỗi quá số ký tự (hoặc ô nhập chặn không cho gõ ký tự thứ 11)",
       note="Nguồn: Calendar list r60. RULE-01: cặp biên trong/ngoài."),

    tc("Màn list calendar", "DATA-TEXT-001", "Normal",
       "管理名 nhập ký tự tiếng Nhật (hiragana + katakana + kanji) → lưu và hiển thị đúng",
       CAL,
       "1. Nhập 管理名 =「レッスン教室」\n2. Lưu\n3. Reload màn list",
       "「レッスン教室」",
       "- Lưu thành công, màn list hiện đúng「レッスン教室」không bị mojibake",
       note="Nguồn: Calendar list r61."),

    tc("Màn list calendar", "FUNC-001", "Normal",
       "Nút mở trang quản lý calendar → sang đúng calendar tương ứng",
       CAL + "\n- Bot có 2 calendar C1, C2",
       "1. Bấm nút mở trang quản lý trên card C2",
       "2 calendar",
       "- Điều hướng tới /basic/calendar-management/{id của C2}\n"
       "- Header hiện đúng tên C2, không phải C1",
       note="Nguồn: Calendar list r53."),

    # ══════════════════ 2. Wizard tạo calendar ══════════════════
    tc("Wizard tạo calendar", "FUNC-002", "Abnormal",
       "Popup tạo calendar — 2 trường bắt buộc để trống → báo required",
       ADM,
       "1. 新規作成 → 次にすすむ → hiện popup tạo calendar\n"
       "2. Để trống cả 2 ô (tên hiển thị bên LINE + 管理名) → bấm nút tạo",
       "Cả 2 ô rỗng",
       "- Cả 2 ô đều báo lỗi required\n- KHÔNG tạo bản ghi trong `calendar_management`",
       note="Nguồn: Calendar list r28, r31."),

    tc("Wizard tạo calendar", "FUNC-004", "Boundary",
       "Tên hiển thị bên LINE — biên 30 và 31 ký tự",
       ADM,
       "1. Mở popup tạo calendar\n2. Nhập tên hiển thị 30 ký tự → tạo\n"
       "3. Tạo calendar khác, nhập tên hiển thị 31 ký tự → tạo",
       "30 ký tự / 31 ký tự tiếng Nhật",
       "- 30 ký tự: tạo thành công, màn edit hiện đủ 30 ký tự\n"
       "- 31 ký tự: tự động cắt còn 30 HOẶC báo lỗi vượt số ký tự — phải nhất quán 1 trong 2, "
       "không được vừa cắt vừa báo lỗi",
       note="Nguồn: Calendar list r29. ⚠️ TC gốc ghi「tự động cắt hoặc báo lỗi」— chưa chốt hành vi nào. "
            "Xem MT-02."),

    tc("Wizard tạo calendar", "FUNC-004", "Boundary",
       "管理名 lúc tạo — biên 10 và 11 ký tự",
       ADM,
       "1. Mở popup tạo calendar\n2. Nhập 管理名 10 ký tự → tạo\n3. Lần khác nhập 11 ký tự → tạo",
       "10 / 11 ký tự tiếng Nhật",
       "- 10 ký tự: tạo thành công\n- 11 ký tự: tự động cắt còn 10 HOẶC báo lỗi vượt ký tự",
       note="Nguồn: Calendar list r32. Cùng vấn đề chưa chốt như MT-02."),

    tc("Wizard tạo calendar", "DATA-TEXT-001", "Normal",
       "2 ô tên nhập tiếng Nhật → lưu và hiển thị lại đúng ở màn edit",
       ADM,
       "1. Nhập tên hiển thị「ヨガ・ピラティス教室」+ 管理名「ヨガ教室」\n2. Tạo\n3. Vào lại màn edit calendar",
       "Text Nhật có ký tự ・ và long vowel",
       "- Tạo thành công\n- Màn edit hiện lại đúng cả 2 giá trị, không mất ký tự ・ và ー",
       note="Nguồn: Calendar list r30, r33."),

    tc("Wizard tạo calendar", "FUNC-001", "Normal",
       "Nút X và Back trên popup tạo calendar",
       ADM,
       "1. Mở popup tạo, nhập data → bấm X\n"
       "2. Mở lại popup tạo từ preview, nhập data → bấm Back\n3. Từ preview bấm 次にすすむ lại",
       "Data hợp lệ đã nhập",
       "- Bước 1: đóng popup, KHÔNG lưu data, quay về màn list calendar (`calendar_management` không thêm dòng)\n"
       "- Bước 2: quay về màn preview trước đó\n"
       "- Bước 3: popup tạo hiện lại — cần xác nhận có giữ data vừa nhập hay không",
       note="Nguồn: Calendar list r34-r35. ⚠️ TC gốc r35 đặt câu hỏi mở「có hiển thị data trước đấy "
            "nhập ko?」— chưa có kết quả mong đợi. Xem MT-03."),

    tc("Wizard tạo calendar", "DATA-001", "Normal",
       "Tạo calendar thành công → sinh bản ghi DB + chuyển sang popup tạo course",
       ADM,
       "1. Nhập data hợp lệ 2 ô tên\n2. Bấm nút tạo/次へ",
       "Tên hiển thị「レッスンA」· 管理名「レA」",
       "- Đóng popup tạo calendar, hiện popup tạo course đầu tiên\n"
       "- DB: có 1 bản ghi mới ở `calendar_management`\n"
       "- DB: tự sinh 2 bản ghi `calendar_setting_send_messages` (moment = booking và cancel)\n"
       "- DB: tự sinh 2 bản ghi `calendar_setting_send_forms` — họ tên (friend_information_id = -1) "
       "và email (-3), cả 2 có can_delete = 0",
       note="Nguồn: Calendar list r36 + spec BR-07 (2 setting message + 2 form mặc định). "
            "Phần 4 bản ghi mặc định là bổ sung từ spec — corpus chỉ kiểm bảng calendar."),

    tc("Wizard tạo calendar", "DATA-001", "Normal",
       "store_name được gán bằng line_name lúc tạo",
       ADM,
       "1. Tạo calendar mới với tên hiển thị bên LINE =「レッスンA」\n"
       "2. Query `calendar_management` bản ghi vừa tạo",
       "line_name =「レッスンA」",
       "- `store_name` = `line_name` =「レッスンA」ngay sau khi tạo",
       spec="Spec không ghi",
       note="Suy luận của AI từ spec BR-08 — corpus KHÔNG có TC này. Cần Leader xác nhận. "
            "Liên quan Gap G-10: dump 0/174 bản ghi có store_name ⇒ nếu FAIL thì màn top page LINE user rỗng."),

    tc("Wizard tạo calendar", "FUNC-002", "Abnormal",
       "Popup tạo course đầu — tên course để trống → required",
       ADM + "\n- Đang ở popup tạo course sau khi tạo calendar",
       "1. Để trống ô tên course\n2. Bấm Lưu",
       "Chuỗi rỗng",
       "- Báo lỗi required, không tạo course",
       note="Nguồn: Calendar list r37."),

    tc("Wizard tạo calendar", "FUNC-004", "Boundary",
       "Tên course ở popup tạo đầu — giới hạn 30 ký tự",
       ADM + "\n- Đang ở popup tạo course",
       "1. Nhập tên course dài hơn 30 ký tự\n2. Quan sát ô nhập / thông báo",
       "Chuỗi 35 ký tự",
       "- Chỉ nhận tối đa 30 ký tự (cắt hoặc chặn gõ tiếp)",
       note="Nguồn: Calendar list r38. ⚠️ MÂU THUẪN với「Quản lý course」r28-r29 nói tên course max "
            "50 ký tự (đã confirm). Xem MT-04."),

    tc("Wizard tạo calendar", "FUNC-004", "Boundary",
       "Thời lượng course ở popup tạo đầu — default và dải giá trị",
       ADM + "\n- Đang ở popup tạo course",
       "1. Quan sát giá trị mặc định ô giờ/phút\n2. Mở droplist giờ\n3. Mở droplist phút",
       "—",
       "- Default: 1 giờ 00 phút\n- Droplist giờ: 0 → 23\n- Droplist phút: 00 → 55, bước 5 phút "
       "(00, 05, 10, …, 55)",
       note="Nguồn: Calendar list r40-r42."),

    tc("Wizard tạo calendar", "UI-INPUT-001", "Normal",
       "Số tiền course ở popup tạo đầu — default 0 và format dấu phẩy",
       ADM + "\n- Đang ở popup tạo course",
       "1. Quan sát giá trị mặc định ô số tiền\n2. Nhập 1000\n3. Rời khỏi ô",
       "1000",
       "- Default: 0 yên\n- Sau khi nhập 1000 và blur: hiển thị「1,000」(có dấu phẩy ngăn cách nghìn)",
       note="Nguồn: Calendar list r43-r44."),

    tc("Wizard tạo calendar", "FUNC-001", "Normal",
       "Lưu course đầu → chuyển sang màn quản lý calendar",
       ADM + "\n- Đang ở popup tạo course, đã nhập data hợp lệ",
       "1. Bấm Lưu",
       "Tên course「初心者向けトレーニング」· 1h00 · 5000 yên",
       "- Lưu thành công, redirect sang màn hình quản lý calendar (tab 予約カレンダー)\n"
       "- DB `calendar_course` có 1 bản ghi mới với booking_page_display = 1",
       note="Nguồn: Calendar list r45 + spec BR-09."),

    # ══════════════════ 3. Giới hạn theo plan ══════════════════
    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan free: bộ đếm hiện 0/1, tạo calendar thứ 2 bị chặn",
       "- Bot B gói **free**, chưa có lesson calendar nào\n- Đăng nhập admin bot B",
       "1. Mở /basic/calendar-management → quan sát bộ đếm\n2. Tạo calendar thứ 1 → thành công\n"
       "3. Bấm 新規作成 để tạo calendar thứ 2",
       "Bot free",
       "- Bước 1: bộ đếm hiển thị「0/1」\n"
       "- Bước 3: báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- DB: `calendar_management` của bot B chỉ có 1 bản ghi",
       note="Nguồn: Calendar list r8-r9. Khớp spec BR-01 (free = 1) và BR-02 (2 loại message)."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan standard (bot_contract_new = 0): bộ đếm 0/3, tạo cái thứ 4 bị chặn",
       "- Bot C gói **standard**, `bots.flag_contract_new` = 0, chưa có lesson calendar",
       "1. Quan sát bộ đếm\n2. Tạo lần lượt 3 calendar\n3. Bấm 新規作成 để tạo calendar thứ 4",
       "Bot standard hợp đồng cũ",
       "- Bước 1: bộ đếm「0/3」\n"
       "- Bước 3: báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」",
       note="Nguồn: Calendar list r10-r11. 🔴 MÂU THUẪN với spec BR-01 (standard CŨ = 10, standard MỚI = 3). "
            "Xem MT-05."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan standard (bot_contract_new = 1): tạo calendar thứ 4 bị chặn",
       "- Bot D gói **standard**, `bots.flag_contract_new` = 1, đã có 3 lesson calendar",
       "1. Bấm 新規作成 để tạo calendar thứ 4",
       "Bot standard hợp đồng mới",
       "- Báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- Không tạo được bản ghi thứ 4",
       note="Nguồn: Calendar list r12. Khớp spec BR-01 nhánh standard mới = 3."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan pro: bộ đếm 0/10, tạo cái thứ 11 báo message KHÁC plan free",
       "- Bot E gói **pro**, đã có 10 lesson calendar",
       "1. Quan sát bộ đếm\n2. Bấm 新規作成 để tạo calendar thứ 11",
       "Bot pro, 10 calendar sẵn có",
       "- Bộ đếm「10/10」(khi chưa có calendar nào thì hiện「0/10」)\n"
       "- Báo lỗi「上限に達したので、新しく追加できません。」— KHÁC message của plan free",
       note="Nguồn: Calendar list r13-r14. Khớp spec BR-02 (2 message khác nhau theo gói)."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan enterprise (standard) và enterprise (pro): bộ đếm đều 0/10",
       "- Bot F gói enterprise nền standard · Bot G gói enterprise nền pro",
       "1. Đăng nhập bot F → quan sát bộ đếm\n2. Đăng nhập bot G → quan sát bộ đếm",
       "2 bot enterprise",
       "- Cả 2 bot đều hiển thị bộ đếm「0/10」",
       note="Nguồn: Calendar list r15-r16. 🔴 MÂU THUẪN spec BR-01 (enterprise = 3, enterprise_pro = 10). "
            "Xem MT-05."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan free: giới hạn 2 course/lịch — kể cả khi 1 hoặc cả 2 course đang OFF",
       "- Bot B gói free, đã có 1 lesson calendar với 2 course",
       "1. Cả 2 course đang ON → bấm コース作成\n"
       "2. Tắt 1 course về OFF → bấm コース作成\n3. Tắt cả 2 course về OFF → bấm コース作成",
       "Bot free, 2 course",
       "- Cả 3 bước đều báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- ⇒ Bộ đếm course tính CẢ course đang OFF",
       note="Nguồn: Quản lý course r20-r22 (3 state ON/OFF, mỗi state 1 TC riêng theo quy tắc tách TC)."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Plan standard / pro: TC gốc nói không giới hạn số course — cần verify trần cứng 200",
       "- Bot C gói standard, đã có 1 lesson calendar với 5 course",
       "1. Tạo thêm course cho tới khi đạt 200 course\n2. Tạo course thứ 201",
       "200 course trên 1 calendar",
       "- Tạo được tới course thứ 200\n- Course thứ 201: bị chặn (theo spec BR-04, trần cứng 200/lịch)",
       spec="Đã hỏi leader",
       note="🔴 TC gốc「Quản lý course」r23-r24 ghi「plan standard/pro: KHÔNG giới hạn course」— "
            "MÂU THUẪN spec BR-04 (trần cứng 200). TC này viết theo SPEC, DỰ KIẾN có thể FAIL nếu hệ thống "
            "thật sự không giới hạn ⇒ khi đó phải raise bug hoặc sửa spec. Xem MT-06."),

    tc("Giới hạn theo plan", "FUNC-004", "Boundary",
       "Giới hạn 100 câu hỏi form / 1 lịch",
       CAL,
       "1. Vào 全体設定 > 予約時のお客様への質問項目\n"
       "2. Tạo câu hỏi cho đến khi đủ 100 (gồm 2 câu mặc định họ tên + email)\n"
       "3. Tạo câu hỏi thứ 101",
       "100 câu hỏi",
       "- Tạo được tới câu 100\n- Câu 101: bị chặn, có message báo đã đạt giới hạn",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-05 — corpus KHÔNG có TC nào cho giới hạn 100 câu hỏi (GAP). "
            "Cần Leader xác nhận message hiển thị."),

    # ══════════════════ 4. コース — list & hiển thị ══════════════════
    tc("コース — list & hiển thị", "UI-001", "Normal",
       "Tab コース設定 hiển thị đúng nhãn và các cột dữ liệu của course",
       CAL + "\n- Course「初心者向けトレーニング」có ảnh, giá 6.000 yên, thời lượng 1h00",
       "1. Mở màn quản lý calendar → chọn tab コース設定\n2. Quan sát dòng course",
       "1 course có đủ ảnh + giá + thời lượng",
       "- Tên tab đúng「コース設定」\n- Cột イメージ: hiện ảnh đã upload\n"
       "- Cột コース名: hiện tên course\n- Cột 料金: hiện「¥ 6,000」\n"
       "- Cột 基本所要時間: hiện「01時間00分」",
       note="Nguồn: Quản lý course r4-r5, r8, r10."),

    tc("コース — list & hiển thị", "UI-001", "Normal",
       "Course không có ảnh → hiện ảnh default; course không setting giá → hiện 設定なし",
       CAL + "\n- Course C2 KHÔNG upload ảnh và KHÔNG nhập số tiền",
       "1. Mở tab コース設定\n2. Quan sát dòng course C2",
       "Course không ảnh, không giá",
       "- Cột イメージ hiện ảnh mặc định của hệ thống (không vỡ ảnh, không rỗng)\n"
       "- Cột 料金 hiện text「設定なし」(không hiện ¥ 0)",
       note="Nguồn: Quản lý course r6, r9."),

    tc("コース — list & hiển thị", "FUNC-001", "Normal",
       "Bấm tên course → mở màn detail course tương ứng",
       CAL + "\n- Có 2 course C1, C2",
       "1. Mở tab コース設定\n2. Đưa chuột lên tên course C2 (kiểm mouse over)\n3. Bấm vào tên C2",
       "2 course",
       "- Mouse over: con trỏ đổi thành pointer / có hiệu ứng hover\n"
       "- Bấm: mở /basic/calendar-management/{id}/edit-course/{id C2}, hiện đúng data của C2",
       note="Nguồn: Quản lý course r11."),

    tc("コース — list & hiển thị", "LIST-001", "Normal",
       "Drag&drop sắp xếp course → thứ tự đồng bộ ở 9 màn admin + màn LINE user",
       CAL + "\n- Calendar có 3 course C1, C2, C3 (thứ tự C1→C2→C3), tất cả ON, mỗi course có ≥1 slot",
       "1. Tab コース設定 → kéo C3 lên đầu\n"
       "2. Kiểm thứ tự lần lượt tại: tab コース設定 · quản lý theo ngày · theo tuần · theo tháng · "
       "theo list · modal add slot · modal edit slot · modal quản lý CSV · modal filter theo course\n"
       "3. Mở trang booking bên LINE user",
       "3 course",
       "- Cả 9 màn admin ở bước 2 đều hiện thứ tự C3, C1, C2\n"
       "- Màn chọn course phía LINE user cũng hiện thứ tự C3, C1, C2",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r14-r15 (gộp 1 TC vì CÙNG kết quả cho 9 điểm hiển thị; "
            "liệt kê đủ 9 điểm ở cột Các bước). RULE-06: verify tới output cuối là màn LINE user."),

    tc("コース — list & hiển thị", "LIST-001", "Normal",
       "List course nhiều → có scroll và hiện đủ",
       CAL + "\n- Calendar có 30 course",
       "1. Mở tab コース設定\n2. Cuộn xuống cuối danh sách",
       "30 course",
       "- Hiện đủ 30 course, có thanh cuộn\n- Course cuối cùng hiển thị đầy đủ, không bị cắt",
       note="Nguồn: Quản lý course r18."),

    tc("コース — list & hiển thị", "STATE-001", "Normal",
       "Course ON → hiện ở đủ 12 điểm (9 màn admin + 3 màn LINE user)",
       CAL + "\n- Course C1 đang ON, có slot trong tuần hiện tại và đã có 1 booking",
       "1. Bật C1 = ON\n"
       "2. Kiểm C1 có hiện tại: Today&NewBooking · quản lý theo ngày · tuần · tháng · list · "
       "modal detail lịch sử booking · màn booking đã xóa · modal booking mới · export CSV · "
       "modal filter ở màn quản lý theo list\n"
       "3. Phía LINE user: màn booking mới · màn lịch sử book · chức năng copy booking",
       "1 course ON",
       "- Toàn bộ 10 điểm phía admin ở bước 2 đều HIỆN course C1\n"
       "- Cả 3 điểm phía LINE user ở bước 3 đều HIỆN course C1",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r200-r212 (13 dòng cùng kết quả「Có hiện course」→ gộp 1 TC, "
            "liệt kê đủ điểm ở cột Các bước). Feature #27496."),

    tc("コース — list & hiển thị", "STATE-001", "Abnormal",
       "Course OFF → VẪN hiện ở màn quản lý & lịch sử admin (7 điểm)",
       CAL + "\n- Course C1 đã có booking, sau đó admin tắt C1 = OFF",
       "1. Tắt C1 = OFF\n"
       "2. Kiểm C1 tại: Today&NewBooking tab 新着の予約 · tab 本日の予約 · quản lý theo ngày · tuần · "
       "tháng · list · modal detail lịch sử booking · màn booking đã xóa · modal filter màn list",
       "1 course OFF, có booking cũ",
       "- Cả 9 điểm trên đều VẪN HIỆN course C1 (để admin còn xem được lịch sử)",
       note="Nguồn: Quản lý course r213-r220, r223 (9 dòng cùng kết quả). Feature #27496: "
            "OFF course thì lịch sử vẫn hiển thị."),

    tc("コース — list & hiển thị", "STATE-001", "Abnormal",
       "Course OFF → KHÔNG hiện ở modal booking mới, export CSV và màn booking của LINE user",
       CAL + "\n- Course C1 đã OFF",
       "1. Mở modal 予約追加 (admin thêm booking) → xem droplist course\n"
       "2. Mở modal quản lý CSV → xem list course để export\n"
       "3. LINE user mở trang booking mới → xem danh sách course",
       "1 course OFF",
       "- Bước 1: KHÔNG có C1 trong droplist\n"
       "- Bước 2: KHÔNG có C1 trong list export\n"
       "- Bước 3: LINE user KHÔNG thấy C1 ở màn chọn course",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r221-r222, r224 (3 dòng cùng kết quả「Không hiện」)."),

    tc("コース — list & hiển thị", "STATE-001", "Normal",
       "Course OFF → LINE user vẫn thấy booking cũ ở lịch sử nhưng KHÔNG copy được",
       CAL + "\n- LINE user U1 đã booking course C1, sau đó admin tắt C1 = OFF",
       "1. U1 mở màn lịch sử booking\n2. U1 bấm nút 同じ内容で予約 (copy booking) trên booking của C1",
       "1 booking của course đã OFF",
       "- Bước 1: booking của C1 VẪN hiện trong lịch sử\n"
       "- Bước 2: bấm copy thì báo lỗi (không cho đặt lại course đã OFF)",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r225-r226. ⚠️ MÂU THUẪN với「Booking phía line user」r62 nói "
            "「Booking đã bị OFF course → ko hiển thị ở mh history nữa」. Xem MT-07."),
]
