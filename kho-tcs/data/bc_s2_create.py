# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 7-12: tạo broadcast bước 1 (tiêu đề, thời gian gửi,
nhiều lịch, lưu & điều hướng) và đăng ký tin nhắn bước 2 (メッセージ登録,
テンプレートから追加, エルメアクション).
"""
from _common import tc

A = ("- Đăng nhập Admin của 1 bot đã liên kết LOA, bot có ≥10 bạn bè\n"
     "- Vào /basic/message-send-all → bấm「新規作成」(màn SCR-BC-02)")
B2 = ("- Đã tạo broadcast bước 1 thành công, đang ở màn SCR-BC-04 "
      "(/basic/add-broadcast-v2?broadcast_id=XXX)")

S2 = [
    # ═══════════ 7. 管理用タイトル & validate ═══════════
    tc("管理用タイトル & validate", "UI-FIELD-001", "Normal",
       "Trường 管理用タイトル mặc định trống và là trường bắt buộc",
       A,
       "1. Bấm「新規作成」\n"
       "2. Quan sát trường「管理用タイトル」khi chưa nhập gì",
       "—",
       "- Trường trống\n"
       "- Có dấu hiệu bắt buộc (ký hiệu 必須 hoặc dấu sao) theo design",
       note="Nguồn: r64, r406."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Normal",
       "Nhập 管理用タイトル từ 1 đến 20 ký tự — lưu thành công",
       A,
       "1. Nhập「配信」(2 ký tự) vào 管理用タイトル\n"
       "2. Chọn gửi ngay, để đối tượng mặc định すべての友だち\n"
       "3. Bấm「配信内容を確認して送信に進む」\n"
       "4. Lặp lại với chuỗi đúng 20 ký tự",
       "「配」(1 ký tự) · 「配信」(2) · 「あいうえおかきくけこさしすせそたちつて」(20 ký tự full-width)",
       "- Cả 3 giá trị đều lưu thành công, không hiện validate\n"
       "- Tên hiển thị đúng nguyên văn ở màn list (không bị cắt trong DB)",
       note="Nguồn: r65, r407. Gộp 3 độ dài vì CÙNG 1 kết quả (lưu OK) — RULE tách TC chỉ áp khi "
            "kết quả mong đợi khác nhau."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Abnormal",
       "Không nhập 管理用タイトル — hiện validate, không lưu",
       A,
       "1. Để trống「管理用タイトル」\n"
       "2. Điền các trường còn lại hợp lệ\n"
       "3. Bấm「配信内容を確認して送信に進む」",
       "管理用タイトル = trống",
       "- Hiện thông báo validate「管理用タイトルを入力してください」\n"
       "- KHÔNG tạo bản ghi broadcast mới (đếm số bản ghi ở tab 下書き không tăng)",
       note="Nguồn: r61, r66, r408 + file 03/tab function r204."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Abnormal",
       "Nhập chỉ toàn khoảng trắng vào 管理用タイトル — bị coi là trống",
       A,
       "1. Nhập 5 dấu cách vào「管理用タイトル」\n"
       "2. Điền các trường còn lại hợp lệ\n"
       "3. Bấm lưu",
       "「     」(5 space)",
       "- Hiện thông báo「管理用タイトルを入力してください」\n"
       "- KHÔNG tạo bản ghi mới",
       note="Nguồn: file 03/tab function r204 + Small Send All r14."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Boundary",
       "Nhập 管理用タイトル lớn hơn 20 ký tự — hiện validate",
       A,
       "1. Nhập chuỗi 21 ký tự vào「管理用タイトル」\n"
       "2. Điền các trường còn lại hợp lệ\n"
       "3. Bấm lưu\n"
       "4. Thử lại với 50 ký tự",
       "21 ký tự full-width · 50 ký tự full-width",
       "- Hiện validate báo vượt độ dài (hoặc ô nhập chặn không cho gõ quá 20)\n"
       "- KHÔNG lưu được bản ghi với tên > 20 ký tự",
       note="Nguồn: r67, r409 + feature-spec.md §4 hàng 1 (max 20 ký tự)."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Normal",
       "管理用タイトル tự trim khoảng trắng đầu/cuối khi lưu",
       A,
       "1. Nhập「  配信テスト  」vào 管理用タイトル\n"
       "2. Lưu broadcast\n"
       "3. Về màn list, đọc giá trị cột「管理用タイトル」\n"
       "4. Mở lại màn edit, đọc lại giá trị trong ô",
       "「  配信テスト  」",
       "- Màn list hiển thị「配信テスト」(không có space thừa)\n"
       "- Ô nhập ở màn edit cũng hiển thị「配信テスト」",
       note="Nguồn: r69, r411."),

    tc("管理用タイトル & validate", "UI-INPUT-001", "Boundary",
       "Nhập 管理用タイトル độ dài tối đa — không vỡ layout ở form và màn list",
       A,
       "1. Nhập đúng 20 ký tự full-width vào 管理用タイトル\n"
       "2. Quan sát ô nhập ở form\n"
       "3. Lưu, về màn list quan sát cột「管理用タイトル」",
       "20 ký tự full-width「あいうえおかきくけこさしすせそたちつて」",
       "- Ô nhập không giãn làm vỡ form\n"
       "- Cột 管理用タイトル ở màn list không đẩy các cột khác lệch\n"
       "- Text bị cắt kèm dấu … hoặc xuống dòng gọn trong ô",
       note="Nguồn: r68, r410."),

    # ═══════════ 8. 配信タイミング設定 — gửi ngay/đặt lịch ═══════════
    tc("配信タイミング設定 — gửi ngay/đặt lịch", "UI-FIELD-001", "Normal",
       "Mặc định 配信タイミング設定 tích「メッセージ登録後すぐに配信」",
       A,
       "1. Bấm「新規作成」\n"
       "2. Quan sát khối「配信タイミング設定」",
       "—",
       "- Radio「メッセージ登録後すぐに配信」đang được tích\n"
       "- Khối chọn ngày/giờ đang ẩn hoặc disable",
       note="Nguồn: r70, r412 + db-mapping.md §5 (setting_send_message = 1)."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "UI-FIELD-001", "Normal",
       "Tích「配信予約」— hiện ngày giờ hiện tại, disable ngày quá khứ trên lịch",
       A,
       "1. Tích radio「配信予約」\n"
       "2. Quan sát giá trị ngày giờ mặc định\n"
       "3. Mở date picker, thử bấm vào 1 ngày trong quá khứ",
       "Ngày test = hôm nay",
       "- Ngày giờ mặc định = ngày giờ hiện tại\n"
       "- Các ngày trước hôm nay bị disable trên date picker, bấm không chọn được",
       note="Nguồn: r78, r413."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "STATE-001", "Normal",
       "Broadcast gửi ngay + có tin nhắn — status chuyển wait_to_send và xuất hiện ở 配信履歴",
       A + "\n- Đã chuẩn bị sẵn 1 template text",
       "1. Nhập tiêu đề, chọn「メッセージ登録後すぐに配信」\n"
       "2. Lưu bước 1, sang bước 2 thêm 1 tin nhắn text\n"
       "3. Bấm「配信内容を確認して送信に進む」và xác nhận gửi\n"
       "4. Về màn list, mở tab「配信履歴」\n"
       "5. Kiểm tra hộp thoại LINE của 1 friend",
       "Tiêu đề「即時配信」, 1 template text「テスト」",
       "- Broadcast xuất hiện ở tab「配信履歴」\n"
       "- Hiển thị ngày giờ gửi = thời điểm hiện tại, số 配信数 = tổng bạn bè\n"
       "- Friend nhận được tin nhắn「テスト」trong app LINE",
       env="PRODUCTION",
       note="Nguồn: r24, r153 (file 03/tab function). RULE-06: đi tới output cuối là app LINE. "
            "RULE-08: cần job thật → PRODUCTION."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "STATE-001", "Normal",
       "Broadcast đặt lịch tương lai + có tin nhắn — status wait_to_send, nằm ở tab 配信予約",
       A + "\n- Đã chuẩn bị sẵn 1 template text",
       "1. Nhập tiêu đề, tích「配信予約」, chọn thời gian sau 30 phút\n"
       "2. Lưu bước 1, sang bước 2 thêm 1 tin nhắn\n"
       "3. Bấm「配信内容を確認して送信に進む」\n"
       "4. Về màn list, mở tab「配信予約」",
       "Thời gian gửi = hiện tại + 30 phút",
       "- Broadcast nằm ở tab「配信予約」\n"
       "- Hiển thị đúng ngày giờ chờ gửi\n"
       "- Bảng broadcast: status = 'wait_to_send'",
       note="Nguồn: r18, r36, r395."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "STATE-001", "Abnormal",
       "Broadcast KHÔNG có tin nhắn — không chuyển sang chờ gửi, nằm ở tab 下書き",
       A,
       "1. Nhập tiêu đề, tích「配信予約」thời gian tương lai\n"
       "2. Lưu bước 1 (sang màn SCR-BC-04)\n"
       "3. KHÔNG thêm tin nhắn nào\n"
       "4. Quay về màn list bằng「メッセージ配信一覧に戻る」\n"
       "5. Kiểm tra cả 3 tab",
       "Không thêm template nào",
       "- Broadcast nằm ở tab「下書き」, KHÔNG ở tab「配信予約」\n"
       "- Đến giờ đặt lịch, friend KHÔNG nhận được tin nhắn nào",
       env="PRODUCTION",
       note="Nguồn: r17, r110, r139, r154 (file 03/tab function). ⚠️ Xem MT-03 — corpus r17 gọi trạng thái "
            "này là『unregistered』, r24 ghi nhận『không có message vẫn đang lưu được (chưa fix)』; "
            "spec logic-spec.md:27 nói create → 'unregistered', feature-spec.md §5 BR-01 nói tạo mới → 'draft'."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "FUNC-DATE-001", "Abnormal",
       "Đặt lịch ở thời điểm quá khứ — hiện alert cảnh báo gửi ngay",
       A,
       "1. Nhập tiêu đề, tích「配信予約」\n"
       "2. Chọn ngày giờ nhỏ hơn thời điểm hiện tại (VD hôm nay, 1 giờ trước)\n"
       "3. Bấm「配信内容を確認して送信に進む」",
       "Thời gian gửi = hiện tại − 1 giờ",
       "- Hiện alert đúng nguyên văn:「配信日時に現在時刻より前の時間が設定されています。配信登録を押すと即時配信となりますがよろしいですか？」\n"
       "- Alert có nút xác nhận và nút hủy\n"
       "- Chọn xác nhận → broadcast được lưu và gửi ngay",
       note="Nguồn: r60, r76, r352 + file 03/tab function r205. ⚠️ r60 và r76 ghi nhận『chưa có nút hủy』— "
            "TC viết theo hành vi ĐÚNG (phải có nút hủy), dự kiến FAIL nếu chưa fix → cần raise bug."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "FUNC-DATE-001", "Abnormal",
       "Đặt lịch quá khứ rồi bấm HỦY ở alert — không lưu, giữ nguyên màn hình",
       A,
       "1. Nhập tiêu đề, tích「配信予約」, chọn thời gian quá khứ\n"
       "2. Bấm「配信内容を確認して送信に進む」→ alert hiện ra\n"
       "3. Bấm nút hủy trên alert\n"
       "4. Quan sát màn hình và kiểm tra tab「配信履歴」",
       "Thời gian gửi = hiện tại − 1 giờ",
       "- Alert đóng, quay lại màn form với dữ liệu đã nhập còn nguyên\n"
       "- KHÔNG có broadcast mới ở tab「配信履歴」\n"
       "- Friend KHÔNG nhận được tin nhắn",
       env="PRODUCTION",
       note="Nguồn: suy ra từ r60/r76 (『chưa có nút hủy』). ⚠️ Đây là nhánh corpus CHƯA test — "
            "TC do AI bổ sung, cần Leader xác nhận alert có nút hủy trên bản hiện tại."),

    tc("配信タイミング設定 — gửi ngay/đặt lịch", "FUNC-DATE-001", "Abnormal",
       "Ở tab 配信予約 đặt lịch quá khứ — hành vi có phải là validate chặn không?",
       A,
       "1. Từ tab「配信予約」bấm「新規作成」\n"
       "2. Tích「配信予約」, chọn thời gian quá khứ\n"
       "3. Bấm lưu\n"
       "4. Ghi lại chính xác thông báo hiện ra",
       "Thời gian gửi = hôm qua 10:00",
       "- Ghi lại hành vi thực tế: là alert xác nhận (như TC trên) hay validate chặn hẳn\n"
       "- Nếu là validate chặn: KHÔNG cho lưu, không tạo bản ghi",
       spec="Đã hỏi leader",
       note="⚠️ MT-04 — r76 nói『aleret』, r84 nói『validate』cho cùng thao tác chọn time quá khứ ở 2 khối "
            "khác nhau của cùng tab master; r84 kết quả NG. Cần Leader chốt hành vi đúng."),

    # ═══════════ 9. 配信日時追加 — nhiều lịch gửi ═══════════
    tc("配信日時追加 — nhiều lịch gửi", "UI-FIELD-001", "Normal",
       "Ghi chú giới hạn 10 mốc thời gian hiển thị trên form",
       A,
       "1. Tích「配信予約」\n"
       "2. Đọc dòng ghi chú cạnh nút「配信日時追加」",
       "—",
       "- Hiển thị đúng câu「配信日時は複数登録ができます。最大10個の日時まで登録可能です。」",
       note="Nguồn: ui-spec.md:174."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-MULTI-001", "Normal",
       "Thêm dưới 10 mốc thời gian — nút 配信日時追加 vẫn enable",
       A,
       "1. Tích「配信予約」\n"
       "2. Bấm「配信日時追加」lần lượt tới khi có tổng 9 mốc\n"
       "3. Quan sát trạng thái nút「配信日時追加」",
       "9 mốc thời gian khác nhau trong tương lai",
       "- Sau mỗi lần thêm, mốc mới xuất hiện trong danh sách\n"
       "- Nút「配信日時追加」vẫn enable khi tổng số mốc < 10",
       note="Nguồn: r71, r79, r414."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-MULTI-001", "Boundary",
       "Đủ 10 mốc thời gian — nút 配信日時追加 chuyển sang disable",
       A,
       "1. Tích「配信予約」\n"
       "2. Thêm mốc cho tới khi tổng đúng 10\n"
       "3. Quan sát nút「配信日時追加」\n"
       "4. Thử bấm vào nút",
       "10 mốc thời gian khác nhau trong tương lai",
       "- Nút「配信日時追加」chuyển sang disable\n"
       "- Bấm vào nút không thêm được mốc thứ 11\n"
       "- Danh sách vẫn đúng 10 mốc",
       note="Nguồn: r72-r73, r80-r81, r415-r416 — r72/r73 ghi nhận『chưa disable button 配信日時追加』ở lần "
            "test dev. TC viết theo hành vi ĐÚNG; nếu vẫn chưa disable → raise bug."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-MULTI-001", "Boundary",
       "Cố lưu broadcast có hơn 10 mốc thời gian — hệ thống chặn ở tầng lưu",
       A,
       "1. Tạo broadcast có đúng 10 mốc, lưu thành công\n"
       "2. Dùng DevTools gọi lại API lưu broadcast với mảng delivery_dates gồm 11 phần tử\n"
       "3. Về màn list, đếm số dòng của broadcast đó",
       "delivery_dates = 11 phần tử",
       "- API trả lỗi hoặc chỉ lưu tối đa 10 mốc\n"
       "- Màn list hiển thị tối đa 10 dòng cho broadcast đó\n"
       "- Bảng broadcast: số bản ghi con ≤ 9 (cha + 9 con = 10 mốc)",
       spec="Đã hỏi leader",
       note="⚠️ Corpus chỉ test ở tầng UI (r73/r81『setup hơn 10 option』). TC này bổ sung tầng API — "
            "do AI viết, cần Leader xác nhận backend có validate giới hạn 10 hay chỉ chặn ở FE.",
       group="API"),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-001", "Normal",
       "Sửa 1 mốc thời gian đã thêm — click thẳng vào là sửa được",
       A,
       "1. Tích「配信予約」, thêm 3 mốc thời gian\n"
       "2. Bấm vào mốc thứ 2 trong danh sách\n"
       "3. Đổi sang thời gian khác\n"
       "4. Quan sát danh sách",
       "3 mốc: mai 09:00 / mai 12:00 / mai 15:00 → sửa mốc 2 thành mai 18:00",
       "- Click vào mốc là mở được ô chỉnh sửa ngay tại chỗ\n"
       "- Sau khi sửa, danh sách hiển thị mai 09:00 / mai 15:00 / mai 18:00",
       note="Nguồn: r74, r82, r417."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-001", "Normal",
       "Xóa 1 mốc thời gian đã thêm",
       A,
       "1. Tích「配信予約」, thêm 3 mốc thời gian\n"
       "2. Bấm icon xóa ở mốc thứ 2\n"
       "3. Đếm số mốc còn lại\n"
       "4. Lưu broadcast và về màn list đếm số dòng",
       "3 mốc → xóa 1 mốc",
       "- Danh sách còn đúng 2 mốc, đúng 2 giá trị còn lại\n"
       "- Sau khi lưu, màn list hiển thị 2 dòng cho broadcast đó\n"
       "- Bảng broadcast: chỉ còn 1 bản ghi con",
       note="Nguồn: r77, r85, r419, r823-r825, r848-r850."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-UNIQ-001", "Abnormal",
       "Đặt 2 mốc thời gian trùng nhau — hiện validate trùng",
       A,
       "1. Tích「配信予約」, đặt mốc 1 = mai 10:00\n"
       "2. Thêm mốc 2 cũng = mai 10:00\n"
       "3. Bấm lưu\n"
       "4. Lặp lại với trường hợp mốc con trùng mốc con khác",
       "Mốc 1 = mốc 2 = mai 10:00",
       "- Hiện validate đúng nguyên văn「重複になっています。」\n"
       "- KHÔNG lưu được broadcast với 2 mốc trùng",
       note="Nguồn: file 03/tab function r15 (『check time trùng nhau: time con = time cha, "
            "time con = time con → validate 重複になっています。』)."),

    tc("配信日時追加 — nhiều lịch gửi", "FUNC-MULTI-001", "Normal",
       "Thêm mốc thời gian SAU khi broadcast đã tạo xong",
       A + "\n- Đã có 1 broadcast wait_to_send với 1 mốc gửi, cách giờ gửi > 30 phút",
       "1. Mở broadcast đó ở màn edit\n"
       "2. Bấm「配信日時追加」thêm 2 mốc mới\n"
       "3. Lưu\n"
       "4. Về màn list đếm số dòng của broadcast",
       "Thêm 2 mốc: hiện tại + 2h và + 3h",
       "- Lưu thành công\n"
       "- Màn list hiển thị 3 dòng cho broadcast đó\n"
       "- Bảng broadcast: 2 bản ghi con mới có parent_id = id của broadcast cha",
       note="Nguồn: r817-r822, r843-r847, file 03/tab function r183."),

    tc("配信日時追加 — nhiều lịch gửi", "DATA-REF-001", "Normal",
       "Mốc con clone đủ tin nhắn, action và filter từ mốc cha",
       A + "\n- Chuẩn bị 1 tag T gắn cho 3 friend",
       "1. Tạo broadcast: tiêu đề, đặt lịch mai 10:00, filter theo tag T\n"
       "2. Lưu bước 1, thêm 1 tin nhắn text và 1 action gán tag\n"
       "3. Quay lại thêm mốc gửi thứ 2 = mai 14:00, lưu\n"
       "4. Mở màn preview của dòng mốc thứ 2 ở màn list\n"
       "5. Đối chiếu tin nhắn, action, filter, số 配信数 với dòng mốc cha",
       "Tag T = 3 friend · 1 template text · 1 action gán tag",
       "- Dòng mốc con hiển thị đúng cùng tin nhắn, cùng action, cùng điều kiện filter\n"
       "- Số 配信数 của mốc con = 3, bằng mốc cha\n"
       "- Bảng filters_v2: bản ghi filter của mốc con trỏ đúng về broadcast con",
       note="Nguồn: r16, r48-r59 + logic-spec.md:184-190 (clone templates/actions, filter sync).",
       group="Data"),

    tc("配信日時追加 — nhiều lịch gửi", "DATA-REF-001", "Normal",
       "Sửa tin nhắn khi CHƯA tạo xong — mốc con thay đổi theo mốc cha",
       A,
       "1. Tạo broadcast nhiều mốc, lưu bước 1 nhưng CHƯA thêm tin nhắn\n"
       "2. Thêm 1 tin nhắn text ở mốc cha\n"
       "3. Mở preview của từng mốc con",
       "2 mốc gửi, thêm 1 template text ở mốc cha",
       "- Tất cả mốc con đều hiển thị tin nhắn vừa thêm\n"
       "- Sửa nội dung ở cha thì con đổi theo",
       note="Nguồn: file 03/tab function r105 (『khi chưa tạo xong tin nhắn (parent id của con = parent id cha) "
            "→ cha thay đổi sao con thay đổi vậy』).",
       group="Data"),

    tc("配信日時追加 — nhiều lịch gửi", "DATA-REF-001", "Normal",
       "Sửa tin nhắn SAU khi đã tạo xong — chỉ mốc được sửa thay đổi",
       A,
       "1. Tạo broadcast 2 mốc, thêm tin nhắn, lưu hoàn tất (status wait_to_send)\n"
       "2. Mở màn edit của mốc con, sửa nội dung tin nhắn\n"
       "3. Mở preview của mốc cha và mốc con",
       "Sửa nội dung tin nhắn của mốc con thành「変更後」",
       "- Mốc con hiển thị「変更後」\n"
       "- Mốc cha giữ nguyên nội dung cũ, KHÔNG bị đổi theo",
       note="Nguồn: file 03/tab function r106 (『khi đã tạo xong tin nhắn (parent id của con = Null) → "
            "edit bản nào thì bản đó thay đổi』) — cột Note ghi nhận bug『edit message 1 bản các bản khác "
            "cũng thay đổi theo』. TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa fix → raise bug.",
       group="Data"),

    # ═══════════ 10. Lưu & điều hướng bước 1 ═══════════
    tc("Lưu & điều hướng bước 1", "FUNC-001", "Normal",
       "Nhập đủ thông tin bước 1 → mở ra phần メッセージ登録 và エルメアクションを追加",
       A,
       "1. Nhập「管理用タイトル」\n"
       "2. Chọn「配信タイミング設定」\n"
       "3. Chọn「配信先絞込み」\n"
       "4. Bấm「配信内容を確認して送信に進む」",
       "Tiêu đề「テスト配信」, gửi ngay, すべての友だち",
       "- Chuyển sang màn SCR-BC-04, URL có ?broadcast_id=XXX\n"
       "- Hiện ra khối「メッセージ登録」và khối「エルメアクションを追加」\n"
       "- Bảng broadcast: tạo bản ghi mới, parent_id = NULL",
       note="Nguồn: r16, r393, r102 (file 03/tab function)."),

    tc("Lưu & điều hướng bước 1", "CONC-002", "Abnormal",
       "Double click「配信内容を確認して送信に進む」— chỉ tạo 1 broadcast",
       A,
       "1. Nhập đủ thông tin bước 1\n"
       "2. Double click nhanh vào「配信内容を確認して送信に進む」\n"
       "3. Về màn list, đếm số bản ghi trùng tên",
       "Double click trong < 1 giây",
       "- Chỉ tạo đúng 1 bản ghi broadcast\n"
       "- Không có 2 bản ghi cùng tên, cùng thời gian",
       note="Nguồn: r153, r481.",
       group="API"),

    tc("Lưu & điều hướng bước 1", "FUNC-DRAFT-001", "Normal",
       "Bấm「下書きとして保存」với đủ trường bắt buộc — lưu vào tab 下書き",
       A,
       "1. Nhập「管理用タイトル」và thời gian gửi\n"
       "2. Bấm「下書きとして保存」\n"
       "3. Về màn list, mở tab「下書き」",
       "Tiêu đề「下書きテスト」, đặt lịch mai 10:00",
       "- Broadcast xuất hiện ở tab「下書き」\n"
       "- Bảng broadcast: status = 'draft'\n"
       "- KHÔNG xuất hiện ở tab「配信予約」",
       note="Nguồn: r157, r400, r485."),

    tc("Lưu & điều hướng bước 1", "FUNC-DRAFT-001", "Abnormal",
       "Bấm「下書きとして保存」khi thiếu trường bắt buộc — hiện alert, không lưu",
       A,
       "1. Để trống「管理用タイトル」\n"
       "2. Bấm「下書きとして保存」\n"
       "3. Kiểm tra tab「下書き」",
       "管理用タイトル = trống",
       "- Hiện alert báo thiếu trường bắt buộc\n"
       "- KHÔNG tạo bản ghi ở tab「下書き」",
       note="Nguồn: r158, r402-r404."),

    tc("Lưu & điều hướng bước 1", "CONC-002", "Abnormal",
       "Double click「下書きとして保存」— chỉ tạo 1 bản nháp",
       A,
       "1. Nhập đủ thông tin\n"
       "2. Double click nhanh vào「下書きとして保存」\n"
       "3. Về tab「下書き」đếm số bản ghi trùng tên",
       "Double click trong < 1 giây",
       "- Chỉ tạo đúng 1 bản nháp",
       note="Nguồn: r156, r484.",
       group="API"),

    tc("Lưu & điều hướng bước 1", "STATE-CLEAN-001", "Abnormal",
       "Nhập đủ thông tin nhưng KHÔNG bấm lưu rồi rời màn — không tạo bản ghi",
       A,
       "1. Nhập đủ「管理用タイトル」, thời gian, đối tượng\n"
       "2. KHÔNG bấm nút lưu nào\n"
       "3. Bấm「メッセージ配信一覧に戻る」\n"
       "4. Kiểm tra cả 3 tab",
       "Tiêu đề「保存しない」",
       "- Không có broadcast nào tên「保存しない」ở bất kỳ tab nào\n"
       "- Bảng broadcast không có bản ghi mới",
       note="Nguồn: r63, r405."),

    tc("Lưu & điều hướng bước 1", "FUNC-001", "Normal",
       "Button「メッセージ配信一覧に戻る」quay về màn list",
       A + "\n- Đang ở màn SCR-BC-02 hoặc SCR-BC-04",
       "1. Bấm「メッセージ配信一覧に戻る」\n"
       "2. Quan sát màn hình",
       "—",
       "- Quay về /basic/message-send-all\n"
       "- Hiển thị tab đang xem trước đó",
       note="Nguồn: r150, r478 + file 03/tab function r93."),

    tc("Lưu & điều hướng bước 1", "CONC-002", "Abnormal",
       "Double click「メッセージ配信一覧に戻る」— chỉ chuyển màn 1 lần",
       A,
       "1. Double click nhanh vào「メッセージ配信一覧に戻る」\n"
       "2. Quan sát lịch sử trình duyệt (nút Back)",
       "Double click trong < 1 giây",
       "- Chỉ chuyển về màn list 1 lần\n"
       "- Bấm Back của trình duyệt quay về đúng màn form, không bị kẹt vòng lặp",
       note="Nguồn: r151, r479."),

    # ═══════════ 11. メッセージ登録 — thêm/sửa/xóa ═══════════
    tc("メッセージ登録 — thêm/sửa/xóa", "LIST-001", "Normal",
       "Khối メッセージ登録 khi chưa có tin nhắn nào — hiển thị empty state",
       B2,
       "1. Ở màn SCR-BC-04, quan sát khối「メッセージ登録」khi chưa thêm gì",
       "0 template",
       "- Hiển thị đúng câu「メッセージが登録されていません」",
       note="Nguồn: r86, r420."),

    tc("メッセージ登録 — thêm/sửa/xóa", "LIST-001", "Normal",
       "Danh sách tin nhắn sắp xếp từ cũ đến mới",
       B2 + "\n- Đã thêm 3 tin nhắn theo thứ tự A → B → C",
       "1. Thêm lần lượt 3 tin nhắn text nội dung A, B, C\n"
       "2. Đọc thứ tự trong khối「メッセージ登録」",
       "3 template text: A, B, C",
       "- Thứ tự hiển thị là A, B, C (cũ nhất trên đầu)",
       note="Nguồn: r87, r421."),

    tc("メッセージ登録 — thêm/sửa/xóa", "FUNC-001", "Normal",
       "Kéo thả sắp xếp lại thứ tự tin nhắn — preview và tin friend nhận đổi theo",
       B2 + "\n- Đã thêm 3 tin nhắn text A, B, C",
       "1. Quan sát khung viền của tin nhắn trước khi kéo\n"
       "2. Kéo tin C lên vị trí đầu tiên, thả\n"
       "3. Mở「プレビューとテスト」đọc thứ tự ở tab メッセージ\n"
       "4. Gửi test cho 1 friend, mở app LINE đọc thứ tự tin nhận được",
       "3 template text A, B, C → kéo C lên đầu",
       "- Khi kéo, có khung chỉ vị trí thả theo design\n"
       "- Sau khi thả: danh sách là C, A, B\n"
       "- Preview hiển thị đúng thứ tự C, A, B\n"
       "- Friend nhận được tin theo đúng thứ tự C, A, B trong app LINE",
       env="PRODUCTION",
       note="Nguồn: r88-r90, r422-r424. RULE-06 + RULE-07: verify cả màn hình, preview và output LINE."),

    tc("メッセージ登録 — thêm/sửa/xóa", "FUNC-001", "Normal",
       "Sửa tin nhắn — preview và tin friend nhận cập nhật theo",
       B2 + "\n- Đã thêm 1 tin nhắn text nội dung「変更前」",
       "1. Bấm「編集」ở tin nhắn\n"
       "2. Sửa nội dung thành「変更後」, lưu\n"
       "3. Mở preview kiểm tra nội dung\n"
       "4. Gửi test cho 1 friend, mở app LINE",
       "「変更前」→「変更後」",
       "- Preview hiển thị「変更後」\n"
       "- Friend nhận được tin「変更後」, không phải「変更前」",
       env="PRODUCTION",
       note="Nguồn: r91-r93, r425-r427."),

    tc("メッセージ登録 — thêm/sửa/xóa", "CONC-002", "Abnormal",
       "Double click button「編集」— chỉ mở 1 màn soạn tin",
       B2 + "\n- Đã thêm 1 tin nhắn",
       "1. Double click nhanh vào「編集」\n"
       "2. Quan sát số màn/tab mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 màn soạn tin nhắn (SCR-BC-05)",
       note="Nguồn: r91, r425."),

    tc("メッセージ登録 — thêm/sửa/xóa", "FUNC-001", "Normal",
       "Xóa tin nhắn — biến mất khỏi preview và friend không còn nhận",
       B2 + "\n- Đã thêm 2 tin nhắn text A và B",
       "1. Xóa tin nhắn B\n"
       "2. Mở preview kiểm tra\n"
       "3. Gửi test cho 1 friend, mở app LINE",
       "2 template A, B → xóa B",
       "- Preview chỉ còn tin A\n"
       "- Friend chỉ nhận được tin A, KHÔNG nhận tin B\n"
       "- Bảng broadcast: template_ids không còn id của B",
       env="PRODUCTION",
       note="Nguồn: r94-r95, r428-r429."),

    tc("メッセージ登録 — thêm/sửa/xóa", "CONC-002", "Abnormal",
       "Double click「メッセージ追加」— chỉ mở 1 màn chọn loại tin nhắn",
       B2,
       "1. Double click nhanh vào「メッセージ追加」\n"
       "2. Quan sát số màn mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 màn SCR-BC-05「メッセージタイプを選択」",
       note="Nguồn: r96, r430."),

    tc("メッセージ登録 — thêm/sửa/xóa", "MSG-001", "Normal",
       "Tin nhắn thêm trực tiếp — template button có action mở URL giữ nguyên domain",
       B2 + "\n- Chuẩn bị 1 URL dài của trang ngoài (VD https://example.com/very/long/path)",
       "1. Bấm「メッセージ追加」→ chọn loại パネル・ボタン\n"
       "2. Tạo 1 button có action「URLを開く」trỏ tới URL đã chuẩn bị\n"
       "3. Lưu, đặt lịch gửi và chờ job gửi\n"
       "4. Ở app LINE, bấm vào button\n"
       "5. Quan sát URL trên thanh địa chỉ trình duyệt mở ra",
       "URL: https://example.com/very/long/path?a=1&b=2",
       "- URL mở ra GIỮ NGUYÊN domain gốc, KHÔNG bị rút gọn thành domain tracking\n"
       "- Trang đích mở đúng nội dung",
       env="PRODUCTION",
       note="Nguồn: r97, r103, r106 — corpus ghi rõ『chỉ check case send phía job, phía web có r』. "
            "RULE-08: URL/domain + job → PRODUCTION.",
       group="API"),

    tc("メッセージ登録 — thêm/sửa/xóa", "MSG-001", "Normal",
       "Template image map có action mở URL — giữ nguyên domain khi friend bấm",
       B2 + "\n- Chuẩn bị 1 ảnh image map và 1 URL dài",
       "1. Thêm tin nhắn loại image map, gán action「URLを開く」cho 1 vùng tap\n"
       "2. Lưu, đặt lịch gửi và chờ job gửi\n"
       "3. Ở app LINE, bấm vào vùng tap đó\n"
       "4. Quan sát URL trên thanh địa chỉ",
       "Image map 1040×1040, 1 vùng tap trỏ https://example.com/very/long/path",
       "- URL mở ra giữ nguyên domain gốc, không bị rút gọn\n"
       "- Vùng tap đúng vị trí đã cấu hình",
       env="PRODUCTION",
       note="Nguồn: r98, r104, r107. RULE-08: media + URL + job → PRODUCTION.",
       group="API"),

    tc("メッセージ登録 — thêm/sửa/xóa", "MSG-001", "Abnormal",
       "Lưu broadcast KHÔNG có tin nhắn nào — phải bị chặn bằng validate",
       B2,
       "1. Ở màn SCR-BC-04, không thêm tin nhắn nào\n"
       "2. Bấm「配信内容を確認して送信に進む」",
       "0 template",
       "- Hiện validate báo phải có ít nhất 1 tin nhắn\n"
       "- KHÔNG chuyển broadcast sang trạng thái chờ gửi",
       note="Nguồn: r62 — kết quả gốc ghi『chưa validate』và r24 ghi『không có message vẫn đang lưu được "
            "(chưa fix)』. TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa fix → cần raise bug."),

    tc("メッセージ登録 — thêm/sửa/xóa", "MEDIA-001", "Abnormal",
       "Thêm tin nhắn loại PDF — không bị treo loading",
       B2 + "\n- Chuẩn bị 1 file PDF hợp lệ",
       "1. Bấm「メッセージ追加」→ chọn loại có upload PDF\n"
       "2. Upload file PDF, bấm lưu\n"
       "3. Quan sát màn hình sau khi bấm lưu",
       "File PDF 1 trang, < 10MB",
       "- Lưu thành công trong thời gian hợp lý\n"
       "- Màn hình quay lại SCR-BC-04, KHÔNG bị kẹt ở trạng thái loading\n"
       "- Tin nhắn PDF xuất hiện trong danh sách",
       env="PRODUCTION",
       note="Nguồn: file 03/tab function r13 — ghi nhận『loading mãi success không back ra ngoài』trên "
            "staging, 『dev k bị』. RULE-08: media → PRODUCTION."),

    # ═══════════ 12. テンプレートから追加 ═══════════
    tc("テンプレートから追加", "CONC-002", "Abnormal",
       "Double click「テンプレートから追加」— chỉ mở 1 popup",
       B2,
       "1. Double click nhanh vào「テンプレートから追加」\n"
       "2. Quan sát số popup mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 popup「テンプレートから選択」",
       note="Nguồn: r100, r432."),

    tc("テンプレートから追加", "UI-001", "Normal",
       "Popup テンプレートから選択 hiển thị 2 lựa chọn sử dụng",
       B2 + "\n- Thư viện template có ≥1 group template",
       "1. Bấm「テンプレートから追加」\n"
       "2. Quan sát nội dung popup",
       "≥1 group template trong thư viện",
       "- Popup hiển thị 2 lựa chọn:「テンプレートをそのまま利用する」và「テンプレートを引用して編集する」",
       note="Nguồn: r101, r433."),

    tc("テンプレートから追加", "DATA-REF-001", "Normal",
       "Chọn「テンプレートをそのまま利用する」— sửa template gốc thì broadcast đổi theo",
       B2 + "\n- Thư viện có template T nội dung「元の内容」",
       "1. Bấm「テンプレートから追加」→ chọn「テンプレートをそのまま利用する」\n"
       "2. Chọn template T, lưu\n"
       "3. Sang màn「テンプレート」sửa nội dung T thành「編集後」\n"
       "4. Quay lại broadcast, mở preview",
       "Template T:「元の内容」→「編集後」",
       "- Preview của broadcast hiển thị「編集後」\n"
       "- Bảng broadcast: template_ids trỏ tới id của template T (category_id ≥ 0, không clone)",
       note="Nguồn: r102, r434, file 03/tab function r112 + logic-spec.md:186-187.",
       group="Data"),

    tc("テンプレートから追加", "DATA-REF-001", "Normal",
       "Chọn「テンプレートを引用して編集する」— sửa template gốc KHÔNG ảnh hưởng broadcast",
       B2 + "\n- Thư viện có template T nội dung「元の内容」",
       "1. Bấm「テンプレートから追加」→ chọn「テンプレートを引用して編集する」\n"
       "2. Chọn template T, lưu\n"
       "3. Sang màn「テンプレート」sửa nội dung T thành「編集後」\n"
       "4. Quay lại broadcast, mở preview",
       "Template T:「元の内容」→「編集後」",
       "- Preview của broadcast vẫn hiển thị「元の内容」\n"
       "- Bảng template: có bản clone mới với category_id = -11",
       note="Nguồn: r105, r435, file 03/tab function r113 + logic-spec.md:186-188.",
       group="Data"),

    tc("テンプレートから追加", "REG-SHARED-001", "Normal",
       "Chức năng tạo template cũ vẫn hoạt động bình thường khi mở từ broadcast",
       B2,
       "1. Bấm「テンプレートから追加」\n"
       "2. Trong popup, thử tạo mới 1 template\n"
       "3. Lưu và kiểm tra template mới có ở thư viện「テンプレート」không",
       "Template mới tên「新規テンプレート」",
       "- Tạo template thành công từ trong luồng broadcast\n"
       "- Template mới xuất hiện ở màn「テンプレート」với đúng nội dung",
       note="Nguồn: r99, r431."),

    tc("テンプレートから追加", "MSG-001", "Normal",
       "Template button dùng lại nguyên mẫu — action mở URL giữ nguyên domain",
       B2 + "\n- Thư viện có template button với action「URLを開く」trỏ URL dài",
       "1. Thêm template đó bằng「テンプレートをそのまま利用する」\n"
       "2. Đặt lịch gửi, chờ job gửi\n"
       "3. Ở app LINE bấm vào button\n"
       "4. Quan sát URL mở ra",
       "URL: https://example.com/very/long/path?a=1&b=2",
       "- URL giữ nguyên domain gốc, không bị rút gọn",
       env="PRODUCTION",
       note="Nguồn: r103. RULE-08: URL/domain + job → PRODUCTION.",
       group="API"),

    tc("テンプレートから追加", "DATA-REF-001", "Normal",
       "Sửa 1 tin nhắn trong nhóm dùng nguyên mẫu — các bản khác trong nhóm đổi theo",
       B2 + "\n- Broadcast nhiều mốc gửi, dùng template T theo kiểu「そのまま利用する」",
       "1. Tạo broadcast 2 mốc gửi, thêm template T kiểu そのまま利用する\n"
       "2. Sửa nội dung template T\n"
       "3. Mở preview của cả 2 mốc",
       "Template T dùng chung cho 2 mốc",
       "- Cả 2 mốc đều hiển thị nội dung mới\n"
       "- Template gốc ở thư viện cũng là nội dung mới",
       note="Nguồn: file 03/tab function r112.",
       group="Data"),

    tc("テンプレートから追加", "DATA-REF-001", "Normal",
       "Sửa 1 tin nhắn trong nhóm dùng trích dẫn — chỉ bản đó thay đổi",
       B2 + "\n- Broadcast nhiều mốc gửi, dùng template T kiểu「引用して編集する」",
       "1. Tạo broadcast 2 mốc, thêm template T kiểu 引用して編集する\n"
       "2. Sửa nội dung tin nhắn ở mốc 1\n"
       "3. Mở preview của mốc 1 và mốc 2\n"
       "4. Kiểm tra template gốc ở thư viện",
       "Template T trích dẫn, sửa ở mốc 1",
       "- Mốc 1 đổi nội dung, mốc 2 giữ nguyên\n"
       "- Template gốc ở thư viện KHÔNG đổi\n"
       "- Bảng template: bản clone có category_id = -11",
       note="Nguồn: file 03/tab function r113-r115.",
       group="Data"),

    # ═══════════ 13. エルメアクション — đăng ký & filter ═══════════
    tc("エルメアクション — đăng ký & filter", "UI-FIELD-001", "Normal",
       "Khối エルメアクションを追加 mặc định ở trạng thái thu gọn",
       B2,
       "1. Quan sát khối「エルメアクションを追加」khi vừa vào màn SCR-BC-04",
       "—",
       "- Khối đang thu gọn (collapsed)\n"
       "- Có icon mở rộng",
       note="Nguồn: r112, r439."),

    tc("エルメアクション — đăng ký & filter", "FUNC-001", "Normal",
       "Bấm icon mở rộng khối エルメアクション",
       B2,
       "1. Bấm icon mở rộng ở khối「エルメアクションを追加」\n"
       "2. Quan sát nội dung hiện ra",
       "—",
       "- Khối mở rộng, hiển thị danh sách action và nút「アクション登録」",
       note="Nguồn: r113, r440."),

    tc("エルメアクション — đăng ký & filter", "LIST-001", "Normal",
       "Danh sách action khi chưa có action nào — hiển thị empty state",
       B2,
       "1. Mở rộng khối「エルメアクションを追加」khi chưa đăng ký action nào",
       "0 action",
       "- Hiển thị đúng câu「エルメアクションが登録されていません」",
       note="Nguồn: r114, r441."),

    tc("エルメアクション — đăng ký & filter", "LIST-001", "Normal",
       "Danh sách action khi có action — hiển thị theo vị trí folder tương ứng",
       B2 + "\n- Đã đăng ký 3 action thuộc 2 folder khác nhau",
       "1. Mở rộng khối「エルメアクションを追加」\n"
       "2. Đọc thứ tự các action\n"
       "3. Đối chiếu với thứ tự folder ở màn cấu hình action",
       "3 action: 2 action ở folder A, 1 action ở folder B",
       "- Hiển thị đủ 3 action\n"
       "- Thứ tự khớp với vị trí của folder tương ứng",
       note="Nguồn: r115, r442."),

    tc("エルメアクション — đăng ký & filter", "CONC-002", "Abnormal",
       "Double click「アクション登録」— chỉ mở 1 modal",
       B2,
       "1. Double click nhanh vào「アクション登録」\n"
       "2. Quan sát số modal mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 modal cấu hình action",
       note="Nguồn: r116, r443."),

    tc("エルメアクション — đăng ký & filter", "REG-SHARED-001", "Normal",
       "Chức năng đăng ký action cũ vẫn hoạt động khi mở từ broadcast",
       B2,
       "1. Bấm「アクション登録」\n"
       "2. Thử lần lượt các loại action: gán tag · trigger step · đổi rich menu\n"
       "3. Lưu và kiểm tra danh sách action của broadcast",
       "3 action: gán tag T · trigger scenario S · đổi richmenu R",
       "- Cả 3 loại đăng ký được, xuất hiện đủ trong danh sách\n"
       "- Bảng t_actions + t_actions_detail có bản ghi tương ứng",
       note="Nguồn: r117, r444."),

    tc("エルメアクション — đăng ký & filter", "MSG-004", "Normal",
       "Action 絞り込みなし — mọi friend nhận tin đều được thực thi action",
       B2 + "\n- Bot có 5 friend, 3 người có tag T\n- Broadcast gửi cho すべての友だち",
       "1. Đăng ký action gán tag X, chọn「絞り込みなし」\n"
       "2. Lưu, đặt lịch gửi và chờ job gửi xong\n"
       "3. Kiểm tra tag X của cả 5 friend ở màn 友だちリスト",
       "5 friend, action gán tag X, không filter",
       "- Cả 5 friend đều được gán tag X\n"
       "- Bảng action_line_users có 5 bản ghi tương ứng",
       env="PRODUCTION",
       note="Nguồn: r118, r445. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("エルメアクション — đăng ký & filter", "MSG-004", "Normal",
       "Action 絞り込みあり — chỉ friend thỏa filter của action mới được thực thi",
       B2 + "\n- Bot có 5 friend, 3 người có tag T\n- Broadcast gửi cho すべての友だち",
       "1. Đăng ký action gán tag X, chọn「絞り込みあり」với điều kiện có tag T\n"
       "2. Lưu, đặt lịch gửi và chờ job gửi xong\n"
       "3. Kiểm tra tag X của từng friend trong 5 người",
       "5 friend, 3 người có tag T, action gán tag X lọc theo tag T",
       "- Cả 5 friend đều NHẬN được tin nhắn\n"
       "- Chỉ 3 friend có tag T được gán thêm tag X\n"
       "- 2 friend còn lại không có tag X",
       env="PRODUCTION",
       note="Nguồn: r119, r446 — r119 ghi rõ điều kiện『friend phải có tên trên phần 配信先絞込み』, "
            "tức filter của action là tập CON của đối tượng nhận. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("エルメアクション — đăng ký & filter", "MSG-004", "Boundary",
       "Friend thỏa filter action nhưng KHÔNG thuộc đối tượng nhận — không được thực thi action",
       B2 + "\n- Bot có 5 friend: 3 người tag T, 2 người tag U\n- Broadcast lọc đối tượng theo tag U",
       "1. Đặt「配信先絞込み」= có tag U (2 friend)\n"
       "2. Đăng ký action gán tag X với「絞り込みあり」điều kiện có tag T (3 friend)\n"
       "3. Lưu, đặt lịch gửi và chờ job gửi xong\n"
       "4. Kiểm tra tag X của cả 5 friend",
       "配信先 = tag U (2 người) · action filter = tag T (3 người) · 2 tập không giao nhau",
       "- Chỉ 2 friend có tag U nhận được tin nhắn\n"
       "- KHÔNG friend nào được gán tag X (vì 3 người tag T không nằm trong đối tượng nhận)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r27, r119 (『vs đk friend phải có tên trên phần 配信先絞込み』). Đây là suy luận từ "
            "quy tắc chung sang trường hợp 2 tập KHÔNG giao nhau — corpus không test trực tiếp. "
            "⚠️ Cần Leader xác nhận.",
       group="API"),

    tc("エルメアクション — đăng ký & filter", "MSG-004", "Normal",
       "Friend bấm vào vùng ảnh của tin nhắn có action — nhận được tin nhắn tương ứng",
       B2 + "\n- Đã thêm template image map có action gửi tin nhắn cho từng vùng",
       "1. Thêm template image map, gán action gửi tin cho từng vùng tap\n"
       "2. Lưu, gửi broadcast và chờ job gửi xong\n"
       "3. Ở app LINE, bấm lần lượt vào từng vùng của ảnh",
       "Image map 4 vùng tap, mỗi vùng gửi 1 tin khác nhau",
       "- Mỗi vùng bấm trả về đúng tin nhắn đã cấu hình cho vùng đó\n"
       "- Không có vùng nào trả nhầm tin của vùng khác",
       env="PRODUCTION",
       note="Nguồn: r120, r447. RULE-06: đi tới output cuối là app LINE.",
       group="API"),

    tc("エルメアクション — đăng ký & filter", "STATE-CLEAN-001", "Abnormal",
       "Tạo action nhưng KHÔNG lưu — action không được đăng ký",
       B2,
       "1. Bấm「アクション登録」, cấu hình 1 action gán tag\n"
       "2. Đóng modal mà KHÔNG bấm lưu\n"
       "3. Quan sát danh sách action của broadcast",
       "Action gán tag X, không lưu",
       "- Danh sách action vẫn rỗng («エルメアクションが登録されていません»)\n"
       "- Bảng t_actions không có bản ghi mới",
       note="Nguồn: r121, r448."),

    tc("エルメアクション — đăng ký & filter", "UI-001", "Normal",
       "Xem lại filter của action từ preview — mở popup filter đúng điều kiện đã đặt",
       B2 + "\n- Đã đăng ký 1 action với 絞り込みあり điều kiện có tag T",
       "1. Mở「プレビューとテスト」→ tab「アクション」\n"
       "2. Double click vào action có「絞り込みあり」\n"
       "3. Đọc điều kiện trong popup filter hiện ra",
       "Action gán tag X, filter = có tag T",
       "- Hiện popup filter\n"
       "- Điều kiện hiển thị đúng là「có tag T」",
       note="Nguồn: r228, r343, r744."),

    tc("エルメアクション — đăng ký & filter", "UI-001", "Normal",
       "Action 絞り込みなし — double click không mở được popup filter",
       B2 + "\n- Đã đăng ký 1 action với 絞り込みなし",
       "1. Mở「プレビューとテスト」→ tab「アクション」\n"
       "2. Double click vào action có「絞り込みなし」",
       "Action gán tag X, không filter",
       "- Không mở popup filter nào\n"
       "- Không có lỗi JavaScript trên console",
       note="Nguồn: r227."),

    tc("エルメアクション — đăng ký & filter", "FUNC-001", "Normal",
       "Sửa action rồi kiểm tra lại preview — nội dung cập nhật",
       B2 + "\n- Đã đăng ký 1 action gán tag X",
       "1. Mở preview tab「アクション」, ghi lại nội dung\n"
       "2. Sửa action thành gán tag Y\n"
       "3. Mở lại preview tab「アクション」",
       "Action: gán tag X → gán tag Y",
       "- Preview hiển thị action gán tag Y\n"
       "- Không còn hiển thị tag X",
       note="Nguồn: r232, r347, r748."),

    tc("エルメアクション — đăng ký & filter", "LIST-001", "Normal",
       "Danh sách action nhiều — có scroll trong khung, không vỡ layout",
       B2 + "\n- Đã đăng ký ≥15 action",
       "1. Mở preview tab「アクション」\n"
       "2. Cuộn trong khung danh sách action",
       "15 action",
       "- Danh sách có thanh cuộn riêng trong khung\n"
       "- Cuộn tới cuối vẫn đọc được action cuối cùng\n"
       "- Popup không bị tràn ra ngoài màn hình",
       note="Nguồn: r230-r231, r345-r346, r746-r747."),
]

# ═══════════ 14. Ma trận đăng ký & gửi (r24-r59 của tab master) ═══════════
# Corpus dành 36 dòng (r24-r59) cho ma trận:
#   配信タイミング (3: 送信後すぐ / 予約1time / 予約nhiều time)
#   × nguồn tin nhắn (2: メッセージ追加 / テンプレートから追加)
#   × action (3: 絞り込みなし / 絞り込みあり / không có action)
#   × 配信先 (2: すべての友だち / 絞り込み)
# Rút gọn: nguồn tin nhắn KHÔNG đổi kết quả → gộp. 配信タイミング chỉ đổi TAB đích và
# cách hiển thị thời gian → đã có TC riêng ở nhóm「配信タイミング設定」và「Tab 配信予約」.
# Còn lại 6 tổ hợp (action × 配信先) có 6 KẾT QUẢ KHÁC NHAU → 6 TC dưới đây.

MTX = ("- Đăng nhập Admin, bot có 10 bạn bè\n"
       "- Tag T gắn cho 4 friend (dùng làm 配信先絞込み)\n"
       "- Tag U gắn cho 6 friend, trong đó 3 người TRÙNG với nhóm tag T (dùng làm filter của action)\n"
       "- Đang ở màn tạo broadcast mới")
MTX_NOTE = ("Ô của ma trận r24-r59. Chạy lại TC này cho đủ 3 kiểu 配信タイミング "
            "(メッセージ登録後すぐに配信 / 配信予約 1 mốc / 配信予約 nhiều mốc) và 2 nguồn tin nhắn "
            "(メッセージ追加 / テンプレートから追加) — 6 lần chạy, kết quả về action và số người phải "
            "GIỐNG NHAU, chỉ khác tab đích và cách hiển thị thời gian. ")

S2 += [
    tc("Ma trận đăng ký & gửi", "MSG-004", "Normal",
       "Action KHÔNG filter + gửi cho すべての友だち — mọi friend nhận tin và nhận action",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, giữ「すべての友だち」\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. Đăng ký action gán tag X với「絞り込みなし」\n"
       "4. Bấm「配信内容を確認して送信に進む」\n"
       "5. Chờ job gửi xong\n"
       "6. Kiểm tra app LINE và tag X của cả 10 friend",
       "配信先 = すべての友だち (10 người) · action gán tag X, 絞り込みなし",
       "- Số 配信数 = 10 (toàn bộ bạn bè)\n"
       "- Cả 10 friend nhận được tin nhắn trong app LINE\n"
       "- Cả 10 friend đều được gán tag X",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r24, r30, r36, r42, r48, r54. RULE-06 + RULE-08.",
       group="API"),

    tc("Ma trận đăng ký & gửi", "MSG-004", "Normal",
       "Action KHÔNG filter + gửi cho nhóm đã lọc — chỉ nhóm lọc nhận tin và nhận action",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, tích「絞り込み」đặt điều kiện có tag T\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. Đăng ký action gán tag X với「絞り込みなし」\n"
       "4. Đăng ký gửi, chờ job gửi xong\n"
       "5. Kiểm tra app LINE và tag X của cả 10 friend",
       "配信先 = tag T (4 người) · action gán tag X, 絞り込みなし",
       "- Số 配信数 = 4 (đúng số người đã lọc, KHÔNG phải 10)\n"
       "- Chỉ 4 friend có tag T nhận được tin nhắn\n"
       "- Cả 4 friend đó đều được gán tag X\n"
       "- 6 friend còn lại không nhận tin, không có tag X",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r25, r31, r37, r43, r49, r55. RULE-06 + RULE-08.",
       group="API"),

    tc("Ma trận đăng ký & gửi", "MSG-004", "Normal",
       "Action CÓ filter + gửi cho すべての友だち — mọi friend nhận tin, chỉ nhóm lọc của action nhận action",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, giữ「すべての友だち」\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. Đăng ký action gán tag X với「絞り込みあり」điều kiện có tag U\n"
       "4. Đăng ký gửi, chờ job gửi xong\n"
       "5. Kiểm tra app LINE và tag X của cả 10 friend",
       "配信先 = すべての友だち (10 người) · action gán tag X, 絞り込みあり = tag U (6 người)",
       "- Số 配信数 = 10\n"
       "- Cả 10 friend nhận được tin nhắn\n"
       "- Chỉ 6 friend có tag U được gán tag X\n"
       "- 4 friend còn lại nhận tin nhưng KHÔNG có tag X",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r26, r32, r38, r44, r50, r56. RULE-06 + RULE-08.",
       group="API"),

    tc("Ma trận đăng ký & gửi", "MSG-004", "Boundary",
       "Action CÓ filter + gửi cho nhóm đã lọc — action chỉ chạy ở phần GIAO của 2 nhóm",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, tích「絞り込み」đặt điều kiện có tag T\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. Đăng ký action gán tag X với「絞り込みあり」điều kiện có tag U\n"
       "4. Đăng ký gửi, chờ job gửi xong\n"
       "5. Kiểm tra app LINE và tag X của cả 10 friend, đối chiếu với nhóm giao T∩U",
       "配信先 = tag T (4 người) · action filter = tag U (6 người) · giao nhau 3 người",
       "- Số 配信数 = 4 (theo 配信先絞込み)\n"
       "- Đúng 4 friend có tag T nhận được tin nhắn\n"
       "- Chỉ 3 friend thuộc CẢ tag T và tag U được gán tag X\n"
       "- 1 friend chỉ có tag T nhận tin nhưng KHÔNG có tag X\n"
       "- 3 friend chỉ có tag U không nhận tin và không có tag X",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r27, r33, r39, r45, r51, r57 — r27 ghi rõ điều kiện "
            "『vs đk friend phải có tên trên phần 配信先絞込み』. Đây là ô quan trọng nhất của ma trận "
            "vì thể hiện action chỉ chạy ở phần GIAO. RULE-06 + RULE-08.",
       group="API"),

    tc("Ma trận đăng ký & gửi", "MSG-001", "Normal",
       "KHÔNG có action + gửi cho すべての友だち — mọi friend chỉ nhận tin, không có action",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, giữ「すべての友だち」\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. KHÔNG đăng ký action nào\n"
       "4. Đăng ký gửi, chờ job gửi xong\n"
       "5. Kiểm tra app LINE và tag của cả 10 friend",
       "配信先 = すべての友だち (10 người) · không có action",
       "- Số 配信数 = 10\n"
       "- Cả 10 friend nhận được tin nhắn\n"
       "- KHÔNG friend nào bị gán thêm tag hay thay đổi trạng thái gì",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r28, r34, r40, r46, r52, r58. RULE-06 + RULE-08.",
       group="API"),

    tc("Ma trận đăng ký & gửi", "MSG-001", "Normal",
       "KHÔNG có action + gửi cho nhóm đã lọc — chỉ nhóm lọc nhận tin, không có action",
       MTX,
       "1. Nhập tiêu đề, chọn kiểu gửi, tích「絞り込み」đặt điều kiện có tag T\n"
       "2. Lưu bước 1, thêm 1 tin nhắn\n"
       "3. KHÔNG đăng ký action nào\n"
       "4. Đăng ký gửi, chờ job gửi xong\n"
       "5. Kiểm tra app LINE và tag của cả 10 friend",
       "配信先 = tag T (4 người) · không có action",
       "- Số 配信数 = 4\n"
       "- Chỉ 4 friend có tag T nhận được tin nhắn\n"
       "- KHÔNG friend nào bị gán thêm tag hay thay đổi trạng thái gì",
       env="PRODUCTION",
       note=MTX_NOTE + "Nguồn: r29, r35, r41, r47, r53, r59. RULE-06 + RULE-08.",
       group="API"),
]
