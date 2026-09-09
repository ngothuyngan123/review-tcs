# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 25-38: toàn bộ tab 予約設定 (受付上限, 前後の空き時間,
メッセージ・アクション, 予約の開始・締切, 1人あたりの予約上限, 質問項目, リマインド,
空き枠通知, トップ・店舗情報・利用規約, システムワード, 予約ページの非表示, 予約システムの削除).

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Setting calendar」(07/2024 → 05/2026, 1482 TC lá — SpecImprove #36037 thứ tự remind,
    SpecChange #26462 2 trường mặc định, Support #29272 friend info 日時, Bug #29462/#29678/#30053,
    SpecChange #29475 auto-save radio random staff)
  - tab「Quản lý calendar」r409-r541 (limit + blocktime), r2503+ (random)
  - tab「Test limit booking_V4_2」(02/2026 — bộ limit MỚI NHẤT)
"""
from _common import tc

SET = ("- Đăng nhập admin (主管理者) bot A\n"
       "- Calendar「サロンA」loại スタッフ, staff S1/S2, course C1\n"
       "- Mở /basic/calendar-salon/{id} → tab「予約設定」")

S5 = [
    # ══════════════ 25. 受付上限 — 店舗・スタッフ ══════════════
    tc("受付上限 — 店舗・スタッフ", "UI-FIELD-001", "Normal",
       "4 tuỳ chọn 受付上限 của cửa hàng và giá trị mặc định khi tạo calendar mới",
       SET + "\n- Mở mục「店舗とスタッフの受付上限」",
       "1. Với calendar TẠO MỚI sau khi release code → quan sát tuỳ chọn đang chọn\n"
       "2. Với calendar tạo TRƯỚC khi release code → quan sát\n"
       "3. Liệt kê đủ các tuỳ chọn có trên màn",
       "1 calendar mới + 1 calendar cũ",
       "- Calendar mới: mặc định option 1.1 (1 staff thực hiện xuyên suốt 1 booking)\n"
       "- Calendar cũ: mặc định option 1.2 (1 booking có thể do nhiều staff thực hiện)\n"
       "- Có đủ các tuỳ chọn: option 1 (đếm theo số staff, tách 1.1/1.2) · option 2 (không giới hạn) · "
       "option 3 (nhập số cụ thể) · tuỳ chọn「上限をその時間に受付可能なスタッフ数の合計にする」",
       note="Nguồn: Quản lý calendar r3119-r3128 (issue #29114) + Setting calendar r1729-r1778. "
            "⚠ Spec §2.4.4 chỉ mô tả `limit` (0=unlimited, 1=limited) — KHÔNG có 4 tuỳ chọn này → MT-22."),

    tc("受付上限 — 店舗・スタッフ", "UI-FIELD-001", "Normal",
       "Setting 受付上限 riêng cho từng staff — lưu vào calendar_salon_staff.setting_staff_limit",
       SET + "\n- Mở mục「スタッフごとの同時受付上限」",
       "1. Với calendar vừa tạo → đọc giá trị mặc định của S1, S2\n"
       "2. Set S1 = 2, S2 = không giới hạn → lưu\n"
       "3. Reload màn → kiểm tra\n4. Kiểm tra hiển thị 同時に対応できる数 ở lưới QL ngày",
       "S1 = 2 · S2 = không giới hạn",
       "- Mặc định của calendar mới: theo giá trị khởi tạo (`createSettingLimitDefault`)\n"
       "- Sau khi lưu: giá trị giữ đúng sau reload\n"
       "- Lưới QL ngày: cột S1 hiện số 2, cột S2 hiện「設定しない」",
       note="Nguồn: Quản lý calendar r5887-r5893 + Setting calendar r1735-r1745. EP-37/EP-38."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Option 1: booking chưa đạt limit cửa hàng và staff → đặt được ở mọi cột",
       SET + "\n- Option 1; S1 limit 2, S2 limit 1 → limit calendar = 2\n"
             "- S1 có ca 08:00-12:00, S2 có ca 09:00-14:00, chưa có booking nào",
       "1. LINE user xem lịch → chọn 指定なし / S1 / S2 ở khung 10:00-11:00\n"
       "2. Đối chiếu lưới QL ngày phía admin\n"
       "3. Tạo 1 booking ở 指定なし → lặp lại bước 1 và 2\n"
       "4. Tạo 1 booking ở S1 → lặp lại bước 1 và 2",
       "S1 limit 2 · S2 limit 1 · limit calendar 2",
       "- Cả 3 bước: 指定なし = đặt được · S1 = đặt được · S2 = đặt được\n"
       "- Lưới admin hiển thị khớp với phía LINE user",
       note="Nguồn: Test limit booking_V4_2 r4-r11 (bộ limit MỚI NHẤT, 02/2026)."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Option 1: đạt đúng limit cửa hàng và staff → chặn đúng khung giờ có booking",
       SET + "\n- Option 1; S1 limit 1, S2 limit 1 → limit calendar = 2\n"
             "- S1 có ca 08:00-12:00, S2 có ca 09:00-14:00\n"
             "- Đã có booking ở 指定なし và S2 khung 10:00-11:00",
       "1. LINE user xem lịch từng khung 08:00-09:00 · 09:00-10:00 · 10:00-11:00 · 11:00-12:00 · "
       "12:00-14:00 với 指定なし / S1 / S2\n2. Đối chiếu lưới QL ngày",
       "2 booking khung 10:00-11:00",
       "- 08:00-09:00: 指定なし = được · S1 = được · S2 = KHÔNG (chưa có ca)\n"
       "- 09:00-10:00: cả 3 đều được\n- 10:00-11:00: cả 3 đều KHÔNG (đã đủ limit calendar = 2)\n"
       "- 11:00-12:00: cả 3 đều được\n- Lưới admin khớp phía LINE user",
       note="Nguồn: Test limit booking_V4_2 r12-r13."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Option 1: calendar còn slot nhưng staff đã full → chặn đúng staff đó",
       SET + "\n- Option 1; S1 limit 1, S2 limit 1, limit calendar = 3\n"
             "- S1 có ca 08:00-12:00, S2 có ca 09:00-14:00",
       "1. Chỉ S1 có booking khung 10:00-11:00 → LINE user chọn 指定なし / S1 / S2\n"
       "2. Cả S1 và S2 có booking khung đó → chọn lại 3 lựa chọn\n"
       "3. 指定なし và S1 có booking → chọn lại\n4. 指定なし có 2 booking → chọn lại",
       "limit calendar 3 · mỗi staff limit 1",
       "- B1: 指定なし = được · S1 = KHÔNG · S2 = được\n"
       "- B2, B3, B4: cả 3 lựa chọn đều KHÔNG đặt được",
       note="Nguồn: Test limit booking_V4_2 r20-r27."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Option 1: staff chưa full nhưng calendar đã full → chặn tất cả",
       SET + "\n- Option 1; limit calendar = 1; S1 limit 1, S2 limit 1 (hoặc S1 không giới hạn)\n"
             "- S1 và S2 đều có ca",
       "1. Có 1 booking ở 指定なし khung 10:00-11:00 → LINE user chọn 3 lựa chọn\n"
       "2. Có 1 booking ở S1 khung đó → chọn 3 lựa chọn\n"
       "3. Lặp lại với cấu hình S1 = không giới hạn",
       "limit calendar 1",
       "- Cả 3 lựa chọn đều KHÔNG đặt được (limit calendar quyết định)\n"
       "- Kết quả giống nhau ở cả 2 cấu hình staff",
       note="Nguồn: Test limit booking_V4_2 r30-r41."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Admin book cưỡng chế vẫn ĐƯỢC TÍNH vào limit",
       SET + "\n- Option 1; S1 limit 1, S2 limit 1; limit calendar = 2",
       "1. Admin book chèn vào giờ làm việc của S1 → LINE user kiểm tra khung đó\n"
       "2. Admin book cho staff đang OFF → kiểm tra\n"
       "3. Admin book vào ngày staff set nghỉ → kiểm tra\n"
       "4. Admin book chèn vào vùng nghỉ trước/sau của 1 booking khác → kiểm tra",
       "4 kiểu admin book cưỡng chế",
       "- Cả 4 trường hợp: booking admin VẪN được tính vào limit\n"
       "- Vùng nghỉ trước/sau của booking cũng được tính là booking khi đếm limit",
       note="Nguồn: Test limit booking_V4_2 r46-r95."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Block time từ Google KHÔNG được tính vào limit (nhưng chặn slot)",
       SET + "\n- Option 1; S1 đã liên kết Google, có event chặn khung 10:00-11:00",
       "1. LINE user chọn S1 khung 10:00-11:00 → quan sát\n"
       "2. LINE user chọn 指定なし và S2 khung đó → quan sát\n"
       "3. Admin book chèn vào vùng nghỉ trước/sau của block time Google → kiểm tra limit",
       "1 block time Google ở S1",
       "- S1: không đặt được khung 10:00-11:00 (bị block time chặn)\n"
       "- 指定なし và S2: VẪN đặt được (block time KHÔNG tính vào limit calendar)\n"
       "- Vùng nghỉ trước/sau của block time: được xử lý như block time",
       note="Nguồn: Test limit booking_V4_2 r96-r129 + Quản lý calendar r3172, r3180 "
            "(「option 3 tính theo số lượng booking, ko tính theo blocktime」)."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Option 1.1 vs 1.2: khác nhau khi 1 booking cần nhiều staff nối tiếp",
       SET + "\n- Course C1 dài 2 giờ; 2 staff, mỗi staff limit = 1\n"
             "- S1 đã có booking 10:00-11:00, S2 đã có booking 11:00-12:00",
       "1. Đặt option 1.1 → LINE user chọn 指定なし khung 10:00-12:00\n"
       "2. Đổi sang option 1.2 → chọn lại khung 10:00-12:00\n"
       "3. Đối chiếu lưới admin ở cả 2 cấu hình",
       "Course 2 giờ · 2 booking chèn nối tiếp",
       "- Option 1.1: khung 10:00-12:00 bị OFF (không staff nào phục vụ xuyên suốt được)\n"
       "- Option 1.2: khung 10:00-12:00 VẪN ON (chấp nhận nhiều staff nối tiếp)",
       note="Nguồn: Quản lý calendar r3129-r3151 (option 1.1) và r3169-r3171 (option 1.2)."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Tuỳ chọn 上限をその時間に受付可能なスタッフ数の合計にする — limit = tổng limit các staff khả dụng",
       SET + "\n- Đã chọn tuỳ chọn「上限をその時間に受付可能なスタッフ数の合計にする」\n"
             "- Có 2 staff cùng thực hiện course C1",
       "1. S1 limit 1, S2 limit 1, cả 2 đều ON và có ca → đếm số booking tối đa 1 khung\n"
       "2. S1 limit 2, S2 limit 1 → đếm lại\n"
       "3. S1 limit 1 nhưng OFF, S2 limit 1 → đếm lại\n"
       "4. S1 limit 1 nhưng KHÔNG có ca, S2 limit 1 → đếm lại\n"
       "5. Cả 2 không có ca → đếm lại",
       "Các tổ hợp limit như mô tả",
       "- B1: tối đa 2 booking / khung\n- B2: tối đa 3\n- B3: tối đa 1 (staff OFF không tính)\n"
       "- B4: tối đa 1 (staff không ca không tính)\n- B5: 0 — không đặt được",
       note="Nguồn: Quản lý calendar r221-r266, r3694-r3790 + Setting calendar r1773-r1849."),

    tc("受付上限 — 店舗・スタッフ", "UI-001", "Normal",
       "Staff OFF vẫn hiển thị ở lưới admin nhưng KHÔNG tính vào limit",
       SET + "\n- S1 có ca và có booking, sau đó bị OFF; S2 có ca",
       "1. OFF S1 → mở lưới QL ngày\n2. Quan sát cột S1: ca và booking cũ\n"
       "3. Đặt thêm booking cho 指定なし và S2 → xem limit",
       "S1 OFF (đã có ca + booking)",
       "- Lưới admin VẪN hiển thị cột S1 kèm ca và booking đã có trước khi OFF\n"
       "- Nhưng limit calendar KHÔNG cộng limit của S1 (vì S1 đang OFF)",
       note="Nguồn: Quản lý calendar r224-r226, r238-r240, r253-r255, r261-r263 (cập nhật 12/02/2025)."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Bug #26908: block time Google được coi như block time thường (không báo lý do 'đã limit')",
       SET + "\n- Option 3 với limit = 1; S1 đã liên kết Google có event chặn khung 10:00-11:00",
       "1. Ở lưới QL ngày bấm khung 10:00-11:00 của S1\n2. Đọc lý do trong modal",
       "1 block time Google, chưa có booking LME nào",
       "- Lý do KHÔNG phải「đã đạt limit」mà phải là lý do liên quan block time / không đặt được\n"
       "- Nhất quán với cách xử lý block time ở tính năng Calendar",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar r289 (Bug #26908, 14/10/2024). ⚠ Corpus không ghi text lý do "
            "chính xác → cần verify text thực tế, xem MT-23."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "V4_2 (02/2026): option limit 3 đếm CẢ booking ngoài giờ làm việc",
       SET + "\n- Option 3 với limit = 2; S1 có ca 08:00-12:00\n"
             "- Admin đã book cưỡng chế 1 booking ở 14:00-15:00 (ngoài ca của mọi staff)",
       "1. LINE user xem khung 14:00-15:00 → quan sát\n"
       "2. Đếm tổng số booking được phép trong khung đó\n3. Đối chiếu lưới admin",
       "Booking ngoài giờ làm việc",
       "- Booking ngoài giờ làm việc VẪN được đếm vào limit của option 3\n"
       "- Số slot còn lại giảm đúng",
       note="Nguồn: Test limit booking_V4_2 r3 (tiêu đề khối:「Sửa option limit 3: count cả các "
            "booking ngoài giờ lv」) — đây là thay đổi MỚI NHẤT về logic đếm limit."),

    tc("受付上限 — 店舗・スタッフ", "DATA-COUNT-001", "Boundary",
       "Limit ở calendar loại 個人: chỉ tính limit của calendar",
       SET + "\n- Calendar loại 個人",
       "1. Set không giới hạn → LINE user đặt nhiều booking cùng khung\n"
       "2. Set limit = 1 → đặt booking thứ 2 cùng khung\n3. Set limit = 2 → đặt booking thứ 3",
       "Calendar 個人",
       "- Không giới hạn: đặt được nhiều booking cùng khung\n"
       "- limit = 1: booking thứ 2 bị chặn\n- limit = 2: booking thứ 3 bị chặn",
       note="Nguồn: Test limit booking_V4_2 r217-r233 + Setting calendar r1760-r1764."),

    # ══════════════ 26. 前後の空き時間 ══════════════
    tc("前後の空き時間", "FUNC-DATE-001", "Normal",
       "Set thời gian nghỉ trước/sau cho booking LME và cho block time Google riêng biệt",
       SET + "\n- Mở mục「前後の空き時間」",
       "1. Set thời gian nghỉ trước/sau cho booking trên エルメ → lưu\n"
       "2. Set thời gian nghỉ trước/sau cho lịch sync từ Google Calendar → lưu\n"
       "3. Reload kiểm tra 4 giá trị\n4. Kiểm tra lưới QL ngày và phía LINE user",
       "time_before = 30 · time_after = 15 · time_before_google = 20 · time_after_google = 10",
       "- 4 giá trị lưu độc lập vào `calendar_salon_setting_time_free`\n"
       "- Lưới admin: vùng nghỉ hiển thị đúng độ dài từng loại\n"
       "- LINE user: slot bị chặn đúng theo từng loại",
       note="Nguồn: Setting calendar r1703-r1719. EP-35/EP-36."),

    tc("前後の空き時間", "FUNC-DATE-001", "Boundary",
       "Slot đầu ngày và cuối ngày KHÔNG bị trừ thời gian nghỉ",
       SET + "\n- Giờ làm việc 08:00-17:00, course 1 giờ",
       "1. Không set thời gian nghỉ → LINE user xem slot đầu và cuối\n"
       "2. Set nghỉ trước 15 phút → xem lại\n3. Set nghỉ sau 15 phút → xem lại\n"
       "4. Set cả trước và sau 15 phút → xem lại",
       "Giờ làm 08:00-17:00 · course 60 phút · nghỉ 15 phút",
       "- Cả 4 trường hợp: slot đầu tiên = 08:00; slot cuối cùng = 16:00 "
       "(= giờ kết thúc - thời gian course, KHÔNG trừ thêm thời gian nghỉ)",
       note="Nguồn: Booking phía line user r1295, r1297, r1299, r1301."),

    tc("前後の空き時間", "FUNC-DATE-001", "Boundary",
       "Ma trận slot bị chặn quanh 1 booking theo 4 cấu hình nghỉ",
       SET + "\n- Giờ làm 08:00-17:00, course 1 giờ, có 1 booking 09:30-10:30",
       "1. Không set nghỉ → LINE user xem slot enable/disable\n2. Chỉ nghỉ trước 15' → xem\n"
       "3. Chỉ nghỉ sau 15' → xem\n4. Cả trước và sau 15' → xem",
       "Booking 09:30-10:30 · nghỉ 15 phút",
       "- Không nghỉ: disable 09:30-10:29; slot trước gần nhất 08:30; slot sau gần nhất 10:30\n"
       "- Nghỉ trước: disable 09:15-10:29; slot trước 08:15; slot sau 10:45\n"
       "- Nghỉ sau: disable 09:30-10:44; slot trước 08:15; slot sau 10:45\n"
       "- Cả 2: disable 09:15-10:44; slot trước 07:45 (nhỏ hơn giờ mở cửa → disable hết); slot sau 10:45",
       note="Nguồn: Booking phía line user r1296, r1298, r1300, r1302 (có phép tính tay — RULE-05)."),

    tc("前後の空き時間", "INTG-CAL-001", "Boundary",
       "Event sync từ Google được xử lý y hệt booking LME về vùng nghỉ",
       SET + "\n- Giờ làm 08:00-17:00, course 1 giờ; có 1 event Google 09:30-10:30",
       "1. Không set nghỉ → LINE user xem slot\n2. Chỉ nghỉ trước 15' → xem\n"
       "3. Chỉ nghỉ sau 15' → xem\n4. Cả 2 → xem",
       "Event Google 09:30-10:30",
       "- Kết quả GIỐNG HỆT ma trận của booking LME (xem TC trước)\n"
       "- Riêng nhánh 'chỉ nghỉ trước': slot cuối cùng = giờ đóng cửa - course - nghỉ trước",
       note="Nguồn: Booking phía line user r1303-r1310. "
            "⚠ r1305 ghi slot cuối cùng có TRỪ thời gian nghỉ trước, khác với booking LME (r1297) → MT-24."),

    # ══════════════ 27. 予約・キャンセル メッセージ ══════════════
    tc("予約・キャンセル メッセージ", "MSG-004", "Normal",
       "4 mẫu tin nhắn đặt lịch có nội dung mặc định và insert được token",
       SET + "\n- Mở mục「予約・キャンセルのメッセージ・リクエストと締切」→ tab メッセージ",
       "1. Quan sát nội dung mặc định của 4 mẫu: 予約完了時 · 予約リクエスト受付時 · 予約リクエスト承認時 · "
       "予約リクエスト否認時\n"
       "2. Với mỗi mẫu, bấm「例文を挿入する」→ đối chiếu nội dung\n"
       "3. Insert 5 token 予約情報: 予約日時 · コース名 · 料金 · キャンセル用URL · 店舗名\n"
       "4. Insert token LINE名 và {name}\n5. Lưu và xem tin nhắn thực tế phía LINE user",
       "4 mẫu tin nhắn",
       "- 4 mẫu có nội dung mặc định như design\n"
       "- Bấm 例文を挿入する: điền đúng mẫu tương ứng của từng loại\n"
       "- 5 token sinh ra: [SALON_CALENDAR_date_time] · [SALON_CALENDAR_course] · "
       "[SALON_CALENDAR_reservation_currency] · [SALON_CALENDAR_url_cancel] · [SALON_CALENDAR_reservation_name]\n"
       "- LINE user nhận tin nhắn với dữ liệu thật đã thay thế đúng",
       note="Nguồn: Setting calendar r91-r101, r115-r121, r135-r141, r152-r158, r167. RULE-06."),

    tc("予約・キャンセル メッセージ", "MSG-004", "Boundary",
       "Validate độ dài tin nhắn 5000 ký tự và trường hợp vượt sau khi thay token",
       SET + "\n- Đang ở tab メッセージ của 1 trong 4 mẫu",
       "1. Nhập 5000 ký tự tiếng Nhật → lưu\n2. Nhập 5001 ký tự → lưu\n"
       "3. Nhập < 5000 ký tự nhưng sau khi thay token thì vượt 5000 → lưu → cho LINE user đặt lịch",
       "Chuỗi 5000 và 5001 ký tự · nội dung có token dài",
       "- B1: lưu thành công\n- B2: Invalid\n"
       "- B3: GUI vẫn lưu thành công nhưng khi gửi cho LINE user thì LỖI → lỗi hiện ở màn error msg",
       note="Nguồn: Setting calendar r103-r105, r124-r125, r144-r145, r161-r162."),

    tc("予約・キャンセル メッセージ", "MSG-004", "Normal",
       "Tuỳ chọn 利用しない: disable ô nhập và không gửi tin nhắn",
       SET,
       "1. Chọn「利用しない」ở 1 mẫu → quan sát ô nhập\n2. Lưu\n"
       "3. Cho LINE user thực hiện hành động tương ứng → kiểm tra tin nhắn\n"
       "4. Nếu có multi action → kiểm tra multi action",
       "1 mẫu tin nhắn",
       "- Ô nhập text bị disable\n- LINE user KHÔNG nhận tin nhắn text\n"
       "- Multi action (nếu có) VẪN chạy",
       note="Nguồn: Setting calendar r102, r122, r319."),

    tc("予約・キャンセル メッセージ", "DATA-REF-001", "Abnormal",
       "Insert friend info rồi XÓA friend info đó → chỉ mất phần token, phần còn lại vẫn gửi",
       SET + "\n- Tin nhắn đã insert token của friend info FI-1 và FI-2",
       "1. Xóa friend info FI-1 → cho LINE user đặt lịch → đọc tin nhắn\n"
       "2. Đổi TÊN friend info FI-2 → đặt lịch → đọc tin nhắn\n"
       "3. Đổi folder chứa FI-2 → đặt lịch → đọc tin nhắn\n"
       "4. XÓA folder chứa FI-2 → đặt lịch → đọc tin nhắn",
       "2 friend info",
       "- B1: token của FI-1 KHÔNG được gửi, các nội dung còn lại vẫn gửi bình thường\n"
       "- B2, B3: vẫn gửi được nội dung của friend info đó\n"
       "- B4: token của friend info trong folder bị xóa KHÔNG được gửi, phần còn lại vẫn gửi",
       note="Nguồn: Setting calendar r97-r100, r120, r140, r157."),

    tc("予約・キャンセル メッセージ", "FRIEND-001", "Normal",
       "Modal chọn friend info để insert: đồng bộ danh sách với màn quản lý friend info",
       SET + "\n- Modal insert friend info đang mở",
       "1. Quan sát danh sách folder (thứ tự, scroll, tên dài)\n"
       "2. Chọn folder khác → quan sát danh sách friend info\n"
       "3. Chuyển qua lại nhiều folder\n"
       "4. Ở màn quản lý friend info: thêm / sửa / xóa 1 item → mở lại modal\n"
       "5. Double-click nút「メッセージに挿入」\n6. Bấm 戻る / X",
       "Nhiều folder và item friend info",
       "- Danh sách folder và item khớp thứ tự ở màn quản lý friend info; scroll được; tên dài xuống dòng\n"
       "- Chuyển folder: clear item của folder cũ\n"
       "- Thêm/sửa/xóa ở màn friend info phản ánh đúng vào modal\n"
       "- Double-click: chỉ insert 1 lần\n- 戻る/X: đóng modal",
       note="Nguồn: Setting calendar r168-r179."),

    tc("予約・キャンセル メッセージ", "MSG-004", "Normal",
       "4 mẫu tin nhắn hủy lịch và nhánh 予約後のキャンセル不可",
       SET + "\n- Mở mục cài đặt hủy lịch",
       "1. Với 4 mẫu キャンセル完了時 · キャンセルリクエスト受付時 · キャンセルリクエスト承認時 · "
       "キャンセルリクエスト否認時: bấm 例文を挿入する → lưu\n"
       "2. Cho LINE user thực hiện luồng hủy tương ứng → đọc tin nhắn\n"
       "3. Chọn「予約後のキャンセル不可」→ LINE user mở detail booking",
       "4 mẫu tin nhắn hủy",
       "- 4 mẫu insert đúng nội dung mẫu tương ứng\n"
       "- LINE user nhận tin đúng ở từng bước của luồng hủy\n"
       "- Chọn không cho hủy: màn detail lịch sử của LINE user KHÔNG hiện nút hủy",
       note="Nguồn: Setting calendar r318, r337, r356, r374, r386."),

    # ══════════════ 28. 予約・キャンセル アクション ══════════════
    tc("予約・キャンセル アクション", "FUNC-001", "Normal",
       "Modal multi action mở đủ 9 loại action (không có remind)",
       SET + "\n- Mở tab アクション của 1 mẫu",
       "1. Khi chưa set action → quan sát\n2. Bấm「アクション登録・編集」→ liệt kê các loại action",
       "-",
       "- Chưa set: hiện text「エルメアクションが登録されていません」\n"
       "- Modal có đủ 9 loại: ステップ · テンプレート · テキスト · タグ · リッチメニュー · ブックマーク · "
       "友だち情報 · 対応ステータス · ブロック (KHÔNG có action remind)",
       note="Nguồn: Setting calendar r106-r107, r126-r127, r146-r147, r163-r164, r323-r324, r342-r343."),

    tc("予約・キャンセル アクション", "DATA-DB-001", "Normal",
       "Sửa / xóa multi action lưu ngay không cần bấm save ở cuối màn",
       SET + "\n- Mẫu tin nhắn đã có multi action gồm 2 action",
       "1. Sửa 1 action trong modal → bấm save của MODAL (không bấm save cuối màn) → kiểm tra DB\n"
       "2. Xóa 1 action → save modal → kiểm tra DB\n"
       "3. Xóa TẤT CẢ action → save modal → kiểm tra DB",
       "2 multi action",
       "- Sửa: `setting_action_id` giữ nguyên, bảng `t_actions_detail` cập nhật ngay\n"
       "- Xóa 1: `setting_action_id` giữ nguyên, bản ghi tương ứng bị xóa khỏi `t_actions_detail`\n"
       "- Xóa hết: `calendar_salon_setting_send_messages.setting_action_id` = NULL và "
       "dữ liệu `t_actions_detail` bị xóa",
       note="Nguồn: Setting calendar r111-r113, r131-r133, r328-r330, r347-r349, r365-r367, r383-r385."),

    tc("予約・キャンセル アクション", "FUNC-001", "Normal",
       "Cài đặt 予約時の確認方法 (approve_type) quyết định trạng thái booking mới",
       SET + "\n- Mở mục「各種設定」",
       "1. Chọn tự động duyệt (approve_type = 1) → LINE user đặt lịch\n"
       "2. Chọn admin duyệt thủ công (approve_type = 2) → LINE user đặt lịch\n"
       "3. Chọn không cho hủy (approve_type = 3) → LINE user đặt lịch rồi thử hủy",
       "3 giá trị approve_type",
       "- (1): booking vào thẳng「予約確定」, gửi action 予約完了時\n"
       "- (2): booking vào「予約リクエスト」, gửi action リクエスト受付時; admin duyệt mới thành 予約確定\n"
       "- (3): booking vào 予約確定; LINE user không có nút hủy",
       note="Nguồn: Spec Field #39 + Setting calendar r386 + Booking phía line user r1233-r1236."),

    # ══════════════ 29. 予約の開始・締切 ══════════════
    tc("予約の開始・締切", "FUNC-DATE-001", "Normal",
       "Cài đặt thời gian BẮT ĐẦU nhận booking — 3 kiểu",
       SET + "\n- Mở mục「予約の開始・締切」",
       "1. Giữ mặc định (option 1: nhận đến khi bắt đầu course) → LINE user xem lịch\n"
       "2. Chọn option 2 kiểu chỉ định ngày+giờ (trước 1 ngày lúc 23:59) → xem lịch\n"
       "3. Chọn option 3 kiểu duration (trước X giờ Y phút) → xem lịch",
       "3 kiểu cài đặt",
       "- Option 1 (`start_receive_booking_type` = 1): LINE user đặt được mọi lúc cho đến khi dừng nhận; "
       "nếu không set hạn thì đặt được đến giờ bắt đầu ca\n"
       "- Option 2: ví dụ course bắt đầu 10:00 ngày 04/03 → đặt được từ 23:59 ngày 03/03\n"
       "- Option 3: đặt được trước đúng khoảng duration đã cài",
       note="Nguồn: Setting calendar r180-r181, r205-r208."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "Validate số ngày (1~180) và giờ (00:00~23:59) của thời gian bắt đầu nhận",
       SET + "\n- Đang ở option 2 kiểu chỉ định ngày",
       "1. Nhập số ngày = 1 → lưu\n2. Nhập 180 → lưu\n3. Bỏ trống ô ngày → lưu\n"
       "4. Nhập 0 → lưu\n5. Nhập 181 → lưu\n6. Nhập số âm / số thực / chữ\n"
       "7. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → lưu\n8. Bỏ trống ô giờ → lưu\n"
       "9. Nhập 24:60 → lưu\n10. Nhập ký tự không phải số vào ô giờ",
       "1 · 180 · 0 · 181 · -1 · 1.5 · abc · 4 mốc giờ · 24:60",
       "- B1, B2: lưu thành công (`before_booking_day` = 1 / 180)\n"
       "- B3, B4: lỗi「1日から入力してください」\n- B5: lỗi「設定できるのは最大180日前からになります」\n"
       "- B6: không cho nhập\n- B7: cả 4 mốc lưu thành công\n"
       "- B8: tự lưu `before_booking_hour` = 00:00:00\n"
       "- B9: Invalid, tự fill 23:59\n- B10: Invalid, tự fill giá trị default",
       note="Nguồn: Setting calendar r182-r194."),

    tc("予約の開始・締切", "FUNC-DATE-001", "Boundary",
       "Kiểm chứng thực tế mốc thời gian bắt đầu nhận với 4 cấu hình",
       SET + "\n- Đã set option 2 kiểu chỉ định ngày",
       "1. before_booking_day = 1, hour = 15:30 → xem lịch lúc 15:27 ngày 03/07, rồi lúc 15:30\n"
       "2. before_booking_day = 3, hour = 00:00 → xem lịch lúc 16:01 ngày 03/07\n"
       "3. before_booking_day = 40, hour = 09:15 → xem lịch lúc 17:56 ngày 03/07\n"
       "4. before_booking_day = 180, hour = 23:59 → xem lịch lúc 18:48 ngày 03/07",
       "4 cấu hình như mô tả",
       "- B1: lúc 15:27 hiện được đến 18:30 ngày 03/07; đến 15:30 thì hiện từ 16:00 ngày 03/07 trở đi\n"
       "- B2: hiện từ 16:30 ngày 03/07 đến 18:30 ngày 06/07\n"
       "- B3: hiện từ 18:00 ngày 03/07 đến 18:30 ngày 12/08\n"
       "- B4: hiện booking đến 18:30 ngày 29/12",
       note="Nguồn: Setting calendar r195-r198 (có phép tính tay theo ngày giờ cụ thể — RULE-05)."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "Validate kiểu duration (giờ 00~23, phút 00~59)",
       SET + "\n- Đang ở kiểu duration",
       "1. Nhập giờ 00~23, phút 00~59 → lưu\n2. Bỏ trống ô thời gian → lưu\n"
       "3. Nhập số âm / số thực / chữ\n4. Nhập giờ > 23 → lưu\n5. Nhập phút > 59 → lưu\n"
       "6. Test thực tế: (0h30) · (1h30) · (5h50) · (23h59)",
       "Các cấu hình như mô tả",
       "- B1: lưu vào `booking_time_from` / `booking_time_to`\n"
       "- B2: tự lưu cả 2 = 0\n- B3: không cho nhập\n"
       "- B4, B5: lỗi「設定できるのは23時間59分以内です」\n"
       "- B6: đặt được trước đúng khoảng duration đã cài (đối chiếu bằng đồng hồ thật)",
       note="Nguồn: Setting calendar r199-r208."),

    tc("予約の開始・締切", "FUNC-DATE-001", "Boundary",
       "Cài đặt thời gian DỪNG nhận booking và kiểm chứng thực tế",
       SET,
       "1. Chọn「締切を設定しない（コース開始まで予約可能）」→ LINE user xem lịch\n"
       "2. deadline_before_booking_day = 1, hour = 19:00 → xem lịch lúc 19:28 ngày 03/07\n"
       "3. day = 1, hour = 20:00 → xem lịch lúc 19:30 ngày 03/07\n"
       "4. day = 36, hour = 00:00 → xem lịch lúc 11:00 ngày 04/07\n"
       "5. day = 180, hour = 23:59 → xem lịch lúc 11:00 ngày 04/07",
       "4 cấu hình như mô tả",
       "- B1: đặt được đến khi khóa học bắt đầu\n"
       "- B2: hiện booking từ ngày 05/07 trở đi (ẩn 03/07 và 04/07)\n"
       "- B3: hiện từ ngày 04/07 trở đi\n"
       "- B4: hiện từ ngày 10/08 trở đi (đã quá giờ setting thì phải next thêm 1 ngày)\n"
       "- B5: hiện từ ngày 31/12 trở đi",
       note="Nguồn: Setting calendar r210, r220-r223."),

    tc("予約の開始・締切", "FUNC-004", "Boundary",
       "Validate số ngày dừng nhận (0~180) khác với bắt đầu nhận (1~180)",
       SET,
       "1. Nhập số ngày = 0 → lưu\n2. Nhập 180 → lưu\n3. Bỏ trống → lưu\n4. Nhập 181 → lưu\n"
       "5. Nhập số âm / số thực / chữ",
       "0 · 180 · rỗng · 181",
       "- B1: lưu thành công (khác với ô bắt đầu nhận: 0 là INVALID)\n- B2: thành công\n"
       "- B3: lỗi「0日から入力してください」\n- B4: lỗi「設定できるのは最大180日前からになります」\n"
       "- B5: không cho nhập",
       note="Nguồn: Setting calendar r211-r215. ⚠ r211 ghi「Nhập 0 → save success => deadline_before_"
            "booking_day = 1」— giá trị lưu KHÔNG khớp giá trị nhập, cần verify, xem MT-25."),

    tc("予約の開始・締切", "FUNC-DATE-001", "Abnormal",
       "Chặn cấu hình dừng nhận SỚM HƠN bắt đầu nhận",
       SET,
       "1. Bắt đầu nhận: trước 2 ngày lúc 12:00; dừng nhận: trước 3 ngày lúc 12:00 → lưu\n"
       "2. Bắt đầu: trước 1 ngày lúc 20:00; dừng: 23:59 → lưu\n"
       "3. Bắt đầu: 10:00; dừng: 12:00 → lưu\n"
       "4. Bắt đầu: 23:59; dừng: trước 2 ngày lúc 20:00 → lưu",
       "4 cấu hình như mô tả",
       "- B1, B3, B4: lỗi「予約締切は予約開始よりも後に設定してください」\n- B2: lưu thành công",
       note="Nguồn: Setting calendar r232-r235."),

    tc("予約の開始・締切", "FUNC-DATE-001", "Boundary",
       "Thời hạn HỦY booking (変更の締切) — validate và kiểm chứng thực tế",
       SET + "\n- Mở mục「変更の締切」",
       "1. Chọn không giới hạn → LINE user xem detail booking\n"
       "2. Nhập số ngày = 0 / rỗng → lưu\n3. Nhập 1, 180 → lưu\n4. Nhập 181 → lưu\n"
       "5. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → lưu\n"
       "6. Test thực tế: booking 15:00 ngày 22/07, hiện tại 12:15 ngày 20/07, với các cấu hình "
       "deadline khác nhau (cùng ngày và qua ngày)",
       "Các cấu hình như mô tả",
       "- B1: hủy được đến khi khóa học bắt đầu; quá giờ thì màn detail KHÔNG hiện nút hủy\n"
       "- B2: lỗi「1日から入力してください」\n- B3: lưu thành công\n"
       "- B4: lỗi「設定できるのは最大180日前からになります」\n- B5: 4 mốc đều lưu được\n"
       "- B6: quá hạn → lỗi「キャンセルできません。」; chưa quá hạn → hủy được",
       note="Nguồn: Setting calendar r387-r409."),

    # ══════════════ 30. 1人あたりの予約上限 ══════════════
    tc("1人あたりの予約上限", "DATA-COUNT-001", "Normal",
       "Giới hạn số booking đồng thời của 1 người — mặc định và ý nghĩa 'đồng thời'",
       SET + "\n- Mở mục「オプション設定」→ giới hạn nhận booking cho 1 user",
       "1. Set limit = 1 → khách F1 đặt 1 booking lúc 10:00 ngày 28/4\n"
       "2. F1 thử đặt tiếp (cùng course, khác course, khác staff, staff không chỉ định) ở màn tuần và tháng\n"
       "3. Chờ qua 10:00 ngày 28/4 → F1 đặt lại\n"
       "4. Set limit = 2 → F1 đặt booking A (10:00) và B (12:00) cùng ngày 28/4 → thử đặt tiếp\n"
       "5. Sau khi qua 10:00 ngày 28/4 → F1 đặt lại",
       "limit = 1 và 2",
       "- limit 1: từ lúc đặt đến 10:00 ngày 28/4, mọi lối đặt tiếp đều báo lỗi giới hạn\n"
       "- Sau khi qua giờ booking cũ: đặt lại thành công\n"
       "- limit 2: sau khi có A và B thì bị chặn; qua 10:00 thì được đặt thêm 1 lần nữa",
       note="Nguồn: Setting calendar r238-r244."),

    tc("1人あたりの予約上限", "OUT-TRUTH-001", "Normal",
       "Text báo lỗi khi đạt giới hạn — theo cài đặt mới và calendar cũ",
       SET + "\n- limit = 1; khách F1 đã có 1 booking",
       "1. Calendar CŨ chưa set text (`text_limit_book_each_customer` = NULL) → F1 đặt tiếp\n"
       "2. Nhập text hướng dẫn「受付制限に達している場合の案内テキスト」→ lưu → F1 đặt tiếp",
       "Calendar có/không có text tuỳ chỉnh",
       "- Chưa set text: hiện lỗi mặc định (theo spec update 2026-03-26)\n"
       "- Đã set text: hiện đúng text admin đã nhập",
       note="Nguồn: Setting calendar r238-r242 (Spec update 2026-03-26, SpecImprove #35407). "
            "⚠ Corpus ghi 2 chuỗi lỗi khác nhau ở 2 thời điểm:「この予約の受付制限中ですので、予約できません。」"
            "và「1人あたりの予約受付上限に…」→ cần verify text hiện tại, xem MT-26."),

    tc("1人あたりの予約上限", "DATA-COUNT-001", "Boundary",
       "Trạng thái booking nào được tính vào giới hạn của 1 người",
       SET + "\n- limit = 1; khách F1 đã có 1 booking ở trạng thái cần kiểm tra",
       "1. Booking cũ ở status 1 (user đặt, đã duyệt) → F1 đặt tiếp\n"
       "2. status 2 (admin book) → đặt tiếp\n3. status 0 (đợi duyệt) → đặt tiếp\n"
       "4. status 5 (đợi hủy) → đặt tiếp\n5. status 4, 7 (đã hủy) → đặt tiếp\n"
       "6. status 3 (đợi thông báo) → đặt tiếp\n7. status 6 (bị từ chối) → đặt tiếp",
       "Booking ở đủ 7 trạng thái",
       "- status 1, 2, 5: KHÔNG đặt được nữa (được tính vào giới hạn)\n"
       "- status 0, 3, 4, 6, 7: VẪN đặt được (không tính vào giới hạn)",
       note="Nguồn: Setting calendar r245-r251."),

    tc("1人あたりの予約上限", "DATA-COUNT-001", "Normal",
       "Chọn 制限なし → LINE user đặt thoải mái miễn còn slot",
       SET,
       "1. Chọn「制限なし」(`limit_book_each_customer` = 0) → lưu\n"
       "2. Khách F1 đặt liên tiếp 5 booking ở các khung khác nhau",
       "limit_book_each_customer = 0",
       "- Cả 5 booking đều thành công (chỉ bị chặn khi hết slot)",
       note="Nguồn: Setting calendar r252."),

    # ══════════════ 31. 予約時のお客様への質問項目 ══════════════
    tc("予約時のお客様への質問項目", "UI-FIELD-001", "Normal",
       "2 trường mặc định 名前 và メール của calendar mới",
       SET + "\n- Calendar vừa được tạo, lần đầu mở tab 質問項目",
       "1. Quan sát danh sách item mặc định\n2. Thử bỏ chọn / xóa 2 item này\n"
       "3. Bật 決済連携 → quan sát 2 item này\n4. Tắt 決済連携 → quan sát",
       "Calendar mới",
       "- Có sẵn 2 item: system name (friend_information_id = -1) và email (-3)\n"
       "- Khi BẬT 決済: 2 item TỰ ĐỘNG được bật và đặt bắt buộc, không tắt được\n"
       "- Khi tắt 決済: 2 item có thể tắt lại",
       note="Nguồn: Setting calendar r774-r784 (SpecChange #26462, 08/2024) + Spec BR-05."),

    tc("予約時のお客様への質問項目", "UI-FIELD-001", "Abnormal",
       "Bật 決済 khi 2 trường mặc định đang tắt → báo lỗi hướng dẫn",
       SET + "\n- Đã liên kết Stripe/UnivaPay\n- Đã TẮT cả 2 item name và email ở tab 質問項目",
       "1. Vào tab 決済連携 → bật「決済機能の利用」→ lưu\n2. Đọc thông báo lỗi",
       "2 item mặc định đang tắt",
       "- Lỗi「予約時のお客様への質問項目にメールとお名前を追加してから、有効してください。」\n"
       "- Không bật được 決済",
       note="Nguồn: Liên kết bill tiền r15. Spec BR-05."),

    tc("予約時のお客様への質問項目", "FRIEND-001", "Normal",
       "Tạo item câu hỏi 5 kiểu và cấu hình liên kết friend info",
       SET + "\n- Mở tab「予約時のお客様への質問項目」",
       "1. Tạo lần lượt item kiểu: 短文回答 · 長文回答 · 単一選択 · 複数選択 · 日時\n"
       "2. Với mỗi item: nhập nội dung câu hỏi, chọn bắt buộc/không, chọn đích liên kết friend info\n"
       "3. Lưu và kiểm tra thứ tự hiển thị ở tab\n"
       "4. Kiểm tra hiển thị phía LINE user khi đặt lịch",
       "5 kiểu item",
       "- 5 item tạo thành công và hiển thị đúng kiểu ở màn LINE user "
       "(text / textarea / radio hoặc dropdown / checkbox / date picker)\n"
       "- Thứ tự hiển thị ở LINE user khớp thứ tự ở tab cài đặt",
       note="Nguồn: Setting calendar r415-r688 (3.1 Tạo item) + Quản lý calendar r1062-r1093."),

    tc("予約時のお客様への質問項目", "FRIEND-001", "Normal",
       "Sửa item câu hỏi — dữ liệu cũ và câu trả lời đã có",
       SET + "\n- Có item「お電話番号」đã có câu trả lời của khách F1",
       "1. Sửa nội dung câu hỏi → lưu → kiểm tra ở LINE user và ở detail booking cũ\n"
       "2. Đổi đích liên kết friend info → lưu → cho F1 đặt lịch mới → kiểm tra friend info\n"
       "3. Đổi kiểu item (nếu cho phép) → quan sát",
       "Item có câu trả lời cũ",
       "- Câu trả lời của booking cũ giữ nguyên\n"
       "- Booking mới ghi vào đích liên kết mới\n"
       "- Ràng buộc đổi kiểu item được xử lý rõ ràng (cho hoặc chặn, không lỗi)",
       note="Nguồn: Setting calendar r689-r773 (3.2 Edit item), r890-r985."),

    tc("予約時のお客様への質問項目", "FRIEND-001", "Abnormal",
       "Support #29272: item 日時 CÓ giờ + chọn 自動で友だち情報を生成 → xử lý ra sao",
       SET + "\n- Mở tab 質問項目",
       "1. Tạo item kiểu 日時 CÓ chọn hiển thị giờ\n"
       "2. Chọn「自動で友だち情報を生成して回答を記録」→ lưu\n"
       "3. Cho LINE user đặt lịch điền item này → kiểm tra friend info sinh ra",
       "Item 日時 có giờ",
       "- Hệ thống xử lý nhất quán: hoặc chặn cấu hình này, hoặc sinh friend info kiểu phù hợp\n"
       "- KHÔNG được lưu sai định dạng hoặc mất dữ liệu giờ",
       spec="Đã hỏi leader",
       note="Nguồn: Setting calendar r793 (Support #29272, 23/03/2025) + Quản lý calendar r1090. "
            "⚠ Corpus ghi「Case này sẽ ko thể gán vào friend info nào trong hệ thống cả」nhưng "
            "Support #29272 lại nói về nhánh tự sinh → cần Leader chốt, xem MT-27."),

    tc("予約時のお客様への質問項目", "UI-001", "Abnormal",
       "Bug #30053: tên friend info liên kết dài gây lỗi UI",
       SET + "\n- Có friend info với tên rất dài (≥ 50 ký tự)",
       "1. Tạo item và liên kết với friend info tên dài → lưu\n"
       "2. Quan sát hiển thị ở tab 質問項目\n3. Quan sát ở màn LINE user\n4. Kiểm tra ở lesson calendar",
       "Friend info tên ≥ 50 ký tự",
       "- Tên dài xuống dòng hoặc cắt gọn, KHÔNG vỡ layout ở cả salon và lesson",
       note="Nguồn: Setting calendar r2009-r2013 (Bug #30053)."),

    tc("予約時のお客様への質問項目", "STATE-001", "Abnormal",
       "Bug #29678: item không lưu được từ lần đầu, lần thứ 2 mới lưu",
       SET,
       "1. Tạo item mới, chọn liên kết friend info → bấm lưu LẦN ĐẦU\n"
       "2. Reload màn → kiểm tra item vừa tạo\n3. Nếu chưa có, bấm lưu lần 2 → kiểm tra",
       "Item có chọn liên kết friend info",
       "- Item phải được lưu NGAY LẦN ĐẦU\n- Sau reload, item và liên kết friend info hiển thị đúng",
       note="Nguồn: Setting calendar r1992-r2003 (Bug #29678, 22/04/2025)."),

    # ══════════════ 32. リマインド — cài đặt ══════════════
    tc("リマインド — cài đặt", "UI-001", "Normal",
       "Màn setting remind: remind mặc định và cách hiển thị 2 nhóm",
       SET + "\n- Calendar vừa tạo, lần đầu mở tab「予約前後に送るリマインドメッセージ」",
       "1. Quan sát nhóm remind TRƯỚC khi bắt đầu\n2. Quan sát nhóm remind SAU khi kết thúc\n"
       "3. Với calendar tạo mới nhưng CHƯA mở tab lần nào → kiểm tra DB\n4. Mở tab lần đầu → kiểm tra DB",
       "Calendar mới",
       "- Nhóm trước: có 1 remind mặc định gửi trước 1 ngày lúc 10:00; cuối danh sách là marker「コース開始」\n"
       "- Nhóm sau: đầu danh sách là marker「コース終了」; có 1 remind mặc định gửi sau 1 ngày lúc 10:00\n"
       "- Remind mặc định chỉ được TẠO khi mở tab lần đầu, không tạo lúc tạo calendar",
       note="Nguồn: Setting calendar r988-r989, r1022-r1023."),

    tc("リマインド — cài đặt", "UI-001", "Normal",
       "Định dạng hiển thị của mỗi remind theo 2 kiểu thời gian và trạng thái filter",
       SET + "\n- Đã tạo remind kiểu chỉ định ngày giờ và remind kiểu duration; 1 remind có filter",
       "1. Quan sát dòng remind kiểu chỉ định ngày giờ (nhóm trước và nhóm sau)\n"
       "2. Quan sát dòng remind kiểu duration (nhóm trước và nhóm sau)\n"
       "3. Quan sát remind CÓ filter và remind KHÔNG filter\n4. Rê chuột vào 1 remind",
       "4 remind",
       "- Nhóm trước, chỉ định ngày giờ:「予約開始 1日前の 15時00分」\n"
       "- Nhóm trước, duration:「予約開始 03 時間 00 分 前」\n"
       "- Nhóm sau, chỉ định ngày giờ:「予約終了 1日後の 10時00分」\n"
       "- Nhóm sau, duration:「予約終了 03 時間 00 分 前」\n"
       "- Có filter:「絞り込みが設定されています」; không filter:「絞り込みは設定されていません」\n"
       "- Rê chuột: hiện nút preview/edit màu #5799DBCC đè lên remind",
       note="Nguồn: Setting calendar r990-r994, r1024-r1028."),

    tc("リマインド — cài đặt", "LIST-001", "Normal",
       "SpecImprove #36037: thứ tự sắp xếp remind KHÁC NHAU giữa nhóm trước và nhóm sau",
       SET + "\n- Nhóm trước và nhóm sau đều có: 2 remind chỉ định ngày (khác ngày và cùng ngày khác giờ) "
             "và 2 remind duration khác giờ",
       "1. Quan sát thứ tự trong nhóm TRƯỚC khi bắt đầu\n"
       "2. Quan sát thứ tự trong nhóm SAU khi kết thúc\n"
       "3. Tạo mới / sửa giờ / xóa 1 remind → kiểm tra lại thứ tự",
       "4 remind mỗi nhóm",
       "- Nhóm TRƯỚC: remind chỉ định ngày xếp TRÊN remind duration; trong nhóm chỉ định ngày, "
       "ngày lớn hơn ở trên; trong nhóm duration, giờ lớn hơn ở trên\n"
       "- Nhóm SAU: remind duration xếp TRÊN remind chỉ định ngày; ngày nhỏ hơn ở trên; "
       "giờ nhỏ hơn ở trên\n"
       "- Sau khi tạo/sửa/xóa: thứ tự tự sắp xếp lại đúng quy tắc",
       note="Nguồn: Setting calendar r987, r996-r1001, r1030-r1035 (SpecImprove #36037, 22/04/2026). "
            "⚠ r998 ghi CẢ「giờ lớn hơn hiện ở trên」và「Giờ nhỏ hơn hiện ở trên」→ mâu thuẫn nội bộ, "
            "xem MT-28."),

    tc("リマインド — cài đặt", "OUT-PREVIEW-001", "Normal",
       "Popup preview remind: nội dung message, action và filter",
       SET + "\n- Có 1 remind đã set message + 2 action + filter theo course và staff",
       "1. Bấm「プレビュー・編集」→ quan sát animation và tiêu đề\n"
       "2. Xem tab メッセージ khi có nội dung và khi chọn không sử dụng\n"
       "3. Xem tab アクション khi có và không có action\n"
       "4. Bấm hyperlink「絞り込みが設定されています」\n"
       "5. Bấm「編集する」\n6. Bấm X",
       "1 remind đầy đủ cấu hình",
       "- Popup trượt từ phải vào giữa, tiêu đề「予約開始前のメッセージ・アクション」"
       "(hoặc「コース終了後の…」với nhóm sau)\n"
       "- Tab メッセージ: có nội dung → hiện nội dung; chọn không dùng →「メッセージが登録されていません」\n"
       "- Tab アクション: không có →「アクションが登録されていません」; có → liệt kê action, scroll dọc; "
       "action có filter thì hiện nút filter\n"
       "- Hyperlink filter: mở popup hiển thị system name của course/staff đã chọn; "
       "phần không set hiện「絞り込みは設定されていません」\n"
       "- 編集する: mở màn edit remind; X: đóng popup",
       note="Nguồn: Setting calendar r995, r1002-r1014, r1036-r1045."),

    tc("リマインド — cài đặt", "FUNC-004", "Boundary",
       "Validate khi tạo remind: số ngày và giờ",
       SET + "\n- Bấm「送信タイミングを追加する」→ popup chọn timing",
       "1. Chọn kiểu 日時で指定: bỏ trống ô ngày → lưu\n2. Nhập 0 → lưu\n3. Nhập 100 → lưu\n"
       "4. Nhập số không nguyên / số âm\n5. Nhập giờ 00:00 / 00:30 / 15:15 / 23:59 → lưu\n"
       "6. Chọn kiểu 経過時間で指定: bỏ trống ô giờ → lưu",
       "0 · 100 · số âm · 4 mốc giờ",
       "- B1: lỗi「日時を入力してください。」\n- B2, B3: lưu thành công\n"
       "- B4: chặn không cho nhập\n- B5: cả 4 mốc lưu thành công\n"
       "- B6: lỗi「時間を入力してください。」",
       note="Nguồn: Setting calendar r1049-r1060."),

    tc("リマインド — cài đặt", "MSG-002", "Normal",
       "Ý nghĩa 2 kiểu thời gian gửi remind — kiểm chứng bằng thời điểm gửi thật",
       SET + "\n- Course bắt đầu 10:00 ngày 20/4",
       "1. Tạo remind kiểu 日時で指定: trước 1 ngày lúc 08:00 → cho LINE user đặt lịch\n"
       "2. Tạo remind kiểu 経過時間で指定: trước 1 giờ 00 phút → cho LINE user đặt lịch\n"
       "3. Kiểm tra `event_step_time.sent_date_time` của từng remind\n"
       "4. Chờ đến giờ → kiểm tra tin nhắn LINE user nhận",
       "Course 10:00 ngày 20/4",
       "- Remind 1: `sent_date_time` = 08:00 ngày 19/4\n"
       "- Remind 2: `sent_date_time` = 09:00 ngày 20/4\n"
       "- LINE user nhận đúng tin ở đúng thời điểm",
       note="Nguồn: Setting calendar r1049, r1059. Spec BR-08. RULE-06 + RULE-07."),

    tc("リマインド — cài đặt", "MSG-002", "Boundary",
       "Change spec: remind sau kết thúc tính theo END_TIME của booking",
       SET + "\n- Booking 10:00-11:00 ngày 20/4",
       "1. Tạo remind nhóm SAU: sau 1 giờ → cho LINE user đặt lịch\n"
       "2. Kiểm tra `event_step_time.sent_date_time`\n"
       "3. Kiểm tra cờ `is_after_day` trong bảng `event_step`",
       "Booking 10:00-11:00",
       "- Remind nhóm SAU tính theo end_time → `sent_date_time` = 12:00 ngày 20/4\n"
       "- Remind nhóm TRƯỚC tính theo start_time (`is_after_day` = 0)",
       note="Nguồn: Setting calendar r1217-r1297 (comment 16, 18: change spec tính theo end_time)."),

    # ══════════════ 33. リマインド — job gửi ══════════════
    tc("リマインド — job gửi", "JOB-001", "Normal",
       "Sinh bản ghi remind theo lối đặt lịch và trạng thái booking",
       SET + "\n- Calendar đã bật remind",
       "1. Admin đặt lịch → kiểm tra `event_step_time`\n"
       "2. LINE user đặt lịch được duyệt ngay → kiểm tra\n"
       "3. LINE user đặt lịch chờ duyệt → kiểm tra ngay sau khi đặt\n"
       "4. Admin duyệt booking đó → kiểm tra\n5. Admin từ chối booking → kiểm tra\n"
       "6. LINE user đặt vào slot chờ thông báo (status 3) → kiểm tra",
       "6 kịch bản đặt lịch",
       "- B1, B2: insert bản ghi remind ngay\n- B3: CHƯA insert\n"
       "- B4: insert sau khi duyệt\n- B5, B6: KHÔNG insert",
       note="Nguồn: Setting calendar r1149-r1154."),

    tc("リマインド — job gửi", "JOB-001", "Normal",
       "Xóa bản ghi remind khi hủy booking",
       SET + "\n- Calendar đã bật remind; có booking đã sinh remind",
       "1. Admin hủy booking → kiểm tra `event_step_time`\n"
       "2. LINE user hủy được duyệt ngay → kiểm tra\n"
       "3. LINE user gửi yêu cầu hủy (chưa duyệt) → kiểm tra\n"
       "4. Admin duyệt yêu cầu hủy → kiểm tra\n5. Admin từ chối yêu cầu hủy → kiểm tra",
       "Booking đã có remind",
       "- B1, B2, B4: XÓA bản ghi remind\n- B3, B5: KHÔNG xóa",
       note="Nguồn: Setting calendar r1159-r1163."),

    tc("リマインド — job gửi", "MSG-003", "Abnormal",
       "Khách bị bot block: không gửi được remind",
       SET + "\n- Calendar đã bật remind",
       "1. Khách F1 bị block (`bot_line_user.is_block` = 1) → thử đặt lịch\n"
       "2. Khách F2 đặt lịch thành công → sau đó bot block F2 → chờ đến giờ remind\n"
       "3. Trong lúc F2 đang bị block, thêm/sửa remind hợp lệ → kiểm tra `event_step_time`",
       "F1 bị block trước · F2 bị block sau khi đặt",
       "- B1: F1 KHÔNG đặt được, không sinh remind\n"
       "- B2: remind đã có trong bảng nhưng đến giờ KHÔNG gửi\n"
       "- B3: vẫn insert bản ghi remind nhưng đến giờ không gửi",
       note="Nguồn: Setting calendar r1155-r1158."),

    tc("リマインド — job gửi", "MSG-001", "Boundary",
       "Filter remind theo course/staff quyết định có sinh bản ghi hay không",
       SET + "\n- Remind R1 có filter course = [C1], R2 có filter staff = [S1], "
             "R3 có filter cả course = [C1] và staff = [S1]",
       "1. Đặt lịch với course C1, staff S2 → kiểm tra bản ghi remind của R1, R2, R3\n"
       "2. Đặt lịch với course C2, staff S1 → kiểm tra\n"
       "3. Đặt lịch với course C1, staff S1 → kiểm tra\n"
       "4. Đặt lịch với course C2, staff S2 → kiểm tra\n"
       "5. Admin đặt lịch KHÔNG chọn course/staff → kiểm tra\n"
       "6. Lặp lại cho luồng admin duyệt request",
       "3 remind có filter khác nhau",
       "- R1 (filter course): chỉ sinh khi course thuộc filter\n"
       "- R2 (filter staff): chỉ sinh khi staff thuộc filter\n"
       "- R3 (cả 2): chỉ sinh khi CẢ course VÀ staff đều thuộc filter\n"
       "- Admin không chọn course/staff: KHÔNG thỏa filter → không sinh bản ghi\n"
       "- Kết quả nhất quán giữa admin book, user book và admin duyệt request",
       note="Nguồn: Setting calendar r1164-r1187."),

    tc("リマインド — job gửi", "JOB-001", "Normal",
       "Job gửi remind thay token đúng và hiển thị đúng phía LINE user",
       SET + "\n- Remind có nội dung chứa đủ token: {name} · 予約日時 · コース · 料金 · "
             "キャンセル用URL · 店舗名 · friend info basic và friend info tự tạo",
       "1. Cho LINE user đặt lịch → chờ đến giờ remind\n"
       "2. Đọc tin nhắn nhận được trên LINE app\n3. Bấm URL hủy trong tin nhắn",
       "Booking 25/02/2026 00:00-01:00",
       "- Tất cả token được thay bằng dữ liệu thật\n"
       "- Ngày giờ format「2026年02月25日（水）00:00-01:00」(chữ（水）cùng dòng với ngày, giống web)\n"
       "- Tên course/staff, số tiền, tên calendar hiển thị đúng\n"
       "- URL hủy mở đúng màn detail booking",
       note="Nguồn: Setting calendar r1340-r1350. Spec §7.1.2 NewEventRemindTask. RULE-06."),

    tc("リマインド — job gửi", "JOB-001", "Abnormal",
       "Job gửi remind khi course/staff bị OFF — hành vi theo có/không có filter",
       SET + "\n- Có remind KHÔNG filter và remind CÓ filter course + staff",
       "1. Remind KHÔNG filter, course ON staff ON → chờ giờ remind\n"
       "2. Remind KHÔNG filter, course OFF hoặc staff OFF (4 tổ hợp) → chờ giờ remind\n"
       "3. Remind CÓ filter, 4 tổ hợp ON/OFF của course và staff → chờ giờ remind\n"
       "4. Kiểm tra hiển thị course/staff OFF ở màn cài đặt filter và preview filter",
       "2 loại remind × 4 tổ hợp ON/OFF",
       "- Remind KHÔNG filter: LUÔN gửi cho mọi booking, bất kể course/staff ON hay OFF\n"
       "- Remind CÓ filter: LUÔN gửi cho booking có course & staff thỏa filter, bất kể ON/OFF\n"
       "- Màn cài đặt filter và preview filter: VẪN hiện tên course/staff kể cả khi đang OFF",
       note="Nguồn: Setting calendar r1377-r1389 (khối mới sau Bug #30544, 02/07/2025). "
            "⚠ MÂU THUẪN với r1355/r1361/r1373-1375 cùng tab (「course OFF thì không send」) → MT-29."),

    tc("リマインド — job gửi", "MSG-002", "Normal",
       "Remind của calendar loại 個人",
       "- Calendar「サロン個人」loại 個人, đã bật remind\n- Có booking của khách F1",
       "1. Mở tab remind của calendar 個人 → quan sát phần filter staff\n"
       "2. Cho F1 đặt lịch → chờ đến giờ remind → đọc tin nhắn",
       "Calendar 個人",
       "- Phần filter staff bị ẩn hoặc không áp dụng\n- F1 nhận được remind đúng nội dung và thời điểm",
       note="Nguồn: Setting calendar r1393-r1394."),

    # ══════════════ 34. 空き枠通知受け取り設定 ══════════════
    tc("空き枠通知受け取り設定", "FUNC-001", "Normal",
       "Bật/tắt chức năng danh sách chờ và banner trạng thái",
       SET + "\n- Mở tab「空き枠通知受け取り設定」",
       "1. Quan sát trạng thái mặc định\n2. Chọn ON「受付中」→ lưu → quan sát banner\n"
       "3. Cho LINE user chọn slot đã đầy → quan sát\n4. Chọn OFF「停止中」→ lưu → LINE user thử lại",
       "Slot đã đầy",
       "- Mặc định OFF, banner「現在、空き枠通知受け取り設定は 停止中 です」\n"
       "- Bật ON: banner「…受付中 です」; LINE user đăng ký nhận thông báo được (status 3)\n"
       "- Tắt OFF: LINE user không đăng ký được nữa",
       note="Nguồn: Setting calendar r1412-r1413. EP-55/EP-56, `is_notify_full_slot`."),

    tc("空き枠通知受け取り設定", "MSG-002", "Normal",
       "Action gửi khi khách đăng ký chờ thông báo (通知受け取り申請時)",
       SET + "\n- Đã bật chức năng danh sách chờ; slot đã đầy",
       "1. Quan sát nội dung mặc định của mẫu tin nhắn\n2. Insert token LINE名 → lưu\n"
       "3. Cho LINE user đăng ký chờ → đọc tin nhắn nhận được\n"
       "4. Chọn「利用しない」→ cho LINE user đăng ký chờ → kiểm tra\n"
       "5. Không set cả text lẫn action → cho đăng ký chờ → kiểm tra\n"
       "6. Nhập 5001 ký tự → lưu",
       "Mẫu tin nhắn 通知受け取り申請時",
       "- Nội dung mặc định như design; token thay đúng\n"
       "- Chọn 利用しない: KHÔNG gửi text nhưng VẪN gửi multi action (nếu có); "
       "`calendar_management.use_message_notify_full_slot` đổi giá trị\n"
       "- Không set gì: không gửi action nào\n- 5001 ký tự: Invalid",
       note="Nguồn: Setting calendar r1414-r1432."),

    tc("空き枠通知受け取り設定", "MSG-001", "Normal",
       "Action gửi khi có slot trống (受付再開時) — gửi cho TẤT CẢ người đang chờ",
       SET + "\n- Đã bật danh sách chờ; có 3 khách F1, F2, F3 đang ở trạng thái chờ thông báo (status 3) "
             "cùng 1 slot",
       "1. Cho 1 khách đã đặt slot đó HỦY (được duyệt ngay) → quan sát tin nhắn của F1, F2, F3\n"
       "2. Khách nào nhận trước đặt trước → kiểm tra ai đặt được\n"
       "3. Admin NÂNG số lượng slot lên → quan sát tin nhắn 3 khách\n"
       "4. Trường hợp còn có khách đang 予約確定 / chờ duyệt cùng slot → quan sát ai nhận tin\n"
       "5. Tắt chức năng danh sách chờ → tạo slot trống → quan sát",
       "3 khách chờ thông báo",
       "- B1, B3: CẢ 3 khách đều nhận tin nhắn thông báo có slot trống; ai đặt trước thì được\n"
       "- B4: CHỈ khách đang chờ thông báo nhận tin, khách đã 予約確定/chờ duyệt không nhận\n"
       "- B5: khách đang chờ KHÔNG nhận được thông báo nữa; các booking chờ vẫn giữ nguyên trạng thái",
       note="Nguồn: Setting calendar r1433-r1437. ⚠ Spec KHÔNG mô tả rule『gửi cho tất cả, ai đặt trước "
            "thì được』→ MT-30."),

    tc("空き枠通知受け取り設定", "DATA-AUDIT-001", "Normal",
       "Màn lịch sử thay đổi cài đặt danh sách chờ (変更履歴)",
       SET + "\n- Đã đổi trạng thái ON/OFF vài lần bởi cả admin và staff",
       "1. Mở màn「変更履歴」\n2. Đối chiếu cột ngày giờ, người thao tác, nội dung\n"
       "3. Kiểm tra thứ tự sắp xếp\n4. Bấm X",
       "≥ 3 lần đổi trạng thái",
       "- Ngày giờ format「2024.09.25 (金) 10:31」\n- Cột người thao tác hiện tên staff/admin\n"
       "- Nội dung: bật →「停止中→受付中 に変更」; tắt →「受付中→停止中 に変更」\n"
       "- Sort thời gian mới nhất lên đầu\n- X: đóng popup",
       note="Nguồn: Setting calendar r1452-r1458."),

    # ══════════════ 35. トップ・店舗情報・利用規約 ══════════════
    tc("トップ・店舗情報・利用規約", "MEDIA-IMG-001", "Abnormal",
       "Upload ảnh ở tab トップ設定 và 店舗・ビジネス情報 — giới hạn và định dạng",
       SET + "\n- Mở tab「トップ設定」",
       "1. Upload ảnh không phải 1000x500 → lưu\n2. Upload ảnh đúng 1000x500 → lưu\n"
       "3. Upload ảnh > 10MB\n4. Upload file có tên tiếng Nhật / có khoảng trắng\n"
       "5. Upload file không phải ảnh và ảnh .avif\n6. Upload jpg / png / gif / jpeg\n"
       "7. Upload 1 ảnh rồi thay bằng ảnh khác\n8. Lặp lại toàn bộ ở tab「店舗・ビジネス情報」",
       "Các file như mô tả",
       "- Ảnh mọi tỉ lệ, tên JP, có khoảng trắng, 4 định dạng hợp lệ: upload thành công\n"
       "- Ảnh > 10MB: lỗi「10MB以下のをアップしてください。」\n"
       "- File sai định dạng ở トップ設定: lỗi「png, jpg, gif画像を選択してください。」\n"
       "- File sai định dạng ở 店舗・ビジネス情報: lỗi「ファイルの形式が正しくありません。」\n"
       "- Thay ảnh: ảnh mới hiển thị đúng",
       env="PRODUCTION",
       note="Nguồn: Setting calendar r1470-r1476, r1515-r1520. ⚠ 2 màn dùng 2 message lỗi KHÁC NHAU "
            "cho cùng 1 tình huống → MT-31. RULE-08: media test production."),

    tc("トップ・店舗情報・利用規約", "FUNC-004", "Boundary",
       "Validate tên cửa hàng 店舗名 và đồng bộ với calendar_name",
       SET + "\n- Mở tab「トップ設定」",
       "1. Lần đầu vào màn → quan sát giá trị mặc định của 店舗名\n"
       "2. Nhập 30 ký tự hợp lệ → lưu → kiểm tra `calendar_name` và `store_name`\n"
       "3. Xóa trắng → lưu\n4. Nhập 31 ký tự → lưu",
       "Chuỗi 30 và 31 ký tự",
       "- Mặc định lấy `calendar_name` đã tạo ở màn tạo calendar\n"
       "- Lưu 30 ký tự: cập nhật CẢ `calendar_name` và `store_name`\n"
       "- Xóa trắng: lỗi「店舗名を入力してください。」\n"
       "- 31 ký tự: lỗi「店舗名は30文字以内で入力してください。」",
       note="Nguồn: Setting calendar r1477, r1480-r1485. ⚠ r1477 ghi「Check setting tên cửa hàng "
            "=> Change spec: 100 ký tự」nhưng r1484 lại báo lỗi ở 31 ký tự → MT-32."),

    tc("トップ・店舗情報・利用規約", "LIFF-ENTRY-001", "Normal",
       "Ẩn/hiện trang TOP quyết định màn đầu tiên phía LINE user",
       SET + "\n- Mở tab「トップ設定」",
       "1. Chọn HIỆN top page → LINE user mở link booking / link lịch sử / link hủy\n"
       "2. Chọn ẨN top page → quan sát các mục cài đặt ở màn admin\n"
       "3. Với các tổ hợp (có/không dùng course × có/không dùng staff) → LINE user mở link booking\n"
       "4. LINE user mở link lịch sử và link hủy\n5. Đổi qua lại ẩn/hiện nhiều lần → kiểm tra",
       "4 tổ hợp course/staff",
       "- HIỆN: link booking luôn ra màn top page; link lịch sử ra màn lịch sử; link hủy ra detail booking\n"
       "- ẨN: các mục ảnh / tên calendar / mô tả không hiển thị ở màn cài đặt\n"
       "- ẨN + có course: vào thẳng màn chọn course\n- ẨN + bỏ course, có staff: vào màn chọn staff\n"
       "- ẨN + bỏ cả 2: vào thẳng màn chọn slot\n"
       "- Link lịch sử và link hủy: không đổi\n- Đổi qua lại nhiều lần: luôn hiển thị đúng setting hiện tại",
       note="Nguồn: Setting calendar r1499-r1510."),

    tc("トップ・店舗情報・利用規約", "OUT-PREVIEW-001", "Normal",
       "Nút preview và nút save của tab トップ設定",
       SET + "\n- Đã điền thông tin ở tab トップ設定",
       "1. Bấm nút preview\n2. Sửa thông tin rồi bấm preview lại\n3. Bấm save\n"
       "4. Sửa thông tin nhưng chuyển tab khác không lưu",
       "Thông tin top page",
       "- Preview: lưu thông tin và mở tab mới hiển thị đúng như phía LINE user\n"
       "- Preview sau khi sửa: lưu thông tin mới rồi mở preview với dữ liệu mới\n"
       "- Save: lưu thông tin\n- Chuyển tab không lưu: KHÔNG lưu các thay đổi",
       note="Nguồn: Setting calendar r1491-r1498, r1409-r1410."),

    tc("トップ・店舗情報・利用規約", "FUNC-001", "Normal",
       "Cài đặt 利用規約 — bật/tắt và nội dung HTML",
       SET + "\n- Mở tab「利用規約の設定」",
       "1. Chọn OFF quy chế → LINE user vào màn đặt lịch\n"
       "2. Chọn ON nhưng bỏ trống nội dung → lưu\n"
       "3. Nhập 5000 ký tự text thường → lưu → xem phía LINE user\n"
       "4. Nhập nội dung định dạng HTML → lưu → xem phía LINE user",
       "Nội dung text và HTML",
       "- OFF: LINE user KHÔNG thấy quy chế\n- ON + bỏ trống: báo lỗi\n"
       "- 5000 ký tự text: lưu và hiển thị đúng phía LINE user\n"
       "- HTML: hiển thị đúng định dạng HTML phía LINE user",
       note="Nguồn: Setting calendar r1461-r1466."),

    # ══════════════ 36. システムワード & 予約ページ表示設定 ══════════════
    tc("システムワード & 予約ページ表示設定", "DATA-001", "Normal",
       "Đổi từ hệ thống (システムワード変更) áp dụng ở mọi màn phía LINE user",
       SET + "\n- Mở mục「システムワード変更」",
       "1. Quan sát ô text hiện tại (vd「コース」)\n2. Bỏ trống ô thay thế → lưu\n"
       "3. Nhập 11 ký tự → quan sát\n4. Nhập text thay thế hợp lệ cho コース → lưu → xem phía LINE user\n"
       "5. Đổi text thay thế cho スタッフ → lưu → xem tất cả màn phía LINE user\n"
       "6. Không bấm save mà chuyển tab / bấm save nhiều lần",
       "Text thay thế ≤ 10 ký tự",
       "- Ô text hiện tại bị disable\n- Bỏ trống: KHÔNG bắt buộc (không required)\n"
       "- 11 ký tự: báo lỗi hoặc không nhập được ký tự thứ 11\n"
       "- LINE user: mọi chỗ có chữ コース / スタッフ đều đổi thành text đã cài — kiểm tra ở "
       "màn chọn staff · detail staff · chọn slot · nhập thông tin · xác nhận · hoàn tất · lịch sử\n"
       "- Không save: không lưu; save nhiều lần: chỉ tính 1 lần",
       note="Nguồn: Setting calendar r1404-r1410, r1316-r1317 + Booking phía line user r91, r130."),

    tc("システムワード & 予約ページ表示設定", "DATA-001", "Normal",
       "予約ページの表示設定 — 3 tuỳ chọn hiển thị và trường hợp bị ghi đè",
       SET + "\n- Mở tab「予約ページの表示設定」",
       "1. Hiển thị giá course: chọn 表示する / 表示しない → xem phía LINE user\n"
       "2. Bật 決済連携 → xem lại giá course phía LINE user\n"
       "3. Hiển thị số chỗ còn lại: chọn 表示する / 表示しない → xem phía LINE user\n"
       "4. Slot đã hết chỗ: chọn 表示する / 表示しない → xem phía LINE user\n"
       "5. Bật chức năng danh sách chờ → xem lại slot đã hết chỗ",
       "3 tuỳ chọn",
       "- Giá course: 表示する → hiện giá; 表示しない → không hiện\n"
       "- Bật 決済: LUÔN hiện giá, KHÔNG theo cài đặt này nữa\n"
       "- Số chỗ còn lại: hiện「残り XXX」hoặc không hiện\n"
       "- Slot hết chỗ 表示する: vẫn hiện kèm「残り 0」và bị disable; 表示しない: ẩn hẳn slot\n"
       "- Bật danh sách chờ: slot đã đầy VẪN hiện và đặt được (đăng ký chờ), không theo cài đặt này",
       note="Nguồn: Setting calendar r1396-r1403."),

    tc("システムワード & 予約ページ表示設定", "UI-001", "Normal",
       "Cài đặt hiển thị theo tuần hay theo tháng ở màn chọn slot",
       SET,
       "1. Chọn hiển thị theo TUẦN → LINE user đặt mới → quan sát tab focus\n"
       "2. LINE user copy booking cũ → quan sát tab focus\n"
       "3. Chọn hiển thị theo THÁNG → lặp lại 2 bước trên",
       "2 cài đặt hiển thị",
       "- Cài theo tuần: cả đặt mới và copy đều focus vào tab hiển thị theo tuần\n"
       "- Cài theo tháng: cả 2 đều focus vào tab hiển thị theo tháng",
       note="Nguồn: Booking phía line user r1312-r1315. ⚠ Bug #29364 (27/03/2025): lần đầu click "
            "không hiện được màn tháng → cần verify sau fix."),

    # ══════════════ 37. 予約ページの非表示 (filter) ══════════════
    tc("予約ページの非表示 (filter)", "LIFF-ENTRY-001", "Normal",
       "Không set filter → LINE user luôn vào được trang đặt lịch",
       SET + "\n- Chưa set điều kiện 予約ページの非表示",
       "1. Với 4 tổ hợp (có/không top page × có/không dùng course/staff): LINE user mở link booking\n"
       "2. LINE user mở link lịch sử",
       "4 tổ hợp cài đặt",
       "- Có top page: hiện trang top, bấm nút đặt lịch ra màn tương ứng theo cấu hình\n"
       "- Không top page: vào thẳng màn chọn course / chọn staff / chọn slot theo cấu hình\n"
       "- Link lịch sử: hiện màn lịch sử",
       note="Nguồn: Setting calendar r261-r266, r289-r292."),

    tc("予約ページの非表示 (filter)", "PERM-001", "Abnormal",
       "Khách THỎA MÃN filter → bị chặn trang đặt lịch với message tuỳ chỉnh",
       SET + "\n- Đã set filter「予約ページの非表示」(vd: khách có tag T1)\n"
             "- Khách F1 có tag T1, khách F2 không có",
       "1. F1 mở link booking (cả khi có và không có top page, cả 4 tổ hợp course/staff)\n"
       "2. F2 mở link booking\n3. F1 mở link lịch sử\n4. F2 mở link lịch sử\n"
       "5. Với calendar loại 個人 → lặp lại",
       "F1 thỏa filter, F2 không thỏa",
       "- F1 (booking): hiện trang báo lỗi kèm message đã cài ở mục「予約ページの案内テキスト」\n"
       "- F2: vào được trang đặt lịch bình thường\n"
       "- F2 (lịch sử): hiện trang lịch sử\n- Calendar 個人 cho kết quả tương tự",
       note="Nguồn: Setting calendar r267-r282, r293-r308 + Booking phía line user r1321-r1325."),

    tc("予約ページの非表示 (filter)", "PERM-001", "Normal",
       "Update spec 06/11/2025: khách thỏa filter VẪN vào được màn hủy booking",
       SET + "\n- Đã set filter; khách F1 thỏa filter và đã có booking từ trước",
       "1. F1 mở link lịch sử booking\n2. F1 mở link HỦY booking (URL gửi trong action)\n"
       "3. F1 thực hiện hủy booking",
       "F1 thỏa filter, đã có booking",
       "- Theo update spec 06/11/2025: F1 VẪN hiển thị được màn hủy booking và hủy được\n"
       "- Không bị chặn như luồng đặt lịch mới",
       note="Nguồn: Setting calendar r275-r278 (update spec 06/11/2025) + SpecChange #32646 "
            "(Booking phía line user r1358-r1374). ⚠ MÂU THUẪN với r1324 cùng corpus "
            "(「user mở từ link lịch sử + thỏa filter → hiện trang báo lỗi」) → MT-33."),

    tc("予約ページの非表示 (filter)", "OUT-TRUTH-001", "Normal",
       "Nội dung trang báo lỗi khi bị filter chặn",
       SET + "\n- Đã set filter chặn khách F1",
       "1. Không nhập text hướng dẫn → F1 mở link booking\n"
       "2. Nhập text hướng dẫn (có ký tự xuống dòng) → lưu → F1 mở lại",
       "Text có xuống dòng",
       "- Không nhập: hiện text mặc định「詳細は運営元までお問い合わせください」\n"
       "- Có nhập: hiện đúng text đã nhập, giữ nguyên xuống dòng",
       note="Nguồn: Setting calendar r287-r288 + Booking phía line user r1326-r1327."),

    tc("予約ページの非表示 (filter)", "DATA-REF-001", "Abnormal",
       "Xóa filter đang được tham chiếu — cả trường hợp bình thường và dữ liệu lỗi",
       SET + "\n- Calendar đang tham chiếu filter FL-1",
       "1. Xóa filter FL-1 theo luồng bình thường (`filter_calendar_salon_ids` bị xóa khỏi calendar) → "
       "LINE user mở link booking và link lịch sử\n"
       "2. Trường hợp bất thường: `filter_calendar_salon_ids` VẪN còn trên calendar nhưng bản ghi filter "
       "đã bị xóa → LINE user mở 2 link",
       "Filter FL-1 bị xóa 2 cách",
       "- Cả 2 trường hợp: LINE user vào được trang đặt lịch và trang lịch sử bình thường\n"
       "- Không lỗi màn trắng / lỗi hệ thống",
       note="Nguồn: Setting calendar r283-r286, r305-r308."),

    # ══════════════ 38. 予約システムの削除 ══════════════
    tc("予約システムの削除", "NOTI-MAIL-001", "Normal",
       "Quy trình xóa calendar 2 bước xác thực bằng mã email",
       SET + "\n- Mở tab「予約システムの削除」",
       "1. Quan sát màn trước khi gửi mã\n2. Bấm「削除用認証コードをメールで受け取る」\n"
       "3. Kiểm tra hộp thư admin\n4. Bấm「メールを再送する」\n5. Nhập mã hợp lệ → xác nhận",
       "Email admin của bot",
       "- Màn đầu hiện tên calendar + nút gửi mã (không hiện tên quản lý)\n"
       "- Bấm gửi mã: chuyển sang màn nhập mã, admin nhận được email chứa mã\n"
       "- Bấm gửi lại: reload màn, gửi được email mới\n- Nhập mã đúng: hiện popup xác nhận cuối",
       note="Nguồn: Setting calendar r1663-r1673. Spec BR-07, EP-43/EP-44."),

    tc("予約システムの削除", "NOTI-MAIL-001", "Abnormal",
       "Validate mã xác thực xóa calendar",
       SET + "\n- Đã gửi mã lần 1, sau đó gửi lại mã lần 2",
       "1. Bỏ trống ô mã → bấm tiếp\n2. Nhập mã sai → bấm tiếp\n"
       "3. Nhập mã CŨ (lần 1) → bấm tiếp\n4. Nhập mã mới có khoảng trắng đầu/cuối → bấm tiếp",
       "Mã rỗng · mã sai · mã cũ · mã mới có khoảng trắng",
       "- B1, B2, B3: báo lỗi, không xóa được\n"
       "- B4: tự trim khoảng trắng, hiện popup xác nhận cuối",
       note="Nguồn: Setting calendar r1668-r1672."),

    tc("予約システムの削除", "DATA-REF-001", "Normal",
       "Xóa calendar → cascade xóa toàn bộ dữ liệu liên quan",
       SET + "\n- Calendar「サロンA」có: 2 course + 1 menu · 2 staff · ca làm việc · booking · remind · "
             "liên kết Google Calendar",
       "1. Thực hiện xóa calendar đến bước cuối → bấm「予約システムを削除する」\n"
       "2. Kiểm tra điều hướng\n"
       "3. Kiểm tra các bảng: `calendar_salon`, `calendar_salon_course`, `calendar_course_menu`, "
       "`calendar_salon_staff`, `calendar_salon_time_booking`, `calendar_salon_line_bookings`, "
       "`events` (type = 5 theo booking_calendar_id)\n"
       "4. Kiểm tra event trên Google Calendar của staff",
       "Calendar đầy đủ dữ liệu",
       "- Quay về màn list calendar, calendar đã biến mất\n"
       "- Toàn bộ các bảng liên quan không còn bản ghi của calendar này\n"
       "- Remind (`events` type 5) bị xóa\n- Event trên Google Calendar được xử lý theo BR-07",
       note="Nguồn: Setting calendar r1677, r1680-r1685. Spec BR-07."),

    tc("予約システムの削除", "LIFF-ENTRY-001", "Abnormal",
       "LINE user mở link của calendar đã bị xóa",
       "- Calendar「サロンA」đã bị xóa\n- Khách F1 vẫn còn link booking và link lịch sử cũ",
       "1. F1 mở link booking\n2. F1 mở link lịch sử",
       "2 link cũ",
       "- Cả 2 link: hiện lỗi「この予約ページはすでに削除されています。」",
       note="Nguồn: Setting calendar r1678-r1679 + Booking phía line user r5."),

    tc("予約システムの削除", "LIFF-ENTRY-001", "Normal",
       "Nút back / X trong popup xác nhận xóa cuối cùng",
       SET + "\n- Đang ở popup xác nhận xóa cuối cùng",
       "1. Bấm「戻る」\n2. Mở lại popup → bấm X",
       "-",
       "- Cả 2: đóng popup, quay về màn nhập mã, KHÔNG xóa calendar",
       note="Nguồn: Setting calendar r1675-r1676."),
]
