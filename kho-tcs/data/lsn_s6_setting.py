# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm 全体設定 phần 1: メッセージ・アクション, 開始・締切, 1人あたりの予約上限,
質問項目.

Nguồn chính: 11.2 TCsLine_LessonCalendar → tab「Setting calendar」r3-r826
  (05/2024 → 05/2026; SpecChange #26462 08/2024, SpecImprove #33696 01/2026 validate label trùng,
   redmine #29272 bộ TC Create/Edit Form)
Spec: BR-07…BR-10, BR-44…BR-49, BR-50, BR-P07, BR-P08, EP-53, EP-54.
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, course C1「初心者」1h00, 5.000 yên\n"
       "- Mở /basic/calendar-management/21 > tab 全体設定")

S6 = [
    # ══════════════════ Menu 全体設定 ══════════════════
    tc("予約・キャンセル メッセージ", "UI-001", "Normal",
       "Sidebar 全体設定: 4 nhóm label và các menu con",
       CAL,
       "1. Mở tab 全体設定\n2. Quan sát menu bên trái",
       "—",
       "- Label 1「メッセージ・予約の各種設定」gồm 3 menu: setting booking · remind · nhận notify\n"
       "- Label 2「予約画面」gồm 5 menu: item friend info · setting hiển thị · màn top · "
       "màn business · terms\n"
       "- Label 3「連携設定」gồm: liên kết Google\n"
       "- Label 4「その他」gồm: xóa calendar",
       note="Nguồn: Setting calendar r3-r6."),

    tc("予約・キャンセル メッセージ", "UI-001", "Normal",
       "Màn hub 予約・キャンセル: preview message và tổng quan setting (2 thẻ)",
       CAL + "\n- Đã setting message lúc booking, chưa setting message lúc cancel\n"
             "- Setting booking = 全承認, hạn nhận = 7日前 00:00 ~ 1日前 23:59",
       "1. Vào menu「予約・キャンセルのメッセージ・リクエストと締切」\n"
       "2. Quan sát thẻ 予約: tab メッセージ, tab 各種設定, tab アクション\n"
       "3. Quan sát thẻ キャンセル tương tự",
       "1 thẻ có data, 1 thẻ rỗng",
       "- Thẻ 予約 tab メッセージ: hiện nội dung message đã setting (có scroll nếu dài)\n"
       "- Thẻ キャンセル tab メッセージ: hiện text「メッセージは設定されていません」\n"
       "- Tab 各種設定 của thẻ 予約: hiện「予約を全承認する」và「7日前 00:00から / 1日前 23:59まで」\n"
       "- Tab アクション chưa set: hiện「アクションは設定されていません」",
       note="Nguồn: Setting calendar r8-r11, r15-r18."),

    tc("予約・キャンセル メッセージ", "UI-001", "Normal",
       "Màn hub: 3 giá trị 承認・リクエスト của thẻ キャンセル",
       CAL,
       "1. Đổi setting cancel = 全承認 → quay lại màn hub, quan sát tab 各種設定 thẻ キャンセル\n"
       "2. Đổi sang リクエスト制 → quan sát\n3. Đổi sang 予約後のキャンセル不可 → quan sát",
       "3 giá trị approve_type",
       "-「キャンセルを全承認する」·「リクエスト制にする」·「予約後のキャンセル不可」",
       note="Nguồn: Setting calendar r17."),

    tc("予約・キャンセル メッセージ", "UI-001", "Normal",
       "Màn hub: preview action có filter → hiện nhãn 絞り込みあり và mở modal filter",
       CAL + "\n- Đã setting 3 action lúc booking, trong đó 1 action có filter",
       "1. Vào màn hub → tab アクション của thẻ 予約\n2. Quan sát danh sách action\n"
       "3. Bấm vào nhãn「絞り込みあり」",
       "3 action, 1 có filter",
       "- Hiện preview đủ 3 action: loại action + nội dung, có scroll\n"
       "- Action có filter hiện thêm text「絞り込みあり」\n"
       "- Bấm vào: mở modal edit filter của action đó",
       note="Nguồn: Setting calendar r13, r20."),

    tc("予約・キャンセル メッセージ", "FUNC-001", "Normal",
       "Màn hub: 2 nút chuyển sang màn setting chi tiết",
       CAL,
       "1. Bấm「予約時の設定をする」\n2. Quay lại, bấm「キャンセル時の設定をする」",
       "—",
       "- Bước 1: sang màn setting lúc booking (SCR 予約時の各種設定)\n"
       "- Bước 2: sang màn setting lúc cancel (SCR 予約キャンセル時の各種設定)",
       note="Nguồn: Setting calendar r14, r21."),

    # ══════════════════ Message & action lúc booking ══════════════════
    tc("予約・キャンセル メッセージ", "MSG-002", "Normal",
       "Setting 全承認: insert mã và mẫu vào message 予約完了時",
       CAL + "\n- Chọn option「全承認制にする」",
       "1. Bấm ＋ LINE名 → chèn\n"
       "2. Bấm 予約情報 → chèn lần lượt 5 mã: 予約日時 · コース名 · 料金 · キャンセル用 URL · 店舗名\n"
       "3. Bấm 友だち情報 → chèn info basic và các kiểu friend info khác\n"
       "4. Bấm「例文を挿入する」→ quan sát nội dung mẫu\n5. Lưu → cho U1 booking",
       "5 mã booking + friend info",
       "- Bước 2: mã キャンセル用URL được chèn dạng VIẾT LIỀN (không có khoảng trắng)\n"
       "- Bước 4: mẫu bắt đầu「[name]様」+ 「下記の通り、予約が完了いたしました。」+ 4 mục "
       "予約日時 / ご予約コース名 / コース料金 / キャンセル用 URL\n"
       "- Bước 5: U1 nhận tin với tất cả mã đã thay bằng giá trị thật; URL hủy bấm được và "
       "mở đúng màn hủy booking của U1",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r24-r33, r87. RULE-06: verify tới output cuối là tin LINE + "
            "URL bấm được."),

    tc("予約・キャンセル メッセージ", "DATA-REF-001", "Abnormal",
       "Message booking: friend info bị xóa / đổi / folder bị xóa hoặc đổi",
       CAL + "\n- Message đã chèn friend info F1 (folder FD1) và F2 (folder FD2)",
       "1. Xóa F1 → cho U1 booking → kiểm tin\n2. Đổi tên F2 → booking → kiểm tin\n"
       "3. Đổi tên folder FD2 → booking → kiểm tin\n4. Xóa folder FD2 → booking → kiểm tin",
       "2 friend info, 2 folder",
       "- Bước 1: nội dung của F1 KHÔNG được gửi, phần còn lại vẫn gửi bình thường\n"
       "- Bước 2, 3: VẪN gửi được nội dung của F2\n"
       "- Bước 4: nội dung của F2 KHÔNG được gửi, phần còn lại vẫn gửi",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r29-r32."),

    tc("予約・キャンセル メッセージ", "MSG-002", "Normal",
       "Message booking: chọn 利用しない → disable textbox, chỉ gửi multi action",
       CAL + "\n- Đã setting message text + 2 multi action",
       "1. Tích「利用しない」→ quan sát textbox\n2. Lưu → cho U1 booking\n3. Kiểm tin LINE U1",
       "Message + 2 action",
       "- Textbox bị disable\n- U1 KHÔNG nhận msg text\n- U1 VẪN nhận 2 multi action",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r34."),

    tc("予約・キャンセル メッセージ", "FUNC-004", "Boundary",
       "Message booking: biên 5000 / 5001 ký tự và trường hợp vượt sau khi thay mã",
       CAL,
       "1. Nhập 5000 ký tự Nhật → Lưu\n2. Nhập 5001 ký tự → Lưu\n"
       "3. Nhập 4800 ký tự + chèn friend info của U1 có giá trị 1000 ký tự → Lưu → U1 booking\n"
       "4. Kiểm tin LINE U1 và màn エラーメッセージ",
       "5000 / 5001 / 4800+mã",
       "- 5000: save success\n- 5001: Invalid\n"
       "- Bước 3: GUI vẫn save success\n"
       "- Bước 4: U1 KHÔNG nhận tin; màn error message ghi nhận lỗi gửi",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r35-r37."),

    tc("予約・キャンセル アクション", "MSG-002", "Normal",
       "4 loại message của luồng booking: mẫu 例文 khác nhau cho mỗi loại",
       CAL,
       "1. Chọn 全承認制 → bấm 例文を挿入する ở 予約完了時 → ghi nội dung\n"
       "2. Chọn リクエスト制 → bấm 例文 ở 予約リクエスト受付時 → ghi nội dung\n"
       "3. Ở 予約リクエスト承認時 → bấm 例文 → ghi\n4. Ở 予約リクエスト否認時 → bấm 例文 → ghi",
       "4 loại message",
       "- 予約完了時:「下記の通り、予約が完了いたしました。」\n"
       "- 予約リクエスト受付時:「下記の通り、予約リクエストを受付いたしました。」\n"
       "- 予約リクエスト承認時:「下記の通り、予約リクエストを承認いたしました。」\n"
       "- 予約リクエスト否認時:「申し訳ございませんが、リクエストいただいた予約を受け付けることが"
       "できませんでした。」\n- 4 nội dung PHẢI khác nhau",
       note="Nguồn: Setting calendar r33, r48, r63, r78 (mỗi loại 1 mẫu riêng → tách rõ trong 1 TC "
            "so sánh vì đây là 1 chuỗi kiểm tra đối chiếu)."),

    tc("予約・キャンセル アクション", "MSG-002", "Normal",
       "Hyperlink コース設定 ở 4 màn setting action → nhảy sang màn setting course",
       CAL,
       "1. Ở màn setting 全承認制, bấm hyperlink「コース設定」\n"
       "2. Lặp ở màn リクエスト制 (3 tab: 受付時 / 承認時 / 否認時)",
       "4 màn",
       "- Cả 4 lần đều nhảy sang màn hình setting course",
       note="Nguồn: Setting calendar r22, r41, r56, r71."),

    tc("予約・キャンセル アクション", "MSG-002", "Normal",
       "Setting 全承認: admin book có chọn gửi/không gửi action, user book luôn gửi",
       CAL + "\n- Chọn 全承認制, đã setting message + action",
       "1. LINE user U1 booking → kiểm tin\n2. Admin book cho U2, chọn「実行する」→ kiểm tin U2\n"
       "3. Admin book cho U3, chọn「実行しない」→ kiểm tin U3",
       "3 kiểu đặt",
       "- U1: LUÔN nhận action (user booking không có lựa chọn)\n"
       "- U2: nhận action\n- U3: KHÔNG nhận action",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r22, r179."),

    tc("予約・キャンセル アクション", "MSG-002", "Normal",
       "Modal insert thông tin booking: giao diện, double click, nút đóng",
       CAL,
       "1. Bấm 予約情報 → quan sát option được chọn sẵn\n"
       "2. Chọn 1 mã, double click nút「メッセージに挿入」\n3. Bấm nút 戻る hoặc icon X",
       "—",
       "- Default select「予約日時」\n- Double click: chỉ insert 1 lần (không insert 2 mã)\n"
       "- Bấm 戻る/X: đóng modal",
       note="Nguồn: Setting calendar r86, r88-r89."),

    tc("予約・キャンセル アクション", "UI-001", "Normal",
       "Modal insert friend info: list folder, list info, đổi folder, cập nhật khi CRUD",
       CAL + "\n- Bot có 5 folder friend info, folder FD1 có tên dài max length\n"
             "- Có friend info đủ kiểu: text, date, point, select, image, pdf",
       "1. Bấm 友だち情報 → quan sát folder được chọn sẵn và danh sách folder\n"
       "2. Chọn folder FD2 → quan sát list info\n3. Đổi qua lại giữa nhiều folder\n"
       "4. Ở màn 友だち情報管理: thêm / sửa / xóa 1 friend info → mở lại modal này",
       "5 folder, 6 kiểu info",
       "- Default select folder mặc định\n- List folder đủ 5, đúng thứ tự như màn friend info, "
       "có scroll, tên dài xuống dòng hiển thị đầy đủ\n"
       "- Đổi folder: list info đổi tương ứng, CLEAR item của folder cũ\n"
       "- Bước 4: modal cập nhật đúng (thêm→có, sửa→đổi tên, xóa→mất)",
       note="Nguồn: Setting calendar r90-r99."),

    # ══════════════════ 予約の開始・締切 ══════════════════
    tc("予約の開始・締切", "UI-FIELD-001", "Normal",
       "Màn 予約の開始・締切: label và hiển thị theo option đang chọn",
       CAL,
       "1. Vào menu「予約の開始・締切」\n2. Quan sát 2 label\n"
       "3. Chọn option 1 (không setting) → quan sát\n4. Chọn option 2 (có setting) → quan sát",
       "—",
       "- 2 label:「予約受付開始」và「予約締切」\n"
       "- Option 1: các ô nhập của option 2 bị ẨN\n- Option 2: hiện các ô nhập tương ứng",
       note="Nguồn: Setting calendar r100-r102."),

    tc("予約の開始・締切", "FUNC-001", "Normal",
       "予約受付開始 mặc định いつでも予約を受け付ける → user book bất cứ lúc nào",
       CAL + "\n- Chọn option「いつでも予約を受け付ける」\n- Có slot ngày mai 10:00",
       "1. Lưu setting\n2. LINE user U1 mở trang booking ngay bây giờ → chọn slot ngày mai",
       "Slot tương lai",
       "- U1 book được ngay, không bị chặn bởi thời điểm mở nhận đặt",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r103."),

    tc("予約の開始・締切", "FUNC-001", "Normal",
       "予約受付開始 kiểu 日数指定: mở nhận đặt trước X ngày lúc Y giờ",
       CAL + "\n- Course start 10:00 ngày 04/03/2024",
       "1. Chọn「受付開始の時間を設定する」+ kiểu 日数指定, nhập 1 ngày lúc 08:00 → Lưu\n"
       "2. Ở thời điểm 07:59 ngày 03/03, LINE user mở trang booking\n"
       "3. Ở thời điểm 08:01 ngày 03/03, mở lại",
       "1 ngày trước, 08:00",
       "- Bước 2: chưa đến giờ mở nhận đặt ⇒ slot KHÔNG book được\n"
       "- Bước 3: book được bình thường",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r104. RULE-08: phụ thuộc thời gian server thật."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "予約受付開始 kiểu 日数指定: validate số ngày 1~180 và giờ 00:00~23:59",
       CAL,
       "1. Nhập số ngày = 1 → Lưu\n2. = 180 → Lưu\n3. = 0 → Lưu\n4. = 181 → Lưu\n"
       "5. = -1 và = 1.5 → Lưu\n"
       "6. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → Lưu từng giá trị",
       "Số ngày 1/180/0/181/-1/1.5 · 4 mốc giờ",
       "- Số ngày 1 và 180: Save success, kiểm được trên màn booking của user\n"
       "- Số ngày 0, 181, -1, 1.5: Invalid\n- Cả 4 mốc giờ: Save success",
       note="Nguồn: Setting calendar r105-r113."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "予約受付開始 kiểu 時間指定: validate giờ 00~23 và phút 00~59",
       CAL + "\n- Chọn kiểu 時間指定",
       "1. Nhập giờ = 23, phút = 59 → Lưu\n2. Nhập giờ = 24 → Lưu\n3. Nhập phút = 60 → Lưu\n"
       "4. Nhập giờ 09 phút 30 → Lưu, kiểm màn booking của user",
       "Biên giờ/phút",
       "- Giờ 23 phút 59: Save success\n- Giờ 24 hoặc phút 60: Invalid\n"
       "- Setting 09:30: course start 10:00 ngày 12/04 ⇒ user book được từ 00:30 ngày 12/04",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Setting calendar r114-r115 — TC gốc CHỈ CÓ TIÊU ĐỀ「Validate giờ từ 00~23」"
            "「Validate phút từ 00~59」. Kết quả mong đợi do AI bổ sung."),

    tc("予約の開始・締切", "FUNC-001", "Normal",
       "予約締切 mặc định 締切を設定しない → user book đến khi course start",
       CAL + "\n- Chọn「締切を設定しない（コース開始まで予約可能）」\n- Slot 10:00 hôm nay",
       "1. Lưu\n2. Lúc 09:59 LINE user mở trang booking\n3. Lúc 10:01 mở lại",
       "Slot 10:00 hôm nay",
       "- Bước 2: book được\n- Bước 3: slot bị ẨN, không book được nữa",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r117 + Booking phía line user r261, r405."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "予約締切 kiểu 日数指定: validate 1~180 ngày và 4 mốc giờ",
       CAL,
       "1. Chọn「予約締切を設定する」+ 日数指定\n"
       "2. Nhập 1 → Lưu · 180 → Lưu · 0 → Lưu · 181 → Lưu · 1.5 → Lưu\n"
       "3. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → Lưu từng giá trị",
       "5 số ngày + 4 mốc giờ",
       "- 1 và 180: Save success\n- 0, 181, 1.5: Invalid\n- Cả 4 mốc giờ: Save success",
       note="Nguồn: Setting calendar r118-r126."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "予約締切 kiểu 時間指定: vượt 23 giờ 59 phút → báo lỗi",
       CAL + "\n- Chọn 予約締切を設定する + 時間指定",
       "1. Nhập 23 giờ 59 phút → Lưu\n2. Nhập 24 giờ → Lưu\n3. Nhập 23 giờ 60 phút → Lưu",
       "Biên 23:59",
       "- 23 giờ 59 phút: Save success\n"
       "- 24 giờ hoặc 60 phút: báo lỗi「設定できるのは23時間59分以内です」",
       note="Nguồn: Setting calendar r127-r128."),

    tc("予約の開始・締切", "FUNC-002", "Abnormal",
       "Quan hệ 予約受付開始 và 予約締切 — 4 tổ hợp",
       CAL,
       "Với từng tổ hợp, bấm Lưu và ghi kết quả:\n"
       "1. Start = 2 ngày trước lúc 12:00 · End = 3 ngày trước lúc 12:00\n"
       "2. Start = 1 ngày trước lúc 20:00 · End = 23:59 (cùng ngày course)\n"
       "3. Start = 10:00 (kiểu giờ) · End = 12:00 (kiểu giờ)\n"
       "4. Start = 23:59 (kiểu giờ) · End = 2 ngày trước lúc 20:00",
       "4 tổ hợp",
       "- Tổ hợp 1: báo lỗi「予約締切は予約開始よりも後に設定してください」\n"
       "- Tổ hợp 2: Save success\n"
       "- Tổ hợp 3: báo lỗi「予約締切は予約開始よりも後に設定してください」\n"
       "- Tổ hợp 4: cần chốt — TC gốc để trống kết quả",
       spec="Đã hỏi leader",
       note="Nguồn: Setting calendar r129-r132. ⚠️ r132 (case 4) CHỈ CÓ TIÊU ĐỀ, không có kết quả. "
            "Lưu ý case 3: cùng kiểu 時間指定 mà start 10:00 < end 12:00 lại báo lỗi vì đếm NGƯỢC "
            "(trước bao nhiêu giờ). Xem MT-28."),

    tc("予約の開始・締切", "CONC-001", "Abnormal",
       "Double click nút Lưu và nút 戻る ở màn 予約の開始・締切",
       CAL,
       "1. Nhập setting hợp lệ, double click nút Lưu\n2. Bấm nút「戻る」",
       "—",
       "- Double click: chỉ lưu 1 lần, không văng lỗi\n- Bấm 戻る: quay về màn hub preview setting",
       note="Nguồn: Setting calendar r133-r134."),

    # ══════════════════ 1人あたりの予約上限 ══════════════════
    tc("1人あたりの予約上限", "FUNC-001", "Normal",
       "Default 制限なし → user book thoải mái khi còn slot",
       CAL + "\n- Chọn「制限なし」",
       "1. Lưu\n2. LINE user U1 booking 3 slot khác nhau trong cùng calendar",
       "3 slot còn chỗ",
       "- U1 book được cả 3, không bị chặn",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r146."),

    tc("1人あたりの予約上限", "FUNC-004", "Boundary",
       "Giới hạn = 1: user đã có 1 booking → không book thêm được cho tới khi qua giờ slot đó",
       CAL + "\n- Setting giới hạn = 1\n- U1 đã booking slot A 10:00 ngày 28/04",
       "1. U1 mở trang booking, chọn lịch ở màn TUẦN → thử book slot khác\n"
       "2. Thử ở màn THÁNG\n3. Thử book slot của COURSE KHÁC\n"
       "4. Sau 10:00 ngày 28/04, U1 book lại",
       "Giới hạn 1 booking/user",
       "- Bước 1, 2, 3: báo đã đạt giới hạn — nội dung tuỳ setting:\n"
       "  · Calendar CŨ chưa setting `text_limit_book_each_customer` (NULL): hiện "
       "「1人あたりの予約受付上限に達しています」\n"
       "  · Calendar đã setting text 受付制限に達している場合の案内テキスト: hiện đúng text đã setting\n"
       "- Bước 4: booking thành công",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r135-r138."),

    tc("1人あたりの予約上限", "FUNC-004", "Boundary",
       "Giới hạn = 2: user có 2 booking → chặn; qua giờ slot sớm nhất thì được book thêm 1",
       CAL + "\n- Setting giới hạn = 2\n- U1 đã booking slot A 10:00 và slot B 12:00 cùng ngày 28/04",
       "1. U1 thử book slot thứ 3 → quan sát\n"
       "2. Sau 10:00 ngày 28/04 (qua slot A), U1 book lại → quan sát\n"
       "3. Sau 12:00 (qua cả 2 slot), U1 book lại",
       "Giới hạn 2, 2 booking sẵn có",
       "- Bước 1: báo lỗi đã đạt giới hạn\n"
       "- Bước 2: book được thêm 1 lần\n- Bước 3: book được thêm nữa",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r139."),

    tc("1人あたりの予約上限", "DATA-001", "Normal",
       "Giới hạn = 1: ma trận 6 trạng thái booking sẵn có — cái nào tính vào giới hạn",
       CAL + "\n- Setting giới hạn = 1\n- Chuẩn bị 6 kịch bản, mỗi kịch bản U1 có 1 booking ở 1 trạng thái",
       "Với từng kịch bản, U1 thử booking slot mới và ghi kết quả:\n"
       "1. Booking sẵn có ở trạng thái booking success (status 1)\n"
       "2. Booking success do ADMIN book (status 2)\n3. Booking đang chờ approve (status 0)\n"
       "4. Booking đang request cancel (status 5)\n5. Booking đã cancel (status 4/7)\n"
       "6. Booking đang đợi nhận thông báo (status 3)",
       "6 trạng thái",
       "- Kịch bản 1, 2, 4: KHÔNG book thêm được (status 1, 2, 5 tính chiếm chỗ)\n"
       "- Kịch bản 3, 5, 6: VẪN book thêm được",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r140-r145 + spec BR-P07 (đếm status ∈ {1,2,5}). "
            "⚠️ Kịch bản 3 (status 0) KHÔNG tính giới hạn ⇒ ở chế độ リクエスト制 user có thể "
            "gửi vô hạn yêu cầu — xem MT-29."),

    tc("1人あたりの予約上限", "FUNC-002", "Abnormal",
       "Validate ô nhập giới hạn và text hiển thị khi đạt giới hạn",
       CAL,
       "1. Chọn option giới hạn, nhập 0 → Lưu\n2. Nhập 1.5 và「abc」→ Lưu\n"
       "3. Nhập 3 nhưng để trống ô text hiển thị → Lưu\n"
       "4. Nhập text có xuống dòng → Lưu → reload màn hình\n"
       "5. Đổi qua lại giữa 制限なし và có giới hạn nhiều lần → Lưu",
       "0 · 1.5 · abc · text rỗng · text có enter",
       "- Bước 1: Invalid (bắt đầu từ 1)\n- Bước 2: Invalid\n"
       "- Bước 3: báo lỗi「受付制限に達している場合の案内テキストを入力してください」\n"
       "- Bước 4: lưu vào `calendar_salon_setting_send_messages.text_limit_book_each_customer`; "
       "reload vẫn hiện đúng text (giữ xuống dòng); phía LINE user hiển thị đúng text này khi đạt limit\n"
       "- Bước 5: lưu theo lần thao tác CUỐI CÙNG",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r147-r153. RULE-07: verify DB + reload + màn LINE user."),

    # ══════════════════ 予約時のお客様への質問項目 ══════════════════
    tc("予約時のお客様への質問項目", "UI-001", "Normal",
       "Màn 質問項目: hyperlink hướng dẫn mở video mới",
       CAL,
       "1. Vào menu「予約時のお客様への質問項目」\n"
       "2. Bấm hyperlink「回答内容をお客様に送信する方法はこちら」",
       "—",
       "- Mở tab mới tới video hướng dẫn hiện hành "
       "(https://www.youtube.com/watch?v=HZp9BAsN3eY — bản cập nhật 05/2026)\n"
       "- KHÔNG mở video cũ https://youtu.be/UO5X0Yuzwuc",
       note="Nguồn: Setting calendar r255 (Bug KH #36770 05/2026 — link video cũ). "
            "TC gốc ghi cả 2 URL; đã lấy URL MỚI theo ngày."),

    tc("予約時のお客様への質問項目", "UI-001", "Normal",
       "Khối 1 — chọn loại item: 5 loại theo đúng thứ tự, hover và click",
       CAL,
       "1. Quan sát khối 1「項目を追加」\n2. Hover lên 1 loại item → quan sát\n"
       "3. Click vào loại「短文回答」→ quan sát khối 2 và 3\n"
       "4. Click liên tiếp 3 lần vào cùng 1 loại",
       "5 loại item",
       "- Khối 1 hiện đúng 5 loại theo thứ tự: text 1 dòng · text nhiều dòng · radio · checkbox · 日時\n"
       "- Chưa hover: không hiện nút add\n"
       "- Hover: đổi màu item + hiện nút add phía trên\n"
       "- Click: thêm item vào khối 2, khối 3 hiện nội dung item vừa thêm\n"
       "- Click 3 lần: tạo ra ĐÚNG 3 item",
       note="Nguồn: Setting calendar r257-r261."),

    tc("予約時のお客様への質問項目", "FUNC-DRAFT-001", "Normal",
       "Khối 3: đổi item đang chọn khi chưa lưu → hiện data trống của item mới",
       CAL,
       "1. Mới vào màn setting item → quan sát khối 3\n"
       "2. Chọn item X, gõ nội dung nhưng CHƯA click ra ngoài\n3. Chọn tiếp item Y ở khối 1\n"
       "4. Khối 2 đã có item X, chọn tiếp X ở khối 1 lần nữa",
       "2 item",
       "- Bước 1: khối 3 KHÔNG hiển thị gì\n"
       "- Bước 3: khối 3 hiển thị nội dung của item Y với data TRỐNG\n"
       "- Bước 4: khối 3 hiển thị item X mới với data TRỐNG (không load lại item X cũ)",
       note="Nguồn: Setting calendar r262-r264."),

    tc("予約時のお客様への質問項目", "DATA-001", "Normal",
       "Khối 2: 2 item mặc định họ tên + email, không cho xóa",
       CAL + "\n- Calendar vừa tạo mới",
       "1. Vào màn 質問項目 → quan sát khối 2\n"
       "2. Query `calendar_setting_send_forms` của calendar này\n3. Tìm nút xóa của 2 item này",
       "Calendar mới",
       "- Khối 2 có sẵn 2 item: họ tên (liên kết friend info systemname, id = -1) và "
       "email (liên kết mail, id = -3)\n"
       "- DB: 2 bản ghi có `can_delete` = 0\n- KHÔNG có nút xóa cho 2 item này",
       note="Nguồn: Setting calendar r265, r280, r341 + spec BR-07."),

    tc("予約時のお客様への質問項目", "UI-001", "Normal",
       "Khối 2: các marker của 1 item (tên, required, liên kết friend info)",
       CAL + "\n- Có item Q1 tên 8 ký tự required + liên kết friend info F1; "
             "item Q2 tên 15 ký tự, không required, không liên kết",
       "1. Quan sát dòng Q1 và Q2 ở khối 2",
       "2 item khác cấu hình",
       "- Marker loại item khớp với loại ở khối 1\n"
       "- Q1: hiện đủ tên 8 ký tự · marker「必須」· icon + tên friend info F1\n"
       "- Q2: tên bị cắt hiển thị「…」(vượt 10 ký tự) · marker「任意」· icon + text「なし」",
       note="Nguồn: Setting calendar r267-r273."),

    tc("予約時のお客様への質問項目", "FUNC-004", "Boundary",
       "Item 短文回答: validate 質問内容 (required, 50/51 ký tự) và 補足 (200 ký tự)",
       CAL,
       "1. Click vào ô 質問内容 rồi click ra ngoài mà không nhập → quan sát\n"
       "2. Nhập 50 ký tự → click ra ngoài\n3. Nhập 51 ký tự\n"
       "4. Nhập trùng nội dung với item đã có\n"
       "5. Bấm「質問の補足を入力」→ nhập 200 ký tự → click ra ngoài\n6. Nhập 201 ký tự",
       "rỗng · 50 · 51 · trùng · 200 · 201",
       "- Bước 1: báo required\n- Bước 2: save success\n- Bước 3: báo lỗi vượt ký tự\n"
       "- Bước 4: save success (CHO PHÉP trùng tên item)\n"
       "- Bước 5: save success\n- Bước 6: báo lỗi",
       note="Nguồn: Setting calendar r302, r304-r306, r311-r312. ⚠️ r351-r352 (item text nhiều dòng) "
            "ghi giới hạn 補足 là 50 ký tự thay vì 200 — KHÔNG NHẤT QUÁN. Xem MT-30."),

    tc("予約時のお客様への質問項目", "UI-INPUT-001", "Normal",
       "Ô 補足: đóng/mở giữ nội dung + placeholder",
       CAL,
       "1. Bấm「質問の補足を入力」→ nhập text\n2. Bấm lại「質問の補足を入力」→ quan sát\n"
       "3. Bấm lần nữa để mở lại → quan sát nội dung\n4. Quan sát placeholder khi ô rỗng",
       "—",
       "- Bước 2: ô 補足 đóng lại\n- Bước 3: nội dung đã nhập VẪN được giữ\n"
       "- Bước 4: placeholder là「補足情報を入力してください」",
       note="Nguồn: Setting calendar r307-r309."),

    tc("予約時のお客様への質問項目", "FUNC-003", "Normal",
       "Item 短文回答: 4 rule validate 入力内容の制限",
       CAL,
       "1. Quan sát option mặc định của「入力内容の制限」\n"
       "2. Chọn「利用する」→ quan sát selectbox\n"
       "3. Chọn lần lượt メールアドレス · 電話番号（11桁ハイフンなし）· カナ入力 · 整数 → Lưu\n"
       "4. LINE user mở trang booking, nhập giá trị sai và đúng cho từng rule",
       "4 rule",
       "- Bước 1: mặc định「利用しない」, KHÔNG hiện selectbox format\n"
       "- Bước 2: selectbox hiện, giá trị để trống\n"
       "- Bước 3: selectbox có đúng 4 lựa chọn, save success mỗi lựa chọn\n"
       "- Bước 4: phía LINE user validate đúng theo từng rule (xem TC nhóm LINE user)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r316-r322."),

    tc("予約時のお客様への質問項目", "FUNC-001", "Normal",
       "Item: option 必須 / 任意 → marker ở khối 2 và required phía LINE user",
       CAL,
       "1. Quan sát option mặc định\n2. Đổi sang 任意 → Lưu\n"
       "3. LINE user mở trang booking → thử submit không nhập câu hỏi này\n"
       "4. Đổi lại 必須 → LINE user thử submit không nhập",
       "2 mức bắt buộc",
       "- Mặc định là「必須」\n"
       "- 任意: khối 2 hiện marker 任意; LINE user submit được khi bỏ trống\n"
       "- 必須: khối 2 hiện marker 必須; LINE user bỏ trống thì báo lỗi「回答を入力してください」",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r323-r324. ⚠️ TC gốc ghi kết quả GIỐNG NHAU cho cả 2 nhánh "
            "(「có marker required ở mục 2」) — rõ ràng là lỗi soạn TC; AI đã sửa lại theo logic. "
            "Xem MT-31."),

    tc("予約時のお客様への質問項目", "FRIEND-001", "Normal",
       "Liên kết friend info: 3 option và hành vi tự tạo friend info",
       CAL,
       "1. Quan sát option mặc định của「友だち情報に回答を記録」\n"
       "2. Chọn「自動で友だち情報を生成して回答を記録」→ Lưu → mở màn 友だち情報管理\n"
       "3. Đổi tên item ở màn setting → kiểm màn 友だち情報管理\n"
       "4. Đổi tên friend info ở màn 友だち情報管理 → kiểm màn setting item\n"
       "5. Xóa item ở màn setting → kiểm màn 友だち情報管理",
       "3 option liên kết",
       "- Mặc định:「利用しない」— không hiện phần chọn friend info\n"
       "- Bước 2: tự tạo friend info cùng tên trong folder「未分類」\n"
       "- Bước 3: tên friend info bên màn QL cũng ĐỔI THEO\n"
       "- Bước 4: tên item bên màn setting KHÔNG đổi theo (chiều ngược lại không đồng bộ)\n"
       "- Bước 5: friend info bên màn QL VẪN CÒN (không bị xóa)",
       note="Nguồn: Setting calendar r336-r337."),

    tc("予約時のお客様への質問項目", "FRIEND-001", "Normal",
       "Liên kết friend info có sẵn: danh sách chỉ hiện đúng KIỂU tương thích",
       CAL + "\n- Bot có friend info kiểu text, select, date, point, image, pdf",
       "1. Ở item 短文回答, chọn「すでに作成済みの友だち情報に回答を紐付け」→ mở droplist\n"
       "2. Ở item 単一選択 (radio), làm tương tự\n3. Ở item 日時, làm tương tự\n"
       "4. Hover icon tooltip của phần chọn friend info",
       "6 kiểu friend info",
       "- Item 短文回答: droplist CHỈ hiện friend info kiểu TEXT (kèm folder)\n"
       "- Item 単一選択: droplist hiện friend info kiểu TEXT và SELECT\n"
       "- Item 日時: droplist CHỈ hiện friend info kiểu DATE\n"
       "- Tooltip:「すでに友だち情報が記録されている場合 情報が上書きされますのでご注意下さい。」",
       note="Nguồn: Setting calendar r328-r330, r361, r404, r508."),

    tc("予約時のお客様への質問項目", "DATA-001", "Normal",
       "Liên kết friend info kiểu SELECT: tự load option, 2 cột, edit cột 1",
       CAL + "\n- Có friend info kiểu select F_sel với 3 option A/B/C",
       "1. Ở item 単一選択, chọn liên kết với F_sel\n2. Quan sát vùng option\n"
       "3. Sửa nội dung option ở cột 1 → click ra ngoài\n4. Quan sát cột 2",
       "friend info select 3 option",
       "- Tự load 3 option A/B/C ra 2 cột giống nhau\n"
       "- Cột 1 EDIT được, cột 2 bị DISABLE\n"
       "- Sửa cột 1: cột 2 KHÔNG bị thay đổi, save success",
       note="Nguồn: Setting calendar r407-r408."),

    tc("予約時のお客様への質問項目", "STATE-001", "Abnormal",
       "Đổi giữa các option liên kết / đổi kiểu friend info → data option cũ bị clear",
       CAL + "\n- Item 単一選択 đang liên kết friend info kiểu select, đã có 3 option",
       "1. Đổi sang liên kết friend info kiểu TEXT → quan sát vùng option\n"
       "2. Đổi lại về kiểu select → quan sát\n"
       "3. Đổi option liên kết từ「利用しない」sang「自動生成」rồi ngược lại",
       "Đổi kiểu liên kết",
       "- Bước 1: xóa hết option của kiểu cũ, hiện default 1 textbox không có icon xóa\n"
       "- Bước 2: option đã tạo trước đó KHÔNG được khôi phục (đã bị lưu đè khi click ra ngoài)\n"
       "- Bước 3: option MỚI hiện data trống; option CŨ vẫn hiển thị lại được data cũ",
       note="Nguồn: Setting calendar r339, r409, r417, r557, r562-r563."),

    tc("予約時のお客様への質問項目", "FUNC-001", "Normal",
       "Auto-save khi click ra ngoài → hiện toast 3 giây",
       CAL,
       "1. Sửa nội dung 1 item ở khối 3\n2. Click ra ngoài vùng khối 3\n"
       "3. Quan sát góc màn hình\n4. Bấm nút X trên toast",
       "—",
       "- Hiện message「編集が保存されました」và TỰ BIẾN MẤT sau 3 giây\n"
       "- Bấm X: message ẩn ngay",
       note="Nguồn: Setting calendar r338, r369."),

    tc("予約時のお客様への質問項目", "FUNC-MULTI-001", "Normal",
       "Item radio / checkbox: quản lý danh sách option (thêm, xóa, di chuyển, để trống)",
       CAL,
       "1. Thêm item 単一選択 → quan sát vùng option mặc định\n"
       "2. Bấm「選択肢追加」3 lần\n3. Bấm icon xóa 1 option\n"
       "4. Xóa hết option → LINE user mở trang booking\n"
       "5. Để trống 1 textbox option rồi click ra ngoài\n6. Dùng nút di chuyển đổi thứ tự option",
       "—",
       "- Bước 1: KHÔNG hiện option nào; bấm add mới hiện 1 textbox, textbox đầu KHÔNG có icon xóa\n"
       "- Placeholder:「選択肢を入力してください」\n"
       "- Bước 4: LINE user KHÔNG thấy item này (ẩn cả nội dung câu hỏi)\n"
       "- Bước 5: khung textbox chuyển màu đỏ / báo lỗi「選択肢を入力してください」\n"
       "- Bước 6: thứ tự option đổi đúng, hiển thị đúng thứ tự phía LINE user",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r391-r398, r459-r465."),

    tc("予約時のお客様への質問項目", "FUNC-002", "Normal",
       "Item 単一選択: 表示方法 radio button vs dropdown",
       CAL + "\n- Item Q1 kiểu 単一選択 có 3 option",
       "1. Chọn 表示方法 =「ラジオボタン」→ Lưu → LINE user mở trang booking\n"
       "2. Chọn「ドロップダウン」→ Lưu → LINE user mở lại",
       "2 kiểu hiển thị",
       "- Bước 1: phía LINE user hiện 3 radio button\n"
       "- Bước 2: phía LINE user hiện 1 dropdown chứa 3 lựa chọn",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r386-r387."),

    tc("予約時のお客様への質問項目", "FUNC-UNIQ-001", "Abnormal",
       "SpecImprove #33696: option label trùng nhau trong CÙNG item → báo lỗi",
       CAL,
       "1. Tạo item 単一選択, nhập 4 option: A, B, A, C → click ra ngoài\n"
       "2. Sửa option thứ 3 thành D → click ra ngoài\n"
       "3. Tạo item checkbox, nhập option trùng → quan sát\n"
       "4. Nhập option「A」và「A 」(có space cuối) → quan sát",
       "Option trùng và trùng-sau-trim",
       "- Bước 1, 3: báo lỗi「選択肢の表示名が重複しています。異なる値を入力してください。」\n"
       "- Bước 2: Save item success\n"
       "- Bước 4: VẪN báo lỗi trùng (space đầu/cuối bị trim trước khi so sánh)",
       note="Nguồn: Setting calendar r422, r424, r427, r432, r434, r437, r470-r472 "
            "(SpecImprove #33696, 01/2026)."),

    tc("予約時のお客様への質問項目", "FUNC-UNIQ-001", "Normal",
       "SpecImprove #33696: option label trùng GIỮA 2 item khác nhau → CHO PHÉP",
       CAL + "\n- Item Q1 đã có option A, B, C",
       "1. Tạo item Q2 với option A, B, C (trùng hoàn toàn với Q1) → click ra ngoài\n"
       "2. Kiểm 3 nhánh: không liên kết info · tự tạo info · liên kết info có sẵn\n"
       "3. LINE user và admin mở màn booking",
       "2 item option trùng nhau",
       "- Cả 3 nhánh: Save item success (validate chỉ áp dụng TRONG cùng 1 item)\n"
       "- Cả LINE user và admin đều thấy đủ option của cả 2 item",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r429-r431, r439-r443, r473-r475."),

    tc("予約時のお客様への質問項目", "FUNC-001", "Normal",
       "Item 日時: default 当日 / 指定日 và setting ghi nhận giờ",
       CAL,
       "1. Thêm item 日時 → quan sát tooltip và option mặc định\n"
       "2. Chọn「指定日」→ chọn ngày trong quá khứ → Lưu\n"
       "3. Quan sát option「時間の記録」mặc định\n"
       "4. Chọn「利用する」→ quan sát phần liên kết friend info\n"
       "5. LINE user mở trang booking, quan sát ô ngày",
       "2 kiểu default date × 2 kiểu ghi giờ",
       "- Tooltip:「初めから入力されている日付を設定します。」\n"
       "- Default「当日」: LINE user thấy ngày hôm nay\n"
       "- 指定日: hiện datepicker format yyyy-mm-dd; chọn ngày quá khứ vẫn Save success; "
       "LINE user thấy ngày đã chọn\n"
       "- 時間の記録 mặc định「利用しない」: LINE user KHÔNG có ô chọn giờ, item liên kết được friend info\n"
       "- Chọn「利用する」: LINE user CÓ ô chọn giờ, phần liên kết friend info bị ẨN HOÀN TOÀN\n"
       "- Tooltip:「時間の記録を利用しない場合、日付だけの登録となります。なお、時間の記録を利用する場合、"
       "友だち情報への回答記録は利用できません。」",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r492-r500, r507-r511."),

    tc("予約時のお客様への質問項目", "FUNC-001", "Normal",
       "Xóa item: alert xác nhận và reload màn hình",
       CAL + "\n- Có 3 item tự tạo",
       "1. Chọn item Q2 → bấm「この項目を削除」→ quan sát alert\n"
       "2. Xác nhận xóa\n3. Quan sát khối 2 và khối 3",
       "3 item",
       "- Alert:「この質問を削除しますがよろしいですか？」\n"
       "- Sau khi xác nhận: Q2 biến mất khỏi khối 2, màn hình reload và hover về item đầu tiên",
       note="Nguồn: Setting calendar r340, r371, r418, r466, r512."),

    tc("予約時のお客様への質問項目", "OUT-PREVIEW-001", "Normal",
       "Nút preview màn 質問項目: mở tab mới, hiện đúng item, nút next disable",
       CAL + "\n- Có 5 item đã tạo",
       "1. Bấm nút preview\n2. Quan sát nội dung\n3. Thử fill data\n4. Bấm nút「決済情報入力にすすむ」",
       "5 item",
       "- Mở tab mới\n- Hiện đủ 5 item theo đúng thứ tự đã tạo\n"
       "- Fill được data (chỉ để xem, không lưu)\n- Nút「決済情報入力にすすむ」KHÔNG click được",
       note="Nguồn: Setting calendar r276-r279."),

    # ══════════════════ SpecChange #26462 — 2 item mặc định khi ON bill tiền ══════════════════
    tc("予約時のお客様への質問項目", "PAY-STATE-001", "Normal",
       "SpecChange #26462: ON bill tiền → 2 item mặc định bị ép bắt buộc và ẩn setting",
       CAL + "\n- Calendar đang ON bill tiền",
       "1. Vào màn 質問項目, chọn item họ tên → quan sát các khối setting\n"
       "2. Chọn item email → quan sát\n"
       "3. Query `calendar_setting_send_forms` 2 bản ghi mặc định",
       "Calendar ON bill tiền",
       "- Cả 2 item: ẨN các khối「表示設定」「回答設定」「入力内容」\n"
       "- Item họ tên: bắt buộc nhập; DB `enable` = 1, `required` = 1, `rule_type` = 0\n"
       "- Item email: bắt buộc nhập + validate email; DB `enable` = 1, `required` = 1, "
       "`rule_type` = 1, `rule_validation_type` = 'email'",
       note="Nguồn: Setting calendar r810-r813 (SpecChange #26462, 08/2024) + spec BR-50."),

    tc("予約時のお客様への質問項目", "PAY-STATE-001", "Abnormal",
       "SpecChange #26462: OFF bill tiền → 2 item mặc định setting bình thường",
       CAL + "\n- Calendar đang OFF bill tiền",
       "1. Vào màn 質問項目, chọn item họ tên → quan sát\n"
       "2. Đổi item họ tên sang 任意 và OFF hiển thị → Lưu\n"
       "3. LINE user và admin mở màn booking",
       "Calendar OFF bill tiền",
       "- Hiện đủ các khối setting 表示設定 / 回答設定 / 入力内容\n"
       "- Đổi sang 任意 và OFF: save success\n"
       "- LINE user và admin: item họ tên KHÔNG hiển thị (do đã OFF)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Setting calendar r817-r819 — TC gốc CHỈ CÓ TIÊU ĐỀ, expected do AI bổ sung."),

    tc("予約時のお客様への質問項目", "PAY-STATE-001", "Abnormal",
       "Bật bill tiền khi item mặc định đang OFF hoặc 任意 → chặn + message",
       CAL + "\n- Calendar đang OFF bill tiền",
       "Với từng tổ hợp, thử bật bill tiền và ghi kết quả:\n"
       "1. Item mặc định OFF + không required\n2. Item mặc định ON + không required\n"
       "3. Item mặc định OFF + required\n4. Item mặc định ON + required",
       "4 tổ hợp",
       "- Tổ hợp 1, 2, 3: KHÔNG bật được bill tiền; tổ hợp 2 báo lỗi cần chuyển item mặc định "
       "sang required\n- Tổ hợp 4: bật bill tiền thành công",
       note="Nguồn: Setting calendar r286-r289, r299-r301."),

    tc("予約時のお客様への質問項目", "DATA-REF-001", "Normal",
       "Có item KHÁC cũng liên kết vào họ tên / email → quy tắc lấy data",
       CAL + "\n- Ngoài 2 item mặc định, tạo thêm item Q_name liên kết friend info systemname\n"
             "- Calendar ON bill tiền",
       "1. Kiểm điều kiện bật bill tiền\n2. LINE user booking, nhập giá trị KHÁC NHAU cho "
       "item mặc định và Q_name\n3. Kiểm màn nhập thẻ và màn mypage friend info",
       "2 item cùng liên kết 1 friend info",
       "- Bước 1: bật bill tiền CHỈ kiểm ON/OFF của item MẶC ĐỊNH (item Q_name không ảnh hưởng)\n"
       "- Màn bill tiền lấy data của item MẶC ĐỊNH\n"
       "- Friend info trên mypage lấy data của item MỚI NHẤT",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r296-r298."),

    tc("予約時のお客様への質問項目", "DATA-MIG-001", "Normal",
       "SpecChange #26462 — recover data: item mặc định đang required=0 khi ON bill tiền",
       CAL + "\n- Trước khi release: bot đang ON bill tiền nhưng item họ tên/email đã bị đổi "
             "sang không required (`required` = 0)",
       "1. Chạy query tìm dữ liệu cần recover:\n"
       "`SELECT * FROM calendar_setting_send_forms a JOIN calendar_management b "
       "ON a.calendar_id = b.id WHERE a.can_delete = 0 AND a.link_friend_information = 3 "
       "AND a.friend_information_id = -1 AND b.is_use_payment = 1`\n"
       "2. Chạy recover\n3. Query lại 2 bản ghi\n4. Mở màn 質問項目 trên GUI",
       "Bản ghi required = 0",
       "- Sau recover: item họ tên có `enable` = 1, `required` = 1, `rule_type` = 0\n"
       "- Item email có `enable` = 1, `required` = 1, `rule_type` = 1, `rule_validation_type` = 'email'\n"
       "- GUI: ẩn các khối 表示設定 / 回答設定 / 入力内容",
       note="Nguồn: Setting calendar r820-r821."),

    # ══════════════════ Bộ TC Create/Edit Form (#29272) ══════════════════
    tc("予約時のお客様への質問項目", "FUNC-001", "Normal",
       "Điều hướng vào màn Setting Form từ menu 予約管理",
       CAL,
       "1. Bấm tab 予約管理\n2. Bấm submenu レッスン予約\n3. Bấm nút「+ 新規作成」",
       "—",
       "- Hiển thị giao diện màn hình 新規作成",
       note="Nguồn: Setting calendar r584 (bộ TC redmine #29272)."),

    tc("予約時のお客様への質問項目", "UI-001", "Normal",
       "Màn Setting Form của calendar MỚI: 5 loại item đều hiển thị data trắng",
       CAL + "\n- Calendar vừa được tạo mới",
       "1. Vào màn Setting Form\n2. Thêm lần lượt 5 loại item: 短文回答 · 長文回答 · 単一選択 · "
       "複数選択 · 日時\n3. Quan sát khối 3 của từng loại",
       "5 loại item",
       "- Cả 5 loại đều hiển thị TRẮNG data (không có giá trị mặc định lạ)",
       note="Nguồn: Setting calendar r585-r589."),

    tc("予約時のお客様への質問項目", "DATA-001", "Normal",
       "質問内容 nhập / không nhập × phía admin và LINE user (5 loại item)",
       CAL,
       "Với từng loại item (短文回答 · 長文回答 · 単一選択 · 複数選択 · 日時):\n"
       "1. Nhập 質問内容 → Lưu → kiểm màn admin book và màn LINE user\n"
       "2. Để trống 質問内容 → Lưu → kiểm lại",
       "5 loại item × 2 nhánh",
       "- Có nhập: admin Lưu thay đổi; LINE user HIỂN THỊ câu hỏi (item 日時 hiện calendar)\n"
       "- Không nhập: admin vẫn Lưu thay đổi; LINE user KHÔNG hiển thị câu hỏi (và không hiện calendar)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r591-r594, r608-r611, r625-r628, r642-r645, r647-r650."),

    tc("予約時のお客様への質問項目", "DATA-001", "Normal",
       "Checkbox すでに友だち情報が登録されている場合、初めから入力された状態にする — 4 tổ hợp",
       CAL + "\n- U1 đã có giá trị friend info từ lần booking trước",
       "Với 2 option liên kết (自動生成 và すでに作成済み), làm 2 nhánh:\n"
       "1. TÍCH checkbox → admin book → LINE user book lần 1, lần 2, lần N\n"
       "2. KHÔNG tích checkbox → admin book → LINE user book lần 1, lần 2",
       "2 option × 2 nhánh checkbox",
       "- TÍCH: admin lưu và GHI LẠI câu trả lời; LINE user lần 1 trắng data, "
       "lần 2 hiện friend info lần 1, lần N hiện friend info lần N-1\n"
       "- KHÔNG tích: admin lưu nhưng KHÔNG hiển thị bên friend info; LINE user KHÔNG được fill sẵn",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r597-r606, r614-r623, r631-r640. ⚠️ r601 và r618 ghi kết quả "
            "khác nhau cho CÙNG tổ hợp (「không hiển thị bên friend info」vs「không ghi lại câu trả lời」) "
            "— xem MT-32."),

    tc("予約時のお客様への質問項目", "DATA-001", "Normal",
       "Item 日時 + デフォルト日付 = 当日: ngày mặc định phía LINE user theo 2 nhánh checkbox",
       CAL + "\n- Item 日時 setting デフォルト日付 =「当日」, liên kết friend info kiểu date\n"
             "- U1 đã lưu ngày 2026-01-15 vào friend info này",
       "1. TÍCH checkbox 初めから入力された状態にする → admin book cho U1 → quan sát ô ngày\n"
       "2. LINE user U1 mở trang booking → quan sát ô ngày\n"
       "3. BỎ tích checkbox → lặp bước 1-2",
       "friend info đã có giá trị",
       "- TÍCH: cả admin và LINE user đều thấy ngày mặc định = 2026-01-15 (ngày đã lưu ở friend info)\n"
       "- KHÔNG tích: cả 2 đều thấy ngày mặc định = HÔM NAY",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r651-r664."),
]
