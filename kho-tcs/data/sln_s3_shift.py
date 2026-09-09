# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 16-19: ca làm việc (シフト) — thêm/ghi đè, sửa/xóa,
qua ngày & biên 00:00, quản lý bằng CSV.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Quản lý calendar」r1397-r1570 (modal add/edit ca), r2002-r2164 (Bug #32568 hợp nhất ca
    liên tiếp, Bug #32775 import CSV, Bug Tester #34185 xóa ca), r2377-r2501 (logic qua ngày)
  - tab「#38520」(07/2026, 99 TC format phẳng — Bug KH #38519/#38520/#38537 ca chạm nửa đêm,
    KHỐI MỚI NHẤT của tính năng)
  - tab「Setting lịch lv」·「Main case」
"""
from _common import tc

CAL = ("- Đăng nhập admin (主管理者) bot A\n"
       "- Calendar「サロンA」loại スタッフ, staff S1 và S2\n"
       "- Mở /basic/calendar-salon/{id} → tab「予約カレンダー」")
SHIFT = CAL + "\n- Modal「シフト追加」đang mở"

S3 = [
    # ══════════════ 16. Ca làm việc — thêm & ghi đè ══════════════
    tc("Ca làm việc — thêm & ghi đè", "FUNC-001", "Normal",
       "Mở modal シフト追加 từ cả 3 lưới ngày/tuần/tháng",
       CAL,
       "1. Ở lưới ngày bấm「シフト追加」\n2. Ở lưới tuần bấm「シフト追加」\n"
       "3. Ở lưới tháng bấm「シフト追加」\n4. Ở tab シフト (chế độ list) bấm「シフト追加」",
       "-",
       "- Cả 4 lối vào đều mở đúng popup thêm ca làm việc",
       note="Nguồn: Quản lý calendar r88, r580, r622, r752, r1398."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-001", "Abnormal",
       "Không chọn staff / không chọn ngày → chặn lưu",
       SHIFT,
       "1. Không chọn staff → bấm đăng ký\n2. Chọn staff nhưng không chọn ngày → bấm đăng ký",
       "-",
       "- B1: lỗi「スタッフを選択してください」\n- B2: lỗi「日程を選択してください」\n"
       "- Không sinh bản ghi `calendar_salon_time_booking`",
       note="Nguồn: Quản lý calendar r1404, r1408."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-001", "Normal",
       "Dropdown chọn staff: default, thứ tự, ẩn staff OFF",
       SHIFT + "\n- Calendar có S1, S2 (ON) và S3 (OFF)",
       "1. Quan sát giá trị mặc định\n2. Mở dropdown → đối chiếu danh sách và thứ tự\n"
       "3. Với calendar chưa có staff nào → mở dropdown",
       "S1, S2 ON · S3 OFF",
       "- Mặc định「選択してください」\n- Hiện S1, S2 theo đúng thứ tự màn list staff\n"
       "- KHÔNG hiện S3 (đang OFF)\n- Calendar chưa có staff: dropdown rỗng",
       note="Nguồn: Quản lý calendar r1401-r1403."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Abnormal",
       "Không chọn được ngày quá khứ; ngày hôm nay giờ quá khứ vẫn thêm được",
       SHIFT,
       "1. Mở calendar chọn ngày → bấm 1 ngày trong quá khứ\n"
       "2. Chọn ngày hôm nay, nhập giờ đã trôi qua (vd hiện tại 15:00, nhập 09:00-12:00) → lưu\n"
       "3. Chọn nhiều ngày trong đó có cả ngày quá khứ",
       "Ngày quá khứ · giờ quá khứ của hôm nay",
       "- B1: KHÔNG chọn được ngày quá khứ\n- B2: VẪN thêm được ca\n"
       "- B3: chỉ các ngày từ hôm nay trở đi được chọn",
       note="Nguồn: Quản lý calendar r1409-r1410, r1414."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Chọn nhiều ngày, kéo dài qua tuần / qua tháng đều tạo đủ ca",
       SHIFT,
       "1. Chọn nhiều ngày liên tiếp gồm hôm nay và các ngày tương lai → lưu\n"
       "2. Chọn dải ngày kéo từ tuần này sang tuần sau → lưu\n"
       "3. Chọn dải ngày kéo từ tháng này sang tháng sau → lưu\n"
       "4. Đối chiếu số bản ghi `calendar_salon_time_booking` và lưới calendar",
       "5 ngày · dải qua tuần · dải qua tháng",
       "- Tất cả các ngày đã chọn đều có ca hiển thị trên lưới\n"
       "- Số bản ghi DB khớp đúng số ngày × số khung giờ đã nhập",
       note="Nguồn: Quản lý calendar r1413-r1417 + #38520 r40 (TẤT CẢ ngày đã chọn đều có ca, "
            "không chỉ ngày đầu tiên)."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Abnormal",
       "Validate giờ trong modal thêm ca — 5 nhánh lỗi",
       SHIFT,
       "1. Bỏ trống ô giờ → lưu\n2. Nhập số âm / số thập phân\n"
       "3. Nhập giờ bắt đầu = giờ kết thúc (09:00~09:00)\n"
       "4. Nhập 2 khung giờ giống hệt nhau (07:00-12:00 và 07:00-12:00)\n"
       "5. Nhập 2 khung chồng lấn (09:00-11:00 và 10:00-12:00)",
       "Các cặp giờ như mô tả",
       "- B1: báo lỗi\n- B2: chặn không cho nhập\n"
       "- B3: lỗi「開始時間は終了時間よりも前の時間を設定して下さい」\n"
       "- B4: lỗi「重複している時間があります。」\n- B5: báo lỗi chồng lấn",
       note="Nguồn: Quản lý calendar r1419-r1424."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Thêm nhiều khung giờ liền nhau / cách nhau trong cùng 1 ngày",
       SHIFT,
       "1. Nhập 07:00-12:00 và 12:00-18:00 → lưu\n"
       "2. Nhập 08:00-12:00, 13:00-18:00, 19:00-22:00 → lưu\n"
       "3. Kiểm tra lưới calendar và DB",
       "Các khung như mô tả",
       "- B1: tạo thành ca liên tục 07:00-18:00\n"
       "- B2: tạo 3 ca riêng biệt đúng như đã nhập",
       note="Nguồn: Quản lý calendar r1428-r1429. ⚠ Sau Bug #32568 (10/2025) hành vi với 2 khung LIỀN NHAU "
            "đã đổi thành BÁO LỖI yêu cầu gộp — xem TC nhóm này và MT-04."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Abnormal",
       "Bug #32568: 2 khung giờ LIỀN NHAU phải báo lỗi yêu cầu gộp",
       SHIFT + "\n- Staff S1 CHƯA có ca ngày 11/07",
       "1. Nhập 2 khung 15:00-15:30 và 15:30-16:00 → lưu\n"
       "2. Nhập 15:00-15:30 và 15:20-16:00 → lưu\n"
       "3. Nhập 23:30-00:00 và 00:00-00:30 → lưu\n"
       "4. Nhập 23:30-00:30 và 00:01-01:00 → lưu",
       "Các cặp khung liền nhau / chồng nhau",
       "- Cả 4 trường hợp: lỗi「シフトの時間が連続する場合は、合算して登録してください"
       "（例：13:00~14:30 14:30~15:00の場合、13:00~15:00に合算してください）」\n"
       "- KHÔNG tạo ca nào",
       note="Nguồn: Quản lý calendar r2002-r2005 (Bug #32568, 27/10/2025 — khối MỚI HƠN r1428)."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Boundary",
       "Bug #32568: khung CÁCH NHAU tối thiểu 1 phút thì tạo được 2 ca",
       SHIFT + "\n- Staff S1 chưa có ca ngày 11/07",
       "1. Nhập 15:00-15:29 và 15:30-16:00 → lưu\n2. Nhập 23:30-23:59 và 00:00-00:30 → lưu\n"
       "3. Nhập 23:30-00:29 và 00:30-01:00 → lưu\n4. Nhập 23:30-00:30 và 00:25-01:00 → lưu",
       "Các cặp khung cách nhau như mô tả",
       "- B1, B2, B3: tạo được 2 ca riêng biệt\n"
       "- B4: tạo 2 ca, trong đó ca 00:25-01:00 được gán cho CHÍNH ngày hôm đó (không phải ca qua ngày)",
       note="Nguồn: Quản lý calendar r2007-r2010."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Ghi đè: staff đã có ca, thêm ca chồng lấn → xóa ca cũ, tạo ca mới",
       SHIFT + "\n- S1 đã có ca ngày 11/07 15:00-15:30",
       "1. Thêm ca 15:25-16:00 cho cùng ngày → lưu\n2. Kiểm tra lưới và DB\n"
       "3. Với S1 đã có ca 23:30-00:00, thêm 23:50-00:30 → lưu\n"
       "4. Với S1 có 2 ca 10:00-11:00 và 11:15-12:15, thêm 10:59-11:16 → lưu",
       "Các tổ hợp ca cũ/mới như mô tả",
       "- B1: ca cũ bị xóa, kết quả còn ca 15:25-16:00\n"
       "- B3: kết quả còn ca 23:50-00:30\n- B4: kết quả còn ca 10:59-11:16\n"
       "- DB chỉ còn bản ghi ca mới, không có 2 ca chồng nhau",
       note="Nguồn: Quản lý calendar r2018-r2020 (SpecChange #28381 — merge time đổi thành GHI ĐÈ)."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Abnormal",
       "Ghi đè bị CHẶN khi phần bị cắt còn booking 予約確定",
       SHIFT + "\n- S1 đã có ca ngày 11/07 15:00-15:30\n- Có booking「予約確定」15:00-15:30",
       "1. Thêm ca 15:25-16:00 cho cùng ngày → lưu\n2. Đọc thông báo lỗi\n3. Kiểm tra ca cũ và booking",
       "Ca 15:00-15:30 + booking 予約確定 trong ca",
       "- Lỗi「上書き（短縮）するシフトの中に「ステータス：予約確定」の予約が1つ以上残っています。"
       "シフトを上書き（短縮）する場合、短縮されるシフトに対しての予約が全て「ステータス：キャンセル」に"
       "なっている必要があります。」\n"
       "- Ca cũ giữ nguyên 15:00-15:30, booking không bị ảnh hưởng",
       note="Nguồn: Quản lý calendar r2024, r2048 + #38520 r4."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Ghi đè chỉ ảnh hưởng ngày/staff được chọn, ngày trùng thì skip",
       SHIFT + "\n- S1 đã có ca ngày 11/07 09:00-12:00; S2 chưa có ca",
       "1. Thêm ca 09:00-12:00 cho S1 vào đúng ngày 11/07 → lưu\n"
       "2. Thêm ca giờ khác cho S1 vào đúng ngày 11/07 → lưu\n"
       "3. Thêm ca cùng giờ cho S1 vào ngày 12/07 → lưu\n"
       "4. Chọn nhiều ngày trong đó có ngày đã có ca → lưu\n"
       "5. Thêm ca trùng giờ cho S2 → lưu",
       "Ca cũ của S1 ngày 11/07",
       "- B1, B2, B3, B5: thành công\n"
       "- B4: ngày đã có ca thì skip, ngày chưa có thì insert\n"
       "- Ca của S2 không ảnh hưởng ca của S1",
       note="Nguồn: Quản lý calendar r1439-r1443."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Checkbox 休業日として設定する: disable ô giờ, ngày thành ngày nghỉ",
       SHIFT,
       "1. Quan sát trạng thái mặc định\n2. Tick「休業日として設定する」→ quan sát các ô giờ\n"
       "3. Chọn 2 ngày → lưu\n4. Kiểm tra lưới calendar và phía LINE user",
       "2 ngày set nghỉ",
       "- Mặc định KHÔNG tick, thêm ca bình thường\n- Tick: các ô giờ bị disable\n"
       "- 2 ngày đã chọn hiển thị「休業日」trên lưới\n- LINE user KHÔNG chọn được 2 ngày đó",
       note="Nguồn: Quản lý calendar r1436-r1437 + #38520 r20. RULE-06 (đi tới output cuối = LIFF)."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Abnormal",
       "Đặt ngày nghỉ vào ngày đã có booking 予約確定 → chặn với message riêng",
       CAL + "\n- Ngày 11/07 có booking「予約確定」của LINE user",
       "1. Mở「シフト追加」→ chọn ngày 11/07 → tick 休業日 → lưu\n"
       "2. Mở modal EDIT ca của ngày 11/07 → tick 休業日 → lưu",
       "Booking 予約確定 ngày 11/07",
       "- Cả 2 lối vào: lỗi「「ステータス：予約確定」の予約が1つ以上残っています。休業日に変更する場合、"
       "該当する日付にに対する全ての予約が「ステータス：キャンセル」になっている必要があります。」\n"
       "- Ngày 11/07 KHÔNG chuyển thành ngày nghỉ",
       note="Nguồn: Quản lý calendar r539-r540, r1862-r1863 (Support #27066). "
            "⚠ Text lỗi trong corpus có lỗi chính tả「日付にに対する」— cần đối chiếu bản JP thật."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-DATE-001", "Normal",
       "Đặt ngày nghỉ vào ngày có booking ở trạng thái KHÔNG chặn",
       CAL + "\n- Ngày 12/07 chỉ có booking: đợi thông báo (status 3) · bị deny (6) · "
             "user đã cancel (4) · admin cancel (7) · admin book (2)",
       "1. Mở modal edit ca ngày 12/07 → tick 休業日 → lưu\n2. Kiểm tra lưới calendar",
       "5 booking như mô tả",
       "- Lưu thành công, ngày 12/07 chuyển thành ngày nghỉ",
       note="Nguồn: Quản lý calendar r1451-r1455."),

    tc("Ca làm việc — thêm & ghi đè", "UI-INPUT-001", "Normal",
       "Nút +追加 và icon xóa khung giờ trong modal",
       SHIFT,
       "1. Bấm「+追加」→ quan sát\n2. Bấm icon xóa của khung vừa thêm\n"
       "3. Khi chỉ còn 1 khung → quan sát icon xóa",
       "-",
       "- +追加: hiện thêm 1 dòng khung giờ ở cuối\n- Icon xóa: xóa đúng dòng tương ứng\n"
       "- Chỉ còn 1 khung: KHÔNG hiển thị icon xóa",
       note="Nguồn: Quản lý calendar r1434-r1435 + SpecImprove #33147 r1475-r1476."),

    tc("Ca làm việc — thêm & ghi đè", "UI-001", "Normal",
       "SpecImprove #33147: icon xóa hiện khi có ≥ 2 ca, ẩn khi còn 1 ca",
       CAL + "\n- Staff S1 ngày 11/07 có 1 ca 09:00-14:00",
       "1. Mở modal EDIT ca → quan sát icon xóa\n"
       "2. Thêm ca thứ 2 15:00-20:00 → quan sát icon xóa của cả 2 dòng\n"
       "3. Thêm ca thứ 3 → quan sát\n4. Xóa 1 ca → còn 2 ca → quan sát\n"
       "5. Xóa tiếp 1 ca → còn 1 ca → quan sát",
       "1 → 2 → 3 → 2 → 1 ca",
       "- 1 ca: KHÔNG hiện icon xóa\n- 2 ca: icon xóa hiện ở CẢ 2 dòng\n"
       "- 3 ca: icon xóa hiện ở tất cả các dòng\n- Xóa về còn 1 ca: icon xóa biến mất",
       note="Nguồn: Quản lý calendar r1475-r1484, r1503-r1506 (SpecImprove #33147, 21/10/2025). "
            "Áp dụng cho cả calendar staff, private, và app mobile."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-MULTI-001", "Normal",
       "Thêm ca theo 曜日 (thứ trong tuần) áp dụng cho mọi tuần",
       CAL,
       "1. Mở tab thêm ca theo thứ → chọn thứ 7 → nhập 19:00-24:00 → lưu\n"
       "2. Quan sát lưới ngày / tuần / tháng / tab list các tuần kế tiếp\n"
       "3. Chọn 2 thứ cùng lúc (thứ 2 và thứ 4) → lưu → kiểm tra",
       "Thứ 7 19:00-24:00 · thứ 2 + thứ 4",
       "- Mọi thứ 7 trên calendar đều hiện ca 19:00-24:00 (kể cả tuần kế tiếp)\n"
       "- Giờ kết thúc 24:00 được lưu đúng\n"
       "- Chọn 2 thứ: CẢ 2 thứ đều được áp dụng ở mọi tuần, không sót thứ thứ 2",
       note="Nguồn: Quản lý calendar r1797, r1803 + #38520 r17, r40."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-MULTI-001", "Normal",
       "Ca theo 曜日 ghi đè ca theo ngày cụ thể đã có",
       CAL + "\n- Ngày 18/07/2026 (thứ 7) đã có ca riêng 10:00-15:00",
       "1. Thêm ca theo 曜日 thứ 7 = 19:00-24:00 → lưu\n2. Quan sát ngày 18/07 và DB",
       "Ca riêng 10:00-15:00 ngày 18/07",
       "- Ca ngày 18/07 bị GHI ĐÈ thành 19:00-24:00 (đúng như cảnh báo)\n"
       "- KHÔNG tạo bản ghi trùng, không sinh 2 ca chồng nhau trên cùng ngày",
       note="Nguồn: #38520 r19."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-MULTI-001", "Normal",
       "Sửa ca theo 曜日 khi ngày hôm sau có booking kết thúc 00:00 → không bị chặn nhầm",
       CAL + "\n- Ca theo 曜日 thứ 7 = 19:00-24:00; ca Chủ nhật kế tiếp = 19:00-24:00\n"
             "- Chủ nhật có booking「予約確定」22:00-00:00",
       "1. Sửa ca theo 曜日 thứ 7 thành 19:00-23:00 → lưu\n2. Kiểm tra ca thứ 7 và booking Chủ nhật",
       "Booking Chủ nhật 22:00-00:00",
       "- Lưu thành công, KHÔNG báo lỗi 上書き（短縮）…\n"
       "- Ca thứ 7 cập nhật đúng 19:00-23:00\n- Booking Chủ nhật không bị ảnh hưởng",
       note="Nguồn: #38520 r18 (Bug KH #38519, 07/2026)."),

    tc("Ca làm việc — thêm & ghi đè", "CONC-002", "Abnormal",
       "Double-click nút 登録する → chỉ tạo 1 ca",
       SHIFT + "\n- Đã điền đủ dữ liệu hợp lệ",
       "1. Double-click nhanh nút「登録する」\n2. Đếm bản ghi `calendar_salon_time_booking`\n"
       "3. Quan sát lưới calendar",
       "Ca 10:00-18:00 ngày 11/07",
       "- Chỉ 1 ca được tạo (DB có đúng 1 row)\n- Lưới không hiển thị 2 ca chồng nhau\n"
       "- Nút bị disable sau click đầu hoặc request thứ 2 bị chặn",
       note="Nguồn: #38520 r42."),

    tc("Ca làm việc — thêm & ghi đè", "SEC-001", "Abnormal",
       "Validate giờ ở CẢ frontend và server",
       SHIFT,
       "1. Nhập giờ sai định dạng ở UI → quan sát\n"
       "2. Dùng công cụ dev gọi trực tiếp API `add-work-schedule` với giá trị giờ sai định dạng\n"
       "3. Kiểm tra bảng `calendar_salon_time_booking`",
       "Giờ sai định dạng (vd「25:70」,「abc」)",
       "- FE: hiển thị lỗi validation rõ ràng, không cho lưu\n"
       "- Gọi API trực tiếp: server CŨNG chặn, trả lỗi\n- KHÔNG có bản ghi rác trong DB",
       note="Nguồn: #38520 r38. EP-19."),

    tc("Ca làm việc — thêm & ghi đè", "PERF-LARGE-001", "Boundary",
       "Chọn nhiều ngày ở mức biên và biên+1 của giới hạn số lượng",
       SHIFT,
       "1. Chọn số ngày = đúng giá trị biên cho phép → lưu\n"
       "2. Chọn số ngày = biên + 1 → lưu\n3. Kiểm tra DB sau mỗi lần",
       "Số ngày ở mức biên (xác định từ spec/impl trước khi test)",
       "- Ở đúng biên: lưu thành công, đủ số ca\n"
       "- Vượt biên: chặn rõ ràng bằng thông báo lỗi, KHÔNG lưu một phần (không có ca lẻ trong DB)",
       spec="Đã hỏi leader",
       note="Nguồn: #38520 r39. ⚠ Giá trị biên cụ thể chưa có trong spec — cần Leader xác nhận, xem MT-15."),

    tc("Ca làm việc — thêm & ghi đè", "UI-INPUT-001", "Normal",
       "Ô 出勤時間 nhận paste bằng cả hotkey và chuột phải, tự trim khoảng trắng",
       SHIFT,
       "1. Copy chuỗi「 10:00 」(có khoảng trắng đầu/cuối)\n"
       "2. Paste vào ô giờ bằng Ctrl+V → quan sát nút 登録する\n"
       "3. Paste bằng chuột phải → Paste → quan sát\n4. Lưu và kiểm tra DB",
       "Chuỗi「 10:00 」",
       "- Cả 2 cách paste đều được nhận, nút「登録する」enable đúng, validation kích hoạt\n"
       "- Khoảng trắng đầu/cuối bị trim, DB lưu「10:00」",
       note="Nguồn: #38520 r59."),

    tc("Ca làm việc — thêm & ghi đè", "FUNC-SEQ-001", "Abnormal",
       "Chuỗi thao tác liên tiếp + reload xen giữa không làm hỏng dữ liệu ca",
       CAL + "\n- S1 chưa có ca ngày 11-13/07",
       "1. Thêm ca 11/07 → F5 → sửa ca → F5 → xóa ca → F5\n"
       "2. Thêm ca 12/07 → thêm tiếp ca 13/07 → F5 → xóa cả 2 → F5\n"
       "3. Sau mỗi bước: đối chiếu lưới calendar với DB và quan sát console trình duyệt",
       "Chuỗi thao tác trên 3 ngày",
       "- Mọi chuỗi cho kết quả đúng; trạng thái sau F5 GIỐNG HỆT trạng thái ngay sau thao tác\n"
       "- KHÔNG có lỗi JS/console\n- Sau reload không mất ca, không sinh ca thừa",
       note="Nguồn: #38520 r41."),

    # ══════════════ 17. Ca làm việc — sửa & xóa ══════════════
    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Normal",
       "Modal edit ca hiện đúng ngày và trạng thái đã set",
       CAL + "\n- Ngày 01/10 của S1 đã có ca 09:00-18:00",
       "1. Mở modal edit ca của ngày 01/10\n2. Đọc dòng ngày\n"
       "3. Mở modal của ngày đã set 24h\n4. Mở modal của ngày đã set nghỉ\n5. Bấm X",
       "3 ngày ở 3 trạng thái",
       "- Dòng ngày format「2024.10.01(日)」\n- Hiện đúng giờ bắt đầu - kết thúc\n"
       "- Ngày 24h: tick sẵn 24h\n- Ngày nghỉ: tick sẵn ngày nghỉ\n"
       "- Bấm X: đóng popup, KHÔNG lưu thay đổi",
       note="Nguồn: Quản lý calendar r1445, r1447, r1467."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Abnormal",
       "Sửa giờ ca đang có booking của LINE user ở trạng thái chặn",
       CAL + "\n- Ca 09:00-18:00 của S1 ngày 11/07 có booking LINE user",
       "1. Booking đang 予約リクエスト (status 0) → sửa giờ ca → lưu\n"
       "2. Booking đã 予約確定 (status 1) → sửa giờ ca → lưu\n"
       "3. Booking đang キャンセルリクエスト (status 5) → sửa giờ ca → lưu",
       "3 trạng thái booking",
       "- Cả 3 trường hợp: hiện thông báo và KHÔNG cho sửa\n"
       "- Ca giữ nguyên giờ cũ",
       note="Nguồn: Quản lý calendar r1459-r1461, r2436-r2438."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Normal",
       "Sửa giờ ca khi booking ở trạng thái KHÔNG chặn",
       CAL + "\n- Ca của S1 ngày 12/07 có booking: admin book (2) · đợi thông báo (3) · deny (6) · "
             "user cancel (4) · admin cancel (7)",
       "1. Sửa giờ ca thành hợp lệ → lưu\n2. Kiểm tra ca và các booking",
       "5 booking như mô tả",
       "- Lưu thành công\n- Các booking vẫn giữ nguyên, không bị xóa",
       note="Nguồn: Quản lý calendar r1458, r1462-r1465."),

    tc("Ca làm việc — sửa & xóa", "DATA-REF-001", "Abnormal",
       "Xóa ca còn booking 予約確定 → chặn với message xóa ca",
       CAL + "\n- Ca S1 ngày 11/07 19:00-24:00 có booking「予約確定」20:00-21:00",
       "1. Ở tab シフト tick ca đó → bấm「一括シフト削除」\n2. Đọc message\n"
       "3. Kiểm tra DB `calendar_salon_time_booking`",
       "Ca có booking 予約確定",
       "- Lỗi「削除するシフトの中に「ステータス：予約確定」の予約が1つ以上残っています。シフトを削除する場合、"
       "選択したシフトに対する全ての予約が「ステータス：キャンセル」になっている必要があります。」\n"
       "- Ca KHÔNG bị xóa, bản ghi vẫn còn trong DB",
       note="Nguồn: Quản lý calendar r717-r722 + #38520 r6, r83."),

    tc("Ca làm việc — sửa & xóa", "DATA-REF-001", "Normal",
       "Xóa ca chưa có booking → confirm rồi xóa thành công",
       CAL + "\n- Ca S1 ngày 11/07 10:00-18:00 KHÔNG có booking nào",
       "1. Tick ca → bấm「一括シフト削除」\n2. Đọc message confirm → bấm OK\n"
       "3. Kiểm tra lưới calendar và DB\n4. Kiểm tra phía LINE user",
       "Ca không booking",
       "- Message confirm「選択されたシフトを全て削除しますがよろしいですか？」\n"
       "- Xóa thành công: ca biến mất khỏi lưới, `calendar_salon_time_booking` không còn bản ghi\n"
       "- LINE user không còn slot ở ca đó",
       note="Nguồn: Quản lý calendar r709 + #38520 r85."),

    tc("Ca làm việc — sửa & xóa", "DATA-REF-001", "Normal",
       "Xóa nhiều ca cùng lúc, ở trang khác trang 1, và qua nhiều tháng",
       CAL + "\n- Có ca của S1 và S2 ở nhiều ngày, nhiều tháng, nhiều trang",
       "1. Tick nhiều ca chưa có booking (2 staff, 2 ngày) → xóa\n"
       "2. Chuyển sang trang 2 → tick ca → xóa\n3. Tick ca thuộc 2 tháng khác nhau → xóa\n"
       "4. Trong mỗi trường hợp, thử với ca còn booking 予約確定",
       "Ca của 2 staff ở nhiều ngày/tháng/trang",
       "- Ca chưa booking hoặc booking ở trạng thái cho phép: xóa thành công\n"
       "- Ca còn booking 予約確定: chặn với message xóa ca\n"
       "- Số bản ghi DB giảm đúng bằng số ca đã xóa",
       note="Nguồn: Quản lý calendar r727-r738."),

    tc("Ca làm việc — sửa & xóa", "CONC-002", "Normal",
       "Double-click nút 一括シフト削除 và trạng thái nút sau khi xóa",
       CAL + "\n- Đã tick 1 ca chưa có booking",
       "1. Double-click nút「一括シフト削除」→ xác nhận\n2. Quan sát nút sau khi xóa xong",
       "1 ca",
       "- Chỉ tính 1 lần (không xóa 2 lần / không lỗi)\n- Sau khi xóa: nút bị disable",
       note="Nguồn: Quản lý calendar r739-r740."),

    tc("Ca làm việc — sửa & xóa", "DATA-REF-001", "Boundary",
       "2 ca cùng ngày: xóa ca không booking khi ca kia CÓ booking → không chặn nhầm",
       CAL + "\n- S1 ngày 11/07 có Ca1 10:00-13:00 và Ca2 15:00-18:00\n"
             "- Booking「予約確定」11:00-12:00 nằm trong Ca1",
       "1. Xóa Ca2 (không có booking) → quan sát\n"
       "2. Xóa Ca1 (có booking) → quan sát\n3. Kiểm tra DB sau mỗi bước",
       "2 ca, booking chỉ ở Ca1",
       "- B1: xóa Ca2 THÀNH CÔNG, không báo lỗi (booking của Ca1 không bị tính vào Ca2)\n"
       "- B2: Xóa Ca1 bị CHẶN với message 削除するシフト…\n"
       "- Cuối cùng chỉ còn Ca1 trong DB",
       note="Nguồn: #38520 r88-r89."),

    tc("Ca làm việc — sửa & xóa", "DATA-REF-001", "Normal",
       "2 ca cùng ngày: xóa 1 ca không làm mất ca còn lại",
       CAL + "\n- S1 ngày 11/07 có Ca1 10:00-13:00 và Ca2 15:00-18:00, không booking",
       "1. Xóa Ca1 → quan sát lưới và DB\n2. Kiểm tra Ca2",
       "2 ca không booking",
       "- Ca1 bị xóa, lưới chỉ còn Ca2 15:00-18:00\n"
       "- Ca2 giữ nguyên, DB còn đúng 1 bản ghi ca",
       note="Nguồn: #38520 r87."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Normal",
       "Rút ngắn ca vẫn bao trọn booking → cho phép (không chặn nhầm)",
       CAL + "\n- Ca S1 ngày 11/07 19:00-24:00; booking「予約確定」20:00-21:00",
       "1. Sửa ca thành 19:00-22:00 → lưu\n2. Kiểm tra ca và booking",
       "Booking 20:00-21:00 nằm trong phần giữ lại",
       "- Lưu thành công, KHÔNG báo lỗi\n- Ca hiển thị 19:00-22:00\n- Booking giữ nguyên",
       note="Nguồn: #38520 r82."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Abnormal",
       "Thu hẹp ca từ phía ĐẦU cắt vào booking 予約確定 → phải chặn",
       CAL + "\n- Ca S1 ngày 11/07 19:00-24:00; booking「予約確定」19:00-20:00",
       "1. Sửa ca thành 21:00-24:00 (nâng giờ bắt đầu) → lưu\n2. Kiểm tra ca",
       "Booking rơi ngoài ca mới",
       "- Chặn, lỗi 上書き（短縮）…\n- Ca giữ nguyên 19:00-24:00",
       note="Nguồn: #38520 r81."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Boundary",
       "Ca khớp ĐÚNG giờ 1 booking 予約確定 → rút ngắn và xóa đều phải chặn",
       CAL + "\n- Ca S1 ngày 11/07 20:00-21:00; booking「予約確定」20:00-21:00",
       "1. Rút ngắn ca thành 20:00-20:30 → lưu\n2. Xóa ca → xác nhận\n3. Kiểm tra DB",
       "Ca trùng khít booking",
       "- B1: chặn với lỗi 上書き（短縮）…\n- B2: chặn với lỗi 削除するシフト…\n"
       "- Ca vẫn còn trong DB",
       note="Nguồn: #38520 r76, r83."),

    tc("Ca làm việc — sửa & xóa", "FUNC-DATE-001", "Normal",
       "Booking đã キャンセル / 否認 trong phần bị cắt → cho phép sửa ca",
       CAL + "\n- Ca S1 ngày 11/07 19:00-24:00; booking 22:00-23:00 đang ở trạng thái キャンセル",
       "1. Sửa ca thành 19:00-21:00 → lưu\n2. Kiểm tra ca",
       "Booking キャンセル trong phần bị cắt",
       "- Lưu thành công, không báo lỗi\n"
       "- Chỉ booking「予約確定」mới chặn thao tác; booking「キャンセル」/「否認」không chiếm slot",
       note="Nguồn: #38520 r9."),

    tc("Ca làm việc — sửa & xóa", "CONC-003", "Abnormal",
       "2 tab cùng thao tác 1 ca: tab A xóa, tab B sửa",
       CAL + "\n- Ca S1 ngày 11/07 19:00-24:00; mở màn edit ca ở 2 tab",
       "1. Tab A: xóa ca → thành công\n2. Tab B: sửa giờ ca đó → lưu\n"
       "3. Quan sát tab B và kiểm tra DB",
       "1 ca, 2 tab",
       "- Tab B KHÔNG ghi dữ liệu cũ vào ca đã xóa: hiển thị lỗi/thông báo hợp lý hoặc tự reload\n"
       "- Không có lỗi JS/console\n- DB nhất quán: không có bản ghi ca mồ côi",
       note="Nguồn: #38520 r35."),

    tc("Ca làm việc — sửa & xóa", "CONC-003", "Abnormal",
       "Người khác tạo booking trong lúc admin đang mở màn edit ca → chặn xóa",
       CAL + "\n- Ca S1 ngày 11/07 09:00-14:00 chưa có booking",
       "1. Admin A mở màn edit ca\n2. LINE user B đặt booking thành công trong ca đó\n"
       "3. Admin A bấm xóa ca",
       "Booking mới tạo trong lúc màn edit đang mở",
       "- KHÔNG cho xóa (server check lại tại thời điểm submit)\n- Ca và booking đều giữ nguyên",
       note="Nguồn: Quản lý calendar r1496, r1518, r1541, r1563."),

    tc("Ca làm việc — sửa & xóa", "STATE-001", "Abnormal",
       "Đóng tab / mất mạng giữa lúc lưu nhiều ca → không để lại dữ liệu nửa vời",
       SHIFT + "\n- Đã điền đủ, chọn 5 ngày (ghi 5 bản ghi)",
       "1. Bấm「登録する」rồi ngắt mạng / đóng tab ngay\n"
       "2. Mở lại màn hình → đếm số ca đã tạo\n3. Kiểm tra DB",
       "5 ngày",
       "- HOẶC cả 5 ca được tạo, HOẶC không ca nào được tạo — KHÔNG được tạo dở (vd 3/5)\n"
       "- Không có bản ghi mồ côi / ca không hiển thị được trên lưới",
       note="Nguồn: #38520 r54."),

    tc("Ca làm việc — sửa & xóa", "FUNC-MULTI-001", "Boundary",
       "Ghép 2 ca rời thành 1 ca liên tục — booking được bảo toàn",
       CAL + "\n- S1 ngày 11/07 có Ca1 10:00-13:00 và Ca2 15:00-18:00\n"
             "- Có booking「予約確定」11:00-12:00 (Ca1) và 16:00-17:00 (Ca2)",
       "1. Thao tác ghép thành 1 ca 10:00-18:00 → lưu\n"
       "2. Kiểm tra DB số bản ghi ca\n3. Kiểm tra 2 booking\n4. Kiểm tra LIFF phía LINE user",
       "2 ca + 2 booking",
       "- Kết quả cuối: 1 ca 10:00-18:00, không còn 2 bản ghi rời/chồng\n"
       "- CẢ 2 booking giữ nguyên: không mất, không nhân đôi, không đổi trạng thái\n"
       "- LIFF: khoảng 13:00-15:00 giờ trở thành đặt được",
       note="Nguồn: #38520 r94-r95. RULE-07 (3 tầng: DB + lưới admin + LIFF)."),

    tc("Ca làm việc — sửa & xóa", "FUNC-MULTI-001", "Normal",
       "Thêm ca thứ 2 KHÔNG chồng giờ → 2 ca cùng tồn tại, không ghi đè",
       CAL + "\n- S1 ngày 11/07 đã có Ca1 10:00-13:00",
       "1. Thêm ca 15:00-18:00 → lưu\n2. Kiểm tra lưới và DB\n3. Kiểm tra LIFF",
       "Ca1 10:00-13:00 · ca mới 15:00-18:00",
       "- Cả 2 ca cùng tồn tại, KHÔNG ghi đè Ca1\n- DB có 2 bản ghi ca\n"
       "- LIFF: đặt được ở 2 khung, khoảng 13:00-15:00 không có slot",
       note="Nguồn: #38520 r90."),

    tc("Ca làm việc — sửa & xóa", "FUNC-MULTI-001", "Normal",
       "Rút ngắn / kéo dài 1 trong 2 ca không ảnh hưởng ca còn lại",
       CAL + "\n- S1 ngày 11/07 có Ca1 10:00-13:00 và Ca2 15:00-18:00",
       "1. Rút Ca1 thành 10:00-12:00 → lưu → kiểm tra Ca2\n"
       "2. Kéo dài Ca1 thành 10:00-14:00 (không chạm Ca2) → lưu → kiểm tra Ca2\n"
       "3. Kéo dài Ca1 thành 10:00-16:00 (chồng Ca2) → lưu",
       "2 ca như mô tả",
       "- B1: Ca1 = 10:00-12:00, Ca2 giữ nguyên, DB đúng 2 bản ghi\n"
       "- B2: Ca1 = 10:00-14:00, Ca2 giữ nguyên, 2 ca độc lập\n"
       "- B3: xử lý theo rule overlap (ghi đè / gộp / chặn) — KHÔNG tạo 2 ca chồng nhau âm thầm",
       note="Nguồn: #38520 r91-r93. ⚠ B3 hành vi chưa chốt rõ ràng trong corpus — xem MT-04."),

    tc("Ca làm việc — sửa & xóa", "SYNC-APP-001", "Normal",
       "Xóa ca ở modal edit trên app mobile — theo trạng thái booking",
       CAL + "\n- Đã đăng nhập app mobile bằng tài khoản Admin bot A\n"
             "- S1 có nhiều ca (cả ca thường và ca qua ngày)",
       "1. App: xóa ca chưa có booking → quan sát\n"
       "2. App: xóa ca có booking đã cancel / đang request booking → quan sát\n"
       "3. App: xóa ca có booking success / đang request cancel → quan sát\n"
       "4. Lặp lại cho calendar loại private",
       "Ca ở 4 trạng thái booking",
       "- B1, B2: xóa thành công\n- B3: báo lỗi, không xóa\n"
       "- Calendar private cho kết quả giống calendar staff",
       note="Nguồn: Quản lý calendar r2155-r2163."),

    tc("Ca làm việc — sửa & xóa", "SYNC-APP-001", "Abnormal",
       "Bug Tester #33314: booking có start/end nằm TRONG ca thì không được xóa/sửa ca",
       CAL + "\n- Ca S1 ngày 11/07 08:00-12:00\n- Có booking「予約確定」07:30-08:30 (start ngoài ca, end trong ca)",
       "1. Xóa ca 08:00-12:00 → quan sát\n2. Sửa giờ ca → quan sát",
       "Booking 07:30-08:30",
       "- Cả 2 thao tác đều bị CHẶN, báo lỗi\n- Ca và booking giữ nguyên",
       note="Nguồn: Quản lý calendar r1564-r1565 (Bug Tester #33314)."),

    # ══════════════ 18. Ca làm việc — qua ngày & biên 00:00 ══════════════
    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Nhập giờ kết thúc 24:00 và 00:00 cho ra cùng 1 ca",
       SHIFT + "\n- S1 chưa có ca ngày 11/07 và 12/07",
       "1. Ngày 11/07: nhập ca 19:00-24:00 → lưu → quan sát lưới\n"
       "2. Ngày 12/07: nhập ca 19:00-00:00 → lưu → quan sát lưới\n"
       "3. So sánh 2 ca trên lưới, trong DB và ở LIFF",
       "24:00 và 00:00",
       "- Cả 2 cách nhập cho ra CÙNG 1 loại ca (19:00 đến hết ngày)\n"
       "- Hiển thị nhất quán trên calendar\n- Ca không bị hiểu thành độ dài 0 hoặc âm",
       note="Nguồn: #38520 r30, r71, r101-r102. ⚠ Corpus ghi rõ「00:00 đã bị SQL CASE cap→ …」— đây là "
            "định dạng THỰC SỰ kích hoạt bug trên môi trường thật, phải test cả 2 định dạng."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Ca qua rạng sáng 23:00-01:00: độ dài và ngày sở hữu đúng",
       SHIFT + "\n- S1 chưa có ca ngày 11/07",
       "1. Nhập ca 23:00-01:00 cho ngày 11/07 → lưu\n"
       "2. Quan sát lưới ngày 11/07 và ngày 12/07\n3. Kiểm tra LIFF",
       "Ca 23:00~翌01:00",
       "- Ca lưu đúng, độ dài = 2 giờ (không âm, không = 0)\n"
       "- Ca thuộc ngày 11/07, KHÔNG bị chuyển hẳn sang 12/07\n"
       "- LIFF hiển thị slot đặt được ở cả phần 23:00-24:00 và 00:00-01:00",
       note="Nguồn: #38520 r31, r98."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Normal",
       "Bug KH #38519: sửa ca ngày X khi ngày X+1 có booking kết thúc 00:00 → không chặn nhầm",
       CAL + "\n- S1 chưa có ca ngày 11/07 và 12/07",
       "1. Tạo ca S1 ngày 11/07 = 19:00-24:00 và ngày 12/07 = 19:00-24:00\n"
       "2. Tạo booking「予約確定」ngày 12/07 22:00-00:00\n"
       "3. Sửa ca ngày 11/07 thành 19:00-23:00 → lưu\n4. Kiểm tra ca và booking",
       "Booking ngày 12/07 kết thúc đúng 00:00",
       "- Ca ngày 11/07 lưu THÀNH CÔNG, hiển thị 19:00-23:00\n"
       "- KHÔNG hiển thị lỗi 上書き（短縮）…\n- Booking ngày 12/07 giữ nguyên",
       note="Nguồn: #38520 r3 (repro chính Bug KH #38519, 07/07/2026)."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Abnormal",
       "Chống over-fix: booking kết thúc 00:00 của CHÍNH ngày đó vẫn phải chặn",
       CAL + "\n- Ca S1 ngày 11/07 = 19:00-24:00\n- Booking「予約確定」ngày 11/07 22:00-00:00",
       "1. Rút ngắn ca ngày 11/07 thành 19:00-21:00 → lưu\n"
       "2. Xóa ca ngày 11/07 → xác nhận\n3. Kiểm tra ca và booking",
       "Booking cùng ngày kết thúc 00:00",
       "- B1: CHẶN với lỗi 上書き（短縮）…, ca giữ nguyên 19:00-24:00\n"
       "- B2: CHẶN với lỗi 削除するシフト…\n- Ca + booking còn nguyên trong DB",
       note="Nguồn: #38520 r77-r78, r84. Đây là case chống over-fix của Bug #38519."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Abnormal",
       "Ca qua rạng sáng: booking nằm trong phần rạng sáng vẫn phải chặn khi rút ngắn",
       CAL + "\n- Ca S1 ngày 11/07 = 19:00-翌03:00\n- Booking「予約確定」ngày 12/07 01:00-02:00",
       "1. Rút ngắn ca ngày 11/07 thành 19:00-24:00 → lưu\n2. Kiểm tra ca",
       "Booking rạng sáng 01:00-02:00",
       "- CHẶN với lỗi 上書き（短縮）…\n- Ca giữ nguyên 19:00-翌03:00",
       note="Nguồn: #38520 r8, r80."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Ca qua rạng sáng: booking BUỔI TỐI ngày X+1 KHÔNG thuộc ca ngày X",
       CAL + "\n- S1 chưa có ca ngày 11/07 và 12/07",
       "1. Tạo ca S1 ngày 11/07 = 19:00-翌03:00\n"
       "2. Tạo booking「予約確定」ngày 12/07 23:00-00:00\n"
       "3. Sửa / xóa ca ngày 11/07 → quan sát",
       "Booking 12/07 23:00-00:00 (start 23:00 > giờ cuối ca 03:00)",
       "- Lưu / xóa THÀNH CÔNG, không báo lỗi\n"
       "- Booking 12/07 23:00-00:00 KHÔNG bị tính là thuộc ca ngày 11/07",
       note="Nguồn: #38520 r7, r72-r74."),

    tc("Ca làm việc — qua ngày & biên 00:00", "DATA-001", "Abnormal",
       "Booking kết thúc 00:00 KHÔNG được sinh booking ảo ở ngày hôm sau (day/week/month view)",
       CAL + "\n- Có booking「予約確定」ngày 11/07/2026 19:00-00:00",
       "1. Xem lưới NGÀY 11/07 và 12/07\n2. Xem lưới TUẦN chứa 2 ngày này\n"
       "3. Xem lưới THÁNG 07/2026\n4. Đối chiếu số đếm booking giữa 3 lưới",
       "1 booking kết thúc đúng 00:00",
       "- Ngày 11/07: hiển thị 1 booking\n- Ngày 12/07: KHÔNG có booking nào (không có booking ảo)\n"
       "- Lưới tuần: cột ngày 12 không hiện booking ảo\n"
       "- Lưới tháng: ô ngày 12 không có booking; số đếm mỗi ô khớp với lưới ngày",
       note="Nguồn: #38520 r12, r16 (Bug KH #38520/#38537, 07/2026)."),

    tc("Ca làm việc — qua ngày & biên 00:00", "DATA-001", "Normal",
       "Booking cross-midnight THẬT vẫn hiển thị đủ ở cả 2 ngày",
       CAL + "\n- Ca S1 ngày 11/07 = 19:00-翌03:00\n- Booking「予約確定」ngày 11/07 23:00-翌01:00",
       "1. Xem lưới ngày 11/07\n2. Xem lưới ngày 12/07",
       "Booking 23:00-01:00",
       "- Ngày 11/07: hiển thị phần 23:00-24:00\n"
       "- Ngày 12/07: VẪN hiển thị phần 00:00-01:00 (đây là booking thật, không phải ảo)",
       note="Nguồn: #38520 r11, r79 (booking kết thúc 00:01 cũng phải hiển thị ở ngày hôm sau)."),

    tc("Ca làm việc — qua ngày & biên 00:00", "DATA-001", "Boundary",
       "Booking cross-THÁNG và cross-NĂM không lọt sang ngày đầu tháng/năm sau",
       CAL + "\n- Có booking「予約確定」31/08/2026 19:00-00:00 và ca 31/12 19:00-01/01 00:00",
       "1. Xem lưới tháng 08/2026 ô ngày 31\n2. Xem lưới tháng 09/2026 ô ngày 01\n"
       "3. Xem lưới tháng 01/2027 ô ngày 01\n4. Sửa ca ngày 31/08 và ngày 31/12 → quan sát",
       "Booking cross-tháng và cross-năm",
       "- Tháng 08: ô ngày 31 hiển thị booking đúng\n"
       "- Tháng 09: ô ngày 01 KHÔNG hiển thị booking đó\n"
       "- 01/01/2027: KHÔNG có booking ảo (so sánh full-date phải tính đúng cả năm)\n"
       "- Sửa ca ngày 31/08 và 31/12: THÀNH CÔNG, không bị chặn nhầm (logic date+1 nhảy đúng tháng/năm)",
       note="Nguồn: #38520 r13, r32, r70."),

    tc("Ca làm việc — qua ngày & biên 00:00", "DATA-001", "Abnormal",
       "Ngày 休業日 kế tiếp không sinh booking ảo và LINE user không đặt được",
       CAL + "\n- Ca S1 ngày 11/07 = 19:00-24:00\n- Ngày 12/07 đã set「休業日として設定する」",
       "1. Xem lưới ngày 12/07\n2. LINE user mở LIFF chọn ngày 12/07",
       "Ngày nghỉ 12/07",
       "- Ngày 12/07: KHÔNG hiển thị booking ảo\n"
       "- LIFF: ngày 12/07 không chọn được, hiển thị đúng thông báo không có slot",
       note="Nguồn: #38520 r14-r15, r99."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Abnormal",
       "Thêm nhiều khoảng giờ trong đó có khoảng qua ngày chồng lấn → báo lỗi đúng dòng",
       SHIFT,
       "1. Nhập 08:00-12:00 và 23:00-03:00 → lưu\n"
       "2. Nhập 22:30-01:30 và 23:00-01:00 → lưu\n"
       "3. Nhập nhiều khoảng qua ngày chồng nhau → lưu\n"
       "4. Ngày đã có ca 22:00-05:00, thêm 03:00-06:00 → lưu",
       "Các tổ hợp như mô tả",
       "- B1: add thành công (2 khoảng không chồng nhau)\n"
       "- B2, B3, B4: hiển thị message lỗi ở đúng số thứ tự dòng bị lỗi",
       note="Nguồn: Quản lý calendar r2385-r2391."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Ca qua ngày biên: 23:59~23:58 và 2 khoảng liền nhau qua nửa đêm",
       SHIFT,
       "1. Nhập ca 23:59-23:58 → lưu\n2. Nhập 08:00-12:00 và 12:00-16:00 → lưu → kiểm tra phía LINE user",
       "23:59~23:58 · 2 khoảng liền nhau",
       "- B1: add thành công (ca gần như trọn 24h)\n"
       "- B2: phía LINE user hiển thị tương đương ca 08:00-16:00",
       note="Nguồn: Quản lý calendar r2382-r2384."),

    tc("Ca làm việc — qua ngày & biên 00:00", "DATA-001", "Normal",
       "Ca qua ngày hiển thị đúng ở 5 nơi",
       CAL + "\n- S1 có ca ngày 11/07 = 23:00-翌05:00",
       "1. Kiểm tra lưới NGÀY 11/07 và 12/07\n2. Kiểm tra lưới TUẦN\n3. Kiểm tra lưới THÁNG\n"
       "4. Kiểm tra tab シフト (list)\n5. Kiểm tra LIFF phía LINE user",
       "Ca 23:00~翌05:00",
       "- Cả 5 nơi hiển thị nhất quán ca qua ngày\n"
       "- LIFF cho đặt được slot trong cả phần trước và sau nửa đêm",
       note="Nguồn: Quản lý calendar r2383. ⚠ Corpus đánh dấu NG ở lưới TUẦN tại thời điểm test → "
            "cần verify lại lưới tuần sau khi fix."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Ca qua ngày × setting mùa vụ ở 2 biên",
       CAL + "\n- Mùa vụ 10/8 - 20/8",
       "1. Thêm ca qua ngày cho ngày 9/8 (trước mùa vụ) → xem đầu ngày 10/8 phía admin và LINE user\n"
       "2. Thêm ca qua ngày cho ngày 20/8 (cuối mùa vụ) → xem đầu ngày 21/8",
       "Ca qua ngày ở 2 biên mùa vụ",
       "- Biên đầu: đầu ngày 10/8 hiển thị icon ĐẶT ĐƯỢC ở lưới ngày admin\n"
       "- Biên cuối: đầu ngày 21/8 hiển thị icon KHÔNG đặt được\n"
       "- Kiểm tra đồng bộ ở cả lưới tuần/tháng phía LINE user",
       note="Nguồn: Quản lý calendar r2492-r2493. ⚠ Corpus đánh NG cho lưới tuần/tháng phía LINE user ở "
            "biên đầu → cần verify lại, xem MT-16."),

    tc("Ca làm việc — qua ngày & biên 00:00", "FUNC-DATE-001", "Boundary",
       "Ca qua ngày + thời gian nghỉ trước/sau: slot phía LINE user bị cắt đúng",
       CAL + "\n- Nghỉ trước 30 phút, nghỉ sau 10 phút\n- Ca S1 = 20:00-翌05:00\n"
             "- Có booking 23:30-翌00:30",
       "1. LINE user mở LIFF chọn ngày đó\n2. Đối chiếu các slot enable/disable",
       "Nghỉ trước 30' · sau 10' · booking 23:30-00:30",
       "- Chỉ hiển thị slot đặt được đến khung 21:30 và từ khung 01:30 trở đi\n"
       "- Khoảng 21:30-01:30 bị disable (booking + vùng nghỉ)",
       note="Nguồn: Quản lý calendar r2494."),

    tc("Ca làm việc — qua ngày & biên 00:00", "ENV-002", "Normal",
       "Múi giờ JST: giờ hiển thị không lệch giữa Web / App / CSV",
       CAL + "\n- Có booking「予約確定」ngày 11/07/2026 19:00-00:00",
       "1. Xem giờ trên Web\n2. Xem giờ trên app mobile\n3. Export CSV và mở file",
       "Booking 19:00-00:00",
       "- Giờ hiển thị đúng theo JST ở cả 3 nơi\n- Không lệch ±9 giờ do timezone",
       note="Nguồn: #38520 r33."),

    tc("Ca làm việc — qua ngày & biên 00:00", "PERM-003", "Normal",
       "Multi-tenant: sửa ca ở bot A không ảnh hưởng bot B",
       "- Bot A và Bot B đều có salon calendar, staff CÙNG TÊN, ca cùng giờ\n"
       "- Đăng nhập admin có quyền cả 2 bot",
       "1. Ở bot A, sửa ca của staff S1 ngày 11/07\n"
       "2. Chuyển sang bot B, kiểm tra ca và booking của staff cùng tên\n3. Kiểm tra DB theo bot_id",
       "2 bot, staff trùng tên",
       "- Chỉ ca của bot A thay đổi\n- Ca + booking của bot B giữ nguyên\n"
       "- Truy vấn có điều kiện `bot_id` / `calendar_salon_id` đúng, không có bản ghi lẫn bot",
       note="Nguồn: #38520 r34."),

    # ══════════════ 19. Ca làm việc — CSV ══════════════
    tc("Ca làm việc — CSV", "OUT-EXPORT-001", "Abnormal",
       "Export CSV ca: bắt buộc chọn staff, mỗi staff 1 file",
       CAL + "\n- Mở modal「CSVでシフトを管理」→ tab エクスポート",
       "1. Không chọn staff → bấm export\n2. Chọn 1 staff → export\n"
       "3. Chọn nhiều staff → export\n4. Chọn tất cả staff → export",
       "S1, S2, S3",
       "- B1: lỗi「スタッフを選択してください。」\n- B2: tải về 1 file\n"
       "- B3, B4: mỗi staff 1 file riêng",
       note="Nguồn: Quản lý calendar r949-r953."),

    tc("Ca làm việc — CSV", "OUT-EXPORT-001", "Normal",
       "File CSV export đúng 3 cột, không xuất ngày nghỉ, sort theo thời gian",
       CAL + "\n- S1 có ca ở nhiều ngày, trong đó có 1 ngày là 休業日",
       "1. Export CSV của S1 → mở file\n2. Đối chiếu header và dữ liệu\n3. Kiểm tra ngày nghỉ",
       "Ca của S1 trong 3 tháng, có ngày nghỉ",
       "- File có 3 cột:「追加したい日付」「開始時間」「終了時間」\n"
       "- KHÔNG export ngày nghỉ (is_day_off = 1)\n"
       "- Dữ liệu sort theo date, rồi start_time, rồi end_time tăng dần",
       note="Nguồn: Quản lý calendar r954-r955."),

    tc("Ca làm việc — CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV chứa ca kết thúc 24:00 → giờ xuất đầy đủ, không mojibake",
       CAL + "\n- S1 có ca ngày 11/07 = 19:00-24:00",
       "1. Export CSV của S1\n2. Mở file bằng Excel tiếng Nhật\n3. Đối chiếu cột giờ",
       "Ca 19:00-24:00",
       "- File mở được, encoding hiển thị tiếng Nhật đúng (không mojibake)\n"
       "- Cột giờ của ca ngày 11/07 xuất ĐẦY ĐỦ cả phần giờ (không mất giờ kết thúc)",
       note="Nguồn: #38520 r21. ⚠ Corpus ghi「ở csv chỉ nhập được: 00:00」— cần đối chiếu giá trị "
            "thực xuất ra (24:00 hay 00:00), xem MT-04."),

    tc("Ca làm việc — CSV", "FUNC-003", "Abnormal",
       "Import CSV: validate thiếu staff / thiếu file / sai định dạng file",
       CAL + "\n- Mở modal「CSVでシフトを管理」→ tab インポート",
       "1. Không chọn staff → bấm import\n2. Không chọn file → bấm import\n"
       "3. Chọn file không phải CSV/Excel",
       "File .txt, .pdf",
       "- B1: lỗi「スタッフを選択してください。」\n- B2: không import\n"
       "- B3: chỉ chọn được file định dạng cho phép",
       note="Nguồn: Quản lý calendar r986-r988."),

    tc("Ca làm việc — CSV", "FUNC-003", "Abnormal",
       "Import CSV: validate từng cột dữ liệu",
       CAL + "\n- Mở tab インポート",
       "1. Bỏ trống cột 追加したい日付 → import\n"
       "2. Ngày sai format (dd-mm-yyyy, yyyy/mm/dd, chuỗi không phải date) → import\n"
       "3. Bỏ trống cột 開始時間 → import\n4. Bỏ trống cột 終了時間 → import\n"
       "5. start hoặc end > 23:59 → import\n6. start > end → import\n7. start = end → import",
       "File CSV với các dòng lỗi tương ứng",
       "- Ngày trống: lỗi「xxx行の追加したい日付のデータに不備があります」\n"
       "- Ngày sai format: validate báo lỗi\n"
       "- 開始時間 trống hoặc > 23:59 hoặc start > end: lỗi「xxx行の開始時間のデータに不備があります」\n"
       "- 終了時間 trống hoặc start = end: lỗi「xxx行の終了時間のデータに不備があります」\n"
       "- KHÔNG tạo ca nào từ các dòng lỗi (không có ca rác / độ dài âm trong DB)",
       note="Nguồn: Quản lý calendar r990-r998 + #38520 r23."),

    tc("Ca làm việc — CSV", "FUNC-003", "Abnormal",
       "Import CSV: chặn dòng có thời gian quá khứ",
       CAL + "\n- Mở tab インポート",
       "1. File có dòng với ngày < hôm nay → import\n"
       "2. File có dòng ngày = hôm nay nhưng start_time < giờ hiện tại → import\n"
       "3. File có cả dòng quá khứ và dòng hợp lệ → import",
       "Dòng quá khứ và dòng hợp lệ",
       "- Dòng quá khứ: lỗi「{line}行目の時間は現在より過去になりますので、登録できません。」\n"
       "- Các dòng hợp lệ vẫn được import (bỏ qua dòng quá khứ)",
       note="Nguồn: Quản lý calendar r999-r1000, r1009."),

    tc("Ca làm việc — CSV", "FUNC-003", "Normal",
       "Import CSV: dòng trùng thì skip, dòng mới thì insert",
       CAL + "\n- S1 đã có ca 11:20-13:20 ngày X trong DB",
       "1. Import dòng cùng ngày + cùng start + cùng end → kiểm tra\n"
       "2. Import dòng cùng ngày + khác start + khác end (không chồng) → kiểm tra\n"
       "3. Import dòng cùng ngày + khác start + cùng end → kiểm tra\n"
       "4. Import dòng cùng ngày + cùng start + khác end → kiểm tra\n"
       "5. Import file có 1 dòng mới (09:00-10:00) và 1 dòng đã có (11:20-13:20)",
       "Ca đã có 11:20-13:20",
       "- B1, B3, B4: SKIP dòng đã có\n- B2: insert bản ghi mới\n"
       "- B5: dòng đã có skip, dòng mới được add",
       note="Nguồn: Quản lý calendar r966-r974, r978-r981."),

    tc("Ca làm việc — CSV", "FUNC-003", "Normal",
       "Import CSV: khoảng giờ chồng nhau trong cùng file → bỏ qua khoảng sau",
       CAL + "\n- Mở tab インポート",
       "1. File có 09:00-10:00 và 09:30-11:30 → import\n2. File có 2 dòng 01:00-02:00 giống hệt → import",
       "2 file như mô tả",
       "- B1: bỏ qua khoảng sau (chỉ tạo 09:00-10:00)\n- B2: dòng đã có thì skip",
       note="Nguồn: Quản lý calendar r972-r973."),

    tc("Ca làm việc — CSV", "FUNC-003", "Normal",
       "Import CSV vào ngày đang là 休業日 → xóa ngày nghỉ, thêm ca mới",
       CAL + "\n- Ngày X của S1 đang set 休業日",
       "1. Import file có dòng ca cho ngày X → kiểm tra lưới và DB",
       "Ngày X đang là ngày nghỉ",
       "- Ngày nghỉ bị xóa, ca mới được thêm vào ngày X\n- Lưới hiển thị ca thay vì「休業日」",
       note="Nguồn: Quản lý calendar r975, r982."),

    tc("Ca làm việc — CSV", "FUNC-003", "Boundary",
       "Bug #32775: import CSV chỉ check trùng giờ TRONG CÙNG 1 NGÀY",
       CAL + "\n- Mở tab インポート",
       "1. Import file: 2024-08-28,07:30,06:15 · 2024-08-30,11:25,15:30 · 2024-08-29,06:20,09:15\n"
       "2. Import file: 2024-08-28,07:30,06:15 · 2024-08-29,04:20,09:15",
       "2 file như mô tả",
       "- B1: import THÀNH CÔNG (các ngày khác nhau không bị check trùng lẫn nhau)\n"
       "- B2: lỗi「...項目の開始時間は、他の終了時間より、大きくしてください。」(ca qua ngày 28→29 "
       "lấn giờ của ngày 29)",
       note="Nguồn: Quản lý calendar r976-r977, r983-r984, r2110-r2114 (Bug #32775, 10/11/2025)."),

    tc("Ca làm việc — CSV", "FUNC-003", "Abnormal",
       "Import CSV KHÔNG validate tên cột — đọc theo thứ tự cột",
       CAL + "\n- Mở tab インポート",
       "1. Sửa tên 3 cột header trong file thành tên bất kỳ (giữ nguyên thứ tự) → import\n"
       "2. Đảo THỨ TỰ 2 cột 開始時間 và 終了時間 (giữ tên đúng) → import\n3. Kiểm tra DB",
       "File sai tên cột · file đảo thứ tự cột",
       "- B1: vẫn import được (hệ thống đọc theo thứ tự cột, không theo tên)\n"
       "- B2: dữ liệu bị hiểu sai theo vị trí → cần xác nhận có validate hay không",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar r989 (「sai tên cột vẫn cho vào, dev đang lấy theo thứ tự cột」). "
            "⚠ Đây là rủi ro dữ liệu — cần Leader quyết có bổ sung validate header không, xem MT-17."),

    tc("Ca làm việc — CSV", "FUNC-003", "Boundary",
       "Bug #26943: format giờ 1 chữ số và ngày không zero-pad",
       CAL + "\n- Mở tab インポート",
       "1. Import các dòng giờ dạng「9:00」và「09:00」→ kiểm tra\n"
       "2. Import dòng giờ「09:5」và「10:9」→ kiểm tra\n"
       "3. Import ngày「2024-09-28」→ kiểm tra\n4. Import ngày「2024-9-28」→ kiểm tra",
       "Các định dạng như mô tả",
       "- B1: cả 2 định dạng giờ đều insert thành công\n"
       "- B2: insert FAIL (thiếu chữ số phút)\n"
       "- B3: thành công\n- B4: FAIL (ngày phải zero-pad)",
       note="Nguồn: Quản lý calendar r1004-r1008 (Bug #26943, 21/10/2024)."),

    tc("Ca làm việc — CSV", "FUNC-003", "Normal",
       "Import CSV tạo ca 19:00-24:00 → sau đó sửa/xóa ca không bị chặn nhầm",
       CAL + "\n- S1 chưa có ca ngày 11/07 và 12/07",
       "1. Import file tạo ca 11/07 = 19:00-24:00 và 12/07 = 19:00-24:00\n"
       "2. Tạo booking「予約確定」ngày 12/07 22:00-00:00\n"
       "3. Sửa ca ngày 11/07 thành 19:00-23:00 → lưu\n4. Đối chiếu hành vi với ca tạo bằng UI",
       "Ca tạo bằng CSV",
       "- Import thành công, 2 ca tạo đúng trên calendar\n"
       "- Bước 3: lưu thành công, KHÔNG báo lỗi 上書き（短縮）…\n"
       "- Ca tạo bằng CSV hành xử GIỐNG ca tạo bằng UI",
       note="Nguồn: #38520 r22."),

    tc("Ca làm việc — CSV", "FUNC-003", "Normal",
       "Round-trip: export → import lại chính file vừa export → ca không đổi",
       CAL + "\n- S1 có: ca thường 10:00-18:00, ca kết thúc 24:00, ca qua rạng sáng, 1 ngày 休業日",
       "1. Export CSV của S1\n2. Import lại chính file vừa export\n"
       "3. Đối chiếu toàn bộ ca trên lưới và DB",
       "4 loại ca như mô tả",
       "- Toàn bộ ca giữ nguyên (giờ, cờ 休業日, ca qua ngày)\n"
       "- Không sinh ca trùng, không mất ca\n"
       "- Đặc biệt ca kết thúc 24:00 và ca qua rạng sáng phải giữ nguyên",
       note="Nguồn: #38520 r25."),

    tc("Ca làm việc — CSV", "FUNC-003", "Abnormal",
       "Import CSV ghi đè ca đã có booking 予約確定 → hành vi phải khớp rule của UI",
       CAL + "\n- Ca S1 ngày 11/07 = 19:00-24:00, có booking「予約確定」22:00-23:00",
       "1. Import file có dòng ca 11/07 = 19:00-21:00 (rút ngắn cắt vào booking)\n"
       "2. Quan sát kết quả và đối chiếu với hành vi khi làm cùng thao tác trên UI",
       "File CSV rút ngắn ca",
       "- Hành vi khớp rule ghi đè của UI: HOẶC ghi đè thành công, HOẶC CHẶN vì còn booking 予約確定 "
       "trong phần bị rút ngắn\n"
       "- Không được xử lý khác UI",
       spec="Đã hỏi leader",
       note="Nguồn: #38520 r24. ⚠ Corpus để ngỏ 2 khả năng → cần Leader chốt, xem MT-04."),
]
