# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 4-15: màn quản lý đặt lịch (ngày/tuần/tháng/list), filter,
一括操作, admin thêm booking, modal lý do, detail booking, booking đã xóa, hoàn tiền.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Quản lý calendar」(07/2024 → 07/2026, 4097 TC lá — tab MASTER lớn nhất, 9 cột ticket:
    Bug#34667 · Bug Tester #34185 · SpecImprove #33147 · Bug #32775 · SpecChange #32679 ·
    Bug #32568 · Support #32704 · Bug KH #36938)
  - tab「Main case」r270-r329 (logic hiển thị tuần/tháng)
  - tab「Today&NewBooking」·「#30919」·「Check middle ware」
"""
from _common import tc

CAL = ("- Đăng nhập admin (主管理者) bot A\n"
       "- Calendar「サロンA」loại スタッフ, 2 staff S1/S2 (+ 指定なし), course「カットA」60 phút\n"
       "- Mở /basic/calendar-salon/{id} → tab「予約カレンダー」")
DAY = CAL + "\n- Đang ở chế độ hiển thị theo ngày, ngày hiện tại có lịch làm việc S1 09:00-18:00"

S2 = [
    # ══════════════ 4. Tab 本日/新着の予約 ══════════════
    tc("Tab 本日/新着の予約", "LIST-001", "Normal",
       "Bảng danh sách booking hiện đủ 8 cột + phân trang",
       CAL + "\n- Có 60 booking ở các trạng thái khác nhau",
       "1. Mở tab「本日／新着の予約」\n2. Đối chiếu từng cột với booking đã tạo\n3. Chuyển sang trang 2",
       "60 booking · per_page = 50",
       "- Đủ 8 cột: 操作が行われた日時 | 来店予定日時 | ステータス | お名前 | コース | スタッフ | 決済金額 | nút thao tác\n"
       "- Ngày format Y.m.d, giờ format H:i\n- Trang 2 hiện 10 booking còn lại, số dòng khớp tổng 60",
       note="Nguồn: Quản lý calendar r637-r643, r659. Spec feature-spec.md §2.2 SCR-SLN-02a, EP-07."),

    tc("Tab 本日/新着の予約", "LIST-001", "Normal",
       "Cột スタッフ / コース lấy tên quản lý (system_name), private hiện 個人",
       CAL + "\n- Có booking của calendar スタッフ và 1 calendar 個人",
       "1. Xem booking của calendar スタッフ có staff + course\n"
       "2. Xem booking của calendar 個人\n3. Xem course KHÔNG set system_name",
       "Course có/không có system_name",
       "- Calendar スタッフ: cột スタッフ hiện `staff_system_name`, không có thì để trống\n"
       "- Calendar 個人: cột スタッフ hiện「個人」\n"
       "- Course: có system_name → hiện system_name; không có → hiện course_name",
       note="Nguồn: Quản lý calendar r640-r642."),

    tc("Tab 本日/新着の予約", "DATA-COUNT-001", "Normal",
       "Bộ đếm 予約数 và キャンセル数 đếm đúng nhóm status",
       CAL + "\n- Trong khoảng hiển thị có: 2 booking status 1, 1 status 2, 1 status 5, "
             "1 status 4, 1 status 7, 1 status 6",
       "1. Mở tab danh sách với khoảng ngày chứa 6 booking trên\n"
       "2. Đọc「予約数」và「キャンセル数」\n3. Đối chiếu bằng tay",
       "status 1,2,5 = 4 booking · status 4,7 = 2 booking · status 6 = 1",
       "- 予約数 = 4 (đếm status 1, 2, 5)\n- キャンセル数 = 2 (đếm status 4, 7)\n"
       "- Booking status 6 (否認) không vào cả 2 bộ đếm",
       note="Nguồn: Quản lý calendar r676-r677."),

    tc("Tab 本日/新着の予約", "LIST-001", "Normal",
       "Khoảng hiển thị mặc định là 7 ngày kể từ hôm nay",
       CAL,
       "1. Mở tab danh sách lần đầu\n2. Đọc dòng「表示期間」",
       "Hôm nay = 02/07/2024 (ví dụ)",
       "- Mặc định hiển thị booking từ hôm nay đến 7 ngày sau\n"
       "- Format「表示期間：2024年7月2日(火) 〜 2024年7月9日(火)」",
       note="Nguồn: Quản lý calendar r659, r675."),

    tc("Tab 本日/新着の予約", "LIST-001", "Normal",
       "Xóa từ khóa tìm kiếm và Enter → hiện lại toàn bộ dữ liệu",
       CAL + "\n- Đang có kết quả tìm kiếm theo từ khóa",
       "1. Xóa trắng ô tìm kiếm → nhấn Enter\n2. Đối chiếu số dòng với khi chưa search",
       "Từ khóa bất kỳ",
       "- Hiện lại toàn bộ danh sách như trước khi search",
       note="Nguồn: Quản lý calendar r680, r683."),

    tc("Tab 本日/新着の予約", "BULK-001", "Abnormal",
       "Không chọn booking nào → nút アクションを選択する không mở modal",
       CAL,
       "1. Không tick booking nào\n2. Bấm「アクションを選択する >」\n"
       "3. Tick 1 booking → bấm lại",
       "-",
       "- B2: không mở modal action\n- B3: mở modal action đồng loạt",
       note="Nguồn: Quản lý calendar r684-r685."),

    tc("Tab 本日/新着の予約", "UI-003", "Normal",
       "Cột 決済金額 hiện 決済なし cho các trường hợp không phát sinh thanh toán",
       CAL,
       "1. Booking ở calendar KHÔNG bật bill tiền\n"
       "2. Calendar bật bill nhưng course giá 0 — admin book và user book\n"
       "3. Calendar bật bill, course có giá nhưng ADMIN book\n"
       "4. Calendar bật bill, course có giá, USER book",
       "Course 0 yên và course 5,000 yên",
       "- B1, B2, B3: cột hiện「決済なし」\n- B4: hiện「テスト決済」(môi trường test)",
       note="Nguồn: Quản lý calendar r756-r760."),

    # ══════════════ 5. Calendar theo ngày ══════════════
    tc("Calendar theo ngày", "LIST-001", "Normal",
       "Cột staff hiển thị đủ và đúng thứ tự, private hiện 運営者",
       DAY,
       "1. Mở calendar theo ngày của calendar loại スタッフ\n"
       "2. Mở calendar theo ngày của calendar loại 個人\n3. Với calendar có nhiều staff → scroll ngang",
       "Calendar 個人 và calendar スタッフ ≥ 10 staff",
       "- Loại 個人: chỉ 1 cột staff tên「運営者」\n"
       "- Loại スタッフ: cột đầu là「指定なし」, các staff sau theo đúng thứ tự màn QL staff\n"
       "- Nhiều staff: hiện thanh scroll; khi scroll thì cột khung giờ bên trái KHÔNG bị trôi theo",
       note="Nguồn: Quản lý calendar r10-r11, r138, r152, r155 (Support #32704 — cố định khung giờ khi scroll)."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Hiển thị 同時に対応できる数 của từng staff và link sang màn setting",
       DAY + "\n- S1 set limit = 2, S2 không set limit",
       "1. Đọc dòng 同時に対応できる数 của cột 指定なし, S1 và S2\n2. Bấm vào con số của S1",
       "S1 limit 2 · S2 không limit",
       "- Cột 指定なし: hiện text「説明を見る」\n- S1: hiện số 2\n- S2: hiện text「設定しない」\n"
       "- Bấm vào: mở màn setting 受付上限",
       note="Nguồn: Quản lý calendar r12-r17, r127, r141."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Icon khung giờ theo lịch làm việc: có ca = O xanh, không ca = O gạch chéo xám",
       DAY + "\n- S1 có ca 09:00-18:00, S2 không có ca nào, S3 set ngày nghỉ",
       "1. Quan sát cột S1 trong và ngoài khung 09:00-18:00\n2. Quan sát cột S2\n3. Quan sát cột S3",
       "3 staff ở 3 trạng thái ca khác nhau",
       "- S1 trong ca: icon O màu #5799DB, nền #EDF4FB\n- S1 ngoài ca: icon O gạch chéo, màu xám\n"
       "- S2: toàn bộ khung giờ đều là O gạch chéo\n"
       "- S3: kéo dài từ khung đầu đến khung cuối, hiện text「休日」",
       note="Nguồn: Quản lý calendar r18-r20, r130-r131."),

    tc("Calendar theo ngày", "UI-001", "Boundary",
       "Ca nằm giữa khung giờ: chỉ phần trong ca mới hiện O",
       DAY + "\n- Đơn vị nhận booking = 30 phút; S1 có ca 09:30-09:50",
       "1. Quan sát khung 09:30-10:00 của S1",
       "Ca 09:30~09:50 · khung 30 phút",
       "- Từ 09:30 đến 09:50 hiện O\n- Từ 09:50 đến 10:00 hiện O gạch chéo",
       note="Nguồn: Quản lý calendar r21."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Booking hiển thị đúng format và đúng nhãn trạng thái",
       DAY + "\n- Có booking approve, booking request, booking đã cancel, booking bị deny, "
             "và 1 event sync từ Google",
       "1. Quan sát từng booking trên lưới",
       "5 loại bản ghi",
       "- Format: giờ bắt đầu - kết thúc + tên người đặt (theo setting) + tên course\n"
       "- Nhãn: đã approve =「予約確定」· đang request =「リクエスト」· đã cancel =「キャンセル」\n"
       "- Booking bị deny: KHÔNG hiện ở lưới, chỉ hiện ở màn danh sách với status「否認済」\n"
       "- Event Google: hiện icon + label + tên event (dài thì cắt bằng ...)",
       note="Nguồn: Quản lý calendar r33, r45-r48."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Hiển thị 前後の空き時間 theo đúng cài đặt, kể cả với event sync từ Google",
       DAY + "\n- Có 1 booking LME và 1 event sync từ Google trong ngày",
       "1. Không set thời gian nghỉ → quan sát\n2. Chỉ set nghỉ trước 30 phút → quan sát\n"
       "3. Chỉ set nghỉ sau 30 phút → quan sát\n4. Set cả trước và sau → quan sát",
       "time_before = 30 · time_after = 30",
       "- B1: không hiện vùng nghỉ ở cả booking LME và event Google\n"
       "- B2: hiện vùng nghỉ TRƯỚC booking, LINE user không đặt được trong vùng này\n"
       "- B3: hiện vùng nghỉ SAU booking, LINE user không đặt được\n"
       "- B4: hiện cả 2 vùng",
       note="Nguồn: Quản lý calendar r49-r52 (kết quả 4 nhánh khác nhau nhưng cùng 1 ma trận cài đặt; "
            "verify 2 tầng: lưới admin + khả năng đặt phía LINE user)."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "前後の空き時間 chỉ hiện với booking status 予約確定 và キャンセルリクエスト",
       DAY + "\n- Đã set nghỉ trước/sau; có booking ở 5 trạng thái",
       "1. Quan sát vùng nghỉ của: booking đã approve · đợi approve · đã cancel · "
       "đang request cancel · đang đợi nhận thông báo",
       "5 booking khác status",
       "- Đã approve: CÓ hiện time nghỉ\n- Đợi approve: KHÔNG hiện\n- Đã cancel: KHÔNG hiện\n"
       "- Request cancel: CÓ hiện\n- Đợi nhận thông báo: KHÔNG hiện",
       note="Nguồn: Quản lý calendar r63-r67 (5 state → giữ 1 TC vì cùng 1 lần quan sát ma trận, "
            "liệt kê đủ 5 điểm ở cột Dữ liệu — kết quả từng điểm ghi rõ trong Expected)."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Nhiều booking chồng giờ được xếp đúng số hàng",
       DAY,
       "1. Tạo booking 09:00-09:30 và 09:30-10:00 → quan sát\n"
       "2. Tạo 2 booking 09:00-10:00 rồi thêm 08:30-09:00 → quan sát\n"
       "3. Tạo 08:00-09:00 và 10:00-10:30 rồi thêm 09:00-10:00 → quan sát\n"
       "4. Tạo 08:00-09:00 · 08:00-09:30 · 09:30-10:00 · 07:30-09:00 → quan sát",
       "Các cặp giờ như mô tả",
       "- B1: 2 booking nằm trên 1 hàng\n- B2: hiển thị 2 hàng\n"
       "- B3: nằm trên 1 hàng\n- B4: nằm trên 3 hàng",
       note="Nguồn: Quản lý calendar r53-r56."),

    tc("Calendar theo ngày", "LIST-001", "Normal",
       "Time picker: chọn ngày quá khứ / tương lai / năm khác đều load đúng dữ liệu",
       DAY,
       "1. Quan sát ngày mặc định\n2. Mở time picker, chọn ngày trong tháng này · tháng quá khứ · "
       "tháng tương lai · năm trước · năm sau\n3. Bấm mũi tên next 1 lần và nhiều lần\n"
       "4. Bấm mũi tên back 1 lần và nhiều lần\n5. Bấm「今日」",
       "Các mốc ngày như mô tả",
       "- Mặc định là ngày hiện tại, format「10月1日(日)」\n"
       "- Mọi mốc chọn/next/back đều hiển thị đúng dữ liệu của ngày đã chọn\n"
       "- Bấm 今日: luôn quay về calendar của hôm nay",
       note="Nguồn: Quản lý calendar r75-r87 (13 dòng cùng 1 kết quả「hiển thị đúng dữ liệu」→ gộp 1 TC, "
            "liệt kê đủ các mốc ở Các bước — RULE gộp cùng kết quả)."),

    tc("Calendar theo ngày", "UI-FIELD-001", "Normal",
       "Dropdown 予約受付時間の単位: mặc định 30分 và đủ 13 lựa chọn",
       DAY,
       "1. Bấm nút「予約受付時間の単位」→ quan sát popup mô tả\n2. Mở dropdown chọn đơn vị",
       "-",
       "- Popup mô tả đơn vị nhận booking hiện ra\n"
       "- Dropdown mặc định 30分, có đủ: 10分 15分 20分 30分 45分 1時間 1時間30分 2時間 3時間 4時間 6時間 12時間 1日",
       note="Nguồn: Quản lý calendar r90-r92."),

    tc("Calendar theo ngày", "UI-004", "Normal",
       "Checkbox hiển thị dữ liệu lọc đúng 4 loại phần tử trên lưới",
       DAY + "\n- Ngày đang xem có: booking LME, event sync Google, vùng nghỉ trước/sau, icon O/O gạch chéo",
       "1. Quan sát trạng thái mặc định\n2. Chỉ tick「booking」\n3. Chỉ tick「sync google」\n"
       "4. Chỉ tick「thời gian trống trước sau」\n5. Chỉ tick「icon có thể/không thể book」\n"
       "6. Bỏ tick tất cả",
       "4 loại phần tử trên cùng 1 ngày",
       "- Mặc định: tick tất cả, hiện đủ 4 loại\n"
       "- Mỗi lần chỉ tick 1 loại: CHỈ loại đó hiển thị, 3 loại còn lại bị ẩn\n"
       "- Bỏ tick hết: lưới hiển thị trắng",
       note="Nguồn: Quản lý calendar r114-r119."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Bấm vào vùng 前後の空き時間 mở popup mô tả đúng cho cả booking LME và event Google",
       DAY + "\n- Đã set nghỉ trước/sau 60 phút; có 1 booking LME và 1 event Google",
       "1. Bấm vùng nghỉ TRƯỚC của booking LME\n2. Bấm vùng nghỉ SAU của booking LME\n"
       "3. Bấm vùng nghỉ TRƯỚC của event Google\n4. Bấm vùng nghỉ SAU của event Google\n"
       "5. Trong popup bấm text「前後の空き時間」",
       "time_before = time_after = 60",
       "- Mỗi lần: mở popup hiện số phút nghỉ + ngày giờ của booking tương ứng\n"
       "- Label: nghỉ trước =「予約前の空き時間（60分）」, nghỉ sau =「予約後の空き時間（60分）」\n"
       "- Bấm hyperlink: mở màn setting 前後の空き時間",
       note="Nguồn: Quản lý calendar r120-r123, r1277-r1284."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Nút スタッフ追加 / スタッフ管理 / checkbox ẩn staff nghỉ chỉ có ở calendar loại スタッフ",
       DAY + "\n- Có 1 calendar 個人 và 1 calendar スタッフ; calendar スタッフ có 1 staff đang nghỉ",
       "1. Ở calendar 個人: tìm 3 thành phần trên\n"
       "2. Ở calendar スタッフ: bấm「スタッフ追加」\n3. Bấm「スタッフ管理」\n"
       "4. Tick checkbox ẩn staff nghỉ",
       "1 staff đang set nghỉ trong ngày",
       "- Calendar 個人: KHÔNG có cả 3 thành phần\n"
       "- スタッフ追加: hiện popup nhập tên staff → sau khi nhập ra màn detail staff → lưu xong quay lại "
       "màn QL ngày và staff mới hiển thị\n"
       "- スタッフ管理: chuyển sang màn QL staff\n"
       "- Mặc định KHÔNG tick, staff nghỉ vẫn hiện; tick vào → staff nghỉ bị ẩn khỏi lưới",
       note="Nguồn: Quản lý calendar r68-r74."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Rule cuộn/hiển thị mốc giờ đầu tiên theo booking và ca sớm nhất",
       DAY,
       "1. Có booking sớm nhất 06:00, ca bắt đầu 07:00 → mở màn\n"
       "2. Ca bắt đầu 08:00, booking sớm nhất 09:00 → mở màn\n"
       "3. Ca bắt đầu 00:00, booking 01:00 → mở màn\n"
       "4. Ca bắt đầu 00:00, có booking qua ngày 23:00-00:30 → mở màn\n"
       "5. Cuộn xuống rồi admin thêm booking thành công",
       "Các mốc như mô tả",
       "- B1: hiển thị bắt đầu từ booking sớm nhất (06:00)\n- B2: bắt đầu từ giờ ca (08:00)\n"
       "- B3, B4: bắt đầu từ 00:00\n- B5: sau khi thêm thành công, cuộn về đầu giờ làm việc",
       note="Nguồn: Quản lý calendar r188-r192, r196."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Nút シフト編集 trên cột staff: ẩn với ngày quá khứ và với 指定なし",
       DAY,
       "1. Chuyển về 1 ngày quá khứ → quan sát nút edit ca\n"
       "2. Ở hôm nay, staff CÓ ca → bấm nút edit ca\n3. Ở hôm nay, staff CHƯA có ca → bấm nút edit ca\n"
       "4. Quan sát cột 指定なし\n"
       "5. Ngày 11 có ca qua ngày 20:00-05:00 → bấm edit ca ở ngày 12",
       "Ngày quá khứ · hôm nay · ngày 12 sau ca qua ngày",
       "- B1: KHÔNG hiện nút edit ca\n- B2: mở màn edit ca đúng ngày + đúng staff\n"
       "- B3: mở màn edit, khung giờ trống như màn thêm mới\n"
       "- B4: cột 指定なし KHÔNG có nút edit ca\n"
       "- B5: hiển thị đúng lịch của ngày 12 (rỗng), KHÔNG kéo theo ca qua ngày của ngày 11",
       note="Nguồn: Quản lý calendar r197-r199, r205, r207-r208."),

    tc("Calendar theo ngày", "DATA-001", "Normal",
       "Modal 表示変更（LINE名/システム表示名）đổi được cách hiển thị tên ở mọi màn",
       DAY + "\n- Có booking của LINE user trong hệ thống và booking do admin nhập tay tên khách",
       "1. Mở オプション →「表示変更（LINE名/システム表示名）」\n"
       "2. Chọn lần lượt 4 tuỳ chọn: LINE名/システム表示名 · システム表示名/LINE名 · chỉ LINE名 · chỉ システム表示名\n"
       "3. Với mỗi tuỳ chọn, đối chiếu tên hiển thị ở: danh sách booking theo ngày · detail booking · "
       "detail lịch sử · modal cancel · modal admin thêm booking\n"
       "4. Kiểm tra booking của khách nhập tay",
       "1 LINE user có system_name, 1 LINE user KHÔNG có system_name, 1 khách nhập tay",
       "- Mặc định là LINE名/システム表示名\n"
       "- Mỗi tuỳ chọn: tên ở cả 5 màn đổi đúng theo setting\n"
       "- Khách nhập tay: luôn hiện tên đã nhập lúc booking, không phụ thuộc setting",
       note="Nguồn: Quản lý calendar r168-r175. ⚠ Corpus ghi NG ở modal admin add booking cho 3/4 tuỳ chọn "
            "(case user không có system_name) → cần verify lại sau khi fix, xem MT-08."),

    # ══════════════ 6. Calendar theo tuần ══════════════
    tc("Calendar theo tuần", "UI-001", "Normal",
       "Lưới tuần hiện thứ 2 → CN, trục dọc từ 00:00 đến 24:00",
       CAL,
       "1. Chuyển chế độ hiển thị sang tuần\n2. Quan sát hàng ngang và cột dọc",
       "-",
       "- Hàng ngang: thứ 2 đến CN, format「10月1日(月)」\n"
       "- Cột dọc: khung giờ 0h → 24h (không có setting giờ mở cửa riêng cho lưới tuần)",
       note="Nguồn: Quản lý calendar r542. ⚠ Corpus ghi「nếu được thì scroll xuống thời gian làm việc "
            "gần nhất => chưa check」— hành vi cuộn ở lưới tuần chưa được xác nhận."),

    tc("Calendar theo tuần", "UI-001", "Normal",
       "Icon có thể/không thể book ở lưới tuần theo trạng thái ca của các staff",
       CAL + "\n- Chuyển sang chế độ tuần",
       "1. Ngày có staff CÓ ca và staff đang ON → quan sát\n"
       "2. Ngày có staff có ca nhưng đã OFF → quan sát\n3. Ngày không staff nào có ca → quan sát\n"
       "4. Ngày 1 staff set nghỉ nhưng staff khác có ca → quan sát",
       "Các trạng thái ca như mô tả",
       "- B1: icon có thể book\n- B2: icon KHÔNG thể book\n- B3: icon KHÔNG thể book\n"
       "- B4: khung giờ có ca hiện O, khung ngoài ca hiện O gạch chéo",
       note="Nguồn: Quản lý calendar r543-r550."),

    tc("Calendar theo tuần", "UI-001", "Boundary",
       "Ô ngày ở lưới tuần tô xanh theo hợp của các khoảng ca",
       CAL + "\n- Chuyển sang chế độ tuần",
       "1. Ca staff 07:00-07:30 → quan sát\n2. Ca staff 07:30-08:30 → quan sát\n"
       "3. S1 08:00-09:00 và S2 09:00-10:00 → quan sát",
       "Các khoảng ca như mô tả",
       "- B1: tô xanh ô 07:00-08:00\n- B2: tô xanh ô 07:00-09:00\n- B3: tô xanh ô 08:00-10:00",
       note="Nguồn: Quản lý calendar r545-r547."),

    tc("Calendar theo tuần", "DATA-COUNT-001", "Normal",
       "Thống kê số booking trong ô tuần đếm đúng theo 3 nhóm trạng thái",
       CAL + "\n- Khung 09:00-10:00 ngày X có: 1 user book approve, 1 admin book, 1 request booking, "
             "1 request cancel, 1 user cancel, 1 admin cancel, 1 booking bị deny, 1 event Google",
       "1. Chuyển sang chế độ tuần\n2. Đọc 3 con số thống kê trong ô 09:00-10:00 ngày X\n3. Tính tay đối chiếu",
       "8 bản ghi như mô tả",
       "- 予約確定 = 2 (user approve + admin book)\n- リクエスト = 2 (request booking + request cancel)\n"
       "- キャンセル = 2 (user cancel + admin cancel)\n"
       "- Booking bị deny KHÔNG hiện ở lưới\n- Event Google KHÔNG được đếm và KHÔNG hiển thị\n"
       "- Format hiển thị: trạng thái - số lượng",
       note="Nguồn: Quản lý calendar r556-r569 (ma trận đếm — RULE-05 có phép tính tay)."),

    tc("Calendar theo tuần", "UI-001", "Normal",
       "Lưới tuần KHÔNG hiển thị vùng nghỉ trước/sau",
       CAL + "\n- Đã set nghỉ trước/sau 30 phút, có booking trong tuần",
       "1. Chuyển sang chế độ tuần\n2. Quan sát ô chứa booking",
       "time_before = time_after = 30",
       "- Chỉ hiển thị booking, KHÔNG hiển thị vùng nghỉ trước/sau",
       note="Nguồn: Quản lý calendar r554, r568."),

    tc("Calendar theo tuần", "LIST-001", "Normal",
       "Rê chuột vào ô có booking → nút 詳細を見る mở popup danh sách booking của khung đó",
       CAL + "\n- Ô 09:00-10:00 ngày X có ≥ 2 booking của các staff khác nhau",
       "1. Chuyển sang chế độ tuần\n2. Rê chuột vào ô 09:00-10:00\n3. Bấm「詳細を見る」",
       "≥ 2 booking cùng khung",
       "- Rê chuột: hiện nút「詳細を見る」\n"
       "- Bấm: mở popup danh sách booking của ngày giờ đó, gồm TẤT CẢ staff",
       note="Nguồn: Quản lý calendar r570-r571, r766."),

    tc("Calendar theo tuần", "LIST-001", "Normal",
       "Date picker tuần: mặc định tuần hiện tại, next/back và 今日 hoạt động đúng",
       CAL,
       "1. Chuyển sang chế độ tuần → đọc dòng ngày\n2. Bấm date picker\n"
       "3. Bấm next 1 lần và nhiều lần\n4. Bấm back 1 lần và nhiều lần\n5. Bấm「今日」",
       "-",
       "- Mặc định tuần hiện tại bắt đầu từ thứ 2, format「10月 1日 (月) > 10月 7日 (日)」\n"
       "- Date picker mở calendar, focus vào hôm nay\n"
       "- next/back: hiển thị đúng dữ liệu tuần tương ứng\n- 今日: quay về tuần hiện tại",
       note="Nguồn: Quản lý calendar r572-r579."),

    tc("Calendar theo tuần", "LIST-001", "Normal",
       "Popup danh sách booking theo tuần: đủ cột, sort, hyperlink tên user",
       CAL + "\n- Popup danh sách booking của 1 khung giờ đang mở",
       "1. Đối chiếu header với ngày đã chọn\n2. Đối chiếu các cột dữ liệu\n"
       "3. Bấm tên user (user trong hệ thống)\n4. Bấm tên khách nhập tay\n"
       "5. Bấm sort theo status → sort theo staff\n6. Bấm「詳細」của 1 booking\n"
       "7. Bấm X / 閉じる",
       "Booking của user hệ thống + khách nhập tay",
       "- Header: ngày đã chọn, format「2024.10.01(日)」\n"
       "- Cột: 予約日時 | ステータス | お客様 | スタッフ | コース\n"
       "- User hệ thống: tên là hyperlink, mở tab mới màn mypage của user\n"
       "- Khách nhập tay: KHÔNG có hyperlink\n"
       "- Sort status: 0→7 và ngược lại; sort staff: nhỏ→lớn và ngược lại\n"
       "- 詳細: mở detail booking; X/閉じる: đóng popup",
       note="Nguồn: Quản lý calendar r767-r782."),

    # ══════════════ 7. Calendar theo tháng ══════════════
    tc("Calendar theo tháng", "UI-001", "Normal",
       "Icon ở lưới tháng theo trạng thái ca — khác quy tắc lưới tuần",
       CAL,
       "1. Chuyển sang chế độ tháng\n2. Ngày chỉ có 1 staff nhưng đã OFF → quan sát\n"
       "3. Ngày có 2 staff, 1 ON 1 OFF → quan sát\n4. Ngày không staff nào có ca → quan sát\n"
       "5. Ngày có staff set nghỉ (các staff khác không có ca / có ca) → quan sát",
       "Các trạng thái như mô tả",
       "- B2: icon KHÔNG thể book\n- B3: icon CÓ thể book\n"
       "- B4: icon CÓ thể book\n- B5: cả 2 trường hợp đều icon CÓ thể book",
       note="Nguồn: Quản lý calendar r595-r599. ⚠ Lưới tháng cho ngày KHÔNG có ca vẫn hiện「có thể book」"
            "trong khi lưới tuần hiện「không thể book」(r548) → hành vi lệch giữa 2 lưới, xem MT-09."),

    tc("Calendar theo tháng", "DATA-COUNT-001", "Normal",
       "Thống kê booking theo ngày ở lưới tháng đếm đúng 3 nhóm, bỏ event Google",
       CAL + "\n- Ngày X có 2 booking approve, 1 request booking, 1 request cancel, 1 user cancel, "
             "1 admin cancel, 1 deny, 1 event Google",
       "1. Chuyển sang chế độ tháng\n2. Đọc 3 con số ở ô ngày X\n3. Tính tay đối chiếu",
       "8 bản ghi ngày X",
       "- 予約確定 = 2 · リクエスト = 2 · キャンセル = 2\n"
       "- Booking deny không hiện ở lưới (chỉ ở màn danh sách với「否認済」)\n"
       "- Event Google không đếm, không hiển thị",
       note="Nguồn: Quản lý calendar r600-r612."),

    tc("Calendar theo tháng", "LIST-001", "Normal",
       "Date picker tháng: mặc định tháng hiện tại, next/back và 今日",
       CAL,
       "1. Chuyển sang chế độ tháng → đọc tiêu đề\n2. Bấm date picker\n"
       "3. Bấm next / back 1 lần và nhiều lần\n4. Bấm「今日」",
       "-",
       "- Mặc định tháng hiện tại, format「2024年10月」\n- Date picker mở calendar theo tháng\n"
       "- next/back: đúng dữ liệu tháng tương ứng\n- 今日: quay về tháng hiện tại",
       note="Nguồn: Quản lý calendar r614-r621."),

    tc("Calendar theo tháng", "LIST-001", "Normal",
       "Popup danh sách booking theo tháng và các thao tác trong popup",
       CAL + "\n- Ngày X có ≥ 3 booking",
       "1. Chuyển chế độ tháng, rê chuột ô ngày X → bấm「詳細を見る」\n"
       "2. Đối chiếu header và cột\n3. Bấm tên người đặt\n4. Sort theo status rồi theo staff\n"
       "5. Bấm「詳細」1 booking\n6. Bấm X / 閉じる",
       "≥ 3 booking ngày X",
       "- Popup hiện danh sách booking trong ngày đã chọn, header format「2024.10.01(日)」\n"
       "- Cột: 予約日時 | ステータス | お客様 | スタッフ | コース\n"
       "- Tên người đặt: mở tab mới màn mypage\n- Sort đúng 2 chiều\n"
       "- 詳細: mở detail booking; X/閉じる: đóng popup",
       note="Nguồn: Quản lý calendar r784-r793."),

    tc("Calendar theo tháng", "UI-004", "Normal",
       "Ở lưới tuần và tháng, checkbox hiển thị chỉ còn 2 loại phần tử",
       CAL,
       "1. Ở chế độ tuần: quan sát mặc định · chỉ tick booking · chỉ tick icon · bỏ tick hết\n"
       "2. Lặp lại ở chế độ tháng",
       "-",
       "- Mặc định tick tất cả\n- Chỉ tick booking: chỉ hiện booking LME (mọi status)\n"
       "- Chỉ tick icon: chỉ hiện icon có/không thể book\n- Bỏ tick hết: hiển thị trắng toàn bộ",
       note="Nguồn: Quản lý calendar r590-r593, r632-r635. ⚠ Nhánh「booking sync google」ở 2 lưới này "
            "corpus ghi「chưa test」→ cần verify."),

    # ══════════════ 8. Hiển thị theo list & tab シフト ══════════════
    tc("Hiển thị theo list & tab シフト", "LIST-001", "Normal",
       "Chuyển đổi 4 chế độ hiển thị ngày/tuần/tháng/list giữ đúng focus",
       CAL,
       "1. Từ chế độ ngày chọn lần lượt tuần → tháng → list\n"
       "2. Từ mỗi chế độ, chọn ngược lại về ngày",
       "-",
       "- Mỗi lần chọn: hiển thị đúng dạng tương ứng và focus vào dạng đang chọn",
       note="Nguồn: Quản lý calendar r106-r109, r582-r585, r628-r631."),

    tc("Hiển thị theo list & tab シフト", "LIST-001", "Normal",
       "Tab シフト: danh sách ca sort mặc định theo ngày tăng dần, sort được theo staff",
       CAL + "\n- Có ca của S1 và S2 ở nhiều ngày",
       "1. Chuyển sang chế độ list → mở tab「シフト」\n2. Quan sát thứ tự mặc định\n"
       "3. Bấm sort theo staff\n4. Ở calendar 個人 quan sát cột staff\n"
       "5. Với staff CHƯA có ca → quan sát",
       "Ca của 2 staff ở nhiều ngày",
       "- Mặc định sort theo `date_setting` tăng dần\n- Sort theo staff: theo tên staff\n"
       "- Calendar 個人: cột staff hiện「運営者」và phần chọn staff bị ẩn\n"
       "- Staff chưa có ca: hiện text thông báo trống",
       note="Nguồn: Quản lý calendar r698, r701, r705, r742-r744."),

    tc("Hiển thị theo list & tab シフト", "FUNC-001", "Normal",
       "Tab シフト: nút 詳細 mở màn edit ca; nút thêm ca / thêm booking mở đúng modal",
       CAL,
       "1. Ở tab シフト bấm「詳細」của 1 ca\n2. Bấm「シフト追加」\n3. Bấm「予約追加」",
       "Ca đã có sẵn",
       "- 詳細: mở màn edit lịch làm việc của ca đó\n"
       "- シフト追加: mở modal thêm ca (màn 21)\n- 予約追加: mở modal thêm booking (màn 22)",
       note="Nguồn: Quản lý calendar r706, r751-r752."),

    tc("Hiển thị theo list & tab シフト", "LIST-001", "Normal",
       "Phân trang ở tab booking và tab シフト",
       CAL + "\n- Có > 1 trang dữ liệu ở cả 2 tab",
       "1. Ở tab booking bấm số trang / next / previous\n"
       "2. Ở tab シフト bấm số trang / next / previous\n3. Đối chiếu item đầu-cuối mỗi trang",
       "> 1 trang dữ liệu",
       "- Dữ liệu từng trang hiển thị đúng\n- Số thứ tự item đầu - cuối của mỗi trang khớp",
       note="Nguồn: Quản lý calendar r687, r747."),

    # ══════════════ 9. Modal filter booking & shift ══════════════
    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Filter booking theo khoảng ngày: mặc định 7 ngày, chặn start > end",
       CAL,
       "1. Mở modal filter booking → đọc khoảng ngày mặc định\n"
       "2. Chọn start date > end date → bấm lọc",
       "-",
       "- Mặc định: từ ngày hiện tại đến 7 ngày sau\n- start > end: KHÔNG được phép",
       note="Nguồn: Quản lý calendar r797, r803."),

    tc("Modal filter booking & shift", "LIST-001", "Boundary",
       "Filter theo 予約開始時間 — các tổ hợp time from/to cho kết quả khác nhau",
       CAL + "\n- Có booking ở nhiều khung giờ trong ngày",
       "1. time from < time to → lọc\n2. time from = time to → lọc\n3. time from > time to → lọc\n"
       "4. Đặt 00:00 - 00:00 → lọc\n5. Chỉ nhập time from, để time to = 00:00 → lọc\n"
       "6. Chỉ nhập time to, để time from = 00:00 → lọc\n7. Bỏ trống cả 2 ô → lọc",
       "Các tổ hợp giờ như mô tả",
       "- B1: lọc booking có time start nằm trong khoảng [from, to]\n"
       "- B2: chỉ booking có time start bằng đúng giá trị đó\n"
       "- B3: vẫn cho nhập nhưng kết quả rỗng\n- B4: KHÔNG lọc theo giờ\n"
       "- B5: chỉ lọc theo time from\n- B6: lọc từ 00:00 đến time to\n- B7: KHÔNG lọc",
       note="Nguồn: Quản lý calendar r804-r815 (7 kết quả khác nhau → giữ chung 1 TC ma trận vì cùng "
            "1 lần mở modal, ghi rõ kết quả từng nhánh)."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Filter theo コース / スタッフ — đồng bộ thứ tự sort và ẩn item OFF",
       CAL + "\n- Có 3 course (1 course đang OFF) và 3 staff (1 staff đang OFF)",
       "1. Sort lại danh sách course ở màn QL course → mở modal filter\n"
       "2. OFF 1 course → mở modal filter\n3. Không chọn course → lọc\n"
       "4. Chọn 1 course → lọc\n5. Chọn nhiều course → lọc\n6. Chọn「全選択」→ lọc\n"
       "7. Lặp lại các bước tương ứng cho staff\n8. Với calendar 個人 → quan sát vùng staff",
       "3 course (1 OFF) · 3 staff (1 OFF)",
       "- Danh sách trong modal khớp thứ tự đã sort ở màn quản lý\n"
       "- Course/staff OFF: KHÔNG hiện trong modal filter\n"
       "- Không chọn = 全選択 = KHÔNG lọc\n- Chọn 1 hoặc nhiều: lọc đúng theo lựa chọn\n"
       "- Calendar 個人: vùng chọn staff bị ẩn",
       note="Nguồn: Quản lý calendar r820-r837."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Filter theo 予約ステータス — ánh xạ đúng sang giá trị status",
       CAL + "\n- Có booking đủ các status 0,1,2,3,4,5,6,7",
       "1. Chọn 予約確定 → lọc\n2. Chọn 予約リクエスト中 → lọc\n3. Chọn キャンセルリクエスト中 → lọc\n"
       "4. Chọn キャンセル → lọc\n5. Chọn「全選択」→ lọc",
       "Booking đủ 8 status",
       "- 予約確定 → status 1, 2\n- 予約リクエスト中 → status 0\n- キャンセルリクエスト中 → status 5\n"
       "- キャンセル → status 4, 7\n"
       "- 全選択 → status 0,1,2,4,5,7 (KHÔNG gồm status 3 đợi thông báo và 6 bị deny)",
       note="Nguồn: Quản lý calendar r840-r845."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Filter theo 決済ステータス — 4 trạng thái cơ bản",
       CAL + "\n- Có booking với payment_status 0, 1, 2, 3",
       "1. Chọn 未決済 → lọc\n2. Chọn 決済成功 → lọc\n3. Chọn 返金済み → lọc\n4. Chọn 決済なし → lọc",
       "4 booking khác payment_status",
       "- 未決済 → payment_status = 0\n- 決済成功 → 1\n- 返金済み → 3\n- 決済なし → 2",
       note="Nguồn: Quản lý calendar r848-r851."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Filter thêm 2 trạng thái 現地決済 (thanh toán tại chỗ)",
       CAL + "\n- Calendar bật 決済 với payment_time = 2 (選択可能)\n"
             "- Có booking 現地決済 chưa thanh toán và đã thanh toán",
       "1. Mở modal filter → chọn trạng thái 現地決済 chưa thanh toán → lọc\n"
       "2. Chọn trạng thái 現地決済 đã thanh toán → lọc",
       "2 booking 現地決済",
       "- Chưa thanh toán: lọc ra booking có `payment_time` = 2 và `payment_status` = 0\n"
       "- Đã thanh toán: `payment_time` = 2 và `payment_status` = 1",
       note="Nguồn: Quản lý calendar r2823-r2825. ⚠ Spec §9.1 mục 1 ghi「現地決済 không có constants "
            "trong source」→ TC này LẤP GAP của spec, xem MT-12."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Nút xóa filter, bấm 絞り込み表示 nhiều lần, và trường hợp không chọn gì",
       CAL,
       "1. Đặt filter → bấm icon X trên chip filter\n"
       "2. Bấm/double-click nút「絞り込み表示」\n3. Không chọn điều kiện gì → bấm lọc",
       "-",
       "- X: clear filter\n- Double-click: chỉ chạy 1 lần, hiện dữ liệu theo filter đã chọn\n"
       "- Không chọn gì: hệ thống VẪN luôn lọc theo date + time",
       note="Nguồn: Quản lý calendar r865-r867."),

    tc("Modal filter booking & shift", "LIST-001", "Normal",
       "Modal filter tab シフト: mặc định 1 tháng, dữ liệu ngoài lưới ăn theo filter",
       CAL + "\n- Đang ở chế độ list, tab シフト",
       "1. Bấm「絞り込み」→ đọc khoảng ngày mặc định\n"
       "2. Lọc trong 1 tuần / 1 tháng / nhiều tháng / nhiều năm\n"
       "3. start = end → lọc\n4. start > end → lọc\n"
       "5. Bấm/double-click「絞り込み表示」\n6. Không chọn gì → lọc",
       "Các khoảng ngày như mô tả",
       "- Mặc định: từ hôm nay đến 1 tháng sau\n"
       "- Mọi khoảng hợp lệ: dữ liệu ĐÚNG theo khoảng đã chọn; ngày hiển thị bên ngoài màn quản lý "
       "phải ăn theo khoảng filter bên trong\n"
       "- start = end: hiện dữ liệu của đúng ngày đó\n- start > end: KHÔNG được phép",
       note="Nguồn: Quản lý calendar r919-r925, r943-r944."),

    # ══════════════ 10. リクエスト一括操作 ══════════════
    tc("リクエスト一括操作", "BULK-001", "Normal",
       "Modal 一括操作: default, bộ đếm đã chọn, đóng modal",
       CAL + "\n- Đang ở chế độ list, đã tick 3 booking",
       "1. Bấm「リクエスト一括操作」\n2. Quan sát lựa chọn mặc định + số lượng\n3. Bấm X / 閉じる",
       "3 booking đã tick",
       "- Mặc định chọn「新規予約リクエストを承認する」\n- Hiện「3人を選択中」\n- X/閉じる: đóng popup",
       note="Nguồn: Quản lý calendar r870-r872."),

    tc("リクエスト一括操作", "BULK-001", "Abnormal",
       "Không tick booking nào → nút mở modal 一括操作 bị disable",
       CAL,
       "1. Không tick booking nào\n2. Quan sát nút「リクエスト一括操作」",
       "-",
       "- Nút bị disable, không mở được modal",
       note="Nguồn: Quản lý calendar r873."),

    tc("リクエスト一括操作", "MSG-001", "Normal",
       "Duyệt hàng loạt 新規予約リクエスト có chọn 実行する — gửi action theo cài đặt",
       CAL + "\n- Có 3 booking đang ở trạng thái 予約リクエスト của 3 LINE user",
       "1. Chuẩn bị 4 cấu hình: (a) không set action nào · (b) có message pattern + có sử dụng · "
       "(c) có message pattern + chọn không sử dụng · (d) message pattern + multi action\n"
       "2. Với mỗi cấu hình: tick 3 booking → 一括操作 → chọn 承認する + 実行する → thực thi\n"
       "3. Kiểm tra status ở màn list và tin nhắn phía LINE user",
       "3 booking request · 4 cấu hình action",
       "- Cả 4 cấu hình: 3 booking chuyển「予約確定」, màn list cập nhật status\n"
       "- (a): không gửi tin nhắn nào\n- (b): gửi message pattern lúc approve\n"
       "- (c): KHÔNG gửi tin nhắn\n- (d): gửi message pattern + toàn bộ multi action\n"
       "- Trước khi chạy hiện alert「※コース・スタッフ別の予約完了時アクションを設定している場合、"
       "全体設定の予約（リクエスト承認）時アクションは稼働しません。」",
       note="Nguồn: Quản lý calendar r874-r878."),

    tc("リクエスト一括操作", "MSG-001", "Normal",
       "Duyệt hàng loạt chọn 実行しない — luôn KHÔNG gửi action dù đã cài đặt",
       CAL + "\n- Có 3 booking 予約リクエスト; đã cài message pattern + multi action + có sử dụng",
       "1. Tick 3 booking → 一括操作 → chọn 承認する + 実行しない → thực thi\n"
       "2. Kiểm tra status và tin nhắn phía LINE user\n"
       "3. Kiểm tra bảng `action_lineuser`",
       "3 booking request",
       "- 3 booking chuyển「予約確定」\n- KHÔNG gửi tin nhắn nào cho LINE user\n"
       "- KHÔNG sinh bản ghi trong `action_lineuser`",
       note="Nguồn: Quản lý calendar r879-r881, r887."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Duyệt hàng loạt khi course/staff có action riêng — ưu tiên action của course/staff",
       CAL + "\n- Course C1 và staff S1 đều có cài đặt action riêng; booking dùng C1 + S1",
       "1. course + staff set action message và CÓ sử dụng → duyệt với 実行する\n"
       "2. course + staff CHỈ set action message và chọn KHÔNG sử dụng → duyệt với 実行する\n"
       "3. course + staff chỉ set multi action (không set message) → duyệt với 実行する\n"
       "4. course + staff set cả message + multi action → duyệt với 実行する\n"
       "5. Lặp lại B1 nhưng chọn 実行しない",
       "1 booking dùng C1 + S1",
       "- B1: gửi action của course + staff\n"
       "- B2: gửi action CHUNG của booking (không phải của course/staff)\n"
       "- B3: gửi action của course + staff\n- B4: gửi message + multi action của course + staff\n"
       "- B5: KHÔNG gửi action nào",
       note="Nguồn: Quản lý calendar r883-r887, r1115-r1118. ⚠ Spec KHÔNG có BR nào mô tả thứ tự ưu tiên "
            "action course/staff vs booking chung → MT-10."),

    tc("リクエスト一括操作", "JOB-001", "Normal",
       "Duyệt request booking hàng loạt → sinh bản ghi remind vào event_step_time",
       CAL + "\n- Calendar đã bật remind trước giờ hẹn\n- Có 3 booking 予約リクエスト",
       "1. Duyệt hàng loạt 3 booking\n2. Kiểm tra bảng `event_step_time` theo user_booking_id\n"
       "3. Chờ đến thời điểm remind → kiểm tra LINE user nhận tin",
       "3 booking request · 1 remind trước 1 ngày lúc 10:00",
       "- Sinh bản ghi remind tương ứng cho từng booking trong `event_step_time`\n"
       "- Đến giờ, LINE user nhận đúng tin nhắn remind",
       note="Nguồn: Quản lý calendar r882. RULE-06 (đi tới output cuối = tin nhắn LINE)."),

    tc("リクエスト一括操作", "MSG-001", "Normal",
       "Từ chối hàng loạt 新規予約リクエスト — action theo cài đặt, KHÔNG sinh remind",
       CAL + "\n- Có 3 booking 予約リクエスト; calendar đã bật remind",
       "1. Chuẩn bị 4 cấu hình action như TC duyệt\n"
       "2. Với mỗi cấu hình: tick 3 booking → chọn「新規予約リクエストを否認する」+ 実行する → thực thi\n"
       "3. Kiểm tra status, tin nhắn, và bảng `event_step_time`\n"
       "4. Lặp lại 1 cấu hình với 実行しない",
       "3 booking request · 4 cấu hình action",
       "- 3 booking chuyển「否認済」\n- Action gửi theo đúng cấu hình (giống quy tắc duyệt)\n"
       "- Chọn 実行しない: KHÔNG gửi action nào\n"
       "- KHÔNG sinh bản ghi remind trong `event_step_time`",
       note="Nguồn: Quản lý calendar r888-r895. Ghi chú corpus: nhánh này KHÔNG quan tâm action của course/staff."),

    tc("リクエスト一括操作", "MSG-001", "Normal",
       "Duyệt hàng loạt キャンセルリクエスト — chuyển キャンセル và XÓA remind chưa gửi",
       CAL + "\n- Có 3 booking đang ở キャンセルリクエスト; calendar đã bật remind (đã sinh event_step_time)",
       "1. Chuẩn bị 4 cấu hình action\n"
       "2. Tick 3 booking → chọn「キャンセルリクエストを承認する」+ 実行する → thực thi\n"
       "3. Kiểm tra status + tin nhắn + bảng `event_step_time`\n4. Lặp lại với 実行しない",
       "3 booking request cancel",
       "- 3 booking chuyển「キャンセル」\n- Action gửi theo đúng cấu hình; 実行しない → không gửi\n"
       "- Toàn bộ remind CHƯA gửi của các booking này bị xóa khỏi `event_step_time`",
       note="Nguồn: Quản lý calendar r896-r903."),

    tc("リクエスト一括操作", "MSG-001", "Normal",
       "Từ chối hàng loạt キャンセルリクエスト — quay về 予約確定, KHÔNG xóa remind",
       CAL + "\n- Có 3 booking đang ở キャンセルリクエスト; đã có remind trong event_step_time",
       "1. Tick 3 booking → chọn「キャンセルリクエストを否認する」+ 実行する → thực thi\n"
       "2. Kiểm tra status + tin nhắn + `event_step_time`\n3. Lặp lại với 実行しない",
       "3 booking request cancel",
       "- 3 booking quay về「予約確定」\n- Action gửi theo cấu hình; 実行しない → không gửi\n"
       "- Remind trong `event_step_time` KHÔNG bị xóa",
       note="Nguồn: Quản lý calendar r904-r911."),

    tc("リクエスト一括操作", "BULK-001", "Abnormal",
       "Chọn lẫn booking không phù hợp với thao tác → bỏ qua booking đó",
       CAL + "\n- Tick 5 booking gồm: 2 booking 予約リクエスト và 3 booking 予約確定",
       "1. Chọn thao tác「新規予約リクエストを承認する」+ 実行する → thực thi\n"
       "2. Kiểm tra status của cả 5 booking\n3. Kiểm tra tin nhắn LINE của 3 chủ booking 予約確定",
       "5 booking hỗn hợp",
       "- 2 booking 予約リクエスト chuyển「予約確定」\n"
       "- 3 booking 予約確定 giữ nguyên trạng thái, KHÔNG bị đổi\n"
       "- KHÔNG gửi action cho 3 booking bị bỏ qua",
       note="Nguồn: Quản lý calendar r913."),

    tc("リクエスト一括操作", "BULK-001", "Normal",
       "Thao tác hàng loạt ở trang 2, 3, 4 vẫn hoạt động bình thường",
       CAL + "\n- Danh sách có ≥ 4 trang, trang 3 có booking 予約リクエスト",
       "1. Chuyển sang trang 3 → tick 2 booking → 一括操作 → 承認する → thực thi\n"
       "2. Kiểm tra status 2 booking đó",
       "≥ 4 trang dữ liệu",
       "- 2 booking ở trang 3 chuyển「予約確定」bình thường",
       note="Nguồn: Quản lý calendar r916."),

    # ══════════════ 11. Admin thêm booking thủ công ══════════════
    tc("Admin thêm booking thủ công", "FUNC-002", "Abnormal",
       "Không chọn / không nhập tên khách → chặn đăng ký",
       CAL + "\n- Modal「予約追加」đang mở",
       "1. Tìm khách bằng từ khóa không có kết quả → bấm đăng ký\n"
       "2. Chọn chế độ nhập tay nhưng bỏ trống tên → bấm đăng ký",
       "Từ khóa không khớp · tên rỗng",
       "- B1: lỗi「お客様名を選択してください」\n- B2: lỗi「客様名を入力してください」\n"
       "- Không sinh bản ghi `calendar_salon_line_booking`",
       note="Nguồn: Quản lý calendar r1024, r1127."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Normal",
       "Dropdown コース: default, thứ tự, ẩn course OFF, không chọn vẫn book được",
       CAL + "\n- Modal「予約追加」đang mở; có 3 course (1 course OFF, 1 course không có system_name)",
       "1. Quan sát giá trị mặc định\n2. Mở dropdown → đối chiếu thứ tự và nội dung\n"
       "3. Không chọn course → đăng ký booking",
       "3 course như mô tả",
       "- Mặc định「選択してください」\n- Thứ tự khớp màn QL course; hiện tên quản lý course\n"
       "- Course OFF KHÔNG hiện; course không có system_name thì hiện course_name\n"
       "- Không chọn course: vẫn booking thành công, phần thông tin course hiện「指定なし」",
       note="Nguồn: Quản lý calendar r1026-r1028."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Normal",
       "Dropdown スタッフ: ẩn staff OFF nhưng VẪN hiện staff không thực hiện course",
       CAL + "\n- Modal「予約追加」đang mở; có S1 (thực hiện course C1), S2 (KHÔNG thực hiện C1), "
             "S3 (đang OFF)",
       "1. Chọn course C1 → mở dropdown staff\n2. Không chọn staff → đăng ký\n3. Chọn S1 → đăng ký",
       "3 staff như mô tả",
       "- Dropdown hiện S1 và S2 (staff không thực hiện course vẫn hiện để admin book được), "
       "KHÔNG hiện S3 (đang OFF)\n"
       "- Không chọn staff: booking vào 指定なし\n- Chọn S1: booking gán cho S1",
       note="Nguồn: Quản lý calendar r1030-r1033. ⚠ Corpus đánh dấu NG cho「hiển thị tên quản lý staff」→ "
            "cần verify lại cột tên hiển thị trong dropdown."),

    tc("Admin thêm booking thủ công", "FUNC-DATE-001", "Abnormal",
       "Validate ngày giờ của booking thủ công",
       CAL + "\n- Modal「予約追加」đang mở",
       "1. Bỏ trống ngày → đăng ký\n2. Nhập ngày quá khứ\n3. Nhập ngày hôm nay + giờ đã qua\n"
       "4. Bỏ trống giờ → đăng ký\n5. Nhập giờ kết thúc < giờ bắt đầu\n"
       "6. Nhập giờ kết thúc = giờ bắt đầu\n7. Nhập giờ kết thúc > giờ bắt đầu",
       "Các mốc ngày giờ như mô tả",
       "- B1, B4: lỗi「予約日時を入力してください。」\n"
       "- B2: lỗi「過去の日付は選択できません。」\n- B3: VẪN booking được\n"
       "- B5, B6: lỗi「開始時間は終了時間よりも前の時間を設定して下さい」\n- B7: thành công",
       note="Nguồn: Quản lý calendar r1036-r1045."),

    tc("Admin thêm booking thủ công", "FUNC-DATE-001", "Normal",
       "Checkbox コース所要時間を基準に終了時間を設定 điều khiển ô giờ kết thúc",
       CAL + "\n- Modal「予約追加」đang mở; course C1 = 60 phút",
       "1. Quan sát trạng thái mặc định của checkbox và ô giờ kết thúc\n"
       "2. Chọn course C1, đặt giờ bắt đầu 10:00 → quan sát giờ kết thúc\n"
       "3. Bỏ tick checkbox → quan sát ô giờ kết thúc\n"
       "4. Không chọn course, giữ tick → quan sát giờ kết thúc",
       "Course 60 phút · `calendar_salon.time_make_course`",
       "- Mặc định TICK; ô giờ kết thúc bị disable\n- Có course: tự tính 11:00\n"
       "- Bỏ tick: ô giờ kết thúc enable, nhập tay được\n"
       "- Không chọn course: tự tính theo `time_make_course` của calendar",
       note="Nguồn: Quản lý calendar r1035, r1046-r1047."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Câu hỏi friend info hiển thị và lưu đúng khi admin book",
       CAL + "\n- Modal「予約追加」đang mở\n- Calendar mới tạo có sẵn 2 item mặc định: system name + email",
       "1. Calendar KHÔNG bật item nào → book\n"
       "2. Calendar có 2 item mặc định → điền → book\n"
       "3. Kiểm tra `calendar_salon_line_booking.friend_info` và bảng friend info của khách",
       "2 item mặc định",
       "- B1: booking bình thường, không hiện câu hỏi\n"
       "- B2: hiện đủ câu hỏi; sau khi book, dữ liệu lưu vào friend info tương ứng của khách",
       note="Nguồn: Quản lý calendar r1048-r1050."),

    tc("Admin thêm booking thủ công", "FUNC-003", "Abnormal",
       "Validate 短文回答 theo 4 kiểu ràng buộc khi admin book",
       CAL + "\n- Modal「予約追加」đang mở\n"
             "- Có 4 câu hỏi 短文回答 với validate: カナ入力 · 電話番号(11桁) · メールアドレス · 整数",
       "1. Ô カナ: nhập katakana → nhập chữ latinh\n"
       "2. Ô điện thoại: nhập 10 số → 12 số → 11 số → nhập chữ\n"
       "3. Ô email: nhập đúng format (kể cả có dấu +) → nhập sai format\n"
       "4. Ô số nguyên: nhập số nguyên → nhập chữ\n5. Book và kiểm tra friend info",
       "カタカナ · 0901234567 · 090123456789 · 09012345678 · a+b@test.com · abc · 100",
       "- カナ sai: lỗi「カナのみ入力してください。」\n"
       "- Điện thoại 10 hoặc 12 số: lỗi「携帯電話11桁の数値を入力してください。」; 11 số: pass\n"
       "- Email sai: lỗi「Emailフォーマットが不正なメールアドレスです。フォーマットを確認してください。」\n"
       "- Số nguyên sai: lỗi「数値のみ入力してください。」\n"
       "- Giá trị hợp lệ: lưu đúng vào friend info tương ứng",
       note="Nguồn: Quản lý calendar r1051-r1055. ⚠ Corpus ghi chú「Nhập số 10 chữ số => cho pass giống "
            "lesson」ở nhánh điện thoại — hành vi chưa thống nhất, xem MT-11."),

    tc("Admin thêm booking thủ công", "FUNC-003", "Abnormal",
       "Câu hỏi bắt buộc bỏ trống → chặn; không bắt buộc thì bỏ trống vẫn qua",
       CAL + "\n- Modal「予約追加」đang mở; có 1 câu hỏi bắt buộc và 1 câu hỏi không bắt buộc",
       "1. Bỏ trống câu hỏi KHÔNG bắt buộc → đăng ký\n2. Bỏ trống câu hỏi BẮT BUỘC → đăng ký",
       "2 câu hỏi",
       "- B1: đăng ký thành công\n- B2: lỗi「回答を入力してください」, không tạo booking",
       note="Nguồn: Quản lý calendar r1056-r1058."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Đích lưu câu trả lời theo 3 kiểu liên kết friend info",
       CAL + "\n- Modal「予約追加」đang mở\n"
             "- 3 câu hỏi: (a) không gắn friend info · (b) tự tạo friend info · (c) gắn friend info có sẵn",
       "1. Điền cả 3 câu hỏi → đăng ký booking\n"
       "2. Kiểm tra `calendar_salon_line_booking.friend_info`\n"
       "3. Kiểm tra bảng `friend_information_value` của khách",
       "3 câu hỏi 3 kiểu liên kết",
       "- (a): chỉ lưu trong `friend_info` của booking, KHÔNG ghi vào friend info nào\n"
       "- (b): tự tạo friend info mới và gán giá trị\n"
       "- (c): gán vào đúng friend info admin đã chọn",
       note="Nguồn: Quản lý calendar r1059-r1061, r1070-r1072, r1078-r1080."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Abnormal",
       "Câu hỏi 日時 có kèm giờ → KHÔNG gán được vào friend info nào",
       CAL + "\n- Có 1 câu hỏi kiểu 日時 CÓ giờ và 1 câu hỏi 日時 KHÔNG giờ",
       "1. Vào cài đặt câu hỏi 日時 có giờ → thử chọn đích liên kết friend info\n"
       "2. Với câu hỏi 日時 không giờ → chọn 3 kiểu liên kết → book và đối chiếu",
       "2 câu hỏi kiểu 日時",
       "- Câu hỏi 日時 CÓ giờ: không thể gán vào bất kỳ friend info nào trong hệ thống\n"
       "- Câu hỏi 日時 KHÔNG giờ: gán được theo cả 3 kiểu như câu hỏi thường",
       note="Nguồn: Quản lý calendar r1090-r1093."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Option すでに情報が登録されている場合、自動入力する điều khiển tự điền friend info",
       CAL + "\n- Modal「予約追加」đang mở\n"
             "- Khách F1 đã có dữ liệu friend info, khách F2 chưa có",
       "1. BỎ tick option, nhưng ở cài đặt form đang BẬT「すでに友だち情報が登録されている場合、"
       "初めから入力された状態にする」→ chọn F1\n"
       "2. BỎ tick option và cài đặt form đang TẮT → chọn F1\n"
       "3. TICK option + cài đặt form TẮT → chọn F1\n4. TICK option → chọn F2\n"
       "5. Tick → bỏ tick → tick lại\n6. Tick option → chọn F1 rồi chọn F2",
       "F1 có dữ liệu · F2 chưa có dữ liệu",
       "- B1: VẪN tự điền\n- B2: KHÔNG điền\n- B3: tự điền\n- B4: không điền gì\n"
       "- B5: tick → điền, bỏ tick → xóa dữ liệu đã điền, tick lại → điền lại\n"
       "- B6: hiển thị đúng thông tin của từng khách khi đổi",
       note="Nguồn: Quản lý calendar r1095-r1100."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Option 自動入力 mặc định LUÔN được tick (Support #28264)",
       CAL,
       "1. Mở modal「予約追加」lần 1 → quan sát option\n"
       "2. Đóng, mở lại lần 2 → quan sát\n"
       "3. Chuyển qua lại giữa 2 lựa chọn khách (エルメ上に表示されている / chưa kết bạn) → quan sát",
       "-",
       "- Cả 3 lần: option「すでに情報が登録されている場合、自動入力する」luôn được tick sẵn\n"
       "- Ở lựa chọn khách chưa kết bạn / không có trên エルメ: option KHÔNG hiển thị",
       note="Nguồn: Quản lý calendar r3312-r3315 (Support #28264, 02/2025)."),

    tc("Admin thêm booking thủ công", "MSG-003", "Normal",
       "Action khi admin thêm booking theo 5 cấu hình",
       CAL + "\n- Modal「予約追加」đang mở, đã chọn khách F1",
       "1. Không set message, không set multi action → book với 実行する\n"
       "2. Set message + có sử dụng → book\n3. Set message + chọn không sử dụng → book\n"
       "4. Chỉ set multi action → book\n5. Set cả message + multi action → book",
       "5 cấu hình action",
       "- B1: không gửi gì\n- B2: gửi tin nhắn text\n- B3: KHÔNG gửi tin nhắn\n"
       "- B4: chạy multi action\n- B5: gửi tin nhắn + chạy multi action\n"
       "- Verify ở LINE app của F1 và ở chat 1:1 của admin",
       note="Nguồn: Quản lý calendar r1102-r1106, r1109-r1113. RULE-06."),

    tc("Admin thêm booking thủ công", "PAY-CONFIRM-001", "Normal",
       "Alert cảnh báo khi admin book vào course/staff CÓ giá và calendar đang bật 決済",
       CAL + "\n- Calendar đã bật 決済連携\n- course C1 có giá 5,000; course C0 giá 0; "
             "staff S1 có phí 1,000; staff S0 phí 0",
       "1. Book C1 + S1 → bấm lưu\n2. Book C1 + S0 → bấm lưu\n3. Book C0 + S1 → bấm lưu\n"
       "4. Book C0 + S0 → bấm lưu\n5. Ở calendar TẮT 決済, book C1 + S1 → bấm lưu\n"
       "6. Ở B1 bấm OK và bấm Hủy trên alert",
       "Course/staff có giá và không giá",
       "- B1, B2, B3: hiện alert「手動での予約追加の場合、本来予約ができない日時やコースの組み合わせでも"
       "強制的に予約が可能となります。また、有料コースの場合でも、お客様に料金は請求されませんが"
       "この予約を登録してよろしいですか？」\n"
       "- B4, B5: KHÔNG hiện alert, booking thành công luôn\n"
       "- B6: OK → tạo booking; Hủy → KHÔNG tạo booking",
       note="Nguồn: Quản lý calendar r1120-r1124."),

    tc("Admin thêm booking thủ công", "FUNC-001", "Normal",
       "Admin book KHÔNG bị chặn bởi mọi ràng buộc đặt lịch",
       CAL + "\n- Modal「予約追加」đang mở",
       "1. Chọn khung giờ staff KHÔNG có ca → book\n"
       "2. Chọn khung giờ staff đã đạt 受付上限 của staff → book\n"
       "3. Chọn khung giờ đã đạt 受付上限 của calendar → book\n"
       "4. Chọn khách đã đạt giới hạn số lần đặt của 1 người → book\n"
       "5. Chọn khung giờ trùng block time sync từ Google → book\n"
       "6. Course đang bật 決済 → book",
       "Các trạng thái chặn như mô tả",
       "- Cả 6 trường hợp: booking THÀNH CÔNG (admin book bỏ qua toàn bộ validate)\n"
       "- Trường hợp 6: KHÔNG bill tiền, không tính phí khách",
       note="Nguồn: Quản lý calendar r1020, r1143-r1148. ⚠ Spec KHÔNG mô tả rule『admin book bỏ qua "
            "validate』→ MT-13."),

    tc("Admin thêm booking thủ công", "CONC-001", "Abnormal",
       "Double-click nút 登録する → chỉ tạo 1 booking",
       CAL + "\n- Modal「予約追加」đã điền đủ dữ liệu hợp lệ",
       "1. Double-click nhanh nút「登録する」\n2. Đếm số bản ghi trong `calendar_salon_line_booking`\n"
       "3. Quan sát lưới calendar",
       "Booking 10:00-11:00 cho F1",
       "- Chỉ 1 booking được tạo\n- Lưới calendar chỉ hiện 1 booking\n"
       "- LINE user chỉ nhận 1 lần action (nếu có)",
       note="Nguồn: Quản lý calendar r1150."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Normal",
       "Bấm X đóng modal thêm booking không lưu gì",
       CAL + "\n- Modal「予約追加」đã điền dữ liệu",
       "1. Bấm icon X\n2. Kiểm tra lưới calendar và DB",
       "Dữ liệu đã điền",
       "- Đóng modal, KHÔNG tạo booking, không thay đổi gì",
       note="Nguồn: Quản lý calendar r1151."),

    tc("Admin thêm booking thủ công", "COMPAT-LEGACY-001", "Normal",
       "Calendar dùng cấu hình form cũ: câu trả lời KHÔNG ghi vào friend_information_value",
       CAL + "\n- Calendar cũ chỉ dùng「form」(2 form mặc định system name + email), không dùng "
             "cấu hình 質問項目 mới",
       "1. Mở modal「予約追加」→ quan sát option 自動入力\n2. Điền form → book\n"
       "3. Kiểm tra `calendar_salon_line_booking.friend_info` và `friend_information_value`\n"
       "4. Chọn 実行する rồi book → kiểm tra `action_lineuser`",
       "Calendar cấu hình form cũ",
       "- KHÔNG có option「すでに情報が登録されている場合、自動入力する」\n"
       "- Dữ liệu CHỈ lưu vào `friend_info` của booking, KHÔNG ghi `friend_information_value`\n"
       "- Dù chọn 実行する hay 実行しない đều KHÔNG chạy action và KHÔNG sinh bản ghi `action_lineuser`",
       note="Nguồn: Quản lý calendar r1131-r1141. Nhánh tương thích ngược của calendar cũ."),

    # ══════════════ 12. Modal lý do không đặt được ══════════════
    tc("Modal lý do không đặt được", "OUT-TRUTH-001", "Normal",
       "Bấm khung giờ không đặt được → mở modal lý do với label và thời gian đúng",
       DAY + "\n- Có khung giờ không thể đặt (staff không có ca)",
       "1. Bấm vào khung 09:00-09:30 của staff không có ca\n2. Quan sát label và dòng thời gian\n"
       "3. Bấm X",
       "Khung 09:00-09:30 ngày 01/10",
       "- Mở modal lý do không đặt được\n- Label: icon +「予約が追加できない日時」\n"
       "- Thời gian: đúng khung đã bấm, format「2024.10.01(日) 09:00~09:30」\n- X: đóng modal",
       note="Nguồn: Quản lý calendar r1166-r1168, r1222."),

    tc("Modal lý do không đặt được", "OUT-TRUTH-001", "Normal",
       "Thứ tự ưu tiên lý do: 0.mùa vụ > 1.không có ca > 2.thời gian nhận > 3.limit calendar > 4.limit staff",
       DAY + "\n- Chuẩn bị các tổ hợp: ngoài mùa vụ + có ca / không ca; trong mùa vụ + không ca + "
             "chưa/quá giờ nhận; có ca + chưa/quá giờ nhận; có ca + đã limit",
       "1. Ngoài mùa vụ, staff CÓ ca → bấm khung\n2. Ngoài mùa vụ, staff KHÔNG ca → bấm khung\n"
       "3. Trong mùa vụ, không ca, chưa đến giờ nhận → bấm khung\n"
       "4. Trong mùa vụ, không ca, đã quá giờ nhận → bấm khung\n"
       "5. Có ca, chưa đến giờ nhận → bấm\n6. Có ca, đã quá giờ nhận → bấm\n"
       "7. Có ca, thỏa giờ nhận, đã limit calendar → bấm",
       "7 tổ hợp trạng thái",
       "- B1, B2: lý do「営業期間外です」(mùa vụ ưu tiên cao nhất)\n"
       "- B3, B4: lý do「予約受付可能なシフトが登録されていません」(không có ca thắng lý do giờ nhận)\n"
       "- B5: lý do chưa đến giờ nhận booking\n- B6: lý do đã quá giờ nhận booking\n"
       "- B7: lý do đã đạt 受付上限 của calendar",
       note="Nguồn: Quản lý calendar r1169-r1178, r1200-r1203, r1242-r1253. "
            "⚠ r1250 ghi「QL tháng NG」ở nhánh không-có-ca + chưa-đến-giờ → cần verify lại lưới tháng."),

    tc("Modal lý do không đặt được", "MSG-004", "Normal",
       "Nội dung lý do 'chưa đến thời gian nhận booking' và hyperlink sang màn cài đặt",
       DAY + "\n- Cài đặt bắt đầu nhận booking trước 1 ngày lúc 15:00; hiện tại 13:00 ngày 31/7",
       "1. Bấm khung giờ có ca của ngày 01/8\n2. Đọc nội dung modal\n3. Bấm hyperlink trong modal",
       "before_booking_day = 1, before_booking_hour = 15:00",
       "- Lý do:「予約の受付を開始していません。予約設定 > 予約・変更・キャンセルのリクエストと締切 > "
       "予約の開始・締め切り より予約受付開始時間をご確認ください。」\n"
       "- Bấm hyperlink: mở đúng màn cài đặt thời gian nhận booking",
       note="Nguồn: Quản lý calendar r1191-r1193, r1221. ⚠ Corpus đánh NG cho nội dung text ở thời điểm "
            "test, đã có yêu cầu đổi text → cần verify text hiện tại trên môi trường."),

    tc("Modal lý do không đặt được", "DATA-COUNT-001", "Boundary",
       "Ma trận limit chung vs limit staff quyết định khung nào bị chặn",
       DAY + "\n- Calendar có S1, S2 và 指定なし",
       "1. limit chung = 2, limit S1 = 1, limit S2 = 1; S1 có 1 booking khung 20:00 → quan sát 指定なし và S2\n"
       "2. limit chung = 1, limit S1 = 2; S1 có 1 booking khung 20:00 → quan sát 指定なし và S2 "
       "(cả khi S2 có ca và không ca)\n"
       "3. limit chung = 1, limit S1 = 1; S1 có 1 booking → quan sát 指定なし và S2",
       "Các tổ hợp limit như mô tả",
       "- B1: 指定なし và S2 VẪN đặt được\n"
       "- B2: 指定なし bị chặn với lý do đã limit calendar; S2 có ca → chặn với lý do limit calendar; "
       "S2 không ca → lý do không có ca\n"
       "- B3: giống B2",
       note="Nguồn: Quản lý calendar r1207-r1213 (ma trận có kết quả khác nhau theo từng ô — "
            "giữ chung 1 TC vì cùng 1 lần dựng cấu hình, ghi rõ kết quả từng ô)."),

    tc("Modal lý do không đặt được", "DATA-COUNT-001", "Normal",
       "Giới hạn số booking đồng thời của 1 người KHÔNG ảnh hưởng hiển thị phía admin",
       DAY + "\n- Cài đặt「1人あたりの予約上限」= 1; khách F1 đã có 1 booking",
       "1. Ở lưới admin, quan sát icon các khung giờ\n2. Bấm 1 khung giờ",
       "limit_book_each_customer = 1",
       "- Icon vẫn hiển thị theo lịch làm việc bình thường\n"
       "- Tùy chọn này CHỈ áp dụng phía LINE user, không có ý nghĩa với admin",
       note="Nguồn: Quản lý calendar r1214."),

    # ══════════════ 13. Detail booking & lịch sử ══════════════
    tc("Detail booking & lịch sử", "UI-001", "Normal",
       "Header detail booking đã approve hiện đủ thông tin và hyperlink tên khách",
       CAL + "\n- Có 1 booking 予約確定 của LINE user F1",
       "1. Mở detail booking\n2. Đối chiếu header\n3. Bấm tên LINE của F1",
       "Booking 予約確定 10:00-11:00 course C1 staff S1",
       "- Header: ảnh course · status「予約確定」· ngày giờ format「2024.10.01(日) 09:00~10:00」· "
       "tên course (kèm thời gian thực hiện) · tên staff · tên khách\n"
       "- Bấm tên khách: mở tab mới màn mypage của F1",
       note="Nguồn: Quản lý calendar r1286-r1287."),

    tc("Detail booking & lịch sử", "FRIEND-001", "Abnormal",
       "Booking của khách bị bot block / bị xóa khỏi hệ thống",
       CAL + "\n- Có booking của khách F2 bị bot block (chưa xóa) và khách F3 đã bị xóa",
       "1. Mở detail booking của F2\n2. Mở màn quản lý, tìm booking của F3\n3. Kiểm tra DB",
       "F2 bị block · F3 đã xóa",
       "- F2: booking vẫn còn, vào được màn mypage bình thường\n"
       "- F3: KHÔNG hiển thị booking trên giao diện nhưng bản ghi vẫn còn trong DB",
       note="Nguồn: Quản lý calendar r1288-r1289."),

    tc("Detail booking & lịch sử", "UI-001", "Normal",
       "Tab お客様情報: hiện câu trả lời friend info theo đúng thứ tự, disable không cho sửa",
       CAL + "\n- Booking có 3 câu trả lời friend info, trong đó 1 câu bỏ trống",
       "1. Mở detail booking → tab「お客様情報」\n2. Đối chiếu thứ tự và nội dung\n3. Thử sửa 1 ô",
       "3 câu hỏi (1 câu trống)",
       "- Hiện lần lượt như thứ tự lúc LINE user đặt lịch\n"
       "- Câu có dữ liệu: hiện đúng nội dung đã điền; câu trống: để trống\n"
       "- Toàn bộ ô bị disable, KHÔNG sửa được",
       note="Nguồn: Quản lý calendar r1294-r1296."),

    tc("Detail booking & lịch sử", "PAY-STATE-001", "Normal",
       "Tab 決済情報: hiện đủ thông tin thanh toán và nút hoàn tiền",
       CAL + "\n- Booking đã thanh toán qua Stripe 5,000 yên",
       "1. Mở detail booking → tab「決済情報」\n2. Đối chiếu từng trường\n3. Bấm「返金する」",
       "Booking đã thanh toán, thẻ test",
       "- 決済システム: hiện stripe / univapay, disable không sửa\n"
       "- Số tiền format「¥ 5,000」· Số thẻ「XXXXXXXX1234」· Hạn thẻ「01/30」\n"
       "- Bấm 返金する: mở màn hoàn tiền",
       note="Nguồn: Quản lý calendar r1298-r1302."),

    tc("Detail booking & lịch sử", "OUT-TRUTH-001", "Normal",
       "Nhãn trạng thái ở tab lịch sử ánh xạ đúng theo status",
       CAL + "\n- Có booking ở đủ các status 0,1,2,3,4,5,6,7",
       "1. Mở tab lịch sử booking của từng booking\n2. Đối chiếu nhãn hiển thị",
       "Booking đủ 8 status",
       "- status 0, 5 →「リクエスト」\n- status 1, 2 →「予約確定」\n- status 3 →「通知受取希望」\n"
       "- status 4, 7 →「キャンセル」\n- status 6 →「否認済」",
       note="Nguồn: Quản lý calendar r1340-r1344."),

    tc("Detail booking & lịch sử", "LIST-001", "Normal",
       "Danh sách 10 booking gần nhất của khách ở tab lịch sử",
       CAL + "\n- Khách F1 có 15 booking (cả quá khứ và tương lai)",
       "1. Mở detail 1 booking của F1 → tab「予約履歴」\n2. Đếm số booking hiển thị\n"
       "3. Tạo thêm 1 booking mới cho F1 → mở lại tab",
       "15 booking của F1",
       "- Chỉ hiện 10 booking gần today nhất (gồm cả quá khứ và tương lai)\n"
       "- Booking mới tạo hiển thị lên đầu\n- Format dòng「2024.09.21 (月) 10:00 ~ 11:00 予約確定 コース名」",
       note="Nguồn: Quản lý calendar r1336-r1339, r2325."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Cột 人thao tác trong lịch sử phân biệt 友だち / スタッフ / 管理者",
       CAL + "\n- Booking có lịch sử do LINE user, staff và admin thao tác",
       "1. Mở tab lịch sử của booking\n2. Đối chiếu cột người thao tác từng dòng\n3. Đối chiếu ngày giờ",
       "3 dòng lịch sử 3 người thao tác",
       "- LINE user: hiện「友だち」\n- Staff và Admin: hiện `username` từ bảng `user`\n"
       "- Ngày giờ format「2024.09.24 (木) 10:31」lấy từ `created_at`",
       note="Nguồn: Quản lý calendar r1312-r1315."),

    tc("Detail booking & lịch sử", "INTG-CAL-001", "Normal",
       "Tab Googleカレンダー同期履歴 ghi đủ 3 loại sự kiện",
       CAL + "\n- Staff S1 đã liên kết Google Calendar; có booking của S1 đã sync",
       "1. Booking chưa liên kết Google → mở tab đồng bộ\n"
       "2. Sau khi liên kết và sync → mở tab\n3. Sửa event trên Google → mở tab\n"
       "4. Xóa event trên Google → mở tab",
       "1 booking của S1",
       "- Chưa liên kết: không có dữ liệu\n"
       "- Sync lên: hiện thời gian +「Googleカレンダーに登録されました」\n"
       "- Sửa trên Google:「Googleカレンダーのスケジュールが変更されました」\n"
       "- Xóa trên Google:「Googleカレンダーからスケジュールが削除されました」\n"
       "- Thời gian format「2024.09.24 (木) 10:31」",
       note="Nguồn: Quản lý calendar r1347-r1350."),

    tc("Detail booking & lịch sử", "MSG-005", "Normal",
       "Duyệt/từ chối request từ màn detail — action theo cấu hình, có bill tiền khi duyệt",
       CAL + "\n- Có 1 booking 予約リクエスト của F1; calendar bật 決済; course C1 có giá 5,000",
       "1. Chọn 実行しない → bấm「承認する」\n"
       "2. Đặt lại cấu hình: message + có sử dụng → 実行する → 承認する\n"
       "3. Cấu hình message + không sử dụng → 承認する\n"
       "4. Cấu hình message + multi action → 承認する\n"
       "5. Với calendar TẮT 決済 và course C1 có giá → 承認する\n"
       "6. Với course C0 giá 0 → 承認する",
       "Booking request · course có/không giá · calendar bật/tắt 決済",
       "- B1: chỉ approve, KHÔNG gửi action\n- B2: gửi message pattern\n"
       "- B3: KHÔNG gửi message\n- B4: gửi message + multi action\n"
       "- Calendar bật 決済 + course có giá: approve và BILL TIỀN\n"
       "- Calendar bật 決済 + course giá 0: chỉ approve\n- Calendar tắt 決済: chỉ approve, KHÔNG bill",
       note="Nguồn: Quản lý calendar r1355-r1365."),

    tc("Detail booking & lịch sử", "MSG-005", "Normal",
       "Từ chối request booking từ màn detail — action riêng của course/staff KHÔNG được dùng",
       CAL + "\n- Có booking 予約リクエスト dùng course C1 và staff S1 đều có action riêng",
       "1. Chọn 実行する → bấm「否認する」\n2. Kiểm tra tin nhắn phía LINE user",
       "Course + staff có action riêng",
       "- Booking chuyển「否認済」\n"
       "- Gửi action CHUNG của booking (deny), KHÔNG dùng action riêng của course/staff",
       note="Nguồn: Quản lý calendar r1371-r1377."),

    tc("Detail booking & lịch sử", "MSG-005", "Normal",
       "Duyệt / từ chối キャンセルリクエスト từ màn detail",
       CAL + "\n- Có booking đang ở キャンセルリクエスト",
       "1. Với 5 cấu hình action, bấm「承認する」→ kiểm tra status + tin nhắn\n"
       "2. Với 5 cấu hình action, bấm「否認する」→ kiểm tra status + tin nhắn",
       "5 cấu hình action",
       "- 承認する: booking chuyển「キャンセル」, action gửi theo cấu hình\n"
       "- 否認する: booking quay về「予約確定」, action gửi theo cấu hình\n"
       "- Chọn 実行しない: KHÔNG gửi action ở cả 2 nhánh",
       note="Nguồn: Quản lý calendar r1366-r1370, r1379-r1383."),

    tc("Detail booking & lịch sử", "UI-001", "Normal",
       "Modal chi tiết từng loại lịch sử hiển thị đúng title và dữ liệu",
       CAL + "\n- Có booking đã trải qua đủ các loại thao tác",
       "1. Mở lần lượt modal chi tiết của: 予約完了 · 予約リクエスト · 予約リクエスト承認 · 予約リクエスト否認 · "
       "手動予約追加 · 予約キャンセル · キャンセルリクエスト · キャンセルリクエスト承認 · キャンセルリクエスト否認 · "
       "手動予約キャンセル · 予約情報の削除\n2. Với mỗi modal, đối chiếu title và dữ liệu\n"
       "3. Bấm tên LINE trong modal\n4. Bấm 閉じる / X",
       "Booking đã trải qua đủ vòng đời",
       "- Title đúng theo từng loại thao tác\n"
       "- Dữ liệu gồm: giờ bắt đầu booking · course · staff · giá tiền · trạng thái thanh toán · "
       "tên LINE · người thao tác · thời gian thao tác\n"
       "- Riêng 手動予約追加: phần giá hiện「手動追加の場合、請求は行われません」\n"
       "- Bấm tên LINE: mở tab mới màn mypage\n- 閉じる/X: đóng modal, về tab lịch sử",
       note="Nguồn: Quản lý calendar r2197-r2282 (gộp ma trận modal cùng bộ trường hiển thị — "
            "liệt kê đủ 11 loại ở Các bước)."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Mã status trong bảng lịch sử ánh xạ đúng nội dung hiển thị",
       CAL + "\n- Có booking đã trải qua đủ các thao tác",
       "1. Với mỗi thao tác, đọc `calendar_salon_line_booking_history_actions.status`\n"
       "2. Đối chiếu với nội dung hiển thị trên UI",
       "Bảng ánh xạ status ↔ nội dung",
       "- 1=予約完了 · 2=予約リクエスト · 4=予約リクエスト承認 · 14=予約リクエスト否認 · 5=手動予約追加 · "
       "6=予約キャンセル · 7=キャンセルリクエスト · 9=キャンセルリクエスト承認 · 15=キャンセルリクエスト否認 · "
       "10=手動予約キャンセル · 11=キャンセル待ち登録 · 12=返金 · 13=予約情報の削除 và 受付枠削除による予約削除",
       note="Nguồn: Quản lý calendar r2311-r2324."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Sau khi duyệt/từ chối từ modal lịch sử → sinh bản ghi mới, bản ghi gốc mất nút thao tác",
       CAL + "\n- Có booking 予約リクエスト",
       "1. Ở tab lịch sử, mở modal của bản ghi 予約リクエスト → bấm 承認する\n"
       "2. Quan sát alert và điều hướng\n3. Mở lại modal của bản ghi GỐC\n"
       "4. Kiểm tra danh sách lịch sử\n5. Lặp lại với 否認する",
       "Booking request",
       "- Hiện alert「※コース・スタッフ別の予約完了時アクションを設定している場合、全体設定の予約（リクエスト承認）"
       "時アクションは稼働しません。」\n"
       "- Đóng popup, quay về tab lịch sử; SINH 1 bản ghi lịch sử mới\n"
       "- Bản ghi GỐC giữ nguyên title「予約リクエスト」nhưng KHÔNG còn phần chọn action và 2 nút duyệt/từ chối",
       note="Nguồn: Quản lý calendar r2208-r2212."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Duyệt キャンセルリクエスト từ modal lịch sử — alert cảnh báo không tự hoàn tiền",
       CAL + "\n- Có booking đã thanh toán, đang ở キャンセルリクエスト",
       "1. Ở tab lịch sử, mở modal キャンセルリクエスト → bấm 承認する\n2. Đọc alert\n"
       "3. Kiểm tra trạng thái thanh toán của booking",
       "Booking đã thanh toán 5,000 yên",
       "- Alert「※すでに決済が完了している場合、キャンセルリクエストを承認しても自動で返金は行われません。"
       "返金が必要な場合は手動で返金を行なってください。」\n"
       "- Booking chuyển キャンセル nhưng `payment_status` KHÔNG đổi (không tự hoàn tiền)",
       note="Nguồn: Quản lý calendar r2238."),

    tc("Detail booking & lịch sử", "OUT-TRUTH-001", "Abnormal",
       "Booking đang ở 予約リクエスト thì LINE user KHÔNG hủy được",
       CAL + "\n- Booking của F1 đang ở 予約リクエスト",
       "1. F1 mở màn lịch sử → mở detail booking\n2. Tìm nút hủy",
       "Booking status 0",
       "- KHÔNG có nút hủy; nếu gọi trực tiếp thì hiện「予約リクエストの取り消しはできません」",
       note="Nguồn: Quản lý calendar r2213 + Booking phía line user r1235."),

    tc("Detail booking & lịch sử", "FUNC-001", "Normal",
       "Detail booking đã cancel: chỉ còn nút xóa booking",
       CAL + "\n- Có booking ở trạng thái キャンセル",
       "1. Mở detail booking đã cancel\n2. Quan sát header và các nút\n3. Bấm「この予約を削除する」",
       "Booking status 4 hoặc 7",
       "- Header: icon + status「キャンセル」\n"
       "- Có nút「この予約を削除する」; bấm → chuyển sang luồng xóa booking\n"
       "- Không có nút hủy nữa",
       note="Nguồn: Quản lý calendar r1390-r1392."),

    # ══════════════ 14. Booking đã xóa ══════════════
    tc("Booking đã xóa", "LIST-001", "Normal",
       "Màn 削除済み予約 hiện danh sách booking đã xóa, có scroll",
       CAL + "\n- Có ≥ 30 booking đã bị xóa",
       "1. Bấm オプション →「削除済み予約」\n2. Quan sát danh sách + scroll\n"
       "3. Bấm 詳細 của 1 booking",
       "≥ 30 booking đã xóa",
       "- Hiện danh sách booking đã xóa, scroll được\n"
       "- Bấm 詳細: mở detail booking đã xóa (chỉ xem, không thao tác được)",
       note="Nguồn: Quản lý calendar r113, r2284-r2292. EP-53."),

    tc("Booking đã xóa", "DATA-AUDIT-001", "Boundary",
       "Booking xóa quá 90 ngày không còn hiển thị ở màn lịch sử xóa",
       CAL + "\n- Có booking có `deleted_at` = hôm nay - 89 ngày và booking `deleted_at` = hôm nay - 91 ngày",
       "1. Mở màn「削除済み予約」\n2. Tìm 2 booking trên",
       "deleted_at 89 ngày và 91 ngày trước",
       "- Booking xóa 89 ngày: VẪN hiển thị\n- Booking xóa 91 ngày: KHÔNG còn hiển thị",
       note="Nguồn: Quản lý calendar r2293. ⚠ Spec KHÔNG có rule retention 90 ngày → MT-14."),

    tc("Booking đã xóa", "UI-001", "Normal",
       "Detail booking đã xóa hiện đủ thông tin thanh toán và 5 trạng thái bill",
       CAL + "\n- Có booking đã xóa: 1 chưa bill, 1 đã bill, 1 không bill, 1 đã refund",
       "1. Mở detail từng booking đã xóa\n2. Đối chiếu vùng thanh toán\n3. Với khách không có friend info",
       "4 booking đã xóa khác payment_status",
       "- Số tiền format「¥ 5,000」· số thẻ「XXXXXXXX1234」· hạn thẻ「01/30」\n"
       "- Trạng thái: 未決済 / 決済成功 / 決済なし / 返金済み / 未返金\n"
       "- Khách không có friend info: để trống phần thông tin",
       note="Nguồn: Quản lý calendar r2295-r2303."),

    tc("Booking đã xóa", "DATA-REF-001", "Normal",
       "Booking bị xóa do xóa ca làm việc hiển thị ở màn booking đã xóa",
       CAL + "\n- Có ca làm việc chứa booking ở trạng thái cho phép xóa ca",
       "1. Xóa ca làm việc đó\n2. Mở màn quản lý theo ngày / tuần / tháng\n"
       "3. Mở màn「削除済み予約」\n4. Mở detail và xem lịch sử",
       "Ca có booking status 2, 4, 6, 7",
       "- Các booking liên quan biến mất khỏi lưới quản lý\n"
       "- Xuất hiện ở màn「削除済み予約」\n"
       "- Lịch sử ghi「受付枠削除による予約削除」(status 13)",
       note="Nguồn: Quản lý calendar r711-r716, r724, r2324. ⚠ Xung đột với Bug #29394 (03/2025) — xem MT-03."),

    # ══════════════ 15. Hoàn tiền 返金 ══════════════
    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Hoàn tiền qua UnivaPay từ エルメ — cả booking user tự approve và admin approve",
       CAL + "\n- Calendar bật 決済 UnivaPay môi trường テスト\n"
             "- Có 2 booking đã thanh toán: 1 do user đặt được approve ngay, 1 do admin approve",
       "1. Mở detail booking 1 → tab 決済情報 → bấm 返金する\n"
       "2. Chọn「この画面から返金を行う」→ tick checkbox xác nhận → bấm 返金する\n"
       "3. Kiểm tra `payment_status`, `refund_type`, lịch sử, và dashboard UnivaPay\n"
       "4. Lặp lại với booking 2",
       "2 booking UnivaPay đã thanh toán 5,000 yên",
       "- Cả 2 booking: `payment_status` = 3, `refund_type` = 'now'\n"
       "- Sinh lịch sử `calendar_salon_line_booking_history_actions.reason` = '¥5,000の返金（エルメから）'\n"
       "- Trên dashboard UnivaPay: giao dịch đã hoàn tiền thành công",
       note="Nguồn: Quản lý calendar r2167-r2168. RULE-07 (verify 3 tầng: DB + màn hình + hệ thống bill)."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Đã hoàn tiền trên UnivaPay rồi hoàn lại từ エルメ → báo lỗi, không đổi trạng thái",
       CAL + "\n- Booking đã được hoàn tiền trực tiếp trên dashboard UnivaPay",
       "1. Mở detail booking → 返金する → chọn hoàn từ エルメ → xác nhận\n"
       "2. Đọc thông báo lỗi\n3. Kiểm tra `payment_status`",
       "Booking đã refund trên UnivaPay",
       "- Lỗi「返金金額が課金金額を超過しています。」\n- `payment_status` KHÔNG đổi",
       note="Nguồn: Quản lý calendar r2169-r2170."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Đã hoàn tiền trên Stripe rồi hoàn lại từ エルメ → hiện lỗi do Stripe trả về",
       CAL + "\n- Calendar bật 決済 Stripe; booking đã refund trực tiếp trên Stripe",
       "1. Mở detail booking → 返金する → chọn hoàn từ エルメ → xác nhận\n"
       "2. Đọc thông báo lỗi\n3. Kiểm tra `payment_status`",
       "Booking đã refund trên Stripe",
       "- Hiện lỗi do Stripe trả về, dạng「Charge ch_xxx has already been refunded.」\n"
       "- `payment_status` KHÔNG đổi",
       note="Nguồn: Quản lý calendar r2184-r2185, r2192."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Chọn 'chỉ đổi trạng thái' — không gọi API hoàn tiền của hệ thống thanh toán",
       CAL + "\n- Có booking đã thanh toán qua Stripe và 1 qua UnivaPay",
       "1. Mở detail booking → 返金する\n"
       "2. Chọn「返金は決済システム管理画面から行い エルメ上のステータスのみ返金済みに変更する」→ "
       "tick xác nhận → bấm 返金する\n"
       "3. Kiểm tra `payment_status` và lịch sử\n4. Kiểm tra dashboard Stripe/UnivaPay",
       "2 booking đã thanh toán",
       "- `payment_status` = 3 (返金済み) trên エルメ\n"
       "- Lịch sử ghi reason có ghi rõ nguồn thao tác「決済システムから操作（Stripe/UnivaPay）」\n"
       "- Trên Stripe/UnivaPay: KHÔNG phát sinh giao dịch hoàn tiền",
       note="Nguồn: Quản lý calendar r2174, r2181, r2188, r2194, r2322."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Không tick checkbox xác nhận → không hoàn tiền được",
       CAL + "\n- Có booking đã thanh toán, màn hoàn tiền đang mở",
       "1. Không tick「返金後の取り消し操作はできないことを確認しました。」\n2. Bấm「返金する」",
       "Booking đã thanh toán",
       "- Nút hoàn tiền không thực thi / hiện lỗi bắt buộc tick checkbox\n"
       "- `payment_status` không đổi",
       note="Nguồn: Quản lý calendar r2176, r2189."),

    tc("Hoàn tiền 返金", "ENV-001", "Normal",
       "Hoàn tiền trên môi trường PRODUCTION với cả Stripe và UnivaPay",
       "- Bot production đã liên kết Stripe / UnivaPay môi trường 本番\n"
       "- Có booking thật đã thanh toán bằng thẻ thật số tiền nhỏ",
       "1. Mở detail booking → 返金する → chọn hoàn từ エルメ → xác nhận\n"
       "2. Kiểm tra `payment_status`, lịch sử\n3. Kiểm tra dashboard nhà cung cấp\n"
       "4. Kiểm tra sao kê thẻ / thông báo hoàn tiền",
       "Booking thật, số tiền nhỏ nhất có thể",
       "- `payment_status` = 3, lịch sử ghi đúng\n"
       "- Giao dịch hoàn tiền xuất hiện trên dashboard nhà cung cấp\n- Khách nhận được hoàn tiền",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar r2177-r2181, r2190-r2194. RULE-08: bill tiền BẮT BUỘC test production."),
]
