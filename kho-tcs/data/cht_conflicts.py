# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ CHỜ QUYẾT ĐỊNH của Leader.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

CONFLICTS = [
    ["MT-01", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Gửi tin từ LME có cập nhật tin nhắn cuối của bạn bè hay không — spec nói CÓ, TC mới nhất nói KHÔNG",
     "SpecImprove #35389 (4/2026 — khối MỚI NHẤT của tab master 「Content: Send message」r302-r350):\n"
     "• Tiêu đề ticket: 「Sửa khi send message ko update last message và last time send, "
     "Chỉ update khi có message friend gửi đến」\n"
     "• Hơn 60 dòng TC (r32-r35, r38-r55, r74-r81, r104-r127, r222-r248, r267-r301) đều có Expected: "
     "「Spec change 4/2026: Không update last message của friend / + Time của last message không update / "
     "+ Nội dung last message không update」\n"
     "• Áp cho MỌI đường gửi từ LME: chat 1:1 (web + app), đặt lịch, send test ở Template/Broadcast/"
     "Scenario/Remind, trả lời ở talk list, action text của salon/lesson/kết bạn/QR/form, action tag, "
     "job Broadcast/Scenario/Event remind, action schedule\n"
     "• Chiều ngược lại (r303-r311): friend gửi tin đến bot thì VẪN update last message",
     "• `feature-spec.md:57` Luồng 1 gửi text: 「MessageService@createMessageV2: … "
     "3. UPDATE conversation (last_message, last_time_message)」\n"
     "• `db/db-mapping.md:879`: 「UPDATE conversation SET last_message = ?, last_time_message = NOW() WHERE id = ?」 "
     "nằm trong chuỗi SQL của luồng gửi tin\n"
     "• `feature-spec.md:391-392` Field Traceability cột trái: Last message / Last message date map thẳng vào "
     "conversation.last_message / last_time_message, không ghi điều kiện gì\n"
     "→ Spec KHÔNG hề nhắc tới thay đổi 4/2026",
     "Đây KHÔNG phải chi tiết kỹ thuật — nó đổi hành vi người dùng cuối thấy được. "
     "Theo BR-02 (`feature-spec.md:464`) danh sách bạn bè sắp xếp theo `last_time_message DESC`. "
     "Nếu admin gửi tin mà không cập nhật last_time_message thì hội thoại KHÔNG nhảy lên đầu danh sách sau khi trả lời, "
     "và dòng tin nhắn cuối vẫn hiện tin của friend chứ không phải tin admin vừa gửi. "
     "Người đọc spec sẽ tin ngược lại và viết TC sai; tester đọc spec sẽ báo bug nhầm.",
     "TC-CHT-* nhóm 「Gửi text & phím tắt」(3 TC), 「Chèn friend info vào tin nhắn」(1 TC), "
     "「Gửi sticker」(1 TC), 「Gửi template — nội dung & action」(1 TC)",
     "",
     "Chốt hành vi đúng cho 4 ô: (LME gửi / friend gửi) × (last_message / last_time_message). "
     "Nếu quyết định theo #35389: cập nhật `feature-spec.md:57`, `db-mapping.md:879`, và bổ sung 1 Business Rule "
     "mới ghi rõ 「chỉ friend gửi tin mới cập nhật tin nhắn cuối」; đồng thời ghi rõ hệ quả lên BR-02 "
     "(thứ tự sắp xếp danh sách bạn bè). Nếu code chưa fix thì các TC này dự kiến FAIL → raise bug."],

    ["MT-02", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Tính năng trả lời trích dẫn (reply/quote) — spec KHÔNG có mô tả nghiệp vụ nào",
     "Corpus có ~230 dòng về trả lời trích dẫn ở tab 「Content: Hiển thị msg」 (r6-r13, r909-r1140):\n"
     "• Feature #28618 (02/2025) 「Hiển thị reply message từ phía line friend」+ Support #27755 (01/2025)\n"
     "• Bot trích dẫn: icon mũi tên trên tin, khung trích dẫn hiện avatar + tên + nội dung tin gốc\n"
     "• Loại tin KHÔNG trích dẫn được: audio (r916, r924, r961), vị trí (r926, r969), file (r917), "
     "image map (r965 — ảnh thường thì được)\n"
     "• Trả lời bằng media/template thì KHÔNG giữ trích dẫn, gửi như tin thường (r948)\n"
     "• Chuyển sang friend khác thì xoá trích dẫn + nội dung đang gõ (r950, Support #29057)\n"
     "• Bấm vào khung trích dẫn KHÔNG nhảy tới tin gốc (r991)\n"
     "• Friend trích dẫn: hiển thị đúng profile của tin gốc, đúng cho ~50 đường gửi của LME (r1054-r1137)",
     "• `db/db-mapping.md:119-121`: bảng tin nhắn có 3 cột `quote_token`, `quote_message_id`, "
     "`quote_message_content` — CHỈ có mô tả cột, không có quy tắc nghiệp vụ\n"
     "• `feature-spec.md` §2 (8 luồng end-to-end): KHÔNG có luồng trả lời trích dẫn\n"
     "• `feature-spec.md` §5 (17 Business Rules BR-01..BR-17): KHÔNG có rule nào về trích dẫn\n"
     "• `feature-spec.md` §6 (49 endpoints): không có endpoint riêng cho trích dẫn\n"
     "• `job/job-spec.md:256` chỉ có 1 dòng `needQuoteToken = true`",
     "Đây là tính năng người dùng cuối nhìn thấy và dùng hàng ngày, đã phát hành từ 02/2025, "
     "nhưng spec chỉ có 3 cột DB. Không có tài liệu nào trả lời được: loại tin nào trích dẫn được, "
     "trích dẫn bị xoá khi nào, trả lời bằng media thì ra tin gì. Tester mới đọc spec sẽ bỏ sót toàn bộ vùng này.",
     "TC-CHT-* nhóm 「Reply / quote message」(15 TC)",
     "",
     "Bổ sung vào `feature-spec.md`: 1 luồng end-to-end cho trả lời trích dẫn + ≥3 Business Rule "
     "(loại tin hỗ trợ trích dẫn, điều kiện xoá trích dẫn, hành vi khi trả lời bằng media/template). "
     "Bổ sung mô tả nghiệp vụ cho 3 cột quote_* ở `db-mapping.md`."],

    ["MT-03", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Bot gói miễn phí chỉ xem được 180 ngày lịch sử chat — spec KHÔNG có rule này",
     "Feature #28859 (6/2025 — tab riêng trong file master, 8 TC lá):\n"
     "• Bot standard / pro / enterprise: hiện được TOÀN BỘ lịch sử chat (r3-r5)\n"
     "• Bot free: tin trong 180 ngày hiện bình thường; tin cũ hơn 180 ngày KHÔNG hiện, thay bằng "
     "「180日以上前のトーク閲覧はエルメの有料プランご契約が必要です」(r6-r8)\n"
     "• Áp dụng cho cả web và app mobile (r7, r8)\n"
     "• Bấm chữ 有料プラン → mở màn nâng cấp gói (r9); sau khi nâng cấp thì hiện lại toàn bộ tin (r10)\n"
     "• Tab 「Test fix bug Kh」r29 nhắc lại rule này khi kiểm tra bot free",
     "• `feature-spec.md:469` BR-07 「Gioi han gui mien phi」: chỉ có giới hạn 1000 tin/tháng "
     "(`free_send_count`), KHÔNG nhắc tới 180 ngày\n"
     "• `db/db-mapping.md:702-706` §5.14 `bots.plan_type`: 「2 = Free — Gioi han 1000 tin/thang」, "
     "không có mô tả giới hạn xem lịch sử\n"
     "• `feature-spec.md:471` BR-10 (message sharding): mô tả cách LẤY lịch sử theo bảng, "
     "không có điều kiện lọc theo gói cước\n"
     "→ Toàn bộ spec KHÔNG có chỗ nào nói tới con số 180 ngày",
     "Đây là giới hạn TÍNH PHÍ mà khách hàng nhìn thấy trực tiếp. Người đọc spec sẽ tin bot free "
     "xem được toàn bộ lịch sử (vì BR-10 mô tả lấy đủ 3 tầng bảng) và không test vùng này. "
     "Ngược lại nếu code lỗi và hiện quá 180 ngày cho bot free thì đó là thất thoát doanh thu — "
     "không ai phát hiện vì không có rule để đối chiếu.",
     "TC-CHT-* nhóm 「Giới hạn plan & token」(3 TC: bot trả phí / bot miễn phí / sau khi nâng cấp)",
     "",
     "Bổ sung vào `feature-spec.md` §5 một Business Rule mới về giới hạn 180 ngày cho gói free, "
     "ghi rõ: mốc tính từ đâu, áp cho cả web và app, nội dung thông báo, hành vi sau khi nâng cấp gói. "
     "Bổ sung điều kiện lọc theo gói cước vào mô tả BR-10 và vào `db-mapping.md` §5.14."],

    ["MT-04", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Màn Cài đặt chat có 6 tab hay 8 tab — spec nói 6, TC mới nhất nói 8",
     "Tab 「[AI] Flow_setting_chat_v2」+ 「AI_TCs_Setting_chat_v1」 (06-07/2026 — bộ TC MỚI NHẤT của file master, "
     "cột kết quả ghi Pass trên cả staging và production):\n"
     "• TC-SC-001: sidebar trái hiển thị đúng 8 tab theo thứ tự:\n"
     "  1.「対応ステータス編集」2.「チャットのCSVエクスポート」3.「メッセージの自動確認済み変更」\n"
     "  4.「送信ショートカット」5.「短縮URLの利用」6.「送信プレビュー」7.「既読情報の表示」8.「重複送信防止機能」\n"
     "• Ghi chú của TC: 「FA-041 sidebar mở rộng từ 6 → 8 tab, thứ tự đã xác nhận QA-026」\n"
     "• TC-SC-003 mô tả tab CSV có job chạy nền với thanh tiến trình",
     "• `feature-spec.md:31`: 「SCR-CHT-02: Man hinh Cai dat Chat — 6 tabs cau hinh "
     "(status, auto-confirm, shortcut, shorten URL, preview, FAQ)」\n"
     "• `feature-spec.md:179-215` §2.2 mô tả CHI TIẾT đúng 6 tab, tab 6 là FAQ chỉ đọc\n"
     "• `spec-features/admin/chat-setting/feature-spec.md:27`: 「Phạm vi ¦ 6 tab + 1 modal add/edit status」\n"
     "• `spec-features/admin/chat-setting/feature-spec.md:464`: 「Số màn hình ¦ 7 (6 tab + 1 modal)」\n"
     "→ CẢ HAI spec (chat-11 và chat-setting) đều nói 6 tab",
     "2 tab MỚI (「チャットのCSVエクスポート」xuất CSV chat và「重複送信防止機能」chống gửi trùng) "
     "hoàn toàn vắng mặt trong spec — kể cả spec riêng của màn cài đặt. Tab xuất CSV còn có job chạy nền, "
     "tức là có cả luồng máy chủ chưa được ghi lại. Bất kỳ ai lập kế hoạch test dựa trên spec sẽ bỏ sót 2 tab.",
     "Không có TC trong tab FA-001 (màn cài đặt chat được gom ở FA-041) — "
     "mâu thuẫn này ghi nhận để sửa spec, và ảnh hưởng phạm vi khi gom FA-041",
     "",
     "Cập nhật `feature-spec.md:31` và §2.2 của chat-11, đồng thời cập nhật `chat-setting/feature-spec.md:27, 464` "
     "lên 8 tab. Bổ sung mô tả nghiệp vụ + endpoint + job cho 2 tab mới. "
     "Quyết định luôn: khi gom FA-041 thì lấy tab 「Setting Chat」(human) hay 4 tab 「[AI]」làm nguồn chính."],

    ["MT-05", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Khoảng giãn cách khi gửi tin dạng delay — spec nói 2-4 giây, TC nói 2-5 giây",
     "• Tab 「Content: Send message」r1093: 「check setting send temp delay => mỗi temp con sẽ send "
     "cách nhau 2-5s」\n"
     "• Tab 「Rightbar」r382-r383: 「các msg phía sau save vào DB để job send … tại cột time_send "
     "thời gian của các template sẽ tăng dần + (2-5s)」",
     "• `feature-spec.md:104`: 「scheduleSendDelay() → INSERT send_random_messages (gian cach 2-4s)」\n"
     "• `feature-spec.md:626`: lặp lại 「gian cach 2-4s」\n"
     "• `db/db-mapping.md:401`: cột `time_send` — 「Thoi gian gui (gian cach 2-4s)」\n"
     "• `db/db-mapping.md:943`: 「tach thanh nhieu record send_random_messages voi thoi gian gian cach 2-4 giay」\n"
     "• `job/job-spec.md:132`: 「thoi gian gui gian cach ngau nhien 2-4 giay」",
     "Chênh 1 giây ở biên trên. Tester đo được khoảng cách 4,5 giây sẽ không biết là PASS hay FAIL: "
     "theo spec là vượt ngưỡng, theo TC là hợp lệ. Ảnh hưởng trực tiếp tới việc verify job gửi giãn cách.",
     "TC-CHT-* 「Gửi template — nội dung & action」(TC delay) và 「Đặt lịch gửi — delay & job」(TC bật giãn cách)",
     "",
     "Nhờ Dev xác nhận khoảng ngẫu nhiên thực tế trong code. Sau đó sửa CHO KHỚP ở cả 5 chỗ trong spec "
     "(`feature-spec.md:104, 626` · `db-mapping.md:401, 943` · `job-spec.md:132`) hoặc sửa TC — "
     "và ghi rõ ngưỡng cho phép khi đo thủ công."],

    ["MT-06", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Trạng thái của bản ghi lịch gửi — spec TỰ MÂU THUẪN giữa BR-11 và mô tả job",
     "• Tab 「Rightbar」r269: thêm tin nhắn mà không lưu → 「check db: status = -1」 (nháp)\n"
     "• Tab 「Rightbar」r272: thao tác từ app mobile ghi đè → 「bản ghi được đè update status = 0 để send」\n"
     "• Tab 「Rightbar」r369-r370: tắt job → 「status = 0, user chưa nhận được tin nhắn」\n"
     "→ TC chỉ chứng kiến 2 giá trị -1 và 0, KHÔNG có TC nào kiểm tra giá trị sau khi gửi xong",
     "• `feature-spec.md:471` BR-11: 「3 trang thai: -1 (draft), 0 (cho gui), 2 (da huy)」\n"
     "• `feature-spec.md:117` §2.1 Luồng 4 (mô tả job): 「UPDATE schedule_send_chat.status = 1」\n"
     "→ BR-11 liệt kê 3 giá trị nhưng KHÔNG có giá trị 1, trong khi chính spec mô tả job set status = 1",
     "Spec tự mâu thuẫn với chính nó. Tester đọc BR-11 sẽ tin trạng thái sau khi gửi xong vẫn là 0 hoặc 2, "
     "và sẽ báo bug nhầm khi thấy giá trị 1 trong DB. Cũng không rõ giá trị 2 (đã huỷ) sinh ra khi nào — "
     "corpus không có TC nào cho nhánh này.",
     "TC-CHT-* nhóm 「Đặt lịch gửi — soạn & lưu」(TC lưu nháp, TC lưu lịch, TC huỷ đặt lịch) "
     "và 「Đặt lịch gửi — delay & job」(TC tắt/bật job)",
     "",
     "Liệt kê ĐỦ các giá trị trạng thái trong BR-11 (-1 nháp / 0 chờ gửi / 1 đã gửi / 2 đã huỷ) "
     "và ghi rõ ai chuyển trạng thái ở mỗi bước. Bổ sung TC cho nhánh trạng thái đã huỷ (hiện corpus chưa có)."],

    ["MT-07", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Giới hạn độ dài 送信ユーザー名 (tên profile người gửi) — CORPUS TỰ MÂU THUẪN, spec không ghi gì",
     "Tab 「Leftbar+Header」, cùng 1 màn Thêm/Sửa profile:\n"
     "• r352: 「nhập 20 ký tự」→ Expected: 「success」\n"
     "• r356: 「Nhập 20 ký tự」→ Expected: 「không nhập được ký tự 31」 (câu này tự mâu thuẫn: "
     "nhập 20 mà nói tới ký tự thứ 31)\n"
     "• r387 (màn Sửa profile): 「Nhập 31 ký tự」→ Expected: 「invalid」\n"
     "• r384: 「nhập 20 ký tự」→ 「success」; r385: 「nhập 10 ký tự」→ 「success」\n"
     "→ Không suy ra được giới hạn là 20 hay 30 ký tự",
     "• `db/db-mapping.md:328-338` §3.13 `bots_profiles`: liệt kê cột `nick_name` nhưng KHÔNG ghi "
     "kiểu dữ liệu độ dài hay ràng buộc\n"
     "• `feature-spec.md:507` Field Traceability: 「Ten nguoi gui (admin) ¦ 「送信ユーザー名」¦ bots_profiles ¦ "
     "nick_name」— cột Validation để trống\n"
     "• `feature-spec.md` §5: KHÔNG có Business Rule nào về độ dài tên profile\n"
     "→ Spec KHÔNG có bất kỳ con số nào",
     "Tên profile người gửi hiển thị trực tiếp trên app LINE của người dùng cuối. "
     "Nếu giới hạn thực là 30 mà tester test theo 20 thì bỏ lọt vùng 21-30; nếu ngược lại thì báo bug nhầm. "
     "Không tài liệu nào, kể cả TC gốc, trả lời được câu hỏi này.",
     "TC-CHT-* 「Profile người gửi — quản lý」(TC giới hạn độ dài — đã viết dưới dạng ĐO ngưỡng thực tế)",
     "",
     "Nhờ Dev xác nhận ràng buộc thực tế (cả tầng giao diện và tầng máy chủ, cả khi Thêm và khi Sửa). "
     "Ghi con số vào cột Validation của `feature-spec.md:507`, bổ sung ràng buộc cột `nick_name` "
     "vào `db-mapping.md` §3.13, và ghi rõ cơ chế khi vượt ngưỡng là CHẶN NHẬP hay BÁO LỖI "
     "(tuyệt đối không cắt âm thầm)."],

    ["MT-08", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Ẩn bạn bè thì tự động xác nhận tin — người dùng chọn 「未確認」vẫn bị ghi đè thành đã xác nhận",
     "• Tab 「Leftbar+Header」r241: 「friend chưa confirm」→ Expected: 「spec cũ là ẩn đi thì sẽ confirm」\n"
     "• r289 (kết hợp 2 action): 「確認状況を変更 với 非表示・ブロック」→ Expected: "
     "「spec cũ là ẩn đi thì sẽ confirm => chọn option chưa confirm nhưng friend vẫn bị hiển thị đã confirm là đúng」\n"
     "• Tab 「improve count comfirm_message」r31: 「bot ẩn friend」→ 「thực hiện như case comfirm message: "
     "confirm_count = 0, has_status_1 = 1, bảng unconfirm_message không còn bản ghi」",
     "• `feature-spec.md:467` BR-05 「An friend — tu dong xac nhan」: 「Khi an friend, tu dong xac nhan "
     "tat ca tin chua doc. Tao tin he thong「非表示しました」」\n"
     "→ Spec CÓ mô tả hành vi tự động xác nhận, nhưng KHÔNG nói gì về trường hợp người dùng chọn đồng thời "
     "「未確認」và「非表示」ở modal quick action",
     "Hành vi hiện tại đi NGƯỢC lựa chọn của người dùng: chọn 「chuyển sang chưa xác nhận」nhưng kết quả là "
     "「đã xác nhận」. TC gốc gọi đây là 「spec cũ」— tức chính người viết TC cũng không chắc rule này còn đúng. "
     "Đây là vùng dễ gây khiếu nại: bạn bè bị ẩn kèm mất luôn dấu chưa đọc.",
     "TC-CHT-* 「Quick action — xác nhận, ẩn, block」(TC ẩn bạn bè có tin chưa xác nhận) và "
     "「Quick action — tag & kết hợp action」(TC kết hợp 未確認 + 非表示), 「Bộ đếm chưa xác nhận」(TC bot ẩn bạn bè)",
     "",
     "Chốt: (a) ẩn bạn bè có còn tự động xác nhận không; (b) khi chọn đồng thời 未確認 + 非表示 thì "
     "ưu tiên lựa chọn nào. Sau đó bổ sung vào BR-05 phần xử lý xung đột giữa 2 action, "
     "và cân nhắc chặn/cảnh báo ở giao diện khi người dùng chọn tổ hợp mâu thuẫn."],

    ["MT-09", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Cơ chế lưu trữ tin nhắn cũ — spec liệt kê bảng theo NĂM, corpus mô tả bảng lưu trữ theo TRANG",
     "• File 「01. TCsLine_Chat1:1」(cũ) tab 「Improve move database」(09/2023): mô tả 2 bảng lưu trữ "
     "`message_page_2` và `message_old`; kiểm tra tải lịch sử, xác nhận / bỏ xác nhận tin ở từng bảng (r3-r15); "
     "kiểm tra job chuyển tin giữa 2 bảng (r28, r29)\n"
     "• Tab 「Job move message」(TCsLine_Improve chung + TCsLine_JOB): mô tả CHI TIẾT quy tắc — "
     "hội thoại ≤20 tin thì không chuyển; >20 tin thì giữ lại 20 tin mới nhất, phần còn lại chuyển sang bảng lưu trữ; "
     "trùng thời điểm tạo thì giữ tin có mã lớn hơn; giữ nguyên mã, thời điểm tạo và cập nhật (r3-r14)\n"
     "• Tab 「Content: Hiển thị msg」r1426-r1435 (mới hơn): mô tả cơ chế theo NĂM — "
     "kiểm tra tổ hợp bảng mới / bảng cũ / 2023 / 2024 / 2025",
     "• `feature-spec.md:317-320` §3.3 Secondary Tables: liệt kê `messages_2020`...`messages_2025` "
     "(sharded theo năm) + `messages_conversation_mapping`\n"
     "• `feature-spec.md:471` BR-10 「Message sharding theo nam」: 「messages_v2s → messages → messages_{year}」\n"
     "→ Spec KHÔNG có `message_page_2` và `message_old` ở bất kỳ đâu",
     "Không rõ 2 bảng `message_page_2` / `message_old` đã bị cơ chế theo năm thay thế hoàn toàn hay vẫn còn "
     "dữ liệu lịch sử nằm ở đó. Nếu vẫn còn mà spec không ghi, tester sẽ không test đường tải dữ liệu từ 2 bảng này "
     "và có thể bỏ lọt bug mất lịch sử chat của khách hàng lâu năm — đúng loại bug mà #33113 và #36859 đã từng xảy ra.",
     "TC-CHT-* nhóm 「Lịch sử chat & bảng message」(5 TC)",
     "",
     "Nhờ Dev xác nhận: 2 bảng `message_page_2` / `message_old` còn tồn tại và còn dữ liệu không; "
     "job chuyển tin giữa chúng còn chạy không. Nếu còn: bổ sung vào `feature-spec.md` §3.3 và BR-10. "
     "Nếu đã bỏ: ghi rõ mốc thời gian ngừng dùng và cách dữ liệu cũ đã được chuyển đi, "
     "rồi đánh dấu các TC của tab 「Improve move database」là lỗi thời."],

    ["MT-10", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Giới hạn dung lượng và định dạng file khi gửi media ở chat 1:1 — spec không ghi",
     "Tab 「Content: Send message」khối gửi media:\n"
     "• r409-r411: 「ảnh > 10 MB」/「video > 200 MB」/「audio > 25MB」 — nằm trong khối 「check upload fail」\n"
     "• r412: 「upload > 5 file media cùng 1 lúc」→ 「msg validate: 同時にアップロードできるのは最大5つだけです。」\n"
     "• r403-r406: định dạng hợp lệ — ảnh jpg/png/jpeg, audio m4a, video mp4\n"
     "• r413-r415: định dạng bị chặn — ảnh tiff/gif; video avi/wmv/mkv; audio wma/wav/mkv/mp3",
     "• `feature-spec.md:76-79` Luồng 2 gửi media: chỉ ghi 「Xu ly file: Image resize 1040px, "
     "Video tao thumbnail, Audio convert M4A」và 「Chunk thanh nhom 5 (gioi han LINE API)」\n"
     "• `feature-spec.md` §4 Field Traceability: không có dòng nào cho giới hạn media\n"
     "• `feature-spec.md` §5: không có Business Rule nào về dung lượng/định dạng\n"
     "→ Spec có con số 5 file (chunk) nhưng KHÔNG có dung lượng và danh sách định dạng",
     "Đây là ràng buộc người dùng gặp hàng ngày và là nguồn khiếu nại phổ biến (không gửi được ảnh). "
     "Không có trong spec nghĩa là không ai biết khi nào lỗi là do giới hạn hệ thống, khi nào là bug. "
     "Ngoài ra con số 5 trong spec được giải thích là giới hạn LINE API, còn TC lại mô tả nó như "
     "giới hạn số file upload một lần ở giao diện — hai chuyện khác nhau.",
     "TC-CHT-* nhóm 「Gửi media」(TC vượt dung lượng, TC sai định dạng, TC giới hạn 5 file)",
     "",
     "Bổ sung vào `feature-spec.md` một Business Rule liệt kê đủ: dung lượng tối đa từng loại, "
     "danh sách định dạng được phép, số file tối đa mỗi lần và thông báo lỗi tương ứng. "
     "Đối chiếu với ma trận media ở `framework/catalog-lme.md` để bảo đảm nhất quán giữa các tính năng."],

    ["MT-11", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Hai chỗ upload ảnh trong CÙNG màn chat 1:1 có quy tắc định dạng khác nhau",
     "• Tab 「Leftbar+Header」r345-r348 (ảnh profile người gửi, màn Thêm): 「Upload ảnh png」→ success; "
     "「Upload ảnh jpg, gif, jpeg」→ 「hiển thị msg png画像を選択してください。 / hiện tại: ảnh khác không hiển thị để chọn」\n"
     "• r378-r380 (màn Sửa profile): lặp lại đúng quy tắc CHỈ PNG\n"
     "• Tab 「Rightbar」r112 (friend info kiểu ảnh): 「check button 編集」→ "
     "「thay đổi/upload ảnh success — chỉ cho phép upload định dạng png, jpg」\n"
     "• r115 (friend info kiểu PDF): cũng ghi 「chỉ cho phép upload định dạng png, jpg」 "
     "(bản thân dòng này cũng đáng ngờ vì đang nói về mục PDF)",
     "• `feature-spec.md` §4.6 và §4.4 Field Traceability: cột Validation của cả 「送信ユーザー画像」"
     "và custom field đều để TRỐNG\n"
     "• `db/db-mapping.md` §3.13 `bots_profiles.avt_path`: không ghi ràng buộc định dạng\n"
     "→ Spec không có quy tắc nào cho cả 2 chỗ",
     "Cùng một màn hình, cùng thao tác 「upload ảnh」nhưng 2 chỗ nhận định dạng khác nhau — "
     "người dùng sẽ nhầm và tester không có căn cứ để nói chỗ nào đúng. Riêng dòng r115 nói mục PDF "
     "chỉ nhận png/jpg còn tự mâu thuẫn ngay trong TC gốc.",
     "TC-CHT-* 「Profile người gửi — quản lý」(TC validate ảnh PNG) và 「Rightbar — 友だち情報」"
     "(TC mục kiểu ảnh và kiểu PDF)",
     "",
     "Chốt định dạng cho từng chỗ: (a) ảnh profile người gửi; (b) friend info kiểu ảnh; (c) friend info kiểu PDF. "
     "Ghi vào cột Validation tương ứng trong `feature-spec.md` §4.4 và §4.6. "
     "Nếu 2 chỗ khác nhau là chủ ý thì ghi rõ lý do; nếu không thì thống nhất lại."],

    ["MT-12", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Tổ hợp chéo điều kiện lọc tag và lọc 対応ステータス — chưa ai xác nhận hành vi",
     "Tab 「Leftbar+Header」khối 「Filter kết hợp tag và status」:\n"
     "• r65: 「Filter tag điều kiện OR + Filter status điều kiện OR」→ 「hiển thị friend thỏa mãn all đk」\n"
     "• r66: 「Filter tag điều kiện AND + Filter status điều kiện AND」→ 「hiển thị friend thỏa mãn all đk」\n"
     "• r67: 「Filter tag điều kiện OR + Filter status điều kiện AND」→ 「hiện tại mình chưa làm 2 case này」\n"
     "• r68: 「Filter tag điều kiện AND + Filter status điều kiện OR」→ 「hiện tại mình chưa làm 2 case này」\n"
     "→ 2/4 ô của ma trận bị bỏ trống, TC gốc thừa nhận chưa test",
     "• `feature-spec.md:466` BR-04 「Tag filter AND/OR」: chỉ mô tả cho TAG "
     "(OR = có ít nhất 1 tag; AND = có tất cả tag)\n"
     "• `feature-spec.md:121-122` Luồng 5: 「Filter tag: AND logic … hoac OR logic … 」— "
     "cũng chỉ nói về tag\n"
     "• `web/logic-spec.md:166` `getFriend()`: 「Filter theo tags (AND/OR)」— không nhắc status\n"
     "→ Spec KHÔNG mô tả điều kiện AND/OR cho 対応ステータス và KHÔNG mô tả quan hệ giữa 2 nhóm lọc",
     "Bộ lọc là cửa vào của mọi thao tác hàng loạt (đặc biệt là 全て確認済みに変更 — thao tác không hoàn tác được). "
     "Nếu tổ hợp chéo trả về tập bạn bè sai, admin sẽ xác nhận nhầm hàng loạt hội thoại của khách. "
     "Hiện không có tài liệu nào nói tập kết quả đúng phải là gì.",
     "TC-CHT-* 「Modal 絞り込み — tag & trạng thái」(TC tổ hợp chéo — viết dưới dạng GHI NHẬN hành vi thực tế) "
     "và TC lọc theo trạng thái điều kiện AND",
     "",
     "Chốt hành vi cho đủ 4 ô của ma trận (tag OR/AND × status OR/AND) và quan hệ giữa 2 nhóm lọc. "
     "Bổ sung vào BR-04 phần điều kiện AND/OR của 対応ステータス. Nếu 2 tổ hợp chéo chưa hỗ trợ thì "
     "phải chặn ở giao diện chứ không trả kết quả sai âm thầm."],

    ["MT-13", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "URL rút gọn — chat 1:1 hiện link GỐC còn app LINE hiện link rút gọn; spec không nói tầng hiển thị",
     "Tab 「Content: Send message」:\n"
     "• r545-r546 (preview trước khi gửi template): 「chỗ này update là dù shorten thì hiển thị trên chat 11 "
     "cũng hiển thị link gốc / chỉ có bên user hiển thị theo setting shorten thôi」\n"
     "• r1101-r1112 (khối 「check setting shorten temp」): tất cả 12 dòng đều có Expected "
     "「chat 11 + preview: hiển thị url gốc / user: hiển thị shorten」— đúng cho mọi tổ hợp "
     "(bật/tắt shorten ở chat 1:1 × gửi template / multi action / action từ nút bấm / dán URL trực tiếp)\n"
     "• r203: 「có shorten」→ 「giữ nguyên link đã nhập」\n"
     "• r222-r225: 「url ở last message hiện link gốc」",
     "• `feature-spec.md:477` BR-15 「URL rut gon tu dong」: 「Khi bots.is_shorten_url=1: URL trong tin text "
     "→ short URL qua ChatHelper@sendShortUrl. Phuc vu FA-023 URL Analysis」\n"
     "• `feature-spec.md:55` Luồng 1: 「Neu is_shorten_url=1: chuyen URL thanh short URL → BR-15」\n"
     "→ Spec chỉ mô tả việc CHUYỂN ĐỔI, KHÔNG nói gì về việc chat 1:1 vẫn hiển thị link gốc",
     "Người đọc spec sẽ tin rằng bật rút gọn thì mọi nơi đều thấy link rút gọn — kể cả chat 1:1. "
     "Thực tế chat 1:1 và màn xem trước cố tình giữ link gốc để admin đọc được. "
     "Tester sẽ báo bug nhầm ngay lần đầu kiểm tra, hoặc ngược lại bỏ qua khi chat 1:1 hiện nhầm link rút gọn.",
     "TC-CHT-* nhóm 「Shorten URL」(4 TC)",
     "",
     "Bổ sung vào BR-15 phần TẦNG HIỂN THỊ: ghi rõ chat 1:1 và màn xem trước luôn hiển thị URL gốc, "
     "chỉ phía người dùng LINE mới nhận URL rút gọn; và ghi rõ thứ tự ưu tiên giữa cấu hình rút gọn "
     "của template và cấu hình của chat 1:1."],

    ["MT-14", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Nhóm LINE — spec không có quy tắc nào cho hội thoại nhóm",
     "File 「01. TCsLine_Chat1:1」(cũ) tab 「Group chat」(05/2023, 64 dòng):\n"
     "• r15-r17: nhóm ẨN 3 mục ở cột phải — システム表示名, friend info, tag\n"
     "• r45: gửi URL vào nhóm 「luôn không shorten」\n"
     "• r59-r63: các tính năng KHÔNG áp dụng cho nhóm — Broadcast 「không gửi message đến group chat」, "
     "tự động trả lời 「group chat sẽ không action auto-reply」, rich menu 「không set rich menu cho group」, "
     "lịch chạy action 「không action cho group」\n"
     "• r47-r50: thành viên nhóm bấm link form/item/booking → nếu chưa kết bạn thì chuyển sang màn kết bạn; "
     "nếu đã kết bạn thì kết quả lưu cho RIÊNG thành viên đó",
     "• `feature-spec.md:120` Luồng 5: chỉ có 1 dòng 「groupChat: conversation_kind=1」trong danh sách bộ lọc\n"
     "• `feature-spec.md:322` §3.3: liệt kê bảng `group_members` — 「Thanh vien nhom (conversation_kind=1)」\n"
     "• `feature-spec.md` §5 (17 Business Rules): KHÔNG có rule nào cho nhóm\n"
     "• `feature-spec.md` §2 (8 luồng): KHÔNG có luồng nào cho nhóm",
     "Nhóm LINE là một loại hội thoại riêng với hành vi khác hẳn bạn bè cá nhân (ẩn bớt tính năng, "
     "không nhận Broadcast, không nhận rich menu, URL không rút gọn). Spec chỉ coi nhóm là 1 giá trị bộ lọc. "
     "Ai đọc spec sẽ mặc định nhóm hoạt động y hệt bạn bè và bỏ sót toàn bộ vùng khác biệt này. "
     "Lưu ý: TC gốc từ 05/2023 — đã hơn 2 năm, cần verify lại.",
     "TC-CHT-* nhóm 「Group chat」(14 TC) và 「Danh sách nhóm — hiển thị」(6 TC)",
     "",
     "Verify lại toàn bộ danh sách khác biệt (TC gốc > 2 năm), sau đó bổ sung vào `feature-spec.md` "
     "một mục riêng cho hội thoại nhóm: các mục bị ẩn ở cột phải, danh sách tính năng không áp dụng, "
     "quy tắc URL, và hành vi khi thành viên nhóm bấm link của LME."],

    ["MT-15", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Các trường phục vụ bộ đếm chưa xác nhận — spec chỉ mô tả 1 trong 5 trường",
     "Tab 「improve count comfirm_message」(120 dòng TC) mô tả nhất quán 5 trường:\n"
     "• `conversation.confirm_count` — tăng 1 mỗi tin friend gửi đến (r3)\n"
     "• `conversation.has_status_0` — đánh dấu còn tin chưa xác nhận (r3, r10)\n"
     "• `conversation.has_status_1` — đánh dấu đã xác nhận (r10)\n"
     "• `conversation.status_last_message` — trạng thái tin cuối, 0/1 (r10, r19)\n"
     "• `bots.count_user_unconfirm` — tổng số bạn bè chưa xác nhận của bot, giảm 1 khi xoá bạn bè (r14-r18)\n"
     "• Bảng `unconfirm_message` — có/không bản ghi theo trạng thái (r10, r19)\n"
     "Tab 「Leftbar+Header」r542 (SpecImprove #35144) cũng nói rõ bug cũ là 「không count lại mà update "
     "count_user_unconfirm = 0 luôn => sai」",
     "• `db/db-mapping.md:83`: `status_last_message` — mô tả duy nhất 「Trang thai tin nhan cuoi」\n"
     "• `db/db-mapping.md:762`: `status_last_message` — 「Su dung noi bo」 (không giải thích thêm)\n"
     "• `feature-spec.md:394` Field Traceability: chỉ có 「Unread badge ¦ conversation.confirm_count ¦ "
     "0=da xac nhan, >0=chua」\n"
     "• `feature-spec.md` §5: BR-08 chỉ nói tự động xác nhận khi trả lời\n"
     "→ Spec KHÔNG mô tả `has_status_0`, `has_status_1`, `bots.count_user_unconfirm`",
     "Bộ đếm chưa xác nhận là con số admin nhìn thấy đầu tiên khi mở tool và là căn cứ cho bộ lọc 未確認. "
     "Nó được duy trì bởi ít nhất 5 trường ở 3 bảng, nhưng spec chỉ mô tả 1 trường. "
     "Bug #35144 và #39257 đều xuất phát từ vùng này. Không có spec đầy đủ thì không thể verify được "
     "bộ đếm đúng hay sai — và cũng chính là gốc của MT-19.\n"
     "Lưu ý: `feature-spec.md:394` ghi 「>0 = chua xac nhan」 nhưng `feature-spec.md:121` lại ghi điều kiện lọc "
     "là 「confirm_count=1」 — spec tự mâu thuẫn ngay bên trong (xem MT-19).",
     "TC-CHT-* nhóm 「Bộ đếm chưa xác nhận」(12 TC) và 「全て確認済みに変更」(11 TC)",
     "",
     "Bổ sung mô tả nghiệp vụ đầy đủ cho `has_status_0`, `has_status_1`, `status_last_message` và "
     "`bots.count_user_unconfirm` vào `db-mapping.md`; thêm 1 Business Rule mô tả vòng đời bộ đếm "
     "(khi nào tăng, khi nào giảm, khi nào giữ nguyên — bao gồm cả các nhánh chặn / bỏ chặn / ẩn / xoá bạn bè)."],

    ["MT-16", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Giới hạn độ dài tiêu đề và nội dung ghi chú — spec không ghi",
     "Tab 「Rightbar」khối メモ:\n"
     "• r198: 「Field tên quản lý = blank」→ 「hiển thị msg タイトルを入力してください。」\n"
     "• r199: 「nhập text tiếng nhật dưới 20 kí tự」→ 「save thành công」\n"
     "• r201: 「nhập 21 ký tự」→ 「không cho phép nhập trên 20 kí tự」\n"
     "• r204: 「Field nội dung = blank」→ 「hiển thị msg メモ本文を入力してください。」\n"
     "• r205, r207: nội dung dưới 1.000 ký tự lưu được; 「nhập hơn 1,000 ký tự」có TC riêng",
     "• `feature-spec.md:475` BR-13 「Memo history — gioi han 10」: chỉ nói giới hạn 10 lịch sử mỗi ghi chú\n"
     "• `feature-spec.md` §4.5 Field Traceability: 「Memo title ¦ memos.title」và 「Memo content ¦ memos.content」"
     "— cột Business Rule chỉ ghi BR-13, không có ràng buộc độ dài\n"
     "→ Spec KHÔNG có con số 20 và 1.000",
     "Mức độ thấp vì ghi chú là dữ liệu nội bộ, không gửi ra ngoài. Nhưng vẫn là ràng buộc nhập liệu "
     "mà tester cần biết để test biên, và người dùng cần biết để không mất nội dung đã soạn.",
     "TC-CHT-* 「Rightbar — メモ」(TC giới hạn độ dài — viết dưới dạng ĐO ngưỡng thực tế)",
     "",
     "Bổ sung ràng buộc bắt buộc + độ dài tối đa của 2 trường vào `feature-spec.md` §4.5 và "
     "`db-mapping.md` bảng ghi chú, kèm thông báo lỗi tương ứng và cơ chế khi vượt ngưỡng "
     "(chặn nhập hay báo lỗi)."],

    ["MT-17", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Phân quyền Staff ở Chat 1:1 — spec tự nhận CHƯA XÁC ĐỊNH, corpus có ~40 dòng TC nhưng không có kết quả mong đợi",
     "• Corpus rải rác ~40 dòng 「Check thao tác bằng account staff」 / 「check account staff」 ở khắp các tab "
     "(Leftbar+Header r20, r124, r196, r313, r403, r472, r540, r564; Content: Send message r175, r196, r374, "
     "r389, r1220, r1256; Content: Hiển thị msg r74, r951, r1383, r1605; Rightbar r74, r121, r156, r188, r251, r392) "
     "— TẤT CẢ đều để TRỐNG cột Expected Result\n"
     "• Tab 「Phân quyền」(TCsLine_Improve chung) mô tả 3 vai trò 副管理人 / 運用者 / サポート với thông báo "
     "「操作できません。この機能の操作権限が付与されていません。主管理者に操作権限を付与してもらうことで操作が可能となります。」 "
     "nhưng chỉ ở mức MÀN HÌNH (vào được hay không), không đi vào từng thao tác trong chat 1:1\n"
     "• Tab 「AI_TCs_Setting_chat_v1」TC-SC-124 nhắc ticket Feature #36819 về phân quyền staff cho màn cài đặt chat",
     "• `feature-spec.md:26` mô tả Staff: 「Tuy role — co the bi gioi han truy cap chat hoac chi xem. … "
     "**Luu y**: khong phat hien kiem tra quyen Staff trong code Chat 1:1 — co the Staff co toan quyen chat "
     "neu duoc gan menu (Confidence: **Trung binh**)」\n"
     "• `feature-spec.md` §6 Xac thuc: 「Khong dung Policies/Gates. Moi query filter theo bot_id tu session」\n"
     "→ Spec tự thừa nhận KHÔNG xác định được, độ tin cậy Trung bình",
     "Chat 1:1 là màn có quyền lực lớn nhất trong tool: gửi tin trực tiếp tới khách hàng cuối, xem toàn bộ lịch sử, "
     "sửa thông tin bạn bè, thao tác hàng loạt không hoàn tác được (全て確認済みに変更). "
     "Nếu Staff thực sự có toàn quyền chỉ vì được gán menu thì đây là rủi ro bảo mật, không chỉ là thiếu tài liệu. "
     "Corpus có 40 chỗ nhắc phải test staff nhưng không chỗ nào ghi kết quả kỳ vọng — nghĩa là chưa từng được chốt.",
     "TC-CHT-* nhóm 「Phân quyền staff & môi trường」(4 TC đầu — viết dưới dạng LẬP MA TRẬN quyền thực tế, "
     "bắt buộc kiểm tra ở tầng API chứ không chỉ giao diện)",
     "",
     "Nhờ Dev xác nhận có kiểm tra quyền ở tầng máy chủ cho các endpoint của chat 1:1 hay không. "
     "Lập ma trận quyền chính thức: 3 vai trò × các nhóm thao tác (xem / gửi tin / thao tác hàng loạt / "
     "sửa thông tin bạn bè / quản lý profile người gửi / chỉnh sửa 対応ステータス). "
     "Cập nhật `feature-spec.md:26` và §6 Xac thuc, nâng độ tin cậy lên Cao. "
     "Nếu phát hiện Staff bypass được ở tầng API → raise bug bảo mật ngay."],

    ["MT-18", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Bộ nhớ đệm 30 giây khi gửi lại template — spec không mô tả cơ chế đệm nào",
     "Bug KH #37831 (06/2026 — khối MỚI NHẤT của tab 「Content: Hiển thị msg」r1613-r1689):\n"
     "• Hiện tượng: template gửi qua action, sau khi sửa nội dung rồi gửi lại trong vòng 30 giây thì "
     "chat 1:1 hiện nội dung CŨ (dù phía LINE user nhận nội dung mới)\n"
     "• TC-NEW-01 (r1682): xác nhận mốc 30 giây\n"
     "• TC-NEW-02 (r1683): cùng hiện tượng với step message của scenario\n"
     "• TC-NEW-03 (r1684): template dùng chung cho action tag và step scenario → sửa 1 lần phải xoá đệm cả 2 phía\n"
     "• TC-NEW-05 (r1686): thêm template con mới thì danh sách ở chat 1:1 không mở rộng theo "
     "(nghi do so sánh danh sách 1 chiều)\n"
     "• TC-NEW-07 (r1688): đổi thứ tự template con — nhánh job hiện vẫn NG (Bug Tester #37907)",
     "• `feature-spec.md` §3.3: có bảng `capture_templates` — 「Template da capture — luu noi dung gui thuc te」\n"
     "• `feature-spec.md` §5: KHÔNG có Business Rule nào về bộ nhớ đệm\n"
     "• `web/logic-spec.md`: không mô tả cơ chế đệm nguồn tin nhắn\n"
     "→ Spec KHÔNG có mốc 30 giây, không có tên cơ chế đệm, không có điều kiện xoá đệm",
     "Hậu quả nhìn thấy được: admin sửa template rồi gửi lại, chat 1:1 hiện một đằng còn khách hàng nhận một nẻo. "
     "Admin không biết khách thực sự nhận được gì. Đây là lỗi khách hàng đã báo (#37831) và còn 1 nhánh chưa xong (#37907). "
     "Không có mốc 30 giây trong spec thì tester không biết phải chờ bao lâu mới kết luận là bug.",
     "TC-CHT-* 「Gửi template — nội dung & action」(4 TC: sửa template gửi lại, thêm/xoá/sắp xếp template con, "
     "dùng chung action + scenario, gửi lại sau 30 giây)",
     "",
     "Bổ sung vào `feature-spec.md` mô tả cơ chế đệm nguồn tin nhắn: phạm vi đệm, thời gian sống, "
     "sự kiện nào xoá đệm (sửa/xoá/sắp xếp template con, sửa step scenario), và ghi rõ ràng buộc "
     "「nội dung hiển thị ở chat 1:1 phải luôn khớp nội dung thực gửi cho người dùng LINE」. "
     "Theo dõi nhánh job của #37907 tới khi đóng."],

    ["MT-19", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Điều kiện lọc 「未確認」 — spec ghi confirm_count = 1, corpus chứng minh bộ đếm tăng dần theo số tin",
     "• Tab 「improve count comfirm_message」r3: 「friend nhắn tin đến bot」→ 「count số message bảng conversation "
     "cột confirm_count / mỗi lần nhắn 1 tin đến -> confirm_count + 1 / has_status_0 = 1」 "
     "→ bộ đếm có thể là 2, 3, 5… chứ không chỉ 1\n"
     "• Tab 「Leftbar+Header」r70: filter 未確認 → 「hiển thị friend có msg Chưa được xác nhận」\n"
     "• Tab 「Leftbar+Header」r74: SpecImprove #33731 [14-01-2026] [9330] — tiêu đề chính là "
     "「[Chat 1:1] Filter các friend unconfirm msg nhưng không hiển thị đủ list friend tương ứng」 "
     "→ khách hàng ĐÃ báo lỗi đúng vùng này",
     "• `feature-spec.md:121` Luồng 5 (Loc va tim kiem ban be): 「Filter theo filterTypeFriend: "
     "- all: is_hide=0 ¦ **unconfirm: confirm_count=1** ¦ confirm: confirm_count=0 …」\n"
     "• Ngược lại `feature-spec.md:394` Field Traceability lại ghi: 「Unread badge ¦ conversation.confirm_count ¦ "
     "**0=da xac nhan, >0=chua**」\n"
     "→ Spec TỰ MÂU THUẪN: chỗ này nói điều kiện là `= 1`, chỗ kia nói `> 0`",
     "Nếu điều kiện lọc thật sự là `confirm_count = 1` thì mọi bạn bè có từ 2 tin chưa đọc trở lên "
     "sẽ KHÔNG hiện trong bộ lọc 未確認 — tức là admin bỏ sót đúng những khách hàng nhắn nhiều nhất. "
     "Đây chính xác là hiện tượng khách hàng báo ở #33731. Spec đang mô tả 2 điều kiện khác nhau ở 2 chỗ, "
     "không thể dùng để verify.",
     "TC-CHT-* 「Filter danh sách bạn bè」(TC filter 未確認 — viết theo hướng dữ liệu có 1/2/5 tin chưa đọc) "
     "và 「Bộ đếm chưa xác nhận」(TC bộ đếm tăng dần)",
     "",
     "Nhờ Dev xác nhận điều kiện thực trong truy vấn lọc. Sửa `feature-spec.md:121` cho khớp với "
     "`feature-spec.md:394`. Nếu điều kiện thực là `= 1` thì đây là BUG chưa đóng của #33731 → raise lại. "
     "Bổ sung TC dữ liệu biên: bạn bè có đúng 1 tin, 2 tin và nhiều tin chưa đọc."],

    ["MT-20", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Tính năng AI tạo tin trả lời trên chat 1:1 — spec không nhắc tới",
     "• Tab 「Content: Hiển thị msg」r8, r12: mô tả 「icon AI」trên tin nhắn, khi rê chuột hiện "
     "「AIで返信メッセージを自動生成」với màu #1DE275 + #10CFD6\n"
     "• Tab 「Leftbar+Header」r568-r573: Feature #35547 [01-04-2026] 「[Chat 1:1] Comment update cho tính năng bên AI」 "
     "— gồm đổi vị trí icon bookmark, cho phép sao chép mã LME của bạn bè "
     "「Mục đích: id này để chat gpt get…」, sửa icon vỡ ở màn 14 inch\n"
     "• File master còn có tab riêng 「Chat GPT」(780 dòng TC lá) và 「Bug chatGPT」 về học liệu ChatGPT",
     "• `feature-spec.md` §1 Muc dich: liệt kê các chức năng của chat 1:1 — KHÔNG nhắc AI/ChatGPT\n"
     "• `feature-spec.md` §6 (49 endpoints): không có endpoint nào cho AI\n"
     "• `feature-spec.md` §4 Field Traceability: không có phần tử giao diện nào là icon AI\n"
     "→ Spec chat-11 hoàn toàn không biết tới tính năng này",
     "Mức độ thấp vì đây có thể là tính năng riêng (đã có tab 「Chat GPT」riêng trong file nguồn, "
     "đề xuất tách thành feature khác). Nhưng icon AI nằm NGAY TRÊN từng tin nhắn trong màn chat 1:1 — "
     "tức là một phần tử giao diện của FA-001 mà spec không ghi. Người đọc spec sẽ không biết icon đó tồn tại.",
     "TC-CHT-* 「Reply / quote message」(TC icon trả lời và icon AI)",
     "",
     "Chốt phạm vi: icon AI trên tin nhắn thuộc FA-001 hay thuộc feature ChatGPT riêng. "
     "Nếu thuộc FA-001: bổ sung vào §4 Field Traceability và mô tả luồng. "
     "Nếu tách riêng: tạo feature mới cho 「ChatGPT連携」và gom tab 「Chat GPT」(780 dòng) vào đó "
     "— xem câu hỏi treo trong báo cáo."],
]
