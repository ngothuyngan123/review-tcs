# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 6: group chat, realtime & typing, bộ đếm chưa xác nhận, lịch sử chat,
giới hạn plan & token, phân quyền và môi trường."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3"
GRP = BOT + "\n- Bot A đang ở trong nhóm LINE G1 có ≥3 thành viên"

S6 = [
    # ═══════════════ Group chat ═══════════════
    tc("Group chat", "INTG-LINE-001", "Normal",
       "Bot được thêm vào nhóm LINE mới — tự tạo hội thoại nhóm",
       BOT + "\n- Có nhóm LINE G_new chưa có bot A",
       "1. Trên app LINE: thêm bot A vào nhóm G_new\n2. Mở /basic/chat-v3, chọn filter グループ\n"
       "3. Kiểm tra DB: bản ghi hội thoại của G_new và trường phân loại hội thoại",
       "Nhóm G_new, thêm bot vào nhóm",
       "- Hội thoại của G_new xuất hiện trong danh sách khi lọc グループ\n"
       "- DB: có bản ghi hội thoại mới với trường phân loại = nhóm (giá trị 1)",
       env="PRODUCTION",
       note="Verify DB + màn hình. Nguồn: Group chat r3"),

    tc("Group chat", "INTG-LINE-001", "Normal",
       "Nhóm LINE cũ (bot đã ở sẵn) gửi tin — hội thoại nhóm được tạo",
       BOT + "\n- Bot A đã ở trong nhóm G_old từ trước nhưng LME chưa có bản ghi",
       "1. Cho 1 thành viên trong G_old gửi tin đến nhóm\n2. Mở chat 1:1, lọc グループ\n3. Kiểm tra DB",
       "Nhóm G_old, có tin nhắn mới",
       "- Hội thoại của G_old xuất hiện trong danh sách\n- DB: bản ghi hội thoại mới với phân loại = nhóm",
       env="PRODUCTION",
       note="Nguồn: Group chat r5"),

    tc("Group chat", "INTG-LINE-001", "Normal",
       "Bot rời nhóm và được thêm lại — trạng thái chặn của hội thoại thay đổi tương ứng",
       GRP,
       "1. Trên app LINE: xoá bot A khỏi nhóm G1\n2. Kiểm tra DB trường trạng thái chặn của hội thoại G1\n"
       "3. Quan sát dòng G1 ở chat 1:1\n4. Thêm lại bot A vào G1 → kiểm tra DB và màn hình",
       "Nhóm G1: xoá bot rồi thêm lại",
       "- Sau khi xoá bot: trạng thái chặn = 1, dòng G1 hiển thị trạng thái đã chặn\n"
       "- Sau khi thêm lại: trạng thái chặn = 0, hội thoại dùng lại được bình thường",
       env="PRODUCTION",
       note="Nguồn: Group chat r4, r6"),

    tc("Group chat", "UI-FIELD-001", "Normal",
       "Thông tin nhóm ở cột phải — tên nhóm, ngày thêm, ghi chú và liên kết hướng dẫn",
       GRP,
       "1. Chọn hội thoại nhóm G1 → quan sát cột phải\n"
       "2. Đọc tên nhóm, ngày giờ được thêm vào nhóm, phần ghi chú và tên đội quản lý\n"
       "3. Bấm nút cập nhật thông tin → kiểm tra dữ liệu\n4. Bấm liên kết 公式マニュアル",
       "Nhóm G1",
       "- Cột phải hiện: tên nhóm LINE, ngày giờ được thêm (định dạng 2024.10.15 13:56), phần ghi chú lưu ý\n"
       "- Bấm nút cập nhật: lấy lại thông tin nhóm mới nhất\n"
       "- Bấm 公式マニュアル: mở trang hướng dẫn ở tab mới",
       note="Nguồn: Content: Hiển thị msg r1310-r1318"),

    tc("Group chat", "PERM-001", "Normal",
       "Nhóm — ẩn các mục không áp dụng ở cột phải",
       GRP,
       "1. Chọn hội thoại nhóm G1\n2. Kiểm tra ở cột phải có các mục: システム表示名, 友だち情報, タグ\n"
       "3. So sánh với cột phải của 1 friend cá nhân",
       "Nhóm G1 vs friend cá nhân",
       "- Với nhóm: 3 mục システム表示名, 友だち情報, タグ đều bị ẨN\n"
       "- Với friend cá nhân: 3 mục này hiển thị bình thường",
       spec="Spec không ghi",
       note="MT-14: spec chat-11 không có quy tắc nào cho nhóm. Nguồn: Group chat r15-r17"),

    tc("Group chat", "FUNC-001", "Normal",
       "Nhóm — bookmark, 対応ステータス, ghi chú và bộ lọc hoạt động như bạn bè cá nhân",
       GRP,
       "1. Bookmark nhóm G1 → kiểm tra vị trí trong danh sách và DB\n"
       "2. Gán 対応ステータス cho G1 → kiểm tra badge\n"
       "3. Tạo ghi chú cho G1 → kiểm tra tab メモ\n"
       "4. Lọc theo tag và theo trạng thái đối ứng → kiểm tra G1 có xuất hiện đúng không",
       "Nhóm G1",
       "- Bookmark: G1 lên đầu danh sách, DB lưu đúng\n"
       "- 対応ステータス: badge hiện đúng text và màu\n- Ghi chú: tạo và hiển thị được\n"
       "- Bộ lọc: G1 xuất hiện đúng theo điều kiện lọc",
       note="Gộp vì cùng dạng kết quả. Nguồn: Group chat r12, r18, r19, r20"),

    tc("Group chat", "FUNC-001", "Normal",
       "Ẩn nhóm khỏi màn chat và xoá nhóm ở màn danh sách đã ẩn",
       GRP,
       "1. Ẩn nhóm G1 → kiểm tra filter 全ての友だち và filter 非表示中\n"
       "2. Ở màn danh sách bạn bè đã ẩn: xoá nhóm G1\n3. Kiểm tra lại danh sách ở chat 1:1 và DB",
       "Nhóm G1: ẩn rồi xoá",
       "- Sau khi ẩn: G1 biến mất khỏi filter 全ての友だち, xuất hiện ở filter 非表示中\n"
       "- Sau khi xoá: G1 không còn ở cả 2 filter, bản ghi hội thoại bị xoá khỏi DB",
       note="Nguồn: Group chat r13, r14"),

    tc("Group chat", "MSG-001", "Normal",
       "Nhận tin từ nhóm — hiển thị đủ loại tin ở chat 1:1",
       GRP,
       "1. Cho thành viên nhóm gửi lần lượt từng loại tin ở cột Dữ liệu test vào nhóm\n"
       "2. Quan sát hiển thị ở chat 1:1",
       "text · ảnh · sticker · video · audio · vị trí · file",
       "- Tất cả loại tin đều hiển thị được ở chat 1:1 của hội thoại nhóm\n"
       "- Hiện đúng tên và avatar người gửi trong nhóm",
       env="PRODUCTION",
       note="Gộp 7 loại vì cùng kết quả. Nguồn: Group chat r22-r28"),

    tc("Group chat", "MSG-001", "Normal",
       "Gửi tin vào nhóm — đủ loại nội dung, thành viên nhóm nhận được",
       GRP,
       "1. Với mỗi loại nội dung ở cột Dữ liệu test: gửi vào nhóm G1\n"
       "2. Kiểm tra hiển thị ở chat 1:1\n3. Kiểm tra thành viên nhóm nhận được trên app LINE",
       "Text nhập trực tiếp · PDF · ảnh · video · audio · sticker · "
       "template text · template button · template ảnh thường · template image map · "
       "template video (thường và có action) · template audio · template sticker · template vị trí · template 紹介",
       "- Tất cả gửi thành công, hiển thị đúng ở chat 1:1\n"
       "- Thành viên nhóm nhận được đầy đủ trên app LINE",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Group chat r29-r44"),

    tc("Group chat", "MSG-003", "Normal",
       "Gửi URL vào nhóm — URL thường LUÔN không rút gọn",
       GRP + "\n- Cài đặt chat: BẬT 短縮URLの利用",
       "1. Gửi 1 URL thường vào nhóm G1\n2. Đọc URL ở chat 1:1 và trên app LINE của thành viên nhóm\n"
       "3. So sánh với hành vi khi gửi cho friend cá nhân (cùng cài đặt bật rút gọn)",
       "URL thường, cài đặt rút gọn đang BẬT",
       "- Gửi vào nhóm: URL KHÔNG bị rút gọn ở cả 2 phía\n"
       "- Khác với gửi cho friend cá nhân (bị rút gọn phía LINE)",
       env="PRODUCTION", spec="Spec không ghi",
       note="MT-14. Nguồn: Group chat r45"),

    tc("Group chat", "LIFF-ENTRY-001", "Normal",
       "Thành viên nhóm bấm link form / item / booking gửi trong nhóm",
       GRP + "\n- Đã tạo form F, item I, event booking E, calendar booking C\n"
       "- Trong nhóm có thành viên CHƯA kết bạn với bot và thành viên ĐÃ kết bạn",
       "1. Gửi link form F vào nhóm\n"
       "2. Thành viên CHƯA kết bạn bấm link → quan sát màn hình\n"
       "3. Thành viên ĐÃ kết bạn bấm link → điền và gửi form → kiểm tra kết quả lưu\n"
       "4. Lặp lại với item, event booking, calendar booking",
       "Form F · item I · event booking E · calendar booking C; thành viên chưa và đã kết bạn",
       "- Thành viên CHƯA kết bạn: bị chuyển sang màn kết bạn với bot\n"
       "- Thành viên ĐÃ kết bạn: mở được trang, thao tác được (gửi form / mua item / đặt lịch)\n"
       "- Kết quả được lưu cho RIÊNG thành viên đó và action tương ứng chạy cho chính người đó",
       env="PRODUCTION",
       note="Gộp 4 loại link vì cùng dạng kết quả. Nguồn: Group chat r47-r50"),

    tc("Group chat", "MSG-003", "Normal",
       "Gửi mã form kiểu cũ vào nhóm — được thay thành link form mới",
       GRP + "\n- Có form F đã tạo, hệ thống còn hỗ trợ mã form kiểu cũ",
       "1. Soạn tin chứa mã form kiểu cũ, gửi vào nhóm G1\n"
       "2. Đọc nội dung ở chat 1:1 và trên app LINE của thành viên nhóm\n3. Bấm vào link",
       "Mã form kiểu cũ của form F",
       "- Khi gửi, mã được thay thành LINK MỚI của form\n- Bấm link mở đúng form F",
       env="PRODUCTION",
       note="Nguồn: Group chat r46"),

    tc("Group chat", "FUNC-001", "Normal",
       "Thành viên nhóm bấm nút / xem video / bấm ảnh có action",
       GRP + "\n- Template có action ở nút bấm, image map và video",
       "1. Gửi template có action vào nhóm G1\n"
       "2. Thành viên nhóm bấm nút / bấm image map / xem hết video\n"
       "3. Kiểm tra action có chạy không và chạy cho ai\n4. Gửi URL rút gọn có action → thành viên bấm → kiểm tra",
       "Nút bấm · image map · video có action · URL rút gọn có action",
       "- Action chạy cho CHÍNH thành viên đã thao tác (không phải cả nhóm)\n"
       "- Kiểm chứng được qua kết quả action (tag được gắn, tin nhắn nhận được…)",
       env="PRODUCTION",
       note="Gộp 4 loại vì cùng dạng. Nguồn: Group chat r54-r57"),

    tc("Group chat", "PERM-002", "Abnormal",
       "Các tính năng KHÔNG áp dụng cho nhóm — Broadcast, tự động trả lời, rich menu, lịch chạy action",
       GRP,
       "1. Tạo Broadcast gửi toàn bộ bạn bè → chạy → kiểm tra nhóm G1 có nhận tin không\n"
       "2. Cấu hình tự động trả lời → cho thành viên nhóm gửi tin khớp từ khoá vào nhóm → kiểm tra\n"
       "3. Thử gán rich menu cho nhóm G1\n"
       "4. Tạo lịch chạy action áp dụng cho toàn bộ bạn bè → chờ chạy → kiểm tra nhóm G1\n"
       "5. Thử bắt đầu scenario cho nhóm G1",
       "Broadcast · tự động trả lời · rich menu · lịch chạy action · scenario",
       "- Broadcast: nhóm KHÔNG nhận tin\n"
       "- Tự động trả lời: nhóm KHÔNG được trả lời tự động\n"
       "- Rich menu: KHÔNG gán được cho nhóm\n"
       "- Lịch chạy action: KHÔNG chạy cho nhóm\n"
       "- Scenario: ghi nhận hiện trạng và đối chiếu quyết định của Leader",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-14: spec chat-11 KHÔNG có quy tắc nào giới hạn tính năng cho nhóm. Nguồn: Group chat r59-r63"),

    tc("Group chat", "MSG-002", "Normal",
       "Gửi tin vào nhóm bằng profile người gửi — áp dụng đúng ở cả 2 phía",
       GRP + "\n- Đang chọn profile P1 (tên và ảnh riêng)",
       "1. Gửi 1 tin vào nhóm G1 bằng profile mặc định → kiểm tra chat 1:1 và app LINE\n"
       "2. Đổi sang P1 → gửi tin vào nhóm → kiểm tra lại",
       "Profile mặc định và profile P1",
       "- Tin gửi bằng profile mặc định: hiện tên và ảnh bot gốc ở cả 2 phía\n"
       "- Tin gửi bằng P1: hiện tên và ảnh của P1 ở cả 2 phía",
       env="PRODUCTION",
       note="Nguồn: Group chat r53 + Profile sender r32, r33"),

    # ═══════════════ Realtime socket & typing ═══════════════
    tc("Realtime socket & typing", "SYNC-APP-001", "Normal",
       "Tin nhắn mới hiển thị realtime trên chat 1:1 WEB — cả tin bot gửi và tin bạn bè gửi",
       BOT + "\n- Đang mở hội thoại friend A, KHÔNG reload trang trong suốt bài test",
       "1. Với mỗi loại tin BOT gửi ở cột Dữ liệu test: gửi và quan sát khung hội thoại (không reload)\n"
       "2. Với mỗi loại tin BẠN BÈ gửi: cho friend A gửi và quan sát",
       "Bot gửi: text · template (nhóm nhiều template con: nút bấm, vị trí, 紹介) · multi action · "
       "media · PDF · sticker\nBạn bè gửi: text · ảnh · sticker · video · audio · file",
       "- Mọi loại tin đều hiển thị REALTIME trên chat 1:1, không cần reload\n"
       "- Nhóm nhiều template con: hiển thị đủ và ĐÚNG THỨ TỰ",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. RULE-08: socket → PRODUCTION. Nguồn: Improve socket r3-r6 + Content: Hiển thị msg r1391-r1399"),

    tc("Realtime socket & typing", "SYNC-APP-001", "Normal",
       "Tin nhắn mới hiển thị realtime trên APP MOBILE",
       "- App mobile LME đăng nhập account admin bot A, đang mở hội thoại friend A",
       "1. Với mỗi loại tin bot gửi và bạn bè gửi: gửi và quan sát màn chat của app mobile\n"
       "2. Kiểm tra thứ tự hiển thị của nhóm nhiều template con",
       "Bot gửi: text · template · multi action · media · PDF · sticker\n"
       "Bạn bè gửi: text · ảnh · sticker · video · audio · file",
       "- Mọi loại tin đều hiển thị REALTIME trên app mobile\n- Nhóm nhiều template con hiển thị đủ và đúng thứ tự",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Improve socket r11-r18 + Content: Hiển thị msg r1400-r1408"),

    tc("Realtime socket & typing", "CONC-001", "Abnormal",
       "Gửi nhiều tin liên tiếp — hiển thị đủ và đúng thứ tự, không double click",
       BOT + "\n- Đang mở hội thoại friend A",
       "1. Gõ và gửi liên tiếp nhanh: text → ảnh → video → audio → file\n"
       "2. Quan sát thứ tự hiển thị ở chat 1:1 và trên app LINE\n"
       "3. Cho friend A gửi liên tiếp nhiều tin → quan sát thứ tự\n"
       "4. Double click nút gửi ở cả phía bot và phía friend",
       "5 tin gửi liên tiếp mỗi phía",
       "- Tất cả tin hiển thị ĐỦ và ĐÚNG THỨ TỰ ở cả chat 1:1 và app LINE\n"
       "- Double click: không gửi trùng tin",
       env="PRODUCTION",
       note="Nguồn: Improve socket r7-r10, r15-r18"),

    tc("Realtime socket & typing", "DATA-COUNT-001", "Normal",
       "Realtime không ảnh hưởng bộ đếm tin chưa xác nhận",
       BOT + "\n- Ghi lại badge số tin chưa đọc ở menu 1:1チャット",
       "1. Với mỗi loại tin ở cột Dữ liệu test: gửi cho friend A từ web (và từ app nếu hỗ trợ)\n"
       "2. Sau mỗi lần: kiểm tra badge số tin chưa đọc ở menu",
       "text · ảnh · video · audio (chỉ web) · PDF (chỉ web) · "
       "template text/nút bấm/media/sticker/vị trí/紹介 (chỉ web) · sticker",
       "- Badge số tin chưa xác nhận KHÔNG thay đổi khi BOT gửi tin\n- Không có tin nào bị đếm nhầm",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Improve socket r19-r31"),

    tc("Realtime socket & typing", "CONC-002", "Normal",
       "Hiển thị khi nhân viên khác đang soạn tin — WEB",
       "- 2 trình duyệt: 1 đăng nhập user chính, 1 đăng nhập account staff của cùng bot A\n"
       "- Cả 2 cùng mở hội thoại friend A",
       "1. Staff bắt đầu gõ tin → quan sát màn của user chính\n"
       "2. Đổi vai: user chính gõ → quan sát màn của staff\n"
       "3. Dùng 2 account staff khác nhau: staff 2 gõ → quan sát màn staff 1\n"
       "4. Ngừng gõ, đợi 5 giây → quan sát\n"
       "5. Cho 2 người cùng gõ một lúc → quan sát\n"
       "6. Khi staff đang gõ, user chính gửi tin → quan sát vị trí hiển thị dòng thông báo",
       "user chính + 2 account staff",
       "- Hiển thị dòng「スタッフ [スタッフ名] が入力中 ....」ở hội thoại tương ứng\n"
       "- Sau 5 giây ngừng gõ: dòng thông báo biến mất\n"
       "- 2 người cùng gõ: hiện「{số người}人が入力中」\n"
       "- Khi có tin gửi đi: dòng thông báo nằm PHÍA DƯỚI tin vừa gửi",
       env="PRODUCTION", spec="Spec không ghi",
       note="Spec chat-11 §Real-time chỉ liệt kê sự kiện tin nhắn và badge, KHÔNG có sự kiện đang soạn tin. "
            "Nguồn: Content: Hiển thị msg r1410-r1415"),

    tc("Realtime socket & typing", "SYNC-APP-001", "Normal",
       "Hiển thị khi nhân viên khác đang soạn tin — APP MOBILE",
       "- App mobile đăng nhập 1 account; trình duyệt đăng nhập account còn lại của cùng bot A\n"
       "- Cả 2 cùng mở hội thoại friend A",
       "1. Staff gõ trên web → quan sát app mobile của user chính\n"
       "2. User chính gõ → quan sát app mobile của staff\n"
       "3. Staff 2 gõ → quan sát app mobile của staff 1\n"
       "4. Ngừng gõ 5 giây → quan sát\n5. 2 người cùng gõ → quan sát",
       "user chính + 2 account staff, quan sát trên app mobile",
       "- Nếu người gõ là STAFF: hiện「スタッフ [スタッフ名] が入力中 ....」\n"
       "- Nếu người gõ là USER CHÍNH: hiện「[名] が入力中 ....」(không có tiền tố スタッフ)\n"
       "- Sau 5 giây ngừng gõ: dòng thông báo biến mất\n- 2 người cùng gõ: hiện「{số người}人が入力中」",
       env="PRODUCTION", spec="Spec không ghi",
       note="Định dạng chữ ở app khác web → TC riêng. Nguồn: Content: Hiển thị msg r1416-r1420"),

    # ═══════════════ Bộ đếm chưa xác nhận ═══════════════
    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bạn bè gửi tin — bộ đếm tăng 1 mỗi tin, hiển thị ngay ở web và app",
       BOT + "\n- Friend A đang ở trạng thái ĐÃ xác nhận hết tin (bộ đếm = 0)",
       "1. Ghi lại giá trị bộ đếm của hội thoại A và badge ở menu\n"
       "2. Cho friend A gửi 1 tin → kiểm tra bộ đếm, badge ở web và ở app mobile\n"
       "3. Cho A gửi thêm 2 tin nữa → kiểm tra lại\n"
       "4. Kiểm tra DB: bộ đếm của hội thoại và các trường trạng thái tin cuối",
       "Friend A gửi 3 tin liên tiếp",
       "- Mỗi tin đến: bộ đếm TĂNG 1 (0 → 1 → 2 → 3)\n"
       "- Trường đánh dấu có tin chưa xác nhận = 1\n"
       "- Số tin chưa xác nhận hiển thị ngay ở chat 1:1 trên cả web và app mobile",
       env="PRODUCTION",
       note="Bằng chứng cho MT-19 (spec ghi điều kiện lọc chưa xác nhận là bộ đếm = 1). "
            "Nguồn: improve count comfirm_message r3-r5, r43-r45"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Nhóm LINE gửi tin — bộ đếm hoạt động như bạn bè cá nhân",
       BOT + "\n- Nhóm G1 đang ở trạng thái đã xác nhận",
       "1. Cho thành viên nhóm gửi 2 tin vào nhóm\n2. Kiểm tra bộ đếm của hội thoại nhóm ở web và app\n"
       "3. Kiểm tra DB",
       "Nhóm G1, 2 tin đến",
       "- Bộ đếm tăng 1 mỗi tin, hiển thị đúng ở cả web và app mobile\n"
       "- Trường đánh dấu có tin chưa xác nhận = 1",
       env="PRODUCTION",
       note="Nguồn: improve count comfirm_message r6-r8, r46-r48"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bấm xác nhận ở chat 1:1 — bộ đếm về 0 và xoá bản ghi tin chưa xác nhận",
       BOT + "\n- Friend A có 3 tin chưa xác nhận",
       "1. Kiểm tra DB: bộ đếm, các trường trạng thái và bảng tin chưa xác nhận của A\n"
       "2. Bấm xác nhận ở hội thoại A trên WEB\n3. Kiểm tra lại DB và badge menu\n"
       "4. Lặp lại toàn bộ trên APP MOBILE\n5. Lặp lại với hội thoại NHÓM",
       "Friend A và nhóm G1, mỗi bên 3 tin chưa xác nhận; thao tác trên web và app",
       "- Bộ đếm về 0; trường trạng thái tin cuối = 1; trường đánh dấu đã xác nhận = 1; "
       "trường đánh dấu chưa xác nhận = 0\n"
       "- Bảng tin chưa xác nhận KHÔNG còn bản ghi của hội thoại đó\n"
       "- Kết quả giống nhau trên web, app và với cả nhóm",
       env="PRODUCTION",
       note="Gộp 4 tổ hợp vì cùng kết quả. Nguồn: improve count comfirm_message r10-r13"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bấm chuyển về chưa xác nhận — bộ đếm tăng và tạo lại bản ghi tin chưa xác nhận",
       BOT + "\n- Friend A và nhóm G1 đều đã xác nhận hết tin",
       "1. Bấm chuyển A về chưa xác nhận trên WEB → kiểm tra DB và badge menu\n"
       "2. Lặp lại trên APP MOBILE\n3. Lặp lại với nhóm G1 trên cả web và app",
       "Friend A và nhóm G1; thao tác trên web và app",
       "- Bộ đếm tăng lên; trường trạng thái tin cuối = 0; trường đánh dấu đã xác nhận = 0; "
       "trường đánh dấu chưa xác nhận = 1\n"
       "- Bảng tin chưa xác nhận CÓ bản ghi của hội thoại đó\n"
       "- Badge menu tăng tương ứng",
       env="PRODUCTION",
       note="Gộp 4 tổ hợp vì cùng kết quả. Nguồn: improve count comfirm_message r49-r52"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Xoá bạn bè — bản ghi hội thoại bị xoá và bộ đếm tổng của bot giảm 1",
       BOT + "\n- Friend A đang có tin chưa xác nhận",
       "1. Ghi lại bộ đếm tổng của bot\n"
       "2. Xoá friend A từ từng nơi ở cột Dữ liệu test (mỗi lần dùng 1 friend khác nhau)\n"
       "3. Sau mỗi lần: kiểm tra bản ghi hội thoại, bảng tin chưa xác nhận và bộ đếm tổng của bot",
       "Xoá từ: my_page (web) · màn danh sách bạn bè đã ẩn · màn bạn bè đã chặn bot · "
       "màn bot đã chặn bạn bè · my_page trên app mobile",
       "- Bản ghi hội thoại bị xoá\n"
       "- Bản ghi ở bảng tin chưa xác nhận KHÔNG bị xoá theo\n"
       "- Bộ đếm tổng của bot GIẢM 1 sau mỗi lần xoá",
       env="PRODUCTION", spec="Spec không ghi",
       note="Gộp 5 đường xoá vì cùng kết quả. Spec không mô tả trường bộ đếm tổng của bot. "
            "Nguồn: improve count comfirm_message r14-r18"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bạn bè đã xoá nhắn tin lại — tạo bản ghi hội thoại mới với bộ đếm = 1",
       BOT + "\n- Friend A vừa bị xoá khỏi LME",
       "1. Cho friend A gửi 1 tin đến bot\n"
       "2. Kiểm tra DB: bản ghi hội thoại mới, bộ đếm và các trường trạng thái\n"
       "3. Kiểm tra bảng tin chưa xác nhận",
       "Friend A đã bị xoá, nhắn lại 1 tin",
       "- Tạo bản ghi hội thoại MỚI\n"
       "- Bộ đếm = 1; trường trạng thái tin cuối = 0; đánh dấu đã xác nhận = 0; đánh dấu chưa xác nhận = 1\n"
       "- Bảng tin chưa xác nhận có bản ghi mới",
       env="PRODUCTION",
       note="Nguồn: improve count comfirm_message r19"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Chặn và bỏ chặn — bộ đếm giữ nguyên, chỉ tăng khi bạn bè nhắn tin lại",
       BOT + "\n- Friend A có 2 tin chưa xác nhận (bộ đếm = 2)",
       "1. Cho friend A chặn bot → kiểm tra bộ đếm\n2. Cho A bỏ chặn → kiểm tra bộ đếm\n"
       "3. Cho A nhắn 1 tin → kiểm tra bộ đếm\n"
       "4. Lặp lại kịch bản với BOT chặn friend (trên web rồi trên app mobile): chặn → nhắn tin → bỏ chặn → nhắn tin",
       "Bạn bè chặn bot · bot chặn bạn bè (web và app); mỗi lần kiểm tra bộ đếm",
       "- Chặn (cả 2 chiều): bộ đếm GIỮ NGUYÊN\n"
       "- Bỏ chặn: bộ đếm GIỮ NGUYÊN\n"
       "- Khi bot đang chặn bạn bè mà bạn bè nhắn tin: bộ đếm KHÔNG tăng\n"
       "- Sau khi bỏ chặn rồi bạn bè nhắn tin: bộ đếm TĂNG 1",
       env="PRODUCTION",
       note="Gộp vì cùng thuộc chuỗi trạng thái chặn. Nguồn: improve count comfirm_message r20-r30, r58-r68"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bot ẩn bạn bè — xử lý như xác nhận; bạn bè nhắn lại thì bộ đếm tăng",
       BOT + "\n- Friend A có 2 tin chưa xác nhận",
       "1. Ẩn friend A → kiểm tra bộ đếm, các trường trạng thái và bảng tin chưa xác nhận\n"
       "2. Cho A nhắn 1 tin mới → kiểm tra lại",
       "Friend A: ẩn rồi nhắn tin lại",
       "- Sau khi ẩn: bộ đếm = 0; trạng thái tin cuối = 1; đánh dấu đã xác nhận = 1; "
       "bảng tin chưa xác nhận KHÔNG còn bản ghi của A\n"
       "- Sau khi A nhắn tin: bộ đếm = 1; trạng thái tin cuối = 0; đánh dấu chưa xác nhận = 1; "
       "bảng tin chưa xác nhận có bản ghi mới",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-08. Nguồn: improve count comfirm_message r31, r32, r69, r70"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Mọi đường BOT gửi tin — bộ đếm chưa xác nhận KHÔNG đổi",
       BOT + "\n- Friend A có bộ đếm khác 0 và friend B có bộ đếm = 0",
       "1. Với mỗi đường gửi ở cột Dữ liệu test: gửi cho friend A rồi cho friend B\n"
       "2. Sau mỗi lần: kiểm tra bộ đếm của cả 2 friend và badge menu\n"
       "3. Kiểm tra bạn bè có nhận được tin trên app LINE",
       "Send test từ màn Template / Broadcast / Scenario / Remind · "
       "gửi qua job từ Broadcast / Scenario / Remind · nhắn tin ở chat 1:1 (web và app mobile)",
       "- TẤT CẢ: bộ đếm chưa xác nhận GIỮ NGUYÊN\n- Bạn bè nhận được tin thành công",
       env="PRODUCTION",
       note="Gộp ~11 đường vì cùng kết quả. Nguồn: improve count comfirm_message r33-r41, r71-r79"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Bạn bè bấm nút của template — bộ đếm TĂNG 1",
       BOT + "\n- Đã gửi cho friend A template có nút bấm",
       "1. Ghi lại bộ đếm của A\n2. Cho A bấm nút trên app LINE\n"
       "3. Kiểm tra bộ đếm và badge menu\n"
       "4. Bật cấu hình tự động xác nhận cho tin dạng nút bấm → lặp lại → kiểm tra",
       "Bạn bè bấm nút template; 2 trạng thái cấu hình tự động xác nhận",
       "- Khi TẮT tự động xác nhận: bộ đếm TĂNG 1\n"
       "- Khi BẬT tự động xác nhận cho tin dạng nút bấm: tin tự chuyển thành đã xác nhận, bộ đếm KHÔNG tăng",
       env="PRODUCTION",
       note="Nguồn: improve count comfirm_message r42, r80 + Leftbar+Header r101"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Cấu hình tự động xác nhận — 5 trường hợp tự chuyển sang đã xác nhận realtime",
       BOT + "\n- Ở màn cài đặt chat: BẬT cả 5 tuỳ chọn tự động xác nhận\n"
       "- Đang mở màn chat 1:1, KHÔNG reload trong suốt bài test",
       "1. Với mỗi trường hợp ở cột Dữ liệu test: tạo tình huống tương ứng\n"
       "2. Sau mỗi lần: quan sát badge số tin và trạng thái hội thoại (không reload)\n"
       "3. Kiểm tra DB bộ đếm của hội thoại",
       "Bạn bè bấm nút template · bạn bè gửi sticker · tự động trả lời với mọi tin nhắn · "
       "tự động trả lời theo từ khoá · bot trả lời tin thường · bạn bè chặn bot",
       "- Mọi trường hợp: tin tự chuyển sang ĐÃ xác nhận REALTIME, không cần reload\n"
       "- Badge số tin GIẢM 1 tương ứng\n- DB: bộ đếm của hội thoại về 0",
       env="PRODUCTION",
       note="Gộp 6 trường hợp vì cùng kết quả. Nguồn: Leftbar+Header r101-r106 + spec feature-spec.md:199-206"),

    tc("Bộ đếm chưa xác nhận", "DATA-COUNT-001", "Normal",
       "Badge số tin chưa đọc cập nhật realtime khi có tin đến, đúng với mọi bộ lọc",
       BOT + "\n- Đang mở màn chat 1:1, KHÔNG reload trong suốt bài test",
       "1. Với mỗi loại tin ở cột Dữ liệu test: cho friend A gửi tới bot\n"
       "2. Quan sát badge ở menu 1:1チャット (không reload)\n"
       "3. Lặp lại khi đang áp dụng từng bộ lọc ở cột Dữ liệu test\n4. Kiểm tra DB bộ đếm tổng của bot",
       "Loại tin: text · ảnh/video · PDF · sticker\n"
       "Bộ lọc: không lọc · 未確認 · 確認済み · 非表示中 · グループ",
       "- Badge cập nhật realtime khi có tin đến, không cần reload\n"
       "- DB bộ đếm tổng của bot khớp số bạn bè thực sự còn chưa xác nhận\n"
       "- Danh sách bạn bè hiển thị đúng theo từng bộ lọc",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Leftbar+Header r93-r100"),

    # ═══════════════ Lịch sử chat & bảng message ═══════════════
    tc("Lịch sử chat & bảng message", "DATA-DB-001", "Normal",
       "Lịch sử chat lấy từ nhiều bảng lưu tin nhắn — hiển thị đủ và đúng thứ tự thời gian",
       BOT + "\n- Friend A có tin nhắn nằm ở nhiều bảng lưu tin nhắn theo năm",
       "1. Với mỗi tổ hợp dữ liệu ở cột Dữ liệu test: chuẩn bị friend có phân bố tin nhắn tương ứng\n"
       "2. Mở hội thoại, cuộn lên để tải hết lịch sử\n"
       "3. Kiểm tra tin nhắn hiển thị ĐỦ và ĐÚNG THỨ TỰ thời gian\n"
       "4. Lặp lại trên app mobile",
       "Bảng mới có tin + bảng cũ có tin + 2023/2024/2025 đều có tin · "
       "bảng mới có, bảng cũ không, 2025 có · bảng mới có, bảng cũ có, 2023 và 2024 có · "
       "bảng mới có, bảng cũ có, 2025 không · bảng mới không, bảng cũ có, 2025 có · "
       "bảng mới và bảng cũ đều không, chỉ 2025 có",
       "- Mọi tổ hợp: lịch sử hiển thị ĐỦ tin nhắn từ tất cả các bảng, sắp xếp đúng thứ tự thời gian\n"
       "- Không mất tin, không lặp tin\n- Đúng trên cả web và app mobile",
       env="PRODUCTION",
       note="Gộp 6 tổ hợp vì cùng kết quả. Nguồn: Content: Hiển thị msg r1427-r1435"),

    tc("Lịch sử chat & bảng message", "PERF-LARGE-001", "Normal",
       "Lịch sử chat rất dài — tải thêm nhiều trang không lỗi",
       "- Bot PRODUCTION, friend có lịch sử chat lớn: bảng mới ~4 trang, bảng cũ ~6 trang, "
       "bảng theo năm ~40 bản ghi",
       "1. Mở hội thoại, cuộn lên tải thêm liên tiếp cho tới hết lịch sử\n"
       "2. Đếm tổng số tin đã tải, đo thời gian mỗi lần tải thêm\n"
       "3. Kiểm tra thứ tự thời gian sau mỗi lần tải thêm\n4. Lặp lại trên app mobile",
       "Lịch sử ~10 trang trở lên",
       "- Tải thêm được tới hết lịch sử, không lỗi, không mất tin\n"
       "- Thứ tự thời gian đúng sau mỗi lần tải thêm\n"
       "- Ghi lại thời gian tải thực tế làm evidence",
       env="PRODUCTION",
       note="RULE-08: hiệu năng bắt buộc PRODUCTION. Nguồn: Content: Hiển thị msg r1433 + Test fix bug Kh r27, r55"),

    tc("Lịch sử chat & bảng message", "JOB-001", "Normal",
       "Job chuyển tin nhắn sang bảng lưu trữ — giữ lại 20 tin mới nhất",
       "- Môi trường có job chuyển tin nhắn đang chạy\n- Hội thoại H1 có ≤20 tin; hội thoại H2 có >20 tin",
       "1. Chạy job chuyển tin nhắn\n"
       "2. Với H1 (≤20 tin): kiểm tra tin có bị chuyển không\n"
       "3. Với H2 (>20 tin): kiểm tra số tin còn lại ở bảng gốc và số tin đã chuyển\n"
       "4. Kiểm tra tin có cùng thời điểm tạo được xử lý thế nào\n"
       "5. Lặp lại cho bước chuyển tiếp sang bảng lưu trữ cũ hơn",
       "H1: 20 tin · H2: 50 tin; có ≥2 tin trùng thời điểm tạo",
       "- H1 (≤20 tin): KHÔNG chuyển tin nào\n"
       "- H2 (>20 tin): giữ lại đúng 20 tin có thời điểm tạo MỚI NHẤT ở bảng gốc, phần còn lại chuyển sang bảng lưu trữ\n"
       "- Tin trùng thời điểm tạo: giữ tin có mã lớn hơn\n- Quy tắc giống nhau ở cả 2 bước chuyển",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-09: spec chat-11 liệt kê bảng theo năm nhưng KHÔNG có 2 bảng lưu trữ này. "
            "Nguồn: Job move message r3-r10"),

    tc("Lịch sử chat & bảng message", "DATA-MIG-001", "Normal",
       "Job chuyển tin nhắn — giữ nguyên mã, thời điểm tạo, thời điểm cập nhật và dữ liệu",
       "- Hội thoại H2 có >20 tin, chuẩn bị chạy job chuyển tin nhắn",
       "1. Ghi lại mã, thời điểm tạo, thời điểm cập nhật và nội dung của 5 tin sắp bị chuyển\n"
       "2. Chạy job chuyển tin nhắn\n3. Tìm 5 tin đó ở bảng lưu trữ, so sánh từng trường\n"
       "4. Mở lịch sử chat của H2 ở chat 1:1, kiểm tra 5 tin đó hiển thị đúng\n"
       "5. Lặp lại với hội thoại NHÓM",
       "5 tin bị chuyển; hội thoại thường và hội thoại nhóm",
       "- Mã tin GIỮ NGUYÊN (không tạo mã mới)\n"
       "- Thời điểm tạo và thời điểm cập nhật GIỮ NGUYÊN\n- Toàn bộ dữ liệu khác giữ nguyên\n"
       "- Lịch sử chat vẫn hiển thị đủ 5 tin đó, đúng nội dung và thời gian\n- Đúng cả với hội thoại nhóm",
       env="PRODUCTION",
       note="Nguồn: Job move message r5-r8, r11-r16"),

    tc("Lịch sử chat & bảng message", "COMPAT-LEGACY-001", "Normal",
       "Xác nhận / bỏ xác nhận tin nhắn nằm ở bảng lưu trữ",
       BOT + "\n- Hội thoại có tin nhắn ở bảng gốc, bảng lưu trữ và bảng lưu trữ cũ",
       "1. Với mỗi bảng: chọn 1 hội thoại có tin chưa xác nhận ở bảng đó\n"
       "2. Bấm xác nhận → kiểm tra trạng thái và DB\n3. Bấm bỏ xác nhận → kiểm tra lại\n"
       "4. Lặp lại trên app mobile",
       "Tin ở bảng gốc · bảng lưu trữ · bảng lưu trữ cũ; thao tác trên web và app",
       "- Xác nhận và bỏ xác nhận hoạt động đúng với tin ở CẢ 3 bảng\n"
       "- DB cập nhật đúng, không lỗi",
       env="PRODUCTION",
       note="Nguồn: Improve move database r5-r15 (09/2023 — TC > 2 năm, CẦN VERIFY LẠI)"),

    # ═══════════════ Giới hạn plan & token ═══════════════
    tc("Giới hạn plan & token", "PAY-PLAN-001", "Normal",
       "Bot trả phí — xem được toàn bộ lịch sử chat",
       "- Có bot ở gói standard, gói pro và gói enterprise\n- Mỗi bot có friend với lịch sử chat > 180 ngày",
       "1. Với mỗi gói: mở hội thoại của friend có lịch sử dài\n"
       "2. Cuộn lên tải hết lịch sử\n3. Kiểm tra tin nhắn cũ nhất có hiển thị không",
       "Bot gói standard · pro · enterprise",
       "- Cả 3 gói: hiển thị được TOÀN BỘ lịch sử chat, kể cả tin cũ hơn 180 ngày\n"
       "- Không hiện thông báo yêu cầu nâng cấp gói",
       env="PRODUCTION",
       note="Gộp 3 gói vì cùng kết quả. Nguồn: Feature #28859 r3-r5"),

    tc("Giới hạn plan & token", "PAY-PLAN-001", "Boundary",
       "Bot miễn phí — chỉ xem được lịch sử chat trong 180 ngày",
       "- Bot gói MIỄN PHÍ\n- Friend có tin nhắn trong 180 ngày và tin nhắn cũ hơn 180 ngày",
       "1. Xác định mốc 180 ngày trước hôm nay\n"
       "2. Mở hội thoại, cuộn lên xem tin trong khoảng 180 ngày → kiểm tra\n"
       "3. Cuộn tiếp tới vùng tin cũ hơn 180 ngày → quan sát\n"
       "4. Kiểm tra trên app mobile\n5. Bấm vào chữ 有料プラン trong thông báo",
       "Bot miễn phí; tin trong và ngoài mốc 180 ngày",
       "- Tin trong 180 ngày: hiển thị bình thường\n"
       "- Tin cũ hơn 180 ngày: KHÔNG hiển thị, thay bằng thông báo "
       "「180日以上前のトーク閲覧はエルメの有料プランご契約が必要です」\n"
       "- Đúng trên cả web và app mobile\n- Bấm 有料プラン: mở màn nâng cấp gói",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-03: spec chat-11 BR-07 chỉ có giới hạn 1.000 tin/tháng, KHÔNG có quy tắc 180 ngày. "
            "Nguồn: Feature #28859 r6-r9 + Test fix bug Kh r29"),

    tc("Giới hạn plan & token", "PAY-PLAN-001", "Normal",
       "Nâng cấp từ gói miễn phí lên gói trả phí — mở khoá toàn bộ lịch sử",
       "- Bot miễn phí đang bị chặn xem lịch sử cũ hơn 180 ngày",
       "1. Ghi lại mốc thời gian tin cũ nhất đang xem được\n2. Nâng cấp bot lên gói trả phí\n"
       "3. Mở lại hội thoại, cuộn lên hết lịch sử\n4. Kiểm tra tin cũ hơn 180 ngày",
       "Bot nâng cấp từ miễn phí lên trả phí",
       "- Sau khi nâng cấp: hiển thị được TOÀN BỘ tin nhắn, kể cả tin cũ hơn 180 ngày\n"
       "- Thông báo yêu cầu nâng cấp gói biến mất",
       env="PRODUCTION",
       note="Nguồn: Feature #28859 r10"),

    tc("Giới hạn plan & token", "PAY-LIMIT-001", "Boundary",
       "Bot miễn phí — giới hạn 1.000 tin gửi mỗi tháng",
       "- Bot gói MIỄN PHÍ, số tin đã gửi trong tháng gần chạm 1.000",
       "1. Ghi lại số tin đã gửi trong tháng của bot\n2. Gửi tin cho tới khi đạt 999 → kiểm tra vẫn gửi được\n"
       "3. Gửi tin thứ 1.000 → kiểm tra\n4. Gửi tin thứ 1.001 → đọc thông báo\n"
       "5. Kiểm tra bạn bè có nhận tin không",
       "Bot miễn phí, mốc 999 / 1.000 / 1.001 tin",
       "- Tới mốc 1.000: vẫn gửi được, số tin đã gửi tăng lên đúng\n"
       "- Vượt 1.000: hiện thông báo「配信数上限に達しています」, KHÔNG gọi API gửi, bạn bè KHÔNG nhận tin",
       env="PRODUCTION",
       note="Khớp spec BR-07 (feature-spec.md:469). Nguồn: Content: Send message r1257 + spec"),

    tc("Giới hạn plan & token", "INTG-LINE-001", "Normal",
       "Gửi tin khi khoá kết nối LINE còn hạn — gửi bình thường ở mọi đường",
       BOT + "\n- Bot A có khoá kết nối LINE còn hạn",
       "1. Với mỗi đường gửi ở cột Dữ liệu test: gửi cho friend A\n"
       "2. Kiểm tra friend nhận được tin trên app LINE và tin hiển thị ở chat 1:1\n"
       "3. Kiểm tra DB trường hạn của khoá kết nối",
       "Chat 1:1 (ảnh, video, text, sticker) · màn danh sách bạn bè (text) · action gắn tag (template text) · "
       "send test ở Template / Broadcast / Remind / Scenario · trả lời ở talk list · remind gửi ngay · "
       "action text của salon, QR",
       "- TẤT CẢ: gửi bình thường, bạn bè nhận được tin, tin hiển thị ở chat 1:1\n"
       "- Trường hạn của khoá kết nối không đổi",
       env="PRODUCTION",
       note="Gộp ~12 đường vì cùng kết quả. Nguồn: Content: Send message r1224-r1234 (SpecImprove #35523 04/2026)"),

    tc("Giới hạn plan & token", "INTG-LINE-001", "Normal",
       "Khoá kết nối LINE hết hạn — tự làm mới khoá rồi gửi tin thành công",
       BOT + "\n- Nhờ Dev đặt khoá kết nối LINE của bot A thành sai/hết hạn",
       "1. Với mỗi đường gửi ở cột Dữ liệu test: gửi cho friend A\n"
       "2. Kiểm tra DB: khoá kết nối có được cập nhật giá trị mới không\n"
       "3. Kiểm tra bạn bè nhận được tin và tin hiển thị ở chat 1:1",
       "Chat 1:1 (text, sticker, ảnh, emoji) · màn danh sách bạn bè · action gắn tag · "
       "send test ở Template / Broadcast / Remind / Scenario · trả lời ở talk list · remind gửi ngay · "
       "action text của lesson, kết bạn — thử trên cả web và app mobile",
       "- Khoá kết nối được tự làm mới và LƯU LẠI giá trị mới vào DB\n"
       "- Sau đó tin gửi bình thường: bạn bè nhận được, tin hiển thị ở chat 1:1",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r1235-r1252"),

    tc("Giới hạn plan & token", "INTG-LINE-001", "Abnormal",
       "Làm mới khoá kết nối THẤT BẠI — tin vào màn lỗi, không nuốt lỗi",
       BOT + "\n- Nhờ Dev đặt cấu hình khoá kết nối sai để việc làm mới thất bại",
       "1. Gửi tin cho friend A từ chat 1:1 (thử cả text và ảnh)\n"
       "2. Quan sát thông báo trên màn chat\n3. Mở màn quản lý tin nhắn lỗi → tìm tin vừa gửi\n"
       "4. Lặp lại trên app mobile",
       "Khoá kết nối sai, làm mới thất bại; gửi text và ảnh; trên web và app",
       "- Tin gửi bị lỗi và ĐƯỢC GHI vào màn quản lý tin nhắn lỗi\n"
       "- Trên app: gửi text trực tiếp có thể không hiện thông báo lỗi dù không gửi được — "
       "ghi rõ hiện trạng này ở evidence",
       env="PRODUCTION", spec="Spec không ghi",
       note="Nguồn: Content: Send message r1246, r1253"),

    tc("Giới hạn plan & token", "INTG-LINE-001", "Normal",
       "Chuyển giữa 2 bot có tình trạng khoá kết nối khác nhau",
       "- Bot A: khoá kết nối CÒN hạn\n- Bot B: khoá kết nối HẾT hạn\n- Mỗi bot có ≥2 friend",
       "1. Ở bot A: gửi tin cho friend 1 và friend 2 → kiểm tra cả 2 nhận đúng tin\n"
       "2. Chuyển sang bot B: gửi tin cho friend của bot B\n"
       "3. Kiểm tra khoá kết nối của bot B có được làm mới không và bạn bè có nhận tin không\n"
       "4. Kiểm tra khoá kết nối của bot A không bị ảnh hưởng",
       "Bot A còn hạn (2 friend) · bot B hết hạn",
       "- Bot A: cả 2 friend nhận ĐÚNG tin của mình, không lẫn\n"
       "- Bot B: khoá được làm mới thành công, friend nhận đúng tin\n- Khoá của bot A không bị ảnh hưởng",
       env="PRODUCTION",
       note="Nguồn: Content: Send message r1254, r1255"),

    # ═══════════════ Phân quyền staff & môi trường ═══════════════
    tc("Phân quyền staff & môi trường", "PERM-001", "Normal",
       "Account staff thao tác trên chat 1:1 — xác định phạm vi quyền thực tế",
       BOT + "\n- Có account staff của bot A với vai trò 副管理人, 運用者 và サポート",
       "1. Với mỗi vai trò staff: đăng nhập và mở /basic/chat-v3\n"
       "2. Thực hiện lần lượt các thao tác ở cột Dữ liệu test\n"
       "3. Ghi nhận thao tác nào làm được, thao tác nào bị chặn và cách bị chặn\n"
       "4. Gọi TRỰC TIẾP API tương ứng (không qua giao diện) để kiểm tra tầng máy chủ có chặn không",
       "3 vai trò staff × thao tác: xem danh sách bạn bè · lọc và tìm kiếm · quick action · "
       "gửi tin (text/media/template/action) · đặt lịch gửi · quản lý profile người gửi · "
       "chỉnh sửa 対応ステータス · sửa thông tin ở cột phải (thông tin cơ bản, friend info, tag, ghi chú)",
       "- Ghi nhận đầy đủ ma trận quyền thực tế và đối chiếu với quyết định của Leader ở MT-17\n"
       "- Với thao tác bị chặn ở giao diện: gọi trực tiếp API cũng PHẢI bị chặn ở tầng máy chủ",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-17: spec chat-11 ghi「khong phat hien kiem tra quyen Staff trong code Chat 1:1」(feature-spec.md:26, "
            "độ tin cậy Trung bình). Corpus có ~40 dòng 「Check thao tác bằng account staff」nhưng KHÔNG có kết quả "
            "mong đợi. Kiểm tra tầng API là bắt buộc, không chỉ giao diện"),

    tc("Phân quyền staff & môi trường", "PERM-002", "Normal",
       "Màn hình không được cấp quyền — hiện chú thích và không vào được",
       "- Account staff bị gỡ quyền vào màn chat 1:1",
       "1. Đăng nhập bằng staff đó\n2. Rê chuột vào mục menu 1:1チャット → đọc chú thích\n"
       "3. Thử bấm vào mục menu\n4. Cuộn trang xuống rồi rê chuột lại → kiểm tra vị trí chú thích\n"
       "5. Thử gõ thẳng URL /basic/chat-v3 vào thanh địa chỉ",
       "Staff không có quyền vào chat 1:1",
       "- Rê chuột: hiện「操作できません。この機能の操作権限が付与されていません。"
       "主管理者に操作権限を付与してもらうことで操作が可能となります。」\n"
       "- Bấm vào: KHÔNG vào được màn hình\n"
       "- Chú thích hiển thị đúng vị trí theo mục menu kể cả khi đã cuộn trang\n"
       "- Gõ thẳng URL: cũng bị chặn ở tầng máy chủ",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung → tab Phân quyền r4, r5, r7"),

    tc("Phân quyền staff & môi trường", "PERM-003", "Normal",
       "Thay đổi phân quyền staff — có hiệu lực ngay ở lần truy cập tiếp theo",
       "- Account staff đang CÓ quyền vào chat 1:1",
       "1. Ở màn phân quyền: gỡ quyền vào chat 1:1 của staff\n"
       "2. Ở phiên của staff: thử vào chat 1:1 → ghi nhận\n"
       "3. Cấp lại quyền → staff thử vào lại → ghi nhận\n"
       "4. Lặp lại với 3 vai trò 副管理人 / 運用者 / サポート",
       "3 vai trò staff, gỡ rồi cấp lại quyền",
       "- Sau khi gỡ quyền: staff không vào được, hiện đúng chú thích\n"
       "- Sau khi cấp lại quyền: staff vào được bình thường\n- Đúng với cả 3 vai trò",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung → tab Phân quyền r22-r35"),

    tc("Phân quyền staff & môi trường", "PERM-004", "Normal",
       "Staff chỉ thấy dữ liệu của bot được cấp quyền",
       "- Account staff chỉ được cấp quyền ở bot A, KHÔNG có quyền ở bot B",
       "1. Đăng nhập staff, kiểm tra danh sách bot chọn được\n"
       "2. Vào chat 1:1 của bot A → kiểm tra thấy đúng bạn bè, tin nhắn, ghi chú, tag của bot A\n"
       "3. Thử chuyển sang bot B qua giao diện\n"
       "4. Gọi trực tiếp API lấy danh sách bạn bè với mã bot B",
       "Staff chỉ có quyền ở bot A",
       "- Danh sách bot chọn được chỉ có bot A\n"
       "- Dữ liệu hiển thị đúng của bot A, không lẫn dữ liệu bot B\n"
       "- Gọi trực tiếp API với mã bot B: bị chặn ở tầng máy chủ, không trả về dữ liệu",
       env="PRODUCTION", spec="Spec không ghi",
       note="Spec ghi mọi truy vấn lọc theo mã bot lấy từ phiên đăng nhập (feature-spec.md §Xác thực) — "
            "cần kiểm chứng ở tầng API. Nguồn: TCsLine_Improve chung → tab Phân quyền r11, r16, r21"),

    tc("Phân quyền staff & môi trường", "ENV-001", "Normal",
       "Chat 1:1 chạy đúng trên môi trường dev, staging và production",
       "- Có tài khoản truy cập cả 3 môi trường, mỗi môi trường có bot với dữ liệu chat",
       "1. Trên mỗi môi trường: mở /basic/chat-v3, gửi 1 tin text và 1 ảnh\n"
       "2. Kiểm tra hiển thị realtime, đường dẫn file media và tin nhắn phía bạn bè\n"
       "3. Ghi nhận khác biệt giữa 3 môi trường",
       "3 môi trường: dev · staging · production",
       "- Cả 3 môi trường: gửi và hiển thị tin nhắn bình thường\n"
       "- Đường dẫn file media trỏ đúng máy chủ của từng môi trường\n"
       "- Ghi rõ mọi khác biệt phát hiện được làm evidence",
       env="PRODUCTION",
       note="Đối chiếu framework/catalog-lme.md mục khác biệt môi trường (mã ENV-*)"),

    tc("Phân quyền staff & môi trường", "PERF-LARGE-001", "Normal",
       "Chat 1:1 dưới tải thật — kiểm tra hiệu năng ở production",
       "- Bot PRODUCTION có ≥50.000 bạn bè và hội thoại lịch sử lớn",
       "1. Đo thời gian tải màn /basic/chat-v3 lần đầu\n2. Đo thời gian tải thêm danh sách bạn bè\n"
       "3. Đo thời gian mở 1 hội thoại có lịch sử lớn\n"
       "4. Đo thời gian thực hiện 全て確認済みに変更 khi không lọc\n"
       "5. Ghi lại toàn bộ số đo",
       "Bot ≥50.000 bạn bè",
       "- Mọi thao tác hoàn tất, không timeout, không màn trắng\n"
       "- Ghi lại số đo thực tế cho từng thao tác làm evidence để Leader đánh giá ngưỡng chấp nhận",
       env="PRODUCTION",
       note="RULE-08. Bug tự detect #39257 chính là vấn đề hiệu năng của thao tác xác nhận toàn bộ. "
            "Nguồn: Test fix bug Kh r98 + Leftbar+Header r563"),

    tc("Phân quyền staff & môi trường", "REG-SHARED-001", "Normal",
       "Sau khi sửa chat 1:1 — rà lại các màn dùng chung dữ liệu hội thoại",
       BOT + "\n- Đã chuẩn bị dữ liệu ở các màn liên quan",
       "1. Với mỗi màn ở cột Dữ liệu test: mở màn và kiểm tra dữ liệu hội thoại hiển thị đúng\n"
       "2. Thực hiện 1 thao tác cơ bản trên từng màn\n"
       "3. Đối chiếu ngược lại với chat 1:1",
       "Màn quản lý chat (talk list) · màn danh sách bạn bè · màn chi tiết bạn bè (my_page) · "
       "màn quản lý tin nhắn lỗi · màn thống kê gửi tin · app mobile",
       "- Mọi màn hiển thị đúng dữ liệu hội thoại, không lỗi\n"
       "- Thao tác cơ bản trên từng màn chạy đúng và phản ánh ngược lại chat 1:1",
       env="PRODUCTION",
       note="Nguồn: Improve move database r16-r27 + Test fix bug Kh r97 — cần thiết vì chat 1:1 dùng chung "
            "bảng hội thoại và bảng tin nhắn với nhiều tính năng"),

    tc("Phân quyền staff & môi trường", "REG-RUN-001", "Normal",
       "Kiểm tra tổng thể sau khi phát hành — luồng chính của chat 1:1 trên web và app",
       BOT + "\n- Bot standard/pro có đủ dữ liệu: bạn bè, nhóm, tag, scenario, rich menu, form, ghi chú",
       "1. Cột trái: xem danh sách, tải thêm, lọc, tìm kiếm, quick action (ẩn/chặn, bookmark, xác nhận, "
       "đổi trạng thái, gắn/gỡ tag), quản lý profile người gửi\n"
       "2. Cột giữa: xem lịch sử chat, tải thêm tới năm cũ, chuyển hội thoại, gửi text/media/PDF/sticker/"
       "template/multi action/trả lời trích dẫn, bookmark, đổi trạng thái, xác nhận, ẩn hội thoại\n"
       "3. Cột phải: 5 tab (thông tin cơ bản, friend info, tag, kết quả form, ghi chú) — xem và cập nhật\n"
       "4. Lặp lại các bước chính trên app mobile",
       "Bot standard/pro với dữ liệu đầy đủ; kiểm tra trên web và app mobile",
       "- Mọi chức năng hiển thị đúng dữ liệu và thao tác được bình thường\n"
       "- Không lỗi JS, không màn trắng, không mất dữ liệu\n"
       "- Kết quả nhất quán giữa web và app mobile",
       env="PRODUCTION",
       note="Bộ case chính dùng cho mỗi lần phát hành. Nguồn: Test fix bug Kh r13-r62 + Maincase (tab flat)"),
]
