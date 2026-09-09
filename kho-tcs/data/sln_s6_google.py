# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 39-40: Googleカレンダー連携 và Googleスプレッドシート連携.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Sync google calendar」(09/2024 → 07/2026, 440 TC lá — Bug #26653 2 salon chung 1 calendar,
    Bug #26739 event qua ngày, Bug #28770/#29169 xóa event, Bug #29844 SyncToken lỗi,
    Bug #30419 blocktime rác, Bug KH #35312 job retry, Support #35768 hủy liên kết,
    Bug tự detect #38446 performance)
  - tab「Setting calendar」r1533-r1661 (Googleスプレッドシート連携 + Support #32733 cảnh báo mất liên kết)
"""
from _common import tc

GG = ("- Đăng nhập admin (主管理者) bot A\n"
      "- Calendar「サロンA」loại スタッフ, staff S1 và S2\n"
      "- Có sẵn 2 tài khoản Google test (A và B) có quyền tạo/sửa Calendar và Spreadsheet\n"
      "- Mở /basic/calendar-salon/{id} → tab「予約設定」→「Googleカレンダー連携」")

S6 = [
    # ══════════════ 39. Googleカレンダー連携 ══════════════
    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Liên kết Google Calendar mới → sync booking hiện có lên Google theo trạng thái",
       GG + "\n- S1 chưa liên kết Google\n"
            "- S1 đã có booking ở đủ các trạng thái: approve (1), admin book (2), deny (6), "
            "đợi approve (0), request cancel (5), đã cancel (4/7), và booking khách ngoài hệ thống",
       "1. Liên kết Google Calendar cho S1\n2. Mở Google Calendar của tài khoản đã liên kết\n"
       "3. Đối chiếu từng booking\n4. Với booking qua ngày → kiểm tra ngày giờ start-end của event",
       "Booking đủ 7 trạng thái, có cả booking qua ngày",
       "- Tạo event cho booking status 1, 2, 5 (kể cả booking khách ngoài hệ thống)\n"
       "- KHÔNG tạo event cho status 0, 4, 6, 7\n"
       "- Booking qua ngày: tạo event loại qua ngày, ngày giờ start-end đúng",
       note="Nguồn: Sync google calendar r3-r11. Spec BR-09, EP-47/EP-48."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Nội dung event sync lên Google Calendar",
       GG + "\n- S1 đã liên kết Google; có booking của khách trong hệ thống và khách ngoài hệ thống",
       "1. Mở event trên Google Calendar\n2. Đối chiếu tiêu đề, ngày giờ, course, staff, tên LINE\n"
       "3. Với booking admin book KHÔNG chọn course → kiểm tra\n"
       "4. Với booking chọn 指定なし → kiểm tra\n5. Với calendar loại 個人 → kiểm tra",
       "Booking đầy đủ và booking thiếu course/staff",
       "- Tiêu đề:「<system name>様 <tên quản lý course>」\n"
       "- Ngày giờ:「予約日時 2024年08月08日 23:30~03:30」(ngày start + giờ start ~ giờ end)\n"
       "- コース: tên quản lý course; không chọn course →「指定なし」\n"
       "- 予約枠: tên quản lý staff; 指定なし →「指定なし」; calendar 個人 →「運営者」\n"
       "- Khách trong hệ thống: hiện line name + link my_page; khách ngoài: KHÔNG hiện phần này",
       note="Nguồn: Sync google calendar r12-r21."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Sync khi có booking MỚI — theo trạng thái và theo lối tạo",
       GG + "\n- S1 đã liên kết Google Calendar",
       "1. LINE user đặt lịch được duyệt ngay → kiểm tra Google\n"
       "2. LINE user đặt lịch chờ duyệt → kiểm tra Google\n"
       "3. Admin duyệt booking đó → kiểm tra\n4. Admin từ chối booking → kiểm tra\n"
       "5. Admin duyệt HÀNG LOẠT nhiều booking → kiểm tra\n"
       "6. Admin từ chối hàng loạt → kiểm tra\n"
       "7. Admin đặt lịch chọn khách trong tool và khách ngoài tool → kiểm tra",
       "7 kịch bản tạo booking",
       "- B1, B3, B5, B7: TẠO event trên Google với đủ thông tin (ngày giờ, course, staff, "
       "friend info, line name + link my_page)\n"
       "- B2, B4, B6: KHÔNG tạo event",
       note="Nguồn: Sync google calendar r33-r40."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Sync khi HỦY booking — theo trạng thái và theo lối hủy",
       GG + "\n- S1 đã liên kết Google; có booking đã sync lên Google",
       "1. LINE user hủy được duyệt ngay → kiểm tra Google\n"
       "2. LINE user gửi yêu cầu hủy (chờ duyệt) → kiểm tra\n"
       "3. Admin duyệt yêu cầu hủy → kiểm tra\n4. Admin từ chối yêu cầu hủy → kiểm tra\n"
       "5. Admin duyệt hàng loạt yêu cầu hủy → kiểm tra\n6. Admin từ chối hàng loạt → kiểm tra\n"
       "7. Admin hủy trực tiếp → kiểm tra\n8. Admin XÓA booking đã hủy → kiểm tra",
       "8 kịch bản hủy",
       "- B1, B3, B5, B7: XÓA event trên Google\n"
       "- B2, B4, B6: KHÔNG xóa event\n"
       "- B8: lúc hủy đã xóa event rồi nên khi xóa booking KHÔNG sync thêm",
       note="Nguồn: Sync google calendar r46-r58."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Boundary",
       "Bug #26739: event QUA NGÀY từ Google được tách thành 2 block time",
       GG + "\n- S1 chưa liên kết Google\n- Trên Google Calendar đã có event qua ngày (vd 22:00 ngày 1 → 02:00 ngày 2)",
       "1. Liên kết Google Calendar cho S1\n"
       "2. Kiểm tra bảng `calendar_salon_booking_by_google`\n"
       "3. Kiểm tra lưới QL ngày của ngày 1 và ngày 2\n4. Kiểm tra slot phía LINE user 2 ngày đó",
       "Event Google qua ngày",
       "- Tạo 2 bản ghi block time: bản 1 từ 22:00 đến 23:59 ngày 1; bản 2 từ 00:00 đến 02:00 ngày 2\n"
       "- Lưới admin và LINE user đều chặn đúng 2 khoảng",
       note="Nguồn: Sync google calendar r61, r321-r344 (Bug #26739, 23/09/2024)."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Xóa event trên Google (đơn lẻ và loại lặp) → xóa block time tương ứng",
       GG + "\n- S1 đã liên kết Google; đã sync về block time từ event thường và event lặp (repeat)",
       "1. Xóa 1 event thường trên Google → chờ sync → kiểm tra bảng và lưới\n"
       "2. Xóa 1 event trong chuỗi lặp → kiểm tra\n3. Xóa nhiều event trong chuỗi lặp → kiểm tra\n"
       "4. Xóa toàn bộ chuỗi lặp → kiểm tra",
       "Event thường + event lặp",
       "- Mọi trường hợp: block time tương ứng bị xóa khỏi `calendar_salon_booking_by_google`\n"
       "- Lưới admin và slot phía LINE user mở lại đúng các khung tương ứng",
       note="Nguồn: Sync google calendar r77-r80."),

    tc("Googleカレンダー連携", "STATE-CLEAN-001", "Normal",
       "Hủy liên kết Google của staff → xóa cả 2 chiều dữ liệu sync",
       GG + "\n- S1 đã liên kết Google, có event sync 2 chiều",
       "1. Bấm hủy liên kết Google của S1\n"
       "2. Kiểm tra Google Calendar (các event do LME đẩy lên)\n"
       "3. Kiểm tra bảng `calendar_salon_booking_by_google`\n"
       "4. Kiểm tra bảng `b_c_salon_google_calendar`\n5. Kiểm tra lưới admin",
       "S1 có event 2 chiều",
       "- Xóa các event do LME đã sync lên Google của S1\n"
       "- Xóa các block time đã sync từ Google về\n- Xóa bản ghi liên kết của S1\n"
       "- Lưới admin không còn block time của S1",
       note="Nguồn: Sync google calendar r31-r32, r85-r111. Spec BR-09."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Nhiều staff liên kết cùng 1 tài khoản Google / khác tài khoản",
       GG + "\n- Tài khoản Google A có 2 calendar X và Y",
       "1. S1 chọn calendar X, S2 KHÔNG chọn calendar nào → kiểm tra sync\n"
       "2. S1 chọn X, S2 chọn Y → kiểm tra sync của từng staff\n"
       "3. S1 liên kết tài khoản A, S2 liên kết tài khoản B → kiểm tra sync",
       "2 tài khoản Google, 2 calendar",
       "- Staff không chọn calendar: KHÔNG liên kết, không sync\n"
       "- Mỗi staff sync đúng dữ liệu của calendar mình chọn\n"
       "- Khác tài khoản: mỗi staff sync lên calendar của tài khoản tương ứng",
       note="Nguồn: Sync google calendar r81-r84."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Abnormal",
       "Bug #26653: 2 staff liên kết CHUNG 1 Google Calendar",
       GG + "\n- Tài khoản Google A có calendar X",
       "1. S1 liên kết calendar X → sau đó S2 cũng liên kết calendar X\n"
       "2. Tạo booking cho S1 → kiểm tra event trên calendar X\n"
       "3. Tạo booking cho S2 → kiểm tra\n4. Tạo event trực tiếp trên calendar X → kiểm tra block time\n"
       "5. Hủy liên kết của S1 → kiểm tra dữ liệu của S2",
       "2 staff cùng calendar X",
       "- Cả 2 staff sync được lên calendar X, event không đè lên nhau\n"
       "- Event từ Google sync về tạo block time cho CẢ 2 staff (hoặc theo rule đã chốt)\n"
       "- Hủy liên kết S1: dữ liệu sync của S2 KHÔNG bị mất",
       spec="Đã hỏi leader",
       note="Nguồn: Sync google calendar r280-r320 (Bug #26653, 11/09/2024). "
            "⚠ Corpus không ghi rõ block time chung tạo cho 1 hay 2 staff → cần Leader chốt, xem MT-34."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Abnormal",
       "Bug #29844: SyncToken lỗi (410 Gone) → fallback đồng bộ theo khoảng thời gian",
       GG + "\n- S1 đã liên kết Google\n- Chuẩn bị được trạng thái `sync_token_google_calendar` lỗi",
       "1. Làm hỏng SyncToken (hoặc chờ Google trả 410)\n"
       "2. Tạo / sửa / xóa event trên Google\n3. Chờ job xử lý → kiểm tra block time trên LME\n"
       "4. Kiểm tra lịch sử sync\n5. Lặp lại với SyncToken bình thường",
       "SyncToken lỗi và bình thường",
       "- Khi token lỗi: job fallback sang đồng bộ theo khoảng thời gian, dữ liệu vẫn đúng\n"
       "- Khi token bình thường: đồng bộ theo token, dữ liệu đúng\n"
       "- Không sinh block time rác hoặc mất block time",
       note="Nguồn: Sync google calendar r431-r447 (Bug #29844, 13/05/2025). Spec §7.1.1."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Abnormal",
       "Bug #28770 / #29169 / #30419: xóa event trên Google nhưng block time còn sót",
       GG + "\n- S1 đã liên kết Google",
       "1. Xóa event trên Google ngay sau khi vừa liên kết → chờ sync → kiểm tra\n"
       "2. Xóa event trên Google sau khi đã liên kết ổn định → chờ sync → kiểm tra\n"
       "3. Kiểm tra chiều ngược lại: hủy booking trên LME → kiểm tra Google\n"
       "4. Kiểm tra ngày cụ thể xem còn block time rác không (lưới admin + LINE user)",
       "Event Google bị xóa ở 2 thời điểm",
       "- Cả 2 trường hợp: block time bị xóa hoàn toàn khỏi LME\n"
       "- Không còn khung giờ bị chặn mà không có event tương ứng trên Google\n"
       "- Chiều LME → Google cũng đồng bộ đúng",
       note="Nguồn: Sync google calendar r392-r430, r448-r456 (Bug #28770, #29169, #30419)."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Abnormal",
       "Bug tự detect: 2 staff liên kết 2 tài khoản Google khác nhau rồi đổi staff của booking",
       GG + "\n- S1 liên kết tài khoản Google A, S2 liên kết tài khoản Google B\n"
            "- Có booking「予約確定」của S1 đã sync lên tài khoản A",
       "1. Đổi staff của booking từ S1 sang S2\n2. Kiểm tra Google Calendar tài khoản A\n"
       "3. Kiểm tra Google Calendar tài khoản B\n"
       "4. Lặp lại với trường hợp 2 staff liên kết CÙNG 1 tài khoản",
       "2 tài khoản Google khác nhau",
       "- Event trên tài khoản A bị XÓA\n- Event mới được tạo trên tài khoản B\n"
       "- Trường hợp cùng tài khoản: event chuyển đúng calendar tương ứng",
       note="Nguồn: Sync google calendar r457-r509 (Bug tự detect change staff google calendar)."),

    tc("Googleカレンダー連携", "JOB-001", "Normal",
       "Bug KH #35312: sync lên Google FAIL → ghi vào bảng lỗi và job retry",
       GG + "\n- S1 đã liên kết Google\n- Chuẩn bị được tình huống gọi Google API thất bại",
       "1. Gán thủ công staff S1 cho 1 booking trong lúc Google API lỗi\n"
       "2. Kiểm tra bảng `result_error_google`\n3. Chờ job retry chạy\n"
       "4. Kiểm tra Google Calendar và lịch sử sync ở detail booking\n"
       "5. Lặp lại với calendar loại 個人",
       "Booking gán staff thủ công, Google API lỗi",
       "- Khi sync fail: sinh bản ghi trong `result_error_google` để job retry\n"
       "- Sau khi job retry chạy: event được tạo trên Google, lịch sử sync ghi nhận thành công\n"
       "- Calendar 個人 cho kết quả tương tự",
       note="Nguồn: Sync google calendar r522-r613 (Bug KH #35312, 23/03/2026)."),

    tc("Googleカレンダー連携", "DATA-AUDIT-001", "Normal",
       "Lịch sử đồng bộ Google — màn データ同期履歴 và modal chi tiết",
       GG + "\n- S1 đã liên kết Google, đã có nhiều lượt sync 2 chiều",
       "1. Mở tab「データ同期履歴」khi chưa liên kết → quan sát\n"
       "2. Mở khi đã liên kết → đối chiếu danh sách\n3. Mở modal chi tiết 1 lượt sync\n"
       "4. Bấm popup download CSV",
       "Nhiều lượt sync",
       "- Chưa liên kết: giao diện trống theo design\n"
       "- Đã liên kết: hiện danh sách lượt sync với thời gian và loại thao tác\n"
       "- Modal chi tiết hiện đủ thông tin lượt sync\n- Download CSV: tải được file lịch sử",
       note="Nguồn: Sync google calendar r112-r145 + Setting calendar r1851-r1921. Spec §7.1.3 "
            "(CSV encoding SHIFT-JIS)."),

    tc("Googleカレンダー連携", "PERF-LARGE-001", "Normal",
       "Bug tự detect #38446: hiệu năng khi liên kết / hủy liên kết Google Calendar",
       GG + "\n- Calendar có nhiều staff và nhiều booking (≥ 500 booking)",
       "1. Bấm liên kết Google Calendar cho 1 staff → đo thời gian phản hồi\n"
       "2. Bấm hủy liên kết → đo thời gian\n"
       "3. Với staff bị OFF (tự xóa liên kết) → đo thời gian\n"
       "4. Xóa staff đang liên kết → đo thời gian\n5. Kiểm tra liên kết Google Sheet không bị ảnh hưởng",
       "≥ 500 booking",
       "- Các thao tác hoàn tất trong thời gian chấp nhận được, KHÔNG treo màn hình\n"
       "- Dữ liệu sau thao tác đúng và đầy đủ",
       env="PRODUCTION",
       note="Nguồn: Sync google calendar r621-r634 (Bug tự detect #38446, 07/2026). "
            "RULE-08: performance BẮT BUỘC test production."),

    tc("Googleカレンダー連携", "INTG-CAL-001", "Normal",
       "Support #35768: hủy liên kết Google Calendar KHÔNG ảnh hưởng Google Spreadsheet",
       GG + "\n- Calendar đã liên kết CẢ Google Calendar (per staff) và Google Spreadsheet",
       "1. Bấm text「Googleアカウント・マイカレンダーの接続を解除する」→ xác nhận\n"
       "2. Kiểm tra liên kết Google Spreadsheet ở tab tương ứng\n"
       "3. Cho LINE user đặt lịch mới → kiểm tra dữ liệu ghi vào Google Sheet",
       "Đã liên kết cả 2 dịch vụ Google",
       "- Hủy liên kết Calendar thành công\n"
       "- Liên kết Google Spreadsheet VẪN còn nguyên\n"
       "- Booking mới VẪN được ghi vào Google Sheet",
       note="Nguồn: Sync google calendar r614-r620 (Support #35768, 09/04/2026)."),

    tc("Googleカレンダー連携", "PERM-002", "Normal",
       "Tài khoản staff thao tác liên kết Google Calendar",
       GG + "\n- Có tài khoản staff được cấp quyền màn 予約管理",
       "1. Đăng nhập bằng tài khoản staff → mở tab Googleカレンダー連携\n"
       "2. Thử liên kết / hủy liên kết\n3. Kiểm tra kết quả",
       "Tài khoản staff có quyền",
       "- Staff thao tác được như admin trên màn đã được cấp quyền\n"
       "- Kết quả liên kết/hủy liên kết đúng",
       spec="Đã hỏi leader",
       note="Nguồn: Sync google calendar r520-r521 + Quản lý calendar r1866, r3118, r3287 — corpus ghi "
            "「trên dev acc staff thiếu quyền salon nên ko check được」→ nhóm case này CHƯA từng được "
            "test, xem MT-35."),

    tc("Googleカレンダー連携", "INTG-HOOK-001", "Abnormal",
       "Webhook Google Calendar tới TRỄ / TRÙNG / sai thứ tự",
       GG + "\n- S1 đã liên kết Google Calendar",
       "1. Trên Google: tạo event → sửa giờ → xóa event thật nhanh liên tiếp\n"
       "2. Chờ job xử lý xong → đối chiếu block time trên LME với trạng thái CUỐI CÙNG trên Google\n"
       "3. Chuẩn bị 2 bản ghi callback TRÙNG cho cùng 1 event → chờ job\n"
       "4. Kiểm tra bảng `salon_google_calendar_callback` và `calendar_salon_booking_by_google`",
       "Chuỗi thao tác nhanh trên Google · callback trùng",
       "- Trạng thái block time trên LME khớp trạng thái CUỐI CÙNG trên Google (không kẹt ở bước giữa)\n"
       "- Callback trùng KHÔNG sinh block time nhân đôi\n"
       "- Không còn bản ghi callback kẹt ở trạng thái đang xử lý",
       env="PRODUCTION",
       note="Spec §7.1.1 (queue `salon_google_calendar_callback`, 5 consumer thread, per-bot "
            "serialization). ⚠ Corpus KHÔNG có TC cho webhook trễ/trùng → TC bổ sung theo spec. RULE-08."),

    # ══════════════ 40. Googleスプレッドシート連携 ══════════════
    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Liên kết Google Spreadsheet lần đầu và giao diện trước/sau liên kết",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」"),
       "1. Khi chưa liên kết → quan sát màn\n2. Bấm nút đăng nhập Google → cấp đủ quyền\n"
       "3. Sau khi liên kết → quan sát tên tài khoản và link Google Sheet\n4. Bấm vào link",
       "Tài khoản Google có quyền",
       "- Chưa liên kết: hiện「Googleアカウント連携が完了していません」\n"
       "- Bấm đăng nhập: mở màn OAuth của Google\n"
       "- Sau liên kết: hiện tên tài khoản + ảnh đại diện\n"
       "- Bấm link: mở tab mới file Google Sheet mang tên cửa hàng",
       note="Nguồn: Setting calendar r1534-r1537."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Liên kết Google Spreadsheet KHÔNG cấp đủ quyền → báo lỗi và liên kết lại được",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」"),
       "1. Liên kết tài khoản A nhưng bỏ tick quyền → quan sát\n"
       "2. Liên kết lại tài khoản A và cấp ĐỦ quyền → quan sát\n"
       "3. Lần 1 tài khoản A không cấp quyền → lần 2 liên kết tài khoản B có cấp quyền\n"
       "4. Không cấp quyền 2 lần liên tiếp → lần 3 cấp quyền",
       "2 tài khoản Google",
       "- Không cấp quyền: lỗi「Google スプレッドシートのアクセス権限をチェックしてください」\n"
       "- Cấp đủ quyền ở lần sau: liên kết thành công\n"
       "- Liên kết tài khoản khác có cấp quyền: thành công",
       note="Nguồn: Sync google calendar r87-r103."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Dữ liệu ghi vào Google Sheet — chỉ booking phát sinh SAU khi liên kết",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Trước khi liên kết đã có 3 booking cũ",
       "1. Liên kết Google Sheet → mở file → quan sát\n"
       "2. Cho LINE user đặt 1 booking mới → mở file → quan sát",
       "3 booking cũ + 1 booking mới",
       "- Ngay sau khi liên kết: file chưa có dữ liệu booking cũ\n"
       "- Sau khi có booking mới: file hiện TOÀN BỘ booking (cả cũ và mới)",
       note="Nguồn: Setting calendar r1538-r1540. ⚠ Hành vi này khác trực giác — cần nêu rõ với member "
            "khi test."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Cấu trúc cột của file Google Sheet",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Đã liên kết Google Sheet; có booking đủ các trạng thái",
       "1. Mở file Google Sheet\n2. Đối chiếu từng cột với booking tương ứng",
       "Booking đủ trạng thái",
       "- タイムスタンプ:「2024.10.01（日）08:44」\n- 予約（来店）日:「2024.10.25（金）」\n"
       "- 予約開始時間 / 予約終了時間: HH:MM\n"
       "- ステータス: admin book =「予約確定（手動追加）」· request =「予約リクエスト」· deny =「否認」· "
       "duyệt =「予約確定」· admin hủy =「キャンセル（手動）」· request cancel =「キャンセルリクエスト」· "
       "hủy =「キャンセル」\n"
       "- コース: có system_name thì lấy system_name; không chọn course →「指定なし」\n"
       "- スタッフ: 指定なし →「指定なし」; calendar 個人 →「運営者」\n"
       "- 決済金額: luôn hiện `payment_amount` kể cả khi tắt 決済",
       note="Nguồn: Setting calendar r1547-r1570."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Cột trạng thái thanh toán trong Google Sheet — môi trường test và production",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」"),
       "1. Với calendar TẮT 決済: admin book và user book → đọc cột 決済ステータス\n"
       "2. Môi trường PRODUCTION: admin book · user book duyệt ngay · user request · "
       "admin duyệt request · admin refund · book course free + staff free · book 指定なし → đọc cột\n"
       "3. Môi trường TEST: các trường hợp không bill và có bill → đọc cột",
       "Các trường hợp như mô tả",
       "- Tắt 決済: cả admin và user đều「決済なし」\n"
       "- PRODUCTION: admin book「決済なし」· user duyệt ngay「決済済み」· user request「未決済」· "
       "duyệt request「決済済み」· refund「返金済み」· course+staff free「決済なし」· 指定なし「決済なし」\n"
       "- TEST: không bill →「決済なし」; còn lại →「テスト決済」",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1571-r1581. RULE-08: bill tiền test production."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Google Sheet cập nhật khi trạng thái booking / thanh toán thay đổi",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Đã liên kết Google Sheet; có booking đã ghi vào file",
       "1. Thực hiện lần lượt: admin duyệt · admin từ chối · user hủy · admin hủy · "
       "user gửi yêu cầu hủy · admin duyệt/từ chối yêu cầu hủy · admin XÓA booking\n"
       "2. Sau mỗi thao tác, đọc lại dòng tương ứng trong Google Sheet\n"
       "3. Admin duyệt booking có bill → đọc cột trạng thái thanh toán\n"
       "4. Admin hoàn tiền → đọc cột trạng thái thanh toán",
       "1 booking trải qua đủ vòng đời",
       "- Dòng trong Sheet được CẬP NHẬT theo trạng thái mới (không sinh dòng mới)\n"
       "- Admin xóa booking:「キャンセル（手動）」và KHÔNG bị xóa khỏi danh sách\n"
       "- Duyệt booking có bill: chuyển「決済済み」\n- Hoàn tiền: chuyển「返金済み」",
       note="Nguồn: Setting calendar r1584-r1600."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Booking KHÔNG được ghi vào Google Sheet",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」"),
       "1. LINE user đăng ký chờ thông báo khi slot đầy (status 3) → kiểm tra file\n"
       "2. Admin book vào slot đã đầy → kiểm tra file\n"
       "3. Booking đã bị xóa (`deleted_at` khác NULL) → kiểm tra file",
       "Booking status 3 · admin book full slot · booking đã xóa",
       "- Booking status 3: KHÔNG insert vào file\n"
       "- Admin book full slot:「予約確定（手動追加）」có insert\n"
       "- Booking đã xóa: hiện tại KHÔNG hiển thị trong file",
       note="Nguồn: Setting calendar r1596-r1597, r1601."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Cột friend info trong Google Sheet thay đổi theo cấu hình câu hỏi",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Đã liên kết Google Sheet; có 3 item câu hỏi",
       "1. Thêm 1 item friend info mới → cho đặt lịch → kiểm tra cột trong file\n"
       "2. Xóa 1 item → cho đặt lịch → kiểm tra\n3. Đổi 1 item → cho đặt lịch → kiểm tra\n"
       "4. Sắp xếp lại thứ tự item → cho đặt lịch → kiểm tra",
       "3 item friend info",
       "- Thêm: dữ liệu cột mới được thêm vào (KHÔNG hiển thị tiêu đề cột)\n"
       "- Xóa: các cột bị xóa được đẩy ra sau\n- Đổi: các cột vừa đổi đẩy ra sau\n"
       "- Sắp xếp: các cột hiển thị đúng thứ tự đã sắp xếp",
       note="Nguồn: Setting calendar r1543-r1546."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Người dùng can thiệp vào file Google Sheet",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Đã liên kết Google Sheet, file đang có dữ liệu",
       "1. Đổi TÊN sheet (tab) trong file → cho đặt lịch mới → kiểm tra\n"
       "2. Ẩn dòng cuối cùng của sheet → cho đặt lịch mới → kiểm tra\n"
       "3. Tạo file mới CÙNG TÊN, xóa file cũ → cho đặt lịch mới → kiểm tra\n"
       "4. Tạo file mới KHÁC TÊN, không xóa file cũ → cho đặt lịch mới → kiểm tra",
       "4 kiểu can thiệp",
       "- B1: không update vào sheet cũ nữa, hệ thống mở sheet mới\n"
       "- B2: dữ liệu KHÔNG được cập nhật (đã có ghi chú cảnh báo trên màn)\n"
       "- B3: các booking cũ cũng được ghi lại vào file tự tạo\n"
       "- B4: dữ liệu vẫn ghi vào file CŨ",
       note="Nguồn: Setting calendar r1541-r1542, r1602-r1603."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Hủy liên kết Google Spreadsheet — điều kiện theo trạng thái tạo sheet",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」"),
       "1. Vừa liên kết xong (status = 0) → bấm hủy liên kết\n"
       "2. Trong lúc job đang tạo sheet (status = 1) → bấm hủy\n"
       "3. Sau khi tạo sheet xong (status = 2) → bấm hủy\n"
       "4. Khi tạo sheet lỗi (status = 3) → bấm hủy\n"
       "5. Với tài khoản trước đó không cấp quyền → bấm hủy",
       "4 trạng thái tạo sheet",
       "- status 0, 1, 3: lỗi「スプレッドシートを作成しているため、接続を解除できません。"
       "３〜5分少し待ってから操作してください。」\n"
       "- status 2: hủy thành công\n- Tài khoản không cấp quyền: hủy thành công",
       note="Nguồn: Sync google calendar r94-r98 + Setting calendar r1604-r1607."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Support #32733: liên kết lại Google Sheet — luôn tạo file MỚI và sync toàn bộ",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Calendar đã liên kết Google Sheet và có booking",
       "1. Hủy liên kết → liên kết lại CÙNG email cũ → kiểm tra `google_sheet_account_email`\n"
       "2. Kiểm tra file Google được tạo\n"
       "3. Ngay sau khi liên kết lại, CHƯA có booking mới → kiểm tra file\n"
       "4. Có booking mới ngay sau khi liên kết lại → kiểm tra file\n"
       "5. Có UPDATE trạng thái booking cũ ngay sau khi liên kết lại → kiểm tra file\n"
       "6. Lặp lại với email KHÁC",
       "Calendar đã có booking",
       "- Liên kết lại: lưu được email vào cột `google_sheet_account_email`\n"
       "- LUÔN tạo 1 file Google MỚI cho calendar\n"
       "- Chưa có booking/update mới: KHÔNG sync\n"
       "- Có booking mới hoặc update: sync TOÀN BỘ booking của calendar vào file mới "
       "(gồm cả thông tin mới nhất của booking có update)\n"
       "- Email khác: hành vi tương tự",
       note="Nguồn: Setting calendar r1614-r1620 (Support #32733, 05/11/2025)."),

    tc("Googleスプレッドシート連携", "COMPAT-LEGACY-001", "Normal",
       "Calendar đã liên kết Google Sheet TRƯỚC khi bổ sung cột email",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Calendar liên kết Google Sheet từ trước khi release Support #32733",
       "1. Kiểm tra cột `google_sheet_account_email` trong DB\n"
       "2. Cho LINE user đặt booking mới → kiểm tra file\n"
       "3. Cập nhật trạng thái booking cũ → kiểm tra file\n4. Bấm hủy liên kết",
       "Calendar liên kết cũ",
       "- Cột `google_sheet_account_email` rỗng (không recover được) nhưng KHÔNG gây lỗi\n"
       "- Booking mới vẫn sync vào file Google\n- Update booking vẫn cập nhật được\n"
       "- Hủy liên kết thành công",
       note="Nguồn: Setting calendar r1611-r1614."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "1 tài khoản Google liên kết cho nhiều bot",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Có bot A và bot B, cùng dùng 1 tài khoản Google",
       "1. Liên kết Google Sheet cho calendar của bot A\n2. Liên kết cho calendar của bot B\n"
       "3. Kiểm tra icon Google Sheet ở màn list calendar của cả 2 bot\n"
       "4. Đặt lịch ở mỗi bot → kiểm tra file tương ứng",
       "2 bot, 1 tài khoản Google",
       "- Cả 2 bot liên kết thành công, mỗi bot có file riêng\n"
       "- Icon spreadsheet hiện đúng ở màn list của từng bot\n"
       "- Dữ liệu ghi đúng file, không lẫn giữa 2 bot",
       note="Nguồn: Sync google calendar r92."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Abnormal",
       "Cảnh báo khi mất liên kết Google",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Calendar đã liên kết Google nhưng token bị thu hồi / hết hạn",
       "1. Thu hồi quyền của LME ở phía Google\n2. Mở màn quản lý calendar → quan sát\n"
       "3. Cho LINE user đặt lịch → kiểm tra file Google\n4. Liên kết lại → kiểm tra",
       "Token bị thu hồi",
       "- Hiện alert báo mất liên kết Google\n"
       "- Dữ liệu không sync được nhưng KHÔNG chặn việc đặt lịch\n"
       "- Sau khi liên kết lại: sync lại được",
       note="Nguồn: Sync google calendar r93 + Setting calendar r1610 (Support #32733 — "
            "「Cảnh báo cần liên kết lại với Google」, triển khai ngang cho Salon/Lesson/QrCode)."),

    tc("Googleスプレッドシート連携", "INTG-SHEET-001", "Normal",
       "Booking kết thúc 00:00 sync sang Google Sheet không sinh dòng ảo",
       GG.replace("「Googleカレンダー連携」", "「Googleスプレッドシート連携」")
         + "\n- Đã liên kết Google Sheet",
       "1. Tạo booking「予約確定」ngày 11/07 19:00-00:00\n2. Mở file Google Sheet\n"
       "3. Đếm số dòng của booking này và đọc cột ngày",
       "Booking 19:00-00:00",
       "- Sheet có ĐÚNG 1 dòng cho booking này\n- Cột ngày ghi 11/07 (KHÔNG phải 12/07)\n"
       "- KHÔNG sinh dòng ảo / dòng trùng ở ngày hôm sau",
       note="Nguồn: #38520 r56 (Bug KH #38520, 07/2026)."),
]
