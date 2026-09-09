# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm quản lý đặt chỗ phía admin: tab 本日/新着, 4 chế độ xem calendar,
modal danh sách booking.

Nguồn chính: 11.2 TCsLine_LessonCalendar
  - tab「Quản lý calendar_new」(478 TC lá) — bản mô tả GIAO DIỆN MỚI: tuần có 2 tab コース別/一覧,
    modal edit slot, xóa nhiều slot. Đối chiếu spec ui-spec.md:1264 và BR-17 ⇒ là bản CÒN HIỆU LỰC.
  - tab「Quản lý calendar」(460 TC lá) — tab master còn cột ticket mới nhất (#32704 11/2025,
    #29484 04/2025, #27978 01/2025) + khối Test security + Feature #26528 hiển thị bill tiền.
  - tab「Today&NewBooking」(45 TC lá, 10/2024 — spec change 8/10/2024 dùng user_update_time)
  - tab「Ngần check_step」— ma trận coverage theo màn, KHÔNG có kết quả mong đợi (dùng đối chiếu).
Xem MT-11 về quan hệ 2 tab Quản lý calendar / _new.
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Có lesson calendar「レッスンA」(id 21) đang ON, 3 course C1/C2/C3 đều ON\n"
       "- Mở /basic/calendar-management/21 > tab 予約カレンダー")
DATA = (CAL + "\n- C1 có slot 12:00-13:30 ngày hôm nay với 定員 5, đã có 2 booking 予約確定, "
        "1 booking リクエスト, 1 booking キャンセル")

S3 = [
    # ══════════════════ Tab 本日/新着の予約 ══════════════════
    tc("Tab 本日/新着の予約", "UI-001", "Normal",
       "Mở tab 本日／新着の予約 → default hiển thị tab 新着の予約一覧",
       CAL,
       "1. Bấm tab menu「本日／新着の予約」\n2. Quan sát tab con được chọn sẵn",
       "—",
       "- Tab con mặc định là「新着の予約一覧」\n"
       "- Hiển thị ngày hiện tại đúng format「2024年 10月 1日(日)」",
       note="Nguồn: Today&NewBooking r3-r4."),

    tc("Tab 本日/新着の予約", "LIST-001", "Abnormal",
       "Tab 新着の予約: không có booking mới trong 7 ngày → hiện message rỗng",
       CAL + "\n- Không có booking nào có `user_update_time` trong 7 ngày gần đây",
       "1. Mở tab 新着の予約一覧",
       "0 booking mới",
       "- Hiện message「7日間以内の新着予約はありません」\n- Không hiện dòng booking nào",
       note="Nguồn: Today&NewBooking r5."),

    tc("Tab 本日/新着の予約", "DATA-001", "Normal",
       "Tab 新着の予約: lấy booking theo user_update_time trong 7 ngày + received_booking_date >= hôm nay",
       CAL + "\n- Hôm nay 08/10. Chuẩn bị booking: B1 (user_update_time 08/10, slot 20/10), "
             "B2 (user_update_time 01/10, slot 20/10), B3 (user_update_time 05/10, slot 01/10 — quá khứ), "
             "B4 (user_update_time 30/09, slot 20/10), B5 (user_update_time 09/10 — tương lai, slot 20/10)",
       "1. Mở tab 新着の予約一覧\n2. Đối chiếu với query:\n"
       "`SELECT b.id, b.user_update_time, r.received_booking_date FROM calendar_course_bookings b "
       "LEFT JOIN calendar_course_receptions r ON b.reception_id = r.id JOIN calendar_course c "
       "ON r.course_id = c.id WHERE b.calendar_id = 21 AND b.deleted_at IS NULL AND "
       "(b.user_update_time BETWEEN '2024-10-01 00:00:00' AND '2024-10-08 23:59:59') AND "
       "r.received_booking_date >= CURDATE() AND c.booking_page_display = 1 "
       "ORDER BY b.user_update_time DESC`",
       "5 booking như trên",
       "- Hiển thị B1 và B2 (thoả cả 2 điều kiện)\n"
       "- KHÔNG hiển thị B3 (slot quá khứ), B4 (ngoài 7 ngày), B5 (user_update_time tương lai)\n"
       "- Sort: booking có user_update_time mới nhất lên đầu",
       note="Nguồn: Today&NewBooking r5, r39-r51 (spec change 8/10/2024 đổi từ booking_date sang "
            "user_update_time). Gộp ma trận 5 điểm vì cùng 1 truy vấn."),

    tc("Tab 本日/新着の予約", "DATA-001", "Normal",
       "Cột user_update_time CHỈ update khi LINE user thao tác, KHÔNG update khi admin thao tác",
       CAL + "\n- Có 1 booking B1 của LINE user U1",
       "Thực hiện lần lượt, sau mỗi thao tác query `user_update_time` của B1 và kiểm tab 新着の予約:\n"
       "1. U1 request booking\n2. Admin deny → 3. Admin approve\n4. Admin cancel\n"
       "5. U1 request cancel\n6. Admin deny request cancel → 7. Admin approve request cancel\n"
       "8. U1 cancel ngay",
       "8 thao tác",
       "- Bước 1, 5, 8 (LINE user thao tác): `user_update_time` ĐƯỢC cập nhật → booking hiện ở "
       "tab 新着の予約\n"
       "- Bước 2, 3, 4, 6, 7 (admin thao tác): `user_update_time` KHÔNG đổi, chỉ đổi `status`",
       note="Nguồn: Today&NewBooking r37-r38, r53-r61. Gộp vì là 1 chuỗi thao tác liên tiếp trên "
            "cùng 1 booking."),

    tc("Tab 本日/新着の予約", "DATA-001", "Abnormal",
       "Admin book / admin book full slot → KHÔNG hiện ở tab 新着の予約; user book full slot → CÓ hiện",
       CAL + "\n- Slot S1 của C1 còn chỗ; slot S2 đã full và bật nhận thông báo",
       "1. Admin thêm booking vào S1 → kiểm tab 新着の予約\n"
       "2. Admin thêm booking vào S2 (full slot) → kiểm\n"
       "3. LINE user đăng ký nhận thông báo ở S2 → kiểm",
       "3 kiểu đặt",
       "- Bước 1: KHÔNG hiển thị\n- Bước 2: KHÔNG hiển thị\n- Bước 3: CÓ hiển thị",
       note="Nguồn: Today&NewBooking r52, r62-r63."),

    tc("Tab 本日/新着の予約", "DATA-001", "Abnormal",
       "Admin xóa booking → booking biến mất khỏi tab 新着の予約",
       CAL + "\n- Có booking B1 đang hiện ở tab 新着の予約, đã ở trạng thái cancel",
       "1. Admin xóa booking B1\n2. Reload tab 新着の予約",
       "1 booking bị xóa",
       "- B1 không còn trong danh sách 新着の予約",
       note="Nguồn: Today&NewBooking r64."),

    tc("Tab 本日/新着の予約", "UI-001", "Normal",
       "Tab 新着の予約: các cột dữ liệu của 1 dòng booking",
       DATA,
       "1. Mở tab 新着の予約\n2. Quan sát 1 dòng booking",
       "1 booking có bill tiền 5.000 yên",
       "- Hiện đủ: tên course (lấy `system_name`) · ngày thực hiện book · status booking · "
       "profile/line name/system name · số tiền bill「¥ 5,000」· trạng thái bill tiền",
       note="Nguồn: Today&NewBooking r6 — lưu ý「tên course lấy system_name mới đúng」."),

    tc("Tab 本日/新着の予約", "DATA-001", "Normal",
       "Tab 本日の予約: lấy theo received_booking_date = hôm nay, sort theo start_time tăng dần",
       CAL + "\n- Hôm nay có 3 slot: 09:00 (C1), 13:00 (C2), 11:00 (C3), mỗi slot 1 booking",
       "1. Mở tab con「本日の予約一覧」\n2. Quan sát thứ tự và ngày hiển thị",
       "3 booking hôm nay",
       "- Hiện ngày hôm nay format「2024年 10月 1日(日)」\n"
       "- Thứ tự: 09:00 → 11:00 → 13:00 (sort theo start_time ASC)\n"
       "- Chỉ hiện booking của course đang ON",
       note="Nguồn: Today&NewBooking r20, r22. Đã chốt spec: lấy theo thời gian start của booking."),

    tc("Tab 本日/新着の予約", "LIST-001", "Abnormal",
       "Tab 本日の予約 rỗng → hiện message",
       CAL + "\n- Hôm nay không có slot/booking nào",
       "1. Mở tab 本日の予約一覧",
       "0 booking hôm nay",
       "- Hiện message「本日の予約はありません」",
       note="Nguồn: Today&NewBooking r21."),

    tc("Tab 本日/新着の予約", "FUNC-DATE-001", "Normal",
       "Sang ngày mới → tab 本日の予約 tự đổi sang danh sách của ngày mới",
       CAL + "\n- Đang mở tab 本日の予約 lúc 23:55\n- Ngày mai có 2 booking",
       "1. Giữ màn hình mở qua 00:00\n2. Reload trang sau 00:00",
       "Booking của 2 ngày liên tiếp",
       "- Sau 00:00 và reload: danh sách hiển thị booking của NGÀY MỚI, tiêu đề ngày cũng đổi",
       env="PRODUCTION",
       note="Nguồn: Today&NewBooking r28 — TC gốc chỉ có tiêu đề, expected do AI bổ sung. "
            "PRODUCTION vì phụ thuộc thời gian thật của server."),

    tc("Tab 本日/新着の予約", "FUNC-001", "Normal",
       "Cả 2 tab: bấm 詳細 mở đúng modal detail booking theo status",
       DATA,
       "1. Ở tab 新着の予約, bấm 詳細 trên booking đang リクエスト\n"
       "2. Bấm 詳細 trên booking đã approve\n3. Lặp ở tab 本日の予約",
       "Booking đủ 4 status",
       "- Modal detail mở ra giống hệt modal ở màn quản lý calendar\n"
       "- Booking リクエスト: có nút approve + deny\n- Booking đã approve: có nút cancel + refund\n"
       "- Booking request cancel: có nút approve/deny request cancel + refund\n"
       "- Booking đã cancel: có nút xóa booking + refund",
       note="Nguồn: Today&NewBooking r7-r11, r23-r27."),

    tc("Tab 本日/新着の予約", "LIST-001", "Normal",
       "Phân trang tab 本日/新着: đổi số item/page và thao tác ở trang 2",
       CAL + "\n- Tab 新着の予約 có 45 booking",
       "1. Chọn số item/page = 20 → kiểm số trang\n2. Sang trang 2, kiểm data và số thứ tự item\n"
       "3. Ở trang 2 bấm 詳細 mở modal booking và thực hiện approve",
       "45 booking",
       "- Bước 1: có 3 trang\n- Bước 2: hiện đúng item 21-40, không trùng với trang 1\n"
       "- Bước 3: approve thành công, danh sách trang 2 cập nhật status",
       spec="Spec không ghi",
       note="Nguồn: Today&NewBooking r17-r19, r29-r31 — TC gốc CHỈ CÓ TIÊU ĐỀ, kết quả mong đợi "
            "do AI bổ sung. Cần Leader xác nhận số item/page mặc định."),

    tc("Tab 本日/新着の予約", "STATE-001", "Abnormal",
       "Course OFF → ẩn booking của course đó khỏi cả 4 chế độ xem, số lượng ngoài cũng giảm",
       DATA + "\n- Course C1 có 2 booking approve trong tuần này",
       "1. Tắt C1 = OFF\n2. Kiểm màn quản lý theo ngày · theo tuần · theo tháng · theo list\n"
       "3. Đối chiếu số lượng booking hiển thị ở khung giờ tương ứng",
       "1 course OFF có 2 booking",
       "- Cả 4 màn: booking của C1 bị ẩn\n- Số đếm ở khung giờ giảm đúng 2",
       note="Nguồn: Today&NewBooking r32-r35. ⚠️ MÂU THUẪN với「Quản lý course」r213-r220 nói "
            "course OFF VẪN hiện ở các màn quản lý. Xem MT-12."),

    # ══════════════════ Calendar theo ngày ══════════════════
    tc("Calendar theo ngày", "UI-001", "Normal",
       "Default hiển thị ngày hiện tại + format tiêu đề",
       CAL,
       "1. Vào tab 予約カレンダー\n2. Quan sát chế độ xem và tiêu đề ngày",
       "—",
       "- Default hiển thị calendar theo ngày\n- Tiêu đề format「<tháng>月<ngày>日(<thứ>)」ví dụ「10月1日(日)」",
       note="Nguồn: Quản lý calendar_new r14, Quản lý calendar r6, r22."),

    tc("Calendar theo ngày", "LIST-001", "Abnormal",
       "Course chưa có slot nào → hiện message hướng dẫn + link tới màn add slot",
       CAL + "\n- Course C1 chưa có slot nào trong ngày đang xem",
       "1. Quan sát vùng của C1\n2. Bấm vào link「受付枠追加」trong message",
       "Course không slot",
       "- Hiện message「受付枠が登録されていないため、予約を受け付けることができません。"
       "受付枠追加 から受付可能な日時を登録してください。」\n"
       "- Bấm 受付枠追加: mở màn hình add slot",
       note="Nguồn: Quản lý calendar_new r5, Quản lý calendar r12, r45."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Course có slot nhưng chưa có booking → format hiển thị 3 dòng",
       CAL + "\n- Course C1 có slot 12:00-13:30, 定員 5, chưa có booking nào",
       "1. Quan sát khung slot của C1",
       "1 slot trống",
       "- Hiển thị 3 dòng:「12:00-13:30」/「確定 0　残枠 5」/「まだ予約はありません」",
       note="Nguồn: Quản lý calendar_new r6, Quản lý calendar r13."),

    tc("Calendar theo ngày", "DATA-COUNT-001", "Normal",
       "Số lượng theo status ở màn ngày — 予約確定 / リクエスト / キャンセル",
       DATA,
       "1. Quan sát khung slot 12:00-13:30 của C1\n"
       "2. Đối chiếu với `SELECT status, COUNT(*) FROM calendar_course_bookings "
       "WHERE reception_id = {id} AND deleted_at IS NULL GROUP BY status`",
       "2 booking status 1, 1 booking status 0, 1 booking status 4",
       "-「予約確定」= 2 (đếm status IN (1,2) — gồm cả admin book)\n"
       "-「リクエスト」= 1 (đếm status IN (0,5) — gồm cả request booking và request cancel)\n"
       "-「キャンセル」= 1 (đếm status IN (4,7) — gồm cả user cancel và admin cancel)",
       note="Nguồn: Quản lý calendar_new r10-r12. Khớp spec §6.2."),

    tc("Calendar theo ngày", "UI-001", "Normal",
       "Tên course ở màn ngày lấy system_name",
       CAL + "\n- Course C1 có course_name「初心者向けトレーニング」và system_name「初心者」",
       "1. Quan sát tên course hiển thị trên lưới ngày",
       "Course có cả 2 tên",
       "- Hiển thị「初心者」(system_name), KHÔNG hiển thị course_name",
       note="Nguồn: Quản lý calendar_new r7."),

    tc("Calendar theo ngày", "FUNC-001", "Normal",
       "Chọn ngày từ vùng calendar — 5 mốc thời gian",
       CAL + "\n- Có booking rải ở: tháng này, tháng quá khứ, tháng tương lai, năm trước, năm sau",
       "1. Bấm vùng calendar → hiện lịch Nhật\n"
       "2. Chọn lần lượt: 1 ngày tháng này · 1 ngày tháng quá khứ · 1 ngày tháng tương lai · "
       "1 ngày năm trước · 1 ngày năm sau",
       "5 mốc",
       "- Mỗi lần chọn: lưới ngày hiển thị đúng dữ liệu booking của ngày đã chọn, tiêu đề ngày đổi tương ứng",
       note="Nguồn: Quản lý calendar_new r15-r20 (5 điểm CÙNG kết quả → gộp 1 TC, liệt kê đủ ở "
            "cột Các bước)."),

    tc("Calendar theo ngày", "FUNC-001", "Normal",
       "Mũi tên next/back theo ngày và nút 今日",
       CAL,
       "1. Bấm mũi tên next 1 lần → kiểm ngày\n2. Bấm next liên tiếp 5 lần → kiểm\n"
       "3. Bấm back 1 lần, rồi back liên tiếp 5 lần → kiểm\n"
       "4. Đổi qua lại next/back nhiều lần\n5. Bấm nút「今日」",
       "—",
       "- Bước 1-4: mỗi lần bấm lùi/tiến đúng 1 ngày, dữ liệu khớp ngày đang hiển thị\n"
       "- Bước 5: bất kể đang ở ngày nào cũng quay về calendar của HÔM NAY",
       note="Nguồn: Quản lý calendar_new r21-r26."),

    tc("Calendar theo ngày", "UI-002", "Normal",
       "Mouse over slot → hiện nút 詳細を見る, bấm mở màn danh sách booking theo ngày",
       DATA,
       "1. Đưa chuột lên khung slot 12:00-13:30\n2. Bấm nút「詳細を見る」",
       "1 slot có booking",
       "- Hiện nút「詳細を見る」khi hover\n"
       "- Bấm: mở modal danh sách booking theo ngày của slot đó",
       note="Nguồn: Quản lý calendar_new r13."),

    tc("Calendar theo ngày", "UI-002", "Normal",
       "Support #32704: cố định cột khung giờ khi scroll ngang list course",
       CAL + "\n- Calendar có 15 course đều ON, mỗi course có slot trong ngày",
       "1. Mở màn quản lý theo ngày → quan sát có thanh scroll ngang\n"
       "2. Scroll ngang danh sách course\n3. Quan sát cột khung giờ bên trái",
       "15 course",
       "- Có thanh scroll ngang\n- Cột khung giờ 00:00 → 23:30 KHÔNG bị di chuyển khi scroll ngang\n"
       "- Text「受付枠が登録されていないため…」cũng cố định, không trôi theo",
       note="Nguồn: Quản lý calendar r41, r52-r54 (Support #32704, 11/2025 — tab master mới nhất). "
            "TC gốc ghi「chưa test」⇒ chưa có bằng chứng chạy."),

    tc("Calendar theo ngày", "UI-002", "Normal",
       "Calendar ít course → không hiện thanh scroll ngang",
       CAL + "\n- Calendar chỉ có 1 course",
       "1. Mở màn quản lý theo ngày\n2. Quan sát",
       "1 course",
       "- KHÔNG hiện thanh scroll ngang, toàn bộ nội dung nằm gọn trong khung",
       note="Nguồn: Quản lý calendar r42-r43."),

    tc("Calendar theo ngày", "UI-002", "Normal",
       "Màn quản lý theo ngày trên màn hình 1366x768 và trên máy Mac",
       CAL + "\n- Có 2 thiết bị: PC Windows 1366x768 và máy Mac",
       "1. Mở màn quản lý theo ngày ở độ phân giải 1366x768\n2. Mở trên máy Mac (Safari + Chrome)",
       "2 môi trường",
       "- Cả 2: lưới course/khung giờ hiển thị đầy đủ, không tràn ra ngoài, không chồng chữ\n"
       "- Thanh scroll ngang hoạt động bình thường",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Quản lý calendar r60-r61 — TC gốc CHỈ CÓ TIÊU ĐỀ. Kết quả mong đợi do AI bổ sung. "
            "⚠️ Không có tool soi giao diện LME ⇒ cần Leader xác nhận tiêu chí layout."),

    tc("Calendar theo ngày", "PERM-002", "Normal",
       "Account staff mở màn quản lý theo ngày → hiển thị đủ dữ liệu như admin",
       CAL + "\n- Có staff S1 được cấp quyền route レッスン予約",
       "1. Đăng nhập staff S1\n2. Mở màn quản lý theo ngày của calendar 21",
       "Account staff",
       "- Hiển thị đủ list course, slot, số lượng booking như admin chính, không trắng data",
       note="Nguồn: Quản lý calendar r62 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    # ══════════════════ Calendar theo tuần ══════════════════
    tc("Calendar theo tuần", "UI-001", "Normal",
       "Giao diện tuần: bắt đầu thứ 2, format ngày/giờ",
       CAL,
       "1. Chọn chế độ xem theo tuần\n2. Quan sát header cột và cột giờ",
       "—",
       "- Cột đầu tiên là thứ 2\n- Format ngày「10月1日(月)」\n- Format giờ「09:00」",
       note="Nguồn: Quản lý calendar_new r31."),

    tc("Calendar theo tuần", "UI-001", "Normal",
       "Tiêu đề tuần chia 2 vùng, không hiện số 0 ở đầu",
       CAL,
       "1. Chuyển tới tuần 01/10 → 07/10\n2. Quan sát tiêu đề",
       "Tuần 01/10-07/10",
       "- Hiển thị「10月1日 - 10月7日」(không phải 10月01日)",
       note="Nguồn: Quản lý calendar_new r47. ⚠️ Tab「Quản lý calendar」r76 ghi format KHÁC: "
            "「2024年10月 1〜 7日」. Xem MT-11."),

    tc("Calendar theo tuần", "UI-001", "Abnormal",
       "Ô khung giờ tuần: course chưa có slot → trống; có slot chưa booking → icon + tên + 0",
       CAL + "\n- Khung 09:00 thứ 2: C1 chưa có slot; C2 có slot chưa ai đặt",
       "1. Quan sát ô 09:00 thứ 2",
       "2 course khác trạng thái",
       "- C1: ô hiển thị TRỐNG\n- C2: hiển thị icon + tên course + số 0",
       note="Nguồn: Quản lý calendar_new r32-r33 (2 kết quả khác nhau → 1 TC có cả 2 nhánh trong "
            "cùng 1 ô quan sát)."),

    tc("Calendar theo tuần", "UI-001", "Normal",
       "1 khung giờ nhiều course chưa booking → hiện 2 course đầu + 他 xxx 件",
       CAL + "\n- Khung 09:00 thứ 2 có 5 course có slot, trong đó course A có 2 slot cùng khung giờ",
       "1. Quan sát ô 09:00 thứ 2",
       "5 course, 1 course 2 slot",
       "- Hiện icon + tên + 0 của 2 course đầu\n- Dòng cuối hiện「他 3 件」(đếm theo SỐ COURSE, "
       "course A có 2 slot chỉ tính 1 lần)",
       note="Nguồn: Quản lý calendar_new r34. ⚠️ Tab「Quản lý calendar」r65 ghi「xxx là số SLOT "
            "thỏa mãn」— khác đơn vị đếm. Xem MT-11."),

    tc("Calendar theo tuần", "UI-001", "Normal",
       "Ô khung giờ tuần có booking: chỉ hiện status có booking, 4 loại status, ẩn 否認",
       CAL + "\n- Khung 09:00 thứ 2 của C1 có: 2 booking approve, 1 request, 1 cancel, "
             "1 đợi nhận thông báo, 1 booking bị deny",
       "1. Quan sát ô 09:00 thứ 2",
       "6 booking đủ 5 nhóm status",
       "- Hiển thị 4 dòng status có booking: 予約確定 2 · リクエスト 1 · キャンセル 1 · 通知希望 1\n"
       "- KHÔNG hiển thị booking bị deny (否認)\n"
       "- Status nào chưa có booking thì KHÔNG hiển thị dòng đó\n"
       "- Format mỗi dòng: icon status - trạng thái - số lượng",
       note="Nguồn: Quản lý calendar_new r35, r44."),

    tc("Calendar theo tuần", "DATA-COUNT-001", "Normal",
       "Ô tuần: 4 bộ đếm khớp DB — 1 khung 1 course",
       CAL + "\n- Khung 09:00 thứ 2 chỉ có course C1",
       "1. Quan sát 4 con số ở ô 09:00\n2. Query `calendar_course_receptions` của slot đó",
       "1 slot, các status đủ 4 nhóm",
       "-「予約確定」= `total_approve` = COUNT(status IN (1,2))\n"
       "-「リクエスト」= `total_request` + `total_request_cancel` = COUNT(status IN (0,5))\n"
       "-「キャンセル」= `total_cancel` = COUNT(status IN (4,7))\n"
       "-「通知希望」= `total_request_booking_wait_cancel` = COUNT(status = 3)",
       note="Nguồn: Quản lý calendar_new r36-r39. Khớp spec BR-21."),

    tc("Calendar theo tuần", "DATA-COUNT-001", "Normal",
       "Ô tuần: 4 bộ đếm khi 1 khung giờ có NHIỀU course → cộng dồn đúng",
       CAL + "\n- Khung 09:00 thứ 2 có C1 (2 approve, 1 request) và C2 (1 approve, 1 cancel)",
       "1. Quan sát 4 con số ở ô 09:00\n2. Cộng tay số liệu từ 2 slot trong DB",
       "2 course cùng khung giờ",
       "-「予約確定」= 3 (2+1)\n-「リクエスト」= 1\n-「キャンセル」= 1\n"
       "- Không đếm trùng, không bỏ sót course nào trong khung",
       note="Nguồn: Quản lý calendar_new r40-r43."),

    tc("Calendar theo tuần", "FUNC-001", "Normal",
       "Bấm 詳細を見る ở ô tuần → mở danh sách slot dạng コース別",
       CAL + "\n- Khung 09:00 thứ 2 có 3 slot của 2 course",
       "1. Hover ô 09:00 thứ 2 → bấm「詳細を見る」",
       "3 slot",
       "- Mở màn danh sách slot của khung giờ + ngày đã chọn\n"
       "- DEFAULT hiển thị dạng「コース別」(từng course phân biệt), KHÔNG phải dạng 一覧",
       note="Nguồn: Quản lý calendar_new r45. ⚠️ Tab「Quản lý calendar」r74 KHÔNG có khái niệm "
            "コース別/一覧 — xem MT-11. Spec ui-spec.md:1264 xác nhận có 2 view ⇒ theo bản _new."),

    tc("Calendar theo tuần", "FUNC-001", "Normal",
       "Vùng calendar tuần: chọn ngày, next/back tuần, nút 今日, nút 削除",
       CAL,
       "1. Bấm vùng calendar → chọn 1 ngày bất kỳ tháng hiện tại\n"
       "2. Chọn 1 ngày quá khứ · 1 ngày tương lai · 1 ngày năm khác\n"
       "3. Bấm 今日\n4. Bấm 削除 (xóa ngày đã chọn)\n"
       "5. Bấm mũi tên next/back tuần 1 lần và nhiều lần",
       "—",
       "- Bước 1-2: hiển thị TUẦN CHỨA ngày đã chọn, dữ liệu khớp\n"
       "- Bước 3: hiển thị tuần chứa hôm nay\n- Bước 4: xóa lựa chọn ngày\n"
       "- Bước 5: mỗi lần bấm lùi/tiến đúng 1 tuần",
       note="Nguồn: Quản lý calendar_new r47-r62."),

    # ══════════════════ Calendar theo tháng ══════════════════
    tc("Calendar theo tháng", "UI-001", "Normal",
       "Giao diện tháng: tiêu đề, ô ngày không booking, > 2 course",
       CAL + "\n- Ngày 05/10 có 4 course có slot, chưa có booking nào",
       "1. Chuyển sang chế độ xem theo tháng\n2. Quan sát tiêu đề\n3. Quan sát ô ngày 05/10",
       "4 course có slot, 0 booking",
       "- Tiêu đề format「2024年10月」\n"
       "- Ô ngày 05/10 hiện tên 2 course đầu + text「他2件」",
       note="Nguồn: Quản lý calendar_new r67-r68, r78."),

    tc("Calendar theo tháng", "DATA-COUNT-001", "Normal",
       "Ô ngày tháng có booking: format và 3 bộ đếm status",
       CAL + "\n- Ngày 05/10: C1 có 2 approve + 1 request; C2 có 1 cancel",
       "1. Quan sát ô ngày 05/10\n2. Query DB đối chiếu",
       "4 booking / 2 course",
       "- Format mỗi dòng: icon status - số lượng - trạng thái\n"
       "-「予約確定」= 2 (status 1,2) ·「リクエスト」= 1 (status 0,5) ·「キャンセル」= 1 (status 4,7)\n"
       "- Nhiều course trong 1 ngày thì cộng dồn đúng, không đếm trùng",
       note="Nguồn: Quản lý calendar_new r69-r76."),

    tc("Calendar theo tháng", "FUNC-001", "Normal",
       "Ô ngày tháng: hover → 詳細を見る mở list slot trong ngày; vùng calendar KHÔNG mở picker",
       CAL,
       "1. Hover ô ngày 05/10 → bấm「詳細を見る」\n2. Bấm vào vùng tiêu đề calendar tháng",
       "—",
       "- Bước 1: mở danh sách slot của ngày 05/10\n"
       "- Bước 2: KHÔNG hiển thị date picker (giống spec calendar cũ)",
       note="Nguồn: Quản lý calendar_new r77, r79."),

    tc("Calendar theo tháng", "FUNC-001", "Normal",
       "Mũi tên next/back tháng và các nút thao tác trên header tháng",
       CAL,
       "1. Bấm next tháng 1 lần rồi nhiều lần\n2. Bấm back tháng 1 lần rồi nhiều lần\n"
       "3. Đổi qua lại next/back\n4. Bấm 受付枠追加 · 絞り込み · 削除済み予約 · CSV管理",
       "—",
       "- Bước 1-3: mỗi lần lùi/tiến đúng 1 tháng, dữ liệu khớp tháng hiển thị\n"
       "- Bước 4: 4 nút mở đúng 4 màn tương ứng (add slot / modal filter / booking đã xóa / quản lý CSV)",
       note="Nguồn: Quản lý calendar_new r80-r89."),

    # ══════════════════ Calendar theo list ══════════════════
    tc("Calendar theo list", "UI-001", "Normal",
       "Tab 予約一覧: các cột dữ liệu và format",
       DATA + "\n- Có booking do admin book và booking do user book, có bill 5.000 yên",
       "1. Chọn chế độ xem theo list → tab「予約一覧」\n2. Quan sát các cột",
       "Booking đủ loại",
       "- Cột コース: tên course\n- Cột 日時: format「2024.10.01(日) 09:00~11:00」\n"
       "- Cột ステータス: 予約確定 (approve) · 予約確定 + icon (admin book) · リクエスト (booking + cancel) · "
       "キャンセル · 否認\n"
       "- Cột お名前: profile/line name/system name (đúng cả case user book và admin book)\n"
       "- Cột số tiền: format「¥ 5,000」",
       note="Nguồn: Quản lý calendar_new r91-r95."),

    tc("Calendar theo list", "PAY-STATE-001", "Normal",
       "Ma trận trạng thái bill tiền ở tab 予約一覧 — course CÓ bill tiền (6 luồng)",
       DATA + "\n- Calendar enable bill tiền, course C1 có giá 5.000 yên",
       "Tạo 6 booking theo 6 luồng rồi kiểm cột trạng thái bill:\n"
       "1. User booking (リクエスト制) → admin approve → admin refund\n"
       "2. User booking → admin từ chối request\n"
       "3. User booking approve ngay → admin refund\n"
       "4. User request cancel → admin approve cancel\n5. User cancel ngay\n"
       "6. User booking lúc full slot → sau đó booking lại khi có slot trống",
       "6 luồng",
       "- Luồng 1: 未決済 → 決済成功 → 返金済み\n- Luồng 2: giữ 未決済\n"
       "- Luồng 3: 決済成功 → 返金済み\n- Luồng 4: giữ 決済成功 (KHÔNG tự refund)\n"
       "- Luồng 5: giữ 決済成功, không refund\n"
       "- Luồng 6: lúc full slot 決済なし; booking lại nếu approve ngay → 決済成功, "
       "nếu chờ approve → 未決済",
       env="PRODUCTION",
       note="Nguồn: Quản lý calendar_new r96-r101 — TC gốc CHỈ CÓ TIÊU ĐỀ nhưng mô tả đã chứa "
            "kết quả từng bước; AI đã chuyển thành expected đo được. Spec BR-P27: refund KHÔNG đổi status."),

    tc("Calendar theo list", "PAY-STATE-001", "Normal",
       "Ma trận trạng thái bill — course KHÔNG bill tiền hoặc admin disable bill (7 luồng)",
       DATA + "\n- Course C2 không setting giá HOẶC admin đã disable tính năng bill tiền",
       "Tạo 7 booking theo các luồng: user booking chờ approve → approve · user booking approve ngay · "
       "user request cancel → approve cancel · user cancel ngay · user booking full slot → booking lại · "
       "admin booking · admin cancel. Kiểm cột trạng thái bill mỗi lần",
       "7 luồng",
       "- TẤT CẢ đều hiển thị「決済なし」\n"
       "- Modal detail booking KHÔNG hiển thị nút 返金する ở mọi luồng",
       note="Nguồn: Quản lý calendar_new r104-r110."),

    tc("Calendar theo list", "DATA-001", "Normal",
       "Tab 予約一覧: default hiển thị 1 tháng từ hôm nay, chỉ course ON, bỏ booking đã xóa",
       CAL + "\n- Hôm nay 11/04. Có booking ở slot 05/04 (quá khứ), 20/04, 05/05, 20/05 (>1 tháng)\n"
             "- 1 booking của course đã OFF, 1 booking đã bị xóa mềm",
       "1. Mở tab 予約一覧\n2. Đối chiếu với query:\n"
       "`… WHERE b.calendar_id = 21 AND b.deleted_at IS NULL AND (r.received_booking_date BETWEEN "
       "CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 1 MONTH)) AND c.booking_page_display = 1 "
       "ORDER BY r.received_booking_date, r.start_time, b.id ASC`",
       "Booking rải 4 mốc + 2 booking loại trừ",
       "- Chỉ hiện booking của slot 20/04 và 05/05 (trong khoảng 11/04 → 11/05)\n"
       "- KHÔNG hiện booking 05/04, 20/05, booking của course OFF, booking đã xóa\n"
       "- Header hiển thị「表示期間：2023年10月1日(日) 〜 2023年10月31日(火)」khớp khoảng lọc",
       note="Nguồn: Quản lý calendar_new r111, r113."),

    tc("Calendar theo list", "DATA-COUNT-001", "Normal",
       "Tab 予約一覧: bộ đếm 予約数 và キャンセル数",
       CAL + "\n- Trong khoảng lọc có: 3 booking approve, 1 request cancel, 2 booking cancel, "
             "1 booking request (chờ approve), 1 booking deny",
       "1. Quan sát 2 con số 予約数 và キャンセル数\n2. Đối chiếu query COUNT với status IN (1,2,5) "
       "và status IN (4,7)",
       "8 booking đủ status",
       "-「予約数」= 4 (3 approve + 1 request cancel — đếm status 1,2,5)\n"
       "-「キャンセル数」= 2 (đếm status 4,7)\n"
       "- Booking đang chờ approve (status 0) và deny (status 6) KHÔNG được đếm vào 2 số này",
       note="Nguồn: Quản lý calendar_new r114-r115."),

    tc("Calendar theo list", "FUNC-002", "Normal",
       "Tìm kiếm theo friend name / system name ở tab 予約一覧",
       CAL + "\n- Có 30 booking; friend U1 tên LINE「太郎」, system name「タロウ」",
       "1. Search theo friend name「太郎」→ kiểm kết quả\n"
       "2. Search từ khóa không tồn tại「zzzz」→ kiểm\n"
       "3. Xóa từ khóa và Enter\n4. Lặp bước 1-3 với ô search theo system name",
       "30 booking",
       "- Bước 1: chỉ hiện booking của U1\n- Bước 2: hiện danh sách rỗng / message không có kết quả\n"
       "- Bước 3: hiển thị lại ALL data\n- Bước 4: kết quả tương tự",
       note="Nguồn: Quản lý calendar_new r116-r123. ⚠️ Spec ui-spec.md §8 nghi vấn 2 ô search "
            "cùng bind `v-model=\"lineName\"` — nếu 2 ô ảnh hưởng lẫn nhau thì raise bug."),

    tc("Calendar theo list", "BULK-001", "Abnormal",
       "Không chọn booking nào → nút アクションを選択する bị disable",
       CAL + "\n- Tab 予約一覧 có 5 booking",
       "1. Không tick chọn booking nào\n2. Bấm nút「アクションを選択する」",
       "0 booking được chọn",
       "- Nút bị disable, KHÔNG mở modal action đồng loạt",
       note="Nguồn: Quản lý calendar_new r124, r406."),

    tc("Calendar theo list", "BULK-001", "Normal",
       "Chọn 1 hoặc nhiều booking → mở modal action đồng loạt",
       CAL + "\n- Tab 予約一覧 có 5 booking",
       "1. Tick 1 booking → bấm「アクションを選択する」\n2. Đóng, tick 3 booking → bấm lại",
       "1 và 3 booking",
       "- Cả 2 lần đều mở modal action đồng loạt\n"
       "- Modal hiện đúng số lượng đã chọn:「1人を選択中」/「3人を選択中」",
       note="Nguồn: Quản lý calendar_new r125, r404."),

    tc("Calendar theo list", "LIST-001", "Normal",
       "Phân trang tab 予約一覧 và thao tác ở trang 2",
       CAL + "\n- Tab 予約一覧 có 55 booking",
       "1. Chọn số item/page = 20 → kiểm số trang, item start-end mỗi trang\n"
       "2. Sang trang 2 → bấm 詳細 mở modal, thực hiện approve/deny/cancel/refund/xóa booking\n"
       "3. Ở trang 2 dùng chức năng search theo friend name\n4. Ở trang 2 thao tác action đồng loạt",
       "55 booking",
       "- Bước 1: 3 trang, item start-end đúng (1-20, 21-40, 41-55)\n"
       "- Bước 2-4: mọi thao tác đều thành công như ở trang 1",
       note="Nguồn: Quản lý calendar_new r126-r131, r448."),

    tc("Calendar theo list", "UI-001", "Normal",
       "Tab 受付枠一覧: các cột dữ liệu và công thức 予約確定/残数",
       CAL + "\n- Slot 01/10 09:00-11:00 của C1: 定員 5, có 2 booking approve + 1 request cancel",
       "1. Chuyển sang tab「受付枠一覧」\n2. Quan sát dòng slot đó\n"
       "3. Query `calendar_course_receptions` slot này",
       "1 slot 定員 5",
       "- Cột 日時: format「2024.10.01(日) 09:00~11:00」\n- Cột コース: tên course\n"
       "- Cột コース料金: format「¥ 5,000 -」\n"
       "- Cột 予約確定 / 残数 = `total_approve` / (`total_person` − `total_booking`) = 2 / 2 "
       "(vì total_booking = 2 approve + 1 request cancel = 3)\n"
       "- Cột リクエスト = `total_request` + `total_request_cancel`",
       note="Nguồn: Quản lý calendar_new r138-r144. ⚠️ Số chỗ còn lại ĐANG TÍNH CẢ booking đang "
            "request cancel — điểm dễ hiểu nhầm, khớp spec §6.2 nhóm chiếm chỗ {1,2,5}."),

    tc("Calendar theo list", "DATA-001", "Normal",
       "Tab 受付枠一覧: default hiển thị data 1 tháng từ hôm nay, chỉ course ON",
       CAL + "\n- Hôm nay 26/04. Có slot ở 20/04, 30/04, 20/05, 30/05\n- 1 course OFF có slot 30/04",
       "1. Mở tab 受付枠一覧\n2. Quan sát khoảng thời gian hiển thị",
       "4 slot + 1 slot của course OFF",
       "- Chỉ hiện slot 30/04 và 20/05 (trong 26/04 → 26/05)\n"
       "- KHÔNG hiện slot 20/04, 30/05 và slot của course OFF\n"
       "- Sort theo `received_booking_date`, `start_time` ASC",
       note="Nguồn: Quản lý calendar_new r145."),

    tc("Calendar theo list", "FUNC-002", "Normal",
       "Tab 受付枠一覧: tìm kiếm theo course system name + phân trang + thao tác trang 2",
       CAL + "\n- Có 40 slot của 5 course",
       "1. Search theo system name của C2 → kiểm\n2. Search từ khóa không có kết quả\n"
       "3. Chọn item/page, sang trang 2, bấm 詳細 mở modal edit slot",
       "40 slot",
       "- Bước 1: chỉ hiện slot của C2\n- Bước 2: danh sách rỗng\n"
       "- Bước 3: data trang 2 đúng, mở được modal edit slot",
       note="Nguồn: Quản lý calendar_new r148-r153."),

    tc("Calendar theo list", "FUNC-SEQ-001", "Normal",
       "Chuyển đổi qua lại giữa tab 予約 và tab 受付枠",
       CAL,
       "1. Ở tab 予約一覧, bấm「受付枠」\n2. Bấm「予約」quay lại\n3. Lặp 3 lần",
       "—",
       "- Mỗi lần chuyển hiển thị đúng tab tương ứng, dữ liệu không bị trắng, không lỗi JS",
       note="Nguồn: Quản lý calendar_new r137, r158."),

    # ══════════════════ Modal danh sách booking ══════════════════
    tc("Modal danh sách booking", "UI-001", "Normal",
       "Modal danh sách booking theo ngày: footer hiển thị tên course + reception time",
       DATA,
       "1. Từ màn ngày, bấm 詳細を見る trên slot 12:00-13:30 của C1\n2. Quan sát footer modal",
       "1 slot có booking",
       "- Hiển thị tên course đã bấm trước đó\n"
       "- Reception time format「2024.10.01(日) 09:00~10:00」",
       note="Nguồn: Quản lý calendar_new r160."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Kỳ hạn nhận booking: admin KHÔNG setting thời gian dừng nhận → hiện hyperlink 期限なし",
       DATA + "\n- Calendar KHÔNG setting thời gian dừng nhận booking",
       "1. Mở modal danh sách booking theo ngày\n2. Quan sát dòng kỳ hạn nhận booking\n3. Bấm vào text đó",
       "Không setting deadline",
       "- Hiện text hyperlink「期限なし」\n- Bấm: redirect sang màn setting 予約の開始・締切",
       note="Nguồn: Quản lý calendar_new r161. 🔴 MÂU THUẪN tab「Quản lý calendar」r227 mô tả 3 nhánh "
            "khác nhau (期限なし / bỏ trống phần thời gian nhận / …). Xem MT-11."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Kỳ hạn nhận booking: setting kiểu ngày giờ và kiểu giờ phút",
       DATA + "\n- Calendar setting nhận từ 3 ngày trước 09:00, dừng nhận 1 ngày trước 09:00",
       "1. Mở modal danh sách booking\n2. Quan sát dòng kỳ hạn\n"
       "3. Đổi sang setting kiểu 時間指定 (2 giờ 30 phút trước) → mở lại modal\n"
       "4. Bấm vào dòng kỳ hạn",
       "2 kiểu setting deadline",
       "- Bước 2: hiển thị đúng format「2024.09.01(水) 09:00 ~ 2024.09.30(金) 09:00 まで 予約できます」\n"
       "- Bước 3: hiển thị theo kiểu giờ phút\n"
       "- Bước 4: redirect sang màn setting dừng nhận booking",
       note="Nguồn: Quản lý calendar_new r162-r164."),

    tc("Modal danh sách booking", "DATA-COUNT-001", "Normal",
       "Modal danh sách booking: 受付上限 và 予約確定 — 予約確定 KHÔNG đếm request cancel",
       DATA + "\n- Slot 定員 5, có 2 booking approve + 1 booking request cancel",
       "1. Mở modal danh sách booking của slot\n2. Quan sát 2 con số ở header",
       "定員 5, 2 approve, 1 request cancel",
       "-「受付上限 5人」\n-「予約確定 2人」— CHỈ đếm status approve, KHÔNG đếm request cancel",
       note="Nguồn: Quản lý calendar_new r165. Lưu ý khác với công thức 残数 ở tab 受付枠一覧."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Modal danh sách booking: 6 icon status booking",
       DATA + "\n- Slot có đủ 6 loại booking: approve mới, đang chờ approve, admin book, cancel, "
              "đợi nhận thông báo, bị deny",
       "1. Mở modal danh sách booking\n2. Quan sát nhãn từng dòng",
       "6 booking đủ status",
       "- Booking mới được approve:「予約確定」\n- Đang đợi approve:「リクエスト」\n"
       "- Do admin book:「予約確定」+ icon setting\n- Đã cancel:「キャンセル」\n"
       "- Đợi nhận thông báo:「通知受取希望」\n- Bị deny: hiện nhãn deny",
       note="Nguồn: Quản lý calendar_new r167. ⚠️ TC gốc ghi「Booking bị deny: chưa có icon」— "
            "cần xác nhận nhãn hiển thị. Spec §6.1 ghi nhãn 否認済."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Modal danh sách booking: avatar/line name/system name — 3 kiểu người đặt",
       DATA + "\n- Có 3 booking: user tự book, admin book cho friend trong hệ thống, "
              "admin book cho khách ngoài hệ thống",
       "1. Mở modal danh sách booking\n2. Quan sát cột tên của 3 dòng",
       "3 kiểu người đặt",
       "- User tự book: hiện avatar + LINE name + system name\n"
       "- Admin book friend trong hệ thống: hiện avatar + LINE name + system name\n"
       "- Admin book khách ngoài hệ thống: KHÔNG có LINE name, chỉ có tên admin nhập",
       note="Nguồn: Quản lý calendar_new r169. ⚠️ Tab「Quản lý calendar」r235 chỉ liệt kê 2 case "
            "(user book / admin book) — bản _new chi tiết hơn, đã lấy theo _new."),

    tc("Modal danh sách booking", "LIST-001", "Normal",
       "Modal danh sách booking: sort theo status tăng/giảm dần",
       DATA + "\n- Slot có 5 booking đủ status khác nhau",
       "1. Bấm sort cột status tăng dần\n2. Bấm sort giảm dần",
       "5 booking",
       "- Sort theo id status trong bảng `calendar_course_bookings` (0→7 khi tăng dần, "
       "7→0 khi giảm dần), không phải theo thứ tự chữ cái nhãn hiển thị",
       note="Nguồn: Quản lý calendar_new r171-r172, r213-r214."),

    tc("Modal danh sách booking", "FUNC-001", "Normal",
       "Modal danh sách booking: link 予約の全承認制 ⇄ リクエスト制の変更はこちら",
       DATA,
       "1. Mở modal danh sách booking\n2. Bấm link「予約の全承認制 ⇄ リクエスト制の変更はこちら」",
       "—",
       "- Điều hướng sang màn setting message booking (SCR 予約時の各種設定)",
       note="Nguồn: Quản lý calendar_new r188."),

    tc("Modal danh sách booking", "FUNC-001", "Normal",
       "Tab 受付枠編集 trong modal: sửa 定員 và nút 戻る",
       DATA + "\n- Slot 定員 5, có 2 booking approve",
       "1. Trong modal, bấm tab「受付枠編集」\n2. Quan sát ảnh/tên course/thời gian/số 定員 hiện tại\n"
       "3. Sửa 定員 = 10 → Lưu\n4. Sửa 定員 = 1 → Lưu\n5. Bấm nút「戻る」",
       "定員 5 → 10 → 1",
       "- Bước 2: hiện đúng ảnh course, tên course, thời gian, `total_person` = 5\n"
       "- Bước 3: Edit success\n"
       "- Bước 4: báo lỗi vì 1 < số booking approve hiện tại (2)\n"
       "- Bước 5: back về màn danh sách booking",
       note="Nguồn: Quản lý calendar_new r191-r195. So sánh `total_person` với `total_approve` "
            "(KHÔNG đếm booking đang request cancel)."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Màn danh sách slot theo tuần — dạng コース別: thông tin course và 定員",
       CAL + "\n- Khung 09:00 thứ 2 có 2 slot của C1 (定員 5) và C2 (không giới hạn)\n"
             "- C1 có ảnh dọc, C2 không có ảnh",
       "1. Từ màn tuần bấm 詳細を見る\n2. Quan sát dạng コース別",
       "2 slot, 1 có limit 1 không",
       "- Hiện ảnh course (case không ảnh dùng ảnh mặc định; ảnh ngang/dọc/vuông không vỡ khung)\n"
       "- Tên course + time format「2024.10.01(日) 09:00~10:00」\n"
       "- C1 hiện「定員：5人」· C2 hiện「定員：上限なし」",
       note="Nguồn: Quản lý calendar_new r199-r202."),

    tc("Modal danh sách booking", "LIST-001", "Abnormal",
       "Dạng コース別: slot chưa có booking → hiện message rỗng",
       CAL + "\n- Slot 09:00 của C1 chưa có booking",
       "1. Mở danh sách slot dạng コース別\n2. Quan sát vùng booking của C1",
       "Slot rỗng",
       "- Hiện message「まだ予約はありません」",
       note="Nguồn: Quản lý calendar_new r203."),

    tc("Modal danh sách booking", "UI-001", "Normal",
       "Dạng コース別: 5 nhóm status booking và nút 詳細 mở đúng modal",
       CAL + "\n- Slot có booking đủ 5 nhóm: approve, request (booking + cancel), cancel, "
             "đợi nhận thông báo, deny",
       "1. Mở dạng コース別\n2. Quan sát nhãn từng booking\n"
       "3. Bấm 詳細 lần lượt trên từng loại booking",
       "5 nhóm status",
       "- Nhãn:「予約確定」(user approve + admin book) ·「リクエスト」(request booking + request cancel) · "
       "「キャンセル」(user + admin cancel) ·「通知希望」·「否認済」\n"
       "- Bấm 詳細: mở đúng modal detail của từng loại booking",
       note="Nguồn: Quản lý calendar_new r204, r206-r211."),

    tc("Modal danh sách booking", "FUNC-001", "Normal",
       "Dạng 一覧: dữ liệu hiển thị và nút 詳細",
       CAL + "\n- Ngày 01/10 khung 09:00 có 3 course có slot",
       "1. Mở danh sách slot, chuyển sang dạng「一覧」\n2. Quan sát các cột\n"
       "3. Bấm 詳細 của 1 course",
       "3 slot",
       "- Hiện ngày đã click「2024.10.01(日)」· 開催日時 format「09:00~10:00」· cột コース · "
       "cột 予約確定 (chỉ đếm booking approve, KHÔNG đếm request cancel)\n"
       "- Bấm 詳細: mở màn danh sách booking theo course tương ứng",
       note="Nguồn: Quản lý calendar_new r232, r235. ⚠️ TC gốc r233 để câu hỏi mở「Mở danh sách "
            "booking hay mở MH edit slot?」— xem MT-13."),

    tc("Modal danh sách booking", "FUNC-SEQ-001", "Normal",
       "Chuyển đổi qua lại giữa 2 tab コース別 và 一覧, nút 閉じる và icon X",
       CAL,
       "1. Mở danh sách slot theo tuần\n2. Chuyển コース別 → 一覧 → コース別 (3 lần)\n"
       "3. Bấm nút「閉じる」\n4. Mở lại, bấm icon X",
       "—",
       "- Bước 2: mỗi lần chuyển hiển thị đúng dạng tương ứng, không trắng data\n"
       "- Bước 3, 4: đóng màn hình, quay lại lưới tuần",
       note="Nguồn: Quản lý calendar_new r230-r231, r236-r238."),

    tc("Modal danh sách booking", "FUNC-001", "Normal",
       "Modal danh sách booking theo THÁNG: footer, tab 受付枠編集, dữ liệu của từng course",
       CAL + "\n- Ngày 01/10 có 2 course có slot và booking",
       "1. Từ màn tháng bấm 詳細を見る ngày 01/10\n2. Quan sát footer\n"
       "3. Quan sát dữ liệu của từng course\n4. Bấm tab「受付枠編集」→ bấm 詳細 để mở edit slot",
       "2 course có booking",
       "- Footer hiện ngày đã chọn format「2024.10.01(日)」\n"
       "- Mỗi course hiện: tên · ảnh · reception time · kỳ hạn nhận booking · 受付上限 · 予約確定\n"
       "- Tab 受付枠編集 mở được màn edit slot của course tương ứng",
       note="Nguồn: Quản lý calendar_new r239-r266."),
]
