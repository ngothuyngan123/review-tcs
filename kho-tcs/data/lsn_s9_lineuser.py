# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm LINE user (LIFF) + đồng thời/verify API + app mobile +
add link booking vào tin nhắn + phân quyền & môi trường.

Nguồn chính: 11.2 TCsLine_LessonCalendar → tab「Booking phía line user」(395 TC lá, 05/2024 → 07/2026)
  Bug #31477 (08/2025 entry chưa kết bạn) · Feature #35707 (03/2026 xóa booking đợi nhận thông báo) ·
  SpecImprove #32808/#32884 (11/2025 hiển thị dấu -) · SpecImprove #32887 (11/2025 nút 今日) ·
  SpecChange #32646 (10/2025 URL cancel luôn vào được) · SpecImprove #32567 (10/2025 timeout form) ·
  Feature #31268 (08/2025 ẩn text bill tiền) · Bug KH #38280 (06/2026 race condition — KHỐI MỚI NHẤT,
  đã có sẵn TC dạng AI NEW-*/RV-*)
Bổ sung: tab「Task nhỏ + fix bug KH」r20-r49 (Review #29331 tuần/tháng có lịch làm việc),
  TCsLine_Improve chung → tab「add link salon và lesson」(Support #26549, 08/2024).
Spec: BR-P01…BR-P06, BR-P13…BR-P17, S-01…S-04, RP-01.
"""
from _common import tc

LU = ("- Lesson calendar「レッスンA」(id 21) đang ON của bot A\n"
      "- LINE user U1 đã kết bạn với bot A và có bản ghi trong LME, không bị block\n"
      "- Có course C1 đang ON với slot trong tuần hiện tại")

S9 = [
    # ══════════════════ LINE user — mở link & entry ══════════════════
    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Calendar ON / OFF / đã xóa → 3 kết quả khi mở URL booking",
       LU,
       "1. Calendar ON: U1 mở URL booking → quan sát\n"
       "2. Tắt calendar OFF: U1 mở lại → quan sát\n"
       "3. Xóa calendar: U1 mở lại → quan sát",
       "3 trạng thái calendar",
       "- ON: vào màn TOP page\n"
       "- OFF: báo lỗi「この予約は現在利用できません。」\n"
       "- Đã xóa: báo lỗi「この予約ページはすでに削除されています。」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r3-r5 + Setting calendar r1561. "
            "⚠️ TC gốc r4-r5 ghi cùng 1 message cho cả OFF và đã xóa, nhưng Setting calendar r1561 "
            "ghi message riêng cho calendar đã xóa. Xem MT-52."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Bug #31477: user CHƯA kết bạn với bot → redirect màn kết bạn (2 dạng link)",
       "- Lesson calendar「レッスンA」đang ON\n"
       "- LINE user U9 CHƯA kết bạn với bot A, chưa có bản ghi `line_user`",
       "1. U9 mở URL booking dạng LIFF trực tiếp → quan sát\n"
       "2. U9 mở URL dạng https://line.me/R/app/1657492329-pyRxJ8lJ?calendar_id=44 → quan sát\n"
       "3. U9 bấm kết bạn với bot A → mở lại link booking\n"
       "4. Thử booking cả 2 nhánh: course KHÔNG bill tiền và course CÓ bill tiền",
       "User chưa kết bạn",
       "- Bước 1, 2: redirect sang màn KẾT BẠN với bot (KHÔNG văng lỗi "
       "「Trying to get property 'id' of non-object」)\n"
       "- Bước 3, 4: sau khi kết bạn, U9 booking được bình thường ở cả 2 nhánh có/không bill tiền",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r10-r12 (Bug #31477, 08/2025)."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "User đã kết bạn nhưng CHƯA có trong LME → tự thêm vào LME (chỉ với link LIFF trực tiếp)",
       "- LINE user U8 đã kết bạn với bot A nhưng CHƯA có bản ghi trong LME",
       "1. U8 mở URL booking dạng LIFF trực tiếp → quan sát + query `line_user`\n"
       "2. U8 mở URL dạng https://line.me/R/app/… → quan sát",
       "User đã kết bạn, chưa ở LME",
       "- Bước 1: hệ thống TỰ ĐỘNG thêm U8 vào LME; hiển thị màn booking, booking được bình thường "
       "(cả nhánh có và không bill tiền)\n"
       "- Bước 2: KHÔNG tự động add friend được ⇒ KHÔNG mở được màn booking",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r13-r14."),

    tc("LINE user — mở link & entry", "MSG-003", "Abnormal",
       "User bị BOT BLOCK → không mở được màn booking (3 lối vào)",
       LU + "\n- Bot A đã block U1 (`bot_line_user.is_blocked` = 1)",
       "1. U1 mở URL booking dạng LIFF trực tiếp\n2. U1 mở URL dạng line.me/R/app/…\n"
       "3. U1 mở từ button / image map / rich menu",
       "User bị bot block",
       "- Cả 3 lối vào: KHÔNG hiển thị màn booking; màn LIFF đóng lại và quay về màn chat",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r18-r20, r487."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "User đã UNFOLLOW bot → redirect màn kết bạn, kết bạn lại thì booking được",
       "- LINE user U7 đã từng kết bạn rồi UNFOLLOW bot A",
       "1. U7 mở URL booking (3 lối vào: LIFF trực tiếp · line.me/R/app · từ button/image/richmenu)\n"
       "2. U7 kết bạn lại → mở lại link → booking cả 2 nhánh có/không bill tiền",
       "User đã unfollow",
       "- Cả 3 lối vào đều redirect sang màn KẾT BẠN\n"
       "- Sau khi kết bạn lại: booking được bình thường ở cả 2 nhánh",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r21-r23."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Đã kết bạn + có ở LME + không bị block → vào được từ 3 lối",
       LU,
       "1. U1 mở URL LIFF trực tiếp\n2. Mở URL dạng line.me/R/app\n"
       "3. Mở từ button / image map / rich menu\n4. Với mỗi lối, booking cả 2 nhánh có/không bill",
       "3 lối vào",
       "- Cả 3 lối: hiển thị màn booking, booking được bình thường",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r15-r17, r546-r548."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Abnormal",
       "Disable nút submit khi chưa lấy được line_id",
       LU,
       "1. U1 mở link booking bằng app LINE, quan sát nút submit khi CHƯA load được line_id\n"
       "2. Khi đã load được line_id → quan sát nút\n"
       "3. Reload link: nếu vẫn chưa lấy được line_id → quan sát\n"
       "4. Sau reload lấy được line_id → quan sát\n5. Lặp toàn bộ khi mở bằng APP NGOÀI LINE",
       "2 môi trường mở link",
       "- Chưa có line_id: nút bị DISABLE, màu nền #F0F0F0, màu chữ #222222\n"
       "- Có line_id: hiển thị calendar, hiển thị đủ setting, chọn slot được, đặt lịch thành công "
       "và gửi được action sau khi đặt\n"
       "- Reload mà vẫn chưa có line_id: nút VẪN disable",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r24-r40 (Disable button submit, 09/2025)."),

    tc("LINE user — mở link & entry", "CONC-001", "Abnormal",
       "Double click nút đặt lịch phía LINE user → không book trùng",
       LU,
       "1. U1 đi tới màn confirm cuối, double click nhanh nút đặt lịch\n"
       "2. Query `calendar_course_bookings`",
       "1 lần đặt, 2 click",
       "- Chỉ tạo ĐÚNG 1 booking (không duplicate)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r27, r35."),

    tc("LINE user — mở link & entry", "OUT-PREVIEW-001", "Normal",
       "Preview khi admin gửi link booking (OGP)",
       LU + "\n- Calendar đã setting ảnh và mô tả ở màn トップ設定",
       "1. Admin gửi link booking qua chat 1:1 cho U1\n2. Quan sát khối preview trên LINE app",
       "Calendar có ảnh + mô tả",
       "- Preview hiện ảnh, title và description đã setting\n"
       "- Nếu KHÔNG nhập title và description: preview hiện tên cửa hàng và system name",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r6. ⚠️ TC gốc mô tả hành vi của「Calendar cũ」— "
            "cần verify lại với calendar lesson hiện tại. Xem MT-53."),

    tc("LINE user — mở link & entry", "UI-001", "Normal",
       "Màn TOP page và menu trượt phải",
       LU + "\n- Calendar đã setting ảnh, tên cửa hàng, description ở màn トップ設定 và ビジネス情報",
       "1. U1 mở URL booking → quan sát màn top\n2. Bấm nút menu → quan sát\n"
       "3. Bấm「基本情報」\n4. Bấm「予約履歴一覧」\n5. Bấm「特定商取引法に関する記載」\n"
       "6. Bấm「予約にすすむ」",
       "Calendar đã setting đủ",
       "- Màn top hiện đúng ảnh, tên cửa hàng, description theo setting トップ設定\n"
       "- Menu có 3 mục: 基本情報 · 予約履歴一覧 · 特定商取引法に関する記載\n"
       "- 基本情報: hiện data theo setting ビジネス情報\n- 予約履歴一覧: sang màn lịch sử\n"
       "- 特定商取引法: hiện nội dung setting ở màn 決済連携 (chỉ hiện khi ENABLE bill tiền)\n"
       "- 予約にすすむ: sang màn chọn course",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r7-r9, r42-r44, r180-r181."),

    # ══════════════════ LINE user — chọn コース ══════════════════
    tc("LINE user — chọn コース", "UI-001", "Normal",
       "Màn chọn course: thông tin hiển thị và modal detail",
       LU + "\n- Course C1 có ảnh, thời lượng 1h30, giá 5.000 yên, có mô tả\n"
            "- Calendar setting HIỂN THỊ giá course",
       "1. U1 vào màn chọn course → quan sát 1 dòng course\n2. Bấm tên course → quan sát modal\n"
       "3. Với calendar có 20 course: cuộn danh sách",
       "1 course đầy đủ thông tin",
       "- Dòng course: ảnh · tên course · thời gian hoàn thành · giá tiền (theo setting 表示設定)\n"
       "- Modal detail: hiện ảnh, giá, thời lượng và mô tả course\n"
       "- 20 course: cuộn được, hiện đủ, course cuối không bị cắt",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r206-r209."),

    # ══════════════════ LINE user — chọn 受付枠 ══════════════════
    tc("LINE user — chọn 受付枠", "UI-001", "Normal",
       "Màn chọn slot: default hiển thị theo TUẦN, format ngày",
       LU,
       "1. U1 chọn course C1 → quan sát chế độ hiển thị mặc định\n2. Quan sát format ngày",
       "—",
       "- Default hiển thị slot theo TUẦN\n- Format ngày「2024年10月10日（火）」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r211-r212. ⚠️ Feature #27978 thêm setting ưu tiên "
            "hiển thị tuần/tháng ⇒ nếu admin setting ưu tiên tháng thì default là tháng. "
            "Xem TC ở dưới."),

    tc("LINE user — chọn 受付枠", "UI-001", "Normal",
       "Hiển thị slot ở màn TUẦN: 4 trạng thái slot",
       LU + "\n- Trong tuần có: slot A còn trống (定員 5, đã 2 booking), slot B đã full + setting "
            "HIỂN THỊ slot full + TẮT nhận thông báo, slot C đã full + BẬT nhận thông báo, "
            "slot D đã full + setting ẨN slot full + TẮT nhận thông báo",
       "1. U1 vào màn chọn slot theo tuần → quan sát 4 slot\n"
       "2. Quan sát cách xếp slot trong 1 ngày",
       "4 trạng thái slot",
       "- Slot A: ENABLE, icon「◯」, hiện「残り 3」\n"
       "- Slot B: DISABLE, icon「-」, hiện「残り 0」\n"
       "- Slot C: ENABLE, icon hình LOA, hiện「通知受け取り」\n"
       "- Slot D: BỊ ẨN hoàn toàn\n"
       "- Trong 1 ngày: 3 slot / 1 hàng, sort theo thời gian nhỏ nhất lên đầu, > 3 slot thì xuống dòng\n"
       "- Format thời gian slot「12:00 - 13:00」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r216-r222 + spec BR-P04."),

    tc("LINE user — chọn 受付枠", "UI-001", "Normal",
       "Hiển thị slot ở màn THÁNG: enable/disable từng ngày và list slot phía dưới",
       LU + "\n- Trong tháng: ngày 05 có slot còn chỗ, ngày 10 có slot đã full (tắt nhận thông báo), "
            "ngày 15 có slot full nhưng vừa được nới thêm chỗ",
       "1. U1 chuyển sang chế độ xem THÁNG → quan sát calendar\n"
       "2. Bấm vào ngày 05 → quan sát vùng slot phía dưới\n3. Bấm next/back tháng",
       "3 ngày khác trạng thái",
       "- Cột từ thứ 2 → CN; hiển thị cả ngày của tháng trước/sau\n"
       "- Ngày quá khứ và ngày tháng sau: DISABLE\n"
       "- Mặc định CHƯA chọn ngày nào (vùng slot phía dưới trống)\n"
       "- Ngày 05: ENABLE · Ngày 10: DISABLE · Ngày 15: ENABLE (sau khi nới chỗ)\n"
       "- Bấm ngày enable: hiện list slot của course trong ngày đó\n"
       "- Bấm next/back: hiện lịch tháng tương ứng, vùng slot phía dưới KHÔNG hiện data",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r228-r235, r241-r246."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "Chọn slot còn trống / slot full có nhận thông báo → 2 màn khác nhau",
       LU + "\n- Slot A còn trống; slot C đã full và BẬT nhận thông báo",
       "1. Ở màn TUẦN: chọn slot A → quan sát\n2. Chọn slot C → quan sát\n"
       "3. Chọn slot của tuần tương lai (cả A và C) → quan sát\n"
       "4. Kiểm slot của tuần quá khứ\n5. Lặp toàn bộ ở màn THÁNG",
       "2 loại slot × 2 chế độ xem",
       "- Chọn slot còn trống: sang màn nhập thông tin booking\n"
       "- Chọn slot full có nhận thông báo: sang màn confirm ĐĂNG KÝ NHẬN THÔNG BÁO\n"
       "- Slot của tuần/tháng quá khứ: KHÔNG hiển thị",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r223-r227, r242-r246."),

    tc("LINE user — chọn 受付枠", "FUNC-DATE-001", "Boundary",
       "SpecImprove #32808/#32884: chưa tới giờ MỞ nhận đặt → hiển thị dấu「-」",
       LU + "\n- Slot start 08:00 ngày 05/12",
       "Ở CẢ màn TUẦN và màn THÁNG, với từng setting:\n"
       "1. Setting「いつでも予約を受け付ける」, hiện tại 12:00 ngày 02/12 → quan sát\n"
       "2. Setting 日数指定 mở nhận trước 0 ngày lúc 12:00, hiện tại 0 ngày lúc 08:00 → quan sát\n"
       "3. Cùng setting, hiện tại 0 ngày lúc 12:30 → quan sát\n"
       "4. Setting 時間指定 mở nhận trước 2 giờ 30 phút, hiện tại còn 4 giờ → quan sát\n"
       "5. Cùng setting, hiện tại còn 2 giờ → quan sát",
       "5 mốc thời gian × 2 chế độ xem",
       "- Trường hợp 1, 3, 5 (đã tới giờ mở nhận đặt): hiển thị「◯」\n"
       "- Trường hợp 2, 4 (chưa tới giờ): hiển thị「-」ngay từ đầu, KHÔNG chờ tới lúc bấm mới báo lỗi",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r249-r257, r273-r281 (SpecImprove #32808 + #32884, 11/2025). "
            "⚠️ Spec BR-P05 nói chế độ 月 LOẠI BỎ slot chưa tới giờ mở nhận đặt còn chế độ 週 chỉ KHOÁ "
            "⇒ 2 chế độ hiển thị LỆCH nhau. Xem MT-54."),

    tc("LINE user — chọn 受付枠", "FUNC-DATE-001", "Boundary",
       "Đã quá giờ DỪNG nhận đặt → ẩn hẳn slot",
       LU + "\n- Slot start 12:00 ngày 02/12",
       "Ở CẢ màn TUẦN và THÁNG:\n"
       "1. Setting「いつでも」, hiện tại 12:10 ngày 02/12 (đã quá start) → quan sát\n"
       "2. Setting 日数指定 dừng nhận trước 0 ngày lúc 12:00, hiện tại 08:00 → quan sát\n"
       "3. Cùng setting, hiện tại 12:30 → quan sát\n"
       "4. Setting 時間指定 dừng nhận trước 2 giờ 30 phút, hiện tại còn 4 giờ → quan sát\n"
       "5. Cùng setting, hiện tại còn 2 giờ → quan sát",
       "5 mốc thời gian",
       "- Trường hợp 2, 4 (chưa tới hạn dừng): hiển thị「◯」\n"
       "- Trường hợp 1, 3, 5 (đã quá hạn dừng): ẨN HẲN slot (không phải disable)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r261-r269, r282-r290, r405-r413 (Support #26508, 08/2024)."),

    tc("LINE user — chọn 受付枠", "FUNC-004", "Boundary",
       "Màn THÁNG: 1 ngày có 2 slot — ma trận 8 tổ hợp trạng thái",
       LU + "\n- Ngày 03/12 có 2 slot, mỗi tổ hợp setting time nhận/dừng nhận khác nhau",
       "Với từng tổ hợp, quan sát ô ngày 03/12 ở màn tháng:\n"
       "1. CẢ 2 slot chưa tới giờ nhận\n2. CẢ 2 slot đã tới giờ nhận\n"
       "3. CẢ 2 slot chưa tới hạn dừng\n4. CẢ 2 slot đã quá hạn dừng\n"
       "5. 1 slot chưa tới giờ nhận + 1 slot đã tới giờ nhận\n"
       "6. 1 chưa tới giờ nhận + 1 chưa tới hạn dừng\n"
       "7. 1 chưa tới giờ nhận + 1 đã quá hạn dừng\n"
       "8. 1 đã tới giờ nhận + 1 đã quá hạn dừng\n"
       "9. 1 chưa tới hạn dừng + 1 đã quá hạn dừng",
       "9 tổ hợp",
       "- Tổ hợp 1: hiển thị「-」\n- Tổ hợp 4: ngày đó KHÔNG hiển thị slot nào\n"
       "- Tổ hợp 7: hiển thị「-」\n"
       "- Tổ hợp 2, 3, 5, 6, 8, 9: hiển thị「◯」\n"
       "⇒ Chỉ cần 1 slot còn đặt được thì ngày hiện「◯」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r294-r303."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "Review #29331: tuần/tháng hiện tại không có lịch → tự nhảy tới tuần/tháng gần nhất có lịch",
       LU,
       "Với CẢ chế độ TUẦN và THÁNG, chuẩn bị từng kịch bản rồi cho U1 mở màn chọn slot:\n"
       "1. Tuần/tháng 1 (hiện tại) CÓ lịch làm việc\n2. Tuần 1 không có, tuần 2 có\n"
       "3. Tuần 1-2 không có, tuần 3 có\n4. Tuần 1-3 không có, tuần 4 có\n"
       "5. Tuần 1-4 không có, tuần 5 có\n6. Tuần 1-5 đều KHÔNG có lịch",
       "6 kịch bản × 2 chế độ",
       "- Kịch bản 1: hiện tuần/tháng hiện tại\n- Kịch bản 2-5: hiện tuần/tháng gần nhất CÓ lịch\n"
       "- Kịch bản 6: hiện tuần 5 (hoặc tháng 3) kể cả không có lịch — dừng nhảy sau tối đa "
       "4 tuần / 2 tháng",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r21-r26, r35-r38 (Review #29331, 03/2025) + spec BR-P06."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "Review #29331: các trường hợp lịch có nhưng không đặt được",
       LU,
       "Với CẢ chế độ TUẦN và THÁNG:\n"
       "1. Tuần có lịch nhưng chỉ ở ngày QUÁ KHỨ (hôm nay 07/5, chỉ 05/5 có lịch)\n"
       "2. Tuần có lịch, các slot đều FULL nhưng setting HIỂN THỊ slot full hoặc BẬT nhận thông báo\n"
       "3. Tuần có lịch, các slot đều FULL + setting ẨN slot full + TẮT nhận thông báo\n"
       "4. Tuần có lịch nhưng CHƯA tới giờ mở nhận đặt\n"
       "5. Tuần có lịch nhưng ĐÃ QUÁ hạn dừng nhận đặt",
       "5 kịch bản × 2 chế độ",
       "- Kịch bản 1: nhảy sang tuần/tháng tiếp theo CÓ lịch\n"
       "- Kịch bản 2: hiện tuần/tháng HIỆN TẠI\n"
       "- Kịch bản 3: nhảy sang tuần/tháng tiếp theo có lịch\n"
       "- Kịch bản 4: VẪN hiện tuần/tháng hiện tại (slot hiện ra nhưng bấm vào báo lỗi)\n"
       "- Kịch bản 5: nhảy sang tuần/tháng tiếp theo có lịch",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r27-r31, r39-r42."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "Review #29331: nút next/back và nút 今日 sau khi đã tự nhảy",
       LU + "\n- Tuần hiện tại KHÔNG có lịch, tuần 3 mới có lịch",
       "1. U1 mở màn chọn slot (tự nhảy sang tuần 3)\n"
       "2. Bấm next tuần rồi back tuần → quan sát\n3. Bấm nút「今日」→ quan sát\n"
       "4. Lặp ở chế độ THÁNG\n5. Chuyển đổi qua lại giữa 2 chế độ tuần/tháng\n"
       "6. Mở màn chọn slot từ chức năng COPY BOOKING → quan sát",
       "Tuần hiện tại không lịch",
       "- Bước 2: next/back đi LẦN LƯỢT từng tuần, kể cả tuần không có lịch\n"
       "- Bước 5, 6: hiện đúng tuần/tháng gần nhất có lịch (giống lúc mở booking mới)\n"
       "- Bước 3 (nút 今日): xem TC SpecImprove #32887 phía dưới — HÀNH VI ĐÃ ĐỔI",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r32-r34, r43-r49."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "SpecImprove #32887: nút 今日 LUÔN về tuần/tháng chứa hôm nay",
       LU,
       "Với CẢ chế độ TUẦN và THÁNG, với từng kịch bản, bấm nút「今日」/「今月」:\n"
       "1. Tuần/tháng hiện tại CÓ lịch làm việc\n2. Tuần/tháng hiện tại KHÔNG có lịch\n"
       "3. Tuần/tháng hiện tại có lịch nhưng slot đều đã limit\n"
       "4. Có lịch nhưng chưa tới giờ mở nhận đặt\n5. Có lịch nhưng đã quá hạn dừng nhận đặt",
       "5 kịch bản × 2 chế độ",
       "- TẤT CẢ kịch bản: hiển thị tuần/tháng CHỨA HÔM NAY (không nhảy sang tuần/tháng có lịch)\n"
       "- Kịch bản 2, 5: hiện tuần hiện tại, KHÔNG hiển thị message gì\n"
       "- Kịch bản 1, 3, 4: hiện tuần hiện tại kèm lịch làm việc\n"
       "⇒ Quy tắc nhảy 4 tuần CHỈ áp dụng lúc MỚI MỞ calendar",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r307-r318 (SpecImprove #32887, 11/2025 — GHI ĐÈ hành vi "
            "cũ ở Task nhỏ r34/r45). Xem MT-55."),

    tc("LINE user — chọn 受付枠", "STATE-DEP-001", "Abnormal",
       "Đang booking thì tới giờ dừng nhận / slot vừa full",
       LU + "\n- Slot A sắp tới hạn dừng nhận đặt trong 1 phút",
       "1. U1 chọn slot A, đang ở màn nhập thông tin → chờ qua hạn dừng nhận\n"
       "2. Bấm nút hoàn tất → quan sát\n"
       "3. Kịch bản khác: slot vừa đủ full trong lúc U1 đang nhập → bấm hoàn tất",
       "Trạng thái đổi giữa chừng",
       "- Bước 2: hiện message「予約の受付が終了されました。」\n"
       "- Bước 3: nếu BẬT nhận thông báo → báo đã đặt hết, mời chọn chỗ khác; "
       "nếu TẮT → báo lỗi để user quay lại booking từ đầu",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r304-r306, r473-r474."),

    tc("LINE user — chọn 受付枠", "FUNC-001", "Normal",
       "Feature #27978: setting ưu tiên hiển thị tuần / tháng phía LINE user",
       LU,
       "1. Admin setting ưu tiên hiển thị TUẦN → U1 mở booking mới → quan sát\n"
       "2. U1 vào từ màn lịch sử rồi bấm copy booking → quan sát\n"
       "3. Admin đổi sang ưu tiên THÁNG → lặp bước 1-2\n"
       "4. Kiểm màn LỊCH SỬ của U1 (không phải màn chọn slot)",
       "2 setting ưu tiên",
       "- Setting tuần: cả 2 lối vào đều mở màn chọn slot theo TUẦN\n"
       "- Setting tháng: cả 2 lối vào đều mở theo THÁNG\n"
       "- Màn LỊCH SỬ: KHÔNG theo setting này (giữ hiển thị riêng)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Setting calendar r1575-r1584 (Feature #27978) — TC gốc CHỈ CÓ TIÊU ĐỀ, "
            "kết quả mong đợi do AI bổ sung. Cần Leader xác nhận."),

    # ══════════════════ LINE user — nhập form & xác nhận ══════════════════
    tc("LINE user — nhập form & xác nhận", "FUNC-003", "Abnormal",
       "Form booking: 4 rule validate của item 短文回答 (phía LINE user)",
       LU + "\n- Calendar có 4 câu hỏi 短文回答 với 4 rule: カナ入力 · 電話番号 11 số · "
            "メールアドレス · 整数",
       "Với từng câu hỏi, U1 nhập giá trị sai rồi đúng, bấm next:\n"
       "1. カナ: nhập「abc」rồi「タロウ」\n"
       "2. SĐT: nhập「abc」· 9 số · 13 số · 10 số · 11 số · 12 số\n"
       "3. Email: nhập「abc」rồi「a+b@test.com」\n4. 整数: nhập「1.5」rồi「10」",
       "4 rule",
       "- カナ sai: báo lỗi; đúng: pass\n"
       "- SĐT: không phải số → Invalid; < 10 số hoặc > 12 số → báo lỗi; 10-12 số → PASS\n"
       "- Email sai format: báo lỗi; email có dấu + : pass\n"
       "- 整数 không nguyên: báo lỗi; số nguyên: pass\n"
       "- Sau khi submit: giá trị lưu đúng vào friend info tương ứng",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r327-r331. 🔴 MÂU THUẪN: phía LINE user chấp nhận SĐT "
            "10-12 số, nhưng phía ADMIN (Quản lý calendar_new r543) chỉ chấp nhận ĐÚNG 11 số. "
            "Xem MT-56."),

    tc("LINE user — nhập form & xác nhận", "FUNC-002", "Abnormal",
       "Form booking: câu hỏi 必須 bỏ trống → message required riêng phía LINE user",
       LU + "\n- Có câu hỏi Q1 設定 必須 và Q2 設定 任意",
       "1. Bỏ trống cả Q1 và Q2 → bấm next\n2. Điền Q1, bỏ trống Q2 → bấm next",
       "2 mức bắt buộc",
       "- Bước 1: báo lỗi「回答を入力してください」ở Q1\n- Bước 2: pass",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r332-r334."),

    tc("LINE user — nhập form & xác nhận", "FRIEND-001", "Normal",
       "Form booking: 3 kiểu liên kết friend info khi LINE user tự đặt",
       LU + "\n- Có 3 câu hỏi: Q1 không gắn friend info, Q2 tự tạo friend info, Q3 gắn friend info có sẵn",
       "1. U1 booking, điền cả 3 câu → hoàn tất\n"
       "2. Query `friend_information_values` của U1 và mở màn 友だち情報管理\n"
       "3. U1 booking LẦN 2 → quan sát các ô có được fill sẵn không",
       "3 kiểu liên kết",
       "- Q1: không gán vào friend info nào\n"
       "- Q2: tự tạo friend info và gán giá trị U1 đã nhập\n- Q3: gán vào friend info đã chọn\n"
       "- Nếu U1 KHÔNG trả lời câu nào thì câu đó không gán giá trị cho U1\n"
       "- Bước 3: các ô được fill sẵn hay không phụ thuộc setting "
       "「すでに友だち情報が登録されている場合、初めから入力された状態にする」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r335-r337, r346-r347."),

    tc("LINE user — nhập form & xác nhận", "DATA-REF-001", "Abnormal",
       "Calendar KHÔNG setting câu hỏi nào → vẫn bắt buộc 2 item mặc định",
       LU + "\n- Calendar đã xóa/tắt hết câu hỏi tự tạo",
       "1. U1 vào màn nhập thông tin → quan sát",
       "0 câu hỏi tự tạo",
       "- VẪN hiển thị 2 item mặc định: họ tên và email (bắt buộc nhập)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r326."),

    tc("LINE user — nhập form & xác nhận", "DATA-REF-001", "Abnormal",
       "Case đặc biệt: đổi vị trí 2 form mặc định + bill tiền → lỗi validate email",
       LU + "\n- Calendar ENABLE bill tiền\n- Admin ĐỔI VỊ TRÍ 2 form mặc định (email lên trước họ tên)",
       "1. U1 booking course có giá, điền đủ thông tin → bấm submit\n2. Quan sát message",
       "2 form mặc định bị đổi vị trí",
       "- KHÔNG được báo lỗi invalid email sai chỗ\n"
       "- ⚠️ Nếu tái hiện bug (dev luôn fill giá trị thứ 2 của form là email): báo lỗi "
       "invalid email dù đã nhập đúng ⇒ raise bug",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r325 — TC gốc mô tả nguyên nhân bug nhưng CHỈ CÓ TIÊU ĐỀ. "
            "Kết quả mong đợi do AI viết theo mô tả. Cần Leader xác nhận đã fix chưa."),

    tc("LINE user — nhập form & xác nhận", "ENV-001", "Abnormal",
       "SpecImprove #32567: server chậm / mất mạng khi load màn nhập form",
       LU,
       "Kịch bản A — server chậm (nhờ dev sửa sleep để tái hiện):\n"
       "1. U1 chọn slot → next sang màn nhập form → quan sát\n"
       "2. Quan sát nút next step khi form chưa load xong\n"
       "3. Sau khi hết timeout → quan sát\n4. Bấm「トーク画面に戻る」và bấm X\n"
       "5. Hoàn tất booking → kiểm friend info\n"
       "Kịch bản B — mất mạng:\n"
       "6. Ở màn chọn slot, TẮT MẠNG rồi bấm chọn slot và next → quan sát\n"
       "7. Bật lại mạng, bấm booking tiếp → kiểm friend info của booking",
       "2 kịch bản lỗi mạng",
       "- Bước 1-3: hiện LOADING, sau khi hết timeout hiện màn theo design (không hiện form trắng)\n"
       "- Bước 2: nút next step bị DISABLE cho tới khi form load xong\n"
       "- Bước 4: đóng màn hình và quay lại LINE talk\n"
       "- Bước 5, 7: U1 booking thành công VÀ CÓ đầy đủ thông tin friend info đã nhập\n"
       "- Bước 6: sau fix — reload lại URL, phía user quay về màn đầu tiên để booking lại từ đầu\n"
       "- ⚠️ Nếu tái hiện bug cũ: booking success NHƯNG KHÔNG có thông tin friend info ⇒ raise bug",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r529-r545 (SpecImprove #32567, 10/2025). "
            "Kiểm cả khi mở URL NGOÀI app LINE."),

    tc("LINE user — nhập form & xác nhận", "FUNC-001", "Normal",
       "Màn nhập form: nút back, double click submit, validate lại",
       LU + "\n- Có 2 câu hỏi bắt buộc",
       "1. Ở màn nhập form, bấm nút back → quan sát\n"
       "2. Quay lại, bỏ trống câu bắt buộc → bấm submit\n3. Điền đủ, double click nút submit",
       "—",
       "- Bước 1: quay lại màn chọn slot\n- Bước 2: báo lỗi ở câu bắt buộc\n"
       "- Bước 3: chỉ tạo 1 booking",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r532-r534."),

    tc("LINE user — nhập form & xác nhận", "UI-001", "Normal",
       "Feature #31268: ẩn text về thẻ khi calendar/course không có bill tiền",
       LU,
       "Với từng tổ hợp, U1 booking tới màn confirm request và màn booking success:\n"
       "1. Calendar KHÔNG enable bill tiền\n2. Calendar enable bill + course KHÔNG có giá\n"
       "3. Calendar enable bill + course CÓ giá",
       "3 tổ hợp",
       "- Tổ hợp 1, 2: ẨN text「※前ページでカード情報を入力された方は、リクエストが承認された時に、"
       "カード決済が行われます。」ở màn confirm và ẩn「※予約時にカード情報を入力された方は、"
       "リクエストが承認された時に、カード決済が行われます。」ở màn booking success\n"
       "- Tổ hợp 3: GIỮ NGUYÊN cả 2 text",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r488-r494 (Feature #31268, 01/2026)."),

    tc("LINE user — nhập form & xác nhận", "STATE-DEP-001", "Abnormal",
       "Verify lại data ở bước confirm — admin đổi setting giữa chừng (6 kịch bản)",
       LU + "\n- U1 đang ở bước sau khi chọn slot (nhập form / nhập thẻ)",
       "Với từng kịch bản, admin thao tác trong lúc U1 đang booking, sau đó U1 bấm confirm:\n"
       "1. Admin đổi 定員 của slot = đúng số booking hiện tại, ĐANG BẬT nhận thông báo\n"
       "2. Cùng thao tác nhưng TẮT nhận thông báo\n3. Admin XÓA course mà U1 đã chọn\n"
       "4. Admin XÓA slot mà U1 đã chọn\n5. Admin đổi time nhận / dừng nhận booking\n"
       "6. Admin đổi giới hạn số lần booking của 1 user = 1 (U1 đã có 1 booking)",
       "6 kịch bản",
       "- Kịch bản 1: báo「đã đặt hết, vui lòng đặt chỗ khác」\n"
       "- Kịch bản 2: báo lỗi để user quay lại booking từ đầu\n"
       "- Kịch bản 3: báo lỗi course không tồn tại\n- Kịch bản 4: báo lỗi slot không tồn tại\n"
       "- Kịch bản 5: báo lỗi hết thời gian nhận booking / chưa tới thời gian nhận booking\n"
       "- Kịch bản 6: báo lỗi đã đầy booking của user",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r473-r477, r480."),

    tc("LINE user — nhập form & xác nhận", "STATE-DEP-001", "Normal",
       "Verify lại data: admin xóa câu hỏi / xóa friend info giữa chừng → VẪN booking được",
       LU + "\n- U1 đã trả lời xong danh sách câu hỏi, đang ở màn confirm",
       "1. Admin XÓA 1 item câu hỏi ở màn 質問項目 → U1 bấm confirm\n"
       "2. Admin xóa friend info (đang gắn vào 1 câu hỏi) ở màn 友だち情報管理 → U1 confirm\n"
       "3. Admin đổi format validate của câu hỏi (SĐT → katakana) → U1 confirm\n"
       "4. Kịch bản 3 nhưng U1 đã ở màn confirm rồi back lại nhập lại",
       "4 kịch bản",
       "- Cả 4 kịch bản: U1 VẪN booking success (không bị chặn)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r482-r483, r485-r486."),

    # ══════════════════ LINE user — lịch sử & copy ══════════════════
    tc("LINE user — lịch sử & copy", "LIST-001", "Normal",
       "Feature #35707: màn lịch sử chia 3 nhóm theo đúng thứ tự",
       LU + "\n- U1 có booking ở đủ trạng thái: hiện tại (chưa tới giờ), đợi nhận thông báo, quá khứ",
       "1. U1 mở màn lịch sử booking dạng LIST → quan sát thứ tự các nhóm\n"
       "2. Lặp ở dạng THÁNG\n3. Mở link NGOÀI app LINE → quan sát\n"
       "4. Kiểm booking của user KHÁC có bị lẫn vào không",
       "3 nhóm booking",
       "- Thứ tự hiển thị: 現在の予約 → 通知受け取り → 過去の予約\n"
       "- Cả trong và ngoài app LINE đều cùng thứ tự\n"
       "- Chỉ hiển thị booking của CHÍNH U1, không lẫn của user khác\n"
       "- Sort theo thời gian booking, mới nhất lên đầu\n"
       "- Nhóm 現在: status 0,1,2,4,5,6,7 · Nhóm 通知受け取り: status 3 · "
       "Nhóm 過去: status 0,1,2,3,4,5,6,7",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r48-r54, r105-r106, r128-r130, r175-r176 "
            "(Feature #35707, 03/2026)."),

    tc("LINE user — lịch sử & copy", "UI-001", "Normal",
       "Màn lịch sử: 7 nhãn trạng thái booking",
       LU + "\n- U1 có booking ở đủ 7 trạng thái",
       "1. Mở màn lịch sử → quan sát nhãn từng booking",
       "7 trạng thái",
       "-「予約リクエスト中」(đang chờ approve) ·「予約確定」(đã approve) ·「否認済」(bị deny) ·"
       "「キャンセルリクエスト中」·「キャンセル」·「通知受け取り」(đăng ký chờ hủy) ·"
       "「終了」(booking quá khứ)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r55-r61, r80-r86."),

    tc("LINE user — lịch sử & copy", "UI-001", "Normal",
       "Màn lịch sử: nội dung 1 dòng booking và setting hiển thị giá",
       LU + "\n- Booking của course C1 có ảnh, giá 5.000 yên; calendar đã setting text thay nhãn コース",
       "1. Quan sát 1 dòng booking\n"
       "2. Với 3 tổ hợp setting giá: (không hiển thị + không bill) · (không hiển thị + có bill) · "
       "(có hiển thị) → quan sát cột giá",
       "3 tổ hợp setting giá",
       "- Dòng booking: ảnh course (không có ảnh thì dùng ảnh mặc định) · tên course · "
       "ngày giờ booking format「2024/10/10 (火) 13:00 - 14:00」· số tiền · "
       "nút mở detail · nút copy booking\n"
       "- Nhãn cột course hiện TEXT THAY THẾ đã setting (không phải「コース」)\n"
       "- Tổ hợp 1: KHÔNG hiện giá · Tổ hợp 2, 3: CÓ hiện giá",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r67-r79, r141-r146."),

    tc("LINE user — lịch sử & copy", "STATE-001", "Abnormal",
       "Booking của course đã OFF / đã XÓA → không hiện ở lịch sử",
       LU + "\n- U1 đã booking course C1, sau đó admin OFF C1; U1 cũng đã booking C2 rồi C2 bị xóa",
       "1. U1 mở màn lịch sử (cả dạng list và dạng tháng) → quan sát",
       "1 course OFF + 1 course đã xóa",
       "- Booking của C1 (course OFF) KHÔNG hiện ở màn lịch sử\n"
       "- Booking của C2 (course đã xóa) KHÔNG hiện ở màn lịch sử",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r62-r63, r139-r140. 🔴 MÂU THUẪN「Quản lý course」r225 "
            "(Feature #27496) nói booking của course OFF VẪN hiện ở lịch sử. Xem MT-07."),

    tc("LINE user — lịch sử & copy", "FUNC-002", "Normal",
       "Booking của course bị FILTER ẩn → VẪN hiện ở lịch sử",
       LU + "\n- Ban đầu course C1 không có filter, U1 đã booking\n"
            "- Sau đó admin thêm filter khiến C1 không hiển thị với U1",
       "1. U1 mở màn lịch sử → quan sát booking của C1\n2. U1 bấm nút copy booking đó",
       "Course bị filter",
       "- Booking của C1 VẪN hiện ở màn lịch sử\n"
       "- Bấm copy: báo lỗi course không tồn tại",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r64, r116."),

    tc("LINE user — lịch sử & copy", "FUNC-001", "Normal",
       "Copy booking (同じ内容で予約) — 7 trạng thái booking nguồn",
       LU + "\n- U1 có booking ở 7 trạng thái",
       "Với từng trạng thái, bấm nút「同じ内容で予約」và ghi kết quả:\n"
       "1. Đang chờ approve\n2. Đã được approve\n3. Bị denied\n4. Đang request cancel\n"
       "5. Đã cancel\n6. Đang đăng ký chờ hủy\n7. Đã hoàn thành (quá khứ)",
       "7 trạng thái",
       "- Trạng thái 2: chọn sẵn course tương ứng và nhảy tới màn chọn slot của course đó\n"
       "- Các trạng thái còn lại: cần chốt hành vi (TC gốc chỉ ghi「Làm giống tương tự bên booking "
       "calendar」và các dòng còn lại KHÔNG có kết quả)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: Booking phía line user r109-r115, r149-r155. ⚠️ 6/7 trạng thái KHÔNG có kết quả "
            "mong đợi. Xem MT-57."),

    tc("LINE user — lịch sử & copy", "FUNC-004", "Boundary",
       "Copy booking khi đã đạt giới hạn số lần booking của user",
       LU + "\n- Calendar setting giới hạn 1 booking/user; U1 đã đạt giới hạn\n"
            "- Có slot A còn trống và slot B đã full (bật nhận thông báo)",
       "1. U1 bấm copy booking → chọn slot A → quan sát\n2. Bấm copy → chọn slot B → quan sát",
       "2 loại slot",
       "- Slot A: báo message đã đạt giới hạn booking\n"
       "- Slot B (đăng ký nhận thông báo): BOOKING SUCCESS (không tính vào giới hạn)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r117-r118, r156-r157 + spec BR-P07 "
            "(「Bỏ qua hoàn toàn khi register_notify_slot」)."),

    tc("LINE user — lịch sử & copy", "UI-001", "Normal",
       "Màn lịch sử dạng THÁNG: calendar và next/back tháng",
       LU + "\n- U1 có booking ở nhiều tháng",
       "1. Bấm nút「月次」→ quan sát tháng mặc định và format\n"
       "2. Bấm next tháng, back tháng\n3. Bấm next/back liên tục nhiều lần\n4. Bấm「一覧」",
       "Booking nhiều tháng",
       "- Default hiển thị tháng hiện tại, format「2024年10月」\n"
       "- Next/back: hiển thị đúng dữ liệu booking của tháng đã chọn, chỉ của U1\n"
       "- Next/back liên tục: dữ liệu load kịp, không treo, không hiển thị sai tháng\n"
       "- Bấm 一覧: quay lại màn lịch sử dạng list",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r120-r124, r178."),

    tc("LINE user — lịch sử & copy", "UI-001", "Normal",
       "Màn detail booking từ lịch sử: 2 nhóm nút theo trạng thái",
       LU + "\n- U1 có booking hiện tại (đã approve) và booking quá khứ",
       "1. Ở nhóm 現在の予約, bấm「詳細を見る」→ quan sát nội dung và nút\n"
       "2. Ở nhóm 過去の予約, bấm「詳細を見る」→ quan sát\n"
       "3. Bấm nút「< 一覧に戻る」từ 2 lối vào (từ list và từ tháng)",
       "2 nhóm booking",
       "- Booking hiện tại: hiện thời gian đến format「2024/10/10 (火) 13:00 - 14:00」· tên course "
       "(theo setting thay thế) · số tiền (theo setting hiển thị) · thời gian course; "
       "CÓ nút cancel và nút copy\n"
       "- Booking quá khứ: KHÔNG có nút cancel, CHỈ có nút copy\n"
       "- Nút 一覧に戻る: quay về ĐÚNG màn list trước đó (list hoặc tháng)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r107-r108, r147-r148, r182-r193."),

    # ══════════════════ LINE user — hủy booking ══════════════════
    tc("LINE user — hủy booking", "STATE-DEP-001", "Normal",
       "Hủy booking đã approve: 2 chế độ duyệt hủy",
       LU + "\n- U1 có booking đã approve ở slot tương lai",
       "1. Setting cancel = 全承認: U1 bấm hủy → confirm → query DB + kiểm bộ đếm slot + "
       "kiểm tin LINE U1\n"
       "2. Setting cancel = リクエスト制: U1 bấm hủy → confirm → query\n"
       "3. Admin deny request cancel → query\n4. Admin approve request cancel → query",
       "2 chế độ duyệt hủy",
       "- Chế độ 全承認: cancel success ngay, `status` = 4, số chỗ còn lại của slot +1, "
       "U1 nhận action cancel; nếu có user đang chờ nhận thông báo thì họ được gửi thông báo\n"
       "- Chế độ リクエスト制: chuyển sang `status` = 5 (キャンセルリクエスト中)\n"
       "- Admin deny: quay về `status` = 1 (đã approve)\n- Admin approve: `status` = 4",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r464-r465. RULE-07: verify DB + bộ đếm + action."),

    tc("LINE user — hủy booking", "STATE-DEP-001", "Abnormal",
       "Hủy booking ĐANG CHỜ APPROVE và rút lại yêu cầu hủy",
       LU + "\n- U1 có booking status リクエスト (chưa được approve)\n"
            "- U1 có booking khác đang ở status キャンセルリクエスト",
       "1. U1 mở detail booking đang chờ approve → tìm nút hủy\n"
       "2. Nếu có, bấm hủy → query DB\n"
       "3. U1 mở detail booking đang request cancel → tìm nút hủy việc cancel",
       "2 booking",
       "- Theo GIAO DIỆN MỚI: booking đang chờ approve KHÔNG có nút cancel\n"
       "- Nếu hủy được: chuyển thẳng sang `status` = 4, KHÔNG cần admin approve "
       "(bất kể setting duyệt hủy)\n"
       "- Booking đang request cancel: KHÔNG cho phép rút lại yêu cầu hủy (UI khóa nút)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r466-r467 + spec BR-P14 (ngoại lệ status 0 luôn về 4) "
            "và BR-P15 (backend CÓ năng lực rút lại nhưng UI khóa)."),

    tc("LINE user — hủy booking", "FUNC-DATE-001", "Boundary",
       "Hạn dừng nhận hủy — 4 setting × biên ngày/giờ",
       LU + "\n- U1 có booking đã approve ở slot 10:00 ngày 20/04",
       "Với từng setting, U1 mở detail booking và ghi kết quả:\n"
       "1. Setting không giới hạn (hủy tới khi course start): trước 10:00 ngày 20/04\n"
       "2. Cùng setting: sau 10:00 ngày 20/04\n"
       "3. Setting 日数指定 hủy trước 2 ngày: hiện tại là ngày 17/04 (còn 3 ngày)\n"
       "4. Cùng setting: hiện tại 19/04 (còn 1 ngày)\n"
       "5. Cùng setting, hiện tại đúng 18/04: giờ setting > giờ hiện tại · giờ setting < giờ hiện tại\n"
       "6. Setting 時間指定 hủy trước 3 giờ: còn 5 giờ · còn 2 giờ",
       "6 mốc thời gian",
       "- Trường hợp 1, 3, 5a, 6a: màn detail lịch sử HIỆN nút cancel, bấm vào hiện confirm hủy\n"
       "- Trường hợp 2, 4, 5b, 6b: KHÔNG cho hủy (ẩn nút cancel hoặc báo lỗi)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r456-r463."),

    tc("LINE user — hủy booking", "UI-001", "Normal",
       "Text về hoàn tiền ở màn xác nhận đã hủy — 3 nhánh",
       LU,
       "Với từng nhánh, U1 hủy booking rồi quan sát màn xác nhận đã hủy:\n"
       "1. Course KHÔNG setting số tiền (bill = 0)\n"
       "2. Course CÓ setting bill tiền, booking đã thanh toán (`payment_status` ∈ {1, 3})\n"
       "3. Course CÓ setting bill tiền nhưng booking KHÔNG bị thu tiền (`payment_status` = 2)",
       "3 nhánh",
       "- Nhánh 1: KHÔNG hiện text note nào\n"
       "- Nhánh 2: hiện「お支払い済みのコース料金の返金に関しましては、サービス運営元まで"
       "お問い合わせください。」\n"
       "- Nhánh 3: hiện「コース料金の請求は行われておりませんので、返金はございません。」",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r470-r472."),

    tc("LINE user — hủy booking", "STATE-DEP-001", "Normal",
       "SpecChange #32646: URL cancel LUÔN vào được dù user thỏa filter chặn",
       LU + "\n- U1 đã booking thành công và nhận được action chứa URL cancel\n"
            "- Sau đó admin thêm filter khiến U1 KHÔNG được xem trang booking",
       "Với 4 tổ hợp (thỏa/không thỏa filter × có/không setting top page):\n"
       "1. U1 mở URL CANCEL → quan sát\n"
       "2. Từ màn cancel, bấm sang list history → bấm copy booking → quan sát\n"
       "3. Từ màn cancel, bấm sang page booking → quan sát\n"
       "4. Sau khi cancel xong, mở lại URL cancel → quan sát\n"
       "5. So sánh: U1 mở URL BOOKING (không phải cancel) khi thỏa filter",
       "4 tổ hợp filter × top page",
       "- Bước 1: LUÔN vào được màn cancel của booking tương ứng và hủy được bình thường "
       "(kể cả khi thỏa filter chặn)\n"
       "- Bước 2, 3: khi U1 thỏa filter — bấm copy booking hoặc sang page booking thì hiện "
       "màn KHÔNG CHO PHÉP BOOKING\n"
       "- Bước 4: vẫn mở được màn cancel của booking đó\n"
       "- Bước 5: hiện màn không cho phép booking",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r513-r527 (SpecChange #32646, 10/2025)."),

    # ══════════════════ LINE user — キャンセル待ち ══════════════════
    tc("LINE user — キャンセル待ち", "STATE-DEP-001", "Normal",
       "Đăng ký chờ hủy KHÔNG theo setting duyệt và KHÔNG tính giới hạn",
       LU + "\n- Slot S1 đã full, đã bật 空き枠通知受け取り設定\n"
            "- Calendar đã đạt giới hạn booking của U1",
       "1. Setting booking = 全承認: U1 đăng ký chờ hủy ở S1 → query DB\n"
       "2. Setting booking = リクエスト制: U2 đăng ký chờ hủy → query\n"
       "3. Calendar đã đạt giới hạn max của U1: U1 đăng ký chờ hủy → quan sát",
       "2 chế độ duyệt + đạt giới hạn",
       "- Cả 3: đăng ký thành công NGAY (status = 3), KHÔNG theo setting duyệt booking\n"
       "- Đạt giới hạn max: VẪN đăng ký chờ hủy được",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r434-r435, r437 + spec BR-P12."),

    tc("LINE user — キャンセル待ち", "FUNC-004", "Abnormal",
       "Đăng ký chờ hủy: vẫn chịu ràng buộc thời gian nhận/dừng nhận booking",
       LU + "\n- Slot S1 đã full",
       "1. Khi CHƯA tới giờ mở nhận đặt: U1 thử đăng ký chờ hủy → quan sát\n"
       "2. Khi ĐÃ QUÁ hạn dừng nhận đặt: U1 thử đăng ký → quan sát",
       "2 mốc thời gian",
       "- Cả 2: KHÔNG đăng ký được, báo lỗi chưa tới thời gian / đã hết thời gian booking",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r436."),

    tc("LINE user — キャンセル待ち", "STATE-DEP-001", "Normal",
       "Nhận thông báo có chỗ trống rồi book lại → booking cũ status 3 KHÔNG bị xóa",
       LU + "\n- U1 đã đăng ký chờ hủy ở slot S1",
       "1. Cho slot S1 có chỗ trống → U1 nhận thông báo → U1 vào booking lại slot S1\n"
       "2. Query `SELECT * FROM calendar_course_bookings WHERE reception_id = {S1} "
       "AND status = 3 ORDER BY booking_date DESC`\n"
       "3. Đếm số booking status 3, status 2 (admin book), status 1 (approve) của slot S1",
       "1 user chờ + book lại",
       "- Booking có status = 3 KHÔNG bị xóa đi\n"
       "- Số lượng từng status khớp với thực tế thao tác",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r438. ⚠️ MÂU THUẪN với Setting calendar r1232 nói "
            "「không tạo booking mới mà UPDATE vào booking có status = 3 ban đầu」— nếu update thì "
            "bản ghi status 3 KHÔNG CÒN. Xem MT-58."),

    tc("LINE user — キャンセル待ち", "STATE-DEP-001", "Normal",
       "Hủy booking đợi chờ hủy: luôn cancel ngay, không theo setting duyệt hủy",
       LU + "\n- U1 có booking status = 3 ở slot S1",
       "1. Setting cancel = 全承認: U1 vào history → detail → hủy → query DB\n"
       "2. Setting cancel = リクエスト制: lặp với U2 → query\n"
       "3. Khi ĐÃ QUÁ hạn dừng nhận hủy: lặp với U3 → query",
       "3 kịch bản",
       "- Cả 3: cancel SUCCESS ngay, KHÔNG theo setting duyệt hủy và KHÔNG bị chặn bởi hạn hủy",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r439-r441."),

    tc("LINE user — キャンセル待ち", "MSG-002", "Normal",
       "Action khi đăng ký chờ hủy và khi hủy đăng ký chờ hủy",
       LU + "\n- Calendar có setting action lúc booking, action lúc cancel và action riêng ở tab "
            "「通知受け取り申請時」\n- Course C1 cũng có setting action riêng",
       "1. U1 đăng ký chờ hủy ở slot full → kiểm tin LINE U1\n"
       "2. U1 hủy đăng ký chờ hủy → kiểm tin LINE U1",
       "Đăng ký + hủy đăng ký",
       "- Bước 1: CHỈ gửi action của tab「通知受け取り申請時」(msg text + multi action), "
       "KHÔNG gửi action booking thường và KHÔNG gửi action của course\n"
       "- Bước 2: KHÔNG có thông báo nào",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r442-r444."),

    tc("LINE user — キャンセル待ち", "FUNC-001", "Normal",
       "Feature #35707: LINE user tự xóa booking đợi nhận thông báo",
       LU + "\n- U1 có booking status = 3 ở slot TƯƠNG LAI và 1 booking status = 3 ở slot QUÁ KHỨ",
       "1. Mở màn lịch sử → nhóm 通知受け取り → quan sát booking tương lai\n"
       "2. Bấm「通知受け取りを停止」→ quan sát modal confirm\n3. Bấm icon X → quan sát\n"
       "4. Bấm lại, bấm「停止する」→ query DB\n5. Quan sát booking QUÁ KHỨ",
       "2 booking status 3",
       "- Booking tương lai: hiện nút「通知受け取りを停止」\n"
       "- Modal confirm:「通知受け取りを 停止してよろしいですか？」\n"
       "- Bấm X: đóng modal, booking VẪN còn\n- Bấm 停止する: XÓA HẲN booking đó khỏi DB\n"
       "- Booking quá khứ: hiện ở nhóm 過去の予約 với nhãn「通知受け取り」và KHÔNG có nút xóa",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r87-r98, r158-r168 (Feature #35707, 03/2026). "
            "⚠️ r95 nói booking quá khứ KHÔNG có nút xóa, nhưng r102 lại nói「Check xóa booking "
            "quá khứ → User xóa booking thành công」. Xem MT-59."),

    tc("LINE user — キャンセル待ち", "PERM-003", "Normal",
       "Feature #35707: xóa đúng booking của đúng user và đúng bot",
       "- Admin có 2 bot A và B, mỗi bot có 1 lesson calendar\n"
       "- U1 có booking status = 3 ở CẢ bot A và bot B\n- U2 cũng có booking status = 3 ở bot A",
       "1. U1 mở lịch sử của bot A → xóa booking status 3 → query DB cả 2 bot\n"
       "2. U1 mở lịch sử của bot B → xóa → query\n"
       "3. U2 mở lịch sử của bot A → xóa → query",
       "2 bot × 2 user",
       "- Bước 1: chỉ xóa booking của U1 ở BOT A; booking của U1 ở bot B và của U2 KHÔNG bị đụng\n"
       "- Bước 2: chỉ xóa booking của U1 ở bot B\n- Bước 3: chỉ xóa booking của U2 ở bot A",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r99-r101, r169-r171."),

    tc("LINE user — キャンセル待ち", "DATA-COUNT-001", "Normal",
       "1 user đăng ký chờ hủy 2 lần cùng slot / 2 slot khác nhau",
       LU + "\n- Slot S1 và S2 đều đã full",
       "1. U1 đăng ký chờ hủy ở S1 lần 1, rồi lần 2 → quan sát màn lịch sử + query DB\n"
       "2. U1 đăng ký chờ hủy ở S2 → quan sát",
       "2 slot",
       "- Bước 1: màn lịch sử chỉ hiện ĐÚNG 1 booking cho slot S1 (không nhân đôi)\n"
       "- Bước 2: hiện thêm 1 booking riêng cho slot S2",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r92-r93, r163-r164. ⚠️ TC gốc ghi「1 user được booking "
            "nhiều lần nhưng hiển thị 1 booking」— nhưng Bug KH #36729 (05/2026, MỚI HƠN) khẳng định "
            "lần 2 phải BỊ CHẶN kèm message. Đã lấy theo bản mới. Xem MT-60."),

    tc("LINE user — キャンセル待ち", "DATA-REF-001", "Abnormal",
       "Bug #28801: slot có remain = 0 hoặc < 0 vẫn đăng ký/booking được theo setting",
       LU + "\n- Chuẩn bị: slot P chưa limit; slot Q có remain = 0; slot R có remain < 0 "
            "(số booking approve > 定員, do admin book vượt)",
       "Với từng slot và từng setting (BẬT / TẮT booking khi full slot), cho LINE user và admin "
       "thử đặt và ghi kết quả:\n"
       "1. Slot P: user book · admin book\n"
       "2. Slot Q, BẬT full slot: user book · admin book\n3. Slot Q, TẮT full slot: user · admin\n"
       "4. Slot R, BẬT full slot: user · admin\n5. Slot R, TẮT full slot: user · admin",
       "3 slot × 2 setting × 2 người đặt",
       "- Slot P: cả user và admin đều booking success\n"
       "- Slot Q và R khi BẬT full slot: cả user và admin đều booking success "
       "(KHÔNG hiện lỗi「予約枠がいっぱいです」)\n"
       "- Slot Q và R khi TẮT full slot: user bị DISABLE slot không cho book; admin VẪN book được",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r446-r455 (Bug #28801, 03/2025). "
            "TC gốc CHỈ CÓ TIÊU ĐỀ nhưng tiêu đề đã chứa kết quả — AI chuyển thành expected đo được."),

    # ══════════════════ Đồng thời & verify API ══════════════════
    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "Bug KH #38280: slot còn 1 chỗ, 2 user bấm đăng ký cùng lúc — calendar KHÔNG bill tiền",
       LU + "\n- Calendar KHÔNG setting bill tiền\n"
            "- Chuẩn bị các slot: slot không giới hạn · slot remain = 2 · slot remain = 1",
       "1. Slot không giới hạn: 2 user bấm booking cùng lúc → query DB\n"
       "2. Slot remain = 2: 2 user cùng lúc → query\n"
       "3. Slot remain = 1: chỉ user A đặt → query\n"
       "4. Slot remain = 1: user A và B bấm cùng lúc → query\n"
       "5. Slot remain = 1: 3 user bấm cùng lúc → query\n"
       "6. Slot remain = 1: A bấm trước, B bấm sau (khác giây) → query",
       "6 kịch bản race",
       "- Kịch bản 1, 2: cả 2 booking đều thành công\n- Kịch bản 3: A thành công\n"
       "- Kịch bản 4, 5: CHỈ 1 booking được tạo, các user còn lại nhận thông báo hết chỗ\n"
       "- Kịch bản 6: A thành công, B báo hết chỗ",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r551-r556 (Bug KH #38280, 06/2026 — KHỐI MỚI NHẤT). "
            "RULE-08: race condition test PRODUCTION."),

    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "Bug KH #38280: race condition ở chế độ リクエスト制 và khi bật nhận thông báo full slot",
       LU,
       "1. Calendar setting リクエスト制, slot remain = 1: 2 user bấm cùng lúc → query DB\n"
       "2. Calendar bật nhận thông báo full slot, slot remain = 0: 2 user bấm cùng lúc → query",
       "2 cấu hình",
       "- Kịch bản 1: CẢ 2 booking đều thành công với trạng thái リクエスト "
       "(vì status 0 KHÔNG chiếm chỗ)\n"
       "- Kịch bản 2: CẢ 2 booking đều thành công với trạng thái đợi nhận thông báo",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r557-r558. ⚠️ Spec §6.2 hệ quả 1: ở chế độ リクエスト制 "
            "hệ thống nhận yêu cầu VÔ HẠN và `approveBooking` KHÔNG kiểm sức chứa ⇒ "
            "duyệt hàng loạt sẽ OVERBOOKING. Xem MT-61."),

    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "Bug KH #38280: race condition khi calendar CÓ bill tiền",
       LU + "\n- Calendar ENABLE bill tiền (Stripe hoặc UnivaPay sandbox)",
       "1. Slot không giới hạn: 2 user thanh toán cùng lúc → query DB + dashboard cổng\n"
       "2. Slot remain = 2: 2 user cùng lúc → query\n"
       "3. Slot remain = 1: 2 user cùng lúc → query + đối chiếu 3 nơi "
       "(admin LME · màn user · dashboard cổng)\n"
       "4. Slot remain = 1: 3 user cùng lúc → query\n"
       "5. Slot remain = 1: A trước B sau → query\n"
       "6. Bật nhận thông báo full slot, remain = 0: 2 user cùng lúc → query",
       "6 kịch bản có bill tiền",
       "- Kịch bản 1, 2: cả 2 thành công\n"
       "- Kịch bản 3, 4: CHỈ 1 booking + 1 giao dịch charge thành công; user thua KHÔNG có charge "
       "(hoặc nếu có thì phải được refund tự động), trạng thái khớp ở CẢ 3 NƠI\n"
       "- ⚠️ Tuyệt đối KHÔNG được có case「mất tiền mà không có chỗ」\n"
       "- Kịch bản 5: A thành công, B báo hết chỗ\n- Kịch bản 6: cả 2 vào trạng thái đợi nhận thông báo",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r559-r565, r570 (NEW-07 — TC AI đã có sẵn trong corpus)."),

    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "NEW-02: double click nút đặt lịch tại slot remain = 1",
       LU + "\n- Slot remain = 1, chỉ user A thao tác",
       "1. A bấm nút「予約する」2 lần liên tiếp trong < 300ms\n"
       "2. Query `calendar_course_bookings` đếm booking của slot\n"
       "3. Kiểm số tin xác nhận A nhận được",
       "1 user, 2 click nhanh",
       "- Đúng 1 booking được tạo\n"
       "- KHÔNG tạo 2 bản rồi xóa 1 (kiểm id không bị nhảy 2 đơn vị nếu có thể)\n"
       "- Tin xác nhận KHÔNG gửi 2 lần",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r566 (NEW-02 — TC do AI viết sẵn trong corpus, "
            "giữ nguyên nội dung gốc)."),

    tc("Đồng thời & verify API", "DATA-COUNT-001", "Abnormal",
       "NEW-04: verify 3 tầng sau race — DB + màn hình + output",
       LU + "\n- Slot remain = 1, 2 user A/B bắn đồng thời cùng giây",
       "1. Chạy race\n"
       "2. Query `calendar_course_bookings` đếm bản ghi chiếm chỗ của khung đó\n"
       "3. Query `calendar_course_receptions.total_booking`\n"
       "4. Mở trang booking phía LINE user + màn admin Today&NewBooking",
       "2 user, 1 chỗ",
       "- (a) DB: đúng 1 booking chiếm chỗ\n"
       "- (b) `total_booking` = 1 (đếm lại đúng sau khi xóa bản dư, không bị lệch)\n"
       "- (c) Trang LINE hiện「hết chỗ」\n- (d) Màn admin hiện 1 booking\n"
       "- Cả 4 điểm phải KHỚP nhau",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r567 (NEW-04). RULE-07."),

    tc("Đồng thời & verify API", "DATA-DB-001", "Abnormal",
       "NEW-05: arbiter KHÔNG được xóa nhầm booking của calendar / bot khác",
       "- 2 bot (hoặc 2 calendar / 2 course) khác nhau, mỗi bên có 1 khung cùng ngày cùng giờ, "
       "mỗi bên remain = 1",
       "1. Bắn đồng thời trong cùng 1 giây: user A đặt ở bot 1, user B đặt ở bot 2 "
       "(2 booking HỢP LỆ, khác khung)\n2. Query DB cả 2 bot",
       "2 bot, 2 booking hợp lệ",
       "- CẢ 2 booking đều tồn tại\n"
       "- Arbiter KHÔNG xóa bên nào (điều kiện query phải đủ `bot_id` / `course_id` / `reception_id`)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r568 (NEW-05)."),

    tc("Đồng thời & verify API", "DATA-REF-001", "Abnormal",
       "NEW-06: user THUA cuộc không được nhận bất kỳ side-effect nào",
       LU + "\n- Slot remain = 1; calendar bật: tin xác nhận LINE, remind, sync Google, action gắn tag\n"
            "- 2 user A/B bắn đồng thời",
       "1. Chạy race → B là bản dư bị xóa\n2. Kiểm LINE app của B (iOS + Android)\n"
       "3. Kiểm hộp thư của B\n4. Kiểm remind schedule trong DB/admin\n"
       "5. Kiểm Google Sheet\n6. Kiểm tag / friend info của B",
       "2 user, 1 chỗ",
       "- B KHÔNG nhận tin「đặt lịch thành công」\n- KHÔNG có mail xác nhận\n"
       "- KHÔNG có remind đã lên lịch\n- KHÔNG có bản ghi trên Google Sheet\n"
       "- KHÔNG bị gắn tag / chạy action\n- B CHỈ nhận thông báo hết chỗ",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r569 (NEW-06). ⚠️ TC gốc ghi「event trên Google Calendar」"
            "— nhưng spec §1.2 khẳng định FA-019 KHÔNG có tích hợp Google Calendar ⇒ đã đổi thành "
            "Google Sheet. Xem MT-62."),

    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "NEW-10: ADMIN_BOOK vs user tự đặt cùng giây — arbiter chỉ nhận diện APPROVE",
       LU + "\n- Slot remain = 1",
       "1. Admin đặt hộ khách (tạo booking ADMIN_BOOK, status 2) CÙNG GIÂY với lúc user A tự đặt "
       "(APPROVE, status 1)\n2. Query DB đếm booking chiếm chỗ",
       "1 admin book + 1 user book",
       "- Tổng booking chiếm chỗ = 1 (không vượt giới hạn)\n"
       "- ⚠️ Theo mô tả fix, arbiter chỉ so bản APPROVE khác ⇒ TC này NHIỀU KHẢ NĂNG FAIL. "
       "Nếu fail → escalate: arbiter phải xét cả ADMIN_BOOK",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r571 (NEW-10). DỰ KIẾN FAIL — phải raise bug nếu tái hiện. "
            "Khớp spec RA-02 (job monitor bỏ qua booking status = 2)."),

    tc("Đồng thời & verify API", "REG-SHARED-001", "Abnormal",
       "NEW-12: regression Booking Event có dính cùng pattern check-then-act không",
       "- Booking Event có giới hạn số chỗ, còn ĐÚNG 1 chỗ\n- 2 user A/B",
       "1. Bắn 2 request đặt event đồng thời cùng giây\n2. Query DB",
       "2 user, 1 chỗ event",
       "- Chỉ 1 booking được tạo\n"
       "- ⚠️ Nếu CẢ 2 thành công → Booking Event cũng dính bug gốc, chưa được fix → TẠO TICKET RIÊNG",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r572 (NEW-12). TC hồi quy sang FA-021 イベント予約."),

    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "NEW-13: hủy + đặt mới đồng thời tại slot đầy (REQUEST_CANCEL vẫn chiếm chỗ)",
       LU + "\n- Slot đã đầy (remain = 0), có 1 booking của user A",
       "1. A bấm hủy ĐÚNG LÚC user B bấm đặt (đồng thời, cùng giây)\n"
       "2. Query DB đếm booking chiếm chỗ (status 1, 2, 5)",
       "1 hủy + 1 đặt đồng thời",
       "- KHÔNG over-book: hoặc B bị báo hết chỗ (nếu hủy chưa hoàn tất), hoặc B đặt được "
       "sau khi A hủy xong — KHÔNG BAO GIỜ ra 2 booking chiếm chỗ\n"
       "- `total_booking` khớp số thật",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r573 (NEW-13)."),

    tc("Đồng thời & verify API", "REG-SHARED-001", "Normal",
       "RV-05: regression đặt TUẦN TỰ khác giây — arbiter không xóa nhầm",
       LU + "\n- Lesson calendar limit = 1",
       "1. User A đặt rồi HỦY (giải phóng chỗ)\n"
       "2. User B đặt sau đó (KHÁC GIÂY) khi còn chỗ\n3. Query DB",
       "Đặt tuần tự",
       "- Booking của B được GIỮ bình thường, arbiter KHÔNG xóa "
       "(`created_at` khác giây với mọi bản còn lại)\n- Không hồi quy luồng đặt tuần tự",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r574 (RV-05)."),

    tc("Đồng thời & verify API", "DATA-COUNT-001", "Abnormal",
       "RV-11: REQUEST_CANCEL (status 5) VẪN tính chiếm chỗ khi khử trùng",
       LU + "\n- Khung limit = 2, đã có 1 booking APPROVE + 1 booking đang REQUEST_CANCEL",
       "1. Người mới đặt đồng thời (cùng giây tạo bản mới)\n2. Query DB",
       "2 chỗ đã bị chiếm",
       "- Người mới BỊ CHẶN vì 2 chỗ đã bị chiếm (APPROVE + REQUEST_CANCEL đều tính, "
       "theo status 1, 2, 5)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r575 (RV-11 — đối chiếu AI TC-05)."),

    tc("Đồng thời & verify API", "DATA-COUNT-001", "Normal",
       "RV-12: đối chứng âm — status đã hủy / từ chối / chờ duyệt KHÔNG tính giới hạn",
       LU + "\n- Khung limit = 1, có 1 booking ở trạng thái đã hủy / từ chối / chờ duyệt "
            "(không thuộc status 1, 2, 5)",
       "1. Người mới đặt\n2. Query DB",
       "1 booking không chiếm chỗ",
       "- Người mới đặt THÀNH CÔNG (chỉ đếm status chiếm chỗ 1, 2, 5; các status khác không chặn)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r576 (RV-12 — đối chứng âm chống chặn nhầm)."),

    tc("Đồng thời & verify API", "PAY-AMOUNT-001", "Abnormal",
       "🔴 Verify API: client gửi checkHasPayment = false để bỏ qua thanh toán",
       LU + "\n- Calendar ENABLE bill tiền, course Cp giá 10.000 yên",
       "1. Dùng công cụ chặn/sửa request (proxy hoặc devtools) khi U1 bấm đặt lịch\n"
       "2. Sửa `checkHasPayment` thành `false` → gửi request\n"
       "3. Query `calendar_course_bookings` và kiểm dashboard cổng thanh toán\n"
       "4. Thử tiếp: sửa `amount` thành 1 → gửi\n"
       "5. Thử tiếp: sửa `approve_type` → gửi",
       "3 tham số bị sửa từ client",
       "- Server PHẢI đối chiếu lại với `calendar_management.is_use_payment`, "
       "`calendar_course.amount` và kết quả thật từ cổng thanh toán\n"
       "- Booking KHÔNG được tạo với「予約確定」+ `payment_status` = 2 khi thực tế phải thu tiền\n"
       "- KHÔNG được thu 1 yên cho khóa học 10.000 yên\n"
       "- ⚠️ Theo spec RP-01 / S-04: cả 3 tham số hiện do CLIENT gửi và server KHÔNG đối chiếu "
       "⇒ TC này DỰ KIẾN FAIL, phải raise bug ngay",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 TOP-1 (RP-01 / S-04, mức Nghiêm trọng). "
            "Corpus KHÔNG có TC nào. DỰ KIẾN FAIL. Xem MT-63."),

    tc("Đồng thời & verify API", "SEC-001", "Abnormal",
       "🔴 Verify API: IDOR đọc thông tin booking của bot khác (EP-P16)",
       LU + "\n- Bot A có booking id = 100 của U1; bot B (bot KHÁC) có booking id = 101",
       "1. Từ phiên LIFF của bot A, gọi API lấy chi tiết booking với `booking_id` = 101\n"
       "2. Quan sát response\n3. Thử duyệt tuần tự nhiều booking_id",
       "booking_id của bot khác",
       "- Server PHẢI kiểm `booking.calendar_id` == `calendar_id` truyền vào VÀ kiểm chủ sở hữu\n"
       "- KHÔNG được trả về `friend_info` (họ tên, email, SĐT, đáp án form), `last4`, "
       "`payment_card_expired`, `charge_id`, số tiền của booking thuộc bot khác\n"
       "- ⚠️ Theo spec S-01: hiện KHÔNG kiểm gì ⇒ TC này DỰ KIẾN FAIL, rò rỉ PII XUYÊN BOT",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.2 S-01. Corpus KHÔNG có TC. DỰ KIẾN FAIL. Xem MT-63."),

    tc("Đồng thời & verify API", "SEC-001", "Abnormal",
       "🔴 Verify API admin: id con (receptionId / bookingId / courseId) không được kiểm",
       "- Admin có bot A (calendar id = 1) và KHÔNG có quyền với bot B (calendar id = 2)\n"
       "- Bot B có reception id = 500, booking id = 600, course id = 700",
       "1. Gọi endpoint sửa/xóa khung giờ với `{id}` = 1 (calendar hợp lệ của mình) "
       "nhưng `receptionId` = 500 (của bot B)\n"
       "2. Tương tự với `bookingId` = 600 (đổi trạng thái booking) và `courseId` = 700 (xuất CSV)\n"
       "3. Query DB của bot B sau mỗi lần",
       "id con thuộc bot khác",
       "- Server PHẢI đối chiếu id con với calendar `{id}` và từ chối\n"
       "- Dữ liệu của bot B KHÔNG được đọc / sửa / xóa\n"
       "- ⚠️ Theo spec A-06: middleware CHỈ kiểm `{id}` cấp calendar ⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 TOP-4 (A-06), ảnh hưởng EP-36/38/42/43/44/46/47/50/63. "
            "Corpus chỉ có TC security ở tầng URL calendar (Quản lý calendar r3, Quản lý course r180). "
            "DỰ KIẾN FAIL. Xem MT-63."),

    tc("Đồng thời & verify API", "PERM-002", "Abnormal",
       "🔴 Verify API: nhóm route /ajax/calendar/* thiếu kiểm quyền staff và CSRF",
       "- Bot A có staff S1 KHÔNG được cấp quyền route `calendar.index`\n"
       "- Bot A có 1 lesson calendar",
       "1. Đăng nhập bằng staff S1\n"
       "2. Gọi trực tiếp endpoint xóa hệ thống đặt lịch trong nhóm `/ajax/calendar/*`\n"
       "3. Gọi endpoint sửa 利用規約 và 店舗情報 trong cùng nhóm\n"
       "4. Gọi endpoint cấu hình remind\n5. Query DB sau mỗi lần\n"
       "6. Với bot đã HẾT HẠN hợp đồng: lặp bước 2-4",
       "Staff không quyền + bot hết hạn",
       "- TẤT CẢ các lời gọi PHẢI bị từ chối (staff không quyền và bot hết hạn đều không thao tác được)\n"
       "- DB KHÔNG bị thay đổi\n"
       "- ⚠️ Theo spec A-01: nhóm route này thiếu `basic_access`, thiếu `is_expire` và miễn CSRF "
       "⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 TOP-2 (A-01, 17 endpoint). Corpus KHÔNG có TC. "
            "DỰ KIẾN FAIL. Xem MT-63."),

    tc("Đồng thời & verify API", "SEC-001", "Abnormal",
       "🔴 Verify API: POST /{id}/edit là mass assignment lên calendar_management",
       "- Admin có bot A (calendar id = 1); bot B có calendar id = 2 (không thuộc quyền admin)",
       "1. Gọi `POST /basic/calendar-management/2/edit` với body chứa các trường ngoài 管理名: "
       "`bot_id`, `is_use_payment`, `environment`, `google_sheet_access_token`, `code_delete`\n"
       "2. Query bản ghi `calendar_management` id = 2",
       "Body chứa trường nhạy cảm",
       "- Server PHẢI chỉ nhận trường 管理名 và PHẢI kiểm calendar thuộc bot của mình\n"
       "- Bản ghi calendar id = 2 KHÔNG bị thay đổi bất kỳ trường nào\n"
       "- ⚠️ Theo spec A-02: endpoint nằm NGOÀI middleware kiểm bot và dùng `$request->all()` "
       "⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 TOP-3 (A-02). Corpus chỉ test đổi 管理名 ở mức UI "
            "(Calendar list r52, r58). DỰ KIẾN FAIL. Xem MT-63."),

    tc("Đồng thời & verify API", "DATA-REF-001", "Abnormal",
       "🔴 Verify API: xóa course KHÔNG được kiểm lại ở server",
       LU + "\n- Course C1 còn booking TƯƠNG LAI ở status 予約確定",
       "1. Ở UI, bấm xóa C1 → bị chặn (đúng)\n"
       "2. Gọi TRỰC TIẾP endpoint xóa course (bỏ qua UI) với `courseId` = C1\n"
       "3. Query `calendar_course` và các booking của C1",
       "Course còn booking tương lai",
       "- Server PHẢI kiểm lại điều kiện và TỪ CHỐI xóa\n"
       "- Course C1 và booking của nó KHÔNG bị xóa\n"
       "- ⚠️ Theo spec BR-30: rule này CHỈ kiểm ở FRONT-END, server KHÔNG kiểm lại "
       "⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec BR-30. Corpus chỉ test nhánh UI (Quản lý course r77-r82). "
            "DỰ KIẾN FAIL. Xem MT-63."),

    # ══════════════════ App mobile ══════════════════
    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile admin: xem và thao tác booking lesson",
       LU + "\n- App mobile admin đã đăng nhập bot A",
       "1. Mở app → vào màn calendar lesson → quan sát list booking\n"
       "2. Mở detail 1 booking đang リクエスト → approve → kiểm trên WEB\n"
       "3. Booking khác → deny → kiểm\n4. Booking đã approve → cancel → kiểm\n"
       "5. Booking đã thanh toán → refund → kiểm\n6. Thêm booking mới từ app → kiểm trên WEB",
       "6 thao tác",
       "- Mọi thao tác trên app phải phản ánh ĐÚNG và NGAY trên màn WEB (và ngược lại)\n"
       "- Trạng thái, bộ đếm slot, lịch sử booking khớp giữa 2 kênh",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Sửa bill tiền univapay r49-r58, r108-r116 + Setting calendar r1034, r1039, "
            "r1043, r1047. TC tổng hợp do AI viết — corpus chỉ có TC app mobile rải rác theo ticket. "
            "Cần Leader xác nhận."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile: notify cho admin khi có booking mới / thao tác của user",
       LU + "\n- App mobile admin đã bật notify",
       "1. LINE user booking mới → kiểm notify trên app\n"
       "2. Mở notify → vào detail booking → quan sát\n"
       "3. LINE user request cancel → kiểm notify\n"
       "4. LINE user đăng ký chờ hủy → kiểm notify\n5. Admin refund 1 booking → kiểm notify",
       "5 sự kiện",
       "- Sự kiện 1, 3: admin NHẬN được notify\n"
       "- Sự kiện 4 (đăng ký キャンセル待ち) và 5 (hoàn tiền): admin KHÔNG nhận notify\n"
       "- Bấm notify: mở đúng detail booking tương ứng",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-P33 (「Admin KHÔNG nhận mobile_notify cho 2 sự kiện: "
            "đăng ký キャンセル待ち và hoàn tiền」) — corpus lesson chỉ có TC mở detail từ màn notify. "
            "Cần Leader xác nhận."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "Sửa sort lịch sử booking theo time mới nhất lên đầu (lesson + app)",
       LU + "\n- Booking B1 có nhiều dòng lịch sử: user book → admin approve → user request cancel",
       "1. Mở tab 予約履歴 trên WEB → quan sát thứ tự\n"
       "2. Mở lịch sử booking đó trên APP MOBILE → quan sát\n"
       "3. Lặp với booking do admin book và booking do user book",
       "3 nguồn booking × 2 kênh",
       "- Cả WEB và APP: lịch sử sort theo thời gian MỚI NHẤT lên đầu",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r1053-r1056."),

    # ══════════════════ Add link booking vào tin nhắn ══════════════════
    tc("Add link booking vào tin nhắn", "LIFF-ENTRY-001", "Normal",
       "Support #26549: chèn link booking / link lịch sử của calendar lesson vào template text",
       LU + "\n- Bot A có 3 lesson calendar: L1 và L2 đang ON, L3 đang OFF",
       "1. Vào màn template → tạo template text → bấm chèn link lesson → quan sát list calendar\n"
       "2. Chọn L1 → chọn「link booking」→ quan sát nội dung được chèn\n"
       "3. Chọn L1 → chọn「link lịch sử」→ quan sát",
       "3 calendar, 1 OFF",
       "- List hiện đúng calendar của bot A và CHỈ hiện L1, L2 (calendar OFF KHÔNG hiện)\n"
       "- Chọn link booking: chèn đúng URL booking của L1\n"
       "- Chọn link lịch sử: chèn đúng URL lịch sử của L1",
       env="PRODUCTION",
       note="Nguồn: add link salon và lesson r43-r45 (Support #26549, 08/2024)."),

    tc("Add link booking vào tin nhắn", "LIFF-ENTRY-001", "Normal",
       "Support #26549: chèn link lesson ở 6 loại template và 5 màn khác",
       LU + "\n- Bot A có lesson calendar L1 đang ON",
       "Chèn link booking lesson tại các vị trí sau, mỗi vị trí kiểm chèn được và list calendar đúng:\n"
       "1. Template text\n2. Template button — btn standard · btn set màu · btn ảnh\n"
       "3. Quick reply — chèn vào message text và chèn vào button\n4. Template image map\n"
       "5. Màn send all (broadcast)\n6. Màn step message (scenario)\n7. Màn remind\n8. Màn rich menu",
       "8 vị trí chèn",
       "- Tất cả vị trí: chèn được link booking/lịch sử của lesson calendar\n"
       "- List calendar luôn chỉ hiện calendar ON của bot",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: add link salon và lesson r46-r55 — TC gốc CHỈ CÓ TIÊU ĐỀ, "
            "kết quả mong đợi do AI bổ sung theo mẫu r43-r45. Cần Leader xác nhận."),

    tc("Add link booking vào tin nhắn", "LIFF-ENTRY-001", "Normal",
       "Support #26549: LINE user mở link lesson từ action open url — gửi bởi WEB và bởi JOB",
       LU + "\n- Đã tạo template chứa link booking lesson ở nhiều dạng",
       "Với CẢ 2 nguồn gửi (gửi từ WEB — kể cả send test — và gửi bởi JOB), kiểm U1 mở được link tại:\n"
       "1. URL trong template text\n2. Button standard — chỉ set action mở url · set url + multi action\n"
       "3. Button set màu — 2 nhánh như trên\n4. Button ảnh — 2 nhánh\n"
       "5. Quick reply — mở từ msg text · từ button (2 nhánh)\n"
       "6. Image map — chỉ mở url · mở url + multi action\n7. Rich menu — 2 nhánh",
       "2 nguồn gửi × 7 vị trí",
       "- Mọi tổ hợp: U1 bấm vào mở ĐÚNG màn booking / lịch sử của lesson calendar\n"
       "- Với nhánh có multi action: các action kèm theo cũng chạy đúng",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: add link salon và lesson r56-r81 — TC gốc CHỈ CÓ TIÊU ĐỀ (26 dòng), "
            "kết quả mong đợi do AI bổ sung. Cần Leader xác nhận."),

    tc("Add link booking vào tin nhắn", "DATA-BACKUP-001", "Normal",
       "Support #26549: backup rich menu có chứa link lesson",
       LU + "\n- Bot A có rich menu chứa action mở link booking lesson",
       "1. Backup rich menu của bot A sang bot B\n2. Ở bot B, add rich menu cho user\n"
       "3. U1 (friend của bot B) bấm vào vùng có action mở link lesson",
       "Rich menu có link lesson",
       "- Backup được rich menu\n- Rich menu hiển thị bình thường ở bot B\n"
       "- Bấm vào: action mở url chạy bình thường\n"
       "- ⚠️ Cần chốt: link trỏ tới calendar của BOT GỐC hay bot đích",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: add link salon và lesson r82. ⚠️ Rủi ro rò rỉ dữ liệu chéo bot nếu link vẫn "
            "trỏ id calendar của bot gốc (giống lỗi MT-16 của FA-033 Backup). Xem MT-64."),

    # ══════════════════ Phân quyền & môi trường ══════════════════
    tc("Phân quyền & môi trường", "SEC-001", "Abnormal",
       "Test security: từ bot B paste URL màn quản lý calendar của bot A",
       "- Admin có 2 bot A và B\n- Bot A có lesson calendar id = 1",
       "1. Đăng nhập admin, đang chọn bot B\n"
       "2. Paste URL https://step.lme.jp/basic/calendar-management/1 → quan sát",
       "URL calendar của bot A",
       "- Redirect ra màn hình LIST calendar của bot B\n"
       "- KHÔNG hiển thị dữ liệu calendar của bot A",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar r3."),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Account staff: các màn của レッスン予約 hiển thị và thao tác được",
       LU + "\n- Có staff S1 được cấp quyền route レッスン予約",
       "Đăng nhập staff S1 và kiểm tại các màn:\n"
       "1. Màn list calendar · màn quản lý theo ngày/tuần/tháng/list\n"
       "2. Màn detail course (tab 基本情報 và tab アクション)\n"
       "3. Màn 全体設定 (các menu con: filter, remind, notify, google)\n"
       "4. Thao tác approve/deny/cancel/refund booking\n5. Kiểm lịch sử booking ghi tên staff",
       "Account staff",
       "- Staff thấy đầy đủ dữ liệu như admin chính, không bị trắng data\n"
       "- Thao tác thành công; lịch sử booking ghi người thao tác là「スタッフA」\n"
       "- ⚠️ Cần chốt DANH SÁCH route con mà staff được cấp",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: nhiều dòng「Check account staff」rải rác (Calendar list r63, Quản lý calendar r62, "
            "Quản lý course r73/r139, Setting calendar r256/r1537, Sửa bill tiền univapay r165) — "
            "TẤT CẢ đều CHỈ CÓ TIÊU ĐỀ. Spec Gap G-01 chưa xác minh được dữ liệu phân quyền. "
            "Xem MT-43."),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "🔴 Staff bị cấm route レッスン予約 vẫn thao tác được qua nhóm /ajax/calendar/*",
       "- Bot A có staff S2 KHÔNG được cấp quyền route レッスン予約",
       "1. Đăng nhập staff S2 → mở sidebar → kiểm menu レッスン予約 có hiện không\n"
       "2. Paste trực tiếp URL /basic/calendar-management → quan sát\n"
       "3. Gọi TRỰC TIẾP các endpoint trong nhóm `/ajax/calendar/*` (sửa 利用規約, sửa 店舗情報, "
       "cấu hình remind, xóa hệ thống đặt lịch)\n4. Query DB sau mỗi lần",
       "Staff không quyền",
       "- Bước 1, 2: menu bị ẩn và URL bị chặn\n"
       "- Bước 3: TẤT CẢ endpoint đều PHẢI bị từ chối ở TẦNG SERVER\n"
       "- DB KHÔNG bị thay đổi\n"
       "- ⚠️ Theo spec A-01: nhóm route này chỉ được che bởi `check_login` (không có nhánh else) "
       "⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 TOP-2 (A-01). Đây là kiểu bug「UI ẩn menu nhưng API "
            "không enforce quyền」— phải rà ở TẦNG API, không chỉ UI. Xem MT-63."),

    tc("Phân quyền & môi trường", "ENV-003", "Normal",
       "Bot hết hạn hợp đồng → chặn truy cập trang booking phía LINE user",
       LU + "\n- Bot A đã HẾT HẠN hợp đồng",
       "1. U1 mở URL booking của calendar thuộc bot A → quan sát mã trạng thái HTTP và màn hình\n"
       "2. U1 mở URL lịch sử → quan sát",
       "Bot hết hạn",
       "- Trả về HTTP 410 (hoặc màn báo lỗi rõ ràng), không cho booking\n"
       "- KHÔNG lỗi 500, không trắng trang",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-P01 (6 điều kiện chặn, gồm「bot chưa hết hạn (410)」) — "
            "corpus KHÔNG có TC. Cần Leader xác nhận."),

    tc("Phân quyền & môi trường", "OUT-PREVIEW-001", "Normal",
       "uCode = 'preview': bỏ qua filter bạn bè và bỏ qua giới hạn số lần đặt",
       LU + "\n- Calendar có filter chặn U1 và setting giới hạn 1 booking/user; U1 đã đạt giới hạn",
       "1. Admin bấm nút「予約カレンダーを見る」ở header để mở preview\n"
       "2. Quan sát các màn: TOP · TOP detail · điều khoản · history (list và tháng) · chọn course · "
       "chọn slot (list và tháng) · nhập friend info\n"
       "3. Thử bấm nút next ở màn nhập friend info",
       "Preview của admin",
       "- Bỏ qua TOÀN BỘ filter bạn bè và bỏ qua giới hạn số lần đặt\n"
       "- Màn history: hiển thị TRỐNG\n"
       "- Màn chọn course: CHỈ hiện course đang ON, hiển thị giống bên user\n"
       "- Màn nhập friend info: hiện đủ friend info tương ứng nhưng nút NEXT bị DISABLE "
       "(không qua được màn bill tiền)",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r503-r512 + spec BR-P02."),

    tc("Phân quyền & môi trường", "UI-002", "Normal",
       "Màn booking phía LINE user: mở trong app LINE và mở bằng trình duyệt ngoài",
       LU,
       "1. U1 mở link booking TRONG app LINE (iOS và Android) → booking hoàn chỉnh\n"
       "2. U1 mở link booking bằng trình duyệt NGOÀI app LINE → booking hoàn chỉnh\n"
       "3. Lặp với màn lịch sử booking",
       "2 môi trường × 2 OS",
       "- Cả 2 môi trường: hiển thị đúng, booking hoàn chỉnh, nhận được action sau khi đặt\n"
       "- Màn lịch sử: thứ tự 3 nhóm giống nhau ở cả 2 môi trường",
       env="PRODUCTION",
       note="Nguồn: Booking phía line user r33-r40, r105-r106, r175-r176, r543-r545."),

    tc("Phân quyền & môi trường", "REG-SHARED-001", "Normal",
       "Hồi quy: thao tác trên lesson KHÔNG ảnh hưởng salon và event booking",
       LU + "\n- Bot A có đồng thời: 1 lesson calendar, 1 salon calendar, 1 event booking",
       "1. Tạo / sửa / xóa slot, course, booking ở LESSON\n"
       "2. Kiểm dữ liệu của SALON calendar (`calendar_salon*`) không đổi\n"
       "3. Kiểm dữ liệu của EVENT booking (`booking_event*`) không đổi\n"
       "4. Xóa lesson calendar → kiểm lại 2 tính năng kia",
       "3 tính năng đặt lịch",
       "- Mọi thao tác trên lesson KHÔNG làm thay đổi dữ liệu của salon và event\n"
       "- Xóa lesson calendar: salon và event vẫn hoạt động bình thường",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec §1.2 (3 hệ thống đặt chỗ dùng bảng RIÊNG) và §12.2 "
            "(FA-019 có phụ thuộc THẬT vào FA-020 — dùng chung "
            "`calendar_salon_setting_send_messages.text_limit_book_each_customer`). "
            "Corpus KHÔNG có TC hồi quy chéo. Cần Leader xác nhận. Xem MT-65."),
]
