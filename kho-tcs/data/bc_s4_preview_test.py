# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 18-20: Preview 3 tab nội dung, tài khoản test &
quick test, テスト送信 & 一括テスト送信.

Popup preview xuất hiện ở 3 chỗ: màn edit SCR-BC-04 (nút「プレビューとテスト」),
màn list tab 配信予約/下書き (icon「プレビュー・テスト」), màn list tab 配信履歴.
Corpus lặp gần như nguyên khối cho cả 3 chỗ (r160-r232 · r274-r347 · r699-r748) —
kho gộp thành 1 bộ TC, ghi rõ ở Tiền điều kiện là phải chạy đủ cả 3 điểm vào.
"""
from _common import tc

PV = ("- Đăng nhập Admin, có broadcast đã thêm ≥1 tin nhắn\n"
      "- Mở popup preview từ 1 trong 3 điểm: nút「プレビューとテスト」ở màn SCR-BC-04, "
      "icon「プレビュー・テスト」ở tab「配信予約」/「下書き」, hoặc ở tab「配信履歴」")

S4 = [
    # ═══════════ 18. Preview — 3 tab nội dung ═══════════
    tc("Preview — 3 tab nội dung", "CONC-002", "Abnormal",
       "Double click nút/icon mở preview — chỉ mở 1 popup",
       PV.replace("- Mở popup preview", "- CHƯA mở popup preview"),
       "1. Double click nhanh vào「プレビューとテスト」ở màn SCR-BC-04\n"
       "2. Đếm số popup mở ra\n"
       "3. Lặp lại với icon「プレビュー・テスト」ở màn list (cả 3 tab)",
       "Double click trong < 1 giây, thực hiện ở cả 4 điểm vào",
       "- Mỗi điểm vào chỉ mở đúng 1 popup preview\n"
       "- Không mở chồng 2 popup lên nhau",
       note="Nguồn: r161, r275, r700."),

    tc("Preview — 3 tab nội dung", "UI-001", "Normal",
       "Popup preview hiển thị đủ 3 tab theo đúng design",
       PV,
       "1. Mở popup preview\n"
       "2. Đọc tên và thứ tự các tab\n"
       "3. Đối chiếu bố cục với design",
       "Broadcast có tin nhắn, có filter, có action",
       "- Ở màn edit và tab 配信予約/下書き: 3 tab là「メッセージ」·「概要」·「アクション」\n"
       "- Ở tab 配信履歴: tab đầu là「トークルーム」thay cho「メッセージ」\n"
       "- Bố cục 2 cột: preview bên trái, phần gửi thử/thông tin bên phải",
       note="Nguồn: r162-r163, r210, r219, r226, r276, r331, r340, r701, r732, r742. "
            "⚠️ MT-15 — tab đầu ở màn 配信履歴 tên「トークルーム」còn 2 tab kia tên「メッセージ」; "
            "spec KHÔNG mô tả popup preview (U-01 trong feature-spec §9)."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Normal",
       "Tab メッセージ — preview template text đúng nội dung đã cài đặt",
       PV + "\n- Broadcast có 1 tin nhắn text dài, có emoji, URL, tag chèn và file PDF",
       "1. Mở popup preview → tab「メッセージ」\n"
       "2. Đọc nội dung preview và so với nội dung đã soạn\n"
       "3. Cuộn trong khung preview nếu text dài",
       "Text tiếng Nhật độ dài tối đa · có ký tự xuống dòng (Enter) · emoji và symbol · "
       "URL trong nội dung · tag chèn dữ liệu · file PDF đăng ký kèm",
       "- Preview hiển thị đúng toàn bộ nội dung đã soạn\n"
       "- Xuống dòng, emoji, symbol hiển thị đúng, không bị escape thành mã\n"
       "- Text dài có thể cuộn trong khung, không tràn ra ngoài popup",
       note="Nguồn: r210, r322, r733. Gộp 6 dạng nội dung vì cùng 1 kết quả『hiển thị đúng như đã setup』."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Normal",
       "Tab メッセージ — preview template media (ảnh, video, âm thanh)",
       PV + "\n- Broadcast có 3 tin nhắn: 1 ảnh, 1 video, 1 audio",
       "1. Mở popup preview → tab「メッセージ」\n"
       "2. Quan sát từng tin nhắn media\n"
       "3. Thử phát video và audio trong preview (nếu hỗ trợ)",
       "1 ảnh JPG · 1 video MP4 · 1 file audio",
       "- Ảnh hiển thị đúng ảnh đã upload, không vỡ/méo\n"
       "- Video và audio hiển thị đúng thumbnail/khung phát, không báo lỗi tải file",
       env="PRODUCTION",
       note="Nguồn: r211, r323, r734. RULE-08: media → PRODUCTION."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Normal",
       "Tab メッセージ — preview template sticker và location",
       PV + "\n- Broadcast có 1 tin sticker và 1 tin location",
       "1. Mở popup preview → tab「メッセージ」\n"
       "2. Quan sát tin sticker và tin location",
       "1 sticker · 1 location (tên địa điểm + địa chỉ + tọa độ)",
       "- Sticker hiển thị đúng hình sticker đã chọn\n"
       "- Location hiển thị đúng tên địa điểm, địa chỉ và bản đồ/ảnh vị trí",
       note="Nguồn: r212-r213, r324-r325, r735-r736."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Normal",
       "Tab メッセージ — thứ tự tin nhắn khớp thứ tự đã sắp, button quick nằm CUỐI",
       PV + "\n- Broadcast có 4 tin nhắn: text A, text B, button standard C, button quick reply D",
       "1. Sắp xếp thứ tự A → B → C → D ở khối メッセージ登録\n"
       "2. Mở preview tab「メッセージ」đọc thứ tự\n"
       "3. Gửi test cho friend, mở app LINE đọc thứ tự",
       "4 tin: text A · text B · button standard C · button quick reply D",
       "- Preview hiển thị theo thứ tự A, B, C rồi D\n"
       "- Button quick reply LUÔN nằm cuối danh sách\n"
       "- Thứ tự trong app LINE khớp với preview",
       env="PRODUCTION",
       note="Nguồn: r214, r326, r737 + feature-spec.md §5 BR-04 (『ButtonQuickReply luôn đứng cuối "
            "danh sách template_ids』). RULE-07: khớp preview + output LINE."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Boundary",
       "Tab メッセージ — nhiều tin nhắn thì khung preview có scroll",
       PV + "\n- Broadcast có ≥10 tin nhắn",
       "1. Mở preview tab「メッセージ」\n"
       "2. Cuộn trong khung preview xuống tin cuối cùng\n"
       "3. Cuộn ngược lên",
       "10 tin nhắn hỗn hợp text và media",
       "- Khung preview có thanh cuộn riêng\n"
       "- Đọc được tin cuối cùng sau khi cuộn\n"
       "- Popup không bị giãn tràn ra ngoài màn hình",
       note="Nguồn: r215-r216, r327-r328, r738-r739."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Normal",
       "Sửa tin nhắn xong — preview cập nhật nội dung mới",
       PV + "\n- Broadcast có 1 tin nhắn text「変更前」",
       "1. Mở preview, ghi lại nội dung\n"
       "2. Đóng preview, sửa tin nhắn thành「変更後」\n"
       "3. Mở lại preview",
       "「変更前」→「変更後」",
       "- Preview hiển thị「変更後」\n"
       "- Không còn hiển thị nội dung cũ (không bị cache)",
       note="Nguồn: r217, r329, r740 — file 03/tab function r72 ghi nhận bug『edit template nhưng preview "
            "vẫn hiển thị cái cũ』(không tái hiện lại được). TC viết theo hành vi ĐÚNG."),

    tc("Preview — 3 tab nội dung", "OUT-PREVIEW-001", "Boundary",
       "Preview template button quick reply có NHIỀU button — điểm hay lỗi",
       PV + "\n- Broadcast có 1 template button quick reply với ≥10 button",
       "1. Tạo template quick reply với 10 button, label dài\n"
       "2. Mở preview tab「メッセージ」\n"
       "3. Cuộn ngang trong dải quick reply\n"
       "4. Gửi test cho friend, so với app LINE",
       "Quick reply 10 button, mỗi label 20 ký tự",
       "- Preview hiển thị đủ 10 button, cuộn ngang được\n"
       "- Không button nào bị mất hoặc chồng lên nhau\n"
       "- Số lượng và thứ tự button khớp với app LINE",
       env="PRODUCTION",
       note="Nguồn: r218, r330, r741 — corpus ghi rõ『case này hay lỗi』."),

    tc("Preview — 3 tab nội dung", "OUT-TRUTH-001", "Normal",
       "Tab 概要 — hiển thị đúng tiêu đề, thời gian gửi, điều kiện lọc, số gửi, người gửi",
       PV + "\n- Broadcast có đủ: tiêu đề, đặt lịch, filter tag T, profile 送信者A",
       "1. Mở preview → tab「概要」\n"
       "2. Đọc từng mục: タイトル · 配信日時 · 絞込み · 配信数 · 送信者名\n"
       "3. Đối chiếu từng mục với giá trị ở màn edit",
       "Tiêu đề「概要テスト」· đặt lịch mai 10:00 · filter tag T (4 friend) · profile「送信者A」",
       "- タイトル =「概要テスト」\n"
       "- 配信日時 = mai 10:00\n"
       "- 絞込み hiển thị điều kiện tag T\n"
       "- 配信数 = 4\n"
       "- 送信者名 hiển thị đúng tên và avatar「送信者A」, avatar không vỡ",
       note="Nguồn: r219-r225, r333-r339."),

    tc("Preview — 3 tab nội dung", "OUT-TRUTH-001", "Normal",
       "Tab アクション — hiển thị đủ action đã đăng ký, đúng thứ tự",
       PV + "\n- Broadcast đã đăng ký 3 action ở 2 folder khác nhau",
       "1. Mở preview → tab「アクション」\n"
       "2. Đọc danh sách action và thứ tự\n"
       "3. Đối chiếu với danh sách ở khối「エルメアクションを追加」",
       "3 action: gán tag · trigger step · đổi richmenu, ở 2 folder",
       "- Hiển thị đủ 3 action\n"
       "- Thứ tự khớp với khối エルメアクションを追加 ở màn edit",
       note="Nguồn: r226, r229, r342, r344, r743, r745."),

    tc("Preview — 3 tab nội dung", "UI-001", "Normal",
       "Link「検索してもアカウントが表示されない場合はこちら」mở trang hướng dẫn gửi thử",
       PV,
       "1. Mở popup preview\n"
       "2. Bấm link「検索してもアカウントが表示されない場合はこちら」\n"
       "3. Quan sát trang mở ra\n"
       "4. Lặp lại ở cả tab「概要」và tab「アクション」",
       "—",
       "- Mở trang https://lme.jp/manual/test_delivery/\n"
       "- Mở ở tab mới, popup preview vẫn giữ nguyên\n"
       "- Link hoạt động ở cả 3 tab của popup",
       note="Nguồn: r164, r332, r341."),

    # ═══════════ 19. Tài khoản test & quick test ═══════════
    tc("Tài khoản test & quick test", "UI-INPUT-001", "Normal",
       "Ô tìm kiếm friend trong preview có placeholder theo design",
       PV,
       "1. Mở popup preview\n"
       "2. Quan sát ô tìm kiếm ở phần gửi thử (bên phải) khi chưa nhập gì",
       "—",
       "- Ô tìm kiếm hiển thị placeholder theo design",
       note="Nguồn: r165, r277."),

    tc("Tài khoản test & quick test", "UI-INPUT-001", "Normal",
       "Ô tìm kiếm friend tự trim khoảng trắng đầu/cuối",
       PV + "\n- Bot có friend tên「テスト太郎」",
       "1. Nhập「  テスト太郎  」vào ô tìm kiếm\n"
       "2. Quan sát kết quả",
       "「  テスト太郎  」",
       "- Tìm ra đúng friend「テスト太郎」\n"
       "- Space thừa không làm mất kết quả",
       note="Nguồn: r166, r278."),

    tc("Tài khoản test & quick test", "FUNC-001", "Normal",
       "Click vào ô tìm kiếm khi chưa gõ — tự hiển thị 20 friend đầu tiên",
       PV + "\n- Bot có ≥30 bạn bè",
       "1. Mở popup preview\n"
       "2. Click vào ô tìm kiếm, KHÔNG gõ gì\n"
       "3. Đếm số friend hiện ra trong danh sách gợi ý",
       "30 bạn bè",
       "- Tự hiển thị danh sách gợi ý gồm đúng 20 friend đầu tiên trong danh sách bạn bè\n"
       "- Thứ tự khớp với thứ tự mặc định ở màn「友だちリスト」",
       note="Nguồn: r167, r279."),

    tc("Tài khoản test & quick test", "FUNC-001", "Normal",
       "Tìm kiếm friend — khớp chính xác, khớp một phần, không phân biệt hoa thường",
       PV + "\n- Bot có friend tên「TestTaro」và「テスト太郎」",
       "1. Nhập「TestTaro」→ đọc kết quả\n"
       "2. Nhập「Test」→ đọc kết quả\n"
       "3. Nhập「testtaro」(chữ thường) → đọc kết quả\n"
       "4. Nhập「TESTTARO」(chữ hoa) → đọc kết quả",
       "「TestTaro」·「Test」·「testtaro」·「TESTTARO」",
       "- Cả 4 truy vấn đều tìm ra friend「TestTaro」\n"
       "- Tìm kiếm khớp một phần và không phân biệt hoa/thường",
       note="Nguồn: r168-r170, r280-r282. Gộp 4 truy vấn vì cùng 1 kết quả."),

    tc("Tài khoản test & quick test", "LIST-001", "Normal",
       "Kết quả tìm kiếm ít — không có scroll; kết quả nhiều — có scroll",
       PV + "\n- Bot có ≥30 friend có tên chứa「テスト」và 1 friend tên「ユニーク」",
       "1. Nhập「ユニーク」→ quan sát khung kết quả (ít)\n"
       "2. Nhập「テスト」→ quan sát khung kết quả (nhiều), cuộn xuống cuối",
       "1 kết quả · 30 kết quả",
       "- Với 1 kết quả: khung không có thanh cuộn, không giãn thừa\n"
       "- Với 30 kết quả: khung có thanh cuộn riêng, cuộn tới friend cuối cùng được",
       note="Nguồn: r171-r172, r283-r284."),

    tc("Tài khoản test & quick test", "FUNC-001", "Abnormal",
       "Tìm kiếm tên friend không tồn tại — không hiển thị friend nào",
       PV,
       "1. Nhập tên chắc chắn không tồn tại vào ô tìm kiếm\n"
       "2. Quan sát danh sách kết quả",
       "「ZZZ_NOT_EXIST_9999」",
       "- Danh sách kết quả rỗng, không hiển thị friend nào\n"
       "- Không báo lỗi JavaScript",
       note="Nguồn: r173, r285."),

    tc("Tài khoản test & quick test", "FUNC-001", "Normal",
       "Thêm friend vào danh sách tài khoản test",
       PV + "\n- Bot có friend「テスト太郎」chưa nằm trong danh sách test",
       "1. Tìm「テスト太郎」\n"
       "2. Bấm nút add ở dòng friend đó\n"
       "3. Quan sát danh sách tài khoản test bên dưới",
       "Friend「テスト太郎」",
       "- Thêm thành công\n"
       "- Danh sách tài khoản test có tên「テスト太郎」",
       note="Nguồn: r175, r179, r287, r291."),

    tc("Tài khoản test & quick test", "STATE-001", "Normal",
       "Nút add của friend đã thêm chuyển sang disable",
       PV + "\n- Đã thêm「テスト太郎」vào danh sách test",
       "1. Tìm lại「テスト太郎」trong ô tìm kiếm\n"
       "2. Quan sát trạng thái nút add ở dòng đó\n"
       "3. Thử double click vào nút đã disable\n"
       "4. Đếm số dòng trong danh sách test",
       "Friend đã có trong danh sách test",
       "- Nút add ở trạng thái disable\n"
       "- Double click không thêm được lần 2\n"
       "- Danh sách test vẫn chỉ có 1 dòng「テスト太郎」",
       note="Nguồn: r176-r177, r288-r289."),

    tc("Tài khoản test & quick test", "STATE-001", "Normal",
       "Xóa friend khỏi danh sách test — nút add của friend đó enable trở lại",
       PV + "\n- Danh sách test đang có「テスト太郎」",
       "1. Bấm icon xóa ở「テスト太郎」trong danh sách test\n"
       "2. Xác nhận friend biến mất khỏi danh sách\n"
       "3. Tìm lại「テスト太郎」trong ô tìm kiếm\n"
       "4. Quan sát nút add",
       "Friend「テスト太郎」",
       "- Friend biến mất khỏi danh sách tài khoản test\n"
       "- Nút add ở kết quả tìm kiếm quay lại trạng thái enable",
       note="Nguồn: r178, r208-r209, r290, r320-r321."),

    tc("Tài khoản test & quick test", "UI-001", "Normal",
       "Hover vào icon xóa friend test — đổi màu xám đậm",
       PV + "\n- Danh sách test có ≥1 friend",
       "1. Rê chuột vào icon xóa ở 1 dòng trong danh sách test\n"
       "2. Quan sát màu icon",
       "—",
       "- Icon đổi sang màu xám đậm theo design\n"
       "- Con trỏ chuyển thành hình bàn tay",
       note="Nguồn: r206-r207, r318-r319."),

    tc("Tài khoản test & quick test", "CONC-002", "Abnormal",
       "Double click nút add khi đang enable — chỉ thêm 1 lần",
       PV + "\n- Bot có friend「テスト太郎」chưa trong danh sách test",
       "1. Tìm「テスト太郎」\n"
       "2. Double click nhanh vào nút add\n"
       "3. Đếm số dòng「テスト太郎」trong danh sách test",
       "Double click trong < 1 giây",
       "- Chỉ 1 dòng「テスト太郎」được thêm vào\n"
       "- Không bị nhân đôi",
       note="Nguồn: r174, r286.",
       group="API"),

    tc("Tài khoản test & quick test", "LIST-001", "Normal",
       "Danh sách tài khoản test ít bản ghi — không scroll; nhiều bản ghi — có scroll",
       PV,
       "1. Thêm 2 friend vào danh sách test → quan sát khung\n"
       "2. Thêm tiếp cho đủ ≥20 friend → cuộn trong khung danh sách",
       "2 friend · 20 friend",
       "- Với 2 friend: không có thanh cuộn\n"
       "- Với 20 friend: khung có thanh cuộn riêng, cuộn tới dòng cuối được\n"
       "- Popup không tràn ra ngoài màn hình",
       note="Nguồn: r180-r181, r292-r293."),

    tc("Tài khoản test & quick test", "UI-001", "Normal",
       "Icon quick send mặc định disable, hover đổi màu xanh",
       PV + "\n- Danh sách test có ≥1 friend chưa đăng ký quick test",
       "1. Quan sát icon quick send của friend chưa đăng ký\n"
       "2. Rê chuột vào icon\n"
       "3. Đọc tooltip hiện ra",
       "1 friend chưa đăng ký quick test",
       "- Icon ở trạng thái disable (chưa đăng ký)\n"
       "- Hover: icon đổi màu xanh, con trỏ thành hình bàn tay\n"
       "- Tooltip hiển thị「クイックテストユーザーに登録（3人まで)」",
       note="Nguồn: r196-r198, r202, r308-r310, r314."),

    tc("Tài khoản test & quick test", "FUNC-001", "Boundary",
       "Đăng ký quick test — tối đa 3 friend",
       PV + "\n- Danh sách test có ≥5 friend, chưa ai là quick tester",
       "1. Bấm icon quick send cho friend 1, 2, 3 → quan sát\n"
       "2. Hover vào icon quick send của friend thứ 4\n"
       "3. Thử bấm vào icon của friend thứ 4\n"
       "4. Đếm số quick tester",
       "5 friend trong danh sách test",
       "- 3 friend đầu đăng ký được, icon chuyển sang enable\n"
       "- Hover friend thứ 4: hiện tooltip「クイックテストユーザーに登録（3人まで)」\n"
       "- Bấm vào friend thứ 4 KHÔNG đăng ký được\n"
       "- Số quick tester dừng ở 3",
       note="Nguồn: r199, r203, r311, r315."),

    tc("Tài khoản test & quick test", "FUNC-001", "Normal",
       "Bỏ đăng ký quick test — friend rời khỏi danh sách quick",
       PV + "\n- Đã có 3 quick tester",
       "1. Hover vào icon quick send đang enable của 1 friend\n"
       "2. Đọc tooltip\n"
       "3. Bấm vào icon\n"
       "4. Đếm lại số quick tester\n"
       "5. Hover vào icon của 1 friend chưa đăng ký, thử bấm",
       "3 quick tester → bỏ 1",
       "- Tooltip khi hover icon enable là「クイックテストユーザーの登録を解除」\n"
       "- Bấm vào: friend bị gỡ khỏi danh sách quick, còn 2 quick tester\n"
       "- Sau khi còn dưới 3, bấm icon của friend khác đăng ký được bình thường",
       note="Nguồn: r200-r202, r312-r314."),

    tc("Tài khoản test & quick test", "STATE-001", "Normal",
       "Quick tester đã chọn hiển thị ở màn list và ở màn đăng ký tin nhắn",
       PV + "\n- Vừa đăng ký「テスト太郎」làm quick tester",
       "1. Đăng ký「テスト太郎」làm quick tester, đóng popup\n"
       "2. Về màn list tab「配信予約」, đọc cột「クイックテスト」\n"
       "3. Mở màn SCR-BC-04, quan sát chỗ「クイックテスト未設定」",
       "1 quick tester「テスト太郎」",
       "- Cột「クイックテスト」ở màn list hiển thị avatar của「テスト太郎」\n"
       "- Ở màn đăng ký tin nhắn, chữ「クイックテスト未設定」được thay bằng avatar「テスト太郎」",
       note="Nguồn: r110, r204-r205, r316-r317, r438."),

    tc("Tài khoản test & quick test", "UI-001", "Normal",
       "Chữ「クイックテスト未設定」có gạch chân, bấm vào mở popup preview",
       "- Đăng nhập Admin, đang ở màn SCR-BC-04\n- Chưa đăng ký quick tester nào",
       "1. Quan sát chữ「クイックテスト未設定」\n"
       "2. Bấm vào chữ đó\n"
       "3. Double click vào chữ đó",
       "0 quick tester",
       "- Chữ「クイックテスト未設定」có gạch chân\n"
       "- Bấm vào: mở popup preview gửi thử\n"
       "- Double click: chỉ mở 1 popup",
       note="Nguồn: r108-r109, r436-r437."),

    tc("Tài khoản test & quick test", "MSG-001", "Normal",
       "Gửi quick test từ màn list — friend nhận được tin nhắn",
       "- Broadcast wait_to_send đã có tin nhắn và 1 quick tester",
       "1. Ở màn list tab「配信予約」, bấm avatar quick test\n"
       "2. Quan sát thông báo\n"
       "3. Mở app LINE của quick tester",
       "1 quick tester, broadcast có 2 tin nhắn text",
       "- Hiện thông báo gửi thành công\n"
       "- Quick tester nhận đủ 2 tin nhắn, đúng thứ tự trong app LINE",
       env="PRODUCTION",
       note="Nguồn: r111 + file 03/tab function r61-r62, r68-r69. RULE-06: đi tới output cuối là app LINE.",
       group="API"),

    # ═══════════ 20. テスト送信 & 一括テスト送信 ═══════════
    tc("テスト送信 & 一括テスト送信", "UI-001", "Normal",
       "Button テスト送信 hiển thị đúng design, hover đổi màu xanh",
       PV + "\n- Danh sách test có ≥1 friend",
       "1. Quan sát button「テスト送信」ở dòng friend\n"
       "2. Rê chuột vào button",
       "—",
       "- Button hiển thị đúng design\n"
       "- Hover: đổi sang màu xanh, con trỏ thành hình bàn tay",
       note="Nguồn: r182-r183, r294-r295."),

    tc("テスト送信 & 一括テスト送信", "CONC-002", "Abnormal",
       "Double click「テスト送信」— chỉ gửi 1 lần",
       PV + "\n- Danh sách test có 1 friend, broadcast có 1 tin nhắn",
       "1. Double click nhanh vào「テスト送信」\n"
       "2. Mở app LINE của friend đếm số tin nhận được\n"
       "3. Mở DevTools → Network đếm số request",
       "Double click trong < 1 giây",
       "- Chỉ 1 request được gửi\n"
       "- Friend nhận đúng 1 lần tin nhắn, không bị gửi lặp",
       env="PRODUCTION",
       note="Nguồn: r184, r296. RULE-08: gửi tin thật → PRODUCTION.",
       group="API"),

    tc("テスト送信 & 一括テスト送信", "MSG-001", "Normal",
       "Gửi thử cho 1 friend thành công — nhận đủ, đúng, đúng thứ tự",
       PV + "\n- Danh sách test có 1 friend, broadcast có 3 tin nhắn A, B, C",
       "1. Bấm「テスト送信」ở dòng friend\n"
       "2. Đọc thông báo trả về\n"
       "3. Mở app LINE của friend, đếm và đọc thứ tự tin nhắn\n"
       "4. Mở chat 1:1 trên web của admin, kiểm tra tin đã gửi",
       "3 tin nhắn text A, B, C",
       "- Hiện thông báo gửi thành công\n"
       "- App LINE: nhận đủ 3 tin, đúng nội dung, đúng thứ tự A, B, C\n"
       "- Chat 1:1 trên web cũng hiển thị 3 tin đó",
       env="PRODUCTION",
       note="Nguồn: r185-r186, r297-r298. RULE-06 + RULE-07.",
       group="API"),

    tc("テスト送信 & 一括テスト送信", "MSG-005", "Abnormal",
       "Gửi thử thất bại — hiện thông báo lỗi, friend KHÔNG nhận được tin",
       PV + "\n- Có friend đã BLOCK bot nhưng vẫn nằm trong danh sách test",
       "1. Thêm friend đã block bot vào danh sách test\n"
       "2. Bấm「テスト送信」cho friend đó\n"
       "3. Đọc thông báo trả về\n"
       "4. Mở app LINE của friend kiểm tra",
       "Friend có is_blocked = 1",
       "- Hiện thông báo gửi thất bại (không báo thành công giả)\n"
       "- Friend KHÔNG nhận được tin nhắn\n"
       "- Bảng message_error có bản ghi lỗi tương ứng",
       env="PRODUCTION",
       note="Nguồn: r187-r188, r299-r300. RULE-08: gửi tin thật → PRODUCTION.",
       group="API"),

    tc("テスト送信 & 一括テスト送信", "UI-001", "Normal",
       "Button 一括テスト送信 mặc định disable khi chưa tích friend nào",
       PV + "\n- Danh sách test có ≥2 friend, chưa tích ai",
       "1. Quan sát button「一括テスト送信」khi chưa tích friend\n"
       "2. Tích chọn 1 friend → quan sát lại button\n"
       "3. Bỏ tích friend đó → quan sát lại",
       "2 friend trong danh sách test",
       "- Chưa tích: button disable\n"
       "- Tích ≥1 friend: button enable\n"
       "- Bỏ tích hết: button quay lại disable",
       note="Nguồn: r189-r192, r301-r304."),

    tc("テスト送信 & 一括テスト送信", "STATE-001", "Normal",
       "Xóa friend đang được tích khỏi danh sách test — button 一括テスト送信 về disable",
       PV + "\n- Danh sách test có 1 friend, đã tích chọn friend đó",
       "1. Tích chọn friend duy nhất → button enable\n"
       "2. Bấm icon xóa friend đó khỏi danh sách test\n"
       "3. Quan sát button「一括テスト送信」",
       "1 friend, đã tích rồi xóa",
       "- Button quay về trạng thái disable\n"
       "- Không giữ lại trạng thái tích của friend đã bị xóa",
       note="Nguồn: r192, r304."),

    tc("テスト送信 & 一括テスト送信", "BULK-001", "Normal",
       "Gửi thử hàng loạt — tất cả friend được tích đều nhận đủ tin, đúng thứ tự",
       PV + "\n- Danh sách test có 5 friend, broadcast có 3 tin nhắn A, B, C",
       "1. Tích chọn cả 5 friend\n"
       "2. Bấm「一括テスト送信」\n"
       "3. Mở app LINE của từng friend trong 5 người\n"
       "4. Quan sát trạng thái button sau khi gửi",
       "5 friend · 3 tin nhắn A, B, C",
       "- Cả 5 friend đều nhận đủ 3 tin, đúng nội dung, đúng thứ tự A, B, C\n"
       "- Sau khi gửi xong, button「一括テスト送信」quay về disable (checkbox bị bỏ tích)",
       env="PRODUCTION",
       note="Nguồn: r194-r195, r306-r307. RULE-06: verify tới app LINE của TỪNG friend.",
       group="API"),

    tc("テスト送信 & 一括テスト送信", "CONC-002", "Abnormal",
       "Double click「一括テスト送信」— mỗi friend chỉ nhận 1 lần",
       PV + "\n- Danh sách test có 3 friend, đã tích cả 3",
       "1. Double click nhanh vào「一括テスト送信」\n"
       "2. Mở app LINE của cả 3 friend đếm số lần nhận",
       "Double click trong < 1 giây, 3 friend",
       "- Mỗi friend chỉ nhận 1 lần bộ tin nhắn\n"
       "- Không friend nào nhận trùng 2 lần",
       env="PRODUCTION",
       note="Nguồn: r193, r305. RULE-08: gửi tin thật → PRODUCTION.",
       group="API"),

    tc("テスト送信 & 一括テスト送信", "MSG-001", "Normal",
       "Gửi thử KHÔNG làm tăng số 配信数 và không đổi trạng thái broadcast",
       PV + "\n- Broadcast wait_to_send, 配信数 = 5, chưa tới giờ gửi",
       "1. Ghi lại 配信数 và tab đang chứa broadcast\n"
       "2. Gửi thử cho 2 friend trong danh sách test\n"
       "3. Về màn list, đọc lại 配信数 và tab chứa broadcast\n"
       "4. Kiểm tra bảng broadcast: status và send_count",
       "配信数 = 5 trước khi gửi thử · gửi thử 2 friend",
       "- 配信数 vẫn là 5, KHÔNG tăng lên 7\n"
       "- Broadcast vẫn ở tab「配信予約」, status vẫn wait_to_send\n"
       "- send_count không thay đổi",
       spec="Đã hỏi leader",
       note="⚠️ Corpus KHÔNG test trực tiếp nhánh này. TC do AI bổ sung — quan trọng vì logic-spec.md:114 "
            "ghi gửi thử có `free_send_count + 1` (tính vào quota bot) nhưng không nói về send_count của "
            "broadcast. Cần Leader xác nhận.",
       group="Data"),

    tc("テスト送信 & 一括テスト送信", "PAY-LIMIT-001", "Normal",
       "Gửi thử có tính vào quota tin nhắn của bot (free_send_count)",
       PV + "\n- Bot đang ở gói Free, đã dùng N tin trong tháng",
       "1. Ghi lại số tin đã dùng ở header (L Message: N/1,000)\n"
       "2. Gửi thử cho 3 friend bằng「一括テスト送信」\n"
       "3. Reload trang, đọc lại số ở header",
       "Bot gói Free, đã dùng N tin · gửi thử 3 friend, mỗi friend 1 tin",
       "- Số ở header tăng đúng 3 (thành N+3)\n"
       "- Bảng bots: free_send_count tăng 3",
       env="PRODUCTION",
       note="Nguồn: logic-spec.md:114 (『Nếu thành công → free_send_count + 1, updateMessageSendCount()』). "
            "⚠️ Corpus không test nhánh này — TC do AI bổ sung từ spec, cần Leader xác nhận. "
            "RULE-08: bill/quota → PRODUCTION.",
       group="Data"),
]
