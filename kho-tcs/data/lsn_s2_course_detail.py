# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm コース: tạo/sửa/xóa course + action & filter cấp course.

Nguồn chính: 11.2 TCsLine_LessonCalendar → tab「Quản lý course」r25-r198
  (05/2024 → 02/2026; Bug KH #34561 02/2026 — action/filter không hiển thị khi đổi tab;
   Support #27091 11/2024 — chỉ validate booking tương lai khi xóa course)
Bổ sung: tab「Task nhỏ + fix bug KH」r111-r143 (Bug #30002 — ưu tiên action của course).
Spec: BR-30 (không xóa course khi còn booking tương lai — CHỈ kiểm front-end), BR-31 (snapshot),
      BR-44/BR-P29 (ưu tiên action cấp course), BR-09 (course mới không tự gửi tin cấp course).
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Có 1 lesson calendar「レッスンA」đang ON\n"
       "- Mở /basic/calendar-management/{id} > tab コース設定")
CRS = CAL + "\n- Đã có course「初心者向けトレーニング」(system_name「初心者」, 1h00, 5.000 yên)"

S2 = [
    # ══════════════════ Tạo course ══════════════════
    tc("コース — tạo/sửa/xóa", "FUNC-002", "Abnormal",
       "Popup tạo course: tên course để trống → required",
       CAL,
       "1. Bấm nút「コース作成」→ hiện popup\n2. Để trống ô tên course\n3. Bấm Lưu",
       "Chuỗi rỗng",
       "- Báo lỗi required, KHÔNG tạo bản ghi `calendar_course`",
       note="Nguồn: Quản lý course r27."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Tên course ở popup tạo — biên 50 và 51 ký tự",
       CAL,
       "1. Bấm コース作成\n2. Nhập tên course đúng 50 ký tự tiếng Nhật → Lưu\n"
       "3. Tạo course khác, nhập 51 ký tự → Lưu",
       "50 ký tự / 51 ký tự tiếng Nhật",
       "- 50 ký tự: Save success, mở màn detail course với đủ 50 ký tự\n"
       "- 51 ký tự: KHÔNG cho phép nhập ký tự thứ 51 (ô nhập chặn)",
       note="Nguồn: Quản lý course r28-r29. Đã confirm: tên này là course name HIỂN THỊ BÊN BOOKING, "
            "max 50 ký tự. ⚠️ Xem MT-04 (popup wizard tạo đầu chỉ cho 30)."),

    tc("コース — tạo/sửa/xóa", "DATA-TEXT-001", "Normal",
       "Tên course nhập tiếng Nhật → lưu và hiển thị lại đúng",
       CAL,
       "1. Nhập tên course「まことボット智恵助」(hiragana + katakana + kanji)\n2. Lưu\n3. Mở lại màn detail",
       "「まことボット智恵助」",
       "- Save success, màn detail và màn list hiện đúng chuỗi, không mojibake",
       note="Nguồn: Quản lý course r30."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Lưu course mới → chuyển sang màn detail course",
       CAL,
       "1. Nhập tên course hợp lệ\n2. Bấm Lưu",
       "「初心者向けトレーニング」",
       "- Lưu thành công và chuyển sang màn hình detail của course vừa tạo\n"
       "- DB `calendar_course` có 1 bản ghi mới, `booking_page_display` = 1",
       note="Nguồn: Quản lý course r31 + spec BR-09."),

    tc("コース — tạo/sửa/xóa", "CONC-001", "Abnormal",
       "Double click nút Lưu ở popup tạo course → chỉ tạo 1 bản ghi",
       CAL,
       "1. Nhập tên course hợp lệ\n2. Double click nhanh (<300ms) nút Lưu\n"
       "3. Query `SELECT COUNT(*) FROM calendar_course WHERE calendar_id = {id} AND course_name = '…'`",
       "Tên course「テストDBL」",
       "- Chỉ có ĐÚNG 1 bản ghi trong `calendar_course`\n- Màn list chỉ hiện 1 course",
       note="Nguồn: Quản lý course r32, r76 (2 chỗ đều test double click save)."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Bấm icon X ở popup tạo course → đóng và không tạo",
       CAL,
       "1. Mở popup tạo course, nhập tên\n2. Bấm icon X",
       "Tên đã nhập",
       "- Đóng popup, back về màn list course\n- KHÔNG tạo bản ghi `calendar_course`",
       note="Nguồn: Quản lý course r33."),

    # ══════════════════ Detail course — tab 基本情報 ══════════════════
    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Tab 基本情報: course name (hiển thị booking) — biên 50/51 và bỏ trống",
       CRS,
       "1. Vào detail course > tab 基本情報\n2. Nhập course name 50 ký tự Nhật → Lưu\n"
       "3. Nhập 51 ký tự → Lưu\n4. Xóa trống → Lưu",
       "50 / 51 / rỗng",
       "- 50 ký tự: Save success\n- 51 ký tự: Invalid\n- Rỗng: Invalid (bắt buộc nhập)",
       note="Nguồn: Quản lý course r36-r38."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Tab 基本情報: system_name (tên hiển thị bên admin) — biên 10/11 ký tự",
       CRS,
       "1. Nhập system_name 10 ký tự tiếng Nhật → Lưu\n2. Nhập 11 ký tự → Lưu",
       "10 / 11 ký tự",
       "- 10 ký tự: Save success\n- 11 ký tự: Invalid",
       note="Nguồn: Quản lý course r39-r40."),

    tc("コース — tạo/sửa/xóa", "FUNC-002", "Abnormal",
       "Tab 基本情報: system_name để trống → hành vi chưa chốt",
       CRS,
       "1. Xóa trống ô system_name\n2. Bấm Lưu\n3. Quan sát màn list course",
       "Chuỗi rỗng",
       "- Cần xác nhận 1 trong 2: (a) báo lỗi required, HOẶC (b) Save success và tự lấy course name "
       "cắt 10 ký tự đầu làm system_name\n- KHÔNG được vừa lưu vừa báo lỗi",
       spec="Đã hỏi leader",
       note="🔴 Nguồn: Quản lý course r41 — kết quả mong đợi GHI 2 Ý TRÁI NGƯỢC trong cùng 1 ô: "
            "「Save success và lấy course name cắt 10 ký tự」+「báo lỗi - required nhập」. Xem MT-08."),

    tc("コース — tạo/sửa/xóa", "MEDIA-IMG-001", "Normal",
       "Upload ảnh course: không set ảnh / ảnh sai kích thước / ảnh đúng 1000x700 đều Add success",
       CRS,
       "1. Không upload ảnh → Lưu\n2. Upload ảnh 800x600 → Lưu\n3. Upload ảnh 1000x700 → Lưu",
       "3 trường hợp ảnh",
       "- Cả 3 trường hợp đều Add success (hệ thống KHÔNG bắt buộc kích thước 1000x700)\n"
       "- Ảnh hiển thị đúng ở màn list course và ở màn chọn course phía LINE user",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r42-r44 (3 dòng cùng kết quả Add success → gộp 1 TC, liệt kê đủ "
            "3 input ở cột Các bước). RULE-08: media test PRODUCTION."),

    tc("コース — tạo/sửa/xóa", "MEDIA-001", "Boundary",
       "Upload ảnh course > 10MB → báo lỗi giới hạn dung lượng",
       CRS,
       "1. Chọn file ảnh jpg dung lượng 11MB\n2. Bấm upload",
       "File ảnh 11MB",
       "- Báo lỗi「ファイルサイズが制限（10MB）を超えています」\n- KHÔNG upload lên server",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r45."),

    tc("コース — tạo/sửa/xóa", "MEDIA-001", "Abnormal",
       "Upload file sai định dạng (không phải ảnh / ảnh avif) → báo lỗi format",
       CRS,
       "1. Upload file .txt\n2. Upload file ảnh định dạng .avif",
       "file.txt · image.avif",
       "- Cả 2 trường hợp: báo lỗi「ファイルの形式が正しくありません。」\n- KHÔNG upload",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r47."),

    tc("コース — tạo/sửa/xóa", "MEDIA-001", "Normal",
       "Upload ảnh jpg / png / gif / jpeg → thành công",
       CRS,
       "1. Upload lần lượt 4 file: a.jpg, b.png, c.gif, d.jpeg",
       "4 định dạng ảnh hợp lệ",
       "- Cả 4 định dạng đều upload success, ảnh hiển thị đúng ở màn list course và LINE user",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r48 (4 input cùng 1 kết quả → gộp 1 TC)."),

    tc("コース — tạo/sửa/xóa", "MEDIA-IMG-001", "Normal",
       "Upload ảnh có tên file chứa tiếng Nhật / khoảng trắng",
       CRS,
       "1. Upload file tên「レッスン 画像.png」\n2. Kiểm ảnh hiển thị ở màn list và LINE user",
       "Tên file có ký tự Nhật + space",
       "- Upload success, ảnh hiển thị đúng (không vỡ ảnh, không 404)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Quản lý course r46 — TC gốc CHỈ CÓ TIÊU ĐỀ, kết quả mong đợi do AI bổ sung. "
            "Cần Leader xác nhận."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Thời lượng course — biên 0h00 (invalid), 0h05, 1h00, 23h55",
       CRS,
       "1. Chọn 0 giờ 00 phút → Lưu\n2. Chọn 0 giờ 05 phút → Lưu\n"
       "3. Chọn 1 giờ 00 phút → Lưu\n4. Chọn 23 giờ 55 phút → Lưu",
       "0h00 / 0h05 / 1h00 / 23h55",
       "- 0h00: Invalid, báo lỗi「所要時間は5分以上に設定してください。」\n"
       "- 0h05 / 1h00 / 23h55: đều Save success\n"
       "- Sau khi lưu 23h55: màn list course hiện「23時間55分」",
       note="Nguồn: Quản lý course r54-r57. Đây là 2 nhóm kết quả khác nhau nên gộp thành 1 TC "
            "boundary có cả biên trong và biên ngoài (RULE-01)."),

    tc("コース — tạo/sửa/xóa", "UI-INPUT-001", "Abnormal",
       "Thời lượng course: chỉ cho chọn trong select, không nhập tay",
       CRS,
       "1. Thử gõ trực tiếp vào ô giờ/phút\n2. Quan sát",
       "Gõ tay「99」",
       "- Không nhập được, chỉ chọn được giá trị trong danh sách select",
       note="Nguồn: Quản lý course r53."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Số tiền course không nhập → save success, hiển thị 設定なし ở list, 0 yên bên user",
       CRS,
       "1. Xóa trống ô số tiền → Lưu\n2. Quan sát màn list course\n"
       "3. LINE user mở màn chọn course",
       "Số tiền rỗng",
       "- Save success\n- Màn list course: cột 料金 hiện「設定なし」\n"
       "- Phía LINE user: hiển thị 0 yên (hoặc ẩn giá theo setting 表示設定)",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r58 (verify 3 tầng: lưu + màn list + màn LINE user — RULE-07)."),

    tc("コース — tạo/sửa/xóa", "UI-INPUT-001", "Normal",
       "Số tiền course: nhập số nguyên → format dấu phẩy",
       CRS,
       "1. Nhập 5000 vào ô số tiền\n2. Blur khỏi ô",
       "5000",
       "- Hiển thị「5,000」",
       note="Nguồn: Quản lý course r59."),

    tc("コース — tạo/sửa/xóa", "FUNC-003", "Abnormal",
       "Số tiền course: không phải số / số âm / số thực → Invalid",
       CRS,
       "1. Nhập「abc」→ Lưu\n2. Nhập「-100」→ Lưu\n3. Nhập「1000.5」→ Lưu",
       "abc · -100 · 1000.5",
       "- Cả 3 giá trị đều Invalid, không lưu",
       note="Nguồn: Quản lý course r60 (3 input cùng 1 kết quả → gộp 1 TC)."),

    tc("コース — tạo/sửa/xóa", "PAY-LIMIT-001", "Normal",
       "Bot free: hiện cảnh báo cần upgrade để dùng thanh toán, link tới màn upgrade",
       "- Bot B gói **free**, có 1 lesson calendar và 1 course\n- Đang ở màn detail course",
       "1. Quan sát vùng số tiền course\n2. Bấm link「アップグレード」",
       "Bot free",
       "- Hiện text cảnh báo「決済機能の利用は、有料プランにアップグレードする必要があります。」\n"
       "- Bấm アップグレード: redirect sang /admin/bot-add?upgrade_bot_id={id bot đã mã hóa}",
       note="Nguồn: Quản lý course r61."),

    tc("コース — tạo/sửa/xóa", "PAY-LIMIT-001", "Normal",
       "Bot khác free: KHÔNG hiện cảnh báo upgrade ở màn detail course",
       "- Bot A gói standard, có 1 course\n- Đang ở màn detail course",
       "1. Quan sát vùng số tiền course",
       "Bot standard",
       "- KHÔNG hiện text「決済機能の利用は、有料プランに…」",
       note="Nguồn: Quản lý course r62 — TC gốc chỉ có tiêu đề, expected do AI viết lại thành "
            "câu đo được (đối chứng âm của r61)."),

    tc("コース — tạo/sửa/xóa", "FUNC-004", "Boundary",
       "Mô tả course (explain) — không nhập / 1000 / 1001 ký tự",
       CRS,
       "1. Để trống ô mô tả → Lưu\n2. Nhập 1000 ký tự tiếng Nhật → Lưu\n3. Nhập 1001 ký tự → Lưu",
       "rỗng / 1000 / 1001 ký tự",
       "- Rỗng: Save success\n- 1000 ký tự: Save success\n- 1001 ký tự: Invalid",
       note="Nguồn: Quản lý course r63-r65."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Nút 戻る ở màn detail course → back về màn list course",
       CRS,
       "1. Vào detail course\n2. Bấm nút「戻る」",
       "—",
       "- Quay về màn list course (tab コース設定)",
       note="Nguồn: Quản lý course r83."),

    # ══════════════════ Xóa course ══════════════════
    tc("コース — tạo/sửa/xóa", "STATE-DEP-001", "Abnormal",
       "Xóa course khi còn booking 予約確定 hoặc リクエスト → chặn kèm alert",
       CRS + "\n- Course C1 có 1 booking status 予約確定 và 1 booking status リクエスト (đều ở TƯƠNG LAI)",
       "1. Vào detail course C1\n2. Bấm「このコースを削除する」",
       "Booking status = 1 (approve) và 0 (request)",
       "- Hiện alert「「ステータス：予約確定、リクエスト」の予約が残っています。このコースを削除する場合、"
       "このコースを予約しているすべての予約が「ステータス：キャンセル」になっている必要があります。」\n"
       "- KHÔNG xóa course, `calendar_course` giữ nguyên bản ghi",
       note="Nguồn: Quản lý course r77. ⚠️ Spec BR-30: rule này CHỈ kiểm ở FRONT-END, server không "
            "kiểm lại ⇒ xem TC Đồng thời & verify API."),

    tc("コース — tạo/sửa/xóa", "STATE-DEP-001", "Normal",
       "Xóa course khi toàn bộ booking đã cancel → xóa được",
       CRS + "\n- Toàn bộ booking của C1 ở status 4 (user cancel) hoặc 7 (admin cancel)",
       "1. Bấm「このコースを削除する」\n2. Xác nhận trên popup\n"
       "3. Query `calendar_course` và mở màn 削除済み予約",
       "Booking status ∈ {4, 7}",
       "- Hiện popup confirm「コースの削除」→ xác nhận thì xóa\n"
       "- Redirect về màn list course, C1 biến mất\n"
       "- DB: bản ghi `calendar_course` của C1 bị xóa\n"
       "- Các booking của C1 xuất hiện ở màn「削除済み予約」",
       note="Nguồn: Quản lý course r78, r80, r82 (verify 3 tầng: UI + DB + màn booking đã xóa)."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Xóa course chưa có booking nào → hiện popup confirm rồi xóa",
       CRS + "\n- Course C2 chưa có booking nào",
       "1. Bấm「このコースを削除する」\n2. Quan sát popup confirm",
       "Course không booking",
       "- Hiện popup confirm「コースの削除」kèm 管理名 (system_name) của course tương ứng\n"
       "- Có alert「コースを削除した場合、このコースが関連する予約はすべて「削除済み予約」に表示されます。」",
       note="Nguồn: Quản lý course r79-r80."),

    tc("コース — tạo/sửa/xóa", "FUNC-001", "Normal",
       "Popup confirm xóa course: nút 戻る và X → đóng, không xóa",
       CRS,
       "1. Mở popup confirm xóa\n2. Bấm 戻る\n3. Mở lại popup, bấm icon X",
       "—",
       "- Cả 2 lần đều đóng popup và KHÔNG xóa course\n- `calendar_course` giữ nguyên",
       note="Nguồn: Quản lý course r81."),

    tc("コース — tạo/sửa/xóa", "DATA-001", "Normal",
       "Support #27091: chỉ chặn xóa course khi còn booking TƯƠNG LAI",
       CRS + "\n- Course C1 có 1 booking 予約確定 ở NGÀY QUÁ KHỨ và không có booking tương lai",
       "1. Bấm「このコースを削除する」",
       "Booking approve ở quá khứ",
       "- Cho phép xóa course (không hiện alert chặn)\n- Booking cũ chuyển vào màn 削除済み予約",
       note="Nguồn: Quản lý course r181, r184, r189. ⚠️ MÂU THUẪN với r77 (nói kể cả booking đã qua "
            "time nhưng vẫn status 予約確定 thì VẪN KHÔNG cho xóa — 'đã confirm a Tư'). Xem MT-09."),

    tc("コース — tạo/sửa/xóa", "DATA-001", "Abnormal",
       "Support #27091 — ma trận trạng thái booking tương lai chặn xóa course",
       CRS + "\n- Chuẩn bị 6 course riêng, mỗi course có đúng 1 booking TƯƠNG LAI ở 1 trạng thái",
       "Với từng course, bấm「このコースを削除する」và ghi kết quả:\n"
       "1. Booking 予約確定 do admin book (status 2)\n2. Booking 予約確定 do user book (status 1)\n"
       "3. Booking đang リクエスト của user (status 0)\n4. Booking đang request cancel (status 5)\n"
       "5. Booking đã cancel của admin (status 7)\n6. Booking đã cancel của user (status 4)",
       "6 trạng thái booking tương lai",
       "- Case 1, 2, 3, 4: BÁO LỖI, không xóa được course\n"
       "- Case 5, 6: XÓA ĐƯỢC course",
       note="Nguồn: Quản lý course r182-r197 (ma trận, mỗi trạng thái 1 kết quả). Gộp 1 TC vì cùng "
            "1 chuỗi thao tác lặp; đủ 6 điểm ở cột Các bước. Giữ khối này vì phủ đủ 6 status."),

    tc("コース — tạo/sửa/xóa", "STATE-CLEAN-001", "Normal",
       "Xóa course → snapshot tên/giá/ảnh vào mọi booking cũ",
       CRS + "\n- Course C1 tên「初心者向けトレーニング」giá 5.000 yên, đã có 2 booking cancel "
             "(1 booking chưa xóa, 1 booking đã xóa mềm)",
       "1. Xóa course C1\n2. Mở màn 削除済み予約 xem 2 booking\n"
       "3. Query `calendar_course_bookings` 2 bản ghi này",
       "2 booking của course sắp xóa",
       "- Sau khi xóa course, cả 2 booking VẪN hiển thị đúng tên course「初心者向けトレーニング」, "
       "số tiền 5.000 yên và ảnh course (không rỗng, không hiện ID)\n"
       "- DB: cột `course_name` / `course_amount` / `system_name` / `course_image` của cả 2 booking "
       "đã được ghi giá trị snapshot",
       spec="Spec không ghi",
       note="Suy luận của AI theo spec BR-31 (snapshot áp dụng cho CẢ booking đã soft-delete) — "
            "corpus KHÔNG có TC nào kiểm snapshot. Cần Leader xác nhận."),

    # ══════════════════ Action & filter cấp course ══════════════════
    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Tab アクション・詳細設定: chưa setting action → hiện text rỗng",
       CRS,
       "1. Vào detail course > tab アクション・詳細設定\n2. Quan sát khối 予約完了時 và 予約リクエスト承認時",
       "Course chưa setting action",
       "- Cả 2 khối đều hiện text「エルメアクションが登録されていません」",
       note="Nguồn: Quản lý course r84, r118."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Insert mẫu 例文を挿入する ở tab 予約完了時 → fill đúng nội dung mẫu",
       CRS,
       "1. Vào tab アクション・詳細設定 > 予約完了時\n2. Bấm「例文を挿入する」\n3. Quan sát ô nội dung",
       "—",
       "- Ô nội dung được fill mẫu bắt đầu bằng「[name]様」và chứa đủ 4 mục: 予約日時 · ご予約コース名 · "
       "コース料金 · 変更・キャンセル用 URL",
       note="Nguồn: Quản lý course r90 (nội dung mẫu tại https://x.gd/4d4Al)."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Insert mẫu ở tab 予約リクエスト承認時 → nội dung mẫu KHÁC tab 予約完了時",
       CRS,
       "1. Vào tab 予約リクエスト承認時\n2. Bấm「例文を挿入する」",
       "—",
       "- Nội dung mẫu chứa câu「下記の通り、予約リクエストを承認いたしました。」\n"
       "- KHÁC với mẫu của tab 予約完了時 (「予約が完了いたしました。」)",
       note="Nguồn: Quản lý course r124 (2 mẫu khác nhau → 2 TC riêng theo quy tắc tách TC)."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Insert LINE名 / thông tin booking / friend info vào message của course",
       CRS + "\n- Bot có friend info kiểu text, date, point, select, image, pdf\n"
             "- LINE user U1 đã có giá trị cho các friend info này",
       "1. Ở tab 予約完了時, bấm ＋ LINE名\n"
       "2. Bấm 予約情報 → chèn lần lượt 予約日時 · コース名 · 料金 · 変更・キャンセル用 URL · 店舗名\n"
       "3. Bấm 友だち情報 → chèn info basic (system name, mail, sđt, ngày sinh, địa chỉ)\n"
       "4. Chèn thêm friend info kiểu text/date/point/select/image/pdf\n"
       "5. Lưu → U1 booking course này",
       "Đủ 5 mã booking + 5 info basic + 6 kiểu friend info",
       "- Bước 1-4: chèn được, GUI save success\n"
       "- Bước 5: U1 nhận tin LINE với TOÀN BỘ mã đã được thay bằng giá trị thật "
       "(tên LINE, ngày giờ booking, tên course, số tiền, URL hủy bấm được, tên cửa hàng, "
       "các friend info của U1); friend info kiểu image hiện dạng link bấm ra ảnh",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r86-r89 (gộp vì cùng 1 chuỗi thao tác liên tiếp + verify ở output "
            "cuối là tin LINE — RULE-06). Chi tiết từng mã xem tab Setting calendar."),

    tc("コース — action & filter riêng", "DATA-REF-001", "Abnormal",
       "Friend info đã chèn bị XÓA → khi send action chỉ mất mã đó, phần còn lại vẫn gửi",
       CRS + "\n- Message của course đã chèn friend info F1 và F2\n- U1 có giá trị cho cả F1, F2",
       "1. Xóa friend info F1 ở màn 友だち情報管理\n2. U1 booking course này\n3. Kiểm tin LINE U1 nhận",
       "1 friend info bị xóa",
       "- U1 VẪN nhận được tin\n- Phần nội dung của F1 KHÔNG được gửi (bỏ trống / bỏ hẳn)\n"
       "- Các mã còn lại (F2, tên, giá) vẫn thay đúng giá trị",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r91."),

    tc("コース — action & filter riêng", "DATA-REF-001", "Normal",
       "Friend info đã chèn bị ĐỔI TÊN → vẫn gửi được nội dung của friend info đó",
       CRS + "\n- Message của course đã chèn friend info F1",
       "1. Đổi tên F1 ở màn 友だち情報管理\n2. U1 booking course\n3. Kiểm tin LINE U1 nhận",
       "1 friend info đổi tên",
       "- U1 nhận tin, giá trị của F1 VẪN được thay đúng (không bị rỗng)",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r92."),

    tc("コース — action & filter riêng", "DATA-REF-001", "Abnormal",
       "FOLDER chứa friend info đã chèn bị XÓA → không gửi phần đó, phần còn lại vẫn gửi",
       CRS + "\n- Message của course đã chèn friend info F1 nằm trong folder FD1, và F2 ở folder khác",
       "1. Xóa folder FD1\n2. U1 booking course\n3. Kiểm tin LINE U1 nhận",
       "1 folder friend info bị xóa",
       "- Nội dung của F1 KHÔNG được gửi\n- F2 và các mã khác vẫn thay đúng giá trị",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r93."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Chọn 利用しない ở message của course → disable ô nhập, không gửi msg text",
       CRS + "\n- Course đã setting message text và có 1 multi action",
       "1. Tích chọn「利用しない」\n2. Quan sát ô nội dung\n3. Lưu → U1 booking course",
       "Course có msg text + multi action",
       "- Ô nội dung bị disable\n- U1 KHÔNG nhận tin text của course\n"
       "- U1 VẪN nhận multi action đã set (nếu có)",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r94, r125. Spec BR-47: cờ is_send_message mang nghĩa ĐẢO."),

    tc("コース — action & filter riêng", "FUNC-004", "Boundary",
       "Message của course — biên 5000 và 5001 ký tự",
       CRS,
       "1. Nhập 5000 ký tự tiếng Nhật vào message của course → Lưu\n2. Nhập 5001 ký tự → Lưu",
       "5000 / 5001 ký tự",
       "- 5000 ký tự: Save success\n- 5001 ký tự: Invalid",
       note="Nguồn: Quản lý course r95-r96, r126-r127."),

    tc("コース — action & filter riêng", "FUNC-004", "Abnormal",
       "Message < 5000 ký tự nhưng sau khi thay mã vượt 5000 → gửi lỗi, hiện ở màn error msg",
       CRS + "\n- U1 có friend info giá trị rất dài (~1000 ký tự)\n"
             "- Message course dài 4800 ký tự + chèn friend info của U1",
       "1. Lưu message (GUI cho lưu)\n2. U1 booking course\n"
       "3. Kiểm tin LINE của U1\n4. Mở màn hình エラーメッセージ của tool",
       "Message sau thay mã ≈ 5800 ký tự",
       "- Bước 1: GUI vẫn save success\n"
       "- Bước 3: U1 KHÔNG nhận được tin\n"
       "- Bước 4: màn error message ghi nhận lỗi gửi tin của booking này",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r97, r128 (verify 3 tầng: GUI + LINE app + màn error — RULE-07)."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Modal action của course: add / edit / xóa action → lưu vào DB ngay khi bấm Save ở MODAL",
       CRS,
       "1. Bấm「アクション登録・編集」→ mở modal action\n2. Add 1 action mới → bấm Save ở MODAL "
       "(CHƯA bấm Save của course)\n3. Query `t_actions_detail`\n"
       "4. Edit action đó → Save modal → query lại\n5. Xóa action → Save modal → query lại",
       "1 action gắn course",
       "- Bước 2-3: action đã có trong DB dù chưa bấm Save course\n"
       "- Bước 4: action được cập nhật trong DB\n- Bước 5: action bị xóa khỏi DB\n"
       "- Màn detail course hiện đúng danh sách action sau mỗi lần thao tác",
       note="Nguồn: Quản lý course r98-r101, r129-r132 (Update 02/2026). Verify DB + GUI — RULE-07."),

    tc("コース — action & filter riêng", "FUNC-SEQ-001", "Normal",
       "Bug KH #34561: đổi tab qua lại sau khi Save modal action → vẫn hiện action đã set",
       CRS,
       "1. Vào detail course, mở modal action, add action + filter, bấm Save ở modal\n"
       "2. CHƯA bấm Save course → chuyển sang tab 基本情報 rồi quay lại tab アクション\n"
       "3. Chuyển qua lại giữa tab 予約完了時 và 予約リクエスト承認時\n"
       "4. Mở lại modal action và modal filter",
       "1 action + 1 filter chưa save course",
       "- Bước 2, 3, 4: luôn hiển thị đúng action và filter vừa set, không bị trắng data",
       note="Nguồn: Quản lý course r66-r67 (Bug KH #34561), r102, r108, r133, r140-r141."),

    tc("コース — action & filter riêng", "FUNC-SEQ-001", "Normal",
       "Bug KH #34561: vào tab action bằng HYPERLINK từ màn edit course → hiện đủ setting cũ",
       CRS + "\n- Course đã setting sẵn message text + multi action + filter ở cả 2 tab",
       "1. Vào màn edit course (tab 基本情報)\n"
       "2. Bấm NGAY hyperlink「予約完了・リクエスト承認時アクションを設定する」\n"
       "3. Quan sát 3 khối: setting message text · setting action · setting filter\n"
       "4. Từ tab action, bấm hyperlink「基本情報を設定する」",
       "Course đã có đủ 3 loại setting",
       "- Bước 2: nhảy sang tab setting action\n"
       "- Bước 3: cả 3 khối đều HIỆN ĐÚNG setting hiện có và EDIT được bình thường\n"
       "- Bước 4: nhảy sang tab 基本情報, hiện đủ ảnh · name · giờ làm việc · số tiền · description",
       note="Nguồn: Quản lý course r68-r71, r136-r137 (Bug KH #34561 bug số 1)."),

    tc("コース — action & filter riêng", "CONC-001", "Abnormal",
       "Double click hyperlink chuyển tab → chỉ nhảy 1 lần, không lỗi",
       CRS,
       "1. Double click nhanh「予約完了・リクエスト承認時アクションを設定する」\n"
       "2. Double click nhanh「基本情報を設定する」",
       "—",
       "- Cả 2 lần đều nhảy đúng tab tương ứng, không mở 2 lần, không văng lỗi JS",
       note="Nguồn: Quản lý course r72, r138."),

    tc("コース — action & filter riêng", "PERM-002", "Normal",
       "Account staff mở tab action/基本情報 của course bằng hyperlink → vẫn thấy data đã setting",
       CRS + "\n- Có account staff S1 được cấp quyền route レッスン予約",
       "1. Đăng nhập staff S1\n2. Vào detail course, bấm hyperlink sang tab action\n"
       "3. Bấm hyperlink sang tab 基本情報",
       "Account staff",
       "- Staff S1 thấy đầy đủ setting action / filter / message như admin chính, không bị trắng data",
       note="Nguồn: Quản lý course r73, r139 — TC gốc chỉ có tiêu đề, expected do AI viết lại "
            "thành câu đo được. Cần Leader xác nhận."),

    tc("コース — action & filter riêng", "FUNC-001", "Normal",
       "Modal filter của course: dùng CHUNG cho 2 tab 予約完了時 và 予約リクエスト承認時",
       CRS,
       "1. Ở tab 予約完了時, mở modal filter, set filter theo 1 tag → Save modal\n"
       "2. Chuyển sang tab 予約リクエスト承認時\n3. Mở modal filter",
       "1 filter theo tag T1",
       "- Bước 2-3: filter ở tab 予約リクエスト承認時 GIỮ NGUYÊN đúng filter vừa set (dùng chung)",
       note="Nguồn: Quản lý course r103, r115."),

    tc("コース — action & filter riêng", "FUNC-002", "Normal",
       "Filter コースの絞り込み表示 theo tag → chỉ user thỏa filter mới thấy course",
       CRS + "\n- Tag T1 gắn cho U1, không gắn cho U2\n- Cả U1 và U2 đều là bạn của bot A",
       "1. Set filter AND: có tag T1 → Save\n2. U1 mở trang booking\n3. U2 mở trang booking",
       "Filter AND 1 tag",
       "- Save success\n- U1 THẤY course trong danh sách chọn course\n- U2 KHÔNG thấy course",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r109 (verify tới output cuối = màn LINE user — RULE-06). "
            "Spec BR-P03: course chỉ hiện khi booking_page_display=1 VÀ thoả FilterV2."),

    tc("コース — action & filter riêng", "FUNC-002", "Normal",
       "Filter OR / AND-OR nhiều tag → user thỏa mãn mới thấy course",
       CRS + "\n- Tag T1 gắn U1 · Tag T2 gắn U2 · U3 không có tag nào",
       "1. Set filter OR: có T1 HOẶC T2 → Save\n2. U1, U2, U3 lần lượt mở trang booking\n"
       "3. Đổi sang filter kết hợp AND-OR nhiều tag, lặp lại",
       "Filter OR 2 tag",
       "- U1 và U2 THẤY course; U3 KHÔNG thấy",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Quản lý course r110-r114 — TC gốc CHỈ CÓ TIÊU ĐỀ (5 dòng chọn 1 tag / nhiều tag "
            "AND, OR, AND-OR), kết quả mong đợi do AI bổ sung theo mẫu r109. Cần Leader xác nhận."),

    tc("コース — action & filter riêng", "DATA-COUNT-001", "Normal",
       "Bộ đếm 対象人数 của filter course — case không filter và có filter",
       CRS + "\n- Bot A có 100 friend, trong đó 10 friend bị block/hide/bị block\n"
             "- Tag T1 gắn cho 20 friend",
       "1. Không set filter → quan sát số hiển thị\n"
       "2. Set filter「có tag T1」→ quan sát số hiển thị\n3. Bấm vào con số → xem list friend",
       "100 friend · 20 friend có T1",
       "- Bước 1: hiện「XX人（友だち全員）」— XX là tổng friend hợp lệ, cần chốt có trừ friend "
       "block/hide hay không\n"
       "- Bước 2: hiện「20人」\n"
       "- Bước 3: list friend hiện đúng 20 friend có tag T1",
       spec="Đã hỏi leader",
       note="Nguồn: Quản lý course r116-r117, r134. ⚠️ TC gốc r116 để dấu hỏi「(trừ friend đã "
            "block/ hide/ bị block?)」— chưa chốt công thức đếm. Xem MT-10."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Filter course chỉ send multi action cho user thỏa filter",
       CRS + "\n- Course có multi action + filter「có tag T1」\n- U1 có T1, U2 không có",
       "1. Cho U1 và U2 cùng booking course này (admin book hộ để bỏ qua filter hiển thị)\n"
       "2. Kiểm LINE app của U1 và U2",
       "2 user, 1 có tag 1 không",
       "- U1 nhận được multi action của course\n- U2 KHÔNG nhận multi action",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r135."),

    # ══════════════════ Ưu tiên action course vs booking (Bug #30002) ══════════════════
    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Ưu tiên action: course CÓ message text → luôn gửi theo action của course (6 tổ hợp)",
       CRS + "\n- Calendar setting 予約を全承認 (approve luôn)\n"
             "- Setting action chung của calendar: có message text riêng\n"
             "- Course C1 bật message text riêng",
       "Lặp 6 tổ hợp, mỗi tổ hợp booking 1 lần rồi kiểm tin LINE user nhận được:\n"
       "1. LINE user book — course có msg text, KHÔNG set multi action (id trong DB = NULL)\n"
       "2. LINE user book — course có msg text, có multi action CÓ action detail\n"
       "3. LINE user book — course có msg text, có multi action KHÔNG có action detail\n"
       "4. Admin book ở web — 3 tổ hợp tương tự",
       "6 tổ hợp",
       "- Cả 6 tổ hợp: user nhận MESSAGE TEXT CỦA COURSE (không phải của calendar) và multi action "
       "của course nếu có",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r112-r114, r118-r120 (Bug #30002 05/2025). Spec BR-44."),

    tc("コース — action & filter riêng", "MSG-002", "Abnormal",
       "Ưu tiên action: course KHÔNG có message text + multi action KHÔNG có action detail → "
       "gửi action CHUNG của calendar",
       CRS + "\n- Calendar setting approve luôn, có action chung\n"
             "- Course C1 KHÔNG bật message text; có multi action nhưng action đó KHÔNG có action detail "
             "(tái hiện: add action course → vào edit action bấm xóa action ở modal → Save modal, "
             "KHÔNG bấm Save course)",
       "1. LINE user U1 booking course C1\n2. Kiểm tin LINE U1 nhận\n"
       "3. Lặp lại với admin book ở web và admin book ở app",
       "Course có multi action rỗng detail",
       "- Cả 3 lối đặt: U1 nhận ACTION CHUNG của calendar (không bị mất action)\n"
       "- Trước khi fix Bug #30002: user KHÔNG nhận gì — nếu tái hiện thì raise bug",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r117, r123, r129 (Bug #30002 — nguyên nhân gốc)."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Ưu tiên action: course KHÔNG có msg text + multi action CÓ detail → gửi action của course",
       CRS + "\n- Course C1 không bật msg text, có multi action hợp lệ",
       "1. LINE user book\n2. Admin book ở web\n3. Admin book ở app\n4. Kiểm tin LINE user nhận",
       "3 lối đặt",
       "- Cả 3 lối: user nhận MULTI ACTION CỦA COURSE (không nhận msg text của calendar)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r116, r122, r128."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Ưu tiên action khi ADMIN APPROVE booking — 6 tổ hợp × approve 1 và approve nhiều",
       CRS + "\n- Calendar setting リクエスト制 (cần admin approve)\n"
             "- Đã có 3 booking đang chờ approve của course C1",
       "1. Approve 1 booking — lặp 6 tổ hợp (course có/không msg text × multi action NULL / "
       "có detail / không detail)\n"
       "2. Approve cùng lúc 3 booking — lặp 6 tổ hợp tương tự\n"
       "3. Kiểm tin LINE của từng user sau mỗi lần",
       "6 tổ hợp × 2 kiểu approve",
       "- Course CÓ msg text: mọi tổ hợp đều gửi action của course\n"
       "- Course KHÔNG msg text + multi action NULL hoặc không có detail: gửi action CHUNG\n"
       "- Course KHÔNG msg text + multi action có detail: gửi action của course\n"
       "- Approve hàng loạt cho kết quả GIỐNG approve từng cái",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r132-r143."),

    tc("コース — action & filter riêng", "MSG-002", "Normal",
       "Ưu tiên action khi booking CÓ bill tiền — giống case không bill",
       CRS + "\n- Calendar enable bill tiền, course C1 có giá 5.000 yên, có action riêng",
       "1. U1 booking, thanh toán thành công ngay\n2. Kiểm tin U1 nhận\n"
       "3. Tạo 1 booking khác, để job quét kết quả bill trả về success\n4. Kiểm tin",
       "Booking có bill tiền",
       "- Cả 2 case: U1 nhận đúng action của course, giống hệt case booking không bill tiền",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r130-r131."),

    tc("コース — action & filter riêng", "MSG-002", "Abnormal",
       "Ma trận ưu tiên action booking vs course (4 tổ hợp)",
       CRS + "\n- Calendar (booking chung) có setting action A_bk\n- Course C1 có setting action A_cs",
       "Chuẩn bị 4 tổ hợp rồi cho user booking, kiểm tin LINE mỗi lần:\n"
       "1. Booking KHÔNG action + course CÓ action\n2. Booking CÓ action + course CÓ action\n"
       "3. Booking CÓ action + course KHÔNG action\n4. Booking KHÔNG action + course KHÔNG action",
       "4 tổ hợp",
       "- Case 1: user nhận A_cs\n- Case 2: user nhận A_cs (course đè booking)\n"
       "- Case 3: user nhận A_bk\n- Case 4: user KHÔNG nhận action nào",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r172-r175 — TC gốc CHỈ CÓ TIÊU ĐỀ; kết quả mong đợi lấy từ chính "
            "tiêu đề (「=> Send action của course」…) và spec BR-44. Áp dụng tương tự cho tab "
            "「Action khi request booking được approve」(r176-r179)."),

    tc("コース — action & filter riêng", "SEC-001", "Abnormal",
       "Test security: từ bot B paste link detail course của bot A",
       "- Admin có 2 bot A và B\n- Bot A có course id = 1 trong calendar id = 1",
       "1. Đăng nhập admin, đang chọn bot B\n"
       "2. Paste URL https://step.lme.jp/basic/calendar-management/1/edit-course/1",
       "URL detail course của bot A",
       "- Redirect ra màn hình list calendar của bot B\n- KHÔNG hiển thị data course của bot A",
       env="PRODUCTION",
       note="Nguồn: Quản lý course r180. ⚠️ Spec A-06: middleware CHỈ kiểm {id} calendar, KHÔNG kiểm "
            "courseId ⇒ TC này chỉ phủ nhánh calendar-id sai. Xem TC IDOR ở nhóm Đồng thời & verify API."),

    tc("コース — tạo/sửa/xóa", "FUNC-002", "Normal",
       "Edit course: đổi ảnh sai định dạng → báo lỗi; đổi thời lượng không hợp lệ → báo lỗi",
       CRS + "\n- Course C1 đã có ảnh và thời lượng 1h00",
       "1. Vào edit C1, đổi ảnh sang file .txt → Lưu\n"
       "2. Đổi thời lượng về 0 giờ 00 phút → Lưu",
       "file.txt · 0h00",
       "- Bước 1: báo lỗi「ファイルの形式が正しくありません。」, ảnh cũ giữ nguyên\n"
       "- Bước 2: báo lỗi「所要時間は5分以上に設定してください。」, thời lượng cũ giữ nguyên",
       note="Nguồn: Quản lý course r152, r154."),

    tc("コース — tạo/sửa/xóa", "FUNC-SEQ-001", "Normal",
       "Edit course: vào edit rồi Lưu mà không đổi gì → data giữ nguyên",
       CRS,
       "1. Vào detail course C1\n2. Không sửa gì, bấm Lưu\n3. Reload và so sánh toàn bộ trường",
       "Course C1 đầy đủ data",
       "- Toàn bộ trường (tên, system_name, ảnh, thời lượng, giá, mô tả, action, filter) giữ nguyên "
       "giá trị cũ, không bị reset về mặc định",
       spec="Spec không ghi",
       note="Nguồn: Quản lý course r146 — TC gốc chỉ có tiêu đề, expected do AI bổ sung. "
            "Cần Leader xác nhận."),
]
