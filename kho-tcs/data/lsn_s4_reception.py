# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm 受付枠 (khung nhận đặt): thêm / sửa 定員 / xóa / xóa nhiều / CSV.

Nguồn chính: 11.2 TCsLine_LessonCalendar
  - tab「Quản lý calendar_new」r267-r342 (modal add slot + modal edit slot), r477-r524 (CSV),
    r997-r1051 (xóa nhiều slot — khối chỉ có ở bản _new, khớp spec BR-17)
  - tab「Quản lý calendar」r299-r330 (modal add slot bản cũ), r464-r523 (CSV bản cũ)
  - tab「Task nhỏ + fix bug KH」r51-r109 (Support #29830 — nhập 24h), r187-r199 (Bug KH #35173 —
    add slot lệch ngày, 03/2026 — KHỐI MỚI NHẤT của nhóm này)
Spec: BR-11…BR-19 (khung nhận đặt), EP-51 (import CSV).
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, có course C1「初心者」thời lượng 1h30\n"
       "- Mở /basic/calendar-management/21 > tab 予約カレンダー")

S4 = [
    # ══════════════════ Modal add slot ══════════════════
    tc("受付枠 — thêm khung giờ", "UI-001", "Normal",
       "Droplist course ở modal add slot: chỉ course ON, đúng thứ tự, default KHÔNG chọn sẵn",
       CAL + "\n- Có 4 course: C1, C2, C3 đang ON và C4 đang OFF, thứ tự ở màn quản lý course là C2→C1→C3",
       "1. Bấm「受付枠追加」→ mở modal add slot\n2. Mở droplist course",
       "3 course ON + 1 OFF",
       "- Droplist chỉ hiện C2, C1, C3 — KHÔNG hiện C4 (OFF)\n"
       "- Thứ tự giống màn quản lý course: C2 → C1 → C3\n"
       "- Default KHÔNG select course nào, hiện placeholder「コースを選択してください」",
       note="Nguồn: Quản lý calendar_new r268. 🔴 MÂU THUẪN tab「Quản lý calendar」r301 nói "
            "「Default select course đầu tiên」. Xem MT-11 — đã lấy theo bản _new vì có validate "
            "「コースを選択してください」đi kèm."),

    tc("受付枠 — thêm khung giờ", "FUNC-002", "Normal",
       "Add / sửa / xóa course rồi mở lại modal add slot → droplist cập nhật",
       CAL + "\n- Đang có 3 course ON",
       "1. Mở modal add slot, ghi nhận droplist\n2. Đóng modal, thêm course C5\n"
       "3. Mở lại modal → kiểm droplist\n4. Đổi tên C1 → mở lại modal\n5. Xóa C3 → mở lại modal",
       "3 → 4 → 3 course",
       "- Bước 3: droplist có thêm C5\n- Bước 4: droplist hiện tên mới của C1\n"
       "- Bước 5: droplist không còn C3",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r270 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("受付枠 — thêm khung giờ", "FUNC-002", "Abnormal",
       "Calendar chọn ngày: KHÔNG cho chọn ngày quá khứ",
       CAL,
       "1. Mở modal add slot → phần「受付枠を追加したい日程を選択」chọn kiểu カレンダーから選択\n"
       "2. Quan sát tháng mặc định\n3. Thử bấm 1 ngày trong quá khứ\n4. Bấm next/previous tháng",
       "—",
       "- Default hiển thị tháng hiện tại\n- Ngày quá khứ bị disable, không bấm chọn được\n"
       "- Next/previous tháng hoạt động bình thường",
       note="Nguồn: Quản lý calendar_new r271. Spec BR-16: chế độ chọn ngày cụ thể "
            "「không kiểm quá khứ, không kiểm giới hạn 1 năm」ở tầng SERVER — xem MT-14."),

    tc("受付枠 — thêm khung giờ", "FUNC-002", "Abnormal",
       "Không chọn course / không chọn ngày → validate riêng từng message",
       CAL,
       "1. Mở modal add slot, không chọn course, không chọn ngày → bấm Lưu\n"
       "2. Chọn course, vẫn không chọn ngày → bấm Lưu",
       "—",
       "- Bước 1: báo lỗi「コースを選択してください」\n"
       "- Bước 2: báo lỗi「日程を選択してください」\n- Cả 2 bước đều KHÔNG tạo bản ghi `calendar_course_receptions`",
       note="Nguồn: Quản lý calendar_new r275, r301-r302. 🔴 MÂU THUẪN tab「Quản lý calendar」r327 "
            "nói「Không có case này vì default luôn chọn course đầu tiên」và r328 chỉ ghi "
            "「Báo lỗi invalid」chung chung. Xem MT-11."),

    tc("受付枠 — thêm khung giờ", "FUNC-001", "Normal",
       "Default time khi chưa chọn course và sau khi chọn course",
       CAL + "\n- Course C1 thời lượng 1h30",
       "1. Mở modal add slot, CHƯA chọn course → quan sát khối time\n"
       "2. Chọn course C1 → quan sát lại\n3. Đổi sang course C2 (2h00) → quan sát",
       "C1 = 1h30, C2 = 2h00",
       "- Bước 1: checkbox「設定済みの所要時間とは異なるの時間を設定」KHÔNG tích; "
       "start_time = --:--, end_time = --:--, 定員 =「設定しない」\n"
       "- Bước 2: start_time = 0:00, end_time = 1:30 (start + thời lượng course)\n"
       "- Bước 3: end_time đổi thành 2:00",
       note="Nguồn: Quản lý calendar_new r276-r278."),

    tc("受付枠 — thêm khung giờ", "UI-FIELD-001", "Normal",
       "Checkbox 設定済みの所要時間とは異なるの時間を設定 điều khiển ô end time",
       CAL + "\n- Đã chọn course C1 (1h30)",
       "1. Quan sát ô end time khi checkbox chưa tích\n2. Tích checkbox → quan sát",
       "—",
       "- Chưa tích: ô end time bị DISABLE và tự set = start + thời lượng course\n"
       "- Đã tích: ô end time được ENABLE, sửa tay được",
       note="Nguồn: Quản lý calendar_new r279-r280."),

    tc("受付枠 — thêm khung giờ", "FUNC-004", "Boundary",
       "Nhập time: biên 00:00 ~ 23:59 và các quan hệ start/end",
       CAL + "\n- Đã tích checkbox cho phép nhập end time",
       "1. Nhập 00:00 ~ 23:59 → Lưu\n2. Nhập 09:00 ~ 10:00 → Lưu\n"
       "3. Nhập start = end (10:00 ~ 10:00) → Lưu\n4. Nhập start > end (10:00 ~ 09:00) → Lưu",
       "4 cặp giá trị",
       "- Bước 1, 2: Add success\n- Bước 3: Invalid\n"
       "- Bước 4: Invalid, báo lỗi「開始時間は終了時間よりも前の時間を設定して下さい」",
       note="Nguồn: Quản lý calendar_new r281-r284."),

    tc("受付枠 — thêm khung giờ", "FUNC-UNIQ-001", "Abnormal",
       "Trùng khung giờ với slot đã có — CHỌN 1 NGÀY → bỏ qua im lặng, KHÔNG báo lỗi",
       CAL + "\n- Đã có slot của C1 ngày 20/10, 09:00-10:30",
       "1. Mở modal add slot, chọn C1, chọn đúng ngày 20/10, nhập 09:00-10:30 → Lưu\n"
       "2. Query `calendar_course_receptions` của C1 ngày 20/10",
       "Trùng hoàn toàn (course + ngày + start + end)",
       "- KHÔNG hiện message báo lỗi\n- KHÔNG tạo bản ghi mới, DB vẫn chỉ có 1 slot 09:00-10:30",
       note="Nguồn: Quản lý calendar_new r287 + khớp spec BR-15 (「trùng thì bỏ qua im lặng, "
            "không lỗi」). 🔴 MÂU THUẪN tab「Quản lý calendar」r324 nói「Báo lỗi すでに存在しています。」— "
            "đã lấy theo bản _new vì khớp spec. Xem MT-15."),

    tc("受付枠 — thêm khung giờ", "FUNC-UNIQ-001", "Normal",
       "Trùng khung giờ — CHỌN NHIỀU NGÀY → bỏ qua ngày đã có, insert ngày chưa có",
       CAL + "\n- Đã có slot C1 ngày 20/10, 09:00-10:30",
       "1. Chọn C1, chọn 3 ngày 20/10 + 21/10 + 22/10, nhập 09:00-10:30 → Lưu\n"
       "2. Query `calendar_course_receptions` của C1",
       "3 ngày, 1 ngày đã tồn tại",
       "- Sau khi lưu có ĐÚNG 3 bản ghi (20/10 giữ nguyên bản cũ, thêm mới 21/10 và 22/10)\n"
       "- Không có bản ghi trùng lặp ở ngày 20/10",
       note="Nguồn: Quản lý calendar_new r288, Quản lý calendar r325 (2 tab NHẤT QUÁN ở case này)."),

    tc("受付枠 — thêm khung giờ", "FUNC-UNIQ-001", "Normal",
       "Cùng start khác end / cùng end khác start → được phép thêm",
       CAL + "\n- Đã có slot C1 ngày 20/10, 09:00-10:30",
       "1. Thêm slot C1 ngày 20/10, 09:00-11:00 → Lưu\n"
       "2. Thêm slot C1 ngày 20/10, 08:00-10:30 → Lưu\n3. Query DB",
       "2 slot khác biên",
       "- Cả 2 đều Add success\n- DB có 3 bản ghi cho C1 ngày 20/10",
       note="Nguồn: Quản lý calendar_new r285-r286."),

    tc("受付枠 — thêm khung giờ", "FUNC-MULTI-001", "Normal",
       "Nhập nhiều khoảng time trong 1 lần: thêm, xóa, không cho xóa hết",
       CAL,
       "1. Bấm「＋受付時間を追加」3 lần → quan sát\n2. Bấm icon xóa ở khoảng time thứ 3\n"
       "3. Xóa tiếp cho tới khi còn 1 khoảng\n4. Thử xóa khoảng cuối cùng\n"
       "5. Bấm 「＋受付時間を追加」nhưng KHÔNG nhập time rồi bấm Lưu",
       "—",
       "- Bước 1: có 4 khoảng time, cuộn được khi nhiều\n- Bước 2: xóa đúng khoảng đó\n"
       "- Bước 4: khoảng đầu tiên KHÔNG có icon xóa ⇒ không xóa hết được\n"
       "- Bước 5: khoảng trống tự động bị bỏ qua khi lưu, không tạo bản ghi rỗng",
       note="Nguồn: Quản lý calendar_new r299-r300, r303-r304."),

    tc("受付枠 — thêm khung giờ", "FUNC-MULTI-001", "Normal",
       "Tạo nhiều khoảng time hợp lệ trong 1 lần lưu",
       CAL,
       "1. Chọn C1, chọn ngày 20/10\n"
       "2. Nhập 4 khoảng: 00:00~1:40 · 1:41~3:59 · 4:00~5:00 · 23:00~23:59 → Lưu\n"
       "3. Query DB",
       "4 khoảng time không chồng nhau",
       "- Tạo đủ 4 bản ghi `calendar_course_receptions` cho ngày 20/10",
       note="Nguồn: Quản lý calendar_new r294-r295 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("受付枠 — thêm khung giờ", "FUNC-UNIQ-001", "Abnormal",
       "Nhập 2 khoảng time GIỐNG HỆT trong cùng 1 lần lưu → chỉ ghi nhận khoảng đầu",
       CAL,
       "1. Chọn C1, chọn ngày 20/10\n"
       "2. Nhập khoảng 1: 1:00-2:00 定員 2; khoảng 2: 1:00-2:00 定員 10 → Lưu\n"
       "3. Query DB",
       "2 khoảng trùng, 定員 khác nhau",
       "- Chỉ tạo 1 bản ghi với `total_person` = 2 (ghi nhận khoảng ĐẦU TIÊN)",
       note="Nguồn: Quản lý calendar_new r297."),

    tc("受付枠 — thêm khung giờ", "FUNC-UNIQ-001", "Normal",
       "Nhập nhiều khoảng, trong đó có khoảng đã tồn tại trong DB → skip cái đã có",
       CAL + "\n- Đã có slot C1 ngày 20/10, 11:20-13:20",
       "1. Nhập 2 khoảng: 9:00-10:00 (chưa có) và 11:20-13:20 (đã có) → Lưu\n2. Query DB",
       "2 khoảng, 1 đã tồn tại",
       "- Chỉ thêm mới 9:00-10:00\n- Khoảng 11:20-13:20 bị skip, DB không nhân đôi",
       note="Nguồn: Quản lý calendar_new r298."),

    tc("受付枠 — thêm khung giờ", "UI-FIELD-001", "Normal",
       "定員: default 設定しない, chọn giới hạn thì default 1",
       CAL,
       "1. Mở modal add slot → quan sát khối 定員\n2. Chọn option có giới hạn → quan sát ô nhập",
       "—",
       "- Default: chọn「設定しない」và ô nhập số bị DISABLE\n"
       "- Chọn có giới hạn: ô nhập enable, giá trị mặc định = 1",
       note="Nguồn: Quản lý calendar_new r289-r290."),

    tc("受付枠 — thêm khung giờ", "FUNC-003", "Abnormal",
       "定員: nhập số âm / không phải số → Invalid",
       CAL + "\n- Đã chọn option có giới hạn",
       "1. Nhập -1 → Lưu\n2. Nhập「abc」→ Lưu\n3. Nhập 0 và để trống → Lưu",
       "-1 · abc · 0 · rỗng",
       "- -1 và abc: Invalid, không lưu\n"
       "- 0 và rỗng: cần chốt hành vi — TC gốc chỉ ghi tiêu đề, chưa có kết quả",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar_new r291-r293. ⚠️ r291「Check chọn set max và nhập 0, để trống」"
            "KHÔNG có kết quả mong đợi. Xem MT-17."),

    tc("受付枠 — thêm khung giờ", "CONC-001", "Abnormal",
       "Double click nút 保存する ở modal add slot → chỉ tạo 1 bộ slot",
       CAL,
       "1. Chọn course, chọn 1 ngày, nhập 1 khoảng time hợp lệ\n"
       "2. Double click nhanh (<300ms) nút「保存する」\n3. Query `calendar_course_receptions`",
       "1 course × 1 ngày × 1 khoảng",
       "- Chỉ tạo ĐÚNG 1 bản ghi, không tạo 2 bản trùng",
       note="Nguồn: Quản lý calendar_new r308, Quản lý calendar r326."),

    tc("受付枠 — thêm khung giờ", "FUNC-001", "Normal",
       "Bấm icon X ở modal add slot → đóng và không tạo",
       CAL,
       "1. Nhập đầy đủ data hợp lệ\n2. Bấm icon X",
       "Data hợp lệ chưa lưu",
       "- Đóng modal, KHÔNG tạo bản ghi `calendar_course_receptions`",
       note="Nguồn: Quản lý calendar_new r309."),

    # ══════════════════ Bug KH #35173 — add slot lệch ngày ══════════════════
    tc("受付枠 — thêm khung giờ", "FUNC-DATE-001", "Normal",
       "Bug KH #35173: add slot CHỌN NGÀY → slot hiện đúng ngày và giờ đã setting",
       CAL + "\n- Course C1 thời lượng 1h30",
       "1. Mở modal add slot, chọn kiểu カレンダーから選択, chọn ĐÚNG 1 ngày (ví dụ 19/03)\n"
       "2. Nhập khoảng 10:00~11:30 → Lưu\n3. Lặp với 13:00~14:30 và 14:00~15:30\n"
       "4. Kiểm slot ở màn quản lý theo ngày và theo tháng",
       "3 khoảng, ngày 19/03",
       "- Cả 3 slot đều được tạo\n"
       "- Slot hiện ĐÚNG ngày 19/03 (KHÔNG bị lệch sang 18/03) và đúng khung giờ đã nhập",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r188-r190 (Bug KH #35173, 03/2026). ⚠️ Bug này CHƯA TÁI HIỆN "
            "ĐƯỢC — fix chỉ là thêm log. PRODUCTION vì liên quan timezone server thật."),

    tc("受付枠 — thêm khung giờ", "DATA-001", "Normal",
       "Bug KH #35173: add slot liên tiếp nhiều đợt (1 ngày rồi nhiều ngày, khác tháng)",
       CAL,
       "1. Add slot cho tháng 3: chọn 1 ngày → Lưu\n"
       "2. Add tiếp slot cho tháng 4: chọn NHIỀU ngày → Lưu\n"
       "3. Kiểm toàn bộ slot ở màn tháng 3 và tháng 4",
       "2 đợt add liên tiếp",
       "- Toàn bộ slot của cả 2 đợt hiện đúng ngày và giờ đã setting, không lệch ngày",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r191."),

    tc("受付枠 — thêm khung giờ", "FUNC-DATE-001", "Normal",
       "Bug KH #35173: add slot theo THỨ trong tuần → slot hiện đúng ngày và giờ",
       CAL,
       "1. Mở modal add slot, chọn kiểu 曜日から選択\n2. Chọn 1 thứ (thứ 4), nhập 10:00~11:30, "
       "đặt ngày hết hạn lặp → Lưu\n3. Lặp với 13:00~14:30 và 14:00~15:30\n"
       "4. Add tiếp cho các thứ khác\n5. Kiểm slot ở màn tháng",
       "Add theo thứ, nhiều đợt",
       "- Slot được tạo ở đúng các ngày rơi vào thứ đã chọn, đúng khung giờ, không lệch ngày",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r192-r195."),

    tc("受付枠 — thêm khung giờ", "FUNC-002", "Abnormal",
       "Add slot theo THỨ: validate ngày hết hạn lặp — quá khứ và quá 1 năm",
       CAL,
       "1. Chọn kiểu 曜日から選択, chọn thứ 4\n2. Đặt ngày hết hạn lặp = hôm qua → Lưu\n"
       "3. Đặt ngày hết hạn lặp = hôm nay + 13 tháng → Lưu\n"
       "4. Đặt ngày hết hạn lặp = hôm nay + 6 tháng → Lưu\n5. Không chọn thứ nào → Lưu",
       "4 giá trị ngày hết hạn + 1 case không chọn thứ",
       "- Bước 2: Invalid (không cho ngày quá khứ)\n- Bước 3: Invalid (vượt giới hạn 1 năm)\n"
       "- Bước 4: Add success\n- Bước 5: Invalid (phải chọn ít nhất 1 thứ)",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-11/BR-12/BR-13 — corpus lesson KHÔNG có TC validate "
            "ngày hết hạn lặp (chỉ có ở Feature #27978 r1585-r1588 dạng tiêu đề). Cần Leader xác nhận."),

    # ══════════════════ Support #29830 — nhập 24h ══════════════════
    tc("受付枠 — thêm khung giờ", "FUNC-DATE-001", "Boundary",
       "Support #29830: cho phép end time = 00:00 (nghĩa là 24:00)",
       CAL,
       "Add slot với từng cặp giá trị, ghi kết quả:\n"
       "1. 00:00 ~ 00:00\n2. 00:00 ~ 02:00\n3. 02:00 ~ 00:00\n4. 02:00 ~ 03:00\n5. 02:00 ~ 01:00",
       "5 cặp start/end",
       "- Case 1, 2, 3, 4: cho phép add slot\n"
       "- Case 5: báo lỗi, không cho start time > end time",
       note="Nguồn: Task nhỏ + fix bug KH r96-r100 (Support #29830 05/2025). Đã đối chiếu TC add slot "
            "trên app mobile — cùng bộ giá trị."),

    tc("受付枠 — thêm khung giờ", "UI-003", "Normal",
       "Support #29830: slot end time 00:00 hiển thị là 24:00 ở app mobile",
       CAL + "\n- Đã có slot 23:00 ~ 00:00\n- Có app mobile admin đã đăng nhập bot A",
       "Trên APP MOBILE, kiểm hiển thị slot 23:00~00:00 tại:\n"
       "1. Màn calendar (list slot)\n2. Modal detail của 1 slot\n3. Màn edit slot\n"
       "4. Modal add booking mới",
       "1 slot 23:00-00:00",
       "- Cả 4 màn đều hiển thị「23:00 - 24:00」(KHÔNG hiển thị 23:00 - 00:00)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r101-r104."),

    tc("受付枠 — thêm khung giờ", "UI-003", "Normal",
       "Support #29830: booking end time 00:00 hiển thị 24:00 ở app mobile (4 màn)",
       CAL + "\n- Có booking ở slot 23:00-00:00 của LINE user U1",
       "Trên APP MOBILE kiểm hiển thị booking tại:\n"
       "1. Màn calendar lesson → list booking\n2. Detail booking\n3. Lịch sử book\n"
       "4. Màn notify → list notify\n5. Detail booking mở từ notify",
       "1 booking 23:00-00:00",
       "- Cả 5 màn đều hiển thị booking「23:00 - 24:00」",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r105-r109."),

    tc("受付枠 — thêm khung giờ", "MSG-002", "Normal",
       "Support #29830: mã [LESSON_CALENDAR_date_time] thay đúng khung giờ 24h trong action",
       CAL + "\n- Slot 23:00-00:00; message action booking có chèn mã [LESSON_CALENDAR_date_time]",
       "1. U1 booking slot 23:00-00:00 (case approve luôn)\n2. Kiểm tin LINE U1 nhận\n"
       "3. Lặp với: case request booking · admin approve · admin deny · message của course · "
       "message khi cancel (4 nhánh) · message remind",
       "1 slot 23:00-00:00, nhiều loại action",
       "- Mọi loại tin nhắn đều thay mã thành khung giờ đúng dạng「23:00 - 24:00」",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Task nhỏ + fix bug KH r84-r94 — TC gốc CHỈ CÓ TIÊU ĐỀ (11 dòng), "
            "kết quả mong đợi do AI gộp và bổ sung. Cần Leader xác nhận."),

    tc("受付枠 — thêm khung giờ", "OUT-EXPORT-001", "Normal",
       "Support #29830: export CSV booking của slot 24h → tên file và tên sheet đúng khung giờ",
       CAL + "\n- Slot 23:00-00:00 có 2 booking",
       "1. Mở modal danh sách booking của slot\n2. Bấm nút CSV → tải file\n"
       "3. Mở file, kiểm tên file và tên sheet",
       "1 slot 23:00-00:00",
       "- Tên file và tên sheet chứa khung giờ hiển thị đúng (23:00~24:00), không phải 23:00~00:00",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r73."),

    # ══════════════════ Modal edit slot ══════════════════
    tc("受付枠 — sửa 定員 & xóa", "UI-001", "Normal",
       "Modal detail slot: dữ liệu hiển thị và 2 nhánh giới hạn/không giới hạn",
       CAL + "\n- Slot S1 của C1 setting KHÔNG giới hạn; slot S2 setting giới hạn 5 người\n"
             "- Calendar KHÔNG setting thời gian bắt đầu nhận booking",
       "1. Mở modal edit slot của S1 → quan sát\n2. Mở của S2 → quan sát\n"
       "3. Bấm link「受付期限の変更はこちら」",
       "2 slot khác kiểu giới hạn",
       "- Cả 2: hiện ảnh course, tên course, thời gian thực hiện\n"
       "- S1: hiện「上限なし」· S2: hiện「5人」\n"
       "- Thời gian start nhận booking: hiện「設定されていません」\n"
       "- Thời gian dừng nhận: hiện「<time start course>まで 予約できます」\n"
       "- Bước 3: redirect sang màn setting dừng nhận booking",
       note="Nguồn: Quản lý calendar_new r314-r324."),

    tc("受付枠 — sửa 定員 & xóa", "FUNC-002", "Normal",
       "Edit 定員 — slot chưa có booking hoặc chỉ có booking không phải approve",
       CAL + "\n- Slot S1 chưa có booking; slot S2 có 1 booking cancel + 1 booking request",
       "1. Sửa 定員 của S1 từ 5 → 10 → Lưu, query `calendar_course_receptions.total_person`\n"
       "2. Sửa 定員 của S1 = 0 → Lưu, query\n3. Lặp bước 1-2 với slot S2",
       "2 slot, 定員 mới 10 và 0",
       "- Cả 4 lần đều Edit success, `total_person` cập nhật đúng giá trị mới (10 và 0)",
       note="Nguồn: Quản lý calendar_new r327-r330."),

    tc("受付枠 — sửa 定員 & xóa", "FUNC-004", "Boundary",
       "Edit 定員 khi slot ĐÃ CÓ booking approve — 3 biên so với số approve",
       CAL + "\n- Slot S3 定員 5, hiện có 3 booking status 予約確定 (approve)",
       "1. Sửa 定員 = 3 (bằng số approve) → Lưu\n2. Sửa 定員 = 7 (lớn hơn) → Lưu\n"
       "3. Sửa 定員 = 2 (nhỏ hơn) → Lưu",
       "定員 3 / 7 / 2 với 3 booking approve",
       "- 定員 = 3: Edit success\n- 定員 = 7: Edit success\n"
       "- 定員 = 2: báo lỗi「入力した受付上限数が、「ステータス：予約確定」の人数を下回っています。"
       "予約上限数を減らしたい場合、確定してる予約をキャンセルして、受付上限数 >「ステータス：予約確定」"
       "の人数となるように変更してください。」và KHÔNG lưu",
       note="Nguồn: Quản lý calendar_new r331-r333. So sánh với `total_approve`, KHÔNG tính "
            "booking đang request cancel."),

    tc("受付枠 — sửa 定員 & xóa", "FUNC-003", "Abnormal",
       "Edit 定員: validate không nhập / số âm / số thực / ký tự",
       CAL + "\n- Slot S1 定員 5",
       "1. Xóa trống ô 定員 → Lưu\n2. Nhập -1 → Lưu\n3. Nhập 2.5 → Lưu\n4. Nhập「abc」→ Lưu",
       "rỗng · -1 · 2.5 · abc",
       "- Cả 4 trường hợp: Invalid, không lưu, `total_person` giữ giá trị cũ",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r334 — TC gốc chỉ có tiêu đề liệt kê 4 input, "
            "kết quả mong đợi do AI bổ sung."),

    tc("受付枠 — sửa 定員 & xóa", "FUNC-002", "Normal",
       "Edit từ không giới hạn ⇄ có giới hạn",
       CAL + "\n- Slot S1 đang setting 不制限 (type_limit_booking = 0)",
       "1. Đổi sang có giới hạn, nhập 5 → Lưu → query DB\n"
       "2. Đổi lại về không giới hạn → Lưu → query DB",
       "Đổi 2 chiều",
       "- Bước 1: `type_limit_booking` = 1, `total_person` = 5\n"
       "- Bước 2: `type_limit_booking` = 0\n"
       "- Màn 受付枠一覧 hiển thị tương ứng「5人」và「上限なし」",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r325-r326 — TC gốc chỉ có tiêu đề. Phần DB do AI bổ sung "
            "theo spec (Q-19: 無制限 lưu total_person = 1 là giá trị RÁC, chỉ type_limit_booking có nghĩa)."),

    tc("受付枠 — sửa 定員 & xóa", "STATE-DEP-001", "Normal",
       "Xóa 1 slot chưa có booking → xóa mềm thành công",
       CAL + "\n- Slot S1 chưa có booking nào",
       "1. Mở modal edit slot S1 → bấm「この受付枠を削除する」→ xác nhận\n"
       "2. Query `calendar_course_receptions.deleted_at`\n3. Kiểm 4 màn xem: ngày/tuần/tháng/list",
       "1 slot rỗng",
       "- `deleted_at` được ghi giá trị (xóa mềm)\n- Slot biến mất khỏi cả 4 màn quản lý",
       note="Nguồn: Quản lý calendar_new r335, r1021-r1024."),

    tc("受付枠 — sửa 定員 & xóa", "DATA-DB-001", "Normal",
       "Xóa slot có booking KHÔNG phải approve → xóa cả booking + ghi history",
       CAL + "\n- Slot S2 có 1 booking status リクエスト và 1 booking キャンセル",
       "1. Bấm xóa slot S2 → quan sát message confirm → bấm OK\n"
       "2. Query `calendar_course_receptions`, `calendar_course_bookings`, "
       "`calendar_course_booking_history_actions`\n3. Mở màn 削除済み予約",
       "1 slot, 2 booking không approve",
       "- Hiện confirm「本当にこの受付枠を削除してよろしいですか？」\n"
       "- `calendar_course_receptions.deleted_at` được ghi\n"
       "- `calendar_course_bookings.deleted_at` của CẢ 2 booking được ghi\n"
       "- `calendar_course_booking_history_actions` có bản ghi mới: admin_id · action_date · "
       "reason = '受付枠削除による予約削除' · status = 13\n"
       "- 2 booking xuất hiện ở màn 削除済み予約",
       note="Nguồn: Quản lý calendar_new r336. Verify 3 tầng: UI + DB + màn booking đã xóa (RULE-07). "
            "Khớp spec BR-18."),

    tc("受付枠 — sửa 定員 & xóa", "STATE-DEP-001", "Abnormal",
       "Xóa slot còn booking 予約確定 (admin book hoặc user book) → chặn kèm message",
       CAL + "\n- Slot S3 còn 1 booking 予約確定 (chuẩn bị 2 phiên bản: do admin book và do user book)",
       "1. Bấm xóa slot S3 (bản admin book) → quan sát\n2. Lặp với bản user book được approve",
       "2 kiểu booking approve",
       "- Cả 2 trường hợp: KHÔNG cho xóa, hiện message「「ステータス：予約確定」の予約が残っています。 "
       "受付枠を削除する場合、この受付枠の全ての予約が 「ステータス：キャンセル」になっている必要があります。」\n"
       "- Slot và booking giữ nguyên trong DB",
       note="Nguồn: Quản lý calendar_new r337-r338 + Quản lý calendar r267."),

    tc("受付枠 — sửa 定員 & xóa", "CONC-001", "Abnormal",
       "Đang ở bước confirm xóa slot thì có booking approve mới → vẫn chặn được",
       CAL + "\n- Slot S4 chưa có booking approve nào",
       "1. Mở modal xóa slot S4, đứng ở màn confirm (CHƯA bấm OK)\n"
       "2. Ở tab khác, cho LINE user booking vào S4 và được approve ngay\n"
       "3. Quay lại tab đầu, bấm OK trên confirm",
       "Booking approve chen giữa",
       "- Sau khi bấm OK: hiện message「「ステータス：予約確定」の予約が残っています。…」\n"
       "- Slot KHÔNG bị xóa, booking mới KHÔNG bị xóa oan",
       note="Nguồn: Quản lý calendar_new r339 (race condition — kiểm tra lại điều kiện ở thời điểm "
            "commit chứ không phải lúc mở confirm)."),

    tc("受付枠 — sửa 定員 & xóa", "OUT-TRUTH-001", "Abnormal",
       "Mở 2 tab cùng 1 slot: tab 1 xóa slot, tab 2 vào edit slot đó",
       CAL + "\n- Slot S1 chưa có booking, mở ở 2 tab trình duyệt",
       "1. Tab 1: xóa slot S1 thành công\n2. Tab 2 (chưa reload): mở modal edit slot S1, sửa 定員 → Lưu",
       "1 slot đã bị xóa ở tab khác",
       "- Tab 2 phải báo lỗi rõ ràng rằng slot không còn tồn tại HOẶC tự reload lại danh sách\n"
       "- TUYỆT ĐỐI KHÔNG được trả về success giả rồi không ghi gì vào DB",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar_new r983 — TC gốc CHỈ CÓ TIÊU ĐỀ. 🔴 Spec B-4 / A-23 nêu "
            "`updateReception` (EP-46) LUÔN trả `success: true` kể cả khi reception không tồn tại "
            "⇒ TC này DỰ KIẾN FAIL, phải raise bug. Xem MT-18."),

    tc("受付枠 — sửa 定員 & xóa", "CONC-001", "Abnormal",
       "Đang ở màn quản lý calendar bot A, đổi sang bot B (kể cả từ tab khác)",
       CAL + "\n- Admin có 2 bot A và B, mở màn quản lý calendar bot A ở 2 tab",
       "1. Ở tab 1, đổi bot sang B\n2. Quan sát tab 1\n3. Chuyển sang tab 2, thao tác bất kỳ",
       "2 bot, 2 tab",
       "- Tab 1: hiển thị màn LIST calendar của bot B\n"
       "- Tab 2: tự động reload lại data và hiển thị list calendar của bot đã đổi (B), "
       "không thao tác nhầm lên dữ liệu bot A",
       note="Nguồn: Quản lý calendar_new r981-r982."),

    # ══════════════════ Xóa nhiều slot ══════════════════
    tc("受付枠 — xóa nhiều", "BULK-001", "Normal",
       "Modal xóa nhiều slot: 2 message alert theo tình trạng booking",
       CAL + "\n- Tab 受付枠一覧 có: slot A (không booking), slot B (1 booking 予約確定)",
       "1. Tick chọn slot A → bấm「選択した受付枠を一括削除」→ quan sát alert\n"
       "2. Tick thêm slot B → bấm nút xóa → quan sát alert",
       "2 slot khác tình trạng",
       "- Bước 1: hiện alert「選択された受付枠を全て削除しますがよろしいですか？」(cho phép xóa)\n"
       "- Bước 2: hiện alert「削除する受付枠の中に「ステータス：予約確定」の予約が1つ以上残っています。"
       "受付枠を削除する場合、この受付枠の全ての予約が「ステータス：キャンセル」になっている必要があります。」"
       "và KHÔNG cho xóa",
       note="Nguồn: Quản lý calendar_new r998-r999. ⚠️ Message này KHÁC message khi xóa 1 slot "
            "(thêm tiền tố 削除する受付枠の中に…が1つ以上). Khớp spec BR-17 (kiểm SUM(total_approve) > 0)."),

    tc("受付枠 — xóa nhiều", "BULK-001", "Normal",
       "Xóa 1 slot / nhiều slot / all slot khi KHÔNG còn booking approve",
       CAL + "\n- Tab 受付枠一覧 có 5 slot: 2 slot rỗng, 3 slot chỉ có booking request/cancel",
       "1. Tick 1 slot rỗng → xóa → OK\n2. Tick 3 slot (rỗng + có booking không approve) → xóa → OK\n"
       "3. Tick 全選択 all slot còn lại → xóa → OK\n4. Query DB sau mỗi bước",
       "5 slot",
       "- Cả 3 bước đều hiện confirm「選択された受付枠を全て削除しますがよろしいですか？」\n"
       "- Sau OK: `calendar_course_receptions.deleted_at` và `calendar_course_bookings.deleted_at` "
       "của các slot/booking tương ứng được ghi\n"
       "- `calendar_course_booking_history_actions` ghi reason = '受付枠削除による予約削除', status = 13",
       note="Nguồn: Quản lý calendar_new r1000-r1001, r1013-r1014, r1017-r1018, r1034-r1035."),

    tc("受付枠 — xóa nhiều", "BULK-001", "Abnormal",
       "Xóa nhiều slot khi trong tập chọn CÓ slot còn booking approve → chặn TOÀN BỘ",
       CAL + "\n- Chọn 4 slot: 3 slot rỗng + 1 slot còn 1 booking 予約確定",
       "1. Tick 4 slot → bấm xóa\n2. Query DB kiểm 3 slot rỗng có bị xóa không",
       "4 slot, 1 slot vướng booking approve",
       "- Hiện message「削除する受付枠の中に「ステータス：予約確定」の予約が1つ以上残っています。…」\n"
       "- KHÔNG slot nào bị xóa (kể cả 3 slot rỗng) — thao tác là all-or-nothing",
       note="Nguồn: Quản lý calendar_new r1008-r1012, r1015-r1016, r1019-r1020, r1036-r1037."),

    tc("受付枠 — xóa nhiều", "BULK-001", "Abnormal",
       "Xóa nhiều slot — ma trận 6 nguồn booking approve đều chặn",
       CAL + "\n- Chuẩn bị 6 slot, mỗi slot có đúng 1 booking approve từ 1 nguồn khác nhau",
       "Với từng slot, tick chọn và bấm xóa nhiều:\n"
       "1. Admin book\n2. User book được approve\n3. Booking approve luôn rồi user request cancel "
       "→ admin DENY (quay lại approve)\n4. Admin booking full slot\n5. User booking full slot\n"
       "6. Booking approve rồi user request cancel (đang chờ duyệt)",
       "6 nguồn booking",
       "- Case 1, 2, 3, 4, 5: bị CHẶN với message 削除する受付枠の中に…\n"
       "- Case 6 (đang request cancel, status 5): cần chốt — spec BR-17 chỉ kiểm `total_approve` "
       "nên có thể CHO xóa, nhưng booking này vẫn đang chiếm chỗ",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar_new r1008-r1012. Case 6 là suy luận của AI từ spec BR-17 "
            "(chỉ kiểm total_approve) — corpus không có TC. Xem MT-19."),

    tc("受付枠 — xóa nhiều", "BULK-001", "Normal",
       "Xóa slot ở trang 2 và xóa slot thuộc nhiều tháng",
       CAL + "\n- Tab 受付枠一覧 có 60 slot rải nhiều tháng, phân trang 20 item/trang",
       "1. Sang trang 2, tick 3 slot → xóa → OK\n"
       "2. Lọc khoảng ngày trải 3 tháng, tick slot ở cả 3 tháng → xóa → OK\n3. Query DB",
       "60 slot",
       "- Bước 1: 3 slot ở trang 2 bị xóa đúng, không xóa nhầm slot trang 1\n"
       "- Bước 2: xóa thành công slot ở cả 3 tháng",
       note="Nguồn: Quản lý calendar_new r1026-r1027, r1043."),

    tc("受付枠 — xóa nhiều", "BULK-001", "Abnormal",
       "Tick chọn ở trang 2 rồi sang trang khác → mất lựa chọn",
       CAL + "\n- Tab 受付枠一覧 có 60 slot",
       "1. Sang trang 2, tick 3 slot\n2. Chuyển sang trang 3\n3. Quay lại trang 2",
       "60 slot",
       "- Bước 2: bộ đếm số slot đã chọn về 0, nút xóa disable\n"
       "- Bước 3: các slot ở trang 2 KHÔNG còn được tick",
       note="Nguồn: Quản lý calendar_new r1049."),

    tc("受付枠 — xóa nhiều", "CONC-001", "Abnormal",
       "Double click nút 選択した受付枠を一括削除 → chỉ tính 1 lần; sau khi xóa xong nút disable",
       CAL + "\n- Tick chọn 2 slot rỗng",
       "1. Double click nhanh nút「選択した受付枠を一括削除」\n2. Xác nhận\n"
       "3. Quan sát nút sau khi xóa thành công\n4. Query DB",
       "2 slot",
       "- Chỉ thực hiện 1 lần xóa, không văng lỗi, không gửi 2 request\n"
       "- Sau khi xóa xong nút bị disable (vì không còn slot nào được tick)",
       note="Nguồn: Quản lý calendar_new r1050-r1051."),

    tc("受付枠 — xóa nhiều", "LIST-001", "Normal",
       "Xóa nhiều slot: kiểm phân trang và thao tác 詳細 khi không ở trang 1",
       CAL + "\n- Tab 受付枠一覧 có 60 slot",
       "1. Chọn số item/page → kiểm số trang, item start-end\n"
       "2. Bấm số trang / next / previous → kiểm dữ liệu\n"
       "3. Ở trang 2 bấm 詳細 mở modal edit slot rồi xóa slot đó",
       "60 slot",
       "- Data từng trang đúng, không trùng lặp\n- Thao tác 詳細 và xóa ở trang 2 hoạt động bình thường",
       note="Nguồn: Quản lý calendar_new r1044-r1048."),

    # ══════════════════ CSV export ══════════════════
    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Màn export CSV: list course chỉ course ON, đúng thứ tự, có scroll",
       CAL + "\n- Có 25 course, trong đó 3 course OFF",
       "1. Bấm「CSV管理」→ tab エクスポート\n2. Quan sát list course",
       "25 course, 3 OFF",
       "- Chỉ hiện 22 course đang ON\n- Hiển thị `system_name` của course\n"
       "- Đúng thứ tự như màn quản lý course\n- Có thanh scroll khi list dài",
       note="Nguồn: Quản lý calendar_new r478-r479."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Abnormal",
       "Export CSV không chọn course nào → báo lỗi",
       CAL,
       "1. Mở màn export CSV\n2. Không tick course nào\n3. Bấm「CSVダウンロード」",
       "0 course",
       "- Báo lỗi「コースを入力してください」\n- Không tải file nào",
       note="Nguồn: Quản lý calendar_new r483."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV: chọn nhiều course → mỗi course 1 file",
       CAL + "\n- Có 3 course C1, C2, C3 đều có slot trong khoảng ngày chọn",
       "1. Chọn khoảng ngày 01/04 → 04/05\n2. Tick cả 3 course\n3. Bấm CSVダウンロード\n"
       "4. Kiểm số file tải về",
       "3 course",
       "- Tải về ĐÚNG 3 file CSV, mỗi course 1 file\n"
       "- Chú thích trên màn ghi「コースごとにCSVが作成されます。」",
       note="Nguồn: Quản lý calendar_new r485."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV: format 4 cột và thứ tự dữ liệu",
       CAL + "\n- Course C1 có 5 slot trong khoảng ngày chọn, 1 slot setting 無制限",
       "1. Export CSV cho C1 khoảng 04/04 → 04/05\n2. Mở file, kiểm header và dữ liệu\n"
       "3. Đối chiếu query `SELECT * FROM calendar_course_receptions WHERE course_id = {C1} "
       "AND received_booking_date BETWEEN '2024-04-04' AND '2024-05-04' "
       "ORDER BY received_booking_date, start_time ASC`",
       "5 slot",
       "- File có đúng 4 cột:「追加したい日付」「開始時間」「終了時間」"
       "「このコースの予約を停止する予約上限人数」\n"
       "- Dữ liệu sort theo `received_booking_date` rồi `start_time` tăng dần\n"
       "- Slot 無制限 xuất ra text「無制限」ở cột 4",
       note="Nguồn: Quản lý calendar_new r487-r488, r502."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV: các khoảng thời gian khác nhau + double click nút export",
       CAL + "\n- C1 có slot rải nhiều ngày, nhiều tháng, sang năm sau",
       "1. Export data trong 1 ngày\n2. Trong nhiều ngày\n3. Trong nhiều tháng\n"
       "4. Từ năm này sang năm khác\n5. Double click nhanh nút export",
       "4 khoảng thời gian",
       "- Bước 1-4: file chứa đủ slot trong khoảng đã chọn, không thiếu ngày biên\n"
       "- Bước 5: chỉ tải về 1 bộ file, không tải 2 lần",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r489-r493 — TC gốc CHỈ CÓ TIÊU ĐỀ, expected do AI bổ sung."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Abnormal",
       "Bug #29484: thêm slot / đổi time rồi export → file phải có ĐỦ data mới",
       CAL + "\n- C1 đã có slot ngày 31/03, 01/04, 02/04, 04/04",
       "1. Thêm slot mới ngày 10/04 và đổi time slot 01/04\n"
       "2. Export CSV cho C1 khoảng 31/03 → 30/04\n3. Mở file kiểm",
       "4 slot cũ + 1 slot mới + 1 slot đổi time",
       "- File chứa ĐỦ 5 slot, bao gồm slot 10/04 mới thêm\n"
       "- Slot 01/04 hiển thị time đã đổi",
       note="Nguồn: Quản lý calendar r1066 (Bug #29484, 04/2025). ⚠️ TC gốc ghi kết quả rất mơ hồ "
            "「Nga: check download đc là dc」— expected trên do AI viết lại theo mô tả bug. "
            "Cần Leader xác nhận."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV booking của 1 slot: tên file, encoding, cột cố định",
       CAL + "\n- Slot 01/10 09:00-10:00 của course「初心者」có 3 booking",
       "1. Mở modal danh sách booking của slot\n2. Bấm nút CSV → tải file\n"
       "3. Mở file bằng Excel (Windows), kiểm tên file và nội dung",
       "3 booking",
       "- Tên file format「コース名 2024.10.01(日) 09:00~10:00」\n"
       "- Encoding Shift-JIS ⇒ mở bằng Excel không bị mojibake tiếng Nhật\n"
       "- Có cột タイムスタンプ format「2024.10.01（日）08:44」\n"
       "- Dữ liệu sort theo booking time tăng dần\n- KHÔNG export booking đã xóa",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r174, r217-r218, r224, r180."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV booking: cột ステータス — ma trận 11 luồng",
       CAL + "\n- Slot có booking đủ 11 luồng thao tác",
       "1. Tạo booking theo 11 luồng: admin book · user book đợi approve · admin approve · "
       "admin deny · user book approve ngay · admin cancel · user request cancel · deny request cancel · "
       "approve request cancel · user cancel ngay · user book lúc full slot\n"
       "2. Export CSV, kiểm cột ステータス từng dòng",
       "11 luồng",
       "- Admin book:「予約確定（手動追加）」\n- Đợi approve:「予約リクエスト」\n"
       "- Được approve / deny request cancel:「予約確定」\n- Bị deny:「否認」\n"
       "- Admin cancel:「キャンセル（手動）」\n- Đang request cancel:「キャンセルリクエスト」\n"
       "- Đã cancel (user cancel / approve request cancel):「キャンセル」\n"
       "- Book lúc full slot:「通知希望」",
       note="Nguồn: Quản lý calendar_new r175, r219."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV booking: cột お客様名 khi admin book khách NGOÀI hệ thống",
       CAL + "\n- Có 1 booking do admin book cho khách ngoài hệ thống (nhập tên tay)",
       "1. Export CSV của slot\n2. Kiểm 2 cột お客様名（LINE名）và お客様名（システム表示名）",
       "1 booking khách ngoài hệ thống",
       "- Cột お客様名（LINE名）: TRỐNG\n- Cột お客様名（システム表示名）: chứa tên admin đã nhập",
       note="Nguồn: Quản lý calendar_new r220-r221."),

    tc("受付枠 — CSV export/import", "OUT-EXPORT-001", "Normal",
       "Export CSV booking: cột friend info — thêm/OFF/không title/dấu phẩy",
       CAL + "\n- Form có 2 câu mặc định (họ tên, email) + câu hỏi Q1 (ON), Q2 (OFF), "
             "Q3 (không nhập title)\n- 1 booking có câu trả lời chứa dấu phẩy「A,B,C」",
       "1. Export CSV, kiểm số cột và nội dung\n"
       "2. Tạo thêm friend info mới Q4 rồi export lại",
       "5 câu hỏi + 1 câu trả lời có dấu phẩy",
       "- Có cột cho họ tên, email, Q1, Q2 (câu OFF VẪN export)\n"
       "- KHÔNG có cột cho Q3 (không có title)\n"
       "- Câu trả lời「A,B,C」không làm vỡ format CSV (được escape đúng)\n"
       "- Sau khi tạo Q4: file export có thêm cột tương ứng Q4",
       note="Nguồn: Quản lý calendar_new r177, r181, r225-r229."),

    # ══════════════════ CSV import ══════════════════
    tc("受付枠 — CSV export/import", "UI-001", "Normal",
       "Màn import CSV: list course chỉ course ON, có scroll",
       CAL + "\n- Có 25 course, 3 course OFF",
       "1. Bấm CSV管理 → tab インポート\n2. Quan sát list course",
       "25 course",
       "- Chỉ hiện 22 course ON, hiển thị `system_name`, đúng thứ tự màn quản lý course, có scroll",
       note="Nguồn: Quản lý calendar_new r494-r495."),

    tc("受付枠 — CSV export/import", "DATA-001", "Normal",
       "Import CSV: 4 tổ hợp trùng/không trùng khung giờ với slot đã có",
       CAL + "\n- C1 đã có slot ngày 20/10 09:00-10:00 定員 5",
       "Import file CSV cho C1 với 4 dòng:\n"
       "1. 2024-10-20, 09:00, 10:00, 8 (trùng hoàn toàn)\n"
       "2. 2024-10-20, 11:00, 12:00, 3 (khác cả start và end)\n"
       "3. 2024-10-20, 08:00, 10:00, 3 (khác start, cùng end)\n"
       "4. 2024-10-20, 09:00, 11:00, 3 (cùng start, khác end)\n"
       "Sau import query `calendar_course_receptions`",
       "4 dòng CSV",
       "- Dòng 1: GHI ĐÈ `total_person` của slot cũ thành 8 (không tạo bản ghi mới)\n"
       "- Dòng 2, 3, 4: INSERT bản ghi mới\n- Tổng cộng có 4 slot cho C1 ngày 20/10",
       note="Nguồn: Quản lý calendar_new r497-r500."),

    tc("受付枠 — CSV export/import", "DATA-REF-001", "Normal",
       "Import CSV: khung giờ trùng với slot ĐÃ XÓA MỀM → insert bản ghi mới",
       CAL + "\n- C1 có slot 20/10 09:00-10:00 đã bị xóa mềm (`deleted_at` khác NULL)",
       "1. Import CSV dòng: 2024-10-20, 09:00, 10:00, 5\n2. Query DB",
       "1 slot đã xóa mềm",
       "- INSERT bản ghi MỚI (không hồi sinh bản ghi đã xóa)\n"
       "- DB có 2 dòng: 1 dòng `deleted_at` khác NULL và 1 dòng mới `deleted_at` = NULL",
       note="Nguồn: Quản lý calendar_new r501."),

    tc("受付枠 — CSV export/import", "DATA-001", "Normal",
       "Import CSV: cột cuối là 無制限 → set type_limit_booking = không giới hạn",
       CAL,
       "1. Import CSV dòng: 2024-10-25, 09:00, 10:00, 無制限\n"
       "2. Query `calendar_course_receptions`\n3. Kiểm hiển thị ở tab 受付枠一覧 và export lại CSV",
       "Giá trị「無制限」",
       "- DB: `type_limit_booking` = 0 (không giới hạn)\n"
       "- Tab 受付枠一覧 hiển thị「上限なし」\n- Export lại: cột cuối ra đúng「無制限」",
       note="Nguồn: Quản lý calendar_new r502. ⚠️ Spec Q-19: khi 無制限, `total_person` lưu giá trị "
            "rác = 1 — chỉ được đọc `type_limit_booking`."),

    tc("受付枠 — CSV export/import", "FUNC-003", "Abnormal",
       "Import CSV: validate file và cột — sai định dạng file, sai tên cột",
       CAL,
       "1. Chọn file .txt → bấm import\n2. Chọn file CSV nhưng đổi tên header các cột → import\n"
       "3. Không chọn course → import\n4. Không chọn file → import",
       "4 tình huống",
       "- Bước 1: chỉ chọn được file excel/csv (dialog lọc định dạng)\n"
       "- Bước 2: VẪN import được — hệ thống lấy theo THỨ TỰ CỘT, không theo tên cột\n"
       "- Bước 3, 4: báo lỗi bắt buộc chọn",
       note="Nguồn: Quản lý calendar_new r504-r507. ⚠️ Hành vi ở bước 2 (bỏ qua tên cột) là rủi ro "
            "silent-error: file sai thứ tự cột sẽ import sai mà không báo. Xem MT-20."),

    tc("受付枠 — CSV export/import", "FUNC-003", "Abnormal",
       "Import CSV: validate từng cột — message lỗi kèm số dòng",
       CAL,
       "Import file CSV có các dòng lỗi, kiểm message trả về:\n"
       "1. Dòng 2: cột 追加したい日付 bỏ trống\n2. Dòng 3: ngày format dd-mm-yyyy\n"
       "3. Dòng 4: ngày format yyyy/mm/dd\n4. Dòng 5: ngày không phải date\n"
       "5. Dòng 6: cột 開始時間 bỏ trống\n6. Dòng 7: cột 終了時間 bỏ trống\n"
       "7. Dòng 8: start hoặc end > 23:59\n8. Dòng 9: start > end\n9. Dòng 10: start = end\n"
       "10. Dòng 11: 予約上限人数 bỏ trống\n11. Dòng 12: 予約上限人数 = 2.5",
       "File CSV 11 dòng lỗi",
       "- Trả về chuỗi lỗi NHIỀU DÒNG, mỗi dòng nêu đúng số dòng và tên cột:\n"
       "  ·「2行の追加したい日付のデータに不備があります」(cả 4 case lỗi ngày)\n"
       "  ·「6行の開始時間のデータに不備があります」(cả case start > end và start > 23:59)\n"
       "  ·「7行の終了時間のデータに不備があります」(cả case start = end)\n"
       "  ·「11行の予約上限人数のデータに不備があります」\n"
       "- KHÔNG ghi bản ghi nào vào DB (có 1 dòng lỗi là bỏ toàn bộ file)",
       note="Nguồn: Quản lý calendar_new r508-r518 + spec EP-51 (api-spec.md §EP-51: "
            "「Nếu có bất kỳ lỗi nào ⇒ không ghi gì, trả toàn bộ chuỗi lỗi」)."),

    tc("受付枠 — CSV export/import", "FUNC-004", "Boundary",
       "Import CSV: 予約上限人数 = 0 → import success",
       CAL,
       "1. Import CSV dòng: 2024-10-25, 09:00, 10:00, 0\n2. Query DB",
       "定員 = 0",
       "- Import success, `total_person` = 0",
       note="Nguồn: Quản lý calendar_new r519."),

    tc("受付枠 — CSV export/import", "FUNC-003", "Abnormal",
       "Import CSV: 予約上限人数 nhỏ hơn số booking đã approve hiện tại → validate",
       CAL + "\n- C1 có slot 20/10 09:00-10:00 với 3 booking approve",
       "1. Import CSV dòng: 2024-10-20, 09:00, 10:00, 1\n2. Query DB",
       "定員 mới = 1 < 3 approve",
       "- Báo lỗi「{n}行の予約上限人数のデータに不備があります」\n"
       "- `total_person` giữ nguyên giá trị cũ",
       note="Nguồn: Quản lý calendar_new r520 + spec EP-51 (điều kiện 「total_booking > giá trị mới」)."),

    tc("受付枠 — CSV export/import", "FUNC-002", "Abnormal",
       "🔴 Import CSV: dòng có thời điểm QUÁ KHỨ — bỏ qua im lặng hay báo lỗi?",
       CAL + "\n- Hôm nay 25/10/2024, 10:00",
       "1. Import CSV có 3 dòng: (a) 2024-10-01 (ngày quá khứ), (b) 2024-10-25 09:00 "
       "(hôm nay nhưng giờ đã qua), (c) 2024-10-30 09:00 (hợp lệ)\n"
       "2. Quan sát message trả về\n3. Query `calendar_course_receptions`",
       "3 dòng, 2 dòng quá khứ",
       "- Theo spec EP-51 (isPast) và tab「Quản lý calendar」r506-r507: dòng (a) và (b) bị BỎ QUA "
       "IM LẶNG, không báo lỗi; dòng (c) được insert ⇒ DB có 1 slot mới\n"
       "- Nếu hệ thống báo lỗi「{line}行目の時間は現在より過去になりますので、登録できません。」"
       "và KHÔNG insert dòng (c) ⇒ FAIL, phải escalate",
       spec="Đã hỏi leader",
       note="🔴 MÂU THUẪN 2 tab: 「Quản lý calendar」r506-r507 (spec update 8/10/2024 —「bỏ qua, "
            "KHÔNG báo lỗi nữa」) vs「Quản lý calendar_new」r521-r522 (báo lỗi「{line}行目の時間は"
            "現在より過去になりますので、登録できません。」). Spec EP-51 đứng về phía tab cũ. "
            "TC viết theo SPEC. Xem MT-15."),

    tc("受付枠 — CSV export/import", "DATA-REF-001", "Normal",
       "Import CSV nới 定員 trên slot đang kín chỗ → tự bắn 空き枠通知",
       CAL + "\n- Slot 30/10 09:00-10:00 定員 2, đã có 2 booking approve (kín chỗ)\n"
             "- Có 2 LINE user đang đăng ký キャンセル待ち ở slot này\n"
             "- Calendar đang bật 空き枠通知受け取り設定",
       "1. Import CSV dòng: 2024-10-30, 09:00, 10:00, 5\n"
       "2. Kiểm LINE app của 2 user đang chờ",
       "定員 2 → 5, 2 user chờ",
       "- Cả 2 user nhận được tin nhắn thông báo có chỗ trống\n"
       "- Slot chuyển từ kín sang còn 3 chỗ ở màn LINE user",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1177, r1185, r1193, r1201 (change limit bằng import CSV) "
            "+ spec BR-19. RULE-06: verify tới output cuối là tin LINE."),

    tc("受付枠 — CSV export/import", "DATA-REF-001", "Abnormal",
       "Import CSV: chọn course A rồi đổi sang course B trước khi bấm import",
       CAL + "\n- Có 2 course A và B",
       "1. Vào màn import, chọn course A, upload file\n2. Đổi selection sang course B\n"
       "3. Bấm import\n4. Query slot của A và B",
       "1 file, 2 course",
       "- Data được import vào course B (course đang chọn tại thời điểm bấm import)\n"
       "- Course A KHÔNG bị thêm slot nào",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r523 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("受付枠 — CSV export/import", "CONC-001", "Abnormal",
       "Double click nút import → chỉ import 1 lần",
       CAL,
       "1. Chọn course, upload file CSV 5 dòng hợp lệ\n2. Double click nhanh nút import\n"
       "3. Query `calendar_course_receptions`",
       "File 5 dòng",
       "- Chỉ tạo 5 slot, KHÔNG tạo 10 slot",
       note="Nguồn: Quản lý calendar_new r524."),
]
