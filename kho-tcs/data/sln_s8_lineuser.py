# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 44-52: luồng LINE user (LIFF), đồng thời & verify API,
job nền & monitor, app mobile, phân quyền & môi trường, dữ liệu cũ & hồi quy.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Booking phía line user」(07/2024 → 07/2026, 1191 TC lá — Bug KH #38280 race condition,
    Bug tự detect #38629, Feature #31269 màn không có lịch, SpecImprove #32567 mất data form,
    Bug KH #33003/#33013, Bug #31160, SpecChange #32646 URL hủy)
  - tab「Main case」r270-r329 (logic hiển thị tuần/tháng khi không có lịch làm việc)
  - tab「Quản lý calendar」r3322-r3343 (monitor), r2350-r2351 (đổi bot)
  - tab「#38520」r43-r63 (race, phân quyền staff, LIFF entry, audit log, release, dữ liệu cũ)
  - tab「Check middle ware」·「#30919」
"""
from _common import tc

LU = ("- Bot A đã đăng ký LIFF ID cho tính năng đặt lịch\n"
      "- Calendar「サロンA」đang bật (enable_use_calendar = 1), có course C1 và staff S1/S2 có ca\n"
      "- LINE user U1 đã kết bạn với bot A và có bản ghi trên エルメ")

S8 = [
    # ══════════════ 44. LINE user — mở link & entry ══════════════
    tc("LINE user — mở link & entry", "MSG-USER-001", "Normal",
       "Ma trận trạng thái kết bạn × lối vào link đặt lịch",
       LU + "\n- Chuẩn bị thêm: U2 chưa kết bạn (chưa có bản ghi `line_user`), "
            "U3 đã kết bạn nhưng chưa có trên エルメ, U4 đã bị bot block, U5 đã unfollow",
       "1. U2 mở link trực tiếp và mở link dạng `https://line.me/R/app/{liff}?calendar_salon_id={id}`\n"
       "2. U3 mở 2 dạng link trên\n3. U1 mở 2 dạng link + mở từ button / image map / rich menu\n"
       "4. U4 mở 3 lối vào\n5. U5 mở 3 lối vào",
       "5 LINE user ở 5 trạng thái",
       "- U2: bị chuyển sang màn kết bạn ở CẢ 2 dạng link; sau khi kết bạn thì đặt lịch được "
       "(cả booking không bill và có bill)\n"
       "- U3 mở link trực tiếp: tự thêm user vào エルメ và vào được màn đặt lịch\n"
       "- U3 mở link dạng `line.me/R/app/...`: KHÔNG tự thêm bạn được → không mở được màn đặt lịch\n"
       "- U1: vào được màn đặt lịch ở cả 3 lối vào\n"
       "- U4 (bị block): KHÔNG hiển thị màn đặt lịch ở cả 3 lối vào\n"
       "- U5 (unfollow): chuyển sang màn kết bạn; kết bạn lại thì đặt được",
       note="Nguồn: Booking phía line user r11-r23 + #38520 r53. "
            "⚠ Nhánh U3 + link `line.me/R/app` là điểm KHÁC BIỆT dễ lọt — nêu rõ cho member."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Trang TOP hiển thị đúng nội dung đã cài ở トップ設定",
       LU + "\n- Đã cài ảnh, tên cửa hàng và mô tả ở tab トップ設定",
       "1. U1 mở link đặt lịch → quan sát trang top\n"
       "2. Từ menu chọn「基本情報」→ quan sát\n3. Từ menu chọn「特定商取引法に関する記載」→ quan sát",
       "Ảnh + tên cửa hàng + mô tả",
       "- Trang top hiện đúng ảnh / tên cửa hàng / mô tả đã cài ở トップ設定\n"
       "- 基本情報: hiện đúng nội dung đã cài ở ビジネス情報\n"
       "- 特定商取引法: hiện đúng nội dung đã cài ở tab 決済連携",
       note="Nguồn: Booking phía line user r7, r69, r148-r149."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Abnormal",
       "Chưa lấy được LINE ID → disable nút xác nhận (chống booking thiếu định danh)",
       LU,
       "1. Mở link bằng LINE app khi CHƯA lấy được line id → quan sát nút submit\n"
       "2. Reload lại link, vẫn chưa lấy được line id → quan sát\n"
       "3. Khi đã lấy được line id → quan sát nút và đặt lịch\n"
       "4. Lặp lại toàn bộ khi mở bằng trình duyệt ngoài LINE\n"
       "5. Double-click nút xác nhận khi đã lấy được line id",
       "Trạng thái chưa/đã có line id",
       "- Chưa có line id: nút bị disable (nền #F0F0F0, chữ #222222); reload vẫn disable\n"
       "- Đã có line id: nút enable, hiển thị được calendar và chọn slot bình thường, "
       "đặt lịch thành công và gửi được action\n"
       "- Double-click: KHÔNG tạo booking trùng\n"
       "- Kết quả giống nhau ở cả LINE app và trình duyệt ngoài",
       note="Nguồn: Booking phía line user r26-r64 (Info r30: disable button submit khi chưa lấy line id, "
            "09/2025)."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Preview khi admin gửi link đặt lịch (OGP)",
       LU,
       "1. Admin gửi link đặt lịch vào chat 1:1 → quan sát preview trên LINE\n"
       "2. Trường hợp đã nhập title và description → quan sát\n"
       "3. Trường hợp chưa nhập → quan sát",
       "Calendar có/không có title + description",
       "- Có title/description: preview hiện đúng title và description đã nhập\n"
       "- Không có: preview hiện tên cửa hàng và system name",
       note="Nguồn: Booking phía line user r6. ⚠ Corpus ghi「Calendar cũ:…」— cần verify hành vi hiện tại "
            "cho calendar mới."),

    # ══════════════ 45. LINE user — chọn コース/スタッフ ══════════════
    tc("LINE user — chọn コース/スタッフ", "LIFF-ENTRY-001", "Abnormal",
       "Không có course nào bật → không đi tiếp được",
       LU + "\n- Admin OFF toàn bộ course",
       "1. U1 mở link đặt lịch → đến bước chọn course\n2. Thử bấm đi tiếp",
       "0 course đang bật",
       "- KHÔNG next sang bước tiếp theo được",
       note="Nguồn: Booking phía line user r170."),

    tc("LINE user — chọn コース/スタッフ", "LIST-001", "Normal",
       "Danh sách course phía LINE user — thứ tự, nội dung, ẩn course OFF",
       LU + "\n- Có 3 course (1 course đang OFF, 1 course không có ảnh)",
       "1. U1 đến màn chọn course → đối chiếu thứ tự với màn quản lý\n"
       "2. Đối chiếu nội dung: ảnh, thời gian hoàn thành, giá tiền\n3. Bấm「詳細を見る」của 1 course",
       "3 course như mô tả",
       "- Course OFF: KHÔNG hiển thị\n- Thứ tự khớp `course_order` ở màn quản lý\n"
       "- Course không có ảnh: hiện ảnh mặc định\n"
       "- Thời gian và giá hiển thị theo cài đặt ở 表示設定\n"
       "- Bấm 詳細を見る: mở modal chi tiết course với đủ dữ liệu",
       note="Nguồn: Booking phía line user r171-r174."),

    tc("LINE user — chọn コース/スタッフ", "LIST-001", "Normal",
       "Danh sách course theo MENU nhóm",
       LU + "\n- Đã bật chế độ メニューあり với 3 menu, mỗi menu vài course",
       "1. U1 đến màn chọn course → quan sát danh sách menu (thứ tự, scroll, ảnh, tên)\n"
       "2. Quan sát trạng thái menu chưa mở và đã mở\n"
       "3. Mở 1 menu → đối chiếu thứ tự course trong menu\n4. Bấm 詳細を見る của 1 course",
       "3 menu, có menu không có ảnh",
       "- Danh sách menu hiển thị đủ, scroll được, đúng thứ tự admin cài\n"
       "- Menu chưa mở: chữ đen + mũi tên xuống; đã mở: chữ xanh + mũi tên lên\n"
       "- Menu không có ảnh: hiện ảnh mặc định\n"
       "- Course trong menu sắp theo `course_menu_id` rồi `order`",
       note="Nguồn: Booking phía line user r176-r182."),

    tc("LINE user — chọn コース/スタッフ", "LIST-001", "Normal",
       "Danh sách staff phía LINE user và modal chi tiết staff",
       LU + "\n- Có S1, S2 (ON) và S3 (OFF); đã bật dùng 指定なし",
       "1. U1 chọn course → đến màn chọn staff → đối chiếu danh sách\n"
       "2. Quan sát nội dung mỗi staff: tên hiển thị, ảnh, phí\n"
       "3. Bấm tên staff → quan sát modal chi tiết\n4. Trong modal bấm「このスタッフを選択する」\n"
       "5. Bấm icon X trong modal\n6. Bấm「このスタッフを予約する」ở ngoài danh sách\n7. Bấm「戻る」",
       "3 staff, 1 OFF",
       "- S3 (OFF) KHÔNG hiển thị\n- Nút「指定しない」hiện ở TRÊN CÙNG danh sách\n"
       "- Mỗi staff: tên hiển thị phía booking, ảnh (không có thì ảnh mặc định), "
       "phí theo cài đặt 表示設定\n"
       "- Modal chi tiết hiện đủ 3 trường trên\n"
       "- Chọn staff (từ modal hoặc từ danh sách): sang màn chọn slot\n"
       "- X: đóng modal; 戻る: về màn chọn course",
       note="Nguồn: Booking phía line user r190-r206."),

    # ══════════════ 46. LINE user — chọn slot ══════════════
    tc("LINE user — chọn slot", "LIFF-ENTRY-001", "Normal",
       "Khung giờ hiển thị theo đơn vị nhận booking (13 mức)",
       LU + "\n- Staff S1 có ca 08:30-15:30",
       "1. Đặt đơn vị nhận booking = 10分 → U1 xem màn chọn slot\n"
       "2. Lần lượt đổi sang 15分 · 30分 · 1時間 · 2時間 · 3時間 · 6時間 · 1日 → xem lại",
       "Ca 08:30-15:30, các đơn vị nhận booking",
       "- 10分: 08:30, 08:40, 08:50 … 15:10, 15:20\n- 15分: 08:30, 08:45, 09:00 … 15:00, 15:15\n"
       "- 30分: 08:30, 09:00, 09:30 … 14:30, 15:00\n- 1時間: 08:30, 09:30 … 13:30, 14:30\n"
       "- 2時間: 08:30, 10:30, 12:30, 14:30\n- 3時間: 08:30, 11:30, 14:30\n"
       "- 6時間: 08:30, 14:30\n- 1日: 08:30",
       note="Nguồn: Booking phía line user r213-r220 (có phép tính tay — RULE-05)."),

    tc("LINE user — chọn slot", "LIFF-ENTRY-001", "Abnormal",
       "Không hiển thị slot của ngày quá khứ",
       LU,
       "1. U1 đến màn chọn slot → chuyển về tuần quá khứ → quan sát",
       "Tuần quá khứ",
       "- KHÔNG hiển thị slot của những ngày quá khứ",
       note="Nguồn: Booking phía line user r221."),

    tc("LINE user — chọn slot", "LIST-001", "Boundary",
       "Logic chọn tuần hiển thị khi các tuần đầu KHÔNG có lịch làm việc",
       LU,
       "1. Trong 4 tuần đầu có ít nhất 1 tuần có ca → U1 mở màn chọn slot\n"
       "2. Tuần 1-4 không có ca, tuần 5 có ca CHƯA đầy → mở màn\n"
       "3. Tuần 1-4 không ca, tuần 5 có ca ĐÃ đầy, còn ca ở tuần 6/7 → mở màn\n"
       "4. Tuần 1-4 không ca, tuần 5 có ca đã đầy, KHÔNG còn ca nào sau đó → mở màn\n"
       "5. Tuần 1-5 đều không ca, còn ca sau tuần 5 → mở màn\n"
       "6. Tuần 1-5 không ca, KHÔNG còn ca nào sau đó → mở màn",
       "6 cấu hình lịch làm việc",
       "- B1: hiện tuần có ca gần nhất\n- B2: hiện tuần 5, có ca\n"
       "- B3: hiện tuần 5, các slot hiện nhưng đều bị disable\n"
       "- B4, B6: hiện màn theo design「không có lịch để đặt」(Feature #31269)\n"
       "- B5: hiện tuần 5 kèm message「この週には予約可能な日程がありません」",
       note="Nguồn: Main case r270-r275 + Info r56 (Feature #31269, 4/2026)."),

    tc("LINE user — chọn slot", "LIST-001", "Boundary",
       "Logic chọn THÁNG hiển thị khi các tháng đầu không có lịch làm việc",
       LU + "\n- Cài đặt hiển thị theo tháng",
       "1. Trong 2 tháng đầu có ca → U1 mở màn chọn slot\n"
       "2. Tháng 1-2 không ca, tháng 3 có ca chưa đầy → mở màn\n"
       "3. Tháng 1-2 không ca, tháng 3 có ca đã đầy, còn ca ở tháng sau → mở màn\n"
       "4. Tháng 1-2 không ca, tháng 3 có ca đã đầy, không còn ca nào → mở màn\n"
       "5. Tháng 1-3 không ca, còn ca sau tháng 3 → mở màn\n"
       "6. Tháng 1-3 không ca, không còn ca nào → mở màn",
       "6 cấu hình lịch làm việc",
       "- B1: hiện tháng có ca gần nhất\n- B2: hiện tháng 3, enable các ngày có ca chưa đầy\n"
       "- B3, B5: hiện tháng 3, các ngày đều disable\n"
       "- B4, B6: hiện màn theo design「không có lịch để đặt」",
       note="Nguồn: Main case r279-r284."),

    tc("LINE user — chọn slot", "LIST-001", "Normal",
       "Điều hướng tuần/tháng và nút 今日 phía LINE user",
       LU,
       "1. Bấm next / back tuần nhiều lần → quan sát\n2. Bấm「今日」ở chế độ tuần\n"
       "3. Bấm next / back tháng nhiều lần → quan sát\n4. Bấm「今日」ở chế độ tháng\n"
       "5. Ở chế độ tháng, bấm vào 1 ngày CÓ ca\n6. Chuyển qua lại giữa tab tuần và tháng",
       "-",
       "- next/back: chuyển lần lượt từng tuần/tháng kể cả tuần/tháng không có ca\n"
       "- 今日: LUÔN hiển thị tuần / tháng HIỆN TẠI (theo spec đã update)\n"
       "- Bấm 1 ngày ở lưới tháng: mở sang lưới tuần chứa ngày đó\n"
       "- Đổi tab: hiển thị đúng tuần/tháng có ca gần nhất",
       note="Nguồn: Main case r276-r278, r285-r289. ⚠ r278 và r287 có 2 phiên bản kết quả "
            "(「hiện tuần/tháng gần nhất có lịch」cũ và「luôn hiển thị tuần/tháng hiện tại」mới) → "
            "lấy bản MỚI, xem MT-40."),

    tc("LINE user — chọn slot", "FUNC-DATE-001", "Boundary",
       "Setting 期間限定 (mùa vụ) ảnh hưởng tuần/tháng hiển thị",
       LU + "\n- Đã set mùa vụ (期間限定) cho calendar",
       "1. Ngày bắt đầu mùa vụ ở QUÁ KHỨ, tuần có ca vẫn trong mùa vụ → U1 mở màn\n"
       "2. Tuần có ca NẰM NGOÀI mùa vụ → mở màn\n"
       "3. Tuần 5 có ca nhưng ngoài mùa vụ → mở màn\n"
       "4. Ngày bắt đầu mùa vụ ở TƯƠNG LAI → lặp lại 3 trường hợp trên\n"
       "5. Lặp lại toàn bộ ở chế độ hiển thị theo tháng",
       "Mùa vụ ở quá khứ và tương lai",
       "- Tuần/tháng có ca còn trong mùa vụ: hiển thị bình thường\n"
       "- Tuần/tháng có ca nằm NGOÀI mùa vụ: hiển thị tuần/tháng CUỐI CÙNG của mùa vụ\n"
       "- Không còn ca hợp lệ trong mùa vụ: hiện màn theo design「không có lịch để đặt」\n"
       "- Mùa vụ bắt đầu ở tương lai: đếm tuần/tháng tính từ tuần/tháng chứa ngày bắt đầu mùa vụ",
       note="Nguồn: Main case r290-r329 + SpecImprove #32887 (Booking phía line user r904-r936)."),

    tc("LINE user — chọn slot", "OUT-TRUTH-001", "Abnormal",
       "Bug KH #33003: giờ bắt đầu tuần sau bị lấy nhầm theo tuần trước",
       LU + "\n- Chủ nhật và thứ 2 có giờ bắt đầu ca khác nhau\n"
            "- Tuần 1: ca sớm nhất từ 09:00; tuần 2: ca sớm nhất từ 09:30",
       "1. U1 mở màn chọn slot ở tuần 1 → đọc giờ bắt đầu hiển thị\n"
       "2. Bấm next sang tuần 2 → đọc giờ bắt đầu hiển thị",
       "2 tuần có giờ bắt đầu khác nhau",
       "- Tuần 1: hiển thị từ 09:00\n- Tuần 2: hiển thị từ 09:30 (KHÔNG lấy nhầm 09:00 của tuần 1)",
       note="Nguồn: Booking phía line user r223-r224 (Bug KH #33003, 04/12/2025)."),

    tc("LINE user — chọn slot", "OUT-TRUTH-001", "Boundary",
       "Giờ bắt đầu hiển thị lấy theo staff được chọn",
       LU + "\n- Tuần 1: S1 có ca 09:00-18:00, S2 có ca 07:30-17:00; tuần 2 không có ca",
       "1. U1 chọn 指定なし → đọc giờ bắt đầu tuần 1 và nội dung tuần 2\n"
       "2. Chọn S1 → đọc lại\n3. Chọn S2 → đọc lại\n"
       "4. Với trường hợp khung 07:30-09:30 đã đầy → chọn 指定なし và đọc lại",
       "S1 09:00 · S2 07:30",
       "- 指定なし: hiển thị từ 07:30 (giờ sớm nhất trong các staff)\n"
       "- S1: từ 09:00\n- S2: từ 07:30\n- Tuần 2: hiện message không có lịch làm việc\n"
       "- Khung sớm nhất đã đầy: VẪN hiển thị từ 07:30 (chỉ disable slot)",
       note="Nguồn: Booking phía line user r226-r230."),

    tc("LINE user — chọn slot", "OUT-TRUTH-001", "Abnormal",
       "Bug #31160: chọn course có 所要時間 lẻ → lịch hiển thị sai",
       LU + "\n- Course「せどり［20分］」có thời gian 20 phút; đơn vị nhận booking khác 20 phút",
       "1. U1 chọn course 20 phút → xem màn chọn slot\n"
       "2. Đối chiếu các slot với ca làm việc của staff\n3. Đặt lịch ở slot cuối cùng\n"
       "4. Lặp lại cho calendar loại 個人",
       "Course 20 phút",
       "- Slot hiển thị đúng theo ca làm việc, không thiếu / không thừa slot\n"
       "- Slot cuối cùng đặt được và giờ kết thúc không vượt giờ đóng ca\n"
       "- Calendar 個人 cho kết quả tương tự",
       note="Nguồn: Booking phía line user r565-r899 (Bug #31160, 31/07/2025)."),

    tc("LINE user — chọn slot", "OUT-TRUTH-001", "Abnormal",
       "Bug KH #33013: xem theo tuần thấy ngày đặt được nhưng thực tế không",
       LU + "\n- Course「60分無料相談」; ca làm việc và limit như trong repro của ticket",
       "1. U1 xem theo TUẦN → ghi lại các ngày/slot hiển thị đặt được\n"
       "2. Bấm vào từng slot đó để đặt → quan sát\n3. Đối chiếu với lưới admin\n"
       "4. Lặp lại ở chế độ THÁNG và cho calendar 個人",
       "Course 60 phút",
       "- Ngày/slot hiển thị đặt được thì PHẢI đặt được thật\n"
       "- Lưới tuần, lưới tháng và lưới admin nhất quán với nhau",
       note="Nguồn: Booking phía line user r937-r1152 (Bug KH #33013, 05/12/2025)."),

    tc("LINE user — chọn slot", "OUT-TRUTH-001", "Abnormal",
       "Bug: màn tháng không hiển thị khi có filter staff",
       LU + "\n- Có filter staff được áp dụng",
       "1. U1 chọn staff → chuyển sang chế độ hiển thị theo tháng → quan sát\n"
       "2. Trường hợp có filter + cài đặt KHÔNG hiện top page, U1 thỏa filter → mở link\n"
       "3. Lặp lại cho calendar 個人 (không có filter staff)",
       "Có filter staff",
       "- Màn tháng hiển thị được bình thường khi có filter staff\n"
       "- User thỏa filter: hiện đúng trang báo lỗi, KHÔNG lọt vào màn đặt lịch\n"
       "- Calendar 個人: không có phần filter staff",
       note="Nguồn: Booking phía line user r504-r564 (Bug tự detect 9/2025: 「Không hiển thị màn hình "
            "tháng khi có filter của staff」+「set filter + setting không hiện top page thì user thỏa "
            "filter vẫn bị hiện màn booking」)."),

    # ══════════════ 47. LINE user — nhập form & xác nhận ══════════════
    tc("LINE user — nhập form & xác nhận", "LIFF-ENTRY-001", "Normal",
       "Điền form câu hỏi và hoàn tất đặt lịch — lưu đủ 3 tầng",
       LU + "\n- Calendar có 3 câu hỏi (1 bắt buộc, 1 gắn friend info có sẵn, 1 tự tạo friend info)",
       "1. U1 chọn course + staff + slot → đến màn nhập thông tin\n2. Điền đủ 3 câu hỏi → xác nhận\n"
       "3. Kiểm tra `calendar_salon_line_booking.friend_info`\n"
       "4. Kiểm tra `friend_information_value` của U1\n5. Kiểm tra lưới admin\n"
       "6. Kiểm tra tin nhắn U1 nhận trên LINE",
       "3 câu hỏi",
       "- Booking tạo thành công\n- `friend_info` lưu đủ 3 câu trả lời\n"
       "- Friend info của U1 được cập nhật đúng theo cấu hình liên kết\n"
       "- Lưới admin hiện booking mới\n- U1 nhận tin nhắn hoàn tất đặt lịch",
       note="Nguồn: Booking phía line user r168-r222 + Quản lý calendar r1059-r1093. RULE-07."),

    tc("LINE user — nhập form & xác nhận", "MSG-004", "Normal",
       "Ma trận action khi LINE user đặt lịch được duyệt ngay",
       LU + "\n- approve_type = 1 (duyệt ngay)\n- Course và staff KHÔNG có action riêng",
       "1. Booking action: message rỗng/NULL + không multi action → U1 đặt lịch\n"
       "2. Message + chọn không sử dụng + không multi action → đặt\n"
       "3. Message + có sử dụng + không multi action → đặt\n"
       "4. Message rỗng + CÓ multi action → đặt\n"
       "5. Message + không sử dụng + có multi action → đặt\n"
       "6. Message + có sử dụng + có multi action → đặt\n"
       "7. Với mỗi trường hợp, kiểm tra LINE app của U1 và bảng `action_lineuser`",
       "6 cấu hình action",
       "- B1, B2: không gửi tin nhắn, KHÔNG tạo bản ghi `action_lineuser`\n"
       "- B3: gửi tin nhắn đặt lịch, không tạo `action_lineuser`\n"
       "- B4, B5: KHÔNG gửi tin nhắn, CÓ tạo `action_lineuser` và chạy multi action\n"
       "- B6: gửi tin nhắn + tạo `action_lineuser` + chạy multi action",
       note="Nguồn: Booking phía line user r1175-r1180. RULE-06 + RULE-07."),

    tc("LINE user — nhập form & xác nhận", "MSG-004", "Normal",
       "Course/staff có action riêng → ưu tiên action của course/staff khi duyệt ngay",
       LU + "\n- approve_type = 1; course C1 và staff S1 có action riêng",
       "1. U1 đặt lịch chọn C1 + S1 → kiểm tra tin nhắn nhận được\n"
       "2. Lặp lại với cấu hình course/staff CHỈ set message và chọn KHÔNG sử dụng",
       "Course + staff có action riêng",
       "- Mặc định: gửi action của course và staff\n"
       "- Trường hợp course + staff chỉ set message và chọn không sử dụng: gửi action CHUNG của booking",
       note="Nguồn: Booking phía line user r1172 + Quản lý calendar r1115-r1118."),

    tc("LINE user — nhập form & xác nhận", "MSG-004", "Normal",
       "Luồng REQUEST: action của course/staff KHÔNG áp dụng",
       LU + "\n- approve_type = 2 (chờ duyệt); course C1 và staff S1 đều có action riêng",
       "1. U1 đặt lịch chọn C1 + S1 → kiểm tra tin nhắn ngay sau khi đặt\n"
       "2. Admin từ chối booking → kiểm tra tin nhắn",
       "Course + staff có action riêng",
       "- Lúc đặt (request): chỉ gửi action CHUNG「予約リクエスト受付時」, KHÔNG dùng action course/staff\n"
       "- Lúc bị từ chối: chỉ gửi action CHUNG「予約リクエスト否認時」\n"
       "- Action của course/staff CHỈ áp dụng khi đặt được duyệt ngay hoặc khi admin duyệt request",
       note="Nguồn: Booking phía line user r1181-r1191."),

    tc("LINE user — nhập form & xác nhận", "MSG-004", "Normal",
       "Ma trận action ở 4 mốc của luồng HỦY",
       LU + "\n- Có booking của U1 đã 予約確定",
       "1. U1 hủy được duyệt ngay: thử 6 cấu hình action (message rỗng/không dùng/có dùng × "
       "có/không multi action) → kiểm tra tin nhắn + `action_lineuser`\n"
       "2. U1 gửi yêu cầu hủy: lặp 6 cấu hình\n"
       "3. Admin duyệt yêu cầu hủy: lặp 6 cấu hình\n4. Admin từ chối yêu cầu hủy: lặp 6 cấu hình",
       "4 mốc × 6 cấu hình",
       "- Quy tắc giống nhau ở cả 4 mốc: chỉ gửi tin nhắn khi message được cài và CHỌN SỬ DỤNG; "
       "multi action luôn chạy khi có cài, kèm tạo bản ghi `action_lineuser`\n"
       "- Action của course/staff KHÔNG áp dụng cho luồng hủy",
       note="Nguồn: Booking phía line user r1194-r1217."),

    tc("LINE user — nhập form & xác nhận", "LIFF-ENTRY-001", "Abnormal",
       "SpecImprove #32567: mất mạng / server chậm ở bước tải form → không mất dữ liệu",
       LU,
       "1. U1 chọn slot → ngắt mạng → bấm đi tiếp sang màn form\n"
       "2. Bật mạng lại → reload → quan sát màn form và đặt lịch\n"
       "3. Giả lập server chậm (request timeout) ở bước tải form → quan sát\n"
       "4. Mở link ngoài app LINE và lặp lại 3 bước trên\n"
       "5. Sau khi đặt lịch, kiểm tra thông tin form ở màn admin (booking request)",
       "Mạng ngắt / request timeout",
       "- Màn form load lại được, U1 đặt lịch thành công\n"
       "- Booking request ở màn admin HIỆN ĐỦ thông tin form đã nhập (không mất data)\n"
       "- Kết quả giống nhau khi mở trong LINE app và ngoài app",
       note="Nguồn: Booking phía line user r1375-r1391 (SpecImprove #32567, 25/10/2025)."),

    tc("LINE user — nhập form & xác nhận", "PERF-LARGE-001", "Abnormal",
       "Bug tự detect #38629: salon nhiều staff gây lỗi Undefined index: start_time",
       LU + "\n- Salon có 40 staff, tất cả có ca trong 1 tuần",
       "1. U1 chọn 指定なし → chọn slot → đặt lịch (không bật random)\n"
       "2. Bật random staff → đặt lại\n3. Đặt lịch KHÔNG thanh toán / có Stripe / có UnivaPay "
       "(cả webhook và không webhook)\n"
       "4. Admin đặt lịch trên web và app với 指定なし (bật và không bật random)\n"
       "5. Đặt nhiều booking liên tiếp\n6. Kiểm tra action, remind, friend info, lịch sử, Google sync",
       "40 staff, nhiều khung giờ",
       "- KHÔNG còn lỗi「order booking salon: Undefined index: start_time」\n"
       "- Booking thành công ở mọi nhánh; random staff hoạt động đúng\n"
       "- Action / remind / friend info / lịch sử / sync Google đều đúng",
       note="Nguồn: Booking phía line user r1414-r1436 (Bug tự detect #38629, 07/2026 — KHỐI MỚI NHẤT)."),

    # ══════════════ 48. LINE user — lịch sử & copy ══════════════
    tc("LINE user — lịch sử & copy", "LIST-001", "Normal",
       "Màn lịch sử dạng list: chia 2 phần hiện tại / quá khứ, sort đúng",
       LU + "\n- U1 có ≥ 10 booking cả tương lai và quá khứ; có booking của user khác cùng calendar",
       "1. U1 mở link lịch sử → quan sát 2 phần và thứ tự\n2. Scroll danh sách\n"
       "3. Kiểm tra không lẫn booking của user khác\n4. Bấm「詳細を見る」ở phần hiện tại và phần quá khứ",
       "≥ 10 booking của U1 + booking user khác",
       "- Mặc định hiển thị dạng list, chia「現在の予約」và「過去の予約」\n"
       "- Sort theo thời gian đặt lịch, mới nhất lên đầu; scroll được\n"
       "- CHỈ hiện booking của U1\n"
       "- Phần hiện tại: detail có nút hủy (trừ booking đang request)\n"
       "- Phần quá khứ: detail không có nút hủy, chỉ có nút copy",
       note="Nguồn: Booking phía line user r72-r76, r95-r97."),

    tc("LINE user — lịch sử & copy", "LIST-001", "Normal",
       "Màn lịch sử dạng THÁNG: điều hướng và dữ liệu",
       LU + "\n- U1 có booking ở nhiều tháng",
       "1. U1 mở màn lịch sử → chuyển sang tab dạng tháng → quan sát tháng mặc định\n"
       "2. Bấm next / back tháng, bấm liên tục → quan sát tốc độ và dữ liệu\n"
       "3. Quan sát 2 phần hiện tại / quá khứ và scroll\n4. Bấm 詳細を見る ở cả 2 phần",
       "Booking nhiều tháng",
       "- Mặc định tháng hiện tại, format「2024年10月」\n"
       "- next/back: hiển thị đúng dữ liệu của tháng đã chọn, chỉ của U1\n"
       "- Bấm liên tục: dữ liệu load kịp, không hiển thị nhầm tháng\n"
       "- 2 phần và nút detail hoạt động giống dạng list",
       note="Nguồn: Booking phía line user r111-r135."),

    tc("LINE user — lịch sử & copy", "DATA-REF-001", "Abnormal",
       "Booking có course bị OFF / bị XÓA / bị FILTER → hành vi khác nhau ở màn lịch sử",
       LU + "\n- U1 có 3 booking dùng course CA (sẽ OFF), CB (sẽ xóa), CC (sẽ thêm filter)",
       "1. OFF course CA → U1 mở màn lịch sử\n2. XÓA course CB → U1 mở lại\n"
       "3. Thêm filter cho course CC sao cho U1 KHÔNG thỏa → U1 mở lại",
       "3 course ở 3 trạng thái",
       "- Course OFF: booking KHÔNG còn hiển thị ở màn lịch sử\n"
       "- Course bị xóa: booking KHÔNG còn hiển thị\n"
       "- Course bị filter: booking VẪN hiển thị ở màn lịch sử",
       note="Nguồn: Booking phía line user r84-r86, r126-r127."),

    tc("LINE user — lịch sử & copy", "FUNC-001", "Normal",
       "Copy đặt lịch 同じ内容で予約 từ booking cũ",
       LU + "\n- U1 có booking quá khứ dùng course CC",
       "1. U1 mở detail booking quá khứ → bấm「同じ内容で予約」\n"
       "2. Chọn slot còn trống → hoàn tất\n"
       "3. Với course đã bị filter không hiển thị cho U1 → bấm copy\n"
       "4. Khi U1 đã đạt giới hạn số lần đặt của calendar → bấm copy và chọn slot trống\n"
       "5. Khi chọn slot đang ở trạng thái chờ thông báo → quan sát",
       "Booking quá khứ · course bị filter · U1 đạt giới hạn",
       "- B1, B2: copy sang màn chọn slot, đặt lịch thành công\n"
       "- B3: báo lỗi (course không còn hiển thị với U1)\n"
       "- B4: hiện message báo đã đạt giới hạn đặt lịch của calendar\n"
       "- B5: đặt thành công vào trạng thái chờ thông báo",
       note="Nguồn: Booking phía line user r98, r105-r106, r143-r144, r165."),

    tc("LINE user — lịch sử & copy", "UI-001", "Normal",
       "Hiển thị giá và tên course/staff ở màn lịch sử theo cài đặt",
       LU + "\n- U1 có booking; đã cài text thay thế cho コース và スタッフ",
       "1. Cài KHÔNG hiển thị giá + KHÔNG bật 決済 → U1 mở lịch sử\n"
       "2. Cài KHÔNG hiển thị giá + BẬT 決済 → mở lại\n3. Cài CÓ hiển thị giá → mở lại\n"
       "4. Quan sát nhãn コース / スタッフ\n5. Với calendar loại 個人 → quan sát vùng staff",
       "3 cấu hình hiển thị giá",
       "- B1: KHÔNG hiện giá course\n- B2: CÓ hiện giá course (決済 ghi đè cài đặt)\n"
       "- B3: có hiện giá\n- Nhãn hiển thị theo text thay thế đã cài\n"
       "- Calendar 個人: KHÔNG có phần staff",
       note="Nguồn: Booking phía line user r91-r94, r130-r133, r151-r154, r160-r163."),

    # ══════════════ 49. LINE user — hủy booking ══════════════
    tc("LINE user — hủy booking", "FUNC-001", "Normal",
       "Hủy booking đã duyệt — theo cài đặt duyệt hủy",
       LU + "\n- U1 có booking「予約確定」",
       "1. Admin cài LUÔN cho phép hủy → U1 mở detail → bấm hủy → xác nhận\n"
       "2. Kiểm tra status và tin nhắn\n"
       "3. Admin cài CẦN DUYỆT khi hủy → U1 hủy → kiểm tra status\n"
       "4. Admin từ chối yêu cầu hủy → kiểm tra status\n5. Admin duyệt yêu cầu hủy → kiểm tra status",
       "2 cấu hình duyệt hủy",
       "- Luôn cho hủy: status → 4, gửi action hủy được duyệt ngay\n"
       "- Cần duyệt: status → 5 (キャンセルリクエスト)\n"
       "- Admin từ chối: status quay về 1\n- Admin duyệt: status → 4",
       note="Nguồn: Booking phía line user r156, r1233-r1234."),

    tc("LINE user — hủy booking", "FUNC-001", "Abnormal",
       "Không hủy được booking chưa duyệt và không rút lại yêu cầu hủy",
       LU + "\n- U1 có booking đang 予約リクエスト và 1 booking đang キャンセルリクエスト",
       "1. U1 mở detail booking 予約リクエスト → tìm nút hủy\n"
       "2. U1 mở detail booking キャンセルリクエスト → tìm nút hủy yêu cầu",
       "2 booking",
       "- Booking 予約リクエスト: KHÔNG có nút hủy; nếu cố thao tác → "
       "message「予約リクエストの取り消しはできません」\n"
       "- Booking キャンセルリクエスト: KHÔNG có nút; message「キャンセルリクエストの取り消しはできません」",
       note="Nguồn: Booking phía line user r96, r1235-r1236."),

    tc("LINE user — hủy booking", "FUNC-DATE-001", "Boundary",
       "Hạn hủy 変更の締切 — kiểu chỉ định ngày và kiểu chỉ định giờ",
       LU + "\n- U1 có booking「予約確定」bắt đầu 15:00 ngày 21/07",
       "1. Cài không giới hạn: booking chưa đến giờ → U1 mở detail\n"
       "2. Cài hạn theo NGÀY: (ngày start - số ngày) > hôm nay → mở detail\n"
       "3. (ngày start - số ngày) < hôm nay → mở detail\n"
       "4. (ngày start - số ngày) = hôm nay và giờ cài > giờ hiện tại → mở detail\n"
       "5. Cùng ngày nhưng giờ cài ≤ giờ hiện tại → mở detail\n"
       "6. Cài hạn theo GIỜ: mốc (giờ start - duration) còn trong cùng ngày và qua ngày → thử hủy\n"
       "7. Booking đã qua giờ bắt đầu → mở detail",
       "7 mốc thời gian như mô tả",
       "- B1, B2, B4: có nút hủy, hủy được\n"
       "- B3, B5, B7: KHÔNG cho hủy (ẩn nút hoặc lỗi「キャンセルできません。」)\n"
       "- B6: trước mốc thì hủy được, sau mốc thì không — đúng cho cả trường hợp mốc qua ngày",
       note="Nguồn: Booking phía line user r1223-r1232 + Setting calendar r398-r409."),

    tc("LINE user — hủy booking", "LIFF-ENTRY-001", "Normal",
       "SpecChange #32646: URL hủy vẫn dùng được khi user bị filter chặn trang đặt lịch",
       LU + "\n- U1 đặt lịch thành công và nhận được action chứa URL hủy\n"
            "- Sau đó admin thêm filter khiến U1 KHÔNG được hiển thị trang đặt lịch",
       "1. U1 mở URL hủy trong tin nhắn\n2. Quan sát màn hiển thị\n3. Thực hiện hủy\n"
       "4. Lặp lại cho calendar loại 個人",
       "U1 thỏa filter chặn",
       "- U1 VẪN mở được màn detail booking từ URL hủy\n"
       "- Hủy được booking\n- Calendar 個人 cho kết quả tương tự",
       note="Nguồn: Booking phía line user r1358-r1374 (SpecChange #32646, 29/10/2025). "
            "⚠ Xem MT-33 về mâu thuẫn với hành vi link lịch sử."),

    # ══════════════ 50. Đồng thời & verify API ══════════════
    tc("Đồng thời & verify API", "CONC-001", "Abnormal",
       "Bug KH #38280: 2 user đặt cùng slot cuối cùng gần như đồng thời",
       LU + "\n- Slot ngày 11/07 chỉ còn ĐÚNG 1 chỗ trống",
       "1. Calendar KHÔNG bật 決済: U1 và U2 bấm xác nhận gần như cùng lúc\n"
       "2. 3 user bấm cùng lúc\n3. U1 bấm trước, U2 bấm sau vài giây\n"
       "4. Calendar BẬT 決済: lặp lại 3 bước trên\n"
       "5. Slot còn 2 chỗ: 2 user đặt cùng lúc\n6. Slot KHÔNG giới hạn: 2 user đặt cùng lúc\n"
       "7. Calendar cấu hình REQUEST: slot còn 1, 2 user đặt cùng lúc\n"
       "8. Lặp lại cho calendar 個人 (limit 1 và không limit)",
       "Slot còn 1/2/không giới hạn",
       "- Slot còn 1: CHỈ 1 booking được tạo, user còn lại nhận thông báo hết chỗ "
       "(KHÔNG báo thành công giả)\n"
       "- Slot còn 2 hoặc không giới hạn: cả 2 đều thành công\n"
       "- Cấu hình REQUEST: cả 2 đều đặt được ở trạng thái 予約リクエスト\n"
       "- Có/không 決済 và calendar 個人 đều cho kết quả nhất quán\n"
       "- DB không sinh booking vượt limit",
       note="Nguồn: Booking phía line user r1396-r1413 (Bug KH #38280, 29/06/2026) + #38520 r43."),

    tc("Đồng thời & verify API", "CONC-002", "Abnormal",
       "Verify lại dữ liệu ở bước xác nhận — admin đổi cấu hình giữa chừng",
       LU + "\n- U1 đã chọn slot và đang ở bước nhập form / nhập thẻ",
       "1. Admin đổi 受付上限 của staff = đúng số booking hiện tại (khi ĐANG bật danh sách chờ) → "
       "U1 bấm xác nhận\n"
       "2. Như trên nhưng TẮT danh sách chờ → U1 xác nhận\n"
       "3. Admin đổi 受付上限 của calendar = số booking hiện tại → U1 xác nhận\n"
       "4. Admin thêm filter course mà U1 không thỏa → U1 xác nhận\n"
       "5. Admin OFF course U1 đã chọn → xác nhận\n6. Admin XÓA course → xác nhận\n"
       "7. Admin bỏ course khỏi staff đã chọn → xác nhận\n8. Admin OFF staff → xác nhận\n"
       "9. Admin XÓA staff → xác nhận\n10. Admin đổi/xóa ca làm việc chứa slot đã chọn → xác nhận\n"
       "11. Admin đổi thời gian nhận/dừng nhận → xác nhận\n"
       "12. Admin đổi giới hạn số lần đặt của 1 người → xác nhận",
       "12 kịch bản admin đổi cấu hình",
       "- (1): thông báo đã hết chỗ, mời chọn chỗ khác\n- (2): báo lỗi yêu cầu đặt lại từ đầu\n"
       "- (3): lỗi「この予約の受付制限中ですので、予約できません。」\n"
       "- (4): báo lỗi đặt lại từ đầu (course không tồn tại)\n- (5), (6): lỗi「コースが存在していません。」\n"
       "- (7): lỗi「スタッフ対応不可能なコースです。」\n- (8), (9): lỗi「このスタッフが存在していません。」\n"
       "- (10): lỗi「このシフトが存在していません。」\n- (11): lỗi hết / chưa đến thời gian nhận booking\n"
       "- (12): lỗi đã đủ số lần đặt của user",
       note="Nguồn: Booking phía line user r1237-r1254."),

    tc("Đồng thời & verify API", "CONC-002", "Normal",
       "Admin xóa friend info / xóa booking trong lúc user đang thao tác",
       LU + "\n- U1 đã trả lời xong danh sách câu hỏi và đang ở bước xác nhận",
       "1. Admin xóa 1 item câu hỏi → U1 bấm xác nhận\n"
       "2. Admin xóa friend info đang gắn với câu hỏi (ở màn quản lý friend info) → U1 xác nhận\n"
       "3. U1 đang ở màn lịch sử định mở detail booking A, admin xóa booking A → U1 bấm mở\n"
       "4. U1 bấm copy booking A đó",
       "Item bị xóa giữa chừng",
       "- B1, B2: booking VẪN thành công\n"
       "- B3: U1 vẫn xem được detail booking\n"
       "- B4: copy vẫn đặt lịch thành công; vào lại màn lịch sử thì booking đã xóa không còn",
       note="Nguồn: Booking phía line user r1255-r1257."),

    tc("Đồng thời & verify API", "CONC-002", "Abnormal",
       "Bot block user trong lúc user đang mở link đặt lịch",
       LU,
       "1. Bot gửi link đặt lịch cho U1\n2. Bot block U1 (`bot_line_user.is_blocked` = 1)\n"
       "3. U1 mở link đặt lịch",
       "U1 bị block sau khi nhận link",
       "- Màn đặt lịch đóng lại và hiển thị màn chat",
       note="Nguồn: Booking phía line user r1258."),

    tc("Đồng thời & verify API", "SEC-ISO-001", "Abnormal",
       "Đổi bot khi đang mở màn quản lý calendar (kể cả 2 tab)",
       "- Admin quản lý cả bot A và bot B, mỗi bot có salon calendar riêng",
       "1. Đang ở màn quản lý calendar của bot A → chọn sang bot B\n"
       "2. Mở màn quản lý calendar bot A ở 2 tab → tab 1 đổi sang bot B → sang tab 2 thao tác",
       "2 bot",
       "- B1: hiển thị màn list calendar của bot B\n"
       "- B2: tab 2 tự reload dữ liệu và hiển thị list calendar của bot đã đổi, "
       "không thao tác nhầm sang bot cũ",
       note="Nguồn: Quản lý calendar r2350-r2351."),

    tc("Đồng thời & verify API", "CONC-003", "Abnormal",
       "Chuyển nhanh giữa day / week / month khi API chưa trả",
       "- Đăng nhập admin bot A\n- Có booking ở nhiều ngày trong tháng 07/2026\n"
       "- Mở tab「予約カレンダー」",
       "1. Bấm liên tiếp day → week → month → day trong lúc API chưa trả xong\n"
       "2. Quan sát dữ liệu cuối cùng hiển thị\n3. Đếm số booking so với lưới đúng",
       "Nhiều booking trong tháng",
       "- Màn luôn hiển thị dữ liệu của view / tháng được chọn CUỐI CÙNG\n"
       "- Không trùng booking, không mất booking",
       note="Nguồn: #38520 r50."),

    tc("Đồng thời & verify API", "DATA-COUNT-001", "Normal",
       "Đối chiếu số booking giữa 4 nguồn: month view · day view · CSV export · API",
       "- Đăng nhập admin bot A\n"
       "- Trong tháng 07/2026 có 5 booking, trong đó 1 booking「キャンセル」và 1 booking「否認」",
       "1. Đếm booking ở lưới tháng\n2. Đếm ở lưới ngày (cộng các ngày)\n"
       "3. Export CSV → đếm\n4. Gọi API danh sách booking → đếm\n5. So sánh 4 con số",
       "5 booking, có cancel và deny",
       "- 4 nguồn cho ra CÙNG một con số, khớp tuyệt đối\n"
       "- Booking「キャンセル」/「否認」được xử lý nhất quán ở cả 4 nguồn (cùng tính hoặc cùng loại bỏ)",
       note="Nguồn: #38520 r45."),

    # ══════════════ 51. Job nền & monitor ══════════════
    tc("Job nền & monitor", "JOB-001", "Normal",
       "Job monitor phát hiện booking chèn vào block time Google",
       "- Bot production có salon calendar đã liên kết Google Calendar\n"
       "- Job `MonitorCalendarBookingTask` đang bật",
       "1. Đặt 1 booking hợp lệ, sau đó sửa DB để giờ booking chèn vào block time Google\n"
       "2. Chờ ≤ 60 giây → kiểm tra kênh cảnh báo Chatwork\n"
       "3. Với booking KHÔNG trùng block time → chờ 60 giây → kiểm tra\n"
       "4. Với booking trùng vùng nghỉ trước/sau của block time → kiểm tra",
       "Booking chèn / không chèn block time",
       "- Booking chèn block time (kể cả chèn vào vùng nghỉ trước/sau): CÓ cảnh báo cho dev\n"
       "- Booking không trùng: KHÔNG cảnh báo\n"
       "- Job KHÔNG tự sửa dữ liệu",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar r3322-r3332. Spec §7.1.4. RULE-08: job BẮT BUỘC test production."),

    tc("Job nền & monitor", "JOB-001", "Boundary",
       "Job monitor chỉ đếm booking của FRIEND ở trạng thái thành công",
       "- Bot production; job monitor đang bật\n- Slot có limit = 5 và đã có 5 booking status 1, 2, 5",
       "1. ADMIN đặt thêm 1 booking thành công vượt limit → chờ 60 giây → kiểm tra cảnh báo\n"
       "2. FRIEND đặt thêm 1 booking thành công vượt limit (sửa DB nếu cần) → kiểm tra\n"
       "3. Insert booking với `admin_id` ≠ NULL và status = 2 → kiểm tra\n"
       "4. Insert booking `admin_id` = NULL, status = 3 → kiểm tra\n"
       "5. Insert `admin_id` = NULL, status = 0 → kiểm tra\n"
       "6. Insert `admin_id` = NULL, status = 1 → kiểm tra\n"
       "7. Slot có số booking < limit và = limit → kiểm tra",
       "Các tổ hợp admin_id × status",
       "- CHỈ cảnh báo khi `admin_id` = NULL VÀ status = 1 (friend đặt và thành công)\n"
       "- Admin đặt vượt limit: KHÔNG cảnh báo\n- status 0, 2, 3: KHÔNG cảnh báo\n"
       "- Số booking < limit hoặc = limit: KHÔNG cảnh báo",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar r3334-r3343. ⚠ Spec §7.1.4 chỉ mô tả monitor overlap block time, "
            "KHÔNG mô tả monitor vượt limit và bộ lọc admin_id/status → MT-41."),

    tc("Job nền & monitor", "JOB-001", "Normal",
       "Job đồng bộ webhook Google Calendar — luồng và khôi phục sau restart",
       "- Bot production, staff đã liên kết Google Calendar\n"
       "- Job `HandleSalonCalendarCallbackManager` đang bật",
       "1. Tạo / sửa / xóa event trên Google Calendar\n"
       "2. Kiểm tra bảng `salon_google_calendar_callback` (trạng thái 0 → 4 → 2)\n"
       "3. Kiểm tra block time trên LME sau khi job xử lý\n"
       "4. Restart service Spring Boot trong lúc còn bản ghi đang xử lý → kiểm tra sau restart\n"
       "5. Tạo event ở nhiều bot cùng lúc → kiểm tra không lẫn dữ liệu",
       "Event Google ở nhiều bot",
       "- Bản ghi callback chuyển đúng trạng thái đến DONE\n"
       "- Block time trên LME khớp với event trên Google\n"
       "- Sau restart: các bản ghi đang xử lý được đưa lại vào hàng đợi, không mất dữ liệu\n"
       "- Dữ liệu các bot không lẫn nhau (per-bot serialization)",
       env="PRODUCTION",
       note="Nguồn: Spec §7.1.1 + Sync google calendar r112-r145. RULE-08."),

    tc("Job nền & monitor", "JOB-001", "Boundary",
       "Job đồng bộ Google bỏ qua event quá cũ / quá xa / loại workingLocation",
       "- Bot production, staff đã liên kết Google Calendar",
       "1. Tạo event trên Google ở quá khứ > 30 ngày → chờ sync → kiểm tra block time\n"
       "2. Tạo event ở tương lai > 2 năm → kiểm tra\n"
       "3. Tạo event loại「勤務場所 (workingLocation)」→ kiểm tra\n"
       "4. Tạo event trong khoảng hợp lệ → kiểm tra\n"
       "5. Tạo event nhiều ngày (multi-day) → kiểm tra số bản ghi block time",
       "Event ở các mốc thời gian và loại khác nhau",
       "- Event quá khứ > 30 ngày, tương lai > 2 năm, loại workingLocation: BỎ QUA, không tạo block time\n"
       "- Event hợp lệ: tạo block time đúng\n"
       "- Event nhiều ngày: tách thành nhiều bản ghi, mỗi bản ghi 1 ngày (múi giờ Asia/Tokyo)",
       env="PRODUCTION",
       note="Nguồn: Spec §7.1.1 (đặc điểm kỹ thuật). ⚠ Corpus KHÔNG có TC cho các mốc lọc này → "
            "TC bổ sung theo spec, cần verify."),

    tc("Job nền & monitor", "JOB-001", "Normal",
       "Job export CSV lịch sử đồng bộ Google — encoding và nội dung",
       "- Bot production, calendar đã liên kết Google Calendar và có lịch sử sync 2 chiều",
       "1. Ở tab データ同期履歴 bấm tải CSV loại 1 (LME → Google) → chờ job\n"
       "2. Mở file bằng Excel tiếng Nhật\n3. Lặp lại với loại 2 (Google → LME)\n"
       "4. Kiểm tra bảng `calendar_salon_download_csv_sync_google_calendar`",
       "Lịch sử sync 2 chiều",
       "- File tải về mở được, tiếng Nhật hiển thị đúng (encoding SHIFT-JIS, không mojibake)\n"
       "- Loại 1 chứa lịch sử đẩy booking LME sang Google; loại 2 chứa lịch sử block time Google về LME\n"
       "- Bản ghi trong bảng queue chuyển đúng trạng thái",
       env="PRODUCTION",
       note="Nguồn: Spec §7.1.3 + Setting calendar r1888-r1921. RULE-08."),

    tc("Job nền & monitor", "JOB-001", "Abnormal",
       "Job gửi remind bỏ qua bot hết hạn plan và user bị block",
       "- Bot production đã bật remind\n- Có 1 bot đã hết hạn plan > 7 ngày",
       "1. Tạo booking ở bot hết hạn plan → chờ đến giờ remind → kiểm tra\n"
       "2. Booking của user bị block → chờ đến giờ remind → kiểm tra\n"
       "3. Booking bình thường → chờ đến giờ remind → kiểm tra",
       "Bot hết hạn · user bị block · trường hợp bình thường",
       "- Bot hết hạn > 7 ngày: bỏ qua, không gửi\n- User bị block: không gửi\n"
       "- Trường hợp bình thường: gửi đúng nội dung và đúng thời điểm",
       env="PRODUCTION",
       note="Nguồn: Spec §7.3 (bảng error handling NewEventRemindTask) + Setting calendar r1155-r1156."),

    # ══════════════ 52. App mobile ══════════════
    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile: lưới ngày và tháng không sinh booking ảo",
       "- Đã đăng nhập app mobile bằng tài khoản Admin bot A\n"
       "- Có booking「予約確定」11/07/2026 19:00-00:00 và booking 31/08/2026 19:00-00:00",
       "1. Mở app → lưới ngày 11/07 và 12/07 → quan sát\n"
       "2. Mở lưới tháng 07/2026 → quan sát ô ngày 11 và 12\n"
       "3. Mở lưới tháng 08 và 09/2026 → quan sát ô 31/08 và 01/09\n"
       "4. Xem danh sách booking ngày 12/07",
       "Booking kết thúc đúng 00:00",
       "- Ngày 11/07 hiển thị đúng 1 booking; ngày 12/07 KHÔNG có booking ảo\n"
       "- Tháng 07: ô ngày 11 có booking, ô ngày 12 không\n"
       "- Tháng 09: ô ngày 01 KHÔNG có booking của 31/08\n"
       "- Danh sách booking ngày 12/07 không chứa booking ảo",
       note="Nguồn: #38520 r26-r27."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "Đối chiếu song song Web và App cùng 1 kịch bản",
       "- Đăng nhập cả Web và app mobile bằng cùng tài khoản admin bot A\n"
       "- Có booking「予約確定」11/07/2026 19:00-00:00 và 1 booking cross-midnight thật 23:00-01:00",
       "1. Mở cùng ngày trên Web và App → so sánh từng ngày\n"
       "2. So sánh lưới tuần và lưới tháng\n3. So sánh danh sách booking",
       "2 booking khác kiểu",
       "- Web và App hiển thị GIỐNG NHAU ở mọi ngày\n"
       "- Không có booking ảo ở cả 2 nơi\n"
       "- Booking cross-midnight thật hiển thị đủ ở cả 2 ngày trên cả Web và App",
       note="Nguồn: #38520 r28."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile: thêm / sửa / xóa ca làm việc và đồng bộ sang Web",
       "- Đã đăng nhập app mobile bằng tài khoản Admin bot A",
       "1. Trên app: thêm ca 19:00-24:00 cho S1 → kiểm tra trên Web\n"
       "2. Trên app: sửa ca → kiểm tra trên Web\n3. Trên app: xóa ca → kiểm tra trên Web\n"
       "4. Trên Web: sửa/xóa ca vừa tạo trên app → kiểm tra không bị chặn nhầm\n"
       "5. Thử các case ghi đè / báo lỗi ca liên tiếp trên app",
       "Ca 19:00-24:00",
       "- Ca lưu thành công trên app, Web hiển thị đúng 19:00-24:00\n"
       "- Sửa / xóa ở Web KHÔNG bị chặn nhầm\n"
       "- Quy tắc ghi đè và báo lỗi ca liên tiếp GIỐNG Web",
       note="Nguồn: #38520 r29 + Quản lý calendar r2025-r2048 (Add lịch lv trên app), "
            "r2074-r2088 (Edit lịch lv trên app)."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile: admin đặt lịch + random staff + action + remind",
       "- Đã đăng nhập app mobile bằng tài khoản Admin bot A\n- Đã bật random staff",
       "1. Trên app đặt lịch chọn 指定なし (có bật random) → kiểm tra staff được gán\n"
       "2. Tắt random → đặt lại chọn 指定なし → kiểm tra\n3. Đặt lịch có chọn staff cụ thể → kiểm tra\n"
       "4. Đặt nhiều lần liên tiếp → kiểm tra\n"
       "5. Với mỗi trường hợp: kiểm tra action ở chat 1:1, remind, friend info, lịch sử",
       "Random bật/tắt",
       "- Bật random: gán được staff thỏa mãn\n- Tắt random: giữ 指定なし\n"
       "- Chọn staff cụ thể: giữ nguyên\n- Đặt liên tiếp: mọi booking đều thành công\n"
       "- Action / remind / friend info / lịch sử đều đúng ở cả 4 trường hợp",
       note="Nguồn: Booking phía line user r1432-r1435 + Quản lý calendar r2715-r2729."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "App mobile: lịch sử booking sort mới nhất lên đầu",
       "- Đã đăng nhập app mobile bằng tài khoản Admin bot A\n"
       "- Có booking đã trải qua nhiều thao tác (đặt, đổi staff, duyệt)",
       "1. Mở detail booking trên app → xem tab lịch sử\n2. Đối chiếu thứ tự với Web",
       "Booking có nhiều dòng lịch sử",
       "- Lịch sử sort thời gian MỚI NHẤT lên đầu, giống Web",
       note="Nguồn: Quản lý calendar r3318-r3321 (Review #29803)."),

    # ══════════════ 53. Phân quyền & môi trường ══════════════
    tc("Phân quyền & môi trường", "PERM-003", "Abnormal",
       "Staff KHÔNG có quyền màn 予約管理 → chặn ở cả UI, URL và API",
       "- Có tài khoản Staff của bot A CHƯA được cấp quyền màn 予約管理\n"
       "- Đăng nhập bằng tài khoản Staff đó",
       "1. Quan sát menu bên trái\n2. Gõ trực tiếp URL /basic/calendar-salon\n"
       "3. Gõ URL /basic/calendar-salon/{id}\n"
       "4. Gọi trực tiếp API danh sách calendar / danh sách booking bằng công cụ dev",
       "Staff chưa được cấp quyền",
       "- Menu 予約管理 KHÔNG hiển thị\n"
       "- Vào URL trực tiếp: bị chặn, chuyển về list bot + toast「この権限は許可されていません。」\n"
       "- Gọi API trực tiếp: CŨNG bị chặn (không chỉ ẩn UI)",
       note="Nguồn: #38520 r51. ⚠ Spec §9.2 mục 9 ghi「Phân quyền Staff chi tiết」là Gap → "
            "TC này lấp Gap, xem MT-35."),

    tc("Phân quyền & môi trường", "PERM-003", "Normal",
       "Staff CÓ quyền màn 予約管理 → thao tác như admin",
       "- Tài khoản Staff của bot A ĐÃ được cấp quyền màn 予約管理",
       "1. Đăng nhập bằng tài khoản Staff → mở màn 予約管理\n"
       "2. Tạo / sửa / xóa ca làm việc\n3. Đặt lịch thủ công, duyệt/từ chối request\n"
       "4. Kiểm tra tên người thao tác trong lịch sử booking\n"
       "5. Kiểm tra có bị giới hạn theo「người tạo」không",
       "Staff đã được cấp quyền",
       "- Staff thấy đủ nút và thao tác được TOÀN BỘ (tạo/sửa/xóa) như Admin trên màn đó\n"
       "- KHÔNG bị giới hạn theo người tạo\n"
       "- Lịch sử ghi đúng tên staff đã thao tác",
       note="Nguồn: #38520 r52 + Quản lý calendar r1312-r1315."),

    tc("Phân quyền & môi trường", "PERM-004", "Normal",
       "Rà soát phân quyền staff trên TẤT CẢ màn con của salon",
       "- Tài khoản Staff của bot A với các mức quyền khác nhau",
       "1. Với từng màn con: Calendar list · QL calendar theo ngày/tuần/tháng/list · "
       "danh sách booking · QL CSV · admin tạo booking · detail booking · booking đã xóa · "
       "màn setting (từng mục) · liên kết Google · 決済連携\n"
       "2. Kiểm tra hiển thị menu, truy cập URL trực tiếp và gọi API trực tiếp",
       "Danh sách màn con lấy từ tab「Staff」của file nguồn",
       "- Mỗi màn: hiển thị/ẩn đúng theo quyền\n"
       "- Truy cập URL và gọi API trực tiếp đều bị chặn khi không có quyền",
       spec="Đã hỏi leader",
       note="Nguồn: tab「Staff」(bảng liệt kê màn con để test acc staff) + các dòng「check acc staff」"
            "ở Quản lý calendar r166-r175, r1866, r3118, r3287 và Sync google r520-r521. "
            "⚠ Corpus ghi nhiều lần「trên dev acc staff thiếu quyền salon nên ko test được」→ "
            "nhóm case này CHƯA từng được test, xem MT-35."),

    tc("Phân quyền & môi trường", "UI-002", "Normal",
       "Kiểm tra trình duyệt và độ phân giải",
       "- Có ca kết thúc 24:00 và ca qua rạng sáng trên calendar\n"
       "- Chuẩn bị Windows Chrome, macOS Safari, màn 1366×768 và 1280",
       "1. Mở màn quản lý calendar trên Windows Chrome\n2. Mở trên macOS Safari\n"
       "3. Thu màn hình xuống 1366×768 rồi 1280 → mở các modal chính",
       "3 môi trường hiển thị",
       "- Hiển thị và hành vi NHẤT QUÁN giữa Chrome và Safari\n"
       "- Ở 1366×768 và 1280: không vỡ layout, modal không tràn, ca vẫn đọc được",
       note="Nguồn: #38520 r58 + Quản lý calendar r164-r165, r3125."),

    tc("Phân quyền & môi trường", "UI-003", "Normal",
       "3 trạng thái Loading / Rỗng / Lỗi của màn quản lý",
       "- Đăng nhập admin bot A",
       "1. Mở calendar chưa có booking nào → quan sát\n"
       "2. Mở màn khi mạng chậm → quan sát trong lúc chờ\n"
       "3. Giả lập API lỗi → quan sát",
       "3 trạng thái",
       "- Rỗng: hiển thị empty state rõ ràng (KHÔNG phải màn trắng)\n"
       "- Loading: có chỉ báo đang tải\n- Lỗi: báo lỗi rõ ràng, KHÔNG màn trắng",
       note="Nguồn: #38520 r57."),

    tc("Phân quyền & môi trường", "DATA-TEXT-001", "Normal",
       "Tên khách có emoji / ký tự đặc biệt hiển thị đúng ở mọi nơi",
       "- LINE user test có tên chứa emoji và ký tự đặc biệt\n- User này đã có booking",
       "1. Xem tên ở lưới quản lý (ngày/tuần/tháng/list)\n2. Xem ở detail booking\n"
       "3. Xem ở app mobile\n4. Export CSV và mở bằng Excel\n5. Xem trong Google Sheet",
       "Tên có emoji + ký tự đặc biệt",
       "- Tên hiển thị GIỐNG NHAU, không lỗi font, không mất ký tự ở cả 5 nơi\n"
       "- CSV mở bằng Excel không mojibake",
       note="Nguồn: #38520 r49."),

    tc("Phân quyền & môi trường", "DATA-AUDIT-001", "Normal",
       "Ghi log thao tác sửa / xóa ca làm việc",
       "- Đăng nhập admin bot A và tài khoản staff có quyền",
       "1. Admin sửa ca → kiểm tra log\n2. Staff xóa ca → kiểm tra log\n"
       "3. Đối chiếu: ai thao tác, khi nào, thay đổi gì (giá trị trước → sau)",
       "2 thao tác bởi 2 tài khoản",
       "- Log ghi đủ: ai (admin/staff id), khi nào, thay đổi gì (trước → sau)\n"
       "- Truy được người thao tác khi cần điều tra",
       spec="Đã hỏi leader",
       note="Nguồn: #38520 r63. ⚠ Spec KHÔNG có bảng audit log cho ca làm việc "
            "(chỉ có history cho booking và payment) → cần Leader xác nhận có log không, xem MT-42."),

    # ══════════════ 54. Dữ liệu cũ & hồi quy ══════════════
    tc("Dữ liệu cũ & hồi quy", "DATA-MIG-001", "Normal",
       "Dữ liệu ca + booking tạo TRƯỚC khi deploy fix vẫn chạy đúng sau deploy",
       "- Chuẩn bị TRƯỚC khi deploy branch fix: ca kết thúc 24:00 · ca qua rạng sáng · "
       "booking kết thúc đúng 00:00 · booking cross-midnight thật",
       "1. Deploy branch fix\n2. Mở lưới ngày / tuần / tháng → đối chiếu dữ liệu cũ\n"
       "3. Sửa và xóa ca cũ → quan sát\n4. Kiểm tra LIFF phía LINE user",
       "Dữ liệu tạo trước deploy",
       "- Dữ liệu cũ hiển thị ĐÚNG sau deploy, không mất ca / mất booking\n"
       "- Booking cũ kết thúc 00:00 KHÔNG còn sinh booking ảo\n"
       "- Ca cũ sửa/xóa được, không bị chặn nhầm",
       note="Nguồn: #38520 r60."),

    tc("Dữ liệu cũ & hồi quy", "REG-SHARED-001", "Normal",
       "Rà mọi nơi dùng chung logic lọc booking theo ngày sau fix",
       "- Đã deploy các branch fix liên quan booking cross-midnight",
       "1. Liệt kê mọi nơi hiển thị danh sách booking: lưới ngày/tuần/tháng · danh sách booking · "
       "danh sách booking đã xóa · app mobile · LIFF · CSV export · Google Sheet · remind\n"
       "2. Với mỗi nơi: kiểm tra booking ảo và booking cross-midnight thật",
       "Booking 19:00-00:00 và booking 23:00-01:00",
       "- MỌI nơi: không có booking ảo, booking cross-midnight thật hiển thị đủ\n"
       "- Nơi nào còn lỗi → ghi rõ ra để dev xử lý tiếp",
       note="Nguồn: #38520 r61."),

    tc("Dữ liệu cũ & hồi quy", "DEPLOY-LIVE-001", "Abnormal",
       "UI load TRƯỚC release, submit SAU release",
       "- Release KHÔNG bật chế độ bảo trì",
       "1. Mở màn thêm ca và điền đủ dữ liệu TRƯỚC khi release\n"
       "2. Thực hiện release\n3. Bấm lưu sau khi release xong\n"
       "4. Lặp lại với màn thêm booking và màn cài đặt",
       "Form đã điền trước release",
       "- HOẶC lưu thành công đúng dữ liệu, HOẶC báo lỗi rõ ràng yêu cầu reload\n"
       "- KHÔNG lưu sai dữ liệu, không lỗi JS trắng màn",
       env="PRODUCTION",
       note="Nguồn: #38520 r62. RULE-08: deploy/release test production."),

    tc("Dữ liệu cũ & hồi quy", "REG-SHARED-001", "Normal",
       "Ca giờ THƯỜNG (không chạm nửa đêm) vẫn hoạt động bình thường sau fix",
       "- Đăng nhập admin bot A; S1 chưa có ca ngày 11/07",
       "1. Tạo ca 10:00-18:00 → quan sát\n2. Sửa ca → quan sát\n3. Xóa ca → quan sát\n"
       "4. Tạo booking trong ca → kiểm tra lưới ngày 11/07 và 12/07",
       "Ca 10:00-18:00",
       "- Tạo / sửa / xóa ca đều thành công, không báo lỗi\n"
       "- Booking hiển thị đúng ở ngày 11/07, KHÔNG xuất hiện ở ngày 12/07\n"
       "- Fix cross-midnight không làm hỏng luồng ca thường",
       note="Nguồn: #38520 r64, r68."),

    tc("Dữ liệu cũ & hồi quy", "REG-SHARED-001", "Normal",
       "Số badge booking ở lưới tháng/ngày không đổi trước và sau fix",
       "- Có dữ liệu booking đa dạng trong tháng",
       "1. Ghi lại số badge của từng ô lưới tháng và lưới ngày TRƯỚC fix\n"
       "2. Deploy fix\n3. Ghi lại số badge SAU fix → so sánh",
       "Dữ liệu booking đa dạng",
       "- Số badge lưới tháng và lưới ngày GIỐNG NHAU trước và sau fix",
       note="Nguồn: #38520 r67."),

    tc("Dữ liệu cũ & hồi quy", "PERF-LARGE-001", "Normal",
       "SpecImprove #33408 / #34506: hiệu năng API calendar salon",
       "- Bot production có calendar nhiều staff (≥ 20) và nhiều booking (≥ 1000)",
       "1. Mở lưới ngày / tuần / tháng → đo thời gian phản hồi\n"
       "2. Mở màn chọn slot phía LINE user → đo thời gian\n"
       "3. Chuyển đổi giữa các chế độ hiển thị liên tục → quan sát\n"
       "4. Đối chiếu dữ liệu hiển thị với trước khi cải thiện hiệu năng",
       "≥ 20 staff, ≥ 1000 booking",
       "- Thời gian phản hồi trong ngưỡng chấp nhận được, không treo\n"
       "- Dữ liệu hiển thị KHÔNG đổi so với trước khi cải thiện hiệu năng",
       env="PRODUCTION",
       note="Nguồn: tab「SpecImprove #33408」(01/2026, 424 TC lá) + Test limit booking_V4_2 r216 "
            "(SpecImprove #34506, 23/02/2026). RULE-08: performance test production."),

    tc("Dữ liệu cũ & hồi quy", "REG-SPEC-001", "Normal",
       "Bug #29394: xóa ca làm việc KHÔNG được xóa booking",
       "- Đăng nhập admin bot A\n- Ca của S1 ngày 11/07 có booking ở trạng thái cho phép xóa ca",
       "1. Xóa ca đó → xác nhận\n2. Kiểm tra các booking liên quan ở lưới quản lý\n"
       "3. Kiểm tra màn「削除済み予約」\n4. Kiểm tra `calendar_salon_line_booking.deleted_at`",
       "Ca có booking",
       "- Theo Bug #29394 (03/2025 — đã BỎ logic cũ): xóa ca làm việc KHÔNG xóa booking liên quan\n"
       "- Booking vẫn giữ nguyên trên lưới, KHÔNG chuyển sang màn booking đã xóa",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar r3023-r3028 (Bug #29394, 30/03/2025). "
            "⚠ MÂU THUẪN TRỰC TIẾP với r711-r716 (khối cũ: xóa ca thì xóa cả booking) → MT-03, "
            "cần Leader chốt trước khi chạy TC này."),

    tc("Dữ liệu cũ & hồi quy", "REG-SPEC-001", "Normal",
       "Bug #29458 / SpecChange #29379: ghi đè ca làm việc trên web và app",
       "- Đăng nhập admin bot A và app mobile",
       "1. Trên web: sửa trực tiếp ca đã có (ghi đè) → quan sát có báo lỗi không\n"
       "2. Trên web: thêm mới ca 09:00-12:00 khi đã có ca 13:00-17:00 → quan sát ca cũ\n"
       "3. Trên app: lặp lại 2 bước trên\n4. Import CSV: lặp lại kịch bản thêm mới",
       "Ca cũ 13:00-17:00",
       "- Sửa trực tiếp ca có sẵn: KHÔNG báo lỗi (Bug #29458 đã fix)\n"
       "- Thêm mới / import CSV: áp dụng rule ghi đè theo SpecChange #29379 — "
       "ca cũ bị xử lý theo đúng rule đã chốt, không để lại ca rác\n"
       "- Web và app cho kết quả nhất quán",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar r3029-r3116 (Bug #29458 04/04/2025, SpecChange #29379 27/03/2025). "
            "⚠ SpecChange #29379 ghi「chỉ sửa case add mới / import csv」→ hành vi khác nhau giữa "
            "add mới và edit trực tiếp, cần Leader chốt rõ, xem MT-04."),

    tc("Job nền & monitor", "INTG-LINE-001", "Abnormal",
       "LINE API lỗi khi job gửi remind / action đặt lịch",
       "- Bot production đã bật remind và có action lúc đặt lịch\n"
       "- Chuẩn bị được tình huống LINE Messaging API trả lỗi (rate limit / 5xx)",
       "1. Cho LINE user đặt lịch trong lúc LINE API lỗi → quan sát booking\n"
       "2. Chờ đến giờ remind trong lúc LINE API lỗi → quan sát\n"
       "3. Sau khi LINE API hồi phục → kiểm tra tin nhắn user nhận được\n"
       "4. Kiểm tra màn danh sách lỗi gửi tin của tool",
       "LINE API lỗi tạm thời",
       "- Booking VẪN được tạo (lỗi gửi tin không được làm hỏng việc đặt lịch)\n"
       "- Lỗi gửi tin hiển thị ở màn danh sách lỗi, không im lặng bỏ qua\n"
       "- Sau khi API hồi phục: hành vi retry (nếu có) đúng như thiết kế, không gửi trùng",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Spec §7.1.2 (RequestSentQueue → LINE Messaging API) và §7.3 chỉ liệt kê lỗi bot expired / "
            "user bị block. ⚠ Corpus KHÔNG có TC cho lỗi LINE API → TC bổ sung, cần Leader xác nhận "
            "cơ chế retry. RULE-08."),

    tc("Dữ liệu cũ & hồi quy", "REG-RUN-001", "Abnormal",
       "Release trong lúc job remind / sync Google đang chạy dở",
       "- Bot production đang có bản ghi remind sắp đến giờ gửi và callback Google đang trong hàng đợi",
       "1. Thực hiện release / restart service khi job đang xử lý\n"
       "2. Sau release: kiểm tra `event_step_time` (bản ghi ở trạng thái đang gửi)\n"
       "3. Kiểm tra `salon_google_calendar_callback` (bản ghi đang xử lý)\n"
       "4. Kiểm tra LINE user có nhận remind không, có bị gửi trùng không\n"
       "5. Kiểm tra block time Google có bị mất/nhân đôi không",
       "Job đang chạy dở khi release",
       "- Bản ghi đang xử lý được đưa lại vào hàng đợi sau restart (theo cơ chế recovery)\n"
       "- KHÔNG mất remind, KHÔNG gửi trùng remind\n- Block time Google không mất và không nhân đôi",
       env="PRODUCTION",
       note="Spec §7.3「Recovery khi restart Spring Boot」. ⚠ Corpus KHÔNG có TC cho nhánh này → "
            "TC bổ sung theo spec. RULE-08."),

    tc("Dữ liệu cũ & hồi quy", "REG-URL-001", "Normal",
       "LIFF URL đặt lịch / lịch sử KHÔNG được đổi sau release",
       "- Đã ghi lại LIFF URL đặt lịch và URL lịch sử của calendar「サロンA」trước release\n"
       "- Các URL này đã được KH gắn vào rich menu, template và tin nhắn cũ",
       "1. Thực hiện release\n2. So sánh 2 URL trước và sau release\n"
       "3. Mở lại URL cũ đã gắn ở rich menu / template / tin nhắn cũ\n"
       "4. Kiểm tra URL hủy booking trong các tin nhắn action đã gửi trước release",
       "URL trước release",
       "- 2 URL GIỮ NGUYÊN sau release (chỉ tham số `ts` thay đổi)\n"
       "- URL cũ ở rich menu / template / tin nhắn cũ vẫn mở đúng màn\n"
       "- URL hủy trong tin nhắn cũ vẫn mở đúng detail booking",
       note="Spec §2.1 (LIFF URL format) + §2.6. ⚠ Corpus KHÔNG có TC hồi quy URL → TC bổ sung; "
            "quan trọng vì KH đã phát tán URL ra ngoài."),

    tc("Dữ liệu cũ & hồi quy", "DATA-BACKUP-001", "Normal",
       "Dữ liệu salon KHÔNG nằm trong phạm vi データコピー (backup sang bot khác)",
       "- Bot A có calendar salon đầy đủ (course, staff, ca, booking, cài đặt)\n"
       "- Bot B trống, đã chuẩn bị mã copy từ bot A",
       "1. Thực hiện データコピー từ bot A sang bot B\n"
       "2. Ở bot B mở menu 予約管理 > サロン・面談予約 → quan sát\n"
       "3. Đối chiếu với danh sách dữ liệu được copy ở màn xác nhận",
       "Bot A có salon, bot B trống",
       "- Bot B KHÔNG có calendar salon nào được copy sang\n"
       "- Màn xác nhận copy KHÔNG liệt kê サロン・面談予約 trong danh sách dữ liệu\n"
       "- Dữ liệu salon của bot A không bị ảnh hưởng",
       spec="Đã hỏi leader",
       note="⚠ `SECTIONS_BK` của FA-033 KHÔNG có mục copy salon (chỉ có イベント予約). TC này XÁC NHẬN "
            "salon nằm ngoài phạm vi copy — cần Leader xác nhận đây là ý đồ chứ không phải thiếu sót."),

    tc("Dữ liệu cũ & hồi quy", "MEDIA-CLEAN-001", "Normal",
       "Thay / xóa ảnh course, staff, top page → dọn file cũ trên server",
       "- Đăng nhập admin bot A\n- Course C1, staff S1 và trang top đều đã có ảnh",
       "1. Thay ảnh của C1 bằng ảnh mới → ghi lại đường dẫn ảnh cũ và mới\n"
       "2. Thay ảnh S1 và ảnh top page tương tự\n3. Xóa course C1 (sau khi hủy hết booking)\n"
       "4. Xóa calendar\n5. Với mỗi bước, kiểm tra file ảnh CŨ trên server còn tồn tại không",
       "3 ảnh ở 3 nơi",
       "- Ảnh mới hiển thị đúng ở màn admin và phía LINE user\n"
       "- File ảnh CŨ được dọn khỏi server (không để lại file rác)\n"
       "- Xóa course / xóa calendar cũng dọn ảnh liên quan",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="⚠ Corpus KHÔNG có TC dọn file; spec BR-07 liệt kê cascade delete nhưng KHÔNG nhắc file ảnh. "
            "Cần Leader xác nhận có cơ chế dọn file không. RULE-08: media test production."),

    tc("Dữ liệu cũ & hồi quy", "DEPLOY-ASSET-001", "Normal",
       "Version asset JS/CSS của màn salon sau release",
       "- Đã mở màn quản lý calendar trước release (asset cũ còn trong cache trình duyệt)",
       "1. Thực hiện release có thay đổi JS/CSS của màn salon\n"
       "2. KHÔNG xóa cache, tải lại màn quản lý calendar\n"
       "3. Thao tác thêm/sửa ca, thêm booking → quan sát\n"
       "4. Kiểm tra tham số version trên đường dẫn asset\n5. Lặp lại với màn LIFF phía LINE user",
       "Trình duyệt còn cache asset cũ",
       "- Asset được tải lại bản mới (tham số version đổi), không dính bản cũ\n"
       "- Các thao tác chạy đúng, KHÔNG lỗi JS/console\n- Màn LIFF phía LINE user cũng nhận asset mới",
       env="PRODUCTION",
       note="⚠ Corpus KHÔNG có TC version asset cho salon → TC bổ sung theo quan điểm DEPLOY-ASSET-001. "
            "RULE-08: deploy test production."),

    tc("LINE user — mở link & entry", "DATA-CACHE-001", "Abnormal",
       "Trang LIFF mở sẵn từ trước, admin đổi cài đặt rồi user mới thao tác",
       "- LINE user U1 đã mở trang đặt lịch và để yên (không đóng) 30 phút",
       "1. Trong lúc đó admin đổi: danh sách course · giờ làm việc · 受付上限 · text hiển thị\n"
       "2. U1 thao tác tiếp trên trang đang mở (chọn course, chọn slot, xác nhận)\n"
       "3. U1 kéo xuống refresh / mở lại link\n4. Đối chiếu dữ liệu U1 thấy với cài đặt hiện tại",
       "Trang LIFF mở sẵn 30 phút",
       "- Khi xác nhận, hệ thống kiểm tra lại dữ liệu MỚI NHẤT và báo lỗi rõ ràng nếu không còn hợp lệ "
       "(không đặt được bằng dữ liệu cũ)\n"
       "- Sau khi mở lại link: hiển thị đúng cài đặt hiện tại",
       note="Nguồn: Booking phía line user r1237-r1254 (cơ chế verify lại ở bước xác nhận) — "
            "TC này soi riêng góc dữ liệu cũ (stale) của trang mở lâu."),
]
