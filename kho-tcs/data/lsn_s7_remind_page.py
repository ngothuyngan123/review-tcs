# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm 全体設定 phần 2: リマインド, 空き枠通知, 予約ページ表示設定 & filter,
トップ・店舗情報・利用規約, 予約システムの削除, Googleスプレッドシート連携.

Nguồn chính: 11.2 TCsLine_LessonCalendar → tab「Setting calendar」r827-r1610
  (SpecImprove #36037 04/2026 thứ tự remind · SpecChange #32367 10/2025 remind theo end time ·
   Support #33648 01/2026 recover remind · Bug KH #36729 05/2026 キャンセル用URL ·
   Bug #31595 09/2025 sync giờ lên Google · Support #32733 11/2025 cảnh báo liên kết lại Google)
Bổ sung: tab「Task nhỏ + fix bug KH」r145-r185 (retry sync Google).
Spec: BR-32…BR-43, BR-53…BR-55, BR-P30, BR-P31, BR-P32, job-spec §10.3.
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, có 3 course C1/C2/C3\n"
       "- Mở /basic/calendar-management/21 > tab 全体設定")

S7 = [
    # ══════════════════ リマインド — cài đặt ══════════════════
    tc("リマインド — cài đặt", "UI-001", "Normal",
       "Màn setting remind: 2 label và remind mặc định được tạo lazy",
       CAL + "\n- Calendar VỪA tạo mới, CHƯA từng mở tab remind",
       "1. Vào menu「予約前後に送るリマインドメッセージ」lần đầu\n"
       "2. Quan sát 2 label và danh sách remind\n"
       "3. Query bảng `events` (type = 4) và `event_step`\n"
       "4. Đóng và mở lại tab remind lần 2 → query lại\n"
       "5. Xóa remind mặc định, mở lại tab remind → query lại",
       "Calendar mới",
       "- 2 label:「コース開始前のメッセージ・アクション」và「コース終了後のメッセージ・アクション」\n"
       "- Lần đầu mở: TỰ TẠO 1 remind trước 1 ngày lúc 10:00 và 1 remind sau 1 ngày lúc 10:00; "
       "DB có bản ghi `events` type = 4 và `event_step` tương ứng\n"
       "- Lần 2: KHÔNG tạo lại remind mặc định (không nhân đôi)\n"
       "- Sau khi xóa rồi mở lại: KHÔNG tạo lại remind mặc định",
       note="Nguồn: Setting calendar r829-r831, r856 + spec BR-07 (lazy-create) và BR-37."),

    tc("リマインド — cài đặt", "UI-003", "Normal",
       "Format hiển thị mốc remind — 2 kiểu timing × trước/sau course",
       CAL + "\n- Đã tạo: remind trước kiểu ngày (1 ngày lúc 10:00), remind trước kiểu duration "
             "(2 giờ 30 phút), remind sau kiểu ngày (1 ngày lúc 10:00), remind sau kiểu duration",
       "1. Quan sát format hiển thị của 4 mốc remind ở màn list",
       "4 mốc remind",
       "- Trước + kiểu ngày:「コース開始 1日前の 10時00分」\n"
       "- Trước + duration:「コース開始 2 時間 30 分 前」\n"
       "- Sau + kiểu ngày:「コース終了 1日後の 10時00分」\n"
       "- Sau + duration:「コース終了 <hh> 時間 <mm> 分 前」",
       note="Nguồn: Setting calendar r832-r833, r857-r858. ⚠️ Format remind SAU kiểu duration ghi "
            "chữ「前」— nhiều khả năng là lỗi hiển thị (phải là 後). Xem MT-33."),

    tc("リマインド — cài đặt", "UI-001", "Normal",
       "Marker filter course trên mốc remind",
       CAL + "\n- Remind R1 có filter theo course, remind R2 không có filter",
       "1. Quan sát dòng R1 và R2 ở màn list remind",
       "2 remind",
       "- R1: hiện「コースごとの絞り込みが設定されています」\n"
       "- R2: hiện「コースごとの絞り込みは設定されていません」",
       note="Nguồn: Setting calendar r834-r835, r859-r860."),

    tc("リマインド — cài đặt", "OUT-PREVIEW-001", "Normal",
       "Hover mốc remind → hiện nút プレビュー・編集 và mở popup preview",
       CAL + "\n- Đã có remind R1 với message text + 2 action, 1 action có filter",
       "1. Hover lên R1 → quan sát\n2. Bấm「プレビュー・編集」\n"
       "3. Quan sát tab メッセージ và tab アクション\n4. Bấm nút X",
       "1 remind có msg + action",
       "- Hover: hiện nút phủ màu #5799DBCC lên mốc remind\n"
       "- Popup preview trượt từ phải vào giữa, title đúng「コース開始前のメッセージ・アクション」\n"
       "- Tab メッセージ: hiện nội dung msg text (nếu chọn không dùng thì hiện "
       "「メッセージが登録されていません」)\n"
       "- Tab アクション: hiện 2 action, action có filter hiện nút filter, có scroll dọc\n"
       "- Bấm X: đóng popup, về màn setting remind",
       note="Nguồn: Setting calendar r836-r837, r848-r851, r854."),

    tc("リマインド — cài đặt", "LIST-001", "Normal",
       "SpecImprove #36037: thứ tự hiển thị remind TRƯỚC course",
       CAL + "\n- Tạo các mốc remind TRƯỚC: R1 (3 ngày 10:00), R2 (1 ngày 10:00), "
             "R3 (1 ngày 15:00), R4 (2 giờ 00), R5 (30 phút)",
       "1. Vào màn setting remind\n2. Quan sát thứ tự từ trên xuống của khối コース開始前",
       "5 mốc remind trước",
       "- Remind kiểu CHỈ ĐỊNH NGÀY xếp TRÊN, kiểu CHỈ ĐỊNH GIỜ xếp DƯỚI\n"
       "- Trong nhóm chỉ định ngày: ngày LỚN HƠN lên trên (R1 3 ngày → R2/R3 1 ngày)\n"
       "- Cùng ngày: cần chốt quy tắc theo giờ (TC gốc ghi 2 câu MÂU THUẪN)\n"
       "- Trong nhóm chỉ định giờ: giờ LỚN HƠN lên trên (R4 2 giờ → R5 30 phút)\n"
       "- Cuối cùng là marker「コース開始」",
       spec="Đã hỏi leader",
       note="🔴 Nguồn: Setting calendar r838-r841 (SpecImprove #36037, 04/2026). "
            "r840 ghi ĐỒNG THỜI「giờ lớn hơn hiện ở trên」VÀ「Giờ nhỏ hơn hiện ở trên」— "
            "TỰ MÂU THUẪN trong 1 ô. Xem MT-34."),

    tc("リマインド — cài đặt", "LIST-001", "Normal",
       "SpecImprove #36037: thứ tự hiển thị remind SAU course (ngược với remind trước)",
       CAL + "\n- Tạo remind SAU: R6 (1 ngày 10:00), R7 (3 ngày 10:00), R8 (1 ngày 08:00), "
             "R9 (2 giờ), R10 (30 phút)",
       "1. Quan sát thứ tự khối コース終了後",
       "5 mốc remind sau",
       "- Đầu tiên là marker「コース終了」\n"
       "- Remind kiểu CHỈ ĐỊNH GIỜ xếp TRÊN, kiểu CHỈ ĐỊNH NGÀY xếp DƯỚI (NGƯỢC với remind trước)\n"
       "- Trong nhóm chỉ định ngày: ngày NHỎ HƠN lên trên\n"
       "- Cùng ngày: giờ NHỎ HƠN lên trên\n"
       "- Trong nhóm chỉ định giờ: giờ NHỎ HƠN lên trên\n"
       "⇒ Toàn bộ danh sách xếp theo thời điểm gửi thật, gần buổi học nhất ở gần marker",
       note="Nguồn: Setting calendar r863-r866."),

    tc("リマインド — cài đặt", "LIST-001", "Normal",
       "SpecImprove #36037: sau khi tạo / sửa time / xóa remind → thứ tự tự sắp lại đúng",
       CAL + "\n- Đã có 4 mốc remind trước và 3 mốc remind sau",
       "1. Tạo thêm 1 remind mới → quan sát thứ tự\n"
       "2. Sửa time của 1 remind giữa danh sách → quan sát\n3. Xóa 1 remind → quan sát",
       "7 → 8 → 8 → 7 mốc",
       "- Sau mỗi thao tác, danh sách tự sắp lại đúng thứ tự theo quy tắc trên (không cần F5)",
       note="Nguồn: Setting calendar r843, r868."),

    tc("リマインド — cài đặt", "FUNC-003", "Abnormal",
       "Popup chọn timing remind TRƯỚC — kiểu 日時で指定: validate ngày và giờ",
       CAL,
       "1. Bấm「送信タイミングを追加する」→ chọn kiểu「日時で指定」\n"
       "2. Để trống ô ngày → Lưu\n3. Nhập 0 → Lưu\n4. Nhập 100 → Lưu\n"
       "5. Nhập 1.5 → Lưu\n6. Nhập -1 → quan sát ô nhập\n"
       "7. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → Lưu từng giá trị",
       "6 giá trị ngày + 4 mốc giờ",
       "- Để trống: báo lỗi\n- Nhập 0: Save success\n- Nhập 100: Save success\n"
       "- Nhập 1.5: báo lỗi\n- Nhập -1: KHÔNG cho nhập\n- Cả 4 mốc giờ: Save success",
       note="Nguồn: Setting calendar r884-r892."),

    tc("リマインド — cài đặt", "FUNC-001", "Normal",
       "Popup chọn timing remind: 2 kiểu và công thức tính thời điểm gửi",
       CAL + "\n- Course start 10:00 ngày 20/04, kết thúc 11:00 cùng ngày",
       "1. Tạo remind TRƯỚC kiểu 日時で指定: 1 ngày lúc 08:00 → Lưu\n"
       "2. Tạo remind TRƯỚC kiểu 経過時間で指定: 1 giờ 00 phút → Lưu\n"
       "3. Tạo remind SAU kiểu 日時で指定: 1 ngày lúc 08:00 → Lưu\n"
       "4. Tạo remind SAU kiểu 経過時間で指定: 1 giờ 00 phút → Lưu\n"
       "5. Cho U1 booking course này → query `event_step_time.sent_date_time`",
       "4 mốc remind",
       "- Remind 1: gửi lúc 08:00 ngày 19/04\n- Remind 2: gửi lúc 09:00 ngày 20/04\n"
       "- Remind 3: gửi lúc 08:00 ngày 21/04\n- Remind 4: gửi lúc 12:00 ngày 20/04 "
       "(tính theo giờ KẾT THÚC 11:00)",
       note="Nguồn: Setting calendar r883, r893, r933, r941 + spec BR-38/BR-39."),

    tc("リマインド — cài đặt", "CONC-001", "Abnormal",
       "Popup timing: click nhiều lần nút 決定 → chỉ tạo 1 bản ghi; nút X đóng không tạo",
       CAL,
       "1. Nhập timing hợp lệ, click nhanh 3 lần nút「決定」\n"
       "2. Query `event_step`\n3. Mở lại popup, nhập timing rồi bấm X",
       "1 mốc timing",
       "- Chỉ tạo ĐÚNG 1 bản ghi trong `event_step`, mở màn tạo action/filter cho timing đó\n"
       "- Bấm X: đóng popup, quay về màn setting remind, không tạo bản ghi",
       note="Nguồn: Setting calendar r899-r900, r944-r945."),

    tc("リマインド — cài đặt", "FUNC-002", "Normal",
       "Filter course của remind: default OFF, bật ON và các tổ hợp chọn course",
       CAL + "\n- Calendar có 5 course",
       "1. Mở màn setting msg/action của 1 remind → quan sát khối「コースの絞り込み設定」\n"
       "2. Quan sát option mặc định\n3. Bật ON → quan sát course được chọn sẵn\n"
       "4. Bỏ hết course → Lưu\n5. Giữ course mặc định → Lưu\n"
       "6. Chọn thêm course khác → Lưu\n7. Bỏ course mặc định, chọn course khác → Lưu\n"
       "8. Chọn all course → Lưu\n9. Đổi từ ON về OFF → Lưu",
       "5 course",
       "- Khối hiện list all course của calendar, hiển thị 3 course đầu, còn lại scroll\n"
       "- Default: OFF ⇒ insert `event_step_time` khi có booking của TẤT CẢ course\n"
       "- Bật ON: tự chọn course ĐẦU TIÊN của list\n"
       "- Bước 4: báo lỗi (phải chọn ít nhất 1 course)\n"
       "- Bước 5-8: save success, chỉ gửi remind cho các course đã chọn\n"
       "- Bước 9: save success, quay về gửi cho tất cả course",
       note="Nguồn: Setting calendar r904-r912, r948-r952."),

    tc("リマインド — cài đặt", "MSG-002", "Normal",
       "Nội dung message remind: mẫu mặc định của remind TRƯỚC và SAU khác nhau",
       CAL,
       "1. Ở remind TRƯỚC, bấm「例文を挿入する」→ ghi nội dung\n"
       "2. Ở remind SAU, bấm「例文を挿入する」→ ghi nội dung",
       "2 loại remind",
       "- Remind TRƯỚC: mẫu chứa「ご予約の【1日前】となりましたので、念のためお知らせ申し上げます。」"
       "+ 4 mục 予約日時 / ご予約コース名 / コース料金 / 変更・キャンセル用 URL\n"
       "- Remind SAU: mẫu chứa「昨日はご来店、誠にありがとうございました。またのお越しを心よりお待ち"
       "しております。」\n- 2 nội dung PHẢI khác nhau",
       note="Nguồn: Setting calendar r919, r959. ⚠️ Spec BR-43: mẫu chứa chuỗi CỨNG「1日前」/「昨日」"
            "— KHÔNG đổi theo `before_day` thực tế ⇒ nếu setting 3 ngày trước thì nội dung vẫn ghi "
            "「1日前」. Xem MT-35."),

    tc("リマインド — cài đặt", "MSG-002", "Normal",
       "Message remind: bỏ bớt phần thông tin course vẫn replace được phần còn lại",
       CAL + "\n- Message remind đã insert đủ mẫu",
       "1. Xóa dòng chứa mã コース名 khỏi message → Lưu\n2. Cho U1 booking → chờ remind gửi\n"
       "3. Kiểm tin LINE U1",
       "Message thiếu 1 mã",
       "- U1 nhận tin, các mã còn lại (ngày giờ, số tiền, URL hủy) VẪN thay đúng giá trị",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r920."),

    tc("リマインド — cài đặt", "FUNC-004", "Boundary",
       "Message remind: 利用しない, biên 5000/5001 ký tự, và setting action khác",
       CAL,
       "1. Tích「利用しない」→ quan sát textbox → Lưu → cho U1 booking\n"
       "2. Bỏ tích, nhập 5000 ký tự Nhật → Lưu\n3. Nhập 5001 ký tự → Lưu\n"
       "4. Chưa setting action nào → quan sát khối action\n5. Bấm「アクション登録・編集」",
       "利用しない · 5000 · 5001 ký tự",
       "- Bước 1: textbox disable, U1 KHÔNG nhận msg remind (nhưng vẫn nhận multi action nếu có)\n"
       "- 5000 ký tự: save success\n- 5001 ký tự: Invalid\n"
       "- Bước 4: hiện「エルメアクションが登録されていません」\n- Bước 5: mở modal action",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r921-r926, r960-r965."),

    tc("リマインド — cài đặt", "FUNC-001", "Normal",
       "Nút xóa / Lưu / Back ở màn setting msg-action của remind",
       CAL + "\n- Đang ở màn setting của remind R1",
       "1. Bấm「このメッセージ・アクションを削除する」→ quan sát alert → OK\n"
       "2. Tạo lại remind, sửa nội dung, click nhiều lần nút「保存」\n"
       "3. Tạo remind khác, sửa nội dung rồi bấm「戻る」",
       "—",
       "- Bước 1: hiện alert; bấm OK thì xóa remind tương ứng, về màn setting remind\n"
       "- Bước 2: chỉ hiện 1 lần toast đã lưu (3 giây), không lưu 2 lần\n"
       "- Bước 3: về màn setting remind, preview VẪN là data CŨ (thay đổi chưa lưu bị bỏ)",
       note="Nguồn: Setting calendar r928-r930, r967-r969, r1104-r1106, r1116-r1118."),

    tc("リマインド — cài đặt", "FUNC-002", "Normal",
       "Edit remind: sửa timing / filter / message / action rồi Lưu → preview cập nhật",
       CAL + "\n- Remind R1 đã có timing, filter 2 course, message text và 1 action",
       "1. Từ popup preview bấm「編集する」→ quan sát data\n"
       "2. Sửa timing, thêm 1 course vào filter, đổi nội dung msg, thêm 1 action → Lưu\n"
       "3. Quay lại màn setting remind → mở lại preview",
       "1 remind đầy đủ",
       "- Bước 1: màn edit hiện đúng toàn bộ data hiện có của R1\n"
       "- Bước 3: preview hiển thị data MỚI (timing mới, 3 course, msg mới, 2 action)",
       note="Nguồn: Setting calendar r1094, r1105, r1117."),

    # ══════════════════ リマインド — job gửi & recover ══════════════════
    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "Add remind vào event_step_time theo trạng thái booking (6 nhánh)",
       CAL + "\n- Đã setting 1 remind trước và 1 remind sau, slot ở TƯƠNG LAI",
       "Với từng nhánh, thực hiện thao tác rồi query `event_step_time` theo `user_booking_id`:\n"
       "1. Admin book\n2. User book được approve luôn\n3. User book chờ approve (lúc vừa book)\n"
       "4. Admin approve booking đó\n5. Admin từ chối booking\n6. User đăng ký đợi nhận thông báo",
       "6 nhánh",
       "- Nhánh 1, 2, 4: CÓ insert bản ghi `event_step_time` (status = 0)\n"
       "- Nhánh 3, 5, 6: KHÔNG insert bản ghi nào\n"
       "⇒ Chỉ booking vào status ∈ {1, 2} mới sinh remind",
       note="Nguồn: Setting calendar r970-r975 + spec BR-P30."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "Xóa remind khỏi event_step_time theo thao tác cancel (5 nhánh)",
       CAL + "\n- Booking B1 đã có 2 bản ghi `event_step_time` status = 0",
       "Với từng nhánh, thực hiện rồi query `event_step_time`:\n"
       "1. Admin cancel booking\n2. User cancel được approve luôn\n"
       "3. User request cancel (lúc vừa bấm)\n4. Admin approve request cancel\n"
       "5. Admin từ chối request cancel",
       "5 nhánh",
       "- Nhánh 1, 2, 4: XÓA các bản ghi `event_step_time` có status = 0\n"
       "- Nhánh 3, 5: KHÔNG xóa",
       note="Nguồn: Setting calendar r982-r986."),

    tc("リマインド — job gửi & recover", "MSG-003", "Abnormal",
       "Friend bị block / block bot → vẫn insert event_step_time nhưng KHÔNG gửi",
       CAL + "\n- Đã setting remind, U1 đã booking thành công và có `event_step_time`",
       "1. Bot block U1 (`bot_line_user.is_block` = 1) → chờ tới giờ remind → kiểm LINE U1\n"
       "2. Thêm remind mới hợp lệ trong lúc U1 đang bị block → query `event_step_time` → "
       "chờ tới giờ → kiểm\n3. U1 block bot → lặp\n4. U1 bỏ block bot → chờ tới giờ remind → kiểm",
       "Trạng thái block 2 chiều",
       "- Bước 1, 3: `event_step_time` VẪN có bản ghi nhưng đến giờ KHÔNG gửi remind\n"
       "- Bước 2: vẫn insert bản ghi, đến giờ KHÔNG gửi\n"
       "- Bước 4: sau khi bỏ block, remind chưa gửi VẪN gửi bình thường",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r976-r981."),

    tc("リマインド — job gửi & recover", "FUNC-002", "Normal",
       "Filter course của remind: add remind theo course thỏa/không thỏa filter",
       CAL + "\n- Remind R1 có filter chỉ course C1",
       "1. Admin book cho U1 course C1 → query `event_step_time`\n"
       "2. Admin book cho U2 course C2 → query\n3. Lặp với LINE user tự book",
       "2 course, 1 trong filter",
       "- Booking course C1: CÓ add remind (thỏa thời gian và filter)\n"
       "- Booking course C2: KHÔNG add remind dù thỏa thời gian",
       note="Nguồn: Setting calendar r987-r990."),

    tc("リマインド — job gửi & recover", "STATE-001", "Normal",
       "Course OFF sau khi user booking → VẪN gửi remind (spec change)",
       CAL + "\n- U1 đã booking course C1, đã có `event_step_time`",
       "1. Kiểm remind gửi bình thường khi C1 đang ON\n"
       "2. Tắt C1 = OFF → chờ tới giờ remind → kiểm LINE U1 và query `event_step_time.status`\n"
       "3. Bật lại C1 = ON → chờ remind khác → kiểm",
       "1 course bật/tắt",
       "- Bước 1, 3: U1 nhận remind, `status` = 2 (đã gửi)\n"
       "- Bước 2: theo SPEC CHANGE — U1 VẪN nhận remind, `status` = 2\n"
       "  ⚠️ Spec CŨ: không gửi và update `status` = 5 ⇒ nếu thấy `status` = 5 thì là code cũ",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r999-r1001, r1030. Spec RJ-09 xác nhận "
            "`STATUS_SKIP_COURSE_OFF` = 5 là CODE CHẾT (nhánh set nó đã bị comment) ⇒ khớp spec change."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "Add remind mới → backfill cho booking đã có, theo 6 trạng thái booking",
       CAL + "\n- Đã có sẵn 6 booking ở 6 trạng thái: approve (1), admin book (2), "
             "chờ approve (0), deny (6), đợi nhận thông báo (3), request cancel (5), cancel (4/7)",
       "1. Thêm mốc remind TRƯỚC mới (thời điểm gửi còn ở tương lai) → query `event_step_time`\n"
       "2. Thêm mốc remind SAU mới → query",
       "7 booking đủ trạng thái",
       "- Booking status 1, 2, 5: CÓ backfill thêm bản ghi `event_step_time`\n"
       "- Booking status 0, 3, 4, 6, 7: KHÔNG backfill\n"
       "- Mốc TRƯỚC tính `sent_date_time` theo start time; mốc SAU tính theo END time của booking\n"
       "- Backfill đủ cho TOÀN BỘ user đã booking lesson này",
       note="Nguồn: Setting calendar r1048-r1059 (SpecChange #32367)."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "Sửa timing remind → tính lại event_step_time (hợp lệ ⇄ không hợp lệ)",
       CAL + "\n- Có remind R1 và các booking tương lai đã có `event_step_time`",
       "1. Sửa timing R1 từ hợp lệ → không hợp lệ (thời điểm gửi rơi vào quá khứ) → query\n"
       "2. Sửa ngược lại → query\n3. Lặp cho cả 2 kiểu timing (ngày và duration), "
       "cả remind trước và remind sau\n4. Xóa remind R1 → query",
       "4 tổ hợp × 2 chiều",
       "- Đổi sang KHÔNG hợp lệ: XÓA bản ghi `event_step_time` tương ứng\n"
       "- Đổi sang HỢP LỆ: tạo lại / cập nhật `sent_date_time` cho các booking thỏa mãn\n"
       "- Xóa remind: xóa toàn bộ `event_step_time` tương ứng",
       note="Nguồn: Setting calendar r1010-r1019, r1060-r1068."),

    tc("リマインド — job gửi & recover", "STATE-CLEAN-001", "Normal",
       "Xóa booking / slot / course / calendar → xóa event_step_time tương ứng",
       CAL + "\n- Có booking, slot, course, calendar đều có remind trong `event_step_time`",
       "1. Cancel rồi xóa 1 booking → query `event_step_time`\n"
       "2. Cancel hết booking rồi xóa 1 slot → query\n3. Xóa 1 course → query\n"
       "4. Xóa cả calendar → query",
       "4 mức xóa",
       "- Cả 4 mức: các bản ghi `event_step_time` liên quan đều bị xóa\n"
       "- Không còn bản ghi mồ côi trỏ tới booking/slot/course/calendar đã xóa",
       note="Nguồn: Setting calendar r1019-r1023."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "Job gửi remind: 3 tổ hợp message text × multi action",
       CAL + "\n- U1 đã booking, có remind sắp tới giờ gửi",
       "1. Remind KHÔNG set message text, chỉ có multi action → chờ tới giờ → kiểm LINE U1\n"
       "2. Remind có msg text + tích「利用する」+ multi action → kiểm\n"
       "3. Remind có msg text nhưng tích「利用しない」+ multi action → kiểm",
       "3 tổ hợp",
       "- Tổ hợp 1: U1 chỉ nhận multi action, KHÔNG có msg text\n"
       "- Tổ hợp 2: U1 nhận msg text + multi action\n"
       "- Tổ hợp 3: U1 chỉ nhận multi action",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1024-r1026, r1119-r1122."),

    tc("リマインド — job gửi & recover", "MSG-002", "Normal",
       "Job gửi remind: replace đủ mã và format hiển thị phía LINE user",
       CAL + "\n- Message remind chèn đủ: thông tin booking (5 mã) · {name} · friend info basic · "
             "friend info khác\n- U1 booking slot 25/02/2026 00:00-01:00 của course C1 giá 5.000 yên",
       "1. Chờ tới giờ remind → kiểm tin LINE U1\n2. Đối chiếu từng mã",
       "Đủ các loại mã",
       "- Ngày giờ booking hiển thị「2026年02月25日（水）00:00-01:00」— chữ（水）cùng dòng với ngày\n"
       "- Tên course: đúng tên course đã book\n- Số tiền: đúng số tiền của booking\n"
       "- URL cancel: bấm được, mở đúng màn hủy booking của U1\n"
       "- Tên calendar: đúng tên hiển thị phía LINE user\n"
       "- {name} và friend info: đúng giá trị của U1",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1123-r1133. RULE-06/RULE-07."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "SpecChange #32367: remind SAU tính theo END time, remind TRƯỚC theo START time",
       CAL + "\n- Course C1 slot 10:00-11:00 ngày 20/04\n"
             "- Remind trước 1 giờ (`event_step.is_after_day` = 0), remind sau 1 giờ (= 1)",
       "1. Admin book ở WEB cho U1 → query `event_step_time.sent_date_time`\n"
       "2. Admin book ở APP cho U2 → query\n3. U3 tự book approve ngay → query\n"
       "4. U4 book chờ approve, admin approve ở WEB → query\n5. Admin approve ở APP → query",
       "5 lối tạo booking",
       "- Cả 5 lối: remind TRƯỚC có `sent_date_time` = 09:00 ngày 20/04 (start − 1 giờ)\n"
       "- Remind SAU có `sent_date_time` = 12:00 ngày 20/04 (END 11:00 + 1 giờ)",
       note="Nguồn: Setting calendar r1032-r1039 (SpecChange #32367, 10/2025)."),

    tc("リマインド — job gửi & recover", "JOB-001", "Normal",
       "SpecChange #32367: xóa remind khi cancel — cả web và app mobile",
       CAL + "\n- U1 đã booking, có remind chưa gửi",
       "1. U1 cancel được approve ngay → query `event_step_time`\n"
       "2. U2 request cancel (lúc vừa bấm) → query\n"
       "3. Admin approve request cancel trên APP → query\n4. Trên WEB → query\n"
       "5. Admin deny request cancel → query\n6. Admin cancel trên WEB và trên APP → query",
       "6 nhánh",
       "- Nhánh 1, 3, 4, 6: XÓA remind đã add trước đó\n- Nhánh 2, 5: KHÔNG xóa remind",
       note="Nguồn: Setting calendar r1041-r1047."),

    tc("リマインド — job gửi & recover", "DATA-MIG-001", "Normal",
       "Support #33648: command recover:remindLesson — nhánh step gửi TRƯỚC không đổi",
       CAL + "\n- Có booking cũ với `event_step_time` của step gửi TRƯỚC (`is_after_day` = 0), "
             "`sent_date_time` đang tính theo start time",
       "1. Ghi lại `sent_date_time` hiện tại của các bản ghi step TRƯỚC (cả đã gửi và chưa gửi, "
       "cả kiểu ngày day=0/day>0 và kiểu duration)\n"
       "2. Chạy command `recover:remindLesson`\n3. Query lại `event_step_time`",
       "Step gửi TRƯỚC, 5 tổ hợp",
       "- TOÀN BỘ bản ghi step gửi TRƯỚC: KHÔNG bị recover, `sent_date_time` giữ nguyên",
       note="Nguồn: Setting calendar r1070-r1075 (Support #33648, 01/2026)."),

    tc("リマインド — job gửi & recover", "DATA-MIG-001", "Normal",
       "Support #33648: recover step gửi SAU của booking CŨ (trước khi release #32367)",
       CAL + "\n- Booking cũ có `event_step_time` của step SAU, `sent_date_time` đang tính theo "
             "START time",
       "Với từng tổ hợp, chạy `recover:remindLesson` rồi query `event_step_time`:\n"
       "1. Step đã gửi (status ≠ 0)\n"
       "2. Chưa gửi, kiểu ngày day = 0, send time < start time booking (ban đầu KHÔNG được add)\n"
       "3. Chưa gửi, kiểu ngày day = 0, send time > start time (ban đầu CÓ add)\n"
       "4. Chưa gửi, kiểu ngày day > 0 (ban đầu CÓ add)\n5. Chưa gửi, kiểu duration",
       "5 tổ hợp booking cũ",
       "- Tổ hợp 1: KHÔNG recover, `sent_date_time` giữ nguyên\n"
       "- Tổ hợp 2: tính lại theo end time vẫn < end time ⇒ KHÔNG recover, KHÔNG bị add thêm\n"
       "- Tổ hợp 3: tính lại theo end time — nếu send time > end time thì GIỮ NGUYÊN; "
       "nếu send time < end time thì XÓA bản ghi remind\n"
       "- Tổ hợp 4, 5: recover — `sent_date_time` được tính lại theo giờ KẾT THÚC của booking",
       note="Nguồn: Setting calendar r1076-r1081."),

    tc("リマインド — job gửi & recover", "DATA-MIG-001", "Normal",
       "Support #33648: booking MỚI (sau #32367) → command recover KHÔNG đụng tới",
       CAL + "\n- Booking mới có `event_step_time` step SAU đã tính theo END time",
       "1. Ghi lại `sent_date_time` của 4 tổ hợp (đã gửi · chưa gửi day=0 send<end · "
       "chưa gửi day=0 send>end · chưa gửi day>0)\n2. Chạy `recover:remindLesson`\n3. Query lại",
       "4 tổ hợp booking mới",
       "- Cả 4 tổ hợp: KHÔNG recover, `sent_date_time` KHÔNG đổi, KHÔNG tạo thêm bản ghi",
       note="Nguồn: Setting calendar r1082-r1085."),

    tc("リマインド — job gửi & recover", "DATA-MIG-001", "Normal",
       "Support #33648: recover theo trạng thái booking (6 nhánh)",
       CAL + "\n- Chuẩn bị booking cũ ở 6 trạng thái: approve (1,2) · chờ approve (0) · deny (6) · "
             "đợi nhận thông báo (3) · request cancel (5) · đã cancel (4,7)",
       "1. Chạy `recover:remindLesson`\n2. Query `event_step_time` từng nhóm",
       "6 trạng thái",
       "- Status 1, 2 và 5: CÓ recover (cập nhật `sent_date_time`)\n"
       "- Status 0, 3, 4, 6, 7: user chưa từng được add remind ⇒ KHÔNG recover và KHÔNG bị add mới",
       note="Nguồn: Setting calendar r1088-r1093."),

    # ══════════════════ 空き枠通知受け取り設定 ══════════════════
    tc("空き枠通知受け取り設定", "UI-001", "Normal",
       "Bật/tắt setting danh sách chờ → banner trạng thái và auto-save",
       CAL,
       "1. Vào menu「空き枠通知受け取り設定」→ quan sát trạng thái mặc định\n"
       "2. Quan sát phần nội dung setting phía dưới\n3. Chuyển sang ON → quan sát",
       "—",
       "- Mặc định OFF: banner「現在、空き枠通知受け取り設定は 停止中 です」, "
       "phần nội dung setting phía dưới bị ẨN\n"
       "- Chuyển ON: banner đổi thành「現在、空き枠通知受け取り設定は 受付中 です」, "
       "tự động lưu và hiện toast ở góc phải dưới màn hình",
       note="Nguồn: Setting calendar r1151-r1153."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "Tab 通知受け取り申請時: gửi khi user đăng ký chờ hủy",
       CAL + "\n- Đã bật ON 空き枠通知受け取り設定, đã setting msg text + 1 action ở tab 通知受け取り申請時\n"
             "- Slot S1 đã full",
       "1. LINE user U1 mở trang booking, chọn slot S1 → đăng ký nhận thông báo\n"
       "2. Kiểm tin LINE của U1",
       "1 slot full",
       "- U1 nhận msg text đã setting + action đã setting\n"
       "- Message pattern mặc định đã được tạo sẵn từ đầu (áp dụng cho cả 2 tab)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1154-r1155."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "Tab 通知受け取り申請時: chọn 利用しない → không gửi msg nhưng vẫn gửi action",
       CAL + "\n- Đã setting msg text + 1 action ở tab 通知受け取り申請時",
       "1. Tích「利用しない」→ Lưu → query `calendar_management.use_message_notify_full_slot`\n"
       "2. U1 đăng ký chờ hủy → kiểm tin LINE\n"
       "3. Bỏ tích → Lưu → query lại → U2 đăng ký chờ hủy → kiểm",
       "2 trạng thái cờ",
       "- Tích 利用しない: `use_message_notify_full_slot` = 1 ⇒ KHÔNG gửi msg, VẪN gửi action\n"
       "- Bỏ tích: `use_message_notify_full_slot` = 0 ⇒ CÓ gửi msg",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1162. ⚠️ Cờ mang nghĩa ĐẢO (0 = gửi) — khớp spec BR-47."),

    tc("空き枠通知受け取り設定", "MSG-002", "Abnormal",
       "Tab 通知受け取り申請時: không setting cả msg và action → user không nhận gì",
       CAL + "\n- Tab 通知受け取り申請時 chưa setting msg text và không có action nào",
       "1. U1 đăng ký chờ hủy ở slot full\n2. Kiểm tin LINE U1\n"
       "3. Query `calendar_course_bookings` của U1",
       "Không setting gì",
       "- U1 KHÔNG nhận tin nhắn hay action nào\n"
       "- Nhưng bản ghi booking status = 3 VẪN được tạo",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1166, r1172."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "Modal action của tab 通知受け取り申請時: xóa và edit action lưu ngay vào DB",
       CAL,
       "1. Bấm「アクション登録・編集」→ add 1 action → Save modal → query `calendar_management`\n"
       "2. Edit action đó sang loại khác → Save modal → query lại\n"
       "3. Xóa action → Save modal → query lại\n"
       "4. Có action → xóa → thêm action mới → Save → so sánh id action",
       "1 action",
       "- Bước 1-2: lưu luôn vào DB không cần bấm Save của màn setting\n"
       "- Bước 3: action bị xóa khỏi DB\n"
       "- Bước 4: id action MỚI khác id action cũ",
       note="Nguồn: Setting calendar r1169-r1171."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "Tab 受付再開時: gửi cho TẤT CẢ user đang chờ khi có chỗ trống",
       CAL + "\n- Slot S1 定員 3, đã full\n- 3 LINE user U1, U2, U3 đang đăng ký chờ hủy ở S1\n"
             "- Tab 受付再開時 đã setting msg text + 1 action",
       "1. Cho 1 booking ở S1 cancel (được approve ngay)\n2. Kiểm LINE app của U1, U2, U3\n"
       "3. Query `calendar_course_bookings` của 3 user\n4. U2 vào booking lại slot S1",
       "3 user chờ, 1 chỗ trống",
       "- CẢ 3 user U1, U2, U3 đều nhận msg + action báo có chỗ trống (gửi đồng loạt, "
       "KHÔNG xếp thứ tự ưu tiên)\n"
       "- Bản ghi status = 3 của cả 3 user GIỮ NGUYÊN sau khi gửi\n"
       "- Bước 4: U2 booking được (ai nhanh hơn thì được, kể cả user mới không nằm trong danh sách chờ)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1173-r1174 + spec BR-33. ⚠️ Không giới hạn số lượng và "
            "không có thứ tự ưu tiên ⇒ khách hàng có thể phàn nàn. Xem MT-36."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "空き枠通知: 4 nguồn phát sinh chỗ trống × 2 lối thao tác (web / app / CSV)",
       CAL + "\n- Slot S1 (TƯƠNG LAI) đã full, có 2 user đang chờ\n- Đã bật 空き枠通知受け取り設定",
       "Với từng nguồn, thực hiện rồi kiểm LINE của 2 user đang chờ:\n"
       "1. 1 user của S1 cancel và được approve ngay\n"
       "2. Admin tăng 定員 (hoặc đổi sang không giới hạn) ở WEB · ở APP · bằng import CSV\n"
       "3. Admin cancel 1 booking của S1 ở WEB · ở APP\n"
       "4. Admin approve request cancel của S1 ở WEB · ở APP",
       "4 nguồn × các lối thao tác",
       "- TẤT CẢ trường hợp: 2 user đang chờ đều nhận msg text + action báo có chỗ trống\n"
       "- Kiểm cả với account STAFF thực hiện thao tác — kết quả phải giống admin chính",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1174-r1181 (slot ngày TƯƠNG LAI) + spec BR-19, BR-32."),

    tc("空き枠通知受け取り設定", "FUNC-004", "Boundary",
       "空き枠通知: biên thời gian — slot hôm nay chưa/đã qua giờ start",
       CAL + "\n- Slot S2 vào NGÀY HÔM NAY, đã full, có 2 user đang chờ",
       "1. Khi giờ hiện tại < start time của S2: cho 1 booking cancel → kiểm LINE 2 user\n"
       "2. Khi giờ hiện tại > start time của S2: lặp lại (dùng slot khác cùng điều kiện)\n"
       "3. Với slot ở ngày QUÁ KHỨ: lặp lại",
       "3 mốc thời gian",
       "- Bước 1: 2 user NHẬN được thông báo có chỗ trống\n"
       "- Bước 2, 3: KHÔNG gửi msg, KHÔNG gửi action",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1182-r1205 (ma trận đầy đủ 4 nguồn × 4 mốc thời gian; "
            "gộp theo 2 nhóm kết quả). Khớp spec BR-32."),

    tc("空き枠通知受け取り設定", "MSG-002", "Abnormal",
       "空き枠通知 chỉ gửi cho user đang CHỜ, không gửi cho user đã có booking",
       CAL + "\n- Slot S1 có: U1 đã approve, U2 đang chờ approve, U3 đang chờ nhận thông báo",
       "1. Cho 1 booking khác của S1 cancel để phát sinh chỗ trống\n"
       "2. Kiểm LINE của U1, U2, U3",
       "3 user 3 trạng thái",
       "- CHỈ U3 (đang chờ nhận thông báo) nhận được action báo chỗ trống\n"
       "- U1 và U2 KHÔNG nhận gì",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1206."),

    tc("空き枠通知受け取り設定", "STATE-001", "Abnormal",
       "Tắt setting 空き枠通知 khi đang có user chờ → user không nhận thông báo nữa",
       CAL + "\n- Đã bật ON, U1 đang đăng ký chờ hủy ở slot S1",
       "1. Admin tắt setting về OFF\n2. Cho 1 booking của S1 cancel\n"
       "3. Kiểm LINE U1\n4. Query `calendar_course_bookings` của U1",
       "1 user đang chờ",
       "- U1 KHÔNG nhận thông báo chỗ trống nữa\n"
       "- Booking status = 3 của U1 VẪN giữ nguyên trong DB",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1207."),

    tc("空き枠通知受け取り設定", "FUNC-002", "Abnormal",
       "Tab 受付再開時: KHÔNG có option 利用しない, bắt buộc nhập nội dung",
       CAL,
       "1. Vào tab 受付再開時 → tìm option「利用しない」\n"
       "2. Xóa trống ô nội dung → Lưu\n3. Nhập 5001 ký tự → Lưu\n4. Nhập 5000 ký tự → Lưu",
       "rỗng · 5001 · 5000 ký tự",
       "- KHÔNG có option「利用しない」ở tab này (để đảm bảo user luôn nhận được tin khi có chỗ trống)\n"
       "- Bỏ trống: validate báo lỗi\n- 5001 ký tự: Invalid\n- 5000 ký tự: Save success",
       note="Nguồn: Setting calendar r1173, r1215-r1217."),

    tc("空き枠通知受け取り設定", "DATA-AUDIT-001", "Normal",
       "Màn lịch sử 変更履歴 của setting 空き枠通知",
       CAL + "\n- Đã bật/tắt setting nhiều lần bởi admin chính và staff A",
       "1. Mở 変更履歴 → quan sát các cột\n2. Kiểm sort\n3. Bấm nút X",
       "Nhiều lần bật/tắt",
       "- Cột 日時 format「2024.09.25 (金) 10:31」\n"
       "- Cột 操作した人: hiện「スタッフA」khi staff thao tác, tên admin khi admin chính thao tác\n"
       "- Cột 内容: OFF→ON hiện「停止中→受付中 に変更」; ON→OFF hiện「受付中→停止中 に変更」\n"
       "- Sort: thời gian mới nhất lên đầu\n- Nút X: đóng popup, về màn setting notify",
       note="Nguồn: Setting calendar r1256-r1262. ⚠️ Spec BR-36: CHỈ ghi lịch sử khi `is_notify_full_slot` "
            "ĐỔI giá trị — thay đổi NỘI DUNG msg/action KHÔNG để lại dấu vết. Xem MT-37."),

    # ══════════════════ Bug KH #36729 — キャンセル用URL ══════════════════
    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729 — tái hiện: đăng ký chờ hủy 2 lần cùng slot",
       CAL + "\n- Đã bật 空き枠通知受け取り設定\n- Slot A đã full",
       "1. LINE user U1 mở màn booking, chọn slot A → đăng ký nhận thông báo (lần 1)\n"
       "2. U1 quay lại màn booking, chọn slot A → đăng ký nhận thông báo (lần 2)\n"
       "3. Kiểm tin LINE U1 nhận sau lần 2\n"
       "4. Nếu có URL キャンセル用URL mới, bấm vào và quan sát",
       "1 slot full, đăng ký 2 lần",
       "- Lần 2 phải hiện message lỗi「キャンセル待ち通知受け取りがすでに登録されています」\n"
       "- KHÔNG gửi message mới, KHÔNG gửi キャンセル用URL mới\n"
       "- ⚠️ Nếu tái hiện được bug: URL gửi lần 2 có dạng "
       "https://liff.line.me/…?calendar_id=xxx&tab=detail&booking_id= (booking_id RỖNG), "
       "bấm vào hiện「予約が解除されました」nhưng đăng ký thật KHÔNG bị hủy ⇒ raise bug",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1222-r1223, r1225-r1226 (Bug KH #36729, 05/2026 — "
            "KHỐI MỚI NHẤT của tab Setting calendar)."),

    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729: đăng ký chờ hủy lần đầu thành công",
       CAL + "\n- U1 CHƯA có đăng ký chờ hủy nào cho slot A (slot A đã full)",
       "1. U1 mở màn Lesson Booking → chọn slot A → đăng ký nhận thông báo\n"
       "2. Query `calendar_course_bookings` của U1\n3. Kiểm tin LINE U1\n"
       "4. Cho slot A có chỗ trống → kiểm U1 có nhận thông báo không",
       "1 slot full",
       "- Tạo bản ghi booking status = 3 (WAIT_CANCEL)\n"
       "- U1 nhận message có chứa キャンセル用URL hợp lệ\n"
       "- Khi có chỗ trống: U1 nhận được thông báo",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1224."),

    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729: đăng ký trùng KHÔNG update bản ghi cũ, URL cũ vẫn hủy được",
       CAL + "\n- U1 đã có đăng ký WAIT_CANCEL cho slot A",
       "1. Ghi lại `booking_id` và `status` hiện tại của U1\n"
       "2. U1 đăng ký lại slot A (bị chặn)\n3. Query lại bản ghi\n"
       "4. U1 mở キャンセル用URL nhận được từ lần đăng ký ĐẦU TIÊN → thực hiện hủy\n"
       "5. Query lại và kiểm U1 có còn nhận thông báo không",
       "1 đăng ký, 1 lần chặn",
       "- Bước 3: `booking_id` GIỮ NGUYÊN, `status` vẫn = 3, KHÔNG phát sinh update\n"
       "- Bước 4: URL CŨ vẫn hoạt động, hủy đăng ký thành công\n"
       "- Bước 5: bản ghi được cancel, U1 KHÔNG còn nhận thông báo",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1227-r1229."),

    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729: đăng ký slot KHÁC / user KHÁC cùng slot vẫn thành công",
       CAL + "\n- U1 đã có WAIT_CANCEL cho slot A (đã full); slot B cũng đã full",
       "1. U1 chọn slot B → đăng ký nhận thông báo\n2. Query `calendar_course_bookings` của U1\n"
       "3. U2 (chưa đăng ký gì) chọn slot A → đăng ký\n4. Query của U2",
       "2 slot, 2 user",
       "- Bước 1-2: U1 đăng ký thành công, tạo bản ghi WAIT_CANCEL MỚI cho slot B, "
       "nhận được URL tương ứng\n"
       "- Bước 3-4: U2 đăng ký thành công, sinh booking riêng (không ảnh hưởng U1)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1230-r1231."),

    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729: nhánh bookingType='notify' — book thật thì UPDATE bản ghi status=3",
       CAL + "\n- U1 có WAIT_CANCEL cho slot A với `booking_id` hợp lệ\n- Slot A vừa có chỗ trống",
       "1. U1 bấm link booking từ thông báo → book slot A → query DB\n"
       "2. Với U2 (cũng có WAIT_CANCEL slot A): mở キャンセル用URL → bấm nút sang màn booking mới → "
       "book slot A → query DB\n3. Kiểm tin LINE của U1 và U2",
       "2 lối vào đặt lại",
       "- Cả 2 lối: book thành công\n"
       "- DB: KHÔNG tạo booking mới, mà UPDATE bản ghi có status = 3 ban đầu thành booking thật\n"
       "- U1 và U2 đều nhận được action booking mới",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1232-r1233. Khớp spec T-05 / T-06."),

    tc("空き枠通知受け取り設定", "DATA-REF-001", "Normal",
       "Bug KH #36729: đăng ký lại SAU KHI đã hủy → tạo booking mới",
       CAL + "\n- U1 đã hủy WAIT_CANCEL cho slot A bằng キャンセル用URL",
       "1. U1 chọn lại slot A → đăng ký nhận thông báo\n2. Query DB và kiểm tin LINE",
       "Đã hủy rồi đăng ký lại",
       "- Đăng ký thành công, tạo booking MỚI (booking_id khác cũ)\n- Gửi URL mới hợp lệ",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1234."),

    tc("空き枠通知受け取り設定", "SEC-001", "Abnormal",
       "Bug KH #36729: truy cập キャンセル用URL bị sửa booking_id hoặc token",
       CAL + "\n- U1 có URL hủy hợp lệ",
       "1. Sửa `booking_id` trên URL thành id của booking user khác → truy cập\n"
       "2. Sửa thành id không tồn tại → truy cập\n3. Bỏ trống `booking_id` → truy cập\n"
       "4. Query DB sau mỗi lần",
       "3 kiểu URL invalid",
       "- Cả 3 trường hợp: hiển thị lỗi phù hợp, KHÔNG hủy nhầm booking của người khác\n"
       "- DB KHÔNG bị thay đổi ở mọi trường hợp",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1235. ⚠️ Spec S-01/S-02: LIFF KHÔNG xác thực, `booking_id` là "
            "số nguyên tự tăng ⇒ TC này DỰ KIẾN FAIL ở bước 1. Xem MT-38."),

    tc("空き枠通知受け取り設定", "CONC-001", "Abnormal",
       "Bug KH #36729: spam nhiều request đăng ký cùng slot đồng thời",
       CAL + "\n- U1 chưa có WAIT_CANCEL cho slot A (đã full)",
       "1. Gửi 5 request đăng ký nhận thông báo cùng slot A gần như đồng thời (< 1 giây)\n"
       "2. Query `SELECT COUNT(*) FROM calendar_course_bookings WHERE reception_id = {A} "
       "AND line_user_id = {U1} AND status = 3 AND deleted_at IS NULL`\n"
       "3. Kiểm số message U1 nhận",
       "5 request đồng thời",
       "- Chỉ tạo ĐÚNG 1 bản ghi WAIT_CANCEL\n- 4 request còn lại bị reject\n"
       "- U1 chỉ nhận ĐÚNG 1 message và 1 キャンセル用URL",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1236. ⚠️ Spec RA-01: KHÔNG có DB transaction ở bất kỳ luồng "
            "ghi nào ⇒ TC này có rủi ro FAIL cao. RULE-08: race condition test PRODUCTION."),

    # ══════════════════ 予約ページの表示設定 ══════════════════
    tc("予約ページの表示設定", "FUNC-001", "Normal",
       "Setting hiển thị giá course — 2 option + nhánh enable bill tiền đè setting",
       CAL + "\n- Course C1 giá 5.000 yên",
       "1. Chọn「表示する」→ Lưu → LINE user mở trang booking\n"
       "2. Chọn「表示しない」→ Lưu → LINE user mở lại\n"
       "3. Bật enable bill tiền (vẫn giữ 表示しない) → LINE user mở lại",
       "2 option × enable bill",
       "- Bước 1: LINE user THẤY giá course\n- Bước 2: LINE user KHÔNG thấy giá\n"
       "- Bước 3: LINE user VẪN THẤY giá (enable bill tiền ĐÈ setting này)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1135-r1137."),

    tc("予約ページの表示設定", "FUNC-001", "Normal",
       "Setting hiển thị số chỗ còn lại 残りの定員数 — 2 option",
       CAL + "\n- Slot S1 定員 5, đã có 2 booking approve",
       "1. Chọn「表示する」→ Lưu → LINE user mở trang chọn slot\n"
       "2. Chọn「表示しない」→ Lưu → LINE user mở lại",
       "Slot còn 3 chỗ",
       "- Bước 1: LINE user thấy「残り 3」\n- Bước 2: LINE user KHÔNG thấy số chỗ còn lại",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1138-r1139."),

    tc("予約ページの表示設定", "FUNC-001", "Normal",
       "Setting slot đã hết chỗ 満席のコース — 2 option + nhánh bật danh sách chờ",
       CAL + "\n- Slot S1 đã full (定員 = số approve)",
       "1. Chọn「表示する」+ TẮT danh sách chờ → LINE user mở trang chọn slot\n"
       "2. Chọn「表示しない」+ TẮT danh sách chờ → mở lại\n"
       "3. Chọn「表示しない」+ BẬT danh sách chờ → mở lại",
       "Slot full",
       "- Bước 1: LINE user THẤY slot, hiển thị「残り 0」và slot bị DISABLE\n"
       "- Bước 2: LINE user KHÔNG thấy slot (bị ẩn)\n"
       "- Bước 3: LINE user THẤY slot và ENABLE để đăng ký nhận thông báo "
       "(bật danh sách chờ ĐÈ setting này)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1140-r1142 + spec BR-P04."),

    tc("予約ページの表示設定", "FUNC-004", "Boundary",
       "Setting đổi text thay cho nhãn コース — validate 10 ký tự",
       CAL,
       "1. Quan sát ô textbox text hiện tại「コース」\n"
       "2. Nhập text thay thế 10 ký tự → Lưu → LINE user mở trang booking\n"
       "3. Nhập 11 ký tự → Lưu\n4. Xóa trống → Lưu",
       "10 / 11 / rỗng",
       "- Ô text hiện tại「コース」bị DISABLE (không sửa được)\n"
       "- 10 ký tự: Save success; LINE user thấy nhãn mới thay cho「コース」ở màn chọn course, "
       "màn lịch sử, màn detail booking\n"
       "- 11 ký tự: báo lỗi hoặc chặn gõ ký tự thứ 11\n"
       "- Rỗng: KHÔNG required (được phép để trống)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1143-r1147 + Booking phía line user r69, r143."),

    tc("予約ページの表示設定", "FUNC-DRAFT-001", "Abnormal",
       "Nút Lưu màn 表示設定: không bấm mà sang tab khác → mất thay đổi; double click → 1 lần",
       CAL,
       "1. Đổi setting hiển thị giá → KHÔNG bấm Lưu → sang tab khác rồi quay lại\n"
       "2. Đổi setting lại → double click nút Lưu\n3. Reload màn hình",
       "—",
       "- Bước 1: các thay đổi KHÔNG được lưu (hiển thị lại giá trị cũ)\n"
       "- Bước 2-3: chỉ lưu 1 lần, giá trị mới được ghi nhận",
       note="Nguồn: Setting calendar r1148-r1149."),

    # ══════════════════ 予約ページの非表示 (filter) ══════════════════
    tc("予約ページの非表示 (filter)", "FUNC-002", "Normal",
       "CRUD filter 予約ページの非表示 — admin chính và staff đều thao tác được",
       CAL,
       "Với CẢ admin chính VÀ account staff S1, làm lần lượt:\n"
       "1. Chưa set filter → quan sát preview\n2. Add filter mới (theo tag T1) → quan sát\n"
       "3. Edit filter → mở modal, sửa, lưu\n4. Xóa filter → quan sát",
       "2 loại account",
       "- Chưa set: hiện text「絞り込み条件が登録されていません」\n"
       "- Add: hiện preview filter + số friend thỏa mãn\n"
       "- Edit: modal hiện đúng filter cũ, sửa và lưu được giá trị mới nhất\n"
       "- Xóa: quay về text「絞り込み条件が登録されていません」\n"
       "- Kết quả GIỐNG NHAU cho cả admin chính và staff",
       note="Nguồn: Setting calendar r155-r162."),

    tc("予約ページの非表示 (filter)", "FUNC-002", "Normal",
       "Không set filter → LINE user vào được trang booking (2 nhánh top page)",
       CAL,
       "1. Không set filter + BẬT hiển thị trang top → LINE user mở URL booking\n"
       "2. Không set filter + TẮT trang top → LINE user mở URL booking",
       "2 nhánh top page",
       "- Bước 1: hiện trang TOP; bấm nút booking thì sang màn chọn course\n"
       "- Bước 2: vào thẳng màn chọn course",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r163-r164."),

    tc("予約ページの非表示 (filter)", "FUNC-002", "Abnormal",
       "Có filter: user THỎA điều kiện → chặn cả URL booking và URL lịch sử",
       CAL + "\n- Filter: friend có tag T1\n- U1 CÓ tag T1",
       "1. Bật trang top → U1 mở URL booking\n2. Tắt trang top → U1 mở URL booking\n"
       "3. Bật trang top → U1 mở URL lịch sử\n4. Tắt trang top → U1 mở URL lịch sử",
       "User thỏa filter",
       "- Cả 4 trường hợp: hiện trang báo lỗi kèm message đã setting ở mục "
       "「予約ページの案内テキスト」\n- KHÔNG vào được trang booking hay lịch sử",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r165-r166, r169-r170."),

    tc("予約ページの非表示 (filter)", "FUNC-002", "Normal",
       "Có filter: user KHÔNG thỏa điều kiện → vào bình thường",
       CAL + "\n- Filter: friend có tag T1\n- U2 KHÔNG có tag T1",
       "1. Bật/tắt trang top × mở URL booking và URL lịch sử (4 tổ hợp) với U2",
       "User không thỏa filter",
       "- Cả 4 tổ hợp: U2 vào được trang booking / trang lịch sử bình thường",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r167-r168, r171-r172."),

    tc("予約ページの非表示 (filter)", "DATA-REF-001", "Abnormal",
       "Filter bị xóa — 2 kịch bản dữ liệu (normal và abnormal)",
       CAL + "\n- Calendar đã set filter, sau đó filter bị xóa",
       "Kịch bản NORMAL: `filter_calendar_salon_ids` bị clear khỏi `calendar_salon` "
       "(WEB hiện đang set thành chuỗi rỗng)\n"
       "1. U1 mở URL booking → quan sát\n2. U1 mở URL lịch sử → quan sát\n"
       "Kịch bản ABNORMAL: `filter_calendar_salon_ids` KHÔNG bị clear nhưng bảng `filters_v2` "
       "KHÔNG còn bản ghi của filter_id đó\n3. Lặp bước 1-2",
       "2 kịch bản dữ liệu mồ côi",
       "- Cả 2 kịch bản: U1 vào được trang booking và trang lịch sử BÌNH THƯỜNG "
       "(không bị chặn oan, không lỗi 500)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r173-r176."),

    tc("予約ページの非表示 (filter)", "MSG-002", "Normal",
       "Nội dung 予約ページの案内テキスト — không nhập / có nhập",
       CAL + "\n- Filter đang chặn U1",
       "1. Để trống ô text → Lưu → U1 mở URL booking\n"
       "2. Nhập text có xuống dòng → Lưu → U1 mở lại",
       "rỗng / text có enter",
       "- Bước 1: hiện text mặc định「詳細は運営元までお問い合わせください」\n"
       "- Bước 2: hiện đúng text đã nhập, giữ nguyên xuống dòng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r177-r178."),

    # ══════════════════ トップ・店舗情報・利用規約 ══════════════════
    tc("トップ・店舗情報・利用規約", "MEDIA-IMG-001", "Normal",
       "Màn トップ設定 và ビジネス情報: upload ảnh — 6 nhánh giống nhau",
       CAL,
       "Làm ở CẢ 2 màn (トップ設定 và ビジネス情報):\n"
       "1. Chưa upload → quan sát\n2. Upload ảnh 800x600 (không đúng 1000x700) → Lưu\n"
       "3. Upload ảnh đúng 1000x700 → Lưu\n4. Upload ảnh 11MB → Lưu\n"
       "5. Upload file .txt và ảnh .avif → Lưu\n6. Upload jpg/png/gif/jpeg → Lưu\n"
       "7. Upload tên file chứa tiếng Nhật + space → Lưu\n8. Upload 1 ảnh rồi thay bằng ảnh khác",
       "8 tình huống × 2 màn",
       "- Bước 1: hiện msg「設定されていません」\n"
       "- Bước 2, 3, 6, 7, 8: upload success\n"
       "- Bước 4: báo lỗi「10MB以下のをアップしてください。」\n"
       "- Bước 5: báo lỗi「ファイルの形式が正しくありません。」",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1273-r1280 (トップ設定) và r1306-r1313 (ビジネス情報) — "
            "2 khối HOÀN TOÀN GIỐNG NHAU nên gộp 1 TC, liệt kê đủ 2 màn ở cột Các bước."),

    tc("トップ・店舗情報・利用規約", "FUNC-004", "Boundary",
       "店舗名 ở màn トップ設定 — default, validate 30/31 và required",
       CAL + "\n- Calendar tạo mới với `calendar_name` =「レA」",
       "1. Vào màn トップ設定 lần đầu → quan sát ô 店舗名\n"
       "2. Nhập 30 ký tự → Lưu → query `calendar_management`\n"
       "3. Nhập 31 ký tự → Lưu\n4. Xóa trống → Lưu",
       "default / 30 / 31 / rỗng",
       "- Bước 1: hiển thị mặc định là `calendar_name` đã tạo ở màn tạo calendar\n"
       "- Bước 2: Update success, ghi vào CẢ `calendar_name` VÀ `store_name`\n"
       "- Bước 3: báo lỗi「店舗名は30文字以内で入力してください。」\n"
       "- Bước 4: báo lỗi「店舗名を入力してください。」",
       note="Nguồn: Setting calendar r1281, r1284-r1288. ⚠️ TC gốc r1281 ghi「Change spec → 100 ký tự」"
            "nhưng r1288 lại nói giới hạn 30 — MÂU THUẪN. Xem MT-39."),

    tc("トップ・店舗情報・利用規約", "DATA-MIG-001", "Normal",
       "Recover data 店舗名 cho calendar cũ",
       CAL + "\n- Có calendar cũ với `store_name` = NULL và calendar có `store_name` khác NULL",
       "1. Chạy recover:\n"
       "`UPDATE calendar_management SET line_name = store_name WHERE store_name IS NOT NULL;`\n"
       "`UPDATE calendar_management SET store_name = line_name WHERE store_name IS NULL;`\n"
       "2. Query lại 2 nhóm calendar\n3. Mở màn top page phía LINE user",
       "2 nhóm calendar",
       "- Sau recover: mọi calendar đều có `store_name` và `line_name` khác NULL\n"
       "- Màn top page phía LINE user hiển thị đúng tên cửa hàng, không rỗng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1289. ⚠️ Spec Gap G-10: dump 0/174 bản ghi có `store_name` "
            "⇒ nếu chưa chạy recover thì màn top page LUÔN hiển thị rỗng. Xem MT-40."),

    tc("トップ・店舗情報・利用規約", "FUNC-002", "Abnormal",
       "Ô description ở màn トップ設定 và ビジネス情報: nhập HTML bị clear",
       CAL,
       "1. Ở màn トップ設定, nhập text thường có xuống dòng, ký tự Nhật, icon → Lưu → "
       "kiểm phía LINE user\n"
       "2. Nhập chuỗi có thẻ HTML (ví dụ `<script>alert(1)</script>` hoặc `<b>đậm</b>`) → Lưu\n"
       "3. Lặp ở màn ビジネス情報",
       "text thường + HTML",
       "- Text thường, xuống dòng, ký tự Nhật, icon: lưu và hiển thị đúng phía LINE user\n"
       "- Chuỗi HTML: phần HTML BỊ CLEAR (không lưu, không render, không thực thi script)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1290-r1294, r1314-r1318."),

    tc("トップ・店舗情報・利用規約", "OUT-PREVIEW-001", "Normal",
       "Nút preview ở màn トップ設定 và ビジネス情報 — lưu rồi mở tab mới",
       CAL,
       "1. Sửa ảnh + 店舗名 + description ở màn トップ設定 → bấm nút preview\n"
       "2. Quan sát tab mới\n3. Bấm nút「予約にすすむ」\n"
       "4. Lặp ở màn ビジネス情報\n5. Sửa tiếp rồi bấm preview lần nữa",
       "—",
       "- Bấm preview: LƯU thông tin vừa nhập rồi mở tab mới\n"
       "- Tab mới hiển thị đúng data vừa nhập (giống màn LINE user thật)\n"
       "- Bấm 予約にすすむ: sang màn chọn course\n"
       "- Bước 5: preview hiển thị data MỚI nhất",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1295-r1302, r1319-r1324."),

    tc("トップ・店舗情報・利用規約", "FUNC-004", "Boundary",
       "利用規約: OFF/ON và validate nội dung 10.000 ký tự (text thường và HTML)",
       CAL,
       "1. Quan sát option mặc định\n2. Setting OFF → LINE user mở trang booking\n"
       "3. Setting ON nhưng để trống nội dung → Lưu\n"
       "4. ON + nhập 10.000 ký tự text thường → Lưu → kiểm LINE user\n"
       "5. ON + nhập 10.001 ký tự → Lưu\n"
       "6. ON + nhập nội dung format HTML 10.000 ký tự → Lưu → kiểm LINE user\n"
       "7. Chuyển đổi qua lại ON ⇄ OFF nhiều lần",
       "OFF/ON × 10000/10001 ký tự × text/HTML",
       "- Mặc định: OFF (表示しない)\n- OFF: LINE user KHÔNG thấy màn quy chế\n"
       "- Bước 3: báo lỗi (bắt buộc nhập nội dung khi ON)\n"
       "- 10.000 ký tự: Save success, LINE user thấy đúng nội dung\n"
       "- 10.001 ký tự: Invalid\n"
       "- HTML: LINE user thấy nội dung ĐÃ RENDER HTML (khác màn description ở trên)\n"
       "- Bước 7: lưu theo lần thao tác cuối",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1264-r1271."),

    # ══════════════════ 予約システムの削除 ══════════════════
    tc("予約システムの削除", "NOTI-MAIL-001", "Normal",
       "Bước 1: gửi mã xác thực qua email",
       CAL,
       "1. Vào menu「予約システムの削除」→ quan sát tên calendar hiển thị\n"
       "2. Bấm「削除用認証コードをメールで受け取る」\n3. Kiểm hộp thư của admin\n"
       "4. Ở màn tiếp theo, bấm「メールを再送する」→ kiểm hộp thư",
       "1 calendar",
       "- Hiển thị đúng tên calendar đang thao tác\n"
       "- Nhận được email chứa mã xác thực 10 ký tự, format email đúng mẫu\n"
       "- Bấm gửi lại: hiện toast đã gửi lại + nhận được EMAIL MỚI với mã MỚI",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1544-r1548. RULE-06: verify tới output cuối là email nhận được."),

    tc("予約システムの削除", "NOTI-MAIL-001", "Abnormal",
       "Bước 2: validate mã xác thực — 5 tình huống",
       CAL + "\n- Đã nhận 2 email: mã cũ M1 (từ lần gửi đầu) và mã mới M2 (sau khi bấm gửi lại)",
       "1. Để trống ô mã → bấm「削除の最終確認にすすむ」\n2. Nhập mã sai「XXXXXXXXXX」\n"
       "3. Nhập mã CŨ M1\n4. Nhập mã M2 kèm khoảng trắng đầu/cuối「 M2 」\n5. Nhập đúng M2",
       "5 giá trị mã",
       "- Bước 1, 2, 3: báo lỗi, KHÔNG sang bước tiếp\n"
       "- Bước 4: tự động trim khoảng trắng, sang popup confirm cuối cùng\n"
       "- Bước 5: sang popup confirm cuối cùng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1549-r1554. ⚠️ Spec BR-53 / A-05: mã lưu PLAINTEXT ở "
            "`calendar_management.code_delete`, KHÔNG hết hạn và KHÔNG xóa sau khi dùng, còn bị "
            "trả thẳng trong response JSON. Xem MT-41."),

    tc("予約システムの削除", "PERM-002", "Abnormal",
       "Mã xác thực xóa quá 24h → cần chốt còn dùng được không",
       CAL + "\n- Đã nhận mã M1 từ hơn 24 giờ trước, chưa dùng",
       "1. Vào màn nhập mã, nhập M1\n2. Quan sát kết quả",
       "Mã 24h+ tuổi",
       "- Cần chốt hành vi: mã có hết hạn hay không\n"
       "- Nếu mã VẪN dùng được ⇒ rủi ro bảo mật (xóa cả hệ thống đặt lịch)",
       spec="Đã hỏi leader",
       note="Nguồn: Setting calendar r1552 — TC gốc CHỈ CÓ TIÊU ĐỀ「nhập mã code đã quá 24h」, "
            "KHÔNG có kết quả mong đợi. Spec BR-53 khẳng định mã KHÔNG có hạn dùng ⇒ TC này "
            "DỰ KIẾN mã vẫn dùng được. Xem MT-41."),

    tc("予約システムの削除", "DATA-DB-001", "Normal",
       "Bước 3: popup confirm và xóa calendar — kiểm 8 bảng dữ liệu liên quan",
       CAL + "\n- Calendar「レッスンA」có: 3 course, 10 slot, 20 booking, 2 remind, "
             "5 câu hỏi form, setting notify full slot, lịch sử action, setting send message",
       "1. Nhập mã đúng → quan sát popup confirm\n2. Bấm 戻る rồi bấm X (kiểm không xóa)\n"
       "3. Bấm「予約システムを削除する」\n"
       "4. Query 8 bảng: `calendar_course` · `calendar_course_receptions` · "
       "`calendar_course_bookings` · `events` (type=4, booking_calendar_id) · `event_step` · "
       "`event_step_time` · `calendar_setting_send_forms` · `calendar_setting_notify_full_history` · "
       "`calendar_course_booking_history_actions` · `calendar_setting_send_messages`",
       "Calendar đầy đủ dữ liệu",
       "- Popup hiện đúng tên calendar\n- Bấm 戻る / X: đóng popup, KHÔNG xóa\n"
       "- Sau khi xóa: về màn list calendar, calendar biến mất\n"
       "- Dữ liệu ở TẤT CẢ các bảng trên đều bị xóa theo calendar_id tương ứng\n"
       "- Với bảng `events`: CHỈ xóa bản ghi có `booking_calendar_id` = id booking đã xóa VÀ "
       "`type` = 4; KHÔNG xóa bản ghi `type` = 2 của booking calendar\n"
       "- Dữ liệu của các calendar KHÁC KHÔNG bị ảnh hưởng",
       note="Nguồn: Setting calendar r1555-r1560, r1563-r1573."),

    tc("予約システムの削除", "FUNC-001", "Abnormal",
       "LINE user mở URL của calendar đã bị xóa",
       CAL + "\n- Calendar đã bị xóa; LINE user U1 còn giữ URL booking và URL lịch sử cũ",
       "1. U1 mở URL booking → quan sát\n2. U1 mở URL lịch sử → quan sát",
       "2 URL của calendar đã xóa",
       "- Cả 2: hiện message lỗi「この予約ページはすでに削除されています。」\n"
       "- Không lỗi 500, không trắng trang",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1561-r1562."),

    # ══════════════════ Googleスプレッドシート連携 ══════════════════
    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Trạng thái chưa liên kết và luồng liên kết Google",
       CAL + "\n- Calendar chưa liên kết Google",
       "1. Vào menu「Googleスプレッドシート連携」→ quan sát\n"
       "2. Bấm nút Sign in with Google → chọn account, CẤP ĐỦ quyền\n"
       "3. Quan sát màn sau khi liên kết\n4. Bấm link Google Sheet",
       "1 account Google",
       "- Chưa liên kết: hiện「Googleアカウント連携が完了していません」\n"
       "- Bấm Sign in: mở màn OAuth của Google\n"
       "- Sau khi liên kết: hiện tên + avatar account Google vừa liên kết, "
       "note「複数選択の場合、友だち情報に回答を紐付けすることはできません」và "
       "「スプレッドシート利用の注意点」\n"
       "- Bấm link: mở tab mới tới Google Sheet mang tên cửa hàng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1326-r1331, r1473."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Liên kết Google nhưng KHÔNG cấp đủ quyền → báo lỗi, liên kết lại được",
       CAL,
       "1. Liên kết account A, KHÔNG tích cấp quyền → quan sát\n"
       "2. Liên kết lại account A, CẤP ĐỦ quyền → quan sát\n"
       "3. Lần khác: liên kết A không cấp quyền → liên kết account B có cấp quyền\n"
       "4. Không cấp quyền 2 lần liên tiếp → lần 3 cấp quyền",
       "2 account Google",
       "- Không cấp quyền: báo lỗi「Google スプレッドシートのアクセス権限をチェックしてください」\n"
       "- Bước 2: liên kết account A thành công\n- Bước 3: liên kết account B thành công\n"
       "- Bước 4: lần 1 và 2 báo lỗi, lần 3 thành công",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1469-r1472."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Dữ liệu sync lên Google Sheet — booking trước và sau khi liên kết",
       CAL + "\n- Calendar đã có 5 booking TRƯỚC khi liên kết Google",
       "1. Liên kết Google → mở Sheet ngay → quan sát\n"
       "2. Cho U1 booking MỚI → mở Sheet lại → quan sát\n"
       "3. Đổi tên sheet trong file Google → cho booking mới → quan sát\n"
       "4. Ẩn dòng cuối cùng của sheet → cho booking mới → quan sát",
       "5 booking cũ + booking mới",
       "- Bước 1: Sheet chưa có dữ liệu của 5 booking cũ\n"
       "- Bước 2: sau khi có booking mới, Sheet hiển thị TOÀN BỘ booking (cả 5 cũ + 1 mới)\n"
       "- Bước 3: dữ liệu KHÔNG update vào sheet đã đổi tên, mở SHEET MỚI\n"
       "- Bước 4: dữ liệu KHÔNG được update (đã có note cảnh báo trên màn)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1332-r1336."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Cột friend info trên Google Sheet khi thêm / xóa / đổi / sort item",
       CAL + "\n- Calendar đã liên kết Google, có 3 câu hỏi form",
       "1. Thêm câu hỏi Q4 → cho booking mới → quan sát cột trên Sheet\n"
       "2. Xóa câu hỏi Q2 → booking mới → quan sát\n"
       "3. Đổi câu hỏi Q3 sang loại khác → booking mới → quan sát\n"
       "4. Sort lại thứ tự câu hỏi → booking mới → quan sát",
       "4 thao tác trên form",
       "- Thêm: có thêm cột tương ứng (KHÔNG hiển thị title)\n"
       "- Xóa: cột bị xóa được ĐẨY RA SAU\n- Đổi: cột vừa đổi ĐẨY RA SAU\n"
       "- Sort: các cột hiển thị đúng thứ tự đã sort",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1337-r1340."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Cột ステータス trên Google Sheet — ma trận 13 luồng thao tác",
       CAL + "\n- Calendar đã liên kết Google",
       "Tạo booking theo 13 luồng, sau mỗi luồng mở Google Sheet kiểm cột ステータス:\n"
       "1. Admin booking\n2. User request booking\n3. → Deny\n4. → Approve\n"
       "5. User booking approve ngay\n6. Admin cancel\n7. Booking approve → user request cancel\n"
       "8. → Deny\n9. → Approve\n10. User cancel ngay\n11. User booking full slot\n"
       "12. Admin booking full slot\n13. Admin xóa booking",
       "13 luồng",
       "-「予約確定（手動追加）」(1, 12) ·「予約リクエスト」(2) ·「否認」(3) ·「予約確定」(4, 5, 8) ·"
       "「キャンセル（手動）」(6, 13) ·「キャンセルリクエスト」(7) ·「キャンセル」(9, 10)\n"
       "- Luồng 11 (user booking full slot): KHÔNG insert vào file\n"
       "- Luồng 13: hiển thị「キャンセル（手動）」và KHÔNG bị xóa khỏi danh sách trên Sheet",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1346-r1358."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Cột 決済ステータス trên Google Sheet — môi trường product và test",
       CAL + "\n- Calendar đã liên kết Google, enable bill tiền",
       "1. Môi trường PRODUCT: tạo booking theo 5 luồng (admin book · user book approve ngay · "
       "user request booking · request → approve · admin refund · user book course free) → "
       "kiểm cột 決済ステータス\n"
       "2. Đổi sang môi trường TEST: user book và admin book → kiểm\n"
       "3. Disable bill tiền: user book và admin book → kiểm",
       "3 cấu hình × nhiều luồng",
       "- Môi trường PRODUCT: admin book và course free →「決済なし」; user book approve ngay và "
       "request→approve →「決済済み」; user request booking →「未決済」; admin refund →「返金済み」\n"
       "- Môi trường TEST: không bill →「決済なし」; các case còn lại →「テスト決済」\n"
       "- Disable bill tiền: cả user và admin book đều →「決済なし」",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1360-r1369."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Cột 決済ステータス: booking full slot rồi book lại ở môi trường KHÁC",
       CAL + "\n- Calendar enable bill tiền",
       "1. User book full slot ở môi trường TEST → sau đó admin book cho user đó ở môi trường "
       "PRODUCT → kiểm Sheet\n"
       "2. User book full slot ở PRODUCT → sau đó user book lại ở TEST → kiểm Sheet",
       "2 kịch bản đổi môi trường",
       "- Cả 2: áp dụng MÔI TRƯỜNG MỚI tại thời điểm booking (không giữ môi trường cũ)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1370-r1371."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Cột コース trên Sheet: ưu tiên system_name",
       CAL + "\n- Course C1 có cả `course_name` và `system_name`; C2 chỉ có `course_name`",
       "1. Cho booking ở C1 và C2 → mở Sheet kiểm cột コース",
       "2 course",
       "- C1: hiển thị `system_name`\n- C2: hiển thị `course_name`",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1359."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Bug #31595: friend info kiểu 日時 CÓ GIỜ phải sync đủ giờ lên Google",
       CAL + "\n- Có câu hỏi kiểu 日時 setting「時間の記録を利用する」\n- Calendar đã liên kết Google",
       "Với 3 lối đặt (admin book ở WEB · admin book ở APP · LINE user tự book), "
       "và 3 giá trị giờ (00:00 · giờ ngẫu nhiên · 23:59):\n"
       "1. Đặt booking, điền câu hỏi 日時 kèm giờ\n"
       "2. Query `calendar_course_bookings.friend_info`\n3. Mở Google Sheet kiểm cột tương ứng",
       "3 lối đặt × 3 giá trị giờ",
       "- Cả 9 tổ hợp: giá trị lưu trong DB CÓ CẢ NGÀY VÀ GIỜ\n"
       "- Google Sheet hiển thị đủ ngày + giờ (không bị mất phần giờ)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1372, r1382-r1385, r1397-r1400, r1412-r1415 "
            "(Bug #31595, 09/2025)."),

    tc("Googleスプレッドシート連携", "FRIEND-001", "Normal",
       "Sync friend info lên Google — 10 loại item × 4 nguồn tạo booking",
       CAL + "\n- Calendar có 10 loại câu hỏi: name · email · text 1 dòng · text area (có và không "
             "xuống dòng) · radio · dropdown · checkbox (chọn 1 và chọn nhiều) · date (có và không giờ)",
       "Với từng nguồn (admin book WEB · admin book APP · LINE user book · job retry sync):\n"
       "1. Tạo booking, điền đủ 10 loại câu hỏi\n"
       "2. Query `friend_information_values` của user\n3. Mở Google Sheet đối chiếu từng cột",
       "10 loại item × 4 nguồn",
       "- Cả 4 nguồn: friend info được LƯU đúng vào DB và SYNC đúng lên Google Sheet\n"
       "- Text area có xuống dòng: giữ nguyên xuống dòng trên Sheet, không vỡ ô\n"
       "- Checkbox chọn nhiều: các lựa chọn nằm trong 1 ô, không vỡ format CSV/Sheet",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1373-r1430 (4 khối lặp cùng cấu trúc → gộp 1 TC, "
            "liệt kê đủ ở cột Các bước)."),

    tc("Googleスプレッドシート連携", "DATA-REF-001", "Normal",
       "Sync friend info khi admin EDIT giá trị friend info của user",
       CAL + "\n- U1 đã có booking, dữ liệu đã sync lên Sheet",
       "1. Ở màn WEB (app mobile không có nút edit friend info), admin sửa giá trị friend info của U1 "
       "cho 10 loại item\n2. Mở Google Sheet kiểm các cột tương ứng",
       "10 loại item",
       "- Google Sheet cập nhật giá trị MỚI của các item đã sửa",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Setting calendar r1450-r1464 — TC gốc phần lớn CHỈ CÓ TIÊU ĐỀ, "
            "kết quả mong đợi do AI bổ sung. Cần Leader xác nhận."),

    tc("Googleスプレッドシート連携", "DATA-001", "Abnormal",
       "Google Sheet KHÔNG hiển thị booking đã xóa và booking đợi nhận thông báo",
       CAL + "\n- Có booking đã xóa mềm và booking status = 3",
       "1. Mở Google Sheet\n"
       "2. Đối chiếu query `SELECT * FROM calendar_course_bookings WHERE calendar_id = 21 "
       "AND deleted_at IS NULL AND status != 3 ORDER BY id ASC`",
       "Booking đủ trạng thái",
       "- Sheet hiển thị đủ số bản ghi theo query trên\n"
       "- KHÔNG có booking đã xóa và booking status = 3",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1465."),

    tc("Googleスプレッドシート連携", "DATA-REF-001", "Normal",
       "Khôi phục Google Sheet: tạo sheet mới, xóa sheet cũ",
       CAL + "\n- Calendar đã liên kết Google, đã có dữ liệu trên Sheet cũ",
       "1. Tạo sheet mới → xóa sheet cũ → cho booking mới → quan sát sheet mới\n"
       "2. Lần khác: tạo sheet mới nhưng KHÔNG xóa sheet cũ → cho booking mới → quan sát cả 2 sheet",
       "2 kịch bản",
       "- Bước 1: các booking TRƯỚC ĐÂY cũng được get ra sheet tự tạo\n"
       "- Bước 2: dữ liệu hiển thị ở SHEET CŨ (không sang sheet mới)",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1466-r1467."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Ngắt quyền truy cập Google từ phía Google → tool cảnh báo mất liên kết",
       CAL + "\n- Calendar đã liên kết Google account A",
       "1. Vào https://myaccount.google.com/connections, xóa quyền truy cập của LME\n"
       "2. Quay lại tool, mở màn liên kết Google (hoặc thực hiện thao tác cần sync)",
       "Quyền bị thu hồi",
       "- Hiện alert báo mất liên kết Google",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1475."),

    tc("Googleスプレッドシート連携", "STATE-CLEAN-001", "Abnormal",
       "Hủy liên kết Google theo 4 trạng thái google_sheet_status",
       CAL,
       "Với từng trạng thái, bấm hủy liên kết và ghi kết quả:\n"
       "1. `google_sheet_status` = 0 (vừa mới liên kết)\n2. = 1 (job đang tạo sheet)\n"
       "3. = 2 (đã tạo sheet xong)\n4. = 3 (tạo sheet lỗi)",
       "4 trạng thái",
       "- Trạng thái 0, 1, 3: báo lỗi「スプレッドシートを作成しているため、接続を解除できません。"
       "３〜5分少し待ってから操作してください。」\n"
       "- Trạng thái 2: hủy liên kết SUCCESS",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1476-r1479. ⚠️ Spec BR-55: `cancelGoogsheet()` xóa token "
            "nhưng KHÔNG reset `google_sheet_status` ⇒ có thể kẹt ở trạng thái lỗi liên kết. "
            "Xem MT-42."),

    tc("Googleスプレッドシート連携", "FUNC-001", "Normal",
       "Popup confirm hủy liên kết Google",
       CAL + "\n- Calendar đang liên kết Google account A, `google_sheet_status` = 2",
       "1. Bấm「Googleアカウントの接続を解除する」→ quan sát popup\n"
       "2. Bấm X (không hủy)\n3. Mở lại, bấm nút xóa liên kết",
       "—",
       "- Popup hiện tên account Google\n- Bấm X: đóng popup, giữ liên kết\n"
       "- Bấm xóa: hủy liên kết, quay về màn chưa liên kết",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1483-r1486."),

    tc("Googleスプレッドシート連携", "DATA-REF-001", "Normal",
       "Support #32733: calendar liên kết CŨ (chưa có google_sheet_account_email)",
       CAL + "\n- Calendar liên kết Google TRƯỚC khi release Support #32733",
       "1. Query `calendar_management.google_sheet_account_email` → quan sát\n"
       "2. Cho booking mới → kiểm Sheet\n3. Update 1 booking (approve/cancel) → kiểm Sheet\n"
       "4. Bấm hủy liên kết → liên kết lại CÙNG email cũ → query DB và kiểm file Google",
       "Calendar liên kết cũ",
       "- Bước 1: cột `google_sheet_account_email` RỖNG (không recover được)\n"
       "- Bước 2, 3: vẫn sync/update bình thường lên file Google cũ\n"
       "- Bước 4: hủy thành công; liên kết lại thì LƯU được email vào "
       "`google_sheet_account_email` và LUÔN tạo 1 FILE GOOGLE MỚI",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1489-r1494 (Support #32733, 11/2025)."),

    tc("Googleスプレッドシート連携", "JOB-001", "Normal",
       "Support #32733: sync sau khi liên kết lại — 3 mốc thời điểm",
       CAL + "\n- Calendar vừa hủy rồi liên kết lại Google (cùng email hoặc email khác)",
       "1. Ngay sau khi liên kết lại, chưa có booking mới và chưa update booking → kiểm Sheet\n"
       "2. Cho U1 booking MỚI → kiểm Sheet\n3. Update 1 booking CŨ (approve/cancel) → kiểm Sheet",
       "3 mốc",
       "- Bước 1: KHÔNG sync gì (file Google mới trống)\n"
       "- Bước 2: sync TOÀN BỘ booking của calendar vào file Google mới\n"
       "- Bước 3: KHÔNG sync — vì file mới chưa có bản ghi của booking đó thì không update được",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1495-r1497, r1500-r1501, r1519-r1521, r1524-r1526."),

    tc("Googleスプレッドシート連携", "JOB-001", "Normal",
       "Support #32733: liên kết lại CÙNG account sau khi sync LỖI → khôi phục bản ghi thiếu",
       CAL + "\n- Calendar đang liên kết Google nhưng sync lỗi, có bản ghi trong `result_error_googles`\n"
             "- Cột `datetime_connect_google_sheet` đã được ghi",
       "1. Ở modal báo lỗi, bấm liên kết lại với CÙNG account Google cũ\n"
       "2. Query `calendar_management.google_sheet_account_email` và file Google\n"
       "3. Query `result_error_googles` của calendar này\n"
       "4. Chờ job chạy → mở Google Sheet đối chiếu",
       "Bản ghi sync lỗi",
       "- Lưu được email vào `google_sheet_account_email`\n"
       "- KHÔNG tạo file Google mới — calendar vẫn map file cũ\n"
       "- Các bản ghi `result_error_googles` có `created_at` > `datetime_connect_google_sheet` "
       "được update `status` = 0, `retry_time` = 0, `next_retry_time` = NOW để job sync lại\n"
       "- Sau khi job chạy: Google Sheet hiển thị ĐỦ số bản ghi trước đó sync thiếu, "
       "KHÔNG có bản ghi bị TRÙNG, thứ tự các booking đúng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1527-r1531. RULE-08: job nền test PRODUCTION."),

    tc("Googleスプレッドシート連携", "JOB-001", "Abnormal",
       "Support #32733: liên kết lại account KHÁC sau khi sync lỗi → tạo file mới, không khôi phục",
       CAL + "\n- Calendar sync lỗi, có bản ghi `result_error_googles`",
       "1. Liên kết lại với account Google KHÁC\n2. Query DB và kiểm file Google\n"
       "3. Chưa có booking mới → kiểm Sheet\n4. Cho booking mới → kiểm Sheet\n"
       "5. Update booking cũ → kiểm Sheet",
       "Đổi account Google",
       "- Lưu email mới vào `google_sheet_account_email`, LUÔN tạo file Google MỚI\n"
       "- Bước 3: KHÔNG sync lại các booking bị lỗi trước đó\n"
       "- Bước 4: sync TOÀN BỘ booking của calendar vào file mới\n- Bước 5: KHÔNG sync",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1532-r1536."),

    tc("Googleスプレッドシート連携", "JOB-001", "Normal",
       "Retry sync Google: job retry 5 lần theo mốc 1p/5p/10p/30p/60p",
       CAL + "\n- Calendar đã liên kết Google\n- Chuẩn bị điều kiện làm sync FAIL "
             "(ví dụ tạm thu hồi quyền truy cập)",
       "1. Cho U1 booking mới trong lúc sync đang lỗi → query `result_error_googles`\n"
       "2. Theo dõi từng lần job retry, sau mỗi lần query `status`, `retry_time`, `next_time_retry`\n"
       "3. Cho lần retry cuối cùng (lần 5) cũng fail\n4. Kiểm thông báo Chatwork",
       "1 booking sync fail",
       "- Bước 1: thêm bản ghi `result_error_googles` với `status` = 0, `type` = 3, `is_update` = 0\n"
       "- Retry lần 1 (sau 1 phút) fail: `status` = 0, `retry_time` = 2, `next_time_retry` +5 phút\n"
       "- Lần 2 (sau 5p) fail: `retry_time` = 3, +10 phút · Lần 3 (10p): `retry_time` = 4, +30 phút · "
       "Lần 4 (30p): `retry_time` = 5, +60 phút\n"
       "- Lần 5 (60p) fail: `status` = 3 và GỬI THÔNG BÁO CHATWORK\n"
       "- Nếu bất kỳ lần nào thành công: `status` = 2 và dừng retry",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r146-r157 (retry sync google, 07/2025). "
            "RULE-06: verify tới output cuối là thông báo Chatwork."),

    tc("Googleスプレッドシート連携", "JOB-001", "Normal",
       "Retry sync Google: nhánh UPDATE booking (is_update = 1)",
       CAL + "\n- Calendar liên kết Google, đã có booking trên Sheet\n- Sync đang lỗi",
       "1. Update 1 booking (approve/cancel/refund) → query `result_error_googles`\n"
       "2. Cho job retry thành công → mở Sheet kiểm dữ liệu",
       "1 booking update",
       "- Bản ghi `result_error_googles` có `status` = 0, `type` = 3, `is_update` = 1\n"
       "- Sau khi retry thành công: `status` = 2; Sheet cập nhật đúng dữ liệu MỚI NHẤT của booking "
       "tại thời điểm job chạy (status booking, status bill tiền, friend info)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r166-r178."),

    tc("Googleスプレッドシート連携", "DATA-001", "Normal",
       "Retry sync Google thành công → dữ liệu booking đầy đủ trên Sheet",
       CAL + "\n- Booking B1 sync fail rồi được job retry thành công",
       "1. Sau khi job retry success, mở Google Sheet\n2. Đối chiếu từng cột của B1",
       "1 booking retry thành công",
       "- Sheet hiển thị đủ: ngày giờ book · ngày giờ của course · trạng thái booking "
       "(request / approve luôn / admin book) · tên course · thông tin bill tiền · friend info",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Task nhỏ + fix bug KH r158-r165 — TC gốc CHỈ CÓ TIÊU ĐỀ, "
            "kết quả mong đợi do AI bổ sung."),

    tc("Googleスプレッドシート連携", "PERM-002", "Normal",
       "Account staff thao tác liên kết / hủy liên kết Google",
       CAL + "\n- Có staff S1 được cấp quyền route レッスン予約",
       "1. Đăng nhập staff S1 → vào menu Googleスプレッドシート連携\n"
       "2. Thực hiện liên kết Google\n3. Thực hiện hủy liên kết",
       "Account staff",
       "- Staff xem được trạng thái liên kết\n"
       "- Cần chốt: staff CÓ được phép liên kết / hủy liên kết Google hay không",
       spec="Đã hỏi leader",
       note="Nguồn: Setting calendar r1537 — TC gốc CHỈ CÓ TIÊU ĐỀ「Check account staff」, "
            "không có kết quả mong đợi. Spec Gap G-01: dữ liệu phân quyền staff cho FA-019 "
            "chưa xác minh được. Xem MT-43."),
]
