# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 20-24: コース, スタッフ, cài đặt hiển thị, スタッフ自動割り当て (random staff).

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Quản lý course&staff」(07/2024 → 06/2026, 458 TC lá — Sửa max item 08/2025,
    Feature #27496 OFF course/staff, Bug Tester #34656 action/filter chưa save)
  - tab「Quản lý calendar」r2503-r2880 (Feature #27976 random staff), r3117-r3310
    (limit option 1.1/1.2, Review #29803 lịch sử change staff), r3344-r3368 (Bug #30555, #29918)
"""
from _common import tc

CS = ("- Đăng nhập admin (主管理者) bot A\n"
      "- Calendar「サロンA」loại スタッフ, 2 staff S1/S2, 2 course C1/C2\n"
      "- Mở /basic/calendar-salon/{id} → tab「コース・スタッフ」")

S4 = [
    # ══════════════ 20. コース — list & menu ══════════════
    tc("コース — list & menu", "UI-FIELD-001", "Normal",
       "Setting コース選択の利用: bật/tắt điều khiển luồng và bắt buộc 所要時間",
       CS + "\n- Đang ở mục「コースの基本設定」",
       "1. Quan sát lựa chọn mặc định\n"
       "2. Chọn「コース選択を利用しない」→ quan sát phần setting thời gian\n"
       "3. Bỏ trống thời gian cần thiết → lưu\n4. Nhập 0h00 → lưu\n"
       "5. Chuyển qua lại giữa 2 lựa chọn rồi lưu",
       "0h00 · giá trị hợp lệ",
       "- Mặc định「コース選択を利用する」\n"
       "- Chọn không dùng course: hiện thêm ô「thời gian cần thiết」(ghi vào `calendar_salon.time_make_course`), "
       "có dấu bắt buộc\n"
       "- Bỏ trống: required\n- 0h00: lỗi「所要時間は5分以上に設定してください。」\n"
       "- Chuyển qua lại: KHÔNG bị required ở lựa chọn đang không được chọn",
       note="Nguồn: Quản lý course&staff r4, r13-r18. Field #36 `use_course`."),

    tc("コース — list & menu", "PAY-AMOUNT-001", "Normal",
       "Ma trận hiển thị giá course/staff theo 決済 và 2 cờ display_*_cost",
       CS,
       "1. Bật 決済連携 → đặt display_course_cost = 0 rồi = 1 → xem phía LINE user\n"
       "2. Tắt 決済連携 → thử 4 tổ hợp (display_course_cost, display_staff_cost) = "
       "(0,0) · (1,0) · (0,1) · (1,1) → xem phía LINE user ở màn chọn course, detail course, "
       "chọn staff, detail staff và các màn còn lại",
       "4 tổ hợp cờ hiển thị · calendar bật/tắt 決済",
       "- Bật 決済: LUÔN hiện phí course ở mọi màn, bất kể cờ\n"
       "- Tắt 決済 (0,0): KHÔNG hiện phí course ở màn chọn/detail course; không hiện phí tổng ở màn khác\n"
       "- (1,0): hiện phí course ở màn chọn/detail course; KHÔNG hiện phí staff; VẪN hiện phí tổng ở màn khác\n"
       "- (0,1): ngược lại — không hiện phí course, có hiện phí staff, vẫn hiện phí tổng\n"
       "- (1,1): hiện phí course và phí tổng (course + staff) ở mọi màn",
       note="Nguồn: Quản lý course&staff r5-r10. Spec Field #37 ghi「Bắt buộc hiện khi bật payment」"
            "nhưng KHÔNG mô tả ma trận 4 tổ hợp → MT-18."),

    tc("コース — list & menu", "DATA-001", "Normal",
       "Setting hiển thị 所要時間 của course phía LINE user",
       CS,
       "1. Chọn option hiển thị「表示する」→ lưu → xem phía LINE user\n"
       "2. Chọn「表示しない」→ lưu → xem phía LINE user",
       "-",
       "- Mặc định 表示する: LINE user thấy thời gian thực hiện course\n"
       "- 表示しない: LINE user KHÔNG thấy thời gian thực hiện",
       note="Nguồn: Quản lý course&staff r11-r12. Field #38 `display_time_make_course`."),

    tc("コース — list & menu", "OUT-TRUTH-001", "Abnormal",
       "Chọn không dùng course rồi vào menu コースの作成・編集 → popup chặn + link quay lại setting",
       CS + "\n- Đã chọn「コース選択を利用しない」",
       "1. Bấm menu「コースの作成・編集」\n2. Bấm hyperlink「コースの基本設定」trong popup\n"
       "3. Đổi lại thành「コース選択を利用する」→ bấm menu コースの作成・編集",
       "-",
       "- B1: hiện popup trên nền màn hình báo đang chọn không dùng course\n"
       "- B2: chuyển sang màn setting cơ bản của course\n- B3: hiện màn list course bình thường",
       note="Nguồn: Quản lý course&staff r23-r25."),

    tc("コース — list & menu", "FUNC-001", "Normal",
       "Bật/tắt chế độ メニュー (nhóm course) đổi giao diện list",
       CS,
       "1. Quan sát giao diện mặc định\n2. Bấm icon setting menu → chọn「メニューあり」→ lưu\n"
       "3. Quan sát giao diện list\n4. Đổi lại「メニューなし」",
       "-",
       "- Mặc định「メニューなし」, hiện list course phẳng\n"
       "- Chọn メニューあり: list course hiển thị theo nhóm menu\n"
       "- Đổi lại メニューなし: quay về giao diện phẳng",
       note="Nguồn: Quản lý course&staff r26-r29, r200."),

    tc("コース — list & menu", "FUNC-001", "Normal",
       "Tạo / sửa / sắp xếp menu nhóm course",
       CS + "\n- Đã bật chế độ メニューあり",
       "1. Tạo menu mới với tên hợp lệ → lưu\n2. Sửa tên menu → lưu\n"
       "3. Mở modal sắp xếp menu → đổi thứ tự → lưu\n4. Kiểm tra thứ tự phía LINE user",
       "2 menu M1, M2",
       "- Menu tạo/sửa thành công, hiển thị đúng ở list course\n"
       "- Thứ tự sau khi sắp xếp giữ nguyên ở cả màn admin và phía LINE user",
       note="Nguồn: Quản lý course&staff r208-r235 + Booking phía line user r176-r180."),

    tc("コース — list & menu", "LIST-001", "Normal",
       "Bảng list course hiện đủ cột và toggle 予約ページ表示",
       CS,
       "1. Mở màn list course\n2. Đối chiếu các cột\n"
       "3. Gạt toggle「予約ページ表示」của C1 sang OFF\n4. Xem phía LINE user",
       "C1 có ảnh + giá 5,000; C2 không giá",
       "- Cột: drag handle |「予約ページ表示」| ảnh |「コース名」|「料金」| icon edit\n"
       "- Course không có giá: cột 料金 hiện「設定なし」\n"
       "- C1 OFF: LINE user KHÔNG thấy C1 ở màn chọn course",
       note="Nguồn: Quản lý course&staff r30-r74 + Booking phía line user r171. EP-61."),

    tc("コース — list & menu", "STATE-DEP-001", "Normal",
       "Ẩn course (booking_page_display = 0) → xóa booking sync từ Google liên quan",
       CS + "\n- Staff S1 đã liên kết Google Calendar; có booking dùng course C1 đã sync lên Google",
       "1. Gạt toggle 予約ページ表示 của C1 sang OFF\n"
       "2. Kiểm tra Google Calendar của S1\n3. Kiểm tra bảng đồng bộ",
       "Booking dùng C1 đã sync",
       "- Booking sync từ Google liên quan bị xóa\n"
       "- Kiểm tra ở cả Google Calendar và bảng đồng bộ trên tool",
       note="Nguồn: Spec BR-10 + EP-61 (「Khi ẩn: xóa booking sync từ Google liên quan」). "
            "⚠ Corpus KHÔNG có TC cho nhánh này ở course (chỉ có ở staff) → TC bổ sung theo spec, "
            "cần verify hành vi thực tế."),

    tc("コース — list & menu", "DATA-001", "Normal",
       "Sắp xếp course bằng drag-drop đồng bộ sang mọi nơi hiển thị",
       CS + "\n- Có 3 course C1, C2, C3",
       "1. Kéo C3 lên đầu ở màn list course → lưu\n"
       "2. Kiểm tra thứ tự ở: modal filter booking · modal admin thêm booking · "
       "màn chọn course phía LINE user · filter remind",
       "3 course",
       "- Thứ tự mới lưu vào `course_order`\n"
       "- Tất cả các nơi hiển thị đều theo đúng thứ tự mới",
       note="Nguồn: Quản lý course&staff r447 + Quản lý calendar r820, r1027 + "
            "Booking phía line user r172. EP-59."),

    # ══════════════ 21. コース — tạo/sửa/xóa ══════════════
    tc("コース — tạo/sửa/xóa", "FUNC-004", "Abnormal",
       "Validate tên course ở màn コース作成・編集 — TỰ CẮT khi vượt độ dài",
       CS + "\n- Mở form tạo course mới",
       "1. Bỏ trống「コース名」(tên hiển thị phía booking) → lưu\n"
       "2. Nhập 50 ký tự tiếng Nhật → lưu\n3. Nhập 51 ký tự → lưu\n"
       "4. Bỏ trống tên hiển thị bên admin (system name) → lưu\n"
       "5. Nhập 10 ký tự vào system name → lưu\n6. Nhập 11 ký tự vào system name → lưu",
       "Chuỗi 50, 51, 10, 11 ký tự",
       "- B1: Invalid\n- B2: lưu thành công\n- B3: TỰ CẮT còn 50 ký tự\n"
       "- B4: lưu thành công và tự lấy 10 ký tự đầu của コース名\n"
       "- B5: lưu thành công\n- B6: TỰ CẮT còn 10 ký tự",
       note="Nguồn: Quản lý course&staff r238-r243. ⚠ Ở wizard tạo calendar, 51 ký tự lại BÁO LỖI "
            "(Calendar list r196) → 2 lối vào 2 hành vi khác nhau, xem MT-05."),

    tc("コース — tạo/sửa/xóa", "MEDIA-001", "Abnormal",
       "Upload ảnh course: giới hạn 10MB và định dạng",
       CS + "\n- Mở form tạo course",
       "1. Không set ảnh → lưu\n2. Upload ảnh 1000x500 → lưu\n3. Upload ảnh tỉ lệ khác → lưu\n"
       "4. Upload ảnh > 10MB\n5. Upload file không phải ảnh và ảnh .avif\n"
       "6. Upload lần lượt jpg / png / gif / jpeg",
       "Ảnh 1000x500 · ảnh 800x800 · ảnh 12MB · file .txt · .avif · 4 định dạng hợp lệ",
       "- B1, B2, B3, B6: thành công\n"
       "- B4: lỗi「ファイルサイズが制限（10MB）を超えています」\n"
       "- B5: lỗi「ファイルの形式が正しくありません。」",
       env="PRODUCTION",
       note="Nguồn: Quản lý course&staff r244-r250. RULE-08: media BẮT BUỘC test production."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Validate 所要時間 và 料金 của course",
       CS + "\n- Mở form tạo course",
       "1. Set 所要時間 = 0h00 → lưu\n2. Set 0h05 / 1h00 / 23h55 → lưu\n"
       "3. Bỏ trống 料金 → lưu → xem cột 料金 ở list\n4. Nhập 5000 → lưu\n"
       "5. Nhập số âm / số thực / chữ",
       "0h00 · 0h05 · 1h00 · 23h55 · 5000 · -100 · 1.5 · abc",
       "- B1: lỗi「所要時間は5分以上に設定してください。」\n- B2: cả 3 mốc lưu thành công\n"
       "- B3: lưu thành công, tự fill 0, list hiện「設定なし」\n- B4: format 5,000\n"
       "- B5: bị chặn không cho nhập",
       note="Nguồn: Quản lý course&staff r253-r259."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Validate mô tả course — 1000 ký tự, vượt thì tự cắt",
       CS + "\n- Mở form tạo course",
       "1. Bỏ trống mô tả → lưu\n2. Nhập 1000 ký tự tiếng Nhật → lưu\n3. Nhập 1001 ký tự → lưu",
       "Chuỗi 1000 và 1001 ký tự JP",
       "- B1, B2: lưu thành công\n- B3: TỰ CẮT còn 1000 ký tự",
       note="Nguồn: Quản lý course&staff r262-r264."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Tab アクション・詳細設定 của course: lưu được message / action / filter",
       CS + "\n- Mở form course, đã điền tab 基本情報",
       "1. Bấm hyperlink「アクション・詳細設定」→ quan sát điều hướng\n"
       "2. Set message text → lưu → mở lại kiểm tra\n3. Set multi action → lưu → kiểm tra `t_actions_detail`\n"
       "4. Set filter cho action → lưu → kiểm tra\n"
       "5. Double-click nút「予約完了・リクエスト承認時アクションを設定する」",
       "Message + multi action + filter",
       "- Hyperlink: chuyển sang tab setting action, cuộn về đầu trang\n"
       "- Cả 3 loại cài đặt đều hiển thị lại đúng khi mở lại và ghi đúng vào `t_actions_detail`\n"
       "- Double-click: chỉ chuyển tab 1 lần, không lỗi",
       note="Nguồn: Quản lý course&staff r267-r271."),

    tc("コース — tạo/sửa/xóa", "FUNC-DRAFT-001", "Abnormal",
       "Bug Tester #34656: chuyển tab qua lại khi chưa lưu → action và filter phải giữ nguyên",
       CS + "\n- Mở form tạo course",
       "1. Ở tab アクション・詳細設定 set action + filter (CHƯA bấm save)\n"
       "2. Chuyển sang tab 基本情報 rồi quay lại tab アクション\n3. Quan sát action và filter đã set",
       "Action + filter chưa lưu",
       "- Action và filter vẫn hiển thị đúng như vừa set, KHÔNG bị mất\n"
       "- Lặp lại tương tự ở màn quản lý staff",
       note="Nguồn: Info r49 (Bug Tester #34656, 03/2026) + Quản lý course&staff r377-r389."),

    tc("コース — tạo/sửa/xóa", "CONC-002", "Abnormal",
       "Double-click nút lưu course → chỉ tạo 1 course",
       CS + "\n- Form tạo course đã điền đủ dữ liệu hợp lệ",
       "1. Double-click nút save\n2. Đếm số course trong list và DB",
       "Course「カットA」",
       "- Chỉ 1 course được tạo",
       note="Nguồn: Quản lý course&staff r274."),

    tc("コース — tạo/sửa/xóa", "DATA-REF-001", "Abnormal",
       "Xóa course còn booking ở status 0/1/2/5 → chặn",
       CS + "\n- Course C1 còn booking ở các status 0, 1, 2, 5 (kể cả booking đã qua giờ)",
       "1. Bấm nút xóa C1\n2. Đọc alert\n3. Kiểm tra course còn trong list",
       "Booking status 0,1,2,5",
       "- Alert「「ステータス：予約確定、リクエスト」の予約が残っています。このコースを削除する場合、"
       "このコースを予約しているすべての予約が「ステータス：キャンセル」になっている必要があります。」\n"
       "- Course KHÔNG bị xóa (kể cả booking đã qua thời gian)",
       note="Nguồn: Quản lý course&staff r275. Spec BR-11."),

    tc("コース — tạo/sửa/xóa", "DATA-REF-001", "Normal",
       "Xóa course khi booking ở status cho phép → popup confirm → booking chuyển sang 削除済み予約",
       CS + "\n- Course C2 chỉ còn booking ở status 4, 7 (đã cancel) hoặc 3, 6",
       "1. Bấm xóa C2 → đọc popup confirm\n2. Bấm「戻る」/ X → quan sát\n"
       "3. Bấm xóa lại → bấm「このコースを削除する」\n"
       "4. Kiểm tra list course, màn「削除済み予約」và `calendar_salon_course.deleted_at`",
       "Booking status 4, 7, 3, 6",
       "- Popup confirm hiện tên quản lý course + alert「コースを削除した場合、このコースが関連する予約は"
       "すべて「削除済み予約」に表示されます。」\n"
       "- 戻る/X: đóng popup, không xóa\n"
       "- Xác nhận xóa: quay về list course; `calendar_salon_course.deleted_at` được cập nhật; "
       "các booking của course hiện ở màn「削除済み予約」",
       note="Nguồn: Quản lý course&staff r276-r281."),

    tc("コース — tạo/sửa/xóa", "DATA-REF-001", "Normal",
       "Feature #27496: OFF course thì lịch sử vẫn hiện, chỉ ẩn với LINE user",
       CS + "\n- Course C1 có booking cũ của khách F1",
       "1. Gạt OFF C1\n2. Ở admin: mở màn danh sách booking, detail booking, lịch sử → kiểm tra tên course\n"
       "3. Ở LINE user F1: mở màn chọn course\n4. Ở LINE user F1: mở màn lịch sử booking",
       "Course C1 đã OFF, có booking cũ",
       "- Admin: mọi màn vẫn hiển thị tên course C1 bình thường\n"
       "- LINE user: KHÔNG thấy C1 ở màn chọn course\n"
       "- LINE user: booking cũ dùng C1 KHÔNG còn hiển thị ở màn lịch sử",
       note="Nguồn: Quản lý course&staff r648, r679-r705 + Booking phía line user r84. "
            "⚠ Corpus r86 lại ghi「course bị filter thì màn history VẪN hiển thị booking đã book」— "
            "khác với course OFF/xóa, cần phân biệt rõ."),

    tc("コース — tạo/sửa/xóa", "SEC-002", "Abnormal",
       "Truy cập URL detail course khi chưa đăng nhập / bằng bot khác",
       CS + "\n- Có URL detail của course C1 thuộc bot A",
       "1. Đăng xuất → mở URL detail course\n"
       "2. Đăng nhập bot B (không sở hữu C1) → mở URL detail course của bot A",
       "URL detail course bot A",
       "- Chưa đăng nhập: chuyển về màn đăng nhập\n"
       "- Bot khác: bị chặn, không xem/sửa được course của bot A",
       note="Nguồn: Quản lý course&staff r635-r640."),

    # ══════════════ 22. スタッフ — list & tạo/sửa/xóa ══════════════
    tc("スタッフ — list & tạo/sửa/xóa", "LIST-001", "Normal",
       "Màn list staff hiện đủ dữ liệu và các thao tác cơ bản",
       CS,
       "1. Mở màn list staff\n2. Đối chiếu dữ liệu từng dòng\n3. Bấm icon 3 chấm\n"
       "4. Bấm tên staff\n5. Gạt toggle ON/OFF hiển thị trên trang booking\n"
       "6. Kéo-thả sắp xếp staff\n7. Với danh sách nhiều staff → scroll",
       "≥ 3 staff",
       "- Hiển thị đủ dữ liệu staff theo từng dòng\n- 3 chấm: mở menu thao tác\n"
       "- Bấm tên: mở màn detail staff\n- Toggle: cập nhật hiển thị phía LINE user\n"
       "- Kéo thả: lưu thứ tự mới\n- Nhiều staff: scroll được",
       note="Nguồn: Quản lý course&staff r435-r451. EP-28, EP-60, EP-62."),

    tc("スタッフ — list & tạo/sửa/xóa", "INTG-CAL-001", "Normal",
       "Ẩn staff (EP-62 status = 0) → xóa liên kết + booking sync Google của staff đó",
       CS + "\n- Staff S1 đã liên kết Google Calendar, có booking đã sync",
       "1. Gạt toggle 予約ページ表示 của S1 sang OFF\n"
       "2. Kiểm tra Google Calendar của S1\n3. Kiểm tra liên kết Google của S1 ở màn cài đặt\n"
       "4. Kiểm tra bảng `b_c_salon_google_calendar`",
       "S1 đã liên kết Google, có booking sync",
       "- Toàn bộ booking sync từ Google của S1 bị xóa\n"
       "- Bản ghi liên kết Google của S1 bị xóa\n- Màn cài đặt hiện S1 là chưa liên kết",
       note="Nguồn: Spec BR-10 + Sync google calendar r631-r633."),

    tc("スタッフ — list & tạo/sửa/xóa", "DATA-REF-001", "Normal",
       "Copy staff và các thao tác từ menu 3 chấm",
       CS + "\n- Staff S1 đã có đầy đủ cài đặt (ảnh, phí, course phụ trách, action)",
       "1. Bấm 3 chấm ở S1 → chọn copy\n2. Kiểm tra staff mới sinh ra\n"
       "3. Đối chiếu các trường với S1\n4. Kiểm tra lịch làm việc của staff mới",
       "S1 có đầy đủ cài đặt",
       "- Sinh staff mới với dữ liệu copy từ S1\n"
       "- Đối chiếu từng trường: tên, ảnh, phí, danh sách course, cài đặt action\n"
       "- Lịch làm việc: xác nhận có được copy hay không",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý course&staff r456-r466. ⚠ Corpus KHÔNG nói rõ ca làm việc có được copy "
            "hay không → cần Leader xác nhận, xem MT-19."),

    tc("スタッフ — list & tạo/sửa/xóa", "DATA-REF-001", "Abnormal",
       "Xóa staff còn booking chưa cancel → chặn hoặc xử lý nhất quán",
       CS + "\n- Staff S1 có ca ngày 11/07 và booking「予約確定」11/07 20:00-21:00",
       "1. Bấm xóa S1\n2. Quan sát kết quả\n"
       "3. Nếu cho xóa: kiểm tra mọi nơi tham chiếu (danh sách booking, detail, lịch sử, CSV, LIFF)",
       "S1 có ca + booking 予約確定",
       "- HOẶC chặn xóa với thông báo rõ ràng\n"
       "- HOẶC cho xóa và hiển thị trạng thái「đã xóa」ở MỌI nơi tham chiếu\n"
       "- Trong mọi trường hợp: không có màn nào lỗi/trắng, không mất booking",
       spec="Đã hỏi leader",
       note="Nguồn: #38520 r46 + Quản lý course&staff r467. ⚠ Corpus để ngỏ 2 khả năng → cần Leader "
            "chốt, xem MT-19."),

    tc("スタッフ — list & tạo/sửa/xóa", "FUNC-004", "Normal",
       "Validate các trường ở tab 基本情報 của staff",
       CS + "\n- Mở form tạo/sửa staff",
       "1. Bỏ trống tên hiển thị phía booking → lưu\n2. Nhập 50 ký tự → 51 ký tự → lưu\n"
       "3. Bỏ trống tên quản lý (system name) → lưu\n4. Nhập 10 → 11 ký tự → lưu\n"
       "5. Upload ảnh > 10MB · file không phải ảnh · ảnh hợp lệ\n"
       "6. Bỏ trống phí staff → lưu\n7. Nhập 5000 → lưu\n8. Nhập số âm / số thực / chữ",
       "Các giá trị biên như mô tả",
       "- Tên hiển thị: bỏ trống → required; 51 ký tự → tự cắt hoặc báo lỗi\n"
       "- System name: bỏ trống → tự lấy 10 ký tự đầu; 11 ký tự → tự cắt\n"
       "- Ảnh > 10MB / sai định dạng: báo lỗi tương ứng\n"
       "- Phí: bỏ trống → 0 và hiện「設定なし」; 5000 → format 5,000; giá trị sai → chặn",
       note="Nguồn: Quản lý course&staff r485-r541 + Calendar list r209-r215."),

    tc("スタッフ — list & tạo/sửa/xóa", "UI-FIELD-001", "Normal",
       "Cài đặt staff phụ trách course: is_all_course và danh sách course_ids",
       CS + "\n- Calendar có 3 course C1, C2, C3",
       "1. Ở form staff S1 chọn「phụ trách tất cả course」→ lưu\n"
       "2. Chọn chỉ phụ trách C1 và C2 → lưu\n"
       "3. Ở LINE user: chọn course C3 → xem danh sách staff\n"
       "4. Ở LINE user: chọn course C1 → xem danh sách staff",
       "3 course, S1 phụ trách C1 + C2",
       "- Chọn tất cả: LINE user chọn course nào cũng thấy S1\n"
       "- Chọn C1 + C2: LINE user chọn C3 KHÔNG thấy S1; chọn C1 thì thấy S1",
       note="Nguồn: Quản lý course&staff r485-r541 (tab 基本情報) + Quản lý calendar r3440 "
            "(staff không thực hiện course thì không tính vào limit phía friend)."),

    tc("スタッフ — list & tạo/sửa/xóa", "SEC-002", "Abnormal",
       "Truy cập URL detail staff khi chưa đăng nhập / bằng bot khác",
       CS + "\n- Có URL detail staff S1 thuộc bot A",
       "1. Đăng xuất → mở URL detail staff\n2. Đăng nhập bot B → mở URL detail staff của bot A",
       "URL detail staff bot A",
       "- Chưa đăng nhập: chuyển về màn đăng nhập\n- Bot khác: bị chặn",
       note="Nguồn: Quản lý course&staff r641-r647."),

    tc("スタッフ — list & tạo/sửa/xóa", "DATA-ID-001", "Abnormal",
       "2 staff TRÙNG TÊN hiển thị → ca và booking không bị gộp",
       CS + "\n- Tạo staff S1' có tên hiển thị GIỐNG HỆT S1\n- Cả 2 có ca ngày 11/07 và booking riêng",
       "1. Xem lưới calendar theo ngày\n2. Xem danh sách ca ở tab シフト\n"
       "3. Sửa ca của S1 → kiểm tra ca của S1'",
       "2 staff trùng tên",
       "- Calendar hiển thị 2 dòng / 2 ca riêng biệt, KHÔNG gộp thành 1 theo tên\n"
       "- Booking gán đúng từng người\n- Sửa ca S1 KHÔNG ảnh hưởng S1'",
       note="Nguồn: #38520 r48 + Info r46 (bug OEM 16/02/2026: 2 staff cùng tên hiển thị chung 1 dòng "
            "ở màn list lịch làm việc)."),

    # ══════════════ 23. Hiển thị コース・スタッフ ══════════════
    tc("Hiển thị コース・スタッフ", "UI-FIELD-001", "Normal",
       "Setting 指定なし: bật/tắt lựa chọn staff không chỉ định phía LINE user",
       CS + "\n- Đang ở mục「スタッフの表示設定」",
       "1. Chọn CÓ sử dụng 指定なし → lưu → LINE user vào màn chọn staff\n"
       "2. Chọn KHÔNG sử dụng 指定なし → lưu → LINE user vào màn chọn staff\n"
       "3. Với trường hợp OFF hết staff + KHÔNG dùng 指定なし → LINE user vào booking\n"
       "4. Với trường hợp OFF hết staff + CÓ dùng 指定なし → LINE user vào booking",
       "Các tổ hợp như mô tả",
       "- B1: hiện nút「指定しない」ở TRÊN CÙNG danh sách staff\n"
       "- B2: KHÔNG hiện nút 指定しない\n"
       "- B3: LINE user không next sang bước tiếp được\n"
       "- B4: chọn được 指定なし và next sang bước tiếp theo",
       note="Nguồn: Quản lý course&staff r414-r415 + Booking phía line user r188-r193."),

    tc("Hiển thị コース・スタッフ", "UI-FIELD-001", "Normal",
       "Setting hiển thị phí staff và trường hợp calendar loại 個人",
       CS,
       "1. Chọn hiển thị phí staff → lưu → LINE user xem màn chọn staff và detail staff\n"
       "2. Chọn KHÔNG hiển thị phí staff → lưu → LINE user xem lại\n"
       "3. Với calendar loại 個人 → vào mục スタッフの表示設定",
       "-",
       "- Bật: LINE user thấy phí của staff\n- Tắt: LINE user không thấy phí staff\n"
       "- Calendar 個人: mục này bị ẩn / không áp dụng",
       note="Nguồn: Quản lý course&staff r416-r433."),

    tc("Hiển thị コース・スタッフ", "FUNC-001", "Normal",
       "Bỏ qua màn chọn course / chọn staff theo cài đặt",
       CS,
       "1. Bật dùng course + bật dùng staff → LINE user mở link booking\n"
       "2. Tắt dùng course + bật dùng staff → LINE user mở link\n"
       "3. Bật dùng course + tắt dùng staff → LINE user mở link\n"
       "4. Tắt cả 2 → LINE user mở link\n5. Lặp lại với calendar 個人",
       "4 tổ hợp cài đặt",
       "- (bật, bật): màn chọn course → màn chọn staff → màn chọn slot\n"
       "- (tắt, bật): vào thẳng màn chọn staff\n- (bật, tắt): màn chọn course → màn chọn slot\n"
       "- (tắt, tắt): vào thẳng màn chọn slot\n"
       "- Calendar 個人: KHÔNG có bước chọn staff",
       note="Nguồn: Setting calendar r261-r266, r289-r292, r1504-r1507 + Booking phía line user r186-r187, r1318-r1320."),

    # ══════════════ 24. スタッフ自動割り当て ══════════════
    tc("スタッフ自動割り当て", "UI-FIELD-001", "Normal",
       "3 option của スタッフ自動割り当て và hiển thị phần thứ tự ưu tiên",
       CS + "\n- Mở màn setting スタッフ自動割り当て",
       "1. Quan sát option mặc định\n2. Chọn option 2 (random tự do) → lưu\n"
       "3. Chọn option 3 (theo thứ tự ưu tiên) → lưu\n4. Quan sát vùng sắp xếp thứ tự ưu tiên",
       "-",
       "- Mặc định option 1「スタッフ自動割り当てを利用しない」, KHÔNG hiện phần sắp xếp thứ tự\n"
       "- Option 2: lưu thành công, KHÔNG hiện phần sắp xếp thứ tự\n"
       "- Option 3: lưu thành công, HIỆN phần sắp xếp thứ tự ưu tiên\n"
       "- Thứ tự mặc định của danh sách ưu tiên = thứ tự ở màn quản lý staff",
       note="Nguồn: Quản lý calendar r2506-r2509 (Feature #27976, 01/2025). "
            "⚠ Spec KHÔNG có BR nào cho tính năng này → MT-20."),

    tc("スタッフ自動割り当て", "UI-FIELD-001", "Normal",
       "Đổi thứ tự ưu tiên KHÔNG làm đổi thứ tự staff ở các màn khác",
       CS + "\n- Đã chọn option 3, có 3 staff S1, S2, S3",
       "1. Đổi thứ tự ưu tiên thành S3 - S1 - S2 → lưu\n"
       "2. Kiểm tra thứ tự staff ở: màn QL staff · lưới QL ngày · filter staff ở tab シフト · "
       "modal thêm ca · modal import CSV ca · filter staff ở màn remind · phía LINE user\n"
       "3. Kiểm tra thứ tự ở modal detail booking → change staff",
       "3 staff",
       "- Tất cả các màn ở bước 2: giữ nguyên thứ tự cũ, KHÔNG đổi theo thứ tự ưu tiên\n"
       "- Riêng modal detail booking → change staff: hiển thị THEO thứ tự ưu tiên",
       note="Nguồn: Quản lý calendar r2510-r2511."),

    tc("スタッフ自動割り当て", "UI-FIELD-001", "Normal",
       "Nút lưu / back của màn thứ tự ưu tiên",
       CS + "\n- Đang ở màn setting thứ tự ưu tiên",
       "1. Đổi thứ tự → bấm save → reload kiểm tra\n2. Đổi thứ tự → bấm back / X → reload kiểm tra",
       "3 staff",
       "- Bấm save: thứ tự mới được lưu\n- Bấm back/X: KHÔNG lưu thay đổi",
       note="Nguồn: Quản lý calendar r2512-r2513."),

    tc("スタッフ自動割り当て", "FUNC-001", "Normal",
       "Option 1 (không tự phân công): booking vào 指定なし ở mọi lối vào",
       CS + "\n- Đã chọn option 1\n- Staff S1, S2, S3 đều có ca và rảnh",
       "1. LINE user đặt lịch chọn 指定なし\n2. Admin đặt lịch trên web chọn 指定なし\n"
       "3. Admin đặt lịch trên app mobile chọn 指定なし\n"
       "4. Kiểm tra `staff_id` của 3 booking\n5. Kiểm tra Google Calendar của 指定なし",
       "3 staff rảnh",
       "- Cả 3 booking đều giữ nguyên 指定なし (staff_id NULL), KHÔNG random\n"
       "- Action / remind / Google Sheet đều ghi 指定なし\n"
       "- Sync Google: liên kết với Google Calendar của 指定なし",
       note="Nguồn: Quản lý calendar r2556-r2559, r2681-r2683, r3357."),

    tc("スタッフ自動割り当て", "FUNC-001", "Normal",
       "Option 2 (random tự do): chỉ chọn trong các staff THỎA MÃN điều kiện",
       CS + "\n- Đã chọn option 2, limit mỗi staff = 1",
       "1. S1 có ca, S2 có ca, S3 KHÔNG có ca → LINE user đặt 指定なし\n"
       "2. S1 không ca, S2 có ca, S3 không ca → đặt 指定なし\n"
       "3. S1 set ngày nghỉ, S2 và S3 có ca → đặt 指定なし\n"
       "4. S1 có ca (đã có booking), S2 có ca, S3 có ca (đã có booking đã cancel) → đặt 指定なし\n"
       "5. Cả 3 staff đều đã có booking chiếm hết limit → đặt 指定なし",
       "3 staff ở các trạng thái như mô tả",
       "- B1: random vào S1 hoặc S2 (không vào S3)\n- B2: random vào S2\n"
       "- B3: random vào S2 hoặc S3\n- B4: random vào S2 hoặc S3 (booking đã cancel không chiếm slot)\n"
       "- B5: KHÔNG gán được staff → booking giữ nguyên 指定なし",
       note="Nguồn: Quản lý calendar r2560-r2570, r2697, r2712."),

    tc("スタッフ自動割り当て", "FUNC-001", "Normal",
       "Option 3 (theo thứ tự ưu tiên): chọn staff ĐẦU TIÊN thỏa mãn theo danh sách ưu tiên",
       CS + "\n- Đã chọn option 3, thứ tự ưu tiên S1 - S3 - S2, limit mỗi staff = 1",
       "1. S1 có ca, S3 có ca, S2 không ca → LINE user đặt 指定なし\n"
       "2. S1 không ca, S3 có ca, S2 có ca → đặt 指定なし\n"
       "3. S1 set ngày nghỉ, S3 và S2 có ca → đặt 指定なし\n"
       "4. S1 đã có booking 予約確定 / キャンセルリクエスト → đặt 指定なし\n"
       "5. S1 có booking đã cancel / deny / đang request → đặt 指定なし\n"
       "6. S3 có vùng nghỉ của booking khác chèn vào → đặt 指定なし\n"
       "7. S1 có block time từ Google → đặt 指定なし",
       "3 staff, thứ tự ưu tiên S1-S3-S2",
       "- B1: vào S1\n- B2: vào S3\n- B3: vào S3\n- B4: vào S3\n"
       "- B5: vào S1 (booking đã cancel/deny/đang request không chiếm slot)\n"
       "- B6: vào S1\n- B7: vào S3",
       note="Nguồn: Quản lý calendar r2636-r2645."),

    tc("スタッフ自動割り当て", "FUNC-001", "Abnormal",
       "Bug #32588: danh sách ưu tiên KHÔNG đồng bộ với sort ở màn QL staff",
       CS + "\n- Calendar mới tạo với 3 staff, chưa sort lần nào",
       "1. Chưa sort cả 2 nơi → so sánh thứ tự ở màn QL staff và danh sách ưu tiên\n"
       "2. Sort ở màn QL staff (chưa sort danh sách ưu tiên) → so sánh 2 nơi → đặt lịch 指定なし\n"
       "3. Sort ở danh sách ưu tiên (chưa sort màn QL staff) → so sánh → đặt lịch\n"
       "4. Sort cả 2 nơi (2 chiều thứ tự) → so sánh → đặt lịch\n"
       "5. Xóa staff đứng đầu danh sách ưu tiên → so sánh → đặt lịch",
       "3 staff",
       "- B1: 2 nơi hiển thị thứ tự GIỐNG NHAU\n"
       "- B2: màn QL staff theo thứ tự đã sort; danh sách ưu tiên GIỮ thứ tự ban đầu; "
       "booking nhảy vào staff đầu tiên của DANH SÁCH ƯU TIÊN\n"
       "- B3, B4: booking luôn nhảy vào staff đầu tiên của danh sách ưu tiên\n"
       "- B5: danh sách ưu tiên bỏ staff đã xóa, booking vào staff đầu tiên còn lại",
       note="Nguồn: Quản lý calendar r2515-r2541 (Bug #32588, 27/10/2025). "
            "Áp dụng cho cả admin book và user book (booking approve ngay + request)."),

    tc("スタッフ自動割り当て", "FUNC-001", "Normal",
       "Random staff hoạt động ở cả 3 lối đặt lịch, kể cả nhiều booking liên tiếp",
       CS + "\n- Đã bật random (option 2 hoặc 3)\n- Có ≥ 3 staff rảnh",
       "1. LINE user đặt liên tiếp 3 booking chọn 指定なし\n"
       "2. Admin đặt trên web liên tiếp 3 booking chọn 指定なし\n"
       "3. Admin đặt trên app mobile liên tiếp 3 booking chọn 指定なし\n"
       "4. Kiểm tra `staff_id` của tất cả booking",
       "≥ 3 staff rảnh",
       "- MỌI booking đều được gán staff thỏa mãn, không booking nào bị bỏ sót\n"
       "- Cả 3 lối vào cho kết quả nhất quán",
       note="Nguồn: Quản lý calendar r2694, r2709, r2724."),

    tc("スタッフ自動割り当て", "FUNC-001", "Normal",
       "Đặt lịch CÓ chọn staff cụ thể → giữ nguyên, không random",
       CS + "\n- Đã bật random",
       "1. LINE user đặt và chọn S2\n2. Admin web đặt và chọn S2\n3. Admin app đặt và chọn S2",
       "S2",
       "- Cả 3 booking giữ nguyên staff S2, KHÔNG bị random sang staff khác",
       note="Nguồn: Quản lý calendar r2693, r2708, r2723."),

    tc("スタッフ自動割り当て", "FUNC-DATE-001", "Boundary",
       "Random × thời gian nhận booking: khác nhau giữa LINE user và admin",
       CS + "\n- Đã bật random; có cài đặt thời gian bắt đầu nhận và hạn nhận booking",
       "1. LINE user đặt TRƯỚC giờ bắt đầu nhận → quan sát\n"
       "2. LINE user đặt ĐÚNG lúc bắt đầu nhận / SAU đó → quan sát\n"
       "3. LINE user đặt TRƯỚC hạn nhưng job random chạy SAU hạn → quan sát\n"
       "4. LINE user đặt ĐÚNG hạn / SAU hạn → quan sát\n"
       "5. Admin đặt ở TẤT CẢ các mốc trên → quan sát",
       "Các mốc thời gian như mô tả",
       "- LINE user trước giờ nhận: slot bị disable, không đặt được\n"
       "- LINE user đúng/sau giờ nhận, trước hạn: đặt thành công + random được staff\n"
       "- LINE user đặt trước hạn nhưng job chạy sau hạn: VẪN thành công + random được\n"
       "- LINE user đúng hạn hoặc sau hạn: lỗi「予約の受付が終了されました。」\n"
       "- Admin: THÀNH CÔNG + random được ở TẤT CẢ các mốc (không bị chặn bởi thời gian nhận)",
       note="Nguồn: Quản lý calendar r2684-r2692, r2700-r2707, r2715-r2722."),

    tc("スタッフ自動割り当て", "DATA-COUNT-001", "Boundary",
       "Bug #29918: chỉ cho đặt khi CÓ staff thực hiện được (option 1.1)",
       CS + "\n- Đã bật random; limit theo option 1 (đếm theo số staff)",
       "1. S1 và S2 đều có ca → limit calendar = 2 → đặt lịch\n"
       "2. S1 có ca nhưng OFF, S2 có ca → limit calendar = 1 → đặt lịch\n"
       "3. S1 có ca nhưng KHÔNG thực hiện course đã chọn, S2 có ca → đặt lịch phía LINE user\n"
       "4. S1 có ca, S2 KHÔNG có ca → limit = 1 → đặt lịch\n"
       "5. S1 có ca nhưng OFF, S2 không ca → limit = 0 → đặt lịch\n"
       "6. Cả 2 không có ca → limit = 0 → đặt lịch",
       "6 cấu hình như mô tả",
       "- B1: đặt được 2 booking cùng khung\n- B2, B3, B4: đặt được 1 booking\n"
       "- B5, B6: KHÔNG đặt được (limit = 0)\n"
       "- Kiểm tra ở cả phía LINE user và lưới admin",
       note="Nguồn: Quản lý calendar r3371-r3492 (Bug #29918, 24/05/2025 — sửa spec: chỉ cho booking khi "
            "có staff thực hiện được). Trường hợp 3 CHỈ kiểm tra phía LINE user."),

    tc("スタッフ自動割り当て", "FUNC-001", "Abnormal",
       "Bug #30555: staff KHÔNG có ca vẫn nhận booking khi random",
       CS + "\n- S1 và S2 có ca, S3 KHÔNG có ca",
       "1. Option 2 (random tự do): admin đặt 指定なし → kiểm tra staff được gán\n"
       "2. Option 2: LINE user đặt 指定なし → kiểm tra\n"
       "3. Option 3 với S3 ưu tiên đầu tiên: admin đặt 指定なし → kiểm tra\n"
       "4. Option 1: admin đặt 指定なし → kiểm tra\n"
       "5. Lặp lại cho case ca qua ngày",
       "S3 không có ca",
       "- B1, B2, B3: random vào S1 hoặc S2, TUYỆT ĐỐI không vào S3\n"
       "- B4: booking giữ 指定なし\n- Case qua ngày cho kết quả nhất quán",
       note="Nguồn: Quản lý calendar r3344-r3358 (Bug #30555, 03/07/2025)."),

    tc("スタッフ自動割り当て", "INTG-CAL-001", "Normal",
       "Đổi staff của booking → đồng bộ lại Google Calendar theo trạng thái booking",
       CS + "\n- Staff S1 và S2 đều đã liên kết Google Calendar",
       "1. Booking 予約リクエスト (status 0) → đổi staff → kiểm tra Google\n"
       "2. Booking user 予約確定 (status 1) → đổi staff → kiểm tra\n"
       "3. Booking admin book (status 2) → đổi staff → kiểm tra\n"
       "4. Booking user cancel (status 4) / admin cancel (7) / deny (6) → đổi staff → kiểm tra\n"
       "5. Booking キャンセルリクエスト (status 5) → đổi staff → kiểm tra\n"
       "6. Đổi từ 指定なし → staff, staff → 指定なし, staff 1 → staff 2",
       "Booking ở đủ các status",
       "- status 0: KHÔNG sync sang Google của staff mới; chỉ khi admin approve mới sync\n"
       "- status 1, 2, 5: XÓA event Google cũ và TẠO event ở Google của staff mới\n"
       "- status 4, 7: xóa event cũ, KHÔNG tạo event mới\n"
       "- status 6: KHÔNG sync\n- Cả 3 chiều đổi ở bước 6 đều xử lý như trên",
       note="Nguồn: Quản lý calendar r2742-r2751."),

    tc("スタッフ自動割り当て", "JOB-001", "Normal",
       "Đổi staff của booking → tính lại remind trong event_step_time",
       CS + "\n- Calendar đã bật remind; có booking 予約リクエスト và booking 予約確定",
       "1. Booking 予約リクエスト → đổi staff → kiểm tra `event_step_time`\n"
       "2. Admin approve booking đó → kiểm tra `event_step_time`\n"
       "3. Booking 予約確定 → đổi staff → kiểm tra `event_step_time`",
       "Remind đã cài đặt · booking ở 2 trạng thái",
       "- B1: KHÔNG insert remind\n- B2: insert remind sau khi approve\n"
       "- B3: XÓA các remind cũ (trừ remind đã gửi status = 2) và insert remind mới ngay",
       note="Nguồn: Quản lý calendar r2761-r2762."),

    tc("スタッフ自動割り当て", "DATA-AUDIT-001", "Normal",
       "Review #29803: lịch sử ghi thêm bản ghi phân công staff",
       CS + "\n- Đã bật random staff",
       "1. Admin đặt 指定なし → random vào S1 → xem lịch sử booking\n"
       "2. LINE user đặt 指定なし → random vào S1 → xem lịch sử\n"
       "3. Random KHÔNG tìm được staff (vào 指定なし) → xem lịch sử\n"
       "4. Admin đổi thủ công từ S1 sang S2 → xem lịch sử\n"
       "5. Admin đổi thủ công từ 指定なし sang S2 → xem lịch sử\n"
       "6. Admin chọn lại CHÍNH staff hiện tại → xem lịch sử",
       "Các thao tác như mô tả",
       "- Random: ngoài bản ghi trạng thái, sinh thêm bản ghi「指定なし自動割り当て（スタッフ〇〇）」\n"
       "  (tên staff lấy từ `staff_system_name`, kèm người thao tác)\n"
       "- Đổi thủ công staff → staff: bản ghi「手動スタッフ変更（〇〇→△△）」\n"
       "- Đổi thủ công 指定なし → staff: bản ghi「手動割り当て（スタッフ〇〇）」\n"
       "- Chọn lại chính staff hiện tại: KHÔNG sinh bản ghi lịch sử",
       note="Nguồn: Quản lý calendar r3291-r3304 (Review #29803, 29/04/2025)."),

    tc("スタッフ自動割り当て", "DATA-AUDIT-001", "Normal",
       "Lịch sử random staff hiển thị đúng nhãn theo option và sort mới nhất lên đầu",
       CS,
       "1. Option 1: user đặt (booking success và request) + admin đặt → xem nội dung lịch sử\n"
       "2. Option 2: user đặt (booking success, request, sau khi approve) → xem nhãn\n"
       "3. Option 3: tương tự → xem nhãn\n4. Kiểm tra thứ tự sắp xếp lịch sử ở web và app",
       "3 option × 3 kiểu đặt",
       "- Option 1: nội dung như cũ, KHÔNG có thêm「（自動割り当て）」; modal detail hiện 指定なし / "
       "staff đã chọn như ban đầu\n"
       "- Option 2 và 3: nhãn có thêm「（自動割り当て）」— vd「予約完了（自動割り当て）」,「予約リクエスト（自動割り当て）」\n"
       "- Lịch sử sort thời gian MỚI NHẤT lên đầu ở cả web và app",
       note="Nguồn: Quản lý calendar r2828-r2839, r3318-r3321 (Review #29803 bổ sung sort)."),

    tc("スタッフ自動割り当て", "DATA-COUNT-001", "Boundary",
       "SpecChange #32679: ma trận random option × limit option",
       CS + "\n- Có 3 staff, mỗi staff limit = 1",
       "1. random option 2 + limit option 1.1 (1 staff xuyên suốt 1 booking) → đặt lịch\n"
       "2. random option 2 + limit option 1.2 (nhiều staff cùng thực hiện 1 booking) → đặt lịch\n"
       "3. random option 3 + limit option 2 (không giới hạn) → đặt lịch\n"
       "4. random option 2 + limit option 3 = 1 → đặt lịch\n"
       "5. random option 2 + limit option 3 = 3 → đặt lịch\n"
       "6. random option 2 + limit option 3 = 4 → đặt lịch",
       "3 staff, mỗi staff limit 1, các tổ hợp option",
       "- Mỗi tổ hợp: booking được gán staff theo đúng quy tắc random và đếm limit tương ứng\n"
       "- Số booking tối đa trên 1 khung giờ khớp giá trị limit đã cấu hình\n"
       "- Với limit option 3 = 4 mà chỉ có 3 staff mỗi staff limit 1: tối đa vẫn là 3 booking",
       note="Nguồn: Quản lý calendar r2843-r2878 (SpecChange #32679, 03/11/2025). "
            "⚠ Nhánh limit 3 = 4 > tổng limit staff — kết quả mong đợi cần Leader xác nhận, xem MT-21."),
]
