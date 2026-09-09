# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 1-6: màn danh sách SCR-BC-01, 3 tab, sắp xếp,
lọc theo thời gian, phân trang.

Nguồn chính: 03. TCsLine_Broadcast → tab「Improver send all(task broadcast)」(gid=0,
tab master 02/2024 → 05/2026). Số dòng ghi ở cột Ghi chú theo dạng `r<n>` là dòng
của tab master trừ khi ghi rõ file/tab khác.
"""
from _common import tc

A = ("- Đăng nhập Admin của 1 bot đã liên kết LOA\n"
     "- Vào Sidebar →「メッセージ」→「メッセージ配信」(/basic/message-send-all)")

S1 = [
    # ═══════════ 1. Màn list — layout & Check UI ═══════════
    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Vào màn メッセージ配信 — hiển thị đủ tiêu đề, link manual, cảnh báo trễ, 3 tab, toolbar, bảng",
       A,
       "1. Đăng nhập Admin\n"
       "2. Mở Sidebar →「メッセージ」→「メッセージ配信」\n"
       "3. Quan sát toàn bộ nội dung trang",
       "Bot có sẵn ≥1 broadcast ở mỗi tab",
       "- URL là /basic/message-send-all, trang tải xong không có alert\n"
       "- Có tiêu đề「メッセージ配信」kèm link「マニュアル」\n"
       "- Có dòng cảnh báo「通信状況により配信予定時間から5~15分遅れて配信される場合があります。」\n"
       "- Có đủ 3 tab:「配信予約」·「下書き」·「配信履歴」\n"
       "- Có toolbar:「新規作成」·「全期間」· ô tìm kiếm ·「一括削除」\n"
       "- Console trình duyệt không có lỗi JavaScript",
       note="Nguồn: r3, r10 + ui-spec.md:59-77. Evidence: ảnh full trang."),

    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Check giao diện theo design — căn lề, text, màu, font size, bo góc, độ dày chữ",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Mở file design Adobe XD (link ở tab Info của file TCs gốc)\n"
       "3. So từng vùng: header, tabs, toolbar, bảng, phân trang",
       "Design: xd.adobe.com/view/010df35d-8f5d-4ea6-b225-54f36160f6b1-545e",
       "- Căn lề, text, màu (color), font size, bo góc (border radius), độ dày chữ (font weight) khớp design\n"
       "- Không có vùng nào lệch/tràn so với design",
       note="Nguồn: r3. TC gốc chỉ có tiêu đề『Hiển thị đúng như design』— đã tách rõ 6 thuộc tính cần so. "
            "⚠️ TC từ 02/2024, đã hơn 2 năm — CẦN VERIFY LẠI design còn hiệu lực không."),

    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Hover vào button/icon — đổi màu và con trỏ thành hình bàn tay",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Rê chuột lần lượt qua:「新規作成」·「全期間」·「一括削除」· icon sort · icon preview · icon copy · icon xóa\n"
       "3. Quan sát màu và hình dạng con trỏ",
       "Dùng chuột trên PC (không phải touch)",
       "- Mỗi button/icon đổi màu khi hover\n"
       "- Con trỏ chuyển thành hình bàn tay (pointer), KHÔNG còn là mũi tên",
       note="Nguồn: r4 + file 03/tab function r67."),

    tc("Màn list — layout & Check UI", "UI-002", "Boundary",
       "Màn hình 1366×768 — không vỡ layout, không scroll ngang ngoài ý muốn",
       A + "\n- Đặt cửa sổ trình duyệt về đúng 1366×768",
       "1. Đặt độ phân giải/cửa sổ về 1366×768\n"
       "2. Vào màn メッセージ配信\n"
       "3. Lần lượt mở cả 3 tab và quan sát bảng dữ liệu",
       "1366×768 — độ phân giải nhỏ nhất được hỗ trợ",
       "- Toàn bộ cột của bảng hiển thị được (hoặc scroll ngang trong khung bảng, không phải cả trang)\n"
       "- Không có phần tử nào bị che khuất hoặc chồng lên nhau\n"
       "- Toolbar và phân trang vẫn thao tác được",
       note="Nguồn: r5."),

    tc("Màn list — layout & Check UI", "UI-INPUT-001", "Boundary",
       "Nhập input với dữ liệu độ dài tối đa — không vỡ layout",
       A,
       "1. Vào ô tìm kiếm trên toolbar\n"
       "2. Nhập chuỗi dài tối đa cho phép (ký tự nửa chiều rộng và tiếng Nhật full-width)\n"
       "3. Quan sát ô nhập và các phần tử xung quanh",
       "Chuỗi 255 ký tự latinh + chuỗi 255 ký tự tiếng Nhật (あいうえお…)",
       "- Ô nhập không giãn ra làm vỡ toolbar\n"
       "- Text bị cắt/scroll trong ô, không tràn ra ngoài\n"
       "- Các button bên cạnh vẫn đúng vị trí",
       note="Nguồn: r6."),

    tc("Màn list — layout & Check UI", "UI-INPUT-001", "Normal",
       "Ô nhập text tự động trim khoảng trắng đầu/cuối",
       A + "\n- Có broadcast tên「テスト配信」",
       "1. Vào ô tìm kiếm\n"
       "2. Nhập「  テスト配信  」(có space đầu và cuối)\n"
       "3. Bấm tìm kiếm\n"
       "4. Kiểm tra kết quả và giá trị còn lại trong ô",
       "「  テスト配信  」— 2 space đầu, 2 space cuối",
       "- Kết quả tìm kiếm ra đúng broadcast「テスト配信」(space bị trim)\n"
       "- Không báo lỗi không tìm thấy do space thừa",
       note="Nguồn: r7 + r69."),

    tc("Màn list — layout & Check UI", "LIST-001", "Normal",
       "Scroll dọc khi nhiều bản ghi trên 1 trang",
       A + "\n- Tab 配信予約 có đủ số bản ghi để tràn 1 màn hình (≥30 bản ghi)",
       "1. Vào tab 配信予約\n"
       "2. Cuộn chuột xuống dưới cùng bảng\n"
       "3. Cuộn ngược lên",
       "≥30 broadcast đang chờ gửi",
       "- Cuộn dọc mượt, header bảng và toolbar hoạt động bình thường\n"
       "- Không mất bản ghi nào khi cuộn\n"
       "- Phân trang vẫn nằm dưới cùng bảng",
       note="Nguồn: r8, r386, r675, r774."),

    tc("Màn list — layout & Check UI", "LIST-001", "Normal",
       "Scroll ngang khi bảng rộng hơn khung",
       A + "\n- Cửa sổ trình duyệt hẹp (1280px) để bảng tràn ngang",
       "1. Thu hẹp cửa sổ còn 1280px\n"
       "2. Vào tab 配信予約\n"
       "3. Cuộn ngang trong khung bảng",
       "Cửa sổ 1280px, bảng 9 cột",
       "- Cuộn ngang diễn ra TRONG khung bảng, không làm cả trang trượt ngang\n"
       "- Cột đầu (checkbox) và các cột còn lại vẫn đọc được đầy đủ",
       note="Nguồn: r387, r676, r775."),

    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Link「マニュアル」mở đúng trang hướng dẫn",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Bấm link「マニュアル」cạnh tiêu đề\n"
       "3. Quan sát tab/trang mở ra",
       "—",
       "- Mở trang manual của LME đúng chủ đề メッセージ配信\n"
       "- Mở ở tab mới, tab hiện tại giữ nguyên màn list",
       note="Nguồn: r11. TC gốc chỉ ghi『Như design』— đã tự viết kết quả mong đợi đo lường được "
            "(⚠️ suy luận của AI, cần Leader xác nhận URL manual cụ thể)."),

    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Placeholder và tooltip hiển thị đủ theo design",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Kiểm tra ô tìm kiếm khi chưa nhập gì (placeholder)\n"
       "3. Rê chuột vào từng icon ở cột「操作」để xem tooltip",
       "—",
       "- Ô tìm kiếm có placeholder theo design\n"
       "- Mỗi icon thao tác có tooltip mô tả đúng hành động (sửa / xóa / copy / preview)",
       note="Nguồn: r9."),

    tc("Màn list — layout & Check UI", "FUNC-001", "Normal",
       "Button「新規作成」chuyển sang màn tạo broadcast",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Bấm「新規作成」",
       "—",
       "- Chuyển sang /basic/add-broadcast-v2 (SCR-BC-02), không kèm broadcast_id\n"
       "- Form tạo mới ở trạng thái rỗng",
       note="Nguồn: r14."),

    tc("Màn list — layout & Check UI", "CONC-002", "Abnormal",
       "Double click「新規作成」— chỉ mở 1 màn tạo mới, không tạo 2 bản ghi",
       A,
       "1. Vào màn メッセージ配信\n"
       "2. Double click nhanh vào「新規作成」\n"
       "3. Quay lại màn list, đếm số bản ghi ở tab 下書き",
       "Double click trong < 1 giây",
       "- Chỉ chuyển màn 1 lần, không mở 2 tab\n"
       "- Số bản ghi ở tab 下書き KHÔNG tăng (vì bấm新規作成 chưa tạo bản ghi)",
       note="Nguồn: r15."),

    # ═══════════ 2. Tab 配信予約 — cột & hiển thị ═══════════
    tc("Tab 配信予約 — cột & hiển thị", "LIST-001", "Normal",
       "Tab 配信予約 khi chưa có bản ghi nào — hiển thị empty state",
       A + "\n- Bot chưa có broadcast nào ở trạng thái wait_to_send",
       "1. Vào màn メッセージ配信\n"
       "2. Mở tab「配信予約」",
       "0 broadcast wait_to_send",
       "- Hiển thị đúng câu「配信予約の登録はありません」\n"
       "- Không hiển thị bảng rỗng có header trống hoặc phân trang\n"
       "- Button「一括削除」ở trạng thái disable",
       note="Nguồn: r12 + file 03/tab function r218."),

    tc("Tab 配信予約 — cột & hiển thị", "LIST-001", "Normal",
       "Tab 配信予約 khi có bản ghi — đủ 9 cột đúng thứ tự",
       A + "\n- Có ≥1 broadcast wait_to_send, có filter, có action, đã set quick test",
       "1. Mở tab「配信予約」\n"
       "2. Đọc header bảng từ trái sang phải\n"
       "3. Đối chiếu dữ liệu từng cột của 1 bản ghi với màn chi tiết của chính nó",
       "1 broadcast: tên「予約テスト」, đặt lịch tương lai, có filter tag, có action gán tag, 1 quick tester",
       "- Header đúng thứ tự: checkbox ·「配信予定日時」·「管理用タイトル」·「配信先絞込み」·「配信数」·「送信者名」·「アクション」·「クイックテスト」·「操作」\n"
       "- 配信予定日時 = send_day + send_time của bản ghi\n"
       "- 配信先絞込み hiển thị「設定済み」(vì có filter)\n"
       "- 配信数 = số friend thỏa filter\n"
       "- クイックテスト hiển thị avatar của friend đã tick quick test",
       note="Nguồn: r13 + ui-spec.md:87-99."),

    tc("Tab 配信予約 — cột & hiển thị", "DATA-TEXT-001", "Normal",
       "Cột 配信先絞込み hiển thị「未設定（全員）」khi broadcast không đặt filter",
       A + "\n- Có broadcast wait_to_send chọn すべての友だち (không filter)",
       "1. Mở tab「配信予約」\n"
       "2. Tìm broadcast không đặt filter\n"
       "3. Đọc giá trị cột「配信先絞込み」",
       "Broadcast「全員配信」, flag_setting_filter = 0",
       "- Cột hiển thị「未設定（全員）」\n"
       "- Cột 配信数 hiển thị tổng số bạn bè của bot (không tính người đã block)",
       note="Nguồn: r141-r142 + logic-spec.md:91-92."),

    tc("Tab 配信予約 — cột & hiển thị", "LIST-001", "Normal",
       "Broadcast nhiều lịch gửi — màn list hiển thị đủ các mốc thời gian, giảm dần",
       A + "\n- Có 1 broadcast đặt 3 mốc gửi khác nhau trong tương lai",
       "1. Tạo broadcast có 3 mốc gửi: 10:00, 14:00, 18:00 cùng ngày mai\n"
       "2. Lưu và về màn list\n"
       "3. Mở tab「配信予約」, quan sát các dòng của broadcast đó",
       "3 mốc: mai 10:00 / mai 14:00 / mai 18:00",
       "- Hiển thị đủ 3 mốc thời gian (bản ghi cha + 2 bản ghi con)\n"
       "- Sắp xếp theo thứ tự giảm dần của thời gian gửi\n"
       "- Mỗi dòng dùng chung tên quản lý, filter, số 配信数 với bản ghi cha",
       note="Nguồn: r48-r53. ⚠️ Xem MT-02 — corpus có 2 mô tả khác nhau về thứ tự (『giảm dần』ở r48 "
            "và『từ bé đến lớn』ở r75)."),

    tc("Tab 配信予約 — cột & hiển thị", "DATA-COUNT-001", "Normal",
       "Cột 配信数 ở tab 配信予約 hiển thị số dự kiến (filter_number), chưa phải số đã gửi",
       A + "\n- Có broadcast wait_to_send, filter theo tag T, tag T đang gắn cho 5 friend",
       "1. Mở tab「配信予約」\n"
       "2. Đọc số ở cột「配信数」của broadcast đó\n"
       "3. Vào màn chi tiết broadcast, đọc số ở phần「配信先絞込み」",
       "Tag T gắn 5 friend, chưa ai bị block",
       "- Cột 配信数 hiển thị 5\n"
       "- Số ở màn list và màn chi tiết KHỚP nhau\n"
       "- Đây là số dự kiến (filter_number), broadcast chưa gửi nên chưa có send_count",
       note="Nguồn: r146 + logic-spec.md:94 (`number_send`: send_count nếu delivered, rỗng nếu chưa)."),

    # ═══════════ 3. Tab 下書き — cột & hiển thị ═══════════
    tc("Tab 下書き — cột & hiển thị", "LIST-001", "Normal",
       "Tab 下書き khi chưa có bản ghi nào — hiển thị empty state",
       A + "\n- Bot chưa có broadcast nào ở trạng thái draft/unregistered/not_delivery",
       "1. Mở tab「下書き」",
       "0 broadcast draft",
       "- Hiển thị đúng câu「下書きの登録はありません」\n"
       "- Button「一括削除」disable",
       note="Nguồn: r389 + file 03/tab function r219."),

    tc("Tab 下書き — cột & hiển thị", "LIST-001", "Normal",
       "Tab 下書き khi có bản ghi — có thêm cột 作成・更新日時, KHÔNG có cột クイックテスト",
       A + "\n- Có ≥1 broadcast draft",
       "1. Mở tab「下書き」\n"
       "2. Đọc header bảng từ trái sang phải\n"
       "3. So sánh với header của tab「配信予約」",
       "1 broadcast draft tên「下書きテスト」",
       "- Header có: checkbox ·「作成・更新日時」·「管理用タイトル」·「配信予定日時」·「配信先絞込み」·「配信数」·「送信者名」·「アクション」·「操作」\n"
       "- KHÔNG có cột「クイックテスト」\n"
       "- 作成・更新日時 = broadcast.updated_at (hoặc created_at nếu chưa sửa)",
       note="Nguồn: r390 + ui-spec.md:103-115. ⚠️ Xem MT-06 — corpus r436-r438 vẫn test クイックテスト "
            "ở màn đăng ký của luồng 下書き."),

    tc("Tab 下書き — cột & hiển thị", "FUNC-DRAFT-001", "Normal",
       "Bản nháp có 配信予定日時 đã qua vẫn KHÔNG bị job gửi",
       A + "\n- Có broadcast status=draft, send_day/send_time đặt ở quá khứ (VD hôm qua 10:00)",
       "1. Tạo broadcast, nhập đủ tiêu đề + tin nhắn, đặt lịch quá khứ\n"
       "2. Bấm「下書きとして保存」\n"
       "3. Chờ qua 2 chu kỳ poll của job (≥ 1 phút)\n"
       "4. Mở tab「下書き」và tab「配信履歴」\n"
       "5. Kiểm tra hộp thoại LINE của 1 friend thuộc đối tượng nhận",
       "send_day = hôm qua, send_time = 10:00, status = draft",
       "- Broadcast vẫn nằm ở tab「下書き」, KHÔNG chuyển sang「配信履歴」\n"
       "- Friend KHÔNG nhận được tin nhắn nào\n"
       "- Bảng broadcast: status vẫn = 'draft', send_count vẫn NULL",
       env="PRODUCTION",
       note="Nguồn: ui-spec.md:117「配信予定日時が現在日時より前の場合でも、下書きの場合は配信されません。」 "
            "+ [AI] alert_limit r47 (TC-BAL-046). RULE-08: liên quan job nền → chạy PRODUCTION."),

    # ═══════════ 4. Tab 配信履歴 — cột & hiển thị ═══════════
    tc("Tab 配信履歴 — cột & hiển thị", "LIST-001", "Normal",
       "Tab 配信履歴 khi chưa có bản ghi nào — hiển thị empty state",
       A + "\n- Bot chưa gửi broadcast nào",
       "1. Mở tab「配信履歴」",
       "0 broadcast delivered/delivering/send_false",
       "- Hiển thị đúng câu「配信履歴はありません」",
       note="Nguồn: r678 + file 03/tab function r220."),

    tc("Tab 配信履歴 — cột & hiển thị", "LIST-001", "Normal",
       "Tab 配信履歴 — KHÔNG có checkbox, KHÔNG có 一括削除, KHÔNG có クイックテスト",
       A + "\n- Có ≥1 broadcast đã gửi xong",
       "1. Mở tab「配信履歴」\n"
       "2. Đọc header bảng\n"
       "3. Quan sát toolbar phía trên bảng",
       "1 broadcast delivered",
       "- Header có: 「配信日時」·「管理用タイトル」·「配信先絞込み」·「配信数」·「送信者名」·「アクション」·「操作」\n"
       "- KHÔNG có cột checkbox ở đầu dòng\n"
       "- KHÔNG có button「一括削除」khả dụng cho tab này\n"
       "- KHÔNG có cột「クイックテスト」",
       note="Nguồn: r677-r678 + ui-spec.md:119-133."),

    tc("Tab 配信履歴 — cột & hiển thị", "LIST-001", "Normal",
       "Tab 配信履歴 mặc định — bản ghi mới nhất lên đầu, hiển thị toàn bộ dữ liệu",
       A + "\n- Có ≥5 broadcast đã gửi ở nhiều tháng khác nhau",
       "1. Mở tab「配信履歴」\n"
       "2. Đọc thứ tự các bản ghi theo cột「配信日時」\n"
       "3. Kiểm tra bộ lọc thời gian ở toolbar",
       "5 broadcast gửi ở 3 tháng khác nhau",
       "- Bản ghi có 配信日時 mới nhất nằm trên đầu\n"
       "- Hiển thị toàn bộ bản ghi (không mặc định lọc theo tháng hiện tại)\n"
       "- Bộ lọc thời gian ở trạng thái rỗng (null)",
       note="Nguồn: r679, r683 + file 03/tab function r96 (ghi nhận bug cũ『đang hiển thị 2 tháng nhưng "
            "data hiển thị là all >> mong muốn: time để null』— đã fix, TC này verify trạng thái đúng)."),

    tc("Tab 配信履歴 — cột & hiển thị", "LIST-001", "Normal",
       "Broadcast nhiều lịch gửi — tab 配信履歴 hiển thị mốc gửi gần nhất",
       A + "\n- Có 1 broadcast 3 mốc gửi, cả 3 mốc đều đã gửi xong",
       "1. Tạo broadcast 3 mốc gửi liên tiếp cách nhau 5 phút, đều ở quá khứ gần\n"
       "2. Chờ job gửi hết cả 3 mốc\n"
       "3. Mở tab「配信履歴」và quan sát dòng của broadcast đó",
       "3 mốc: 09:00 / 09:05 / 09:10 hôm nay",
       "- Hiển thị mốc thời gian của bản ghi con gửi GẦN NHẤT (09:10)\n"
       "- Không hiển thị lặp 3 dòng cho cùng 1 broadcast",
       env="PRODUCTION",
       note="Nguồn: r679. ⚠️ Xem MT-07 — file 03/tab function r21 ghi nhận『màn đã send đang hiển thị hết "
            "tất cả thằng con』, mâu thuẫn với kết quả mong đợi ở r679. RULE-08: cần job thật."),

    tc("Tab 配信履歴 — cột & hiển thị", "OUT-TRUTH-001", "Normal",
       "Tiêu đề trang danh sách friend đã gửi của broadcast là「一斉配信（送信済み友だち）」",
       A + "\n- Có broadcast đã gửi xong cho ≥3 friend",
       "1. Mở tab「配信履歴」\n"
       "2. Bấm vào số ở cột「配信数」của broadcast đó\n"
       "3. Đọc tiêu đề của trang vừa mở",
       "Broadcast「配信テスト」đã gửi cho 3 friend",
       "- Tiêu đề trang hiển thị「一斉配信（送信済み友だち）」\n"
       "- KHÔNG hiển thị「ステップ配信（送信済み友だち）」",
       note="Nguồn: r923 (Bug KH #35506, 01/04/2026). Đây là bản ghi mới nhất về hành vi này."),

    tc("Tab 配信履歴 — cột & hiển thị", "OUT-TRUTH-001", "Normal",
       "Cùng màn friend đã gửi nhưng vào từ scenario — tiêu đề là「ステップ配信（送信済み友だち）」",
       A + "\n- Có 1 scenario đã gửi step message cho ≥3 friend",
       "1. Vào「ステップ配信」→ mở scenario đã gửi\n"
       "2. Bấm vào số lượng người đã gửi\n"
       "3. Đọc tiêu đề trang",
       "Scenario「ステップテスト」đã gửi cho 3 friend",
       "- Tiêu đề trang hiển thị「ステップ配信（送信済み友だち）」\n"
       "- Không bị lẫn sang tiêu đề của broadcast",
       note="Nguồn: r924 (Bug KH #35506). Giữ trong tab FA-008 vì là cặp đối chứng của TC trên — "
            "cùng 1 trang dùng chung, fix ở FA-008 làm hỏng nhánh này là hồi quy."),

    # ═══════════ 5. Sắp xếp & lọc theo thời gian ═══════════
    tc("Sắp xếp & lọc theo thời gian", "UI-001", "Normal",
       "Icon sort ở cột 配信予定日時 là icon vector, không phải file ảnh",
       A + "\n- Tab 配信予約 có ≥2 bản ghi",
       "1. Mở tab「配信予約」\n"
       "2. Bấm chuột phải vào icon sort ở header cột「配信予定日時」\n"
       "3. Kiểm tra bằng DevTools xem phần tử là icon font/SVG hay thẻ <img>",
       "—",
       "- Icon được render bằng icon font hoặc SVG\n"
       "- KHÔNG phải thẻ <img> trỏ tới file ảnh",
       note="Nguồn: r234, r685."),

    tc("Sắp xếp & lọc theo thời gian", "LIST-001", "Normal",
       "Sort tăng dần theo 配信予定日時 ở tab 配信予約",
       A + "\n- Tab 配信予約 có ≥5 bản ghi với thời gian gửi khác nhau",
       "1. Mở tab「配信予約」\n"
       "2. Bấm icon sort ở cột「配信予定日時」để chọn tăng dần\n"
       "3. Đọc lần lượt giá trị cột đó từ trên xuống",
       "5 broadcast: mai 08:00 / mai 12:00 / mai 20:00 / ngày kia 09:00 / ngày kia 15:00",
       "- Danh sách sắp xếp từ thời gian sớm nhất đến muộn nhất\n"
       "- Không có bản ghi nào bị mất hoặc lặp",
       note="Nguồn: r235 + file 03/tab function r44."),

    tc("Sắp xếp & lọc theo thời gian", "LIST-001", "Normal",
       "Sort giảm dần theo 配信予定日時 ở tab 配信予約",
       A + "\n- Tab 配信予約 có ≥5 bản ghi với thời gian gửi khác nhau",
       "1. Mở tab「配信予約」\n"
       "2. Bấm icon sort để chọn giảm dần\n"
       "3. Đọc lần lượt giá trị cột「配信予定日時」từ trên xuống",
       "Cùng bộ 5 broadcast như TC sort tăng dần",
       "- Danh sách sắp xếp từ thời gian muộn nhất đến sớm nhất",
       note="Nguồn: r236 + file 03/tab function r43."),

    tc("Sắp xếp & lọc theo thời gian", "LIST-001", "Abnormal",
       "Broadcast nhiều lịch — bản ghi con có thời gian sớm hơn cha vẫn phải xếp đúng thứ tự",
       A + "\n- Tạo broadcast cha đặt lịch mai 18:00, sau đó thêm mốc con mai 09:00",
       "1. Tạo broadcast, mốc đầu (cha) = mai 18:00\n"
       "2. Thêm mốc gửi thứ hai = mai 09:00\n"
       "3. Lưu, về màn list tab「配信予約」\n"
       "4. Sort tăng dần theo 配信予定日時\n"
       "5. Đọc thứ tự 2 dòng của broadcast đó",
       "Cha: mai 18:00 · Con: mai 09:00",
       "- Dòng mai 09:00 (con) đứng TRƯỚC dòng mai 18:00 (cha)\n"
       "- Thứ tự tính theo giá trị thời gian, KHÔNG theo quan hệ cha/con",
       note="Nguồn: r75 — kết quả gốc ghi NG『time con bé hơn cha ngoài màn list đang hiển thị cha trước』. "
            "TC này viết theo hành vi ĐÚNG, dự kiến FAIL nếu bug chưa fix → cần raise bug."),

    tc("Sắp xếp & lọc theo thời gian", "LIST-001", "Abnormal",
       "Sort ở tab 配信履歴 — verify lại sau khi corpus ghi nhận NG",
       A + "\n- Tab 配信履歴 có ≥5 bản ghi đã gửi ở nhiều thời điểm",
       "1. Mở tab「配信履歴」\n"
       "2. Bấm icon sort ở cột「配信日時」, chọn tăng dần → đọc thứ tự\n"
       "3. Bấm tiếp để chọn giảm dần → đọc thứ tự",
       "5 broadcast đã gửi, thời gian gửi cách nhau ≥1 ngày",
       "- Tăng dần: sớm nhất lên đầu · Giảm dần: muộn nhất lên đầu\n"
       "- Cả 2 chiều đều đúng, không bị bỏ sót bản ghi",
       note="Nguồn: r686-r687 — kết quả gốc là NG cho cả 2 chiều. TC này viết theo hành vi ĐÚNG, "
            "dự kiến FAIL nếu chưa fix → cần raise bug."),

    tc("Sắp xếp & lọc theo thời gian", "LIST-001", "Normal",
       "Sort giữ đúng khi chuyển trang",
       A + "\n- Tab 配信予約 có > 1 trang bản ghi",
       "1. Mở tab「配信予約」, sort tăng dần\n"
       "2. Chuyển sang trang 2\n"
       "3. Đọc bản ghi đầu tiên của trang 2 và bản ghi cuối của trang 1",
       "≥60 broadcast wait_to_send",
       "- Bản ghi đầu trang 2 có thời gian ≥ bản ghi cuối trang 1\n"
       "- Chiều sort không bị reset khi chuyển trang",
       note="Nguồn: r237, r688 + file 03/tab function r45-r46."),

    tc("Sắp xếp & lọc theo thời gian", "STATE-CLEAN-001", "Normal",
       "Reload trang — sort quay về mặc định, không ảnh hưởng màn khác",
       A + "\n- Tab 配信予約 đang sort tăng dần",
       "1. Sort tăng dần ở tab「配信予約」\n"
       "2. Nhấn F5 reload trang\n"
       "3. Đọc thứ tự bản ghi\n"
       "4. Sang tab「下書き」và「配信履歴」, kiểm tra thứ tự",
       "—",
       "- Sau reload, tab 配信予約 quay về thứ tự mặc định (DESC theo send_day, send_time, id)\n"
       "- Tab 下書き và 配信履歴 không bị đổi thứ tự theo\n"
       "- Các màn hình khác của tool không bị ảnh hưởng",
       note="Nguồn: r244, r693 + logic-spec.md:89 (『Sort mặc định DESC theo send_day, send_time, id』)."),

    tc("Sắp xếp & lọc theo thời gian", "FUNC-DATE-001", "Normal",
       "Bộ lọc theo tháng ở tab 配信予約 — mặc định là tháng hiện tại",
       A + "\n- Có broadcast wait_to_send ở tháng này và tháng sau",
       "1. Mở tab「配信予約」\n"
       "2. Đọc giá trị đang chọn ở bộ lọc thời gian\n"
       "3. Đếm số bản ghi hiển thị",
       "2 broadcast tháng này, 2 broadcast tháng sau",
       "- Bộ lọc mặc định là tháng hiện tại\n"
       "- Chỉ hiển thị 2 broadcast có 配信予定日時 thuộc tháng hiện tại",
       note="Nguồn: r366-r367."),

    tc("Sắp xếp & lọc theo thời gian", "FUNC-DATE-001", "Normal",
       "Chuyển sang tháng tiếp theo và lùi về tháng trước",
       A + "\n- Có broadcast wait_to_send ở tháng trước, tháng này, tháng sau",
       "1. Mở tab「配信予約」\n"
       "2. Bấm icon「>」để sang tháng tiếp theo → đếm bản ghi\n"
       "3. Bấm icon「<」hai lần để lùi về tháng trước → đếm bản ghi",
       "Mỗi tháng 2 broadcast",
       "- Icon「>」luôn enable, chuyển đúng sang tháng kế tiếp\n"
       "- Sang tháng sau: chỉ hiện 2 broadcast của tháng sau\n"
       "- Lùi tháng trước: chỉ hiện 2 broadcast của tháng trước",
       note="Nguồn: r368-r369 + file 03/tab function r94-r95."),

    tc("Sắp xếp & lọc theo thời gian", "FUNC-001", "Normal",
       "Button「全期間」hiển thị toàn bộ bản ghi bất kể tháng",
       A + "\n- Có broadcast wait_to_send trải trên ≥3 tháng khác nhau",
       "1. Mở tab「配信予約」(đang lọc tháng hiện tại)\n"
       "2. Bấm button「全期間」\n"
       "3. Đếm số bản ghi hiển thị và so với tổng số broadcast wait_to_send trong DB",
       "6 broadcast trải 3 tháng",
       "- Hiển thị đủ 6 bản ghi\n"
       "- Bộ lọc tháng không còn giới hạn kết quả",
       note="Nguồn: r370, r372, r680, r682."),

    tc("Sắp xếp & lọc theo thời gian", "CONC-002", "Abnormal",
       "Double click「全期間」— chỉ gọi 1 lần, không nhân đôi bản ghi",
       A + "\n- Tab 配信予約 có ≥6 bản ghi trải nhiều tháng",
       "1. Mở tab「配信予約」\n"
       "2. Double click nhanh vào「全期間」\n"
       "3. Đếm số bản ghi hiển thị\n"
       "4. Mở DevTools → tab Network, đếm số request gửi đi",
       "Double click trong < 1 giây",
       "- Chỉ 1 request được gửi\n"
       "- Danh sách hiển thị đúng số bản ghi, không lặp dòng",
       note="Nguồn: r371, r681."),

    tc("Sắp xếp & lọc theo thời gian", "FUNC-001", "Normal",
       "Các chức năng khác vẫn hoạt động sau khi đổi sort/lọc",
       A + "\n- Tab 配信予約 đang sort tăng dần và lọc「全期間」",
       "1. Sort tăng dần + bấm「全期間」\n"
       "2. Lần lượt thử: lọc theo tháng · chọn nhiều bản ghi rồi xóa · tạo mới · sửa 1 bản ghi · mở preview/test\n"
       "3. Sau mỗi thao tác quay lại màn list kiểm tra",
       "—",
       "- Cả 5 chức năng đều thao tác được bình thường\n"
       "- Sau mỗi thao tác, danh sách vẫn giữ đúng bộ lọc/sort đang chọn (trừ khi reload trang)",
       note="Nguồn: r238-r243, r689-r692."),

    # ═══════════ 6. Phân trang & số dòng hiển thị ═══════════
    tc("Phân trang & số dòng hiển thị", "LIST-001", "Boundary",
       "Ít hơn 1 trang bản ghi — không hiển thị thanh phân trang",
       A + "\n- Tab 配信予約 có 3 bản ghi",
       "1. Mở tab「配信予約」\n"
       "2. Quan sát phía dưới bảng",
       "3 broadcast wait_to_send",
       "- Không hiển thị thanh phân trang (số trang, icon < >)\n"
       "- Chỉ có thể hiển thị dòng tổng số bản ghi",
       note="Nguồn: r378, r766."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Boundary",
       "Số bản ghi tối đa trên 1 trang ở tab 配信予約 và 下書き",
       A + "\n- Tab 配信予約 có ≥120 bản ghi",
       "1. Mở tab「配信予約」, bấm「全期間」\n"
       "2. Đếm số dòng hiển thị trên trang 1\n"
       "3. Lặp lại với tab「下書き」",
       "120 broadcast wait_to_send, 120 broadcast draft",
       "- Mỗi trang hiển thị đúng số dòng theo quy định (corpus ghi 50 dòng/trang)\n"
       "- Số trang = ceil(tổng bản ghi / số dòng mỗi trang)",
       spec="Đã hỏi leader",
       note="Nguồn: r379, r767 (『50 bản ghi/1 trang』). ⚠️ MT-01 — ui-spec.md:134,140 nói tab 配信履歴 "
            "có dropdown「表示件数」100/200/500 và 2 tab kia『không thấy』; corpus nói 50. Cần Leader chốt."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Normal",
       "Dropdown「表示件数」ở tab 配信履歴 — đổi số dòng hiển thị",
       A + "\n- Tab 配信履歴 có ≥250 bản ghi đã gửi",
       "1. Mở tab「配信履歴」\n"
       "2. Kiểm tra có dropdown「表示件数」không\n"
       "3. Chọn lần lượt 100件 → 200件 → 500件, mỗi lần đếm số dòng trang 1",
       "250 broadcast delivered",
       "- Có dropdown「表示件数」với 3 lựa chọn 100件 / 200件 / 500件\n"
       "- Chọn 100件 → trang 1 có 100 dòng, có 3 trang\n"
       "- Chọn 200件 → trang 1 có 200 dòng, có 2 trang\n"
       "- Chọn 500件 → hiển thị hết 250 dòng trên 1 trang, không có phân trang",
       spec="Đã hỏi leader",
       note="⚠️ MT-01 — chỉ có trong ui-spec.md:134,140; corpus TCs KHÔNG có TC nào cho dropdown này. "
            "TC do AI viết từ spec, cần Leader xác nhận dropdown có thật trên production."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Boundary",
       "Ở trang cuối — không có icon chuyển sang trang sau",
       A + "\n- Tab 配信予約 có 3 trang bản ghi",
       "1. Mở tab「配信予約」, bấm「全期間」\n"
       "2. Chuyển tới trang cuối (trang 3)\n"
       "3. Quan sát icon「>」",
       "3 trang bản ghi",
       "- Icon「>」bị ẩn hoặc disable, bấm không có tác dụng\n"
       "- Không nhảy sang trang 4 rỗng",
       note="Nguồn: r380, r768."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Normal",
       "Ở các trang không phải trang cuối — icon「>」khả dụng",
       A + "\n- Tab 配信予約 có 3 trang bản ghi",
       "1. Mở tab「配信予約」ở trang 1\n"
       "2. Bấm icon「>」→ sang trang 2\n"
       "3. Bấm tiếp「>」→ sang trang 3",
       "3 trang bản ghi",
       "- Icon「>」enable ở trang 1 và 2\n"
       "- Mỗi lần bấm chuyển đúng 1 trang, dữ liệu khớp với vị trí trang",
       note="Nguồn: r381, r769."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Boundary",
       "Ở trang 1 — không có icon chuyển về trang trước",
       A + "\n- Tab 配信予約 có ≥2 trang bản ghi",
       "1. Mở tab「配信予約」ở trang 1\n"
       "2. Quan sát icon「<」",
       "≥2 trang bản ghi",
       "- Icon「<」bị ẩn hoặc disable\n"
       "- Không nhảy về trang 0",
       note="Nguồn: r382, r770."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Normal",
       "Từ trang 2 trở đi — icon「<」khả dụng",
       A + "\n- Tab 配信予約 có ≥3 trang bản ghi",
       "1. Chuyển tới trang 3\n"
       "2. Bấm icon「<」→ về trang 2\n"
       "3. Bấm tiếp「<」→ về trang 1",
       "3 trang bản ghi",
       "- Icon「<」enable từ trang 2 trở đi\n"
       "- Mỗi lần bấm lùi đúng 1 trang, dữ liệu khớp vị trí trang",
       note="Nguồn: r383, r771."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Normal",
       "Bấm trực tiếp số trang bất kỳ — dữ liệu khớp đúng trang được chọn",
       A + "\n- Tab 配信予約 có 3 trang bản ghi, đang sort tăng dần",
       "1. Ghi lại bản ghi đầu và cuối của từng trang bằng cách duyệt tuần tự\n"
       "2. Về trang 1, bấm thẳng vào số「3」\n"
       "3. So bản ghi hiển thị với danh sách đã ghi",
       "3 trang bản ghi",
       "- Trang 3 hiển thị đúng bộ bản ghi đã ghi nhận ở bước 1\n"
       "- Không bị lệch dòng hay lặp bản ghi giữa các trang",
       note="Nguồn: r384, r772."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Normal",
       "Chức năng chung vẫn hoạt động ở trang không phải trang 1",
       A + "\n- Tab 配信予約 có ≥2 trang bản ghi",
       "1. Chuyển sang trang 2\n"
       "2. Lần lượt thử: tick checkbox → 一括削除 · mở preview/test · bấm sửa 1 bản ghi · hover vào 配信数\n"
       "3. Quay lại kiểm tra kết quả từng thao tác",
       "≥2 trang bản ghi",
       "- Tất cả thao tác đều đúng với bản ghi ở trang 2, không tác động nhầm bản ghi trang 1\n"
       "- Sau khi xóa, danh sách trang 2 cập nhật đúng",
       note="Nguồn: r385, r773 + r938, r949 (hover ở page 2 / page cuối)."),

    tc("Phân trang & số dòng hiển thị", "LIST-001", "Abnormal",
       "Chuyển trang ở tab 配信履歴 — số trang không bị giảm bất thường",
       A + "\n- Tab 配信履歴 có ≥8 trang bản ghi",
       "1. Mở tab「配信履歴」, bấm「全期間」\n"
       "2. Ghi lại tổng số trang hiển thị\n"
       "3. Bấm sang trang 2\n"
       "4. Đọc lại tổng số trang",
       "8 trang bản ghi đã gửi",
       "- Tổng số trang sau khi chuyển trang vẫn là 8\n"
       "- Không bị tụt xuống 2 hoặc số khác",
       note="Nguồn: file 03/tab function r99 — ghi nhận bug『click sang trang khác thì sl trang bị giảm "
            "từ 8 xuống còn 2』và r58『sang trang đang bị lỗi nên k test được』. TC viết theo hành vi ĐÚNG."),

    tc("Phân trang & số dòng hiển thị", "DATA-COUNT-001", "Normal",
       "Dòng tổng số bản ghi hiển thị đúng định dạng và đúng số",
       A + "\n- Tab 配信予約 có đúng 7 bản ghi",
       "1. Mở tab「配信予約」, bấm「全期間」\n"
       "2. Đọc dòng tổng số phía dưới bảng\n"
       "3. Đếm tay số dòng trong bảng",
       "7 broadcast wait_to_send",
       "- Dòng tổng hiển thị dạng「全7件中 1-7件を表示」\n"
       "- Số trong dòng tổng khớp với số dòng đếm tay",
       note="Nguồn: ui-spec.md:100 (「全0件中 1-0件を表示」). Con số trong TC là ví dụ cụ thể hóa."),
]

# ── Bổ sung sau audit coverage: 2 phần tử của toolbar mà corpus KHÔNG test ──
S1 += [
    tc("Màn list — layout & Check UI", "LIST-001", "Normal",
       "Ô tìm kiếm broadcast — lọc đúng theo 管理用タイトル",
       A + "\n- Tab「配信履歴」có broadcast tên「春のキャンペーン」và「夏のキャンペーン」",
       "1. Mở tab「配信履歴」\n"
       "2. Nhập「春」vào ô tìm kiếm, xác nhận tìm\n"
       "3. Đếm kết quả\n"
       "4. Nhập「キャンペーン」→ đếm kết quả\n"
       "5. Xóa trắng ô tìm kiếm → đếm kết quả",
       "「春」·「キャンペーン」· ô trống",
       "- Nhập「春」: chỉ hiện broadcast「春のキャンペーン」\n"
       "- Nhập「キャンペーン」: hiện cả 2 broadcast\n"
       "- Xóa trắng: hiện lại toàn bộ danh sách",
       spec="Đã hỏi leader",
       note="⚠️ Corpus KHÔNG có TC nào cho ô tìm kiếm. TC do AI bổ sung từ ui-spec.md:77 "
            "(『Ô tìm kiếm | (không label) | Textbox | Toolbar giữa | Tìm kiếm broadcast』). "
            "Cần Leader xác nhận ô này tìm theo trường nào (chỉ 管理用タイトル hay cả nội dung tin nhắn) "
            "và có ở cả 3 tab hay chỉ tab 配信履歴 (ui-spec.md:134 nói tab 配信履歴 'có thêm' ô tìm kiếm)."),

    tc("Màn list — layout & Check UI", "UI-001", "Normal",
       "Nút「Choose File」ở cuối trang — xác định dùng để làm gì",
       A,
       "1. Cuộn xuống cuối màn list\n"
       "2. Ghi lại có nút「Choose File」không và nhãn kèm theo\n"
       "3. Nếu có: bấm vào, ghi lại loại file được chấp nhận\n"
       "4. Thử chọn 1 file CSV hợp lệ và quan sát hành vi",
       "1 file CSV mẫu",
       "- Ghi rõ nút có tồn tại trên production không\n"
       "- Nếu có: ghi rõ chức năng thật (import broadcast từ CSV hay việc khác) và định dạng chấp nhận\n"
       "- Nếu không dùng tới: đề xuất gỡ khỏi giao diện",
       spec="Đã hỏi leader",
       note="⚠️ Corpus chỉ có 1 dòng trống ghi「csv」ở file 03/tab「test filte」r26, không có nội dung test. "
            "ui-spec.md:101 ghi『Nút「Choose File」ở cuối trang (có thể import CSV)』và feature-spec.md §9 "
            "U-06 để ngỏ câu hỏi này (ưu tiên Thấp). TC do AI bổ sung để đóng U-06 — cần Leader xác nhận."),
]
