# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm thao tác trên đặt chỗ: filter, リクエスト一括操作, admin thêm booking,
detail booking & lịch sử, booking đã xóa, hoàn tiền.

Nguồn chính: 11.2 TCsLine_LessonCalendar → tab「Quản lý calendar_new」r343-r979 và
「Quản lý calendar」khối tương ứng (r330-r978) + r997-r1047 (Feature #26528 hiển thị bill tiền).
Spec: BR-20…BR-31 (trạng thái & sức chứa), BR-P27/BR-P28 (hoàn tiền), BR-54 (削除済み予約 90 ngày),
      §6.3 bảng 21 chuyển trạng thái.
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, 3 course C1/C2/C3\n"
       "- Mở /basic/calendar-management/21 > tab 予約カレンダー > chế độ xem 一覧")
BK = CAL + "\n- Trong khoảng lọc có 8 booking đủ các trạng thái 0/1/2/3/4/5/6/7"

S5 = [
    # ══════════════════ Modal filter booking ══════════════════
    tc("Modal filter booking", "FUNC-001", "Normal",
       "Filter booking: khoảng ngày mặc định theo chế độ xem đang mở",
       BK,
       "1. Ở chế độ xem TUẦN, mở modal filter → quan sát ngày mặc định\n"
       "2. Ở chế độ xem THÁNG, mở modal filter → quan sát\n"
       "3. Ở chế độ xem LIST, mở modal filter → quan sát",
       "3 chế độ xem",
       "- Tuần: mặc định là tuần hiện tại\n"
       "- Tháng: mặc định từ ngày đầu tháng đến ngày cuối tháng\n"
       "- List: mặc định từ ngày hiện tại đến 1 tháng sau",
       note="Nguồn: Quản lý calendar_new r345-r347."),

    tc("Modal filter booking", "FUNC-004", "Boundary",
       "Filter booking: quan hệ start date và end date",
       BK,
       "1. Chọn start < end trong 1 tuần → Lọc\n2. Trong 1 tháng · nhiều tháng · nhiều năm → Lọc\n"
       "3. Chọn start = end → Lọc\n4. Chọn start > end → Lọc",
       "4 quan hệ ngày",
       "- Bước 1-2: lọc thành công, dữ liệu đúng khoảng đã chọn\n"
       "- Bước 3: hiển thị data đúng 1 ngày đó\n- Bước 4: KHÔNG được phép (chặn / báo lỗi)",
       note="Nguồn: Quản lý calendar_new r348-r353."),

    tc("Modal filter booking", "FUNC-004", "Boundary",
       "Filter booking theo thời gian bắt đầu course — biên và quan hệ from/to",
       BK,
       "1. Quan sát giá trị mặc định của 2 ô time\n2. Chọn time from 00:00, to 23:59 → Lọc\n"
       "3. Chọn from < to (09:00 ~ 12:00) → Lọc\n4. Chọn from = to (09:00 ~ 09:00) → Lọc\n"
       "5. Chọn from > to (12:00 ~ 09:00) → Lọc\n"
       "6. Chỉ nhập from, để to = 00:00 → Lọc; rồi chỉ nhập to, from = 00:00 → Lọc",
       "6 tổ hợp",
       "- Bước 1: mặc định 00:00 - 00:00 ⇒ KHÔNG filter theo time (lấy tất cả)\n"
       "- Bước 2-3: lọc đúng slot có start_time trong khoảng\n"
       "- Bước 5: KHÔNG được phép\n"
       "- Bước 4 và 6: cần chốt hành vi (TC gốc để trống kết quả)",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar_new r354-r363. ⚠️ r360 (from = to khác 00:00) và r362-r363 "
            "chỉ có tiêu đề, không có kết quả mong đợi. Xem MT-21."),

    tc("Modal filter booking", "FUNC-002", "Normal",
       "Filter booking theo course — 4 tổ hợp chọn",
       BK + "\n- Calendar có C1, C2, C3 đều có booking trong khoảng lọc",
       "1. Không chọn course nào → Lọc\n2. Chọn 1 course C2 → Lọc\n"
       "3. Chọn 2 course C1 + C3 → Lọc\n4. Bấm 全選択 → Lọc",
       "3 course",
       "- Bước 1: tương đương select all — hiện booking của cả 3 course\n"
       "- Bước 2: chỉ booking của C2\n- Bước 3: chỉ booking của C1 và C3\n"
       "- Bước 4: hiện booking của cả 3 course",
       note="Nguồn: Quản lý calendar_new r368-r371."),

    tc("Modal filter booking", "FUNC-002", "Normal",
       "Filter booking: cập nhật list course khi add/edit/xóa course",
       BK,
       "1. Mở modal filter, ghi nhận list course\n2. Đóng, thêm course C4 → mở lại modal filter\n"
       "3. Đổi tên C1 → mở lại\n4. Xóa C3 → mở lại",
       "3 → 4 → 3 course",
       "- Modal filter luôn hiện danh sách course mới nhất sau mỗi thao tác",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r364-r367 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("Modal filter booking", "FUNC-002", "Normal",
       "Filter theo trạng thái booking — 4 trạng thái riêng lẻ, mỗi trạng thái 1 tập status",
       BK,
       "1. Không chọn trạng thái nào → Lọc\n2. Chọn「予約確定」→ Lọc\n"
       "3. Chọn「予約リクエスト中」→ Lọc\n4. Chọn「キャンセルリクエスト中」→ Lọc\n"
       "5. Chọn「キャンセル」→ Lọc\n6. Bấm 全選択 → Lọc",
       "8 booking đủ status 0-7",
       "- Bước 1: lọc ALL trạng thái, GỒM CẢ booking đăng ký full slot (status 3) và deny (status 6)\n"
       "- Bước 2: chỉ status IN (1,2)\n- Bước 3: chỉ status = 0\n- Bước 4: chỉ status = 5\n"
       "- Bước 5: chỉ status IN (4,7)\n"
       "- Bước 6 (全選択): status IN (0,1,2,4,5,7) — KHÔNG gồm status 3 và 6",
       note="Nguồn: Quản lý calendar_new r372-r379. ⚠️ Điểm dễ nhầm: KHÔNG chọn gì ≠ 全選択 "
            "(khác nhau ở status 3 và 6)."),

    tc("Modal filter booking", "FUNC-002", "Normal",
       "Filter theo trạng thái bill tiền — 4 trạng thái",
       BK + "\n- Có booking đủ 4 payment_status: 0 (未決済), 1 (決済成功), 2 (決済なし), 3 (返金済み)",
       "1. Không chọn trạng thái bill → Lọc\n2. Chọn「未決済」→ Lọc\n3. Chọn「決済成功」→ Lọc\n"
       "4. Chọn「返金済み」→ Lọc\n5. Chọn「決済なし」→ Lọc\n6. 全選択 → Lọc",
       "Booking đủ 4 payment_status",
       "- Bước 1 và 6: lọc `payment_status` IN (0,1,2,3) — kết quả GIỐNG nhau\n"
       "- Bước 2: chỉ payment_status = 0\n- Bước 3: chỉ = 1\n- Bước 4: chỉ = 3\n- Bước 5: chỉ = 2",
       note="Nguồn: Quản lý calendar_new r380-r387."),

    tc("Modal filter booking", "FUNC-002", "Normal",
       "Filter kết hợp nhiều điều kiện + áp dụng ở 3 chế độ xem",
       BK,
       "1. Filter date + time → Lọc\n2. date + course · date + status booking · date + status bill\n"
       "3. date + time + course · date + time + status booking · date + time + status bill\n"
       "4. date + course + status booking + status bill\n5. Kết hợp TẤT CẢ điều kiện\n"
       "6. Áp cùng bộ filter ở màn tuần, tháng, list",
       "9 tổ hợp",
       "- Mọi tổ hợp: kết quả là GIAO của tất cả điều kiện, không sót không thừa\n"
       "- Bước 6: cùng bộ filter cho cùng tập booking ở cả 3 chế độ xem",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r388-r399 — TC gốc CHỈ CÓ TIÊU ĐỀ (12 dòng), "
            "kết quả mong đợi do AI bổ sung. Cần Leader xác nhận."),

    tc("Modal filter booking", "FUNC-001", "Normal",
       "Nút 絞り込み表示 (kể cả double click) và trường hợp không chọn gì",
       BK,
       "1. Chọn filter → bấm「絞り込み表示」1 lần\n2. Double click nút này\n"
       "3. Mở modal, không chọn gì → bấm 絞り込み表示",
       "—",
       "- Bước 1-2: hiển thị data theo filter đã chọn, double click không gửi 2 request\n"
       "- Bước 3: hiển thị toàn bộ data (không lọc)",
       note="Nguồn: Quản lý calendar_new r400-r401."),

    # ══════════════════ Modal filter 受付枠 ══════════════════
    tc("Modal filter 受付枠", "FUNC-001", "Normal",
       "Filter slot: mặc định từ hôm nay đến 1 tháng sau; data ngoài phải ăn theo filter trong",
       CAL + "\n- Hôm nay 08/05. Tab 受付枠一覧 có slot rải từ 01/05 đến 30/06",
       "1. Vào tab 受付枠, bấm 絞り込み → quan sát khoảng ngày mặc định\n"
       "2. Chọn khoảng 06/05 → 12/05 → Lọc\n3. Quan sát cả trong modal và ngoài màn quản lý",
       "Slot rải 2 tháng",
       "- Mặc định 08/05 → 08/06\n- Sau khi lọc: chỉ hiện slot từ 06/05 đến 12/05\n"
       "- Ngày hiển thị bên NGOÀI màn quản lý cũng ăn theo khoảng filter bên trong",
       note="Nguồn: Quản lý calendar_new r451-r455 (nhấn mạnh「DATA DATE BÊN NGOÀI PHẢI ĂN THEO "
            "DATE FILTER BÊN TRONG」)."),

    tc("Modal filter 受付枠", "FUNC-004", "Boundary",
       "Filter slot: start = end, start > end và biên time",
       CAL,
       "1. Chọn start date = end date → Lọc\n2. Chọn start date > end date → Lọc\n"
       "3. Chọn start time = end time = 00:00 → Lọc\n"
       "4. Chọn start time = end time khác 00:00 (09:00~09:00) → Lọc\n"
       "5. Chọn start time > end time → Lọc",
       "5 tổ hợp",
       "- Bước 1: hiển thị data đúng ngày hôm đó\n- Bước 2: KHÔNG được phép\n"
       "- Bước 3: lọc ALL start_time (không lọc theo time)\n"
       "- Bước 4 và 5: data invalid ⇒ KHÔNG hiển thị kết quả nào",
       note="Nguồn: Quản lý calendar_new r456-r457, r461-r463."),

    tc("Modal filter 受付枠", "FUNC-002", "Normal",
       "Filter slot theo course: chỉ course ON, reload list khi course thay đổi",
       CAL + "\n- Có 25 course, 3 course OFF; mở 2 tab: tab 1 màn quản lý list, tab 2 màn quản lý course",
       "1. Tab 1: mở modal filter slot → quan sát list course\n"
       "2. Tab 2: thêm course mới C_new\n3. Tab 1: bấm lại nút filter → quan sát list course\n"
       "4. Không chọn course nào → Lọc\n5. Chọn 1 course → Lọc",
       "25 course, 3 OFF",
       "- Bước 1: chỉ 22 course ON, list dài có scroll\n"
       "- Bước 3: list course reload, có C_new (không cần F5 trang)\n"
       "- Bước 4: lọc all course ON (KHÔNG hiện slot của course OFF)\n"
       "- Bước 5: chỉ slot của course đã chọn",
       note="Nguồn: Quản lý calendar_new r464-r469."),

    # ══════════════════ リクエスト一括操作 ══════════════════
    tc("リクエスト一括操作", "UI-001", "Normal",
       "Modal action đồng loạt: giao diện, số lượng đã chọn, nút đóng",
       BK,
       "1. Tick 3 booking → bấm「アクションを選択する」\n2. Quan sát action được chọn sẵn và số lượng\n"
       "3. Bấm nút「閉じる」\n4. Mở lại, bấm icon X",
       "3 booking",
       "- Default chọn sẵn action「新規予約リクエストを承認する」\n"
       "- Hiển thị「3人を選択中」\n- Nút 閉じる và icon X đều đóng popup, không thực hiện gì",
       note="Nguồn: Quản lý calendar_new r403-r405."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Approve request booking hàng loạt — chọn 実行する: 4 tổ hợp setting message/action",
       BK + "\n- Có 3 booking đang リクエスト của LINE user U1, U2, U3\n"
            "- Calendar setting リクエスト制",
       "Với từng tổ hợp, tick 3 booking → chọn「新規予約リクエストを承認する」+「実行する」→ "
       "bấm「リクエスト一括操作を実行する」, sau đó kiểm status ở màn list và tin LINE:\n"
       "1. KHÔNG setting msg action nào\n2. Có msg pattern + tích SỬ DỤNG\n"
       "3. Có msg pattern nhưng tích KHÔNG sử dụng\n4. Có msg pattern + multi action",
       "4 tổ hợp × 3 booking",
       "- Cả 4 tổ hợp: 3 booking chuyển sang 予約確定, màn list ngoài cập nhật status\n"
       "- Tổ hợp 1: KHÔNG gửi msg\n- Tổ hợp 2: gửi msg pattern lúc approve booking\n"
       "- Tổ hợp 3: KHÔNG gửi msg\n- Tổ hợp 4: gửi msg pattern + chạy đủ multi action",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r407-r410. RULE-06: verify tới tin LINE user nhận được."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Approve request booking hàng loạt — chọn 実行しない: đổi status nhưng KHÔNG gửi gì",
       BK + "\n- 3 booking đang リクエスト; calendar có setting msg pattern + multi action",
       "1. Tick 3 booking → chọn approve + 「実行しない」→ thực hiện\n"
       "2. Kiểm status và tin LINE của 3 user\n3. Lặp với 3 tổ hợp setting msg khác nhau",
       "3 tổ hợp",
       "- Cả 3 tổ hợp: booking chuyển 予約確定, màn list cập nhật\n"
       "- TUYỆT ĐỐI KHÔNG gửi msg và KHÔNG chạy multi action nào",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r411-r413. Khớp spec BR-49."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Approve hàng loạt: ưu tiên action của COURSE (5 tổ hợp)",
       BK + "\n- Booking thuộc course C1 có setting action riêng cho tab 予約リクエスト承認時",
       "Với từng tổ hợp, approve hàng loạt và kiểm tin LINE:\n"
       "1. 実行する + course có action message + CÓ sử dụng\n"
       "2. 実行する + course có action message + KHÔNG sử dụng\n"
       "3. 実行する + course chỉ có multi action (không có message)\n"
       "4. 実行する + course có cả message + multi action\n5. 実行しない",
       "5 tổ hợp",
       "- Tổ hợp 1, 3, 4: gửi action của COURSE\n"
       "- Tổ hợp 2: gửi action CHUNG của booking\n"
       "- Tổ hợp 5: KHÔNG gửi gì dù course có setting",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r415-r419. Khớp spec BR-44."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Approve request booking hàng loạt → add remind vào event_step_time",
       BK + "\n- Calendar đã setting 2 mốc remind (1 trước, 1 sau buổi học)\n"
            "- 3 booking đang リクエスト ở slot tương lai",
       "1. Approve hàng loạt 3 booking\n"
       "2. Query `event_step_time` theo `user_booking_id` của 3 booking",
       "3 booking × 2 mốc remind",
       "- Sinh 6 bản ghi `event_step_time` (3 booking × 2 mốc), status = 0\n"
       "- `sent_date_time` của mốc TRƯỚC tính theo start time của booking; mốc SAU tính theo end time",
       note="Nguồn: Quản lý calendar_new r414 + Setting calendar r1032-r1039 (SpecChange #32367)."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Deny request booking hàng loạt — 実行する / 実行しない, và KHÔNG add remind",
       BK + "\n- 3 booking đang リクエスト; calendar đã setting remind",
       "1. Tick 3 booking → chọn「新規予約リクエストを否認する」+ 実行する (4 tổ hợp msg) → thực hiện\n"
       "2. Lặp với 実行しない (3 tổ hợp)\n3. Query `event_step_time`",
       "7 tổ hợp",
       "- Mọi tổ hợp: 3 booking chuyển sang「否認済」, màn list cập nhật\n"
       "- 実行する + có msg pattern sử dụng: gửi msg lúc deny booking\n"
       "- 実行しない: KHÔNG gửi msg\n"
       "- KHÔNG có bản ghi `event_step_time` nào được tạo cho 3 booking này",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r420-r427."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Deny request booking: ưu tiên action — luôn dùng action CHUNG, kể cả course có action riêng",
       BK + "\n- Booking thuộc course C1 có setting action riêng",
       "1. Deny 1 booking với 実行する\n2. Kiểm tin LINE user nhận",
       "Course có action riêng",
       "- User nhận action CHUNG của booking (KHÔNG dùng action của course)",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r717, r722. ⚠️ Spec BR-45: `denyBooking` và `denyCancel` "
            "DÙNG CHUNG `setting_action_reject` + `message_send_deny` ⇒ không tách được nội dung "
            "từ chối đặt và từ chối hủy. Xem MT-22."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Approve request CANCEL hàng loạt — 7 tổ hợp + xóa remind",
       BK + "\n- 3 booking đang キャンセルリクエスト, đã có remind trong `event_step_time`",
       "1. Tick 3 booking → chọn「キャンセルリクエストを承認する」+ 実行する (4 tổ hợp msg) → thực hiện\n"
       "2. Lặp với 実行しない (3 tổ hợp)\n3. Query `event_step_time` của 3 booking",
       "7 tổ hợp",
       "- Mọi tổ hợp: 3 booking chuyển sang「キャンセル」\n"
       "- 実行する + msg pattern sử dụng: gửi msg lúc approve request cancel\n"
       "- Toàn bộ remind CHƯA GỬI (status = 0) của 3 booking bị XÓA khỏi `event_step_time`",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r428-r435."),

    tc("リクエスト一括操作", "MSG-002", "Normal",
       "Deny request CANCEL hàng loạt — 7 tổ hợp + KHÔNG xóa remind",
       BK + "\n- 3 booking đang キャンセルリクエスト, đã có remind",
       "1. Tick 3 booking → chọn「キャンセルリクエストを否認する」+ 実行する (4 tổ hợp) → thực hiện\n"
       "2. Lặp với 実行しない (3 tổ hợp)\n3. Query `event_step_time`",
       "7 tổ hợp",
       "- Mọi tổ hợp: 3 booking QUAY VỀ trạng thái「予約確定」\n"
       "- 実行する + msg pattern sử dụng: gửi msg lúc deny request cancel\n"
       "- Remind trong `event_step_time` KHÔNG bị xóa",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r436-r443."),

    tc("リクエスト一括操作", "OUT-TRUTH-001", "Abnormal",
       "Chọn tập booking có cả loại KHÔNG phù hợp với action → bỏ qua, không đổi trạng thái",
       BK + "\n- Tick 4 booking: 2 đang リクエスト booking, 1 đang キャンセルリクエスト, 1 đã 予約確定",
       "1. Chọn action「キャンセルリクエストを承認する」→ thực hiện\n"
       "2. Kiểm trạng thái của cả 4 booking\n3. Kiểm tin LINE của 4 user",
       "4 booking hỗn hợp",
       "- Chỉ booking đang キャンセルリクエスト được chuyển sang キャンセル\n"
       "- 3 booking còn lại GIỮ NGUYÊN trạng thái và KHÔNG nhận action nào",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r445. ⚠️ Spec BR-22: cặp (status nguồn, action) không khớp "
            "guard ⇒ IM LẶNG nhưng API vẫn trả `success: true` (RA-17). Xem MT-23."),

    tc("リクエスト一括操作", "BULK-001", "Normal",
       "Chọn ALL booking của 1 trang + thao tác liên tiếp + thao tác ở trang 2",
       BK + "\n- Tab 予約一覧 có 55 booking đang リクエスト, phân trang 20/trang",
       "1. Tick 全選択 của trang 1 → approve hàng loạt → kiểm 20 booking\n"
       "2. Ngay sau đó tick tiếp 10 booking khác → deny hàng loạt → kiểm\n"
       "3. Sang trang 2, tick 5 booking → approve → kiểm",
       "55 booking",
       "- Bước 1: đúng 20 booking của trang 1 chuyển 予約確定\n"
       "- Bước 2: 10 booking chuyển 否認済, không ảnh hưởng 20 booking bước 1\n"
       "- Bước 3: thao tác ở trang 2 hoạt động bình thường",
       note="Nguồn: Quản lý calendar_new r446-r448."),

    tc("リクエスト一括操作", "PAY-STATE-001", "Abnormal",
       "Approve hàng loạt có bill tiền: 1 booking bill LỖI → dừng ở booking đó",
       BK + "\n- Calendar enable bill tiền UnivaPay\n"
            "- 3 booking đang リクエスト của U1, U2, U3; thẻ của U2 sẽ bill FAIL",
       "1. Tick 3 booking theo thứ tự U1, U2, U3 → approve hàng loạt\n"
       "2. Quan sát message lỗi\n3. Kiểm trạng thái từng booking và giao dịch trên UnivaPay",
       "3 booking, 1 thẻ fail",
       "- U1: approve thành công + bill thành công\n"
       "- U2: bill lỗi ⇒ báo lỗi「一般エラーが発生しました。詳細情報は管理画面で確認できます」, "
       "booking GIỮ NGUYÊN trạng thái リクエスト\n"
       "- U3: KHÔNG được xử lý (dừng luôn tại booking lỗi)\n"
       "- Trên UnivaPay chỉ có 1 giao dịch thành công của U1",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r36-r39 + spec logic-spec.md:1042 "
            "(「lỗi thanh toán ở bản ghi đầu tiên làm return, bỏ dở toàn bộ phần còn lại」)."),

    # ══════════════════ Admin thêm booking thủ công ══════════════════
    tc("Admin thêm booking thủ công", "UI-001", "Normal",
       "Modal 予約追加: thông tin course và kỳ hạn nhận booking",
       CAL + "\n- Course C1 có ảnh, giá 5.000 yên, slot 01/10 09:00-10:00\n"
             "- Calendar KHÔNG setting giới hạn thời gian nhận/dừng nhận",
       "1. Từ modal danh sách booking của slot, bấm「予約追加」\n2. Quan sát header modal",
       "1 slot của course có giá",
       "- Hiện tên course đã chọn trước đó\n- Time course format「2024.10.01(日) 09:00~10:00」\n"
       "- Kỳ hạn nhận booking hiện「~ <time start của course>まで予約できます」\n"
       "- Khối thông tin course: ảnh · tên · giá「¥ 5,000」· 日時",
       note="Nguồn: Quản lý calendar_new r526-r532."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Normal",
       "Chọn friend TRONG hệ thống: search theo system name và line name",
       CAL + "\n- Bot A có friend U1 (LINE name「太郎」, system name「タロウ」)",
       "1. Chọn tab「エルメ上に表示されている」\n2. Search「タロウ」→ chọn U1\n"
       "3. Search「太郎」→ chọn U1\n4. Search「zzzz」(không tồn tại) → bấm đăng ký booking",
       "1 friend U1",
       "- Bước 2, 3: tìm được U1 bằng cả 2 loại tên\n"
       "- Bước 4: không có kết quả ⇒ bấm đăng ký báo lỗi「お客様名を選択してください」, không tạo booking",
       note="Nguồn: Quản lý calendar_new r534-r536."),

    tc("Admin thêm booking thủ công", "PERF-LARGE-001", "Normal",
       "Bot có nhiều friend → search trong modal add booking không quá chậm",
       CAL + "\n- Bot A có ≥ 50.000 friend",
       "1. Mở modal 予約追加, gõ từ khóa search\n2. Đo thời gian trả kết quả",
       "50.000 friend",
       "- Kết quả trả về trong ≤ 3 giây, không treo trình duyệt",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r537 — TC gốc chỉ có tiêu đề「Check performance khi search」, "
            "ngưỡng 3 giây do AI đặt. Cần Leader chốt ngưỡng."),

    tc("Admin thêm booking thủ công", "FUNC-001", "Normal",
       "Admin book: không có form nào ON → vẫn booking bình thường",
       CAL + "\n- Calendar đã tắt hết câu hỏi (chỉ còn 2 câu mặc định bị OFF)",
       "1. Mở modal 予約追加, chọn friend U1\n2. Bấm đăng ký",
       "0 câu hỏi hiển thị",
       "- Không hiển thị khối câu hỏi nào\n- Booking thành công, tạo bản ghi status = 2",
       note="Nguồn: Quản lý calendar_new r538."),

    tc("Admin thêm booking thủ công", "DATA-001", "Normal",
       "Admin book friend TRONG hệ thống: câu trả lời form được lưu vào friend info",
       CAL + "\n- Calendar mới tạo, có 2 form mặc định (system name, email)\n"
             "- Thêm form gắn friend info basic: SĐT, ngày sinh, địa chỉ",
       "1. Mở modal 予約追加, chọn friend U1, tích「すでに情報が登録されている場合、自動入力する」\n"
       "2. Điền đủ các câu hỏi → đăng ký\n"
       "3. Query `friend_information_values` của U1 và mở màn 友だち情報管理",
       "5 câu hỏi gắn friend info",
       "- Booking thành công\n- Giá trị đã nhập được lưu vào friend info tương ứng của U1\n"
       "- Mở lại modal add booking cho U1: các ô tự động fill lại đúng giá trị đã lưu",
       note="Nguồn: Quản lý calendar_new r539-r540 (verify 3 tầng: booking + DB friend info + "
            "auto fill lần sau — RULE-07)."),

    tc("Admin thêm booking thủ công", "FUNC-003", "Abnormal",
       "Admin book: validate 4 kiểu format của câu hỏi short text",
       CAL + "\n- Có 4 câu hỏi 短文回答 với 4 rule validate: カナ入力 · 電話番号 11 số · メールアドレス · 整数",
       "Với mỗi câu hỏi nhập giá trị sai rồi đúng, bấm đăng ký:\n"
       "1. カナ: nhập「abc」rồi nhập「タロウ」\n2. SĐT: nhập「abc」, 10 số, 12 số, rồi 11 số\n"
       "3. Email: nhập「abc」rồi「a+b@test.com」\n4. 整数: nhập「1.5」rồi「10」",
       "4 loại validate",
       "- カナ sai: báo lỗi「カナのみ入力してください。」· đúng: pass\n"
       "- SĐT không phải số: Invalid; 10 và 12 số: báo lỗi「携帯電話11桁の数値を入力してください。」; "
       "11 số: pass\n"
       "- Email sai format: báo lỗi「Emailフォーマットが不正なメールアドレスです。フォーマットを確認してください。」; "
       "email có dấu + : pass\n"
       "- 整数 không nguyên: báo lỗi「数値のみ入力してください。」; số nguyên: pass\n"
       "- Sau khi submit thành công: giá trị được lưu đúng vào friend info tương ứng",
       note="Nguồn: Quản lý calendar_new r542-r545."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Abnormal",
       "Admin book: câu hỏi 必須 bỏ trống → Invalid; câu 任意 bỏ trống → pass",
       CAL + "\n- Có 1 câu hỏi 必須 (Q1) và 1 câu 任意 (Q2)",
       "1. Bỏ trống cả Q1 và Q2 → đăng ký\n2. Điền Q1, bỏ trống Q2 → đăng ký",
       "2 câu hỏi khác mức bắt buộc",
       "- Bước 1: báo lỗi「回答を入力してください」ở Q1, không tạo booking\n"
       "- Bước 2: đăng ký thành công",
       note="Nguồn: Quản lý calendar_new r546-r548."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Admin book: 3 kiểu liên kết friend info của câu hỏi",
       CAL + "\n- Có 3 câu hỏi: Q1 không gắn friend info, Q2 tự tạo friend info, "
             "Q3 gắn friend info có sẵn F1",
       "1. Admin book cho U1, điền cả 3 câu → đăng ký\n"
       "2. Query `calendar_course_bookings.friend_info` và `friend_information_values` của U1\n"
       "3. Mở màn 友だち情報管理",
       "3 kiểu liên kết",
       "- Q1: chỉ lưu trong `calendar_course_bookings.friend_info`, KHÔNG lưu vào friend info nào\n"
       "- Q2: tự tạo friend info mới (folder 未分類) và gán giá trị cho U1\n"
       "- Q3: gán giá trị vào F1 của U1",
       note="Nguồn: Quản lý calendar_new r549-r551."),

    tc("Admin thêm booking thủ công", "FRIEND-001", "Normal",
       "Admin book: câu hỏi 単一選択 / 複数選択 / 日時 — quy tắc lưu friend info",
       CAL + "\n- Có câu hỏi 単一選択 (radio), 複数選択 (checkbox), 日時 (có time và không time)",
       "1. Admin book, trả lời đủ 4 loại câu hỏi → đăng ký\n"
       "2. Query `calendar_course_bookings.friend_info` và `friend_information_values`",
       "4 loại câu hỏi",
       "- 単一選択: lưu được vào friend info (nếu có gắn)\n"
       "- 複数選択: CHỈ lưu trong `calendar_course_bookings.friend_info`, KHÔNG lưu vào friend info\n"
       "- 日時 KHÔNG có time: lưu được vào friend info\n"
       "- 日時 CÓ time: KHÔNG gán được vào friend info nào",
       note="Nguồn: Quản lý calendar_new r563-r583."),

    tc("Admin thêm booking thủ công", "FUNC-001", "Normal",
       "Option すでに情報が登録されている場合、自動入力する — 4 trạng thái",
       CAL + "\n- U1 có sẵn giá trị friend info; U2 chưa có\n"
             "- Form setting すでに友だち情報が登録されている場合、初めから入力された状態にする đang BẬT",
       "1. Quan sát trạng thái mặc định của checkbox\n"
       "2. KHÔNG tích checkbox, chọn U1 → quan sát các ô câu hỏi\n"
       "3. Tích checkbox, chọn U1 → quan sát\n4. Tích checkbox, chọn U2 → quan sát\n"
       "5. Tích → bỏ tích → tích lại\n6. Tích rồi chọn U1, sau đó đổi sang U2",
       "2 friend khác trạng thái data",
       "- Bước 1: default KHÔNG tích\n"
       "- Bước 2: VẪN tự động fill (vì form setting đang bật) — nếu form setting tắt thì không fill\n"
       "- Bước 3: fill đúng giá trị của U1\n- Bước 4: không fill gì\n"
       "- Bước 5: tích→fill, bỏ tích→clear thông tin đã fill, tích lại→fill lại\n"
       "- Bước 6: đổi friend thì fill lại theo friend mới",
       note="Nguồn: Quản lý calendar_new r584-r590."),

    tc("Admin thêm booking thủ công", "MSG-002", "Normal",
       "Admin book: 実行する / 実行しない × setting 全承認 và リクエスト制",
       CAL + "\n- Booking chung có setting msg text + multi action",
       "1. Calendar setting 全承認: admin book chọn「実行する」→ kiểm tin U1\n"
       "2. Cùng setting, chọn「実行しない」→ kiểm\n"
       "3. Đổi calendar sang リクエスト制, lặp 2 bước trên (action lúc admin approve)",
       "2 chế độ duyệt × 2 lựa chọn action",
       "- 実行する: U1 nhận action tương ứng (booking approve luôn / approve request)\n"
       "- 実行しない: U1 KHÔNG nhận gì, nhưng booking VẪN được tạo và status vẫn đổi",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r591-r609. Khớp spec BR-49."),

    tc("Admin thêm booking thủ công", "FUNC-002", "Abnormal",
       "Admin book khách NGOÀI hệ thống: bắt buộc nhập tên",
       CAL,
       "1. Chọn tab「LINE公式アカウントに友だち追加していない または、エルメ上に表示されていない」\n"
       "2. Bỏ trống ô tên → bấm đăng ký\n3. Nhập tên「山田太郎」→ đăng ký",
       "Khách ngoài hệ thống",
       "- Bước 2: báo lỗi「客様名を入力してください」\n- Bước 3: Add booking success",
       note="Nguồn: Quản lý calendar_new r611-r612."),

    tc("Admin thêm booking thủ công", "DATA-001", "Abnormal",
       "Admin book khách NGOÀI hệ thống: KHÔNG lưu friend info, KHÔNG gửi action",
       CAL + "\n- Calendar có 3 câu hỏi gắn friend info",
       "1. Book cho khách ngoài hệ thống, điền đủ câu hỏi, chọn「実行する」→ đăng ký\n"
       "2. Query `calendar_course_bookings.friend_info` và `friend_information_values`\n"
       "3. Query `action_lineuser`\n4. Tích/bỏ tích option auto fill và quan sát",
       "Khách ngoài hệ thống",
       "- Câu trả lời CHỈ lưu vào `calendar_course_bookings.friend_info`\n"
       "- KHÔNG có bản ghi nào trong `friend_information_values`\n"
       "- KHÔNG gửi action, KHÔNG insert bản ghi vào `action_lineuser` dù chọn 実行する\n"
       "- Option auto fill: dù tích hay không cũng KHÔNG hiển thị data",
       note="Nguồn: Quản lý calendar_new r614-r623 + spec BR-26 (chỉ gửi khi `line_user_id` khác rỗng)."),

    tc("Admin thêm booking thủ công", "UI-001", "Normal",
       "Alert cảnh báo không thu tiền — ma trận 4 tổ hợp",
       CAL + "\n- Course Cf không setting giá; course Cp có giá 5.000 yên",
       "Với từng tổ hợp, bấm đăng ký booking và quan sát alert:\n"
       "1. Admin ENABLE bill tiền + course Cf\n2. Admin ENABLE bill tiền + course Cp\n"
       "3. Admin DISABLE bill tiền + course Cf\n4. Admin DISABLE bill tiền + course Cp",
       "4 tổ hợp",
       "- Tổ hợp 2: HIỆN alert「有料コースの場合でも、お客様に料金は請求されませんが "
       "この予約を登録してよろしいですか？」\n"
       "- Tổ hợp 1, 3, 4: KHÔNG hiện alert",
       note="Nguồn: Quản lý calendar_new r625-r628."),

    tc("Admin thêm booking thủ công", "CONC-001", "Abnormal",
       "Double click nút 登録する → chỉ tạo 1 booking; icon X đóng không tạo",
       CAL,
       "1. Điền đủ thông tin, double click nhanh nút「登録する」\n"
       "2. Query `calendar_course_bookings`\n3. Mở lại modal, điền data rồi bấm icon X",
       "1 booking",
       "- Chỉ tạo ĐÚNG 1 booking\n- Bấm X: đóng modal, không tạo booking nào",
       note="Nguồn: Quản lý calendar_new r630-r631."),

    tc("Admin thêm booking thủ công", "DATA-REF-001", "Normal",
       "Admin book đúng user đang đợi nhận thông báo cùng slot → UPDATE bản ghi cũ (BR-28)",
       CAL + "\n- U1 có 1 booking status = 3 (đợi nhận thông báo) ở slot X\n"
             "- U1 cũng có 1 booking status = 3 ở slot Y",
       "1. Admin book cho U1 vào slot X\n"
       "2. Query booking của U1 ở slot X và slot Y\n"
       "3. Admin book cho U2 (chưa có booking nào) vào slot X → query",
       "2 slot, 2 user",
       "- Bước 2: bản ghi status = 3 ở slot X được UPDATE thành status = 2 (admin book), "
       "KHÔNG tạo bản ghi mới\n"
       "- Bản ghi ở slot Y KHÔNG bị đụng tới\n"
       "- Bước 3: tạo bản ghi booking MỚI cho U2",
       note="Nguồn: Quản lý calendar_new r632-r634. Khớp spec BR-28 / T-07."),

    tc("Admin thêm booking thủ công", "FUNC-001", "Normal",
       "Mở modal add booking từ 4 màn khác nhau → thông tin course/slot đúng theo màn nguồn",
       CAL + "\n- Có nhiều slot của nhiều course",
       "1. Mở modal add booking từ màn danh sách booking theo NGÀY\n"
       "2. Từ màn theo TUẦN\n3. Từ màn theo THÁNG\n4. Từ màn theo LIST (tab 受付枠)",
       "4 lối vào",
       "- Cả 4 lối: modal hiện đúng course và khung giờ của slot đã chọn ở màn nguồn, "
       "không lấy nhầm slot khác",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar_new r635-r638 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("Admin thêm booking thủ công", "DATA-001", "Normal",
       "Admin book: payment_status luôn là 決済なし, số tiền lấy từ course tại thời điểm tạo",
       CAL + "\n- Calendar enable bill tiền, course Cp giá 5.000 yên",
       "1. Admin book cho U1 vào slot của Cp\n"
       "2. Query `calendar_course_bookings` bản ghi vừa tạo\n"
       "3. Kiểm dashboard Stripe/UnivaPay",
       "Course có giá 5.000",
       "- `payment_status` = 2 (決済なし)\n- `payment_amount` = 5000 (snapshot từ `calendar_course.amount`)\n"
       "- KHÔNG có giao dịch nào trên cổng thanh toán",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-29 — corpus chỉ khẳng định「admin booking không bill tiền」"
            "mà không kiểm 2 cột DB. Cần Leader xác nhận."),

    # ══════════════════ Detail booking & lịch sử ══════════════════
    tc("Detail booking & lịch sử", "UI-001", "Normal",
       "Detail booking đã approve: thông tin friend info và thanh toán",
       CAL + "\n- Booking B1 status 予約確定 của U1, đã thanh toán bằng thẻ 4242…4242, hạn 01/30\n"
             "- U1 có friend info: お名前, メールアドレス, 都道府県",
       "1. Mở detail booking B1, tab 予約情報\n2. Quan sát các khối thông tin",
       "1 booking đã thanh toán",
       "- Avatar + LINE名 / システム表示名\n- ステータス:「予約確定」\n"
       "- Khối friend info: hiện đúng お名前 · メールアドレス · 都道府県 của U1\n"
       "- 決済システム: tên cổng · 決済金額「¥ 5,000」· カード番号「XXXXXXXX4242」· 有効期限「01/30」",
       note="Nguồn: Quản lý calendar_new r642-r649."),

    tc("Detail booking & lịch sử", "UI-001", "Abnormal",
       "Detail booking: friend KHÔNG có friend info → để trống, không lỗi",
       CAL + "\n- U2 chưa có friend info nào, đã có booking B2",
       "1. Mở detail booking B2",
       "Friend không có info",
       "- Khối friend info hiển thị TRỐNG (không lỗi JS, không hiện undefined/null)",
       note="Nguồn: Quản lý calendar_new r645, r936."),

    tc("Detail booking & lịch sử", "STATE-DEP-001", "Normal",
       "Detail booking đã approve: popup cancel booking — có/không thực hiện action",
       CAL + "\n- Booking B1 status 予約確定; calendar có setting msg lúc cancel",
       "1. Mở detail B1 → bấm「この予約をキャンセルする」→ quan sát popup\n"
       "2. Chọn KHÔNG thực hiện action → bấm「キャンセルする」→ kiểm status + tin LINE\n"
       "3. Lặp với booking khác, chọn CÓ thực hiện action",
       "2 lựa chọn action",
       "- Popup hiện đúng tên course, thời gian booking, avatar/LINE name/system name\n"
       "- Cả 2 bước: booking chuyển sang status 7 (admin cancel), màn list cập nhật\n"
       "- Bước 2: U1 KHÔNG nhận tin\n- Bước 3: U1 nhận msg lúc cancel",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r651-r655, r985-r996."),

    tc("Detail booking & lịch sử", "MSG-002", "Normal",
       "Admin cancel: nội dung gửi phụ thuộc approve_type của moment cancel (3 nhánh)",
       CAL + "\n- Booking B1 status 予約確定",
       "1. Setting cancel = 全承認 (approve_type 1) → admin cancel B1 → kiểm tin U1\n"
       "2. Setting cancel = リクエスト制 (approve_type 2) → admin cancel booking khác → kiểm\n"
       "3. Setting cancel = 予約後のキャンセル不可 (approve_type 3) → admin cancel → kiểm",
       "3 nhánh approve_type",
       "- Nhánh 1: gửi nội dung của `message_send_end` (msg khi cancel hoàn tất)\n"
       "- Nhánh 2: gửi nội dung của `message_send_approve` (msg khi approve request cancel)\n"
       "- Nhánh 3: KHÔNG gửi gì\n- Cả 3 nhánh: booking vẫn chuyển sang status 7",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-46 — corpus KHÔNG có TC nào phân biệt 3 nhánh này khi "
            "admin cancel. Cần Leader xác nhận (đây là điểm dễ gửi nhầm nội dung cho khách)."),

    tc("Detail booking & lịch sử", "STATE-DEP-001", "Normal",
       "Detail booking đang リクエスト: approve — 5 tổ hợp action",
       CAL + "\n- Booking B3 status リクエスト của U1",
       "1. Mở detail B3, bấm「承認する」, chọn「実行しない」→ kiểm\n"
       "2. Booking khác: chọn「実行する」+ không setting action nào\n"
       "3. + có msg pattern và CÓ sử dụng\n4. + msg pattern KHÔNG sử dụng\n"
       "5. + msg pattern + multi action",
       "5 tổ hợp",
       "- Mọi tổ hợp: booking chuyển sang 予約確定\n"
       "- Tổ hợp 1: không gửi action nào (kể cả khi course có setting action riêng)\n"
       "- Tổ hợp 2: approve, không gửi action\n- Tổ hợp 3: gửi msg pattern\n"
       "- Tổ hợp 4: không gửi msg pattern\n- Tổ hợp 5: gửi msg pattern + chạy multi action",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r699-r705."),

    tc("Detail booking & lịch sử", "PAY-STATE-001", "Normal",
       "Approve booking có bill tiền: 4 tổ hợp enable/disable × course có/không giá",
       CAL + "\n- Booking đang リクエスト với thẻ đã lưu\n- Course Cp có giá, Cf không giá",
       "1. Enable bill tiền + course Cp → approve → kiểm giao dịch trên cổng và `payment_status`\n"
       "2. Enable bill tiền + course Cf → approve → kiểm\n"
       "3. Disable bill tiền + course Cp → approve → kiểm\n4. Disable + course Cf → approve",
       "4 tổ hợp",
       "- Tổ hợp 1: approve + THU TIỀN thật, `payment_status` = 1\n"
       "- Tổ hợp 2, 3, 4: chỉ approve, KHÔNG thu tiền, `payment_status` = 2",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r706, r708-r710. Khớp spec BR-24."),

    tc("Detail booking & lịch sử", "PAY-STATE-001", "Abnormal",
       "Approve booking mà bill FAIL → booking GIỮ NGUYÊN trạng thái リクエスト",
       CAL + "\n- Calendar enable bill Stripe\n"
             "- Booking B4 đang リクエスト, U1 đã nhập thẻ 4000000000003063 (pass lúc validate card "
             "nhưng fail lúc charge)",
       "1. Mở detail B4 → bấm「承認する」\n2. Quan sát message\n"
       "3. Query `calendar_course_bookings` của B4 và `calendar_course_receptions`",
       "Thẻ fail lúc charge",
       "- Báo lỗi thanh toán\n- Booking B4 GIỮ NGUYÊN status = 0 (リクエスト), KHÔNG chuyển 予約確定\n"
       "- `payment_status` KHÔNG đổi\n- Bộ đếm `total_approve` KHÔNG tăng",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r707. Khớp spec BR-24 (thất bại ⇒ return ngay)."),

    tc("Detail booking & lịch sử", "STATE-DEP-001", "Normal",
       "Detail booking đang リクエスト: deny — 5 tổ hợp + không bill tiền",
       CAL + "\n- Booking B5 status リクエスト",
       "1. Bấm「否認する」với「実行しない」→ kiểm\n"
       "2. Với「実行する」× 4 tổ hợp msg pattern\n3. Query `payment_status` sau khi deny",
       "5 tổ hợp",
       "- Mọi tổ hợp: booking chuyển sang 否認済 (status 6)\n"
       "- 実行しない: không gửi action\n- Có msg pattern + sử dụng: gửi msg\n"
       "- Dù enable hay disable bill tiền cũng KHÔNG thu tiền",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r716-r723."),

    tc("Detail booking & lịch sử", "STATE-DEP-001", "Normal",
       "Detail booking: approve / deny request CANCEL — 5 tổ hợp mỗi loại",
       CAL + "\n- Booking B6 status キャンセルリクエスト",
       "1. Bấm approve request cancel với 実行しない, rồi 4 tổ hợp msg pattern\n"
       "2. Với booking khác, bấm deny request cancel — lặp 5 tổ hợp\n3. Kiểm status sau mỗi lần",
       "10 tổ hợp",
       "- Approve request cancel: booking chuyển sang キャンセル (status 4)\n"
       "- Deny request cancel: booking QUAY VỀ 予約確定\n"
       "- Gửi msg đúng theo từng tổ hợp như các case trên",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r711-r715, r724-r728."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Tab 予約履歴: thông tin cơ bản và người thao tác (3 loại)",
       CAL + "\n- Booking B1 đã trải qua: user book → admin (chính) approve → staff S1 refund",
       "1. Mở detail B1 → tab「予約履歴」\n2. Quan sát các dòng lịch sử",
       "3 thao tác từ 3 loại actor",
       "- Mỗi dòng có avatar + LINE名/システム表示名\n"
       "- Ngày giờ thao tác format「2024.09.24 (木) 10:31」\n"
       "- Người thao tác:「友だち」(LINE user) ·「管理者」(admin chính) ·「スタッフA」(staff)",
       note="Nguồn: Quản lý calendar_new r657-r661."),

    tc("Detail booking & lịch sử", "DATA-AUDIT-001", "Normal",
       "Tab 予約履歴: 13 loại nội dung 内容 và mã status tương ứng trong DB",
       CAL + "\n- Chuẩn bị booking đi qua đủ 13 loại thao tác",
       "1. Mở tab 予約履歴 của các booking tương ứng\n"
       "2. Đối chiếu với `calendar_course_booking_history_actions.status`",
       "13 loại thao tác",
       "-「予約完了」= status 1 ·「予約リクエスト」= 2 ·「予約リクエスト 承認」= 4 ·"
       "「予約リクエスト 否認」= 14 ·「手動予約追加」= 5 ·「予約キャンセル」= 6 ·"
       "「キャンセルリクエスト」= 7 ·「キャンセルリクエスト 承認」= 9 ·「キャンセルリクエスト 否認」= 15 ·"
       "「手動予約キャンセル」= 10 ·「キャンセル待ち 登録」= 11 ·「¥〇の返金（エルメから or 決済システムから）」= 12 ·"
       "「予約情報の削除」và「受付枠削除による予約削除」= 13",
       note="Nguồn: Quản lý calendar_new r949-r962 (khối màn booking đã xóa có mã status ĐẦY ĐỦ NHẤT). "
            "⚠️ Khối r735-r748 (tab thường) để TRỐNG nhiều ô mã status — đã lấy theo khối đầy đủ hơn. "
            "Xem MT-24."),

    tc("Detail booking & lịch sử", "UI-001", "Abnormal",
       "Tab 予約履歴: 2 trạng thái dễ nhầm — キャンセル待ち登録 vs キャンセルリクエスト",
       CAL + "\n- Booking B7 status 3 (đăng ký chờ hủy) và booking B8 status 5 (xin hủy)",
       "1. Mở tab 予約履歴 của B7 → quan sát nội dung\n2. Mở của B8 → quan sát\n"
       "3. So sánh 2 nhãn hiển thị",
       "2 booking khác bản chất",
       "- B7 hiện「キャンセル待ち 登録」(đăng ký nhận thông báo khi có chỗ)\n"
       "- B8 hiện「キャンセルリクエスト」(xin hủy booking đã có)\n"
       "- 2 nhãn PHẢI phân biệt được, không được hiển thị giống nhau",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý calendar_new r672, r760 — TC gốc ĐẶT CÂU HỎI「Trạng thái này khác gì "
            "trạng thái キャンセルリクエスト?」chứ không có kết quả mong đợi. Xem MT-25."),

    tc("Detail booking & lịch sử", "DATA-001", "Normal",
       "Khối 過去（直近10件）の予約一覧: 10 booking gần nhất của friend trong calendar",
       CAL + "\n- U1 có 15 booking trong calendar 21 (đủ các status), trong đó có booking do admin book",
       "1. Mở detail booking của U1 → tab 予約履歴\n2. Quan sát khối 過去（直近10件）の予約一覧\n"
       "3. Đối chiếu với `SELECT b.reception_id, b.status, c.system_name FROM "
       "calendar_course_bookings b JOIN calendar_course c ON b.course_id = c.id "
       "WHERE b.calendar_id = 21 AND b.line_user_id = {U1} AND b.deleted_at IS NULL "
       "ORDER BY b.id DESC LIMIT 10`",
       "15 booking của U1",
       "- Hiện đúng 10 booking mới nhất theo id giảm dần\n"
       "- Format mỗi dòng:「2024.09.21 (月) 10:00 ~ 11:00」+ trạng thái + tên course\n"
       "- Nhãn trạng thái: status 0,5 →「リクエスト」· 1,2 →「予約確定」· 3 →「通知受取希望」· "
       "4,7 →「キャンセル」· 6 →「否認」\n"
       "- Booking do admin book: KHÔNG có data để hiển thị",
       note="Nguồn: Quản lý calendar_new r677-r682."),

    tc("Detail booking & lịch sử", "STATE-001", "Abnormal",
       "Detail request booking: admin đã approve/deny rồi mà mở lại → ẩn nút approve/deny",
       CAL + "\n- Booking B9 vừa được admin approve; booking B10 vừa bị deny",
       "1. Từ tab lịch sử, mở lại modal detail của request booking B9\n2. Lặp với B10",
       "2 booking đã xử lý",
       "- Cả 2: KHÔNG hiển thị khối chọn action và 2 nút 承認する / 否認する\n"
       "- Chỉ có nút 閉じる",
       note="Nguồn: Quản lý calendar_new r860-r863, r882-r883."),

    tc("Detail booking & lịch sử", "STATE-DEP-001", "Normal",
       "Detail booking đã cancel: xóa booking → vào màn 削除済み予約 giữ 90 ngày",
       CAL + "\n- Booking B11 status キャンセル",
       "1. Mở detail B11 → bấm「この予約を削除する」→ quan sát popup confirm\n"
       "2. Bấm xóa\n3. Mở màn 削除済み予約\n4. Bấm icon X trên popup confirm ở lần khác",
       "1 booking cancel",
       "- Popup confirm hiện ra\n- Sau khi xóa: booking hiển thị ở màn 削除済み予約 trong 90 ngày\n"
       "- Bấm X: đóng popup, không xóa",
       note="Nguồn: Quản lý calendar_new r778-r781. Khớp spec BR-54."),

    # ══════════════════ Booking đã xóa ══════════════════
    tc("Booking đã xóa", "LIST-001", "Normal",
       "Màn 削除済み予約: các cột dữ liệu và sort theo thời gian xóa",
       CAL + "\n- Có 5 booking đã xóa ở các thời điểm khác nhau",
       "1. Bấm nút「削除済み予約」\n2. Quan sát các cột\n3. Sort tăng dần rồi giảm dần theo 削除された日時",
       "5 booking đã xóa",
       "- Cột 削除された日時 format「2024.09.25 (金) 10:31」\n"
       "- Cột お名前 (avatar/line name/friend name) · 予約していたコース · 予約していた日時\n"
       "- Sort 2 chiều hoạt động đúng",
       note="Nguồn: Quản lý calendar_new r922-r927."),

    tc("Booking đã xóa", "DATA-001", "Abnormal",
       "Màn 削除済み予約: booking xóa quá 90 ngày → không hiển thị",
       CAL + "\n- Booking B12 có `deleted_at` = 100 ngày trước; B13 = 80 ngày trước",
       "1. Mở màn 削除済み予約\n"
       "2. Đối chiếu query `… WHERE b.deleted_at IS NOT NULL AND "
       "DATEDIFF(CURDATE(), DATE(b.deleted_at)) <= 90`\n3. Query trực tiếp B12 trong DB",
       "2 booking xóa khác thời điểm",
       "- Chỉ hiển thị B13\n- B12 KHÔNG hiển thị trên UI\n"
       "- ⚠️ B12 VẪN CÒN trong DB (chỉ là bộ lọc hiển thị, không có job nào xóa thật)",
       note="Nguồn: Quản lý calendar_new r929-r930 + spec BR-54. Điểm bổ sung về DB là suy luận "
            "từ spec (「UI nói dữ liệu tự xoá sau 90 ngày nhưng không có job/cron nào thực sự xoá」)."),

    tc("Booking đã xóa", "UI-001", "Normal",
       "Detail booking đã xóa: status và trạng thái bill",
       CAL + "\n- Booking B13 đã xóa, trước đó đã thanh toán 5.000 yên bằng thẻ 4242…4242",
       "1. Mở màn 削除済み予約 → bấm 詳細 của B13\n2. Quan sát tab 予約情報",
       "1 booking đã xóa, đã thanh toán",
       "- ステータス:「予約削除済み」\n- 決済金額「¥ 5,000」· カード番号「XXXXXXXX4242」· 有効期限「01/30」\n"
       "- Trạng thái bill hiển thị đúng 1 trong 5 giá trị: 未決済 / 決済成功 / 決済なし / 返金済み / 未返金",
       note="Nguồn: Quản lý calendar_new r934, r938-r941."),

    tc("Booking đã xóa", "OUT-TRUTH-001", "Abnormal",
       "🔴 Modal 削除済み予約: bấm 承認する / 否認する trên booking đã xóa",
       CAL + "\n- Booking B14 đã bị xóa mềm khi đang ở status リクエスト",
       "1. Mở màn 削除済み予約 → mở detail B14\n"
       "2. Nếu có nút 承認する: bấm vào\n3. Quan sát UI và query `calendar_course_bookings` của B14",
       "1 booking đã xóa còn status リクエスト",
       "- Modal của booking ĐÃ XÓA KHÔNG được hiển thị nút 承認する / 否認する\n"
       "- Nếu bấm được: UI KHÔNG được báo thành công khi DB không đổi\n"
       "- Nếu bấm「承認する」mà booking bị TỪ CHỐI ⇒ FAIL nghiêm trọng, phải raise bug ngay",
       spec="Đã hỏi leader",
       note="🔴 Suy luận của AI từ spec §11.1 mục 10-11 (B-2: `findById()` thiếu `withTrashed()` "
            "⇒ API LUÔN trả success:true, UI đóng modal và vẽ lại bảng dù DB không đổi) và "
            "B-1 (nút 承認する/否認する ĐẢO HANDLER ở 2 file modal 削除済み予約, hiện đang bị B-2 che). "
            "Corpus KHÔNG có TC nào. DỰ KIẾN FAIL. Xem MT-26."),

    # ══════════════════ Hoàn tiền ══════════════════
    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Refund từ LME — UnivaPay môi trường TEST: 2 kiểu booking approve",
       CAL + "\n- Calendar liên kết UnivaPay môi trường TEST\n"
             "- 2 booking đã thanh toán: B1 (user book approve ngay), B2 (user book, admin approve)",
       "1. Mở detail B1 → bấm「返金する」→ chọn「この画面から返金を行う」→ tích checkbox confirm → "
       "bấm 返金する\n2. Query `calendar_course_bookings` và `calendar_course_booking_history_actions`\n"
       "3. Kiểm dashboard UnivaPay\n4. Lặp với B2",
       "2 booking đã thanh toán",
       "- Cả 2: `payment_status` = 3 (返金済み)\n"
       "- `calendar_course_booking_history_actions.reason` = '¥〇の返金（エルメから）'\n"
       "- Trên UnivaPay: giao dịch chuyển sang trạng thái đã refund\n"
       "- ⚠️ `status` của booking KHÔNG đổi (booking VẪN chiếm chỗ)",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r823-r824 + spec BR-P27. RULE-07: verify DB + màn admin + "
            "dashboard cổng thanh toán."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Refund UnivaPay: đã refund trên UnivaPay rồi refund lại từ LME → báo lỗi",
       CAL + "\n- Booking B1 đã được refund THỦ CÔNG trên dashboard UnivaPay",
       "1. Mở detail B1 → refund từ LME\n2. Quan sát message\n3. Query `payment_status`",
       "Booking đã refund bên ngoài",
       "- Hiện message「返金金額が課金金額を超過しています。」\n"
       "- `payment_status` KHÔNG đổi (vẫn là 1)",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r825-r826."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Refund Stripe: đã refund trên Stripe rồi refund lại từ LME → báo lỗi từ Stripe",
       CAL + "\n- Booking B2 thanh toán Stripe, đã refund thủ công trên dashboard Stripe",
       "1. Mở detail B2 → refund từ LME\n2. Quan sát message\n3. Query `payment_status`",
       "Booking Stripe đã refund",
       "- Hiện lỗi do Stripe trả về:「Charge ch_xxx has already been refunded.」\n"
       "- `payment_status` KHÔNG đổi",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r839-r840, r847."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Refund CHỈ ĐÁNH DẤU (返金は決済システム管理画面から行い…) → không gọi cổng thanh toán",
       CAL + "\n- Booking B3 đã thanh toán Stripe 5.000 yên",
       "1. Mở màn refund → chọn「返金は決済システム管理画面から行い エルメ上のステータスのみ返金済みに変更する」\n"
       "2. Tích checkbox confirm → bấm 返金する\n3. Query DB\n4. Kiểm dashboard Stripe",
       "Refund kiểu đánh dấu",
       "- `calendar_course_bookings.payment_status` = 3\n"
       "- `calendar_course_booking_history_actions.reason` = '¥〇の返金（決済システムから）'\n"
       "- Trên Stripe: giao dịch VẪN ở trạng thái đã thu tiền (KHÔNG bị refund)",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r830, r836, r843, r849. Khớp spec BR-P28."),

    tc("Hoàn tiền 返金", "FUNC-002", "Abnormal",
       "Refund: không tích checkbox xác nhận → không cho bấm nút refund",
       CAL + "\n- Booking B4 đã thanh toán",
       "1. Mở màn refund\n2. KHÔNG tích checkbox「返金後の取り消し操作はできないことを確認しました。」\n"
       "3. Bấm nút「返金する」",
       "Chưa tích confirm",
       "- Nút 返金する bị disable HOẶC báo lỗi bắt buộc tích checkbox\n"
       "- KHÔNG thực hiện refund",
       note="Nguồn: Quản lý calendar_new r831, r844. ⚠️ 2 dòng ghi 2 hành vi khác nhau (disable "
            "vs validate báo lỗi) — cần chốt 1. Xem MT-27."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Refund môi trường PRODUCTION — UnivaPay và Stripe",
       "- Calendar liên kết cổng thanh toán ở môi trường **本番 (production)**\n"
       "- Có 2 booking thật đã thanh toán: 1 qua UnivaPay, 1 qua Stripe (số tiền nhỏ nhất cho phép)",
       "1. Refund booking UnivaPay từ LME → kiểm DB + dashboard UnivaPay\n"
       "2. Refund booking Stripe từ LME → kiểm DB + dashboard Stripe",
       "2 booking thật",
       "- Cả 2: `payment_status` = 3, history ghi '¥〇の返金（エルメから）'\n"
       "- Số tiền được hoàn thật trên dashboard tương ứng",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r832-r835, r845-r848. RULE-08: bill tiền phải test PRODUCTION."),

    tc("Hoàn tiền 返金", "DATA-AUDIT-001", "Normal",
       "Modal lịch sử refund: 4 kiểu thao tác refund và người thực hiện",
       CAL + "\n- Có 4 booking đã refund: LME+Stripe, LME+UnivaPay, hệ thống bill+Stripe, "
             "hệ thống bill+UnivaPay; 2 do admin chính, 2 do staff A",
       "1. Mở tab 予約履歴 → bấm vào dòng refund → quan sát modal 返金",
       "4 kiểu refund",
       "- Title「返金」· LINE名/システム表示名 · コース · 日時 · 返金した金額\n"
       "- 返金処理 hiển thị đúng 1 trong 4:「エルメから操作（Stripe）」·「エルメから操作（UnivaPay）」·"
       "「決済システムからから操作（Stripe）」·「決済システムからから操作（UnivaPay）」\n"
       "- この操作が行われた日時 format「2024.09.22 (火) 10:10」\n"
       "- この操作を行ったユーザー hiện「管理者」hoặc「スタッフA」",
       note="Nguồn: Quản lý calendar_new r898-r909."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Refund: booking do ADMIN đặt (決済なし) → KHÔNG hiển thị nút 返金する",
       CAL + "\n- Booking B5 do admin book, `payment_status` = 2 (決済なし)",
       "1. Mở detail B5\n2. Tìm nút「返金する」",
       "Booking admin book",
       "- KHÔNG hiển thị nút 返金する",
       note="Nguồn: Quản lý calendar_new r102, r104-r105, r109."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Refund KHÔNG gửi thông báo cho khách",
       CAL + "\n- Booking B6 đã thanh toán của LINE user U1",
       "1. Admin refund B6 từ LME\n2. Kiểm LINE app của U1\n3. Kiểm màn lịch sử booking của U1",
       "1 booking được refund",
       "- U1 KHÔNG nhận bất kỳ tin nhắn nào về việc hoàn tiền\n"
       "- Màn lịch sử của U1 hiển thị trạng thái bill là 返金済み",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-P27 (「KHÔNG thông báo cho khách」) và BR-P33 "
            "(admin cũng không nhận mobile_notify cho refund) — corpus KHÔNG có TC. "
            "Cần Leader xác nhận đây là đúng thiết kế hay là thiếu sót."),

    # ══════════════════ Feature #26528 — hiển thị bill tiền ══════════════════
    tc("Detail booking & lịch sử", "PAY-STATE-001", "Normal",
       "Feature #26528: hiển thị bill tiền ở màn Today/New booking, list, detail, lịch sử",
       CAL + "\n- Calendar enable bill tiền; có booking ở đủ trạng thái thanh toán",
       "Kiểm hiển thị số tiền và trạng thái bill tại 4 màn:\n"
       "1. Màn Today/New booking (2 tab)\n2. Màn quản lý theo list\n3. Modal detail booking\n"
       "4. Modal detail lịch sử booking",
       "Booking đủ trạng thái bill",
       "- Cả 4 màn đều hiển thị số tiền và trạng thái bill nhất quán\n"
       "- User request booking → approve: hiện「決済成功」\n"
       "- User booking approve ngay đã thanh toán: hiện「決済成功」\n"
       "- Booking đã approve có thanh toán: hiện nút「返金する」",
       note="Nguồn: Quản lý calendar r997-r1044 (Feature #26528, 08/2024 — khối này CHỈ CÓ ở tab "
            "「Quản lý calendar」, không có ở bản _new). Xem MT-11."),

    tc("Detail booking & lịch sử", "PAY-STATE-001", "Normal",
       "Feature #26528: setting hiển thị giá course × enable/disable bill tiền (4 tổ hợp)",
       CAL + "\n- Course C1 có giá 5.000 yên",
       "Với từng tổ hợp, kiểm hiển thị giá ở 5 màn phía LINE user "
       "(list course · detail course · màn confirm booking · màn booking success · các màn lịch sử):\n"
       "1. Setting CÓ hiển thị giá + ENABLE bill tiền\n2. Setting CÓ hiển thị giá + DISABLE bill\n"
       "3. Setting KHÔNG hiển thị giá + ENABLE bill\n4. Setting KHÔNG hiển thị giá + DISABLE bill",
       "4 tổ hợp × 5 màn",
       "- Tổ hợp 1, 2, 3: CÓ hiển thị số tiền ở cả 5 màn\n"
       "- Tổ hợp 4: KHÔNG hiển thị số tiền ở cả 5 màn\n"
       "- ⇒ Khi enable bill tiền thì luôn hiện giá, bỏ qua setting 表示設定",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar r998-r1001 + Setting calendar r1137."),
]
