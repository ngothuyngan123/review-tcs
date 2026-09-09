# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 20-21: Preview & send test step · Send test 一括テスト.

Nguồn: tab「Testcase」(master) · tab「2/12」(send test theo 3 option)
· tab「Job scenario」(Bug KH #34489 03/2026 — thứ tự gửi khi send test).
"""
from _common import tc

STEP = ("- Đăng nhập admin (主管理者), bot A\n- Scenario S1 có step「02時間00分後」với 3 message "
        "(text / image / button quick reply) và 2 action")
PREV = STEP + "\n- Đang mở popup preview & send test của step"

S4 = [
    # ══════════════════ 20. Preview & send test step ══════════════════
    tc("Preview & send test step", "UI-001", "Normal",
       "Icon preview message: đúng design; double click → chỉ mở 1 màn preview/send test",
       STEP,
       "1. Quan sát icon preview của 1 message\n2. Double click nhanh icon preview\n3. Đếm số màn/popup mở ra + đối chiếu design",
       "—",
       "- Icon khớp design\n- Chỉ mở ĐÚNG 1 màn hình preview/send test, giao diện khớp design",
       note="Nguồn: r511-r513, r565"),

    tc("Preview & send test step", "UI-001", "Normal",
       "Button プレビューとテスト: đúng design, hover đổi màu, double click chỉ mở 1 popup 2 bên (trái preview 2 tab, phải send test)",
       STEP,
       "1. Quan sát button「プレビューとテスト」\n2. Hover vào button\n3. Double click nhanh\n"
       "4. Quan sát bố cục popup mở ra",
       "—",
       "- Button khớp design, hover đổi màu\n- Chỉ mở 1 popup\n"
       "- Popup chia 2 bên: BÊN TRÁI có 2 tab「メッセージ」và「アクション」; BÊN PHẢI là vùng send test",
       note="Nguồn: r566-r569, r658"),

    tc("Preview & send test step", "OUT-001", "Normal",
       "Link 検索してもアカウントが表示されない場合はこちら → mở https://lme.jp/manual/test_delivery/",
       PREV,
       "1. Click link「検索してもアカウントが表示されない場合はこちら」\n2. Quan sát URL trang mở ra",
       "—",
       "- Mở đúng trang https://lme.jp/manual/test_delivery/",
       note="Nguồn: r514, r570"),

    tc("Preview & send test step", "UI-FIELD-001", "Normal",
       "Ô tìm kiếm friend ở vùng send test: có placeholder, tự trim space đầu/cuối; click vào ô → tự hiện 20 friend đầu tiên",
       PREV + "\n- Bot A có ≥ 50 friend",
       "1. Quan sát placeholder của ô tìm kiếm\n2. Click vào ô tìm kiếm (chưa nhập gì) → đếm số friend hiển thị\n"
       "3. Nhập「  さや  」(có space đầu/cuối) → Enter → quan sát kết quả",
       "≥ 50 friend; từ khoá「  さや  」",
       "- Có placeholder đúng design\n- Click vào ô: tự động hiển thị 20 friend đầu tiên trong list bạn bè\n"
       "- Search「  さや  」cho kết quả giống「さや」(đã trim space)",
       note="Nguồn: r515-r517, r571-r573"),

    tc("Preview & send test step", "FUNC-SEARCH-001", "Normal",
       "Search friend: đúng (JP) / gần đúng / hoa-thường → đều ra kết quả; kết quả nhiều thì có scroll",
       PREV + "\n- Bot có friend「さやか」,「Sayaka」,「sayaka2」và ≥ 30 friend tên chứa「テスト」",
       "1. Search「さやか」(chính xác, tiếng Nhật) → quan sát\n2. Search「さや」(gần đúng) → quan sát\n"
       "3. Search「SAYAKA」(chữ hoa) → quan sát\n4. Search「テスト」(≥ 30 kết quả) → kiểm tra scroll",
       "「さやか」·「さや」·「SAYAKA」·「テスト」",
       "- Cả 3 kiểu search đều trả về đúng friend tương ứng (khớp gần đúng, không phân biệt hoa/thường)\n"
       "- Kết quả ít: hiển thị đủ không scroll; kết quả nhiều: có scroll và hiển thị đủ",
       note="Nguồn: r574-r578"),

    tc("Preview & send test step", "FUNC-SEARCH-001", "Abnormal",
       "Search friend bằng LINE name KHÔNG tồn tại → không hiển thị friend nào",
       PREV,
       "1. Nhập LINE name không tồn tại「ZZZZ存在しない」\n2. Quan sát danh sách kết quả",
       "「ZZZZ存在しない」",
       "- Không hiển thị friend nào\n- Không lỗi JS",
       note="Nguồn: r518, r579"),

    tc("Preview & send test step", "CONC-001", "Abnormal",
       "Đăng ký tài khoản test: double click button add (enable) → chỉ add 1 lần; sau add button chuyển DISABLE; double click khi disable không có tác dụng",
       PREV,
       "1. Search friend「さやか」\n2. Double click nhanh button add của friend đó\n3. Đếm số dòng trong danh sách account test\n"
       "4. Quan sát trạng thái button add của friend vừa add\n5. Double click lại button add đang disable → quan sát",
       "Friend「さやか」",
       "- Chỉ add ĐÚNG 1 lần, danh sách account test có 1 dòng「さやか」\n"
       "- Button add của「さやか」chuyển sang DISABLE\n- Double click khi disable: không có tác dụng, không nhân đôi",
       note="Nguồn: r519-r522, r580-r583"),

    tc("Preview & send test step", "STATE-CLEAN-001", "Normal",
       "Xoá friend khỏi danh sách account test → button add của friend đó ENABLE trở lại",
       PREV + "\n- Đã add friend「さやか」vào danh sách account test",
       "1. Xoá「さやか」khỏi danh sách account test (click icon xoá)\n2. Quan sát danh sách account test\n"
       "3. Search lại「さやか」→ quan sát trạng thái button add\n4. Hover vào icon xoá của friend khác → quan sát màu",
       "Friend「さやか」đã add rồi xoá",
       "- Danh sách account test mất「さやか」\n- Button add của「さやか」ENABLE trở lại\n"
       "- Hover icon xoá: đổi màu xám đậm (theo design)",
       note="Nguồn: r523, r538-r540, r584, r619-r622"),

    tc("Preview & send test step", "FRIEND-001", "Abnormal",
       "Friend BỊ CHẶN: search đúng từ khoá nhưng KHÔNG ra kết quả; và bị mất khỏi danh sách account test",
       PREV + "\n- Friend「ブロック太郎」đã add vào danh sách account test, sau đó block bot",
       "1. Friend「ブロック太郎」thực hiện block bot\n2. Ở màn send test, search đúng「ブロック太郎」→ quan sát kết quả\n"
       "3. Quan sát danh sách account test",
       "Friend「ブロック太郎」đang block bot",
       "- Search đúng từ khoá nhưng KHÔNG hiển thị friend nào\n- Friend biến mất khỏi danh sách account test",
       env="PRODUCTION",
       note="RULE-08: hành vi block phía LINE → cần PRODUCTION. Nguồn: r524, r527, r585, r590"),

    tc("Preview & send test step", "FRIEND-001", "Normal",
       "Friend MỞ CHẶN: search lại được và hiện lại ở danh sách account test, NHƯNG mất trạng thái quick send đã tick trước đó",
       PREV + "\n- Friend「ブロック太郎」trước khi block đã được tick quick send; hiện đang block bot",
       "1. Friend「ブロック太郎」mở chặn (unblock) bot\n2. Search「ブロック太郎」→ quan sát kết quả\n"
       "3. Quan sát danh sách account test và trạng thái icon quick send của friend này",
       "Friend「ブロック太郎」từng tick quick send, block rồi unblock",
       "- Search thành công\n- Friend hiển thị lại ở danh sách account test\n"
       "- Trạng thái quick send BỊ MẤT (icon quick send về disable)",
       env="PRODUCTION",
       note="RULE-08. Nguồn: r525, r528, r586, r591"),

    tc("Preview & send test step", "UI-002", "Normal",
       "Danh sách account test: hiển thị friend vừa add; ít bản ghi không scroll, nhiều bản ghi có scroll",
       PREV + "\n- Chuẩn bị 2 trạng thái: 3 friend (chưa scroll) và 15 friend (có scroll)",
       "1. Add 3 friend → quan sát danh sách (có scroll không)\n2. Add tiếp lên 15 friend → quan sát scroll\n"
       "3. Scroll xuống cuối, đếm số friend",
       "3 friend và 15 friend",
       "- 3 friend: hiển thị đủ, chưa cần scroll\n- 15 friend: có scroll, scroll xuống thấy đủ 15",
       note="Nguồn: r526, r587-r589"),

    tc("Preview & send test step", "OUT-001", "Normal",
       "テスト送信 (gửi từng friend): button đúng design, hover đổi màu, double click chỉ gửi 1 lần, hiển thị thông báo thành công",
       PREV + "\n- Đã add friend test「さやか」",
       "1. Quan sát button「テスト送信」+ hover\n2. Double click nhanh button「テスト送信」\n"
       "3. Quan sát thông báo + LINE app của「さやか」\n4. Đếm số message nhận được",
       "Friend「さやか」; step có 3 message",
       "- Button khớp design, hover đổi màu\n- Double click chỉ gửi 1 lần\n- Hiển thị thông báo THÀNH CÔNG\n"
       "- LINE app nhận đủ 3 message, ĐÚNG thứ tự, KHÔNG trùng",
       env="PRODUCTION",
       note="RULE-06 + RULE-07. Nguồn: r530-r532, r593-r597"),

    tc("Preview & send test step", "OUT-001", "Abnormal",
       "テスト送信 FAIL → hiển thị thông báo thất bại, friend KHÔNG nhận được message",
       PREV + "\n- Tạo điều kiện gửi thất bại (vd friend đã block giữa chừng / bot hết quota)",
       "1. Nhấn「テスト送信」trong điều kiện gửi thất bại\n2. Quan sát thông báo\n3. Kiểm tra LINE app của friend",
       "Điều kiện gửi thất bại",
       "- Hiển thị thông báo THẤT BẠI\n- Friend KHÔNG nhận được message nào",
       env="PRODUCTION",
       note="Nguồn: r598, r599"),

    tc("Preview & send test step", "BULK-001", "Normal",
       "一括テスト送信: default không tick → DISABLE; tick friend → ENABLE; tick rồi xoá friend → về DISABLE; sau khi gửi xong → DISABLE",
       PREV + "\n- Đã add 3 friend test",
       "1. Không tick friend nào → quan sát trạng thái button「一括テスト送信」\n2. Tick 2 friend → quan sát button\n"
       "3. Tick 1 friend rồi XOÁ chính friend đó khỏi danh sách → quan sát button\n"
       "4. Tick lại 2 friend → nhấn gửi thành công → quan sát button sau khi gửi",
       "3 friend test",
       "- Chưa tick: DISABLE\n- Tick: ENABLE\n- Tick rồi xoá friend: về DISABLE\n- Sau khi gửi xong: về DISABLE",
       note="Nguồn: r533-r536, r600-r606"),

    tc("Preview & send test step", "BULK-001", "Normal",
       "一括テスト送信: double click chỉ gửi 1 lần; friend được chọn nhận đủ template con trong template cha, đúng thứ tự",
       PREV + "\n- Đã add 3 friend test; step có 1 template group chứa 4 template con",
       "1. Tick cả 3 friend\n2. Double click nhanh button「一括テスト送信」\n"
       "3. Kiểm tra LINE app của cả 3 friend\n4. Đếm số message và đối chiếu thứ tự",
       "3 friend; template group có 4 template con",
       "- Chỉ gửi 1 lần (không nhân đôi)\n- Cả 3 friend nhận ĐỦ 4 template con, ĐÚNG thứ tự, KHÔNG trùng",
       env="PRODUCTION",
       note="RULE-06. Nguồn: r537, r605"),

    tc("Preview & send test step", "UI-FIELD-001", "Normal",
       "Quick send: icon đúng design, default DISABLE, hover đổi màu; tick được tối đa 3 friend",
       PREV + "\n- Đã add 5 friend test",
       "1. Quan sát icon quick send của các friend (default)\n2. Hover vào icon quick send\n"
       "3. Tick quick send cho friend 1, 2, 3\n4. Thử tick friend thứ 4",
       "5 friend test",
       "- Icon khớp design, default DISABLE, hover đổi màu xanh\n- Tick được 3 friend đầu\n"
       "- Friend thứ 4: KHÔNG tick thêm được (giới hạn 3)",
       note="Nguồn: r541-r543, r607-r610"),

    tc("Preview & send test step", "MSG-001", "Normal",
       "Quick send: hover icon ĐANG BẬT → hiện クイックテストユーザーの登録を解除, click → gỡ khỏi list; hover icon TẮT khi đã đủ 3 → hiện クイックテストユーザーに登録（3人まで) và không bật được",
       PREV + "\n- Đã add 5 friend test, đã tick quick send cho đúng 3 friend",
       "1. Hover icon quick send ĐANG BẬT của friend 1 → đọc tooltip\n2. Click vào → quan sát danh sách quick send\n"
       "3. Tick lại đủ 3 friend\n4. Hover icon quick send ĐANG TẮT của friend 4 → đọc tooltip → click thử\n"
       "5. Gỡ 1 friend để còn 2, hover icon tắt của friend 4 → click",
       "5 friend, 3 đang quick send",
       "- Icon bật: tooltip「クイックテストユーザーの登録を解除」; click → gỡ khỏi list quick send\n"
       "- Icon tắt khi đã đủ 3: tooltip「クイックテストユーザーに登録（3人まで)」, KHÔNG bật được\n"
       "- Khi dưới 3: click bật được bình thường",
       note="Nguồn: r544-r547, r611-r614, r529"),

    tc("Preview & send test step", "REG-SHARED-001", "Normal",
       "Quick send thành công → friend đã chọn hiển thị ở màn list, màn メッセージ登録 và ngoài step; send test từ quick send hoạt động đúng",
       PREV + "\n- Đã tick quick send cho 2 friend",
       "1. Tick quick send cho「さやか」và「たろう」\n2. Đóng popup, quan sát vùng quick send ngoài step\n"
       "3. Mở màn「メッセージ登録」→ quan sát danh sách quick send\n4. Nhấn nút quick send → kiểm tra LINE app 2 friend",
       "2 friend quick send",
       "- Cả 3 nơi (màn list, màn メッセージ登録, ngoài step) đều hiển thị đúng 2 friend đã chọn quick send\n"
       "- Nhấn quick send: cả 2 friend nhận được message",
       env="PRODUCTION",
       note="RULE-07 verify 3 nơi hiển thị + output LINE. Nguồn: r615-r618"),

    tc("Preview & send test step", "OUT-PREVIEW-001", "Normal",
       "Preview (bên trái) tab メッセージ: hiển thị đúng text (JP max length, xuống dòng), media, stamp, location, quick reply nhiều button",
       PREV + "\n- Step có template text JP dài (max length, có xuống dòng), template media (image/video/audio), "
       "template stamp, template location, template button quick reply nhiều button",
       "1. Mở tab「メッセージ」ở bên trái popup preview\n2. Kiểm tra hiển thị template text (max length + enter) → scroll\n"
       "3. Kiểm tra template media: image, video, audio\n4. Kiểm tra template stamp\n5. Kiểm tra template location\n"
       "6. Kiểm tra template button quick reply có nhiều button",
       "5 loại template; text JP max length có xuống dòng; quick reply nhiều button",
       "- Hiển thị ĐÚNG toàn bộ template và message đã setup\n- Text dài: có scroll, giữ đúng xuống dòng\n"
       "- Media/stamp/location hiển thị đúng dạng\n- Quick reply nhiều button hiển thị đủ, không vỡ layout",
       env="PRODUCTION",
       note="RULE-08: media → PRODUCTION. Corpus ghi chú r632/r668:『case này hay lỗi』với quick reply nhiều button. "
            "Nguồn: r548-r552, r624-r627, r632"),

    tc("Preview & send test step", "OUT-PREVIEW-001", "Normal",
       "Preview: thứ tự template con giống màn list template, button QUICK luôn ở CUỐI; ít thì không scroll, nhiều thì có scroll",
       PREV + "\n- Step có template group chứa 6 template con, trong đó có 1 button quick reply",
       "1. Mở tab「メッセージ」\n2. Đối chiếu thứ tự template con với thứ tự ở màn list template\n"
       "3. Xác định vị trí button quick reply\n4. Kiểm tra scroll khi ít (2 template con) và nhiều (6 template con)",
       "Template group 6 template con (1 quick reply)",
       "- Thứ tự template con GIỐNG thứ tự ở màn list template\n- Button quick reply nằm ở CUỐI danh sách\n"
       "- 2 template con: chưa scroll; 6 template con: có scroll và hiển thị đủ",
       note="Nguồn: r553-r555, r628-r630, r664-r666"),

    tc("Preview & send test step", "OUT-PREVIEW-001", "Normal",
       "Preview tab アクション: hiển thị đủ 5 nhóm action; 絞り込みなし không click được; 絞り込みあり mở popup filter",
       PREV + "\n- Step có 5 action: start/stop/start-từ-giữa scenario · template · text · remind start/stop · tag gắn/xoá; "
       "trong đó 2 action có filter, 3 action không filter",
       "1. Mở tab「アクション」\n2. Đếm và đối chiếu danh sách action hiển thị\n"
       "3. Double click action「絞り込みなし」→ quan sát\n4. Double click action「絞り込みあり」→ quan sát popup\n"
       "5. Kiểm tra thứ tự action + scroll khi nhiều action",
       "5 nhóm action; 2 có filter, 3 không filter",
       "- Hiển thị đủ 5 action, đúng thứ tự, có scroll khi nhiều\n"
       "- Action「絞り込みなし」: KHÔNG click được\n"
       "- Action「絞り込みあり」: mở popup filter, nêu rõ chỉ friend thoả bộ lọc (và có tên trên 配信先絞込み) mới nhận action",
       note="Nguồn: r633-r640, r669-r677"),

    tc("Preview & send test step", "FUNC-004", "Normal",
       "Xoá step: double click icon xoá → chỉ 1 lần + popup xác nhận; OK = xoá, Cancel = huỷ",
       STEP,
       "1. Double click nhanh icon xoá step\n2. Đếm số popup + quan sát nội dung popup\n"
       "3. Click Cancel → kiểm tra step còn không\n4. Lặp lại, click OK → kiểm tra danh sách step + `step_message`",
       "Step「02時間00分後」",
       "- Chỉ mở 1 popup xác nhận\n- Cancel: step vẫn còn\n- OK: step bị xoá khỏi danh sách và khỏi `step_message`",
       note="Nguồn: r702, r703"),

    tc("Preview & send test step", "DATA-CASCADE-001", "Abnormal",
       "Xoá step trong scenario ĐANG start cho friend (step chưa tới lượt) → bản ghi pending bị xoá, friend không nhận step đó",
       STEP + "\n- S1 đang có 3 friend chạy; step「02時間00分後」chưa tới giờ gửi",
       "1. Ghi lại `scenario_step_time` (status = 0) của step này\n2. Xoá step\n"
       "3. Query lại `scenario_step_time`\n4. Chờ qua mốc 02時間00分後 → kiểm tra LINE app 3 friend\n"
       "5. Kiểm tra `scenario_lineuser`.`is_following` và `is_last_step` của step còn lại",
       "3 friend đang chạy; xoá step chưa tới lượt",
       "- Bản ghi `scenario_step_time` (status = 0) của step bị XOÁ\n- 3 friend KHÔNG nhận message của step đã xoá\n"
       "- Nếu step bị xoá là last step: step còn lại có send_time lớn nhất được set `is_last_step` = 1",
       spec="Spec không ghi",
       note="Corpus r705 chỉ đánh OK, không có kết quả mong đợi → kết quả mong đợi suy từ spec logic-spec "
            "`deleteScenarioStep`. CẦN LEADER XÁC NHẬN. Nguồn: r705"),

    tc("Preview & send test step", "OUT-001", "Normal",
       "Send test TẠI STEP → friend nào được chọn thì nhận message NGAY, KHÔNG quan tâm điều kiện filter",
       STEP + "\n- Step thuộc filter F-A (điều kiện: có tag「A」)\n- friend「たろう」KHÔNG có tag「A」",
       "1. Ở step thuộc F-A, mở preview & send test\n2. Add friend「たろう」(không thoả filter) vào account test\n"
       "3. Nhấn「テスト送信」\n4. Kiểm tra LINE app của「たろう」",
       "Friend「たろう」không thoả điều kiện filter F-A",
       "- Friend「たろう」VẪN NHẬN được message ngay lập tức\n"
       "- Send test tại step KHÔNG áp dụng điều kiện filter (khác với 一括テスト)",
       env="PRODUCTION",
       note="⚠️ Đây là điểm KHÁC BIỆT quan trọng so với 一括テスト (r774: 『thật sao test vậy, user phải thỏa mãn filter "
            "thì mới được send』). Nguồn: r814"),

    # ══════════════════ 21. Send test 一括テスト ══════════════════
    tc("Send test 一括テスト", "UI-001", "Normal",
       "一括テスト: giao diện đúng design; logic『thật sao test vậy』— user phải thoả mãn filter mới được send",
       "- Đăng nhập admin, bot A\n- Scenario S1 có filter default (2 step) và filter F-A (điều kiện tag「A」, 2 step)\n"
       "- Chuẩn bị friend「たろう」có tag「A」và friend「はなこ」không có tag",
       "1. Mở màn「一括テスト」\n2. Đối chiếu giao diện với design\n3. Add cả「たろう」và「はなこ」vào account test\n"
       "4. Chọn option 1, nhấn 一括テスト送信\n5. Kiểm tra LINE app của 2 friend\n"
       "6. Query `filters_v2` WHERE parent_type = 'filter_manager' AND parent_id = <F-A>",
       "friend「たろう」(tag A) · friend「はなこ」(không tag)",
       "- Giao diện khớp design; search + add friend vào account test hoạt động đúng\n"
       "-「たろう」: nhận message của CẢ filter default và F-A\n"
       "-「はなこ」: chỉ nhận message của filter default, KHÔNG nhận của F-A",
       env="PRODUCTION",
       note="RULE-06 + RULE-07. Nguồn: r774, r775, r819, r11-r13 (tab 2/12)"),

    tc("Send test 一括テスト", "FUNC-DATE-001", "Normal",
       "Option 1「設定した配信タイミング通りに…」+ 1 user: send theo đúng timing của scenario; time đã QUA thì bỏ qua message của time đó",
       "- Scenario S1 (filter default) có 3 step: ステップ開始直後 · 経過時間 00時間30分後 · 日時で指定 1日後 08:00\n"
       "- Thời điểm nhấn send test: 2026/03/04 18:00\n- 1 friend test「たろう」",
       "1. Mở「一括テスト」, tick「たろう」\n2. Chọn option 1「設定した配信タイミング通りにメッセージ・アクションの送信・稼働テストをする」\n"
       "3. Nhấn「一括テスト送信」\n4. Query `scenario_step_time` WHERE user_id = <たろう>: send_time, is_last_step\n"
       "5. Quan sát LINE app của「たろう」theo từng mốc thời gian",
       "3 step; nhấn send test lúc 2026/03/04 18:00",
       "- step ステップ開始直後 → send_time = 2026-03-04 18:00\n"
       "- step 経過時間 00時間30分後 → send_time = 2026-03-04 18:30\n"
       "- step 日時で指定 1日後 08:00 → send_time = 2026-03-05 08:00\n"
       "- Các bản ghi có `is_last_step` = 2 (đánh dấu send test)\n"
       "- LINE app nhận message ĐÚNG các mốc trên; time nào đã qua thì bỏ qua message của time đó",
       env="PRODUCTION",
       note="RULE-08: phụ thuộc job nền → PRODUCTION. Nguồn: r776-r778, r240, r815, tab 2/12 r3-r5"),

    tc("Send test 一括テスト", "FUNC-DATE-001", "Normal",
       "Option 1 + NHIỀU user: insert bản ghi scenario_step_time đúng cho từng user, không lẫn user",
       "- Scenario S1 có 3 step\n- 3 friend test「たろう」,「はなこ」,「さやか」",
       "1. Tick cả 3 friend, chọn option 1 → nhấn「一括テスト送信」\n"
       "2. Query `scenario_step_time` GROUP BY user_id → đếm số bản ghi mỗi user\n"
       "3. Đối chiếu send_time của từng user với timing scenario\n4. Kiểm tra LINE app cả 3 friend",
       "3 friend × 3 step = 9 bản ghi",
       "- `scenario_step_time` có đúng 9 bản ghi, mỗi user 3 bản ghi\n"
       "- send_time của từng user tính đúng theo timing scenario\n"
       "- Bản ghi được insert lần lượt hết step của user này rồi mới tới user kế tiếp\n"
       "- Cả 3 friend nhận message đúng thứ tự, không trùng, không lẫn",
       env="PRODUCTION",
       note="Nguồn: r779, r243, r58, tab 2/12 r6"),

    tc("Send test 一括テスト", "FUNC-SEQ-001", "Normal",
       "Option 2「全てのメッセージを同時に送信」: chỉ tạo 1 bản ghi cho step có send_time NHỎ NHẤT, is_last_step = 3; sau mỗi lần gửi mới chèn step kế tiếp",
       "- Scenario S1 có 4 step ở 2 filter (default 2 step, F-A 2 step), friend test thoả mãn cả 2 filter\n"
       "- Bot chạy trên môi trường có job scenario hoạt động",
       "1. Tick 1 friend, chọn option 2「全てのメッセージを同時に送信」→ nhấn gửi\n"
       "2. NGAY sau khi nhấn: query `scenario_step_time` WHERE user_id = <friend> → đếm số bản ghi + is_last_step\n"
       "3. Theo dõi liên tục: sau mỗi lần job gửi 1 step, query lại `scenario_step_time`\n"
       "4. Đếm tổng số message friend nhận trên LINE app và thứ tự",
       "4 step ở 2 filter (cả có filter và không filter)",
       "- Ngay sau khi nhấn: `scenario_step_time` chỉ có ĐÚNG 1 bản ghi — của step có send_time NHỎ NHẤT, `is_last_step` = 3\n"
       "- Sau mỗi lần gửi xong: job check step kế tiếp và insert bản ghi mới (send_time = thời điểm hiện tại, is_last_step = 3)\n"
       "- Friend nhận đủ 4 message liên tục, ĐÚNG thứ tự setting trên web",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-31 — MÂU THUẪN THEO NIÊN ĐẠI: corpus CŨ (r780/r816, 2024-2025) ghi『sent_time của TẤT CẢ step_message_id "
            "sẽ giống nhau = thời điểm click send』(tạo hết bản ghi cùng lúc); corpus MỚI (Bug KH #34489, 03/2026 — "
            "「Job scenario」r242, r253) ghi『chỉ tạo 1 record cho step có send_time nhỏ nhất, is_last_step = 3, "
            "gửi xong mới chèn step kế』. Đã áp bản MỚI theo quy tắc ưu tiên TC mới nhất. Nguồn: r780, r816, r242, r253"),

    tc("Send test 一括テスト", "FUNC-SEQ-001", "Normal",
       "Bug KH #34489: send test all — thứ tự message giữa các step phải đúng A → B → C → D (không bị đảo do multi thread)",
       "- Scenario S1: step 1 có 2 template A và B; step 2 có 2 template C và D\n- 1 friend test",
       "1. Tick 1 friend, chọn option 2「全てのメッセージを同時に送信」→ nhấn gửi\n"
       "2. Quan sát LINE app: ghi lại thứ tự 4 message nhận được\n"
       "3. Lặp lại 3 lần vào giờ cao điểm để kiểm tra tính ổn định",
       "step1 = [A, B]; step2 = [C, D]",
       "- LINE app nhận đúng thứ tự: A → B → C → D\n- Lặp 3 lần đều đúng thứ tự, không bị đảo",
       env="PRODUCTION",
       note="Bug KH #34489 (21-02-2026). RULE-06. Nguồn:「Job scenario」r254"),

    tc("Send test 一括テスト", "FUNC-SEQ-001", "Normal",
       "Bug KH #34489: thứ tự ưu tiên step khi job send test — send ngay → cộng giờ → cộng ngày; cùng type thì time nhỏ hơn trước; cùng giờ thì sort theo id tăng dần",
       "- Scenario S1 có 5 step: ステップ開始直後 · 経過時間 01時間00分後 · 経過時間 02時間00分後 · "
       "日時で指定 0日後 20:00 · 日時で指定 1日後 09:00\n- Thêm 2 step khác filter nhưng CÙNG giờ gửi",
       "1. Tick 1 friend, chọn option 2 → nhấn gửi\n2. Ghi lại thứ tự message nhận trên LINE app\n"
       "3. Query `scenario_step_time` theo thứ tự insert\n4. Với 2 step cùng giờ: đối chiếu thứ tự với `step_message`.`id`",
       "5 step đủ 3 loại timing + 2 step trùng giờ",
       "- Thứ tự gửi: send ngay → 01時間00分後 → 02時間00分後 → 0日後20:00 → 1日後09:00\n"
       "- 2 step CÙNG giờ gửi: gửi xong step 1 rồi mới tới step 2, sort theo `id` TĂNG DẦN",
       env="PRODUCTION",
       note="Bug KH #34489. Nguồn:「Job scenario」r255, r256"),

    tc("Send test 一括テスト", "FUNC-DATE-001", "Normal",
       "Option 3「20~30秒ごとにメッセージを送信」: step đầu gửi ngay, các step sau cách nhau random 20-30 giây",
       "- Scenario S1 có 3 step: ステップ開始直後 · 経過時間 00時間30分後 · 日時で指定 1日後 08:00\n"
       "- Thời điểm nhấn send test: 2026/03/04 18:00 · 1 friend test",
       "1. Tick 1 friend, chọn option 3「20~30秒ごとにメッセージを送信（テスト開始後の編集内容は反映されません）」→ nhấn gửi\n"
       "2. Query `scenario_step_time`: send_time của từng step\n"
       "3. Ghi lại thời điểm thực tế nhận message trên LINE app, tính khoảng cách giữa các message",
       "3 step; nhấn gửi lúc 18:00:00",
       "- step 1 (send ngay): send_time = 18:00:00, gửi luôn\n"
       "- step 2: send_time cách step 1 từ 20 đến 30 giây (vd 18:00:20)\n"
       "- step 3: cách step 2 từ 20 đến 30 giây\n"
       "- LINE app nhận 3 message với khoảng cách thực tế 20–30 giây",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-32 — corpus r782 ghi chú kết quả test:『Chưa thấy random』. Cần xác nhận random 20-30s đã hoạt động chưa. "
            "Nguồn: r782, r783, r817, r241"),

    tc("Send test 一括テスト", "DATA-COUNT-001", "Normal",
       "Send test 一括テスト: KHÔNG ghi nhận số friend đã send ở step và ở màn list; KHÔNG lưu lịch sử gửi (không hiện ở my_page)",
       "- Scenario S1 có 3 step, send_count hiện tại = 0; 3 cột đếm friend ở màn list = 0\n- 1 friend test",
       "1. Ghi lại `step_message`.`send_count` và 3 cột đếm ở màn list scenario\n"
       "2. Tick 1 friend, chọn option 1 → gửi → chờ gửi xong\n"
       "3. Query lại `step_message`.`send_count` + xem 配信済 ở từng step\n"
       "4. Xem 3 cột đếm ở màn list scenario\n5. Query `step_message_history` WHERE line_user_id = <friend>\n"
       "6. Mở màn my_page của friend → kiểm tra lịch sử gửi",
       "1 friend send test qua option 1",
       "- `step_message`.`send_count` KHÔNG tăng; 配信済 ở từng step vẫn 0人\n"
       "- 3 cột đếm ở màn list scenario KHÔNG đổi\n"
       "- `step_message_history` KHÔNG có bản ghi mới\n- Màn my_page KHÔNG hiển thị lịch sử gửi",
       env="PRODUCTION",
       note="RULE-07 verify DB + màn hình + my_page. Nguồn: r815-r817, r251-r253, tab 2/12 r3-r10"),

    tc("Send test 一括テスト", "OUT-001", "Normal",
       "Bug KH #34489: send test 1 template con / toàn bộ template của 1 step → gửi NGAY, trigger chat 1:1 hiển thị 'trigger send test'",
       "- Scenario S1 có step「02時間00分後」với template group chứa 3 template con\n- 1 friend test",
       "1. Ở step, nhấn send test cho ĐÚNG 1 template con → kiểm tra LINE app + trigger chat 1:1\n"
       "2. Nhấn send test cho TOÀN BỘ template của step → kiểm tra LINE app + trigger chat 1:1",
       "1 template con / toàn bộ 3 template con",
       "- Cả 2 case: message được gửi NGAY cho friend (không chờ timing của step)\n"
       "- Màn chat 1:1 hiển thị trigger loại「send test」",
       env="PRODUCTION",
       note="Bug KH #34489. Nguồn:「Job scenario」r238, r239"),

    tc("Send test 一括テスト", "CONC-001", "Abnormal",
       "Double click button send test / 一括テスト送信 → KHÔNG tạo duplicate bản ghi trong scenario_step_time",
       "- Scenario S1 có 3 step; 1 friend test đã add",
       "1. Tick 1 friend, chọn option 1 → double click nhanh button「一括テスト送信」\n"
       "2. Query `scenario_step_time` WHERE user_id = <friend> → đếm số bản ghi\n"
       "3. Lặp với nút gửi nhanh「テスト送信」\n4. Kiểm tra LINE app xem có nhận trùng message không",
       "3 step; double click nút gửi",
       "- `scenario_step_time` có đúng 3 bản ghi (không nhân đôi thành 6)\n- LINE app không nhận message trùng",
       env="PRODUCTION",
       note="Bug KH #34489. Nguồn:「Job scenario」r246"),

    tc("Send test 一括テスト", "PERM-001", "Normal",
       "Account STAFF nhấn send test 一括テスト → tạo được bản ghi cho toàn bộ user được chọn",
       "- Đăng nhập bằng account STAFF có quyền truy cập màn scenario\n- Scenario S1 có 3 step; 2 friend test",
       "1. Đăng nhập account staff, mở scenario S1\n2. Tick 2 friend, chọn option 1 → nhấn「一括テスト送信」\n"
       "3. Query `scenario_step_time` WHERE user_id IN (2 friend)\n4. Kiểm tra LINE app của 2 friend",
       "Account staff; 2 friend × 3 step = 6 bản ghi",
       "- Tạo đủ 6 bản ghi `scenario_step_time` cho cả 2 user được chọn\n- Cả 2 friend nhận đủ message",
       env="PRODUCTION",
       note="Bug KH #34489. Nguồn:「Job scenario」r245"),

    tc("Send test 一括テスト", "FUNC-001", "Normal",
       "Nút gửi nhanh テスト送信 (quick send) ở màn 一括テスト → tạo bản ghi giống hệt nhấn 一括テスト送信",
       "- Scenario S1 có 3 step; 1 friend đã tick quick send",
       "1. Nhấn nút gửi nhanh「テスト送信」cho friend quick send\n"
       "2. Query `scenario_step_time` WHERE user_id = <friend>\n"
       "3. So sánh với kết quả khi nhấn「一括テスト送信」cho cùng friend đó",
       "1 friend quick send; 3 step",
       "- Bản ghi tạo ra GIỐNG HỆT case nhấn「一括テスト送信」(cùng số lượng, cùng send_time, cùng is_last_step)",
       env="PRODUCTION",
       note="Bug KH #34489. Nguồn:「Job scenario」r244, r792"),

    tc("Send test 一括テスト", "FUNC-DATE-001", "Normal",
       "テスト送信 (gửi từng friend) ở màn 一括テスト cũng hỗ trợ đủ 3 option gửi, kết quả giống 一括テスト送信",
       "- Scenario S1 có 3 step đủ 3 loại timing; 1 friend và 3 friend test",
       "1. Chọn option 1 → nhấn「テスト送信」cho 1 friend → query `scenario_step_time` + kiểm tra LINE app\n"
       "2. Lặp với option 2 và option 3\n3. Lặp toàn bộ với 3 friend cùng lúc",
       "3 option × (1 friend / 3 friend)",
       "- Cả 6 tổ hợp: bản ghi `scenario_step_time` và message nhận trên LINE app GIỐNG kết quả của「一括テスト送信」tương ứng",
       env="PRODUCTION",
       note="6 tổ hợp cùng 1 kết quả → giữ chung. Nguồn: r784-r791"),

    tc("Send test 一括テスト", "DATA-COUNT-001", "Normal",
       "Send test qua friend list / chat 1:1: số lượng đã send lấy từ step_message_history và cột send_count của step_message",
       "- Scenario S1 có filter F-A (điều kiện tag「A」); friend「たろう」có tag A, friend「はなこ」không có\n"
       "- Ghi lại `step_message`.`send_count` ban đầu",
       "1. Từ màn friend list, chọn 2 friend → send test scenario S1\n2. Kiểm tra LINE app 2 friend\n"
       "3. Query `step_message_history` và `step_message`.`send_count`\n"
       "4. Lặp từ màn chat 1:1 với 1 friend và nhiều friend\n5. Kiểm tra next scenario có được trigger không",
       "friend「たろう」(tag A) ·「はなこ」(không tag)",
       "- Chỉ friend thoả mãn filter nhận được message\n"
       "- Số lượng được send step lấy từ `step_message_history`, khớp với cột `send_count` của `step_message`\n"
       "- next scenario được trigger đúng theo setting",
       env="PRODUCTION",
       note="RULE-07. Nguồn: tab 2/12 r11-r14"),
]
