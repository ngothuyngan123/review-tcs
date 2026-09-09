# -*- coding: utf-8 -*-
"""FA-015 — Nhóm 3: Sửa · Copy · Xóa trường thông tin (gồm cascade khi đổi tên option).

Nguồn chính:
- 10.2 /「Change spec info type select」(12/2024, Bug #27314) r3-r84 — cascade option select 7 bảng.
- 10.2 /「test fix bug」khối Bug KH #34625 (02/2026) r162-r195 — copy friend info các kiểu.
- 10.2 /「test fix bug」khối Bug KH #37606 (06/2026) r231-r273 — action mồ côi khi xóa tag.
"""
from _common import tc

ADM = "- Đăng nhập admin bot A (plan có phí), mở /basic/friend-information"

S3 = [
    # ══════════════════ Sửa info ══════════════════
    tc("Sửa info", "FUNC-001", "Normal",
       "Mở màn edit → hiển thị đúng dữ liệu đã lưu của trường (mọi kiểu)",
       ADM + "\n- Có sẵn 4 trường: 選択肢 (3 option có action), 記述, 年月日 (có setting lịch), ポイント (2 ngưỡng)",
       "1. Click 管理名 của từng trường để vào màn edit\n2. Đối chiếu 管理名, folder, 情報タイプ, khối cấu hình riêng\n"
       "3. Chụp màn hình từng màn edit",
       "4 trường, 4 kiểu",
       "- Mỗi màn edit hiển thị đúng 管理名, đúng folder, đúng 情報タイプ (disabled)\n"
       "- 選択肢: đủ 3 option đúng thứ tự, mỗi option hiện preview action đã gắn\n"
       "- 年月日: đúng 登録 (月日/年月日), số ngày, 前/後, giờ\n- ポイント: đủ 2 ngưỡng và action",
       note="Nguồn: spec EP-07 initDataInfo + corpus r291 (check lại màn edit)."),

    tc("Sửa info", "FUNC-001", "Normal",
       "Đổi 管理名 → cập nhật ở màn list và ở preview action của các tính năng đang tham chiếu",
       ADM + "\n- Trường「予約プラン」kiểu 選択肢 đang được dùng làm action ở 1 auto-reply và 1 richmenu",
       "1. Ghi lại text preview action ở auto-reply và richmenu\n"
       "2. Vào màn edit đổi 管理名 thành「予約プラン2026」→ lưu\n3. Đọc lại màn list\n"
       "4. Mở lại auto-reply và richmenu, đọc preview action",
       "管理名: 予約プラン → 予約プラン2026",
       "- Màn list hiển thị 管理名 mới\n"
       "- Preview action ở auto-reply và richmenu hiển thị tên MỚI「予約プラン2026」\n"
       "- Action vẫn trỏ đúng trường cũ (chạy thử vẫn ghi giá trị vào đúng trường)",
       note="Spec BR-11. Nguồn: ModalAction /「Update tên action」(04/2025) + spec feature-spec §SCR-FRI-02."),

    tc("Sửa info", "FUNC-001", "Normal",
       "Đổi folder của trường ở màn edit → trường chuyển folder, count 2 folder cập nhật",
       ADM + "\n- Trường I1 đang ở folder A (folder A có 3 trường, folder B có 1 trường)",
       "1. Ghi lại count A và B\n2. Vào edit I1, đổi dropdown folder sang B → lưu\n"
       "3. Đọc count ở panel trái\n4. Click vào A và B kiểm tra danh sách",
       "I1: folder A → folder B",
       "- Count: A = 2, B = 2\n- I1 xuất hiện trong B, không còn trong A\n"
       "- 回答人数 và giá trị bạn bè của I1 không đổi",
       note="Nguồn: r216 (#36201)."),

    tc("Sửa info", "FUNC-001", "Normal",
       "Thêm option mới vào trường 選択肢 đã có bạn dùng → option mới xuất hiện, giá trị cũ không đổi",
       ADM + "\n- Trường 選択肢 có 2 option A, B; U1 =「A」, U2 =「B」",
       "1. Vào edit, thêm option C → lưu\n2. Mở 友だち詳細 của U1, U2 xem giá trị\n"
       "3. Mở danh sách chọn của trường ở 友だち詳細\n4. Gán C cho U3\n5. Đọc 回答人数",
       "Thêm option C, gán C cho U3",
       "- Danh sách chọn có đủ A, B, C\n- U1 vẫn「A」, U2 vẫn「B」\n"
       "- U3 =「C」, 回答人数 tăng từ 2 lên 3",
       note="Nguồn: tab「Change spec info type select」r3 + r39-r48 (add option → các màn setting cập nhật)."),

    tc("Sửa info", "DATA-REF-001", "Normal",
       "Đổi TEXT của option → giá trị của bạn đang giữ option đó đổi theo (không mất bản ghi)",
       ADM + "\n- Trường 選択肢 có option「プランA」; U1 và U2 đang giữ「プランA」",
       "1. Ghi lại 回答人数 và giá trị của U1, U2\n2. Vào edit đổi option thành「プランA-2026」→ lưu\n"
       "3. Mở 友だち詳細 của U1, U2\n4. Mở right bar chat 1:1 của U1\n5. Đọc lại 回答人数",
       "「プランA」→「プランA-2026」",
       "- U1 và U2 hiển thị giá trị mới「プランA-2026」ở cả 友だち詳細 và right bar\n"
       "- 回答人数 KHÔNG đổi (vẫn 2人)\n- Không sinh thêm bản ghi giá trị nào",
       note="Đây là lõi Bug #27314 (12/2024 — trước fix, giá trị của bạn vẫn giữ text cũ). "
            "Nguồn: tab「Change spec info type select」r4, r23."),

    tc("Sửa info", "REG-SHARED-001", "Normal",
       "Đổi text option → cập nhật đồng bộ ở TẤT CẢ nơi tham chiếu (form, booking, item, action, filter)",
       ADM + "\n- Trường 選択肢「予約プラン」với option「プランA」đang được tham chiếu ở:\n"
       "  form answer · booking calendar · booking event · lesson · salon · item · modal action · modal filter",
       "1. Ghi lại text option hiển thị ở 8 nơi tham chiếu\n"
       "2. Ở màn friend information đổi option thành「プランA-2026」→ lưu\n"
       "3. Mở lại lần lượt 8 nơi và đọc text option",
       "8 điểm tham chiếu: form answer, booking calendar, booking event, lesson, salon, item, modal action, modal filter",
       "- Cả 8 nơi đều hiển thị text MỚI「プランA-2026」\n"
       "- Không nơi nào còn text cũ, không nơi nào bị mất option",
       note="8 điểm cùng 1 kết quả nên gộp 1 TC. Spec BR-09 (cascade 7 bảng). "
            "Nguồn: tab「Change spec info type select」r49-r58."),

    tc("Sửa info", "REG-SHARED-001", "Abnormal",
       "Xóa option ở màn friend information → option biến mất ở tất cả nơi tham chiếu",
       ADM + "\n- Như TC trên: option「プランA」được tham chiếu ở 8 nơi",
       "1. Xóa option「プランA」ở màn edit trường → lưu\n"
       "2. Mở lại lần lượt 8 nơi tham chiếu\n3. Kiểm tra bạn đang giữ option đó",
       "Xóa option đang được 8 nơi tham chiếu",
       "- Cả 8 nơi không còn option「プランA」trong danh sách chọn\n"
       "- Không nơi nào văng lỗi khi mở\n"
       "- Bạn đang giữ「プランA」mất giá trị, 回答人数 giảm tương ứng",
       note="Nguồn: tab「Change spec info type select」r24, r59-r68."),

    tc("Sửa info", "REG-SHARED-001", "Normal",
       "Thêm option mới → option xuất hiện ở tất cả nơi tham chiếu để chọn",
       ADM + "\n- Trường 選択肢「予約プラン」đang được tham chiếu ở 8 nơi (như TC trên)",
       "1. Thêm option「プランD」ở màn edit trường → lưu\n"
       "2. Mở lần lượt 8 nơi tham chiếu và mở danh sách chọn option",
       "Thêm 1 option mới",
       "- Cả 8 nơi đều có「プランD」trong danh sách chọn\n"
       "- Các option cũ vẫn còn nguyên, đúng thứ tự",
       note="Nguồn: tab「Change spec info type select」r39-r48."),

    tc("Sửa info", "REG-SHARED-001", "Normal",
       "Sửa option ở màn setting form nhập của lesson/salon (loại info tự gen) → đồng bộ ngược về trường friend info",
       ADM + "\n- Có lesson và salon dùng form nhập với item map tới friend info kiểu 選択肢 (loại tự gen)",
       "1. Ở màn setting form nhập của lesson, sửa text 1 option → lưu\n"
       "2. Mở màn friend information kiểm tra option của trường\n"
       "3. Kiểm tra giá trị của bạn đang giữ option đó\n4. Lặp lại toàn bộ với salon",
       "Lesson + Salon, mỗi bên 1 option đổi text",
       "- Option ở màn friend information đổi theo text mới\n"
       "- Giá trị của bạn đang giữ option đó đổi theo, không mất bản ghi\n"
       "- Cả 2 chiều (lesson và salon) đều đồng bộ",
       note="⚠️ Corpus r34 (salon) ĐANG ĐÁNH DẤU 'NG' cho vế update giá trị bạn bè — xem MT-04. "
            "Nguồn: tab「Change spec info type select」r30, r34."),

    tc("Sửa info", "REG-SHARED-001", "Normal",
       "Xóa option ở màn setting form nhập của lesson/salon → xóa đồng bộ về trường friend info",
       ADM + "\n- Như TC trên",
       "1. Ở màn setting form nhập của lesson, xóa 1 option → lưu\n"
       "2. Kiểm tra option ở màn friend information\n3. Kiểm tra bạn đang giữ option đó\n"
       "4. Lặp lại với salon",
       "Lesson + Salon, mỗi bên xóa 1 option",
       "- Option biến mất ở màn friend information\n"
       "- Bạn đang giữ option đó mất giá trị, 回答人数 giảm\n- Không màn nào văng lỗi",
       note="Nguồn: tab「Change spec info type select」r31, r35."),

    tc("Sửa info", "FUNC-001", "Normal",
       "Sort option nhưng KHÔNG sửa text → dữ liệu option và giá trị bạn bè không thay đổi",
       ADM + "\n- Trường 選択肢 có 3 option, mỗi option có ≥ 1 bạn đang giữ",
       "1. Ghi lại 回答人数 và giá trị từng bạn\n2. Vào edit, đổi thứ tự 3 option (không sửa text) → lưu\n"
       "3. Mở lại 友だち詳細 của các bạn\n4. Đọc lại 回答人数",
       "Đảo thứ tự 3 option",
       "- Giá trị của mọi bạn giữ nguyên như trước khi sort\n- 回答人数 không đổi\n"
       "- Thứ tự option ở danh sách chọn theo đúng thứ tự mới",
       note="Nguồn: tab「Change spec info type select」r6 ('sort option (không edit text) ⇒ không update bảng')."),

    tc("Sửa info", "DATA-REF-001", "Normal",
       "Đổi action gắn cho option → action mới chạy, action cũ không còn chạy",
       ADM + "\n- Trường 選択肢, option A đang gắn action gửi text T1\n- Bạn U1 chưa có giá trị",
       "1. Vào edit, đổi action của option A sang gửi text T2 → lưu\n"
       "2. Gán option A cho U1\n3. Kiểm tra LINE app của U1",
       "Action: T1 → T2",
       "- U1 nhận đúng text T2\n- U1 KHÔNG nhận T1\n- Preview action ở màn edit hiển thị T2",
       note="RULE-06. Nguồn: tab「Change spec info type select」r5 + spec BR-03."),

    tc("Sửa info", "DATA-REF-001", "Abnormal",
       "Xóa TAG đang được gắn làm action trong option → mở màn edit trường KHÔNG báo lỗi, action con bị dọn",
       ADM + "\n- Trường 選択肢「予約済みのプラン」có 3 option, mỗi option gắn 1 action tag khác nhau",
       "1. Ở màn quản lý tag, xóa tag được gắn ở option ĐẦU TIÊN\n"
       "2. Quay lại màn friend information, click vào 管理名 để mở màn edit\n"
       "3. Quan sát có alert lỗi không\n4. Đọc preview action của 3 option\n"
       "5. Lặp lại với tag ở option GIỮA, option CUỐI, và xóa NHIỀU tag (không xóa hết)",
       "4 nhánh: xóa action đầu / giữa / cuối / nhiều action",
       "- Màn edit mở bình thường, KHÔNG hiển thị alert lỗi\n"
       "- Option có tag bị xóa: không còn hiển thị action đó\n"
       "- Các option còn lại vẫn hiển thị action đúng như trước",
       note="Bug KH #37606 (06/2026 — lỗi \"Trying to get property 'details' of non-object\"). "
            "Nguồn: r231-r234."),

    tc("Sửa info", "DATA-REF-001", "Abnormal",
       "Xóa HẾT tag được gắn trong trường → màn edit vẫn mở được, không còn action nào hiển thị",
       ADM + "\n- Trường 選択肢 có 3 option, cả 3 gắn action tag",
       "1. Xóa toàn bộ 3 tag ở màn quản lý tag\n2. Mở màn edit của trường\n"
       "3. Quan sát alert và preview action",
       "Xóa 3/3 tag",
       "- Màn edit mở bình thường, không alert lỗi\n- Không option nào hiển thị action tag nữa\n"
       "- Trường vẫn lưu/sửa được bình thường",
       note="Nguồn: r235, r247, r259 (#37606)."),

    tc("Sửa info", "DATA-REF-001", "Normal",
       "Xóa tag KHÔNG liên quan → trường friend info không bị ảnh hưởng, không bị clean nhầm",
       ADM + "\n- Trường 選択肢 có option gắn action tag A\n- Có thêm tag B không được dùng ở đâu",
       "1. Tạo tag B rồi xóa tag B\n2. Mở màn edit của trường\n3. Đọc preview action của option",
       "Xóa tag B (không liên quan)",
       "- Option vẫn giữ nguyên action tag A\n- Màn edit không báo lỗi\n"
       "- Gán option cho 1 bạn → tag A vẫn được gắn đúng",
       note="Đối chứng âm. Nguồn: r239, r251, r263 (#37606)."),

    tc("Sửa info", "DATA-REF-001", "Abnormal",
       "Xóa tag đang gắn rồi KHÔI PHỤC lại tag đó → trường không tự lấy lại action đã dọn",
       ADM + "\n- Trường 選択肢 có option gắn action tag A",
       "1. Xóa tag A\n2. Khôi phục tag A từ màn tag đã xóa\n3. Mở màn edit của trường\n"
       "4. Đọc preview action của option",
       "Xóa rồi khôi phục tag A",
       "- Màn edit mở bình thường, không báo lỗi\n"
       "- Option KHÔNG hiển thị lại action tag A (action con đã bị dọn khi xóa tag)\n"
       "- Tag A tồn tại trở lại ở màn quản lý tag",
       note="Nguồn: r240, r252, r264 (#37606)."),

    tc("Sửa info", "CONC-002", "Abnormal",
       "User A đang mở màn edit trường, User B xóa tag đang gắn → A reload không crash",
       "- 2 tài khoản admin cùng bot A\n- Trường 選択肢 có option gắn action tag A",
       "1. User A mở màn edit của trường\n2. User B xóa tag A ở màn quản lý tag\n"
       "3. User A reload màn edit\n4. User A bấm lưu",
       "2 người thao tác đồng thời",
       "- Màn edit của A sau reload hiển thị bình thường, không crash/alert lỗi\n"
       "- Không còn action tag A ở option\n- User A lưu được, các option khác không bị mất",
       note="Nguồn: r241, r253, r265 (#37606)."),

    tc("Sửa info", "DATA-REF-001", "Abnormal",
       "Xóa các loại đối tượng khác đang gắn làm action (kịch bản, richmenu, template, remind, trạng thái chat, friend info khác) "
       "→ màn edit không lỗi, action còn lại vẫn chạy",
       ADM + "\n- Trường 選択肢 với các option gắn action: kịch bản + tag, richmenu + tag, template + tag, "
       "remind, trạng thái chat, friend info khác",
       "1. Lần lượt xóa từng đối tượng gốc (kịch bản / richmenu / template / remind / trạng thái chat / friend info)\n"
       "2. Sau mỗi lần, mở màn edit và đọc preview action\n"
       "3. Gán option tương ứng cho 1 bạn và kiểm tra LINE app",
       "6 loại đối tượng",
       "- Màn edit mở bình thường sau mỗi lần xóa, không alert lỗi\n"
       "- Option không còn hiển thị action của đối tượng đã xóa\n"
       "- Option vẫn giữ action tag đi kèm (nếu có) và action tag đó VẪN chạy khi bạn chọn option\n"
       "- Với option chỉ có 1 action đã bị xóa: bạn chọn option không nhận action nào",
       note="6 điểm cùng 1 kết quả nên gộp 1 TC. Nguồn: r267-r272 (#37606)."),

    tc("Sửa info", "DATA-REF-001", "Normal",
       "Trường 年月日 / ポイント có action tag bị xóa → hành vi giống trường 選択肢",
       ADM + "\n- 1 trường 年月日 và 1 trường ポイント, mỗi trường có action gắn tag",
       "1. Xóa tag đang gắn\n2. Mở màn edit của trường 年月日 → quan sát\n"
       "3. Mở màn edit của trường ポイント → quan sát\n4. Kiểm tra các action còn lại",
       "2 trường × xóa tag",
       "- Cả 2 màn edit mở bình thường, không alert lỗi\n"
       "- Không còn hiển thị action tag đã xóa\n- Các action khác hiển thị và chạy bình thường",
       note="Nguồn: r243-r266 (#37606 mở rộng cho type date và point)."),

    tc("Sửa info", "PERM-001", "Abnormal",
       "Account staff sửa trường thông tin → theo đúng quyền được cấp",
       "- Tài khoản staff có quyền xem nhưng KHÔNG có quyền sửa màn friend information",
       "1. Đăng nhập staff, mở màn friend information (nếu có quyền xem)\n"
       "2. Thử mở màn edit 1 trường\n3. Thử bấm lưu\n4. Ghi lại hành vi thực tế",
       "Staff quyền xem, không quyền sửa",
       "- Ghi nhận thực tế: staff có vào được màn edit không, có lưu được không\n"
       "- Nếu không có quyền: hiển thị message quyền, không lưu được thay đổi",
       spec="Đã hỏi leader",
       note="⚠️ Spec Gap #2: chưa xác nhận cơ chế phân quyền cho FA-015 — xem MT-12. "
            "Corpus có dòng 'Check account staff' (r273, r499, r574) nhưng KHÔNG có kết quả mong đợi → expected do AI viết."),

    # ══════════════════ Copy info ══════════════════
    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 年月日 CÓ cấu hình lịch → bản copy giống bản gốc trên GUI, action là action mới",
       ADM + "\n- Trường 年月日「誕生日案内」có ≥ 1 dòng cấu hình lịch + action, đang có 2 bạn có giá trị",
       "1. Thực hiện copy trường (lặp 3 lần liên tiếp: copy lần 1, 2, 3)\n"
       "2. Với mỗi bản copy: mở màn edit và so sánh từng mục với bản gốc\n"
       "3. Kiểm tra 回答人数 của bản copy\n4. Mở lại bản gốc kiểm tra không đổi",
       "Copy 3 lần từ cùng 1 trường gốc",
       "- Cả 3 lần copy thành công, KHÔNG hiển thị lỗi\n"
       "- Màn edit bản copy hiển thị giống hệt bản gốc: 情報タイプ, 登録 (月日/年月日), số ngày, 前/後, giờ, action\n"
       "- 回答人数 của bản copy =「0人」\n- Bản gốc giữ nguyên toàn bộ thông tin và 回答人数",
       note="Bug KH #34625 (02/2026 — copy friend info dạng datetime báo lỗi \"Undefined property: stdClass::$value\"). "
            "Nguồn: r162-r164."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 年月日 rồi ĐỔI FOLDER đích → bản copy nằm đúng folder mới",
       ADM + "\n- Trường 年月日 ở folder A, tồn tại folder B",
       "1. Copy trường, ở màn copy đổi folder sang B\n2. Lưu\n3. Về màn list kiểm tra folder A và B",
       "Copy từ folder A → lưu vào folder B",
       "- Bản copy nằm trong folder B, count B tăng 1\n- Bản gốc vẫn ở folder A, count A không đổi",
       note="Nguồn: r165 (#34625)."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 年月日 KHÔNG có cấu hình lịch → vẫn copy thành công",
       ADM + "\n- Trường 年月日 chưa cấu hình action/lịch nào",
       "1. Copy trường (lặp 2 lần)\n2. Mở màn edit bản copy so sánh với bản gốc",
       "Copy 2 lần",
       "- Cả 2 lần copy thành công, không lỗi\n- Bản copy giống bản gốc, không có cấu hình lịch\n"
       "- 回答人数 bản copy = 0人",
       note="Nguồn: r166-r167 (#34625)."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy rồi SỬA dữ liệu ngay tại màn copy → chỉ bản copy đổi, bản gốc không đổi",
       ADM + "\n- Trường 年月日「誕生日案内」có cấu hình lịch",
       "1. Bấm copy\n2. Tại màn copy đổi 管理名, đổi số ngày, đổi giờ, đổi action\n3. Lưu\n"
       "4. Mở màn edit bản gốc và đối chiếu từng mục",
       "Bản copy: 管理名「誕生日案内-2」, số ngày 3 → 7, giờ 09:00 → 18:00",
       "- Bản copy lưu đúng các giá trị vừa sửa\n"
       "- Bản gốc GIỮ NGUYÊN 管理名, số ngày 3, giờ 09:00 và action cũ",
       note="Nguồn: r168, r177-r178 (#34625)."),

    tc("Copy info", "JOB-001", "Normal",
       "Bản copy của trường 年月日 vẫn gửi action đúng khi tới mốc (cả chiều trước và sau)",
       "- Đã copy 1 trường 年月日 có cấu hình lịch\n- Gán giá trị cho U1 (bản gốc) và U2 (bản copy)",
       "1. Bản gốc cấu hình gửi TRƯỚC N ngày, bản copy gửi SAU N ngày\n"
       "2. Gán giá trị cho U1 ở bản gốc, U2 ở bản copy\n"
       "3. Chờ qua cả 2 mốc, kiểm tra LINE app của U1 và U2",
       "U1 (gốc, gửi trước 2 ngày) · U2 (copy, gửi sau 2 ngày)",
       "- U1 nhận action đúng mốc trước 2 ngày\n- U2 nhận action đúng mốc sau 2 ngày\n"
       "- 2 action độc lập, không bạn nào nhận nhầm cấu hình của bên kia",
       env="PRODUCTION",
       note="RULE-08 (job). Nguồn: r169-r172 (#34625)."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 選択肢 → option và action của option được nhân bản, là action MỚI (không dùng chung)",
       ADM + "\n- Trường 選択肢 có 3 option, mỗi option gắn action tag khác nhau",
       "1. Copy trường (2 lần)\n2. Mở màn edit bản copy: đếm option và đọc preview action\n"
       "3. Ở BẢN COPY, đổi action của option 1 sang tag khác → lưu\n"
       "4. Mở lại BẢN GỐC đọc preview action của option 1",
       "Copy 2 lần, sau đó sửa action ở bản copy",
       "- Bản copy có đủ 3 option đúng text và đúng thứ tự, mỗi option có action tương ứng\n"
       "- Sửa action ở bản copy KHÔNG làm đổi action của bản gốc (action là bản ghi mới)",
       note="Nguồn: r175-r176 (#34625 — 'Check case setting action của info select ⇒ phải tạo ra action_id mới')."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 選択肢 rồi gán giá trị cho bạn ở bản copy → giá trị độc lập với bản gốc",
       ADM + "\n- Trường 選択肢 gốc có U1 đang giữ option A\n- Đã copy thành trường mới",
       "1. Gán option A của BẢN COPY cho U1\n2. Mở 友だち詳細 của U1\n"
       "3. Đọc 回答人数 của bản gốc và bản copy",
       "U1 có giá trị ở cả 2 trường",
       "- 友だち詳細 của U1 hiển thị 2 dòng: 1 của trường gốc, 1 của trường copy\n"
       "- 回答人数 bản gốc và bản copy đều tính riêng, mỗi bên tăng đúng phần của mình",
       note="Nguồn: r173 (#34625)."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường kiểu ポイント / 記述 / 画像 / PDF → copy thành công, gán giá trị được",
       ADM + "\n- Có sẵn 4 trường kiểu ポイント, 記述, 画像, PDF",
       "1. Copy từng trường, mỗi trường lặp 3 lần\n2. Mở màn edit từng bản copy so với bản gốc\n"
       "3. Gán giá trị cho 1 bạn ở mỗi bản copy\n4. Đọc 回答人数",
       "4 kiểu × 3 lần copy = 12 bản copy",
       "- Cả 12 lần copy thành công, không lỗi\n- Bản copy giống bản gốc về cấu hình, 回答人数 = 0人 lúc mới copy\n"
       "- Gán giá trị được cho bạn ở mọi bản copy, 回答人数 tăng đúng",
       note="4 kiểu cùng 1 kết quả nên gộp 1 TC. Nguồn: r180-r194 (#34625)."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường có nhiều action điểm → preview action ở bản copy hiển thị đúng",
       ADM + "\n- Trường 選択肢 có option gắn nhiều action điểm (ghi đè / cộng / trừ)",
       "1. Copy trường\n2. Mở màn edit bản copy\n3. Đọc toàn bộ preview action của từng option",
       "Trường có ≥ 3 action điểm khác loại",
       "- Preview action ở bản copy hiển thị đúng từng loại (登録 / プラス / マイナス) và đúng số điểm\n"
       "- Không action nào bị mất hoặc hiển thị sai loại",
       note="Nguồn: r304 (#38469 — 'Check copy friend info có chứa action point')."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường có action gắn trường friend info KHÁC → sau khi xóa trường đích, preview bản copy vẫn không lỗi",
       ADM + "\n- Trường I1 có action ghi giá trị vào trường I2 (kiểu ポイント)",
       "1. Copy I1 thành I1-copy\n2. Xóa trường I2\n3. Mở màn edit I1-copy và I1\n"
       "4. Đọc preview action",
       "Xóa trường đích I2 sau khi copy",
       "- Cả 2 màn edit mở bình thường, không alert lỗi\n"
       "- Action trỏ tới I2 không còn hiển thị ở cả bản gốc và bản copy",
       note="Nguồn: r305 (#38469 — 'Check xóa friend info point => check lại preview action')."),

    tc("Copy info", "UI-INPUT-001", "Normal",
       "管理名 của bản copy: quy tắc đặt tên và giới hạn 20 ký tự",
       ADM + "\n- Trường gốc có 管理名 dài 20 ký tự",
       "1. Bấm copy\n2. Quan sát 管理名 mặc định ở màn copy (có hậu tố copy không, có vượt 20 ký tự không)\n"
       "3. Lưu và đọc 管理名 ở màn list",
       "管理名 gốc = 20 ký tự",
       "- Ghi nhận quy tắc đặt tên mặc định của bản copy\n"
       "- 管理名 bản copy KHÔNG vượt quá 20 ký tự\n- Lưu thành công",
       spec="Spec không ghi",
       note="⚠️ Spec BR-05 không nói quy tắc đặt tên bản copy — xem MT-10. TC do AI bổ sung."),

    tc("Copy info", "FUNC-001", "Normal",
       "Copy trường 選択肢 rồi XÓA bản copy → bản gốc và giá trị bạn bè không bị ảnh hưởng",
       ADM + "\n- Trường gốc có 3 option, U1 đang giữ option A\n- Đã copy thành 1 trường mới",
       "1. Xóa bản copy ở màn list\n2. Mở màn edit bản gốc\n3. Mở 友だち詳細 của U1\n"
       "4. Đọc 回答人数 của bản gốc",
       "Xóa bản copy",
       "- Bản gốc còn nguyên 3 option và action\n- U1 vẫn giữ option A\n"
       "- 回答人数 bản gốc không đổi",
       note="Nguồn: r174, r179, r183, r187, r191, r195 (#34625 — 'check xóa' sau copy)."),

    tc("Copy info", "SEC-ISO-001", "Abnormal",
       "Copy trường bằng URL copy với id thuộc BOT KHÁC → không copy được",
       "- Tài khoản admin bot A\n- Biết id 1 trường friend info của bot B",
       "1. Đăng nhập bot A\n2. Gõ URL /basic/friend-information/copy/{id của bot B}\n"
       "3. Nếu mở được form thì bấm lưu\n4. Kiểm tra màn list bot A và bot B",
       "id trường của bot B",
       "- Không mở được form copy (báo lỗi/không tìm thấy) HOẶC không lưu được\n"
       "- Bot A không xuất hiện trường của bot B\n- Trường của bot B không bị sửa đổi",
       note="TC do AI bổ sung theo SEC-ISO-001 (spec EP-04 có route copy). Cần Leader xác nhận."),

    # ══════════════════ Xóa info ══════════════════
    tc("Xóa info", "FUNC-001", "Normal",
       "Xóa 1 trường thông tin → biến mất khỏi màn list, count folder giảm",
       ADM + "\n- Folder A có 3 trường",
       "1. Ghi lại count folder A\n2. Xóa 1 trường và xác nhận\n3. Reload màn list\n"
       "4. Đọc count folder A",
       "Xóa 1/3 trường",
       "- Trường biến mất khỏi bảng, không quay lại sau reload\n- Count folder A = 2\n"
       "- 2 trường còn lại giữ nguyên thứ tự và 回答人数",
       note="Nguồn: r212 (#36201) + spec EP-06 action=deleteItem."),

    tc("Xóa info", "DATA-REF-001", "Abnormal",
       "Xóa trường có giá trị bạn bè → giá trị bị dọn ở 友だち詳細, right bar chat 1:1 và màn danh sách câu trả lời",
       ADM + "\n- Trường I1 có 3 bạn đang có giá trị, đang được bật hiển thị ở right bar chat 1:1",
       "1. Ghi lại 回答人数 và danh sách 3 bạn\n2. Xóa trường I1\n"
       "3. Mở 友だち詳細 của 3 bạn\n4. Mở right bar chat 1:1 của 1 bạn\n"
       "5. Thử mở URL màn danh sách câu trả lời của I1",
       "3 bạn có giá trị",
       "- 友だち詳細 của cả 3 bạn không còn dòng của trường I1\n"
       "- Right bar chat 1:1 không còn I1\n"
       "- Mở URL màn danh sách câu trả lời của I1 báo không tồn tại (không văng lỗi hệ thống)",
       note="Spec BR-06 cascade (5 bảng). Expected ở tầng UI do AI viết từ corpus khối cascade."),

    tc("Xóa info", "DATA-REF-001", "Abnormal",
       "Xóa trường đang được dùng làm ACTION ở tính năng khác → action đó bị dọn, màn tính năng đó không lỗi",
       ADM + "\n- Trường I1 đang được dùng làm action ở: auto-reply, richmenu, form, booking event",
       "1. Xóa trường I1\n2. Mở lần lượt 4 màn tính năng trên\n"
       "3. Đọc preview action ở từng màn\n4. Kích hoạt thử 1 action (vd bạn nhập keyword auto-reply)",
       "4 tính năng tham chiếu",
       "- Cả 4 màn mở bình thường, không alert lỗi\n"
       "- Action trỏ tới I1 không còn hiển thị\n"
       "- Kích hoạt action: bạn không nhận action của I1, các action khác trong cùng cụm vẫn chạy",
       note="Spec BR-06 mục 1 (xóa t_actions_detail type='friend_info'). Nguồn: r270, r305."),

    tc("Xóa info", "DATA-REF-001", "Abnormal",
       "Xóa trường đang được dùng trong FILTER → filter đó không còn điều kiện friend info, màn filter không lỗi",
       ADM + "\n- Có 1 broadcast và 1 auto-reply dùng filter theo trường I1",
       "1. Ghi lại điều kiện filter hiện tại của 2 tính năng\n2. Xóa trường I1\n"
       "3. Mở lại modal filter của broadcast và auto-reply\n4. Bấm xem số bạn thỏa mãn filter",
       "2 tính năng dùng filter theo I1",
       "- Modal filter mở bình thường, không alert lỗi\n"
       "- Không còn điều kiện trỏ tới I1 (hoặc hiển thị rõ điều kiện đã mất hiệu lực)\n"
       "- Số bạn thỏa mãn filter tính lại được, không báo lỗi truy vấn",
       spec="Spec không ghi",
       note="⚠️ Spec BR-06 KHÔNG liệt kê dọn filter_v2 khi xóa trường (chỉ có cascade khi ĐỔI TÊN option, BR-09) — "
            "xem MT-13. TC do AI bổ sung."),

    tc("Xóa info", "JOB-001", "Abnormal",
       "Xóa trường 年月日 đang có lịch gửi → lịch bị dọn, bạn không nhận action mồ côi",
       "- Trường 年月日 có 2 bạn đã sinh lịch gửi trong tương lai gần\n"
       "- Có 1 trường 年月日 khác cũng có lịch (đối chứng)",
       "1. Ghi lại mốc gửi dự kiến của 2 bạn\n2. Xóa trường 年月日 thứ nhất\n"
       "3. Chờ qua mốc gửi cũ, kiểm tra LINE app 2 bạn\n"
       "4. Chờ mốc của trường đối chứng, kiểm tra LINE app bạn thuộc trường đó",
       "2 bạn ở trường bị xóa · 1 bạn ở trường đối chứng",
       "- 2 bạn thuộc trường đã xóa KHÔNG nhận action nào\n"
       "- Bạn thuộc trường đối chứng VẪN nhận action đúng giờ\n- Job không lỗi",
       env="PRODUCTION",
       note="RULE-08 (job). Spec BR-06 mục 6 ghi 'implicit' — xem MT-09. Nguồn: r390 ('Check xóa action info ⇒ "
            "xóa record trong bảng event_step_time')."),

    tc("Xóa info", "STATE-CLEAN-001", "Normal",
       "Xóa trường rồi TẠO trường mới cùng 管理名 → trường mới sạch, không kế thừa giá trị cũ",
       ADM + "\n- Trường「予約プラン」có 3 bạn có giá trị",
       "1. Xóa trường「予約プラン」\n2. Tạo trường mới cùng tên「予約プラン」, cùng kiểu, cùng folder\n"
       "3. Đọc 回答人数 của trường mới\n4. Mở 友だち詳細 của 3 bạn cũ",
       "Tạo lại cùng 管理名 sau khi xóa",
       "- 回答人数 của trường mới =「0人」\n"
       "- 3 bạn cũ không có giá trị ở trường mới\n- Màn list không hiển thị 2 trường trùng tên",
       note="Nguồn: r213, r224 (#36201: xóa → tạo mới). Vế 'không kế thừa' do AI viết."),

    tc("Xóa info", "FUNC-001", "Abnormal",
       "Hủy hộp thoại xác nhận xóa → trường không bị xóa",
       ADM + "\n- Folder A có 3 trường",
       "1. Bấm xóa 1 trường\n2. Ở hộp thoại xác nhận bấm hủy\n3. Reload màn list\n4. Đọc count folder A",
       "Hủy xác nhận",
       "- Trường vẫn còn trong danh sách\n- Count folder A = 3\n- Giá trị bạn bè không bị đụng",
       note="TC do AI bổ sung theo FUNC-001, cần Leader xác nhận có hộp thoại xác nhận hay không."),

    tc("Xóa info", "CONC-001", "Abnormal",
       "2 tab cùng mở màn list, tab A xóa trường, tab B bấm xóa lại trường đó → không lỗi hệ thống",
       ADM + "\n- Mở màn list ở 2 tab trình duyệt",
       "1. Tab A xóa trường I1\n2. Tab B (chưa reload) bấm xóa I1\n3. Quan sát thông báo ở tab B\n"
       "4. Reload cả 2 tab",
       "Xóa trùng 1 trường từ 2 tab",
       "- Tab B hiển thị thông báo hợp lý (đã bị xóa / không tìm thấy), KHÔNG văng lỗi hệ thống\n"
       "- Sau reload, cả 2 tab đều không còn I1\n- Không trường nào khác bị xóa nhầm",
       note="TC do AI bổ sung theo CONC-001, cần Leader xác nhận message."),

    tc("Xóa info", "SEC-001", "Abnormal",
       "Gọi trực tiếp API xóa trường với id thuộc bot khác → không xóa nhầm",
       "- Tài khoản admin bot A\n- Biết id trường friend info của bot B",
       "1. Ở bot A thực hiện xóa 1 trường và bắt request\n"
       "2. Gửi lại request với item_id là id trường của bot B\n"
       "3. Kiểm tra màn list của bot B",
       "item_id = id trường bot B",
       "- Request bị từ chối\n- Trường của bot B còn nguyên cùng toàn bộ giá trị và 回答人数",
       note="TC do AI bổ sung theo SEC-001, cần Leader xác nhận (liên quan spec Gap #2)."),

    tc("Xóa info", "DATA-REF-001", "Normal",
       "Xóa trường 選択肢 → toàn bộ option của trường bị dọn, không còn xuất hiện ở nơi tham chiếu",
       ADM + "\n- Trường 選択肢 có 3 option đang được tham chiếu ở form answer và modal filter",
       "1. Xóa trường\n2. Mở màn setting form answer đang map tới trường này\n"
       "3. Mở modal filter của 1 broadcast\n4. Quan sát danh sách trường/option còn lại",
       "3 option, 2 nơi tham chiếu",
       "- Không nơi nào còn hiển thị 3 option của trường đã xóa\n"
       "- Trường không còn trong danh sách chọn friend info\n- Cả 2 màn mở bình thường",
       note="Nguồn: tab「Change spec info type select」r69-r71 ('xóa 1 item / xóa nhiều item / xóa folder ⇒ "
            "xóa bản ghi friend_info_option_select')."),
]
